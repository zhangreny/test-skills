---
title: "sfs/1.3.0/SMTX 文件存储 CLI 命令参考"
source_url: "https://internal-docs.smartx.com/sfs/1.3.0/sfs_cli/sfs_cli_preface"
sections: 7
---

# sfs/1.3.0/SMTX 文件存储 CLI 命令参考
## 关于本文档

# 关于本文档

本文档介绍了 SMTX 文件存储（SMTX File Storage，简称“SFS”）常见的使用场景及相关命令行。

---

## 文档更新信息

# 文档更新信息

**2026-02-06：文档随 SMTX 文件存储 1.3.0 正式发布**

---

## 概述

# 概述

文件存储集群通过 `kube-apiserver` 进行 CRD（CustomResourceDefinition）管理，因此使用 kubectl 命令行工具即可查看文件存储集群相关信息。

## 命令行格式说明

本文档中提到的命令行格式说明如下表所示。

| 格式 | 描述 |
| --- | --- |
| `kubectl get sfscluster -n sfs-system` | 不带参数的命令，按原样输入。例如：  `kubectl get sfscluster -n sfs-system` |
| `<parameter_value>` | 尖括号表示必选参数，需用参数值代替。例如：  语法：`kubectl describe sfscluster <NAME> -n sfs-system`  输入：`kubectl describe sfscluster c80b72f4-40a0-46fa-987c-70d3d821580f -n sfs-system` |

## 场景及相关命令概览

本文档主要介绍了如下几类场景的 CLI 命令：

### 查看文件存储集群信息

ssh 登录 CloudTower 后，使用如下命令查看文件存储集群的相关信息。

| 场景 | 命令 |
| --- | --- |
| 查看文件存储集群列表 | `kubectl get sfscluster -n sfs-system` |
| 查看指定文件存储集群的详细信息 | `kubectl describe sfscluster <cluster Name> -n sfs-system` |
| 查看文件控制器列表 | `kubectl get fscontroller -n sfs-system` |
| 查看指定文件控制器的详细信息 | `kubectl describe fscontroller <fsc Name> -n sfs-system` |
| 查看文件存储集群网络列表 | `kubectl get sfsvlan -n sfs-system` |
| 查看指定文件存储集群网络的详细信息 | `kubectl describe sfsvlan <vlan Name> -n sfs-system` |
| 查看文件存储集群的统计数据列表 | `kubectl get metrics -n sfs-system` |
| 查看指定文件存储集群的统计数据详细信息 | `kubectl describe metrics <metrics Name> -n sfs-system` |
| 查看文件存储集群的虚拟机放置组配置列表 | `kubectl get sfsvmplacementgroup -n sfs-system` |
| 查看指定文件存储集群的虚拟机放置组配置详细信息 | `kubectl describe sfsvmplacementgroup <vmplacementgroup Name> -n sfs-system` |
| 查看文件存储集群的可观测服务列表 | `kubectl get sfsobs -n sfs-system` |
| 查看指定文件存储集群的可观测服务详细信息 | `kubectl describe sfsobs <obs Name> -n sfs-system` |

### 管理文件存储集群

ssh 登录 CloudTower 后，使用如下命令管理文件存储集群。

| 场景 | 命令 |
| --- | --- |
| 下线文件存储集群 | `kubectl patch sfscluster <cluster Name> -n sfs-system -p '{"spec": {"online": false}}' --type=merge` |
| 上线文件存储集群 | `kubectl patch sfscluster <cluster Name> -n sfs-system -p '{"spec": {"online": true}}' --type=merge` |

### 查看文件系统信息

在本地计算端，使用如下命令行查看文件系统的相关信息。

| 场景 | 命令 |
| --- | --- |
| 查看文件系统列表 | `kubectl get sfsns` |
| 查看指定文件系统的详细信息 | `kubectl describe sfsns <ns Name>` |
| 查看文件控制器列表 | `kubectl get sfsnode` |
| 查看指定文件控制器的详细信息 | `kubectl describe sfsnode <node Name>` |
| 查看 shard 列表 | `kubectl get sfsshd` |
| 查看指定 shard 的详细信息 | `kubectl describe sfsshd <shard Name>` |
| 查看文件接入 IP 列表 | `kubectl get vips` |
| 查看指定文件接入 IP 的详细信息 | `kubectl describe vips <vip Name>` |
| 查看 session 列表 | `kubectl get sessions` |
| 查看指定 session 的详细信息 | `kubectl describe sessions <session Name>` |
| 查看许可信息 | `kubectl describe license` |
| 查看所有文件系统的瞬时性能和容量信息 | `kubectl describe metrics` |

---

## 查看文件存储集群信息

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

| 主要参数 | 说明 |
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
kubectl describe sfscluster e984be92-d6c3-4869-bc56-0cf6a297087b -n sfs-system
```

**输出示例**

```
Name:         e984be92-d6c3-4869-bc56-0cf6a297087b
Namespace:    sfs-system
Labels:       <none>
Annotations:  x-tower-user-id: cluj9mm0j025n0958jzfkg6ml
              x-tower-user-ip: 10.1.0.1
API Version:  sfs.iomesh.io/v1alpha1
Kind:         SfsCluster
Metadata:
  Creation Timestamp:  2024-06-21T04:25:28Z
  Finalizers:
    cluster.finalizers.sfs-operator
  Generation:  3
  Managed Fields:
    ……
  Resource Version:  26004174
  UID:               bfbc71ba-ef7c-42b2-a68b-f06b5237567d
Spec:
  Architecture:     X86_64
  Base Cluster Id:  cluj9nu4f029o0958oso293du
  Cluster Vip:      172.20.180.82
  Description:
  Fsc Config:
    Cpu Exclusive:         true
    Memory:                8589934592
    Vcpu:                  4
  Fsc Num:                 4
  Last Upgrade Timestamp:  2024-06-21T08:41:16Z
  Name:                    ry-test
  Network Config:
    Network Config:
      Gateway:  172.20.128.1
      Ips:
        172.20.180.115
        172.20.180.116
        172.20.180.117
        172.20.180.118
      Mask:        255.255.0.0
    Network Type:  ManagementNetwork
    Vlan Attribute:
      Os Vlan Attribute:
        Vlan Id:  clujdxj7h0lju09582bhwy007
    Network Config:
      Ips:
        10.20.160.115
        10.20.160.116
        10.20.160.117
        10.20.160.118
      Mask:        255.255.0.0
    Network Type:  StorageNetwork
    Vlan Attribute:
      Os Vlan Attribute:
        Vlan Id:  cluj9o35j09te0958dafvuigt
    Network Config:
      Ips:
        10.21.160.115
        10.21.160.116
        10.21.160.117
        10.21.160.118
      Mask:        255.255.240.0
    Network Type:  AccessNetwork
    Vlan Attribute:
      Os Vlan Attribute:
        Vlan Id:           clujdvmpi0l3y0958ez0v9ub1
  Online:                  true
  Revision History Limit:  0
  Version:                 v1.1.0-rc.9-20240620190653-83cacca2605d-debug-nostrip
Status:
  Current Fsc Num:   4
  Current Revision:  e984be92-d6c3-4869-bc56-0cf6a297087b-759b6f859
  Expected Fsc Num:  4
  State:             Normal
  Update Revision:   e984be92-d6c3-4869-bc56-0cf6a297087b-759b6f859
  Version:           v1.1.0-rc.9-20240620190653-83cacca2605d-debug-nostrip
Events:              <none>
```

**输出说明**

| 类别 | 主要参数 | 说明 |
| --- | --- | --- |
| SPEC | Architecture | 文件存储集群架构。 |
| Base Cluster Id | 文件存储集群所在的 SMTX OS（ELF）集群 ID。 |
| Cluster Vip | 文件存储集群的文件管理虚拟 IP。 |
| Description | 文件存储集群文字描述信息。 |
| Fsc Config | 文件控制器配置：  - Memory：单个文件控制器内存大小，单位为 B - Rate Limit：单个文件控制器流量限制 - Egress：出流量限制 - Ingress：入流量限制 - Burst：突发通信量上限，单位为 bps - Max：最大带宽，单位为 bps - Vcpu：单个文件控制器 vCPU 数量 |
| Fsc Num | 文件控制器数量。 |
| Name | 文件存储集群名称。 |
| Network Config | 文件存储集群网络配置，包含文件管理网络、文件接入网络和文件存储网络的配置信息、网络类型和 VLAN 信息：  - Network Type：网络类型（ManagementNetwork 表示文件管理网络，StorageNetwork 表示文件存储网络，AccessNetwork表示文件接入网络） - Gateway：网关信息 - Ips：IP 地址 - Mask：子网掩码 - Vlan Id：文件存储集群网络对应的 SMTX OS 集群的 VLAN ID |
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

| 主要参数 | 说明 |
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

| 类别 | 主要参数 | 说明 |
| --- | --- | --- |
| SPEC | Cluster Id | 文件控制器所在文件存储集群的 ID。 |
| Fsc Type | 文件控制器类型：  - MasterController：文件控制器主节点 - StorageController：文件控制器存储节点 |
| Master Fs Controllers | 文件存储集群中所有的主文件控制器。 |
| Network Config | 文件控制器网络配置，包含文件管理网络、文件接入网络和文件存储网络的具体信息：  - Network Type：网络类型（ManagementNetwork 表示文件管理网络，StorageNetwork 表示文件存储网络，AccessNetwork表示文件接入网络） - Gateway：网关信息 - Ip：IP 地址 - Mask：子网掩码 |
| Online | 文件控制器上线开关。 |
| Version | 文件控制器目标版本。 |
| STATUS | Application Id | 文件控制器在 CloudTower 的 CAPP ID。 |
| Host Id | 文件控制器所在 SMTX OS 集群的主机 ID。 |
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

| 主要参数 | 说明 |
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
kubectl describe sfsvlan e984be92-d6c3-4869-bc56-0cf6a297087b-storagenetwork -n sfs-system
```

**输出示例**

```
Name:         e984be92-d6c3-4869-bc56-0cf6a297087b-storagenetwork
Namespace:    sfs-system
Labels:       cluster=e984be92-d6c3-4869-bc56-0cf6a297087b
              networkType=StorageNetwork
Annotations:  <none>
API Version:  sfs.iomesh.io/v1alpha1
Kind:         SfsVlan
Metadata:
  ……
  Resource Version:  23047775
  UID:               9c587f31-9f22-4c17-bfbe-d7fc11c1f575
Spec:
  Network Type:  StorageNetwork
  Vlan Attribute:
    Os Vlan Attribute:
      Vlan Id:  cluj9o35j09te0958dafvuigt
Status:
  Vlan Id:  cluj9o35j09te0958dafvuigt
Events:     <none>
```

**输出说明**

| 类别 | 主要参数 | 说明 |
| --- | --- | --- |
| SPEC | Network Type | 网络类型 |
| Vlan Attribute | VLAN 信息包括：  - Os Vlan Attribute：SMTX OS 集群的 VLAN 信息 - Vlan Id：SMTX OS 集群的 VLAN ID |
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

| 主要参数 | 说明 |
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

| 类别 | 主要参数 | 说明 |
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

| 主要参数 | 说明 |
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

| 类别 | 主要参数 | 说明 |
| --- | --- | --- |
| SPEC | Sfs Cluster Id | 虚拟机放置组配置关联的文件存储集群 ID。 |
| Base Cluster Id | 虚拟机放置组配置关联的 SMTX OS 集群 ID。 |
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

| 类别 | 主要参数 | 说明 |
| --- | --- | --- |
| SPEC | Sfs Cluster Id | 虚拟机放置组配置关联的文件存储集群 ID。 |
| Base Cluster Id | 虚拟机放置组配置关联的 SMTX OS 集群 ID。 |
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

## 管理文件存储集群

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

## 查看文件系统信息

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

   `<userName>` 是登录文件控制器的用户名，`<SFS_VIP>` 是文件存储集群的的文件管理虚拟 IP。

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

| 主要参数 | 说明 |
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
kubectl describe sfsns chaos-auto-ns-eyeg7
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

| 类别 | 主要参数 | 说明 |
| --- | --- | --- |
| SPEC | Capacity | 文件系统容量，单位为 B。 |
| cloud\_provider | 文件系统使用的 cloud provider 名称。 |
| Dshards | 文件系统中 data shard 数量。 |
| Export | 文件系统上线开关。 |
| Followers | shard follower 数量，即最多可容忍的 shard 失联的数量。 |
| Mshards | 文件系统中 meta shard 数量。 |
| nfs\_export\_config | 文件系统通过 NFS 协议访问的选项配置：身份验证方式、访问权限等。 |
| Protocols | 文件系统的访问协议选项：是否支持 NFS 协议访问，是否支持 HDFS 协议访问。 |
| storage\_policy | - Kind: 文件系统的存储策略，支持副本或纠删码 - Ec: 数据块(K)，校验块(M) - Replicas：副本数 - thin\_provision：是否精简置备 |
| user\_description | 文件系统的描述信息。 |
| STATUS | Created | 文件系统是否创建。 |
| Dshards | 文件系统中 data shard 信息， 格式为 `shard id: shard 所在文件控制器名称`。 |
| export\_status | 文件系统是否上线。 |
| Mshards | 文件系统中 meta shard 信息， 格式为 `shard id: shard 所在文件控制器名称`。 |
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

| 主要参数 | 说明 |
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
kubectl describe sfsnode c80b72f4-40a0-46fa-987c-70d3d821580f-0
```

**输出示例**

```
Name:         c80b72f4-40a0-46fa-987c-70d3d821580f-0
Namespace:    default
Labels:       <none>
Annotations:  <none>
API Version:  sfs.iomesh.io/v1
Kind:         Node
Metadata:
  Creation Timestamp:  2024-04-03T16:01:21Z
  Finalizers:
    agent.sfs.iomesh.io
    manager.sfs.iomesh.io
  Generation:  31
  Managed Fields:
    ……
  Resource Version:  1251908
  UID:               162fb840-1dbf-4382-b425-f4fd24e8e6fe
Spec:
  data_server:  http://10.100.240.38:20020
  data_shards:
    2:          a1e179ea-cacf-4d59-ae5c-da73996afa24
    3:          8cde5517-ec44-4b2d-826c-aee76fe2181e
    6:          76e5ce22-35d3-4648-97cc-1e78d3e010d2
    7:          d2adc633-e796-43f2-8cf2-73c2b066c997
  meta_server:  http://10.100.240.38:20010
  meta_shards:
    1:        64180107-9ac9-42af-bae1-aa1872ed56aa
    5:        713d9b0c-1a7c-498e-ade7-cad53719fada
  node_uuid:  e1ea235e-b5b9-46fc-9ddd-be56386ffe63
  Online:     true
Status:
  data_shard_count:  4
  data_shards:
    2:               {"type":"Elf","provider":"elfcp","vol_name":"a1e179ea-cacf-4d59-ae5c-da73996afa24","vol_wwn":"24d8007f7fbe9f1c","dev_path":"/dev/sdc"}
    3:               {"type":"Elf","provider":"elfcp","vol_name":"8cde5517-ec44-4b2d-826c-aee76fe2181e","vol_wwn":"24d9007f7ff51f63","dev_path":"/dev/sdd"}
    6:               {"type":"Elf","provider":"elfcp","vol_name":"76e5ce22-35d3-4648-97cc-1e78d3e010d2","vol_wwn":"24d0007f7fed3732","dev_path":"/dev/sde"}
    7:               {"type":"Elf","provider":"elfcp","vol_name":"d2adc633-e796-43f2-8cf2-73c2b066c997","vol_wwn":"24d7007f7f2eb179","dev_path":"/dev/sdf"}
  meta_shard_count:  2
  meta_shards:
    1:   {"type":"Elf","provider":"elfcp","vol_name":"64180107-9ac9-42af-bae1-aa1872ed56aa","vol_wwn":"24d6007f7fc141d4","dev_path":"/dev/sdb"}
    5:   {"type":"Elf","provider":"elfcp","vol_name":"713d9b0c-1a7c-498e-ade7-cad53719fada","vol_wwn":"24dc007f7f547e96","dev_path":"/dev/sdg"}
Events:  <none>
```

**输出说明**

| 类别 | 主要参数 | 说明 |
| --- | --- | --- |
| SPEC | data\_server | 文件控制器内部 sfs-data 服务监听 IP + 端口号。 |
| data\_shards | 文件控制器被分配的 data shard。 |
| meta\_server | 文件控制器内部 sfs-meta 服务监听 IP + 端口号。 |
| meta\_shards | 文件控制器被分配的 meta shard。 |
| node\_uuid | 文件控制器的 uuid。 |
| Online | 文件控制器上线开关。 |
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

| 主要参数 | 说明 |
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
kubectl describe sfsshd 1-5
```

**输出示例**

```
Name:         1-5
Namespace:    default
Labels:       <none>
Annotations:  <none>
API Version:  sfs.iomesh.io/v1
Kind:         Shard
Metadata:
  Creation Timestamp:  2024-06-21T09:08:59Z
  Finalizers:
    shards.sfs.iomesh.io
  Generation:        1
  Resource Version:  146753
  UID:               6e12ec30-b95d-4f6b-8be0-0aa4eca60898
Spec:
  cloud_provider:  elfcp
  Export:          true
  Followers:       1
  max_blksize:     <nil>
  ns_ref:
    ns_name:       ns1
    ns_namespace:  default
    ns_uid:        3fa1d231-6deb-4f70-abc8-a6df987a0030
  Nsid:            1
  prefer_node:     e984be92-d6c3-4869-bc56-0cf6a297087b-2
  shard_id:        5
  shard_type:      Data
Status:
  Abnormal:   false
  Exported:   true
  Formatted:  2024-06-21T17:09:24.246331627+08:00
  ha_members:
    e984be92-d6c3-4869-bc56-0cf6a297087b-2
    e984be92-d6c3-4869-bc56-0cf6a297087b-3
  mount_nodes:
    e984be92-d6c3-4869-bc56-0cf6a297087b-2
    e984be92-d6c3-4869-bc56-0cf6a297087b-3
  node_name:       e984be92-d6c3-4869-bc56-0cf6a297087b-2
  volume_created:  true
  volume_name:     036524bf-96b8-4cb5-9a0d-53fbde5080d1
  volume_path:     iscsi://iqn.2016-02.com.smartx:system:zbs-iscsi-datastore-1703660994176f/15
  volume_wwn:      24d0007f7fdfa72e
Events:            <none>
```

**输出说明**

| 类别 | 主要参数 | 说明 |
| --- | --- | --- |
| SPEC | cloud\_provider | shard 使用的 cloud provider 名称。 |
| Export | shard 上线开关。 |
| Followers | shard follower 数量，即最多可容忍的 shard 失联的数量。 |
| ns\_ref | shard 关联的文件系统索引。 |
| Nsid | shard 关联的文件系统 ID。 |
| prefer\_node | shard 期望挂载的文件控制器名称。 |
| shard\_id | shard ID，创建时系统自动分配。 |
| shard\_type | shard 类型：  - meta - data |
| STATUS | Abnormal | shard 状态是否异常。 |
| Exported | shard 是否已上线。 |
| ha\_members | shard 分配的文件控制器，第一个是 leader 所在的文件控制器。 |
| mount\_nodes | shard 挂载的文件控制器，正常状态下与 `ha_members` 一致，不一致说明处于 shard 迁移的临时状态。 |
| node\_name | shard leader 所在的文件控制器，正常状态下与 `ha_members` 的第一个成员一致，不一致说明处于 shard 迁移的中间状态。 |
| volume\_created | shard 对应的 volume 是否创建。 |
| volume\_name | shard 对应 volume 名称。 |
| volume\_wwn | shard volume 对应的 wwn，可用于文件控制器查询对应的磁盘。 |
| Formatted | shard 被格式化的时间。 |
| volume\_path | shard 对应的 iscsi 路径。 |

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

| 主要参数 | 说明 |
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

| 类别 | 主要参数 | 说明 |
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

| 主要参数 | 说明 |
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

| 类别 | 主要参数 | 说明 |
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

## 查看许可信息

**操作方法**

在本地计算端使用如下命令查看文件存储集群的许可信息：

```
kubectl describe license
```

**输出示例**

```
Name:         default
Namespace:    default
Labels:       <none>
Annotations:  <none>
API Version:  sfs.iomesh.io/v1
Kind:         License
Metadata:
  Creation Timestamp:  2024-04-03T16:01:26Z
  Finalizers:
    licenses.sfs.iomesh.io
  Generation:  1
  Managed Fields:
    ……
  Resource Version:  1251997
  UID:               396f2c89-7eaf-4b42-9577-a429dfa278b4
Spec:
  Code:  <nil>
Status:
  Info:
    license_type:      Trial
    max_capacity:      0
    Period:            7776000
    serial_number:     93931b2a-715c-50cb-96f4-a1d98ab55c03
    sign_date:         1712160085
    software_edition:  Standard
  used_capacity:       7274496
  Valid:               true
Events:                <none>
```

**输出说明**

| 类别 | 主要参数 | 说明 |
| --- | --- | --- |
| SPEC | Code | 许可码，为空表示没有许可码，会使用默认的试用许可。 |
| STATUS | Info | 许可信息，包括：  - license\_type：许可类型 - max\_capacity：许可容量，试用许可时为 0 - Period：许可有效时间，单位为 seconds - serial\_number：文件存储集群序列号 - sign\_date：许可签发时间，UNIX timestamp - software\_edition：软件版本 |
| used\_capacity | 整个文件存储集群已使用容量总和。 |
| Valid | 许可码签名是否合法。 |

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

| 类别 | 主要参数 | 说明 |
| --- | --- | --- |
| SPEC | cluster\_id | 性能数据关联的文件存储集群 ID。 |
| STATUS | cluster\_io\_metric | 文件存储集群读写 I/O 瞬时值。 |
| cluster\_stat\_metric | 集群粒度统计信息，例如：所有文件系统总的容量，总文件数等。 |
| namespace\_io\_metrics | 文件系统读写 I/O 瞬时值。 |
| namespace\_stat\_metrics | 文件系统粒度统计信息，例如：使用的容量，文件数等。 |

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
