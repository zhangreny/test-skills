---
title: "SMTXOS/6.3.0/SMTX OS 运维指南"
source_url: "https://internal-docs.smartx.com/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_preface_generic"
sections: 86
---

# SMTXOS/6.3.0/SMTX OS 运维指南
## 关于本文档

# 关于本文档

本文档介绍了 SMTX OS 集群上线后例行检查的方式，以及运行维护时可能会遇到的部分场景和解决办法。

阅读本文档需了解 SMTX OS 软件，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

**2026-02-04：配合 SMTX OS 6.3.0 正式发布**

相较于 6.2.0，本版本主要更新如下：

- **物理盘运维**：
  - 新增**下载物理盘日志**章节。
  - **挂载物理盘**：
    - 新增不同容量规格的主机可挂载的数据分区总容量限制。
    - 新增为物理盘选择物理盘池的步骤。
  - **卸载物理盘**：更新卸载要求。
- **节点运维**：
  - **设置维护模式**：新增 CloudTower 启用 HA 后进入维护模式的处理方式。
  - **关闭节点**、**重启节点**：新增 CloudTower 启用 HA 时执行节点操作的前提条件。
  - **添加节点**：
    - **未启用双活特性的 SMTX OS 集群**：
      - **为 SMTX OS（ELF）集群添加新节点** > **为集群添加主机**：
        - 为启用 RDMA 功能的集群选择网卡时，删除网口来自同一张网卡的要求。
        - 新增镜像出口网口的相关说明。
        - 新增配置隧道源 IP 的说明。
        - 新增配置物理盘池的步骤。
        - 更新指定物理盘用途的步骤，并支持指定所属物理盘池。
        - 新增统一集群 SSH 端口的说明。
        - 新增激活 TencentOS 和在主机上部署 SVM 的后续操作。
      - **为 SMTX OS (VMware ESXi) 集群添加新节点**：
        - **准备工作**：新增确认 ESXi 主机 SSH 端口号的说明。
        - **为集群添加主机**：更新指定物理盘用途的步骤说明；在执行部署步骤新增统一集群 SSH 端口的说明。
    - 新增**启用双活特性的 SMTX OS 集群**章节。
  - **移除节点**：新增集群启用深度安全防护功能时移除节点前需完成的操作。
- **集群运维**：
  - **更新 NTP 服务器**：更新操作步骤。
  - **调整集群系统时间**：支持通过界面调整系统时间，更新操作步骤。
  - **设置服务端口**：新增**编辑 ssh 服务端口**小节。

---

## 例行检查

# 例行检查

SMTX OS 集群正式上线运行后，IT 基础架构管理员或运维工程师需要定期登录集群的管理平台，监控 SMTX OS 集群的运行情况，及时分析集群的日志和报警信息并定位问题，以保证集群正常运行。

## 查看资源

您可以通过 CloudTower 查看虚拟机、主机和集群的运行状态和资源使用情况。

- **虚拟机**：您可以在 CloudTower 主页面左侧的导航栏中选择组织、数据中心、集群、主机或双活集群的可用域，在右侧的管理页面选择虚拟机，资源列表中会展示所选范围内所有虚拟机的信息。信息的具体说明请参考《SMTX OS 管理指南》[虚拟机的配置信息](/smtxos/6.3.0/os_administration_guide/os_administration_guide_007)章节。
- **主机**：您可以在 CloudTower 主页面左侧的导航栏中选择组织、数据中心、集群或双活集群的可用域，在右侧的管理页面选择主机，资源列表中会展示所选范围内所有主机的信息。信息的具体说明请参考《SMTX OS 管理指南》[查看主机信息](/smtxos/6.3.0/os_administration_guide/os_administration_guide_128)章节。
- **集群**：您可以在 CloudTower 主页面左侧的导航栏中选择组织、数据中心，在右侧的管理页面选择集群，资源列表中会展示所选资源内所有集群的信息。信息的具体说明请参考《SMTX OS 管理指南》[了解 SMTX OS 集群](/smtxos/6.3.0/os_administration_guide/os_administration_guide_001)章节。

## 查看监控

通过监控分析功能，通过对集群内的虚拟机和主机等多种资源对象的指标进行监控，并以视图和图表的方式组织和呈现数据，以帮助您对资源使用情况进行分析。详情请参考《SMTX OS 管理指南》[监控分析](/smtxos/6.3.0/os_administration_guide/os_administration_guide_169)章节。

除 SMTX OS 提供的监控分析外，还可以通过部署可观测性服务和高级监控实现集群更全面的监控。

- 可观测性服务支持按需随时增加 CPU、内存和存储资源，确保在监控数据量显著增长的情况下监控性能不受影响，还支持更深入地分析和处理监控数据。详情请参考对应版本的《可观测性平台用户指南》**管理监控功能**章节。
- 高级监控支持保存更长时间的数据，还支持自定义 CPU、内存和存储资源。详情请参考对应版本的《CloudTower 使用指南》**管理高级监控**章节。

相较于高级监控，可观测性服务提供更稳定的数据采集和存储能力、更丰富的监控报警能力，并且支持统一处理多个集群的数据，建议优先部署可观测性服务。已部署高级监控的集群，建议部署可观测性服务，并将高级监控的数据迁移至可观测性服务。

## 查看报警

报警信息包含了该报警的触发原因、可能产生的影响以及推荐的解决方法等。您可以通过告警信息判断当前集群的运行状况，定位具体的问题。详情请参考对应版本的《CloudTower 使用指南》**管理报警**章节。

关联可观测性服务后，可选择通过可观测性服务将集群的报警信息发送到指定的邮箱、webhook 或第三方监控平台，获得增强的报警通知能力。详情请参考对应版本的《可观测性平台用户指南》**管理报警功能**章节。

## 查看日志

您可以采集集群的操作系统日志、SMTX OS 服务日志、Coredump 日志和节点信息。详情请参考《SMTX OS 管理指南》[采集日志](/smtxos/6.3.0/os_administration_guide/os_administration_guide_229)章节。

关联 1.1.0 及以上版本的可观测性服务后，您可以通过日志检索功能快速查询到特定条件的日志，还可以通过日志传输功能将集群产生的日志实时发送到配置的 Syslog 服务器中，以便您将日志保存在第三方服务器上。详情请参考对应版本的《可观测性平台用户指南》**管理日志功能**章节。

## 查看事件

超级管理员、运维管理员和安全审计员可以查看事件审计信息以便追溯运维事件。详情请参考对应版本的《CloudTower 使用指南》**事件审计**章节。

## 定期巡检

你可以通过巡检中心对目标集群的配置、使用情况、性能和服务状态进行检查，由此识别集群当前存在的问题及潜在的风险，并为每条风险项提供针对性的解决方案，可帮助您快速了解集群信息、明确优化方向，确保集群的资源和运行处于最优状态。详情请参考对应版本的《巡检中心用户指南》。

---

## 物理盘运维 > 升级物理盘固件

# 升级物理盘固件

升级物理盘固件时，请您根据硬件厂商提供的物理盘升级方案是否需要重启节点，以及升级的物理盘是否为系统盘（包含 SMTX 系统盘）参考不同的操作步骤进行升级：

- 升级方案需要重启节点，如提供 liveOS 或者插 U 盘进行升级，请参考[离线升级物理盘固件](#%E7%A6%BB%E7%BA%BF%E5%8D%87%E7%BA%A7%E7%89%A9%E7%90%86%E7%9B%98%E5%9B%BA%E4%BB%B6)章节内容。
- 升级方案不需要重启节点：
  - 待升级固件的物理盘为系统盘，请参考[在线升级系统盘固件](#%E5%9C%A8%E7%BA%BF%E5%8D%87%E7%BA%A7%E7%B3%BB%E7%BB%9F%E7%9B%98%E5%9B%BA%E4%BB%B6)章节内容。
  - 待升级固件的物理盘为非系统盘，请参考[在线升级非系统盘固件](#%E5%9C%A8%E7%BA%BF%E5%8D%87%E7%BA%A7%E9%9D%9E%E7%B3%BB%E7%BB%9F%E7%9B%98%E5%9B%BA%E4%BB%B6)章节内容。
  - 待升级固件的物理盘同时包含系统盘和非系统盘，请参考[在线升级系统盘固件](#%E5%9C%A8%E7%BA%BF%E5%8D%87%E7%BA%A7%E7%B3%BB%E7%BB%9F%E7%9B%98%E5%9B%BA%E4%BB%B6)章节内容。

## 离线升级物理盘固件

1. 登录 CloudTower，将待升级物理盘固件的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 在 CloudTower 中[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)该节点。
3. 升级固件，确认固件版本为目标版本后启动服务器。
4. 登录 CloudTower，将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。
5. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`
6. 在集群任意节点执行如下命令，确认数据恢复是否完成：

   `sudo zbs-meta pextent find need_recover`

   若返回 `No PExtents found.` 表示数据恢复完成。否则请等待一段时间再次数据恢复完成。

## 在线升级系统盘固件

1. 登录 CloudTower，将待升级物理盘固件的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 在待升级物理盘固件的节点命令行终端执行如下命令，停止节点 chunk 服务：

   `sudo systemctl stop zbs-chunkd`
3. 继续执行如下命令，确认 chunk 服务已经停止：

   `sudo systemctl status zbs-chunkd`

   输出如下结果表示 chunk 服务已经停止，请确认此时 `Active` 为 **inactive (dead)**：

   ```
     ● zbs-chunkd.service - ZBS chunk service
        Loaded: loaded (/usr/lib/systemd/system/zbs-chunkd.service; enabled; vendor preset: disabled)
       Drop-In: /etc/systemd/system/zbs-chunkd.service.d
                └─cgroup.conf, delegate.conf
        Active: inactive (dead) since Fri 2024-12-20 12:08:24 CST; 42s ago
       Process: 180462 ExecStart=/usr/share/zbs/bin/zbs_run_service.sh zbs/others /usr/sbin/zbs-chunkd --foreground (code=exited, status=0/SUCCESS)
      Main PID: 180462 (code=exited, status=0/SUCCESS)
        Status: "Starting event loop..."
   ```

   > **说明**：
   >
   > 此时 CloudTower 上会出现该节点**存储服务健康状态异常**的告警，是预期行为。
4. 升级固件，完成后确认固件版本为目标版本。
5. 在待升级物理盘固件的节点命令行终端执行如下命令，启动节点 chunk 服务。

   `sudo systemctl start zbs-chunkd`
6. 继续执行如下命令，检查 chunk 服务是否正常启动：

   `sudo systemctl status zbs-chunkd`

   输出如下结果表示 chunk 服务正常启动，请确认此时 `Active` 为 **active (running)**：

   ```
       ● zbs-chunkd.service - ZBS chunk service
          Loaded: loaded (/usr/lib/systemd/system/zbs-chunkd.service; enabled; vendor preset: disabled)
         Drop-In: /etc/systemd/system/zbs-chunkd.service.d
                  └─cgroup.conf, delegate.conf
          Active: active (running) since Fri 2024-12-20 12:45:12 CST; 3s ago
         Process: 132708 ExecStartPre=/usr/share/zbs/bin/zbs_config_rdma_qos.sh dscp $CHUNK_SERVER_ACCESS_QOS_MODE (code=exited, status=0/SUCCESS)
        Main PID: 132712 (zbs-chunkd)
          Status: "Starting event loop..."
           Tasks: 21
          Memory: 112.0M
          CGroup: /smtx.slice/smtx-zbs.slice/smtx-zbs-chunkd.slice/zbs-chunkd.service
                  └─132712 /usr/sbin/zbs-chunkd --foreground
   ```
7. 等待 CloudTower 上该节点**存储服务健康状态异常**的告警取消。
8. 在 CloudTower 上将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。
9. 在集群任意节点执行如下命令，确认数据恢复是否完成：

   `sudo zbs-meta pextent find need_recover`

   若返回 `No PExtents found.` 表示数据恢复完成。否则请等待一段时间再次数据恢复完成。

## 在线升级非系统盘固件

1. 将待升级物理盘固件的主机设置为存储维护模式，请参考《SMTX OS CLI 命令参考》确认 chunk ID 并[设置 chunk 进入存储维护模式](/smtxos/6.3.0/cli_guide/cli_guide_30)。

   输出内容中 ID 和 IP 是待升级物理盘固件的主机且 `Maintenance Mode` 为 **True** 则表示进入存储维护模式成功。进入存储维护模式成功之后，等待 10 秒。
2. 在待升级物理盘固件的节点命令行终端执行如下命令，停止节点 chunk 服务：

   `sudo systemctl stop zbs-chunkd`
3. 继续执行如下命令，确认 chunk 服务已经停止：

   `sudo systemctl status zbs-chunkd`

   输出如下结果表示 chunk 服务已经停止，请确认此时 `Active` 为 **inactive (dead)**：

   ```
     ● zbs-chunkd.service - ZBS chunk service
        Loaded: loaded (/usr/lib/systemd/system/zbs-chunkd.service; enabled; vendor preset: disabled)
       Drop-In: /etc/systemd/system/zbs-chunkd.service.d
                └─cgroup.conf, delegate.conf
        Active: inactive (dead) since Fri 2024-12-20 12:08:24 CST; 42s ago
       Process: 180462 ExecStart=/usr/share/zbs/bin/zbs_run_service.sh zbs/others /usr/sbin/zbs-chunkd --foreground (code=exited, status=0/SUCCESS)
      Main PID: 180462 (code=exited, status=0/SUCCESS)
        Status: "Starting event loop..."
   ```

   > **说明**：
   >
   > 此时 CloudTower 上会出现该节点**存储服务健康状态异常**的告警，是预期行为。
4. 升级固件，完成后确认固件版本为目标版本。
5. 在待升级物理盘固件的节点命令行终端执行如下命令，启动节点 chunk 服务。

   `sudo systemctl start zbs-chunkd`
6. 继续执行如下命令，检查 chunk 服务是否正常启动：

   `sudo systemctl status zbs-chunkd`

   输出如下结果表示 chunk 服务正常启动，请确认此时 `Active` 为 **active (running)**：

   ```
       ● zbs-chunkd.service - ZBS chunk service
          Loaded: loaded (/usr/lib/systemd/system/zbs-chunkd.service; enabled; vendor preset: disabled)
         Drop-In: /etc/systemd/system/zbs-chunkd.service.d
                  └─cgroup.conf, delegate.conf
          Active: active (running) since Fri 2024-12-20 12:45:12 CST; 3s ago
         Process: 132708 ExecStartPre=/usr/share/zbs/bin/zbs_config_rdma_qos.sh dscp $CHUNK_SERVER_ACCESS_QOS_MODE (code=exited, status=0/SUCCESS)
        Main PID: 132712 (zbs-chunkd)
          Status: "Starting event loop..."
           Tasks: 21
          Memory: 112.0M
          CGroup: /smtx.slice/smtx-zbs.slice/smtx-zbs-chunkd.slice/zbs-chunkd.service
                  └─132712 /usr/sbin/zbs-chunkd --foreground
   ```
7. 等待 CloudTower 上该节点**存储服务健康状态异常**的告警取消。
8. 将节点退出存储维护模式，请参考《SMTX OS CLI 命令参考》确认 chunk ID 并[设置 chunk 退出存储维护模式](/smtxos/6.3.0/cli_guide/cli_guide_30)。
9. 在集群任意节点执行如下命令，确认数据恢复是否完成：

   `sudo zbs-meta pextent find need_recover`

   若返回 `No PExtents found.` 表示数据恢复完成。否则请等待一段时间再次数据恢复完成。

---

## 物理盘运维 > 下载物理盘日志

# 下载物理盘日志

物理盘日志中包含 S.M.A.R.T 日志、zbs-node 日志以及所属主机的 messages 日志，物理盘故障时日志将协助您快速定位故障。

1. 进入 CloudTower 的**物理盘**页面，在物理盘列表中单击故障物理盘右侧的 **···**，选择**下载日志**。
2. 在弹出的**下载物理盘日志**对话框中选择是否需要包含所属主机的 messages 日志。
3. 单击**下载**。

---

## 物理盘运维 > 定位物理盘

# 定位物理盘

通过物理盘的闪灯和灭灯您可以确定物理盘在服务器中的位置。

如您使用非 NVMe SSD 物理盘，且存储控制器在下表所示的兼容性范围内，您可以[通过 CloudTower 的闪灯和停止闪灯功能](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_113)快速定位物理盘在服务器中的位置。

如果使用的是 NVMe SSD 或存储控制器不在下表的兼容性范围内，请您根据物理盘驱动类型[使用 CLI 命令](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_26)定位。

| 服务器品牌 | 服务器型号 | 存储控制器型号 |
| --- | --- | --- |
| 戴尔 | PowerEdge C6420 | Dell HBA330 Mini |
| PowerEdge R750 | Dell HBA355i Fnt/Dell HBA350i Adp |
| PowerEdge R740xd | Dell HBA330 Adp |
| PERC H730P Mini |
| 联想 | ThinkSystem SR650 | ThinkSystem RAID 530-16i PCIe 12Gb Adapter |
| ThinkSystem 430-16i SAS/SATA 12Gb HBA |
| ThinkSystem RAID 530-8i PCIe 12Gb Adapter |
| Lenovo SR658H | ThinkSystem RAID 930-16i |
| 浪潮 | Inspur CS5280H | INSPUR PM8222-SHBA |
| Inspur NF5280M5 | INSPUR 3108MR-4GB |
| HPE | HPE ProLiant DL380 Gen10 | HPE Smart Array P816i-a SR Gen10 |
| 鲲泰 | KunTai R722 | Huawei SR150-M |
| AVAGO MegaRAID SAS 9460-8i |

---

## 物理盘运维 > 定位物理盘 > 通过 CloudTower 定位

# 通过 CloudTower 定位

1. 进入 CloudTower 的**物理盘**页面，在物理盘列表中选中物理盘。
2. 在弹出的物理盘详情面板中单击**闪灯**或**停止闪灯**，通过主机上物理盘的闪灯或灭灯确定物理盘的位置。

---

## 物理盘运维 > 定位物理盘 > 使用命令行定位

# 使用命令行定位

根据物理盘驱动类型的不同，操作闪灯所使用的命令和操作方式也不同，如下表所示。

| 物理盘驱动 | 使用的命令行 |
| --- | --- |
| ahci | `ledctl` |
| mpt2sas | `sas2ircu` |
| mpt3sas | `storcli` 或 `perccli (DELL)` |
| megaraid\_sas | `storcli` 或 `perccli (DELL)` |
| smartpqi | `arcconf` |

**操作步骤**

1. 执行如下命令，确认物理盘使用的驱动类型。此处以物理盘 `sdx` 为例：

   `udevadm info -a -n /dev/sdx | grep DRIVERS | egrep 'ahci|megaraid_sas|mpt2sas|mpt3sas|smartpqi|nvme'`

   若该物理盘驱动类型为 **ahci**，则输出信息如下。其他类型依此类推。

   `DRIVERS=="ahci"`
2. 确认物理盘序列号。

   使用 mpt2sas、mpt3sas、megaraid\_sas、smartpqi 驱动的物理盘，需要通过序列号定位物理盘所在的插槽号。

   | 操作 | 执行的命令 | 输出的信息 |
   | --- | --- | --- |
   | 查看指定物理盘的序列号  （以物理盘 sdx 为例） | `smartctl -i /dev/sdx | grep Serial` | `Serial Number: W462CK1F` |
   | 查看所有物理盘的序列号 | `lsblk -d -o NAME,SERIAL` | `NAME SERIAL` `sda 96D70756062400160899` `sdb BTHV519309ZA400NGN` `sdc BTHV5194065D400NGN` `sdd W462CK1F` `sde W462MH8S` `sdf W462MH87` `sdg W462CKCD` |
3. 操作物理盘闪灯/灭灯。

   - **ahci 驱动**

     以物理盘 sdx 为例：

     - 闪灯

       `ledctl locate=/dev/sdx`
     - 灭灯

       `ledctl locate_off=/dev/sdx`
   - **mpt2sas 驱动**

     对于 mpt2sas 驱动类型的物理盘，执行闪灯和灭灯操作需要额外获取物理盘的 **controller\_id**、**enclosure\_id** 和 **slot\_id**。

     1. 执行命令 `sas2ircu list`，输出内容如下，其中 Index 列对应的数字即为 **controller\_id**。

        ```
        LSI Corporation SAS2 IR Configuration Utility.
        Version 15.00.00.00 (2012.11.08)
        Copyright (c) 2009-2012 LSI Corporation. All rights reserved.

                Adapter      Vendor  Device                       SubSys  SubSys
        Index    Type          ID      ID    Pci Address          Ven ID  Dev ID
        -----  ------------  ------  ------  -----------------    ------  ------
        0      SAS2008        1000h    72h    00h:02h:00h:00h      1170h   6019h

        SAS2IRCU: Utility Completed Successfully.
        ```
     2. 根据前面步骤中获取的 **controller\_id** 来获取 **enclosure\_id** 和 **slot\_id**。

        `sas2ircu ${controller_id} display | egrep "Enclosure #|Slot #|Serial No" | grep -v Unit`

        执行命令后，输出如下内容。其中 **Enclosure #**、**Slot#** 和 **Serial No** 将成对出现，分别表示 **enclosure\_id**、**slot\_id** 和对应的物理盘序列号，由此可通过之前已获取的物理盘序列号来确定对应的插槽号。

        ```
        Enclosure #                             : 1
        Slot #                                  : 0
        Serial No                               : BTHV522308T3400NGN
        Enclosure #                             : 1
        Slot #                                  : 1
        Serial No                               : BTHV522301VC400NGN
        Enclosure #                             : 1
        Slot #                                  : 2
        Serial No                               : W461T787
        Enclosure #                             : 1
        Slot #                                  : 3
        Serial No                               : W461SGBK
        ```

        在获取了物理盘的 **controller\_id**、**enclosure\_id** 和 **slot\_id** 之后，即可执行闪灯和灭灯操作。
     3. 执行闪灯/灭灯操作。

        - 闪灯

          `sas2ircu $controller_id locate $enclosure_id:$slot_id on`  
          例如，对 controller\_id = 0，enclosure\_id=1，slot\_id=0 的物理盘执行闪灯操作 `sas2ircu 0 locate 1:0 on`。
        - 灭灯

          `sas2ircu $controller_id locate $enclosure_id:$slot_id off`  
          例如，对 controller\_id = 0，enclosure\_id=1，slot\_id=3 的物理盘执行灭灯操作 `sas2ircu 0 locate 1:3 off`。
   - **mpt3sas 和 megaraid\_sas 驱动**

     对于 mpt3sas 和 megaraid\_sas 驱动类型的物理盘，执行闪灯和灭灯操作还需要额外获取物理盘的槽位信息。

     - 服务器厂商为 DELL 时，请使用 `perccli` 命令获取信息；
     - 其他厂商服务器请使用 `storcli` 命令获取信息。

     `perccli` 和 `storcli` 命令的使用方式和输出内容基本一致，使用时请注意需输入完整的命令路径。下面以 `perccli` 命令为例，描述获取物理盘槽位信息的流程。

     1. 执行以下命令，列出物理盘的槽位和序列号。

        `/opt/MegaRAID/perccli/perccli64 /call/eall/sall show all | egrep "Device attributes|SN ="`

        执行完命令后，输出内容如下。**Device** 和 **SN** 将成对出现，分别表示物理盘槽位号和对应的物理盘序列号。

        ```
        Drive /c0/e4/s0 Device attributes :
        SN = 61K0A1KFFQYF
        Drive /c0/e4/s1 Device attributes :
        SN = 61K0A1LKFQYF
        ```
     2. 执行闪灯/灭灯操作。

        - 闪灯

          `/opt/MegaRAID/perccli/perccli64 /cx/ex/sx start locate`  
          例如，对槽位为 `/c0/e1/s1` 的物理盘执行闪灯操作：`/opt/MegaRAID/perccli/perccli64 /c0/e1/s1 start locate`。
        - 灭灯

          `/opt/MegaRAID/perccli/perccli64 /cx/ex/sx stop locate`  
          例如，对槽位为 `/c0/e1/s1` 的物理盘执行灭灯操作：`/opt/MegaRAID/perccli/perccli64 /c0/e1/s1 stop locate`。
   - **smartpqi 驱动**

     对于 smartpqi 驱动类型的物理盘，执行闪灯和灭灯操作需要额外获取物理盘的 **controller\_id**、**channel\_id** 和 **device\_id**。

     1. 执行命令 `/usr/Arcconf/arcconf list`，输出内容如下，其中 `Controller ID` 列对应的数字即为 **controller\_id**。在使用 `arcconf` 命令时，请务必输入完整的命令路径。

        ```
        Controllers found: 1
        ----------------------------------------------------------------------
        Controller information
        ----------------------------------------------------------------------
        Controller ID             : Status, Slot, Mode, Name, SerialNumber, WWN
        ----------------------------------------------------------------------
        Controller 1:             : Optimal, Slot 11, Mixed, INSPUR PM 8222-SHBA, SAMA22GP3910A60, 56C92BF000A1C676

        Command completed successfully.
        ```
     2. 根据前面步骤中获取的 **controller\_id** 来列出 **channel\_id** 和 **device\_id**。

        `/usr/Arcconf/arcconf getconfig ${controller_id} pd | egrep "Reported Channel|Serial number"`

        执行命令后，输出如下内容。**Channel,Device** 和 **Serial number** 成对出现，分别表示 **channel\_id**、**device\_id** 和对应的物理盘**序列号**，由此可通过之前已获取的物理盘序列号来确定对应的插槽号。

        ```
        Reported Channel,Device(T:L)         : 0,0(0:0)
        Serial number                        : 5QHMR5PB
        Reported Channel,Device(T:L)         : 0,1(1:0)
        Serial number                        : 5QHMWGXB
        Reported Channel,Device(T:L)         : 0,2(2:0)
        Serial number                        : 5QHNPB5B
        Reported Channel,Device(T:L)         : 0,3(3:0)
        Serial number                        : 5QHL8DMB
        Reported Channel,Device(T:L)         : 2,0(0:0)
        ```

        从示例输出内容中可以获取如下信息：**序列号**为 `5QHMR5PB` 的物理盘，其 **channel\_id** = `0`，**device\_id** = `0`；**序列号**为 `5QHMWGXB` 的物理盘，其 **channel\_id** = `0`，**device\_id** = `1`，以此类推。
     3. 执行闪灯/灭灯操作。

        - 闪灯

          `/usr/Arcconf/arcconf identify ${controller_id} device ${channel_id} ${device_id} start`

          例如，对 controller\_id = 0，channel\_id=1，device\_id=1 的物理盘执行闪灯操作 `/usr/Arcconf/arcconf identify 0 device 1 1 start`。
        - 灭灯

          `/usr/Arcconf/arcconf identify ${controller_id} device ${channel_id} ${device_id} stop`

          例如，对 controller\_id = 0，channel\_id=1，device\_id=2 的物理盘执行灭灯操作 `/usr/Arcconf/arcconf identify 0 device 1 2 stop`。

---

## 物理盘运维 > 挂载物理盘

# 挂载物理盘

挂载前请确认 SMTX OS 集群的部署模式，不同部署模式下允许挂载的物理盘不同：

- SMTX OS 集群采用不分层模式时，只允许挂载 SSD。
- SMTX OS 集群采用分层模式且缓存和数据共用所有物理盘时：

  - 节点配置为全 NVMe SSD 全闪配置时，只允许挂载 NVMe SSD。
  - 节点配置为全 SATA SSD 或 SAS SSD 全闪配置时，只允许挂载 SATA SSD 或 SAS SSD。
- SMTX OS 集群采用分层模式且缓存盘和数据盘独立部署时，允许挂载 SSD 和 HDD，但 HDD 只允许挂载为`数据盘`。

不同容量规格的主机可挂载的数据分区总容量限制请参考下表：

| 主机容量规格 | 数据分区总容量限制 |
| --- | --- |
| 标准容量 | 128 TiB |
| 大容量 | 256 TiB |

**风险提示**

挂载物理盘会清除该物理盘上的所有数据，请谨慎操作。

**操作步骤**

1. 在 CloudTower 主页面左侧导航栏中，选择一个组织、数据中心、集群或主机后，选择**全部** > **物理盘**，物理盘列表页面将会提示当前范围内健康且可挂载的物理盘的数量。
2. 选择待挂载的物理盘，您可以通过如下两种方式选择：

   - 单击 `x 块健康的物理盘可挂载。`提示右侧的**查看**，将会展示该范围下所有可挂载的物理盘，请您勾选同一集群内需要挂载的一个或多个物理盘，然后单击**挂载**。
   - 在物理盘列表中根据需求勾选属于同一集群的一个或多个状态为`健康盘·可挂载`的物理盘，单击**挂载**。
3. （可选）如果主机有多个物理盘池，系统将自动为每块物理盘选择一个物理盘池，您可以按需将物理盘移动至其他物理盘池中。请单击物理盘用途右侧的![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_071.png)按钮，选择目标物理盘池。

   > **说明**：
   >
   > - 单个物理盘池内物理盘的数据分区总容量不超过 256 TiB，缓存分区总容量不超过 51 TiB。
   > - 不同部署模式下，单个物理盘池中可挂载的物理盘数量不同：
   >
   >   - `分层模式且缓存和数据盘独立部署`时，单个物理盘池中最多可挂载 64 个物理盘。
   >   - `不分层模式`或`分层模式且缓存和数据共享所有物理盘`时，单个物理盘池中最多可挂载 32 个物理盘。
4. 弹出的**挂载物理盘**对话框中确认待挂载的物理盘及其所属的集群和主机，选择物理盘**用途**，单击**挂载 x 块物理盘**。

---

## 物理盘运维 > 卸载物理盘

# 卸载物理盘

当物理盘出现故障需要拔出时，请您先参照本章节内容在 CloudTower 中卸载物理盘，再从主机上拔出物理盘。

## 卸载要求

- **不允许**卸载启动盘。
- **不允许**卸载所属物理盘池中最后一块包含 Journal 分区的物理盘。
- `不分层模式`或`分层模式且缓存和数据共享所有物理盘`时，**不允许**卸载所属物理盘池中最后一块包含数据分区的物理盘。
- **不允许**卸载所属主机中最后一块包含元数据分区或最后一块包含系统分区的物理盘。
- **不允许**卸载发生 I/O 阻塞，已下线并停止处理任何 I/O 的物理盘。
- 如需卸载物理盘，物理盘所属的集群需要满足以下所有要求：

  - 无数据恢复；
  - 没有正在卸载的物理盘；
  - 集群中空闲缓存容量足以承载该物理盘缓存分区的数据；
  - 集群中空闲存储容量足以承载该物理盘数据分区的数据；
  - 集群中空闲常驻缓存容量足以承载常驻缓存卷在该物理盘上的数据。

## 卸载步骤

1. 进入 CloudTower 的**物理盘**页面，在物理盘列表中单击待卸除的物理盘右侧的 **...** 后，选择 **卸载**。
2. 在弹出的**卸载物理盘**对话框中根据物理盘的基本信息确认待卸载的物理盘及其所属的主机，单击**卸载**。

---

## 物理盘运维 > 更换物理盘

# 更换物理盘

如您需要更换集群中的物理盘，请您先通过 CloudTower [卸载物理盘](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_115)并确认数据迁移完成后，再根据物理盘的类型（HDD/SSD）参照本章节的内容，在服务器上更换物理盘。

> **风险提示**：
>
> 从服务器中强行拔除未卸载的物理盘，可能会导致用户业务中断甚至永久性丢失数据。

---

## 物理盘运维 > 更换物理盘 > 更换 SSD > 更换 SSD（ELF 平台）

# 更换 SSD（ELF 平台）

您可以参考本小节为 SMTX OS（ELF）集群的某个主机更换 SSD。

**适用场景**

SSD 的更换操作与集群部署时是否采用存储分层模式和该硬盘的用途有关。本节描述的步骤仅适用于以下两种场景：

- 集群采用存储分层模式，当前用途为`缓存盘`、`含元数据分区的缓存盘`、`数据盘`或`含元数据分区的数据盘`的 SSD 更换。
- 集群采用不存储分层模式，当前用途为`数据盘`的 SSD 更换。

对于采用不存储分层模式的集群，当前用途为`不含元数据分区的数据盘` 的 SSD 更换步骤请参考​[更换 HDD ​](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_17)。

对于当前用途为 `SMTX 系统盘`的 SSD 更换步骤请参考[更换 SMTX 系统盘](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_90)。

**准备工作**

- 确认即将安装的 SSD 与服务器机型兼容，可通过[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)进行查询，且即将安装的 SSD 的容量不低于原来的 SSD 的容量。
- 确定并记录待更换 SSD 所在的物理节点序列号、机架所在位置以及需要更换的物理盘槽位。可参考​[物理盘闪灯定位​](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_112)点亮物理盘的指示灯以确定物理盘在主机上的位置。
- 登录 CloudTower 管理平台，[卸载](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_115)该 SSD。

**操作步骤**

1. 按照下图所示操作，从主机上拔除 SSD。

   1. 按压释放按钮以打开硬盘托架释放手柄。
   2. 握住硬盘托架释放手柄，将硬盘托架滑出驱动器插槽。

   ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_039.png)
2. 登录 CloudTower，报警信息提示系统侦测到物理盘从主机上拔出，如果主机是多节点高密服务器或刀片服务器，拔除物理盘后还会提示该物理盘插槽在机箱中的位置。
3. 按照下图所示操作，在物理服务器上安装新的 SSD。

   1. 将新硬盘托架滑入硬盘插槽中。
   2. 合上硬盘托架释放手柄以将硬盘锁定到位。

   ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_040.png)
4. 登录 CloudTower，报警信息提示系统侦测到有新的物理盘插入主机，如果主机是多节点高密服务器或刀片服务器，还会提示该物理盘插槽在机箱中的位置。
5. 使用 SSH 方式登录 SSD 所在的主机，执行命令 `lsblk`，查看新安装的 SSD，此时物理盘尚未被分区，如下例所示的 **sdb**。

   ```
   NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
       sda 8:0 0 59.6G 0 disk
       └─sda1 8:1 0 200M 0 part /boot
       sdb 8:16 0 372.6G 0 disk
       sdc 8:32 0 372.6G 0 disk
       ├─sdc1 8:33 0 45G 0 part
       │ └─md127 9:127 0 45G 0 raid1 /
       ├─sdc2 8:34 0 20G 0 part
       │ └─md0 9:0 0 20G 0 raid1 /var/lib/zbs/metad
       ├─sdc3 8:35 0 10G 0 part
       └─sdc4 8:36 0 287.6G 0 part
       sdd 8:48 0 931.5G 0 disk
       └─sdd1 8:49 0 931.5G 0 part
       sde 8:64 0 931.5G 0 disk
       └─sde1 8:65 0 931.5G 0 part
       sdf 8:80 0 931.5G 0 disk
       └─sdf1 8:81 0 931.5G 0 part
       sdg 8:96 0 931.5G 0 disk
       └─sdg1 8:97 0 931.5G 0 part
       sr0 11:0 1 1.4G 0 rom
   ```
6. 登录 CloudTower，[挂载](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_114)新的 SSD。
7. 挂载成功后，可在主机的物理盘列表中确认该 SSD 的挂载状态为**已挂载**，更换操作结束。
8. 如果通过 CloudTower 挂载 SSD 失败，可参考如下步骤，通过命令行重新挂载 SSD，其中 `sdb` 表示挂载的 SSD 盘。

   - 更换的 SSD 为含元数据分区的缓存盘（存储分层模式），或者含元数据分区的数据盘（不存储分层模式）

     ```
     zbs-deploy-manage mount-disk /dev/sdb smtx_system
     ```

     再次执行命令 `lsblk`，确认新安装的 **sdb** 已成功分区。

     ```
     NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
     sdb 8:16 0 372.6G 0 disk
     ├─sdb1 8:17 0 85G 0 part
     │ └─md127 9:127 0 85G 0 raid1 /
     ├─sdb2 8:18 0 20G 0 part
     │ └─md0 9:0 0 20G 0 raid1 /var/lib/zbs/metad
     ├─sdb3 8:19 0 10G 0 part
     └─sdb4 8:20 0 247.6G 0 part`
     ```
   - 更换的 SSD 为含元数据分区的数据盘（存储分层模式单一类型 SSD 全闪配置）

     ```
     zbs-deploy-manage mount-disk /dev/sdb smtx_system
     ```

     再次执行命令 `lsblk`，确认新安装的 **sdb** 已成功分区。

     ```
     NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
     sdb         8:16   0   500G  0 disk
     ├─sdb4      8:20   0    20G  0 part
     ├─sdb2      8:18   0   100G  0 part
     │ └─md0     9:0    0   100G  0 raid1 /var/lib/zbs/metad
     ├─sdb5      8:21   0   175G  0 part
     ├─sdb3      8:19   0    10G  0 part
     └─sdb1      8:17   0   185G  0 part
     └─md127   9:127  0 184.9G  0 raid1 /
     ```
   - 更换的 SSD 为不含元数据分区的数据盘（存储分层模式单一类型 SSD 全闪配置）

     ```
     zbs-deploy-manage mount-disk /dev/sdb  data
     ```

     再次执行命令 `lsblk`，确认新安装的 **sdb** 已成功分区。

     ```
     NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
     sdb         8:48   0   500G  0 disk
     ├─sdb2      8:50   0    48G  0 part
     ├─sdb3      8:51   0   432G  0 part
     └─sdb1      8:49   0    10G  0 part
     ```
   - 更换的 SSD 为不含元数据分区的缓存盘（存储分层模式）

     ```
     zbs-deploy-manage mount-disk /dev/sdb cache
     ```

     再次执行命令 `lsblk`，确认新安装的 **sdb** 已成功分区。

     ```
     NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
     sdb 8:16 0 372.6G 0 disk
     ├─sdb1 8:19 0 10G 0 part
     └─sdb2 8:20 0 362.6G 0 part
     ```

---

## 物理盘运维 > 更换物理盘 > 更换 SSD > 更换 SSD（VMware ESXi 平台） > 更换 SAS/SATA SSD

# 更换 SAS/SATA SSD

更换步骤可参考[更换 SSD（ELF 平台）](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_65)。

---

## 物理盘运维 > 更换物理盘 > 更换 SSD > 更换 SSD（VMware ESXi 平台） > 更换 NVMe SSD

# 更换 NVMe SSD

## 适用场景

本节描述的步骤仅适用于为同时满足以下条件的 SMTX OS（VMware ESXi）集群主机更换 NVMe SSD。

- ESXi 版本为 8.0 U1 及以上。
- 待更换的 SSD 为 U.2 NVMe SSD。
- 已在集群的安装部署阶段为 ESXi 主机和 SCVM 配置相关参数以支持热插拔功能。具体可参考《SMTX OS 集群安装部署指南（VMware ESXi 平台）》中的[修改 ESXi 主机的参数](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_28)和[为 NVMe 直通硬盘热插拔功能设置 SCVM](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_99) 章节。

## 更换步骤

### 准备 vmpctl 文件

1. 根据本地主机的 CPU 架构和操作系统下载适配的 vmpctl 文件。
2. 将 vmpctl 文件重新命名并赋予可执行权限。

   - 如果本地主机的操作系统是 Linux 或 macOS，请重新命名为 **vmpctl**，然后进入该文件所在目录，执行命令 `chmod a+x vmpctl` 赋予可执行权限。
   - 如果本地主机的操作系统是 Windows，请重新命名为 **vmpctl.exe**，然后关闭杀毒软件或者将该软件添加至杀毒软件白名单，避免文件被杀毒软件误删。

### 热移除 NVMe SSD

1. 在本地主机上使用终端工具打开 vmpctl 文件，执行如下命令，通过 vSphere API 将 NVMe SSD 从 SCVM 中热移除。

   其中 NVMe SSD 的 ESXi PCI ID 可参考[附录](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_68)中的方法，根据 NVMe SSD 名称获取。

   ```
   ./vmpctl remove --address=<ESXI_IP> --username=<ESXI_USER> --password=<ESXI_PASSWORD> --vm=<SCVM_NAME> --device=<ESXI_PCI_ID>
   ```

   | 参数 | 说明 |
   | --- | --- |
   | `ESXI_IP` | ESXi 主机的 IP 地址 |
   | `ESXI_USER` | ESXi 主机的用户名 |
   | `ESXI_PASSWORD` | ESXi 主机的密码 |
   | `SCVM_NAME` | SCVM 的名称 |
   | `ESXI_PCI_ID` | NVMe SSD 的 ESXi PCI ID |

   > **注意**：
   >
   > - 当本地主机的操作系统是 macOS 时，如果在打开 vmpctl 文件时出现弹窗提示无法打开，可能是由于该文件被系统自动阻止使用，可以单击弹窗右上角的 **?** 图标，参考弹出的说明信息打开此文件。
   > - 如果 ESXi 主机的用户名或密码包含特殊字符，且本地主机的操作系统为 Linux 或 macOS，执行命令时需要在用户名或密码两侧添加单引号（'）。

   - 如果输出结果中显示 `remove device success`，表示移除成功。
   - 如果输出结果中显示 `remove device failed`，表示移除失败，可在 ESXi 主机中执行 `dmesg -T | tail` 命令，根据 kernel 日志确定是否有硬件不兼容的情况，解决问题后重试。
2. 可选：在 SCVM 中执行 `lsblk`、`lspci` 或 `mdadm` 命令确认 NVMe SSD 是否已正常移除。

   - 执行 `lsblk -bld` 命令，查看所有硬盘信息，如果输出结果不包含已移除硬盘，则表示设备已正常移除。

     ![](https://cdn.smartx.com/internal-docs/assets/937061e9/esxi_hotplug_01.png)
   - 执行 `lspci` 命令，查看所有 PCI 设备信息，如果输出结果中不包含已移除硬盘，则表示设备已正常移除。

     ![](https://cdn.smartx.com/internal-docs/assets/937061e9/esxi_hotplug_02.png)
   - 以名称为 md127 的 RAID 阵列为例，执行 `mdadm -D /dev/md127` 命令，查看 RAID 阵列信息，其中 **md127** 表示已移除硬盘所在 RAID 阵列的名称，如果输出结果中显示状态为 removed，则表示设备已正常移除。

     ![](https://cdn.smartx.com/internal-docs/assets/937061e9/esxi_hotplug_03.png)
3. 将已移除的 NVMe SSD 从物理服务器中拔除。

### 热添加 NVMe SSD

1. 将 NVMe SSD 安装至物理服务器。
2. SSH 登录 NVMe SSD 所在的 ESXi 主机，执行如下命令获取所有 NVMe SSD 信息，根据硬盘的 Physical Slot 和 Slot Description 确认对应的硬盘，其中 Address 所示 ID 即为该硬盘的 ESXi PCI ID。

   ```
   esxcli hardware pci list --class=0x0108
   ```

   ![](https://cdn.smartx.com/internal-docs/assets/2850888f/esxi_hotplug_04.png)
3. 在本地主机上使用终端工具打开 vmpctl 文件，执行如下命令，将 NVMe SSD 热添加到 SCVM 中。

   ```
   ./vmpctl add --address=<ESXI_IP> --username=<ESXI_USER> --password=<ESXI_PASSWORD> --vm=<SCVM_NAME> --device=<ESXI_PCI_ID>
   ```

   | 参数 | 说明 |
   | --- | --- |
   | `ESXI_IP` | ESXi 主机的 IP 地址 |
   | `ESXI_USER` | ESXi 主机的用户名 |
   | `ESXI_PASSWORD` | ESXi 主机的密码 |
   | `SCVM_NAME` | SCVM 的名称 |
   | `ESXI_PCI_ID` | NVMe SSD 的 ESXi PCI ID |

   > **注意**：
   >
   > - 当本地主机的操作系统是 macOS 时，如果在打开 vmpctl 文件时出现弹窗提示无法打开，可能是由于该文件被系统自动阻止使用，可以单击弹窗右上角的 **?** 图标，参考弹出的说明信息打开此文件。
   > - 如果 ESXi 主机的用户名或密码包含特殊字符，且本地主机的操作系统为 Linux 或 macOS，执行命令时需要在用户名或密码两侧添加单引号（'）。

   - 如果输出结果中显示 `add device success`，表示添加成功。
   - 如果输出结果中显示 `add device failed`，表示添加失败，可在 ESXi 主机中执行 `dmesg -T | tail` 命令，根据 kernel 日志确定是否有硬件不兼容的情况，解决问题后重试。
4. 参考以下步骤，挂载物理盘。

   - 如果更换的 NVMe SSD 是含元数据分区的缓存盘（存储分层模式），或者含元数据分区的数据盘（不存储分层模式），需在 SCVM 中执行如下命令，其中 **nvme1n1** 表示待挂载 NVMe SSD的名称。

     ```
     zbs-deploy-manage mount-disk /dev/nvme1n1 smtx_system
     ```

     如果输出结果中显示 `Mount disk: /dev/nvme1n1 success!`，表示挂载成功。
   - 如果更换的 NVMe SSD 是不含元数据分区的缓存盘（存储分层模式），需在 SCVM 中执行如下命令，其中 **nvme2n1** 表示待挂载 NVMe SSD的名称。

     ```
     zbs-deploy-manage mount-disk /dev/nvme2n1 cache
     ```

     如果输出结果中显示 `Mount disk: /dev/nvme2n1 success!`，表示挂载成功。
5. 在 SCVM 中执行 `lsblk` 命令，确认新安装的 NVMe SSD 已成功分区。

---

## 物理盘运维 > 更换物理盘 > 更换 HDD

# 更换 HDD

**准备工作**

- 确认即将安装的 HDD 与服务器机型兼容，可通过[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)进行查询，且即将安装的 HDD 的容量不低于原来的 HDD 的容量。
- 确定并记录待更换 HDD 所在的物理节点序列号、机架所在位置以及待更换的物理盘槽位。可参考​​[定位物理盘​](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_112)点亮物理盘的指示灯以确定物理盘在主机上的位置。
- 登录 CloudTower 管理平台，[卸载](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_115)待更换的 HDD。

**操作步骤**

1. 按照下图所示操作，从主机上拔除 HDD。

   1. 按压释放按钮以打开硬盘托架释放手柄。
   2. 握住硬盘托架释放手柄，将硬盘托架滑出驱动器插槽。

   ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_039.png)
2. 登录 CloudTower，报警信息提示系统侦测到物理盘从主机上拔出，如果主机是多节点高密服务器或刀片服务器，拔除物理盘后还会提示该物理盘插槽在机箱中的位置。
3. 按照下图所示操作，在物理服务器上安装新的 HDD。

   1. 将新硬盘托架滑入硬盘插槽中。
   2. 合上硬盘托架释放手柄以将硬盘锁定到位。

   ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_040.png)
4. 登录 CloudTower，报警信息提示系统侦测到有新的物理盘插入主机，如果主机是多节点高密服务器或刀片服务器，还会提示该物理盘插槽在机箱中的位置。
5. 使用 SSH 方式登录 HDD 所在的主机，执行命令 `lsblk`，查看新安装的 HDD，此时物理盘尚未被分区，如下例所示的 **sdf**。

   ```
    NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
       sda 8:0 0 59.6G 0 disk
       └─sda1 8:1 0 200M 0 part /boot
       sdb 8:16 0 372.6G 0 disk
       ├─sdb1 8:17 0 45G 0 part
       │ └─md127 9:127 0 45G 0 raid1 /
       ├─sdb2 8:18 0 20G 0 part
       │ └─md0 9:0 0 20G 0 raid1 /var/lib/zbs/metad
       ├─sdb3 8:19 0 10G 0 part
       └─sdb4 8:20 0 287.6G 0 part
       sdc 8:32 0 372.6G 0 disk
       ├─sdc1 8:33 0 45G 0 part
       │ └─md127 9:127 0 45G 0 raid1 /
       ├─sdc2 8:34 0 20G 0 part
       │ └─md0 9:0 0 20G 0 raid1 /var/lib/zbs/metad
       ├─sdc3 8:35 0 10G 0 part
       └─sdc4 8:36 0 287.6G 0 part
       sdd 8:48 0 931.5G 0 disk
       └─sdd1 8:49 0 931.5G 0 part
       sde 8:64 0 931.5G 0 disk
       └─sde1 8:65 0 931.5G 0 part
       sdf 8:80 0 931.5G 0 disk
       sdg 8:96 0 931.5G 0 disk
       └─sdg1 8:97 0 931.5G 0 part
       sr0 11:0 1 1.4G 0 rom
   ```
6. 登录 CloudTower，[挂载](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_114)新的物理盘。
7. 挂载成功后，可在主机的物理盘列表中确认该 HDD 的挂载状态为**已挂载**，更换操作结束。

   如果通过 CloudTower 挂载 HDD 失败，可在 HDD 所在的节点执行如下命令，重新挂载 HDD，其中 **sdf** 表示挂载的 HDD 盘。

   ```
   ```
   zbs-deploy-manage mount-disk /dev/sdf data
   ```
   ```

   系统输出如下信息，表明挂载物理盘成功。

   ```
   ```
   2017-06-14 10:42:31,382 INFO mount_extent_disk: Start mount extent disk: /dev/sdf
   2017-06-14 10:42:31,562 INFO run: waiting zbs-chunkd start .....
   ......
   2017-06-14 10:42:33,141 INFO run: Number Start End Size File system Name Flags
   2017-06-14 10:42:33,141 INFO run: 1 0.02MiB 953870MiB 953870MiB 1
   2017-06-14 10:42:33,141 INFO run:
   2017-06-14 10:42:33,141 INFO run: Format disk using zbs-chunk partition:/dev/sdf1
   2017-06-14 10:42:33,542 INFO run: Format succeed
   2017-06-14 10:42:33,542 INFO run: Mount disk using zbs-chunk
   2017-06-14 10:42:34,074 INFO run: Mount succeed
   d2017-06-14 10:42:35,175 INFO mount_extent_disk: Mount extent disk: /dev/sdf success!
   ```
   ```

---

## 物理盘运维 > 更换 SMTX 系统盘

# 更换 SMTX 系统盘

本小节介绍了在 SMTX OS 集群的主机上更换 SMTX 系统盘中的成员物理盘的操作方法。

定位物理盘槽位前，请您确认存储控制器型号以及是否支持物理盘闪灯功能：

- 如果存储控制器支持物理盘闪灯，此时可以快速通过界面的闪灯功能确定物理盘的槽位，而支持物理盘闪灯也通常意味着支持物理盘热插拔，请参考[不停机更换物理盘](#%E4%B8%8D%E5%81%9C%E6%9C%BA%E6%9B%B4%E6%8D%A2%E7%89%A9%E7%90%86%E7%9B%98)章节内容更换该物理盘。
- 如果存储控制器不支持物理盘闪灯，则可以通过物理盘序列号定位其槽位，而不支持物理盘闪灯也通常意味着不支持物理盘热插拔，请参考[停机更换物理盘](#%E5%81%9C%E6%9C%BA%E6%9B%B4%E6%8D%A2%E7%89%A9%E7%90%86%E7%9B%98)章节内容关停服务器并更换物理盘。

> **说明：**
>
> SMTX 系统盘的成员物理盘仅能通过**成员物理盘**页签内的**序列号**识别，`0 号`和 `1 号`仅代表成员物理盘的序号，无法唯一标识这块盘。

## 不停机更换物理盘

1. 通过 CloudTower 或 BMC 界面对指定物理盘发起闪灯。

   - Broadcom MegaRAID（LSI SAS3XXX）支持通过 CloudTower 发起闪灯。

     1. 进入 CloudTower 的**主机**概览页面，查看 **SMTX 系统盘**详情。
     2. 在弹出的 SMTX 系统盘详情面板中选择**成员物理盘**页签，单击 **···**，选择**闪灯**或**停止闪灯**，通过主机上物理盘的闪灯或灭灯确定物理盘的位置。
   - 其他型号的存储控制器可能支持通过 BMC 发起闪灯，例如 Dell BOSS-N1 支持通过 iDRAC 界面发起闪灯，具体操作请查阅相关厂商的说明文档。
2. 根据服务器的闪灯提示拔除故障的物理盘，并在原来物理盘的槽位中插入新的物理盘。

   > **注意：**
   >
   > 请确保更换的新物理盘与原 RAID 组中的成员物理盘规格一致。
3. 等待存储控制器完成硬件 RAID 重建，使两块物理盘之间的数据完成同步。

   该操作流程全程不影响服务器和操作系统正常运行。

## 停机更换物理盘

1. 通过 CloudTower 界面或者 BMC 界面确认物理盘序列号。

   - 通过 CloudTower 查看物理盘序列号。

     1. 进入 CloudTower 的**主机**概览页面，查看 **SMTX 系统盘**详情。
     2. 在弹出的 SMTX 系统盘详情面板中选择**成员物理盘**页签，查看**序列号**。
   - 通过服务器的 BMC 界面查看物理盘序列号，具体操作请查阅相关厂商的说明文档。
2. 登录 CloudTower，将待更换物理盘的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
3. 在 CloudTower 中[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)该节点。
4. 断开服务器机箱电源，并打开服务器机箱外壳。
5. 根据序列号拔除故障的物理盘，并在原来物理盘的槽位中插入新的物理盘。

   > **注意：**
   >
   > 请确保更换的新物理盘与原 RAID 组中的成员物理盘规格一致。
6. 恢复服务器机箱外壳并接入机箱电源，启动服务器。
7. 登录 CloudTower，将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。
8. 等待存储控制器完成[硬件 RAID 重建](#%E6%9F%A5%E7%9C%8B%E7%A1%AC%E4%BB%B6-raid-%E9%87%8D%E5%BB%BA%E8%BF%9B%E5%BA%A6)，使两块物理盘之间的数据完成同步。

   硬件 RAID 的重建过程不影响服务器和操作系统正常运行。

## 查看硬件 RAID 重建进度

SMTX 系统盘中的成员物理盘更换新盘后，正常情况下存储控制器会自动重建 RAID，使两块物理盘之间的数据同步。在重建的过程中，RAID 组会处于 “降级（degraded）”状态，待重建完毕后 RAID 状态将会恢复正常。

不同型号的控制器和服务器查看硬件 RAID 重建进度的方式各不相同，下表仅列出几款常见的、用于 SMTX 系统盘的存储控制器、对应的 BMC 系统以及查看重建进度的命令行工具，不同 BMC 系统的界面各不相同，请参照各厂商的说明文档进行操作。

| 品牌 | BMC 系统 | RAID 控制器 | 命令行工具 |
| --- | --- | --- | --- |
| Dell PowerEdge | iDRAC | Marvell SATA M.2（Dell BOSS-S1/S2） | mvcli |
| Marvell NVMe M.2（Dell BOSS-N1） | mnvcli |
| Lenovo ThinkSystem | XClarity | Marvell SATA M.2（ThinkSystem M.2 SATA 2-Bay RAID） | mvcli |
| Marvell NVMe M.2（ThinkSystem M.2 NVMe 2-Bay RAID） | mnvcli |
| xFusion | iBMC | Broadcom MegaRAID（LSI SAS3XXX） | storcli |

### 使用 mvcli 查看

通过 `mvcli info -o vd` 查看 RAID 重建进度，在如下所示的输出内容中查看 **BGA progress**。

```
$ mvcli info -o vd
Virtual Disk Information
-------------------------
id:                  0
name:                test_raid1
status:              degraded
Stripe size:         64
RAID mode:           RAID1
Cache mode:          Not Support
size:                457798 M
BGA status:          running
Block ids:           0 4
# of PDs:            2
PD RAID setup:       0 1
Running OS:          yes
BGA progress:    rebuilding is 15% done
Total # of VD:       1
```

### 使用 mnvcli 查看

通过如下命令查看 RAID 重建进度：

- Dell PowerEdge 服务器请使用 `/opt/marvell/mnvcli/dell/mnv_cli`
- Lenovo ThinkSystem 服务器请使用 `/opt/marvell/mnvcli/lenovo/mnv_cli`

并在如下所示的输出内容中查看 **BGA progress**。

```
$ /opt/marvell/mnvcli/dell/mnv_cli info -o vd
VD ID:               0
Name:                VD_0
Status:              Degrade
Importable:          No
RAID Mode:           RAID1
size:                447 GB
PD Count:            2
PDs:                 0 1
Stripe Block Size:   128K
Sector Size:         512 bytes
VD is secure:        No
BGA progress:        Rebuilding is running in 21%
Total # of VD:       1
```

### 使用 iBMC 查看

在使用 iBMC 和 Broadcom MegaRAID 存储控制器的服务器上，您可以通过 iBMC 界面观察到 RAID 重建进度，如下图所示的 **Rebuild Status**：

![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_067.png)

重建完毕后，新插入的磁盘会自动重新加入 RAID 组：

![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_068.png)

---

## 其他部件运维 > 增加内存

# 增加内存

当 SMTX OS 集群的 CPU 使用率不高，空闲的存储资源较多，但可分配的内存比较紧张时，建议为集群的主机增加内存。

**准备工作**

在关机增加内存前，请按照如下要求检查待安装的内存条和集群状态，并做好准备。

- 检查正在运行的主机中的内存条和待增加的内存条，确保这两个内存条的型号与主频一致。
- 对于 SMTX OS（VMware ESXi）集群，请参考 VMware 官方文档，手动将待增加内存的 ESXi 主机上的虚拟机全部迁移至其他 ESXi 主机。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间增加内存，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间增加内存，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，将待增加内存的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 在 CloudTower 中[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)该节点。
3. 为服务器安装新内存条，并记录内存安装槽位，然后启动服务器。
4. 登录节点的 IPMI 管理台，确认 IPMI 管理台已识别新增加的内存。
5. 登录 CloudTower，将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。
6. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`
7. 登录 CloudTower，进入该主机的概览界面，查看**主机信息**模块中的**内存容量**参数，确认主机的内存容量已增加。

---

## 其他部件运维 > 更换内存

# 更换内存

**准备工作**

在关机更换内存前，请按照如下要求检查新的内存和集群状态，并做好准备。

- 检查主机中的故障内存和即将安装的内存，确保这两个内存的型号与主频一致。
- 对于 SMTX OS（VMware ESXi）集群，请参考 VMware 官方文档，手动将待更换内存的 ESXi 主机上的虚拟机全部迁移至其他 ESXi 主机。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间更换内存，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换网卡，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，将待更换内存的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 在 CloudTower 中[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)该节点。
3. 更换内存，并记录内存安装槽位。
4. 启动服务器，开机后登录节点的 IPMI 管理台，确认 IPMI 管理台已识别新更换的内存。
5. 登录 CloudTower，将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。
6. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`
7. 登录 CloudTower，进入该主机的概览界面，查看**主机信息**模块中的**内存容量**参数，确认主机的内存容量显示符合预期。

---

## 其他部件运维 > 增加网卡

# 增加网卡

当 SMTX OS 集群承载的业务越来越多，虚拟机网络的带宽出现瓶颈时，可以通过在服务器节点上增加网卡来提升网络带宽。

> **说明**：
>
> 如果增加网卡的目的是为了增加带宽而不是仅用于高可用，建议对 RDMA 网卡使用 balance-tcp 绑定模式，其他网卡可按需使用 balance-tcp 或 balance-slb 绑定模式。

**准备工作**

在关机增加网卡前，请按照如下要求检查待安装的网卡和集群状态，并做好准备。

- 确认新增的网卡与服务器机型兼容，可通过[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)进行查询。
- 对于 SMTX OS（VMware ESXi）集群，请参考 VMware 官方文档，手动将待增加网卡的 ESXi 主机上的虚拟机全部迁移至其他 ESXi 主机。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间增加网卡，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间增加网卡，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，将待增加网卡的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 在 CloudTower 中[关闭](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_120)该节点。
3. 在服务器中插入新网卡，然后启动服务器。
4. 登录节点的 IPMI 管理台，确认 IPMI 管理台已识别新增加的网卡。
5. 登录 CloudTower，将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。
6. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`
7. 将待增加网卡的虚拟分布式交换机与新添加的网口完成关联。

   - **ELF 平台**

     登录 CloudTower，在集群的虚拟分布式交换机列表中选中待增加网卡的虚拟分布式交换机，单击右侧的 **...** 后选择**编辑**，在弹出的**编辑虚拟分布式交换机**对话框里勾选新增的网口前的复选框，并保存设置。
   - **VMware ESXi 平台**

     通过 VMware vSphere Web Client 登录到 vCenter Server，并浏览到新增加网卡的 ESXi 主机，将新添加的物理网络适配器与虚拟机网络的标准交换机绑定。
8. 确认集群的虚拟机网络可正常访问。

   将集群中其他节点上的一台虚拟机手动迁移至已增加网卡的节点上，并登录该虚拟机的操作系统，若能 ping 通其他虚拟机，表明虚拟机网络正常。

---

## 节点运维

# 节点运维

SMTX OS 软件可运行在物理服务器上或者虚拟机中，而**节点**特指运行了 SMTX OS 软件的单个**物理服务器**或者**虚拟机**。

---

## 节点运维 > 设置维护模式

# 设置维护模式

在离线维护时使用维护模式，系统将自动检查集群和节点的状态，确保集群里其它节点的关键服务运行正常，保障集群剩余数据的安全提高运维效率。

**推荐**在以下场景使用维护模式：

- 升级时，例如升级固件、升级内核等。
- 更换除物理盘以外的硬件时，例如更换内存、网卡、CPU、存储控制器等。
- 从集群中移除节点时。

---

## 节点运维 > 设置维护模式 > 维护流程

# 维护流程

根据集群所使用的虚拟化平台查看对应的使用维护模式的流程。

**ELF 平台**

![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_069.png)

**VMware ESXi 平台**

SMTX OS（VMware ESXi）集群使用此模式时，可能需要同时使用 ESXi 主机的维护模式：

![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_070.png)

- **进入维护模式前**：系统进行预检查，集群和主机或 SCVM 状态符合要求才允许进入维护模式。
- **进入维护模式中**：设置主机或 SCVM 进入维护模式，主机或 SCVM 状态为`进入维护模式中`。

  SMTX OS（ELF）集群的主机进入维护模式的过程中，系统会自动将该主机上所有`运行中`的虚拟机热迁移至集群中的其他主机，无法完成热迁移的虚拟机在您确认后关机，开启了 HA 的虚拟机冷迁移至集群中的其他主机。

  此过程中如出现数据恢复则立即停止进入维护模式，待数据恢复完成后主机或 SCVM 将继续进入维护模式。
- **主机或 SCVM 处于维护模式**：任务中心提示进入维护模式成功或主机或 SCVM 状态更新为`维护模式`后，您可以对主机或 SCVM 进行离线升级或运维操作。

  - 三副本数据的异常副本位于该主机或 SCVM ，且其他主机或 SCVM 上仍有两个健康副本时，系统不会触发数据恢复。
  - 两副本数据的异常副本或纠删码的异常分片位于该主机或 SCVM 时，系统将在极短时间内自动触发数据恢复。
  - 主机或 SCVM 处于维护模式 7天后，系统将自动开始恢复主机或 SCVM 上的冷数据。
- **退出维护模式**：系统进行退出检查，主机或 SCVM 符合要求才允许退出维护模式。

  SMTX OS（ELF）集群的主机在退出维护模式时，可以选择将进入维护模式前自动迁出的虚拟机迁回当前主机、将自动关闭的虚拟机开机。

---

## 节点运维 > 设置维护模式 > 进入维护模式

# 进入维护模式

系统通过预检查，确认集群和主机的状态满足进入维护模式的条件后，才允许主机进入维护模式。

**注意事项**

进入维护模式的主机将不再接受任何虚拟机的调度操作，包括虚拟机开机、创建虚拟机、迁移虚拟机或 HA 至此主机。

**操作步骤**

1. 在 CloudTower 的主机列表单击目标主机或 SCVM 右侧的 **...** 后，选择**进入维护模式**。
2. 在弹出的**进入维护模式**对话框中，系统将执行如下预检查。部分检查结果不满足要求时，请参照操作建议手动调整，然后再次尝试进入维护模式。

   | 预检查要求 | 检查项不符合要求时的操作建议 |
   | --- | --- |
   | 当前主机上不存在需要迁出的业务虚拟机，或需要迁出的虚拟机不包含“必须”类型且已启用的放置组规则。 | - 选择**允许忽略规则**，系统将忽略放置组规则迁移虚拟机，此时集群可能存在虚拟机不符合放置组的告警，属于预期行为。 - 选择**必须遵循规则**，系统将遵守放置组规则迁移虚拟机。 |
   | （仅 ELF 平台）当前主机上不存在运行中的虚拟机或运行中的虚拟机可全部迁出。 | - 手动调整集群资源。 - 将`运行中`且不可迁出的虚拟机关机。 - 勾选**将无法迁出的虚拟机关机**。 |
   | （仅 ELF 平台）当前主机上不存在开启了 HA 的虚拟机或开启了 HA 的虚拟机可全部迁出。 | - 手动调整集群资源。 - 手动迁出虚拟机。 |
   | （仅 ELF 平台）当前主机上不存在`暂停`或`未知`状态的虚拟机。 | 手动调整虚拟机。 |
   | （仅 ELF 平台）当前主机上虚拟机（包含回收站内虚拟机）数量不超过 150 个。 | 将部分虚拟机迁出当前主机。 |
   | 当前主机不存在只有一个副本的数据。 | - 调整副本策略。 - 等待完成数据恢复。 |
   | 当前主机的存储网络连接正常。 | 修复故障。 |
   | 集群中不存在主机或 SCVM 处于`进入维护模式中`或`维护模式`状态。 | 等待其他主机完成维护任务并退出维护模式。 |
   | 集群无数据恢复。 | 等待数据恢复完成。 |
   | 集群中其他节点中空闲存储空间充足，即满足如下两个条件： - 集群剩余节点可用存储容量 > 该节点已使用存储容量 - 集群剩余节点可用写缓存容量 > 该节点已使用写缓存容量 | - 扩容集群。 - 删除部分快照或虚拟机以释放集群容量。 - 如判断可以在 7天内完成线下维护的，确认风险后也允许进入维护模式。 |
   | 以下服务运行状态均满足条件： - 除当前节点外，集群的 `zookeeper`、`mongodb` 服务不存在异常； - 集群的其他节点中，存在 `zbs-meta` 服务运行正常的节点； - 如集群中存在冗余策略使用纠删码的虚拟卷或 NFS Export，除当前节点外，包含健康且非移除中的存储服务的节点数量不少于任一虚拟卷或 NFS Export 纠删码配置的数据块（K）和校验块（M）数量之和； - 当前节点的 `job-center-worker` 服务运行正常； - 当前节点的 `libvirt` 服务运行正常； | 修复故障。 |

   > **说明**：
   >
   > - 如当前主机存在启用 DRS 自动迁移的虚拟机，可能导致虚拟机在主机维护模式期间发生位置变更，从而无法在退出维护模式时自动迁回至当前主机。请单击**编辑 DRS 设置**跳转至动态资源调度页面，按需调整 DRS 自动迁移的设置，参数说明请参考《SMTX OS 管理指南》的[动态资源调度的设置选项](/smtxos/6.3.0/os_administration_guide/os_administration_guide_198)章节。
   > - 如 SMTX OS（ELF）集群部署了文件存储集群，且文件控制器位于当前主机，请单击文件控制器名称跳转至文件控制器页面，将该文件控制器下线。1.2.0 及以上版本的文件存储集群请参考《SMTX 文件存储用户指南》下线文件控制器章节，1.2.0 以下版本请联系售后协助下线。
   > - 当 SMTX OS（ELF）集群部署了 Everoute 服务或 SKS 服务，且系统服务虚拟机位于当前主机，主机进入维护模式时，这些系统服务虚拟机将自动忽略已启用的“必须”类型的放置组规则迁移，且该迁移不会对业务造成影响。
   > - 当 CloudTower 启用 HA ，且高可用节点位于当前主机，主机进入维护模式时，高可用节点将自动忽略已启用的“必须”类型的放置组规则迁移，且该迁移不会对业务造成影响。
   > - 如目标主机可为虚拟机预留的 CPU 不足导致虚拟机迁移失败，请根据目标主机可用资源调整该虚拟机的 CPU 预留。
3. 所有检查项目全部满足要求，单击对话框右下方的**进入维护模式**。
4. SMTX OS（VMware ESXi）集群如需使用 ESXi 主机维护模式，请您参考 VMware 官方文档操作。

---

## 节点运维 > 设置维护模式 > 退出维护模式

# 退出维护模式

完成离线升级或维护之后，可以将主机退出维护模式。退出前，SMTX OS 也会进行退出检查，确认主机或 SCVM 满足退出该模式的条件后，才允许主机或 SCVM 退出维护模式。

**操作步骤**

1. 在 CloudTower 的主机列表单击处于维护模式的主机右侧的 **...** 后，选择**退出维护模式**，或在主机概览页面单击**退出维护模式**。
2. 在弹出的**退出维护模式**对话框中，系统将执行如下检查。部分检查结果不满足要求时，请参照操作建议手动调整主机，然后再次尝试退出维护模式。

   | 检查项目 | 检查项不符合要求时的操作建议 |
   | --- | --- |
   | 以下服务运行状态均满足条件： - 当前节点的 `job-center-worker`、`zbs-iscsi-redirectord` 服务运行正常 - （仅 ELF 平台）当前节点的 `libvirt`、`elf-vm-monitor` 服务运行正常 | 修复故障。 |
   | 当前主机的存储网络连接正常。 | 修复故障。 |
3. 所有检查项目全部满足要求时：

   - SMTX OS（ELF）集群：在对话框中确认是否同时将进入维护模式时迁出的虚拟机迁回、是否将关机的虚拟机开机，然后单击**退出维护模式**。

     > **说明：**
     >
     > - 退出维护模式的虚拟机放置组操作策略会与进入维护模式时保持一致。如果进入时选择**允许忽略规则**，则退出时也会忽略规则；如果进入时选择**必须遵循规则**，则退出时也会遵循规则。
     > - 如果在主机维护期间，虚拟机运行状态、虚拟机所在主机已经发生变化，或虚拟机挂载了直通设备，退出维护模式时，系统无法自动迁回或开启虚拟机，请您退出维护模式后手动处理。
   - SMTX OS（VMware ESXi）集群：单击**退出维护模式**。
4. 如进入维护模式前下线了 SFS 服务的文件控制器，退出维护模式后，请将文件控制器上线。1.2.0 及以上版本的 SFS 服务请参考《SMTX 文件存储用户指南》上线文件控制器章节，1.2.0 以下版本请联系售后协助上线。

---

## 节点运维 > 关闭节点

# 关闭节点

您可以在 CloudTower 上便捷地关闭 SMTX OS 集群的主机和 SCVM，在 CloudTower 关闭 SCVM 不会对 ESXi 主机的电源状态造成影响。

更换硬件时，例如更换内存、网卡、CPU、存储控制器等，请将节点进入维护模式然后使用此功能关闭节点后进行线下维护操作。如遇需要紧急关闭节点的情况，可以在非维护模式下强制关闭。

同一集群内，同一时间仅允许进行一个关闭节点的任务。

**风险提示**

SMTX OS（ELF）集群中部署了文件存储集群时，对于每个文件存储集群，如果关闭 2 个及以上文件控制器所在的节点，可能会造成文件存储集群及其提供的文件存储服务不可用。

**前提条件**

- 当前节点处于`健康`、`初始化`或`异常`状态。
- 当前节点关闭后，所在集群中的剩余节点满足选举主节点的数量要求。
- 所在集群未使用当前节点的管理 IP 来关联 CloudTower。
- 当前节点处于维护模式。

  若节点未处于维护模式时强制关闭，请确保满足以下条件：

  - CloudTower 虚拟机不能位于当前主机之上（若 CloudTower 已启用高可用，则 CloudTower 高可用节点不能位于当前主机之上）。
  - 如集群中存在冗余策略使用纠删码的虚拟卷，除当前节点外，所在集群中包含健康且非移除中的存储服务的节点数量不少于任一虚拟卷纠删码配置的数据块数量（K）。
  - 集群中其他节点中空闲存储空间充足，即满足如下两个条件：
    - 集群剩余节点可用存储容量 > 该节点已使用存储容量
    - 集群剩余节点可用写缓存容量 > 该节点已使用写缓存容量
  - 当前节点中不存在只有一个副本的数据。

**注意事项**

- 未设置节点进入维护模式或者在节点正在进入维护模式的状态下强制关闭节点，将导致该节点上的虚拟机被强制关机。如果虚拟机开启了 **HA**，将优先触发 HA。如果虚拟机启用了**随主机开机**，节点开机时，节点上的虚拟机将自动开机。
- 若集群开启静态数据加密，节点关机后，缓存的密钥会丢失，在启动后会重新缓存。

**操作步骤**

1. 登录 CloudTower，在集群的主机列表中选中目标节点，单击右侧的 **...** 后选择**关机**或**关闭 SCVM**。
2. 在弹出的对话框中输入原因，然后单击**关机**或**关闭 SCVM**。

**后续操作**

如需关闭或重启 ESXi 主机，请在关闭 SCVM 之后，根据 CloudTower 弹出的**关闭 SCVM** 对话框中的提示及 VMware 技术文档，在 VMware 提供的界面内关闭或重启 ESXi 主机。

---

## 节点运维 > 重启节点

# 重启节点

您可以在 CloudTower 上便捷地重启 SMTX OS 集群的主机和 SCVM，在 CloudTower 重启 SCVM 不会对 ESXi 主机的电源状态造成影响。

修改配置时，例如修改网口 SR-IOV、主机 IOMMU 等系统配置，请使节点进入维护模式后使用此功能重启节点使配置生效。如遇需要紧急关闭或重启节点的情况，可以在非维护模式下强制关闭或重启。

同一集群内，同一时间仅允许进行一个重启节点的任务。

**前提条件**

- 当前节点处于`健康`、`初始化`或`异常`状态。
- 当前节点重启后，所在集群中的剩余节点满足选举主节点的数量要求。
- 所在集群未使用当前节点的管理 IP 来关联 CloudTower。
- 当前节点处于维护模式。

  若节点未处于维护模式时强制重启，请确保满足以下条件：

  - CloudTower 虚拟机不能位于当前主机之上（若 CloudTower 已启用高可用，则 CloudTower 高可用节点不能位于当前主机之上）。
  - 如集群中存在冗余策略使用纠删码的虚拟卷或 NFS Export，除当前节点外，所在集群中包含健康且非移除中的存储服务的节点数量不少于任一虚拟卷或 NFS Export 纠删码配置的数据块数量（K）。
  - 集群中其他节点中空闲存储空间充足，即满足如下两个条件：
    - 集群剩余节点可用存储容量 > 该节点已使用存储容量
    - 集群剩余节点可用写缓存容量 > 该节点已使用写缓存容量
  - 当前节点中不存在只有 1 个副本的数据。

**注意事项**

- 未设置节点进入维护模式或者在节点正在进入维护模式的状态下强制重启节点，将导致该节点上的虚拟机被强制关机。如果虚拟机开启了 **HA**，将优先触发 HA。如果虚拟机启用了**随主机开机**，节点开机时，节点上的虚拟机将自动开机。
- 若集群开启静态数据加密，节点重启后，缓存的密钥会丢失，在启动后会重新缓存。

**操作步骤**

1. 登录 CloudTower，在集群的主机列表中选中目标节点，单击右侧的 **...** 后选择**重启**或**重启 SCVM**。
2. 在弹出的对话框中输入原因，然后单击**重启**或**重启 SCVM**。

---

## 节点运维 > 添加节点

# 添加节点

当 SMTX OS 集群计算或存储资源不足时，可以通过在线添加新节点的方式实现集群的扩容。

**适用场景**

本章节描述的操作仅适用于为未启用双活特性的 SMTX OS 集群添加新节点的场景，为双活集群的优先可用域或次级可用域添加新节点不可参考本小节进行操作。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）集群添加新节点

# 为 SMTX OS（ELF）集群添加新节点

您可以参考本小节内容为 SMTX OS（ELF）集群扩容，建议您在添加新节点前，认真了解[准备工作](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_34)，确保扩容的顺利进行。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）集群添加新节点 > 准备工作

# 准备工作

- 在集群扩容前，请提前向 SmartX 申请 SMTX OS 软件 License。
- 检查集群是否安装第三方插件，如果安装了第三方插件，请在扩容前卸载。
- 参考《SMTX OS 集群安装部署指南（ELF 平台）》的[硬件要求](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_09)章节，确认待添加节点的硬件配置满足要求。
- 确认当前集群的服务器 CPU 架构和所安装的 SMTX OS 软件版本，为待添加的节点提前准备好该版本的 SMTX OS 安装映像文件。
- 为待添加的节点规划两个 IP：SMTX OS 管理 IP、SMTX OS 存储 IP，分别用于管理网络和存储网络，同时记录两个网络的子网掩码、网关等信息。若现有的 SMTX OS 集成硬件管理能力，还需为该节点规划 IPMI 管理台 IP。

  新节点的 IP 地址规划遵循以下规则：

  - 新添加节点与现有 SMTX OS（ELF）集群的节点的存储网络属于同一子网。
  - 新添加节点的 SMTX OS 管理 IP 和存储 IP 不能分配在同一网段。
  - 新添加节点与现有集群节点的 SMTX OS 管理 IP 需要分配在同一网段。
  - 新添加节点与现有集群节点的 SMTX OS 存储 IP 之间可正常连通。
  - IP 地址不能与以下 CIDR 范围内的任何 IP 地址重叠：

    - 169.254.0.0/16
    - 240.0.0.0/4
    - 224.0.0.0/4
    - 198.18.0.0/15
    - 127.0.0.0/8
    - 0.0.0.0/8
  - 若新添加节点曾属于其他集群，请勿复用其在原集群中使用的 SMTX OS 管理 IP 和存储 IP。
  > **说明：**
  >
  > 现有 SMTX OS（ELF）集群节点的 IP 地址配置可以通过登录 CloudTower，在左侧导航栏中选中集群的某个主机后，在右侧弹出的主机概览界面中进行查看。
- 如果待扩容集群启用了 Boost 模式，RDMA 功能或常驻缓存模式，请确认待添加的节点的软硬件配置满足《SMTX OS 特性说明》中启用对应功能的配置要求。
- SMTX OS 集群支持小容量规格、标准容量规格和大容量规格。如果待扩容集群的节点是大容量规格，请确认待添加的节点也是大容量规格；如果待扩容集群内存在小容量规格或标准容量规格的节点，请确认待添加的节点是标准容量规格。
- 如果 SMTX OS 集群为全闪配置且存储介质类型相同，请确认待添加的节点也为全闪配置且存储介质类型与当前集群相同。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）集群添加新节点 > 为待添加节点安装 SMTX OS 软件

# 为待添加节点安装 SMTX OS 软件

参考《SMTX OS 集群安装部署指南（ELF 平台）》文档中的[在物理服务器上安装 SMTX OS](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_22) 章节，在待添加节点上安装 SMTX OS 软件。

> **注意**:
>
> 若待添加节点之前已安装 SMTX OS 软件，为避免因有旧集群残留信息或软件版本错误等问题导致扩容失败，请重新安装 SMTX OS 软件。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）集群添加新节点 > 为 RDMA 功能配置流量控制

# 为 RDMA 功能配置流量控制

若待扩容集群启用了 RDMA 功能，请参考《SMTX OS 集群安装部署指南（ELF 平台）》的[在交换机端配置流量控制](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_47#%E5%9C%A8%E4%BA%A4%E6%8D%A2%E6%9C%BA%E7%AB%AF%E9%85%8D%E7%BD%AE%E6%B5%81%E9%87%8F%E6%8E%A7%E5%88%B6%E4%BB%A5-mellanox-switch-%E4%B8%BA%E4%BE%8B)和[在主机端配置流量控制](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_47#%E5%9C%A8%E4%B8%BB%E6%9C%BA%E7%AB%AF%E9%85%8D%E7%BD%AE%E6%B5%81%E9%87%8F%E6%8E%A7%E5%88%B6)小节配置流量控制；否则请忽略。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）集群添加新节点 > 检查并配置网络环境

# 检查并配置网络环境

登录待添加节点的 SMTX OS 系统，参考《SMTX OS 集群安装部署指南（ELF 平台）》文档中的[检查并配置网络环境](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_26)章节，针对待添加节点设置网络环境。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）集群添加新节点 > 为集群添加主机

# 为集群添加主机

**注意事项**

为待扩容集群添加主机时，仅需要对待添加节点进行以下操作。集群级别的设置可自动从待扩容集群获取，无需重复设置。

**操作步骤**

1. 登录 CloudTower，在左侧导航栏中选中待扩容的集群，进入**概览**界面。在界面右上方选择 **+ 创建** > **添加主机**，进入**添加主机**对话框。用户可以选择手动发现主机，或者通过自动扫描来发现主机。

   - **手动发现主机**

     在**主机地址**输入框中输入待添加主机的 IP 或 MAC 地址，单击**添加**可添加多个主机地址，单击**发现主机**按钮进行主机发现。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_002.png)
   - **自动扫描主机**

     用户也可以单击**自动扫描**来发现主机，扫描完成后若发现当前网络中存在未添加的主机，界面将显示待添加主机的主机名、IP 地址或 MAC 地址。鼠标悬浮在右侧图标上时，将会显示对应的物理盘和网口信息。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_003.png)

   扫描结束后，若系统在当前网络中尚未发现待添加的主机,则系统将会给出提示,请尝试**重新扫描**或**手动发现**主机进行重新搜索发现。
2. 勾选待添加的主机，单击**下一步**。
3. 在**配置主机**界面，输入待添加节点的主机名称。
4. 为虚拟分布式交换机关联物理网口。

   - 如果虚拟分布式交换机仅关联一种网络，如下图，请给待添加节点选择用于该网络的物理网口。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_050.png)

     - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网口。当接入该网络的物理交换机启用了 LACP 动态链路聚合时，需要选择多个网口进行网口绑定。
     - 如果关联的网络为存储网络，当待扩容集群启用 RDMA 功能时，需确认所选的网口均来自支持 RDMA 功能的网卡。
   - 如果虚拟分布式交换机关联了多种网络，如下图，请给待添加节点选择这些网络共用的物理网口。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_049.png)

     可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网口。当接入这些网络的物理交换机启用了 LACP 动态链路聚合时，需要选择两个网口进行网口绑定。

   当待扩容集群创建了镜像出口网络时，还需要为该网络所属的虚拟分布式交换机关联物理网口。

   > **注意**
   >
   > 新增网口的 MTU 需大于等于此虚拟分布式交换机上关联的所有虚拟网络（包括系统网络及虚拟机网络）MTU 的最大值。若新增的网口不满足上述要求，则需勾选**同时调高关联网口 MTU 至此值**，勾选后系统将自动对相关物理网口进行调整。
5. 填写为待添加节点实际规划的管理 IP 和存储 IP。

   ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_052.png)
6. 可选：填写 IPMI IP 信息，及其用户名和密码。

   当待扩容集群创建了镜像出口网络时，还需要为待添加节点配置隧道源 IP。
7. （可选）为待添加节点配置物理盘池。当待添加节点满足多物理盘池的配置要求时，系统会根据节点的存储配置自动选择推荐的物理盘池数量，并分配物理盘及用途，您也可以手动修改物理盘池数量，建议不同节点设置相同的的物理盘池数量。

   > **注意**：
   >
   > - 单集群最多支持配置 255 个物理盘池。
   > - 存储分层模式下：
   >   - 混闪配置、多种类型 SSD 全闪配置，或单一类型多种属性 SSD 全闪配置，单物理盘池的物理盘数量上限为 64；
   >   - 单一类型且单一属性 SSD 全闪配置，单物理盘池的物理盘数量上限为 32。
   > - 存储不分层模式下：单物理盘池的物理盘数量上限为 32。
   > - 单物理盘池的数据盘总容量上限为 256 TB，缓存盘总容量上限为 51 TB，超过容量上限后，将无法添加主机。
8. 指定物理盘的用途和所属物理盘池。

   - **SMTX 系统盘**：不属于任何物理盘池，不可修改用途。
   - **含有元数据分区的缓存盘**和**含有元数据分区的数据盘**：不可修改用途，可移至其他物理盘池。
   - 其余物理盘：

     存储分层模式部署时：

     - 若待添加节点为混闪配置，一般只有当系统判断的物理盘类型有误时，才需要手动修改用途，可移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为多种类型 SSD 全闪配置，当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**用途修改为**缓存盘**；其余情况下，只有当系统判断的物理盘类型有误时，才需要手动修改物理盘用途。可将物理盘移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为单一类型且多种属性的 SSD 全闪配置，物理盘默认为**数据盘**，需手动将高性能 SSD 的用途修改为**缓存盘**；当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**的用途修改为**缓存盘**。可将物理盘移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为单一类型且单一属性的 SSD 全闪配置，物理盘默认为**数据盘**，无需修改用途，可移至其他物理盘池或选择**不挂载**。

     存储不分层模式部署时：所有物理盘默认为数据盘，不可修改用途，可移至其他物理盘池或选择不挂载。
9. 为待添加节点统一设置 root 账户和 smartx 账户的密码。
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
11. 在 CloudTower 中确认节点添加成功，且集群运行正常。

    - 主机列表中将新增显示该主机的详细信息，该主机为健康状态。
    - 在集群概览界面中存储容量、主机数量、物理盘个数、CPU 总核数和内存容量均有增加。
    - 在集群概览界面中报警模块未新增严重警告和注意信息。
12. 可选：若集群当前的总节点数大于或等于 5，但主节点数小于 5，请将集群中的部分存储节点转换为主节点，直至主节点数为 5。可参考[转换节点角色](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_55)章节进行转换。

    > **注意**：
    >
    > 每次只能对集群中的某一个节点执行角色转换操作，不支持多个节点同时进行转换。
13. 可选：若集群关联了虚拟专有云网络，需要为新主机添加 TEP IP。可参考《Everoute 虚拟专有云网络管理指南》**管理关联集群**章节中的**编辑关联集群**小节进行添加。
14. 可选：若集群配置了单独的业务虚拟机网络，请将新主机关联至该网络所属的虚拟分布式交换机，以保证业务的正常运行，具体请参考《SMTX OS 管理指南》**管理网络**章节中的[编辑或删除虚拟分布式交换机](/smtxos/6.3.0/os_administration_guide/os_administration_guide_108#%E7%BC%96%E8%BE%91%E8%99%9A%E6%8B%9F%E5%88%86%E5%B8%83%E5%BC%8F%E4%BA%A4%E6%8D%A2%E6%9C%BA)小节。

**后续操作**

- 在为基于 TencentOS 操作系统的 SMTX OS 集群添加完节点后，需要激活新添加主机的操作系统，请联系 SmartX 售后工程师进行激活。
- 若集群已启用深度安全防护功能，在添加完节点后，需要在新添加主机上部署 SVM，并在 Everoute 的网络导流功能中关联对应的导流网卡，具体步骤请参考《SMTX OS 特性说明》的[深度安全防护功能](/smtxos/6.3.0/os_property_notes/os_property_notes_112)章节

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）集群添加新节点 > 验证流量控制的配置结果

# 验证流量控制的配置结果

当集群启用了 RDMA 功能时，请参考《SMTX OS 集群安装部署指南（ELF 平台）》的[验证流量控制的配置结果](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_47#%E9%AA%8C%E8%AF%81%E6%B5%81%E9%87%8F%E6%8E%A7%E5%88%B6%E7%9A%84%E9%85%8D%E7%BD%AE%E7%BB%93%E6%9E%9C)小节验证新节点的流控配置是否正确。

> **注意**：
>
> 由于验证流量控制的配置结果需要至少 3 个节点，因此需根据本次扩容新增的节点数量确认需要参与测试的节点。
>
> - 若新增节点在 3 个及以上，则仅需对新增节点进行测试。
> - 若新增节点不足 3 个，则需要从集群借用原有的节点与新增节点组成 3 个节点进行测试。为避免影响集群原有节点的业务性能和测试结果的准确性，建议在集群业务空闲期进行验证。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）集群添加新节点

# 为 SMTX OS（VMware ESXi）集群添加新节点

您可以参考本小节内容为 SMTX OS (VMware ESXi) 集群扩容，建议您在添加新节点前，认真了解[准备工作](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_40)，确保扩容的顺利进行。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）集群添加新节点 > 准备工作

# 准备工作

- 在集群扩容前，请提前向 SmartX 申请 SMTX OS 软件 License 和更新许可码。
- 参考《 SMTX OS 集群安装部署指南（VMware ESXi 平台）》的[硬件要求](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_10)章节，确认待添加节点的硬件配置满足要求。
- 确认当前集群的服务器 CPU 架构和所安装的 SMTX OS 软件版本，为待添加的节点提前准备该版本的 SMTX OS 安装映像文件。
- 确认和下载与集群主机所使用的版本相同的 VMware ESXi 安装文件和 SMTX VAAI-NAS 插件安装文件。
- 确认待添加的 ESXi 主机的 SSH 端口号为 22。
- 为待添加的节点规划 4 个 IP：SCVM 管理 IP、SCVM 存储 IP、ESXi 管理 IP 和 ESXi 存储 IP，分别用于管理网络和存储网络，同时记录两个网络的子网掩码、网关等信息。若现有的 SMTX OS 集成硬件管理能力，还需为该节点规划 IPMI 管理台 IP。

  新节点的 IP 地址规划遵循以下规则：

  - 新添加节点与现有 SMTX OS (VMware ESXi) 集群的节点的存储网络属于同一子网。
  - 新添加节点的 SCVM 管理 IP 和存储 IP 不能分配在同一网段。
  - 新添加节点与现有集群节点的 SCVM 管理 IP 需要分配在同一网段。
  - 新添加节点与现有集群节点的 SCVM 存储 IP 之间可正常连通。
  - 新添加节点的 SCVM 存储 IP 和 ESXi 存储 IP 之间，以及 SCVM 管理 IP 和 ESXi 管理 IP 之间可正常连通。
  - IP 地址不能与以下 CIDR 范围内的任何 IP 地址重叠：

    - 169.254.0.0/16
    - 240.0.0.0/4
    - 224.0.0.0/4
    - 198.18.0.0/15
    - 127.0.0.0/8
    - 0.0.0.0/8
  - 若新添加节点曾属于其他集群，请勿复用其在原集群中使用的 SCVM 管理 IP 和存储 IP。
  > **说明：**
  >
  > 现有 SMTX OS (VMware ESXi) 集群节点的 IP 地址配置可以通过登录 CloudTower，在左侧导航栏中选中集群的某个主机后，在右侧弹出的主机概览界面中进行查看。
- 如果待扩容集群启用了 RDMA 功能或常驻缓存模式，请确认待添加的节点的软硬件配置满足《SMTX OS 特性说明》中启用对应功能的配置要求。
- 如果待扩容集群启用了 NVMe 直通硬盘热插拔功能，请参考《安装部署指南（VMware ESXi 平台）》中[启用 NVMe 直通硬盘热插拔功能的要求](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_98)，确认待添加的节点满足启用该功能的要求，并且已在本地主机中准备 vmpctl 文件。
- SMTX OS 集群支持小容量规格、标准容量规格和大容量规格。如果待扩容集群的节点是大容量规格，请确认待添加的节点也是大容量规格；如果待扩容集群内存在小容量规格或标准容量规格的节点，请确认待添加的节点是标准容量规格。
- 如果 SMTX OS 集群为全闪配置且存储介质类型相同，请确认待添加的节点也为全闪配置且存储介质类型与当前集群相同。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）集群添加新节点 > 为待添加节点安装 ESXi 软件和 SMTX OS 软件

# 为待添加节点安装 ESXi 软件和 SMTX OS 软件

**注意事项**

若待添加节点之前已安装 ESXi 软件或 SMTX OS 软件，为避免因有旧集群残留信息或软件版本错误等问题导致扩容失败，请重新安装 ESXi 软件和 SMTX OS 软件。

**操作步骤**

请参考《 SMTX OS 集群安装部署指南（VMware ESXi 平台）》，完成以下操作步骤：

1. 参考[在每个节点上安装 ESXi 软件](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_23)章节，在待添加的主机上安装 VMware ESXi 软件。
2. 参考[设置 ESXi](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_26)，设置待添加的 ESXi 主机。
3. 参考[使用 vCenter Server 纳管 ESXi 主机](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_39)章节，将待添加的 ESXi 主机添加至 vCenter Server 中进行纳管。
4. 参考[配置存储网络](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_42)和[配置 NFS 网络](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_47)章节，为待添加的 ESXi 主机配置存储网络和 NFS 网络。
5. 参考[在 ESXi 节点上创建 SCVM 虚拟机](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_50)章节，在待添加的 ESXi 主机上创建虚拟机 SCVM，用于安装 SMTX OS。
6. 参考[在 SCVM 虚拟机中安装 SMTX OS 软件](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_55)章节，在待添加的 ESXi 主机的 SCVM 中安装 SMTX OS 软件。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）集群添加新节点 > 检查并设置扩容的环境

# 检查并设置扩容的环境

登录待添加节点的 SMTX OS 系统，参考 《SMTX OS 集群安装部署指南（VMware ESXi 平台）》文档中的[检查并设置部署的环境](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_56)章节，针对待添加节点设置扩容环境，同时记录该节点用于管理网络和存储网络的网口信息。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）集群添加新节点 > 为集群添加主机

# 为集群添加主机

**注意事项**

为待扩容集群添加主机时，仅需要对待添加节点进行以下操作。集群级别的设置可自动从待扩容集群获取，无需重复设置。

**操作步骤**

1. 登录 CloudTower，在左侧导航栏中选中待扩容的集群，进入**概览**界面。在界面右上方选择 **+ 创建** > **添加主机**，进入**添加主机**对话框。用户可以选择手动发现主机，或者通过自动扫描来发现主机。

   - **手动发现主机**

     在**主机地址**输入框中输入待添加主机的 IP 或 MAC 地址，单击**添加**可添加多个主机地址，单击**发现主机**按钮进行主机发现。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_002.png)
   - **自动扫描主机**

     用户也可以单击**自动扫描**来发现主机，扫描完成后若发现当前网络中存在未添加的主机，界面将显示待添加主机的主机名、IP 地址或 MAC 地址。鼠标悬浮在右侧图标上时，将会显示对应的物理盘和网口信息。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_003.png)

   扫描结束后，若系统在当前网络中尚未发现待添加的主机,则系统将会给出提示,请尝试**重新扫描**或**手动发现**主机进行重新搜索发现。
2. 勾选待添加的 ESXi 主机，单击**下一步**。
3. 在**配置主机**界面，输入待添加节点的主机名称。
4. 根据在[检查并设置扩容的环境](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_42)时记录的用于管理网络和存储网络的网口信息，为待添加的节点选择管理网口和存储网口，并填写 SCVM 管理 IP 和 SCVM 存储 IP。

   ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_051.png)

   当待扩容集群启用 RDMA 功能时，还需要选择用于 ZBS 网络的网口作为 VMware 接入网口，并填写为待添加的节点实际规划的 VMware 接入 IP。
5. 填写待添加的节点的 ESXi 管理 IP、用户名和密码。
6. （可选）填写待添加的节点的 IPMI IP，用户名和密码。
7. 指定物理盘的用途。请参考以下说明按需修改**含有元数据分区的缓存盘**和**含有元数据分区的数据盘**以外的物理盘的用途。

   - 存储分层模式部署时：

     - 若待添加节点为混闪配置，一般只有当系统判断的物理盘类型有误时，才需要手动修改用途。
     - 若待添加节点为多种类型 SSD 全闪配置，当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**用途修改为**缓存盘**；其余情况下，只有当系统判断的物理盘类型有误时，才需要手动修改用途。
     - 若待添加节点为单一类型且多种属性的 SSD 全闪配置，物理盘默认为**数据盘**，需手动将高性能 SSD 的用途修改为**缓存盘**；当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**的用途修改为**缓存盘**。
     - 若待添加节点为单一类型且单一属性的 SSD 全闪配置，物理盘默认为**数据盘**，无需修改用途。
   - 存储不分层模式部署时：所有物理盘默认为**数据盘**，不可修改用途，但可选择**不挂载**。
8. 为待添加的 SCVM 统一设置 root 账户和 smartx 账户的密码，该设置不影响 ESXi 主机的账号密码。
9. 单击**执行部署**，部署主机。

   开始执行部署后，当前界面将展示部署的总体进度。如果关闭当前窗口，您也可以在任务中心查看部署进度，在对应的任务条目右侧单击 **...** > **查看详情**可以返回**执行部署**界面。

   - 如果部署成功，**执行部署**界面将提示已成功添加主机。

     - 若集群的 SSH 端口号不是 22，界面将提示集群内各主机的 SSH 服务端口号不一致，您需要单击**编辑 ssh 端口号**，重新编辑端口号并保存，以统一集群中所有主机的 SSH 端口号。
     - 若集群已启用端口访问控制，界面将提示新主机的所有端口允许全部 IP 访问，即新主机不会自动应用端口访问控制中的任何访问限制规则。如需为新主机配置 snmp 服务和 ssh 服务的访问限制，请单击**设置访问控制**，编辑存储网段并保存，然后为新主机的 snmp 服务和 ssh 服务端口设置 IP 白名单，详细操作指导可参考[更新端口访问控制](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_130)章节。
   - 如果部署失败，**执行部署**界面将提示部署失败，需根据界面的具体提示进行下一步操作。

     - 如果界面提示集群无法连接新主机，表明是由于网络配置失败导致部署失败，请参考以下步骤重新添加主机。

       ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_055.png)

       1. 通过 IPMI 管理台 IP 访问待添加主机，调整主机的网络配置。
       2. 在待添加 ESXi 节点的 SCVM 中，执行如下命令清理主机信息并重启部署服务。

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
10. 若集群当前的总节点数大于或等于 5，但主节点数小于 5，请将集群中的部分存储节点转换为主节点，直至主节点数为 5。可参考[转换节点角色](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_55)章节进行转换。

    > **注意**：
    >
    > 每次只能对集群中的某一个节点执行角色转换操作，不支持多个节点同时进行转换。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）集群添加新节点 > 设置 SMTX OS 的高可用性

# 设置 SMTX OS 的高可用性

添加完主机后，为保证 SMTX OS 的高可用性，请参考《SMTX OS 集群安装部署指南（VMware ESXi 平台）》为新添加的 ESXi 节点继续完成部分参数设置，并在新添加的 SCVM 中部署 IO 重路由脚本，操作步骤如下。

1. 参考[设置 SCVM 在 ESXi 开机时自动启动](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_79)，设置新添加的 SCVM 与 ESXi 主机一起自动启动和关机。
2. 参考[开启 ESXi 主机防火墙的 SSH 服务](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_82)，开启新添加的 ESXi 主机防火墙的 SSH 服务。
3. 参考以下步骤，部署 IO 重路由脚本和 SCVM 自动重启脚本。

   1. 在浏览器中输入新添加的 ESXi 主机的管理 IP，并使用 **root** 账号登录。
   2. 在左侧导航栏中选中 SCVM，打开控制台，执行命令 `zbs-node collect_node_info`。
   3. 可选：若集群已开启 RDMA 特性，则在 SCVM 中继续执行命令 `zbs-deploy-manage deploy-rdma`，否则请忽略此步骤。
   4. 在 SCVM 中执行命令 `zbs-deploy-manage deploy-hypervisor`。

      执行成功后，界面将显示 `Finish deploy hypervisor` 的提示信息，并且 1 分钟后您可以在 SCVM 对应的 ESXi 主机命令行界面上观察到 reroute 进程正在运行。
4. 参考[检查部署结果](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_88)，在 CloudTower 上检查 IO 重路由脚本的部署结果，在新添加的 ESXi 节点上检查 SCVM 自动重启脚本的部署结果。

   > **注意**：
   >
   > - 如果 IO 重路由脚本部署失败，请先根据相关日志定位出失败原因并解决问题，然后在新添加的 SCVM 中执行 `zbs-deploy-manage clear-hypervisor`，最后再重新执行以上部署流程。
   > - 如果 SCVM 自动重启脚本部署失败，请先根据相关日志定位出失败原因并解决问题，然后在新添加的 SCVM 中执行 `zbs-deploy-manage update-scvm-autostart` 命令部署脚本，完成后重新执行检查，确保脚本部署成功。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）集群添加新节点 > 为新节点挂载 NFS 数据存储

# 为新节点挂载 NFS 数据存储

完成 SMTX OS 的高可用性设置后，请为新添加的 ESXi 节点挂载 NFS 数据存储。

- 如果需要创建新的 NFS 数据存储进行挂载，请参考《SMTX OS 安装部署指南》的[创建 NFS Export 并挂载至 ESXi 主机](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_77)章节进行操作。
- 如果需要挂载集群中已有的 NFS 数据存储，请参考以下步骤进行操作。

  1. 在 vCenter Server 中选中集群，在右侧管理界面中单击**数据存储**。
  2. 右键单击需要挂载的 NFS 数据存储，选择**将数据存储挂载至其他主机**。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_058.png)
  3. 在弹出的**将数据存储挂载至其他主机**对话框中，选择需要挂载该存储的新 ESXi 主机，单击**确定**。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_059.png)

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）集群添加新节点 > 关联新节点与 SMTX OS 集群

# 关联新节点与 SMTX OS 集群

1. 在 CloudTower 管理平台中确认节点添加成功。

   - 主机列表中将新增显示该主机的详细信息，该主机为健康状态。
   - 集群概览界面中的存储容量、主机数量、物理盘个数均有增加。
   - 集群概览界面的报警模块新增一条严重警告，提示新加入的 ESXi 主机未与 SMTX OS 集群完成关联。
2. 在 CloudTower 的集群管理界面中单击**设置**按钮，选择 **ESXi**，并输入主机的 ESXi 管理 IP、用户名和密码，将 ESXi 主机与 SMTX OS 集群完成关联。

   关联成功并在大约几分钟以后，集群概览界面中对应的严重警告消失，同时 CPU 总核数和内存容量均有增加。
3. 如果集群已启用机架感知功能，请在 CloudTower 的集群管理界面中单击**全部** > **机架配置**，然后为新 ESXi 主机设置所属机箱和机架。否则请忽略。

---

## 节点运维 > 添加节点 > 未启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）集群添加新节点 > 验证流量控制的配置结果

# 验证流量控制的配置结果

当集群启用了 RDMA 功能时，请参考《SMTX OS 集群安装部署指南（VMware ESXi 平台）》的[验证流量控制的配置结果](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_38)小节验证新节点的流控配置是否正确。

> **注意**：
>
> 由于验证流量控制的配置结果需要至少 3 个节点，因此需根据本次扩容新增的节点数量确认需要参与测试的节点。
>
> - 若新增节点在 3 个及以上，则仅需对新增节点进行测试。
> - 若新增节点不足 3 个，则需要从集群借用原有的节点与新增节点组成 3 个节点进行测试。为避免影响集群原有节点的业务性能和测试结果的准确性，建议在集群业务空闲期进行验证。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）双活集群添加新节点

# 为 SMTX OS（ELF）双活集群添加新节点

您可以参考本小节内容为 SMTX OS（ELF）双活集群扩容，建议您在添加新节点前，认真了解[准备工作](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_132)，确保扩容的顺利进行。

> **说明**：
>
> 仅支持添加存储节点，若需要添加主节点，请在完成节点添加后参考[转换节点角色](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_55)将添加的存储节点转化为主节点。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）双活集群添加新节点 > 准备工作

# 准备工作

在为 SMTX OS（ELF）双活集群添加节点之前，请按照如下要求提前完成准备工作。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）双活集群添加新节点 > 准备工作 > 硬件配置准备

# 硬件配置准备

- 现有 SMTX OS（ELF）双活集群已完成硬件拓扑配置，即所有主机均已分配机箱和机架。

  若当前集群还未配置硬件拓扑，请参考《SMTX OS 管理指南》中的[配置机架拓扑](/smtxos/6.3.0/os_administration_guide/os_administration_guide_167)章节为主机添加机箱和机架。
- 待添加节点的硬件配置满足《SMTX OS 双活集群安装部署指南（ELF 平台）》中的[硬件要求](/smtxos/6.3.0/elf_multiactive_installation/elf_multiactive_installation_12)。
- 如果待扩容集群启用了 Boost 模式或常驻缓存模式，请确认待添加的节点的软硬件配置满足《SMTX OS 特性说明》中启用对应功能的配置要求。
- SMTX OS（ELF）双活集群支持小容量规格、标准容量规格和大容量规格。如果待扩容集群的节点是大容量规格，请确认待添加的节点也是大容量规格；如果待扩容集群内存在小容量规格或标准容量规格的节点，请确认待添加的节点是标准容量规格。。
- 如果当前集群为全闪配置且存储介质类型相同，请确认待添加的节点也为全闪配置，并且存储介质类型与当前集群相同。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）双活集群添加新节点 > 准备工作 > 软件配置准备

# 软件配置准备

- 提前下载当前集群的主机所安装的 ISO 映像文件，要求 ISO 映像文件的版本、CPU 架构和底层操作系统（CentOS 或 openEuler）与当前集群完全相同。
- 请提前向 SmartX 申请 SMTX OS 软件 License，License 版本必须为敏捷版、标准版或企业版。双活集群需要单独购买双活的许可，请确认软件许可满足要求。
- 检查集群是否安装第三方插件，如果安装了第三方插件，请在扩容前卸载。
- 确认待添加的 ESXi 主机的 SSH 端口号为 22。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）双活集群添加新节点 > 准备工作 > 为新节点规划 IP

# 为新节点规划 IP

为待添加的节点规划两个 IP：SMTX OS 管理 IP、SMTX OS 存储 IP，分别用于管理网络和存储网络，同时记录两个网络的子网掩码、网关等信息。若现有的 SMTX OS 集成硬件管理能力，还需为该节点规划 IPMI 管理台 IP。

优先/次级可用域的节点 IP 地址规划如下表所示。

| 节点名称 | 网络类型 | IP 地址 | 子网掩码 | 网关 | VLAN ID（可选） |
| --- | --- | --- | --- | --- | --- |
| 优先可用域节点 | 管理网络 | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| 存储网络 | xx.xx.xx.xx | xx.xx.xx.xx | - | xx |
| 次级可用域节点 | 管理网络 | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| 存储网络 | xx.xx.xx.xx | xx.xx.xx.xx | - | xx |

网络管理员在分配新节点的管理 IP、存储 IP、迁移 IP 和接入 IP 时，必须遵循以下规则：

- 相同类型系统网络中，新添加节点 IP 与现有集群节点 IP 必须分配在同一网段且可以正常通信。
- 不同类型系统网络中，新添加节点 IP 不得分配在同一网段。
- 上述 IP 地址不能与以下 CIDR 范围内的任何 IP 地址重叠：
  - 169.254.0.0/16
  - 240.0.0.0/4
  - 224.0.0.0/4
  - 198.18.0.0/15
  - 127.0.0.0/8
  - 0.0.0.0/8

- 若新添加节点曾属于其他集群，请勿复用其在原集群中使用的 SMTX OS 管理 IP 和存储 IP。

规划完以上 IP 后，需要将新添加节点的 IP 与服务器序列号（即服务标签）一一对应。

> **说明：**
>
> 现有 SMTX OS（ELF）双活集群节点的 IP 地址配置可以通过登录 CloudTower，在左侧导航栏中选中集群的某个主机后，在右侧弹出的主机概览界面中进行查看。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）双活集群添加新节点 > 为待添加节点安装 SMTX OS 软件

# 为待添加节点安装 SMTX OS 软件

请参考《SMTX OS 双活集群安装部署指南（ELF 平台）》文档中的以下章节，依次检查 BIOS 设置、挂载 SMTX OS 映像文件和安装 SMTX OS 映像文件。

- [检查 BIOS 设置](/smtxos/6.3.0/elf_multiactive_installation/elf_installation_guide/elf_installation_guide_23)
- [挂载 SMTX OS 映像文件](/smtxos/6.3.0/elf_multiactive_installation/elf_installation_guide/elf_installation_guide_24)
- [在优先/次级可用域的节点上安装映像文件](/smtxos/6.3.0/elf_multiactive_installation/elf_multiactive_installation_29)

> **注意**:
>
> 若待添加节点之前已安装 SMTX OS 软件，为避免因有旧集群残留信息或软件版本错误等问题导致扩容失败，请重新安装 SMTX OS 软件。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）双活集群添加新节点 > 为待添加节点绑定管理网口

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

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）双活集群添加新节点 > 为待添加节点的管理网口配置子接口

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

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）双活集群添加新节点 > 检查并设置扩容的环境

# 检查并设置扩容的环境

登陆待添加节点的 SMTX OS 系统，参考《SMTX OS 双活集群安装部署指南（ELF 平台）》文档中的[为优先/次级可用域节点设置部署的环境](/smtxos/6.3.0/elf_multiactive_installation/elf_multiactive_installation_36)章节，针对待添加节点设置扩容环境。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）双活集群添加新节点 > 为可用域添加节点

# 为可用域添加节点

为双活集群的可用域添加节点时，仅需要对待添加的所有主机进行以下操作。集群级别的设置可自动从原有集群获取，无需重复设置。

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
4. （可选）若集群已配置静态路由，则需为待添加节点指定可用域，可选择优先可用域或次级可用域。
5. 为虚拟分布式交换机关联物理网口。可以根据下图中显示的网口速率、连接状态和 MAC 地址等综合判断，选择关联合适的网口。

   - 如果虚拟分布式交换机仅关联一种网络，即集群采用网络分离部署模式，如下图，请给待添加节点选择用于该网络的物理网口。当接入该网络的物理交换机启用了 LACP 动态链路聚合时，需要选择多个网口进行网口绑定。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_050.png)
   - 如果虚拟分布式交换机关联了多种网络，即集群采用网络融合部署模式，如下图，请为待添加的节点选择这些网络共用的物理网口。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_049.png)

     可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网口。当接入这些网络的物理交换机启用了 LACP 动态链路聚合时，需要选择两个网口进行网口绑定。

   当待扩容集群创建了镜像出口网络时，还需要为该网络所属的虚拟分布式交换机关联物理网口。

   > **注意**
   >
   > 新增网口的 MTU 需大于等于此虚拟分布式交换机上关联的所有虚拟网络（包括系统网络及虚拟机网络） MTU 的最大值。若新增的网口不满足上述要求，则需勾选**同时调高关联网口 MTU 至此值**，勾选后系统将自动对相关物理网口进行调整。
6. 填写待添加节点实际规划的管理 IP 和存储 IP。

   ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_052.png)
7. （可选）填写为待添加节点规划的 IPMI IP 信息，以及用户名和密码。

   当待扩容集群创建了镜像出口网络时，还需要为待添加节点配置隧道源 IP。
8. （可选）为待添加节点配置物理盘池。当待添加节点满足多物理盘池的配置要求时，系统会根据节点的存储配置自动选择推荐的物理盘池数量，并分配物理盘及用途，您也可以手动修改物理盘池数量，建议不同节点设置相同的的物理盘池数量。

   **注意**：

   - 单集群最多支持配置 255 个物理盘池。
   - 存储分层模式下：
     - 混闪配置、多种类型 SSD 全闪配置，或单一类型多种属性 SSD 全闪配置，单物理盘池的物理盘数量上限为 64；
     - 单一类型且单一属性 SSD 全闪配置，单物理盘池的物理盘数量上限为 32。
   - 存储不分层模式下：单物理盘池的物理盘数量上限为 32。
   - 单物理盘池的数据盘总容量上限为 256 TB，缓存盘总容量上限为 51 TB，超过容量上限后，将无法添加主机。
9. 指定物理盘的用途和所属物理盘池。

   - **SMTX 系统盘**：不属于任何物理盘池，不可修改用途。
   - **含有元数据分区的缓存盘和含有元数据分区的数据盘**：不可修改用途，可移至其他物理盘池。
   - 其余物理盘：

     存储分层模式部署时：

     - 若待添加节点为混闪配置，一般只有当系统判断的物理盘类型有误时，才需要手动修改用途，可移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为多种类型 SSD 全闪配置，当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**用途修改为**缓存盘**；其余情况下，只有当系统判断的物理盘类型有误时，才需要手动修改物理盘用途。可将物理盘移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为单一类型且多种属性的 SSD 全闪配置，物理盘默认为**数据盘**，需手动将高性能 SSD 的用途修改为**缓存盘**；当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**的用途修改为**缓存盘**。可将物理盘移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为单一类型且单一属性的 SSD 全闪配置，物理盘默认为**数据盘**，无需修改用途，可移至其他物理盘池或选择**不挂载**。

     存储不分层模式部署时：所有物理盘默认为**数据盘**，不可修改用途，可移至其他物理盘池或选择**不挂载**。
10. 为待添加节点统一设置 `root` 账户和 `smartx` 账户的密码。
11. 单击**执行部署**，部署主机。

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
12. 在 CloudTower 中确认集群的所有节点添加成功，以及集群运行正常。

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

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）双活集群添加新节点 > 扩容后配置

# 扩容后配置

完成双活集群扩容后，必须为新添加节点配置机架拓扑来确保数据副本跨可用域分布。同时，当您在新添加节点中正式创建虚拟机并运行业务时，若您期望虚拟机在适当的主机上运行，则需要为虚拟机设置放置组规则，或将虚拟机加入已有的虚拟机放置组，以保障业务的连续性。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）双活集群添加新节点 > 扩容后配置 > 配置机架拓扑

# 配置机架拓扑

双活集群扩容后，需要在机架拓扑中将新添加节点放置到正确位置，以使系统可以根据拓扑来调整数据的分配情况。请参考《SMTX OS 管理指南》的[在机箱中添加主机](/smtxos/6.3.0/os_administration_guide/os_administration_guide_167#%E5%9C%A8%E6%9C%BA%E7%AE%B1%E4%B8%AD%E6%B7%BB%E5%8A%A0%E4%B8%BB%E6%9C%BA)小节进行配置。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（ELF）双活集群添加新节点 > 扩容后配置 > 配置虚拟机放置组规则

# 配置虚拟机放置组规则

当您在新添加节点中正式创建虚拟机并运行业务时，建议根据《SMTX OS 双活集群安装部署指南（ELF 平台）》中的[设置虚拟机放置组规则](/smtxos/6.3.0/elf_multiactive_installation/elf_multiactive_installation_53)设置放置组规则。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点

# 为 SMTX OS（VMware ESXi）双活集群添加新节点

您可以参考本小节内容为 SMTX OS（VMware ESXi）双活集群扩容，建议您在添加新节点前，认真了解[准备工作](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_141)，确保扩容的顺利进行。

> **说明**：
>
> 仅支持添加存储节点，若需要添加主节点，请在完成节点添加后参考[转换节点角色](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_55)将添加的存储节点转化为主节点。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点 > 准备工作

# 准备工作

在为 SMTX OS（VMware ESXi）双活集群添加节点之前，请按照如下要求提前完成准备工作。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点 > 准备工作 > 新节点的硬件配置准备

# 新节点的硬件配置准备

- 现有 SMTX OS（VMware ESXi）双活集群已完成硬件拓扑配置，即所有主机均已分配机箱和机架。

  若当前集群还未配置硬件拓扑，请参考《SMTX OS 管理指南》中的[配置机架拓扑](/smtxos/6.3.0/os_administration_guide/os_administration_guide_167)章节为主机添加机箱和机架。
- 待添加节点的硬件配置满足《SMTX OS 双活集群安装部署指南（VMware ESXi 平台）》中的[硬件要求](/smtxos/6.3.0/vmware_multiactive_installation/vmware_multiactive_installation_12)。
- 如果待扩容集群启用了常驻缓存模式，请确认待添加的节点的软硬件配置满足《SMTX OS 特性说明》中启用对应功能的配置要求。
- 如果待扩容集群启用了 NVMe 直通硬盘热插拔功能，请参考《双活集群安装部署指南（VMware ESXi 平台）》中[启用 NVMe 直通硬盘热插拔功能的要求](/smtxos/6.3.0/vmware_multiactive_installation/vmware_multiactive_installation_26)，确认待添加的节点满足启用该功能的要求，并且已在本地主机中准备 vmpctl 文件。
- SMTX OS（VMware ESXi）双活集群支持小容量规格、标准容量规格和大容量规格。如果待扩容集群的节点是大容量规格，请确认待添加的节点也是大容量规格；如果待扩容集群内存在小容量规格或标准容量规格的节点，请确认待添加的节点是标准容量规格。
- 如果当前集群为全闪配置且存储介质类型相同，请确认待添加的节点也为全闪配置，并且存储介质类型与当前集群相同。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点 > 准备工作 > 软件准备

# 软件准备

- 提前下载当前集群的主机所安装的 ISO 映像文件，要求 ISO 映像文件的版本、CPU 架构和底层操作系统（CentOS 或 openEuler）与当前集群完全相同。
- 确认和下载与集群主机所使用的版本相同的 VMware ESXi 安装文件和 SMTX VAAI-NAS 插件安装文件。
- 请提前向 SmartX 申请 SMTX OS 软件 License，License 版本必须为敏捷版、标准版或企业版。双活集群需要单独购买双活的许可，请确认软件许可满足要求。
- 检查集群是否安装第三方插件，如果安装了第三方插件，请在扩容前卸载。
- 确认待添加的 ESXi 主机的 SSH 端口号为 22。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点 > 准备工作 > 为新节点规划 IP

# 为新节点规划 IP

为待添加的节点规划 4 个 IP：SCVM 管理 IP、SCVM 存储 IP、ESXi 管理 IP 和 ESXi 存储 IP，分别用于管理网络和存储网络，同时记录两个网络的子网掩码、网关等信息。若现有的 SMTX OS 集成硬件管理能力，还需为该节点规划 IPMI 管理台 IP。

优先/次级可用域的节点 IP 地址规划如下表所示。

| 网络类型 | IP 类型 | IP 地址 | 子网掩码 | 网关 | VLAN ID （可选） |
| --- | --- | --- | --- | --- | --- |
| 管理网络 | SCVM 管理 IP | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| ESXi 管理 IP | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| 存储网络 | SCVM 存储 IP | xx.xx.xx.xx | xx.xx.xx.xx | - | xx |
| ESXi 存储 IP | xx.xx.xx.xx | xx.xx.xx.xx | - | xx |
| 内部网络 | NFS Server IP | 192.168.33.2 | 255.255.255.0 | - | - |
| NFS VMkernel IP | 192.168.33.1 | 255.255.255.0 | - | - |

新节点的 IP 地址规划遵循以下规则：

- 新添加节点与现有 SMTX OS（VMware ESXi）双活集群的节点的存储网络属于同一子网。
- 新添加节点的 SCVM 管理 IP 和存储 IP 不能分配在同一网段。
- 新添加节点与现有集群节点的 SCVM 管理 IP 需要分配在同一网段。
- 新添加节点与现有集群节点的 SCVM 存储 IP 之间可正常连通。

- 新添加节点的 SCVM 存储 IP 和 ESXi 存储 IP 之间，以及 SCVM 管理 IP 和 ESXi 管理 IP 之间可正常连通。
- IP 地址不能与以下 CIDR 范围内的任何 IP 地址重叠：

  - 169.254.0.0/16
  - 240.0.0.0/4
  - 224.0.0.0/4
  - 198.18.0.0/15
  - 127.0.0.0/8
  - 0.0.0.0/8

- 若新添加节点曾属于其他集群，请勿复用其在原集群中使用的 SMTX OS 管理 IP 和存储 IP。

规划完以上 IP 后，需要将新添加节点的 IP 与服务器序列号（即服务标签）一一对应。

> **说明：**
>
> 现有 SMTX OS（VMware ESXi）双活集群节点的 IP 地址配置可以通过登录 CloudTower，在左侧导航栏中选中集群的某个主机后，在右侧弹出的主机概览界面中进行查看。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点 > 为待添加节点安装 ESXi 软件和 SMTX OS 软件

# 为待添加节点安装 ESXi 软件和 SMTX OS 软件

**注意事项**

若待添加节点之前已安装 ESXi 软件或 SMTX OS 软件，为避免因有旧集群残留信息或软件版本错误等问题导致扩容失败，请重新安装 ESXi 软件和 SMTX OS 软件。

**操作步骤**

请参考《 SMTX OS 双活集群安装部署指南（VMware ESXi 平台）》，完成以下操作步骤：

1. 参考[在每个优先/次级可用域的节点上安装 ESXi 软件](/smtxos/6.3.0/vmware_multiactive_installation/vmware_multiactive_installation_29)章节，在待添加的主机上安装 VMware ESXi 软件。
2. 参考[设置 ESXi](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_26)，设置待添加的 ESXi 主机。
3. 参考[使用 vCenter Server 纳管 ESXi 主机](/smtxos/6.3.0/vmware_multiactive_installation/vmware_multiactive_installation_30)章节，将待添加的 ESXi 主机添加至 vCenter Server 中进行纳管。
4. 参考[配置存储网络](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_42)和[配置 NFS 网络](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_47)章节，为待添加的 ESXi 主机配置存储网络和 NFS 网络。
5. 参考[在 ESXi 节点上创建 SCVM 虚拟机](/smtxos/6.3.0/vmware_multiactive_installation/vmware_multiactive_installation_31)章节，在待添加的 ESXi 主机上创建虚拟机 SCVM，用于安装 SMTX OS。
6. 参考[在 SCVM 虚拟机中安装 SMTX OS 软件](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_55)章节，在待添加的 ESXi 主机的 SCVM 中安装 SMTX OS 软件。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点 > 检查并设置扩容的环境

# 检查并设置扩容的环境

登录待添加节点的 SMTX OS 系统，参考 《SMTX OS 双活集群安装部署指南（VMware ESXi 平台）》文档中的[为优先/次级可用域节点设置部署的环境](/smtxos/6.3.0/vmware_multiactive_installation/vmware_multiactive_installation_37)章节，针对待添加节点设置扩容环境，同时记录该节点用于管理网络和存储网络的网口信息。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点 > 为可用域添加节点

# 为可用域添加节点

**注意事项**

为待扩容集群添加主机时，仅需要对待添加节点进行以下操作。集群级别的设置可自动从待扩容集群获取，无需重复设置。

**操作步骤**

1. 登录 CloudTower，在左侧导航栏中选中待扩容的集群，进入**概览**界面。在界面右上方选择 **+ 创建** > **添加主机**，进入**添加主机**对话框。用户可以选择手动发现主机，或者通过自动扫描来发现主机。

   - **手动发现主机**

     在**主机地址**输入框中输入待添加主机的 IP 或 MAC 地址，单击**添加**可添加多个主机地址，单击**发现主机**按钮进行主机发现。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_002.png)
   - **自动扫描主机**

     用户也可以单击**自动扫描**来发现主机，扫描完成后若发现当前网络中存在未添加的主机，界面将显示待添加主机的主机名、IP 地址或 MAC 地址。鼠标悬浮在右侧图标上时，将会显示对应的物理盘和网口信息。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_003.png)

   扫描结束后，若系统在当前网络中尚未发现待添加的主机,则系统将会给出提示,请尝试**重新扫描**或**手动发现**主机进行重新搜索发现。
2. 勾选待添加的 ESXi 主机，单击**下一步**。
3. 在**配置主机**界面，输入待添加节点的主机名称。
4. （可选）若集群已配置静态路由，则需为待添加节点指定可用域，可选择优先可用域或次级可用域。
5. 根据在[检查并设置扩容的环境](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_152)时记录的用于管理网络和存储网络的网口信息，为待添加的节点选择管理网口和存储网口，并填写 SCVM 管理 IP 和 SCVM 存储 IP。

   ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_051.png)
6. 填写待添加的节点的 ESXi 管理 IP、用户名和密码。
7. （可选）填写待添加的节点的 IPMI IP，用户名和密码。
8. 检查磁盘用途，并根据需要指定物理盘的用途。请参考以下说明按需修改**含有元数据分区的缓存盘**和**含有元数据分区的数据盘**以外的物理盘的用途。

   - 存储分层模式部署时：
     - 若待添加节点为混闪配置，一般只有当系统判断的物理盘类型有误时，才需要手动修改用途。
     - 若待添加节点为多种类型 SSD 全闪配置，当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**用途修改为**缓存盘**；其余情况下，只有当系统判断的物理盘类型有误时，才需要手动修改用途。
     - 若待添加节点为单一类型且多种属性的 SSD 全闪配置，物理盘默认为**数据盘**，需手动将高性能 SSD 的用途修改为**缓存盘**；当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**的用途修改为**缓存盘**。
     - 若待添加节点为单一类型且单一属性的 SSD 全闪配置，物理盘默认为数据盘，无需修改用途。
   - 存储不分层模式部署时：所有物理盘默认为**数据盘**，不可修改用途，但可选择**不挂载**。
9. 为待添加的 SCVM 统一设置 root 账户和 smartx 账户的密码，该设置不影响 ESXi 主机的账号密码。
10. 单击**执行部署**，部署主机。

    开始执行部署后，当前界面将展示部署的总体进度。如果关闭当前窗口，您也可以在任务中心查看部署进度，在对应的任务条目右侧单击 **...** > **查看详情**可以返回**执行部署**界面。

    - 如果部署成功，**执行部署**界面将提示已成功添加主机。

      - 若集群的 SSH 端口号不是 22，界面将提示集群内各主机的 SSH 服务端口号不一致，您需要单击**编辑 ssh 端口号**，重新编辑端口号并保存，以统一集群中所有主机的 SSH 端口号。
      - 若集群已启用端口访问控制，界面将提示新主机的所有端口允许全部 IP 访问，即新主机不会自动应用端口访问控制中的任何访问限制规则。如需为新主机配置 snmp 服务和 ssh 服务的访问限制，请单击**设置访问控制**，编辑存储网段并保存，然后为新主机的 snmp 服务和 ssh 服务端口设置 IP 白名单，详细操作指导可参考[更新端口访问控制](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_130)章节。
    - 如果部署失败，**执行部署**界面将提示部署失败，需根据界面的具体提示进行下一步操作。

      - 如果界面提示集群无法连接新主机，表明是由于网络配置失败导致部署失败，请参考以下步骤重新添加主机。

        ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_055.png)

        1. 通过 IPMI 管理台 IP 访问待添加主机，调整主机的网络配置。
        2. 在待添加 ESXi 节点的 SCVM 中，执行如下命令清理主机信息并重启部署服务。

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
12. （可选）若可用域中的主节点数小于 2，请将可用域中的部分存储节点转换为主节点，直至主节点数为 2。可参考[转换节点角色](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_55)章节进行转换。

    > **注意**：
    >
    > 每次只能对集群中的某一个节点执行角色转换操作，不支持多个节点同时进行转换。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点 > 设置 SMTX OS 的高可用性

# 设置 SMTX OS 的高可用性

添加完主机后，为保证 SMTX OS 的高可用性，请参考《SMTX OS 双活集群安装部署指南（VMware ESXi 平台）》为新添加的 ESXi 节点继续完成部分参数设置，并在新添加的 SCVM 中部署 IO 重路由脚本，操作步骤如下。

1. 参考[设置 SCVM 在 ESXi 开机时自动启动](/smtxos/6.3.0/vmware_multiactive_installation/vmware_installation_guide/vmware_installation_guide_79)，设置新添加的 SCVM 与 ESXi 主机一起自动启动和关机。
2. 参考[开启 ESXi 主机防火墙的 SSH 服务](/smtxos/6.3.0/vmware_multiactive_installation/vmware_installation_guide/vmware_installation_guide_82)，开启新添加的 ESXi 主机防火墙的 SSH 服务。
3. 参考以下步骤，部署 IO 重路由脚本和 SCVM 自动重启脚本。

   1. 在浏览器中输入新添加的 ESXi 主机的管理 IP，并使用 **root** 账号登录。
   2. 在左侧导航栏中选中 SCVM，打开控制台，执行命令 `zbs-node collect_node_info`。
   3. 可选：若集群已开启 RDMA 特性，则在 SCVM 中继续执行命令 `zbs-deploy-manage deploy-rdma`，否则请忽略此步骤。
   4. 在 SCVM 中执行命令 `zbs-deploy-manage deploy-hypervisor`。

      执行成功后，界面将显示 `Finish deploy hypervisor` 的提示信息，并且 1 分钟后您可以在 SCVM 对应的 ESXi 主机命令行界面上观察到 reroute 进程正在运行。
4. 参考[检查部署结果](/smtxos/6.3.0/vmware_multiactive_installation/vmware_installation_guide/vmware_installation_guide_88)，在 CloudTower 上检查 IO 重路由脚本的部署结果，在新添加的 ESXi 节点上检查 SCVM 自动重启脚本的部署结果。

   > **注意**：
   >
   > - 如果 IO 重路由脚本部署失败，请先根据相关日志定位出失败原因并解决问题，然后在新添加的 SCVM 中执行 `zbs-deploy-manage clear-hypervisor`，最后再重新执行以上部署流程。
   > - 如果 SCVM 自动重启脚本部署失败，请先根据相关日志定位出失败原因并解决问题，然后在新添加的 SCVM 中执行 `zbs-deploy-manage update-scvm-autostart` 命令部署脚本，完成后重新执行检查，确保脚本部署成功。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点 > 为新节点挂载 NFS 数据存储

# 为新节点挂载 NFS 数据存储

完成 SMTX OS 的高可用性设置后，请为新添加的 ESXi 节点挂载 NFS 数据存储。

- 如果需要创建新的 NFS 数据存储进行挂载，请参考《SMTX OS 安装部署指南》的[创建 NFS Export 并挂载至 ESXi 主机](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_77)章节进行操作。
- 如果需要挂载集群中已有的 NFS 数据存储，请参考以下步骤进行操作。

  1. 在 vCenter Server 中选中集群，在右侧管理界面中单击**数据存储**。
  2. 右键单击需要挂载的 NFS 数据存储，选择**将数据存储挂载至其他主机**。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_058.png)
  3. 在弹出的**将数据存储挂载至其他主机**对话框中，选择需要挂载该存储的新 ESXi 主机，单击**确定**。

     ![](https://cdn.smartx.com/internal-docs/assets/9e08ec8e/os_operation_maintenance_059.png)

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点 > 关联新节点与双活集群

# 关联 ESXi 主机与双活集群

1. 在 CloudTower 管理平台中确认节点添加成功。

   - 主机列表中将新增显示该主机的详细信息，该主机为健康状态。
   - 集群概览界面中的存储容量、主机数量、物理盘个数均有增加。
   - 集群概览界面的报警模块新增一条严重警告，提示新加入的 ESXi 主机未与 SMTX OS 集群完成关联。
2. 在 CloudTower 的集群管理界面中单击**设置**按钮，选择 **ESXi**，并输入主机的 ESXi 管理 IP、用户名和密码，将 ESXi 主机与 SMTX OS 集群完成关联。

   关联成功并在大约几分钟以后，集群概览界面中对应的严重警告消失，同时 CPU 总核数和内存容量均有增加。
3. 可选：如果集群已启用机架感知功能，请在 CloudTower 的集群管理界面中单击**全部** > **机架配置**，然后为新 ESXi 主机设置所属机箱和机架。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点 > 扩容后配置

# 扩容后配置

完成双活集群扩容后，必须为新添加节点配置机架拓扑来确保数据副本跨可用域分布；同时，当您在新添加主机中添加虚拟机并运行业务时，还需要在 VMware vCenter 中设置虚拟机放置组规则，以确保双活集群的故障切换能力和高可用能力得以充分发挥。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点 > 扩容后配置 > 配置机架拓扑

# 配置机架拓扑

双活集群扩容后，需要在机架拓扑中将新添加节点放置到正确位置，以使系统可以根据拓扑来调整数据的分配情况，请参考《SMTX OS 管理指南》的[在机箱中添加主机](/smtxos/6.3.0/os_administration_guide/os_administration_guide_167#%E5%9C%A8%E6%9C%BA%E7%AE%B1%E4%B8%AD%E6%B7%BB%E5%8A%A0%E4%B8%BB%E6%9C%BA)小节进行配置。

---

## 节点运维 > 添加节点 > 启用双活特性的 SMTX OS 集群 > 为 SMTX OS（VMware ESXi）双活集群添加新节点 > 扩容后配置 > 在 VMware vCenter 中设置虚拟机放置组规则

# 在 VMware vCenter 中设置虚拟机放置组规则

若原集群已配置虚拟机放置组规则以限制虚拟机优先或必须在某个可用于运行，则在添加 ESXi 主机后，需要将所有新添加的主机添加至对应主机组。

**操作步骤**

1. 登录 vSphere Web Client，浏览并选中集群。
2. 单击**配置**选项卡，选择**配置** > **虚拟机/主机组**。
3. 单击目标主机组，主机组成员将展示在虚拟机/主机组列表下方。单击主机组成员列表上方的**添加**，弹出**添加组成员**对话框。
4. 勾选新添加的 ESXi 主机，并单击**确定**。

此外，当您在新添加节点中正式创建虚拟机并运行业务时，若期望虚拟机在适当主机上运行，则可为虚拟机设置虚拟机放置组规则，或将虚拟机加入已创建的虚拟机组。具体操作步骤请参考《双活集群安装部署指南（VMware ESXi 平台）》的[在 VMware vCenter 中设置虚拟机放置组规则](/smtxos/6.3.0/vmware_multiactive_installation/vmware_multiactive_installation_56)小节。

---

## 节点运维 > 移除节点

# 移除节点

当集群中的主机或 SCVM 发生不可修复的故障需要被彻底移除时，或运维人员需要替换服务器、腾挪节点时，可以在 CloudTower 界面上安全高效地移除主机。

本小节操作适用于未启用双活特性的 SMTX OS 集群，或 SMTX OS 双活集群的可用域中的存储节点。要求如下：

- 未启用双活特性的 SMTX OS 集群：移除节点后集群中至少有 **3** 个健康节点。
- SMTX OS 双活集群：移除节点后优先可用域至少有 **2** 个健康节点，次级可用域至少有 **1** 个健康节点。若集群已启用静态数据加密，且选择**内置密钥管理服务**，则移除节点后要求每个可用域中至少有 **3** 个健康节点，否则无法移除节点。

> **说明**：
>
> - 如果集群不满足上述条件，移除后将不满足 SMTX OS 集群最低节点数要求，会存在数据恢复，无法直接移除该节点请您使用新节点替换该节点，请参考[替换节点](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_73)章节。
> - 若双活集群的**仲裁节点**发生异常需要移除，请联系售后工程师重建双活集群仲裁节点。

**风险提示**

从集群中移除主机将删除该主机上存储的数据，且该操作无法撤回，请谨慎操作。

**注意事项**

- 移除当前主机后，如计划添加新主机进行替换重建，请记录当前主机的主机名和网络配置信息，届时为新主机添加相同的配置。
- 移除无响应主机后，请勿开启该主机。若此主机还需用作其他用途，请先为其重装系统。

**操作步骤**

1. 在 CloudTower 的主机列表单击目标主机右侧的 **...** 后，选择**移除主机**。
2. 在弹出的**移除主机**对话框中，系统将执行如下一系列的预检查。部分检查结果不满足要求时，请参照操作建议手动调整，然后单击**重新检查**再次尝试移除。

   | 预检查要求 | 检查项不符合要求时的操作建议 |
   | --- | --- |
   | 当前主机处于`无响应`或`维护模式`状态。 | 设置主机进入维护模式，或将主机关机。 |
   | （仅 ELF 平台）当前主机上没有回收站以外的虚拟机。 | 请参考表格下方的说明 ① 进行操作。 |
   | （仅 ELF 平台）当前主机上没有被虚拟机挂载的 USB 设备。 | 从虚拟机上卸载 USB 设备。 |
   | 当前主机不是主节点。 | 将主机转换为存储节点。 |
   | 集群中主节点数量满足要求。 | 不满足要求则不允许移除主机。 |
   | 集群 ZooKeeper 及 MongoDB 服务正常运行。 | 修复故障。 |
   | 集群中其他主机的所有存储服务均不处于 `removing` 或 `idle` 状态。 | 等待其他主机的存储服务恢复健康。 |
   | 移除当前主机后，集群中包含健康且非移除中的存储服务的主机数量不少于任⼀虚拟卷或 NFS Export 纠删码配置的数据块（K）和校验块（M）数量之和。 | 移除主机会造成数据丢失，不允许移除主机。 |
   | 集群中其他主机的空闲存储空间充足。 | 扩容集群，或删除部分快照或虚拟机以释放集群容量。 |
   | （仅 ELF 平台）集群中没有涉及当前主机的虚拟机放置组。 | 将当前主机从放置组中移除。 |
   | 集群中没有如下状态的其他主机： - 正在添加； - 正在进入维护模式； - 处于维护模式中； - 正在移除； - 移除失败； - 正在转换角色； - 角色转换失败。 | 等待主机完成当前进行中的任务，并结束当前的状态。 |
   | 集群中没有数据恢复。 | 等待数据恢复完成。 |
   | 集群中没有 dead pextent。 | 联系售后工程师恢复集群数据。 |
   | 集群不处于`升级中`状态。 | 等待集群升级完成。 |
   | （仅双活集群）仲裁节点处于`健康`状态。 | 恢复仲裁节点。 |
   | （仅双活集群）移除当前主机后，优先可用域中至少有 2 个健康的主机，次级可用域中至少有 1 个健康的主机。 | 恢复非健康状态的主机并进行集群扩容。 |

   > **说明 ①**：
   >
   > - 如果主机上存在业务虚拟机，手动关机或迁移至其他主机后再移除当前主机。
   > - 如果主机上存在 SFS 服务的文件控制器，请联系售后工程师将文件控制器下线并迁移至其他主机后再移除当前主机。
   > - 如果主机上存在安全防护虚拟机（SVM）和开启了防病毒或深度包检测的虚拟机（GVM），请完成如下步骤后再移除当前主机：
   >   1. 关闭所有 GVM 的防病毒和深度包检测功能，请参考《SMTX OS 管理指南》[编辑虚拟机基本信息](/smtxos/6.3.0/os_administration_guide/os_administration_guide_040)小节；
   >   2. 取消 Everoute 网络安全导流功能与 SVM 的关联关系，请参考《SMTX OS 管理指南》[编辑虚拟分布式交换机](/smtxos/6.3.0/os_administration_guide/os_administration_guide_108#%E7%BC%96%E8%BE%91%E8%99%9A%E6%8B%9F%E5%88%86%E5%B8%83%E5%BC%8F%E4%BA%A4%E6%8D%A2%E6%9C%BA)小节移除 VDS 与当前主机的关联关系；
   >   3. 关闭 SVM，请参考《SMTX OS 管理指南》[对虚拟机执行电源操作](/smtxos/6.3.0/os_administration_guide/os_administration_guide_052)小节；
   >   4. 删除 SVM 和 GVM，请参考《SMTX OS 管理指南》[永久删除虚拟机](/smtxos/6.3.0/os_administration_guide/os_administration_guide_058)小节。
3. 所有检查项目全部满足要求，在**我确认删除**后的输入框中输入待删除主机的名称，然后单击对话框右下方的**移除**。

   提交任务后页面将展示任务进度以及是否移除成功。如果移除失败，请选择**重新移除主机**，再次提交移除主机任务。

---

## 节点运维 > 转换节点角色

# 转换节点角色

主机和 SCVM 的节点角色包含主节点和存储节点。主节点和存储节点的详细说明请参考《SMTX OS 故障场景说明》[节点类型](/smtxos/6.3.0/failure_scenario_guide/failure_scenario_guide_07)章节。

当节点发生故障或者为了业务负载均衡等情况下需要腾挪节点时，您可以在 CloudTower 界面上高效地将主节点转换为存储节点，或将存储节点转换为主节点。

**操作步骤**

1. 在 CloudTower 的主机列表单击目标主机或 SCVM 右侧的 **...** 后，选择**转换角色**。
2. 在弹出的**转换角色**对话框中，系统将执行一系列的预检查。部分检查结果不满足要求时，请参照操作建议手动调整，然后单击**重新检查**再次尝试转换。

   - **`主节点`转换为`存储节点`**

     | 预检查要求 | 检查项不符合要求时的操作建议 |
     | --- | --- |
     | 集群中全部主机都处于`健康`或`无响应`状态。 | 请恢复主机状态为健康。 |
     | 当前主机转换角色后，集群中健康的主节点数量满足要求： - `健康`状态的主节点转换角色后，集群中健康的主节点数量应 ≥ 3 且 ≤ 5。 - `无响应`状态的主节点转换角色后，集群中健康的主节点数量应 ≥ 2 且 ≤ 5。 | 如果存在不健康的主节点，请恢复主机状态为健康状态；如果主节点均为健康状态且不满足数量要求，不允许转换角色。 |
     | 集群 ZooKeeper 及 MongoDB 服务正常运行。 | 修复故障。 |
     | 集群中没有数据恢复。 | 等待数据恢复完成。 |
     | 集群中没有如下状态的其他主机： - 正在添加； - 正在进入维护模式； - 处于维护模式中； - 正在移除； - 移除失败； - 正在转换角色； - 角色转换失败。 | 等待主机完成当前进行中的任务，并结束当前的状态。 |
     | 集群不处于`升级中`状态。 | 等待集群升级完成。 |
     | （仅双活集群）仲裁节点处于`健康`状态。 | 恢复仲裁节点。 |
   - **`存储节点`转换为`主节点`**

     | 预检查要求 | 检查项不符合要求时的操作建议 |
     | --- | --- |
     | 集群中全部主机都处于`健康`状态，且当前主机未处于`维护模式`状态。 | 如果当前主机处于维护模式，请将其退出维护模式；如果有主机不处于健康状态，请恢复主机状态为健康。 |
     | 当前主机转换角色后，集群中健康的主节点数量应 ≥ 3 且 ≤ 5。 | 如果存在不健康的主节点，请恢复主机状态为健康；如果主节点均为健康状态且不满足数量要求，不允许转换角色。 |
     | 集群 ZooKeeper 及 MongoDB 服务正常运行。 | 修复故障。 |
     | 集群中没有数据恢复。 | 等待数据恢复完成。 |
     | 集群中没有如下状态的其他主机： - 正在添加； - 正在进入维护模式； - 处于维护模式中； - 正在移除； - 移除失败； - 正在转换角色； - 角色转换失败。 | 等待主机完成当前进行中的任务，并结束当前的状态。 |
     | 集群不处于`升级中`状态。 | 等待集群升级完成。 |
     | （仅双活集群）仲裁节点处于`健康`状态。 | 恢复仲裁节点。 |
3. 所有检查项目全部满足要求，单击对话框右下方的**转换**。

   提交转换主机角色任务后，页面将展示任务进度以及是否转换成功。如果转换失败，请选择**重新转换角色**，再次提交转换主机角色任务。

---

## 节点运维 > 替换节点

# 替换节点

SMTX OS（ELF）集群中节点发生故障或需要整机更换时，可以参照本节内容用新节点替换旧节点，无需等待数据迁移，替换后新节点的数据将与原故障节点保持一致。

**适用场景**

- SMTX OS（ELF）集群中节点发生故障时，请参照本节内容用[新节点替换故障节点](#%E6%9B%BF%E6%8D%A2%E6%95%85%E9%9A%9C%E8%8A%82%E7%82%B9)。
- SMTX OS（ELF）集群中有且仅有 3 个健康节点时，如需更换服务器整机，请参照本节内容用[新节点替换旧健康节点](#%E6%9B%BF%E6%8D%A2%E5%81%A5%E5%BA%B7%E8%8A%82%E7%82%B9)。

**注意事项**

原节点移除后，请勿开启该节点。若此节点还需用作其他用途，请先为其重装系统。

**准备工作**

- 记录原节点的主机名、网络配置信息和物理盘用途。
- 将原节点上的所有虚拟机迁移至其他节点。
- 确认新节点的硬件配置满足要求，请参考《SMTX OS 集群安装部署指南（ELF 平台）》的[硬件要求](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_09)章节。
- 在新节点上安装该版本的 SMTX OS 软件，请参考《SMTX OS 集群安装部署指南（ELF 平台）》的[在物理服务器上安装 SMTX OS](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_22) 章节。

## 替换故障节点

1. 确认故障节点的角色，在 CloudTower 的主机列表中查看所有故障节点的角色。

   - 如果故障节点中包含主节点，请参考步骤 2。
   - 如果所有故障节点都是存储节点，请直接参考步骤 3，并跳过步骤 6。
2. 逐一将所有故障主节点转换为存储节点。在集群中除故障节点外的任一节点中执行如下命令，请确保同一时间只有一个节点在转换角色。

   ```
   zbs-cluster convert_to_storage [--is_alive <Boolean>] --ignore_recover_status [--offline_host_ips <offline_host_ips>] <data_ip>
   ```

   - `[--is_alive <Boolean>]`：可选项。故障主节点与集群其他节点的存储网络不连通时，需要填写此参数，并将 `<Boolean>` 设置为 `False`；连通时可以不填写该参数，也可以将 `<Boolean>` 设置为 `True`。
   - `[--offline_host_ips <offline_host_ips>]`：可选项。故障主节点处于无响应状态时需要填写此参数，其中 `<offline_host_ips>` 表示此时集群中所有`无响应`状态节点的存储 IP，多个存储 IP 之间请使用半角逗号 “,” 分隔。
   - `<data_ip>`：表示故障主节点的存储 IP。
3. 确认故障节点处于`无响应`状态。在 CloudTower 的主机列表或概览页中查看故障节点的状态。

   - 故障节点都处于`无响应`状态，请直接参考步骤 4。
   - 故障节点中存在未处于`无响应`状态的节点，请在 CloudTower 主机列表单击该节点右侧的 **...** 后选择**关机**，在弹出的关闭主机对话框中输入**关机原因**，单击**关机**。如果通过 CloudTower 关机失败，可以通过 IPMI 控制或关闭服务器电源使节点处于`无响应`状态。
4. 逐一移除所有故障节点。在集群中除故障节点外的任一节点中执行如下命令，请确保同一时间只有一个节点正在被移除。

   ```
   zbs-deploy-manage meta_remove_node --offline_host_ips <offline_host_ips> --keep_zbs_meta <data_ip>
   ```

   - `<offline_host_ips>` 表示此时集群中所有无响应状态节点的存储 IP，多个存储 IP 之间请使用半角逗号 “,” 分隔。
   - `<data_ip>`：表示故障节点的存储 IP。
5. 将新节点添加至集群，请参考[为集群添加主机](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_39)章节。新节点的主机名和网络配置信息请按照此前记录的故障节点配置信息进行填写；物理盘用途可参考故障节点配置，也可根据实际情况填写。
6. 如果此前移除的故障节点是主节点，需要将新节点从存储节点转换为主节点，请参考[转换节点角色](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_55)章节。
7. 按需将迁移走的虚拟机迁移至新节点。

## 替换健康节点

1. 确认节点的角色，在 CloudTower 的主机列表中查看目标节点的角色。

   - 如果目标节点为主节点，请参考步骤 2。
   - 如果目标节点是存储节点，请直接参考步骤 3，并跳过步骤 6。
2. 将目标节点转换为存储节点。在集群中任一节点中执行如下命令。

   ```
   zbs-cluster convert_to_storage --ignore_recover_status <data_ip>
   ```

   `<data_ip>`：表示目标主节点的存储 IP。
3. 移除目标节点。在集群中除目标节点外的任一节点中执行如下命令，请确保同一时间只有一个节点正在被移除。

   ```
   zbs-deploy-manage meta_remove_node --keep_zbs_meta <data_ip>
   ```

   `<data_ip>`：表示目标节点的存储 IP。
4. 通过 BMC 将目标节点关机，确保目标主机不再占用原 IP。
5. 将新节点添加至集群，请参考[为集群添加主机](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_39)章节。新节点的主机名和网络配置信息请按照此前记录的旧节点配置信息进行填写；物理盘用途可参考旧节点配置，也可根据实际情况填写。
6. 如果此前移除的目标节点是主节点，需要将新节点从存储节点转换为主节点，请参考[转换节点角色](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_55)章节。
7. 按需将迁移走的虚拟机迁移至新节点。

---

## 集群运维 > 更新许可码

# 更新许可码

在如下情况中，需要更新集群许可：

- 首次安装部署集群之后，从试用许可更新为永久许可或订阅许可。
- 需进行主机扩容时，当前最大主机数不再满足需要。
- 版本升级，例如从基础版升级为企业版。
- 延长试用许可或订阅许可有效期。

更新许可时，需将所有当前软件许可信息提供给 SmartX 客户经理，在完成商务流程后，客户经理将提供新的许可码。

**前提条件**

集群已使用的数据分区容量小于等于新导入许可的集群最大容量。

**更新步骤**

1. 将许可码粘贴在**新许可码**处。
2. 单击输入框外部的空白区域，载入新许可信息。
3. 确认无误后，单击**更新**完成许可更新。

---

## 集群运维 > 更新 NTP 服务器

# 更新 NTP 服务器

集群的 NTP 服务器在部署集群时进行过初始设置，如有需要，可以在 CloudTower 中更新设置。

**风险提示**

更新集群的 NTP 服务器的设置会影响集群的可用性，请谨慎操作。

**注意事项**

- 从使用外部 NTP 服务器切换至使用集群内主机作为 NTP 服务器后，无法立即执行其他节点与 NTP Leader 节点的时钟同步，请等待大约 7 分钟再执行操作。
- 如果 CloudTower 配置了 NTP 服务器，请确保集群的 NTP 服务器与 CloudTower 的 NTP 服务器的时钟保持同步。

**操作步骤**

1. 进入集群的管理界面，单击**设置**，选择**集群时间**。
2. 单击 **NTP 服务器**右侧的**编辑**。
3. 在服务器地址列填写外部 NTP 服务器地址，可单击 **+ 添加服务器**增加 NTP 服务器。

   建议配置 3 个及以上的外部 NTP 服务器，并确保集群所有主机均可访问；若不配置外部 NTP 服务器，则所有主机向时钟管理服务主节点保持同步。
4. 填写完成后，单击**检查有效性**进行检查。

   - 若检查不通过，请根据错误提示调整后重新检查。
   - 若检查通过，单击**保存**，完成配置。

---

## 集群运维 > 调整集群系统时间

# 调整集群系统时间

当用户修改集群的 NTP 服务器配置后，例如在使用外部 NTP 服务器和使用内部主机作为 NTP 服务器两个模式间切换时，可能导致集群里某些节点的系统时间不准确，此时可在 CloudTower 中调整集群系统时间，确保集群里所有节点的系统时间保持一致。

**操作步骤**

1. 进入集群的管理界面，单击**设置**，选择**集群时间**。
2. 在**当前时间**区域单击**强制同步**。
3. 在弹出的**强制同步时间**对话框中确认同步方式：

   - 集群已配置外部 NTP 服务器：确认外部 NTP 服务器时间无误后，勾选**我已知晓**。
   - 集群未配置外部 NTP 服务器：填写期望调整到的具体系统时间后，勾选**我已知晓**。
4. 单击**强制同步**，完成更新。

   同步过程中，可在界面查看同步进度，也可在任务中心查看同步状态。

---

## 集群运维 > 创建 SNMP 传输

# 创建 SNMP 传输

SMTX OS 支持使用简单网络管理协议（SNMP）和第三方监控报警平台（如 Zabbix）集成，通过创建 SNMP 传输，使得 SNMP 客户端能接收集群监控信息。

**前提条件**

已在其他监控工具中配置了 SNMP。

**操作步骤**

1. 进入集群的管理界面，单击**设置**，选择 **SNMP 传输**。
2. 在 **SNMP 传输**页签下，单击**创建传输**，在弹出的对话框填写如下信息：

   | 字段 | 说明 |
   | --- | --- |
   | 名称 | 所创建的 SNMP 传输的名称。 |
   | 协议 | 目前仅支持 UDP 协议，无法更改。 |
   | 端口 | 传输端口号，默认为 161。不能为已被其他传输所占用的端口。 |
   | 版本 | v2c/v3。 |
   | 群组  （仅 v2c 需要） | 指定用于访问远程 SNMP 管理器的群组名称。 |
   | 用户名  （仅 v3 需要） | 新增 SNMP 用户的用户名。 |
   | 用户密码  （仅 v3 需要） | 用于认证的用户密码。 |
   | 身份认证协议  （仅 v3 需要） | MD5/SHA，加密用户密码的协议，用于确保用户身份的安全性。 |
   | 隐私协议  （仅 v3 需要） | DES/AES，对 SNMP 消息进行加密的方式。 |
   | 私有密钥  （仅 v3 需要） | 加密时使用的密钥。 |
3. 单击**创建**，完成创建操作。

---

## 集群运维 > 编辑主机 IPMI 信息

# 编辑主机 IPMI 信息

为主机设置 IPMI 信息后，您可以在 CloudTower 上查看 SMTX Halo 超融合一体机的机箱拓扑和电源监控，查看主机的风扇转速和 CPU 温度。

**操作步骤**

1. 您可以在 CloudTower 主页面左侧的导航栏中选择某一集群，在右侧的管理页面选择**设置** > **IPMI 信息**。
2. 编辑主机的 IPMI 信息。密码留空则不更新。

   - 单独编辑：单击**编辑**，设置其中一个主机的 IPMI IP、用户名或密码。
   - 批量编辑：单击**批量编辑**，通过起始 IPMI IP 和统一的用户名及密码设置全部主机的 IPMI 信息。
3. 单击**保存**。提交修改后，若验证失败，会出现相应提示。

---

## 集群运维 > 更新 DNS 服务器

# 更新 DNS 服务器

DNS 服务器在部署集群时进行过初始设置，如有需要，可以在 CloudTower 中更新设置。

**风险提示**

更新 DNS 服务器的设置会影响集群的可用性，请谨慎操作。

**操作步骤**

1. 进入集群的管理界面，单击**设置**，选择 **DNS 服务器**。
2. 输入 DNS 服务器地址，多个服务器地址可用半角逗号“,”分隔。
3. 单击**保存**，完成修改。

---

## 集群运维 > 更新管理虚拟 IP

# 更新管理虚拟 IP

设置集群的管理虚拟 IP 是为了保证集群管理界面的高可用。访问此 IP 时，可以自动通过集群内任一可用的 SMTX OS 管理 IP（ELF 平台）或 SCVM 管理 IP（VMware ESXi 平台）访问集群。

**注意事项**

- 必须确保管理虚拟 IP 与节点的 SMTX OS 管理 IP（ELF 平台）或 SCVM 管理 IP（VMware ESXi 平台）在同一个子网内，并且 CloudTower 可以通过管理虚拟 IP 访问集群。
- 若 SMTX OS 集群中已部署文件存储集群，则 SMTX OS 集群的管理虚拟 IP 不允许设置为空。

**操作步骤**

1. 在集群的管理界面中，单击**设置**，选择**虚拟 IP**。
2. 修改管理虚拟 IP。
3. 单击**保存**。

---

## 集群运维 > 设置服务端口

# 设置服务端口

为保障集群中主机的访问安全，您可以查看主机内部服务已使用的端口及其用途、启用端口访问控制、并对 ssh 和 snmp 服务端口配置 IP 白名单。

此外，您还可以统一修改集群中所有主机的 ssh 服务端口，以提升集群安全性、满足审计或合规要求。

## 配置端口访问控制

仅允许指定 IP 访问端口，从而实现最小化的访问控制，防止外部网络攻击。

**规则生效顺序**

配置完成后访问控制规则的生效顺序如下：

1. 存储网段内的所有 IP 地址：可以通过任意端口通信。
2. 主机中的其他 IP 地址（如管理 IP、迁移 IP 等）：
   - 已配置访问限制的端口：仅允许指定 IP 访问。
   - 未配置访问限制的端口：允许所有 IP 访问。
3. 内部服务未使用的端口：端口关闭，无法访问。

**注意事项**

- 如已在主机上通过 `iptables` 自定义配置安全规则，在启用端口访问控制之前，需要手动清理所有已配置的规则，否则可能由于规则冲突而导致配置不生效。
- 在集群中添加新主机后，为确保集群服务正常运行，请重新编辑存储网段规则，确保新主机的存储 IP 地址在设置的存储网段范围内。新添加的主机默认允许全部 IP 访问该主机的服务端口，您可以按需为该主机的服务端口设置 IP 白名单。
- 为确保巡检中心能够正常访问集群主机并完成巡检任务，请将集群中所有主机的管理 IP 地址添加至 ssh 端口的 IP 白名单。

**操作步骤**

1. 在集群管理页面选中某一集群，单击**设置**，选择**服务端口**。
2. 在**访问控制**区域启用端口访问限制。

   1. 单击**编辑**。
   2. 启用**访问限制**，并添加**存储网段**。
      - 对于 SMTX OS (ELF) 集群，请确保所有主机的存储 IP 均包含在存储网段范围内。
      - 对于 SMTX OS (VMware ESXi) 集群，请确保所有 SCVM 存储 IP 及 ESXi 存储 IP 包含在存储网段范围内。
   3. 单击**保存**。
3. 在**服务端口**区域为 snmp 或 ssh 服务端口设置 IP 白名单。

   1. 单击 **...** > **编辑 IP 白名单**。
   2. 选择配置方式。
      - **按集群配置**：批量为集群中的所有主机配置相同的 IP 白名单，配置后统一下发至所有主机。
      - **按主机配置**：对集群中的每个主机单独配置不同的 IP 白名单。
   3. 设置 IP 白名单。当选择**按主机配置**时，需为每个主机配置 IP 白名单，支持批量填充。
      - **全部禁止**：禁止全部 IP 访问该主机的服务端口。
      - **允许指定 IP**：允许指定的 IP 访问该主机的服务端口。单击 **+ 添加**，可添加多个 IP 地址、IP 地址范围或 CIDR 块。
      - **全部允许**：允许全部 IP 访问该主机的服务端口。
   4. 单击**保存**。

**相关操作**

当您不再需要使用端口访问控制功能时，可以手动关闭该功能。关闭后，集群中所有主机的安全规则将被清空，所有服务端口将允许全部 IP 地址访问。

## 编辑 ssh 服务端口

**注意事项**

- 当集群或主机处于如下状态时，无法编辑 ssh 的服务端口：

  - 集群正在升级、执行巡检任务、采集日志或强制同步集群时间
  - 集群正在添加主机
  - 集群连接异常
  - 主机处于`关机中`、`重启中`、`异常`或`无响应`状态
  - 主机正在进入或退出维护模式
- 集群中所有主机的 ssh 服务端口号需保持一致；若不一致，页面将弹出提示，请重新编辑端口号并保存。
- 对于 SMTX OS (VMware ESXi) 集群，本操作仅修改 SCVM 的 ssh 服务端口，不会影响 ESXi 主机的端口设置。请确保 ESXi 主机的 ssh 服务端口保持默认 `22`，以免影响集群扩容或升级操作。

**操作步骤**

1. 在集群管理页面选中某一集群，单击**设置**，选择**服务端口**。
2. 在**服务端口**区域，单击 ssh 服务右侧的 **...** > **编辑端口号**。
3. 输入新端口号，建议配置在 10022～10099 范围内，该端口号需未被其他服务所使用。
4. 勾选**我已知晓**，阅读并确认端口号变更的影响。
5. 单击**检查**，确认是否可变更为新端口号。若检查未通过，请根据页面提示修复对应问题，再单击**重新检查**。
6. 全部检查通过后单击**保存**。

---

## 集群运维 > 更新 SCVM 管理 IP（VMware ESXi 平台）

# 更新 SCVM 管理 IP（VMware ESXi 平台）

对于 SMTX OS（VMware ESXi）集群，您可以更新集群内各个节点的 SCVM 管理 IP。

**注意事项**

SCVM 管理 IP 必须遵循以下规则：

- SCVM 管理 IP 在管理网络的网段内。
- SCVM 管理 IP 和 SCVM 存储 IP 不能分配在同一网段。
- 集群各节点的 SCVM 管理 IP 需要分配在同一网段。
- 集群各节点的 SCVM 管理 IP 和 ESXi 管理 IP 之间可以正常通信。

**操作步骤**

1. 在集群的管理界面中，单击**设置**，选择**管理 IP**。
2. （可选）修改管理网络的子网掩码和网关。
3. 修改节点的 SCVM 管理 IP，即界面上主机的管理 IP。
4. 单击**保存**。

---

## 集群运维 > 编辑主机的 ESXi 关联信息（VMware ESXi 平台）

# 编辑主机的 ESXi 关联信息（VMware ESXi 平台）

为主机设置 ESXi 关联信息后，可以获取 SMTX OS（VMware ESXi）集群的 ESXi 主机硬件信息，还可以配置 ESXi 主机 IO 重路由和 SCVM 随 ESXi 开机而自动启动。

1. 您可以在 CloudTower 主页面左侧的导航栏中选择某一 SMTX OS（VMware ESXi）集群，在右侧的管理页面选择**设置** > **ESXi**。
2. 编辑主机的 ESXi 关联信息。密码留空则不更新。

   - 单独编辑：单击**编辑**，设置其中一个主机的 ESXi IP、用户名或密码。
   - 批量编辑：单击**批量编辑**，通过起始 ESXi IP 以及统一的用户名及密码设置全部主机的 ESXi 关联。
3. 单击**保存**。提交修改后，若验证失败，会出现相应提示。

---

## 集群运维 > 更新 vCenter Server 的关联信息（VMware ESXi 平台）

# 更新 vCenter Server 的关联信息（VMware ESXi 平台）

对于 SMTX OS（VMware ESXi）集群，您可以更新 vCenter Server 的关联信息。

**前提条件**

vCenter 中至少包含一个数据中心和一个集群。

**操作步骤**

1. 在集群的管理界面中，单击**设置**，选择 **vCenter Server**。
2. 单击**更新**，修改以下参数。

   - **vCenter 地址**：输入新的 vCenter 地址。
   - **管理员用户名/密码**：输入 vCenter 的管理员账号和密码，以保证必要的资源操作权限。
3. 单击**关联**。

   系统将在后台对 vCenter 地址、用户名和密码进行认证，认证通过后即关联成功。

---

## 附录 > 根据 NVMe 直通硬盘名称获取对应的 ESXi PCI ID

# 根据 NVMe 直通硬盘名称获取对应的 ESXi PCI ID

热添加和热移除命令需要使用 NVMe 直通硬盘对应的 ESXi PCI ID ，下面将以名称为 s100 的 SCVM、名称为 nvme0n1 的 NVMe 硬盘为例，描述获取该硬盘 ESXi PCI ID 的过程。

1. 在 NVMe 直通硬盘所在的 SCVM 中执行如下命令获取硬盘对应的 SCVM PCI ID。

   ```
   udevadm info -q path /dev/nvme0n1
   ```

   **输出示例**

   ```
   /devices/pci0000:03/0000:03:00.0/nvme/nvme0/nvme0n1
   ```

   输出结果中的 `0000:03:00.0` 为该硬盘的 SCVM PCI ID。
2. 执行如下命令，根据 SCVM PCI ID 获取该 PCI 设备对应 ESXi 虚拟机的设备名称及设备插槽序号。

   ```
   lspci -v -s 0000:03:00.0
   ```

   **输出示例**

   ```
   03:01.0 Non-Volatile memory controller: Intel Corporation NVMe Datacenter SSD [3DNAND, Beta Rock Controller] (prog-if 02 [NVM Express])
     DeviceName: pciPassthru1
     Subsystem: Intel Corporation NVMe Datacenter SSD [3DNAND] ME 2.5" U.2 (P4610)
     Physical Slot: 65
     Flags: bus master, fast devsel, latency 64, IRQ 18, NUMA node 0
     Memory at ffb14000 (64-bit, non-prefetchable) [size=16K]
     Capabilities: [40] Power Management version 3
     Capabilities: [50] MSI-X: Enable+ Count=128 Masked-
     Capabilities: [60] Express Endpoint, MSI 00
     Capabilities: [a0] MSI: Enable- Count=1/1 Maskable- 64bit+
     Capabilities: [100] Advanced Error Reporting
     Capabilities: [150] Virtual Channel
     Capabilities: [180] Power Budgeting <?>
     Capabilities: [190] Alternative Routing-ID Interpretation (ARI)
     Capabilities: [270] Device Serial Number 55-cd-2e-41-50-99-15-f8
     Capabilities: [2a0] Secondary PCI Express
     Capabilities: [2d0] Latency Tolerance Reporting
     Capabilities: [310] L1 PM Substates
     Kernel driver in use: nvme
     Kernel modules: nvme
   ```

   输出结果中的 `DeviceName` 表示此 PCI 设备对应 ESXi 虚拟机的设备名称，`Physical Slot` 表示此 PCI 设备对应 ESXi 虚拟机的设备插槽序号。

   > **注意**：
   >
   > 部分 PCI 设备可能不存在 `DeviceName`，此时仅获取 `Physical Slot` 即可。
3. SSH 登录到 SCVM 所在的 ESXi 主机，执行如下命令找到 SCVM 的配置文件目录。

   ```
   find /vmfs/volumes/ -type d -name 's100'
   ```

   **输出示例**

   ```
   /vmfs/volumes/65002d70-e4c9f18d-d7e5-b49691f2e1c8/s100
   ```
4. 进入 SCVM 的配置文件目录后，找到 SCVM 的 `.vmx` 文件，执行如下命令获取 `<devicename>.id`。其中 `<devicename>` 表示在步骤 2 中获取到的设备名称，如 `pciPassthru1`。

   > **注意**：
   >
   > 如果在步骤 2 中仅获取到设备插槽序号，如 `65`，可根据输出结果中的 `pciPassthru1.pciSlotNumber = "65"` 确定设备名称为 `pciPassthru1`。

   ```
   grep 'pciPassthru' s100.vmx
   ```

   **输出示例**

   ```
   pciPassthru0.id = "00000:090:00.0"
   pciPassthru0.deviceId = "0x005d"
   pciPassthru0.vendorId = "0x1000"
   pciPassthru0.systemId = "658e9fb5-c1e3-43f4-7b65-7cd30ae17a18"
   pciPassthru0.present = "TRUE"
   pciPassthru1.id = "00000:217:00.0"
   pciPassthru1.deviceId = "0x0a54"
   pciPassthru1.vendorId = "0x8086"
   pciPassthru1.systemId = "658e9fb5-c1e3-43f4-7b65-7cd30ae17a18"
   pciPassthru1.present = "TRUE"
   pciPassthru2.id = "00000:218:00.0"
   pciPassthru2.deviceId = "0x0a54"
   pciPassthru2.vendorId = "0x8086"
   pciPassthru2.systemId = "658e9fb5-c1e3-43f4-7b65-7cd30ae17a18"
   pciPassthru2.present = "TRUE"
   pciPassthru0.pxm = "0"
   pciPassthru1.pxm = "0"
   pciPassthru2.pxm = "0"
   pciPassthru0.pciSlotNumber = "64"
   pciPassthru1.pciSlotNumber = "65"
   pciPassthru2.pciSlotNumber = "66"
   ```
5. 将在上一步中获取到的`<devicename>.id` 中的十进制数转换为十六进制，例如十进制 217 对应的十六进制为 d9，则该设备的 ESXi PCI ID 为 0000:d9:00.0。

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
