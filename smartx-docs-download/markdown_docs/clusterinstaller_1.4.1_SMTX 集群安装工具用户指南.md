---
title: "clusterinstaller/1.4.1/SMTX 集群安装工具用户指南"
source_url: "https://internal-docs.smartx.com/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_preface_generic"
sections: 98
---

# clusterinstaller/1.4.1/SMTX 集群安装工具用户指南
## 关于本文档

# 关于本文档

本文档介绍了如何使用 SMTX 集群安装工具（ Cluster Installer ）进行自动化安装部署、扩容 SMTX OS（VMware ESXi）集群，以及在物理服务器上安装 SMTX OS、SMTX ELF 和 SMTX ZBS 的操作。

---

## 文档更新信息

# 文档更新信息

**2025-12-11：配合 SMTX 集群安装工具 1.4.1 正式发布**

---

## SMTX 集群安装工具简介

# SMTX 集群安装工具简介

SMTX 集群安装工具（ 以下简称 “Cluster Installer” ）是一款可以一站式安装部署、扩容 SMTX OS（VMware ESXi）集群，以及在物理服务器上安装 SMTX OS、SMTX ELF 和 SMTX ZBS 的自动化工具，可有效降低安装部署的操作难度和出错概率，减少所需的人力投入。

---

## 版本配套说明

# 版本配套说明

## 配套的软件版本

使用 Cluster Installer 可以安装部署、扩容 SMTX OS（VMware ESXi）集群，以及在物理服务器上安装 SMTX OS 软件、SMTX ELF 软件、SMTX ZBS 软件，但目标软件版本须符合以下配套要求：

| 软件 | 目标版本要求 | 备注 |
| --- | --- | --- |
| ESXi | - ESXi 6.5 P06 及后续版本 - ESXi 6.7 P03 及后续版本 - ESXi 7.0b, ESXi 7.0 U1, ESXi 7.0 U2, ESXi 7.0 U3f, ESXi 7.0 U3g - ESXi 8.0 U1, ESXi 8.0 U2, ESXi 8.0 U3 | 如果目标 ESXi 软件版本是 Patch 版本，则需要先使用 Cluster Installer 安装 Patch 版本的上一个 ISO 版本的 ESXi 软件，再登录 Broadcom 文档官网，参考要安装的 ESXi 软件版本对应的 《VMware ESXi 升级》 手册，手动升级 ESXi 版本至目标版本。 |
| SMTX OS | - 5.0.2～5.0.7 - 5.1.0～5.1.5 - 6.0.0 - 6.1.1 - 6.2.0 | - |
| SMTX ELF | - 6.1.1 - 6.2.0 | - |
| SMTX ZBS | 5.1.0～5.6.2 | - |
| CloudTower | - 3.4.3～3.4.5 - 4.1.0～4.1.1 - 4.2.2 - 4.3.0 - 4.4.0、4.4.1、4.4.3 - 4.5.0 - 4.6.2 - 4.7.1 | 仅当需要使用 Cluster Installer 安装 CloudTower 时才需满足此版本要求。Cluster Installer 仅支持在部署 SMTX OS（VMware ESXi）集群时安装 CloudTower，并且仅支持使用 CentOS 操作系统的 CloudTower 安装文件（Intel x86\_64 架构，ISO 映像文件）进行安装。 |

## 配套的服务器

已验证配套的服务器型号请见下表。

对于未进行内部验证，但在 [SMTX OS 硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)（也适用于 SMTX ELF）和 [SMTX ZBS 硬件兼容性查询工具](https://www.smartx.com/smtxzbs-compatibility/)上可以查询到的服务器型号，请先确认服务器型号对应的 BMC 是否在白名单上（BMC 白名单：Dell iDRAC、HPE iLO5、Huawei iBMC、Inspur BMC、Lenovo XClarity、Suma BMC）：

- 如果在白名单上，也可以尝试使用 Cluster Installer，操作过程中如遇到硬件兼容性问题，请联系 SmartX 售后工程师协助处理。
- 如果不在白名单上，不建议使用 Cluster Installer 在物理服务器上安装 ESXi、SMTX OS、SMTX ELF 或 SMTX ZBS，但可以使用 Cluster Installer 完成 SMTX OS（VMware ESXi）集群的集群部署或集群扩容操作。

### Intel x86\_64 架构

| 厂商 | 服务器型号 | 备注 |
| --- | --- | --- |
| Dell | PowerEdge R740xd（Halo 7100） | 为保证能够成功在物理服务器上安装 ESXi、SMTX OS、SMTX ELF 或 SMTX ZBS，服务器需确保已安装 iDRAC Enterprise 或 Datacenter 许可证。 |
| PowerEdge C6420（Halo 8100） |
| PowerEdge R750（Halo 7200） |
| 联想 | ThinkSystem SR650（Halo 7100） | - |
| SuperMicro | SuperServer 2028TR-HTR（Halo 400） | 仅支持完成 SMTX OS（VMware ESXi）集群的集群部署或集群扩容操作，不支持在物理服务器上安装 ESXi、SMTX OS、SMTX ELF 或 SMTX ZBS。 |
| HPE | HPE ProLiant DL380 Gen10 | 为保证能够成功在物理服务器上安装 ESXi、SMTX OS、SMTX ELF 或 SMTX ZBS，服务器需确保已安装 iLO Advanced 许可证。 |
| 浪潮 | Inspur NF5280M6（Halo 7200） | - |
| 超聚变 | FusionServer 2288H V6 | 在物理服务器上安装 ESXi、SMTX OS、SMTX ELF 或 SMTX ZBS 时，仅支持使用 UEFI 模式进行安装。 |

### Hygon x86\_64 架构

| 厂商 | 服务器型号 | 备注 |
| --- | --- | --- |
| 中科可控 | Suma H620-G30 | 仅支持在物理服务器上安装 SMTX OS、SMTX ELF 或 SMTX ZBS。 |
| Suma R6230HA |
| Suma R6240H0 |

> **注意**：
>
> - Suma H620-G30/R6230HA：BMC 固件版本不能低于 3.30，若低于 3.30 请联系硬件厂商进行 BMC 固件升级或采用手动安装的方式。
> - Suma R6240H0：该服务器 BIOS 固件存在已知问题，需要参照《SMTX 集群安装工具用户指南》的[检查服务器的 BMC 和 BIOS 设置](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_16)章节进行相应配置。

### 鲲鹏 AArch64 架构

| 厂商 | 服务器型号 | 备注 |
| --- | --- | --- |
| 神州数码 | KunTai R722 | 仅支持在物理服务器上安装 SMTX OS、SMTX ELF 或 SMTX ZBS。 |
| 华鲲振宇 | HuaKun TG225 A1/B1 |
| KunLun | KunLun 2280-VF |

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台）

# 安装部署 SMTX OS 集群（VMware ESXi 平台）

搭配 VMware ESXi 虚拟化平台部署 SMTX OS 集群时，您可以使用 Cluster Installer 完成 ESXi 安装和集群部署，如果安装部署现场环境或需求受限，您也可以选择仅使用 Cluster Installer 安装 ESXi 或者部署集群。下文将详细介绍使用 Cluster Installer 安装部署 SMTX OS（VMware ESXi) 集群的方式、要求、操作流程和操作步骤。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 安装部署 SMTX OS 集群的方式

# 安装部署 SMTX OS 集群的方式

使用 Cluster Installer 完整安装部署 SMTX OS 集群时，有以下两种方式。

- 一次性完成 ESXi 安装和集群部署：仅需要手动输入一次安装部署 SMTX OS 集群过程所需信息，Cluster Installer 即可自动化执行安装部署的全部流程，执行期间无需操作人值守，但该方式对网络要求较高。
- 先安装 ESXi，再部署集群：需要先手动输入安装 ESXi 所需信息，等待 Cluster Installer 执行 ESXi 软件安装，再输入部署集群所需信息，Cluster Installer 自动完成集群部署。该方式对网络要求较低。

如果现场安装部署环境仅能满足安装 ESXi 软件的网络要求，或者 Cluster Installer 不支持目标 SMTX OS 集群版本，也可以仅使用 Cluster Installer 安装 ESXi，但后续还需要参考目标 SMTX OS 集群版本的《SMTX OS 集群安装部署指南》，从“设置 ESXi”章节开始继续手动完成集群的部署。

如果现场安装部署环境仅能满足部署集群的网络要求，也可以仅使用 Cluster Installer 部署集群，但在此之前需要参考目标 SMTX OS 版本的《SMTX OS 集群安装部署指南》的“在每个节点上安装 ESXi 软件”和“设置 ESXi”章节，手动安装 ESXi 软件并为 ESXi 管理网络配置 IP，再使用 Cluster Installer 完成集群的部署。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 安装部署 SMTX OS 集群的要求

# 安装部署 SMTX OS 集群的要求

使用 Cluster Installer 进行 SMTX OS 集群的安装部署之前，需要先确保现场安装部署环境满足构建 SMTX OS 集群的基本要求，再确保其满足使用 Cluster Installer 的要求。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 安装部署 SMTX OS 集群的要求 > 构建 SMTX OS 集群的基本要求

# 构建 SMTX OS 集群的基本要求

请参考目标 SMTX OS 集群版本的《SMTX OS 集群安装部署指南》确认现场安装部署环境满足构建 SMTX OS 集群的要求，并规划 SMTX OS 网络。

> **注意**：
>
> 当需要为 U.2 NVMe 直通硬盘启用热插拔功能时，如果使用 Cluster Installer 进行集群部署，则无需提前准备 vmpctl 文件，只要满足以下要求，集群部署完成后该功能即可默认开启。
>
> - 集群不启用 RDMA 功能，因为 NVMe 直通硬盘热插拔功能与 RDMA 功能无法同时启用。
> - 目标 ESXi 软件是 8.0 U1 及以上版本。
> - 服务器的引导模式已设置为 “UEFI”。
> - 服务器支持 VMDirectPath I/O 功能，可在 [Broadcom 官网](https://compatibilityguide.broadcom.com/)查看当前服务器型号是否支持该功能。
> - 服务器平台和设备满足 VMDirectPath I/O 功能的要求，可在 [Broadcom 官网](https://knowledge.broadcom.com/external/article?legacyId=2142307)查看具体要求。
>
> 另外，部署过程中您也无需手动设置 ESXi 主机和 SCVM 的参数，在后续运维集群阶段热插拔 NVMe 直通硬盘时也无需再提前准备 vmpctl 文件，可直接在 SCVM 中执行相关命令。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 安装部署 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求

# 使用 Cluster Installer 的要求

请确认现场安装部署环境满足以下对使用 Cluster Installer 的要求。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 安装部署 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求 > Cluster Installer 所在虚拟机的运行环境要求

# Cluster Installer 所在虚拟机的运行环境要求

Cluster Installer 部署在虚拟机中，该虚拟机需运行在已安装虚拟机管理程序的服务器、个人电脑或集群主机中，当前仅支持以下类型。

- ESXi 主机；

  > **注意**：
  >
  > 如果仅使用 Cluster Installer 部署集群，可以选择使用待部署集群中的任意一个 ESXi 主机。否则需要使用不属于此次待部署集群的 ESXi 主机。
- 已安装如下虚拟机管理软件的个人电脑：

  - VMware Workstation：14 Pro 及以上版本；
  - Oracle VirtualBox：6.0 及以上版本。
  > **注意**：
  >
  > 为确保软件能成功安装，建议在安装前先在本地计算机的 BIOS/固件设置中启用 Intel VT-x，然后重启计算机。
- 5.0.5 及以上版本的 SMTX OS（ELF）集群中的主机。
- SMTX ELF 集群中的主机（已配置关联存储）。

此外，以上服务器、个人电脑和集群主机还需满足以下要求：

- CPU 架构为 x86\_64；
- 有足够的资源空间：
  - 至少 2 个 CPU；
  - 至少 64 GB 存储空间；
  - 至少 2 GB 内存，但对于 SMTX OS（ELF）集群中的主机，则需预留至少 3 GiB 内存。
- 对于个人电脑，其使用的物理网卡速率必须大于或等于 1 Gbps。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 安装部署 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求 > 软件版本要求

# 软件版本要求

不同的安装部署方式对安装部署 SMTX OS 集群的目标软件版本的要求不同。

- 使用 Cluster Installer 一次性完成 ESXi 安装和集群部署：需要满足[配套的软件版本](/clusterinstaller/1.4.1/installer_release_notes/cluster_installer_release_notes_02#%E9%85%8D%E5%A5%97%E7%9A%84%E8%BD%AF%E4%BB%B6%E7%89%88%E6%9C%AC)要求，并且目标 ESXi 软件版本必须是 ISO 版本。
- 使用 Cluster Installer 先安装 ESXi，再部署集群：需要满足[配套的软件版本](/clusterinstaller/1.4.1/installer_release_notes/cluster_installer_release_notes_02#%E9%85%8D%E5%A5%97%E7%9A%84%E8%BD%AF%E4%BB%B6%E7%89%88%E6%9C%AC)要求。
- 仅使用 Cluster Installer 安装 ESXi：仅需要满足[配套的软件版本](/clusterinstaller/1.4.1/installer_release_notes/cluster_installer_release_notes_02#%E9%85%8D%E5%A5%97%E7%9A%84%E8%BD%AF%E4%BB%B6%E7%89%88%E6%9C%AC)中对 ESXi 软件版本的要求。
- 仅使用 Cluster Installer 部署集群：需要满足[配套的软件版本](/clusterinstaller/1.4.1/installer_release_notes/cluster_installer_release_notes_02#%E9%85%8D%E5%A5%97%E7%9A%84%E8%BD%AF%E4%BB%B6%E7%89%88%E6%9C%AC)要求。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 安装部署 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求 > 待部署 SMTX OS 集群的服务器要求

# 待部署 SMTX OS 集群的服务器要求

待安装部署 SMTX OS 集群的服务器需要以下要求：

- 服务器的型号满足[配套的服务器](/clusterinstaller/1.4.1/installer_release_notes/cluster_installer_release_notes_02#%E9%85%8D%E5%A5%97%E7%9A%84%E6%9C%8D%E5%8A%A1%E5%99%A8)要求。
- 如果需要使用 Cluster Installer 一次性完成 ESXi 安装和集群部署，且需要启用 RDMA，则为服务器配置的 RDMA 网卡不能为 ConnectX-4 Lx 系列的 Mellanox 网卡。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 安装部署 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求 > 浏览器版本要求

# 浏览器版本要求

借助 Cluster Installer 安装部署 SMTX OS 集群过程中需要使用 Web 浏览器，为保证兼容性，建议使用 Chrome 80 或 Firefox 78 及以上版本的浏览器，并启用 Cookie 和 JavaScript。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 安装部署 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求 > 网络连通要求

# 网络连通要求

借助 Cluster Installer 安装部署 SMTX OS 集群时，需要确保 Cluster Installer 的网络环境和 IP 均满足网络连通要求，但不同的安装部署方式对网络连通的要求不同，请参考以下说明规划 Cluster Installer 的网络和 IP：

- 使用 Cluster Installer 一次性完成 ESXi 安装和集群部署：需满足下表中对 **ESXi 安装和集群部署**功能的要求。
- 使用 Cluster Installer 先安装 ESXi，再部署集群：需分别满足下表中对 **ESXi 安装**、**集群部署**功能的要求。
- 仅使用 Cluster Installer 安装 ESXi：需满足下表中对 **ESXi 安装**功能的要求。
- 仅使用 Cluster Installer 部署集群：需满足下表中对**集群部署**功能的要求。

| 功能 | 对 Cluster Installer 网络环境的要求 | 对 Cluster Installer IP 的要求 |
| --- | --- | --- |
| ESXi 安装和集群部署 | - 若在 ESXi 主机、SMTX OS 集群或 SMTX ELF 集群中安装 Cluster Installer，则主机或集群中需要有可同时连通待部署集群的 ESXi 管理网络和服务器 IPMI 网络的虚拟机网络，且虚拟机网络的带宽必须大于或等于 1 Gbps。 - 若在个人电脑中安装 Cluster Installer，则个人电脑需能同时与待部署集群的 ESXi 管理网络和服务器 IPMI 网络连通。 | 须同时满足 **ESXi 安装、集群部署**的要求。 |
| ESXi 安装 | - 若在 ESXi 主机、SMTX OS 集群或 SMTX ELF 集群中安装 Cluster Installer，则主机或集群中需要有可连通待部署集群的服务器 IPMI 网络的虚拟机网络，且虚拟机网络的带宽必须大于或等于 1 Gbps。 - 若在个人电脑中安装 Cluster Installer，则个人电脑需要与待部署集群的服务器 IPMI 网络连通。 | Cluster Installer IP 与待部署集群的 IPMI IP 可以互相连通。 |
| 集群部署 | - 若在 ESXi 主机、SMTX OS 集群或 SMTX ELF 集群中安装 Cluster Installer，则主机或集群中需要有可连通待部署集群的 ESXi 管理网络的虚拟机网络，且虚拟机网络的带宽必须大于或等于 1 Gbps。 - 若在个人电脑中安装 Cluster Installer，则个人电脑需要与待部署集群的 ESXi 管理网络连通。 | - Cluster Installer IP 与待部署集群的 ESXi 管理 IP 可以互相连通。 - Cluster Installer IP 可以连通待部署集群的 SCVM 管理 IP。 - 如果需要使用 Cluster Installer 关联 vCenter Server，则要求 Cluster Installer IP 可以连通 vCenter Server IP。 - 如果需要使用 Cluster Installer 关联 CloudTower，则要求 Cluster Installer IP 可以连通 CloudTower IP。 |

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 安装部署 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求 > 防火墙端口开放要求

# 防火墙端口开放要求

如果 Cluster Installer 与待部署集群、CloudTower、vCenter Server 等之间通信的网络存在防火墙，则目标端须开放相应的端口。不同的安装部署方式对端口开放有不同的要求，请参考以下说明检查防火墙端口：

- 使用 Cluster Installer 一次性完成 ESXi 安装和集群部署，或者先安装 ESXi 再部署集群：需同时满足下表中对 **ESXi 安装**、**集群部署**功能的要求。
- 仅使用 Cluster Installer 安装 ESXi：需满足下表中对 **ESXi 安装**功能的要求。
- 仅使用 Cluster Installer 部署集群：需满足下表中对**集群部署**功能的要求。

| 功能 | 源端 | 目标端 | 目标端需开放端口 | 用途 |
| --- | --- | --- | --- | --- |
| ESXi 安装 | 浏览器客户端 IP | Cluster Installer IP | TCP 80 | 用于浏览器 Web 访问 Cluster Installer |
| Cluster Installer IP | 服务器 IPMI IP | TCP 443 | BMC Redfish/HTTPS API 端口 |
| UDP 623 | IPMI 协议端口，用于获取服务器 FRU 信息、SOL 串口输出 |
| TCP 22 | 如果服务器的 BMC 为 Huawei iBMC 或 Dell iDRAC 且 iDRAC 版本低于 4.0，需要通过 SSH 登录到 BMC 挂载 ISO 文件 |
| 服务器 IPMI IP | Cluster Installer IP | Cluster Installer 虚拟机 NFS Server 端口 \* | NFS 访问端口，BMC 需要通过 NFS 协议挂载 Cluster Installer 虚拟机里的 ISO 文件 |
| TCP 80 | 如果服务器的 BMC 为 HPE iLO5，需开放此端口 |
| 集群部署 | 浏览器客户端 IP | Cluster Installer IP | TCP 80 | 用于浏览器 Web 访问 Cluster Installer |
| Cluster Installer IP | ESXi 管理 IP | TCP 443 | ESXi HTTPS API 访问端口 |
| TCP 22 | 用于 SSH 登录 ESXi 主机 |
| Cluster Installer IP | SCVM 管理 IP | TCP 443 | SMTX OS 集群 API 访问端口 |
| TCP 80 | SMTX OS 集群部署 API 访问端口 |
| TCP 22 | 用于 SSH 登录 SCVM 主机 |
| ESXi 管理 IP | Cluster Installer IP | Cluster Installer 虚拟机 NFS Server 端口 \* | ESXi 主机通过挂载 Cluster Installer 虚拟机 NFS 数据存储的方式访问 ISO、ESXi 插件等文件 |
| Cluster Installer IP | vCenter Server IP | TCP 443 | vCenter API 访问端口，当关联 vCenter 时需要开放此端口 |
| Cluster Installer IP | CloudTower IP | TCP 22 | SSH 登录 CloudTower 虚拟机，当选择部署新 CloudTower 时需要开放此端口 |
| TCP 443 | CloudTower API 访问端口 |
| TCP 80 | CloudTower API 访问端口 |

> **说明**：
>
> Cluster Installer 虚拟机 NFS Server 端口（表中有星号 \* 标记的端口）除了 `2049` 和 `111` 两个固定端口外，其他端口均为随机端口。在创建完 Cluster Installer 虚拟机并配置完 IP 后，您才能查看 NFS Server 使用了哪些随机端口，同时您也可以选择自定义除 111 端口外的其他 NFS Server 端口，建议参考上述要求提前规划。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 安装部署 SMTX OS 集群的流程

# 安装部署 SMTX OS 集群的流程

使用 Cluster Installer 安装部署 SMTX OS 集群的 4 种方式的操作流程如下。

## 使用 Cluster Installer 一次性完成 ESXi 安装和集群部署

1. 确认现场安装部署环境满足使用该方式的要求，参见[安装部署 SMTX OS 集群的要求](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_05)。
2. 创建 Cluster Installer 虚拟机，参见[创建 Cluster Installer 虚拟机](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_13)。
3. 配置 Cluster Installer IP，参见[配置 Cluster Installer IP](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_14)。
4. 开放 NFS Server 端口，参见[开放 NFS Server 端口](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_15)。
5. 检查服务器的 BMC 和 BIOS 设置，参见[检查服务器的 BMC 和 BIOS 设置](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_16)。
6. 若需要启用 RDMA，建议先参考《SMTX OS 集群安装部署指南》的“在交换机端配置流量控制”小节手动在物理交换机端配置的流量控制。
7. 使用 Cluster Installer 安装 ESXi 和部署集群，参见[安装 ESXi 和部署集群](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_17)。
8. 若已启用 RDMA，请参考《SMTX OS 集群安装部署指南》的“验证流量控制的配置结果”小节，在 SCVM 中验证流量控制配置是否正确。

## 使用 Cluster Installer 先安装 ESXi，再部署集群

1. 确认现场安装部署环境满足使用该方式的要求，参见[安装部署 SMTX OS 集群的要求](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_05)。
2. 创建 Cluster Installer 虚拟机，参见[创建 Cluster Installer 虚拟机](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_13)。
3. 配置 Cluster Installer IP，参见[配置 Cluster Installer IP](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_14)。
4. 开放 NFS Server 端口，参见[开放 NFS Server 端口](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_15)。
5. 检查服务器的 BMC 和 BIOS 设置，参见[检查服务器的 BMC 和 BIOS 设置](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_16)。
6. 若需要启用 RDMA，建议先参考《SMTX OS 集群安装部署指南》的“在交换机端配置流量控制”小节手动在物理交换机端配置的流量控制。
7. 使用 Cluster Installer 安装 ESXi，参见[安装 ESXi](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_18)。
8. 若目标 ESXi 软件版本是 Patch 版本，请登录 Broadcom 文档官网，参考对应 ESXi 软件版本的 《VMware ESXi 升级》手册，手动升级 ESXi 版本至目标版本。
9. 使用 Cluster Installer 部署集群，参见[部署集群](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_19)。
10. 若已启用 RDMA，请参考《SMTX OS 集群安装部署指南》的“验证流量控制的配置结果”小节，在 SCVM 中验证流量控制配置是否正确。

## 仅使用 Cluster Installer 部署集群

1. 确认现场安装部署环境满足使用该方式的要求，参见[安装部署 SMTX OS 集群的要求](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_05)。
2. 参考目标 SMTX OS 版本的《SMTX OS 集群安装部署指南》的“在每个节点上安装 ESXi 软件”和“设置 ESXi”章节，手动安装 ESXi 软件并为 ESXi 管理网络配置 IP。
3. 创建 Cluster Installer 虚拟机，参见[创建 Cluster Installer 虚拟机](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_13)。
4. 配置 Cluster Installer IP，参见[配置 Cluster Installer IP](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_14)。
5. 开放 NFS Server 端口，参见[开放 NFS Server 端口](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_15)。
6. 若需要启用 RDMA，建议先参考《SMTX OS 集群安装部署指南》的“在交换机端配置流量控制”小节手动在物理交换机端配置的流量控制。
7. 使用 Cluster Installer 部署集群，参见[部署集群](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_19)。
8. 若已启用 RDMA，请参考《SMTX OS 集群安装部署指南》的“验证流量控制的配置结果”小节，在 SCVM 中验证流量控制配置是否正确。

## 仅使用 Cluster Installer 安装 ESXi

1. 确认现场安装部署环境满足使用该方式的要求，参见[安装部署 SMTX OS 集群的要求](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_05)。
2. 创建 Cluster Installer 虚拟机，参见[创建 Cluster Installer 虚拟机](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_13)。
3. 配置 Cluster Installer IP，参见[配置 Cluster Installer IP](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_14)。
4. 开放 NFS Server 端口，参见[开放 NFS Server 端口](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_15)。
5. 检查服务器的 BMC 和 BIOS 设置，参见[检查服务器的 BMC 和 BIOS 设置](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_16)。
6. 使用 Cluster Installer 安装 ESXi，参见[安装 ESXi](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_18)。
7. 若目标 ESXi 软件版本是 Patch 版本，请登录 Broadcom 文档官网，参考对应 ESXi 软件版本的 《VMware ESXi 升级》手册，手动升级 ESXi 版本至目标版本。
8. 参考目标 SMTX OS 版本的《SMTX OS 集群安装部署指南》的”设置 ESXi“章节，继续手动完成集群的部署。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 创建 Cluster Installer 虚拟机

# 创建 Cluster Installer 虚拟机

您可以根据当前环境选择在 ESXi 主机、SMTX OS（ELF）集群的主机、或者个人电脑中创建 Cluster Installer 虚拟机。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 创建 Cluster Installer 虚拟机 > 在 ESXi 主机中创建

# 在 ESXi 主机中创建

在 ESXi 主机中创建 Cluster Installer 虚拟机时，可以选择直接登录 ESXi 主机进行创建或者在 vCenter Server 的 ESXi 主机中创建。

**注意事项**

Cluster Installer 虚拟机的名称不能包含除下划线 `_`、减号 `-`、点 `.` 以外的特殊字符，否则会导致安装程序出错。

## 直接登录 ESXi 主机进行创建

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 登录 ESXi 主机的 Web 管理页面，打开**创建/注册虚拟机**，选择**从 OVF 或 OVA 文件部署虚拟机**，单击**下一步**。
3. 输入虚拟机的名称，打开**单击以选择文件或拖放**，选择已下载至本地计算机上的 OVA 文件，单击**下一步**。
4. 为虚拟机的配置文件及其虚拟磁盘选择数据存储，单击**下一步**。
5. 在部署选项设置中，将网络映射 nic0 设置为符合网络连通要求的虚拟机网络，然后依次单击**下一步**完成配置。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_33.png)

## 在 vCenter Server 中的 ESXi 主机中创建

**注意事项**

若 vCenter 集群需要开启 EVC 特性，请先开启 EVC 特性，再安装 Cluster Installer 虚拟机。

**操作步骤**

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 登录 vCenter Server 的 Web 管理界面，定位到用于部署 Cluster Installer 虚拟机的 ESXi 主机，右键单击该主机，并选择**部署 OVF 模板**。
3. 选择**本地文件**，单击**上传文件**，上传已下载至本地计算机上的 OVA 文件。
4. 依次输入虚拟机名称、选择虚拟机安装位置、选择计算机资源、选择存储。
5. 在选择网络配置中，将网络映射 nic0 设置为符合网络连通要求的虚拟机网络，并完成后续配置。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_11.png)

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 创建 Cluster Installer 虚拟机 > 在 SMTX OS（ELF）集群或 SMTX ELF 集群的主机中创建

# 在 SMTX OS（ELF）集群或 SMTX ELF 集群的主机中创建

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 重命名该 OVA 文件，将文件名后缀 `.ova` 修改为 `.tar`，并解压该文件。
3. 登录 CloudTower，单击**创建** > **导入虚拟机**。
4. 在**导入虚拟机**界面中，选择安装 Cluster Installer 的集群和主机，并将已解压的对应文件上传至在**模板信息**区。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_67.png)
5. 在**计算资源**配置界面，将内存分配设置为 **3 GiB**。
6. 在**磁盘**配置界面，将总线类型设置为 **VIRTIO**，选择其他类型会导致虚拟机无法正常启动。
7. 在**虚拟网卡**界面，选择符合网络连通要求的虚拟机网络。
8. 在**其他**配置页面，选择**创建完成后自动开机**，单击**确定**。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 创建 Cluster Installer 虚拟机 > 在个人电脑中创建

# 在个人电脑中创建

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 根据个人电脑中所安装的虚拟机管理软件类型参考对应步骤创建 Cluster Installer 虚拟机。
   - **在 VMware Workstation 中创建**
     1. 在 VMware Workstation 单击**导入虚拟机**，导入已下载的 OVA 模板文件，输入新虚拟机名称以及 OVA 文件所在的存储路径。请确保存储路径所在分区的剩余可用空间不小于 64 GB。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_04.png)
     2. 在**编辑**菜单中单击**虚拟网络编辑器**，选择**更改设置**，选择 VMnet0 的桥接模式，在**已桥接至**下拉列表中选择本地计算机所使用的物理网卡。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_07.png)
     3. 打开 Cluster Installer 的**虚拟机设置**，确认网络连接模式为**桥接模式**。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_08.png)
   - **在 Oracle VirtualBox 中创建**
     1. 在 VirtualBox 中单击**管理**菜单，选择**导入虚拟机电脑**，选择 OVA 文件所在的存储路径，并确认**默认虚拟机电脑位置**所在分区的剩余可用空间不小于 64 GB。

        导入时将 MAC 地址设定设置为**为所有网卡重新生成 MAC 地址**。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_09.png)
     2. 导入虚拟机后，打开虚拟机设置页面，确保网卡 1 的连接方式为**桥接网卡**。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_10.png)

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 配置 Cluster Installer IP

# 配置 Cluster Installer IP

创建 Cluster Installer 虚拟机后，需要为虚拟机配置 IP 地址。下文以 VMware Workstation 为例介绍配置步骤。

**操作步骤**

1. 打开 VMware Workstation，在**我的计算机**中，选择已创建的 Cluster Installer 虚拟机单击**开启此虚拟机**。
2. 配置虚拟机的 IP 地址。

   - 如果虚拟机桥接网络内有 DHCP 服务器，Cluster Installer 会通过 DHCP 服务器自动获取 IP 地址，并显示在虚拟机控制台。

     ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_12.png)
   - 如果虚拟机桥接网络内没有 DHCP 服务器，则请执行以下操作。

     1. 打开 `/etc/sysconfig/network-scripts/ifcfg-eth0` 文件，设置静态 IP。
     2. 重启 Cluster Installer 虚拟机。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_13.png)
3. 执行 `prepare.sh` 命令检查虚拟机内的服务是否正常运行。

   当时输出结果显示 `Failed: 0` 和 `Skipped: 0` 时，表示服务正常运行。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_14.png)

   - 如果服务正常运行，则可以正常使用 Cluster Installer 。
   - 如果服务未正常运行，排查完原因后，若需要变更 Cluster Installer 所在的网络和修改 IP 地址，请从上一步开始重新执行操作。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 开放 NFS Server 端口

# 开放 NFS Server 端口

1. 登录 Cluster Installer 虚拟机，执行以下命令查看 NFS Server 当前使用的所有端口信息。

   ```
   rpcinfo -p
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_80.png)
2. （可选）如果需要自定义 NFS Server 端口，请执行以下步骤。

   1. 执行以下命令，然后根据提示输入实际规划的新端口。如果不需要修改某端口，可以直接按 Enter 键跳过该端口的设置。

      ```
      /root/deploy/tools/update_nfs_ports.sh
      ```

      ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_82.png)
   2. 执行以下命令，确认端口已修改成功。

      ```
      rpcinfo -p
      ```

      ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_83.png)
3. 执行以下命令，查看需要开放的 NFS Server 端口。

   ```
   rpcinfo -p | awk '{print $3,$4}' | sort -u
   ```
4. 参考防火墙端口开放要求，为 Cluster Installer 虚拟机开放 NFS Server 端口。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 检查服务器的 BMC 和 BIOS 设置

# 检查服务器的 BMC 和 BIOS 设置

使用 Cluster Installer 在物理服务器上安装 ESXi、SMTX OS、SMTX ELF 或 SMTX ZBS 时，需依赖服务器的 BMC（基板管理控制器）对服务器执行开机、重启、挂载 ISO、卸载 ISO、获取 Console 输出等操作，因此在安装前，需参考下文检查服务器的 BMC 和 BIOS 设置，确保已启用以下功能：

- Redfish 或 HTTPS 访问功能；
- IPMI Over LAN 功能；
- SOL（Serial Over LAN ）功能。

**注意事项**

- 如果选择 `Avago MegaRAID` 卡上的硬盘作为服务器的启动盘，安装前需要确保 RAID 卡在 BIOS 设置里的 **Boot device** 为所选的硬盘，否则会导致 ISO 安装完后由于启动设备配置错误导致系统无法正常启动。

  ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_65.png)
- 如果服务器的 CPU 架构为鲲鹏 AArch64，需要确保服务器的 BIOS 设置里的 **CPU Prefetching Configuration** 选项为 **Enabled**，否则会影响 CPU 性能。

  ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_73.png)

## Dell iDRAC

1. 打开浏览器，在地址栏输入服务器的 IPMI 管理台 IP，登录服务器的 iDRAC 管理界面。
2. 单击 **iDRAC 设置** > **连接性** > **LAN 上串行**，将**启用 LAN 上串行**状态设置为**已启用**，然后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_51.png)
3. 单击 **iDRAC 设置** > **连接性** > **网络** >**IPMI 设置**，将**启用 LAN 上的 IPMI** 状态设置为**已启用**，然后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_52.png)
4. 单击 **iDRAC 设置** > **用户** > **本地用户**，确认本地用户的 **LAN 上串行**已启用。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_53.png)
5. 单击 **iDRAC 设置** > **服务** > **Redfish**，将 Redfish 状态设置为**已启用**，然后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_54.png)

## Lenovo XClarity

1. 打开浏览器，在浏览器的地址栏输入服务器的 IPMI 管理台 IP，登录服务器的 XClarity Controller 管理界面。
2. 单击 **BMC 配置**，然后参考下图启用 **Web Over HTTPS**、**REST Over HTTPS** 和 **IPMI over LAN**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_55.png)

## HPE iLO5

1. 打开浏览器，在浏览器的地址栏输入服务器的 IPMI 管理台 IP，登录服务器的 iLO5 管理界面。
2. 单击**安全性** > **访问设置**，然后按下图设置参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_56.png)

## Inspur BMC

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录服务器的 BMC 管理界面。
2. 单击**系统设置** > **服务**，然后按下图设置 WEB、CD-Media 和 IPMI 服务的参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_77.png)
3. 单击**系统设置** > **用户精细化管理**，然后按下图检查并确认当前用户属于 Administrator 用户组，用户已启用，且 IPMI 权限为 `administrator`。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_78.png)

## Huawei iBMC

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录服务器的 iBMC 管理界面。
2. 单击**服务管理** > **端口服务**，然后按下图设置参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_57.png)
3. 单击**用户&安全** > **本地用户**，然后按下图设置登录接口。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_58.png)
4. 单击**系统管理** > **BIOS 配置**，开启**支持 IPMI 设置启动模式**，然后将**启动模式**选项设置为**统一可扩展固件接口（UEFI）**，完成后单击**保存**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_79.png)

## Suma BMC

> **注意**：
>
> - 对于 **Suma R6240H0** 型号服务器，由于其固件存在已知问题，需要在 BIOS 中禁用 `Serial Port`，否则会导致无法正常使用 SOL 功能。禁用 `Serial Port` 方法如下：
>
>   重启服务器，进入 `BIOS Setup Utility`，将 `Advanced`>`AST2500 Super IO Configuration`>`Serial Port Configuration`>`Serial Port` 参数设置为 **Disabled**。
>
>   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_62.png)
> - 对于 **Suma H620-G30/R6230HA** 型号服务器，其 BMC 固件版本不能低于 **3.30** ，若低于 **3.30** 请联系硬件厂商进行 BMC 固件升级。
>
>   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_59.png)

1. 单击 **BMC 设置** > **服务**，然后按照下图设置 web 和 ipmi 服务的参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_60.png)
2. 单击**远程设置** > **BIOS 设置** > **管理配置**，然后按照下图设置所有参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_61.png)
3. 单击 **BMC 配置** > **用户/用户组**，然后为当前用户开启 **VMedia 访问**权限。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 安装 ESXi 和部署集群

# 安装 ESXi 和部署集群

## 第 1 步：选择执行任务

1. 打开浏览器，在地址栏输入 Cluster Installer 的 IP 地址，输入用户名和密码，登录 Cluster Installer 的 Web 界面。
2. 在集群类型选项中，选择 **SMTX OS（VMware ESXi 平台）**。
3. 在**开始新项目**界面中，输入本次项目的名称。项目名称可用于区分执行的任务内容，建议使用英文字母和数字命名。
4. 在功能选项中，选择 **ESXi 安装和集群部署**。
5. 单击**开始配置**。

## 第 2 步：获取主机信息

**注意事项**

从本步骤开始需要手动填写项目的配置信息，在填写信息的过程中请勿关闭浏览器，否则项目的配置信息将不会保留。

**操作步骤**

1. 在**集群规模**界面，输入待部署集群的主机数量、以及所有主机的 IPMI 管理台的 IP 地址、管理员用户名和密码。
2. 单击**获取主机信息**，然后根据获取结果确认主机信息是否获取成功，以及主机是否满足安装部署要求。
   - 如果主机信息全部获取成功且主机满足安装部署要求，界面将提示“已获取到主机 CPU 架构等信息”，主机列表中将展示每个主机的 BMC、CPU 架构和服务器型号。
   - 如果主机的 BMC 或 CPU 架构信息未获取成功，可单击下拉框，根据主机的 FRU 信息手动选择当前主机的 BMC 或 CPU 架构。
   - 如果查找不到主机或者主机不满足安装部署要求，界面将有错误提示，请根据提示解决问题后再单击**重新获取主机信息**。
3. 确认主机满足安装部署要求后，单击**下一步**。

## 第 3 步：上传安装文件

1. 在**安装文件**界面，单击**上传到 Cluster Installer**，进入安装文件上传界面。
2. 双击打开 Cluster Installer 中内置的 `md5sum.txt` 文件，以 `md5sum + 空格 + 文件名` 的格式手动添加目标 ESXi 版本的 ISO 的 MD5 信息。若有其他未添加 MD5 信息的安装文件，请以相同的格式手动输入该安装文件的 MD5 信息。

   > **注意**：
   >
   > 请勿更改 MD5 汇总表的文件名及文件格式，否则将导致校验 MD5 步骤出错。
3. 单击安装文件上传界面右上角的上传按钮，在本地计算机中选择安装部署所需的安装文件进行上传。
4. 返回**安装文件**界面，单击**刷新**，然后根据需要选择安装文件。

   在 **CloudTower** 选项处，您可根据实际规划进行选择：

   - **部署全新 CloudTower**：若需要使用 CloudTower 管理集群，但当前环境中未有适配目标集群的 CloudTower，请选择该项，然后选择目标版本的 CloudTower 安装文件。
   - **关联已有 CloudTower**：若需要使用 CloudTower 管理集群，并且当前环境中已有适配目标集群的 CloudTower，请选择该项。
   - **不使用 CloudTower**：若无使用 CloudTower 管理集群的需求，可选择该项。
5. 单击**收集硬件配置**，然后根据收集结果确认主机的硬件配置是否满足安装部署要求，以及主机配置是否支持 RDMA。收集过程中可以单击**按目录查看日志**，确认收集进度。

   如果主机的硬件配置满足安装部署要求，界面将提示“已收集到主机中物理盘、网卡等硬件配置信息”。在此基础上，如果主机配置支持 RDMA，界面还将提示“当前配置支持 RDMA 功能”。
6. （可选）如果需要启用 RDMA 功能，且确认主机配置支持 RDMA，请勾选**为存储网络启用 RDMA**，然后上传以下文件。

   - **MFT vib 软件包**：软件包名称必须以 `mft` 或 `Mellanox-MFT-Tools` 开头。
   - **NMST vib 软件包**：软件包名称必须以 `nmst` 或 `Mellanox-NATIVE-NMST` 开头。
7. 单击**下一步**。

## 第 4 步：输入集群配置信息

在**配置信息**界面，配置集群、存储、ESXi 主机、网络、NFS 存储，并可根据实际情况选择配置 CloudTower、vCenter Server。

### 配置集群

1. 设置 SMTX OS 集群的名称、管理虚拟 IP 和超级管理员 root 的密码。
2. （可选）若有域名配置需求，请填写实际规划的 DNS 服务器的 IP 地址。
3. 选择 NTP 服务器。
   - 若需要使用集群外部 NTP 服务器来同步集群内的主机时间，请选择**使用集群外部 NTP 服务器**，并填写 NTP 服务器地址。
   - 若无使用集群外部 NTP 服务器的需求，请选择**使用集群内主机作为 NTP 服务器**。

### 配置存储

1. 根据集群要采用的存储分层/不分层模式，选择**分层**或**不分层**。
2. （可选）如果 SMTX OS 集群为 6.1.1 及以上版本，请根据实际规划为集群节点选择容量规格。
3. 根据在确认 SMTX OS 集群构建要求时已规划的每块物理盘的用途，为每个主机的物理盘选择用途。

   系统将为不包含 ESXi 系统盘和 SMTX 引导盘的存储控制器开启直通模式。

### 配置 ESXi 主机

为每个主机设置 ESXi 超级管理员 root 的密码和 ESXi 主机名。其中，主机名可使 ESXi 主机在 vCenter Server 资源列表中更有辨识度。

### 配置 SCVM

1. 为每个主机设置 SCVM 名称和 SCVM 主机名。
   - SCVM 名称：SCVM 虚拟机的名称，在 vCenter Server 的虚拟机列表中可使用此名称查看 SCVM 虚拟机。
   - SCVM 主机名：SMTX OS 集群中 SCVM 所在节点的名称，在 CloudTower 或 Web 控制台中可使用此名称查看集群节点。
2. 根据主机的 IPMI IP 辨认并勾选集群的主节点。

### 配置 SCVM 密码

当 SMTX OS 集群为 6.1.1 及以上版本时，请为集群内 SCVM 统一设置 root 账户和 smartx 账户的密码。

### 配置网络

#### 配置标准虚拟交换机

请先选择管理网络和存储网络采用的网络部署模式，再参考所选部署模式对应的步骤配置标准虚拟交换机。

> **注意**：
>
> - 不同的网络部署模式下，系统均已自动完成管理网络和存储网络所需虚拟交换机的创建，若要完成安装部署，您仅需要参考以下步骤完善对虚拟交换机的配置。
> - 如有需要，您还可以关联业务网络、vMotion 网络到已创建或新创建的虚拟交换机。如果 vMotion IP 和存储网络 IP 规划在同一网段，则必须将 vMotion 网络关联至存储网络虚拟交换机 ZBS，否则会导致存储网络异常。

**选择分离式部署**

1. 配置管理网络虚拟交换机 vSwitch0。

   1. 分别为虚拟交换机、ESXi 管理网络和 SCVM 管理网络选择所需的负载均衡模式。
   2. （可选）如果已为 ESXi 管理网络或 SCVM 管理网络规划了 VLAN ID，请填写实际规划的 VLAN ID。
   3. 给每个主机选择用于管理网络的网络适配器。
      - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网络适配器。
      - 若各个主机需要选择的网络适配的名称相同，可以在选择完一个主机的网络适配器后，在选框右侧单击 **...** > **在其他主机上选择同名适配器**。
2. 配置存储网络虚拟交换机 ZBS。

   1. 分别为虚拟交换机和 SCVM 存储网络选择所需的负载均衡模式。如果在[第 3 步：上传安装文件](#%E7%AC%AC-3-%E6%AD%A5%E4%B8%8A%E4%BC%A0%E5%AE%89%E8%A3%85%E6%96%87%E4%BB%B6)中已启用 RDMA 功能，系统默认勾选**启用 RDMA**，且自动将负载均衡模式设置为**基于源虚拟端口的路由**。
   2. （可选）如果已为 SCVM 存储网络规划了 VLAN ID，请填写实际规划的 VLAN ID。如果已启用 RDMA 功能，系统默认设置 VLAN ID 为 0。
   3. 给每个主机选择用于存储网络的网络适配器。
      - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网络适配器。
      - 如果已启用 RDMA 功能，当给同一个主机分配了多个网络适配器时，需要设置备用适配器，并需要确保所选的网络适配器均来自同一张支持 RDMA 功能的网卡。
      - 若各个主机需要选择的网络适配的名称相同，可以在选择完一个主机的网络适配器后，在选框右侧单击 **...** > **在其他主机上选择同名适配器**。
   4. （可选）当所选的网络适配器速率均为 25 GbE 及以上时，如果需要提升存储网络的带宽性能，可以将物理交换机上存储网络对应物理端口的 MTU 修改为 9000，然后勾选**同时将存储网络链路 MTU 设为 9000**。
   5. （可选）如果已启用 RDMA 功能，请选择所需的流量控制方式。
      > **注意**：
      >
      > 在执行安装部署前，需确保已手动在物理交换机端配置相同方式的流量控制。

**选择融合部署**

1. 分别为虚拟交换机、ESXi 管理网络、SCVM 管理网络和 SCVM 存储网络选择所需的负载均衡模式。
2. （可选）如果已为 ESXi 管理网络、SCVM 管理网络或 SCVM 存储网络规划了 VLAN ID，请填写实际规划的 VLAN ID。
3. 给每个主机选择管理网路和存储网络共用的网络适配器。
   - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网络适配器。
   - 若各个主机需要选择的网络适配的名称相同，可以在选择完一个主机的网络适配器后，在选框右侧单击 **...** > **在其他主机上选择同名适配器**。
4. （可选）当所选的网络适配器速率均为 25 GbE 及以上时，如果需要提升存储网络的带宽性能，可以将物理交换机上存储网络对应物理端口的 MTU 修改为 9000，然后勾选**同时将存储网络链路 MTU 设为 9000**。

#### 配置网络 IP

1. 为每个主机输入实际规划的 ESXi 管理 IP、SCVM 管理 IP、ESXi 存储 IP、SCVM 存储 IP。
2. （可选）如果启用了 RDMA 功能，请为每个主机输入 VMware 接入 IP。
3. （可选）如果在虚拟交换机中关联了 vMotion 网络，还输入实际规划的 vMotion 网络 IP。
4. 输入给各个网络实际规划的子网掩码和网关。

### 配置 NFS 数据存储

选择 NFS 存储的默认副本数和置备模式。

> **说明**：
>
> NFS 数据存储名称无需手动设置，系统已自动设置为 `datastore-nfs-<cluster_vip>`，其中 `<cluster_vip>` 表示集群虚拟管理 IP。您可通过集群虚拟管理 IP 区分不同集群对应的 NFS 数据存储。

### 配置 CloudTower

仅当在[第 3 步：上传安装文件](#%E7%AC%AC-3-%E6%AD%A5%E4%B8%8A%E4%BC%A0%E5%AE%89%E8%A3%85%E6%96%87%E4%BB%B6)时选择了**部署全新 CloudTower** 或**关联已有 CloudTower** 才可以配置 CloudTower。建议在此处配置 CloudTower 以便在自动化部署完成后直接对集群进行管理，若不配置，后续也可以参考《 SMTX OS 集群安装部署指南》的“关联 CloudTower“ 小节进行手动关联。

**前提条件**

已规划 CloudTower 的 IP 地址、子网掩码和网关。确保 CloudTower IP 与 SMTX OS 集群的管理虚拟 IP 正常连通。

#### 配置全新 CloudTower

1. 选择 CloudTower 环境的配置。用户可综合考虑待管理的集群数量，主机和虚拟机规模等信息，并结合集群主机的 CPU 利用率、内存余量和存储余量，选择**低配**或**高配**。
2. 设置 CloudTower 的组织名称。
3. （可选）设置集群所属数据中心的名称。设置后系统会自动创建一个该名称的数据中心，并将集群加入此数据中心。

   如果不设置，后续您也可以在 CloudTower 手动创建数据中心再选择该集群加入。
4. 设置 CloudTower 超级管理员 root 的密码。
5. 设置 CloudTower 的 IP 地址、子网掩码和网关。

#### 关联已有 CloudTower

1. 输入已有 CloudTower 的 IP 地址、管理员用户名及密码，然后单击**连接 CloudTower**。
2. （可选）连接 CloudTower 成功后，设置集群所属数据中心，可以从下拉列表中选择已有的数据中心或创建新的数据中心。

   如果不设置，后续您也可以在 CloudTower 手动创建数据中心再将该集群加入。

### 关联 vCenter Server

**注意事项**

- 如果当前环境中已有 vCenter Server，建议参考以下步骤关联 vCenter Server，以便设置 SMTX OS 的高可用。
- 如果当前环境中没有 vCenter Server，且只能在此次待部署集群的服务器上安装该软件，则需要在自动化安装部署完成后再安装 vCenter Server，然后参考《SMTX OS 集群安装部署指南》手动关联 vCenter 和设置 SMTX OS 的高可用性。

**操作步骤**

1. 输入已有 vCenter Server 的 IP 地址和端口号、管理员用户名及管理员密码，然后单击**连接 vCenter Server**。
2. 设置 vSphere 集群名称，即在 vCenter Server 的资源列表中显示的集群名称。
3. 设置集群所属数据中心。可从下拉列表中选择已有的数据中心或创建新的数据中心。
4. （可选）开启 **vSphere HA**，并设置**主机故障响应**和**针对主机隔离的响应**的行为，如无特殊需求，可保持默认设置。

## 第 5 步：执行安装部署

1. 配置信息填写完成后，单击**核查信息**。系统将自动检查信息是否已填写，格式是否正确。
   - 如果通过检查，**核查信息**按钮将变为**执行安装部署**。
   - 如果未通过检查，系统将自动提示错误，请根据提示修改或补充信息，再单击**核查信息**。
2. 通过检查后，单击**执行安装部署**。系统将自动检查 Cluster Installer 是否支持运行安装部署工作。
   - 如果通过检查，弹出的对话框中将不会有错误提示。
   - 如果未通过检查，弹出的对话框中将有无法运行安装部署工作的提示，请根据提示解决问题后重试。
3. 通过检查后，单击**执行安装部署**。系统将自动跳转到**自动化执行**界面，并自动检查配置信息是否满足安装部署条件。
   - 如果通过检查，系统将自动执行安装部署。

     开始执行安装部署后，**自动化执行**界面将展示安装部署的总体进度。您可以单击**按目录查看日志**查看当前 workflow 的日志目录，目录按照主机粒度对 SCVM、tower、zbs-deploy-server、workflow 进行了归类，方便失败后排查。

     如果需要停止安装部署，可以在**自动化执行**界面右上角单击 **...** > **停止安装部署**。停止后如需重新执行，系统将会在所有主机上重新执行安装部署。

     > **注意**：
     >
     > 为保证安装部署的顺利执行，在安装 ESXi 阶段，请勿关闭当前页面，或者同时打开另一个页面查看该项目的**自动化执行**界面。
   - 如果未通过检查，例如检查到部分 IP 已被占用，界面将有错误提示，请根据提示修改配置信息后重新执行安装部署。

## 第 6 步：检查安装部署结果

执行结束后，在**自动化执行**界面可以查看 SMTX OS 集群的安装部署结果。

- 如果安装部署成功，界面将提示集群安装部署成功，您可以选择进行以下操作：
  - **打开 CloudTower**：如果集群已关联 CloudTower，可单击该项访问 CloudTower 进行集群管理。
  - **打开 vCenter Server**：如果集群已关联vCenter Server，可单击该项访问 vCenter Server 进行集群管理。
  - **打开集群 Web 控制台**：如果集群未关联 CloudTower 或 vCenter Server，可单击该项访问 Web 控制台进行集群管理。
  - **查看项目配置**：单击该项可查看此次项目中填写的配置信息。
- 如果安装部署失败，安装部署任务将会被终止，可根据具体的报错及日志信息参考 [Q&A](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_46) 排查导致失败的原因，解决问题后，可参考以下说明重新执行安装部署。
  - 如果无需修改配置信息，请在当前界面单击**重新执行**。系统将从上一次失败的步骤开始执行。
  - 如果需要修改配置信息，请在当前界面单击**修改配置信息**返回**配置信息**界面进行修改，然后再重新执行安装部署。
    > **说明**：
    >
    > 如果安装部署失败前已有主机完成 ESXi 安装，在**执行安装部署**对话框中将展示**重新安装 ESXi** 复选框，若勾选此复选框，系统将为所有主机重新安装 ESXi；若不勾选，系统将从上一次失败的步骤开始执行。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 安装 ESXi

# 安装 ESXi

**注意事项**

如果仅使用 Cluster Installer 安装 ESXi，请先下载 LiveCD 安装文件。

## 第 1 步：选择执行任务

1. 打开浏览器，在地址栏输入 Cluster Installer 的 IP 地址，输入用户名和密码，登录 Cluster Installer 的 Web 界面。
2. 在集群类型选项中，选择 **SMTX OS（VMware ESXi 平台）**。
3. 在**开始新项目**界面中，输入本次项目的名称。项目名称可用于区分执行的任务内容，建议使用英文字母和数字命名。
4. 在功能选项中，选择 **ESXi 安装**。
5. 单击**开始配置**。

## 第 2 步：获取主机信息

**注意事项**

从本步骤开始需要手动填写项目的配置信息，在填写信息的过程中请勿关闭浏览器，否则项目的配置信息将不会保留。

**操作步骤**

1. 在**集群规模**界面，输入待安装 ESXi 的主机数量、以及所有主机的 IPMI 管理台的 IP 地址、管理员用户名和密码。
2. 单击**获取主机信息**，然后根据获取结果确认主机信息是否获取成功，以及主机是否满足安装部署要求。
   - 如果主机信息全部获取成功且主机满足安装部署要求，界面将提示“已获取到主机 CPU 架构等信息”，主机列表中将展示每个主机的 BMC、CPU 架构和服务器型号。
   - 如果主机的 BMC 或 CPU 架构信息未获取成功，可单击下拉框，根据主机的 FRU 信息手动选择当前主机的 BMC 或 CPU 架构。
   - 如果查找不到主机或者主机不满足安装部署要求，界面将有错误提示，请根据提示解决问题后再单击**重新获取主机信息**。
3. 确认主机满足安装部署要求后，单击**下一步**。

## 第 3 步：上传安装文件

1. 在**安装文件**界面，单击**上传到 Cluster Installer**，进入安装文件上传界面。
2. 双击打开 Cluster Installer 中内置的 `md5sum.txt` 文件，以 `md5sum + 空格 + 文件名` 的格式手动添加目标 ESXi 版本的 ISO 的 MD5 信息。若有其他未添加 MD5 信息的安装文件，请以相同的格式手动输入该安装文件的 MD5 信息。

   > **注意**：
   >
   > 请勿更改 MD5 汇总表的文件名及文件格式，否则将导致校验 MD5 步骤出错。
3. 单击安装文件上传界面右上角的上传按钮，在本地计算机中选择所需的 ESXi 和 LiveCD 安装文件进行上传。

   > **说明**：
   >
   > 由于 LiveCD 安装文件的功能是收集主机信息，而 SMTX OS 安装文件也可以实现相同功能，因此建议：
   >
   > - 如果仅使用 Cluster Installer 安装 ESXi，请直接上传已下载的 LiveCD 安装文件。
   > - 如果后续还将使用 Cluster Installer 部署或扩容集群，可以直接上传目标版本的 SMTX OS 安装文件，并将其作为 LiveCD 安装文件使用。
4. 返回**安装文件**界面，单击**刷新**，然后选择所需的 ESXi 和 LiveCD 安装文件。
5. 单击**收集硬件配置**，然后根据收集结果确认主机的硬件配置是否满足安装部署要求。收集过程中可以单击**按目录查看日志**，确认收集进度。

   如果主机的硬件配置满足安装部署要求，界面将提示“已收集到主机中物理盘、网卡等硬件配置信息”。
6. 单击**下一步**。

## 第 4 步：输入配置信息

在**配置信息**界面，配置存储和 ESXi 账户，可根据实际情况选择配置 ESXi 管理网络。

### 配置存储

根据在确认 SMTX OS 集群构建要求时已规划的每块物理盘的用途，为每个主机选择用作 ESXi 系统盘的物理盘。

系统将为不包含 ESXi 系统盘的存储控制器开启直通模式。

### 配置 ESXi 管理网络

建议参考以下步骤配置 ESXi 管理网络，如果暂时无法区分 ESXi 管理网络对应的物理适配器，也可以关闭**配置 ESXi 管理网络**，在 Cluster Installer 完成 ESXi 安装后，再登录 ESXi 主机进行手动配置。

**操作步骤**

1. 给每个主机分别选择一个用于管理网络的网络适配器。
   - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网络适配器。
   - 如果需要给同一个主机分配多个用于管理网络的网络适配器，请在部署集群阶段继续添加。
2. 为每个 ESXi 主机输入实际规划的 ESXi 管理 IP。
3. 输入为管理网络实际规划的子网掩码和网关。
4. （可选）如果已为 ESXi 管理网络规划了 VLAN ID，请填写实际规划的 VLAN ID。

### 配置 ESXi 账户

为每个主机设置 ESXi 超级管理员 root 的密码。

## 第 5 步：执行安装

1. 配置信息填写完成后，单击**核查信息**。系统将自动检查信息是否已填写，格式是否正确。

   - 如果通过检查，**核查信息**按钮将变为**执行安装**。
   - 如果未通过检查，系统将自动提示错误，请根据提示修改或补充信息，再单击**核查信息**。
2. 通过检查后，单击**执行安装**。系统将自动检查 Cluster Installer 是否支持运行安装工作。

   - 如果通过检查，弹出的对话框中将不会有错误提示。
   - 如果未通过检查，弹出的对话框中将有无法运行安装工作的提示，请根据提示解决问题后重试。
3. 通过检查后，单击**执行安装**。系统将自动跳转到**自动化执行**界面，然后自动执行安装。

   开始执行安装后，**自动化执行**界面将展示安装的总体进度。您可以单击**按目录查看日志**查看当前 workflow 的日志目录，目录按照主机粒度进行了归类，方便失败后排查。

   如果需要停止安装，可以在**自动化执行**界面右上角单击 **...** > **停止安装**。停止后如需重新执行，系统将会在所有主机上重新执行安装。

## 第 6 步：检查安装结果

在**自动化执行**界面可以查看 ESXi 的安装结果。

- 如果安装成功，界面将提示 ESXi 安装成功。您可以单击**查看项目配置**查看此次项目中填写的配置信息。
- 如果安装失败，安装任务将会被终止，可根据具体的报错及日志信息参考 [Q&A](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_46) 排查导致失败的原因，解决问题后，可参考以下说明重新执行安装。
  - 如果无需修改配置信息，请在当前界面单击**重新执行**。系统将从上一次失败的步骤开始执行。
  - 如果需要修改配置信息，请在当前界面单击**修改配置信息**返回**配置信息**界面进行修改，然后再重新执行安装。

---

## 安装部署 SMTX OS 集群（VMware ESXi 平台） > 部署集群

# 部署集群

## 第 1 步：选择执行任务

1. 打开浏览器，在地址栏输入 Cluster Installer 的 IP 地址，输入用户名和密码，登录 Cluster Installer 的 Web 界面。
2. 在集群类型选项中，选择 **SMTX OS（VMware ESXi 平台）**。
3. 在**开始新项目**界面中，输入本次项目的名称。项目名称可用于区分执行的任务内容，建议使用英文字母和数字命名。
4. 在功能选项中，选择 **集群部署**。
5. 单击**开始配置**。

## 第 2 步：获取主机信息

**注意事项**

从本步骤开始需要手动填写项目的配置信息，在填写信息的过程中请勿关闭浏览器，否则项目的配置信息将不会保留。

**操作步骤**

1. 在**集群规模**界面，输入 ESXi 主机数量、以及所有主机的 ESXi 管理 IP、ESXi 用户名和密码。
2. 单击**获取主机信息**，然后根据获取结果确认主机信息是否获取成功，以及主机是否满足部署要求。

   如果主机信息获取成功且主机满足部署要求，界面将提示“已获取到主机中物理盘、网卡等硬件信息，并通过了环境检查”。否则界面将有错误提示，请根据提示解决问题后再单击**重新获取主机信息**。
3. 确认主机满足部署要求后，单击**下一步**。

## 第 3 步：上传安装文件

1. 在**安装文件**界面，单击**上传到 Cluster Installer**，进入安装文件上传界面。
2. 双击打开 Cluster Installer 中内置的 `md5sum.txt` 文件，检查文件中是否已包含本次部署所需安装文件的 MD5 信息。如果有未添加的 MD5 信息，请手动输入对应安装文件的 MD5 信息，格式为 `md5sum + 空格 + 文件名`。

   > **注意**：
   >
   > 请勿更改 MD5 汇总表的文件名及文件格式，否则将导致校验 MD5 步骤出错。
3. 单击安装文件上传界面右上角的上传按钮，在本地计算机中选择部署所需的安装文件进行上传。
4. 返回**安装文件**界面，单击**刷新**，然后根据需要选择安装文件。

   在 **CloudTower** 选项处，您可根据实际规划进行选择：

   - **部署全新 CloudTower**：若需要使用 CloudTower 管理集群，但当前环境中未有适配目标集群的 CloudTower，请选择该项，然后选择目标版本的 CloudTower 安装文件。
   - **关联已有 CloudTower**：若需要使用 CloudTower 管理集群，并且当前环境中已有适配目标集群的 CloudTower，请选择该项。
   - **不使用 CloudTower**：若无使用 CloudTower 管理集群的需求，可选择该项。
5. （可选）如果需要启用 RDMA 功能，且主机硬件配置和 ESXi 版本符合要求，可勾选**为存储网络启用 RDMA**，然后上传以下文件。

   - **MFT vib 软件包**：软件包名称必须以 `mft` 或 `Mellanox-MFT-Tools` 开头。
   - **NMST vib 软件包**：软件包名称必须以 `nmst` 或 `Mellanox-NATIVE-NMST` 开头。
   - **网卡固件文件**（仅当 RDMA 网卡是 MT27710 Family [ConnectX-4 Lx] 25Gb 网卡，且固件版本高于 14.26.4012 时展示）：请根据界面提示选择上传网卡固件文件或者手动执行固件降级。如果选择上传固件文件，则文件名必须以 `fw-ConnectX4Lx-rel` 开头。
6. 单击**下一步**。

## 第 4 步：输入集群配置信息

在**配置信息**界面，配置集群、存储、ESXi 主机、SCVM、网络、NFS 存储，并可根据实际情况选择配置 CloudTower、vCenter Server。

### 配置集群

1. 设置 SMTX OS 集群的名称、管理虚拟 IP 和超级管理员 root 的密码。
2. （可选）若有域名配置需求，请填写实际规划的 DNS 服务器的 IP 地址。
3. 选择 NTP 服务器。
   - 若需要使用集群外部 NTP 服务器来同步集群内的主机时间，请选择**使用集群外部 NTP 服务器**，并填写 NTP 服务器地址。
   - 若无使用集群外部 NTP 服务器的需求，请选择**使用集群内主机作为 NTP 服务器**。

### 配置存储

1. 根据集群要采用的存储分层/不分层模式，选择**分层**或**不分层**。
2. （可选）如果 SMTX OS 集群为 6.1.1 及以上版本，请根据实际规划为集群节点选择容量规格。
3. 根据在确认 SMTX OS 集群构建要求时已规划的每块物理盘的用途，为每个主机的物理盘选择用途。

   系统将为不包含 ESXi 系统盘的存储控制器开启直通模式。

### 配置 ESXi 主机

为每个主机设置 ESXi 主机名，使 ESXi 主机在 vCenter Server 资源列表中更有辨识度。

如果在安装 ESXi 阶段已给每个主机设置了 ESXi 主机名，此处将显示已设置的主机名，您也可以修改主机名。

### 配置 SCVM

1. 为每个主机设置 SCVM 名称和 SCVM 主机名。
   - SCVM 名称：SCVM 虚拟机的名称，在 vCenter Server 的虚拟机列表中可使用此名称查看 SCVM 虚拟机。
   - SCVM 主机名：SMTX OS 集群中 SCVM 所在节点的名称，在 CloudTower 或 Web 控制台中可使用此名称查看集群节点。
2. 根据主机的 ESXi 管理 IP 辨认并勾选集群的主节点。

### 配置 SCVM 密码

当 SMTX OS 集群为 6.1.1 及以上版本时，为集群内 SCVM 统一设置 root 账户和 smartx 账户的密码。

### 配置网络

#### 配置标准虚拟交换机

请先选择管理网络和存储网络采用的网络部署模式，再参考所选部署模式对应的步骤配置标准虚拟交换机。

> **注意**：
>
> - 不同的网络部署模式下，系统均已自动完成管理网络和存储网络所需虚拟交换机的创建，若要完成集群部署，您仅需要参考以下步骤完善对虚拟交换机的配置。
> - 如有需要，您还可以关联业务网络、vMotion 网络到已创建或新创建的虚拟交换机。如果 vMotion IP 和存储网络 IP 规划在同一网段，则必须将 vMotion 网络关联至存储网络虚拟交换机 ZBS，否则会导致存储网络异常。

**选择分离式部署**

1. 配置管理网络虚拟交换机 vSwitch0。
   1. 分别为虚拟交换机、ESXi 管理网络和 SCVM 管理网络选择所需的负载均衡模式。
   2. （可选）如果已为 ESXi 管理网络或 SCVM 管理网络规划了 VLAN ID，请填写实际规划的 VLAN ID。
   3. 给每个主机选择用于管理网络的网络适配器。
      - 不可删除系统默认分配网络适配器。
      - 如果需要给同一个主机分配多个用于管理网络的网络适配器，请继续添加网络适配器。
      - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网络适配器。
      - 若各个主机需要选择的网络适配的名称相同，可以在选择完一个主机的网络适配器后，在选框右侧单击 **...** > **在其他主机上选择同名适配器**。
2. 配置存储网络虚拟交换机 ZBS。
   1. 分别为虚拟交换机和 SCVM 存储网络选择所需的负载均衡模式。如果在[第 3 步：上传安装文件](#%E7%AC%AC-3-%E6%AD%A5%E4%B8%8A%E4%BC%A0%E5%AE%89%E8%A3%85%E6%96%87%E4%BB%B6)中已启用 RDMA 功能，系统默认勾选**启用 RDMA**，且自动将负载均衡模式设置为**基于源虚拟端口的路由**。
   2. （可选）如果已为 SCVM 存储网络规划了 VLAN ID，请填写实际规划的 VLAN ID。如果已启用 RDMA 功能，系统默认设置 VLAN ID 为 0。
   3. 给每个主机选择用于存储网络的网络适配器。
      - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网络适配器。
      - 如果已启用 RDMA 功能，当给同一个主机分配了多个网络适配器时，需要设置备用适配器，并需要确保所选的网络适配器均来自同一张支持 RDMA 功能的网卡。
      - 若各个主机需要选择的网络适配的名称相同，可以在选择完一个主机的网络适配器后，在选框右侧单击 **...** > **在其他主机上选择同名适配器**。
   4. （可选）当所选的网络适配器速率均为 25 GbE 及以上时，如果需要提升存储网络的带宽性能，可以将物理交换机上存储网络对应物理端口的 MTU 修改为 9000，然后勾选**同时将存储网络链路 MTU 设为 9000**。
   5. （可选）如果已启用 RDMA 功能，请选择所需的流量控制方式。
      > **注意**：
      >
      > 在执行部署前，需确保已手动在物理交换机端配置相同方式的流量控制。

**选择融合部署**

1. 分别为虚拟交换机、ESXi 管理网络、SCVM 管理网络和 SCVM 存储网络选择所需的负载均衡模式。
2. （可选）如果已为 ESXi 管理网络、SCVM 管理网络或 SCVM 存储网络规划了 VLAN ID，请填写实际规划的 VLAN ID。
3. 给每个主机选择管理网路和存储网络共用的网络适配器。
   - 不可删除系统默认分配网络适配器。
   - 如果需要给同一个主机分配多个网络适配器，请继续添加网络适配器。
   - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网络适配器。
   - 若各个主机需要选择的网络适配的名称相同，可以在选择完一个主机的网络适配器后，在选框右侧单击 **...** > **在其他主机上选择同名适配器**。
4. （可选）当所选的网络适配器速率均为 25 GbE 及以上时，如果需要提升存储网络的带宽性能，可以将物理交换机上存储网络对应物理端口的 MTU 修改为 9000，然后勾选**同时将存储网络链路 MTU 设为 9000**。

#### 配置网络 IP

1. 为每个 ESXi 主机输入实际规划的 SCVM 管理 IP、SCVM 存储 IP、ESXi 存储 IP。
2. （可选）如果启用了 RDMA 功能，请为每个 ESXi 主机输入 VMware 接入 IP。
3. （可选）如果在虚拟交换机中关联了 vMotion 网络，还输入实际规划的 vMotion 网络 IP。
4. 输入给各个网络实际规划的子网掩码和网关。

### 配置 NFS 数据存储

选择 NFS 存储的默认副本数和置备模式。

> **说明**：
>
> NFS 数据存储名称无需手动设置，系统已自动设置为 `datastore-nfs-<cluster_vip>`，其中 `<cluster_vip>` 表示集群虚拟管理 IP。您可通过集群虚拟管理 IP 区分不同集群对应的 NFS 数据存储。

### 关联 IPMI

强烈建议关联 IPMI，以便在 CloudTower 或 Web 控制台上管理集群时使用以下功能：

- 机箱拓扑，包括主机和物理盘定位；
- 物理盘闪灯；
- 主机风扇、CPU 温度和电源监控；

如果关闭**关联 IPMI**，后续您也可在 CloudTower 的集群的管理界面单击**设置** > **IPMI 信息**进行配置，或者在 Web 控制台中单击**设置** > **IPMI 信息**进行配置。

**操作步骤**

输入各个主机的 IPMI 管理台的 IP 地址、管理员用户名及密码。

### 配置 CloudTower

仅当在[第 3 步：上传安装文件](#%E7%AC%AC-3-%E6%AD%A5%E4%B8%8A%E4%BC%A0%E5%AE%89%E8%A3%85%E6%96%87%E4%BB%B6)时选择了**部署全新 CloudTower** 或**关联已有 CloudTower** 才可以配置 CloudTower。建议在此处配置 CloudTower 以便在自动化部署完成后直接对集群进行管理，若不配置，后续也可以参考《 SMTX OS 集群安装部署指南》的“关联 CloudTower“ 小节进行手动关联。

**前提条件**

已规划 CloudTower 的 IP 地址、子网掩码和网关。确保 CloudTower IP 与 SMTX OS 集群的管理虚拟 IP 正常连通。

#### 配置全新 CloudTower

1. 选择 CloudTower 环境的配置。用户可综合考虑待管理的集群数量，主机和虚拟机规模等信息，并结合集群主机的 CPU 利用率、内存余量和存储余量，选择**低配**或**高配**。
2. 设置 CloudTower 的组织名称。
3. （可选）设置集群所属数据中心的名称。设置后系统会自动创建一个该名称的数据中心，并将集群加入此数据中心。

   如果不设置，后续您也可以在 CloudTower 手动创建数据中心再选择该集群加入。
4. 设置 CloudTower 超级管理员 root 的密码。
5. 设置 CloudTower 的 IP 地址、子网掩码和网关。

#### 关联已有 CloudTower

1. 输入已有 CloudTower 的 IP 地址、管理员用户名及密码，然后单击**连接 CloudTower**。
2. （可选）连接 CloudTower 成功后，设置集群所属数据中心，可以从下拉列表中选择已有的数据中心或创建新的数据中心。

   如果不设置，后续您也可以在 CloudTower 手动创建数据中心再将该集群加入。

### 关联 vCenter Server

**注意事项**

- 如果当前环境中已有 vCenter Server，建议参考以下步骤关联 vCenter Server，以便设置 SMTX OS 的高可用。
- 如果当前环境中没有 vCenter Server，且只能在此次待部署集群的服务器上安装该软件，则需要在自动化部署完成后再安装 vCenter Server，然后参考《SMTX OS 集群安装部署指南》手动关联 vCenter 和设置 SMTX OS 的高可用性。

**操作步骤**

1. 输入已有 vCenter Server 的 IP 地址和端口号、管理员用户名及管理员密码，然后单击**连接 vCenter Server**。
2. 设置 vSphere 集群名称，即在 vCenter Server 的资源列表中显示的集群名称。
3. 设置集群所属数据中心。可从下拉列表中选择已有的数据中心或创建新的数据中心。
4. （可选）开启 **vSphere HA**，并设置**主机故障响应**和**针对主机隔离的响应**的行为，如无特殊需求，可保持默认设置。

## 第 5 步：执行部署

1. 配置信息填写完成后，单击**核查信息**。系统将自动检查信息是否已填写，格式是否正确。
   - 如果通过检查，**核查信息**按钮将变为**执行部署**。
   - 如果未通过检查，系统将自动提示错误，请根据提示修改或补充信息，再单击**核查信息**。
2. 通过检查后，单击**执行部署**。系统将自动检查 Cluster Installer 是否支持运行安装部署工作。
   - 如果通过检查，弹出的对话框中将不会有错误提示。
   - 如果未通过检查，弹出的对话框中将有无法运行部署工作的提示，请根据提示解决问题后重试。
3. （可选）当管理网络和存储网络采用分离式部署模式时，为避免由于网络不通导致部署失败，可以在**执行部署**对话框中，单击**检查存储网络连通性**。系统将为存储网络所在的虚拟交换机的所有网络适配器配置 ESXi 存储 IP，并检查 IP 间是否能连通。
   - 如果通过检查，对话框中将提示“所有主机上连接正常的物理适配器的存储网络已正常连通。”
   - 如果未通过检查，对话框中将提示检查不通过，可以根据表格中展示的具体连通情况排查原因，解决问题后，再重新检查连通性。
4. 通过检查后，单击**执行部署**。系统将自动跳转到**自动化执行**界面，并自动检查配置信息是否满足部署条件。
   - 如果通过检查，系统将自动执行部署。

     开始执行部署后，**自动化执行**界面将展示部署的总体进度。您可以单击**按目录查看日志**查看当前 workflow 的日志目录，目录按照主机粒度对 SCVM、tower、zbs-deploy-server、workflow 进行了归类，方便失败后排查。

     如果需要停止部署，可以在**自动化执行**界面右上角单击 **...** > **停止部署**。停止后如需重新执行，系统将会在所有主机上重新执行安装部署。
   - 如果未通过检查，例如检查到部分 IP 已被占用，界面将有错误提示，请根据提示修改配置信息后重新执行部署。

## 第 6 步：检查部署结果

执行结束后，在**自动化执行**界面可以查看 SMTX OS 集群的部署结果。

- 如果部署成功，界面将提示集群部署成功，您可以选择进行以下操作：
  - **打开 CloudTower**：如果集群已关联 CloudTower，可单击该项访问 CloudTower 进行集群管理。
  - **打开 vCenter Server**：如果集群已关联 vCenter Server，可单击该项访问 vCenter Server 进行集群管理。
  - **打开集群 Web 控制台**：如果集群未关联 CloudTower 或 vCenter Server，可单击该项，访问 Web 控制台进行集群管理。
  - **查看项目配置**：单击该项可查看此次项目中填写的配置信息。
- 如果部署失败，部署任务将会被终止，可根据具体的报错及日志信息参考 [Q&A](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_46) 排查导致失败的原因，解决问题后，可参考以下说明重新执行部署。
  - 如果无需修改配置信息，请在当前界面单击**重新执行**。系统将从上一次失败的步骤开始执行。
  - 如果需要修改配置信息，请在当前界面单击**修改配置信息**返回**配置信息**界面进行修改，然后再重新执行部署。

---

## 扩容 SMTX OS 集群（VMware ESXi 平台）

# 扩容 SMTX OS 集群（VMware ESXi 平台）

如果需要扩容 SMTX OS（VMware ESXi）集群，您可以使用 Cluster Installer 完成 ESXi 安装和集群扩容，如果扩容现场环境或需求受限，您也可以选择仅使用 Cluster Installer 安装 ESXi 或者扩容集群。下文将详细介绍使用 Cluster Installer 扩容 SMTX OS（VMware ESXi) 集群的方式、要求、操作流程和操作步骤。

---

## 扩容 SMTX OS 集群（VMware ESXi 平台） > 扩容 SMTX OS 集群的方式

# 扩容 SMTX OS 集群的方式

使用 Cluster Installer 完成扩容 SMTX OS 集群的完整操作时，有以下两种方式。

- 一次性完成 ESXi 安装和集群扩容：仅需要手动输入一次扩容 SMTX OS 集群过程所需信息，Cluster Installer 即可自动化执行安装和扩容的全部流程，执行期间无需操作人值守，但该方式对网络要求较高。
- 先安装 ESXi，再扩容集群：需要先手动输入安装 ESXi 所需信息，等待 Cluster Installer 执行 ESXi 软件安装，再输入扩容集群所需信息，Cluster Installer 自动完成集群扩容。该方式对网络要求较低。

如果现场环境仅能满足安装 ESXi 软件的网络要求，或者 Cluster Installer 不支持待扩容的 SMTX OS 集群版本，也可以仅使用 Cluster Installer 安装 ESXi，但后续还需要手动完成集群的扩容，可以参考对应版本的《SMTX OS 运维指南》的“集群扩容”或“添加节点”章节，从“设置 ESXi”的步骤开始继续操作。

如果现场环境仅能满足扩容集群的网络要求，也可以仅使用 Cluster Installer 扩容集群，但在此之前需要参考对应版本的《SMTX OS 集群安装部署指南》的“在每个节点上安装 ESXi 软件”和“设置 ESXi”章节，为待添加至 SMTX OS 集群的主机手动安装 ESXi 软件和配置 ESXi 管理 IP，再使用 Cluster Installer 完成集群的扩容。

---

## 扩容 SMTX OS 集群（VMware ESXi 平台） > 扩容 SMTX OS 集群的要求

# 扩容 SMTX OS 集群的要求

使用 Cluster Installer 扩容 SMTX OS 集群之前，需要先确保现场扩容环境满足扩容 SMTX OS 集群的基本要求，再确保其满足使用 Cluster Installer 的要求。

---

## 扩容 SMTX OS 集群（VMware ESXi 平台） > 扩容 SMTX OS 集群的要求 > 扩容 SMTX OS 集群的基本要求

# 扩容 SMTX OS 集群的基本要求

请参考待扩容 SMTX OS 集群版本的《SMTX OS 运维指南》的“集群扩容”或“添加节点”章节，做好为集群添加新节点的准备工作。

> **注意**：
>
> 当待扩容集群已为 U.2 NVMe 直通硬盘启用热插拔功能时，如果使用 Cluster Installer 进行集群扩容，则无需提前准备 vmpctl 文件，只需确保待添加的节点满足以下要求。
>
> - 目标 ESXi 软件是 8.0 U1 及以上版本。
> - 服务器的引导模式已设置为 “UEFI”。
> - 服务器支持 VMDirectPath I/O 功能，可在 [Broadcom 官网](https://compatibilityguide.broadcom.com/)查看当前服务器型号是否支持该功能。
> - 服务器平台和设备满足 VMDirectPath I/O 功能的要求，可在 [Broadcom 官网](https://knowledge.broadcom.com/external/article?legacyId=2142307)查看具体要求。
>
> 另外，扩容过程中您也无需手动设置 ESXi 主机和 SCVM 的参数。

---

## 扩容 SMTX OS 集群（VMware ESXi 平台） > 扩容 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求

# 使用 Cluster Installer 的要求

请确认现场扩容环境满足以下对使用 Cluster Installer 的要求。

---

## 扩容 SMTX OS 集群（VMware ESXi 平台） > 扩容 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求 > Cluster Installer 所在虚拟机的运行环境要求

# Cluster Installer 所在虚拟机的运行环境要求

Cluster Installer 部署在虚拟机中，该虚拟机需运行在已安装虚拟机管理程序的服务器、个人电脑或集群主机中，当前仅支持以下类型。

- ESXi 主机；

  > **注意**：
  >
  > 可以直接使用待扩容集群中的任意一个 ESXi 主机。如果仅使用 Cluster Installer 扩容集群，也可以选择使用待添加至集群的任意一个 ESXi 主机。
- 已安装如下虚拟机管理软件的个人电脑：

  - VMware Workstation：14 Pro 及以上版本；
  - Oracle VirtualBox：6.0 及以上版本。
  > **注意**：
  >
  > 为确保软件能成功安装，建议在安装前先在本地计算机的 BIOS/固件设置中启用 Intel VT-x，然后重启计算机。
- 5.0.5 及以上版本的 SMTX OS（ELF）集群中的主机。
- SMTX ELF 集群中的主机（已配置关联存储）。

此外，以上服务器、个人电脑和集群主机还需满足以下要求：

- CPU 架构为 x86\_64；
- 有足够的资源空间：
  - 至少 2 个 CPU；
  - 至少 64 GB 存储空间；
  - 至少 2 GB 内存，但对于 SMTX OS（ELF）集群中的主机，则需预留至少 3 GiB 内存。
- 对于个人电脑，其使用的物理网卡速率必须大于或等于 1 Gbps。

---

## 扩容 SMTX OS 集群（VMware ESXi 平台） > 扩容 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求 > 软件版本要求

# 软件版本要求

不同的扩容方式对扩容 SMTX OS 集群的目标软件版本的要求不同。

- 使用 Cluster Installer 一次性完成 ESXi 安装和集群扩容：需要满足[配套的软件版本](/clusterinstaller/1.4.1/installer_release_notes/cluster_installer_release_notes_02#%E9%85%8D%E5%A5%97%E7%9A%84%E8%BD%AF%E4%BB%B6%E7%89%88%E6%9C%AC)中对 ESXi 和 SMTX OS 软件版本的要求，并且目标 ESXi 软件版本必须是 ISO 版本。
- 使用 Cluster Installer 先安装 ESXi，再扩容集群：使用 Cluster Installer 先安装 ESXi，再部署集群：需要满足[配套的软件版本](/clusterinstaller/1.4.1/installer_release_notes/cluster_installer_release_notes_02#%E9%85%8D%E5%A5%97%E7%9A%84%E8%BD%AF%E4%BB%B6%E7%89%88%E6%9C%AC)中对 ESXi 和 SMTX OS 软件版本的要求。
- 仅使用 Cluster Installer 安装 ESXi：仅需要满足[配套的软件版本](/clusterinstaller/1.4.1/installer_release_notes/cluster_installer_release_notes_02#%E9%85%8D%E5%A5%97%E7%9A%84%E8%BD%AF%E4%BB%B6%E7%89%88%E6%9C%AC)中对 ESXi 软件版本的要求。
- 仅使用 Cluster Installer 扩容集群：需要满足[配套的软件版本](/clusterinstaller/1.4.1/installer_release_notes/cluster_installer_release_notes_02#%E9%85%8D%E5%A5%97%E7%9A%84%E8%BD%AF%E4%BB%B6%E7%89%88%E6%9C%AC)中对 ESXi 和 SMTX OS 软件版本的要求。

---

## 扩容 SMTX OS 集群（VMware ESXi 平台） > 扩容 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求 > 待添加的服务器要求

# 待添加的服务器要求

待添加至 SMTX OS 集群的服务器需要满足以下要求：

- 服务器的型号满足[配套的服务器](/clusterinstaller/1.4.1/installer_release_notes/cluster_installer_release_notes_02#%E9%85%8D%E5%A5%97%E7%9A%84%E6%9C%8D%E5%8A%A1%E5%99%A8)要求。
- 如果需要使用 Cluster Installer 一次性完成 ESXi 安装和集群扩容，且待扩容集群启用了 RDMA，则为服务器配置的 RDMA 网卡不能为 ConnectX-4 Lx 系列的 Mellanox 网卡。

---

## 扩容 SMTX OS 集群（VMware ESXi 平台） > 扩容 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求 > 浏览器版本要求

# 浏览器版本要求

借助 Cluster Installer 扩容 SMTX OS 集群过程中需要使用 Web 浏览器，为保证兼容性，建议使用 Chrome 80 或 Firefox 78 及以上版本的浏览器，并启用 Cookie 和 JavaScript。

---

## 扩容 SMTX OS 集群（VMware ESXi 平台） > 扩容 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求 > 网络连通要求

# 网络连通要求

借助 Cluster Installer 扩容 SMTX OS 集群时，需要确保 Cluster Installer 的网络环境和 IP 均满足网络连通要求，但不同的扩容方式对网络连通的要求不同，请参考以下说明规划 Cluster Installer 的网络和 IP：

- 使用 Cluster Installer 一次性完成 ESXi 安装和集群扩容：需满足下表中对 **ESXi 安装和集群扩容**功能的要求。
- 使用 Cluster Installer 先安装 ESXi，再扩容集群：需满足下表中对 **ESXi 安装**、**集群扩容**功能的要求。
- 仅使用 Cluster Installer 安装 ESXi：需满足下表中对 **ESXi 安装**功能的要求。
- 仅使用 Cluster Installer 扩容集群：需满足下表中对**集群扩容**功能的要求。

| 功能 | 对 Cluster Installer 网络环境的要求 | 对 Cluster Installer IP 的要求 |
| --- | --- | --- |
| ESXi 安装和集群扩容 | - 若在 ESXi 主机、SMTX OS 集群或 SMTX ELF 集群中安装 Cluster Installer，则主机或集群中需要有可同时连通新集群的 ESXi 管理网络、待添加服务器的 IPMI 网络的虚拟机网络，且虚拟机网络的带宽必须大于或等于 1 Gbps。 - 若在个人电脑中安装 Cluster Installer，则个人电脑需能同时与新集群的 ESXi 管理网络、待添加服务器的 IPMI 网络连通。 | 须同时满足 **ESXi 安装、集群扩容**的要求。 |
| ESXi 安装 | - 若在 ESXi 主机、SMTX OS 集群或 SMTX ELF 集群中安装 Cluster Installer，则主机或集群中需要有可连通待添加服务器的 IPMI 网络的虚拟机网络，且虚拟机网络的带宽必须大于或等于 1 Gbps。 - 若在个人电脑中安装 Cluster Installer，则个人电脑需要与待添加服务器的 IPMI 网络连通。 | Cluster Installer IP 与待添加服务器的 IPMI IP 可以互相连通。 |
| 集群扩容 | - 若在 ESXi 主机、SMTX OS 集群或 SMTX ELF 集群中安装 Cluster Installer，则主机或集群中需要有可连通新集群的 ESXi 管理网络的虚拟机网络，且虚拟机网络的带宽必须大于或等于 1 Gbps。 - 若在个人电脑中安装 Cluster Installer，则个人电脑需要与新集群的 ESXi 管理网络连通。 | - Cluster Installer IP 与新集群的 ESXi 管理 IP 可以互相连通。 - Cluster Installer IP 可以连通新集群的 SCVM 管理 IP。 - 如果需要使用 Cluster Installer 关联 vCenter Server，则要求 Cluster Installer IP 可以连通 vCenter Server IP。 - 如果需要使用 Cluster Installer 关联 CloudTower，则要求 Cluster Installer IP 可以连通 CloudTower IP。 |

---

## 扩容 SMTX OS 集群（VMware ESXi 平台） > 扩容 SMTX OS 集群的要求 > 使用 Cluster Installer 的要求 > 防火墙端口开放要求

# 防火墙端口开放要求

如果 Cluster Installer 与待扩容集群、CloudTower、vCenter Server 等之间通信的网络存在防火墙，则目标端须开放相应的端口。不同的扩容方式对端口开放有不同的要求，请参考以下说明检查防火墙端口：

- 使用 Cluster Installer 一次性完成 ESXi 安装和集群扩容，或者先安装 ESXi 再扩容集群：需满足下表中对 **ESXi 安装**、**集群扩容**功能的要求。
- 仅使用 Cluster Installer 安装 ESXi：需满足下表中对 **ESXi 安装**功能的要求。
- 仅使用 Cluster Installer 扩容集群：需满足下表中对**集群扩容**功能的要求。

| 功能 | 源端 | 目标端 | 目标端需开放端口 | 用途 |
| --- | --- | --- | --- | --- |
| ESXi 安装 | 浏览器客户端 IP | Cluster Installer IP | TCP 80 | 浏览器 Web 访问 Cluster Installer |
| Cluster Installer IP | 待添加主机的 IPMI IP | TCP 443 | BMC Redfish/HTTPS API 端口 |
| UDP 623 | IPMI 协议端口，用于获取服务器 FRU 信息、SOL 串口输出 |
| TCP 22 | 如果服务器的 BMC 为 Huawei iBMC 或 Dell iDRAC 且 iDRAC 版本低于 4.0，需要通过 SSH 登录到 BMC 挂载 ISO 文件 |
| 待添加主机的 IPMI IP | Cluster Installer IP | Cluster Installer 虚拟机 NFS Server 端口 \* | NFS 访问端口，BMC 需要通过 NFS 协议挂载 Cluster Installer 虚拟机里的 ISO 文件 |
| TCP 80 | 如果服务器的 BMC 为 HPE iLO5，需开放此端口 |
| 集群扩容 | 浏览器客户端 IP | Cluster Installer IP | TCP 80 | 用于浏览器 Web 访问 Cluster Installer |
| Cluster Installer IP | 待扩容集群的 ESXi 管理 IP | TCP 443 | ESXi HTTPS API 访问端口 |
| TCP 22 | 用于 SSH 登录 ESXi 主机 |
| Cluster Installer IP | 待扩容集群的 ESXi 管理 IP | TCP 443 | SMTX OS 集群 API 访问端口 |
| TCP 80 | SMTX OS 集群扩容 API 访问端口 |
| TCP 22 | 用于 SSH 登录 SCVM 主机 |
| 待扩容集群的 ESXi 管理 IP | Cluster Installer IP | Cluster Installer 虚拟机 NFS Server 端口 \* | ESXi 主机通过挂载 Cluster Installer 虚拟机 NFS 数据存储的方式访问 ISO、ESXi 插件等文件 |
| Cluster Installer IP | vCenter Server IP | TCP 443 | vCenter API 访问端口 |

> **说明**：
>
> Cluster Installer 虚拟机 NFS Server 端口（表中有星号 \* 标记的端口）除了 `2049` 和 `111` 两个固定端口外，其他端口均为随机端口。在创建完 Cluster Installer 虚拟机并配置完 IP 后，您才能查看 NFS Server 使用了哪些随机端口，同时您也可以选择自定义除 111 端口外的其他 NFS Server 端口，建议参考上述要求提前规划。

---

## 扩容 SMTX OS 集群（VMware ESXi 平台） > 扩容 SMTX OS 集群的流程

# 扩容 SMTX OS 集群的流程

使用 Cluster Installer 扩容 SMTX OS 集群的 4 种方式的操作流程如下。

## 使用 Cluster Installer 一次性完成 ESXi 安装和集群扩容

1. 确认现场环境满足使用该方式的要求，参见[扩容 SMTX OS 集群的要求](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_22)。
2. 创建 Cluster Installer 虚拟机，参见[创建 Cluster Installer 虚拟机](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_13)。
3. 配置 Cluster Installer IP，参见[配置 Cluster Installer IP](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_14)。
4. 开放 NFS Server 端口，参见[开放 NFS Server 端口](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_15)。
5. 检查服务器的 BMC 和 BIOS 设置，参见[检查服务器的 BMC 和 BIOS 设置](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_16)。
6. 若待扩容集群已启用 RDMA，建议先参考《SMTX OS 集群安装部署指南》的“在交换机端配置流量控制”小节手动在物理交换机端配置与集群相同方式的流量控制。
7. 使用 Cluster Installer 安装 ESXi 和扩容集群，参见[安装 ESXi 和扩容集群](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_24)。
8. 若已启用 RDMA，请参考《SMTX OS 集群安装部署指南》的“验证流量控制的配置结果”小节，在 SCVM 中验证流量控制配置是否正确。
   > **注意**：
   >
   > 由于验证流量控制的配置结果需要至少 3 个节点，若新增节点在 3 个及以上，则仅需对新增节点进行测试；否则需要从集群借用原有的节点与新增节点组成 3 个节点进行测试，为避免影响集群原有节点的业务性能和测试结果的准确性，建议在集群业务空闲期进行验证。

## 使用 Cluster Installer 先安装 ESXi，再扩容集群

1. 确认现场环境满足使用该方式的要求，参见[扩容 SMTX OS 集群的要求](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_22)。
2. 创建 Cluster Installer 虚拟机，参见[创建 Cluster Installer 虚拟机](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_13)。
3. 配置 Cluster Installer IP，参见[配置 Cluster Installer IP](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_14)。
4. 开放 NFS Server 端口，参见[开放 NFS Server 端口](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_15)。
5. 检查服务器的 BMC 和 BIOS 设置，参见[检查服务器的 BMC 和 BIOS 设置](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_16)。
6. 若待扩容集群已启用 RDMA，建议先参考《SMTX OS 集群安装部署指南》的“在交换机端配置流量控制”小节手动在物理交换机端配置与集群相同方式的流量控制。
7. 使用 Cluster Installer 为待添加主机安装 ESXi，参见[安装 ESXi](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_18)。
8. 若目标 ESXi 软件版本是 Patch 版本，请登录 Broadcom 文档官网，参考对应 ESXi 软件版本的 《VMware ESXi 升级》手册，手动升级 ESXi 版本至目标版本。
9. 使用 Cluster Installer 扩容集群，参见[扩容集群](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_26)。
10. 若已启用 RDMA，请参考《SMTX OS 集群安装部署指南》的“验证流量控制的配置结果”小节，在 SCVM 中验证流量控制配置是否正确。
    > **注意**：
    >
    > 由于验证流量控制的配置结果需要至少 3 个节点，若新增节点在 3 个及以上，则仅需对新增节点进行测试；否则需要从集群借用原有的节点与新增节点组成 3 个节点进行测试，为避免影响集群原有节点的业务性能和测试结果的准确性，建议在集群业务空闲期进行验证。

## 仅使用 Cluster Installer 扩容集群

1. 确认现场环境满足使用该方式的要求，参见[扩容 SMTX OS 集群的要求](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_22)。
2. 参考目标 SMTX OS 版本的《SMTX OS 集群安装部署指南》的“在每个节点上安装 ESXi 软件”和“设置 ESXi”章节，为待添加至 SMTX OS 集群的主机手动安装 ESXi 软件和配置 ESXi 管理 IP。
3. 创建 Cluster Installer 虚拟机，参见[创建 Cluster Installer 虚拟机](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_13)。
4. 配置 Cluster Installer IP，参见[配置 Cluster Installer IP](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_14)。
5. 开放 NFS Server 端口，参见[开放 NFS Server 端口](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_15)。
6. 若待扩容集群已启用 RDMA，建议先参考《SMTX OS 集群安装部署指南》的“在交换机端配置流量控制”小节手动在物理交换机端配置与集群相同方式的流量控制。
7. 使用 Cluster Installer 扩容集群，参见[扩容集群](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_26)。
8. 如果已启用 RDMA，请参考《SMTX OS 集群安装部署指南》的“验证流量控制的配置结果”小节，在 SCVM 中验证流量控制配置是否正确。
   > **注意**：
   >
   > 由于验证流量控制的配置结果需要至少 3 个节点，若新增节点在 3 个及以上，则仅需对新增节点进行测试；否则需要从集群借用原有的节点与新增节点组成 3 个节点进行测试，为避免影响集群原有节点的业务性能和测试结果的准确性，建议在集群业务空闲期进行验证。

## 仅使用 Cluster Installer 安装 ESXi

1. 确认现场环境满足使用该方式的要求，参见[扩容 SMTX OS 集群的要求](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_22)。
2. 创建 Cluster Installer 虚拟机，参见[创建 Cluster Installer 虚拟机](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_13)。
3. 配置 Cluster Installer IP，参见[配置 Cluster Installer IP](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_14)。
4. 开放 NFS Server 端口，参见[开放 NFS Server 端口](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_15)。
5. 检查服务器的 BMC 和 BIOS 设置，参见[检查服务器的 BMC 和 BIOS 设置](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_16)。
6. 使用 Cluster Installer 安装 ESXi，参见[安装 ESXi](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_18)。
7. 若目标 ESXi 软件版本是 Patch 版本，请登录 Broadcom 文档官网，参考对应 ESXi 软件版本的 《VMware ESXi 升级》手册，手动升级 ESXi 版本至目标版本。
8. 参考目标 SMTX OS 版本的《SMTX OS 运维指南》的“集群扩容”或“添加节点”章节，从“设置 ESXi”的步骤开始继续操作。

---

## 扩容 SMTX OS 集群（VMware ESXi 平台） > 安装 ESXi 和扩容集群

# 安装 ESXi 和扩容集群

## 第 1 步：选择执行任务

1. 打开浏览器，在地址栏输入 Cluster Installer 的 IP 地址，输入用户名和密码，登录 Cluster Installer 的 Web 界面。
2. 在集群类型选项中，选择 **SMTX OS（VMware ESXi 平台）**。
3. 在**开始新项目**界面中，输入本次项目的名称。项目名称可用于区分执行的任务内容，建议使用英文字母和数字命名。
4. 在功能选项中，选择 **ESXi 安装和集群扩容**。
5. 单击**开始配置**。

## 第 2 步：关联待扩容集群

**注意事项**

从本步骤开始需要手动填写项目的配置信息，在填写信息的过程中请勿关闭浏览器，否则项目的配置信息将不会保留。

**操作步骤**

1. 在弹出的**集群扩容**对话框中，输入待扩容集群的管理虚拟 IP、管理员用户名和密码。
2. 单击**关联集群**。系统将自动获取并检查集群信息。

   如果关联成功，对话框将提示“连接集群成功”，并显示集群的名称、SMTX OS 软件版本、虚拟化平台、主机数量，如果集群已启用 RDMA，还将显示 `RDMA` 标签。
3. 成功关联集群后，单击**开始配置**。

## 第 3 步：获取主机信息

1. 在**集群规模**界面，输入待添加的主机数量、以及所有待添加主机的 IPMI 管理台的 IP 地址、管理员用户名和密码。
2. 单击**获取主机信息**，然后根据获取结果确认主机信息是否获取成功，以及主机是否满足扩容要求。
   - 如果主机信息全部获取成功且主机满足扩容要求，界面将提示“已获取到主机 CPU 架构等信息”，主机列表中将展示每个主机的 BMC、CPU 架构和服务器型号。
   - 如果主机的 BMC 或 CPU 架构信息未获取成功，可单击下拉框，根据主机的 FRU 信息手动选择当前主机的 BMC 或 CPU 架构。
   - 如果查找不到主机或者主机不满足扩容要求，界面将有错误提示，请根据提示解决问题后再单击**重新获取主机信息**。
3. 确认主机满足扩容要求后，单击**下一步**。

## 第 4 步：上传安装文件

1. 在**安装文件**界面，单击**上传到 Cluster Installer**，进入安装文件上传界面。
2. 双击打开 Cluster Installer 中内置的 `md5sum.txt` 文件，以 `md5sum + 空格 + 文件名` 的格式手动添加目标 ESXi 版本的 ISO 的 MD5 信息。若有其他未添加 MD5 信息的安装文件，请以相同的格式手动输入该安装文件的 MD5 信息。

   > **注意**：
   >
   > 请勿更改 MD5 汇总表的文件名及文件格式，否则将导致校验 MD5 步骤出错。
3. 单击安装文件上传界面右上角的上传按钮，在本地计算机中选择扩容所需的安装文件进行上传。
4. 返回**安装文件**界面，单击**刷新**，然后根据需要选择安装文件。
5. 单击**收集硬件配置**，然后根据收集结果确认待添加主机的硬件配置是否满足扩容要求。收集过程中可以单击**按目录查看日志**，确认收集进度。

   如果主机的硬件配置满足扩容要求，界面将提示“已收集到主机中物理盘、网卡等硬件配置信息”。
6. （可选）如果待扩容集群启用了 RDMA 且待添加主机的配置支持 RDMA，系统将自动勾选**为存储网络启用 RDMA**，请上传以下文件。

   - **MFT vib 软件包**：软件包名称必须以 `mft` 或 `Mellanox-MFT-Tools` 开头。
   - **NMST vib 软件包**：软件包名称必须以 `nmst` 或 `Mellanox-NATIVE-NMST` 开头。
7. 单击**下一步**。

## 第 5 步：输入配置信息

### 配置存储

为待添加主机的物理盘选择实际规划的用途。

系统将为不包含 ESXi 系统盘和 SMTX 引导盘的存储控制器开启直通模式。

### 配置 ESXi 主机

为待添加主机设置 ESXi 超级管理员 root 的密码和 ESXi 主机名。其中，主机名可使 ESXi 主机在 vCenter Server 资源列表中更有辨识度。

### 配置 SCVM

为待添加主机设置 SCVM 名称和 SCVM 主机名。

- SCVM 名称：SCVM 虚拟机的名称，在 vCenter Server 的虚拟机列表中可使用此名称查看 SCVM 虚拟机。
- SCVM 主机名：SMTX OS 集群中 SCVM 所在节点的名称，在 CloudTower 或 Web 控制台中可使用此名称查看集群节点。

### 配置 SCVM 密码

当 SMTX OS 集群为 6.1.1 及以上版本时，请为待添加的 SCVM 统一设置 root 账户和 smartx 账户的密码。

### 配置网络

#### 配置标准虚拟交换机

请参考以下步骤分别配置每个虚拟交换机。

1. 分别为虚拟交换机和其关联网络选择所需的负载均衡模式。
2. （可选）如果待扩容集群的虚拟交换机中的关联网络已配置了 VLAN ID，请输入与集群中其他主机一致的 VLAN ID。
3. 为每个待添加主机选择用于关联网络的网络适配器。
   - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网络适配器。
   - 如果关联网络中包含 SCVM 存储网络且该网络已启用 RDMA 功能，当给同一个主机分配了多个网络适配器时，需要设置备用适配器，并需要确保所选的网络适配器均来自同一张支持 RDMA 功能的网卡。
   - 若各个主机需要选择的网络适配的名称相同，可以在选择完一个主机的网络适配器后，在选框右侧单击 **...** > **在其他主机上选择同名适配器**。
4. （可选）如果关联网络中包含 SCVM 存储网络且该网络已启用 RDMA 功能，请选择待扩容集群使用的流量控制方式。
   > **注意**：
   >
   > 在执行安装扩容前，需确保已手动在物理交换机端配置相同方式的流量控制。

#### 配置网络 IP

**注意事项**

以下仅介绍为待添加主机配置 IP 的步骤。子网掩码和网关的设置已由系统自动从待扩容集群中获取并填写完成，不建议修改，否则将变更集群的子网掩码和网关。

**操作步骤**

1. 为待添加主机输入实际规划的 ESXi 管理 IP、SCVM 管理 IP、ESXi 存储 IP、SCVM 存储 IP。
2. （可选）如果启用了 RDMA 功能，请为待添加主机输入 VMware 接入 IP。

### 挂载 NFS 数据存储

如果需要为待添加主机挂载待扩容集群中已有的 NFS 数据存储，可以在下拉列表中选择所需的 NFS 数据存储。否则请关闭**挂载 NFS 数据存储**，后续再参考《SMTX OS 集群安装部署指南》的“创建 NFS 数据存储并挂载至 ESXi 主机“章节为主机手动创建和挂载 NFS 存储。

## 第 6 步：执行安装扩容

1. 配置信息填写完成后，单击**核查信息**。系统将自动检查信息是否已填写，格式是否正确。
   - 如果通过检查，**核查信息**按钮将变为**执行安装扩容**。
   - 如果未通过检查，系统将自动提示错误，请根据提示修改或补充信息，再单击**核查信息**。
2. 通过检查后，单击**执行安装扩容**。系统将自动检查 Cluster Installer 是否支持运行安装扩容工作。
   - 如果通过检查，弹出的对话框中将不会有错误提示。
   - 如果未通过检查，弹出的对话框中将有无法运行安装扩容工作的提示，请根据提示解决问题后重试。
3. 通过检查后，单击**执行安装扩容**。系统将自动跳转到**自动化执行**界面，并自动检查配置信息是否满足安装扩容条件。
   - 如果通过检查，系统将自动执行安装扩容。

     开始执行安装扩容后，**自动化执行**界面将展示安装扩容的总体进度。您可以单击**按目录查看日志**查看当前 workflow 的日志目录，目录按照主机粒度对 SCVM、tower、zbs-deploy-server、workflow 进行了归类，方便失败后排查。

     如果需要停止安装扩容，可以在**自动化执行**界面右上角单击 **...** > **停止安装扩容**。停止后如需重新执行，系统将会在所有主机上重新执行安装扩容。

     > **注意**：
     >
     > 为保证安装扩容的顺利执行，在安装 ESXi 阶段，请勿关闭当前页面，或者同时打开另一个页面查看该项目的**自动化执行**界面。
   - 如果未通过检查，例如检查到部分 IP 已被占用，界面将有错误提示，请根据提示修改配置信息后重新执行安装扩容。

## 第 7 步：检查集群安装扩容结果

执行结束后，在**自动化执行**界面可以查看 SMTX OS 集群的安装扩容结果。

- 如果安装扩容成功，界面将提示集群安装扩容成功，您可以选择进行以下操作：
  - **打开 CloudTower**：如果待扩容集群已关联 CloudTower，可单击该项访问 CloudTower 进行集群管理。
  - **打开 vCenter Server**：如果待扩容集群已关联 vCenter Server，可单击该项访问 vCenter Server 进行集群管理。
  - **打开集群 Web 控制台**：如果待扩容集群未关联 CloudTower 或 vCenter Server，可单击该项访问 Web 控制台进行集群管理。
  - **查看项目配置**：单击该项可查看此次项目中填写的配置信息。
- 如果安装扩容失败，安装扩容任务将会被终止，可根据具体的报错及日志信息参考 [Q&A](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_46) 排查导致失败的原因，解决问题后，可参考以下说明重新执行安装扩容。
  - 如果无需修改配置信息，请在当前界面单击**重新执行**。系统将从上一次失败的步骤开始执行。
  - 如果需要修改配置信息，请在当前界面单击**修改配置信息**返回**配置信息**界面进行修改，然后再重新执行安装扩容。
    > **说明**：
    >
    > 如果安装扩容失败前已有主机完成 ESXi 安装，在**执行安装扩容**对话框中将展示**重新安装 ESXi** 复选框，若勾选此复选框，系统将为所有主机重新安装 ESXi；若不勾选，系统将从上一次失败的步骤开始执行。

---

## 扩容 SMTX OS 集群（VMware ESXi 平台） > 扩容集群

# 扩容集群

## 第 1 步：选择执行任务

1. 打开浏览器，在地址栏输入 Cluster Installer 的 IP 地址，输入用户名和密码，登录 Cluster Installer 的 Web 界面。
2. 在集群类型选项中，选择 **SMTX OS（VMware ESXi 平台）**。
3. 在**开始新项目**界面中，输入本次项目的名称。项目名称可用于区分执行的任务内容，建议使用英文字母和数字命名。
4. 在功能选项中，选择 **集群扩容**。
5. 单击**开始配置**。

## 第 2 步：关联待扩容集群

**注意事项**

从本步骤开始需要手动填写项目的配置信息，在填写信息的过程中请勿关闭浏览器，否则项目的配置信息将不会保留。

**操作步骤**

1. 在弹出的**集群扩容**对话框中，输入待扩容集群的管理虚拟 IP、管理员用户名和密码。
2. 单击**关联集群**。系统将自动获取并检查集群信息。

   如果关联成功，对话框将提示“连接集群成功”，并显示集群的名称、SMTX OS 软件版本、虚拟化平台、主机数量，如果集群已启用 RDMA，还将显示 `RDMA` 标签。
3. 成功关联集群后，单击**开始配置**。

## 第 3 步：获取主机信息

1. 在**集群规模**界面，输入待添加的主机数量、以及所有待添加主机的 IPMI 管理台的 IP 地址、管理员用户名和密码。
2. 单击**获取主机信息**，然后根据获取结果确认主机信息是否获取成功，以及主机是否满足扩容要求。

   如果主机信息获取成功且主机满足扩容要求，界面将提示“已获取到主机中物理盘、网卡等硬件信息，并通过了环境检查”。否则界面将有错误提示，请根据提示解决问题后再单击**重新获取主机信息**。
3. 确认主机满足扩容要求后，单击**下一步**。

## 第 4 步：上传安装文件

1. 在**安装文件**界面，单击**上传到 Cluster Installer**，进入安装文件上传界面。
2. 双击打开 Cluster Installer 中内置的 `md5sum.txt` 文件，检查文件中是否已包含本次扩容所需安装文件的 MD5 信息。如果有未添加的 MD5 信息，请手动输入对应安装文件的 MD5 信息，格式为 `md5sum + 空格 + 文件名`。

   > **注意**：
   >
   > 请勿更改 MD5 汇总表的文件名及文件格式，否则将导致校验 MD5 步骤出错。
3. 单击安装文件上传界面右上角的上传按钮，在本地计算机中选择所需的安装文件进行上传。
4. 返回**安装文件**界面，单击**刷新**，然后根据需要选择安装文件。
5. （可选）如果待扩容集群启用了 RDMA 且待添加主机的配置支持 RDMA，系统将自动勾选**为存储网络启用 RDMA**，请上传以下文件。

   - **MFT vib 软件包**：软件包名称必须以 `mft` 或 `Mellanox-MFT-Tools` 开头。
   - **NMST vib 软件包**：软件包名称必须以 `nmst` 或 `Mellanox-NATIVE-NMST` 开头。
   - **网卡固件文件**（仅当 RDMA 网卡是 MT27710 Family [ConnectX-4 Lx] 25Gb 网卡，且固件版本高于 14.26.4012 时展示）：请根据界面提示选择上传网卡固件文件或者手动执行固件降级。如果选择上传固件文件，则文件名必须以 `fw-ConnectX4Lx-rel` 开头。
6. 单击**下一步**。

## 第 5 步：输入配置信息

### 配置存储

为待添加主机的物理盘选择实际规划的用途。

系统将为不包含 ESXi 系统盘的存储控制器开启直通模式。

### 配置 ESXi 主机

为待添加主机设置 ESXi 主机名，使 ESXi 主机在 vCenter Server 资源列表中更有辨识度。

如果在安装 ESXi 阶段已给待添加主机设置了 ESXi 主机名，此处将显示已设置的主机名，您也可以修改主机名。

### 配置 SCVM

为待添加主机设置 SCVM 名称和 SCVM 主机名。

- SCVM 名称：SCVM 虚拟机的名称，在 vCenter Server 的虚拟机列表中可使用此名称查看 SCVM 虚拟机。
- SCVM 主机名：SMTX OS 集群中 SCVM 所在节点的名称，在 CloudTower 或 Web 控制台中可使用此名称查看集群节点。

### 配置 SCVM 密码

当 SMTX OS 集群为 6.1.1 及以上版本时，请为待添加的 SCVM 统一设置 root 账户和 smartx 账户的密码。

### 配置网络

#### 配置标准虚拟交换机

请参考以下步骤分别配置每个虚拟交换机。

1. 分别为虚拟交换机和其关联网络选择所需的负载均衡模式。
2. （可选）如果待扩容集群的虚拟交换机中的关联网络已配置了 VLAN ID，请输入与集群中其他主机一致的 VLAN ID。
3. 为每个待添加主机选择用于关联网络的网络适配器。
   - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网络适配器。
   - 如果关联网络中包含 SCVM 存储网络且该网络已启用 RDMA 功能，当给同一个主机分配了多个网络适配器时，需要设置备用适配器，并需要确保所选的网络适配器均来自同一张支持 RDMA 功能的网卡。
   - 若各个主机需要选择的网络适配的名称相同，可以在选择完一个主机的网络适配器后，在选框右侧单击 **...** > **在其他主机上选择同名适配器**。
4. （可选）如果关联网络中包含 SCVM 存储网络且该网络已启用 RDMA 功能，请选择待扩容集群使用的流量控制方式。
   > **注意**：
   >
   > 在执行扩容前，需确保已手动在物理交换机端配置相同方式的流量控制。

#### 配置网络 IP

**注意事项**

以下仅介绍为待添加主机配置 IP 的步骤。子网掩码和网关的设置已由系统自动从待扩容集群中获取并填写完成，不建议修改，否则将变更集群的子网掩码和网关。

**操作步骤**

1. 为待添加主机输入实际规划的 SCVM 管理 IP、SCVM 存储 IP、ESXi 存储 IP。
2. （可选）如果启用了 RDMA 功能，请为待添加主机输入 VMware 接入 IP。

### 挂载 NFS 数据存储

如果需要为待添加主机挂载待扩容集群中已有的 NFS 数据存储，可以在下拉列表中选择所需的 NFS 数据存储。否则请关闭**挂载 NFS 数据存储**，后续再参考《SMTX OS 集群安装部署指南》的“创建 NFS 数据存储并挂载至 ESXi 主机“章节为主机手动创建和挂载 NFS 存储。

### 关联 IPMI

强烈建议关联 IPMI，以便在 CloudTower 或 Web 控制台上管理集群时使用以下功能：

- 机箱拓扑，包括主机和物理盘定位；
- 物理盘闪灯；
- 主机风扇、CPU 温度和电源监控；

如果关闭**关联 IPMI**，后续您也可在 CloudTower 的集群的管理界面单击**设置** > **IPMI 信息**进行配置，或者在 Web 控制台中单击**设置** > **IPMI 信息**进行配置。

**操作步骤**

输入各个主机的 IPMI 管理台的 IP 地址、管理员用户名及密码。

## 第 6 步：执行扩容

1. 配置信息填写完成后，单击**核查信息**。系统将自动检查信息是否已填写，格式是否正确。
   - 如果通过检查，**核查信息**按钮将变为**执行扩容**。
   - 如果未通过检查，系统将自动提示错误，请根据提示修改或补充信息，再单击**核查信息**。
2. 通过检查后，单击**执行扩容**。系统将自动检查 Cluster Installer 是否支持运行扩容工作。
   - 如果通过检查，弹出的对话框中将不会有错误提示。
   - 如果未通过检查，弹出的对话框中将有无法运行安装扩容工作的提示，请根据提示解决问题后重试。
3. （可选）当待扩容集群的管理网络和存储网络采用分离式部署模式时，为避免由于网络不通导致扩容失败，可以在**执行扩容**对话框中，单击**检查存储网络连通性**。系统将为存储网络所在的虚拟交换机的所有网络适配器配置 ESXi 存储 IP，并检查 IP 间是否能连通。
   - 如果通过检查，对话框中将提示“所有主机上连接正常的物理适配器的存储网络已正常连通。”
   - 如果未通过检查，对话框中将提示检查不通过，可以根据表格中展示的具体连通情况排查原因，解决问题后，再重新检查连通性。
4. 通过检查后，单击**执行扩容**。系统将自动跳转到**自动化执行**界面，并自动检查配置信息是否满足扩容条件。
   - 如果通过检查，系统将自动执行扩容。

     开始执行扩容后，**自动化执行**界面将展示扩容的总体进度。您可以单击**按目录查看日志**查看当前 workflow 的日志目录，目录按照主机粒度对 SCVM、tower、zbs-deploy-server、workflow 进行了归类，方便失败后排查。

     如果需要停止扩容，可以在**自动化执行**界面右上角单击 **...** > **停止扩容**。停止后如需重新执行，系统将会在所有主机上重新执行扩容。
   - 如果未通过检查，例如检查到部分 IP 已被占用，界面将有错误提示，请根据提示修改配置信息后重新执行扩容。

## 第 7 步：检查扩容结果

执行结束后，在**自动化执行**界面可以查看 SMTX OS 集群的扩容结果。

- 如果扩容成功，界面将提示集群扩容成功，您可以选择进行以下操作：
  - **打开 CloudTower**：如果待扩容集群已关联 CloudTower，可单击该项访问 CloudTower 进行集群管理。
  - **打开 vCenter Server**：如果待扩容集群已关联 vCenter Server，可单击该项访问 vCenter Server 进行集群管理。
  - **打开集群 Web 控制台**：如果待扩容集群未关联 CloudTower 或 vCenter Server，可单击该项访问 Web 控制台进行集群管理。
  - **查看项目配置**：单击该项可查看此次项目中填写的配置信息。
- 如果扩容失败，扩容任务将会被终止，可根据具体的报错及日志信息参考 [Q&A](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_46) 排查导致失败的原因，解决问题后，可参考以下说明重新执行扩容。
  - 如果无需修改配置信息，请在当前界面单击**重新执行**。系统将从上一次失败的步骤开始执行。
  - 如果需要修改配置信息，请在当前界面单击**修改配置信息**返回**配置信息**界面进行修改，然后再重新执行扩容。

---

## 在物理服务器上安装 SMTX OS（ELF 平台）

# 在物理服务器上安装 SMTX OS（ELF 平台）

本章节介绍了使用 Cluster Installer 在物理服务器上安装 SMTX OS 的要求和操作步骤，完成安装后需手动部署 SMTX OS 集群，可参考《SMTX OS 集群安装部署指南（ELF 平台）》中的“部署 SMTX OS 集群”章节。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 安装 SMTX OS 的要求

# 安装 SMTX OS 的要求

使用 Cluster Installer 在物理服务器上安装 SMTX OS 之前，需要先确保现场安装部署环境满足构建 SMTX OS 集群的基本要求，再确保其满足使用 Cluster Installer 的要求。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 安装 SMTX OS 的要求 > 构建 SMTX OS 集群的基本要求

# 构建 SMTX OS 集群的基本要求

请参考目标 SMTX OS 集群版本的《SMTX OS 集群安装部署指南》确认现场安装部署环境满足构建 SMTX OS 集群的要求，并规划 SMTX OS 网络。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 安装 SMTX OS 的要求 > 使用 Cluster Installer 的要求

# 使用 Cluster Installer 的要求

请确认现场安装部署环境满足以下对使用 Cluster Installer 的要求。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 安装 SMTX OS 的要求 > 使用 Cluster Installer 的要求 > Cluster Installer 所在虚拟机的运行环境要求

# Cluster Installer 所在虚拟机的运行环境要求

Cluster Installer 部署在虚拟机中，该虚拟机需运行在已安装虚拟机管理程序的服务器、个人电脑或集群主机中，当前仅支持以下类型。

- ESXi 主机；
- 已安装如下虚拟机管理软件的个人电脑：

  - VMware Workstation：14 pro 及以上版本；
  - Oracle VirtualBox：6.0 及以上版本。
  > **注意：**
  >
  > 为确保软件能成功安装，建议在安装前先在本地计算机的 BIOS/固件设置中启用 Intel VT-x，然后重启计算机。
- 5.0.5 及以上版本的 SMTX OS（ELF）集群中的主机。
- SMTX ELF 集群中的主机（已配置关联存储）。

此外，以上服务器、个人电脑和集群主机还需满足以下要求：

- CPU 架构为 x86\_64；
- 有足够的资源空间：
  - 至少 2 个 CPU；
  - 至少 64 GB 存储空间；
  - 至少 2 GB 内存，但对于 SMTX OS（ELF）集群中的主机，则需预留至少 3 GiB 内存。
- 对于个人电脑，其使用的物理网卡速率必须大于或等于 1 Gbps。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 安装 SMTX OS 的要求 > 使用 Cluster Installer 的要求 > 软件版本要求

# 软件版本要求

对于在物理服务器上安装 SMTX OS 所使用的软件，需要满足 Cluster Installer 配套说明中对 SMTX OS 软件版本的要求。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 安装 SMTX OS 的要求 > 使用 Cluster Installer 的要求 > 待部署 SMTX OS 集群的服务器要求

# 待部署 SMTX OS 集群的服务器要求

待安装部署 SMTX OS 集群的服务器需要满足[配套的服务器](/clusterinstaller/1.4.1/installer_release_notes/cluster_installer_release_notes_02#%E9%85%8D%E5%A5%97%E7%9A%84%E6%9C%8D%E5%8A%A1%E5%99%A8)要求。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 安装 SMTX OS 的要求 > 使用 Cluster Installer 的要求 > 浏览器版本要求

# 浏览器版本要求

借助 Cluster Installer 在物理服务器上安装 SMTX OS 的过程中需要使用 Web 浏览器，为保证兼容性，建议使用 Chrome 80 或 Firefox 78 及以上版本的浏览器，并启用 Cookie 和 JavaScript。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 安装 SMTX OS 的要求 > 使用 Cluster Installer 的要求 > 网络连通要求

# 网络连通要求

借助 Cluster Installer 在物理服务器上安装 SMTX OS 时，需要确保 Cluster Installer 的网络环境及 IP 均满足如下要求。

- Cluster Installer 网络环境要求：

  - 若在 ESXi 主机、SMTX OS 集群或 SMTX ELF 集群安装 Cluster Installer，需保证主机或集群中有可连通待部署集群的服务器 IPMI 网络的虚拟机网络，且虚拟机网络的带宽必须大于或等于 1 Gbps。
  - 若在个人电脑中安装 Cluster Installer，需保证个人电脑可与待部署集群的服务器 IPMI 网络连通。
- Cluster Installer IP 要求：Cluster Installer IP 与待部署集群的 IPMI IP 互相连通。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 安装 SMTX OS 的要求 > 使用 Cluster Installer 的要求 > 防火墙端口开放要求

# 防火墙端口开放要求

| 源端 | 目标端 | 目标端需开放端口 | 端口说明 |
| --- | --- | --- | --- |
| 浏览器客户端 IP | Cluster Installer IP | TCP 80 | 用于浏览器 Web 访问 Cluster Installer |
| Cluster Installer IP | 服务器 IPMI IP | TCP 443 | BMC Redfish/HTTPS API 端口 |
| UDP 623 | IPMI 协议端口，用于获取服务器 FRU 信息、SOL 串口输出 |
| TCP 22 | 如果服务器的 BMC 为 Huawei iBMC 或 Dell iDRAC 且iDRAC 版本低于 4.0，需要通过 SSH 登录到 BMC 挂载 ISO 文件 |
| 服务器 IPMI IP | Cluster Installer IP | Cluster Installer 虚拟机 NFS Server 端口\* | NFS 访问端口，BMC 需要通过 NFS 协议挂载 Cluster Installer 虚拟机里的 ISO 文件 |
| TCP 80 | 如果服务器的 BMC 为 HPE iLO5，需开放此端口 |

> **说明**：
>
> Cluster Installer 虚拟机 NFS Server 端口（表中有星号 \* 标记的端口）除了 `2049` 和 `111` 两个固定端口外，其他端口均为随机端口。在创建完 Cluster Installer 虚拟机并配置完 IP 后，您才能查看 NFS Server 使用了哪些随机端口，同时您也可以选择自定义除 111 端口外的其他 NFS Server 端口，建议参考上述要求提前规划。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 创建 Cluster Installer 虚拟机

# 创建 Cluster Installer 虚拟机

您可以根据当前环境选择在 ESXi 主机、SMTX OS（ELF）集群的主机、或者个人电脑中创建 Cluster Installer 虚拟机。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 创建 Cluster Installer 虚拟机 > 在 ESXi 主机中创建

# 在 ESXi 主机中创建

在 ESXi 主机中创建 Cluster Installer 虚拟机时，可以选择直接登录 ESXi 主机进行创建或者在 vCenter Server 的 ESXi 主机中创建。

**注意事项**

Cluster Installer 虚拟机的名称不能包含除下划线 `_`、减号 `-`、点 `.` 以外的特殊字符，否则会导致安装程序出错。

## 直接登录 ESXi 主机进行创建

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 登录 ESXi 主机的 Web 管理页面，打开**创建/注册虚拟机**，选择**从 OVF 或 OVA 文件部署虚拟机**，单击**下一步**。
3. 输入虚拟机的名称，打开**单击以选择文件或拖放**，选择已下载至本地计算机上的 OVA 文件，单击**下一步**。
4. 为虚拟机的配置文件及其虚拟磁盘选择数据存储，单击**下一步**。
5. 在部署选项设置中，将网络映射 nic0 设置为符合网络连通要求的虚拟机网络，然后依次单击**下一步**完成配置。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_33.png)

## 在 vCenter Server 中的 ESXi 主机中创建

**注意事项**

若 vCenter 集群需要开启 EVC 特性，请先开启 EVC 特性，再安装 Cluster Installer 虚拟机。

**操作步骤**

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 登录 vCenter Server 的 Web 管理界面，定位到用于部署 Cluster Installer 虚拟机的 ESXi 主机，右键单击该主机，并选择**部署 OVF 模板**。
3. 选择**本地文件**，单击**上传文件**，上传已下载至本地计算机上的 OVA 文件。
4. 依次输入虚拟机名称、选择虚拟机安装位置、选择计算机资源、选择存储。
5. 在选择网络配置中，将网络映射 nic0 设置为符合网络连通要求的虚拟机网络，并完成后续配置。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_11.png)

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 创建 Cluster Installer 虚拟机 > 在 SMTX OS（ELF）集群或 SMTX ELF 集群的主机中创建

# 在 SMTX OS（ELF）集群或 SMTX ELF 集群的主机中创建

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 重命名该 OVA 文件，将文件名后缀 `.ova` 修改为 `.tar`，并解压该文件。
3. 登录 CloudTower，单击**创建** > **导入虚拟机**。
4. 在**导入虚拟机**界面中，选择安装 Cluster Installer 的集群和主机，并将已解压的对应文件上传至在**模板信息**区。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_67.png)
5. 在**计算资源**配置界面，将内存分配设置为 **3 GiB**。
6. 在**磁盘**配置界面，将总线类型设置为 **VIRTIO**，选择其他类型会导致虚拟机无法正常启动。
7. 在**虚拟网卡**界面，选择符合网络连通要求的虚拟机网络。
8. 在**其他**配置页面，选择**创建完成后自动开机**，单击**确定**。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 创建 Cluster Installer 虚拟机 > 在个人电脑中创建

# 在个人电脑中创建

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 根据个人电脑中所安装的虚拟机管理软件类型参考对应步骤创建 Cluster Installer 虚拟机。
   - **在 VMware Workstation 中创建**
     1. 在 VMware Workstation 单击**导入虚拟机**，导入已下载的 OVA 模板文件，输入新虚拟机名称以及 OVA 文件所在的存储路径。请确保存储路径所在分区的剩余可用空间不小于 64 GB。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_04.png)
     2. 在**编辑**菜单中单击**虚拟网络编辑器**，选择**更改设置**，选择 VMnet0 的桥接模式，在**已桥接至**下拉列表中选择本地计算机所使用的物理网卡。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_07.png)
     3. 打开 Cluster Installer 的**虚拟机设置**，确认网络连接模式为**桥接模式**。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_08.png)
   - **在 Oracle VirtualBox 中创建**
     1. 在 VirtualBox 中单击**管理**菜单，选择**导入虚拟机电脑**，选择 OVA 文件所在的存储路径，并确认**默认虚拟机电脑位置**所在分区的剩余可用空间不小于 64 GB。

        导入时将 MAC 地址设定设置为**为所有网卡重新生成 MAC 地址**。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_09.png)
     2. 导入虚拟机后，打开虚拟机设置页面，确保网卡 1 的连接方式为**桥接网卡**。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_10.png)

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 配置 Cluster Installer IP

# 配置 Cluster Installer IP

创建 Cluster Installer 虚拟机后，需要为虚拟机配置 IP 地址。下文以 VMware Workstation 为例介绍配置步骤。

**操作步骤**

1. 打开 VMware Workstation，在**我的计算机**中，选择已创建的 Cluster Installer 虚拟机单击**开启此虚拟机**。
2. 配置虚拟机的 IP 地址。

   - 如果虚拟机桥接网络内有 DHCP 服务器，Cluster Installer 会通过 DHCP 服务器自动获取 IP 地址，并显示在虚拟机控制台。

     ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_12.png)
   - 如果虚拟机桥接网络内没有 DHCP 服务器，则请执行以下操作。

     1. 打开 `/etc/sysconfig/network-scripts/ifcfg-eth0` 文件，设置静态 IP。
     2. 重启 Cluster Installer 虚拟机。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_13.png)
3. 执行 `prepare.sh` 命令检查虚拟机内的服务是否正常运行。

   当时输出结果显示 `Failed: 0` 和 `Skipped: 0` 时，表示服务正常运行。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_14.png)

   - 如果服务正常运行，则可以正常使用 Cluster Installer 。
   - 如果服务未正常运行，排查完原因后，若需要变更 Cluster Installer 所在的网络和修改 IP 地址，请从上一步开始重新执行操作。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 开放 NFS Server 端口

# 开放 NFS Server 端口

1. 登录 Cluster Installer 虚拟机，执行以下命令查看 NFS Server 当前使用的所有端口信息。

   ```
   rpcinfo -p
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_80.png)
2. （可选）如果需要自定义 NFS Server 端口，请执行以下步骤。

   1. 执行以下命令，然后根据提示输入实际规划的新端口。如果不需要修改某端口，可以直接按 Enter 键跳过该端口的设置。

      ```
      /root/deploy/tools/update_nfs_ports.sh
      ```

      ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_82.png)
   2. 执行以下命令，确认端口已修改成功。

      ```
      rpcinfo -p
      ```

      ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_83.png)
3. 执行以下命令，查看需要开放的 NFS Server 端口。

   ```
   rpcinfo -p | awk '{print $3,$4}' | sort -u
   ```
4. 参考防火墙端口开放要求，为 Cluster Installer 虚拟机开放 NFS Server 端口。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 检查服务器的 BMC 和 BIOS 设置

# 检查服务器的 BMC 和 BIOS 设置

使用 Cluster Installer 在物理服务器上安装 ESXi、SMTX OS、SMTX ELF 或 SMTX ZBS 时，需依赖服务器的 BMC（基板管理控制器）对服务器执行开机、重启、挂载 ISO、卸载 ISO、获取 Console 输出等操作，因此在安装前，需参考下文检查服务器的 BMC 和 BIOS 设置，确保已启用以下功能：

- Redfish 或 HTTPS 访问功能；
- IPMI Over LAN 功能；
- SOL（Serial Over LAN ）功能。

**注意事项**

- 如果选择 `Avago MegaRAID` 卡上的硬盘作为服务器的启动盘，安装前需要确保 RAID 卡在 BIOS 设置里的 **Boot device** 为所选的硬盘，否则会导致 ISO 安装完后由于启动设备配置错误导致系统无法正常启动。

  ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_65.png)
- 如果服务器的 CPU 架构为鲲鹏 AArch64，需要确保服务器的 BIOS 设置里的 **CPU Prefetching Configuration** 选项为 **Enabled**，否则会影响 CPU 性能。

  ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_73.png)

## Dell iDRAC

1. 打开浏览器，在地址栏输入服务器的 IPMI 管理台 IP，登录服务器的 iDRAC 管理界面。
2. 单击 **iDRAC 设置** > **连接性** > **LAN 上串行**，将**启用 LAN 上串行**状态设置为**已启用**，然后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_51.png)
3. 单击 **iDRAC 设置** > **连接性** > **网络** >**IPMI 设置**，将**启用 LAN 上的 IPMI** 状态设置为**已启用**，然后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_52.png)
4. 单击 **iDRAC 设置** > **用户** > **本地用户**，确认本地用户的 **LAN 上串行**已启用。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_53.png)
5. 单击 **iDRAC 设置** > **服务** > **Redfish**，将 Redfish 状态设置为**已启用**，然后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_54.png)

## Lenovo XClarity

1. 打开浏览器，在浏览器的地址栏输入服务器的 IPMI 管理台 IP，登录服务器的 XClarity Controller 管理界面。
2. 单击 **BMC 配置**，然后参考下图启用 **Web Over HTTPS**、**REST Over HTTPS** 和 **IPMI over LAN**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_55.png)

## HPE iLO5

1. 打开浏览器，在浏览器的地址栏输入服务器的 IPMI 管理台 IP，登录服务器的 iLO5 管理界面。
2. 单击**安全性** > **访问设置**，然后按下图设置参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_56.png)

## Inspur BMC

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录服务器的 BMC 管理界面。
2. 单击**系统设置** > **服务**，然后按下图设置 WEB、CD-Media 和 IPMI 服务的参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_77.png)
3. 单击**系统设置** > **用户精细化管理**，然后按下图检查并确认当前用户属于 Administrator 用户组，用户已启用，且 IPMI 权限为 `administrator`。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_78.png)

## Huawei iBMC

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录服务器的 iBMC 管理界面。
2. 单击**服务管理** > **端口服务**，然后按下图设置参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_57.png)
3. 单击**用户&安全** > **本地用户**，然后按下图设置登录接口。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_58.png)
4. 单击**系统管理** > **BIOS 配置**，开启**支持 IPMI 设置启动模式**，然后将**启动模式**选项设置为**统一可扩展固件接口（UEFI）**，完成后单击**保存**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_79.png)

## Suma BMC

> **注意**：
>
> - 对于 **Suma R6240H0** 型号服务器，由于其固件存在已知问题，需要在 BIOS 中禁用 `Serial Port`，否则会导致无法正常使用 SOL 功能。禁用 `Serial Port` 方法如下：
>
>   重启服务器，进入 `BIOS Setup Utility`，将 `Advanced`>`AST2500 Super IO Configuration`>`Serial Port Configuration`>`Serial Port` 参数设置为 **Disabled**。
>
>   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_62.png)
> - 对于 **Suma H620-G30/R6230HA** 型号服务器，其 BMC 固件版本不能低于 **3.30** ，若低于 **3.30** 请联系硬件厂商进行 BMC 固件升级。
>
>   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_59.png)

1. 单击 **BMC 设置** > **服务**，然后按照下图设置 web 和 ipmi 服务的参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_60.png)
2. 单击**远程设置** > **BIOS 设置** > **管理配置**，然后按照下图设置所有参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_61.png)
3. 单击 **BMC 配置** > **用户/用户组**，然后为当前用户开启 **VMedia 访问**权限。

---

## 在物理服务器上安装 SMTX OS（ELF 平台） > 安装 SMTX OS

# 安装 SMTX OS

## 第 1 步：选择执行任务

1. 打开浏览器，在地址栏输入 Cluster Installer 的 IP 地址，输入用户名和密码，登录 Cluster Installer 的 Web 界面。
2. 在首页选择集群类型为 **SMTX OS（ELF 平台）**。
3. 在**开始新项目**界面，输入本次项目的名称，项目名称用于区分安装部署（或扩容）的内容，建议使用英文大小写字母及数字。
4. 单击**开始配置**。

## 第 2 步：获取主机信息

**注意事项**

从本步骤开始需要手动填写项目的配置信息，在填写信息的过程中请勿关闭浏览器，否则项目的配置信息将不会保留。

**操作步骤**

1. 在**集群规模**界面，输入主机数量、所有主机的 IPMI IP 地址、管理员用户名及密码。IPMI IP、管理员用户名及密码均可以批量填充。
2. 输入完成后，单击**获取主机信息**，Cluster Installer 开始查找主机并检查主机是否满足安装要求。

   - 若主机满足安装要求，界面将提示“已获取到主机 CPU 架构等信息”。可在界面中查看每个主机的 BMC、CPU 架构以及服务器型号信息。
   - 若部分信息未成功获取，可单击下拉框，根据主机的 FRU 信息，手动选择当前主机的 BMC 或 CPU 架构。
   - 若发现问题，请根据提示解决问题后单击**重新获取主机信息**。
3. 单击**下一步**，继续上传所需的安装文件。

## 第 3 步：上传安装文件

1. 在**安装文件**界面单击**上传到 Cluster Installer**，进入安装文件上传界面。
2. 双击打开 Cluster Installer 中内置的 `md5sum.txt` 文件，检查文件中是否已包含了当前使用的安装文件的 MD5 信息。若有未添加 MD5 信息的安装文件，请手动输入该安装文件的 MD5 信息，格式为 `md5sum + 空格 + 文件名`。完成添加后，保存并关闭`md5sum.txt`文件。

   > **注意**：
   >
   > 请勿更改 MD5 汇总表的文件名及文件格式，否则会导致校验 MD5 步骤出错。
3. 单击安装文件上传界面右上角上传按钮，在本地计算机中选择所需的安装文件进行上传。
4. 上传完成后，返回**安装文件**界面，单击**刷新**，然后根据需要选择安装文件。
5. 选择完成后，单击**收集硬件配置**，Cluster Installer 自动运行 LiveCD 并收集主机中的物理盘、网卡等硬件配置信息。收集过程中可单击**按目录查看日志**，确认收集进度。

   - 若主机硬件满足要求，界面将提示“已收集到主机中物理盘、网卡等硬件配置信息”。
   - 若主机硬件不满足要求，界面将提示发现的问题，解决问题后单击**重新收集硬件配置**。
6. 单击**下一步**，继续输入配置信息。

## 第 4 步：输入配置信息

在**配置信息**界面配置存储和管理网络。

### 配置存储

1. （可选）如果 SMTX OS 集群为 5.1.5 及以上的 5.1.x 版本或 6.1.1 及以上版本，请为所有主机批量选择操作系统安装方式。您也可以根据实际需求为每台主机单独选择操作系统安装方式。
2. （可选）如果 SMTX OS 集群为 6.1.1 及以上版本，请为所有主机批量选择容量规格。您也可以根据实际需求为每台主机单独选择容量规格。
3. 根据在确认 SMTX OS 集群构建要求时已规划的每块物理盘的用途，为每台主机的物理盘选择用途。

### 配置管理网络

若已确定管理网络信息，请参考如下操作进行配置。若部分管理网络信息暂时无法确定，可跳过此步骤，待安装完成后通过 Cluster Installer 在服务器操作系统中预制的管理网络信息的配置脚本完成管理网络配置。

1. 选择管理网络对应的物理网口。

   - 需要为每台主机分配一个状态为**连接正常**且速率在 1GbE 及以上的物理网口。
   - 每台主机仅允许选择一个物理网口，如需多个网口绑定使用，可在集群部署阶段添加。
2. 配置管理网络 IP 以及其对应的子网掩码、网关和 VLAN ID。

## 第 5 步：执行安装部署

1. 填写完所有配置信息后，单击**核查信息**，Cluster Installer 将对已填写的配置信息进行检查。

   - 若通过检查，**核查信息**按钮将变为**执行安装**，可以开始执行安装。
   - 若未通过检查，系统将提示错误，请根据提示对不符合要求的内容进行补充和修改。
2. 通过检查后，单击**执行安装**，此时系统将自动检查 Cluster Installer 是否支持运行安装。

   - 若可正常运行，将弹出对话框提示确认开始执行自动化安装 SMTX OS，单击对话框中的**执行安装**，进入**自动化执行**界面。
     安装过程中用户可以进行如下操作：

     - 查看安装的总体进度。
     - 按目录查看日志：单击可查看当前 workflow 的日志目录，目录中按照主机粒度进行了归类，方便出错后的进一步排查。
     - 停止安装：安装过程中，用户可随时停止安装当前任务。停止安装后，如需重新执行，将会在所有主机上重新执行安装任务。
   - 若无法运行，将弹出对话框提示检查系统日志、Cluster Installer 相关的网络和服务是否正常运行，并解决问题后重试。

## 第 6 步：检查安装结果

执行结束后，在**自动化执行**界面可以查看 SMTX OS 的安装结果。

- 若安装成功，界面将提示 **SMTX OS 安装成功**，此时：

  - **若已配置管理网络**

    可单击任一节点的管理 IP，继续手动部署集群。
  - **若未配置管理网络或有部分网络信息尚未配置**

    可进入服务器操作系统中，编辑 `/tmp/config_mgt_network.sh` 脚本文件，补充管理网络配置信息，然后执行 `bash /tmp/config_mgt_network.sh` 命令运行脚本，完成管理网络配置。
    `/tmp/config_mgt_network.sh` 脚本文件包含如下参数：

    ```
    MGT_IP=                      //管理网络 IP
    NETMASK=                     //子网掩码
    GATEWAY=                     //网关
    MGT_PNIC=                    //管理网卡名称或 MAC 地址
    VLAN=                        //管理网络的 VLAN ID
    ```
  - 可单击**查看项目配置**，查看此次项目中填写的配置信息。
- 若安装过程中任一步骤失败，安装任务将终止，请根据具体的报错及日志信息参考 [Q&A](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_46) 排查导致失败的原因，解决问题后，可参考如下说明重新执行安装。

  - 若无需修改配置信息，请在当前界面单击**重新执行**，系统将从上一次失败的步骤开始执行。
  - 若需要修改配置信息，请在当前界面单击**修改配置信息**返回**配置信息**界面进行修改，然后再重新执行安装任务。

## 第 7 步：手动部署 SMTX OS（ELF）集群

使用 Cluster Installer 完成 SMTX OS 的安装后，可参考《SMTX OS 集群安装部署指南（ELF 平台）》的“部署 SMTX OS 集群”章节，继续手动完成 SMTX OS（ELF）集群的部署。

---

## 在物理服务器上安装 SMTX ZBS

# 在物理服务器上安装 SMTX ZBS

本章节介绍了使用 Cluster Installer 在物理服务器上安装 SMTX ZBS 的要求和操作步骤，完成安装后需手动部署 SMTX ZBS 集群，可参考《SMTX ZBS 安装部署指南》中的“部署 SMTX ZBS 集群”章节。

---

## 在物理服务器上安装 SMTX ZBS > 安装 SMTX ZBS 的要求

# 安装 SMTX ZBS 的要求

使用 Cluster Installer 在物理服务器上安装 SMTX ZBS 之前，需要先确保现场安装部署环境满足构建 SMTX ZBS 集群的基本要求，再确保其满足使用 Cluster Installer 的要求。

---

## 在物理服务器上安装 SMTX ZBS > 安装 SMTX ZBS 的要求 > 构建 SMTX ZBS 集群的基本要求

# 构建 SMTX ZBS 集群的基本要求

请参考目标 SMTX ZBS 集群版本的《SMTX ZBS 安装部署指南》确认现场安装部署环境满足构建 SMTX ZBS 集群的要求，并规划 SMTX ZBS 网络。

---

## 在物理服务器上安装 SMTX ZBS > 安装 SMTX ZBS 的要求 > 使用 Cluster Installer 的要求

# 使用 Cluster Installer 的要求

请确认现场安装部署环境满足以下对使用 Cluster Installer 的要求。

---

## 在物理服务器上安装 SMTX ZBS > 安装 SMTX ZBS 的要求 > 使用 Cluster Installer 的要求 > Cluster Installer 所在虚拟机的运行环境要求

# Cluster Installer 所在虚拟机的运行环境要求

Cluster Installer 部署在虚拟机中，该虚拟机需运行在已安装虚拟机管理程序的服务器、个人电脑或集群主机中，当前仅支持以下类型。

- ESXi 主机；
- 已安装如下虚拟机管理软件的个人电脑：

  - VMware Workstation：14 pro 及以上版本；
  - Oracle VirtualBox：6.0 及以上版本。
  > **注意：**
  >
  > 为确保软件能成功安装，建议在安装前先在本地计算机的 BIOS/固件设置中启用 Intel VT-x，然后重启计算机。
- 5.0.5 及以上版本的 SMTX OS（ELF）集群中的主机。
- SMTX ELF 集群中的主机（已配置关联存储）。

此外，以上服务器、个人电脑和集群主机还需满足以下要求：

- CPU 架构为 x86\_64；
- 有足够的资源空间：
  - 至少 2 个 CPU；
  - 至少 64 GB 存储空间；
  - 至少 2 GB 内存，但对于 SMTX OS（ELF）集群中的主机，则需预留至少 3 GiB 内存。
- 对于个人电脑，其使用的物理网卡速率必须大于或等于 1 Gbps。

---

## 在物理服务器上安装 SMTX ZBS > 安装 SMTX ZBS 的要求 > 使用 Cluster Installer 的要求 > 软件版本要求

# 软件版本要求

在物理服务器上安装 SMTX ZBS 所使用的软件需要满足 Cluster Installer 版本配套说明中对 SMTX ZBS 软件版本的要求。

---

## 在物理服务器上安装 SMTX ZBS > 安装 SMTX ZBS 的要求 > 使用 Cluster Installer 的要求 > 待部署 SMTX ZBS 集群的服务器要求

# 待部署 SMTX ZBS 集群的服务器要求

待安装部署 SMTX ZBS 集群的服务器需要满足[配套的服务器](/clusterinstaller/1.4.1/installer_release_notes/cluster_installer_release_notes_02#%E9%85%8D%E5%A5%97%E7%9A%84%E6%9C%8D%E5%8A%A1%E5%99%A8)要求。

---

## 在物理服务器上安装 SMTX ZBS > 安装 SMTX ZBS 的要求 > 使用 Cluster Installer 的要求 > 浏览器版本要求

# 浏览器版本要求

借助 Cluster Installer 在物理服务器上安装 SMTX ZBS 的过程中需要使用 Web 浏览器，为保证兼容性，建议使用 Chrome 80 或 Firefox 78 及以上版本的浏览器，并启用 Cookie 和 JavaScript。

---

## 在物理服务器上安装 SMTX ZBS > 安装 SMTX ZBS 的要求 > 使用 Cluster Installer 的要求 > 网络连通要求

# 网络连通要求

借助 Cluster Installer 在物理服务器上安装 SMTX ZBS 时，需要确保 Cluster Installer 的网络环境及 IP 均满足如下要求。

- Cluster Installer 网络环境要求：

  - 若在 ESXi 主机、SMTX OS 集群或 SMTX ELF 集群安装 Cluster Installer，需保证主机或集群中有可连通待部署集群的服务器 IPMI 网络的虚拟机网络，且虚拟机网络的带宽必须大于或等于 1 Gbps。
  - 若在个人电脑安装 Cluster Installer，需保证个人电脑已与待部署集群的服务器 IPMI 网络连通。
- Cluster Installer IP 要求：
  集群安装工具 IP 与待部署集群的 IPMI IP 互相连通。

---

## 在物理服务器上安装 SMTX ZBS > 安装 SMTX ZBS 的要求 > 使用 Cluster Installer 的要求 > 防火墙端口开放要求

# 防火墙端口开放要求

| 源端 | 目标端 | 目标端需开放端口 | 端口说明 |
| --- | --- | --- | --- |
| 浏览器客户端 IP | Cluster Installer IP | TCP 80 | 用于浏览器 Web 访问 Cluster Installer |
| Cluster Installer IP | 服务器 IPMI IP | TCP 443 | BMC Redfish/HTTPS API 端口 |
| UDP 623 | IPMI 协议端口，用于获取服务器 FRU 信息、SOL 串口输出 |
| TCP 22 | 如果服务器的 BMC 为 Huawei iBMC 或 Dell iDRAC 且iDRAC 版本低于 4.0，需要通过 SSH 登录到 BMC 挂载 ISO 文件 |
| 服务器 IPMI IP | Cluster Installer IP | Cluster Installer 虚拟机 NFS Server 端口\* | NFS 访问端口，BMC 需要通过 NFS 协议挂载 Cluster Installer 虚拟机里的 ISO 文件 |
| TCP 80 | 如果服务器的 BMC 为 HPE iLO5，需开放此端口 |

> **说明**：
>
> Cluster Installer 虚拟机 NFS Server 端口（表中有星号 \* 标记的端口）除了 `2049` 和 `111` 两个固定端口外，其他端口均为随机端口。在创建完 Cluster Installer 虚拟机并配置完 IP 后，您才能查看 NFS Server 使用了哪些随机端口，同时您也可以选择自定义除 111 端口外的其他 NFS Server 端口，建议参考上述要求提前规划。

---

## 在物理服务器上安装 SMTX ZBS > 创建 Cluster Installer 虚拟机

# 创建 Cluster Installer 虚拟机

您可以根据当前环境选择在 ESXi 主机、SMTX OS（ELF）集群的主机、或者个人电脑中创建 Cluster Installer 虚拟机。

---

## 在物理服务器上安装 SMTX ZBS > 创建 Cluster Installer 虚拟机 > 在 ESXi 主机中创建

# 在 ESXi 主机中创建

在 ESXi 主机中创建 Cluster Installer 虚拟机时，可以选择直接登录 ESXi 主机进行创建或者在 vCenter Server 的 ESXi 主机中创建。

**注意事项**

Cluster Installer 虚拟机的名称不能包含除下划线 `_`、减号 `-`、点 `.` 以外的特殊字符，否则会导致安装程序出错。

## 直接登录 ESXi 主机进行创建

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 登录 ESXi 主机的 Web 管理页面，打开**创建/注册虚拟机**，选择**从 OVF 或 OVA 文件部署虚拟机**，单击**下一步**。
3. 输入虚拟机的名称，打开**单击以选择文件或拖放**，选择已下载至本地计算机上的 OVA 文件，单击**下一步**。
4. 为虚拟机的配置文件及其虚拟磁盘选择数据存储，单击**下一步**。
5. 在部署选项设置中，将网络映射 nic0 设置为符合网络连通要求的虚拟机网络，然后依次单击**下一步**完成配置。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_33.png)

## 在 vCenter Server 中的 ESXi 主机中创建

**注意事项**

若 vCenter 集群需要开启 EVC 特性，请先开启 EVC 特性，再安装 Cluster Installer 虚拟机。

**操作步骤**

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 登录 vCenter Server 的 Web 管理界面，定位到用于部署 Cluster Installer 虚拟机的 ESXi 主机，右键单击该主机，并选择**部署 OVF 模板**。
3. 选择**本地文件**，单击**上传文件**，上传已下载至本地计算机上的 OVA 文件。
4. 依次输入虚拟机名称、选择虚拟机安装位置、选择计算机资源、选择存储。
5. 在选择网络配置中，将网络映射 nic0 设置为符合网络连通要求的虚拟机网络，并完成后续配置。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_11.png)

---

## 在物理服务器上安装 SMTX ZBS > 创建 Cluster Installer 虚拟机 > 在 SMTX OS（ELF）集群或 SMTX ELF 集群的主机中创建

# 在 SMTX OS（ELF）集群或 SMTX ELF 集群的主机中创建

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 重命名该 OVA 文件，将文件名后缀 `.ova` 修改为 `.tar`，并解压该文件。
3. 登录 CloudTower，单击**创建** > **导入虚拟机**。
4. 在**导入虚拟机**界面中，选择安装 Cluster Installer 的集群和主机，并将已解压的对应文件上传至在**模板信息**区。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_67.png)
5. 在**计算资源**配置界面，将内存分配设置为 **3 GiB**。
6. 在**磁盘**配置界面，将总线类型设置为 **VIRTIO**，选择其他类型会导致虚拟机无法正常启动。
7. 在**虚拟网卡**界面，选择符合网络连通要求的虚拟机网络。
8. 在**其他**配置页面，选择**创建完成后自动开机**，单击**确定**。

---

## 在物理服务器上安装 SMTX ZBS > 创建 Cluster Installer 虚拟机 > 在个人电脑中创建

# 在个人电脑中创建

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 根据个人电脑中所安装的虚拟机管理软件类型参考对应步骤创建 Cluster Installer 虚拟机。
   - **在 VMware Workstation 中创建**
     1. 在 VMware Workstation 单击**导入虚拟机**，导入已下载的 OVA 模板文件，输入新虚拟机名称以及 OVA 文件所在的存储路径。请确保存储路径所在分区的剩余可用空间不小于 64 GB。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_04.png)
     2. 在**编辑**菜单中单击**虚拟网络编辑器**，选择**更改设置**，选择 VMnet0 的桥接模式，在**已桥接至**下拉列表中选择本地计算机所使用的物理网卡。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_07.png)
     3. 打开 Cluster Installer 的**虚拟机设置**，确认网络连接模式为**桥接模式**。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_08.png)
   - **在 Oracle VirtualBox 中创建**
     1. 在 VirtualBox 中单击**管理**菜单，选择**导入虚拟机电脑**，选择 OVA 文件所在的存储路径，并确认**默认虚拟机电脑位置**所在分区的剩余可用空间不小于 64 GB。

        导入时将 MAC 地址设定设置为**为所有网卡重新生成 MAC 地址**。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_09.png)
     2. 导入虚拟机后，打开虚拟机设置页面，确保网卡 1 的连接方式为**桥接网卡**。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_10.png)

---

## 在物理服务器上安装 SMTX ZBS > 配置 Cluster Installer IP

# 配置 Cluster Installer IP

创建 Cluster Installer 虚拟机后，需要为虚拟机配置 IP 地址。下文以 VMware Workstation 为例介绍配置步骤。

**操作步骤**

1. 打开 VMware Workstation，在**我的计算机**中，选择已创建的 Cluster Installer 虚拟机单击**开启此虚拟机**。
2. 配置虚拟机的 IP 地址。

   - 如果虚拟机桥接网络内有 DHCP 服务器，Cluster Installer 会通过 DHCP 服务器自动获取 IP 地址，并显示在虚拟机控制台。

     ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_12.png)
   - 如果虚拟机桥接网络内没有 DHCP 服务器，则请执行以下操作。

     1. 打开 `/etc/sysconfig/network-scripts/ifcfg-eth0` 文件，设置静态 IP。
     2. 重启 Cluster Installer 虚拟机。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_13.png)
3. 执行 `prepare.sh` 命令检查虚拟机内的服务是否正常运行。

   当时输出结果显示 `Failed: 0` 和 `Skipped: 0` 时，表示服务正常运行。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_14.png)

   - 如果服务正常运行，则可以正常使用 Cluster Installer 。
   - 如果服务未正常运行，排查完原因后，若需要变更 Cluster Installer 所在的网络和修改 IP 地址，请从上一步开始重新执行操作。

---

## 在物理服务器上安装 SMTX ZBS > 开放 NFS Server 端口

# 开放 NFS Server 端口

1. 登录 Cluster Installer 虚拟机，执行以下命令查看 NFS Server 当前使用的所有端口信息。

   ```
   rpcinfo -p
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_80.png)
2. （可选）如果需要自定义 NFS Server 端口，请执行以下步骤。

   1. 执行以下命令，然后根据提示输入实际规划的新端口。如果不需要修改某端口，可以直接按 Enter 键跳过该端口的设置。

      ```
      /root/deploy/tools/update_nfs_ports.sh
      ```

      ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_82.png)
   2. 执行以下命令，确认端口已修改成功。

      ```
      rpcinfo -p
      ```

      ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_83.png)
3. 执行以下命令，查看需要开放的 NFS Server 端口。

   ```
   rpcinfo -p | awk '{print $3,$4}' | sort -u
   ```
4. 参考防火墙端口开放要求，为 Cluster Installer 虚拟机开放 NFS Server 端口。

---

## 在物理服务器上安装 SMTX ZBS > 检查服务器的 BMC 和 BIOS 设置

# 检查服务器的 BMC 和 BIOS 设置

使用 Cluster Installer 在物理服务器上安装 ESXi、SMTX OS、SMTX ELF 或 SMTX ZBS 时，需依赖服务器的 BMC（基板管理控制器）对服务器执行开机、重启、挂载 ISO、卸载 ISO、获取 Console 输出等操作，因此在安装前，需参考下文检查服务器的 BMC 和 BIOS 设置，确保已启用以下功能：

- Redfish 或 HTTPS 访问功能；
- IPMI Over LAN 功能；
- SOL（Serial Over LAN ）功能。

**注意事项**

- 如果选择 `Avago MegaRAID` 卡上的硬盘作为服务器的启动盘，安装前需要确保 RAID 卡在 BIOS 设置里的 **Boot device** 为所选的硬盘，否则会导致 ISO 安装完后由于启动设备配置错误导致系统无法正常启动。

  ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_65.png)
- 如果服务器的 CPU 架构为鲲鹏 AArch64，需要确保服务器的 BIOS 设置里的 **CPU Prefetching Configuration** 选项为 **Enabled**，否则会影响 CPU 性能。

  ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_73.png)

## Dell iDRAC

1. 打开浏览器，在地址栏输入服务器的 IPMI 管理台 IP，登录服务器的 iDRAC 管理界面。
2. 单击 **iDRAC 设置** > **连接性** > **LAN 上串行**，将**启用 LAN 上串行**状态设置为**已启用**，然后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_51.png)
3. 单击 **iDRAC 设置** > **连接性** > **网络** >**IPMI 设置**，将**启用 LAN 上的 IPMI** 状态设置为**已启用**，然后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_52.png)
4. 单击 **iDRAC 设置** > **用户** > **本地用户**，确认本地用户的 **LAN 上串行**已启用。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_53.png)
5. 单击 **iDRAC 设置** > **服务** > **Redfish**，将 Redfish 状态设置为**已启用**，然后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_54.png)

## Lenovo XClarity

1. 打开浏览器，在浏览器的地址栏输入服务器的 IPMI 管理台 IP，登录服务器的 XClarity Controller 管理界面。
2. 单击 **BMC 配置**，然后参考下图启用 **Web Over HTTPS**、**REST Over HTTPS** 和 **IPMI over LAN**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_55.png)

## HPE iLO5

1. 打开浏览器，在浏览器的地址栏输入服务器的 IPMI 管理台 IP，登录服务器的 iLO5 管理界面。
2. 单击**安全性** > **访问设置**，然后按下图设置参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_56.png)

## Inspur BMC

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录服务器的 BMC 管理界面。
2. 单击**系统设置** > **服务**，然后按下图设置 WEB、CD-Media 和 IPMI 服务的参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_77.png)
3. 单击**系统设置** > **用户精细化管理**，然后按下图检查并确认当前用户属于 Administrator 用户组，用户已启用，且 IPMI 权限为 `administrator`。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_78.png)

## Huawei iBMC

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录服务器的 iBMC 管理界面。
2. 单击**服务管理** > **端口服务**，然后按下图设置参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_57.png)
3. 单击**用户&安全** > **本地用户**，然后按下图设置登录接口。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_58.png)
4. 单击**系统管理** > **BIOS 配置**，开启**支持 IPMI 设置启动模式**，然后将**启动模式**选项设置为**统一可扩展固件接口（UEFI）**，完成后单击**保存**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_79.png)

## Suma BMC

> **注意**：
>
> - 对于 **Suma R6240H0** 型号服务器，由于其固件存在已知问题，需要在 BIOS 中禁用 `Serial Port`，否则会导致无法正常使用 SOL 功能。禁用 `Serial Port` 方法如下：
>
>   重启服务器，进入 `BIOS Setup Utility`，将 `Advanced`>`AST2500 Super IO Configuration`>`Serial Port Configuration`>`Serial Port` 参数设置为 **Disabled**。
>
>   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_62.png)
> - 对于 **Suma H620-G30/R6230HA** 型号服务器，其 BMC 固件版本不能低于 **3.30** ，若低于 **3.30** 请联系硬件厂商进行 BMC 固件升级。
>
>   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_59.png)

1. 单击 **BMC 设置** > **服务**，然后按照下图设置 web 和 ipmi 服务的参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_60.png)
2. 单击**远程设置** > **BIOS 设置** > **管理配置**，然后按照下图设置所有参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_61.png)
3. 单击 **BMC 配置** > **用户/用户组**，然后为当前用户开启 **VMedia 访问**权限。

---

## 在物理服务器上安装 SMTX ZBS > 安装 SMTX ZBS

# 安装 SMTX ZBS

## 第 1 步：选择执行任务

1. 打开浏览器，在地址栏输入 Cluster Installer 的 IP 地址，输入用户名和密码，登录 Cluster Installer 的 Web 界面。
2. 在首页选择集群类型为 **SMTX ZBS**。
3. 在**开始新项目**界面，输入本次项目的名称，项目名称用于区分安装部署（或扩容）的内容，建议使用英文大小写字母及数字。
4. 单击**开始配置**。

## 第 2 步：获取主机信息

**注意事项**

从本步骤开始需要手动填写项目的配置信息，在填写信息的过程中请勿关闭浏览器，否则项目的配置信息将不会保留。

**操作步骤**

1. 在**集群规模**界面，输入主机数量、所有主机的 IPMI IP 地址、管理员用户名及密码。IPMI IP、管理员用户名及密码均可以批量填充。
2. 输入完成后，单击**获取主机信息**，Cluster Installer 开始查找主机并检查主机是否满足安装要求。

   - 若主机满足安装要求，界面将提示“已获取到主机 CPU 架构等信息”。可在界面中查看每个主机的 BMC、CPU 架构以及服务器型号信息。
   - 若部分信息未成功获取，可单击下拉框，根据主机的 FRU 信息，手动选择当前主机的 BMC 及 CPU 架构。
   - 若发现问题，请根据提示解决问题后重试。
3. 单击**下一步**，继续选择所需的安装文件。

## 第 3 步：上传安装文件

1. 在**安装文件**界面，单击**上传到 Cluster Installer**，进入安装文件上传界面。
2. 双击打开 Cluster Installer 中内置的 `md5sum.txt` 文件，检查文件中是否已包含了当前使用的安装文件的 MD5 信息。若有未添加 MD5 信息的安装文件，请手动输入该安装文件的 MD5 信息，格式为 `md5sum + 空格 + 文件名`。完成添加后，保存并关闭`md5sum.txt`文件。

   > **注意**：
   >
   > 请勿更改 MD5 汇总表的文件名及文件格式，否则会导致校验 MD5 步骤出错。
3. 单击安装文件上传界面右上角上传按钮，在本地计算机中选择所需的安装文件进行上传。
4. 上传完成后，返回**安装文件**界面，单击**刷新**，然后根据需要选择安装文件。
5. 选择完成后，单击**收集硬件配置**，Cluster Installer 自动运行 LiveCD 并收集主机中的物理盘、网卡等硬件配置信息。收集过程中可单击**按目录查看日志**，确认收集进度。

   - 若主机硬件满足要求，界面将提示“已收集到主机中物理盘、网卡等硬件配置信息”。
   - 若主机硬件不满足要求，界面将提示已发现的问题，解决问题后单击**重新收集硬件配置**。
6. 单击**下一步**，继续输入配置信息。

## 第 4 步：输入配置信息

在**配置信息**界面配置存储和管理网络。

### 配置存储

1. （可选）如果 SMTX ZBS 集群为 5.5.0 及以上版本，请为所有主机批量选择容量规格。您也可根据实际需求为每台主机单独选择容量规格。
2. 根据在确认 SMTX ZBS 集群构建要求时已规划的每块物理盘的用途，为每台主机的物理盘选择用途。

### 配置管理网络

若已确定管理网络信息，请参考如下操作进行配置。若部分管理网络信息暂时无法确定，可跳过此步骤，待安装完成后通过 Cluster Installer 在服务器操作系统中预制的管理网络信息的配置脚本完成管理网络配置。

1. 选择管理网络对应的物理网口。

   - 需要为每台主机分配一个状态为**连接正常**且速率在 1GbE 及以上的物理网口。
   - 每台主机仅允许选择一个物理网口，如需多个网口绑定使用，可在集群部署阶段添加。
2. 配置管理网络 IP 以及所对应的子网掩码、网关和 VLAN ID。

## 第 5 步：执行安装部署

1. 填写完所有配置信息后，单击**核查信息**，Cluster Installer 将对已填写的配置信息进行检查。

   - 若通过检查，**检查信息**按钮将变为**执行安装**，可以开始执行安装。
   - 若未通过检查，系统将提示错误，请根据提示对不符合要求的内容进行补充和修改。
2. 通过检查后，单击**执行安装**，此时系统将自动检查 Cluster Installer 是否支持运行安装。

   - 若可正常运行，将弹出对话框提示确认开始执行自动化安装 SMTX ZBS，单击对话框中的**执行安装**，进入**自动化执行**界面。
     安装过程中用户可以进行如下操作：

     - 查看安装的总体进度
     - 按目录查看日志：单击可查看当前 workflow 的日志目录，目录中按照主机粒度进行了归类，方便出错后的进一步排查。
     - 停止安装：安装过程中，用户可随时停止安装当前任务。停止安装后，如需重新执行，将会在所有主机上重新执行安装任务。
   - 若无法运行，将弹出对话框提示检查系统日志、Cluster Installer 相关的网络和服务是否正常运行，并解决问题后重试。

## 第 6 步：检查安装结果

执行结束后，在**自动化执行**界面可以查看 SMTX ZBS 的安装结果。

- 若已安装成功，界面将提示 **SMTX ZBS 安装成功**，此时：

  - **若已配置管理网络**

    可单击任一节点的管理 IP，继续手动部署集群。
  - **若未配置管理网络或有部分网络信息尚未配置**

    可进入服务器操作系统中，编辑 `/tmp/config_mgt_network.sh` 脚本文件，补充管理网络配置信息，然后执行 `bash /tmp/config_mgt_network.sh` 命令运行脚本，完成管理网络配置。
    `/tmp/config_mgt_network.sh` 脚本文件包含如下参数：

    ```
    MGT_IP=                      //管理网络 IP
    NETMASK=                     //子网掩码
    GATEWAY=                     //网关
    MGT_PNIC=                    //管理网卡名称或 MAC 地址
    VLAN=                        //管理网络的 VLAN ID
    ```
  - 可单击**查看项目配置**，查看此次项目中填写的配置信息。
- 若安装失败，安装任务将会被终止，请根据具体的报错及日志信息参考 [Q&A](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_46) 排查导致失败的原因，解决问题后，可参考如下说明重新执行安装。

  - 若无需修改配置信息，请在当前界面单击**重新执行**，系统将从上一次失败的步骤开始执行。
  - 若需要修改配置信息，请单击**修改配置信息**返回**配置信息**界面进行修改，然后再重新执行安装任务。

## 第 7 步：手动部署 SMTX ZBS 集群

使用 Cluster Installer 完成 SMTX ZBS 的安装后，可参考《SMTX ZBS 安装部署指南》的“部署 SMTX ZBS 集群”章节，继续手动完成 SMTX ZBS 集群的部署。

---

## 在物理服务器上安装 SMTX ELF

# 在物理服务器上安装 SMTX ELF

本章节介绍了使用 Cluster Installer 在物理服务器上安装 SMTX ELF 的要求和操作步骤，完成安装后需手动部署 SMTX ELF 集群，可参考《SMTX ELF 安装部署指南》中的“部署 SMTX ELF 集群”章节。

---

## 在物理服务器上安装 SMTX ELF > 安装 SMTX ELF 的要求

# 安装 SMTX ELF 的要求

使用 Cluster Installer 在物理服务器上安装 SMTX ELF 之前，需要先确保现场安装部署环境满足构建 SMTX ELF 集群的基本要求，在确保其满足 Cluster Installer 的要求。

---

## 在物理服务器上安装 SMTX ELF > 安装 SMTX ELF 的要求 > 构建 SMTX ELF 集群的基本要求

# 构建 SMTX ELF 集群的基本要求

请参考目标 SMTX ELF 集群版本的《SMTX ELF 安装部署指南》确认现场安装部署环境满足构建 SMTX ELF 集群的要求，并规划 SMTX ELF 网络。

---

## 在物理服务器上安装 SMTX ELF > 安装 SMTX ELF 的要求 > 使用 Cluster Installer 的要求

# 使用 Cluster Installer 的要求

请确认现场安装部署环境满足以下对使用 Cluster Installer 的要求。

---

## 在物理服务器上安装 SMTX ELF > 安装 SMTX ELF 的要求 > 使用 Cluster Installer 的要求 > Cluster Installer 所在虚拟机的运行环境要求

# Cluster Installer 所在虚拟机的运行环境要求

Cluster Installer 部署在虚拟机中，该虚拟机需运行在已安装虚拟机管理程序的服务器、个人电脑或集群主机中，当前仅支持以下类型。

- ESXi 主机；
- 已安装如下虚拟机管理软件的个人电脑：

  - VMware Workstation：14 pro 及以上版本；
  - Oracle VirtualBox：6.0 及以上版本。
  > **注意：**
  >
  > 为确保软件能成功安装，建议在安装前先在本地计算机的 BIOS/固件设置中启用 Intel VT-x，然后重启计算机。
- 5.0.5 及以上版本的 SMTX OS（ELF）集群中的主机。
- SMTX ELF 集群中的主机（已配置关联存储）。

此外，以上服务器、个人电脑和集群主机还需满足以下要求：

- CPU 架构为 x86\_64；
- 有足够的资源空间：
  - 至少 2 个 CPU；
  - 至少 64 GB 存储空间；
  - 至少 2 GB 内存，但对于 SMTX OS（ELF）集群中的主机，则需预留至少 3 GiB 内存。
- 对于个人电脑，其使用的物理网卡速率必须大于或等于 1 Gbps。

---

## 在物理服务器上安装 SMTX ELF > 安装 SMTX ELF 的要求 > 使用 Cluster Installer 的要求 > 软件版本要求

# 软件版本要求

在物理服务器上安装 SMTX ELF 所使用的软件需要满足 Cluster Installer 版本配套说明中对 SMTX ELF 软件版本的要求。

---

## 在物理服务器上安装 SMTX ELF > 安装 SMTX ELF 的要求 > 使用 Cluster Installer 的要求 > 待部署 SMTX ELF 集群的服务器要求

# 待部署 SMTX ELF 集群的服务器要求

待安装部署 SMTX ELF 集群的服务器需要满足[配套的服务器](/clusterinstaller/1.4.1/installer_release_notes/cluster_installer_release_notes_02#%E9%85%8D%E5%A5%97%E7%9A%84%E6%9C%8D%E5%8A%A1%E5%99%A8)要求。

---

## 在物理服务器上安装 SMTX ELF > 安装 SMTX ELF 的要求 > 使用 Cluster Installer 的要求 > 浏览器版本要求

# 浏览器版本要求

借助 Cluster Installer 在物理服务器上安装 SMTX ELF 的过程中需要使用 Web 浏览器，为保证兼容性，建议使用 Chrome 80 或 Firefox 78 及以上版本的浏览器，并启用 Cookie 和 JavaScript。

---

## 在物理服务器上安装 SMTX ELF > 安装 SMTX ELF 的要求 > 使用 Cluster Installer 的要求 > 网络连通要求

# 网络连通要求

借助 Cluster Installer 在物理服务器上安装 SMTX ELF 时，需要确保 Cluster Installer 的网络环境及 IP 均满足如下要求。

- Cluster Installer 网络环境要求：

  - 若在 ESXi 主机、SMTX OS 集群或 SMTX ELF 集群中安装 Cluster Installer，需保证主机或集群中有可连通待部署集群的服务器 IPMI 网络的虚拟机网络，且虚拟机网络的带宽必须大于或等于 1 Gbps。
  - 若在个人电脑安装 Cluster Installer，需保证个人电脑已与待部署集群的服务器 IPMI 网络连通。
- Cluster Installer IP 要求：集群安装工具 IP 与待部署集群的 IPMI IP 互相连通。

---

## 在物理服务器上安装 SMTX ELF > 安装 SMTX ELF 的要求 > 使用 Cluster Installer 的要求 > 防火墙端口开放要求

# 防火墙端口开放要求

| 源端 | 目标端 | 目标端需开放端口 | 端口说明 |
| --- | --- | --- | --- |
| 浏览器客户端 IP | Cluster Installer IP | TCP 80 | 用于浏览器 Web 访问 Cluster Installer |
| Cluster Installer IP | 服务器 IPMI IP | TCP 443 | BMC Redfish/HTTPS API 端口 |
| UDP 623 | IPMI 协议端口，用于获取服务器 FRU 信息、SOL 串口输出 |
| TCP 22 | 如果服务器的 BMC 为 Huawei iBMC 或 Dell iDRAC 且 iDRAC 版本低于 4.0，需要通过 SSH 登录到 BMC 挂载 ISO 文件 |
| 服务器 IPMI IP | Cluster Installer IP | Cluster Installer 虚拟机 NFS Server 端口\* | NFS 访问端口，BMC 需要通过 NFS 协议挂载 Cluster Installer 虚拟机里的 ISO 文件 |
| TCP 80 | 如果服务器的 BMC 为 HPE iLO5，需开放此端口 |

> **说明**：
>
> Cluster Installer 虚拟机 NFS Server 端口（表中有星号 \* 标记的端口）除了 `2049` 和 `111` 两个固定端口外，其他端口均为随机端口。在创建完 Cluster Installer 虚拟机并配置完 IP 后，您才能查看 NFS Server 使用了哪些随机端口，同时您也可以选择自定义除 111 端口外的其他 NFS Server 端口，建议参考上述要求提前规划。

---

## 在物理服务器上安装 SMTX ELF > 创建 Cluster Installer 虚拟机

# 创建 Cluster Installer 虚拟机

您可以根据当前环境选择在 ESXi 主机、SMTX OS（ELF）集群的主机、或者个人电脑中创建 Cluster Installer 虚拟机。

---

## 在物理服务器上安装 SMTX ELF > 创建 Cluster Installer 虚拟机 > 在 ESXi 主机中创建

# 在 ESXi 主机中创建

在 ESXi 主机中创建 Cluster Installer 虚拟机时，可以选择直接登录 ESXi 主机进行创建或者在 vCenter Server 的 ESXi 主机中创建。

**注意事项**

Cluster Installer 虚拟机的名称不能包含除下划线 `_`、减号 `-`、点 `.` 以外的特殊字符，否则会导致安装程序出错。

## 直接登录 ESXi 主机进行创建

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 登录 ESXi 主机的 Web 管理页面，打开**创建/注册虚拟机**，选择**从 OVF 或 OVA 文件部署虚拟机**，单击**下一步**。
3. 输入虚拟机的名称，打开**单击以选择文件或拖放**，选择已下载至本地计算机上的 OVA 文件，单击**下一步**。
4. 为虚拟机的配置文件及其虚拟磁盘选择数据存储，单击**下一步**。
5. 在部署选项设置中，将网络映射 nic0 设置为符合网络连通要求的虚拟机网络，然后依次单击**下一步**完成配置。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_33.png)

## 在 vCenter Server 中的 ESXi 主机中创建

**注意事项**

若 vCenter 集群需要开启 EVC 特性，请先开启 EVC 特性，再安装 Cluster Installer 虚拟机。

**操作步骤**

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 登录 vCenter Server 的 Web 管理界面，定位到用于部署 Cluster Installer 虚拟机的 ESXi 主机，右键单击该主机，并选择**部署 OVF 模板**。
3. 选择**本地文件**，单击**上传文件**，上传已下载至本地计算机上的 OVA 文件。
4. 依次输入虚拟机名称、选择虚拟机安装位置、选择计算机资源、选择存储。
5. 在选择网络配置中，将网络映射 nic0 设置为符合网络连通要求的虚拟机网络，并完成后续配置。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_11.png)

---

## 在物理服务器上安装 SMTX ELF > 创建 Cluster Installer 虚拟机 > 在 SMTX OS（ELF）集群或 SMTX ELF 集群的主机中创建

# 在 SMTX OS（ELF）集群或 SMTX ELF 集群的主机中创建

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 重命名该 OVA 文件，将文件名后缀 `.ova` 修改为 `.tar`，并解压该文件。
3. 登录 CloudTower，单击**创建** > **导入虚拟机**。
4. 在**导入虚拟机**界面中，选择安装 Cluster Installer 的集群和主机，并将已解压的对应文件上传至在**模板信息**区。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_67.png)
5. 在**计算资源**配置界面，将内存分配设置为 **3 GiB**。
6. 在**磁盘**配置界面，将总线类型设置为 **VIRTIO**，选择其他类型会导致虚拟机无法正常启动。
7. 在**虚拟网卡**界面，选择符合网络连通要求的虚拟机网络。
8. 在**其他**配置页面，选择**创建完成后自动开机**，单击**确定**。

---

## 在物理服务器上安装 SMTX ELF > 创建 Cluster Installer 虚拟机 > 在个人电脑中创建

# 在个人电脑中创建

1. 下载 Cluster Installer 的 OVA 模板文件至本地。
2. 根据个人电脑中所安装的虚拟机管理软件类型参考对应步骤创建 Cluster Installer 虚拟机。
   - **在 VMware Workstation 中创建**
     1. 在 VMware Workstation 单击**导入虚拟机**，导入已下载的 OVA 模板文件，输入新虚拟机名称以及 OVA 文件所在的存储路径。请确保存储路径所在分区的剩余可用空间不小于 64 GB。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_04.png)
     2. 在**编辑**菜单中单击**虚拟网络编辑器**，选择**更改设置**，选择 VMnet0 的桥接模式，在**已桥接至**下拉列表中选择本地计算机所使用的物理网卡。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_07.png)
     3. 打开 Cluster Installer 的**虚拟机设置**，确认网络连接模式为**桥接模式**。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_08.png)
   - **在 Oracle VirtualBox 中创建**
     1. 在 VirtualBox 中单击**管理**菜单，选择**导入虚拟机电脑**，选择 OVA 文件所在的存储路径，并确认**默认虚拟机电脑位置**所在分区的剩余可用空间不小于 64 GB。

        导入时将 MAC 地址设定设置为**为所有网卡重新生成 MAC 地址**。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_09.png)
     2. 导入虚拟机后，打开虚拟机设置页面，确保网卡 1 的连接方式为**桥接网卡**。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_10.png)

---

## 在物理服务器上安装 SMTX ELF > 配置 Cluster Installer IP

# 配置 Cluster Installer IP

创建 Cluster Installer 虚拟机后，需要为虚拟机配置 IP 地址。下文以 VMware Workstation 为例介绍配置步骤。

**操作步骤**

1. 打开 VMware Workstation，在**我的计算机**中，选择已创建的 Cluster Installer 虚拟机单击**开启此虚拟机**。
2. 配置虚拟机的 IP 地址。

   - 如果虚拟机桥接网络内有 DHCP 服务器，Cluster Installer 会通过 DHCP 服务器自动获取 IP 地址，并显示在虚拟机控制台。

     ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_12.png)
   - 如果虚拟机桥接网络内没有 DHCP 服务器，则请执行以下操作。

     1. 打开 `/etc/sysconfig/network-scripts/ifcfg-eth0` 文件，设置静态 IP。
     2. 重启 Cluster Installer 虚拟机。

        ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_13.png)
3. 执行 `prepare.sh` 命令检查虚拟机内的服务是否正常运行。

   当时输出结果显示 `Failed: 0` 和 `Skipped: 0` 时，表示服务正常运行。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_14.png)

   - 如果服务正常运行，则可以正常使用 Cluster Installer 。
   - 如果服务未正常运行，排查完原因后，若需要变更 Cluster Installer 所在的网络和修改 IP 地址，请从上一步开始重新执行操作。

---

## 在物理服务器上安装 SMTX ELF > 开放 NFS Server 端口

# 开放 NFS Server 端口

1. 登录 Cluster Installer 虚拟机，执行以下命令查看 NFS Server 当前使用的所有端口信息。

   ```
   rpcinfo -p
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_80.png)
2. （可选）如果需要自定义 NFS Server 端口，请执行以下步骤。

   1. 执行以下命令，然后根据提示输入实际规划的新端口。如果不需要修改某端口，可以直接按 Enter 键跳过该端口的设置。

      ```
      /root/deploy/tools/update_nfs_ports.sh
      ```

      ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_82.png)
   2. 执行以下命令，确认端口已修改成功。

      ```
      rpcinfo -p
      ```

      ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_83.png)
3. 执行以下命令，查看需要开放的 NFS Server 端口。

   ```
   rpcinfo -p | awk '{print $3,$4}' | sort -u
   ```
4. 参考防火墙端口开放要求，为 Cluster Installer 虚拟机开放 NFS Server 端口。

---

## 在物理服务器上安装 SMTX ELF > 检查服务器的 BMC 和 BIOS 设置

# 检查服务器的 BMC 和 BIOS 设置

使用 Cluster Installer 在物理服务器上安装 ESXi、SMTX OS、SMTX ELF 或 SMTX ZBS 时，需依赖服务器的 BMC（基板管理控制器）对服务器执行开机、重启、挂载 ISO、卸载 ISO、获取 Console 输出等操作，因此在安装前，需参考下文检查服务器的 BMC 和 BIOS 设置，确保已启用以下功能：

- Redfish 或 HTTPS 访问功能；
- IPMI Over LAN 功能；
- SOL（Serial Over LAN ）功能。

**注意事项**

- 如果选择 `Avago MegaRAID` 卡上的硬盘作为服务器的启动盘，安装前需要确保 RAID 卡在 BIOS 设置里的 **Boot device** 为所选的硬盘，否则会导致 ISO 安装完后由于启动设备配置错误导致系统无法正常启动。

  ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_65.png)
- 如果服务器的 CPU 架构为鲲鹏 AArch64，需要确保服务器的 BIOS 设置里的 **CPU Prefetching Configuration** 选项为 **Enabled**，否则会影响 CPU 性能。

  ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_73.png)

## Dell iDRAC

1. 打开浏览器，在地址栏输入服务器的 IPMI 管理台 IP，登录服务器的 iDRAC 管理界面。
2. 单击 **iDRAC 设置** > **连接性** > **LAN 上串行**，将**启用 LAN 上串行**状态设置为**已启用**，然后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_51.png)
3. 单击 **iDRAC 设置** > **连接性** > **网络** >**IPMI 设置**，将**启用 LAN 上的 IPMI** 状态设置为**已启用**，然后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_52.png)
4. 单击 **iDRAC 设置** > **用户** > **本地用户**，确认本地用户的 **LAN 上串行**已启用。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_53.png)
5. 单击 **iDRAC 设置** > **服务** > **Redfish**，将 Redfish 状态设置为**已启用**，然后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_54.png)

## Lenovo XClarity

1. 打开浏览器，在浏览器的地址栏输入服务器的 IPMI 管理台 IP，登录服务器的 XClarity Controller 管理界面。
2. 单击 **BMC 配置**，然后参考下图启用 **Web Over HTTPS**、**REST Over HTTPS** 和 **IPMI over LAN**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_55.png)

## HPE iLO5

1. 打开浏览器，在浏览器的地址栏输入服务器的 IPMI 管理台 IP，登录服务器的 iLO5 管理界面。
2. 单击**安全性** > **访问设置**，然后按下图设置参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_56.png)

## Inspur BMC

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录服务器的 BMC 管理界面。
2. 单击**系统设置** > **服务**，然后按下图设置 WEB、CD-Media 和 IPMI 服务的参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_77.png)
3. 单击**系统设置** > **用户精细化管理**，然后按下图检查并确认当前用户属于 Administrator 用户组，用户已启用，且 IPMI 权限为 `administrator`。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_78.png)

## Huawei iBMC

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录服务器的 iBMC 管理界面。
2. 单击**服务管理** > **端口服务**，然后按下图设置参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_57.png)
3. 单击**用户&安全** > **本地用户**，然后按下图设置登录接口。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_58.png)
4. 单击**系统管理** > **BIOS 配置**，开启**支持 IPMI 设置启动模式**，然后将**启动模式**选项设置为**统一可扩展固件接口（UEFI）**，完成后单击**保存**。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_79.png)

## Suma BMC

> **注意**：
>
> - 对于 **Suma R6240H0** 型号服务器，由于其固件存在已知问题，需要在 BIOS 中禁用 `Serial Port`，否则会导致无法正常使用 SOL 功能。禁用 `Serial Port` 方法如下：
>
>   重启服务器，进入 `BIOS Setup Utility`，将 `Advanced`>`AST2500 Super IO Configuration`>`Serial Port Configuration`>`Serial Port` 参数设置为 **Disabled**。
>
>   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_62.png)
> - 对于 **Suma H620-G30/R6230HA** 型号服务器，其 BMC 固件版本不能低于 **3.30** ，若低于 **3.30** 请联系硬件厂商进行 BMC 固件升级。
>
>   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_59.png)

1. 单击 **BMC 设置** > **服务**，然后按照下图设置 web 和 ipmi 服务的参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_60.png)
2. 单击**远程设置** > **BIOS 设置** > **管理配置**，然后按照下图设置所有参数。

   ![](https://cdn.smartx.com/internal-docs/assets/d7e8f8e1/installer_guide_61.png)
3. 单击 **BMC 配置** > **用户/用户组**，然后为当前用户开启 **VMedia 访问**权限。

---

## 在物理服务器上安装 SMTX ELF > 安装 SMTX ELF

# 安装 SMTX ELF

## 第 1 步：选择执行任务

1. 打开浏览器，在地址栏输入 Cluster Installer 的 IP 地址，输入用户名和密码，登录 Cluster Installer 的 Web 界面。
2. 在首页选择集群类型为 **SMTX ELF**。
3. 在**开始新项目**界面，输入本次项目的名称，项目名称用于区分安装部署（或扩容）的内容。建议使用英文大小写字母及数字。
4. 单机**开始配置**。

## 第 2 步：获取主机信息

**注意事项**

从本步骤开始需要手动填写项目的配置信息，在填写信息的过程中请勿关闭浏览器，否则项目的配置信息将不会保留。

**操作步骤**

1. 在集群规模界面，输入主机数量、所有主机的 IPMI IP 地址、管理员用户名及密码。IPMI IP、管理员用户名及密码均可以批量填充。
2. 输入完成后，单击**获取主机信息**，Cluster Installer 开始查找主机并检查主机是否满足安装要求。

   - 若主机满足安装要求，界面将提示“已获取到主机 CPU 架构等信息”。可在界面查看每个主机的 BMC、CPU 架构以及服务器型号信息。
   - 若部分信息未成功获取，可单击下拉框，根据主机的 FRU 信息，手动选择当前主机的 BMC 或 CPU 架构。
   - 若发现问题，请根据提示解决问题后单击**重新获取主机信息**。
3. 单击**下一步**，请继续上传所需的安装文件。

## 第 3 步：上传安装文件

1. 在安装文件界面单击**上传到 Cluster Installer**，进入安装文件上传界面。
2. 双击打开 Cluster Installer 中内置的 `md5sum.txt` 文件，检查文件中是否已包含了当前使用的安装文件的 MD5 信息。若有未添加 MD5 信息的安装文件，请手动输入该安装文件的 MD5 信息，格式为 `md5sum + 空格 + 文件名`。完成添加后，保存并关闭 `md5sum.txt` 文件。

   > **注意**：
   >
   > 请勿更改 MD5 汇总表的文件名及文件格式，否则会导致校验 MD5 步骤出错。
3. 单击安装文件上传界面右上角上传按钮，在本地计算机中选择所需的安装文件进行上传。
4. 上传完成后，返回**安装文件**界面，单击**刷新**，然后根据需要选择安装文件。
5. 选择完成后，单击**收集硬件配置**，Cluster Installer 自动运行 LiveCD 并收集主机中的物理盘、网卡等硬件配置信息。收集过程中可单击**按目录查看日志**，确认收集进度。

   - 若主机硬件满足要求，界面将提示“已收集到主机中物理盘、网卡等硬件配置信息”。
   - 若主机硬件不满足要求，界面将提示发现的问题，解决问题后单击**重新收集硬件配置**。
6. 单击**下一步**，继续输入配置信息。

## 第 4 步：输入配置信息

在**配置信息**界面配置存储和管理网络。

### 配置存储

为每台主机指定 1 块容量最多为 2 TiB 的物理盘作为 SMTX 引导盘。

### 配置管理网络

若已确定管理网络信息，请参考如下操作进行配置。若部分网络信息暂时无法确定，可跳过此步骤，待安装完成后通过 Cluster Installer 在服务器操作系统中预制的管理网络信息的配置脚本完成管理网络配置。

1. 选择管理网络对应的网口。

   - 需要为每台主机分配一个状态为**连接正常**且速率在 1 GbE 及以上的物理网口。
   - 每台主机仅允许选择一个物理网口，如需多个网口绑定使用，可在集群部署阶段添加。
2. 配置管理网络 IP 以及其对应的子网掩码、网关和 VLAN ID。

## 第 5 步：执行安装部署

1. 填写完所有配置信息后，单击**核查信息**，Cluster Installer 将对已填写的配置信息进行检查。

   - 若通过检查，**核查信息**按钮将变为**执行安装**，可以开始执行安装。
   - 若未通过检查，系统将提示错误，请根据提示对不符合要求的内容进行补充和修改。
2. 通过检查后，单击**执行安装**，此时系统将自动检查 Cluster Installer 是否支持运行安装。

   - 若可正常运行，将弹出对话框提示确认开始执行自动话安装 SMTX ELF，单击对话框中的**执行安装**，进入**自动化执行**界面。安装过程中您可以进行如下操作：

     - 查看安装的总体进度。
     - 按目录查看日志：单击可查看当前 workflow 的日志目录，目录中安装主机粒度进行了归类，方便出错后的进一步排查。
     - 停止安装：安装过程中，用户可随时停止安装当前任务。停止安装后，如需重新执行，将会在所有主机上重新执行安装任务。
   - 若无法运行，将弹出对话框提示检查系统日志、Cluster Installer 相关的网络是否正常运行，并解决问题后重试。

## 第 6 步：检查安装结果

执行结束后，在**自动化执行**界面可以查看 SMTX ELF 的安装结果。

- 若安装成功，界面将提示 **SMTX ELF 安装成功**，此时：

  - **若已配置管理网络**

    可单击任一节点的管理网络，继续手动部署集群。
  - **若未配置管理网络或有部分网络信息尚未配置**

    可进入服务器操作系统中，编辑 `/tmp/config_mgt_network.sh` 脚本文件，补充管理网络配置信息，然后执行 `bash /tmp/config_mgt_network.sh` 命令运行脚本，完成管理网络配置。
    `/tmp/config_mgt_network.sh` 脚本文件包含如下参数：

    ```
    MGT_IP=                      //管理网络 IP
    NETMASK=                     //子网掩码
    GATEWAY=                     //网关
    MGT_PNIC=                    //管理网卡名称或 MAC 地址
    VLAN=                        //管理网络的 VLAN ID
    ```
  - 可单击**查看项目配置**，查看此次项目中填写的配置信息。
- 若安装过程中任一步骤失败，安装任务将终止，请根据具体的报错及日志信息参考 [Q&A](/clusterinstaller/1.4.1/installer_user_guide/installer_user_guide_46) 排查导致失败的原因，解决问题后，可参考如下说明重新执行安装。

  - 若无需修改配置信息，请在当前界面单击**重新执行**，系统将从上一此失败的步骤开始执行。
  - 若需要修改配置信息，请在当前界面单击**修改配置信息**返回**配置信息**界面进行修改，然后再重新执行安装任务。

## 第 7 步：手动部署 SMTX ELF 集群

使用 Cluster Installer 完成 SMTX ELF 的安装后，可参考《SMTX ELF 安装部署指南》的“部署 SMTX ELF 集群”章节，继续手动完成 SMTX ELF 集群的部署。

---

## 查看执行项目

# 查看执行项目

在 Cluster Installer 首页下方的**全部项目**列表展示了所有已发起过自动化执行任务的项目，您可以查看以下项目信息。

- 基本信息：在列表中可直接查看项目的以下基本信息。
  - 执行状态：项目的执行状态，也是项目的最近一次自动化执行任务的执行状态。
  - 项目名称：手动设置的项目名称。
  - 集群类型：项目的目标集群类型。
  - 功能：项目完成的功能。
  - 上次执行开始时间：项目的最近一次自动化执行任务的开始执行时间。
- 执行历史：单击项目左侧的三角形图标，可以查看项目已发起的所有自动化执行任务的执行情况，包括执行的次数、起始时间、用时和结果，如果执行失败，还可查看失败的原因和执行日志。
- 执行进度：如果项目正在执行中，单击项目右侧的 **...** 图标，选择**查看进度**，可以跳转到项目的**自动化执行**界面查看项目的具体执行进度。
- 执行结果：如果项目执行成功或失败，单击项目右侧的 **...** 图标，选择**查看结果**，可以跳转到项目的**自动化执行**界面查看项目的执行结果。
- 配置信息：如果项目执行成功，单击项目右侧的 **...** 图标，选择**查看项目配置**，可以查看在开始该项目后填写的所有配置信息。

---

## 卸载 Cluster Installer

# 卸载 Cluster Installer

关闭 Cluster Installer 虚拟机，然后将该虚拟机彻底删除即可。

---

## Q&A

# Q&A

以下为安装部署各阶段常见的失败提示和排查方法。

## 获取主机信息

**Q：输入了正确的 IPMI 用户名和密码，但无法获取到主机信息。**

**A**：请检查如下设置：

- 检查服务器是否开启 Redfish 或 HTTPS 访问功能，且确保开启 443 TCP 端口；
- 检查当前用户是否开启 IPMI Over LAN 功能，且确保开启 623 UDP 端口；
- 检查当前用户是否被限制登录，如密码输入错误次数被锁定、IPMI 管理台已达到最大连接数等。

**Q：挂载 LiveCD 失败。**

**A**：登录到服务器 IPMI 管理台，手动卸载已挂载的 LiveCD。若卸载 LiveCD 失败，可以尝试重启 IPMI 管理台，然后重新卸载 ISO。

> **说明**：
> 若服务器在使用 Cluster Installer 之前已经挂载过 NFS 或 CIFS 类型的 ISO，且 ISO 源文件已不存在时，卸载 LiveCD 将会失败。此时需重启 IPMI 管理台，然后重新卸载。

**Q：收集主机硬件信息失败。**

**A**：若收集主机硬件信息失败，请按如下步骤进行排查：

1. 检查 LiveCD 是否已正常启动。

   登录到服务器 IPMI 管理台，按 `CTRL+ALT+F2` 键切换到 tty1 终端，检查 `/tmp` 目录下是否存在 `get_host_info.py` 文件，若存在该文件说明已经正常从 ISO 启动。

   若按下 `CTRL+ALT+F2` 无反应，或者 `/tmp` 目录下不存在 `get_host_info.py` 文件，说明 LiveCD 未正常启动，请联系研发处理。
2. 若 LiveCD 已正常启动，请在 Installer 界面单击**按目录查看日志**，如果日志目录中存在 `host-info-$IPMI_IP.json` 文件，`$IPMI_IP.log` 文件不为空，且不小于 1 KB，说明对应的服务器已成功收集到硬件信息。否则：

   - 若日志目录中不存在 `host-info-$IPMI_IP.json` 文件，请联系研发处理；
   - 若 `$IPMI_IP.log` 文件为空，或者文件小于 1 KB，说明服务器的 SOL 串口重定向功能异常，导致 Cluster Installer 无法获取服务器的串口输入内容。请检查 IPMI 管理台是否开启 SOL 功能。

**Q：收集硬件信息和安装阶段服务器虚拟控制台无输出内容**

**A**：在收集硬件信息和安装 ESXi/SMTX OS/SMTX ELF/SMTX ZBS 阶段，Cluster Installer 会将服务器的控制台输出通过 SOL 功能重定向到 Cluster Installer 安装程序，并以 `$IPMI_IP.log` 日志的形式保存。在此期间无法通过虚拟控制台查看安装进度，用户可以通过按目录查看 `$IPMI_IP.log` 文件查看服务器输出。

**Q: 获取主机信息后，界面提示“物理盘数量不足”，但实际服务器中物理盘数量足够。**

**A**: 查看 ESXi 主机是否已经组成了集群。如已有集群，请按照如下步骤清理集群信息后再使用 Cluster Installer 进行部署。清理操作不会涉及物理主机上的硬盘。

1. 删除 SCVM 之外的全部虚拟机；
2. 删除 CloudTower 虚拟机；
3. 删除 ZBS NFS datastore；
4. 删除 SCVM 虚拟机；
5. 删除创建的网络；
6. 清理 IO 路由脚本；
7. 禁用 PCI 设备直通，重启 ESXi 主机。

## 安装 ESXi/SMTX OS/SMTX ELF/SMTX ZBS

**Q： 服务器从 ISO 启动时，虚拟控制台显示 `exit_boot() failed! efi_main() failed!` 错误**

**A**：请尝试将服务器关机然后重启，然后再次使用 Cluster Installer 安装。

**Q：SMTX OS/SMTX ELF/SMTX ZBS 在安装阶段配置了管理 IP，安装完后无法 ping 通管理 IP。**

**A**：请进行如下检查：

- 登录服务器 IPMI 管理台，查看服务器是否已经启动到 OS；
- 执行 `ip addr` 命令查看管理网络网卡是否已经配置静态 IP；
- 检查管理网络 IP、子网掩码、网关是否配置正确；
- 若管理网卡上存在 DHCP 分配的 IP，请运行 `systemctl restart network` 命令重启网络，再尝试能否连通管理 IP。

## 部署前检查

**Q: 长时间停留在“正在检查部署环境”界面，且无法在此界面停止部署或查看日志。**

**A**: Cluster Installer 虚拟机内部可能发生服务异。请登录 Cluster Installer 虚拟机，参照配置虚拟机网络流程中的步骤，执行 `prepare.sh` 命令检查 Cluster Installer 虚拟机内的服务是否正常运行，`Failed` 和 `Skipped: 0` 时表示当前服务正常。

**Q: 界面提示“如下 IP 已被占用”**

**A**: 检查在**配置信息**中设置的 SCVM 管理网络 IP、SMTX OS 集群管理虚拟 IP 等 IP 已被占用。如有，需返回部署流程，修改 IP 地址后

**Q: 界面提示“安装部署文件不存在”。**

**A**：按照提示信息中的**上传到 Cluster Installer**链接访问文件管理页面，查看否已包含此次部署需使用的安装文件是。如有问题，需重新上传相关的安装文件。

**Q: 界面提示“安装部署文件 md5 校验失败”。**

**A**: 按照提示信息中的 **md5sum.txt 文件**链接，查看此次部署使用的 MD5 文件：

- 检查是否已上传 `md5sum.txt` 文件，文件格式是否正确，文件内容是否符合要求。
- 确认文件中的 MD5 内容是否正确。如不正确，需要修改文件中对应安装文件的 MD5 值；如正确，需检查已上传的安装文件的 MD5 值，确保文件未发生损坏。

为避免错误，强烈建议使用最新的 MD5 汇总表。

**Q: 部署前检查失败，无明确错误提示。**

**A**: 检查 ESXi 主机是否已经被加入到 vCenter Server 中，如已加入，请从 vCenter Server 中移除主机后再次执行部署前检查。

## 自动化部署

**Q: 界面在“配置 ESXi 主机”步骤提示部署失败。**

**A**: 检查是否配置了 NTP 服务器，如果配置了 NTP 服务器是否可以连通。
如有上述问题，需调整 NTP 服务器后重新部署。

**Q: 界面在“创建 ESXi 网络”步骤提示部署失败。**

**A**: 检查如下内容：

- 存储网络网卡是否正常，如不正常，需调整存储网络网卡后重新部署。
- 存储网络网络 IP 是否已被占用，如有，需单击**修改配置信息**，修改存储网络 IP 后重新部署。
- 在使用 Cluster Installer 进行部署之前，是否已经在 ESXi 中创建 vSwitch 并使用了存储网络对应的物理网卡，如有，需在 ESXi 中删除 vSwitch 后重新部署。

**Q: 界面在“检查 ESXi 网络”步骤提示部署失败。**

**A**: 检查如下内容：

- 各主机的 ESXi 管理网络或存储网络之间是否无法互相连通；
- 存储网络物理网卡选择错误；
- 配置的 vMotion 网络和存储网络在同一网段，但关联了不同的 vSwitch；
- 配置信息中的 VLAN ID 是否设置错误。

如有，需单击**修改配置信息**，修改网络配置后重新部署。

**Q: 界面在“安装 ESXi 插件”步骤提示部署失败。**

**A**: 检查所选的 VAAI-NAS 插件版本与 ESXi 版本是否匹配，具体规则详见获取安装文件部分。

如不匹配，需单击**修改配置信息**，在**安装文件**部分修改使用的 VAAI-NAS 插件后重新部署。

**Q: 界面在“配置 PCI 设备透传”步骤提示部署失败。**

**A**: 检查使用的 PCI 设备是否支持直通。

**Q: 界面在“等待 ESXi 主机重启就绪”步骤执行时间过长。**

**A**: 检查物理服务器启动项是否为 ESXi OS 引导，如不是，需要手动调整物理服务器启动项为 ESXi OS，处理完成后，Cluster Installer 可继续进行部署流程。

**Q: 界面在“创建 SCVM 虚拟机”步骤失败。**

**A**: 检查如下内容：

- ESXi 主机 datastore 上是否残留着同名的 SCVM 虚拟机文件夹。如有，需删除对应的虚拟机文件夹后重新部署。
- 所选 PCI 设备是否不支持被添加到 SCVM 虚拟机。
- SMTX OS 系统盘选择错误或者 SCVM 没有识别到选择的盘。如有，需调整物理盘硬件或单击**修改配置信息**修改系统盘选择后重新部署。

**Q: 界面在“等待 SCVM 就绪”步骤失败。**

**A**: 检查如下内容：

- ESXi 主机与 Cluster Installer 虚拟机之间的网络链接是否正常。

  如网络连接异常或连接状态不稳定，可能导致 NFS 访问错误，或在 SCVM 虚拟机中安装 SMTX OS 超时失败，请在调整网络环境后重新部署。强烈建议将 Cluster Installer 与集群部署在同一网段内，避免由于网络问题导致部署时间过长或部署错误。
- SCVM 管理网络 VLAN ID 是否设置错误，导致 Cluster Installer 虚拟机无法 ssh 登录。如设置错误，请单击**修改配置信息**修改网络信息后重新部署。

**Q: 界面在“部署 SMTX OS 集群”步骤失败。**

**A**: 检查是否存在如下问题：

- SCVM 与 ESXi 之间的存储网络和管理网络无法互相访问。
- ESXi 存储网路 IP 和 SCVM 存储网路 IP 不在同一个网段。

如有上述问题，请单击**修改配置信息**修改 IP 信息后重新部署。

**Q: 界面在“等待 SMTX OS 集群就绪”步骤失败。**

**A**: SMTX OS 集群部署失败，需要查看 zbs-deploy-server 部署日志。

**Q: 界面在“配置 SMTX OS 集群”或“配置 IO 路由”步骤失败。**

**A**: SMTX OS 集群异常，请登录 SCVM 节点查看 SMTX OS 服务状态。

**Q: 界面在“创建 Datastore” 步骤失败。**

**A**: 检查 ESXi 主机上是否有已有 datastore 的残留数据，导致挂载 192.168.33.2:/nfs/datastore-nfs 失败。

**Q: 界面在“创建 CloudTower 虚拟机”步骤失败。**

**A**: 检查**主机 1** 是否存在异常。

**Q: 界面在“等待 CloudTower 虚拟机创建完成”步骤失败。**

**A**: 检查是否存在如下问题：

- Cluster Installer 虚拟机无法访问 CloudTower IP。
- CloudTower 虚拟机网络异常。

**Q: 界面在“其他 CloudTower 相关任务”步骤失败**

**A**: 登录 CloudTower 虚拟机，查看部署日志。

**Q: 界面在“配置 vCenter 集群”步骤失败。**

**A**: 检查是否存在如下问题：

- vCenter Server 中是否已经存在相同 IP 的主机。
- vCenter Server 版本与 ESXi 版本不兼容。
- 对应 vCenter 集群若开启了 EVC 特性，ESXi 主机 CPU 无法满足 EVC 要求。

**Q: 当存储网络的带宽为 25 Gbps 及以上时，将存储网络链路 MTU 设为 9000，SCVM 的存储虚拟网卡未永久保存 MTU=9000 的设置。**

**A**: 登录 SCVM，检查存储虚拟网卡配置文件中是否不包含 `MTU="9000"` 的配置项。如不包含，请执行以下步骤。

1. 在存储虚拟网卡配置文件中添加 `MTU="9000"` 的配置项。
2. 重启存储虚拟网卡。
3. 执行 `ifconfig` 命令，确认存储网络网卡的 MTU 值为 `9000`。

## 自动化扩容

**Q: 界面在“检查 IO 重路由状态”步骤失败**

**A**: 请参考《SMTX OS 集群安装部署指南（VMware ESXi 平台）》的**部署 IO 重路由脚本和 SCVM 自动重启脚本**章节，检查 ESXi 主机 IO 重路由脚本是否正常运行。

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
