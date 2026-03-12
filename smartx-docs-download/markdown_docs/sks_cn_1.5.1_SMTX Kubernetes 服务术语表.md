---
title: "sks_cn/1.5.1/SMTX Kubernetes 服务术语表"
source_url: "https://internal-docs.smartx.com/sks_cn/1.5.1/sks_glossary/sks_glossary_preface"
sections: 8
---

# sks_cn/1.5.1/SMTX Kubernetes 服务术语表
## 关于本文档

# 关于本文档

本文档介绍了 SMTX Kubernetes 服务（简称 “SKS”）相关文档的常用术语，这些术语是基于它们在 SKS 中的应用来定义的。

---

## 文档更新信息

# 文档更新信息

**2025-12-12：配合 SMTX Kubernetes 服务 1.5.1 正式发布**

---

## A-E

# A-E

持久卷（PV）
:   持久卷（PersistentVolume，PV）是集群中的一块存储，与节点相似，均为集群层面的资源。

持久卷申领（PVC）
:   持久卷申领（PersistentVolumeClaim，PVC）表达对存储的特定的请求，例如大小和访问模式等。持久卷申领会耗用持久卷资源。

Control Plane 节点
:   Control Plane 节点上运行 Kubernetes 集群的 Control Plane 组件。

Control Plane 虚拟 IP
:   为管控集群或工作负载集群的 Control Plane 节点配置的虚拟 IP，是外部访问集群的入口，负责将外部访问请求自动转发到某一个 Control Plane 节点。

存储类
:   存储类（StorageClass）为管理员提供了描述存储类的方法，包含 provisioner、parameters 和 reclaimPolicy 等字段。

---

## F-J

# F-J

访问模式
:   访问模式（Access Mode）指的是持久卷所支持的具体访问方式，包含 ReadWriteOnce、ReadOnlyMany、ReadWriteMany 和 ReadWriteOncePod 四种模式。

负载均衡器
:   负载均衡器（LoadBalancer）为 Kubernetes Service 对象提供外部可访问的 IP 地址，可将流量发送到集群节点的正确端口上。

工作负载
:   在 Kubernetes 集群上运行的应用程序。Kubernetes 提供若干种内置的工作负载资源，包括 Deployment、StatefulSet、DaemonSet、Job、​CronJob 等多种类型。

工作负载集群
:   通过 SKS 创建的 Kubernetes 集群，可在其上部署工作负载，包括虚拟机集群和物理机集群。

管控集群
:   由多个虚拟机节点构建的 Kubernetes 集群。由基础设施管理员在 SMTX OS 集群中创建，运行着 SKS 系统服务，负责创建和管理工作负载集群。

滚动更新
:   指分批创建新的节点来替换旧的节点，并将旧节点上的工作负载迁移到新节点上，从而保证用户业务可以连续运行。

Ingress
:   对集群中服务的外部访问进行管理的 API 对象，典型的访问方式是 HTTP。

IP 池
:   一个 IP 池可以自动管理一系列 IP，主要提供 IP 分配、回收等功能。

节点
:   Kubernetes 通过将容器放入在节点上运行的 Pod 中来运行工作负载，节点可以是一个虚拟机或者物理机。一个 Kubernetes 集群中包含两种不同角色的节点：Control Plane 节点和 Worker 节点。

卷模式
:   卷模式（volumeMode）说明了卷的具体模式，包含文件系统、块两种模式。

---

## K-O

# K-O

Kubeconfig 文件
:   用于配置集群访问的文件，其中包含集群、用户、名字空间和身份认证机制等信息。

Kubernetes
:   一个可移植、可扩展的开源平台，用于管理容器化的工作负载和服务，可促进声明式配置和自动化。

名字空间
:   名字空间（Namespace）提供一种机制，将同一集群中的资源划分为相互隔离的组，可以在一个集群按需创建组并分开管理。

内部容器镜像仓库
:   用户在 CloudTower 的**容器镜像仓库**界面创建的容器镜像仓库。在 SKS 中可以直接配置给工作负载集群使用，以拉取相应的容器镜像。

内容库
:   CloudTower 提供的用于管理虚拟机模板和 ISO 映像的功能。

---

## P-T

# P-T

Pod
:   Kubernetes 中创建和管理的最小可部署计算单元，代表了一个独立的应用程序运行实例，该实例可能由单个容器或者几个紧耦合在一起的容器组成。

容器存储接口 (CSI)
:   容器存储接口 (Container Storage Interface，CSI) 定义了存储系统暴露给容器的标准接口。

容器镜像
:   容器镜像所承载的是封装了应用程序及其所有软件依赖的二进制数据。容器镜像是轻量级、可执行的软件包，可以单独运行；该软件包对所处的运行环境具有良定（Well Defined）的假定。

容器镜像仓库
:   一个用于存储和管理容器镜像的中心化存储系统。在 SKS 文档中，“容器镜像仓库”（“SKS 容器镜像仓库”和“外部容器镜像仓库”除外）一般指“内部容器镜像仓库”。

容器网络接口（CNI）
:   容器网络接口（Container Network Interface，CNI）定义了给容器配置网络的标准接口。

SKS 容器镜像仓库
:   在 CloudTower 的 **Kubernetes 服务**界面中部署 SKS 时创建的唯一的容器镜像仓库，用于存储和管理系统使用的容器镜像。部署 SKS 服务、创建工作负载集群时，将从该仓库拉取相应的系统镜像。

SKS 系统服务
:   SKS 相关服务的组件的总称，目前包含管控集群和 SKS 容器镜像仓库。

SMTX Kubernetes 服务（SKS）
:   SMTX Kubernetes 服务（SMTX Kubernetes Service，SKS）是面向现代化基础设施的 Kubernetes 服务。它基于 SmartX 虚拟化、分布式存储和网络等核心能力，为用户提供高性能、高可用的生产级容器基础设施。

SMTX OS 集群
:   SMTX OS 集群属于逻辑概念。在实际生产环境中，一个 SMTX OS 集群由至少 3 个运行了 SMTX OS 软件的节点通过网络互连组成。

SMTX OS 双活集群
:   启用双活特性的 SMTX OS 集群。集群以拉伸形态部署，由两个可用域和一个仲裁节点组成。两个可用域与仲裁节点间通过网络连接通信。

---

## U-Z

# U-Z

vGPU 驱动
:   vGPU 驱动随 SMTX OS 发布，是经过 SmartX 改造和适配的 NVIDIA Virtual GPU Manager。它部署在虚拟化平台，为虚拟机提供 vGPU 功能。

外部容器镜像仓库
:   用户自行部署的其他容器镜像仓库。可通过域名或 IP 地址配置给工作负载集群使用，以拉取相应的容器镜像。

Worker 节点
:   Worker 节点上运行容器化的用户工作负载。

物理机集群
:   由虚拟机节点和物理机节点构建的工作负载集群，其中 Control Plane 节点为虚拟机节点，Worker 节点为物理机节点。

虚拟机集群
:   由多个虚拟机节点构建的工作负载集群。

原地更新
:   指在更新集群或节点配置的过程中，依次更新各个节点配置而不重建节点，可以使配置变更快速生效，并避免节点重建带来的额外开销。

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
