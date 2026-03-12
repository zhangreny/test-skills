---
title: "SMTXOS/6.3.0/SMTX OS CLI 命令参考"
source_url: "https://internal-docs.smartx.com/smtxos/6.3.0/cli_guide/cli_guide_preface_generic"
sections: 109
---

# SMTXOS/6.3.0/SMTX OS CLI 命令参考
## 关于本文档

# 关于本文档

本文档介绍了 SMTX OS（读作 SmartX OS）常见的使用场景及相关命令行。

---

## 文档更新信息

# 文档更新信息

**2026-02-04：配合 SMTX OS 6.3.0 正式发布**

相较于 OS 6.2.0，本版本主要更新如下：

- 新增了“设置网络服务 CPU 模式”、“查询集群可用的时区列表”、“查看集群当前时区设置”、“设置集群时区”、“获取单个物理盘池的常驻缓存信息”、“获取集群所有物理盘池的常驻缓存信息”、“设置单个物理盘池的常驻缓存比例”、“配置回收站”、“查看回收站相关信息”、“从回收站中恢复暂存卷”、“清理回收站中的暂存卷”、“管理业务主机组”、“管理业务主机”、“查看本地 chunk 的全部数据块”、“查看本地 Chunk 的数据链路信息”、“查看 chunk 线程轮询状态”、“查看节点活跃访问的的存储卷”、“查看存储卷数据在缓存分区和数据分区上的分布情况”、“查看指定数据块的所有子数据块”、“迁移指定数据块”、“本地聚集指定虚拟卷”、“清空手动触发的迁移命令”、“查询卸载盘上待迁移数据块的上报配置”、“更新卸载盘上待迁移数据块的上报配置”、“查询卸载盘上的待迁移数据块”、“创建 CDP 任务”、“结束 CDP 任务”、“取消 CDP 任务”、“删除 CDP 任务”、“查看 CDP 任务”、“修改 CDP 任务模式”、“创建同步点快照”、“管理脏页面追踪”、“查看所有密钥管理服务信息”、“管理外置密钥管理服务”、“管理内置密钥管理服务”、“管理加密”、“迁移 default 虚拟机网络至其他 VDS”小节；
- 更新了“查询物理盘健康记录”、“挂载物理盘”、“查看当前节点数据分区信息”、“格式化指定路径下的数据分区”、“将数据分区挂载至 chunk”、“查看当前节点 Journal 分区信息”、“格式化指定路径下的 Journal 分区”、“将 Journal 分区挂载到 chunk”、“查看拓扑列表”、“查看机架、机箱、节点的详细信息”、“更新机架、机箱、节点的详细信息”、“查看节点缓存信息”、“格式化指定路径下的缓存分区”、“将缓存分区挂载到 chunk”、“将节点 chunk 注册到 meta 中”、“查看集群中节点下的 chunk 列表”、“查看 chunk 所有 PID”、“查看集群中所有 chunk 的空间负载情况”、“查看 chunk 信息”、“查看节点恢复速度”、“查看节点的迁移速度”、“查看本地 chunk 的数据块”、“查看本地 chunk 的地址配置信息”、“查看 chunk 的实时 I/O metric 数据”、“查看本地 chunk 的下沉信息”、“将某个 chunk 从节点移除”、“设置 chunk 的数据校验模式”、“设置下沉策略的相关参数”、“查询下沉策略的相关参数”、“查看所有的 iSCSI target”、“查看指定 iSCSI target 的基本信息和 CHAP 认证信息”、“创建 iSCSI target”、“更新 iSCSI target”、“设置 initiator CHAP 认证”、“更新 initiator CHAP 认证设置”、“更新 Target CHAP 认证”、“查看 iSCSI LUN 信息”、“创建 iSCSI LUN”、“克隆 iSCSI LUN”、“移动 iSCSI LUN 至另一 iSCSI target”、“查看 UIO/Access 统计信息”、“查看 access 模块的总体性能信息”、“查看 LSM 模块的总体性能信息”、“设置网桥参数”、“同步网桥网卡修改后的信息至数据库”、“将多个网口绑定为一个支持 LACP 协议的网口”、“创建 VLAN 子接口”、“给绑定网口直接配置静态 IP、子网掩码、网关”、“配置指定物理网口”、“清除部署前的管理网络配置信息”、“清除节点所有网络配置信息”小节。

---

## 命令行须知

# 命令行须知

## 通用格式说明

本文档中使用的命令行格式说明如下表所示。

| 格式 | 说明 |
| --- | --- |
| `zbs-meta migrate list` | 不带参数的命令，按原样输入。例如：  `zbs-meta migrate list` |
| `<parameter_value>` | 尖括号表示必选参数，需用参数值代替。例如:  语法：`shutdown <IP address>`  输入：`shutdown 192.168.67.59` |
| `|` | 竖线用于分隔多个互斥的可选参数 |
| `{}` | 大括号表示有多个参数，但必选一个。例如：  `shutdown {<IP address> | <MAC address>}` |
| `[]` | 方括号表示可选参数，可为空。例如：  `shutdown [force | now]` |

## 通用参数说明

大部分命令支持以下通用参数，需在子命令前指定。

| 参数 | 说明 |
| --- | --- |
| `-h`, `--help` | 显示命令的帮助信息，包括使用方式和支持的子命令。 |
| `-v` | 输出详细的执行细节和报错信息（verbose 模式）。 |
| `-f <format>` | 指定输出格式，支持 `json`、`table`、`dict` 三种格式。详细说明请参考[输出格式的说明](#%E8%BE%93%E5%87%BA%E6%A0%BC%E5%BC%8F%E7%9A%84%E8%AF%B4%E6%98%8E)。 |

## 输出格式说明

当前支持通过 `-f` 参数指定命令的输出格式：

- `json`：JSON 格式输出。适用于自动化脚本解析。如果您需要编写自动化脚本或测试程序来解析此命令的输出，**强烈建议使用 JSON 格式输出**，JSON 格式输出始终保持前向兼容，确保脚本在版本升级后仍能正常工作。
- `table`：表格格式输出，默认的文本输出格式，便于人工阅读。文本格式可能会在版本更新中进行优化调整，无法保证前向兼容性，可能导致测试脚本失效的情况。
- `dict`：字典格式输出。

---

## 管理集群 > 查看集群信息

# 查看集群信息

## 查看集群整体信息

查看集群的健康节点、总存储空间、已使用存储空间等信息。

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta cluster summary`

**输出示例**

```
{'alive_meta_hosts': [{'ip': '10.2.234.197', 'port': 10100},
                      {'ip': '10.2.234.196', 'port': 10100},
                      {'ip': '10.2.234.198', 'port': 10100}],
 'allocated_data_space': 0,
 'alloced_lids': 8237,
 'alloced_pids': 8242,
 'cluster_info': {'access_write_compress_enabled': False,
                  'default_prio_space_ratio': 0,
                  'desc': 'smtxzbs_cluster_desc',
                  'is_stretched': False,
                  'name': 'smtxzbs_cluster',
                  'negotiated_config': {'chunk_zk_session': True,
                                        'deprecated__enable_thick_extent': False,
                                        'enable_config_push': True,
                                        'enable_data_report_channel': True,
                                        'enable_lextent_lease': True,
                                        'enable_offload_unmap': True,
                                        'enable_temporary_replica': True,
                                        'enable_thick_extent': True,
                                        'enable_tiering': True,
                                        'enable_unmap': True},
                  'no_performance_layer': False,
                  'object_version': {'lextent_version': 2},
                  'preferred_zone_id': 'default',
                  'replica_capacity_only': False,
                  'uuid': 'fef6f2ea-e2fd-44ba-ac17-f78555e74e7e',
                  'zk_uuid_recorded': True},
 'cluster_perf': {...},
 'connecting_nodes': 0,
 'data_reduction_info': {'data_reduction_ratio': 0.0,
                         'data_reduction_saving': 0,
                         'overall_efficiency': 0.0},
 'dirty_cache_space': 539230208,
 'error_nodes': 1,
 'failure_cache_space': 0,
 'failure_data_space': 0,
 'healthy_nodes': 2,
 'idle_nodes': 0,
 'in_use_nodes': 3,
 'leader': '10.2.234.197:10100',
 'migrate_enabled': True,
 'migrate_speed': 0,
 'num_ongoing_migrates': 0,
 'num_ongoing_recovers': 0,
 'num_pending_migrates': 0,
 'num_pending_recovers': 0,
 'num_pending_recycles': 0,
 'perf_allocated_data_space': 538443776,
 'perf_failure_data_space': 0,
 'perf_planned_space': 5906628608,
 'perf_total_data_capacity': 64419790848,
 'perf_used_data_space': 538443776,
 'perf_valid_data_space': 64419790848,
 'provisioned_data_space': 0,
 'recover_enabled': True,
 'recover_info': {'cross_zone_migrate_speed': 0,
                  'cross_zone_recover_migrate_speed': 0,
                  'cross_zone_recover_speed': 0,
                  'migrate_speed': 0,
                  'ongoing_migrates_bytes': 0,
                  'ongoing_recovers_bytes': 0,
                  'pending_migrates_bytes': 0,
                  'pending_recovers_bytes': 0,
                  'recover_migrate_speed': 0,
                  'recover_speed': 0},
 'recover_migrate_speed': 0,
 'recover_speed': 0,
 'removing_nodes': 0,
 'serial': 'fef6f2ea-e2fd-44ba-ac17-f78555e74e7e',
 'space_info': {...},
 'storage_pools': [...],
 'total_cache_capacity': 80524345344,
 'total_data_capacity': 1940278738944,
 'total_nodes': 3,
 'total_prio_volume_size': 0,
 'upgrade_mode_duration': 0,
 'used_cache_space': 539230208,
 'used_data_space': 2684354560,
 'valid_cache_space': 80524345344,
 'valid_data_space': 1940278738944,
 'valid_free_cache_space': 79985115136,
 'warning_nodes': 0,
 'zone_infos': [...]}
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `connecting_nodes` | 正在连接的节点数。 |
| `dirty_cache_space` | 脏缓存空间大小，指还未下沉到数据分区的缓存空间。 |
| `error_nodes` | 异常节点数。 |
| `failure_cache_space` | 失效缓存空间，不健康的节点提供的存储都会失效。 |
| `failure_data_space` | 失效数据空间。 |
| `healthy_nodes` | 健康节点数。 |
| `idle_nodes` | 空闲节点数。 |
| `provisioned_data_space` | 已置备数据空间。 |
| `recover_enabled` | 是否开启数据恢复，当 extent 副本数量小于预期数量时会触发数据恢复。 |
| `removing_nodes` | 正在移除的节点。 |
| `total_cache_capacity` | 总缓存容量，总缓存盘的容量总和。 |
| `total_data_capacity` | 总数据容量。 |
| `used_cache_space` | 已使用缓存容量。 |
| `used_data_space` | 已使用数据容量。 |
| `valid_cache_space` | 有效的缓存容量，等于总缓存容量减去失效缓存容量。 |
| `valid_data_space` | 有效的数据容量，等于总数据容量减去失效数据容量。 |

> **注意**：
>
> 在出现坏盘或者拔盘的情况下，`total_data_capacity` 可能出现比 `used_data_space` 小的情况。这是因为 `total_data_capacity` 会排除坏盘或拔出物理盘的空间，而 `used_data_space` 则需要等待数据恢复后才会被更新。

## 查看集群性能数据

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta cluster perf`

**输出示例**

```
---------------  ------------
read_iops        0.0
read_avgrq       0 B
read_avgqz       0.0
read_bandwidth   0 B/s(0 B/s)
read_latency     0.0 NS
write_iops       0.0
write_avgrq      0 B
write_avgqz      0.0
write_bandwidth  0 B/s(0 B/s)
write_latency    0.0 NS
---------------  ------------
```

**输出说明**

| 参数 | 说明 | 单位 |
| --- | --- | --- |
| `read_iops` | 集群读请求 IOPS。 | 次/s |
| `read_avgrq` | 集群读请求的平均请求块大小（估算）。 | byte，自动调整 |
| `read_avgq` | 集群读请求平均深度（估算）。 | 无 |
| `read_bandwidth` | 集群读请求带宽。 | byte/s，自动调整 |
| `read_latency` | 集群读请求延时，是用户 I/O 在存储系统内观察到的延时，反映集群的整体存储性能 | ns，自动调整 |
| `write_iops` | 集群写请求 IOPS。 | 次/s |
| `write_avgrq` | 集群写请求的平均请求块大小（估算）。 | byte，自动调整 |
| `write_avgqz` | 集群写请求平均深度（估算）。 | 无 |
| `write_bandwidth` | 集群写请求带宽。 | byte，自动调整 |
| `write_latency` | 集群写请求延时，是用户 I/O 在存储系统内观察到的延时，反映集群的整体存储性能 | ns，自动调整 |

## 查看集群的 NTP 服务器

**操作方法**

在集群任一节点执行如下命令：

`ntpm source show`

**输出示例**

![](https://cdn.smartx.com/internal-docs/assets/d15aec0b/cli_guide_03.png)

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `NTP SERVER` | NTP 服务器的地址，可以是 IP 或者域名。 |
| `TYPE` | NTP 服务器类型。其中，`external` 表示该服务器为用户配置的外部 NTP 服务器，`internal` 表示使用集群内部某个节点作为 NTP 服务器。当用户未配置外部 NTP 服务器或外部 NTP 服务器均不可用时，会使用内部 NTP 服务器进行同步。 |

## 查看集群 Boost 模式状态

**操作方法**

在集群任一节点执行如下命令：

`zbs-cluster vhost show`

**输出示例**

```
Finish check vhost state.
Cluster vhost status: disabled, allow update.
```

**输出说明**

- 若输出中 `Cluster vhost status` 为 `enabled`，表示集群 Boost 模式已开启。
- 若输出中 `Cluster vhost status` 为 `disabled`，表示集群 Boost 模式已关闭。

---

## 管理集群 > 查看集群服务 > 查看集群中的服务

# 查看集群中的服务

## 查看集群中运行的所有服务信息

**操作方法**

在集群任一节点执行如下命令，查看集群中运行的所有服务信息，输出结果将默认为文本格式：

`zbs-tool service list`

您也可以指定输出格式：

- 指定输出为 JSON 格式：

  `zbs-tool -f json service list`

  如果您需要编写自动化脚本或测试程序来解析此命令的输出，**强烈建议使用 JSON 格式输出**，JSON 格式输出始终保持前向兼容，确保脚本在版本升级后仍能正常工作。
- 指定输出为文本格式：

  `zbs-tool -f table service list`

  文本格式可能会在版本更新中进行优化调整，无法保证前向兼容性，可能导致测试脚本失效的情况。

**输出示例**

- 文本格式输出：

  ```
  Name    Members                                                       Leader            Specified members                                             Priority    Current priority
  ------  ------------------------------------------------------------  ----------------  ------------------------------------------------------------  ----------  ------------------
  meta    ['10.0.20.52:10100', '10.0.20.51:10100', '10.0.20.50:10100']  10.0.20.50:10100  ['10.0.20.50:10100', '10.0.20.51:10100', '10.0.20.52:10100']
  ntp     ['10.0.20.52:0', '10.0.20.51:0', '10.0.20.50:0']              10.0.20.50:0      ['']
  taskd   ['10.0.20.51:10601', '10.0.20.50:10601', '10.0.20.52:10601']  10.0.20.50:10601  ['']
  ```
- JSON 格式输出：

  ```
  [{"Name": "insight", "Members": "['10.234.1.2:10701', '10.234.1.3:10701', '10.234.1.1:10701']", "Leader": "10.234.1.3:10701", "Specified members": "['']", "Priority": "", "Current priority": ""}, {"Name": "meta", "Members": "['10.234.1.2:10100', '10.234.1.3:10100', '10.234.1.1:10100']", "Leader": "10.234.1.2:10100", "Specified members": "['10.234.1.2:10100', '10.234.1.1:10100', '10.234.1.3:10100']", "Priority": "10.234.1.2:10100:3,10.234.1.1:10100:2,10.234.1.3:10100:1", "Current priority": ""}]
  ```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Name` | 集群中运行的服务名称。 |
| `Members` | 服务中包含的 members，其格式为 `IP：Port`。 |
| `Leader` | 当前服务的主节点。 |
| `Specified members` | 运行 meta 服务的节点。 |
| `Priority` | 为某服务的 members 设置的优先级，取值为 0 ~ 255 的整数，数值越大，优先级越高。若 `Priority` 中没有显示某节点，则该节点的优先级默认为 1。 |
| `Current priority` | 当前某服务的 members 的优先级。 `Current priority` 可根据节点状态在优先级不高于 `Priority` 的范围内自动进行动态调整，节点检测到自身异常时，主动降低自身的当前优先级，检测到服务恢复后，再将当前优先级恢复至设置的优先级。节点正常运行时，`Current priority` 与 `Priority` 相同。若 `Current priority` 中没有显示某节点，则该节点当前的 `Current priority` 默认与 `Priority` 相同。 |

## 查看某服务的详细信息

**操作方法**

在集群任一节点执行如下命令：

`zbs-tool service show <service_name>`

`<service_name>` 指待查询详细信息的服务名。

**使用示例**

`zbs-tool service show meta`

**输出示例**

```
-----------------  -----------------------------------------------------------------------------------------
Name               meta
Members            ['10.10.25.47:10100', '10.10.29.172:10100', '10.10.29.232:10100', '10.10.31.176:10100']
Leader             10.10.25.47:10100
Specified members  ['[10.10.25.47:10100', '10.10.31.176:10100', '10.10.29.172:10100', '10.10.29.232:10100]']
Priority           10.10.25.47:10100:2,10.10.31.176:10100:2,10.10.29.172:10100:1,10.10.29.232:10100:1
Current priority
-----------------  -----------------------------------------------------------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Name` | 集群中运行的服务名称。 |
| `Members` | 服务中包含的 members，其格式为 `IP：Port`。 |
| `Leader` | 当前服务的主节点。 |
| `Specified members` | 运行 meta 服务的节点。 |
| `Priority` | 为某服务的 members 设置的优先级，取值为 0 ~ 255 的整数，数值越大，优先级越高。若 `Priority` 中没有显示某节点，则该节点的优先级默认为 1。 |
| `Current priority` | 当前某服务的 members 的优先级。 `Current priority` 可根据节点状态在优先级不高于 `Priority` 的范围内自动进行动态调整，节点检测到自身异常时，主动降低自身的当前优先级，检测到服务恢复后，再将当前优先级恢复至设置的优先级。节点正常运行时，`Current priority` 与 `Priority` 相同。若 `Current priority` 中没有显示某节点，则该节点当前的 `Current priority` 默认与 `Priority` 相同。 |

## 查看所有服务的 VIP

**操作方法**

执行如下命令，列出所有服务的 VIP：

`vipservice-tool show`

**输出示例**

```
+------------+--------------+---------------------------------------------+
| NAME       | IP           | VIP-LEADER                                  |
+------------+--------------+---------------------------------------------+
| iscsi      | 101.19.1.74  | f9c441ee-91b4-4b43-b13f-ff3136fd2bf8/node34 |
| management | 192.168.66.5 | 784a8264-948e-4742-93a0-8b50c9e0a81e/node31 |
+------------+--------------+---------------------------------------------+
```

---

## 管理集群 > 查看集群服务 > 查看本地 meta 状态

# 查看本地 meta 状态

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta local status`

**输出示例**

```
{ 'alive_meta_hosts': [ { 'ip': u'10.0.22.223',
                          'port': 10100},
                        { 'ip': u'10.0.22.222',
                          'port': 10100},
                        { 'ip': u'10.0.22.221',
                          'port': 10100}],
  'is_leader': False,
  'leader': u'10.0.22.223:10100',
  'meta_status': 'META_RUNNING'}
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `alive_meta_hosts` | 集群中各个主节点的存储网络 IP。 |
| `is_leader` | 当前节点是否为 leader 节点。 |
| `leader` | Leader 节点的 IP 地址。 |
| `meta_status` | 本地 meta 状态。 |

---

## 管理集群 > 查看集群服务 > 管理 Zookeeper 服务

# 管理 Zookeeper 服务

## 查看所有 Zookeeper 服务运行是否正常

**操作方法**

在集群任一节点执行如下命令，查看 Zookeeper 服务是否运行正常：

`zbs-tool zk list`

**输出示例**

若输出以下信息，则表示 ZooKeeper 服务运行正常；若返回报错信息，则表示 ZooKeeper 服务异常。

```
10.0.20.50:2181	  follower	0x100000aa8
10.0.20.51:2181	  follower	0x100000aa8
10.0.20.52:2181	    leader	0x100000aa8
```

**输出说明**

输出运行 Zookeeper 服务的节点 IP 地址、节点角色和 Zookeeper 事务 ID。

## 查看运行 Zookeeper 服务节点的状态

**操作方法**

在集群任一节点执行如下命令：

`zbs-tool zk status`

**输出示例**

```
10.0.20.50:2181: imok
10.0.20.51:2181: imok
10.0.20.52:2181: imok
```

**输出说明**

`imok` 表示节点 Zookeeper 服务正常运行。

## 查看 Zookeeper 服务运行信息

**操作方法**

在集群任一节点执行如下命令：

`zbs-tool zk stat`

**输出示例**

```
10.0.20.50:2181:
       'Zookeeper version: 3.5.9-3661b1e3c6c87ec14990b65968fe4a3bed5f7235, built on 07/31/2022 15:45 GMT',
        'Clients:',
        ' /10.0.20.52:37730[1](queued=0,recved=4655,sent=4909)',
        ' /10.0.20.51:60136[1](queued=0,recved=3533,sent=3533)',
        ' /10.0.20.50:47502[1](queued=0,recved=3527,sent=3527)',
        ' /10.0.20.51:54430[1](queued=0,recved=4553,sent=4803)',
        ' /10.0.20.51:56094[1](queued=0,recved=454,sent=454)',
        ' /10.0.20.52:37710[1](queued=0,recved=2768,sent=2769)',
        ' /10.0.20.52:38122[1](queued=0,recved=3676,sent=3676)',
        ' /10.0.20.50:42962[1](queued=0,recved=454,sent=454)',
        ' /10.0.20.52:44324[0](queued=0,recved=1,sent=0)',
        ' /10.0.20.51:54812[1](queued=0,recved=3676,sent=3676)',
        ' /10.0.20.50:41556[1](queued=0,recved=3676,sent=3676)',
        ' /10.0.20.52:38332[1](queued=0,recved=3672,sent=3672)',
        ' /10.0.20.52:43420[1](queued=0,recved=3533,sent=3533)',
        ' /10.0.20.52:37740[1](queued=0,recved=2773,sent=2774)',
        ' /10.0.20.51:56086[1](queued=0,recved=454,sent=454)',
        ' /10.0.20.51:56096[1](queued=0,recved=454,sent=454)',
        ' /10.0.20.50:42960[1](queued=0,recved=454,sent=454)',
        '',
        'Latency min/avg/max: 0/0/11',
        'Received: 51215',
        'Sent: 51728',
        'Connections: 17',
        'Outstanding: 0',
        'Zxid: 0x100000b0f',
        'Mode: follower',
        'Node count: 1315'
...
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Latency min/avg/max` | 最小、平均和最大响应延时，单位：ms。 |
| `Received` | 收包数。 |
| `Sent` | 发包数。 |
| `Outstanding` | 堆积请求数目。 |
| `Zxid` | 事务 ID。 |
| `Mode` | 主从状态。 |
| `Node count` | Node 数量。 |

## 查看 Zookeeper 运行环境

**操作方法**

在集群任一节点执行如下命令：

`zbs-tool zk env`

**输出示例**

```
10.0.0.20:2181:
'Environment:',
'zookeeper.version=3.4.10-e52e475caf7498b144747d385f506fd1e4633805, built on 05/26/2017 06:34 GMT',
'host.name=<NA>',
'java.version=1.8.0_131',
'java.vendor=Oracle Corporation',
'java.home=/usr/java/jdk1.8.0_131/jre',
'java.class.path=/usr/sbin/../build/classes:/usr/sbin/../build/lib/*.jar:/usr/sbin/../share/zookeeper/zookeeper-3.4.10.jar:/usr/sbin/../share/zookeeper/slf4j-log4j12-1.6.1.jar:/usr/sbin/../share/zookeeper/slf4j-api-1.6.1.jar:/usr/sbin/../share/zookeeper/netty-3.10.5.Final.jar:/usr/sbin/../share/zookeeper/log4j-1.2.16.jar:/usr/sbin/../share/zookeeper/jline-0.9.94.jar:/usr/sbin/../src/java/lib/*.jar:/etc/zookeeper:',
'java.library.path=/usr/java/packages/lib/amd64:/usr/lib64:/lib64:/lib:/usr/lib',
'java.io.tmpdir=/tmp',
'java.compiler=<NA>',
'os.name=Linux',
'os.arch=amd64',
'os.version=3.10.0-327.36.3.el7.smartx.2.x86_64',
'user.name=zookeeper',
'user.home=/usr/share/zookeeper',
'user.dir=/'
...
```

## 查看 Zookeeper 详细信息

**操作方法**

在集群任一节点执行如下命令：

`zbs-tool zk detail`

**输出示例**

```
10.0.0.20:2181:
'Zookeeper version: 3.4.10-e52e475caf7498b144747d385f506fd1e4633805, built on 05/26/2017 06:34 GMT',
'Latency min/avg/max: 0/0/416',
'Received: 11412218',
'Sent: 11472904',
'Connections: 5',
'Outstanding: 0',
'Zxid: 0x100283f5b',
'Mode: follower',
'Node count: 66652'
...
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Latency min/avg/max` | 最小、平均和最大响应延时，单位：ms。 |
| `Received` | 收包数。 |
| `Sent` | 发包数。 |
| `Outstanding` | 堆积请求数目。 |
| `Zxid` | 事务 ID。 |
| `Mode` | 主从状态。 |
| `Node count` | Node 数量。 |

---

## 管理集群 > 查看集群服务 > 查看 Mongo 服务

# 查看 Mongo 服务

## 查看当前 Mongo 集群所有成员节点的整体状态

**操作方法**

在集群任一节点执行如下命令：

`zbs-node mongo status`

**输出示例**

```
{
    "$clusterTime": {
        "clusterTime": {
            "$timestamp": {
                "i": 164,
                "t": 1668590597
            }
        },
        "signature": {
            "hash": {
                "$binary": "AAAAAAAAAAAAAAAAAAAAAAAAAAA=",
                "$type": "00"
            },
            "keyId": 0
        }
    },
    "date": {
        "$date": 1668590597686
    },
    "electionCandidateMetrics": {
        "electionTerm": 1,
        "electionTimeoutMillis": 10000,
        "lastCommittedOpTimeAtElection": {
            "t": -1,
            "ts": {
                "$timestamp": {
                    "i": 1,
                    "t": 1668587490
                }
            }
        },
        "lastElectionDate": {
            "$date": 1668587502162
        },
        "lastElectionReason": "electionTimeout",
        "lastSeenOpTimeAtElection": {
            "t": -1,
            "ts": {
                "$timestamp": {
                    "i": 1,
                    "t": 1668587490
                }
            }
        },
...
}
```

**输出说明**

通过输出结果中如下参数可查看 Mongo 服务运行是否正常。

- `not reacheable/health`：该节点的 Mongo 服务运行异常。
- `PRIMARY`：该节点的角色为 primary，并且 Mongo 服务运行正常。
- `SECONDARY`：该节点的角色为 secondary，并且 Mongo 服务运行正常。

## 查看当前 Mongo 集群所有成员节点的 IP 地址和端口

**操作方法**

在集群任一节点执行如下命令：

`zbs-node mongo list`

**输出示例**

```
10.0.0.11:27017
10.0.0.13:27017
10.0.0.14:27017
```

## 查看当前 Mongo 集群中的 primary 节点

**操作方法**

在集群任一节点执行如下命令：

`zbs-node mongo leader`

**输出示例**

```
10.0.0.11:27017
```

## 进入 Mongo Shell 执行查询或维护工作

**操作方法**

在集群中运行了 mongod 服务的节点上执行如下命令，进入 Mongo Shell 执行查询或维护工作。该命令等同于 MongoDB 官方提供的 `mongo` 或 `mongosh` 命令。

`zbs-node mongo shell`

**输出示例**

```
MongoDB shell version v5.0.6
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("75e9a2c2-d8ab-4f12-b5b1-fcfab66d06db") }
MongoDB server version: 5.0.6
================
Warning: the "mongo" shell has been superseded by "mongosh",
which delivers improved usability and compatibility.The "mongo" shell has been deprecated and will be removed in
an upcoming release.
For installation instructions, see
https://docs.mongodb.com/mongodb-shell/install/
================
---
The server generated these startup warnings when booting:
        2022-11-16T16:30:25.280+08:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
        2022-11-16T16:30:25.972+08:00: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
        2022-11-16T16:30:25.972+08:00: You are running on a NUMA machine. We suggest launching mongod like this to avoid performance problems: numactl --interleave=all mongod [other options]
---
---
        Enable MongoDB's free cloud-based monitoring service, which will then receive and display
        metrics about your deployment (disk utilization, CPU, operation statistics, etc).

        The monitoring data will be available on a MongoDB website with a unique URL accessible to you
        and anyone you share the URL with. MongoDB may use this information to make product
        improvements and to suggest MongoDB products and deployment options to you.

        To enable free monitoring, run the following command: db.enableFreeMonitoring()
        To permanently disable this reminder, run the following command: db.disableFreeMonitoring()
---
zbs:SECONDARY>
```

## 将 Mongo 节点和其他节点重新同步

当 Mongo 节点由于数据目录异常，或由于与 Mongo primary 节点失去同步，陷入 RECOVERING 状态时，可以使用此命令清空本节点的 Mongo 数据目录（/var/lib/mongodb），并重启本节点的 mongod 服务，以重新和其他节点同步数据恢复正常状态。

**操作方法**

在需要重新同步的 Mongo 节点执行如下命令：

`zbs-node mongo resync`

**输出示例**

```
All mongo data on this node will be cleared
Are you sure to continue? [y/N]: y
2024-12-24 14:36:47,317 node.py 1296 [53562] [INFO] pre-check success, mongod is ready to resync
2024-12-24 14:36:47,317 recovering_resync.py 169 [53562] [INFO] starting rescue mongod ...
2024-12-24 14:36:47,317 recovering_resync.py 74 [53562] [INFO] stopping mongod.service ...
2024-12-24 14:36:47,333 recovering_resync.py 78 [53562] [INFO] cmd: systemctl status mongod res: 0 output: ● mongod.service - containerd mongod.service
...
2024-12-24 14:36:47,334 recovering_resync.py 83 [53562] [INFO] systemctl stop mongod
2024-12-24 14:37:03,889 recovering_resync.py 85 [53562] [INFO] cmd: systemctl stop mongod res: 0 output:
2024-12-24 14:37:03,916 recovering_resync.py 93 [53562] [INFO] cmd: systemctl status mongod res: 3 output: ● mongod.service - containerd mongod.service
...
2024-12-24 14:37:03,917 recovering_resync.py 130 [53562] [INFO] cleaning /var/lib/mongodb/ ...
2024-12-24 14:37:03,924 recovering_resync.py 142 [53562] [INFO] clean data files: /var/lib/mongodb/collection-412-6983241241505598203.wt
...
2024-12-24 14:37:04,020 recovering_resync.py 142 [53562] [INFO] clean data files: /var/lib/mongodb/index-304-6983241241505598203.wt
2024-12-24 14:37:04,020 recovering_resync.py 98 [53562] [INFO] restarting mongod.service ...
2024-12-24 14:37:04,047 recovering_resync.py 102 [53562] [INFO] cmd: systemctl status mongod res: 3 output: ● mongod.service - containerd mongod.service
...
2024-12-24 14:37:04,047 recovering_resync.py 107 [53562] [INFO] systemctl restart mongod
2024-12-24 14:37:04,136 recovering_resync.py 109 [53562] [INFO] cmd: systemctl restart mongod res: 0 output:
2024-12-24 14:37:04,150 recovering_resync.py 117 [53562] [INFO] cmd: systemctl status mongod res: 0 output: ● mongod.service - containerd mongod.service
...
2024-12-24 14:37:04,150 recovering_resync.py 158 [53562] [INFO] check mongo rs.status(), round 0
2024-12-24 14:37:04,153 recovering_resync.py 164 [53562] [INFO] wait for mongo recovery: (not reachable/healthy)
2024-12-24 14:37:14,155 recovering_resync.py 158 [53562] [INFO] check mongo rs.status(), round 1
2024-12-24 14:37:14,157 recovering_resync.py 161 [53562] [INFO] mongo state become healthy: SECONDARY
2024-12-24 14:37:14,157 node.py 1298 [53562] [INFO] resync mongod data succeed
```

---

## 管理集群 > 管理集群服务

# 管理集群服务

## 设置网络服务 CPU 模式

**操作方法**

在 SMTX OS（ELF）集群任一节点执行如下命令：

`zbs-cluster network_cpu_mode set --mode {share|isolate_normal}`

| **参数** | **说明** |
| --- | --- |
| `--mode {share|isolate_normal}` | 必须输入的参数。代表网络服务的 CPU 模式。  - `share`：网络服务运行在系统服务预留的 CPU 上，集群部署后默认为此模式。 - `isolate_normal`：网络服务运行在集群额外为其预留的 2 核 CPU 上，网络服务压力较高的集群可切换至此模式。 |

**输出示例**

```
...
2025-12-12 10:19:53,716 cluster.py 1150 [18537] [INFO] Setting network cpu mode to isolate_normal for all cluster nodes...
...
2025-12-12 10:18:52,887 cluster.py 1158 [14225] [INFO] Successfully set network cpu mode to share for all cluster nodes
```

## 设置服务优先级

为某服务的 members 设置优先级。

**操作方法**

在集群任一节点执行如下命令，设置 `service_name` 服务的优先级：

`zbs-tool service set_priority [--force] <service_name> <priority>`

| 参数 | 说明 |
| --- | --- |
| `--force` | 可选参数，将 `Current priority` 临时设置为与 `Priority` 相同。 在查看集群中运行的服务时，可以查询到 `Current priority`。  `Current priority` 为当前优先级，可根据节点状态在优先级不高于 `Priority` 的范围内自动进行动态调整。使用 `--force` 时，可确保在当前时刻，`Current priority` 与 `Priority`相同。 |
| `service_name` | 必选参数，待设置优先级的服务名。可通过 `zbs-tool service list` 查询集群中运行的服务及其 members。 |
| `priority` | 必选参数，服务的优先级。  格式为 `IP:Port:priority`，可对同一个服务的一个或多个 member 进行设置。如对多个 member 进行设置，用逗号（,）分隔，例如`IP1:Port1:priority1,IP2:Port2:priority2`。   - `IP:Port`：指的是某个服务的 member。 - `priority`：指的是服务的优先级，取值为 0 ~ 255 的整数，数值越大，优先级越高。 |

**使用示例**

将 taskd 服务的 member `10.0.100.42:10602` 的优先级设置为 `2`；`10.0.100.53:10600` 的优先级设置为 `254`。

`zbs-tool service set_priority taskd 10.0.100.42:10602:2,10.0.100.53:10600:254`

**输出说明**

执行成功无输出。

## 注册服务信息

在集群部署或升级阶段执行该命令进行报警规则以及其他服务依赖信息的自动注册，如果特殊场景下手动修改关联规则（在 /etc/aquarium/register\_conf/）后，可以执行该命令进行信息注册来自动更新。

**操作方法**

在集群任一节点执行如下命令：

`zbs-deploy-manage register-service`

**输出说明**

输出注册服务过程。

## 设置服务的 VIP

**操作方法**

执行如下命令，把名为 `service_name` 的服务的 VIP 设为 `ipv4_vip`。目前支持的 `service_name` 包括 `iscsi` 和 `management`：

`vipservice-tool set <service_name> <ipv4_vip>`

**输出说明**

执行成功无输出。

## 删除服务的 VIP

**操作方法**

执行如下命令，删除名为 `service_name` 的服务的 VIP：

`vipservice-tool delete <service_name>`

**输出说明**

执行成功无输出。

## 切换服务的 VIP 所在主机

**操作方法**

执行如下命令，把名为 `service_name` 的服务的 VIP 切换至其他可用节点：

`vipservice-tool drain <service_name>`

**输出说明**

执行成功无输出。

## 将服务的 VIP 从 zbs-taskd 迁移至 vipservice 进行管理

**操作方法**

执行如下命令，将服务为 `management` 和 `iscsi` 的 VIP 从 `zbs-taskd` 迁移到 `vipservice` 进行管理：

`vipservice-tool migrate`

**输出示例**

```
migrate service management from taskd to vipservice
migrate service management from taskd: done
migrate service iscsi from taskd to vipservice
migrate service iscsi from taskd: done
```

---

## 管理集群 > 更新集群配置

# 更新集群配置

## 设置集群名称和描述

**操作方法**

在集群任一节点执行如下命令，更新集群名称和描述：

`zbs-meta cluster update [--new_name <NEW_NAME>] [--new_desc <NEW_DESC>]`

| 参数 | 说明 |
| --- | --- |
| `--new_name <NEW_NAME>` | 可选参数，更新集群名称。 |
| `--new_desc <NEW_DESC>` | 可选参数，更新集群描述。 |

**输出说明**

执行成功无输出。

## 手动生成 cgroup 配置信息

SMTX OS 使用 cgroup 进行进程级别资源隔离，在部署和升级阶段会自动生成 cgroup 配置。若节点 cgroup 配置信息存在人为改动情况，可使用该命令重新生成 cgroup 配置信息并使其生效。

**操作方法**

执行如下命令：

`zbs-deploy-manage config_cgroup`

**输出说明**

输出 cgroup 配置过程。

---

## 管理集群 > 集群部署及升级相关操作

# 集群部署及升级相关操作

## 配置节点的 /etc/hosts 文件（ELF 平台）

当集群虚拟化平台为 ELF 时，如需对所有节点 /etc/hosts 进行配置，可以使用该命令进行配置，配置时需要输入节点当前主机名称。

**操作方法**

在集群节点执行如下命令：

`zbs-deploy-manage config_hosts <hostname>`

`hostname` 为节点当前主机名称。

**输出示例**

```
2021-07-21 18:34:43,970 INFO update_hosts: Query and insert hostname entry to /etc/hosts
2021-07-21 18:34:43,970 INFO update_hosts: hostname entry is already in /etc/hosts
```

## 更新 SCVM 自动重启脚本（VMware ESXi 平台）

当集群虚拟化平台为 VMware ESXi 时，执行升级操作后，应更新 SCVM 自动重启脚本。

**操作方法**

在集群的任意一个 SCVM 中执行如下命令，系统将自动检查和更新集群里每个 ESXi 节点的 SCVM 自动重启脚本。

`zbs-deploy-manage update-scvm-autostart`

**输出说明**

若输出 `Success update latest vmware scvm autostart script to all esxi done` 则表示所有 ESXi 节点的 SCVM 自动重启脚本已更新为最新版本。

## 清理节点部署标记

若集群部署失败，则应在部署失败集群的所有节点清理节点部署标记，使其恢复为未部署状态，以便重新进行扫描和部署。

请注意本条命令仅在部署失败时使用，禁止在其他场景使用。

**操作方法**

在部署失败集群的所有节点执行如下命令：

`zbs-deploy-manage clear_deploy_tag`

**输出说明**

执行成功无输出。

---

## 管理集群 > 管理 I/O 重路由脚本（VMware ESXi 平台）

# 管理 I/O 重路由脚本（VMware ESXi 平台）

## 部署 I/O 重路由脚本

当集群虚拟化平台为 VMware ESXi 时，通过命令方式部署 I/O 重路由脚本。

**操作方法**

在集群的每个 SCVM 中执行如下命令：

`zbs-deploy-manage deploy-hypervisor [--gen_ssh_key|--no_gen_ssh_key]`

**参数说明**

`[--gen_ssh_key|--no_gen_ssh_key]` 为可选参数，用于选择在部署过程中是否生成 SSH Key。若不填写，默认为不生成 SSH Key。

- `--gen_ssh_key`：生成 SSH Key。
- `--no_gen_ssh_key`：不生成 SSH Key。

**使用示例**

`zbs-deploy-manage deploy-hypervisor --gen_ssh_key`

**输出说明**

若输出 `Finish deploy hypervisor` 则表示部署成功。

## 清理 I/O 重路由脚本

当集群虚拟化平台为 VMware ESXi 时，若 I/O 重路由脚本部署失败，必须先清理部署在每个 ESXi 节点和 SCVM 上的脚本。

**操作方法**

在部署 I/O 重路由脚本失败的每个 SCVM 中执行如下命令：

`zbs-deploy-manage clear-hypervisor`

**输出说明**

若输出 `Finish clear hypervisor` 则表示清理成功。

## 更新 I/O 重路由脚本

当集群虚拟化平台为 VMware ESXi 时，执行升级操作后，应更新 I/O 重路由脚本。

**操作方法**

在集群的任意一个 SCVM 中执行如下命令，系统将自动检查和更新集群里每个 ESXi 节点的 I/O 重路由脚本。

`zbs-deploy-manage update_reroute_version`

**输出说明**

若输出 `Success update latest vmware reroute script to all esxi done` 则表示所有 ESXi 节点的 I/O 重路由脚本已更新为最新版本。

---

## 管理集群 > 管理集群许可

# 管理集群许可

查看当前许可证和激活新的许可证。

## 查看集群许可

**操作方法**

在集群任一节点执行如下命令查看集群当前许可信息：

`zbs-meta license show`

**输出示例**

```
-----------------------  ------------------------------------
serial                   fef6f2ea-e2fd-44ba-ac17-f78555e74e7e
sign date                2024-06-17 14:06:04
expire date              2024-07-17 14:06:04
subscribe sign date
subscribe expire date
maintenance start date
maintenance expire date
max space size           0.00 B
max node space size      128.00 TiB
max node num             255
license type             TRIAL
software edition         ENTERPRISE
oem vendor               SMTX
support metrox           True
support remote backup    True
support platform         BARE_METAL|KVM|VMWARE
system mode              SERVER_SAN
pricing type             PRICING_TYPE_UNKNOWN
-----------------------  ------------------------------------
```

## 激活新许可

**操作方法**

在集群任一节点执行如下命令激活新许可证：

`zbs-meta license set <license_number>`

其中，`license_number` 为集群序列号。

**输出说明**

执行成功无输出

## 解析许可

**操作方法**

执行如下命令解析许可证：

`zbs-meta license parse <license_number>`

**输出示例**

```
-------------- ------------------------------------
serial                   b136f2be-de9c-4889-95ed-3d3ebf974d16
sign date                2021-10-21 12:13:49
expire date              2021-11-20 12:13:49
subscribe sign date
subscribe expire date
maintenance start date
maintenance expire date
max space size           0.00 B
max node space size      128.00 TiB
max node num             255
license type             TRIAL
software edition         ENTERPRISE
oem vendor               SMTX
support metrox           True
support remote backup    True
support platform         BARE_METAL|KVM|VMWARE
-------------- ------------------------------------
```

---

## 管理集群 > 管理集群拓扑

# 管理集群拓扑

通过对区域、机架组和机架等进行控制，可以合理地将副本分放在不同的区域，以最大限度地提高数据安全性。

## 查看拓扑列表

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta topo list [--show_details]`

| 参数 | 说明 |
| --- | --- |
| `--show_details` | 可选参数，是否展示包含所有 chunk 对象以及 node 对象的完整拓扑对象清单。 |

**输出示例**

```
id                                    type     name                                          parent_id      ring_id    position.row    position.column    capacity.row    capacity.column    dimension.row    dimension.column  create_time          description
------------------------------------  -------  --------------------------------------------  -----------  ---------  --------------  -----------------  --------------  -----------------  ---------------  ------------------  -------------------  -------------
27742cfa-d7e7-4fe7-ba05-3290d4723b06  CHUNK    chunk-2-27742cfa-d7e7-4fe7-ba05-3290d4723b06  topo                 1               1                  1               1                  1                1                   1  2024-06-17 14:06:13  chunk2
36c38812-4f4d-44df-a09f-06437bcedb95  BRICK    new-brick                                     defrack              0               1                  1               1                  1                1                   1  2024-06-17 15:30:42
default                               ZONE     default                                       topo                 0               1                  1               1                  1                1                   1  1970-01-01 08:00:00
defrack                               RACK                                                   default              0               1                  1             256                  1                1                   1  1970-01-01 08:00:00
f677b91b-4932-4047-b5f2-f1988c8d8e32  CHUNK    chunk-3-f677b91b-4932-4047-b5f2-f1988c8d8e32  topo                 2               1                  1               1                  1                1                   1  2024-06-17 14:06:13  chunk3
fdaee4fd-8f5d-47a8-bf80-43e0f8db6ba7  CHUNK    chunk-1-fdaee4fd-8f5d-47a8-bf80-43e0f8db6ba7  topo                 3               1                  1               1                  1                1                   1  2024-06-17 14:06:12  chunk1
topo                                  CLUSTER                                                topo                 0               1                  1               1                  1                1                   1  1970-01-01 08:00:00
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `id` | 标识 ID。 |
| `type` | 拓扑类型：机架、机箱等等。 |
| `name` | 名称。 |
| `parent_id` | 父节点 ID。 |
| `ring_id` | 拓扑环 ID。 |
| `position.row`, `position.column` | 当前节点置于父节点的位置：横纵坐标。 |
| `capacity.row`, `capacity.column` | 节点自身容量。 |
| `dimension.row`, `dimension.column` | 占用父节点的大小。 |

## 创建机架和机箱

**操作方法**

在集群任一节点执行如下命令创建机架或机箱：

`zbs-meta topo create <type> <name>`

参数说明如下：

| 名称 | 说明 |
| --- | --- |
| `type` | - type 设为 `rack` 时，创建机架。例如：  `zbs-meta topo create rack new-rack --parent_id default`  创建一个名为 `new-rack` 的新机架。  - type 设为 `brick` 时，创建机箱。但其后必须要跟 `--parent_id` 参数，用来指定该机箱位于哪个机架。例如：  `zbs-meta topo create brick new-brick --parent_id d7c626fd`  创建一个名为 `new-brick` 的新机箱，该机箱被置于 ID 号为 `d7c626fd` 的机架中。 |
| `name` | 所创建机箱或机架的名称。 |

**输出说明**

执行成功无输出。

## 删除机架和机箱

**操作方法**

在集群任一节点执行如下命令删除机架或机箱：

`zbs-meta topo delete <id>`

`id` 为机架或机箱的 ID。

**输出说明**

执行成功无输出。

## 查看机架、机箱、节点的详细信息

**操作方法**

在集群任一节点执行如下命令，查看机架、机箱或节点的详细信息：

`zbs-meta topo show <id> [--show_details]`

| 参数 | 说明 |
| --- | --- |
| `id` | 必选参数，机架、机箱或节点的 ID。 |
| `--show_details` | 可选参数，当 ID 对应一个 chunk 物理盘池对象时是否展示其真实的父节点对象，默认展示其逻辑父节点对象。 |

**输出示例**

```
----------------  --------------------------------------------
id                27742cfa-d7e7-4fe7-ba05-3290d4723b06
type              CHUNK
name              chunk-2-27742cfa-d7e7-4fe7-ba05-3290d4723b06
parent_id         topo
ring_id           1
position.row      1
position.column   1
capacity.row      1
capacity.column   1
dimension.row     1
dimension.column  1
create_time       2024-06-17 14:06:13
description       chunk2
----------------  --------------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `id` | 标识 ID。 |
| `type` | 拓扑类型：机架、机箱等等。 |
| `name` | 名称。 |
| `parent_id` | 父节点 ID。 |
| `ring_id` | 拓扑环 ID。 |
| `position.row`, `position.column` | 当前节点置于父节点的位置：横纵坐标。 |
| `capacity.row`, `capacity.column` | 节点自身容量。 |
| `dimension.row`, `dimension.column` | 占用父节点的大小。 |

## 更新机架、机箱、节点的详细信息

**操作方法**

在集群任一节点执行如下命令，更新机箱、机架或节点的信息（对 chunk 物理盘池对象更新其位置信息会自动转换为对 node 节点对象进行更新）。

`zbs-meta topo update <id>`

**输出说明**

执行成功无输出。

---

## 管理集群 > 管理集群接入服务

# 管理集群接入服务

## 查看接入服务的所有会话状态

**操作方法**

每个可用的接入点和 meta 之间会维持一个会话（session）。在集群任一节点执行如下命令可查看接入服务的会话（access session）状态的列表：

`zbs-meta session list`

**输出示例**

```
UUID                                  Ip              Port    Cid  Secondary_data_ip    Zone     Machine UUID
------------------------------------  ------------  ------  -----  -------------------  -------  ------------------------------------
0b48597c-7d6b-45a7-82f5-94f3b9f0aaa0  10.2.234.198   10201      1  10.93.180.25         default  22a79016-2c6d-11ef-806c-52540097039a
8af221a8-96ad-4d82-ae41-94756414a170  10.2.234.197   10201      3  10.93.180.24         default  0f8d8274-2c6d-11ef-a0c4-52540097039a
d1ceb1f7-8142-4922-a717-cbe4e948c766  10.2.234.196   10201      2  10.93.180.23         default  05e85370-2c6d-11ef-ba09-52540097039a
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `UUID` | 会话的 UUID。 |
| `IP` | 存储网络地址。 |
| `Port` | 存储端口。 |
| `Cid` | 节点所在的 cluster ID。 |
| `Secondary_data_ip` | 管理网络地址。 |
| `Zone` | 所属区域，用来区分多活集群。 |
| `Machine UUID` | Access 所在物理节点的 UUID。 |

## 查看指定会话的详细信息

**操作方法**

在集群任一节点执行如下命令，根据 UUID 查询会话：

`zbs-meta session show <session_id>`

**输出示例**

```
{ 'group': u'access',
  'items': [ { 'key': u'ZBS-ISCSI',
               'value': u'dummy'},
             { 'key': u'has_config_push_ability',
               'value': u'true'},
             { 'key': u'has_thick_extent_ability',
               'value': u'true'},
             { 'key': u'host_data_ip',
               'value': u''},
             { 'key': u'ip',
               'value': u'10.0.20.50'},
             { 'key': u'machine_id',
               'value': u'1ad7ec12-5f34-11ed-9699-5254001b0267'},
             { 'key': u'port',
               'value': u'10201'},
             { 'key': u'sec_data_ip',
               'value': u'192.168.20.36'},
             { 'key': u'sec_valid',
               'value': u'true'},
             { 'key': u'zone',
               'value': u'default'}],
  'lease_expire_ns': 777738098323556L,
  'session_epoch': { 'epoch': 1814861099L,
                     'uuid': u'4b1b1ef7-0326-4950-abb5-e520612311e2'}}
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `has_config_push_ability` | 是否能够上传 iSCSI config。 |
| `ip` | 存储网络 IP。 |
| `port` | 存储网络端口。 |
| `sec_data_ip` | 次级网络 IP。 |
| `sec_valid` | 是否支持通过次级网络进行数据链接。 |
| `zone` | 所属可用域。 |

## 查看会话处理的 iSCSI 连接信息

**操作方法**

在集群任一节点执行如下命令，查看会话处理的 iSCSI 连接信息：

`zbs-meta session list_iscsi_conn [session_id]`

`session_id` 为 session 的 UUID。若不指定此参数，输出结果将展示所有连接信息。

**输出示例**

```
Initiator                                                                                           Initiator IP    Target ID                               Client Port  Session ID                              CID  Transport Type
--------------------------------------------------------------------------------------------------  --------------  ------------------------------------  -------------  ------------------------------------  -----  ----------------
iqn.1994-05.com.redhat:3d529e7b469                                                                  10.0.18.155     4a461048-a6a6-4156-9530-3f385a3bb35a          34386  59688f04-57cb-4f3e-b716-f3752b67a856      3  TCP
iqn.1994-05.com.redhat:c83cb51956cd                                                                 10.1.18.75      62901dbb-df26-4635-9975-0c617e7e5177          33472  59688f04-57cb-4f3e-b716-f3752b67a856      3  TCP
iqn.1994-05.com.redhat:e389825c840                                                                  10.0.18.212     01f2e1e3-1984-45b2-b1a2-8087cf2c1653          43534  59688f04-57cb-4f3e-b716-f3752b67a856      3  TCP
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Initiator` | iSCSI 客户端。 |
| `Initiator IP` | iSCSI 客户端 IP 地址。 |
| `Target ID` | iSCSI 协议对象 target ID，对应 ZBS 里 pool 的概念。 |
| `Session ID` | 管理这个 iSCSI 连接的 `session ID`。 |
| `CID` | iSCSI 连接 ID。 |
| `Transport Type` | 传输协议类型。 |

## 查看当前重路由功能的设置

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta reroute show`

**输出示例**

```
enable_reroute: true

enable_secondary_data_channel: true
```

## 更新重路由功能的设置

**操作方法**

在集群任一节点执行如下命令，更新重路由功能的设置：

`zbs-meta reroute update [--enable_reroute {true|false}] [--enable_secondary_data_channel {true|false}]`

| 参数 | 说明 |
| --- | --- |
| `--enable_reroute` | 是否启用 I/O 重定向服务。 |
| `--enable_secondary_data_channel` | 是否使用管理网络作为备用数据链路。 |

**输出说明**

执行成功无输出。

---

## 管理集群 > 查看任务运行状态

# 查看任务运行状态

## 查看任务执行者情况

**操作方法**

执行如下命令查看任务执行者的情况：

`zbs-task runner list`

**输出示例**

```
ip            port
----------  ------
10.0.20.50   10601
10.0.20.51   10601
10.0.20.52   10601
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `ip` | 任务执行者的 IP 地址。 |
| `port` | 任务执行者的 RPC 端口。 |

## 查看运行中或已结束的任务

**操作方法**

使用如下命令查看当前运行中或已结束的任务：

`zbs-task task list_by_status {unfinished|finished} [--task_type <task_type_value>]`

| 参数 | 说明 |
| --- | --- |
| `--task_type <task_type_value>` | `task_type_value` 取值可为以下任何一种：   - `storage_pool`：存储池 - `backup`：备份 - `restore`：取回 - `rsync`：同步 - `copy_volume`：复制 |

**输出示例**

```
No task found
```

---

## 管理节点 > 收集节点的软硬件信息

# 收集节点的软硬件信息

**操作方法**

在集群节点执行如下命令，收集该节点的硬件信息和软件信息。

`zbs-node collect_node_info`

**输出示例**

```
2021-07-20 18:58:16,332 [56252] [INFO] Start collecting node info
2021-07-20 18:58:19,103 [56252] [WARNING] product name and/or sn is not as defined format
2021-07-20 18:58:19,105 [56252] [WARNING] not ready for topo. please check json configuration, create racks and/or bricks, if necessary, and move nodes into bricks from fisheye
```

---

## 管理节点 > 部署 SSH Key

# 部署 SSH Key

在集群部署或升级阶段会执行该命令进行同一集群中所有节点的 SSH 免密登录配置，配置用户为 `smartx`。若集群节点中 `smartx` 用户无法通过 SSH 进行免密登录到其他节点，可以执行该命令进行 SSH key 生成动作。

**操作方法**

在集群任一节点执行如下命令：

`zbs-deploy-manage deploy_ssh_key`

**输出说明**

输出配置 SSH Key 过程。当输出 `Deploy SSH Key Success` 代表配置成功。

---

## 管理节点 > 关闭与重启节点

# 关闭与重启节点

对一个或多个节点执行关机或重启操作。

> **注意：**
>
> 在对节点进行关机和重启操作前，请务必登录 CloudTower，进入集群的虚拟机列表，确认目标主机不存在虚拟机，或者虚拟机处于**关机**状态。

**操作方法**

`zbs-cluster shutdown_hosts [--hosts <HOST_IPS> --action {reboot|poweroff}] [--network {mgt|storage} --reason <TEXT>]`

| 参数 | 说明 | 示例 |
| --- | --- | --- |
| `--hosts` | 目标节点的 IP 地址。若同时要对多个节点操作，可输入多个节点的 IP 地址，不同 IP 以英文逗号 `,` 分开。如果要对所有节点进行关机，可使用 `all` 代替所有主机 IP。 | `--hosts 10.172.11.111,10.172.11.112` |
| `--action` | 电源管理行为。`reboot`表示重启主机；`poweroff` 表示关闭主机电源。 | `--action reboot` |
| `--network` | 输入节点 IP 地址对应的网络类型。`mgt` 表示管理网络，`storage` 表示存储网络。默认为存储网络。 | `--network mgt` |
| `--reason` | 关机或重启的原因，该内容会被记录在审计日志中。 | `--reason upgrade kernel` |

**操作示例**

- 重启一个节点。

  ```
  $ zbs-cluster shutdown_hosts --hosts=10.172.20.111 --action=reboot --network=storage
  ```
- 关闭多个节点

  ```
  $ zbs-cluster shutdown_hosts --hosts=192.168.22.111，192.168.22.112 --action=poweroff --network=mgt
  ```
- 关闭整个集群

  ```
  $ zbs-cluster shutdown_hosts --hosts=all --action=poweroff --network=storage
  ```

**输出示例**

```
[smartx@scvm-22-211 17:23:37 ~]$sudo zbs-cluster shutdown_hosts --hosts=10.168.22.112 --action=reboot
2023-04-17 17:24:06,241 cmdline.py 169 [2697] [INFO]
2023-04-17 17:24:06,251 cmdline.py 169 [2697] [INFO] PLAY [10.168.22.112] ***********************************************************
2023-04-17 17:24:06,252 cmdline.py 169 [2697] [INFO]
2023-04-17 17:24:06,253 cmdline.py 169 [2697] [INFO] TASK [fail] ********************************************************************
2023-04-17 17:24:06,312 cmdline.py 169 [2697] [INFO] skipping: [10.168.22.112]
2023-04-17 17:24:06,313 cmdline.py 169 [2697] [INFO]
2023-04-17 17:24:06,313 cmdline.py 169 [2697] [INFO] TASK [gather host ip address facts] ********************************************
2023-04-17 17:24:10,728 cmdline.py 169 [2697] [INFO] ok: [10.168.22.112]
2023-04-17 17:24:10,728 cmdline.py 169 [2697] [INFO]
2023-04-17 17:24:10,728 cmdline.py 169 [2697] [INFO] TASK [set_fact] ****************************************************************
2023-04-17 17:24:10,793 cmdline.py 169 [2697] [INFO] ok: [10.168.22.112]
2023-04-17 17:24:10,793 cmdline.py 169 [2697] [INFO]
2023-04-17 17:24:10,793 cmdline.py 169 [2697] [INFO] TASK [stop vipservice for migrate vip to other hosts before shutdown] **********
2023-04-17 17:24:14,663 cmdline.py 169 [2697] [INFO] changed: [10.168.22.112]
2023-04-17 17:24:14,664 cmdline.py 169 [2697] [INFO]
2023-04-17 17:24:14,664 cmdline.py 169 [2697] [INFO] TASK [stop non-zbs services] ***************************************************
2023-04-17 17:25:35,378 cmdline.py 169 [2697] [INFO] changed: [10.168.22.112]
2023-04-17 17:25:35,379 cmdline.py 169 [2697] [INFO]
2023-04-17 17:25:35,379 cmdline.py 169 [2697] [INFO] TASK [gather running vm list on the target host] *******************************
2023-04-17 17:25:38,037 cmdline.py 169 [2697] [INFO] fatal: [10.168.22.112]: FAILED! => {"changed": true, "cmd": ["timeout", "-k", "300", "300", "virsh", "list", "--all", "--state-running", "--uuid"], "delta": "0:00:00.028824", "end": "2023-04-17 17:25:37.586861", "msg": "non-zero return code", "rc": 1, "start": "2023-04-17 17:25:37.558037", "stderr": "error: failed to connect to the hypervisor\nerror: Failed to connect socket to '/var/run/libvirt/libvirt-sock': No such file or directory", "stderr_lines": ["error: failed to connect to the hypervisor", "error: Failed to connect socket to '/var/run/libvirt/libvirt-sock': No such file or directory"], "stdout": "", "stdout_lines": []}
2023-04-17 17:25:38,037 cmdline.py 169 [2697] [INFO] ...ignoring
2023-04-17 17:25:38,037 cmdline.py 169 [2697] [INFO]
2023-04-17 17:25:38,037 cmdline.py 169 [2697] [INFO] TASK [stop all running vm by virsh shutdown] ***********************************
2023-04-17 17:25:38,076 cmdline.py 169 [2697] [INFO] skipping: [10.168.22.112]
2023-04-17 17:25:38,076 cmdline.py 169 [2697] [INFO]
2023-04-17 17:25:38,076 cmdline.py 169 [2697] [INFO] TASK [virsh shutdown result] ***************************************************
2023-04-17 17:25:38,132 cmdline.py 169 [2697] [INFO] ok: [10.168.22.112] => {
2023-04-17 17:25:38,133 cmdline.py 169 [2697] [INFO]     "msg": {
2023-04-17 17:25:38,133 cmdline.py 169 [2697] [INFO]         "changed": false,
2023-04-17 17:25:38,133 cmdline.py 169 [2697] [INFO]         "skip_reason": "Conditional result was False",
2023-04-17 17:25:38,133 cmdline.py 169 [2697] [INFO]         "skipped": true
2023-04-17 17:25:38,133 cmdline.py 169 [2697] [INFO]     }
2023-04-17 17:25:38,133 cmdline.py 169 [2697] [INFO] }
2023-04-17 17:25:38,133 cmdline.py 169 [2697] [INFO]
2023-04-17 17:25:38,133 cmdline.py 169 [2697] [INFO] TASK [stop all running vm by virsh destroy] ************************************
2023-04-17 17:25:38,171 cmdline.py 169 [2697] [INFO] skipping: [10.168.22.112]
2023-04-17 17:25:38,171 cmdline.py 169 [2697] [INFO]
2023-04-17 17:25:38,171 cmdline.py 169 [2697] [INFO] TASK [virsh destroy result] ****************************************************
2023-04-17 17:25:38,231 cmdline.py 169 [2697] [INFO] ok: [10.168.22.112] => {
2023-04-17 17:25:38,231 cmdline.py 169 [2697] [INFO]     "msg": {
2023-04-17 17:25:38,231 cmdline.py 169 [2697] [INFO]         "changed": false,
2023-04-17 17:25:38,231 cmdline.py 169 [2697] [INFO]         "skip_reason": "Conditional result was False",
2023-04-17 17:25:38,232 cmdline.py 169 [2697] [INFO]         "skipped": true
2023-04-17 17:25:38,232 cmdline.py 169 [2697] [INFO]     }
2023-04-17 17:25:38,232 cmdline.py 169 [2697] [INFO] }
2023-04-17 17:25:38,232 cmdline.py 169 [2697] [INFO]
2023-04-17 17:25:38,232 cmdline.py 169 [2697] [INFO] TASK [umount nfs mount point] **************************************************
2023-04-17 17:25:40,979 cmdline.py 169 [2697] [INFO] changed: [10.168.22.112]
2023-04-17 17:25:40,979 cmdline.py 169 [2697] [INFO]
2023-04-17 17:25:40,979 cmdline.py 169 [2697] [INFO] TASK [stop all smtxos system services] *****************************************
2023-04-17 17:25:59,166 cmdline.py 169 [2697] [INFO] changed: [10.168.22.112]
2023-04-17 17:25:59,166 cmdline.py 169 [2697] [INFO]
2023-04-17 17:25:59,167 cmdline.py 169 [2697] [INFO] TASK [shutdown system by reboot on 10.168.22.112] ******************************
2023-04-17 17:26:03,978 cmdline.py 169 [2697] [INFO] fatal: [10.168.22.112]: FAILED! => {"changed": false, "module_stderr": "Connection to 10.168.22.112 closed.\r\n", "module_stdout": "/bin/sh: line 1: 25671 Terminated              sudo -H -S -n -u root /bin/sh -c 'echo BECOME-SUCCESS-tarxkpmgivpmzdmewmkzqjbjfjlyjhbf ; /usr/bin/python /home/smartx/.ansible/tmp/ansible-tmp-1681723559.5943196-3544-107651429146572/AnsiballZ_command.py'\r\n", "msg": "MODULE FAILURE\nSee stdout/stderr for the exact error", "rc": 143}
2023-04-17 17:26:03,978 cmdline.py 169 [2697] [INFO] ...ignoring
2023-04-17 17:26:03,978 cmdline.py 169 [2697] [INFO]
2023-04-17 17:26:03,978 cmdline.py 169 [2697] [INFO] TASK [wait for system shutdown] ************************************************
2023-04-17 17:26:09,563 cmdline.py 169 [2697] [INFO] ok: [10.168.22.112 -> localhost]
2023-04-17 17:26:09,564 cmdline.py 169 [2697] [INFO]
2023-04-17 17:26:09,564 cmdline.py 169 [2697] [INFO] TASK [wait for system fishished reboot] ****************************************
2023-04-17 17:27:32,801 cmdline.py 169 [2697] [INFO] FAILED - RETRYING: [10.168.22.112 -> localhost]: wait for system fishished reboot (120 retries left).
2023-04-17 17:27:32,802 cmdline.py 169 [2697] [INFO] FAILED - RETRYING: [10.168.22.112 -> localhost]: wait for system fishished reboot (119 retries left).
2023-04-17 17:27:32,802 cmdline.py 169 [2697] [INFO] FAILED - RETRYING: [10.168.22.112 -> localhost]: wait for system fishished reboot (118 retries left).
2023-04-17 17:27:32,802 cmdline.py 169 [2697] [INFO] FAILED - RETRYING: [10.168.22.112 -> localhost]: wait for system fishished reboot (117 retries left).
2023-04-17 17:27:32,802 cmdline.py 169 [2697] [INFO] FAILED - RETRYING: [10.168.22.112 -> localhost]: wait for system fishished reboot (116 retries left).
2023-04-17 17:27:32,802 cmdline.py 169 [2697] [INFO] ok: [10.168.22.112 -> localhost]
2023-04-17 17:27:32,802 cmdline.py 169 [2697] [INFO]
2023-04-17 17:27:32,803 cmdline.py 169 [2697] [INFO] TASK [shutdown system by reboot on ansible host] *******************************
2023-04-17 17:27:32,858 cmdline.py 169 [2697] [INFO] skipping: [10.168.22.112]
2023-04-17 17:27:32,858 cmdline.py 169 [2697] [INFO]
2023-04-17 17:27:32,858 cmdline.py 169 [2697] [INFO] PLAY RECAP *********************************************************************
2023-04-17 17:27:32,859 cmdline.py 169 [2697] [INFO] 10.168.22.112              : ok=12   changed=5    unreachable=0    failed=0    skipped=4    rescued=0    ignored=2
2023-04-17 17:27:32,859 cmdline.py 169 [2697] [INFO]
2023-04-17 17:27:34,063 cluster.py 479 [2697] [INFO] Reboot 10.168.22.112 hosts successfully
```

**输出说明**

显示节点关机或重启的进度和结果。

---

## 管理节点 > 主机维护模式相关操作（ELF 平台）

# 主机维护模式相关操作（ELF 平台）

## 查看虚拟机迁移历史

**操作方法**

在节点上执行如下命令：

`zbs-node evict list`

**输出示例**

```
evict_uuid: 1b39dc80-486b-4122-8da5-a699dc774465         operated_time: 2022-11-24 16:38:31      live_migrate_vm_count: 2
evict_uuid: abb46105-f346-453b-9228-57ac69b3cd99         operated_time: 2022-11-24 16:39:58      live_migrate_vm_count: 2
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `evict_uuid` | 迁移任务 UUID。 |
| `operated_time` | 迁移动作完成时间。 |
| `live_migrate_vm_count` | 迁移虚拟机数量。 |

## 将节点上的虚拟机迁移至其他节点

对于开启了 Boost 模式的集群，若需升级 procurator，在升级完成后需要手动将节点中的节点中的虚拟机迁移至其他节点，之后再迁回原虚拟机，以使得虚拟机相关的二进制文件生效。

**操作方法**

在节点上执行如下命令，将当前节点上所有运行中的虚拟机迁移至其他节点：

`$zbs-node evict migrate_vms [--data_ip <DATA_IP>]`

| 参数 | 说明 |
| --- | --- |
| `--data_ip <DATA_IP>` | 目标节点的存储网络 IP 地址。 |

**输出示例**

```
$zbs-node evict migrate_vms --data_ip 10.192.210.40
2022-11-24 16:38:25,562 client.py 53 [99265] [INFO] Create channel to 127.0.0.1:9999
2022-11-24 16:38:26,539 connectionpool.py 203 [99265] [INFO] Starting new HTTP connection (1): 127.0.0.1
2022-11-24 16:38:27,427 connectionpool.py 383 [99265] [DEBUG] "GET /api/v2/vms?count=50&skip_page=1&filter_criteria=node_ip=10.192.210.40 HTTP/1.1" 200 23837
2022-11-24 16:38:27,430 elf.py 61 [99265] [INFO] Get vms successfully.
...
2022-11-24 16:38:31,343 elf.py 30 [99265] [INFO] Try migrate vms successfully.
...
2022-11-24 16:38:42,212 vm_operate_service.py 423 [99265] [INFO] [VMOperateService] live_migrate_vm succeed
2022-11-24 16:38:42,264 vm_operate_service.py 456 [99265] [INFO]
vm_name: CentOS-1002-clone02     vm_uuid: e52aaa4e-09fc-4780-9973-4e11b3d1c684   source_host_ip: 10.192.210.40   target_host_ip: 10.192.210.41   state: done
vm_name: CentOS-1003-clone       vm_uuid: 95485c57-1755-484d-bd83-172aaeeafcbd   source_host_ip: 10.192.210.40   target_host_ip: 10.192.210.42   state: pending

2022-11-24 16:38:42,264 vm_operate_service.py 322 [99265] [INFO] vm operate uuid 1b39dc80-486b-4122-8da5-a699dc774465
...
2022-11-24 16:38:53,472 vm_operate_service.py 423 [99265] [INFO] [VMOperateService] live_migrate_vm succeed
2022-11-24 16:38:53,492 vm_operate_service.py 456 [99265] [INFO]
vm_name: CentOS-1002-clone02     vm_uuid: e52aaa4e-09fc-4780-9973-4e11b3d1c684   source_host_ip: 10.192.210.40   target_host_ip: 10.192.210.41   state: done
vm_name: CentOS-1003-clone       vm_uuid: 95485c57-1755-484d-bd83-172aaeeafcbd   source_host_ip: 10.192.210.40   target_host_ip: 10.192.210.42   state: done

2022-11-24 16:38:53,492 vm_operate_service.py 439 [99265] [INFO] [VMOperateService] live_migrate_vms succeed
```

**输出说明**

显示迁移日志，具体迁移进度和迁移结果。

## 将虚拟机迁回原节点

**操作方法**

在节点上执行如下命令，将迁移任务包含的所有虚拟机迁回原节点：

`zbs-node evict migrate_back_vms [--evict_uuid <EVICT_UUID>] [--data_ip <DATA_IP>]`

| 参数 | 说明 |
| --- | --- |
| `--evict_uuid <EVICT_UUID>` | 迁移任务 UUID。 |
| `--data_ip <DATA_IP>` | 迁回节点的存储网络 IP 地址。 |

**输出示例**

```
$zbs-node evict migrate_back_vms --evict_uuid f2bf03da-4bec-4165-861d-9026199ca16b --data_ip 10.192.210.40
2022-11-24 16:55:16,307 vm_operate_service.py 239 [134050] [INFO] [VMOperateService] calc_vms_for_exit_mt_mode
...
2022-11-24 16:55:17,267 elf.py 68 [134050] [INFO] Get vm successfully.
...
2022-11-24 16:55:33,337 vm_operate_service.py 423 [134050] [INFO] [VMOperateService] live_migrate_vm succeed
2022-11-24 16:55:33,387 vm_operate_service.py 456 [134050] [INFO]
vm_name: CentOS-1003-clone       vm_uuid: 95485c57-1755-484d-bd83-172aaeeafcbd   source_host_ip: 10.192.210.42   target_host_ip: 10.192.210.40   state: done
vm_name: CentOS-02       vm_uuid: ac16c9a9-4322-4fbe-a34a-3ce8176df3cd   source_host_ip: 10.192.210.42   target_host_ip: 10.192.210.40   state: pending

2022-11-24 16:55:33,388 vm_operate_service.py 322 [134050] [INFO] vm operate uuid 6404fcb3-66df-4324-9d26-a3b64f9667b8
2022-11-24 16:55:33,388 vm_operate_service.py 62 [134050] [INFO] [VMOperateService] check_job
2022-11-24 16:55:33,436 vm_operate_service.py 407 [134050] [INFO] [VMOperateService] live_migrate_vm
2022-11-24 16:55:33,437 vm_operate_service.py 413 [134050] [INFO] [VMOperateService] live_migrate_vm vm_uuid: ac16c9a9-4322-4fbe-a34a-3ce8176df3cd, target_host_ip: 10.192.210.40
...
2022-11-24 16:55:49,975 vm_operate_service.py 423 [134050] [INFO] [VMOperateService] live_migrate_vm succeed
2022-11-24 16:55:50,019 vm_operate_service.py 456 [134050] [INFO]
vm_name: CentOS-1003-clone       vm_uuid: 95485c57-1755-484d-bd83-172aaeeafcbd   source_host_ip: 10.192.210.42   target_host_ip: 10.192.210.40   state: done
vm_name: CentOS-02       vm_uuid: ac16c9a9-4322-4fbe-a34a-3ce8176df3cd   source_host_ip: 10.192.210.42   target_host_ip: 10.192.210.40   state: done

2022-11-24 16:55:50,020 vm_operate_service.py 439 [134050] [INFO] [VMOperateService] live_migrate_vms succeed
```

**输出说明**

输出迁移日志、具体迁移进度和迁移结果。

---

## 管理节点 > 将仲裁节点的管理 IP 同步给其他节点

# 将仲裁节点的管理 IP 同步给其他节点

当仲裁节点新配置了管理 IP 或者更新了管理 IP 后，需将仲裁节点管理 IP 同步到集群其他节点。

**操作方法**

在仲裁节点执行如下命令，将管理 IP 同步至其他节点，其中 `witness_mgt_ip` 为仲裁节点的管理 IP。

`zbs-cluster sync_witness_mgt_ip <witness_mgt_ip>`

**输出示例**

```
$ zbs-cluster sync_witness_mgt_ip 192.168.31.69
2023-11-20 18:44:05,613 sync_cluster.py 21 [27711] [INFO] no changes, cluster ips up-to-date
2023-11-20 18:44:05,622 ansible_manager.py 160 [27711] [INFO] Exec cmd with ansible: ansible -i /etc/zbs/inventory all -m raw -a 'echo 192.168.31.69 > /etc/zbs/witness_mgt_ip' --ssh-common-args='-o StrictHostKeyChecking=no'
2023-11-20 18:44:05,622 cmdline.py 119 [27711] [INFO] run cmd: ansible -i /etc/zbs/inventory all -m raw -a 'echo 192.168.31.69 > /etc/zbs/witness_mgt_ip' --ssh-common-args='-o StrictHostKeyChecking=no'
2023-11-20 18:44:10,722 cluster.py 582 [27711] [INFO] Sync witness mgt ip 192.168.31.69 to all nodes successfully
```

**输出说明**

输出同步过程。若输出 `Sync witness mgt ip xx.xx.xx.xx to all nodes successfully` 表示 IP 同步已成功。

---

## 管理节点 > 管理时间同步

# 管理时间同步

## 查询节点的 NTP 同步状态

**操作方法**

在集群任一节点执行如下命令：

`ntpm server show`

**输出示例**

![](https://cdn.smartx.com/internal-docs/assets/d15aec0b/cli_guide_02.png)

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `NODE DATAIP` | 节点的存储 IP。 |
| `NODE PRIORITY` | 节点的选主优先级。由内部 NTP 服务器产生。优先级最高的节点优先当选 `Leader`。 |
| `NODE ROLE` | 集群中某个节点的身份。`Leader` 表示该节点选主成功，充当内部 NTP 服务器；`Follower` 表示该节点同步 `Leader` 节点的时间；`CurrentNode` 表示当前执行命令的节点。 |
| `NTP ADDR` | 进行同步的 NTP 服务器地址，可以有多个。如果为 `localhost`，表示该节点未设置 NTP 服务器，采用自身的时钟。 |
| `NTP STRATUM` | NTP 服务器所属的层级。数值越小表示优先级越高，时间越精确。 |
| `NTP STATE` | NTP 服务器状态。`sync` 表示当前节点正在和 NTP 服务器进行时间同步；`falseticker` 表示该 NTP 服务器的时间不可信。 |
| `NTP OFFSET` | 当前主机与 NTP 服务器的时间偏移量。 |

## 将节点时间与 NTP 服务器同步

当集群内某个节点的时间和 NTP 服务器有较大偏移时，需将该节点的时间和外部 NTP 服务器或 NTP Leader 的时间进行同步。

**操作方法**

在时间不准确的节点执行如下命令，将时间和外部 NTP 服务器或 NTP Leader 的时间进行同步：

`zbs-node sync_time`

**输出示例**

```
2023-11-09 14:08:48,351 node.py 640 [2509628] [INFO] sync node ntp to internal ntp leader successfully
```

## 将集群所有节点时间与 NTP 服务器同步

当集群使用内部 NTP 服务或配置外部 NTP 服务器，如果集群整体时间偏移量较大，将所有节点的时间同步到外部 NTP 服务器或 NTP Leader 的时间。

**操作方法**

在任意节点执行如下命令，同步时间到外部 NTP 服务器的时间：

`zbs-cluster sync_time`

**输出示例**

输出同步过程。

## 查询集群可用的时区列表

查询当前 SMTX OS 支持的时区列表，便于选择合适的时区。

**操作方法**

在集群任一节点执行如下命令，查看全部可用时区：

`zbs-cluster get_available_timezones`

若仅需查看某一大洲或区域下的时区，可增加过滤参数，例如：

`zbs-cluster get_available_timezones --zone_filter Asia`

**输出说明**

输出支持的时区名称列表，例如 `Asia/Shanghai`、`America/Los_Angeles` 等。

## 查看集群当前时区设置

**操作方法**

在集群任一节点执行如下命令，查看当前集群各节点设置的时区信息：

`zbs-cluster show_timezone`

**输出说明**

输出集群内各节点当前配置的时区信息。若各节点时区不一致，可通过[设置集群时区](#%E8%AE%BE%E7%BD%AE%E9%9B%86%E7%BE%A4%E6%97%B6%E5%8C%BA)命令统一所有节点的时区。

## 设置集群时区

**操作方法**

在集群任一节点执行如下命令，将集群所有节点时区设置为指定时区，可通过[查询集群可用的时区列表](#%E6%9F%A5%E8%AF%A2%E9%9B%86%E7%BE%A4%E5%8F%AF%E7%94%A8%E7%9A%84%E6%97%B6%E5%8C%BA%E5%88%97%E8%A1%A8)命令获取可设置的时区。

例如设置为 `Asia/Shanghai`：

`zbs-cluster set_timezone --timezone Asia/Shanghai`

**输出说明**

输出设置集群各节点时区的结果。

**后续操作**

为确保集群所有服务在新时区下正常运行，设置集群时区后需完成集群下线再上线的操作，详情请参考《集群上下线工具用户指南》，若业务不允许或环境不支持集群整体下线和上线，请将集群内所有节点逐个进入维护模式并重启节点，详情请参考《SMTX OS 运维指南》。

---

## 管理节点 > 收集节点的硬件信息

# 收集节点的硬件信息

## 收集节点的 PCI 设备信息

**操作方法**

执行如下命令，收集节点的 PCI 设备信息。

`zbs-node collect_pci_device`

**输出说明**

若存在 PCI 设备信息更新，输出对应设备的信息，否则无相关输出。

## 收集节点的网卡设备信息

**操作方法**

执行如下命令，收集节点的网卡设备信息。

`zbs-node collect_nic_device`

**输出说明**

若存在网卡设备信息更新，输出对应设备的信息，否则无相关输出。

## 收集节点的 GPU 设备信息

**操作方法**

执行如下命令，收集节点的 GPU 设备信息。

`zbs-node collect_gpu_device`

**输出说明**

若存在 GPU 设备信息更新，输出对应设备的信息，否则无相关输出。

## 收集节点的硬件 RAID 信息

**操作方法**

执行如下命令，收集节点的硬件 RAID 信息。

`zbs-node collect_hardware_raid`

**输出说明**

若存在硬件 RAID 信息更新，输出对应设备的信息，否则无相关输出。

## 收集节点的 USB 信息

**操作方法**

执行如下命令，收集节点的 USB 信息。

`zbs-node collect_usb_device`

**输出说明**

若存在 USB 设备信息更新，输出对应设备的信息，否则无相关输出。

## 收集节点的所有类型设备的信息

**操作方法**

执行如下命令，收集节点的 PCI、网卡、GPU、USB 和硬件 RAID 等设备的信息。

`zbs-node collect_all_device`

**输出说明**

若存在设备信息更新，输出对应设备的信息，否则无相关输出。

---

## 管理节点 > 管理常驻缓存

# 管理常驻缓存

## 获取单个物理盘池的常驻缓存信息

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta chunk get_prs_ratio <cid>`

**输出示例**

```
--------------  ------------
Chunk ID        9
IP              10.255.0.104
Ratio           10.0%
Planned PRS     39.62 GiB
Allocated PRS   38.00 GiB
Downgraded PRS  0.00 B
--------------  ------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Chunk ID` | 物理盘池的 chunk ID。 |
| `IP` | 物理盘池所属的节点的存储网络 IP。 |
| `Ratio` | 物理盘池的缓存预留比例。 |
| `Planned PRS` | 物理盘池的预期缓存预留空间的大小。 |
| `Allocated PRS` | 物理盘池的已使用缓存预留数据的大小。 |
| `Downgraded PRS` | 物理盘池降级的缓存预留数据的大小。 |

## 获取集群所有物理盘池的常驻缓存信息

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta cluster list_prs_info`

**输出示例**

```
  Chunk ID  IP            Ratio    Planned PRS    Allocated PRS    Downgraded PRS
----------  ------------  -------  -------------  ---------------  ----------------
         1  10.13.111.13  0.0%     0.00 B         0.00 B           0.00 B
         2  10.13.111.11  0.0%     0.00 B         0.00 B           0.00 B
         3  10.13.111.13  0.0%     0.00 B         0.00 B           0.00 B
         4  10.13.111.12  0.0%     0.00 B         0.00 B           0.00 B
         5  10.13.111.11  0.0%     0.00 B         0.00 B           0.00 B
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Chunk ID` | 物理盘池的 chunk ID。 |
| `IP` | 物理盘池所属的节点的存储网络 IP。 |
| `Ratio` | 物理盘池的缓存预留比例。 |
| `Planned PRS` | 物理盘池的预期缓存预留空间的大小。 |
| `Allocated PRS` | 物理盘池的已使用缓存预留数据的大小。 |
| `Downgraded PRS` | 物理盘池降级的缓存预留数据的大小。 |

## 设置单个物理盘池的常驻缓存比例

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta chunk set_prs_ratio <cid> <ratio>`

`<ratio>` 最大值为 75%。

**输出说明**

执行成功无输出。

---

## 管理节点 > 查看节点 watchdog 日志

# 查看节点 watchdog 日志

**操作**

在节点上执行如下命令，查看本节点是否触发了系统只读事件，如果有，则会显示第一次判定的时间和 kill 的服务名称，如果没有则会显示没有触发系统只读事件：

`zbs-tool watchdog show_log [--raw]`

| 参数 | 说明 |
| --- | --- |
| `--raw` | 指定则展示日志原文。 |

**输出示例**

```
Filesystem did not trigger readonly event
```

**输出说明**

本节点没有触发系统只读事件。

---

## 管理节点 > 管理 CPU 安全补丁

# 管理 CPU 安全补丁

## 开启与关闭节点 CPU 安全补丁

**操作方法**

在节点上执行如下命令，开启或关闭 CPU 安全补丁：

`zbs-node grub cpu_vulnerabilities_patches`

| 参数 | 说明 |
| --- | --- |
| `--disable` | 关闭 CPU 安全补丁。 |
| `--enable` | 开启 CPU 安全补丁。 |

> **注意**：
>
> 如果想要使配置生效，需要重启主机，可通过 CloudTower 对主机进行重启。

**输出示例**

```
$ zbs-node  grub cpu_vulnerabilities_patches --disable
2024-07-08 14:59:41,005 node.py 1577 [90899] [INFO] disable cpu vulnerabilities patches
2024-07-08 14:59:41,008 grub2_manager.py 185 [90899] [INFO] Will add ['noibrs', 'noibpb', 'nopti', 'nospectre_v2', 'nospectre_v1', 'l1tf=off', 'nosp
ec_store_bypass_disable', 'no_stf_barrier', 'mds=off', 'tsx_async_abort=off', 'mitigations=off', 'tsx=on'] to grub cmdline
2024-07-08 14:59:41,008 grub2_manager.py 86 [90899] [INFO] Start update grub file /etc/default/grub
2024-07-08 14:59:41,009 grub2_manager.py 93 [90899] [INFO] Old config:
GRUB_CMDLINE_LINUX="intel_idle.max_cstate=0 processor.max_cstate=1 intel_pstate=disable transparent_hugepage=never slab_nomerge console=ttyS0,115200
n8 console=tty0 precise_iostat=0 tsx=on megaraid_sas.scmd_timeout=20 nvme_core.multipath=0 crashkernel=512M spectre_v2=retpoline rd.md.uuid=92204985
:309b4907:5e172ae5:3ce75de7   nf_conntrack.hashsize=262144"

2024-07-08 14:59:41,009 grub2_manager.py 97 [90899] [INFO] New config:
GRUB_CMDLINE_LINUX="intel_idle.max_cstate=0 processor.max_cstate=1 intel_pstate=disable transparent_hugepage=never slab_nomerge console=ttyS0,115200
n8 console=tty0 precise_iostat=0 tsx=on megaraid_sas.scmd_timeout=20 nvme_core.multipath=0 crashkernel=512M spectre_v2=retpoline rd.md.uuid=92204985
:309b4907:5e172ae5:3ce75de7 nf_conntrack.hashsize=262144 noibrs noibpb nopti nospectre_v2 nospectre_v1 l1tf=off nospec_store_bypass_disable no_stf_b
arrier mds=off tsx_async_abort=off mitigations=off"
2024-07-08 14:59:41,010 grub2_manager.py 99 [90899] [INFO] Replace /etc/default/grub with new generated config file
2024-07-08 14:59:41,010 grub2_manager.py 102 [90899] [INFO] Finish update grub file /etc/default/grub
2024-07-08 14:59:41,011 grub2_manager.py 68 [90899] [INFO] Start generate boot config /boot/grub2/grub.cfg
2024-07-08 14:59:41,011 cmdline.py 119 [90899] [INFO] run cmd: grub2-mkconfig -o /boot/grub2/grub.cfg.bak
2024-07-08 14:59:41,665 grub2_manager.py 78 [90899] [INFO] Replace /boot/grub2/grub.cfg with new generated config file
2024-07-08 14:59:41,666 grub2_manager.py 81 [90899] [INFO] Finish generate boot config /boot/grub2/grub.cfg
2024-07-08 14:59:41,666 node.py 1582 [90899] [INFO] Done
```

**输出说明**

显示配置过程，以及配置结果。

## 开启与关闭集群所有节点的 CPU 安全补丁

**操作方法**

在集群已有节点上执行如下命令，开启或关闭集群所有节点 CPU 安全补丁：

`zbs-cluster grub cpu_vulnerabilities_patches`

| 参数 | 说明 |
| --- | --- |
| `--disable` | 关闭 CPU 安全补丁。 |
| `--enable` | 开启 CPU 安全补丁。 |

> **注意**：
>
> 如果想要使配置生效，需要重启集群所有节点主机，可通过 CloudTower 对集群主机依次进行重启。

**输出示例**

```
$ zbs-cluster grub cpu_vulnerabilities_patches --disable
2024-07-08 15:23:20,452 ansible_manager.py 160 [78574] [INFO] Exec cmd with ansible: ansible -i /etc/zbs/inventory cluster -m raw -a 'zbs-node grub cpu_vulnerabilities_patches --disable' --ssh-common-args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
2024-07-08 15:23:25,770 cmdline.py 188 [78574] [INFO] 10.234.103.12 | CHANGED | rc=0 >>
2024-07-08 15:23:25,771 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,014 node.py 1577 [85073] [INFO] disable cpu vulnerabilities patches
2024-07-08 15:23:25,771 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,016 grub2_manager.py 185 [85073] [INFO] Will add ['noibrs', 'noibpb', 'nopti', 'nospectre_v2', 'nospectre_v1', 'l1tf=off', 'nospec_store_bypass_disable', 'no_stf_barrier', 'mds=off', 'tsx_async_abort=off', 'mitigations=off', 'tsx=on'] to grub cmdline
2024-07-08 15:23:25,771 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,017 grub2_manager.py 86 [85073] [INFO] Start update grub file /etc/default/grub
2024-07-08 15:23:25,771 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,017 grub2_manager.py 93 [85073] [INFO] Old config:
2024-07-08 15:23:25,771 cmdline.py 188 [78574] [INFO] GRUB_CMDLINE_LINUX="intel_idle.max_cstate=0 processor.max_cstate=1 intel_pstate=disable transparent_hugepage=never slab_nomerge console=ttyS0,115200n8 console=tty0 precise_iostat=0 tsx=on megaraid_sas.scmd_timeout=20 nvme_core.multipath=0 no5lvl rd.md.uuid=667caa2d:a65fcb77:3aca94a4:cfc30103 selinux=0 crashk
ernel=512M nf_conntrack.hashsize=262144"
2024-07-08 15:23:25,771 cmdline.py 188 [78574] [INFO]
2024-07-08 15:23:25,772 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,018 grub2_manager.py 97 [85073] [INFO] New config:
2024-07-08 15:23:25,772 cmdline.py 188 [78574] [INFO] GRUB_CMDLINE_LINUX="intel_idle.max_cstate=0 processor.max_cstate=1 intel_pstate=disable transparent_hugepage=never slab_nomerge console=ttyS0,115200n8 console=tty0 precise_iostat=0 tsx=on megaraid_sas.scmd_timeout=20 nvme_core.multipath=0 no5lvl rd.md.uuid=667caa2d:a65fcb77:3aca94a4:cfc30103 selinux=0 crashk
ernel=512M nf_conntrack.hashsize=262144 noibrs noibpb nopti nospectre_v2 nospectre_v1 l1tf=off nospec_store_bypass_disable no_stf_barrier mds=off tsx_async_abort=off mitigations=off"
2024-07-08 15:23:25,772 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,018 grub2_manager.py 99 [85073] [INFO] Replace /etc/default/grub with new generated config file
2024-07-08 15:23:25,772 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,018 grub2_manager.py 102 [85073] [INFO] Finish update grub file /etc/default/grub
2024-07-08 15:23:25,772 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,018 grub2_manager.py 68 [85073] [INFO] Start generate boot config /boot/grub2/grub.cfg
2024-07-08 15:23:25,772 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,018 cmdline.py 119 [85073] [INFO] run cmd: grub2-mkconfig -o /boot/grub2/grub.cfg.bak
2024-07-08 15:23:25,773 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:25,435 grub2_manager.py 78 [85073] [INFO] Replace /boot/grub2/grub.cfg with new generated config file
2024-07-08 15:23:25,773 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:25,435 grub2_manager.py 81 [85073] [INFO] Finish generate boot config /boot/grub2/grub.cfg
2024-07-08 15:23:25,773 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:25,435 node.py 1582 [85073] [INFO] Done
2024-07-08 15:23:25,773 cmdline.py 188 [78574] [INFO] Warning: Permanently added '10.234.103.12' (ED25519) to the list of known hosts.
2024-07-08 15:23:25,773 cmdline.py 188 [78574] [INFO] Connection to 10.234.103.12 closed.
2024-07-08 15:23:25,773 cmdline.py 188 [78574] [INFO]
2024-07-08 15:23:25,773 cmdline.py 188 [78574] [INFO] 10.234.103.13 | CHANGED | rc=0 >>
2024-07-08 15:23:25,774 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,076 node.py 1577 [77908] [INFO] disable cpu vulnerabilities patches
2024-07-08 15:23:25,774 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,079 grub2_manager.py 185 [77908] [INFO] Will add ['noibrs', 'noibpb', 'nopti', 'nospectre_v2', 'nospectre_v1', 'l1tf=off', 'nospec_store_bypass_disable', 'no_stf_barrier', 'mds=off', 'tsx_async_abort=off', 'mitigations=off', 'tsx=on'] to grub cmdline
2024-07-08 15:23:25,774 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,079 grub2_manager.py 86 [77908] [INFO] Start update grub file /etc/default/grub
2024-07-08 15:23:25,774 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,080 grub2_manager.py 93 [77908] [INFO] Old config:
2024-07-08 15:23:25,774 cmdline.py 188 [78574] [INFO] GRUB_CMDLINE_LINUX="intel_idle.max_cstate=0 processor.max_cstate=1 intel_pstate=disable transparent_hugepage=never slab_nomerge console=ttyS0,115200n8 console=tty0 precise_iostat=0 tsx=on megaraid_sas.scmd_timeout=20 nvme_core.multipath=0 no5lvl rd.md.uuid=667caa2d:a65fcb77:3aca94a4:cfc30103 selinux=0 crashk
ernel=512M nf_conntrack.hashsize=262144"
2024-07-08 15:23:25,775 cmdline.py 188 [78574] [INFO]
2024-07-08 15:23:25,775 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,080 grub2_manager.py 97 [77908] [INFO] New config:
2024-07-08 15:23:25,775 cmdline.py 188 [78574] [INFO] GRUB_CMDLINE_LINUX="intel_idle.max_cstate=0 processor.max_cstate=1 intel_pstate=disable transparent_hugepage=never slab_nomerge console=ttyS0,115200n8 console=tty0 precise_iostat=0 tsx=on megaraid_sas.scmd_timeout=20 nvme_core.multipath=0 no5lvl rd.md.uuid=667caa2d:a65fcb77:3aca94a4:cfc30103 selinux=0 crashk
ernel=512M nf_conntrack.hashsize=262144 noibrs noibpb nopti nospectre_v2 nospectre_v1 l1tf=off nospec_store_bypass_disable no_stf_barrier mds=off tsx_async_abort=off mitigations=off"
2024-07-08 15:23:25,775 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,080 grub2_manager.py 99 [77908] [INFO] Replace /etc/default/grub with new generated config file
2024-07-08 15:23:25,775 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,081 grub2_manager.py 102 [77908] [INFO] Finish update grub file /etc/default/grub
2024-07-08 15:23:25,775 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,081 grub2_manager.py 68 [77908] [INFO] Start generate boot config /boot/grub2/grub.cfg
2024-07-08 15:23:25,776 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:24,081 cmdline.py 119 [77908] [INFO] run cmd: grub2-mkconfig -o /boot/grub2/grub.cfg.bak
2024-07-08 15:23:25,776 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:25,603 grub2_manager.py 78 [77908] [INFO] Replace /boot/grub2/grub.cfg with new generated config file
2024-07-08 15:23:25,776 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:25,603 grub2_manager.py 81 [77908] [INFO] Finish generate boot config /boot/grub2/grub.cfg
2024-07-08 15:23:25,776 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:25,603 node.py 1582 [77908] [INFO] Done
2024-07-08 15:23:25,776 cmdline.py 188 [78574] [INFO] Warning: Permanently added '10.234.103.13' (ED25519) to the list of known hosts.
2024-07-08 15:23:25,776 cmdline.py 188 [78574] [INFO] Connection to 10.234.103.13 closed.
2024-07-08 15:23:25,777 cmdline.py 188 [78574] [INFO]
2024-07-08 15:23:25,777 cmdline.py 188 [78574] [INFO] 10.234.103.11 | CHANGED | rc=0 >>
2024-07-08 15:23:25,777 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:23,931 node.py 1577 [78764] [INFO] disable cpu vulnerabilities patches
2024-07-08 15:23:25,777 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:23,933 grub2_manager.py 185 [78764] [INFO] Will add ['noibrs', 'noibpb', 'nopti', 'nospectre_v2', 'nospectre_v1', 'l1tf=off', 'nospec_store_bypass_disable', 'no_stf_barrier', 'mds=off', 'tsx_async_abort=off', 'mitigations=off', 'tsx=on'] to grub cmdline
2024-07-08 15:23:25,777 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:23,934 grub2_manager.py 86 [78764] [INFO] Start update grub file /etc/default/grub
2024-07-08 15:23:25,777 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:23,935 grub2_manager.py 93 [78764] [INFO] Old config:
2024-07-08 15:23:25,777 cmdline.py 188 [78574] [INFO] GRUB_CMDLINE_LINUX="intel_idle.max_cstate=0 processor.max_cstate=1 intel_pstate=disable transparent_hugepage=never slab_nomerge console=ttyS0,115200n8 console=tty0 precise_iostat=0 tsx=on megaraid_sas.scmd_timeout=20 nvme_core.multipath=0 no5lvl rd.md.uuid=667caa2d:a65fcb77:3aca94a4:cfc30103 selinux=0 crashk
ernel=512M nf_conntrack.hashsize=262144"
2024-07-08 15:23:25,778 cmdline.py 188 [78574] [INFO]
2024-07-08 15:23:25,778 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:23,935 grub2_manager.py 97 [78764] [INFO] New config:
2024-07-08 15:23:25,778 cmdline.py 188 [78574] [INFO] GRUB_CMDLINE_LINUX="intel_idle.max_cstate=0 processor.max_cstate=1 intel_pstate=disable transparent_hugepage=never slab_nomerge console=ttyS0,115200n8 console=tty0 precise_iostat=0 tsx=on megaraid_sas.scmd_timeout=20 nvme_core.multipath=0 no5lvl rd.md.uuid=667caa2d:a65fcb77:3aca94a4:cfc30103 selinux=0 crashk
ernel=512M nf_conntrack.hashsize=262144 noibrs noibpb nopti nospectre_v2 nospectre_v1 l1tf=off nospec_store_bypass_disable no_stf_barrier mds=off tsx_async_abort=off mitigations=off"
2024-07-08 15:23:25,778 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:23,935 grub2_manager.py 99 [78764] [INFO] Replace /etc/default/grub with new generated config file
2024-07-08 15:23:25,778 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:23,936 grub2_manager.py 102 [78764] [INFO] Finish update grub file /etc/default/grub
2024-07-08 15:23:25,778 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:23,936 grub2_manager.py 68 [78764] [INFO] Start generate boot config /boot/grub2/grub.cfg
2024-07-08 15:23:25,779 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:23,937 cmdline.py 119 [78764] [INFO] run cmd: grub2-mkconfig -o /boot/grub2/grub.cfg.bak
2024-07-08 15:23:25,779 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:25,630 grub2_manager.py 78 [78764] [INFO] Replace /boot/grub2/grub.cfg with new generated config file
2024-07-08 15:23:25,779 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:25,631 grub2_manager.py 81 [78764] [INFO] Finish generate boot config /boot/grub2/grub.cfg
2024-07-08 15:23:25,779 cmdline.py 188 [78574] [INFO] 2024-07-08 15:23:25,631 node.py 1582 [78764] [INFO] Done
2024-07-08 15:23:25,779 cmdline.py 188 [78574] [INFO] Warning: Permanently added '10.234.103.11' (ED25519) to the list of known hosts.
2024-07-08 15:23:25,780 cmdline.py 188 [78574] [INFO] Connection to 10.234.103.11 closed.
2024-07-08 15:23:25,780 cmdline.py 188 [78574] [INFO]
2024-07-08 15:23:26,981 cluster.py 771 [78574] [INFO] disable cpu vulnerabilities patches successfully
```

**输出说明**

显示配置过程，以及配置结果。

---

## 管理物理盘 > 查看物理盘信息

# 查看物理盘信息

## 查看指定路径下的物理盘信息

**操作方法**

在集群节点执行如下命令，获取该节点指定路径下的物理盘信息：

`zbs-chunk query disk <path>`

**输出示例**

```
{ 'exist': True,
  'formatted': False,
  'in_use': False,
  'instance_id': 0}
Query Success
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `exist` | 物理盘是否存在。 |
| `formatted` | 物理盘是否被 chunk 格式化。 |
| `in_use` | 物理盘是否被 chunk 使用。 |

## 查询物理盘健康记录

使用物理盘盘符或者物理盘的序列号查询物理盘的健康详情。

**操作方法**

- **使用物理盘盘符查询**

  在物理盘所在的节点上执行如下命令，查询物理盘的健康详情：

  `zbs-node show_disk_status [-p] [/dev/]<disk_name> [--with_rawdata]`

  其中 `disk_name` 表示物理盘的盘符，若物理盘被探测标记为高延时盘，使用 `--with_rawdata` 选项可以输出物理盘原始的 diskstats 数据。

  **操作示例**

  以下三条命令等效：

  ```
  zbs-node show_disk_status -p /dev/sdc
  zbs-node show_disk_status /dev/sdc
  zbs-node show_disk_status sdc
  ```
- **使用物理盘序列号查询**

  在集群的任意一个节点上运行如下命令，查询物理盘的健康详情：

  `zbs-node show_disk_status -s <disk_serial>`

  其中 `disk_serial` 表示物理盘的序列号。

  **操作示例**

  `zbs-node show_disk_status -s 9XG6GTFN`

**输出示例**

```
== Base Information ==
is healthy                            : True
device name                           : /dev/sdc
bus type                              : ata
model                                 : ST91000640NS
firmware                              : SN03
disk serial                           : 9XG6GTFN
last belong to                        : 10.0.67.212
== Fault Detection ==
chunk errflag detected                : False
chunk warnflag detected               : False
chunk io error count overflow         : False
chunk checksum error count overflow   : False
iostat latency detected               : False
smart error detected                  : False
software raid faulty detected         : False
offline due to io timeout             : False
offline due to cmd abort              : False
offline due to error queue            : False
reallocated sectors count overflow    : False
== Extra Fault Detection ==
chunk io errors count                 : -
chunk checksum errors count           : -
io latency (ms)                       : -
iops                                  : -
sectors per second                    : -
bandwidth (MiB/s)                     : -
smartctl hang process                 : -
S.M.A.R.T. assessment error           : -
reallocated sectors count             : -
== S.M.A.R.T. Attributes ==
ID#   ATTRIBUTE_NAME            VALUE    THRESH   RAW             CHECK_FIELD     CHECK_THRESH    CHECK_RES
5     Reallocated_Sector_Ct     100      036      1               raw             10              True
187   Reported_Uncorrect        100      000      0               raw             0               True
188   Command_Timeout           100      000      0               value           10              True
194   Temperature_Celsius       018      000      18              raw             45              True
197   Current_Pending_Sector    100      000      0               raw             0               True
198   Offline_Uncorrectable     100      000      0               raw             0               True
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `is healthy` | 物理盘状态是否健康。 |
| `bus type` | 总线接口类型，如 `ata`、`scsi` 等。 |
| `model` | 物理盘型号。 |
| `firmware` | 固件版本。 |
| `disk path` | 物理盘路径。 |
| `disk serial` | 物理盘序列号。 |
| `trace id` | 系统用来跟踪物理盘相关状态的的标记（一般是序列号，但也可能是 nguid 等其他信息）。 |
| `controller` | 物理盘控制器所使用的驱动类型。 |
| `last belong to` | 上次所属 chunk IP。 |
| `chunk errflag detected` | 是否检测到错误状态物理盘。 |
| `chunk warnflag detected` | 是否检测到亚健康状态物理盘。 |
| `chunk io error count overflow` | 是否检测到 I/O 错误 (I/O 错误计数超过阈值)。 |
| `chunk checksum error count overflow` | LSM 是否检测校验失败。 |
| `iostat latency detected` | 是否通过 iostat 输出检测到慢盘异常。 |
| `smart error detected` | 是否通过 SMART 信息检测到错误。 |
| `software raid faulty detected` | 是否检测到软件 RAID 故障。 |
| `offline due to io timeout` | 是否因 I/O 超时离线。 |
| `offline due to cmd abort` | 是否因命令被中止离线。 |
| `offline due to error queue` | 是否因错误队列离线。 |
| `reallocated sectors count overflow` | 是否检测到重映射扇区数超过阈值。 |
| `Reallocated_Sector_Ct` | 重映射扇区数，基本代表不良扇区的数量。 |
| `Reported_Uncorrect` | 无法校正的错误，无法通过硬件 ECC 校正的错误。 |
| `Command_Timeout` | 通信超时，无法链接硬盘的错误。 |
| `Temperature_Celsius` | 温度。 |
| `Current_Pending_Sector` | 当前待映射扇区计数，不稳定扇区数量。 |
| `Offline_Uncorrectable` | 脱机无法校正的扇区计数。 |

## 重置物理盘健康状态

在排除物理盘故障后，需重置物理盘健康状态，否则该物理盘将不可继续挂载使用。

**操作方法**

在物理盘所在的节点上执行如下命令重置物理盘健康状态：

`zbs-node set_disk_healthy [/dev/]<disk_name>`

其中 `disk_name` 表示物理盘的盘符。

**输出示例**

```
2024-06-18 14:07:43,908 node.py 769 [13302] [INFO] set chunk partition healthy.
2024-06-18 14:07:45,591 node.py 781 [13302] [INFO] set tuna disk record healthy.
2024-06-18 14:07:46,770 node.py 787 [13302] [INFO] clean from slow disk record.
2024-06-18 14:07:46,800 node.py 793 [13302] [INFO] Setting disk sdc healthy succeed.
```

---

## 管理物理盘 > 挂载和卸载

# 挂载和卸载

## 挂载物理盘

系统会自动发现物理机中插入的物理盘。但插入主机的新物理盘处于未挂载状态，需要通过挂载操作进行格式化，才可以为集群存储所用。

> **注意**
>
> 挂载物理盘将会对其进行格式化，清空其所有数据。进行挂载操作前请确保物理盘上没有需要保留的数据。

**操作方法**

执行如下命令挂载物理盘：

`zbs-deploy-manage mount-disk <disk path> <usage> --chunk_ins_id <chunk_ins_id>`

| **参数** | **说明** |
| --- | --- |
| `disk path` | 需挂载物理盘的路径。 |
| `usage` | 挂载物理盘用途：  - `smtx_system`：挂载物理盘用作节点系统盘，该类型物理盘包含系统分区。 - `cache`：挂载物理盘用作缓存盘。 - `data`：挂载物理盘用作数据盘。 |
| `--chunk_ins_id` | 需要挂载物理盘的物理盘池 ID, 可以通过 `zbs-meta node list` 获取。 |

**输出说明**

输出挂载过程。

## 卸载物理盘

**操作方法**

执行如下命令，将物理盘从节点中卸载：

`zbs-deploy-manage umount-disk <disk path>`

| **参数** | **说明** |
| --- | --- |
| `disk path` | 需卸载物理盘的路径。 |

**输出说明**

输出卸载过程。

---

## 管理物理盘 > 管理数据分区

# 管理数据分区

chunk 会对节点上的物理盘（除系统盘以外）进行管理，管理物理盘分区时，需先格式化物理盘分区，然后将分区挂载到 chunk 上，最终通过 chunk 管理物理盘分区。

## 查看当前节点数据分区信息

**操作方法**

在集群节点执行如下命令，查看当前节点的数据分区信息：

`zbs-chunk [--ins_id <id>] partition list`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数，物理盘池 ID。可用来在多物理盘池环境下过滤仅输出特定物理盘池的信息。 |

**输出示例**

```
==============  ==============================================================  ====================================  ============  ===========  =====================  ===============  =================  ==========  =============  ====================================  ===========  =================
PATH            DEVICE ID                                                       UUID                                  TOTAL SIZE    USED SIZE      NUM CHECKSUM ERRORS    NUM IO ERRORS  STATUS               ERRFLAGS    NUM SLOW IO  PART UUID                               WARNFLAGS    CHECKSUM ENABLE
==============  ==============================================================  ====================================  ============  ===========  =====================  ===============  =================  ==========  =============  ====================================  ===========  =================
/dev/nvme2n1p1  nvme-eui.01000000000000005cd2e40e40575551-part1                 b7a5b3bc-cd9b-483a-8496-b9984dd0f361  1.46 TiB      1.18 TiB                         0                0  PARTITION_MOUNTED           0              0  f8141e82-17e4-4b7e-8c25-85c14fa319b6            0                  0
==============  ==============================================================  ====================================  ============  ===========  =====================  ===============  =================  ==========  =============  ====================================  ===========  =================
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `INS ID` | 物理盘池 ID（仅当多物理盘池且未进行过滤时显示）。 |
| `PATH` | 分区路径。 |
| `DEVICE ID` | 物理盘 ID。 |
| `UUID` | 数据分区的唯一 UUID 标识符。 |
| `TOTAL SIZE` | 数据分区的总容量。 |
| `USED SIZE` | 已使用空间大小。 |
| `NUM CHECKSUM ERRORS` | 校验和的错误数。 |
| `NUM IO ERRORS` | 错误 I/O 数量。 |
| `STATUS` | 分区状态。 |
| `ERRFLAGS` | 错误标记。 |
| `NUM SLOW IO` | Slow I/O 数量。 |
| `PART UUID` | 物理分区的唯一 UUID 标识符。 |
| `WARNFLAGS` | 告警标记。 |
| `CHECKSUM ENABLE` | 是否启用校验和，`0` 代表不启用，`1` 代表启用。 |

## 格式化指定路径下的数据分区

**操作方法**

- **格式化指定路径下的数据分区**

  在集群节点执行如下命令，格式化该节点指定路径下的数据分区：

  `zbs-chunk [--ins_id <id>] partition format <path>`
- **格式化指定路径下已有数据的数据分区**

  在集群节点执行如下命令，格式化该节点指定路径下已有数据的数据分区：

  `zbs-chunk [--ins_id <id>] partition format --force <path>`

  > **注意**：
  >
  > 执行该命令后，数据分区已有数据会丢失，请谨慎操作。
- **格式化用作全闪 SSD 的数据分区**

  在集群节点执行如下命令，格式化该节点指定路径下已有数据的数据分区：

  `zbs-chunk [--ins_id <id>] partition format --ignore_data_checksum <path>`

> **说明**：
>
> 多物理盘池环境下，上述命令中如果指定的分区被其他物理盘池所挂载，命令会执行失败，需要先卸载对应分区。

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数（在多物理盘池环境下是必选参数），物理盘池 ID。指定多物理盘池环境下格式化所使用的物理盘池。 |

**输出示例**

```
Partition successfully formatted
```

## 将数据分区挂载至 chunk

**操作方法**

- **挂载空数据分区**

  在集群节点执行如下命令，将数据分区挂载至该节点指定路径：

  `zbs-chunk [--ins_id <id>] partition mount <path>`
- **挂载已有数据的数据分区**

  > **注意**：
  >
  > 挂载已有数据的数据分区是危险操作，使用如下命令时，需格外谨慎。

  在集群节点执行如下命令，将已有数据的数据分区挂载至该节点指定路径：

  `zbs-chunk [--ins_id <id>] partition mount --force <path>`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数（在多物理盘池环境下是必选参数），物理盘池 ID。指定多物理盘池环境下挂载所使用的物理盘池，需要跟格式化使用的物理盘池保持一致。 |

**输出示例**

```
Partition successfully mounted
```

## 将健康数据分区从 chunk 卸载

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的数据分区从 chunk 卸载：

`zbs-chunk partition umount <path>`

**输出示例**

```
Partition is STAGING, umount will be done in background
```

## 停止将健康数据分区从 chunk 卸载

**操作方法**

在集群节点执行如下命令，停止将该节点指定路径下的数据分区从 chunk 卸载：

`zbs-chunk partition cancel-umount <path>`

**输出示例**

```
Partition cancel umount submitted
```

## 将异常数据分区从 chunk 卸载

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的数据分区从 chunk 卸载，不可取消：

`zbs-chunk partition umount --scheme uuid --mode offline <uuid>`

**输出示例**

```
Partition is STAGING, umount will be done in background
```

## 将数据分区设置为健康状态

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的数据分区设置为健康状态：

`zbs-chunk partition set-healthy <path>`

**输出示例**

```
Partition is set healthy!
```

## 将数据分区设置为不健康状态

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的数据分区设置为不健康状态：

`zbs-chunk partition set-unhealthy <path>`

**输出示例**

```
Partition is set unhealthy! umount and recover will be done in background
```

## 隔离亚健康状态的数据分区

**操作方法**

在集群节点执行如下命令，隔离指定路径下处于亚健康状态的物理盘数据分区：

`zbs-chunk partition isolate <path>`

**输出示例**

```
Partition is HIGH_LAT, isolate will be done in background
```

---

## 管理物理盘 > 管理 Journal 分区

# 管理 Journal 分区

每个节点的 SSD 会专门留出部分分区用作 Journal 分区。ZBS 会在 Journal 分区中记录所做过的操作，以保证数据安全性。

## 查看当前节点 Journal 分区信息

**操作方法**

在集群节点执行如下命令，查看当前节点的所有 Journal 分区：

`zbs-chunk [--ins_id <id>] journal list`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数，物理盘池 ID。可用来在多物理盘池环境下过滤仅输出特定物理盘池的信息。 |

**输出示例**

```
==============  ==================  =============  ========  ============  ===============
PATH              RESERVED ENTRIES    MAX ENTRIES    SEQ NO  STATUS          NUM IO ERRORS
==============  ==================  =============  ========  ============  ===============
/dev/nvme0n1p3                   0      418377728     67005  JOURNAL_IDLE                0
/dev/nvme0n1p3            20819968      418377728     67001  JOURNAL_BUSY                0
==============  ==================  =============  ========  ============  ===============
==============  ===============================================  ====================================  ====================================  ==========  ====================  ===============  ===========
PATH            DEVICE ID                                        UUID                                  PART UUID                               ERRFLAGS  STATUS                  NUM IO ERRORS    WARNFLAGS
==============  ===============================================  ====================================  ====================================  ==========  ====================  ===============  ===========
/dev/nvme0n1p3  nvme-eui.01000000000000005cd2e4d80f575551-part3  2e7322aa-5041-44a2-bda0-a1e53a39b8ab  78ebfe36-4b80-4f5f-813c-3dff49e549d1           0  JOURNALGROUP_MOUNTED                0            0
/dev/nvme1n1p3  nvme-eui.01000000000000005cd2e42a6a5d5551-part3  3d8f44a6-c8d6-42c3-8784-93612236ba40  9f64a25c-a680-43b1-aada-9870feef838f           0  JOURNALGROUP_MOUNTED                0            0
==============  ===============================================  ====================================  ====================================  ==========  ====================  ===============  ===========
```

**输出说明**

在输出结果中，有可能多行对应一次 journal mount 命令成功挂载的 Journal 分区（跟挂载 Journal 分区的空间有关）。

| 参数 | 说明 |
| --- | --- |
| `INS ID` | 物理盘池 ID（仅当多物理盘池且未进行过滤时显示）。 |
| `PATH` | Journal 分区路径。 |
| `RESERVED ENTRIES` | Journal 分区 group 已使用 entry 数量。 |
| `MAX ENTRIES` | Journal 分区 entry 数量。 |
| `SEQ NO` | Journal 分区已复用次数。 |
| `STATUS` | Journal 分区状态：`IDLE`，`BUSY`。 |
| `NUM IO ERRORS` | 错误 I/O 数量。 |

| 参数 | 说明 |
| --- | --- |
| `INS ID` | 物理盘池 ID（仅当多物理盘池且未进行过滤时显示）。 |
| `PATH` | Journal 分区路径。 |
| `DEVICE ID` | 物理盘 ID。 |
| `UUID` | Journal 分区的唯一 UUID 标识符。 |
| `PART UUID` | 物理分区的唯一 UUID 标识符。 |
| `ERRFLAGS` | 错误标记。 |
| `STATUS` | 分区状态。 |
| `NUM IO ERRORS` | 错误 I/O 数量。 |
| `WARNFLAGS` | 告警标记。 |

## 格式化指定路径下的 Journal 分区

**操作方法**

- **格式化指定路径下的空 Journal 分区**

  在集群节点执行如下命令，将该节点指定路径下的空 Journal 分区格式化：

  `zbs-chunk [--ins_id <id>] journal format <path>`
- **格式化指定路径下的已有数据的 Journal 分区**

  在集群节点执行如下命令，将该节点指定路径下已有数据的 Journal 分区格式化：

  `zbs-chunk [--ins_id <id>] journal format --force <path>`

  > **注意**：
  >
  > 执行该命令后，Journal 分区已有数据会丢失，请谨慎操作。

> **说明**：
>
> 多物理盘池环境下，上述命令中如果指定的分区被其他物理盘池所挂载，命令会执行失败，需要先卸载对应分区。

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数（在多物理盘池环境下是必选参数），物理盘池 ID。指定多物理盘池环境下格式化所使用的物理盘池。 |

**输出示例**

```
Journal successfully formatted
```

## 将 Journal 分区挂载到 chunk

**操作方法**

在集群节点执行如下命令，将 Journal 分区挂载到该节点指定路径下的 chunk 上：

`zbs-chunk [--ins_id <id>] journal format <path>`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数（在多物理盘池环境下是必选参数），物理盘池 ID。指定多物理盘池环境下挂载所使用的物理盘池，需要跟格式化使用的物理盘池保持一致。 |

**输出示例**

```
Journal successfully mounted
```

## 将 Journal 分区从 chunk 卸载

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的 Journal 分区从 chunk 卸载：

`zbs-chunk journal umount <path>`

**输出示例**

```
Journal successfully unmounted
```

## 将 Journal 分区设置为健康状态

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的 Journal 分区设置为健康状态：

`zbs-chunk journal set-healthy <path>`

**输出示例**

```
Journal device is set healthy!
```

## 将 Journal 分区设置为不健康状态

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的 Journal 分区设置为不健康状态：

`zbs-chunk journal set-unhealthy <path>`

**输出示例**

```
Journal device is set unhealthy!
```

## 刷新节点的所有 Journal 分区

**操作方法**

在集群节点执行如下命令，刷新该节点的所有 Journal 分区：

`zbs-chunk journal flush`

**输出示例**

```
Journal successfully flushed
```

**输出说明**

此命令是异步操作，即没有完成前也会立即返回。

---

## 管理物理盘 > 管理缓存分区

# 管理缓存分区

在 SSD 中，除了需要 Journal 分区来记录所进行过的操作，还会用部分分区用作缓存，来对数据读写进行加速。

## 查看节点缓存信息

查看节点中查询活跃缓存、非活跃缓存、干净缓存、空闲缓存的大小及占比。

> **注意**：
>
> 上述四个指标的值相加不一定等于总缓存的大小，因为缓存分区内部划分出了一部分用作集群的性能分区，而前三个指标是不把性能分区统计在内的。

**操作方法**

在集群节点中执行如下命令：

`zbs-chunk [--ins_id <id>] cache list`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数，物理盘池 ID。可用来在多物理盘池环境下过滤仅输出特定物理盘池的信息。 |

**输出示例**

```
====ALL INSTANCES CACHE SUMMARY====
CACHE HIT RATE:        1.0
TOTAL ACTIVE:           0B ( 0.00%)
TOTAL INACTIVE:         0B ( 0.00%)
TOTAL CLEAN:            0B ( 0.00%)
TOTAL PERF USED:   681.07G ( 6.04%)
TOTAL FREE:         10.34T (93.96%)
TOTAL:              11.01T
========  ==============  =================================================  ====================================  ===============  =============  ==========  =============  ====================================  ===========  ============  ===========
  INS ID  PATH            DEVICE ID                                          UUID                                    NUM IO ERRORS  STATUS           ERRFLAGS    NUM SLOW IO  PART UUID                               WARNFLAGS  TOTAL SIZE    USED SIZE
========  ==============  =================================================  ====================================  ===============  =============  ==========  =============  ====================================  ===========  ============  ===========
       1  /dev/nvme0n1p4  nvme-eui.01000000000000005cd2e4fbb1e35551-part4    47cc2154-ca41-456f-80ab-cb1b53916e4f                0  CACHE_MOUNTED           0              0  6a1c9e11-1964-456c-89da-8d6f6d934ffb            0  2.61 TiB      321.07 GiB
       2  /dev/nvme1n1p4  nvme-INTEL_SSDPF2KE032T1_BTAX3161016C3P8CGN-part4  e9cc8c41-c9ef-4a65-9773-82ba7f8ef405                0  CACHE_MOUNTED           0              0  ced654e4-6b2d-4344-8627-6a8e57b41e44            0  2.61 TiB      120.00 GiB
       3  /dev/nvme2n1p2  nvme-INTEL_SSDPF2KE032T1_PHAX331404UY3P8CGN-part2  d4f180ad-5b8d-40af-9568-ec870db4716e                0  CACHE_MOUNTED           0              0  9fb6b81a-8e6d-4d85-94de-b4a628d1a6eb            0  2.89 TiB      120.00 GiB
       4  /dev/nvme3n1p2  nvme-INTEL_SSDPF2KE032T1_PHAX325004L53P8CGN-part2  e3743e81-fab4-42c2-b8e2-ecf493ae446c                0  CACHE_MOUNTED           0              0  644079ef-5078-4c89-a14e-dadd9a3d4cd7            0  2.89 TiB      120.00 GiB
========  ==============  =================================================  ====================================  ===============  =============  ==========  =============  ====================================  ===========  ============  ===========
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `CACHE HIT RATE` | 缓存命中率，缓存仅代表读缓存。 |
| `TOTAL ACTIVE` | 活跃缓存大小及其占比（不包含性能分区），预期长期是 0。 |
| `TOTAL INACTIVE` | 非活跃缓存大小及其占比（不包含性能分区），预期长期是 0。 |
| `TOTAL CLEAN` | 干净缓存大小及其占比（不包含性能分区），预期长期大于 0。 |
| `TOTAL PERF USED` | 性能层空间总体占用。 |
| `TOTAL FREE` | 空闲缓存大小及其占比（包含性能分区）。 |
| `TOTAL` | 总缓存大小（包含性能分区）。 |
| `PATH` | 分区路径。 |
| `DEVICE ID` | 物理盘 ID。 |
| `UUID` | 缓存分区的唯一 UUID 标识符。 |
| `NUM IO ERRORS` | 错误 I/O 数量。 |
| `STATUS` | 分区状态。 |
| `ERRFLAGS` | 错误标记。 |
| `NUM SLOW IO` | Slow I/O 数量。 |
| `PART UUID` | 物理分区的唯一 UUID 标识符。 |
| `WARNFLAGS` | 告警标记。 |
| `TOTAL SIZE` | 缓存分区的总容量。 |
| `USED SIZE` | 已使用空间大小。 |

## 格式化指定路径下的缓存分区

**操作方法**

- **格式化指定路径下的缓存分区**

  在集群节点执行如下命令，格式化该节点指定路径下的缓存分区：

  `zbs-chunk [--ins_id <id>] cache format <path>`
- **格式化指定路径下已有数据的缓存分区**

  在集群节点执行如下命令，格式化该节点指定路径下已有数据的缓存分区：

  `zbs-chunk [--ins_id <id>] cache format --force <path>`

  > **注意**：
  >
  > 执行该命令后，缓存分区已有数据会丢失，请谨慎操作。

> **说明**：
>
> 多物理盘池环境下，上述命令中如果指定的分区被其他物理盘池所挂载，命令会执行失败，需要先卸载对应分区。

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数（在多物理盘池环境下是必选参数），物理盘池 ID。指定多物理盘池环境下格式化所使用的物理盘池。 |

**输出示例**

```
Cache successfully formatted
```

## 将缓存分区挂载到 chunk

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的缓存分区挂载到 chunk：

`zbs-chunk [--ins_id <id>] cache mount <path>`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数（在多物理盘池环境下是必选参数），物理盘池 ID。指定多物理盘池环境下挂载所使用的物理盘池，需要跟格式化使用的物理盘池保持一致。 |

**输出示例**

```
Successfully mounted
```

## 将健康缓存分区从 chunk 卸载

**操作方法**

在集群节点执行如下命令，将该节点指定路径的缓存分区从 chunk 上卸载：

`zbs-chunk cache umount <path>`

**输出示例**

```
Cache device is STAGING now, umount will be done in background
```

## 停止将健康缓存分区从 chunk 卸载

**操作方法**

在集群节点执行如下命令，停止将该节点指定路径的缓存分区从 chunk 上卸载：

`zbs-chunk cache cancel-umount <path>`

**输出示例**

```
Cache cancel umount submitted
```

## 将异常缓存分区从 chunk 卸载

**操作方法**

在集群节点执行如下命令，将该节点指定路径的缓存分区从 chunk 上卸载，不可取消：

`zbs-chunk cache umount --scheme uuid --mode offline <uuid>`

**输出示例**

```
Cache device is STAGING now, umount will be done in background
```

## 将缓存分区设置为健康状态

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的缓存分区设置健康状态：

`zbs-chunk cache set-healthy <path>`

**输出示例**

```
Cache device is set healthy!
```

## 将缓存分区设置为不健康状态

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的缓存分区设置为不健康状态：

`zbs-chunk cache set-unhealthy <path>`

**输出示例**

```
Cache device is set unhealthy! umount and recover will be done in background
```

---

## 管理 chunk

# 管理 chunk

chunk 运行在每一台服务器节点上，主要提供三类服务：

- 负责和 meta 的通信，向 meta 提供 chunk 的心跳信息、本节点的使用容量和数据块的副本数等信息。
- 负责处理客户端的读写请求。
- LSM（Local Storage Manager）：负责管理本节点上的除了系统盘以外的所有本地存储盘。包括 PCI-SSD、SSD、SATA 和 SAS 盘。按照存储盘的用途可以分为缓存盘和数据盘。

每个节点的 chunk 服务都会注册到 meta 服务，也就是元数据服务中，然后可以通过 meta 来管理整个集群。

---

## 管理 chunk > 将节点 chunk 注册到 meta 中

# 将节点 chunk 注册到 meta 中

Chunk 服务在 ZBS 中负责数据管理，每个节点的 chunk 服务都会注册到 meta 服务，也就是元数据服务中，然后可以通过 meta 来管理整个集群。

**操作方法**

在集群任一节点执行如下命令，将节点 chunk 注册到 meta 中：

`zbs-meta chunk register <ip> <chunk_port> [--data_port <chunk_data_port>]`

| 参数 | 说明 |
| --- | --- |
| `ip` | Chunk 存储网络的 IP 地址。 |
| `chunk_port` | Chunk 的端口号。 |
| `--data_port <chunk_data_port>` | 可选参数（在多物理盘池环境下是必选参数），chunk 的数据通信端口号。 |

---

## 管理 chunk > 查看 chunk

# 查看 chunk

## 查看集群中连通的 chunk 列表

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta chunk list [--show_details]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `--show_details` | 可选参数，选择是否显示更加详细的 chunk 信息。 |

**输出示例**

```
  ID  IP            Host Name                                         Port  Storage Pool    Use State    Link Status        Data Capacity    Valid Space    Allocated Space    Failure Data Space    Perf Data Capacity    Perf Valid Space    Perf Allocated Space    Perf Failure Data Space    Registered Date      LSM Version    Zone     Maintenance Mode
----  ------------  ----------------------------------------------  ------  --------------  -----------  -----------------  ---------------  -------------  -----------------  --------------------  --------------------  ------------------  ----------------------  -------------------------  -------------------  -------------  -------  ------------------
   1  10.2.234.198  smtxzbs-5-6-0-b45-el7X0617125715X3   10200  system          IN_USE       CONNECTED_ERROR    602.34 GiB       602.34 GiB     0.00 B             0.00 B                20.00 GiB             20.00 GiB           768.00 KiB              0.00 B                     2024-06-17 14:06:12  2.4.1          default  False
   2  10.2.234.196  smtxzbs-5-6-0-b45-el7X0617125715X1   10200  system          IN_USE       CONNECTED_HEALTHY  602.34 GiB       602.34 GiB     0.00 B             0.00 B                20.00 GiB             20.00 GiB           256.75 MiB              0.00 B                     2024-06-17 14:06:13  2.4.1          default  False
   3  10.2.234.197  smtxzbs-5-6-0-b45-el7X0617125715X2   10200  system          IN_USE       CONNECTED_HEALTHY  602.34 GiB       602.34 GiB     0.00 B             0.00 B                20.00 GiB             20.00 GiB           256.75 MiB              0.00 B                     2024-06-17 14:06:13  2.4.1          default  False
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `ID` | Chunk ID。 |
| `IP` | Chunk 存储 IP。 |
| `HostName` | chunk 节点主机名。 |
| `Port` | Chunk RPC 端口。 |
| `Storage Pool` | 所属存储池。 |
| `Use State` | 使用状态。 |
| `Link Status` | 连接状态。 |
| `Data Capacity` | 容量层提供的总数据空间大小。 |
| `Valid Space` | 容量层有效数据空间大小。 |
| `Allocated Space` | 容量层已分配的数据空间大小（meta 认为的空间消耗）。 |
| `Failure Data Space` | 容量层失效数据空间大小。 |
| `Perf Data Capacity` | 性能层提供的总数据空间大小。 |
| `Perf Valid Space` | 性能层有效数据空间大小。 |
| `Perf Allocated Space` | 性能层已分配的数据空间大小（meta 认为的空间消耗）。 |
| `Perf Failure Data Space` | 性能层失效数据空间大小。 |
| `Registered Date` | 注册时间。 |
| `LSM Version` | LSM 版本。 |
| `Zone` | 所属可用域。 |
| `Maintenance Mode` | 是否处于维护模式。 |

## 查看集群中节点下的 chunk 列表

**操作方法**

在集群任一节点执行如下命令，查看集群中指定节点下的 chunk 列表：

`zbs-meta node show <data_ip> [--show_details]`

也可以在集群任一节点执行如下命令，查看集群中所有节点下的 chunk 列表：

`zbs-meta node list [--show_details]`

参数定义如下：

| 参数 | 说明 |
| --- | --- |
| `data_ip` | 节点存储 IP 地址。 |
| `--show_details` | 可选参数，选择是否显示更加详细的节点信息。 |

**输出示例**

```
Node: 10.0.128.55, Host: Node55
  INS ID    CID    Data Port  Status               Cap Size    Cap Valid    Cap Alloc    Perf Size    Perf Valid    Perf Alloc    Register Date
--------  -----  -----------  -------------------  ----------  -----------  -----------  -----------  ------------  ------------  -------------------
       1      2        10201  🟢 CONNECTED_HEALTHY  4.70 TiB    4.70 TiB     10.00 GiB    536.00 GiB   536.00 GiB    270.60 GiB    2024-12-24 11:20:43
       2      4        12201  🟢 CONNECTED_HEALTHY  5.05 TiB    5.05 TiB     0.00 B       475.20 GiB   475.20 GiB    85.52 GiB     2025-01-15 14:32:34
       3      5        14201  🟢 CONNECTED_HEALTHY  5.20 TiB    5.20 TiB     5.00 GiB     594.00 GiB   594.00 GiB    186.90 GiB    2025-01-15 14:32:37
       4      6        16201  🟢 CONNECTED_HEALTHY  5.20 TiB    5.20 TiB     5.00 GiB     594.00 GiB   594.00 GiB    186.90 GiB    2025-01-15 14:37:50
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Node` | 节点存储 IP。 |
| `Host` | 节点主机名。 |
| `INS ID` | 物理盘池 ID。 |
| `CID` | Chunk ID。 |
| `Data Port` | Chunk 数据通信端口。 |
| `Status` | 连接状态。 |
| `Cap Size` | 容量层提供的总数据空间大小。 |
| `Cap Valid` | 容量层有效数据空间大小。 |
| `Cap Alloc` | 容量层已分配的数据空间大小（meta 认为的空间消耗）。 |
| `Perf Size` | 性能层提供的总数据空间大小。 |
| `Perf Valid` | 性能层有效数据空间大小。 |
| `Perf Alloc` | 性能层已分配的数据空间大小（meta 认为的空间消耗）。 |
| `Registered Date` | 注册时间。 |

## 查看集群中健康 chunk 间的数据链路连通性

**操作方法**

在集群任一节点执行如下命令，查看集群中与 meta 正常连接的 chunk 间的数据链路连通性：

`zbs-meta cluster get_chunk_connectivities`

**输出示例**

```
cid 1: {1: CONNECTED, 2: CONNECTED, 3: CONNECTED, 4: DISCONNECTED}
cid 2: {1: CONNECTED, 2: CONNECTED, 3: CONNECTED, 4: CONNECTED}
cid 3: {1: CONNECTED, 2: CONNECTED, 3: CONNECTED, 4: CONNECTED}
cid 4: {1: DISCONNECTED, 2: CONNECTED, 3: CONNECTED, 4: CONNECTED}
```

## 查看集群中某一 chunk 与其他 chunk 间的数据链路连通性

**操作方法**

在集群任一节点执行如下命令，查看集群中某一 chunk 与其他和 meta 正常连接的 chunk 间的数据链路连通性：

`zbs-meta cluster show_chunk_connectivity <cid>`

| 参数 | 说明 |
| --- | --- |
| `cid` | 需要获取与其他 chunk 间的数据链路连通性的 chunk ID。 |

**输出示例**

```
dst cid: 1, CONNECTED
dst cid: 2, CONNECTED
dst cid: 3, CONNECTED
dst cid: 4, DISCONNECTED
```

## 查看某个节点 chunk 的详细信息

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta chunk show <data_ip> <data_port>`

| 参数 | 说明 |
| --- | --- |
| `data_ip` | 节点存储 IP 地址。 |
| `data_port` | Chunk 使用端口。 |

**输出示例**

```
-----------------------  ----------------------------------------------
ID                       2
IP                       10.2.234.196
Host Name                5-6-0-b45-el7X0617125715X1
Port                     10200
Storage Pool             system
Use State                IN_USE
Link Status              CONNECTED_HEALTHY
Data Capacity            602.34 GiB
Valid Space              602.34 GiB
Allocated Space          0.00 B
Failure Data Space       0.00 B
Perf Data Capacity       20.00 GiB
Perf Valid Space         20.00 GiB
Perf Allocated Space     256.75 MiB
Perf Failure Data Space  0.00 B
Registered Date          2024-06-17 14:06:13
LSM Version              2.4.1
Zone                     default
Maintenance Mode         False
-----------------------  ----------------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Storage Pool` | 所属存储池。 |
| `Use State` | 使用状态。 |
| `Link Status` | 连接状态。 |
| `Data Capacity` | 容量层提供的总数据空间大小。 |
| `Valid Space` | 容量层有效数据空间大小。 |
| `Allocated Space` | 容量层已分配的数据空间大小（meta 认为的空间消耗）。 |
| `Failure Data Space` | 容量层失效数据空间大小。 |
| `Perf Data Capacity` | 性能层提供的总数据空间大小。 |
| `Perf Valid Space` | 性能层有效数据空间大小。 |
| `Perf Allocated Space` | 性能层已分配的数据空间大小（meta 认为的空间消耗）。 |
| `Perf Failure Data Space` | 性能层失效数据空间大小。 |
| `Registered Date` | 注册时间。 |
| `LSM Version` | LSM 版本。 |
| `Zone` | 所属可用域。 |
| `Maintenance Mode` | 是否处于维护模式。 |

## 查看 chunk 所有 PID

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta chunk list_pid <chunk_id>`

**输出示例**

```
[root@localhost ~]# zbs-meta chunk list_pid 1
cap pid num: 11
cap thin pid num: 5
cap thick pid num: 6
cap rx pid num: 0
cap tx pid num: 4
cap recover src pid num: 5
cap new thin pid num: 0
cap thin reserved pid num: 0
cap thick reserved pid num: 0

perf pid num: 0
perf thin pid num: 0
perf thick pid num: 0
perf rx pid num: 0
perf tx pid num: 0
perf recover src pid num: 0
perf new thin pid num: 0
perf thin reserved pid num: 0
perf thick reserved pid num: 0

cap pid:                  8930,8938,9107,9112,10193,11230,11231,11234,11246,11250,11254
cap thin pid:             8930,8938,9107,9112,10193
cap thick pid:            11230,11231,11234,11246,11250,11254
cap rx pid:
cap tx pid:               12107,13426,14619,14628
cap recover src pid:      12107,13426,14619,14628,14654
cap new thin pid:
cap thin reserved pid:
cap thick reserved pid:

perf pid:
perf thin pid:
perf thick pid:
perf rx pid:
perf tx pid:
perf recover src pid:
perf new thin pid:
perf thin reserved pid:
perf thick reserved pid:
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `cap pid` | 该 chunk 管理的容量层 PID 列表。 |
| `cap thin pid` | 容量层精简置备 PID。 |
| `cap thick pid` | 容量层厚置备 PID。 |
| `cap rx pid` | 容量层正在接收的 PID。 |
| `cap tx pid` | 容量层正在发送的 PID。 |
| `perf pid` | 该 chunk 管理的性能层 PID 列表。 |
| `perf thin pid` | 性能层精简置备 PID。 |
| `perf thick pid` | 性能层厚置备 PID。 |
| `perf rx pid` | 性能层正在接收的 PID。 |
| `perf tx pid` | 性能层正在发送的 PID。 |

## 查看集群中所有 chunk 的空间负载情况

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta chunk list_space`

**输出示例**

```
[root@node131-203 22:33:58 ~]$ zbs-meta chunk list_space
  ID  Cap Valid    Cap Alloc    Cap Ratio    Cap Total    Cap Failure    Cap Inherited    Perf Thin/Thick Valid    Perf Thin/Thick Alloc    Perf Thin/Thick Ratio    Perf Valid    Perf Alloc    Perf Total    Perf Failure    Perf Inherited    Prior Percent    Prior Planned    Prior Alloc
----  -----------  -----------  -----------  -----------  -------------  ---------------  -----------------------  -----------------------  -----------------------  ------------  ------------  ------------  --------------  ----------------  ---------------  ---------------  -------------
   1  109.57 TiB   8.48 TiB     7.70%        109.57 TiB   0.00 B         4.81 GiB         (8.82 TiB, 475.33 GiB)   (4.13 TiB, 226.25 GiB)   (46.85%, 47.60%)         9.28 TiB      4.60 TiB      9.28 TiB      0.00 B          0.00 B            5%               475.33 GiB       226.25 GiB
   2  95.87 TiB    12.82 TiB    13.40%       95.87 TiB    0.00 B         19.66 GiB        (7.84 TiB, 422.53 GiB)   (3.54 TiB, 303.25 GiB)   (45.22%, 71.77%)         8.25 TiB      3.96 TiB      8.25 TiB      0.00 B          0.00 B            5%               422.53 GiB       303.25 GiB
   3  41.09 TiB    7.82 TiB     19.00%       41.09 TiB    0.00 B         7.50 GiB         (7.84 TiB, 422.53 GiB)   (3.88 TiB, 305.00 GiB)   (49.43%, 72.18%)         8.25 TiB      4.29 TiB      8.25 TiB      0.00 B          0.00 B            5%               422.53 GiB       305.00 GiB
   4  47.94 TiB    5.42 TiB     11.30%       47.94 TiB    0.00 B         184.25 MiB       (3.92 TiB, 211.27 GiB)   (1.91 TiB, 131.00 GiB)   (48.84%, 62.01%)         4.13 TiB      2.12 TiB      4.13 TiB      0.00 B          0.00 B            5%               211.27 GiB       131.00 GiB
   5  41.09 TiB    898.48 GiB   2.10%        41.09 TiB    0.00 B         0.00 B           (7.84 TiB, 422.53 GiB)   (0.00 B, 507.50 MiB)     (0.00%, 0.12%)           8.25 TiB      422.53 GiB    8.25 TiB      0.00 B          0.00 B            5%               422.53 GiB       0.00 B
   6  109.57 TiB   6.39 TiB     5.80%        109.57 TiB   0.00 B         18.50 MiB        (8.82 TiB, 475.33 GiB)   (4.03 TiB, 223.75 GiB)   (45.69%, 47.07%)         9.28 TiB      4.49 TiB      9.28 TiB      0.00 B          0.00 B            5%               475.33 GiB       223.75 GiB
   7  47.94 TiB    5.08 TiB     10.60%       47.94 TiB    0.00 B         333.50 MiB       (3.92 TiB, 211.27 GiB)   (1.80 TiB, 152.00 GiB)   (46.01%, 71.95%)         4.13 TiB      2.01 TiB      4.13 TiB      0.00 B          0.00 B            5%               211.27 GiB       152.00 GiB
```

## 查看处于存储维护模式的 chunk 信息

获取处于存储维护模式的 chunk 信息，包括 chunk ID 和超时时间。

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta chunk get_maintenance`

**输出示例**

```
[root@localhost ~]$zbs-meta chunk get_maintenance
maintenance cid: 1
expire time left: 98 s
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `maintenance cid` | 进入维护模式的 chunk ID。 |
| `expire time left` | 维护模式到期时间。 |

## 查看 chunk 信息

查看 chunk 相关的信息，包括 chunk 支持的功能、LSM 的版本，以及 I/O 速率等

**操作方法**

在集群节点执行如下命令，可查看指定物理盘池 chunk 中全部的数据块：

`zbs-chunk [--ins_id <id>] summary`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数，物理盘池 ID。可用来在多物理盘池环境下过滤仅输出特定物理盘池的信息。 |

**输出示例**

```
LSM Version:
============================================================
lsm_state                     : LSM_READY
lsm_version                   : 2.4.3
ctime(Instance 1)             : 2025-06-07T14:31:56Z
lsm_uuid(Instance 1)          : 7a1da998-1e48-472c-a7c7-298e8de2cc3d
ctime(Instance 2)             : 2025-06-07T14:31:56Z
lsm_uuid(Instance 2)          : be837875-fe8b-4b03-87a4-3c8712ab3db9

LSM Capability:
============================================================
LSM_CAP_DISK_SAFE_UMOUNT      : True
LSM_CAP_DISK_REJECT_UNHEALTHY : True
LSM_CAP_PARTITION_ISOLATE     : True
LSM_CAP_COMPARE_EXTENT        : True
LSM_CAP_CACHE_ISOLATE         : True

LSM Speed(All instances):
============================================================
LSM IOPS                      : 0 /s
LSM BW                        : 0.00 B/s(0.00 B/s)
Writeback IOPS                : 0 /s
Writeback BW                  : 0.00 B/s(0.00 B/s)
Unmap IOPS                    : 0 /s
Unmap BW                      : 0.00 B/s(0.00 B/s)
Waiting Reclaim Items         : 0

Data Channel Server:
============================================================
Use RDMA                      : False

chunk Capability:
============================================================
Agile Recover                 : True

Storage Server Status:
============================================================
iSCSI                         : Running
NFS                           : Running
Vhost                         : Running
NVMe-oF                       : Running

Flags:
============================================================
metric_on                     : True
trace_on                      : False
adaptive_trace_on             : True
accel_copy_mode               : ACCEL_COPY_DISABLED
chunk_instances_num           : 2
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `lsm_state` | LSM 状态。 |
| `ctime` | LSM 创建时间。 |
| `lsm_uuid` | LSM UUID。 |
| `lsm_version` | LSM 版本号。 |
| `LSM_CAP_DISK_SAFE_UMOUNT` | `True` 代表 LSM 提供了安全卸载物理盘的能力。 |
| `LSM_CAP_DISK_REJECT_UNHEALTHY` | `True` 代表 LSM 会拒绝接入不健康的物理盘。 |
| `LSM_CAP_PARTITION_ISOLATE` | `True` 代表 LSM 提供了隔离物理数据盘的能力。 |
| `LSM_CAP_COMPARE_EXTENT` | `True` 代表 LSM 提供了比较 extent 数据差异的能力。 |
| `LSM_CAP_CACHE_ISOLATE` | `True` 代表 LSM 提供了隔离物理缓存盘的能力。 |
| `LSM IOPS` | LSM 当前 IOPS。 |
| `LSM BW` | LSM 当前带宽。 |
| `Writeback IOPS` | LSM 从缓存分区写回数据分区的 IOPS。 |
| `Writeback BW` | LSM 从缓存分区写回数据分区的 BW。 |
| `Unmap IOPS` | Unmap 当前 IOPS。 |
| `Unmap BW` | Unmap 当前带宽。 |
| `Waiting Reclaim Items` | 等待回收的 extent 数量。 |
| `Use RDMA` | 是否启用了 RDMA。 |
| `Agile Recover` | 是否启用了敏捷恢复，chunk 退出维护模式之后，敏捷恢复能够更高效完成数据恢复。 |
| `iSCSI` | iSCSI server 运行状态。 |
| `NFS` | NFS server 运行状态。 |
| `Vhost` | Vhost server 运行状态。 |
| `NVMe-oF` | NVMe-oF server 运行状态。 |
| `metric_on` | `True` 代表开启了 metric 统计。 |
| `trace_on` | `True` 代表开启了 I/O trace 统计。 |
| `adaptive_trace_on` | `True` 代表开启了动态 I/O trace 统计。 |
| `accel_copy_mode` | 硬件加速拷贝运行状态（`ACCEL_COPY_DISABLED`表示禁用，`ACCEL_COPY_BY_DSA`表示启用，`ACCEL_COPY_BY_SOFTWARE`表示配置错误未能正确启用硬件加速拷贝）。 |
| `chunk_instances_num` | 当前节点的物理盘池数量。 |

## 查看 chunk 计数器

Chunk 的读写操作对 chunk 的影响会暂时记录在 chunk 的计数器中。

**操作方法**

在集群节点执行如下命令查看所有计数器：

`zbs-chunk counter list '*'`

**输出示例**

```
=================== ========== ============= ============== ==============

============ =========== ========== =========== ========== =========

NAME DURATION TOTAL VALUE TOTAL TIME TOTAL CNT

LAST VALUE LAST TIME LAST CNT CUR VALUE CUR TIME CUR CNT

=================== ========== ============= ============== ==============

============ =========== ========== =========== ========== =========

chunk read counter 1 1.66235e+11 1.45566e+14 4.01898e+07

0 0 0 0 0 0

chunk write counter 1 3.30623e+11 5.42942e+14 4.08241e+07

0 0 0 0 0 0

migrate 1 0 0 0

0 0 0 0 0 0

recover 1 2.68435e+08 1024 1024

0 0 0 0 0 0

=================== ========== ============= ============== ==============

============ =========== ========== =========== ========== =========
```

## 查看节点恢复速度

**操作方法**

在集群节点执行如下命令，可查看当前节点全部或特定物理盘池的恢复速度：

`zbs-chunk [--ins_id <id>] recover list`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数，物理盘池 ID。可用来在多物理盘池环境下过滤仅输出特定物理盘池的信息。 |

**输出示例**

```
Total Recover Speed: 0.00 B/s(0.00 B/s)
From Local Speed: 0.00 B/s(0.00 B/s)
From Remote Speed: 0.00 B/s(0.00 B/s)
```

## 查看节点的迁移速度

**操作方法**

在集群节点执行如下命令，可查看当前节点全部或特定物理盘池的迁移速度：

`zbs-chunk [--ins_id <id>] migrate list`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数，物理盘池 ID。可用来在多物理盘池环境下过滤仅输出特定物理盘池的信息。 |

**输出示例**

```
Total Migrate Speed: 0.00 B/s(0.00 B/s)
From Local Speed: 0.00 B/s(0.00 B/s)
From Remote Speed: 0.00 B/s(0.00 B/s)
```

## 查看本地 chunk 的数据块

**操作方法**

在集群节点执行如下命令，可查看指定物理盘池 chunk 中指定范围内的数据块：

`zbs-chunk [--ins_id <id>] extent list [--start <START_PID>] [--length <LENGTH>]`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数，物理盘池 ID，默认值为 `1`。可用来在多物理盘池环境下过滤仅输出特定物理盘池的信息。 |
| `--start <START_PID>` | 可选参数，extent 的起始 PID，默认值为 `0`。 |
| `--length <LENGTH>` | 可选参数，extent 的数量，默认值和最大值均为 `1024`。 |

**输出示例**

```
=====  ========  ==============  =========  ===========  ============  ========  =======  =====  =================  ======
  PID    STATUS    NUM CHILDREN    PART ID    EXTENT NO    ORIGIN PID  BITMAP      EPOCH    GEN  THICK PROVISION    PERF
=====  ========  ==============  =========  ===========  ============  ========  =======  =====  =================  ======
    5         1               0          0            0             0                  5   1783  False              True
   22         1               0          0            0             0                 14   1025  False              True
   23         1               0          0            0             0                 15      0  False              True
   24         1               0          0            0             0                 16      0  False              True
   25         1               0          0            0             0                 17      0  False              True
=====  ========  ==============  =========  ===========  ============  ========  =======  =====  =================  ======
```

## 查看本地 chunk 的全部数据块

**操作方法**

在集群节点执行如下命令，可查看指定物理盘池 chunk 中全部的数据块：

`zbs-chunk [--ins_id <id>] extent listall --output_file <file>`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数，物理盘池 ID，默认值为 `1`。可用来在多物理盘池环境下过滤仅输出特定物理盘池的信息。 |
| `file` | 必选参数，输出文件路径。 |

**输出示例**

```
List all extents done.
```

## 查看本地 chunk 的地址配置信息

**操作方法**

在集群节点执行如下命令，查看当前节点全部或特定物理盘池 chunk 的地址配置信息：

`zbs-chunk [--ins_id <id>] address show`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数，物理盘池 ID。可用来在多物理盘池环境下过滤仅输出特定物理盘池的信息。 |

**输出示例**

```
rpc_ip: "10.0.128.25"
rpc_port: 10200
data_ip: "10.0.128.25"
data_port: 10201
data_unix_path: ""
meta_ip: "10.0.128.25"
meta_port: 10100
chunk_id: 4
secondary_data_ip: "20.0.128.25"
scvm_mode_host_data_ip: ""
instance_id: 1

rpc_ip: "10.0.128.25"
rpc_port: 10200
data_ip: "10.0.128.25"
data_port: 12201
data_unix_path: ""
meta_ip: "10.0.128.25"
meta_port: 10100
chunk_id: 9
secondary_data_ip: "20.0.128.25"
scvm_mode_host_data_ip: ""
instance_id: 2
```

## 查看 chunk 的实时 I/O metric 数据

**操作方法**

在集群节点执行如下命令，可查看当前节点的 I/O Metric：

`zbs-chunk [--ins_id <id>] metric <METRIC_TYPE>`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数，物理盘池 ID，默认值为 `1`。可用来在多物理盘池环境下过滤仅输出特定物理盘池的信息。 |
| `METRIC_TYPE` | 指定要查看实时 metric 数据的 I/O 类型，可选值为 `app`（业务 I/O），`sink`（下沉 I/O），`reposition`（ recover 和 migrate I/O），`fc`（性能层限流）。 |

**输出示例**

查看业务 I/O 的 metric (`METRIC_TYPE` 取值为 `app`)

```
-----------------------------  -----------------------------------------------------------
Access Perf Read               IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Perf Write              IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap EC Read             IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap EC Write            IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap Replica Read        IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap Replica Write       IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Perf Promote Write      IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap EC Promote Read     IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap Rep Promote Read    IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Perf Read          IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Perf Write         IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Cap EC Read        IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Cap EC Write       IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Cap Replica Read   IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Cap Replica Write  IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Perf Read           IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Perf Write          IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Cap EC Read         IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Cap EC Write        IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Cap Replica Read    IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Cap Replica Write   IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Help                           App IO
-----------------------------  -----------------------------------------------------------
```

查看下沉 I/O 的 metric (`METRIC_TYPE` 取值为 `sink`)

```
-----------------------------  ------------------------------------------------------------------------------------------------
Access Perf Read               IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Perf Write              IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap EC Read             IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap EC Write            IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap Replica Read        IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap Replica Write       IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Perf Promote Write      IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap EC Promote Read     IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap Rep Promote Read    IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Perf Read          IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Perf Write         IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Cap EC Read        IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Cap EC Write       IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Cap Replica Read   IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Cap Replica Write  IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Perf Read           IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Perf Write          IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Cap EC Read         IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Cap EC Write        IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Cap Replica Read    IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Cap Replica Write   IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Help                           -----------------------------------------------------------------------------------------------
                               * Local: sink io triggered by this chunk; Remote: sink io from by other chunk.

                               * perf write:                    promote during sink & unmap
                               * perf read:                     sink speed
                               * cap ec read:                   ec read during block-granularity update + promote for ec block-size alignment.
                               * cap replica read:              should always be 0.
                               * cap write (both ec & replica):         sink speed with write amplification
                               * ec perf promote write:                 promote for ec block-size alignment (write part).
                               * cap ec promote read:           promote for ec block-size alignment (read part).
                               * cap replica promote read:      should always be 0.
-----------------------------  ------------------------------------------------------------------------------------------------
```

查看 recover 和 migrate I/O 的 metric (`METRIC_TYPE` 取值为 `reposition`)

```
-----------------------------  -----------------------------------------------------------
Access Perf Read               IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Perf Write              IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap EC Read             IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap EC Write            IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap Replica Read        IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap Replica Write       IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Perf Promote Write      IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap EC Promote Read     IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Access Cap Rep Promote Read    IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Perf Read          IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Perf Write         IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Cap EC Read        IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Cap EC Write       IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Cap Replica Read   IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Remote Cap Replica Write  IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Perf Read           IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Perf Write          IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Cap EC Read         IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Cap EC Write        IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Cap Replica Read    IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
From Local Cap Replica Write   IOPS: 0, BW: 0.000 MiB/s, Lat: 0.000 ms, ReqSize: 0.000 KiB
Help                           Recover or Migrate IO
-----------------------------  -----------------------------------------------------------
```

查看性能层限流的 metric (`METRIC_TYPE` 取值为 `fc`)

```
[Flow Manager]
Flow control enable: False
Avail tokens: 2
Perf thin used ratio: 1.0%
Perf thin free ratio: 98.0%
Flow Controller      Requested Tokens    Used Tokens    Over Used Tokens
-----------------  ------------------  -------------  ------------------
1 -> 1                              0              0                   0
2 -> 1                              0              0                   0
3 -> 1                              0              0                   0
4 -> 1                              0              0                   0

[Flow Controller]
Flow Controller    Dest Perf Thin Not Free Ratio      Avail Tokens    Used Tokens No Wait    Used Tokens After Wait    Over Used Tokens    Avg Wait token Lat    Avg Wait token Num
-----------------  -------------------------------  --------------  ---------------------  ------------------------  ------------------  --------------------  --------------------
1 -> 1             2.0%                                   10000000                      0                         0                   0                     0                     0
1 -> 2             7.0%                                   10000000                      0                         0                   0                     0                     0
1 -> 3             7.0%                                   10000000                      0                         0                   0                     0                     0
1 -> 4             2.0%                                   10000000                      0                         0                   0                     0                     0
```

**输出说明**

I/O metric 的输出

| 参数 | 说明 |
| --- | --- |
| `Access Perf Read` | Access 发起的性能层读 I/O。 |
| `Access Perf Write` | Access 发起的性能层写 I/O。 |
| `Access Cap EC Read` | Access 发起的容量层 EC 读 I/O。 |
| `Access Cap EC Write` | Access 发起的容量层 EC 写 I/O。 |
| `Access Cap Replica Read` | Access 发起的容量层副本读 I/O。 |
| `Access Cap Replica Write` | Access 发起的容量层副本写 I/O。 |
| `Access Perf Promote Write` | Access 为凑齐特定大小 I/O 长度而发起的 promote I/O，写性能层的部分。 |
| `Access Cap EC Promote Read` | Access 为凑齐特定大小 I/O 长度而发起的 promote I/O，读容量层 EC 的部分。 |
| `Access Cap Rep Promote Read` | Access 为凑齐特定大小 I/O 长度而发起的 promote I/O，读容量层副本的部分。 |
| `From Remote Perf Read` | 从其他 access 发来的性能层读 I/O。 |
| `From Remote Perf Write` | 从其他 access 发来的性能层写 I/O。 |
| `From Remote Cap EC Read` | 从其他 access 发来的容量层 EC 读 I/O。 |
| `From Remote Cap EC Write` | 从其他 access 发来的容量层 EC 写 I/O。 |
| `From Remote Cap Replica Read` | 从其他 access 发来的容量层副本读 I/O。 |
| `From Remote Cap Replica Write` | 从其他 access 发来的容量层副本写 I/O。 |
| `From Local Perf Read` | 从本地 access 发来的性能层读 I/O。 |
| `From Local Perf Write` | 从本地 access 发来的性能层写 I/O。 |
| `From Local Cap EC Read` | 从本地 access 发来的容量层 EC 读 I/O。 |
| `From Local Cap EC Write` | 从本地 access 发来的容量层 EC 写 I/O。 |
| `From Local Cap Replica Read` | 从本地 access 发来的容量层副本读 I/O。 |
| `From Local Cap Replica Write` | 从本地 access 发来的容量层副本写 I/O。 |

性能层限流 metric 的输出 (flow manager 相关)

| 参数 | 说明 |
| --- | --- |
| `Flow Manager` | 分配 token 的模块，源端 chunk (分配 token) -> 目的端 chunk（申请 token）。 |
| `Flow control enable` | 性能层限流是否已开启。 |
| `Avail token` | 当前空闲 token 的数量。 |
| `Perf thin used ratios` | 当前性能层使用比例。 |
| `Perf thin free ratio` | 当前性能层空闲比例。 |
| `Flow Controller` | 申请 token 的模块，源端 chunk (申请 token) -> 目的端 chunk（分配 token）。 |
| `Requested Tokens` | 最近 1s 累计希望申请 token 的数量（该值可参考性意义较低，一般可以忽略）。 |
| `Used Tokens` | 最近 1s 消费的 token 数量。 |
| `Over Used Tokens` | 最近 1s 没有拿 token 就下发副本 I/O 的数量，一般可能是由于 DataChannel 失联、拿 token 超时等原因。 |

性能层限流 metric 的输出 (flow controller 相关)

| 参数 | 说明 |
| --- | --- |
| `Flow Controller` | 申请 token 的模块，源端 chunk (申请 token) -> 目的端 chunk（分配 token）。 |
| `Dest Perf Thin Not Free Ratio` | 目的端 chunk 的性能层空间使用率。 |
| `Avail Tokens` | 当前时刻持有到目的节点的 tokens。未限速时数值固定为 `10000000`。 |
| `Used Tokens No Wait` | 最近 1s 不需要等待就获得 token 的副本 I/O 数量。 |
| `Used Tokens After Wait` | 最近 1s 需要等待才获得 token 的副本 I/O 数量。 |
| `Over Used Tokens` | 没有拿 token 就下发的副本 I/O 的数量，一般可能是由于 DataChannel 失联、拿 token 超时等原因。 |
| `Avg Wait Token Lat` | 最近 1s 等待 token 的延时。 |
| `Avg Wait Token Num` | 最近 1s 等待 token 的副本 I/O 数量。 |

## 查看本地 chunk 的下沉信息

在集群节点执行如下命令，可查看当前节点的下沉信息：

`zbs-chunk [--ins_id <id>] sink list`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数，物理盘池 ID。可用来在多物理盘池环境下过滤仅输出特定物理盘池的信息。 |

**输出示例**

```
Sink mode: SINK_HIGH
Inactive interval: 900 s
Sink inactive lease: True
Cap directly write policy: CAP_DIO_ALL_THROTTLED
Sinkable block lru info:
  Active blocks: 4914422
  Inactive blocks: 631664
  Clean blocks: 0
  Reserve active blocks: 6556339
Potential sinkable block lru info:
  Active blocks: 0
  Inactive blocks: 0
  Clean blocks: 0
  Reserve active blocks: 6556339
Accelerate cids: [4]
Accelerate blocks: 179
Inactive extents: 11125
Max sink task num: 32
Max sink io concurrency: 32
    lid    lepoch    perf_pid    perf_epoch  perf_location      cur_block_no  type
-------  --------  ----------  ------------  ---------------  --------------  -----------
2729295  13723839     2758531      39830494  [2, 3]                      454  SINK_EXTENT
2900678  13896894     4661280      41724371  [2, 4]                      241  SINK_BLOCK
2961581  14890778     8191744      44708358  [2, 1]                      116  DRAIN_EXTENT
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Sink mode` | 当前节点的下沉档位。 |
| `Inactive interval` | 判定 extent 是否为非活跃状态的时间阈值。 |
| `Sink inactive lease` | 是否对非活跃 extent 进行下沉。 |
| `Cap directly write policy` | 当前节点的容量层直写策略。 |
| `Sinkable block lru info` | 当前节点的可下沉 block LRU 信息。 |
| `Potential sinkable block lru info` | 当前节点的潜在可下沉 block LRU 信息。 |
| `Accelerate cids` | 当前节点感知的需要加速下沉的 chunk 列表。 |
| `Accelerate blocks` | 当前节点感知的需要加速下沉的 block 数量。 |
| `Inactive extents` | 当前节点的非活跃 extent 数量。 |
| `Max sink task num` | 当前节点最大下沉任务数量。 |
| `Max sink io concurrency` | 当前节点最大下沉 I/O 并发数。 |

## 查看本地 chunk 的数据链路信息

在集群节点执行如下命令，可查看当前节点作为客户端与其他节点连接的数据链路信息：

`zbs-chunk dc get_manager_info`

| 参数 | 说明 |
| --- | --- |
| `--dst_ip` | 可选参数，选择是否仅展示指定对端 IP 的数据链路。 |
| `--type` | 可选参数，选择是否仅展示存储网或接入网的数据链路。 |
| `--show_details` | 可选参数，选择是否展示详细信息。 |
| `--show_pids` | 可选参数，选择是否展示每条数据链路上的所有 pid 信息。 |
| `--summary` | 可选参数，选择是否仅展示总结信息。 |

**输出示例**

```
Version: DATA_CHANNEL_V3
Src                  Dst                  Type      Up Time (sec)
-------------------  -------------------  ------  ---------------
10.10.130.72:32830   10.10.130.73:11201   RDMA              52374
10.10.130.72:37114   10.10.130.74:11201   RDMA              54065
10.10.130.72:45090   10.10.130.72:11201   RDMA              54065
10.10.130.72:46660   10.10.130.71:11201   RDMA              53334
10.199.130.72:46482  10.199.130.71:10201  TCP               53334
10.199.130.72:57680  10.199.130.74:10201  TCP               54067
10.199.130.72:59436  10.199.130.73:10201  TCP               52374
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Version` | 数据链路的版本。 |
| `Src` | 数据链路的本端节点使用的 IP 和端口。 |
| `Dst` | 数据链路的对端节点使用的 IP 和端口。 |
| `Type` | 数据链路类型，可为 TCP 或 RDMA。 |
| `Up Time (sec)` | 数据链路的活跃时间。 |

在集群节点执行如下命令，可查看当前节点作为服务端与其他节点连接的数据链路信息：

`zbs-chunk dc get_server_info`

| 参数 | 说明 |
| --- | --- |
| `--show_details` | 可选参数，选择是否展示详细信息。 |

**输出示例**

```
Version: DATA_CHANNEL_V3
Src                  Dst                  Type      Up Time (sec)
-------------------  -------------------  ------  ---------------
10.10.130.72:10201   10.10.130.72:52768   TCP                5551
10.10.130.72:11201   10.10.130.73:45276   RDMA                 26
10.10.130.72:11201   10.10.130.74:46626   RDMA                411
10.10.130.72:11201   10.10.130.72:45090   RDMA              54559
10.10.130.72:11201   10.10.130.71:52162   RDMA              53825
10.199.130.72:10201  10.199.130.73:40152  TCP                  27
10.199.130.72:10201  10.199.130.74:56334  TCP                 413
10.199.130.72:10201  10.199.130.71:55514  TCP               53828
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Version` | 数据链路的版本。 |
| `Src` | 数据链路的本端节点使用的 IP 和端口。 |
| `Dst` | 数据链路的对端节点使用的 IP 和端口。 |
| `Type` | 数据链路类型，可为 TCP 或 RDMA。 |
| `Up Time (sec)` | 数据链路的活跃时间。 |

---

## 管理 chunk > 将某个 chunk 从节点移除

# 将某个 chunk 从节点移除

仅能操作 IDLE 状态的 chunk，即只能移除已经从存储池中移除的 chunk。

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta chunk remove <data_ip> <data_port>`

| 参数 | 说明 |
| --- | --- |
| `data_ip` | 节点存储 IP 地址。 |
| `data_port` | Chunk 使用端口。 |

> **说明**：
>
> 多物理盘池环境下，需要按照物理盘池 ID 从大到小的顺序移除。

**输出说明**

执行成功无输出。

---

## 管理 chunk > 设置 chunk 进入或退出存储维护模式

# 设置 chunk 进入或退出存储维护模式

**操作方法**

在集群任一节点执行如下命令，设置 chunk 进入或退出存储维护模式。

`zbs-meta chunk set_maintenance <cid> <is_maintenance> [--expire_duration_s <EXPIRE_DURATION_S>]`

| 参数 | 说明 |
| --- | --- |
| `cid` | Chunk ID。 |
| `is_maintenance` | 取值为 `true` 或 `false`，分别表示是否进入维护模式。 |
| `--expire_duration_s <EXPIRE_DURATION_S>` | 可选参数，设置维护模式过期时间，仅在进入存储维护模式时有效。如果不设置该参数，则系统默认为最大值 `604800` 秒（7 天）。 |

**输出示例**

```
-----------------------  ----------------------------------------------
ID                       1
IP                       10.2.234.198
Host Name                smtxzbs-5-6-0-b45-el7X0617125715X3
Port                     10200
Storage Pool             system
Use State                IN_USE
Link Status              CONNECTED_ERROR
Data Capacity            602.34 GiB
Valid Space              602.34 GiB
Allocated Space          0.00 B
Failure Data Space       0.00 B
Perf Data Capacity       20.00 GiB
Perf Valid Space         20.00 GiB
Perf Allocated Space     768.00 KiB
Perf Failure Data Space  0.00 B
Registered Date          2024-06-17 14:06:12
LSM Version              2.4.1
Zone                     default
Maintenance Mode         True
-----------------------  ----------------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Storage Pool` | 所属存储池。 |
| `Use State` | 使用状态。 |
| `Link Status` | 连接状态。 |
| `Data Capacity` | 容量层提供的总数据空间大小。 |
| `Valid Space` | 容量层有效数据空间大小。 |
| `Allocated Space` | 容量层已分配的数据空间大小（meta 认为的空间消耗）。 |
| `Failure Data Space` | 容量层失效数据空间大小。 |
| `Perf Data Capacity` | 性能层提供的总数据空间大小。 |
| `Perf Valid Space` | 性能层有效数据空间大小。 |
| `Perf Allocated Space` | 性能层已分配的数据空间大小（meta 认为的空间消耗）。 |
| `Perf Failure Data Space` | 性能层失效数据空间大小。 |
| `Registered Date` | 注册时间。 |
| `LSM Version` | LSM 版本。 |
| `Zone` | 所属可用域。 |
| `Maintenance Mode` | 是否处于维护模式。 |

---

## 管理 chunk > 设置 chunk 的数据校验模式

# 设置 chunk 的数据校验模式

**操作方法**

在集群节点执行如下命令，设置该节点全部或特定物理盘池 chunk 的数据校验模式：

`zbs-chunk [--ins_id <id>] verify {none|log|crash}`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数，物理盘池 ID。指定需要设置的物理盘池，默认将对当前节点上全部物理盘池的 chunk 进行设置。 |
| `none` | 不校验数据。 |
| `log` | 校验数据，并将发现的问题以日志的方式记录。 |
| `crash` | 校验数据，并且当发现问题时直接退出。 |

**输出说明**

执行成功无输出。

---

## 管理 chunk > 重新加载 chunk 配置或更新 Zookeeper 信息

# 重新加载 chunk 配置或更新 Zookeeper 信息

**操作方法**

在集群节点执行如下命令：

`zbs-chunk config {reload|show_zk_hosts|reload_hostname}`

| 参数 | 说明 |
| --- | --- |
| `reload` | 更新 Zookeeper 信息。 |
| `show_zk_hosts` | 显示当前 Zookeeper hosts 列表。 |
| `reload_hostname` | 重新加载主机名。 |

**输出示例**

```
zk_hosts: 10.139.57.103:2181,10.139.57.104:2181,10.139.57.105:2181
```

---

## 管理 chunk > 查看或清除异常物理盘记录

# 查看或清除异常物理盘记录

**操作方法**

在集群节点执行如下命令：

`zbs-chunk rejection {list | revoke }`

| 参数 | 说明 |
| --- | --- |
| `list` | 查看异常物理盘。 |
| `revoke` | 清除异常物理盘记录。 |

**输出示例**

```
no rejection items
```

---

## 管理 chunk > 更新本地 chunk 的次级数据网络 IP

# 更新本地 chunk 的次级数据网络 IP

**操作方法**

在当前集群节点执行如下命令，更新本地 chunk 的次级数据网络 IP。

`zbs-chunk address update_secondary_data_ip <ip>`

**输出说明**

执行成功无输出。

---

## 管理 chunk > 查看 chunk 线程轮询状态

# 查看 chunk 线程轮询状态

**操作方法**

在当前节点执行如下命令，查看本地 chunk 线程轮询状态。按 ctrl + c 退出执行。

`zbs-chunk tool show_polling_stats`

**输出示例**

```
zbs-chunk tool show_polling_stats
Tid CPU NUMA Name Busy_tsc Idle_tsc Busy(%)
======================================================================
42187 10 0 c1-chunk-dcc 100528374 3698639286 2.65%
42153 1 0 c1-chunk-main 137681042 3661487410 3.62%
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Tid` | 线程 ID。 |
| `CPU` | 线程运行的 CPU。 |
| `NUMA` | 线程运行的 NUMA 节点。 |
| `Name` | 线程名称。 |
| `Busy_tsc` | 繁忙时间（单位 tick）。 |
| `Idle_tsc` | 空闲时间（单位 tick）。 |
| `Busy` | 线程繁忙程度，即繁忙时间 / （繁忙时间 + 空闲时间）\* 100%。 |

---

## 管理块存储服务 > 管理存储池

# 管理存储池

存储池是 ZBS 对存储介质进行组织的单元。不同的存储介质可以加入不同的存储池，使得存储池具备不同的存储特性，例如：SSD/HDD 混合存储池，全 SSD 存储池等（在目前 ZBS 的实现中，服务器是可以加入存储池的最小单元）。也可以指定某一个数据存储、NFS Export 或 iSCSI 目标到某一个特定的存储池，然后其上的数据卷都会存放在指定存储池的 chunk 上。系统默认的存储池是 “system”。用户可以把存储池的 chunk 移动到另一个存储池。

存储池提供了数据物理隔离的能力，一份数据的所有副本，都会保存在同一个存储池中。数据在存储池之间并不共享。如果数据需要在存储池之间进行移动，需要触发数据拷贝。

## 查看集群当前所有存储池

**操作方法**

在集群任一节点执行如下命令，可查看集群当前所有存储池：

`zbs-meta storage_pool list`

**输出示例**

```
id      name    chunks
------  ------  --------
system  system  3,2,1
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `id` | 存储池 ID。 |
| `name` | 存储池名称。 |
| `chunks` | 存储池的 chunk。 |

## 查看指定存储池的属性

**操作方法**

在集群任一节点执行如下命令，查看指定 ID 的存储池的属性：

`zbs-meta storage_pool show <storage_pool_id>`

**输出示例**

```
------  ------
id      system
name    system
chunks  3,2,1
------  ------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `id` | 存储池 ID。 |
| `name` | 存储池名称。 |
| `chunks` | 存储池的 chunk。 |

## 创建存储池

**操作方法**

在集群任一节点执行如下命令，创建指定名称的存储池：

`zbs-meta storage_pool create <storage_pool name>`

**输出说明**

执行成功无输出。

## 删除存储池

**操作方法**

在集群任一节点执行如下命令，删除指定 ID 的存储池：

`zbs-meta storage_pool delete <storage_pool id>`

**输出说明**

执行成功无输出。

## 更新存储池名称

**操作方法**

在集群任一节点执行如下命令，更新指定 ID 的存储池的名称：

`zbs-meta storage_pool update <storage_pool_id> <new_name>`

**输出说明**

执行成功无输出。

## 在存储池中添加 chunk

**操作方法**

在集群任一节点执行如下命令，在存储池中添加 chunk。

`zbs-meta storage_pool add_chunk <storage_pool_id> <chunk_id>`

**输出说明**

执行成功无输出。

## 在存储池中移除 chunk

**操作方法**

在集群任一节点执行如下命令，将 chunk 从存储池中移除。

`zbs-meta storage_pool remove_chunk <storage_pool_id> <chunk_id>`

**输出说明**

执行成功无输出。

## 取消 chunk 从存储池中移除

在 chunk 还未从存储池中完成移除时，可使用如下命令取消移除操作。

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta storage_pool cancel_remove <chunk_id>`

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理数据存储

# 管理数据存储

数据存储（Datastore）是一组存储卷的集合。数据存储中包含的存储卷都具有相同的存储策略，例如副本数、精简配置等。

## 查看集群中全部数据存储

**操作方法**

在集群任一节点执行如下命令，查看集群中全部数据存储的信息：

`zbs-meta pool list`

**输出示例**

```
ID                                    Name                                                                Storage Pool    Creation Time                  Resiliency Type    Encrypt Method        Replica#  EC Param    Thin    Export    Description         Whitelist                            Is Prioritized
------------------------------------  ------------------------------------------------------------------  --------------  -----------------------------  -----------------  ------------------  ----------  ----------  ------  --------  ------------------  -----------------------------------  ----------------
b248894b-32ab-4ec5-8239-69cdaecdba46  zbs-iscsi-datastore-bacd3e5a-596d-41b3-aa6b-ad8c879db00b            system          2024-12-17 11:44:07.665726649  RT_REPLICA         ENCRYPT_PLAIN_TEXT           2              True    False                         10.17.92.13,10.17.92.12,10.17.92.11  False
cd8e5073-4c33-4022-bc6a-3717054fa30c  default                                                             system          2024-12-16 16:28:08.277991975  RT_REPLICA         ENCRYPT_PLAIN_TEXT           2              True    False                         */*                                  False
d268f50a-77f9-42fc-9b3a-b228d6b1c3ed  encrypt_pool                                                        system          2024-12-30 14:57:58.159887452  RT_REPLICA         ENCRYPT_AES256_CTR           2              True    False                         */*                                  False
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Name` | 数据存储名称。 |
| `Storage Pool` | 数据存储所属存储池。 |
| `Resiliency Type` | 数据存储的冗余模式。 |
| `Replica#` | 数据存储的副本数。 |
| `Encrypt Method` | 数据存储的加密方法。 |
| `EC Param` | 数据存储在 EC 冗余模式下对应的 EC 参数。 |
| `Thin` | 数据存储是否为精简置备。 |
| `Export` | 是否为 NFS Export。 |
| `Whitelist` | 数据存储的白名单。 |
| `Is Prioritized` | 是否采用常驻缓存。 |

## 查看某个数据存储

**操作方法**

在集群任一节点执行如下命令，查看某个数据存储的详细信息：

- 通过数据存储名称查看：

  `zbs-meta pool show <pool_name>`
- 通过 Pool ID 查看：

  `zbs-meta pool show_by_id <pool_id>`

**输出示例**

```
---------------  ------------------------------------
ID               3fec5d68-0e2d-4ca8-9022-fd6b5a88617f
Name             default
Storage Pool     system
Creation Time    2024-06-17 14:06:08.359138865
Resiliency Type  RT_REPLICA
Encrypt Method   ENCRYPT_PLAIN_TEXT
Replica#         2
EC Param
Thin             True
Export           False
Description
Whitelist        */*
Is Prioritized   False
---------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Name` | 数据存储名称。 |
| `Storage Pool` | 数据存储所属存储池。 |
| `Resiliency Type` | 数据存储的冗余模式。 |
| `Replica#` | 数据存储的副本数。 |
| `Encrypt Method` | 数据存储的加密方法。 |
| `EC Param` | 数据存储在 EC 冗余模式下对应的 EC 参数。 |
| `Thin` | 数据存储是否为精简置备。 |
| `Export` | 是否为 NFS Export。 |
| `Whitelist` | 数据存储的白名单。 |
| `Is Prioritized` | 是否采用常驻缓存。 |

## 创建数据存储

**操作方法**

在集群任一节点执行如下命令，创建指定名称的数据存储：

```
zbs-meta pool create <pool_name> [--resiliency_type <RESILIENCY_TYPE>]
					   [--replica_num <REPLICA_NUM>] [--ec_algo <EC_ALGO>]
                       [--encrypt_method <ENCRYPT_METHOD>]
					   [--ec_k <EC_K>] [--ec_m <EC_M>]
					   [--thin_provision <THIN_PROVISION>] [--desc <DESC>]
					   [--storage_pool_id <STORAGE_POOL_ID>]
					   [--whitelist <WHITELIST>] [--iops <IOPS>]
					   [--iops_rd <IOPS_RD>] [--iops_wr <IOPS_WR>]
					   [--iops_max <IOPS_MAX>]
					   [--iops_rd_max <IOPS_RD_MAX>]
					   [--iops_wr_max <IOPS_WR_MAX>]
					   [--iops_max_length <IOPS_MAX_LENGTH>]
					   [--iops_rd_max_length <IOPS_RD_MAX_LENGTH>]
					   [--iops_wr_max_length <IOPS_WR_MAX_LENGTH>]
					   [--iops_io_size <IOPS_IO_SIZE>] [--bps <BPS>]
					   [--bps_rd <BPS_RD>] [--bps_wr <BPS_WR>]
					   [--bps_max <BPS_MAX>] [--bps_rd_max <BPS_RD_MAX>]
					   [--bps_wr_max <BPS_WR_MAX>]
					   [--bps_max_length <BPS_MAX_LENGTH>]
					   [--bps_rd_max_length <BPS_RD_MAX_LENGTH>]
					   [--bps_wr_max_length <BPS_WR_MAX_LENGTH>]
					   [--prioritized <PRIORITIZED>]
```

| 参数 | 说明 |
| --- | --- |
| `pool_name` | 数据存储名称。 |
| `--resiliency_type <RESILIENCY_TYPE>` | 设置冗余模式，副本或 EC，默认为 `None`。 |
| `--replica_num <REPLICA_NUM>` | 设置数据存储内新建存储卷的默认副本数，可设置为 2 副本或 3 副本。 |
| `--ec_algo <EC_ALGO>` | 设置 EC 算法，当冗余模式为 EC 时必须设置，默认为 `RS`。 |
| `--encrypt_method <ENCRYPT_METHOD>` | 设置数据加密方法，默认为不加密 。 |
| `--ec_k <EC_K>` | 设置 EC 算法参数 K，参数范围为 `[2，23]`，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--ec_m <EC_M>` | 设置 EC 算法参数 M，参数范围为 `[1，4]`，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--thin_provision <THIN_PROVISION>` | `True` 或 `False`，表示是否设置数据存储新建存储卷的置备方式为精简置备。 |
| `--desc <DESC>` | 设置数据存储描述。 |
| `--storage_pool_id <STORAGE_POOL_ID>` | 指定创建数据存储的存储池 ID。 |
| `--whitelist <WHITELIST>` | IP 访问白名单。 |
| `--iops <IOPS>` | 设置数据存储内新建存储卷的总 IOPS 上限值。 |
| `--iops_rd <IOPS_RD>` | 设置读 IOPS 的上限值。 |
| `--iops_wr <IOPS_WR>` | 设置写 IOPS 的上限值。 |
| `--iops_max <IOPS_MAX>` | 设置总 IOPS 突发的上限值。 |
| `--iops_rd_max <IOPS_RD_MAX>` | 设置读 IOPS 突发的上限值。 |
| `--iops_wr_max <IOPS_WR_MAX>` | 设置写 IOPS 突发的上限值。 |
| `--iops_max_length <IOPS_MAX_LENGTH>` | 设置总 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_rd_max_length <IOPS_RD_MAX_LENGTH>` | 设置读 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_wr_max_length <IOPS_WR_MAX_LENGTH>` | 设置写 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_io_size <IOPS_IO_SIZE>` | 使用 IOPS 限速时，假定的平均 I/O 数据量大小。 |
| `--bps <BPS>` | 设置数据存储内新建存储卷的总带宽限制，单位为 Bps。 |
| `--bps_rd <BPS_RD>` | 设置读带宽的上限值。 |
| `--bps_wr <BPS_WR>` | 设置写带宽的上限值。 |
| `--bps_max <BPS_MAX>` | 设置总带宽在发生 I/O 突发时的上限值。 |
| `--bps_rd_max <BPS_RD_MAX>` | 设置读带宽在发生 I/O 突发时的上限值。 |
| `--bps_wr_max <BPS_WR_MAX>` | 设置写带宽在发生 I/O 突发时的上限值。 |
| `--bps_max_length <BPS_MAX_LENGTH>` | 设置在发生 I/O 突发时，以总带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_rd_max_length <BPS_RD_MAX_LENGTH>` | 设置在发生 I/O 突发时，以读带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_wr_max_length <BPS_WR_MAX_LENGTH>` | 设置在发生 I/O 突发时，以写带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--prioritized <PRIORITIZED>` | 设置在数据存储内创建存储卷时是否默认开启常驻缓存，可设置为`True` 或 `False`。 |

**输出示例**

```
---------------  ------------------------------------
ID               559a383d-e24f-4ba3-b685-bb417174b612
Name             pool4
Storage Pool     system
Creation Time    2024-06-18 14:19:25.455244549
Resiliency Type  RT_REPLICA
Encrypt Method   ENCRYPT_PLAIN_TEXT
Replica#         2
EC Param
Thin             True
Export           False
Description
Whitelist        */*
Is Prioritized   False
---------------  ------------------------------------
```

## 更新数据存储

**操作方法**

在集群任一节点执行如下命令，更新数据存储名称、副本数、置备模式和 IP 白名单。更新数据存储不影响已经创建的存储卷。

`zbs-meta pool update [--new_pool_name <NEW_POOL_NAME>] [--replica_num <REPLICA_NUM>] [--thin_provision {true|false}] [--desc <DESC>] [--whitelist <WHITELIST>] [--encrypt_method <ENCRYPT_METHOD>] <pool_name>`

| 参数 | 说明 |
| --- | --- |
| `--new_pool_name` | 可选参数，更新数据存储名称。 |
| `--replica_num` | 可选参数，更新数据存储中存储卷的默认副本数，不影响已经创建好的存储卷。 |
| `--thin_provision {true|false}` | 可选参数，更新数据存储中存储卷的默认置备模式，`true` 和 `false` 表示是否为精简配置。 |
| `--desc` | 可选参数，更新数据存储的详细描述。 |
| `--whitelist` | 可选参数，IP 访问白名单。 |
| `--encrypt_method` | 可选参数，更新数据加密方法。 |
| `pool_name` | 必选参数，原数据存储名称。 |

**输出说明**

执行成功无输出。

## 删除数据存储

**操作方法**

在集群任一节点执行如下命令，删除指定名称的数据存储：

`zbs-meta pool delete <pool_name>`

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理存储卷

# 管理存储卷

存储卷（volume），是 ZBS 对外提供的最基本的数据结构。它可以对应到一个虚拟机的存储卷，也可以对应到 iSCSI 中的一个 LUN。用户可以通过存储卷来创建虚拟机或者对虚拟机进行添加磁盘的操作。这一切都是基于存储卷进行的，volume 参数可以让用户直接对存储卷进行操作。

---

## 管理块存储服务 > 管理存储卷 > 查看存储卷

# 查看存储卷

## 查看集群所有存储卷信息

**操作方法**

在集群任一节点执行如下命令，查看集群中所有存储卷信息，或单个存储卷的信息：

`zbs-meta volume listall [pool_name]`

当 `pool_name` 为空时查看整个集群所有存储卷信息。当 `pool_name` 不为空时，查看指定存储卷信息。

**输出示例**

```
ID                                    Name                                  Parent ID                             Pool Name                                                 Size         Perf Unique Size    Perf Shared Size    Cap Unique Size    Cap Shared Size    Logical Used Size    Creation Time                  Status         Resiliency Type    Encrypt Method      Encrypt Metadata Id      Replica Num  EC Param    Thin Provision    Read Only    Description    Alloc Even      Clone count    Prefer CID  Access Points    Is Prioritized    Downgraded PRS
------------------------------------  ------------------------------------  ------------------------------------  --------------------------------------------------------  -----------  ------------------  ------------------  -----------------  -----------------  -------------------  -----------------------------  -------------  -----------------  ------------------  ---------------------  -------------  ----------  ----------------  -----------  -------------  ------------  -------------  ------------  ---------------  ----------------  ----------------
9dd3d94c-68ed-49e7-bddc-44ead6379725  9dd3d94c-68ed-49e7-bddc-44ead6379725  74bc8b9e-4e3d-41ce-89df-985a1ace9e90  44c8861c-8d10-45e0-a933-ad32a5202d25                      1024.00 MiB  0.00 B              0.00 B              3.00 MiB           0.00 B             1024.00 KiB          2024-12-05 20:49:42.296145302  VOLUME_ONLINE  RT_REPLICA         ENCRYPT_PLAIN_TEXT  None                               3              True              False                       False                     0             0  []               False             0.00 B
192fc562-df2d-43d0-ae7e-9350addcd2ee  encrypted_volume                      e691d599-e506-42ad-aa8a-473580b15d51  encrypted_pool                                            1024.00 GiB  0.00 B              0.00 B              0.00 B             0.00 B             0.00 B               2025-01-06 15:09:07.156447863  VOLUME_ONLINE  RT_REPLICA         ENCRYPT_AES256_CTR  4260                               2              True              False                       False                     0             0  []               False             0.00 B
5847b867-bc66-4cdc-a145-7d751f219ca3  5847b867-bc66-4cdc-a145-7d751f219ca3  e2ec7cc1-b2eb-474b-bb51-4a331547e986  guyi-target-1                                             30.00 GiB    0.00 B              0.00 B              0.00 B             0.00 B             0.00 B               2024-12-31 14:32:53.274472838  VOLUME_ONLINE  RT_REPLICA         ENCRYPT_PLAIN_TEXT  None                               2              True              False                       False                     0             0  []               False             0.00 B             0  []               False             0.00 B
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Parent ID` | 存储卷所属 pool ID。 |
| `Size` | 存储卷大小。 |
| `Perf Unique Size` | 存储卷独占的性能层空间大小。 |
| `Perf Shared Size` | 存储卷和其他存储卷或快照共享的性能层空间大小。 |
| `Cap Unique Size` | 存储卷独占的容量层空间大小。 |
| `Cap Shared Size` | 存储卷和其他存储卷或快照共享的容量层空间大小。 |
| `Logical Used Size` | 存储卷已经分配的逻辑空间大小。 |
| `Status` | 存储卷状态。 |
| `Resiliency Type` | 存储卷的冗余模式。 |
| `Encrypt Method` | 存储卷的数据加密算法。 |
| `Encrypt Metadata Id` | 存储卷的加密元数据 ID。 |
| `Replica Num` | 副本数量。 |
| `EC Param` | 存储卷在 EC 冗余模式下对应的 EC 参数。 |
| `Thin Provision` | 是否为精简置备。 |
| `Read Only` | 存储卷是否只读。 |
| `Alloc Even` | 存储卷所属副本是否均匀分配。 |
| `Clone count` | 该存储卷克隆的次数。 |
| `Prefer CID` | I/O 亲和 chunk，存储卷的 extent 会更倾向于存储在该 chunk上。 |
| `Access Points` | 存储卷的访问接入点。 |
| `Is Prioritized` | 存储卷的数据是否都需要维持在性能层中。 |
| `Downgraded PRS` | 存储卷的尚未提升到性能层的空间大小。 |

## 查看某个数据存储中的存储卷信息

**操作方法**

执行如下命令，查看某个数据存储中的存储卷信息：

`zbs-meta volume list <pool_name>`

**输出示例**

```
ID                                    Name              Parent ID                             Size         Perf Unique Size    Perf Shared Size    Cap Unique Size    Cap Shared Size    Logical Used Size    Creation Time                  Status         Resiliency Type    Encrypt Method      Encrypt Metadata Id      Replica Num  EC Param    Thin Provision    Read Only    Description    Alloc Even      Clone count    Prefer CID  Access Points    Is Prioritized    Downgraded PRS
------------------------------------  ----------------  ------------------------------------  -----------  ------------------  ------------------  -----------------  -----------------  -------------------  -----------------------------  -------------  -----------------  ------------------  ---------------------  -------------  ----------  ----------------  -----------  -------------  ------------  -------------  ------------  ---------------  ----------------  ----------------
45e912c6-cb2d-4803-954c-3f402445a7f5  encrypted_volume  8a21c3e0-7324-41e2-a3b2-1bf858d851ec  1024.00 GiB  In Process          In Process          In Process         In Process         In Process           2025-01-06 15:27:14.358870889  VOLUME_ONLINE  RT_REPLICA         ENCRYPT_AES256_CTR  4261                               2              True              False                       False                     0             0  []               False             0.00 B
8d6167dd-a2c5-4a52-882b-6721946a9015  plain_volume      8a21c3e0-7324-41e2-a3b2-1bf858d851ec  1024.00 GiB  In Process          In Process          In Process         In Process         In Process           2025-01-06 15:27:27.394580981  VOLUME_ONLINE  RT_REPLICA         ENCRYPT_PLAIN_TEXT  None                               2              True              False                       False                     0             0  []               False             0.00 B
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Parent ID` | 存储卷所属 pool ID。 |
| `Size` | 存储卷大小。 |
| `Perf Unique Size` | 存储卷独占的性能层空间大小。 |
| `Perf Shared Size` | 存储卷和其他存储卷或快照共享的性能层空间大小。 |
| `Cap Unique Size` | 存储卷独占的容量层空间大小。 |
| `Cap Shared Size` | 存储卷和其他存储卷或快照共享的容量层空间大小。 |
| `Logical Used Size` | 存储卷已经分配的逻辑空间大小。 |
| `Status` | 存储卷状态。 |
| `Resiliency Type` | 存储卷的冗余模式。 |
| `Encrypt Method` | 存储卷的数据加密算法。 |
| `Encrypt Metadata Id` | 存储卷的加密元数据 ID。 |
| `Replica Num` | 副本数量。 |
| `EC Param` | 存储卷在 EC 冗余模式下对应的 EC 参数。 |
| `Thin Provision` | 是否为精简置备。 |
| `Read Only` | 存储卷是否只读。 |
| `Alloc Even` | 存储卷所属副本是否均匀分配。 |
| `Clone count` | 该存储卷克隆的次数。 |
| `Prefer CID` | I/O 亲和 chunk，存储卷的 extent 会更倾向于存储在该 chunk上。 |
| `Access Points` | 存储卷的访问接入点。 |
| `Is Prioritized` | 存储卷的数据是否都需要维持在性能层中。 |
| `Downgraded PRS` | 存储卷的尚未提升到性能层的空间大小。 |

## 查看集群中拥有特定属性的存储卷

**操作方法**

在集群任一节点执行如下命令，查看拥有特定属性的存储卷：

`zbs-meta volume find <volume-status>`

| 参数 | 说明 |
| --- | --- |
| `volume-status` | 查找指定状态的卷：  - `even`：集群中分配策略为 even 的卷。 - `need_elevate`：集群中需要进行提升的缓存预留卷。 |

**输出示例**

```
[root@node35 16:52:54 ~]$zbs-meta volume find even
ID                                    Name                                                                                   Parent ID                             Size         Perf Unique Size    Perf Shared Size    Cap Unique Size    Cap Shared Size    Logical Used Size    Creation Time                  Status         Resiliency Type      Replica Num  EC Param    Thin Provision    Read Only    Description    Alloc Even      Clone count    Prefer CID  Access Points    Is Prioritized    Downgraded PRS
------------------------------------  -------------------------------------------------------------------------------------  ------------------------------------  -----------  ------------------  ------------------  -----------------  -----------------  -------------------  -----------------------------  -------------  -----------------  -------------  ----------  ----------------  -----------  -------------  ------------  -------------  ------------  ---------------  ----------------  ----------------
005fd3ad-4cb2-49f3-af81-e932938fdb78  jp-test-centos-template-1-clo4573zf02z21wud5fpjegse                                    1815f208-6062-437f-bbc3-2a773b7b16df  40.00 GiB    In Process          In Process          In Process         In Process         In Process           2023-10-24 17:46:56.637390550  VOLUME_ONLINE  RT_REPLICA                     2              True              False                       False                    10             0  []               False             0.00 B
00cc4a36-81ba-4095-a074-93c7f0cd8a2d  cloudinit_clout-init_windows7-scsi-bios_cloud-init_1_1_1-clps78hrc1hug1wud91d46n0w     8b78623c-abd3-40b5-92ec-a839c545bddc  15.00 GiB    In Process          In Process          In Process         In Process         In Process           2023-12-05 18:30:10.952332837  VOLUME_ONLINE  RT_REPLICA                     2              True              False                       False                    11             0  []               False             0.00 B
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Parent ID` | 存储卷所属 pool ID。 |
| `Size` | 存储卷大小。 |
| `Perf Unique Size` | 存储卷独占的性能层空间大小。 |
| `Perf Shared Size` | 存储卷和其他存储卷或快照共享的性能层空间大小。 |
| `Cap Unique Size` | 存储卷独占的容量层空间大小。 |
| `Cap Shared Size` | 存储卷和其他存储卷或快照共享的容量层空间大小。 |
| `Logical Used Size` | 存储卷已经分配的逻辑空间大小。 |
| `Status` | 存储卷状态。 |
| `Resiliency Type` | 存储卷的冗余模式。 |
| `Encrypt Method` | 存储卷的数据加密算法。 |
| `Encrypt Metadata Id` | 存储卷的加密元数据 ID。 |
| `Replica Num` | 副本数量。 |
| `EC Param` | 存储卷在 EC 冗余模式下对应的 EC 参数。 |
| `Thin Provision` | 是否为精简置备。 |
| `Read Only` | 存储卷是否只读。 |
| `Alloc Even` | 存储卷所属副本是否均匀分配。 |
| `Clone count` | 该存储卷克隆的次数。 |
| `Prefer CID` | I/O 亲和 chunk，存储卷的 extent 会更倾向于存储在该 chunk 上。 |
| `Access Points` | 存储卷的访问接入点。 |
| `Is Prioritized` | 存储卷的数据是否都需要维持在性能层中。 |
| `Downgraded PRS` | 存储卷的尚未提升到性能层的空间大小。 |

## 查看当前正在进行提升的缓存预留卷

目前块存储服务在同一时间只会进行一个提升任务，每个提升任务将一个缓存预留卷的数据从容量层提升到性能层。

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta elevate show`

**输出示例**

```
# zbs-meta elevate show
---------  ------------------------------------
Volume ID  c8b4ef94-6d7d-4898-afb8-3c92c6fb9657
---------  ------------------------------------

Running Cmds:
  LExtent ID    VExtent No
------------  ------------
           9             0
          10             1
          11             2
          12             3
          13             4
          14             5
          15             6

Pending Cmds:
  LExtent ID    VExtent No
------------  ------------
          25            16
          26            17
          27            18
          28            19
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Volume ID` | 被提升的卷的 ID。 |
| `Running Cmds` | 已经被下发到节点的提升指令。 |
| `Pending Cmds` | 尚未被下发到节点的提升指令。 |

## 查看节点活跃访问的的存储卷

在集群任一节点执行如下命令，查看集群中某个或所有节点活跃访问的存储卷信息：

`zbs-meta volume list_access_record [--page_index PAGE_INDEX] [--page_size PAGE_SIZE] [cid]`

| 参数 | 说明 |
| --- | --- |
| `--page_index` | 存储卷信息较多时会分页显示，此参数表示分页的起始页码，默认为 `0`。 |
| `--page_size` | 存储卷信息较多时会分页展示，此参数表示每个分页显示的行数，默认为 `1024`。 |
| `cid` | 可选参数，节点的 chunk ID，默认为 `0`。当取值为 `0` 时，仅显示集群中每个节点活跃访问的存储卷数量，其他情况显示 `cid` 对应节点的活跃访问存储卷信息。 |

**输出示例**

```
zbs-meta volume list_access_record 12

Total record in all nodes is 28. Node:10.0.128.12 's volume_access_record is 1.
Cur page start at 0, cur page size is 1024.
node_ip      cids    volume_id                               last_report_s    report_count
-----------  ------  ------------------------------------  ---------------  --------------
10.0.128.12  11,12   951033b1-fed5-4bfa-a1df-2d7480c86e38            44948               1
```

```
zbs-meta volume list_access_record

Total record in all nodes is 28.
Node:10.0.128.10 's volume_access_record is 1.
Node:10.0.128.11 's volume_access_record is 1.
Node:10.0.128.12 's volume_access_record is 1.
Node:10.0.128.25 's volume_access_record is 4.
Node:10.0.128.26 's volume_access_record is 4.
Node:10.0.128.27 's volume_access_record is 17.
```

## 查看虚拟机关联的虚拟卷信息

**操作方法**

在任意节点执行如下命令，查看与某个虚拟机对应的 ZBS 卷的相关信息。

`zbs-tool elf show_vol_by_vm_id <elf_vm_uuid>`

| 参数 | 说明 |
| --- | --- |
| `elf_vm_uuid` | 虚拟机的 UUID。 |

**输出示例**

```
zbs-tool get_zbs_vol_by_elf_vol_uuid f796cef6-1b19-4f0e-b46d-9dbc8099609c
ELF Volume UUID                       Volume ID                             Size        Perf Unique Size    Perf Shared Size    Cap Unique Size    Cap Shared Size      Prefer CID
------------------------------------  ------------------------------------  ----------  ------------------  ------------------  -----------------  -----------------  ------------
f796cef6-1b19-4f0e-b46d-9dbc8099609c  035b26a8-baf0-410e-93ac-b8bc5fd7ea5c  400.00 GiB  4.02 GiB            43.54 GiB           0.00 B             11.50 GiB                     0
f796cef6-1b19-4f0e-b46d-9dbc8099609d  035b26a8-baf0-410e-93ac-b8bc5fd7ea5d  400.00 GiB  4.02 GiB            43.54 GiB           0.00 B             11.50 GiB                     0
f796cef6-1b19-4f0e-b46d-9dbc8099609e  035b26a8-baf0-410e-93ac-b8bc5fd7ea5e  400.00 GiB  4.02 GiB            43.54 GiB           0.00 B             11.50 GiB                     0
f796cef6-1b19-4f0e-b46d-9dbc8099609f  035b26a8-baf0-410e-93ac-b8bc5fd7ea5f  400.00 GiB  4.02 GiB            43.54 GiB           0.00 B             11.50 GiB                     0
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `ELF Volume UUID` | 虚拟卷的 UUID。 |
| `Volume ID` | 虚拟卷对应的 ZBS 卷 ID。 |
| `Size` | 存储卷大小。 |
| `Perf Unique Size` | 存储卷独占的性能层空间大小。 |
| `Perf Shared Size` | 存储卷和其他存储卷或快照共享的性能层空间大小。 |
| `Cap Unique Size` | 存储卷独占的容量层空间大小。 |
| `Cap Shared Size` | 存储卷和其他存储卷或快照共享的容量层空间大小。 |
| `Prefer CID` | I/O 亲和 chunk，存储卷的 extent 会更倾向于存储在该 chunk上。 |

## 查看虚拟卷 ID 对应的 ZBS 卷 ID

**操作方法**

在任意节点执行如下命令，查看与某个虚拟卷对应的 ZBS 卷 ID。

`zbs-tool elf get_zbs_vol_by_elf_vol_uuid <elf_vol_uuid>`

| 参数 | 说明 |
| --- | --- |
| `elf_vol_uuid` | 虚拟卷的 UUID。 |

**输出示例**

```
zbs-tool elf get_zbs_vol_by_elf_vol_uuid f796cef6-1b19-4f0e-b46d-9dbc8099609c
-------------  ------------------------------------
Volume UUID    f796cef6-1b19-4f0e-b46d-9dbc8099609c
Zbs Volume ID  035b26a8-baf0-410e-93ac-b8bc5fd7ea5c
-------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Volume UUID` | 虚拟卷的 UUID。 |
| `Zbs Volume ID` | 虚拟卷对应的 ZBS 卷 ID。 |

## 查看存储卷数据在缓存分区和数据分区上的分布情况

**操作方法**

- 在集群任一节点执行如下命令，查看指定名称的存储卷的数据在缓存分区和数据分区上的分布情况：

  `zbs-tool volume show_dist <pool_name> <volume_name>`
- 在集群任一节点执行如下命令，查看指定 ID 的存储卷的数据在缓存分区和数据分区上的分布情况：

  `zbs-tool volume show_dist_by_id <volume_id>`

**输出示例**

```
Volume used performance cache size: 1024.00 MiB
Volume used read cache size: 1024.00 KiB
Volume used partition size: 1024.00 MiB
```

---

## 管理块存储服务 > 管理存储卷 > 查看存储卷上的数据块信息

# 查看存储卷上的数据块信息

查看存储卷的 LExtent 和 PExtent，以及 PExtent 在各个 chunk 上的副本数量。

**操作方法**

- 在集群任一节点执行如下命令，查看指定名称的存储卷的 extent 信息：

  `zbs-meta volume show <pool_name> <volume_name> [--show_lextents] [--show_pextents] [--show_replica_distribution]`
- 在集群任一节点执行如下命令，查看指定 ID 的存储卷的 extent 信息：

  `zbs-meta volume show_by_id <volume_id> [--show_lextents] [--show_pextents] [--show_replica_distribution]`

| 参数 | 说明 |
| --- | --- |
| `--show_lextents` | 可选参数，选择是否显示存储卷的 LExtent 信息。 |
| `--show_pextents` | 可选参数，选择是否显示存储卷的 PExtent 信息。 |
| `--show_replica_distribution` | 可选参数，选择是否显示该存储卷的 PExtents 在各个 chunk 上的副本数量。 |

**输出示例**

```
-----------------  ------------------------------------
ID                 83f70467-3b24-4495-bc83-f542238ad7d7
Name               83f70467-3b24-4495-bc83-f542238ad7d7
Parent ID          d821c3d7-0dfa-4cbb-b946-cecb46815115
Size               1024.00 GiB
Perf Unique Size   5.50 MiB
Perf Shared Size   0.00 B
Cap Unique Size    719.11 GiB
Cap Shared Size    0.00 B
Logical Used Size  359.55 GiB
Creation Time      2024-06-05 17:22:28.397537266
Status             VOLUME_ONLINE
Resiliency Type    RT_REPLICA
Replica Num        2
EC Param
Thin Provision     True
Read Only          False
Description
Alloc Even         False
Clone count        0
Iops               0
Iops Read          0
Iops Write         0
Bps                0
Bps Read           0
Bps Write          0
Stripe Num         4
Stripe Size        262144
Prefer CID         0
Access Points      []
Is Prioritized     False
Downgraded PRS     0.00 B
-----------------  ------------------------------------
```

```
LExtent ID     Epoch  Ever Exist      Perf PID    Perf Epoch    Cap ID    Cap Epoch    Lease Owner  Is Prioritized
------------  --------  ------------  ----------  ------------  --------  -----------  -------------  ----------------
     3080352  14149839  True             3393731      45495047   5023870     42086915              4  False
     3080353  14149840  True                   0             0   5023871     42086916              4  False
     3080354  14149841  True                   0             0   5023872     42086917              0  False
     3080355  14149842  True                   0             0   5023873     42086918              0  False
```

```
     ID  Replica    Alive Replica    Temporary Replica    Ever Exist    Is Garbage      Origin PExtent    Origin Epoch    Expected Replica num     Epoch    Prefer Local    Lease Owner  Allocated Space    Is Sinkable    PExtent Type
-------  ---------  ---------------  -------------------  ------------  ------------  ----------------  --------------  ----------------------  --------  --------------  -------------  -----------------  -------------  --------------
3393731  [3, 2]     [3, 2]           []                   True          False                        0               0                       2  45495047               0              4  1024.00 KiB        True           PT_PERF
5023870  [1, 4]     [1, 4]           []                   True          False                        0               0                       2  42086915               1              4  2.00 MiB                          PT_CAP
5023871  [1, 4]     [1, 4]           []                   True          False                        0               0                       2  42086916               1              4  2.00 MiB                          PT_CAP
5023872  [1, 4]     [1, 4]           []                   True          False                        0               0                       2  42086917               1              0  0.00 B                            PT_CAP
5023873  [1, 4]     [1, 4]           []                   True          False                        0               0                       2  42086918               1              0  512.00 KiB                        PT_CAP
```

```
PT_PERF DISTRIBUTION
  chunk_id    total_replica_count    alive_replica_count    prefer_local_count    lease_owner_count
----------  ---------------------  ---------------------  --------------------  -------------------
         1                    468                    214                   469                  119
         2                      5                      5                     0                    0
         3                     22                      5                     0                    7
         4                      2                      2                     0                    0
         5                      0                      0                     0                    5
         6                    449                    210                     0                    3
         7                    461                    209                     0                    2
PT_PERF no prefer local count: 731
PT_PERF no lease  owner count: 1064

PT_CAP DISTRIBUTION
  chunk_id    total_replica_count    alive_replica_count    prefer_local_count    lease_owner_count
----------  ---------------------  ---------------------  --------------------  -------------------
         1                   1189                   1189                  1200                  191
         2                   1193                   1193                     0                    0
         3                   1200                   1200                     0                  173
         4                    579                    579                     0                    0
         5                   1099                   1099                     0                  157
         6                   1004                   1004                     0                  152
         7                    936                    936                     0                  188
PT_CAP no prefer local count: 0
PT_CAP no lease  owner count: 339
```

```
In Chunk Sizes
  chunk_id perf unique size   perf shared size   cap unique size   cap shared size
---------- ------------------ ------------------ ----------------- -----------------
         1 0.00 B             0.00 B             0.00 B            0.00 B
         2 0.00 B             0.00 B             0.00 B            0.00 B
         3 0.00 B             0.00 B             0.00 B            0.00 B
         4 0.00 B             0.00 B             0.00 B            0.00 B
         5 0.00 B             0.00 B             0.00 B            0.00 B
         6 0.00 B             0.00 B             0.00 B            0.00 B
         7 0.00 B             0.00 B             0.00 B            0.00 B
```

---

## 管理块存储服务 > 管理存储卷 > 创建存储卷

# 创建存储卷

在某个数据存储中创建一个指定名字和指定大小（默认单位：GiB）的存储卷。

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta volume create <pool_name> <volume_name> <volume_size> [--thin_provision <THIN_PROVISION>] [--resiliency_type <RESILIENCY_TYPE>] [--replica_num <REPLICA_NUM>] [--encrypt_method ENCRYPT_METHOD] [--ec_block_size <EC_BLOCK_SIZE>] [--read_only <READ_ONLY>] [--snapshot <SNAPSHOT>] [--snapshot_id <SNAPSHOT_ID>] [--stripe_num <STRIPE_NUM>] [--stripe_size <STRIPE_SIZE>] [--preferred_cid <PREFERRED_CID>] [--prioritized <PRIORITIZED>]`

| 参数 | 说明 |
| --- | --- |
| `volume_name` | 设置存储卷名称。 |
| `volume_size` | 设置存储卷大小。 |
| `--thin_provision <THIN_PROVISION>` | 设置新建存储卷的置备方式是否为精简置备，可设置为 `True` 或 `False`。 |
| `--resiliency_type <RESILIENCY_TYPE>` | 设置冗余模式，副本或 EC，若未设置，将从数据存储继承，默认为 `None`。 |
| `--replica_num <REPLICA_NUM>` | 设置新建存储卷的默认副本数，可设置为 2 副本或 3 副本，默认为 `None`。 |
| `--encrypt_method <ENCRYPT_METHOD>` | 设置数据加密方法，默认为不加密。 |
| `--ec_block_size <EC_BLOCK_SIZE>` | 设置 EC 算法的使用的数据块大小。当冗余模式为 EC 时，默认为 `4096`，否则默认为 `None`。 |
| `--read_only <READ_ONLY>` | 设置存储卷是否为只读模式，可设置为 `True` 或 `False`。 |
| `--snapshot <SNAPSHOT>` | 设置快照路径，从快照中创建一个存储卷。 |
| `--snapshot_id <SNAPSHOT_ID>` | 设置快照 ID，从快照中创建一个存储卷。 |
| `--stripe_num <STRIPE_NUM>` | 新建存储卷的条带数。 |
| `--stripe_size <STRIPE_SIZE>` | 新建存储卷的条带大小。 |
| `--preferred_cid <PREFERRED_CID>` | 设置倾向的 chunk ID，meta 在分配 PExtent 副本时，会尽量靠近该 chunk。 |
| `--prioritized <PRIORITIZED>` | 设置存储卷的数据是否都需要维持在性能层中，可设置为 `True` 或 `False`。 |

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理存储卷 > 在数据存储中删除存储卷

# 在数据存储中删除存储卷

从数据存储中将存储卷删除。

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta volume delete <pool_name> <volume_name> [--with-snapshots]`

| 参数 | 说明 |
| --- | --- |
| `pool_name` | 存储卷所属的数据存储。 |
| `volume_name` | 存储卷名称。 |
| `--with-snapshots` | 删除存储卷的快照。 |

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理存储卷 > 将存储卷移至新数据存储中

# 将存储卷移至新数据存储中

**操作方法**

在集群任一节点执行如下命令，将存储卷移至新的数据存储中：

`zbs-meta volume move <src_pool_name> <volume_name> <dst_pool_name>`

| 参数 | 说明 |
| --- | --- |
| `src_pool_name` | 源数据存储。 |
| `dst_pool_name` | 目的数据存储。 |
| `volume_name` | 待移动的存储卷名称。 |

---

## 管理块存储服务 > 管理存储卷 > 提升存储卷副本数

# 提升存储卷副本数

**操作方法**

在集群任一节点执行如下命令，提升存储卷副本数：

`zbs-meta volume update <pool_name> <volume_name> [--replica_num <REPLICA_NUM>]`

| 参数 | 说明 |
| --- | --- |
| `--prefer_cid` | 副本优先选择存储的 chunk ID。 |
| `--replica_num <REPLICA_NUM>` | 可选参数，更新存储卷的副本数, 只支持提高，不支持降低。 |
| `pool_name` | 必选参数，pool 名称。 |
| `volume_name` | 必选参数，存储卷名称。 |

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理存储卷 > 调整存储卷大小

# 调整存储卷大小

**操作方法**

在集群任一节点执行如下命令调整存储卷的大小，单位为 GiB：

`zbs-meta volume resize <pool_name> <volume_name> <size>`

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理存储卷 > 管理接入点

# 管理接入点

## 查看存储卷的活跃接入点

**操作方法**

在集群任一节点执行如下命令，查看指定存储卷在集群中的活跃接入点：

`zbs-meta volume show_access_record <volume_id>`

| 参数 | 说明 |
| --- | --- |
| `volume_id` | 存储卷 ID。 |

**输出示例**

```
zbs-meta volume show_access_record 951033b1-fed5-4bfa-a1df-2d7480c86e38
node_ip      cids      last_report_s    report_count
-----------  ------  ---------------  --------------
10.0.128.12  11,12             44948               1
```

其中，`cid` 表示节点的 chunk ID。

## 调整存储卷的本地接入点

**操作方法**

在集群任一节点执行如下命令，手动调整存储卷的本地接入点：

`zbs-meta volume report_access <volume_id> <chunk_id> [--include_cow]`

| 参数 | 说明 |
| --- | --- |
| `volume_id` | 存储卷 ID。 |
| `chunk_id` | chunk ID。 |
| `--include_cow` | 可选参数，允许更改处于 COW 状态的 extent 的本地接入点。 |

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理存储卷 > 读取存储卷数据

# 读取存储卷数据

**操作方法**

在集群节点执行如下命令，从指定的数据存储中读取指定名字的存储卷，并把读取结果存入到指定名字的文件中。若不指定文件名，则输出到屏幕。

`zbs-chunk volume read <pool_name> <volume_name> -o <file_name>`

**输出示例**

```
smartx/test1 100% |#############################################################################################| 60.69 M/s Time: 00:00:17
```

---

## 管理块存储服务 > 管理存储卷 > 将数据写入存储卷

# 将数据写入存储卷

**操作方法**

在集群节点执行如下命令，把指定名字的文件中的数据写入到指定数据存储的存储卷中。若没有指定文件名，则从键盘接收输入。

`zbs-chunk volume write <pool_name> <volume_name> -i <file_name>`

**输出示例**

```
smartx/test1 100% |#############################################################################################| 24.81 M/s Time: 00:00:43
```

---

## 管理块存储服务 > 管理存储卷 > 复制存储卷

# 复制存储卷

**操作方法**

在集群任一节点执行如下命令，将源存储卷复制到目的存储卷。

`zbs-task copy_volume copy <src_volume_id> <dst_volume_id> <src_hosts> <dst_hosts>`

`src_hosts` 和 `dst_hosts` 格式为 `ip:10201:10206` 和 `ip:10201:10206`。

**输出示例**

```
{'created_ms': 1718692495535,
 'expect_state': 0,
 'id': '203d6492-713a-4cb6-afc0-fb67284b29b0',
 'last_failed_ms': 0,
 'max_schedule_times': 10,
 'method_id': 0,
 'name': '',
 'schedule_times': 0,
 'service_id': 6007,
 'state': 2,
 'task': {'bps_max': 314572800,
          'cur_state': 0,
          'dst_hosts': 'localhost:10201:10206',
          'dst_volume_id': 'fe4daff8-9cd3-494e-8d22-bd5a4af2e54d',
          'io_depth': 32,
          'preferred_cid': 0,
          'runtime': {'end_hour': 23,
                      'end_min': 59,
                      'start_hour': 0,
                      'start_min': 0},
          'skip_zero': False,
          'src_hosts': 'localhost:10201:10206',
          'src_volume_id': 'a116a8b8-9cfb-4c33-8640-3cb1a60df6d0',
          'use_compression': False}}
```

---

## 管理块存储服务 > 管理存储卷 > 下沉存储卷的性能层数据

# 下沉存储卷的性能层数据

## 下沉指定名称的存储卷的性能层数据

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta volume sink <pool_name> <volume_name>`

**输出说明**

执行成功无输出。

## 下沉指定 ID 的存储卷的性能层数据

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta volume sink_by_id <volume_id>`

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理存储卷快照 > 查看存储卷快照

# 查看存储卷快照

## 查看所有存储卷快照

用户可查看所有数据存储中的存储卷快照，也可以查看单个数据存储中的所有存储卷快照。

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta snapshot listall [pool_name]`

`pool_name` 为数据存储名称。该参数为空时，查看的是所有数据存储中的快照。

**输出示例**

```
ID                                    Snap Name       Size      Perf Unique Size    Perf Shared Size    Cap Unique Size    Cap Shared Size    Logical Used Size    Diff Size    Volume Id                             Creation Time                  Description
------------------------------------  --------------  --------  ------------------  ------------------  -----------------  -----------------  -------------------  -----------  ------------------------------------  -----------------------------  ---------------------
22d70f1a-1372-4535-876e-2f629f623706  sp2             3.00 GiB  0.00 B              0.00 B              0.00 B             0.00 B             0.00 B               0.00 B       24fe0d76-1528-461a-b83f-db96f7b3d4a2  2024-06-17 18:45:47.147650126  snapshot-description2
a8ac78fc-9ca8-428e-b5e0-dde6a6955e35  snapshot-name7  3.00 GiB  0.00 B              512.00 MiB          0.00 B             0.00 B             256.00 MiB           0.00 B       057f5339-73e5-4b83-93f1-78a583649c50  2024-06-17 18:45:47.147465364
e1546006-bf0e-427a-ba7a-51fb24a1701f  snapshot1       3.00 GiB  0.00 B              512.00 MiB          0.00 B             0.00 B             256.00 MiB           0.00 B       057f5339-73e5-4b83-93f1-78a583649c50  2024-06-17 17:56:14.482402754
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Size` | 快照逻辑大小。 |
| `Perf Unique Size` | 快照独占的性能层空间大小。 |
| `Perf Shared Size` | 快照和其他对象共享的性能层空间大小。 |
| `Cap Unique Size` | 快照独占的容量层空间大小。 |
| `Cap Shared Size` | 快照和其他对象共享的容量层空间大小。 |
| `Logical Used Size` | 快照已经分配的逻辑空间大小。 |

## 查看某个存储卷的快照

**操作方法**

在集群任一节点执行如下命令，查看某个存储卷的快照：

`zbs-meta snapshot list <pool_name> <volume_name>`

**输出示例**

```
ID                                    Snap Name       Size      Perf Unique Size    Perf Shared Size    Cap Unique Size    Cap Shared Size    Logical Used Size    Diff Size    Volume Id                             Creation Time                  Description
------------------------------------  --------------  --------  ------------------  ------------------  -----------------  -----------------  -------------------  -----------  ------------------------------------  -----------------------------  -------------
033ad13a-6d63-4e02-bfc5-2e1ca8e676ed  sp1             3.00 GiB  In Process          In Process          In Process         In Process         In Process           0.00 B       057f5339-73e5-4b83-93f1-78a583649c50  2024-06-18 14:42:05.810181135
a8ac78fc-9ca8-428e-b5e0-dde6a6955e35  snapshot-name7  3.00 GiB  In Process          In Process          In Process         In Process         In Process           0.00 B       057f5339-73e5-4b83-93f1-78a583649c50  2024-06-17 18:45:47.147465364
e1546006-bf0e-427a-ba7a-51fb24a1701f  snapshot1       3.00 GiB  In Process          In Process          In Process         In Process         In Process           0.00 B       057f5339-73e5-4b83-93f1-78a583649c50  2024-06-17 17:56:14.482402754
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Size` | 快照逻辑大小。 |
| `Perf Unique Size` | 快照独占的性能层空间大小。 |
| `Perf Shared Size` | 快照和其他对象共享的性能层空间大小。 |
| `Cap Unique Size` | 快照独占的容量层空间大小。 |
| `Cap Shared Size` | 快照和其他对象共享的容量层空间大小。 |
| `Logical Used Size` | 快照已经分配的逻辑空间大小。 |

## 查看指定存储卷快照的详细信息

**操作方法**

在集群任一节点执行如下命令，查看指定存储卷快照的详细信息：

`zbs-meta snapshot show_by_id <snapshot_id>`

**输出示例**

```
-----------------  ------------------------------------
ID                 033ad13a-6d63-4e02-bfc5-2e1ca8e676ed
Name               sp1
Parent ID          057f5339-73e5-4b83-93f1-78a583649c50
Size               3.00 GiB
Perf Unique Size   0.00 B
Perf Shared Size   512.00 MiB
Cap Unique Size    0.00 B
Cap Shared Size    0.00 B
Logical Used Size  256.00 MiB
Creation Time      2024-06-18 14:42:05.810181135
Status             VOLUME_ONLINE
Resiliency Type    RT_REPLICA
Replica Num        3
EC Param
Thin Provision     True
Read Only          False
Description
Alloc Even         False
Clone count        0
Iops               0
Iops Read          0
Iops Write         0
Bps                0
Bps Read           0
Bps Write          0
Stripe Num         1
Stripe Size        262144
Prefer CID         0
Access Points      [1]
Is Prioritized     False
Downgraded PRS     0.00 B
-----------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Size` | 快照逻辑大小。 |
| `Perf Unique Size` | 快照独占的性能层空间大小。 |
| `Perf Shared Size` | 快照和其他对象共享的性能层空间大小。 |
| `Cap Unique Size` | 快照独占的容量层空间大小。 |
| `Cap Shared Size` | 快照和其他对象共享的容量层空间大小。 |
| `Logical Used Size` | 快照已经分配的逻辑空间大小。 |
| `Resiliency Type` | 冗余模式。 |
| `Replica Num` | 副本冗余模式下对应的副本数。 |
| `EC Param` | EC 冗余模式下对应的 EC 参数。 |
| `Thin Provision` | 是否为精简置备。 |
| `Read Only` | 是否只读。 |
| `Alloc Even` | 副本是否均匀分配。 |
| `Access Points` | 快照的访问接入点。 |
| `Is Prioritized` | 快照的数据是否都需要维持在性能层中。 |
| `Downgraded PRS` | 快照的尚未提升到性能层的空间大小。 |

---

## 管理块存储服务 > 管理存储卷快照 > 创建存储卷快照

# 创建存储卷快照

## 创建一个指定名称的快照

**操作方法**

在集群任一节点执行如下命令，某个数据存储中为某个存储卷创建一个指定名称的存储卷快照：

`zbs-meta snapshot create <pool_name> <volume_name> <snapshot_name>`

| 参数 | 说明 |
| --- | --- |
| `pool_name` | 数据存储名称。 |
| `volume_name` | 存储卷名称。 |
| `snapshot_name` | 快照名称。 |

**输出说明**

执行成功无输出。

## 批量为多个存储卷创建快照

**操作方法**

在集群任一节点执行如下命令，批量为多个存储卷创建快照：

`zbs-meta snapshot batch_create "<volumes>"`

`volumes` 为待创建快照的存储卷。可以输入多个存储卷，并以英文逗号 `,` 分开。单个存储卷的输入格式如下：

`VOLUME = VOLUME_ID,BATCH_SNAPSHOT_VOLUME_TYPE,OBJ_ID,SNAPSHOT_NAME,SNAPSHOT_DESCRIPTION,SECONDARY_ID`

各参数说明如下：

| 参数 | 说明 | 示例 |
| --- | --- | --- |
| `VOLUME_ID` | 必选参数。输入存储卷 ID。 | `9c2e2f88-99f7-4581-8eae-289924118962` |
| `BATCH_SNAPSHOT_VOLUME_TYPE` | 必选参数。输入存储卷的类型。根据存储卷的类型，可以为 `BATCH_SNAPSHOT_VOLUME`、`BATCH_SNAPSHOT_LUN`、`BATCH_SNAPSHOT_FILE` 和`BATCH_SNAPSHOT_NAMESPACE`。需要注意的是，所有字母均需大写输入。 | `BATCH_SNAPSHOT_VOLUME_LUN` |
| `OBJ_ID` | 必选参数。根据存储卷类型，输入对应的 ID。对于 `BATCH_SNAPSHOT_VOLUME`，请留空；对于 `BATCH_SNAPSHOT_LUN`，请输入 LUN ID；对于 `BATCH_SNAPSHOT_FILE`，请输入 Inode ID；对于 `BATCH_SNAPSHOT_NAMESPACE`，请输入 namespace ID。 | `1` |
| `SNAPSHOT_NAME` | 可选参数。输入快照名称。 | `snapshot1` |
| `SNAPSHOT_DESCRIPTION` | 可选参数。输入快照描述。可留空。 | `snapshotdescription` |
| `SECONDARY_ID` | 可选参数。输入快照 secondary ID。可留空。 | `99cf762a-0375-4327-927d-a17243374d25` |

**使用示例**

以对批量对存储卷 ID 为 `911dcc87-b366-42ad-a093-500a9ce7e0de` 和 `cf4f60ff-1190-4497-b8d8-3d1967b860b7` 的存储卷创建快照，示例如下：

`zbs-meta snapshot batch_create "911dcc87-b366-42ad-a093-500a9ce7e0de,BATCH_SNAPSHOT_VOLUME,,snapshot-name7,,secondary_id7;cf4f60ff-1190-4497-b8d8-3d1967b860b7,BATCH_SNAPSHOT_VOLUME,,snapshot-name6,snapshot-description2,secondary_id2"`

**输出示例**

```
[root@zbs17-73 14:16:08 ~]$zbs-meta snapshot batch_create "4983d31d-798f-41ef-b36f-41a6938d287d,BATCH_SNAPSHOT_VOLUME,,snapshot-name456,,secondary_id456;fe4daff8-9cd3-494e-8d22-bd5a4af2e54d,BATCH_SNAPSHOT_VOLUME,,snapshot-name123,snapshot-description2,secondary_id123"
ID                                    Name              Parent ID                             Size         Perf Unique Size    Perf Shared Size    Cap Unique Size    Cap Shared Size    Logical Used Size    Creation Time                  Status         Resiliency Type      Replica Num  EC Param    Thin Provision    Read Only    Description            Alloc Even      Clone count    Prefer CID  Access Points    Is Prioritized    Downgraded PRS
------------------------------------  ----------------  ------------------------------------  -----------  ------------------  ------------------  -----------------  -----------------  -------------------  -----------------------------  -------------  -----------------  -------------  ----------  ----------------  -----------  ---------------------  ------------  -------------  ------------  ---------------  ----------------  ----------------
7950dd46-07f2-4cf5-a42d-201eaf900839  snapshot-name456  4983d31d-798f-41ef-b36f-41a6938d287d  1024.00 GiB  In Process          In Process          In Process         In Process         In Process           2024-06-18 14:47:47.459604104  VOLUME_ONLINE  RT_REPLICA                     2              True              False                               False                     0             0  []               False             0.00 B
ff0996f9-c749-4d61-9959-d95b30a5d0f3  snapshot-name123  fe4daff8-9cd3-494e-8d22-bd5a4af2e54d  0.00 B       In Process          In Process          In Process         In Process         In Process           2024-06-18 14:47:47.459820330  VOLUME_ONLINE  RT_REPLICA                     3              True              False        snapshot-description2  False                     0             0  []               False             0.00 B
```

---

## 管理块存储服务 > 管理存储卷快照 > 删除存储卷快照

# 删除存储卷快照

## 删除指定名称的存储卷快照

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta snapshot delete <pool_name> <volume_name> <snapshot_name>`

**输出说明**

执行成功无输出。

## 删除指定 ID 的存储卷快照

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta snapshot delete_by_id <snapshot_id>`

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理存储卷快照 > 更新存储卷快照

# 更新存储卷快照

用户可根据快照 ID 或快照名称来更新相应的快照。

## 根据快照名称更新快照

**操作方法**

执行如下命令：

`zbs-meta snapshot update <pool_name> <volume_name> <snapshot_name> [--new_snapshot_name NEW_SNAPSHOT_NAME] [--new_alloc_even NEW_ALLOC_EVEN]`

**输出说明**

执行成功无输出。

## 根据快照 ID 更新快照

**操作方法**

执行如下命令：

`zbs-meta snapshot update_by_id <snapshot_id> <new_name> [--new_desc NEW_DESC] [--new_alloc_even NEW_ALLOC_EVEN]`

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理存储卷快照 > 从存储卷快照回滚

# 从存储卷快照回滚

**操作方法**

在集群任一节点执行如下命令，从存储卷快照回滚：

`zbs-meta snapshot rollback <pool_name> <volume_name> <snapshot_name>`

| 参数 | 说明 |
| --- | --- |
| `pool_name` | 数据存储名称。 |
| `volume_name` | 存储卷名称。 |
| `snapshot_name` | 快照名称。 |

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理存储卷快照 > 下沉指定 ID 的存储卷快照的性能层数据

# 下沉指定 ID 的存储卷快照的性能层数据

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta volume sink_by_id <snapshot_id>`

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理数据块

# 管理数据块

数据块（extent）是 MetaCluster 管理的基本单元。⼀个存储卷被切分成多个固定⼤⼩的数据块存储在 ChunkServer 中。数据的恢复、迁移、写时复制（CopyOnWrite - COW）等，都以数据块为单位进⾏。技术人员可以通过 LExtent 和 PExtent 对集群的数据块进行查看和调试。其中 LExtent 为逻辑数据块，PExtent 为实际落盘的物理数据块。

## 查看数据块

### 查看某个逻辑数据块的详细信息

**操作方法**

在集群任一节点执行如下命令，查看某个逻辑数据块的详细信息：

`zbs-meta lextent show <lextent_id>`

**输出示例**

```
-------------  -------
Logical ID     8
Logical Epoch  8431008
Perf PID       None
Perf Epoch     None
Cap PID        24348
Cap Epoch      8742712
Prioritized    False
-------------  -------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Logical ID` | 逻辑数据块 ID。 |
| `Logical Epoch` | 逻辑数据块版本号。 |
| `Perf PID` | 性能层物理数据块 ID。 |
| `Perf Epoch` | 性能层物理数据块版本号。 |
| `Cap PID` | 容量层物理数据块 ID。 |
| `Cap Epoch` | 容量层物理数据块版本号。 |
| `Prioritized` | 是否被常驻缓存卷引用。 |

### 查看逻辑数据块所属存储卷

**操作方法**

在集群任一节点执行如下命令，查看逻辑数据块所属的存储卷：

`zbs-meta lextent getref <lextent_id>`

**输出示例**

```
-----------------------  ------------------------------------
Pool Name                zbs-images
Volume ID                ef5e94a3-2215-4ed9-814e-d08e393d7648
Volume Name              ef5e94a3-2215-4ed9
Volume Is Snapshot       False
Volume Snapshot Pool ID
Snapshot Name
-----------------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Pool Name` | 逻辑数据块所属数据存储。 |
| `Volume ID` | 逻辑数据块所属存储卷的 ID。 |
| `Volume Name` | 逻辑数据块所属存储卷的名称。 |
| `Volume Is Snapshot` | 逻辑数据块所属存储卷是否有快照。 |
| `Volume Snapshot Pool ID` | 逻辑数据块所属数据存储的 ID。 |
| `Snapshot Name` | 逻辑数据块所属存储卷的快照名称。 |

### 查看集群中物理数据块

**操作方法**

在集群任一节点执行如下命令，查看集群中指定范围的物理数据块：

`zbs-meta pextent list [start_id] [end_id] [--show_non_exist] [--show_cap_only] [--show_perf_only]`

| 参数 | 说明 |
| --- | --- |
| `start_id` | 开始查找的 PExtent ID。 |
| `end_id` | 结束查找的 PExtent ID。 |
| `--show_non_exist` | 展示还未被分配过的 PExtent ID。 |
| `--show_cap_only` | 仅展示位于容量层的 PExtent ID。 |
| `--show_perf_only` | 仅展示位于性能层的 PExtent ID。 |

> **注意**：
>
> 随着集群的规模扩展，此操作可能会非常耗时。

**输出示例**

```
[root@9f29fde8244f zbs-client-py]# zbs-meta pextent list 1 548 --show_non_exist --show_cap_only
  ID  Replica    Alive Replica    Temporary Replica    Ever Exist    Is Garbage      Origin PExtent    Origin Epoch    Expected Replica num    Epoch    Prefer Local  Allocated Space    Resiliency Type    PExtent Type    EC Param    Is Sinkable
----  ---------  ---------------  -------------------  ------------  ------------  ----------------  --------------  ----------------------  -------  --------------  -----------------  -----------------  --------------  ----------  -------------
   1  [4, 2, 7]  [4, 2, 7]        []                   True          False                        0               0                       3        1               2  5.25 MiB           RT_REPLICA         PT_CAP
   2  []         []               []                   False         False                        0               0                       3        2               2  0.00 B             RT_REPLICA         PT_CAP
   3  []         []               []                   False         False                        0               0                       3        3               2  0.00 B             RT_REPLICA         PT_CAP
   4  []         []               []                   False         False                        0               0                       3        4               2  0.00 B             RT_REPLICA         PT_CAP
...
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Replica` | 副本位置。 |
| `Alive Replica` | 活跃副本位置。 |
| `Ever Exist` | 数据是否真实存在。 |
| `Temporary Replica` | 对于副本模式的 PExtent，在有副本异常时，将会创建出对应的临时副本。 |
| `Is Garbage` | 是否需要回收。 |
| `Origin PExtent` | 源 PExtent。 |
| `Origin Epoch` | 源 PExtent 的 `Epoch`。 |
| `Expected Replica num` | 预期副本数量。 |
| `Epoch` | 版本号。 |
| `Prefer Local` | 该 PExtent 默认保存的 chunk ID。 |
| `Allocated Space` | 已分配物理空间。 |
| `Resiliency Type` | 冗余策略类型。 |
| `PExtent Type` | 是 capacity PExtent 还是 performance PExtent。 |
| `EC Param` | EC 冗余策略下对应的 EC 策略属性。 |
| `Is Sinkable` | 是否可以下沉。 |

### 查看某个物理数据块的详细信息

**操作方法**

在集群任一节点执行如下命令，查看某个物理数据块的详细信息：

`zbs-meta pextent show <pextent_id>`

**输出示例**

```
--------------------  ----------
ID                    5
Replica               [3, 1, 2]
Alive Replica         [3, 1, 2]
Temporary Replica     []
Ever Exist            True
Is Garbage            False
Origin PExtent        0
Origin Epoch          0
Expected Replica num  3
Epoch                 5
Prefer Local          3
Allocated Space       2.25 MiB
Resiliency Type       RT_REPLICA
PExtent Type          PT_PERF
EC Param
Is Sinkable           True
--------------------  ----------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Replica` | 副本位置。 |
| `Alive Replica` | 活跃副本位置。 |
| `Ever Exist` | 数据是否真实存在。 |
| `Temporary Replica` | 对于副本模式的 PExtent，在有副本异常时，将会创建出对应的临时副本。 |
| `Is Garbage` | 是否需要回收。 |
| `Origin PExtent` | 源 PExtent。 |
| `Origin Epoch` | 源 PExtent 的 `Epoch`。 |
| `Expected Replica num` | 预期副本数量。 |
| `Epoch` | 版本号。 |
| `Prefer Local` | 该 PExtent 默认保存的 chunk ID。 |
| `Allocated Space` | 已分配物理空间。 |
| `Resiliency Type` | 冗余策略类型。 |
| `PExtent Type` | 是 capacity PExtent 还是 performance PExtent。 |
| `EC Param` | EC 冗余策略下对应的 EC 策略属性。 |
| `Is Sinkable` | 是否可以下沉。 |

### 查看数据块所属存储卷

**操作方法**

在集群任一节点执行如下命令，查看数据块所属的存储卷：

`zbs-meta pextent getref <pextent_id> [--show_lextent_only]`

| 参数 | 说明 |
| --- | --- |
| `--show_lextent_only` | 仅查看所属 LExtent 的详细信息，默认为 `False`。 |

**输出示例**

```
[root@9f29fde8244f zbs-client-py]# zbs-meta pextent getref 1
-------------  -------
Logical ID           1
Logical Epoch        1
Perf PID       5485175
Perf Epoch     8997306
Cap PID              1
Cap Epoch            1
Prioritized      False
-------------  -------
-----------------------  ------------------------------------
Pool Name                ee8e1b5d-be53-4c7d-80df-d651579c5dd4
Volume ID                f08a4c60-e5b9-4046-b388-ecc23fa8e06c
Volume Name              f08a4c60-e5b9-4046-b388-ecc23fa8e06c
Volume Is Snapshot       False
Volume Snapshot Pool ID
Snapshot Name
-----------------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Logical ID` | 逻辑数据块 ID。 |
| `Logical Epoch` | 逻辑数据块版本号。 |
| `Perf PID` | 性能层物理数据块 ID。 |
| `Perf Epoch` | 性能层物理数据块版本号。 |
| `Cap PID` | 容量层物理数据块 ID。 |
| `Cap Epoch` | 容量层物理数据块版本号。 |
| `Prioritized` | 是否被常驻缓存卷引用。 |
| `Pool Name` | 数据块所属数据存储。 |
| `Volume ID` | 数据块所属存储卷的 ID。 |
| `Volume Name` | 数据块所属存储卷的名称。 |
| `Volume Is Snapshot` | 存储卷是否有快照。 |
| `Volume Snapshot Pool ID` | 数据块所属数据存储的 ID。 |
| `Snapshot Name` | 数据块所属存储卷的快照名称。 |

### 查看指定数据块的所有子数据块

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta pextent list_children <pextent_id>`

**输出示例**

```
    ID  Replica    Alive Replica    Temporary Replica    Ever Exist    Is Garbage      Origin PExtent    Origin Epoch    Expected Replica num    Epoch    Prefer Local  Allocated Space    Unique Space    Shared Space    Resiliency Type    PExtent Type    EC Param    Is Sinkable
------  ---------  ---------------  -------------------  ------------  ------------  ----------------  --------------  ----------------------  -------  --------------  -----------------  --------------  --------------  -----------------  --------------  ----------  -------------
917439  []         []               []                   False         False                   917343          917343                       2   917439               2  0.00 B             0.00 B          0.00 B          RT_REPLICA         PT_CAP
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Replica` | 副本位置。 |
| `Alive Replica` | 活跃副本位置。 |
| `Ever Exist` | 数据是否真实存在。 |
| `Temporary Replica` | 对于副本模式的 PExtent，在有副本异常时，将会创建出对应的临时副本。 |
| `Is Garbage` | 是否需要回收。 |
| `Origin PExtent` | 源 PExtent。 |
| `Origin Epoch` | 源 PExtent 的 `Epoch`。 |
| `Expected Replica num` | 预期副本数量。 |
| `Epoch` | 版本号。 |
| `Prefer Local` | 该 PExtent 默认保存的 chunk ID。 |
| `Allocated Space` | 已分配物理空间。 |
| `Resiliency Type` | 冗余策略类型。 |
| `PExtent Type` | 是 capacity PExtent 还是 performance PExtent。 |
| `EC Param` | EC 冗余策略下对应的 EC 策略属性。 |
| `Is Sinkable` | 是否可以下沉。 |

### 查看数据块关联的虚拟机

**操作方法**

在任意节点执行如下命令，查看与某个 PExtent 关联的虚拟机

`zbs-tool elf get_vm_by_pid <pid>`

| 参数 | 说明 |
| --- | --- |
| `pid` | PExtent ID。 |

**输出示例**

在 SMTX OS（ELF）集群，将展示对应的虚拟机名称；
在 SMTX OS（VMware ESXi）集群将展示相关的文件名称，可以通过文件名称进一步在 VMware 管理界面搜索相关的虚拟机。

```
     ID  Replica    Alive Replica    Temporary Replica    Ever Exist    Affected ZBS Volumes                      Affected VMs
-------  ---------  ---------------  -------------------  ------------  ----------------------------------------  ----------------------------------------------
111111  [2, 1]     [2, 1]           []                   False         ['3848f8a2-dd36-43dc-bd5e-90094f46990x']  ['vm-281bb7c2-5ada-4730-ae7b-9c7da2758091-2']
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `ID` | PExtent ID。 |
| `Replica` | PExtent 应有的副本。 |
| `Alive Replica` | PExtent 实际存活的副本。 |
| `Temporary Replica` | 对于副本模式的 PExtent，在有副本异常时，将会创建出对应的临时副本。 |
| `Ever Exist` | PExtent 是否曾经被分配过(精简置备的物理数据块只有发生读写后才会真实存在)。 |
| `Affected ZBS Volumes` | PExtent 影响的虚拟卷的 ID， 可显示多个。 |
| `Affected ZBS NFS Files` | PExtent 影响的虚拟卷对应的 NFS 文件名。仅在使用 NFS 接入协议的显示值，否则为空值。 |

## 查找处于某个状态的物理数据块

**操作方法**

在集群任一节点执行如下命令，查找处于某个状态的物理数据块：

`zbs-meta pextent find <pextent_status> [--start START] [--length Length]`

| 参数 | 说明 |
| --- | --- |
| `pextent_status` | 查找指定状态的物理数据块：  - `dead`：所有副本都不可访问的 PExtent。 - `need_recover`：需要进行数据恢复的 PExtent，当前正在恢复。 - `may_recover`：可能进行数据恢复的 PExtent，当前没有恢复，但即将进行恢复。 - `garbage`：标记为回收的 PExtent。 - `need_drain`需要进行数据下沉的 PExtent。 |
| `--start START` | 指定开始查找的 PExtent ID，默认为 `1`。 |
| `--length LENGTH` | 设置返回的 PExtent 的数量。默认值以及最大值均为 `1024`。 |

**使用示例**

`$ zbs-meta pextent find need_recover`

**输出示例**

```
   ID  Replica    Alive Replica    Temporary Replica    Ever Exist    Is Garbage      Origin PExtent    Origin Epoch    Expected Replica num    Epoch    Prefer Local  Allocated Space    Resiliency Type    PExtent Type    EC Param    Is Sinkable
----  ---------  ---------------  -------------------  ------------  ------------  ----------------  --------------  ----------------------  -------  --------------  -----------------  -----------------  --------------  ----------  -------------
  22  [3, 2]     [3, 2]           []                   True          False                        0               0                       3       14               0  512.00 MiB         RT_REPLICA         PT_PERF                     True
  23  [3, 2]     [3, 2]           []                   False         False                        0               0                       3       15               3  0.00 B             RT_REPLICA         PT_PERF                     True
  24  [3, 2]     [3, 2]           []                   False         False                        0               0                       3       16               3  0.00 B             RT_REPLICA         PT_PERF                     True
  25  [3, 2]     [3, 2]           []                   False         False                        0               0                       3       17               3  0.00 B             RT_REPLICA         PT_PERF                     True
```

## 查找 dead extent 和影响范围

当物理盘损坏或者节点下线时，部分物理数据块可能会丢失所有活跃的副本，此类物理数据块将被标记为 dead extent，且无法被访问。用户可以通过命令检测出 dead extent 及其影响的虚拟卷、虚拟机等。

**操作方法**

在集群任一节点执行如下命令：

`zbs-tool abnormal_detect find_dead_extent [--start START] [--length Length]`

| 参数 | 说明 |
| --- | --- |
| `--start START` | 指定开始查找的 PExtent ID，默认为 `1`。 |
| `--length LENGTH` | 设置返回的 PExtent 的数量。默认值以及最大值均为 `1024`。 |

**输出示例**

在不同虚拟化平台下输出结果有所不同，具体说明如下:

- **ELF 平台**

  可输出 dead extent 及其受影响的虚拟卷和对应的 NFS 文件名等，同时还可查询受影响的虚拟机。

  输出示例如下：

  ```
  [root@444541dcac3f zbs-client-py]# zbs-tool abnormal_detect find_dead_extent
  ID  Replica    Alive Replica    Temporary Replica    Ever Exist    Is Garbage      Origin PExtent    Origin Epoch    Expected Replica num    Epoch    Prefer Local  Allocated Space    Resiliency Type    PExtent Type    EC Param    Is Sinkable    Affected ZBS Volumes                      Affected ZBS NFS Files    Affected VMs
  ----  ---------  ---------------  -------------------  ------------  ------------  ----------------  --------------  ----------------------  -------  --------------  -----------------  -----------------  --------------  ----------  -------------  ----------------------------------------  ------------------------  --------------
  139  [1, 3]     []               []                   True          False                        0               0                       2      139               1  0.00 B             RT_REPLICA         PT_PERF                     True           ['e6fd591c-2176-47ed-b50c-51a59cfe4a67']  []                        [example_vm]
  ```

  以该输出结果为例，可得知以下主要信息：

  - dead extent 的 PID 为 `139`；
  - 受 dead extent 影响的虚拟卷 ID 为 `e6fd591c-2176-47ed-b50c-51a59cfe4a67`；
  - 受影响的虚拟机为 `example_vm`。
- **VMware ESXi 平台**

  可输出 dead extent 及其受影响的虚拟卷和对应的 NFS 文件名等，用户通过 NFS 文件名可以进一步在 VMware ESXi 平台查询对应的虚拟机。
  输出示例如下：

  ```
  [root@444541dcac3f zbs-client-py]# zbs-tool abnormal_detect find_dead_extent
  ID  Replica    Alive Replica    Temporary Replica    Ever Exist    Is Garbage      Origin PExtent    Origin Epoch    Expected Replica num    Epoch    Prefer Local  Allocated Space    Resiliency Type    PExtent Type    EC Param    Is Sinkable    Affected ZBS Volumes                      Affected ZBS NFS Files
  ----  ---------  ---------------  -------------------  ------------  ------------  ----------------  --------------  ----------------------  -------  --------------  -----------------  -----------------  --------------  ----------  -------------  ----------------------------------------  ------------------------
  105  [3, 2]     []               []                   True          False                        0               0                       2      105               3  1024.00 KiB        RT_REPLICA         PT_PERF                     True           ['cd74ead0-58a8-42d6-81e3-d1057275046a']  [example_vm.vmdk]
  ```

  以该输出结果为例，可以得知以下主要信息：

  - Dead extent 的 PID 为 `105`；
  - 受 dead extent 影响的虚拟卷 ID 为 `cd74ead0-58a8-42d6-81e3-d1057275046a`；
  - 受影响的虚拟卷对应的 NFS 文件为 `example_vm.vmdk`，通过该文件名可进一步在 VMware ESXi 平台查询受影响的虚拟机。

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `ID` | Dead extent 的 PID。 |
| `Replica` | Dead extent 应有的副本。 |
| `Alive Replica` | Dead extent 实际存活的副本。 |
| `Temporary Replica` | 对于副本模式的 PExtent，在有副本异常时，将会创建出对应的临时副本。 |
| `Ever Exist` | Dead extent 是否曾经被分配过（精简置备的数据块只有发生读写后才会真实存在）。 |
| `Is Garbage` | Dead extent 是否被标记为 Garbage，Garbage 意味着其所属的虚拟卷和快照等完全被删除，此数据块已经无用。 |
| `Origin PExtent` | 展示 dead extent 是否从其他数据块复制。若复制自其他数据块，显示其来源数据块的 PID，否则显示为 `0`。 |
| `Origin Epoch` | 源 PExtent 的 `Epoch`。 |
| `Expected Replica num` | Dead extent 预期的副本数，取决于其所属的上级对象(虚拟卷/快照)的配置。 |
| `Epoch` | 与 PID 组合用于唯一标识一个 extent 的属性值。 |
| `Prefer Local` | Dead extent 副本预期被分配到的节点 ID， 由副本分配策略决定。 |
| `Allocated Space` | 已分配物理空间。 |
| `Resiliency Type` | 冗余策略类型。 |
| `PExtent Type` | 是 capacity PExtent 还是 performance PExtent。 |
| `EC Param` | EC 冗余策略下对应的 EC 策略属性。 |
| `Is Sinkable` | 是否可以下沉。 |
| `Affected ZBS Volumes` | Dead extent 影响的虚拟卷的 ID，可显示多个。 |
| `Affected ZBS NFS Files` | Dead extent 影响的虚拟卷对应的 NFS 文件名。仅在使用 NFS 接入协议的显示值，否则为空值。 |
| `Affected VMs` | Dead extent 影响的虚拟机，该属性只在 ELF 平台展示，可展示多个虚拟机名称。 |

## 写入从物理数据块中读取到的数据

**操作方法**

在集群任一节点指定如下命令，将指定 `PExtent_id` 对应的 PExtent 中从 `offset` 开始，长度为 `length` 的数据写入到 `output_file` 中：

`zbs-meta pextent read -o <output_file> <pextent_id> <offset> <length>`

| 参数 | 说明 |
| --- | --- |
| `output_file` | 用于存储读取到的数据的文件。 |
| `offset` | 读取数据的起始偏移量(相对于虚拟卷)，需要能被 512 整除。 |
| `length` | 读取数据的长度，需要能被 512 整除。 |

## 查看 chunk 上的物理数据块的属性

**操作方法**

在当前节点执行如下命令，查看处于该 chunk 上的某个 PExtent 的属性。

`zbs-chunk extent show <pid>`

**输出示例**

```
pid: 5
epoch: 5
generation: 1783
status: 1
private_blob_num: 3
shared_blob_num: 0
thick_provision: False
perf: True
```

---

## 管理块存储服务 > 触发垃圾回收

# 触发垃圾回收

**注意事项**

集群中的垃圾回收是周期性进行的，正常场景下不需要手动触发。该命令用于主动触发垃圾回收。

**操作方法**

在集群任一节点执行如下命令，触发垃圾回收：

`zbs-meta gc scan_immediate`

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理业务主机组

# 管理业务主机组

业务主机组为一组业务主机的集合，为存储资源关联一个业务主机组相当于关联该业务主机组内的所有业务主机。

## 查看所有的业务主机组

**操作方法**

在集群任一节点执行如下命令，查看集群的所有业务主机组：

```
zbs-meta host_group list
```

**输出示例**

```
ID                                    Name                 Description
------------------------------------  -------------------  -------------
26bbbf0d-1c66-4ed6-b7cd-01e420137ce5  test-group-1
adf9f50f-2ed9-46d2-9891-581ea28e9239  test-group-3
eb01b152-4565-46cf-b67c-b958d8c56b24  test-group-2
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `ID` | 业务主机组 ID。 |
| `Name` | 业务主机组名称。 |
| `Description` | 业务主机组描述。 |

## 查看指定业务主机组的基本信息和关联存储资源信息

**操作方法**

在集群任一节点执行如下命令，查看指定业务主机组的基本信息和关联存储资源信息：

- 通过业务主机组名称查看：

  ```
  zbs-meta host_group show <host_group_name> [--show_associated_resources]
  ```
- 通过业务主机组 ID 查看：

  ```
  zbs-meta host_group show_by_id <host_group_id> [--show_associated_resources]
  ```

| 参数 | 说明 |
| --- | --- |
| `--show_associated_resources` | 可选参数，显示该业务主机组的关联存储资源信息，不指定则不显示。 |
| `host_group_name` | 业务主机组名称。 |
| `host_group_id` | 业务主机组 ID。 |

**输出示例**

```
-----------  ------------------------------------
ID           26bbbf0d-1c66-4ed6-b7cd-01e420137ce5
Name         test-group-1
Description
-----------  ------------------------------------
Associated Targets
Target ID
------------------------------------
2734d5ce-006e-4b35-a69c-fffefea1dcc0

Associated Luns
Parent Target ID                        Lun ID
------------------------------------  --------
2734d5ce-006e-4b35-a69c-fffefea1dcc0         1
69af0b7d-e684-4cd6-9d46-d9f459daa36f         2

No subsystem associated

No namespace associated
```

**输出说明**

- **业务主机组基本信息**

  | 参数 | 说明 |
  | --- | --- |
  | `ID` | 业务主机组 ID。 |
  | `Name` | 业务主机组名称。 |
  | `Description` | 业务主机组描述。 |
- **关联存储资源信息**

  - 关联 iSCSI target 信息

    | 参数 | 说明 |
    | --- | --- |
    | `Target ID` | Target ID。 |
  - 关联 iSCSI LUN 信息

    | 参数 | 说明 |
    | --- | --- |
    | `Parent Target ID` | LUN 所属 target 的 ID。 |
    | `Lun ID` | LUN ID。 |
  - 关联 NVMe Subsystem 信息

    | 参数 | 说明 |
    | --- | --- |
    | `Subsystem ID` | Subsystem ID。 |
  - 关联 NVMe Namespace 信息

    | 参数 | 说明 |
    | --- | --- |
    | `Parent Subsystem ID` | Namespace 所属 Subsystem 的 ID。 |
    | `NS ID` | Namespace ID。 |

## 创建业务主机组

**操作方法**

在集群任一节点执行如下命令，创建业务主机组，并设置业务主机组的名称和描述：

```
zbs-meta host_group create <host_group_name> [--desc DESC]
```

| 参数 | 说明 |
| --- | --- |
| `host_group_name` | 业务主机组名称。 |
| `--desc <DESC>` | 业务主机组描述。 |

**输出示例**

```
-----------  ------------------------------------
ID           45787fff-83fc-4d3b-9535-1c5934e4886b
Name         test-host-group
Description  test-desc
-----------  ------------------------------------
```

## 更新业务主机组

**操作方法**

在集群任一节点执行如下命令，更新业务主机组（此命令为全量更新命令，所有参数均需指定）：

```
zbs-meta host_group update <host_group_name> <new_host_group_name> <desc>
```

| 参数 | 说明 |
| --- | --- |
| `host_group_name` | 待更新业务主机组的名称。 |
| `new_host_group_name` | 重新命名业务主机组。 |
| `desc` | 更新业务主机组描述。 |

**输出示例**

```
-----------  ------------------------------------
ID           45787fff-83fc-4d3b-9535-1c5934e4886b
Name         new-test-host-group
Description  new-desc
-----------  ------------------------------------
```

## 删除业务主机组

**操作方法**

在集群任一节点执行如下命令，删除指定的业务主机组：

- 通过业务主机组名称删除：

  `zbs-meta host_group delete <host_group_name>`
- 通过业务主机组 ID 删除：

  `zbs-meta host_group delete_by_id <host_group_id>`

| 参数 | 说明 |
| --- | --- |
| `host_group_name` | 待删除业务主机组名称。 |
| `host_group_id` | 待删除业务主机组 ID。 |

**输出说明**

执行成功无输出。

---

## 管理块存储服务 > 管理业务主机

# 管理业务主机

业务主机代表一个想要访问存储资源的客户端，为存储资源关联业务主机，该业务主机对应的客户端即可获得该存储资源的访问权限。

## 查看所有的业务主机

**操作方法**

在集群任一节点执行如下命令，查看集群所有的业务主机：

```
zbs-meta host list
```

**输出示例**

```
ID                                    Name    Group ID                              Description
------------------------------------  ------  ------------------------------------  -------------
2dd38a55-f64d-4916-8f51-1fce4cbe844e  h1      9fc99f41-c08a-4a3a-9739-a8ee9e22e57b
e3283316-90c6-4d16-a540-50bccce5e109  h2      9fc99f41-c08a-4a3a-9739-a8ee9e22e57b
ee104b5f-74b1-4600-98d6-645dbb91f77b  h3
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `ID` | 业务主机 ID。 |
| `Name` | 业务主机名称。 |
| `Group ID` | 所属业务主机组 ID。 |
| `Description` | 业务主机描述。 |

## 查看指定业务主机组中所有的业务主机

**操作方法**

在集群任一节点执行如下命令，查看指定业务主机组中所有的业务主机：

- 通过业务主机组名称查看：

  ```
  zbs-meta host list_by_group <host_group_name>
  ```
- 通过业务主机组 ID 查看：

  ```
  zbs-meta host list_by_group_id <host_group_id>
  ```

**输出示例**

```
ID                                    Name    Group ID                              Description
------------------------------------  ------  ------------------------------------  -------------
2dd38a55-f64d-4916-8f51-1fce4cbe844e  h1      9fc99f41-c08a-4a3a-9739-a8ee9e22e57b
e3283316-90c6-4d16-a540-50bccce5e109  h2      9fc99f41-c08a-4a3a-9739-a8ee9e22e57b
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `ID` | 业务主机 ID。 |
| `Name` | 业务主机名称。 |
| `Group ID` | 所属业务主机组 ID。 |
| `Description` | 业务主机描述。 |

## 查看指定业务主机的基本信息，启动器信息和关联存储资源信息

**操作方法**

在集群任一节点执行如下命令，查看指定业务主机的基本信息，启动器信息和关联存储资源信息：

- 通过业务主机名称查看：

  ```
  zbs-meta host show <host_name> [--show_initiators] [--show_associated_resources]
  ```
- 通过业务主机 ID 查看：

  ```
  zbs-meta host show_by_id <host_id> [--show_initiators] [--show_associated_resources]
  ```

| 参数 | 说明 |
| --- | --- |
| `--show_initiators` | 可选参数，显示该业务主机的启动器信息，不指定则不显示。 |
| `--show_associated_resources` | 可选参数，显示该业务主机的关联存储资源信息，不指定则不显示。 |
| `host_name` | 业务主机名称。 |
| `host_id` | 业务主机 ID。 |

**输出示例**

```
-----------  ------------------------------------
ID           bcfee527-d61e-4a5d-9ba9-ab57210f2e13
Name         test-host1
Group ID     f9865678-f149-49b5-8f3d-a8010424c50f
Description
-----------  ------------------------------------
Host Initiator Info
Identifier                                                            Ips    Enable Chap    Chap Name    Chap Secret
--------------------------------------------------------------------  -----  -------------  -----------  -------------
iqn.1994-05.com.redhat:858c488e9b7                                           False
nqn.2014-08.org.nvmexpress:uuid:26755e30-4e9b-4b1e-bd32-79eff062f7d1         False

Associated Targets
Target ID
------------------------------------
beda75cd-8b44-4baf-b6b5-726414ee3a2d

Associated Luns
Parent Target ID                        Lun ID
------------------------------------  --------
beda75cd-8b44-4baf-b6b5-726414ee3a2d         1

Associated Subsystems
Subsystem ID
------------------------------------
79d6d69a-42b5-47bb-87a3-5d2d1b2b1e6e

Associated Namespaces
Parent Subsystem ID                     NS ID
------------------------------------  -------
79d6d69a-42b5-47bb-87a3-5d2d1b2b1e6e        1
```

**输出说明**

- **业务主机基本信息**

  | 参数 | 说明 |
  | --- | --- |
  | `ID` | 业务主机 ID。 |
  | `Name` | 业务主机名称。 |
  | `Group ID` | 所属业务主机组 ID。 |
  | `Description` | 业务主机描述。 |
- **启动器信息**

  | 参数 | 说明 |
  | --- | --- |
  | `Identifier` | 启动器标识符，IQN 或 NQN。 |
  | `Ips` | 启动器 IP。 |
  | `Enable Chap` | 是否使能 CHAP 认证。 |
  | `Chap Name` | CHAP 名称。 |
  | `Chap Secret` | CHAP 密码。 |
- **关联存储资源信息**

  - 关联 iSCSI target 信息

    | 参数 | 说明 |
    | --- | --- |
    | `Target ID` | Target ID。 |
  - 关联 iSCSI LUN 信息

    | 参数 | 说明 |
    | --- | --- |
    | `Parent Target ID` | LUN 所属 target 的 ID。 |
    | `Lun ID` | LUN ID。 |
  - 关联 NVMe Subsystem 信息

    | 参数 | 说明 |
    | --- | --- |
    | `Subsystem ID` | Subsystem ID。 |
  - 关联 NVMe Namespace 信息

    | 参数 | 说明 |
    | --- | --- |
    | `Parent Subsystem ID` | Namespace 所属 Subsystem 的 ID。 |
    | `NS ID` | Namespace ID。 |

## 创建业务主机

**操作方法**

在集群任一节点执行如下命令，创建业务主机，并设置业务主机的名称，描述，所属业务主机组和启动器信息：

```
zbs-meta host create <host_name> [--desc DESC] [--group_name GROUP_NAME] [--initiators INITIATORS]
```

| 参数 | 说明 |
| --- | --- |
| `host_name` | 业务主机名称。 |
| `--desc <DESC>` | 业务主机描述。 |
| `--group_name GROUP_NAME` | 指定所属业务主机组的名称。 |
| `--initiators INITIATORS` | 启动器信息。 指定内容使用英文双引号（""）包裹，双引号内以斜杠（/）分隔多个启动器信息，启动器信息中以英文分号（;）分隔多个元素，IP 信息中以英文逗号（,）分隔多个 IP。 单个启动器格式为：identifier;ips;enable\_chap;chap\_name;chap\_secret 例如： iqn;ip1,ip2;True;name;secret nqn;ip1;;; ;ip1,ip2;;; iqn;ip1;True;name;secret/iqn;;;;/nqn;;;; |

**输出示例**

```
-----------  ------------------------------------
ID           9c312691-0be9-443c-8033-8aa6a60bf712
Name         h4
Group ID
Description
-----------  ------------------------------------
```

## 更新业务主机

**操作方法**

在集群任一节点执行如下命令，更新业务主机（此命令为全量更新命令，所有参数均需指定）：

```
zbs-meta host update <host_name> <new_host_name> <desc> <group_name> <initiators>
```

| 参数 | 说明 |
| --- | --- |
| `host_name` | 待更新业务主机的名称。 |
| `new_host_name` | 重新命名业务主机。 |
| `desc` | 更新业务主机描述。 |
| `group_name` | 更新所属业务主机组。 |
| `initiators` | 更新启动器信息。 指定内容使用英文双引号（""）包裹，双引号内以斜杠（/）分隔多个启动器信息，启动器信息中以英文分号（;）分隔多个元素，IP 信息中以英文逗号（,）分隔多个 IP。 单个启动器格式为：identifier;ips;enable\_chap;chap\_name;chap\_secret 例如： iqn;ip1,ip2;True;name;secret nqn;ip1;;; ;ip1,ip2;;; iqn;ip1;True;name;secret/iqn;;;;/nqn;;;; |

**输出示例**

```
-----------  ------------------------------------
ID           ee104b5f-74b1-4600-98d6-645dbb91f77b
Name         h3
Group ID
Description  new desc
-----------  ------------------------------------
```

## 批量将业务主机移入业务主机组

**操作方法**

在集群任一节点执行如下命令，批量将业务主机移入业务主机组，移入前所有业务主机必须均不属于任一业务主机组：

```
zbs-meta host batch_add_hosts_to_group <group_name> <host_ids>
```

| 参数 | 说明 |
| --- | --- |
| `group_name` | 指定业务主机要移入的业务主机组。 |
| `host_ids` | 指定业务主机的 ID，以英文逗号（,）分隔多个 ID。 |

**输出示例**

```
ID                                    Name    Group ID                              Description
------------------------------------  ------  ------------------------------------  -------------
2dd38a55-f64d-4916-8f51-1fce4cbe844e  h1      9fc99f41-c08a-4a3a-9739-a8ee9e22e57b
e3283316-90c6-4d16-a540-50bccce5e109  h2      9fc99f41-c08a-4a3a-9739-a8ee9e22e57b
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `ID` | 业务主机 ID。 |
| `Name` | 业务主机名称。 |
| `Group ID` | 所属业务主机组 ID。 |
| `Description` | 业务主机描述。 |

## 批量将业务主机移出业务主机组

**操作方法**

在集群任一节点执行如下命令，批量将业务主机移出业务主机组，移出前所有业务主机必须同属于同一业务主机组：

```
zbs-meta host batch_remove_hosts_from_group <group_name> <host_ids>
```

| 参数 | 说明 |
| --- | --- |
| `group_name` | 指定业务主机所属业务主机组。 |
| `host_ids` | 指定业务主机的 ID，以英文逗号（,）分隔多个 ID。 |

**输出示例**

```
ID                                    Name    Group ID    Description
------------------------------------  ------  ----------  -------------
2dd38a55-f64d-4916-8f51-1fce4cbe844e  h1
e3283316-90c6-4d16-a540-50bccce5e109  h2
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `ID` | 业务主机 ID。 |
| `Name` | 业务主机名称。 |
| `Group ID` | 所属业务主机组 ID。 |
| `Description` | 业务主机描述。 |

## 删除业务主机

**操作方法**

在集群任一节点执行如下命令，删除指定的业务主机：

- 通过业务主机名称删除：

  `zbs-meta host delete <host_name>`
- 通过业务主机 ID 删除：

  `zbs-meta host delete_by_id <host_id>`

| 参数 | 说明 |
| --- | --- |
| `host_name` | 待删除业务主机名称。 |
| `host_id` | 待删除业务主机 ID。 |

**输出说明**

执行成功无输出。

## 批量删除业务主机

**操作方法**

在集群任一节点执行如下命令，批量删除业务主机：

```
zbs-meta host batch_delete_by_id <host_ids>
```

| 参数 | 说明 |
| --- | --- |
| `host_ids` | 指定待删除业务主机的 ID，以英文逗号（,）分隔多个 ID。 |

**输出说明**

执行成功无输出。

---

## 管理回收站 > 配置回收站

# 配置回收站

## 启用回收站

启用回收站后，所有删除的卷将先被标记为 **Trash(暂存)** 并移动到 zbs-trash-pool 存储池。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin enable
```

**输出示例**

```
$ zbs-meta recycle_bin enable
Enabled RecycleBin, Check RecycleBin config by show_config
```

## 禁用回收站

禁用回收站后，回收站内所有卷会被立即清理。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin disable
```

**输出示例**

```
$ zbs-meta recycle_bin disable
Disabled RecycleBin, Check RecycleBin config by show_config
```

## 更新回收站内暂存卷的默认过期时间

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin update_default_expired_hours <hours>
```

| 参数 | 说明 |
| --- | --- |
| `hours` | 过期小时数，范围：1~8760（最多 365 天）。 |

**输出示例**

```
$ zbs-meta recycle_bin update_default_expired_hours 24
Check RecycleBin config by show_config
```

---

## 管理回收站 > 查看回收站相关信息

# 查看回收站相关信息

## 查看回收站配置

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin show_config
```

**输出示例**

```
$ zbs-meta recycle_bin show_config
enable_recycle_bin: true
default_vol_expired_hours: 24
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `enable_recycle_bin` | 回收站是否开启。 |
| `default_vol_expired_hours` | 回收站内卷的默认过期时间，单位为小时。 |

## 查看回收站对应的存储池

回收站对应的存储池为集群受保护的特殊存储池，仅用于暂存待清理的卷，不允许删除该存储池以及在存储池内执行普通卷相关操作（例如：创建卷、删除卷、对卷创建快照、克隆卷等）。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin show_pool
```

**输出示例**

```
$ zbs-meta recycle_bin show_pool
---------------  ---------------------------------------------------
ID               b38fabd3-dd16-439e-8913-59137b3a7f32
Name             zbs-trash-pool-072af8cf-2f79-4102-9515-5089ff2fe18a
Storage Pool     system
Creation Time    2025-07-02 17:35:26.54852529
Resiliency Type  RT_REPLICA
Encrypt Method   ENCRYPT_PLAIN_TEXT
Replica#         2
EC Param
Thin             True
Export           False
Description
Whitelist        */*
Is Prioritized   False
---------------  ---------------------------------------------------
```

## 查看回收站占用的存储空间用量

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin show_usage
```

**输出示例**

```
$ zbs-meta recycle_bin show_usage
--------------------------  ------
Logical Size                0.00 B
Logical Used Size           0.00 B
Sweep Size Until Today End  0.00 B
Sweep Size In 3 Days        0.00 B
Sweep Size In 7 Days        0.00 B
Sweep Size In 30 Days       0.00 B
Sweep Size After 30 Days    0.00 B
--------------------------  ------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Logical Size` | 回收站使用的逻辑空间。 |
| `Logical Used Size` | 回收站实际使用的逻辑存储空间。 |
| `Sweep Size Until Today End` | 今天结束前可清理的实际使用空间。 |
| `Sweep Size In 3 Days` | 未来 3 天内可清理的实际使用空间。 |
| `Sweep Size In 7 Days` | 未来 7 天内可清理的实际使用空间。 |
| `Sweep Size In 30 Days` | 未来 30 天内可清理的实际使用空间。 |
| `Sweep Size After 30 Days` | 30 天后才能清理的实际使用空间。 |

## 查看暂存卷或暂存快照的详细信息

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin show_volume <volume_id_or_snapshot_id> [--show_detail]
```

| 参数 | 说明 |
| --- | --- |
| `--show_detail` | 可选参数，是否显示原始的协议对象，用于查询删除前协议对象的信息，默认不显示。 |

**输出示例**

```
$ zbs-meta recycle_bin show_volume 8104264d-86df-4a63-9ed1-bd18dca36902
-------------------  ------------------------------------
Volume ID            8104264d-86df-4a63-9ed1-bd18dca36902
Name                 8104264d-86df-4a63-9ed1-bd18dca36902
Second Id
Origin Pool Id       640e38ec-e419-48b2-954b-693bb28cb1d6
Deleted Time         2025-07-04 18:01:28.211840745
Expired Time         2025-07-05 18:01:28.0
Protocol Type        ISCSI_Lun
Protocol Name        8104264d-86df-4a63-9ed1-bd18dca36902
Protocol Identifier  1
-------------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Volume ID` | 暂存卷的唯一标识符，与删除前一致。 |
| `Name` | 卷名称，与删除前一致。 |
| `Second Id` | 卷的 secondary ID。 |
| `Origin Pool Id` | 卷所在原始存储池的 ID。 |
| `Deleted Time` | 卷被删除进入回收站的时间。 |
| `Expired Time` | 卷的过期清理时间。 |
| `Protocol Type` | 卷原始类型，如 `ISCSI_Lun`、`NVMF_Namespace`、`NFS_File`、`ZBS_Volume`。 |
| `Protocol Name` | 卷在原协议中的名称。 |
| `Protocol Identifier` | 卷协议标识符（例如 LUN ID、Namespace ID 等）。 |

## 查看所有暂存卷

支持分页列出当前的暂存卷。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin list_volumes <--page_num> <--page_pos> <--last_key> [--show_total_num]
```

| 参数 | 说明 |
| --- | --- |
| `--page_num` | 每页显示的条目数量。 |
| `--page_pos` | 当前请求的页码（从 0 开始）。 |
| `--last_key` | 上一页返回的最后一个 `Volume ID`，用于游标翻页（与 `page_pos` 二选一）。 |
| `--show_total_num` | 可选参数，是否显示回收站总条目数，默认不显示。 |

**输出示例**

```
$ zbs-meta recycle_bin list_volumes --page_num 3 --page_pos 50 --show_total_num
Total Number Of Trash Volumes Is 102
Volume ID                               Name  Second Id    Origin Pool Id                        Deleted Time                   Expired Time           Protocol Type    Protocol Name    Protocol Identifier
------------------------------------  ------  -----------  ------------------------------------  -----------------------------  ---------------------  ---------------  ---------------  ---------------------
ce3ed82a-1b89-4e1a-a403-41db6a74a175      82               1614ee98-be69-4f54-ad43-c9d233fa473e  2025-07-04 18:00:59.161419823  2025-07-05 18:00:59.0  ZBS_Volume
b51fdba7-5e59-4652-a994-b0a52592d775      63               1614ee98-be69-4f54-ad43-c9d233fa473e  2025-07-04 18:00:48.856953257  2025-07-05 18:00:48.0  ZBS_Volume
27b4b3cc-731b-4002-a43a-0111b7dc5377      84               1614ee98-be69-4f54-ad43-c9d233fa473e  2025-07-04 18:01:00.203668965  2025-07-05 18:01:00.0  ZBS_Volume
```

**输出说明**

首行输出当前回收站的卷总数。

| 参数 | 说明 |
| --- | --- |
| `Volume ID` | 暂存卷的唯一标识符，与删除前一致。 |
| `Name` | 卷名称，与删除前一致。 |
| `Second Id` | 卷的 secondary ID。 |
| `Origin Pool Id` | 卷所在原始存储池的 ID。 |
| `Deleted Time` | 卷被删除进入回收站的时间。 |
| `Expired Time` | 卷的过期清理时间。 |
| `Protocol Type` | 卷原始类型，如 `ISCSI_Lun`、`NVMF_Namespace`、`NFS_File`、`ZBS_Volume`。 |
| `Protocol Name` | 卷在原协议中的名称。 |
| `Protocol Identifier` | 卷协议标识符（例如 LUN ID、Namespace ID 等）。 |

## 查看所有暂存快照

分页列出当前的暂存快照。

> **说明**：
>
> 当前版本默认不支持快照进入回收站，需人工开启。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin list_snapshots <--page_num> <--page_pos> <--last_key> [--show_total_num]
```

| 参数 | 说明 |
| --- | --- |
| `--page_num` | 每页显示的条目数量。 |
| `--page_pos` | 当前请求的页码（从 0 开始）。 |
| `--last_key` | 上一页返回的最后一个 `snapshot_id`，用于游标翻页（与 `page_pos` 二选一）。 |
| `--show_total_num` | 可选参数，是否显示回收站总条目数，默认不显示。 |

**输出示例**

```
$ zbs-meta recycle_bin list_snapshots
Snapshot ID                           Name    Second Id    Origin Pool Id                        Origin Volume Id                      Deleted Time                   Expired Time
------------------------------------  ------  -----------  ------------------------------------  ------------------------------------  -----------------------------  ---------------------
4efbf291-e3e4-4210-aa28-700718e63ef6  1-snap               1614ee98-be69-4f54-ad43-c9d233fa473e  f0ec3190-86d7-42b6-a656-1a3c56df0928  2025-07-04 18:22:47.511904702  2025-07-05 18:22:47.0
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| Snapshot ID | 快照的唯一标识符。 |
| Name | 快照名称。 |
| Second Id | 快照的 secondary ID。 |
| Origin Pool Id | 快照所属卷原始的存储池 ID。 |
| Origin Volume Id | 创建该快照时所属的卷 ID。 |
| Deleted Time | 被删除进入回收站的时间。 |
| Expired Time | 回收站中快照的过期时间。 |

---

## 管理回收站 > 从回收站中恢复暂存卷

# 从回收站中恢复暂存卷

## 将指定的暂存卷恢复为 LUN

仅当暂存卷的 `Protocol Type` 卷原始类型为 **ISCSI\_Lun** 时允许执行。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin restore_volume_to_lun <trash_volume_id> <--dst_target_id> <--new_lun_name> <--new_lun_id>
```

| 参数 | 说明 |
| --- | --- |
| trash\_volume\_id | 被恢复的暂存卷的唯一标识符。 |
| --dst\_target\_id | 目标 iSCSI target 的唯一标识符，不指定时，默认恢复至原始 target。 |
| --new\_lun\_name | 指定新还原出的 LUN 名称，不指定时，默认恢复至原始 LUN 的名称。 |
| --new\_lun\_id | 指定的还原后 LUN 的 ID，不指定时，默认恢复至原始 LUN 的 ID。 |

**输出示例**

```
$ zbs-meta recycle_bin restore_volume_to_lun 8104264d-86df-4a63-9ed1-bd18dca36902
--dst_target_id 640e38ec-e419-48b2-954b-693bb28cb1d6 --new_lun_name new-lun-1 --new_lun_id 10
----------------------  ------------------------------------
LUN Id                  10
LUN Name                new-lun-1
Size                    10.00 GiB
Perf Unique Size        In Process
Perf Shared Size        In Process
Cap Unique Size         In Process
Cap Shared Size         In Process
Logical Used Size       In Process
Volume id               8104264d-86df-4a63-9ed1-bd18dca36902
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Encrypt Metadata Id     None
Replica Num             2
EC Param
Thin Provision          True
Creation Time           2025-07-04 18:01:14.859265353
Description
NAA                     33a4dfd6add462401
Allowed Initiators      */*
Single Access           False
PR                      Details
Prefer CID              Unknown
Read Only               Unknown
Secondary ID            Unknown
Is Prioritized          False
Downgraded PRS          0.00 B
Chunk Instances
Labels                  []
Use Host                False
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

**输出说明**

参考[查看 iSCSI LUN 信息](/smtxos/6.3.0/cli_guide/cli_guide_70)的输出说明。

## 将指定的暂存卷恢复为 namespace

仅当暂存卷的 `Protocol Type` 卷原始类型为 **NVMF\_Namespace** 时允许执行。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin restore_volume_to_ns <trash_volume_id> <--dst_subsystem_id> <--new_ns_name>
<--new_ns_id> <--new_ns_group_id> <--new_ns_is_shared>
```

| 参数 | 说明 |
| --- | --- |
| trash\_volume\_id | 被还原的暂存卷的唯一标识符。 |
| --dst\_subsystem\_id | 目标 subsystem ID，暂存卷将被还原至该 subsystem。不指定时，默认恢复至原始 subsystem。 |
| --new\_ns\_name | 新 namespace 的名称。不指定时，默认恢复至原始 namespace 的名称。 |
| --new\_ns\_id | 新 namespace 的 ID。不指定时，默认恢复至原始 namespace 的 ID。 |
| --new\_ns\_group\_id | 所属 namespace 组的 ID，当目的 subsystem 为均衡模式时需要设置。不指定时，默认恢复至原始 namespace 所属组 |
| --new\_ns\_is\_shared | 是否为共享 namespace ，取值为 `true` 或 `false` ，当目的 subsystem 为继承模式时需要设置。不指定时，默认恢复至原始 namespace 配置。 |

**输出示例**

```
$ zbs-meta recycle_bin restore_volume_to_ns afb7c9f9-2162-4345-8882-6652443416b5  --dst_subsystem_id  3bae6e45-1320-4a6a-83d7-bbb53815f2cb --new_ns_name test-bal-100 --new_ns_id 100 --new_ns_group_id fcc489b7-7848-4059-9e1b-cc2fc87f31fc
----------------------  ------------------------------------
NS Id                   100
NS Name                 test-bal-100
Size                    10.00 GiB
Perf Unique Size        In Process
Perf Shared Size        In Process
Cap Unique Size         In Process
Cap Shared Size         In Process
Logical Used Size       In Process
Is Shared               False
Volume id               afb7c9f9-2162-4345-8882-6652443416b5
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Encrypt Metadata Id     Unknown
Replica Num             2
EC Param
Thin Provision          True
Group id                fcc489b7-7848-4059-9e1b-cc2fc87f31fc
Preferred Access        3
Creation Time           2025-07-07 11:19:08.376997524
Description
NQN Whitelist
Single Access           False
Read Only               Unknown
Is Prioritized          False
Downgraded PRS          0.00 B
Chunk Instances
Use Host                False
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 将指定的暂存卷恢复为 file

仅当暂存卷 `Protocol Type` 卷原始类型为 **NFS\_File** 时允许执行。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin restore_volume_to_file <trash_volume_id> <--dst_dir_id>
```

| 参数 | 说明 |
| --- | --- |
| <trash\_volume\_id> | 被恢复的暂存卷的唯一标识符。 |
| --dst\_dir\_id | 目标文件目录的唯一标识符。不指定时，默认恢复至原始文件目录。 |

**输出示例**

```
$ zbs-meta recycle_bin restore_volume_to_file  9a72fa62-da0b-4c4e-aa41-ef18f75073f6 --dst_dir_id 90d97c59-8074-4d68
-----------------  ------------------------------------
id                 9a72fa62-da0b-4c4e
name               test-file
pool               90d97c59-8074-4d68-bcc4-42ee7d417358
preallocate        False
volume             9a72fa62-da0b-4c4e-aa41-ef18f75073f6
type               FILE
Encrypt Method     ENCRYPT_PLAIN_TEXT
mode               432
uid                0
gid                0
size               0.00 B
perf unique size   In Process
perf shared size   In Process
cap unique size    In Process
cap shared size    In Process
logical used size  In Process
prioritized        False
downgraded_prs     0.00 B
-----------------  ------------------------------------
```

## 将指定的暂存快照恢复到存储池

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin restore_snapshot <trash_snapshot_id> <--dst_pool_id> <--new_snapshot_name>
```

| 参数 | 说明 |
| --- | --- |
| trash\_snapshot\_id | 被恢复的暂存快照的唯一标识符。 |
| --dst\_pool\_id | 目标存储池的唯一标识符。不指定时，默认恢复至原始存储池。 |
| --new\_snapshot\_name | 新快照的名称。不指定时，默认恢复至原始快照的名称。 |

**输出示例**

```
$ zbs-meta recycle_bin restore_snapshot 59f1ec4a-0838-430b-9582-bb6f4785c6d5
-------------------  ------------------------------------
ID                   59f1ec4a-0838-430b-9582-bb6f4785c6d5
Name                 snap-1
Parent ID
Size                 1024.00 MiB
Perf Unique Size     In Process
Perf Shared Size     In Process
Cap Unique Size      In Process
Cap Shared Size      In Process
Logical Used Size    In Process
Creation Time        2025-07-07 11:31:11.860730949
Status               VOLUME_ONLINE
Resiliency Type      RT_REPLICA
Encrypt Method       ENCRYPT_PLAIN_TEXT
Encrypt Metadata Id  None
Replica Num          2
EC Param
Thin Provision       True
Read Only            False
Description
Alloc Even           False
Clone count          0
Prefer CID           0
Access Points        []
Is Prioritized       False
Downgraded PRS       0.00 B
Chunk Instances
-------------------  ------------------------------------
```

**输出说明**

参考[查看指定存储卷快照的详细信息](/smtxos/6.3.0/cli_guide/cli_guide_50)的输出说明。

## 将指定的暂存卷恢复到原始存储池

仅当暂存卷的 `Protocol Type` 卷原始类型为 **ZBS\_Volume** 时允许执行。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin restore_volume <trash_volume_id> <--dst_pool_id> <--new_volume_name>
```

| 参数 | 说明 |
| --- | --- |
| trash\_volume\_id | 被恢复的暂存卷的唯一标识符。 |
| --dst\_pool\_id | 目标存储池的唯一标识符。不指定时，默认恢复至原始存储池。 |
| --new\_volume\_name | 新卷的名称。不指定时，默认恢复至原卷的名称 |

**输出示例**

```
$ zbs-meta recycle_bin restore_volume f0ec3190-86d7-42b6-a656-1a3c56df0928
-------------------  ------------------------------------
ID                   f0ec3190-86d7-42b6-a656-1a3c56df0928
Name                 1
Parent ID            1614ee98-be69-4f54-ad43-c9d233fa473e
Size                 1024.00 MiB
Perf Unique Size     In Process
Perf Shared Size     In Process
Cap Unique Size      In Process
Cap Shared Size      In Process
Logical Used Size    In Process
Creation Time        2025-07-04 18:22:29.387646606
Status               VOLUME_ONLINE
Resiliency Type      RT_REPLICA
Encrypt Method       ENCRYPT_PLAIN_TEXT
Encrypt Metadata Id  None
Replica Num          2
EC Param
Thin Provision       True
Read Only            False
Description
Alloc Even           False
Clone count          0
Prefer CID           0
Access Points        []
Is Prioritized       False
Downgraded PRS       0.00 B
Chunk Instances
-------------------  ------------------------------------
```

**输出说明**

参考[查看存储卷上的数据块信息](/smtxos/6.3.0/cli_guide/cli_guide_38)的输出说明。

---

## 管理回收站 > 清理回收站中的暂存卷

# 清理回收站中的暂存卷

## 清理回收站内所有已过期的暂存卷

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin sweep_immediate
```

**输出示例**

无。

## 清理回收站内所有暂存卷

将清理当前所有暂存卷（无论是否过期）。

> **注意**：
>
> 同一时间仅允许一个任务运行，且运行中不可中止。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin start_cleaner
```

**输出示例**

```
$ zbs-meta recycle_bin start_cleaner
---------------  ------------------------------------
Cleaner Running  True
Task UUID        4922e9b2-8b34-4d52-a9f8-3b97b5ae5609
Volume Count     0
Clean Type       ALL
---------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Cleaner Running` | 任务是否在运行。 |
| `Task UUID` | 最新任务的 UUID， 如果任务未在运行，指代上次任务的 UUID，如果任务正在运行，指代当前任务的 UUID。 |
| `Volume Count` | 任务包含的卷数量。 |
| `Clean Type` | 清理类型，默认为全部清理。 |

## 批量清理尚未过期的暂存卷

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin batch_sweep_volumes <volume_ids>
```

| 参数 | 说明 |
| --- | --- |
| <volume\_ids> | 待清理的暂存卷的 ID 集合，用 ‘,’ 间隔。 |

**输出说明**

清理命令本身无输出，可通过 `zbs-meta recycle_bin list_volumes` 检查回收站查看清理对象是否存在。

## 查看当前清理任务的状态

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin show_cleaner
```

**输出示例**

```
$ zbs-meta recycle_bin show_cleaner
---------------  ------------------------------------
Cleaner Running  False
Task UUID        4922e9b2-8b34-4d52-a9f8-3b97b5ae5609
Volume Count     0
Clean Type       ALL
---------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Cleaner Running` | 任务是否在运行。 |
| `Task UUID` | 最新任务的 UUID， 如果任务未在运行，指代上次任务的 UUID，如果任务正在运行，指代当前任务的 UUID。 |
| `Volume Count` | 任务包含的卷数量。 |
| `Clean Type` | 清理类型，默认为全部清理。 |

---

## 管理集群内部 I/O > 管理数据迁移和恢复 > 管理数据恢复

# 管理数据恢复

## 扫描出需要被恢复的数据块

**操作方法**

在集群任一节点执行如下命令，扫描出需要被恢复的数据块：

`zbs-meta recover scan_immediate`

**输出说明**

执行成功无输出。

## 开启数据恢复功能

**操作方法**

在集群任一节点执行如下命令，开启数据恢复功能：

`zbs-meta recover enable`

**输出示例**

```
Enabled
```

## 关闭数据恢复功能

**操作方法**

在集群任一节点执行如下命令，关闭数据恢复功能：

`zbs-meta recover disable`

**输出示例**

```
Disabled
```

## 查询数据恢复的模式

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta recover get_mode_info`

**输出示例**

```
Recover enable: True
Recover scan interval: 60s
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Recover enable` | 是否已开启数据恢复功能。 |
| `Recover scan interval` | 数据恢复扫描时间间隔。 |

## 查看集群中正在恢复的数据块

**操作方法**

在集群任一节点执行如下命令，查询正在恢复的数据块：

`zbs-meta recover list`

**输出示例**

```
No recovery command is running.
```

## 调节恢复速度

请参考[设置内部 I/O 的模式和优先级](/smtxos/6.3.0/cli_guide/cli_guide_63)。

---

## 管理集群内部 I/O > 管理数据迁移和恢复 > 管理数据迁移

# 管理数据迁移

## 扫描出需要被迁移的数据块

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta migrate scan_immediate`

**输出说明**

执行成功无输出。

## 开启数据迁移功能

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta migrate enable`

**输出示例**

```
Enabled
```

## 关闭数据迁移功能

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta migrate disable`

**输出示例**

```
Disabled
```

## 查询当前迁移数据的模式

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta migrate get_mode_info`

**输出示例**

```
Migrate enable: True
Migrate scan interval: 120s
Perf thick ratio: 0.722, load: LOAD_HIGH
Perf thin  ratio: 0.494, load: LOAD_LOW
Cap        ratio: 0.346, load: LOAD_LOW
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Migrate enable` | 数据迁移是否已开启。 |
| `Migrate scan interval` | 数据迁移扫描时间间隔。 |
| `Perf thick load` | Pin 空间的负载状态。 |
| `Perf thin load` | 性能层空间负载状态。 |
| `Cap load` | 容量层空间负载状态。 |

## 查看集群中正在迁移的数据块

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta migrate list`

**输出示例**

```
No migration command is running.
```

## 迁移指定数据块

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta migrate pextent <pid> <src_cid> <dst_cid> <replace_cid> [--ignore_topo_safety]`

| 参数 | 说明 |
| --- | --- |
| `src_cid` | 源端 chunk ID。 |
| `dst_cid` | 目的端 chunk ID。 |
| `replace_cid` | 待移除 chunk ID。 |
| `--ignore_topo_safety` | 本次迁移是否忽略拓扑安全，默认为 `False`。 |

**输出说明**

执行成功无输出。

## 本地聚集指定虚拟卷

**操作方法**

在集群任一节点执行如下命令，将指定虚拟卷上的数据块手动迁移到各自的 prefer local 节点上：

`zbs-meta migrate volume <volume_id> [--ignore_perf] [--ignore_cap]`

| 参数 | 说明 |
| --- | --- |
| `volume_id` | 指定的虚拟卷 ID。 |
| `--ignore_perf` | 忽略在性能层上的数据块。 |
| `--ignore_cap` | 忽略在容量层上的数据块。 |

**使用示例**

`$ zbs-meta migrate volume 135a8de9-64f7-4e89-a81c-844976d871be --ignore_perf`

**输出示例**

```
need_migrate_num: 10
```

该输出表示该虚拟卷上将有 10 个数据块被迁移到它们各自的 prefer local 节点上。

## 清空手动触发的迁移命令

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta migrate clear_manual_migrate`

手动触发的迁移命令还未生成时，集群将不会自动生成迁移命令，此时可借助这条命令恢复系统的自动迁移。

**输出示例**

执行成功无输出。

## 查询卸载盘上待迁移数据块的上报配置

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta migrate show_umounting_report_option`

**输出示例**

```
Report enable:  True
Include cache:  False
Include partition:  True
Max report size:  2048
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Report enable` | 集群中的 chunk 是否上报让 meta 辅助迁移的待卸载数据块。 |
| `Include cache` | 集群中的 chunk 是否上报在性能层的待卸载数据块，默认为 `False`。 |
| `Include partition` | 集群中的 chunk 是否上报在容量层的待卸载数据块，默认为 `True`。 |
| `Max report size` | 集群中的 chunk 单次最多上报待卸载数据块的数量。 |

## 更新卸载盘上待迁移数据块的上报配置

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta migrate update_umounting_report_option [--report_enable] [--include_cache] [--include_partition] [--max_report_size]`

**输出说明**

执行成功无输出。

**使用示例**

`$ zbs-meta migrate update_umounting_report_option --include_partition True --max_report_size 1024`

## 查询卸载盘上的待迁移数据块

**操作方法**

在集群任一节点执行如下命令，查看 chunk 上报的卸载盘上的待迁移数据块：

`zbs-meta migrate list_umounting_pextents [--cid CID] [--length LENGTH] [--ignore_ec] [--show_details]`

| 参数 | 说明 |
| --- | --- |
| `--cid` | 指定 chunk ID，不指定时查询所有 chunk 卸载盘上的待迁移数据块。 |
| `--length` | 设置返回的 pextents 的数量。默认值以及最大值均为 `1024`。 |
| `--ignore_ec` | 是否忽略冗余类型为 EC 的数据块，默认为 `False`。 |
| `--show_details` | 是否显示卸载盘上的待迁移数据块的具体信息，默认不显示。 |

**使用示例**

`$ zbs-meta migrate list_umounting_pextents --cid 4 --show_details`

**输出示例**

```
Umounting cid: 4, cap report size: 5
    Pid    Umounting Cid  Pextent Type    Resiliency Type    Thin Provision
-------  ---------------  --------------  -----------------  ----------------
2798982                4  PT_CAP          RT_REPLICA         True
2822009                4  PT_CAP          RT_EC              True
2822033                4  PT_CAP          RT_EC              True
2937914                4  PT_CAP          RT_REPLICA         True
2954389                4  PT_CAP          RT_EC              True
```

## 调节迁移速度

请参考[设置内部 I/O 的模式和优先级](/smtxos/6.3.0/cli_guide/cli_guide_63)。

---

## 管理集群内部 I/O > 管理数据迁移和恢复 > 管理任务

# 管理任务

## 查看集群中恢复和迁移任务的概况

**操作方法**

在集群任一节点执行如下命令，输出恢复和迁移任务的概况：

`zbs-meta reposition summary [--chunk_id <CHUNK_ID>]`

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `--chunk_id <CHUNK_ID>` | 可选参数，选择是否查看指定节点的信息。 |

**输出示例**

```
chunk ID    Cap Src    Cap Replace    Cap Dst    Perf Src    Perf Replace    Perf Thin Dst    Perf Thick Dst
----------  ---------  -------------  ---------  ----------  --------------  ---------------  ----------------
    1          0              0          0           0               0                0                 0
    2          0              0          0           0               0                0                 0
    3          0              0          0           0               0                0                 0
    4          0              0          0           0               0                0                 0
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Chunk ID` | 节点的 chunk ID。 |
| `Cap Src` | 容量层将该节点作为源端的恢复和迁移任务的数量。 |
| `Cap Replace` | 容量层将该节点作为替换端的恢复和迁移任务的数量。 |
| `Cap Dst` | 容量层将该节点作为目的端的恢复和迁移任务的数量。 |
| `Perf Src` | 性能层将该节点作为源端的恢复和迁移任务的数量。 |
| `Perf Replace` | 性能层将该节点作为替换端的恢复和迁移任务的数量。 |
| `Perf Thin Dst` | 性能层将该节点作为目的端的非 pin 恢复和迁移任务的数量。 |
| `Perf Thick Dst` | 性能层将该节点作为目的端的 pin in perf 恢复和迁移任务的数量。 |

## 查看集群中恢复和迁移任务的详细信息

**操作方法**

在集群任一节点执行如下命令，输出恢复和迁移任务的详细信息：

`zbs-meta reposition show`

**输出示例**

```
1. Recover Manager params:
Reposition thread wakeup interval: 4s
Current generate cmds per round limit: 1024
Current cap distribute cmds per chunk limit: 128
Current perf distribute cmds per chunk limit: 256

1.1 Recover params:
Recover enable: True
Recover scan interval: 60s

1.2 Migrate params:
Migrate enable: True
Migrate scan interval: 120s
Perf thick ratio: 0.722, load: LOAD_HIGH
Perf thin  ratio: 0.494, load: LOAD_LOW
Cap        ratio: 0.346, load: LOAD_LOW

2. Recover Handler params:
Reposition mode: REPOSITION_STATIC
Max cap reposition concurrency limit: 64
Max perf reposition concurrency limit: 128

Static cap reposition concurrency limit: 16
Static perf reposition concurrency limit: 32

Owner Cid 1 Reposition Concurrency Info
  Cmd Cid    Cur Cap Concurrency    Cur Cap Concurrency Limit    Cur Perf Concurrency    Cur Perf Concurrency Limit
---------  ---------------------  ---------------------------  ----------------------  ----------------------------
        1                      0                           16                      32                            32
        2                      0                           16                      32                            32
        3                      0                           16                       0                            32
        4                      0                           16                       0                            32

Owner Cid 2 Reposition Concurrency Info
  Cmd Cid    Cur Cap Concurrency    Cur Cap Concurrency Limit    Cur Perf Concurrency    Cur Perf Concurrency Limit
---------  ---------------------  ---------------------------  ----------------------  ----------------------------
        1                      0                           16                       0                            32
        2                      0                           16                       0                            32
        3                      0                           16                       0                            32
        4                      0                           16                       0                            32

Owner Cid 3 Reposition Concurrency Info
  Cmd Cid    Cur Cap Concurrency    Cur Cap Concurrency Limit    Cur Perf Concurrency    Cur Perf Concurrency Limit
---------  ---------------------  ---------------------------  ----------------------  ----------------------------
        1                      0                           16                       0                            32
        3                      0                           16                       0                            32

Owner Cid 4 Reposition Concurrency Info
  Cmd Cid    Cur Cap Concurrency    Cur Cap Concurrency Limit    Cur Perf Concurrency    Cur Perf Concurrency Limit
---------  ---------------------  ---------------------------  ----------------------  ----------------------------
        1                      0                           16                      15                            32
        2                      0                           16                      15                            32
        3                      0                           16                       0                            32
        4                      0                           16                       0                            32
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Reposition thread wakeup interval` | Meta 恢复和迁移线程唤醒的时间间隔。 |
| `Current generate cmds per round limit` | 每一轮生成恢复和迁移命令的数量的上限。 |
| `Current cap distribute cmds per chunk limit` | 每一个 chunk 生成容量层恢复和迁移命令的数量的上限。 |
| `Current perf distribute cmds per chunk limit` | 每一个 chunk 生成性能层恢复和迁移命令的数量的上限。 |
| `Recover scan interval` | 恢复扫描的时间间隔。 |
| `Migrate scan interval` | 迁移扫描的时间间隔。 |
| `Perf thick load` | 性能层 pin in perf 负载水位。 |
| `Perf thin load` | 性能层非 pin 负载水位。 |
| `Cap load` | 容量层负载水位。 |
| `Reposition mode` | 当前恢复和迁移任务并发度限制的模式（静态/动态）。 |
| `Max cap reposition concurrency limit` | 容量层恢复和迁移任务并发度上限的最大值。 |
| `Max perf reposition concurrency limit` | 性能层恢复和迁移任务并发度上限的最大值。 |
| `Static cap reposition concurrency limit` | 容量层静态模式下恢复和迁移任务并发度上限。 |
| `Static perf reposition concurrency limit` | 性能层静态模式下恢复和迁移任务并发度上限。 |
| `Cur Cap Concurrency` | 当前容量层恢复和迁移任务的并发度。 |
| `Cur Cap Concurrency Limit` | 当前容量层恢复和迁移任务的并发度上限。 |
| `Cur Perf Concurrency` | 当前性能层恢复和迁移任务的并发度。 |
| `Cur Perf Concurrency Limit` | 当前容量层恢复和迁移任务的并发度上限。 |

## 更改集群中恢复和迁移任务的设置

**操作方法**

在集群任一节点执行如下命令，更改恢复和迁移任务的设置：

`zbs-meta reposition update [--mode <MODE>] [--static_cap_reposition_concurrency_limit <STATIC_CAP_REPOSITION_CONCURRENCY_LIMIT>] [--static_perf_reposition_concurrency_limit <STATIC_PERF_REPOSITION_CONCURRENCY_LIMIT>] [--static_generate_cmds_per_round_limit <STATIC_GENERATE_CMDS_PER_ROUND_LIMIT>] [--static_cap_distribute_cmds_per_chunk_limit <STATIC_CAP_DISTRIBUTE_CMDS_PER_CHUNK_LIMIT>] [--static_perf_distribute_cmds_per_chunk_limit <STATIC_PERF_DISTRIBUTE_CMDS_PER_CHUNK_LIMIT>]`

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `--mode <MODE>` | 可选参数，更改并发度限制的模式：`0`（动态），`1`（静态）。 |
| `--static_cap_reposition_concurrency_limit <STATIC_CAP_REPOSITION_CONCURRENCY_LIMIT>` | 可选参数，更改容量层并发度限制静态模式下的并发度上限。 |
| `--static_perf_reposition_concurrency_limit <STATIC_PERF_REPOSITION_CONCURRENCY_LIMIT>` | 可选参数，更改性能层并发度限制静态模式下的并发度上限。 |
| `--static_generate_cmds_per_round_limit <STATIC_GENERATE_CMDS_PER_ROUND_LIMIT>` | 可选参数，设置每一轮生成恢复和迁移命令的数量的上限。 |
| `--static_cap_distribute_cmds_per_chunk_limit <STATIC_CAP_DISTRIBUTE_CMDS_PER_CHUNK_LIMIT>` | 可选参数，设置对每一个 chunk 生成容量层恢复和迁移命令的数量的上限。 |
| `--static_perf_distribute_cmds_per_chunk_limit <STATIC_PERF_DISTRIBUTE_CMDS_PER_CHUNK_LIMIT>` | 可选参数，设置对每一个 chunk 生成性能层恢复和迁移命令的数量的上限。 |

**输出说明**

执行成功无输出。

---

## 管理集群内部 I/O > 管理数据下沉和下沉策略 > 管理数据下沉

# 管理数据下沉

分层部署的集群默认按照数据的冷热程度自动分层，访问频率较高的数据将停留在速度更快的性能层，访问频率较低的数据将下沉至速度相对较慢的容量层。本节介绍的命令用于管理集群的数据下沉。

**注意事项**

本节描述的命令仅适用于排查问题，以及查看集群的内部状态。若不明确了解这些命令带来的影响，请勿使用这些命令改变集群的默认行为。

## 开启数据下沉功能

**操作方法**

在集群任一节点执行如下命令，开启数据下沉功能：

`zbs-meta drain enable`

**输出示例**

```
Enabled
```

## 关闭数据下沉功能

**操作方法**

在集群任一节点执行如下命令，关闭数据下沉功能：

`zbs-meta drain disable`

**输出示例**

```
Disabled
```

## 设置数据下沉的相关参数

**操作方法**

在集群任一节点执行如下命令，设置数据下沉的相关参数：

`zbs-meta drain update [--cmd_timeout_ms <CMD_TIMEOUT_MS>] [--generate_cmds_per_round_limit <GENERATE_CMDS_PER_ROUND_LIMIT>] [--distribute_cmds_per_chunk_limit <DISTRIBUTE_CMDS_PER_CHUNK_LIMIT>]`

| 参数 | 说明 |
| --- | --- |
| `--cmd_timeout_ms <CMD_TIMEOUT_MS>` | 可选参数，指定下沉命令的超时时间（毫秒），默认值为 `600000`，取值范围为 `60000 ～ 720000`。 |
| `--generate_cmds_per_round_limit <GENERATE_CMDS_PER_ROUND_LIMIT>` | 可选参数，指定集群每次下发的下沉命令的最大数量，默认值为 `1024`，取值范围为 `2 ～ 4096`。 |
| `--distribute_cmds_per_chunk_limit <DISTRIBUTE_CMDS_PER_CHUNK_LIMIT>` | 可选参数，指定集群为每个 chunk 生成的下沉命令的最大数量，默认值为 `128`，取值范围为 `2 ～ 4096`。 |

**输出说明**

执行成功无输出。

## 查询数据下沉的相关参数

**操作方法**

在集群任一节点执行如下命令，查询当前数据下沉的相关参数：

`zbs-meta drain show`

**输出示例**

```
Cluster enable drain: 1
Allow drain: 0
Scan interval: 180s
Generate cmds interval: 30s
Drain no lease timeout: 600s
Drain cmd timeout: 600s
Max number of drain cmds generated per round: 1024
Max number of drain cmds distributed per chunk: 128
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Cluster enable drain` | 集群是否开启数据下沉功能，`1` 代表已开启，`0` 代表未开启。 |
| `Allow drain` | 数据下沉是否已被下沉策略开启，`1` 代表已开启，`0` 代表未开启。 |
| `Scan interval` | 集群扫描间隔时间。 |
| `Generate cmds interval` | 生成下沉命令的间隔时间。 |
| `Drain no lease timeout` | 数据块维持无 lease 状态的时间超过该值时，下发下沉命令。 |
| `Drain cmd timeout` | 下沉命令的超时时间。 |
| `Max number of drain cmds generated per round` | 集群每次下发的下沉命令的最大数量。 |
| `Max number of drain cmds distributed per chunk` | 集群为每个 chunk 生成的下沉命令的最大数量。 |

## 查看集群中正在下沉的数据块

**操作方法**

在集群任一节点执行如下命令，查看正在下沉的数据块：

`zbs-meta drain list`

**输出示例**

```
No drain command is running.
```

---

## 管理集群内部 I/O > 管理数据下沉和下沉策略 > 管理下沉策略

# 管理下沉策略

下沉策略根据集群当前性能层的使用负载判定下沉档位，从而动态调整需要下沉的数据量、数据下沉参数及容量层直写模式等策略。本节介绍的命令用于管理集群的下沉策略。

**注意事项**

本节描述的命令仅适用于排查问题，以及查看集群的内部状态。若不明确了解这些命令带来的影响，请勿使用这些命令改变集群的默认行为。

## 触发下沉策略的更新

**操作方法**

在集群任一节点执行如下命令，立即触发下沉策略的更新：

`zbs-meta sink scan_immediate`

**输出说明**

执行成功无输出。

## 设置下沉策略的相关参数

下沉策略包含四种档位，系统可根据集群的当前性能层使用负载进行动态调节：

- SINK\_LOW：低档位
- SINK\_MID：中档位
- SINK\_HIGH：高档位
- SINK\_VERY\_HIGH：超高档位

容量层直写模式共有四种，仅适用于冗余策略为副本的卷：

- CAP\_DIO\_DISABLED：禁用容量层直写
- CAP\_DIO\_BLOCK\_ALIGNED\_ONLY: 仅对 256 KiB 对齐的 I/O 进行容量层直写
- CAP\_DIO\_ALL\_THROTTLED: 对被性能层限流的 I/O 进行容量层直写，与 CAP\_DIO\_BLOCK\_ALIGNED\_ONLY 相同
- CAP\_DIO\_ALL: 仅对 8 KiB 对齐的 I/O 进行容量层直写

**操作方法**

在集群任一节点执行如下命令，设置下沉策略的相关参数：

`zbs-meta sink update [--inactive_lease_interval_map <INACTIVE_LEASE_INTERVAL_MAP>] [--no_lease_timeout_map <NO_LEASE_TIMEOUT_MAP>] [--cap_direct_write_policy_map <CAP_DIRECT_WRITE_POLICY_MAP>] [--prefer_cap_passthru <PREFER_CAP_PASSTHRU>]`

| 参数 | 说明 |
| --- | --- |
| `--inactive_lease_interval_map <INACTIVE_LEASE_INTERVAL_MAP>` | 可选参数，指定不同下沉档位对应的判定 lease 是否活跃的时间阈值。 |
| `--no_lease_timeout_map <NO_LEASE_TIMEOUT_MAP>` | 可选参数，指定不同下沉档位对应的判定是否对无 lease extent 下发下沉命令的时间阈值。 |
| `--cap_direct_write_policy_map <CAP_DIRECT_WRITE_POLICY_MAP>` | 可选参数，指定不同下沉档位对应的容量层直写策略。 |
| `--prefer_cap_passthru <PREFER_CAP_PASSTHRU>` | 可选参数，指定携带 PREFER\_CAP IO Flag 的写 I/O 是否应在满足条件时直写容量层。 |

**输出说明**

执行成功无输出。

## 查询下沉策略的相关参数

**操作方法**

在集群任一节点执行如下命令，查询当前下沉策略的相关参数：

`zbs-meta sink show`

**输出示例**

```
Sink scan interval: 10s
Sink mode:  SINK_LOW
Sink load: 0.42
Sink mid load ratio: 0.50
Sink high load ratio: 0.80
Sink very high load ratio: 0.95
Drain parent start mode:  SINK_LOW
Drain idle start mode:  SINK_MID
Cap direct write policy:  CAP_DIO_BLOCK_ALIGNED_ONLY
Start cap direct write in SINK_LOW ratio: 0.40
Prefer cap passthru:  False
Access reserve block num: reserve all
Inactive lease interval (sec) map:  (SINK_MID, 1800), (SINK_HIGH, 900), (SINK_VERY_HIGH, 180)
No lease timeout (ms) map:  (SINK_LOW, 600000), (SINK_MID, 600000), (SINK_HIGH, 300000), (SINK_VERY_HIGH, 180000)
Cap direct write policy map:  (SINK_LOW, CAP_DIO_DISABLED), (SINK_MID, CAP_DIO_BLOCK_ALIGNED_ONLY), (SINK_HIGH, CAP_DIO_ALL_THROTTLED), (SINK_VERY_HIGH, CAP_DIO_ALL)
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Sink scan interval` | 更新下沉策略的间隔时间。 |
| `Sink mode` | 当前下沉档位。 |
| `Sink load` | 当前性能层使用负载，使用该值判定当前的下沉档位。 |
| `Sink mid load ratio` | 性能层使用负载高于该值时，集群进入下沉中档位。 |
| `Sink high load ratio` | 性能层使用负载高于该值时，集群进入下沉高档位。 |
| `Sink very high load ratio` | 性能层使用负载高于该值时，集群进入下沉超高档位。 |
| `Drain parent start mode` | 开始对 parent extent 下发下沉命令的下沉档位。 |
| `Drain idle start mode` | 开始对无 lease extent 下发下沉命令的下沉档位。 |
| `Cap direct write policy` | 当前的容量层直写策略。 |
| `Start cap direct write in SINK_LOW ratio` | 在当前下沉档位为低档位且 `Sink load` 高于该值时，开启容量层直写。 |
| `Prefer cap passthru` | 携带 PREFER\_CAP IO Flag 的写 I/O 是否应在满足条件时直写容量层。 |
| `Access reserve block num` | Access 当前可保留的数据块数量。 |
| `Inactive lease interval (sec) map` | 不同下沉档位对应的判定 lease 是否活跃的时间阈值。 |
| `No lease timeout (ms) map` | 不同下沉档位对应的判定是否对无 lease extent 下发下沉命令的时间阈值。 |
| `Cap direct write policy map` | 不同下沉档位对应的容量层直写策略。 |

---

## 管理集群内部 I/O > 管理 I/O 模式和优先级

# 管理 I/O 模式和优先级

您可以通过命令管理集群内部 I/O 的模式和优先级。

内部 I/O 包含两种模式：

- AUTO：智能调节模式，根据当前系统负载自动调节内部 I/O 的速度。
- STATIC：静态调节模式，可指定内部 I/O 的最大速率。集群的空间分为性能层（perf） 和 容量层（cap），性能层和容量层的限速不同，可分别设置。

内部 I/O 包括 recover I/O （数据恢复 I/O），sink I/O（数据下沉 I/O） 和 migrate I/O （数据迁移 I/O）。每种内部 I/O 都可以设置优先级，优先级高的内部 I/O 执行更快。内部 I/O 包括三种优先级:

- INTERNAL\_HIGH: 高优先级
- INTERNAL\_MID: 中优先级
- INTERNAL\_LOW: 低优先级

集群内部 I/O 的优先级默认设置如下；

- recover I/O: INTERNAL\_HIGH
- sink I/O: INTERNAL\_MID
- migrate I/O: INTERNAL\_LOW

## 设置内部 I/O 的模式和优先级

内部 I/O 模式和内部 I/O 优先级可独立设置。

**操作方法**

在集群任一节点执行如下命令，设置内部 I/O 的模式和优先级：

`zbs-meta internal_io update [-h] [--mode <MODE>] [--static_cap_internal_io_speed_limit <STATIC_CAP_INTERNAL_IO_SPEED_LIMIT>] [--static_perf_internal_io_speed_limit <STATIC_PERF_INTERNAL_IO_SPEED_LIMIT>] [--recover <RECOVER>] [--sink <SINK>] [--migrate <MIGRATE>]`

| 参数 | 说明 |
| --- | --- |
| `-h` | 可选参数，输出 update 命令行帮助信息。 |
| `--mode <MODE>` | 指定内部 I/O 的模式：  - `AUTO`：智能调节模式。此模式是默认模式。 - `STATIC`：静态调节模式。只允许对 meta 下的所有 chunk 设置同一限额，不能够对每个 chunk 单独设置。 |
| `--static_perf_internal_io_speed_limit <STATIC_PERF_INTERNAL_IO_SPEED_LIMIT>` | 可选参数，且只有在上述 mode 设置为 `STATIC` 时才生效。此参数指定性能层内部 I/O 的最大速率（MiB/s）。  如果 mode 被设置为 `AUTO`，但又设置了该参数，则该参数的设置不生效。 |
| `--static_cap_internal_io_speed_limit <STATIC_CAP_INTERNAL_IO_SPEED_LIMIT>` | 可选参数，且只有在上述 mode 设置为 `STATIC` 时才生效。此参数指定容量层内部 I/O 的最大速率（MiB/s）。  如果 mode 被设置为 `AUTO`，但又设置了该参数，则该参数的设置不生效。 |
| `--recover <RECOVER>` | 可选参数，与模式无关，可单独设置。此参数指定 recover I/O 的优先级（`INTERNAL_HIGH > INTERNAL_MID > INTERNAL_LOW`） **注意：**若对内部 I/O 的优先级无强烈的变更需求，建议不改变集群的默认设置（`INTERNAL_HIGH`）。 |
| `--sink <SINK>` | 可选参数，与模式无关，可单独设置。此参数指定 sink I/O 的优先级（`INTERNAL_HIGH` > `INTERNAL_MID` > `INTERNAL_LOW`） **注意：**若对内部 I/O 的优先级无强烈的变更需求，建议不改变集群的默认设置（`INTERNAL_MID`）。 |
| `--migrate <MIGRATE>` | 可选参数，与模式无关，可单独设置。此参数指定 migrate I/O 的优先级（`INTERNAL_HIGH` > `INTERNAL_MID` > `INTERNAL_LOW`） **注意：**若对内部 I/O 的优先级无强烈的变更需求，建议不改变集群的默认设置（`INTERNAL_LOW`）。 |

**输出说明**

执行成功无输出。

## 查询当前内部 I/O 的模式和优先级

**操作方法**

在集群任一节点执行如下命令，查询当前内部 I/O 的模式和优先级：

`zbs-meta internal_io show`

**输出示例**

```
Internal I/O mode: INTERNAL_IO_STATIC
Static cap speed limit: 104.86 MB/s(100.00 MiB/s)
Static perf speed limit: 209.72 MB/s(200.00 MiB/s)
Recover I/O Priority: INTERNAL_HIGH
Sink I/O Priority: INTERNAL_MID
Migrate I/O Priority: INTERNAL_LOW

Session ID                            IP           Current Cap Speed Limit    Cap HW Speed Limit     Current Perf Speed Limit    Perf HW Speed Limit
------------------------------------  -----------  -------------------------  ---------------------  --------------------------  ---------------------
1e654354-e233-4fc3-a5ac-4338bb379bed  10.0.130.82  104.86 MB/s(100.00 MiB/s)  1.56 GB/s(1.46 GiB/s)  209.72 MB/s(200.00 MiB/s)   1.26 GB/s(1.17 GiB/s)
27ddc961-86df-4019-9c5e-9171d42d0f29  10.0.130.84  104.86 MB/s(100.00 MiB/s)  1.56 GB/s(1.46 GiB/s)  209.72 MB/s(200.00 MiB/s)   1.26 GB/s(1.17 GiB/s)
30d56eee-bb9b-4082-a9fa-15a410ec716b  10.0.130.83  104.86 MB/s(100.00 MiB/s)  1.56 GB/s(1.46 GiB/s)  209.72 MB/s(200.00 MiB/s)   1.26 GB/s(1.17 GiB/s)
fcc1166a-0de6-40a3-839b-c71c9d5bd4e4  10.0.130.81  104.86 MB/s(100.00 MiB/s)  1.56 GB/s(1.46 GiB/s)  209.72 MB/s(200.00 MiB/s)   1.26 GB/s(1.17 GiB/s)
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Interal I/O mode` | 内部 I/O 模式。 |
| `Static cap speed limit` | 静态容量层内部 I/O 限速。 |
| `Static perf speed limit` | 静态性能层内部 I/O 限速。 |
| `Recover I/O Priority` | Recover I/O 优先级。 |
| `Sink I/O Priority` | Sink I/O 优先级。 |
| `Migrate I/O Priority` | Migrate I/O 优先级。 |
| `Current Cap Speed limit` | 当前容量层内部 I/O 限速。 |
| `Cap HW Speed limit` | 当前容量层内部 I/O 硬件决定的限速的最大值。 |
| `Currnet Perf Speed limit` | 当前性能层内部 I/O 限速。 |
| `Perf HW Speed limit` | 当前性能层内部 I/O 硬件决定的限速的最大值。 |

---

## 管理 NFS 存储服务

# 管理 NFS 存储服务

当 SMTX OS 集群部署在 VMware ESXi 平台时，ZBS 作为存储服务运行在 SCVM 中，通过 NFS 协议将 ZBS 存储对象转化为 NFS 目录/文件，并对外提供标准的 NFS 访问接口。VMware ESXi 可以通过私有网络访问到 NFS 服务，通过创建数据存储将 NFS Export 挂载到 ESXi 主机，提供给虚拟机使用。

---

## 管理 NFS 存储服务 > 管理 NFS Export

# 管理 NFS Export

## 创建 NFS Export

**操作方法**

在集群任一节点执行如下命令，创建名为指定名称的 Export：

`zbs-nfs export create <export_name>`

**输出示例**

```
---------------  ------------------------------------
ID               8dedc9e8-d1ed-4451-abb9-48bd0804734b
Name             ex5
Storage Pool     system
Creation Time    2024-06-18 14:59:54.769150602
Resiliency Type  RT_REPLICA
Encrypt Method   ENCRYPT_PLAIN_TEXT
Replica#         2
EC Param
Thin             True
Description
Whitelist        */*
Stripe Num       4
Stripe Size      262144
---------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Resiliency Type` | 冗余模式。 |
| `Replica#` | 副本冗余模式下对应的副本数。 |
| `Encrypt Method` | 数据存储的加密方法。 |
| `EC Param` | EC 冗余模式下对应的 EC 参数。 |
| `Thin` | 是否是精简置备。 |
| `Description` | Export 描述。 |
| `Whitelist` | IPv4 白名单。 |
| `StripeNum` | 条带数。 |
| `StripeSize` | 单个条带大小 单位：Byte。 |

## 查看 NFS Export

**操作方法**

在集群任一节点执行如下命令，查看 NFS Export：

`zbs-nfs export list`

**输出示例**

```
ID                                    Name                                                                Storage Pool    Creation Time                  Resiliency Type      Replica#  EC Param    Thin    Description         Whitelist                                 Stripe Num    Stripe Size
------------------------------------  ------------------------------------------------------------------  --------------  -----------------------------  -----------------  ----------  ----------  ------  ------------------  --------------------------------------  ------------  -------------
3d3b3d48-2e74-448e-8af0-9981c117e557  advanced-monitoring-instances-fef6f2ea-e2fd-44ba-ac17-f78555e74e7e  system          2024-06-17 14:09:59.169416063  RT_REPLICA                  3              True                        */*                                                4         262144
5a7f9661-ec37-4417-9277-4adcfaf26f55  zbs-images                                                          system          2024-06-17 14:12:43.298885514  RT_REPLICA                  3              True    Auto create export  10.2.234.196,10.2.234.198,10.2.234.197             4         262144
615b512f-5c66-436e-9139-a74a9d3ecf0b  nfs-volume-template                                                 system          2024-06-17 14:12:44.165056027  RT_REPLICA                  3              True    Auto create export  10.2.234.196,10.2.234.198,10.2.234.197             4         262144
8dedc9e8-d1ed-4451-abb9-48bd0804734b  ex5                                                                 system          2024-06-18 14:59:54.769150602  RT_REPLICA                  2              True                        */*                                                4         262144
b2640265-e6af-4854-9efb-4ccbbe7739ba  e1                                                                  system          2024-06-17 19:29:30.378361779  RT_REPLICA                  2              True                        */*                                                4         262144
ce75ff79-bb94-4ac5-8c61-1709bc3f925d  advanced-monitoring-images-fef6f2ea-e2fd-44ba-ac17-f78555e74e7e     system          2024-06-17 14:09:53.882235699  RT_REPLICA                  3              True                        */*                                                4         262144
f6722181-7eb8-4ab4-ac39-7a06d29f6890  zbs-volumes                                                         system          2024-06-17 14:12:43.740327641  RT_REPLICA                  3              True    Auto create export  10.2.234.198,10.2.234.197,10.2.234.196             4         262144
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Resiliency Type` | 冗余模式。 |
| `Replica#` | 副本冗余模式下对应的副本数。 |
| `Encrypt Method` | 数据存储的加密方法。 |
| `EC Param` | EC 冗余模式下对应的 EC 参数。 |
| `StripeNum` | 条带数。 |
| `Thin` | 是否是精简置备。 |
| `Description` | Export 描述。 |
| `Whitelist` | IPv4 白名单。 |
| `StripeSize` | 单个条带大小 单位：Byte。 |

## 更新 NFS Export

用户可以通过命令行更新 NFS Export 如下信息：

- 名称、描述
- 置备方式
- 副本数
- 白名单

**操作方法**

在集群任一节点执行如下命令，更新指定名称的 NFS Export：

`zbs-nfs export update <export_name> [optional arguments]`

| 参数 | 说明 |
| --- | --- |
| `--new_name <new_name>` | 把原名为 `export_name` 的 NFS Export 的重新命名为 `new_name`。例如：  `zbs-nfs export update Colour --new_name Couleur`  把名字为 `Colour` 的 NFS Export 重新命名为 `Couleur`。 |
| `--thin_provision {true|false}` | 设置 NFS Export 是否为精简配置。例如：  `zbs-nfs export update Export-centre --thin_provision false`  把名为 `Export-centre` 的 NFS Export 设置为非精简配置。 |
| `--replica_num <replica_factor>` | 重置 NFS Export 的副本数，取值范围只能是 `1`、`2` 或 `3`，超出此范围会报错。例如：  `zbs-nfs export update Organised-exporter --replica_num 3`  把名为 `Organised-exporter` 的 NFS Export 的副本数设置为 `3`。 |
| `--des <description>` | 更新 NFS Export 的描述。例如：  `zbs-nfs export update Organised-exporter --des "Organised-exporter"`  把名为 `Organised-exporter` 的 NFS Export 的描述设置为 `Organised-exporter`。 |
| `--whitelist <white_list>` | 更新 NFS Export 的白名单，白名单中的 IP 可以此 Export。取值可以为：   - 普通 IP：例如 192.168.67.25 - CIDR 块：例如 192.168.10.0/24 - `*/*`：表示任何 IP 都可以访问此 Export。   例如：  `zbs-nfs export update zpp-exporter --whitelist */*`  `zbs-nfs export update zpp-exporter --whitelist 192.168.10.0/24` |

**输出说明**

执行成功无输出。

## 删除 NFS Export

**操作方法**

在集群任一节点执行如下命令，删除指定名称的 Export：

`zbs-nfs export delete <export_name>`

**输出说明**

执行成功无输出。

---

## 管理 NFS 存储服务 > 管理 inode

# 管理 inode

## 查看 inode

### 查看指定路径下 inode

**操作方法**

在集群任一节点执行如下命令，查看指定的 `dir_id` 路径下的 inode。

`zbs-nfs inode list <dir_id>`

**输出示例**

```
id                  name    pool                                  preallocate    volume                                type    Encrypt Method        mode    uid    gid  size    perf unique size    perf shared size    cap unique size    cap shared size    logical used size    prioritized    downgraded_prs
------------------  ------  ------------------------------------  -------------  ------------------------------------  ------  ------------------  ------  -----  -----  ------  ------------------  ------------------  -----------------  -----------------  -------------------  -------------  ----------------
512c83c1-15db-4271  nfs1    ea479340-5d9d-4538-9386-eb1f2ab3f2d1  False          512c83c1-15db-4271-aeac-fc231f63c9f5  FILE    ENCRYPT_PLAIN_TEXT     432      0      0  0.00 B  In Process          In Process          In Process         In Process         In Process           False          0.00 B
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `preallocate` | inode 文件是否预分配。 |
| `volume` | 分配的存储卷 ID。 |
| `type` | `FILE` 或 `DIR`。 |
| `Encrypt Method` | 文件的数据加密算法。 |
| `mode` | 文件权限。 |
| `uid` | 用户 ID。 |
| `gid` | 组 ID。 |
| `perf unique size` | 独占的性能层空间大小。 |
| `perf shared size` | 和其他对象共享的性能层空间大小。 |
| `cap unique size` | 独占的容量层空间大小。 |
| `cap shared size` | 和其他对象共享的容量层空间大小。 |
| `logical used size` | 已经分配的逻辑空间大小。 |
| `prioritized` | 是否要将数据都维持在性能层中。 |
| `downgraded_prs` | 尚未提升到性能层的空间大小。 |

### 查看 inode 信息

**操作方法**

- **通过 inode ID 查看 inode 信息**

  在集群任一节点执行如下命令：

  `zbs-nfs inode show <inode_id>`
- **通过 parent ID 和 inode 名称查看 inode 信息**

  在集群任一节点执行如下命令：

  `zbs-nfs inode lookup <parent_id> <inode_name>`

**输出示例**

```
-----------------  ------------------------------------
id                 512c83c1-15db-4271
name               nfs1
pool               ea479340-5d9d-4538-9386-eb1f2ab3f2d1
preallocate        False
volume             512c83c1-15db-4271-aeac-fc231f63c9f5
type               FILE
Encrypt Method     ENCRYPT_PLAIN_TEXT
mode               432
uid                0
gid                0
size               0.00 B
perf unique size   In Process
perf shared size   In Process
cap unique size    In Process
cap shared size    In Process
logical used size  In Process
prioritized        False
downgraded_prs     0.00 B
-----------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `preallocate` | 是否预分配。 |
| `volume` | 分配的存储卷 ID。 |
| `type` | `FILE` 或 `DIR`。 |
| `Encrypt Method` | 文件的数据加密算法。 |
| `mode` | 文件权限。 |
| `uid` | 用户 ID。 |
| `gid` | 组 ID。 |
| `perf unique size` | 独占的性能层空间大小。 |
| `perf shared size` | 和其他对象共享的性能层空间大小。 |
| `cap unique size` | 独占的容量层空间大小。 |
| `cap shared size` | 和其他对象共享的容量层空间大小。 |
| `logical used size` | 已经分配的逻辑空间大小。 |
| `prioritized` | 是否要将数据都维持在性能层中。 |
| `downgraded_prs` | 尚未提升到性能层的空间大小。 |

### 查看 inode 文件大小

**操作方法**

在集群任一节点执行如下命令：

`zbs-nfs inode sizeinfo <inode_id>`

**输出示例**

```
-----------  ----------
size                  6
volume size  1073741824
-----------  ----------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `size` | inode 文件大小。 |
| `volume size` | 存储卷大小。 |

### 查看 inode 属性

**操作方法**

在集群任一节点执行如下命令：

`zbs-nfs inode getattr <inode_id>`

**输出示例**

```
----  ----
type     2
mode   511
uid      0
gid      0
size  4096
----  ----
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `type` | inode 的文件类型。1 到 7 分别为 `FILE`, `DIR`, `BLK`, `CHR`, `LNK`, `SOCK`, `FIFO`。 |
| `mode` | inode 的文件模式。 |
| `uid` | 用户 ID。 |
| `gid` | 组 ID。 |
| `size` | 文件大小。 |

## 更新 inode 属性

**操作方法**

在集群任一节点执行如下命令，更新 inode 属性：

`zbs-nfs inode setattr <inode_id> [--mode <MODE>] [--uid <UID>] [--gid <GID>] [--size <SIZE>]`

| 参数 | 说明 |
| --- | --- |
| `--mode <MODE>` | 文件模式。 |
| `--uid <UID>` | 用户 ID。 |
| `--gid <GID>` | 组 ID。 |
| `--size <SIZE>` | 文件大小。 |

**输出示例**

```
-----------------  ------------------------------------
id                 7bbed56f-e5f0-4532
name               nfs1
pool               f6722181-7eb8-4ab4-ac39-7a06d29f6890
preallocate        False
volume             7bbed56f-e5f0-4532-9224-1d7ea5ca6c8f
type               FILE
Encrypt Method     ENCRYPT_PLAIN_TEXT
mode               432
uid                0
gid                0
size               16.00 B
perf unique size   In Process
perf shared size   In Process
cap unique size    In Process
cap shared size    In Process
logical used size  In Process
prioritized        False
downgraded_prs     0.00 B
-----------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `preallocate` | 是否预分配。 |
| `volume` | 分配的存储卷 ID。 |
| `type` | `FILE` 或 `DIR`。 |
| `Encrypt Method` | 文件的数据加密算法。 |
| `mode` | 文件权限。 |
| `uid` | 用户 ID。 |
| `gid` | 组 ID。 |
| `perf unique size` | 独占的性能层空间大小。 |
| `perf shared size` | 和其他对象共享的性能层空间大小。 |
| `cap unique size` | 独占的容量层空间大小。 |
| `cap shared size` | 和其他对象共享的容量层空间大小。 |
| `logical used size` | 已经分配的逻辑空间大小。 |
| `prioritized` | 是否要将数据都维持在性能层中。 |
| `downgraded_prs` | 尚未提升到性能层的空间大小。 |

## 重命名 inode

**操作方法**

在集群任一节点执行如下命令：

`zbs-nfs inode rename <src_parent_id> <src_inode_name> <dst_parent_id> <dst_inode_name>`

将 inode 从 `src_parent_id` 文件夹移动到 `dst_parent_id`，当 `dst_parent_id` 和 `src_parent_id` 相同时，即为对 inode 重命名。

**使用示例**

```
zbs-nfs inode rename 8be8661e-ef17-4a74 inode2 8be8661e-ef17-4a74 inode1
```

**输出示例**

```
-----------------  ------------------------------------
id                 7bbed56f-e5f0-4532
name               inode1
pool               f6722181-7eb8-4ab4-ac39-7a06d29f6890
preallocate        False
volume             7bbed56f-e5f0-4532-9224-1d7ea5ca6c8f
type               FILE
Encrypt Method     ENCRYPT_PLAIN_TEXT
mode               432
uid                0
gid                0
size               16.00 B
perf unique size   In Process
perf shared size   In Process
cap unique size    In Process
cap shared size    In Process
logical used size  In Process
prioritized        False
downgraded_prs     0.00 B
-----------------  ------------------------------------
```

## 更新 file 类型的 inode 文件大小

**操作方法**

在集群任一节点执行如下命令，更改 file 类型的 inode 文件大小：

`zbs-nfs inode truncate <file_id> <size>`

**输出示例**

```
-----------------  ------------------------------------
id                 7bbed56f-e5f0-4532
name               inode1
pool               f6722181-7eb8-4ab4-ac39-7a06d29f6890
preallocate        False
volume             7bbed56f-e5f0-4532-9224-1d7ea5ca6c8f
type               FILE
Encrypt Method     ENCRYPT_PLAIN_TEXT
mode               432
uid                0
gid                0
size               512.00 B
perf unique size   In Process
perf shared size   In Process
cap unique size    In Process
cap shared size    In Process
logical used size  In Process
prioritized        False
downgraded_prs     0.00 B
-----------------  ------------------------------------
```

## 删除指定路径下 inode

**操作方法**

在集群任一节点执行如下命令，删除 `<parent_id>` 目录下的名为 `<inode_name>` 的inode：

`zbs-nfs inode delete <parent_id> <inode_name> [--recursive {true|false}]`

其中，`--recursive {true|false}` 表示是否递归删除 inode 下的所有文件或文件夹。

**输出说明**

执行成功无输出。

---

## 管理 NFS 存储服务 > 管理 NFS 文件

# 管理 NFS 文件

## 创建 NFS 文件

**操作方法**

在集群任一节点执行如下命令，创建 NFS 文件：

`zbs-nfs file create <parent_id> <name>`

**输出示例**

```
-----------------  ------------------------------------
id                 fe4daff8-9cd3-494e
name               nfs4
pool               f6722181-7eb8-4ab4-ac39-7a06d29f6890
preallocate        False
volume             fe4daff8-9cd3-494e-8d22-bd5a4af2e54d
type               FILE
Encrypt Method     ENCRYPT_PLAIN_TEXT
mode               432
uid                0
gid                0
size               0.00 B
perf unique size   In Process
perf shared size   In Process
cap unique size    In Process
cap shared size    In Process
logical used size  In Process
prioritized        False
downgraded_prs     0.00 B
-----------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `preallocate` | 是否预分配。 |
| `volume` | 分配的存储卷 ID。 |
| `type` | `FILE` 或 `DIR`。 |
| `Encrypt Method` | 文件的数据加密算法。 |
| `mode` | 文件权限。 |
| `uid` | 用户 ID。 |
| `gid` | 组 ID。 |
| `size` | 文件大小。 |
| `perf unique size` | 独占的性能层空间大小。 |
| `perf shared size` | 和其他对象共享的性能层空间大小。 |
| `cap unique size` | 独占的容量层空间大小。 |
| `cap shared size` | 和其他对象共享的容量层空间大小。 |
| `logical used size` | 已经分配的逻辑空间大小。 |
| `prioritized` | 是否要将数据都维持在性能层中。 |
| `downgraded_prs` | 尚未提升到性能层的空间大小。 |

## 克隆 NFS 文件

**操作方法**

在集群任一节点执行如下命令：

`zbs-nfs file clone <src_export_name> <src_path> <dst_export_name> <dst_path>`

**输出示例**

```
----------- -----------
id 6
name test1_clone
pool 7
preallocate False
volume 5
type 1
mode 420
uid 0
gid 0
size 2
----------- -----------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `preallocate` | 文件是否预分配。 |
| `volume` | 文件分配的存储卷 ID。 |
| `type` | 文件的类型。 |
| `mode` | 文件权限。 |
| `uid` | 用户 ID。 |
| `gid` | 组 ID。 |
| `size` | 文件大小。 |

## 提升 NFS 文件副本数

**操作方法**

在集群任一节点节点执行如下命令：

`zbs-nfs file update [--replica_num REPLICA_NUM] <inode_id>`

| 参数 | 说明 |
| --- | --- |
| `--replica_num REPLICA_NUM` | 可选参数，重新设置副本数。仅支持提高副本数，不支持降低副本数。 |
| `inode_id` | inode ID。 |

**输出说明**

执行成功无输出。

## 将 NFS 文件转换为 iSCSI LUN

**操作方法**

在集群节点执行如下命令：

`zbs-iscsi lun convert_from_nfs <target_name> <lun_id> <inode_path> [--lun_name <LUN_NAME>][--replica_num <REPLICA_NUM>][--thin_provision {true|false}] [--desc <DESC>] [--stripe_num <STRIPE_NUM>][--stripe_size <STRIPE_SIZE>]`

| 参数 | 说明 |
| --- | --- |
| `target_name` | LUN 所属的 target 名称。 |
| `lun_id` | LUN ID。 |
| `inode_path` | inode 路径 |
| `--lun_name <LUN_NAME>` | 设置 LUN 名称。 |
| `--replica_num <REPLICA_NUM>` | 设置 LUN 副本数。 |
| `--thin_provision {true｜false}` | 设置 LUN 是否为精简置备。 |
| `--desc <DESC>` | LUN 描述。 |
| `--stripe_num <STRIPE_NUM>` | LUN 条带数。 |
| `--stripe_size <STRIPE_SIZE>` | LUN 条带大小。 |

**输出示例**

```
------------------  ------------------------------------
LUN Id              123
LUN Name            585db8a9-3054-4ca9-b93c-aa54ed4be3d3
Size                1024.00 MiB
Unique Size         In Process
Shared Size         In Process
Volume id           1664e191-c804-4911-98f5-4473ea3f0917
Replica Num         2
Creation Time       2022-11-22 19:46:28.676330094
Description
NAA                 3394d408ed191e466
Allowed Initiators  */*
Single Access       False
PR                  Details
Prefer CID          Unknown
------------------  ------------------------------------
```

---

## 管理 NFS 存储服务 > 管理 NFS 文件快照

# 管理 NFS 文件快照

当用户通过 NFS 形式来使用存储时，ZBS 提供对文件进行快照的功能，使用户可以对文件进行创建快照、从快照中回滚等操作。

## 创建 NFS 文件快照

**操作方法**

在集群任一节点执行如下命令，为指定目录下的文件创建一个指定名字的快照：

`zbs-nfs snapshot create <export_name> <file_path> <snapshot_name>`

| 参数 | 说明 |
| --- | --- |
| `export_name` | NFS Export 名称。 |
| `file_path` | 文件路径。 |
| `snapshot_name` | 快照名称。 |

**输出示例**

```
------------ -----------------------------
Snap Name test1_snap
Size 1024.00 MiB
Diff Size 256.00 MiB
Volume Id 4
Creation Time 2016-01-30 01:43:49.439047235
Description
------------ -----------------------------
```

## 查看 NFS 文件快照

**操作方法**

- 在集群任一节点执行如下命令，查看指定路径下某个 NFS 文件的快照。

`zbs-nfs snapshot list <export_name> [--path <PATH>]`

| 参数 | 说明 |
| --- | --- |
| `export_name` | NFS 文件所属的 NFS Exporter。 |
| `--path <PATH>` | NFS 文件路径。 |

- 在集群任一节点执行如下命令，查看指定 ID 的 NFS 文件快照：

`zbs-nfs snapshot show_by_id <snapshot_id>`

**输出示例**

```
ID Snap Name Size Unique Size Shared Size Diff Size Volume Id Creation Time Description

------------------------------------ ---------------------------------------------------------------- ------ ------------- ------------- ----------- ------------------------------------ ----------------------------- -------------

015638eb-e0f7-49b6-a223-c256e4cd9cf6 ddd-214627-2016-11-25-10-40 0.00 B 0.00 B 0.00 B 0.00 B 9bbe6391-4d4e-487c-a56d-82b8aa9dea1b 2016-11-25 18:40:36.730107938 test

0159b0c1-1d6e-4606-ac57-031f28324fc5 ddd-e7e9e134-dd70-473b-bef3-4ba95aa27af8-214627-2016-11-21-18-57 0.00 B 0.00 B 0.00 B 0.00 B 321e3929-c2bf-47a3-8307-76439eb31f0c 2016-11-22 02:57:22.932895298 test
```

## 更新 NFS 文件快照属性

用户可使用命令行更新快照的描述，以及设置数据是否均匀分布。

**操作方法**

- 在集群任一节点执行如下命令，对指定路径下某个 NFS 文件的快照进行更新：

  `zbs-nfs snapshot update <export_name> <file_path> <snapshot_name> <new_snapshot_name> [--new_desc <NEW_DESC>] [--new_alloc_even <NEW_ALLOC_EVEN>]`
- 在集群任一节点执行如下命令，对指定 ID 的 NFS 文件的快照进行更新：

  `zbs-nfs snapshot update_by_id <snapshot_id> <new_snapshot_name> [--new_desc <NEW_DESC>] [--new_alloc_even <NEW_ALLOC_EVEN>]`

| 参数 | 说明 |
| --- | --- |
| `--new_desc <NEW_DESC>` | 更新对相应快照的描述。 |
| `--new_alloc_even <NEW_ALLOC_EVEN>` | `NEW_ALLOC_EVEN` 取值为 `true` 或 `false`，分别表示是否设置数据均匀分布。 |

**输出说明**

执行成功无输出。

## 从 NFS 文件快照回滚

**操作方法**

- 在集群任一节点执行如下命令，将 NFS 文件从指定名称的快照进行回滚：

  `zbs-nfs snapshot rollback <export_name> <file_path> <snapshot_name>`
- 在集群任一节点执行如下命令，将 NFS 文件从指定 ID 的快照进行回滚：

  `zbs-nfs snapshot rollback_by_id <export_name> <file_path> <snapshot_id>`

**输出说明**

执行成功无输出。

## 删除 NFS 文件快照

**操作方法**

- 在集群任一节点执行如下命令，删除指定名称的快照：

  `zbs-nfs snapshot delete <export_name> <file_path> <snapshot_name>`
- 在集群任一节点执行如下命令，删除指定 ID 的快照：

  `zbs-nfs snapshot delete_by_id <snapshot_id>`

**输出示例**

```
ID Snap Name Size Unique Size Shared Size Diff Size Volume Id Creation Time Description
------------------------------------ ---------------------------------------------------------------- ------ ------------- ------------- ----------- ------------------------------------ ----------------------------- -------------
015638eb-e0f7-49b6-a223-c256e4cd9cf6 ddd-214627-2016-11-25-10-40 0.00 B 0.00 B 0.00 B 0.00 B 9bbe6391-4d4e-487c-a56d-82b8aa9dea1b 2016-11-25 18:40:36.730107938 test
[root@localhost test]# zbs-nfs snapshot delete smartx test1 ddd-214627-2016-11-25-10-40
[root@localhost test]# zbs-nfs snapshot list smartx test1
No snapshot found
```

---

## 管理 iSCSI 存储服务

# 管理 iSCSI 存储服务

SMTX OS 可通过 iSCSI 协议为第三方计算平台提供 iSCSI 块存储服务。本文档介绍了 iSCSI 块存储服务的相关命令。

---

## 管理 iSCSI 存储服务 > 管理 iSCSI target

# 管理 iSCSI target

iSCSI target 是 iSCSI initiator 访问的存储设备，用于响应 initiator 的存储访问请求。iSCSI target 可以提供一个或多个 LUN 供客户端使用。

## 查看所有的 iSCSI target

**操作方法**

在集群任一节点执行如下命令，查看集群的所有 iSCSI target。

`zbs-iscsi target list`

**输出示例**

```
ID                                    Name                                  IQN Name                                                            Creation Time                  Encrypt Method      Resiliency Type      Cap/Perf Segment   EC Param    Thin    Description    Storage Pool    Whitelist    IQN Whitelist                                                                                                                          External Use      Stripe Num    Stripe Size  Adaptive IQN Whitelist    Labels            Is Prioritized    Use Host    Allowed Host Ids                      Allowed Host Group Ids
------------------------------------  ------------------------------------  ------------------------------------------------------------------  -----------------------------  ------------------  -----------------  ----------  ----------  ------  -------------  --------------  -----------  -------------------------------------------------------------------------------------------------------------------------------------  --------------  ------------  -------------  ------------------------  ----------------  ----------------  ----------  ------------------------------------  ------------------------------------
114b6749-d902-43bc-8280-e3ad8b8f2451  test-not-select-host-and-group        iqn.2016-02.com.smartx:system:test-not-select-host-and-group        2025-07-02 11:47:23.323384547  ENCRYPT_PLAIN_TEXT  RT_REPLICA                   (3, 3)               True                   system                                                                                                                                                              True                       8         262144  False                     []                False             True
17d46e36-bee2-45ab-8f20-a1611eb55353  test-by-manual-and-iqn-allban         iqn.2016-02.com.smartx:system:test-by-manual-and-iqn-allban         2025-07-02 11:49:36.805802270  ENCRYPT_PLAIN_TEXT  RT_REPLICA                   (3, 3)               True                   system          */*                                                                                                                                                 True                       8         262144  False                     []                False             False
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `IQN Name` | Target 的 IQN 名称。 |
| `Encrypt Method` | 存储卷的数据加密算法。 |
| `Resiliency Type` | 冗余模式。 |
| `Cap/Perf Segment Num` | 容量层/性能层的期望分片数。 |
| `EC Param` | EC 冗余模式下对应的 EC 参数。 |
| `IQN Whitelist` | IQN 白名单。 |
| `Stripe Num` | 条带数。 |
| `Stripe Size` | 条带大小。 |
| `Adaptive IQN Whitelist` | 是否采用自适应 IQN 白名单。 |
| `Labels` | 标签，用于在不指定 target 创建 LUN 时提供标签匹配功能。 |
| `Is Prioritized` | 是否要将数据都维持在性能层中。 |
| `Use Host` | 是否使用业务主机指定白名单。 |
| `Allowed Host Ids` | 关联的业务主机的 ID。 |
| `Allowed Host Group Ids` | 关联的业务主机组的 ID。 |

## 查看指定 iSCSI target 的基本信息和 CHAP 认证信息

**操作方法**

在集群任一节点执行如下命令，查看指定名称的 iSCSI target 的基本信息和 CHAP 认证信息：

`zbs-iscsi target show [--show_chap] <name>`

| 参数 | 说明 |
| --- | --- |
| `--show_chap` | 可选参数，显示该 iSCSI target 的 CHAP 认证信息。 |
| `name` | iSCSI target 名称。 |

**输出示例**

```
----------------------  -----------------------------------------
ID                      745c5404-2a5a-4c20-97d0-0a56fbeafdb6
Name                    target-chap
IQN Name                iqn.2016-02.com.smartx:system:target-chap
Creation Time           2025-07-04 18:17:24.24872660
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Cap/Perf Segment Num    (2, 2)
EC Param
Thin                    True
Description
Storage Pool            system
Whitelist               */*
IQN Whitelist           iqn.1994-05.com.redhat:5141c8ae99f1
External Use            True
Stripe Num              8
Stripe Size             262144
Adaptive IQN Whitelist  False
Labels                  [('ELF_PROTECTED', 'TRUE')]
Is Prioritized          False
Use Host                True
Allowed Host Ids        b8f9877c-995d-41fa-b18e-0fefe4b8250c
Allowed Host Group Ids
----------------------  -----------------------------------------
Target Chap Info
---------  ------------
Chap Name  test
Secret     123456123456
Enable     True
---------  ------------
Initiator Chap Info
IQN                                  Chap Name          Secret  Enable
-----------------------------------  -----------  ------------  --------
iqn.1994-05.com.redhat:5141c8ae99f1  test         123456789012  True
```

**输出说明**

- **iSCSI target 基本信息**

  | 参数 | 说明 |
  | --- | --- |
  | `ID` | Target ID |
  | `Name` | Target 名称。 |
  | `IQN Name` | IQN 名称。 |
  | `Resiliency Type` | 冗余模式。 |
  | `Encrypt Method` | 存储卷的数据加密算法。 |
  | `Cap/Perf Segment Num` | 容量层/性能层的期望分片数。 |
  | `EC Param` | EC 冗余模式下对应的 EC 参数。 |
  | `Thin` | Target 内新建 LUN 是否采用精简置备。 |
  | `Description` | Target 描述。 |
  | `Storage Pool` | Target 所属存储池。 |
  | `Whitelist` | 可访问该 target 的 IP 白名单。 |
  | `IQN Whitelist` | 可访问该 target 的 IQN 白名单。 |
  | `External Use` | `True` 或 `False`，表示 iSCSI target 是否用作外部接入。 |
  | `Stripe Num` | Target 内新建 LUN 的条带数。 |
  | `Stripe Size` | Target 内新建 LUN 的条带大小。 |
  | `Adaptive IQN Whitelist` | 是否开启了自适应 IQN 白名单。 |
  | `Labels` | Target 标签。 |
  | `Is Prioritized` | 是否要将数据都维持在性能层中。 |
  | `Use Host` | 是否使用业务主机指定白名单。 |
  | `Allowed Host Ids` | 关联的业务主机的 ID。 |
  | `Allowed Host Group Ids` | 关联的业务主机组的 ID。 |
- **CHAP 认证信息**

  - Target CHAP 认证信息

    | 参数 | 说明 |
    | --- | --- |
    | `Chap Name` | Target CHAP 认证名称。 |
    | `Secret` | Target CHAP 认证密码。 |
    | `Enable` | `True` 或 `False`，表示是否启用了 target CHAP 认证。 |
  - Initiator CHAP 认证信息

    | 参数 | 说明 |
    | --- | --- |
    | `IQN` | Initiator 的 IQN 名称。 |
    | `Chap Name` | Initiator CHAP 认证名称。 |
    | `Secret` | Initiator CHAP 认证密码。 |
    | `Enable` | `True` 或 `False`，表示是否启用了 initiator CHAP 认证。 |

## 创建 iSCSI target

**操作方法**

在集群任一节点执行如下命令，创建 iSCSI target，并设置 target 的名称、IQN、存储策略、CHAP 认证信息、I/O 限速等：

```
zbs-iscsi target create <name> [--desc <DESC>][--iqn_date <IQN_DATE>]
                               [--iqn_naming_auth <IQN_NAMING_AUTH>]
                               [--replica_num <REPLICA_NUM>]
                               [--thin_provision <THIN_PROVISION>]
                               [--storage_pool_id <STORAGE_POOL_ID>]
                               [--whitelist <WHITELIST>]
                               [--iqn_whitelist <IQN_WHITELIST>]
                               [--adaptive_iqn_whitelist <ADAPTIVE_IQN_WHITELIST>]
                               [--chap_name <CHAP_NAME>] [--secret <SECRET>]
                               [--external_use <EXTERNAL_USE>]
                               [--stripe_num <STRIPE_NUM>]
                               [--stripe_size <STRIPE_SIZE>]
                               [--iops IOPS] [--iops_rd <IOPS_RD>]
                               [--iops_wr IOPS_WR] [--iops_max <IOPS_MAX>]
                               [--iops_rd_max <IOPS_RD_MAX>]
                               [--iops_wr_max <IOPS_WR_MAX>]
                               [--iops_max_length <IOPS_MAX_LENGTH>]
                               [--iops_rd_max_length <IOPS_RD_MAX_LENGTH>]
                               [--iops_wr_max_length <IOPS_WR_MAX_LENGTH>]
                               [--iops_io_size <IOPS_IO_SIZE>] [--bps <BPS>]
                               [--bps_rd <BPS_RD>] [--bps_wr <BPS_WR>]
                               [--bps_max <BPS_MAX>] [--bps_rd_max <BPS_RD_MAX>]
                               [--bps_wr_max <BPS_WR_MAX>]
                               [--bps_max_length <BPS_MAX_LENGTH>]
                               [--bps_rd_max_length <BPS_RD_MAX_LENGTH>]
                               [--bps_wr_max_length <BPS_WR_MAX_LENGTH>]
                               [--resiliency_type <RESILIENCY_TYPE>]
                               [--ec_algo <EC_ALGO>] [--ec_k <EC_K>] [--ec_m <EC_M>]
                               [--encrypt_method <ENCRYPT_METHOD>]
                               [--driver_name <DRIVER_NAME>]
                               [--prioritized <PRIORITIZED>]
                               [--use_host <USE_HOST>]
                               [--allowed_host_ids <ALLOWED_HOST_IDS>]
                               [--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>]
```

| 参数 | 说明 |
| --- | --- |
| `name` | 设置 Target 名称，允许输入字母、数字以及特殊符号 `-`、`.`。iSCSI Target 的名称不区分大小写，不论以大写还是小写输入，都将统一转换为小写格式。 |
| `--desc <DESC>` | 设置 Target 描述。 |
| `--iqn_date <IQN_DATE>` | 用于生成 Target 的 IQN，必须为 `yyyy-mm` 格式。默认为 `2016-02`。 |
| `--iqn_naming_auth <IQN_NAMING_AUTH>` | 指定 Naming Auth，用于生成 Target IQN。格式为 `com.公司名`，默认为 `com.smartx`。允许输入字母、数字以及特殊符号 `-`、`.`，但不允许以 `-` 开头或结尾。 |
| `--replica_num <REPLICA_NUM>` | 设置 Target 内新建 LUN 的默认副本数，可设置为 2 副本或 3 副本，默认 `None`。 |
| `--thin_provision <THIN_PROVISION>` | 设置 Target 新建 LUN 的置备方式是否为精简置备，可设置为`True` 或 `False`。 |
| `--storage_pool_id <STORAGE_POOL_ID>` | 选择 Target 所属的存储池。 |
| `--whitelist <WHITELIST>` | 设置 iSCSI Target 的 IP 白名单，可输入 IP 地址或 CIDR 块。`*/*` 表示任何 IP 都可以访问此 Target。 |
| `--iqn_whitelist <IQN_WHITELIST>` | 设置 iSCSI Target 的 IQN 白名单，多个 IQN 之间以英文逗号 `,` 分隔。 |
| `--adaptive_iqn_whitelist <ADAPTIVE_IQN_WHITELIST>` | 设置是否启用 IQN 白名单自适应功能，可设置为`True` 或 `False`。开启后，IQN 白名单会自动保持为所包含 LUN 的 IQN 白名单的并集。开启自适应功能时，不应同时设置 `--iqn_whitelist` 参数。 |
| `--chap_name <CHAP_NAME>` | 创建 target CHAP 认证名称。允许输入长度为 1 ~ 223 的字母、数字，以及特殊符号 `.`、`-`、`:`。 |
| `--secret <SECRET>` | 指定 target CHAP 认证密码。允许输入长度 12 ~ 16 的字母和数字。 |
| `--external_use <EXTERNAL_USE>` | `true` 或 `false`，表示 target 是否用作外部接入。 |
| `--stripe_num <STRIPE_NUM>` | Target 新建 LUN 的条带数。 |
| `--stripe_size <STRIPE_SIZE>` | Target 新建 LUN 的条带大小。 |
| `--iops <IOPS>` | 设置 target 内新建 LUN 的总 IOPS 上限值。 |
| `--iops_rd <IOPS_RD>` | 设置读 IOPS 的上限值。 |
| `--iops_wr <IOPS_WR>` | 设置写 IOPS 的上限值。 |
| `--iops_max <IOPS_MAX>` | 设置总 IOPS 突发的上限值。 |
| `--iops_rd_max <IOPS_RD_MAX>` | 设置读 IOPS 突发的上限值。 |
| `--iops_wr_max <IOPS_WR_MAX>` | 设置写 IOPS 突发的上限值。 |
| `--iops_max_length <IOPS_MAX_LENGTH>` | 设置总 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_rd_max_length <IOPS_RD_MAX_LENGTH>` | 设置读 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_wr_max_length <IOPS_WR_MAX_LENGTH>` | 设置写 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_io_size <IOPS_IO_SIZE>` | 使用 IOPS 限速时，假定的平均 I/O 数据量大小。 |
| `--bps <BPS>` | 设置 target 内新建 LUN 的总带宽限制，单位为 Bps。 |
| `--bps_rd <BPS_RD>` | 设置读带宽的上限值。 |
| `--bps_wr <BPS_WR>` | 设置写带宽的上限值。 |
| `--bps_max <BPS_MAX>` | 设置总带宽在发生 I/O 突发时的上限值。 |
| `--bps_rd_max <BPS_RD_MAX>` | 设置读带宽在发生 I/O 突发时的上限值。 |
| `--bps_wr_max <BPS_WR_MAX>` | 设置写带宽在发生 I/O 突发时的上限值。 |
| `--bps_max_length <BPS_MAX_LENGTH>` | 设置在发生 I/O 突发时，以总带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_rd_max_length <BPS_RD_MAX_LENGTH>` | 设置在发生 I/O 突发时，以读带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_wr_max_length <BPS_WR_MAX_LENGTH>` | 设置在发生 I/O 突发时，以写带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--resiliency_type <RESILIENCY_TYPE>` | 设置冗余模式，副本或 EC，默认为 `None`。 |
| `--ec_algo <EC_ALGO>` | 设置 EC 算法，当冗余模式为 EC 时必须设置，默认为 `RS`。 |
| `--ec_k <EC_K>` | 设置 EC 算法参数 K，参数范围为 [2，23]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--ec_m <EC_M>` | 设置 EC 算法参数 M，参数范围为 [1，4]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--encrypt_method <ENCRYPT_METHOD>` | 设置数据加密方法，默认为不加密 。 |
| `--driver_name <DRIVER_NAME>` | 设置驱动名称，`iscsi` 或 `iser`，默认为 `None`。 |
| `--prioritized <PRIORITIZED>` | 设置在 target 内创建 LUN 时是否默认开启常驻缓存，可设置为 `True` 或 `False`。 |
| `--use_host <USE_HOST>` | 设置是否使用业务主机指定白名单。use\_host 为 `true` 时，不允许设置 `whitelist` 和 `iqn_whitelist` 参数；为 `false` 时，不允许设置 `allowed_host_ids` 和 `allowed_host_group_ids` 参数。 |
| `--allowed_host_ids <ALLOWED_HOST_IDS>` | 设置关联的业务主机的 ID，以英文逗号（,）分隔多个 ID。 |
| `--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>` | 设置关联的业务主机组的 ID，以英文逗号（,）分隔多个 ID。 |

**输出示例**

```
----------------------  ------------------------------------
ID                      07dfebb7-d05f-44d3-b06a-b2289a2d7418
Name                    t1
IQN Name                iqn.2016-02.com.smartx:system:t1
Creation Time           2025-07-07 09:38:03.381779382
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Replica#                2
EC Param
Thin                    True
Description
Storage Pool            system
Whitelist               */*
IQN Whitelist           */*
External Use            False
Stripe Num              8
Stripe Size             262144
Adaptive IQN Whitelist  False
Labels                  []
Is Prioritized          False
Use Host                False
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 更新 iSCSI target

**操作方法**

在集群任一节点执行如下命令，更新 iSCSI target：

```
zbs-iscsi target update <name> [--new_name <NEW_NAME>][--desc <DESC>]
                               [--iqn_date <IQN_DATE>]
                               [--iqn_naming_auth <IQN_NAMING_AUTH>]
                               [--replica_num <REPLICA_NUM>]
                               [--thin_provision <THIN_PROVISION>]
                               [--whitelist <WHITELIST>]
                               [--iqn_whitelist <IQN_WHITELIST>]
                               [--adaptive_iqn_whitelist <ADAPTIVE_IQN_WHITELIST>]
                               [--external_use <EXTERNAL_USE>]
                               [--stripe_num <STRIPE_NUM>]
                               [--stripe_size <STRIPE_SIZE>]
                               [--enable_target_chap <ENABLE_TARGET_CHAP>]
                               [--remove_target_chap <REMOVE_TARGET_CHAP>]
                               [--target_chap_name <TARGET_CHAP_NAME>]
                               [--target_secret <TARGET_SECRET>]
                               [--iops IOPS] [--iops_rd <IOPS_RD>]
                               [--iops_wr IOPS_WR] [--iops_max <IOPS_MAX>]
                               [--iops_rd_max <IOPS_RD_MAX>]
                               [--iops_wr_max <IOPS_WR_MAX>]
                               [--iops_max_length <IOPS_MAX_LENGTH>]
                               [--iops_rd_max_length <IOPS_RD_MAX_LENGTH>]
                               [--iops_wr_max_length <IOPS_WR_MAX_LENGTH>]
                               [--iops_io_size <IOPS_IO_SIZE>] [--bps <BPS>]
                               [--bps_rd <BPS_RD>] [--bps_wr <BPS_WR>]
                               [--bps_max <BPS_MAX>] [--bps_rd_max <BPS_RD_MAX>]
                               [--bps_wr_max <BPS_WR_MAX>]
                               [--bps_max_length <BPS_MAX_LENGTH>]
                               [--bps_rd_max_length <BPS_RD_MAX_LENGTH>]
                               [--bps_wr_max_length <BPS_WR_MAX_LENGTH>]
                               [--resiliency_type <RESILIENCY_TYPE>]
                               [--ec_algo <EC_ALGO>] [--ec_k <EC_K>] [--ec_m <EC_M>]
                               [--recursive] [--prioritized <PRIORITIZED>]
                               [--use_host <USE_HOST>]
                               [--allowed_host_ids <ALLOWED_HOST_IDS>]
                               [--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>]
```

| 参数 | 说明 |
| --- | --- |
| `name` | 待更新 target 的名称。 |
| `--new_name <NEW_NAME>` | 重新命名 target，允许输入字母、数字以及特殊符号 `-`、`.`。iSCSI target 的名称不区分大小写，不论以大写还是小写输入，都将统一转换为小写格式。 |
| `--desc <DESC>` | 更新 target 描述。 |
| `--iqn_date <IQN_DATE>` | 更新用于生成 target 的 IQN，必须为 `yyyy-mm` 格式。默认为 `2016-02`。 |
| `--iqn_naming_auth <IQN_NAMING_AUTH>` | 更新 Naming Auth，用于生成 target IQN。格式为 `com.公司名`，默认为 `com.smartx`。允许输入字母、数字以及特殊符号 `-`、`.`，但不允许以 `-` 开头或结尾。 |
| `--replica_num <REPLICA_NUM>` | 更新 target 内新建 LUN 的默认副本数，副本数只支持由 2 副本提升至 3 副本。 |
| `--thin_provision <THIN_PROVISION>` | `True` 或 `False`，表示是否设置 target 新建 LUN 的置备方式为精简置备。 |
| `--storage_pool_id <STORAGE_POOL_ID>` | 更新 target 所属的存储池。 |
| `--whitelist <WHITELIST>` | 更新 iSCSI target 的 IP 白名单，可输入 IP 地址或 CIDR 块。`*/*` 表示任何 IP 都可以访问此 target。 |
| `--iqn_whitelist <IQN_WHITELIST>` | 更新 iSCSI target 的 IQN 白名单，多个 IQN 之间以英文逗号 `,` 分隔。 |
| `--adaptive_iqn_whitelist <ADAPTIVE_IQN_WHITELIST>` | `True` 或 `False`，表示是否启用 IQN 白名单自适应功能。开启后，IQN 白名单会自动保持为所包含 LUN 的 IQN 白名单的并集。开启自适应功能时，不应同时设置 `--iqn_whitelist` 参数。 |
| `--external_use <EXTERNAL_USE>` | `True` 或 `False`，表示 target 是否用作外部接入。 |
| `--stripe_num <STRIPE_NUM>` | 更新 target 新建 LUN 的条带数。 |
| `--stripe_size <STRIPE_SIZE>` | 更新 target 新建 LUN 的条带大小。 |
| `--enable_target_chap <ENABLE_TARGET_CHAP>` | `True` 或 `False`，开启或关闭 target CHAP 认证。 |
| `--remove_target_chap <REMOVE_TARGET_CHAP>` | 移除 target CHAP 认证信息。 |
| `--target_chap_name <TARGET_CHAP_NAMEE>` | 更新 target CHAP 认证名称。允许输入长度为 1 ~ 223 的字母、数字，以及特殊符号 `.`、`-`、`:`。 |
| `--target_secret <TARGET_SECRET>` | 更新 target CHAP 认证密码。允许输入长度 12 ~ 16 的字母和数字。 |
| `--iops <IOPS>` | 更新 target 内新建 LUN 的总 IOPS 上限值。 |
| `--iops_rd <IOPS_RD>` | 更新读 IOPS 的上限值。 |
| `--iops_wr <IOPS_WR>` | 更新写 IOPS 的上限值。 |
| `--iops_max <IOPS_MAX>` | 更新总 IOPS 突发的上限值。 |
| `--iops_rd_max <IOPS_RD_MAX>` | 更新读 IOPS 突发的上限值。 |
| `--iops_wr_max <IOPS_WR_MAX>` | 更新写 IOPS 突发的上限值。 |
| `--iops_max_length <IOPS_MAX_LENGTH>` | 更新总 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_rd_max_length <IOPS_RD_MAX_LENGTH>` | 更新读 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_wr_max_length <IOPS_WR_MAX_LENGTH>` | 更新写 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_io_size <IOPS_IO_SIZE>` | 更新使用 IOPS 限速时假定的平均 I/O 数据量大小。 |
| `--bps <BPS>` | 更新 target 内新建 LUN 的总带宽限制，单位为 Bps。 |
| `--bps_rd <BPS_RD>` | 更新读带宽的上限值。 |
| `--bps_wr <BPS_WR>` | 更新写带宽的上限值。 |
| `--bps_max <BPS_MAX>` | 更新总带宽在发生 I/O 突发时的上限值。 |
| `--bps_rd_max <BPS_RD_MAX>` | 更新读带宽在发生 I/O 突发时的上限值。 |
| `--bps_wr_max <BPS_WR_MAX>` | 更新写带宽在发生 I/O 突发时的上限值。 |
| `--bps_max_length <BPS_MAX_LENGTH>` | 更新在发生 I/O 突发时，以总带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_rd_max_length <BPS_RD_MAX_LENGTH>` | 更新在发生 I/O 突发时，以读带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_wr_max_length <BPS_WR_MAX_LENGTH>` | 更新在发生 I/O 突发时，以写带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--resiliency_type <RESILIENCY_TYPE>` | 更新冗余模式，副本或 EC，默认为 `None`。 |
| `--ec_algo <EC_ALGO>` | 更新 EC 算法，当冗余模式为 EC 时必须设置，默认为 `RS`。 |
| `--ec_k <EC_K>` | 更新 EC 算法参数 K，参数范围为 [2，23]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--ec_m <EC_M>` | 更新 EC 算法参数 M，参数范围为 [1，4]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--encrypt_method <ENCRYPT_METHOD>` | 设置数据加密方法，默认为不加密 。 |
| `--recursive` | 递归地更新 target 内的所有 LUN 的副本数至较大或相等的副本数，默认为 `False`。 |
| `--prioritized <PRIORITIZED>` | 更新在 target 内创建 LUN 时是否默认开启常驻缓存的设置，可设置为 `True` 或 `False`。 |
| `--use_host <USE_HOST>` | 更新是否使用业务主机指定白名单。use\_host 为 `true` 时，不允许设置 `whitelist` 和 `iqn_whitelist` 参数；为 `false` 时，不允许设置 `allowed_host_ids` 和 `allowed_host_group_ids` 参数。 |
| `--allowed_host_ids <ALLOWED_HOST_IDS>` | 更新关联的业务主机的 ID，以英文逗号（,）分隔多个 ID。 |
| `--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>` | 更新关联的业务主机组的 ID，以英文逗号（,）分隔多个 ID。 |

**输出示例**

```
----------------------  ------------------------------------
ID                      07dfebb7-d05f-44d3-b06a-b2289a2d7418
Name                    t1
IQN Name                iqn.2016-02.com.smartx:system:t1
Creation Time           2025-07-07 09:38:03.381779382
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Replica#                2
EC Param
Thin                    True
Description
Storage Pool            system
Whitelist
IQN Whitelist
External Use            False
Stripe Num              8
Stripe Size             262144
Adaptive IQN Whitelist  False
Labels                  []
Is Prioritized          False
Use Host                True
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 删除 iSCSI target

**操作方法**

在集群任一节点执行如下命令，删除指定的 iSCSI target：

`zbs-iscsi target delete <name> [--recursive {true | false}]`

| 参数 | 说明 |
| --- | --- |
| `name` | 待删除 target 名称。 |
| `--recursive` | `True` 或 `False`，是否清空 target 内的所有 LUN，默认为 `None`（等效于否）。 |

**输出说明**

执行成功无输出。

## 设置 initiator CHAP 认证

设置客户端对 iSCSI target 的认证

**操作方法**

在集群任一节点执行如下命令，设置 initiator 认证：

`zbs-iscsi initiator_chap create <name> <iqn> <chap_name> <chap_password> {true|false}`

| 参数 | 说明 |
| --- | --- |
| `name` | Target 名称。 |
| `iqn` | Initiator IQN 名称。 |
| `chap_name` | Initiator CHAP 认证名称。允许输入长度为 1 ~ 512 的字母、数字，以及 `.`、`-`、`:`。 |
| `chap_password` | Initiator CHAP 认证密码。允许输入长度 12 ~ 512 的字母和数字。 |
| `true` 或 `false` | 是否开启 initiator 认证。 |

**输出示例**

```
[root@zbs17-73 11:45:52 ~]$zbs-iscsi initiator_chap create t2 iqn.2016-02.com.smartx:system:tttt admin1234 admin12345678 True
----------------------  ------------------------------------
ID                      0d07024b-1d62-49ae-afab-da06cd9f7ce2
Name                    t2
IQN Name                iqn.2016-02.com.smartx:system:t2
Creation Time           2024-06-18 11:07:42.615775691
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Replica#                2
EC Param
Thin                    True
Description
Storage Pool            system
Whitelist               */*
IQN Whitelist           */*
External Use            False
Stripe Num              8
Stripe Size             262144
Adaptive IQN Whitelist  False
Labels                  []
Is Prioritized          False
Use Host                False
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 更新 initiator CHAP 认证设置

**操作方法**

在集群任一节点执行如下命令，更新 initiator CHAP 认证设置：

`zbs-iscsi initiator_chap update <name> <iqn> <chap_name> <chap_password> {true|false}`

| 参数 | 说明 |
| --- | --- |
| `name` | Target 名称。 |
| `iqn` | Initiator IQN 名称。 |
| `chap_name` | Initiator CHAP 认证名称。允许输入长度为 1 ~ 512 的字母、数字，以及 `.`、`-`、`:`。 |
| `chap_password` | Initiator CHAP 认证密码。允许输入长度 12 ~ 512 的字母和数字。 |
| `true` 或 `false` | 是否开启 initiator 认证。 |

**输出示例**

```
[root@zbs17-73 13:39:24 ~]$zbs-iscsi initiator_chap update t2 iqn.2016-02.com.smartx:system:tttt admin1234 admin12345678 True
----------------------  ------------------------------------
ID                      0d07024b-1d62-49ae-afab-da06cd9f7ce2
Name                    t2
IQN Name                iqn.2016-02.com.smartx:system:t2
Creation Time           2024-06-18 11:07:42.615775691
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Replica#                2
EC Param
Thin                    True
Description
Storage Pool            system
Whitelist               */*
IQN Whitelist           */*
External Use            False
Stripe Num              8
Stripe Size             262144
Adaptive IQN Whitelist  False
Labels                  []
Is Prioritized          False
Use Host                False
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 关闭 initiator CHAP 认证

**操作方法**

在集群任一节点执行如下命令，关闭 initiator CHAP 认证：

`zbs-iscsi initiator_chap remove <name> <iqn>`

**输出示例**

```
[root@scvm31 12:44:34 ~]$zbs-iscsi initiator_chap remove fl-iscsi-chap iqn.2016-02.com.smartx:system:fl-iscsi-chap
------------- -------------------------------------------
ID c640ae8b-5d78-47fc-8018-54dbc061ca99
Name fl-iscsi-chap
IQN Name iqn.2016-02.com.smartx:system:fl-iscsi-chap
Creation Time 2019-03-21 12:31:19.373503032
Replica# 2
Thin True
Description
Storage Pool system
Whitelist */*
IQN Whitelist */*
External Use False
------------- -------------------------------------------
```

## 更新 Target CHAP 认证

更新 iSCSI target CHAP 的认证。

**操作方法**

在集群任一节点执行如下命令：

`zbs-iscsi target update [--enable_target_chap <ENABLE_TARGET_CHAP>] [--target_chap_name <TARGET_CHAP_NAME>] [--target_secret <TARGET_SECRET>] [--remove_target_chap <REMOVE_TARGET_CHAP>] <name>`

| 参数 | 说明 |
| --- | --- |
| `--enable_target_chap <ENABLE_TARGET_CHAP>` | `True` 或 `False`，选择开启或关闭 target CHAP 认证。 |
| `--target_chap_name <TARGET_CHAP_NAME>` | Target CHAP 认证用户名。允许输入长度为 1 ~ 223 的字母、数字，以及特殊字符 `.`、`-`、`:`。 |
| `--target_secret <TARGET_SECRET>` | Target CHAP 认证密码。允许输入长度 12 ~ 16 的字母和数字。 |
| `--remove_target_chap <REMOVE_TARGET_CHAP>` | 删除 target CHAP 信息，默认为 `None`。 |
| `name` | iSCSI target 名称。 |

**输出示例**

```
[root@scvm31 12:40:57 ~]$zbs-iscsi target update --enable_target_chap true --target_chap_name xxx2 --target_secret abc123456789 t2
----------------------  ------------------------------------
ID                      0d07024b-1d62-49ae-afab-da06cd9f7ce2
Name                    t2
IQN Name                iqn.2016-02.com.smartx:system:t2
Creation Time           2024-06-18 11:07:42.615775691
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Replica#                2
EC Param
Thin                    True
Description
Storage Pool            system
Whitelist               */*
IQN Whitelist           */*
External Use            False
Stripe Num              8
Stripe Size             262144
Adaptive IQN Whitelist  False
Labels                  []
Is Prioritized          False
Use Host                False
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

---

## 管理 iSCSI 存储服务 > 管理 iSCSI LUN

# 管理 iSCSI LUN

## 查看 iSCSI LUN 信息

介绍通过不同的方式来查看 iSCSI LUN 信息。

**操作方法**

- **查看指定 ID 的 iSCSI LUN**

  在集群任一节点执行如下命令：

  `zbs-iscsi lun show [--all] <target_name> <lun_id>`
- **查看指定名称的 iSCSI LUN**

  在集群任一节点执行如下命令：

  `zbs-iscsi lun show_by_name <target_name> <lun_name>`
- **查看指定 UUID 的 iSCSI LUN**

  在集群任一节点执行如下命令：

  `zbs-iscsi lun show_target_and_lun_by_uuid <lun_uuid>`
- **查看指定 secondary ID 的 iSCSI LUN**

  在集群任一节点执行如下命令：

  `zbs-iscsi lun show_target_and_lun_by_secondary_id <secondary_id>`
- **查看某个 iSCSI target 下所有的 LUN**

  在集群任一节点执行如下命令：

  `zbs-iscsi lun list <target_name>`

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `[--all]` | 可选参数，显示 LUN 的所有参数。 |
| `<target_name>` | 必选参数，LUN 所属的 target 名称。 |
| `<lun_id>` | 必选参数，待查看的 LUN 的 ID。 |
| `<lun_name>` | 必选参数，待查看的 LUN 的名称。 |
| `<lun_uuid>` | 必选参数，待查看的 LUN 的存储卷 ID。 |
| `<secondary_id>` | 必选参数，待查看的 LUN 的 secondary ID。 |

**输出示例**

```
----------------------  ------------------------------------
LUN Id                  1
LUN Name                260246de-86f6-4c56-ba82-f409e17f388b
Size                    10.00 GiB
Perf Unique Size        In Process
Perf Shared Size        In Process
Cap Unique Size         In Process
Cap Shared Size         In Process
Logical Used Size       In Process
Volume id               260246de-86f6-4c56-ba82-f409e17f388b
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Encrypt Metadata Id     0
Replica Num             2
EC Param
Thin Provision          True
Creation Time           2025-07-07 09:54:03.247136154
Description
NAA                     33c4d6f6aded64206
Allowed Initiators
Single Access           False
PR                      Details
Prefer CID              0
Read Only               False
Secondary ID
Is Prioritized          False
Downgraded PRS          0.00 B
Chunk Instances
Labels                  []
Use Host                True
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Size` | LUN 的总容量 |
| `Perf Unique Size` | 独占的性能层空间大小。 |
| `Perf Shared Size` | 和其他对象共享的性能层空间大小。 |
| `Cap Unique Size` | 独占的容量层空间大小。 |
| `Cap Shared Size` | 和其他对象共享的容量层空间大小。 |
| `Logical Used Size` | 已经分配的逻辑空间大小。 |
| `Resiliency Type` | 冗余模式。 |
| `Encrypt Method` | 存储卷的数据加密算法。 |
| `Encrypt Metadata Id` | 存储卷的加密元数据 ID。 |
| `Replica Num` | 副本数。 |
| `EC Param` | EC 冗余模式下对应的 EC 参数。 |
| `Thin Provision` | 是否启用精简置备。`True`代表启用精简置备；`False`代表不启用精简置备，存储策略为厚置备。 |
| `NAA` | NAA ID。 |
| `Allowed Initiators` | LUN 级别的 initiator 白名单。 |
| `Single Access` | 是否开启了 single access。若开启了 single access，存储卷仅能被唯一客户端访问。 |
| `PR` | Persistence Reserve，永久保留信息。 |
| `Is Prioritized` | 是否要将数据都维持在性能层中。 |
| `Downgraded PRS` | 尚未提升到性能层的空间大小。 |
| `Use Host` | 是否使用业务主机指定白名单。 |
| `Allowed Host Ids` | 关联的业务主机的 ID。 |
| `Allowed Host Group Ids` | 关联的业务主机组的 ID。 |

## 创建 iSCSI LUN

**操作方法**

在集群任一节点执行如下命令：

```
zbs-iscsi lun create <target_name> <lun_id> <size>
                     [--lun_name <LUN_NAME>] [--lun_uuid <LUN_UUID>]
                     [--resiliency_type <RESILIENCY_TYPE>]
                     [--replica_num <REPLICA_NUM>] [--ec_algo <EC_ALGO>]
                     [--ec_k <EC_K>] [--ec_m <EC_M>][--ec_block_size <EC_BLOCK_SIZE>]
                     [--encrypt_method <ENCRYPT_METHOD>]
                     [--thin_provision <THIN_PROVISION>] [--desc <DESC>]
                     [--stripe_num <STRIPE_NUM>] [--stripe_size <STRIPE_SIZE>]
                     [--iops <IOPS>] [--iops_rd <IOPS_RD>]
                     [--iops_wr <IOPS_WR>] [--iops_max <IOPS_MAX>]
                     [--iops_rd_max <IOPS_RD_MAX>] [--iops_wr_max <IOPS_WR_MAX>]
                     [--iops_max_length <IOPS_MAX_LENGTH>]
                     [--iops_rd_max_length <IOPS_RD_MAX_LENGTH>]
                     [--iops_wr_max_length <IOPS_WR_MAX_LENGTH>]
                     [--iops_io_size <IOPS_IO_SIZE>] [--bps <BPS>] [--bps_rd <BPS_RD>]
                     [--bps_wr <BPS_WR>]
                     [--bps_max <BPS_MAX>] [--bps_rd_max <BPS_RD_MAX>]
                     [--bps_wr_max <BPS_WR_MAX>] [--bps_max_length <BPS_MAX_LENGTH>]
                     [--bps_rd_max_length <BPS_RD_MAX_LENGTH>]
                     [--bps_wr_max_length <BPS_WR_MAX_LENGTH>]
                     [--allowed_initiators <ALLOWED_INITIATORS>]
                     [--preferred_cid <PREFERRED_CID>]
                     [--single_access <SINGLE_ACCESS>] [--prioritized <PRIORITIZED>]
                     [--use_host <USE_HOST>] [--allowed_host_ids <ALLOWED_HOST_IDS>]
                     [--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>]
```

| 参数 | 说明 |
| --- | --- |
| `target_name` | LUN 所属的 target 名称。 |
| `lun_id` | LUN ID。 |
| `size` | LUN 大小。 |
| `--lun_name <LUN_NAME>` | 新建 LUN 名称。 |
| `--lun_uuid <LUN_UUID>` | 新建 LUN UUID。 |
| `--resiliency_type <RESILIENCY_TYPE>` | 设置冗余模式，副本或 EC，若未设置，将从 target 继承，默认为 `None`。 |
| `--replica_num <REPLICA_NUM>` | 设置新建 LUN 的默认副本数，可设置为 2 副本或 3 副本，默认为 `None`。 |
| `--ec_algo <EC_ALGO>` | 设置 EC 算法，当冗余模式为 EC 时必须设置，默认为 `RS`。 |
| `--ec_k <EC_K>` | 设置 EC 算法参数 K，参数范围为 [2，23]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--ec_m <EC_M>` | 设置 EC 算法参数 M，参数范围为 [1，4]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--ec_block_size <EC_BLOCK_SIZE>` | 当冗余模式为 EC 时，默认为 `4096`，否则默认为 `None`。 |
| `--encrypt_method <ENCRYPT_METHOD>` | 设置数据加密方法，默认为不加密 。 |
| `--thin_provision <THIN_PROVISION>` | `True` 或 `False`，表示是否设置新建 LUN 的置备方式为精简置备。 |
| `--desc <DESC>` | 设置 LUN 描述。 |
| `--stripe_num <STRIPE_NUM>` | 新建 LUN 的条带数。 |
| `--stripe_size <STRIPE_SIZE>` | 新建 LUN 的条带大小。 |
| `--iops <IOPS>` | 设置新建 LUN 的总 IOPS 上限值。 |
| `--iops_rd <IOPS_RD>` | 设置读 IOPS 的上限值。 |
| `--iops_wr <IOPS_WR>` | 设置写 IOPS 的上限值。 |
| `--iops_max <IOPS_MAX>` | 设置总 IOPS 突发的上限值。 |
| `--iops_rd_max <IOPS_RD_MAX>` | 设置读 IOPS 突发的上限值。 |
| `--iops_wr_max <IOPS_WR_MAX>` | 设置写 IOPS 突发的上限值。 |
| `--iops_max_length <IOPS_MAX_LENGTH>` | 设置总 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_rd_max_length <IOPS_RD_MAX_LENGTH>` | 设置读 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_wr_max_length <IOPS_WR_MAX_LENGTH>` | 设置写 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_io_size <IOPS_IO_SIZE>` | 使用 IOPS 限速时，假定的平均 I/O 数据量大小。 |
| `--bps <BPS>` | 设置新建 LUN 的总带宽限制，单位为 Bps。 |
| `--bps_rd <BPS_RD>` | 设置读带宽的上限值。 |
| `--bps_wr <BPS_WR>` | 设置写带宽的上限值。 |
| `--bps_max <BPS_MAX>` | 设置总带宽在发生 I/O 突发时的上限值。 |
| `--bps_rd_max <BPS_RD_MAX>` | 设置读带宽在发生 I/O 突发时的上限值。 |
| `--bps_wr_max <BPS_WR_MAX>` | 设置写带宽在发生 I/O 突发时的上限值。 |
| `--bps_max_length <BPS_MAX_LENGTH>` | 设置在发生 I/O 突发时，以总带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_rd_max_length <BPS_RD_MAX_LENGTH>` | 设置在发生 I/O 突发时，以读带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_wr_max_length <BPS_WR_MAX_LENGTH>` | 设置在发生 I/O 突发时，以写带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--allowed_initiators <ALLOWED_INITIATORS>` | 设置新建 LUN 的 IQN 白名单。 |
| `--preferred_cid <PREFERRED_CID>` | 设置倾向的 chunk ID，Meta 在分配 PExtent 副本时，会尽量靠近该 chunk。 |
| `--single_access <SINGLE_ACCESS>` | `True` 或 `False`，若为 `True`，则只有一个 initiator 可以访问该 LUN，且该 LUN 的 IQN 白名单只能为空或单个 IQN。 |
| `--prioritized <PRIORITIZED>` | 设置 LUN 的数据是否都需要维持在性能层中，可设置为 `True` 或 `False`。 |
| `--use_host <USE_HOST>` | 设置是否使用业务主机指定白名单。 |
| `--allowed_host_ids <ALLOWED_HOST_IDS>` | 设置关联的业务主机的 ID，以英文逗号（,）分隔多个 ID。 |
| `--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>` | 设置关联的业务主机组的 ID，以英文逗号（,）分隔多个 ID。 |

**输出示例**

```
----------------------  ------------------------------------
LUN Id                  1
LUN Name                260246de-86f6-4c56-ba82-f409e17f388b
Size                    10.00 GiB
Perf Unique Size        In Process
Perf Shared Size        In Process
Cap Unique Size         In Process
Cap Shared Size         In Process
Logical Used Size       In Process
Volume id               260246de-86f6-4c56-ba82-f409e17f388b
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Encrypt Metadata Id     0
Replica Num             2
EC Param
Thin Provision          True
Creation Time           2025-07-07 09:54:03.247136154
Description
NAA                     33c4d6f6aded64206
Allowed Initiators
Single Access           False
PR                      Details
Prefer CID              0
Read Only               False
Secondary ID
Is Prioritized          False
Downgraded PRS          0.00 B
Chunk Instances
Labels                  []
Use Host                True
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 提升 iSCSI LUN 副本数和扩容 LUN 容量

**操作方法**

在集群节点执行如下命令：

`zbs-iscsi lun update <target_name> <lun_id> [--replica_num <REPLICA_NUM>][--new_name <NEW_NAME>] [--desc <DESC>] [--size <SIZE>]`

| 参数 | 说明 |
| --- | --- |
| `target_name` | LUN 所属的 target 名称。 |
| `lun_id` | LUN ID。 |
| `--replica_num <REPLICA_NUM>` | 重新设置 LUN 副本数，副本数只支持提升，不支持降低。 |
| `--new_name <NEW_NAME>` | 设置 LUN 的新名称。 |
| `--desc <DESC>` | 设置 LUN 描述。 |
| `--size <SIZE>` | 调整 LUN 大小，新设置容量不能小于原容量，否则报错。因此仅能为 LUN 扩容。 |

**输出示例**

```
----------------------  ------------------------------------
LUN Id                  1
LUN Name                260246de-86f6-4c56-ba82-f409e17f388b
Size                    10.00 GiB
Perf Unique Size        0.00 B
Perf Shared Size        0.00 B
Cap Unique Size         0.00 B
Cap Shared Size         0.00 B
Logical Used Size       0.00 B
Volume id               260246de-86f6-4c56-ba82-f409e17f388b
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Encrypt Metadata Id     0
Replica Num             2
EC Param
Thin Provision          True
Creation Time           2025-07-07 09:54:03.247136154
Description             new-desc
NAA                     33c4d6f6aded64206
Allowed Initiators
Single Access           False
PR                      Details
Prefer CID              0
Read Only               False
Secondary ID
Is Prioritized          False
Downgraded PRS          0.00 B
Chunk Instances
Labels                  []
Use Host                True
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 克隆 iSCSI LUN

**操作方法**

在集群任一节点执行如下命令，克隆 iSCSI LUN：

`zbs-iscsi lun clone [--lun_name <LUN_NAME>] [--src_target_name <SRC_TARGET_NAME>] [--src_lun_id <SRC_LUN_ID>] [--src_snapshot_id <SRC_SNAPSHOT_ID>] <dst_target_name> <dst_lun_id>`

| 参数 | 说明 |
| --- | --- |
| `--lun_name <LUN_NAME>` | 克隆的 LUN 的名称。 |
| `--src_target_name <SRC_TARGET_NAME>` | 克隆的源 target 名称。 |
| `--src_lun_id <SRC_LUN_ID>` | 克隆的源 LUN ID。 |
| `--src_snapshot_id <SRC_SNAPSHOT_ID>` | 克隆的源 snapshot ID，若源 LUN ID 和源 snapshot ID 均被指定，则使用源 snapshot ID 作为克隆源。 |
| `dst_target_name` | 克隆 LUN 所属的 target。 |
| `dst_lun_id` | 克隆的 LUN 的 ID。 |

**输出示例**

```
[root@host-3 16:21:32 ~]$ zbs-iscsi lun clone --src_target_name t1 --src_lun_id 1 t2 1
----------------------  ------------------------------------
LUN Id                  1
LUN Name                50341729-faf6-4315-b7e9-b17bb7163010
Size                    10.00 GiB
Perf Unique Size        In Process
Perf Shared Size        In Process
Cap Unique Size         In Process
Cap Shared Size         In Process
Logical Used Size       In Process
Volume id               50341729-faf6-4315-b7e9-b17bb7163010
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Encrypt Metadata Id     0
Replica Num             2
EC Param
Thin Provision          True
Creation Time           2025-07-07 10:08:49.433888331
Description
NAA                     3334d6fafd9271430
Allowed Initiators      */*
Single Access           False
PR                      Details
Prefer CID              0
Read Only               False
Secondary ID
Is Prioritized          False
Downgraded PRS          0.00 B
Chunk Instances
Labels                  []
Use Host                False
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 移动 iSCSI LUN 至另一 iSCSI target

**操作方法**

在集群任一节点执行如下命令，将 LUN 从当前所属 target 移动至另一 target：

`zbs-iscsi lun move <src_target_name> <src_lun_id> <target_name> <lun_id> <lun_name>`

| 参数 | 说明 |
| --- | --- |
| `src_target_name` | LUN 所属源 target。 |
| `src_lun_id` | 待移动的 LUN ID。 |
| `target_name` | LUN 移动的目的 target。 |
| `lun_id` | 移动至新 target 后的 LUN ID。 |
| `lun_name` | 移动至新 target 后的 LUN 名称。 |

**输出示例**

```
----------------------  ------------------------------------
LUN Id                  1
LUN Name                50341729-faf6-4315-b7e9-b17bb7163010
Size                    10.00 GiB
Perf Unique Size        In Process
Perf Shared Size        In Process
Cap Unique Size         In Process
Cap Shared Size         In Process
Logical Used Size       In Process
Volume id               50341729-faf6-4315-b7e9-b17bb7163010
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Encrypt Metadata Id     0
Replica Num             2
EC Param
Thin Provision          True
Creation Time           2025-07-07 10:08:49.433888331
Description
NAA                     3334d6fafd9271430
Allowed Initiators      */*
Single Access           False
PR                      Details
Prefer CID              0
Read Only               False
Secondary ID
Is Prioritized          False
Downgraded PRS          0.00 B
Chunk Instances
Labels                  []
Use Host                False
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 添加 iSCSI LUN 的客户端 IQN 白名单

**操作方法**

在集群任一节点执行如下命令，增加可访问 iSCSI LUN 的客户端 IQN 白名单：

`zbs-iscsi lun add_allowed_initiators <target_name> <lun_id> <new_allowed_initiators>`

| 参数 | 说明 |
| --- | --- |
| `target_name` | LUN 所属的 iSCSI target 名称。 |
| `lun_id` | LUN 名称。 |
| `new_allowed_initiators` | 新增可访问 LUN 的客户端 IQN 白名单，多个客户端之间以英文逗号 `,` 隔开，例如：`iqn.1994-05.com.redhat:d422cf1e7f5,iqn.1994-05.com.redhat:1` |

**输出说明**

执行成功无输出。

## 移除 iSCSI LUN 的客户端 IQN 白名单

**操作方法**

在集群任一节点执行如下命令，移除 iSCSI LUN 的客户端 IQN 白名单：

`zbs-iscsi lun remove_allowed_initiators <target_name> <lun_id> <initiators>`

| 参数 | 说明 |
| --- | --- |
| `target_name` | LUN 所属的 iSCSI target 名称。 |
| `lun_id` | LUN 名称。 |
| `initiators` | 移除可访问 LUN 的客户端 IQN 白名单，多个客户端之间以英文逗号 `,` 隔开，例如：`iqn.1994-05.com.redhat:d422cf1e7f5, iqn.1994-05.com.redhat:1`。 |

**输出说明**

执行成功无输出。

## 删除 iSCSI LUN

**操作方法**

在集群任一节点执行如下命令，删除 iSCSI target 下的指定 LUN：

`zbs-iscsi lun delete <target_name> <lun_id>`

**输出说明**

执行成功无输出。

## 清空 iSCSI LUN 的永久保留信息

如异常情况下发现 LUN 有残留的 PR，或者存在不需要的注册者（registrants），可使用如下命令清空 LUN 的永久保留信息。

**操作方法**

在集群任一节点执行如下命令：

`zbs-iscsi lun reset_pr <target_name> <lun_id>`

**输出说明**

执行成功无输出。

## 将 iSCSI LUN 转换为 NFS 文件

**操作方法**

在集群任一节点执行如下命令：

`zbs-nfs file convert_from_lun <parent_id> <name> <lun_uuid> [--mode MODE] [--uid UID] [--gid GID] [--atime_how <ATIME_HOW>] [--mtime_how <MTIME_HOW>] [--atime_sec <ATIME_SEC>] [--atime_nsec <ATIME_NSEC>] [--mtime_sec <MTIME_SEC>] [--mtime_nsec <MTIME_NSEC>]`

| 参数 | 说明 |
| --- | --- |
| `parent_id` | inode 文件的目录 ID。 |
| `name` | inode 文件名称。 |
| `lun_uuid` | 待转换 LUN 的 UUID。 |
| `--mode MODE` | 文件的读/写权限设置。 |
| `--atime_how <ATIME_HOW>` | 设置文件访问时间的来源。`SET_TO_SERVER_TIME`：访问时间使用 NFS 文件 server 端的时间； `SET_TO_CLIENT_TIME`：访问时间使用客户端的时间；`DONT_CHANGE`：不改变访问时间，此为默认设置。 |
| `--atime_sec <ATIME_SEC>` | 设置访问时间，以秒（s）为单位。 |
| `--atime_nsec <ATIME_NSEC>` | 设置访问时间，以纳秒（ns）为单位。 |
| `--mtime_how <MTIME_HOW>` | 设置文件修改时间的来源。`SET_TO_SERVER_TIME`：修改时间使用 NFS 文件 server 端的时间； `SET_TO_CLIENT_TIME`：修改时间使用客户端的时间；`DONT_CHANGE`：不改变修改时间，此为默认设置。 |
| `--mtime_sec <MTIME_SEC>` | 设置修改时间，以秒（s）为单位。 |
| `--mtime_nsec <MTIME_NSEC>` | 设置修改时间，以纳秒（ns）为单位。 |

**输出示例**

```
-----------------  ------------------------------------
id                 9ab2f518-0947-4bd3
name               nfs5
pool               f6722181-7eb8-4ab4-ac39-7a06d29f6890
preallocate        False
volume             9ab2f518-0947-4bd3-b8b3-984e1a2d634f
type               FILE
mode               432
uid                0
gid                0
size               1024.00 GiB
perf unique size   In Process
perf shared size   In Process
cap unique size    In Process
cap shared size    In Process
logical used size  In Process
prioritized        False
downgraded_prs     0.00 B
-----------------  ------------------------------------
```

---

## 管理 iSCSI 存储服务 > 管理 iSCSI LUN 快照

# 管理 iSCSI LUN 快照

## 查看 iSCSI LUN 快照

**操作方法**

- 在集群任一节点执行如下命令，查看指定 target 下的所有 iSCSI LUN 快照：

  `zbs-iscsi snapshot list <target_name> [--lun_id <LUN_ID>]`

  其中，`--lun_id <LUN_ID>` 为可选参数，可选择查看指定 LUN 的所有快照。
- 在集群任一节点执行如下命令，查看指定名称的 iSCSI LUN 快照：

  `zbs-iscsi snapshot show <target_name> <lun_id> <snapshot_name>`
- 在集群任一节点执行如下命令，查看指定 ID 的 iSCSI LUN 快照：

  `zbs-iscsi snapshot show_by_id <snapshot_id>`

**输出示例**

```
ID                                    Snap Name    Size      Perf Unique Size    Perf Shared Size    Cap Unique Size    Cap Shared Size    Logical Used Size    Diff Size    Volume Id                             Creation Time                  Description
------------------------------------  -----------  --------  ------------------  ------------------  -----------------  -----------------  -------------------  -----------  ------------------------------------  -----------------------------  -------------
310d7ba5-361f-42e7-bdc4-aba0d12806f6  sp1          4.00 GiB  0.00 B              0.00 B              0.00 B             0.00 B             0.00 B               0.00 B       b85164e6-dee3-47e0-8867-e8f3f7cb26e7  2024-06-18 11:45:46.442463351
```

## 创建 iSCSI LUN 快照

**操作方法**

在集群任一节点执行如下命令：

`zbs-iscsi snapshot create <target_name> <lun_id> <name>`

**输出示例**

```
-----------------  ------------------------------------
ID                 310d7ba5-361f-42e7-bdc4-aba0d12806f6
Snap Name          sp1
Size               4.00 GiB
Perf Unique Size   In Process
Perf Shared Size   In Process
Cap Unique Size    In Process
Cap Shared Size    In Process
Logical Used Size  In Process
Diff Size          0.00 B
Volume Id          b85164e6-dee3-47e0-8867-e8f3f7cb26e7
Creation Time      2024-06-18 11:45:46.442463351
Description
-----------------  ------------------------------------
```

## 从 iSCSI LUN 快照回滚

将快照回滚至指定的 LUN 中，快照可以是其他 LUN 的快照，而非原始 LUN 的快照。在执行操作后，LUN 内的数据会被快照的数据完整替换。

**操作方法**

- 在集群任一节点执行如下命令，将 iSCSI LUN 从指定名称的快照进行回滚：

  `zbs-iscsi snapshot rollback <target_name> <lun_id> <snapshot_name>`
- 在集群任一节点执行如下命令，将 iSCSI LUN 从指定 ID 的快照进行回滚：

  `zbs-iscsi snapshot rollback_by_id <target_name> <lun_id> <snapshot_id>`

**输出说明**

执行成功无输出。

## 更新 iSCSI LUN 快照

重新设置 iSCSI LUN 的名称、描述以及数据是否均匀分配。

**操作方法**

- 在集群任一节点执行如下命令，更新指定名称的 LUN 快照：

  `zbs-iscsi snapshot update [--new_name <NEW_NAME>] [--new_desc <NEW_DESC>] [--new_alloc_even <NEW_ALLOC_EVEN>] <target_name> <lun_id> <snapshot_name>`
- 在集群任一节点执行如下命令，更新指定 ID 的 LUN 快照：

  `zbs-iscsi snapshot update_by_id [--new_name <NEW_NAME>] [--new_desc <NEW_DESC>] [--new_alloc_even <NEW_ALLOC_EVEN>] <snapshot_id>`

| 参数 | 说明 |
| --- | --- |
| `--new_name <NEW_NAME>` | 更新对相应快照的名称。 |
| `--new_desc <NEW_DESC>` | 更新对相应快照的描述。 |
| `--new_alloc_even <NEW_ALLOC_EVEN>` | `NEW_ALLOC_EVEN` 取值为 `true` 或 `false`，分别表示是否设置副本均匀分布。 |

**输出示例**

```
-----------------  ------------------------------------
ID                 310d7ba5-361f-42e7-bdc4-aba0d12806f6
Snap Name          snapshot1
Size               4.00 GiB
Perf Unique Size   In Process
Perf Shared Size   In Process
Cap Unique Size    In Process
Cap Shared Size    In Process
Logical Used Size  In Process
Diff Size          0.00 B
Volume Id          b85164e6-dee3-47e0-8867-e8f3f7cb26e7
Creation Time      2024-06-18 11:45:46.442463351
Description
-----------------  -----------------------------------
```

## 删除 iSCSI LUN 快照

**操作方法**

- 在集群任一节点执行如下命令，删除指定名称的快照：

  `zbs-iscsi snapshot delete <target_name> <lun_id> <name>`
- 在集群任一节点执行如下命令，删除指定 ID 的快照：

  `zbs-iscsi snapshot delete_by_id <snapshot_id>`

**输出说明**

执行成功无输出。

---

## 管理 CDP 任务

# 管理 CDP 任务

本章节介绍 Continuous Data Protection (CDP) 相关的命令操作，主要包括 CDP 任务的创建、结束、取消、删除、查询以及模式切换等管理功能。此外，还包含用于脏页面追踪（Dirty Block Tracing）的测试命令。

---

## 管理 CDP 任务 > 创建 CDP 任务

# 创建 CDP 任务

## 创建单个 CDP 任务

**操作方法**

在集群任一节点执行如下命令：

```
zbs-cdp job create <volume_id> <remote_volume_id> <remote_zbs_hosts> [options]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `volume_id` | 必选参数，本地存储卷 ID。 |
| `remote_volume_id` | 必选参数，远端存储卷 ID。 |
| `remote_zbs_hosts` | 必选参数，远端主机列表，格式为 `ip:data_port:meta_port,ip:data_port:meta_port...`。 |
| `--cid <CID>` | 可选参数，本地 chunk ID，默认为 `None`。 |
| `--group <GROUP>` | 可选参数，CDP 任务组名称，默认为 `None`。 |
| `--skip_fc_write_zero` | 可选参数，是否跳过同步全零 I/O，默认为 `True`。可以使用 `--no_skip_fc_write_zero` 关闭此功能。 |
| `--auto_clean` | 可选参数，任务完成或取消后是否自动清理，默认为 `False`。 |
| `--use_compress` | 可选参数，是否启用 CDP 块 I/O 压缩，默认为 `False`。 |
| `--tracking_only` | 可选参数，创建后是否仅进行追踪模式，默认为 `False`。 |
| `--skip_full_copy` | 可选参数，是否跳过全量复制，默认为 `False`。 |
| `--sync` / `--no-sync` | 可选参数，是否同步等待任务创建完成，默认为 `True`。 |
| `--max_read_timeout_ms <MS>` | 可选参数，最大读取超时时间（毫秒），默认为 `None`。 |
| `--max_block_write_timeout_ms <MS>` | 可选参数，最大块写入超时时间（毫秒），默认为 `None`。 |
| `--max_mirror_write_timeout_ms <MS>` | 可选参数，最大镜像写入超时时间（毫秒），默认为 `None`。 |
| `-v` / `--version <VER>` | 必选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
zbs-cdp job create be09dd2c-325d-406c-b772-bcb36d3991fd 6c786d90-1857-4423-a655-0f268622aea0 10.10.130.31:10201:10206 --cid 1 -v v2
-------------  ------------------------------------
Version        v2
ID             3d936175-65c6-4cb0-8909-3796511875e4
Group          None
Stage          FULL_COPY
Compress       False
No Full Copy   False
CID            1
Local volume   be09dd2c-325d-406c-b772-bcb36d3991fd
Remote volume  6c786d90-1857-4423-a655-0f268622aea0
Remote Addr    10.10.130.31:10201:10206
CDPJobOption
ERROR          None
-------------  ------------------------------------
```

**输出说明**

执行成功后，将显示新创建的 CDP 任务详情：

| 参数 | 说明 |
| --- | --- |
| `Version` | CDP 协议版本。 |
| `ID` | 任务唯一标识符。 |
| `Group` | 任务所属组名称。 |
| `Stage` | 任务当前阶段（如 `FULL_COPY`、`MIRROR` 等）。 |
| `Compress` | 是否启用 CDP 块 I/O 压缩。 |
| `No Full Copy` | 是否跳过全量复制。 |
| `CID` | 本地 chunk ID。 |
| `Local volume` | 本地存储卷 ID。 |
| `Remote volume` | 远端存储卷 ID。 |
| `Remote Addr` | 远端主机地址。 |
| `CDPJobOption` | 任务特定选项（如超时配置）。 |
| `ERROR` | 错误信息（无错误则显示 `None`）。 |

## 批量创建 CDP 任务

**操作方法**

在集群任一节点执行如下命令：

```
zbs-cdp job add_by_group <group> <remote_zbs_hosts> --volume_pairs <PAIRS> [options]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `group` | 必选参数，CDP 任务组名称。 |
| `remote_zbs_hosts` | 必选参数，远端主机列表，格式为 `ip:data_port:meta_port,ip:data_port:meta_port...`。 |
| `--volume_pairs` | 必选参数，存储卷对列表，格式为 `local_volume_id=remote_volume_id`，支持多个。 |
| `--cid <CID>` | 可选参数，本地 chunk ID，默认为 `None`。 |
| `--skip_fc_write_zero` | 可选参数，是否跳过同步全零 I/O，默认为 `True`。可以使用 `--no_skip_fc_write_zero` 关闭此功能。 |
| `--auto_clean` | 可选参数，任务完成或取消后是否自动清理，默认为 `False`。 |
| `--use_compress` | 可选参数，是否启用 CDP 块 I/O 压缩，默认为 `False`。 |
| `--tracking_only` | 可选参数，创建后是否仅进行追踪模式，默认为 `False`。 |
| `--skip_full_copy` | 可选参数，是否跳过全量复制，默认为 `False`。 |
| `--sync` | 可选参数，是否同步等待任务创建完成，默认为 `True`。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
zbs-cdp job add_by_group example 10.10.130.31:10201:10206 --cid 1 -v v2 --volume_pairs 2ea55379-34dc-4b36-a4bd-6027b5d1f8b2=e9fbfd57-8ac2-4908-b44d-e8f0bfe2b89b 3af41af7-db61-425a-91ed-1e366f7404b9=da2f5f67-a3a1-4b24-bc5d-132e337dc1c8
Version    ID                                    Group    Stage    Compress    No Full Copy      CID  Local volume                          Remote volume                         Remote Addr               CDPJobOption    ERROR
---------  ------------------------------------  -------  -------  ----------  --------------  -----  ------------------------------------  ------------------------------------  ------------------------  --------------  -------
v2         c791e4e2-e4d4-4e97-8636-bcc84cc76c85  example  INIT     False       False               1  2ea55379-34dc-4b36-a4bd-6027b5d1f8b2  e9fbfd57-8ac2-4908-b44d-e8f0bfe2b89b  10.10.130.31:10201:10206                  None
v2         322ee53b-ab96-4367-873c-f8b0fbd296f1  example  INIT     False       False               1  3af41af7-db61-425a-91ed-1e366f7404b9  da2f5f67-a3a1-4b24-bc5d-132e337dc1c8  10.10.130.31:10201:10206                  None
```

**输出说明**

批量创建成功后，将以列表形式展示该组内所有新创建的任务信息。字段说明详见[创建单个 CDP 任务](#%E5%88%9B%E5%BB%BA%E5%8D%95%E4%B8%AA-cdp-%E4%BB%BB%E5%8A%A1)部分的输出说明。

---

## 管理 CDP 任务 > 结束 CDP 任务

# 结束 CDP 任务

## 结束单个 CDP 任务

**操作方法**

在集群任一节点执行如下命令：

- 通过任务 ID 结束：

  ```
  zbs-cdp job finish <id> [options]
  ```
- 通过本地卷 ID 结束：

  ```
  zbs-cdp job finish_by_volume <volume_id> [options]
  ```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `id` | 任务 ID。 |
| `volume_id` | 本地存储卷 ID。 |
| `--sync` / `--no-sync` | 可选参数，是否同步等待任务结束，默认为 `True`。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

- 通过任务 ID 结束：

  ```
  zbs-cdp job finish 1 -v v2
  ```
- 通过本地卷 ID 结束：

  ```
  zbs-cdp job finish_by_volume 1 -v v2
  ```

**输出说明**

执行成功无输出。若执行失败，将显示异常提示信息。

## 批量结束 CDP 任务

批量结束 CDP 任务即结束 CDP 任务组中所有 CDP 任务。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-cdp job finish_by_group <group> [options]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `group` | CDP 任务组名称。 |
| `--sync` / `--no-sync` | 可选参数，是否同步等待任务组结束，默认为 `True`。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
zbs-cdp job finish_by_group group1 -v v2
```

**输出说明**

执行成功无输出。若执行失败，将显示异常提示信息。

---

## 管理 CDP 任务 > 取消 CDP 任务

# 取消 CDP 任务

取消任务会停止当前的同步进程。

## 取消单个 CDP 任务

**操作方法**

在集群任一节点执行如下命令：

- 通过任务 ID 取消：

  ```
  zbs-cdp job cancel <id> [options]
  ```
- 通过本地卷 ID 取消：

  ```
  zbs-cdp job cancel_by_volume <volume_id> [options]
  ```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `id` | 任务 ID。 |
| `volume_id` | 本地存储卷 ID。 |
| `--sync` / `--no-sync` | 可选参数，是否同步等待任务取消，默认为 `True`。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

- 通过任务 ID 取消：

  ```
  zbs-cdp job cancel 1 -v v2
  ```
- 通过本地卷 ID 取消：

  ```
  zbs-cdp job cancel_by_volume 1 -v v2
  ```

**输出说明**

执行成功无输出。若执行失败，将显示异常提示信息。

## 批量取消 CDP 任务

批量取消 CDP 任务即取消 CDP 任务组中所有 CDP 任务。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-cdp job cancel_by_group <group> [options]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `group` | CDP 任务组名称。 |
| `--sync` / `--no-sync` | 可选参数，是否同步等待任务组取消，默认为 `True`。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
zbs-cdp job cancel_by_group group1 -v v2
```

**输出说明**

执行成功无输出。若执行失败，将显示异常提示信息。

---

## 管理 CDP 任务 > 删除 CDP 任务

# 删除 CDP 任务

删除任务会移除任务记录。

## 删除单个 CDP 任务

**操作方法**

- 通过任务 ID 删除：

  ```
  zbs-cdp job delete <id>
  ```
- 通过本地卷 ID 删除：

  ```
  zbs-cdp job delete_by_volume <volume_id>
  ```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `id` | 任务 ID。 |
| `volume_id` | 本地存储卷 ID。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
zbs-cdp job delete 1 -v v2
```

或

```
zbs-cdp job delete_by_volume 1 -v v2
```

**输出说明**

执行成功无输出。若执行失败，将显示异常提示信息。

## 批量删除 CDP 任务

批量删除 CDP 任务即删除 CDP 任务组中所有 CDP 任务。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-cdp job delete_by_group <group> [options]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `group` | CDP 任务组名称。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
zbs-cdp job delete_by_group group1 -v v2
```

**输出说明**

执行成功无输出。若执行失败，将显示异常提示信息。

---

## 管理 CDP 任务 > 查看 CDP 任务

# 查看 CDP 任务

## 查看 CDP 任务列表

### 查看所有 CDP 任务

**操作方法**

在集群任一节点执行如下命令：

```
zbs-cdp job list [options]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `--group <GROUP>` | 可选参数，按组名称筛选。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
zbs-cdp job list
Version    ID                                    Group                                            Stage    Compress    No Full Copy      CID  Local volume                          Remote volume                         Remote Addr               CDPJobOption    ERROR
---------  ------------------------------------  -----------------------------------------------  -------  ----------  --------------  -----  ------------------------------------  ------------------------------------  ------------------------  --------------  -------
v2         c791e4e2-e4d4-4e97-8636-bcc84cc76c85  example                                          MIRROR   False       False               1  2ea55379-34dc-4b36-a4bd-6027b5d1f8b2  e9fbfd57-8ac2-4908-b44d-e8f0bfe2b89b  10.10.130.31:10201:10206                  None
v2         322ee53b-ab96-4367-873c-f8b0fbd296f1  example                                          MIRROR   False       False               1  3af41af7-db61-425a-91ed-1e366f7404b9  da2f5f67-a3a1-4b24-bc5d-132e337dc1c8  10.10.130.31:10201:10206                  None
v2         e5fc0fbe-bdae-4f4d-a943-b465b928c91d  cmjjmxbzp15w701udccy464wr-6c9dc8b557-78f766f5c4  MIRROR   False       True                4  d971646c-d470-46cb-9dff-32cd0cfff5d2  77215d42-d068-4582-9e82-0b6c0c192ba9  10.10.130.31:10201:10206                  None
v2         e4c47df1-012d-4a72-a424-1a34818fd905  cmjjmxbzp15w701udccy464wr-6c9dc8b557-78f766f5c4  MIRROR   False       True                4  46b9fea1-3aee-4121-8fbc-270ae577f7f8  b7aaa2e8-0d52-4a11-a97a-d5ac420e025a  10.10.130.31:10201:10206                  None
```

**输出说明**

执行成功后，将列出所有符合条件的 CDP 任务列表。字段说明详见[创建单个 CDP 任务](/smtxos/6.3.0/cli_guide/cli_guide_105#%E5%88%9B%E5%BB%BA%E5%8D%95%E4%B8%AA-cdp-%E4%BB%BB%E5%8A%A1)部分的输出说明。

### 查看本地 CDP 任务

**操作方法**

在集群任一节点执行如下命令：

```
zbs-cdp job list_local [options]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `--group <GROUP>` | 可选参数，按组名称筛选。 |
| `--chunk_ip <IP>` | 可选参数，指定 chunk 节点的 IP 地址。 |
| `--chunk_port <PORT>` | 可选参数，指定 chunk 节点的端口。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
zbs-cdp job list_local
Version    ID                                    Group    Stage    Compress    No Full Copy      CID  Local volume                          Remote volume                         Remote Addr               CDPJobOption    ERROR
---------  ------------------------------------  -------  -------  ----------  --------------  -----  ------------------------------------  ------------------------------------  ------------------------  --------------  -------
v2         322ee53b-ab96-4367-873c-f8b0fbd296f1  example  MIRROR   False       False               0  3af41af7-db61-425a-91ed-1e366f7404b9  da2f5f67-a3a1-4b24-bc5d-132e337dc1c8  10.10.130.31:10201:10206                  None
```

**输出说明**

执行成功后，将列出本地节点上运行的 CDP 任务列表。字段说明详见[创建单个 CDP 任务](#%E5%88%9B%E5%BB%BA%E5%8D%95%E4%B8%AA-cdp-%E4%BB%BB%E5%8A%A1)部分的输出说明。

## 查看 CDP 任务详情

### 查看任务详情

**操作方法**

在集群任一节点执行如下命令：

- 通过任务 ID 查看：

  ```
  zbs-cdp job show <id> [options]
  ```
- 通过本地卷 ID 查看：

  ```
  zbs-cdp job show_by_volume <volume_id> [options]
  ```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `id` | 任务 ID。 |
| `volume_id` | 本地存储卷 ID。 |
| `--show_sync_point_tasks` | 可选参数，显示该任务的同步点任务详情。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
-------------  ------------------------------------
Version        v2
ID             c7312eda-e462-41bf-860f-ebc61571ae2e
Group          example
Stage          MIRROR
Compress       False
No Full Copy   False
CID            1
Local volume   be09dd2c-325d-406c-b772-bcb36d3991fd
Remote volume  6c786d90-1857-4423-a655-0f268622aea0
Remote Addr    10.10.130.31:10201:10206
CDPJobOption
ERROR          None
-------------  ------------------------------------

========== CURRENT SYNC POINT TASK ==========
ID: bd9268c3-512d-4191-99fa-6b3a46543029 -> 3515af1e-56b8-46e0-bb95-eebc2148dc0c
Name: test_sp_20251226_141434_r1_1 -> test_sp_20251226_141434_r1_1
Secondary ID:  ->

========== SYNC POINT TASKS ==========
Stage    Src Snapshot                  Src ID                                Src Secondary ID    Remote Snapshot               Remote ID                             Remote Secondary ID    ERROR
-------  ----------------------------  ------------------------------------  ------------------  ----------------------------  ------------------------------------  ---------------------  -------
DONE     test_sp_20251226_141434_r1_1  bd9268c3-512d-4191-99fa-6b3a46543029  None                test_sp_20251226_141434_r1_1  3515af1e-56b8-46e0-bb95-eebc2148dc0c  None                   None
```

**输出说明**

执行成功后，将显示任务详情。基础字段说明详见[创建单个 CDP 任务](#%E5%88%9B%E5%BB%BA%E5%8D%95%E4%B8%AA-cdp-%E4%BB%BB%E5%8A%A1)部分的输出说明。

若指定了 `--show_sync_point_tasks`，还将显示同步点任务信息：

- **CURRENT SYNC POINT TASK 字段说明**

  | 字段 | 说明 |
  | --- | --- |
  | `ID` | 本地快照 ID -> 远端快照 ID。 |
  | `Name` | 本地快照名称 -> 远端快照名称。 |
  | `Secondary ID` | 本地次要快照 ID -> 远端次要快照 ID。 |
- **SYNC POINT TASKS 列表字段说明**

  | 字段 | 说明 |
  | --- | --- |
  | `Stage` | 同步点任务阶段（如 `DONE`、`ERROR` 等）。 |
  | `Src Snapshot` | 本地快照名称。 |
  | `Src ID` | 本地快照 ID。 |
  | `Src Secondary ID` | 本地次要快照 ID。 |
  | `Remote Snapshot` | 远端快照名称。 |
  | `Remote ID` | 远端快照 ID。 |
  | `Remote Secondary ID` | 远端次要快照 ID。 |
  | `ERROR` | 错误信息。 |

### 查看本地任务详情

**操作方法**

在集群任一节点执行如下命令：

```
zbs-cdp job show_local <id> [options]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `id` | 任务 ID。 |
| `--chunk_ip <IP>` | 可选参数，指定 chunk 节点的 IP 地址。 |
| `--chunk_port <PORT>` | 可选参数，指定 chunk 节点的端口。 |
| `--show_sync_point_tasks` | 可选参数，显示该任务的同步点任务详情。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
zbs-cdp job show_local c0bb7d91-e74b-434c-98e2-00c57e8bb93f
-------------  ------------------------------------
Version        v2
ID             c0bb7d91-e74b-434c-98e2-00c57e8bb93f
Group          cdp-test
Stage          MIRROR
Compress       False
No Full Copy   False
CID            1
Local volume   babbe516-4b44-4651-a0a5-eeb36a6a6e0d
Remote volume  0b5cb6fc-11cf-4770-8109-28d3435c03b5
Remote Addr    10.88.67.95:10201:10206
ERROR          None
-------------  ------------------------------------

------------------  ----------
Total Read          10.00 GB
Total Write         8.50 GB
Total Read Latency  150.00 ms
Total Write Latency 120.00 ms
Total Read Times    1024
Total Write Times   800
Avg Read Latency    0.15 ms
Avg Write Latency   0.15 ms
Read Throughput     100.00 MB/s
Write Throughput    85.00 MB/s
------------------  ----------
```

**输出说明**

执行成功后，将显示本地任务详情及性能统计信息。

基础字段说明详见[创建单个 CDP 任务](#%E5%88%9B%E5%BB%BA%E5%8D%95%E4%B8%AA-cdp-%E4%BB%BB%E5%8A%A1)部分的输出说明。

性能统计字段说明如下：

| 字段 | 说明 |
| --- | --- |
| `Total Read` | 总读取数据量。 |
| `Total Write` | 总写入数据量。 |
| `Total Read Latency` | 总读取延迟。 |
| `Total Write Latency` | 总写入延迟。 |
| `Total Read Times` | 总读取次数。 |
| `Total Write Times` | 总写入次数。 |
| `Avg Read Latency` | 平均读取延迟。 |
| `Avg Write Latency` | 平均写入延迟。 |
| `Read Throughput` | 读取吞吐量。 |
| `Write Throughput` | 写入吞吐量。 |

---

## 管理 CDP 任务 > 修改 CDP 任务模式

# 修改 CDP 任务模式

支持在 Tracking Only（仅追踪）和 Normal（正常同步）模式间切换。

- Tracking Only 模式下仅记录脏块，不进行数据复制。
- Normal 模式下会进行正常的数据复制。

## 切换至 Tracking Only 模式

### 切换单个 CDP 任务至 Tracking Only 模式

**操作方法**

- 通过任务 ID 切换：

  ```
  zbs-cdp job enter_tracking_only <id> [options]
  ```
- 通过本地卷 ID 切换：

  ```
  zbs-cdp job enter_tracking_only_by_volume <volume_id> [options]
  ```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `id` | 任务 ID。 |
| `volume_id` | 本地存储卷 ID。 |
| `--sync` / `--no-sync` | 可选参数，是否同步等待任务切换，默认为 `True`。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
zbs-cdp job enter_tracking_only c0bb7d91-e74b-434c-98e2-00c57e8bb93f
```

**输出说明**

执行成功后无输出。

### 批量切换至 Tracking Only 模式

**操作方法**

在集群任一节点执行如下命令：

```
zbs-cdp job enter_tracking_only_by_group <group> [options]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `group` | CDP 任务组名称。 |
| `--sync` / `--no-sync` | 可选参数，是否同步等待任务组切换，默认为 `True`。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
zbs-cdp job enter_tracking_only c0bb7d91-e74b-434c-98e2-00c57e8bb93f
```

**输出说明**

执行成功后无输出。

## 退出 Tracking Only 模式

退出 Tracking Only 模式即切换至 Normal 模式，即恢复正常的数据复制。

## 单个 CDP 任务退出 Tracking Only 模式

**操作方法**

- 通过任务 ID 退出：

  ```
  zbs-cdp job exit_tracking_only <id> [options]
  ```
- 通过本地卷 ID 退出：

  ```
  zbs-cdp job exit_tracking_only_by_volume <volume_id> [options]
  ```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `id` | 任务 ID。 |
| `volume_id` | 本地存储卷 ID。 |
| `--sync` / `--no-sync` | 可选参数，是否同步等待任务退出，默认为 `True`。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
zbs-cdp job exit_tracking_only c0bb7d91-e74b-434c-98e2-00c57e8bb93f
```

**输出说明**

执行成功后无输出。

## 批量退出 Tracking Only 模式

批量退出 Tracking Only 模式即设置 CDP 任务组中所有 CDP 任务均退出 Tracking Only 模式。

**操作方法**

在集群任一节点执行如下命令：

```
zbs-cdp job exit_tracking_only_by_group <group> [options]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `group` | CDP 任务组名称。 |
| `--sync` / `--no-sync` | 可选参数，是否同步等待任务组退出，默认为 `True`。 |
| `-v` / `--version <VER>` | 可选参数，CDP 协议版本（`v1` 或 `v2`）。 |

**输出示例**

```
zbs-cdp job exit_tracking_only c0bb7d91-e74b-434c-98e2-00c57e8bb93f
```

**输出说明**

执行成功后无输出。

---

## 管理 CDP 任务 > 创建同步点快照

# 创建同步点快照

在存储卷开启 CDP 的情况下，可以创建同步点快照，此时将在本地和远端集群中同时创建一个协调一致的快照。

## 创建单个同步点快照

### Meta

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta snapshot create <pool_name> <volume_name> <snapshot_name> --as_cdp_sync_point [options]
```

**输出示例**

```
zbs-meta snapshot create pool1 vol1 snap1 --as_cdp_sync_point
```

**输出说明**

执行成功后，将返回新创建的快照信息。

### iSCSI

**操作方法**

在集群任一节点执行如下命令：

```
zbs-iscsi snapshot create <target_name> <lun_id> <snapshot_name> --as_cdp_sync_point [options]
```

**输出示例**

```
zbs-iscsi snapshot create target1 1 snap1 --as_cdp_sync_point
```

**输出说明**

执行成功后，将返回新创建的快照信息。

## 批量创建同步点快照 (Meta)

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta snapshot batch_create --volumes <VOLUMES> --as_cdp_sync_point
```

**输出示例**

```
zbs-meta snapshot batch_create --volumes pool1/vol1:snap1,pool1/vol2:snap2 --as_cdp_sync_point
```

**输出说明**

执行成功后，将列出所有成功创建的同步点快照信息。

---

## 管理 CDP 任务 > 管理脏页面追踪

# 管理脏页面追踪

本节提供用于测试目的的脏页面追踪（Dirty Block Tracing）的命令。

## 启动脏页面追踪

**操作方法**

在集群任一节点执行如下命令：

```
zbs-cdp dirty-trace start <volume_id> [options]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `volume_id` | 本地存储卷 ID。 |
| `--chunk_ip <IP>` | 可选参数，指定 chunk 节点的 IP 地址。 |
| `--chunk_port <PORT>` | 可选参数，指定 chunk 节点的端口。 |

**输出示例**

```
zbs-cdp dirty-trace start be09dd2c-325d-406c-b772-bcb36d3991fd
```

**输出说明**

执行成功无输出。

## 停止脏页面追踪

**操作方法**

在集群任一节点执行如下命令：

```
zbs-cdp dirty-trace stop <volume_id> [options]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `volume_id` | 本地存储卷 ID。 |
| `--chunk_ip <IP>` | 可选参数，指定 chunk 节点的 IP 地址。 |
| `--chunk_port <PORT>` | 可选参数，指定 chunk 节点的端口。 |

**输出示例**

```
zbs-cdp dirty-trace stop be09dd2c-325d-406c-b772-bcb36d3991fd
```

**输出说明**

执行成功无输出。

## 查看脏页面信息

**操作方法**

在集群任一节点执行如下命令：

```
zbs-cdp dirty-trace show <volume_id> [options]
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `volume_id` | 本地存储卷 ID。 |
| `--chunk_ip <IP>` | 可选参数，指定 chunk 节点的 IP 地址。 |
| `--chunk_port <PORT>` | 可选参数，指定 chunk 节点的端口。 |
| `--dry_run` / `--no_dry_run` | 可选参数。默认为 `--dry_run`，表示不清理缓存的脏块；设置为`--no_dry_run` 表示清理。 |
| `--show_details` | 可选参数，显示所有块的详细信息，默认不显示。 |

**输出示例**

```
zbs-cdp dirty-trace show be09dd2c-325d-406c-b772-bcb36d3991fd
total: 13
```

或显示详细信息

```
zbs-cdp dirty-trace show be09dd2c-325d-406c-b772-bcb36d3991fd --show_details
total: 13
[0, 1, 2, 3, 20, 21, 22, 28, 86, 87, 88, 89, 99]
```

**输出说明**

执行成功后，将显示脏页面统计信息。

| 字段 | 说明 |
| --- | --- |
| `total` | 脏块的总数。 |
| `[...]` | 若指定了 `--show_details`，将列出所有脏块的索引列表。 |

---

## 采集集群的性能数据

# 采集集群的性能数据

SMTX OS 提供了全路径 I/O 性能分析工具 `zbs-perf-tools`，可采集集群的性能数据，帮助工程师感知集群的整体负载情况和延时分布，从而定位出偶发的性能延时出现的原因，同时帮助工程师判断集群的网络或者物理盘是否存在问题，指明问题的排查方向。

---

## 采集集群的性能数据 > 实时采集并分析整个集群的 I/O 性能数据

# 实时采集并分析整个集群的 I/O 性能数据

**操作方法**

在集群任一节点执行如下命令，将会创建一个 live session，同时开始采集 chunk 服务数据并且实时输出结果到控制台，支持如下两种输出格式：

- text：直接输出解析后的 trace 日志。
- io\_pattern ：按秒统计每个 I/O size 的 I/O 累计数量，并且输出 top 20 的值。

`zbs-perf-tools trace live_trace [--trace_time <time>] [--output_type <type>]`

| 参数 | 说明 |
| --- | --- |
| `--trace_time <time>` | 数据采集时长，默认值为 `10s`，最大值为 `600s`。 |
| `--output_type <type>` | 输出类型，可选 `text` 或 `io_pattern`，默认值为 `text`。 |

键入 `ctrl + c` 组合键即可停止数据采集。

**输出示例**

```
$zbs-perf-tools  trace live_trace
live session started...
[17:43:45.136861534] (+?.?????????) zbs17-73 chunk:zbs_client_io_size: { cpu_id = 2 }, { volume_id = 0x55C2E2ABED40, op = 5, len = 12288, offset = 10548602003456 }
[17:43:45.136958065] (+0.000096531) zbs17-73 chunk:zbs_client_io_size: { cpu_id = 2 }, { volume_id = 0x55C2E2B597C0, op = 5, len = 12288, offset = 10548107517952 }
[17:43:45.137670669] (+0.000712604) zbs17-73 chunk:zbs_client_io_size: { cpu_id = 2 }, { volume_id = 0x55C2E2AC2540, op = 5, len = 8192, offset = 10659264245760 }
```

```
$zbs-perf-tools  trace live_trace --output_type io_pattern
timestamp:  2023-07-28 17:46:29.105326112 +0800 CST m=+9.508150252
IO PATTERN
------------------
  I/O SIZE  COUNT  
------------------
  4096     15038  
  512      3841   
  8192     3009   
  12288    844    
  16384    476    
  20480    220    
  49152    154    
  32768    152    
  24576    145    
  28672    138    
  40960    137    
  65536    132    
  2048     132    
  45056    102    
  36864    88     
  53248    72     
  1024     66     
  131072   62     
  57344    59     
  61440    41     
------------------
```

---

## 采集集群的性能数据 > 查看存储卷性能

# 查看存储卷性能

## 查看所有存储卷的性能信息

**操作方法**

在集群节点执行如下命令，查看所有存储卷的性能信息：

`zbs-perf-tools volume list [--chunk-addr <ip>] [--sort_by <sort_by>] [-A]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd RPC server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 chunk。 |
| `--sort_by <sort_by>` | 按照该字段对所有存储卷性能信息进行降序或升序排列，仅可指定 iops/bw/latency 类字段，默认为 `total_iops` |
| `-A, --ascending` | 按照 `sort_by` 字段升序排列所有存储卷的性能信息，不指定默认降序排列 |

**输出示例**

```
$ zbs-perf-tools volume list
---------------------------------------------------------------------
  volume_id                    dc656bde-8095-4a58-938b-00018a951190
  read_iops                    601.00
  read_avgrq                   262.14 KB(256.00 KiB)
  read_bw                      157.55 MB/s(150.25 MiB/s)
  read_latency                 242.12 US
  splited_read_iops            601.00
  splited_read_latency         208.46 US
  splited_local_read_ratio     1.00 (601.00 / 601.00)
  splited_local_read_bw        157.55 MB/s(150.25 MiB/s)
  splited_local_read_latency   208.46 US
  write_iops                   0.00
  write_avgrq                  0.00 B(0.00 B)
  write_bw                     0.00 B/s(0.00 B/s)
  write_latency                0.00 NS
  splited_write_iops           0.00
  splited_write_latency        0.00 NS
  splited_local_write_ratio    0.00
  splited_local_write_bw       0.00 B/s(0.00 B/s)
  splited_local_write_latency  0.00 NS
  total_iops                   601.00
  total_avgrq                  262.14 KB(256.00 KiB)
  total_bw                     157.55 MB/s(150.25 MiB/s)
  total_latency                242.12 US
  total_iop30s                 18011.00
  unmap_iops                   0.00
  unmap_total                  0
  unmap_unaligned_iops         0.00
  unmap_unaligned_total        0
---------------------------------------------------------------------
---------------------------------------------------------------------
  volume_id                    ae12b673-8bca-4118-a9b3-45db8f60f945
  read_iops                    0.00
  read_avgrq                   0.00 B(0.00 B)
  read_bw                      0.00 B/s(0.00 B/s)
  read_latency                 0.00 NS
  splited_read_iops            0.00
  splited_read_latency         0.00 NS
  splited_local_read_ratio     0.00
  splited_local_read_bw        0.00 B/s(0.00 B/s)
  splited_local_read_latency   0.00 NS
  write_iops                   601.00
  write_avgrq                  262.14 KB(256.00 KiB)
  write_bw                     157.55 MB/s(150.25 MiB/s)
  write_latency                108.41 US
  splited_write_iops           601.00
  splited_write_latency        76.36 US
  splited_local_write_ratio    1.00 (601.00 / 601.00)
  splited_local_write_bw       157.55 MB/s(150.25 MiB/s)
  splited_local_write_latency  76.36 US
  total_iops                   601.00
  total_avgrq                  262.14 KB(256.00 KiB)
  total_bw                     157.55 MB/s(150.25 MiB/s)
  total_latency                108.41 US
  total_iop30s                 18008.00
  unmap_iops                   0.00
  unmap_total                  0
  unmap_unaligned_iops         0.00
  unmap_unaligned_total        0
---------------------------------------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `read_iops` | 最近 1s 内读 IOPS。 |
| `read_avgrq` | 最近 1s 内读请求平均大小。 |
| `read_bw` | 最近 1s 内读带宽。 |
| `read_latency` | 最近 1s 内读请求平均延时。 |
| `splited_read_iops` | 最近 1s 内拆分后的读 IOPS。当条带大小为 256 KiB 时，512 KiB 的读请求会被拆分成两个 256 KiB 大小的请求下发给 access。 |
| `splited_read_latency` | 最近 1s 内拆分后的读请求平均延时。 |
| `splited_local_read_ratio` | 最近 1s 内拆分后的读请求下发给本地 access 的 IOPS 比例。 |
| `splited_local_read_bw` | 最近 1s 内拆分后的下发给本地 access 的读带宽。 |
| `splited_local_read_latency` | 最近 1s 内拆分后的读请求下发给本地 access 的平均延时。 |
| `write_iops` | 最近 1s 内写 IOPS。 |
| `write_avgrq` | 最近 1s 内写请求平均大小。 |
| `write_bw` | 最近 1s 内写带宽。 |
| `write_latency` | 最近 1s 内写请求平均延时。 |
| `splited_write_iops` | 最近 1s 内拆分后的写 IOPS。当条带大小为 256 KiB 时，512 KiB 的写请求会被拆分成两个 256 KiB 大小的请求下发给 access。 |
| `splited_write_latency` | 最近 1s 内拆分后的写请求平均延时。 |
| `splited_local_write_ratio` | 最近 1s 内拆分后的写请求下发给本地 access 的 IOPS 比例。 |
| `splited_local_write_bw` | 最近 1s 内拆分后的下发给本地 access 的写带宽。 |
| `splited_local_write_latency` | 最近 1s 内拆分后的写请求下发给本地 access 的平均延时。 |
| `total_iops` | 最近 1s 内 IOPS。 |
| `total_avgrq` | 最近 1s 内请求平均大小。 |
| `total_bw` | 最近 1s 内带宽。 |
| `total_latency` | 最近 1s 内平均延时。 |
| `total_iop30s` | 最近 30s 内 I/O 次数。 |
| `unmap_iops` | 最近 1s 内 UNMAP 指令 I/O 次数。 |
| `unmap_total` | UNMAP 指令的总 I/O 次数。 |
| `unmap_unaligned_iops` | 最近 1s 内非对齐 UNMAP 指令 I/O 次数。 |
| `unmap_unaligned_total` | 非对齐 UNMAP 指令的总 I/O 次数。 |

## 查看指定 ID 的存储卷的性能信息

**操作方法**

在集群节点执行如下命令，查看指定 ID 的存储卷的性能信息：

`zbs-perf-tools volume show <volume id> [--chunk-addr <ip>] [-L] [-A]`

| 参数 | 说明 |
| --- | --- |
| `volume id` | 存储卷 ID。 |
| `--chunk-addr <ip>` | zbs-chunkd RPC server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 chunk。 |
| `-L` | 仅展示本地 chunk 服务器的数据。 |
| `-A` | 展示图表的全部属性。 |

**输出示例**

```
$zbs-perf-tools volume show e5a1d376-7d14-4c44-82b4-f2bc2a2334ee
Aggregated Data:
---------------------------------------------------------------------
  volume_id                    f618b4b1-c0c9-4b93-8dc1-9ffdcd086679  
  read_iops                    0.00                                  
  read_avgrq                   0.00 B(0.00 B)                        
  read_bw                      0.00 B/s(0.00 B/s)                    
  read_latency                 0.00 NS                               
  splited_read_iops            0.00                                  
  splited_read_latency         0.00 NS                               
  splited_local_read_ratio     0.00                                  
  splited_local_read_bw        0.00 B/s(0.00 B/s)                    
  splited_local_read_latency   0.00 NS                               
  write_iops                   0.00                                  
  write_avgrq                  0.00 B(0.00 B)                        
  write_bw                     0.00 B/s(0.00 B/s)                    
  write_latency                0.00 NS                               
  splited_write_iops           0.00                                  
  splited_write_latency        0.00 NS                               
  splited_local_write_ratio    0.00                                  
  splited_local_write_bw       0.00 B/s(0.00 B/s)                    
  splited_local_write_latency  0.00 NS                               
  total_iops                   0.00                                  
  total_avgrq                  0.00 B(0.00 B)                        
  total_bw                     0.00 B/s(0.00 B/s)                    
  total_latency                0.00 NS                               
  total_iop30s                 0.00                                  
  unmap_iops                   0.00                                  
  unmap_total                  0                                     
  unmap_unaligned_iops         0.00                                  
  unmap_unaligned_total        0                                     
---------------------------------------------------------------------
chunk-Specific Data:
--------------------------------------------------------------------------------
  CHUNK IP       TOTAL IOPS  TOTAL AVGRQ     TOTAL BW            TOTAL LATENCY  
--------------------------------------------------------------------------------
  10.213.141.86  0.00        0.00 B(0.00 B)  0.00 B/s(0.00 B/s)  0.00 NS        
  10.213.141.88  0.00        0.00 B(0.00 B)  0.00 B/s(0.00 B/s)  0.00 NS        
  10.213.141.87  0.00        0.00 B(0.00 B)  0.00 B/s(0.00 B/s)  0.00 NS        
  10.213.141.89  0.00        0.00 B(0.00 B)  0.00 B/s(0.00 B/s)  0.00 NS        
--------------------------------------------------------------------------------
```

**输出说明**

`chunk-Specific Data` 为 chunk 级别数据，表示从集群中的所有 chunk 服务采集到的数据。

`Aggregated Data` 为聚合数据，表示从整个集群的全部 chunk 服务采集到的性能数据的综合结果，其中延时值和平均值是取加权平均值，计数值是取总和。

| 参数 | 说明 |
| --- | --- |
| `read_iops` | 最近 1s 内读 IOPS。 |
| `read_avgrq` | 最近 1s 内读请求平均大小。 |
| `read_bw` | 最近 1s 内读带宽。 |
| `read_latency` | 最近 1s 内读请求平均延时。 |
| `splited_read_iops` | 最近 1s 内拆分后的读 IOPS。当条带大小为 256 KiB 时，512 KiB 的读请求会被拆分成两个 256 KiB 大小的请求下发给 access。 |
| `splited_read_latency` | 最近 1s 内拆分后的读请求平均延时。 |
| `splited_local_read_ratio` | 最近 1s 内拆分后的读请求下发给本地 access 的 IOPS 比例。 |
| `splited_local_read_bw` | 最近 1s 内拆分后的下发给本地 access 的读带宽。 |
| `splited_local_read_latency` | 最近 1s 内拆分后的读请求下发给本地 access 的平均延时。 |
| `write_iops` | 最近 1s 内写 IOPS。 |
| `write_avgrq` | 最近 1s 内写请求平均大小。 |
| `write_bw` | 最近 1s 内写带宽。 |
| `write_latency` | 最近 1s 内写请求平均延时。 |
| `splited_write_iops` | 最近 1s 内拆分后的写 IOPS。当条带大小为 256 KiB 时，512 KiB 的写请求会被拆分成两个 256 KiB 大小的请求下发给 access。 |
| `splited_write_latency` | 最近 1s 内拆分后的写请求平均延时。 |
| `splited_local_write_ratio` | 最近 1s 内拆分后的写请求下发给本地 access 的 IOPS 比例。 |
| `splited_local_write_bw` | 最近 1s 内拆分后的下发给本地 access 的写带宽。 |
| `splited_local_write_latency` | 最近 1s 内拆分后的写请求下发给本地 access 的平均延时。 |
| `total_iops` | 最近 1s 内 IOPS。 |
| `total_avgrq` | 最近 1s 内请求平均大小。 |
| `total_bw` | 最近 1s 内带宽。 |
| `total_latency` | 最近 1s 内平均延时。 |
| `total_iop30s` | 最近 30s 内 I/O 次数。 |
| `unmap_iops` | 最近 1s 内 UNMAP 指令 I/O 次数。 |
| `unmap_total` | UNMAP 指令的总 I/O 次数。 |
| `unmap_unaligned_iops` | 最近 1s 内非对齐 UNMAP 指令 I/O 次数。 |
| `unmap_unaligned_total` | 非对齐 UNMAP 指令的总 I/O 次数。 |

## 探测存储卷的 I/O 延时分布、IO 请求大小分布和区域访问热度

通过设置存储卷的探测模式，可周期性探测存储卷的 I/O 延时分布，IO 请求大小分布和区域访问热度，并以直方图的方式呈现。

**操作方法**

在集群节点执行如下命令，开启指定的探测模式。按下 `ctrl + c` 可退出探测模式，命令退出后将自动清理 zbs-chunkd 探测模式相关的 metrics。

`zbs-perf-tools volume probe <volume id> [--chunk-addr <ip>] [--meta-addr <ip>] [--distribution {lat | rqsz | logical_offset}] [--interval <int>] [--readwrite {read | write | readwrite}]`

| 参数 | 说明 |
| --- | --- |
| `volume id` | ZBS 卷 ID。 |
| `--chunk-addr <ip>` | zbs-chunkd RPC server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 chunk。 |
| `--meta-addr <ip>` | zbs-meta RPC server 地址。可选参数，默认值为 `127.0.0.1:10206`。 |
| `--distribution` | I/O 分布类型，默认为 `lat`。`lat`：IO 延时分布；`rqsz`：IO 请求大小分布；`logical_offset`：逻辑区域访问热力分布。 |
| `--interval <int>` | 探测周期，即获取最近一段时内的分布信息。单位为秒，默认为 1 秒。 |
| `--readwrite` | 探测指定 I/O 类型的分布，可取 `read`, `write`,`readwrite`，默认为 `readwrite`。 |

**输出示例**

如果实际某个分布区间没有值，输出时会略过空的区间，比如延时都集中在 [0,64.00 us] 这个区间，而其他区间都是空的，则只输出 [0,64.00us] 区间。

- **探测存储卷的读写请求的延时分布**

  输出结果中，直方图第一列是延时区间（单位为 us），第二列为对应区间的计数，第三列为区间的分布情况。

  ```
  $zbs-perf-tools volume probe e5a1d376-7d144c44-82b4-f2bc2a2334ee --distribution lat
      readwrite lat(us)          : count     distribution
              [0,64.00)          : 57       |*                               |
          [64.00,128.00)         : 6172     |**********                      |
          [128.00,256.00)        : 15473    |*************************       |
          [256.00,512.00)        : 20443    |********************************|
          [512.00,1024.00)       : 10467    |*****************               |
          [1024.00,2048.00)      : 1361     |***                             |
          [2048.00,4096.00)      : 337      |*                               |
  ```
- **探测存储卷的 I/O 读写请求的大小分布**

  输出结果中，直方图第一列是 I/O 请求大小区间（单位为 KB），第二列为对应区间的计数，第三列为区间的分布情况。

  ```
  $zbs-perf-tools volume probe e5a1d376-7d14-4c44-82b4-f2bc2a2334ee --distribution rqsz
        readwrite size(KB)        : count     distribution
            [4.00,8.00)           : 71       |********************************|
            [16.00,32.00)         : 58       |***************************     |
            [256.00,512.00)       : 3        |**                              |
  ```
- **探测存储卷I/O 读写的区域热力分布**

  输出结果中，直方图第一列是 I/O 请求读写的区间（每 1 GB 为一个区间），第二列为对应区间的计数，第三列为区间的分布情况。

  ```
  $zbs-perf-tools volume probe e5a1d376-7d14-4c44-82b4-f2bc2a2334ee --distribution logical_offset
     readwrite logical offset(GB)    : count     distribution
             [0,1.00)                : 29248    |********************************|
            [1.00,2.00)              : 16579    |*******************             |
            [2.00,3.00)              : 16763    |*******************             |
            [3.00,4.00)              : 16320    |******************              |
  ```

## 采集并分析指定存储卷的 I/O 性能数据

**操作方法**

在集群任一节点执行如下命令，创建一个以存储卷 ID 命名的会话，同时开始采集数据。

`zbs-perf-tools trace volume <volume_id> --trace_time <time>`

| 参数 | 说明 |
| --- | --- |
| `volume_id` | 目标存储卷的 ID。 |
| `--trace_time <time>` | 数据采集时长，默认值为 `10s`，最大值为 `600s`。 |

键入 `ctrl + c` 组合键即可停止数据采集, 而后将会自动进行数据分析步骤。

数据分析的结果包括统计表和统计图两部分，其中统计表将会在控制台直接输出，统计图将会以静态 HTML 文件的形式在每个节点的 trace 数据的目录生成，其路径将会展示在控制台输出中，您可以将其下载到本地通过 Web 浏览器查看。

**输出示例**

```
$ zbs-perf-tools trace volume 5be99682-cdc9-4516-b262-3bfe44379207
session started...
Trace time is over, sending interrupt signal...
stopping tracing...
/root/zbs-trace/5be99682-cdc9-4516-b262-3bfe44379207/trace-data/cid-1-10-0-18-31 parse succeed. wrote to /root/zbs-trace/5be99682-cdc9-4516-b262-3bfe44379207/trace-data/cid-1-10-0-18-31/2023-07-28-165212+0800/parsed_data
/root/zbs-trace/5be99682-cdc9-4516-b262-3bfe44379207/trace-data/cid-2-10-0-18-34 parse succeed. wrote to /root/zbs-trace/5be99682-cdc9-4516-b262-3bfe44379207/trace-data/cid-2-10-0-18-34/2023-07-28-165211+0800/parsed_data
/root/zbs-trace/5be99682-cdc9-4516-b262-3bfe44379207/trace-data/cid-4-10-0-18-32 parse succeed. wrote to /root/zbs-trace/5be99682-cdc9-4516-b262-3bfe44379207/trace-data/cid-4-10-0-18-32/2023-07-28-165212+0800/parsed_data
The report of directory: /root/zbs-trace/5be99682-cdc9-4516-b262-3bfe44379207/trace-data/cid-1-10-0-18-31/2023-07-28-165212+0800/parsed_data
ACCESS
------------------------------------------------------------------------
                        AVG      P50      P95      P99      MAX      N  
------------------------------------------------------------------------
  read                  0.00 NS  0.00 NS  0.00 NS  0.00 NS  0.00 NS  0  
  write                 0.00 NS  0.00 NS  0.00 NS  0.00 NS  0.00 NS  0  
  readwrite             0.00 NS  0.00 NS  0.00 NS  0.00 NS  0.00 NS  0  
  sync_gen              0.00 NS  0.00 NS  0.00 NS  0.00 NS  0.00 NS  0  
  wait_recover          0.00 NS  0.00 NS  0.00 NS  0.00 NS  0.00 NS  0  
  caw                   0.00 NS  0.00 NS  0.00 NS  0.00 NS  0.00 NS  0  
  replica_io_read       0.00 NS  0.00 NS  0.00 NS  0.00 NS  0.00 NS  0  
  replica_io_write      0.00 NS  0.00 NS  0.00 NS  0.00 NS  0.00 NS  0  
  replica_io_readwrite  0.00 NS  0.00 NS  0.00 NS  0.00 NS  0.00 NS  0  
------------------------------------------------------------------------
……
```

---

## 采集集群的性能数据 > 查看 UIO/Access 统计信息

# 查看 UIO/Access 统计信息

UIO（User I/O）是用户侧发过来的 I/O。zbs\_client 负责将用户发过来的 I/O 请求转化成 ZBS 内部的 I/O 请求，并发往 I/O 请求对应的 extent 的 lease owner。用户可使用命令行查看 UIO 的统计信息。

**操作方法**

执行如下命令，查看节点的 UIO 统计信息：

`zbs-perf-tools chunk uio summary [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd RPC server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 chunk。 |

**输出示例**

```
$zbs-perf-tools chunk uio summary
---------------------------------------------------
  host                 127.0.0.1:10200
  instance_id          1
  total_iops           4852.00
  total_bw             403.66 MB/s(384.96 MiB/s)
  total_latency        230.05 US
  read_iops            885.00
  read_bw              146.32 MB/s(139.54 MiB/s)
  read_latency         172.73 US
  write_iops           3967.00
  write_bw             257.35 MB/s(245.42 MiB/s)
  write_latency        242.83 US
  local_io_ratio       1.00 (4852.00 / 4852.00)
  local_io_latency     230.05 US
  local_io_bw          403.66 MB/s(384.96 MiB/s)
  local_read_ratio     1.00 (885.00 / 885.00)
  local_read_latency   172.73 US
  local_read_bw        146.32 MB/s(139.54 MiB/s)
  local_write_ratio    1.00 (3967.00 / 3967.00)
  local_write_latency  242.83 US
  local_write_bw       257.35 MB/s(245.42 MiB/s)
  failed_io_ratio      0.00
  retry_io_ratio       0.00
  retry_queue_size     0
  active_extents       7630
  active_volumes       21
  waiting_queue_size   0
---------------------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `total_iops` | 最近 1s 内 zbs\_client 模块中总 IOPS。 |
| `total_bw` | 最近 1s 内 zbs\_client 模块的总带宽。 |
| `total_latency` | 最近 1s 内 zbs\_client 模块的总平均延时。 |
| `read_iops` | 最近 1s 内 zbs\_client 模块中读 IOPS。 |
| `read_bw` | 最近 1s 内 zbs\_client 模块的读带宽。 |
| `read_latency` | 最近 1s 内 zbs\_client 模块的读平均延时。 |
| `write_iops` | 最近 1s 内 zbs\_client 模块中写 IOPS。 |
| `write_bw` | 最近 1s 内 zbs\_client 模块的写带宽。 |
| `write_latency` | 最近 1s 内 zbs\_client 模块的写平均延时。 |
| `local_io_ratio` | 最近 1s 内发往本地 access 的 I/O 比例。 |
| `local_io_latency` | 最近 1s 内发往本地 access 的 I/O 平均延时。 |
| `local_io_bw` | 最近 1s 内发往本地 access 的 I/O 带宽。 |
| `local_read_ratio` | 最近 1s 内发往本地 access 的读 I/O 比例。 |
| `local_read_latency` | 最近 1s 内发往本地 access 的读 I/O 平均延时。 |
| `local_read_bw` | 最近 1s 内发往本地 access 的读 I/O 带宽。 |
| `local_write_ratio` | 最近 1s 内发往本地 access 的写 I/O 比例。 |
| `local_write_latency` | 最近 1s 内发往本地 access 的写 I/O 平均延时。 |
| `local_write_bw` | 最近 1s 内发往本地 access 的写 I/O 带宽。 |
| `failed_io_ratio` | 最近 1s 内失败的 I/O 比例。 |
| `retry_io_ratio` | 最近 1s 内重试 I/O 的比例。 |
| `retry_queue_size` | 当前重试队列大小。 |
| `active_extents` | 当前活跃的 extent 数量。 |
| `active_volumes` | 当前活跃的存储卷数量。 |
| `waiting_queue_size` | 当前等待队列大小。 |

> **说明**：
>
> 多物理盘池环境下，会展示每一个 chunk 的性能数据，若想查看整体性能数据可以执行 `zbs-perf-tools node uio summary`。

## 查看 access 模块的总体性能信息

**操作方法**

执行如下命令，查看 access 模块的总体性能信息：

`zbs-perf-tools chunk access summary [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd RPC server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 chunk。 |

**输出示例**

```
$ sudo zbs-perf-tools chunk access summary
----------------------------------------------------
  host                          127.0.0.1:10200     
  instance_id                   1
  read_iops                     0.00                
  read_latency                  0.00 NS             
  read_bw                       0.00 B/s(0.00 B/s)  
  write_iops                    0.00                
  write_latency                 0.00 NS             
  write_bw                      0.00 B/s(0.00 B/s)  
  total_iops                    0.00                
  total_latency                 0.00 NS             
  total_bw                      0.00 B/s(0.00 B/s)  
  io_hard_rate                  0.00                
  io_retry_rate                 0.00                
  io_timeout_rate               0.00                
  from_local_read_iops          0.00                
  from_local_read_latency       0.00 NS             
  from_local_read_bw            0.00 B/s(0.00 B/s)  
  from_local_write_iops         0.00                
  from_local_write_latency      0.00 NS             
  from_local_write_bw           0.00 B/s(0.00 B/s)  
  from_local_total_iops         0.00                
  from_local_total_latency      0.00 NS             
  from_local_total_bw           0.00 B/s(0.00 B/s)  
  from_local_throttle_latency   0.00 NS             
  from_remote_read_iops         0.00                
  from_remote_read_latency      0.00 NS             
  from_remote_read_bw           0.00 B/s(0.00 B/s)  
  from_remote_write_iops        0.00                
  from_remote_write_latency     0.00 NS             
  from_remote_write_bw          0.00 B/s(0.00 B/s)  
  from_remote_total_iops        0.00                
  from_remote_total_latency     0.00 NS             
  from_remote_total_bw          0.00 B/s(0.00 B/s)  
  from_remote_throttle_latency  0.00 NS             
----------------------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `read_iops` | 最近 1s 内 access 模块中读 IOPS。 |
| `read_latency` | 最近 1s 内 access 模块的读平均延时。 |
| `read_bw` | 最近 1s 内 access 模块的读带宽。 |
| `write_iops` | 最近 1s 内 access 模块中写 IOPS。 |
| `write_latency` | 最近 1s 内 access 模块的写平均延时。 |
| `write_bw` | 最近 1s 内 access 模块的写带宽。 |
| `total_iops` | 最近 1s 内 access 模块中总 IOPS。 |
| `total_latency` | 最近 1s 内 access 模块的总平均延时。 |
| `total_bw` | 最近 1s 内 access 模块的总带宽。 |
| `io_hard_rate` | 最近 1s 内 access 标记为 hard 的 I/O 次数，hard I/O 一般是由于 LSM 中有慢盘。 |
| `io_retry_rate` | 最近 1s 内 access 读重试次数。Access 读副本失败时会尝试读取下一个副本。 |
| `io_timeout_rate` | 最近 1s 内发往本地 access I/O 超时次数。 |
| `from_local_read_iops` | 最近 1s access 处理本地发来的读 IOPS。 |
| `from_local_read_latency` | 最近 1s access 处理本地发来的读平均延时。 |
| `from_local_read_bw` | 最近 1s access 处理本地发来的读带宽。 |
| `from_local_write_iops` | 最近 1s access 处理本地发来的写 IOPS。 |
| `from_local_write_latency` | 最近 1s access 处理本地发来的写平均延时。 |
| `from_local_write_bw` | 最近 1s access 处理本地发来的写带宽。 |
| `from_local_total_iops` | 最近 1s access 处理本地发来的总 IOPS。 |
| `from_local_total_latency` | 最近 1s access 处理本地发来的总平均延时。 |
| `from_local_total_bw` | 最近 1s access 处理本地发来的总带宽。 |
| `from_local_throttle_latency` | 最近 1s 内 access 处理本地发来的被限流的 I/O 的平均延时。 |
| `from_remote_read_iops` | 最近 1s access 处理其他 access 发来的读 IOPS。 |
| `from_remote_read_latency` | 最近 1s access 处理其他 access 发来的读平均延时。 |
| `from_remote_read_bw` | 最近 1s access 处理其他 access 发来的读带宽。 |
| `from_remote_write_iops` | 最近 1s access 处理其他 access 发来的写 IOPS。 |
| `from_remote_write_latency` | 最近 1s access 处理其他 access 发来的写平均延时。 |
| `from_remote_write_bw` | 最近 1s access 处理其他 access 发来的写带宽。 |
| `from_remote_total_iops` | 最近 1s access 处理其他 access 发来的总 IOPS。 |
| `from_remote_total_latency` | 最近 1s access 处理其他 access 发来的总平均延时。 |
| `from_remote_total_bw` | 最近 1s access 处理其他 access 发来的总带宽。 |
| `from_remote_throttle_latency` | 最近 1s 内 access 处理其他 access 发来的被限流的 I/O 的平均延时。 |

> **说明**：
>
> 多物理盘池环境下，会展示每一个 chunk 的性能数据，若想查看整体性能数据可以执行 `zbs-perf-tools node access summary`。

## 查看当前 access 模块的副本 I/O 流向和基本统计信息

**操作方法**

执行如下命令，查看当前 access 的副本 I/O 流向和基本统计信息：

`zbs-perf-tools chunk access replica_io [--chunk-addr <ip>] [-d]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd RPC server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 chunk。 |
| `-d` | 目的 chunk ID，数组类型参数，简称 cid。输入该参数后仅输出目的 chunk 的数据。 |

**输出示例**

```
$zbs-perf-tools chunk access replica_io -d 1 -d 2
  DIRECTION  READ IOPS  READ LATENCY  READ BW             WRITE IOPS  WRITE LATENCY  WRITE BW               TOTAL IOPS  TOTAL LATENCY  TOTAL BW               
--------------------------------------------------------------------------------------------------------------------------------------------------------------
   1 -> 3      0.00       0.00 NS     0.00 B/s(0.00 B/s)    129.00      324.91 US    1.13 MB/s(1.08 MiB/s)    129.00      324.91 US    1.13 MB/s(1.08 MiB/s)  
   1 -> 2      0.00       0.00 NS     0.00 B/s(0.00 B/s)    188.00      166.46 US    2.37 MB/s(2.26 MiB/s)    188.00      166.46 US    2.37 MB/s(2.26 MiB/s)  
   1 -> 1      0.00       0.00 NS     0.00 B/s(0.00 B/s)    209.00      141.29 US    2.49 MB/s(2.38 MiB/s)    209.00      141.29 US    2.49 MB/s(2.38 MiB/s)
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `DIRECTION` | 副本 I/O 流向。 |
| `READ IOPS` | 最近 1s 内读 IOPS。 |
| `READ LATENCY` | 最近 1s 内读平均延时。 |
| `READ BW` | 最近 1s 内读带宽。 |
| `WRITE IOPS` | 最近 1s 内写 IOPS。 |
| `WRITE LATENCY` | 最近 1s 内写平均延时。 |
| `WRITE BW` | 最近 1s 内写带宽。 |
| `TOTAL IOPS` | 最近 1s 内总 IOPS。 |
| `TOTAL LATENCY` | 最近 1s 内总平均延时。 |
| `TOTAL BW` | 最近 1s 内总带宽。 |

---

## 采集集群的性能数据 > 查看 LSM2 模块性能

# 查看 LSM2 模块性能

LSM2 管理磁盘和 extent 等元数据，元数据存储在 LSM2 DB 中。LSM2 负责将 access 发来的副本 I/O 落盘。在 LSM2 中，SSD 通常用作缓存盘和 Journal 盘，HDD 用做数据盘（全闪情况下，数据盘全为 SSD，没有缓存盘），一次写请求需要将元数据的更新和数据写入 Journal 盘 (部分情况不需要将数据写入 journal) , 然后写入到缓存盘或者数据盘中，即是说一次 I/O 请求可能涉及到 LSM2 DB，Journal 分区，缓存分区，数据分区。

此部分命令行从 LSM2 获取 LSM2 的整体数据，以及 LSM2 DB，Journal 分区，缓存分区，数据分区等分区的性能数据并展示。

## 查看 LSM 模块的总体性能信息

**操作方法**

执行如下命令，查看 LSM 的总体性能信息：

`zbs-perf-tools chunk lsm summary [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd RPC server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 chunk。 |

**输出示例**

```
$zbs-perf-tools chunk lsm summary
--------------------------------------
  instance_id              1
  read_iops                0.00                   
  read_bw                  0.00 B/s(0.00 B/s)     
  read_latency             0.00 NS                
  read_cache_hit           1.00                   
  write_iops               239.00                 
  write_bw                 2.67 MB/s(2.55 MiB/s)  
  write_latency            143.72 US              
  write_cache_hit          1.00                   
  total_iops               239.00                 
  total_bw                 2.67 MB/s(2.55 MiB/s)  
  total_latency            143.72 US              
  total_cache_hit          1.00                   
  failed_io_ratio          0.00                   
  hard_io_ratio            0.00                   
  slow_io_ratio            0.00                   
  throttle_latency         0.00 NS                
  cache_promotion_rate     0.00                   
  cache_promotion_bw       0.00 B/s(0.00 B/s)     
  cache_writeback_rate     0.00                   
  cache_writeback_bw       0.00 B/s(0.00 B/s)     
  journal_reclaim_rate     1.00                   
  journal_reclaim_latency  8.74 MS  
--------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `total_iops` | 最近 1s 内 LSM 模块中总 IOPS。 |
| `total_bw` | 最近 1s 内 LSM 模块的总带宽。 |
| `total_latency` | 最近 1s 内 LSM 模块的总平均延时。 |
| `total_cache_hit` | 最近 1s 内 LSM 模块的总缓存命中率。 |
| `read_iops` | 最近 1s 内 LSM 模块中读 IOPS。 |
| `read_bw` | 最近 1s 内 LSM 模块的读带宽。 |
| `read_latency` | 最近 1s 内 LSM 模块的读平均延时。 |
| `read_cache_hit` | 最近 1s 内 LSM 模块的读缓存命中率。 |
| `write_iops` | 最近 1s 内 LSM 模块中写 IOPS。 |
| `write_bw` | 最近 1s 内 LSM 模块的写带宽。 |
| `write_latency` | 最近 1s 内 LSM 模块的写平均延时。 |
| `write_cache_hit` | 最近 1s 内 LSM 模块的写缓存命中率。 |
| `failed_io_ratio` | 最近 1s 内 LSM 模块的 I/O 失败率。 |
| `hard_io_ratio` | 最近 1s 内 LSM 模块的 hard I/O 比例。 |
| `slow_io_ratio` | 最近 1s 内 LSM 模块的 slow I/O 比例。 |
| `throttle_latency` | 最近 1s 内 LSM 模块处理 I/O 的 throttle 延时。 |
| `cache_promotion_rate` | 最近 1s 内 LSM 从数据分区写到缓存分区的 IOPS。 |
| `cache_promotion_bw` | 最近 1s 内 LSM 从数据分区写到缓存分区的带宽。 |
| `cache_writeback_rate` | 最近 1s 内 LSM 从缓存分区写回数据分区的 IOPS。 |
| `cache_writeback_bw` | 最近 1s 内 LSM 从缓存分区写到数据分区的带宽。 |
| `journal_reclaim_rate` | 最近 1s 内 LSM Journal 分区回收速度。 |
| `journal_reclaim_latency` | 最近 1s 内 LSM Journal 分区回收延时。 |

> **说明**：
>
> 多物理盘池环境下，会展示每一个 chunk 的性能数据，若想查看整体性能数据可以执行 `zbs-perf-tools node lsm summary`。

## 查看 LSM DB 的性能信息

**操作方法**

执行如下命令，查看 LSM DB 的性能信息：

`zbs-perf-tools chunk lsm db [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd RPC server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 chunk。 |

**输出示例**

```
$zbs-perf-tools chunk lsm db
--------------------------------------
  OP      RATE  LATENCY  MAX LATENCY
--------------------------------------
  GET     0.00  0.00 NS  0.00 NS
  PUT     0.00  0.00 NS  0.00 NS
  DELETE  0.00  0.00 NS  113.39 US
  WRITE   1.00  2.68 MS  3.19 MS
--------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `OP` | LSM DB 操作。 |
| `RATE` | 最近 1s DB 操作次数。 |
| `LATENCY` | 最近 1s DB 操作平均延时。 |
| `MAX LATENCY` | 最近 30s DB 操作的最大延时。 |

## 查看 LSM Journal 分区的性能信息

**操作方法**

执行如下命令，查看 LSM Journal 分区的性能信息：

`zbs-perf-tools chunk lsm journal [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd RPC server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 chunk。 |

**输出示例**

```
$zbs-perf-tools chunk lsm journal
  path                /dev/sdf3
  commit_rate         0.00
  commit_bw           0.00 B/s(0.00 B/s)
  commit_latency      0.00 NS
  max_commit_latency  0.00 NS
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `PATH` | Journal 分区。 |
| `COMMIT RATE` | 最近 1s commit 次数。 |
| `COMMIT BW` | 最近 1s commit 带宽。 |
| `COMMIT LATENCY` | 最近 1s commit 平均延时。 |
| `MAX COMMIT LATENCY` | 最近 30s commit 最大延时。 |

## 查看 LSM 缓存分区的性能信息

**操作方法**

执行如下命令，查看 LSM 缓存分区的性能信息：

`zbs-perf-tools chunk lsm cache [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd RPC server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 chunk。 |

**输出示例**

```
$zbs-perf-tools chunk lsm cache
 path           /dev/sdf4
  r/s            0.00
  read_bw        0.00 B/s(0.00 B/s)
  read_lat       0.00 NS
  read_max_lat   0.00 NS
  w/s            0.00
  write_bw       0.00 B/s(0.00 B/s)
  write_lat      0.00 NS
  write_max_lat  0.00 NS
  sync/s         0.00
  sync_lat       0.00 NS
  sync_max_lat   0.00 NS
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `PATH` | 缓存分区。 |
| `R/S` | 最近 1s 读 IOPS。 |
| `READ BW` | 最近 1s 的读 I/O 带宽。 |
| `READ LAT` | 最近 1s 的读 I/O 平均延时。 |
| `READ MAX LAT` | 最近 30s 的读 I/O 最大延时。 |
| `W/S` | 最近 1s 的写 IOPS。 |
| `WRITE BW` | 最近 1s 的写 I/O 带宽。 |
| `WRITE LAT` | 最近 1s 的写 I/O 平均延时。 |
| `WRITE MAX LAT` | 最近 30s 的写 I/O 最大延时。 |
| `SYNC/S` | 最近 1s 的 sync 次数。 |
| `SYNC LAT` | 最近 1s 的 sync 平均延时。 |
| `SYNC MAX LAT` | 最近 30s 的 sync 最大延时。 |

## 查看 LSM 数据分区的性能信息

**操作方法**

执行如下命令，查看 LSM 数据分区的性能信息：

`zbs-perf-tools chunk lsm partition [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd RPC server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 chunk。 |

**输出示例**

```
$zbs-perf-tools chunk lsm  partition
  PATH       R/S    READ BW                READ LAT  READ MAX LAT  W/S   WRITE BW            WRITE LAT  WRITE MAX LAT  SYNC/S  SYNC LAT  SYNC MAX LAT  
-------------------------------------------------------------------------------------------------------------------------------------------------------
  /dev/sdb1  18.00  4.72 MB/s(4.50 MiB/s)  7.88 MS   17.95 MS      0.00  0.00 B/s(0.00 B/s)  0.00 NS    0.00 NS        0.00    0.00 NS   0.00 NS       
  /dev/sdc1  18.00  4.72 MB/s(4.50 MiB/s)  5.59 MS   12.85 MS      0.00  0.00 B/s(0.00 B/s)  0.00 NS    0.00 NS        0.00    0.00 NS   0.00 NS       
  /dev/sdd1  18.00  4.72 MB/s(4.50 MiB/s)  4.20 MS   9.42 MS       0.00  0.00 B/s(0.00 B/s)  0.00 NS    0.00 NS        0.00    0.00 NS   0.00 NS       
  /dev/sde1  18.00  4.72 MB/s(4.50 MiB/s)  7.77 MS   15.62 MS      0.00  0.00 B/s(0.00 B/s)  0.00 NS    0.00 NS        0.00    0.00 NS   0.00 NS
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `PATH` | 数据分区。 |
| `R/S` | 最近 1s 的读 IOPS。 |
| `READ BW` | 最近 1s 的读 I/O 带宽。 |
| `READ LAT` | 最近 1s 的读 I/O 平均延时。 |
| `READ MAX LAT` | 最近 30s 的读 I/O 最大延时。 |
| `W/S` | 最近 1s 的写 IOPS。 |
| `WRITE BW` | 最近 1s 的写 I/O 带宽。 |
| `WRITE LAT` | 最近 1s 的写 I/O 平均延时。 |
| `WRITE MAX LAT` | 最近 30s 的写 I/O 最大延时。 |
| `SYNC/S` | 最近 1s 的 sync 次数。 |
| `SYNC LAT` | 最近 1s 的 sync 平均延时。 |
| `SYNC MAX LAT` | 最近 30s 的 sync 最大延时。 |

---

## 采集集群的性能数据 > 采集并分析指定 target 的 I/O 性能数据

# 采集并分析指定 target 的 I/O 性能数据

## 创建会话

**操作方法**

在集群任一节点执行如下命令创建指定名称的会话。

`zbs-perf-tools trace session create [--session <session_name>]`

| 参数 | 说明 |
| --- | --- |
| `--session <session_name>` | 会话名称。 |

执行命令后，在 `/root/zbs-trace/` 目录下会生成以会话名称命名的文件夹。

**输出说明**

执行成功无输出。

## 查看已创建的会话

**操作方法**

在集群任一节点执行如下命令，查看当前已创建的会话。

`zbs-perf-tools trace session list`

**输出示例**

```
------------------
  name     session1
  started  false
------------------
```

## 将 Target 添加到会话中

**操作方法**

在集群任一节点进入 `/root/zbs-trace/<session name>` 目录执行如下命令，将 target 添加到会话中：

`zbs-perf-tools trace session add-target <TARGET NAME> <TARGET HOST> [--event]`

| 参数 | 说明 |
| --- | --- |
| `TARGET NAME` | Target 名称。同一个会话中的 target 名称不可重复。 |
| `TARGET HOST` | Target 所在节点的 IP。 |
| `--event` | 数组类型参数，待追踪的事件名称，目前支持 `zbs_client:*`，`access:*` 和 `lsm2:*`。 |

**输出说明**

执行成功无输出。

## 使用 JSON 文件添加多个 target

采集一个指定卷的数据时，可以通过使用 JSON 文件来添加多个 target。

**操作方法**

在集群任一节点进入 `/root/zbs-trace/<session name>` 目录执行如下命令：

`zbs-perf-tools trace session add-target --from-json <JSON FILE>`

| 参数 | 说明 |
| --- | --- |
| `--from-json` | 表示从 JSON 文件添加 target。 |
| `JSON FILE` | JSON 文件名。 |

**输出说明**

执行成功无输出。

## 更新会话的 target

**操作方法**

在集群任一节点进入 `/root/zbs-trace/<session name>` 目录执行如下命令，更新会话的 target：

`zbs-perf-tools trace session update-target <TARGET NAME> [--remove-event <stringArray>] [--add-event <stringArray>]`

| 参数 | 说明 |
| --- | --- |
| `--remove-event <stringArray>` | 数组类型，删除 event。 |
| `--add-event <stringArray>` | 数组类型，增加 event。 |

**输出说明**

执行成功无输出。

## 从会话中移除 target

**操作方法**

在集群任一节点进入 `/root/zbs-trace/<session name>` 目录执行如下命令，从会话中移除 target：

`zbs-perf-tools trace session remove-target <TARGET NAME>`

**输出说明**

执行成功无输出。

## 启动会话

**操作方法**

在集群任一节点进入 `/root/zbs-trace/<session name>` 目录执行如下命令，启动会话：

`zbs-perf-tools trace session start [-d]`

若指定 `-d` 该选项，会话将在后台启动。

停止会话后，将在 `/root/zbs-trace/<session name>/trace-data/` 目录下生成 target 的追踪数据。

**输出示例**

```
$zbs-perf-tools trace session start
session started...
```

## 销毁会话并清理数据

**操作方法**

在集群任一节点执行如下命令：

`zbs-perf-tools trace session destroy`

**输出说明**

执行成功无输出。

## 将采集到的性能数据输出到指定目录

**操作方法**

在集群任一节点执行如下命令，将采集到的性能数据输出到指定目录：

`zbs-perf-tools trace analyze parse <MODULE> <PATH> <OUTPUT DIR> [--time_begin] [--time_end] [--volume] [--slow_io_latency]`

| 参数 | 说明 |
| --- | --- |
| `MODULE` | 待解析的模块，可选 `client`，`access`，`lsm` 或 `all`，其中 `all` 代表所有模块。 |
| `PATH` | 追踪数据目录，需要指定到时间层级。 |
| `OUTPUT DIR` | 输出目录。 |
| `--time_begin` | 从指定时间开始解析。 |
| `--time_end` | 解析到某个时间，需要与 `--time_begin` 配合使用。 |
| `--volume` | 指定 `zbs-perf-tools volume gentrace [VOLUME ID]` 生成的 JSON 文件。 |
| `--slow_io_latency` | 将超过指定延时的 I/O 输出到 `[OUTPUT DIR]/[MODULE].slow_io` 文件。单位 ms，默认为 `200`。 |

**输出说明**

执行成功无输出。

## 查看 ZBS 各模块的数据分析结果

**操作方法**

在集群任一节点执行如下命令，查看 ZBS 各模块的性能数据分析结果：

`zbs-perf-tools trace analyze report <MODULE> <DIR>`

| 参数 | 说明 |
| --- | --- |
| `MODULE` | 待解析的模块，可选 `client`，`access`，`lsm` 或 `all`，其中 `all` 代表所有模块。 |
| `DIR` | 解析得到的数据目录。 |

**输出示例**

- **输出 Client 模块的数据分析**

  ```
  zbs-perf-tools trace analyze report client  cid-2
  CLIENT CID 2
  ---------------------------------------------------------------------------
    OP         AVG        P50        P95        P99       MAX       N
  ---------------------------------------------------------------------------
    read       416.10 US  280.58 US  544.77 US  11.60 MS  11.65 MS  82
    write      1.21 MS    544.77 US  6.13 MS    12.65 MS  87.86 MS  1378248
    readwrite  1.21 MS    544.77 US  6.13 MS    12.65 MS  87.86 MS  1378330
  ---------------------------------------------------------------------------
  TO LEASE OWNER
  -----------------------------------------------------------------------------------
    TO CID  OP         AVG        P50        P95        P99       MAX       N
  -----------------------------------------------------------------------------------
    2       read       416.10 US  280.58 US  544.77 US  11.60 MS  11.65 MS  82
            write      1.21 MS    544.77 US  6.13 MS    12.65 MS  87.86 MS  1378248
            readwrite  1.21 MS    544.77 US  6.13 MS    12.65 MS  87.86 MS  1378330
  -----------------------------------------------------------------------------------
  FAILED COUNT: 0.000000
  ```
- **输出 access 模块的数据分析**

  ```
  $zbs-perf-tools trace analyze report access  cid-2
  ACCESS
  ----------------------------------------------------------------------------------------
                          AVG        P50        P95        P99        MAX        N
  ----------------------------------------------------------------------------------------
    read                  422.59 US  244.74 US  561.15 US  11.47 MS   11.53 MS   88
    write                 1.21 MS    544.77 US  6.13 MS    12.52 MS   87.86 MS   1378249
    readwrite             1.21 MS    544.77 US  6.13 MS    12.52 MS   87.86 MS   1378337
    sync_gen              912.89 US  468.99 US  3.88 MS    6.91 MS    11.38 MS   239
    wait_recover          625.62 NS  540.00 NS  924.00 NS  1.18 US    429.49 US  1378629
    caw                   544.34 NS  490.00 NS  724.00 NS  900.00 NS  120.19 US  1378630
    replica_io_read       284.56 US  236.54 US  544.77 US  2.69 MS    2.69 MS    88
    replica_io_write      815.45 US  399.36 US  3.42 MS    10.29 MS   87.86 MS   2756640
    replica_io_readwrite  815.44 US  399.36 US  3.42 MS    10.29 MS   87.86 MS   2756728
  ----------------------------------------------------------------------------------------
  TO REPLICA
  -----------------------------------------------------------------------------------
    TO CID  OP         AVG        P50        P95        P99       MAX       N
  -----------------------------------------------------------------------------------
    1       read       0.00 NS    0.00 NS    0.00 NS    0.00 NS   0.00 NS   0
            write      1.19 MS    536.58 US  6.13 MS    12.52 MS  17.79 MS  1378241
            readwrite  1.19 MS    536.58 US  6.13 MS    12.52 MS  17.79 MS  1378241
    2       read       284.56 US  236.54 US  544.77 US  2.69 MS   2.69 MS   88
            write      443.16 US  264.19 US  1.66 MS    3.65 MS   87.86 MS  1378399
            readwrite  443.15 US  264.19 US  1.66 MS    3.65 MS   87.86 MS  1378487
  -----------------------------------------------------------------------------------
  ```
- **输出 LSM 模块的数据分析**

  ```
  $zbs-perf-tools trace analyze report lsm  cid-2
  LSM
  ---------------------------------------------------------------------------------------
                        AVG        P50        P95        P99        MAX        N
  ---------------------------------------------------------------------------------------
    read                 207.65 US  162.82 US  444.42 US  733.18 US  737.24 US  88
    write                276.36 US  234.50 US  468.99 US  626.69 US  87.98 MS   1380604
    readwrite            276.36 US  234.50 US  468.99 US  626.69 US  87.98 MS   1380692
    throttle             2.29 US    1.82 US    5.09 US    9.02 US    129.51 US  1380819
    lock_range           1.37 US    700.00 NS  2.22 US    5.86 US    10.46 MS   1380699
    reserve_journal      984.42 NS  764.00 NS  2.51 US    5.98 US    129.63 US  1380611
    tx_commit            206.83 US  175.10 US  399.36 US  528.38 US  87.85 MS   1380608
    cache_read           203.65 US  158.72 US  440.32 US  733.18 US  733.73 US  88
    cache_write          63.49 US   42.24 US   123.39 US  205.82 US  25.86 MS   1380604
    cache_readwrite      63.50 US   42.24 US   123.39 US  205.82 US  25.86 MS   1380692
    partition_read       0.00 NS    0.00 NS    0.00 NS    0.00 NS    0.00 NS    0
    partition_write      0.00 NS    0.00 NS    0.00 NS    0.00 NS    0.00 NS    0
    partition_readwrite  0.00 NS    0.00 NS    0.00 NS    0.00 NS    0.00 NS    0
  ---------------------------------------------------------------------------------------
  TX COMMIT
  --------------------------------------------------------------------------------
    PATH            AVG        P50        P95        P99        MAX       N
  --------------------------------------------------------------------------------
    /dev/sdc1       265.18 US  240.64 US  481.28 US  577.54 US  2.03 MS   414317
    /dev/nvme1n1p3  189.75 US  148.48 US  313.34 US  448.51 US  87.85 MS  438224
    /dev/nvme0n1p3  175.24 US  150.53 US  317.44 US  428.03 US  65.05 MS  528067
  --------------------------------------------------------------------------------
  CACHE
  --------------------------------------------------------------------------------------------
    PATH            OP         AVG        P50        P95        P99        MAX        N
  --------------------------------------------------------------------------------------------
    /dev/nvme0n1p4  read       237.58 US  203.78 US  432.13 US  460.80 US  462.31 US  26
                    write      57.98 US   42.24 US   122.37 US  195.58 US  19.65 MS   678635
                    readwrite  57.98 US   42.24 US   122.37 US  195.58 US  19.65 MS   678661
    /dev/nvme1n1p4  read       189.42 US  134.14 US  440.32 US  733.18 US  733.73 US  62
                    write      68.82 US   42.24 US   123.39 US  234.50 US  25.86 MS   701969
                    readwrite  68.83 US   42.24 US   123.39 US  234.50 US  25.86 MS   702031
  --------------------------------------------------------------------------------------------
  FAILED: 0
  COW PARERENT: 0
  PROMOTION BLOCK: 0
  RECOVER: 0
  SYNCGEN: 120
  READWRITE CACHE HIT RATIO: 1
  READ CACHE HIT RATIO: 1
  WRITE CACHE HIT RATIO: 1
  ```

## 查看成对的 event 之间的延时分布直方图

**操作方法**

在集群任一节点执行如下命令，输出成对的 event（一般为 I/O 的开始和结束的 event，或者连续两个 event）之间的延时分布直方图。

`zbs-perf-tools trace analyze latdist <TRACE DATA DIR> <TRACE_BEGIN> <TRACE_END> <TRACE_ID>`

| 参数 | 说明 |
| --- | --- |
| `TRACE DATA DIR` | 在会话开始的时创建的追踪数据目录。 |
| `TRACE_BEGIN` | 两个成对的 trace event 的第一个 trace event 的名称。 |
| `TRACE_END` | 两个成对的 trace event 的第二个 trace event 的名称。 |
| `TRACE_ID` | 用于关联 `TRACE_BEGIN` 和 `TRACE_END` 的字段名称。 |

**输出示例**

```
$zbs-perf-tools trace analyze latdist trace-data/cid-2-10-168-57-62/2022-04-06-083408+0800/ zbs_client:io_begin zbs_client:io_end trace_id

                     lat           : count     distribution
              0 -> 64.00           : 3        |*                               |
          64.00 -> 128.00          : 62       |*                               |
         128.00 -> 256.00          : 8730     |*                               |
         256.00 -> 512.00          : 567272   |*****************************   |
         512.00 -> 1024.00         : 639739   |********************************|
        1024.00 -> 2048.00         : 18695    |*                               |
        2048.00 -> 4096.00         : 35172    |**                              |
        4096.00 -> 8192.00         : 63875    |****                            |
        8192.00 -> 16384.00        : 44440    |***                             |
       16384.00 -> 32768.00        : 198      |*                               |
       32768.00 -> +inf            : 144      |*                               |
```

---

## 管理密钥管理服务和加密 > 管理密钥管理服务

# 管理密钥管理服务

密钥管理服务可选外置密钥管理服务和内置密钥管理服务。

- 外置密钥管理服务由一个或多个密钥管理服务器组成，这些密钥管理服务器共享数据，在密钥管理服务任意节点注册的 client 可以访问密钥管理服务的任意节点。
- 内置密钥管理服务是集群提供的内部密钥管理服务，功能和外置密钥管理服务一致。

---

## 管理密钥管理服务和加密 > 管理密钥管理服务 > 查看所有密钥管理服务信息

# 查看所有密钥管理服务信息

**操作方法**

在集群任一节点执行如下命令，查看所有密钥管理服务的信息：

```
zbs-meta kms list
```

**输出示例**

- 外置密钥管理服务：

  ```
  Type: kmip
  Provider Id:  1b8872b5-ffc4-4811-8671-b814efdf9c54
  Provider Name:  kmip-kms
  Vendor:  test-vendor
  Auth Id:  ka-1b8872-01
  Username:  test-username
  Is Rotating Key:  False
  Key Rotation Seconds:  31536000
  Last Key Rotation Time:  2026-01-06 13:46:04
  Last Key Backup Time:  2025-12-24 16:31:20.0
  SM4 Code:  258
  Crypt Stats:
    CipherFamily: AES256_CTR, Encrypt Res Num:  60
    CipherFamily: SM4_CTR, Encrypt Res Num:  0
  Status:  KMS_STATUS_RUNNING

  ID            Host              Port  Status
  ------------  --------------  ------  ------------------------
  ks-1b8872-01  192.168.2.2    5696  KMIP_SERVER_CONNECTED
  ks-1b8872-02  172.20.1.1     5696  KMIP_SERVER_DISCONNECTED
  ```

  | 参数 | 说明 |
  | --- | --- |
  | `Type` | 密钥管理服务类型，`kmip` 表示用 kmip 协议通信的外置密钥管理服务。 |
  | `Provider Id` | 密钥管理服务 ID。 |
  | `Provider Name` | 密钥管理服务的名称。 |
  | `Vendor` | 密钥管理服务的厂商。 |
  | `Auth Id` | 密钥管理服务的认证信息 ID。 |
  | `Username` | 密钥管理服务的认证信息中的用户名字段。 |
  | `Is Rotating Key` | 集群是否正在轮换密钥。 |
  | `Key Rotation Seconds` | 集群自动轮换密钥间隔。 |
  | `Last Key Rotation Time` | 上一次密钥轮换时间。 |
  | `Last Key Backup Time` | 上一次密钥备份时间。 |
  | `SM4 Code` | SM4 的加密算法值。 |
  | `CipherFamily` | 密钥管理服务开启的加密算法。 |
  | `Encrypt Res Num` | 集群与该加密算法关联的加密资源数量。 |
  | `Status` | 密钥管理服务的状态。 |
  | `ID` | 密钥管理服务器的 ID。 |
  | `Host` | 密钥管理服务器的 IP 或域名。 |
  | `Port` | 密钥管理服务器的端口。 |
  | `Status` | 密钥管理服务器的状态。 |
- 内置密钥管理服务：

  ```
  Type: native
  Provider Id:  1a1e76cf-ffa5-44da-a98b-3a13a2633702
  Provider Name:  NativeKMS
  Is Rotating Key:  False
  Key Rotation Seconds:  31536000
  Last Key Rotation Time:  2026-01-06 11:56:37.0
  Last Key Backup Time:  2025-12-24 16:31:20.0
  Crypt Stats:
     CipherFamily: AES256_CTR, Encrypt Res Num:  60
     CipherFamily: SM4_CTR, Encrypt Res Num:  0
  Status:  KMS_STATUS_RUNNING
  ```

  | 参数 | 说明 |
  | --- | --- |
  | `Type` | 密钥管理服务类型，native 表示内置密钥管理服务。 |
  | `Provider Id` | 密钥管理服务 ID。 |
  | `Provider Name` | 密钥管理服务的名称。 |
  | `Is Rotating Key` | 集群是否正在轮换密钥。 |
  | `Key Rotation Seconds` | 集群自动轮换密钥间隔。 |
  | `Last Key Rotation Time` | 上一次密钥轮换时间。 |
  | `Last Key Backup Time` | 上一次密钥备份时间。 |
  | `CipherFamily` | 密钥管理服务开启的加密算法。 |
  | `Encrypt Res Num` | 集群与该加密算法关联的加密资源数量。 |
  | `Status` | 密钥管理服务的状态。 |

---

## 管理密钥管理服务和加密 > 管理密钥管理服务 > 管理外置密钥管理服务

# 管理外置密钥管理服务

外置密钥管理服务由一个或多个密钥管理服务器组成，这些密钥管理服务器共享数据，在密钥管理服务任意节点注册的 client 可以访问密钥管理服务的任意节点。

## 创建外置密钥管理服务

**操作方法**

在集群任一节点执行如下命令，创建外置密钥管理服务：

```
zbs-meta kms create_kmip --servers SERVERS [--vendor <VENDOR>] [--key_rotate_period_seconds <KEY_ROTATE_PERIOD_SECONDS>]
                        --certificate <CERTIFICATE> --private_key <PRIVATE_KEY> [--username <USERNAME>] [--password <PASSWORD>]
                        [--sm4_code <SM4_CODE>] [--crypt_algos <CRYPT_ALGOS>]
                        <provider_name>
```

| 参数 | 说明 |
| --- | --- |
| `--servers <SERVERS>` | 密钥管理服务器的信息，格式为 `host:port`，支持传入多个，用 `,` 隔开。 |
| `--vendor <VENDOR>` | 密钥管理服务的提供商。 |
| `--key_rotate_period_seconds <KEY_ROTATE_PERIOD_SECONDS>` | SMTX OS 集群自动轮换密钥的周期，取值为[86400, 31536000]，单位为秒。 |
| `--certificate <CERTIFICATE>` | 访问密钥管理服务需要的认证信息的证书路径。 |
| `--private_key <PRIVATE_KEY>` | 访问密钥管理服务需要的认证信息的私钥路径。 |
| `--username <USERNAME>` | 访问密钥管理服务需要的认证信息的用户名。 |
| `--password <PASSWORD>` | 访问密钥管理服务需要的认证信息的密码。 |
| `--sm4_code <SM4_CODE>` | 密钥管理服务对应的 SM4 算法值。 |
| `--crypt_algos <CRYPT_ALGOS>` | 密钥管理服服务开启的加密算法，支持 AES256\_CTR 和 SM4\_CTR。 |
| `<provider_name>` | 密钥管理服务的名称。 |

**输出示例**

```
Provider Id:  1b8872b5-ffc4-4811-8671-b814efdf9c54
Provider Name:  kmip-kms
Vendor:  test-vendor
Auth Id:  ka-1b8872-01
Username:  test-username
Is Rotating Key:  False
Key Rotation Seconds:  31536000
Last Key Rotation Time:  2026-01-06 13:46:04.0
Last Key Backup Time:  2026-01-01 11:04:12.0
SM4 Code:  258
Crypt Stats:
  CipherFamily: AES256_CTR, Encrypt Res Num:  60
  CipherFamily: SM4_CTR, Encrypt Res Num:  0
Status:  KMS_STATUS_RUNNING

ID            Host              Port  Status
------------  --------------  ------  ------------------------
ks-1b8872-01  192.168.2.2    5696  KMIP_SERVER_CONNECTED
ks-1b8872-02  172.20.1.1     5696  KMIP_SERVER_DISCONNECTED
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Provider Id` | 密钥管理服务 ID |
| `Provider Name` | 密钥管理服务的名称。 |
| `Vendor` | 密钥管理服务的厂商。 |
| `Auth Id` | 密钥管理服务的认证信息 ID。 |
| `Username` | 密钥管理服务的认证信息中的用户名。 |
| `Is Rotating Key` | 集群是否正在轮换密钥。 |
| `Key Rotation Seconds` | 集群自动轮换密钥间隔。 |
| `Last Key Rotation Time` | 上一次密钥轮换时间。 |
| `Last Key Backup Time` | 上一次密钥备份时间。 |
| `SM4 Code` | SM4 的加密算法值。 |
| `CipherFamily` | 密钥管理服务开启的加密算法。 |
| `Encrypt Res Num` | 集群与该加密算法关联的加密资源数量。 |
| `Status` | 密钥管理服务的状态。 |
| `ID` | 密钥管理服务器的 ID。 |
| `Host` | 密钥管理服务器的 IP 或域名。 |
| `Port` | 密钥管理服务器的端口。 |
| `Status` | 密钥管理服务器的状态。 |

**输出说明**

执行成功无输出。

## 更新外置密钥管理服务配置

**操作方法**

在集群任一节点执行如下命令，更新外置密钥管理服务配置：

```
zbs-meta kms refresh_kmip [--provider_name <PROVIDER_NAME>] --servers <SERVERS> [--vendor <VENDOR>] [--key_rotate_period_seconds <KEY_ROTATE_PERIOD_SECONDS>] --certificate <CERTIFICATE> --private_key <PRIVATE_KEY> [--username <USERNAME>] [--password <PASSWORD>] [--sm4_code <SM4_CODE>] [--crypt_algos <CRYPT_ALGOS>] <provider_id>
```

| 参数 | 说明 |
| --- | --- |
| `--provider_name <PROVIDER_NAME>` | 更新的密钥管理服务的名称。 |
| `--servers <SERVERS>` | 更新的密钥管理服务器的信息，格式为 `host:port`，支持传入多个，用 `,` 隔开。 |
| `--vendor <VENDOR>` | 更新的密钥管理服务的提供商。 |
| `--key_rotate_period_seconds <KEY_ROTATE_PERIOD_SECONDS>` | SMTX OS 集群自动轮换密钥的周期，取值为[86400, 31536000]，单位为秒。 |
| `--certificate <CERTIFICATE>` | 更新的密钥管理服务认证信息的证书路径。 |
| `--private_key <PRIVATE_KEY>` | 更新的密钥管理服务认证信息的私钥路径。 |
| `--username <USERNAME>` | 更新的密钥管理服务认证信息的用户名。 |
| `--password <PASSWORD>` | 更新的密钥管理服务认证信息的密码。 |
| `--sm4_code <SM4_CODE>` | 更新的密钥管理服务对应的 SM4 算法值。 |
| `--crypt_algos <CRYPT_ALGOS>` | 更新的密钥管理服服务开启的加密算法，支持 AES256\_CTR 和 SM4\_CTR。 |
| `<provider_id>` | 更新的密钥管理服务 ID。 |

**输出示例**

```
Provider Id:  1b8872b5-ffc4-4811-8671-b814efdf9c54
Provider Name:  kmip-kms
Vendor:  test-vendor
Auth Id:  ka-1b8872-01
Username:  test-username
Is Rotating Key:  False
Key Rotation Seconds:  31536000
Last Key Rotation Time:  2026-01-06 13:46:04.0
SM4 Code:  258
Crypt Stats:
  CipherFamily: AES256_CTR, Encrypt Res Num:  60
  CipherFamily: SM4_CTR, Encrypt Res Num:  0
Status:  KMS_STATUS_RUNNING

ID            Host              Port  Status
------------  --------------  ------  ------------------------
ks-1b8872-01  192.168.2.2    5696  KMIP_SERVER_CONNECTED
ks-1b8872-02  172.20.1.1     5696  KMIP_SERVER_DISCONNECTED
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Provider Id` | 密钥管理服务 ID |
| `Provider Name` | 密钥管理服务的名称。 |
| `Vendor` | 密钥管理服务的厂商。 |
| `Auth Id` | 密钥管理服务的认证信息 ID。 |
| `Username` | 密钥管理服务的认证信息中的用户名。 |
| `Is Rotating Key` | 集群是否正在轮换密钥。 |
| `Key Rotation Seconds` | 集群自动轮换密钥间隔。 |
| `Last Key Rotation Time` | 上一次密钥轮换时间。 |
| `Last Key Backup Time` | 上一次密钥备份时间。 |
| `SM4 Code` | SM4 的加密算法值。 |
| `CipherFamily` | 密钥管理服务开启的加密算法。 |
| `Encrypt Res Num` | 集群与该加密算法关联的加密资源数量。 |
| `Status` | 密钥管理服务的状态。 |
| `ID` | 密钥管理服务器的 ID。 |
| `Host` | 密钥管理服务器的 IP 或域名。 |
| `Port` | 密钥管理服务器的端口。 |
| `Status` | 密钥管理服务器的状态。 |

## 更新外置密钥管理服务信息

仅允许更新外置密钥管理服务的基本信息和认证信息。

### 更新外置密钥管理服务基本信息

**操作方法**

在集群任一节点执行如下命令，更新集群中外置密钥管理服务的基本信息：

```
zbs-meta kms update_kmip_attr [--name <NAME>] [--vendor <VENDOR>] [--key_rotate_period_seconds <KEY_ROTATE_PERIOD_SECONDS>] [--sm4_code <SM4_CODE>] [--crypt_algos CRYPT_ALGOS] <provider_id>
```

| 参数 | 说明 |
| --- | --- |
| `--name <NAME>` | 需要更新的密钥管理服务的名称。 |
| `--vendor <VENDOR>` | 需要更新的密钥管理服务的厂商名称。 |
| `--key_rotate_period_seconds <KEY_ROTATE_PERIOD_SECONDS>` | 更新集群自动轮换密钥的间隔，取值为 `[86400,31536000]`，单位为秒。 |
| `--sm4_code <SM4_CODE>` | 需要更新的密钥管理服务对应的 SM4 算法值。 |
| `--crypt_algos <CRYPT_ALGOS>` | 需要更新的密钥管理服服务开启的加密算法，支持 `AES256_CTR` 和 `SM4_CTR`。 |
| `<provider_id>` | 被更新的密钥管理服务 ID。 |

**输出说明**

执行成功无输出。

### 更新外置密钥管理服务认证信息

**操作方法**

在集群任一节点执行如下命令，更新外置密钥管理服务的认证信息：

```
zbs-meta kms update_kmip_auth [--action {add|set|delete}] [--force] [--auth_id AUTH_ID] [--certificate CERTIFICATE] [--private_key PRIVATE_KEY] [--username USERNAME] [--password PASSWORD] <provider_id>
```

| 参数 | 说明 |
| --- | --- |
| `--action {add|set|delete}` | 对应的更新操作：`add` 表示添加密钥管理服务认证信息，`set` 表示设置密钥管理服务认证信息，`delete` 表示删除密钥管理服务认证信息。 |
| `--force` | 强制更新密钥管理服务认证信息。 |
| `--auth_id AUTH_ID` | 需要更新的密钥管理服务认证信息 ID。 |
| `--certificate CERTIFICATE` | 需要更新的密钥管理服务认证信息的证书路径。 |
| `--private_key PRIVATE_KEY` | 需要更新的密钥管理服务认证信息的私钥路径。 |
| `--username USERNAME` | 需要更新的密钥管理认证信息的用户名信息。 |
| `--password PASSWORD` | 需要更新的密钥管理认证信息的密码信息。 |

**输出说明**

执行成功无输出。

## 删除外置密钥管理服务

**操作方法**

在集群任一节点执行如下命令，删除集群中的外置密钥管理服务，不存在加密资源（虚拟卷、虚拟机模板的卷、快照、iSCSI target、LUN 等）时才允许删除：

```
zbs-meta kms delete_kmip <provider_id>
```

| 参数 | 说明 |
| --- | --- |
| `provider_id` | 待删除的密钥管理服务 ID。 |

**输出说明**

执行成功无输出。

## 管理外置密钥管理服务的密钥管理服务器

仅允许对外置密钥管理服务的密钥管理服务器进行管理。

### 查看外置密钥管理服务的密钥管理服务器

**操作方法**

在集群任一节点执行如下命令，查看密钥管理服务器：

```
zbs-meta kms list_kmip_server [--show_task] <provider_id>
```

| 参数 | 说明 |
| --- | --- |
| `--show_task` | 查看密钥管理服务器的心跳任务。 |
| `provider_id` | 密钥管理服务器所属密钥管理服务的 ID。 |

**输出示例**

```
Server:      192.168.20.227:5696
Heart Task:  2026-01-06 13:48:04 c0fe30d662484a608190da0cd6c39b6bcb2ba625366b45438abd9809d32e7946 EOK

ID            Host              Port  Status
------------  --------------  ------  ---------------------
ks-1b8872-01  192.168.20.227    5696  KMIP_SERVER_CONNECTED
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Server` | 密钥管理服务器信息。 |
| `Heart Task` | 心跳任务信息。 |
| `ID` | 密钥管理服务器的 ID。 |
| `Host` | 密钥管理服务器的 IP 或域名。 |
| `Port` | 密钥管理服务器的端口。 |
| `Status` | 密钥管理服务器的运行状态。 |

### 更新外置密钥管理服务的密钥管理服务器

**操作方法**

在集群任一节点执行如下命令，更新密钥管理服务器信息：

```
zbs-meta kms update_kmip_server [--action {add|set|delete}] [--force] [--server_id <SERVER_ID>] [--name <NAME>] [--host <HOST>] [--port <PORT>] <provider_id>
```

| 参数 | 说明 |
| --- | --- |
| `--action {add|set|delete}` | 对应的更新操作：`add` 表示添加密钥管理服务器，`set` 表示设置密钥管理服务器信息，`delete` 表示删除密钥管理服务器。 |
| `--force` | 强制更新密钥管理服务器。 |
| `--server_id <SERVER_ID>` | 需要更新的密钥管理服务器 ID。 |
| `--name <NAME>` | 需要更新的密钥管理服务器名称。 |
| `--host <HOST>` | 需要更新的密钥管理服务器 IP 或域名。 |
| `--port <PORT>` | 需要更新的密钥管理服务器端口。 |
| `<provider_id>` | 需要更新的密钥管理服务器所属密钥管理服务 ID。 |

**输出说明**

执行成功无输出。

---

## 管理密钥管理服务和加密 > 管理密钥管理服务 > 管理内置密钥管理服务

# 管理内置密钥管理服务

内置密钥管理服务是集群提供的内部密钥管理服务，功能和外置密钥管理服务一致。

## 查看内置密钥管理服务信息

**操作方法**

在集群任一节点执行如下命令，查看集群中内置密钥管理服务的信息：

```
zbs-meta kms show_native
```

**输出示例**

```
------------------------  -----------------------------------------
Provider Id               1487fdf7-f730-4d25-9b85-510322067010
Provider Name             NativeKMS
Last key rotate time      2026-01-06 14:26:57
Key rotate period         31536000
Last all key backup time  -
Rotating master key       No
Status                    KMS_STATUS_RUNNING
Crypt Stats               AES256_CTR Encrypt Res Num: 0
                          SM4_CTR Encrypt Res Num: 1

------------------------  -----------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Provider Id` | 密钥管理服务 ID。 |
| `Provider Name` | 密钥管理服务名称。 |
| `Last key rotate time` | 上次主密钥轮转时间。 |
| `Key rotate period` | 自动轮换主密钥间隔，单位秒。 |
| `Last all key backup time` | 上一次备份数据密钥时间。 |
| `Rotating master key` | 集群是否正在轮换密钥。 |
| `Status` | 密钥管理服务的状态。 |
| `Crypt Stats` | 密钥管理服务支持的算法以及正在使用的资源数量。 |

## 创建内置密钥管理服务

**操作方法**

在集群任一节点执行如下命令，创建密钥管理服务，一个 SMTX OS 集群只支持一套内置密钥管理服务：

```
zbs-meta kms create_native --crypt_algos <CRYPT_ALGOS> [--key_rotate_period_seconds <KEY_ROTATE_PERIOD_SECONDS>]
```

| 参数 | 说明 |
| --- | --- |
| `--crypt_algos <CRYPT_ALGOS>` | 内置密钥管理服服务开启的加密算法，支持 `AES256_CTR` 和 `SM4_CTR`。 |
| `--key_rotate_period_seconds <KEY_ROTATE_PERIOD_SECONDS>` | SMTX OS 集群自动轮换密钥的周期，取值为[86400, 31536000]，单位为秒。 |

**输出说明**

与 `show_native` 输出结果相同。

## 更新内置密钥管理服务配置

**操作方法**

在集群任一节点执行如下命令，更新内置密钥管理服务配置：

```
zbs-meta kms update_native [--crypt_algos <CRYPT_ALGOS>] [--key_rotate_period_seconds <KEY_ROTATE_PERIOD_SECONDS>]
```

| 参数 | 说明 |
| --- | --- |
| `--crypt_algos <CRYPT_ALGOS>` | 内置密钥管理服服务开启的加密算法，支持 `AES256_CTR` 和 `SM4_CTR`。 |
| `--key_rotate_period_seconds <KEY_ROTATE_PERIOD_SECONDS>` | SMTX OS 集群自动轮换密钥的周期，取值为 `[86400,31536000]`，单位为秒。 |

**输出说明**

执行成功无输出。

## 删除内置密钥管理服务

**操作方法**

在集群任一节点执行如下命令，删除集群中的内置密钥管理服务，不存在加密资源（虚拟卷、虚拟机模板的卷、快照、iSCSI target、LUN 等）时才允许删除：

```
zbs-meta kms delete_native
```

**输出说明**

执行成功无输出。

## 运维内置 KMS key

通过  `zbs-meta native_key -h` 管理和查看当前 KMS key 的服务状态和密钥状态。

> **注意**
>
> 通常仅需使用 show 即可，其余操作属于特殊运维指令，请咨询研发工程师后使用。

| 参数 | 说明 |
| --- | --- |
| `--mgt_id <MGT_ID>` | 除 show 外的其余动作，需要设置该值为 KMS 实例 ID。 |
| `--history` | 展示集群中仍存在的历史的 KMS key。 |

**输出示例**

以下展示 show 操作的输出示例：

```
$ zbs-meta native_key show
-----------------  ----------------------------------------
KMS Id             e99e5601-0780-4c68-98a7-3b563d01c516
Created time       2025-12-30 19:29:15
Current shamir id  nsk_6f751f04-7b8f-4409-8eaa-b02e17105988
Rotate period      31536000
Last rotate time   2026-01-05 19:30:50
-----------------  ----------------------------------------
[State: NK_STATE_RUNNING]
[Current shamir key ⬇ ]
-------------  ------------------------------------------------------------------------------
Key Id         nsk_6f751f04-7b8f-4409-8eaa-b02e17105988
Total mkey     10
Garbage mkey   8
Inuse mkey     2
Create time    2026-01-05 19:30:50
Zones summary  zone_id: default
                 k/n: 2/4
                 dist_time: 2026-01-05 19:30:50, dist_no: 1
                 protection: LEVEL4: All shares have acked
                 share_cnt: 4, shares:
                 - [share_id: 1, cid: 1, ip: 10.234.5.14, last_ack_time: 2026-01-06 17:19:29]
                 - [share_id: 2, cid: 3, ip: 10.234.5.12, last_ack_time: 2026-01-06 17:19:29]
                 - [share_id: 3, cid: 5, ip: 10.234.5.13, last_ack_time: 2026-01-06 17:19:29]
                 - [share_id: 4, cid: 7, ip: 10.234.5.11, last_ack_time: 2026-01-06 17:19:29]
-------------  ------------------------------------------------------------------------------
```

**输出说明**

| KMS 实例参数 | 说明 |
| --- | --- |
| `KMS Id` | 内置 KMS 实例 ID。 |
| `Created time` | 实例创建时间。 |
| `Current shamir id` | 正在使用的 KMS key ID。 |
| `Rotate period` | 自动轮换 KMS key 间隔，单位秒。 |
| `Last rotate time` | 上一次 KMS key 轮换时间。 |
| `State` | 实例运行状态。 |

| KMS key 参数 | 说明 |
| --- | --- |
| `Key Id` | KMS key ID |
| `Total mkey` | 实例内全部的主密钥数量。 |
| `Garbage mkey` | 实例内过期的主密钥数量。 |
| `Inuse mkey` | 实例内使用的主密钥数量。 |
| `Create time` | KMS key 创建时间。 |
| `Zones summary` | KMS key 的分片放置计划，重点关注 protection 是否在 LEVEL2 及以上、share 的 last\_ack\_time 是否过久。 |

---

## 管理密钥管理服务和加密 > 管理加密

# 管理加密

## 查看集群内的主密钥 ID

**操作方法**

在集群任一节点执行如下命令，查看集群内所有加密卷所使用的主密钥 ID。

```
zbs-meta kms list_master_key
```

**输出示例**

```
Id                                        Encrypt Type      Volume Num    Snapshot Num
----------------------------------------  --------------  ------------  --------------
nmk_02842077-715d-4562-a98d-36efa518cafb  AES256_CTR                 0               0
nmk_6fb683d3-9064-457b-b003-5574d1f26b72  SM4_CTR                    1               0
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Id` | 集群主密钥 ID。 |
| `Encrypt Type` | 加密算法类型。 |
| `Volume Num` | 使用该主密钥的存储卷数量。 |
| `Snapshot Num` | 使用该主密钥的快照数量。 |

## 手动轮换主密钥

**操作方法**

在集群任一节点执行如下命令，轮换集群主密钥：

```
zbs-meta kms rotate_key <provider_id>
```

| 参数 | 说明 |
| --- | --- |
| `provider_id` | 密钥管理服务 ID。 |

**输出示例**

执行成功无输出。

## 导出所有卷的加密密钥

**操作方法**

在集群任一节点执行如下命令，导出所有加密卷的加密密钥：

```
zbs-meta kms export_key --dek_encrypt_password <DEK_ENCRYPT_PASSWORD> --output <OUTPUT>
```

| 参数 | 说明 |
| --- | --- |
| `<DEK_ENCRYPT_PASSWORD>` | 导出加密卷使用的密码。 |
| `<OUTPUT>` | 导出密钥的保存文件路径。 |

**输出示例**

执行成功无输出。

## 导入卷的加密密钥

**操作方法**

在集群任一节点执行如下命令，为集群导入密钥：

```
zbs-meta kms import_key --dek_decrypt_password <DEK_DECRYPT_PASSWORD> --input <INPUT>
```

| 参数 | 说明 |
| --- | --- |
| `<DEK_DECRYPT_PASSWORD>` | 导入密钥时的密码，与导出这批密钥时所使用的密码一样。 |
| `<INPUT>` | 导入密钥的文件路径。 |

**输出示例**

执行成功无输出。

---

## 管理网络 > 更新网络配置

# 更新网络配置

## 配置 RDMA 接入网络（VMware ESXi 平台）

当集群虚拟化平台为 VMware ESXi 且开启 RDMA 功能时，在集群部署完成后需要额外配置 RDMA 接入网络，此时可以执行该命令，该命令会通过连接当前 SCVM 所在 ESXi 主机获取网络信息，进而配置 SCVM 节点 VMware 接入网络。

**操作方法**

在集群任一节点执行如下命令：

`zbs-deploy-manage deploy-rdma`

**输出示例**

若输出 `Finish deploy RDMA` 则表示配置成功。

## 配置流量控制

为存储网络或接入网络配置流量控制。

**操作方法**

在待配置流量控制的节点上执行如下命令：

`zbs-deploy-manage config-rdma-fc [--storage_qos_mode <storage_qos_mode>] [--access_qos_mode <access_qos_mode>]`

**参数说明**

| 参数 | 说明 |
| --- | --- |
| `[--storage_qos_mode <storage_qos_mode>]` | 可选参数，为存储网络配置流量控制。  `<storage_qos_mode>` 取值为：   - `dscp`：基于 L3 DSCP 的 PFC 流量控制 - `global`：基于 Global Pause 流量控制 |
| `[--access_qos_mode <access_qos_mode>]` | 可选参数，为接入网络配置流量控制。  `<access_qos_mode>` 取值为：   - `dscp`：基于 L3 DSCP 的 PFC 流量控制 - `global`：基于 Global Pause 流量控制 |

**使用示例**

为接入网络配置基于 L3 DSCP 的 PFC 流量控制：

`zbs-deploy-manage config-rdma-fc --access_qos_mode dscp`

**输出示例**

```
[root@Node211 16:55:17 smartx]$ zbs-deploy-manage config-rdma-fc --access_qos_mode dscp
Storage Network QoS Mode: dscp IBDEV: rocex1070fd0300a0b708
DCBX mode: OS controlled
Priority trust state: dscp
dscp2prio mapping:
        prio:0 dscp:07,06,05,04,03,02,01,00,
        prio:1 dscp:15,14,13,12,11,10,09,08,
        prio:2 dscp:23,22,21,20,19,18,17,16,
        prio:3 dscp:31,30,29,28,27,26,25,24,
        prio:4 dscp:39,38,37,36,35,34,33,32,
        prio:5 dscp:47,46,45,44,43,42,41,40,
        prio:6 dscp:55,54,53,52,51,50,49,48,
        prio:7 dscp:63,62,61,60,59,58,57,56,
default priority:
Receive buffer size (bytes): 130944,130944,0,0,0,0,0,0,
Cable len: 7
PFC configuration:
        priority    0   1   2   3   4   5   6   7
        enabled     0   0   0   1   0   0   0   0
        buffer      0   0   0   1   0   0   0   0
tc: 0 ratelimit: unlimited, tsa: vendor
         priority:  1
tc: 1 ratelimit: unlimited, tsa: vendor
...
PFC configuration:
        priority    0   1   2   3   4   5   6   7
        enabled     0   0   0   1   0   0   0   0
        buffer      0   0   0   1   0   0   0   0
tc: 0 ratelimit: unlimited, tsa: vendor
         priority:  1
tc: 1 ratelimit: unlimited, tsa: vendor
         priority:  0
tc: 2 ratelimit: unlimited, tsa: vendor
         priority:  2
tc: 3 ratelimit: unlimited, tsa: vendor
         priority:  3
tc: 4 ratelimit: unlimited, tsa: vendor
         priority:  4
tc: 5 ratelimit: unlimited, tsa: vendor
         priority:  5
tc: 6 ratelimit: unlimited, tsa: vendor
         priority:  6
tc: 7 ratelimit: unlimited, tsa: vendor
         priority:  7
```

---

## 管理网络 > 管理网卡

# 管理网卡

使用命令行可以查看和修改虚拟分布式交换机 OVS 网桥所关联的物理网口和物理网口绑定模式。

如下命令主要适用于以下几种场景：

- 更换网卡。
- 更改主机上的 OVS 网桥关联的网卡。
- 修改 OVS 网桥关联的网卡的绑定模式。

**注意事项**

- 更换网卡需要修改节点主机上的虚拟网桥（OVS 网桥）信息，并需要将修改后的虚拟网桥信息同步到数据库中。
- 更换网卡要求节点上不存在数据恢复。如果节点上存在数据恢复，完成数据恢复可能需要等待的时间不定（具体时间根据业务压力而定），建议在节点业务压力低的情况下操作更换网卡。

## 获取网桥当前所使用的网卡绑定的名称

在正常运行的节点上获取 OVS 网桥所对应的绑定名称。

**操作方法**

在节点执行如下命令：

`network-tool get-bond-name --ovsbr_name <ovsbr_name>`

`--ovsbr_name <ovsbr_name>` 为需要获取绑定名称对应的 OVS 网桥名称。

**使用示例**

`network-tool get-bond-name --ovsbr_name ovsbr-n5b9qlfm2`

**输出示例**

```
2022-05-18 12:44:33,892 [72353] [INFO] bond_name: bond-m-dd417f1a
```

## 设置网桥参数

使用命令行设置网桥的如下参数：

- 网桥名称
- 网桥关联的网卡
- 网桥所关联的虚拟分布式交换机（VDS）使用的绑定模式

**操作方法**

在网桥所在节点执行如下命令：

`network-tool change-bridge {argument list}`

参数说明如下：

| **参数** | **说明** |
| --- | --- |
| **`--ovsbr_name <ovsbr_name_to_be_changed>`** | 必须输入的参数。代表变更前 OVS 网桥的名称。 |
| **`--old_port_name <old_port_name>`** | 必须输入的参数。代表更换网卡前，OVS 网桥所关联的物理网口名称或者绑定名称。  - 若 OVS 网桥未关联网口：`<old_port_name>` 为 `None`。 - 若 OVS 网桥关联单个物理网口：`<old_port_name>` 为 OVS 网桥当前所关联的物理网口名称。 - 若 OVS 网桥绑定多个物理网口：通过 `network-tool get-bond-name --ovsbr_name <ovsbr_name>` 命令获取该 OVS 网桥所对应的网口绑定名称，即 `bond_name` 参数值。 |
| **`--nics <target_nics>`** | 必须输入的参数，代表 OVS 网桥计划关联的所有网口的名称，例如 `eth0` 或 `"eth0 eth1"` 等。  - 如有多个网口，需要列举出该 OVS 网桥需要关联的所有网口，用空格将多个网口名称隔开，并注意对存在空格的参数使用双引号（`" "`）。例如 `"eth0 eth1"`。 - 此处输入的网口需保证未与其他 OVS 网桥关联。 |
| **`--bond_mode <bonding_mode>`** | 必须输入的参数。指定该 OVS 网桥所关联的虚拟分布式交换机（VDS）使用的绑定模式。  - 若 OVS 网桥只关联了一个网口，则无法设置绑定，请填写 `None`。 - 若 OVS 网桥关联了存储网络，则 VDS 使用 OVS Bond 模式，包括 ：   - `active-backup`（OVS Bond）   - `balance-slb`：若存储网络已开启 RDMA，则不支持该绑定模式。   - `balance-tcp`：设置为此模式时，要求对端交换机开启 LACP 动态链路聚合。 |
| **`--rb_interval <rb_interval>`** | 可选输入的参数，代表 `balance-slb` 绑定模式下 rebalance 的时间间隔。仅当网口绑定模式为 `balance-slb` 时需要填写，其他模式时此字段及参数 `--rb_interval <rb_interval>` 均不需要填写。 若网口绑定模式为 `balance-slb`：   - 禁用 rebalance：将 `<rb_interval>` 设置为 `0`。 - 使用默认的 rebalance 时间间隔 60 秒：不输入 `--rb_interval <rb_interval>` 字段，或输入 `--rb_interval ""`。 - 自定义 rebalance 的时间间隔：将 `<rb_interval>` 设置为大于 0 的整数。 |
| **`--bond_name <bonding_name>`** | 必须输入的参数。代表 OVS 网桥对应的绑定名称，该绑定名称不能和已存在的绑定名称相同。  - 不同单网口之间互相转换时，请通过 `network-tool get-bond-name --ovsbr_name <ovsbr_name>` 命令获取。 - 从单⽹⼝或 Linux Bond 转换为 OVS Bond 时，`<bonding_name>` 不能取 `bond0`、 `bond1` 和 `bond2`。 - 从单⽹⼝或 OVS Bond 转换为 Linux Bond 时，`<bonding_name>` 取固定值，接⼊⽹络为 `bond0`，管理⽹络为 `bond1`，存储⽹络为 `bond2`。 - 从 OVS Bond 转换为单⽹⼝时，不允许改变绑定名称，与 `old_port_name` 保持一致。 - 不同 OVS Bond 之间互相转换时，不允许改变绑定名称，与 `old_port_name` 保持一致。 - 从 Linux Bond 转换为单⽹⼝时，`<bonding_name>` 设置为 `None`。 - Linux Bond 转换为 OVS Bond 时，转换后 OVS 网桥对应的绑定名称为新的名称。 |
| **`--active_slave <active_nic_name>`** | 可选输入的参数，仅当网口绑定模式为 `active-backup` 时，可以通过设置该参数指定一个 Active 网口，不设置该参数则由系统自动选定一个 Active 网口。 |
| **`--mcast_snooping <current_mcast_snooping>`** | 必须输入的参数，请根据 OVS 网桥关联的 VDS 当前的 IGMP/MLD 侦听配置输入对应的值。若当前已开启 IGMP/MLD 侦听，则设置该参数为 `enable`，否则设置为 `disable`。  **注意**:  该参数不可用于开启或关闭 VDS IGMP/MLD 侦听，仅表示 VDS 当前的 IGMP/MLD 侦听配置。 |

**使用示例**

对原始名称为 ovsbr-mgt 的 OVS 网桥进行参数设置。将单网口（eth0） 变更为双网口（eth0 和 eth1），该 OVS 网桥所关联的 VDS 使用的绑定模式为 OVS Bond 中的 balance-slb 模式，rebalance 时间间隔为 80 秒， OVS 网桥对应的新的绑定名称为 bond-mgt。

`network-tool change-bridge --ovsbr_name ovsbr-mgt --old_port_name eth0 --nics "eth0 eth1" --bond_mode balance-slb --rb_interval 80 --bond_name bond-mgt --mcast_snooping disable`

如果存储网络开启了 RDMA，对原始名称为 ovsbr-stor 的 OVS 网桥进行参数设置。将 Linux Bond 802.3ad 模式变更为 OVS Bond balance-tcp 模式（eth0 和 eth1）， OVS 网桥对应的新的绑定名称为 bond-storage。

`network-tool change-bridge --ovsbr_name ovsbr-stor --old_port_name bond2 --nics "eth0 eth1" --bond_mode balance-tcp --bond_name bond-storage --mcast_snooping disable`

**输出说明**

若输出 `change bridge finish`，则表明修改 OVS 网桥信息成功。

## 同步网桥网卡修改后的信息至数据库

将修改的 OVS 网桥信息同步到数据库。

**操作方法**

在网桥所在节点执行如下命令：

`network-tool sync-bridge {argument list}`

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `--ovsbr_name <ovsbr_name_to_be_changed>` | 必须输入的参数。代表待修改的 OVS 网桥的名称。 |
| `--bond_mode <bonding_mode>` | 必须输入的参数。代表 OVS 网桥所关联的虚拟分布式交换机（VDS）使用的绑定模式。必须与设置网桥参数时，使用的 `--bond_mode <bonding_mode>` 相同。 |
| `--bond_name <bonding_name>` | 必须输入的参数。 代表 OVS 网桥对应的绑定名称。必须与设置网桥参数时，使用的 `--bond_name <bonding_name>` 相同。 |
| `--nics <uplink_nics>` | 可选参数。命令格式为 `--nics "eth0 eth1"`。若通过 `network-tool change-bridge` 命令将被隔离的故障网卡和 OVS 网桥解除关联，需配置此参数，且需和 `network-tool change-bridge` 命令中的 `--nics <target_nics>` 参数保持一致。 |
| `--active_slave <active_nic_name>` | 可选输入的参数，仅当网口绑定模式为 `active-backup` 时，可以通过设置该参数指定一个 active 网口，不设置该参数则由系统自动选定一个 active 网口。 |

**使用示例**

`network-tool sync-bridge --ovsbr_name ovsbr-mgt --bond_mode balance-slb --bond_name bond-mgt --nics "eth0 eth1"`

**输出说明**

若输出 `sync successfully`，则表明同步数据成功。

**注意事项**

所有节点完成网桥信息同步后，若最后一个执行 `network-tool sync-bridge` 命令的节点为单网口，且存在其他节点为多网口时，需选择任意一个多网口节点再执行一次 `network-tool sync-bridge`。

## 获取 Linux Bond 包含的物理网口

**操作方法**

在网桥所在节点执行如下命令，获取 Linux Bond 中包含的物理网口信息：

`network-tool get-linux-bond-list`

**输出说明**

输出 Linux Bond 包含的物理网口信息。

## 检测 OVS Bond 网口的网络连通性

**操作方法**

在网桥所在节点执行如下命令，检测 OVS Bond 中包含的物理网口的连通性。

> **说明**：
>
> - 该检测命令只能检测管理网络和存储网路 VDS 中绑定网口的连通性。
> - 检测过程中会对 Bond 网口执行 ifdown/ifup 操作，可能会引起网络的短暂中断。

`network-tool check-ovs-bond-nics --bond_mode <bond_mode>`

| 参数 | 说明 |
| --- | --- |
| `--bond_mode <bond_mode>` | 必须输入的参数。代表检测该 Bond 类型中网口的连通性，支持 `"active-backup"` 或 `"balance-slb"`。 |

**使用示例**

`network-tool check-ovs-bond-nics --bond_mode "active-backup"`

**输出说明**

输出 Bond 中的每个网口到其他节点的连通性检测结果。

- 若输出 `check bond nic complete: all nic connection perfect!` 表示 Bond 中的网口连通性都正常。
- 若输出 `['eth2 can not ping xx.xx.xx.xx', 'eth2 can not ping xx.xx.xx.xx']` 表示 Bond 中的 `eth2` 网口的网络连通性异常。

## 更改节点管理网络 IP

**操作方法**

在集群节点执行如下命令，更改当前节点的管理 IP 地址：

`network-tool change-manage-ip <ip> <netmask> <gateway> [--vlan_id <vlan_id>]`

| **参数** | **说明** |
| --- | --- |
| `ip` | 管理网络 IP 地址。 |
| `netmask` | IP 地址子网掩码。 |
| `gateway` | 网关地址。 |
| `--vlan_id <vlan_id>` | 管理网络的 VLAN ID。  - 若不添加该参数，则执行命令后不会更新管理网络的 VLAN ID。 - 若物理交换机端口从 `Trunk 模式` 改为 `Access 模式`，请将该参数指定为 `--vlan_id 0`。 |

**输出示例**

输出配置过程，若输出 `change management ip address success!` 表示修改该节点管理 IP 地址成功。

## 迁移 default 虚拟机网络至其他 VDS

集群部署完成后，管理网络所在的 VDS 上将自动创建一个名为 `default` 的虚拟机网络。如需迁移 `default` 虚拟机网络至其他 VDS，请参考本节内容操作。迁移后，`default` 虚拟机网络的 MTU 将被重置为 1500。

**前提条件**

- default 虚拟机网络未配置 QoS。
- default 虚拟机网络未关联配置了虚拟网卡的虚拟机、虚拟机快照和虚拟机模版。

**操作方法**

在集群任意一个节点执行如下命令，将 default 虚拟机网络迁移至其他 VDS。

`network-tool migrate-default-network --vds_name <vds_name>`

| 参数 | 说明 |
| --- | --- |
| `<vds_name>` | default 虚拟机网络迁移的目标 VDS 的名称。 |

**使用示例**

`network-tool migrate-default-vm --vds_name vds_new`

**输出说明**

- 迁移失败将输出对应失败的原因。
- 迁移成功将输出 `migrate default vm network to vds_new success!`。

---

## 管理网络 > 管理部署前的管理网络配置信息

# 管理部署前的管理网络配置信息

使用命令行对部署前的管理网络配置信息进行管理。

在集群完成部署前，若重启已配置管理网络的节点，其管理网络配置将失效。请参考[清除部署前的管理网络配置信息](#%E6%B8%85%E9%99%A4%E9%83%A8%E7%BD%B2%E5%89%8D%E7%9A%84%E7%AE%A1%E7%90%86%E7%BD%91%E7%BB%9C%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF)小节内容清理残留配置后重新配置。

## 将多个网口绑定为一个支持 LACP 协议的网口

将管理网络使用的多个网口绑定为一个支持 LACP 协议的网口，绑定后网口名称默认为 `pre_bond`，并生成网口配置文件 `ifcfg-pre_bond`。

**操作方法**

在网口配置文件路径下执行以下命令：

`network-preconfig create-lacp --nics <nics>`

`--nics <nics>` 为必选参数，指的是管理网络使用的多个网口的名称。设置时，将多个网口名称用空格隔开，并注意对存在空格的参数使用双引号（" "），例如`"eth0 eth1"`。

**使用示例**

将管理网络使用的两个网口 `eth0` 和 `eth1` 绑定为一个支持 LACP 协议的网口。

`network-preconfig create-lacp --nics "eth0 eth1"`

**输出示例**

若系统输出 `create lacp bond port success`，则表明 `pre_bond` 网口创建完成，绑定管理网口成功。

若系统报错或需要修改配置，请先参考[清除部署前的管理网络配置信息](#%E6%B8%85%E9%99%A4%E9%83%A8%E7%BD%B2%E5%89%8D%E7%9A%84%E7%AE%A1%E7%90%86%E7%BD%91%E7%BB%9C%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF)小节内容清理后重新配置。

## 创建 VLAN 子接口

为管理网络使用的单网口或绑定网口创建 VLAN 子接口，并为 VLAN 子接口配置静态 IP、子网掩码、网关、VLAN ID 并生成对应的子接口配置文件。

**操作方法**

在网口配置文件路径下执行以下命令：

`network-preconfig create-vlanif --iface <iface> --ipaddr <ipaddr> --netmask <netmask> --gateway<gateway> --vlanid <vlanid>`

参数说明如下：

| **参数** | **说明** |
| --- | --- |
| `--iface <iface>` | 必选参数。表示待创建 VLAN 子接口的网口名称。  - 若待创建 VLAN 子接口的管理网络网口为 pre\_bond 网口，请设置为 `pre_bond`。 - 若待创建 VLAN 子接口的管理网络网口为单网口，请设置为实际的网口名称，如 `eth0`。 |
| `--ipaddr <ipaddr>` | 必选参数。表示实际规划的 VLAN 子接口的静态 IP 地址。 |
| `--netmask <netmask>` | 必选参数。表示实际规划的 VLAN 子接口的子网掩码。 |
| `--gateway <gateway>` | 必选参数。表示实际规划的 VLAN 子接口的网关。 |
| `--vlanid <vlanid>` | 必选参数。表示实际规划的 VLAN 子接口的 VLAN ID。 创建的子接口名称为 pre\_vlan.*vlanid*，对应生成的子接口配置文件名称为 ifcfg-pre\_vlan.*vlanid*。 |

**使用示例**

为绑定网口 pre\_bond 创建 VLAN 子接口，其静态 IP 为 192.168.52.251，子网掩码为 255.255.240.0，网关为 192.168.16.1，VLAN ID 为 1。

`network-preconfig create-vlanif --iface pre_bond --ipaddr 192.168.52.251 --netmask 255.255.240.0 --gateway 192.168.16.1 --vlanid 1`

**输出示例**

若系统输出 `create vlan interface success`，则表明 VLAN 子接口创建成功。创建的子接口名称为 pre\_vlan.1。

若系统报错或需要修改配置，请先参考[清除部署前的管理网络配置信息](#%E6%B8%85%E9%99%A4%E9%83%A8%E7%BD%B2%E5%89%8D%E7%9A%84%E7%AE%A1%E7%90%86%E7%BD%91%E7%BB%9C%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF)小节内容清理后重新配置。

## 给绑定网口直接配置静态 IP、子网掩码、网关

直接给绑定网口 pre\_bond 配置 IP 地址和网关，不配置 vlan 子接口，使用绑定网口直接进行部署。

**操作方法**

在网口配置文件路径下执行以下任一命令：

- `network-preconfig config-bond-address --ipaddr <ipaddr> --netmask <netmask> --gateway<gateway>`

  如需清理或修改配置，请参考[清除部署前的管理网络配置信息](#%E6%B8%85%E9%99%A4%E9%83%A8%E7%BD%B2%E5%89%8D%E7%9A%84%E7%AE%A1%E7%90%86%E7%BD%91%E7%BB%9C%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF)小节内容清理配置。
- `network-preconfig config-address --iface pre_bond --ipaddr <ipaddr> --netmask <netmask> --gateway<gateway>`

  如需清理或修改配置，请使用 `ip addr del` 命令清理配置。

参数说明如下：

| **参数** | **说明** |
| --- | --- |
| `--ipaddr <ipaddr>` | 必选参数。表示实际规划的绑定网口的静态 IP 地址。 |
| `--netmask <netmask>` | 必选参数。表示实际规划的绑定网口的子网掩码。 |
| `--gateway <gateway>` | 必选参数。表示实际规划的绑定网口的网关。 |

**使用示例**

为绑定网口 pre\_bond 配置其静态 IP 为 192.168.52.251，子网掩码为 255.255.240.0，网关为 192.168.16.1。

- `network-preconfig config-bond-address --ipaddr 192.168.52.251 --netmask 255.255.240.0 --gateway 192.168.16.1`
- `network-preconfig config-address --iface pre_bond --ipaddr 192.168.52.251 --netmask 255.255.240.0 --gateway 192.168.16.1`

**输出示例**

若系统输出 `config ip address for pre_bond interface success`，则表明给 pre\_bond 配置的地址信息成功。

## 配置指定物理网口

给指定的物理网口配置静态 IP 地址，子网掩码及缺省网关。

如需清理或修改配置，请使用 `ip addr del` 命令清理配置。

**操作方法**

在网口配置文件路径下执行以下命令：

`network-preconfig config-address --iface <iface> --ipaddr <ipaddr> --netmask <netmask> --gateway<gateway>`

参数说明如下：

| **参数** | **说明** |
| --- | --- |
| `--iface <iface>` | 必选参数。表示待设置地址的管理网络物理网口的网口名称，如 `eth0`。 |
| `--ipaddr <ipaddr>` | 必选参数。表示实际规划的网口的静态 IP 地址。 |
| `--netmask <netmask>` | 必选参数。表示实际规划的网口的子网掩码。 |
| `--gateway <gateway>` | 必选参数。表示实际规划的网口的网关。 |

**使用示例**

为物理网口 eth0 配置其静态 IP 为 192.168.52.251，子网掩码为 255.255.240.0，网关为 192.168.16.1。

`network-preconfig config-address --iface eth0 --ipaddr 192.168.52.251 --netmask 255.255.240.0 --gateway 192.168.16.1`

**输出示例**

若输出 `config ip address for pre_bond interface success`，则表明给绑定网口 `pre_bond` 配置 IP 地址，子网掩码和网关成功。

## 清除部署前的管理网络配置信息

清除部署前管理网络的所有配置信息，包括将多个网口绑定为一个支持 LACP 协议的网口的配置信息和创建 VLAN 子接口的配置信息。

**操作方法**

在网口配置文件路径下执行以下命令：

`network-preconfig clear-config`

**输出示例**

- 若系统输出 `delete pre_bond configuration`，则表明 pre\_bond 网口的配置信息清理成功。
- 若系统输出 `delete pre_vlan configuration`，则表明 VLAN 子接口的配置信息清理成功。

## 清除节点所有网络配置信息

清除节点上所有网络配置信息，包括节点上 OVS 网桥、系统网络、Bond 配置。

**风险提示**

清理后节点无任何网络配置，该操作属于高危操作，请您谨慎执行。

**操作方法**

在网口配置文件路径下执行以下命令：

- 若输出 `delete pre_bond configuration`，则表明 `pre_bond` 网口的配置信息清理成功。
- 若输出 `delete pre_vlan configuration`，则表明 VLAN 子接口的配置信息清理成功。

**输出示例**

若系统输出 `clean network configuration success!`，则表明节点网络配置信息完全清理成功。

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
