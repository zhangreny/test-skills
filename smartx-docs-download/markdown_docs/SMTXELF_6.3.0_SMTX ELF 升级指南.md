---
title: "SMTXELF/6.3.0/SMTX ELF 升级指南"
source_url: "https://internal-docs.smartx.com/smtxelf/6.3.0/elf_upgrade_guide/preface_elf_upgrade_guide"
sections: 15
---

# SMTXELF/6.3.0/SMTX ELF 升级指南
## 关于本文档

# 关于本文档

本文档介绍了 SMTX ELF 从 6.x.x 版本升级到此版本的流程和步骤。

阅读本文档需要了解 SMTX ELF 虚拟化软件，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

**2026-02-04：配合 SMTX ELF 6.3.0 正式发布**

相较于 SMTX ELF 6.2.0，本版本主要进行了如下更新：

- **升级说明**：更新升级路径。
- **升级前准备**：新增**确认集群的 SSH 端口是否为 22**小节。
- **手动升级内核** > **内核更新记录**：新增 SMTX ELF 6.3.0 的内核更新记录。

---

## 概述

# 概述

SMTX ELF 支持使用以下两种方式进行升级。

- **通过升级中心升级**

  通过 CloudTower 的升级中心，可以一站式完成集群升级和内核升级操作，极大降低操作难度，有效提升升级效率和成功率，建议您参考[《升级中心使用指南》](/cluster-upgrade/1.2.1/cluster_upgrade_user_guide/cluster_upgrade_user_guide_01)进行升级。
- **通过命令行升级**

  在集群单个节点上执行命令行升级操作即可完成整个集群的升级，无需人工干预，且可以查看详细的升级日志。

---

## 升级说明

# 升级说明

## 升级路径

SMTX ELF 6.0.0 ~ 6.2.0 P4 版本可通过升级中心或命令行的方式直接升级到本版本。

具体的升级路径可参考如下升级路径图。

![](https://cdn.smartx.com/internal-docs/assets/f3307ae5/elf_upgrade_guide_02.png)

## 升级流程

SMTX ELF 升级流程图如下：

![](https://cdn.smartx.com/internal-docs/assets/f3307ae5/elf_upgrade_guide_01.png)

## 升级特点

SMTX ELF 采用在线不停机的方式进行升级。

## 升级时限制的操作

进行集群和内核升级不会影响业务的正常运行，但禁止执行如下操作：

- 为集群添加或移除主机。
- 将集群从 CloudTower 中移除。
- 手动将主机进入或退出维护模式。
- 手动关机或重启主机。
- 对主机执行角色转换操作。

---

## 升级前准备

# 升级前准备

在启动升级前，请检查并做如下准备。

## 获取目标版本的升级文件

根据您选择的升级方式，以及当前虚拟化平台的服务器类型，提前获取目标版本的 SMTX ELF 的升级 ISO 文件。

## 确认是否需要升级内核版本

SMTX ELF 将不定期提供新的内核版本以提⾼系统性能或应对安全风险，新的内核版本集成在 SMTX ELF 新版本的安装部署文件和升级文件中。

在准备升级前，您可先通过查看[内核更新记录](/smtxelf/6.3.0/elf_upgrade_guide/elf_upgrade_guide_06)，确认升级前的内核版本与升级后目标版本所配套的内核版本是否一致。若版本不一致，可根据内核更新记录按需更新。

- 若您使用升级中心升级集群，可在升级界面选择在升级集群的同时自动升级内核，或在升级集群后单独升级内核。具体说明请参考[《升级中心使用指南》](/cluster-upgrade/1.2.1/cluster_upgrade_user_guide/cluster_upgrade_user_guide_01)。
- 若您使用命令行升级集群，需要在集群升级完成后手动升级内核。具体操作请参考本文档的[手动升级内核](/smtxelf/6.3.0/elf_upgrade_guide/elf_upgrade_guide_05)。

## 确认内存资源是否充足

在正式执行升级前，请先确认目标版本系统需占用的内存资源（详见[《SMTX ELF 配置和管理规格》](/smtxelf/6.3.0/elf_config_specs/elf_installation_guide/elf_installation_guide_13)。若剩余内存不满足目标版本要求，则无法升级。在此情况下节点需提前释放内存，然后重新发起升级，具体操作方法如下。

- 将对应节点上的虚拟机迁移至其他内存充足的节点以释放内存。
- 若迁移虚拟机的方式无法释放足够内存，可考虑关闭对应节点上的一些非必需的虚拟机来释放内存。

## 确认系统分区空间是否充足

若系统分区空间使用率较高，升级组件可能无法正常工作导致集群升级失败。因此，需要在升级前对系统分区空间进行清理以解决此报警，然后才可进行后续的升级动作。

## 确认集群是否启用了动态资源调度

在使用升级中心对集群和内核进行升级操作前，或手动升级内核前，请确保集群已关闭动态资源调度功能，避免升级过程中自动迁移虚拟机，影响升级流程。请进入集群主界面，选择动态资源调度，关闭当前集群的动态资源调度功能，升级完成后再恢复启用。

## 确认集群的状态

请确认待升级的集群满足如下要求：

- 集群中没有主机处于维护模式或进入维护模式中；
- 集群中所有主机均处于健康状态；
- 集群未处于环境检查中、升级中或升级内核中状态；
- 集群中没有正在添加的主机；
- 如使用升级中心升级，集群与 CloudTower 的连接状态需为`已连接`。

## 确认集群的 SSH 端口号是否为 22

对于 SMTX ELF 6.2.0 及以下版本的集群，在集群升级时，需依赖 SSH 服务的默认 22 端口。若集群的 SSH 端口已被修改为其他端口，请在升级前将 SSH 端口号变更回 22。

---

## 升级集群 > 通过升级中心升级

# 通过升级中心升级

通过升级中心升级集群的操作方法请参考[《升级中心使用指南》](/cluster-upgrade/1.2.1/cluster_upgrade_user_guide/cluster_upgrade_user_guide_01)。

---

## 升级集群 > 通过命令行升级

# 通过命令行升级

**前提条件**

- 已下载适配服务器类型的 SMTX ELF 升级 ISO 文件，以及对应的元数据 JSON 文件。
- 拥有超级管理员 root 的操作权限。该权限说明可参见 [SMTX ELF 节点的本地账户说明](/smtxelf/6.3.0/elf_installation_guide/elf_installation_guide_48)。

**注意事项**

- 在集群升级过程中，系统会暂停 `elf-vm-monitor` 和 `elf-vm-watchdog` 服务，同时触发监控报警系统对此服务的报警。用户可以忽略该告警，待升级结束后，系统将自动恢复 `elf-vm-monitor` 和 `elf-vm-watchdog` 服务的运行。
- 如果升级过程中断，`elf-vm-monitor` 和 `elf-vm-watchdog` 服务将处于停止运行的状态。在查明升级中断的原因前，请勿启动任何节点的 `elf-vm-monitor` 服务。重新执行升级命令并顺利完成升级后，系统将自动恢复 `elf-vm-monitor` 和 `elf-vm-watchdog` 服务的运行。

**操作步骤**

您只需在集群的某个节点执行命令行操作，即可完成整个集群的升级。

1. 使用 root 账号登录服务器节点的 SMTX ELF 系统，利用工具将目标版本的升级 ISO 文件及对应的元数据 JSON 文件上传至集群的某个节点。

   举例：集群某个节点的管理 IP 地址为 `192.168.75.101`，升级前可借助 Xshell 工具（或其他同类工具）将目标版本的升级 ISO 文件和对应的元数据 JSON 文件上传至 `192.168.75.101` 节点的 `/home/smartx` 目录下。
2. 输入以下命令，挂载升级 ISO 文件，并配置 yum 源为 `smartxos.repo`。

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

   执行完毕后，检查 `/etc/yum.repos.d`，确保此目录下仅有 `smartxos.repo` 文件, 并且其内容与上述要求的一致。
3. 安装或更新 `cluster-upgrade rpm` 包，请输入以下命令进行更新。

   `yum clean all`

   `yum install -y cluster-upgrade`
4. 进入 `/usr/share/upgrade/runner/` 目录下，执行以下脚本。其中 `<iso path>` 表示升级的目标版本的升级 ISO 文件的绝对路径，`<metadata path>` 表示升级的目标版本的 ISO 元数据文件的绝对路径。

   `nohup python cluster_upgrader.py --iso_path <iso path> --metadata_path <metadata path> &`
5. 在脚本执行过程中，输入命令 `tail -f nohup.out` 实时查看更新日志。

   - 若集群升级成功，则日志中将输出 `Cluster upgrade successful`。
   - 若集群升级失败，则请先根据相关日志定位出失败原因并解决问题，然后再重新升级，将会从上次升级失败后继续进行后续升级。

> **说明**：
>
> - 当在日志中出现提示信息如“存在正在进行的准备升级工具进程，无法进行集群升级”或“存在其他正在进行的集群升级进程”时：
>   - 若该现象是由其他人在同时升级所导致，则不需要再重新升级。
>   - 若该现象不是由其他人在同时升级所导致，则请在所使用虚拟化平台对应的节点系统中执行 `cluster-upgrade clear_upgrade_event` 命令清理升级失败的信息，最后再重新升级。
> - 若升级失败，在修复相关问题后可继续升级。系统将自动跳过已执行的步骤，并从上次失败的步骤继续执行。

---

## 手动升级内核

# 手动升级内核

若升级目标版本所对应的内核版本与升级前的内核版本不一致，请根据[内核更新记录](/smtxelf/6.3.0/elf_upgrade_guide/elf_upgrade_guide_06)，按需升级内核。

本章节介绍了如何使用命令行手动升级内核。若您的集群版本支持使用升级中心进行升级，请参考[《升级中心使用指南》](/cluster-upgrade/1.2.1/cluster_upgrade_user_guide/cluster_upgrade_user_guide_01)完成对内核的自动升级。

**升级说明**

- 当 SMTX ELF 部署在不同的服务器平台时，与其配套使用的内核版本均不同，但手动升级内核版本的操作步骤基本相同。
- 若节点已安装了 vGPU 驱动，在升级内核后，需要将驱动更新至新内核的对应版本。

**前提条件**

集群已完成升级。

**注意事项**

- 在升级内核前，请确保集群已关闭动态资源调度功能，避免升级过程中自动迁移虚拟机，影响升级流程。请进入集群主界面，选择**动态资源调度**，关闭当前集群的动态资源调度功能，升级完成后再恢复启用。
- 升级结束后，需要重启物理机使升级生效，系统将会出现短暂的 I/O 中断，但不影响业务的正常运行。

---

## 手动升级内核 > 内核更新记录

# 内核更新记录

下表列出了 SMTX ELF 版本与内核版本的配套关系及更新记录。

当 SMTX ELF 部署在不同架构的服务器时，与其配套使用的内核版本均不同，请参照部署的服务器类型，查看对应的内核版本更新记录。

SMTX ELF 全新安装时默认使用对应的内核版本，但 SMTX ELF 升级时默认不自动升级内核，需要手动更新。

## Intel x86\_64、AMD x86\_64、Hygon x86\_64 或兆芯 x86 架构

| SMTX ELF 版本 | 内核版本 | 更新原因 |
| --- | --- | --- |
| 6.1.0～6.1.1 | kernel-4.19.90-2307.3.0.oe1​.smartx.59.x86\_64.rpm | - sysfs 暴露 scsi io timeout 指标 - 限制 tun 设备打印异常包的速率 - 解决 ovs nested actions 导致的内存泄漏问题 - 解决中断重入的误判打印 - 新增 mpi3mr 驱动，支持 H965 系列 RAID 卡 - 优化 tcp 包在 conntrack 中是否无效的判定 - 解决网络 bug 导致的虚拟机接受到元数据被破坏的网络包 - 修复 nf 模块的安全漏洞 CVE-2024-1086 - 优化 overlay 网络中的 udp 性能 - 支持 conntrack 过滤器 - 新增海光 4 PMU 等模块支持 - 解决 hygon 平台 PCIe 设备直通时 iommu 异常 |
| 6.2.0 | kernel-4.19.90-2307.3.0.​oe1.v97.x86\_64.rpm | - 支持海光 HCT 加密设备 - 支持 SSSRAID 控制卡 - 支持网迅万兆网卡（txgbe 系列） - 虚拟机 CPU 兼容性支持 IceLake CPU model - 修复 QLogic 网卡开启 PTP 特性时，CPU 使用率突增的问题 - 修复 vCPU 热添加场景中，Guest OS 时钟同步异常的问题 - 修复安全漏洞 CVE-2019-3016 - 修复仅支持 32 bit MSI 的 PCIe 设备无法工作的问题 - 修复 Hygon CPU 缺陷 errata 1096 - 修复数据不一致导致的块层 I/O 卡死问题 - 修复 ext4 文件系统在线重置容量可能导致数据被破坏的问题 - 修复内存子系统可能被破坏的问题 - 修复 buffer I/O 数据可能不一致的问题 - 修复 KVM 异步缺页异常导致卡死的问题 - 修复内存申请路径可能卡死的问题 - 修复 Windows 虚拟机直通 NVIDIA A 系列显卡导致主机宕机并重启的问题 |
| 6.3.0 | 基于 openEuler：kernel-5.10.0-247.0.0.oe1.v79.x86\_64.rpm | - 内核升级至 5.10.0-247.0.0 - 升级 linkdata raid 卡驱动至 2.6.0.23 - 升级 mpt3sas 驱动至 55.00.00.00 - 升级 i40e 驱动至 2.20.12 - 升级 megaraid 驱动至 07.735.03.00 |
| 基于 TencentOS：kernel-5.4.119-19.0009.54.tl3.v98.x86\_64.rpm | - |

## 鲲鹏 AArch64 或飞腾 AArch64 架构

| **SMTX ELF 版本** | **内核版本** | **更新原因** |
| --- | --- | --- |
| 6.1.0～6.1.1 | kernel-4.19.90-2307.3.0.​oe1.smartx.59.aarch64.rpm | - sysfs 暴露 scsi io timeout 指标 - 限制 tun 设备打印异常包的速率 - 解决 ovs nested actions 导致的内存泄漏问题 - 解决中断重入的误判打印 - 新增 mpi3mr 驱动，支持 H965 系列 RAID 卡 - 优化 tcp 包在 conntrack 中是否无效的判定 - 解决网络 bug 导致的虚拟机接受到元数据被破坏的网络包 - 修复 nf 模块的安全漏洞 CVE-2024-1086 - 优化 overlay 网络中的 udp 性能 - 支持 conntrack 过滤器 |
| 6.2.0 | kernel-4.19.90-2307.3.0.oe1.v97.aarch64.rpm | - 支持飞腾 S5000C 系列 CPU - 支持 SSSRAID 控制卡 - 支持网迅万兆网卡（txgbe 系列） - 支持在集群中使用虚拟 PTP 硬件时钟（PTP Hardware Clock）以确保虚拟机和其主机时间同步 - 修复 QLogic 网卡开启 PTP 特性时，CPU 使用率突增的问题 - 修复安全漏洞 CVE-2019-3016 - 修复仅支持 32 bit MSI 的 PCIe 设备无法工作的问题 - 修复数据不一致导致的块层 I/O 卡死问题 - 修复 ext4 文件系统在线重置容量可能导致数据被破坏的问题 - 修复内存子系统可能被破坏的问题 - 修复 buffer I/O 数据可能不一致的问题 - 修复 KVM 异步缺页异常导致卡死的问题 - 修复内存申请路径可能卡死的问题 |
| 6.3.0 | 基于 openEuler：kernel-5.10.0-247.0.0.oe1.v79.aarch64.rpm | - 内核升级至 5.10.0-247.0.0 - 升级 linkdata raid 卡驱动至 2.6.0.23 - 升级 mpt3sas 驱动至 55.00.00.00 - 升级 megaraid 驱动至 07.735.03.00 - 支持海思 SP680 系列网卡 |
| 基于 TencentOS：kernel-5.4.119-19.0009.54.tl3.v98.aarch64.rpm | - |

---

## 手动升级内核 > 执行升级

# 执行升级

**前提条件**

- 检查集群资源，确保集群的计算资源和存储资源均满足集群中单节点故障场景。
- 执行命令 `uname -a` ，查看并记录升级前的内核版本。
- 集群已完成升级，否则将导致内核与内部服务不兼容。
- 对照《SMTX ELF 运维指南》中的[进入维护模式的要求](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_43)完成自检，确认所有检查项目满足要求。
- 若待升级主机上存在安装了 vGPU 的虚拟机，则需要将这些虚拟机关机。

## 第 1 步：上传升级 ISO 文件至节点

上传本版本升级 ISO 文件到节点，并在该节点执行以下命令，以准备升级内核所需的 repo，然后记录此节点的存储接入 IP。其中，`<iso_path>` 表示 ISO 文件在该节点的绝对路径。

`cluster-upgrade prepare_repo <iso_path>`

执行完成后，如果输出信息显示 `prepare repo success`，表明 repo 已准备完成。

## 第 2 步：升级节点的内核

1. 登录 CloudTower，在集群的主机列表中选中节点所在的主机，单击右侧的 **...** 后选择**进入维护模式**。
2. 执行下述命令用于准备 repo。其中 `<repo_ip>` 为 Meta Leader 节点的存储接入 IP。

   `cluster-upgrade config_repo --repo_ip <repo_ip>`

   执行完成后，若输出信息显示 `config repo success.`，表明当前节点升级内核所需要的 repo 已配置完成。
3. 执行以下命令进行内核升级。当显示 `Upgrade done` 字样时，表明升级成功。

   `skc upgrade`
4. 登录 CloudTower，在集群的主机列表中选中目标主机，单击右侧的 **...** 后选择**重启**，输入重启原因后重启主机。
5. 执行 `uname -a` 命令，查看内核是否已成功升级到目标版本。若升级不符合预期，可参考[回滚内核版本](/smtxelf/6.3.0/elf_upgrade_guide/elf_upgrade_guide_08)一节对内核进行回滚。
6. 在 CloudTower 的主机概览页面查看当前主机已处于维护模式的时间，单击提示内容右侧的**退出维护模式**。
7. 系统弹出检查对话框进行退出检查，检查结束后返回所有检查项目的检查结果。

   - 所有检查项目全部满足要求，允许主机退出维护模式。单击**退出维护模式**。
   - 部分检查结果不满足要求，请对照《SMTX ELF 运维指南》中的[退出维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_44)的要求进行调整，然后再次尝试退出主机维护模式。
8. 切换至其他节点，执行如上步骤，直至所有节点完成升级。

## 第 3 步：清理 boot 分区残留的内核包

由于 `/boot` 分区存储空间有限，在多次升级内核后，`/boot` 分区存储空间可能会被占满。可执行 `skc clean` 命令，清理掉没有运行的驱动和内核包。

---

## 手动升级内核 > 回滚内核版本

# 回滚内核版本

若升级内核失败或升级的版本不及预期，可参考如下步骤回滚内核。

**操作步骤**

1. 执行 `skc boot` 命令，选择要回滚到的内核版本。主机重启后将默认启动该内核。
2. 登录 CloudTower，在集群的主机列表中选中此节点所在的主机，单击右侧的 **...** 后选择**进入维护模式**。
3. 当主机处于维护模式后，在集群的主机列表中选中目标主机，单击右侧的 **...** 后选择**重启**，输入重启原因后重启主机。
4. 执行 `uname -a` 命令，确认当前内核是否已经成功回滚为目标版本。

---

## 手动升级内核 > 更新 vGPU 驱动

# 更新 vGPU 驱动

节点 vGPU 驱动的版本需适配内核版本。因此，若节点已安装 vGPU 驱动，在升级或回退内核版本后，vGPU 驱动也需更新至适配新内核的版本。

**准备工作**

- 执行命令 `uname -a`，查看该主机当前的内核版本。根据内核版本和所需的 vGPU 驱动版本，获取驱动安装包。

  > **说明**：
  >
  > 使用 NVIDIA L20 时请选择开放驱动。
- 待更新驱动所在主机上挂载了 vGPU 的虚拟机均处于关机状态。

**操作步骤**

1. 登录 CloudTower，将主机[置为主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_43)。
2. 上传驱动安装包到该主机的 `/home/smartx` 路径下。
3. 执行如下命令，删除当前的 vGPU 驱动。

   ```
   rpm -e Nvidia-vGPU
   ```
4. 删除后执行命令 `rpm -qi Nvidia-vGPU`，确认驱动已删除成功。示例输出如下：

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

## 升级后配置 > 禁用 Spectre 和 Meltdown 补丁（可选）

# 禁用 Spectre 和 Meltdown 补丁（可选）

为应对以下漏洞造成的安全风险，SMTX ELF 通过升级内核（以启用补丁的形式）对漏洞进行了修复。新的漏洞补丁可能会导致 I/O 性能下降约 20% ~ 30%。SMTX ELF 升级至目标版本后，您可参考自身情况，在合适的场景下手动禁用补丁。

- Intel Spectre（[CVE-2017-5753](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5753)、[CVE-2017-5715](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5715)）
- Meltdown（[CVE-2017-5754](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5754)）

> **说明**：
>
> 若集群在升级前已禁用了 Spectre 和 Meltdown 补丁，在升级至新版本后，禁用仍然生效，无需再次手动禁用。

**禁用方法**

> **说明**：
>
> 以下操作需在集群中每个节点执行。

1. 在节点打开 `/etc/default/grub` 文件并定位至 `GRUB_CMDLINE_LINUX` 行。向 `GRUB_CMDLINE_LINUX` 中增加 `noibrs noibpb nopti nospectre_v2 nospectre_v1 l1tf=off nospec_store_bypass_disable no_stf_barrier mds=off mitigations=off`。

   ```
   [root@node ~]$cat /etc/default/grub | grep GRUB_CMDLINE_LINUX
    GRUB_CMDLINE_LINUX="crashkernel=2048M,high rd.md.uuid=00f5a41e:86a83763:655f8331:092cd656 noibrs noibpb nopti nospectre_v2 nospectre_v1 l1tf=off nospec_store_bypass_disable no_stf_barrier mds=off mitigations=off"
   ```
2. 更新 Grub。

   - 若系统存在 `/sys/firmware/efi` 目录且不为空，执行如下命令更新 Grub：

     `grub2-mkconfig -o /etc/grub2-efi.cfg`
   - 若系统不存在 `/sys/firmware/efi`目录，执行如下命令更新 Grub：

     `grub2-mkconfig -o /etc/grub2.cfg`
3. 执行 `reboot` 命令重启系统。
4. 节点重启后，执行如下命令，确认输出结果中已包含了在 `GRUB_CMDLINE_LINUX` 增加的参数。

   `cat /proc/cmdline`

---

## 附录 > SMTX ELF 节点的本地账户说明

# SMTX ELF 节点的本地账户说明

SMTX ELF 节点支持以下三种本地账户：

| 本地账户 | 说明 | 注意事项 |
| --- | --- | --- |
| root | 默认账户，默认禁止 SSH 远程登录。您可以使用该账户管理 SMTX ELF 节点。 | - 请勿删除该账户。 - 强烈建议不要开启 root 账户通过 SSH 远程登录的权限。 - 以命令行方式升级集群时必须拥有 root 权限。 |
| smartx | 默认账户，默认支持 SSH 远程登录。您可以使用该账户通过 SSH 协议远程连接到 SMTX ELF 节点。 | - 请勿删除该账户。 - 请勿更改 `/etc/sudoers` 里针对该账户的配置。 - 以该账户登录节点后，必须切换为 root 账户再执行运维操作。执行 `sudo su` 命令可免密码切换。 |
| 其他本地账户 | 由 root 账户创建的其他账户，账户权限由 root 账户决定。您可自行创建新的本地账户用于 SSH 远程登录。 | - |

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
