---
title: "SMTXZBS/5.7.0/SMTX ZBS 块存储特性说明"
source_url: "https://internal-docs.smartx.com/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_01"
sections: 33
---

# SMTXZBS/5.7.0/SMTX ZBS 块存储特性说明
## 关于本文档

# 关于本文档

本文档介绍了 SMTX ZBS 块存储集群支持的关键特性：

- 启用 RDMA 功能可降低远程节点的写入延时，提高块存储集群的整体性能。
- 启用 NVMe-oF 功能可以允许计算平台通过更高速的网络协议连接到块存储集群，提升访问效率。
- 启用常驻缓存模式可以将 ISCSI LUN 或 NVMe Namespace 内数据保留在缓存层，从而获得更稳定的高性能。

启用上述功能，除了要满足构建块存储集群的基础要求外，还需满足一些额外的要求。本文档即为您详细描述这些要求和限制，同时提供启用这些功能的部署和配置操作。

阅读本文档需了解 SMTX ZBS 块存储、RDMA 协议、NVMe-oF 协议和常驻缓存模式相关技术背景知识，并具备丰富的数据中心操作经验。

---

## 更新信息

# 更新信息

**2025-12-01：配合 SMTX ZBS 5.7.0 正式发布**

相较于 SMTX ZBS 5.6.4，本版本主要更新如下：

- 更新了 NVMe-oF 的系统资源占用；
- 更新了常驻缓存的使用限制说明。
- 调整了部分章节结构。

---

## RDMA 功能

# RDMA 功能

SMTX ZBS 块存储通过引入 RDMA 能力以优化远程节点写入延时、改进吞吐能力，实现了集群性能的显著提升。

---

## RDMA 功能 > 概述

# 概述

本章主要介绍了 RDMA 功能简介、技术实现方案和特性优势。

---

## RDMA 功能 > 概述 > 特性简介

# 特性简介

在传统的计算机系统中，CPU 负责执行所有的计算任务和数据传输任务。当数据需要从外部设备（如硬盘、显卡、网卡等）传输到内存或者从内存传输到外部设备时，CPU 必须介入进行控制，这导致了 CPU 的处理能力成了系统性能瓶颈。在此背景下出现了 DMA（Direct Memory Access，直接内存访问）技术。DMA 可通过专门的控制器实现外部设备直接读取系统内存，而不需要 CPU 参与处理，可以有效减少 CPU 的负担，使 CPU 可以专注于处理其他任务，提高系统的处理效率。

RDMA（Remote Direct Memory Access）是 DMA 在网络通信领域的扩展和演进，其核心功能为允许计算机通过传输网络直接读取远端计算机的内存，整个过程无需两端的 CPU 介入。RDMA 技术可降低 CPU 负载，解决传统数据传输方式中的瓶颈问题，实现高性能、低延时的数据传输。

![](https://cdn.smartx.com/internal-docs/assets/c6d2a776/rdma_01.png)

---

## RDMA 功能 > 概述 > 技术实现

# 技术实现

RDMA 的技术实现方案主要有三种：InfiniBand（IB）、RoCE 和 iWARP。

- **InfiniBand**（IB）

  InfiniBand 是最早实现的 RDMA 技术。InfiniBand 不依赖于以太网，包含编程接口、自身独有的网络协议栈（数据链路层、网络层、传输层）、网卡、网卡接口和交换机等一整套 RDMA 解决方案，拥有从硬件到软件的全栈全场景的技术集成。InfiniBand 可以为 RDMA 提供高性能的传输，但需要专门的硬件支持，部署成本较为高昂。
- **RoCE**（RDMA over Converged Ethernet）

  RoCE 支持在标准以太网基础设施上使用 RDMA 技术，实现 RDMA over Ethernet。RoCE 支持 RoCEv1 和 RoCEv2 两个版本。

  - **RoCEv1**

    RoCEv1 是通过以太网链路层实现的 RDMA 协议。通过使用 IB 网络层代替传统的 TCP/IP 网络层，从而在最大程度上保留 InfiniBand 的性能和特性，同时在以太网上实现对 RDMA 的支持。但同样因为使用了 IB 网络层替代了 TCP/IP 网络层， RoCEv1 仅支持在二层网络实现 RDMA，无法在三层网络实现 IP 路由功能。
  - **RoCEv2**

    RoCEv2 是对 RoCEv1 的改进。 RoCEv2 使用 UDP/IP 协议，通过以太链路层、UDP、IP 和传统的以太链路层协议栈进行数据传输，这使得 RoCEv2 可以跨越不同子网进行 RDMA 通信。RoCEv2 是目前最流行的实现 RDMA 的协议，得到了广泛的采用和支持。
- **iWARP**（Internet Wide Area RDMA Protocol）

  iWARP 是一种基于 TCP/IP 协议，可在标准以太网实现 RDMA 的技术。iWARP 支持在标准以太网基础设施上使用 RDMA，具有良好的互操作性和可扩展性，但必须要求网卡支持 iWARP，且由于其协议架构比较复杂，实现和部署相对更为困难，且性能相对更低。

在综合比较中，基于 RoCEv2 具备高灵活性、支持 IP 路由、无需使用专用硬件等优势，SMTX ZBS 块存储选择 RoCEv2 技术作为 RDMA 的实现方案，使其适用于各类网络环境，同时在性能和成本之间取得了平衡。

---

## RDMA 功能 > 概述 > 特性优势

# 特性优势

- **零拷贝**（Zero Copy）

  RDMA 允许网卡直接读取或写入内存，数据可以直接在内存之间传递，避免了数据操作系统的缓冲区之间的拷贝，实现了不同节点之间的分布式块存储服务直接通讯，有效降低延时。
- **内核旁路**（内核Bypass）

  RDMA 避免了传统传输过程中应用内存和内核之间的数据复制，在不需要任何内核参与的条件下，数据能够从应用内存发送到本地网卡并通过网络发送给远程网卡。内核旁路功能使得 RDMA 在大规模集群和分布式系统中表现出色，系统可以更轻松地处理大量节点之间的数据传输需求。
- **CPU 卸载**（CPU Offload）

  RDMA 技术通过直接在网络适配器上执行数据传输和处理，在高带宽压力下对 CPU 占用极低，能够使 CPU 更专注于计算任务而非数据传输的管理，提高系统的吞吐量和效率。这种机制适用于高并发和大规模数据处理环境，可有效减轻系统瓶颈。

---

## RDMA 功能 > 配置要求

# 配置要求

如需启用 RDMA 功能，在安装部署 SMTX ZBS 块存储集群时，该集群不仅要满足构建集群的基础要求，还需满足下述要求。

---

## RDMA 功能 > 配置要求 > 硬件要求

# 硬件要求

## CPU 架构

服务器的 CPU 架构须为以下类型：

- Intel x86\_64
- AMD x86\_64
- Hygon x86\_64
- 鲲鹏 AArch64

## 网卡

每个节点必须包含一张支持 RDMA 功能的存储网卡，目前仅支持 Mellanox Technologies 厂商的以下型号：

| **网卡型号** | **Driver 版本** | **FW 版本** | **支持的 CPU 架构** |
| --- | --- | --- | --- |
| MT27710 Family [ConnectX-4 Lx] 25 Gb | Mlx5\_core 5.0-0 | 14.24.80.00 及以上版本 | - Intel x86\_64 - AMD x86\_64 - Hygon x86\_64 - 鲲鹏 AArch64 |
| MT27800 Family [ConnectX-5] 25 Gb | Mlx5\_core 5.0-0 | 16.25.1020 及以上版本 | - Intel x86\_64 - Hygon x86\_64 - 鲲鹏 AArch64 |
| MT27800 Family [ConnectX-5] 100 Gb |
| MT2892 Family [ConnectX-6 Dx] 25 Gb | Mlx5\_core 5.0-0 | 22.37.1014 及以上版本 | - Intel x86\_64 - AMD x86\_64 - Hygon x86\_64 |
| MT28841 Family [ConnectX-6 Dx] 25 Gb | Mlx5\_core 5.0-0 | 22.37.1014 及以上版本 | - Intel x86\_64 - AMD x86\_64 - Hygon x86\_64 |
| MT28850 Family [ConnectX-6 Dx] 25 Gb | Mlx5\_core 5.0-0 | 22.37.1014 及以上版本 | - Intel x86\_64 - AMD x86\_64 - Hygon x86\_64 |
| MT28851 Family [ConnectX-6 Dx] 25 Gb | Mlx5\_core 5.0-0 | 22.37.1014 及以上版本 | - Intel x86\_64 - AMD x86\_64 - Hygon x86\_64 |
| MT2894 Family [ConnectX-6 Lx] 25 Gb | Mlx5\_core 5.0-0 | 26.37.1014 及以上版本 | - Intel x86\_64 - AMD x86\_64 - Hygon x86\_64 |

## 交换机

交换机必须支持以下一种流量控制方式：

- L3 DSCP 流控
- Global Pause 流控

## 缓存盘

推荐使用 NVMe SSD 作为缓存盘。

---

## RDMA 功能 > 配置要求 > 软件版本要求

# 软件版本要求

SMTX ZBS 块存储软件版本为标准版或企业版。

---

## RDMA 功能 > 使用限制

# 使用限制

- 仅支持在新部署块存储集群时启用 RDMA 功能。对于升级前未启用 RDMA 的集群，不支持在升级过程中及升级后对其启用该功能。
- 对于已经启用 RDMA 功能的块存储集群，在扩容时，新增节点应与待扩容集群的启用状态相同，因此需要满足启⽤ RDMA 的[配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_08)。
- 存储网络启用 RDMA 功能时，不允许与其他系统网络共用虚拟分布式交换机，且不支持启用 QoS 策略。
- 当存储网络使用 Mellanox CX5 网卡且启用 RDMA 时，仅支持配置为 `active-backup` 绑定模式。若需实现存储网络 RDMA 多路径，建议使用 Mellanox CX6 网卡。
- 不支持在双活集群中启用 RDMA 功能。

---

## RDMA 功能 > 配置 RDMA

# 配置 RDMA

如需启用块存储集群的 RDMA 功能，则应在该集群中完成相应的配置，配置流程如下：

1. 部署前，确认待部署集群满足 RDMA [配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_08)。
2. 部署时，在**配置网络**阶段，为存储网络[创建虚拟分布式交换机](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_40)时，启用块存储集群的 RDMA 功能，详情请参考《SMTX ZBS 安装部署指南》。
3. 部署后，在交换机端和主机端分别针对存储网络[配置流量控制](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_52)，详情请参考《SMTX ZBS 安装部署指南》。

---

## NVMe-oF 功能

# NVMe-oF 功能

SMTX ZBS 块存储集群支持客户端通过 NVMe over TCP 和 NVMe over RDMA 协议远程访问其块存储服务。您可以根据客户端的网络硬件条件选择通过 NVMe over TCP 或者 NVMe over RDMA 协议使用 NVMe 存储服务。

---

## NVMe-oF 功能 > 配置要求

# 配置要求

块存储集群的 NVMe-oF 功能支持 RDMA 协议（NVMe over RDMA）和 TCP 协议（NVMe over TCP）。

- 如需使用 NVMe over TCP 协议访问块存储服务：

  - 块存储集群应满足[启⽤ NVMe over TCP 的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_12)。
  - 客户端应满足[使用 NVMe over TCP 协议访问存储的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_21)。
- 如需使用 NVMe over RDMA 协议或同时使用 NVMe over TCP 和 RDMA 协议访问块存储服务：

  - 块存储集群应满足[启用 NVMe over TCP 和 RDMA 的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_13)。
  - 客户端应根据实际情况满足如下要求：
    - 仅使用 NVMe over RDMA 协议：满足[使用 NVMe over RDMA 协议访问存储的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_22)。
    - 同时使用 NVMe over TCP 和 RDMA 协议：同时满足[使用 NVMe over RDMA 协议访问存储的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_22)和[使用 NVMe over TCP 协议访问存储的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_21)。

---

## NVMe-oF 功能 > 配置要求 > 硬件要求

# 硬件要求

在安装部署块存储集群阶段，创建虚拟分布式交换机时，**启⽤ NVMe over TCP** 或**启⽤ NVMe over TCP 和 RDMA** 对集群的要求不同。因此，在安装部署块存储集群时，该集群不仅要满⾜构建块存储集群的基础要求，还需根据不同的启用项满足下述要求。

---

## NVMe-oF 功能 > 配置要求 > 硬件要求 > 启⽤ NVMe over TCP

# 启⽤ NVMe over TCP

如需使用 NVMe over TCP 协议访问块存储服务，则在安装部署块存储集群时，应**启用 NVMe over TCP**，具体硬件要求如下。

## CPU 架构

服务器的 CPU 架构须为以下类型：

- Intel x86\_64
- AMD x86\_64
- Hygon x86\_64
- 鲲鹏 AArch64

## 缓存盘

推荐使用 NVMe SSD 作为缓存盘。

---

## NVMe-oF 功能 > 配置要求 > 硬件要求 > 启⽤ NVMe over TCP 和 RDMA

# 启⽤ NVMe over TCP 和 RDMA

如需使用 NVMe over RDMA 协议或同时使用 NVMe over TCP 和 RDMA 协议访问块存储服务，则在安装部署块存储集群时，应**启⽤ NVMe over TCP 和 RDMA**，具体硬件要求如下。

## CPU 架构

服务器的 CPU 架构须为以下类型：

- Intel x86\_64
- AMD x86\_64
- Hygon x86\_64
- 鲲鹏 AArch64

## 网卡

每个节点必须包含一张支持 RDMA 功能的网卡，目前仅支持 Mellanox Technologies 厂商的以下型号：

| **网卡型号** | **Driver 版本** | **FW 版本** | **支持的 CPU 架构** |
| --- | --- | --- | --- |
| MT27710 Family [ConnectX-4 Lx] 25 Gb | Mlx5\_core 5.0-0 | 14.24.80.00 及以上版本 | - Intel x86\_64 - AMD x86\_64 - Hygon x86\_64 - 鲲鹏 AArch64 |
| MT27800 Family [ConnectX-5] 25 Gb | Mlx5\_core 5.0-0 | 16.25.1020 及以上版本 | - Intel x86\_64 - AMD x86\_64 - Hygon x86\_64 - 鲲鹏 AArch64 |
| MT27800 Family [ConnectX-5] 100 Gb |
| MT2892 Family [ConnectX-6 Dx] 25 Gb | Mlx5\_core 5.0-0 | 22.37.1014 及以上版本 | - Intel x86\_64 - AMD x86\_64 - Hygon x86\_64 |
| MT28841 Family [ConnectX-6 Dx] 25 Gb | Mlx5\_core 5.0-0 | 22.37.1014 及以上版本 | - Intel x86\_64 - AMD x86\_64 - Hygon x86\_64 |
| MT28850 Family [ConnectX-6 Dx] 25 Gb | Mlx5\_core 5.0-0 | 22.37.1014 及以上版本 | - Intel x86\_64 - AMD x86\_64 - Hygon x86\_64 |
| MT28851 Family [ConnectX-6 Dx] 25 Gb | Mlx5\_core 5.0-0 | 22.37.1014 及以上版本 | - Intel x86\_64 - Hygon x86\_64 |
| MT2894 Family [ConnectX-6 Lx] 25 Gb | Mlx5\_core 5.0-0 | 26.37.1014 及以上版本 | - Intel x86\_64 - AMD x86\_64 - Hygon x86\_64 |

## 交换机

支持 ECN 功能，同时支持以下一种流量控制方式：

- L3 DSCP 的 PFC 流控
- Global Pause 流控

## 缓存盘

推荐使用 NVMe SSD 作为缓存盘。

---

## NVMe-oF 功能 > 配置要求 > 软件版本要求

# 软件版本要求

SMTX ZBS 块存储软件版本为企业版。

---

## NVMe-oF 功能 > 配置要求 > 系统资源占用

# 系统资源占用

本版本软件支持启用 NVMe-oF 功能，启用与否会对主机 CPU 和内存占用产生差异。详细说明见《SMTX ZBS 配置与管理规格》 的[系统对主机 CPU 和内存的占用](/smtxzbs/5.7.0/zbs_installation_guide/zbs_config_specs/zbs_config_specs_07)。

---

## NVMe-oF 功能 > 配置要求 > 客户端要求

# 客户端要求

客户端可通过 NVMe over TCP 协议和 NVMe over RDMA 协议访问块存储服务，使用不同协议对客户端的配置要求不同，具体要求如下。

---

## NVMe-oF 功能 > 配置要求 > 客户端要求 > 使用 NVMe over TCP 协议访问存储

# 使用 NVMe over TCP 协议访问存储

客户端可配置为搭载 Linux 操作系统的物理机或 VMware vSphere 集群，具体配置要求如下。

- 搭载 Linux 操作系统的物理机，支持的操作系统版本：

  > **说明**
  >
  > - NVMe over TCP 接入协议支持内核 4.15 及以上的 Linux 发行版（建议使用最新的内核版本），此处仅列举了经过部署验证的版本。
  > - Linux 计算端通过 NVMe over TCP 协议访问存储服务时，如果内核版本低于 5.16.16，在计算节点和存储节点失去连接后，可能出现 Linux NVMe 驱动重连无法成功的问题，需要重启计算节点后恢复连接。

  - CentOS 8
  - Ubuntu 20.04
  - openSUSE Leap 15.3
  - Fedora 35
- VMware vSphere 集群，支持 7.0U3C 及以上版本。

---

## NVMe-oF 功能 > 配置要求 > 客户端要求 > 使用 NVMe over RDMA 协议访问存储

# 使用 NVMe over RDMA 协议访问存储

客户端可配置为搭载 Linux 操作系统的物理机或 VMware vSphere 集群，具体配置要求如下。

- 搭载 Linux 操作系统的物理机，操作系统版本要求如下：

  > **说明**
  >
  > - NVMe over RDMA 接入协议支持内核 4.15 及以上的 Linux 发行版（建议使用最新的内核版本），此处仅列举了经过部署验证的版本。
  > - Linux 计算端通过 NVMe over RDMA 协议访问存储服务时，如果内核版本低于 5.16.16，在计算节点和存储节点失去连接后，可能出现 Linux NVMe 驱动重连无法成功的问题，需要重启计算节点后恢复连接。

  - CentOS 7

    > **说明**
    >
    > CentOS 7 的 nvme\_core driver 不支持 multipath 功能，因此无法使用高可用功能。
  - CentOS 8
  - Ubuntu 20.04
  - openSUSE Leap 15.3
  - Fedora 35
- VMware vSphere 集群，支持 7.0U2 及以上版本。

---

## NVMe-oF 功能 > 使用限制

# 使用限制

- 仅支持在新部署块存储集群时启用 NVMe-oF 功能。对于升级前未启用 NVMe-oF 的块存储集群，不支持在升级过程中及升级后对其启用该功能。
- 对于已经启用 NVMe-oF 功能的块存储集群，在扩容时，新增节点应与待扩容集群的启用状态相同，因此需要满足[启⽤ NVMe over TCP 的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_12) 或 [启用 NVMe over TCP 和 RDMA 的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_13)。
- 接入网络启用 NVMe over RDMA 功能时，接入网络不能和其他系统网络共用虚拟分布式交换机，且不支持启用 QoS 策略。
- 接入网络启用 NVMe over RDMA 功能时，如需对多个网口实现 bonding，必须确保每个主机上所选的网口来自同一张支持 NVMe over RDMA 功能的网卡。
- 不支持在双活集群中启用 NVMe-oF 功能。

---

## NVMe-oF 功能 > 配置 NVMe-oF

# 配置 NVMe-oF

块存储集群的 NVMe-oF 功能支持 TCP 协议（NVMe over TCP）和 RDMA 协议（NVMe over RDMA），使用不同协议访问存储时，配置操作不同，具体操作如下所述。

## 使用 TCP 协议访问存储

1. 部署前，确认待部署集群满足[启⽤ NVMe over TCP 的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_12)。
2. 部署时，在**配置网络**阶段，为接入网络[创建虚拟分布式交换机](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_40)时，启用块存储集群的 NVMe-oF 功能，选择**启用 NVMe over TCP**，详情请参考《SMTX ZBS 安装部署指南》。
3. 部署后，[创建 NVMe Subsystem 和 Namespace](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_10)，详情请参考《SMTX ZBS 块存储配置指南》。
4. 配置客户端：

   1. 确认客户端满足[使用 NVMe over TCP 协议访问存储的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_21)。
   2. [配置客户端通过 NVMe over TCP 访问存储](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_11)，详情请参考《SMTX ZBS 块存储配置指南》。

## 仅使用 RDMA 协议或同时使用 RDMA 和 TCP 协议访问存储

1. 部署前，确认待部署集群满足[启用 NVMe over TCP 和 RDMA 的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_13)。
2. 部署时，在**配置网络**阶段，为接入网络[创建虚拟分布式交换机](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_40)时，启用块存储集群的 NVMe-oF 功能，选择**启用 NVMe over TCP 和 RDMA**。部署成功后，在交换机端和主机端分别针对接入网络[配置流量控制](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_52)，详情请参考《SMTX ZBS 安装部署指南》。
3. 部署后，[创建 NVMe Subsystem 和 Namespace](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_10)，详情请参考《SMTX ZBS 块存储配置指南》。
4. 配置客户端。

   - 客户端仅通过 **NVMe over RDMA** 协议访问存储：
     1. 确认客户端满足[使用 NVMe over RDMA 协议访问存储的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_22)。
     2. [配置客户端通过 NVMe over RDMA 访问存储](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_14)，详情请参考《SMTX ZBS 块存储配置指南》。
   - 客户端通过 **NVMe over TCP 和 RDMA** 协议访问存储：
     1. 确认客户端同时满足[使用 NVMe over TCP 协议访问存储的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_21)和[使用 NVMe over RDMA 协议访问存储的配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_22)。
     2. 配置客户端[通过 NVMe over TCP 访问存储](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_11)和[通过 NVMe over RDMA 访问存储](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_14)，详情请参考《SMTX ZBS 块存储配置指南》。

---

## 常驻缓存模式

# 常驻缓存模式

数据常驻缓存（Volume pining）是集群在分层部署（包括混闪分层部署和全闪分层部署）模式下可使用的一种存储优化策略，通过将 iSCSI LUN 或 NVMe Namespace 保留在缓存层中，可保障关键业务持续保持高性能。

---

## 常驻缓存模式 > 概述

# 概述

本章主要介绍了常驻缓存模式的功能、优势和应用场景。

---

## 常驻缓存模式 > 概述 > 特性简介

# 特性简介

分层部署的集群在默认情况下，iSCSI LUN/NVMe Namespace 中具有较高访问频率的数据将停留在速度更快的缓存层，访问频率较低的数据将下沉至速度相对较慢的数据层。在实际场景中，部分应用需要将所有数据始终保留在缓存层中以提供高性能服务。在此场景下，可以为这些应用的 iSCSI LUN 或 NVMe Namespace 启用常驻缓存模式，将数据始终保留在缓存层，从而获得更稳定的高性能。

---

## 常驻缓存模式 > 概述 > 特性优势

# 特性优势

常驻缓存模式具有如下优点：

- **为关键应用提供稳定的高性能**

  通过将特定的 iSCSI LUN 或 NVMe Namespace 始终保持在缓存层，可以使关键应用在任何时刻都能够以低延时访问数据，且可避免数据下沉至底层存储系统而导致大量请求穿透缓存直接访问底层存储的情况，确保应用可持续保持高性能。
- **提升成本效益**

  无需采用成本更高的不分层部署模式或使用全闪的分层部署模式，通过仅将特定 iSCSI LUN 或 NVMe Namespace 保留在缓存层，可在满足部分关键应用持续高性能的同时控制整体的存储成本。

---

## 常驻缓存模式 > 概述 > 应用场景

# 应用场景

常驻缓存模式主要应用场景如下：

- **关键应用持续保持高性能**

  一些关键应用，例如金融交易数据库、在线支付系统，对实时性能和数据访问的延时具有高度敏感性，任何性能波动都可能对业务产生重大影响。在这种场景下，启用常驻缓存模式可确保关键应用数据始终在高性能缓存中，为数据提供稳定的低延时访问，并可防止大量请求穿透缓存直接访问底层存储系统，保障关键业务的稳定性和可靠性。
- **低频率、高延时敏感数据访问**

  某些应用中，数据在长时间内访问频率较低，但一旦被访问，对存取速度有较高要求。在分层部署的集群中，默认按照数据的冷热程度自动分层，访问频率较低的数据会下沉到性能较低的存储中，导致再次访问时速度较慢。常驻缓存模式通过将特定存储卷保留在高性能缓存，一旦需要访问，仍可从缓存中快速获取，满足对访问速度的要求。

---

## 常驻缓存模式 > 配置要求

# 配置要求

如需启用集群的常驻缓存模式，安装部署时，该集群不仅要满足构建集群的基础要求，还需满足下述要求。

## 硬件要求

### 存储设备要求

安装部署 SMTX ZBS 块存储集群时，必须采用存储分层模式（混闪配置或多种类型 SSD 全闪配置），主机上的存储设备（即物理盘）必须满足《SMTX ZBS 安装部署指南》中分层模式下的[存储设备配置要求](/smtxzbs/5.7.0/zbs_installation_guide/zbs_installation_guide_09)。

### 缓存盘容量要求

配置常驻缓存时，为避免其占满缓存空间、影响其他卷性能，需要合理规划缓存盘容量。规划原则是：扣除常驻缓存容量后，缓存盘的剩余容量与数据盘总容量之比仍应大于 10%。

- 若集群尚未部署，应在规划阶段评估常驻缓存需求，并预留足够的缓存盘容量以支撑未来负载。
- 若集群已部署，但现有缓存盘不足以满足新增常驻缓存需求，则需按所需容量进行扩容，避免因缓存不足而无法启用常驻缓存。

**参数说明**：

| 参数 | 说明 |
| --- | --- |
| 缓存盘容量 | 对于标准容量规格节点，缓存盘容量上限为 25 TB；对于大容量规格节点，缓存盘容量上限为 50 TB。若计算得出数值小于上限值，容量可配置为计算值，否则只能配置为上限值。 |
| 热数据比例 | 数据盘中访问频率较高的数据所占的比例，一般为 10% ~ 20%。 |
| X% | 预留常驻缓存比例，为常驻缓存容量占写缓存容量的比例，且取值需为整。写缓存容量为总缓存容量的 80%。 |

#### 已知常驻缓存所需容量

若已知常驻缓存所需的具体容量，可以根据该需求来规划集群需要配置的缓存盘容量。在规划时，需要综合考虑常驻缓存卷的逻辑容量和卷的冗余策略，从而计算所需的总缓存容量。具体说明如下：

1. 确定常驻缓存卷所需的容量。通常建议预留的常驻缓存容量比所需容量大 10% ~ 20%。
2. 考虑冗余策略对常驻缓存容量的影响。

   假设集群常驻缓存卷的逻辑容量为 a，考虑冗余策略后，`需预留常驻缓存容量 = a * 副本数`。

   副本数的确定规则如下：

   - 若卷采用了副本策略，副本数为副本策略设置的副本数
   - 若卷采用了纠删码策略，副本数根据纠删码的配置确定：

     - 当 m = 1 时，副本数为 2；
     - 当 m = 2、3、4 时，副本数为 3。
3. 计算集群所需的总缓存容量。

   `集群所需总缓存容量 = 预留常驻缓存容量 / X% / 80%`
4. 确定每个节点需配置的缓存盘容量。

   `每个节点需配置的缓存盘容量 = 集群所需总缓存容量 / 节点数量 + 系统占用的缓存容量`

   > **说明**：
   >
   > 系统占用的缓存容量请参考[《SMTX ZBS 配置和管理规格》](/smtxzbs/5.7.0/zbs_installation_guide/zbs_config_specs/zbs_config_specs_preface_generic)。

**示例**：

假设一个集群由 3 个标准容量规格节点组成，每节点配置 2 块含元数据分区的缓存盘。需启用常驻缓存的卷逻辑容量为 1 TiB，采用 2 副本机制，则计算如下：

```
启用常驻缓存所需的缓存容量为 1 TiB * 2 = 2 TiB。

对应集群的总缓存容量至少为 2 TiB / 50% / 80% = 5 TiB。

每节点缓存盘至少需配置 5 TiB / 3 + 305 GiB * 2 = 2.26 TiB。
```

#### 未知常驻缓存所需容量

在常驻缓存卷容容量未知时，可以根据节点数据盘容量、热数据比例和预留常驻缓存比例来估算缓存盘所需容量。

因此，综合考虑热数据和常驻缓存卷的需求，规划缓存盘容量时，请采用如下公式计算：

`缓存盘容量 =（数据盘容量 * 热数据比例）/（1 - 0.8 * X%）`

**示例**

在一个数据中心中采用标准容量规格节点部署 SMTX ZBS 集群，单个节点的数据盘容量为 10 TB。根据业务分析，该集群中的热数据约占总数据量的 15%。此外为确保关键数据一直保持高性能，希望为常驻缓存卷预留 20% 的缓存空间。

根据如上需求，单节点所需缓存盘容量计算如下：

```
缓存盘容量 =（数据盘容量 * 热数据比例）/（1 - 0.8 * X%）
         =（10 TB * 15%）/（1 - 0.8* 20%）
         ≈ 1.786 TB
```

计算出的缓存盘容量未超过缓存盘的容量上限，建议将缓存盘容量设置为约 2 TB。

#### 计算常驻缓存卷最大可配置容量

单个常驻缓存卷最大可配置容量取决于集群预留的总常驻缓存容量和冗余策略设置。

`单个常驻缓存卷最大可配置容量 = 集群预留常驻缓存总量 / 副本数 = 集群总缓存容量 * 0.8 * X% / 副本数`

其中，副本数的确定规则如下：

- 若卷采用了副本策略，副本数为副本策略设置的副本数
- 若卷采用了纠删码策略，副本数根据纠删码的配置确定：

  - 当 m = 1 时，副本数为 2；
  - 当 m = 2、3、4 时，副本数为 3。

---

## 常驻缓存模式 > 使用限制

# 使用限制

使用常驻缓存模式具有如下使用限制：

- **部署要求**：仅支持分层部署集群，且集群内所有物理盘不能为单一类型单一属性 SSD 全闪配置。
- **主机配置要求**：

  - 非双活集群：至少需为集群内 **3** 个主机设置预留缓存比例；
  - 双活集群：至少需为每个可用域内 **2** 个主机设置预留缓存比例。
- **为常驻缓存卷预留的缓存比例**：

  - 默认预留缓存比例可设置为 1% ~ 75%；
  - 若针对单个物理盘池设置：
    - 含数据分区的物理盘池：可设置为 0%～75%；
    - 不含数据分区的物理盘池：可设置为 0%～100%。

---

## 常驻缓存模式 > 配置常驻缓存

# 配置常驻缓存

如需启用块存储集群的常驻缓存模式，应在该集群中完成相应的配置，配置流程如下：

1. 部署前，确认待部署集群的主机满足启用常驻缓存的[配置要求](/smtxzbs/5.7.0/zbs_property_notes/zbs_property_notes_28)。
2. 部署时，请参考《SMTX ZBS 安装部署指南》，在**配置存储**阶段，选择**存储分层模式**。
3. 部署后，启用常驻缓存模式：

   1. 在集群的**设置**界面中开启`允许数据常驻缓存`，并为常驻缓存卷预留缓存容量，详情请参考[《SMTX ZBS 管理指南》](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_125)。
   2. 在创建 iSCSI Target、LUN 或 NVMe Subsystem、Namespace 时启用常驻缓存模式，详情请参考《SMTX ZBS 块存储配置指南》。

      - 客户端通过 iSCSI 协议远程访问集群的块存储服务：[创建 iSCSI Target 和 LUN](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_03) 时启用常驻缓存模式。
      - 客户端通过 NVMe over TCP 或 NVMe over RDMA 协议远程访问集群的块存储服务：[创建 NVMe Subsystem 和 Namespace](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_10) 时启用常驻缓存模式。

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
