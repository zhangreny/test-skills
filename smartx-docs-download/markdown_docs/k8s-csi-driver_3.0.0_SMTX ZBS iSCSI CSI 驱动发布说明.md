---
title: "k8s-csi-driver/3.0.0/SMTX ZBS iSCSI CSI 驱动发布说明"
source_url: "https://internal-docs.smartx.com/k8s-csi-driver/3.0.0/k8s_iscsi_csi_driver_release_notes/zbs-iscsi-csi-driver-release-notes"
sections: 5
---

# k8s-csi-driver/3.0.0/SMTX ZBS iSCSI CSI 驱动发布说明
## 关于本文档

# 关于本文档

本文档介绍了相较于 2.8.0 版本，SMTX ZBS iSCIS CSI 驱动 3.0.0 的新增功能、修复问题和版本配套说明。

---

## 文档更新信息

# 文档更新信息

**2025-12-01：配合 SMTX ZBS iSCSI CSI 驱动 3.0.0 正式发布**

首次发布 SMTX ZBS iSCSI CSI 驱动 3.0.0 发布说明。

---

## 版本更新说明

# 版本更新说明

## 新增

- 拆分 iscsi.zbs.csi.smartx.com 作为独立的 CSI 驱动，支持 Kubernetes 集群通过该驱动使用 iSCSI 协议访问块存储服务。
- 支持对持久卷的数据进行静态加密。
- 支持 Block 和 Filesystem 类型的持久卷使用 ReadWriteOncePod 作为访问模式。
- 支持使用 SMTX ZBS 集群已有的 iSCSI LUN 静态创建持久卷，并在绑定持久卷申领后供 Kubernetes 集群使用。
- 支持使用 SMTX ZBS 集群中已有的 iSCSI LUN 快照创建卷快照内容和卷快照。
- 支持使用 Node Down Pod Handler 加速有状态 Pod 的跨节点恢复。

## 修复问题

- 调整持久卷创建逻辑，当冗余策略为纠删码时，k 值不可为奇数。
- 修复了 SMTX ZBS 块存储集群更换 Meta Leader 后，新建 Pod 无法挂载持久卷申领的问题。

---

## 版本配套说明

# 版本配套说明

| **产品/操作系统名称** | **适配版本** |
| --- | --- |
| Kubernetes | - Kubernetes v1.17 ~ v1.33 - OpenShift v4.4 ~ v4.19 |
| Linux 操作系统 | SMTX ZBS iSCSI CSI 驱动对 Linux 操作系统的版本没有依赖，下面仅列出经过测试的版本：  - CentOS 7、8 - CentOS Stream 8、9、10 - Debian 10、11、12 - openEuler 20.03、22.03、24.03 - openSUSE Leap 15 - Rocky Linux 8、9 - Ubuntu 20.04、22.04、24.04 - Ubuntu Kylin 20.04、22.04、24.04 |
| SMTX ZBS | SMTX ZBS 5.0.0 及以上版本 |
| SMTX OS | SMTX OS 4.0.7 ~ 4.0.10（分离式部署模式） |

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
