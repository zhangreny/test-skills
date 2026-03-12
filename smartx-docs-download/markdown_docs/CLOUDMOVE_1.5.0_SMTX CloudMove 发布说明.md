---
title: "CLOUDMOVE/1.5.0/SMTX CloudMove 发布说明"
source_url: "https://internal-docs.smartx.com/cloudmove/1.5.0/cloudmove_release_notes/cloudmove_release_notes_preface"
sections: 10
---

# CLOUDMOVE/1.5.0/SMTX CloudMove 发布说明
## 关于本文档

# 关于本文档

本文档介绍了 SMTX CloudMove 1.5.0 版本的各个子版本的更新说明，以及最新子版本的配套信息。

---

## 文档更新信息

# 文档更新信息

- **2025-11-12：更新版本更新说明和版本配套说明**

  - 在“版本更新说明”中，新增 1.5.0-11590 和 1.5.0-11622 版本的版本更新说明。
  - 在“版本配套说明”的“对 CloudTower 版本的配套要求”中新增 4.6.2 和 4.7.0 版本。
  - 在“版本配套说明”的“对控制中心操作系统的要求”和“对源主机操作系统的要求”中，更新兼容的操作系统版本。
- **2025-08-18：更新版本更新说明和版本配套说明**

  - 在“版本更新说明”中，新增 1.5.0-11255 版本的版本更新说明。
  - 在“版本配套说明”的“对控制中心操作系统的要求”和“对虚拟代理机操作系统的要求”中，更新兼容的操作系统版本。
- **2025-08-07：更新版本更新说明和版本配套说明**

  - 在“版本更新说明”中，新增 1.5.0-11187 版本的版本更新说明。
  - 在“版本配套说明”的“对源主机操作系统的要求”中，更新兼容的操作系统版本。
- **2025-07-01：更新版本更新说明和版本配套说明**

  - 在“版本更新说明”中，新增 1.5.0-10768、1.5.0-10841、1.5.0-10857、1.5.0-10898、1.5.0-10967 版本的版本更新说明。
  - 在“版本配套说明”中的“对 CloudTower 版本的配套要求”中新增 4.6.0 版本。
  - 在“版本配套说明”中的“对控制中心操作系统的要求”中，x86\_64 架构兼容的版本新增 Ubuntu Server 24.04、openEuler 24.03。
  - 在“版本配套说明”中的“对源主机操作系统的要求”中，x86\_64 架构兼容的版本新增 Oracle Linux 8.6 uek、RHEL 9.6。
- **2025-03-17：更新版本更新说明和版本配套说明**

  - 在“版本更新说明”中，补充 1.5.0-10696、1.5.0-10668 和 1.5.0-10565 版本的版本更新说明。
  - 在“版本配套说明”中的“对 CloudTower 版本的配套要求”中新增 4.5.0 版本。
  - 在“版本配套说明”中的“对源主机操作系统的要求”中新增 SUSE Linux Enterprise Server 12 GA、12 SP3 和 12 SP4 版本。
- **2024-12-30：第一次正式发布《SMTX CloudMove 1.5.0 发布说明》**

---

## 版本更新说明

# 版本更新说明

## 1.5.0-11622

- 新增 CQ Security Linux V24 操作系统支持，请查看版本配套说明。
- 修复了迁移 Anolis 8.6 虚拟机时变化数据捕获可能异常的问题。
- 修复了删除虚拟机资源时可能遗留快照的问题。

## 1.5.0-11590

- 支持在选择多个计划进行切换时对切换顺序进行编排。
- 支持将控制中心告警事件推送至 Zabbix 服务器。
- 新增 Huawei Cloud EulerOS (HCE) 2.0 、UOS 20 Desktop Pro 1050/1060 操作系统支持及其他 Linux 操作系统的发行版和不同 kernel 支持，请查看版本配套说明。
- 优化 CloudMove 代理，减少对 Windows 系统补丁的依赖，请查看版本配套说明。
- 优化迁移 Windows 虚拟机时对内存数据的处理，减少同步结束后的变化数据。
- 修复了迁移计划运行时修改计划属性可能无法保存的问题。
- 修复了批量导入迁移计划时将“切换后目标机卸载代理”选项非预期关闭的问题。

## 1.5.0-11255

- 新增 AImaLinux 8.8 和 9.6、Kylin Desktop V10 SP1 2403 操作系统支持及其他 Linux 操作系统的不同 kernel 支持，请查看版本配套说明。
- 优化了源主机处于需要通过 DNAT 规则进行端口转发的网络时对源主机与迁移计划状态的处理。

## 1.5.0-11187

- 新增 Debian 7.5 操作系统支持及其他 Linux 操作系统的不同 kernel 支持，请查看版本配套说明。
- 优化了对 SUSE Linux Enterprise Server 15 的兼容支持。
- 优化了切换时对源主机系统缓存的处理。
- 优化了对主机列表页面和迁移计划页面中主机状态的更新处理。
- 修复了数据同步前修改迁移计划属性可能无法保存的问题。

## 1.5.0-10967

- 新增 RHEL 9.6 及其他操作系统的 kernel 支持，请查看版本配套说明。
- 优化迁移源端平台为 Xen 时的迁移支持。

## 1.5.0-10898

修复了迁移 Windows 虚拟机时，切换过程中可能出现虚拟机启动失败的问题。

## 1.5.0-10857

- 新增 Oracle Linux 8.6 uek 操作系统支持，请查看版本配套说明。
- 支持为 Agent 生成离线安装包，简化源主机手动安装 Agent 的步骤。

## 1.5.0-10841

- 支持为迁移计划设置定时运行。
- 新增 AArch64 架构下多个中标麒麟 V7 小版本支持。

## 1.5.0-10768

- 新增多个中标麒麟 V7 小版本支持。
- 修复了拉取安装方式下可能存在源主机无法自动注册到控制中心的问题。

## 1.5.0-10696

- 修复了 SUSE Linux Enterprise Server 15 SP4 虚拟机可能由于目标文件目录不存在导致切换后代理服务无法启动，无法完成 IP 设置等任务的问题。
- 修复了 SUSE Linux Enterprise Server 12 SP5 虚拟机可能由于网卡配置文件参数异常导致虚拟机开机时网卡无法自动启用的问题。

## 1.5.0-10668

新增部分 Linux 版本支持，请查看版本配套说明。

## 1.5.0-10565

- 优化不同 Linux kernel 版本下同步时数据比较的相关处理。
- 新增部分 Linux 版本支持，请查看版本配套说明。

## 1.5.0-10460

修复了迁移 Windows 虚拟机时，进行切换后数据缓存盘可能无法自动卸载的问题。

## 1.5.0-10443

修复了迁移 RHEL 9 及下游发行版的虚拟机时，虚拟机卷组名称包含 `-` 符号可能导致进行切换后目标端虚拟机启动时进入紧急模式的问题。

## 1.5.0-10432

- 新增了支持的源主机操作系统：SUSE Linux Enterprise Server 15 SP6。
- 新增了特定告警平台对接及告警转发功能。修复了目标集群可能因无法挂载安装镜像导致无法安装 VMTools 的问题。
- 修复了迁移 RHEL 9 及下游发行版的虚拟机时，进行切换后非 root 逻辑卷可能未自动挂载导致目标端虚拟机启动时将进入紧急模式的问题。
- 修复了迁移 RHEL 9 及下游发行版的虚拟机时，进行切换后目标端虚拟机静态 IP 设置可能未生效的问题。
- 修复了迁移 SUSE Linux Enterprise Server 系列的虚拟机时，进行切换后目标端虚拟机的静态路由设置可能未生效的问题。

## 1.5.0-10356

修复了目标集群关联的 CloudTower 中存在以特殊字符命名的虚拟机组可能导致控制中心无法同步到目标集群信息的问题。

## 1.5.0-10308

增加了对 CloudTower 4.4.0 版本的支持：支持为目标虚拟机配置 VPC 网络。

---

## 版本配套说明 > 对 SmartX 集群类型的配套要求

# 对 SmartX 集群类型的配套要求

SMTX CloudMove 支持将以下类型的集群作为迁移的目标集群。

- SMTX OS（ELF）集群
- SMTX ELF 集群

---

## 版本配套说明 > 对 CloudTower 版本的配套要求

# 对 CloudTower 版本的配套要求

SMTX CloudMove 支持添加以下 CloudTower 版本的账户，因此目标集群所关联的 CloudTower 需符合以下版本要求。

- 4.4.0～4.4.1
- 4.5.0
- 4.6.2
- 4.7.0～4.7.1

---

## 版本配套说明 > 对服务器架构的配套要求

# 对服务器架构的配套要求

使用 SMTX CloudMove 迁移源主机前，需要在虚拟机或物理机上安装控制中心，以及在目标集群创建的虚拟代理机。源主机、控制中心所在虚拟机或物理机、虚拟代理机均支持以下两种服务器架构。

- x86\_64
- AArch64

---

## 版本配套说明 > 对操作系统的配套要求 > 对控制中心操作系统的要求

# 对控制中心操作系统的要求

SMTX CloudMove 控制中心可安装在虚拟机或物理机中，其所支持安装的虚拟机或物理机的 CPU 架构和操作系统如下表所示。

| **CPU 架构** | **操作系统** | **操作系统版本** |
| --- | --- | --- |
| x86\_64 | CentOS | 7.9 |
| RHEL | 7.9  8.2 ~ 8.8 |
| Rocky Linux | 8.9  9.4 |
| Ubuntu Server | 20.04  22.04  24.04 |
| openEuler | 20.03  22.03  24.03 |
| Anolis | 8.8 ~ 8.10 |
| Kylin Server | V10 SP2  V10 SP3 |
| UOS Server | UOS 20 1050u1a  UOS 20 1050u1e  UOS 20 1060a  UOS 20 1060e |
| AArch64 | Ubuntu Server | 20.04  22.04 |
| openEuler | 20.03 |
| Anolis | 8.8 ~ 8.10 |
| Kylin Server | V10 SP1 20210518  V10 SP2 20210524 |

---

## 版本配套说明 > 对操作系统的配套要求 > 对源主机操作系统的要求

# 对源主机操作系统的要求

SMTX CloudMove 支持将虚拟机或物理机从各类源端平台迁移至 ELF 平台，其所支持迁移的源端主机的 CPU 架构和操作系统如下表所示。

| **CPU 架构** | **操作系统** | **操作系统版本** |
| --- | --- | --- |
| x86\_64 | CentOS | 4.5  4.7  4.8  5.0 ~ 5.11  6.0 ~ 6.10  7.0 ~ 7.9  8.0 ~ 8.5  Stream 9  **说明**：CentOS 5.x 和 4.x 版本只支持推送安装，不支持拉取安装。 |
| RHEL | 4.5  4.7  4.8  5.0 ~ 5.11  6.0 ~ 6.10  7.0 ~ 7.9  8.0 ~ 8.9  9.0 ~ 9.6 |
| Rocky Linux | 8.9  9.4 |
| openEuler | 20.03  22.03 |
| Ubuntu Server | 14.04.3  14.04.4  14.04.6  16.04  18.04  20.04  22.04（内核版本为 5.15 及以下）  24.04 |
| Anolis | 7.9  8.6  8.8  8.9 |
| Debian | 7.5  10.4 |
| Oracle Linux | 6.5 ~ 6.10  7.6 ~ 7.9  8.6（uek & rhck）  8.9（uek & rhck）  9.5（uek & rhck） |
| SUSE Linux Enterprise Server | 15 SP1  15 SP2  15 SP4  15 SP5  15 SP6  11 SP2  11 SP3  12 GA  12 SP3  12 SP4  12 SP5  **说明**：   - 支持 ext4、xfs，暂不支持 btrfs。 - 对于 SUSE Linux Enterprise Server 11，要求目标主机系统盘的总线类型需为 `IDE`；而对于 `SCSI` 或 `VIRTIO`总线，系统盘可能无法启动。 |
| UOS Server | V20  **说明**： Hygon 5000 系列和 Hygon 7000 系列 CPU 仅支持搭配此版本操作系统。 |
| UOS | 20 Desktop Pro 1050/1060 |
| Kylin Server | V10 |
| Kylin Desktop | V10 SP1 2403 |
| 中标麒麟 | V7 |
| 中科方德高可信服务器 | V4.0 |
| 腾讯服务器 TencentOS Server | 3.1 (TK4) |
| Windows | 7 SP1  8  8.1  10  11 |
| Windows Server | 2008 SP2  2008 R2 SP1  2012  2012 R2  2016  2019  2022 |
| AImaLinux | 8.8  9.6 |
| Huawei Cloud Euler OS（HCE） | 2.0 |
| CQ Security Linux v24 | T24.1 R04  T24.2 Anolis 8 |
| AArch64 | CentOS | 7.9 |
| OpenEuler | 20.03  24.03（需安装 `iptable` 包） |
| UOS Server | V20  **说明**:   - 鲲鹏 916 和鲲鹏 920 CPU 仅支持搭配此版本操作系统。 - 腾云 S2500 和 FT-2000+/64 CPU 仅支持搭配此版本操作系统。 |
| Kylin Server | V10 |
| 中标麒麟 | V7 |

> **说明**：
>
> - 关于 Linux 系统支持的 Kernel 列表，请参见 [Linux 系统 Kernel 支持列表](/cloudmove/1.5.0/cloudmove_user_guide/cloudmove_user_guide_19)。
> - Windows Server 2008 需要安装 SP2 才可以数据迁移，请参考 [Windows 2008 SP2 操作指导](/cloudmove/1.5.0/cloudmove_user_guide/cloudmove_user_guide_20)进行操作。
> - Windows 7 和 Windows Server 2008 R2 需要安装 SP1 和补丁包才支持数据迁移。其中，对于 CloudMove 1.5.0-11590 以下版本，需安装 Windows 2008 R2 补丁包和 Windows 2008 R2 补丁包精简版；对于 CloudMove 1.5.0-11590 及以上版本仅需安装 KB4474419。安装过程中提示重启时建议重启，否则累积到最后一次性重启时可能导致启动时间过长或无法正常启动。
>   - [Windows 7 SP1/Windows Server 2008 R2 SP1](https://support.microsoft.com/zh-cn/topic/%E6%9C%89%E5%85%B3%E9%80%82%E7%94%A8%E4%BA%8E-windows-7-%E5%92%8C-windows-server-2008-r2-%E7%9A%84-service-pack-1-%E7%9A%84%E4%BF%A1%E6%81%AF-df044624-55b8-3a97-de80-5d99cb689063)：请首先在微软官网下载安装 SP1，然后再安装下方补丁包。
>   - [Windows 2008 R2 补丁包](https://cloudock.cn/download/windowsupdate/windows2008r2update.zip)：需要重启多次；安装代理支持拉取安装和推送安装。该补丁包中包括 MicrosoftRootCertificateAuthority2011.cer、KB2999226、KB3004394-v2、kb3138612、kb4474419-v3、kb4490628、kb4565354、kb3125574-v4，可自行到微软官网下载按顺序安装。
>   - [Windows 2008 R2 补丁包精简版](https://cloudock.cn/download/windowsupdate/windows2008r2update-base.zip)：精简版，需要重启一次；安装代理只能使用拉取安装，不能使用推送安装。该补丁包中包括 KB2999226、KB4474419、KB4490628，可自行到微软官网下载按顺序安装。
>   - [KB4474419](https://cloudock.cn/download/windowsupdate/windows6.1-kb4474419-v3-x64.msu)：单击左侧链接下载，或在微软官网进行下载。
> - 当 CloudMove 为 1.5.0-11590 以下版本时，Windows 2012 R2 需要安装以下补丁包，注意安装提示重启时建议重启，否则累积到最后一次性重启时可能导致启动时间过长或无法正常启动：
>   - [Windows 2012 R2 补丁包](https://cloudock.cn/download/windowsupdate/windows2012r2update-base.zip)：该补丁包中包括 KB2919442、KB2919355、KB2999226 及相关依赖。Windows 8.1 平台请自行更新。

---

## 版本配套说明 > 对操作系统的配套要求 > 对虚拟代理机操作系统的要求

# 对虚拟代理机操作系统的要求

虚拟代理机支持的操作系统和源主机的操作系统有关，具体要求如下：

- 若源主机的操作系统是 **Windows**，则要求虚拟代理机的操作系统为 Windows 2019，CPU 架构为 x86\_64。
- 若源主机的操作系统为 **Linux**，则虚拟代理机的操作系统需为源主机操作系统的相同或上游版本，或如下表列出的操作系统：

  | 源主机 | 虚拟代理机 | |
  | --- | --- | --- |
  | 操作系统 | 操作系统 | CPU 架构 |
  | CentOS 系列, RHEL 8.x | Ubuntu Server 20.04 | x86\_64 |
  | CentOS 系列, RHEL 系列, openEuler 系列 | CentOS 8.2 | x86\_64 |
  | CentOS 系列, RHEL 系列, Rocky Linux 9.x | Ubuntu Server 24.04, openEuler 24.03 | x86\_64 |
  | RHEL 系列, CentOS Stream 系列, Rocky Linux 系列, AlmaLinux 系列 | - Ubuntu Server 22.04, 24.04 - openEuler 22.03, 24.03 | x86\_64 |
  | Kylin Server V10 | Kylin Server V10 | - x86\_64 - AArch64 |
  | UOS Server V20 | UOS Server V20 | - x86\_64 - AArch64 |
  | 所有 Linux 发行版 | - Ubuntu Server 20.04, 22.04 - openEuler 20.03, 22.03 - Anolis 8.8, 8.9 | x86\_64 |

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
