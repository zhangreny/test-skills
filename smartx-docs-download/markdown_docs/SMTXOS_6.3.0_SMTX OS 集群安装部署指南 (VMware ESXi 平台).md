---
title: "SMTXOS/6.3.0/SMTX OS 集群安装部署指南 (VMware ESXi 平台)"
source_url: "https://internal-docs.smartx.com/smtxos/6.3.0/vmware_installation_guide/preface_vmware_installation_guide"
sections: 107
---

# SMTXOS/6.3.0/SMTX OS 集群安装部署指南 (VMware ESXi 平台)
## 关于本文档

# 关于本文档

本文档介绍了 SMTX OS（读作 SmartX OS）超融合软件的使用场景，重点描述了当使用 VMware ESXi 平台进行部署时，安装部署 SMTX OS 的环境要求、网络规划要求和具体的流程。

阅读本文档需了解 SMTX OS 超融合软件，了解虚拟化、块存储和网络等云计算相关的技术背景知识，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

**2026-02-04：配合 SMTX OS 6.3.0 正式发布**

相较于 SMTX OS 6.2.0，本版本主要进行了如下更新：

- **SMTX OS 简介** > **相关概念**：更新存储分层模式的概念。
- **构建 SMTX OS 集群的要求** > **硬件要求**：
  - **系统资源占用** > **系统对 SCVM 的 CPU 和内存的占用**：更新占用的数值及说明。
  - **ESXi 主机配置要求** > **存储设备配置要求**：更新存储配置分类及相关要求说明。
- **在 ESXi 节点上创建 SCVM 虚拟机** > **启用 RDMA 功能的配置要求**：更新 CPU 的要求说明。
- **部署 SMTX OS 集群**：
  - **第 1 步：集群设置**：新增为静态数据加密设置加密加速的步骤。
  - **第 4 步：配置存储**：新增选择系统盘用途的步骤，并更新其余物理盘用途的说明。
- **设置参数（部署成功后）** > **关联 CloudTower**：更新设置完 IPMI 信息后系统跳转的界面截图和对应的设置步骤。

---

## SMTX OS 简介

# SMTX OS 简介

SMTX OS（读作 SmartX OS）是由北京志凌海纳科技股份有限公司（以下简称 “SmartX” ）研发的超融合软件，提供分布式块存储、计算虚拟化和网络、数据保护及运维管理服务，可帮助企业快速构建稳定可靠的 IT 基础架构。SMTX OS 功能丰富且性能卓越，可运行在 x86\_64/AArch64 架构的服务器上，目前已被金融、制造和医疗等行业的相关企业广泛使用。

---

## SMTX OS 简介 > 相关概念

# 相关概念

在安装部署 SMTX OS 前，您需要先了解与其相关的一些概念，以更好地帮助您理解 SMTX OS 的安装部署流程和功能。

**超融合**

超融合是一种 IT 基础架构，通过将计算虚拟化、分布式存储、网络及各类运维管理等服务融合部署在通用的 x86\_64/AArch64 架构的服务器上，大幅简化基础设施类资源的交付、上线和运维。

**SMTX OS 节点**

SMTX OS 软件可运行在物理服务器上或者虚拟机中，而节点特指运行了 SMTX OS 软件的单个物理服务器或者虚拟机。节点是组成 SMTX OS 集群的基本单位。

**SMTX OS 集群**

SMTX OS 集群属于逻辑概念。在实际生产环境中，一个 SMTX OS 集群至少由 3 个节点通过网络互连组成。

**ELF**

ELF 平台即指 SMTX OS 原生虚拟化计算平台，是当 SMTX OS 以超融合形态直接部署在 x86\_64/AArch64 架构的服务器上时，该超融合软件中基于 KVM 的虚拟化引擎组件。ELF 除提供虚拟机生命周期管理、电源操作、高可用、冷热迁移等基本功能外，通过与存储组件 ZBS 相结合，还能提供秒级快照、模板和克隆等高级的虚拟机服务。

ELF 简单易用，对 SMTX OS 集群的所有操作均可通过 CloudTower 完成。

**ZBS**

SMTX OS 内置的分布式块存储软件，它负责接管服务器的所有存储资源（包括所有的 SSD 和 HDD），将多个服务器的存储资源池化，构建统一的存储池，为虚拟机提供存储服务。

**VMware ESXi 平台**

ESXi 是 VMware 公司（目前属于 Broadcom 公司）推出的一套服务器虚拟化解决方案（vSphere）中的一个关键组件，可独立安装和运行在物理服务器上，是 VMware 的裸机虚拟机管理程序。VMware ESXi 平台特指运行着 ESXi 程序的虚拟化平台。

**SCVM**

当 SMTX OS 结合 VMware ESXi 平台以超融合的形态进行部署时，SMTX OS 软件需安装在一种特殊的虚拟机中，该虚拟机即为 SCVM（SmartX Controller Virtual Machine）。

SCVM 能直接管理主机上的硬盘设备（SSD/HDD），使得这些硬盘统一由 ZBS 负责管理，并通过网络将 SCVM 组成分布式存储集群，为 VMware ESXi 主机中的虚拟机提供存储服务。

**CloudTower**

SmartX 多集群资源集中管理平台。CloudTower 运行在虚拟机内，通过使用少量的计算和存储资源便可管理上千台虚拟机。除虚拟机生命周期管理、存储管理、网络管理、硬件管理、监控和报警等基本服务外，CloudTower 还提供全局搜索、虚拟机资源优化、事件审计、虚拟机回收站和报表等功能，帮助运维管理员轻松管理和使用多个 SMTX OS 和 SMTX ZBS 集群。

**SMTX OS 双活集群**

启用双活特性的 SMTX OS 集群简称 “SMTX OS 双活集群”。SMTX OS 双活集群以拉伸形态部署，由两个可用域和一个仲裁节点组成。两个可用域一般位于同一个城市有一定距离的物理节点所在区域，分为优先可用域和次级可用域。每个可用域至少包含 3 个节点，并且均可以完全独立地提供计算和存储服务，集群正常工作时业务主要运行在优先可用域上。

为了保证选主类服务正常运行，并使得业务在优先或次级可用域中自动切换，需要部署一个额外的仲裁节点，这个节点仅仅参与选主算法，而不存放任何数据。仲裁节点可以是物理机或虚拟机，需要部署在与优先可用域及次级可用域不同的物理故障区。

两个可用域与仲裁节点相互间通过网络连接通信。当一个可用域失效后，另一个可用域仍可以继续提供服务，从而获得可用域级别的容灾能力。

**主节点**

SMTX OS 集群中额外运行元数据服务的节点。

**存储节点**

SMTX OS 集群中未运行元数据服务的普通节点。

**副本数**

使用多副本技术提供数据冗余，一份数据会在不同主机上保存多个副本，以提高数据的可靠性和安全性。

**纠删码**

使用一定的算法对 K 个原始数据块计算出 M 个校验块，在节点或硬盘故障后，使用其中 K 个数据块和校验块来重建数据块，从而提供对应的容错能力。纠删码仅支持在存储分层模式下使用。

**容量规格**

SMTX OS 按照不同的物理盘容量上限区分了三种容量规格，其中小容量规格单个主机最大支持 50 TB，标准容量规格单个主机最大支持 128 TB，大容量规格单个主机最大支持 256 TB。小容量规格仅适用于从 SMTX OS 6.1.0 以下版本升级上来的集群，具体可参考《SMTX OS 升级指南》的[确认数据分区容量和存储引擎版本](/smtxos/6.3.0/upgrade_guide/upgrade_guide_02#%E7%A1%AE%E8%AE%A4%E6%95%B0%E6%8D%AE%E5%88%86%E5%8C%BA%E5%AE%B9%E9%87%8F%E5%92%8C%E5%AD%98%E5%82%A8%E5%BC%95%E6%93%8E%E7%89%88%E6%9C%AC)章节。

**存储分层模式**

把集群内的存储设备分为缓存层和容量层，其中容量层是所有节点数据分区构成的空间，用于存放冷数据，冷数据根据设定的数据冗余策略，以副本或纠删码的形态存储。不同存储配置下缓存层的构成不同。

当节点为混闪配置、多种类型 SSD 全闪配置或单一类型多种属性 SSD 全闪配置时，缓存盘与数据盘将独立部署，高速介质为缓存，低速介质为容量。数据会以副本形态先存入写缓存，待数据变冷后下沉到容量层。

- 混闪配置和多种类型 SSD 全闪配置：缓存层将分为写缓存和读缓存。写缓存用于存放新写入的数据，读缓存用于存放被频繁访问的已下沉的数据，写缓存与读缓存的容量比为 8：2。
- 单一类型多种属性 SSD 全闪配置：缓存层均为写缓存，用于存放新写入的数据。

当节点均为单一类型 SSD 全闪配置时，缓存与数据将共享所有物理盘，每块物理盘的部分容量作为缓存使用，缓存分区与数据分区的容量比为 1：9。此时缓存层均为写缓存，用于存放新写入的数据，副本卷将仅使用容量层，不使用缓存层。

**存储不分层模式**

不设置缓存层。除了含有系统分区的物理盘，剩余的所有物理盘都作为数据盘使用。使用存储不分层模式时只能用全闪配置。

**RDMA 功能**

RDMA（Remote Direct Memory Access）技术是一种直接内存访问技术，节点间进行数据传输时，可以绕过双方的操作系统内核，通过网络直接访问其内存数据。由于不经过操作系统，可以节省大量 CPU 资源，提高系统吞吐量，并降低系统的网络通信延时。

SMTX OS 通过引入 RDMA 能力来达到降低远程节点的写入延时，提高集群的整体性能的目的，成功改进延时和吞吐能力两个性能指标。

**VAAI-NAS 插件**

SmartX 开发的一款获得 VMware 官方认证的插件。当 SMTX OS 结合 VMware ESXi 平台以超融合的形态进行部署时，使用此插件可以支持虚拟机磁盘的厚置备模式 (thick mode) 和快速克隆等功能。

**常驻缓存模式**

SMTX OS 支持常驻缓存模式，将虚拟卷（ELF 平台）或 NFS 文件（VMware ESXi 平台）中的数据保留在缓存层，从而获得更稳定的高性能。

---

## SMTX OS 简介 > 部署形态

# 部署形态

SMTX OS 以超融合架构进行部署时，支持以下两种部署形态：

- **采用 SmartX 原生虚拟化 ELF 部署**

  SMTX OS 直接运行在物理服务器上，通过 iSCSI 或 vhost 接入协议为虚拟机提供虚拟磁盘进行存储。

  当所有节点安装完 SMTX OS 软件并实现集群初始化后，就可以提供原生的 SMTX 虚拟机服务和存储服务。
- **搭配 VMware ESXi 虚拟化部署**

  SMTX OS 与 VMware ESXi 平台相结合，运行在 ESXi 主机的 SCVM 虚拟机内，通过 NFS 协议为 ESXi 主机提供存储服务，而虚拟机服务则由 VMware ESXi 提供。

本文档仅介绍 SMTX OS 搭配 VMware ESXi 虚拟化部署的流程和步骤。采用 SmartX 原生虚拟化 ELF 部署 SMTX OS 的流程和步骤，请参见文档[《 SMTX OS 集群安装部署指南（ELF 平台）》](/smtxos/6.3.0/elf_installation_guide/preface_elf_installation_guide)。

---

## SMTX OS 简介 > 部署选项

# 部署选项

一般组成未启用双活特性的 SMTX OS 集群的所有节点均位于同一个数据中心，但是在一些特殊场景下，为了灾备需要，您也可以选择将 SMTX OS 以拉伸形态部署在两个数据中心，组成 SMTX OS 双活集群，确保其中一个数据中心故障时，另外一个数据中心快速恢复业务，以获得 RPO（数据恢复点目标）为 0，RTO（恢复时间目标）为分钟级的站点失效容错能力。若选择部署 SMTX OS 双活集群，需先单独购买双活的许可。

未启用双活特性的 SMTX OS 集群和 SMTX OS 双活集群都支持采用原生虚拟化 ELF 部署和搭配 VMware ESXi 虚拟化进行部署。本文档仅介绍搭配 VMware ESXi 虚拟化部署未启用双活特性的 SMTX OS 集群的流程和步骤，关于 SMTX OS 双活集群的更多详细信息和部署操作，可查看[《SMTX OS 双活集群安装部署指南（ELF 平台）》](/smtxos/6.3.0/elf_multiactive_installation/elf_multiactive_installation_preface)和[《SMTX OS 双活集群安装部署指南（VMware ESXi 平台）》](/smtxos/6.3.0/vmware_multiactive_installation/vmware_multiactive_installation_preface)。

---

## 构建 SMTX OS 集群的要求

# 构建 SMTX OS 集群的要求

在规划和部署使用 VMware ESXi 平台的 SMTX OS 集群时，请验证您的安装部署环境是否满足以下要求。

> **说明**：
>
> - 若集群不启用任何高级特性或功能，仅参考本章节中的集群规模、网络、硬件、软件和浏览器版本要求即可。
> - 若集群需启用双活特性，请直接参考[《SMTX OS 双活集群安装部署指南（VMware ESXi 平台）》](/smtxos/6.3.0/vmware_multiactive_installation/vmware_multiactive_installation_preface)了解构建集群的要求和部署操作。
> - 若集群不启用双活特性，但需启用 RDMA 功能、常驻缓存模式或机架拓扑感知，请参考本章节中的所有要求，包括[启用高级功能的要求](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_15)。

---

## 构建 SMTX OS 集群的要求 > 集群规模要求

# 集群规模要求

规划 SMTX OS 集群规模时，需遵照以下要求设计集群节点数、冗余策略和主节点。

- 集群节点数

  单个集群最少应包含 3 个节点。为了发挥集群的最高性能，我们推荐单个集群最多不超过 64 个节点。
- 冗余策略

  SMTX OS 支持使用副本或纠删码的冗余策略，集群节点数不同时，推荐的副本数或纠删码配比也有所不同。

  - 副本

    SMTX OS 支持 2 副本或者 3 副本的冗余策略。

    一般情况下，推荐使用 3 副本，您也可根据实际情况设计冗余策略。
  - 纠删码

    纠删码要求集群至少包含 4 个节点。集群部署完成后，如果选择纠删码作为集群的默认冗余策略，系统会根据集群内的节点数量默认选择推荐的纠删码配比，您也可以根据实际需求自定义纠删码配比。不同节点数下的推荐配比和可自定义配比如下。

    | **节点数** | **推荐配比 K + M** | **自定义配比 K** | | | |
    | --- | --- | --- | --- | --- | --- |
    | **M = 1** | **M = 2** | **M = 3** | **M = 4** |
    | 4 | 2 + 1 | 2 | - | - | - |
    | 5 | 2 + 2 | 2 | 2 | - | - |
    | 6 | 2 + 2 | 2、4 | 2 | - | - |
    | 7 | 4 + 2 | 2、4 | 2、4 | - | - |
    | 8 | 4 + 2 | 2、4、6 | 2、4 | 4 | - |
    | 9 | 4 + 2 | 2、4、6 | 2、4、6 | 4 | 4 |
    | 10 | 4 + 2 | 2、4、6、8 | 2、4、6 | 4、6 | 4 |
    | 11 | 8 + 2 | 2、4、6、8 | 2、4、6、8 | 4、6 | 4、6 |
    | 12 | 8 + 2 | 2、4、6、8、​10 | 2、4、6、8 | 4、6、8 | 4、6 |
    | 13 | 8 + 2 | 2、4、6、8、​10 | 2、4、6、8、​10 | 4、6、8 | 4、6、8 |

    > **说明**：
    >
    > - 数据块数量仅支持偶数，当校验块数量为 1 或 2 时，数据块数量的取值范围为 2 ～ 22；当校验块数量为 3 或 4 时，数据块数量的取值范围为 4 ～ 8。
    > - 系统最大支持的校验块数量为 4。
    > - 可选择的纠删码配比需满足：数据块数量与校验块数量之和加一不超过可提供存储服务（存储服务健康且未处于移除中状态）的节点数。
    > - 当集群节点数大于等于 11 时，均推荐 8 + 2 的纠删码配比。
- 主节点

  对于少于 5 个节点的集群，必须规划 3 个主节点；对于 5 个节点及以上规模的集群，必须规划 5 个主节点，并且集群的所有主节点应尽量分布在不同的机架和机箱上，以确保更高的可靠性。

  请在规划集群时同时记录每个节点的服务器序列号，并标记出主节点的服务器序列号。

---

## 构建 SMTX OS 集群的要求 > 网络要求 > SMTX OS 网络

# SMTX OS 网络

搭配 VMware ESXi 虚拟化部署时，SMTX OS 运行在 ESXi 主机的 SCVM 虚拟机上，并复用 VMware vSphere 本身的虚拟网络功能。

在 SCVM 上需创建 3 个网络适配器，并分别配置到 vSphere 虚拟交换机（vSwitch）对应的端口组中，分别给管理网络、存储网络和 NFS 网络使用。

## SMTX OS 使用的虚拟交换机

通过在每台 ESXi 主机中创建以下标准虚拟交换机，可分别实现管理网络、存储网络和 NFS 网络的通信。

- **管理网络虚拟交换机 —— vSwitch0**

  ESXi 安装完成后，会默认创建一个用于 ESXi 管理和 SCVM 管理的虚拟交换机，默认名称为 vSwitch0。vSwitch0 关联的 vmnic 为 ESXi 管理网络对应的物理网口。vSwitch0 中已默认创建了一个网络标签（即网络名称）为 Management Network 的 VMkernel 和一个名称为 VM Network 的虚拟机端口组，分别用于 ESXi 管理网络和 SCVM 管理网络。
- **存储网络虚拟交换机 —— vSwitch1**

  默认情况下，需要为存储网络单独创建一个虚拟交换机（ vSwitch1）。若存储网络与管理网络共用相同的物理网卡，可复用管理网络虚拟交换机 vSwitch0。存储网络虚拟交换机需关联至少一个带宽为 10 Gbps 及以上的物理网口。

  存储网络虚拟机交换机上需创建一个网络标签固定为 **ZBS** 的虚拟机端口组，用于为 SCVM 提供存储网络。
- **NFS 网络虚拟交换机**

  NFS 网络虚拟交换机用于创建 NFS 网络和 NFS VMkernel。由于 NFS 网络仅供 ESXi 主机与本主机上的 SCVM 虚拟机进行通信，所以 NFS 网络虚拟交换机不需要关联任何物理网卡。

  NFS 网络虚拟机交换机上需创建一个网络标签固定为 **NFS** 的虚拟机端口组，用于为 SCVM 提供 NFS 网络。

## SMTX OS 使用的网络类型

您需要创建一系列的 VMkernel 或虚拟机端口组作为系统网络，用于节点之间的通信。

- **ESXi 管理网络 —— Management Network（VMkernel）**

  ESXi 管理网络对应的是 vSwitch0 中名为 Management Network 的 VMkernel，用于 ESXi 主机之间的管理流量通信。ESXi 管理网络在 ESXi 的安装过程中自动创建，您可配置该网络的 IP 地址、子网掩码、网关和 VLAN ID 信息。
- **SCVM 管理网络 —— VM Network（虚拟机端口组）**

  SCVM 管理网络对应的是 vSwitch0 中名为 VM Network 的虚拟机端口组，用于给 SCVM 虚拟机和 CloudTower 虚拟机使用，并处理 SCVM 虚拟机之间的管理流量。

  在每个 SCVM 虚拟机中，需创建一个网络适配器并关联 SCVM 管理网络。后续可在此网络中配置 SCVM 的管理网络 IP、子网掩码、网关和 VLAN ID 信息。

  在 CloudTower 虚拟机中，需创建一个网络适配器并关联 SCVM 管理网络。后续可在此网络中配置 CloudTower IP、子网掩码、网关和 VLAN ID 信息。
- **ESXi 存储网络 —— ZBS-vmk（VMkernel）**

  ESXi 存储网络对应 vSwitch1 中名为 ZBS-vmk 的 VMkernel，用于各 ESXi 主机间的数据交换。您可配置该网络的 IP 地址、子网掩码、网关和 VLAN ID 信息。
- **SCVM 存储网络 —— ZBS（虚拟机端口组）**

  SCVM 存储网络对应存储网络虚拟交换机中名为 **ZBS** 的虚拟机端口组。

  在每个 SCVM 虚拟机中，需创建一个网络适配器并关联 SCVM 存储网络。后续可在此网络中配置 SCVM 的存储网络 IP、子网掩码、网关和 VLAN ID 信息。
- **NFS 网络（虚拟机端口组）**

  NFS 网络对应 NFS 网络虚拟交换机中名为 **NFS** 的虚拟机端口组，用于 ESXi 主机和本主机上的 SCVM 虚拟机进行通信。

  在每个 SCVM 虚拟机中，需创建一个网络适配器并关联 NFS 网络。NFS 网络的 IP 地址固定为 192.168.33.2，子网掩码为 255.255.255.0，不允许更改。
- **NFS VMkernel（连接 NFS 网络的 VMkernel）**

  NFS VMkernel 对应一个 VMKernel 网络适配器，用于 SCVM 连接 NFS 网络。NFS Kernel 的 IP 地址固定为 192.168.33.1，子网掩码为 255.255.255.0，不允许更改。

> **注意**：
>
> 若启用 RDMA 功能，需要对存储网卡的物理网口开启 SR-IOV，ESXi 主机使用网口的物理功能 PF，同时提供虚拟功能 VF 给 SCVM 使用。
>
> 在 SCVM 中，SR-IOV 的 VF 网络将作为 SCVM 存储网络，负责节点间的数据传输，该网络将对应 RDMA 网络虚拟交换机中名为 RDMA 的虚拟机端口组；原有的 ZBS 网络将作为 VMware 接入网络，负责 SCVM 和本地 ESXi 的通信。

关于 SMTX OS 网络的更多介绍可参考文档[《 SMTX OS 网络技术白皮书》](/smtxos/6.3.0/network_whitepaper/network_whitepaper_preface_generic)。

---

## 构建 SMTX OS 集群的要求 > 网络要求 > 网络部署模式

# 网络部署模式

在规划 SMTX OS 网络时，您可以根据部署环境和实际业务需求，选择为集群的管理网络和存储网络分别设计一个独享的虚拟交换机，并为每个虚拟交换机分配物理网络适配器，即采用网络分离部署模式；也可以设计管理网络与存储网络共享同一个虚拟交换机和相应物理网络适配器的带宽，即采用网络融合部署模式。

下面以管理网络和存储网络为例，介绍使用网络分离部署和网络融合部署的拓扑结构。

- **网络分离部署**

  ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_231.png)
- **网络融合部署**

  ![](https://cdn.smartx.com/internal-docs/assets/b3c87667/vmware_installation_guide_008.png)

> **说明**：
>
> - 若存储网络开启了 RDMA 功能，则存储网络不可与管理网络共用一个虚拟交换机。
> - 无论采用网络分离部署还是网络融合部署模式，虚拟机网络均可选择与管理网络共享一个虚拟交换机或者独享一个虚拟交换机。

---

## 构建 SMTX OS 集群的要求 > 网络要求 > 网络配置要求

# 网络配置要求

参照[《 SMTX OS 网络技术白皮书》](/smtxos/6.3.0/network_whitepaper/network_whitepaper_preface_generic)中 VMware ESXi 平台的网络描述，集群的网络配置须满足以下要求。

- 网络带宽

  - 集群的存储网络带宽必须不低于 10 Gbps。若需要提升带宽性能，可以配置 25 Gbps 及以上带宽，但对于不启用 RDMA 功能的集群，还需要在集群部署成功后修改整体网络链路的 MTU 值。
  - 集群的管理网络带宽必须不低于 1 Gbps。若管理网络和存储网络采用融合部署模式，即两个网络共用相同的网口，则可复用存储网络带宽。
  - 集群的虚拟机网络带宽必须不低于 1 Gbps，若虚拟机网络和管理网络共用相同的网口，则可复用管理网络带宽。
- 网络连接

  集群中的所有 ESXi 主机必须连接到 L2 层网络。
- 网络延时

  对于 1400 字节及以上的数据包，集群的存储网络 ping 延时在 1 ms 以下。

---

## 构建 SMTX OS 集群的要求 > 网络要求 > IP 规划要求

# IP 规划要求

在 SMTX OS 集群的部署阶段和关联 CloudTower 阶段，需要填写 IP 地址、子网掩码、网关、管理虚拟 IP 等，请在安装部署前参考如下要求提前进行规划

---

## 构建 SMTX OS 集群的要求 > 网络要求 > IP 规划要求 > 集群节点 IP

# 集群节点 IP

从 SMTX OS 网络拓扑图可以确认，无论 SMTX OS 集群采用网络融合部署模式还是网络分离部署模式，在部署集群之前，都需要为集群的每个节点至少规划 4 个 IP：SCVM 管理 IP 、SCVM 存储 IP 、ESXi 管理 IP 和 ESXi 存储 IP，分别用于管理网络和存储网络。而 NFS Server IP 和 NFS VMkernel IP 由于使用的是固定的 IP 地址，无须单独规划。

规划管理网络和存储网络时，还需提供子网掩码、网关等信息，如下表所示。

| 网络类型 | IP 类型 | IP 地址 | 子网掩码 | 网关 | VLAN ID （可选） |
| --- | --- | --- | --- | --- | --- |
| 管理网络 | SCVM 管理 IP | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| ESXi 管理 IP | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| 存储网络 | SCVM 存储 IP | xx.xx.xx.xx | xx.xx.xx.xx | - | xx |
| ESXi 存储 IP | xx.xx.xx.xx | xx.xx.xx.xx | - | xx |
| 内部网络 | NFS Server IP | 192.168.33.2 | 255.255.255.0 | - | - |
| NFS VMkernel IP | 192.168.33.1 | 255.255.255.0 | - | - |

如果您还将启用集群的 RDMA 功能，则还需进行以下规划：

- 为每个节点同步规划 VMware 接入 IP。此 IP 设置在 SCVM 的 VMware 接入网络网卡上，用于节点 SCVM 与 ESXi 主机通信。
- 当物理交换机为存储网络配置了 VLAN 时，物理交换机需要配置为 Access 模式，且上表中存储网络的 VLAN ID 必须规划为 0。

如果需要 SMTX OS 集成硬件管理能力，还需为每个节点预留 IPMI 管理台 IP。

网络管理员在分配各节点的 IP 地址时，必须遵循以下规则：

- IP 地址不能与以下 CIDR 范围内的任何 IP 地址重叠：
  - 169.254.0.0/16
  - 240.0.0.0/4
  - 224.0.0.0/4
  - 198.18.0.0/15
  - 127.0.0.0/8
  - 0.0.0.0/8
- 管理 IP 和存储 IP：
  - SCVM 管理 IP 和存储 IP 不能分配在同一网段。
  - 集群各节点的 SCVM 存储 IP 之间， 以及 SCVM 存储 IP 和 ESXi 存储 IP 之间可以正常通信。
  - 集群各节点的 SCVM 管理 IP 需要分配在同一网段。
  - 集群各节点的 SCVM 管理 IP 和 ESXi 管理 IP 之间可以正常通信。
- VMware 接入 IP：
  - VMware 接入 IP 和 SCVM 存储 IP 必须分配在同一网段，且可以正常通信。
  - 集群各节点的 VMware 接入 IP 之间可以正常通信。

规划完以上 IP 后，需要将集群每个节点的 IP 与服务器序列号（即服务标签）一一对应。

---

## 构建 SMTX OS 集群的要求 > 网络要求 > IP 规划要求 > 集群管理虚拟 IP

# 集群管理虚拟 IP

设置集群的管理虚拟 IP 是为了保证集群管理界面的高可用。访问此 IP 时，可以自动通过集群内任一可用的 SCVM 管理 IP 访问集群。

部署集群成功后，在设置参数阶段，系统会自动跳转至关联 CloudTower 的界面，要求将 SMTX OS 集群与 CloudTower 进行关联，此时必须输入集群的管理虚拟 IP。

因此，请参考如下要求与建议，提前规划集群的管理虚拟 IP：

- 确保 CloudTower 可以通过管理虚拟 IP 访问集群。
- 管理虚拟 IP 与节点的 SCVM 管理 IP 分配在同一个子网。
- 管理虚拟 IP 不能与以下 CIDR 范围内的任何 IP 地址重叠：
  - 169.254.0.0/16
  - 240.0.0.0/4
  - 224.0.0.0/4
  - 198.18.0.0/15
  - 127.0.0.0/8
  - 0.0.0.0/8

---

## 构建 SMTX OS 集群的要求 > 网络要求 > 防火墙端口规划要求

# 防火墙端口规划要求

为确保 SMTX OS 功能能够正常工作，ESXi 和 vCenter 防火墙需开放相应的端口；此外，为确保集群能够正常对外提供服务，如果 SMTX OS 集群的网络之间或集群与外部客户端之间存在防火墙，对应防火墙也需开放一些端口。请参考[《SMTX OS 防火墙端口说明》](/smtxos/6.3.0/firewall_guide/firewall_guide_preface_generic)提前规划需要开放的端口。

---

## 构建 SMTX OS 集群的要求 > 硬件要求

# 硬件要求

您需要确保集群内的各个服务器满足**硬件兼容性要求**，以及 **ESXi 主机配置要求**。在此之前，您可以先阅读**系统资源占用**，了解 SMTX OS 集群需占用的计算和存储资源。

---

## 构建 SMTX OS 集群的要求 > 硬件要求 > 系统资源占用 > 系统对物理盘存储空间的占用

# 系统对物理盘存储空间的占用

对于同一种容量规格，系统对每个节点中特定用途的物理盘占用的存储空间是固定的，如下表。

| 容量规格 | 物理盘用途 | 系统占用的存储空间 | 说明 |
| --- | --- | --- | --- |
| 标准容量规格 | 含元数据分区的缓存盘或含元数据分区的数据盘 | 305 GiB | 系统分区、元数据分区、Journal 分区和预留空间固定共占用 305 GiB 空间。 |
| 缓存盘或数据盘 | 20 GiB | Journal 分区固定占用 20 GiB 空间。 |
| 大容量规格 | 含元数据分区的缓存盘或含元数据分区的数据盘 | 660 GiB | 系统分区、元数据分区、Journal 分区和预留空间固定共占用 660 GiB 空间。 |
| 缓存盘或数据盘 | 20 GiB | Journal 分区固定占用 20 GiB 空间。 |

您可以参考下表了解集群采用不同的存储配置时每个节点的存储空间分配情况和逻辑可用容量。

| 存储配置 | 物理盘用途 | 存储空间分配说明 | 逻辑可用容量说明 |
| --- | --- | --- | --- |
| 混闪配置或多种类型 SSD 全闪配置 | 含元数据分区的缓存盘 | 系统占用一定的存储空间（如上表），剩余空间为缓存分区。 | 逻辑可用容量 = 数据分区用于存储数据的容量 × 空间利用率  **说明：**   - 若集群使用纠删码的冗余策略，则空间利用率 = K / (K + M)。 - 若集群使用副本的冗余策略，则空间利用率 = 1 / 副本数。 |
| 缓存盘 |
| 数据盘 | 数据分区。  **说明：** 若集群采用混闪配置，则数据盘（HDD）数据分区的 1 / 17 将用于存放校验信息，剩余空间用于存放数据。 |
| 单一类型 SSD 全闪配置 | 含元数据分区的数据盘 | 系统占用一定的存储空间（如上表），若集群采用存储分层模式，则剩余空间由缓存与数据共享，缓存分区和数据分区的比例为 1：9；若集群采用存储不分层模式，则剩余空间为数据分区。 |
| 数据盘 |

下面以集群采用如下配置为例展示逻辑可用容量的计算过程：

- 存储配置：单一类型 SSD 全闪配置
- 存储分层/不分层模式：分层模式
- 冗余策略：纠删码（2 + 1 配比）
- 节点容量规格：标准容量规格
- 每节点的含元数据分区的数据盘：2 块 960 GB（约为 894 GiB）的数据中心级 SSD
- 每节点的数据盘：1 块 960 GB（约为 894 GiB）的数据中心级 SSD

每个节点的逻辑可用容量 = [(894 - 305) × 2 + (894 - 20)] × 9 / (1 + 9) × 2 / (2 + 1) = 1231.2 GiB。

---

## 构建 SMTX OS 集群的要求 > 硬件要求 > 系统资源占用 > 系统对 SCVM 的 CPU 和内存的占用

# 系统对 SCVM 的 CPU 和内存的占用

- CPU 占用：7 核

  > **说明**：
  >
  > SMTX OS 支持静态数据加密功能，部署集群时可选择是否为该功能启用加密加速，若启用，将额外增加 2 个 CPU 核心的占用。
- 内存占用：30 GB + ⌈ 节点数据盘总容量（TB）/ 10 TB × 1.5 GB ⌉

  > **说明**：
  >
  > - ⌈⌉ 为上取整符号，其运算结果为不小于原数的最小整数，例如 ⌈3.2⌉ = 4。
  > - 当节点缓存盘容量超过挂载的数据盘容量的 20% 时，每超过 8 TiB 将增加 2 GB 的内存占用。
  > - 内存占用为 SMTX OS 对 SCVM 的需求，实际部署时需在此基础上额外预留 2 GB 内存供 SCVM 自身使用。

---

## 构建 SMTX OS 集群的要求 > 硬件要求 > 硬件兼容性要求

# 硬件兼容性要求

确认现场服务器的型号、CPU（仅支持 `Intel x86_64`、`AMD x86_64`）、硬盘、网卡和存储控制器与 SMTX OS 兼容，可通过[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)进行查询。

---

## 构建 SMTX OS 集群的要求 > 硬件要求 > ESXi 主机配置要求

# ESXi 主机配置要求

建议先明确集群节点使用的容量规格，以及集群采用存储分层还是不分层模式，再确认集群内每个 ESXi 主机的配置满足以下要求。

> **注意**：
>
> - 同一集群内所有主机的 CPU 供应商和容量规格必须相同。
> - 如需使用纠删码的冗余策略，必须选择存储分层模式。

---

## 构建 SMTX OS 集群的要求 > 硬件要求 > ESXi 主机配置要求 > 计算资源配置要求

# 计算资源配置要求

| 项目 | 最低配置要求与建议 |
| --- | --- |
| 处理器 | 单颗 CPU 的最小逻辑核心数为 12，节点逻辑核心数不少于 24，主频不低于 2.0 GHz，推荐 2 路服务器。 |
| CPU 微架构 | - Intel x86\_64：最低版本为 Sandy Bridge - AMD x86\_64：最低版本为 Zen |
| 内存 | - 标准容量规格：建议至少 128 GB - 大容量规格：建议至少 256 GB |

---

## 构建 SMTX OS 集群的要求 > 硬件要求 > ESXi 主机配置要求 > 存储设备配置要求

# 存储设备配置要求

请按以下要求规划集群的存储设备。确认完主机上每块物理盘的用途后，请记录对应的物理盘类型、型号和容量大小。

## 标准容量规格

### 存储分层模式

| 项目 | 混闪配置或多种类型 SSD 全闪配置 | 单一类型且多种属性 SSD 全闪配置 | 单一类型且单一属性 SSD 全闪配置 |
| --- | --- | --- | --- |
| 含元数据分区的缓存盘 | 2 块 960 GB 及以上（DWPD ≥ 3）的数据中心级 SSD。 全闪配置下，建议使用高性能 SSD 作为含元数据分区的缓存盘。如：节点包含 NVMe 和 SATA 两种类型 SSD 时，使用 NVMe SSD 作为含元数据分区的缓存盘。 | 2 块 960 GB 及以上（DWPD ≥ 3）的数据中心级 SSD。 建议使用高性能 SSD 作为含元数据分区的缓存盘。如：节点包含高 DWPD 和低 DWPD 两种属性 SSD 时，使用高 DWPD 的 SSD 作为含元数据分区的缓存盘。 | - |
| 含元数据分区的数据盘 | - | - | 2 块 960 GB 及以上（DWPD ≥ 1）的数据中心级 SSD。 |
| 缓存盘 | 使用含元数据分区的缓存盘的剩余空间，或单独配置数据中心级 SSD。 | 使用含元数据分区的缓存盘的剩余空间，或单独配置数据中心级 SSD。 | - |
| 数据盘 | - 全闪配置：建议配置 960 GB 及以上（DWPD ≥ 1）的数据中心级 SSD。 - 混闪配置：建议配置 1 TB 及以上的 HDD。 | 建议配置 960 GB 及以上（DWPD ≥ 1）的数据中心级 SSD。 | 至少 1 块 960 GB 及以上（DWPD ≥ 1）的数据中心级 SSD。 |
| 存储控制器 | 1 张支持 JBOD 模式的 RAID 卡或 HBA 卡。  **注意：**该存储控制器用于管理除启动盘外的所有物理盘。若 U.2 NVMe 硬盘通过 retimer 或 Switch 或者直接使用 AIC NVMe 转接至 PCIe 接口，也可以不使用存储控制器。 | | |
| 启动盘 | 使用 ESXi 系统盘的 7 GB 容量。对 ESXi 系统盘的要求请在 [Broadcom 文档官网](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html)中参考要安装的 ESXi 软件版本对应的安装和设置文档。 | | |

> **说明**：
>
> - 混闪配置、多种类型 SSD 全闪配置或单一类型且多种属性 SSD 全闪配置时，单节点限制如下：
>   - 数据盘总容量不超过 128 TB。
>   - 缓存盘、含元数据分区的缓存盘和数据盘总数量不可超过 64。
>   - 缓存盘和含元数据分区的缓存盘总容量不超过 51 TB。
>   - 缓存盘和含元数据分区的缓存盘的总容量与数据盘总容量之比应高于 10%。  
>     若计划在集群中启用常驻缓存模式，需注意：
>     - 在扣除常驻缓存容量后，缓存盘和含元数据分区的缓存盘的剩余容量与数据盘总容量之比仍需高于 10%。
>     - 采用多种类型 SSD 全闪配置或单一类型且多种属性 SSD 全闪配置时，若计划预留常驻缓存比例高于 75%，需要在部署集群的[第 4 步：配置存储](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_63)阶段，将所有数据盘的用途修改为缓存盘。
> - 单一类型且单一属性 SSD 全闪配置时，单节点限制如下：
>   - 数据盘和含元数据分区的数据盘的总容量不超过 128 TB。
>   - 数据盘和含元数据分区的数据盘的总数量不超过 32。

### 存储不分层模式

| 存储配置 | 项目 | 配置要求与建议 |
| --- | --- | --- |
| 单一类型 SSD 全闪配置 | 存储控制器 | 1 张支持 JBOD 模式的 RAID 卡或 HBA 卡。  **注意：**该存储控制器用于管理除启动盘外的所有物理盘。若 U.2 NVMe 硬盘通过 retimer 或 Switch 或者直接使用 AIC NVMe 转接至 PCIe 接口，也可以不使用存储控制器。 |
| 启动盘 | 使用 ESXi 系统盘的 7 GB 容量。对 ESXi 系统盘的要求请在 [Broadcom 文档官网](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html)中参考要安装的 ESXi 软件版本对应的安装和设置文档。 |
| 含元数据分区的数据盘 | 2 块 960 GB 及以上（DWPD ≥ 1）的数据中心级 SSD。 |
| 数据盘 | 使用含元数据分区的数据盘的剩余空间，或单独配置数据中心级 SSD，建议使用同一品牌型号且容量规格相同的 SSD。 |

> **说明**：
>
> 单节点限制如下：
>
> - 数据盘和含元数据分区的数据盘总容量不超过 128 TB。
> - 数据盘和含元数据分区的数据盘总数量不可超过 32。

## 大容量规格

### 存储分层模式

| 项目 | 混闪配置或多种类型 SSD 全闪配置 | 单一类型且多种属性 SSD 全闪配置 | 单一类型且单一属性 SSD 全闪配置 |
| --- | --- | --- | --- |
| 含元数据分区的缓存盘 | 2 块 960 GB 及以上（DWPD ≥ 3）的数据中心级 SSD。 全闪配置下，建议使用高性能 SSD 作为含元数据分区的缓存盘。如：节点包含 NVMe 和 SATA 两种类型 SSD 时，使用 NVMe SSD 作为含元数据分区的缓存盘。 | 2 块 960 GB 及以上（DWPD ≥ 3）的数据中心级 SSD。 建议使用高性能 SSD 作为含元数据分区的缓存盘。如：节点包含高 DWPD 和低 DWPD 两种属性 SSD 时，使用高 DWPD 的 SSD 作为含元数据分区的缓存盘。 | - |
| 含元数据分区的数据盘 | - | - | 2 块 960 GB 及以上（DWPD ≥ 1）的数据中心级 SSD。 |
| 缓存盘 | 使用含元数据分区的缓存盘的剩余空间，或单独配置数据中心级 SSD。 | 使用含元数据分区的缓存盘的剩余空间，或单独配置数据中心级 SSD。 | - |
| 数据盘 | - 全闪配置：建议配置 960 GB 及以上的数据中心级 SSD。 - 混闪配置：建议配置 1 TB 及以上的 HDD。 | 建议配置 960 GB 及以上的数据中心级 SSD。 | 至少 1 块 960 GB 及以上（DWPD ≥ 1）的数据中心级 SSD。 |
| 存储控制器 | 1 张支持 JBOD 模式的 RAID 卡或 HBA 卡。  **注意：**该存储控制器用于管理除启动盘外的所有物理盘。若 U.2 NVMe 硬盘通过 retimer 或 Switch 或者直接使用 AIC NVMe 转接至 PCIe 接口，也可以不使用存储控制器。 | | |
| 启动盘 | 使用 ESXi 系统盘的 7 GB 容量。对 ESXi 系统盘的要求请在 [Broadcom 文档官网](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html)中参考要安装的 ESXi 软件版本对应的安装和设置文档。 | | |

> **说明**：
>
> - 混闪配置、多种类型 SSD 全闪配置或单一类型且多种属性 SSD 全闪配置时，单节点限制如下：
>   - 数据盘总容量不超过 256 TB。
>   - 缓存盘和含元数据分区的缓存盘总容量不超过 51 TB。
>   - 缓存盘、含元数据分区的缓存盘和数据盘总数量不可超过 64。
>   - 缓存盘和含元数据分区的缓存盘的总容量与数据盘总容量之比应高于 10%。
>     若计划在集群中启用常驻缓存模式，需注意：
>     - 在扣除常驻缓存容量后，缓存盘和含元数据分区的缓存盘的剩余容量与数据盘总容量之比仍需高于 10%。
>     - 采用多种类型 SSD 全闪配置或单一类型且多种属性 SSD 全闪配置时，若计划预留常驻缓存比例高于 75%，需要在部署集群的[第 4 步：配置存储](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_63)阶段，将所有数据盘的用途修改为缓存盘。
> - 单一类型且单一属性 SSD 全闪配置时，单节点限制如下：
>   - 数据盘和含元数据分区的数据盘的总容量不超过 256 TB。
>   - 数据盘和含元数据分区的数据盘的总数量不超过 32。

### 存储不分层模式

| 存储配置 | 项目 | 配置要求与建议 |
| --- | --- | --- |
| 单一类型 SSD 全闪配置 | 存储控制器 | 1 张支持 JBOD 模式的 RAID 卡或 HBA 卡。  **注意：**该存储控制器用于管理除启动盘外的所有物理盘。若 U.2 NVMe 硬盘通过 retimer 或 Switch 或者直接使用 AIC NVMe 转接至 PCIe 接口，也可以不使用存储控制器。 |
| 启动盘 | 使用 ESXi 系统盘的 7 GB 容量。对 ESXi 系统盘的要求请在 [Broadcom 文档官网](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html)中参考要安装的 ESXi 软件版本对应的安装和设置文档。 |
| 含元数据分区的数据盘 | 2 块 960 GB 及以上（DWPD ≥ 1）的数据中心级 SSD。 |
| 数据盘 | 使用含元数据分区的数据盘的剩余空间，或单独配置数据中心级 SSD，建议使用同一品牌型号且容量规格相同的 SSD。 |

> **说明**：
>
> 单节点限制如下：
>
> - 数据盘和含元数据分区的数据盘总容量不超过 256 TB。
> - 数据盘和含元数据分区的数据盘总数量不可超过 32。

---

## 构建 SMTX OS 集群的要求 > 硬件要求 > ESXi 主机配置要求 > 网络设备配置要求

# 网络设备配置要求

| 项目 | 配置要求与建议 |
| --- | --- |
| 网卡 | - 存储网络：1 张速率至少为 10 Gbps 的双口网卡。 - 管理网络：1 张速率至少为 1 Gbps 的双口网卡。若管理网络和存储网络采用融合部署模式，可复用存储网络的网卡。 - 虚拟机网络：1 张速率至少为 1 Gbps 的双口网卡，可复用管理网络的网卡或者使用独立的网卡。 |
| 网口 | 千兆网口和万兆网口数量均不超过 16。 |

---

## 构建 SMTX OS 集群的要求 > 软件要求

# 软件要求

在正式部署前，提前下载如下安装文件。

- SMTX OS 安装文件（Intel x86\_64 或 AMD x86\_64 架构，ISO 映像文件）

  您可以根据实际需求选择 CentOS 或 openEuler 操作系统的安装文件。同一集群内所有节点必须使用相同的安装文件进行安装。
- CloudTower 安装文件（可选）

  如果安装部署环境中没有 CloudTower，您可以根据实际需求下载 CentOS 或 openEuler 操作系统的安装文件（Intel x86\_64 或 AMD x86\_64 架构，ISO 映像文件），否则无需下载。
- VMware ESXi 安装文件

  VMware ESXi 软件现为 Broadcom 公司的产品，请向相关供应商获取指定版本的安装映像文件，或者登录 Broadcom 官网下载安装程序。
- VMware vCenter Server 安装文件（可选）

  VMware vCenter Server 软件现为 Broadcom 公司的产品，如果安装部署环境中没有 vCenter Server，则需要在安装部署期间在任一 ESXi 节点上安装该软件。请向相关供应商获取指定版本的安装映像文件，或者登录 Broadcom 官网下载安装程序。
- VAAI-NAS 插件（可选）

  请根据[《SMTX OS 发布说明》](/smtxos/6.3.0/release_notes/release-notes)的“虚拟化平台与应用场景配套说明”所备注的信息判断是否需要下载插件，以及具体应该下载的插件版本。
- 高级监控安装文件（可选）

  当集群准备在部署结束后开启高级监控功能，请提前下载该功能对应的安装文件（Intel x86\_64 或 AMD x86\_64 架构），否则请忽略此项要求。

---

## 构建 SMTX OS 集群的要求 > 浏览器版本要求

# 浏览器版本要求

安装部署 SMTX OS 过程中需要使用 Web 浏览器，为保证兼容性，我们建议您使用以下版本的浏览器，同时开启 Cookie 和 JavaScript。

- Google Chrome：91 及以上版本
- Microsoft Edge：107 及以上版本
- Mozilla Firefox：107.0 及以上版本
- Apple Safari：14.1 及以上版本

---

## 构建 SMTX OS 集群的要求 > 启用高级功能的要求

# 启用高级功能的要求

SMTX OS 支持在 VMware ESXi 平台启用 RDMA 功能和常驻缓存模式，以提升集群的性能，同时还支持机架拓扑感知功能。启用 RDMA 功能和常驻缓存模式对集群的软硬件配置等有一些特殊的要求；启用机架拓扑功能还需要规划集群节点在机架的分布，并在 CloudTower 中正确配置物理拓扑。建议您提前了解这些要求。

---

## 构建 SMTX OS 集群的要求 > 启用高级功能的要求 > 启用 RDMA 功能

# 启用 RDMA 功能

启用集群的 RDMA 功能需参考《 SMTX OS 特性说明》中 RDMA 功能的[配置要求](/smtxos/6.3.0/os_property_notes/os_property_notes_19)进行准备。另外，建议先登录 [Mellanox 官方网站](https://network.nvidia.com/products/adapter-software/firmware-tools/)，下载与待安装的 ESXi 软件版本适配的 MFT 软件包，其中包含 mft 和 nmst 的 vib 软件包。

---

## 构建 SMTX OS 集群的要求 > 启用高级功能的要求 > 启用常驻缓存模式

# 启用常驻缓存模式

启用集群的常驻缓存模式需参考《SMTX OS 特性说明》中的[配置要求](/smtxos/6.3.0/os_property_notes/os_property_notes_72)进行准备。

---

## 构建 SMTX OS 集群的要求 > 启用高级功能的要求 > 启用机架拓扑感知

# 启用机架拓扑感知

为了确保在机架断电或损坏等极端状况下，系统还能在其他机架的主机上找到存活的副本或找到数据块和校验块重建数据，继续提供数据访问能力和增加数据可用性，SMTX OS 提供了机架感知功能。

启用机架拓扑感知功能并达到机箱或机架级别的容错能力需要在规划集群时满足以下要求：

- 如果期望使用多副本的冗余策略，则机箱或机架数须大于等于副本数，并将服务器平均分布在不同的机架中，从而尽量使数据的多个副本均匀地分配到不同的机架、机箱和主机上。
- 如果期望使用纠删码的冗余策略，则机箱或机架数须大于等于 K + M + 1，并将服务器平均分布在不同的机架中，从而尽量使数据块和校验块均匀地分配到不同的机架、机箱和主机上。

除上述要求外，还需在 CloudTower 管理平台正确配置集群的物理拓扑。即在集群部署结束后，使用 CloudTower 的机架配置功能，如实呈现安装部署现场的主机与机架的位置和拓扑结构，然后系统将根据拓扑来调整数据的分配情况。详细的配置建议和操作可参见《SMTX OS 管理指南》中**管理机架拓扑**章节的[配置机架拓扑](/smtxos/6.3.0/os_administration_guide/os_administration_guide_167)小节。

---

## 构建 SMTX OS 集群的要求 > 启用 NVMe 直通硬盘热插拔功能的要求

# 启用 NVMe 直通硬盘热插拔功能的要求

当 SMTX OS 集群的存储设备中包含 U.2 NVMe 硬盘时，如果需要为直通给 SCVM 的 U.2 NVMe 硬盘启用热插拔功能，即允许在后续运维集群阶段使用 SmartX 提供的 vmpctl 工具在 SCVM 开机状态下更换直通的 U.2 NVMe 硬盘，则需参考如下要求进行准备。

- 确认集群不需要启用 RDMA 功能，因为 NVMe 直通硬盘热插拔功能与 RDMA 功能无法同时启用。
- 确认待安装的 VMware ESXi 软件版本为 8.0 U1 及以上版本。
- 确认服务器支持 VMDirectPath I/O 功能，可在 [Broadcom 官网](https://compatibilityguide.broadcom.com)查看当前服务器型号是否支持该功能。
- 确认服务器平台和设备满足 VMDirectPath I/O 功能的要求，可在 [Broadcom 官网](https://knowledge.broadcom.com/external/article?legacyId=2142307)查看具体要求。
- 根据本地主机的 CPU 架构和操作系统下载 vmpctl 文件，然后参考以下说明为该文件重命名和赋予可执行权限。
  - 如果操作系统是 Linux 或 macOS，请重命名为 `vmpctl`，然后进入该文件所在目录，执行命令 `chmod a+x vmpctl` 赋予可执行权限。
  - 如果操作系统是 Windows，请重命名为 `vmpctl.exe`，然后关闭杀毒软件或者将该软件添加至杀毒软件白名单，避免文件被杀毒软件误删。

---

## 安装部署须知

# 安装部署须知

部署完 SMTX OS 集群后，请勿在 SCVM 虚拟机中安装第三方插件，以免影响集群中业务虚拟机的稳定运行。

如果需要为 SMTX OS 集群启用如下功能，在安装部署集群过程中和结束后，还需要为相应功能进行一些特殊设置，建议您在安装部署集群前，认真阅读本章内容，了解每个功能的注意事项。

- 启用 RDMA 功能
- 启用常驻缓存模式
- 配置 25 Gbps 及以上带宽的存储网络
- 启用 NVMe 直通硬盘热插拔功能

---

## 安装部署须知 > 启用 RDMA 功能

# 启用 RDMA 功能

如果要启用 RDMA 功能，请注意在安装部署期间完成如下配置：

- 在设置 ESXi 阶段，需要[为启用 RDMA 功能设置 ESXi 主机](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_31) ，包括安装 Mellanox 固件工具，设置固件和驱动程序启用 SR-IOV，然后在交换机端和 ESXi 主机端分别[为 RDMA 功能配置流量控制](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_35)。
- 在配置存储网络阶段，在[创建新的 vSphere 标准交换机](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_43)时，需要将 RDMA 网卡的指定网口分配给新创建的交换机，并单独[为 RDMA 网络创建标准交换机](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_46)。
- 在 ESXi 节点上创建 SCVM 虚拟机阶段，需要满足[启用 RDMA 特性的配置要求](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_52)。
- 在部署集群的[第 5 步：配置网络](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_64)阶段，需要启用 RDMA，并设置 VMware 接入网口和 VMware 接入 IP。
- [为 RDMA 功能验证流量控制的配置结果](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_38)。
- 在[部署 I/O 重路由脚本和 SCVM 自动重启脚本](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_85)阶段，需要为 RDMA 网卡配置静态路由，并验证其部署结果。

---

## 安装部署须知 > 启用常驻缓存模式

# 启用常驻缓存模式

如果要启用常驻缓存模式，请注意在安装部署期间以及结束后完成如下配置：

- 在部署 SMTX OS 集群的[第 4 步：配置存储](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_63)时，需要选择**分层**模式。
- 安装部署完成后，需要在集群的设置页面中开启“允许数据常驻缓存”，并为常驻缓存卷预留缓存容量，然后为 NFS 文件启用常驻缓存模式，详情请参考《SMTX OS 管理指南》。

---

## 安装部署须知 > 配置 25 Gbps 及以上带宽的存储网络

# 配置 25 Gbps 及以上带宽的存储网络

对于不启用 RDMA 功能的集群，如果需要将存储网络的带宽配置为 25 Gbps 及以上，请注意需要在集群部署成功后的设置参数阶段，分别在物理交换机端、ESXi 主机端和 SCVM 的端口[修改整体网络链路的 MTU 值](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_71)。

---

## 安装部署须知 > 启用 NVMe 直通硬盘热插拔功能

# 启用 NVMe 直通硬盘热插拔功能

如果需要启用 NVMe 直通硬盘热插拔功能，请注意在安装部署期间完成如下配置：

- 在安装 ESXi 前，需要将所有服务器的引导模式都设置为 “UEFI”。
- 在设置 ESXi 阶段，[修改 ESXi 主机参数](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_28)时，需要设置 ESXi VMkernel 参数。
- 在 ESXi 节点上创建 SCVM 虚拟机后且未安装 SMTX OS 时，需要[为 NVMe 直通硬盘热插拔功能设置 SCVM](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_99)。

---

## 在每个节点上安装 ESXi 软件

# 在每个节点上安装 ESXi 软件

通过浏览器访问每个节点的 IPMI 管理台 IP，检查 BIOS 设置，远程安装并配置 ESXi。

**前提条件**

- 已获得整个集群的规划和完整的 IP 地址分配表，并且为每个节点已配置 IPMI 管理台 IP。
- 已获取 VMware ESXi 安装文件。如果要启用集群的 RDMA 功能，则 ESXi 软件版本需满足《 SMTX OS 特性说明》的[启用 RDMA 功能](/smtxos/6.3.0/os_property_notes/os_property_notes_14)的配置要求。

**注意事项**

在安装 ESXi 软件前，建议将所有服务器的引导模式都设置为 “UEFI”。如果主机使用的 RAID 卡为 `MegaRAID 9560-8i`，或者需要启用 NVMe 直通硬盘热插拔功能，请注意设置为 “UEFI”。

下文将以每台节点使用戴尔服务器（C6420）为例，介绍 SMTX OS 集群的安装和部署流程。

---

## 在每个节点上安装 ESXi 软件 > 检查 BIOS 设置

# 检查 BIOS 设置

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录该节点的 IPMI 管理台。
2. 登录成功后，找到**虚拟控制台**，单击**启动虚拟控制台**，进入虚拟控制台界面。
3. 在界面顶端单击**功率**，在弹出的**电源控制**窗口中，单击**复位系统（热启动）**，重启服务器。
4. 在服务器启动过程中，当出现选项菜单时，按 **F2** 键，进入 **System Setup** 界面后，单击 **System BIOS**。
5. 在 **System BIOS Settings** 界面中，单击 **Processor Settings**。检查并确认 CPU 的 **Virtualization Technology** 选项为 **Enabled** ，确保启用 CPU 的虚拟化特性。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_010.png)
6. 单击 **Back**，返回 **System BIOS Settings** 界面后，单击 **System Profile Settings**，检查并确认 **System Profile** 选项为 **Performance**，以确保关闭电源的节能模式。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_011.png)
7. 单击 **Back**，返回 **System BIOS Settings** 界面后，单击 **Integrated Devices**，将 **SR-IOV Global Enable** 选项的值设置为 **Enabled**。
8. 单击 **Back**，在 **System BIOS Settings** 界面和 **System Setup** 界面单击 **Finish**。在弹出的 **Warning** 对话框中，单击 **Yes**。

---

## 在每个节点上安装 ESXi 软件 > 安装 VMware ESXi 软件

# 安装 VMware ESXi 软件

VMware ESXi 软件现为 Broadcom 公司的产品，请登录 [Broadcom 文档官网](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html)，参考要安装的软件版本对应的安装和设置文档，在每个服务器的节点安装 VMware ESXi 软件。

---

## 设置 ESXi

# 设置 ESXi

安装完 VMware ESXi 软件后，需要设置 ESXi 主机。

---

## 设置 ESXi > 为 ESXi 管理网络配置 IP

# 为 ESXi 管理网络配置 IP

根据 SMTX OS 网络拓扑图，ESXi 主机之间通过管理网络通信，因此需要为 ESXi 管理网络配置 IP、子网掩码和网关。

**操作步骤**

1. ESXi 系统启动完成后，按 **F2** 键，用 **root** 账户登录系统，进入 **System Customization** 菜单。
2. 选择 **Configure Management Network** > **Network Adapters**，在弹出的界面里选择管理网络绑定的网卡。
3. 选择 **Configure Management Network** > **IPv4 Configuration**，在弹出的界面里先选择 **Set static IPv4 address and network configuration**，再选择 **IPv4 Address**，然后手动输入 ESXi 的管理 IP。
4. 选择 **IPv4 Configuration** > **Subnet Mask**，输入子网掩码。然后在 **Default Gateway** 选项里输入网关。
5. （可选）选择 **Configure Management Network** > **DNS Configuration**，设置 DNS 的主机名和 IP 地址。
6. 保存设置。
7. 参考以上步骤，对其他节点设置 ESXi 的管理 IP、子网掩码和网关等信息。

---

## 设置 ESXi > 修改 ESXi 主机的参数

# 修改 ESXi 主机的参数

为确保 SCVM 能很好地运行在 VMware ESXi 主机上，需要修改 ESXi 主机的参数。

**操作步骤**

1. 返回 **System Customization** 菜单，选择 **Troubleshooting Options > Enable SSH**，然后按 **Enter** 键，启用 SSH 服务。
2. 通过 SSH 服务连接到 ESXi 主机，并以 **root** 账户登录 ESXi 主机，在 ESXi 主机上依次运行如下命令：

   ```
   esxcfg-advcfg -s 30 /NFS/HeartbeatTimeout
   esxcfg-advcfg -s 64 /NFS/MaxVolumes
   esxcfg-advcfg -s 1 /Misc/APDHandlingEnable
   esxcfg-advcfg -s 32 /Net/TcpipHeapSize
   esxcfg-advcfg -s 1536 /Net/TcpipHeapMax
   esxcfg-advcfg -s 1 /UserVars/SuppressShellWarning
   ```
3. （可选）如果需要启用 NVMe 直通硬盘热插拔功能，请在 ESXi 主机上运行如下命令设置 ESXi VMkernel 参数。

   ```
   esxcli system settings kernel set -s maxIntrCookies -v 4096
   ```
4. 重启 ESXi 主机。

   > **说明**：
   >
   > 由于后续配置 PCI 直通时也需要重启 ESXi 主机，因此您在此处也可选择不重启，在配置 PCI 直通时再重启。
5. 参照以上步骤，对其他节点的 ESXi 主机的参数进行修改。

---

## 设置 ESXi > 安装 SMTX VAAI-NAS 插件

# 安装 SMTX VAAI-NAS 插件

为支持虚拟机磁盘的厚置备模式和快速克隆文件等功能，您需要在 ESXi 主机上安装 SMTX VAAI-NAS 插件，但 SMTX VAAI-NAS 插件版本需与 VMware ESXi 的版本适配，请先根据[《SMTX OS 发布说明》](/smtxos/6.3.0/release_notes/release-notes)中**虚拟化平台与应用场景配套说明** > **虚拟化平台**部分的备注信息判断是否需要安装插件，以及具体应该安装的插件版本。

- 如果无需安装 SMTX VAAI-NAS 插件，请直接跳转到[配置 PCI 直通](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_30)。
- 如果需要安装 SMTX VAAI-NAS 插件，请参考[《SMTX VAAI-NAS 插件安装与升级指南》](/smtxos/6.3.0/vaainas/vaai_nas_installtion_upgrade/vaai_nas_installtion_upgrade_01)中对应插件版本的安装步骤完成插件的安装。

---

## 设置 ESXi > 配置 PCI 直通

# 配置 PCI 直通

为了使除 ESXi 系统盘外的物理盘能直通给 SCVM 使用，若 ESXi 主机使用存储控制器来管理这些物理盘，则您需要为该存储控制器配置 PCI 直通；否则您需要为对应物理盘配置 PCI 直通。

**操作步骤**

下文以存储控制器 HBA330 直通卡为例介绍配置 PCI 直通的操作步骤。

1. 使用浏览器登录到 ESXi 系统控制台。
2. 选择**管理** > **硬件** > **PCI 设备**，找到需要直通的存储控制器，可通过 PCI 设备名的关键字进行筛选。以下图 Dell 服务器为例，通过输入 `330` 可筛选出 HBA330 直通卡，下文将继续以此设备为例介绍操作步骤。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_031.png)
3. 查看 PCI 设备列表中**直通**字段的取值，若显示为`禁用`，请参考下面步骤配置直通模式，完成后进入步骤 5；否则，请跳转进入下一步。

   1. 选中该项，单击**切换直通**，启用 HBA330 直通卡。
   2. 通过 SSH Client 连接至 ESXi 主机，并通过 PCI 设备关键字进行过滤，查找对应属性信息。例如查询得出下方 HBA330 设备的对应属性值（供应商 ID、设备 ID）为 `1000 0097`。

      ```
      [root@localhost:~] lspci -v |grep 330 -A 1
      0000:3b:00.0 Mass storage controller Serial Attached SCSI controller:    Avago      (LSI Logic) Dell HBA330 Mini [vmhba4]
              Class 0107: 1000:0097
      ```
   3. 记录设备的属性值，更新配置文件 `/etc/vmware/passthru.map`，在文件尾部追加如下内容，保存并退出。其中 `1000 0097` 为上述步骤显示的属性值。

      ```
      1000  0097 d3d0 false
      ```
4. 如果**直通**字段显示为`不支持`，请参考下面步骤进行配置，然后进入步骤 5。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_225.png)

   1. 通过 SSH Client 连接至 ESXi 主机，并通过 PCI 设备关键字进行过滤，查找对应属性信息。例如查询得出下方 HBA330 设备的对应属性值（供应商 ID、设备 ID）为 `1000 0097`。

      ```
      [root@localhost:~] lspci -v |grep 330 -A 1
      0000:3b:00.0 Mass storage controller Serial Attached SCSI controller:    Avago      (LSI Logic) Dell HBA330 Mini [vmhba4]
              Class 0107: 1000:0097
      ```
   2. 记录设备的属性值，更新配置文件 `/etc/vmware/passthru.map`，在文件尾部追加如下内容，保存并退出。其中 `1000 0097` 为上述步骤显示的属性值。

      ```
      1000  0097 d3d0 false
      ```
   3. 单击**重新引导主机**，重启 ESXi 主机。
   4. 使用浏览器重新登录到 ESXi 系统控制台。
   5. 选择**管理** > **硬件** > **PCI 设备**，在 PCI 设备列表中筛选出上述修改配置文件的 PCI 设备，发现此时**直通**字段显示为`禁用`。
   6. 选中该项，单击**切换直通**，启用 HBA330 直通卡。
5. 对于 ESXi 主机中其他需要直通的 PCI 设备，请参照步骤 1 ~ 4 完成直通模式的配置。
6. 单击**重新引导主机**，重启 ESXi 主机。
7. 参照以上步骤，对其他节点的 ESXi 主机配置存储控制器直通模式。

**后续操作**

- 如果集群启用 RDMA 功能，还需要进行以下设置：
  - **为启用 RDMA 功能设置 ESXi 主机**
  - **为 RDMA 功能配置流量控制**
- 如果集群不启用 RDMA 功能，请直接跳转到**使用 vCenter Server 纳管 ESXi 主机**一章。

---

## 设置 ESXi > 为启用 RDMA 功能设置 ESXi 主机

# 为启用 RDMA 功能设置 ESXi 主机

SMTX OS 以 SR-IOV 的方式支持 RDMA 功能。若集群即将开启 RDMA 功能，则还需要对 ESXi 主机进行以下配置；否则请忽略下述配置步骤。

- 在 ESXi 主机中安装 MFT vib 工具，用于管理和配置网卡固件。
- 在网卡固件中开启 SR-IOV，设置最大的虚拟功能（VF）数量。
- 在 ESXi 网卡驱动中开启 SR-IOV，设置 VF 数量，并重启 ESXi 主机。

**注意事项**

在配置之前，请指定一张 Mellanox 网卡作为 RDMA 网卡，可以使用 `esxcfg-nics -l` 命令查看所有网卡的接口信息，如下，以判断出要作为 RDMA 网卡的 Mellanox 网卡的接口，并记录下该网卡上需要使用的网口的名称（如 `vminc1`）和 PCI ID（如 `0000:18:00.0`）。

当需要使用多个网口时，请确保记录下来的网口属于同一张 RDMA 网卡。同一张网卡上不同网口的 PCI ID 只有最后一位数不同，其余部分都相同。

```
# esxcfg-nics -l
Name    PCI          Driver      Link Speed      Duplex MAC Address       MTU    Description
vmnic1  0000:18:00.0 nmlx5_core  Up   25000Mbps  Full   0c:42:a1:24:ad:1e 1500   Mellanox Technologies ConnectX-4 Lx EN NIC; OCP; 25GbE; dual-port SFP28; (MCX4421A-ACQ)
vmnic2  0000:18:00.1 nmlx5_core  Up   25000Mbps  Full   0c:42:a1:24:ad:1f 1500   Mellanox Technologies ConnectX-4 Lx EN NIC; OCP; 25GbE; dual-port SFP28; (MCX4421A-ACQ)
vmnic3  0000:5e:00.0 igbn        Up   1000Mbps   Full   b4:96:91:93:a6:d8 1500   Intel Corporation I350 Gigabit Network Connection
vmnic4  0000:5e:00.1 igbn        Down 0Mbps      Half   b4:96:91:93:a6:d9 1500   Intel Corporation I350 Gigabit Network Connection
```

---

## 设置 ESXi > 为启用 RDMA 功能设置 ESXi 主机 > 安装 Mellanox 固件工具

# 安装 Mellanox 固件工具

1. 通过 SSH 服务连接到 ESXi 主机，并以 root 账号登录 ESXi 主机。
2. 将 MFT 软件包上传至 `ESXi /tmp` 路径下，并通过以下命令确认 mft 和 nmst 的 vib 软件包已经上传完毕。

   ```
   cd /tmp
   ls
   mft-4.22.1.11-10EM-730.0.0.18434556.x86_64.vib
   nmst-4.22.1.11-1OEM.703.0.0.18434556.x86_64.vib
   ```
3. 执行以下命令，获取网络适配器列表，确认列表中有 Mellanox 网卡。

   ```
   esxcli network nic list
   Name   PCI Device   Driver     Admin Status Link Status Speed  Duplex MAC Address       MTU  Description
   ------ ------------ ---------- ------------ ----------- ------ ------ ----------------- ---- ----------------------------------------------------
   vmnic0 0000:81:00.0 igbn       Up           Up          1000   Full   0c:c4:7a:e3:5c:20 1500 Intel Corporation I350 Gigabit Network Connection
   vmnic1 0000:81:00.1 igbn       Up           Down        0      Half   0c:c4:7a:e3:5c:21 1500 Intel Corporation I350 Gigabit Network Connection
   vmnic2 0000:02:00.0 nmlx5_core Up           Up          100000 Full   ec:0d:9a:8a:27:8a 1500 Mellanox Technologies MT28800 Family [ConnectX-5 Ex]
   vmnic3 0000:02:00.1 nmlx5_core Up           Down        0      Half   ec:0d:9a:8a:27:8b 1500 Mellanox Technologies MT28800 Family [ConnectX-5 Ex]
   ```
4. 执行如下命令，安装 nmst 和 mft。

   ```
   esxcli software vib install -v /tmp/nmst-4.22.1.11-1OEM.703.0.0.18434556.x86_64.vib -f
   Installation Result
   Message: The update completed successfully, but the system needs to be rebooted for the changes to be effective.
   Reboot Required: true
   VIBs Installed: MEL_bootbank_nmst_4.22.1.11-1OEM.703.0.0.18434556
   VIBs Removed:
   VIBs Skipped:

   esxcli software vib install -v /tmp/mft-4.22.1.11-10EM-730.0.0.18434556.x86_64.vib -f
   Installation Result
   Message: The update completed successfully, but the system needs to be rebooted for the changes to be effective.
   Reboot Required: true
   VIBs Installed: MEL_bootbank_mft_4.22.1.11-0
   VIBs Removed:
   VIBs Skipped:
   ```
5. 设置 ESXi 主机进入维护模式。
6. 重启 ESXi 主机。
7. 设置 ESXi 主机退出维护模式。
8. 进入 `/opt/mellanox/bin/` 文件夹下，确认 MFT 工具已存在。
9. 执行如下命令，运行 mst。

   ```
   cd /opt/mellanox/bin
   ./mst start
   Module mst loaded successfully
   ```
10. 检查 Mellanox 设备当前所处的状态。

    ```
    /opt/mellanox/bin/mst status
    MST devices:
    ------------
    mt4121_pciconf0
    ```
11. 查看 Mellanox 设备的详细信息。

    ```
    /opt/mellanox/bin/mst status -vv
    PCI devices:
    ------------
    DEVICE_TYPE MST PCI RDMA NET NUMA
    ConnectX5(rev:0) mt4121_pciconf0 02:00.0 net-vmnic2
    ConnectX5(rev:0) mt4121_pciconf0.1 02:00.1 net-vmnic3
    ```

---

## 设置 ESXi > 为启用 RDMA 功能设置 ESXi 主机 > 固件降级

# 固件降级

如果 RDMA 网卡是 ConnectX-4 Lx 系列的 Mellanox 网卡，为避免在固件中开启 SR-IOV 后出现 RDMA 性能抖动的问题，需要确保 RDMA 网卡的固件版本不高于 `14.26.4012`，否则需要进行固件降级。可以先进行以下操作，确认当前的固件版本。

1. 通过 SSH 服务连接到 ESXi 主机，并以 root 账号登录 ESXi 主机。
2. 输入 `esxcli network nic get -n <vmnic>` 命令查看 RDMA 网卡上任意一个已记录的指定网口的固件版本，其中 `<vmnic>` 表示网口的名称。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_222.png)

   - 如果固件版本不高于 `14.26.4012`，请直接跳转到[设置固件开启 SR-IOV](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_33)。
   - 如果固件版本高于 `14.26.4012`，请进行固件降级。

     1. 输入 `/opt/mellanox/bin/flint -d <PCI ID> q`，查看网卡接口的 PSID，以判断该网卡是否为 Mellanox 原厂生产。其中，`<PCI ID>` 表示网口的 PCI ID。

        ```
        [root@87-21:~]#/opt/mellanox/bin/flint -d 0000:18:00.0 q
        Image type:            FS3
        FW Version:            14.22.1002
        FW Release Date:       23.2.2018
        Product Version:       rel-14_22_1002
        Rom Info:              type=UEFI version=14.15.19 cpu=AMD64,AARCH64
                               type=PXE version=3.5.403 cpu=AMD64
        Description:           UID                GuidsNumber
        Base GUID:             0c42a103008c51a8        4
        Base MAC:              0c42a18c51a8            4
        Image VSD:             N/A
        Device VSD:            N/A
        PSID:                  MT_2420110034
        Orig PSID:             HUA0000000001
        Security Attributes:   N/A
        ```

        如果 PSID 以 `MT` 开头，如 `MT_2420110034`，则说明该网卡为 Mellanox 原厂生产的网卡，否则说明该网卡由 OEM 厂商生产。
     2. 执行固件降级。

        - 对于 Mellanox 原厂生产的网卡，根据网卡型号（如下图 *MCX4421A-ACQ*），单击[此链接](https://www.mellanox.com/support/firmware/firmware-downloads)下载对应的固件，并参考[官网文档](https://www.mellanox.com/support/firmware/nic) 进行固件降级。

          ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_223.png)
        - 对于 Mellanox 网卡由 OEM 厂商生产的情况，请向 OEM 厂商咨询对应的固件降级方法。

---

## 设置 ESXi > 为启用 RDMA 功能设置 ESXi 主机 > 设置固件开启 SR-IOV

# 设置固件开启 SR-IOV

1. 通过 SSH 服务连接到 ESXi 主机，并以 **root** 权限登录 ESXi 主机。
2. 运行 MFT 并检查其所处的状态。

   ```
   # /opt/mellanox/bin/mst start
   Module mst loaded successfully
    
   # /opt/mellanox/bin/mst status
    
    
   MST devices: 
   ------------
   mt4121_pciconf0
   ```
3. 查询设备目前所处的状态，检查 `SRIOV_EN` 字段和 `NUM_OF_VFS` 字段的取值。

   若 `SRIOV_EN` 为 **True**，并且 `NUM_OF_VFS` 为 **8**，则表示已开启 SR-IOV，请忽略后续步骤，直接进入[设置驱动程序开启 SR-IOV](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_34)；否则请继续执行下一步。

   ```
   # /opt/mellanox/bin/mlxconfig -d mt4121_pciconf0 q
    
   Device #1:
   ----------
   Device type: ConnectX5
   Name: N/A
   Description: N/A
   Device: mt4121_pciconf0
    
   Configurations: Current
    
   ...
   NUM_OF_VFS 0
   SRIOV_EN False(0)
   ...
   ```
4. 开启 SR-IOV 并设置期望的虚拟功能（VF）的数量。

   以如下参数为例进行配置。其中 `mt4121_pciconf0` 表示 MST 设备名称，您可以根据实际的设备名进行替换。

   - SRIOV\_EN=1
   - NUM\_OF\_VFS=8，将虚拟功能数量设置为 8

     ```
     # /opt/mellanox/bin/mlxconfig -d mt4121_pciconf0 set SRIOV_EN=1 NUM_OF_VFS=8
      
     Device #1: 
     ----------
      
     Device type: ConnectX5 
     Name: N/A 
     Description: N/A 
     Device: mt4121_pciconf0
      
     Configurations: Next Boot New 
     SRIOV_EN True(1) True(1) 
     NUM_OF_VFS 16 8
      
     Apply new Configuration? ? (y/n) [n] : y 
     Applying... Done! 
     -I- Please reboot machine to load new configurations.
     ```
   > **注意**：
   >
   > 必须为每个 PCI 设备执行 `mlxconfig` 命令。在驱动程序中，由于配置是按模块进行的，因此该配置将用于服务器上所安装的全部适配器。
5. 设置 ESXi 主机进入维护模式。
6. 重启 ESXi 主机。

   > **注意**：
   >
   > 重启后通过 `lspci` 命令将无法查看相应的虚拟功能，只有当 SR-IOV 在驱动程序中已经启动后，才可以看到期望的虚拟功能。

   ```
   # lspci -d | grep Mellanox
   0000:02:00.0 Network controller: Mellanox Technologies MT28800 Family [ConnectX-5 Ex] [vmnic2]
   0000:02:00.1 Network controller: Mellanox Technologies MT28800 Family [ConnectX-5 Ex] [vmnic3]
   ```
7. 将 ESXi 主机退出维护模式。
8. 检查固件中是否已启用 SR-IOV。其中 `mt4121_pciconf0` 表示 MST 设备名称，您可以根据实际的设备名进行替换。

   ```
   # /opt/mellanox/bin/mlxconfig -d mt4121_pciconf0 q
    
    
   Device #1:
   ----------
    
   Device type: ConnectX5
   Name: N/A
   Description: N/A
   Device: mt4121_pciconf0
    
   Configurations: Current
    
   ...
    
   NUM_OF_VFS 8
    
   SRIOV_EN True(1)
    
   ...
   ```

---

## 设置 ESXi > 为启用 RDMA 功能设置 ESXi 主机 > 设置驱动程序开启 SR-IOV

# 设置驱动程序开启 SR-IOV

1. 获取模块参数列表并查看每个参数的具体含义，便于后续进行配置。

   ```
   # esxcli system module parameters list -m nmlx5_core
    
   Name Type Value Description
   ...
   max_vfs array of uint Number of PCI VFs to initialize
   Values : Array of 'uint' of range 0-128, May be limited by device, 0 - disabled
   Default: 0
   ...
   ```
2. 在驱动程序中启用 SR-IOV，设置 **max\_vfs** 模块的参数。

   以下命令中的 `<value>` 为 **max\_vfs** 模块的具体参数。假设 ESXi 主机中所有 Mellanox 网卡的网口总数为 N，则 `<value>` 应为 N 个用英文逗号隔开的 `4`。例如，若 ESXi 主机中所有 Mellanox 网卡的网口总数为 2，则 `<value>` 应替换为 `4,4`。

   ```
   # esxcli system module parameters set -m nmlx5_core -p "max_vfs=<value>"
   ```

   如果曾配置过 pfc，则执行如下命令：

   ```
   # esxcli system module parameters set -m nmlx5_core -p "pfctx=0x08 pfcrx=0x08 trust_state=2 max_vfs=<value>"
   ```
3. 设置 ESXi 主机进入维护模式。
4. 重启 ESXi 主机。
5. 将 ESXi 主机退出维护模式。
6. 输入 `esxcli network sriovnic vf list -n <vmnic>` 命令依次检查所有 Mellanox 网卡的网口的 VF 配置，其中 `<vmnic>` 表示网口名称。

   如果每个网口的输出结果都包含 4 个 VF，如下，则表明固件和驱动程序均已成功开启 SR-IOV；否则表示开启失败，请对照[设置固件开启 SR-IOV](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_33)和本节的步骤进行检查，确保正确完成全部配置后，再重新检查 VF 配置。

   ```
   # esxcli network sriovnic vf list -n vmnic0

   VF ID  Active  PCI Address     Owner World ID
   -----  ------  --------------  --------------
       0   false  00000:101:00.1   -
       1   false  00000:101:00.2   -
       2   false  00000:101:00.3   -
       3   false  00000:101:00.4   -
   ```

---

## 设置 ESXi > 为 RDMA 功能配置流量控制

# 为 RDMA 功能配置流量控制

若集群即将开启 RDMA 功能，则还需要配置流量控制。

**注意事项**

以下操作中的网口必须使用 RDMA 网卡上已记录的指定网口，交换机端口也必须使用这些网口所连接的交换机端口。

---

## 设置 ESXi > 为 RDMA 功能配置流量控制 > 在交换机端配置流量控制

# 在交换机端配置流量控制

SMTX OS 支持在交换机中配置基于 L3 DSCP 的 PFC 流量控制和基于 Global Pause 流量控制，但推荐使用基于 L3 DSCP 的 PFC 流量控制。下面以 Mellanox Switch 为例介绍配置步骤。

## 基于 L3 DSCP 的 PFC 流量控制配置 (推荐配置)

1. 将 RoCE 的流量类型设置为 **`3`**，同时开启 ECN, 以启用 DCQCN。将 ECN 的最低和最高触发阈值都设置为 **`3000`** KB。

   ```
   switch > enable
   switch # configure terminal
   switch (config) # interface ethernet 1/1-1/2 traffic-class 3 congestion-control ecn minimum-absolute 3000 maximum-absolute 3000
   ```
2. 设置 **QoS trust mode** 为 **`L3(DSCP)`**。

   ```
   switch (config) # interface ethernet 1/1-1/2 qos trust L3
   ```
3. 设置交换机的 PFC 在 priority 3 上开启。

   ```
   switch (config) # dcb priority-flow-control enable force
   switch (config) # dcb priority-flow-control priority 3 enable
   switch (config) # interface ethernet 1/1-1/2 dcb priority-flow-control mode on force
   switch (config) # interface ethernet 1/1-1/2 pfc-wd
   ```
4. 验证 PFC 是否已开启, 确认后保存配置。

   ```
   switch (config) # show dcb priority-flow-control   
   PFC: enabled
   Priority Enabled List: 3
   Priority Disabled List: 0 1 2 4 5 6 7   
   -------------------------------------------------
   Interface        PFC admin        PFC oper
   -------------------------------------------------
   Eth1/1           Auto             Enabled
   Eth1/2           Auto             Enabled
   ......   
   switch (config) # configuration write
   ```

## 基于 Global Pause 流量控制配置

设置 RDMA 网卡所连交换机端口的 `flowcontrol` 为 **`on`**, 验证并保存配置。

```
Mellanox Switch
switch > enable
switch # configure terminal
switch (config) # interface ethernet 1/1-1/2 traffic-class 0 congestion-control ecn minimum-absolute 3000 maximum-absolute 3000
switch (config) # interface ethernet 1/1-1/2 flowcontrol send on force
switch (config) # interface ethernet 1/1-1/2 flowcontrol receive on force
switch (config) # show interfaces ethernet 1/1 | include Flow-control
Flow-control                     : receive on send on
switch (config) # show interfaces ethernet 1/2 | include Flow-control
Flow-control                     : receive on send on
switch (config) # configuration write
```

---

## 设置 ESXi > 为 RDMA 功能配置流量控制 > 在 ESXi 主机端配置流量控制

# 在 ESXi 主机端配置流量控制

SMTX OS 支持在集群的主机端通过以下两种方式为存储网络的 RDMA 功能配置流量控制：基于 L3 DSCP 流量控制配置和基于 Global Pause 流量控制配置，推荐使用基于 L3 DSCP 的流控配制。

**注意事项**

集群的主机端与交换机端所使用的流控配置方式必须保持一致。

## 基于 L3 DSCP 流量控制配置

1. 配置 Mellanox Driver 的参数，开启 PFC，将 **Trust level** 设置为 `DSCP`。其中，max\_vfs 的配置需要与[设置驱动程序开启 SR-IOV](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_34) 的步骤 2 的配置保持一致，请根据实际配置情况替换以下命令中的 `<value>`。

   ```
   # esxcli system module parameters set -m nmlx5_core -p "pfctx=0x08 pfcrx=0x08 trust_state=2 max_vfs=<value>"
   # esxcli system module parameters set -m nmlx5_rdma -p "dscp_force=26"
   ```
2. 设置 ESXi 主机进入维护模式。
3. 重启 ESXi 主机。
4. 将 ESXi 主机退出维护模式。
5. 检查并确认流量控制配置成功。

   ```
   # esxcfg-module -g nmlx5_core
   nmlx5_core enabled = 1 options = 'pfctx=0x08 pfcrx=0x08 trust_state=2 max_vfs=<value>'
   # esxcfg-module -g nmlx5_rdma
   nmlx5_rdma enabled = 1 options = 'dscp_force=26'
   ```

   其中，输出结果中 `<value>` 显示的值对应步骤 1 中相应的值。

## 基于 Global Pause 流量控制配置

一般情况下，只要保证 Mellanox Driver 没有配置 **pfctx** 参数和 **pfcrx** 参数，则网口将默认开启 Global Pause 流量控制。

输入以下命令，检查网口是否已开启 Global Pause，在返回的结果中查看对应 vmnic 的 **Pause RX** 和 **Pause TX** 列的取值。

```
# esxcli network nic pauseParams list
NIC     Pause Params Supported  Pause RX  Pause TX  Auto Negotiation  Auto Negotiation Resolution Avail  RX Auto Negotiation Resolution  TX Auto Negotiation Resolution
------  ----------------------  --------  --------  ----------------  ---------------------------------  ------------------------------  ------------------------------
vmnic1                    true      true      true             false                              false                           false                           false
vmnic2                    true      true      true             false                              false                           false                           false
```

- 如果返回值为 **True**，则表示该网口已开启 Global Pause 流量控制。
- 如果返回值为 **False**，则输入以下命令，配置 Mellanox 网卡上网口的 pause params，将 TX 和 RX 开启。其中 `vmnicX` 为配置网口的名称。

  ```
  # esxcli network nic pauseParams set -t 1 -r 1 -n vmnicX
  ```

---

## 使用 vCenter Server 纳管 ESXi 主机

# 使用 vCenter Server 纳管 ESXi 主机

如果当前环境中已有 VMware vCenter Server，请直接跳转至[将 ESXi 主机添加至 vCenter Server](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_41)，否则请先[安装 VMware vCenter Server](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_40)。

---

## 使用 vCenter Server 纳管 ESXi 主机 > 安装 VMware vCenter Server

# 安装 VMware vCenter Server

VMware vCenter Server 软件现为 Broadcom 公司的产品，请登录 [Broadcom 文档官网](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html)，参考需要安装的软件版本对应的安装和设置文档，在任意一个 ESXi 节点安装 vCenter Server。

---

## 使用 vCenter Server 纳管 ESXi 主机 > 将 ESXi 主机添加至 vCenter Server

# 将 ESXi 主机添加至 vCenter Server

1. 打开 Web 浏览器，然后输入 vCenter Server 的 IP 地址。选择**启动 vSphere Client (HTML5)**。
2. 输入具有 vCenter Server 权限的用户的凭据，然后单击**登录**。
3. 新建数据中心。在左侧导航栏选中服务器，右键选择**新建数据中心**，输入数据中心的名称。
4. 新建集群。选中新建的数据中心，右键选择**新建集群**，输入集群的名称。
5. 添加 ESXi 主机。选中新建的集群，右键选择**添加主机**。
6. 输入每个需要添加的主机的 IP 地址、用户名和密码，然后单击**下一页**，按照要求输入对应信息，将集群里的所有 ESXi 主机添加至已创建的数据中心。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_046.png)

---

## 配置存储网络

# 配置存储网络

SMTX OS 的存储网络用来处理 ESXi 主机和 SMTX OS 所在的 SCVM 之间的网络流量，可以使用 vSphere 标准交换机为 ESXi 主机和 SCVM 提供网络连接。

---

## 配置存储网络 > 为存储网络创建标准交换机

# 为存储网络创建标准交换机

1. 使用 VMware vSphere Web Client 登录 vCenter Server，浏览到 ESXi 主机。
2. 选中 ESXi 主机，选择**配置** > **网络** > **虚拟交换机** > **添加网络**，在弹出的**添加网络**界面中，选择 **VMkernel 网络适配器**，然后单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_032.png)
3. 根据管理网络和存储网络采用的网络部署模式选择目标设备。

   - 若采用网络分离部署模式，请选择**新建标准交换机**，然后单击 **NEXT**，为新创建的交换机分配合适的物理网络适配器。

     > **说明：**
     >
     > 若集群需要开启 RDMA 功能，则此处应选择 RDMA 网卡上已记录的指定网口。
   - 若采用网络融合部署模式，则无需新建标准交换机，请选择**选择现有标准交换机**，再选择管理网络虚拟交换机 vSwicth0，然后单击 **NEXT**。

     ![](https://cdn.smartx.com/internal-docs/assets/b3c87667/vmware_installation_guide_003.png)
4. 设置端口属性。将**网络标签**设置为 `ZBS-vmk`，其余设置可使用默认设置，设置完成后单击 **NEXT**。
5. 设置 IPv4 参数。选择**使用静态 IPv4 设置**，在 **IPv4 地址**中输入已规划的 ESXi 存储 IP，**子网掩码**设置为 `255.255.255.0`。
6. 按照导引进入下一步，直至完成配置。

**后续操作**

若为存储网络的标准交换机分配了两个物理网络适配器，则需要[修改标准交换机的绑定和故障切换策略](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_44)，否则，请继续[为存储网络添加虚拟机端口组](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_45)，以便为虚拟机提供连接。

---

## 配置存储网络 > 修改标准交换机的绑定和故障切换策略

# 修改标准交换机的绑定和故障切换策略

仅当为存储网络的标准交换机分配了两个物理网络适配器时需要执行以下操作，否则请忽略。

**操作步骤**

1. 选中 ESXi 主机，选择**配置** > **网络** > **虚拟交换机** > **编辑**，弹出标准交换机的编辑设置对话框。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_226.png)
2. 选择**绑定和故障切换**页签，在**故障切换顺序**区域框内将两个物理网络适配器配置为主备模式，同时将**故障恢复**选项设置为`否`。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_227.png)
3. 单击 **OK**，完成设置。

---

## 配置存储网络 > 为存储网络添加虚拟机端口组

# 为存储网络添加虚拟机端口组

1. 选中 ESXi 主机，选择**配置** > **网络** > **虚拟交换机** > **添加网络**，在弹出的**添加网络**界面中，选择**标准交换机的虚拟机端口组**，然后单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_180.png)
2. 选择目标设备。勾选**选择现有标准交换机**，选择存储网络虚拟交换机，然后单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_181.png)
3. 设置连接。将**网络标签**设置为 *ZBS*，然后单击 **NEXT** 继续完成剩下的设置。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_182.png)

   > **注意：**
   >
   > 存储网络虚拟机端口组的**网络标签**必须设置为 *ZBS*，否则将影响系统其他功能的安装和使用，比如高级监控的部署等。

**后续操作**

若集群启用 RDMA 功能，还需**为 RDMA 网络创建标准交换机**。

---

## 配置存储网络 > 为 RDMA 网络创建标准交换机

# 为 RDMA 网络创建标准交换机

仅当集群启用 RDMA 功能时需要执行以下步骤，否则请忽略。

1. 选中 ESXi 主机，选择**配置** > **网络** > **虚拟交换机** > **添加网络**，在弹出的**添加网络**界面中，选择 **标准交换机的虚拟机端口组**。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_183.png)
2. 按照**添加网络**界面引导，单击 **NEXT**，进入**选择目标设备**界面，选择**新建标准交换机**。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_184.png)
3. 在**创建标准交换机**界面，单击 **NEXT**，弹出警告提示。单击**确定**，进入下一步。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_185.png)

   > **说明：**
   >
   > RDMA 网络通过 SR-IOV 的 VF（虚拟功能）做流量收发，因此无需配置网络适配器。
4. 在**连接设置**选项中，将**网络标签**设置为 *RDMA*。单击 **NEXT** 继续完成剩下的设置。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_186.png)
5. 编辑该虚拟交换机，在**安全**选项中，将**混杂模式**从**拒绝**改为**接受**，将**伪传输**从**拒绝**改为**接受**。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_187.png)

---

## 配置 NFS 网络

# 配置 NFS 网络

NFS 网络仅供本地 ESXi 主机与主机上的 SCVM 虚拟机进行通信，因此为该网络创建的标准交换机不需要物理网络适配器，该交换机上的所有流量仅限于其内部交换。

---

## 配置 NFS 网络 > 创建新的 vSphere 标准交换机

# 创建新的 vSphere 标准交换机

1. 使用 VMware vSphere Web Client 登录 vCenter Server，浏览到 ESXi 主机。
2. 选中 ESXi 主机，选择**配置** > **网络** > **虚拟交换机** > **添加网络**，在弹出的**添加网络**界面中，选择**VMkernel 网络适配器**。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_032.png)
3. 按照**添加网络**界面引导，单击 **NEXT**，进入**选择目标设备**。选择**新建标准交换机**。
4. 在**创建标准交换机**界面，单击 **NEXT**，弹出警告提示。单击确定，进入下一步。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_047.png)
5. 设置端口属性。在**端口属性**选项页面，使用默认的属性设置，单击 **NEXT**。
6. 设置 IPv4 参数。选择**使用静态 IPv4 设置**，在 **IPv4 地址**中输入固定的 NFS VMkernel IP ：*192.168.33.1*，**子网掩码**设置为*255.255.255.0*。
7. 按照导引进入下一步，直至完成配置。

---

## 配置 NFS 网络 > 为 NFS 网络添加虚拟机端口组

# 为 NFS 网络添加虚拟机端口组

1. 单击**添加网络**图标，连接类型选择**标准交换机的虚拟机端口组**。
2. 在**选择目标设备**选项中，勾选**选择现有标准交换机**，并浏览选中新创建的交换机，单击 **NEXT**，进入下一步。
3. 在**连接设置**选项中，**网络标签**设置为 *NFS*。单击 **NEXT** 继续完成剩下的设置。

   > **注意：**
   >
   > NFS 网络虚拟机端口组的**网络标签**必须设置为 *NFS*，否则将影响系统其他功能的安装和使用，比如高级监控的部署等。

---

## 在 ESXi 节点上创建 SCVM 虚拟机

# 在 ESXi 节点上创建 SCVM 虚拟机

在集群的每个节点上配置完 ESXi 主机后，需要在每个节点上创建一个虚拟机 SCVM 用于安装 SMTX OS。

**前提条件**

- 在集群的每个节点上已成功配置完 ESXi 主机，并通过 vCenter Server 实现纳管。
- SMTX OS 安装映像文件已上传至 ESXi 主机。
- 已配置完存储网络和 NFS 网络。

---

## 在 ESXi 节点上创建 SCVM 虚拟机 > SCVM 的资源要求

# SCVM 的资源要求

SCVM 满足安装 SMTX OS 软件的最少资源如下：

- CPU：参见**构建 SMTX OS 集群的要求 > 硬件要求 > 系统资源占用**小节
- 内存：参见**构建 SMTX OS 集群的要求 > 硬件要求 > 系统资源占用**小节
- 启动盘：至少 7 GB
- 网络：管理网络、存储网络、NFS 网络
- 存储控制器或物理盘：直通模式

---

## 在 ESXi 节点上创建 SCVM 虚拟机 > 启用 RDMA 功能的配置要求

# 启用 RDMA 功能的配置要求

如果要开启集群的 RDMA 功能，需要在创建 SCVM 虚拟机时，在满足 [SCVM 的资源要求](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_51)的基础上：

- 多分配 2 核 CPU。
- 多分配 3 GB 内存。
- 分配一个 VMware 接入网络。

---

## 在 ESXi 节点上创建 SCVM 虚拟机 > 在 ESXi 主机上创建新的虚拟机

# 在 ESXi 主机上创建新的虚拟机

1. 登录 vCenter Server 主界面，浏览到 ESXi 主机。
2. 选中一台 ESXi 主机，单击右键，选择**新建虚拟机**。单击**选择创建类型** > **创建新虚拟机**。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_048.png)
3. 在**选择名称和文件夹**界面，设置虚拟机的名称和目标位置。
4. 在**选择计算资源**界面，选中 ESXi 主机的名称，单击 **NEXT** 进入下一步。
5. 选择存储。在**虚拟机存储策略**下拉菜单中选择**数据存储默认值**。
6. 选择兼容性。在**兼容**下拉菜单中选择虚拟机兼容的 ESXi 版本，建议与该虚拟机所在主机的 ESXi 版本保持一致。
7. 选择客户机操作系统。**客户机操作系统系列**中选择 **Linux**，**客户机操作系统版本**选择 **CentOS 7（64位）**。

---

## 在 ESXi 节点上创建 SCVM 虚拟机 > 为 SCVM 虚拟机配置虚拟硬件

# 为 SCVM 虚拟机配置虚拟硬件

选择完操作系统后，请执行以下步骤，为虚拟机配置硬件。

**操作步骤**

1. 根据 SCVM 的资源要求配置 CPU。

   - **每个插槽内核数**请选择 **1**，不推荐选择其他数值。
   - 为保证在 CPU 资源有限的情况下能预留足够资源供虚拟机使用，**预留**一项填入的数值应为 "CPU 核数 × 单核主频"的乘积，其中“单核主频”的具体数值需要在 ESXi 节点上输入以下命令查看。

     ```
     esxcli hardware cpu list | grep 'Core Speed' | awk '{print $NF}' | cut -c1-4 | sort -u
     ```
   - 若要开启集群的 RDMA 功能，需多分配 2 核 CPU。

   ![](https://cdn.smartx.com/internal-docs/assets/b3c87667/vmware_installation_guide_009.png)
2. 根据 SCVM 的资源要求配置内存。

   - **预留所有客户机内存（全部锁定）** 选项必须勾选。
   - 若要开启集群的 RDMA 功能，需多分配 3 GB 内存。

   ![](https://cdn.smartx.com/internal-docs/assets/b3c87667/vmware_installation_guide_010.png)
3. 设置硬盘的参数如下。

   ![](https://cdn.smartx.com/internal-docs/assets/b3c87667/vmware_installation_guide_011.png)
4. 在**新 SCSI 控制器**选项中选择 **LSI Logic 并行**，**SCSI 总线共享**设置为默认值**无**。
5. 在**虚拟硬件**页面右上角单击**添加新设备** > **网络适配器**，添加三个网络适配器，分别用于管理网络、存储网络和 NFS 网络，参数设置如下。其中，**ZBS** 网络用作存储网络，**VM Network** 网络是 ESXi 系统默认创建的管理网络，您也可以自己创建其他管理网络。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_062.png)
6. （可选）如果要开启集群的 RDMA 功能，则原有的 **ZBS** 网络将用作 VMware 接入网络，请参考以下步骤添加新的用于存储网络的网络适配器。

   1. 添加新的网络适配器，在**新网络**选项中选择 **RDMA** 网络。
   2. 根据主机的 ESXi 软件版本选择适配器类型，并添加网口。
      - ESXi 版本为 8.0：在**适配器类型**选项中选择 **PCI 设备直通**，在**设备**选项中选择 RDMA 网卡上的一个已记录的指定网口进行添加。
      - ESXi 版本为 8.0 以下：在**适配器类型**选项中选择 **SR-IOV 直通**，在**物理功能**选项中选择 RDMA 网卡上的一个已记录的指定网口进行添加。
   3. （可选）若 RDMA 网卡上已记录的指定网口不止一个，请继续重复以上操作，直至所有指定网口添加完成。
7. 在**新的 CD/DVD 驱动器**选项中选择**数据存储 ISO 文件**，上传即将要安装的 SMTX OS 安装映像文件。上传结束后，在 **CD/DVD 介质**选项中，选中 SMTX OS 安装映像文件。其他参数设置如下。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_063.png)
8. 在**虚拟硬件**页面右上角单击**添加新设备** > **PCI 设备**，若 ESXi 主机使用存储控制器管理除 ESXi 系统盘外的物理盘，请选择需要直通的存储控制器进行添加；否则请选择需要直通的物理盘进行添加。
9. 在**自定义硬件**窗口单击**虚拟机选项**页签，在 **VMware Tools** 选项中确认没有开启与主机同步时间的功能。
10. 在**高级**选项中调整虚拟机**延迟敏感度**为**高**。
11. 按照界面指引继续操作。最后单击 **Finish**，完成虚拟机的创建。

---

## 在 ESXi 节点上创建 SCVM 虚拟机 > 为 NVMe 直通硬盘热插拔功能设置 SCVM

# 为 NVMe 直通硬盘热插拔功能设置 SCVM

**注意事项**

以下步骤必须在 SCVM 创建完成后且未安装 SMTX OS 时执行。如果 SMTX OS 已安装完成，则必须重新创建 SCVM 再执行以下步骤，然后再重新安装 SMTX OS。

**操作步骤**

1. 检查集群中的 SCVM 是否都处于关机状态。如果存在已开机的 SCVM，请将其关机。
2. 在本地主机上使用终端工具打开 vmpctl 文件，然后执行以下命令以调整 SCVM 启动项为 UEFI，开启 Fixed Passthru Hot Plug Enabled 参数，以及调整 Motherboard Latout 为 ACPI。

   ```
   ./vmpctl config --address=<ESXI_IP> --username=<ESXI_USER> --password=<ESXI_PASSWORD> --vm=<SCVM_NAME>
   ```

   其中，带有 `<>` 符号的字段表示某一 SCVM 的参数，如下。

   - `ESXI_IP`：SCVM 所在 ESXi 主机的 ESXi 管理 IP。
   - `ESXI_USER`：SCVM 所在 ESXi 主机的用户名。如果用户名包含特殊字符，并且本地主机的操作系统是 Linux 或 macOS，需要在用户名两侧添加单引号（')。
   - `ESXI_PASSWORD`：SCVM 所在 ESXi 主机的密码。如果密码包含特殊字符，并且本地主机的操作系统是 Linux 或 macOS，需要在密码两侧添加单引号（')。
   - `SCVM_NAME`：SCVM 的名称。
   > **注意**：
   >
   > - 由于集群中有多个 SCVM，因此上述命令需要执行多次。您需要将命令中带有 `<>` 符号的字段依次替换成集群中每个 SCVM 的参数，然后依次执行针对不同 SCVM 的命令。
   > - 当本地主机的操作系统是 macOS 时，如果在打开 vmpctl 文件时出现弹窗提示无法打开，可能是由于该文件被系统自动阻止使用，可以单击弹窗右上角的 **?** 图标，参考弹出的说明信息打开此文件。
3. 启动 SCVM。

---

## 在 SCVM 虚拟机中安装 SMTX OS 软件

# 在 SCVM 虚拟机中安装 SMTX OS 软件

在集群的每个 ESXi 节点上创建 SCVM 后，需要在 SCVM 中安装 SMTX OS 软件。

**前提条件**

在集群的每个 ESXi 节点上已成功创建 SCVM，并且在设置时已挂载 SMTX OS 安装映像文件。

**操作步骤**

1. 在浏览器中输入 ESXi 节点的管理 IP，登录 ESXi 主机。
2. 选择**打开电源**，并打开控制台，启动 SCVM 虚拟机。
3. SCVM 启动后，进入 SMTX OS 安装引导界面后，选择 **Automatic Installation**。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_171.png)
4. 根据实际规划选择集群节点的容量规格。若选择标准容量规格，请输入字符 `1`；若选择大容量规格，请输入字符 `2`。

   ![](https://cdn.smartx.com/internal-docs/assets/b3c87667/vmware_installation_guide_004.png)
5. 选择是否将 SMTX OS 安装在两块硬盘构成的软 RAID1 上，本版本的 SMTX OS（VMware ESXi）集群不支持将 SMTX OS 安装在独立的物理硬盘上，因此请输入 `yes`。

   ![](https://cdn.smartx.com/internal-docs/assets/b3c87667/vmware_installation_guide_005.png)
6. 系统将自动选择一块容量在 7 GiB 至 240 GiB 之间的硬盘作为启动盘，如果找到一块以上符合此条件的硬盘，请根据**存储设备配置要求**中所规划和记录的启动盘，手动输入启动盘的盘符。

   ![](https://cdn.smartx.com/internal-docs/assets/b3c87667/vmware_installation_guide_006.png)
7. 系统将自动选择两块硬盘（SSD 优先）构成软 RAID1，若未找到符合条件的硬盘，或者找到两块以上符合此条件的硬盘，请根据**存储设备配置要求**中所规划和记录的**含元数据分区的缓存盘**或**含元数据分区的数据盘**，手动输入该盘的盘符。

   ![](https://cdn.smartx.com/internal-docs/assets/b3c87667/vmware_installation_guide_007.png)

   选择完硬盘后，SMTX OS 将会自动安装，安装所需时间与服务器类型和当前网络条件有关。安装完成后，服务器会自动重启。
8. 服务器重启后，用默认账户 `root` 登录 SMTX OS。

---

## 部署 SMTX OS 集群

# 部署 SMTX OS 集群

SMTX OS 使用的是向导式的部署界面，您只需按照界面指引，依次完成每个步骤的设置即可成功部署集群。

**前提条件**

- 网卡都已启动，且已获取到 IPv4 或 IPv6 地址。
- 集群内所有节点的时间统一设置为当前时间。

---

## 部署 SMTX OS 集群 > 启用高级功能的部署要求

# 启用高级功能的部署要求

如果需要启用高级功能，在部署时请注意需要为相应功能进行一些特殊设置，如下。

- **启用 RDMA 功能**：在配置集群网络时，需要启用 RDMA，并设置 VMware 接入网口和 VMware 接入 IP。
- **启用常驻缓存模式**：在配置集群存储时，需要选择“分层“模式。

---

## 部署 SMTX OS 集群 > 检查并设置部署的环境

# 检查并设置部署的环境

当每个服务器节点的 SCVM 安装完 SMTX OS 软件后，在正式部署集群前，请参照集群和节点的特点，针对每个节点设置部署环境。

**操作步骤**

1. 确认各虚拟网口对应的 MAC 地址，并调整每个网络适配器对应的端口组。

   1. 重新启动并使用 **root** 账户登录每个节点的 SCVM 系统，使用 `cd /etc/sysconfig/network-scripts/` 命令，进入配置文件路径。
   2. 使用 `ip a` 命令，确认每个虚拟网口对应的 MAC 地址。

      ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_066.png)
   3. 关闭 SCVM 虚拟机。
   4. 返回 ESXi 节点的管理界面，选中虚拟机，单击右键选择**编辑设置**，根据确认的虚拟网口名称和对应的 MAC 地址，重新调整和确认每个网络适配器对应的端口组。

      ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_065.png)
   5. 调整完成后，保存设置。重新启动并登录 SCVM 系统。
2. 设置管理网络和存储网络的网口、IP 地址和子网掩码等信息。

   使用 `vi /etc/sysconfig/network-scripts/ifcfg-*` 命令，分别修改管理网络和存储网络的网口配置文件。其中 \* 表示网口名称。

   1. 修改 **BOOTPROTO=dhcp** 为 **BOOTPROTO=static**。
   2. 修改 **ONBOOT=no** 为 **ONBOOT=yes**。
   3. 在管理网络的网口配置文件末尾添加以下内容：

      ```
      IPADDR=SMTX_ManageIP_address
      NETMASK=SMTX_ManageIP_netmask
      GATEWAY=SMTX_ManageIP_gateway
      ```

      其中 *`SMTX_ManageIP_address`* 、*`SMTX_ManageIP_netmask`* 和 *`SMTX_ManageIP_gateway`* 为实际规划的 SCVM 管理 IP 地址、子网掩码和网关。
   4. 在存储网络的网口配置文件末尾添加以下内容：

      ```
      IPADDR=SMTX_storageIP_address
      NETMASK=SMTX_storageIP_netmask
      ```

      其中 *`SMTX_storageIP_address`* 和 *`SMTX_storageIP_netmask`* 为实际规划的 SCVM 存储 IP 地址和子网掩码。
3. （可选）在每个节点的 SCVM 系统中，输入以下命令，修改主机名称，使主机名称更有辨识度。其中，`<name>` 表示需要重命名的主机名称。

   ```
   hostname <name>
   su
   ```

   在部署集群的配置主机期间勾选集群节点时，可以根据主机名称辨认集群节点。
4. 在每个节点的 SCVM 系统中执行 `systemctl restart network` 命令，重启服务。
5. 在每个节点的 SCVM 系统中执行 `systemctl status nginx` 命令，确认 nginx 服务启动。
6. 在每个节点的 SCVM 系统中执行 `systemctl status zbs-deploy-server`，确认 zbs-deploy-server 服务启动。
7. 将所有节点时间统一调整为当前时间，否则可能因同一集群不同节点的时间设置不同步，而导致集群无法正常工作。可以在每个节点的 SCVM 系统中使用 Linux 命令 `date` 进行调整，比如：`date -s "2020-06-13 15:21:23"`。

---

## 部署 SMTX OS 集群 > 开始部署

# 开始部署

1. 在浏览器中输入集群中任意一台 SCVM 的管理 IP，进入集群配置界面。
2. 阅读软件产品安装协议，单击**我已阅读并同意服务条款**。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_138.png)

---

## 部署 SMTX OS 集群 > 第 1 步：集群设置

# 第 1 步：集群设置

1. 在**集群设置**界面，输入集群的名称，选择部署架构为 **vSphere**。
2. SMTX OS 支持静态数据加密功能，可选择是否为该功能启用加密加速。如需支持 SM4 加密算法，则必须启用加密加速。
3. 在**容灾**选项中，选择**不启用同城双活**。
4. 单击**扫描集群**，进入下一步。

---

## 部署 SMTX OS 集群 > 第 2 步：扫描集群

# 第 2 步：扫描集群

待扫描集群结束后，检查扫描结果。请确保集群里待部署的节点，均显示在扫描结果中。

> **说明**：
>
> SMTX OS 会优先通过万兆网卡扫描集群发现节点；若万兆网络发现节点失败，则转由通过千兆网络发现节点。当前集群扫描同时支持 IPv4 协议和 IPv6 协议，采用 IPv6 协议扫描会通过多播地址 ff02::1 来获取当前网段的所有可联通节点；采用 IPv4 扫描会通过 nmap 发送 ICMP 报文获取可联通节点。默认采用 IPv6 协议进行扫描。
>
> 如果集群里待部署的节点未显示在扫描结果中，请检查各个节点的网卡是否已启动，以及是否配置 IPv6 地址或 IPv4 地址。

---

## 部署 SMTX OS 集群 > 第 3 步：配置主机

# 第 3 步：配置主机

1. 勾选要添加到集群的主机，取消勾选其他主机。

   > **注意**：
   >
   > 只允许选择容量规格相同的主机。
2. （可选）修改要添加到集群的主机名，使集群内各个节点的名称更有辨识度。
3. 根据 SCVM 管理 IP 或主机名称辨认并勾选集群的主节点。
4. 为集群内 SCVM 统一设置 root 账户和 smartx 账户的密码。
5. 单击**配置存储**，进入下一步。

---

## 部署 SMTX OS 集群 > 第 4 步：配置存储

# 第 4 步：配置存储

1. 根据集群要采用的存储分层或不分层模式，选择**分层**或**不分层**。

   系统会根据所选的分层模式和物理盘类型自动选择物理盘用途。

   > **注意**：
   >
   > 如需启用常驻缓存模式或使用纠删码的冗余策略，必须选择存储分层模式。
2. 当采用存储分层模式部署时，若集群内所有节点均为单一类型 SSD 全闪配置，请按照以下说明选择系统盘用途，否则请忽略。

   - 如果节点为单一属性 SSD 全闪配置，请选择系统盘用途为**含元数据分区的数据盘**。
   - 如果节点为多种属性 SSD 全闪配置，请选择系统盘用途为**含元数据分区的缓存盘**。
3. 参考在确认[存储设备配置要求](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_102#%E5%AD%98%E5%82%A8%E8%AE%BE%E5%A4%87%E9%85%8D%E7%BD%AE%E8%A6%81%E6%B1%82)时已记录的每块物理盘的用途，确认系统自动选择的物理盘用途。

   - **含有元数据分区的缓存盘**或**含有元数据分区的数据盘**：即[在 SCVM 虚拟机中安装 SMTX OS 软件](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_55)的步骤 7 所选择的物理盘，不可修改用途。
   - 其余物理盘：

     存储分层模式部署时：

     - 若节点为混闪配置，一般只有当系统判断的物理盘类型有误时，才需要手动修改用途。
     - 若节点为多种类型 SSD 全闪配置，当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**用途修改为**缓存盘**；其余情况下，只有当系统判断的物理盘类型有误时，才需要手动修改用途。
     - 若节点为单一类型且多种属性的 SSD 全闪配置，物理盘默认为**数据盘**，需手动将高性能 SSD 的用途修改为**缓存盘**；当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**的用途修改为**缓存盘**。
     - 若节点为单一类型且单一属性的 SSD 全闪配置，物理盘默认为**数据盘**，无需修改用途。

     存储不分层模式部署时：所有物理盘默认为**数据盘**，不可修改用途，但可选择**不挂载**。
4. 单击**配置网络**，进入下一步。

---

## 部署 SMTX OS 集群 > 第 5 步：配置网络

# 第 5 步：配置网络

1. 根据规划的 IP 地址分配表，在**配置集群网络**界面，填写管理和存储网络的配置信息。

   - 管理网络的管理 IP 和存储网络的存储 IP 可以通过设置起始 IP 批量设置。
   - 管理网络网口和存储网络网口的设置需要与前面确认的各个网络的虚拟网口一一对应。
   - **NTP 服务器**：如果没有外部 NTP 服务器，可以选择使用集群内主机作为 NTP 服务器。
   > **注意**：
   >
   > - 若计划将集群关联至已有的 CloudTower 且 CloudTower 配置了 NTP 服务器，请确保集群的 NTP 服务器与 CloudTower 的 NTP 服务器的时钟保持同步。
   > - 若需要开启集群的 RDMA 功能，则可单击**启用 RDMA**。启用 RDMA 功能后，还需要在 **VMware 接入网口**选项选择用于 ZBS 网络的网口，并填写实际规划的 VMware 接入 IP。
2. 单击**检查配置**，进入下一步。

---

## 部署 SMTX OS 集群 > 第 6 步：检查配置

# 第 6 步：检查配置

检查此前设置的各主机对应的物理盘用途，管理网络和存储网络的配置等信息。确认无误后，单击**执行部署**，开始部署集群。

---

## 部署 SMTX OS 集群 > 第 7 步：执行部署

# 第 7 步：执行部署

在**执行部署**界面，可看到每个主机部署的进度，也可以单击**查看日志**，查看部署的详细信息。

- 若集群部署成功，则将显示如下界面。

  ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_020.png)
- 若集群部署失败，则请先根据相关日志定位出失败原因并解决问题，然后在集群的所有 SCVM 中执行以下命令清除集群数据，最后再重新[开始部署](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_59)。

  ```
  zbs-deploy-manage clear_deploy_tag
  systemctl restart zbs-deploy-server nginx
  ```

---

## 设置参数（部署成功后）

# 设置参数（部署成功后）

部署完 SMTX OS 集群后，还需要进行以下设置：

- 设置超级管理员密码
- 关联 vSphere
- 设置 IPMI 信息
- 关联 CloudTower
- 修改存储网络的整体网络链路 MTU 值（仅适用于不启用 RDMA 功能的集群）

---

## 设置参数（部署成功后） > 设置超级管理员密码

# 设置超级管理员密码

部署成功后，需要先设置集群的超级管理员 root 账户的密码。

1. 在集群部署成功后显示的界面，单击**开始部署后配置**。
2. 设置超级管理员 **root** 的密码。
3. 单击**关联 vSphere**，进入下一步。

---

## 设置参数（部署成功后） > 关联 vSphere

# 关联 vSphere

开始配置 vSphere 相关信息，以实现集群和 vSphere 平台的集成。

1. 输入每台 ESXi 主机对应的管理 IP，以及登录的用户名和密码。
2. 单击**设置 IPMI**，界面将弹出提示框，提示关联 vSphere 成功。

---

## 设置参数（部署成功后） > 设置 IPMI 信息

# 设置 IPMI 信息

设置主机的 IPMI 信息后，可以在 CloudTower 上管理集群时使用以下功能：

- 机箱拓扑，包括主机和物理盘定位
- 主机风扇、CPU 温度和电源监控

强烈建议设置 IPMI 信息，您可以在这一步进行设置，操作步骤如下。若单击**跳过此步骤**，后续也可在 CloudTower 的集群的管理界面单击**设置 > IPMI 信息**进行设置。

**操作步骤**

1. 输入各个主机的 IPMI 管理台 IP。

   若需要设置比较多的 IPMI IP，可以在 **IPMI 起始 IP** 字段下输入一个起始 IP，所有的 IPMI IP 将以递增方式自动生成并填充。
2. 输入用户名和密码。

   在**批量设置用户名密码**字段下输入用户名和密码可以使所有主机应用相同的设置。

**后续操作**

对于存储网络带宽为 25 Gbps 及以上并且不启用 RDMA 功能的集群，需要[修改存储网络的整体网络链路 MTU 值](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_71)，以提升整体的带宽性能；否则请直接[关联 CloudTower](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_72)。

---

## 设置参数（部署成功后） > 修改存储网络的整体网络链路 MTU 值

# 修改存储网络的整体网络链路 MTU 值

对于不启用 RDMA 功能的集群，当存储网络的带宽为 25 Gbps 及以上时，需要在物理交换机端、ESXi 主机端和 SCVM 的端口修改整体网络链路的 MTU 值，以提升整体的带宽性能；否则可以忽略以下操作。

**操作步骤**

1. 登录到物理交换机管理界面，将存储网络对应物理端口的 `MTU` 修改为该交换机支持的 MTU 最大值，具体数值可参考对应交换机的使用手册。
2. 开启 ESXi 主机 SSH 服务，通过 SSH Client 连接到 ESXi 主机，参考如下步骤进行配置。

   1. 执行如下命令，修改存储网络标准交换机 `vswitch mtu` 值为 **9000**，并查看修改后的结果是否生效。其中 `vSwitch1` 表示存储网络标准交换机的名称。

      ```
      [root@localhost:~] esxcfg-vswitch -m 9000 vSwitch1
      [root@localhost:~] esxcfg-vswitch -l
      ```
   2. 执行如下命令，修改存储网络 `vmkernel mtu` 值为 **9000**，并查看修改后的结果是否生效。

      ```
      [root@localhost:~] esxcfg-vmknic -m 9000 -p VMkernel
      [root@localhost:~] esxcfg-vmknic -l
      ```
3. 在所有 ESXi 主机上参考步骤 2 完成配置，并在任意两台 ESXi 主机间使用 ping 命令确认可以 ping 通，则表示上述配置正常。

   > **注意**：
   >
   > 使用 ping 命令时，若 ping 数据包大小为默认值（ 56 Bytes），则将无法判断 MTU 值为 9000 时网络是否正常。此时，需要执行 `ping -s 8972 -d $IP`命令，将 ping 数据包大小设置为 8972 Bytes。
4. 登录 ESXi 节点的 SCVM，参考如下步骤进行配置。

   1. 编辑存储网络网卡配置文件 `/etc/sysconfig/network-scripts/ifcfg-ensxxx`, 其中 *`ensxxx`* 表具体的网卡名称。在文件中增加如下内容后并保存。

      ```
      MTU="9000"
      ```
   2. 执行命令 `systemctl restart network.service`，重启网络。
   3. 执行下述命令检查配置是否生效。其中 *`ensxxx`* 表具体的网卡名称。

      ```
      [root@localhost network-scripts]# ifconfig ensxxx
      ensxxx: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 9000
              inet 10.10.1.253  netmask 255.255.0.0  broadcast 10.10.255.255
              inet6 fe80::1b09:b2d2:ffd6:3595  prefixlen 64  scopeid 0x20<link>
              ether 52:54:00:e7:27:25  txqueuelen 1000  (Ethernet)
              RX packets 417875601  bytes 71409590956 (66.5 GiB)
              RX errors 0  dropped 390657  overruns 0  frame 0
              TX packets 156741156  bytes 62038586752 (57.7 GiB)
              TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
      ```
5. 在所有 ESXi 节点的 SCVM 中参考步骤 4 完成配置，并在任意两台 SCVM 间使用 ping 命令确认可以 ping 通，则表示上述配置正常。

   > **注意**：
   >
   > 使用 ping 命令时，若 ping 数据包大小为默认值（ 56 Bytes），则将无法判断 MTU 值为 9000 时网络是否正常。此时，需要执行 `ping -M do -s 8972 $IP`命令，将 ping 数据包大小设置为 8972 Bytes。

---

## 设置参数（部署成功后） > 关联 CloudTower

# 关联 CloudTower

SMTX OS 集群的管理服务由 CloudTower 提供。CloudTower 需安装运行在虚拟机内。在设置完 IPMI 信息后，系统将跳转至如下界面，请输入集群超级管理员的用户名和密码并单击**下一步**，然后开始关联 CloudTower。

![](https://cdn.smartx.com/internal-docs/assets/b3c87667/vmware_installation_guide_002.png)

**注意事项**

SMTX OS 与 CloudTower 的软件版本必须兼容，在安装全新的 CloudTower 或使用现有的 CloudTower 管理平台关联集群前，请务必参考[《SMTX OS 发布说明》](/smtxos/6.3.0/release_notes/release-notes)中的 “SMTX OS 与 CloudTower 版本配套说明”部分，确认即将安装或关联的 CloudTower 管理平台的版本符合配套要求。

---

## 设置参数（部署成功后） > 关联 CloudTower > 环境中已有 CloudTower

# 环境中已有 CloudTower

若当前环境中已部署 CloudTower，并且 CloudTower 支持将现有的 SMTX OS 集群纳入管理，请参考以下步骤，在 CloudTower 中关联 SMTX OS 集群。

**注意事项**

若现有的 CloudTower 管理平台版本低于当前 SMTX OS 所兼容的版本，则需升级 CloudTower 至兼容的版本。CloudTower 软件升级方法，请参见对应版本的《CloudTower 发布说明》和《CloudTower 安装与升级指南》。

**操作步骤**

1. 设置集群管理虚拟 IP 地址。设置集群的管理虚拟 IP 后，即可通过管理虚拟 IP 访问集群中可用的主机，从而保证管理界面的高可用。完成后单击**下一步**。

   > **说明：**
   >
   > 必须确保 CloudTower 可以通过管理虚拟 IP 访问集群，建议管理虚拟 IP 与节点的管理 IP 在同一个子网内。
2. 在浏览器中输入 CloudTower 的 IP 地址，以超级管理员 **root** 账户登录 CloudTower。
3. 在 CloudTower 主界面右上角单击 **+ 创建 > 关联集群**，弹出**关联集群**对话框。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_145.png)
4. 在**关联集群**对话框中按照要求填写 SMTX OS 集群的信息。完成后单击**下一步**。

   - **集群管理虚拟 IP**：填写集群的管理虚拟 IP。
   - **管理员用户名**：填写集群的超级管理员账户的用户名。
   - **管理员密码**：填写超级管理员账户对应的密码。
5. 单击**下一步**后，开始加载集群的数据，获取到集群信息后，确认即将关联的集群的信息，包括集群的名称、管理虚拟 IP、软件版本、以及使用的虚拟化平台等。
6. 为集群选择所属的数据中心。也可以选择**不加入数据中心**。

   > **说明：**
   >
   > - 您可以在关联集群的**确认关联集群**阶段，直接创建新的数据中心，然后再将此集群加入该数据中心。
   > - 若您此时选择**不加入数据中心**，在关联集群后，也可以在系统主界面创建一个新的数据中心，并重新选择加入。
7. 单击**关联集群**，成功将 CloudTower 与 SMTX OS 集群完成关联。

   > **注意**：
   >
   > - 完成集群关联后，如果发现该集群有错误或遗漏的配置而需要重新安装部署，必须先取消其与 CloudTower 的关联。
   > - 若 CloudTower 时区与集群时区不一致，建议手动调整时区使两者一致。

---

## 设置参数（部署成功后） > 关联 CloudTower > 安装全新的 CloudTower 并关联集群

# 安装全新的 CloudTower 并关联集群

若当前环境中没有 CloudTower，请现在集群的 ESXi 主机中创建一台虚拟机，并完成 CloudTower 的安装，然后在 CloudTower 中关联 SMTX OS 集群。

**前提条件**

- 提前下载 CloudTower 的安装文件（Intel x86\_64 或 AMD x86\_64 架构，ISO 映像文件）。您可以根据实际需求选择 CentOS 或 openEuler 操作系统的安装文件。
- 已规划 CloudTower 的 IP 地址、子网掩码和网关。确保 CloudTower IP 与 SMTX OS 集群的管理虚拟 IP 正常连通。

**注意事项**

在集群中安装完 CloudTower 后，请勿在 CloudTower 虚拟机中安装第三方插件，以免影响 CloudTower 虚拟机的稳定运行。

**操作步骤**

1. 设置集群管理虚拟 IP 地址。设置集群的管理虚拟 IP 后，即可通过管理虚拟 IP 访问集群中可用的主机，从而保证管理界面的高可用。完成后单击**下一步**。

   > **说明：**
   >
   > 必须确保 CloudTower 可以通过管理虚拟 IP 访问集群，建议管理虚拟 IP 与节点的管理 IP 在同一个子网内。
2. 在集群的 ESXi 主机中创建一台虚拟机，并安装 CloudTower。

   1. 新建虚拟机，并完成基本参数设置。

      - 设置硬件参数时，请综合考虑 CloudTower 待管理的集群数量，主机和虚拟机规模等信息，并结合集群主机的 CPU 利用率、内存余量和存储余量，为虚拟机设置对应的参数（参见下表中的 **CloudTower 虚拟机配置**列）。

        | **CloudTower 管理能力** | **CloudTower 虚拟机配置** |
        | --- | --- |
        | - 10 个集群 - 100 台主机 - 1000 个虚拟机 | - 4 核 CPU - 12 GB 内存 - 100 GB 存储空间 |
        | - 100 个集群 - 1000 台主机 - 10000 个虚拟机 | - 8 核 CPU - 19 GB 内存 - 400 GB 存储空间 |

        若无特殊要求，建议 **CPU** 数值设置为 `4`，**内存**设置为 `12 GB`，**新硬盘**设置为 `100 GB`。
      - 设置硬件参数时，需要挂载即将要安装的 CloudTower 的安装映像文件。
   2. 在虚拟机中完成 Guest OS 的安装。

      虚拟机 Guest OS 的默认用户名为 `smartx`。
   3. 重启后登录虚拟机 Guest OS，为 CloudTower 配置 IP，并确认虚拟机可以 ping 通 SMTX OS 集群的管理虚拟 IP。
   4. 在虚拟机 Guest OS 中依次执行如下命令，安装 CloudTower。

      ```
      sudo bash
      cd /usr/share/smartx/tower
      sh ./preinstall.sh
      cd ./installer
      ./binary/installer deploy
      ```

      若不能通过默认的虚拟 IP 访问 CloudTower，例如该虚拟机绑定多个 IP，则需要执行如下命令安装 CloudTower。其中 `$VM_IP` 表示可访问 CloudTower 的 IP 地址。

      ```
      sudo bash
      cd /usr/share/smartx/tower
      sh ./preinstall.sh
      cd ./installer
      ./binary/installer deploy --vip $VM_IP
      ```
3. 安装完成后，在 CloudTower 中关联 SMTX OS 集群。

   1. 在浏览器中输入 CloudTower 的 IP 地址，以超级管理员 **root** 账户登录 CloudTower。
   2. 在 CloudTower 主界面中间单击**关联集群**或在界面右上角单击 **+ 创建 > 关联集群**，弹出**关联集群**对话框。

      ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_145.png)
   3. 在**关联集群**对话框中按照要求填写 SMTX OS 集群的信息。完成后单击**下一步**。

      - **集群管理虚拟 IP**：填写集群的管理虚拟 IP。
      - **管理员用户名**：填写集群的超级管理员账户的用户名。
      - **管理员密码**：填写超级管理员账户对应的密码。
   4. 单击**下一步**后，开始加载集群的数据，获取到集群信息后，确认即将关联的集群的信息，包括集群的名称、管理虚拟 IP、软件版本、以及使用的虚拟化平台等。
   5. 为集群选择所属的数据中心。也可以选择**不加入数据中心**。

      > **说明：**
      >
      > - 您可以在关联集群的**确认关联集群**阶段，直接创建新的数据中心，然后再将此集群加入该数据中心。
      > - 若您此时选择**不加入数据中心**，在关联集群后，也可以在系统主界面创建一个新的数据中心，并重新选择加入。
   6. 单击**关联集群**，成功将 CloudTower 与 SMTX OS 集群完成关联。

      > **注意**：
      >
      > - 完成集群关联后，如果发现该集群有错误或遗漏的配置而需要重新安装部署，必须先取消其与 CloudTower 的关联。
      > - 若 CloudTower 时区与集群时区不一致，建议手动调整时区使两者一致。

---

## 在 CloudTower 中查看集群状态

# 在 CloudTower 中查看集群状态

关联完 SMTX OS 集群后，可以在集群的**概览**界面查看集群的基本信息。由于此时还未完成所有部署后的配置，因此集群会存在报警信息，且集群中主机的部分信息可能也无法展示，需待后续所有配置完成后，系统才会自动解除报警和获取主机信息。

---

## 为 RDMA 功能验证流量控制的配置结果

# 为 RDMA 功能验证流量控制的配置结果

在交换机和主机端部署完流控后，可以通过在任一节点的 SCVM 中，执行 SMTX OS 系统文件中自带的自动化测试脚本 `data_channel_bench.py`，以产生较大的 I/O 流量，从而验证节点流控配置的正确性。

**测试验证原理**

以三节点的 SMTX OS 集群进行举例说明。

假设 SMTX OS 集群中有 A B C 三个节点，若在三个节点上均已正确配置流量控制，则每个节点运行下面描述的 3 种典型网络 I/O 模型时，其表现应与 B 节点完全相同。B 节点的网络 I/O 模型表现如下（-> 表示数据传输方向）：

- A -> B -> C：B 节点从 A 节点接收数据，同时向 C 节点发送数据，收发两条链路传输速度应满带宽运行；
- A <- B -> C：B 节点同时向 A C 两节点发送数据，两条发送链路的速度都应为满带宽的一半；
- A -> B <- C：B 节点同时从 A C 两节点接收数据，两条接收链路的速度都应为满带宽的一半。

在集群任意节点的 SCVM 中执行自动化测试脚本 `data_channel_bench.py` 时，需指定集群所有节点的 SCVM 管理 IP 和测试的网络类型，脚本文件执行时将根据测试网络获取每个节点的 RDMA 网卡名称，然后依次对集群中的每个节点执行上述三种网络 I/O 模型的测试，从而验证每个节点的流控配置是否正确。

**注意事项**

- 执行该自动化测试脚本产生的 I/O 流量较大，很可能会影响正常业务的运行，请勿在客户的生产环境中执行此脚本文件和验证流量控制的配置结果。
- 必须使用 `smartx` 账号登录节点的 SCVM 执行该自动化测试脚本。
- 该自动化测试脚本也适用于三个节点以上的集群测试。脚本文件在执行时自动将三个节点分为一组，对每个组执行上述测试，总的测试时间约为 round\_up(N / 3) × (3 × 3) × 5 秒，约等于 N × 15 秒，其中 N 为集群节点数量。

**验证方法**

下面以 3 个节点组成的 SMTX OS 集群为例，展示存储网络的流控配置测试结果。下述带宽数据均为 MB/s。

对存储网络执行测试命令 `python /usr/share/zbs/bin/data_channel_bench.py "192.168.57.[85-87]" --mode data`。

- `/usr/share/zbs/bin/data_channel_bench.py` 为该自动化测试脚本在节点中的默认存储路径。
- `"192.168.57.[85-87]"` 表示连续的 3 个节点的管理 IP，您可根据实际节点的管理 IP 进行替换。当多个节点的管理 IP 不连续时，IP 之间可以用空格隔开，并在 IP 外侧去掉引号，例如 `192.168.57.85 192.168.57.87 192.168.57.89`。
- `--mode data` 表示设置的测试网络为存储网络。

当显示如下输出结果，并且每一行中成对出现的两个带宽数值之间的差值不超过 200 MB/s 时，表示该存储网络的流控配置正常；否则表示流控配置失败，请对照[在交换机端配置流量控制](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_36)和[在 ESXi 主机端配置流量控制](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_37)的步骤进行检查，确保已完成全部配置后，再重新验证流量控制的配置结果。

```
$ python /usr/share/zbs/bin/data_channel_bench.py -h
usage: data_channel_bench.py [-h] [--mode MODE] nodes [nodes ...]

positional arguments:
  nodes        node ips, at least 3 ips should be given. E.g. 192.168.1.1
               192.168.1.2 192.168.1.3 or 192.168.1.[1-3]

optional arguments:
  -h, --help   show this help message and exit
  --mode MODE  test mode, can be data or access. Default is data.

$ python /usr/share/zbs/bin/data_channel_bench.py "192.168.57.[85-87]" --mode data
================================================================================
[Node Info]
Node ID: 0, IP: 192.168.57.85, IBDev: rocexb8cef6030013125c, Polling CPU: set([8, 2, 3, 6]), Total CPU: 64
Node ID: 1, IP: 192.168.57.86, IBDev: rocexb8cef603001313d4, Polling CPU: set([8, 2, 3, 6]), Total CPU: 64
Node ID: 2, IP: 192.168.57.87, IBDev: rocex043f720300ffb1d8, Polling CPU: set([8, 2, 3, 6]), Total CPU: 64
--------------------------------------------------------------------------------
[Run two way test: 0 1 2]
--------------------------------------------------------------------------------
1 -> 0: 1391.75	2 -> 0: 1392
0 -> 1: 1411.5	0 -> 2: 1406
1 -> 0: 2732	0 -> 2: 2722.75
--------------------------------------------------------------------------------
0 -> 1: 1367.5	2 -> 1: 1363
1 -> 0: 1412.25	1 -> 2: 1391.5
0 -> 1: 2727	1 -> 2: 2737.25
--------------------------------------------------------------------------------
0 -> 2: 1370	1 -> 2: 1356.75
2 -> 0: 1406	2 -> 1: 1395.75
0 -> 2: 2711.25	2 -> 1: 2720.25
```

---

## 关联 vCenter

# 关联 vCenter

为保证 SMTX OS 集群可以成功获取 ESXi 主机信息，以及后续您可以为集群部署高级监控，需要在 CloudTower 中将 SMTX OS 与 vCenter 进行关联。

**前提条件**

SMTX OS 集群中所有 ESXi 主机已加入 vCenter 集群。vCenter 清单（inventory）的结构必须为：vCenter -> 数据中心 -> 集群 -> ESXi 主机。

如果当前 ESXi 主机未被 vCenter Server 纳管，请参考**使用 vCenter Server 纳管 ESXi 主机**一章进行操作。

**操作步骤**

1. 在 CloudTower 主界面的左侧导航栏中选中 SMTX OS 集群，在右侧的集群管理界面选择**设置**，在**计算平台集成**字段下选择 **vCenter Server**，进入 **vCenter 关联**界面。
2. 输入 vCenter 地址、端口号、管理员用户名和密码，选择**关联**。系统认证通过后，弹出提示关联 vCenter 成功。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_214.png)

---

## 创建 NFS Export 并挂载至 ESXi 主机

# 创建 NFS Export 并挂载至 ESXi 主机

在 SMTX OS 集群中创建的 NFS 卷可以挂载给 ESXi 主机用于存储。ESXi 主机中内置的 NFS 客户端可使用 NFS 协议通过 TCP/IP 访问 NFS 卷。

1. 在 CloudTower 的集群管理界面，单击右上方的 **+ 创建**，选择**创建 NFS Export**，弹出**新建 NFS Export**对话框。
2. 输入 NFS Export 的名称，并设置存储策略，以及访问限制等信息。单击**创建**。
3. 向 ESXi 主机添加数据存储。

   1. 使用 VMware vSphere Web Client 连接到 vCenter，浏览到 SMTX OS 集群。
   2. 选中集群后右键选择**存储** > **新建数据存储**，在弹出的**新建数据存储**对话框中指定存储类型为 **NFS**，单击 **NEXT**。
   3. 设置 NFS 版本为 **NFS 3**，单击 **NEXT**。
   4. 输入数据存储的名称、NFS 存储的文件夹名称和 NFS Server IP 地址。单击 **NEXT**。

      > **说明：**
      >
      > - NFS 存储的**文件夹**名称必须设置为 `/nfs/*`，其中 `*` 表示在 CloudTower 中所创建的 NFS 存储的名称。
      > - **服务器**的 IP 地址必须填写固定的 NFS Server IP `192.168.33.2`。

      ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_219.png)
   5. 在**主机的可访问性**列表中勾选所有主机，将数据存储挂载至集群的所有主机，单击 **NEXT**。

      ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_220.png)
   6. 单击 **FINISH**。在集群的**数据存储**页签，确认 NFS 存储已挂载成功。

      ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_221.png)
4. 如果主机的 ESXi 软件为 8.0 U2 及以上版本，请在 ESXi 系统中执行 `esxcli storage nfs firewall add --ip-mask 192.168.33.2/24` 命令手动添加一条防火墙规则。

---

## 设置 SMTX OS 的高可用性

# 设置 SMTX OS 的高可用性

为保证 SMTX OS 的高可用性，需要在 vCenter 中继续完成 ESXi 主机的部分参数配置，并在 SCVM 中部署 I/O 重路由脚本。

IO 重路由是指在本地 SCVM 失效的情况下，将业务虚拟机的 I/O 流量重新路由到远程的 SCVM 进行恢复，确保业务的高可用性。

---

## 设置 SMTX OS 的高可用性 > 设置 SCVM 在 ESXi 开机时自动启动

# 设置 SCVM 在 ESXi 开机时自动启动

1. 使用 VMware vSphere Web Client 连接到 vCenter，浏览到 ESXi 主机。
2. 选择**配置** > **虚拟机** > **虚拟机启动/关机**，单击**编辑**，弹出**编辑虚拟机启动/关机配置**对话框。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_077.png)
3. 勾选**与系统一起自动启动和停止虚拟机**，单击**确定**。
4. 重复以上步骤，对集群内其他 SCVM 同样设置与 ESXi 主机一起自动启动和关机。

---

## 设置 SMTX OS 的高可用性 > 开启 vSphere 集群 HA 并修改虚拟机的 HA 策略

# 开启 vSphere 集群 HA 并修改虚拟机的 HA 策略

1. 使用 VMware vSphere Web Client 连接到 vCenter，浏览到 ESXi 主机。
2. 选择**配置** > **系统** > **高级系统设置**，并单击**编辑**按钮。在弹出的**编辑高级系统设置**参数表中，将 **Misc.APDHandlingEnable** 参数的值修改为 `1`。
3. 参考上述步骤，将每个 ESXi 主机的 **Misc.APDHandlingEnable** 参数的值修改为 `1`。
4. 在 vCenter 中选中集群，选择**配置** > **服务** > **vSphere 可用性**，在 vSphere 可用性设置界面右侧选择**编辑**，然后在弹出的**编辑集群设置**对话框中开启 **vSphere HA** 选项。
5. 在**故障和响应**页面，进行以下设置：

   1. 开启**启用主机监控**选项。
   2. 将**主机故障响应**选项设置为**重新启动虚拟机**。
   3. 将**针对主机隔离的响应**选项设置为**关闭虚拟机电源再重新启动虚拟机**。
   4. 将**处于 PDL 状态的数据存储**选项设置为**禁用**。
   5. 展开**处于 APD 状态的数据存储**，将**全部路径异常 (APD) 故障响应**选项设置为**关闭虚拟机电源并重新启动虚拟机 - 保守的重新启动策略**，将**响应恢复**选项设置为**禁用**，再将**响应延迟**的值设置为 `3` 分钟。
6. 单击**确定**。

---

## 设置 SMTX OS 的高可用性 > 开启 ESXi 主机防火墙的 SSH 服务

# 开启 ESXi 主机防火墙的 SSH 服务

请根据 vCenter 版本选择配置方式：

- 若 vCenter 版本低于 7.0，则请[通过 vSphere Web Client 配置](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_83)。
- 若 vCenter 版本为 7.0 及以上，则请[通过命令行配置](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_84)。

---

## 设置 SMTX OS 的高可用性 > 开启 ESXi 主机防火墙的 SSH 服务 > 通过 vSphere Web Client 配置

# 通过 vSphere Web Client 配置

1. 登录 vSphere Web Client，浏览到 ESXi 主机，选择**配置** > **防火墙**，单击**编辑**，进入**编辑安全配置文件**对话框。
2. 勾选 **SSH Client** 和 **SSH Server** 后，单击**确定**，完成设置。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_085.png)
3. 针对集群里其他 ESXi 主机，重复以上步骤，开启所有 ESXi 主机防火墙的 SSH 服务。

---

## 设置 SMTX OS 的高可用性 > 开启 ESXi 主机防火墙的 SSH 服务 > 通过命令行配置

# 通过命令行配置

1. 通过 SSH 服务连接到 ESXi 主机，并以 root 账号登录 ESXi 主机。
2. 输入以下命令，设置防火墙的 SSH 服务。

   ```
   esxcli network firewall ruleset set --ruleset-id=sshClient --enabled=true
   esxcli network firewall refresh
   ```
3. 输入以下命令，检查防火墙是否生效。

   `esxcli network firewall ruleset list | grep ssh`
4. 针对集群里其他 ESXi 主机，重复以上步骤，开启所有 ESXi 主机防火墙的 SSH 服务。

---

## 设置 SMTX OS 的高可用性 > 部署 I/O 重路由脚本和 SCVM 自动重启脚本

# 部署 I/O 重路由脚本和 SCVM 自动重启脚本

**前提条件**

- 按照安装部署指导要求，已完成上述所有操作步骤。确保 ESXi 高级设置已经更改，并且集群里所有 ESXi 主机防火墙的 SSH 服务已开启。
- 确保集群内所有 SCVM 与 ESXi 主机之间可以通过 SSH 服务互相访问。
- 已配置 ESXi 节点的关联信息。可以在 CloudTower **设置**主界面，选择**计算平台集成** > **ESXi**，在弹出的 **ESXi 关联**界面中确认 ESXi 主机的管理 IP、以及账号信息都已实现关联。其中此处填写的账号需要具有写入权限。

---

## 设置 SMTX OS 的高可用性 > 部署 I/O 重路由脚本和 SCVM 自动重启脚本 > 启用 RDMA 功能的部署要求

# 启用 RDMA 功能的部署要求

若集群已启用 RDMA 功能，需要在部署脚本时，在每台 SCVM 中为 RDMA 网卡配置静态路由。

---

## 设置 SMTX OS 的高可用性 > 部署 I/O 重路由脚本和 SCVM 自动重启脚本 > 部署脚本

# 部署脚本

1. 在浏览器中输入 ESXi 主机的管理 IP，并使用 **root** 账号登录。在左侧导航栏中选中 SCVM，打开控制台。
2. 在每台 SCVM 中执行如下命令。

   `zbs-node collect_node_info`。
3. （可选）若集群已开启 RDMA 特性，则在每台 SCVM 中执行如下命令，为 RDMA 网卡配置静态路由。

   `zbs-deploy-manage deploy-rdma`。

   > **注意**：
   >
   > 如果主机的 ESXi 版本为 8.0，则需要先执行以下操作，再执行上述命令。
   >
   > 1. 使用 VMware vSphere Web Client 连接到 vCenter，浏览到 ESXi 主机。
   > 2. 选择**配置** > **网络** > **虚拟交换机**，然后在**虚拟交换机**界面右上角单击**刷新**。
   >
   >    ![](https://cdn.smartx.com/internal-docs/assets/b3c87667/vmware_installation_guide_001.png)
4. 选择其中一台 SCVM，执行如下命令。

   `zbs-deploy-manage deploy-hypervisor --gen_ssh_key`

   执行成功后，界面将显示 `Finish deploy hypervisor` 的提示信息，并且 1 分钟后您可以在 SCVM 对应的 ESXi 主机命令行界面上观察到 reroute 进程正在运行。
5. 在其他 SCVM 的控制台中，执行如下命令。

   `zbs-deploy-manage deploy-hypervisor`

   执行成功后，界面将显示 `Finish deploy hypervisor` 的提示信息，并且 1 分钟后您可以在 SCVM 对应的 ESXi 主机命令行界面上观察到 reroute 进程正在运行。

---

## 设置 SMTX OS 的高可用性 > 部署 I/O 重路由脚本和 SCVM 自动重启脚本 > 检查部署结果

# 检查部署结果

部署完成后，需要检查 I/O 重路由脚本和 SCVM 自动重启脚本的部署结果。

## 检查 I/O 重路由脚本的部署结果

**前提条件**

在 SCVM 中已部署完 I/O 重路由脚本。

**操作步骤**

脚本部署完成 5 分钟后，在集群关联的 CloudTower 上检查该集群是否出现 I/O 重路由异常的报警信息，如“存储 IP 为 xx.xx.xx.xx 的 SCVM 所在主机的 I/O 重路由服务停止工作”或者“存储 IP 为 xx.xx.xx.xx 的 SCVM 所在主机的 I/O 重路由未指向当前节点”。

- 如果未出现 I/O 重路由异常的报警信息，则说明 I/O 重路由脚本部署成功，请继续[检查SCVM 自动重启脚本的部署结果](#%E6%A3%80%E6%9F%A5-scvm-%E8%87%AA%E5%8A%A8%E9%87%8D%E5%90%AF%E8%84%9A%E6%9C%AC%E7%9A%84%E9%83%A8%E7%BD%B2%E7%BB%93%E6%9E%9C)。
- 如果有出现 I/O 重路由异常的报警信息，则请先根据相关日志定位出失败原因并解决问题，然后[清理 I/O 重路由脚本和 SCVM 自动重启脚本](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_89)，最后再重新部署。

## 检查 SCVM 自动重启脚本的部署结果

**前提条件**

在 SCVM 中已部署完 SCVM 自动重启脚本。

**操作步骤**

1. 在所有 ESXi 节点上执行 `cat /etc/rc.local.d/local.sh | grep scvm` 命令。

   若界面信息中包含 `sh /vmfs/volumes/xxxx/vmware_scvm_autostart/scvm_autostart.sh &` 提示信息，其中 `xxxx` 表示 scvm uuid，则请继续执行下一步。否则表示 SCVM 自动重启脚本部署失败。
2. 执行命令 `ls -lh /vmfs/volumes/*/vmware_scvm_autostart/scvm_autostart.sh | grep -v datastore`。

   若输出的信息中包含 `scvm_autostart.sh` 文件，则表明 SCVM 自动重启脚本部署成功。否则表示 SCVM 自动重启脚本部署失败。

**后续操作**

- 若 SCVM 自动重启脚本部署成功，则检查结束。
- 若 SCVM 自动重启脚本部署失败，请在任意一台 SCVM 中执行 `zbs-deploy-manage update-scvm-autostart` 命令部署脚本，完成后重新执行检查，确保脚本部署成功。

  若 SCVM 自动重启脚本仍然部署失败，则请联系 SmartX 售后工程师进行排查。

---

## 设置 SMTX OS 的高可用性 > 清理 I/O 重路由脚本和 SCVM 自动重启脚本部署脚本

# 清理 I/O 重路由脚本和 SCVM 自动重启脚本

如果 I/O 重路由脚本部署失败，必须先清理部署在每个 ESXi 节点和 SCVM 上的脚本。清除完成后再重新部署脚本。

**注意事项**

在 ESXi 节点参照下述步骤 2 ~ 4 执行命令清理脚本时，界面均应不显示任何输出，否则表示该步骤中的命令未按预期执行，请直接联系售后工程师进行处理。

**操作步骤**

1. 登录 SCVM，在所有 SCVM 中执行命令： `zbs-deploy-manage clear-hypervisor` ，开始清理配置。
2. 登录 ESXi 节点，在每个 ESXi 节点上执行命令：`grep scvm_failure /var/spool/cron/crontabs/root`，执行完后，若界面未显示任何输出，请继续执行下一步。
3. 在每个 ESXi 节点上执行命令：`ps -c | grep scvm_failure | grep -v grep`，执行完后，若界面未显示任何输出，请继续执行下一步。
4. 在每个 ESXi 节点上执行命令：`esxcfg-route -l | grep 192.168.33.2`，执行完后，若界面未显示任何输出，请继续执行下一步。

   > **说明**：
   >
   > 如果当前集群已开启 RDMA 功能，则在每个 ESXi 节点上还需多执行一条命令：`esxcfg-route -d y.y.y.y/32 x.x.x.x`，删除之前添加的路由。其中 *y.y.y.y* 表示 ZBS 存储网 IP 地址， *x.x.x.x* 表示网关地址。
5. 在每个 ESXi 节点上执行命令：`tail -f /var/log/scvm_failure.log`，确保不再继续输出任何信息。

   如果 `scvm_failure.log` 中的内容仍然有输出，则需要从本节步骤 1 开始，再次尝试清理，直至`scvm_failure.log` 没有内容输出为止。

**后续操作**

清理完成后，请参考[部署脚本](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_87)，重新部署 I/O 重路由脚本和 SCVM 自动重启脚本。

---

## 检查 SMTX OS 集群状态

# 检查 SMTX OS 集群状态

设置完 SMTX OS 的高可用性后，请在 CloudTower 上查看集群和集群中主机的**概览**界面。如果集群的**严重警告**信息为 0，且主机的信息已全部正常显示，则表示 SMTX OS 集群运行正常，集群的安装部署操作结束。

---

## SMTX OS 节点的本地账户与默认安全设置说明 > SMTX OS 节点的本地账户说明

# SMTX OS 节点的本地账户说明

SMTX OS 节点支持以下三种本地账户：

| 本地账户 | 说明 | 注意事项 |
| --- | --- | --- |
| root | 默认账户，默认禁止 SSH 远程登录。您可以使用该账户管理 SMTX OS 节点。 | - 请勿删除该账户。 - 强烈建议不要开启 root 账户通过 SSH 远程登录的权限。 - 以命令行方式升级集群时必须拥有 root 权限。 |
| smartx | 默认账户，默认支持 SSH 远程登录。您可以使用该账户通过 SSH 协议远程连接到 SMTX OS 节点。 | - 请勿删除该账户。 - 请勿更改 `/etc/sudoers` 里针对该账户的配置。 - 以该账户登录节点后，必须切换为 root 账户再执行运维操作。执行 `sudo su` 命令可免密码切换。 |
| 其他本地账户 | 由 root 账户创建的其他账户，账户权限由 root 账户决定。您可自行创建新的本地账户用于 SSH 远程登录。 | - |

---

## SMTX OS 节点的本地账户与默认安全设置说明 > SMTX OS 节点的默认安全设置说明

# SMTX OS 节点的默认安全设置说明

SMTX OS 系统安装完成后，会默认对 SMTX OS 节点进行如下安全设置。

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
