---
title: "ELF_CSI/1.1.1/SMTX ELF CSI Driver 发布说明"
source_url: "https://internal-docs.smartx.com/elf-csi/1.1.1/release_notes/release_notes_preface_generic"
sections: 5
---

# ELF_CSI/1.1.1/SMTX ELF CSI Driver 发布说明
## 关于本文档

# 关于本文档

本文档介绍了 SMTX ELF CSI Driver 1.1.1 的版本特性，以及该版本相关的配套信息。

---

## 文档更新信息

# 文档更新信息

**2025-11-10：配合 SMTX ELF CSI Driver 1.1.1 正式发布**

---

## 版本特性说明

# 版本特性说明

**存储管理**

- 支持离线部署 SMTX ELF CSI Driver，便于在无网络环境下使用。
- 支持离线升级 SMTX ELF CSI Driver，保证存储服务的持续更新。

**存储策略**

支持创建存储类，满足不同场景的存储需求。

- 创建的 StorageClass 配置的卷挂载文件类型支持 ext4（默认）和 xfs 以满足不同业务需求。
- 创建的 StorageClass 配置的卷存储策略支持精简 2 副本（默认）、精简 3 副本、厚置备 2 副本、厚置备 3 副本。

**卷管理**

- 支持动态创建、删除持久卷，简化存储管理。
- 支持 Block 和 Filesystem 两种卷模式。
- 支持 ReadWriteOnce、ReadWriteMany、ReadOnlyMany 三种访问模式，访问模式根据不同的卷模式而有所不同。

**快照与克隆**

- 支持创建、删除持久卷快照，加强数据安全保障。
- 支持从快照恢复持久卷、克隆持久卷，简化数据备份和恢复。
- 支持增加持久卷的容量，满足业务扩展需求。

---

## 版本配套说明

# 版本配套说明

Kubernetes（简称 “K8s”）集群通过 SMTX ELF CSI Driver 可以从 K8s 集群所在的 SMTX OS（ELF）集群中获得持久存储服务，但 K8s 集群节点的 K8s 软件和操作系统、K8s 集群所在的 SMTX OS（ELF）集群、以及该 SMTX OS（ELF）集群所关联的 CloudTower 需满足以下版本要求。

| 产品或操作系统名称 | 版本要求 |
| --- | --- |
| Kubernetes | 1.20 ~ 1.30 |
| K8s 节点操作系统（Linux 操作系统） | SMTX ELF CSI Driver 对大多数 Linux 操作系统的版本没有依赖（已知不支持 CentOS 7），下面仅列出经过测试可以兼容的版本。  - Ubuntu 22.04 及以上 - 麒麟 V10 SP2 或 SP3 - Rocky 8.9 |
| SMTX OS（ELF） | 5.0.3 及以上的 5.0.x、5.1.x、6.0.x、6.1.x、6.2.x |
| CloudTower | 4.3.0 及以上的 4.x.x，且必须为基础版、企业版或企业增强版 |

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
