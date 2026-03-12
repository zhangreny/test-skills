---
title: "SMTXZBS/5.7.0/SMTX ZBS CLI 命令参考"
source_url: "https://internal-docs.smartx.com/smtxzbs/5.7.0/zbs_cli_guide/zbs_cli_guide_preface_generic"
sections: 102
---

# SMTXZBS/5.7.0/SMTX ZBS CLI 命令参考
## 关于本文档

# 关于本文档

本文档介绍了 SMTX ZBS（读作 SmartX ZBS）常见的使用场景及相关命令行。

---

## 文档更新信息

# 文档更新信息

**2025-12-01**：**文档随 SMTX ZBS 5.7.0 正式发布**。

相较于 5.6.4 版本，本版本更新如下：

- 删除了**移除异常 Partition**、**将某个 Cache 分区设置为无效**小节；
- 更新了**将 mongo 节点和其他节点重新同步**小节、**设置网桥参数**小节、多个与数据加密相关的小节、多个与多 chunk 实例功能相关的小节；
- 新增了**将异常 Partition 从 chunk 卸载**、**将异常 Cache 分区从 chunk 卸载**、**管理业务主机组**、**管理业务主机**、**管理回收站**、**管理 KMS 和加密**、**管理 CPU 安全补丁**、**查看节点 watchdog 日志**、**查看 chunk 线程轮训状态**小节。

---

## 命令行格式说明

# 命令行格式说明

本文档中提到的命令行格式说明如下表所示。用户在任何命令后都可以输入 `-h` 或者 `--help` 获得此命令的帮助提示。

| 格式 | 说明 |
| --- | --- |
| `zbs-meta migrate list` | 不带参数的命令，按原样输入。例如：  `zbs-meta migrate list` |
| `<parameter_value>` | 尖括号表示必选参数，需用参数值代替。例如:  语法：`shutdown <IP address>`  输入：`shutdown 192.168.67.59` |
| `|` | 竖线用于分隔多个互斥的可选参数 |
| `{}` | 大括号表示有多个参数，但必选一个。例如：  `shutdown {<IP address> | <MAC address>}` |
| `[]` | 方括号表示可选参数，可为空。例如：  `shutdown [force | now]` |

---

## 块存储集群 CLI 命令 > 管理集群 > 查看集群信息

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
| `dirty_cache_space` | 脏缓存空间大小，指还未下沉到 Partition 的 Cache 空间 |
| `error_nodes` | 异常节点数 |
| `failure_cache_space` | 失效缓存空间，不健康的节点提供的存储都会失效 |
| `failure_data_space` | 失效数据空间 |
| `healthy_nodes` | 健康节点数 |
| `idle_nodes` | 空闲节点数 |
| `provisioned_data_space` | 已置备数据空间 |
| `recover_enabled` | 是否开启数据恢复，当 Extent 副本数量小于预期数量时会触发数据恢复 |
| `removing_nodes` | 正在移除的节点 |
| `total_cache_capacity` | 总缓存容量，总缓存盘的容量总和 |
| `total_data_capacity` | 总数据容量 |
| `used_cache_space` | 已使用缓存容量 |
| `used_data_space` | 已使用数据容量 |
| `valid_cache_space` | 有效的缓存容量，等于总缓存容量减去失效缓存容量 |
| `valid_data_space` | 有效的数据容量，等于总数据容量减去失效数据容量 |

> **注意**：
>
> 在出现坏盘或者拔盘的情况下，total\_space 可能出现比 used\_space 小的情况。这是因为 total\_space 会排除坏盘或拔出物理盘的空间，而 used\_space 则需要等待数据恢复后才会被更新。

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

| 字段 | 说明 | 单位 |
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

![](https://cdn.smartx.com/internal-docs/assets/e1137223/zbs_cli_guide_01.png)

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

## 块存储集群 CLI 命令 > 管理集群 > 查看集群服务 > 查看集群中的服务

# 查看集群中的服务

## 查看集群中运行的所有服务信息

**操作方法**

在集群任一节点执行如下命令：

`zbs-tool service list`

**输出示例**

```
Name    Members                                                       Leader            Specified members                                             Priority    Current priority
------  ------------------------------------------------------------  ----------------  ------------------------------------------------------------  ----------  ------------------
meta    ['10.0.20.52:10100', '10.0.20.51:10100', '10.0.20.50:10100']  10.0.20.50:10100  ['10.0.20.50:10100', '10.0.20.51:10100', '10.0.20.52:10100']
ntp     ['10.0.20.52:0', '10.0.20.51:0', '10.0.20.50:0']              10.0.20.50:0      ['']
taskd   ['10.0.20.51:10601', '10.0.20.50:10601', '10.0.20.52:10601']  10.0.20.50:10601  ['']
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Name` | 集群中运行的服务名称。 |
| `Members` | 服务中包含的 Members，其格式为 IP：Port。 |
| `Leader` | 当前服务的主节点。 |
| `Specified members` | 运行 Meta 服务的节点。 |
| `Priority` | 为某服务的 Members 设置的优先级，取值为 0 ~ 255 的整数，数值越大，优先级越高。若 `Priority` 中没有显示某节点，则该节点的优先级默认为 1。 |
| `Current priority` | 当前某服务的 Members 的优先级。 `Current priority` 可根据节点状态在优先级不高于 `Priority` 的范围内自动进行动态调整，节点检测到自身异常时，主动降低自身的当前优先级，检测到服务恢复后，再将当前优先级恢复至设置的优先级。节点正常运行时， `Current priority` 与 `Priority` 相同。若 `Current priority` 中没有显示某节点，则该节点当前的 `Current priority` 默认与 `Priority` 相同。 |

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
| `Members` | 服务中包含的 Members，其格式为 IP：Port。 |
| `Leader` | 当前服务的主节点。 |
| `Specified members` | 运行 Meta 服务的节点。 |
| `Priority` | 为某服务的 Members 设置的优先级，取值为 0 ~ 255 的整数，数值越大，优先级越高。若 `Priority` 中没有显示某节点，则该节点的优先级默认为 1。 |
| `Current priority` | 当前某服务的 Members 的优先级。 `Current priority` 可根据节点状态在优先级不高于 `Priority` 的范围内自动进行动态调整，节点检测到自身异常时，主动降低自身的当前优先级，检测到服务恢复后，再将当前优先级恢复至设置的优先级。节点正常运行时， `Current priority` 与 `Priority` 相同。若 `Current priority` 中没有显示某节点，则该节点当前的 `Current priority` 默认与 `Priority` 相同。 |

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

## 块存储集群 CLI 命令 > 管理集群 > 查看集群服务 > 查看本地 Meta 状态

# 查看本地 Meta 状态

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

| 字段 | 说明 |
| --- | --- |
| `alive_meta_hosts` | 集群中各个主节点的 data\_ip。 |
| `is_leader` | 当前节点是否为 leader 节点。 |
| `leader` | leader 节点的 IP 地址。 |
| `meta_status` | 本地 Meta 状态。 |

---

## 块存储集群 CLI 命令 > 管理集群 > 查看集群服务 > 管理 Zookeeper 服务

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

## 块存储集群 CLI 命令 > 管理集群 > 查看集群服务 > 查看 mongo 服务

# 查看 mongo 服务

## 查看当前 mongo 集群所有成员节点的整体状态

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

## 查看当前 mongo 集群所有成员节点的 IP 地址和端口

**操作方法**

在集群任一节点执行如下命令：

`zbs-node mongo list`

**输出示例**

```
10.0.0.11:27017
10.0.0.13:27017
10.0.0.14:27017
```

## 查看当前 mongo 集群中的 PRIMARY 节点

**操作方法**

在集群任一节点执行如下命令：

`zbs-node mongo leader`

**输出示例**

```
10.0.0.11:27017
```

## 进入 mongo shell 执行查询或维护工作

**操作方法**

在集群中运行了 mongod 服务的节点上执行如下命令，进入 mongo shell 执行查询或维护工作。该命令等同于 mongodb 官方提供的 `mongo` 或 `mongosh` 命令。

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

## 将 mongo 节点和其他节点重新同步

当 mongo 节点由于数据目录异常，或由于与 mongo Primary 节点失去同步，陷入 RECOVERING 状态时，可以使用此命令清空本节点的 mongo 数据目录（/var/lib/mongodb），并重启本节点的 mongod 服务，以重新和其他节点同步数据恢复正常状态。

**操作方法**

在需要重新同步的 mongo 节点执行如下命令：

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

## 块存储集群 CLI 命令 > 管理集群 > 管理集群服务

# 管理集群服务

## 设置服务优先级

为某服务的 Members 设置优先级。

**操作方法**

在集群任一节点执行如下命令，设置 `service_name` 服务的优先级：

`zbs-tool service set_priority [--force] <service_name> <priority>`

| 参数 | 说明 |
| --- | --- |
| `--force` | 可选参数，将 `Current priority` 临时设置为与 `Priority` 相同。 在查看集群中运行的服务时，可以查询到 `Current priority`。  `Current priority` 为当前优先级，可根据节点状态在优先级不高于 `Priority` 的范围内自动进行动态调整。使用 `--force` 时，可确保在当前时刻，`Current priority` 与 `Priority`相同。 |
| `service_name` | 必选参数，待设置优先级的服务名。可通过 `zbs-tool service list` 查询集群中运行的服务及其 Members。 |
| `priority` | 必选参数，服务的优先级。  格式为 `IP:Port:priority`，可对同一个服务的一个或多个 Member 进行设置。如对多个 Member 进行设置，用逗号（,）分隔，例如`IP1:Port1:priority1,IP2:Port2:priority2`。   - IP:Port：指的是某个服务的 Member。 - priority：指的是服务的优先级，取值为 0 ~ 255 的整数，数值越大，优先级越高。 |

**使用示例**

将 taskd 服务的 Member 10.0.100.42:10602 优先级设置为 2；10.0.100.53:10600 的优先级设置为 254。

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

## 块存储集群 CLI 命令 > 管理集群 > 更新集群配置

# 更新集群配置

## 设置集群名称和描述

**操作方法**

在集群任一节点执行如下命令，更新集群名称和描述

`zbs-meta cluster update [--new_name <NEW_NAME>] [--new_desc <NEW_DESC>]`

| 参数 | 说明 |
| --- | --- |
| `--new_name <NEW_NAME>` | 可选参数，更新集群名称。 |
| `--new_desc <NEW_DESC>` | 可选参数，更新集群描述。 |

**输出说明**

执行成功无输出。

## 手动生成 cgroup 配置信息

SMTX ZBS 块存储使用 cgroup 进行进程级别资源隔离，在部署和升级阶段会自动生成 cgroup 配置。若节点 cgroup 配置信息存在人为改动情况，可使用该命令重新生成 cgroup 配置信息并使其生效。

**操作方法**

执行如下命令：

`zbs-deploy-manage config_cgroup`

**输出说明**

输出 cgroup 配置过程。

---

## 块存储集群 CLI 命令 > 管理集群 > 集群部署相关操作

# 集群部署相关操作

## 清理节点部署标记

若集群部署失败，则应在部署失败集群的所有节点清理节点部署标记，使其恢复为未部署状态，以便重新进行扫描和部署。

请注意本条命令仅在部署失败时使用，禁止在其他场景使用。

**操作方法**

在部署失败集群的所有节点执行如下命令：

`zbs-deploy-manage clear_deploy_tag`

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理集群 > 管理集群许可

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
-------------- ------------------------------------
```

---

## 块存储集群 CLI 命令 > 管理集群 > 管理集群拓扑

# 管理集群拓扑

通过对区域、机架组和机架等进行控制，可以合理地将副本分放在不同的区域，以最大限度地提高数据安全性。

## 查看拓扑列表

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta topo list [--show_details]`

| 参数 | 说明 |
| --- | --- |
| `--show_details` | 可选参数，是否展示包含所有 chunk 对象以及 NODE 对象的完整拓扑对象清单。 |

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
| `type` | 拓扑类型：机架、机箱等等 |
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

参数定义如下：

| 名称 | 说明 |
| --- | --- |
| `type` | - type 设为 `rack` 时，创建机架。例如：  `zbs-meta topo create rack new-rack --parent_id default`  创建一个名为 new-rack 的新机架。  - type 设为 `brick` 时，创建机箱。但其后必须要跟 --parent\_id 这个参数，用来指定该机箱位于哪个机架。例如：  `zbs-meta topo create brick new-brick --parent_id d7c626fd`  创建一个名为 new-rack 的新机架，该机箱被置于 ID 号为 d7c626fd 的机架中。 |
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
| `type` | 拓扑类型：机架、机箱等等 |
| `name` | 名称。 |
| `parent_id` | 父节点 ID。 |
| `ring_id` | 拓扑环 ID。 |
| `position.row`, `position.column` | 当前节点置于父节点的位置：横纵坐标。 |
| `capacity.row`, `capacity.column` | 节点自身容量。 |
| `dimension.row`, `dimension.column` | 占用父节点的大小。 |

## 更新机架、机箱、节点的详细信息

**操作方法**

在集群任一节点执行如下命令，更新机箱、机架或节点的信息（对 chunk 物理盘池对象更新其位置信息会自动转换为对 NODE 节点对象进行更新）。

`zbs-meta topo update <id>`

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理集群 > 管理集群接入服务

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
| `UUID` | Session 的 UUID。 |
| `IP` | 存储网络地址。 |
| `Port` | 存储端口。 |
| `Cid` | 节点 Cluster ID。 |
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
| `has_config_push_ability` | 是否能够上传 iscsi config。 |
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
| `Target ID` | iSCSI 协议对象 Target ID，对应 ZBS 里 pool 的概念。 |
| `Session ID` | 管理这个 iSCSI 连接的 `session ID`。 |
| `CID` | iSCSI 连接 ID。 |
| `Transport Type` | 传输协议类型。 |

## 查看会话处理的 NVMe-oF 连接信息

**操作方法**

在集群任一节点执行如下命令，查看会话处理的 NVMe-oF 连接信息。当不指定 Session ID 时，展示所有连接信息。

`zbs-meta session list_nvmf_conn [session_id]`

**输出示例**

```
Host NQN                                                              Host IP      Subsystem ID                            Client Port  Session ID                              CID
--------------------------------------------------------------------  -----------  ------------------------------------  -------------  ------------------------------------  -----
nqn.2014-08.org.nvmexpress:uuid:4483f2e6-1d38-4c7d-bf11-a3dd7f2504ad  10.0.58.200  f540de69-b28b-4ad4-b5bf-8301cab83a3e          35956  126e15a0-ee88-4a6c-9a8a-5e013415624c      3
nqn.2014-08.org.nvmexpress:uuid:4483f2e6-1d38-4c7d-bf11-a3dd7f2504ad  10.0.58.200  f540de69-b28b-4ad4-b5bf-8301cab83a3e          36352  c2226461-cc29-4a55-83e0-ddea07e192e3      2
nqn.2014-08.org.nvmexpress:uuid:4483f2e6-1d38-4c7d-bf11-a3dd7f2504ad  10.0.58.200  f540de69-b28b-4ad4-b5bf-8301cab83a3e          54498  984a181c-092e-4fff-b378-a6c9088f0089      1
nqn.2014-08.org.nvmexpress:uuid:72e7bd3a-0f9f-4972-850a-e72bb9175df8  10.0.58.139  f540de69-b28b-4ad4-b5bf-8301cab83a3e          33141  984a181c-092e-4fff-b378-a6c9088f0089      1
nqn.2014-08.org.nvmexpress:uuid:72e7bd3a-0f9f-4972-850a-e72bb9175df8  10.0.58.139  f540de69-b28b-4ad4-b5bf-8301cab83a3e          46332  c2226461-cc29-4a55-83e0-ddea07e192e3      2
```

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

## 块存储集群 CLI 命令 > 管理集群 > 查看任务运行状态

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
| `ip` | runner 的 IP 地址。 |
| `port` | runner 的 rpc 端口。 |

## 查看运行中或已结束的任务

**操作方法**

使用如下命令查看当前运行中或已结束的任务：

`zbs-task task list_by_status {unfinished|finished} [--task_type <task_type_value>]`

| 参数 | 说明 |
| --- | --- |
| `--task_type <task_type_value>` | task\_type\_value 取值可为以下任何一种：   - storage\_pool：存储池 - backup：备份 - restore：取回 - rsync：同步 - copy\_volume：复制 |

**输出示例**

```
No task found
```

---

## 块存储集群 CLI 命令 > 管理节点 > 收集节点的软硬件信息

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

## 块存储集群 CLI 命令 > 管理节点 > 部署 SSH Key

# 部署 SSH Key

在集群部署或升级阶段会执行该命令进行同一集群中所有节点的 SSH 免密登录配置，配置用户为 smartx。若集群节点中 smartx 用户无法通过 SSH 进行免密登录到其他节点，可以执行该命令生成 SSH key。

**操作方法**

在集群任一节点执行如下命令：

`zbs-deploy-manage deploy_ssh_key`

**输出说明**

输出配置 SSH Key 过程。当输出 `Deploy SSH Key Success` 代表配置成功。

---

## 块存储集群 CLI 命令 > 管理节点 > 关闭与重启节点

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

## 块存储集群 CLI 命令 > 管理节点 > 管理时间同步

# 管理时间同步

## 查询节点的 NTP 同步状态

**操作方法**

在集群任一节点执行如下命令：

`ntpm server show`

**输出示例**

![](https://cdn.smartx.com/internal-docs/assets/e1137223/zbs_cli_guide_02.png)

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `NODE DATAIP` | 节点的存储 IP。 |
| `NODE PRIORITY` | 节点的选主优先级。由内部 NTP 服务器产生。优先级最高的节点优先当选 `Leader`。 |
| `NODE ROLE` | 集群中某个节点的身份。`Leader`表示该节点选主成功，充当内部 NTP 服务器；`Follower`表示该节点同步 `Leader` 节点的时间；`CurrentNode` 表示当前执行命令的节点。 |
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

---

## 块存储集群 CLI 命令 > 管理节点 > 收集节点的硬件信息

# 收集节点的硬件信息

## 收集节点的 USB 信息

**操作方法**

执行如下命令，收集节点的 USB 信息。

`zbs-node collect_usb_device`

**输出说明**

若存在 USB 设备信息更新，输出对应设备的信息，否则无相关输出。

---

## 块存储集群 CLI 命令 > 管理节点 > 管理常驻缓存

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

## 块存储集群 CLI 命令 > 管理节点 > 管理 CPU 安全补丁

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

**注意**：如果想要使配置生效，需要重启集群所有节点主机，可通过 CloudTower 对集群主机依次进行重启。

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

## 块存储集群 CLI 命令 > 管理节点 > 查看节点 watchdog 日志

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

## 块存储集群 CLI 命令 > 管理物理盘 > 查看物理盘信息

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
| `instance_id` | 物理盘所属的物理盘池。 |

## 查询物理盘健康记录

使用物理盘盘符或者物理盘的序列号查询物理盘的健康详情。

**操作方法**

- **使用物理盘盘符查询**

  在物理盘所在的节点上执行如下命令，查询物理盘的健康详情：

  `zbs-node show_disk_status [-p] [/dev/]<disk_name> [--with_rawdata]`

  其中 `disk_name` 表示物理盘的盘符，若磁盘被探测标记为高延时盘；使用 `--with_rawdata` 选项可以输出磁盘原始的 diskstats 数据。

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
| `bus type` | 总线接口类型，如 ata、scsi 等。 |
| `model` | 物理盘型号。 |
| `firmware` | 固件版本。 |
| `disk path` | 物理盘路径。 |
| `disk serial` | 物理盘序列号。 |
| `trace id` | 系统用来跟踪物理盘相关状态的标记（一般是序列号，但也可能是 nguid 等其他信息）。 |
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

## 块存储集群 CLI 命令 > 管理物理盘 > 挂载和卸载

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
| `usage` | 挂载物理盘用途：  - smtx\_system：挂载物理盘用作节点系统盘，该类型物理盘包含系统分区。 - cache：挂载物理盘用作缓存盘。 - data：挂载物理盘用作数据盘。 |
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

## 块存储集群 CLI 命令 > 管理物理盘 > 管理 Partition

# 管理 Partition

Chunk 会对节点上的物理盘（除系统盘以外）进行管理：Partition 管理本地物理盘，先对物理盘进行格式化操作，之后将物理盘挂载到 chunk 上，通过 chunk 对物理盘进行控制。

## 查看当前节点 Partition 信息

**操作方法**

在集群节点执行如下命令，查看当前节点的 Partition 信息：

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
| `UUID` | Partition 分区的唯一 UUID 标识符。 |
| `TOTAL SIZE` | Partition 分区的总容量。 |
| `USED SIZE` | 已使用空间大小。 |
| `NUM CHECKSUM ERRORS` | 校验和的错误数。 |
| `NUM IO ERRORS` | 错误 I/O 数量。 |
| `STATUS` | 分区状态。 |
| `ERRFLAGS` | 错误标记。 |
| `NUM SLOW IO` | SLOW I/O 数量。 |
| `PART UUID` | 物理分区的唯一 UUID 标识符。 |
| `WARNFLAGS` | 告警标记。 |
| `CHECKSUM ENABLE` | 是否启用校验和，`0` 代表不启用，`1` 代表启用。 |

## 格式化指定路径下的 Partition

**操作方法**

- **格式化指定路径下的 Partition**

  在集群节点执行如下命令，格式化该节点指定路径下的 Partition：

  `zbs-chunk [--ins_id <id>] partition format <path>`
- **格式化指定路径下已有数据的 Partition**

  在集群节点执行如下命令，格式化该节点指定路径下已有数据的 Partition：

  `zbs-chunk [--ins_id <id>] partition format --force <path>`

  > **注意**：
  >
  > 执行该命令后，Partition 已有数据会丢失，请谨慎操作。
- **格式化用作全闪 SSD 的 Partition**

  在集群节点执行如下命令，格式化该节点指定路径下已有数据的 Partition：

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

## 将 Partition 挂载到 Chunk

**操作方法**

- **挂载空 Partition**

  在集群节点执行如下命令，将 Partition 挂载至该节点指定路径：

  `zbs-chunk [--ins_id <id>] partition mount <path>`
- **挂载已有数据的 Partition**

  > **注意**：
  >
  > 挂载已有数据的分区是危险操作，使用如下命令时，需格外谨慎。

  在集群节点执行如下命令，将已有数据的 Partition 挂载至该节点指定路径：

  `zbs-chunk [--ins_id <id>] partition mount --force <path>`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数（在多物理盘池环境下是必选参数），物理盘池 ID。指定多物理盘池环境下挂载所使用的物理盘池，需要跟格式化使用的物理盘池保持一致。 |

**输出示例**

```
Partition successfully mounted
```

## 将健康 Partition 从 chunk 卸载

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的 Partition 从 chunk 卸载：

`zbs-chunk partition umount <path>`

**输出示例**

```
Partition is STAGING, umount will be done in background
```

## 停止将健康 Partition 从 chunk 卸载

**操作方法**

在集群节点执行如下命令，停止将该节点指定路径下的 Partition 从 chunk 卸载：

`zbs-chunk partition cancel-umount <path>`

**输出示例**

```
Partition cancel umount submitted
```

## 将异常 Partition 从 chunk 卸载

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的 Partition 从 chunk 卸载，不可取消：

`zbs-chunk partition umount --scheme uuid --mode offline <uuid>`

**输出示例**

```
Partition is STAGING, umount will be done in background
```

## 将 Partition 设置为健康状态

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的 Partition 设置为健康状态：

`zbs-chunk partition set-healthy <path>`

**输出示例**

```
Partition is set healthy!
```

## 将 Partition 设置为不健康状态

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的 Partition 设置为不健康状态：

`zbs-chunk partition set-unhealthy <path>`

**输出示例**

```
Partition is set unhealthy! umount and recover will be done in background
```

## 隔离亚健康状态的 Partition

**操作方法**

在集群节点执行如下命令，隔离指定路径下处于亚健康状态的物理盘分区：

`zbs-chunk partition isolate <path>`

**输出示例**

```
Partition is HIGH_LAT, isolate will be done in background
```

---

## 块存储集群 CLI 命令 > 管理物理盘 > 管理 Journal

# 管理 Journal

每个节点的 SSD 会专门留出部分分区用作 Journal。ZBS 会在 Journal 中记录所做过的操作，以保证数据安全性。

## 查看当前节点 Journal 信息

**操作方法**

在集群节点执行如下命令，查看当前节点的所有 Journal：

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

在输出结果中，有可能多行对应一次 journal mount 命令成功挂载的 Journal（跟挂载 Journal 的空间有关）。

| 参数 | 说明 |
| --- | --- |
| `INS ID` | 物理盘池 ID（仅当多物理盘池且未进行过滤时显示）。 |
| `PATH` | Journal 分区路径。 |
| `RESERVED ENTRIES` | Journal Group 已使用 Entry 数量。 |
| `MAX ENTRIES` | Journal Entry 数量。 |
| `SEQ NO` | Journal 已复用次数。 |
| `STATUS` | Journal 状态：IDLE，BUSY。 |
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

## 格式化指定路径下的 Journal

**操作方法**

- **格式化指定路径下的空 Journal**

  在集群节点执行如下命令，将该节点指定路径下的空 Journal 分区格式化：

  `zbs-chunk [--ins_id <id>] journal format <path>`
- **格式化指定路径下的已有数据的 Journal**

  在集群节点执行如下命令，将该节点指定路径下已有数据的 Journal 格式化：

  `zbs-chunk [--ins_id <id>] journal format --force <path>`

  > **注意**：
  >
  > 执行该命令后，Journal 已有数据会丢失，请谨慎操作。

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

## 将 Journal 挂载到 Chunk

**操作方法**

在集群节点执行如下命令，将 Journal 挂载到该节点指定路径下的 chunk 上：

`zbs-chunk [--ins_id <id>] journal mount <path>`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数（在多物理盘池环境下是必选参数），物理盘池 ID。指定多物理盘池环境下挂载所使用的物理盘池，需要跟格式化使用的物理盘池保持一致。 |

**输出示例**

```
Journal successfully mounted
```

## 将 Journal 从 chunk 卸载

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的 Journal 从 chunk 卸载：

`zbs-chunk journal umount <path>`

**输出示例**

```
Journal successfully unmounted
```

## 将 Journal 设置为健康状态

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的 Journal 设置为健康状态：

`zbs-chunk journal set-healthy <path>`

**输出示例**

```
Journal device is set healthy!
```

## 将 Journal 设置为不健康状态

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的 Journal 设置为不健康状态：

`zbs-chunk journal set-unhealthy <path>`

**输出示例**

```
Journal device is set unhealthy!
```

## 刷新节点的所有 Journal

**操作方法**

在集群节点执行如下命令，刷新该节点的所有 Journal：

`zbs-chunk journal flush`

**输出示例**

```
Journal successfully flushed
```

**输出说明**

此命令是异步操作，即没有完成前也会立即返回。

---

## 块存储集群 CLI 命令 > 管理物理盘 > 管理 Cache

# 管理 Cache

在 SSD 中，除了需要 Journal 来记录所进行过的操作，还会用部分分区用作 Cache，来对数据读写进行加速。

## 查看当前节点 Cache 信息

查看节点中查询活跃 Cache、非活跃 Cache、干净 Cache、空闲 Cache 的大小及占比。

> **注意**：
>
> 上述四个指标的值相加不一定等于总 Cache 的大小，因为在 SMTX ZBS 5.6.0 及以上的版本中，Cache 分区内部划分出了一部分用作集群的性能分区，而前三个指标是不把性能分区统计在内的。

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
| `CACHE HIT RATE` | 缓存命中率，在 ZBS 5.6.0 及以上版本中，Cache 仅代表读缓存。 |
| `TOTAL ACTIVE` | 活跃 Cache 大小及其占比（不包含性能分区），预期长期是 0。 |
| `TOTAL INACTIVE` | 非活跃 Cache 大小及其占比（不包含性能分区），预期长期是 0。 |
| `TOTAL CLEAN` | 干净 Cache 大小及其占比（不包含性能分区），预期长期大于 0。 |
| `TOTAL PERF USED` | 性能层空间总体占用。 |
| `TOTAL FREE` | 空闲 Cache 大小及其占比（包含性能分区）。 |
| `TOTAL` | 总 Cache 大小（包含性能分区）。 |
| `INS ID` | 物理盘池 ID（仅当多物理盘池且未进行过滤时显示）。 |
| `PATH` | 分区路径。 |
| `DEVICE ID` | 物理盘 ID。 |
| `UUID` | Cache 分区的唯一 UUID 标识符。 |
| `NUM IO ERRORS` | 错误 I/O 数量。 |
| `STATUS` | 分区状态。 |
| `ERRFLAGS` | 错误标记。 |
| `NUM SLOW IO` | SLOW I/O 数量。 |
| `PART UUID` | 物理分区的唯一 UUID 标识符。 |
| `WARNFLAGS` | 告警标记。 |
| `TOTAL SIZE` | Cache 分区的总容量。 |
| `USED SIZE` | 已使用空间大小。 |

## 格式化指定路径下的 Cache

**操作方法**

- **格式化指定路径下的 Cache**

  在集群节点执行如下命令，格式化该节点指定路径下的 Cache：

  `zbs-chunk [--ins_id <id>] cache format <path>`
- **格式化指定路径下已有数据的 Cache**

  在集群节点执行如下命令，格式化该节点指定路径下已有数据的 Cache：

  `zbs-chunk [--ins_id <id>] cache format --force <path>`

  > **注意**：
  >
  > 执行该命令后，Cache 已有数据会丢失，请谨慎操作。

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

## 将 Cache 挂载到 Chunk

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的 Cache 挂载到 Chunk：

`zbs-chunk [--ins_id <id>] cache mount <path>`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数（在多物理盘池环境下是必选参数），物理盘池 ID。指定多物理盘池环境下挂载所使用的物理盘池，需要跟格式化使用的物理盘池保持一致。 |

**输出示例**

```
Successfully mounted
```

## 将健康 Cache 从 chunk 卸载

**操作方法**

在集群节点执行如下命令，将该节点指定路径的 Cache 从 chunk 上卸载：

`zbs-chunk cache umount <path>`

**输出示例**

```
Cache device is STAGING now, umount will be done in background
```

## 停止将健康 Cache 从 chunk 卸载

**操作方法**

在集群节点执行如下命令，停止将该节点指定路径的 Cache 从 chunk 上卸载：

`zbs-chunk cache cancel-umount <path>`

**输出示例**

```
Cache cancel umount submitted
```

## 将异常 Cache 从 chunk 卸载

**操作方法**

在集群节点执行如下命令，将该节点指定路径的 Cache 从 chunk 上卸载，不可取消：

`zbs-chunk cache umount --scheme uuid --mode offline <uuid>`

**输出示例**

```
Cache device is STAGING now, umount will be done in background
```

## 将 Cache 设置为健康状态

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的 Cache 设置健康状态：

`zbs-chunk cache set-healthy <path>`

**输出示例**

```
Cache device is set healthy!
```

## 将 Cache 设置为不健康状态

**操作方法**

在集群节点执行如下命令，将该节点指定路径下的 Cache 设置为不健康状态：

`zbs-chunk cache set-unhealthy <path>`

**输出示例**

```
Cache device is set unhealthy! umount and recover will be done in background
```

---

## 块存储集群 CLI 命令 > 管理 Chunk

# 管理 Chunk

Chunk 运行在每一台服务器节点上，主要提供三类服务：

- 负责和 meta 的通信，向 meta 提供 chunk 的心跳信息、本节点的使用容量和数据块的副本数等信息。
- 负责处理客户端的读写请求。
- LSM（Local Storage Manager）：负责管理本节点上的除了系统盘以外的所有本地存储盘。包括 PCI-SSD、SSD、SATA 和 SAS 盘。按照存储盘的用途可以分为缓存盘和数据盘。

每个节点的 chunk 服务都会注册到 meta 服务，也就是元数据服务中，然后可以通过 meta 来管理整个集群。

---

## 块存储集群 CLI 命令 > 管理 Chunk > 将节点 chunk 注册到 meta 中

# 将节点 chunk 注册到 meta 中

Chunk 服务在 ZBS 中负责数据管理，每个节点的 chunk 服务都会注册到 meta 服务，也就是元数据服务中，然后可以通过 meta 来管理整个集群。

**操作方法**

在集群任一节点执行如下命令，将节点 chunk 注册到 meta 中：

`zbs-meta chunk register <ip> <chunk_rpc_port> [--data_port <chunk_data_port>]`

| 参数 | 说明 |
| --- | --- |
| `ip` | Chunk 存储网络的 IP 地址。 |
| `chunk_port` | Chunk 的端口号。 |
| `--data_port <chunk_data_port>` | 可选参数（在多物理盘池环境下是必选参数），Chunk 的数据通信端口号。 |

---

## 块存储集群 CLI 命令 > 管理 Chunk > 查看 Chunk

# 查看 Chunk

## 查看集群中的 chunk 列表

**操作方法**

`zbs-meta chunk list [--show_details]`

参数定义如下：

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
| `HostName` | Chunk 节点主机名。 |
| `Port` | Chunk RPC 端口。 |
| `Storage Pool` | 所属 Storage Pool。 |
| `Use State` | 使用状态。 |
| `Link Status` | 连接状态。 |
| `Data Capacity` | 容量层提供的总数据空间大小。 |
| `Valid Space` | 容量层有效数据空间大小。 |
| `Allocated Space` | 容量层已分配的数据空间大小（Meta 认为的空间消耗）。 |
| `Failure Data Space` | 容量层失效数据空间大小。 |
| `Perf Data Capacity` | 性能层提供的总数据空间大小。 |
| `Perf Valid Space` | 性能层有效数据空间大小。 |
| `Perf Allocated Space` | 性能层已分配的数据空间大小（Meta 认为的空间消耗）。 |
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
| `CID` | chunk ID。 |
| `Data Port` | chunk 数据通信端口。 |
| `Status` | 连接状态。 |
| `Cap Size` | 容量层提供的总数据空间大小。 |
| `Cap Valid` | 容量层有效数据空间大小。 |
| `Cap Alloc` | 容量层已分配的数据空间大小（Meta 认为的空间消耗）。 |
| `Perf Size` | 性能层提供的总数据空间大小。 |
| `Perf Valid` | 性能层有效数据空间大小。 |
| `Perf Alloc` | 性能层已分配的数据空间大小（Meta 认为的空间消耗）。 |
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
| `data_port` | chunk 使用数据通信端口。 |

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
| `Storage Pool` | 所属 Storage Pool。 |
| `Use State` | 使用状态。 |
| `Link Status` | 连接状态。 |
| `Data Capacity` | 容量层提供的总数据空间大小。 |
| `Valid Space` | 容量层有效数据空间大小。 |
| `Allocated Space` | 容量层已分配的数据空间大小（Meta 认为的空间消耗）。 |
| `Failure Data Space` | 容量层失效数据空间大小。 |
| `Perf Data Capacity` | 性能层提供的总数据空间大小。 |
| `Perf Valid Space` | 性能层有效数据空间大小。 |
| `Perf Allocated Space` | 性能层已分配的数据空间大小（Meta 认为的空间消耗）。 |
| `Perf Failure Data Space` | 性能层失效数据空间大小。 |
| `Registered Date` | 注册时间。 |
| `LSM Version` | LSM 版本。 |
| `Zone` | 所属可用域。 |
| `Maintenance Mode` | 是否处于维护模式。 |

## 查看 chunk 所有 pid

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
| `pid` | 该 chunk 管理的 pid 列表。 |
| `thin pid` | 该 chunk 管理的精简置备 pid 列表。 |
| `thick pid` | 该 chunk 管理的厚置备 pid 列表。 |
| `rx pid` | 该 chunk 作为迁移或恢复目的端接受的 pid 列表。 |
| `tx pid` | 该 chunk 正在被迁移或恢复移除的 pid 列表。 |
| `recover pid` | 该 chunk 作为迁移或恢复源端接受的 pid 列表。 |
| `new thin pid` | 该 chunk 新创建的精简置备 pid 列表。 |
| `thin reserved pid` | 该 chunk 上预留的精简置备 pid 列表。 |
| `thick reserved pid` | 该 chunk 上预留的厚置备 pid 列表。 |

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

在集群节点执行如下命令，查看该节点全部或特定物理盘池 chunk 信息：

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

Chunk Capability:
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
| `LSM_CAP_DISK_SAFE_UMOUNT` | True 代表 LSM 提供了安全卸载物理盘的能力。 |
| `LSM_CAP_DISK_REJECT_UNHEALTHY` | True 代表 LSM 会拒绝接入不健康的物理盘。 |
| `LSM_CAP_PARTITION_ISOLATE` | True 代表 LSM 提供了隔离物理 Partition 盘的能力。 |
| `LSM_CAP_COMPARE_EXTENT` | True 代表 LSM 提供了比较 Extent 数据差异的能力。 |
| `LSM_CAP_CACHE_ISOLATE` | True 代表 LSM 提供了隔离物理 Cache 盘的能力。 |
| `LSM IOPS` | LSM 当前 IOPS。 |
| `LSM BW` | LSM 当前带宽。 |
| `Writeback IOPS` | LSM 从 Cache 写回 Partition 的 IOPS。 |
| `Writeback BW` | LSM 从 Cache 写回 Partition 的 BW。 |
| `Unmap IOPS` | Unmap 当前 IOPS。 |
| `Unmap BW` | Unmap 当前带宽。 |
| `Waiting Reclaim Items` | 等待回收的 Extent 数量。 |
| `Use RDMA` | 是否启用了 RDMA。 |
| `Agile Recover` | 是否启用了敏捷恢复，Chunk 退出维护模式之后，敏捷恢复能够更高效完成数据恢复。 |
| `iSCSI` | iSCSI Server 运行状态。 |
| `NFS` | NFS Server 运行状态。 |
| `Vhost` | Vhost Server 运行状态。 |
| `NVMe-oF` | NVMe-oF Server 运行状态。 |
| `metric_on` | True 代表开启了 metric 统计。 |
| `trace_on` | True 代表开启了 IO trace 统计。 |
| `adaptive_trace_on` | True 代表开启了动态 IO trace 统计。 |
| `accel_copy_mode` | 硬件加速拷贝运行状态（`ACCEL_COPY_DISABLED`表示禁用，`ACCEL_COPY_BY_DSA`表示启用，`ACCEL_COPY_BY_SOFTWARE`表示配置错误未能正确启用硬件加速拷贝）。 |
| `chunk_instances_num` | 当前节点的物理盘池数量。 |

## 查看 chunk 计数器

chunk 的读写操作对 chunk 的影响会暂时记录在 chunk 的计数器中。

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
| `--start <START_PID>` | 可选参数，extent 的起始 pid，默认值为 `0`。 |
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
listall extents done.
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

## 查看 chunk 的实时 I/O Metric 数据

**操作方法**

在集群节点执行如下命令，可查看当前节点的 I/O Metric：

`zbs-chunk [--ins_id <id>] metric <METRIC_TYPE>`

| 参数 | 说明 |
| --- | --- |
| `--ins_id <id>` | 可选参数，物理盘池 ID。可用来在多物理盘池环境下过滤仅输出特定物理盘池的信息。 |
| `METRIC_TYPE` | 指定要查看实时 Metric 数据的 I/O 类型，可选值为 `app`（业务 IO），`sink`（下沉 IO），`reposition`（ Recover 和 Migrate IO），`fc`（性能层限流）。 |

**输出示例**

查看业务 I/O 的 Metric (`METRIC_TYPE` 取值为 `app`)

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

查看下沉 I/O 的 Metric (`METRIC_TYPE` 取值为 `sink`)

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

查看 Recover 和 Migrate I/O 的 Metric (`METRIC_TYPE` 取值为 `reposition`)

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

查看性能层限流的 Metric (`METRIC_TYPE` 取值为 `fc`)

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
Flow Controller    Dest Perf Thin Not Free Ratio      Avail Tokens    Used Tokens No Wait    Used Tokens After Wait    Over Used Tokens    Avg Wait Token Lat    Avg Wait Token Num
-----------------  -------------------------------  --------------  ---------------------  ------------------------  ------------------  --------------------  --------------------
1 -> 1             2.0%                                   10000000                      0                         0                   0                     0                     0
1 -> 2             7.0%                                   10000000                      0                         0                   0                     0                     0
1 -> 3             7.0%                                   10000000                      0                         0                   0                     0                     0
1 -> 4             2.0%                                   10000000                      0                         0                   0                     0                     0
```

**输出说明**

IO Metric 的输出

| 参数 | 说明 |
| --- | --- |
| `Access Perf Read` | Access 发起的性能层读 I/O。 |
| `Access Perf Write` | Access 发起的性能层写 I/O。 |
| `Access Cap EC Read` | Access 发起的容量层 EC 读 I/O。 |
| `Access Cap EC Write` | Access 发起的容量层 EC 写 I/O 。 |
| `Access Cap Replica Read` | Access 发起的容量层副本读 I/O。 |
| `Access Cap Replica Write` | Access 发起的容量层副本写 I/O。 |
| `Access Perf Promote Write` | Access 为凑齐特定大小 I/O 长度而发起的 Promote IO，写性能层的部分。 |
| `Access Cap EC Promote Read` | Access 为凑齐特定大小 I/O 长度而发起的 Promote IO，读容量层 EC 的部分。 |
| `Access Cap Rep Promote Read` | Access 为凑齐特定大小 I/O 长度而发起的 Promote IO，读容量层副本的部分。 |
| `From Remote Perf Read` | 从其他 Access 发来的性能层读 I/O。 |
| `From Remote Perf Write` | 从其他 Access 发来的性能层写 I/O。 |
| `From Remote Cap EC Read` | 从其他 Access 发来的容量层 EC 读 I/O。 |
| `From Remote Cap EC Write` | 从其他 Access 发来的容量层 EC 写 I/O。 |
| `From Remote Cap Replica Read` | 从其他 Access 发来的容量层副本读 I/O 。 |
| `From Remote Cap Replica Write` | 从其他 Access 发来的容量层副本写 I/O。 |
| `From Local Perf Read` | 从本地 Access 发来的性能层读 I/O。 |
| `From Local Perf Write` | 从本地 Access 发来的性能层写 I/O。 |
| `From Local Cap EC Read` | 从本地 Access 发来的容量层 EC 读 I/O。 |
| `From Local Cap EC Write` | 从本地 Access 发来的容量层 EC 写 I/O。 |
| `From Local Cap Replica Read` | 从本地 Access 发来的容量层副本读 I/O。 |
| `From Local Cap Replica Write` | 从本地 Access 发来的容量层副本写 I/O。 |

性能层限流 Metric 的输出（Flow Manager 相关）

| 参数 | 说明 |
| --- | --- |
| `Flow Manager` | 分配 Token 的模块，源端 Chunk（分配 Token）-> 目的端 Chunk（申请 Token）。 |
| `Flow control enable` | 性能层限流是否已开启。 |
| `Avail token` | 当前空闲 Token 的数量。 |
| `Perf thin used ratios` | 当前性能层使用比例。 |
| `Perf thin free ratio` | 当前性能层空闲比例。 |
| `Flow Controller` | 申请 Token 的模块，源端 Chunk（申请 Token）-> 目的端 chunk （分配 Token）。 |
| `Requested Tokens` | 最近 1s 累计希望申请 Token 的数量（该值可参考性意义较低，一般可以忽略）。 |
| `Used Tokens` | 最近 1s 消费的 Token 数量。 |
| `Over Used Tokens` | 最近 1s 没有拿 Token 就下发副本 I/O 的数量，一般可能是由于 DataChannel 失联、拿 Token 超时等原因。 |

性能层限流 Metric 的输出（Flow Controller 相关）

| 参数 | 说明 |
| --- | --- |
| `Flow Controller` | 申请 Token 的模块，源端 Chunk（申请 Token）-> 目的端 chunk （分配 Token）。 |
| `Dest Perf Thin Not Free Ratio` | 目的端 chunk 的性能层空间使用率。 |
| `Avail Tokens` | 当前时刻持有到目的节点的 Tokens。未限速时数值固定为 `10000000`。 |
| `Used Tokens No Wait` | 最近 1s 不需要等待就获得 Token 的副本 I/O 数量。 |
| `Used Tokens After Wait` | 最近 1s 需要等待才获得 Token 的副本 I/O 数量。 |
| `Over Used Tokens` | 没有拿 Token 就下发的副本 I/O 的数量，一般可能是由于 DataChannel 失联、拿 Token 超时等原因。 |
| `Avg Wait Token Lat` | 最近 1s 等待 Token 的延时。 |
| `Avg Wait Token Num` | 最近 1s 等待 Token 的副本 I/O 数量。 |

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
| `Inactive interval` | 判定 Extent 是否为非活跃状态的时间阈值。 |
| `Sink inactive lease` | 是否对非活跃 Extent 进行下沉。 |
| `Cap directly write policy` | 当前节点的容量层直写策略。 |
| `Sinkable block lru info` | 当前节点的可下沉 Block LRU 信息。 |
| `Potential sinkable block lru info` | 当前节点的潜在可下沉 Block LRU 信息。 |
| `Accelerate cids` | 当前节点感知的需要加速下沉的 chunk 列表。 |
| `Accelerate blocks` | 当前节点感知的需要加速下沉的 Block 数量。 |
| `Inactive extents` | 当前节点的非活跃 Extent 数量。 |
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

## 块存储集群 CLI 命令 > 管理 Chunk > 将某个 chunk 从节点移除

# 将某个 chunk 从节点移除

仅能操作 IDLE 状态的 Chunk，即只能移除已经从存储池中移除的 Chunk。

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta chunk remove <data_ip> <data_port>`

| 参数 | 说明 |
| --- | --- |
| `data_ip` | 节点存储 IP 地址。 |
| `data_port` | chunk 使用数据通信端口。 |

> **说明**：
>
> 多物理盘池环境下，需要按照物理盘池 ID 从大到小的顺序移除。

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理 Chunk > 设置 chunk 进入或退出存储维护模式

# 设置 chunk 进入或退出存储维护模式

**操作方法**

在集群任一节点执行如下命令，设置 chunk 对应节点进入或退出存储维护模式。

`zbs-meta chunk set_maintenance <cid> <is_maintenance> [--expire_duration_s <EXPIRE_DURATION_S>]`

| 参数 | 说明 |
| --- | --- |
| `cid` | chunk ID。该 chunk 所在节点全部 chunk 都将进入或退出存储维护模式。 |
| `is_maintenance` | 取值为 true 或 false，分别表示是否进入维护模式。 |
| `--expire_duration_s <EXPIRE_DURATION_S>` | 可选参数，设置维护模式过期时间，仅在进入存储维护模式时有效。如果不设置该参数，则系统默认为最大值 604800 秒（7 天）。 |

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
| `Storage Pool` | 所属 Storage Pool。 |
| `Use State` | 使用状态。 |
| `Link Status` | 连接状态。 |
| `Data Capacity` | 容量层提供的总数据空间大小。 |
| `Valid Space` | 容量层有效数据空间大小。 |
| `Allocated Space` | 容量层已分配的数据空间大小（Meta 认为的空间消耗）。 |
| `Failure Data Space` | 容量层失效数据空间大小。 |
| `Perf Data Capacity` | 性能层提供的总数据空间大小。 |
| `Perf Valid Space` | 性能层有效数据空间大小。 |
| `Perf Allocated Space` | 性能层已分配的数据空间大小（Meta 认为的空间消耗）。 |
| `Perf Failure Data Space` | 性能层失效数据空间大小。 |
| `Registered Date` | 注册时间。 |
| `LSM Version` | LSM 版本。 |
| `Zone` | 所属可用域。 |
| `Maintenance Mode` | 是否处于维护模式。 |

---

## 块存储集群 CLI 命令 > 管理 Chunk > 设置 chunk 的数据校验模式

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

## 块存储集群 CLI 命令 > 管理 Chunk > 重新加载 chunk 配置或更新 Zookeeper 信息

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

## 块存储集群 CLI 命令 > 管理 Chunk > 查看或清除异常物理盘记录

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

## 块存储集群 CLI 命令 > 管理 Chunk > 更新本地 chunk 的次级数据网络 IP

# 更新本地 chunk 的次级数据网络 IP

**操作方法**

在当前集群节点执行如下命令，更新本地 chunk 的次级数据网络 IP。

`zbs-chunk address update_secondary_data_ip <ip>`

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理 Chunk > 查看 chunk 线程轮询状态

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

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储池

# 管理存储池

存储池是 SMTX ZBS 块存储对存储介质进行组织的单元。不同的存储介质可以加入不同的存储池，使得存储池具备不同的存储特性，例如：SSD/HDD 混合存储池，全 SSD 存储池等（在目前 ZBS 的实现中，服务器是可以加入存储池的最小单元）。也可以指定某一个数据存储、NFS export 或 iSCSI 目标到某一个特定的存储池, 然后其上的数据卷都会存放在指定存储池的 chunk 上。系统默认的存储池是 “system”。用户可以把存储池的 chunk 移动到另一个存储池。

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
| `chunks` | 存储池的 Chunk。 |

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
| `chunks` | 存储池的 Chunk。 |

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

## 在存储池中添加 Chunk

**操作方法**

在集群任一节点执行如下命令，在存储池中添加 Chunk。

`zbs-meta storage_pool add_chunk <storage_pool_id> <chunk_id>`

**输出说明**

执行成功无输出。

## 在存储池中移除 Chunk

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

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理数据存储

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
| `--replica_num <REPLICA_NUM>` | 设置数据存储内新建 Volume 的默认副本数，可设置为 2 副本或 3 副本。 |
| `--ec_algo <EC_ALGO>` | 设置 EC 算法，当冗余模式为 EC 时必须设置，默认为 RS。 |
| `--encrypt_method <ENCRYPT_METHOD>` | 设置数据加密方法，默认为不加密 。 |
| `--ec_k <EC_K>` | 设置 EC 算法参数 K，参数范围为 [2，23]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--ec_m <EC_M>` | 设置 EC 算法参数 M，参数范围为 [1，4]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--thin_provision <THIN_PROVISION>` | True 或 False，表示是否设置数据存储新建 Volume 的置备方式为精简置备。 |
| `--desc <DESC>` | 设置数据存储描述。 |
| `--storage_pool_id <STORAGE_POOL_ID>` | 指定创建数据存储的 Storage Pool ID。 |
| `--whitelist <WHITELIST>` | IP 访问白名单。 |
| `--iops <IOPS>` | 设置数据存储内新建 Volume 的读写总 IOPS 上限值。 |
| `--iops_rd <IOPS_RD>` | 设置读 IOPS 的上限值。 |
| `--iops_wr <IOPS_WR>` | 设置写 IOPS 的上限值。 |
| `--iops_max <IOPS_MAX>` | 设置读写总 IOPS 突发的上限值。 |
| `--iops_rd_max <IOPS_RD_MAX>` | 设置读 IOPS 突发的上限值。 |
| `--iops_wr_max <IOPS_WR_MAX>` | 设置写 IOPS 突发的上限值。 |
| `--iops_max_length <IOPS_MAX_LENGTH>` | 设置读写总 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_rd_max_length <IOPS_RD_MAX_LENGTH>` | 设置读 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_wr_max_length <IOPS_WR_MAX_LENGTH>` | 设置写 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_io_size <IOPS_IO_SIZE>` | 使用 IOPS 限速时，假定的平均 I/O 数据量大小。 |
| `--bps <BPS>` | 设置数据存储内新建 Volume 的读写总带宽限制，单位为 Bps。 |
| `--bps_rd <BPS_RD>` | 设置读带宽的上限值。 |
| `--bps_wr <BPS_WR>` | 设置写带宽的上限值。 |
| `--bps_max <BPS_MAX>` | 设置读写总带宽在发生 I/O 突发时的上限值。 |
| `--bps_rd_max <BPS_RD_MAX>` | 设置读带宽在发生 I/O 突发时的上限值。 |
| `--bps_wr_max <BPS_WR_MAX>` | 设置写带宽在发生 I/O 突发时的上限值。 |
| `--bps_max_length <BPS_MAX_LENGTH>` | 设置在发生 I/O 突发时，以读写总带宽上限进行 I/O 的持续时长限制。单位为秒。 |
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

在集群任一节点执行如下命令，更新数据存储名称、副本数、置备模式和 IP 白名单。更新数据存储不影响已经创建的 Volume。

`zbs-meta pool update [--new_pool_name <NEW_POOL_NAME>] [--replica_num <REPLICA_NUM>] [--thin_provision {true|false}] [--desc <DESC>] [--whitelist <WHITELIST>] [--encrypt_method <ENCRYPT_METHOD>] <pool_name>`

| 参数 | 说明 |
| --- | --- |
| `--new_pool_name` | 可选参数，更新数据存储名称。 |
| `--replica_num` | 可选参数，更新数据存储中 Volume 的默认副本数，不影响已经创建好的 Volume。 |
| `--thin_provision {true|false}` | 可选参数，更新数据存储中 Volume 的默认置备模式，`true` 和 `false` 表示是否为精简配置。 |
| `--desc` | 可选参数，更新数据存储的详细描述。 |
| `--whitelist` | 可选参数，IP 访问白名单。 |
| `--encrypt_method` | 可选参数，更新数据加密方法 |
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

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷

# 管理存储卷

存储卷（Volume），是 SMTX ZBS 块存储对外提供的最基本的数据结构。它可以对应到一个虚拟机的存储卷，也可以对应到 iSCSI 中的一个 LUN。用户可以通过 Volume 来创建虚拟机或者对虚拟机进行添加磁盘的操作。这一切都是基于存储卷进行的，Volume 参数可以让用户直接对存储卷进行操作。

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷 > 查看存储卷

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
| `Parent ID` | 存储卷所属 Pool ID。 |
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
| `Prefer CID` | IO 亲和 Chunk，存储卷的 Extent 会更倾向于存储在该 Chunk上。 |
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
| `Parent ID` | 存储卷所属 Pool ID。 |
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
| `Prefer CID` | I/O 亲和 Chunk，存储卷的 Extent 会更倾向于存储在该 Chunk上。 |
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
| `Parent ID` | 存储卷所属 Pool ID。 |
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
| `Prefer CID` | I/O 亲和 Chunk，存储卷的 Extent 会更倾向于存储在该 chunk 上。 |
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

## 查看节点活跃访问的存储卷

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
| `Prefer CID` | I/O 亲和 Chunk，存储卷的 Extent 会更倾向于存储在该 Chunk上。 |

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

## 查看存储卷数据在 Cache 和 Partition 上的分布情况

**操作方法**

- 在集群任一节点执行如下命令，查看指定名称的存储卷的数据在 Cache 和 Partition 上的分布情况：

  `zbs-tool volume show_dist <pool_name> <volume_name>`
- 在集群任一节点执行如下命令，查看指定 ID 的存储卷的数据在 Cache 和 Partition 上的分布情况：

  `zbs-tool volume show_dist_by_id <volume_id>`

**输出示例**

```
Volume used performance cache size: 1024.00 MiB
Volume used read cache size: 1024.00 KiB
Volume used partition size: 1024.00 MiB
```

## 查看存储卷数据在 Cache 和 Partition 上的分布情况

**操作方法**

- 在集群任一节点执行如下命令，查看指定名称的存储卷的数据在 Cache 和 Partition 上的分布情况：

  `zbs-tool volume show_dist <pool_name> <volume_name>`
- 在集群任一节点执行如下命令，查看指定 ID 的存储卷的数据在 Cache 和 Partition 上的分布情况：

  `zbs-tool volume show_dist_by_id <volume_id>`

**输出示例**

```
Volume used performance cache size: 1024.00 MiB
Volume used read cache size: 1024.00 KiB
Volume used partition size: 1024.00 MiB
```

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷 > 查看存储卷上的数据块信息

# 查看存储卷上的数据块信息

查看存储卷的 lextent 和 pextent，以及 pextent 在各个 chunk 上的副本数量。

**操作方法**

- 在集群任一节点执行如下命令，查看指定名称的存储卷的数据块信息：

  `zbs-meta volume show <pool_name> <volume_name> [--show_lextents] [--show_pextents] [--show_replica_distribution]`
- 在集群任一节点执行如下命令，查看指定 ID 的存储卷的数据块信息：

  `zbs-meta volume show_by_id <volume_id> [--show_lextents] [--show_pextents] [--show_replica_distribution]`

| 参数 | 说明 |
| --- | --- |
| `--show_lextents` | 可选参数，选择是否显示存储卷的 lextent 信息。 |
| `--show_pextents` | 可选参数，选择是否显示存储卷的 pextent 信息。 |
| `--show_replica_distribution` | 可选参数，选择是否显示该存储卷的 pextents 在各个 chunk 上的副本数量。 |

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
In chunk Sizes
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

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷 > 创建存储卷

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
| `--encrypt_method <ENCRYPT_METHOD>` | 设置数据加密方法，默认为不加密 。 |
| `--ec_block_size <EC_BLOCK_SIZE>` | 设置 EC 算法的使用的数据块大小。当冗余模式为 EC 时，默认为 4096，否则默认为 `None`。 |
| `--read_only <READ_ONLY>` | 设置存储卷是否为只读模式，可设置为 `True` 或 `False`。 |
| `--snapshot <SNAPSHOT>` | 设置快照路径，从快照中创建一个存储卷。 |
| `--snapshot_id <SNAPSHOT_ID>` | 设置快照 ID，从快照中创建一个存储卷。 |
| `--stripe_num <STRIPE_NUM>` | 新建存储卷的条带数。 |
| `--stripe_size <STRIPE_SIZE>` | 新建存储卷的条带大小。 |
| `--preferred_cid <PREFERRED_CID>` | 设置倾向节点的 chunk ID（多物理盘池环境下节点中任一 chunk ID 均可），Meta 在分配 PExtent 副本时，会尽量靠近该 chunk 所在的节点。 |
| `--prioritized <PRIORITIZED>` | 设置存储卷的 prioritized 属性，即设置存储卷的数据是否都需要维持在性能层中，可设置为 `True` 或 `False`。 |

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷 > 在数据存储中删除存储卷

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

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷 > 将存储卷移至新数据存储中

# 将存储卷移至新数据存储中

**操作方法**

在集群任一节点执行如下命令，将存储卷移至新的数据存储中。：

`zbs-meta volume move <src_pool_name> <volume_name> <dst_pool_name>`

| 参数 | 说明 |
| --- | --- |
| `src_pool_name` | 源数据存储。 |
| `dst_pool_name` | 目的数据存储。 |
| `volume_name` | 待移动的存储卷名称。 |

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷 > 提升存储卷副本数

# 提升存储卷副本数

**操作方法**

在集群任一节点执行如下命令，提升存储卷副本数：

`zbs-meta volume update <pool_name> <volume_name> [--replica_num <REPLICA_NUM>]`

| 参数 | 说明 |
| --- | --- |
| `--prefer_cid` | 副本优先选择存储的 chunk ID。 |
| `--replica_num <REPLICA_NUM>` | 可选参数，更新存储卷的副本数, 只支持提高，不支持降低。 |
| `pool_name` | 必选参数，Pool 名称。 |
| `volume_name` | 必选参数，存储卷名称。 |

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷 > 调整存储卷大小

# 调整存储卷大小

**操作方法**

在集群任一节点执行如下命令调整存储卷的大小，单位为 GiB：

`zbs-meta volume resize <pool_name> <volume_name> <size>`

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷 > 管理接入点

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
| `--include_cow` | 可选参数，允许更改处于 COW 状态的 Extent 的本地接入点。 |

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷 > 读取存储卷数据

# 读取存储卷数据

**操作方法**

在集群节点执行如下命令，从指定的数据存储中读取指定名字的存储卷，并把读取结果存入到指定名字的文件中。若不指定文件名，则输出到屏幕。

`zbs-chunk volume read <pool_name> <volume_name> -o <file_name>`

**输出示例**

```
smartx/test1 100% |#############################################################################################| 60.69 M/s Time: 00:00:17
```

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷 > 将数据写入存储卷

# 将数据写入存储卷

**操作方法**

在集群节点执行如下命令，把指定名字的文件中的数据写入到指定数据存储的存储卷中。若没有指定文件名，则从键盘接收输入。

`zbs-chunk volume write <pool_name> <volume_name> -i <file_name>`

**输出示例**

```
smartx/test1 100% |#############################################################################################| 24.81 M/s Time: 00:00:43
```

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷 > 复制存储卷

# 复制存储卷

**操作方法**

在集群任一节点执行如下命令，将源 Volume 复制到目的 Volume。

`zbs-task copy_volume copy <src_volume_id> <dst_volume_id> <src_hosts> <dst_hosts>`

`src_hosts` 和 `dst_hosts` 格式为 "ip:10201:10206,ip:10201:10206"。

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

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷 > 下沉存储卷的性能层数据

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

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷快照 > 查看存储卷快照

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

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷快照 > 创建存储卷快照

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

`volumes` 为待创建快照的 Volume。可以输入多个 Volume，并以英文逗号 `;` 分开。单个 Volume 的输入格式如下：

`VOLUME = VOLUME_ID,BATCH_SNAPSHOT_VOLUME_TYPE,OBJ_ID,SNAPSHOT_NAME,SNAPSHOT_DESCRIPTION,SECONDARY_ID`

各参数说明如下：

| 参数 | 说明 | 示例 |
| --- | --- | --- |
| `VOLUME_ID` | 必选参数。输入 Volume ID。 | `9c2e2f88-99f7-4581-8eae-289924118962` |
| `BATCH_SNAPSHOT_VOLUME_TYPE` | 必选参数。输入 Volume 的类型。根据 Volume 的类型，可以为 `BATCH_SNAPSHOT_VOLUME`、`BATCH_SNAPSHOT_LUN`、`BATCH_SNAPSHOT_FILE` 和`BATCH_SNAPSHOT_NAMESPACE`。需要注意的是，所有字母均需大写输入。 | `BATCH_SNAPSHOT_VOLUME_LUN` |
| `OBJ_ID` | 必选参数。根据 Volume 类型，输入对应的 ID。对于 `BATCH_SNAPSHOT_VOLUME`，请留空；对于 `BATCH_SNAPSHOT_LUN`，请输入 LUN ID；`BATCH_SNAPSHOT_FILE`，请输入 Inode ID；对于 `BATCH_SNAPSHOT_NAMESPACE`，请输入 Namespace ID。 | `1` |
| `SNAPSHOT_NAME` | 可选参数。输入快照名称。 | `snapshot1` |
| `SNAPSHOT_DESCRIPTION` | 可选参数。输入快照描述。可留空。 | `snapshotdescription` |
| `SECONDARY_ID` | 可选参数。输入快照 Secondary ID。可留空。 | `99cf762a-0375-4327-927d-a17243374d25` |

**使用示例**

以对批量对 Volume ID 为 `911dcc87-b366-42ad-a093-500a9ce7e0de` 和 `cf4f60ff-1190-4497-b8d8-3d1967b860b7`的存储卷创建快照，示例如下：

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

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷快照 > 删除存储卷快照

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

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷快照 > 更新存储卷快照

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

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷快照 > 从存储卷快照回滚

# 从存储卷快照回滚

**操作方法**

在集群任一节点执行如下命令，从存储卷从快照回滚：

`zbs-meta snapshot rollback <pool_name> <volume_name> <snapshot_name>`

| 参数 | 说明 |
| --- | --- |
| `pool_name` | 数据存储名称。 |
| `volume_name` | 存储卷名称。 |
| `snapshot_name` | 快照名称。 |

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理存储卷快照 > 下沉指定 ID 的存储卷快照的性能层数据

# 下沉指定 ID 的存储卷快照的性能层数据

**操作方法**

在集群任一节点执行如下命令：

`zbs-meta volume sink_by_id <snapshot_id>`

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理一致性组

# 管理一致性组

## 查看所有一致性组

**操作方法**

在集群任一节点执行如下命令，查看当前存在的所有一致性组：

`zbs-meta consistency_group list`

**输出示例**

```
$zbs-meta consistency_group list
ID                                    Group Name    Description    Creation Time
------------------------------------  ------------  -------------  -----------------------------
256a3763-8641-4244-979d-dda565fbff11  test  test           2021-02-24 18:50:50.803339575
```

## 查看指定 ID 的一致性组

**操作方法**

在集群任一节点执行如下命令，查看指定 ID 的一致性组：

`zbs-meta consistency_group show <group_id>`

**输出示例**

```
zbs-meta consistency_group show 256a3763-8641-4244-979d-dda565fbff11
-------------  ------------------------------------
ID             256a3763-8641-4244-979d-dda565fbff11
Group Name     test
Description    test
Creation Time  2021-02-24 18:50:50.803339575
-------------  ------------------------------------
```

## 查看一致性组中的 Volume 成员

**操作方法**

在集群的任一节点执行如下命令，查看一致性组中的 Volume 成员：

`zbs-meta consistency_group list_volume <group_id>`

**输出示例**

```
zbs-meta consistency_group list_volume 256a3763-8641-4244-979d-dda565fbff11
Volume Id                             Pool Id                               Type
------------------------------------  ------------------------------------  ---------------
195025b3-6b31-4735-8d45-10c1b459d21b  6f2af6d8-faad-4a76-8f5e-a6ae3b2db7e8  CONSISTENCY_LUN
895ff6b3-6f48-4510-aac9-3fc65e4dcc15  6f2af6d8-faad-4a76-8f5e-a6ae3b2db7e8  CONSISTENCY_LUN
```

## 创建一致性组

**操作方法**

在集群任一节点执行如下命令，创建一致性组：

`zbs-meta consistency_group create <name> [--description] [--volumes]`

创建一致性组时可以通过 "--volumes" 指定组内的成员，格式如下:

```
 volumes = "VOLUME;VOLUME"

 VOLUME = POOL_ID , VOLUME_ID , CONSISTENCY_VOLUME_TYPE , ID

 CONSISTENCY_VOLUME_TYPE =   CONSISTENCY_VOLUME  |
                             CONSISTENCY_FILE    |
                             CONSISTENCY_LUN     |
                             CONSISTENCY_NAMESPACE
ID = EMPTY | INODE_ID | LUN_ID | NAMESPACE_ID
# 当 CONSISTENCY_VOLUME_TYPE 为 CONSISTENCY_VOLUME，ID 为空
```

**输出示例**

```
zbs-meta consistency_group create test --volumes "6f2af6d8-faad-4a76-8f5e-a6ae3b2db7e8,895ff6b3-6f48-4510-aac9-3fc65e4dcc15,CONSISTENCY_LUN,1;6f2af6d8-faad-4a76-8f5e-a6ae3b2db7e8,195025b3-6b31-4735-8d45-10c1b459d21b,CONSISTENCY_LUN,2" --description "test"
-------------  ------------------------------------
ID             256a3763-8641-4244-979d-dda565fbff11
Group Name     test
Description    test
Creation Time  2021-02-24 18:50:50.803339575
-------------  ------------------------------------
```

## 更新一致性组

**操作方法**

在集群任一节点执行如下命令，可以更新一致性组名称以及组内的 Volume 成员：

`zbs-meta consistency_group update <group_id> [--remove_volumes] [--add_volumes] [--new_description] [--remain_volume_snapshot]`

- `--new_description` 为可选参数, 用于更新一致性组描述信息。
- `--add_volumes` 为可选参数，将 volume 加入到一致性组。
- `--remove_volumes` 为可选参数，将 volume 从一致性组中移除。格式如下：

  ```
  volumes = "VOLUME;VOLUME"

  VOLUME = POOL_ID , VOLUME_ID , CONSISTENCY_VOLUME_TYPE , ID

  CONSISTENCY_VOLUME_TYPE =   CONSISTENCY_VOLUME  |
                              CONSISTENCY_FILE    |
                              CONSISTENCY_LUN     |
                              CONSISTENCY_NAMESPACE
  ID = EMPTY | INODE_ID | LUN_ID | NAMESPACE_ID
  # 当 CONSISTENCY_VOLUME_TYPE 为 CONSISTENCY_VOLUME, ID 为空
  ```
- `--remain_volume_snapshot` 默认值为 `false`，即当一致性组成员发生变更后，将自动删除之前创建的一致性快照组和快照成员；当改为 `true` 时，会删除快照组但将保留卷快照。

**输出示例**

```
zbs-meta consistency_group update  256a3763-8641-4244-979d-dda565fbff11 --remove_volumes "6f2af6d8-faad-4a76-8f5e-a6ae3b2db7e8,195025b3-6b31-4735-8d45-10c1b459d21b,CONSISTENCY_LUN"
-------------  ------------------------------------
ID             256a3763-8641-4244-979d-dda565fbff11
Group Name     test
Description    test
Creation Time  1970-01-01 08:00:00.0
-------------  ------------------------------------
```

## 删除一致性组

**操作方法**

在集群任一节点执行如下命令，删除指定 ID 的一致性组：

`zbs-meta consistency_group delete <group_id> [--remain_volume_snapshot]`

`--remain_volume_snapshot` 默认值为 `false`，即删除一致性组时不保留一致性快照组的卷快照。当改为 `true` 时，删除一致性组时将保留之前创建的卷快照。

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理一致性组快照组

# 管理一致性组快照组

## 查看快照组

**操作方法**

在集群任一节点执行如下命令，

- 查看一致性组中所有快照组：

  `zbs-meta consistency_group_snapshot list <group_id>`
- 查看指定 ID 的快照组：

  `zbs-meta consistency_group_snapshot show <group_snapshot_id>`

**输出示例**

```
zbs-meta consistency_group_snapshot list 256a3763-8641-4244-979d-dda565fbff11
Id                                    Group Id                              Name      Description    Creation Time
------------------------------------  ------------------------------------  --------  -------------  -----------------------------
01b47c5c-c2f4-4809-9ee4-b85944f32f14  256a3763-8641-4244-979d-dda565fbff11  snapshot                 2021-02-24 19:12:01.345927143
```

```
zbs-meta consistency_group_snapshot show 01b47c5c-c2f4-4809-9ee4-b85944f32f14
-------------  ------------------------------------
Id             01b47c5c-c2f4-4809-9ee4-b85944f32f14
Group Id       256a3763-8641-4244-979d-dda565fbff11
Name           snapshot
Description
Creation Time  2021-02-24 19:12:01.345927143
-------------  ------------------------------------
```

## 查看快照组成员

**操作方法**

在集群任一节点执行如下命令，查看快照组成员：

`zbs-meta consistency_group_snapshot list_snapshot <group_snapshot_id>`

**输出示例**

```
zbs-meta consistency_group_snapshot list_snapshot 01b47c5c-c2f4-4809-9ee4-b85944f32f14
Volume Id                             Snapshot Id                           Deleted
------------------------------------  ------------------------------------  ---------
195025b3-6b31-4735-8d45-10c1b459d21b  8146317d-c641-4d7f-9d80-aebe1758b382  None
895ff6b3-6f48-4510-aac9-3fc65e4dcc15  9d842925-f37d-472b-b511-778bc6f91aab  None
```

## 创建快照组

**操作方法**

在集群任一节点执行如下命令，创建快照：

`zbs-meta consistency_group_snapshot create <group_id> <name>`

**输出示例**

```
zbs-meta consistency_group_snapshot create  256a3763-8641-4244-979d-dda565fbff11  snapshot
-------------  ------------------------------------
Id             01b47c5c-c2f4-4809-9ee4-b85944f32f14
Group Id       256a3763-8641-4244-979d-dda565fbff11
Name           snapshot
Description
Creation Time  2021-02-24 19:12:01.345927143
-------------  ------------------------------------
```

## 更新快照组名称和描述

**操作方法**

在集群任一节点执行如下命令，更新快照组的名称和描述：

`zbs-meta consistency_group_snapshot update <group_snapshot_id> [--new_name] [--new_description]`

**输出示例**

```
zbs-meta consistency_group_snapshot update 01b47c5c-c2f4-4809-9ee4-b85944f32f14 --new_name "test" --new_description "test"
-------------  ------------------------------------
Id             01b47c5c-c2f4-4809-9ee4-b85944f32f14
Group Id       256a3763-8641-4244-979d-dda565fbff11
Name           test
Description    test
Creation Time  2021-02-24 19:12:01.345927143
-------------  ------------------------------------
```

## 使用快照组回滚一致性组

**操作方法**

在集群任一节点执行如下命令，使用快照组回滚一致性组：

`zbs-meta consistency_group_snapshot rollback <group_snapshot_id>`

**输出说明**

执行成功无输出。

## 删除快照组

**操作方法**

在集群任一节点执行如下命令，删除快照组：

`zbs-meta consistency_group_snapshot delete <group_snapshot_id> [--remain_volume_snapshot]`

`--remain_volume_snapshot` 为 `true` 时保留快照组的卷快照，默认为 `false`，即不保留快照组的卷快照。

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理数据块

# 管理数据块

数据块（extent）是 MetaCluster 管理的基本单元。⼀个存储卷被切分成多个固定⼤⼩的数据块存储在 ChunkServer 中。数据的恢复、迁移、写时复制（CopyOnWrite - COW）等，都以数据块为单位进⾏。技术人员可以通过 lextent 和 pextent 对集群的数据块进行查看和调试。其中 lextent 为逻辑数据块，pextent 为实际落盘的物理数据块，下文如无特别说明，“物理数据块”均简称为“数据块”。

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
| `Pool Name` | 数据块所属数据存储。 |
| `Volume ID` | 数据块所属存储卷的 ID。 |
| `Volume Name` | 数据块所属存储卷的名称。 |
| `Volume Is Snapshot` | 存储卷是否有快照。 |
| `Volume Snapshot Pool ID` | 数据块所属数据存储的 ID。 |
| `Snapshot Name` | 数据块所属存储卷的快照名称。 |

### 查看集群中数据块

**操作方法**

在集群任一节点执行如下命令，查看集群中指定范围的数据块：

`zbs-meta pextent list [start_id] [end_id] [--show_non_exist] [--show_cap_only] [--show_perf_only]`

| 参数 | 说明 |
| --- | --- |
| `start_id` | 开始查找的 pextent ID。 |
| `end_id` | 结束查找的 pextent ID。 |
| `--show_non_exist` | 展示还未被分配过的 pextent ID。 |
| `--show_cap_only` | 仅展示位于容量层的 pextent ID。 |
| `--show_perf_only` | 仅展示位于性能层的 pextent ID。 |

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
| `Temporary Replica` | 对于副本模式的 pextent，在有副本异常时，将会创建出对应的临时副本。 |
| `Is Garbage` | 是否需要回收。 |
| `Origin PExtent` | 创建快照时，origin pextent 会指向源 pextent。 |
| `Origin Epoch` | 源 pextent 的 `Epoch`。 |
| `Expected Replica num` | 预期副本数量。 |
| `Epoch` | 版本号。 |
| `Prefer Local` | 该 pextent 默认保存的 chunk ID。 |
| `Allocated Space` | 已分配物理空间。 |
| `Resiliency Type` | 冗余策略类型。 |
| `PExtent Type` | 是 Capacity PExtent 还是 Performance PExtent。 |
| `EC Param` | EC 冗余策略下对应的 EC 策略属性。 |
| `Is Sinkable` | 是否可以下沉。 |

### 查看某个数据块的详细信息

**操作方法**

在集群任一节点执行如下命令，查看某个数据块的详细信息：

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
| `Temporary Replica` | 对于副本模式的 pextent，在有副本异常时，将会创建出对应的临时副本。 |
| `Is Garbage` | 是否需要回收。 |
| `Origin PExtent` | 创建快照时，origin pextent 会指向源 pextent。 |
| `Origin Epoch` | 源 pextent 的 `Epoch`。 |
| `Expected Replica num` | 预期副本数量。 |
| `Epoch` | 版本号。 |
| `Prefer Local` | 该 pextent 默认保存的 chunk ID。 |
| `Allocated Space` | 已分配物理空间。 |
| `Resiliency Type` | 冗余策略类型。 |
| `PExtent Type` | 是 Capacity PExtent 还是 Performance PExtent。 |
| `EC Param` | EC 冗余策略下对应的 EC 策略属性。 |
| `Is Sinkable` | 是否可以下沉。 |

### 查看数据块所属存储卷

**操作方法**

在集群任一节点执行如下命令，查看数据块所属的存储卷：

`zbs-meta pextent getref <pextent_id> [--show_lextent_only]`

| 参数 | 说明 |
| --- | --- |
| `--show_lextent_only` | 仅查看所属 lextent 的详细信息，默认为 False |

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
| `Temporary Replica` | 对于副本模式的 pextent，在有副本异常时，将会创建出对应的临时副本。 |
| `Is Garbage` | 是否需要回收。 |
| `Origin PExtent` | 创建快照时，origin pextent 会指向源 pextent。 |
| `Origin Epoch` | 源 pextent 的 `Epoch`。 |
| `Expected Replica num` | 预期副本数量。 |
| `Epoch` | 版本号。 |
| `Prefer Local` | 该 pextent 默认保存的 chunk ID。 |
| `Allocated Space` | 已分配物理空间。 |
| `Resiliency Type` | 冗余策略类型。 |
| `PExtent Type` | 是 Capacity PExtent 还是 Performance PExtent。 |
| `EC Param` | EC 冗余策略下对应的 EC 策略属性。 |
| `Is Sinkable` | 是否可以下沉。 |

### 查看数据块关联的虚拟机

**操作方法**

在任意节点执行如下命令，查看与某个 pextent 关联的虚拟机

`zbs-tool elf get_vm_by_pid <pid>`

| 参数 | 说明 |
| --- | --- |
| `pid` | PExtent ID。 |

**输出示例**

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
| `Temporary Replica` | 对于副本模式的 pextent，在有副本异常时，将会创建出对应的临时副本。 |
| `Ever Exist` | PExtent 是否曾经被分配过(精简置备的数据块只有发生读写后才会真实存在)。 |
| `Affected ZBS Volumes` | PExtent 影响的虚拟卷的 ID， 可显示多个。 |
| `Affected ZBS NFS Files` | PExtent 影响的虚拟卷对应的 NFS 文件名。仅在使用 NFS 接入协议的显示值，否则为空值。 |

## 查找处于某个状态的数据块

**操作方法**

在集群任一节点执行如下命令，查找处于某个状态的数据块：

`zbs-meta pextent find <pextent_status> [--start START] [--length Length]`

| 参数 | 说明 |
| --- | --- |
| `pextent_status` | 查找指定状态的数据块：  - `dead`：所有副本都不可访问的 pextent。 - `need_recover`：需要进行数据恢复的 pextent，当前正在恢复。 - `may_recover`：可能进行数据恢复的 pextent，当前没有恢复，但即将进行恢复。 - `garbage`：标记为回收的 pextent。 - `need_drain`: 需要进行数据下沉的 pextent。 |
| `--start START` | 指定开始查找的 pextent ID，默认为 1。 |
| `--length LENGTH` | 设置返回的 pextent 的数量。默认值以及最大值均为 1024。 |

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

## 查找 dead 块和影响范围

当物理盘损坏或者节点下线时，部分数据块可能会丢失所有活跃的副本，此类数据块将被标记为 dead extent，且无法被访问。用户可以通过命令检测出 dead extent 及其影响的虚拟卷、虚拟机等。

**操作方法**

在集群任一节点执行如下命令：

`zbs-tool abnormal_detect find_dead_extent [--start START] [--length Length]`

| 参数 | 说明 |
| --- | --- |
| `--start START` | 指定开始查找的 pextent ID，默认为 1。 |
| `--length LENGTH` | 设置返回的 pextent 的数量。默认值以及最大值均为 1024。 |

**输出示例**

```
 ID  Replica    Alive Replica    Temporary Replica    Ever Exist    Is Garbage      Origin PExtent    Origin Epoch    Expected Replica num    Epoch    Prefer Local  Allocated Space    Resiliency Type    PExtent Type    EC Param    Is Sinkable    Affected ZBS Volumes                      Affected ZBS NFS Files
-----  ---------  ---------------  -------------------  ------------  ------------  ----------------  --------------  ----------------------  -------  --------------  -----------------  -----------------  --------------  ----------  -------------  ----------------------------------------  ------------------------
    5  [3]        []               []                   True          False                        0               0                       3        5               3  768.00 KiB         RT_REPLICA         PT_PERF                     True           ['c734d7cf-d31d-4782-b6c3-f8acaeb7db1c']  []
```

以该输出结果为例，可得知以下主要信息：

- dead extent 的 PID 为 `5`。
- 受 dead extent 影响的虚拟卷 ID 为 `c734d7cf-d31d-4782-b6c3-f8acaeb7db1c`。

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `ID` | dead extent 的 PID。 |
| `Replica` | dead extent 应有的副本。 |
| `Alive Replica` | dead extent 实际存活的副本。 |
| `Temporary Replica` | 对于副本模式的 pextent，在有副本异常时，将会创建出对应的临时副本。 |
| `Ever Exist` | dead extent 是否曾经被分配过(精简置备的数据块只有发生读写后才会真实存在)。 |
| `Is Garbage` | dead extent 是否被标记为 Garbage，Garbage 意味着其所属的虚拟卷和快照等完全被删除，此数据块已经无用。 |
| `Origin PExtent` | 展示 dead extent 是否从其他数据块复制。若复制自其他数据块，显示其来源数据块的 pid，否则显示为 `0`。 |
| `Origin Epoch` | 源 pextent 的 `Epoch`。 |
| `Expected Replica num` | dead extent 预期的副本数，取决于其所属的上级对象(虚拟卷/快照)的配置。 |
| `Epoch` | 与 PID 组合用于唯一标识一个 extent 的属性值。 |
| `Prefer Local` | dead extent 副本预期被分配到的节点 ID， 由副本分配策略决定。 |
| `Allocated Space` | 已分配物理空间。 |
| `Resiliency Type` | 冗余策略类型。 |
| `PExtent Type` | 是 Capacity PExtent 还是 Performance PExtent。 |
| `EC Param` | EC 冗余策略下对应的 EC 策略属性。 |
| `Is Sinkable` | 是否可以下沉。 |
| `Affected ZBS Volumes` | dead extent 影响的虚拟卷的 ID， 可显示多个。 |
| `Affected ZBS NFS Files` | dead extent 影响的虚拟卷对应的 NFS 文件名。仅在使用 NFS 接入协议的显示值，否则为空值。 |

## 写入从数据块中读取到的数据

**操作方法**

在集群任一节点指定如下命令，将指定 `pextent_id` 对应的 pextent 中从 `offset` 开始，长度为 `length` 的数据写入到 `output_file` 中：

`zbs-meta pextent read -o <output_file> <pextent_id> <offset> <length>`

| 参数 | 说明 |
| --- | --- |
| `output_file` | 用于存储读取到的数据的文件。 |
| `offset` | 读取数据的起始偏移量(相对于虚拟卷)，需要能被 512 整除。 |
| `length` | 读取数据的长度，需要能被 512 整除。 |

## 查看 chunk 上的数据块的属性

**操作方法**

在当前节点执行如下命令，查看处于该 chunk 上的某个 pextent 的属性。

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

## 块存储集群 CLI 命令 > 管理块存储服务 > 触发垃圾回收

# 触发垃圾回收

**注意事项**

集群中的垃圾回收是周期性进行的，正常场景下不需要手动触发。该命令用于主动触发垃圾回收。

**操作方法**

在集群任一节点执行如下命令，触发垃圾回收：

`zbs-meta gc scan_immediate`

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理业务主机组

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

  - 关联 iSCSI Target 信息

    | 参数 | 说明 |
    | --- | --- |
    | `Target ID` | Target ID。 |
  - 关联 iSCSI LUN 信息

    | 参数 | 说明 |
    | --- | --- |
    | `Parent Target ID` | LUN 所属 Target 的 ID。 |
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

## 块存储集群 CLI 命令 > 管理块存储服务 > 管理业务主机

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
  | `Enable Chap` | 是否使能 Chap。 |
  | `Chap Name` | Chap 名称。 |
  | `Chap Secret` | Chap 密码。 |
- **关联存储资源信息**

  - 关联 iSCSI Target 信息

    | 参数 | 说明 |
    | --- | --- |
    | `Target ID` | Target ID。 |
  - 关联 iSCSI LUN 信息

    | 参数 | 说明 |
    | --- | --- |
    | `Parent Target ID` | LUN 所属 Target 的 ID。 |
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

## 块存储集群 CLI 命令 > 管理回收站 > 配置回收站

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

## 块存储集群 CLI 命令 > 管理回收站 > 查看回收站相关信息

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
| `--show_detail` | 可选参数，是否显示原始的协议对象字段，用于查询删除前协议对象的信息，默认不显示。 |

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
| `Second Id` | 卷的 Secondary ID。 |
| `Origin Pool Id` | 卷所在原始存储池的 ID。 |
| `Deleted Time` | 卷被删除进入回收站的时间。 |
| `Expired Time` | 卷的过期清理时间。 |
| `Protocol Type` | 卷原始类型，如 ISCSI\_Lun、NVMF\_Namespace、ZBS\_Volume。 |
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
| `--last_key` | 上一页返回的最后一个 volume\_id，用于游标翻页（与 page\_pos 二选一）。 |
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
| `Second Id` | 卷的 Secondary ID。 |
| `Origin Pool Id` | 卷所在原始存储池的 ID。 |
| `Deleted Time` | 卷被删除进入回收站的时间。 |
| `Expired Time` | 卷的过期清理时间。 |
| `Protocol Type` | 卷原始类型，如 ISCSI\_Lun、NVMF\_Namespace、ZBS\_Volume。 |
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
| `--last_key` | 上一页返回的最后一个 snapshot\_id，用于游标翻页（与 page\_pos 二选一）。 |
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
| Second Id | 快照的 Secondary ID。 |
| Origin Pool Id | 快照所属卷原始的存储池 ID。 |
| Origin Volume Id | 创建该快照时所属的卷 ID。 |
| Deleted Time | 被删除进入回收站的时间。 |
| Expired Time | 回收站中快照的过期时间。 |

---

## 块存储集群 CLI 命令 > 管理回收站 > 从回收站中恢复暂存卷

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
| --dst\_target\_id | 目标 iSCSI Target 的唯一标识符，不指定时，默认恢复至原始 Target 。 |
| --new\_lun\_name | 指定新还原出的 LUN 名称，不指定时，默认恢复至原始 Lun Name。 |
| --new\_lun\_id | 指定的还原后 LUN 的 ID（可选），默认恢复至原始 Lun Id。 |

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

参考[查看 iSCSI LUN 信息](/smtxzbs/5.7.0/zbs_cli_guide/zbs_cli_guide_70)的输出说明。

## 将指定的暂存卷恢复为 Namespace

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
| --dst\_subsystem\_id | 目标 subsystem ID，暂存卷将被还原至该 subsystem。 |
| --new\_ns\_name | 新 namespace 的名称。 |
| --new\_ns\_id | 新 namespace 的 ID。 |
| --new\_ns\_group\_id | 所属 namespace 组的 ID，当目的 subsystem 为均衡模式时需要设置。 |
| --new\_ns\_is\_shared | 是否为共享 namespace ，取值为 true 或 false ，当目的 subsystem 为继承模式时需要设置。 |

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

**输出说明**

参考[查看指定的 NVMe Namespace](/smtxzbs/5.7.0/zbs_cli_guide/zbs_cli_guide_88)的输出说明。

## 将指定的暂存快照恢复到存储池

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin restore_snapshot <trash_snapshot_id> <--dst_pool_id> <--new_snapshot_name>
```

| 参数 | 说明 |
| --- | --- |
| trash\_snapshot\_id | 被恢复的暂存快照的唯一标识符。 |
| --dst\_pool\_id | 目标存储池的唯一标识符。 |
| --new\_snapshot\_name | 新快照的名称。 |

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

参考[查看指定存储卷快照的详细信息](/smtxzbs/5.7.0/zbs_cli_guide/zbs_cli_guide_50)的输出说明。

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
| --dst\_pool\_id | 目标存储池的唯一标识符。 |
| --new\_volume\_name | 新卷的名称。 |

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

参考[查看存储卷上的数据块信息](/smtxzbs/5.7.0/zbs_cli_guide/zbs_cli_guide_38)的输出说明。

---

## 块存储集群 CLI 命令 > 管理回收站 > 清理回收站中的暂存卷

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
---------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Cleaner Running` | 任务是否在运行。 |
| `Task UUID` | 最新任务的 UUID， 如果任务未在运行，指代上次任务的 UUID，如果任务正在运行，指代当前任务的 UUID。 |
| `Volume Count` | 任务包含的卷数量。 |

## 批量清理尚未过期的暂存卷

**操作方法**

在集群任一节点执行如下命令：

```
zbs-meta recycle_bin batch_sweep_volumes <volume_ids>
```

| 参数 | 说明 |
| --- | --- |
| <volume\_ids> | 待清理的 volume-id 集合，用 ‘,’ 间隔 |

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
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Cleaner Running` | 任务是否在运行。 |
| `Task UUID` | 最新任务的 UUID， 如果任务未在运行，指代上次任务的 UUID，如果任务正在运行，指代当前任务的 UUID。 |
| `Volume Count` | 任务包含的卷数量。 |

---

## 块存储集群 CLI 命令 > 管理集群内部 I/O > 管理数据迁移和恢复 > 管理数据恢复

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

请参考[设置内部 I/O 的模式和优先级](/smtxzbs/5.7.0/zbs_cli_guide/zbs_cli_guide_63)。

---

## 块存储集群 CLI 命令 > 管理集群内部 I/O > 管理数据迁移和恢复 > 管理数据迁移

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
| `--ignore_topo_safety` | 本次迁移是否忽略拓扑安全，默认为 False。 |

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
| `Report enable` | 集群中的 chunk 是否上报让 Meta 辅助迁移的待卸载数据块。 |
| `Include cache` | 集群中的 chunk 是否上报在性能层的待卸载数据块，默认为 False。 |
| `Include partition` | 集群中的 chunk 是否上报在容量层的待卸载数据块，默认为 True。 |
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
| `--length` | 设置返回的 pextents 的数量。默认值以及最大值均为 1024。 |
| `--ignore_ec` | 是否忽略冗余类型为 EC 的数据块，默认为 False。 |
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

请参考[设置内部 I/O 的模式和优先级](/smtxzbs/5.7.0/zbs_cli_guide/zbs_cli_guide_63)。

---

## 块存储集群 CLI 命令 > 管理集群内部 I/O > 管理数据迁移和恢复 > 管理任务

# 管理任务

## 查看集群中恢复和迁移任务的概况

**操作方法**

在集群任一节点执行如下命令，输出恢复和迁移任务的概况：

`zbs-meta reposition summary [--chunk_id <CHUNK_ID>]`

参数定义如下：

| 参数 | 说明 |
| --- | --- |
| `--chunk_id <CHUNK_ID>` | 可选参数，选择是否查看指定节点的信息。 |

**输出示例**

```
Chunk ID    Cap Src    Cap Replace    Cap Dst    Perf Src    Perf Replace    Perf Thin Dst    Perf Thick Dst
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
| `Perf Thin Dst` | 性能层将该节点作为目的端的非 Pin 恢复和迁移任务的数量。 |
| `Perf Thick Dst` | 性能层将该节点作为目的端的 Pin in Perf 恢复和迁移任务的数量。 |

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
| `Perf thick load` | 性能层 Pin in Perf 负载水位。 |
| `Perf thin load` | 性能层非 Pin 负载水位。 |
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

参数定义如下：

| 参数 | 说明 |
| --- | --- |
| `--mode <MODE>` | 可选参数，更改并发度限制的模式：0（动态），1（静态）。 |
| `--static_cap_reposition_concurrency_limit <STATIC_CAP_REPOSITION_CONCURRENCY_LIMIT>` | 可选参数，更改容量层并发度限制静态模式下的并发度上限。 |
| `--static_perf_reposition_concurrency_limit <STATIC_PERF_REPOSITION_CONCURRENCY_LIMIT>` | 可选参数，更改性能层并发度限制静态模式下的并发度上限。 |
| `--static_generate_cmds_per_round_limit <STATIC_GENERATE_CMDS_PER_ROUND_LIMIT>` | 可选参数，设置每一轮生成恢复和迁移命令的数量的上限。 |
| `--static_cap_distribute_cmds_per_chunk_limit <STATIC_CAP_DISTRIBUTE_CMDS_PER_CHUNK_LIMIT>` | 可选参数，设置对每一个 chunk 生成容量层恢复和迁移命令的数量的上限。 |
| `--static_perf_distribute_cmds_per_chunk_limit <STATIC_PERF_DISTRIBUTE_CMDS_PER_CHUNK_LIMIT>` | 可选参数，设置对每一个 chunk 生成性能层恢复和迁移命令的数量的上限。 |

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理集群内部 I/O > 管理数据下沉和下沉策略 > 管理数据下沉

# 管理数据下沉

分层部署的块存储集群默认按照数据的冷热程度自动分层，访问频率较高的数据将停留在速度更快的性能层，访问频率较低的数据将下沉至速度相对较慢的容量层。本节介绍的命令用于管理集群的数据下沉。

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
| `--cmd_timeout_ms <CMD_TIMEOUT_MS>` | 可选参数，指定下沉命令的超时时间（毫秒），默认值为 600000，取值范围为 60000 ～ 720000。 |
| `--generate_cmds_per_round_limit <GENERATE_CMDS_PER_ROUND_LIMIT>` | 可选参数，指定集群每次下发的下沉命令的最大数量，默认值为 1024，取值范围为 2 ～ 4096。 |
| `--distribute_cmds_per_chunk_limit <DISTRIBUTE_CMDS_PER_CHUNK_LIMIT>]` | 可选参数，指定集群为每个 chunk 生成的下沉命令的最大数量，默认值为 128，取值范围为 2 ～ 4096。 |

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
| `Cluster enable drain` | 集群是否开启数据下沉功能，1 代表已开启，0 代表未开启。 |
| `Allow drain` | 数据下沉是否已被下沉策略开启，1 代表已开启，0 代表未开启。 |
| `Scan interval` | 集群扫描间隔时间。 |
| `Generate cmds interval` | 生成下沉命令的间隔时间。 |
| `Drain no lease timeout` | 数据块维持无 Lease 状态的时间超过该值时，下发下沉命令。 |
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

## 块存储集群 CLI 命令 > 管理集群内部 I/O > 管理数据下沉和下沉策略 > 管理下沉策略

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
- CAP\_DIO\_ALL\_THROTTLED: 对被性能层限流的 I/O 进行容量层直写，SMTX OS 6.1.0 中实现与 CAP\_DIO\_BLOCK\_ALIGNED\_ONLY 相同
- CAP\_DIO\_ALL: 仅对 8 KiB 对齐的 I/O 进行容量层直写

**操作方法**

在集群任一节点执行如下命令，设置下沉策略的相关参数：

`zbs-meta sink update [--inactive_lease_interval_map <INACTIVE_LEASE_INTERVAL_MAP>] [--no_lease_timeout_map <NO_LEASE_TIMEOUT_MAP>] [--cap_direct_write_policy_map <CAP_DIRECT_WRITE_POLICY_MAP>] [--prefer_cap_passthru <PREFER_CAP_PASSTHRU>]`

| 参数 | 说明 |
| --- | --- |
| `--inactive_lease_interval_map <INACTIVE_LEASE_INTERVAL_MAP>` | 可选参数，指定不同下沉档位对应的判定 Lease 是否活跃的时间阈值。 |
| `--no_lease_timeout_map <NO_LEASE_TIMEOUT_MAP>` | 可选参数，指定不同下沉档位对应的判定是否对无 Lease Extent 下发下沉命令的时间阈值。 |
| `--cap_direct_write_policy_map <CAP_DIRECT_WRITE_POLICY_MAP>` | 可选参数，指定不同下沉档位对应的容量层直写策略。 |
| `--prefer_cap_passthru <PREFER_CAP_PASSTHRU>` | 可选参数，指定携带 PREFER\_CAP IO Flag 的写 IO 是否应在满足条件时直写容量层。 |

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
| `Drain parent start mode` | 开始对 Parent Extent 下发下沉命令的下沉档位。 |
| `Drain idle start mode` | 开始对无 Lease Extent 下发下沉命令的下沉档位。 |
| `Cap direct write policy` | 当前的容量层直写策略。 |
| `Start cap direct write in SINK_LOW ratio` | 在当前下沉档位为低档位且 Sink load 高于该值时，开启容量层直写。 |
| `Prefer cap passthru` | 携带 PREFER\_CAP IO Flag 的写 IO 是否应在满足条件时直写容量层。 |
| `Access reserve block num` | Access 当前可保留的数据块数量。 |
| `Inactive lease interval (sec) map` | 不同下沉档位对应的判定 Lease 是否活跃的时间阈值。 |
| `No lease timeout (ms) map` | 不同下沉档位对应的判定是否对无 Lease Extent 下发下沉命令的时间阈值。 |
| `Cap direct write policy map` | 不同下沉档位对应的容量层直写策略。 |

---

## 块存储集群 CLI 命令 > 管理集群内部 I/O > 管理 I/O 模式和优先级

# 管理 I/O 模式和优先级

您可以通过命令管理集群内部 I/O 的模式和优先级。

内部 I/O 包含两种模式：

- AUTO：智能调节模式，根据当前系统负载自动调节内部 I/O 的速度。
- STATIC：静态调节模式，可指定内部 I/O 的最大速率。SMTX ZBS 5.6.x 集群的空间分为性能层（perf） 和 容量层（cap），性能层和容量层的限速不同，可分别设置。

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
| `--mode <MODE>` | 指定内部 I/O 的模式：  - `AUTO`：智能调节模式。此模式是默认模式。 - `STATIC`：静态调节模式。只允许对 Meta 下的所有 chunk 设置同一限额，不能够对每个 chunk 单独设置。 |
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
| `Recover I/O Priority` | recover I/O 优先级。 |
| `Sink I/O Priority` | sink I/O 优先级。 |
| `Migrate I/O Priority` | migrate I/O 优先级。 |
| `Current Cap Speed limit` | 当前容量层内部 I/O 限速。 |
| `Cap HW Speed limit` | 当前容量层内部 I/O 硬件决定的限速的最大值。 |
| `Currnet Perf Speed limit` | 当前性能层内部 I/O 限速。 |
| `Perf HW Speed limit` | 当前性能层内部 I/O 硬件决定的限速的最大值。 |

---

## 块存储集群 CLI 命令 > 管理 iSCSI 存储服务

# 管理 iSCSI 存储服务

SMTX ZBS 块存储集群支持外部客户端通过 iSCSI 协议使用块存储服务。用户可以使用命令行管理集群的 iSCSI Target 和 LUN。

---

## 块存储集群 CLI 命令 > 管理 iSCSI 存储服务 > 管理 iSCSI Target

# 管理 iSCSI Target

iSCSI Target 是 iSCSI Initiator 访问的存储设备，用于响应 Initiator 的存储访问请求。iSCSI Target 可以提供一个或多个 LUN 供客户端使用。

## 查看所有的 iSCSI Target

**操作方法**

在集群任一节点执行如下命令，查看集群的所有 iSCSI Target。

`zbs-iscsi target list`

**输出示例**

```
ID                                    Name                                  IQN Name                                                            Creation Time                  Encrypt Method      Resiliency Type      Replica#  EC Param    Thin    Description    Storage Pool    Whitelist    IQN Whitelist                                                                                                                          External Use      Stripe Num    Stripe Size  Adaptive IQN Whitelist    Labels            Is Prioritized    Use Host    Allowed Host Ids                      Allowed Host Group Ids
------------------------------------  ------------------------------------  ------------------------------------------------------------------  -----------------------------  ------------------  -----------------  ----------  ----------  ------  -------------  --------------  -----------  -------------------------------------------------------------------------------------------------------------------------------------  --------------  ------------  -------------  ------------------------  ----------------  ----------------  ----------  ------------------------------------  ------------------------------------
114b6749-d902-43bc-8280-e3ad8b8f2451  test-not-select-host-and-group        iqn.2016-02.com.smartx:system:test-not-select-host-and-group        2025-07-02 11:47:23.323384547  ENCRYPT_PLAIN_TEXT  RT_REPLICA                  3              True                   system                                                                                                                                                              True                       8         262144  False                     []                False             True
17d46e36-bee2-45ab-8f20-a1611eb55353  test-by-manual-and-iqn-allban         iqn.2016-02.com.smartx:system:test-by-manual-and-iqn-allban         2025-07-02 11:49:36.805802270  ENCRYPT_PLAIN_TEXT  RT_REPLICA                  3              True                   system          */*                                                                                                                                                 True                       8         262144  False                     []                False             False
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `IQN Name` | Target 的 IQN 名称。 |
| `Encrypt Method` | 存储卷的数据加密算法。 |
| `Resiliency Type` | 冗余模式。 |
| `EC Param` | EC 冗余模式下对应的 EC 参数。 |
| `IQN Whitelist` | IQN 白名单。 |
| `Stripe Num` | 条带数。 |
| `Stripe Size` | 条带大小。 |
| `Adaptive IQN Whitelist` | 是否采用自适应 IQN 白名单。 |
| `Labels` | 标签，用于在不指定 Target 创建 LUN 时提供标签匹配功能。 |
| `Is Prioritized` | 是否要将数据都维持在性能层中。 |
| `Use Host` | 是否使用业务主机指定白名单。 |
| `Allowed Host Ids` | 关联的业务主机的 ID。 |
| `Allowed Host Group Ids` | 关联的业务主机组的 ID。 |

## 查看指定 iSCSI Target 的基本信息和 CHAP 认证信息

**操作方法**

在集群任一节点执行如下命令，查看指定名称的 iSCSI Target 的基本信息和 CHAP 认证信息：

`zbs-iscsi target show [--show_chap] <name>`

| 参数 | 说明 |
| --- | --- |
| `--show_chap` | 可选参数，显示该 iSCSI Target 的 CHAP 认证信息。 |
| `name` | iSCSI Target 名称。 |

**输出示例**

```
----------------------  -----------------------------------------
ID                      745c5404-2a5a-4c20-97d0-0a56fbeafdb6
Name                    target-chap
IQN Name                iqn.2016-02.com.smartx:system:target-chap
Creation Time           2025-07-04 18:17:24.24872660
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Replica#                3
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

- **iSCSI Target 基本信息**

  | 参数 | 说明 |
  | --- | --- |
  | `ID` | Target ID |
  | `Name` | Target 名称。 |
  | `IQN Name` | IQN 名称。 |
  | `Resiliency Type` | 冗余模式。 |
  | `Encrypt Method` | 存储卷的数据加密算法。 |
  | `Replica#` | Target 内新建 LUN 的副本数。 |
  | `EC Param` | EC 冗余模式下对应的 EC 参数。 |
  | `Thin` | Target 内新建 LUN 是否采用精简置备。 |
  | `Description` | Target 描述。 |
  | `Storage Pool` | Target 所属存储池。 |
  | `Whitelist` | 可访问该 Target 的 IP 白名单。 |
  | `IQN Whitelist` | 可访问该 Target 的 IQN 白名单。 |
  | `External Use` | `True` 或 `False`，表示 iSCSI Target 是否用作外部接入。 |
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
    | `Enable` | `True` 或 `False`，表示是否启用了 Target CHAP 认证。 |
  - Initiator CHAP 认证信息

    | 参数 | 说明 |
    | --- | --- |
    | `IQN` | Initiator 的 IQN 名称。 |
    | `Chap Name` | Initiator CHAP 认证名称。 |
    | `Secret` | Initiator CHAP 认证密码。 |
    | `Enable` | `True` 或 `False`，表示是否启用了 Initiator CHAP 认证。 |

## 创建 iSCSI Target

**操作方法**

在集群任一节点执行如下命令，创建 iSCSI Target，并设置 Target 的名称、IQN、存储策略、CHAP 认证信息、IO 限速等：

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
| `--replica_num <REPLICA_NUM>` | 设置 Target 内新建 LUN 的默认副本数，可设置为 2 副本或 3 副本，默认为 2 副本。 |
| `--thin_provision <THIN_PROVISION>` | 设置 Target 新建 LUN 的置备方式是否为精简置备，可设置为`True` 或 `False`。 |
| `--storage_pool_id <STORAGE_POOL_ID>` | 选择 Target 所属的存储池。 |
| `--whitelist <WHITELIST>` | 设置 iSCSI Target 的 IP 白名单，可输入 IP 地址或 CIDR 块。`*/*` 表示任何 IP 都可以访问此 Target。 |
| `--iqn_whitelist <IQN_WHITELIST>` | 设置 iSCSI Target 的 IQN 白名单，多个 IQN 之间以英文逗号 `,` 分隔。 |
| `--adaptive_iqn_whitelist <ADAPTIVE_IQN_WHITELIST>` | 设置是否启用 IQN 白名单自适应功能，可设置为 `True` 或 `False`。开启后，IQN 白名单会自动保持为所包含 LUN 的 IQN 白名单的并集。开启自适应功能时，不应同时设置 `--iqn_whitelist`、`allowed_host_ids` 和 `allowed_host_group_ids` 参数。 |
| `--chap_name <CHAP_NAME>` | 创建 Target CHAP 认证名称。允许输入长度为 1 ~ 223 的字母、数字，以及特殊符号 `.`、`-`、`:`。 |
| `--secret <SECRET>` | 指定 Target CHAP 认证密码。允许输入长度 12 ~ 16 的字母和数字。 |
| `--external_use <EXTERNAL_USE>` | `true` 或 `false`，表示 Target 是否用作外部接入。 |
| `--stripe_num <STRIPE_NUM>` | Target 新建 LUN 的条带数。 |
| `--stripe_size <STRIPE_SIZE>` | Target 新建 LUN 的条带大小。 |
| `--iops <IOPS>` | 设置 Target 内新建 LUN 的读写总 IOPS 上限值。 |
| `--iops_rd <IOPS_RD>` | 设置读 IOPS 的上限值。 |
| `--iops_wr <IOPS_WR>` | 设置写 IOPS 的上限值。 |
| `--iops_max <IOPS_MAX>` | 设置读写总 IOPS 突发的上限值。 |
| `--iops_rd_max <IOPS_RD_MAX>` | 设置读 IOPS 突发的上限值。 |
| `--iops_wr_max <IOPS_WR_MAX>` | 设置写 IOPS 突发的上限值。 |
| `--iops_max_length <IOPS_MAX_LENGTH>` | 设置读写总 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_rd_max_length <IOPS_RD_MAX_LENGTH>` | 设置读 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_wr_max_length <IOPS_WR_MAX_LENGTH>` | 设置写 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_io_size <IOPS_IO_SIZE>` | 使用 IOPS 限速时，假定的平均 I/O 数据量大小。 |
| `--bps <BPS>` | 设置 Target 内新建 LUN 的读写总带宽限制，单位为 Bps。 |
| `--bps_rd <BPS_RD>` | 设置读带宽的上限值。 |
| `--bps_wr <BPS_WR>` | 设置写带宽的上限值。 |
| `--bps_max <BPS_MAX>` | 设置读写总带宽在发生 I/O 突发时的上限值。 |
| `--bps_rd_max <BPS_RD_MAX>` | 设置读带宽在发生 I/O 突发时的上限值。 |
| `--bps_wr_max <BPS_WR_MAX>` | 设置写带宽在发生 I/O 突发时的上限值。 |
| `--bps_max_length <BPS_MAX_LENGTH>` | 设置在发生 I/O 突发时，以读写总带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_rd_max_length <BPS_RD_MAX_LENGTH>` | 设置在发生 I/O 突发时，以读带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_wr_max_length <BPS_WR_MAX_LENGTH>` | 设置在发生 I/O 突发时，以写带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--resiliency_type <RESILIENCY_TYPE>` | 设置冗余模式，副本或 EC，默认为 `None`。 |
| `--ec_algo <EC_ALGO>` | 设置 EC 算法，当冗余模式为 EC 时必须设置，默认为 `RS`。 |
| `--ec_k <EC_K>` | 设置 EC 算法参数 K，参数范围为 [2，23]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--ec_m <EC_M>` | 设置 EC 算法参数 M，参数范围为 [1，4]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--encrypt_method <ENCRYPT_METHOD>` | 设置数据加密方法，默认为不加密 。 |
| `--driver_name <DRIVER_NAME>` | 设置驱动名称，`iscsi` 或 `iser`，默认为 `None`。 |
| `--prioritized <PRIORITIZED>` | 设置在 Target 内创建 LUN 时是否默认开启常驻缓存，可设置为 `True` 或 `False`。 |
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

## 更新 iSCSI Target

**操作方法**

在集群任一节点执行如下命令，更新 iSCSI Target：

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
| `name` | 待更新 Target 的名称。 |
| `--new_name <NEW_NAME>` | 重新命名 Target，允许输入字母、数字以及特殊符号 `-`、`.`。iSCSI Target 的名称不区分大小写，不论以大写还是小写输入，都将统一转换为小写格式。 |
| `--desc <DESC>` | 更新 Target 描述。 |
| `--iqn_date <IQN_DATE>` | 更新用于生成 Target 的 IQN，必须为 `yyyy-mm` 格式。默认为 `2016-02`。 |
| `--iqn_naming_auth <IQN_NAMING_AUTH>` | 更新 Naming Auth，用于生成 Target IQN。格式为 `com.公司名`，默认为 `com.smartx`。允许输入字母、数字以及特殊符号 `-`、`.`，但不允许以 `-` 开头或结尾。 |
| `--replica_num <REPLICA_NUM>` | 更新 Target 内新建 LUN 的默认副本数，副本数只支持由 2 副本提升至 3 副本。 |
| `--thin_provision <THIN_PROVISION>` | `True` 或 `False`，表示是否设置 Target 新建 LUN 的置备方式为精简置备。 |
| `--storage_pool_id <STORAGE_POOL_ID>` | 更新 Target 所属的存储池。 |
| `--whitelist <WHITELIST>` | 更新 iSCSI Target 的 IP 白名单，可输入 IP 地址或 CIDR 块。`*/*` 表示任何 IP 都可以访问此 Target。 |
| `--iqn_whitelist <IQN_WHITELIST>` | 更新 iSCSI Target 的 IQN 白名单，多个 IQN 之间以英文逗号 `,` 分隔。 |
| `--adaptive_iqn_whitelist <ADAPTIVE_IQN_WHITELIST>` | `True` 或 `False`，表示是否启用 IQN 白名单自适应功能。开启后，IQN 白名单会自动保持为所包含 LUN 的 IQN 白名单的并集。开启自适应功能时，不应同时设置 `--iqn_whitelist`、`allowed_host_ids` 和 `allowed_host_group_ids` 参数。 |
| `--external_use <EXTERNAL_USE>` | `True` 或 `False`，表示 Target 是否用作外部接入。 |
| `--stripe_num <STRIPE_NUM>` | 更新 Target 新建 LUN 的条带数。 |
| `--stripe_size <STRIPE_SIZE>` | 更新 Target 新建 LUN 的条带大小。 |
| `--enable_target_chap <ENABLE_TARGET_CHAP>` | `True` 或 `False`，开启或关闭 Target CHAP 认证。 |
| `--remove_target_chap <REMOVE_TARGET_CHAP>` | 移除 Target CHAP 认证信息。 |
| `--target_chap_name <TARGET_CHAP_NAMEE>` | 更新 Target CHAP 认证名称。允许输入长度为 1 ~ 223 的字母、数字，以及特殊符号 `.`、`-`、`:`。 |
| `--target_secret <TARGET_SECRET>` | 更新 Target CHAP 认证密码。允许输入长度 12 ~ 16 的字母和数字。 |
| `--iops <IOPS>` | 更新 Target 内新建 LUN 的读写总 IOPS 上限值。 |
| `--iops_rd <IOPS_RD>` | 更新读 IOPS 的上限值。 |
| `--iops_wr <IOPS_WR>` | 更新写 IOPS 的上限值。 |
| `--iops_max <IOPS_MAX>` | 更新读写总 IOPS 突发的上限值。 |
| `--iops_rd_max <IOPS_RD_MAX>` | 更新读 IOPS 突发的上限值。 |
| `--iops_wr_max <IOPS_WR_MAX>` | 更新写 IOPS 突发的上限值。 |
| `--iops_max_length <IOPS_MAX_LENGTH>` | 更新读写总 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_rd_max_length <IOPS_RD_MAX_LENGTH>` | 更新读 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_wr_max_length <IOPS_WR_MAX_LENGTH>` | 更新写 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_io_size <IOPS_IO_SIZE>` | 更新使用 IOPS 限速时假定的平均 I/O 数据量大小。 |
| `--bps <BPS>` | 更新 Target 内新建 LUN 的读写总带宽限制，单位为 Bps。 |
| `--bps_rd <BPS_RD>` | 更新读带宽的上限值。 |
| `--bps_wr <BPS_WR>` | 更新写带宽的上限值。 |
| `--bps_max <BPS_MAX>` | 更新读写总带宽在发生 I/O 突发时的上限值。 |
| `--bps_rd_max <BPS_RD_MAX>` | 更新读带宽在发生 I/O 突发时的上限值。 |
| `--bps_wr_max <BPS_WR_MAX>` | 更新写带宽在发生 I/O 突发时的上限值。 |
| `--bps_max_length <BPS_MAX_LENGTH>` | 更新在发生 I/O 突发时，以读写总带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_rd_max_length <BPS_RD_MAX_LENGTH>` | 更新在发生 I/O 突发时，以读带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_wr_max_length <BPS_WR_MAX_LENGTH>` | 更新在发生 I/O 突发时，以写带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--resiliency_type <RESILIENCY_TYPE>` | 更新冗余模式，副本或 EC，默认为 `None`。 |
| `--ec_algo <EC_ALGO>` | 更新 EC 算法，当冗余模式为 EC 时必须设置，默认为 `RS`。 |
| `--ec_k <EC_K>` | 更新 EC 算法参数 K，参数范围为 [2，23]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--ec_m <EC_M>` | 更新 EC 算法参数 M，参数范围为 [1，4]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--encrypt_method <ENCRYPT_METHOD>` | 设置数据加密方法，默认为不加密 。 |
| `--recursive` | 递归地更新 Target 内的所有 LUN 的副本数至较大或相等的副本数，默认为 `False`。 |
| `--prioritized <PRIORITIZED>` | 更新在 Target 内创建 LUN 时是否默认开启常驻缓存的设置，可设置为 `True` 或 `False`。 |
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

## 删除 iSCSI Target

**操作方法**

在集群任一节点执行如下命令，删除指定的 iSCSI Target：

`zbs-iscsi target delete <name> [--recursive {true | false}]`

| 参数 | 说明 |
| --- | --- |
| `name` | 待删除 Target 名称。 |
| `--recursive` | `True` 或 `False`，是否清空 Target 内的所有 LUN，默认为 `None`（等效于否）。 |

**输出说明**

执行成功无输出。

## 设置 Initiator CHAP 认证

设置客户端对 iSCSI Target 的认证

**操作方法**

在集群任一节点执行如下命令，设置 Initiator 认证：

`zbs-iscsi initiator_chap create <name> <iqn> <chap_name> <chap_password> {true|false}`

| 参数 | 说明 |
| --- | --- |
| `name` | Target 名称。 |
| `iqn` | Initiator IQN 名称。 |
| `chap_name` | Initiator CHAP 认证名称。允许输入长度为 1 ~ 512 的字母、数字，以及 `.`、`-`、`:`。 |
| `chap_password` | Initiator CHAP 认证密码。允许输入长度 12 ~ 512 的字母和数字。 |
| `true` 或 `false` | 是否开启 Initiator 认证。 |

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

## 更新 Initiator CHAP 认证设置

**操作方法**

在集群任一节点执行如下命令，更新 Initiator CHAP 认证设置：

`zbs-iscsi initiator_chap update <name> <iqn> <chap_name> <chap_password> {true|false}`

| 参数 | 说明 |
| --- | --- |
| `name` | Target 名称。 |
| `iqn` | Initiator IQN 名称。 |
| `chap_name` | Initiator CHAP 认证名称。允许输入长度为 1 ~ 512 的字母、数字，以及 `.`、`-`、`:`。 |
| `chap_password` | Initiator CHAP 认证密码。允许输入长度 12 ~ 512 的字母和数字。 |
| `true` 或 `false` | 是否开启 Initiator 认证。 |

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

## 关闭 Initiator CHAP 认证

**操作方法**

在集群任一节点执行如下命令，关闭 Initiator CHAP 认证：

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

更新 iSCSI Target CHAP 的认证。

**操作方法**

在集群任一节点执行如下命令：

`zbs-iscsi target update [--enable_target_chap <ENABLE_TARGET_CHAP>] [--target_chap_name <TARGET_CHAP_NAME>] [--target_secret <TARGET_SECRET>] [--remove_target_chap <REMOVE_TARGET_CHAP>] <name>`

| 参数 | 说明 |
| --- | --- |
| `--enable_target_chap <ENABLE_TARGET_CHAP>` | `True` 或 `False`，选择开启或关闭 Target CHAP 认证。 |
| `--target_chap_name <TARGET_CHAP_NAME>` | Target CHAP 认证用户名。允许输入长度为 1 ~ 223 的字母、数字，以及特殊字符 `.`、`-`、`:`。 |
| `--target_secret <TARGET_SECRET>` | Target CHAP 认证密码。允许输入长度 12 ~ 16 的字母和数字。 |
| `--remove_target_chap <REMOVE_TARGET_CHAP>` | 删除 Target CHAP 信息，默认为 `None`。 |
| `name` | iSCSI Target 名称。 |

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

## 块存储集群 CLI 命令 > 管理 iSCSI 存储服务 > 管理 iSCSI LUN

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
- **查看指定 Secondary ID 的 iSCSI LUN**

  在集群任一节点执行如下命令：

  `zbs-iscsi lun show_target_and_lun_by_secondary_id <secondary_id>`
- **查看某个 iSCSI Target 下所有的 LUN**

  在集群任一节点执行如下命令：

  `zbs-iscsi lun list <target_name>`

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `[--all]` | 可选参数，显示 LUN 的所有参数。 |
| `<target_name>` | 必选参数，LUN 所属的 Target 名称。 |
| `<lun_id>` | 必选参数，待查看的 LUN 的 ID。 |
| `<lun_name>` | 必选参数，待查看的 LUN 的名称。 |
| `<lun_uuid>` | 必选参数，待查看的 LUN 的 Volume ID。 |
| `<secondary_id>` | 必选参数，待查看的 LUN 的 Secondary ID。 |

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
| `Allowed Initiators` | LUN 级别的 Initiator 白名单。 |
| `Single Access` | 是否开启了 Single Access。若开启了 Single Access，Volume 仅能被唯一客户端访问。 |
| `PR` | Persistence Reserve 永久保留信息。 |
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
| `target_name` | LUN 所属的 Target 名称。 |
| `lun_id` | LUN ID。 |
| `size` | LUN 大小。 |
| `--lun_name <LUN_NAME>` | 新建 LUN 名称。 |
| `--lun_uuid <LUN_UUID>` | 新建 LUN UUID。 |
| `--resiliency_type <RESILIENCY_TYPE>` | 设置冗余模式，副本或 EC，若未设置，将从 Target 继承，默认为 `None`。 |
| `--replica_num <REPLICA_NUM>` | 设置新建 LUN 的默认副本数，可设置为 2 副本或 3 副本，默认为 `None`。 |
| `--ec_algo <EC_ALGO>` | 设置 EC 算法，当冗余模式为 EC 时必须设置，默认为 RS。 |
| `--ec_k <EC_K>` | 设置 EC 算法参数 K，参数范围为 [2，23]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--ec_m <EC_M>` | 设置 EC 算法参数 M，参数范围为 [1，4]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--ec_block_size <EC_BLOCK_SIZE>` | 当冗余模式为 EC 时，默认为 4096，否则默认为 `None`。 |
| `--encrypt_method <ENCRYPT_METHOD>` | 设置数据加密方法，默认为不加密 。 |
| `--thin_provision <THIN_PROVISION>` | True 或 False，表示是否设置新建 LUN 的置备方式为精简置备。 |
| `--desc <DESC>` | 设置 LUN 描述。 |
| `--stripe_num <STRIPE_NUM>` | 新建 LUN 的条带数。 |
| `--stripe_size <STRIPE_SIZE>` | 新建 LUN 的条带大小。 |
| `--iops <IOPS>` | 设置新建 LUN 的读写总 IOPS 上限值。 |
| `--iops_rd <IOPS_RD>` | 设置读 IOPS 的上限值。 |
| `--iops_wr <IOPS_WR>` | 设置写 IOPS 的上限值。 |
| `--iops_max <IOPS_MAX>` | 设置读写总 IOPS 突发的上限值。 |
| `--iops_rd_max <IOPS_RD_MAX>` | 设置读 IOPS 突发的上限值。 |
| `--iops_wr_max <IOPS_WR_MAX>` | 设置写 IOPS 突发的上限值。 |
| `--iops_max_length <IOPS_MAX_LENGTH>` | 设置读写总 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_rd_max_length <IOPS_RD_MAX_LENGTH>` | 设置读 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_wr_max_length <IOPS_WR_MAX_LENGTH>` | 设置写 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_io_size <IOPS_IO_SIZE>` | 使用 IOPS 限速时，假定的平均 I/O 数据量大小。 |
| `--bps <BPS>` | 设置新建 LUN 的读写总带宽限制，单位为 Bps。 |
| `--bps_rd <BPS_RD>` | 设置读带宽的上限值。 |
| `--bps_wr <BPS_WR>` | 设置写带宽的上限值。 |
| `--bps_max <BPS_MAX>` | 设置读写总带宽在发生 I/O 突发时的上限值。 |
| `--bps_rd_max <BPS_RD_MAX>` | 设置读带宽在发生 I/O 突发时的上限值。 |
| `--bps_wr_max <BPS_WR_MAX>` | 设置写带宽在发生 I/O 突发时的上限值。 |
| `--bps_max_length <BPS_MAX_LENGTH>` | 设置在发生 I/O 突发时，以读写总带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_rd_max_length <BPS_RD_MAX_LENGTH>` | 设置在发生 I/O 突发时，以读带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_wr_max_length <BPS_WR_MAX_LENGTH>` | 设置在发生 I/O 突发时，以写带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--allowed_initiators <ALLOWED_INITIATORS>` | 设置可以访问该 LUN 的 Initiator 白名单，以英文逗号（,）分隔多个 IQN。默认参数允许所有 Initiator 访问，设置为空则禁止所有 Initiator 访问。 |
| `--preferred_cid <PREFERRED_CID>` | 设置倾向节点的 chunk ID（多物理盘池环境下节点中任一 chunk ID 均可），Meta 在分配 PExtent 副本时，会尽量靠近该 chunk 所在的节点。 |
| `--single_access <SINGLE_ACCESS>` | True 或 False，若为 True，则只有一个 Initiator 可以访问该 LUN，且该 LUN 的 IQN 白名单只能为空或单个 IQN。 |
| `--prioritized <PRIORITIZED>` | 设置 LUN 的 prioritized 属性，即设置 LUN 的数据是否都需要维持在性能层中，可设置为 `True` 或 `False`。 |
| `target_name` | LUN 所属的 Target 名称。 |
| `lun_id` | LUN ID。 |
| `size` | LUN 大小。 |
| `--use_host <USE_HOST>` | 设置是否使用业务主机指定白名单。use\_host 为 `true` 时，不允许设置 `allowed_initiators` 参数；为 `false` 时，不允许设置 `allowed_host_ids` 和 `allowed_host_group_ids` 参数。 |
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
| `target_name` | LUN 所属的 Target 名称。 |
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
| `--src_target_name <SRC_TARGET_NAME>` | 克隆的源 Target 名称。 |
| `--src_lun_id <SRC_LUN_ID>` | 克隆的源 LUN ID。 |
| `--src_snapshot_id <SRC_SNAPSHOT_ID>` | 克隆的源 Snapshot ID，若源 LUN ID 和源 Snapshot ID 均被指定，则使用源 Snapshot ID 作为克隆源。 |
| `dst_target_name` | 克隆 LUN 所属的 Target。 |
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

## 移动 iSCSI LUN 至另一 iSCSI Target

**操作方法**

在集群任一节点执行如下命令，将 LUN 从当前所属 Target 移动至另一 Target：

`zbs-iscsi lun move <src_target_name> <src_lun_id> <target_name> <lun_id> <lun_name>`

| 参数 | 说明 |
| --- | --- |
| `src_target_name` | LUN 所属源 Target。 |
| `src_lun_id` | 待移动的 LUN ID。 |
| `target_name` | LUN 移动的目的 Target。 |
| `lun_id` | 移动至新 Target 后的 LUN ID。 |
| `lun_name` | 移动至新 Target 后的 LUN 名称。 |

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
| `target_name` | LUN 所属的 iSCSI Target 名称。 |
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
| `target_name` | LUN 所属的 iSCSI Target 名称。 |
| `lun_id` | LUN 名称。 |
| `ininitiators` | 移除可访问 LUN 的客户端 IQN 白名单，多个客户端之间以英文逗号 `,` 隔开，例如：`iqn.1994-05.com.redhat:d422cf1e7f5,iqn.1994-05.com.redhat:1`。 |

**输出说明**

执行成功无输出。

## 删除 iSCSI LUN

**操作方法**

在集群任一节点执行如下命令，删除 iSCSI Target 下的指定 LUN：

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

---

## 块存储集群 CLI 命令 > 管理 iSCSI 存储服务 > 管理 iSCSI LUN 快照

# 管理 iSCSI LUN 快照

## 查看 iSCSI LUN 快照

**操作方法**

- 在集群任一节点执行如下命令，查看指定 Target 下的所有 iSCSI LUN 快照：

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
| `--new_desc <NEW_NAME>` | 更新对相应快照的名称。 |
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

## 块存储集群 CLI 命令 > 管理 NVMe-oF 存储服务

# 管理 NVMe-oF 存储

SMTX ZBS 块存储集群支持外部计算平台通过 NVMe over TCP 和 NVMe over RDMA 协议远程访问其块存储服务。用户可以使用命令行管理集群的 NVMe Subsystem 和 NVMe Namespace。

---

## 块存储集群 CLI 命令 > 管理 NVMe-oF 存储服务 > 管理 NVMe Subsystem

# 管理 NVMe Subsystem

## 查看 NVMe Subsystem

**操作方法**

在集群任一节点执行如下命令，查看 NVMe Subsystem：

- 查看指定名称的 Subsystem：

  `zbs-nvmf subsystem show <name>`
- 查看所有的 Subsystem：

  `zbs-nvmf subsystem list`

**输出示例**

```
----------------------  ------------------------------------
ID                      3f142bc6-2f22-4829-a755-9c276b198b68
Name                    s1
NQN Name                nqn.2020-12.com.smartx:system:s1
Creation Time           2025-06-26 16:43:09.743494209
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Replica#                2
EC Param
Thin                    True
Description
Storage Pool            system
NQN Whitelist           */*
IPv4 Whitelist          */*
Policy                  INHERIT_POLICY
Stripe Num              8
Stripe Size             262144
Labels                  []
Is Prioritized          False
Adaptive NQN Whitelist  False
Use Host                False
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 创建 NVMe Subsystem

**操作方法**

在集群任一节点执行如下命令，创建指定名称的 NVMe Subsystem：

```
zbs-nvmf subsystem create <name> [--nqn_whitelist <nqn_whitelist>]
                                 [--ipv4_whitelist <ipv4_whitelist>]
                                 [--policy <policy>]
                                 [--replica_num <REPLICA_NUM>]
                                 [--thin_provision {true | false}]
                                 [--nqn_date <NQN_DATE>]
                                 [--nqn_naming_auth <NQN_NAMING_AUTH>]
                                 [--resiliency_type <RESILIENCY_TYPE>]
                                 [--ec_algo <EC_ALGO>] [--ec_k <EC_K>]
                                 [--ec_m <EC_M>] [--desc <DESC>]
                                 [--storage_pool_id <STORAGE_POOL_ID>]
                                 [--iops <IOPS>]
                                 [--iops_rd <IOPS_RD>] [--iops_wr <IOPS_WR>]
                                 [--iops_max <IOPS_MAX>]
                                 [--iops_rd_max <IOPS_RD_MAX>]
                                 [--iops_wr_max <IOPS_WR_MAX>]
                                 [--iops_max_length <IOPS_MAX_LENGTH>]
                                 [--iops_rd_max_length <IOPS_RD_MAX_LENGTH>]
                                 [--iops_wr_max_length <IOPS_WR_MAX_LENGTH>]
                                 [--iops_io_size <IOPS_IO_SIZE>]
                                 [--bps <BPS>] [--bps_rd <BPS_RD>] [--bps_wr <BPS_WR>]
                                 [--bps_max <BPS_MAX>] [--bps_rd_max <BPS_RD_MAX>]
                                 [--bps_wr_max <BPS_WR_MAX>]
                                 [--bps_max_length <BPS_MAX_LENGTH>]
                                 [--bps_rd_max_length <BPS_RD_MAX_LENGTH>]
                                 [--bps_wr_max_length <BPS_WR_MAX_LENGTH>]
                                 [--stripe_num <STRIPE_NUM>]
                                 [--stripe_size <STRIPE_SIZE>]
                                 [--prioritized <PRIORITIZED>]
                                 [--use_host <USE_HOST>]
                                 [--allowed_host_ids <ALLOWED_HOST_IDS>]
                                 [--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>]
```

| 参数 | 说明 |
| --- | --- |
| `name` | 新建 Subsystem 的名称。 |
| `--nqn_whitelist <nqn_whitelist>` | 设置 Subsystem 的 NQN 白名单，多个 NQN 之间用英文逗号 `,` 隔开，例如：`nqn.1994-05.com.smartx:aaaa,nqn.1994-05.com.smartx:bbbb`。`*/*` 表示允许所有 NQN 访问。默认为空，表示所有 NQN 均可访问。 |
| `--ipv4_whitelist <ipv4_whitelist>` | 设置 Subsystem 的 IP 白名单，多个 IP 之间用英文逗号 `,` 隔开，例如：`192.168.10.11/24,192.168.10.112/24`。`*/*` 表示允许所有 IP 访问。默认为空，表示所有 IP 均可访问。 |
| `--policy <policy>` | Subsystem 的接入点分配策略，可选值为 `INHERIT`（继承策略） 和 `BALANCE` （均衡策略）。 |
| `--replica_num <REPLICA_NUM>` | 设置副本数，可设置为 2 副本或 3 副本。 |
| `--thin_provision {true &#124; false}` | 是否为精简置备。 |
| `--nqn_date <NQN_DATE>` | 用于生成 Subsystem 的 NQN，必须为 `yyyy-mm` 格式，默认为 `None`。 |
| `--nqn_naming_auth <NQN_NAMING_AUTH>` | 指定 Naming Auth，用于生成 Subsystem 的 NQN。格式为 `com.公司名`，默认为 `None`。 |
| `--resiliency_type <RESILIENCY_TYPE>` | 设置冗余模式，副本或 EC，默认为 `None`。 |
| `--ec_algo <EC_ALGO>` | 设置 EC 算法，当冗余模式为 EC 时必须设置，默认为 RS。 |
| `--ec_k <EC_K>` | 设置 EC 算法参数 K，参数范围为 [2，23]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--ec_m <EC_M>` | 设置 EC 算法参数 M，参数范围为 [1，43]，当冗余模式为 EC 时必须设置，默认为 `None`。 |
| `--desc <DESC>` | 设置 Subsystem 描述。 |
| `--storage_pool_id <STORAGE_POOL_ID>` | 设置创建新 Subsystem 的 Storage Pool ID，默认为 `None`。 |
| `--iops <IOPS>` | 设置 Subsystem 内新建 NS 的读写总 IOPS 上限值。 |
| `--iops_rd <IOPS_RD>` | 设置读 IOPS 的上限值。 |
| `--iops_wr <IOPS_WR>` | 设置写 IOPS 的上限值。 |
| `--iops_max <IOPS_MAX>` | 设置读写总 IOPS 突发的上限值。 |
| `--iops_rd_max <IOPS_RD_MAX>` | 设置读 IOPS 突发的上限值。 |
| `--iops_wr_max <IOPS_WR_MAX>` | 设置写 IOPS 突发的上限值。 |
| `--iops_max_length <IOPS_MAX_LENGTH>` | 设置读写总 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_rd_max_length <IOPS_RD_MAX_LENGTH>` | 设置读 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_wr_max_length <IOPS_WR_MAX_LENGTH>` | 设置写 IOPS 突发的持续时长限制，单位为秒。 |
| `--iops_io_size <IOPS_IO_SIZE>` | 使用 IOPS 限速时，假定的平均 I/O 数据量大小。 |
| `--bps <BPS>` | 设置 Subsystem 内新建 NS 的读写总带宽限制，单位为 Bps。 |
| `--bps_rd <BPS_RD>` | 设置读带宽的上限值。 |
| `--bps_wr <BPS_WR>` | 设置写带宽的上限值。 |
| `--bps_max <BPS_MAX>` | 设置读写总带宽在发生 I/O 突发时的上限值。 |
| `--bps_rd_max <BPS_RD_MAX>` | 设置读带宽在发生 I/O 突发时的上限值。 |
| `--bps_wr_max <BPS_WR_MAX>` | 设置写带宽在发生 I/O 突发时的上限值。 |
| `--bps_max_length <BPS_MAX_LENGTH>` | 设置在发生 I/O 突发时，以读写总带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_rd_max_length <BPS_RD_MAX_LENGTH>` | 设置在发生 I/O 突发时，以读带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--bps_wr_max_length <BPS_WR_MAX_LENGTH>` | 设置在发生 I/O 突发时，以写带宽上限进行 I/O 的持续时长限制。单位为秒。 |
| `--stripe_num <STRIPE_NUM>` | Subsystem 新建 NS 的条带数。 |
| `--stripe_size <STRIPE_SIZE>` | Subsystem 新建 NS 的条带大小。 |
| `--prioritized <PRIORITIZED>` | 设置在 Subsystem 内创建 Namespace 时是否默认开启常驻缓存，可设置为 `True` 或 `False`。 |
| `--use_host <USE_HOST>` | 设置是否使用业务主机指定白名单。use\_host 为 `true` 时，不允许设置 `nqn_whitelist` 和 `ipv4_whitelist` 参数；为 `false` 时，不允许设置 `allowed_host_ids` 和 `allowed_host_group_ids` 参数。 |
| `--allowed_host_ids <ALLOWED_HOST_IDS>` | 设置关联的业务主机的 ID，以英文逗号（,）分隔多个 ID。 |
| `--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>` | 设置关联的业务主机组的 ID，以英文逗号（,）分隔多个 ID。 |

**输出示例**

```
----------------------  ------------------------------------
ID                      568b7280-d9de-40ff-9f93-d1512bc6b292
Name                    s3
NQN Name                nqn.2020-12.com.smartx:system:s3
Creation Time           2025-07-07 10:26:22.27914478
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Replica#                2
EC Param
Thin                    True
Description
Storage Pool            system
NQN Whitelist           */*
IPv4 Whitelist          */*
Policy                  INHERIT_POLICY
Stripe Num              8
Stripe Size             262144
Labels                  []
Is Prioritized          False
Adaptive NQN Whitelist  False
Use Host                False
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 更新 NVMe Subsystem

**操作方法**

在集群任一节点执行如下命令，更新 NVMe Subsystem：

```
zbs-nvmf subsystem update <name> [--nqn_whitelist <nqn_whitelist>]
                                 [--ipv4_whitelist <ipv4_whitelist>]
                                 [--replica_num <REPLICA_NUM>]
                                 [--thin_provision {true | false}]
                                 [--recursive]
                                 [--use_host <USE_HOST>]
                                 [--allowed_host_ids <ALLOWED_HOST_IDS>]
                                 [--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>]
```

| 参数 | 说明 |
| --- | --- |
| `name` | Subsystem 的名称。 |
| `--nqn_whitelist <nqn_whitelist>` | 更新 Subsystem 的 NQN 白名单，多个 NQN 之间用英文逗号 `,` 隔开，例如：`nqn.1994-05.com.smartx:aaaa,nqn.1994-05.com.smartx:bbbb`。`*/*` 表示允许所有 NQN 访问。 |
| `--ipv4_whitelist <ipv4_whitelist>` | 更新 Subsystem 的 IP 白名单，多个 IP 之间用英文逗号 `,` 隔开，例如：`192.168.10.11/24,192.168.10.112/24`。`*/*` 表示允许所有 IP 访问。 |
| `--replica_num <REPLICA_NUM>` | 更新副本数，只支持提高副本数，不支持降低副本数。 |
| `--thin_provision` | 是否为精简置备。 |
| `--recursive` | 递归地更新 Subsystem 内的所有 NS 的副本数至较大或相等的副本数，默认为 `False`。 |
| `--use_host <USE_HOST>` | 更新是否使用业务主机指定白名单。use\_host 为 `true` 时，不允许设置 `nqn_whitelist` 和 `ipv4_whitelist` 参数；为 `false` 时，不允许设置 `allowed_host_ids` 和 `allowed_host_group_ids` 参数。 |
| `--allowed_host_ids <ALLOWED_HOST_IDS>` | 更新关联的业务主机的 ID，以英文逗号（,）分隔多个 ID。 |
| `--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>` | 更新关联的业务主机组的 ID，以英文逗号（,）分隔多个 ID。 |

**输出示例**

```
----------------------  ------------------------------------
ID                      568b7280-d9de-40ff-9f93-d1512bc6b292
Name                    s3
NQN Name                nqn.2020-12.com.smartx:system:s3
Creation Time           2025-07-07 10:26:22.27914478
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Replica#                2
EC Param
Thin                    True
Description
Storage Pool            system
NQN Whitelist
IPv4 Whitelist
Policy                  INHERIT_POLICY
Stripe Num              8
Stripe Size             262144
Labels                  []
Is Prioritized          False
Adaptive NQN Whitelist  False
Use Host                True
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 删除 NVMe Subsystem

删除指定名字的 NVMe Subsystem。仅当该 Subsystem 下不包含任何 namespace、ns\_group、snapshot 时可以删除.

**操作方法**

在集群任一节点执行如下命令，删除指定名称的 Subsystem：

`zbs-nvmf subsystem delete <name> [--recursive {true | false}]`

| 参数 | 说明 |
| --- | --- |
| `name` | 待删除 Subsystem 名称。 |
| `--recursive` | `True` 或 `False`，是否删除 Subsystem 内所有 Namespace，默认为 `None` （等效于否）。 |

**输出示例**

执行成功无输出。

## 查看 NVMe Subsystem 接入点信息

查看 NVMe Subsystem 接入点信息。仅对使用了继承策略的 NVMe Subsystem 生效。

**操作方法**

在集群任一节点执行如下命令，查看指定 Subsystem 的活跃接入记录：

`zbs-nvmf access get <subsystem_id>`

**输出示例**

```
Host NQN                                                                CID
--------------------------------------------------------------------  -----
nqn.2014-08.org.nvmexpress:uuid:82729b6b-4541-41a9-a75b-7bced1d407bd      2
```

## 更新 Host NQN 访问指定 Subsystem 的接入点

更新 Host NQN 访问指定 Subsystem 的接入点。仅对继承策略生效。

**操作方法**

在集群任一节点执行如下命令：

`zbs-nvmf access set <subsystem_id> <host_nqn> <cid>`

**输出示例**

```
{ 'cid': 3,
  'host_nqn': u'nqn.2014-08.org.nvmexpress:uuid:82729b6b-4541-41a9-a75b-7bced1d407bd',
  'subsystem_id': u'f01723e2-52d2-4fcd-9fe0-919571421fc4'}
```

---

## 块存储集群 CLI 命令 > 管理 NVMe-oF 存储服务 > 管理 NVMe Namespace Group

# 管理 NVMe Namespace Group

## 查看 Subsystem 包含的 Namespace Group

**操作方法**

在集群任一节点执行如下命令，查看 Subsystem 包含的 Namespace Group：

`zbs-nvmf ns_group list <subsystem_name>`

**输出示例**

```
NS Group Id                           NS Group Name    Creation Time
------------------------------------  ---------------  ----------------------------
50f930d6-74e2-44b7-9bea-170ad8d24723  group            2021-09-22 21:24:34.16247403
870497b0-89cc-4efc-a10d-eae90e82979b  group2           2021-09-22 21:24:39.39178730
```

## 查看 Namespace Group 详细信息

**操作方法**

在集群任一节点执行如下命令：

`zbs-nvmf ns_group show <subsystem_name> <ns_group_name>`

**输出示例**

```
-------------  ------------------------------------
NS Group Id    50f930d6-74e2-44b7-9bea-170ad8d24723
NS Group Name  group
Creation Time  2021-09-22 21:24:34.16247403
-------------  ------------------------------------
```

## 创建 NVMe Namespace Group

**操作方法**

在集群任一节点执行如下命令：

`zbs-nvmf ns_group create <subsystem_name> <ns_group_name>`

**输出示例**

```
-------------  ------------------------------------
NS Group Id    4f822e9c-4abf-4921-9326-48d725ef240f
NS Group Name  group
Creation Time  2021-09-22 18:23:40.101436428
-------------  ------------------------------------
```

## 更新 Namespace Group 名称

**操作方法**

在集群任一节点执行如下命令：

`zbs-nvmf ns_group update <subsystem_name> <ns_group_name> [--new_name <new_name>]`

**输出示例**

```
-------------  ------------------------------------
NS Group Id    4f822e9c-4abf-4921-9326-48d725ef240f
NS Group Name  newgroup
Creation Time  2021-09-22 18:23:40.101436428
-------------  ------------------------------------
```

## 删除 Namespace Group

**操作方法**

在集群任一节点执行如下命令：

`zbs-nvmf ns_group delete <subsystem_name> <ns_group_name>`

**输出示例**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理 NVMe-oF 存储服务 > 管理 NVMe Namespace

# 管理 NVMe Namespace

## 查看 NVMe Namespace

**操作方法**

在集群任一节点执行如下命令，查看 Subsystem 中的 Namespace：

`zbs-nvmf ns list <subsystem_name>`

**输出示例**

```
  NS Id  NS Name                               Size       Perf Unique Size    Perf Shared Size    Cap Unique Size    Cap Shared Size    Logical Used Size    Is Shared    Volume id                             Resiliency Type    Encrypt Method        Encrypt Metadata Id    Replica Num  EC Param    Thin Provision    Group id      Preferred Access  Creation Time                  Description    NQN Whitelist    Single Access    Read Only    Is Prioritized    Downgraded PRS    Chunk Instances    Use Host    Allowed Host Ids    Allowed Host Group Ids
-------  ------------------------------------  ---------  ------------------  ------------------  -----------------  -----------------  -------------------  -----------  ------------------------------------  -----------------  ------------------  ---------------------  -------------  ----------  ----------------  ----------  ------------------  -----------------------------  -------------  ---------------  ---------------  -----------  ----------------  ----------------  -----------------  ----------  ------------------  ------------------------
      1  53bcb51f-be35-4cc6-be14-d9206574b3c7  10.00 GiB  In Process          In Process          In Process         In Process         In Process           False        53bcb51f-be35-4cc6-be14-d9206574b3c7  RT_REPLICA         ENCRYPT_PLAIN_TEXT                      0              2              True                                           0  2025-07-07 11:09:18.56490093                                   False            False        False             0.00 B                               True
      2  53c12af7-1996-4641-8f18-a256fa589d4d  10.00 GiB  In Process          In Process          In Process         In Process         In Process           False        53c12af7-1996-4641-8f18-a256fa589d4d  RT_REPLICA         ENCRYPT_PLAIN_TEXT                      0              2              True                                           0  2025-07-07 11:09:21.484915134                                  False            False        False             0.00 B                               True
```

## 查看指定的 NVMe Namespace

**操作方法**

- 查看指定 ID 的 Namespace：

  `zbs-nvmf ns show <subsystem_name> <ns_id> [--detail]`
- 查看指定名称的 Namespace：

  `zbs-nvmf ns show_by_name <subsystem_name> <ns_name> [--detail]`

**输出示例**

```
----------------------  ------------------------------------
NS Id                   1
NS Name                 53bcb51f-be35-4cc6-be14-d9206574b3c7
Size                    10.00 GiB
Perf Unique Size        0.00 B
Perf Shared Size        0.00 B
Cap Unique Size         0.00 B
Cap Shared Size         0.00 B
Logical Used Size       0.00 B
Is Shared               False
Volume id               53bcb51f-be35-4cc6-be14-d9206574b3c7
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Encrypt Metadata Id     0
Replica Num             2
EC Param
Thin Provision          True
Group id
Preferred Access        0
Creation Time           2025-07-07 11:09:18.56490093
Description
NQN Whitelist
Single Access           False
Read Only               False
Is Prioritized          False
Downgraded PRS          0.00 B
Chunk Instances
Use Host                True
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 创建 NVMe Namespace

**操作方法**

在集群任一节点执行如下命令，创建 NVMe Namespace：

```
zbs-nvmf ns create <subsystem name> <ns_id> <size> [--ns_name <NS_NAME>]
                                                   [--desc <DESC>]
                                                   [--replica_num <REPLICA_NUM>]
                                                   [--thin_provision {true | false}]
                                                   [--group_id <GROUP_ID>]
                                                   [--nqn_whitelist <NQN_WHITELIST>]
                                                   [--stripe_num <STRIPE_NUM>]
                                                   [--stripe_size <STRIPE_SIZE>]
                                                   [--ec_block_size <EC_BLOCK_SIZE>]
                                                   [--is_shared <IS_SHARED>]
                                                   [--single_access <SINGLE_ACCESS>]
                                                   [--prioritized PRIORITIZED]
                                                   [--use_host <USE_HOST>]
                                                   [--allowed_host_ids <ALLOWED_HOST_IDS>]
                                                   [--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>]
```

| 参数 | 说明 |
| --- | --- |
| `subsystem name` | Namespace 所属的 Subsystem。 |
| `ns_id` | Namespace ID，可取 0 到 255 的正整数。若取值为 0，则自动为 Namespace 分配最小可用正整数作为 ID。 |
| `size` | Namespace 的大小。 |
| `--ns_name <NS_NAME>` | Namespace 的名称。 |
| `--desc <DESC>` | Namespace 的描述。 |
| `--nqn_whitelist <nqn_whitelist>` | Namespace 的 NQN 白名单，多个 NQN 之间用英文逗号 `,` 隔开，例如：`nqn.1994-05.com.smartx:aaaa,nqn.1994-05.com.smartx:bbbb`。 |
| `--replica_num <REPLICA_NUM>` | Namespace 的副本数。 |
| `--thin_provision` | `true` 或 `false`，表示 Namespace 是否为精简置备。 |
| `--group_id <GROUP_ID>` | 目标 Namespace 的 NS Group ID。均衡策略必须指定。 |
| `--stripe_num <STRIPE_NUM>` | 条带数。 |
| `--stripe_size <STRIPE_SIZE>` | 条带大小。 |
| `--ec_block_size <EC_BLOCK_SIZE>` | 当冗余模式为 EC 时，默认为 4096，否则默认为 `None`。 |
| `--is_shared <IS_SHARED>` | Namespace 是否被多个 Host 共享。 |
| `--single_access <SINGLE_ACCESS>` | `True` 或 `False`，若为 `True`，则只有一个 Host 可以访问该 Namespace，且该 Namespace 的 NQN 白名单只能为空或单个 NQN。 |
| `--prioritized <PRIORITIZED>` | 设置 Namespace 的 prioritized 属性，即设置 Namespace 的数据是否都需要维持在性能层中，可设置为 `True` 或 `False`。 |
| `--use_host <USE_HOST>` | 设置是否使用业务主机指定白名单。use\_host 为 `true` 时，不允许设置 `nqn_whitelist` 参数；为 `false` 时，不允许设置 `allowed_host_ids` 和 `allowed_host_group_ids` 参数。 |
| `--allowed_host_ids <ALLOWED_HOST_IDS>` | 设置关联的业务主机的 ID，以英文逗号（,）分隔多个 ID。 |
| `--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>` | 设置关联的业务主机组的 ID，以英文逗号（,）分隔多个 ID。 |

**输出示例**

```
----------------------  ------------------------------------
NS Id                   3
NS Name                 e2f07e5a-1f1b-4821-ae0a-1b9b748ae0f5
Size                    10.00 GiB
Perf Unique Size        In Process
Perf Shared Size        In Process
Cap Unique Size         In Process
Cap Shared Size         In Process
Logical Used Size       In Process
Is Shared               False
Volume id               e2f07e5a-1f1b-4821-ae0a-1b9b748ae0f5
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Encrypt Metadata Id     0
Replica Num             2
EC Param
Thin Provision          True
Group id
Preferred Access        0
Creation Time           2025-07-07 11:20:43.543474145
Description
NQN Whitelist
Single Access           False
Read Only               False
Is Prioritized          False
Downgraded PRS          0.00 B
Chunk Instances
Use Host                True
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 克隆 NVMe Namespace

**操作方法**

在集群任一节点执行如下命令，从一个已有的 Namespace 或者快照，克隆到新的 Namespace：

`zbs-nvmf ns clone <dst_subsystem> <dst_ns_id> [--src_subsystem_name <SRC_SUBSYSTEM_NAME>][--src_ns_id <SRC_NS_ID>][--src_snapshot_id <SRC_SNAPSHOT_ID>] [--group_id <GROUP_ID>]`

| 参数 | 说明 |
| --- | --- |
| --src\_subsystem\_name <SRC\_SUBSYSTEM\_NAME> | 克隆的源 Namespace 所在的 Subsystem Name。 |
| --src\_ns\_id <SRC\_NS\_ID> | 克隆的源 Namespace 的 NSID |
| --src\_snapshot\_id <SRC\_SNAPSHOT\_ID> | 克隆的源快照的 Volume ID。 |
| --group\_id <GROUP\_ID> | 目标 Namespace 的 Namespace Group ID。均衡策略必须指定。 |

**输出示例**

```
----------------------  ------------------------------------
NS Id                   3
NS Name                 e2f07e5a-1f1b-4821-ae0a-1b9b748ae0f5
Size                    10.00 GiB
Perf Unique Size        In Process
Perf Shared Size        In Process
Cap Unique Size         In Process
Cap Shared Size         In Process
Logical Used Size       In Process
Is Shared               False
Volume id               e2f07e5a-1f1b-4821-ae0a-1b9b748ae0f5
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Encrypt Metadata Id     0
Replica Num             2
EC Param
Thin Provision          True
Group id
Preferred Access        0
Creation Time           2025-07-07 11:20:43.543474145
Description
NQN Whitelist
Single Access           False
Read Only               False
Is Prioritized          False
Downgraded PRS          0.00 B
Chunk Instances
Use Host                True
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 更新 NVMe Namespace

**操作方法**

在集群任一节点执行如下命令，更新 NVMe Namespace 的名称、扩容、提升副本数等：

```
zbs-nvmf ns update <subsystem_name> <ns_id> [--size <SIZE>]
                                            [--new_name <NEW_NAME>]
                                            [--desc <DESC>]
                                            [--replica_num <REPLICA_NUM>]
                                            [--thin_provision {true | false}]
                                            [--group_id <GROUP_ID>]
                                            [--nqn_whitelist <NQN_WHITELIST>]
                                            [--stripe_num <STRIPE_NUM>]
                                            [--stripe_size <STRIPE_SIZE>]
                                            [--skip_all_zero_first_write <SKIP_ALL_ZERO_FIRST_WRITE>]
                                            [--alloc_even <ALLOC_EVEN>]
                                            [--read_only <READ_ONLY>]
                                            [--use_host <USE_HOST>]
                                            [--allowed_host_ids <ALLOWED_HOST_IDS>]
                                            [--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>]
```

| 参数 | 说明 |
| --- | --- |
| `subsystem name` | Namespace 所属的 Subsystem。 |
| `ns_id` | Namespace ID。 |
| `--size <SIZE>` | 调整 Namespace 的大小。新设置容量不能小于原容量，否则报错。此命令用来为 Namespace 扩容。 |
| `--new_name <NEW_NAME>` | 更新Namespace 的名称。 |
| `--desc <DESC>` | Namespace 的描述。 |
| `--replica_num <REPLICA_NUM>` | Namespace 的副本数。只支持提升副本数，不支持降低副本数。 |
| `--thin_provision` | 设置 Namespace 是否为精简置备。 |
| `--group_id <GROUP_ID>` | Namespace 的 NS Group ID。均衡策略必须指定。 |
| `--nqn_whitelist <nqn_whitelist>` | Namespace 的 NQN 白名单，多个 NQN 之间用英文逗号 `,` 隔开，例如：`nqn.1994-05.com.smartx:aaaa,nqn.1994-05.com.smartx:bbbb`。 |
| `--stripe_num <STRIPE_NUM>` | Namespace 的条带数。 |
| `--stripe_size <STRIPE_SIZE>` | Namespace 的条带大小。 |
| `--skip_all_zero_first_write <SKIP_ALL_ZERO_FIRST_WRITE>` | `True` 或 `False`，默认为 `None`。 |
| `--alloc_even <ALLOC_EVEN>` | `True` 或 `False`，默认为 `None`。 |
| `--read_only <READ_ONLY>` | `True` 或 `False`，默认为 `None`。 |
| `--use_host <USE_HOST>` | 更新是否使用业务主机指定白名单。use\_host 为 `true` 时，不允许设置 `nqn_whitelist` 参数；为 `false` 时，不允许设置 `allowed_host_ids` 和 `allowed_host_group_ids` 参数。 |
| `--allowed_host_ids <ALLOWED_HOST_IDS>` | 更新关联的业务主机的 ID，以英文逗号（,）分隔多个 ID。 |
| `--allowed_host_group_ids <ALLOWED_HOST_GROUP_IDS>` | 更新关联的业务主机组的 ID，以英文逗号（,）分隔多个 ID。 |

**输出示例**

```
----------------------  ------------------------------------
NS Id                   3
NS Name                 e2f07e5a-1f1b-4821-ae0a-1b9b748ae0f5
Size                    10.00 GiB
Perf Unique Size        In Process
Perf Shared Size        In Process
Cap Unique Size         In Process
Cap Shared Size         In Process
Logical Used Size       In Process
Is Shared               False
Volume id               e2f07e5a-1f1b-4821-ae0a-1b9b748ae0f5
Resiliency Type         RT_REPLICA
Encrypt Method          ENCRYPT_PLAIN_TEXT
Encrypt Metadata Id     0
Replica Num             2
EC Param
Thin Provision          True
Group id
Preferred Access        0
Creation Time           2025-07-07 11:20:43.543474145
Description
NQN Whitelist
Single Access           False
Read Only               False
Is Prioritized          False
Downgraded PRS          0.00 B
Chunk Instances
Use Host                True
Allowed Host Ids
Allowed Host Group Ids
----------------------  ------------------------------------
```

## 删除 NVMe Namespace

**操作方法**

在集群任一节点执行如下命令，删除 NVMe Namespace：

`zbs-nvmf ns delete <subsystem_name> <ns_id>`

**输出示例**

执行成功无输出。

## 查看指定 Namespace 的可接入 Host NQN

**操作方法**

在集群任一节点执行如下命令：

`zbs-nvmf ns get_access <subsystem_name> <ns_id>`

**输出示例**

```
Host NQN                                                                CID
--------------------------------------------------------------------  -----
nqn.2014-08.org.nvmexpress:uuid:82729b6b-4541-41a9-a75b-7bced1d407bd      2
```

## 设置指定 Namespace 的可接入 Host NQN

**操作方法**

在集群任一节点执行如下命令：

`zbs-nvmf ns set_access <subsystem_name> <ns_id> <host_nqns>`

| 参数 | 说明 |
| --- | --- |
| `subsystem name` | Namespace 所属的 Subsystem。 |
| `ns_id` | Namespace ID。 |
| `host_nqns` | 设置可访问 Namespace 的 NQN。多个 NQN 之间用英文逗号 `,` 隔开，例如：`nqn.1994-05.com.smartx:aaaa,nqn.1994-05.com.smartx:bbbb`。 |

**输出示例**

```
Host NQN                                                                CID
--------------------------------------------------------------------  -----
nqn.2014-08.org.nvmexpress:uuid:82729b6b-4541-41a9-a75b-7bced1d407bd      2
```

---

## 块存储集群 CLI 命令 > 管理 NVMe-oF 存储服务 > 管理 NVMe Namespace 快照

# 管理 NVMe Namespace 快照

## 查看 NVMe Subsystem 包含的快照

**操作方法**

在集群任一节点执行如下命令：

`zbs-nvmf snapshot list <subsystem_name> [--ns_id <ns_id>]`

**输出示例**

```
ID                                    Snap Name    Size         Perf Unique Size    Perf Shared Size    Cap Unique Size    Cap Shared Size    Logical Used Size    Diff Size    Volume Id                             Creation Time                  Description
------------------------------------  -----------  -----------  ------------------  ------------------  -----------------  -----------------  -------------------  -----------  ------------------------------------  -----------------------------  -------------
3cf8e5a2-20dc-4c24-980f-4a4209edfa5d  sp1          1024.00 GiB  In Process          In Process          In Process         In Process         In Process           0.00 B       76e29d47-9b92-4de8-8afa-692c2ed4a73d  2024-06-18 15:28:30.611635897
b679b1d0-7c0e-4921-9bd2-2c06a8bd1ddf  sp2          1024.00 GiB  In Process          In Process          In Process         In Process         In Process           0.00 B       76e29d47-9b92-4de8-8afa-692c2ed4a73d  2024-06-18 15:29:04.182468750
```

## 查看 NVMe Namespace 快照

**操作方法**

- 查看指定名称的快照：

  `zbs-nvmf snapshot show <subsystem_name> <ns_id> <snapshot_name>`
- 查看指定 ID 的快照：

  `zbs-nvmf snapshot show_by_id <snapshot_id>`

**输出示例**

```
-----------------  ------------------------------------
ID                 3cf8e5a2-20dc-4c24-980f-4a4209edfa5d
Snap Name          sp1
Size               1024.00 GiB
Perf Unique Size   0.00 B
Perf Shared Size   0.00 B
Cap Unique Size    0.00 B
Cap Shared Size    0.00 B
Logical Used Size  0.00 B
Diff Size          0.00 B
Volume Id          76e29d47-9b92-4de8-8afa-692c2ed4a73d
Creation Time      2024-06-18 15:28:30.611635897
Description
-----------------  ------------------------------------
```

## 创建 NVMe Namespace 快照

**操作方法**

在集群任一节点执行如下命令：

`zbs-nvmf snapshot create <subsystem_name> <ns_id> <name> [--desc <desc>]`

**输出示例**

```
-----------------  ------------------------------------
ID                 3cf8e5a2-20dc-4c24-980f-4a4209edfa5d
Snap Name          sp1
Size               1024.00 GiB
Perf Unique Size   In Process
Perf Shared Size   In Process
Cap Unique Size    In Process
Cap Shared Size    In Process
Logical Used Size  In Process
Diff Size          0.00 B
Volume Id          76e29d47-9b92-4de8-8afa-692c2ed4a73d
Creation Time      2024-06-18 15:28:30.611635897
Description
-----------------  ------------------------------------
```

## 更新 NVMe Namespace 快照

**操作方法**

在集群任一节点执行如下命令，更新 NVMe Namespace 快照信息：

- 更新指定名称的快照：

  `zbs-nvmf snapshot update <subsystem_name> <ns_id> <snapshot_name> [--new_name <NEW_NAME>][--new_desc <NEW_DESC>][--new_alloc_even {true | false}]`
- 更新指定 ID 的快照：

  `zbs-nvmf snapshot update_by_id <snapshot_id> [--new_name <NEW_NAME>][--new_desc <NEW_DESC>][--new_alloc_even {true | false}]`

| 参数 | 说明 |
| --- | --- |
| `--new_name <NEW_NAME>` | 更新快照名称。 |
| `--new_desc <NEW_DESC>` | 更新快照描述。 |
| `--new_alloc_even` | 设置数据是否需要均匀分布。 |

**输出示例**

```
-----------------  ------------------------------------
ID                 3cf8e5a2-20dc-4c24-980f-4a4209edfa5d
Snap Name          ss1
Size               1024.00 GiB
Perf Unique Size   In Process
Perf Shared Size   In Process
Cap Unique Size    In Process
Cap Shared Size    In Process
Logical Used Size  In Process
Diff Size          0.00 B
Volume Id          76e29d47-9b92-4de8-8afa-692c2ed4a73d
Creation Time      2024-06-18 15:28:30.611635897
Description
-----------------  ------------------------------------
```

## 从 NVMe Namespace 快照回滚

**操作方法**

在集群任一节点执行如下命令，将 Namespace 从指定快照回滚：

- 从指定名称的快照回滚：

  `zbs-nvmf snapshot rollback <subsystem_name> <ns_id> <snapshot_name>`
- 从指定 ID 的快照回滚：

  `zbs-nvmf snapshot rollback_by_id <subsystem_name> <ns_id> <snapshot_id>`

**输出示例**

执行成功无输出。

## 删除 NVMe Namespace 快照

**操作方法**

- 删除指定名称的快照：

  `zbs-nvmf snapshot delete <subsystem_name> <ns_id> <snapshot_name>`
- 删除指定 ID 的快照：

  `zbs-nvmf snapshot delete_by_id <snapshot_id>`

**输出示例**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 采集集群的性能数据

# 采集集群的性能数据

SMTX ZBS 提供了全路径 I/O 性能分析工具 `zbs-perf-tools` ，可采集集群的性能数据，帮助工程师感知集群的整体负载情况和延时分布，从而定位出偶发的性能延时出现的原因，同时帮助工程师判断集群的网络或者物理盘是否存在问题，指明问题的排查方向。

---

## 块存储集群 CLI 命令 > 采集集群的性能数据 > 实时采集并分析整个集群的 I/O 性能数据

# 实时采集并分析整个集群的 I/O 性能数据

**操作方法**

在集群任一节点执行如下命令，将会创建一个 Live Session，同时开始采集 chunk 服务数据并且实时输出结果到控制台，支持如下两种输出格式：

- text：直接输出解析后的 trace 日志。
- io\_pattern ：按秒统计每个 I/O Size 的 I/O 累计数量，并且输出 Top 20 的值。

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

## 块存储集群 CLI 命令 > 采集集群的性能数据 > 查看 Volume 性能

# 查看 Volume 性能

## 查看所有 Volume 的性能信息

**操作方法**

在集群节点执行如下命令，查看所有 Volume 的性能信息（iops，request size，bps，lat 等）：

`zbs-perf-tools volume list [--chunk-addr <ip>] [--sort_by <sort_by>] [-A]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd rpc server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 Chunk。 |
| `--sort_by <sort_by>` | 按照该字段对所有 Volume 性能信息进行降序或升序排列，仅可指定 iops/bw/latency 类字段，默认为 total\_iops |
| `-A, --ascending` | 按照 sort\_by 字段升序排列所有 volume 的性能信息，不指定默认降序排列 |

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
| `splited_read_iops` | 最近 1s 内拆分后的读 IOPS。当条带大小为 256 KiB 时，512 KiB 的读请求会被拆分成两个 256 KiB 大小的请求下发给 Access。 |
| `splited_read_latency` | 最近 1s 内拆分后的读请求平均延时。 |
| `splited_local_read_ratio` | 最近 1s 内拆分后的读请求下发给本地 Access 的 IOPS 比例。 |
| `splited_local_read_bw` | 最近 1s 内拆分后的下发给本地 Access 的读带宽。 |
| `splited_local_read_latency` | 最近 1s 内拆分后的读请求下发给本地 Access 的平均延时。 |
| `write_iops` | 最近 1s 内写 IOPS。 |
| `write_avgrq` | 最近 1s 内写请求平均大小。 |
| `write_bw` | 最近 1s 内写带宽。 |
| `write_latency` | 最近 1s 内写请求平均延时。 |
| `splited_write_iops` | 最近 1s 内拆分后的读 IOPS。当条带大小为 256 KiB 时，512 KiB 的写请求会被拆分成两个 256 KiB 大小的请求下发给 Access。 |
| `splited_write_latency` | 最近 1s 内拆分后的写请求平均延时。 |
| `splited_local_write_ratio` | 最近 1s 内拆分后的写请求下发给本地 Access 的 IOPS 比例。 |
| `splited_local_write_bw` | 最近 1s 内拆分后的下发给本地 Access 的写带宽。 |
| `splited_local_write_latency` | 最近 1s 内拆分后的写请求下发给本地 Access 的平均延时。 |
| `total_iops` | 最近 1s 内 IOPS。 |
| `total_avgrq` | 最近 1s 内请求平均大小。 |
| `total_bw` | 最近 1s 内带宽。 |
| `total_latency` | 最近 1s 内平均延时。 |
| `total_iop30s` | 最近 30s 内 I/O 次数。 |
| `unmap_iops` | 最近 1s 内 UNMAP 指令 I/O 次数。 |
| `unmap_total` | UNMAP 指令的总 I/O 次数。 |
| `unmap_unaligned_iops` | 最近 1s 内非对齐 UNMAP 指令 I/O 次数。 |
| `unmap_unaligned_total` | 非对齐 UNMAP 指令的总 I/O 次数。 |

## 查看指定 ID 的 Volume 的性能信息

**操作方法**

在集群节点执行如下命令，查看指定 ID 的 Volume 的性能信息（iops，request size，bps，lat 等）：

`zbs-perf-tools volume show <volume id> [--chunk-addr <ip>] [-L] [-A]`

| 参数 | 说明 |
| --- | --- |
| `volume id` | Volume ID。 |
| `--chunk-addr <ip>` | zbs-chunkd rpc server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 Chunk。 |
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
Chunk-Specific Data:
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

`Chunk-Specific Data` 为 chunk 级别数据，表示从集群中的所有 chunk 服务采集到的数据。

`Aggregated Data` 为聚合数据，表示从整个集群的全部 chunk 服务采集到的性能数据的综合结果，其中延时值和平均值是取加权平均值，计数值是取总和。

| 参数 | 说明 |
| --- | --- |
| `read_iops` | 最近 1s 内读 IOPS。 |
| `read_avgrq` | 最近 1s 内读请求平均大小。 |
| `read_bw` | 最近 1s 内读带宽。 |
| `read_latency` | 最近 1s 内读请求平均延时。 |
| `splited_read_iops` | 最近 1s 内拆分后的读 IOPS。当条带大小为 256 KiB 时，512 KiB 的读请求会被拆分成两个 256 KiB 大小的请求下发给 Access。 |
| `splited_read_latency` | 最近 1s 内拆分后的读请求平均延时。 |
| `splited_local_read_ratio` | 最近 1s 内拆分后的读请求下发给本地 Access 的 IOPS 比例。 |
| `splited_local_read_bw` | 最近 1s 内拆分后的下发给本地 Access 的读带宽。 |
| `splited_local_read_latency` | 最近 1s 内拆分后的读请求下发给本地 Access 的平均延时。 |
| `write_iops` | 最近 1s 内写 IOPS。 |
| `write_avgrq` | 最近 1s 内写请求平均大小。 |
| `write_bw` | 最近 1s 内写带宽。 |
| `write_latency` | 最近 1s 内写请求平均延时。 |
| `splited_write_iops` | 最近 1s 内拆分后的读 IOPS。当条带大小为 256 KiB 时，512 KiB 的写请求会被拆分成两个 256 KiB 大小的请求下发给 Access。 |
| `splited_write_latency` | 最近 1s 内拆分后的写请求平均延时。 |
| `splited_local_write_ratio` | 最近 1s 内拆分后的写请求下发给本地 Access 的 IOPS 比例。 |
| `splited_local_write_bw` | 最近 1s 内拆分后的下发给本地 Access 的写带宽。 |
| `splited_local_write_latency` | 最近 1s 内拆分后的写请求下发给本地 Access 的平均延时。 |
| `total_iops` | 最近 1s 内 IOPS。 |
| `total_avgrq` | 最近 1s 内请求平均大小。 |
| `total_bw` | 最近 1s 内带宽。 |
| `total_latency` | 最近 1s 内平均延时。 |
| `total_iop30s` | 最近 30s 内 I/O 次数。 |
| `unmap_iops` | 最近 1s 内 UNMAP 指令 I/O 次数。 |
| `unmap_total` | UNMAP 指令的总 I/O 次数。 |
| `unmap_unaligned_iops` | 最近 1s 内非对齐 UNMAP 指令 I/O 次数。 |
| `unmap_unaligned_total` | 非对齐 UNMAP 指令的总 I/O 次数。 |

## 探测 Volume 的 I/O 延时分布、IO 请求大小分布和区域访问热度

通过设置 Volume 的探测模式，可周期性探测 Volume 的 I/O 延时分布，IO 请求大小分布和区域访问热度，并以直方图的方式呈现。

**操作方法**

在集群节点执行如下命令，开启指定的探测模式。按下 `ctrl + c` 可退出探测模式，命令退出后将自动清理 zbs-chunkd 探测模式相关的 metrics。

`zbs-perf-tools volume probe <volume id> [--chunk-addr <ip>] [--meta-addr <ip>] [--distribution {lat | rqsz | logical_offset}] [--interval <int>] [--readwrite {read | write | readwrite}]`

| 参数 | 说明 |
| --- | --- |
| `volume id` | ZBS 卷 ID。 |
| `--chunk-addr <ip>` | zbs-chunkd rpc server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 Chunk。 |
| `--meta-addr <ip>` | zbs-meta rpc server 地址。可选参数，默认值为 ”127.0.0.1:10206”。 |
| `--distribution` | I/O 分布类型，默认为 `lat`。`lat`：IO 延时分布；`rqsz`：IO 请求大小分布；`logical_offset`：逻辑区域访问热力分布。 |
| `--interval <int>` | 探测周期，即获取最近一段时内的分布信息。单位为秒，默认为 1 秒。 |
| `--readwrite` | 探测指定 I/O 类型的分布，可取 `read`, `write`,`readwrite`，默认为 `readwrite`。 |

**输出示例**

如果实际某个分布区间没有值，输出时会略过空的区间，比如延时都集中在 [0,64.00 us] 这个区间，而其他区间都是空的，则只输出 [0,64.00us] 区间。

- **探测 Volume 的读写请求的延时分布**

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
- **探测 Volume 的 I/O 读写请求的大小分布**

  输出结果中，直方图第一列是 I/O 请求大小区间（单位为 KB），第二列为对应区间的计数，第三列为区间的分布情况。

  ```
  $zbs-perf-tools volume probe e5a1d376-7d14-4c44-82b4-f2bc2a2334ee --distribution rqsz
        readwrite size(KB)        : count     distribution
            [4.00,8.00)           : 71       |********************************|
            [16.00,32.00)         : 58       |***************************     |
            [256.00,512.00)       : 3        |**                              |
  ```
- **探测 Volume I/O 读写的区域热力分布**

  输出结果中，直方图第一列是 I/O 请求读写的区间（每 1 GB 为一个区间），第二列为对应区间的计数，第三列为区间的分布情况。

  ```
  $zbs-perf-tools volume probe e5a1d376-7d14-4c44-82b4-f2bc2a2334ee --distribution logical_offset
     readwrite logical offset(GB)    : count     distribution
             [0,1.00)                : 29248    |********************************|
            [1.00,2.00)              : 16579    |*******************             |
            [2.00,3.00)              : 16763    |*******************             |
            [3.00,4.00)              : 16320    |******************              |
  ```

## 采集并分析指定 Volume 的 I/O 性能数据

**操作方法**

在集群任一节点执行如下命令，创建一个以 Volume ID 命名的 Session，同时开始采集数据。

`zbs-perf-tools trace volume <volume_id> --trace_time <time>`

| 参数 | 说明 |
| --- | --- |
| `volume_id` | 目标 Volume 的 ID。 |
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

## 块存储集群 CLI 命令 > 采集集群的性能数据 > 查看 UIO/Access 统计信息

# 查看 UIO/Access 统计信息

UIO（User I/O）是用户侧发过来的 I/O。zbs\_client 负责将用户发过来的 I/O 请求转化成 ZBS 内部的 I/O 请求，并发往 I/O 请求对应的 extent 的 lease owner。用户可使用命令行查看 UIO 的统计信息。

**操作方法**

执行如下命令，查看节点的 UIO 统计信息：

`zbs-perf-tools chunk uio summary [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd rpc server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 Chunk。 |

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
| `total_iops` | 最近 1s 内 zbs\_client 模块中读写 IOPS。 |
| `total_bw` | 最近 1s 内 zbs\_client 模块的读写带宽。 |
| `total_latency` | 最近 1s 内 zbs\_client 模块的读写平均延时。 |
| `read_iops` | 最近 1s 内 zbs\_client 模块中读 IOPS。 |
| `read_bw` | 最近 1s 内 zbs\_client 模块的读带宽。 |
| `read_latency` | 最近 1s 内 zbs\_client 模块的读平均延时。 |
| `write_iops` | 最近 1s 内 zbs\_client 模块中写 IOPS。 |
| `write_bw` | 最近 1s 内 zbs\_client 模块的写带宽。 |
| `write_latency` | 最近 1s 内 zbs\_client 模块的读平均延时。 |
| `local_io_ratio` | 最近 1s 内发往本地 Access 的 I/O 比例。 |
| `local_io_latency` | 最近 1s 内发往本地 Access 的 I/O 平均延时。 |
| `local_io_bw` | 最近 1s 内发往本地 Access 的 I/O 带宽。 |
| `local_read_ratio` | 最近 1s 内发往本地 Access 的读 I/O 比例。 |
| `local_read_latency` | 最近 1s 内发往本地 Access 的读 IO平均延时。 |
| `local_read_bw` | 最近 1s 内发往本地 Access 的读 IO带宽。 |
| `local_write_ratio` | 最近 1s 内发往本地 Access 的写 I/O 比例。 |
| `local_write_latency` | 最近 1s 内发往本地 Access 的写 IO平均延时。 |
| `local_write_bw` | 最近 1s 内发往本地 Access 的写 IO带宽。 |
| `failed_io_ratio` | 最近 1s 内失败的 I/O 比例。 |
| `retry_io_ratio` | 最近 1s 内重试 I/O 的比例。 |
| `retry_queue_size` | 当前重试队列大小。 |
| `active_extents` | 当前活跃的 extent 数量。 |
| `active_volumes` | 当前活跃的 volume 数量。 |
| `waiting_queue_size` | 当前等待队列大小。 |

> **说明**：
>
> 多物理盘池环境下，会展示每一个 chunk 的性能数据，若想查看整体性能数据可以执行 `zbs-perf-tools node uio summary`。

## 查看 Access 模块的总体性能信息

**操作方法**

执行如下命令，查看 Access 模块的总体性能信息：

`zbs-perf-tools chunk access summary [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd rpc server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 Chunk。 |

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
| `read_iops` | 最近 1s 内 Access 模块中读 IOPS。 |
| `read_latency` | 最近 1s 内 Access 模块的读平均延时。 |
| `read_bw` | 最近 1s 内 Access 模块的读带宽。 |
| `write_iops` | 最近 1s 内 Access 模块中写 IOPS。 |
| `write_latency` | 最近 1s 内 Access 模块的写平均延时。 |
| `write_bw` | 最近 1s 内 Access 模块的写带宽。 |
| `total_iops` | 最近 1s 内 Access 模块中读写 IOPS。 |
| `total_latency` | 最近 1s 内 Access 模块的读写平均延时。 |
| `total_bw` | 最近 1s 内 Access 模块的读写带宽。 |
| `io_hard_rate` | 最近 1s 内 Access 标记为 hard 的 I/O 次数，hard I/O 一般是由于 LSM 中有慢盘。 |
| `io_retry_rate` | 最近 1s 内 Access 读重试次数。Access 读副本失败时会尝试读取下一个副本。 |
| `io_timeout_rate` | 最近 1s 内发往本地 Access I/O 超时次数。 |
| `from_local_read_iops` | 最近 1s Access 处理本地发来的读 IOPS。 |
| `from_local_read_latency` | 最近 1s Access 处理本地发来的读平均延时。 |
| `from_local_read_bw` | 最近 1s Access 处理本地发来的读带宽。 |
| `from_local_write_iops` | 最近 1s Access 处理本地发来的写 IOPS。 |
| `from_local_write_latency` | 最近 1s Access 处理本地发来的写平均延时。 |
| `from_local_write_bw` | 最近 1s Access 处理本地发来的写带宽。 |
| `from_local_total_iops` | 最近 1s Access 处理本地发来的读写 IOPS。 |
| `from_local_total_latency` | 最近 1s Access 处理本地发来的读写平均延时。 |
| `from_local_total_bw` | 最近 1s Access 处理本地发来的读写带宽。 |
| `from_local_throttle_latency` | 最近 1s 内 Access 处理本地发来的被限流的 I/O 的平均延时。 |
| `from_remote_read_iops` | 最近 1s Access 处理其他 Access 发来的读 IOPS。 |
| `from_remote_read_latency` | 最近 1s Access 处理其他 Access 发来的读平均延时。 |
| `from_remote_read_bw` | 最近 1s Access 处理其他 Access 发来的读带宽。 |
| `from_remote_write_iops` | 最近 1s Access 处理其他 Access 发来的写 IOPS。 |
| `from_remote_write_latency` | 最近 1s Access 处理其他 Access 发来的写平均延时。 |
| `from_remote_write_bw` | 最近 1s Access 处理其他 Access 发来的写带宽。 |
| `from_remote_total_iops` | 最近 1s Access 处理其他 Access 发来的读写 IOPS。 |
| `from_remote_total_latency` | 最近 1s Access 处理其他 Access 发来的读写平均延时。 |
| `from_remote_total_bw` | 最近 1s Access 处理其他 Access 发来的读写带宽。 |
| `from_remote_throttle_latency` | 最近 1s 内 Access 处理其他 Access 发来的被限流的 I/O 的平均延时。 |

> **说明**：
>
> 多物理盘池环境下，会展示每一个 chunk 的性能数据，若想查看整体性能数据可以执行 `zbs-perf-tools node access summary`。

## 查看当前 Access 模块的副本 I/O 流向和基本统计信息

**操作方法**

执行如下命令，查看当前 Access 的副本 I/O 流向和基本统计信息：

`zbs-perf-tools chunk access replica_io [--chunk-addr <ip>] [-d]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd rpc server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 Chunk。 |
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
| `TOTAL IOPS` | 最近 1s 内读写 IOPS。 |
| `TOTAL LATENCY` | 最近 1s 内读写平均延时。 |
| `TOTAL BW` | 最近 1s 内读写带宽。 |

---

## 块存储集群 CLI 命令 > 采集集群的性能数据 > 查看 LSM2 模块性能

# 查看 LSM2 模块性能

LSM2 管理磁盘和 Extent 等元数据，元数据存储在 LSM2 DB 中。LSM2 负责将 Access 发来的副本 I/O 落盘。在 LSM2 中，SSD 通常用作 Cache 盘和 Journal 盘，HDD 用做 Partition 盘（全闪情况下，Partition 全为 SSD，没有 Cache 盘），一次写请求需要将元数据的更新和数据写入 Journal 盘 (部分情况不需要将数据写入 journal) , 然后写入到 Cache 或者 Partition 盘中，即是说一次 I/O 请求可能涉及到 LSM2 DB，Journal，Cache，Partition。

此部分命令行从 LSM2 获取 LSM2 的整体数据，以及 LSM2 DB，Journal，Cache，Partition 等分区的性能数据并展示。

## 查看 LSM 模块的总体性能信息

**操作方法**

执行如下命令，查看 LSM 的总体性能信息：

`zbs-perf-tools chunk lsm summary [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd rpc server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 Chunk。 |

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
| `total_iops` | 最近 1s 内 LSM 模块中读写 IOPS。 |
| `total_bw` | 最近 1s 内 LSM 模块的读写带宽。 |
| `total_latency` | 最近 1s 内 LSM 模块的读写平均延时。 |
| `total_cache_hit` | 最近 1s 内 LSM 模块的读写 cache 命中率。 |
| `read_iops` | 最近 1s 内 LSM 模块中读 IOPS。 |
| `read_bw` | 最近 1s 内 LSM 模块的读带宽。 |
| `read_latency` | 最近 1s 内 LSM 模块的读平均延时。 |
| `read_cache_hit` | 最近 1s 内 LSM 模块的读 cache 命中率。 |
| `write_iops` | 最近 1s 内 LSM 模块中写 IOPS。 |
| `write_bw` | 最近 1s 内 LSM 模块的写带宽。 |
| `write_latency` | 最近 1s 内 LSM 模块的写平均延时。 |
| `write_cache_hit` | 最近 1s 内 LSM 模块的写 cache 命中率。 |
| `failed_io_ratio` | 最近 1s 内 LSM 模块的 I/O 失败率。 |
| `hard_io_ratio` | 最近 1s 内 LSM 模块的 hard I/O 比例。 |
| `slow_io_ratio` | 最近 1s 内 LSM 模块的 slow I/O 比例。 |
| `throttle_latency` | 最近 1s 内 LSM 模块处理 I/O 的 throttle 延时。 |
| `cache_promotion_rate` | 最近 1s 内 LSM 从 partition 写到 cache 的 IOPS。 |
| `cache_promotion_bw` | 最近 1s 内 LSM 从 partition 写到 cache 的带宽。 |
| `cache_writeback_rate` | 最近 1s 内 LSM 从 cache 写回 partition 的 IOPS。 |
| `cache_writeback_bw` | 最近 1s 内 LSM 从 cache 写到 partition 的带宽。 |
| `journal_reclaim_rate` | 最近 1s 内 LSM journal 回收速度。 |
| `journal_reclaim_latency` | 最近 1s 内 LSM journal 回收延时。 |

> **说明**：
>
> 多物理盘池环境下，会展示每一个 chunk 的性能数据，若想查看整体性能数据可以执行 `zbs-perf-tools node lsm summary`。

## 查看 LSM DB 的性能信息

**操作方法**

执行如下命令，查看 LSM DB 的性能信息：

`zbs-perf-tools chunk lsm db [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd rpc server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 Chunk。 |

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
| `OP` | lsm DB 操作。 |
| `RATE` | 最近 1s DB 操作次数。 |
| `LATENCY` | 最近 1s DB 操作平均延时。 |
| `MAX LATENCY` | 最近 30s DB 操作的最大延时。 |

## 查看 LSM Journal 分区的性能信息

**操作方法**

执行如下命令，查看 LSM Journal 分区的性能信息：

`zbs-perf-tools chunk lsm journal [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd rpc server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 Chunk。 |

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

## 查看 LSM Cache 分区的性能信息

**操作方法**

执行如下命令，查看 LSM Cache 分区的性能信息：

`zbs-perf-tools chunk lsm cache [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd rpc server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 Chunk。 |

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
| `PATH` | Cache 分区。 |
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

## 查看 LSM Partition 分区的性能信息

**操作方法**

执行如下命令，查看 LSM Partition 分区的性能信息：

`zbs-perf-tools chunk lsm partition [--chunk-addr <ip>]`

| 参数 | 说明 |
| --- | --- |
| `--chunk-addr <ip>` | zbs-chunkd rpc server 地址。默认值为 `127.0.0.1:10200`，即命令所在节点的 Chunk。 |

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
| `PATH` | Partition 分区。 |
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

## 块存储集群 CLI 命令 > 采集集群的性能数据 > 采集并分析指定 Target 的 I/O 性能数据

# 采集并分析指定 Target 的 I/O 性能数据

## 创建 Session

**操作方法**

在集群任一节点执行如下命令创建指定名称的 Session。执行命令后，在 `/root/zbs-trace/` 目录下会生成以 Session 命名的文件夹。

`zbs-perf-tools trace session create [--session <session_name>]`

| 参数 | 说明 |
| --- | --- |
| `--session <session_name>` | Session 名称。 |

**输出说明**

执行成功无输出。

## 查看已创建的 Session

**操作方法**

在集群任一节点执行如下命令，查看当前已创建的 Session。

`zbs-perf-tools trace session list`

**输出示例**

```
------------------
  name     session1
  started  false
------------------
```

## 将 Target 添加到 Session 中

**操作方法**

在集群任一节点进入 `/root/zbs-trace/<session name>` 目录执行如下命令，将 Target 添加到 Session 中：

`zbs-perf-tools trace session add-target <TARGET NAME> <TARGET HOST> [--event]`

| 参数 | 说明 |
| --- | --- |
| `TARGET NAME` | 目标名称。同一个 Session 中的 Target name 不可重复。 |
| `TARGET HOST` | 目标所在节点的 IP。 |
| `--event` | 数组类型参数，待 trace 的事件名称，目前支持 `zbs_client:*`，`access:*` 和 `lsm2:*`。 |

**输出说明**

执行成功无输出。

## 使用 Json 文件添加多个 Target

采集一个指定卷的数据时，可以通过使用 Json 文件来添加多个 Target。

**操作方法**

在集群任一节点进入 `/root/zbs-trace/<session name>` 目录执行如下命令：

`zbs-perf-tools trace session add-target --from-json <JSON FILE>`

| 参数 | 说明 |
| --- | --- |
| `--from-json` | 表示从 Json 文件添加 Target。 |
| `JSON FILE` | Json 文件名。 |

**输出说明**

执行成功无输出。

## 更新 Session 的 Target

**操作方法**

在集群任一节点进入 `/root/zbs-trace/<session name>` 目录执行如下命令，更新 Session 的 Target：

`zbs-perf-tools trace session update-target <TARGET NAME> [--remove-event <stringArray>] [--add-event <stringArray>]`

| 参数 | 说明 |
| --- | --- |
| `--remove-event <stringArray>` | 数组类型，删除 event。 |
| `--add-event <stringArray>` | 数组类型，增加 event。 |

**输出说明**

执行成功无输出。

## 从 Session 中移除 Target

**操作方法**

在集群任一节点进入 `/root/zbs-trace/<session name>` 目录执行如下命令，从 Session 中移除 Target：

`zbs-perf-tools trace session remove-target <TARGET NAME>`

**输出说明**

执行成功无输出。

## 启动 Session

**操作方法**

在集群任一节点进入 `/root/zbs-trace/<session name>` 目录执行如下命令，启动 Session：

`zbs-perf-tools trace session start [-d]`

若指定 `-d` 该选项，session 将在后台启动。

停止 Session 后，将在 `/root/zbs-trace/<session name>/trace-data/` 目录下生成 Target 的 trace data。

**输出示例**

```
$zbs-perf-tools trace session start
session started...
```

## 销毁 Session 并清理数据

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
| `PATH` | trace 数据目录，需要指定到时间层级。 |
| `OUTPUT DIR` | 输出目录。 |
| `--time_begin` | 从指定时间开始解析。 |
| `--time_end` | 解析到某个时间，需要与 --time\_begin 配合使用。 |
| `--volume` | 指定 zbs-perf-tools volume gentrace [VOLUME ID] 生成的 json 文件。 |
| `--slow_io_latency` | 将超过指定延时的 I/O 输出到 [OUTPUT DIR]/[MODULE].slow\_io 文件。单位 ms，默认为 200ms。 |

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
- **输出 Access 模块的数据分析**

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

在集群任一节点执行如下命令，输出成对的 event（一般为 I/O 的开始和结束的 event，或者连续两个 event）之间的延时分布直方图

`zbs-perf-tools trace analyze latdist <TRACE DATA DIR> <TRACE_BEGIN> <TRACE_END> <TRACE_ID>`

| 参数 | 说明 |
| --- | --- |
| `TRACE DATA DIR` | session start 记录 trace 数据目录。 |
| `TRACE_BEGIN` | 两个成对的 trace event 的第一个 trace event 的名称。 |
| `TRACE_END` | 两个成对的 trace event 的第二个 trace event 的名称。 |
| `TRACE_ID` | 用于关联 TRACE\_BEGIN 和 TRACE\_END 的字段名称。 |

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

## 块存储集群 CLI 命令 > 管理 KMS 和加密 > 管理 KMS 集群

# 管理 KMS 集群

KMS 集群由一个或多个 KMS 服务器组成，这些 KMS 服务器共享数据，在 KMS 集群任意节点注册的 Client 可以访问 KMS 集群的任意节点。

## 查看集群中 KMS 集群信息

**操作方法**

在集群任一节点执行如下命令，查看集群中 KMS 集群的信息：

```
zbs-meta kms list
```

**输出示例**

```
Cluster Id:  f904df96-2dd4-49f2-869a-433f9e8aee95
Auth Id:  9eeba746-147e-410d-baa2-67436215a0df
Cluster Name:  kms-205
Is Rotating Key:  False
Key Rotation Seconds:  31536000
Last Key Rotation Time:  2025-01-10 14:36:42.0
Last Key Backup Time:  2025-01-10 15:10:22.0

ID                                    Host              Port  Status
------------------------------------  --------------  ------  ------------------------
1ae706e7-c622-4410-8e7a-ebf89b22a34f  172.20.146.205    5696  KMIP_SERVER_DISCONNECTED
c40e8457-8524-49af-a1fe-7f2ce997f1bd  1.1.1.1           5696  KMIP_SERVER_DISCONNECTED
ffe4dfcd-8c07-41b3-b455-4eff6e9777ac  172.20.201.196    5696  KMIP_SERVER_CONNECTED
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Cluster Id` | KMS 集群 ID |
| `Auth Id` | KMS 集群的证书 ID。 |
| `Cluster Name` | KMS 集群名。 |
| `Is Rotating Key` | 集群是否正在轮换密钥。 |
| `Key Rotation Seconds` | 集群自动轮换密钥间隔。 |
| `Last Key Rotation Time` | 上一次密钥轮换时间。 |
| `Last Key Backup Time` | 上一次密钥备份时间。 |
| `ID` | 密钥服务器的 ID。 |
| `Host` | 密钥服务器的 IP 或域名。 |
| `Port` | 密钥服务器的端口。 |
| `Status` | 密钥服务器的状态。 |

## 创建 KMS 集群

**操作方法**

在集群任一节点执行如下命令，创建 KMS 集群，一个 SMTX ZBS集群只支持一套 KMS 集群：

```
zbs-meta kms create_cluster <cluster_name> <--servers SERVERS>
                        <--certificate CERTIFICATE> <--private_key PRIVATE_KEY>
                        [--vendor VENDOR]
                        [--key_rotate_period_seconds KEY_ROTATE_PERIOD_SECONDS]
```

| 参数 | 说明 |
| --- | --- |
| `cluster_name` | KMS 集群名称。 |
| `--servers <SERVERS>` | KMS 服务器信息，格式为 host  ，支持传入多个，用 `,` 隔开。 |
| `--certificate <CERTIFICATE>` | 访问 KMS 需要的证书路径。 |
| `--private_key <PRIVATE_KEY>` | 访问 KMS 需要的私钥路径。 |
| `--vendor <VENDOR>` | KMS 提供商，默认为 `None`。 |
| `--key_rotate_period_seconds <KEY_ROTATE_PERIOD_SECONDS>` | SMTX ZBS集群自动轮换密钥的周期，取值为[86400, 31536000]，单位为 second。 |

**输出示例**

```
Cluster Id:  c3ad0d67-6fe7-436d-802f-112705ab6364
Auth Id:  fefece5f-04bb-43fd-8201-58a346c3fe2d
Cluster Name:  test_cluster
Is Rotating Key:  False
Key Rotation Seconds:  31536000
Last Key Rotation Time:  2025-01-10 19:49:11.0

ID                                    Host              Port  Status
------------------------------------  --------------  ------  ------------------------
1ae706e7-c622-4410-8e7a-ebf89b22a34f  172.20.146.205    5696  KMIP_SERVER_DISCONNECTED
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Cluster Id` | KMS 集群 ID |
| `Auth Id` | KMS 集群的证书 ID。 |
| `Cluster Name` | KMS 集群名。 |
| `Is Rotating Key` | 集群是否正在轮换密钥。 |
| `Key Rotation Seconds` | 集群自动轮换密钥间隔。 |
| `Last Key Rotation Time` | 上一次密钥轮换时间。 |
| `ID` | 密钥服务器的 ID。 |
| `Host` | 密钥服务器的 IP 或域名。 |
| `Port` | 密钥服务器的端口。 |
| `Status` | 密钥服务器的状态。 |

## 更新 KMS 集群配置

**操作方法**

在集群任一节点执行如下命令，更新 KMS 集群配置：

```
zbs-meta kms refresh_cluster cluster_id
                                    --servers SERVERS  --certificate CERTIFICATE
                                    --private_key PRIVATE_KEY
                                    [--cluster_name CLUSTER_NAME] [--vendor VENDOR]
```

| 参数 | 说明 |
| --- | --- |
| `cluster_id` | 需要更换的 KMS 集群 ID。 |
| `--servers <SERVERS>` | KMS 服务器信息，格式为 host  ，支持传入多个，用 `,` 隔开。 |
| `--certificate <CERTIFICATE>` | 访问 KMS 需要的证书路径。 |
| `--private_key <PRIVATE_KEY>` | 访问 KMS 需要的私钥路径。 |
| `--vendor <VENDOR>` | KMS 提供商，默认为 `None`。 |
| `--cluster_name <CLUSTER_NAME>` | 需要更换的 KMS 集群名，默认为不更新。 |

**输出示例**

```
Cluster Id:  f904df96-2dd4-49f2-869a-433f9e8aee95
Auth Id:  9eeba746-147e-410d-baa2-67436215a0df
Cluster Name:  kms-205
Is Rotating Key:  False
Key Rotation Seconds:  31536000
Last Key Rotation Time:  2025-01-10 14:36:42.0
Last Key Backup Time:  2025-01-10 15:10:22.0

ID                                    Host              Port  Status
------------------------------------  --------------  ------  ------------------------
1ae706e7-c622-4410-8e7a-ebf89b22a34f  172.20.146.205    5696  KMIP_SERVER_DISCONNECTED
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Cluster Id` | KMS 集群 ID |
| `Auth Id` | KMS 集群的证书 ID。 |
| `Cluster Name` | KMS 集群名。 |
| `Is Rotating Key` | 集群是否正在轮换密钥。 |
| `Key Rotation Seconds` | 集群自动轮换密钥间隔。 |
| `Last Key Rotation Time` | 上一次密钥轮换时间。 |
| `Last Key Backup Time` | 上一次密钥备份时间。 |
| `ID` | 密钥服务器的 ID。 |
| `Host` | 密钥服务器的 IP 或域名。 |
| `Port` | 密钥服务器的端口。 |
| `Status` | 密钥服务器的状态。 |

## 更新 KMS 集群信息

**操作方法**

在集群任一节点执行如下命令，更新 KMS 集群的信息：

```
zbs-meta kms update_cluster  [--key_rotate_period_seconds KEY_ROTATE_PERIOD_SECONDS] [--cluster_name CLUSTER_NAME]
                                   <cluster_id>
```

| 参数 | 说明 |
| --- | --- |
| `cluster_id` | 需要更新的 KMS 集群的 ID。 |
| `--cluster_name <CLUSTER_NAME>` | KMS 集群名。 |
| `--key_rotate_period_seconds <KEY_ROTATE_PERIOD_SECONDS>` | 更新 SMTX ZBS集群自动轮换密钥的周期，取值为[86400, 31536000]，单位为 second。 |

**输出说明**

执行成功无输出。

## 删除 KMS 集群

**操作方法**

在集群任一节点执行如下命令，删除集群中的 KMS 集群，不存在加密资源（虚拟卷、虚拟机模板的卷、快照、iSCSI target、LUN 等）时才允许删除：

```
zbs-meta kms delete_cluster <cluster_id>
```

| 参数 | 说明 |
| --- | --- |
| `cluster_id` | KMS 集群 ID。 |

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理 KMS 和加密 > 管理 KMS 服务器

# 管理 KMS 服务器

允许对 KMS 集群内的 KMS 服务器进行管理。

## 添加 KMS 服务器

**操作方法**

在集群任一节点执行如下命令，为 KMS 集群添加 KMS 服务器：

```
zbs-meta kms add_server <cluster_id> <--server_host SERVER_HOST> <--server_port SERVER_PORT>
```

| 参数 | 说明 |
| --- | --- |
| `cluster_id` | KMS 集群的 ID。 |
| `--server_host SERVER_HOST` | 添加的 KMS 服务器 IP 或域名。 |
| `--server_port SERVER_PORT` | 添加的 KMS 服务器端口。 |

**输出示例**

```
---------------  ------------------------------------
id               559a383d-e24f-4ba3-b685-bb417174b612
name             192.168.91.222
host             192.168.91.222
port             5696
---------------  ------------------------------------
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `id` | 添加的密钥服务器的 ID。 |
| `name` | 添加的密钥服务器的名字。 |
| `host` | 添加的密钥服务器的 IP 或域名。 |
| `port` | 添加的密钥服务器的端口。 |

## 更新 KMS 服务器

**操作方法**

在集群任一节点执行如下命令，更新 KMS 服务器信息：

```
zbs-meta kms update_server  <cluster_id> <server_id> [--force] [--server_host SERVER_HOST] [--server_port SERVER_PORT]
```

| 参数 | 说明 |
| --- | --- |
| `cluster_id` | 需要更新的 KMS 集群 ID。 |
| `server_id` | 需要更新的 KMS 服务器 ID。 |
| `--force` | 强制更新 KMS 服务器。 |
| `--server_host SERVER_HOST` | 需要更新的 KMS 服务器 IP/域名，默认为 None。 |
| `--server_port SERVER_PORT` | 添加的 KMS 服务器端口，默认为 None。 |

**输出说明**

执行成功无输出。

## 删除 KMS 服务器

**操作方法**

在集群任一节点执行如下命令，删除 SMTX ZBS集群中 KMS 集群的一个 KMS 服务器，不允许删除最后一个 KMS 服务器：

```
zbs-meta kms delete_server <cluster_id> <server_id> [--force]
```

| 参数 | 说明 |
| --- | --- |
| `cluster_id` | KMS 集群 ID。 |
| `server_id` | 需要删除的 KMS 服务器 ID。 |
| `--force` | 强制删除 KMS 服务器。 |

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理 KMS 和加密 > 更新 KMS 集群证书

# 更新 KMS 集群证书

**操作方法**

在集群任一节点执行如下命令，更新 KMS 集群的证书信息：

```
zbs-meta kms update_auth [--force] <--certificate CERTIFICATE> <--private_key PRIVATE_KEY> <cluster_id> <auth_id>
```

| 参数 | 说明 |
| --- | --- |
| `cluster_id` | KMS 集群 ID。 |
| `auth_id` | KMS 证书 ID。 |
| `--force` | 强制更新证书。 |
| `--certificate CERTIFICATE` | 添加的 KMS 证书路径。 |
| `--private_key PRIVATE_KEY` | 添加的 KMS 私钥路径。 |

**输出说明**

执行成功无输出。

---

## 块存储集群 CLI 命令 > 管理 KMS 和加密 > 管理加密

# 管理加密

## 手动轮换主密钥

**操作方法**

在集群任一节点执行如下命令，轮换集群主密钥：

```
zbs-meta kms rotate_key <cluster_id>
```

| 参数 | 说明 |
| --- | --- |
| `cluster_id` | KMS 集群 ID。 |

**输出示例**

执行成功无输出。

## 导出所有卷的加密密钥

**操作方法**

在集群任一节点执行如下命令，导出所有加密卷的加密密钥：

```
zbs-meta kms export_key <--dek_encrypt_password DEK_ENCRYPT_PASSWORD> <--output OUTPUT>
```

| 参数 | 说明 |
| --- | --- |
| `--dek_encrypt_password DEK_ENCRYPT_PASSWORD` | 导出加密卷使用的密码 。 |
| `--output OUTPUT` | 导出密钥的保存文件路径。 |

**输出示例**

执行成功无输出。

## 导入卷的加密密钥

**操作方法**

在集群任一节点执行如下命令，为集群导入密钥：

```
zbs-meta kms import_key <--dek_decrypt_password DEK_DECRYPT_PASSWORD> <--input INPUT>
```

| 参数 | 说明 |
| --- | --- |
| `--dek_decrypt_password DEK_DECRYPT_PASSWORD` | 导入密钥时的密码，与导出这批密钥时所使用的密码一样。 |
| `--input INPUT` | 导入密钥的文件路径。 |

**输出示例**

执行成功无输出。

## 查看 KMS 服务器的状态

**操作方法**

在集群任一节点执行如下命令，查看所有 KMS 服务器的状态，包括 KMS 服务器自身的健康状态和内部 task 的状态：

```
zbs-meta kms list_server <cluster_id> [--show_task]
```

| 参数 | 说明 |
| --- | --- |
| `cluster_id` | KMS 集群 ID。 |
| `--show_task` | 可选参数，是否展示 KMS 服务器的 task 信息。 |

**输出示例**

```
Server:      172.20.201.196:5696
Heart Task:  2025-01-17 14:34:13 40d9686604a74f0284625883faf3bb85af0899a9840744c1af60e857766e2e27 EOK
Create Task:  2025-01-17 14:33:36 40d9686604a74f0284625883faf3bb85af0899a9840744c1af60e857766e2e27 EOK

Server:      1.1.1.1:5696
Get Task:    2025-01-17 14:32:22 dbc518ac702049708a95169bd679c61e6bd0e9a64bd94940ab1f27f83049b09f BIO_do_connect failed. hostname: 1.1.1.1 port: 5696 error string: error:00000000:lib(0):func(0):reason(0)
Heart Task:  2025-01-17 14:34:13 40d9686604a74f0284625883faf3bb85af0899a9840744c1af60e857766e2e27 BIO_do_connect failed. hostname: 1.1.1.1 port: 5696 error string: error:00000000:lib(0):func(0):reason(0)

ID                                    Host              Port  Status
------------------------------------  --------------  ------  ------------------------
77a80934-7de1-40ee-a4c6-e21fdea7fae5  1.1.1.1           5696  KMIP_SERVER_DISCONNECTED
cbed892a-8e56-4b06-915f-a3749825c36d  172.20.201.196    5696  KMIP_SERVER_CONNECTED
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Heart Task` | ZBS Meta 启动后，KMS 服务器上一次心跳 task 的时间，使用的主密钥和状态。 |
| `Create Task` | ZBS Meta 启动后，KMS 服务器上一次创建密钥 task 的时间，创建的主密钥和状态。 |
| `Get Task` | ZBS Meta 启动后，KMS 服务器上一次获取密钥 task 的时间，获取的主密钥和状态。 |
| `ID` | KMS 服务器 ID。 |
| `HOST` | KMS 服务器的 IP 或域名地址。 |
| `Port` | KMS 端口名。 |
| `Status` | KMS 服务器的状态。 |

## 查看集群内的主密钥 ID

**操作方法**

在集群任一节点执行如下命令，查看集群内所有加密卷所使用的主密钥 ID。

```
zbs-meta kms list_master_key_ids
```

**输出示例**

```
Master Key ID Size:  1
ac285a29964244e4bf1c11d73344bc2aab78e0973bff4c3488e8ffae6f7dba76
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| `Master Key ID Size` | 集群内加密卷使用的主密钥 ID 数量。 |

---

## 块存储集群 CLI 命令 > 管理网络 > 更新网络配置

# 更新网络配置

## 更改节点管理网络 IP

**操作方法**

在集群节点执行如下命令，更改当前节点的管理 IP 地址：

`zbs-deploy-manage change-manage-ip <ip> <netmask> <gateway> [--vlan_id <vlan_id>]`

| 参数 | 说明 |
| --- | --- |
| `ip` | 管理网络 IP 地址。 |
| `netmask` | IP 地址子网掩码。 |
| `gateway` | 网关地址。 |
| `--vlan_id <vlan_id>` | 管理网络的 VLAN ID。 |

**输出示例**

输出配置过程

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

## 块存储集群 CLI 命令 > 管理网络 > 管理网卡

# 管理网卡

使用命令行可以查看和修改分布式虚拟交换机 OVS 网桥所关联的物理网口和物理网口绑定模式。

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
| **`--old_port_name <old_port_name>`** | 必须输入的参数。代表更换网卡前，OVS 网桥所关联的物理网口名称或者绑定名称。  - 若 OVS 网桥未关联网口：`<old_port_name>` 为 `None`。 - 若 OVS 网桥关联单个物理网口：`<old_port_name>` 为 OVS 网桥当前所关联的物理网口名称。 - 若 OVS 网桥绑定多个物理网口：通过 `network-tool get-bond-name --ovsbr_name <ovsbr_name>` 命令获取该 OVS 网桥所对应的网口绑定名称，即 bond\_name 参数值。 |
| **`--nics <target_nics>`** | 必须输入的参数，代表 OVS 网桥计划关联的所有网口的名称，例如 `eth0` 或 `"eth0 eth1"` 等。  - 如有多个网口，需要列举出该 OVS 网桥需要关联的所有网口，用空格将多个网口名称隔开，并注意对存在空格的参数使用双引号（`" "`）。例如 `"eth0 eth1"`。 - 此处输入的网口需保证未与其他 OVS 网桥关联。 |
| **`--bond_mode <bonding_mode>`** | 必须输入的参数。指定该 OVS 网桥所关联的虚拟分布式交换机（VDS）使用的绑定模式。  - 若 OVS 网桥只关联了一个网口，则无法设置绑定，请填写 `None`。 - 若 OVS 网桥关联了存储网络或未启用 NVMe over RDMA 的接入网络，则 VDS 使用 OVS Bond 模式，包括 ：   - `active-backup`（OVS Bond）   - `balance-slb`：若存储网络已开启 RDMA，则不支持该绑定模式。   - `balance-tcp`：设置为此模式时，要求对端交换机开启 LACP 动态链路聚合。存储网络使用 Mellanox CX5 网卡且已启用 RDMA 时不建议使用该绑定模式，否则可能导致网络延迟升高。 - 若 OVS 网桥关联了已启用 NVMe over RDMA 的接入网络，则 VDS 使用 Linux Bond 模式，包括 ：   - `active-backup`（Linux Bond）   - `balance-xor`：设置为此模式时，要求对端交换机先配置为手工链路聚合。   - `802.3ad`：设置为此模式时，要求对端交换机先开启 LACP 动态链路聚合。 |
| **`--rb_interval <rb_interval>`** | 可选输入的参数，代表 `balance-slb` 绑定模式下 rebalance 的时间间隔。仅当网口绑定模式为 `balance-slb` 时需要填写，其他模式时此字段及参数 `--rb_interval <rb_interval>` 均不需要填写。 若网口绑定模式为 `balance-slb`：   - 禁用 rebalance：将 `<rb_interval>` 设置为 `0`。 - 使用默认的 rebalance 时间间隔 60 秒：不输入 `--rb_interval <rb_interval>` 字段，或输入 `--rb_interval ""`。 - 自定义 rebalance 的时间间隔：将 `<rb_interval>` 设置为大于 0 的整数。 |
| **`--bond_name <bonding_name>`** | 必须输入的参数。代表 OVS 网桥对应的绑定名称，该绑定名称不能和已存在的绑定名称相同。  - 不同单网口之间互相转换时，请通过 `network-tool get-bond-name --ovsbr_name <ovsbr_name>` 命令获取。 - 从单⽹⼝或 Linux Bond 转换为 OVS Bond 时，`<bonding_name>` 不能取 `bond0`、 `bond1` 和 `bond2`。 - 从单⽹⼝或 OVS Bond 转换为 Linux Bond 时，`<bonding_name>` 取固定值，接⼊⽹络为 `bond0`，管理⽹络为 `bond1`，存储⽹络为 `bond2`。 - 从 OVS Bond 转换为单⽹⼝时，不允许改变绑定名称，与 `old_port_name` 保持一致。 - 不同 OVS Bond 之间互相转换时，不允许改变绑定名称，与 `old_port_name` 保持一致。 - 从 Linux Bond 转换为单⽹⼝时，`<bonding_name>` 设置为 `None`。 - Linux Bond 转换为 OVS Bond 时，转换后 OVS 网桥对应的绑定名称为新的名称。 |

**使用示例**

对原始名称为 ovsbr-mgt 的 OVS 网桥进行参数设置。将单网口 （eth0） 变更为双网口（eth0 和 eth1），该 OVS 网桥所关联的 VDS 使用的绑定模式为 OVS Bond 中的 balance-slb 模式，rebalance 时间间隔为 80 秒， OVS 网桥对应的新的绑定名称为 bond-mgt。

`network-tool change-bridge --ovsbr_name ovsbr-mgt --old_port_name eth0 --nics "eth0 eth1" --bond_mode balance-slb --rb_interval 80 --bond_name bond-mgt`

如果存储网络开启了 RDMA，对原始名称为 ovsbr-stor 的 OVS 网桥进行参数设置。将 Linux Bond 802.3ad 模式变更为 OVS Bond balance-tcp 模式（eth0 和 eth1）， OVS 网桥对应的新的绑定名称为 bond-storage。

`network-tool change-bridge --ovsbr_name ovsbr-stor --old_port_name bond2 --nics "eth0 eth1" --bond_mode balance-tcp --bond_name bond-storage`

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

**使用示例**

`network-tool sync-bridge --ovsbr_name ovsbr-mgt --bond_mode balance-slb --bond_name bond-mgt --nics "eth0 eth1"`

**输出说明**

若输出 `sync successfully`，则表明同步数据成功。

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
- 若输出 `['eth2 can not ping xx.xx.xx.xx', 'eth2 can not ping xx.xx.xx.xx']` 表示 Bond 中的 eth2 网口的网络连通性异常。

---

## 块存储集群 CLI 命令 > 管理网络 > 管理部署前的管理网络配置信息

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

若系统输出 `create lacp bond port success`，则表明 pre\_bond 网口创建完成，绑定管理网口成功。

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

## 配置 pre\_bond 网口

为绑定网口 pre\_bond 配置静态 IP 地址，子网掩码及缺省网关。

**操作方法**

在网口配置文件路径下执行以下任一命令：

- `network-preconfig config-bond-address --ipaddr <ipaddr> --netmask <netmask> --gateway<gateway>`

  如需清理或修改配置，请参考[清除部署前的管理网络配置信息](#%E6%B8%85%E9%99%A4%E9%83%A8%E7%BD%B2%E5%89%8D%E7%9A%84%E7%AE%A1%E7%90%86%E7%BD%91%E7%BB%9C%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF)小节内容清理配置。
- `network-preconfig config-address --iface pre_bond --ipaddr <ipaddr> --netmask <netmask> --gateway<gateway>`

  如需清理或修改配置，请使用 `ip addr del` 命令清理配置。

参数说明如下：

| **参数** | **说明** |
| --- | --- |
| `--ipaddr <ipaddr>` | 必选参数。表示实际规划的 pre\_bond 网口的静态 IP 地址。 |
| `--netmask <netmask>` | 必选参数。表示实际规划的 pre\_bond 网口的子网掩码。 |
| `--gateway <gateway>` | 必选参数。表示实际规划的 pre\_bond 网口的网关。 |

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

若系统输出 `config ip address for eth0 interface success`，则表明给 eth0 物理网口配置的地址信息成功。

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

`network-preconfig clean-network-config`

**输出示例**

若系统输出 `clean network configuration success!`，则表明节点网络配置信息完全清理成功。

---

## 文件存储集群 CLI 命令 > 概述

# 概述

文件存储集群通过 `kube-apiserver` 进行 CRD（CustomResourceDefinition）管理，因此使用 kubectl 命令行工具即可查看文件存储集群相关信息。

本文档中提到的命令行格式说明如下表所示。

| 格式 | 说明 |
| --- | --- |
| `kubectl get sfscluster -n sfs-system` | 不带参数的命令，按原样输入。例如：  `kubectl get sfscluster -n sfs-system` |
| `<parameter_value>` | 尖括号表示必选参数，需用参数值代替。例如：  语法：`kubectl describe sfscluster <NAME> -n sfs-system`  输入：`kubectl describe sfscluster c80b72f4-40a0-46fa-987c-70d3d821580f -n sfs-system` |

---

## 文件存储集群 CLI 命令 > 查看文件存储集群信息

# 查看文件存储集群信息

ssh 登录 CloudTower 后，使用如下命令查看文件存储集群的相关信息。

## 查看文件存储集群列表

**操作方法**

ssh 登录 CloudTower 后，使用如下命令查看所有文件存储集群：

```
kubectl get sfscluster -n sfs-system
```

**输出示例**

```
NAME                                   SFSCLUSTERNAME   CURRENTREVISION                                   UPDATEREVISION                                    STATE
08eb01f1-f757-42b4-ba4e-309ab72ac829   bench-hdfs       08eb01f1-f757-42b4-ba4e-309ab72ac829-74b4d7dbbc   08eb01f1-f757-42b4-ba4e-309ab72ac829-74b4d7dbbc   Normal
e4e0aa80-3496-4030-a8ae-1c70555d8c62   ry-test-0920     e4e0aa80-3496-4030-a8ae-1c70555d8c62-5cb56f9847   e4e0aa80-3496-4030-a8ae-1c70555d8c62-5cb56f9847   Normal
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| NAME | 文件存储集群 ID，创建时系统自动分配，用于全局唯一标识集群，不可更改。 |
| SFSCLUSTERNAME | 文件存储集群名称，允许用户修改。 |
| CURRENTREVISION | 当前文件存储集群配置信息对应 hash 值。 |
| UPDATEREVISION | 期望的更新后的文件存储集群配置信息对应 hash 值。 |
| STATE | 文件存储集群当前状态：  - Abnormal：集群异常 - InUpgrade：集群升级中 - Normal：集群正常 - InUpdate：集群更新中 - InDelete：集群删除中 - InDeploy：集群部署中 - DeployFailed：集群部署失败 - Degraded：集群维护中 - Offline：集群已下线 |

## 查看指定文件存储集群的详细信息

**操作方法**

ssh 登录 CloudTower 后，使用如下命令查看指定文件存储集群的详细的配置和状态信息：

```
kubectl describe sfscluster <cluster Name> -n sfs-system
```

`<cluster Name>`为文件存储集群 ID。

**使用示例**

```
kubectl describe sfscluster b9a8ba53-3c3c-4254-a719-43d25424a2ef -n sfs-system
```

**输出示例**

```
Name:         b9a8ba53-3c3c-4254-a719-43d25424a2ef
Namespace:    sfs-system
Labels:       <none>
Annotations:  x-tower-user-id: clou3pkgd01uc0958ackbvtn3
              x-tower-user-ip: 10.1.0.1
API Version:  sfs.iomesh.io/v1alpha1
Kind:         SfsCluster
Metadata:
  Creation Timestamp:  2024-12-20T08:22:13Z
  Finalizers:
    cluster.finalizers.sfs-operator
    cluster.finalizers.sfs-operator/prom-metrics-protection
  Generation:  11
  Managed Fields:
  ...
  Resource Version:  148859677
  UID:               e51f558a-5bf9-4df2-8978-153ec3600cf2
Spec:
  Architecture:     X86_64
  Base Cluster Id:  cm4w6iit7r3e2095815dr3hfq
  Cluster Vip:      172.20.134.107
  Description:      test
  Fsc Config:
    Memory:  17179869184
    Vcpu:    16
  Fsc Num:   3
  Name:      sfs-offline-zbs
  Network Config:
    Network Config:
      Gateway:  172.20.128.1
      Ips:
        172.20.134.104
        172.20.134.105
        172.20.134.106
      Mask:        255.255.128.0
    Network Type:  ManagementNetwork
    Vlan Attribute:
      Zbs Vlan Attribute:
        Vds Id:  cm4w6im6ni7ag0958nkv680sj
    Network Config:
      Ips:
        10.0.130.105
        10.0.130.106
        10.0.130.107
      Mask:        255.255.255.0
    Network Type:  StorageNetwork
    Vlan Attribute:
      Zbs Vlan Attribute:
        Vds Id:  cm4w6im6mi7af0958xxnajj71
    Network Config:
      Ips:
        10.106.120.95
        10.106.120.96
        10.106.120.97
      Mask:        255.255.240.0
    Network Type:  AccessNetwork
    Vlan Attribute:
      Zbs Vlan Attribute:
        Vds Id:            cm4w6im6mi7ae0958c84ilzxn
  Online:                  true
  Revision History Limit:  0
  Version:                 v1.2.0-rc.21-20250313142646-ed6308a59a6d-debug-nostrip
Status:
  Current Fsc Num:   3
  Current Revision:  b9a8ba53-3c3c-4254-a719-43d25424a2ef-7c6bdf7d9c
  Expected Fsc Num:  3
  State:             Normal
  Update Revision:   b9a8ba53-3c3c-4254-a719-43d25424a2ef-7c6bdf7d9c
  Version:           v1.2.0-rc.21-20250313142646-ed6308a59a6d-debug-nostrip
Events:              <none>
```

**输出说明**

| 类别 | 参数 | 说明 |
| --- | --- | --- |
| SPEC | Architecture | 文件存储集群架构。 |
| Base Cluster Id | 文件存储集群所在的 SMTX ZBS 块存储集群 ID。 |
| Cluster Vip | 文件存储集群文件管理虚拟 IP。 |
| Description | 文件存储集群文字描述信息。 |
| Fsc Config | 文件控制器配置：  - Memory：单个文件控制器内存大小，单位为 B - Rate Limit：单个文件控制器流量限制 - Egress：出流量限制 - Ingress：入流量限制 - Burst：突发通信量上限，单位为 bps - Max：最大带宽，单位为 bps - Vcpu：单个文件控制器 vCPU 数量 - Cpu Exclusive：开启 CPU 独占 |
| Fsc Num | 文件控制器数量。 |
| Name | 文件存储集群名称。 |
| Network Config | 文件存储集群网络配置，包含文件管理网络、文件接入网络和文件存储网络的配置信息、网络类型和 VLAN 信息：  - Network Type：网络类型（ManagementNetwork 表示文件管理网络，StorageNetwork 表示文件存储网络，AccessNetwork表示文件接入网络） - Gateway：网关信息 - Ips：IP 地址 - Mask：子网掩码 - Vds Id：文件存储集群网络对应的 SMTX ZBS 块存储集群的 VDS ID |
| Online | 文件存储集群上下线开关。 |
| Revision History Limit | 文件存储集群保留的历史版本数量，默认为 0。 |
| Version | 文件存储集群目标版本。 |
| STATUS | Current Fsc Num | 当前集群配置下的文件控制器数量。 |
| Current Revision | 当前集群配置信息对应 hash 值。 |
| Expected Fsc Num | 期望的更新后集群配置下的文件控制器数量。 |
| State | 文件存储集群当前状态：  - Abnormal：集群异常 - InUpgrade：集群升级中 - Normal：集群正常 - InUpdate：集群更新中 - InDelete：集群删除中 - InDeploy：集群部署中 - DeployFailed：集群部署失败 - Degraded：集群维护中 - Offline：集群已下线 |
| Update Revision | 期望的扩容后的集群配置信息对应 hash 值。 |
| Version | 文件存储集群安装包的版本信息。 |

## 查看文件控制器列表

**操作方法**

ssh 登录 CloudTower 后，使用如下命令查看所有文件控制器的 ID 及其运行状态：

```
kubectl get fscontroller -n sfs-system
```

**输出示例**

```
NAME                                     CURRENTREVISION                                     UPDATEREVISION                                      ISRUNNING   ISREADY
08eb01f1-f757-42b4-ba4e-309ab72ac829-0   08eb01f1-f757-42b4-ba4e-309ab72ac829-0-5c497f94ff   08eb01f1-f757-42b4-ba4e-309ab72ac829-0-5c497f94ff   true        true
08eb01f1-f757-42b4-ba4e-309ab72ac829-1   08eb01f1-f757-42b4-ba4e-309ab72ac829-1-6559b9bdff   08eb01f1-f757-42b4-ba4e-309ab72ac829-1-6559b9bdff   true        true
08eb01f1-f757-42b4-ba4e-309ab72ac829-2   08eb01f1-f757-42b4-ba4e-309ab72ac829-2-5b4b99875    08eb01f1-f757-42b4-ba4e-309ab72ac829-2-5b4b99875    true        true
e4e0aa80-3496-4030-a8ae-1c70555d8c62-0   e4e0aa80-3496-4030-a8ae-1c70555d8c62-0-d4dd95b57    e4e0aa80-3496-4030-a8ae-1c70555d8c62-0-d4dd95b57    true        true
e4e0aa80-3496-4030-a8ae-1c70555d8c62-1   e4e0aa80-3496-4030-a8ae-1c70555d8c62-1-5dcddcfbc9   e4e0aa80-3496-4030-a8ae-1c70555d8c62-1-5dcddcfbc9   true        true
e4e0aa80-3496-4030-a8ae-1c70555d8c62-2   e4e0aa80-3496-4030-a8ae-1c70555d8c62-2-84cd4fc497   e4e0aa80-3496-4030-a8ae-1c70555d8c62-2-84cd4fc497   true        true
e4e0aa80-3496-4030-a8ae-1c70555d8c62-3   e4e0aa80-3496-4030-a8ae-1c70555d8c62-3-77fdcd6fd8   e4e0aa80-3496-4030-a8ae-1c70555d8c62-3-77fdcd6fd8   true        true
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| NAME | 文件控制器 ID，创建时系统自动分配，用于全局唯一标识文件控制器，不可更改。 |
| CURRENTREVISION | 当前文件控制器配置信息对应 hash 值。 |
| UPDATEREVISION | 期望的更新后的文件控制器配置信息对应 hash 值。 |
| ISRUNNING | 文件控制器是否正在运行。 |
| ISREADY | 文件控制器状态是否正常。 |

## 查看指定文件控制器的详细信息

**操作方法**

ssh 登录 CloudTower 后，使用如下命令查看指定文件控制器详细的配置和状态信息：

```
kubectl describe fscontroller <fsc Name> -n sfs-system
```

`<fsc Name>`为文件控制器 ID。

**使用示例**

```
kubectl describe fscontroller e984be92-d6c3-4869-bc56-0cf6a297087b-0 -n sfs-system
```

**输出示例**

```
apiVersion: sfs.iomesh.io/v1alpha1
kind: FsController
metadata:
  creationTimestamp: "2024-06-21T04:25:30Z"
  finalizers:
  - fsc.finalizers.sfs-operator
  generation: 3
  labels:
    cluster: e984be92-d6c3-4869-bc56-0cf6a297087b
    controller-revision-hash: e984be92-d6c3-4869-bc56-0cf6a297087b-759b6f859
    nodeType: MasterController
  managedFields:
    ……
  name: e984be92-d6c3-4869-bc56-0cf6a297087b-0
  namespace: sfs-system
  resourceVersion: "26004124"
  uid: 37a5dcb4-a66e-40b2-b39a-ed5bce185c51
spec:
  clusterId: e984be92-d6c3-4869-bc56-0cf6a297087b
  fscType: MasterController
  masterFsControllers:
    e984be92-d6c3-4869-bc56-0cf6a297087b-0: 10.20.160.115
    e984be92-d6c3-4869-bc56-0cf6a297087b-1: 10.20.160.116
    e984be92-d6c3-4869-bc56-0cf6a297087b-2: 10.20.160.117
  networkConfig:
  - gateway: 172.20.128.1
    ip: 172.20.180.115
    mask: 255.255.0.0
    networkType: ManagementNetwork
  - ip: 10.20.160.115
    mask: 255.255.0.0
    networkType: StorageNetwork
  - ip: ""
    mask: 255.255.240.0
    networkType: AccessNetwork
  online: true
  version: v1.1.0-rc.9-20240620190653-83cacca2605d-debug-nostrip
status:
  Application Id:         cm2vgucto4pge0858khtswup2
  Current Revision:       08eb01f1-f757-42b4-ba4e-309ab72ac829-0-5c497f94ff
  Host Id:                cm2r13gzgf1wq0858a8qhcgwr
  Is Ready:               true
  Is Running:             true
  Observed Spec Version:  3-3628323646
  Update Revision:        08eb01f1-f757-42b4-ba4e-309ab72ac829-0-5c497f94ff
  Version:                v1.2.0-rc.4-20241202115412-5e0e7c62f4ca-debug-nostrip
  Vm Id:                  cm2vgudan4pia0858d7exoiif
  Vm Local Id:            b71b086c-bc83-41e6-8dc2-387d0d7ee54b
```

**输出说明**

| 类别 | 参数 | 说明 |
| --- | --- | --- |
| SPEC | Cluster Id | 文件控制器所在文件存储集群的 ID。 |
| Fsc Type | 文件控制器类型：  - MasterController：文件控制器主节点 - StorageController：文件控制器存储节点 |
| Master Fs Controllers | 文件存储集群中所有的主文件控制器。 |
| Network Config | 文件控制器网络配置，包含文件管理网络、文件接入网络和文件存储网络的具体信息：  - Network Type：网络类型（ManagementNetwork 表示文件管理网络，StorageNetwork 表示文件存储网络，AccessNetwork表示文件接入网络） - Gateway：网关信息 - Ip：IP 地址 - Mask：子网掩码 |
| Online | 文件控制器上下线开关。 |
| Version | 文件控制器目标版本。 |
| STATUS | Application Id | 文件控制器在 CloudTower 的 CAPP ID。 |
| Host Id | 文件控制器所在 SMTX ZBS 块存储集群的主机 ID。 |
| Is Running | 文件控制器是否正在运行。 |
| Is Ready | 文件控制器状态是否正常。 |
| Observed Spec Version | 当前的文件控制器配置信息对应 hash 值。 |
| Version | 当前文件控制器使用的 SFS 安装包的版本。 |
| Vm Id | 文件控制器的虚拟机 ID。 |
| Vm Local Id | 文件控制器的 local ID。 |
| Current Revision | 当前文件控制器配置信息对应 hash 值。 |
| Update Revision | 期望的更新后的文件控制器配置信息对应 hash 值。 |

## 查看文件存储集群网络列表

**操作方法**

ssh 登录 CloudTower 后，使用如下命令查看所有文件存储集群的网络：

```
kubectl get sfsvlan -n sfs-system
```

**输出示例**

```
NAME                                                     OBSERVEDVLAN
03222a4e-890d-419f-bd0f-21bd5e6da78f-accessnetwork       clp98wx8qwd5h0958c3ft7ygf
03222a4e-890d-419f-bd0f-21bd5e6da78f-managementnetwork   clp98wx8mwd5c0958y1thbrl4
03222a4e-890d-419f-bd0f-21bd5e6da78f-storagenetwork      cls1fif08qift0958cc8ab3bg
3c36585b-c264-4d58-bd95-98db926742d7-accessnetwork       clp98wx8qwd5h0958c3ft7ygf
3c36585b-c264-4d58-bd95-98db926742d7-managementnetwork   clp98wx8mwd5c0958y1thbrl4
3c36585b-c264-4d58-bd95-98db926742d7-storagenetwork      cluatuy9644tr09584l89ixbc
c80b72f4-40a0-46fa-987c-70d3d821580f-accessnetwork       clp98wx8owd5g0958euafxjac
c80b72f4-40a0-46fa-987c-70d3d821580f-managementnetwork   clp98wx8nwd5f0958de1m3e4v
c80b72f4-40a0-46fa-987c-70d3d821580f-storagenetwork      clp993nfr3iaf0958vn0xyetj
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| NAME | 文件存储集群网络的 ID，创建时系统自动分配，用于全局唯一标识文件存储集群网络。 |
| OBSERVEDVLAN | 文件存储集群网络在 CloudTower 中对应 VLAN 的 ID。 |

## 查看指定文件存储集群网络的详细信息

**操作方法**

ssh 登录 CloudTower 后，使用如下命令查看指定文件存储集群网络的详细的配置和状态信息：

```
kubectl describe sfsvlan <vlan Name> -n sfs-system
```

`<vlan Name>` 为文件存储集群网络 ID。

**使用示例**

```
kubectl describe sfsvlan 20788a9f-5515-495f-a87c-b9d4d622b811-storagenetwork -n sfs-system
```

**输出示例**

```
Name:         20788a9f-5515-495f-a87c-b9d4d622b811-storagenetwork
Namespace:    sfs-system
Labels:       cluster=20788a9f-5515-495f-a87c-b9d4d622b811
              networkType=StorageNetwork
Annotations:  <none>
API Version:  sfs.iomesh.io/v1alpha1
Kind:         SfsVlan
Metadata:
  Creation Timestamp:  2024-06-05T09:54:19Z
  Finalizers:
    sfsVlan.finalizers.sfs-operator
  Generation:  1
  Managed Fields:
  ……
  Resource Version:  65552181
  UID:               d4e0fa5e-8f2c-49aa-8241-cfa551d019a6
Spec:
  Network Type:  StorageNetwork
  Vlan Attribute:
    Zbs Vlan Attribute:
      Vds Id:  clwpsuwfv4rgn0958oh7asp4u
Status:
  Vlan Id:  clx1nj9obbr9m0958v6kgf7z5
Events:     <none>
```

**输出说明**

| 类别 | 参数 | 说明 |
| --- | --- | --- |
| SPEC | Network Type | 网络类型 |
| Vlan Attribute | VLAN 信息包括：  - Zbs Vlan Attribute：SMTX ZBS 块存储集群的 VLAN 信息 - Vds Id：SMTX ZBS 块存储集群的 VDS ID |
| Status | Vlan Id | 文件存储集群网络在 CloudTower 中对应 VLAN 的 ID。 |

## 查看文件存储集群的统计数据列表

**操作方法**

ssh 登录 CloudTower 后，使用如下命令查看所有文件存储集群的统计数据：

```
kubectl get metrics -n sfs-system
```

**输出示例**

```
NAME                                           AGE
03222a4e-890d-419f-bd0f-21bd5e6da78f-metrics   5d20h
3c36585b-c264-4d58-bd95-98db926742d7-metrics   8d
c80b72f4-40a0-46fa-987c-70d3d821580f-metrics   40h
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| NAME | 统计数据 ID，格式为`集群ID-metrics`。 |
| AGE | 统计数据对应 CR 的创建时长，k8s 默认字段。 |

## 查看指定文件存储集群的统计数据详细信息

**操作方法**

ssh 登录 CloudTower 后，使用如下命令查看指定文件存储集群的统计数据：

```
kubectl describe metrics <metrics Name> -n sfs-system
```

`<metrics Name>` 为文件存储集群统计数据的 ID。

**使用示例**

```
kubectl describe metrics c80b72f4-40a0-46fa-987c-70d3d821580f-metrics -n sfs-system
```

**输出示例**

```
Name:         c80b72f4-40a0-46fa-987c-70d3d821580f-metrics
Namespace:    sfs-system
Labels:       cluster=c80b72f4-40a0-46fa-987c-70d3d821580f
Annotations:  <none>
API Version:  sfs.iomesh.io/v1alpha1
Kind:         Metrics
Metadata:
  Creation Timestamp:  2024-04-03T15:52:28Z
  Generation:          1
  Managed Fields:
    ……
    Manager:    manager
    Operation:  Update
    Time:       2024-04-05T05:14:14Z
  Owner References:
    API Version:           sfs.iomesh.io/v1alpha1
    Block Owner Deletion:  true
    Controller:            true
    Kind:                  SfsCluster
    Name:                  c80b72f4-40a0-46fa-987c-70d3d821580f
    UID:                   8a3fd101-de22-4b39-942c-be7064a30e12
  Resource Version:        40131828
  UID:                     eb2e4355-8d0f-464f-b06b-2707711a6e37
Spec:
  Cluster Id:  c80b72f4-40a0-46fa-987c-70d3d821580f
Status:
  Is Ready:  true
  Ns Info Metrics:
    ns1:
      Ns State:  Exported
    ns2:
      Ns State:  Exported
  Ns Stat Metrics:
    ns1:
      Capacity In Bytes:       107374182400
      Capacity Used In Bytes:  3637248
      Total Files:             0
    ns2:
      Capacity In Bytes:       107374182400
      Capacity Used In Bytes:  3637248
      Total Files:             0
Events:                        <none>
```

**输出说明**

| 类别 | 参数 | 说明 |
| --- | --- | --- |
| SPEC | Cluster Id | 统计数据关联的文件存储集群 ID。 |
| STATUS | Is Ready | true：统计数据正常上报 |
| Ns Info Metrics | Ns State 展示文件存储集群中所有文件系统的状态：  - Unexported：文件系统下线 - InUpdate：文件系统更新中 - Exported：文件系统上线 - Abnormal：文件系统异常 - Unknown：文件系统状态未知 |
| Ns Stat Metrics | 展示文件存储集群中所有文件系统的容量统计信息：  - Capacity In Bytes：文件系统总容量 - Capacity Used In Bytes：文件系统已使用容量 - Total Files：文件系统中创建的文件总数 |

## 查看文件存储集群的虚拟机放置组配置列表

文件存储集群中包括两类虚拟机放置组策略：

- 文件存储集群放置组策略：不同的文件控制器虚拟机必须放置在不同主机上
- 文件控制器放置组策略：指定文件控制器虚拟机必须放置在指定主机上

**操作方法**

ssh 登录 CloudTower 后，使用如下命令查看所有文件存储集群的虚拟机放置组配置：

```
kubectl get sfsvmplacementgroup -n sfs-system
```

**输出示例**

```
NAME                 AGE
lsr-zbs-test-0-vpg   2d5h
lsr-zbs-test-1-vpg   2d5h
lsr-zbs-test-2-vpg   2d5h
lsr-zbs-test-vpg     2d6h
ry-test-0408-0-vpg   5m31s
ry-test-0408-1-vpg   3m11s
ry-test-0408-2-vpg   22s
ry-test-0408-vpg     8m35s
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| NAME | 虚拟机放置组配置对应 ID。  - 文件存储集群放置组策略：格式为 `文件存储集群 ID-vpg` - 文件控制器放置组策略：格式为 `文件控制器 ID-vpg` |
| AGE | 虚拟机放置组配置对应 CR 的创建时长，k8s 默认字段。 |

## 查看指定文件存储集群的虚拟机放置组配置详细信息

### 查看指定文件存储集群放置组策略详细信息

**操作方法**

ssh 登录 CloudTower 后，使用如下命令查看指定文件存储集群虚拟机放置组配置的详细的配置和状态信息：

```
kubectl describe sfsvmplacementgroup <vmplacementgroup Name> -n sfs-system
```

`<vmplacementgroup Name>` 为虚拟机放置组配置对应 ID，格式为 `文件存储集群 ID-vpg`。

**使用示例**

```
kubectl describe sfsvmplacementgroup e984be92-d6c3-4869-bc56-0cf6a297087b-vpg -n sfs-system
```

**输出示例**

```
apiVersion: sfs.iomesh.io/v1alpha1
kind: SfsVmPlacementGroup
metadata:
  creationTimestamp: "2024-06-21T04:25:30Z"
  finalizers:
  - sfsVmPlacementGroupReconciler.finalizers.sfs-operator
  generation: 1
  labels:
    cluster: e984be92-d6c3-4869-bc56-0cf6a297087b
  managedFields:
    ……
   name: e984be92-d6c3-4869-bc56-0cf6a297087b-vpg
  namespace: sfs-system
  resourceVersion: "23049831"
  uid: 9aa9ebe9-4793-4938-9482-0680b636a00a
spec:
  baseClusterId: cluj9nu4f029o0958oso293du
  sfsClusterId: e984be92-d6c3-4869-bc56-0cf6a297087b
status:
  vmPlacementGroupId: clxo6u1h7c2xv0958tlfvnj0g
  vms:
  - clxo6ue7oc32z0958g9bb7si8
  - clxo6y633c3pz0958yql6gcr6
  - clxo72inbc4wh0958iqeogqcn
  - clxo777qqc5yg0958klfuwuna
```

**输出说明**

| 类别 | 参数 | 说明 |
| --- | --- | --- |
| SPEC | Sfs Cluster Id | 虚拟机放置组配置关联的文件存储集群 ID。 |
| Base Cluster Id | 虚拟机放置组配置关联的 SMTX ZBS 块存储集群 ID。 |
| STATUS | Vm Placement Group Id | 虚拟机放置组配置在 CloudTower 中的对应 ID。 |
| Vms | 虚拟机放置组配置关联的虚拟机 ID，预期关联文件存储集群所有文件控制器对应虚拟机。 |

### 查看指定文件控制器放置组策略详细信息

**操作方法**

ssh 登录 CloudTower 后，使用如下命令查看指定文件控制器虚拟机放置组配置的详细的配置和状态信息：

```
kubectl describe sfsvmplacementgroup <vmplacementgroup Name> -n sfs-system
```

`<vmplacementgroup Name>`为虚拟机放置组配置对应 ID，格式为 `文件控制器 ID-vpg`。

**使用示例**

```
describe sfsvmplacementgroup lsr-zbs-test-0-vpg -n sfs-system
```

**输出示例**

```
Name:         lsr-zbs-test-0-vpg
Namespace:    sfs-system
Labels:       cluster=lsr-zbs-test
              node=lsr-zbs-test-0
Annotations:  <none>
API Version:  sfs.iomesh.io/v1alpha1
Kind:         SfsVmPlacementGroup
Metadata:
  Creation Timestamp:  2024-04-16T08:35:58Z
  Finalizers:
    sfsVmPlacementGroupReconciler.finalizers.sfs-operator
  Generation:  1
  Managed Fields:
    ……
  Resource Version:  3959299
  UID:               5d4b7cfb-76fb-41de-a4ca-f82edfa2960c
Spec:
  Base Cluster Id:   cluwdqss6dv7o0958gb7dmtgk
  Fs Controller Id:  lsr-zbs-test-0
  Sfs Cluster Id:    lsr-zbs-test
Status:
  Vm Placement Group Id:  clv24pwqpc80h09583ua45b1t
  Vms:
    clv24m8lhc69o09589ic7liur
Events:  <none>
```

**输出说明**

| 类别 | 参数 | 说明 |
| --- | --- | --- |
| SPEC | Sfs Cluster Id | 虚拟机放置组配置关联的文件存储集群 ID。 |
| Base Cluster Id | 虚拟机放置组配置关联的 SMTX ZBS 块存储集群 ID。 |
| Fs Controller Id | 虚拟机放置组配置关联的文件控制器 ID。 |
| STATUS | Vm Placement Group Id | 虚拟机放置组配置在 CloudTower 中的对应 ID。 |
| Vms | 虚拟机放置组配置关联的虚拟机 ID，预期关联指定文件控制器对应虚拟机。 |

## 查看文件存储集群的可观测服务列表

**操作方法**

ssh 登录 CloudTower 后，使用如下命令查看所有文件存储集群的可观测服务：

```
kubectl get sfsobs -n sfs-system
```

**输出示例**

```
NAME                                       AGE
3defb8c0-df9e-415c-9c73-d6ba960521ba-obs   14d
```

**输出说明**

| 主要参数 | 说明 |
| --- | --- |
| NAME | 可观测服务对应 ID，格式为`集群ID-obs`。 |
| AGE | 可观测服务对应 CR 的创建时长，k8s 默认字段。 |

## 查看指定文件存储集群的可观测服务详细信息

**操作方法**

ssh 登录 CloudTower 后，使用如下命令查看指定文件存储集群的可观测服务的详细的配置和状态信息：

```
kubectl describe sfsobs <obs Name> -n sfs-system
```

`<obs Name>`为可观测服务对应 ID。

**使用示例**

```
kubectl describe sfsobs 3defb8c0-df9e-415c-9c73-d6ba960521ba-obs -n sfs-system
```

**输出示例**

```
Name:         3defb8c0-df9e-415c-9c73-d6ba960521ba-obs
Namespace:    sfs-system
Labels:       cluster=3defb8c0-df9e-415c-9c73-d6ba960521ba
Annotations:  <none>
API Version:  sfs.iomesh.io/v1alpha1
Kind:         SfsObservability
Metadata:
  Creation Timestamp:  2024-09-12T02:30:47Z
  Finalizers:
    sfsObservability.finalizers.sfs-operator
  Generation:  1
  Managed Fields:
    ……
  Owner References:
    API Version:           sfs.iomesh.io/v1alpha1
    Block Owner Deletion:  true
    Controller:            true
    Kind:                  SfsCluster
    Name:                  3defb8c0-df9e-415c-9c73-d6ba960521ba
    UID:                   13e72fd9-1a5b-4449-aeb8-aac14da492cf
  Resource Version:        48013698
  UID:                     d5071212-e8e2-40c6-9d10-40845f0783da
Spec:
  Cluster Id:  3defb8c0-df9e-415c-9c73-d6ba960521ba
Status:
  Instances Info:
    http://172.20.222.101:8685
    http://172.20.222.102:8685
    http://172.20.222.103:8685
    http://172.20.222.104:8685
  Is Connected:  true
  Obs Id:        2kETrCZjBl9K7wdMmZ7aVIdli9v
Events:          <none>
```

**输出说明**

| 类别 | 主要参数 | 说明 |
| --- | --- | --- |
| SPEC | Cluster Id | 可观测服务关联的文件存储集群 ID。 |
| STATUS | Is Connected | 文件存储集群是否已关联可观测服务。 |
| Obs Id | 文件存储集群关联的可观测服务 ID。 |
| Instances Info | 已关联可观测服务的文件控制器 Obs 代理访问地址。 |

---

## 文件存储集群 CLI 命令 > 管理文件存储集群

# 管理文件存储集群

ssh 登录 CloudTower 后，使用如下命令管理文件存储集群。

## 下线文件存储集群

**操作方法**

确保集群中所有文件系统均已下线，然后 ssh 登录 CloudTower，使用如下命令下线指定的文件存储集群：

```
kubectl patch sfscluster <cluster Name> -n sfs-system -p '{"spec": {"online": false}}' --type=merge
```

`<cluster Name>` 为文件存储集群 ID。

**使用示例**

```
kubectl patch sfscluster e4e0aa80-3496-4030-a8ae-1c70555d8c62 -n sfs-system -p '{"spec": {"online": false}}' --type=merge
```

**输出示例**

```
sfscluster.sfs.iomesh.io/e4e0aa80-3496-4030-a8ae-1c70555d8c62 patched
```

**输出说明**

下线命令下发成功。查看该文件存储集群详细信息，集群状态 `status.state` 为 **Offline** 表示下线成功。

## 上线文件存储集群

**操作方法**

ssh 登录 CloudTower 后，使用如下命令上线指定的文件存储集群：

```
kubectl patch sfscluster <cluster Name> -n sfs-system -p '{"spec": {"online": true}}' --type=merge
```

`<cluster Name>` 为文件存储集群 ID。

**使用示例**

```
kubectl patch sfscluster e4e0aa80-3496-4030-a8ae-1c70555d8c62 -n sfs-system -p '{"spec": {"online": true}}' --type=merge
```

**输出示例**

```
sfscluster.sfs.iomesh.io/e4e0aa80-3496-4030-a8ae-1c70555d8c62 patched
```

**输出说明**

上线命令下发成功。查看该文件存储集群详细信息，集群状态 `status.state` 为 **Normal** 表示上线成功。

---

## 文件存储集群 CLI 命令 > 查看文件系统信息

# 查看文件系统信息

## 前提条件

您可以在本地计算端使用本章节提到的命令行查看文件系统的相关信息。使用前，请您查看如下前提条件：

1. 提前获取登录文件控制器的用户名和密码。
2. 确认本地计算端满足如下要求：

   - 已安装 kubectl；
   - 计算端网络与文件管理网络连通。
3. 参照如下命令，获取文件系统所属文件存储集群的 kubeconfig 文件，并将其设置为 KUBECONFIG 环境变量：

   ```
   scp <userName>@<SFS_VIP>:/opt/iomesh/sfs/config/certs/kubevip.conf /dst/of/kubeconfig
   export KUBECONFIG=/dst/of/kubeconfig
   ```

   `<userName>` 是登录文件控制器的用户名，`<SFS_VIP>` 是文件存储集群的文件管理虚拟 IP。

## 查看文件系统列表

**操作方法**

在本地计算端使用如下命令查看文件系统列表：

```
kubectl get sfsns
```

**输出示例**

```
NAME   AGE
ns1    39h
ns2    174m
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| NAME | 文件系统名称，全局唯一，不可修改。 |
| AGE | 文件系统 CR 的创建时长，k8s 默认字段。 |

## 查看指定文件系统的详细信息

**操作方法**

在本地计算端使用如下命令查看文件系统的配置和状态信息：

```
kubectl describe sfsns <ns Name>
```

`<ns Name>`为文件系统的名称。

**使用示例**

```
kubectl describe sfsns sks-test
```

**输出示例**

- 冗余策略使用**副本**时

  ```
  Name:         sks-test
  Namespace:    default
  Labels:       <none>
  Annotations:  <none>
  API Version:  sfs.iomesh.io/v1
  Kind:         Namespace
  Metadata:
    Creation Timestamp:  2024-06-17T05:47:34Z
    Finalizers:
      namespaces.sfs.iomesh.io
    Generation:  2
    Managed Fields:
      ……
    Resource Version:  21045659
    UID:               84317ff8-4da8-4bb0-92aa-b598d0be61b2
  Spec:
    Capacity:        536870912000
    cloud_provider:  elfcp
    Dshards:         3
    Export:          true
    Followers:       1
    Mshards:         1
    nfs_export_config:
      access_config:
        default_access_type:  RW
        special_access_rules:
      anony_user_info:
        Gid:     0
        UID:     0
      sec_type:  Sys
      Squash:    RootSquash
    Protocols:
      support_hdfs:  false
      support_nfs:   true
    storage_policy:
      Ec:    <nil>
      Kind:  replica
      Parameters:
      Replicas:        2
      thin_provision:  true
    user_description:  SKS test
  Status:
    Created:  true
    Dshards:
      14:           281bb7c2-5ada-4730-ae7b-9c7da2758091-2
      15:           281bb7c2-5ada-4730-ae7b-9c7da2758091-0
      16:           281bb7c2-5ada-4730-ae7b-9c7da2758091-1
    export_status:  Exported
    Mshards:
      13:   281bb7c2-5ada-4730-ae7b-9c7da2758091-1
    Nsid:   4
    State:  Exporting
  Events:   <none>
  ```
- 冗余策略使用**纠删码**时

  ```
  Name:         nfsec21
  Namespace:    default
  Labels:       <none>
  Annotations:  <none>
  API Version:  sfs.iomesh.io/v1
  Kind:         Namespace
  Metadata:
    Creation Timestamp:  2024-06-26T10:29:26Z
    Finalizers:
      namespaces.sfs.iomesh.io
    Generation:  2
    Managed Fields:
      ……
     Resource Version:  21045665
    UID:               1618a75f-7d9b-4b06-a956-fdf4299b2c75
   Spec:
    Capacity:        536870912000
    cloud_provider:  elfcp
    Dshards:         3
    Export:          true
    Followers:       1
    Mshards:         1
    nfs_export_config:
       access_config:
        default_access_type:  RW
        special_access_rules:
      anony_user_info:
        Gid:     -2
        UID:     -2
      sec_type:  Sys
      Squash:    RootSquash
    Protocols:
      support_hdfs:  false
      support_nfs:   true
    storage_policy:
      Ec:
        K:   2
        M:   1
      Kind:  ec
      Parameters:
      replicas: null
      thin_provision:  true
    user_description:
  Status:
     Created:  true
     Dshards:
      30:           281bb7c2-5ada-4730-ae7b-9c7da2758091-0
      31:           281bb7c2-5ada-4730-ae7b-9c7da2758091-1
      32:           281bb7c2-5ada-4730-ae7b-9c7da2758091-2
    export_status:  Exported
     Mshards:
      29:   281bb7c2-5ada-4730-ae7b-9c7da2758091-0
    Nsid:   8
    State:  Exporting
  Events:   <none>
  ```

**输出说明**

| 类别 | 参数 | 说明 |
| --- | --- | --- |
| SPEC | Capacity | 文件系统容量，单位为 B。 |
| cloud\_provider | 文件系统使用的 cloud provider 名称。 |
| Dshards | 文件系统中 data shard 数量。 |
| Export | 文件系统上下线开关。 |
| Followers | shard follower 数量，即最多可容忍的 shard 失联的数量。 |
| Mshards | 文件系统中 meta shard 数量。 |
| nfs\_export\_config | 文件系统通过 NFS 协议访问的选项配置：身份验证方式、访问权限等。 |
| Protocols | 文件系统的访问协议选项：是否支持 NFS 协议访问，是否支持 HDFS 协议访问。 |
| storage\_policy | - Kind: 文件系统的存储策略，支持副本或纠删码 - Ec: 数据块(K)，校验块(M) - Replicas：副本数 - thin\_provision：是否精简置备 |
| user\_description | 文件系统的描述信息。 |
| STATUS | Created | 文件系统是否创建。 |
| Dshards | 文件系统中 data shard 信息， 格式为 `shard id: shard所在文件控制器名称`。 |
| export\_status | 文件系统是否上线。 |
| Mshards | 文件系统中 meta shard 信息， 格式为 `shard id: shard所在文件控制器名称`。 |
| Nsid | 文件系统 ID，由文件存储集群自动分配。 |

## 查看文件控制器列表

**操作方法**

在本地计算端使用如下命令查看所有文件控制器：

```
kubectl get sfsnode
```

**输出示例**

```
NAME                                     AGE
c80b72f4-40a0-46fa-987c-70d3d821580f-0   40h
c80b72f4-40a0-46fa-987c-70d3d821580f-1   40h
c80b72f4-40a0-46fa-987c-70d3d821580f-2   40h
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| NAME | 文件控制器名称，全局唯一，不可修改。 |
| AGE | 文件控制器的创建时长，k8s 默认字段。 |

## 查看指定文件控制器的详细信息

**操作方法**

在本地计算端使用如下命令查看指定文件控制器的配置和状态信息：

```
kubectl describe sfsnode <node Name>
```

`<node Name>`为文件控制器的名称。

**使用示例**

```
kubectl describe sfsnode 20788a9f-5515-495f-a87c-b9d4d622b811-0
```

**输出示例**

```
Name:         20788a9f-5515-495f-a87c-b9d4d622b811-0
Namespace:    default
Labels:       <none>
Annotations:  <none>
API Version:  sfs.iomesh.io/v1
Kind:         Node
Metadata:
  Creation Timestamp:  2024-06-05T10:06:07Z
  Finalizers:
    agent.sfs.iomesh.io
    manager.sfs.iomesh.io
  Generation:        34
  Resource Version:  5907450
  UID:               2d523079-12e7-4391-9cec-2906a73d0097
Spec:
  data_server:  10.200.134.77:20020
  data_shards:
    6-27:       4bf51204-daee-439b-adb4-4598a887fbfd
    6-30:       0c2b33e7-95ca-4bdd-9903-6cb9b43aef57
  meta_server:  10.200.134.77:20010
  meta_shards:
    6-26:     85532d5c-af12-4e9e-b7bf-0712188593d1
  node_uuid:  143da6ce-ba1c-44b8-a5a8-d9e88e06d798
  Online:     true
Status:
  data_shard_count:  2
  data_shards:
    6-27:            {"type":"Elf","provider":"elfcp","vol_name":"4bf51204-daee-439b-adb4-4598a887fbfd","vol_wwn":"24dc007f7f9474e3","dev_path":"/dev/sdb"}
    6-30:            {"type":"Elf","provider":"elfcp","vol_name":"0c2b33e7-95ca-4bdd-9903-6cb9b43aef57","vol_wwn":"24d5007f7fef4ed6","dev_path":"/dev/sdc"}
  meta_shard_count:  1
  meta_shards:
    6-26:  {"type":"Elf","provider":"elfcp","vol_name":"85532d5c-af12-4e9e-b7bf-0712188593d1","vol_wwn":"24de007f7f39a449","dev_path":"/dev/sda"}
Events:    <none>
```

**输出说明**

| 类别 | 参数 | 说明 |
| --- | --- | --- |
| SPEC | data\_server | 文件控制器内部 sfs-data 服务监听 IP + 端口号。 |
| data\_shards | 文件控制器被分配的 data shard。 |
| meta\_server | 文件控制器内部 sfs-meta 服务监听 IP + 端口号。 |
| meta\_shards | 文件控制器被分配的 meta shard。 |
| node\_uuid | 文件控制器的 uuid。 |
| Online | 文件控制器上下线开关。 |
| STATUS | data\_shard\_count | 文件控制器实际挂载 data shard 数量。 |
| data\_shards | 文件控制器实际挂载的 data shard。 |
| meta\_shard\_count | 文件控制器当前关联 meta shard 数量。 |
| meta\_shards | 文件控制器实际挂载的 meta shard。 |

## 查看 shard 列表

**操作方法**

在本地计算端使用如下命令查看所有 shard：

```
kubectl get sfsshd
```

**输出示例**

```
NAME  AGE
1-1   6d11h
1-2   6d11h
1-3   6d11h
1-4   6d11h
2-5   6d11h
2-6   6d11h
2-7   6d11h
2-8   6d11h
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| NAME | shard 名称，全局唯一，不可修改。  格式为 `ns_id-shard_id`，例如 1-2 表示的是 shard 信息为：nsid=1，shard\_id=2。 |
| AGE | shard 创建时长，k8s 默认字段。 |

## 查看指定 shard 的详细信息

**操作方法**

在本地计算端使用如下命令查看指定 shard 的配置和状态信息：

```
kubectl describe sfsshd <shard Name>
```

`<shard Name>`为 shard 的名称。

**使用示例**

```
kubectl describe sfsshd 2-5
```

**输出示例**

```
Name:         2-5
Namespace:    default
Labels:       <none>
Annotations:  <none>
API Version:  sfs.iomesh.io/v1
Kind:         Shard
Metadata:
  Creation Timestamp:  2024-06-14T06:05:46Z
  Finalizers:
    shards.sfs.iomesh.io
  Generation:  1
  Managed Fields:
     ……
  Resource Version:  18067953
  UID:               9e70d487-a2dd-464e-8ad9-ee62f7e1f65d
Spec:
  cloud_provider:  elfcp
  Export:          true
  Followers:       1
  max_blksize:     <nil>
  ns_ref:
    ns_name:       ns4backup
    ns_namespace:  default
    ns_uid:        e3b93e76-a3ca-469f-bf4d-41366e5e0fdb
  Nsid:            2
  prefer_node:     281bb7c2-5ada-4730-ae7b-9c7da2758091-2
  shard_id:        5
  shard_type:      Meta
Status:
  Abnormal:   false
  Exported:   true
  Formatted:  2024-06-14T14:06:02.043613736+08:00
  ha_members:
    281bb7c2-5ada-4730-ae7b-9c7da2758091-2
    281bb7c2-5ada-4730-ae7b-9c7da2758091-1
  mount_nodes:
    281bb7c2-5ada-4730-ae7b-9c7da2758091-2
    281bb7c2-5ada-4730-ae7b-9c7da2758091-1
  node_name:       281bb7c2-5ada-4730-ae7b-9c7da2758091-2
  volume_created:  true
  volume_name:     75f4d2f7-f60d-4545-8bbf-61e827419970
  volume_path:     iscsi://iqn.2016-02.com.smartx:system:zbs-iscsi-datastore-1718335967492j/175
  volume_wwn:      24d2007f7f62ede1
Events:            <none>
```

**输出说明**

| 类别 | 参数 | 说明 |
| --- | --- | --- |
| SPEC | cloud\_provider | shard 使用的 cloud provider 名称。 |
| Export | shard 上下线开关。 |
| Followers | shard follower 数量，即最多可容忍的 shard 失联的数量。 |
| ns\_ref | shard 关联的文件系统索引。 |
| Nsid | shard 关联的文件系统 ID。 |
| prefer\_node | shard 期望挂载的文件控制器名称。 |
| shard\_id | shard ID，创建时系统自动分配。 |
| shard\_type | shard 类型：  - meta - data |
| STATUS | Abnormal | shard 状态是否异常。 |
| Exported | shard 是否已上线。 |
| Formatted | shard 被格式化的时间。 |
| ha\_members | shard 分配的文件控制器，第一个是 leader 所在的文件控制器。 |
| mount\_nodes | shard 挂载的文件控制器，正常状态下与 `ha_members` 一致，不一致说明处于 shard 迁移的临时状态。 |
| node\_name | shard leader 所在的文件控制器，正常状态下与 `ha_members` 的第一个成员一致，不一致说明处于 shard 迁移的中间状态。 |
| volume\_created | shard 对应的 volume 是否创建。 |
| volume\_name | shard 对应 volume 名称。 |
| volume\_path | shard 对应的 iscsi 路径。 |
| volume\_wwn | shard volume 对应的 wwn，可用于文件控制器查询对应的磁盘。 |

## 查看文件接入 IP 列表

**操作方法**

在本地计算端使用如下命令查看所有文件接入 IP：

```
kubectl get vips
```

**输出示例**

```
NAME            AGE
10.200.240.38   40h
10.200.240.39   40h
10.200.240.40   40h
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| NAME | 文件接入 IP。 |
| AGE | 文件接入 IP CR 的创建时长，k8s 默认字段。 |

## 查看指定文件接入 IP 的详细信息

**操作方法**

在本地计算端使用如下命令查看指定文件接入 IP 的配置和状态信息：

```
kubectl describe vips <vip Name>
```

`<vip Name>`为文件接入 IP 的名称。

**使用示例**

```
kubectl describe vips 10.200.240.38
```

**输出示例**

```
Name:         10.200.240.38
Namespace:    default
Labels:       <none>
Annotations:  <none>
API Version:  sfs.iomesh.io/v1
Kind:         Vip
Metadata:
  Creation Timestamp:  2024-04-03T16:01:25Z
  Finalizers:
    vips.sfs.iomesh.io
  Generation:  1
  Managed Fields:
     ……
    Manager:         unknown
    Operation:       Update
    Subresource:     status
    Time:            2024-04-03T16:01:26Z
  Resource Version:  1508
  UID:               b3e9cae0-6fa5-4c28-8f07-a0df8095eae7
Spec:
  Addr:  10.200.240.38
Status:
  assigned_session:  c80b72f4-40a0-46fa-987c-70d3d821580f-2
  current_session:   c80b72f4-40a0-46fa-987c-70d3d821580f-2
  prefer_session:    c80b72f4-40a0-46fa-987c-70d3d821580f-2
  Ready:             true
Events:              <none>
```

**输出说明**

| 类别 | 参数 | 说明 |
| --- | --- | --- |
| SPEC | Addr | 文件接入 IP |
| STATUS | assigned\_session | 文件接入 IP 被分配的 session 名称，当 `prefer_session` 健康时，与其一致。 |
| current\_session | 文件接入 IP 当前所在 session 名称，正常情况下与 `assigned_session` 一致，不一致说明处在 IP 迁移过程中。 |
| prefer\_session | 文件接入 IP 优先所在 session，即当该 session 健康时，将文件接入 IP 放置在该 session；不健康时，迁移至其它可用 session。 |
| Ready | 文件接入 IP 是否可用。 |

## 查看 session 列表

session 是 Genesha 实例在 SFS 的抽象，每个 Ganesha 实例对应一个 session，一个文件控制器最多关联一个 session。

**操作方法**

在本地计算端使用如下命令查看所有 session：

```
kubectl get sessions
```

**输出示例**

```
NAME                                     AGE
c80b72f4-40a0-46fa-987c-70d3d821580f-0   40h
c80b72f4-40a0-46fa-987c-70d3d821580f-1   40h
c80b72f4-40a0-46fa-987c-70d3d821580f-2   40h
```

**输出说明**

| 参数 | 说明 |
| --- | --- |
| NAME | session 名称，全局唯一，不可修改。 |
| AGE | session 创建时长，k8s 默认字段。 |

## 查看指定 session 的详细信息

**操作方法**

在本地计算端使用如下命令查看指定 session 的配置和状态信息：

```
kubectl describe sessions <session Name>
```

`<session Name>`为 session 的名称。

**使用示例**

```
kubectl describe sessions c80b72f4-40a0-46fa-987c-70d3d821580f-0
```

**输出示例**

```
Name:         c80b72f4-40a0-46fa-987c-70d3d821580f-0
Namespace:    default
Labels:       node=c80b72f4-40a0-46fa-987c-70d3d821580f-0
Annotations:  <none>
API Version:  sfs.iomesh.io/v1
Kind:         Session
Metadata:
  Creation Timestamp:  2024-04-03T16:01:21Z
  Finalizers:
    manager.sfs.iomesh.io
    agent.sfs.iomesh.io
  Generation:  14
  Managed Fields:
     ……
  Resource Version:  1251988
  UID:               18345152-db31-4252-abdd-4989c49a4952
Spec:
  client_addr:  10.100.240.38:20031
  mac_addr:
    82
    84
    0
    225
    140
    46
  Netmask:  24
  nfs_need_export_nss:
    1:            2987895788
    2:            2987895788
  node_name:      c80b72f4-40a0-46fa-987c-70d3d821580f-0
  protocol_addr:  10.100.240.38:20030
  Stype:          NFS
  Vips:
    10.200.240.40:
Status:
  nfs_export_paths:
    ns1:
      10.200.240.40:/ns1
    ns2:
      10.200.240.40:/ns2
  session_id:  1
Events:        <none>
```

**输出说明**

| 类别 | 参数 | 说明 |
| --- | --- | --- |
| SPEC | client\_addr | session 监听地址及端口，用于接收 SFS client 相关的请求。 |
| mac\_addr | session 文件接入网卡的 mac 地址。 |
| Netmask | session 指定文件接入网卡的子网掩码。 |
| nfs\_need\_export\_nss | session NFS 协议下预期上线的文件系统。 |
| node\_name | session 所在文件控制器名称。 |
| protocol\_addr | session 监听地址及端口，用于接收 NFS 协议相关的请求。 |
| Stype | session 支持的协议类型。 |
| Vips | session 负责的文件接入 IP。 |
| STATUS | nfs\_export\_paths | session 实际上线的文件系统及其挂载路径。 |
| session\_id | session ID，创建时生成。 |
| ha\_members | shard 分配的文件控制器，第一个是 leader 所在的文件控制器。 |

## 查看所有文件系统的瞬时性能和容量信息

**操作方法**

在本地计算端使用如下命令查看所有文件系统的瞬时性能和容量信息：

```
kubectl describe metrics
```

**输出示例**

```
Name:         default
Namespace:    default
Labels:       <none>
Annotations:  <none>
API Version:  sfs.iomesh.io/v1
Kind:         Metric
Metadata:
  Creation Timestamp:  2024-04-03T16:01:12Z
  Generation:          1
  Managed Fields:
    ……
  Resource Version:  1252010
  UID:               95a7b83e-3397-42ee-931a-095d279021a4
Spec:
  cluster_id:  c80b72f4-40a0-46fa-987c-70d3d821580f
Status:
  cluster_io_metric:
    Read:
      Bps:      0
      Latency:  0
      Qps:      0
    Write:
      Bps:      0
      Latency:  0
      Qps:      0
  cluster_stat_metric:
    capacity_used:  7274496
    total_files:    0
  namespace_io_metrics:
    ns1:
      Read:
        Bps:      0
        Latency:  0
        Qps:      0
      Write:
        Bps:      0
        Latency:  0
        Qps:      0
    ns2:
      Read:
        Bps:      0
        Latency:  0
        Qps:      0
      Write:
        Bps:      0
        Latency:  0
        Qps:      0
  namespace_stat_metrics:
    ns1:
      capacity_used:  3637248
      total_files:    0
    ns2:
      capacity_used:  3637248
      total_files:    0
Events:               <none>
```

**输出说明**

| 类别 | 参数 | 说明 |
| --- | --- | --- |
| SPEC | cluster\_id | 性能数据关联的文件存储集群 ID。 |
| STATUS | cluster\_io\_metric | 文件存储集群读写 I/O 瞬时值。 |
| cluster\_stat\_metric | 集群粒度统计信息，例如：所有文件系统总的容量，总文件数等。 |
| namespace\_io\_metrics | 文件系统读写 I/O 瞬时值。 |
| namespace\_stat\_metrics | 文件系统粒度统计信息，例如：使用的容量，文件数等。 |

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
