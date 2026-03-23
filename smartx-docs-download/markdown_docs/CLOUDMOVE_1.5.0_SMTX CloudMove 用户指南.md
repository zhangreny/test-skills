---
title: "CLOUDMOVE/1.5.0/SMTX CloudMove 用户指南"
source_url: "https://internal-docs.smartx.com/cloudmove/1.5.0/cloudmove_user_guide/cloudmove_user_guide_preface"
sections: 28
---

# CLOUDMOVE/1.5.0/SMTX CloudMove 用户指南
## 关于本文档

# 关于本文档

本文档主要介绍了 SMTX CloudMove 的功能，以及如何使用该工具将虚拟机或物理机从各类源端平台迁移至 ELF 平台。

阅读本文档的对象需了解 SMTX OS 超融合软件和 SMTX ELF 虚拟化软件的相关技术背景知识，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

- **2025-11-12：更新“迁移要求”和“附录”**

  - 在“迁移要求”中，更新“对 CloudTower 版本的配套要求”，以及“对操作系统的要求”中的“对控制中心操作系统的要求”和“对源主机操作系统的要求”。
  - 在“附录”中，更新“Linux 操作系统 kernel 支持列表”。
- **2025-08-18：更新“迁移要求”和“附录”**

  - 在“迁移要求“中，更新“对操作系统的要求”中的“对控制中心操作系统的要求”和“对虚拟代理机操作系统的要求”。
  - 在“附录”中，更新“Linux 操作系统 kernel 支持列表”。
- **2025-08-07：更新“迁移要求”**

  在“对操作系统的要求”中的“对源主机操作系统的要求”中，更新兼容的操作系统版本。
- **2025-07-01：更新“迁移要求”**

  - 在“对 CloudTower 版本的配套要求”中新增 4.6.0 版本。
  - 在“对操作系统的要求”中的“对控制中心操作系统的要求”中，x86\_64 架构兼容的版本新增 Ubuntu Server 24.04、openEuler 24.03。
  - 在“对操作系统的要求”中的“对源主机操作系统的要求”中，x86\_64 架构兼容的版本新增 Oracle Linux 8.6 uek、RHEL 9.6。
- **2025-03-17：更新“迁移要求”**

  - 在“对 CloudTower 版本的配套要求”中新增 4.5.0 版本。
  - 在“对操作系统的要求”中的“对源主机操作系统的要求”中新增 SUSE Linux Enterprise Server 12 GA、12 SP3 和 12 SP4 版本。
- **2024-12-30：第一次正式发布《SMTX CloudMove 1.5.0 用户指南》**

---

## SMTX CloudMove 简介

# SMTX CloudMove 简介

SMTX CloudMove 是一款用于跨平台迁移业务主机的工具，支持将虚拟机或物理机从各类源端平台迁移至 ELF 平台。

## 产品特点

- **强大的平台兼容性**

  SMTX CloudMove 支持从任意虚拟化平台、云平台和物理机上迁移业务主机，且不受 Hypervisor 品牌限制，仅对操作系统有兼容性要求，具有更广泛的适用场景和更强的兼容性。
- **迁移不停机**

  SMTX CloudMove 可以对迁移中的源主机进行连续数据保护（CDP），实现整机级别的在线迁移。
- **迁移自动化**

  迁移时，SMTX CloudMove 控制中心会自动在目标集群创建目标虚拟机，实现源主机到目标虚拟机的自动迁移，人工干预少，自动化效率高。

## 产品组件

SMTX CloudMove 主要由以下组件构成：

- **管理界面**

  管理界面是基于 Web 的图形管理界面，用户可以使用它创建、配置、管理和监控迁移计划。用户可以通过浏览器远程访问管理界面。
- **控制中心**

  控制中心通过与代理和管理界面的通讯，控制在混合云或多云中的迁移计划。它记录了所有待迁移的源主机信息、迁移计划信息、备份目标信息与账户信息，同时负责所有迁移计划的管理，包括创建、配置、监控等操作。
- **代理**

  代理（Agent）是迁移解决方案的核心组件。它需要安装在参与迁移计划的源主机和虚拟代理机上。Agent 在源主机会加载卷级 CDP 驱动，Agent 和驱动配合捕捉用户产生的数据，通过网络发送和接受数据，以及写入数据到 ELF 平台上的块设备，并通过 ELF 平台的 API 对平台上的虚拟资源进行管理、配置等操作。

## 迁移原理

在 SMTX CloudMove 控制中心运行迁移计划后，SMTX CloudMove Agent 会在源主机加载卷级驱动，持续抓取生产数据改变，并将源主机的数据备份到目标集群的虚拟代理机上，虚拟卷此时会挂载到虚拟代理机上，同时目标集群上会创建一个目标虚拟机，该虚拟机的计算资源与源主机相同，但不具备磁盘。Agent 会以连续数据保护（CDP）的方式将源主机的数据实时同步至目标虚拟机，两者的数据延时大约为 2 ～ 3 秒。当对迁移计划执行切换后，虚拟卷将从虚拟代理机上卸载并挂载至目标虚拟机，挂载完成后目标虚拟机将自动启动。

![](https://cdn.smartx.com/internal-docs/assets/7deeb18d/cloudmove_user_guide_05.png)

---

## 迁移要求

# 迁移要求

在安装 SMTX CloudMove 之前，请先了解该工具的使用要求。

---

## 迁移要求 > 对 SmartX 集群类型的配套要求

# 对 SmartX 集群类型的配套要求

SMTX CloudMove 支持将以下类型的集群作为迁移的目标集群。

- SMTX OS（ELF）集群
- SMTX ELF 集群

---

## 迁移要求 > 对 CloudTower 版本的配套要求

# 对 CloudTower 版本的配套要求

SMTX CloudMove 支持添加以下 CloudTower 版本的账户，因此目标集群所关联的 CloudTower 需符合以下版本要求。

- 4.4.0～4.4.1
- 4.5.0
- 4.6.2
- 4.7.0～4.7.1

---

## 迁移要求 > 对服务器架构的配套要求

# 对服务器架构的配套要求

使用 SMTX CloudMove 迁移源主机前，需要在虚拟机或物理机上安装控制中心，以及在目标集群创建的虚拟代理机。源主机、控制中心所在虚拟机或物理机、虚拟代理机均支持以下两种服务器架构。

- x86\_64
- AArch64

---

## 迁移要求 > 对硬件的要求

# 对硬件的要求

SMTX CloudMove 的控制中心支持安装的虚拟机或物理机、源主机和虚拟代理机的硬件要求如下。

| 组件 | 平台 | CPU | 内存 | 硬盘空间 |
| --- | --- | --- | --- | --- |
| 控制中心 | Linux | 最小：4 核  建议：8 核以上 | 最小：8 GB  建议：12 GB 以上 | 50 GB |
| 源主机 | Linux/Windows | - | 最小：1 GB  **说明**：如果源主机总内存只有最多 1 GB，请确保停止生产软件系统，停止生产数据更新，否则可能会因生产数据变化大导致内存耗尽，系统异常或崩溃。建议源主机最小剩余 1GB 内存 | /opt 分区或 C:\ 盘：剩余 1 GB  数据缓存：最小 2 GB |
| 虚拟代理机 | Linux/Windows | 最小：2 核 | 最小：4 GB | /opt 分区或 C:\ 盘：剩余 1 GB  数据缓存：最小 2 GB |

---

## 迁移要求 > 对操作系统的要求

# 对操作系统的要求

SMTX CloudMove 对控制中心、源主机和虚拟代理机的操作系统的要求如下。

---

## 迁移要求 > 对操作系统的要求 > 对控制中心操作系统的要求

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

## 迁移要求 > 对操作系统的要求 > 对源主机操作系统的要求

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

## 迁移要求 > 对操作系统的要求 > 对虚拟代理机操作系统的要求

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

## 迁移要求 > 对网络环境的要求

# 对网络环境的要求

- SMTX CloudMove 的控制中心需与迁移源端的主机和迁移目标端集群的主机互相连通。
- 虚拟代理机的虚拟机网络需要和源主机、目标集群关联的 CloudTower 虚拟机、控制中心所在的物理机或虚拟机的虚拟机网络连通。
- 迁移虚拟机前，请检查 CloudTower 是否已开启白名单访问限制。若已开启，则请将控制中心和虚拟代理机的 IP 地址添加至白名单。
- 迁移虚拟机前，请检查控制中心和源主机、目标机之间是否使用 NAT，并根据不同场景在相应主体上开放 TCP 端口。

  - **未使用 NAT**

    | 主体 | 操作系统 | 需要开放的 TCP 端口 | 描述 |
    | --- | --- | --- | --- |
    | CloudTower | - | 80、443 | 控制中心和虚拟代理机通过该端口访问 CloudTower。 |
    | 控制中心 | Linux | 8443 | 用户端通过该端口访问控制中心 |
    | 源主机 | Windows | 5895 | WinRM 远程管理端口 |
    | 7822 | 临时性端口。在远程推送 Agent 时打开，用于接收 Agent 安装包，安装完成后自动关闭 |
    | 1984 | Agent 工作端口。 |
    | Linux | 22 | 控制中心远程连接和推送 Agent 使用 |
    | 1984 | Agent 工作端口 |
    | 虚拟代理机 | Windows | 5895 | WinRM 远程管理端口 |
    | 7822 | 临时性端口。在远程推送 Agent 时打开，用于接收 Agent 安装包，安装完成后自动关闭 |
    | 1984 | Agent 工作端口 |
    | Linux | 22 | 控制中心远程连接和推送 Agent 使用 |
    | 1984 | Agent 工作端口。 |
  - **使用 NAT**

    | 主体 | 操作系统 | 需要开放的 TCP 端口 | 描述 |
    | --- | --- | --- | --- |
    | CloudTower | - | 80、443 | 控制中心和虚拟代理机通过该端口访问 CloudTower。 |
    | 控制中心 | Linux | 8443 | 控制中心对外服务端口 |
    | 源主机 | Windows | 1984 | Agent 工作端口 |
    | Linux |
    | 虚拟代理机 | Windows | 5895 | WinRM 远程管理端口 |
    | 7822 | 临时性端口。在远程推送 Agent 时打开，用于接收 Agent 安装包，安装完成后自动关闭 |
    | 1984 | Agent 工作端口。 |
    | Linux | 22 | 控制中心远程连接和推送 Agent 使用 |
    | 1984 | Agent 工作端口 |

---

## 迁移要求 > 对浏览器的要求

# 对浏览器的要求

SMTX CloudMove 安装完成后，需要使用浏览器登录管理界面，支持的浏览器包括 Google Chrome、Microsoft Edge 和 Mozilla Firefox。

---

## 安装 SMTX CloudMove 控制中心

# 安装 SMTX CloudMove 控制中心

SMTX CloudMove 控制中心支持通过离线安装的方式，安装在虚拟机或物理机中。

**前提条件**

待安装的虚拟机或物理机需与迁移源端的主机、迁移目标端集群的主机相互连通，并且满足[安装控制中心](/cloudmove/1.5.0/cloudmove_release_notes/cloudmove_user_guide/cloudmove_user_guide_22)的要求。

**操作步骤**

1. 根据待安装的虚拟机所在的主机或物理机的 CPU 架构和操作系统，提前获取对应的安装包。
2. 将安装包上传至待安装的虚拟机所在的主机或物理机的任意目录下。
3. 执行以下命令，安装 SMTX CloudMove 控制中心。

   ```
   tar xf easync.tar && chmod +x offline-install.sh
   ./offline-install.sh
   ```

   安装过程中，系统会提示您设置控制中心的访问密码；安装结束后，系统将自动显示控制中心的网址，默认网址为 [*https://ip:8443*](https://ip:8443)。
4. 登录 SMTX CloudMove 控制中心，系统将自动跳转至**产品许可证**页面，请通过以下两种方式获取产品许可。

   - **在线方式**

     使用在线方式获取许可码时，要求 SMTX CloudMove 控制中心能访问互联网。您可直接联系 SmartX 售后工程师获取许可码进行在线激活。

     推荐优先使用此方式获取许可码。
   - **离线方式**

     如果 SMTX CloudMove 控制中心不能访问互联网，请单击**产品许可证**页面下方的**查看机器码**，复制机器码信息并联系 SmartX 售后工程师生成注册码用于激活。
5. 在**产品许可证**的区域框中输入许可码，单击**激活产品**，激活控制中心。

   激活 SMTX CloudMove 控制中心后，**产品许可证**的区域框右边将显示本许可码支持的迁移模式、节点数和过期时间。

---

## 迁移前的准备 > 在目标集群创建虚拟代理机

# 在目标集群创建虚拟代理机

**前提条件**

创建虚拟代理机时，需登录迁移目标集群所关联的 CloudTower 管理平台，请提前获取 CloudTower 的 IP 地址、用户名和密码。

**操作步骤**

1. 在浏览器中输入迁移目标集群所关联的 CloudTower 管理平台的 IP 地址，登录 CloudTower。
2. 在 CloudTower 左侧导航栏中选中目标集群，进入目标集群的管理界面。单击右上方的 **+ 创建**，选择创建空白虚拟机，弹出**创建空白虚拟机**对话框。
3. 填写虚拟机的配置信息，包括基本信息、计算资源、磁盘、网络设备等信息。

   创建的虚拟机将作为虚拟代理机，其相关的配置需符合[硬件要求](/cloudmove/1.5.0/cloudmove_user_guide/cloudmove_user_guide_05)和[操作系统要求](/cloudmove/1.5.0/cloudmove_release_notes/cloudmove_user_guide/cloudmove_user_guide_24#%E5%AF%B9%E8%99%9A%E6%8B%9F%E4%BB%A3%E7%90%86%E6%9C%BA%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F%E7%9A%84%E8%A6%81%E6%B1%82)。
4. 填写完所有的配置信息后，单击右下角的**创建虚拟机**。
5. 为创建的虚拟机安装操作系统，即可完成虚拟代理机的创建。

---

## 迁移前的准备 > 在控制中心添加 CloudTower 账户

# 在控制中心添加 CloudTower 账户

1. 登录 SMTX CloudMove 控制中心，在页面顶部选择**整机迁移**页签，进入迁移页面。
2. 在控制中心左侧导航栏中选择**虚拟化模式** > **云平台账户**，开始添加 CloudTower 账户。
3. 在**云平台账户**界面右上角单击**创建账户**，弹出**新账户**对话框。
4. 输入 CloudTower 账户名称，在**目标类型**下拉框中选择 **SmartX 超融合**，同时输入 CloudTower IP、登录 CloudTower 的用户名和密码。
5. 单击**验证**，确认以上步骤中输入的 CloudTower 账户信息正确无误后，选择**保存**。

   保存账户成功后，新添加的 CloudTower 账户将会显示在**云平台账户**页面的账户信息列表中。

---

## 迁移步骤

# 迁移步骤

完成迁移前的准备工作后，请登录 SMTX CloudMove 控制中心，参考以下步骤迁移源主机。

---

## 迁移步骤 > 第 1 步：添加备份目标

# 第 1 步：添加备份目标

1. 在 SMTX CloudMove 控制中心的顶部导航栏单击**整机迁移**，然后在左侧导航栏的**虚拟化模式**菜单下单击**备份目标**。
2. 在**备份目标**界面右上角单击**添加目标**，在弹出的**新目标**窗口中，设置目标名称，并在**云平台账户**选项中选择迁移的目标集群所关联的 CloudTower 平台账户。

   SMTX CloudMove 将使用所选择的平台账户信息连接 CloudTower，连接成功后将显示**集群**选项，以及**虚拟代理实例**、**目标虚拟机设置**的设置。
3. 在**集群**选项中选择迁移的目标集群。
4. 在**虚拟代理实例**设置中，选择在目标集群上创建的虚拟代理机，并输入虚拟代理机的 IP 地址、用户名和密码。
5. 在**目标虚拟机设置**设置中，在**硬盘类型**选项中选择目标虚拟机需采用的存储策略。如目标集群已创建虚拟机组，你也可以为目标虚拟机选择虚拟机组。
6. 单击**保存**。

   SMTX CloudMove 将自动向虚拟代理机推送 Agent，Agent 安装过程耗时约几十秒至两分钟，您可以在**虚拟代理机**界面查看安装进度，当在虚拟代理机的**代理**一列可以查看到版本号和绿色图标时，表明 Agent 安装成功。若安装失败，请按错误提示排查原因并解决问题，然后再勾选该虚拟代理机，在界面右上角单击**远程安装代理**。

---

## 迁移步骤 > 第 2 步：添加源主机

# 第 2 步：添加源主机

1. 确认需要迁移的源主机已开机。
2. 在控制中心的**整机迁移**界面的左侧导航栏单击**源主机**，然后在界面右上角单击**添加源主机**。
3. 根据当前网络环境以及是否可获取源主机管理员账户选择添加源主机的方式。

   - **推送安装**：若控制中心可以直接与源主机建立连接，并且您可以获取源主机的管理员账户，请选择此方式，然后参考以下步骤执行操作。
     1. 输入源主机的 IP 和显示名称。
     2. 选择远端连接协议。

        - **OpenSSH (Linux)**：若源主机是 Linux 操作系统，请选择此协议。
        - **Windows Remote Management (HTTP)**：若源主机是 Windows 操作系统，请选择此协议。
     3. 输入源主机的用户名、密码或密钥、以及 SSH 端口号。
     4. 勾选**保存时自动安装代理**、**强制安装**，单击**保存**。

        SMTX CloudMove 将会自动向源主机推送 Agent，Agent 安装过程耗时约 1 ～ 2 分钟，当在源主机的**代理**一列可以查看到版本号和绿色图标时，表明 Agent 安装成功。若安装失败，请按错误提示排查原因并解决问题，然后再勾选该源主机，在界面右上角单击**远程安装代理**。
   - **拉取安装**：若控制中心无法直接与源主机建立连接，或者您无法获取源主机的管理员账户，请选择此方式，然后在弹出的窗口中，根据界面提示在源主机端手动安装 Agent。

---

## 迁移步骤 > 第 3 步：创建迁移计划

# 第 3 步：创建迁移计划

1. 在控制中心的**整机迁移**界面的左侧导航栏单击**源主机**，勾选需要迁移的源主机，然后在界面右上角单击**创建计划**。
2. 在弹出的**创建计划**窗口中，选择**虚拟化模式**，然后为计划选择分组，并选择[第 1 步](/cloudmove/1.5.0/cloudmove_user_guide/cloudmove_user_guide_12)添加的备份目标。

   > **说明**：
   >
   > 您可以在左侧导航栏的**虚拟化模式** > **计划**界面创建计划分组，若无分组需求，该计划分组可以选择 **Default group**。
3. 单击**创建计划**。

   创建完成后，您可以在左侧导航栏的**虚拟化模式** > **计划**界面的对应分组下查看到刚刚创建的计划。

---

## 迁移步骤 > 第 4 步：配置虚拟机网络

# 第 4 步：配置虚拟机网络

1. 在**整机迁移**界面的左侧导航栏中选择**虚拟化模式** > **计划**，选择[第 3 步](/cloudmove/1.5.0/cloudmove_user_guide/cloudmove_user_guide_14)中创建的迁移计划并展开，选择虚拟代理机。
2. 在右侧的属性页面中选择**虚拟机**页签。
3. 在**网卡设置**中选择**常规网络**后，单击**增加网卡**。
4. 在弹出的**网卡配置**对话框中配置网卡信息，其中**子网**需要选择目标集群中的虚拟机网络。

   ![](https://cdn.smartx.com/internal-docs/assets/7deeb18d/cloudmove_user_guide_01.png)
5. 网卡配置完成后单击**确认**，然后在**虚拟机**页签中单击**保存**。
6. （可选）如果计划在执行切换前进行演练，还需要在**网卡设置**中选择**演练网络**，然后参考上述步骤 3 ～ 5 增加并配置网卡。

   > **注意**：
   >
   > 在配置演练网络网卡的子网时，需要选择与生产网络和常规网络不同虚拟机网络，避免产生冲突。

---

## 迁移步骤 > 第 5 步：运行迁移计划

# 第 5 步：运行迁移计划

1. 在展开的迁移计划中选择源主机，在右侧的属性页面中配置磁盘 IO 限速并选择所需要复制的卷后，单击**保存**。

   - **磁盘 IO 限速**：默认为**不限速**，可选择**分时段限速（按源主机时间）** 或**全时段限速**。
   - **已经选择的卷**：默认选择源主机上的所有卷。如果需要修改，可单击下方的**修改**按钮，根据实际需求选择所要复制的卷。
2. 在界面上方单击**运行**，在弹出的对话框中选择同步方式后，单击**确定**运行迁移计划。

   - **智能比较**：自动根据计划的运行情况以及计划的类型等不同情况智能地进行数据比较，追求最佳的同步效果，如果您不能判断应该使用何种同步方式时，可选择此方式。
   - **比较**：对源主机和目标主机的数据进行比较，只同步不同的数据，对于数据恢复计划，一般选择此种方式。
   - **不比较**：不会对源主机和目标主机的数据进行比较，直接发送源主机的有效数据，第一次运行计划的时候一般选择此种方式。

   在运行过程中，可单击迁移计划，在右侧属性页面的**状态**页签中查看事件，了解计划运行进度。
3. 运行完成后，迁移计划将显示**切换准备就绪**，目标集群中将创建一台与源主机配置相同（除磁盘外）的目标虚拟机，该虚拟机名称默认为 `源主机名称_vm`。

   ![](https://cdn.smartx.com/internal-docs/assets/7deeb18d/cloudmove_user_guide_02.png)

---

## 迁移步骤 > 第 6 步：（可选）执行演练

# 第 6 步：（可选）执行演练

在执行切换前，可通过演练验证迁移数据的可用性和一致性。

1. 选择已完成运行的迁移计划，在界面右上角选择**虚拟机** > **启动演练**，在弹出的对话框中勾选**手动演练**后，单击**确定**启动演练。
2. 启动演练后，迁移计划将显示**演练中**，系统会为目标虚拟机挂载与源主机相同的虚拟卷，您可以对虚拟机中的数据和应用进行验证。

   ![](https://cdn.smartx.com/internal-docs/assets/7deeb18d/cloudmove_user_guide_03.png)
3. 验证完成后，在界面右上角选择**虚拟机** > **停止演练**，系统会将目标虚拟机关机并清除其中的数据。

---

## 迁移步骤 > 第 7 步：执行切换

# 第 7 步：执行切换

1. 选择已完成运行的迁移计划，在界面上方单击**切换**，在弹出的对话框中单击**确定**后，执行切换。

   在切换过程中，可单击迁移计划，在右侧面板的**状态**页签中查看事件，了解切换进度。
2. 切换完成后，迁移计划将显示**切换结束**，系统会为目标虚拟机挂载虚拟卷并开机。

   ![](https://cdn.smartx.com/internal-docs/assets/7deeb18d/cloudmove_user_guide_04.png)

---

## 附录 > Linux Windows 2008 SP2 操作指导

# Windows 2008 SP2 操作指导

操作系统为 Windows 2008 的源主机必须安装 SP2 才支持数据迁移。在迁移源主机之前，请按照以下操作指导完成安装和设置。

## 安装 Windows 2008 SP2

1. 下载并安装 [Windows 2008 SP2](https://www.microsoft.com/en-us/download/details.aspx?id=5104)。
2. 下载 [Windows 2008 SP2 补丁包](https://cloudock.cn/download/windowsupdate/windows2008update.zip)，并按照顺序依次完成安装，该补丁包包括以下文件：

   - MicrosoftRootCertificateAuthority2011.cer 根证书更新
   - mpsyschk.exe
   - KB968930
   - KB4493730
   - KB4474419-v4
   - KB4039648-v2

## 安装 Agent

安装 Windows 2008 SP2 后，请参照下述步骤手动安装 Agent。

1. 将代理安装包复制到源主机。Windows代理安装包位于控制中心以下路径：

   `/opt/cloudock/easync/cc/download/easync-agent-<version>.windows.x86_64.exe`
2. 双击 `easync-agent-<version>.windows.x86_64.exe` 进行安装。并在弹出的安装对话框中选择**始终安装此驱动程序软件**以完成安装。
3. 将控制中心主机上的两个证书文件复制到源主机的相应目录中。

   - 证书文件：

     `/opt/cloudock/easync/cc/data/easync-g.crt`

     `/opt/cloudock/easync/cc/data/easync-g.key`
   - 源主机目录：

     `C:\Program Files\Cloudock\Easync\agent\data\`
4. 在 Windows 服务界面，重启 Agent 服务。

## 添加数据缓存盘

请参考下述步骤为源主机添加硬盘，以用于数据缓存。

1. 在源主机上添加一块大小为 16 GB 的硬盘。若源主机在迁移期间有大量数据写入，可以适当增加硬盘的容量。
2. 进入源主机的操作系统，为这块硬盘分区分配盘符，例如 `S:`。

## 选择缓存路径

完成数据缓存盘的添加后，请参考[迁移步骤](/cloudmove/1.5.0/cloudmove_user_guide/cloudmove_user_guide_11)进行数据迁移。需注意，在完成**第 3 步：创建迁移计划**后，需要为源主机选择缓存路径，操作步骤如下。

1. 在**虚拟化模式** > **计划**界面选择已创建的迁移计划，选择源主机，在**缓存路径**输入框中填写源主机添加的数据缓存盘的盘符。
2. 在**已选择卷**字段，确认第一步中添加的数据盘没有被选择。若已被选择，请单击**修改**并取消选择该数据盘。
3. 单击**保存**。

---

## 附录 > Linux 操作系统 kernel 支持列表

# Linux 操作系统 kernel 支持列表

## 一般规则

- 对于受支持的 Linux 操作系统，SMTX CloudMove 支持随官方安装文件发布的官方 kernel。
- 对于 RHEL/CentOS 5 ~ 7，安装后通过 repo 升级的 kernel 一般不需要重新编译对应驱动；对于 RHEL/CentOS 8 ~ 9，大部分情况需要重新编译驱动。
- 对于 Ubuntu 系列，不在下方支持列表的 kernel 需要编译对应驱动。
- 对于其余操作系统，安装后通过 repo 升级的 kernel **有可能** 需要重新编译对应驱动。

## CentOS 平台支持的 elrepo kernel 列表

对于 CentOS 7，除了官方发布的各个 kernel 版本，还支持以下 elrepo kernel：

```
4.17.11-1.el7.elrepo.x86_64
4.18.8-1.el7.elrepo.x86_64
4.19.12-1.el7.elrepo.x86_64
5.17.5-1.el7.elrepo.x86_64
5.4.100-1.el7.elrepo.x86_64
5.4.170-1.el7.elrepo.x86_64
5.4.212-1.el7.elrepo.x86_64
5.4.221-1.el7.elrepo.x86_64
5.4.254-1.el7.elrepo.x86_64
5.4.113-1.el7.elrepo.x86_64
5.4.231-1.el7.elrepo.x86_64
5.4.272-1.el7.elrepo.x86_64
5.17.2-1.el7.elrepo.x86_64
6.8.6-1.el7.elrepo.x86_64
```

## 银河麒麟 v10 支持的 kernel 列表

```
4.19.90-17.ky10.x86_64
4.19.90-23.6.v2101.ky10.x86_64
4.19.90-23.8.v2101.ky10.x86_64
4.19.90-23.32.v2101.ky10.x86_64
4.19.90-23.34.v2101.ky10.x86_64
4.19.90-23.49.v2101.ky10.x86_64
4.19.90-23.51.v2101.ky10.x86_64
4.19.90-24.4.v2101.ky10.x86_64
4.19.90-25.9.v2101.ky10.x86_64
4.19.90-25.18.v2101.ky10.x86_64
4.19.90-25.25.v2101.ky10.x86_64
4.19.90-25.40.v2101.ky10.x86_64
4.19.90-25.43.v2101.ky10.x86_64
4.19.90-25.48.v2101.ky10.x86_64
4.19.90-52.15.v2207.ky10.x86_64
4.19.90-52.22.v2207.ky10.x86_64
4.19.90-52.23.v2207.gfb01.ky10.x86_64
4.19.90-52.39.v2207.ky10.x86_64
4.19.90-52.42.v2207.ky10.x86_64
4.19.90-52.46.v2207.ky10.x86_64
4.19.90-52.48.v2207.ky10.x86_64
4.19.90-52.52.v2207.ky10.x86_64
4.19.90-89.11.v2401.ky10.x86_64
4.19.90-89.24.v2401.ky10.x86_64
```

## 统信 UOS 20a、e 系列支持的 kernel 列表

```
4.19.0-91.77.77.uelc20.x86_64
4.19.0-91.82.65.uelc20.x86_64
4.19.0-91.82.92.uelc20.x86_64
4.19.0-91.82.132.uelc20.x86_64
4.19.0-91.82.152.uelc20.x86_64
4.19.0-91.82.179.3.uelc20.x86_64
4.19.90-2109.1.0.0108.up2.uel20.x86_64
4.19.90-2201.4.0.0135.up1.uel20.x86_64
4.19.90-2207.3.0.0159.up1.uel20.x86_64
4.19.90-2207.4.0.0160.up1.uel20.x86_64
4.19.90-2211.5.0.0178.22.uel20.x86_64
4.19.90-2305.1.0.0199.56.uel20.x86_64
4.19.90-2403.3.0.0270.84.uel20.x86_64
4.19.90-2403.3.0.0270.87.uel20.x86_64
5.10.0-4.uelc20.x86_64
5.10.0-18.uel20.x86_64
5.10.0-18.uelc20.x86_64
5.10.0-27.uel20.x86_64
5.10.0-27.uelc20.x86_64
5.10.0-46.uel20.x86_64
5.10.0-46.uelc20.x86_64
5.10.0-74.3.uel20.x86_64
5.10.0-74.3.uelc20.x86_64
```

## Ubuntu Server LTS x64 支持的 kernel 列表

对于 Ubuntu Server LTS 系列，支持以下 kernel。由于存在 kernel backport，同一 kernel 将可能运行在某些不同 Ubuntu Server 版本上。

```
3.19.0-25-generic
4.2.0-27-generic
4.4.0-21-generic
4.4.0-22-generic
4.4.0-24-generic
4.4.0-28-generic
4.4.0-31-generic
4.4.0-34-generic
4.4.0-36-generic
4.4.0-38-generic
4.4.0-42-generic
4.4.0-43-generic
4.4.0-45-generic
4.4.0-47-generic
4.4.0-51-generic
4.4.0-53-generic
4.4.0-57-generic
4.4.0-59-generic
4.4.0-62-generic
4.4.0-63-generic
4.4.0-64-generic
4.4.0-66-generic
4.4.0-67-generic
4.4.0-70-generic
4.4.0-71-generic
4.4.0-72-generic
4.4.0-75-generic
4.4.0-77-generic
4.4.0-78-generic
4.4.0-79-generic
4.4.0-81-generic
4.4.0-83-generic
4.4.0-87-generic
4.4.0-89-generic
4.4.0-91-generic
4.4.0-92-generic
4.4.0-93-generic
4.4.0-96-generic
4.4.0-97-generic
4.4.0-98-generic
4.4.0-101-generic
4.4.0-103-generic
4.4.0-104-generic
4.4.0-108-generic
4.4.0-109-generic
4.4.0-112-generic
4.4.0-116-generic
4.4.0-117-generic
4.4.0-119-generic
4.4.0-121-generic
4.4.0-122-generic
4.4.0-124-generic
4.4.0-127-generic
4.4.0-128-generic
4.4.0-130-generic
4.4.0-131-generic
4.4.0-133-generic
4.4.0-134-generic
4.4.0-135-generic
4.4.0-137-generic
4.4.0-138-generic
4.4.0-139-generic
4.4.0-140-generic
4.4.0-141-generic
4.4.0-142-generic
4.4.0-143-generic
4.4.0-145-generic
4.4.0-146-generic
4.4.0-148-generic
4.4.0-150-generic
4.4.0-151-generic
4.4.0-154-generic
4.4.0-157-generic
4.4.0-159-generic
4.4.0-161-generic
4.4.0-164-generic
4.4.0-165-generic
4.4.0-166-generic
4.4.0-168-generic
4.4.0-169-generic
4.4.0-170-generic
4.4.0-171-generic
4.4.0-173-generic
4.4.0-174-generic
4.4.0-176-generic
4.4.0-177-generic
4.4.0-178-generic
4.4.0-179-generic
4.4.0-184-generic
4.4.0-185-generic
4.4.0-186-generic
4.4.0-187-generic
4.4.0-189-generic
4.4.0-190-generic
4.4.0-193-generic
4.4.0-194-generic
4.4.0-197-generic
4.4.0-198-generic
4.4.0-200-generic
4.4.0-201-generic
4.4.0-203-generic
4.4.0-204-generic
4.4.0-206-generic
4.4.0-208-generic
4.4.0-209-generic
4.4.0-210-generic
4.8.0-34-generic
4.8.0-36-generic
4.8.0-39-generic
4.8.0-41-generic
4.8.0-42-generic
4.8.0-44-generic
4.8.0-45-generic
4.8.0-46-generic
4.8.0-49-generic
4.8.0-51-generic
4.8.0-52-generic
4.8.0-53-generic
4.8.0-54-generic
4.8.0-56-generic
4.8.0-58-generic
4.10.0-14-generic
4.10.0-19-generic
4.10.0-20-generic
4.10.0-21-generic
4.10.0-22-generic
4.10.0-24-generic
4.10.0-26-generic
4.10.0-27-generic
4.10.0-28-generic
4.10.0-30-generic
4.10.0-32-generic
4.10.0-33-generic
4.10.0-35-generic
4.10.0-37-generic
4.10.0-38-generic
4.10.0-40-generic
4.10.0-42-generic
4.11.0-13-generic
4.11.0-14-generic
4.13.0-16-generic
4.13.0-17-generic
4.13.0-19-generic
4.13.0-21-generic
4.13.0-25-generic
4.13.0-26-generic
4.13.0-31-generic
4.13.0-32-generic
4.13.0-36-generic
4.13.0-37-generic
4.13.0-38-generic
4.13.0-39-generic
4.13.0-41-generic
4.13.0-43-generic
4.13.0-45-generic
4.15.0-13-generic
4.15.0-15-generic
4.15.0-20-generic
4.15.0-22-generic
4.15.0-23-generic
4.15.0-24-generic
4.15.0-29-generic
4.15.0-30-generic
4.15.0-32-generic
4.15.0-33-generic
4.15.0-34-generic
4.15.0-36-generic
4.15.0-38-generic
4.15.0-39-generic
4.15.0-42-generic
4.15.0-43-generic
4.15.0-44-generic
4.15.0-45-generic
4.15.0-46-generic
4.15.0-47-generic
4.15.0-48-generic
4.15.0-50-generic
4.15.0-51-generic
4.15.0-52-generic
4.15.0-54-generic
4.15.0-55-generic
4.15.0-58-generic
4.15.0-60-generic
4.15.0-62-generic
4.15.0-64-generic
4.15.0-65-generic
4.15.0-66-generic
4.15.0-69-generic
4.15.0-70-generic
4.15.0-72-generic
4.15.0-74-generic
4.15.0-76-generic
4.15.0-88-generic
4.15.0-91-generic
4.15.0-96-generic
4.15.0-99-generic
4.15.0-101-generic
4.15.0-106-generic
4.15.0-107-generic
4.15.0-108-generic
4.15.0-109-generic
4.15.0-111-generic
4.15.0-112-generic
4.15.0-115-generic
4.15.0-117-generic
4.15.0-118-generic
4.15.0-120-generic
4.15.0-121-generic
4.15.0-122-generic
4.15.0-123-generic
4.15.0-124-generic
4.15.0-125-generic
4.15.0-126-generic
4.15.0-128-generic
4.15.0-129-generic
4.15.0-130-generic
4.15.0-132-generic
4.15.0-133-generic
4.15.0-134-generic
4.15.0-135-generic
4.15.0-136-generic
4.15.0-137-generic
4.15.0-139-generic
4.15.0-140-generic
4.15.0-141-generic
4.15.0-142-generic
4.15.0-143-generic
4.15.0-144-generic
4.15.0-147-generic
4.15.0-151-generic
4.15.0-153-generic
4.15.0-154-generic
4.15.0-156-generic
4.15.0-158-generic
4.15.0-159-generic
4.15.0-161-generic
4.15.0-162-generic
4.15.0-163-generic
4.15.0-166-generic
4.15.0-167-generic
4.15.0-169-generic
4.15.0-171-generic
4.15.0-173-generic
4.15.0-175-generic
4.15.0-176-generic
4.15.0-177-generic
4.15.0-180-generic
4.15.0-184-generic
4.15.0-187-generic
4.15.0-188-generic
4.15.0-189-generic
4.15.0-191-generic
4.15.0-192-generic
4.15.0-193-generic
4.15.0-194-generic
4.15.0-196-generic
4.15.0-197-generic
4.15.0-200-generic
4.15.0-201-generic
4.15.0-202-generic
4.15.0-204-generic
4.15.0-206-generic
4.15.0-208-generic
4.15.0-209-generic
4.15.0-210-generic
4.15.0-211-generic
4.15.0-212-generic
4.15.0-213-generic
4.18.0-10-generic
4.18.0-11-generic
4.18.0-12-generic
4.18.0-13-generic
4.18.0-14-generic
4.18.0-15-generic
4.18.0-16-generic
4.18.0-17-generic
4.18.0-18-generic
4.18.0-20-generic
4.18.0-21-generic
4.18.0-22-generic
4.18.0-24-generic
4.18.0-25-generic
4.18.20-041820-generic
5.0.0-13-generic
5.0.0-15-generic
5.0.0-16-generic
5.0.0-17-generic
5.0.0-19-generic
5.0.0-20-generic
5.0.0-21-generic
5.0.0-23-generic
5.0.0-25-generic
5.0.0-27-generic
5.0.0-29-generic
5.0.0-31-generic
5.0.0-32-generic
5.0.0-35-generic
5.0.0-36-generic
5.0.0-37-generic
5.0.0-38-generic
5.0.0-41-generic
5.0.0-43-generic
5.0.0-44-generic
5.0.0-47-generic
5.0.0-48-generic
5.0.0-52-generic
5.0.0-53-generic
5.0.0-58-generic
5.0.0-60-generic
5.0.0-61-generic
5.0.0-62-generic
5.0.0-63-generic
5.0.0-65-generic
5.2.0-8-generic
5.2.0-15-generic
5.3.0-13-generic
5.3.0-18-generic
5.3.0-19-generic
5.3.0-22-generic
5.3.0-23-generic
5.3.0-24-generic
5.3.0-26-generic
5.3.0-28-generic
5.3.0-29-generic
5.3.0-40-generic
5.3.0-42-generic
5.3.0-45-generic
5.3.0-46-generic
5.3.0-51-generic
5.3.0-53-generic
5.3.0-55-generic
5.3.0-59-generic
5.3.0-61-generic
5.3.0-62-generic
5.3.0-64-generic
5.3.0-65-generic
5.3.0-66-generic
5.3.0-67-generic
5.3.0-68-generic
5.3.0-69-generic
5.3.0-70-generic
5.3.0-72-generic
5.3.0-73-generic
5.3.0-74-generic
5.3.0-75-generic
5.3.0-76-generic
5.4.0-26-generic
5.4.0-28-generic
5.4.0-29-generic
5.4.0-31-generic
5.4.0-33-generic
5.4.0-37-generic
5.4.0-39-generic
5.4.0-40-generic
5.4.0-42-generic
5.4.0-45-generic
5.4.0-47-generic
5.4.0-48-generic
5.4.0-51-generic
5.4.0-52-generic
5.4.0-53-generic
5.4.0-54-generic
5.4.0-56-generic
5.4.0-58-generic
5.4.0-59-generic
5.4.0-60-generic
5.4.0-62-generic
5.4.0-64-generic
5.4.0-65-generic
5.4.0-66-generic
5.4.0-67-generic
5.4.0-70-generic
5.4.0-71-generic
5.4.0-72-generic
5.4.0-73-generic
5.4.0-74-generic
5.4.0-77-generic
5.4.0-80-generic
5.4.0-81-generic
5.4.0-84-generic
5.4.0-86-generic
5.4.0-87-generic
5.4.0-88-generic
5.4.0-89-generic
5.4.0-90-generic
5.4.0-91-generic
5.4.0-92-generic
5.4.0-94-generic
5.4.0-96-generic
5.4.0-97-generic
5.4.0-99-generic
5.4.0-100-generic
5.4.0-104-generic
5.4.0-105-generic
5.4.0-107-generic
5.4.0-109-generic
5.4.0-110-generic
5.4.0-113-generic
5.4.0-117-generic
5.4.0-120-generic
5.4.0-121-generic
5.4.0-122-generic
5.4.0-124-generic
5.4.0-125-generic
5.4.0-126-generic
5.4.0-128-generic
5.4.0-131-generic
5.4.0-132-generic
5.4.0-135-generic
5.4.0-136-generic
5.4.0-137-generic
5.4.0-139-generic
5.4.0-144-generic
5.4.0-146-generic
5.4.0-147-generic
5.4.0-148-generic
5.4.0-149-generic
5.4.0-150-generic
5.4.0-152-generic
5.4.0-153-generic
5.4.0-155-generic
5.4.0-156-generic
5.4.0-159-generic
5.4.0-162-generic
5.4.0-163-generic
5.4.0-164-generic
5.4.0-165-generic
5.4.0-166-generic
5.4.0-167-generic
5.4.0-169-generic
5.4.0-170-generic
5.4.0-171-generic
5.4.0-172-generic
5.4.0-173-generic
5.4.0-174-generic
5.4.0-176-generic
5.4.0-177-generic
5.4.0-181-generic
5.4.0-182-generic
5.4.0-186-generic
5.4.0-187-generic
5.4.0-189-generic
5.4.0-190-generic
5.4.0-192-generic
5.4.0-193-generic
5.4.0-195-generic
5.4.0-196-generic
5.4.0-198-generic
5.4.0-200-generic
5.4.0-202-generic
5.4.0-204-generic
5.4.0-205-generic
5.4.0-208-generic
5.4.0-211-generic
5.4.0-212-generic
5.4.0-214-generic
5.4.0-215-generic
5.4.0-216-generic
5.4.18-110-generic
5.8.0-23-generic
5.8.0-25-generic
5.8.0-28-generic
5.8.0-29-generic
5.8.0-33-generic
5.8.0-34-generic
5.8.0-36-generic
5.8.0-38-generic
5.8.0-40-generic
5.8.0-41-generic
5.8.0-43-generic
5.8.0-44-generic
5.8.0-45-generic
5.8.0-48-generic
5.8.0-49-generic
5.8.0-50-generic
5.8.0-53-generic
5.8.0-55-generic
5.8.0-59-generic
5.8.0-63-generic
5.11.0-22-generic
5.11.0-25-generic
5.11.0-27-generic
5.11.0-34-generic
5.11.0-36-generic
5.11.0-37-generic
5.11.0-38-generic
5.11.0-40-generic
5.11.0-41-generic
5.11.0-43-generic
5.11.0-44-generic
5.11.0-46-generic
5.13.0-21-generic
5.13.0-22-generic
5.13.0-23-generic
5.13.0-25-generic
5.13.0-27-generic
5.13.0-28-generic
5.13.0-30-generic
5.13.0-35-generic
5.13.0-37-generic
5.13.0-39-generic
5.13.0-40-generic
5.13.0-41-generic
5.13.0-44-generic
5.13.0-48-generic
5.13.0-51-generic
5.13.0-52-generic
5.15.0-25-generic
5.15.0-27-generic
5.15.0-30-generic
5.15.0-33-generic
5.15.0-35-generic
5.15.0-37-generic
5.15.0-39-generic
5.15.0-40-generic
5.15.0-41-generic
5.15.0-43-generic
5.15.0-46-generic
5.15.0-47-generic
5.15.0-48-generic
5.15.0-50-generic
5.15.0-52-generic
5.15.0-53-generic
5.15.0-56-generic
5.15.0-57-generic
5.15.0-58-generic
5.15.0-60-generic
5.15.0-67-generic
5.15.0-69-generic
5.15.0-70-generic
5.15.0-71-generic
5.15.0-72-generic
5.15.0-73-generic
5.15.0-75-generic
5.15.0-76-generic
5.15.0-78-generic
5.15.0-79-generic
5.15.0-82-generic
5.15.0-83-generic
5.15.0-84-generic
5.15.0-86-generic
5.15.0-87-generic
5.15.0-88-generic
5.15.0-89-generic
5.15.0-91-generic
5.15.0-92-generic
5.15.0-94-generic
5.15.0-97-generic
5.15.0-100-generic
5.15.0-101-generic
5.15.0-102-generic
5.15.0-105-generic
5.15.0-106-generic
5.15.0-107-generic
5.15.0-112-generic
5.15.0-113-generic
5.15.0-116-generic
5.15.0-117-generic
5.15.0-118-generic
5.15.0-119-generic
5.15.0-121-generic
5.15.0-122-generic
5.15.0-124-generic
5.15.0-125-generic
5.15.0-126-generic
5.15.0-127-generic
5.15.0-128-generic
5.15.0-130-generic
5.15.0-131-generic
5.15.0-133-generic
5.15.0-134-generic
5.15.0-135-generic
5.15.0-136-generic
5.15.0-138-generic
5.15.0-139-generic
5.15.0-140-generic
5.15.0-141-generic
5.15.0-142-generic
5.15.0-143-generic
5.15.0-144-generic
5.15.0-151-generic
5.15.0-152-generic
5.15.0-153-generic
5.15.0-156-generic
5.15.0-157-generic
5.15.0-160-generic
5.19.0-41-generic
5.19.0-42-generic
5.19.0-43-generic
5.19.0-45-generic
5.19.0-46-generic
5.19.0-50-generic
6.2.0-25-generic
6.2.0-26-generic
6.2.0-31-generic
6.2.0-32-generic
6.2.0-33-generic
6.2.0-34-generic
6.2.0-35-generic
6.2.0-36-generic
6.2.0-37-generic
6.2.0-39-generic
6.5.0-14-generic
6.5.0-15-generic
6.5.0-17-generic
6.5.0-18-generic
6.5.0-21-generic
6.5.0-25-generic
6.5.0-26-generic
6.5.0-27-generic
6.5.0-28-generic
6.5.0-35-generic
6.5.0-41-generic
6.5.0-44-generic
6.5.0-45-generic
6.8.0-31-generic
6.8.0-35-generic
6.8.0-36-generic
6.8.0-38-generic
6.8.0-39-generic
6.8.0-40-generic
6.8.0-41-generic
6.8.0-44-generic
6.8.0-45-generic
6.8.0-47-generic
6.8.0-48-generic
6.8.0-49-generic
6.8.0-50-generic
6.8.0-51-generic
6.8.0-52-generic
6.8.0-53-generic
6.8.0-54-generic
6.8.0-55-generic
6.8.0-56-generic
6.8.0-57-generic
6.8.0-58-generic
6.8.0-59-generic
6.8.0-60-generic
6.8.0-62-generic
6.8.0-63-generic
6.8.0-64-generic
6.8.0-65-generic
6.8.0-71-generic
6.8.0-78-generic
6.8.0-79-generic
6.8.0-83-generic
6.8.0-84-generic
6.8.0-85-generic
6.8.0-86-generic
6.11.0-17-generic
6.11.0-19-generic
6.11.0-21-generic
6.11.0-24-generic
6.11.0-25-generic
6.11.0-26-generic
6.11.0-28-generic
6.11.0-29-generic
```

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
