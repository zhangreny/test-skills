---
title: "SMTXELF/6.3.0/SMTX ELF 特性说明"
source_url: "https://internal-docs.smartx.com/smtxelf/6.3.0/elf_property_notes/preface-generic"
sections: 45
---

# SMTXELF/6.3.0/SMTX ELF 特性说明
## 关于本文档

# 关于本文档

SMTX ELF（读作 SmartX ELF）是由北京志凌海纳科技股份有限公司（以下简称 “SmartX” ）研发的超融合软件，提供计算虚拟化和网络、数据保护及运维管理服务，可帮助企业快速构建稳定可靠的 IT 基础架构。

SMTX ELF 支持如下几种关键特性：SR-IOV 特性、海光 HCT 特性、GPU 直通和 vGPU 功能，通过启用以上特性，可以帮助 SMTX ELF 集群增强虚拟机的性能、降低 I/O 延时，对敏感数据进行加密保护。

启用上述特性对部署 SMTX ELF 的服务器 CPU 架构、软硬件配置等均提出了一系列要求，并且每种特性所运行的虚拟化环境和使用场景均有一定限制。本文档即为您详细描述这些要求和限制，同时提供这些特性的部署和配置操作。

阅读本文档需了解 SMTX ELF 超融合软件，了解虚拟化等相关技术背景知识，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

- **2026-03-04：深度安全防护功能新增端口配置要求**
- **2026-02-04：配合 SMTX ELF 6.3.0 正式发布**

  相较于 SMTX ELF 6.2.0，本版本主要进行了如下更新：

  - 新增**深度安全防护功能**章节。
  - 更新**配置网卡 SR-IOV 直通**小节。
  - 在 **vGPU 功能**章节中增加使用 NVIDIA L20 时需选择开放驱动的说明。

---

## SR-IOV 特性

# SR-IOV 特性

SMTX ELF 支持 SR-IOV (Single Root - I/O Virtualization) 直通功能。您可以在 SMTX ELF 集群中启用网卡和加密控制器的 SR-IOV 特性。

---

## SR-IOV 特性 > 特性简介

# 特性简介

SR-IOV 是一种基于硬件的虚拟化解决方案，将一个硬件设备虚拟化为多个独立的虚拟设备的技术，从而提高性能，降低硬件成本。启用了 SR-IOV 的 PCIe 设备可以显示为多个单独的物理设备，以达到单个 I/O 资源被多个虚拟机共享的目的

SR-IOV 包括如下两种功能类型：

- **物理功能 (Physical Function，PF)**

  PF 用于支持和管理 SR-IOV 功能，是全功能的 PCIe 功能，可像其他任何 PCIe 设备一样进行发现、管理和处理。

  PF 拥有完全配置资源，可用于配置或控制 PCIe 设备。一个 PF 可以切割出多个 VF。
- **虚拟功能 (Virtual Function，VF)**

  VF 是一种轻量级的 PCIe 功能，与 PF 以及与同一 PF 关联的其他 VF 共享一个或多个物理资源。

  VF 仅允许拥有用于其自身行为的配置资源。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 概述

# 概述

在传统的虚拟化环境中，虚拟机通过虚拟交换机进行网络通信。由于引入了额外的软件层，因而限制了虚拟机对网络资源的直接访问，特别是在处理大规模网络流量的场景下，软件层可能成为性能瓶颈。

PCI 直通（PCIe Passthrough）允许虚拟机直接访问物理机上的 PCIe（Peripheral Component Interconnect Express，快速外设组件互连）设备，绕过虚拟交换机等软件层，实现了对设备的直接控制。然而，PCI 直通通常仅适用于单一虚拟机的直通。

启用网卡的 SR-IOV 特性，并配置低延时网卡加速允许在多个虚拟机之间高效共享网卡，使得虚拟机能够获得更接近于物理主机的网络性能，从而大幅降低虚拟机的网络延时。

一个支持 SR-IOV 的物理网口可虚拟化出多个 SR-IOV 直通网卡（即 VF），每个 VF 可以作为一个 SR-IOV 直通网卡，被虚拟机直接挂载使用。

![](https://cdn.smartx.com/internal-docs/assets/e7bf4e9a/SR-IOV_01.png)

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 概述 > 特性优势

# 特性优势

![](https://cdn.smartx.com/internal-docs/assets/e7bf4e9a/SR-IOV_02.png)

与**传统虚拟网卡**相比，SR-IOV 直通网卡具有如下特性：

- 可绕过虚拟化层、缩短数据传输的路径，在网络延时上可获得与传统物理网卡接近的网络 I/O 性能。
- 可结合低延时网卡的加速方案使用，绕过内核协议栈、缩短网络包的传输路径，虚拟机的网络 I/O 延时可以超过物理机直连的性能。

与 **PCI 直通网卡**相比，SR-IOV 直通网卡具备更高的可伸缩性。

SMTX ELF 支持 Solarflare 和 Mellanox 系列网卡的加速方案，具体说明如下：

- **Solarflare 系列网卡**：可使用 OpenOnload 加速方案。

  [OpenOnload](https://github.com/Xilinx-CNS/onload) 是一个高性能的运行于用户态的网络堆栈，它为使用 BSD 套接字 API 的应用程序加速 TCP 和 UDP 网络 I/O。

  建议访问 [OpenOnload 官方网站](https://www.xilinx.com/support/download/nic-software-and-drivers.html#open)下载最新发布的 OpenOnload Release Package，并参考《Onload User Guide》完成安装并使用。
- **Mellanox 系列网卡**：可使用 VMA 加速方案。

  Mellanox 的消息传递加速器（VMA）提高了基于消息和流媒体应用程序的性能，例如在金融服务市场数据环境和 Web2.0 集群中发现的应用程序。它允许通过标准套接字 API 编写的应用程序从用户态通过网络运行，并绕过内核协议栈直接操作网卡。

  建议访问 [NVIDIA 官网](https://docs.nvidia.com/networking/display/vmav970#src-99404722_safe-id-TlZJRElBTWVzc2FnaW5nQWNjZWxlcmF0b3IoVk1BKURvY3VtZW50YXRpb25SZXY5LjcuMC1Tb2Z0d2FyZURvd25sb2Fk)下载 VMA，同时参考 [VMA 文档](https://docs.nvidia.com/networking/display/vmav970/installing+vma)完成安装并使用。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 概述 > 应用场景

# 应用场景

SR-IOV 适用于对网络性能要求较高、希望使用有限的物理网卡满足多台虚拟机共享使用需求的业务场景，例如低延时高吞吐业务、多租户环境、网络密集型应用等。

- **低延时高吞吐业务**

  在金融领域，例如期货投资交易，低延时和高吞吐量至关重要。通过使用 SR-IOV 可以为虚拟机提供接近于物理机的网络性能，确保交易系统能够迅速响应市场变化，从而提高交易效率和可靠性。
- **多租户环境**

  在云计算或托管服务提供商的多租户环境中，不同租户可能共享同一组物理资源。通过使用 SR-IOV 可以有效地划分和分配网络资源，确保不同租户之间的网络隔离的同时提供良好的网络性能。
- **网络密集型应用**

  对于处理大规模网络流量的应用，如视频流处理、实时数据分析等，通过使用 SR-IOV 可以优化网络 I/O 性能、降低网络延时，确保流畅的数据传输和处理。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 配置要求

# 配置要求

如需在 SMTX ELF 集群中启用 SR-IOV 特性，则在安装部署 SMTX ELF 前，请确保您的环境满足以下所有配置要求。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 配置要求 > 硬件要求

# 硬件要求

## 网卡

网卡须支持 SR-IOV 特性，不同 CPU 架构下适配 SR-IOV 特性的网卡型号有所差异，具体如下所示。

- **Intel x86\_64 架构**

  | 品牌 | 系列 | 型号 |
  | --- | --- | --- |
  | Solarflare | X2 系列 | Solarflare XtremeScale X2522-25G Adapter |
  | 8000 系列 | Solarflare Flareon Ultra 8000 Series 10G Adapter |
  | Mellanox | CX-4 | Mellanox Technologies MT27710 Family [ConnectX-4 Lx] |
  | CX-5 | Mellanox Technologies MT27800 Family [ConnectX-5] |
  | CX-6 | Mellanox Technologies MT2892 Family [ConnectX-6 Dx] |
  | Intel | X710 | Intel Corporation Ethernet Controller X710 for 10GbE SFP+ (rev 02) |
  | 网迅 | RP1000 | Beijing Wangxun Technology Co., Ltd. Ethernet Controller RP1000 for 10GbE SFP+ (rev 03) |
- **Hygon x86\_64 架构**

  | 品牌 | 系列 | 型号 |
  | --- | --- | --- |
  | Mellanox | CX-4 | Mellanox Technologies MT27710 Family [ConnectX-4 Lx] |
  | CX-5 | Mellanox Technologies MT27800 Family [ConnectX-5] |
  | CX-6 | Mellanox Technologies MT2892 Family [ConnectX-6 Dx] |
  | Intel | X710 | Intel Corporation Ethernet Controller X710 for 10GbE SFP+ (rev 02) |
- **AMD x86\_64 架构**

  | 品牌 | 系列 | 型号 |
  | --- | --- | --- |
  | Mellanox | CX-5 | Mellanox Technologies MT27800 Family [ConnectX-5] |
- **鲲鹏 AArch64 架构**

  | 品牌 | 系列 | 型号 |
  | --- | --- | --- |
  | Mellanox | CX-5 | Mellanox Technologies MT27800 Family [ConnectX-5] |

> **说明**：
>
> Solarflare 系列网卡、Mellanox 系列网卡可结合低延时网卡加速方案进一步提升虚拟机的网络性能、降低网络延时，具体说明请参见[特性优势](/smtxelf/6.3.0/elf_property_notes/elf_property_notes_04)。

## 主机

主机须满足如下要求：

- 支持并启用 IOMMU 和 SR-IOV。
- 已安装物理网卡（PF 网卡）驱动。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 配置要求 > 客户端操作系统要求

# 客户端操作系统要求

客户端操作系统及版本与节点所配置的网卡需满足兼容性要求，已验证的兼容列表如下所示。

- **Intel x86\_64 架构**

  | 网卡型号 | Guest OS 类型 | Guest OS 版本 |
  | --- | --- | --- |
  | Solarflare XtremeScale X2522-25G Adapter | Red Hat Enterprise Linux | - RHEL 6.10 - RHEL 7.6、7.7、7.8 - RHEL 8.1、8.2、8.3、8.4 |
  | Ubuntu Server | Ubuntu 18.04 |
  | Debian GNU/Linux | Debian 9 |
  | Solarflare Flareon Ultra 8000 Series 10G Adapter | Red Hat Enterprise Linux | - RHEL 6.10 - RHEL 7.6、7.7、7.8 - RHEL 8.1、8.2、8.3、8.4 |
  | Ubuntu Server | Ubuntu 18.04 |
  | Debian GNU/Linux | Debian 9 |
  | Mellanox Technologies MT27710 Family [ConnectX-4 Lx] | Red Hat Enterprise Linux | - RHEL 7.4、7.5、7.6、7.7、7.8 - RHEL 8.0、8.1、8.2、8.3、8.4、8.5 |
  | CentOS | - CentOS 7.4、7.5、7.6、7.7、7.8 - CentOS 8.0、8.1、8.2、8.3、8.4 |
  | Ubuntu Server | - Ubuntu 16.04 - Ubuntu 18.04 |
  | Windows Server | Windows Server 2016 DC |
  | Mellanox Technologies MT27800 Family [ConnectX-5] | Red Hat Enterprise Linux | - RHEL 7.4、7.5、7.6、7.7、7.8 - RHEL 8.0、8.1、8.2、8.3、8.4、8.5 |
  | CentOS | - CentOS 7.4、7.5、7.6、7.7、7.8 - CentOS 8.0、8.1、8.2、8.3、8.4 |
  | Ubuntu Server | - Ubuntu 16.04（需手动安装 VF 驱动，参见说明 ①） - Ubuntu 18.04 |
  | Windows Server | - Windows Server 2016 - Windows Server 2019 |
  | Mellanox Technologies MT2892 Family [ConnectX-6 Dx] | Red Hat Enterprise Linux | RHEL 8.5 |
  | CentOS | CentOS 8.5 |
  | SUSE | SLES 15 SP2 |
  | Ubuntu Server | Ubuntu 20.04 |
  | Windows Server | Windows Server 2022 |
  | OpenEuler | - OpenEuler 20.03（需手动安装 VF 驱动，参见说明②） - OpenEuler 22.03 |
  | Beijing Wangxun Technology Co., Ltd. Ethernet Controller RP1000 for 10GbE SFP+ (rev 03) | 银河麒麟 | 银河麒麟桌面操作系统 V10 |
- **Hygon x86\_64 架构**

  | 网卡型号 | Guest OS 类型 | Guest OS 版本 |
  | --- | --- | --- |
  | Mellanox Technologies MT27710 Family [ConnectX-4 Lx] | OpenEuler | - OpenEuler 20.03 - OpenEuler 22.03 |
  | Mellanox Technologies MT27800 Family [ConnectX-5] | OpenEuler | - OpenEuler 20.03 - OpenEuler 22.03 |
  | Mellanox Technologies MT2892 Family [ConnectX-6 Dx] | OpenEuler | - OpenEuler 20.03（需手动安装 VF 驱动，参见说明②） - OpenEuler 22.03 |
  | Intel Corporation Ethernet Controller X710 for 10GbE SFP+ (rev 02) | OpenEuler | - OpenEuler 20.03 - OpenEuler 22.03 |
- **AMD x86\_64 架构**

  | 网卡型号 | Guest OS 类型 | Guest OS 版本 |
  | --- | --- | --- |
  | Mellanox Technologies MT27800 Family [ConnectX-5] | Red Hat Enterprise Linux | - RHEL 7.4、7.5、7.6、7.7、7.8 - RHEL 8.0、8.1、8.2、8.3、8.4、8.5 |
  | CentOS | - CentOS 7.4、7.5、7.6、7.7、7.8 - CentOS 8.0、8.1、8.2、8.3、8.4 |
  | Ubuntu Server | - Ubuntu 16.04（需手动安装 VF 驱动，参见说明 ①） - Ubuntu 18.04 |
  | Windows Server | - Windows Server 2016 - Windows Server 2019 |
- **鲲鹏 AArch64 架构**

  | 网卡型号 | Guest OS 类型 | Guest OS 版本 |
  | --- | --- | --- |
  | Mellanox Technologies MT27800 Family [ConnectX-5] | OpenEuler | - OpenEuler 20.03 - OpenEuler 22.03 |

部分客户端操作系统需手动安装 VF 驱动，请参见如下说明。

- **说明 ①**

  对于使用 Mellanox Technologies MT27800 Family [ConnectX-5] 网卡的主机，当客户端操作系统为 `Ubuntu 16.04` 时，需要在客户端操作系统中手动安装 VF 驱动。请登录 [NVIDIA 官方网站](https://network.nvidia.com/products/ethernet-drivers/linux/mlnx_en/)，下载并安装适用于 Ubuntu 16.04 的网络适配器驱动程序。
- **说明 ②**

  对于使用 Mellanox Technologies MT2892 Family [ConnectX-6 Dx] 网卡的主机，当客户端操作系统为 `OpenEuler 20.03` 时，需要在客户端操作系统中手动安装 VF 驱动。请登录 [NVIDIA 官方网站](https://network.nvidia.com/products/infiniband-drivers/linux/mlnx_ofed/)，下载并安装适用于 OpenEuler 20.03 的网络适配器驱动程序。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 使用限制及影响

# 使用限制及影响

开启网口的 SR-IOV 特性有其使用限制，并且可能影响其他功能。

- 允许集群中仅有部分主机支持 SR-IOV 特性，而其他主机不支持。
- 使用 SR-IOV 直通网卡对其他功能的影响请参考《SMTX ELF 管理指南》[挂载 SR-IOV 直通网卡或 PCI 直通网卡的影响](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_212)。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 配置网卡 SR-IOV 直通

# 配置网卡 SR-IOV 直通

使用网卡的 SR-IOV 特性时需在 SMTX ELF 集群中完成相应的配置，具体配置流程如下图所示。

![](https://cdn.smartx.com/internal-docs/assets/e7bf4e9a/SR-IOV_03.png)

**注意事项**

每次只允许对一个主机的一个网口进行 SR-IOV 相关配置，包括切换网口用途至 **SR-IOV 直通**和编辑 SR-IOV 直通网卡个数，不可同时对两个网口进行操作。

**配置流程**

1. 部署 SMTX ELF 集群前，在需要启用 SR-IOV 特性的所有主机的 BIOS 中开启 IOMMU 和 SR-IOV。

   具体操作请参考《SMTX ELF 集群安装部署指南》的[检查 BIOS 设置](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_22)小节设置 BIOS。
2. 登录 CloudTower，在需要启用 SR-IOV 特性的主机上启用 IOMMU。

   具体操作请参考《SMTX ELF 管理指南》的[启⽤ IOMMU](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_119) 小节，启用后主机 IOMMU 状态变更为`待重启`。

   > **说明**：
   >
   > 进入主机的网口列表，如果 **SR-IOV 状态**显示为`驱动未就绪`，则需单击**重配**，重新配置网口的 SR-IOV 驱动，相关配置将在主机重启后生效。
3. 重启主机。

   具体操作请参考《SMTX ELF 运维指南》的[重启节点](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_45#%E5%85%B3%E9%97%AD%E5%92%8C%E9%87%8D%E5%90%AF%E4%B8%BB%E6%9C%BA)小节。
4. 编辑需要启用 SR-IOV 特性的网口，将**网口用途**切换为 **SR-IOV 直通**，并设置直通网卡个数。

   具体操作请参考《SMTX ELF 管理指南》的[切换网口用途](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_138)小节。

   配置完成后，如需修改 SR-IOV 直通网卡数量，可以参考《SMTX ELF 管理指南》的[重新切分 SR-IOV 直通网卡数量](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_139)小节，重新设置直通网卡个数。
5. 返回主机的网口列表，确认上述步骤中所编辑的网口已增加如下信息，表明此网口已启用 SR-IOV。

   - **所属主机 IOMMU 状态**：`已生效`
   - **SR-IOV 状态**：`已启用`
   - **SR-IOV 直通网卡**：显示步骤 4 中设置的值
   - **SR-IOV 直通网卡已使用数量**：`0`
6. 参考上述步骤 2 ~ 5，为其他主机中支持 SR-IOV 特性的网口启用 SR-IOV。
7. 在包含启用 SR-IOV 特性的网口所在的主机上，为虚拟机挂载 SR-IOV 直通网卡。

   - 创建虚拟机并挂载 SR-IOV 直通网卡：请参考《SMTX ELF 管理指南》的[创建虚拟机](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_012)小节。
   - 为已有虚拟机挂载 SR-IOV 直通网卡：请参考《SMTX ELF 管理指南》的[编辑网络设备](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_044)小节。
8. 进入虚拟机列表，选中已挂载 SR-IOV 直通网卡的虚拟机，在右侧弹出的虚拟机详情面板中查看**网络设备**，SR-IOV 直通网卡的图标中将带有 **SR** 字样。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 概述

# 概述

数据加密是保障关键敏感信息机密性、完整性和有效性的重要手段之一，加密控制器（又称加密卡、密码卡等）是一种能够在虚拟化环境中提供加密保障的 PCIe 设备。

在传统虚拟化架构下，一个加密控制器只能服务一个虚拟机，造成资源的低效利用，增加了硬件使用成本也影响了业务扩展。

通过支持 SR-IOV，一个加密控制器可以虚拟化出多个虚拟加密控制器，即 VF，每个 VF 都可以分别被不同的虚拟机挂载使用，从而显著提升加密控制器的利用率，降低硬件成本，提高加密处理效率。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 概述 > 特性优势

# 特性优势

与传统的加密控制器应用方式相比，基于 SR-IOV 技术实现加密控制器的直通具有如下优势：

- 实现一个物理加密控制器服务多台虚拟机，减少对硬件设备的需求，降低硬件使用成本。
- 在多个虚拟环境中并发进行加密任务，且多个虚拟环境间操作互不影响，有效提高加密处理的效率与稳定性。
- 提供灵活的资源分配与管理能力，根据实际业务需求动态调整 VF 的数量和分配方式，能够迅速响应业务变化，实现更高的扩展性。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 概述 > 应用场景

# 应用场景

加密控制器 SR-IOV 直通适用于对数据安全要求较高、希望使用有限的物理加密控制器满足多台虚拟机共享加密功能的业务场景，例如含敏感数据业务、多租户环境等。

- **含敏感数据业务**

在金融、医疗等领域，存在例如个人身份信息、财务数据、医疗记录等大量敏感数据，将加密控制器通过 SR-IOV 直通给虚拟机使用，实现对敏感数据的加密保护，并帮助企业达成行业的数据合规要求。

- **多租户环境**

在云计算或托管服务提供商的多租户环境中，通过使用 SR-IOV 有效地划分和分配加密控制器，确保多租户共享同一组物理硬件，并允许各租户独立进行加密操作。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 配置要求

# 配置要求

如需在 SMTX ELF 集群中使用 SR-IOV 加密控制器，则在安装部署 SMTX ELF 前，请确保您的环境满足以下所有配置要求。

## 硬件要求

### CPU 架构

服务器的 CPU 架构须为以下类型：

- Intel x86\_64
- Hygon x86\_64
- 鲲鹏 AArch64

### 加密控制器

加密控制器须为以下型号，如需使用其他型号，请联系 SmartX 确认是否可用。

- 渔翁 PCIe V7.1
- 三未信安 SJK1727(ZQ-H)

### 主机

主机须支持并启用 IOMMU 和 SR-IOV。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 对其他功能的影响

# 对其他功能的影响

使用 SR-IOV 加密控制器对其他功能的影响请参考《SMTX ELF 管理指南》[挂载加密控制器的影响](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_234)。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 使用加密控制器 SR-IOV 直通

# 使用加密控制器 SR-IOV 直通

使用 SR-IOV 特性时需在 SMTX ELF 集群中完成相应的配置，具体配置流程如下图所示。

![](https://cdn.smartx.com/internal-docs/assets/e7bf4e9a/SR-IOV_04.png)

**注意事项**

配置加密控制器 SR-IOV 直通时，需要将主机进入维护模式以及重启主机，建议每次只在一台主机上操作。

**准备工作**

- 部署 SMTX ELF 集群前，在需要启用 SR-IOV 特性的所有主机的 BIOS 中开启 IOMMU 和 SR-IOV。

  请参考《SMTX ELF 集群安装部署指南》的[检查 BIOS 设置](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_22)小节设置 BIOS。
- 根据主机当前的内核版本和加密控制器品牌，获取对应的加密控制器驱动包。

  执行命令 `uname -a` ，可以查看该主机当前的内核版本。

**配置流程**

1. 登录 CloudTower，在需要启用 SR-IOV 特性的加密控制器所在主机上启用 IOMMU。

   具体操作请参考《SMTX ELF 管理指南》的[启⽤ IOMMU](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_119)小节，启用后主机 IOMMU 状态变更为`待重启`。
2. 设置主机进入维护模式。

   具体操作请参考《SMTX ELF 运维指南》的[进入主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_41)小节。
3. 在主机上配置加密控制器主机驱动。

   根据加密控制器的品牌参考对应的配置方式：

   - 渔翁

     1. 在主机上执行如下命令，安装加密控制器驱动包：

        ```
        rpm -ivh <fisec_rpm_name>
        ```
     2. 编辑配置文件 `/etc/modprobe.d/fisec.conf`，设置 SR-IOV 直通 VF 数量。
     3. 编辑配置文件 `/etc/modules-load.d/fisec.conf`，声明在系统启动时自动加载对应驱动。
   - 三未信安

     1. 在主机上执行如下命令，安装加密控制器驱动包：

        ```
        rpm -ivh <swcsm_rpm_name>
        ```
     2. 编辑配置文件 `/etc/modprobe.d/sw.conf`，设置 SR-IOV 直通 VF 数量。
     3. 编辑配置文件 `/etc/modules-load.d/swcsm.conf`，声明在系统启动时自动加载对应驱动。
4. 重启主机。

   具体操作请参考《SMTX ELF 运维指南》的[重启节点](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_45)小节。
5. 返回主机的 PCI 设备列表，确认上述步骤中所编辑的加密控制器已增加如下信息，表明此加密控制器已启用 SR-IOV。

   - **所属主机 IOMMU 状态**：`已生效`
   - **直通状态**：`已启用`
   - **设备切分数量**：显示步骤 3 中设置的值
   - **设备切分已使用数量**：`0`
6. 参考上述步骤 1 ~ 5，为其他主机中支持 SR-IOV 特性的加密控制器启用 SR-IOV。
7. 登录 CloudTower，参考《SMTX ELF 运维指南》将该主机[退出主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_44)。
8. 为该主机上的虚拟机挂载 SR-IOV 直通加密控制器。

   - 创建虚拟机并挂载 SR-IOV 直通加密控制器：请参考《SMTX ELF 管理指南》的[创建虚拟机](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_012)小节。
   - 为已有虚拟机挂载 SR-IOV 直通加密控制器：请参考《SMTX ELF 管理指南》的[挂载或卸载加密控制器](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_235)小节。
9. 在挂载了加密控制器的虚拟机的操作系统上安装加密控制器的虚拟机驱动。
10. 进入虚拟机列表，选中已挂载 SR-IOV 直通加密控制器的虚拟机，在右侧弹出的虚拟机详情面板中查看**加密控制器**。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 重新切分加密控制器

# 重新切分加密控制器

本节描述的操作步骤仅适用于在 SMTX ELF 集群中重新切分加密控制器的场景。

**准备工作**

将主机上所有挂载了该加密控制器的虚拟机关机，或确认当前没有虚拟机挂载该加密控制器。

**操作步骤**

1. 设置主机进入维护模式。

   具体操作请参考《SMTX ELF 运维指南》的[进入主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_43)小节。
2. 编辑加密控制器驱动配置文件，重新设置 SR-IOV 直通 VF 数量。

   不同品牌的加密控制器配置文件不同：

   - 渔翁：`/etc/modprobe.d/fisec.conf`
   - 三未信安：`/etc/modprobe.d/sw.conf`
3. 执行如下命令，更新加密控制器驱动中的 SR-IOV 直通 VF 数量：

   ```
   echo <new_vf_num> >/sys/bus/pci/devices/<bus_location_id>/sriov_numvfs
   ```

   其中 `<new_vf_num>` 是上一步骤中设置的 SR-IOV 直通 VF 数量；`<bus_location_id>` 是加密控制器的总线 ID ，可在 CloudTower 的 **PCI 设备**页面查看。
4. 执行如下命令，查看当前加密控制器的分配信息，在输出结果中确认该加密控制器的 `device_id`。

   ```
   zbs-node pci list_assign_info
   ```
5. 执行如下命令，更新加密控制器的配置信息。

   ```
   zbs-node pci update_target_device --device_id <device_id>
   ```

   其中 `<device_id>` 是上一步骤中查询的结果。
6. 登录 CloudTower，参考《SMTX ELF 运维指南》将该主机[退出主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_44)。

---

## 海光 HCT 特性

# 海光 HCT 特性

海光 HCT（Hygon Cryptographic Technology）是海光基于密码协处理器和密码指令集设计和研发的一套密码算法加速技术软件开发套件，能够提供软硬件结合的国密算法加密服务。SMTX ELF 支持将 CCP（Crypto Coprocessor）设备通过 MDEV 形式透传给虚拟机使用，直接利用 CPU 资源高效执行国密算法，具备硬件成本低、系统架构简单、加密处理效率高等优势。

海光 HCT 适用于对敏感数据低成本保护、高吞吐量和低延时等业务场景。

- **敏感数据保护**

  海光 HCT 可为需要保护敏感信息的业务场景提供加密支持，如个人身份信息、支付数据、医疗记录等，无需其他硬件支持即可确保数据在存储和传输过程中得到加密保护，低成本实现防止数据泄露或篡改。
- **高吞吐量、低延迟业务**

  在需要处理大量数据并确保快速响应的业务场景中，HCT 基于硬件模块提升数据加解密处理速度，满足在例如实时通信、在线交易等包含大量数据的场景下提高响应速度的需求。

---

## 海光 HCT 特性 > 配置要求

# 配置要求

如需在 SMTX ELF 集群中使用 HCT 特性，则在安装部署 SMTX ELF 前，请确保您的环境满足以下所有配置要求。

## 硬件要求

### CPU

服务器的 CPU 架构必须为 Hygon x86\_64 架构，且 CPU 型号为海光二代及以上。

### 主机

主机须支持并启用 IOMMU。

## 客户端操作系统要求

虚拟机操作系统中已安装驱动。

---

## 海光 HCT 特性 > 对其他功能的影响

# 对其他功能的影响

使用 CCP 设备 MDEV 直通对其他功能的影响请参考《SMTX ELF 管理指南》[挂载加密控制器的影响](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_234)。

---

## 海光 HCT 特性 > 使用 CCP 设备 MDEV 直通

# 使用 CCP 设备 MDEV 直通

使用海光 HCT 特性时需在 SMTX ELF 集群中完成相应的配置，具体配置流程如下图所示。

![](https://cdn.smartx.com/internal-docs/assets/e7bf4e9a/hct_01.png)

**注意事项**

配置 CCP 设备 MDEV 直通时，需要将主机进入维护模式以及重启主机，建议每次只在一台主机上操作。

**配置流程**

1. 设置主机进入维护模式。

   具体操作请参考《SMTX ELF 运维指南》的[进入主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_43)小节。
2. 登录 CloudTower，在需要使用 CCP 设备 MDEV 直通的虚拟机所在主机上启用 IOMMU。若主机 IOMMU 状态为`已启用`，请直接进行第 4 步。

   具体操作请参考《SMTX ELF 管理指南》的[启⽤ IOMMU](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_119) 小节，启用后主机 IOMMU 状态变更为`待重启`。
3. 重启主机。

   具体操作请参考《SMTX ELF 运维指南》的[重启节点](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_46)小节。
4. 在主机的 BIOS 中开启 IOMMU 并设置 HCT 相关配置。

   具体操作请参考《SMTX ELF 集群安装部署指南》的[检查 BIOS 设置](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_25)小节设置 BIOS。
5. 为主机导入安全证书。

   具体操作请参考[龙蜥社区文档](https://openanolis.cn/sig/Hygon-Arch/doc/865622274698254162)。
6. 证书导入成功后，执行如下命令清除主机因 hag 产生的大页内存：

   ```
   $ rm -f /dev/hugepages/tkm_page_0
   ```
7. 在主机上执行如下命令，切分 CCP 设备：

   ```
   $ zbs-node hct create_mdev_instances [--count <count>]
   ```

   其中 `[--count <count>]` 为可选参数，不配置该参数则默认会在每个 CCP 设备上创建出 32 个 mdev 实例，配置 `<count>` 参数则可以指定出其他数量的 mdev 实例，允许配置为 1～128。
8. 在主机上执行如下命令，同步数据：

   ```
   $ zbs-node hct update_devices
   $ zbs-deploy-manage config_cgroup;zbs-deploy-manage config_hugepage --need_restart
   $ systemctl restart job-center-worker
   ```
9. 返回主机的 PCI 设备列表，确认上述步骤中所编辑的 CCP 设备已增加如下信息，表明此 CCP 设备已启用 MDEV 直通。

   - **所属主机 IOMMU 状态**：`已生效`
   - **设备用途**：`MDEV 直通`
   - **直通状态**：`已启用`
   - **设备切分数量**：显示步骤 7 中设置的值
   - **设备切分已使用数量**：`0`
10. 参考上述步骤 1 ~ 9，为其他包含 CCP 设备的主机进行配置。
11. 登录 CloudTower，参考《SMTX ELF 运维指南》将该主机[退出主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_44)。
12. 为该主机上的虚拟机挂载 CPP 设备。

    - 创建虚拟机并挂载：请参考《SMTX ELF 管理指南》的[创建虚拟机](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_012)小节。
    - 为已有虚拟机挂载：请参考《SMTX ELF 管理指南》的[挂载或卸载加密控制器](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_235)小节。
13. 在挂载了 CCP 设备的虚拟机的操作系统上安装 HCT 驱动。

    具体操作请参考[龙蜥社区文档](https://openanolis.cn/sig/Hygon-Arch/doc/1110520213566721211)。
14. 进入虚拟机列表，选中已挂载 MDEV 直通 CCP 设备的虚拟机，在右侧弹出的虚拟机详情面板中查看**加密控制器**。

---

## 海光 HCT 特性 > 重新切分 CCP 设备

# 重新切分 CCP 设备

本节描述的操作步骤仅适用于在 SMTX ELF 集群中重新切分海光 CCP 设备的场景。

**准备工作**

将主机上所有挂载了该 CCP 设备的虚拟机关机，或确认当前没有虚拟机挂载该 CCP 设备。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间切分 CCP 设备，以避免在主机维护模式期间执行快照操作。

但若集群遇到特殊情况，必须在快照执行期间切分 CCP 设备，您也可以参考下述步骤进行更换。

**操作步骤**

1. 设置主机进入维护模式。

   具体操作请参考《SMTX ELF 运维指南》的[进入主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_43)小节。
2. 在主机上执行如下命令，清理当前的 CCP 设备：

   ```
   $ zbs-node hct clean_all_mdevs
   ```
3. 在主机上执行如下命令，更新 CCP 设备的切分数量并同步数据：

   ```
   $ zbs-node hct create_mdev_instances [--count INTEGER] 
   $ zbs-node hct update_devices
   ```
4. 登录 CloudTower，参考《SMTX ELF 运维指南》将该主机[退出主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_44)。

---

## GPU 直通功能

# GPU 直通功能

GPU 直通是指将物理 GPU 完整地透传给虚拟机使用的功能。

通过 GPU 直通，一台虚拟机将独占一个或多个物理 GPU，拥有物理 GPU 所提供的极强的图像加速处理能力和浮点计算能力，在短时间内能够完成并行的图形处理和海量计算，从而⽀持机器学习模型、高性能计算等，如金融行业使用的反欺诈、交易算法。

---

## GPU 直通功能 > 配置要求

# 配置要求

如需在 SMTX ELF 集群中使用 GPU 直通功能，SMTX ELF 集群需满足以下配置要求。

## 硬件要求

- **CPU 架构**

  服务器的 CPU 架构为 Intel x86\_64、Hygon x86\_64 或 鲲鹏 AArch64。如需在其他架构下使用 GPU 直通功能，请联系 SmartX 确认是否可用。
- **GPU 型号**

  请通过[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/?tab=0)，根据您使用的服务器机型确认当前可选择的 GPU 设备型号。

> **注意**：
>
> 当您使用 NVIDIA RTX 4090、RTX A6000 和 T1000 时，请先参考[前置操作](/smtxelf/6.3.0/elf_property_notes/elf_property_notes_14)解绑该 GPU 的声卡驱动。

---

## GPU 直通功能 > 驱动要求

# 驱动要求

使用 GPU 直通时请您在即将挂载和使用 GPU 的虚拟机上安装 GPU 驱动。

---

## GPU 直通功能 > 特定 GPU 型号的前置操作

# 特定 GPU 型号的前置操作

NVIDIA RTX 4090、RTX A6000 和 T1000 的 GPU 设备将在操作系统上占用两个 PCI 地址，分别对应一个显卡设备和一个声卡设备，而声卡设备在主机开机时会自动绑定到声卡驱动上。当您使用这类 GPU 前，请务必参考本小节内容解绑该 GPU 的声卡驱动，否则挂载该直通 GPU 的虚拟机将无法开机。

请您登录 GPU 所属的主机执行以下步骤：

1. 执行如下命令获取声卡设备的 PCI 地址：

   ```
   ls /sys/bus/pci/devices/<PCI Address of Graphics Card>/iommu_group/devices/
   ```

   其中 `<PCI Address of Graphics Card>` 应根据实际情况替换为显卡设备的 PCI 地址即 CloudTower 展示的 GPU ID。

   输出结果中包含的另一个 PCI 地址即为声卡设备的 PCI 地址。
2. 执行如下命令获取声卡设备绑定的的声卡驱动的名称：

   ```
   ll /sys/bus/pci/devices/<PCI Address of Sound Card>/driver/module/drivers
   ```

   其中 `<PCI Address of Sound Card>` 应根据实际情况替换为步骤 1 中获取的声卡设备的 PCI 地址。

   **示例**

   ```
   ll /sys/bus/pci/devices/0000:86:00.1/driver/module/drivers
   total 0
   lrwxrwxrwx 1 root root 0 Sep 12 13:27 pci:snd_hda_intel -> ../../../bus/pci/drivers/snd_hda_intel
   ```

   表示 PCI 地址为 `0000:86:00.1` 的声卡设备绑定的声卡驱动的名称为 `snd_hda_intel`。
3. 执行如下命令将 GPU 设备从当前绑定的声卡驱动中解绑：

   ```
   echo "<PCI Address of Sound Card>" > /sys/bus/pci/devices/<PCI Address of Sound Card>/driver/unbind
   ```
4. 执行如下命令将声卡驱动加入黑名单，使其不会在主机开机时被自动加载：

   ```
   echo "blacklist <Sound Card Driver>" > /etc/modprobe.d/blacklist_snd_hda_intel.conf
   ```

   其中 `<Sound Card Driver>` 应根据实际情况替换为步骤 2 中获取的声卡驱动名称。

---

## GPU 直通功能 > 使用限制及影响

# 使用限制及影响

使用 GPU 直通功能有其使用限制，并且可能影响其他功能。

## 使用限制

GPU 设备启用 MIG 模式时，无法使用 GPU 直通功能。请参考 [NVIDIA 官方文档](https://docs.nvidia.com/grid/index.html)《Virtual GPU Software User Guide》> **Installing and Configuring NVIDIA Virtual GPU Manager** > **Disabling MIG Mode for One or More GPUs** 关闭此模式。

## 对其他功能的影响

使用 GPU 直通对虚拟机其他功能的影响请参考《SMTX ELF 管理指南》的[挂载 GPU 直通设备或 vGPU 的影响](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_218)章节。

---

## GPU 直通功能 > 使用 GPU 直通

# 使用 GPU 直通

在主机上安装 GPU 设备后，参照本节操作完成相关配置后即可在虚拟机上使用 GPU 设备。

![](https://cdn.smartx.com/internal-docs/assets/e7bf4e9a/gpu_passthrough_01.png)

**准备工作**

获取虚拟机 GPU 驱动。请您根据 GPU 型号、虚拟机操作系统和 GPU 设备厂商官⽅⽀持的驱动版本，从 GPU 设备厂商的官网获取。

**操作流程**

1. 登录主机执行命令以禁用 nouveau 驱动。

   1. 执行以下命令，创建两个配置文件：

      ```
      cat <<_EOF_ > /etc/modprobe.d/gpu-passthrough-disable-nouveau.conf
      blacklist nouveau
      options nouveau modeset=0
      _EOF_
      ```

      ```
      cat <<_EOF_ > /usr/lib/modprobe.d/gpu-passthrough-disable-nouveau.conf
      blacklist nouveau
      options nouveau modeset=0
      _EOF_
      ```
   2. 执行以下命令卸载 nouveau 模块。

      ```
      modprobe -r nouveau
      ```
2. 登录 CloudTower 为 GPU 设备所在主机[开启 IOMMU](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_119) 并重启主机，详情请参考《SMTX ELF 管理指南》。
3. 选择 GPU 设备⽤途为直通。

   如⾸次使⽤该 GPU 设备，设备⽤途默认为直通，请直接参照第 4 步进⾏操作；如此前已将 GPU 设备切分为 vGPU，则先将 [GPU 设备⽤途切换为直通](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_129#%E7%BC%96%E8%BE%91-gpu-%E8%AE%BE%E5%A4%87%E7%94%A8%E9%80%94)，详情请参考《SMTX ELF 管理指南》。
4. [挂载 GPU 设备给虚拟机](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_131)，详情请参考《SMTX ELF 管理指南》。
5. 为虚拟机安装 GPU 驱动，需参考 GPU 设备厂商提供的官方技术文档。
6. 重启虚拟机。

---

## vGPU 功能

# vGPU 功能

vGPU 是将物理 GPU 通过虚拟化技术切割得到的逻辑形态，一个物理 GPU 可以切割为多个 vGPU，vGPU 可以作为虚拟显卡分配给虚拟机。

通过 vGPU 功能，管理员可以根据需求灵活分配有限的 GPU 资源，使多台虚拟机共享一个物理 GPU 的图像加速处理能力和浮点计算能力，从而满足机器学习推理、三维设计与建模、游戏开发、图像渲染等相关应⽤开发与测试的共享需求，还可以为 VDI 提供可运⾏ 2D/3D 开发设计软件的环境。

---

## vGPU 功能 > 配置要求

# 配置要求

如需在 SMTX ELF 集群中使用 vGPU 功能，SMTX ELF 集群需满足以下配置要求。

## 硬件要求

- **CPU 架构**

  服务器的 CPU 架构为 Intel x86\_64 架构。如需在其他架构下使用 vGPU 功能，请联系 SmartX 确认是否可用。
- **GPU 型号**

  请通过[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/?tab=0)，根据您使用的服务器机型确认当前可选择的 GPU 设备型号。

---

## vGPU 功能 > 驱动要求

# 驱动要求

使用 vGPU 需要同时配套 vGPU 软件。

---

## vGPU 功能 > 驱动要求 > 驱动介绍

# 驱动介绍

NVIDIA 官方发布的 vGPU 软件包含 NVIDIA Virtual GPU Manager 和 NVIDIA Graphics Driver。

- NVIDIA Virtual GPU Manager 是部署在虚拟化平台为虚拟机提供 vGPU 功能的驱动，包含专有驱动和开放驱动。SmartX 对 NVIDIA Virtual GPU Manager 进行了改造和适配，并随 SMTX ELF 发布，后文将其称为 **vGPU 驱动**。
- NVIDIA Graphics Driver 是部署在使用 GPU 的虚拟机中使其可以使用 GPU 设备的驱动，后文将其称为 **GPU 驱动**。

在 SMTX ELF 集群中的虚拟机使用 vGPU 时需要提前获取这两个驱动。其中 **vGPU 驱动**需从 SmartX 获取，并参考[安装 vGPU 驱动](/smtxelf/6.3.0/elf_property_notes/elf_property_notes_27)章节内容将其安装在 GPU 设备所在的主机上；**GPU 驱动**需从 NVIDIA 获取，并参考 [NVIDIA 官方文档](https://docs.nvidia.com/grid/latest/grid-vgpu-user-guide/index.html#installing-grid-vgpu-display-drivers)的指引将其安装在即将挂载和使用 vGPU 的虚拟机上。

---

## vGPU 功能 > 驱动要求 > 驱动版本选择

# 驱动版本选择

- **vGPU 驱动版本**

  参考 NVIDIA 官方提供的发布说明及 SMTX ELF 版本配套的 vGPU 驱动版本，选择 NVIDIA Virtual GPU Manager 版本，也就是 **vGPU 驱动**版本。
- **GPU 驱动版本**

  根据所选择的 vGPU 驱动版本和 NVIDIA 官方提供的兼容性列表，选择与主机 vGPU 驱动版本适配的虚拟机 GPU 驱动版本。

---

## vGPU 功能 > 驱动要求 > 安装和升级 vGPU 驱动 > 安装 vGPU 驱动

# 安装 vGPU 驱动

使用 vGPU 前需参照本节内容在主机上安装 vGPU 驱动。

**准备工作**

- 执行命令 `uname -a` ，查看该主机当前的内核版本。
- 根据内核版本和所需的 vGPU 驱动版本，获取驱动安装包。

  > **说明**：
  >
  > 使用 NVIDIA L20 时请选择开放驱动。

**操作步骤**

1. 登录 CloudTower，参考《SMTX ELF 运维指南》将主机[置为主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_43)。
2. 上传驱动安装包到该主机的 `/home/smartx` 路径下。
3. 执行如下命令，完成安装。

   ```
   cd /home/smartx && rpm -ivh <rpm_name>
   ```
4. 通过命令 `rpm -qi Nvidia-vGPU`，查看已安装的驱动信息，确认安装成功。示例输出如下：

   ```
   $rpm -qi Nvidia-vGPU
   Name        : Nvidia-vGPU
   Version     : 14.2
   Release     : 4.18.0_193.28.1.el7.smartx.11
   Architecture: x86_64
   Install Date: Fri 03 Mar 2023 02:58:24 PM CST
   Group       : Unspecified
   Size        : 69359565
   License     : GPL
   Signature   : (none)
   Source RPM  : Nvidia-vGPU-14.2-4.18.0_193.28.1.el7.smartx.11.src.rpm
   Build Date  : Thu 09 Feb 2023 11:19:37 AM CST
   Build Host  : 5e21f91597c8
   Relocations : (not relocatable)
   URL         : http://www.smartx.com
   Summary     : Nvidia vGPU driver
   Description :
   Dynamically create, increase and shrink
   ```
5. 通过 CloudTower 或 IPMI 管理界面重启该主机。
6. 重启完成后，执行命令 `nvidia-smi`，输出 GPU 信息，则证明驱动功能正常。示例输出如下：

   ```
   $nvidia-smi
   Fri Apr 14 10:27:43 2023
   +-----------------------------------------------------------------------------+
   | NVIDIA-SMI 510.85.03    Driver Version: 510.85.03    CUDA Version: N/A      |
   |-------------------------------+----------------------+----------------------+
   | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
   | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
   |                               |                      |               MIG M. |
   |===============================+======================+======================|
   |   0  Tesla V100-PCIE...  On   | 00000000:2F:00.0 Off |                    0 |
   | N/A   32C    P0    25W / 250W |     50MiB / 16384MiB |      0%      Default |
   |                               |                      |                  N/A |
   +-------------------------------+----------------------+----------------------+

   +-----------------------------------------------------------------------------+
   | Processes:                                                                  |
   |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
   |        ID   ID                                                   Usage      |
   |=============================================================================|
   |  No running processes found                                                 |
   +-----------------------------------------------------------------------------+
   ```
7. 登录 CloudTower，参考《SMTX ELF 运维指南》将该主机[退出主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_44)。

---

## vGPU 功能 > 驱动要求 > 安装和升级 vGPU 驱动 > 升级 vGPU 驱动

# 升级 vGPU 驱动

当前用户所使用的 vGPU 版本无法支持用户所需特性或应用时，需要升级主机上的 vGPU 驱动。

**准备工作**

- 执行命令 `uname -a` ，查看该主机当前的内核版本。根据内核版本和所需的 vGPU 驱动版本，获取驱动安装包。

  > **说明**：
  >
  > 使用 NVIDIA L20 时请选择开放驱动。
- 待升级驱动所在主机上挂载了 vGPU 的虚拟机均处于`关机`状态。

**操作步骤**

1. 登录 CloudTower，参考《SMTX ELF 运维指南》将主机[置为主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_43)。
2. 上传驱动安装包到该主机的 `/home/smartx` 路径下。
3. 执行如下命令，删除现有的驱动。

   ```
   rpm -e Nvidia-vGPU
   ```
4. 删除后执行命令 `rpm -qi Nvidia-vGPU`，确认驱动已删除成功，示例输出如下：

   ```
   $rpm -qi Nvidia-vGPU
   package Nvidia-vGPU is not installed
   ```
5. 执行如下命令，完成新驱动包安装。

   ```
   cd /home/smartx && rpm -ivh <new_rpm_name>
   ```
6. 通过命令 `rpm -qi Nvidia-vGPU`，查看已安装的驱动信息，确认安装成功。示例输出如下：

   ```
   $rpm -qi Nvidia-vGPU
   Name        : Nvidia-vGPU
   Version     : 14.2
   Release     : 4.18.0_193.28.1.el7.smartx.11
   Architecture: x86_64
   Install Date: Fri 03 Mar 2023 02:58:24 PM CST
   Group       : Unspecified
   Size        : 69359565
   License     : GPL
   Signature   : (none)
   Source RPM  : Nvidia-vGPU-14.2-4.18.0_193.28.1.el7.smartx.11.src.rpm
   Build Date  : Thu 09 Feb 2023 11:19:37 AM CST
   Build Host  : 5e21f91597c8
   Relocations : (not relocatable)
   URL         : http://www.smartx.com
   Summary     : Nvidia vGPU driver
   Description :
   Dynamically create, increase and shrink
   ```
7. 通过 CloudTower 或 IPMI 管理平台重启该主机。
8. 重启完成后，执行命令 `nvidia-smi`，输出 GPU 信息，则证明驱动功能正常。示例输出如下：

   ```
   $nvidia-smi
   Fri Apr 14 10:27:43 2023
   +-----------------------------------------------------------------------------+
   | NVIDIA-SMI 510.85.03    Driver Version: 510.85.03    CUDA Version: N/A      |
   |-------------------------------+----------------------+----------------------+
   | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
   | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
   |                               |                      |               MIG M. |
   |===============================+======================+======================|
   |   0  Tesla V100-PCIE...  On   | 00000000:2F:00.0 Off |                    0 |
   | N/A   32C    P0    25W / 250W |     50MiB / 16384MiB |      0%      Default |
   |                               |                      |                  N/A |
   +-------------------------------+----------------------+----------------------+

   +-----------------------------------------------------------------------------+
   | Processes:                                                                  |
   |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
   |        ID   ID                                                   Usage      |
   |=============================================================================|
   |  No running processes found                                                 |
   +-----------------------------------------------------------------------------+
   ```
9. 登录 CloudTower，参考《SMTX ELF 运维指南》将该主机[退出主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_44)。

---

## vGPU 功能 > 使用限制及影响

# 使用限制及影响

使用 vGPU 功能有其使用限制，并且可能影响虚拟机的其他功能。

## 使用限制

GPU 设备启用 MIG 模式时，无法使用 vGPU 功能。请参考 [NVIDIA 官方文档](https://docs.nvidia.com/grid/index.html) 《Virtual GPU Software User Guide》> **Installing and Configuring NVIDIA Virtual GPU Manager** > **Disabling MIG Mode for One or More GPUs** 关闭此模式。

## 对其他功能的影响

使用 vGPU 对虚拟机其他功能的影响请参考《SMTX ELF 管理指南》的[挂载 GPU 直通设备或 vGPU 的影响](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_218)章节。

---

## vGPU 功能 > 使用 vGPU

# 使用 vGPU

在主机上安装 GPU 设备后，参照本节操作进行配置即可在虚拟机上使用 vGPU。

![](https://cdn.smartx.com/internal-docs/assets/e7bf4e9a/vgpu_01.png)

**注意事项**

使用 vGPU 需同时参考 NVIDIA 官方文档进行配置。请在 [NVIDIA 官网](https://docs.nvidia.com/grid/index.html)查看 vGPU 软件版本相对应的文档或章节。本章节内提及的所有 NVIDIA 官方文档的名称和查找路径均以 15.3 为例，其他版本可能略有不同。

**准备⼯作**

- 根据主机架构、主机内核版本和所选择的 vGPU 驱动版本，从 SmartX 获取主机 vGPU 驱动安装包。
- 根据所选择的主机 vGPU 驱动版本和兼容性列表，在 NVIDIA 获取与主机 vGPU 驱动版本适配的虚拟机 GPU 驱动。
- 购买 vGPU 授权或[申请试⽤版](https://enterpriseproductregistration.nvidia.com/?LicType=EVAL&ProductFamily=vGPU)。
- 准备另⼀个虚拟机，在其中部署并配置 NVIDIA vGPU software License Server。详情请参考 [NVIDIA 官方文档](https://docs.nvidia.com/grid/index.html)《Client Licensing User Guide》。

  > **说明：**
  >
  > 请您确保部署 License Server 的虚拟机与安装 GPU 驱动的虚拟机网络连通。

**操作流程**

1. 在 GPU 设备所在主机上[安装 vGPU 驱动](/smtxelf/6.3.0/elf_property_notes/elf_property_notes_27)。
2. 在 CloudTower 完成如下操作：

   1. 为 GPU 设备所在主机[开启 IOMMU](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_119) 并重启主机，详情请参考《SMTX ELF 管理指南》。
   2. 将 [GPU ⽤途切换为 vGPU](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_129#%E7%BC%96%E8%BE%91-gpu-%E8%AE%BE%E5%A4%87%E7%94%A8%E9%80%94)，并选择切分规格，详情请参考《SMTX ELF 管理指南》。
   3. [挂载 vGPU 给虚拟机](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_131)，详情请参考《SMTX ELF 管理指南》。
3. 在挂载 vGPU 的虚拟机上完成如下操作：

   1. 为虚拟机安装 GPU 驱动并重启虚拟机。具体请参考 [NVIDIA 官方文档](https://docs.nvidia.com/grid/index.html)《Virtual GPU Software User Guide》的 **Installing the NVIDIA vGPU Software Graphics Driver** 章节。
   2. 在虚拟机 GPU 驱动中关联 License Server，配置 License Server IP 及端⼝信息。具体请参考 [NVIDIA 官方文档](https://docs.nvidia.com/grid/index.html)《Client Licensing User Guide》。

---

## 深度安全防护功能

# 深度安全防护功能

随着虚拟化和云技术的发展，业务系统规模和网络复杂度不断增加，病毒、恶意软件及网络攻击的威胁也日益复杂。传统依赖单机或代理式防护的方式，在大规模虚拟化环境中已难以满足实时防护和统一管理的需求。

为保障业务连续性、数据安全及网络环境稳定，SMTX ELF 提供了深度安全防护功能，针对病毒查杀、恶意流量识别、异常行为监测等多类安全风险进行实时检测与拦截，为虚拟机提供高效、统一的安全防护能力。

---

## 深度安全防护功能 > 概述

# 概述

深度安全防护功能集成亚信的信舱云主机安全 DeepSecurity，通过在集群中统一部署**安全防护虚拟机（SVM，Security Virtual Machine）**，以无代理的方式提供了虚拟机粒度的病毒查杀、以及虚拟网卡粒度的深度包检测能力，能够有效阻止病毒入侵并对网络流量进行深度分析，保障整体网络环境的安全性。

配置深度安全防护功能后，可为业务虚拟机提供如下功能：

- **防病毒**：支持防恶意软件，对病毒、间谍软件、木马等威胁进行查杀，并提供资产管理和入侵检测功能。
- **深度包检测**：配合 Everoute 中的**网络安全导流**功能，可支持 Web 信誉、防火墙和入侵防御功能，检测虚拟机出入站流量并保护操作系统和应用程序免受攻击。

---

## 深度安全防护功能 > 配置要求

# 配置要求

如需使用深度安全防护功能，请确保您的环境满足以下所有配置要求。

## 集群要求

- 集群服务器的 CPU 架构为 x86\_64。
- 集群中的每台主机需额外预留 800 MB 内存。

## 端口要求

为了确保深度安全防护功能的正常使用，当源端访问目标端时，目标端需要开放如下端口。下表如无特殊说明，端口的传输端协议均为 TCP。

| 源端 | 目标端 | 目标端需开放的端口 | 端口说明 |
| --- | --- | --- | --- |
| 深度安全防护系统管理平台（DSM） | 安全防护虚拟机（SVM） | 4118 | DSM 与 SVM 之间通信的端口 |
| 22 | 快速部署 |
| SVM | DSM | 4119 | SVM 与 DSM GUI 或 API 建立会话连接的通信端口 |
| 4120 | DSM 波动信号端口 |
| DSM | CloudTower | 443 | DSM 从 CloudTower 获取虚拟机信息的通信端口 |

## 客户端操作系统要求

- 满足亚信 DeepSecurity 软件对客户端操作系统的兼容要求，具体说明请参考亚信的官方文档。
- 满足 SMTX 虚拟机工具（即 SMTX VMTools）对客户端操作系统的兼容要求，具体说明请参考相应版本《SMTX 虚拟机工具发布说明》的**版本配套说明**小节。

---

## 深度安全防护功能 > 使用限制及影响

# 使用限制及影响

使用深度防护功能存在一定的使用限制，并且可能影响其他功能。

## 使用限制

- 系统服务虚拟机不支持使用深度安全防护功能。
- 当集群从之前的版本升级至本版本后，对于升级前已存在的业务虚拟机，如需使用防病毒功能，需先执行关机再重新开机。
- 关闭防病毒功能将会自动删除隔离区文件。如需保留隔离区文件，建议在功能关闭前先解除隔离。

## 对其他功能的影响

如果业务虚拟机使用了深度安全防护功能，将会有以下影响。

**对配置虚拟机参数的影响**

- 开启深度包检测功能的虚拟网卡，不支持启用虚拟网卡镜像模式。
- 开启深度包检测功能的虚拟网卡在修改虚拟机网络时，禁止选择所属虚拟分布式交换机未关联至 Everoute 网络安全导流功能的虚拟机网络。
- 开启防病毒或深度包检测功能的虚拟机，在启用虚拟机高可用后，若重建的主机不满足功能启用要求，则防病毒功能将会自动关闭、深度包检测功能将无法使用。

**对虚拟机电源操作的影响**

- 开启防病毒功能的虚拟机支持自动调度至满足功能启用要求的主机，或指定所属主机。若目标主机不满足功能启用要求，则虚拟机将无法开机。您可以关闭防病毒功能后再重新开机，或更换目标主机。
- 开启深度包检测功能的虚拟机不支持自动调度至满足功能启用要求的主机。若目标主机不满足功能启用要求，则虚拟机开机后将无法使用该功能。

**对虚拟机模板、虚拟机快照和克隆虚拟机的影响**

- 将虚拟机克隆或转化为虚拟机模板后，生成的模板中不包含防病毒和深度包检测功能的配置。
- 为虚拟机创建快照时，快照中不包含防病毒和深度包检测功能的配置。
- 将虚拟机回滚至快照状态后，不影响回滚前虚拟机已有的防病毒和深度包检测功能的配置。
- 克隆虚拟机默认关闭防病毒和深度包检测功能，您可以在克隆完成后手动开启。

**对导出虚拟机的影响**

导出的虚拟机中不包含防病毒和深度包检测功能的配置。

**对迁移虚拟机的影响**

- 开启防病毒功能的虚拟机，在进行集群内迁移后，虚拟机仍包含该功能的配置。

  - 冷迁移：若目标主机不满足功能启用要求，则迁移后虚拟机无法开机。
  - 热迁移：若目标主机不满足功能启用要求，则无法迁移。
- 开启深度包检测功能的虚拟机，在进行集群内迁移后，虚拟机仍包含该功能的配置。若目标主机不满足功能启用要求，则迁移后该功能将无法使用。
- 开启防病毒或深度包检测功能的虚拟机，在进行跨集群迁移计算资源、或迁移计算和存储资源前，将自动关闭相应功能；仅迁移存储资源时，虚拟机仍包含相应功能的配置。

**对快照、复制、备份计划的影响**

- 创建快照计划时，快照中不包含防病毒和深度包检测功能的配置。
- 创建复制或备份计划时，复制或备份的目标虚拟机中不包含防病毒和深度包检测功能的配置。

---

## 深度安全防护功能 > 使用深度安全防护

# 使用深度安全防护

使用深度安全防护功能时，需在 SMTX ELF 集群中完成相应的配置，具体配置流程如下图所示。

![](https://cdn.smartx.com/internal-docs/assets/e7bf4e9a/security_01.png)

**前提条件**

- 请提前获取 SVM 模板（OVF 文件包），包含 `.ovf` 文件和 `.vmdk` 文件。
- 为业务虚拟机配置安全防护功能前，请确保已部署深度安全防护系统管理平台（DSM），且 DSM 管理网络与 CloudTower 管理网络需保持连通。DSM 提供云主机深度安全防护系统的 Web 控制台，具体操作方式请参考亚信 DeepSecurity 软件的官方文档。
- 请确保已按照[端口要求](/smtxelf/6.3.0/elf_property_notes/elf_property_notes_48#%E7%AB%AF%E5%8F%A3%E8%A6%81%E6%B1%82)完成相关端口的开放与网络连通性检查。

**操作步骤**

1. 登录 CloudTower，进入集群的**设置**页面，为集群开启深度安全防护功能。

   具体操作请参考《SMTX ELF 管理指南》的[为集群开启深度安全防护](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_280)小节。
2. 在集群中批量部署安全防护虚拟机（SVM）。集群中的每台主机需部署一个 SVM，用于为该主机中的虚拟机提供深度安全防护。

   1. 导入 SVM 模板（OVF 文件包）。

      具体操作请参考《SMTX ELF 管理指南》的[部署安全防护虚拟机（SVM）> 导入 SVM 模板](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_281#%E5%AF%BC%E5%85%A5-svm-%E6%A8%A1%E6%9D%BF)小节。
   2. 部署 SVM。

      具体操作请参考《SMTX ELF 管理指南》的[部署安全防护虚拟机（SVM）> 创建 SVM](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_281#%E5%88%9B%E5%BB%BA-svm) 小节。
3. 如需为业务虚拟机开启深度包检测功能，请在 Everoute 中配置网络安全导流功能。如您仅需开启防病毒功能，可直接跳转至步骤 4。

   1. 进入**网络与安全**页面，部署 Everoute 服务并启用网络安全导流功能。

      具体操作请参考《Everoute 安装与升级指南》的**部署前的准备**和**安装部署 Everoute** 小节。
   2. 进入 Everoute 服务的**服务设置** > **网络安全导流**页面，添加关联集群。您需要关联计划使用深度包检测功能的集群及其虚拟分布式交换机，并在该虚拟分布式交换机已关联的每台主机的 SVM 上配置一对导流网卡。

      具体操作请参考《Everoute 网络安全导流管理指南》的**关联集群**小节。
4. 为业务虚拟机配置深度安全防护功能。

   > **说明**：
   >
   > 仅支持在虚拟机创建完成后，通过**编辑虚拟机**的方式开启防病毒或深度包检测功能。

   - **开启防病毒功能**

     1. 确认集群中已上传 4.1.0 及以上版本的 SMTX VMTools 安装包，且业务虚拟机已安装 4.1.0 及以上版本的 VMTools。

        - 如未上传或安装，请参考《SMTX 虚拟机工具用户指南》的**安装 SMTX 虚拟机工具**小节。
        - 如版本不符合要求，请参考《SMTX 虚拟机工具用户指南》的**升级 SMTX 虚拟机工具**小节。
     2. 编辑虚拟机，开启防病毒功能。支持批量开启，启用后可支持防恶意软件、资产管理及入侵检测功能。

        具体操作请参考《SMTX ELF 管理指南》的[编辑虚拟机 > 编辑基本信息](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_041)小节。
   - **开启深度包检测功能**

     编辑虚拟机，为虚拟网卡开启深度包检测功能。支持批量开启，启用后可支持 Web 信誉、防火墙、入侵检测及虚拟机补丁功能。

     具体操作请参考《SMTX ELF 管理指南》的[编辑虚拟机 > 编辑基本信息](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_041)小节。
5. 登录 DSM 控制台，管理 SVM 并为已启用深度安全防护功能的业务虚拟机配置相关安全策略。具体操作请参考亚信 DeepSecurity 软件的官方文档。

**相关操作**

- **集群扩容**

  当集群后续进行扩容时，为确保新增主机能够正常使用深度安全防护功能，请按照如下步骤操作：

  1. 完成集群扩容操作。

     具体操作请参考《SMTX ELF 运维指南》的[添加节点](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_08)小节。
  2. 进入集群的**设置** > **深度安全防护**页面，为新增主机创建 SVM。

     具体操作请参考《SMTX ELF 管理指南》的[部署安全防护虚拟机（SVM）> 创建 SVM](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_281#%E5%88%9B%E5%BB%BA-svm) 小节。
  3. 如您之前已使用网络安全导流功能，则需在网络安全导流已关联的虚拟分布式交换机上为新增主机关联对应的物理网口。已在步骤 1 中为虚拟分布式交换机完成关联网口操作时，可忽略本步骤。

     具体操作请参考《SMTX ELF 管理指南》的[编辑或删除虚拟分布式交换机 > 编辑虚拟分布式交换机](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_100#%E7%BC%96%E8%BE%91%E8%99%9A%E6%8B%9F%E5%88%86%E5%B8%83%E5%BC%8F%E4%BA%A4%E6%8D%A2%E6%9C%BA)小节。
  4. 进入 Everoute 服务的**服务设置** > **网络安全导流**页面，编辑关联集群，为新增主机配置一对导流网卡。

     具体操作请参考《Everoute 网络安全导流管理指南》的**编辑或解除关联集群**小节。
- **SVM 升级**

  当您需要升级 SVM 时，请直接在 DSM 中进行操作，CloudTower 无需进行任何额外配置。

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
