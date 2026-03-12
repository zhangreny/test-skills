---
title: "SMTXOS/6.3.0/SMTX OS 升级指南"
source_url: "https://internal-docs.smartx.com/smtxos/6.3.0/upgrade_guide/preface_upgrade_guide"
sections: 26
---

# SMTXOS/6.3.0/SMTX OS 升级指南
## 关于本文档

# 关于本文档

本文档介绍了 SMTX OS 系统从 4.0.x、5.0.x、5.1.x 或 6.x.x 版本升级到此版本的流程和步骤。

阅读本文档需要了解 SMTX OS 超融合软件，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

- **2026-02-04：配合 SMTX OS 6.3.0 正式发布**

  相较于 SMTX OS 6.2.0，本版本主要进行了如下更新：

  - 更新升级路径；
  - 升级前准备增加对 SSH 端口是否为 22 的检查；
  - 更新内核版本记录。
  - 更新[转换网口绑定模式](/smtxos/6.3.0/upgrade_guide/upgrade_guide_28)。

---

## 概述

# 概述

SMTX OS 支持使用三种方式进行升级。不同版本集群支持的升级方式可能不同，具体请参考[升级路径](/smtxos/6.3.0/upgrade_guide/upgrade_guide_01#%E5%8D%87%E7%BA%A7%E8%B7%AF%E5%BE%84)。

- **通过升级中心升级**

  通过 CloudTower 的升级中心，可以一站式完成集群升级和内核升级操作，极大降低操作难度，有效提升升级效率和成功率。若集群版本支持使用升级中心升级，建议您参考[《升级中心使用指南》](/cluster-upgrade/1.1.2/cluster_upgrade_user_guide/cluster_upgrade_user_guide_01)进行升级。
- **通过命令行升级**

  在集群单个节点上执行命令行升级操作即可完成整个集群的升级，无需人工干预，且可以查看详细的升级日志。
- **通过 Web 控制台升级**

  对于不支持 CloudTower 管理的集群，可通过集群的 Web 控制台进行升级。

---

## 升级说明

# 升级说明

## 升级路径

当 SMTX OS 部署在不同的服务器平台时，从低版本升级到本版本的路径也不同。请参照部署 SMTX OS 的服务器类型，查看对应的升级路径。

### Intel x86\_64 或 AMD x86\_64 架构

| **源软件版本** | **说明** |
| --- | --- |
| 4.0.5 ~ 4.0.14 | 可直接升级到本版本 |
| 5.0.0 ~ 5.0.7 P2 | 可直接升级到本版本 |
| 5.1.0 ~ 5.1.5 P2 | 可直接升级到本版本 |
| 6.0.0 ~ 6.2.0 P4 | 可直接升级到本版本 |

> **说明**:
>
> - 对于 5.0.5 及以下版本的 SMTX OS 集群，若需升级至基于 openEuler 操作系统的本版本 SMTX OS，请联系 SmartX 售后人员进行升级。
> - 对于 5.1.5 及以下版本，且基于 openEuler 操作系统的 SMTX OS 集群，若需升级至基于 TencentOS 操作系统的本版本 SMTX OS，请联系 SmartX 售后人员进行升级。

具体的升级路径和支持的升级方式可参照如下升级路径图：

![](https://cdn.smartx.com/internal-docs/assets/dc9f6d3b/upgrade_guide_02.png)

### Hygon x86\_64

| **源软件版本** | **说明** |
| --- | --- |
| 4.0.5 ~ 4.0.14，5.0.0 ～ 5.0.2 | 请联系 SmartX 售后人员进行升级 |
| 5.0.3 ~ 5.0.7 P2 | 可直接升级到本版本 |
| 5.1.0 ~ 5.1.5 P2 | 可直接升级到本版本 |
| 6.0.0 ~ 6.2.0 P4 | 可直接升级到本版本 |

### 鲲鹏 AArch64 架构

| **源软件版本** | **说明** |
| --- | --- |
| 4.0.9 ~ 4.0.14，5.0.0 ～ 5.0.2 | 请联系 SmartX 售后人员进行升级 |
| 5.0.3 ~ 5.0.7 P2 | 可直接升级到本版本 |
| 5.1.0 ~ 5.1.5 P2 | 可直接升级到本版本 |
| 6.0.0 ~ 6.2.0 P4 | 可直接升级到本版本 |

## 升级流程

SMTX OS 升级流程图如下：

![](https://cdn.smartx.com/internal-docs/assets/dc9f6d3b/upgrade_guide_01.png)

## 升级特点

SMTX OS 采用在线不停机的方式进行升级。

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

根据当前虚拟化平台的服务器类型，提前获取目标版本的 SMTX OS 的升级 ISO 文件。

## 确认 CloudTower 版本配套关系

SMTX OS 只能由特定版本的 CloudTower 进行管理，请先参考目标版本的《SMTX OS 发布说明》确认该版本集群的配套 CloudTower 版本。如果当前 CloudTower 版本不支持管理目标版本集群，请先升级至配套版本。

## 确认集群的 CPU 微架构要求

SMTX OS 在升级过程中会进行 CPU 指令集检查，服务器的 CPU 需要满足微架构最低要求，否则升级操作会被终止。CPU 的微架构最低要求如下。

- **Intel x86\_64 架构**

  对于在 ELF 虚拟化场景下 SMTX OS 所运行的物理机，以及 VMware ESXi 虚拟化场景下 SCVM 所在的 VMware vSphere 集群所配置的 EVC，其 CPU 的微架构最低要求请遵循下表。

  | **SMTX OS 版本** | **微架构最低要求** |
  | --- | --- |
  | 4.0.5 ~ 4.0.8 | Merom |
  | 4.0.9 | Sandy Bridge |
  | 4.0.10 ~ 4.0.x | Merom |
  | 5.0.0 ~ 5.0.x | Sandy Bridge |
  | 5.1.0 ~ 5.1.x | Sandy Bridge |
  | 6.0.0 ~ 6.x.x | Sandy Bridge |
- **AMD x86\_64 架构**

  | **SMTX OS 版本** | **微架构最低要求** |
  | --- | --- |
  | 5.0.0 ~ 5.0.x | Zen |
  | 5.1.0 ~ 5.1.x | Zen |
  | 6.0.0 ~ 6.x.x | Zen |
- **兆芯 x86 架构**

  | **SMTX OS 版本** | **微架构最低要求** |
  | --- | --- |
  | 6.3.0 ~ 6.x.x | 永丰 |
- **Hygon x86\_64 架构**

  | **SMTX OS 版本** | **微架构最低要求** |
  | --- | --- |
  | 4.0.5 ~ 4.0.x | Dhyana |
  | 5.0.0 ~ 5.0.x | Dhyana |
  | 5.1.0 ~ 5.1.x | Dhyana |
  | 6.0.0 ~ 6.x.x | Dhyana |
- **鲲鹏 AArch64 架构**

  | **SMTX OS 版本** | **微架构最低要求** |
  | --- | --- |
  | 4.0.9 ~ 4.0.x | Taishan v110 |
  | 5.0.0 ~ 5.0.x | Taishan v110 |
  | 5.1.0 ~ 5.1.x | Taishan v110 |
  | 6.0.0 ~ 6.x.x | Taishan v110 |

## 确认是否需要升级内核版本

SMTX OS 将不定期提供新的内核版本以提⾼系统性能或应对安全风险，新的内核版本集成在 SMTX OS 新版本的安装部署文件和升级文件中。

在准备升级前，您可先通过查看[内核更新记录](/smtxos/6.3.0/upgrade_guide/upgrade_guide_18)，确认升级前的内核版本与升级后目标版本所配套的内核版本是否一致。若版本不一致，可根据内核更新记录按需更新。

- 若您使用升级中心升级集群，可在升级界面选择在升级集群的同时自动升级内核，或在升级集群后单独升级内核。具体说明请参考[《升级中心使用指南》](/cluster-upgrade/1.1.2/cluster_upgrade_user_guide/cluster_upgrade_user_guide_01)。
- 若您使用命令行或 Web 控制台升级集群，需要在集群升级完成后手动升级内核。具体操作请参考本文档的[升级内核](/smtxos/6.3.0/upgrade_guide/upgrade_guide_11#%E5%8D%87%E7%BA%A7%E5%86%85%E6%A0%B8)。

## 确认内存资源是否充足

在正式执行升级前，请先确认目标版本系统需占用的内存资源（详见[《SMTX OS 配置和管理规格》](/smtxos/6.3.0/config_specs/config_specs_01)）。若剩余内存不满足目标版本要求，则无法升级。在此情况下，ELF 平台下的节点提前需释放内存，VMware ESXi 平台下的 SCVM 需提前扩展内存。具体操作方法如下。

- **ELF 平台**

  节点可通过下述方式释放内存，释放内存后可重新发起升级。

  - 将对应节点上的虚拟机迁移至其他内存充足的节点以释放内存。
  - 若迁移虚拟机的方式无法释放足够内存，可考虑关闭对应节点上的一些非必需的虚拟机来释放内存。
- **VMware ESXi 平台**

  请参考附录[对 SCVM 进行内存扩容](/smtxos/6.3.0/upgrade_guide/upgrade_guide_15)。

## 确认集群内是否存在挂载 NFS 虚拟卷的虚拟机

对于 SMTX 4.0.5 及以上版本的集群，在升级到本版本之前，需检查集群中是否存在已挂载 NFS 虚拟卷的虚拟机。**请联系 SmartX 售后人员进行处理**。

## 确认集群已使用或总数据容量是否超过 “80 TiB \* 当前许可的最大主机数”

集群在升级预检查时，若检查到当前集群总数据容量或已使用数据容量超过“80 TiB \* 当前许可的最大主机数”，则不允许升级。在此情况下，请先申请并更新包含“集群最大容量值”的许可，确保集群的许可容量大于当前的总数据容量或已使用数据容量，然后再进行升级。

## 确认系统分区空间是否充足

若系统分区空间使用率较高，升级组件可能无法正常工作导致集群升级失败。因此，需要在升级前对系统分区空间进行清理以解决此报警，然后才可进行后续的升级动作。

## 确认数据分区容量和存储引擎版本

由于本版本根据数据分区的容量大小对节点划分了小容量规格、标准容量规格和大容量规格。因此，从低版本升级到本版本时，需根据节点数据分区容量大小，判断应升级为哪种节点规格。

此外，仅支持存储引擎为 LSM2 的集群升级至本版本，且升级至不同容量规格对 lsm2db 的容量要求也不相同。

具体说明如下：

- 若**节点数据分区容量 ≤ 50 TiB**，可直接参考本文档进行升级操作。升级后节点为小容量规格。小容量规格节点所需 lsm2db 容量为 20 GiB。系统在小容量规格节点中的资源占用情况请参考本文[附录](/smtxos/6.3.0/upgrade_guide/upgrade_guide_30)。

  > **注意**：
  >
  > 若当前集群为低于 4.0.5 版本升级而来，请在升级至本版本前，确保存储引擎已升级至 LSM2，并将 lsm2db 扩容至 20 GiB，然后执行集群升级。存储引擎的升级和扩容**请联系 SmartX 售后人员进行相关操作**。
- 若 **50 TiB ＜ 节点数据分区容量 ≤ 128 TiB**，需手动将 lsm2db 扩容至 120 GiB，根分区扩容至 185 GiB，然后执行升级操作。升级后的节点为标准容量规格。**请联系 SmartX 售后人员进行相关操作**。
- 若 **128 TiB < 节点数据分区容量 ≤ 256 TiB**，需手动将 lsm2db 扩容至 240 GiB，根分区扩容至 340 GiB，然后执行升级操作。升级后的节点为大容量规格。**请联系 SmartX 售后人员进行相关操作**。

## 确认集群是否部署了 Everoute 服务、SKS 服务或 SFS 服务

若集群中部署了 Everoute 服务、SKS 服务或 SFS 服务，可能会导致主机无法进入维护模式从而无法升级内核。具体说明和解决方法如下：

- **集群中部署了 Everoute 服务或 SKS 服务**

  若集群中 Everoute Controller 虚拟机、负载均衡虚拟机、SKS 管控集群控制面板节点虚拟机或 SKS 工作负载集群控制面板节点虚拟机的数量与集群主机数量**相同**，由于这些系统服务虚拟机设置了必须位于不同主机的虚拟机放置组，且不允许关机，因此会导致主机无法进入维护模式。

  **解决方法**：

  1. 登录 CloudTower，进入集群的**虚拟机放置组**界面，在搜索栏输入关键字 `everoute` 或 `controlplane` 定位 Everoute 相关系统服务虚拟机以及 SKS 相关系统服务虚拟机所在虚拟机放置组。
  2. 关闭上述虚拟机放置组，然后进行内核升级。
  3. 在集群中所有主机完成内核升级后，请重新启用放置组。
- **集群中部署了 SFS 服务**

  由于文件控制器虚拟机必须位于指定主机、且必须位于不同主机的放置组规则，因此也无法迁移至其他主机，导致主机无法进入维护模式。

  - **对于 SFS 1.2.0 以下版本**

    1. 登录主机的 Web 控制台，手动关闭该主机上文件控制器虚拟机的 HA 功能，并将其关机。
    2. 对该主机进行内核升级操作。
    3. 升级完成后，请手动将文件控制器虚拟机开机，并重新启用 HA 功能。
    4. 继续对集群中其他主机依次执行上述操作，直至所有主机的内核升级完毕。
    > **说明**：
    >
    > 由于关闭 2 个及以上的文件控制器可能导致文件存储服务不可用，因此需逐个对主机进行内核升级操作。
  - **对于 SFS 1.2.0 及以上版本**

    1. 进入 CloudTower，下线文件控制器：

       1. 在 CloudTower **文件存储页面**左侧的导航栏中选择**文件存储集群**，在文件存储集群列表中单击目标集群的名称，再单击**设置**页签，选择**文件控制器**。
       2. 选择一个文件控制器，单击右侧的 ...，选择**下线**。
       3. 在弹出的对话框中进行二次确认，阅读风险提示后单击**下线**。
    2. 对关闭了文件控制器的主机进行内核升级操作。
    3. 主机内核升级完毕后，重新上线该主机上的文件控制器：

       1. 在 CloudTower **文件存储页面**左侧的导航栏中选择**文件存储集群**，在文件存储集群列表中单击目标集群的名称，再单击**设置**页签，选择**文件控制器**。
       2. 选择一个文件控制器，单击右侧的 ...，选择**上线**。
    4. 继续对集群中其他主机依次执行上述操作，直至所有主机的内核升级完毕。
    > **说明**：
    >
    > 由于关闭 2 个及以上的文件控制器可能导致文件存储服务不可用，CloudTower 限制了每次只能下线一个文件控制器，因此需逐个下线文件控制器，并对文件控制器所在主机进行内核升级操作。

## 确认启用了 Boost 模式的鲲鹏 AArch64 架构集群是否存在挂载 CD-ROM 的虚拟机

对于鲲鹏 AArch64 架构集群，若集群启用了 Boost 模式，升级前需检查集群中是否存在已挂载 CD-ROM 的虚拟机。**请联系 SmartX 售后人员进行处理**。

## 确认集群内是否存在挂载了 NFS 虚拟卷的虚拟机

对于 SMTX 4.0.5 及以上版本的集群，在升级至本版本前，需检查集群中是否存在已挂载 NFS 虚拟卷的虚拟机。若存在此类虚拟机，请联系 SmartX 售后人员进行处理。

## 确认集群是否启用了动态资源调度

对于 SMTX OS（ELF）集群，在使用升级中心对集群和内核进行升级操作前，或手动升级内核前，请确保集群已关闭动态资源调度功能，避免升级过程中自动迁移虚拟机，影响升级流程。请进入集群主界面，选择动态资源调度，关闭当前集群的动态资源调度功能，升级完成后再恢复启用。

## 确认集群的 SSH 端口号是否为 22

SMTX OS 6.2.0 及以下版本集群升级时，需依赖 SSH 服务的默认 22 端口。若集群的 SSH 端口已被修改为其他端口，请在升级前将 SSH 端口号变更回 22。

## 确认集群的状态

请确认待升级的集群满足如下要求：

- 集群中没有主机处于维护模式或进入维护模式中；
- 集群中所有主机均处于健康状态；
- 集群未处于环境检查中、升级中或升级内核中状态；
- 集群中没有正在添加的主机；
- 如使用升级中心升级，集群与 CloudTower 的连接状态需为`已连接`。

---

## 升级集群 > 通过升级中心升级

# 通过升级中心升级

通过升级中心升级集群的操作方法请参考[《升级中心使用指南》](/cluster-upgrade/1.1.2/cluster_upgrade_user_guide/cluster_upgrade_user_guide_01)。

---

## 升级集群 > 通过命令行升级

# 通过命令行升级

**前提条件**

- 已下载适配服务器类型的 SMTX OS 升级 ISO 文件，以及对应的元数据 JSON 文件。
- 拥有超级管理员 root 的操作权限。该权限说明可参见 [SMTX OS 节点的本地账户](/smtxos/6.3.0/upgrade_guide/elf_installation_guide/elf_installation_guide_49)。

**注意事项**

- 在集群升级过程中，系统会暂停 `elf-vm-monitor 和 elf-vm-watchdog` 服务，同时触发监控报警系统对此服务的报警。用户可以忽略该告警，待升级结束后，系统将自动恢复 `elf-vm-monitor 和 elf-vm-watchdog` 服务的运行。
- 如果升级过程中断，`elf-vm-monitor 和 elf-vm-watchdog` 服务将处于停止运行的状态。在查明升级中断的原因前，请勿启动任何节点的 `elf-vm-monitor` 服务。重新执行升级命令并顺利完成升级后，系统将自动恢复 `elf-vm-monitor 和 elf-vm-watchdog` 服务的运行。

**操作步骤**

您只需在集群的某个节点执行命令行操作，即可完成整个集群的升级。

1. 使用 root 账号登录所使用虚拟化平台对应的节点系统，利用工具将目标版本的 SMTX OS 升级 ISO 文件及对应的元数据 JSON 文件上传至集群的某个节点。

   - 若使用 ELF 平台，请用 root 账号登录服务器节点的 SMTX OS 系统。
   - 若使用 VMware ESXi 平台，请用 root 账号登录 ESXi 节点的 SCVM。

   举例：集群某个节点的管理 IP 地址为 `192.168.75.101`，升级前可借助 Xshell 工具（或其他同类工具）将目标版本的升级 ISO 文件和对应的元数据 JSON 文件上传至 `192.168.75.101` 节点的根目录下。
2. 输入以下命令，挂载映像文件，并配置 yum 源为 `smartxos.repo`。

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
4. 进入 `/usr/share/upgrade/runner/` 目录下，执行以下脚本。其中 `<iso path>` 表示升级的目标版本的 ISO 映像文件的绝对路径，`<metadata path>` 表示升级的目标版本的 ISO 元数据文件的绝对路径。

   `nohup python cluster_upgrader.py --iso_path <iso path> --metadata_path <metadata path> &`
5. 在脚本执行过程中，输入命令 `tail -f nohup.out` 实时查看更新日志。

   - 若集群升级成功，则日志中将输出 `Cluster upgrade successful`。
   - 若集群升级失败，则请先根据相关日志定位出失败原因并解决问题，然后再重新升级，将会从上次升级失败后继续进行后续升级。

> **说明**：
>
> - SMTX OS（VMware ESXi）集群升级时不会⾃动切换 I/O 路由。
> - 当在日志中出现提示信息如“存在正在进行的准备升级工具进程，无法进行集群升级”或“存在其他正在进行的集群升级进程”时：
>   - 若该现象是由其他人在同时升级所导致，则不需要再重新升级。
>   - 若该现象不是由其他人在同时升级所导致，则请在所使用虚拟化平台对应的节点系统中执行`cluster-upgrade clear_upgrade_event` 命令清理升级失败的信息，最后再重新升级。
> - 若升级失败，在修复相关问题后可继续升级。系统将自动跳过已执行的步骤，并从上次失败的步骤继续执行。

---

## 升级集群 > 通过 Web 控制台升级

# 通过 Web 控制台升级

**前提条件**

已下载适配服务器类型的升级 ISO 文件以及对应的元数据 JSON 文件。

**操作步骤**

1. 登录 Web 控制台，进入集群的**设置**界面。在**升级集群**区域，单击**管理**按钮展开升级入口。
2. 单击**上传升级文件**，在弹出的**上传升级文件**对话框中，单击**选择文件**，添加升级 ISO 文件和元数据 JSON 文件。也可以手动将升级 ISO 文件和元数据 JSON 文件拖入区域框中。完成添加后系统开始检查文件的合法性。

   若节点上已有其他版本的升级文件，则可以先单击**上传新升级文件**按钮，再开始上传目标版本的升级 ISO 文件和元数据 JSON 文件。
3. 单击**上传**，系统开始上传升级文件。

   升级文件上传成功后，**可用升级**区域框中的目标升级版本后将显示**准备升级工具**按钮。
4. 单击**准备升级工具**，待升级工具准备结束后，目标升级版本将对应显示**升级集群**按钮。

   若升级工具准备失败，系统将提示具体的出错原因。在解决完所有问题后，可再次尝试准备升级工具。
5. 单击**升级集群**，系统开始升级前的预检查。
6. 单击**升级**，进行集群升级。待集群上所有节点完成升级后，系统将提示集群已成功升级至目标版本。

   升级过程中，单击**升级控制节点**后的**查看日志**可以查看集群升级实时日志信息。

   **升级控制节点**表示当前升级过程的控制节点，当升级失败可访问升级控制节点的 `/var/log/zbs/cluster_upgrade.log` 文件，通过查看其升级日志进行排查。

> **说明**：
>
> - 若升级失败，在修复相关问题后可继续升级。系统将自动跳过已执行的步骤，并从上次失败的步骤继续执行。
> - SMTX OS（VMware ESXi）集群升级时不会⾃动切换 I/O 路由。

---

## 手动升级内核

# 手动升级内核

若升级目标版本所对应的内核版本与升级前的内核版本不一致，请根据[内核更新记录](/smtxos/6.3.0/upgrade_guide/upgrade_guide_18)，按需升级内核。

本章节介绍了如何使用命令行手动升级内核。若您的集群版本支持使用升级中心进行升级，请参考[《升级中心使用指南》](/cluster-upgrade/1.1.2/cluster_upgrade_user_guide/cluster_upgrade_user_guide_01)完成对内核的自动升级。

**升级说明**

- 当 SMTX OS 部署在不同的服务器平台时，与其配套使用的内核版本均不同，但手动升级内核版本的操作步骤基本相同。
- 对于部署在 ELF 平台的 SMTX OS 集群，若节点已安装了 vGPU 驱动，在升级内核后，需要将驱动更新至新内核的对应版本。

**前提条件**

集群已完成了升级。

**注意事项**

- 对于 SMTX OS（ELF）集群，在升级内核前，请确保集群已关闭动态资源调度功能，避免升级过程中自动迁移虚拟机，影响升级流程。请进入集群主界面，选择**动态资源调度**，关闭当前集群的动态资源调度功能，升级完成后再恢复启用。
- 升级结束后，需要重启物理机使升级生效，系统将会出现短暂的 I/O 中断，但不影响业务的正常运行。

---

## 手动升级内核 > 内核更新记录

# 内核更新记录

下表列出了 SMTX OS 版本与内核版本的配套关系及更新记录。

当 SMTX OS 部署在不同架构的服务器时，与其配套使用的内核版本均不同，请参照部署的服务器类型，查看对应的内核版本更新记录。

SMTX OS 全新安装时默认使用对应的内核版本，但 SMTX OS 升级时默认不自动升级内核，需要手动更新。

## Intel x86\_64、AMD x86\_64 或兆芯 x86 架构

| SMTX OS 版本 | 内核版本 | 更新原因 |
| --- | --- | --- |
| 4.0.5 ~ 4.0.8 | kernel-3.10.0-1062.1.2.el7​.smartx.1.x86\_64.rpm | 修复 vhost 漏洞 |
| 4.0.9 ～ 4.0.12 | kernel-3.10.0-1160.11.1.el7​.smartx.1.x86\_64.rpm | 修复因服务出现 OOM (out of memory) 导致内核进程锁死的问题 |
| 4.0.13 | kernel-3.10.0-1160.11.1.el7​​.smartx.3.x86\_64.rpm | 修复虚拟机不定时重启的问题 |
| 4.0.14 | kernel-3.10.0-1160.11.1.el7​​.smartx.7.x86\_64.rpm | 增加对网讯千兆网卡驱动 ngbe 的支持，升级 MegaRAID 驱动和 Mpt3sas 驱动 |
| 5.0.0 ~ 5.0.3 | kernel-4.18.0-193.28.1.el7​.smartx.3.x86\_64.rpm | 修复了因服务出现 OOM (out of memory) 导致内核进程锁死的问题 |
| 5.0.4 | kernel-4.18.0-193.28.1.el7​.smartx.10.x86\_64.rpm | - 修复安全漏洞 CVE-2022-2639 - 升级 MegaRAID 驱动至 07.721.02.00 以修复 MegaRAID SAS 9361 等存储控制器可能无法正常处理 I/O 的问题 - 更新 mpt3sas 驱动版本至 37.00.02.00 以修复 SMTX OS 无法识别硬盘的问题（配置了 SAS HBA 355i 存储控制器的戴尔服务器） |
| 5.0.5 | kernel-4.18.0-193.28.1.el7​.smartx.11.x86\_64.rpm | - 更新 i40e 驱动至 2.20.12 版本，以解决该驱动无法被正常识别的问题 - 解决 i40e 驱动与 mlnx 驱动同时加载时互相冲突的问题 |
| 5.0.6、5.1.0、5.1.1 | 基于 openEuler：kernel-4.19.90-2112.8.0.0131.​oe1.smartx.17.x86\_64.rpm | - 解决使用低版本固件时，x710 网卡无法正常工作的问题 - 加固内核，防止 USB 设备异常导致的机器宕机的问题 - 升级 kvm\_stat 工具 |
| 基于 CentOS：kernel-4.18.0-193.28.1.el7​.smartx.14.x86\_64.rpm | - 解决客户使用低版本固件时，x710 网卡无法正常工作的问题 - 解决开启 Intel VMD 后，机器无法正常工作的问题 - 加固内核，防止 USB 设备异常导致的机器宕机的问题 - 升级 kvm\_stat 工具 |
| 5.1.2 | 基于 openEuler：kernel-4.19.90-2112.8.0.0131.​oe1.smartx.19.x86\_64.rpm | - 解决 PM8222 等 RAID 卡在 mq-deadline 调度器中的性能退化问题。 - 修复 zero page refcount 溢出导致虚拟机异常的问题。 |
| 基于 CentOS：kernel-4.18.0-193.28.1.el7​.smartx.18.x86\_64.rpm | - 解决 PM8222 等 RAID 卡在 mq-deadline 调度器中的性能退化问题 - 解决 HPE 380 机型带外无法输入字符问题 - 修复 zero page refcount 溢出导致虚拟机异常的问题 |
| 5.1.3 | 基于 openEuler：kernel-4.19.90-2112.8.0.0131.​oe1.smartx.28.x86\_64.rpm | 本次更新适用于 ELF 平台和 VMware ESXi 平台：  - 解决 tun 驱动持续收到大量异常包时，触发 soft lockup 的问题 - 解决 mpt3sas 驱动在磁盘异常情况下可能导致系统卡死的问题 - 解决 OVS 内存泄漏问题 - 解决 USB 设备异常导致机器卡死问题 - 修复安全漏洞 [CVE-2023-6931](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-6931) |
| 基于 CentOS：kernel-4.18.0-193.28.1.el7​.smartx.25.x86\_64.rpm | 本次更新适用于 ELF 平台和 VMware ESXi 平台：  - 解决 tun 驱动持续收到大量异常包时，触发 soft lockup 的问题 - 解决 mpt3sas 驱动在磁盘异常情况下可能导致系统卡死的问题 - 解决 OVS 内存泄漏问题 - 解决 USB 设备异常导致机器卡死问题 - 修复安全漏洞 [CVE-2023-6931](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-6931) |
| 5.1.4 | 基于 openEuler：kernel-4.19.90-2112.8.0.0131.​oe1.smartx.68.x86\_64.rpm | 本次更新适用于 ELF 平台和 VMware ESXi 平台：  - 支持 Nvidia A30 和 A6000 GPU 驱动 - 优化 TCP 包在 conntrack 中是否无效的判定 - 修复 ufo 报文分段处理异常的问题（oracle 11g 部署问题） - 修复 Open vSwitch 模块偶发性的 softlock 问题 - 修复网络 bug 导致虚拟机接收到元数据被破坏的网络包的问题 - 修复 Intel ice 驱动无法自动加载的问题 - 修复 tcp backlog limit 溢出问题 - 修复安全漏洞 [CVE-2022-0847](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-0847) - 修复安全漏洞 [CVE-2024-1086](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-1086) - 修复安全漏洞 [CVE-2022-2586](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2586) |
| 基于 CentOS：kernel-4.18.0-193.28.1.el7​.​smartx.34.x86\_64.rpm | 本次更新适用于 ELF 平台和 VMware ESXi 平台：  - 优化 TCP 包在 conntrack 中是否无效的判定 - 修复 Open vSwitch 模块偶发性的 softlock 问题 - 修复 tcp backlog limit 溢出问题 - 修复网络 bug 导致虚拟机接收到元数据被破坏的网络包的问题 - 修复 Intel ice 驱动无法自动加载的问题 - 修复安全漏洞 [CVE-2022-0847](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-0847) - 修复安全漏洞 [CVE-2024-1086](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-1086) - 修复安全漏洞 [CVE-2022-2586](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2586) |
| 5.1.5 | 基于 openEuler：kernel-4.19.90-2307.3.0.​oe1.v115.x86\_64.rpm | 本次更新将内核版本升级至4.19.90-2307.3.0.oe1.v115 版本，适用于 ELF 平台和 VMware ESXi 平台。主要更新如下：  - 新增对 SSSRAID 控制卡的支持 - 新增对网迅 txgbe 系列万兆网卡的支持 - 提升 Open vSwitch 性能 - 修复 Guest OS 内主动触发 SMI 中断导致虚拟机宕机的问题 - 修复因打印内核调度器日志导致节点无响应的问题 - 修复 nouveau 驱动引发节点宕机的问题 - 修复 vCPU 热添加场景中 Guest OS 时钟同步异常的问题 |
| 基于 CentOS：kernel-4.18.0-193.28.1.el7​.​​smartx.54.x86\_64.rpm | 本次更新适用于 ELF 平台和 VMware ESXi 平台：  - 新增对网迅 txgbe 系列万兆网卡的支持 - 新增 mpi3mr 驱动，支持 H965 系列 RAID 卡 - sysfs 接口新增支持 SCSI IO timeout 指标 - 修复仅支持 32bit MSI 的 PCIe 设备无法工作的问题 - 修复 Guest OS 主动触发 SMI 中断导致拟机宕机的问题 - 修复 nouveau 驱动引发节点宕机的问题 - 修复因打印内核调度器日志导致节点无响应的问题 |
| 基于 TencentOS：kernel-5.4.119-19.0009.54.tl3.​v89.x86\_64.rpm | - |
| 6.0.0 | - 基于 openEuler：kernel-4.19.90-2307.3.0.oe1​.smartx.33.x86\_64.rpm - 基于 CentOS：kernel-4.19.90-2307.3.0.el7​.smartx.33.x86\_64.rpm | - 解决 KVM 模块引用计数溢出的问题 - 支持 Nvidia A30 和 A6000 GPU 驱动 - 增加 Intel(R) C600 Series Chipset SAS Controller 的驱动 - 修复部分 USB 设备可能导致内核死锁的问题 - 增加 SCSI 模块超时 IO 数量统计 - 解决浪潮 PM8222 HBA 卡性能不足的问题 |
| 6.1.0 ~ 6.1.1 | - 基于 openEuler：kernel-4.19.90-2307.3.0.oe1​.smartx.59.x86\_64.rpm - 基于 CentOS：kernel-4.19.90-2307.3.0.el7​.smartx.59.x86\_64.rpm | - sysfs 暴露 scsi io timeout 指标 - 限制 tun 设备打印异常包的速率 - 解决 ovs nested actions 导致的内存泄漏问题 - 解决中断重入的误判打印 - 新增 mpi3mr 驱动，支持 H965 系列 RAID 卡 - 优化 TCP 包在 conntrack 中是否无效的判定 - 解决网络 bug 导致的虚拟机接受到元数据被破坏的网络包 - 修复 nf 模块的安全漏洞 CVE-2024-1086 - 优化 overlay 网络中的 UDP 性能 - 支持 conntrack 过滤器 |
| 6.2.0 | - 基于 openEuler：kernel-4.19.90-2307.3.0.​oe1​.v97.x86\_64.rpm - 基于 CentOS：kernel-4.19.90-2307.3.0.​el7​.v97.x86\_64.rpm | - 支持 SSSRAID 控制卡 - 支持网迅万兆网卡（txgbe 系列） - 虚拟机 CPU 兼容性支持 Ice Lake CPU model - 修复 QLogic 网卡开 PTP 特性时，CPU 使用率突增的问题 - 修复 vCPU 热添加场景中，Guest OS 时钟同步异常的问题 - 修复安全漏洞 CVE-2019-3016 - 修复仅支持 32bit MSI 的 PCIe 设备无法工作的问题 - 修复数据不一致导致的块层 I/O 卡死问题 - 修复 ext4 文件系统在线重置容量可能导致数据被破坏的问题 - 修复内存子系统可能被破坏的问题 - 修复 buffer I/O 数据可能不一致的问题 - 修复 KVM 异步缺页异常导致卡死的问题 - 修复内存申请路径可能卡死的问题 - 修复 Windows 虚拟机直通 NVIDIA A 系列显卡导致主机宕机并重启的问题 |
| 6.3.0 | - 基于 openEuler：kernel-5.10.0-247.0.0.oe1​.v79.x86\_64.rpm - 基于 CentOS：kernel-5.10.0-247.0.0.el7​.v79.x86\_64.rpm | - 内核版本升级至 5.10.0-247.0.0 - 支持 io\_uring - linkdata raid 卡驱动版本升级至 2.6.0.23 - mpt3sas 驱动版本升级至 55.00.00.00 - i40e 驱动版本升级至 2.20.12 - megaraid 驱动版本升级至 07.735.03.00-2 - 修复了 io\_uring 中重新提交 I/O 时，I/O 丢失的问题 |
| 基于 TencentOS：kernel-5.4.119-19.0009.54.tl3​.v98.x86\_64.rpm | - |

## Hygon x86\_64 架构

| **SMTX OS 版本** | **内核版本** | **更新原因** |
| --- | --- | --- |
| 5.0.3 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.6.x86\_64.rpm | - |
| 5.0.4 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.11.x86\_64.rpm | - 修复安全漏洞 CVE-2022-2639 - 升级 MegaRAID 驱动至 07.721.02.00 以修复 MegaRAID SAS 9361 等存储控制器可能无法正常处理 I/O 的问题 - 更新 mpt3sas 驱动版本至 37.00.02.00 以修复 SMTX OS 无法识别硬盘的问题（配置了 SAS HBA 355i 存储控制器的戴尔服务器） |
| 5.0.5 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.12.x86\_64.rpm | - 更新 i40e 驱动至 2.20.12 版本，以解决该驱动无法被正常识别的问题 - 解决 i40e 驱动与 mlnx 驱动同时加载时互相冲突的问题 |
| 5.0.6、5.1.0、5.1.1 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.17.x86\_64.rpm | - 解决客户使用低版本固件时，x710 网卡无法正常工作的问题 - 加固内核，防止 USB 设备异常导致的机器宕机的问题 - 升级 kvm\_stat 工具 |
| 5.1.2 | kernel-4.19.90-2112.8.0.0131.​oe1.smartx.19.x86\_64.rpm | - 解决 PM8222 等 RAID 卡在 mq-deadline 调度器中的性能退化问题 - 修复 zero page refcount 溢出导致虚拟机异常的问题 |
| 5.1.3 | kernel-4.19.90-2112.8.0.0131.​oe1.smartx.28.x86\_64.rpm | 本次更新适用于 ELF 平台和 VMware ESXi 平台：  - 解决 tun 驱动持续收到大量异常包时，触发 soft lockup 的问题 - 解决 mpt3sas 驱动在磁盘异常情况下可能导致系统卡死的问题 - 解决 Hygon/AMD 平台触发 I/O \_PAGE\_FAULT 问题，导致设备异常的问题 - 解决 OVS 内存泄漏问题 - 解决 USB 设备异常导致机器卡死问题 - 修复安全漏洞 [CVE-2023-6931](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-6931) |
| 5.1.4 | kernel-4.19.90-2112.8.0.0131.​oe1.smartx.68.x86\_64.rpm | 本次更新适用于 ELF 平台和 VMware ESXi 平台：  - 支持海光 4 代 CPU - 支持 Nvidia A30 和 A6000 GPU 驱动 - 优化 TCP 包在 conntrack 中是否无效的判定 - 修复 PCIe 设备直通时 IOMMU 异常的问题 - 修复 ufo 报文分段处理异常的问题（oracle 11g 部署问题） - 修复 Open vSwitch 模块偶发性的 softlock 问题 - 修复网络 bug 导致的虚拟机接收元数据被破坏的网络包的问题 - 修复 Intel ice 驱动无法自动加载的问题 - 修复 tcp backlog limit 溢出问题 - 修复安全漏洞 [CVE-2022-0847](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-0847) - 修复安全漏洞 [CVE-2024-1086](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-1086) - 修复安全漏洞 [CVE-2022-2586](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2586) |
| 5.1.5 | 基于 openEuler：kernel-4.19.90-2307.3.0.​oe1.v115.x86\_64.rpm | 本次更新将内核版本升级至4.19.90-2307.3.0.oe1.v115 版本，适用于 ELF 平台和 VMware ESXi 平台。主要更新如下：  - 新增对 SSSRAID 控制卡的支持 - 新增对网迅 txgbe 系列万兆网卡的支持 - 提升 Open vSwitch 性能 - 修复 Guest OS 内主动触发 SMI 中断导致虚拟机宕机的问题 - 修复因打印内核调度器日志导致节点无响应的问题 - 修复 nouveau 驱动引发节点宕机的问题 - 修复 vCPU 热添加场景中 Guest OS 时钟同步异常的问题 - 修复因无法使能 PSP 设备导致的宕机问题 |
| 基于 TencentOS：kernel-5.4.119-19.0009.54.tl3.​v89.x86\_64.rpm | - |
| 6.0.0 | kernel-4.19.90-2307.3.0​.oe1.smartx.33.x86\_64.rpm | - 解决 KVM 模块引用计数溢出的问题 - 支持 Nvidia A30 和 A6000 GPU 驱动 - 增加 Intel(R) C600 Series Chipset SAS Controller 的驱动 - 修复部分 USB 设备可能导致内核死锁的问题 - 增加 SCSI 模块超时 IO 数量统计 - 解决在浪潮 PM8222 HBA 卡性能不足的问题 |
| 6.1.0 ~ 6.1.1 | kernel-4.19.90-2307.3.0​.oe1.smartx.56.x86\_64.rpm | - sysfs 暴露 scsi io timeout 指标 - 限制 tun 设备打印异常包的速率 - 解决 ovs nested actions 导致的内存泄漏问题 - 解决中断重入的误判打印 - 新增 mpi3mr 驱动，支持 H965 系列 RAID 卡 - 优化 TCP 包在 conntrack 中是否无效的判定 - 解决网络 bug 导致的虚拟机接受到元数据被破坏的网络包 - 修复 nf 模块的安全漏洞 CVE-2024-1086 - 新增海光 4 PMU 等模块支持 - 优化 overlay 网络中的 UDP 性能 - 支持 conntrack 过滤器 - 解决 PCIE 设备直通时 iommu 异常 |
| 6.2.0 | kernel-4.19.90-2307.3.0.​oe1.v97.x86\_64.rpm | - 支持 Hygon HCT 加密设备 - 支持 SSSRAID 控制卡 - 支持网迅万兆网卡（txgbe 系列） - 修复 QLogic 网卡开启 PTP 特性时，CPU 使用率突增的问题 - 修复 vCPU 热添加场景中，Guest OS 时钟同步异常的问题 - 修复安全漏洞 CVE-2019-3016 - 修复仅支持 32bit MSI 的 PCIe 设备无法工作的问题 - 修复 Hygon CPU 缺陷 errata 1096 - 修复数据不一致导致的块层 I/O 卡死问题 - 修复 ext4 文件系统在线重置容量可能导致数据被破坏的问题 - 修复内存子系统可能被破坏的问题 - 修复 buffer I/O 数据可能不一致的问题 - 修复 KVM 异步缺页异常导致卡死的问题 - 修复内存申请路径可能卡死的问题 - 修复 Windows 虚拟机直通 NVIDIA A 系列显卡导致主机宕机并重启的问题 |
| 6.3.0 | 基于 openEuler：kernel-5.10.0-247.0.0.oe1​.v79.x86\_64.rpm | - 内核版本升级至 5.10.0-247.0.0 - 支持 io\_uring - linkdata raid 卡驱动版本升级至 2.6.0.23 - mpt3sas 驱动版本升级至 55.00.00.00 - i40e 驱动版本升级至 2.20.12 - megaraid 驱动版本升级至 07.735.03.00 - 修复了 io\_uring 中重新提交 I/O 时，I/O 丢失的问题 |
| 基于 TencentOS：kernel-5.4.119-19.0009.54.tl3​.v98.x86\_64.rpm | - |

## 鲲鹏 AArch64/飞腾 AArch64 架构

| **SMTX OS 版本** | **内核版本** | **更新原因** |
| --- | --- | --- |
| 5.0.3 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.6.aarch64.rpm | - |
| 5.0.4 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.11.aarch64.rpm | - 修复安全漏洞 CVE-2022-2639 - 升级 MegaRAID 驱动至 07.721.02.00 以修复 MegaRAID SAS 9361 等存储控制器可能无法正常处理 I/O 的问题 - 更新 mpt3sas 驱动版本至 37.00.02.00 以修复 SMTX OS 无法识别硬盘的问题（配置了 SAS HBA 355i 存储控制器的戴尔服务器） |
| 5.0.5 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.13.aarch64.rpm | - 更新 i40e 驱动至 2.20.12 版本，以解决该驱动无法被正常识别的问题 - 解决 i40e 驱动与 mlnx 驱动同时加载时互相冲突的问题 - 修复了虚拟机从 CentOS 主机热迁移到 openEuler 主机时失败的问题 |
| 5.0.6、5.1.0、5.1.1 | kernel-4.19.90-2112.8.0.0131​.oe1.smartx.17.aarch64.rpm | - 解决客户使用低版本固件时， x710 网卡无法正常工作的问题 - 加固内核，防止 USB 设备异常导致的机器宕机的问题 - 升级 kvm\_stat 工具 - 解决虚拟机无法从 CentOS 主机热迁移到 openEuler 主机的问题 |
| 5.1.2 | kernel-4.19.90-2112.8.0.0131.​oe1.smartx.19.aarch64.rpm | - 解决 PM8222 等 RAID 卡在 mq-deadline 调度器中的性能退化问题 - 修复 zero page refcount 溢出导致虚拟机异常的问题 |
| 5.1.3 | kernel-4.19.90-2112.8.0.0131.​oe1.smartx.28.aarch64.rpm | 本次更新适用于 ELF 平台：  - 解决 tun 驱动持续收到大量异常包时，触发 soft lockup 的问题 - 解决 mpt3sas 驱动在磁盘异常情况下可能导致系统卡死的问题 - 解决 OVS 内存泄漏问题 - 解决 USB 设备异常导致机器卡死问题 - 修复安全漏洞 [CVE-2023-6931](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-6931) - 解决中断迁移导致的潜在的中断丢失的问题 |
| 5.1.4 | kernel-4.19.90-2112.8.0.0131.​oe1.smartx.68.aarch64.rpm | 本次更新适用于 ELF 平台：  - 支持 Nvidia A30 和 A6000 GPU 驱动 - 优化 TCP 包在 conntrack 中是否无效的判定 - 修复 ufo 报文分段处理异常的问题（oracle 11g 部署问题） - 修复 Open vSwitch 模块偶发性的 softlock 问题 - 修复网络 bug 导致虚拟机接收到元数据被破坏的网络包的问题 - 修复 Intel ice 驱动无法自动加载的问题 - 修复 tcp backlog limit 溢出问题 - 修复安全漏洞 [CVE-2024-1086](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-1086) - 修复安全漏洞 [CVE-2022-2586](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2586) |
| 5.1.5 | 基于 openEuler：kernel-4.19.90-2307.3.0.​oe1.v115.aarch64.rpm | 本次更新将内核版本升级至4.19.90-2307.3.0.oe1.v115 版本，适用于 ELF 平台和 VMware ESXi 平台。主要更新如下：  - 新增对网迅 txgbe 系列万兆网卡的支持 - 新增对海思 SP680 系列网卡的支持 - sysfs 接口新增支持 SCSI IO timeout 指标 - 支持在集群中使用虚拟 PTP 硬件时钟（PTP Hardware Clock）以确保虚拟机和其所在主机时间同步 - 提升 Open vSwitch 性能 - 修复仅支持 32bit MSI 的 PCIe 设备无法工作的问题 - 修复因打印内核调度器日志导致节点无响应的问题 - 修复了Boost 模式下虚拟机缺页异常处理中的 bug，解决由此引发的主机宕机问题 |
| 基于 TencentOS：kernel-5.4.119-19.0009.54.tl3.​v89.x86\_64.rpm | - |
| 6.0.0 | kernel-4.19.90-2307.3.0.​oe1.smartx.33.aarch64.rpm | - 解决 KVM 模块引用计数溢出的问题 - 支持 Nvidia A30 和 A6000 GPU 驱动 - 增加 Intel(R) C600 Series Chipset SAS Controller 的驱动 - 修复部分 USB 设备可能导致内核死锁的问题 - 增加 SCSI 模块超时 IO 数量统计 - 解决在浪潮 PM8222 HBA 卡性能不足的问题 |
| 6.1.0 ~ 6.1.1 | kernel-4.19.90-2307.3.0.​oe1.smartx.59.aarch64.rpm | - sysfs 暴露 scsi io timeout 指标 - 限制 tun 设备打印异常包的速率 - 解决 ovs nested actions 导致的内存泄漏问题 - 解决中断重入的误判打印 - 新增 mpi3mr 驱动，支持 H965 系列 RAID 卡 - 优化 TCP 包在 conntrack 中是否无效的判定 - 解决网络 bug 导致的虚拟机接受到元数据被破坏的网络包 - 修复 nf 模块的安全漏洞 CVE-2024-1086 - 优化 overlay 网络中的 UDP 性能 - 支持 conntrack 过滤器 |
| 6.2.0 | kernel-4.19.90-2307.3.0.​oe1.v97.aarch64.rpm | - 支持飞腾 S5000C 系列 CPU - 支持 SSSRAID 控制卡 - 支持网迅万兆网卡（txgbe 系列） - 支持在集群中使用虚拟 PTP 硬件时钟（PTP Hardware Clock）以确保虚拟机和其主机时间同步 - 修复 QLogic 网卡开启 PTP 特性时，CPU 使用率突增的问题 - 修复安全漏洞 CVE-2019-3016 - 修复仅支持 32bit MSI 的 PCIe 设备无法工作的问题 - 修复数据不一致导致的块层 I/O 卡死问题 - 修复 ext4 文件系统在线重置容量可能导致数据被破坏的问题 - 修复内存子系统可能被破坏的问题 - 修复 buffer I/O 数据可能不一致的问题 - 修复 KVM 异步缺页异常导致卡死的问题 - 修复内存申请路径可能卡死的问题 - 修复了 Boost 模式下虚拟机缺页异常处理中的 bug，解决由此引发的主机宕机问题 |
| 6.3.0 | 基于 openEuler：kernel-5.10.0-247.0.0.oe1.v79.aarch64.rpm | - 内核版本升级至 5.10.0-247.0.0 - 支持海思 SP680 系列网卡 - 支持 io\_uring - linkdata raid 卡驱动版本升级至 2.6.0.23 - mpt3sas 驱动版本升级至 55.00.00.00 - megaraid 驱动版本升级至 07.735.03.00 - 修复了 io\_uring 中重新提交 I/O 时，I/O 丢失的问题 |
| 基于 TencentOS：kernel-5.4.119-19.0009.54.tl3​.v98.aarch64.rpm | - |

---

## 手动升级内核 > 执行升级

# 执行升级

**前提条件**

- 检查集群资源，确保集群的计算资源和存储资源均满足集群中单节点故障场景。
- 执行命令 `uname -a` ，查看并记录升级前的内核版本。
- 集群已完成升级，否则将导致内核与 SMTX OS 内部服务不兼容。
- 对照《SMTX OS 运维指南》中的[进入维护模式的要求](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)完成自检，确认所有检查项目满足要求。
- 若待升级主机上存在安装了 vGPU 的虚拟机，则需要将这些虚拟机关机。

## 第 1 步：上传升级 ISO 文件至 Meta Leader 节点

1. 执行命令 `zbs-tool service list`，查询集群 Meta Leader 节点。
2. 上传本版本升级 ISO 文件到 Meta Leader 节点，并在该节点执行以下命令，以准备升级内核所需的 repo，然后记录此节点的存储 IP。其中，`<iso_path>` 表示 ISO 文件在该节点的绝对路径。

   `cluster-upgrade prepare_repo <iso_path>`

   执行完成后，如果输出信息显示 `prepare repo success`，表明 repo 已准备完成。

## 第 2 步：升级非 Meta Leader 节点的内核

1. 登录 CloudTower，在集群的主机列表中选中此节点所在的主机，单击右侧的 **...** 后选择**进入维护模式**。
2. 执行下述命令用于准备 repo。其中 `<repo_ip>` 为 Meta Leader 节点的存储 IP。

   `cluster-upgrade config_repo --repo_ip <repo_ip>`

   执行完成后，若输出信息显示 `config repo success.`，表明当前节点升级内核所需要的 repo 已配置完成。
3. 执行以下命令进行内核升级。当显示 `Upgrade done` 字样时，表明升级成功。

   `skc upgrade`
4. 登录 CloudTower，在集群的主机列表中选中目标主机，单击右侧的 **...** 后选择**重启**，输入重启原因后重启主机。
5. 执行 `uname -a` 命令，查看内核是否已成功升级到目标版本。若升级不符合预期，可参考[回滚内核版本](/smtxos/6.3.0/upgrade_guide/upgrade_guide_26#%E5%9B%9E%E6%BB%9A-kernel-%E7%89%88%E6%9C%AC)一节对内核进行回滚。
6. 在 CloudTower 的主机概览页面查看当前主机已处于维护模式的时间，单击提示内容右侧的**退出维护模式**。
7. 系统弹出检查对话框进行退出检查，检查结束后返回所有检查项目的检查结果。

   - 所有检查项目全部满足要求，允许主机退出维护模式。单击**退出维护模式**。
   - 部分检查结果不满足要求，请对照《SMTX OS 运维指南》中的[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)的要求进行调整，然后再次尝试退出维护模式。
8. 切换至其他非 Meta Leader 节点，执行如上步骤，直至所有非 Meta Leader 节点完成升级。

## 第 3 步：升级 Meta Leader 节点的内核

1. 执行 `zbs-tool service list` 命令，确认 Meta Leader 是否已切换至其他节点。若没有切换，则执行 `systemctl stop zbs-metad` 命令，触发 Meta Leader 切换。
2. 执行 `zbs-meta chunk list` 命令，确认当前集群各个 Chunk 状态均为 `CONNECTED_HEALTHY`。
3. 登录 CloudTower，在集群的主机列表中选中此节点所在的主机，单击右侧的 **...** 后选择**进入维护模式**。
4. 执行下述命令用于准备升级内核所需的 repo。其中，`<repo_ip>` 为节点自身的存储 IP。

   `cluster-upgrade config_repo --repo_ip <repo_ip>`

   执行命令后，若输出 `config repo success.`，表明所需的 repo 已配置完成。
5. 执行以下命令升级内核。当显示 `Upgrade done` 字样时，表明升级成功。

   `skc upgrade`
6. 登录 CloudTower，在集群的主机列表中选中目标主机，单击右侧的 **...** 后选择**重启**，输入重启原因后重启主机。
7. 执行 `uname -a` 命令，查看内核是否已成功升级到目标版本。若升级不符合预期，可参考[回滚内核版本](/smtxos/6.3.0/upgrade_guide/upgrade_guide_26#%E5%9B%9E%E6%BB%9A-kernel-%E7%89%88%E6%9C%AC)一节对内核进行回滚。
8. 在 CloudTower 的主机概览页面查看当前主机已处于维护模式的时间，单击提示内容右侧的**退出维护模式**。
9. 系统弹出检查对话框进行退出检查，检查结束后返回所有检查项目的检查结果。

   - 所有检查项目全部满足要求，允许主机退出维护模式。单击**退出维护模式**。
   - 部分检查结果不满足要求，请对照《SMTX OS 运维指南》中的[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)的要求进行调整，然后再次尝试退出维护模式。
10. 在所有节点完成升级后，通过 CloudTower 确认集群状态正常。

## 第 4 步：清理 boot 分区残留的内核包

由于 `/boot` 分区存储空间有限，在多次升级内核后，`/boot` 分区存储空间可能会被占满。可执行 `skc clean` 命令，清理掉没有运行的驱动和内核包。

---

## 手动升级内核 > 回滚内核版本

# 回滚内核版本

若升级内核失败或升级的版本不及预期，可参考如下步骤回滚内核。

**操作步骤**

1. 执行以下命令，选择要回滚到的内核版本。主机重启后将默认启动该内核。

   `skc boot`

   > **注意**：
   >
   > 对于 5.0.5 及以下版本，且 BIOS 模式为 `legacy bios` 的 SMTX OS 集群，在升级到本版本后，使用该命令无法设置默认启动的内核。在此情况下，请在下次重启时在 grub 界面手动选择默认启动项。
2. 登录 CloudTower，在集群的主机列表中选中此节点所在的主机，单击右侧的 **...** 后选择**进入维护模式**。
3. 当主机处于维护模式后，在集群的主机列表中选中目标主机，单击右侧的 **...** 后选择**重启**，输入重启原因后重启主机。
4. 执行 `uname -a` 命令，确认当前内核是否已经成功回滚为目标版本。

---

## 手动升级内核 > 升级 vGPU 驱动

# 升级 vGPU 驱动

当前用户所使用的 vGPU 版本无法支持用户所需特性或应用时，或集群升级了内核版本时，需要升级主机上的 vGPU 驱动。

**准备工作**

- 执行命令 `uname -a` ，查看该主机当前的内核版本。根据内核版本和所需的 vGPU 驱动版本，获取驱动安装包。

  > **说明**：
  >
  > 使用 NVIDIA L20 时请选择开放驱动。
- 待升级驱动所在主机上挂载了 vGPU 的虚拟机均处于关机状态。

**操作步骤**

1. 登录 CloudTower，设置主机[进入维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
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
9. 在 CloudTower 中将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。

---

## 升级后配置

# 升级后配置

SMTX OS 升级至目标版本后，可能因历史版本的参数项设置与当前版本存在差异需重新调整，或者还有软件的其他功能需一并更新等原因，需要完成一系列的配置才能结束升级。

---

## 升级后配置 > 使用 ELF 平台

# 使用 ELF 平台

以下配置项需根据软件的实际情况进行选择配置，请客户核实后再参考对应内容进行操作。

- **禁⽤ Spectre 和 Meltdown 补丁**：可选操作。自 SMTX OS 3.0.11 版本起，软件针对 Intel Spectre（CVE-2017-5753、CVE-2017-5715），以及 Meltdown（CVE-2017-5754）提供了漏洞补丁，但漏洞补丁可能会导致 I/O 性能下降约 20% ~ 30%。用户可参考自身情况，在合适的场景下禁⽤补丁。
- **转换网口绑定模式**：对于 SMTX OS 5.0.0 ~ 5.0.4 版本，当集群的存储网络开启了 RDMA 且 VDS 配置了网口绑定时，建议您在将集群升级至本版本后，手动将存储网络的网口绑定模式从 OVS Bond 转换为 Linux Bond，以提升系统的稳定性。

---

## 升级后配置 > 使用 ELF 平台 > 禁用 Spectre 和 Meltdown 补丁（可选）

# 禁用 Spectre 和 Meltdown 补丁（可选）

为应对以下漏洞造成的安全风险，SMTX OS 自 3.0.11 版本起，通过升级内核（以启用补丁的形式）对漏洞进行了修复。新的漏洞补丁可能会导致 I/O 性能下降约 20% ~ 30%。用户可参考自身情况，在合适的场景下手动禁用补丁。

- Intel Spectre（[CVE-2017-5753](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5753)、[CVE-2017-5715](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5715)）
- Meltdown（[CVE-2017-5754](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5754)）

> **说明**：
>
> 若 SMTX OS 集群在升级前已禁用了 Spectre 和 Meltdown 补丁，在升级至新版本后，禁用仍然生效，无需再次手动禁用。

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

## 升级后配置 > 使用 ELF 平台 > 转换网口绑定模式

# 转换网口绑定模式

当集群的存储网络开启了 RDMA 且 VDS 配置了 Linux Bond 时，在将集群升级至本版本后，可以选择手动将存储网络的网口绑定模式转换为 OVS Bond 下的 `balance-tcp` 模式，以提升系统性能。

完成转换后，建议在物理交换机上配置 Port Channel 哈希策略，以便充分利用多网口的带宽。具体方法请参考《SMTX OS 集群安装部署指南（ELF 平台）》的[配置 Port Channel 哈希策略](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_80)。

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
> - 若要将绑定模式转换为 `balance-TCP`（OVS Bond），对端交换机需先开启 LACP 动态链路聚合，并建议在转换前参考《SMTX OS 集群安装部署指南（ELF 平台）》的[配置 Port Channel 哈希策略](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_80)。

## 执行转换

> **注意**：
>
> 为保障集群的整体服务在转换过程中不受影响，以下转换操作请在集群各节点依次进行，且 Meta Leader 节点须在最后执行。

1. 使用 SSH 方式登录待转换节点。执行以下命令，确认集群是否有待恢复数据。若有待恢复数据，请在数据恢复完成后再执行后续步骤。

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

     进入 CloudTower 管理界面，在集群的主机列表中选中目标主机，单击右侧的 `...` 后选择进入维护模式。
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

## 升级后配置 > 使用 VMware ESXi 平台

# 使用 VMware ESXi 平台

以下配置项需根据软件的实际情况进行选择配置，请客户核实后再参考对应内容进行操作。

- **更新 I/O 重路由和 SCVM 自动重启脚本**：必选操作。在 SMTX OS 完成升级后进行配置。
- **调整 SCVM 延迟敏感度**：可选操作。SMTX OS 在升级前若版本较低，SCVM 所在的虚拟机的**延迟敏感度**选项可能未重新设置。对于性能要求较高的用户，建议将虚拟机延迟敏感度从**默认值**调整为**高**。如果用户对性能要求不高或无要求，此选项可以忽略。
- **修改虚拟机的 HA 策略**：可选操作。若集群升级前未调整虚拟机的 HA 策略，将 `MisC.APDHandlingEnable` 参数值设置为 `1`，建议在升级后进行调整。
- **升级高级监控**： 可选操作。若升级目标版本所对应的高级监控版本与升级前的高级监控版本不一致，则需要手动升级高级监控应用至最新版本，否则无需关注。

---

## 升级后配置 > 使用 VMware ESXi 平台 > 更新 I/O 重路由和 SCVM 自动重启脚本

# 更新 I/O 重路由和 SCVM 自动重启脚本

执行升级操作后，还需更新 I/O 重路由脚本和 SCVM 自动重启的脚本。

> **说明**：
>
> 若您使用升级中心对集群进行升级，在升级过程中会自动更新 I/O 重路由和 SCVM 自动重启脚本，您无需手动更新。

## 更新 I/O 重路由脚本

1. 在集群的任意一个 SCVM 中执行以下命令，系统将自动检查和升级集群里每个 ESXi 节点的 I/O 重路由脚本。

   `zbs-deploy-manage update_reroute_version`

   - **所有 ESXi 节点的 I/O 重路由脚本已升级为最新版本**：界面逐一显示 `reroute scripts is already the latest version in esxi xxx.xxx.xxx.xxx` 的提示信息，其中 *xxx.xxx.xxx.xxx* 表示集群里节点的管理 IP。在检查完所有节点的 I/O 重路由脚本后，界面将显示 `Success update latest vmware reroute script to all esxi done` 的提示信息。此时可进入下一步。
   - **部分 ESXi 节点的 I/O 重路由脚本待升级为最新版本**：界面显示 `after upgrade zbs, generate latest scripts esxi need`，表明此节点的 I/O 重路由脚本不是最新版本，系统立即启动自动升级。待所有节点自动升级完 I/O 重路由脚本后，界面将显示 `Success update latest vmware reroute script to all esxi done` 的提示信息。此时为确保整个集群的所有节点已完成 I/O 重路由脚本的升级，建议重新执行命令 `zbs-deploy-manage update_reroute_version`，若预期结果与**所有 ESXi 节点的 I/O 重路由脚本已升级为最新版本**的输出相符，则可进入下一步。
2. 在所有 ESXi 节点上执行命令 `ps -c | grep scvm_failure | grep -v grep`，若界面信息中包含 `reroute.py` 脚本信息 ，则表明 I/O 重路由脚本升级成功。

## 更新 SCVM 自动重启脚本

1. 在集群的任意一个 SCVM 中执行 `zbs-deploy-manage update-scvm-autostart` 命令，若输出符合以下要求，则表示集群中所有 ESXi 节点的 SCVM 自动重启脚本已经更新完成。

   - 界面未输出 `esxi scvm uuid: xxx sn miss, please check scvm info`，其中 `xxxx` 表示 scvm uuid；
   - 界面输出中包含信息 `Success update latest vmware scvm autostart script to all esxi done`。
2. 在所有 ESXi 节点上执行 `cat /etc/rc.local.d/local.sh | grep scvm` 命令，若界面信息中包含 `sh /vmfs/volumes/xxxx/vmware_scvm_autostart/scvm_autostart.sh &` 提示信息，其中 `xxxx` 表示 scvm uuid，请继续执行下一步；否则表示 SCVM 自动重启脚本更新失败，请联系 SmartX 研发工程师进行排查。
3. 执行命令  `ls -lh /vmfs/volumes/*/vmware_scvm_autostart/scvm_autostart.sh | grep -v datastore`。若输出的信息中包含 `scvm_autostart.sh` 文件，表明 SCVM 自动重启脚本安装成功；否则表示 SCVM 自动重启脚本更新失败，请联系 SmartX 研发工程师进行排查。

---

## 升级后配置 > 使用 VMware ESXi 平台 > 调整 SCVM 延迟敏感度

# 调整 SCVM 延迟敏感度

SCVM 延迟敏感度的高低与集群性能要求相关。优化 SCVM 虚拟机的延迟时间敏感度，可以降低网络延迟。

对于性能要求高的用户，建议将虚拟机延迟敏感度从默认值**正常**调整为**高**；对于集群性能要求不高的用户，则不必调整。

**操作步骤**

1. 在 vCenter Server 中浏览到虚拟机，右键选择**编辑设置**，在弹出的窗口中选择**虚拟机选项** > **高级**，调整虚拟机**延迟敏感度**为**高**。

   ![](https://cdn.smartx.com/internal-docs/assets/dc9f6d3b/upgrade_guide_04.png)
2. 立即关闭 SCVM，再重新开机，以使参数调整生效。

   > **注意:**
   >
   > 仅重启 SCVM 并不能使**延迟敏感度**的调整生效。请遵守上述要求，关闭 SCVM 后再开机。

---

## 升级后配置 > 使用 VMware ESXi 平台 > 修改虚拟机的 HA 策略

# 修改虚拟机的 HA 策略

1. 使用 VMware vSphere Web Client 连接到 vCenter，浏览到 ESXi 主机。
2. 选择**配置** > **系统** > **高级系统设置**，并单击**编辑**按钮。在弹出的**编辑高级系统设置**参数表中，将 `Misc.APDHandlingEnable` 参数的值修改为 1。
3. 参考上述步骤，将每个 ESXi 主机的 `Misc.APDHandlingEnable` 参数的值修改为 1。
4. 在 vCenter 中选中集群，选择**配置** > **服务** > **vSphere 可用性**，在 vSphere 可用性设置界面右侧选择**编辑**，然后在对话框中的故障和响应页面展开处于 APD 状态的数据存储，进行以下设置：

   - 将全部路径异常 (APD) 故障响应选项设置为**关闭虚拟机电源并重新启动虚拟机 - 保守的重新启动策略**；
   - 将**响应恢复**选项设置为**禁用**；
   - 将**响应延迟**的值设置为 3 分钟。
5. 单击**确定**。

---

## 升级后配置 > 使用 VMware ESXi 平台 > 升级高级监控

# 升级高级监控

**前提条件**

- 已提前下载新版本的安装文件。
- 集群已关联 vCenter Server。

**操作步骤**

1. 在 CloudTower 的**系统配置**主界面左侧的导航树中选择**高级监控**。
2. 在**已部署集群**区域框中定位需要升级的集群，在右侧单击**升级**。
3. 在弹出的**升级高级监控应用**对话框中，上传更新版本的高级监控映像文件，并查看已选择集群的版本和当前高级监控版本。
4. 单击**升级**。

   升级过程中可以在任务中心查看升级进度以及是否升级成功。

---

## 附录 > 对 SCVM 进行内存扩容

# 对 SCVM 进行内存扩容

请依次对各 SCVM 进行如下操作：

> **注意**：
>
> Meta Leader 节点应最后执行操作。在集群任一节点执行 `zbs-tool service list` 命令可确认集群 Meta Leader 节点

1. 将 SCVM 节点设置为维护模式。

   对于 5.0.5 及以上版本的集群，可通过 CloudTower 界面设置主机维护模式；对于 5.0.4 及以下版本的集群，请通过命令行的方式设置存储维护模式。

   - **5.0.5 及以上版本集群**

     登录 CloudTower，在集群的主机列表中选中 SCVM 所在的主机, 单击右侧的 **...** 并选择**进入维护模式**。
   - **5.0.4 及以下版本集群**

     执行以下命令使 SCVM 节点进入存储维护模式：

     `zbs-meta chunk set_maintenance <cid> true [--expire_duration_s EXPIRE_DURATION_S]`

     - **expire\_duration\_s**：存储维护模式超时时间，仅在进入存储维护模式时有效；如果不设置该参数，则系统默认为最大值 604800 秒（7 天）。
     - **cid**：表示将要设置存储维护模式的 Chunk ID。可通过执行命令 `zbs-meta chunk list` 来获取 Chunk ID。
     > **说明**：
     >
     > 若上述命令返回 `Failed to set maintenance mode due to extents in recover` 或者`Failed to set maintenance mode due to extents may recover`，表明当前集群存在数据恢复，请等待数据恢复完成后重试。
2. 在 vCenter Server 中针对此 SCVM 节点，右键选择**启动** > **关闭客户机操作系统**，关闭 SCVM 虚拟机的操作系统。
3. 在 vCenter Server 中针对此 SCVM 节点，右键选择**编辑设置**，将内存大小调整到目标版本集群所需的内存大小。单击**确定**进行保存。

   > **说明**：
   >
   > 若调整内存后保存失败并在 vCenter 中出现`指定的参数不正确：spec.memoryAllocation` 错误提示弹窗，请按照如下步骤进行操作：
   >
   > 1. 将内存调整到目标容量大小后，切换至**虚拟机选项**页签，在高级选项中调整虚拟机延迟敏感度为`正常`，单击**确定**进行保存。
   > 2. 再次打开 SCVM 虚拟机的**编辑设置**页面，并切换至**虚拟机选项**页签，在高级选项中将虚拟机延迟敏感度调回`高`，再次单击**确定**进行保存。
4. 在 vCenter Server 中针对此 SCVM 节点，右键选择**启动** > **打开电源**进行开机。
5. 通过 SSH 登录到 SCVM 后台执行 `free -h` 命令确认内存扩容是否生效。
6. 退出维护模式。

   - **5.0.5 及以上版本集群**

     1. 在 CloudTower 的主机概览界面中查看当前主机已处于维护模式的时间，单击提示内容右侧的**退出维护模式**。
     2. 系统弹出检查对话框，并启动退出维护模式前的自检，检查结束后返回所有自检项目的检查结果。

        - 若所有检查项目全部满足要求，允许主机退出维护模式。
        - 若部分检查结果不满足要求，请参考《SMTX OS 运维指南》中[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)小节完成整改，然后再次尝试退出维护模式。
   - **5.0.4 及以下版本集群**

     1. 执行下列命令检查集群节点状态，若返回 `CONNECTED_HEALTHY` 则表明集群状态正常。

        `zbs-meta chunk list`
     2. 确认集群状态正常后，执行以下命令使 SCVM 节点退出存储维护模式。

        `zbs-meta chunk set_maintenance <cid> false`

---

## 附录 > 小容量规格节点的系统资源占用

# 小容量规格节点的系统资源占用

## 系统对物理盘存储空间的占用

- **分层模式**

  | **物理盘用途** | **占用存储空间** | **说明** |
  | --- | --- | --- |
  | 含元数据分区的缓存盘 | 125 GiB | 系统分区、元数据分区、Journal 分区和预留空间共固定占用 125 GiB 空间，剩余空间为缓存分区。 |
  | 缓存盘 | 20 GiB | Journal 分区和预留空间共固定占用 20 GiB 空间，剩余空间为缓存分区。 |
- **不分层模式**

  | **物理盘用途** | **占用存储空间** | **说明** |
  | --- | --- | --- |
  | 含元数据分区的数据盘 | 125 GiB | 系统分区、元数据分区、Journal 分区和预留空间共固定占用 125 GiB 空间，剩余空间为数据分区。 |
  | 数据盘 | 20 GiB | Journal 分区和预留空间共固定占用 20 GiB 空间，剩余空间为数据分区。 |

## 系统对主机 CPU 和内存的占用

### ELF 平台

| **CPU 架构** | **CPU 占用** | **内存占用** |
| --- | --- | --- |
| Intel x86\_64 或 Hygon x86\_64 架构 | 7 核 | 46.5 GB + 节点内存总量（GB）/ 128 |
| 鲲鹏 AArch64 架构 | 8 核 | 58 GB + 节点内存总量（GB）/ 256 GB × 100 MB |

> **说明**：
>
> - 若服务器未启用超线程，系统将使用 CPU 的物理核心。
> - 若服务器启用了超线程，系统将使用 CPU 的逻辑核心。
> - 若节点为主节点，系统还将额外使用 1 个 CPU 核心。
> - 计算结果需向上取整。

### VMware ESXi 平台

| CPU 占用 | 内存占用 |
| --- | --- |
| 6 核 | 40 GB |

---

## 附录 > SMTX OS 节点的本地账户说明

# SMTX OS 节点的本地账户说明

SMTX OS 节点支持以下三种本地账户：

| 本地账户 | 说明 | 注意事项 |
| --- | --- | --- |
| root | 默认账户，默认禁止 SSH 远程登录。您可以使用该账户管理 SMTX OS 节点。 | - 请勿删除该账户。 - 强烈建议不要开启 root 账户通过 SSH 远程登录的权限。 - 以命令行方式升级集群时必须拥有 root 权限。 |
| smartx | 默认账户，默认支持 SSH 远程登录。您可以使用该账户通过 SSH 协议远程连接到 SMTX OS 节点。 | - 请勿删除该账户。 - 请勿更改 `/etc/sudoers` 里针对该账户的配置。 - 以该账户登录节点后，必须切换为 root 账户再执行运维操作。执行 `sudo su` 命令可免密码切换。 |
| 其他本地账户 | 由 root 账户创建的其他账户，账户权限由 root 账户决定。您可自行创建新的本地账户用于 SSH 远程登录。 | - |

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
