---
title: "SMTXOS/6.3.0/SMTX OS 售后工程师操作指南"
source_url: "https://internal-docs.smartx.com/smtxos/6.3.0/aftersales_guide/aftersales_guide_preface_generic"
sections: 73
---

# SMTXOS/6.3.0/SMTX OS 售后工程师操作指南
## 关于本文档

# 关于本文档

本文档介绍了 SMTX OS 上线后，售后工程师协助用户维护集群时可能执行的操作流程。

---

## 文档更新信息

# 文档更新信息

**2026-02-04：配合 SMTX OS 6.3.0 正式发布**

相较于 6.2.0，本版本主要更新如下：

- 更新了**更换网卡**章节。
- 新增**关闭和恢复系统服务**、**集群停机维护**、**激活 TencentOS**、**未启用双活特性的集群转换为双活集群（ELF 平台）**、**更换双活集群的优先可用域和次级可用域**和**重建双活集群的仲裁节点**章节。

---

## 硬件 > 处理物理盘卸载失败

# 处理物理盘卸载失败

> **风险提示**：
>
> 从服务器中强行拔除未卸载的物理盘，可能会导致用户业务中断甚至永久性丢失数据。

如在 CloudTower 中无法卸载物理盘，请在集群中使用如下命令行确认是否发生阻塞：

```
zbs-chunk partition list
```

或

```
zbs-chunk cache list
```

请您以一分钟为间隔观察物理盘上的 `used_space` 是否下降，如未下降，则可以确认卸载过程发生了阻塞。有以下两种原因会导致阻塞，请参考对应的解决方法继续完成卸载：

- 主机上其他物理盘的存储空间不足，集群中也没有满足数据副本放置要求的主机能够存放正在卸载的物理盘里的数据。

  此时请参照如下操作：

  1. 使用命令行 `zbs-chunk partition cancel-umount` 或 `zbs-chunk cache cancel-umount` 停止卸载物理盘。
  2. 删除集群中部分可删除的数据，释放足够的存储空间。
  3. 在 CloudTower 中再次卸载该物理盘。
- 卸载过程 I/O 中断，此时其他主机或物理盘故障可能导致正在卸载的物理盘上存放有部分数据的唯一副本，导致该物理盘上存在异常数据。

  此时请参照如下操作：

  1. 使用命令行 `zbs-chunk partition cancel-umount` 或 `zbs-chunk cache cancel-umount` 停止卸载物理盘。
  2. 使用命令行 `zbs-chunk partition set-healthy` 或 `zbs-chunk cache set-healthy` 将物理盘重置为健康状态。
  3. 使用命令行 `zbs-meta pextent find dead` 确认集群中没有异常数据。
  4. 使用命令行 `zbs-meta pextent find need_recover` 确认集群中没有待恢复数据。
  5. 在 CloudTower 中再次卸载该物理盘。请参考章节确认是否出现阻塞，并通过该小节提供的解决方法继续卸载。

如通过命令确认未发生阻塞或发生阻塞但通过上述解决方案仍无法卸载的情况下，请确认物理盘是否满足如下直接拔除的全部条件：

- 物理盘 I/O 延时不正常；

  可以所在节点上执行 `lsblk` 看到盘符，但执行 `iostat` 观察到 **await** 参数达秒级；
- 物理盘所在节点处于健康状态；

  可以在 CloudTower 查看。
- 集群中没有异常数据；

  可以使用 `zbs-meta pextent find dead` 确认集群中是否存在异常数据。如果集群经历了 Meta Leader 的切换，可以在 Meta Leader 节点的日志上从后向前搜索，确定其成为 Leader 的时间，在切换完成的 10 分钟之后再确认集群中是否存在异常数据。
- 集群中没有待恢复数据，或者集群中所有待恢复数据都在其他主机上存在至少一个活跃副本。

  可以使用 `zbs-meta pextent find need_recover` 确认集群中是否存在待恢复数据。

如满足直接拔除的全部条件，请直接在服务器上拔除物理盘，如果不满足，请申请 L3 支持。

---

## 硬件 > 修复软件 RAID 故障

# 修复软件 RAID 故障

CloudTower 的物理盘列表界面上出现软件 RAID 故障时，需要先判断物理盘中出现软件 RAID 故障是操作系统分区还是元数据分区，然后判断物理盘是否出现读写错误。

## 定位故障分区

请您首先通过 lsblk 命令查看该物理盘的操作系统分区和元数据分区对应的软件 RAID 组。

```
$ lsblk
NAME      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sdd         8:48   0  250G  0 disk
├─sdd2      8:50   0   20G  0 part
│ └─md0     9:0    0   20G  0 raid1 /var/lib/zbs/metad
├─sdd3      8:51   0   10G  0 part
├─sdd1      8:49   0   85G  0 part
│ └─md127   9:127  0   85G  0 raid1 /
└─sdd4      8:52   0  125G  0 part
sdb         8:16   0  200G  0 disk
└─sdb1      8:17   0  200G  0 part
loop0       7:0    0   20G  0 loop  /var/lib/zbs/lsm2db
sdc         8:32   0  250G  0 disk
├─sdc2      8:34   0   20G  0 part
│ └─md0     9:0    0   20G  0 raid1 /var/lib/zbs/metad
├─sdc3      8:35   0   10G  0 part
├─sdc1      8:33   0   85G  0 part
│ └─md127   9:127  0   85G  0 raid1 /
└─sdc4      8:36   0  125G  0 part
sda         8:0    0    5G  0 disk
└─sda1      8:1    0  512M  0 part  /boot
```

如上输出，根据操作系统分区挂载点（/）确定物理盘操作系统分区对应的 RAID 组，例如上述输出为 md127；根据元数据分区挂载点（/var/lib/zbs/metad）确定物理盘元数据分区对应的 RAID 组，例如上述输出为 md0。

其次，请您通过 mdadm 命令分别查看组成软件 RAID 的物理盘分区的故障情况：

```
$ mdadm --detail /dev/md127
/dev/md127:
           Version : 1.2
     Creation Time : Wed Oct 11 11:39:32 2023
        Raid Level : raid1
        Array Size : 89062400 (84.94 GiB 91.20 GB)
     Used Dev Size : 89062400 (84.94 GiB 91.20 GB)
      Raid Devices : 2
     Total Devices : 2
       Persistence : Superblock is persistent

     Intent Bitmap : Internal

       Update Time : Wed Nov  8 15:46:26 2023
             State : active, degraded
    Active Devices : 1
   Working Devices : 1
    Failed Devices : 1
     Spare Devices : 0

Consistency Policy : bitmap

              Name : localhost:root
              UUID : 9bcec233:9210bdf6:7187ac1e:b7c29294
            Events : 528967

    Number   Major   Minor   RaidDevice State
       1       8       33        0      active sync failfast   /dev/sdc1
       -       0        0        1      removed

       2       8       49        -      faulty failfast   /dev/sdd1
```

如上输出，说明操作系统分区对应的 RAID 组（md127）中的 /dev/sdd1 即物理盘 sdd 的操作系统分区处于故障状态。请以同样的步骤查看元数据分区对应的 RAID 组（md0）中的分区故障情况。

## 确认物理盘读写错误

执行 `ls /var/log/messages` 命令，检查输出结果中是否存在物理盘故障相关的异常日志，确认物理盘上是否存在读写错误。

## 故障场景

- RAID 组中一块物理盘上的操作系统分区出现故障，并且另一块物理盘上的元数据分区也出现故障时：

  - 两块物理盘都存在读写错误，请参考[特殊软件 RAID 故障处理](#%E7%89%B9%E6%AE%8A%E8%BD%AF%E4%BB%B6-raid-%E7%8A%B6%E6%80%81%E5%A4%84%E7%90%86)。
  - 其中一块物理盘不存在读写错误时，不存在读写错误的物理盘请参考[恢复物理盘的软件 RAID 状态](#%E6%81%A2%E5%A4%8D%E7%89%A9%E7%90%86%E7%9B%98%E7%9A%84%E8%BD%AF%E4%BB%B6-raid-%E7%8A%B6%E6%80%81)，然后再参考《SMTX OS 运维指南》中[更换 SSD](../os_operation_maintenance/os_operation_maintenance_16) 或[更换 HDD](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_17) 章节更换存在读写错误的物理盘。
  - 两块物理盘都不存在读写错误，请参考[恢复物理盘的软件 RAID 状态](#%E6%81%A2%E5%A4%8D%E7%89%A9%E7%90%86%E7%9B%98%E7%9A%84%E8%BD%AF%E4%BB%B6-raid-%E7%8A%B6%E6%80%81)后继续使用。
- RAID 组中仅一块物理盘的分区出现故障时：

  - 物理盘存在读写错误，请参考《SMTX OS 运维指南》中[更换 SSD](../os_operation_maintenance/os_operation_maintenance_16) 或[更换 HDD](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_17) 章节更换物理盘。
  - 物理盘不存在读写错误，请参考[恢复物理盘的软件 RAID 状态](#%E6%81%A2%E5%A4%8D%E7%89%A9%E7%90%86%E7%9B%98%E7%9A%84%E8%BD%AF%E4%BB%B6-raid-%E7%8A%B6%E6%80%81)后继续使用。

## 软件 RAID 故障处理方法

下面的步骤说明中，如果涉及到命令行操作，请在完成每一步操作后，及时使用 `mdadm --detail /dev/md127` 检查软件 RAID 状态，如果存在异常，在消除异常前不应该继续执行后续步骤。

### 恢复物理盘的软件 RAID 状态

对于健康状态处于`软件 RAID 故障`但不存在读写错误的物理盘，您可通过以下三种方式恢复该物理盘的软件 RAID 状态。

**方式一**（推荐）：

1. 在 CloudTower 的物理盘列表中单击物理盘右侧的 **...** > **卸载**，该物理盘的挂载状态更新为未挂载。
2. 使用如下命令重置物理盘故障记录：

   `zbs-node set_disk_healthy /dev/sdd`
3. 在 CloudTower 的物理盘列表中单击物理盘右侧的 **...** > **挂载**。在弹出的挂载物理盘对话框中，选择将其挂载为含元数据的盘。

**方式二**：

1. 使用如下命令恢复物理盘在软件 RAID 中的状态：

   `zbs-deploy-manage mount-disk /dev/sdd smtx_system`
2. 使用如下命令重置物理盘故障记录：

   `zbs-node set_disk_healthy /dev/sdd`

**方式三**：

1. 使用如下命令恢复物理盘在软件 RAID 中的状态：

   `mdadm --manage /dev/md127 --re-add /dev/sdd1`
2. 使用如下命令将 RAID 中的设备数设定为 2：

   `mdadm --grow --raid-devices=2 /dev/md127`
3. 使用如下命令重置物理盘故障记录：

   `zbs-node set_disk_healthy /dev/sdd`

### 特殊软件 RAID 状态处理

一般情况下，软件 RAID 由两块物理盘组成。如果第一块物理盘上的系统分区出现故障（例如 /dev/sdd1），同时第二块物理盘上的元数据分区出现故障（例如 /dev/sde2），且这两块物理盘都存在读写错误，则这两块物理盘都不能被卸载，否则剩下的物理盘不能满足系统正常运行的要求。

- **当存在空闲的物理盘槽位时：**

  1. 在主机上空闲的物理盘槽位中插入一块可以在[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)查询到且容量不低于故障盘的新物理盘。
  2. 在 CloudTower 的物理盘列表中，单击新物理盘右侧的 **...** > **挂载**。在弹出的挂载物理盘对话框中，选择将其挂载为含元数据的盘。
  3. 在 CloudTower 的物理盘列表中，单击故障物理盘右侧的 **...** > **卸载**，逐一卸载主机上的两块故障盘。
  4. 在主机上空闲的物理盘槽位中插入第二块可以在[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)查询到且容量不低于故障盘的新物理盘。
  5. 在 CloudTower 的物理盘列表中单击第二块新物理盘右侧的 **...** > **挂载**。在弹出的挂载物理盘对话框中，选择将其挂载为含元数据的盘。
- **当不存在空闲的物理盘槽位时：**

  - 若节点当前剩余数据存储可用量大于或等于一块数据盘的大小，请参照如下步骤处理：

    1. 在 CloudTower 的物理盘列表中，单击一块正常的数据盘（例如 sdb）右侧的 **...** > **卸载**。该物理盘的挂载状态更新为`未挂载`后，使用如下命令将其挂载为系统盘：

       `zbs-deploy-manage mount-disk /dev/sdb smtx_system`
    2. 在 CloudTower 的物理盘列表中，单击元数据分区出现故障且存在读写问题的物理盘（例如 sde）右侧的 **...** > **卸载**，该物理盘的挂载状态更新为`未挂载`后将其从主机上拔出。
    3. 在主机上插入一块可以在[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)查询到且容量不低于故障盘的新物理盘。
    4. 在 CloudTower 的物理盘列表中，单击新物理盘右侧的 **...** > **挂载**。在弹出的挂载物理盘对话框中，选择将其挂载为含元数据的盘。
    5. 在 CloudTower 的物理盘列表中，单击操作系统分区出现故障且存在读写问题的物理盘（例如 sdd）右侧的 **...** > **卸载**，该物理盘的挂载状态更新为`未挂载`后将其从主机上拔出。
    6. 在主机上插入第二块可以在[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)查询到且容量不低于故障盘的新物理盘。
    7. 在 CloudTower 的物理盘列表中，单击第二块新物理盘右侧的 **...** > **挂载**。在弹出的挂载物理盘对话框中，选择将其挂载为含元数据的盘。
    8. 在 CloudTower 的物理盘列表中，单击此前通过命令行挂载为系统盘的物理盘（即 sdb）右侧的 **...** > **卸载**。该物理盘的挂载状态更新为`未挂载`后，单击其右侧的 **...** > **挂载**。在弹出的挂载物理盘对话框中，选择将其挂载为数据盘。
  - 若节点当前剩余数据存储可用量小于一块数据盘的大小，请参照如下步骤处理：

    1. 使用如下命令恢复操作系统分区出现故障且存在读写问题的物理盘（例如 sdd）在软件 RAID 中的状态：

       `mdadm --manage /dev/md127 --re-add /dev/sdd1`
    2. 使用如下命令将 RAID 中设备数设定为 2：

       `mdadm --grow --raid-devices=2 /dev/md127`
    3. 在 CloudTower 的物理盘列表中，单击元数据分区出现故障且存在读写问题的物理盘（例如 sde）右侧的 **...** > **卸载**，该物理盘的挂载状态更新为`未挂载`后将其从主机上拔出。
    4. 在主机上插入一块可以在[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)查询到且容量不低于故障盘的新物理盘。
    5. 在 CloudTower 的物理盘列表中，单击新物理盘右侧的 **...** > **挂载**。在弹出的挂载物理盘对话框中，选择将其挂载为含元数据的盘。
    6. 在 CloudTower 的物理盘列表中，单击第一步中已经恢复软件 RAID 状态的物理盘（即 sdd）右侧的 **...** > **卸载**，该物理盘的挂载状态更新为`未挂载`后将其从主机上拔出。
    7. 在主机上插入第二块可以在[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)查询到且容量不低于故障盘的新物理盘。
    8. 在 CloudTower 的物理盘列表中，单击第二块新物理盘右侧的 **...** > **挂载**。在弹出的挂载物理盘对话框中，选择将其挂载为含元数据的盘。

---

## 硬件 > 处理 I/O 阻塞

# 处理 I/O 阻塞

当物理盘发生 I/O 阻塞时，CloudTower 的物理盘详情页中会出现 `发生 I/O 阻塞，该盘已下线并停止处理任何 I/O。请尽快联系售后。`的提示，此时请根据下图的流程，先[检查集群中存储数据的状态](#%E6%A3%80%E6%9F%A5%E5%AD%98%E5%82%A8%E6%95%B0%E6%8D%AE%E7%8A%B6%E6%80%81)，再根据存储数据的状态来确定物理盘 I/O 阻塞故障的处理流程。

![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_065.png)

## 检查存储数据状态

1. 通过如下命令检查是否存在数据安全和完整性问题：

   ```
   zbs-meta pextent find dead
   ```

   - 如果不存在数据安全和完整性问题，请进行下一步检查集群是否存在数据恢复。
   - 如果存在数据安全和完整性问题，即输出了受影响的数据副本，请及时联系 SmartX L3 存储工程师以提供技术支持，需要[优先恢复数据的完整性](#%E6%81%A2%E5%A4%8D%E5%AD%98%E5%82%A8%E6%95%B0%E6%8D%AE%E5%AE%8C%E6%95%B4%E6%80%A7)。
2. 通过如下命令检查集群是否存在数据恢复：

   ```
   zbs-meta pextent find need_recover
   ```

   如果集群中存在数据恢复，出于数据的安全性考虑，请等待数据恢复结束后再[更换物理盘](#%E6%9B%B4%E6%8D%A2%E5%8F%91%E7%94%9F-io-%E9%98%BB%E5%A1%9E%E7%9A%84%E7%89%A9%E7%90%86%E7%9B%98)；

   如果集群中不存在数据恢复，请[更换物理盘](#%E6%9B%B4%E6%8D%A2%E5%8F%91%E7%94%9F-io-%E9%98%BB%E5%A1%9E%E7%9A%84%E7%89%A9%E7%90%86%E7%9B%98)。

## 恢复存储数据完整性

本章节操作**必须**由 SmartX L3 存储工程师执行。

**风险提示**

`zbs-meta pextent find dead` 命令的输出结果将包含集群中所有存在数据安全和完整性问题的数据副本，这些副本所在的物理盘的故障不仅限于 I/O 阻塞，还可能存在其他存储层故障，为确保数据的安全和完整性，请**务必**联系 SmartX L3 存储工程师定位数据完整性问题的根源。

**操作步骤**

当确定被下线的物理盘上存在存储数据的最后一个副本时，一般情况下，请 SmartX L3 存储工程师参考如下步骤进行处理：

1. 解除发生 I/O 阻塞的物理盘的下线状态，以允许存储系统读取盘上数据。

   以物理盘 sdx 为例，使用如下命令解除该盘的下线状态：

   ```
   echo running > /sys/block/sdx/device/state  # 解除下线状态
   udevadm trigger --name-match=sdx  # 刷新物理盘的 udev 信息和软链接路径
   ```

   > **风险提示**
   >
   > 处于下线状态的物理盘无法读写，但解除下线状态的操作需要对物理盘进行读写，可能在下线状态解除后触发新一轮的 I/O 阻塞，请谨慎执行解除命令。

   如物理盘上的数据无法被存储服务正常读取，此时请 SmartX L3 存储工程师进一步排查相关问题。
2. 等待存储系统完成数据恢复。

   如果存在其他故障因素导致数据恢复无法正常进行，此时请 SmartX L3 存储工程师进一步排查相关问题。
3. 数据恢复完毕后，该盘会被存储系统自动卸载，然后请参考[更换发生 I/O 阻塞的物理盘](#%E6%9B%B4%E6%8D%A2%E5%8F%91%E7%94%9F-io-%E9%98%BB%E5%A1%9E%E7%9A%84%E7%89%A9%E7%90%86%E7%9B%98)进行处理。

## 更换发生 I/O 阻塞的物理盘

流程请参考下图。

![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_066.png)

登录 CloudTower 查看发生 I/O 阻塞已被下线的物理盘的挂载状态。

- 若该物理盘处于`未挂载`状态，请直接将该物理盘从服务器上拔除。
- 若该物理盘处于`部分挂载`或`已挂载`状态，即该物理盘上仍然存在正在被使用的分区：

  - 若剩余分区为 zbs-chunk 使用的存储相关的分区，请联系 SmartX L3 存储工程师调查处理。
  - 若剩余分区为系统分区或元数据分区，请参考[定位故障分区](/smtxos/6.3.0/aftersales_guide/aftersales_guide_01#%E5%AE%9A%E4%BD%8D%E6%95%85%E9%9A%9C%E5%88%86%E5%8C%BA)小节，确认软件 RAID 1 中的另一块物理盘上的系统分区和元数据分区状态是否正常：

    - 若软件 RAID 1 中的另一块物理盘上的系统分区和元数据分区状态正常，请直接将该物理盘从服务器上拔除。
    - 若软件 RAID 1 中的另一块物理盘的系统分区和元数据分区状态存在异常，请联系 SmartX L3 SRE 工程师处理。

> **说明：**
>
> 处于下线状态的物理盘无法读写，而卸载物理盘时会对物理盘进行读写，为了避免卸载过程中对该盘的读写发生阻塞，您无法在CloudTower 上卸载该物理盘，也请您不要通过命令行卸载物理盘。

## 重置物理盘健康状态

如在排查故障后确认该盘仍然可以继续正常使用，在重新使用该物理盘前，请先重置物理盘健康状态。物理盘的故障记录以物理盘的序列号作为标识，且其记录在整个集群跨节点生效。因此，如果一块物理盘存在故障记录，即使将该物理盘从一个节点卸载后插入到另一个节点，也无法挂载给根分区或者 chunk 使用。

```
zbs-node set_disk_healthy sdc
```

或

```
zbs-node set_disk_healthy /dev/sdc
```

该命令会自动解除物理盘的下线状态，并重置与该盘相关的全部健康状态。重置后请在 CloudTower 上的物理盘页面中执行挂载操作。

> **注意**：
>
> 以上操作只适用于清理物理盘误操作所引起的故障记录，对于物理盘本身存在故障而被标记的情况，在修复该故障前此操作无效。

---

## 硬件 > 更换启动盘

# 更换启动盘

SMTX OS 集群的某个节点的启动盘损坏后，服务器将无法重启。您可以参考如下要求和步骤，完成启动盘更换和集群配置操作。

**准备工作**

- 确认待更换启动盘的节点的服务器 CPU 架构和所安装的 SMTX OS 软件版本，并准备好对应的 SMTX OS 安装映像文件。
- 确认待更换启动盘的节点启动时所使用的引导模式：BIOS 或者 UEFI 方式，并根据不同模式选择对应的集群配置操作。

  SMTX OS 集群采用不同的虚拟化平台进行部署时，由于节点的启动盘介质不同，因此查看节点引导模式的方式也不同：

  - 当 SMTX OS 集群采用原生虚拟化 ELF 平台进行部署时，节点的启动盘属于服务器的物理磁盘，通常为 SATADOM 或 DELL BOSS 磁盘。可以通过登录该服务器的 IPMI 管理平台，检查 **BIOS Settings** 界面中 **Boot Mode** 选项的取值，确认其引导模式。
  - 当 SMTX OS 集群搭配 VMware ESXi 平台进行部署时，节点的启动盘属于 vSphere ESXi 的数据存储中的虚拟磁盘。可以通过 vCenter 管理平台，检查 SCVM 配置项中 **Boot Options** 选项的取值，确认其引导模式。

**操作步骤**

1. 如果节点处于健康状态，则参考《SMTX OS 运维指南》将待更换启动盘的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)，然后[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)此节点。如果节点已处于关机状态，则直接执行步骤 2。
2. 更换磁盘，更换结束后启动服务器。
3. 根据节点启动时使用的引导模式，参考 [BIOS 引导模式](/smtxos/6.3.0/aftersales_guide/aftersales_guide_03)或 [UEFI 引导模式](/smtxos/6.3.0/aftersales_guide/aftersales_guide_04)完成集群配置操作。
4. 登录 CloudTower，参考《SMTX OS 运维指南》将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。

---

## 硬件 > 更换启动盘 > BIOS 引导模式

# BIOS 引导模式

1. 在待更换启动盘的节点中挂载 SMTX OS 映像文件，并将其设置为第一启动顺序。
2. 重启服务器，在进入 SMTX OS 安装引导界面后，选择 **Troubleshooting**。

   ![](https://cdn.smartx.com/internal-docs/assets/6e80c98e/installationguide_150.png)
3. 根据操作系统选择对应选项，进入 rescue 模式。

   - 如果操作系统为 CentOS，请选择 **Rescue a OS system**。

     ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_001.png)
   - 如果操作系统为 openEuler，请选择 **Rescue a openEuler Linux Server Storage system**。

     ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_002.png)
4. 输入 **`1`** 后按 Enter 键，等待提示后根据操作系统输入命令切换到 root 路径

   - 如果操作系统为 CentOS，请输入 **`chroot /mnt/sysimage`**。

     ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_003.png)
   - 如果操作系统为 openEuler，请输入 **`chroot /mnt/sysroot`**。

     ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_004.png)
5. 执行命令 `lsblk`，定位更换后的启动盘。然后为其新建分区，保持分区信息与集群其他正常节点一致，如下图所示。

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_005.png)

   正常节点的启动盘信息可参考下图。

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_006.png)
6. 为启动盘新建分区 `sda1`，并为其设置分区大小。例如，下图中分区 Size 设置为 `537MB`。

   ```
   bash-4.2# parted /dev/sda

   bash-4.2# mklabel msdos

   bash-4.2# mkpart primary ext4 1MiB 538MB
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_007.png)
7. 将分区格式化，并将其挂载到 `/boot` 目录下。

   ```
   bash-4.2# mkfs.ext4 /dev/sda1
   bash-4.2# mount /dev/sda1 /boot
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_008.png)
8. 参考[此链接](https://access.redhat.com/solutions/2626631)的方法配置网络，然后参考以下步骤将其他正常节点的 `/boot` 中的内容复制至当前 `/boot` 目录下。

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_009.png)

   1. 完成网络配置后，暂时开启被复制的正常节点的 ssh root 权限。方法如下：

      修改正常节点的 `/etc/ssh/sshd_config` 文件，将 `PermitRootLogin` 选项的值改为 `yes`，然后使用 `systemctl restart sshd` 命令重启 ssh 服务。
   2. 以正常节点 IP 为 `192.168.26.251` 为例，执行如下命令：

      ```
      bash-4.2# scp -r 192.168.26.251:/boot /
      ```

      ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_010.png)
   3. 拷贝完成后，将正常节点的 ssh root 权限关闭。方法如下：

      修改 `/etc/ssh/sshd_config` 文件，将 `PermitRootLogin` 选项的值改为 `no`，然后使用 `systemctl restart sshd` 命令重启 ssh 服务。
9. 修复引导分区，重装 grub，生成配置文件 **grub.cfg**。

   ```
   bash-4.2# grub2-install /dev/sda
   bash-4.2# dracut -v --force --regenerate-all
   bash-4.2# grub2-mkconfig -o /boot/grub2/grub.cfg
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_011.png)

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_012.png)

   > **注意**：
   >
   > 如果 SMTX OS 集群是从 4.0.x 或更低版本升级到本版本，执行 `grub2-install` 命令时，系统提示缺少 grub efi 相关文件，可以通过安装 grub2-efi-modules 包解决（命令如下）；但如果该方法失效，可直接联系 SmartX 研发工程师获取相关 rpm 包。
   >
   > `bash-4.2# yum install grub2-efi-modules -y`
   >
   > 在安装完 grub2-efi-modules 包后，重新执行上述三条命令。
10. 替换 `/etc/fstab` 中 **`uuid`** 为新启动盘分区的 uuid。

    执行 `blkid /dev/sda1` 命令获取 uuid 信息，然后通过 `vi /etc/fstab` 命令更新为新的 uuid 信息。

    ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_013.png)
11. 重启服务器节点，在 BIOS Settings 界面中调整磁盘的启动顺序，确保从启动盘引导启动。

---

## 硬件 > 更换启动盘 > UEFI 引导模式

# UEFI 引导模式

1. 在待更换启动盘的节点中挂载 SMTX OS 映像文件，并将其设置为第一启动顺序。
2. 重启服务器，在进入 SMTX OS 安装引导界面后，选择 **Troubleshooting**。

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_014.png)
3. 根据操作系统类型，选择对应项进入 rescue 模式：

   - 如果操作系统为 CentOS，请选择 **Rescue a SMARTXOS system**，

     ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_015.png)
   - 如果操作系统为 openEuler，请选择 **Rescue a openEuler Linux Server Storage system**。

     ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_016.png)
4. 输入 **`1`** 并按 Enter 键，等待提示后，根据操作系统输入命令以切换到 root 路径：

   - 如果操作系统为 CentOS，请输入 **`chroot /mnt/sysimage`**。

     ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_017.png)
   - 如果操作系统为 openEuler，请输入 **`chroot /mnt/sysroot`**。

     ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_018.png)
5. 执行命令 `lsblk`，定位更换后的启动盘。然后为其新建分区，保持分区信息与集群其他正常节点一致，如下图所示。

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_019.png)

   正常节点的启动盘信息可参考下图。

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_020.png)
6. 为启动盘设置 GPT 分区，新建分区 `sda1`、`sda2`，并为其设置分区大小和文件系统。

   ```
   bash-4.2# parted /dev/sda

   bash-4.2# mklabel GPT

   bash-4.2# mkpart primary fat16 1MiB 269M

   bash-4.2# mkpart primary ext4 269M 806M
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_021.png)
7. 将两块分区格式化，并分别将 sda1 挂载到 `/boot/efi` 目录下，sda2 挂载到 `/boot` 目录下。

   ```
   bash-4.2# mkfs.vfat /dev/sda1
   bash-4.2# mkfs.ext4 /dev/sda2
   bash-4.2# mount /dev/sda2 /boot
   bash-4.2# mkdir /boot/efi
   bash-4.2# mount /dev/sda1 /boot/efi
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_022.png)

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_023.png)
8. 参考[此链接](https://access.redhat.com/solutions/2626631)的方法配置网络，然后参考以下步骤将其他正常节点的 `/boot` 中的内容复制至当前 `/boot` 目录下。

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_024.png)

   1. 完成网络配置后，暂时开启被复制的正常节点的 ssh root 权限。方法如下：

      修改正常节点的 `/etc/ssh/sshd_config` 文件，将 `PermitRootLogin` 选项的值改为 `yes`，然后使用 `systemctl restart sshd` 命令重启 ssh 服务。
   2. 以正常节点 IP 为 `192.168.26.251` 为例，执行如下命令：

      ```
      bash-4.2# scp -r 192.168.26.251:/boot /
      ```

      ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_025.png)

      ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_026.png)
   3. 拷贝完成后，将正常节点的 ssh root 权限关闭。方法如下：

      修改 `/etc/ssh/sshd_config` 文件，将 `PermitRootLogin` 选项的值改为 `no`，然后使用 `systemctl restart sshd` 命令重启 ssh 服务。
9. 修复引导分区，重装 grub，生成配置文件 **grub.cfg**。

   1. 执行以下命令挂载 ISO 映像文件并配置 yum 源为 `smartxos.repo`.

      ```
      # 创建 /mnt/iso 目录
      mkdir /mnt/iso

      # 将 /dev/sr0 下的 SMTX OS 映像文件挂载到 /mnt/iso 目录
      mount /dev/sr0 /mnt/iso

      # 清理 /etc/yum.repos.d 目录下的所有 yum 源文件
      rm -rf /etc/yum.repos.d/*.repo

      # 在 /etc/yum.repos.d/ 目录下创建文件 smartxos.repo
      touch /etc/yum.repos.d/smartxos.repo

      # 使用 vi /etc/yum.repos.d/smartxos.repo 命令打开文件，并写入如下内容
      [smartxos-local-iso]
      name=smartxos
      baseurl=file:///mnt/iso
      gpgcheck=0
      enabled=1
      ```

      执行完毕后，检查 `/etc/yum.repos.d/` 确保此目录下仅有 `smartxos.repo` 文件，并且其内容与上述要求的一致。
   2. 执行以下命令重装 GRUB 2 引导程序相关包：

      ```
      yum clean all
      yum reinstall grub2-efi shim grub2-tools
      ```
   3. 根据主机操作系统类型执行命令重新生成 GRUB 2 引导配置文件：

      - 若操作系统为 CentOS，请执行以下命令

        ```
        grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg
        ```
      - 若操作系统为 openEuler，请执行以下命令

        ```
        grub2-mkconfig -o /boot/efi/EFI/openEuler/grub.cfg
        ```
      - 若操作系统为 TencentOS，请执行以下命令

        ```
        ln -sf /boot/efi/EFI/tencentos/grubenv /boot/grub2/grubenv
        grub2-mkconfig -o /boot/efi/EFI/tencentos/grub.cfg
        ```
10. 替换 `/etc/fstab` 中 **`uuid`** 为新启动盘分区 sda1、sda2 的 uuid。

    执行 `blkid /dev/sda1` 和 `blkid /dev/sda2` 命令分别查看两个分区的 uuid 信息。

    ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_031.png)

    然后通过执行 `vi /etc/fstab` 命令更新为新的 uuid 信息。

    ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_032.png)
11. 重启服务器，调整系统磁盘启动顺序，确保从更换后的启动盘引导启动。

---

## 硬件 > 更换网卡 > 更换未启用 RDMA 特性的网卡

# 更换未启用 RDMA 特性的网卡

**准备工作**

在关机更换网卡前，请按照如下要求检查即将安装的网卡和集群状态，并做好准备。

- 确认即将安装的网卡与服务器机型兼容，可通过[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)进行查询。
- 若当前主机上运行的虚拟机存在无法迁出的其他虚拟机，且该虚拟机上挂载了 PCI 直通网卡或 SR-IOV 直通网卡，则先将虚拟机关机，再打开**编辑虚拟机的网络设备**手动卸载该虚拟机上挂载的 PCI 直通网卡或 SR-IOV 直通网卡。
- 若当前主机上存在处于**关机**状态且挂载了 PCI 直通网卡或 SR-IOV 直通网卡的虚拟机，则需要打开**编辑虚拟机的网络设备**手动卸载该虚拟机上挂载的 PCI 直通网卡或 SR-IOV 直通网卡。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间更换网卡，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换网卡，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，参考《SMTX OS 运维指南》将待更换网卡的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 参考《SMTX OS 运维指南》在 CloudTower 中将待更换网卡的节点[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)。
3. 更换网卡，更换结束后启动服务器。
4. 登录节点的 IPMI 管理台，确认 IPMI 管理台已识别新增加的网卡。
5. 请通过 SSH 登录节点，确认系统识别的新增网卡的名称是否与更换前网卡名称一致。

   - 若更换前后网卡型号不一致，且网卡名称不一致，请直接参考步骤 6 开始退出维护模式。
   - 若更换前后网卡型号一致，但网卡名称不一致。请执行如下操作：

     1. 将登录节点的角色切换为 root 用户。
     2. 执行如下命令查看新网卡当前的 MAC 地址：

        `ifconfig <new_nic_name>`

        其中 `<new_nic_name>` 为新网卡的当前名称。
     3. 修改原网卡配置文件内容：

        在 `vim /etc/sysconfig/network-scripts/ifcfg-<old_nic_name>` 配置文件中，将 **HWADDR** 修改为上一步骤中获取的 MAC 地址。

        其中 `<old_nic_name>` 为原网卡的名称，您可以登录 CloudTower，在集群的虚拟分布式交换机列表中选中管理网络、存储网络或接入网络所在的虚拟分布式交换机查看。
     4. 执行 `reboot` 重启节点。
     5. 节点重启完成后，检查新网卡名称是否与原网卡名称一致。若一致，则直接参考步骤 6 开始退出维护模式。
   - 若更换前后网卡名称一致，请参考步骤 6 开始退出维护模式。
6. 参考《SMTX OS 运维指南》在 CloudTower 中将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。
7. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`
8. 将管理网络、存储网络、虚拟机网络、迁移网络或接入网络所在的虚拟交换机与新添加的网口完成关联。

   登录 CloudTower，在集群的虚拟分布式交换机列表中选中管理网络、存储网络、虚拟机网络、迁移网络或接入网络所在的虚拟分布式交换机，单击右侧的 **...** 后选择**编辑**，在弹出的**编辑虚拟分布式交换机**对话框里勾选新增的网口前的复选框，并保存设置。
9. 确认集群的网络可正常访问。

   将集群中其他节点上的一台虚拟机手动迁移至已增加网卡的节点上，并登录该虚拟机的操作系统，若能 ping 通其他虚拟机，表明网络正常。

---

## 硬件 > 更换网卡 > 更换已启用 RDMA 特性的网卡

# 更换已启用 RDMA 特性的网卡

**适用场景**

本节对于主机所对应的 OVS 网桥关联的网口开启了 RDMA 特性的情况进行了介绍和举例。相较于上一个章节，在不同名网卡的处理上有一定区别，目前 RDMA 特性无法在 CloudTower 上直接更改，需要在主机上使用 CLI 工具做对应的绑定。

因此，您可以参考本节内容在 SMTX OS（ELF）集群完成以下任务：

- 更改主机上的 OVS 网桥所关联的网口。
- 变更网口的绑定模式。

> **说明：**
>
> SMTX OS 的每个网络（存储网络、管理网络和虚拟机网络）通过其所属的 VDS 所关联的物理网口（网卡）进行通信。VDS 通过每台主机上对应的 OVS 网桥与相应的物理网口进行关联，因此更换已启用 RDMA 特性的存储网络网卡时必须同步修改主机上的 OVS 网桥信息。

## 网口绑定模式变更场景及要求

SMTX OS 在创建 VDS 时，可以关联物理主机一个或多个网口。当存储网络所在的 VDS 关联了多个网口时，仅支持设置 OVS Bond 绑定类型，旧版本的可能开启了 Linux Bond 绑定类型，每种绑定类型包括 3 种绑定模式。

- OVS Bond：支持 active-backup、balance-slb、balance-tcp 三种模式。
- Linux Bond：支持 active-backup、balance-xor、802.3ad 三种模式。

详细信息请参考《SMTX OS 网络技术白皮书》中的[网口绑定](/smtxos/6.3.0/network_whitepaper/network_whitepaper_13)章节，包括每种网口绑定模式下网口的作用及支持的组网形态等相关内容。

SMTX OS 支持以下网口绑定模式变更场景，变更时，请注意转换要求和注意事项：

| 变更场景 | 转换要求和注意事项 |
| --- | --- |
| 单⽹⼝转换为 OVS Bond | - 网卡已启用 RDMA 功能，仅支持设置为 active-backup 或者 balance-tcp 模式。 - 设置为 `active-backup` 模式时，对端交换机无需设置。 - 设置为 `balance-tcp` 模式时，要求对端交换机先开启 LACP 动态链路聚合。使用 Mellanox CX5 网卡时不建议使用该绑定模式，否则可能导致网络延迟升高。 |
| OVS Bond 转换为单⽹⼝ | - 转换后，OVS ⽹桥只关联⼀个⽹⼝，绑定模式设置为 `None`。 - 转换前后 OVS 网桥对应的绑定名称保持不变。 |
| 不同 OVS Bond 之间互相转换 | - 开启 RDMA 仅支持在 OVS Bond 模式 active-backup 与 balance-tcp 模式间转换。 - 设置为 `balance-tcp` 模式时，要求对端交换机开启 LACP 动态链路聚合。使用 Mellanox CX5 网卡时不建议使用该绑定模式，否则可能导致网络延迟升高。 - 转换前后 OVS 网桥对应的绑定名称保持不变。 |
| Linux Bond 转换为单⽹⼝ | - 转换后，OVS ⽹桥只关联⼀个⽹⼝，绑定模式设置为 `None`。 - 转换后，OVS 网桥对应的绑定名称设置为 `None`。 |
| Linux Bond 转换为 OVS Bond | - 原始 Linux Bond 为 `802.3ad` 模式时，仅能转换为 OVS Bond 模式 `balance-tcp`。使用 Mellanox CX5 网卡时不建议使用 `balance-tcp`，否则可能导致网络延迟升高。 - 原始 Linux Bond 为 `active-backup` 或者 `balance-xor` 模式时，仅能转换为 OVS Bond 模式 `active-backup`。 - 转换后 OVS 网桥对应的绑定名称为新的名称。 - 若从 Linux Bond 模式 `balance-xor` 转换为 OVS Bond 模式 `active-backup`，在转换前需要修改交换机取消 Port Channel 配置。 |
| OVS 未关联网口 | 在配置好的环境中误删除网卡，导致 OVS 网桥未关联网口，因此重新关联网口时，不需要填写“更换网卡前 OVS 网桥所关联的物理网口名称或者绑定名称”。 |

## 更换流程

**准备工作**

更换网卡时，需要使用 CLI 命令对网桥参数进行查询、设置、同步等操作。请在操作前参考《SMTX OS CLI 命令参考》中**管理网络**章节，了解相关命令的使用方法及参数设置要求。

在关机更换网卡前，请按照如下要求检查待安装的网卡和集群状态，并做好准备。

- 确认新更换的网卡与服务器机型兼容，可通过[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)进行查询。
- 若当前主机上运行的虚拟机存在无法迁出的其他虚拟机，且该虚拟机上挂载了 PCI 直通网卡或 SR-IOV 直通网卡，则先将虚拟机关机，再打开**编辑虚拟机的网络设备**手动卸载该虚拟机上挂载的 PCI 直通网卡或 SR-IOV 直通网卡。
- 若当前主机上存在处于**关机**状态且挂载了 PCI 直通网卡或 SR-IOV 直通网卡的虚拟机，则需要打开**编辑虚拟机的网络设备**手动卸载该虚拟机上挂载的 PCI 直通网卡或 SR-IOV 直通网卡。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间更换网卡，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换网卡，请您知悉上述风险后进行操作。

**操作步骤**

1. 使用 SSH 方式登录待更换网卡的节点。由于更换存储网络、管理网络或接入网络所占用的网卡会造成其对应网络短暂中断，因此，建议通过管理网络登录节点修改连接存储网络或接入网络的 OVS 网桥。
2. 执行命令 `ovs-vsctl show` ，查看主机的 OVS 网桥，并记录**待修改的 OVS 网桥名称**，以及**待更换网卡所绑定的端口名称**。
3. 切换至集群其他正常运行的节点，执行如下命令，查看和步骤 2 中待修改 OVS 网桥名称相同的 OVS 网桥信息，同时记录当前该 OVS 网桥所对应的网口绑定名称，即 `bond_name` 值。

   `network-tool get-bond-name --ovsbr_name <ovsbr_name>`
4. 登录 CloudTower，参考《SMTX OS 运维指南》将待更换网卡的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
5. 参考《SMTX OS 运维指南》在 CloudTower 中将待更换网卡的节点[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)。
6. 更换网卡，更换结束后启动服务器。
7. 登录已更换网卡的节点的 IPMI 管理台，确认 IPMI 管理台已识别新增加的网卡。
8. 请通过 SSH 登录节点，确认系统识别的新增网卡的名称是否与更换前网卡名称一致。

   - 若更换前后网卡型号不一致，且网卡名称不一致，请直接参考步骤 9 修改 OVS 网桥信息。
   - 若更换前后网卡型号一致，但网卡名称不一致。请执行如下操作：

     1. 将登录节点的角色切换为 root 用户。
     2. 执行如下命令查看新网卡当前的 MAC 地址：

        `ifconfig <new_nic_name>`

        其中 `<new_nic_name>` 为新网卡的当前名称。
     3. 修改原网卡配置文件内容：

        在 `vim /etc/sysconfig/network-scripts/ifcfg-<old_nic_name>` 配置文件中，将 **HWADDR** 修改为上一步骤中获取的 MAC 地址。

        其中 `<old_nic_name>` 为原网卡的名称，您可以登录 CloudTower，在集群的虚拟分布式交换机列表中选中网络所在的虚拟分布式交换机查看。
     4. 执行 `reboot` 重启节点。
     5. 节点重启完成后，检查新网卡名称是否与原网卡名称一致。若一致，则跳转至步骤 11，完成剩余操作。
   - 若更换前后网卡名称一致，跳转至步骤 11，完成剩余操作。
9. 在更换网卡节点上执行如下命令，修改 OVS 网桥信息。

   `network-tool change-bridge --ovsbr_name <ovsbr_name_to_be_changed> --old_port_name <old_port_name> --nics <target_nics> --bond_mode <bonding_mode> --rb_interval <rb_interval> --bond_name <bonding_name> --active_slave <active_nic_name> --mcast_snooping <current_mcast_snooping>`

   请参考《SMTX OS CLI 命令参考》中[管理网卡](/smtxos/6.3.0/cli_guide/cli_guide_78#%E8%AE%BE%E7%BD%AE%E7%BD%91%E6%A1%A5%E5%8F%82%E6%95%B0)章节，获取相关 CLI 命令及参数的详细说明。

   执行该命令后，若系统输出 `change bridge finish`，则表明修改 OVS 网桥信息成功。

   **使用示例**

   active-backup（OVS Bond）转换为单⽹⼝的使用示例如下。

   对原始名称为 ovsbr-storage 的 OVS 网桥进行参数设置。将绑定模式为 active-backup（OVS Bond）的双网口变更为单网口（eth0）。通过步骤 3 查询到该 OVS ⽹桥所对应的⽹⼝绑定名称为 `bond-m-dd417f1a` 。该 OVS 网桥关联的 VDS 未开启 IGMP/MLD 侦听。

   ```
   $network-tool get-bond-name --ovsbr_name ovsbr-storage
   ...
   2022-05-18 12:44:33,892 [72353] [INFO] bond_name:  bond-m-dd417f1a

   $network-tool change-bridge --ovsbr_name ovsbr-storage --old_port_name bond-m-dd417f1a --nics eth0 --bond_mode None --bond_name bond-m-dd417f1a --mcast_snooping disable  
   ...  
   ...  
   ...  
   [INFO] change bridge finish
   ```
10. 在更换网卡的节点上执行如下命令，将修改后的 OVS 网桥信息同步至数据库。

    其中 `bonding_mode` 和 `bonding_name` 参数值必须与步骤 9 所执行命令中的 `bonding_mode` 和 `bonding_name` 参数值保持一致。

    `--nics <uplink_nics>` 为可选参数。命令格式为 --nics "eth0 eth1"。若通过 network-tool change-bridge 命令将被隔离的故障网卡和 OVS 网桥解除关联，需配置此参数，且需和 network-tool change-bridge 命令中的 `--nics <target_nics>` 参数保持一致。

    `network-tool sync-bridge --ovsbr_name <ovsbr_name_to_be_changed> --bond_mode <bonding_mode> --bond_name <bonding_name> --active_slave <active_nic_name>`

    请参考《SMTX OS CLI 命令参考》中[管理网卡](/smtxos/6.3.0/cli_guide/cli_guide_78#%E5%90%8C%E6%AD%A5%E7%BD%91%E6%A1%A5%E7%BD%91%E5%8D%A1%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E4%BF%A1%E6%81%AF%E8%87%B3%E6%95%B0%E6%8D%AE%E5%BA%93)章节，获取相关 CLI 命令及参数的详细说明。

    执行完命令后，若系统输出 `sync successfully`，则表明同步数据成功。
11. 登录 CloudTower，参考《SMTX OS 运维指南》将已更换网卡的节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。
12. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

    `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`
13. 确认集群的虚拟机网络可正常访问。

    将集群中其他节点上的一台虚拟机手动迁移至已更换网卡的节点上，并登录该虚拟机的操作系统，若能 ping 通其他虚拟机，表明虚拟机网络正常。

---

## 硬件 > 更换存储控制器

# 更换存储控制器

更换存储控制器时，请您根据存储控制器的使用场景参考不同小节进行操作：

- 存在硬件 RAID 1 配置
- 不存在硬件 RAID 1 配置

## 存在硬件 RAID 1 配置

当构建硬件 RAID 1 的存储控制器（如 RAID 卡或 Dell BOSS 卡）发生故障，该控制器创建的所有 RAID 1 虚拟盘将不可用，请您根据该存储控制器创建的 RAID 1 虚拟盘的使用场景参考不同小节进行操作：

- 系统盘
- 启动盘

### 系统盘硬件 RAID 1

**准备工作**

- 确认即将安装的存储控制器与原来的存储控制器的型号完全相同。
- 记录存储控制器槽位。

**操作步骤**

1. 移除故障控制器所在的主机，请参考《SMTX OS 运维指南》[移除节点](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_31)章节的内容进行操作。
2. 更换存储控制器后，开启服务器，将 2 块系统盘组建成硬件 RAID 1。
3. 将主机重新添加至原集群，请参考《SMTX OS 运维指南》[添加节点](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_08)章节的内容进行操作。

### 启动盘硬件 RAID 1

**准备工作**

在关机更换存储控制器前，请按照如下要求检查集群状态，并做好准备。

- 记录存储控制器槽位。
- 对于 SMTX OS（VMware ESXi）集群，请参考 VMware 官方文档，手动将待更换存储控制器的 ESXi 主机上的虚拟机全部迁移至其他 ESXi 主机。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间更换存储控制器，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换存储控制器，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，参考《SMTX OS 运维指南》将待更换存储控制器的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)，然后[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)该节点。如果节点宕机，可以忽略该操作，直接进行步骤 2。
2. 更换存储控制器，更换结束后开启服务器，将启动盘组建成硬件 RAID 1。
3. 重启服务器后若无法正常引导进系统，请根据服务器原有引导模式参考[更换启动盘](/smtxos/6.3.0/aftersales_guide/aftersales_guide_02)章节内容重建引导盘。

## 不存在硬件 RAID 1 配置

**准备工作**

在关机更换存储控制器前，请按照如下要求检查新的存储控制器和集群状态，并做好准备。

- 确认即将安装的存储控制器与原来的存储控制器的型号完全相同。
- 记录存储控制器槽位。
- 对于 SMTX OS（VMware ESXi）集群，请参考 VMware 官方文档，手动将待更换存储控制器的 ESXi 主机上的虚拟机全部迁移至其他 ESXi 主机。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间更换存储控制器，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换存储控制器，请您知悉上述风险后进行操作。

**操作步骤**

1. 如果节点处于健康状态，则参考《SMTX OS 运维指南》将待更换启动盘的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)，然后[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)该节点。如果节点已处于关机状态，则直接执行步骤 2。
2. 更换存储控制器，断开存储控制器与物理盘的连接，避免服务器开机后直接进入系统。
3. 开启服务器，进入存储控制器配置界面，将存储控制器模式修改为更换前存储控制器的模式。
4. 关闭服务器，重新连接存储控制器与物理盘，再次开启服务器。
5. 登录 CloudTower，参考《SMTX OS 运维指南》将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。如果更换存储控制器前节点宕机，可以忽略该操作，直接进行步骤 6。
6. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

---

## 硬件 > 更换 GPU（ELF 平台）

# 更换 GPU（ELF 平台）

本节描述的操作步骤仅适用于在 SMTX OS（ELF）集群的主机上更换 GPU 的场景。

**准备工作**

将主机上所有挂载了该 GPU 设备的虚拟机关机，并在**编辑虚拟机**页面卸载该 GPU 设备。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间更换 GPU ，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换 GPU，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，参考《SMTX OS 运维指南》将待更换 GPU 的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 参考《SMTX OS 运维指南》在 CloudTower 中[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)该节点。
3. 更换 GPU，更换结束后启动服务器。

   > **说明：**
   >
   > 若主机上存在多个同名的 GPU 设备，可通过 GPU 设备信息中 **ID** 描述的 PCI 地址确定待移除的 GPU 的位置。
4. 登录 CloudTower，参考《SMTX OS 运维指南》将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。
5. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`
6. 登录 CloudTower，进入该主机的概览界面，查看**GPU 设备**列表，确认新的 GPU 设备安装成功。

**注意事项**

若移除主机 GPU 前未卸载虚拟机的 GPU 设备，移除 GPU 后虚拟机将无法开机，并且提示“GPU 设备不存在”。此时虚拟机详情页中会标记已被移除的 GPU 设备，在**编辑虚拟机**中将其卸载后，重新开机即可。

---

## 硬件 > 更换加密控制器（ELF 平台）

# 更换加密控制器（ELF 平台）

本节描述的操作步骤仅适用于在 SMTX OS（ELF）集群的主机上更换独立加密控制器的场景。

**准备工作**

将主机上所有挂载了该加密控制器的虚拟机关机，并在**编辑虚拟机**页面卸载该加密控制器。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间更换加密控制器，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换加密控制器，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，参考《SMTX OS 运维指南》将待更换加密控制器的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 参考《SMTX OS 运维指南》在 CloudTower 中[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)该节点。
3. 更换加密控制器，更换结束后启动服务器。
4. 配置加密控制器 SR-IOV 直通。

   具体请参考《SMTX OS 特性说明》的[使用加密控制器 SR-IOV 直通](/smtxos/6.3.0/os_property_notes/os_property_notes_83)的步骤 3～5。
5. 登录 CloudTower，参考《SMTX OS 运维指南》将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。
6. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

---

## 硬件 > 更换 CPU（SMTX Halo 超融合一体机）

# 更换 CPU（SMTX Halo 超融合一体机）

本节描述的方法和步骤仅针对 SMTX Halo 超融合一体机的 CPU 故障场景，非一体机的 CPU 故障更换由服务器的厂商负责，其流程和步骤与本节不同。

**准备工作**

请确保即将安装的 CPU 与原来服务器上的 CPU 型号须保持一致。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间更换 CPU，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换 CPU，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，参考《SMTX OS 运维指南》将待更换 CPU 的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 参考《SMTX OS 运维指南》在 CloudTower 中[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)该节点。
3. SMTX Halo 超融合一体机的硬件供应商更换 CPU 散热模块，拆卸原来的 CPU 后，安装新的 CPU。
4. 启动服务器，开机后登录节点的 IPMI 管理台，确认 IPMI 管理台已识别新更换的 CPU。
5. 登录 CloudTower，参考《SMTX OS 运维指南》**将该节点**[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。
6. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

---

## 硬件 > 更换主板（SMTX Halo 超融合一体机）

# 更换主板（SMTX Halo 超融合一体机）

本节描述的方法和步骤仅针对 SMTX Halo 超融合一体机的主板故障场景，非一体机的主板故障更换由服务器的厂商负责，其流程和步骤与本节不同。

**准备工作**

请确保即将安装的主板与原来服务器上的主板型号须保持一致。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间更换主板，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换主板，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，参考《SMTX OS 运维指南》将待更换主板的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 参考《SMTX OS 运维指南》在 CloudTower 中[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)该节点。
3. SMTX Halo 超融合一体机的硬件供应商拆卸原来的主板，并更换新主板，最后完成风扇支架、导风罩以及顶盖的安装。
4. 更新 SMTX Halo 超融合一体机的序列号，并在 BIOS 中完成相应的设置。

   - **Lenovo 一体机**：登录 [Lenovo XClarity Essentials OneCLI](https://datacentersupport.lenovo.com/sg/en/solutions/ht116433) 平台并依次执行以下操作：

     1. 参考[此链接](https://support.lenovo.com/sg/en/solutions/ht507532-how-to-update-vpd-using-onecli)开机，进入 BMC 页面并更新 VPD；
     2. 参考[此链接](https://datacentersupport.lenovo.com/sg/en/solutions/ht507603-video-how-to-setup-tpmtcm-policy)开启 TPM/TCM。
   - **Dell 一体机**

     1. [使用 Easy Restore 还原系统](https://www.dell.com/support/manuals/zh-cn/poweredge-r750/per750_ism_pub/%E2%80%9C%E4%BD%BF%E7%94%A8-easy-restore-%E5%8A%9F%E8%83%BD%E8%BF%98%E5%8E%9F%E7%B3%BB%E7%BB%9F%E2%80%9D?guid=guid-348a53d2-8778-496c-a53b-12bc3bc26afa&lang=zh-cn)更新和绑定一体机序列号（更新主板后）以及其他信息。
     2. 参考[此链接](https://www.dell.com/support/manuals/zh-cn/poweredge-r750/per750_ism_pub/%E5%8F%AF%E4%BF%A1%E5%B9%B3%E5%8F%B0%E6%A8%A1%E5%9D%97?guid=guid-d827d373-69b3-440f-9aae-458b19bf77f0&lang=zh-cn)开启 TPM/TCM。
     3. 根据一体机的机型，参考对应的手册设置 BIOS：

        - Halo 7100（G14 系列）：[Setting up BIOS on 14th Generation (14G) Dell EMC PowerEdge Servers](https://downloads.dell.com/solutions/general-solution-resources/White%20Papers/Setting_BIOSin14G-Serv%2816Apr2018%29.pdf)
        - Halo 7200（G15 系列）：[Dell EMC PowerEdge R750 BIOS 和 UEFI 参考指南](https://dl.dell.com/content/manual38508019-dell-emc-poweredge-r750-bios-%E5%92%8C-uefi%E5%8F%82%E8%80%83%E6%8C%87%E5%8D%97.pdf?language=zh-cn&ps=true)
5. 重启服务器，进入 BIOS 并检查配件信息，确认能识别以下所有配件且数量正确。

   - CPU
   - 内存数量或者内存总容量
   - 存储控制器数量及型号
   - 硬盘数量及型号
   - 网卡数量及型号
6. 登录 CloudTower，参考《SMTX OS 运维指南》将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。
7. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

> **注意**：
>
> 如更换主板后发现系统时钟不同步，请参考[调整集群系统时间](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_11)章节修正系统时间。

---

## 集群 > 关闭和恢复系统服务

# 关闭和恢复系统服务

以下运维场景需要您参考本章节内容按顺序关闭 SMTX OS 集群上的所有系统服务：

- 集群停机维护
- 集群启用 Boost 模式

运维结束后，还需参考本章节内容按顺序开启这些系统服务。

---

## 集群 > 关闭和恢复系统服务 > 识别系统服务虚拟机

# 识别系统服务虚拟机

您可以在 Fisheye 的**所有虚拟机**视图中，根据下表搜索关键字，识别对应的所有系统服务虚拟机，然后执行相应操作。

| 系统服务 | 服务虚拟机 | 关键字 |
| --- | --- | --- |
| SMTX 备份与容灾 | 备份服务虚拟机 | `backup-` |
| 复制服务虚拟机 | `replication-` |
| SMTX Kubernetes 服务 | 管控集群 Control Plane 虚拟机 | `sks-mgmt-controlplane-` |
| 管控集群 Worker 虚拟机 | `sks-mgmt-workergroup1-` |
| 工作负载集群 Control Plane 虚拟机 | `工作负载集群名称-controlplane-` |
| 工作负载集群 Worker 虚拟机 | `工作负载集群名称-节点组名称-` |
| SKS 容器镜像仓库虚拟机 | `sks-registry-` |
| 用户容器镜像仓库虚拟机 | `user-registry-service-` |
| SMTX 文件存储 | 文件控制器 | `sfs-` |
| 可观测性平台 | 可观测性服务虚拟机 | `observability-` |
| Everoute | Everoute controller、负载均衡虚拟机 | `everoute-cluster-` |
| 边缘网关虚拟机 | `vpc-gateway-` |
| 深度安全防护 | 安全防护虚拟机 | `SVM-` |
| CloudTower | CloudTower 代理虚拟机 | `agent-mesh-node-` |
| CloudTower 虚拟机 | - CloudTower 未启用 HA：   - 通过 CloudTower Installer 安装部署时CloudTower 虚拟机名称为 `CloudTower`。   - 在集群中手动创建虚拟机后再进行部署时，CloudTower 虚拟机名称为 您为其设置的`虚拟机名称`。 - CloudTower 启用 HA 后：   - 主动节点的名称为启用 HA 前的CloudTower 虚拟机名称，请根据安装部署方式确认。   - 仲裁节点和被动节点的名称为部署 CloudTower 高可用集群时您为其设置的`虚拟机名称`。 |

---

## 集群 > 关闭和恢复系统服务 > 关闭系统服务

# 关闭系统服务

当 SMTX OS 集群中部署了高级监控和其他系统服务，维护前请参考本小节和[识别系统服务虚拟机](/smtxos/6.3.0/aftersales_guide/aftersales_guide_51)小节的内容，识别并按顺序关闭这些系统服务。

## 准备工作

在关闭系统服务前，请您登录 CloudTower，进入**集群**的**虚拟机**列表，确认该集群中不存在除系统服务虚拟机外的虚拟机，或除系统服务虚拟机外的虚拟机均关机。

## 关闭系统服务顺序

![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_033.png)

上图展示了 SMTX OS 集群中部署了所有系统服务时的关闭顺序，实际运维过程中请直接跳过未部署的系统服务。

**第一步**：关闭 SMTX 备份与容灾、SMTX Kubernetes 服务，这两个服务的关闭没有先后顺序。

**第二步**：关闭 SMTX 文件存储、可观测性平台和高级监控，这三个服务的关闭没有先后顺序。

**第三步**：关闭 Everoute 和深度安全防护，这两个服务的关闭没有先后顺序。

**第四步**：关闭 CloudTower。

## 关闭系统服务虚拟机操作

一个系统服务中可能包含多个系统服务虚拟机，请参考本小节内容按顺序关闭系统服务中的所有系统服务虚拟机。

### SMTX 备份与容灾

登录 Fisheye，关闭所有备份服务虚拟机和复制服务虚拟机，这些虚拟机之间没有先后顺序，可以同时关闭。

### SMTX Kubernetes 服务

1. 在 CloudTower 上暂停所有管控集群同步，请参考《SMTX Kubernetes 服务管理指南》的**暂停/恢复同步管控集群**章节。
2. 在 CloudTower 上暂停所有工作负载集群同步，请参考《SMTX Kubernetes 服务管理指南》的**暂停/恢复同步工作负载集群**章节。
3. 登录 Fisheye，按照如下顺序关闭虚拟机：

   1. 管控集群 Control Plane 虚拟机
   2. 管控集群 Worker 虚拟机
   3. 工作负载集群 Control Plane 虚拟机
   4. 工作负载集群 Worker 虚拟机
   5. SKS 容器镜像仓库虚拟机
   6. 用户容器镜像仓库虚拟机

### SMTX 文件存储

- 1.2.0 及以上版本：

  1. 在 CloudTower 上逐一将 SMTX OS 集群上所有的文件存储集群中所有文件系统下线，请参考《SMTX 文件存储用户指南》的**下线文件系统**章节。
  2. 待所有文件系统完成下线后，通过命令行将文件存储集群下线，请参考《SMTX 文件存储 CLI 命令参考》的**下线文件存储集群**章节。
- 1.2.0 以下版本：

  1. 在 CloudTower 上逐一将 SMTX OS 集群上所有的文件存储集群中所有文件系统下线，请参考《SMTX 文件存储用户指南》的**下线文件系统**章节。
  2. 待所有文件系统完成下线后，登录 Fisheye，批量关闭文件控制器，**禁止选择**强制关机。

### 可观测性平台

登录 Fisheye，关闭可观测性服务虚拟机，**禁止选择**强制关机。

### 高级监控

在任一能访问管理 IP 的终端执行如下命令关闭高级监控虚拟机。

`<NODE_IP>` 为 SMTX OS 集群任一节点的管理 IP，`<USERNAME>` 和 `<PASSWORD>` 为 Fisheye 账号及密码。

```
NODE_IP=<NODE_IP>; USERNAME='<USERNAME>'; PASSWORD='<PASSWORD>'; TOKEN=$(curl -s -X POST "http://$NODE_IP/api/v3/sessions" -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" | sed -n 's/.*"token":"\([^"]*\)".*/\1/p'); echo $TOKEN; curl -X POST "http://$NODE_IP/api/v3/applications/octopus-extension:stop" -H "Grpc-Metadata-Token: $TOKEN";
```

### Everoute

登录 Fisheye，批量关闭 Everoute controller、负载均衡虚拟机和边缘网关虚拟机。

### 深度安全防护

登录 CloudTower 关闭安全防护虚拟机。

### CloudTower

1. 登录 Fisheye，关闭 CloudTower 代理虚拟机，**禁止选择**强制关机。
2. 关闭 CloudTower 虚拟机：
   - 若 CloudTower 未启用 HA：登录 Fisheye，关闭 CloudTower 虚拟机，**禁止选择**强制关机。
   - 若 CloudTower 已启用 HA（所有关机操作均**禁止选择**强制关机）：
     - 集群上仅有其中一个高可用节点：
       1. 参考《CloudTower 使用指南》中**管理 CloudTower 高可用** > **查看基本信息**章节，确认该高可用节点状态正常。
       2. 关闭该高可用节点：
          - 主动节点虚拟机或被动节点虚拟机：登录 Fisheye，关闭虚拟机。
          - 仲裁节点虚拟机：
            - 部署在 VMware ESXi 平台时，直接关闭仲裁节点虚拟机。
            - 部署在 SMTX OS（ELF）平台时，登录 Fisheye，关闭仲裁节点虚拟机。
     - 集群上包含两个及以上高可用节点：登录 Fisheye，依次关闭被动节点虚拟机、仲裁节点虚拟机、主动节点虚拟机。

---

## 集群 > 关闭和恢复系统服务 > 恢复系统服务

# 恢复系统服务

当 SMTX OS 集群运维前关闭了系统服务，运维结束后，请参考本小节和[识别系统服务虚拟机](/smtxos/6.3.0/aftersales_guide/aftersales_guide_51)小节的内容，识别并按顺序开启这些系统服务。

## 恢复系统服务顺序

SMTX OS 集群恢复后，请按下图中的顺序确认系统服务虚拟机是否随主机自动开机成功，未开机的系统服务虚拟机请按照指引启动对应的系统服务。

> **说明**：
>
> - 目前支持随主机自动开机的系统服务虚拟机有**CloudTower 代理虚拟机**、**SKS 容器镜像仓库虚拟机**、**容器镜像仓库虚拟机**、**可观测性服务虚拟机**、**备份服务虚拟机**、**复制服务虚拟机**。
> - 下图展示了 SMTX OS 集群中部署了所有系统服务时的恢复顺序，实际运维过程中请直接跳过未部署的系统服务。

![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_034.png)

**第一步**：恢复 CloudTower。

**第二步**：恢复 Everoute 和深度安全防护，这两个服务的恢复没有先后顺序。

**第三步**：恢复 SMTX 文件存储、可观测性平台和高级监控，这三个服务的恢复没有先后顺序。

**第四步**：恢复 SMTX 备份与容灾、SMTX Kubernetes 服务，这两个服务的恢复没有先后顺序。

## 恢复系统服务虚拟机操作

### CloudTower

1. CloudTower 所在的主机开机。
2. 登录 Fisheye：

   - 若 CloudTower 未启用 HA： 开启 CloudTower 虚拟机。
   - 若 CloudTower 已启用 HA： 依次开启主动节点虚拟机、仲裁节点虚拟机、被动节点虚拟机。
3. 确认运维前关闭的 CloudTower 代理虚拟机是否随主机开机。如未开机请登录 Fisheye 开机。

### 深度安全防护

1. 安全防护虚拟机所在主机开机。
2. 登录 CloudTower 确认运维前关闭的安全防护虚拟机是否随主机开机。如未开机请在 CloudTower 上将其开机。
3. 确认安全防护虚拟机开机后，将开启防病毒或深度包检测的虚拟机开机。

### Everoute

主机开机后，确认运维前关闭的 Everoute controller、负载均衡虚拟机和边缘网关虚拟机是否随主机开机。如未开机请登录 Fisheye 批量开机。

### 可观测性平台

主机开机后，确认运维前关闭的可观测性服务虚拟机是否随主机开机。如未开机请登录 Fisheye 开机。

### SMTX 文件存储

- 1.2.0 及以上版本：

  1. 通过命令行将文件存储集群上线，请参考《SMTX 文件存储 CLI 命令参考》的**上线文件存储集群**章节。
  2. 在 CloudTower 上按需将文件系统上线，请参考《SMTX 文件存储用户指南》的**上线文件系统**章节。
- 1.2.0 以下版本：

  1. 主机开机后，确认运维前关闭的文件控制器是否随主机开机。如未开机请登录 Fisheye 批量开机。
  2. 在 CloudTower 上按需将文件系统上线，请参考《SMTX 文件存储用户指南》的**上线文件系统**章节。

### 高级监控

在任一能访问管理 IP 的终端执行如下命令开启高级监控虚拟机。

`<NODE_IP>` 为 SMTX OS 集群任一节点的管理 IP，`<USERNAME>` 和 `<PASSWORD>` 为 Fisheye 账号及密码。

```
NODE_IP=<NODE_IP>; USERNAME='<USERNAME>'; PASSWORD='<PASSWORD>'; TOKEN=$(curl -s -X POST "http://$NODE_IP/api/v3/sessions" -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" | sed -n 's/.*"token":"\([^"]*\)".*/\1/p'); echo $TOKEN; curl -X POST "http://$NODE_IP/api/v3/applications/octopus-extension:start" -H "Grpc-Metadata-Token: $TOKEN";
```

### SMTX Kubernetes 服务

1. 主机开机后，确认运维前关闭的 SKS 容器镜像仓库虚拟机、容器镜像仓库虚拟机是否随主机开机。如未开机请登录 Fisheye 先开启容器镜像仓库虚拟机，然后开启 SKS 容器镜像仓库虚拟机。
2. 登录 Fisheye，依次开启如下虚拟机：

   1. 工作负载集群 Worker 虚拟机
   2. 工作负载集群 Control Plane 虚拟机
   3. 管控集群 Worker 虚拟机
   4. 管控集群 Control Plane 虚拟机
3. 在 CloudTower 上恢复管控集群同步，请参考《SMTX Kubernetes 服务管理指南》的**暂停/恢复同步管控集群**章节。
4. 在 CloudTower 上恢复所有工作负载集群同步，请参考《SMTX Kubernetes 服务管理指南》的**暂停/恢复同步工作负载集群**章节。

### SMTX 备份与容灾

主机开机后，确认运维前关闭的备份服务虚拟机、复制服务虚拟机是否随主机开机。如未开机请登录 Fisheye 开机。

---

## 集群 > 集群停机维护

# 集群停机维护

当机房面临如下场景时，需要手动将 SMTX OS 集群的主机关机，维护期结束后，还需要重新启动服务器，恢复集群的运行。

- 机房搬迁
- 旧集群下线
- 机房进行网络改造
- 在预期内机房断电

## ELF 平台

**准备工作**

使用 SSH 方式登录集群的节点，执行以下命令，确认 SMTX OS 集群不存在数据恢复。

`zbs-meta pextent find need_recover`

若系统输出 `No PExtents found.`，表示集群不存在数据恢复。

**操作步骤**

1. 登录 CloudTower，进入集群的虚拟机列表，确认该集群中不存在虚拟机，或者虚拟机处于**关机**状态。

   > **说明：**
   >
   > - 若虚拟机列表中存在部分未关机的虚拟机，并且虚拟机未安装操作系统，或者虚拟机的操作系统不支持 ACPI，此时可选中虚拟机，在弹出的虚拟机详情面板中单击**关机**，然后选择**强制关闭虚拟机**。
   > - 若虚拟机列表中存在未关机的系统服务虚拟机，请参考[关闭系统服务虚拟机](/smtxos/6.3.0/aftersales_guide/aftersales_guide_52)处理。
2. 使用 SSH 方式登录集群中的一个节点，执行以下命令，关闭集群所有节点。

   ```
   zbs-cluster shutdown_hosts --hosts=all --action=poweroff --network=storage
   ```

   > **说明：**
   >
   > - 如果存储网络无法连通，可以将 `storage` 替换为 `mgt` ，使用管理网络来连接目标主机。
   > - 如果使用 SSH 方式登录失败，可以执行以下步骤依次关闭节点。
   >
   >   1. 通过 IPMI 管理控制台依次登录集群的每个节点，执行以下命令，停止集群上每个节点的相关服务。
   >
   >      ```
   >      /usr/share/tuna/script/control_all_services.sh --action=stop --group=all
   >      ```
   >   2. 在每个节点中执行以下命令，关闭节点。
   >
   >      `shutdown -h now`
   >
   >      如果执行上述命令关闭节点失败，可以通过在 IPMI 管理控制台关闭主机电源的方式来关闭节点。
3. 启动集群停机维护的相关工作，待工作结束后，重新将节点服务器开机。
4. 在节点上执行以下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

## VMware ESXi 平台

**准备工作**

使用 SSH 方式登录集群的 SMTX OS 节点，执行以下命令，确认 SMTX OS 集群不存在数据恢复。

`zbs-meta pextent find need_recover`

若系统输出 `No PExtents found.`，表示集群不存在数据恢复。

**操作步骤**

1. 通过 VMware vSphere Web Client 登录到 vCenter Server，并浏览到某个 SCVM 所在节点的其他虚拟机（非 SCVM 虚拟机），右键选择**启动** > **关闭客户机操作系统**，关闭虚拟机的操作系统。
2. 参考步骤 1 ，将集群中所有 SCVM 所在节点的其他虚拟机（除了 vCLS 虚拟机）全部关机。对于 vCLS 虚拟机，如果它使用的是 ZBS 数据存储，请将该虚拟机迁移到非 ZBS 数据存储上。
3. 在 vCenter 中选中集群，选择**配置 > 服务 > vSphere 可用性**，在 vSphere 可用性设置界面右侧选择**编辑**，然后在弹出的**编辑集群设置**对话框中关闭 **vSphere HA** 选项。单击**确定**，关闭集群的 HA 功能。
4. 使用 SSH 方式登录集群中的一个 SCVM 节点，执行以下命令，关闭集群所有 SCVM 节点。

   ```
   zbs-cluster shutdown_hosts --hosts=all --action=poweroff --network=storage
   ```

   > **说明：**
   >
   > - 如果存储网络无法连通，可以将 `storage` 替换为 `mgt`，使用管理网络来连接目标 SCVM。
   > - 如果使用 SSH 方式登录失败，可以执行以下步骤依次关闭节点。
   >
   >   1. 通过 vCenter Server 连接并依次登录集群的 SCVM 节点，并在所有 SCVM 节点中执行下述命令停止相关服务。
   >
   >      ```
   >      /usr/share/tuna/script/control_all_services.sh --action=stop --group=all
   >      ```
   >   2. 在 vCenter Server 中浏览到 SCVM 节点，右键选择**启动** > **关闭客户机操作系统**，关闭 SCVM 虚拟机的操作系统。
   >
   >      若 vCenter Server 使用了 SMTX OS 提供的存储，则在执行完前面的步骤后，vCenter Server 将无法正常使用，此时可以登录到 SCVM 所在的 ESXi 节点，手动执行 SCVM 虚拟机关机操作。
5. 参考下述步骤，在 vCenter Server 中依次关闭集群中所有的 ESXi 主机。

   1. 浏览到某个 SCVM 节点所在的 ESXi 主机，右键选择**维护模式** > **进入维护模式**，ESXi 主机进入维护模式。
   2. 选中 ESXi 主机，右键选择**电源** > **关机**，关闭 ESXi 主机的电源。
   > **注意：**
   >
   > 若 vCenter Server 所在的 ESXi 主机也在集群中，建议通过 IPMI 管理台对 ESXi 主机执行关机。
6. 启动集群停机维护的相关工作，待工作结束后，在 vCenter Server 中依次对集群中所有的 ESXi 主机开机。

   > **注意：**
   >
   > 若 vCenter Server 所在的 ESXi 主机也在集群中，建议通过 IPMI 管理台对 ESXi 主机执行开机。
7. 开启 ESXi 主机后，在 vCenter Server 中右键选择**维护模式** > **退出维护模式**，并开启节点所在的 SCVM 虚拟机。
8. 参考此操作开启集群中所有 ESXi 节点中的 SCVM 虚拟机。
9. 在节点上执行以下命令 ，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

---

## 集群 > 管理 Boost 模式 > 启用集群 Boost 模式

# 启用集群 Boost 模式

如 SMTX OS 集群从低版本升级到当前版本或在安装部署时未启用 Boost 模式，升级或部署完成后可以为集群启用 Boost 模式。

**前提条件**

- 集群配置满足启用 Boost 模式的要求，可参考《SMTX OS 特性说明》中 Boost 模式的[配置要求](/smtxos/6.3.0/os_property_notes/os_property_notes_05#%E9%85%8D%E7%BD%AE%E8%A6%81%E6%B1%82)。
- 集群中所有虚拟机已关机。若虚拟机列表中存在未关机的系统服务虚拟机，请参考[关闭和恢复系统服务](/smtxos/6.3.0/aftersales_guide/aftersales_guide_50)章节处理。

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

在脚本执行过程中，输入命令 `tail -f nohup.out` 实时查看日志。若输出结果包含 `Done, enable vhost successfully.`，表示集群 Boost 模式相关配置已开启，需要逐一查看集群中的主机日志： `/var/log/hugepage-manager.log` ，确认 Hugepage 是否正确分配，如果正确分配，则无需重启主机，否则需要重启主机使其生效。

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

## 集群 > 管理 Boost 模式 > 关闭集群 Boost 模式

# 关闭集群 Boost 模式

**前提条件**

集群中所有虚拟机已关机。若虚拟机列表中存在未关机的系统服务虚拟机，请参考[关闭和恢复系统服务](/smtxos/6.3.0/aftersales_guide/aftersales_guide_50)章节处理。

**操作步骤**

在集群任一节点执行如下命令：

`nohup zbs-cluster vhost disable &`

**输出示例**

```
2023-09-06 17:06:38,359 cluster_manager.py 223 [49035] [INFO] Checking current status
2023-09-06 17:06:38,610 cluster_manager.py 176 [49035] [INFO] Start checking vhost status
...
2023-09-06 17:06:39,566 cluster_manager.py 235 [49035] [INFO] Start disable vhost
2023-09-06 17:06:43,551 cmdline.py 185 [49035] [INFO]
2023-09-06 17:06:43,552 cmdline.py 185 [49035] [INFO] PLAY [cluster] *****************************************************************
2023-09-06 17:06:43,552 cmdline.py 185 [49035] [INFO]
2023-09-06 17:12:06,034 cmdline.py 185 [49035] [INFO] PLAY RECAP *********************************************************************
2023-09-06 17:12:06,034 cmdline.py 185 [49035] [INFO] 10.142.74.109              : ok=16   changed=13   unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
2023-09-06 17:12:06,034 cmdline.py 185 [49035] [INFO] 10.142.74.110              : ok=16   changed=13   unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
2023-09-06 17:12:06,038 cmdline.py 185 [49035] [INFO] 10.142.74.111              : ok=16   changed=13   unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
2023-09-06 17:12:06,038 cmdline.py 185 [49035] [INFO] 10.142.74.112              : ok=16   changed=13   unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
2023-09-06 17:12:06,038 cmdline.py 185 [49035] [INFO]
2023-09-06 17:12:07,251 cluster.py 500 [49035] [INFO] Done, disable vhost successfully.
```

**输出说明**

在脚本执行过程中，输入命令 `tail -f nohup.out` 实时查看日志。若输出结果包含 `Done, disable vhost successfully.`，表示集群 Boost 模式已关闭。

---

## 集群 > 激活 TencentOS

# 激活 TencentOS

在基于 TencentOS 操作系统的 SMTX OS 集群部署完成后，需要激活主机的操作系统，以获得腾讯官方的技术支持、安全更新等。您可参考本章节通过在线激活（KMS 激活）或离线激活的方式进行激活。

---

## 集群 > 激活 TencentOS > 在线激活（KMS 激活）

# 在线激活（KMS 激活）

KMS（Key Management Service）激活是一种在线批量激活许可的方式，您可以参考本章节创建 KMS 服务器，并使用 KMS 激活 TencentOS Server 操作系统。当需要激活操作系统的主机数量较多时，建议使用此方式进行激活。

**前提条件**

- 已通过 SmartX 获取的 TencentOS Server 的许可（`tar.gz` 文件）。
- 已根据待激活主机的 CPU 架构获取 KMS 服务器的 OVF 文件（包含 `.ovf` 文件和 `.vmdk` 文件）。

---

## 集群 > 激活 TencentOS > 在线激活（KMS 激活） > 准备工作 > 创建 KMS 服务器

# 创建 KMS 服务器

使用已获取的 OVF 文件，参考《SMTX OS 管理指南》的[导入虚拟机](/smtxos/6.3.0/os_administration_guide/os_administration_guide_019)小节，在待激活的 SMTX OS 集群中创建一台虚拟机作为 KMS 服务器。在为虚拟机配置网络设备时，请选择一个可以与系统服务虚拟机连通的虚拟机网络。

---

## 集群 > 激活 TencentOS > 在线激活（KMS 激活） > 准备工作 > 配置 KMS 服务器

# 配置 KMS 服务器

创建 KMS 服务器后，请使用 root 账户登录 KMS 服务器，然后按照如下步骤进行配置。

1. 根据集群当前网络环境为 KMS 服务器配置 IP。配置完成后，可执行 `ip ad` 命令查看当前 KMS 服务器的 IP 地址。
2. 在本地打开终端命令行工具，使用 scp 命令将许可文件上传到 KMS 服务器上，然后执行如下命令导入许可文件，其中 `license.tar.gz` 为许可文件的文件名。

   ```
   tar zxvf license.tar.gz -C /var/lib/txos
   ```
3. 执行如下命令启动 KMS 服务。

   ```
   systemctl enable txos-kms --now
   ```

   启动 KMS 服务后，可分别执行如下命令查看 KMS 服务状态和 KMS 服务器许可状态。

   - 查看 KMS 服务状态

     ```
     systemctl status txos-kms
     ```

     输出示例如下，如果 `Active` 一行显示为 `active (running)`，说明 KMS 服务已正常启动。

     ```
     systemctl status txos-kms
     txos-kms.service - TencentOS KMS Service
     Loaded: loaded (/etc/systemd/system/txos-kms.service; disabled; vendor preset: disabled)
     Active: active (running) since Tue 2025-04-08 10:44:57 CST; 14min ago
     Process: 1724 ExecStartPre=/usr/bin/txos-admin init-db (code=exited, status=0/SUCCESS)
     Process: 1721 ExecStartPre=/usr/bin/mkdir -p /var/lib/txos (code=exited, status=0/SUCCESS)
     Main PID: 1731 (txos-service)
     Tasks: 7 (limit: 2899)
     Memory: 31.2M
     CGroup: /system.slice/txos-kms.service
             └─1731 /usr/bin/txos-service -w /var/lib/txos -t 5
     ```
   - 查看 KMS 服务器许可状态

     ```
     txos-admin show
     ```

     如果输出如下信息，说明 KMS 服务器许可状态正常。

     ```
     # txos-admin show
     +----------------------------------+------+--------+-------+------+------+---------------------+
     |               kms                | type | period | count | used | free |         time        |
     +----------------------------------+------+--------+-------+------+------+---------------------+
     | 1497994293ae4887a61f5fcd8a05a0ca | TEST |   3    |   2   |  0   |  2   | 2025-04-08 10:44:57 |
     +----------------------------------+------+--------+-------+------+------+---------------------+
     ```

---

## 集群 > 激活 TencentOS > 在线激活（KMS 激活） > 激活 SMTX OS 主机操作系统

# 激活 SMTX OS 主机操作系统

1. 通过 IPMI 管理台或 SSH 登录待激活操作系统的主机。
2. 使用 `sudo` 命令切换到 root 账户，执行如下命令激活操作系统，其中 `KMS_IP` 为已创建 KMS 服务器的 IP 地址。

   ```
   txos-tool set url=$KMS_IP
   txos-tool activate kms
   ```
3. 执行如下命令查看操作系统激活状态，若输出结果中 `status` 字段显示为 `Activated` ，说明操作系统激活成功。

   ```
   txos-tool show
   ```

   输出示例如下：

   ```
   txos-tool show
   url     :       $KMS_IP
   port    :       38400
   kms     :       true
   type    :       COMMERCIAL
   sn      :       AAAAAAAA-BBBBBBBB-CCCCCCCC
   hwid    :       AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB
   reg     :       CCCCCCCC-XXXXXXXX-YYYYYYYY-DDDDDDDD
   time    :       2025-03-12 ~ 2025-06-12
   status  :       Activated
   ```

---

## 集群 > 激活 TencentOS > 离线激活

# 离线激活

若待激活的主机数量较少且无需搭建 KMS 服务器，您可以参考本章节，通过离线激活的方式激活 TencentOS Server 操作系统。

---

## 集群 > 激活 TencentOS > 离线激活 > 准备工作 > 获取主机硬件 ID

# 获取主机硬件 ID

## 通过命令行获取

1. 通过 IPMI 管理台或 SSH 登录待激活操作系统的主机。
2. 使用 `sudo` 命令切换到 root 账户，执行如下命令，输出结果中的 `HW ID` 为该主机的硬件 ID，请记录此 ID。

   ```
   txos-tool pull hwid
   ```

   输出示例如下：

   ```
   txos-tool pull hwid
   ######################################################
   ##              ##  ##      ######  ##              ##
   ##  ##########  ####    ######  ##  ##  ##########  ##
   ##  ##      ##  ######          ######  ##      ##  ##
   ##  ##      ##  ##########          ##  ##      ##  ##
   ##  ##      ##  ####  ####    ##    ##  ##      ##  ##
   ##  ##########  ######          ######  ##########  ##
   ##              ##  ##  ##  ##  ##  ##              ##
   ##################  ##      ##    ####################
   ##    ##    ##  ####      ####  ##  ##  ##########  ##
   ##    ##      ######  ########  ##  ####      ####  ##
   ##  ####  ##      ####    ########  ##  ####  ########
   ####        ####              ##    ##    ######    ##
   ##  ####    ##        ##  ######  ####      ##  ######
   ##  ##  ##  ####  ##  ######  ########              ##
   ##    ####      ####    ####    ##    ####  ##    ####
   ##  ##  ##  ######  ##  ##      ####  ##            ##
   ##  ########    ##  ##  ######              ##      ##
   ##################  ####        ##  ######  ##  ######
   ##              ######        ####  ##  ##    ##    ##
   ##  ##########  ####  ####  ####    ######  ##      ##
   ##  ##      ##  ##    ##  ##  ####          ####    ##
   ##  ##      ##  ##        ##      ######    ##      ##
   ##  ##      ##  ####    ##  ####  ##  ####    ##    ##
   ##  ##########  ##  ####  ##    ####    ##  ####  ####
   ##              ##  ##    ##  ##      ##    ##      ##
   ######################################################
   HW ID: AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB
   ```
3. 参考步骤 1～2，获取其他待激活主机的硬件 ID。

## 通过脚本批量获取

**前提条件**

已获取 TencentOS License 激活脚本并上传至待激活集群中的任一主机。

**操作步骤**

1. 通过 IPMI 管理台或 SSH 登录已上传脚本的主机。
2. 使用 `sudo` 命令切换到 root 账户，执行如下命令获取主机硬件 ID。其中 `hosts_file` 为包含待收集硬件 ID 主机 IP 列表的文件（可自定义文件名，例如 `hosts.txt`）；若不提供此参数，脚本将自动从 Ansible inventory 中收集所有主机的硬件 ID。

   ```
   ./tl3.sh [hosts_file]
   ```

   如需指定待收集硬件 ID 的主机，可在当前主机中创建主机 IP 列表文件，并按照以下格式逐行填写待激活主机的存储 IP。

   ```
   10.0.xx.xx
   10.0.xx.xx
   10.0.xx.xx
   ```
3. 查看输出结果。脚本将按以下格式输出主机存储 IP 及其硬件 ID，并将结果保存至 `/tmp/hw_ids.txt` 文件。

   ```
   10.0.xx.xx, AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB
   10.0.xx.xx, AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB
   10.0.xx.xx, AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB
   ```

   可通过执行如下命令查看收集到的硬件 ID 信息。

   ```
   cat /tmp/activation_results.txt
   ```

---

## 集群 > 激活 TencentOS > 离线激活 > 准备工作 > 获取许可码

# 获取许可码

联系 SmartX 售后工程师，提交所有待激活主机的硬件 ID，获取激活所需的许可码。

---

## 集群 > 激活 TencentOS > 离线激活 > 激活 SMTX OS 主机操作系统

# 激活 SMTX OS 主机操作系统

## 通过命令行激活

1. 通过 IPMI 管理台或 SSH 登录待激活操作系统的主机。
2. 使用 `sudo` 命令切换到 root 账户，执行如下命令激活操作系统，其中 `$LICENSE_CODE` 为已获取的许可码。

   ```
   txos-tool set reg $LICENSE_CODE
   txos-tool activate offline
   ```

   输出示例如下：

   ```
   txos-tool set reg  CCCCCCCC-XXXXXXXX-YYYYYYYY-DDDDDDDD
   txos-tool activate offline
   Activate Success!
   ```
3. 执行如下命令查看操作系统激活状态，若输出结果中 `status` 字段显示为 `Activated`，说明操作系统激活成功。

   ```
   txos-tool show
   ```

   输出示例如下：

   ```
   txos-tool show
   url     :       $KMS_IP
   port    :       38400
   kms     :       false
   type    :       COMMERCIAL
   sn      :       AAAAAAAA-BBBBBBBB-CCCCCCCC
   hwid    :       AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB
   reg     :       CCCCCCCC-XXXXXXXX-YYYYYYYY-DDDDDDDD
   time    :       2025-03-12 ~ 2025-06-12
   status  :       Activated
   ```
4. 参考步骤 1～3 激活其他待激活主机的操作系统。

## 通过脚本批量激活

**前提条件**

已获取 TencentOS License 激活脚本并上传至待激活集群的中任一主机。

**操作步骤**

1. 通过 IPMI 管理台或 SSH 登录已上传脚本的主机。
2. 使用 `sudo` 命令切换到 root 账户，创建 `host_license.txt` 文件，并按以下格式逐行输入待激活主机的存储 IP、硬件 ID 和许可码。

   ```
   10.0.xx.xx, AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB, CCCCCCCC-XXXXXXXX-YYYYYYYY-DDDDDDDD
   10.0.xx.xx, AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB, CCCCCCCC-XXXXXXXX-YYYYYYYY-DDDDDDDD
   10.0.xx.xx, AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB, CCCCCCCC-XXXXXXXX-YYYYYYYY-DDDDDDDD
   ```
3. 执行如下命令激活操作系统。

   ```
   ./tl3.sh --activate host_license.txt
   ```

   执行过程中，脚本将依次激活 `host_license.txt` 文件中列出的主机，并在终端显示每台主机的激活状态，详细的执行日志将输出至 `/tmp/activation_results.txt` 文件。
4. 激活完成后，可通过执行如下命令查看主机激活状态。其中 `hosts_file` 为包含待查询主机 IP 列表的文件（可自定义文件名，例如 `hosts.txt`）；若不提供此参数，脚本将自动从 Ansible inventory 中收集所有主机的硬件 ID。

   ```
   ./tl3.sh -c|--check [hosts_file]
   ```

   如需自定义查看主机列表，可在当前主机创建主机 IP 列表文件，并按照以下格式逐行填写待确认激活状态主机的存储 IP：

   ```
   10.0.xx.xx
   10.0.xx.xx
   10.0.xx.xx
   ```

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台）

# 未启用双活特性的集群转换为双活集群（ELF 平台）

对于未启用双活特性的 SMTX OS（ELF）集群，如需使用本章节提供的方法转化为双活集群，则转化前后必须符合以下要求：

- 现有 SMTX OS（ELF）集群运行正常，并且集群未启用 RDMA 功能和 SR-IOV 特性。
- SMTX OS（ELF）集群不包含使用`纠删码`为冗余策略的 iSCSI Target 和虚拟卷。

  > **说明：**
  >
  > - 若集群包含使用`纠删码`为冗余策略的 iSCSI Target，但 iSCSI Target 内没有虚拟卷或 LUN，可通过 ELF 提供的 API 清理完 iSCSI Target 后，再执行双活集群的转换操作。
  > - 若 SMTX OS（ELF）集群的默认冗余策略为`纠删码`，但集群内不包含使用`纠删码`为冗余策略的虚拟卷，则该集群也支持转换为双活集群。转换后双活集群的默认存储策略为 `3 副本`和`精简制备`。
- 现有 SMTX OS（ELF）集群的所有节点在转化后将全部划分至双活集群的优先可用域。
- 新添加节点与现有 SMTX OS（ELF）集群节点的服务器 CPU 架构和 CPU 供应商完全相同。
- 对于新添加的节点，除其中一个节点被指定为仲裁节点外，其余节点将在转化后全部划分至双活集群的次级可用域。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 集群转化前的准备

# 集群转化前的准备

在集群转化前，必须确认现有的 SMTX OS（ELF）集群和部署的环境已按照如下要求做好了相应的准备，方可启动未启用双活特性的集群至双活集群的转化。

## 硬件及拓扑配置准备

- 现有 SMTX OS（ELF）集群已完成硬件拓扑配置，即所有主机均已分配机箱和机架。

  若当前集群还未配置硬件拓扑，请参考《SMTX OS 管理指南》中的[配置机架拓扑](/smtxos/6.3.0/os_administration_guide/os_administration_guide_167)章节为主机添加机箱和机架。
- 待添加节点（次级可用域节点和仲裁节点）的硬件配置满足《SMTX OS 双活集群安装部署指南（ELF 平台）》中[构建双活集群的要求](/smtxos/6.3.0/elf_multiactive_installation/elf_multiactive_installation_05)构建双活集群的要求。
- SMTX OS 集群支持小容量规格、标准容量规格和大容量规格。如果待转换 SMTX OS（ELF）集群的节点为大容量规格，请确认待添加的节点也为大容量规格；如果待转换集群内存在小容量规格或标准容量规格的节点，请确认待添加的节点为标准容量规格。
- 如果 SMTX OS（ELF）集群为全闪配置且存储介质类型相同，请确认待添加的节点也为全闪配置，并且存储介质类型与当前集群相同。

## 软件准备

- 提前下载当前 SMTX OS（ELF）集群的主机所安装的 ISO 映像文件，要求 SMTX OS ISO 映像文件的版本、CPU 架构和底层操作系统（CentOS 或 openEuler）与原集群完全相同，并且必须为敏捷版、标准版或企业版。
- 部署成双活集群需要单独购买双活的许可。在启动集群转换前，请提前确认软件许可满足要求。

## 待添加节点准备

- 仲裁节点可部署在物理主机或虚拟机中。请提前指定转化后的仲裁节点。
- 建议新添加的次级可用域节点的数量与现有 SMTX OS（ELF）集群中的节点数量完全相同。

## CloudTower 关联准备

若 SMTX OS（ELF）集群已经关联到 CloudTower 上进行管理，在集群转化前，请确保该集群所关联的 CloudTower 存在两个数据中心，分别作为转化后的 SMTX OS（ELF）双活集群的优先可用域所属的数据中心和次级可用域所属的数据中心。若集群转化前未关联 CloudTower，可忽略此要求。

如果 CloudTower 中的数据中心个数少于 2 个，可以在 CloudTower 中提前为转化后的优先可用域和次级可用域分别规划和创建对应的数据中心。在 CloudTower 主界面中单击右上方的 **+ 创建**，选择**创建数据中心**，即可为两个可用域创建新的数据中心。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 规划双活集群网络

# 规划双活集群网络

为了保证转化顺利完成，请提前确认双活集群的网络部署模式，为新添加的节点规划 IP，并同时向网络管理员申请 IP 地址分配表。

## 确认双活集群的网络部署模式

未启用双活特性的 SMTX OS 集群和双活集群均支持网络融合部署和分离部署两种模式。转化前后两个集群的网络部署模式必须完全相同，转化过程中不可修改。

在集群转化前，建议提前确认和记录当前 SMTX OS（ELF）集群所使用的部署模式，并[为次级可用域添加节点](/smtxos/6.3.0/aftersales_guide/aftersales_guide_44)做好准备。

## 为次级可用域的节点和仲裁节点规划 IP

从双活集群的网络拓扑可知，为所有待转化为次级可用域的节点需至少规划两个 IP，分别用于管理网络和存储网络，同时还需提供子网掩码、网关等信息。

转化后的仲裁节点与优先/次级可用域节点的 L2 层或 L3 层存储网络连通，因此需为其规划一个 IP 用于存储网络，以及对应的子网掩码和网关等信息。如果希望转化后的双活集群支持通过 SSH 方式登录仲裁节点，建议为其再配置一个 IP 用于管理网络。

次级可用域的节点和仲裁节点的 IP 地址规划如下表所示。

| 节点名称 | 网络类型 | IP 地址 | 子网掩码 | 网关 | VLAN ID（可选） |
| --- | --- | --- | --- | --- | --- |
| 次级可用域节点 | 管理网络 | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| 存储网络 | xx.xx.xx.xx | xx.xx.xx.xx | - | xx |
| 仲裁节点 | 管理网络（可选） | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | - |
| 存储网络 | xx.xx.xx.xx | xx.xx.xx.xx | - | - |

此外，如果需要 SMTX OS 集成硬件管理能力，还需为每个次级可用域节点和仲裁节点预留 IPMI 管理台 IP。

网络管理员在分配转化后的次级可用域节点和仲裁节点的管理 IP 和存储 IP 时，必须遵循以下规则：

- 节点的 SMTX OS 管理 IP 和存储 IP 不能分配在同一网段。
- 现有 SMTX OS（ELF）集群节点、次级可用域节点和仲裁节点的 SMTX OS 存储 IP 之间可以正常通信。
- 现有 SMTX OS（ELF）集群节点、次级可用域节点和仲裁节点的的 SMTX OS 管理 IP 需要分配在同一网段。
- 若待转化为次级可用域的节点或仲裁节点曾属于其他集群，请勿继续使用原集群中为该节点配置的 SMTX OS 管理 IP 和存储 IP，而应重新规划该节点的 SMTX OS 管理 IP 和存储 IP。
- 上述 IP 地址不能与以下 CIDR 范围内的任何 IP 地址重叠：
  - 169.254.0.0/16
  - 240.0.0.0/4
  - 224.0.0.0/4
  - 198.18.0.0/15
  - 127.0.0.0/8
  - 0.0.0.0/8

## 记录集群的节点信息

- 双活集群的优先可用域和次级可用域必须包含 2 个主节点，因此请为两个可用域分别指定 2 个主节点，并且所有主节点应尽量分布在不同的机架和机箱上，以确保更高的可靠性。
- 记录被添加的节点个数、优先/次级可用域中每个节点的 IP 地址规划信息和主节点的信息，仲裁节点的存储网络信息。同时记录集群里每个节点的服务器序列号。

  > **说明：**
  >
  > 现有 SMTX OS（ELF）集群节点的 IP 地址配置可以通过登录 CloudTower，在左侧导航栏中选中集群的某个主机后，在右侧弹出的主机概览界面中进行查看。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 在新添加的节点中安装 SMTX OS

# 在新添加的节点中安装 SMTX OS

除一个节点须被指定为仲裁节点外，其余新添加的节点均将被划分进入次级可用域，请分别参考对应的内容在节点中安装 SMTX OS 映像文件。

- 对于待转化为次级可用域的节点，参考[在次级可用域节点上安装映像文件](/smtxos/6.3.0/aftersales_guide/aftersales_guide_39)小节完成安装。
- 对于指定的仲裁节点，参考[在仲裁节点上安装映像文件](/smtxos/6.3.0/aftersales_guide/aftersales_guide_40)完成安装。

> **注意**:
>
> 若待添加的次级可用域节点或仲裁节点在转化前已安装 SMTX OS 软件，为避免因历史集群的残留信息或软件版本错误等问题导致添加节点失败，请重新安装 SMTX OS 软件。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 在新添加的节点中安装 SMTX OS > 在次级可用域节点上安装映像文件

# 在次级可用域节点上安装映像文件

在双活集群的次级可用域节点上安装 SMTX OS 与在 SMTX OS 集群节点的安装过程完全相同，请从以下两种安装方式中选择其中一种，安装 SMTX OS。

- [将 SMTX OS 安装在独立的硬 RAID 1 中](/smtxos/6.3.0/aftersales_guide/elf_installation_guide/elf_installation_guide_71)（推荐）
- [将 SMTX OS 安装在软 RAID 1 中](/smtxos/6.3.0/aftersales_guide/elf_installation_guide/elf_installation_guide_25)

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 在新添加的节点中安装 SMTX OS > 在次级可用域节点上安装映像文件 > 将 SMTX OS 安装在独立的硬 RAID 1 中

# 将 SMTX OS 安装在独立的硬 RAID 1 中

1. 重启服务器后，在如下 SMTX OS 的安装引导界面中，选择 **Automatic Installation**。

   ![](https://cdn.smartx.com/internal-docs/assets/5a917abd/elf_installation_guide_28.png)
2. 根据实际规划选择集群节点的容量规格。若选择标准容量规格，请输入字符 1；若选择大容量规格，请输入字符 2。

   ![](https://cdn.smartx.com/internal-docs/assets/5a917abd/elf_installation_guide_29.png)
3. 选择是否将 SMTX OS 安装在两块硬盘上并构成软 RAID 1，请输入 `no`。

   ![](https://cdn.smartx.com/internal-docs/assets/5a917abd/elf_installation_guide_33.png)
4. 系统将自动选择一块硬盘（硬 RAID 1），如果未能找到符合条件的硬盘，或者找到一块以上符合条件的硬盘，请根据**存储设备配置要求**中所规划和记录的 SMTX 系统盘，手动输入该盘的盘符。

   ![](https://cdn.smartx.com/internal-docs/assets/5a917abd/elf_installation_guide_34.png)

   选择完硬盘后，SMTX OS 将会自动安装，安装所需时间与服务器类型和当前网络条件有关。安装完成后，服务器会自动重启。
5. 服务器重启后，用默认账户 `root` 登录 SMTX OS。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 在新添加的节点中安装 SMTX OS > 在次级可用域节点上安装映像文件 > 将 SMTX OS 安装在软 RAID 1 中

# 将 SMTX OS 安装在软 RAID 1 中

1. 重启服务器后，在如下 SMTX OS 的安装引导界面中，选择 **Automatic Installation**。

   ![](https://cdn.smartx.com/internal-docs/assets/5a917abd/elf_installation_guide_28.png)
2. 根据实际规划选择集群节点的容量规格。若选择标准容量规格，请输入字符 1；若选择大容量规格，请输入字符 2。

   ![](https://cdn.smartx.com/internal-docs/assets/5a917abd/elf_installation_guide_29.png)
3. 选择是否将 SMTX OS 安装在两块硬盘上并构成软 RAID 1，请输入 `yes`。

   ![](https://cdn.smartx.com/internal-docs/assets/5a917abd/elf_installation_guide_30.png)
4. 系统将自动选择一块容量在 7 GiB 至 240 GiB 之间的硬盘作为启动盘，如果找到一块以上符合此条件的硬盘，请根据**存储设备配置要求**中所规划的和记录的启动盘，手动输入启动盘的盘符。

   ![](https://cdn.smartx.com/internal-docs/assets/5a917abd/elf_installation_guide_31.png)
5. 系统将自动选择两块硬盘（SSD 优先）构成软 RAID 1，若未找到符合条件的硬盘，或者找到两块以上符合此条件的硬盘，请根据**存储设备配置要求**中所规划和记录的含元数据分区的缓存盘或含元数据分区的数据盘，手动输入该盘的盘符。

   ![](https://cdn.smartx.com/internal-docs/assets/5a917abd/elf_installation_guide_32.png)

   选择完硬盘后，SMTX OS 将会自动安装，安装所需时间与服务器类型和当前网络条件有关。安装完成后，服务器会自动重启。
6. 服务器重启后，用默认账户 `root` 登录 SMTX OS。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 在新添加的节点中安装 SMTX OS > 在仲裁节点上安装映像文件

# 在仲裁节点上安装映像文件

1. 重启服务器，在如下 SMTX OS 安装引导界面中，选择 **Manual Installation**。

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_035.png)
2. 系统将提示选择当前节点的容量规格 `ZBS_SPEC`，默认规格为标准容量规格（`Normal`）。仲裁节点选择使用默认的标准容量规格，请直接输入 **1**，进入下一步。

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_036.png)
3. 系统提示是否准备将 OS 安装在两块硬盘上，其中一块硬盘作为镜像，手动输入 **no**。

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_037.png)
4. 手动输入一块硬盘（容量大于 210 GB）安装引导分区和 OS。

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_038.png)
5. 选择完硬盘后，SMTX OS 系统将会自动安装，安装所需时间与服务器类型和当前网络条件有关。
6. 安装完成后，服务器将会自动重启。重启后使用默认账户 `root` 登录 SMTX OS 系统。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 为次级可用域节点绑定管理网口（启用 LACP）

# 为次级可用域节点绑定管理网口（启用 LACP）

当接入当前 SMTX OS（ELF）集群的管理网络的物理交换机启用了 LACP 动态链路聚合时，为保证转化后的双活集群的管理网络仍然支持 LACP 动态链路聚合，需要在转化前，参考[为待添加节点绑定管理网口](/smtxos/6.3.0/aftersales_guide/os_operation_maintenance/os_operation_maintenance_36)小节进行配置，为转化后的双活集群的每个次级可用域节点绑定管理网口。若当前集群未启用 LACP 动态链路聚合，则请忽略下述操作。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 为次级可用域节点绑定管理网口（启用 LACP） > 为待添加节点绑定管理网口

# 为待添加节点绑定管理网口

仅当连接管理网络的物理交换机启用了 LACP 动态链路聚合时，才需要为待添加节点绑定管理网口，操作步骤如下；否则请忽略。

1. 使用默认账户 `root` 登录待添加节点的 SMTX OS 系统。
2. 执行 `cd /etc/sysconfig/network-scripts/` 命令，进入网口配置文件的访问路径。
3. 使用 `ip a` 命令查看所有网卡的接口信息，再使用 `ethtool <port>` 查看每个网卡接口的速率，以判断出用于管理网络的网口，其中 `<port>` 表示实际网口的名称。

   - 当管理网络和存储网络采用分离部署模式时，**Speed** 显示 1000 Mb/s 及以上的网口可以作为用于管理网络的网口。
   - 当管理网络和存储网络采用融合部署模式时，**Speed** 显示 10000 Mb/s 及以上的网口可以作为用于管理网络和存储网络共用的网口。
4. 在网口配置文件路径下执行以下命令，将用于管理网络的网口绑定为一个网口（名称为 `pre_bond`），并生成 ifcfg-pre\_bond 网口配置文件。

   ```
   network-preconfig create-lacp --nics <nics>
   ```

   其中，`<nics>` 表示需要绑定的网口名称，网口名称之间需用空格隔开，且名称外侧需加引号（"）。例如，当需要绑定网口 eth0 和 eth1 时，则执行 `network-preconfig create-lacp --nics "eth0 eth1"`。

   当输出以下信息时，表明 pre\_bond 网口创建完成，绑定管理网口成功。

   ```
   create lacp bond port success
   ```

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 为次级可用域节点的管理网口配置子接口（配置 VLAN）

# 为次级可用域节点的管理网口配置子接口（配置 VLAN）

当物理交换机为当前 SMTX OS 集群的管理网络配置了 VLAN 时，为保证转化后双活集群的管理网络的连通，需要在转化前，参考[为待添加节点的管理网口配置子接口](/smtxos/6.3.0/aftersales_guide/os_operation_maintenance/os_operation_maintenance_37)小节进行配置，为转化后每个次级可用域节点的管理网口配置子接口；否则请忽略下述配置操作。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 为次级可用域节点的管理网口配置子接口（配置 VLAN） > 为待添加节点的管理网口配置子接口

# 为待添加节点的管理网口配置子接口

仅当物理交换机为管理网络配置了 Trunk VLAN 时，才需要为待添加节点的管理网口配置子接口，操作步骤如下；否则请忽略。

1. 用默认账户 `root` 登录待添加节点的 SMTX OS 系统。
2. 使用 `cd /etc/sysconfig/network-scripts/` 命令，进入网口配置文件的访问路径。
3. 使用 `ip a` 命令查看所有网卡的接口信息，再使用 `ethtool <port>` 查看每个网卡接口的速率，以判断并确定用于管理网络的网口，其中 `<port>` 表示实际网口的名称。

   - 当管理网络和存储网络采用分离部署模式时，**Speed** 显示 1000 Mb/s 及以上的网口可以作为用于管理网络的网口。
   - 当管理网络和存储网络采用融合部署模式时，**Speed** 显示 10000 Mb/s 及以上的网口可以作为用于管理网络和存储网络共用的网口。
4. 在网口配置文件路径下执行以下命令，为网口创建 VLAN 子接口，并配置 IP、网关和子网掩码。

   ```
   network-preconfig create-vlanif --iface <iface> --ipaddr <ipaddr> --netmask <netmask> --gateway <gateway> --vlanid <vlanid>
   ```

   其中，带有 `<>` 符号的字段表示管理网络的参数。

   | 参数 | 说明 |
   | --- | --- |
   | `iface` | 表示网口名称。 - 若待添加节点用于管理网络的网口为 pre\_bond 网口，请替换为 `pre_bond`。 - 若待添加节点用于管理网络的网口不为 pre\_bond 网口，请替换为实际的网口名称，如 `eth0`。 |
   | `ipaddr` | 表示实际规划的 IP 地址。 |
   | `netmask` | 表示实际规划的子网掩码。 |
   | `gateway` | 表示实际规划的网关。 |
   | `vlanid` | 表示实际规划的 VLAN ID。 |

   当输出以下信息时，表明 VLAN 子接口创建完成，管理网口已成功配置子接口。

   ```
   create vlan interface success
   ```

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 检查并设置双活集群部署的环境

# 检查并设置双活集群部署的环境

在次级可用域节点和仲裁节点安装完 SMTX OS 软件后，请根据集群和节点的特点，分别参考以下内容，为次级可用域节点和仲裁节点分别设置部署环境。

- 对于待转化为次级可用域的节点，参考[为优先/次级可用域节点设置部署的环境](/smtxos/6.3.0/aftersales_guide/elf_multiactive_installation/elf_multiactive_installation_36)进行设置。
- 对于指定的仲裁节点，参考[为仲裁节点设置部署的环境](/smtxos/6.3.0/aftersales_guide/aftersales_guide_68)进行设置。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 检查并设置双活集群部署的环境 > 为优先/次级可用域节点设置部署的环境

# 为优先/次级可用域节点设置部署的环境

**注意事项**

当物理交换机为集群的管理网络配置了 VLAN 时，请使用 `root` 账户登录每个优先/次级可用域节点的 SMTX OS 系统，然后从步骤 3 开始执行。

**操作步骤**

1. 使用默认账户 `root` 登录每个优先/次级可用域节点的 SMTX OS 系统，确认用于管理网络和存储网络的网口。

   1. 使用 `cd /etc/sysconfig/network-scripts/` 命令，进入网口配置文件的访问路径。
   2. 使用 `ip a` 命令查看所有网卡的接口信息，再使用 `ethtool <port>` 查看每个网卡接口的速率，以判断并确定用于管理网络和存储网络的网口，其中 `<port>` 表示实际网口的名称。

      - 当管理网络和存储网络采用分离部署模式时，**Speed** 显示 1000 Mb/s 及以上的网口可以作为用于管理网络的网口；**Speed** 显示 10000 Mb/s 及以上的网口可以作为用于存储网络的网口。
      - 当管理网络和存储网络采用融合部署模式时，**Speed** 显示 10000 Mb/s 及以上的网口可以作为用于管理网络和存储网络共用的网口。
2. 确认当前配置路径下是否存在管理网络网口的对应配置文件，如果网口名称是 `ens4f0np0` ，那么预期会存在 `ifcfg-ens4f0np0` 配置文件。如果当前配置路径下不存在管理网络网口的对应配置文件，可以从当前配置路径下已有的其他网口配置文件拷贝后进行修改。如网口名称是 `ens4f0np0` 且配置文件不存在，而当前路径存在 `ifcfg-ens4f0` 配置文件，那么可以执行如下操作来生成网口对应配置文件：

   1. 使用 `cp ifcfg-ens4f0 ifcfg-ens4f0np0` 命令拷贝配置文件。
   2. 使用 `vi ifcfg-ens4f0np0` 命令打开 `ifcfg-ens4f0np0` 配置文件。
   3. 将 `DEVICE=ens4f0` 修改为 `DEVICE=ens4f0np0`。
3. 配置用于管理网络的网口。

   使用 `vi ifcfg-<port>` 命令，打开用于管理网络的网口的配置文件，并进行以下修改，其中 `<port>` 表示该网口的名称。

   1. 修改 **BOOTPROTO=dhcp** 为 **BOOTPROTO=static**
   2. 修改 **ONBOOT=no** 为 **ONBOOT=yes**
   3. 在配置文件末尾添加以下内容：

      ```
      IPADDR=manageIP_address
      NETMASK=manageIP_netmask
      GATEWAY=manageIP_gateway
      ```

      其中 **`manageIP_address`**、**`manageIP_netmask`** 和 **`manageIP_gateway`** 为实际规划的优先/次级可用域节点的 SMTX OS 管理 IP 地址、子网掩码和网关。
4. 为双活集群的部署控制节点配置存储网络的网口。

   使用 `vi ifcfg-<port>` 命令，打开用于存储网络的网口的配置文件，并进行以下修改，其中 `<port>` 表示该网口的名称。

   1. 修改 **BOOTPROTO=dhcp** 为 **BOOTPROTO=static**
   2. 修改 **ONBOOT=no** 为 **ONBOOT=yes**
   3. 在配置文件末尾添加以下内容：

      ```
      IPADDR=control_storageIP_address
      NETMASK=control_storageIP_netmask
      ```

      其中 `control_storageIP_address` 和 `control_storageIP_netmask` 为实际规划的部署控制节点的 SMTX OS 存储 IP 和子网掩码。
5. （可选）在每个节点的 SMTX OS 系统中，执行以下命令，修改主机名称，其中 `<name>` 表示重命名后的主机名称。建议使用辨识度较高的主机名称，从而在部署集群的配置主机时，可以更方便地依据主机名称辨认和勾选集群节点。

   ```
   hostname <name>
   su
   ```
6. 在每个优先/次级可用域节点中执行 `systemctl restart network` 命令，重启服务。
7. 两个可用域中所有节点的网口都配置完成后，测试节点网络，确保节点间的管理网络能够互相连通。
8. 在每个优先/次级可用域节点中执行 `systemctl status nginx` 命令，确认 nginx 服务已启动。
9. 在每个优先/次级可用域节点中执行 `systemctl status zbs-deploy-server` 命令，确认 zbs-deploy-server 服务已启动。
10. 使用 date 命令将节点的时间调整为当前时间，例如 `date -s "2022-11-08 15:21:23"`。在每个优先/次级可用域节点中执行命令后，系统将同步所有节点的时间，避免因集群内节点的时间设置不同步，导致集群无法正常工作。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 检查并设置双活集群部署的环境 > 为仲裁节点设置部署的环境

# 为仲裁节点设置部署的环境

1. 登录仲裁节点的 SMTX OS 系统，确认并设置存储网络和管理网络的网卡、IP 地址和子网掩码等信息。

   1. 使用 **root** 账户登录 SMTX OS 系统，使用 `cd /etc/sysconfig/network-scripts/` 命令，进入配置文件访问路径。
   2. 使用 `ip a` 命令查看所有网卡的接口信息，再使用 `ethtool <port>` 查看每个网卡接口的速率，以判断并确定用于存储网络和管理网络的网口，其中 `<port>` 表示实际网口的名称。

      **Speed** 显示 1000 Mb/s 及以上，表示该网口可设置为存储网络或管理网络的网口。
   3. 配置用于存储网络的网口。

      使用 `vi ifcfg-<port>` 命令，打开用于存储网络的网口的配置文件，并进行以下修改，其中 `<port>` 表示该网口的名称。

      1. 修改 **BOOTPROTO=dhcp** 为 **BOOTPROTO=static**
      2. 修改 **ONBOOT=no** 为 **ONBOOT=yes**
      3. 在配置文件末尾添加以下内容：

         ```
         IPADDR=storageIP_address
         NETMASK=storageIP_netmask
         MACADDR=storageIP_mac
         ```

         其中 **`storageIP_address`**、**`storageIP_netmask`** 和 **`storageIP_mac`** 为实际规划的仲裁节点的 SMTX OS 存储 IP 地址、子网掩码和 MAC 地址。
   4. （可选）若为仲裁节点规划了管理 IP 时，参考下面步骤为其配置用于管理网络的网口。

      使用 `vi ifcfg-<port>` 命令，打开用于管理网络的网口配置文件，并进行以下修改，其中 `<port>` 表示该网口的名称。

      1. 修改 **BOOTPROTO=dhcp** 为 **BOOTPROTO=static**
      2. 修改 **ONBOOT=no** 为 **ONBOOT=yes**
      3. 在配置文件末尾添加以下内容：

         ```
         IPADDR=manageIP_address
         MACADDR=manageIP_mac
         NETMASK=manageIP_netmask       
         GATEWAY=manageIP_gateway
         ```

         其中 **`manageIP_address`**、**`manageIP_mac`**、**`manageIP_netmask`** 和 **`manageIP_gateway`** 为实际规划的仲裁节点的 SMTX OS 管理 IP、管理网卡 MAC 地址、子网掩码和网关。
   5. 执行 `systemctl restart network` 命令，重启服务。
2. 输入 `ping control_storageIP_address` 命令，确认仲裁节点与双活集群两个可用域节点 L2 层存储网络连通。其中 **`control_storageIP_address`** 为双活集群部署控制节点的存储 IP。

   > **注意**：
   >
   > 若仲裁节点与集群两个可用域里的主机 L2 层存储网络无法连通, 请参考[为双活集群配置静态路由](/smtxos/6.3.0/aftersales_guide/aftersales_guide_69)的步骤，手动配置可用域的部署控制节点与仲裁节点间的静态路由，以确保仲裁节点与集群可用域里的部署控制节点之间的存储网络可连通。
3. （可选）输入以下命令，修改主机名称，使主机名称更有辨识度。在部署集群的配置主机阶段，可以根据主机名称辨认集群节点。

   ```
   hostname <name>
   su
   ```
4. 执行命令 `systemctl status nginx`，确认 nginx 服务启动。
5. 执行命令 `systemctl status zbs-deploy-server`，确认 zbs-deploy-server 服务启动。
6. 使用 date 命令将仲裁节点的时间调整为当前时间，例如 `date -s "2022-11-08 15:21:23"`，并确认与可用域节点时间保持一致。
7. （可选）如果仲裁节点安装在虚拟机中，请按照此虚拟机的 Hypervisor 类型自行配置高可用 HA 方案。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 为双活集群配置静态路由（可选）

# 为双活集群配置静态路由（可选）

**前提条件**

在[为仲裁节点设置部署的环境](/smtxos/6.3.0/aftersales_guide/aftersales_guide_68)时，若仲裁节点与集群两个可用域里的主机之间 L2 层存储网络无法连通，此时需要手动配置仲裁节点与优先/次级可用域的节点间的静态路由。

**配置实例**

以下面转换后的双活集群为例，包含优先可用域 IDC A、优先可用域 IDC B 和位于 IDC C 内仲裁节点，IDC C 内的仲裁节点与 IDC A、IDC B 的节点之间 L2 层存储网络不连通，其对应的网络配置如下：

- IDC A 包含 3 个节点，各节点的存储 IP 分别为 `40.0.0.231`、`40.0.0.232` 和 `40.0.0.233`，三个节点到仲裁节点的路由网关为 `40.0.0.253`。
- IDC B 包含 3 个节点，各节点的存储 IP 分别为 `40.0.0.234`、`40.0.0.235` 和 `40.0.0.236`，三个节点到仲裁节点的路由网关为 `40.0.0.254`。
- IDC C 内仲裁节点的存储 IP 为 `10.0.0.1`，IDC C 到 IDC A 可用域网关配置为 `10.0.0.2`，IDC C 到 IDC B 可用域网关配置为 `10.0.0.3`。

以下操作步骤为配置 IDC C 内的仲裁节点与 IDC A、IDC B 的节点之间 L3 层存储网络连通。

**操作步骤**

1. 在优先可用域的 3 个节点上添加到仲裁节点的静态路由。

   1. 使用 **root** 账户登录 SMTX OS 系统, 并在每个节点上执行下述命令，配置临时静态路由。

      ```
      ip route add 10.0.0.1/32 via 40.0.0.253 dev port-storage
      ```
   2. 为了防止网络重启后路由配置丢失，请在优先可用域的每个节点上创建静态路由配置文件 `/etc/sysconfig/network-scripts/route-port-storage`，并写入以下内容：

      ```
      10.0.0.1/32 via 40.0.0.253
      ```
2. 在次级可用域的 3 个节点上添加到仲裁节点的静态路由。

   1. 使用 **root** 账户登录 SMTX OS 系统, 并在每个节点上执行下述命令，配置临时静态路由。

      ```
      ip route add 10.0.0.1/32 via 40.0.0.254 dev port-storage
      ```
   2. 为了防止网络重启后路由配置丢失，请在次级可用域的每个节点上创建静态路由配置文件 `/etc/sysconfig/network-scripts/route-port-storage`，并写入以下内容：

      ```
      10.0.0.1/32 via 40.0.0.254
      ```
3. 在仲裁节点上添加到优先可用域节点和次级可用域节点的静态路由。

   1. 使用 **root** 账户登录仲裁节点的 SMTX OS 系统, 并在节点上创建静态路由配置文件 `/etc/sysconfig/network-scripts/route-eth1`，写入以下内容。其中 `eth1` 为实际仲裁节点的存储网络的网口名称。

      ```
      40.0.0.231/32 via 10.0.0.2
      40.0.0.232/32 via 10.0.0.2
      40.0.0.233/32 via 10.0.0.2
      40.0.0.234/32 via 10.0.0.3
      40.0.0.235/32 via 10.0.0.3
      40.0.0.236/32 via 10.0.0.3
      ```
   2. 执行以下命令，重启网络服务以确保配置生效。

      ```
      systemctl restart network
      ```
4. 登录仲裁节点的 SMTX OS 系统，使用 `ping` 命令确认仲裁节点与两个可用域节点之间的网络可连通。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 为次级可用域添加节点

# 为次级可用域添加节点

为双活集群的次级可用域添加节点时，仅需要对待添加的所有主机进行以下操作。集群级别的设置可自动从原有集群获取，无需重复设置。

**操作步骤**

1. 登录 CloudTower，在左侧导航栏中选中现有集群，进入**概览**界面。在界面右上方选择 **+ 创建** > **添加主机**，进入**添加主机**对话框。您可以选择手动发现主机，或者通过自动扫描来发现主机。

   - **手动发现主机**

     在**主机地址**输入框中输入待添加主机的 IP 或 MAC 地址，单击**添加**可添加多个主机地址，单击**发现主机**按钮进行主机发现。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_002.png)
   - **自动扫描主机**

     您也可以单击**自动扫描**来发现主机，扫描完成后若发现当前网络中存在未添加的主机，界面将显示待添加主机的主机名、IP 地址或 MAC 地址。鼠标悬浮在右侧图标上时，将会显示对应的物理盘和网口信息。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_003.png)

   扫描结束后，若系统在当前网络中尚未发现待添加的主机,则系统将会给出提示,请尝试**重新扫描**或**手动发现**主机进行重新搜索发现。
2. 勾选待添加的主机，单击**下一步**。
3. 在**配置主机**界面，输入待添加节点的主机名称。
4. 为虚拟分布式交换机关联物理网口。可以根据下图中显示的网口速率、连接状态和 MAC 地址等综合判断，选择关联合适的网口。

   - 如果虚拟分布式交换机仅关联一种网络，即集群采用网络分离部署模式，如下图，请给待添加节点选择用于该网络的物理网口。当接入该网络的物理交换机启用了 LACP 动态链路聚合时，需要选择多个网口进行网口绑定。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_050.png)
   - 如果虚拟分布式交换机关联了多种网络，即集群采用网络融合部署模式，如下图，请为待添加的节点选择这些网络共用的物理网口。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_049.png)

     可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网口。当接入这些网络的物理交换机启用了 LACP 动态链路聚合时，需要选择两个网口进行网口绑定。

   当待扩容集群创建了镜像出口网络时，还需要为该网络所属的虚拟分布式交换机关联物理网口。

   > **注意**
   >
   > 新增网口的 MTU 需大于等于此虚拟分布式交换机上关联的所有虚拟网络（包括系统网络及虚拟机网络） MTU 的最大值。若新增的网口不满足上述要求，则需勾选**同时调高关联网口 MTU 至此值**，勾选后系统将自动对相关物理网口进行调整。
5. 填写待添加节点实际规划的管理 IP 和存储 IP。

   ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_052.png)
6. （可选）填写为待添加节点规划的 IPMI IP 信息，以及用户名和密码。

   当待扩容集群创建了镜像出口网络时，还需要为待添加节点配置隧道源 IP。
7. （可选）为待添加节点配置物理盘池。当待添加节点满足多物理盘池的配置要求时，系统会根据节点的存储配置自动选择推荐的物理盘池数量，并分配物理盘及用途，您也可以手动修改物理盘池数量，建议不同节点设置相同的的物理盘池数量。

   **注意**：

   - 单集群最多支持配置 255 个物理盘池。
   - 存储分层模式下：
     - 混闪配置、多种类型 SSD 全闪配置，或单一类型多种属性 SSD 全闪配置，单物理盘池的物理盘数量上限为 64；
     - 单一类型且单一属性 SSD 全闪配置，单物理盘池的物理盘数量上限为 32。
   - 存储不分层模式下：单物理盘池的物理盘数量上限为 32。
   - 单物理盘池的数据盘总容量上限为 256 TB，缓存盘总容量上限为 51 TB，超过容量上限后，将无法添加主机。
8. 指定物理盘的用途和所属物理盘池。

   - **SMTX 系统盘**：不属于任何物理盘池，不可修改用途。
   - **含有元数据分区的缓存盘和含有元数据分区的数据盘**：不可修改用途，可移至其他物理盘池。
   - 其余物理盘：

     存储分层模式部署时：

     - 若待添加节点为混闪配置，一般只有当系统判断的物理盘类型有误时，才需要手动修改用途，可移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为多种类型 SSD 全闪配置，当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**用途修改为**缓存盘**；其余情况下，只有当系统判断的物理盘类型有误时，才需要手动修改物理盘用途。可将物理盘移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为单一类型且多种属性的 SSD 全闪配置，物理盘默认为**数据盘**，需手动将高性能 SSD 的用途修改为**缓存盘**；当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**的用途修改为**缓存盘**。可将物理盘移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为单一类型且单一属性的 SSD 全闪配置，物理盘默认为**数据盘**，无需修改用途，可移至其他物理盘池或选择**不挂载**。

     存储不分层模式部署时：所有物理盘默认为**数据盘**，不可修改用途，可移至其他物理盘池或选择**不挂载**。
9. 为待添加节点统一设置 `root` 账户和 `smartx` 账户的密码。
10. 单击**执行部署**，部署主机。

    开始执行部署后，当前界面将展示部署的总体进度。如果关闭当前窗口，您也可以在任务中心查看部署进度，在对应的任务条目右侧单击 **...** > **查看详情**可以返回**执行部署**界面。

    - 如果部署成功，**执行部署**界面将提示已成功添加主机。

      - 若集群的 SSH 端口号不是 22，界面将提示集群内各主机的 SSH 服务端口号不一致，您需要单击**编辑 ssh 端口号**重新编辑端口并保存，以统一集群中所有主机的 SSH 端口号。
      - 若集群已启用端口访问控制，界面将提示新主机的所有端口允许全部 IP 访问，即新主机不会自动应用端口访问控制中的任何访问限制规则。如需为新主机配置 snmp 服务和 ssh 服务的访问限制，请单击**设置访问控制**，编辑存储网段并保存，然后为新主机的 snmp 服务和 ssh 服务端口设置 IP 白名单，详细操作指导可参考[更新端口访问控制](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_130)章节。
    - 如果部署失败，**执行部署**界面将提示部署失败，需根据界面的具体提示进行下一步操作。

      - 如果界面提示集群无法连接新主机，表明是由于网络配置失败导致部署失败，请参考以下步骤重新添加主机。

        ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_055.png)

        1. 通过 IPMI 管理台 IP 访问待添加主机，调整主机的网络配置。
        2. 在待添加节点中执行如下命令清理主机信息并重启部署服务。

           ```
           zbs-deploy-manage clear_deploy_tag
           systemctl restart zbs-deploy-server nginx
           ```
        3. 在**执行部署**界面单击**添加主机**，然后重新从步骤 1 开始添加主机。
      - 如果界面提示需要清理配置信息，表明网络配置成功，但有其他配置异常导致部署失败，请参考以下步骤重新添加主机。

        1. 在**执行部署**界面单击**查看日志**，根据日志详情定位失败原因，解决问题。
        2. 在**执行部署**界面单击**清理**，以清理添加主机过程中产生的脏数据。

           ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_053.png)

           开始清理后，当前界面将展示清理进度。如果单击**完成**关闭当前窗口，您也可以在任务中心查看清理进度，在对应的任务条目右侧单击 **...** > **查看详情**可以返回**执行部署**界面。

           > **注意**：
           >
           > 如果未及时执行清理，当该任务涉及的主机中存在已添加或正在添加至集群的主机时，请勿再清理此部分数据。
        3. 清理成功后，在**执行部署**界面单击**添加主机**，然后重新从步骤 1 开始添加主机。

           ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_054.png)
11. 在 CloudTower 中确认集群的所有节点添加成功，以及集群运行正常。

    - 主机列表中将新增显示新添加的所有主机的详细信息，且均显示为健康状态。
    - 在集群概览界面中存储容量、主机数量、物理盘个数、CPU 总核数和内存容量均有增加。

> **说明**：
>
> 添加节点后，集群预期会产生主机未配置机架拓扑的报警，请参考[配置机架拓扑](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_139)进行操作。

13. （可选）若集群关联了虚拟专有云网络，需要为新主机添加 TEP IP。可参考《Everoute 虚拟专有云网络管理指南》**管理关联集群**章节中的**编辑关联集群**小节进行添加。
14. （可选）若双活集群配置了单独的业务虚拟机网络，请将新主机关联至该网络所属的虚拟分布式交换机，以保证业务的正常运行，具体请参考《SMTX OS 管理指南》**管理网络**章节中的[编辑虚拟分布式交换机](/smtxos/6.3.0/os_administration_guide/os_administration_guide_108#%E7%BC%96%E8%BE%91%E8%99%9A%E6%8B%9F%E5%88%86%E5%B8%83%E5%BC%8F%E4%BA%A4%E6%8D%A2%E6%9C%BA)小节。
15. （可选）若可用域中的主节点数小于 2，请将可用域中的部分存储节点转换为主节点，直至主节点数为 2。可参考[转换节点角色](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_55)章节进行转换。

    > **注意**：
    >
    > 每次只能对集群中的某一个节点执行角色转换操作，不支持多个节点同时进行转换。

**后续操作**

在为基于 TencentOS 操作系统的 SMTX OS 集群添加完节点后，需要激活新添加主机的操作系统，请联系 SmartX 售后工程师进行激活。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 为集群配置仲裁节点

# 为集群配置仲裁节点

1. 使用 `root` 账号登录现有 SMTX OS（ELF）集群，访问 `/home/smartx/.ssh/smartx_id_rsa.pub` 并获取即将执行集群转换命令的节点（双活转换控制节点）的 ssh 公钥。

   > **注意：**
   >
   > 双活转换控制节点必须为现有 SMTX OS（ELF）集群的某个节点，不可设定为新添加的次级可用域节点或者仲裁节点。
2. 登录仲裁节点, 将步骤 1 中获取的 ssh 公钥写入 `/root/.ssh/authorized_keys` 文件中。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 启动集群转换

# 启动集群转换

**前提条件**

请确保当前集群节点和次级可用域节点分布在不同的机架上。

**准备工作**

若集群在节点开机状态下进行集群转换，则在执行执行集群转换之前，建议您手动将集群内所有虚拟卷的副本数统一提升至 3 副本。否则，转换过程中集群可能会因为 I/O 中断时间过长而引发业务异常。具体操作请参考《管理指南》的[提升集群内虚拟卷的副本数](/smtxos/6.3.0/os_administration_guide/os_administration_guide_093)。

> **说明**：
>
> 若集群在节点停机状态下进行集群转换，则不需要执行此操作，转换过程中集群会自动完成副本数的提升。

**操作步骤**

为集群添加完次级可用域节点和配置仲裁节点后，在双活转换控制节点执行命令 `zbs-cluster convert_to_metro`，将现有集群转换为 SMTX OS（ELF）双活集群。

例如：

```
nohup zbs-cluster convert_to_metro --master_zone_nodes 10.1.79.101,10.1.79.102,10.1.79.103 --master_zone_quorum_nodes 10.1.79.101,10.1.79.102 --slave_zone_nodes 10.1.79.104,10.1.79.105,10.1.79.106 --slave_zone_quorum_nodes 10.1.79.104,10.1.79.105 --witness_ip 10.1.79.100 &
```

上述命令中各参数代表的含义如下，请您根据实际情况进行替换。

| **参数** | **描述** | **备注** |
| --- | --- | --- |
| `master_zone_nodes` | 被转换集群（优先可用域）中所有节点的 SMTX OS 存储 IP | - 每个参数内部的多个 IP 使用英文半角逗号（,）隔开。 - 不同参数之间使用空格进行分隔。 |
| `master_zone_quorum_nodes` | 被转换集群（优先可用域）中两个主节点的 SMTX OS 存储 IP |
| `slave_zone_nodes` | 所有被添加节点（次级可用域）的 SMTX OS 存储 IP |
| `slave_zone_quorum_nodes` | 次级可用域中两个主节点的 SMTX OS 存储 IP |
| `witness_ip` | 仲裁节点的 SMTX OS 存储 IP |

在执行脚本过程中, 可以通过命令 `tailf nohup.out` 实时查看双活集群转换命令日志。当界面显示 `Convert to metro cluster successful.` 时表示该集群转换成功。

> **说明：**
>
> - 若现有集群数据量较大，集群转换时间将会比较长，请耐心等待。
> - 在转换为双活集群过程中，系统会自动为被添加节点（次级可用域）配置硬件拓扑，包括机箱和机架。系统默认机箱为 1U 1 节点。用户可登录 CloudTower 进行修改，但是不可跨可用域更改拓扑。
> - 集群转化完成后，ZBS 将自动将现有存储数据更新为 3 副本，系统启动数据迁移。可以在 CloudTower 中查看集群待迁移数据状态和迁移进展，直至数据迁移全部结束。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 同步仲裁节点的管理 IP

# 同步仲裁节点的管理 IP

若为双活集群的仲裁节点配置管理 IP，或者更新管理 IP 地址后，需要将仲裁节点当前的管理 IP 地址同步至集群中所有主机。

**操作步骤**

登录集群的仲裁节点并执行如下命令，同步仲裁节点的管理 IP：

`zbs-cluster sync_witness_mgt_ip <witness_mgt_ip>`

`<witness_mgt_ip>` 为必选参数，表示仲裁节点的实际管理 IP 地址。

**输出示例**

```
$ zbs-cluster sync_witness_mgt_ip 192.168.31.69
2023-11-20 18:44:05,613 sync_cluster.py 21 [27711] [INFO] no changes, cluster ips up-to-date
2023-11-20 18:44:05,622 ansible_manager.py 160 [27711] [INFO] Exec cmd with ansible: ansible -i /etc/zbs/inventory all -m raw -a 'echo 192.168.31.69 > /etc/zbs/witness_mgt_ip' --ssh-common-args='-o StrictHostKeyChecking=no'
2023-11-20 18:44:05,622 cmdline.py 119 [27711] [INFO] run cmd: ansible -i /etc/zbs/inventory all -m raw -a 'echo 192.168.31.69 > /etc/zbs/witness_mgt_ip' --ssh-common-args='-o StrictHostKeyChecking=no'
2023-11-20 18:44:10,722 cluster.py 582 [27711] [INFO] Sync witness mgt ip 192.168.31.69 to all nodes successfully
```

**后续操作**

若集群在转化前已关联至 CloudTower 上进行管理，请进入下一步 [更新 CloudTower 中双活集群信息](/smtxos/6.3.0/aftersales_guide/aftersales_guide_48)，否则集群转化流程已结束，进入[检查集群转化结果](/smtxos/6.3.0/aftersales_guide/aftersales_guide_49)。

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 更新 CloudTower 中双活集群信息

# 更新 CloudTower 中双活集群信息

如果现有集群在转化前已经关联到 CloudTower 上进行管理，则在转化为 SMTX OS（ELF）双活集群后，还需执行下面的步骤，然后 CloudTower 方可正常展示双活集群的信息。

**准备工作**

- 参照 [CloudTower 关联准备](/smtxos/6.3.0/aftersales_guide/aftersales_guide_36#cloudtower-%E5%85%B3%E8%81%94%E5%87%86%E5%A4%87)小节，在 CloudTower 中提前创建两个数据中心，分别作为转化后的 SMTX OS（ELF）双活集群的优先可用域所属的数据中心和次级可用域所属的数据中心。
- 在浏览器中输入网址 <https://cm.smartx.com/share?code=099df0ea-ff1c-43eb-914b-ca08914b3486>，下载脚本文件 `case-1038067-solution.py`，然后上传至 CloudTower 所在的虚拟机中。

**操作步骤**

1. 访问 CloudTower 所在虚拟机的 VNC，远程登录后，在终端里设置下列环境变量。

   ```
   export TOWER_URL=<CloudTower_IP>
   export TOWER_USERNAME=<CloudTower_username>
   export TOWER_PASSWORD=<CloudTower_password>
   ```

   其中 `<CloudTower_IP>` 表示 CloudTower 的 IP 地址，输入时需要附上 http 或 https 协议开头；`<CloudTower_username>` 和 `<CloudTower_password>` 分别表示登录 CloudTower 的用户名和密码。
2. 在终端里执行命令 `python case-1038067-solution.py`，检查双活集群的可用域数据是否已完成同步。若集群的可用域数据信息需要同步，则终端中会打印出双活集群信息，如下所示。

   ```
   cluster ABC ($cluster_ip1) is stretched but missing zones info.
   cluster 123 ($cluster_ip2) is stretched but missing zones info.
   ...
   ```
3. 在终端里执行命令 `python case-1038067-solution.py -f -p_dc <primary_datacentre> -s_dc <secondary_datacentre>`，同步双活集群里可用域的数据信息。其中 `<primary_datacentre>` 和 `<secondary_datacentre>` 分别表示优先可用域和次级可用域所属的数据中心名称。

   执行上述命令后，终端将依次打印如下内容，表示双活集群里可用域的数据信息已完全同步。

   ```
   cluster ABC ($cluster_ip1) is stretched but missing zones info.
   cluster 123 ($cluster_ip2) is stretched but missing zones info.
   ...
   Update clusters done.
   Upsert zones done.
   ```

---

## 集群 > 未启用双活特性的集群转换为双活集群（ELF 平台） > 检查集群转化结果

# 检查集群转化结果

集群转化结束后，还需参照以下方面进行验证，确认集群转化成功。

1. 登录 CloudTower，检查双活集群各节点服务状态，显示集群运行正常。
2. 在集群的任意节点执行 `zbs-meta pextent find need_recover` 命令，系统返回 `No PExtents found` 信息，表示当前集群不存在未恢复的数据。
3. 登录 CloudTower，在左边导航栏中选择**双活集群**，检查转化后的[双活集群运行信息](/smtxos/6.3.0/os_administration_guide/os_administration_guide_274)，确认信息显示状态和网络连接状态正常。

若按照上述检查内容确认后，发现集群转换失败，请直接联系 SmartX 工程师介入处理。

---

## 集群 > 更换双活集群的优先可用域和次级可用域

# 更换双活集群的优先可用域和次级可用域

SMTX OS 双活集群的优先可用域与次级可用域一般位于同一个城市两个不同地理位置的数据中心，两个可用域都可以完全独立地提供计算和存储服务。双活集群正常工作时业务主要运行在优先可用域上。

在特殊情况下，如果双活集群的优先可用域所处的数据中心存在故障风险，可以对两个可用域进行互换，以保证业务的高可用性。

本章节提供的操作方法适用于采用 SmartX 原生虚拟化 ELF 平台和搭配 VMware ESXi 平台的 SMTX OS 双活集群。

---

## 集群 > 更换双活集群的优先可用域和次级可用域 > 更换优先/次级可用域前的准备

# 更换优先/次级可用域前的准备

在更换优先可用域与次级可用域前，请按照如下要求为集群做好准备。

- 登录 CloudTower，确认当前的 SMTX OS（ELF）双活集群或 SMTX OS (VMware ESXi) 双活集群的[双活拓扑状态](/smtxos/6.3.0/os_administration_guide/os_administration_guide_273)和[集群运行状态](/smtxos/6.3.0/os_administration_guide/os_administration_guide_274)处于正常。
- 记录集群优先可用域和次级可用域里每个主机所在的机箱和机架信息。
- 重新规划集群，明确新的优先/次级可用域中每个主机在机箱和机架的具体位置。

---

## 集群 > 更换双活集群的优先可用域和次级可用域 > 调整优先/次级可用域里机架和机箱的位置

# 调整优先/次级可用域里机架和机箱的位置

在 CloudTower 和数据中心机房现场调整优先/次级可用域里机架和机箱的位置时，要求必须提前做好新的集群规划，明确调整后双活集群的每个主机在对应可用域内的存放位置。

**操作步骤**

1. 在 CloudTower 主界面的左侧导航栏中选中双活集群，在右侧的管理界面中选择**全部 > 机架配置**，进入机架配置界面。
2. 参考《SMTX OS 管理指南》中的[调整机架拓扑](/smtxos/6.3.0/os_administration_guide/os_administration_guide_168)小节，将位于优先可用域的机架中的机箱依次移动到规划的目标机架和机架位置上。

   > **说明：**
   >
   > 如果待存放移动后机箱的目标机架已无可用空间，您可以在可用域中先增加机架，然后再移动机箱的位置。
3. 参考步骤 2 ，将位于次级可用域的机架中的机箱依次移动到规划的目标机架和机架位置上。

**后续操作**

双活集群在配置时要求必须启用 SMTX OS 的机架拓扑感知功能，不仅在部署时要考虑尽量将服务器平均分布在不同的机架中，在管理集群时还要求在 CloudTower 中如实呈现数据中心机房现场的主机与机架的位置和拓扑结构。

因此，在 CloudTower 中按照新的集群规划调整优先/次级可用域里机架和机箱的位置后，我们建议您分别在优先可用域和次级可用域的数据中心机房，将每个可用域的主机按照规划的位置摆放在机箱和机架中，以保证 CloudTower 与实际数据中心机房现场的网络拓扑一致。

---

## 集群 > 更换双活集群的优先可用域和次级可用域 > 调整可用域中主机或 SCVM 的 Meta 服务优先级

# 调整可用域中主机或 SCVM 的 Meta 服务优先级

更换 SMTX OS（ELF）双活集群的主机或者 SMTX OS (VMware ESXi) 双活集群的 SCVM 节点所在的可用域后，还需要对每个主机或 SCVM 的 Meta 服务的优先级重新进行配置，以保证主机或 SCVM 内 Meta 服务的优先级与集群的规划完全相同。

**操作步骤**

1. 登录集群的主机或 SCVM，执行 `$cat /etc/zbs/zbs.conf` 命令查看配置文件。通过其 `members` 字段查找各 SMTX OS 节点的 IP 地址列表。

   ```
   [root@node34 09:09:46 ~]$cat /etc/zbs/zbs.conf 
   [network]
   data_ip=10.0.73.34
   heartbeat_ip=10.0.73.34
   vm_ip=192.168.67.34
   web_ip=192.168.67.34

   [cluster]
   role=storage
   members=10.0.73.35,10.0.73.36,10.0.73.37,10.0.73.38
   zookeeper=10.0.73.35:2181,10.0.73.36:2181,10.0.73.37:2181,10.0.73.38:2181,10.0.73.95:2181
   mongo=10.0.73.35:27017,10.0.73.36:27017,10.0.73.37:27017,10.0.73.38:27017,10.0.73.95:2701
   ```
2. 配置主机或 SCVM 的 Meta 服务优先级。

   根据可用域拓扑配置，`members` 中位于优先可用域的节点，其优先级为 2；位于次级可用域的节点，其优先级为 1。若准备将 `10.0.73.35` 和 `10.0.73.36` 配置在优先可用域，`10.0.73.37` 和 `10.0.73.38` 配置在次级可用域，则可以通过执行以下命令实现：

   `$zbs-tool service set_priority meta 10.0.73.35:10100:2,10.0.73.36:10100:2,10.0.73.37:10100:1,10.0.73.38:10100:1`

   查看主机或 SCVM 的优先级配置结果。

   ```
   $zbs-tool service show meta
   -------------------------------------------------------------------------
   Name               meta
   Members            ['10.0.73.35:10100', '10.0.73.36:10100', '10.0.73.37:10100', '10.0.73.38:10100']
   Leader             10.0.73.35:10100
   Specified members  ['10.0.73.37:10100', '10.0.73.38:10100', '10.0.73.35:10100', '10.0.73.36:10100']
   Priority           10.0.73.37:10100:1,10.0.73.38:10100:1,10.0.73.35:10100:2,10.0.73.36:10100:2
   -------------------------------------------------------------------------
   ```

   配置完成后，Meta Leader 将始终在活跃节点里优先级较高的节点中产生。

---

## 集群 > 更换双活集群的优先可用域和次级可用域 > 检查更换可用域后的集群状态

# 检查更换可用域后的集群状态

登录 CloudTower，参照下面的操作和要求，重新查看更换操作结束后集群的运行情况，确认集群处于正常状态。

---

## 集群 > 更换双活集群的优先可用域和次级可用域 > 检查更换可用域后的集群状态 > 查看优先/次级可用域

# 查看优先/次级可用域

双活集群的硬件和虚拟机（ELF 平台）可归属于特定的可用域，因此除了支持在集群层级对这些资源进行管理外，还可以在可用域层级查看和管理这些资源。

在 CloudTower 左侧导航栏中选中数据中心下的**优先可用域**或者**次级可用域**，可以查看可用域内的硬件和虚拟机（ELF 平台）详情。

---

## 集群 > 更换双活集群的优先可用域和次级可用域 > 检查更换可用域后的集群状态 > 查看双活拓扑状态

# 查看双活拓扑状态

为了能清晰直观地了解双活集群的状态，CloudTower 提供双活状态显示功能。

在双活集群中可以单击**双活状态**进入详情界面，将展示以下拓扑状态信息：

- 双活集群组件及资源信息，例如可用域内主机数量、虚拟机数量（ELF 平台）；
- 双活集群健康状态：展示各组件的健康状况，如有报警信息，将展示在状态图上；
- 双活组件运行信息：单击组件后，在弹出的概览页面中查看组件在[双活集群运行信息](/smtxos/6.3.0/os_administration_guide/os_administration_guide_274)。

当集群出现异常时，拓扑状态图会实时变更，并及时提示用户查看。

---

## 集群 > 更换双活集群的优先可用域和次级可用域 > 检查更换可用域后的集群状态 > 查看双活集群运行信息

# 查看双活集群运行信息

查看双活集群的运行信息时，还需包含对双活的健康检查，这依赖于 SMTX OS 的报警监控服务，其判断标准与未启用双活特性的集群完全相同。而可用域的具体情况，可以在可用域级别的资源中查看，信息更丰富。

**操作步骤**

1. 在双活集群界面单击**双活状态**页签。
2. 选择以下组件及网络连接，在弹出的概览页面中查看集群中可用域和节点的基本信息和监控信息，可用域间的网络流量，以及仲裁节点与可用域间 ping 状态。

   | 组件/网络连接 | 查看项目 | 具体信息 |
   | --- | --- | --- |
   | 优先/次级可用域 | 基本信息 | 主机/虚拟机数量  活跃分配 vCPU/内存  所属数据中心  运行中/暂停的虚拟机数量  总存储空间  已使用/失效/空闲存储 |
   | 仲裁节点 | 基本信息 | IP 地址  CPU 分配  内存分配  系统总空间  系统已使用/空闲空间 |
   | 监控信息 | 两小时内，节点的 CPU 使用率及内存使用率 |
   | 可用域之间的网络 | 网络流量 | 优先可用域至次级可用域的网络流量  次级可用域至优先可用域的网络流量 |
   | 仲裁节点与可用域间的网络 | Ping 状态 | 仲裁节点到优先可用域/次级可用域的最差往返延时  优先可用域/次级可用域到仲裁节点的最差往返延时 |
3. 检查可用域的运行状态，以及优先可用域与次级可用域之间，仲裁节点与可用域之间的网络连接状态，并关注和处理注意或告警信息，及时恢复集群的健康运行状态。

   | 组件/网络连接 | 健康检查项目 | 具体信息 |
   | --- | --- | --- |
   | 优先/次级可用域 | 可用域内存资源 | 展示在当前可用域整体失效时，另一可用域的空闲内存资源是否足以承载当前正在运行和暂停的虚拟机。  - **健康**：空闲内存资源足够，完全可以承载。 - **注意**：空闲内存资源不足，无法支持所有正在运行和暂停的虚拟机。 |
   | 可用域总数据空间 | 展示在当前可用域整体失效时，另一可用域的数据空间是否足以恢复当前全部数据至 3 副本。  - **健康**：数据空间足够，完全可以支持恢复数据至 3 副本。 - **注意**：数据空间不足，无法支持当前全部数据恢复至 3 副本。 - **严重警告**：数据空间严重不足，无法支持当前全部数据恢复至 2 副本。 |
   | 可用域内主机的系统时间 | 展示当前可用域内所有主机的系统时间与集群的系统时间相差是否超过 3 秒。  - **健康**：系统时间差均不超过 3 秒。 - **严重警告**：存在部分主机的系统时间与集群的系统时间相差超过 3 秒，需特别关注。 |
   | 可用域内主机电源状态 | 展示当前可用域内所有主机的电源状态。  - **健康**：所有主机均处于开机状态。 - **注意**：部分主机处于断电状态。 |
   | 可用域内主机工作状态 | 展示当前可用域内所有主机的工作状态。  - **健康**：所有主机均处于运行中状态。 - **严重警告**：部分主机的工作状态未知。 |
   | 可用域内主机存储健康状态 | 展示当前可用域内所有主机存储服务的健康状态。  - **健康**：所有主机的存储服务可用。 - **严重警告**：部分主机的存储服务异常。 |
   | 可用域内主节点 zbs-metad 服务、zookeeper 服务和 mongod 服务的运行状态 | 展示当前可用域内主节点 zbs-metad 服务、zookeeper 服务和 mongod 服务是否正在运行。  - **健康**：所有主节点 zbs-metad 服务、zookeeper 服务和 mongod 服务正在运行中。 - **严重警告**：部分主节点 zbs-metad 服务、zookeeper 服务或 mongod 服务未运行。 |
   | 仲裁节点 | 仲裁节点的工作状态 | 展示仲裁节点的工作状态。  - **健康**：仲裁节点处于运行中状态。 - **严重警告**：仲裁节点的工作状态未知。 |
   | 仲裁节点的系统时间 | 展示仲裁节点的系统时间与集群的系统时间相差是否超过 3 秒。  - **健康**：系统时间差不超过 3 秒。 - **严重警告**：系统时间差超过 3 秒，需特别关注。 |
   | 仲裁节点的内部服务 mongod、zookeeper、ntpd 和 master-monitor 的运行状态 | 展示仲裁节点的 mongod 服务、zookeeper 服务、ntpd 服务和 master-monitor 服务是否正在运行。  - **健康**：仲裁节点的 mongod 服务、zookeeper 服务、ntpd 服务和 master-monitor 服务正在运行中。 - **严重警告**：仲裁节点的 mongod 服务、zookeeper 服务、ntpd 服务或 master-monitor 服务未运行。 |
   | 仲裁节点的 CPU 使用率 | 展示仲裁节点的 CPU 使用率及其持续时间。  - **健康**：仲裁节点的 CPU 使用率未超过 80%，或者 CPU 使用率虽超过 80%，但其持续时间不超过 5 分钟。 - **注意**：仲裁节点的 CPU 使用率超过 80%，且持续时间超过 5 分钟。 - **严重警告**：仲裁节点的 CPU 使用率超过 90%，且持续时间超过 5 分钟。 |
   | 仲裁节点的内存使用率 | 展示仲裁节点的内存使用率及其持续时间。  - **健康**：仲裁节点的内存使用率未超过 80%，或者内存使用率虽超过 80%，但其持续时间不超过 5 分钟。 - **注意**：仲裁节点的内存使用率超过 80%，且持续时间超过 5 分钟。 - **严重警告**：仲裁节点的内存使用率超过 90%，且持续时间超过 5 分钟。 |
   | 仲裁节点的系统空间使用率 | 展示仲裁节点的系统空间使用率是否超过 90%。  - **健康**：仲裁节点的系统空间使用率未超过 90%。 - **注意**：仲裁节点的系统空间使用率已超过 90%。 |
   | 可用域之间的网络 | 可用域之间的最差往返延时 | 展示在 5 分钟内，当前可用域的主机到另一可用域的主机的最差往返延时的平均值。  - **健康**：在 5 分钟内，当前可用域的任一主机到另一可用域的任一主机的最差往返延时的平均值不超过 10 毫秒。 - **信息**：在 5 分钟内，当前可用域的任一主机到另一可用域的任一主机的最差往返延时的平均值已超过 10 毫秒。 - **注意**：在 5 分钟内，当前可用域的任一主机到另一可用域的任一主机的最差往返延时的平均值已超过 200 毫秒。 - **严重警告**：在 5 分钟内，当前可用域的任一主机到另一可用域的任一主机的最差往返延时的平均值已超过 2 秒。 |
   | 可用域之间的网络连接 | 展示优先可用域与次级可用域之间的存储网络连接是否正常。  - **健康**：优先可用域与次级可用域之间的存储网络连接正常。 - **严重警告**：优先可用域与次级可用域之间的存储网络连接异常。 |
   | 仲裁节点与可用域之间的网络 | 仲裁节点与可用域之间的最差往返延时 | 展示在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值。  - **健康**：在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值不超过 10 毫秒。 - **信息**：在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值已超过 10 毫秒。 - **注意**：在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值已超过 200 毫秒。 - **严重警告**：在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值已超过 2 秒。 |
   | 仲裁节点与可用域之间的网络连接 | 展示仲裁节点与优先可用域之间，以及仲裁节点与次级可用域之间的存储网络连接是否正常。  - **健康**：仲裁节点与优先可用域之间，以及仲裁节点与次级可用域之间的存储网络连接正常。 - **严重警告**：仲裁节点与优先可用域之间，或者仲裁节点与次级可用域之间的存储网络连接异常。 |

---

## 集群 > 重建双活集群的仲裁节点

# 重建双活集群的仲裁节点

当 SMTX OS（ELF）双活集群或 SMTX OS（VMware ESXi）双活集群的的仲裁节点发生不可恢复的故障并下线后，需要通过一台新的物理机或虚拟机重建仲裁节点，以保证双活集群继续运行和提供服务。

---

## 集群 > 重建双活集群的仲裁节点 > 检查双活集群的状态

# 检查双活集群的状态

登录 CloudTower，在左侧导航栏中选中双活集群，进入**概览**界面，查看当前双活集群的状态。预期**双活状态**卡片中仅显示仲裁节点存在故障，而优先可用域和次级可用域的所有主机显示为`健康`状态（如下图所示）。

![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_039.png)

---

## 集群 > 重建双活集群的仲裁节点 > 清理故障仲裁节点

# 清理故障仲裁节点

在 CloudTower 中确认双活集群的状态后，登录双活集群的主机或 SCVM，获取仲裁节点信息并将该故障节点从双活集群中清除。

**注意事项**

在执行清理仲裁节点的命令前，请务必确认仲裁节点已经发生故障且无法恢复。

**操作步骤**

1. 登录双活集群的优先可用域或次级可用域的任一节点，执行如下命令，获取并记录当前双活集群的仲裁节点信息（`Witness uuid` 和 `Witness ip`）。

   ```
   zbs-deploy-manage witness get
   ```
2. 获取仲裁节点信息后，执行如下命令，清理原来故障仲裁节点的信息，从双活集群中移除该仲裁节点。

   ```
   nohup zbs-deploy-manage witness remove --witness_ip <witness_ip> &
   tail -f nohup.out
   ```

   执行上述命令后，系统会同时对部分服务的配置进行更新，大约需要 10 分钟左右。您可以通过观察屏幕中的日志输出来确认当前状态。

   若移除仲裁节点成功，则日志将会显示如下：

   ```
   2023-05-23 15:56:24,509 INFO _session_callback: Zookeeper connection lost
   2023-05-23 15:56:24,509 INFO _session_callback: Zookeeper session closed, state: CLOSED
   2023-05-23 15:56:24,510 INFO witness_remove: Remove witness node 10.0.0.1 successfully
   ```

**操作结果**

移除故障的仲裁节点后，该双活集群的状态在 CloudTower 界面中可能显示为以下两种：

- 未启用双活特性的集群
- 双活集群，集群为`健康`状态

以上两种状态均符合当前场景（仲裁节点重建前）的预期，后续完成仲裁节点的重建后，双活集群的状态将会恢复正常。

---

## 集群 > 重建双活集群的仲裁节点 > 重建仲裁节点

# 重建仲裁节点

1. 下载当前 SMTX OS 双活集群的主机所安装的 ISO 映像文件，并在新的仲裁节点完成安装。

   - ELF 平台

     参考《SMTX OS 双活集群安装部署指南（ELF 平台）》中的[在仲裁节点上安装映像文件](/smtxos/6.3.0/elf_multiactive_installation/elf_multiactive_installation_30)小节进行安装。
   - VMware ESXi 平台

     参考《SMTX OS 双活集群安装部署指南（VMware ESXi 平台）》中的[在仲裁节点安装 SMTX OS 软件](/smtxos/6.3.0/vmware_multiactive_installation/vmware_multiactive_installation_34)小节进行安装。
2. 为仲裁节点设置部署前的环境。

   - ELF 平台

     参考《SMTX OS 双活集群安装部署指南（ELF 平台）》中的[为仲裁节点设置部署的环境](/smtxos/6.3.0/elf_multiactive_installation/elf_multiactive_installation_37)小节进行安装。
   - VMware ESXi 平台

     参考《SMTX OS 双活集群安装部署指南（VMware ESXi 平台）》中的[为仲裁节点设置部署的环境](/smtxos/6.3.0/vmware_multiactive_installation/vmware_multiactive_installation_38)小节进行安装。
   > **说明：**
   >
   > - 为仲裁节点设置部署的环境时，您需要指定重建的仲裁节点的存储 IP。
   > - 重建的仲裁节点的存储 IP 的子网掩码需根据双活集群的实际情况指定。
3. （可选）若仲裁节点与两个可用域的主机 L3 层存储网络连通，而不是 L2 层网络连通时，需要在仲裁节点上配置到两个可用域的静态路由，其路由配置文件需根据双活集群的实际网络规划信息进行设置。

   例如，以仲裁节点的存储网卡 `eth1` 作为示例，仲裁节点通过网关 `10.0.0.2` 路由到优先可用域的三个节点（`10.0.77.101 ~ 103`），仲裁节点通过网关 `10.0.0.3` 路由到次级可用域的三个节点(`10.0.77.104 ~ 106`)。

   ![](https://cdn.smartx.com/internal-docs/assets/e1ccc446/aftersales_guide_040.png)

---

## 集群 > 重建双活集群的仲裁节点 > 为双活集群主机配置静态路由（可选）

# 为双活集群主机配置静态路由（可选）

如果重建的仲裁节点与双活集群内优先/次级可用域的主机之间 L3 层网络连通，则需要更新集群内所有主机的静态路由信息。

以下为配置示例，其中优先可用域节点通过网关 `10.0.77.253` 路由到仲裁节点，次级可用域节点通过 `10.0.77.254` 网关路由到仲裁节点。

```
[root@node1 16:30:00 smartx]$zbs-deploy-manage witness config-static-routes --help
Usage: zbs-deploy-manage witness config-static-routes [OPTIONS]

  config cluster nodes static routes

Options:
  --witness_ip TEXT               witness node ip  [required]
  --master_to_witness_gateway TEXT
                                  master node to witness node gateway
                                  [required]
  --slave_to_witness_gateway TEXT
                                  master node to witness node gateway
                                  [required]
  --help                          Show this message and exit.
[root@node1 16:30:06 smartx]$zbs-deploy-manage witness config-static-routes --witness_ip 10.0.0.11 --master_to_witness
_gateway 10.0.77.253 --slave_to_witness_gateway 10.0.77.254
```

若配置静态路由成功，则日志显示如下：

```
2023-05-23 16:31:07,204 INFO witness_config_static_routes: Config static routes successfully
```

---

## 集群 > 重建双活集群的仲裁节点 > 添加重建的仲裁节点至双活集群

# 添加重建的仲裁节点至双活集群

在仲裁节点完成基本配置后，可以通过以下命令将仲裁节点添加到双活集群中。

以下为配置示例，其中 `–witness_uuid` 是清理故障仲裁节点时获取的仲裁节点 UUID 信息（`Witness uuid`），即 `44a51c2a-f095-11ed-b46d-52540062a4cf`。

```
nohup zbs-deploy-manage witness add --witness_uuid 44a51c2a-f095-11ed-b46d-52540062a4cf --witness_ip 10.0.0.11 &
tail -f nohup.out
```

若重建的仲裁节点成功添加至双活集群，则日志显示如下：

```
2023-05-23 16:39:34,144 INFO witness_add: Add witness node 10.0.0.11 successfully
```

---

## 集群 > 重建双活集群的仲裁节点 > 同步仲裁节点的管理 IP

# 同步仲裁节点的管理 IP

若为双活集群的仲裁节点配置管理 IP，需要将仲裁节点当前的管理 IP 地址同步至双活集群中所有主机。

**操作步骤**

登录集群的仲裁节点并执行如下命令，同步仲裁节点的管理 IP：

`zbs-cluster sync_witness_mgt_ip <witness_mgt_ip>`

`<witness_mgt_ip>` 为必选参数，表示仲裁节点的实际管理 IP 地址。

**输出示例**

```
$ zbs-cluster sync_witness_mgt_ip 192.168.31.69
2023-11-20 18:44:05,613 sync_cluster.py 21 [27711] [INFO] no changes, cluster ips up-to-date
2023-11-20 18:44:05,622 ansible_manager.py 160 [27711] [INFO] Exec cmd with ansible: ansible -i /etc/zbs/inventory all -m raw -a 'echo 192.168.31.69 > /etc/zbs/witness_mgt_ip' --ssh-common-args='-o StrictHostKeyChecking=no'
2023-11-20 18:44:05,622 cmdline.py 119 [27711] [INFO] run cmd: ansible -i /etc/zbs/inventory all -m raw -a 'echo 192.168.31.69 > /etc/zbs/witness_mgt_ip' --ssh-common-args='-o StrictHostKeyChecking=no'
2023-11-20 18:44:10,722 cluster.py 582 [27711] [INFO] Sync witness mgt ip 192.168.31.69 to all nodes successfully
```

---

## 集群 > 重建双活集群的仲裁节点 > 在 CloudTower 中确认双活集群的状态

# 在 CloudTower 中确认双活集群的状态

访问 CloudTower 所在虚拟机的 VNC，远程登录后，在终端里执行以下命令，CloudTower 将主动更新双活集群信息，其中 `$url` 为 CloudTower 的 IP 地址，并且需要携带权限信息，例如 `admin:cloudtower@192.168.31.126`。如果 CloudTower 使用域名，需要确保双活集群节点可以正确解析 CloudTower 域名。

```
curl "https://$url/api/admin/execute-task?key=UPSERT_WITNESS" -k
curl "https://$url/api/admin/execute-task?key=UPSERT_ZONE" -k
curl "https://$url/api/admin/execute-task?key=UPDATE_CLUSTER" -k
```

登录 CloudTower，并在左侧导航栏中选中双活集群，进入**概览**界面，参考如下步骤，检查集群的运行情况，确认集群处于正常状态。

---

## 集群 > 重建双活集群的仲裁节点 > 查看优先/次级可用域

# 查看优先/次级可用域

双活集群的硬件和虚拟机（ELF 平台）可归属于特定的可用域，因此除了支持在集群层级对这些资源进行管理外，还可以在可用域层级查看和管理这些资源。

在 CloudTower 左侧导航栏中选中数据中心下的**优先可用域**或者**次级可用域**，可以查看可用域内的硬件和虚拟机（ELF 平台）详情。

---

## 集群 > 重建双活集群的仲裁节点 > 查看双活拓扑状态

# 查看双活拓扑状态

为了能清晰直观地了解双活集群的状态，CloudTower 提供双活状态显示功能。

在双活集群中可以单击**双活状态**进入详情界面，将展示以下拓扑状态信息：

- 双活集群组件及资源信息，例如可用域内主机数量、虚拟机数量（ELF 平台）；
- 双活集群健康状态：展示各组件的健康状况，如有报警信息，将展示在状态图上；
- 双活组件运行信息：单击组件后，在弹出的概览页面中查看组件在[双活集群运行信息](/smtxos/6.3.0/os_administration_guide/os_administration_guide_274)。

当集群出现异常时，拓扑状态图会实时变更，并及时提示用户查看。

---

## 集群 > 重建双活集群的仲裁节点 > 查看双活集群运行信息

# 查看双活集群运行信息

查看双活集群的运行信息时，还需包含对双活的健康检查，这依赖于 SMTX OS 的报警监控服务，其判断标准与未启用双活特性的集群完全相同。而可用域的具体情况，可以在可用域级别的资源中查看，信息更丰富。

**操作步骤**

1. 在双活集群界面单击**双活状态**页签。
2. 选择以下组件及网络连接，在弹出的概览页面中查看集群中可用域和节点的基本信息和监控信息，可用域间的网络流量，以及仲裁节点与可用域间 ping 状态。

   | 组件/网络连接 | 查看项目 | 具体信息 |
   | --- | --- | --- |
   | 优先/次级可用域 | 基本信息 | 主机/虚拟机数量  活跃分配 vCPU/内存  所属数据中心  运行中/暂停的虚拟机数量  总存储空间  已使用/失效/空闲存储 |
   | 仲裁节点 | 基本信息 | IP 地址  CPU 分配  内存分配  系统总空间  系统已使用/空闲空间 |
   | 监控信息 | 两小时内，节点的 CPU 使用率及内存使用率 |
   | 可用域之间的网络 | 网络流量 | 优先可用域至次级可用域的网络流量  次级可用域至优先可用域的网络流量 |
   | 仲裁节点与可用域间的网络 | Ping 状态 | 仲裁节点到优先可用域/次级可用域的最差往返延时  优先可用域/次级可用域到仲裁节点的最差往返延时 |
3. 检查可用域的运行状态，以及优先可用域与次级可用域之间，仲裁节点与可用域之间的网络连接状态，并关注和处理注意或告警信息，及时恢复集群的健康运行状态。

   | 组件/网络连接 | 健康检查项目 | 具体信息 |
   | --- | --- | --- |
   | 优先/次级可用域 | 可用域内存资源 | 展示在当前可用域整体失效时，另一可用域的空闲内存资源是否足以承载当前正在运行和暂停的虚拟机。  - **健康**：空闲内存资源足够，完全可以承载。 - **注意**：空闲内存资源不足，无法支持所有正在运行和暂停的虚拟机。 |
   | 可用域总数据空间 | 展示在当前可用域整体失效时，另一可用域的数据空间是否足以恢复当前全部数据至 3 副本。  - **健康**：数据空间足够，完全可以支持恢复数据至 3 副本。 - **注意**：数据空间不足，无法支持当前全部数据恢复至 3 副本。 - **严重警告**：数据空间严重不足，无法支持当前全部数据恢复至 2 副本。 |
   | 可用域内主机的系统时间 | 展示当前可用域内所有主机的系统时间与集群的系统时间相差是否超过 3 秒。  - **健康**：系统时间差均不超过 3 秒。 - **严重警告**：存在部分主机的系统时间与集群的系统时间相差超过 3 秒，需特别关注。 |
   | 可用域内主机电源状态 | 展示当前可用域内所有主机的电源状态。  - **健康**：所有主机均处于开机状态。 - **注意**：部分主机处于断电状态。 |
   | 可用域内主机工作状态 | 展示当前可用域内所有主机的工作状态。  - **健康**：所有主机均处于运行中状态。 - **严重警告**：部分主机的工作状态未知。 |
   | 可用域内主机存储健康状态 | 展示当前可用域内所有主机存储服务的健康状态。  - **健康**：所有主机的存储服务可用。 - **严重警告**：部分主机的存储服务异常。 |
   | 可用域内主节点 zbs-metad 服务、zookeeper 服务和 mongod 服务的运行状态 | 展示当前可用域内主节点 zbs-metad 服务、zookeeper 服务和 mongod 服务是否正在运行。  - **健康**：所有主节点 zbs-metad 服务、zookeeper 服务和 mongod 服务正在运行中。 - **严重警告**：部分主节点 zbs-metad 服务、zookeeper 服务或 mongod 服务未运行。 |
   | 仲裁节点 | 仲裁节点的工作状态 | 展示仲裁节点的工作状态。  - **健康**：仲裁节点处于运行中状态。 - **严重警告**：仲裁节点的工作状态未知。 |
   | 仲裁节点的系统时间 | 展示仲裁节点的系统时间与集群的系统时间相差是否超过 3 秒。  - **健康**：系统时间差不超过 3 秒。 - **严重警告**：系统时间差超过 3 秒，需特别关注。 |
   | 仲裁节点的内部服务 mongod、zookeeper、ntpd 和 master-monitor 的运行状态 | 展示仲裁节点的 mongod 服务、zookeeper 服务、ntpd 服务和 master-monitor 服务是否正在运行。  - **健康**：仲裁节点的 mongod 服务、zookeeper 服务、ntpd 服务和 master-monitor 服务正在运行中。 - **严重警告**：仲裁节点的 mongod 服务、zookeeper 服务、ntpd 服务或 master-monitor 服务未运行。 |
   | 仲裁节点的 CPU 使用率 | 展示仲裁节点的 CPU 使用率及其持续时间。  - **健康**：仲裁节点的 CPU 使用率未超过 80%，或者 CPU 使用率虽超过 80%，但其持续时间不超过 5 分钟。 - **注意**：仲裁节点的 CPU 使用率超过 80%，且持续时间超过 5 分钟。 - **严重警告**：仲裁节点的 CPU 使用率超过 90%，且持续时间超过 5 分钟。 |
   | 仲裁节点的内存使用率 | 展示仲裁节点的内存使用率及其持续时间。  - **健康**：仲裁节点的内存使用率未超过 80%，或者内存使用率虽超过 80%，但其持续时间不超过 5 分钟。 - **注意**：仲裁节点的内存使用率超过 80%，且持续时间超过 5 分钟。 - **严重警告**：仲裁节点的内存使用率超过 90%，且持续时间超过 5 分钟。 |
   | 仲裁节点的系统空间使用率 | 展示仲裁节点的系统空间使用率是否超过 90%。  - **健康**：仲裁节点的系统空间使用率未超过 90%。 - **注意**：仲裁节点的系统空间使用率已超过 90%。 |
   | 可用域之间的网络 | 可用域之间的最差往返延时 | 展示在 5 分钟内，当前可用域的主机到另一可用域的主机的最差往返延时的平均值。  - **健康**：在 5 分钟内，当前可用域的任一主机到另一可用域的任一主机的最差往返延时的平均值不超过 10 毫秒。 - **信息**：在 5 分钟内，当前可用域的任一主机到另一可用域的任一主机的最差往返延时的平均值已超过 10 毫秒。 - **注意**：在 5 分钟内，当前可用域的任一主机到另一可用域的任一主机的最差往返延时的平均值已超过 200 毫秒。 - **严重警告**：在 5 分钟内，当前可用域的任一主机到另一可用域的任一主机的最差往返延时的平均值已超过 2 秒。 |
   | 可用域之间的网络连接 | 展示优先可用域与次级可用域之间的存储网络连接是否正常。  - **健康**：优先可用域与次级可用域之间的存储网络连接正常。 - **严重警告**：优先可用域与次级可用域之间的存储网络连接异常。 |
   | 仲裁节点与可用域之间的网络 | 仲裁节点与可用域之间的最差往返延时 | 展示在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值。  - **健康**：在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值不超过 10 毫秒。 - **信息**：在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值已超过 10 毫秒。 - **注意**：在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值已超过 200 毫秒。 - **严重警告**：在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值已超过 2 秒。 |
   | 仲裁节点与可用域之间的网络连接 | 展示仲裁节点与优先可用域之间，以及仲裁节点与次级可用域之间的存储网络连接是否正常。  - **健康**：仲裁节点与优先可用域之间，以及仲裁节点与次级可用域之间的存储网络连接正常。 - **严重警告**：仲裁节点与优先可用域之间，或者仲裁节点与次级可用域之间的存储网络连接异常。 |

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
