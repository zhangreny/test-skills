---
title: "SMTXZBS/5.7.0/SMTX ZBS 售后工程师操作指南"
source_url: "https://internal-docs.smartx.com/smtxzbs/5.7.0/aftersales_guide/aftersales_guide_preface_generic"
sections: 29
---

# SMTXZBS/5.7.0/SMTX ZBS 售后工程师操作指南
## 关于本文档

# 关于本文档

本文档介绍了 SMTX ZBS 上线后，售后工程师协助用户维护集群时可能执行的操作流程。

---

## 文档更新信息

# 文档更新信息

**2025-12-01**：**文档随 SMTX ZBS 5.7.0 正式发布**。

相较于 5.6.4 版本，本版本在**更换网卡**小节内补充启用 NVMe over RDMA 特性网卡的相关内容。

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
  2. 使用命令行 `zbs-chunk partition set-healthy` 或 `zbs-chunk cache set-healthy`将物理盘重置为健康状态。
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

如满足直接拔除的全部条件，请直接在服务器上拔除物理盘，如果不满足，请申请研发工程师支持。

---

## 硬件 > 处理 I/O 阻塞

# 处理 I/O 阻塞

当物理盘发生 I/O 阻塞时，CloudTower 的物理盘详情页中会出现 `发生 I/O 阻塞，该盘已下线并停止处理任何 I/O。请尽快联系售后。`的提示，此时请根据下图的流程，先[检查集群中存储数据的状态](#%E6%A3%80%E6%9F%A5%E5%AD%98%E5%82%A8%E6%95%B0%E6%8D%AE%E7%8A%B6%E6%80%81)，再根据存储数据的状态来确定物理盘 I/O 阻塞故障的处理流程。

![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_32.png)

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

![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_33.png)

登录 CloudTower 查看发生 I/O 阻塞已被下线的物理盘的挂载状态。

- 若该物理盘处于`未挂载`状态，请直接将该物理盘从服务器上拔除。
- 若该物理盘处于`部分挂载`或`已挂载`状态，即该物理盘上仍然存在正在被使用的分区：

  - 若剩余分区为 zbs-chunk 使用的存储相关的分区，请联系 SmartX L3 存储工程师调查处理。
  - 若剩余分区为系统分区或元数据分区，请参考[定位故障分区](#%E5%AE%9A%E4%BD%8D%E6%95%85%E9%9A%9C%E5%88%86%E5%8C%BA)小节，确认软件 RAID 1 中的另一块物理盘上的系统分区和元数据分区状态是否正常：

    - 若软件 RAID 1 中的另一块物理盘上的系统分区和元数据分区状态正常，请直接将该物理盘从服务器上拔除。
    - 若软件 RAID 1 中的另一块物理盘的系统分区和元数据分区状态存在异常，请联系 SmartX L3 SRE 工程师处理。

> **说明：**
>
> 处于下线状态的物理盘无法读写，而卸载物理盘时会对物理盘进行读写，为了避免卸载过程中对该盘的读写发生阻塞，您无法在CloudTower 上卸载该物理盘，也请您不要通过命令行卸载物理盘。

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

块存储集群的某个节点的启动盘损坏后，服务器将无法重启。您可以参考如下要求和步骤，完成启动盘更换和集群配置操作。

**准备工作**

- 确认待更换启动盘的节点的服务器 CPU 架构和所安装的块存储软件版本，并准备好对应的块存储安装文件。
- 确认待更换启动盘的节点启动时所使用的引导模式：BIOS 或者 UEFI 方式，并根据不同模式选择对应的更换操作步骤。

  登录该节点的 IPMI 管理平台，检查 **BIOS Settings** 界面中 **Boot Mode** 选项的取值，确认其引导模式。

**操作步骤**

1. 如果节点处于健康状态，则将待更换启动盘的节点[置为维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)，然后[关闭](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_09)此节点。如果节点已处于关机状态，则直接执行步骤 2。
2. 更换磁盘，更换结束后启动服务器。
3. 据节点启动时使用的引导模式，参考 [BIOS 引导模式](/smtxzbs/5.7.0/aftersales_guide/aftersales_guide_03)和 [UEFI 引导模式](/smtxzbs/5.7.0/aftersales_guide/aftersales_guide_04)完成集群配置操作.
4. 登录 CloudTower，将该节点[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)。

---

## 硬件 > 更换启动盘 > BIOS 引导模式

# BIOS 引导模式

1. 在待更换启动盘的节点中挂载块存储安装文件，并将其设置为第一启动顺序。
2. 重启服务器，在进入 SMTX ZBS 安装引导界面后，选择 **Troubleshooting**。

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_01.png)
3. 选择 **Rescue a OS system**，进入 rescue 模式。

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_02.png)
4. 输入 **`1`** 后按 Enter 键，等待提示后输入 **`chroot /mnt/sysimage`**。

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_03.png)
5. 执行命令 `lsblk`，定位更换后的启动盘。然后为其新建分区，保持分区信息与集群其他正常节点一致，如下图所示。

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_04.png)

   正常节点的 Boot 盘信息可参考下图。

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_05.png)
6. 为启动盘新建分区 `sda1`，并为其设置分区大小。例如，下图中分区 Size 设置为 `537MB`。

   ```
   bash-4.2# parted /dev/sda

   bash-4.2# mklabel msdos

   bash-4.2# mkpart primary ext4 1MiB 538MB
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_06.png)
7. 将分区格式化，并将其挂载到 `/boot` 目录下。

   ```
   bash-4.2# mkfs.ext4 /dev/sda1
   bash-4.2# mount /dev/sda1 /boot
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_07.png)
8. 参考[此链接](https://access.redhat.com/solutions/2626631)的方法配置网络，然后参考以下步骤将其他正常节点的 `/boot` 中的内容复制至当前 `/boot` 目录下。

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_08.png)

   1. 完成网络配置后，暂时开启被复制的正常节点的 ssh root 权限。方法如下：

      修改正常节点的 `/etc/ssh/sshd_config` 文件，将 `PermitRootLogin` 选项的值改为 `yes`，然后使用`systemctl restart sshd` 命令重启 ssh 服务。
   2. 以正常节点 IP 为 `192.168.26.251` 为例，执行如下命令：

      ```
      bash-4.2# scp -r 192.168.26.251:/boot /
      ```

      ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_09.png)
   3. 拷贝完成后，将正常节点的 ssh root 权限关闭。方法如下：

      修改 `/etc/ssh/sshd_config` 文件，将 `PermitRootLogin` 选项的值改为 `no`，然后使用 `systemctl restart sshd` 命令重启 ssh 服务。
9. 修复引导分区，重装 grub，生成配置文件 **grub.cfg**。

   ```
   bash-4.2# grub2-install /dev/sda
   bash-4.2# dracut -v --force --regenerate-all
   bash-4.2# grub2-mkconfig -o /boot/grub2/grub.cfg
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_10.png)

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_11.png)

   > **注意**：
   >
   > 如果执行 `grub2-install` 命令时，系统提示缺少 grub efi 相关文件，可以通过安装 grub2-efi-modules 包解决（命令如下）；但如果该方法失效，可直接联系 SmartX 研发工程师获取相关 rpm 包。
   >
   > `bash-4.2# yum install grub2-efi-modules -y`
   >
   > 在安装完 grub2-efi-modules 包后，重新执行上述三条命令。
10. 替换 `/etc/fstab` 中 **`uuid`** 为新启动盘分区的 uuid。

    执行 `blkid /dev/sda1` 命令获取 uuid 信息，然后通过 `vi /etc/fstab` 命令更新为新的 uuid 信息。

    ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_12.png)
11. 重启服务器节点，在 BIOS Settings 界面中调整磁盘的启动顺序，确保从启动盘引导启动。

---

## 硬件 > 更换启动盘 > UEFI 引导模式

# UEFI 引导模式

1. 在待更换启动盘的节点中挂载块存储安装文件，并将其设置为第一启动顺序。
2. 重启服务器，在进入 SMTX ZBS 安装引导界面后，选择 **Troubleshooting**。

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_13.png)
3. 选择 **Rescue a SMTXZBS system**，进入 rescue 模式。

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_14.png)
4. 输入 **`1`** 后按 Enter 键，等待提示后输入 **`chroot /mnt/sysimage`**。

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_15.png)
5. 执行命令 `lsblk`，定位更换后的启动盘。然后为其新建分区，保持分区信息与集群其他正常节点一致，如下图所示。

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_16.png)

   正常节点的 Boot 盘信息可参考下图。

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_17.png)
6. 为启动盘设置 GPT 分区，新建分区 `sda1`、`sda2`，并为其设置分区大小和文件系统。

   ```
   bash-4.2# parted /dev/sda

   bash-4.2# mklabel GPT

   bash-4.2# mkpart primary fat16 1MiB 269M

   bash-4.2# mkpart primary ext4 269M 806M
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_18.png)
7. 将两块分区格式化，并分别将 sda1 挂载到 `/boot/efi` 目录下，sda2 挂载到 `/boot` 目录下。

   ```
   bash-4.2# mkfs.vfat /dev/sda1
   bash-4.2# mkfs.ext4 /dev/sda2
   bash-4.2# mount /dev/sda2 /boot
   bash-4.2# mkdir /boot/efi
   bash-4.2# mount /dev/sda1 /boot/efi
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_19.png)

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_20.png)
8. 参考[此链接](https://access.redhat.com/solutions/2626631)的方法配置网络，然后参考以下步骤将其他正常节点的 `/boot` 中的内容复制至当前 `/boot` 目录下。

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_21.png)

   1. 完成网络配置后，暂时开启被复制的正常节点的 ssh root 权限。方法如下：

      修改正常节点的 `/etc/ssh/sshd_config` 文件，将 `PermitRootLogin` 选项的值改为 `yes`，然后使用`systemctl restart sshd` 命令重启 ssh 服务。
   2. 以正常节点 IP 为 `192.168.26.251` 为例，执行如下命令：

      ```
      bash-4.2# scp -r 192.168.26.251:/boot /
      ```

      ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_22.png)

      ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_23.png)
   3. 拷贝完成后，将正常节点的 ssh root 权限关闭。方法如下：

      修改 `/etc/ssh/sshd_config` 文件，将 `PermitRootLogin` 选项的值改为 `no`，然后使用 `systemctl restart sshd` 命令重启 ssh 服务。
9. 修复引导分区，重装 grub，生成配置文件 **grub.cfg**。

   1. 执行以下命令挂载 ISO 映像文件并配置 yum 源为 `smartxos.repo`.

      ```
      # 创建 /mnt/iso 目录
      mkdir /mnt/iso

      # 将 /dev/sr0 下的 SMTX ZBS 映像文件挂载到 /mnt/iso 目录
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

    ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_28.png)

    然后通过执行 `vi /etc/fstab` 命令更新为新的 uuid 信息。

    ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_29.png)
11. 重启服务器，调整系统磁盘启动顺序，确保从更换后的启动盘引导启动。

---

## 硬件 > 更换网卡 > 更换未启用 RDMA 或 NVMe over RDMA 特性的网卡

# 更换未启用 RDMA 或 NVMe over RDMA 特性的网卡

**准备工作**

确认即将安装的网卡与服务器机型兼容，可通过[硬件兼容性查询工具](https://www.smartx.com/smtxzbs-compatibility/)进行查询。

**操作步骤**

1. 登录 CloudTower，将待更换网卡的节点[置为维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)。
2. 在 CloudTower 中将待更换网卡的节点[关闭](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_09)。
3. 更换新网卡，更换结束后启动服务器。
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
6. 登录 CloudTower，将该节点[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)。
7. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

---

## 硬件 > 更换网卡 > 更换已启用 RDMA 或 NVMe over RDMA 特性的网卡

# 更换已启用 RDMA 或 NVMe over RDMA 特性的网卡

本节对于主机所对应的 OVS 网桥关联的网口开启了 RDMA 和 NVMe over RDMA 特性的情况进行了介绍和举例。相较于上一个章节，在不同名网卡的处理上有一定区别，目前 RDMA 特性和 NVMe over RDMA 特性无法在 CloudTower 上直接更改，需要在主机上使用 CLI 工具做对应的绑定。

因此，您可以参考本节内容在块存储集群完成以下任务：

- 更改主机上的 OVS 网桥所关联的网口。
- 变更网口的绑定模式。

> **说明：**
>
> SMTX ZBS 块存储集群的每个网络（存储网络/管理网络/接入网络）通过其所属的 VDS 所关联的物理网口（网卡）进行通信。VDS 通过每台主机上对应的 OVS 网桥与相应的物理网口进行关联，因此更换已启用 RDMA 特性的存储网络网卡和已启用 NVMe over RDMA 特性的接入网卡时必须同步修改主机上的 OVS 网桥信息。

## 网口绑定模式变更场景及要求

### 已启用 RDMA 的存储网络网卡

SMTX ZBS 块存储集群在创建 VDS 时，可以关联物理主机一个或多个网口。当存储网络所在的 VDS 关联了多个网口时，仅支持设置 OVS Bond 绑定类型，旧版本的可能开启了 Linux Bond 绑定类型，每种绑定类型包括 3 种绑定模式。

- OVS Bond：支持 active-backup、balance-slb、balance-tcp 三种模式。
- Linux Bond：支持 active-backup、balance-xor、802.3ad 三种模式。

SMTX ZBS 块存储集群支持以下网口绑定模式变更场景，变更时，请注意转换要求和注意事项：

| **变更场景** | **转换要求和注意事项** |
| --- | --- |
| 单⽹⼝转换为 OVS Bond | - 网卡已启用 RDMA 功能，仅支持设置为 active-backup 或者 balance-tcp 模式。 - 设置为 `active-backup` 模式时，对端交换机无需设置。 - 设置为 `balance-tcp` 模式时，要求对端交换机先开启 LACP 动态链路聚合。使用 Mellanox CX5 网卡时不建议使用该绑定模式，否则可能导致网络延迟升高。 |
| OVS Bond 转换为单⽹⼝ | - 转换后，OVS ⽹桥只关联⼀个⽹⼝，绑定模式设置为 `None`。 - 转换前后 OVS 网桥对应的绑定名称保持不变。 |
| 不同 OVS Bond 之间互相转换 | - 开启 RDMA 仅支持在 OVS Bond 模式 active-backup 与 balance-tcp 模式间转换。 - 设置为 `balance-tcp` 模式时，要求对端交换机开启 LACP 动态链路聚合。使用 Mellanox CX5 网卡时不建议使用该绑定模式，否则可能导致网络延迟升高。 - 转换前后 OVS 网桥对应的绑定名称保持不变。 |
| Linux Bond 转换为单⽹⼝ | - 转换后，OVS ⽹桥只关联⼀个⽹⼝，绑定模式设置为 `None`。 - 转换后，OVS 网桥对应的绑定名称设置为 `None`。 |
| Linux Bond 转换为 OVS Bond | - 原始 Linux Bond 为 `802.3ad` 模式时，仅能转换为 OVS Bond 模式 `balance-tcp`。使用 Mellanox CX5 网卡时不建议使用 `balance-tcp`，否则可能导致网络延迟升高。 - 原始 Linux Bond 为 `active-backup` 或者 `balance-xor` 模式时，仅能转换为 OVS Bond 模式 `active-backup`。 - 转换后 OVS 网桥对应的绑定名称为新的名称。 - 若从 Linux Bond 模式 `balance-xor` 转换为 OVS Bond 模式 `active-backup`，在转换前需要修改交换机取消 Port Channel 配置。 |
| OVS 未关联网口 | 在配置好的环境中误删除网卡，导致 OVS 网桥未关联网口，因此重新关联网口时，不需要填写“更换网卡前 OVS 网桥所关联的物理网口名称或者绑定名称”。 |

### 已启用 NVMe over RDMA 的接入网络网卡

SMTX ZBS 块存储集群在创建 VDS 时，可以关联物理主机一个或多个网口。当接入网络所在 VDS 关联了多个网口时，支持设置 OVS Bond 或者 Linux Bond 绑定类型，每种绑定类型包括 3 种绑定模式。

- OVS Bond：支持 active-backup、balance-slb、balance-tcp 三种模式。
- Linux Bond：支持 active-backup、balance-xor、802.3ad 三种模式。

SMTX ZBS 块存储集群支持以下网口绑定模式变更场景，变更时，请注意转换要求和注意事项：

| **变更场景** | **转换要求和注意事项** |
| --- | --- |
| 单⽹⼝转换为 Linux Bond | - 网卡已启用 NVMe over RDMA 功能。 - 设置为 `balance-xor` 模式时，要求对端交换机先配置为⼿⼯链路聚合。 - 设置为 `802.3ad` 模式时，要求对端交换机先开启 LACP 动态链路聚合。 - 转换后，OVS 网桥对应的绑定名称按如下要求设置，接⼊⽹络设置为 `bond0`。 |
| OVS Bond 转换为单⽹⼝ | - 转换后，OVS ⽹桥只关联⼀个⽹⼝，绑定模式设置为 `None`。 - 转换前后 OVS 网桥对应的绑定名称保持不变。 |
| 不同 OVS Bond 之间互相转换 | - 设置为 `balance-tcp` 模式时，要求对端交换机开启 LACP 动态链路聚合。 - 转换后，OVS 网桥所关联的 VDS 使用的绑定模式为 `balance-slb` 时，可以设置 rebalance 的时间间隔，其他模式均不需要设置。 - 转换前后 OVS 网桥对应的绑定名称保持不变。 |
| Linux Bond 转换为单⽹⼝ | - 转换后，OVS ⽹桥只关联⼀个⽹⼝，绑定模式设置为 `None`。 - 转换后，OVS 网桥对应的绑定名称设置为 `None`。 |
| 不同 Linux Bond 之间互相转换 | - 设置为 `balance-xor` 模式时，要求对端交换机先配置为⼿⼯链路聚合。 - 设置为 `802.3ad` 模式时，要求对端交换机先开启 LACP 动态链路聚合。 - 转换前后 OVS 网桥对应的绑定名称保持不变。 |
| OVS 未关联网口 | 在配置好的环境中误删除网卡，导致 OVS 网桥未关联网口，因此重新关联网口时，不需要填写“更换网卡前 OVS 网桥所关联的物理网口名称或者绑定名称”。 |

## 更换流程

**准备工作**

更换网卡时，需要使用 CLI 命令对网桥参数进行查询、设置、同步等操作。请在操作前参考《SMTX ZBS CLI 命令参考》中**管理网络**章节，了解相关命令的使用方法及参数设置要求。

在关机更换网卡前，请确认新更换的网卡与服务器机型兼容，可通过[硬件兼容性查询工具](https://www.smartx.com/smtxzbs-compatibility/)进行查询。

**操作步骤**

1. 使用 SSH 方式登录待更换网卡的节点。由于更换存储网络、管理网络或接入网络所占用的网卡会造成其对应网络短暂中断，因此，建议通过管理网络登录节点修改连接存储网络或接入网络的 OVS 网桥。
2. 执行命令 `ovs-vsctl show` ，查看节点的 OVS 网桥，并记录**待修改的 OVS 网桥名称**，以及**待更换网卡所绑定的端口名称**。
3. 切换至块存储集群其他正常运行的节点，执行如下命令，查看和步骤 2 中待修改 OVS 网桥名称相同的 OVS 网桥信息，同时记录当前该 OVS 网桥所对应的网口绑定名称，即 `bond_name` 值。

   `network-tool get-bond-name --ovsbr_name <ovsbr_name>`
4. 登录 CloudTower，将待更换网卡的节点[置为维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)。
5. 在 CloudTower 中将待更换网卡的节点[关闭](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_09)。
6. 更换新网卡，更换结束后启动服务器。
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

   `network-tool change-bridge --ovsbr_name <ovsbr_name_to_be_changed> --old_port_name <old_port_name> --nics <target_nics> --bond_mode <bonding_mode> --rb_interval <rb_interval> --bond_name <bonding_name>`

   请参考《SMTX ZBS CLI 命令参考》中[管理网络](/smtxzbs/5.7.0/zbs_cli_guide/zbs_cli_guide_78#%E8%AE%BE%E7%BD%AE%E7%BD%91%E6%A1%A5%E5%8F%82%E6%95%B0)章节，获取相关 CLI 命令及参数的详细说明。

   执行该命令后，若系统输出 `change bridge finish`，则表明修改 OVS 网桥信息成功。

   **使用示例**

   active-backup（OVS Bond）转换为单⽹⼝典型场景的使用示例如下。

   对原始名称为 ovsbr-storage 的 OVS 网桥进行参数设置。将绑定模式为 active-backup（OVS Bond） 的双网口变更为单网口（eth0）。 通过步骤 3 查询到该 OVS ⽹桥所对应的⽹⼝绑定名称为 `bond-m-dd417f1a`。

   ```
   $network-tool get-bond-name --ovsbr_name ovsbr-storage
   ...
   2022-05-18 12:44:33,892 [72353] [INFO] bond_name: bond-m-dd417f1a

   $network-tool change-bridge --ovsbr_name ovsbr-storage --old_port_name bond-m-dd417f1a --nics eth0 --bond_mode None --bond_name bond-m-dd417f1a  
   ...  
   ...  
   ...  
   [INFO] change bridge finish
   ```
10. 在更换网卡的节点上执行如下命令，将修改后的 OVS 网桥信息同步至数据库。

    其中 `bonding_mode` 和 `bonding_name` 参数值必须与步骤 9 所执行命令中的 `bonding_mode` 和 `bonding_name` 参数值保持一致。

    `--nics <uplink_nics>` 为可选参数。命令格式为 --nics "eth0 eth1"。若通过 network-tool change-bridge 命令将被隔离的故障网卡和 OVS 网桥解除关联，需配置此参数，且需和 network-tool change-bridge 命令中的 `--nics <target_nics>` 参数保持一致。

    `network-tool sync-bridge --ovsbr_name <ovsbr_name_to_be_changed> --bond_mode <bonding_mode> --bond_name <bonding_name> --nics <uplink_nics>`

    请参考《SMTX ZBS CLI 命令参考》中[管理网络](/smtxzbs/5.7.0/zbs_cli_guide/zbs_cli_guide_78#%E5%90%8C%E6%AD%A5%E7%BD%91%E6%A1%A5%E7%BD%91%E5%8D%A1%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E4%BF%A1%E6%81%AF%E8%87%B3%E6%95%B0%E6%8D%AE%E5%BA%93)章节，获取相关 CLI 命令及参数的详细说明。

    执行完命令后，若系统输出 `sync successfully`，则表明同步数据成功。
11. 登录 CloudTower，将该节点[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)。
12. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

    `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

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

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间更换存储控制器，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换存储控制器，请您知悉上述风险后进行操作。

**操作步骤**

1. [移除](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_34)故障控制器所在的节点。
2. 更换存储控制器后，开启服务器，将 2 块系统盘组建成硬件 RAID 1。
3. 将节点重新[添加](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_08)至原集群。

### 启动盘硬件 RAID 1

**准备工作**

记录存储控制器槽位。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间更换存储控制器，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换存储控制器，请您知悉上述风险后进行操作。

**操作步骤**

1. 将待更换存储控制器的节点[置为维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)，然后[关闭](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_09)此节点。如果节点宕机，可以忽略该操作，直接进行步骤 2。
2. 更换存储控制器，更换结束后开启服务器，将启动盘组建成硬件 RAID 1。
3. 重启服务器后若无法正常引导进系统，请根据服务器原有引导模式参考[更换启动盘](/smtxzbs/5.7.0/aftersales_guide/aftersales_guide_02)章节内容重建引导盘。

## 不存在硬件 RAID 1 配置

**准备工作**

- 确认即将安装的存储控制器与原来的存储控制器的型号完全相同。
- 记录存储控制器槽位。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间更换存储控制器，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换存储控制器，请您知悉上述风险后进行操作。

**操作步骤**

1. 将待更换存储控制器的节点[置为维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)，然后[关闭](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_09)此节点。如果节点宕机，可以忽略该操作，直接进行步骤 2。
2. 更换存储控制器，断开存储控制器与物理盘的连接，避免服务器开机后直接进入系统。
3. 开启服务器，进入存储控制器配置界面，将存储控制器模式修改为更换前存储控制器的模式。
4. 关闭服务器，重新连接存储控制器与物理盘，再次开启服务器。
5. 登录 CloudTower，将该节点[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)。如果更换存储控制器前节点宕机，可以忽略该操作，直接进行步骤 6 。
6. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

---

## 硬件 > 更换 CPU（SMTX Halo 存储一体机）

# 更换 CPU（SMTX Halo 存储一体机）

本节描述的方法和步骤仅针对 SMTX Halo 超融合一体机的 CPU 故障场景，非一体机的 CPU 故障更换由服务器的厂商负责，其流程和步骤与本节不同。

**准备工作**

确保即将安装的 CPU 与原来服务器上的 CPU 型号须保持一致。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照和异步复制计划之外的其他时间更换 CPU，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换 CPU，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，将待更换 CPU 的节点[置为维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)。
2. 在 CloudTower 中将待更换 CPU 的节点[关闭](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_09)。
3. SMTX Halo 存储一体机的硬件供应商更换 CPU 散热模块，拆卸原来的 CPU 后，安装新的 CPU。
4. 启动服务器，开机后登录节点的 IPMI 管理台，确认 IPMI 管理台已识别新更换的 CPU。
5. 登录 CloudTower，将该节点[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)。
6. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

---

## 硬件 > 更换主板（Halo 存储一体机）

# 更换主板（Halo 存储一体机）

本节描述的方法和步骤仅针对 SMTX Halo 超融合一体机的主板故障场景，非一体机的主板故障更换由服务器的厂商负责，其流程和步骤与本节不同。

**准备工作**

确保即将安装的主板与原来服务器上的主板型号须保持一致。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照和异步复制计划之外的其他时间更换主板，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换主板，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，将待更换主板的节点[置为维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)。
2. 在 CloudTower 中将待更换主板的节点[关闭](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_09)。
3. Halo 存储一体机的硬件供应商拆卸原来的主板，并更换新主板，最后完成风扇支架、导风罩以及顶盖的安装。
4. 更新 Halo 存储一体机的序列号，并在 BIOS 中完成相应的设置。

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
6. 登录 CloudTower，将该节点[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)。
7. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

> **注意**：
>
> 如更换主板后发现系统时钟不同步，请参考[调整块存储集群系统时间](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_11)章节修正系统时间。

---

## 集群 > 管理 Boost 模式 > 启用集群 Boost 模式

# 启用集群 Boost 模式

SMTX ZBS 5.6.0 及以上版本支持为块存储集群启用 Boost 模式。如果 SMTX ZBS 块存储集群从低版本升至 5.6.0 及以上版本或在安装部署时未启用 Boost 模式，升级或部署完成后可以为集群启用 Boost 模式。

**前提条件**

集群中所有系统服务虚拟机已关机。若存在未关机的系统服务虚拟机，请参考《集群上下线工具用户指南》中 SMTX ZBS 集群下线的步骤 3 进行操作。

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

集群中所有系统服务虚拟机已关机。若存在未关机的系统服务虚拟机，请参考《集群上下线工具用户指南》中 SMTX ZBS 集群下线的步骤 3 进行操作。

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

## 集群 > 重建双活集群仲裁节点

# 重建双活集群仲裁节点

当 SMTX ZBS 双活集群的仲裁节点发生不可恢复的故障并下线后，您可以通过一台新的物理机或虚拟机重建仲裁节点，以保证双活集群继续运行和提供服务。

---

## 集群 > 重建双活集群仲裁节点 > 检查双活集群的状态

# 检查双活集群的状态

登录 CloudTower，在左侧导航栏中选中双活集群，进入**概览**界面，查看当前双活集群的状态。预期**双活状态**卡片中仅显示仲裁节点存在故障，而优先可用域和次级可用域的所有主机显示为`健康`状态（如下图所示）。

![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_30.png)

---

## 集群 > 重建双活集群仲裁节点 > 清理故障仲裁节点

# 清理故障仲裁节点

在 CloudTower 中确认双活集群的状态后，登录双活集群的节点，获取仲裁节点信息并将该故障节点从双活集群中清除。

**注意事项**

在执行清理仲裁节点的命令前，请务必确认仲裁节点已经发生故障且无法恢复。

**操作步骤**

1. 登录双活集群的优先可用域或次级可用域的任一节点，执行如下命令，获取并记录当前双活集群的仲裁节点信息（`Witness uuid`）。

   ```
   [root@node1 15:49:11 smartx]$zbs-deploy-manage witness --help
   Usage: zbs-deploy-manage witness [OPTIONS] COMMAND [ARGS]...

     manage witness node

   Options:
     --help  Show this message and exit.

   Commands:
     add                   add witness node
     config-static-routes  config cluster nodes static routes
     get                   get witness node info
     remove                remove witness node
   [root@node1 15:50:13 smartx]$zbs-deploy-manage witness get
   2023-05-23 15:50:17,538 INFO witness_get_info: Witness uuid is 44a51c2a-f095-11ed-b46d-52540062a4cf, ip is 10.0.0.1
   ```
2. 获取仲裁节点信息后，执行如下命令，清理原来故障仲裁节点的信息，从双活集群中移除该仲裁节点。

   ```
   [root@node1 15:50:19 smartx]$zbs-deploy-manage witness remove --help
   Usage: zbs-deploy-manage witness remove [OPTIONS]

     remove witness node

   Options:
     --witness_ip TEXT  witness node ip  [required]
     --help             Show this message and exit.
   [root@node1 15:51:05 smartx]$nohup zbs-deploy-manage witness remove --witness_ip 10.0.0.1 & 
   [root@node1 15:51:05 smartx]$tail -f nohup.out
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

- SMTX ZBS 块存储集群
- SMTX ZBS 双活集群，集群为`健康`状态

以上两种状态均符合当前场景（仲裁节点重建前）的预期，后续完成仲裁节点的重建后，双活集群的状态将会恢复正常。

---

## 集群 > 重建双活集群仲裁节点 > 重建仲裁节点

# 重建仲裁节点

1. 下载当前 SMTX ZBS 双活集群的主机所安装的 ISO 映像文件，并在新的仲裁节点完成安装。

   参考《SMTX ZBS 双活集群安装部署指南》中**在节点上安装 SMTX ZBS 块存储**章节的[在仲裁节点上安装块存储文件](/smtxzbs/5.7.0/multiactive_user_guide/zbs_multiactive_user_guide/zbs_multiactive_user_guide_21)小节进行安装。
2. 为仲裁节点设置部署前的环境。

   参考《SMTX ZBS 双活集群安装部署指南》中**部署 SMTX ZBS 双活集群**章节的[为仲裁节点设置部署的环境](/smtxzbs/5.7.0/multiactive_user_guide/zbs_multiactive_user_guide/zbs_multiactive_user_guide_28)小节进行安装。

   > **说明：**
   >
   > - 为仲裁节点设置部署的环境时，您需要指定重建的仲裁节点的存储 IP。
   > - 重建的仲裁节点的存储 IP 的子网掩码需根据双活集群的实际情况指定。
3. （可选）若仲裁节点与两个可用域的主机 L3 层存储网络连通，而不是 L2 层网络连通时，需要在仲裁节点上配置到两个可用域的静态路由，其路由配置文件需根据双活集群的实际网络规划信息进行设置。

   例如，以仲裁节点的存储网卡 `eth1` 作为示例，仲裁节点通过网关 `10.0.0.2` 路由到优先可用域的三个节点（`10.0.77.101 ~ 103`），仲裁节点通过网关 `10.0.0.3` 路由到次级可用域的三个节点(`10.0.77.104 ~ 106`)。

   ![](https://cdn.smartx.com/internal-docs/assets/4657fe4e/aftersales_guide_31.png)

---

## 集群 > 重建双活集群仲裁节点 > 为双活集群主机配置静态路由（可选）

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

## 集群 > 重建双活集群仲裁节点 > 添加重建的仲裁节点至双活集群

# 添加重建的仲裁节点至双活集群

在仲裁节点完成基本配置后，可以通过以下命令将仲裁节点添加到双活集群中。

以下为配置示例，其中 `–witness_uuid` 是清理故障仲裁节点时获取的仲裁节点 UUID 信息（`Witness uuid`），即 `44a51c2a-f095-11ed-b46d-52540062a4cf`。

```
[root@node1 16:31:07 smartx]$zbs-deploy-manage witness add --help
Usage: zbs-deploy-manage witness add [OPTIONS]

  add witness node

Options:
  --witness_ip TEXT    witness node ip  [required]
  --witness_uuid TEXT  witness node uuid
  --help               Show this message and exit.
[root@node1 16:32:54 smartx]$zbs-deploy-manage witness add --witness_uuid 44a51c2a-f095-11ed-b46d-52540062a4cf --witne
ss_ip 10.0.0.11
```

若重建的仲裁节点成功添加至双活集群，则日志显示如下：

```
2023-05-23 16:39:34,144 INFO witness_add: Add witness node 10.0.0.11 successfully
```

---

## 集群 > 重建双活集群仲裁节点 > 同步仲裁节点的管理 IP

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

## 集群 > 重建双活集群仲裁节点 > 在 CloudTower 中确认双活集群的状态

# 在 CloudTower 中确认双活集群的状态

访问 CloudTower 所在虚拟机的 VNC，远程登录后，在终端里执行以下命令，CloudTower 将主动更新双活集群信息，其中 `$url` 为 CloudTower 的 IP 地址，并且需要携带权限信息，例如 `admin:cloudtower@192.168.31.126`。如果 CloudTower 使用域名，需要确保双活集群节点可以正确解析 CloudTower 域名。

```
curl "https://$url/api/admin/execute-task?key=UPSERT_WITNESS" -k
curl "https://$url/api/admin/execute-task?key=UPSERT_ZONE" -k
curl "https://$url/api/admin/execute-task?key=UPDATE_CLUSTER" -k
```

登录 CloudTower，并在左侧导航栏中选中双活集群，进入**概览**界面，参考如下步骤，检查集群的运行情况，确认集群处于正常状态。

---

## 集群 > 重建双活集群仲裁节点 > 在 CloudTower 中确认双活集群的状态 > 查看优先/次级可用域

# 查看优先/次级可用域

SMTX ZBS 双活集群的硬件可归属于特定的可用域，因此除了支持在集群层级对这些资源进行管理外，还可以在可用域层级查看和管理这些资源，并查看以当前可用域内主机作为接入点的活跃连接。

在 CloudTower 左侧导航栏中选中数据中心下的**优先可用域**或者**次级可用域**，可以查看可用域内的硬件详情及活跃连接信息。

---

## 集群 > 重建双活集群仲裁节点 > 在 CloudTower 中确认双活集群的状态 > 查看双活拓扑状态

# 查看双活拓扑状态

为了能清晰直观地了解双活集群的状态，CloudTower 提供双活状态显示功能。

在双活集群中可以单击**双活状态**进入详情界面，将展示以下拓扑状态信息：

- 双活集群拉伸结构及集群信息，例如可用域内主机数量。
- 双活集群健康状态：展示各组件的健康状况，如有报警信息，将展示在状态图上。
- 双活组件运行信息：单击组件后，在弹出的概览页面中查看组件在[双活集群运行信息](/smtxzbs/5.7.0/aftersales_guide/zbs_administration_guide/zbs_administration_guide_121)。

当双活集群出现异常时，拓扑状态图会实时变更，并及时提示用户查看。

---

## 集群 > 重建双活集群仲裁节点 > 在 CloudTower 中确认双活集群的状态 > 查看双活集群运行信息

# 查看双活集群运行信息

查看双活集群的运行信息时，还需包含对双活的健康检查，这依赖于 SMTX ZBS 块存储集群的报警监控服务。而可用域的具体情况，可以在可用域级别的资源中查看，信息更丰富。

**操作步骤**

1. 在双活集群界面单击**双活状态**页签。
2. 选择以下组件及网络连接，在弹出的概览页面中查看集群中可用域和节点的基本信息和监控信息，可用域间的网络流量，以及仲裁节点与可用域间 ping 状态。

   | 组件/网络连接 | 查看项目 | 具体信息 |
   | --- | --- | --- |
   | 优先/次级可用域 | 基本信息 | 主机数量  所属数据中心  总存储空间  已使用/失效/空闲存储 |
   | 仲裁节点 | 基本信息 | IP 地址  CPU 分配  内存分配  系统总空间  系统已使用/空闲空间 |
   | 监控信息 | 两小时内，节点的 CPU 使用率及内存使用率 |
   | 可用域之间的网络 | 网络流量 | 优先可用域至次级可用域的网络流量  次级可用域至优先可用域的网络流量 |
   | 仲裁节点与可用域间的网络 | Ping 状态 | 仲裁节点到优先可用域/次级可用域的最差往返延时  优先可用域/次级可用域到仲裁节点的最差往返延时 |
3. 检查可用域的运行状态，以及优先可用域与次级可用域之间，仲裁节点与可用域之间的网络连接状态，并关注和处理注意或告警信息，及时恢复集群的健康运行状态。

   | 组件/网络连接 | 健康检查项目 | 具体信息 |
   | --- | --- | --- |
   | 优先/次级可用域 | 可用域总数据空间 | 展示在当前可用域整体失效时，另一可用域的数据空间是否足以恢复当前全部数据至 3 副本。  - **健康**：数据空间足够，完全可以支持恢复数据至 3 副本。 - **注意**：数据空间不足，无法支持当前全部数据恢复至 3 副本。 - **严重警告**：数据空间严重不足，无法支持当前全部数据恢复至 2 副本。 |
   | 可用域内主机的系统时间 | 展示当前可用域内所有主机的系统时间与集群的系统时间相差是否超过 3 秒。  - **健康**：系统时间差均不超过 3 秒。 - **严重警告**：存在部分主机的系统时间与集群的系统时间相差超过 3 秒，需特别关注。 |
   | 可用域内主机电源状态 | 展示当前可用域内所有主机的电源状态。  - **健康**：所有主机均处于开机状态。 - **注意**：部分主机处于断电状态。 |
   | 可用域内主机工作状态 | 展示当前可用域内所有主机的工作状态。  - **健康**：所有主机均处于运行中状态。 - **严重警告**：部分主机的工作状态未知。 |
   | 可用域内主机存储健康状态 | 展示当前可用域内所有主机存储服务的健康状态。  - **健康**：所有主机的存储服务可用。 - **严重警告**：部分主机的存储服务异常。 |
   | 可用域内主节点 zbs-metad、zookeeper 和 mongod 服务的运行状态 | 展示当前可用域内主节点 zbs-metad、zookeeper 和 mongod 服务是否正在运行。  - **健康**：所有主节点 zbs-metad、zookeeper 和 mongod 服务正在运行中。 - **严重警告**：部分主节点 zbs-metad、zookeeper 或 mongod 服务未运行。 |
   | 仲裁节点 | 仲裁节点的工作状态 | 展示仲裁节点的工作状态。  - **健康**：仲裁节点处于运行中状态。 - **严重警告**：仲裁节点的工作状态未知。 |
   | 仲裁节点的系统时间 | 展示仲裁节点的系统时间与集群的系统时间相差是否超过 3 秒。  - **健康**：系统时间差不超过 3 秒。 - **严重警告**：系统时间差超过 3 秒，需特别关注。 |
   | 仲裁节点的系统服务 mongod、zookeeper、ntpd 和 master-monitor 的运行状态 | 展示仲裁节点的 mongod、zookeeper、ntpd 和 master-monitor 服务是否正在运行。  - **健康**：仲裁节点的 mongod、zookeeper、ntpd 和 master-monitor 服务正在运行中。 - **严重警告**：仲裁节点的 mongod、zookeeper、ntpd 或 master-monitor 服务未运行。 |
   | 仲裁节点的 CPU 使用率 | 展示仲裁节点的 CPU 使用率及其持续时间。  - **健康**：仲裁节点的 CPU 使用率未超过 80%，或者 CPU 使用率虽超过 80%，但其持续时间不超过 5 分钟。 - **注意**：仲裁节点的 CPU 使用率超过 80%，且持续时间超过 5 分钟。 - **严重警告**：仲裁节点的 CPU 使用率超过 90%，且持续时间超过 5 分钟。 |
   | 仲裁节点的系统空间使用率 | 展示仲裁节点的系统空间使用率是否超过 90%。  - **健康**：仲裁节点的系统空间使用率未超过 90%。 - **注意**：仲裁节点的系统空间使用率已超过 90%。 |
   | 可用域之间的网络 | 可用域之间的最差往返延时 | 展示在 5 分钟内，当前可用域的主机到另一可用域的主机的最差往返延时的平均值。  - **健康**：在 5 分钟内，当前可用域的任一主机到另一可用域的任一主机的最差往返延时的平均值不超过 10 毫秒。 - **信息**：在 5 分钟内，当前可用域的任一主机到另一可用域的任一主机的最差往返延时的平均值已超过 10 毫秒。 - **注意**：在 5 分钟内，当前可用域的任一主机到另一可用域的任一主机的最差往返延时的平均值已超过 200 毫秒。 - **严重警告**：在 5 分钟内，当前可用域的任一主机到另一可用域的任一主机的最差往返延时的平均值已超过 2 秒。 |
   | 可用域之间的网络连接 | 展示优先可用域与次级可用域之间的存储网络连接是否正常。  - **健康**：优先可用域与次级可用域之间的存储网络连接正常。 - **严重警告**：优先可用域与次级可用域之间的存储网络连接异常。 |
   | 仲裁节点与可用域之间的网络 | 仲裁节点与可用域之间的最差往返延时 | 展示在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值。  - **健康**：在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值不超过 10 毫秒。 - **信息**：在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值已超过 10 毫秒。 - **注意**：在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值已超过 200 毫秒。 - **严重警告**：在 5 分钟内，仲裁节点到优先可用域及次级可用域的任一主机的最差往返延时的平均值已超过 2 秒。 |
   | 仲裁节点与可用域之间的网络连接 | 展示仲裁节点与优先可用域之间，以及仲裁节点与次级可用域之间的存储网络连接是否正常。  - **健康**：仲裁节点与优先可用域之间，以及仲裁节点与次级可用域之间的存储网络连接正常。 - **严重警告**：仲裁节点与优先可用域之间，或者仲裁节点与次级可用域之间的存储网络连接异常。 |

---

## 集群 > 激活 TencentOS

# 激活 TencentOS

在基于 TencentOS 操作系统的 SMTX ZBS 块存储集群部署完成后，需要激活主机的操作系统，以获得腾讯官方的技术支持、安全更新等。您可参考本章节通过离线激活的方式进行激活。

---

## 集群 > 激活 TencentOS > 准备工作 > 获取主机硬件 ID

# 获取主机硬件 ID

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

---

## 集群 > 激活 TencentOS > 准备工作 > 获取许可码

# 获取许可码

联系 SmartX 售后工程师，提交所有待激活主机的硬件 ID，获取激活所需的许可码。

---

## 集群 > 激活 TencentOS > 激活 SMTX ZBS 主机操作系统

# 激活 SMTX ZBS 主机操作系统

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
