---
title: "SMTXZBS/5.7.0/SMTX ZBS 块存储集群运维指南"
source_url: "https://internal-docs.smartx.com/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_preface_generic"
sections: 58
---

# SMTXZBS/5.7.0/SMTX ZBS 块存储集群运维指南
## 关于本文档

# 关于本文档

本文档介绍了 SMTX ZBS 块存储集群上线运行后需要定期监控的关键信息，以及在集群遇到故障后的处理办法和指导原则。此外，该文档还收录了在维护块存储集群时可能会遇到的部分场景和解决办法。

阅读本文档需了解块存储软件，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

**2025-12-01**：**文档随 SMTX ZBS 5.7.0 正式发布**。

相较于 5.6.4 版本，本版本，本版本主要更新如下：

- **物理盘运维**：

  - 删除**物理盘故障**小节，请通过《SMTX ZBS 故障处理指南》了解相关内容。
  - 更新**卸载物理盘**小节。
  - 增加**更换 SMTX 系统盘**小节。
- **其他部件运维**：更新**增加网卡**小节。
- **节点运维**：增加**移除节点**、**转换节点角色**、**替换节点**、**为 SMTX ZBS 双活集群添加节点**小节。
- **集群运维**：增加**更新端口访问控制**小节。

---

## 例行检查

# 例行检查

SMTX ZBS 集群正式上线运行后，IT 基础架构管理员或运维工程师需要定期登录集群的管理平台，监控 SMTX ZBS 集群的运行情况，及时分析集群的日志和报警信息并定位问题，以保证集群正常运行。

## 查看资源

您可以通过 CloudTower 查看主机、集群的运行状态和资源使用情况。

- **主机**：您可以在 CloudTower 主页面左侧的导航栏中选择组织、数据中心、集群或双活集群的可用域，在右侧的管理页面选择主机，资源列表中会展示所选范围内所有主机的信息。信息的具体说明请参考《SMTX ZBS 管理指南》[查看主机信息](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_070)章节。
- **集群**：您可以在 CloudTower 主页面左侧的导航栏中选择组织、数据中心，在右侧的管理页面选择集群，资源列表中会展示所选资源内所有集群的信息。信息的具体说明请参考《SMTX ZBS 管理指南》[了解 SMTX ZBS 集群](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_003)章节。

## 查看监控

通过监控分析功能，通过对集群内的虚拟机和主机等多种资源对象的指标进行监控，并以视图和图表的方式组织和呈现数据，以帮助您对资源使用情况进行分析。详情请参考《SMTX ZBS 管理指南》[监控分析](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_099)章节。

除 SMTX ZBS 提供的监控分析外，还可以通过部署可观测性服务和高级监控实现集群更全面的监控。

- 可观测性服务支持按需随时增加 CPU、内存和存储资源，确保在监控数据量显著增长的情况下监控性能不受影响，还支持更深入地分析和处理监控数据。详情请参考对应版本的《可观测性平台用户指南》**管理监控功能**章节。
- 高级监控支持保存更长时间的数据，还支持自定义 CPU、内存和存储资源。详情请参考对应版本的《CloudTower 使用指南》**管理高级监控**章节。

相较于高级监控，可观测性服务提供更稳定的数据采集和存储能力、更丰富的监控报警能力，并且支持统一处理多个集群的数据，建议优先部署可观测性服务。已部署高级监控的集群，建议部署可观测性服务，并将高级监控的数据迁移至可观测性服务。

## 查看报警

报警信息包含了该报警的触发原因、可能产生的影响以及推荐的解决方法等。您可以通过告警信息判断当前集群的运行状况，定位具体的问题。详情请参考对应版本的《CloudTower 使用指南》**管理报警**章节。

关联了可观测性服务后，可选择通过可观测性服务将集群的报警信息发送到指定的邮箱、webhook 或第三方监控平台，获得增强的报警通知能力。详情请参考对应版本的《可观测性平台用户指南》**管理报警功能**章节。

## 查看日志

您可以采集集群的操作系统日志、SMTX ZBS 服务日志、Coredump 日志和节点信息。详情请参考《SMTX ZBS 管理指南》[采集日志](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_132)章节。

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

1. 登录 CloudTower，将待升级物理盘固件的节点[置为维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)。
2. 在 CloudTower 中[关闭](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_09)该节点。
3. 升级固件，确认固件版本为目标版本后启动服务器。
4. 登录 CloudTower，将该节点[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)。
5. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`
6. 在集群任意节点执行如下命令，确认数据恢复是否完成：

   `sudo zbs-meta pextent find need_recover`

   若返回 `No PExtents found.` 表示数据恢复完成。否则请等待一段时间再次数据恢复完成。

## 在线升级系统盘固件

1. 登录 CloudTower，将待升级物理盘固件的节点[置为维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)。
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
8. 在 CloudTower 上将该节点[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)。
9. 在集群任意节点执行如下命令，确认数据恢复是否完成：

   `sudo zbs-meta pextent find need_recover`

   若返回 `No PExtents found.` 表示数据恢复完成。否则请等待一段时间再次数据恢复完成。

## 在线升级非系统盘固件

1. 将待升级物理盘固件的主机设置为存储维护模式，请参考《SMTX ZBS CLI 命令参考》确认 chunk ID 并[设置 chunk 进入存储维护模式](/smtxzbs/5.7.0/zbs_cli_guide/zbs_cli_guide_30)。

   输出内容中 ID 和 IP 是待升级物理盘固件的主机且 `Maintenance Mode` 为 **True** 则表示进入存储维护模式成功。进入存储维护模式成功之后，等待 10 秒。
2. 在待升级物理盘固件的节点命令行终端执行如下命令，停止节点 chunk 服务：

   `sudo systemctl stop zbs-chunkd`
3. 继续执行如下命令，确认 chunk 服务已经停止：

   `sudo systemctl status zbs-chunkd`

   输出如下结果表示 chunk 服务已经停止，请确认此时 `Active` 为 **inactive (dead)**：

   ```
     ● zbs-chunkd.service - ZBS Chunk service
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
       ● zbs-chunkd.service - ZBS Chunk service
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
8. 将节点退出存储维护模式，请参考《SMTX ZBS CLI 命令参考》确认 chunk ID 并[设置 Chunk 退出存储维护模式](/smtxzbs/5.7.0/zbs_cli_guide/zbs_cli_guide_30)。
9. 在集群任意节点执行如下命令，确认数据恢复是否完成：

   `sudo zbs-meta pextent find need_recover`

   若返回 `No PExtents found.` 表示数据恢复完成。否则请等待一段时间再次数据恢复完成。

---

## 物理盘运维 > 定位物理盘

# 定位物理盘

通过物理盘的闪灯和灭灯您可以确定物理盘在服务器中的位置。

如您使用非 NVMe SSD 物理盘，且存储控制器在下表所示的兼容性范围内，您可以通过 [CloudTower 的闪灯和停止闪灯功能](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_35)快速定位物理盘在服务器中的位置。

如果使用的是 NVMe SSD 或存储控制器不在下表的兼容性范围内，请您根据物理盘驱动类型[使用 CLI 命令](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_26)定位。

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
2. 在弹出的物理盘详情面板中单击**闪灯**或**停止闪灯**，通服务器上物理盘的闪灯或灭灯确定物理盘的位置。

---

## 物理盘运维 > 定位物理盘 > 使用 CLI 命令定位

# 使用 CLI 命令定位

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
        0     SAS2008     1000h    72h   00h:02h:00h:00h      1170h   6019h

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

        执行命令后，输出如下内容。**Channel,Device** 和 **Serial number** 成对出现，分别表示 **channel\_id**、**device\_id** 和对应的物理盘序列号，由此可通过之前已获取的物理盘序列号来确定对应的插槽号。

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

挂载前请确认块存储集群的部署模式，不同部署模式下允许挂载的物理盘不同：

- 块存储集群采用不分层模式时，只允许挂载 SSD。
- 块存储集群采用分层模式且缓存和数据共用所有物理盘时：

  - 节点配置为全 NVMe SSD 全闪配置时，只允许挂载 NVMe SSD。
  - 节点配置为全 SATA/SAS SSD 全闪配置时，只允许挂载 SATA/SAS SSD。
- 块存储集群采用分层模式且缓存盘和数据盘独立部署时，允许挂载 SSD 和 HDD，但 HDD 只允许挂载为`数据盘`。

不同容量规格的主机可挂载的数据分区总容量限制请参考下表：

| 主机容量规格 | 数据分区总容量限制 |
| --- | --- |
| 标准容量 | 128 TiB |
| 大容量 | 256 TiB |
| 加大容量 | 512 TiB |

**风险提示**

挂载物理盘会清除该物理盘上的所有数据，请谨慎操作。

**操作步骤**

1. 在 CloudTower 主页面左侧导航栏中，选择一个组织、数据中心、集群或主机后，选择**全部** > **物理盘**，物理盘列表页面将会提示当前范围内健康且可挂载的物理盘的数量。
2. 选择待挂载的物理盘，您可以通过如下两种方式选择：

   - 单击 `x 块健康的物理盘可挂载。`提示右侧的**查看**，将会展示该范围下所有可挂载的物理盘，请您勾选同一集群内需要挂载的一个或多个物理盘，然后单击**挂载**。
   - 在物理盘列表中根据需求勾选属于同一集群的一个或多个状态为`健康盘·可挂载`的物理盘，单击**挂载**。
3. （可选）如果主机有多个物理盘池，系统将自动为每块物理盘选择一个物理盘池，您可以按需将物理盘移动至其他物理盘池中。请单击物理盘用途右侧的![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_69.png)按钮，选择目标物理盘池。

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

**注意事项**

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

**操作步骤**

1. 进入 CloudTower 的**物理盘**页面，在物理盘列表中单击待卸除的物理盘右侧的 **...** 后，选择 **卸载**。
2. 在弹出的**卸载物理盘**对话框中根据物理盘的基本信息确认待卸载的物理盘及其所属的主机，单击**卸载**。

---

## 物理盘运维 > 更换物理盘

# 更换物理盘

如您需要更换集群中的物理盘，请您先通过 CloudTower [卸载物理盘](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_04)，并确认数据迁移完成后参照本章节的内容，在服务器上更换物理盘。

---

## 物理盘运维 > 更换物理盘 > 更换 SSD

# 更换 SSD

**适用场景**

SSD 的更换操作与集群部署时是否采用存储分层模式和该硬盘的用途有关。本节描述的步骤仅适用于以下两种场景：

- 集群采用存储分层模式，当前用途为`缓存盘`、`含元数据分区的缓存盘`、`数据盘`或`含元数据分区的数据盘`的 SSD 更换。
- 集群采用不存储分层模式，当前用途为`数据盘`的 SSD 更换。

对于采用不存储分层模式的集群，当前用途为`不含元数据分区的数据盘` 的 SSD 更换步骤请参考​[更换 HDD ​](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_17)。

对于当前用途为 `SMTX 系统盘`的 SSD 更换步骤请参考[更换 SMTX 系统盘](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_90)。

**准备工作**

- 确认即将安装的 SSD 与服务器机型兼容，可通过[硬件兼容性查询工具](https://www.smartx.com/smtxzbs-compatibility/)进行查询，且即将安装的 SSD 的容量不低于原来的 SSD 的容量。
- 确定并记录待更换 SSD 所在的物理节点序列号、机架所在位置以及需要更换的物理盘槽位。可参考​[物理盘闪灯定位​](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_01)点亮物理盘的指示灯以确定物理盘在主机上的位置。
- 登录 CloudTower 管理平台，[卸载](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_04)该 SSD。

**操作步骤**

1. 按照下图所示操作，从主机上拔除 SSD。

   1. 按压释放按钮以打开硬盘托架释放手柄。
   2. 握住硬盘托架释放手柄，将硬盘托架滑出驱动器插槽。

   ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_042.png)
2. 登录 CloudTower，报警信息将提示系统侦测到物理盘从主机上拔出，如果主机是多节点高密服务器或刀片服务器，拔除物理盘后还会提示该物理盘插槽在机箱中的位置。
3. 按照下图所示操作，在物理服务器上安装新的 SSD。

   1. 将新硬盘托架滑入硬盘插槽中。
   2. 合上硬盘托架释放手柄以将硬盘锁定到位。

   ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_045.png)
4. 登录 CloudTower，报警信息将提示系统侦测到有新的物理盘从主机中插入。
5. 使用 SSH 方式登录 SSD 所在的节点，执行命令 `lsblk`，查看新安装的 SSD，此时物理盘尚未被分区，如下例所示的 **sdb**。

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
6. 登录 CloudTower，[挂载](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_03)新的 SSD。
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

## 物理盘运维 > 更换物理盘 > 更换 HDD

# 更换 HDD

**准备工作**

- 确认即将安装的 HDD 与服务器机型兼容，可通过[硬件兼容性查询工具](https://www.smartx.com/smtxzbs-compatibility/)进行查询，且即将安装的 HDD 的容量不低于原来的 HDD 的容量。
- 确定并记录待更换 HDD 所在的物理节点序列号、机架所在位置以及需要更换的物理盘槽位。可参考​[物理盘闪灯定位​](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_01)点亮物理盘的指示灯以确定物理盘在主机上的位置。
- 登录 CloudTower 管理平台，[卸载](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_04)该 HDD。

**操作步骤**

1. 按照下图所示操作，从主机上拔除 HDD。

   1. 按压释放按钮以打开硬盘托架释放手柄。
   2. 握住硬盘托架释放手柄，将硬盘托架滑出驱动器插槽。

   ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_042.png)
2. 登录 CloudTower，报警信息将提示系统侦测到物理盘从主机上拔出，如果主机是多节点高密服务器或刀片服务器，拔除物理盘后还会提示该物理盘插槽在机箱中的位置。
3. 按照下图所示操作，在物理服务器上安装新的 HDD。

   1. 将新硬盘托架滑入硬盘插槽中。
   2. 合上硬盘托架释放手柄以将硬盘锁定到位。

   ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_045.png)
4. 登录 CloudTower，报警信息将提示系统侦测到有新的物理盘从主机中插入。
5. 使用 SSH 方式登录 HDD 所在的节点，执行命令 `lsblk`，查看新安装的 HDD，此时物理盘尚未被分区，如下例所示的 **sdf**。

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
6. 登录 CloudTower，[挂载](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_03)新的 HDD。
7. 挂载成功后，可在主机的物理盘列表中确认该 HDD 的挂载状态为**已挂载**，更换操作结束。
8. 如果通过 CloudTower 挂载 HDD 失败，可参考如下步骤，通过命令行重新挂载 HDD，其中 `sdf` 表示挂载的 HDD 盘。

   ```
   `zbs-deploy-manage mount-disk /dev/sdf data`

   系统输出如下信息，表明挂载物理盘成功。

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

本小节介绍了在 SMTX ZBS 集群的主机上更换 SMTX 系统盘中的成员物理盘的操作方法。

定位物理盘槽位前，请您确认存储控制器型号以及是否支持物理盘闪灯功能：

- 如果存储控制器支持物理盘闪灯，此时可以快速通过界面的闪灯功能确定物理盘的槽位，而支持物理盘闪灯也通常意味着支持物理盘热插拔，请参考[不停机更换物理盘](#%E4%B8%8D%E5%81%9C%E6%9C%BA%E6%9B%B4%E6%8D%A2%E7%89%A9%E7%90%86%E7%9B%98)章节内容更换该物理盘。
- 如果存储控制器不支持物理盘闪灯，则可以通过物理盘序列号定位其槽位，而不支持物理盘闪灯也通常意味着不支持物理盘热插拔，请参考[停机更换物理盘](#%E5%81%9C%E6%9C%BA%E6%9B%B4%E6%8D%A2%E7%89%A9%E7%90%86%E7%9B%98)章节内容关停服务器并更换物理盘。

> **说明**：
>
> SMTX 系统盘的成员物理盘仅能通过**成员物理盘**页签内的**序列号**识别，无法通过**成员物理盘**页签内的**槽位**识别。`0 号`和 `1 号`仅代表成员物理的序号，无法唯一标识这块盘。

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
2. 登录 CloudTower，将待更换物理盘的节点[置为维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)。
3. 在 CloudTower 中将待更换物理盘的节点[关闭](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_09)。
4. 断开服务器机箱电源，并打开服务器机箱外壳。
5. 根据序列号拔除故障的物理盘，并在原来物理盘的槽位中插入新的物理盘。

   > **注意：**
   >
   > 请确保更换的新物理盘与原 RAID 组中的成员物理盘规格一致。
6. 恢复服务器机箱外壳并接入机箱电源，对服务器执行开机。
7. 登录 CloudTower，将该节点[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)。
8. 等待存储控制器完成硬件 RAID 重建，使两块物理盘之间的数据完成同步。

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

![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_067.png)

重建完毕后，新插入的磁盘会自动重新加入 RAID 组：

![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_068.png)

---

## 其他部件运维 > 增加内存

# 增加内存

当块存储集群的 CPU 使用率不高，空闲的存储资源较多，但可分配的内存比较紧张时，建议为集群的主机增加内存。

**准备工作**

检查正在运行的主机中的内存条和待增加的内存条，确保这两个内存条的型号与主频一致。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间增加内存，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间增加内存，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，将待增加内存的节点[置为维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)。
2. 在 CloudTower 中将待增加内存的节点[关闭](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_09)。
3. 为服务器安装新内存条，并记录内存安装槽位，然后启动服务器。
4. 启动服务器，开机后登录节点的 IPMI 管理台，确认 IPMI 管理台已识别新增加的内存。
5. 登录 CloudTower，将该节点[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)。
6. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`
7. 登录 CloudTower，进入该主机的概览界面，查看**主机信息**模块中的**内存容量**参数，确认主机的内存容量已增加。

---

## 其他部件运维 > 更换内存

# 更换内存

**准备工作**

检查主机中的故障内存和即将安装的内存，确保这两个内存的型号与主频一致。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间更换内存，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间更换内存，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，将待更换内存的节点[置为维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)。
2. 在 CloudTower 中将待更换内存的节点[关闭](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_09)。
3. 更换内存，并记录内存安装槽位，然后启动服务器。
4. 登录节点的 IPMI 管理台，确认 IPMI 管理台已识别新更换的内存。
5. 登录 CloudTower，将该节点[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)。
6. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`
7. 登录 CloudTower，进入该主机的概览界面，查看**主机信息**模块中的**内存容量**参数，确认主机的内存容量显示符合预期。

---

## 其他部件运维 > 增加网卡

# 增加网卡

当块存储集群承载的业务越来越多，接入/存储网络的带宽出现瓶颈时，可以通过在服务器节点上增加网卡来提升网络带宽。例如，网络的带宽从 10 Gbps 增加至 2x10 Gbps Bonding 及以上。

> **说明**：
>
> 如果增加网卡的目的是为了增加带宽而不是仅用于高可用，建议对启用了 NVMe over RDMA 功能的接入网络使用 802.3ad 绑定模式；对其他网络使用 balance-tcp 绑定模式。

**准备工作**

确认新增的网卡与服务器机型兼容，可通过[硬件兼容性查询工具](https://www.smartx.com/smtxzbs-compatibility/)进行查询。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间增加网卡，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间增加网卡，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，将待增加网卡的节点[置为维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_06)。
2. 在 CloudTower 中将待增加网卡的节点[关闭](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_09)。
3. 在服务器中插入新网卡，然后启动服务器。
4. 登录节点的 IPMI 管理台，确认 IPMI 管理台已识别新增加的网卡。
5. 登录 CloudTower，将该节点[退出维护模式](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_07)。
6. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

---

## 节点运维 > 设置维护模式

# 设置维护模式

在主机离线维护时使用维护模式，系统将自动检查集群和主机的状态，确保集群里其它主机的关键服务运行正常，保障集群剩余数据的安全；还可以自动迁移系统服务虚拟机，减少主机离线维护操作期间产生的数据恢复量，提高主机上线后完成数据恢复的速度。

在以下场景**推荐使用**维护模式，可提高运维效率：

- 升级时，例如升级固件、升级内核等。
- 更换除物理盘以外的硬件时，例如更换内存、网卡、CPU、存储控制器等。
- 从块存储集群中移除主机时。

---

## 节点运维 > 设置维护模式 > 维护流程

# 维护流程

![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_011.png)

**进入维护模式前**：系统进行预检查，块存储集群和主机状态符合要求才允许进入维护模式。

**进入维护模式中**：设置主机进入维护模式，主机状态为`进入维护模式中`。

1. 在进入维护模式的过程中，系统自动将该主机上所有`运行中`的系统服务虚拟机热迁移至集群中的其他主机。

   此过程中任一系统服务虚拟机迁移失败或关机失败，则进入维护模式任务失败，需要重新进入维护模式。
2. 系统再次检查块存储集群是否存在数据恢复，如存在，待数据恢复完成后主机再继续进入维护模式；如不存在，则直接进入维护模式。

**主机处于维护模式**：任务中心提示进入维护模式成功或主机状态更新为`维护模式`后，您可以对主机进行离线升级或运维操作。

- 三副本数据的异常副本位于该主机，且其他主机上仍有两个健康副本时，系统不会触发数据恢复。
- 两副本数据的异常副本或纠删码的异常分片位于该主机时，系统将在极短时间内自动触发数据恢复。
- 主机处于维护模式 7 天后，系统将自动开始恢复主机上的冷数据。

**退出维护模式**：系统进行退出检查，主机符合要求才允许退出维护模式。您可以选择在退出维护模式的同时将进入维护模式前自动迁出的系统服务虚拟机迁回当前主机。

---

## 节点运维 > 设置维护模式 > 进入维护模式

# 进入维护模式

系统通过预检查，确认块存储集群和主机的状态满足进入维护模式的条件后，才允许主机进入维护模式。

**操作步骤**

1. 在 CloudTower 的主机列表单击目标主机右侧的 **...** 后，选择 **进入维护模式**。
2. 在弹出的**进入维护模式**对话框中，系统将执行如下预检查。部分检查结果不满足要求时，请参照操作建议手动调整，然后再次尝试进入维护模式。

   | 预检查要求 | 检查项不符合要求时的操作建议 |
   | --- | --- |
   | 当前主机不存在只有 1 个副本的数据。 | - 调整副本策略。 - 等待完成数据恢复。 |
   | 当前主机的存储网络连接正常。 | 修复故障。 |
   | 集群中不存在主机处于`进入维护模式中`或`维护模式`状态。 | 等待其他主机完成维护任务并退出维护模式。 |
   | 集群无数据恢复。 | 等待数据恢复完成。 |
   | 集群中其他节点中空闲存储空间充足，即满足如下两个条件： - 集群剩余节点可用存储容量 > 该节点已使用存储容量 - 集群剩余节点可用写缓存容量 > 该节点已使用写缓存容量 | - 扩容集群。 - 删除部分快照或虚拟机以释放集群容量。 - 如判断可以在 7 天内完成线下维护的，确认风险后也允许进入维护模式。 |
   | 以下服务运行状态均满足条件： - 除当前节点外，集群的 `zookeeper`、`mongodb` 服务不存在异常； - 集群的其他节点中，存在 `zbs-meta` 服务运行正常的节点； - 如集群中存在冗余策略使用纠删码的 iSCSI Target 或 NVMe Subsystem，除当前节点外，包含健康且非移除中的存储服务的节点数量不少于任一 Target 或 Subsystem 纠删码配置的数据块（K）和校验块（M）数量之和； - 当前节点的 `job-center-worker` 服务运行正常； - 当前节点的 `libvirt` 服务运行正常； | 修复故障。 |
   | 当前主机上不存在无法迁出的系统服务虚拟机。 | 手动调整集群资源，或手动将系统服务虚拟机迁移至其它主机。 |

   > **说明**：
   >
   > 如块存储集群中部署了文件存储集群，且文件控制器位于当前主机，请单击**文件控制器下线**跳转至文件控制器页面，将该文件控制器下线，具体操作请参考《SMTX ZBS 管理指南》[下线文件控制器](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_159)章节。
3. 所有检查项目全部满足要求，单击对话框右下方的**进入维护模式**。

---

## 节点运维 > 设置维护模式 > 退出维护模式

# 退出维护模式

完成离线升级或维护之后，可以将主机退出维护模式。退出前，SMTX ZBS 块存储系统会进行退出检查，确认主机满足退出该模式的条件后，才允许主机退出维护模式。

**操作步骤**

1. 在 CloudTower 的主机列表单击处于维护模式的主机右侧的 **...** 后，选择 **退出维护模式**，或在主机概览页面单击**退出维护模式**。
2. 在弹出的**退出维护模式**对话框中，系统将执行如下检查。部分检查结果不满足要求时，请参照操作建议手动调整主机，然后再次尝试退出维护模式。

   | 检查项目 | 检查项不符合要求时的操作建议 |
   | --- | --- |
   | 以下服务运行状态均满足条件：当前节点的 `job-center-worker`、`zbs-chunk`、`zbs-iscsi-redirectord`、`libvirt`、`elf-vm-monitor` 服务运行正常。 | 修复故障。 |
   | 当前主机的存储网络连接正常。 | 修复故障。 |
3. 所有检查项目全部满足要求时，在对话框中确认是否同时将进入维护模式时迁出的虚拟机迁回、是否将关机的虚拟机开机，然后单击**退出维护模式**。

   > **注意：**
   >
   > 如果在主机维护期间，系统服务虚拟机运行状态、系统服务虚拟机所在主机已经发生变化，退出维护模式时，系统无法自动迁回系统服务虚拟机，请您退出维护模式后手动处理。

**后续操作**

如进入维护模式前下线了文件控制器，退出维护模式后，请将该文件控制器上线，请参考《SMTX ZBS 管理指南》[上线文件控制器](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_160)章节。

---

## 节点运维 > 关闭节点

# 关闭节点

您可以在 CloudTower 上便捷地关闭 SMTX ZBS 块存储集群的节点。

更换硬件时，例如更换内存、网卡、CPU、存储控制器等，请将节点进入维护模式然后使用此功能关闭节点后进行线下维护操作。如遇需要紧急关闭节点的情况，可以在非维护模式下强制关闭。

同一集群内，同一时间仅允许进行一个关闭节点的任务。

**风险提示**

- 未设置节点进入维护模式或者在节点正在进入维护模式的状态下强制关闭节点，将造成大量数据恢复。
- 如部署了文件存储集群，关闭 2 个及以上文件控制器所在的块存储集群节点，可能会造成文件存储集群及其提供的文件存储服务不可用。

**前提条件**

- CloudTower 虚拟机没有运行在当前节点。
- 当前节点处于`健康`、`亚健康`、`初始化`或`出错`状态。
- 当前节点关闭后，所在块存储集群中的剩余节点满足选举主节点的数量要求。
- 所在块存储集群未使用当前节点的管理 IP 来关联 CloudTower。
- 当前节点处于维护模式。

  若节点未处于维护模式时强制关闭，请确保满足以下条件：

  - 如集群中存在冗余策略使用纠删码的 iSCSI Target 或 NVMe Subsystem，除当前节点外，所在集群中包含健康且非移除中的存储服务的节点数量不少于 Target 或 Subsystem 纠删码配置的数据块数量（K）。
  - 集群中其他节点中空闲存储空间充足，即集群剩余节点可用存储容量 > 该节点已使用存储容量 + 集群剩余节点可用写缓存容量 > 该节点已使用写缓存容量。
  - 当前节点中不存在只有 1 个副本的数据。

**注意事项**

若块存储集群开启静态数据加密，节点关闭后，缓存的密钥会丢失，启动后将重新缓存。

**操作步骤**

1. 登录 CloudTower，在集群界面的主机列表中单击目标节点右侧的 **...** 后选择**关机**。
2. 在弹出的对话框中输入原因，单击**关机**。

---

## 节点运维 > 重启节点

# 重启节点

您可以在 CloudTower 上便捷地重启 SMTX ZBS 块存储集群的节点。

修改配置时，请使节点进入维护模式后使用此功能重启节点使配置生效。如遇需要紧急重启主机的情况，可以在非维护模式下强制重启。

同一集群内，同一时间仅允许进行一个重启节点的任务。

**风险提示**

未设置节点进入维护模式或者在节点正在进入维护模式的状态下强制重启节点，将造成大量数据恢复。

**前提条件**

- CloudTower 虚拟机没有运行在当前节点。
- 当前节点处于`健康`、`亚健康`、`初始化`或`出错`状态。
- 当前节点重启后，所在块存储集群中的剩余节点满足选举主节点的数量要求。
- 所在块存储集群未使用当前节点的管理 IP 来关联 CloudTower。
- 当前节点处于维护模式。

  若节点未处于维护模式时强制重启，请确保满足以下条件：

  - 如集群中存在冗余策略使用纠删码的 iSCSI Target 或 NVMe Subsystem，除当前节点外，所在集群中包含健康且非移除中的存储服务的节点数量不少于 Target 或 Subsystem 纠删码配置的数据块数量（K）。
  - 集群中其他节点中空闲存储空间充足，即集群剩余节点可用存储容量 > 该节点已使用存储容量 + 集群剩余节点可用写缓存容量 > 该节点已使用写缓存容量。
  - 当前节点中不存在只有 1 个副本的数据。

**注意事项**

若块存储集群开启静态数据加密，节点重启后，缓存的密钥会丢失，启动后将重新缓存。

**操作步骤**

1. 登录 CloudTower，在集群界面的主机列表中单击目标节点右侧的 **...** 后选择**重启**。
2. 在弹出的对话框中输入原因，单击**重启**。

---

## 节点运维 > 添加节点

# 添加节点

当计算或存储资源不足时，可以通过在线添加新节点的方式实现块存储集群的扩容。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 集群添加节点 > 准备工作

# 准备工作

- SMTX ZBS 采用存储容量授权模式，且仅企业版许可支持全闪配置节点。在块存储集群扩容前，请根据新添加节点的存储配置和扩容后的总存储容量，提前向 SmartX 申请相应的 SMTX ZBS 软件许可。
- 参考《SMTX ZBS 安装部署指南》的[硬件要求](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_06)章节，确认待添加节点的硬件配置满足要求。
- 确认当前集群的服务器 CPU 架构、已安装的块存储软件版本和主机操作系统类型，为待添加的节点提前准备好对应版本的块存储安装映像文件。
- 为待添加的节点规划 3 个 IP：块存储集群管理 IP、块存储集群存储 IP、块存储集群接入 IP，分别用于管理网络、存储网络和接入网络，同时记录三个网络的子网掩码、网关等信息。若现有的 SMTX ZBS 集成硬件管理能力，还需为该节点规划 IPMI 管理台 IP。

  新节点的 IP 地址规划遵循以下规则：

  - 新添加节点与现有块存储集群的节点的存储网络属于同一子网。
  - 新添加节点的块存储集群管理 IP、存储 IP 和接入 IP 不能分配在同一网段。
  - 新添加节点与现有集群节点的块存储集群管理 IP 之间需要分配在同一网段。
  - 新添加节点与现有集群节点的块存储集群存储 IP 之间、块存储集群管理 IP 之间以及块存储集群接入 IP 之间可正常连通。
  - IP 地址不能与以下 CIDR 范围内的任何 IP 地址重叠：

    - 169.254.0.0/16
    - 240.0.0.0/4
    - 224.0.0.0/4
    - 198.18.0.0/15
    - 127.0.0.0/8
    - 0.0.0.0/8
  > **说明：**
  >
  > 现有块存储集群节点的 IP 地址配置可以通过登录 CloudTower，在左侧导航栏中选中集群的某个主机后，在右侧弹出的主机概览界面中进行查看。
- 如果待扩容块存储集群启用了 Boost 模式、RDMA 功能、NVMe-oF 功能或常驻缓存模式，请确认待添加的节点的软硬件配置满足《SMTX ZBS 块存储特性说明》中启用对应功能的配置要求。
- 块存储集群支持标准容量规格、大容量规格和加大容量规格，集群内所有主机的规格必须相同。请提前确认待扩容集群内的主机规格，确保添加的主机规格与其一致。
- 如果待扩容块存储集群为单一类型 SSD 全闪配置，请确认待添加主机也为单一类型 SSD 全闪配置。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 集群添加节点 > 安装块存储软件

# 安装块存储软件

参考《SMTX ZBS 安装部署指南》文档中的[在物理服务器上安装 SMTX ZBS 块存储](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_23)章节，在待添加节点所在的物理服务器上安装块存储软件。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 集群添加节点 > 检查并设置扩容的环境

# 检查并设置扩容的环境

登录待添加节点的 SMTX ZBS 块存储系统，参考《SMTX ZBS 安装部署指南》文档中的[检查并配置网络环境](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_33)章节，针对待添加节点设置网络环境。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 集群添加节点 > 添加主机

# 添加主机

**注意事项**

- 为待扩容块存储集群添加主机时，仅需要对待添加节点进行以下操作。
- 集群级别的设置可自动从待扩容集群获取，无需重复设置。

**操作步骤**

1. 登录 CloudTower，在左侧导航栏中选中待扩容的块存储集群，进入**概览**界面。在界面右上方选择 **+ 创建** > **添加主机**，进入**添加主机**对话框。用户可以选择手动发现主机，或者通过自动扫描来发现主机。

   - **手动发现主机**

     在**主机地址**输入框中输入待添加主机的 IP 或 MAC 地址，单击**添加**可添加多个主机地址，单击**发现主机**按钮进行主机发现。

     ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_002.png)
   - **自动扫描主机**

     用户也可以单击**自动扫描**来发现主机，扫描完成后若发现当前网络中存在未添加的主机，界面将显示待添加主机的主机名、IP 地址或 MAC 地址。鼠标悬浮在右侧图标上时，将会显示对应的物理盘和网口信息。

     ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_003.png)

     扫描结束后，若系统在当前网络中尚未发现待添加的主机，则系统将给出提示，请尝试**重新扫描**或**手动发现**主机进行重新搜索发现。
2. 勾选待添加的主机，单击**下一步**。
3. 在**配置主机**界面，输入待添加节点的主机名称。
4. 为虚拟分布式交换机关联物理网口。

   - 如果虚拟分布式交换机仅关联一种网络，如下图，请给待添加节点选择用于该网络的物理网口。

     ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_040.png)

     - 可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网口。当接入该网络的物理交换机启用了 LACP 动态链路聚合时，需要选择两个网口进行网口绑定。
     - 如果关联的网络为存储网络，当待扩容块存储集群启用 RDMA 功能时，若选择了多个网口，还需确认所选的网口均来自支持 RDMA 功能的网卡。
     - 如果关联的网络为接入网络，当待扩容块存储集群启用 NVMe over TCP 和 RDMA 功能时，若选择了多个网口，还需确认所选的网口来自同一张支持 NVMe over RDMA 功能的网卡。
   - 如果虚拟分布式交换机关联了多种网络，如下图，请给待添加节点选择这些网络共用的物理网口。

     ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_039.png)

     可以根据显示的网口速率、连接状态和 MAC 地址等判断合适的网口。当接入这些网络的物理交换机启用了 LACP 动态链路聚合时，需要选择两个网口进行网口绑定。
5. 填写为待添加节点实际规划的管理 IP、存储 IP 和接入 IP。

   ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_041.png)
6. （可选）填写 IPMI IP 信息，及其用户名和密码。
7. （可选）为待添加节点配置物理盘池。当待添加节点满足多物理盘池的配置要求时，系统会根据节点的存储配置自动选择推荐的物理盘池数量，并分配物理盘及用途，您也可以手动修改物理盘池数量，建议不同节点设置相同的物理盘池数量。

   > **注意**：
   >
   > - 单集群最多支持配置 255 个物理盘池。
   > - 存储分层模式下：
   >   - 混闪配置、多种类型 SSD 全闪配置，或单一类型多种属性 SSD 全闪配置，单物理盘池的物理盘数量上限为 64；
   >   - 单一类型且单一属性 SSD 全闪配置，单物理盘池的物理盘数量上限为 32。
   > - 存储不分层模式下：单物理盘池的物理盘数量上限为 32。
   > - 单物理盘池的数据盘总容量上限为 256 TB，缓存盘总容量上限为 51 TB，超过容量上限后，将无法添加主机。
8. （可选）指定物理盘的用途和所属物理盘池。

   - **SMTX 系统盘**：不属于任何物理盘池，不可修改用途。
   - **含元数据分区的缓存盘**和**含元数据分区的数据盘**：不可修改用途，可移至其他物理盘池。
   - **其余物理盘**：

     存储分层模式部署时：

     - 若待添加节点为混闪配置，一般只有当系统判断的物理盘类型有误时，才需要手动修改用途，可将物理盘移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为多种类型 SSD 全闪配置，当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**用途修改为**缓存盘**；其余情况下，只有当系统判断的物理盘类型有误时，才需要手动修改物理盘用途。可将物理盘移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为单一类型且多种属性的 SSD 全闪配置，物理盘默认为**数据盘**，需手动将高性能 SSD 的用途修改为缓存盘；当计划预留常驻缓存比例高于 75% 时，需要手动将所有**数据盘**的用途修改为**缓存盘**。可将物理盘移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为单一类型且单一属性的 SSD 全闪配置，物理盘默认为**数据盘**，无需修改用途，可移至其他物理盘池或选择**不挂载**。

     存储不分层模式部署时：所有物理盘默认为**数据盘**，不可修改用途，可移至其他物理盘池或选择**不挂载**。
9. 为待添加节点统一设置 root 账户和 smartx 账户的密码。
10. 单击**执行部署**，部署主机。

    开始执行部署后，当前界面将展示部署的总体进度。如果关闭当前窗口，您也可以在任务中心查看部署进度，在对应的任务条目右侧单击 **...** > **查看详情**可以返回**执行部署**界面。

    - 如果部署成功，**执行部署**界面将提示已成功添加主机。
    - 如果部署失败，**执行部署**界面将提示部署失败，需根据界面的具体提示进行下一步操作。

      - 如果界面提示集群无法连接新主机，表明是由于网络配置失败导致部署失败，请参考以下步骤重新添加主机。

        ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_046.png)

        1. 通过 IPMI 管理台 IP 访问待添加主机，调整主机的网络配置。
        2. 在待添加节点中执行如下命令清理主机信息并重启部署服务。

           ```
           zbs-deploy-manage clear_deploy_tag
           systemctl restart zbs-deploy-server nginx
           ```
        3. 在**执行部署**界面单击**添加主机**，然后从步骤 1 开始添加主机。
      - 如果界面提示需要清理配置信息，表明网络配置成功，但有其他配置异常导致部署失败，请参考以下步骤重新添加主机。

        1. 在**执行部署**界面单击**查看日志**，根据日志详情定位失败原因，解决问题。
        2. 在**执行部署**界面单击清理，以清理添加主机过程中产生的脏数据。

           ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_047.png)

           开始清理后，当前界面将展示清理进度。如果单击**完成**关闭当前窗口，您也可以在任务中心查看清理进度，在对应的任务条目右侧单击 **...** > **查看详情**可以返回**执行部署**界面。

           > **注意**：
           >
           > 如果未及时执行清理，当该任务涉及的主机中存在已添加或正在添加至集群的主机时，请勿再清理此部分数据。
        3. 清理成功后，在**执行部署**界面单击**添加主机**，然后从步骤 1 开始添加主机。

        ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_048.png)
11. 在 CloudTower 中确认节点添加成功，以及集群运行正常。

    - 主机列表中将新增显示该主机的详细信息，该主机为健康状态。
    - 在集群概览界面中存储容量、主机数量、物理盘个数、CPU 总核数和内存容量均有增加。
    - 在集群概览界面中报警模块未新增严重警告和注意信息。

**后续操作**

在为基于 TencentOS 操作系统的 SMTX ZBS 块存储集群添加完节点后，需要激活新添加主机的操作系统，请联系 SmartX 售后工程师进行激活。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点

# 为 SMTX ZBS 双活集群添加节点

支持为双活集群的优先/次级可用域添加节点，且要求新添加节点与现有双活集群节点的服务器 CPU 架构和 CPU 供应商完全相同。请参考如下步骤进行操作。

> **说明**：
>
> 仅支持添加存储节点，若需要添加主节点，请参考[转换节点角色](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_40)将添加的存储节点转化为主节点。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 准备工作

# 准备工作

在为 SMTX ZBS 双活集群添加节点之前，请按照如下要求提前完成准备工作。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 准备工作 > 新节点的硬件配置准备

# 新节点的硬件配置准备

- 现有 SMTX ZBS 双活集群已完成硬件拓扑配置，即所有主机均已分配机箱和机架。

  若当前集群还未配置硬件拓扑，请参考《SMTX ZBS 管理指南》中的[配置机架拓扑](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_097)章节为主机添加机箱和机架。
- 待添加节点的硬件配置满足《SMTX ZBS 双活集群安装部署指南》中的[硬件要求](/smtxzbs/5.7.0/multiactive_user_guide/zbs_multiactive_user_guide/zbs_multiactive_user_guide_07)。
- SMTX ZBS 双活集群支持标准容量规格、大容量规格、加大容量规格。请确认待添加的节点与集群中使用的最大容量规格一致。
- 如果当前集群为全闪配置且存储介质类型相同，请确认待添加的节点也为全闪配置，并且存储介质类型与当前集群相同。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 准备工作 > 软件准备

# 软件准备

- 提前下载当前集群的主机所安装的 ISO 映像文件，要求 ISO 映像文件的版本、CPU 架构和底层操作系统（CentOS 或 openEuler）与当前集群完全相同，并且必须为敏捷版、标准版或企业版。
- 请提前向 SmartX 申请 SMTX ZBS 软件 License。双活集群需要单独购买双活的许可，请确认软件许可满足要求。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 准备工作 > 为新节点规划 IP

# 为新节点规划 IP

从双活集群的网络拓扑可知，新添加节点需至少规划三个 IP，分别用于管理网络、存储网络和接入网络，同时还需提供子网掩码、网关等信息。若现有的 SMTX ZBS 集成硬件管理能力，还需为该节点规划 IPMI 管理台 IP。

优先/次级可用域的节点 IP 地址规划如下表所示。

| 节点名称 | 网络类型 | IP 地址 | 子网掩码 | 网关 | VLAN ID（可选） |
| --- | --- | --- | --- | --- | --- |
| 优先可用域节点 | 管理网络 | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| 存储网络 | xx.xx.xx.xx | xx.xx.xx.xx | - | xx |
| 接入网络 | xx.xx.xx.xx | xx.xx.xx.xx | - | xx |
| 次级可用域节点 | 管理网络 | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| 存储网络 | xx.xx.xx.xx | xx.xx.xx.xx | - | xx |
| 接入网络 | xx.xx.xx.xx | xx.xx.xx.xx | - | xx |

网络管理员在分配新添加节点的管理 IP、存储 IP 和接入 IP 时，必须遵循以下规则：

- 新添加节点与现有集群节点的存储网络属于同一子网。
- 新添加节点与现有集群的块存储集群管理 IP、块存储集群存储 IP 和块存储集群接入 IP 不能分配在同一网段。
- 新添加节点与现有集群节点的块存储集群存储 IP 之间可以正常通信。
- 新添加节点与现有集群节点的管理 IP 需要分配在同一网段。
- 新添加节点与现有集群节点的块存储集群存储 IP 之间、块存储集群管理 IP 之间以及块存储集群接入 IP 之间可正常连通。
- 上述 IP 地址不能与以下 CIDR 范围内的任何 IP 地址重叠：
  - 169.254.0.0/16
  - 240.0.0.0/4
  - 224.0.0.0/4
  - 198.18.0.0/15
  - 127.0.0.0/8
  - 0.0.0.0/8

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 安装 SMTX ZBS 块存储软件

# 安装 SMTX ZBS 块存储软件

通过浏览器访问待添加节点的 IPMI 管理台 IP，检查 BIOS 设置，挂载块存储安装文件，并远程安装块存储软件。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 安装 SMTX ZBS 块存储软件 > 检查 BIOS 设置

# 检查 BIOS 设置

对于不同品牌的服务器，进入 BIOS 设置界面的方式和 BIOS 设置的检查项目有较大差异，下文分别以戴尔服务器 R750 和浪潮服务器 NF5280M6 为例，介绍在优先/次级可用域的每个节点上检查 BIOS 设置的操作。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 安装 SMTX ZBS 块存储软件 > 检查 BIOS 设置 > 戴尔 Intel x86 服务器

# 戴尔 Intel x86 服务器

请对每个节点执行以下操作。

**操作步骤**

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录该节点的 IPMI 管理台。
2. 登录成功后，找到**虚拟控制台**，单击**启动虚拟控制台**，进入虚拟控制台界面。
3. 在界面顶端单击**启动**，在弹出的**开机控制**窗口中单击 **BIOS 设置**，然后在弹出的**确认启动操作**对话框中单击**是**。
4. 在界面顶端单击**功率**，在弹出的**电源控制**窗口中单击**复位系统（热启动）**，然后在弹出的**确认电源操作**对话框中单击**是**，完成后等待服务器重启。
5. 当服务器进入 **System Setup** 界面时，单击 **System BIOS**，进入 **System BIOS Settings** 界面。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_55.png)
6. 在界面中单击 **Boot Settings**，将 **Boot Mode** 选项设置为 **UEFI**，以提升部署效率。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_51.png)
7. 单击 **Back**，返回 **System BIOS Settings** 界面后，单击 **Processor Settings**，检查并确认 **Virtualization Technology** 选项为 **Enabled**，以确保启用 CPU 的虚拟化特性。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_52.png)
8. 单击 **Back**，返回 **System BIOS Settings** 界面后，单击 **System Profile Settings**，检查并确认 **System Profile** 选项为 **Performance**，以确保关闭电源的节能模式。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_53.png)
9. 检查并确认 **Workload Profile** 选项为 **Virtualization Optimized Performance Profile**，以确保系统针对虚拟化场景优化性能。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_54.png)
10. （可选）若计划将 SMTX ZBS 块存储安装在独立的硬 RAID 1 中，则必须将 RAID 1 虚拟磁盘的写策略设置为 Write Through，下面以 **H730P Mini** RAID 卡为例，描述操作步骤。

    1. 1. 在 **System Setup** 界面单击 **Device Settings**，进入设备设置界面。

       ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_56.png)
    2. 在 **Device Settings** 界面选择 RAID 1 虚拟磁盘对应的存储控制器。

       ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_57.png)
    3. 单击 **Virtual Disk Management**，进入虚拟磁盘管理界面。

       ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_58.png)
    4. 选择所要安装 SMTX ZBS 块存储的 RAID 1 虚拟磁盘。

       ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_59.png)
    5. 选择虚拟磁盘的高级配置选项后，将 **VIRTUAL DISK POLICIES** 中的 **Default Write Cache Policy** 设置为 **Write Through** 策略后，单击 **Apply Changes**。

       ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_60.png)
11. 单击 **Back**，在 **System BIOS Settings** 界面单击 **Finish**，然后在弹出的 **Warning** 对话框中单击 **Yes** 完成设置。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 安装 SMTX ZBS 块存储软件 > 检查 BIOS 设置 > 浪潮 Intel x86 服务器

# 浪潮 Intel x86 服务器

请对每个节点执行以下操作。

**操作步骤**

1. 打开浏览器，在浏览器的地址栏输入节点的 IPMI 管理台 IP，登录该节点的 BMC 控制器。
2. 登录成功后，在左侧导航栏或**快速启动任务**区域单击**远程控制**，然后选择远程控制模式，以选择“H5Viewer”为例，请单击**启动 H5Viewer**。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_19.png)

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_01.png)
3. 在弹出的控制台界面中，单击**电源** > **设置启动选项**，在弹出的窗口中，将**设置启动选项**选项设置为 **bios 设置**，并勾选**仅限下一引导**复选框以避免影响后续使用，完成后单击**应用**。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_02.png)

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_03.png)
4. 在控制台界面中单击**电源** > **强制关机再开机**，再在弹出的对话框中单击**确定**，然后等待服务器重启。
5. 当服务器进入以下界面时，按“Del”键，稍后服务器将进入 BIOS 设置界面。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_04.png)
6. 在 BIOS 设置界面中，如下，单击 **Socket Configuration**，再单击 **Advanced Power Management Configuration**，然后请按下述步骤进行操作。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_05.png)

   1. 检查并确保 **Power/Performance Profile** 选项为 **Custom**。

      ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_06.png)
   2. 单击 **CPU P state Control**，然后按下图检查所有参数的设置，其中 **CPU Core Flex Ratio** 无需修改，保持默认值即可。

      ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_07.png)
   3. 按“ESC”键，返回 **Advanced Power Management Configuration** 界面后，单击 **Hardware PM State Control**，然后按下图检查所有参数的设置。

      ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_08.png)
   4. 按“ESC”键，返回 **Advanced Power Management Configuration** 界面后，单击 **CPU C state Control**，然后按下图检查所有参数的设置。

      ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_09.png)
   5. 按“ESC”键，返回 **Advanced Power Management Configuration** 界面后，单击 **Package C state Control**，然后按下图检查所有参数的设置。

      ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_10.png)
   6. 按“ESC”键，返回 **Advanced Power Management Configuration** 界面后，单击 **CPU - Advanced PM Tuning**，再单击 **Energy Perf BIAS**，然后按下图检查所有参数的设置。

      ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_11.png)
7. 按“ESC”键，返回至 **Socket Configuration** 页面后，单击 **Processor Configuration**，然后按下图检查所有参数的设置。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_12.png)

   其中需要确认 **VMX** 选项为 **Enabled**，如下图所示：

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_28.png)
8. 按“ESC”键，返回至 **Socket Configuration** 页面后，单击 **Uncore Configuration**，再单击 **Uncore General Configuration**，然后按下图检查所有参数的设置。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_13.png)

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_14.png)
9. 按“ESC”键，返回至 **Socket Configuration** 页面后，单击 **IIO Configuration**，再单击 **Intel VT for Directed I/O (VT-d)**，然后按下图检查所有参数的设置。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_15.png)
10. 按“ESC”键，返回至 **Socket Configuration** 或 **Advanced** 页面后，切换至 **Save & Exit** 页面，单击 **Save Changes and Exit**，在弹出的对话框中，单击 **Yes** 完成设置。

    ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_18.png)
11. （可选）若计划将 SMTX ZBS 块存储安装在独立的硬 RAID 1 中，则需要将 RAID 1 虚拟磁盘的写策略设置为 write through，请根据实际使用的存储控制器，在 BIOS 或相关配置界面中进行相应设置。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 安装 SMTX ZBS 块存储软件 > 挂载块存储安装文件

# 挂载块存储安装文件

由于不同品牌服务器的 IPMI 界面存在差异，挂载映像文件的操作方式也不同。下文以 Dell 服务器为例，介绍如何挂载 SMTX ZBS 块存储安装文件。

1. 在节点的虚拟控制台界面顶端单击**虚拟介质**，在弹出的**虚拟介质**窗口中，单击**连接虚拟介质**。
2. 在**映射 CD/DVD** 字段后单击**选择文件**，选择 SMTX ZBS 块存储安装文件，完成后单击**映射设备**，再单击**关闭**。
3. 在虚拟控制台界面顶端单击**启动**，在弹出的**开机控制**窗口中，选择**虚拟 CD/DVD/ISO**。
4. 在虚拟控制台界面顶端单击**功率**，在弹出的**电源控制**窗口中，单击**电力循环系统（冷启动）** 或**复位系统（热启动）**，重新启动服务器。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 安装 SMTX ZBS 块存储软件 > 安装块存储安装文件

# 安装块存储安装文件

在优先/次级可用域安装块存储安装文件和在 SMTX ZBS 集群中安装块存储安装文件的操作步骤完全相同。请参考如下步骤完成安装。

> **注意**：
>
> 在步骤 2 中为新添加节点设置容量规格时，需和原集群节点的容量规格保持一致。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 安装 SMTX ZBS 块存储软件 > 安装块存储安装文件 > 将 SMTX ZBS 块存储安装在独立的硬 RAID 1 中

# 将 SMTX ZBS 块存储安装在独立的硬 RAID 1 中

1. 重启服务器后，在如下 SMTX ZBS 块存储的安装引导界面中，选择 **Automatic Installation**。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_41.png)
2. 根据实际规划选择集群节点的容量规格。若选择标准容量规格，请输入字符 1；若选择大容量规格，请输入字符 2；若选择加大容量规格，请输入字符 3。

   若计划为节点配置多个物理盘池，请选择大容量规格或加大容量规格。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_42.png)
3. 选择是否将 SMTX ZBS 块存储安装在两块硬盘上并构建软 RAID 1，请输入 `no`。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_43.png)
4. 系统将自动选择一块硬盘（硬 RAID 1），如果未能找到符合条件的硬盘，或者找到一块以上符合条件的硬盘，请根据[存储设备配置要求](/smtxzbs/5.7.0/zbs_installation_guide/zbs_installation_guide_09)中所规划和记录的 **SMTX 系统盘**，手动输入该盘的盘符。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_46.png)

   选择完硬盘后，SMTX ZBS 块存储将会自动安装，安装所需时间与服务器类型和当前网络条件有关。安装完成后，服务器将自动重启。
5. 服务器重启后，用默认账户 `root` 登录 SMTX ZBS 块存储系统。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 安装 SMTX ZBS 块存储软件 > 安装块存储安装文件 > 将 SMTX ZBS 块存储安装在软 RAID 1 中

# 将 SMTX ZBS 块存储安装在软 RAID 1 中

1. 重启服务器后，在如下 SMTX ZBS 块存储的安装引导界面中，选择 **Automatic Installation**。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_41.png)
2. 根据实际规划选择集群节点的容量规格。若选择标准容量规格，请输入字符 1；若选择大容量规格，请输入字符 2；若选择加大容量规格，请输入字符 3。

   若计划为节点配置多个物理盘池，请选择大容量规格或加大容量规格。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_42.png)
3. 选择是否将 SMTX ZBS 块存储安装在两块硬盘上并构建软 RAID 1，请输入 `yes`。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_43.png)
4. 系统将自动选择一块容量在 7 GiB 至 240 GiB 之间的硬盘作为启动盘，如果找到一块以上符合此条件的硬盘，请根据[存储设备配置要求](/smtxzbs/5.7.0/zbs_installation_guide/zbs_installation_guide_09)中所规划和记录的**启动盘**，手动输入启动盘的盘符。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_44.png)
5. 系统将自动选择两块硬盘（SSD 优先）构成软 RAID 1，若未找到符合条件的硬盘，或者找到两块以上符合此条件的硬盘，请根据[存储设备配置要求](/smtxzbs/5.7.0/zbs_installation_guide/zbs_installation_guide_09)中所规划和记录的**含元数据分区的缓存盘**或**含元数据分区的数据盘**，手动输入该盘的盘符。

   ![](https://cdn.smartx.com/internal-docs/assets/9dd8a4af/zbs_installation_guide_45.png)

   选择完硬盘后，SMTX ZBS 块存储系统将会自动安装，安装所需时间与服务器类型和当前网络条件有关。安装完成后，服务器将自动重启。
6. 服务器重启后，用默认账户 `root` 登录 SMTX ZBS 块存储系统。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 创建 pre_bond 网口

# 创建 pre\_bond 网口

仅当接入 SMTX ZBS 块存储双活集群管理网络的物理交换机启用了 LACP 动态链路聚合时，才需要执行以下操作以创建 pre\_bond 网口；否则请忽略。

1. 使用默认账户 `root` 登录待添加节点的 SMTX ZBS 块存储系统。
2. 使用 `cd /etc/sysconfig/network-scripts/` 命令，进入网口配置文件的访问路径。
3. 使用 `ip a` 命令查看所有网卡的接口信息，再使用 `ethtool <port>` 查看每个网卡接口的速率，以判断出两个用于管理网络的网口，其中 `<port>` 表示实际网口的名称。

   - 当管理网络独占一个虚拟分布式交换机时，**Speed** 显示 1000 Mb/s 及以上的网口可以作为用于管理网络的网口。
   - 当管理网络与其他网络共用一个虚拟分布式交换机时，**Speed** 显示 10000 Mb/s 及以上的网口可以作为用于管理网络与其他网络共用的网口。
4. 在网口配置文件路径下执行以下命令，将两个用于管理网络的网口绑定为一个网口（名称为 `pre_bond`），并生成 ifcfg-pre\_bond 网口配置文件。

   ```
   network-preconfig create-lacp --nics <nics>
   ```

   其中，`<nics>` 表示需要绑定的网口名称，网口名称之间需用空格隔开，且名称外侧需加引号（"）。例如，当需要绑定网口 eth0 和 eth1 时，则执行 `network-preconfig create-lacp --nics "eth0 eth1"`。

   当输出以下信息时，表明 pre\_bond 网口创建成功。

   ```
   create lacp bond port success
   ```

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 创建 VLAN 子接口

# 创建 VLAN 子接口

仅当物理交换机为管理网络配置了 VLAN 时，才需要执行以下操作以创建 VLAN 子接口；否则请忽略。

1. 用默认账户 `root` 登录待添加节点的 SMTX ZBS 块存储系统。
2. 使用 `cd /etc/sysconfig/network-scripts/` 命令，进入网口配置文件的访问路径。
3. 使用 `ip a` 命令查看所有网卡的接口信息，再使用 `ethtool <port>` 查看每个网卡接口的速率，以判断并确定用于管理网络的网口，其中 `<port>` 表示实际网口的名称。

   - 当管理网络独占一个虚拟分布式交换机时，**Speed** 显示 1000 Mb/s 及以上的网口可以作为用于管理网络的网口。
   - 当管理网络与其他网络共用一个虚拟分布式交换机时，**Speed** 显示 10000 Mb/s 及以上的网口可以作为用于管理网络与其他网络共用的网口。
4. 在网口配置文件路径下执行以下命令，为网口创建 VLAN 子接口，并配置 IP、网关和子网掩码。

   ```
   network-preconfig create-vlanif --iface <iface> --ipaddr <ipaddr> --netmask <netmask> --gateway <gateway> --vlanid <vlanid>
   ```

   其中，带有`<>`符号的字段表示管理网络的参数。

   | 参数 | 说明 |
   | --- | --- |
   | `iface` | 表示网口名称。 - 若待添加节点用于管理网络的网口为 pre\_bond 网口，请替换为 `pre_bond`。 - 若待添加节点用于管理网络的网口不为 pre\_bond 网口，请替换为实际的网口名称，如 `eth0`。 |
   | `ipaddr` | 表示实际规划的 IP 地址。 |
   | `netmask` | 表示实际规划的子网掩码。 |
   | `gateway` | 表示实际规划的网关。 |
   | `vlanid` | 表示实际规划的 VLAN ID。 |

   当输出以下信息时，表明 VLAN 子接口创建成功。

   ```
   create vlan interface success
   ```

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 为待添加节点设置部署的环境

# 为待添加节点设置部署的环境

请参考《SMTX ZBS 块存储双活集群安装部署指南》文档中的[为优先/次级可用域节点设置部署的环境](/smtxzbs/5.7.0/multiactive_user_guide/zbs_multiactive_user_guide/zbs_multiactive_user_guide_27)进行操作。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 为可用域添加节点

# 为可用域添加节点

为双活集群的可用域添加节点时，仅需要对待添加的所有主机进行以下操作。集群级别的设置可自动从原有集群获取，无需重复设置。

**操作步骤**

1. 登录 CloudTower，在左侧导航栏中选中现有集群，进入**概览**界面。在界面右上方选择 **+ 创建** > **添加主机**，进入**添加主机**对话框。您可以选择手动发现主机，或者通过自动扫描来发现主机。

   - **手动发现主机**

     在**主机地址**输入框中输入待添加主机的 IP 或 MAC 地址，单击**添加**可添加多个主机地址，单击**发现主机**按钮进行主机发现。

     ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_002.png)
   - **自动扫描主机**

     您也可以单击**自动扫描**来发现主机，扫描完成后若发现当前网络中存在未添加的主机，界面将显示待添加主机的主机名、IP 地址或 MAC 地址。鼠标悬浮在右侧图标上时，将会显示对应的物理盘和网口信息。

     ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_003.png)

   扫描结束后，若系统在当前网络中尚未发现待添加的主机,则系统将会给出提示,请尝试**重新扫描**或**手动发现**主机进行重新搜索发现。
2. 勾选待添加的主机，单击**下一步**。
3. 在**配置主机**界面，输入待添加节点的主机名称。
4. （可选）若集群已配置静态路由，则需为待添加节点指定可用域。

   ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_043.png)
5. 为虚拟分布式交换机关联物理网口。请给待添加节点选择用于该网络的物理网口。当接入该网络的物理交换机启用了 LACP 动态链路聚合时，需要选择多个网口进行网口绑定。

   ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_040.png)
6. 填写为新添加节点实际规划的管理 IP、存储 IP 和接入 IP。

   ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_041.png)
7. （可选）填写为新添加节点规划的 IPMI IP 信息，以及用户名和密码。
8. （可选）为待添加节点配置物理盘池。当待添加节点满足多物理盘池的配置要求时，系统会根据节点的存储配置自动选择推荐的物理盘池数量，并分配物理盘及用途，您也可以手动修改物理盘池数量，建议不同节点设置相同的物理盘池数量。

   > **注意**：
   >
   > - 单集群最多支持配置 255 个物理盘池。
   > - 存储分层模式下：
   >   - 混闪配置、多种类型 SSD 全闪配置，或单一类型多种属性 SSD 全闪配置，单物理盘池的物理盘数量上限为 64；
   >   - 单一类型且单一属性 SSD 全闪配置，单物理盘池的物理盘数量上限为 32。
   > - 存储不分层模式下：单物理盘池的物理盘数量上限为 32。
   > - 单物理盘池的数据盘总容量上限为 256 TB，缓存盘总容量上限为 51 TB，超过容量上限后，将无法添加主机。
9. （可选）指定物理盘的用途和所属物理盘池。

   - **SMTX 系统盘**：不属于任何物理盘池，不可修改用途。
   - **含元数据分区的缓存盘**和**含元数据分区的数据盘**：不可修改用途，可移至其他物理盘池。
   - **其余物理盘**：

     存储分层模式部署时：

     - 若待添加节点为混闪配置或多种类型 SSD 全闪配置，一般只有当系统判断的物理盘类型有误时，才需要手动修改用途，可移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为单一类型且多种属性的 SSD 全闪配置，物理盘默认为**数据盘**，需手动将高性能 SSD 的用途修改为缓存盘，可移至其他物理盘池或选择**不挂载**。
     - 若待添加节点为单一类型且单一属性的 SSD 全闪配置，物理盘默认为**数据盘**，无需修改用途，可移至其他物理盘池或选择**不挂载**。

     存储不分层模式部署时：所有物理盘默认为**数据盘**，不可修改用途，可移至其他物理盘池或选择**不挂载**。
10. 为待添加节点统一设置 `root` 账户和 `smartx` 账户的密码。
11. 单击**执行部署**，部署主机。

    开始执行部署后，当前界面将展示部署的总体进度。如果关闭当前窗口，您也可以在任务中心查看部署进度，在对应的任务条目右侧单击 **...** > **查看详情**可以返回**执行部署**界面。

    - 如果部署成功，**执行部署**界面将提示已成功添加主机。
    - 如果部署失败，**执行部署**界面将提示部署失败，需根据界面的具体提示进行下一步操作。

      - 如果界面提示集群无法连接新主机，表明是由于网络配置失败导致部署失败，请参考以下步骤重新添加主机。

        ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_046.png)

        1. 通过 IPMI 管理台 IP 访问待添加主机，调整主机的网络配置。
        2. 在待添加节点中执行如下命令清理主机信息并重启部署服务。

           ```
           zbs-deploy-manage clear_deploy_tag
           systemctl restart zbs-deploy-server nginx
           ```
        3. 在**执行部署**界面单击**添加主机**，然后从步骤 1 开始添加主机。
      - 如果界面提示需要清理配置信息，表明网络配置成功，但有其他配置异常导致部署失败，请参考以下步骤重新添加主机。

        1. 在**执行部署**界面单击**查看日志**，根据日志详情定位失败原因，解决问题。
        2. 在**执行部署**界面单击清理，以清理添加主机过程中产生的脏数据。

           ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_047.png)

           开始清理后，当前界面将展示清理进度。如果单击**完成**关闭当前窗口，您也可以在任务中心查看清理进度，在对应的任务条目右侧单击 **...** > **查看详情**可以返回**执行部署**界面。

           > **注意**：
           >
           > 如果未及时执行清理，当该任务涉及的主机中存在已添加或正在添加至集群的主机时，请勿再清理此部分数据。
        3. 清理成功后，在**执行部署**界面单击**添加主机**，然后从步骤 1 开始添加主机。

        ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_048.png)
12. 在 CloudTower 中确认集群的所有节点添加成功，以及集群运行正常。

    - 主机列表中将新增显示新添加的所有主机的详细信息，且均显示为健康状态。
    - 在集群概览界面中存储容量、主机数量、物理盘个数、CPU 总核数和内存容量均有增加。
    - 在集群概览界面中报警模块未新增严重警告和注意信息。

---

## 节点运维 > 添加节点 > 为 SMTX ZBS 双活集群添加节点 > 配置机架拓扑

# 配置机架拓扑

为双活集群添加节点后，需要在机架拓扑中将新添加节点放置到正确位置，否则会出现主机未配置拓扑信息的报警。请参考《SMTX ZBS 管理指南》文档中的[在机箱添加主机](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_097#%E5%9C%A8%E6%9C%BA%E7%AE%B1%E4%B8%AD%E6%B7%BB%E5%8A%A0%E4%B8%BB%E6%9C%BA)进行操作。

---

## 节点运维 > 移除节点

# 移除节点

当块存储集群和双活集群的可用域中的节点发生不可修复的故障需要被彻底移除时，或运维人员需要替换服务器、腾挪节点时，可以在 CloudTower 界面上安全高效地移除节点。

本小节操作仅适用于满足以下条件的集群：

- 块存储集群和双活集群的可用域。若双活集群的仲裁节点发生异常需要移除，请联系售后工程师重建双活集群仲裁节点。
- 集群中健康节点数量大于 3 的场景下移除存储节点。其中，对于 SMTX ZBS 双活集群，要求移除节点后，优先可用域至少有 2 个健康节点，次级可用域至少有 1 个健康节点。否则，请您进行[节点替换](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_92)。

**风险提示**

从集群中移除节点将删除该节点上存储的数据，且该操作无法撤回，请谨慎操作。

**注意事项**

- 移除当前节点后，如计划添加新节点进行替换重建，请记录当前节点的主机名和网络配置信息，届时为新节点添加相同的配置。
- 移除无响应节点后，请勿开启该节点。若此节点还需用作其他用途，请重装系统后再开机。

**操作步骤**

1. 在 CloudTower 的主机列表单击目标节点右侧的 **...** 后，选择**移除主机**。
2. 在弹出的**移除主机**对话框中，系统将执行如下一系列的预检查。部分检查结果不满足要求时，请参照操作建议手动调整，然后单击**重新检查**再次尝试移除。

   | 预检查要求 | 检查项不符合要求时的操作建议 |
   | --- | --- |
   | 当前主机处于`无响应`、`维护模式`状态。 | 设置主机进入维护模式，或将主机关机。 |
   | 移除当前主机后，集群中包含健康且非移除中的存储服务的主机数量不少于任⼀ iSCSI Target 或 NVMe Subsystem 纠删码配置的数据块（K）和校验块（M）数量之和。 | 移除主机会造成数据丢失，不允许移除主机。 |
   | 当前主机上是否无系统服务虚拟机。 | 如果系统服务虚拟机如文件控制器位于当前主机，请联系售后工程师将文件控制器下线并迁移至其他主机。 |
   | 当前主机是存储节点。 | 将主机转换为存储节点。 |
   | 集群中主节点数量满足要求。 | 不满足要求则不允许移除主机。 |
   | 集群 ZooKeeper 及 MongoDB 服务正常运行 | 修复故障。 |
   | 集群中其他主机的所有存储服务均不处于 `REMOVING` 或 `IDLE` 状态。 | 等待其他主机的存储服务恢复健康。 |
   | 集群中其他主机的空闲存储空间充足。 | 扩容集群，或删除部分快照或虚拟机以释放集群容量。 |
   | 集群中不存在如下状态的其他主机： - 正在添加的主机； - 正在进入维护模式； - 处于维护模式中； - 正在移除； - 移除失败； - 正在转换角色； - 角色转换失败。 | 等待主机完成当前进行中的任务，并结束当前的状态。 |
   | 集群中不存在数据恢复。 | 等待数据恢复完成。 |
   | 集群中不存在 dead pextent。 | 联系售后工程师恢复集群数据。 |
   | 集群不处于`升级中`状态。 | 等待集群升级完成。 |
   | （仅双活集群）仲裁节点处于`健康`状态。 | 恢复仲裁节点。 |
   | （仅双活集群）移除当前主机后，优先可用域中至少有 2 个健康的主机，次级可用域中至少有 1 个健康的主机。 | 恢复非健康状态的主机并进行集群扩容。 |
3. 所有检查项目全部满足要求，在**我确认删除**后的输入框中输入待移除节点的名称，然后单击对话框右下方的**移除**。

   提交移除主机任务后，页面将展示任务进度以及是否移除成功。如果移除失败，请选择**重新移除主机**，再次提交移除主机任务。

---

## 节点运维 > 转换节点角色

# 转换节点角色

节点角色包含主节点和存储节点。主节点和存储节点的详细说明请参考《SMTX ZBS 故障场景说明》[节点类型](/smtxzbs/5.7.0/zbs_failure_scenario_guide/zbs_failure_scenario_guide_07)章节。

当节点发生故障或者为了业务负载均衡等情况下需要腾挪节点时，您可以在 CloudTower 界面上高效地将主节点转换为存储节点，或将存储节点转换为主节点。

**操作步骤**

1. 在 CloudTower 的主机列表单击目标节点右侧的 **...** 后，选择**转换角色**。
2. 在弹出的**转换角色**对话框中，系统将执行一系列的预检查。部分检查结果不满足要求时，请参照操作建议手动调整，然后单击**重新检查**再次尝试转换。

   - **`主节点`转换为`存储节点`**

     | 预检查要求 | 检查项不符合要求时的操作建议 |
     | --- | --- |
     | 集群中全部主机都处于`健康`或`无响应`状态。 | 请恢复主机状态为健康。 |
     | 当前主机转换角色后，集群中健康的主节点数量满足要求： - `健康`状态的主节点转换角色后，集群中健康的主节点数量应 ≥ 3 且 ≤ 5。 - `无响应`状态的主节点转换角色后，集群中健康的主节点数量应 ≥ 2 且 ≤ 5。 | 如果存在不健康的主节点，请恢复主机状态为健康状态；如果主节点均为健康状态且不满足数量要求，不允许转换角色。 |
     | 集群 ZooKeeper 及 MongoDB 服务正常运行。 | 修复故障。 |
     | 集群中不存在数据恢复。 | 等待数据恢复完成。 |
     | 集群中不存在如下状态的其他主机： - 正在添加的主机； - 正在进入维护模式； - 处于维护模式中； - 正在移除； - 移除失败； - 正在转换角色； - 角色转换失败。 | 等待主机完成当前进行中的任务，并结束当前的状态。 |
     | 集群不处于`升级中`状态。 | 等待集群升级完成。 |
     | （仅双活集群）仲裁节点处于`健康`状态。 | 恢复仲裁节点。 |
   - **`存储节点`转换为`主节点`**

     | 预检查要求 | 检查项不符合要求时的操作建议 |
     | --- | --- |
     | 集群中全部主机都处于`健康`状态，且当前主机未处于`维护模式`状态。 | 如果当前主机处于维护模式，请将其退出维护模式；如果有主机不处于健康状态，请恢复主机状态为健康。 |
     | 当前主机转换角色后，集群中健康的主节点数量应 ≥ 3 且 ≤ 5。 | 如果存在不健康的主节点，请恢复主机状态为健康；如果主节点均为健康状态且不满足数量要求，不允许转换角色。 |
     | 集群 ZooKeeper 及 MongoDB 服务正常运行。 | 修复故障。 |
     | 集群中不存在数据恢复。 | 等待数据恢复完成。 |
     | 集群中不存在如下状态的其他主机： - 正在添加的主机； - 正在进入维护模式； - 处于维护模式中； - 正在移除； - 移除失败； - 正在转换角色； - 角色转换失败。 | 等待主机完成当前进行中的任务，并结束当前的状态。 |
     | 集群不处于`升级中`状态。 | 等待集群升级完成。 |
     | （仅双活集群）仲裁节点处于`健康`状态。 | 恢复仲裁节点。 |
3. 所有检查项目全部满足要求，单击对话框右下方的**转换**。

   提交转换节点角色任务后，页面将展示任务进度以及是否转换成功。如果转换失败，请选择**重新转换角色**，再次提交转换节点角色任务。

---

## 节点运维 > 替换节点

# 替换节点

SMTX ZBS 块存储集群中节点发生故障时，可以参照本节内容用新节点替换故障节点，无需等待数据迁移，替换后新节点的数据将与原故障节点保持一致。

**准备工作**

- 记录故障节点的主机名、网络配置信息和物理盘用途。
- 将故障节点上的所有虚拟机迁移至其他节点。
- 确认新节点的硬件配置满足要求，请参考《SMTX ZBS 安装部署指南》的[硬件要求](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_06)章节。
- 在新节点上安装该版本的 SMTX ZBS 软件，请参考《SMTX ZBS 安装部署指南》的[在物理服务器上安装 SMTX ZBS 块存储](/smtxzbs/5.7.0/zbs_installation_guide_INTERNAL_EXTERNAL/zbs_installation_guide/zbs_installation_guide_23)章节。

**操作步骤**

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
   - 故障节点中存在未处于`无响应`状态的节点，请在 CloudTower [关闭](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_09)该节点。如果通过 CloudTower 关机失败，可以通过 IPMI 控制或关闭服务器电源使节点处于`无响应`状态。
4. 逐一移除所有故障节点。在集群中除故障节点外的任一节点中执行如下命令，请确保同一时间只有一个节点正在被移除。

   ```
   zbs-deploy-manage meta_remove_node [--offline_host_ips <offline_host_ips>] --keep_zbs_meta <data_ip>
   ```

   - `[--offline_host_ips <offline_host_ips>]`：可选项。故障节点处于无响应状态时需要填写此参数，其中 `<offline_host_ips>` 表示此时集群中所有无响应状态节点的存储 IP，多个存储 IP 之间请使用半角逗号“,”分隔。
   - `<data_ip>`：表示故障节点的存储 IP。
5. 将新节点添加至集群，请参考[添加主机](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_33)章节。新节点的主机名和网络配置信息请按照此前记录的故障节点配置信息进行填写；物理盘用途可参考故障节点配置，也可根据实际情况填写。
6. 如果此前移除的故障节点是主节点，需要将新节点从存储节点转换为主节点，请参考[转换节点角色](/smtxzbs/5.7.0/zbs_operation_maintenance/zbs_operation_maintenance_40)章节。
7. 按需将迁移走的虚拟机迁移至新节点。

---

## 集群运维 > 更新软件许可码

# 更新软件许可码

在如下情况中，需要更新集群许可：

- 首次安装部署块存储集群之后，从试用许可更新为永久许可或订阅许可;
- 当前许可容量不再满足需要;
- 版本升级，例如从标准版升级为企业版;
- 延长试用许可或订阅许可有效期。

更新许可时，需将所有当前软件许可信息提供给 SmartX 客户经理，在完成商务流程后，客户经理将提供新的许可码。

**更新步骤**

1. 将许可码粘贴在**更新许可**中的**新许可码**处。
2. 单击输入框外部的空白区域，载入新许可信息。
3. 确认无误后，单击**更新**完成许可更新。

> **注意**：
>
> 许可过期对文件存储集群的影响如下：
>
> - 如原本未部署文件存储集群，则不允许部署；
> - 对于已部署的文件存储集群：
>   - 试用许可过期后该文件存储集群将处于`异常`状态；
>   - 订阅许可过期后该文件存储集群将无法增加文件控制器数量，此时创建出来的文件系统将处于`已下线`状态。

---

## 集群运维 > 更新 NTP 服务器

# 更新 NTP 服务器

NTP 服务器在部署块存储集群时进行过初始设置，如有需要，可以在 CloudTower 中修改设置。

**风险提示**

修改 NTP 服务器的配置会影响集群的可用性，请谨慎操作。

**注意事项**

- 从使用外部 NTP 服务器切换至使用集群内主机作为 NTP 服务器后，无法立即执行其他节点与 NTP Leader 节点的时钟同步，请等待大约 7 分钟再执行操作。
- 如果 CloudTower 配置了 NTP 服务器，请确保集群的 NTP 服务器与 CloudTower 的 NTP 服务器的时钟保持同步。

**操作步骤**

1. 进入集群的管理界面，单击**设置**，选择**集群时间**。
2. 选择 NTP 服务器。

   - **使用集群外部 NTP 服务器**

     设置外部 NTP 服务器 IP，多个服务器地址使用半角逗号“,”分隔。需确保集群所有主机都可以访问该服务器，以保证时间同步。
   - **使用集群内主机作为 NTP 服务器**

     集群中运行 Zookeeper 的某台主机将会被设置为 NTP 服务器，其他主机与其保持同步。初始时间与浏览器时间一致。
3. 单击**保存**，完成修改。

---

## 集群运维 > 调整块存储集群系统时间

# 调整块存储集群系统时间

当用户修改块存储集群的 NTP 服务器配置后，例如在使用外部 NTP 服务器和使用内部主机作为 NTP 服务器两个模式间切换时，可能导致集群里某些节点的系统时间不准确，此时需要使用相关命令进行修正，确保集群里所有节点的系统时间保持一致。

**适用场景**

以下操作方法适用于块存储群的某些节点系统时间不准确时的场景。

如果块存储集群使用内部主机作为 NTP 服务器，并且所有节点的系统时间与实际时间均保持一致，此时若用户仍然希望调整集群的时间，则可以通过 `zbs-cluster sync_internal_leader_to_normal --time <time_string>` 命令进行调整，其参数的格式可参考[集群中 NTP Leader 的系统时间不准确](#%E9%9B%86%E7%BE%A4%E4%B8%AD-ntp-leader-%E8%8A%82%E7%82%B9%E7%9A%84%E7%B3%BB%E7%BB%9F%E6%97%B6%E9%97%B4%E4%B8%8D%E5%87%86%E7%A1%AE)的描述。

**注意事项**

prometheus 服务无法保存早于当前系统时间的数据，因此当调整后的系统时间比当前显示的系统时间更早时，prometheus 将无法更新两段时间之间的数据。

**准备工作**

登录块存储集群的任一节点，执行 `ntpm source show` 命令，查看集群的 NTP 配置，确定集群是以内部主机还是外部主机作为其 NTP 服务器。

在系统输出的结果中，通过 **NTP SERVER** 列获取集群所配置的 NTP 服务器的 IP 地址，**TYPE** 列表示 NTP 服务器类型。

- 若输出结果的 **TYPE** 列只包含 `internal`，并且 **NTP SERVER** 显示为集群内某个节点的存储 IP，则表示该集群以内部主机作为其 NTP 服务器。

  ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_049.png)
- 若输出结果的 **TYPE** 列包含 `external`，则表示该集群配置外部主机作为其 NTP 服务器。

  ![](https://cdn.smartx.com/internal-docs/assets/4f00ff92/zbs_operation_maintenance_050.png)

## 集群使用外部 NTP 服务器

**前提条件**

用户需要确保块存储集群使用的外部 NTP 服务器的系统时间准确。

**操作步骤**

在块存储集群中任一节点执行如下命令，将集群的所有节点与外部 NTP 服务器进行时钟同步。

`zbs-cluster sync_time`

## 集群使用内部主机作为 NTP 服务器

**调整集群系统时间的原则**

由于块存储集群中其他节点与 NTP Leader 节点的系统时间差不超过 10 分钟时，其他节点将会自动调整，保持与 Leader 节点的时间同步。因此，我们调整集群的系统时间原则为：确保集群中所有节点的系统时间差不超过 10 分钟。

### 集群中 NTP Leader 节点的系统时间准确

当块存储集群中 NTP Leader 的系统时间与实际时间一致，但集群中某些节点与 NTP Leader 的时间差超过 10 分钟，且无法自动同步时，需要在这类节点上逐一执行以下命令，手动调整这些节点的系统时间与 NTP Leader 的时间同步。

`zbs-node sync_time`

### 集群中 NTP Leader 节点的系统时间不准确

当块存储集群中 NTP Leader 的系统时间与实际时间不一致时，通过在集群任一节点执行以下命令，可以将集群内所有节点的系统时间同步为正确时间。

`zbs-cluster sync_internal_leader_to_normal --time <time_string>`

> **说明**：
>
> - 参数 **time\_string** 的格式与 `date --set="time_str"` 命令中的 **time\_str** 的格式保持一致。

举例，在块存储集群任一节点执行以下命令：

```
zbs-cluster sync_internal_leader_to_normal --time "+600 second"

zbs-cluster sync_internal_leader_to_normal --time "-600 second"
```

其中 **+600 seconds** 表示将所有节点的系统时间向前调整 600 秒，**-600 seconds** 表示将所有节点的系统时间向后调整 600 秒。

如果希望将节点的系统时间调整到具体的时间，比如 19 点 51 分整，则执行如下命令：

```
zbs-cluster sync_internal_leader_to_normal --time "19:51:00"
```

---

## 集群运维 > 配置 SNMP 传输

# 配置 SNMP 传输

SMTX ZBS 块存储支持使用简单网络管理协议（SNMP）和第三方监控报警平台（如 Zabbix）集成，通过创建 SNMP 传输，使得 SNMP 客户端能接收块存储集群监控信息。

**前提条件**

已在其他监控工具中配置了 SNMP。

**操作步骤**

1. 进入集群的管理界面，单击**设置**，选择 **SNMP 传输**。
2. 单击**创建传输**，在弹出的对话框填写如下信息：

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

## 集群运维 > 更新 IPMI 信息

# 更新 IPMI 信息

为主机设置 IPMI 信息后，您可以在 CloudTower 上查看 SMTX Halo 存储一体机的机箱拓扑和电源监控，查看主机的风扇转速和 CPU 温度。

**操作步骤**

1. 您可以在 CloudTower 主页面左侧的导航栏中选择某一集群，在右侧的管理页面选择**设置** > **IPMI 信息**。
2. 编辑主机的 IPMI 信息。密码留空则不更新。

   - 单独编辑：单击**编辑**，设置其中一个主机的 IPMI IP、用户名或密码。
   - 批量编辑：单击**批量编辑**，通过起始 IPMI IP 和统一的用户名及密码设置全部主机的 IPMI 信息。
3. 单击**保存**。提交修改后，若验证失败，会出现相应提示。

---

## 集群运维 > 更新 DNS 服务器

# 更新 DNS 服务器

DNS 服务器在部署块存储集群时进行过初始设置，如有需要，可以在 CloudTower 中修改设置。

**风险提示**

修改 DNS 服务器的配置会影响集群的可用性，请谨慎操作。

**操作步骤**

1. 进入集群的管理界面，单击**设置**，选择 **DNS 服务器**。
2. 输入 DNS 服务器地址。多个服务器地址使用半角逗号“,”分隔。
3. 单击**保存**，完成修改。

---

## 集群运维 > 更新管理虚拟 IP

# 更新管理虚拟 IP

块存储集群的管理虚拟 IP 用于保证集群管理界面的高可用，访问此 IP 时，可以自动通过集群内任一可用的主机管理 IP 访问集群。

**注意事项**

- 必须确保管理虚拟 IP 与节点的块存储集群管理 IP 在同一个子网内，并且 CloudTower 可以通过管理虚拟 IP 访问集群。
- 若块集群中已部署文件存储集群，集群的管理虚拟 IP 不允许为空。

**操作步骤**

1. 在集群的管理界面中，单击**设置**，选择**虚拟 IP**。
2. 修改管理虚拟 IP。
3. 单击**保存**。

---

## 集群运维 > 更新接入虚拟 IP

# 更新接入虚拟 IP

接入虚拟 IP 用于提供 iSCSI 接入服务。计算平台可以通过该虚拟 IP 访问 iSCSI Target 和 LUN。

启用接入虚拟 IP 后，所有的 iSCSI 服务将通过接入虚拟 IP 进行服务重定向至可用的主机。当主机存储服务异常时，iSCSI 服务将自动通过虚拟 IP 所在主机的 iSCSI 重定向服务指向新的可用主机，从而保证了 iSCSI 服务的高可用性。

接入虚拟 IP 仅在接入阶段重定向登录过程，不参与后续的 I/O 处理，无需担心访问集中的可能性。

**注意事项**

直接变更接入虚拟 IP 会导致已挂载的 iSCSI Target 和 LUN 无法访问，不建议经常变更接入虚拟 IP。如必需更新接入虚拟 IP，请在更新前先卸载所有已挂载的 iSCSI Target 和 LUN，待更新后再重新挂载。

**操作步骤**

1. 进入集群的管理界面，单击设置按钮，进入集群的**设置**界面，选择 **虚拟 IP**。
2. 设置接入虚拟 IP。
3. 单击**保存**，完成配置。

---

## 集群运维 > 更新端口访问控制

# 更新端口访问控制

为保障集群中主机的访问安全，您可以查看主机内部服务已使用的端口及其用途，并对 ssh 和 snmp 服务端口配置访问限制。仅允许指定 IP 进行访问，从而实现最小化的访问控制，防止外部网络攻击。

**规则生效顺序**

配置完成后访问控制规则的生效顺序如下：

1. 存储网段内的所有 IP 地址：可以通过任意端口通信。
2. 主机中的其他 IP 地址（如管理 IP、接入 IP 等）：
   - 已配置访问限制的端口：仅允许指定 IP 访问。
   - 未配置访问限制的端口：允许所有 IP 访问。
3. 内部服务未使用的端口：端口关闭，无法访问。

**注意事项**

- 如已在主机上通过 `iptables` 自定义配置安全规则，在启用端口访问控制之前，需要手动清理所有已配置的规则，否则可能由于规则冲突而导致配置不生效。
- 在集群中添加新主机后，为确保集群服务正常运行，请重新编辑存储网段规则，确保新主机的存储 IP 地址在设置的存储网段范围内。新添加的主机默认允许全部 IP 访问该主机的服务端口，您可以按需为该主机的服务端口设置 IP 白名单。

**操作步骤**

1. 在集群管理页面选中某一集群，单击**设置**，选择**端口访问控制**。
2. 在**访问控制**区域启用端口访问限制。

   1. 单击**编辑**。
   2. 启用**访问限制**，并添加**存储网段**，请确保所有主机的存储 IP 均包含在存储网段范围内。
   3. 单击**保存**。
3. 在**服务端口**区域为 snmp 或 ssh 服务端口设置 IP 白名单。

   1. 单击**编辑**。
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

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
