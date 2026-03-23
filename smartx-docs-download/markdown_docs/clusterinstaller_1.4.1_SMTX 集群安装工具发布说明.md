---
title: "clusterinstaller/1.4.1/SMTX 集群安装工具发布说明"
source_url: "https://internal-docs.smartx.com/clusterinstaller/1.4.1/installer_release_notes/cluster-installer-release-notes"
sections: 6
---

# clusterinstaller/1.4.1/SMTX 集群安装工具发布说明
## 关于本文档

# 关于本文档

本文档介绍了相较于 1.4.0 版本，SMTX 集群安装工具 1.4.1 版本新增的功能和修复的问题，以及该版本相关的配套信息和使用限制。

---

## 文档更新信息

# 文档更新信息

**2025-12-11：配合 SMTX 集群安装工具 1.4.1 正式发布**

---

## 版本更新说明

# 版本更新说明

## 新增

增加对英文版的支持。

## 修复

修复了在连续安装部署启用 RDMA 功能的 SMTX OS（VMware ESXi）集群时，Mellanox 最新版固件工具 mft/nmst 无法正常安装的问题。

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

## 版本使用限制

# 版本使用限制

- 不支持部署双活集群。
- 不支持使用 VMD 类型的 NVMe 盘。
- 不支持 NVMe Switch 卡上的 NVMe 盘直通。
- ESXi OS 所在物理盘和 SMTX OS 需要使用的物理盘不能在同一个 PCI 设备上。
- 不支持自动部署 vCenter Server 功能，如需使用 vCenter Server 进行集群管理，请在集群部署完成后单独进行安装。
- 部署 SMTX OS（VMware ESXi）集群时，不支持配置 vSphere 分布式交换机。若集群使用了此类交换机，也不支持通过 Cluster Installer 扩容该集群。

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
