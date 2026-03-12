---
title: "SMTXELF/6.3.0/SMTX ELF 集群安装部署指南"
source_url: "https://internal-docs.smartx.com/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_preface"
sections: 64
---

# SMTXELF/6.3.0/SMTX ELF 集群安装部署指南
## 关于本文档

# 关于本文档

本文档介绍了 SMTX ELF（读作 SmartX ELF）虚拟化软件的使用场景，重点描述了安装部署 SMTX ELF 时的环境要求、网络规划要求和具体的流程。

阅读本文档需了解 SMTX ELF 虚拟化软件，了解虚拟化、网络等云计算相关的技术背景知识，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

**2026-02-04：配合 SMTX ELF 6.3.0 正式发布**

---

## SMTX ELF 简介

# SMTX ELF 简介

SMTX ELF（读作 SmartX ELF）是由北京志凌海纳科技股份有限公司（以下简称“SmartX” ）研发的虚拟化软件，提供计算和网络虚拟化、数据保护及运维管理服务，可帮助企业快速构建稳定可靠的 IT 基础架构。SMTX ELF 功能丰富，可运行在 Intel x86\_64、AMD x86\_64、Hygon x86\_64、兆芯 x86、鲲鹏 AArch64 架构或飞腾 AArch64 架构的服务器上。

---

## SMTX ELF 简介 > 相关概念

# 相关概念

在安装部署 SMTX ELF 前，您需要先了解与其相关的一些概念，以更好地帮助您理解 SMTX ELF 的安装部署流程和功能。

**ELF**

ELF 平台是 SMTX ELF 原生虚拟化计算平台，是该虚拟化软件中基于 KVM 的虚拟化引擎组件。ELF 除提供虚拟机生命周期管理、电源操作、高可用、冷热迁移等基本功能外，通过与存储产品 SMTX ZBS 或超融合产品 SMTX OS 相结合，还能提供秒级快照、模板和克隆等高级的虚拟机服务。

ELF 简单易用，对 SMTX ELF 集群的所有操作均可通过 CloudTower 完成。

**SMTX ELF 节点**

SMTX ELF 软件可运行在物理服务器上，而节点特指运行了 SMTX ELF 软件的单个物理服务器。节点是组成 SMTX ELF 集群的基本单位。

**SMTX ELF 集群**

SMTX ELF 集群属于逻辑概念。在实际生产环境中，一个 SMTX ELF 集群至少由 3 个节点通过网络互连组成。

**主节点**

SMTX ELF 集群中运行了 ZooKeeper 等元数据管理服务的节点。一般对于 5 个节点以内规模的集群，必须规划 3 个主节点；对于 5 个节点及以上规模的集群，必须规划 5 个主节点。

**计算节点**

SMTX ELF 集群中运行了虚拟化组件的节点，用于虚拟机生命周期管理。与主节点不同的是，计算节点不会运行 ZooKeeper 等元数据等关键性服务。

**CloudTower**

SmartX 多集群资源集中管理平台。CloudTower 运行在虚拟机内，通过使用少量的计算和存储资源便可管理上千台虚拟机。除虚拟机生命周期管理、存储管理、网络管理、硬件管理、监控和报警等基本服务外，CloudTower 还提供全局搜索、虚拟机资源优化、事件审计、虚拟机回收站和报表等功能，同时它也提供完整和标准的 RESTful API 和多种语言的 SDK，帮助运维管理员轻松管理和使用多个 SMTX ELF、SMTX OS 和 SMTX ZBS 集群。

**SR-IOV 特性**

SR-IOV (Single Root - I/O Virtualization) 是一种基于硬件的虚拟化解决方案，可提高性能和可伸缩性。

- SR-IOV 允许在虚拟机之间高效共享 PCIe（Peripheral Component Interconnect Express）设备，而且由于在硬件中实现，可以获得能够与主机性能媲美的 I/O 性能。
- 启用了 SR-IOV 并且具有适当的硬件和操作系统支持的 PCIe 设备可以显示为多个单独的物理设备，因此成功达到了单个 I/O 资源被许多虚拟机共享的目的。

SMTX ELF 的 SR-IOV 直通功能将一个支持 SR-IOV 的物理网口虚拟化出多个 SR-IOV 直通网卡并直接挂载给虚拟机使用，大幅降低虚拟机的网络延时。

**LACP 动态链路聚合**

LACP（Link Aggregation Control Protocol，链路聚合控制协议）是一种基于 IEEE802.3ad 标准的实现链路动态聚合与解聚合的协议，属于在链路聚合中常用的协议之一。链路聚合组中启用了 LACP 协议的成员端口通过发送 LACP PDU 报文进行交互，双方对能够发送和接收报文的端口明确并达成一致，确定承担业务流量的链路。此外，当聚合条件发生变化时，如某个链路发生故障，LACP 模式会自动调整聚合组中的链路，组内其他可用成员链路接替故障链路维持负载平衡。因此在不进行硬件升级时，使用 LACP 协议也可以增加设备之间的逻辑带宽，提高网络的可靠性。

动态链路聚合模式需要本端和对端设备同时启用 LACP 协议，所选择的活动接口必须保持一致，然后才能建立链路聚合组 LAG（Link Aggregation Group）。LAG 是指将若干条以太链路捆绑在一起形成一条逻辑链路，也称为 Eth-Trunk 链路。

SMTX ELF 支持 LACP 动态链路聚合功能。在虚拟分布式交换机中，需选择与对端交换机配置 LACP 端口相连的两个物理网口，并且网口绑定模式选择为 OVS bonding 中的 `balance-tcp` 模式。设置完成后即可启用 LACP 动态链路聚合功能。

---

## SMTX ELF 简介 > 安装部署场景

# 安装部署场景

SMTX ELF 集群需搭配 SMTX ZBS 集群或 SMTX OS 集群使用，并通过 CloudTower 进行管理。根据关联存储的集群类型以及当前环境是否已有关联存储和 CloudTower，您可能面临以下场景，不同场景下的安装部署顺序有所不同。

## 关联存储为 SMTX ZBS 集群

- **环境中已有 SMTX ZBS 集群且已关联 CloudTower，仅安装部署 SMTX ELF 集群**

  1. 查阅《SMTX ELF 发布说明》中的版本配套说明，确认已有的 SMTX ZBS 集群和 CloudTower 版本满足要求。
  2. 参考本文档安装部署 SMTX ELF 集群，在[配置关联存储](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_43)时输入已有的 SMTX ZBS 集群的信息，然后将 SMTX ELF 集群关联至已有的 CloudTower。
- **安装部署全新的 SMTX ELF 集群、SMTX ZBS 集群和 CloudTower**

  1. 查阅《SMTX ELF 发布说明》中的版本配套说明，下载适配版本的 SMTX ZBS 块存储安装文件。
  2. 参考《SMTX ZBS 集群安装部署指南》安装部署 SMTX ZBS 集群，并在完成**设置 IPMI 信息**后直接关闭界面。
  3. 参考本文档安装部署 SMTX ELF 集群，在[配置关联存储](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_43)时输入 SMTX ZBS 集群的信息，然后安装全新的 CloudTower 并关联。
  4. 参考《CloudTower 使用指南》的**关联 SmartX 集群**章节将 SMTX ZBS 集群关联至同一 CloudTower 中。

## 关联存储为 SMTX OS 集群

- **已有 SMTX OS 集群且已关联 CloudTower，仅安装部署 SMTX ELF 集群**

  1. 查阅《SMTX ELF 发布说明》中的版本配套说明，确认已有的 SMTX OS 集群和 CloudTower 满足配套版本要求。
  2. 参考《SMTX OS 管理指南》中的**为其他计算端提供块存储（ELF 平台）** 章节，启用**为其他计算端提供块存储**功能，并为 SMTX OS 集群配置独立的接入网络和接入虚拟 IP。
  3. 参考本文档安装部署 SMTX ELF 集群，在[配置关联存储](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_43)时输入 SMTX OS 集群的信息，然后将 SMTX ELF 集群关联至已有的 CloudTower。
- **安装部署全新的 SMTX ELF 集群、SMTX OS 集群和 CloudTower**

  1. 查阅《SMTX ELF 发布说明》中的版本配套说明，下载适配版本的 SMTX OS 安装文件。
  2. 参考《SMTX OS 集群安装部署指南》安装部署 SMTX OS 集群、安装全新的 CloudTower 并关联 SMTX OS 集群。
  3. 参考《SMTX OS 管理指南》中的**为其他计算端提供块存储（ELF 平台）** 章节，启用**为其他计算端提供块存储**功能，并为 SMTX OS 集群配置独立的接入网络和接入虚拟 IP。
  4. 参考本文档安装部署 SMTX ELF 集群，在[配置关联存储](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_43)时输入已有的 SMTX OS 集群的信息，然后将 SMTX ELF 集群关联至已有的 CloudTower。

> **注意**：
>
> 若计划启用虚拟卷的常驻缓存模式，请确保 SMTX ZBS 集群或 SMTX OS 集群已开启常驻缓存模式。

---

## 构建 SMTX ELF 集群的要求

# 构建 SMTX ELF 集群的要求

在规划和部署 SMTX ELF 集群时，请验证您的安装部署环境是否满足以下所有要求。

> **说明**：
>
> 以下所有要求均以构建一个不启用任何高级特性或功能（如 SR-IOV 特性、GPU 直通功能、vGPU 功能）的普通 SMTX ELF 集群为目标进行描述。如果集群需要开启这些高级特性或功能，除参考这些要求外，还需要按照《SMTX ELF 特性说明》中每个特性的**配置要求**小节进行准备。

---

## 构建 SMTX ELF 集群的要求 > 集群规模要求

# 集群规模要求

规划 SMTX ELF 集群时，其规模和主节点需遵照以下要求进行设计。

- 集群节点数

  单个集群最少应包含 3 个节点。

  单个集群的最大节点数不超过 255 个节点。为了发挥集群的最高性能，我们推荐单个集群最多不超过 64 个节点。
- 主节点

  对于少于 5 个节点的集群，必须规划 3 个主节点；对于 5 个节点及以上规模的集群，必须规划 5 个主节点，并且集群的所有主节点在实际环境中应尽量分布在不同的机架和机箱上，以确保更高的可靠性。

  请在规划集群时同时记录每个节点的服务器序列号，并标记出主节点的服务器序列号。

---

## 构建 SMTX ELF 集群的要求 > 网络要求 > 网络类型

# 网络类型

在部署 SMTX ELF 集群时需要创建虚拟分布式交换机并关联网络。

**虚拟分布式交换机（VDS）**

SMTX ELF 利用虚拟化技术将一组物理连通的物理网口（可结合网口绑定实现网络高可用）转化为虚拟化层的分布式交换机（Virtual Distributed Switch, VDS），为主机之间提供网络连接，并为处理各类型系统流量及业务流量提供基础。

SMTX ELF 通过虚拟分布式交换机管理物理网口绑定和 VLAN ID 等，从而实现网络高可用和网络隔离。

**SMTX ELF 网络类型**

虚拟分布式交换机至少需要创建三种类型的虚拟网络：管理网络、存储接入网络和虚拟机网络。每个虚拟网络可使用其所属的虚拟分布式交换机所关联的物理网口（网卡）进行通信。

- **管理网络**：用于管理集群。
- **存储接入网络**：用于计算集群内各节点间数据交换，以及计算集群与存储集群之间的数据交换网络。
- **虚拟机网络**：用于虚拟机业务通信和对外提供服务。

在集群部署结束后，还可以单独为集群配置以下网络：

- **迁移网络**：为虚拟机迁移而单独创建的网络。虚拟机在集群内热迁移时，默认使用存储接入网络进行迁移，单独为集群创建专属的迁移网络后，热迁移的数据将通过该网络进行传输，从而避免占用存储接入网络的带宽。

SMTX ELF 将管理网络、存储接入网络和迁移网络统称为系统网络。

---

## 构建 SMTX ELF 集群的要求 > 网络要求 > 网络部署模式

# 网络部署模式

在规划 SMTX ELF 网络时，可以根据您的部署环境和实际业务需求，选择为集群的系统网络分别设计一个独享的虚拟分布式交换机，并为每个虚拟分布式交换机分别关联物理网口，也可以设计几个系统网络共享同一个虚拟分布式交换机和相应物理网口的带宽。

当集群的两个或以上的系统网络（管理网络、存储接入网络和迁移网络）共享一个虚拟分布式交换机时，即为网络融合部署；当每个系统网络分别独享一个虚拟分布式交换机时，即为网络分离部署。

下面以管理网络、存储接入网络和虚拟机网络为例，介绍使用网络分离部署和网络融合部署的拓扑结构。

- **网络分离部署**

  ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_01.png)
- **网络融合部署**

  ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_02.png)

  上面网络拓扑图中的管理网络、存储接入网络和虚拟机网络共享一个虚拟分布式交换机和两个绑定的物理网口。为了对这三个网络的流量进行隔离，可以给每个网络规划不同的 VLAN ID。

  > **说明**：
  >
  > 无论采用网络分离部署还是网络融合部署模式，虚拟机网络均可选择与管理网络共享一个虚拟分布式交换机或者独享一个虚拟分布式交换机。
  >
  > - 若希望虚拟机网络与管理网络共享虚拟分布式交换机，可在集群部署结束后，登录 CloudTower，在管理网络的虚拟分布式交换机上直接创建虚拟机网络，可参考《SMTX ELF 管理指南》的[创建虚拟机网络](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_103#%E5%88%9B%E5%BB%BA%E8%99%9A%E6%8B%9F%E6%9C%BA%E7%BD%91%E7%BB%9C)小节。
  > - 若希望虚拟机网络独占虚拟分布式交换机，可在集群部署结束后，登录 CloudTower，创建一个虚拟机分布式交换机，并在该虚拟分布式交换机上创建虚拟机网络，可参考《SMTX ELF 管理指南》的[创建虚拟分布式交换机](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_099)和[创建虚拟机网络](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_103#%E5%88%9B%E5%BB%BA%E8%99%9A%E6%8B%9F%E6%9C%BA%E7%BD%91%E7%BB%9C)小节。

---

## 构建 SMTX ELF 集群的要求 > 网络要求 > 网络要求

# 网络要求

SMTX ELF 集群的网络配置须满足以下网络要求。

- 网络带宽

  管理网络带宽须为 1 Gbps 及以上；
  存储接入网络带宽须为 10 Gbps 及以上；
  如果管理网络和存储接入网络使用网络融合部署模式，即两个网络共用相同的网口，则网络带宽须为 10 Gbps 及以上。
- 网络连接

  集群中的所有主机必须连接到 L2 层网络。
- 网络延时

  对于 1400 字节及以上的数据包，集群的存储接入网络 ping 延时在 1 ms 以下。

---

## 构建 SMTX ELF 集群的要求 > 网络要求 > IP 规划要求

# IP 规划要求

在集群的部署阶段和关联 CloudTower 阶段，需要填写 IP 地址、子网掩码、网关、管理虚拟 IP 等，请在安装部署前参考如下要求提前进行规划。

---

## 构建 SMTX ELF 集群的要求 > 网络要求 > IP 规划要求 > 集群节点 IP

# 集群节点 IP

在部署集群阶段，无论 SMTX ELF 集群采用网络融合部署还是分离部署，都需要为集群的每个节点至少规划两个 IP，分别用于管理网络和存储接入网络。

规划管理网络和存储接入网络时，还需提供子网掩码、网关等信息，如下表所示。

| 网络类型 | IP 地址 | 子网掩码 | 网关 | VLAN ID（可选） |
| --- | --- | --- | --- | --- |
| 管理网络 | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| 存储接入网络 | xx.xx.xx.xx | xx.xx.xx.xx | - | xx |

此外，如果需要 SMTX ELF 集成硬件管理能力，还需为每个节点预留 IPMI 管理台 IP。

如果您还有创建迁移网络的需求，在集群部署成功后，还需为每个节点规划迁移 IP，以及对应网络的子网掩码和 VLAN ID 等信息。

网络管理员在分配各节点的管理 IP、存储接入 IP 和迁移 IP 时，必须遵循以下规则：

- 相同类型系统网络中，各节点 IP 必须分配在同一网段且可以正常通信。
- 不同类型系统网络中，各节点 IP 不得分配在同一网段。
- 各节点的 SMTX ELF 存储接入 IP 必须与后续关联的存储集群的存储接入 IP 位于同一网段。
- 如果 SMTX ELF 集群分配的存储接入 IP 与提供存储的 SMTX ZBS 集群或 SMTX OS 集群的接入虚拟 IP 不在同一子网，请在[配置管理和存储接入网络信息](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_62)时启用静态路由。
- IP 地址不能与以下 CIDR 范围内的任何 IP 地址重叠：
  - 169.254.0.0/16
  - 240.0.0.0/4
  - 224.0.0.0/4
  - 198.18.0.0/15
  - 127.0.0.0/8
  - 0.0.0.0/8

规划完以上 IP 后，需要将集群每个节点的 IP 与服务器序列号（即服务标签）一一对应。

---

## 构建 SMTX ELF 集群的要求 > 网络要求 > IP 规划要求 > 集群管理虚拟 IP

# 集群管理虚拟 IP

设置集群的管理虚拟 IP 是为了保证集群管理界面的高可用。访问此 IP 时，可以自动通过集群内任一可用的主机管理 IP 访问集群。

在部署集群成功后，系统在设置参数阶段，会自动跳转至关联 CloudTower 的界面，要求将 SMTX ELF 集群与 CloudTower 进行关联，此时必须输入集群的管理虚拟 IP。

因此，请参考如下要求与建议，提前规划集群的管理虚拟 IP：

- 确保 CloudTower 可以通过管理虚拟 IP 访问集群。
- 管理虚拟 IP 与节点的 SMTX ELF 管理 IP 在同一个子网内。
- 管理虚拟 IP 不能与以下 CIDR 范围内的任何 IP 地址重叠：
  - 169.254.0.0/16
  - 240.0.0.0/4
  - 224.0.0.0/4
  - 198.18.0.0/15
  - 127.0.0.0/8
  - 0.0.0.0/8

---

## 构建 SMTX ELF 集群的要求 > 网络要求 > 防火墙端口要求

# 防火墙端口要求

如果 SMTX ELF 集群的网络之间存在防火墙或集群与外部客户端之间存在防火墙，为确保集群能够正常对外提供服务，防火墙需开放对应的端口，请参考[《SMTX ELF 防火墙端口说明》](/smtxelf/6.3.0/elf_firewall_guide/elf_firewall_guide_preface_generic)提前规划需要开放的端口。

---

## 构建 SMTX ELF 集群的要求 > 硬件要求

# 硬件要求

您需要确保集群内的各个服务器满足**硬件兼容性要求**，以及**物理节点配置要求**。在此之前，您可以先阅读**系统资源占用**，了解系统需占用的计算和存储资源。

---

## 构建 SMTX ELF 集群的要求 > 硬件要求 > 系统资源占用

# 系统资源占用

| **CPU 架构** | **CPU 占用** | **内存占用** |
| --- | --- | --- |
| Intel x86\_64、AMD x86\_64、Hygon x86\_64 或兆芯 x86 架构 | 4 核 | 18.5 GB + 节点内存总量（GB）/ 128 |
| 鲲鹏 AArch64 架构 | 4 核 | 30 GB + 节点内存总量（GB）/ 256 GB × 100 MB |
| 飞腾 AArch64 架构 | 6 核 | 30 GB + 节点内存总量（GB）/ 256 GB × 100 MB |

> **说明**：
>
> - 若节点为主节点，且 CPU 架构不为飞腾 AArch64，系统将额外使用 1 个 CPU 核心。
> - 若服务器未启用超线程，系统将使用 CPU 的物理核心。
> - 若服务器启用了超线程，系统将使用 CPU 的逻辑核心。
> - 计算结果向上取整。

---

## 构建 SMTX ELF 集群的要求 > 硬件要求 > 硬件兼容性要求

# 硬件兼容性要求

确认现场服务器的型号、CPU、硬盘、网卡和存储控制器与 SMTX ELF 兼容，可通过[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)进行查询。

---

## 构建 SMTX ELF 集群的要求 > 硬件要求 > 物理节点配置要求

# 物理节点配置要求

**注意事项**

同一集群内所有物理节点的 CPU 架构和 CPU 供应商必须相同。

| **项目** | **配置要求与建议** |
| --- | --- |
| 处理器 | 单颗 CPU 的最小逻辑核心数为 12，节点逻辑核心数不少于 24，主频不低于 2.0 GHz，推荐 2 路服务器。 |
| CPU 微架构 | - Intel x86\_64：最低版本为 Sandy Bridge - AMD x86\_64：最低版本为 Zen - Hygon x86\_64：最低版本为 Dhyana - 兆芯 x86：最低版本为永丰 - 鲲鹏 AArch64：最低版本为 Taishan v110 - 飞腾 AArch64：最低版本为 ARMv8 |
| 内存 | 至少 64 GB |
| 存储控制器 | 1 个支持硬件 RAID 1 的存储控制器。  **注意**：该存储控制器用于构建系统盘 RAID 1，当仅使用 1 块 SSD 作为系统盘时无需该配件。 |
| 系统盘 | 1 块 240 GB 的数据中心级 SSD，推荐使用 2 块 SSD 及独立的硬件控制器构建 RAID 1。 |
| 网卡 | - 存储接入网络：1 张速率至少为 10 Gbps 的双口网卡。 - 管理网络：1 张速率至少为 1 Gbps 的双口网卡。若管理网络和存储接入网络采用融合部署模式，可复用存储接入网络的网卡。 - 虚拟机网络：1 张速率至少为 1 Gbps 的双口网卡，可复用管理网络的网卡或者使用独立的网卡。 |
| 网口 | 千兆网口和万兆网口数量均不超过 16。 |

---

## 构建 SMTX ELF 集群的要求 > 软件要求

# 软件要求

在正式部署前，请根据服务器的 CPU 架构提前下载如下安装文件。

- SMTX ELF 安装文件（ISO 映像文件）

  - 同一集群内所有节点必须使用相同的安装文件进行安装。
  - 对于 Hygon x86\_64 或鲲鹏 AArch64 架构的服务器，您可以根据实际需求选择 openEuler 或 TencentOS 操作系统的安装文件。
- CloudTower 安装文件（可选）

  - 如果安装部署环境中没有 CloudTower 或已有 CloudTower 不满足配套版本要求，需要下载 CloudTower 安装文件（`tar.gz` 文件）。
    - 对于 Intel x86\_64 或 AMD x86\_64 架构的服务器，您可以根据实际需求选择 CentOS 或 OpenEuler 操作系统的安装文件。
    - 对于 Hygon x86\_64 或鲲鹏 AArch64 架构的服务器，您可以根据实际需求选择 openEuler 或 TencentOS 操作系统的安装文件。
  - 如果安装部署环境中已有符合配套版本要求的 CloudTower，无需下载安装文件。

---

## 构建 SMTX ELF 集群的要求 > 浏览器版本要求

# 浏览器版本要求

安装部署 SMTX ELF 过程中需要使用 Web 浏览器，为保证兼容性，我们建议您使用以下版本的浏览器，同时开启 Cookie 和 JavaScript。

- Google Chrome：91 及以上版本
- Microsoft Edge：107 及以上版本
- Mozilla Firefox：107.0 及以上版本
- Apple Safari：14.1 及以上版本

---

## 构建 SMTX ELF 集群的要求 > 启用高级特性要求

# 启用高级特性要求

SMTX ELF 支持启用 SR-IOV 特性和海光 HCT 特性，启用这两个特性对主机的软硬件配置有特殊的要求，建议您提前了解这些要求。

---

## 构建 SMTX ELF 集群的要求 > 启用高级特性要求 > 启用 SR-IOV 特性

# 启用 SR-IOV 特性

启用集群的 SR-IOV 特性需参考《SMTX ELF 特性说明》中 SR-IOV 特性的[配置要求](/smtxelf/6.3.0/elf_property_notes/elf_property_notes_06)进行准备和配置。

---

## 构建 SMTX ELF 集群的要求 > 启用高级特性要求 > 启用海光 HCT 特性

# 启用海光 HCT 特性

在集群中使用海光 HCT 特性需参考《SMTX ELF 特性说明》中海光 HCT 特性的[配置要求](/smtxelf/6.3.0/elf_property_notes/elf_property_notes_42)进行准备和配置。

---

## 在物理服务器上安装 SMTX ELF

# 在物理服务器上安装 SMTX ELF

通过浏览器访问每个节点的 IPMI 管理台 IP，检查 BIOS 设置，并远程安装 SMTX ELF 软件。

**前提条件**

- 已获得整个集群的规划和完整的 IP 地址分配表，并且为每个节点已配置完 IPMI 管理台 IP。
- 已获取 SMTX ELF ISO 映像文件。

**注意事项**

建议在安装 SMTX ELF 前将所有服务器的引导模式都设置为“UEFI”。

---

## 在物理服务器上安装 SMTX ELF > 检查 BIOS 设置

# 检查 BIOS 设置

对于不同品牌的服务器，进入 BIOS 设置界面的方式和 BIOS 设置的检查项目有较大差异，下文分别以戴尔服务器 R750（CPU 架构为 Intel x86\_64）、浪潮服务器 NF5280M6（CPU 架构为 Intel x86\_64）和中科曙光服务器 R6240H0（CPU 架构为 Hygon x86\_64）为例介绍检查 BIOS 设置的操作。

**注意事项**

如果服务器的 CPU 架构为鲲鹏 AArch64，在检查 BIOS 设置时还需要确保 **CPU Prefetching** 选项为 **Enabled**。

---

## 在物理服务器上安装 SMTX ELF > 检查 BIOS 设置 > 戴尔 Intel x86 服务器

# 戴尔 Intel x86 服务器

请对每个节点执行以下操作。

**操作步骤**

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录该节点的 IPMI 管理台。
2. 登录成功后，找到**虚拟控制台**，单击**启动虚拟控制台**，进入虚拟控制台界面。
3. 在界面顶端单击**启动**，在弹出的**开机控制**窗口中单击 **BIOS 设置**，然后在弹出的**确认启动操作**对话框中单击**是**。
4. 在界面顶端单击**功率**，在弹出的**电源控制**窗口中单击**复位系统（热启动）**，然后在弹出的**确认电源操作**对话框中单击**是**，完成后等待服务器重启。
5. 当服务器进入 **System Setup** 界面时，单击 **System BIOS**，进入 **System BIOS Settings** 界面。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_03.png)
6. 在界面中单击 **Boot Settings**，将 **Boot Mode** 选项设置为 **UEFI**，以提升部署效率。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_04.png)
7. 单击 **Back**，返回 **System BIOS Settings** 界面后，单击 **Processor Settings**，检查并确认 **Virtualization Technology** 选项为 **Enabled**，以确保启用 CPU 虚拟化（VT-x）和 I/O 虚拟化（VT-d）特性。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_05.png)

   > **说明**：
   >
   > IOMMU 的实现因 CPU 和服务器厂商不同而有所差异，请以实际服务器 BIOS 设置界面中的选项为准。本示例中，启用 IOMMU 需将 **Virtualization Technology** 设置为 **Enabled**。
8. 单击 **Back**，返回 **System BIOS Settings** 界面后，单击 **System Profile Settings**，检查并确认 **System Profile** 选项为 **Performance**，以确保关闭电源的节能模式。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_06.png)
9. 检查并确认 **Workload Profile** 选项为 **Virtualization Optimized Performance Profile**，以确保系统针对虚拟化场景优化性能。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_07.png)
10. （可选）若您后续将开启 SR-IOV 特性，单击 **Back**，返回 **System BIOS Settings** 界面后，单击 **Integrated Devices**，检查并确认 **SR-IOV Global Enable** 选项为 **Enabled**。

    ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_08.png)
11. 单击 **Back**，在 **System BIOS Settings** 界面单击 **Finish**，然后在弹出的 **Warning** 对话框中单击 **Yes** 完成设置。

---

## 在物理服务器上安装 SMTX ELF > 检查 BIOS 设置 > 戴尔 AMD x86 服务器

# 戴尔 AMD x86 服务器

请对每个节点执行以下操作。

**操作步骤**

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录该节点的 IPMI 管理台。
2. 登录成功后，找到**虚拟控制台**，单击**启动虚拟控制台**，进入虚拟控制台界面。
3. 在界面顶端单击**启动**，在弹出的**开机控制**窗口中单击 **BIOS 设置**，然后在弹出的**确认启动操作**对话框中单击**是**。
4. 在界面顶端单击**功率**，在弹出的**电源控制**窗口中单击**复位系统（热启动）**，然后在弹出的**确认电源操作**对话框中单击**是**，完成后等待服务器重启。
5. 当服务器进入 **System Setup** 界面时，单击 **System BIOS**，进入 **System BIOS Settings** 界面。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_03.png)
6. 进入 **System BIOS Settings** 界面后，单击 **Processor Settings**，检查并确认 **Logical Processor** 选项为 **Disabled**，以关闭第二个逻辑处理器。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_60_1.png)

   > **说明**:
   >
   > IOMMU 的实现因 CPU 和服务器厂商不同而有所差异，请以实际服务器 BIOS 设置界面中的选项为准。本示例中，**IOMMU Support** 选项默认设置为 **Enabled**，无法修改，无需单独启用 IOMMU。
7. 单击 **Back**，返回 **System BIOS Settings** 界面后，单击 **Integrated Devices**，检查并确认 **SR-IOV Global Enable** 选项为 **Enabled**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_08.png)
8. 单击 **Back**，返回 **System BIOS Settings** 界面后，单击 **System Profile Settings**，检查并确认 **System Profile** 选项为 **Performance**，以确保关闭电源的节能模式。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_60_2.png)

---

## 在物理服务器上安装 SMTX ELF > 检查 BIOS 设置 > 浪潮 Intel x86 服务器

# 浪潮 Intel x86 服务器

请对每个节点执行以下操作。

**操作步骤**

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录该节点的 BMC 控制器。
2. 登录成功后，在左侧导航栏或**快速启动任务**区域单击**远程控制**，然后选择远程控制模式，以选择“H5Viewer”为例，请单击**启动 H5Viewer**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_09.png)

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_10.png)
3. 在弹出的控制台界面中，单击**电源** > **设置启动选项**，在弹出的窗口中，将**设置启动选项**选项设置为 **bios 设置**，并勾选**仅限下一引导**复选框以避免影响后续使用，完成后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_11.png)

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_12.png)
4. 在控制台界面中单击**电源** > **强制关机再开机**，再在弹出的对话框中单击**确定**，然后等待服务器重启。
5. 当服务器进入以下界面时，按“Del”键，稍后服务器将进入 BIOS 设置界面。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_13.png)
6. 在 BIOS 设置界面中，如下，单击 **Socket Configuration**，再单击 **Advanced Power Management Configuration**，然后请按下述步骤进行操作。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_14.png)

   1. 检查并确保 **Power/Performance Profile** 选项为 **Custom**。

      ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_15.png)
   2. 单击 **CPU P state Control**，然后按下图检查所有参数的设置，其中 **CPU Core Flex Ratio** 无需修改，保持默认值即可。

      ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_16.png)
   3. 按“ESC”键，返回 **Advanced Power Management Configuration** 界面后，单击 **Hardware PM State Control**，然后按下图检查所有参数的设置。

      ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_17.png)
   4. 按“ESC”键，返回 **Advanced Power Management Configuration** 界面后，单击 **CPU C state Control**，然后按下图检查所有参数的设置。

      ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_18.png)
   5. 按“ESC”键，返回 **Advanced Power Management Configuration** 界面后，单击 **Package C state Control**，然后按下图检查所有参数的设置。

      ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_19.png)
   6. 按“ESC”键，返回 **Advanced Power Management Configuration** 界面后，单击 **CPU - Advanced PM Tuning**，再单击 **Energy Perf BIAS**，然后按下图检查所有参数的设置。

      ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_20.png)
7. 按“ESC”键，返回至 **Socket Configuration** 页面后，单击 **Processor Configuration**，然后按下图检查所有参数的设置。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_21.png)

   其中需要确认 **VMX** 选项为 **Enabled**，如下图所示：

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_48.png)
8. 按“ESC”键，返回至 **Socket Configuration** 页面后，单击 **Uncore Configuration**，再单击 **Uncore General Configuration**，然后按下图检查所有参数的设置。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_22.png)

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_23.png)
9. 按“ESC”键，返回至 **Socket Configuration** 页面后，单击 **IIO Configuration**，再单击 **Intel VT for Directed I/O (VT-d)**，然后按下图检查所有参数的设置。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_24.png)

   > **说明**：
   >
   > IOMMU 的实现因 CPU 和服务器厂商不同而有所差异，请以实际服务器 BIOS 设置界面中的选项为准。本示例中，启用 IOMMU 需将 **Intel VT for Directed I/O (VT-d)** 设置为 **Enabled**。
10. （可选）若您后续将开启 SR-IOV 特性，请按“ESC”键，返回至 **Socket Configuration** 页面后，切换至 **Advanced** 页面，再单击 **PCI Subsystem Setting**，然后检查并确认 **SR-IOV support** 选项为 **Enabled**。

    ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_25.png)

    ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_26.png)
11. 按“ESC”键，返回至 **Socket Configuration** 或 **Advanced** 页面后，切换至 **Save & Exit** 页面，单击 **Save Changes and Exit**，在弹出的对话框中，单击 **Yes** 完成设置。

    ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_27.png)

---

## 在物理服务器上安装 SMTX ELF > 检查 BIOS 设置 > 中科 Hygon x86 服务器

# 中科 Hygon x86 服务器

1. 打开浏览器，在浏览器的地址栏输入任意一个节点的 IPMI 管理台 IP，登录该节点的 IPMI 管理台。
2. 登录成功后，在左侧导航栏单击**远程控制** > **BIOS 设置**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_28.png)
3. 在 **BIOS 设置**界面中，单击 **CPU 选项**，然后按下图检查所有参数的设置，完成后单击**保存**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_29.png)
4. 单击 **IO 选项**，然后按下图检查所有参数的设置，完成后单击**保存**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_30.png)

   > **说明**：
   >
   > IOMMU 的实现因 CPU 和服务器厂商不同而有所差异，请以实际服务器 BIOS 设置界面中的选项为准。本示例中，启用 IOMMU 需将 **IOMMU** 选项设置为 **Enabled**。
5. 单击**管理选项**，然后按下图检查所有参数的设置，其中 **Bits per second (SOL)**、**Data Bits (SOL)** 和 **Stop Bits (SOL)** 的值无需修改，保持默认值即可，检查完成后单击**保存**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_31.png)
6. 单击**启动选项**，然后检查并确认 **Boot mode** 选项 **UEFI only**，完成后单击**保存**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_32.png)
7. 单击**其他选项**，然后检查并确认 **BIOS Hotkey Support** 选项为 **Enabled**，完成后单击**保存**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_33.png)
8. 单击**导入导出**，在**配置导出**区域单击**导出**，导出 BIOS 设置的配置文件。

   导出的文件包含 BIOS 注册文件（AttributeRegistry.json）和 BIOS 当前选项文件（CurrentSettingBase.json）。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_34.png)
9. 依次登录其他节点的 IPMI 管理台，进入 **BIOS 设置**的**导入导出**界面，然后在**配置导入**区域单击**上传文件**，上传在上一步导出的 BIOS 当前选项文件（CurrentSettingBase.json），以快速完成其他节点的 BIOS 设置。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_35.png)
10. （可选）由于 HCT 功能不支持通过 IPMI 管理台设置，若您后续计划启用海光 HCT 特性，还需要进入服务器的 BIOS 界面执行如下设置。

    1. 选择 **HYGON CBS** 页签，选择 **CPU Common Options**，进入页面后按 **CTRL + F11** 键开启高级设置。
    2. 将 **SEV-ES ASID Space Limit** 选项设置为 **1**，检查并确认 **SMEE Control** 选项为 **Enabled**。

       ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_49.png)
    3. （可选）若后续要为虚拟机挂载 PSP CCP 设备，请将 **Available PSP PCP VQ count** 选项设置为 **4**。

       ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_50.png)
    4. 完成设置后按 **F4** 键，在弹出的对话框中选择 **Yes** 保存设置并退出。

       ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_51.png)

---

## 在物理服务器上安装 SMTX ELF > 挂载 SMTX ELF 映像文件

# 挂载 SMTX ELF 映像文件

1. 在节点的虚拟控制台界面顶端单击**虚拟介质**，在弹出的**虚拟介质**窗口中，单击**连接虚拟介质**。
2. 在**映射 CD/DVD** 字段后单击**选择文件**，选择 SMTX ELF 的映像文件，完成后单击**映射设备**，再单击**关闭**。
3. 在虚拟控制台界面顶端单击**启动**，在弹出的**开机控制**窗口中，选择**虚拟 CD/DVD/ISO**。
4. 在虚拟控制台界面顶端单击**功率**，在弹出的**电源控制**窗口中，单击**电力循环系统（冷启动）** 或 **复位系统（热启动）**，重新启动服务器。

---

## 在物理服务器上安装 SMTX ELF > 安装 SMTX ELF 映像文件

# 安装 SMTX ELF 映像文件

1. 重启服务器后，在如下 SMTX ELF 的安装引导界面中，选择 **Automatic Installation**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_36.png)
2. 请根据[计算资源配置要求](/smtxelf/6.3.0/elf_config_specs/elf_installation_guide/elf_installation_guide_08#%E8%AE%A1%E7%AE%97%E8%B5%84%E6%BA%90%E9%85%8D%E7%BD%AE%E8%A6%81%E6%B1%82)中所规划和记录的系统盘，手动输入系统盘的盘符。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_37.png)

   选择完硬盘后，SMTX ELF 系统将会自动安装，安装所需时间与服务器类型和当前网络条件有关。安装完成后，服务器会自动重启。
3. 服务器重启后，用默认账户 `root` 登录 SMTX ELF 系统。

---

## 部署 SMTX ELF 集群

# 部署 SMTX ELF 集群

SMTX ELF 使用的是向导式的部署界面，您只需按照界面指引，依次完成每个步骤的设置即可成功部署集群。但部署时还需要为某些特性或功能进行特殊设置和操作，建议您在部署集群前，认真阅读[部署须知](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_29)，了解每个特性或功能的注意事项。

---

## 部署 SMTX ELF 集群 > 部署须知

# 部署须知

对于即将部署的集群，必须确保即将关联同一虚拟分布式交换机的所有物理网口互相连通。

对于即将开启的高级特性或功能，请在部署时对照下面列举的各项内容进行设置和操作，部分配置需在部署结束后才能进行，请同时做好相应的记录。

---

## 部署 SMTX ELF 集群 > 部署须知 > 启用 LACP

# 启用 LACP

- 当接入 SMTX ELF 管理网络或存储接入网络的物理交换机启用了 LACP 动态链路聚合时，需要在部署集群的[第 4 步：配置网络](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_37)阶段，为管理网络或存储接入网络创建虚拟分布式交换机时，在**物理网口**区域，需要将的网口的绑定模式设置为 **balance-tcp**。
- 当接入 SMTX ELF 管理网络的物理交换机启用了 LACP 动态链路聚合时，还需要在部署集群前配置 LACP Bond 和管理网络，具体请参考**检查并配置网络环境**章节中的[配置管理网络](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_54)和[配置 LACP Bond](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_55)小节。

---

## 部署 SMTX ELF 集群 > 部署须知 > 配置 VLAN

# 配置 VLAN

- 当物理交换机为 SMTX ELF 管理网络或存储接入网络配置了 VLAN 时，需要在部署集群的[第 4 步：配置网络](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_37)阶段，为管理网络或存储接入网络配置虚拟分布式交换机时，填写 VLAN ID。
- 当物理交换机为管理网络配置了 Trunk VLAN 时，还需要在部署集群前配置管理网络并填写 VLAN ID，具体请参考**检查并配置网络环境**章节中的[配置管理网络](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_54)小节。

---

## 部署 SMTX ELF 集群 > 检查并配置网络环境

# 检查并配置网络环境

在部署集群前，需要根据集群和节点的特点，针对每个节点设置网络环境。SMTX ELF 支持使用 TUI（Terminal User Interface，终端用户界面）配置网络环境，您可以参考本章节进入网络环境配置界面并配置网络环境。

---

## 部署 SMTX ELF 集群 > 检查并配置网络环境 > 进入网络环境配置界面

# 进入网络环境配置界面

1. 通过 IPMI 管理台或 SSH 登录节点。
2. 执行 `sudo -i` 命令切换至 root 账户。
3. 执行 `systemTUI` 命令，进入如下网络环境配置界面。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_53_1.png)

---

## 部署 SMTX ELF 集群 > 检查并配置网络环境 > 配置管理网络

# 配置管理网络

安装 SMTX ELF 映像文件后，节点默认无网络配置，请参考以下步骤为节点配置管理网络。

**注意事项**

- 当接入管理网络的物理交换机启用了 LACP 动态链路聚合时，请先参考[配置 LACP Bond](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_55) 小节创建绑定网口，再配置管理网络。
- 管理网络配置完成后不支持修改。如需变更，请参考[删除 LACP Bond 和管理网络配置](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_58)小节，删除现有配置后重新配置。
- 在集群完成部署前，若重启已配置管理网络的节点，其管理网络配置将失效。请参考[删除 LACP Bond 和管理网络配置](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_58)小节，清理残留配置后重新配置。

**操作步骤**

1. 在 **Network Configure Platform** 界面选择 **Management Network Configure**，单击 **Ok**，系统将显示当前节点上的所有网口及其速率（单位：Mb/s）。若节点已配置 LACP Bond，还会显示一个名称为 `pre_bond` 的网口。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_54_1.png)
2. 根据[网络设备配置要求](/smtxelf/6.3.0/elf_config_specs/elf_installation_guide/elf_installation_guide_08#%E7%BD%91%E7%BB%9C%E8%AE%BE%E5%A4%87%E9%85%8D%E7%BD%AE%E8%A6%81%E6%B1%82)中所规划的网络，选择一个用于管理网络的网口。若接入管理网络的物理交换机启用了 LACP 动态链路聚合，请选择 `pre_bond` 网口，然后单击 **Ok**。

   - 当管理网络和存储接入网络采用分离部署模式时，速率为 1000 Mb/s 及以上的网口可以作为用于管理网络的网口。
   - 当管理网络和存储接入网络采用融合部署模式时，速率为 10000 Mb/s 及以上的网口可以作为用于管理网络和存储接入网络共用的网口。
3. 根据实际规划填写管理网络的 IPv4 地址、子网掩码和默认网关。如果物理交换机为 SMTX OS 管理网络配置了 Trunk VLAN，还需要填写实际规划的 VLAN ID，填写完成后单击 **Confirm**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_54_2.png)
4. 配置成功后，界面将显示 **Success**，单击 **Confirm** 完成配置。

   您可以在 **Network Configure Platform** 界面选择 **List Current Management Network Configure** 查看已配置的管理网络信息。

---

## 部署 SMTX ELF 集群 > 检查并配置网络环境 > 配置 LACP Bond

# 配置 LACP Bond

当接入管理网络的物理交换机启用了 LACP 动态链路聚合时，请参考以下步骤创建绑定网口。

**注意事项**

- 当物理交换机为静态 LACP 模式时，请勿执行以下配置，以免影响网络稳定性。
- LACP Bond 配置完成后不支持修改。如需变更，请参考[删除 LACP Bond 和管理网络配置](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_58)小节，删除现有配置后重新进行配置。
- 在集群完成部署前，若重启已配置 LACP Bond 的节点，其 LACP Bond 配置将失效。请参考[删除 LACP Bond 和管理网络配置](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_58)小节，清理残留配置后重新配置。

**操作步骤**

1. 在 **Network Configure Platform** 界面选择 **LACP Bond Configure (If physical switch configured LACP)**，单击 **Ok**。
2. 在 **LACP Bond Configure** 界面中选择 **Yes**，此时界面上将显示当前节点上的所有网口及其速率（单位：Mb/s）。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_55_1.png)
3. 选择至少两个网口作为绑定网口的成员，单击 **Ok**。

   - 当管理网络和存储接入网络采用分离部署模式时，速率为 1000 Mb/s 及以上的网口可以作为绑定网口的成员。
   - 当管理网络和存储接入网络采用融合部署模式时，速率为 10000 Mb/s 及以上的网口可以作为绑定网口的成员。
4. 配置成功后，界面将显示 **Success** 并生成一个名称为 `pre_bond` 的网口，单击 **Confirm** 完成配置。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_55_2.png)

---

## 部署 SMTX ELF 集群 > 检查并配置网络环境 > 配置 DNS 服务器

# 配置 DNS 服务器

SMTX ELF 支持在部署前配置 DNS 服务器，请参考以下步骤进行操作。

**注意事项**

为节点配置 DNS 服务器后，在**部署集群** > **第 5 步：配置网络** > [配置 DNS 服务器和 NTP 服务器](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_63)时填写的信息将覆盖已配置的 DNS 服务器。

**操作步骤**

1. 在 **Network Configure Platform** 界面选择 **DNS Server Configure**，单击 **Ok**。
2. 选择 **Configure DNS Server**，单击 **Ok**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_56_1.png)
3. 填写 DNS 服务器地址，单击 **Confirm**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_56_2.png)
4. 配置成功后，界面将显示 **Success**，单击 **Confirm** 完成配置。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_56_3.png)

   您可以在 **DNS Server Configure** 界面选择 **List Current DNS Server** 查看已配置的 DNS 服务器。

---

## 部署 SMTX ELF 集群 > 检查并配置网络环境 > 配置主机名称

# 配置主机名称

为节点安装完 SMTX OS 后，您可以根据实际规划修改主机名称，请参考以下步骤进行操作。

**注意事项**

在网络环境配置界面为节点配置主机名称后，在**部署集群** > [第 3 步：配置主机](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_35)阶段添加的主机名将会覆盖已配置的主机名。

**操作步骤**

1. 在 **Network Configure Platform** 界面选择 **Hostname Configure**，单击 **Ok**。
2. 输入新的主机名称，主机名称仅支持大小写英文字母、数字、连字符 (-) 和点（.），填写完成后单击**Ok**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_57_1.png)
3. 配置成功后界面将显示 **Success**，单击 **Confirm** 完成配置。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_57_2.png)

---

## 部署 SMTX ELF 集群 > 检查并配置网络环境 > 删除 LACP Bond 和管理网络配置

# 删除 LACP Bond 和管理网络配置

当需要重新配置管理网络或 LACP Bond 时，请先参考以下步骤删除当前的 LACP Bond 和管理网络配置，完成删除后再重新进行配置。

1. 在 **Network Configure Platform** 界面选择 **Delete LACP Bond and Management Network Configure**。
2. 在 **Delete LACP Bond and Management Network Configure** 界面中选择 **Yes**，系统将删除已配置的 LACP Bond 和管理网络信息。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_58_1.png)
3. 删除成功后，界面将显示 **Success**，单击 **Confirm** 完成配置。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_58_2.png)

---

## 部署 SMTX ELF 集群 > 检查并配置网络环境 > 检查网络环境

# 检查网络环境

为集群中所有节点配置完网络环境后，请在每个节点中执行如下操作，检查网络环境。

1. 使用 root 账户登录节点的 SMTX ELF 系统。
2. 测试节点网络，确保测试节点间的管理网络能够互相连通。
3. 在每个节点中执行 `systemctl status nginx` 命令，确认 nginx 服务已启动。
4. 在每个节点中执行 `systemctl status zbs-deploy-server` 命令，确认 zbs-deploy-server 服务已启动。
5. 将所有节点时间统一调整为当前时间，否则可能因同一集群不同节点的时间设置不同步，而导致集群无法正常工作。可以在每个节点上使用 Linux 命令 `date` 进行调整，例如 `date -s "2022-11-08 15:21:23"`。

---

## 部署 SMTX ELF 集群 > 开始部署

# 开始部署

**前提条件**

- 网卡都已启动，且已获取到 IPv4 或 IPv6 地址。
- 集群内所有节点的时间已统一设置为当前时间。

**操作步骤**

1. 在浏览器的地址栏中输入集群中任意一台节点的管理 IP，进入以下界面。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_38.png)
2. 阅读最终用户软件许可协议，单击**我已阅读并同意服务条款**。

---

## 部署 SMTX ELF 集群 > 第 1 步：集群设置

# 第 1 步：集群设置

1. 在**集群设置**界面，输入集群的名称。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_39.png)
2. 单击**扫描集群**，进入下一步。

---

## 部署 SMTX ELF 集群 > 第 2 步：扫描集群

# 第 2 步：扫描集群

待扫描集群结束后，检查扫描结果，确保要添加到集群的主机已全部显示在扫描结果中。

> **说明**：
>
> SMTX ELF 会优先通过万兆网卡扫描集群发现节点；若万兆网络发现节点失败，则转由通过千兆网络发现节点。如果集群里待部署的节点未显示在扫描结果中，请检查各个节点的网卡是否已启动，以及是否配置 IPv6 地址或 IPv4 地址。

---

## 部署 SMTX ELF 集群 > 第 3 步：配置主机

# 第 3 步：配置主机

1. 勾选要添加到集群的主机，取消勾选其他主机。
2. 可选：修改要添加到集群的主机名，使集群内各个节点的名称更有辨识度。
3. 根据管理 IP 或主机名称辨认并勾选集群的主节点。
4. 为集群内主机统一设置 root 账户和 smartx 账户的密码。
5. 单击**配置网络**，进入下一步。

---

## 部署 SMTX ELF 集群 > 第 4 步：配置网络

# 第 4 步：配置网络

配置网络包含以下步骤：

- 配置虚拟分布式交换机
- 配置管理和存储接入网络信息
- 配置 DNS 服务器和 NTP 服务器

---

## 部署 SMTX ELF 集群 > 第 4 步：配置网络 > 配置虚拟分布式交换机

# 配置虚拟分布式交换机

选择管理网络和存储接入网络所要采用的网络部署模式，系统会根据所选模式自动创建虚拟分布式交换机并关联网络，默认情况下，SMTX ELF 的网络部署模式为分离式部署。

## 选择分离式部署

选择分离式部署时，系统会自动创建两个虚拟分布式交换机并分别关联管理网络和存储接入网络，需要您分别对两个虚拟分布式交换机进行配置。

1. 配置管理网络所关联的虚拟分布式交换机。

   1. 填写虚拟分布式交换机的名称。
   2. 可选：当关联 SMTX ELF 管理网络的物理交换机为管理网络配置了 VLAN 时，请在 **VLAN ID** 字段下填写实际规划的 VLAN ID。
   3. 可选：若要保证管理网络的流量使用需求，可以启用 **QoS 策略**并进行以下设置。

      | 字段 | 说明 | 取值/示例 |
      | --- | --- | --- |
      | 优先级及权重 | 该网络在虚拟分布式交换机中的带宽分配优先级。 - 高（100） - 中（60） - 低（30） - 自定义权重：可设置 0 ~ 100 之间的权重 | “100” |
      | 预留带宽 | 该网络在虚拟分布式交换机中保证预留的带宽。  虚拟分布式交换机中所有虚拟网络的预留带宽之和不允许超过总带宽的 75%。 | “1000 Mbps” |
      | 最大带宽 | 启用**限制带宽**后，将限制该网络可达到的最大带宽。 | “3000 Mbps” |
      | 突发通信量上限 | 启用**限制带宽**后，设置该网络以超出最大带宽的速率进行通信时，最多可完成通信的数据量。 | “300 Mb” |
   4. 在**物理网口**区域的**关联网口**字段下，给每个主机选择用于管理网络的物理网口。

      - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网口，所选的网口速率需为 1 GbE 及以上。
      - 若各个主机的关联网口名称相同，可以在设置完一个主机的关联网口后，单击右侧的 ... 图标，选择**选中其他主机上的同名网口**。
      - 当接入 SMTX ELF 管理网络的物理交换机启用了 LACP 动态链路聚合时，请为需要绑定网口的主机设置**网口绑定模式**为 **balance-tcp**。如下图。

        ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_40.png)

   下图为未配置 VLAN，已启用 Qos 策略，且未设置网口绑定模式的配置界面。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_41.png)
2. 配置存储接入网络所关联的虚拟分布式交换机。

   1. 填写虚拟分布式交换机的名称。
   2. 可选：当关联 SMTX ELF 存储接入网络的物理交换机为存储接入网络配置了 VLAN 时，请在 **VLAN ID** 字段下填写实际规划的 VLAN ID。
   3. 可选：若要保证存储接入网络的流量使用需求，可以启用 **QoS 策略**，设置方式与管理网络相同。
   4. 在**物理网口**区域的**关联网口**字段下，给每个主机选择用于存储接入网络的物理网口。

      - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网口，所选的网口速率需为 10 GbE 及以上。
      - 若各个主机的关联网口名称相同，可以在设置完一个主机的关联网口后，单击右侧的 ... 图标，选择**选中其他主机上的同名网口**。
      - 当关联 SMTX ELF 存储接入网络的物理交换机启用了 LACP 动态链路聚合时，请根据实际需求为需要绑定网口的主机设置**网口绑定模式**。

   下图为未配置 VLAN，已启用 Qos 策略，且未设置网口绑定模式的配置界面。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_42.png)

## 选择融合部署

选择融合部署时，系统会自动创建一个虚拟分布式交换机并同时关联管理网络和存储接入网络，需要您对该虚拟分布式交换机进行配置。

1. 填写虚拟分布式交换机的名称。
2. 可选：当接入 SMTX ELF 管理网络和存储接入网络的物理交换机为管理网络或存储接入网络配置了 VLAN 时，请在对应网络的 **VLAN ID** 字段下填写实际规划的 VLAN ID。
3. 可选：若要保证管理网络或存储接入网络的流量使用需求，可以为对应网络启用 **QoS 策略**并进行以下设置。

   | 字段 | 说明 | 取值/示例 |
   | --- | --- | --- |
   | 优先级及权重 | 该网络在虚拟分布式交换机中的带宽分配优先级。 - 高（100） - 中（60） - 低（30） - 自定义权重：可设置 0 ~ 100 之间的权重 | “100” |
   | 预留带宽 | 该网络在虚拟分布式交换机中保证预留的带宽。  虚拟分布式交换机中所有虚拟网络的预留带宽之和不允许超过总带宽的 75%。 | “1000 Mbps” |
   | 最大带宽 | 启用**限制带宽**后，将限制该网络可达到的最大带宽。 | “3000 Mbps” |
   | 突发通信量上限 | 启用**限制带宽**后，设置该网络以超出最大带宽的速率进行通信时，最多可完成通信的数据量。 | “300 Mb” |
4. 在**物理网口**区域的**关联网口**字段下，给每个主机选择管理网络和存储接入网络共用的物理网口。

   - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网口，所选的网口速率需为 10 GbE 及以上。
   - 当关联 SMTX ELF 管理网络和存储接入网络的物理交换机启用了 LACP 动态链路聚合时，请为需要绑定网口的主机设置**网口绑定模式**为 **balance-tcp**。

---

## 部署 SMTX ELF 集群 > 第 4 步：配置网络 > 配置管理和存储接入网络信息

## 配置管理与存储接入网络信息

1. 在**管理、存储接入 IP** 面板中，填写每个主机实际规划的 SMTX ELF 管理 IP 地址和存储接入 IP 地址。
2. 在**管理网络**面板中，填写为管理网络实际规划的网关和子网掩码。
3. 在**存储接入网络**面板中，填写为存储接入网络实际规划的子网掩码。

> **注意**：
>
> - 当提供存储的 SMTX ZBS 集群的接入虚拟 IP 和 SMTX ELF 集群的存储接入 IP 不在同一子网时，需启用静态路由。
> - SMTX ELF 支持为集群的系统网络设置 MTU，其中编辑存储接入网络 MTU 将造成业务 I/O 较长时间中断。若需修改存储接入网络 MTU，建议在集群部署完成后至业务上线前的窗口期进行，以免对业务造成影响，具体请参考《SMTX ELF 管理指南》的[编辑系统网络](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_108)小节进行操作。

---

## 部署 SMTX ELF 集群 > 第 4 步：配置网络 > 配置 DNS 服务器和 NTP 服务器

# 配置 DNS 服务器和 NTP 服务器

1. 在 **DNS 服务器**面板中，填写 DNS 服务器地址。

   - 若有域名配置需求，请填写实际规划的 DNS 服务器地址。
   - 若无域名配置需求，保留默认地址 127.0.0.1 即可。
2. 在 **NTP 服务器**面板中，选择 NTP 服务器。

   - 若需要使用集群外部 NTP 服务器来同步集群内的主机时间，请选择**使用集群外部 NTP 服务器**，并填写实际规划的 NTP 服务器地址。
   - 若无使用集群外部 NTP 服务器的需求，请选择**使用集群内主机作为 NTP 服务器**。
   - 若计划将集群关联至已有的 CloudTower 且 CloudTower 配置了 NTP 服务器，请确保集群的 NTP 服务器与 CloudTower 的 NTP 服务器的时钟保持同步。
3. 单击**检查配置**，进入下一步操作。

---

## 部署 SMTX ELF 集群 > 第 5 步：检查配置

# 第 5 步：检查配置

检查此前对集群名称、管理 IP 和存储接入 IP、虚拟分布式交换机配置、网络配置、DNS 服务器和 NTP 服务器的设置是否正确。

- 若需要修改设置，可以在左侧的导航栏单击对应的配置步骤，进入对应的配置界面进行修改。
- 若确认设置正确，单击**执行部署**，系统会自动开始部署集群。

---

## 部署 SMTX ELF 集群 > 第 6 步：执行部署

# 第 6 步：执行部署

在**执行部署**界面，可看到每个主机部署的进度，也可以单击**查看日志**，查看部署的详细信息。

- 若集群部署成功，则将显示如下界面。

  ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_43.png)
- 若集群部署失败，则请先根据相关日志定位出失败原因并解决问题，然后在集群的所有节点中执行以下命令清除集群数据，最后再重新[开始部署](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_33)。

  ```
  zbs-deploy-manage clear_deploy_tag

  systemctl restart zbs-deploy-server nginx
  ```

---

## 设置参数（部署成功后）

# 设置参数（部署成功后）

部署完 SMTX ELF 集群后，还需要进行以下设置：

- 设置超级管理员密码
- 设置 IPMI 信息
- 配置关联存储
- 关联 CloudTower

---

## 设置参数（部署成功后） > 第 1 步：设置超级管理员密码

# 第 1 步：设置超级管理员密码

部署成功后，需要先设置集群的超级管理员 root 账户的密码。

**操作步骤**

1. 在集群部署成功后显示的界面，单击**开始部署后配置**。
2. 设置超级管理员 **root** 的密码。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_44.png)
3. 单击**设置 IPMI**，进入下一步。

---

## 设置参数（部署成功后） > 第 2 步：设置 IPMI 信息

# 第 2 步：设置 IPMI 信息

设置主机的 IPMI 信息后，可以在 CloudTower 上管理集群时使用以下功能：

- 机箱拓扑，包括主机和物理盘定位
- 主机风扇、CPU 温度和电源监控

强烈建议用户设置 IPMI 信息，用户可以在这一步进行设置，操作步骤如下。若单击**跳过此步骤**，后续也可在 CloudTower 的集群的管理界面单击**设置** > **IPMI 信息**进行设置。

**操作步骤**

1. 输入各个主机的 IPMI 管理台 IP。

   若需要设置比较多的 IPMI IP，可以在 **IPMI 起始 IP** 字段下输入一个起始 IP，所有的 IPMI IP 将以递增方式自动生成并填充。
2. 输入用户名和密码。

   在**批量设置用户名密码**字段下输入用户名和密码可以使所有主机应用相同的设置。

---

## 设置参数（部署成功后） > 第 3 步：配置关联存储

# 第 3 步：配置关联存储

在设置完成 IPMI 后，需要关联 SMTX OS 集群或 SMTX ZBS 集群，关联成功后，SMTX ELF 集群上的虚拟机可以使用所关联存储集群上的存储资源。

**前提条件**

- 关联存储为 SMTX ZBS 集群时，需确保 SMTX ZBS 集群已设置接入虚拟 IP，并且接入网络与 SMTX ELF 集群的存储接入网络连通。
- 关联存储为 SMTX OS 集群时，需确保 SMTX OS 集群已启用**为其他计算端提供块存储**功能并设置独立的接入网络和接入虚拟 IP，并且接入网络与 SMTX ELF 集群的存储接入网络连通，具体请参考《SMTX OS 管理指南》的**为其他计端提供块存储（ELF 平台）** 章节进行操作。

**操作步骤**

输入 SMTX ZBS 集群或 SMTX OS 集群的接入虚拟 IP、用户名和密码，点击**配置**，配置成功后，单击**关联 CloudTower** 进入下一步。

![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_45.png)

---

## 设置参数（部署成功后） > 第 4 步：关联 CloudTower

# 第 4 步：关联 CloudTower

SMTX ELF 集群的管理服务由 CloudTower 提供，CloudTower 需安装运行在虚拟机内。在设置完 IPMI 信息后，系统将跳转至如下界面，请输入集群超级管理员的用户名和密码并单击下一步，然后开始关联 CloudTower。

![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_44_1.png)

**前提条件**

已获得规划的管理虚拟 IP 地址。

**注意事项**

SMTX ELF 与 CloudTower 的软件版本必须兼容，在安装全新的 CloudTower 或使用现有的 CloudTower 管理平台关联集群前，请务必参考《SMTX ELF 发布说明》中的“SMTX ELF 与 CloudTower 版本配套说明”部分，确认即将安装或关联的 CloudTower 管理平台的版本符合配套要求。

---

## 设置参数（部署成功后） > 第 4 步：关联 CloudTower > 环境中已有 CloudTower

# 环境中已有 CloudTower

若当前环境中已部署 CloudTower，请在**关联 CloudTower** 对话框中选择**已有 CloudTower 环境**，并参考下述步骤设置后，登录 CloudTower 和关联 SMTX ELF 集群。

**注意事项**

若现有的 CloudTower 管理平台版本低于当前 SMTX ELF 所兼容的版本，则需升级 CloudTower 至兼容的版本。CloudTower 软件升级方法，请参见《CloudTower 安装与升级指南》。

**操作步骤**

1. 在**关联 CloudTower** 对话框中设置集群管理虚拟 IP 地址，完成后单击**下一步**。设置集群的管理虚拟 IP 后，即可通过管理虚拟 IP 访问集群中可用的主机，从而保证管理界面的高可用。

   > **说明**：
   >
   > 必须确保 CloudTower 可以通过管理虚拟 IP 访问集群。建议管理虚拟 IP 与节点的管理 IP 在同一个子网内。
2. 在浏览器中输入 CloudTower 的 IP 地址，使用超级管理员 **root** 账户登录 CloudTower。
3. 在 CloudTower 主界面右上角单击 **+ 创建 > 关联集群**，弹出**关联集群**对话框。
4. 在**关联集群**对话框中按照要求填写 SMTX ELF 集群的信息。完成后单击**下一步**。

   ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_45_1.png)

   - **集群管理虚拟 IP**：填写集群的管理虚拟 IP。
   - **管理员用户名**：填写集群的超级管理员账户的用户名。
   - **管理员密码**：填写超级管理员账户对应的密码。
5. 单击**下一步**后，开始加载集群的数据，获取到集群信息后，确认即将关联的集群的信息，包括集群的名称、管理虚拟 IP、软件版本等。
6. 为集群选择所属的数据中心，也可以选择**不加入数据中心**。

   > **说明**：
   >
   > - 用户可以在关联集群的**确认关联集群**阶段，直接创建新的数据中心，然后再将此集群加入该数据中心。
   > - 若用户此时选择**不加入数据中心**，在关联集群后，也可以在 CloudTower 主界面创建一个新的数据中心并重新选择加入。
7. 单击**关联集群**，成功将 CloudTower 与 SMTX ELF 集群完成关联。

   > **注意**：
   >
   > - 完成集群关联后，如果发现该集群有错误或遗漏的配置而需要重新安装部署，必须先取消其与 CloudTower 的关联。
   > - 若 CloudTower 时区与集群时区不一致，建议手动调整时区使两者一致。

**后续操作**

在基于 TencentOS 操作系统的 SMTX ELF 集群部署完成后，需要激活主机的操作系统，请联系 SmartX 售后工程师进行激活。

---

## 设置参数（部署成功后） > 第 4 步：关联 CloudTower > 安装全新的 CloudTower 并关联集群

# 安装全新的 CloudTower 并关联集群

若当前环境中没有 CloudTower，请在**关联 CloudTower** 对话框中选择**全新 CloudTower 环境**，系统将自动为 CloudTower 创建虚拟机，并启动安装 CloudTower。安装完后可以关联 SMTX ELF 集群。

**前提条件**

- 根据服务器的 CPU 架构提前下载对应的 `tar.gz` 格式的 CloudTower 安装映像文件。
- 已规划 CloudTower 的 IP 地址、子网掩码和网关。确保 CloudTower IP 与 SMTX ELF 集群的管理虚拟 IP 正常连通。

**操作步骤**

1. 在**关联 CloudTower** 对话框中设置集群管理虚拟 IP 地址，完成后单击**下一步**。设置集群的管理虚拟 IP 后，即可通过管理虚拟 IP 访问集群中可用的主机，从而保证管理界面的高可用。

   > **说明**：
   >
   > 必须确保 CloudTower 可以通过管理虚拟 IP 访问集群。建议管理虚拟 IP 与节点的管理 IP 在同一个子网内。
2. 上传 CloudTower 的安装映像文件。将本地 `tar.gz` 格式的 CloudTower 安装映像文件拖曳至文件区域，或者单击**选择文件**，选择从本地上传文件。
3. 选择 CloudTower 环境的配置。选择**低配**或**高配**时，需考虑待管理的集群数量、主机和虚拟机规模，并确保 SMTX ELF 集群有足够的 CPU 和内存、其关联的 SMTX ZBS 集群或 SMTX OS 集群有足够的存储空间可分配给部署 CloudTower 的虚拟机（如下表所示）。

   | **配置等级** | **CloudTower 管理能力** | **CloudTower 所在的虚拟机占用的系统资源** |
   | --- | --- | --- |
   | **低配** | - 10 个集群 - 100 台主机 - 1000 个虚拟机 | - 4 核 vCPU - 12 GiB 内存 - 100 GiB 存储空间 |
   | **高配** | - 100 个集群 - 1000 台主机 - 10000 个虚拟机 | - 8 核 vCPU - 19 GiB 内存 - 400 GiB 存储空间 |
4. 设置 CloudTower 的 IP 地址和子网掩码、网关信息。
5. 设置 CloudTower 的组织名称，以及超级管理员 **root** 的密码。
6. 单击**下一步**，开始安装 CloudTower。安装完成后，系统将弹出提示框，单击**打开 CloudTower**。15 秒后系统提示即将离开此网站，单击**离开**后将自动跳转至 CloudTower 环境。
7. 在 CloudTower 中关联 SMTX ELF 集群。

   1. 在浏览器中输入 CloudTower 的 IP 地址，使用超级管理员 **root** 账户登录 CloudTower。
   2. 在 CloudTower 主界面右上角单击 **+ 创建 > 关联集群**，弹出**关联集群**对话框。

      ![](https://cdn.smartx.com/internal-docs/assets/d8c32465/elf_installation_guide_45_1.png)
   3. 在**关联集群**对话框中按照要求填写 SMTX ELF 集群的信息。完成后单击**下一步**。

      - **集群管理虚拟 IP**：填写集群的管理虚拟 IP。
      - **管理员用户名**：填写集群的超级管理员账户的用户名。
      - **管理员密码**：填写超级管理员账户对应的密码。
   4. 单击**下一步**后，开始加载集群的数据，获取到集群信息后，确认即将关联的集群的信息，包括集群的名称、管理虚拟 IP、软件版本、以及使用的虚拟化平台等。
   5. 为集群选择所属的数据中心。也可以选择**不加入数据中心**。

      > **说明**：
      >
      > - 用户可以在关联集群的**确认关联集群**阶段，直接创建新的数据中心，然后再将此集群加入该数据中心。
      > - 若用户此时选择**不加入数据中心**，在关联集群后，也可以在 CloudTower 主界面创建一个新的数据中心并重新选择加入。
   6. 单击**关联集群**，将 CloudTower 与 SMTX ELF 集群完成关联。

      > **注意**：
      >
      > - 完成集群关联后，如果发现该集群有错误或遗漏的配置而需要重新安装部署，必须先取消其与 CloudTower 的关联。
      > - 若 CloudTower 时区与集群时区不一致，建议手动调整时区使两者一致。

**后续操作**

- 在基于 TencentOS 操作系统的 SMTX ELF 集群部署完成后，需要激活主机的操作系统，请联系 SmartX 售后工程师进行激活。
- CloudTower 4.8.0 及以上版本支持高可用功能，如需启用，请在集群部署完成后参考对应版本《CloudTower 使用指南》的**管理 CloudTower 高可用**章节操作。

---

## 在 CloudTower 中查看集群状态

# 在 CloudTower 中查看集群状态

关联 SMTX ELF 集群后，可进入集群的**概览**界面，查看集群的告警信息。如果**严重警告**信息为 0，则表示 SMTX ELF 集群运行正常。

> **说明**：
>
> SMTX ELF 内嵌虚拟机服务，并为其提供了虚拟机工具。关于虚拟机服务和虚拟机工具对 Guest OS 的⽀持与兼容性，请参见《SMTX ELF 虚拟机服务兼容性指南》。

---

## SMTX ELF 节点的本地账户与默认安全设置说明 > SMTX ELF 节点的本地账户说明

# SMTX ELF 节点的本地账户说明

SMTX ELF 节点支持以下三种本地账户：

| 本地账户 | 说明 | 注意事项 |
| --- | --- | --- |
| root | 默认账户，默认禁止 SSH 远程登录。您可以使用该账户管理 SMTX ELF 节点。 | - 请勿删除该账户。 - 强烈建议不要开启 root 账户通过 SSH 远程登录的权限。 - 以命令行方式升级集群时必须拥有 root 权限。 |
| smartx | 默认账户，默认支持 SSH 远程登录。您可以使用该账户通过 SSH 协议远程连接到 SMTX ELF 节点。 | - 请勿删除该账户。 - 请勿更改 `/etc/sudoers` 里针对该账户的配置。 - 以该账户登录节点后，必须切换为 root 账户再执行运维操作。执行 `sudo su` 命令可免密码切换。 |
| 其他本地账户 | 由 root 账户创建的其他账户，账户权限由 root 账户决定。您可自行创建新的本地账户用于 SSH 远程登录。 | - |

---

## SMTX ELF 节点的本地账户与默认安全设置说明 > SMTX ELF 节点的默认安全设置说明

# SMTX ELF 节点的默认安全设置说明

SMTX ELF 系统安装完成后，会默认对 SMTX ELF 节点进行如下安全设置。

| 设置项 | 默认设置说明 |
| --- | --- |
| 连接超时设置 | 登录节点后，如果在 30 分钟内未进行操作，与节点的连接将自动断开。 |
| 密码强度设置 | 除 root 和初始 smartx 外的账户设置密码时：  - 密码长度必须至少为 8 个字符。 - 密码必须至少包含 1 个数字、1 个大写字母、1 个小写字母和 1 个特殊字符。 - 重设的密码不能与前 5 次的密码重复。 |
| 登录失败后锁定设置 | 连续 5 次登录失败后，账户将被锁定 10 分钟。 |
| SSH 设置 | - 禁止 root 账户直接 SSH 远程登录节点。 - SSH 服务的 MACs 和 Ciphers 配置支持 CTR 和 SHA2 算法，不支持 CBC、MD5 和 SHA1 算法。 |

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
