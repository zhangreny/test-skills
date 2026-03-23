---
title: "SMTXZBS/5.7.0/SMTX ZBS 升级指南"
source_url: "https://internal-docs.smartx.com/smtxzbs/5.7.0/zbs_upgrade_guide/zbs_upgrade_preface_generic"
sections: 21
---

# SMTXZBS/5.7.0/SMTX ZBS 升级指南
## 关于本文档

# 关于本文档

本文档介绍了 SMTX ZBS 低版本集群，和以分离式模式部署的 SMTX OS 4.0.x 集群升级到本版本块存储集群，以及升级文件存储集群的步骤。

阅读本文档需了解 SMTX ZBS 块存储和文件存储，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

- **2026-02-06：文档随 SMTX 文件存储 1.3.0 正式发布**

  增加了文件存储部署在 Hygon x86\_64 架构的块存储集群时，文件存储将独占 CPU 核心的相关内容。
- **2025-11-24**：**文档随 SMTX ZBS 5.7.0 正式发布**。

  相较于 SMTX ZBS 5.6.4，本版本主要进行了如下更新：

  - 更新升级路径；
  - 更新 Kernel；
  - 更新[转换网口绑定模式](/smtxzbs/5.7.0/zbs_upgrade_guide/zbs_upgrade_guide_20)。

---

## 升级块存储集群 > 概述

# 概述

SMTX ZBS 块存储集群支持使用升级中心或命令行进行升级。不同版本集群支持的升级方式可能不同，具体请参考[升级路径](/smtxzbs/5.7.0/zbs_upgrade_guide/zbs_upgrade_guide_01#%E5%8D%87%E7%BA%A7%E8%B7%AF%E5%BE%84)。

- **通过升级中心升级**

  通过 CloudTower 的升级中心，可以一站式完成集群升级和内核升级操作，极大降低操作难度，有效提升升级效率和成功率。若集群版本支持使用升级中心升级，建议您参考[《升级中心使用指南》](/cluster-upgrade/1.2.0/cluster_upgrade_user_guide/cluster_upgrade_user_guide_01)进行升级。
- **通过命令行升级**

  在集群单个节点上执行命令行升级操作即可完成整个集群的升级，无需人工干预，且可以查看详细的升级日志。

---

## 升级块存储集群 > 升级说明

# 升级说明

## 升级路径

SMTX ZBS 块存储集群部署在不同的服务器平台时，从低版本升级到本版本的路径也不同。请服务器架构查看对应的升级路径。

### Intel x86\_64 / AMD x86\_64 架构

| 源软件版本 | 说明 |
| --- | --- |
| SMTX OS 4.0.x （分离式模式部署） | 可通过命令行直接升级至本版本。 |
| SMTX ZBS 5.0.0 ~ 5.1.0 | 可通过命令行直接升级至本版本。 |
| SMTX ZBS 5.2.0 ~ 5.6.4 | 可通过命令行或升级中心直接升级至本版本。 |

### Hygon x86\_64 / 鲲鹏 AArch64 架构

| 源软件版本 | 说明 |
| --- | --- |
| SMTX OS 4.0.x （分离式模式部署） | 须通过独立发布的升级包和转换工具先升级到 5.4.1，才能升级至本版本。请联系 SmartX 售后人员进行升级。 |
| SMTX ZBS 5.0.0 ~ 5.1.0 | 须通过独立发布的升级包和转换工具先升级到 5.4.1，才能升级至本版本。请联系 SmartX 售后人员进行升级。 |
| SMTX ZBS 5.2.0 ~ 5.6.4 | 可通过命令行或升级中心直接升级至本版本。 |

## 升级流程

升级流程如下：

![](https://cdn.smartx.com/internal-docs/assets/a5c0a825/zbs_upgrade_guide_01.png)

SMTX ZBS 将不定期提供新的内核版本以提⾼系统性能或应对安全风险，新的内核版本集成在 SMTX ZBS 新版本的安装部署 ISO 文件和升级 ISO 文件中。在准备升级前，您可先通过查看[内核更新记录](/smtxzbs/5.7.0/zbs_upgrade_guide/zbs_upgrade_guide_08)，确认升级前的内核版本与升级后目标版本所配套的内核版本是否一致。若版本不一致，可根据内核更新记录按需更新。

- 若您使用升级中心升级集群，可在升级界面选择在升级集群的同时自动升级内核，或在升级集群后单独升级内核。具体说明请参考[《升级中心使用指南》](/cluster-upgrade/1.2.0/cluster_upgrade_user_guide/cluster_upgrade_user_guide_01)。
- 若您使用命令行升级集群，需要在集群升级完成后手动升级内核。具体操作请参考本文档的[手动升级内核](/smtxzbs/5.7.0/zbs_upgrade_guide/zbs_upgrade_guide_10)。

## 升级特点

SMTX ZBS 块存储集群采用在线不停机的方式进行升级。

## 升级时限制的操作

进行集群和内核升级不会影响业务的正常运行，但禁止执行如下操作：

- 为集群添加或移除主机。
- 将集群从 CloudTower 中移除。
- 手动将主机进入或退出维护模式。
- 手动关机或重启主机。
- 对主机执行角色转换操作。

---

## 升级块存储集群 > 升级前准备

# 升级前准备

在启动升级前，请检查并做好如下准备。

## 获取升级所需文件

- **获取目标版本的升级文件或安装文件**

  根据您选择的升级方式，以及服务器类型，提前获取目标版本的升级 ISO 文件。
- **确认 CloudTower 版本配套关系**

  SMTX ZBS 只能由特定版本的 CloudTower 进行管理，请先参考目标版本的《SMTX ZBS 发布说明》确认该版本集群的配套 CloudTower 版本。如果当前 CloudTower 版本不支持管理目标版本集群，请先升级至配套版本。
- **确认集群的版本类型**

  若集群的软件许可为标准版，且集群内包含全闪配置的节点，需先更新许可为企业版，再进行升级。

## 确认集群硬件是否满足要求

- **确认集群的 CPU 微架构要求**

  集群在升级过程中会进行 CPU 指令集检查，请确认服务器的 CPU 微架构满足下表要求，否则升级操作会被终止。

  | **CPU 架构** | **微架构最低版本** |
  | --- | --- |
  | Intel x86\_64 | Sandy Bridge |
  | AMD x86\_64 | Zen |
  | Hygon x86\_64 | Dhyana |
  | 鲲鹏 AArch64 | Taishan v110 |
- **确认内存资源是否充足**

  在正式执行升级前，请先确认目标版本系统需占用的内存资源（详见[《SMTX ZBS 安装部署指南》](/smtxzbs/5.7.0/zbs_installation_guide/zbs_installation_guide_13)）。若剩余内存不满足目标版本要求，则无法升级。在此情况下请参考附录[对节点进行内存扩容](/smtxzbs/5.7.0/zbs_upgrade_guide/zbs_upgrade_guide_13)。

  > **注意**：
  >
  > 集群标准容量规格节点的内存须不小于 128 GB 才可升级。若不满足内存要求，请在扩容内存后再进行升级。

## 确认集群空间使用率情况

- **确认集群已使用的常驻缓存容量**

  对于启用了常驻缓存的 SMTX ZBS 块存储集群，在升级前，请在集群的**概览** > **缓存** > **常驻缓存**界面检查集群已使用的常驻缓存容量，若已使用常驻缓存超过预留常驻缓存容量的 80%，则不允许升级。此时请先关闭部分卷的常驻缓存，或扩大常驻缓存预留比例，然后进行升级。
- **确认系统分区空间是否充足**

  请在集群的概览页面确认是否存在系统分区空间使用率已超过 90% 的报警。若系统分区空间使用率较高，升级组件可能无法正常工作导致集群升级失败。因此，需要在升级前对系统分区空间进行清理以解决此报警，然后才可进行后续的升级。
- **确认集群的存储空间使用率**

  请在集群的概览页面查看集群当前的存储使用率，若存储空间使用率达到 98%，需先扩容或释放存储空间，再尝试升级。
- **确认集群的缓存空间使用率**

  若集群节点除预留常驻缓存容量外的缓存空间使用率已超过 89%，请先等待数据下沉释放缓存空间，再尝试升级。

## 确认是否部署了文件存储集群

若块存储集群中部署了文件存储集群，由于文件控制器虚拟机必须位于指定主机、且必须位于不同主机的放置组规则，因此无法迁移至其他主机，导致主机无法进入维护模式。具体说明和解决方法如下：

- **对于 1.2.0 以下版本的文件存储**

  1. 登录主机的 Web 控制台，手动关闭该主机上文件控制器虚拟机的 HA 功能，并将其关机。
  2. 对该主机进行内核升级操作。
  3. 升级完成后，请手动将文件控制器虚拟机开机，并重新启用 HA 功能。
  4. 继续对集群中其他主机依次执行上述操作，直至所有主机的内核升级完毕。
  > **说明**：
  >
  > 由于关闭 2 个及以上的文件控制器可能导致文件存储服务不可用，因此需逐个对主机进行内核升级操作。
- **对于 1.2.0 及以上版本的文件存储**

  1. 进入 CloudTower，下线文件控制器：

     1. 在 CloudTower **文件存储页面**左侧的导航栏中选择**文件存储集群**，在文件存储集群列表中单击目标集群的名称，再单击**设置**页签，选择**文件控制器**。
     2. 选择一个文件控制器，单击右侧的 ...，选择**下线**。
     3. 在弹出的对话框中阅读风险提示后单击**下线**。
  2. 对关闭了文件控制器的主机进行内核升级操作。
  3. 主机内核升级完毕后，重新上线该主机上的文件控制器：

     1. 在 CloudTower **文件存储页面**左侧的导航栏中选择**文件存储集群**，在文件存储集群列表中单击目标集群的名称，再单击**设置**页签，选择**文件控制器**。
     2. 选择一个文件控制器，单击右侧的 ...，选择**上线**。
  4. 继续对集群中其他主机依次执行上述操作，直至所有主机的内核升级完毕。
  > **说明**：
  >
  > 由于关闭 2 个及以上的文件控制器可能导致文件存储服务不可用，CloudTower 限制了每次只能下线一个文件控制器，因此需逐个下线文件控制器，并对文件控制器所在主机进行内核升级操作。

## 确认集群的状态

请确认待升级的集群满足如下要求：

- 集群中没有主机处于维护模式或进入维护模式中；
- 集群中所有主机均处于健康状态；
- 集群未处于环境检查中、升级中或升级内核中状态；
- 集群中没有正在添加的主机；
- 如使用升级中心升级，集群与 CloudTower 的连接状态需为`已连接`。

---

## 升级块存储集群 > 升级集群

# 升级集群

SMTX OS 4.0.x 集群（分离式模式）和 SMTX ZBS 块存储集群均支持通过命令行的方式进行自动升级，5.2.0 ~ 5.6.0 版本的 SMTX ZBS 块存储集群也支持通过升级中心升级。升级过程可以保持在线不停机。

> **注意**：
>
> - 对于 Hygon x86\_64 /鲲鹏 AArch64 架构下的 SMTX OS 4.0.x（分离式模式）和 SMTX ZBS 5.0.0 ～ 5.1.0 集群，所涉及升级操作复杂度较高，请联系 SmartX 售后人员帮助升级。
> - 采用存储分层模式的低版本 SMTX ZBS 块存储集群在升级至本版本后，系统会自动腾挪性能层的空间，在空间调整期间不能使用纠删码，不能编辑常驻缓存，不能启用卷的常驻缓存，请等待空间调整完毕。

---

## 升级块存储集群 > 升级集群 > 通过升级中心升级

# 通过升级中心升级

通过升级中心升级集群的操作方法请参考[《升级中心使用指南》](/cluster-upgrade/1.2.0/cluster_upgrade_user_guide/cluster_upgrade_user_guide_01)。

---

## 升级块存储集群 > 升级集群 > 通过命令行升级

# 通过命令行升级

只需在集群的某一个节点执行命令行升级操作，即可完成整个块存储集群的升级。

**前提条件**

- 已获取适配服务器类型的 SMTX ZBS 块存储升级 ISO 文件以及对应的元数据 JSON 文件。
- 拥有节点超级管理员 root 的操作权限。关于该权限的说明可参见 [SMTX OS 节点的本地账户](/smtxzbs/5.7.0/zbs_upgrade_guide/zbs_upgrade_guide_18)和 [SMTX ZBS 节点的本地账户](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_57)。

**注意事项**

- 在块存储集群升级过程中，系统会暂时停止 `elf-vm-monitor` 服务，同时触发监控报警系统对此服务的报警。用户可以忽略该告警，待升级结束后，系统将自动恢复 `elf-vm-monitor` 服务的运行。
- 如果升级过程中断，`elf-vm-monitor` 服务将处于停止运行的状态。在查明升级中断的原因前，请勿启动任何节点的 `elf-vm-monitor` 服务。重新执行升级命令并顺利完成升级后，系统将自动恢复 `elf-vm-monitor` 服务的运行。

**操作步骤**

1. 使用 root 账号登录集群，利用工具将目标版本的 SMTX ZBS 块存储升级 ISO 文件以及对应的元数据 JSON 文件上传至集群的某个节点。

   例如，块存储集群某个节点的管理 IP 地址为 `192.168.75.101`，升级的目标版本为 SMTX ZBS 5.6.1。启动升级前可借助 Xshell 工具将 5.6.1 版本的 .iso 文件以及对应的元数据 JSON 文件上传至 `192.168.75.101` 节点的根目录下。
2. 输入以下命令挂载 ISO 文件，并配置 yum 源为 `smartxos.repo`。

   ```
   # 创建 /mnt/iso 目录
   mkdir /mnt/iso

   # 挂载映像到 /mnt/iso 目录
   mount -o loop new_iso_file_name.iso /mnt/iso

   # 创建 /etc/yum.repos.d/bk 目录
   mkdir /etc/yum.repos.d/bk

   # 将 /etc/yum.repos.d/ 目录下所有 repo 文件移动到 /etc/yum.repos.d/bk/ 目录下
   mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/bk/

   # 在 /etc/yum.repos.d/ 目录下创建文件 smartxos.repo
   touch /etc/yum.repos.d/smartxos.repo

   # 使用 vi /etc/yum.repos.d/smartxos.repo 命令打开文件，并写入如下内容
   [smartxos-local-iso]
   name=smartxos
   baseurl=file:///mnt/iso
   gpgcheck=0
   enabled=1
   ```

   执行完毕后，检查 `/etc/yum.repos.d`，确保此目录下仅有 `smartxos.repo` 文件，并且其内容与上述要求的一致。
3. 更新 smartx-upgrade rpm 包。

   `yum clean all`

   `yum update -y smartx-upgrade`
4. 进入 `/usr/share/upgrade/runner/` 目录，执行以下脚本，其中 <iso path> 表示 ISO 文件的绝对路径；<metadata path> 表示升级的目标版本的 ISO 元数据文件的绝对路径。

   `nohup python cluster_upgrader.py --iso_path <iso path> --metadata_path <metadata path> &`
5. 在脚本执行过程中，通过输入命令 `tail -f nohup.out` 实时查看更新日志。当浏览到日志中输出 `upgrade_cluster: Cluster upgrade successful`，表示升级成功。

> **说明**：
>
> 采用存储分层模式的低版本 SMTX ZBS 块存储集群在升级至本版本后，系统会自动腾挪性能层的空间，在空间调整期间不能使用纠删码，不能编辑常驻缓存，不能启用卷的常驻缓存，请等待空间调整完毕。

---

## 升级块存储集群 > 手动升级内核

# 手动升级内核

本版本发布的同时分别更新了与 Intel x86\_64、AMD x86\_64、Hygon x86\_64 和鲲鹏 AArch64 三种服务器平台配套使用的内核版本，请查看[内核更新记录](/smtxzbs/5.7.0/zbs_upgrade_guide/zbs_upgrade_guide_08)，根据内核更新记录按需升级内核。

本章节介绍了如何使用命令行手动升级内核。若您的集群版本支持使用升级中心进行升级，请参考[《升级中心使用指南》](/cluster-upgrade/1.2.0/cluster_upgrade_user_guide/cluster_upgrade_user_guide_01)完成对内核的自动升级。

**升级说明**

- 当块存储集群部署在不同的服务器平台时，与其配套使用的内核版本均不同，但手动升级内核版本的操作步骤基本相同。
- 内核升级结束后，需要重启物理机使升级生效，系统将会出现短暂的 I/O 中断，但不影响业务的正常运行。

**前提条件**

- 块存储集群已完成升级，否则将导致内核与块存储内部服务不兼容。
- 若 CloudTower 所在的虚拟机部署在块存储集群内，需确保该虚拟机已处于关机状态。
- 对照《SMTX ZBS 管理指南》中[进入维护模式的要求](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)完成自检，确认所有检查项目满足要求。

---

## 升级块存储集群 > 手动升级内核 > 内核更新记录

# 内核更新记录

下表列出了集群版本与内核版本的配套关系及更新记录。

集群在全新安装时默认使用匹配的内核版本，但在升级集群时默认不自动升级内核，需要在集群升级后自行更新。

## Intel x86\_64 或 AMD x86\_64 架构

| **SMTX OS/SMTX ZBS 版本** | **内核版本** | **更新原因** |
| --- | --- | --- |
| SMTX OS 4.0.0 | kernel-3.10.0-693.11.6.el7​.smartx.1.x86\_64.rpm | - |
| SMTX OS 4.0.1 ~ 4.0.3 | kernel-3.10.0-957.21.3.el7​.smartx.2.x86\_64.rpm | 开启嵌套虚拟化导致虚拟机无法热迁移问题。 |
| SMTX OS 4.0.4 ~ 4.0.8 | kernel-3.10.0-1062.1.2.el7​.smartx.1.x86\_64.rpm | 修复 vhost 漏洞。 |
| SMTX OS 4.0.9 ~ 4.0.10 | kernel-3.10.0-1160.11.1.el7​.smartx.1.x86\_64.rpm | 修复因服务出现 OOM (out of memory) 导致内核进程锁死的问题。 |
| SMTX ZBS 5.0.0 ~ 5.1.0 | kernel-4.18.0-193.28.1.el7​.smartx.3.x86\_64.rpm | 内核官方正式发布的更新版本，修复了因服务出现 OOM (out of memory) 导致内核进程锁死的问题。 |
| SMTX ZBS 5.2.0 | - kernel-modules-4.18.0-193.28.1.el7​.smartx.7.x86\_64.rpm - kernel-core-4.18.0-193.28.1.el7​.smartx.7.x86\_64.rpm | 升级 MegaRAID 驱动。 |
| SMTX ZBS 5.3.0 | kernel-4.18.0-193.28.1.el7​.smartx.11.x86\_64.rpm | - 修复安全漏洞 CVE-2022-2639。 - 更新 i40e 驱动至 2.20.12 版本，以解决该驱动无法被正常识别的问题。 - 解决 i40e 驱动与 mlnx 驱动同时加载时互相冲突的问题。 |
| SMTX ZBS 5.4.0 ~ 5.4.1 | kernel-4.18.0-193.28.1.el7​.smartx.13.x86\_64.rpm | - 修复 USB 设备导致系统死机的问题。 - 升级 kvm\_stat 工具。 |
| SMTX ZBS 5.5.0 | kernel-4.18.0-193.28.1.el7​.smartx.14.x86\_64.rpm | 修复在低版本固件场景下，X710 系列网卡无法正常工作的问题。 |
| SMTX ZBS 5.6.0 ~ 5.6.4 | kernel-4.19.90-2307.3.0.el7​.smartx.42.x86\_64.rpm | - 解决 PM8222 等 RAID 卡在 mq-deadline 调度器中的性能退化问题。 - 解决 OVS 内存泄漏问题。 - 支持 H965 系列 RAID 卡驱动 - 解决 mpt3sas 驱动在磁盘异常情况下可能导致系统卡死的问题。 - 加固内核，防止 USB 设备异常导致的机器宕机的问题。 - 解决 TUN 驱动持续收到大量异常包时，触发 soft lockup 的问题。 - 修复 zero page refcount 溢出导致虚拟机异常问题。 - 修复安全漏洞 CVE-2023-6931。 |
| 5.7.0 | kernel-5.10.0-247.0.0.el7.v72.el7.rpm | - 支持 io\_uring - 内核升级至 5.10.0-247.0.0。 - 支持 SSSRAID 控制卡。 - 支持网迅万兆网卡（txgbe 系列）。 - 升级 ps3stor 驱动至 2.6.0.23。 - 支持 Intel E610 网卡。 - 升级 mpt3sas 驱动至 55.00.00.00。 - 升级 i40e 驱动至 2.20.12。 - 升级 megaraid 驱动至 07.735.03.00-2。 - 支持海思 SP680 系列网卡。 - 修复了 iouring 中重新提交 I/O 时，I/O 丢失的问题。 - 修复了为 QLogic 网卡开启 ptp 特性时，CPU 使用率突增的问题。 - 修复了安全漏洞 CVE-2019-3016。 - 修复了仅支持 32bit MSI 的 PCIe 设备无法工作的问题。 - 修复了数据不一致导致块层 I/O 卡死的问题。 - 修复了 ext4 文件系统在线重置容量可能导致数据被破坏的问题。 - 修复了内存子系统可能被破坏的问题。 - 修复了 buffer I/O 数据不一致的问题。 - 修复了 kvm 异步缺页异常导致卡死的问题。 - 修复了内存申请路径可能卡死的问题。 |

## Hygon x86\_64 架构

| **SMTX ZBS 版本** | **内核版本** | **更新原因** |
| --- | --- | --- |
| 5.2.0 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.8.x86\_64.rpm | - |
| 5.3.0 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.12.x86\_64.rpm | - 修复安全漏洞 CVE-2022-2639。 - 更新 i40e 驱动至 2.20.12 版本，以解决该驱动无法被正常识别的问题。 - 解决 i40e 驱动与 mlnx 驱动同时加载时互相冲突的问题。 |
| 5.4.0 ~ 5.4.1 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.15.x86\_64.rpm | - 修复 USB 设备导致系统死机的问题。 - 升级 kvm\_stat 工具。 |
| 5.5.0 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.17.x86\_64.rpm | 修复在低版本固件场景下，X710 系列网卡无法正常工作的问题。 |
| 5.6.0 ~ 5.6.4 | kernel-4.19.90-2307.3.0​.oe1.smartx.42.x86\_64.rpm | - 支持 Hygon 4 代 CPU。 - 解决因触发 IO\_PAGE\_FAULT 导致设备异常的问题。 - 解决 PM8222 等 RAID 卡在 mq-deadline 调度器中的性能退化问题。 - 解决 OVS 内存泄漏问题。 - 解决 mpt3sas 驱动在磁盘异常情况下可能导致系统卡死的问题。 - 加固内核，防止 USB 设备异常导致的机器宕机的问题。 - 解决 TUN 驱动持续收到大量异常包时，触发 soft lockup 的问题。 - 修复 zero page refcount 溢出导致虚拟机异常问题。 - 修复安全漏洞 CVE-2023-6931。 |
| 5.7.0 | kernel-5.10.0-247.0.0.el7.v72.oe1.rpm | - 支持 io\_uring - 内核升级至 5.10.0-247.0.0。 - 支持 SSSRAID 控制卡。 - 支持网迅万兆网卡（txgbe 系列）。 - 升级 ps3stor 驱动至 2.6.0.23。 - 支持 Intel E610 网卡。 - 升级 mpt3sas 驱动至 55.00.00.00。 - 升级 i40e 驱动至 2.20.12。 - 升级 megaraid 驱动至 07.735.03.00-2。 - 支持海思 SP680 系列网卡。 - 修复了 iouring 中重新提交 I/O 时，I/O 丢失的问题。 - 修复了为 QLogic 网卡开启 ptp 特性时，CPU 使用率突增的问题。 - 修复了安全漏洞 CVE-2019-3016。 - 修复了仅支持 32bit MSI 的 PCIe 设备无法工作的问题。 - 修复了数据不一致导致块层 I/O 卡死的问题。 - 修复了 ext4 文件系统在线重置容量可能导致数据被破坏的问题。 - 修复了内存子系统可能被破坏的问题。 - 修复了 buffer I/O 数据不一致的问题。 - 修复了 kvm 异步缺页异常导致卡死的问题。 - 修复了内存申请路径可能卡死的问题。 |

## 鲲鹏 AArch64 架构

| **SMTX ZBS 版本** | **内核版本** | **更新原因** |
| --- | --- | --- |
| 5.2.0 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.8.aarch64.rpm | - |
| 5.3.0 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.12.aarch64.rpm | - 修复安全漏洞 CVE-2022-2639。 - 更新 i40e 驱动至 2.20.12 版本，以解决该驱动无法被正常识别的问题。 - 解决 i40e 驱动与 mlnx 驱动同时加载时互相冲突的问题。 |
| 5.4.0 ~ 5.4.1 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.15.aarch64.rpm | - 修复 USB 设备导致系统死机的问题。 - 升级 kvm\_stat 工具。 - 修复虚拟机热迁移兼容性问题。 |
| 5.5.0 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.17.aarch64.rpm | 修复在低版本固件场景下，X710 系列网卡无法正常工作的问题。 |
| 5.6.0 ~ 5.6.1 | kernel-4.19.90-2307.3.0​.oe1.smartx.42.aarch64.rpm | - 解决 PM8222 等 RAID 卡在 mq-deadline 调度器中的性能退化问题。 - 解决 OVS 内存泄漏问题。 - 解决 mpt3sas 驱动在磁盘异常情况下可能导致系统卡死的问题。 - 加固内核，防止 USB 设备异常导致的机器宕机的问题。 - 解决 TUN 驱动持续收到大量异常包时，触发 soft lockup 的问题。 - 修复 zero page refcount 溢出导致虚拟机异常问题。 - 修复安全漏洞 CVE-2023-6931。 |
| 5.7.0 | kernel-5.10.0-247.0.0.oe1.v72.aarch64.rpm | - 支持 io\_uring - 内核升级至 5.10.0-247.0.0。 - 支持 SSSRAID 控制卡。 - 支持网迅万兆网卡（txgbe 系列）。 - 升级 ps3stor 驱动至 2.6.0.23。 - 升级 mpt3sas 驱动至 55.00.00.00。 - 升级 megaraid 驱动至 07.735.03.00-2。 - 支持海思 SP680 系列网卡。 - 修复了 iouring 中重新提交 I/O 时，I/O 丢失的问题。 - 修复了为 QLogic 网卡开启 ptp 特性时，CPU 使用率突增的问题。 - 修复了安全漏洞 CVE-2019-3016。 - 修复了仅支持 32bit MSI 的 PCIe 设备无法工作的问题。 - 修复了数据不一致导致块层 I/O 卡死的问题。 - 修复了 ext4 文件系统在线重置容量可能导致数据被破坏的问题。 - 修复了内存子系统可能被破坏的问题。 - 修复了 buffer I/O 数据不一致的问题。 - 修复了 kvm 异步缺页异常导致卡死的问题。 - 修复了内存申请路径可能卡死的问题。 |

---

## 升级块存储集群 > 手动升级内核 > 执行内核升级

# 执行内核升级

请按如下步骤升级内核。

## 第 1 步：上传集群升级 ISO 文件或安装 ISO 文件至 Meta Leader 节点

1. 执行命令 `zbs-tool service list`，查询块存储集群 Meta Leader 节点。
2. 上传本版本 SMTX ZBS 块存储升级 ISO 文件或安装 ISO 文件到 Meta Leader 节点，并在该节点执行以下命令，以准备升级内核所需的 repo，然后记录此节点的存储 IP。其中，`<iso_path>` 表示 ISO 映像在该节点的绝对路径。

   `cluster-upgrade prepare_repo <iso_path>`

   执行完成后，如果输出信息显示 `prepare repo success`，表明 repo 已准备完成。

## 第 2 步：升级非 Meta Leader 节点的内核

1. 登录 CloudTower，在块存储集群的主机列表中选中此节点所在的主机，单击右侧的 **...** 后选择**进入维护模式**。
2. 执行下述命令用于准备 repo。其中 `<repo_ip>` 为 Meta Leader 节点的存储 IP。

   `cluster-upgrade config_repo --repo_ip <repo_ip>`

   执行完成后，若输出信息显示 `config repo success.`，表明当前节点升级内核所需要的 repo 已配置完成。
3. （可选）若当前节点的内核版本为 SMTX ZBS 5.0.0 或 5.0.1 的内核版本，执行以下命令卸载 mlnx-ofa\_kernel 包，以确保内核可正常升级。其他版本可略过此步骤。

   `rpm -e --nodeps mlnx-ofa_kernel`
4. 执行以下命令进行内核升级。

   `skc upgrade`
5. 登录 CloudTower，在块存储集群的主机列表中选中目标主机，单击右侧的 **...** 后选择**重启**，输入重启原因后重启主机。
6. 执行 `uname -a` 命令，查看内核是否已成功升级到目标版本。若升级不符合预期，可参考[回滚内核版本](/smtxzbs/5.7.0/zbs_upgrade_guide/zbs_upgrade_guide_21)一节对内核进行回滚。
7. 在 CloudTower 的主机概览界面中查看当前主机已处于维护模式的时间，单击提示内容右侧的**退出维护模式**。
8. 系统弹出检查对话框，并启动退出维护模式前的自检，检查结束后返回所有自检项目的检查结果。

   - 若所有检查项目全部满足要求，允许主机退出维护模式。
   - 若部分检查结果不满足要求，请参考《SMTX ZBS 块存储集群运维指南》中的**主机维护模式**章节，对照[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)前的检查项目及结果一览表的**后续操作及建议**完成整改，然后再次尝试退出维护模式。
9. 切换至其他非 Meta Leader 节点，执行如上步骤，直至所有非 Meta Leader 节点完成升级。

## 第 3 步：升级 Meta Leader 节点的内核

1. 执行 `zbs-tool service list` 命令，确认 Meta Leader 是否已切换至其他节点。若没有切换，则执行 `systemctl stop zbs-metad` 命令，触发 Meta Leader 切换。
2. 执行 `zbs-meta chunk list` 命令，确认当前块存储集群各个 Chunk 状态均为 `CONNECTED_HEALTHY`。
3. 登录 CloudTower，在块存储集群的主机列表中选中此节点所在的主机，单击右侧的 **...** 后选择**进入维护模式**。
4. 执行下述命令用于准备升级内核所需的 repo。其中，`<repo_ip>` 为节点自身的存储 IP。

   `cluster-upgrade config_repo --repo_ip <repo_ip>`

   执行命令后，若输出 `config repo success.`，表明所需的 repo 已配置完成。
5. （可选）若当前节点的内核版本为 SMTX ZBS 5.0.0 或 5.0.1 的内核版本，执行以下命令卸载 mlnx-ofa\_kernel 包，以确保内核可正常升级。其他版本可略过此步骤。

   `rpm -e --nodeps mlnx-ofa_kernel`
6. 执行以下命令升级内核。

   `skc upgrade`
7. 登录 CloudTower，在块存储集群的主机列表中选中目标主机，单击右侧的 **...** 后选择**重启**，输入重启原因后重启主机。
8. 执行 `uname -a` 命令，查看内核是否已成功升级到目标版本。若升级不符合预期，可参考[回滚内核版本](/smtxzbs/5.7.0/zbs_upgrade_guide/zbs_upgrade_guide_21)一节对内核进行回滚。
9. 在 CloudTower 的主机概览界面中查看当前主机已处于维护模式的时间，单击提示内容右侧的**退出维护模式**。
10. 系统弹出检查对话框，并启动退出维护模式前的自检，检查结束后返回所有自检项目的检查结果。

    - 若所有检查项目全部满足要求，允许主机退出维护模式。
    - 若部分检查结果不满足要求，请参考《SMTX ZBS 管理指南》中的**使用主机维护模式**章节，对照[退出维护模式](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_084#%E9%80%80%E5%87%BA%E7%BB%B4%E6%8A%A4%E6%A8%A1%E5%BC%8F)前的检查项目及结果一览表的**后续操作及建议**完成整改，然后再次尝试退出维护模式。
11. 在所有节点完成升级后，通过 CloudTower 确认块存储集群状态正常。

## 第 4 步：清理 boot 分区残留的内核包

由于 `/boot` 分区只有 200 MB 存储空间，在多次升级内核后，`/boot` 分区存储空间可能会被占满。建议执行 `skc clean` 命令，清理掉没有运行的驱动和内核包。

---

## 升级块存储集群 > 手动升级内核 > 回滚内核版本（可选）

# 回滚内核版本（可选）

若升级内核失败或升级的版本不及预期，可参考如下步骤回滚内核。

**操作步骤**

1. 执行以下命令，选择要回滚到的内核版本。主机重启后将默认启动该内核。

   `skc boot`

   > **注意**：
   >
   > 对于 5.4.1 及以下版本，且 BIOS 模式为 `legacy bios` 的块存储集群，在升级到本版本后，使用该命令无法设置默认启动的内核。在此情况下，请在下次重启时在 grub 界面手动选择默认启动项。
2. 登录 CloudTower，在块存储集群的主机列表中选中此节点所在的主机，单击右侧的 **...** 后选择**进入维护模式**。
3. 当主机处于维护模式后，在块存储集群的主机列表中选中目标主机，单击右侧的 **...** 后选择**重启**，输入重启原因后重启主机。
4. 执行 `uname -a` 命令，确认当前内核是否已经成功回滚为目标版本。

---

## 升级块存储集群 > 块存储集群升级后配置 > 启用集群 Boost 模式（可选）

# 启用集群 Boost 模式（可选）

从低版本升级至本版本的 SMTX ZBS 块存储集群未启用 Boost 模式。若需要在块存储集群中部署文件存储集群，请在升级完成后手动为集群启用 Boost 模式。

**操作步骤**

在集群任一节点执行如下命令：

`nohup zbs-cluster vhost enable &`

**输出示例**

```
2023-10-20 14:34:33,919 cluster_manager.py 229 [1638502] [INFO] Checking current status
2023-10-20 14:34:33,963 cluster_manager.py 187 [1638502] [INFO] Start checking vhost status
...
2023-10-20 14:34:34,285 cluster_manager.py 244 [1638502] [INFO] Start enable vhost
2023-10-20 14:34:35,130 cmdline.py 188 [1638502] [INFO]
2023-10-20 14:34:35,131 cmdline.py 188 [1638502] [INFO] PLAY [cluster:!witness]
...
2023-10-20 14:37:24,506 cmdline.py 188 [1638502] [INFO] PLAY RECAP *********************************************************************
2023-10-20 14:37:24,506 cmdline.py 188 [1638502] [INFO] 10.100.128.111             : ok=16   changed=12   unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
2023-10-20 14:37:24,506 cmdline.py 188 [1638502] [INFO] 10.100.128.112             : ok=16   changed=12   unreachable=0    failed=0    skipped=1    resscued=0    ignored=0
2023-10-20 14:37:24,506 cmdline.py 188 [1638502] [INFO] 10.100.128.113             : ok=16   changed=12   unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
2023-10-20 14:37:24,507 cmdline.py 188 [1638502] [INFO] 10.100.128.114             : ok=16   changed=12   unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
2023-10-20 14:37:24,507 cmdline.py 188 [1638502] [INFO]
2023-10-20 14:37:25,607 cluster.py 524 [1638502] [INFO] Done, enable vhost successfully.
```

**输出说明**

在脚本执行过程中，输入命令 `tail -f nohup.out` 实时查看日志。若输出结果包含 `Done, enable vhost successfully.`，表示集群 Boost 模式相关配置已开启，需要逐一查看集群中的主机日志： `/var/log/hugepage-manager.log`，确认 Hugepage 是否正确分配，如果正确分配，则无需重启主机，否则需要重启主机使其生效。

分配正确日志如下：

```
2023-12-14 11:02:17,611 [INFO] setup 54142M hugepage on node 0, cost 0 ms
2023-12-14 11:02:17,627 [INFO] setup 54886M hugepage on node 1, cost 0 ms
2023-12-14 11:02:17,650 [INFO] setup 55226M hugepage on node 2, cost 0 ms
2023-12-14 11:02:17,676 [INFO] setup 52836M hugepage on node 3, cost 0 ms
```

分配错误日志如下：

```
2023-12-13 13:59:53,682 [WARNING] try to setup 54160M hugepage on node 0,but get 34714M
2023-12-13 13:59:57,750 [WARNING] try to setup 54886M hugepage on node 1,but get 47644M
2023-12-13 13:59:59,967 [WARNING] try to setup 55226M hugepage on node 2,but get 18482M
2023-12-13 14:00:00,033 [WARNING] try to setup 52816M hugepage on node 3,but get 40936M
```

---

## 升级块存储集群 > 块存储集群升级后配置 > 转换网口绑定模式（可选）

# 转换网口绑定模式（可选）

当集群的存储网络开启了 RDMA 且 VDS 配置了 Linux Bond 时，在将集群升级至本版本后，可以选择手动将存储网络的网口绑定模式转换为 OVS Bond 下的 `balance-tcp` 模式，以提升系统性能。

完成转换后，建议在物理交换机上配置 Port Channel 哈希策略，以便充分利用多网口的带宽。具体方法请参考《SMTX ZBS 集群安装部署指南》的[配置 Port Channel 哈希策略](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_106)。

**注意事项**

若存储网络使用 Mellanox CX5 网卡且启用 RDMA 时，仅支持配置为 `active-backup` 绑定模式，不支持 `balance-tcp` 模式。若需实现存储网络 RDMA 多路径，建议使用 Mellanox CX6 网卡。

**前提条件**

集群已完成了升级。

## OVS Bond 和 Linux Bond 转换规则

OVS Bond 包括 `active-backup`、`balance-tcp`、`balance-slb` 三种绑定模式；

Linux Bond 包括 `active-backup`、`802.3ad`、`balance-xor` 三种绑定模式。

将 Linux Bond 转换为 OVS Bond 时，支持如下几种转换方式：

- `active-backup`（Linux Bond）或 `balance-xor`（Linux Bond）可以直接转换为 `active-backup`（OVS Bond）；
- `802.3ad`（Linux Bond） 可以直接转换为 `balance-tcp`（OVS Bond）；
- `active-backup`（Linux Bond） 或 `balance-xor`（Linux Bond） 不可直接转换为 `balance-tcp`（OVS Bond），需先转换为 `active-backup`（OVS Bond），再转换为 `balance-tcp`（OVS Bond）。

在将 Linux Bond 转换至对应的 OVS Bond 后，您也可以在不同的 OVS Bond 模式之间进行转换，最终达到您的转换目的。

> **注意**：
>
> - 存储网络开启 RDMA 时不支持 `balance-slb`（OVS Bond）绑定模式。
> - 若要将绑定模式转换为 `balance-TCP`（OVS Bond），对端交换机需先开启 LACP 动态链路聚合，并建议在转换前参考《SMTX ZBS 集群安装部署指南》[为交换机配置 Port Channel 哈希策略](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_106)。

## 执行转换

> **注意**：
>
> 为保障块存储集群的整体服务在转换过程中不受影响，以下转换操作请在集群各节点依次进行，且 Meta Leader 节点须在最后执行。

1. 使用 SSH 方式登录待转换节点。执行以下命令，确认块存储集群是否有待恢复数据。若有待恢复数据，请在数据恢复完成后再执行后续步骤。

   `zbs-meta pextent find need_recover`

   `zbs-meta pextent find may_recover`
2. 执行 `ovs-vsctl show` 命令，获取并记录存储网络的 OVS 网桥名称。以下输出示例中，`Port port-storage` 所在的 `Bridge ovsbr-90k630795`，其名称 `ovsbr-90k630795` 即为网桥名称。

   ```
    Bridge ovsbr-90k630795
        Port port-storage
            tag: 0
            Interface port-storage
                type: internal
        Port bond2
            Interface bond2
        Port ovsbr-90k630795
            Interface ovsbr-90k630795
                type: internal
   ```
3. 执行如下命令，获取并记录存储网络的 OVS 网桥使用 Linux Bond 模式时的网口绑定名称。

   `network-tool get-bond-name --ovsbr_name <ovsbr_name>`
4. 设置主机进入维护模式。可以通过 CloudTower 或使用命令行设置主机进入维护模式。

   - **通过 CloudTower**

     进入 CloudTower 管理界面，在块存储集群的主机列表中选中目标主机，单击右侧的 `...` 后选择进入维护模式。
   - **使用命令行**

     执行如下命令。其中 `cid` 为 Chunk ID，`EXPIRE_DURATION_S` 为维护模式过期时间，建议设置为 600（s）。

     `zbs-meta chunk set_maintenance <cid> true [--expire_duration_s <EXPIRE_DURATION_S>]`
5. 执行如下命令，修改网口的绑定模式。

   `network-tool change-bridge --ovsbr_name <ovsbr_name> --old_port_name <old_port_name> --nics <target_nics> --bond_mode <bonding_mode> --bond_name <bond_name>`

   > **注意**：
   >
   > 若要将绑定模式从 `balance-xor`(Linux Bond) 转换为 `active-backup`(OVS Bond)，执行转换动作前需取消交换机的 Port Channel 配置。

   各配置参数说明如下。

   | 参数 | 描述 |
   | --- | --- |
   | `--ovsbr_name <ovsbr_name>` | 输入存储网络 OVS 网桥名称。 |
   | `--old_port_name <old_port_name>` | 输入在原绑定模式下 OVS 网桥所关联的物理网口的绑定名称。 |
   | `--nics <target_nics>` | 输入 OVS 网桥需要关联的所有网口名称，例如 `ens5f0np0 ens5f1np1`。 |
   | `--bond_mode <bonding_mode>` | 输入 OVS 网桥要转换的 OVS Bond 模式。 |
   | `--bond_name <bond_name>` | 将 Linux Bond 转换为 OVS Bond 后，OVS 网桥的网口绑定名称只能选择 `bond0`、`bond1`、`bond2` 以外的名称，且不能和当前集群中已有的 bond 名称重复。 |

   例如：将 Linux Bond 的 active-backup 模式转换为 OVS Bond 的 active-backup 模式时，可执行如下命令：

   `network-tool change-bridge --ovsbr_name ovsbr-6cnw0rzfs --old_port_name bond2 --nics "ens5f0np0 ens5f1np1" --bond_mode active-backup --bond_name bond-storage`
6. 执行以下命令，将修改后的网口绑定信息同步至数据库。其中 `bonding_mode` 必须与上一步设置的 `bonding_mode` 保持一致。

   `network-tool sync-bridge --ovsbr_name <ovsbr_name> --bond_mode <bonding_mode> --bond_name <bond_name> --nics <uplink_nics>`

   执行完命令后，若系统输出 `sync successfully`，则表明同步数据成功。
7. 通过 CloudTower 界面，或执行 `zbs-meta chunk set_maintenance <cid> false` 命令，退出维护模式。
8. 转换过程网络会短暂中断并触发数据恢复。请等待数据恢复结束，然后继续在其他节点执行如上转换步骤，直至所有节点都已转换完毕。

---

## 升级文件存储集群

# 升级文件存储集群

本版本配套的文件存储为 1.3.0 版本，若块存储集群部署了低版本的文件存储集群，请在升级块存储集群后，将文件存储集群升级至 1.3.0 版本。

请在完成块存储集群的升级后，对文件存储集群进行升级。

---

## 升级文件存储集群 > 上传文件存储安装包

# 上传文件存储安装包

请执行以下操作步骤，上传目标版本的文件存储安装包。

**操作步骤**

1. 登录 CloudTower，进入**文件存储**页面，单击**设置**，选择**安装包管理**。
2. 单击右上角的 **+ 上传安装包**，上传 `tar.gz` 格式的安装包。
3. 单击**上传**。

**相关操作**

如需删除安装包，请确认 CloudTower 中不存在使用该安装包部署的文件存储集群。

---

## 升级文件存储集群 > 执行升级

# 执行升级

在 CloudTower 中上传了目标版本的文件存储安装包后，系统将提示`可升级`，您可以参照本节内容升级文件存储集群至 1.3.0 版本。

**前提条件**

- 已上传目标版本的文件存储安装包。
- 文件存储集群状态为`正常`。
- 文件存储集群里不存在状态为`创建中`、`更新中`的文件系统。
- 从 1.2.0 以下版本升级至本版本时，如文件控制器所属的 SMTX ZBS 块存储集群已启用常驻缓存，请确保该 SMTX ZBS 块存储集群中空闲常驻缓存容量不少于`当前文件存储集群内所有文件控制器中未开启常驻缓存的系统盘容量的总和 * 2`。
- 当主机 CPU 架构为 Hygon x86\_64 时，文件控制器将独占 CPU 资源，请参考[系统总 CPU 占用说明](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_109#hygon-x86_64-%E6%9E%B6%E6%9E%84)确保可独占的 CPU 资源充足。

**注意事项**

升级文件存储集群过程中，请不要为块存储集群中其他存储卷启用常驻缓存，以避免升级过程中出现常驻缓存不足导致升级失败。

**操作步骤**

1. 在文件存储集群列表中，单击文件存储集群版本信息右侧的**可升级**，或在**文件存储集群**页面中单击**设置**页签，选择**集群升级**。
2. 在**集群升级**页面单击目标版本右侧的**升级**。
3. 在弹出的**升级文件存储集群**对话框中单击**升级**。

---

## 附录 > 对节点进行内存扩容

# 对节点进行内存扩容

请参考如下方法对 SMTX ZBS 节点进行内存扩容。

> **注意**：
>
> Meta Leader 节点应最后执行操作。在集群任一节点执行 `zbs-tool service list` 命令可确认集群的 Meta Leader 节点。

1. 将节点设置为维护模式。

   对于 5.3.0 及以上版本的集群，请通过 CloudTower 界面设置维护模式，对于 5.2.0 及以下版本的集群，请通过命令行的方式设置维护模式。

   - **5.3.0 及以上版本集群**

     登录 CloudTower，在集群的主机列表中选中此节点所在的主机，单击右侧的 **…**，并选择**进入维护模式**。
   - **5.2.0 集群**

     执行以下命令使此节点进入存储维护模式：

     `zbs-meta chunk set_maintenance <cid> true [--expire_duration_s <EXPIRE_DURATION_S>]`

     - `expire_duration_s`：存储维护模式超时时间，仅在进入存储维护模式时有效；若不设置该参数，则系统默认为最大值 604800 秒（7 天）。
     - `cid`：表示将要设置存储维护模式的 Chunk ID。可通过执行命令 `zbs-meta chunk list` 来获取 Chunk ID。
     > **说明**：
     >
     > 若上述命令返回 `Failed to set maintenance mode due to extents in recover` 或者 `Failed to set maintenance mode due to extents may recover`，表明当前集群存在数据恢复，请等待数据恢复完成后重试。
2. 当主机处于维护模式状态后，执行命令 `shutdown -h now`，关闭节点。
3. 对主机进行内存扩容。
4. 启动主机，开机后登录主机的 IPMI 管理控制台，确认 IPMI 管理控制台已识别新扩容的内存。
5. 退出维护模式。

   - **5.3.0 及以上版本集群**

     1. 在 CloudTower 的主机概览界面中查看当前主机已处于维护模式的时间，单击提示内容右侧的退出维护模式。
     2. 系统弹出检查对话框，并启动退出维护模式前的自检，检查结束后返回所有自检项目的检查结果。

        - 若所有检查项目全部满足要求，允许主机退出维护模式。
        - 若部分检查结果不满足要求，请参考《SMTX ZBS 块存储集群运维指南》中的**主机维护模式**章节，对照[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)前的检查项目及结果一览表的**后续操作及建议**完成整改，然后再次尝试退出维护模式。
   - **5.2.0 版本集群**

     1. 执行 `zbs-meta chunk list` 命令检查集群节点状态，若返回 `CONNECTED_HEALTHY` 则表明集群状态正常。
     2. 确认集群状态正常后，执行 `zbs-meta chunk set_maintenance <cid> false` 命令使节点退出存储维护模式。

---

## 附录 > SMTX ZBS 节点的本地账户说明

# SMTX ZBS 节点的本地账户说明

SMTX ZBS 节点支持以下三种本地账户：

| **本地账户** | **说明** | **注意事项** |
| --- | --- | --- |
| root | 默认账户，默认禁止 SSH 远程登录。您可以使用该账户管理节点。 | - 请勿删除该账户。 - 强烈建议不要开启 root 账户通过 SSH 远程登录的权限。 - 以命令行方式升级集群时必须拥有 root 权限。 |
| smartx | 默认账户，默认支持 SSH 远程登录。您可以使用该账户通过 SSH 协议远程连接到节点。 | - 请勿删除该账户。 - 请勿更改 `/etc/sudoers` 里针对该账户的配置。 - 以该账户登录节点后，必须切换为 root 账户再执行运维操作。执行 `sudo su` 命令可免密码切换。 |
| 其他本地账户 | 由 root 账户创建的其他账户，账户权限由 root 账户决定。您可自行创建新的本地账户用于 SSH 远程登录。 | - |

---

## 附录 > SMTX OS 节点的本地账户

# SMTX OS 节点的本地账户

SMTX OS 节点支持以下三种本地账户：

| 本地账户 | 说明 |
| --- | --- |
| root | 默认账户，禁止 SSH 远程登录。 |
| smartx | 默认账户，支持 SSH 远程登录。 |
| 其他本地账户 | 由 `root` 账户创建的其他账号，账户权限由 `root` 账户决定。 |

- **root 账户**：每个 SMTX OS 主机都有一个根用户帐户 `root`，该帐户可用于本地管理。SmartX 强烈建议用户不要开启 `root` 账户通过 SSH 远程登录的权限。以命令行方式集群时必须拥有 `root` 权限。
- **smartx 账户**：每个 SMTX OS 主机上会默认创建 `smartx` 帐户。用户可以使用该账户通过 SSH 协议远程连接到 SMTX OS 节点。
- **其他本地账户**：用户可自行创建新的本地账户用于 SSH 远程登录。

> **注意**：
>
> - 请勿删除默认账户。
> - 请勿更改 `/etc/sudoers` 里针对 `smartx` 账户的配置。
> - 以 `smartx` 账户登录节点后，必须切换为 `root` 账户再执行运维操作。执行 `sudo su` 命令可免密码切换。
> - 以命令行方式升级集群时必须拥有 `root` 权限。

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
