---
title: "sfs/1.3.0/SMTX 文件存储发布说明"
source_url: "https://internal-docs.smartx.com/sfs/1.3.0/release_notes/release-notes"
sections: 5
---

# sfs/1.3.0/SMTX 文件存储发布说明
## 关于本文档

# 关于本文档

本文档介绍了相较于 1.2.1 版本，SMTX 文件存储 1.3.0 新增、改进的功能和修复的问题，以及该版本相关的配套信息。

---

## 文档更新信息

# 文档更新信息

**2026-02-06**：**配合 SMTX 文件存储 1.3.0 正式发布**

---

## 版本更新说明

# 版本更新说明

## 新增

- 支持 HDFS 协议，Hadoop 生态系统中的组件可以访问和使用文件系统。
- 支持为 NFS 协议的文件系统自定义导出路径。
- 支持为文件控制器增加计算资源。
- 支持文件管理网络和文件接入网络复用同一个虚拟机网络且 IP 地址位于同一网段。
- 支持展示文件系统的客户端活跃连接。
- 支持展示文件存储集群和文件系统的性能监控图表。
- 支持通过 CloudTower 配置文件存储集群是否允许 Windows 客户端通过 NFSv3 协议访问。
- 支持自动重启系统盘为只读状态的文件控制器。
- 支持文件预取功能。
- 支持在文件系统使用率过高时触发告警。

## 改进

- 将新创建的文件系统的元数据盘冗余策略设置为 3 副本，保障了元数据性能并提升了元数据安全性。
- 减少了文件控制器上线、下线和 HA 文件控制器时的 I/O 暂停时间。

- 优化了文化存储集群升级流程，升级过程无需重启文件控制器，减少了升级期间的 I/O 暂停时间。
- 优化了将文件控制器的文件管理 IP 添加至 CloudTower 白名单的机制。
- 优化了存储引擎的块分配机制，提升块回收效率。

## 修复问题

- 通过改进文件管理虚拟 IP 的高可用机制，修复了文件管理网络异常时文件管理虚拟 IP 未自动迁移的问题。
- 修复了 NTIRPC 组件泄露 socket 文件描述符导致 NFS 请求未被处理的问题。
- 修复了特定条件下 NFS 后端返回非预期的不可重试错误码的问题。
- 修复了 sfs-meta、sfs-data、sfs-ganesha 在 coredump 过程中被 sfs-agent 重启导致 coredump 中断的问题。

---

## 版本配套说明

# 版本配套说明

## 与 SMTX OS 版本配套说明

本版本 SMTX 文件存储支持部署在满足以下条件的 SMTX OS 集群中：

- 软件版本：6.1.0 及以上版本，且为标准版或企业版。
- 虚拟化平台：ELF。
- 是否启用双活特性：不启用。

## 与 CloudTower 版本配套说明

本版本 SMTX 文件存储只支持使用满足以下条件的 CloudTower 管理：

- 软件版本：4.8.0 及以上版本，且为基础版、企业版或企业增强版。
- 环境配置：高配。

## 与可观测性平台版本配套说明

本版本 SMTX 文件存储支持配套可观测性平台 1.4.3 及以上版本。

## 客户端配套说明

### 物理机或虚拟机

SMTX 文件存储支持能够通过 NFSv3 或 NFSv4.1 协议使用文件存储的 Linux 客户端和能够通过 NFSv3 协议使用文件存储的 Windows 客户端。表格中仅列出已经过测试的版本。

| 平台类型 | 具体版本 |
| --- | --- |
| Linux | CentOS 7.9 |
| CentOS 8.5 |
| Ubuntu 22.04 |
| Debian 11.8 |
| Windows | Windows 7 Enterprise |
| Windows 8 Enterprise |
| Windows 8.1 Enterprise |
| Windows 10 Pro |
| Windows 11 Pro |
| Windows 2008 R2 Enterprise |
| Windows 2012 R2 Standard |
| Windows Server 2016 Standard |
| Windows Server 2016 DataCenter |
| Windows Server 2019 Standard |
| Windows Server 2022 Standard |

### Hadoop 生态

SMTX 文件存储与 Hadoop 2.x 和 Hadoop 3.x 兼容，并且与 Hadoop 生态系统中的各种组件兼容。表格中仅列出已经过测试的版本。

| Hadoop 生态平台 | 具体版本 | Hadoop 组件 | 具体版本 |
| --- | --- | --- | --- |
| CDH | 6.3.2 | Hive | 2.1.1 |
| HBase | 2.1.0 |
| Spark | 2.4.0 |
| Tez | 0.9.2 |
| HDP | 2.6.5 | Hive | 1.2.1 |
| HBase | 1.1.2 |
| YARN + MapReduce2 | 2.7.3 |
| Tez | 0.7.0 |
| 3.1.5 | Hive | 3.1.0 |
| HBase | 2.1.6 |
| YARN + MapReduce2 | 3.1.1 |
| Tez | 0.9.1 |
| - | - | StarRocks | 2.5.2 |

### Hadoop Java SDK 配套说明

Hadoop 生态系统中的组件访问和使用本版本 SMTX 文件存储时，需配套 1.0.0 版本 SFS Hadoop Java SDK。

### Kubernetes

Kubernetes 集群可使用 Kubernetes 官方提供的 NFS CSI Driver 访问文件存储集群，其所支持的 Kubernetes 及操作系统版本请参考 NFS CSI Driver 的相关文档。

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
