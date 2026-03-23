---
title: "iomesh_cn/1.2.0/IOMesh 用户指南"
source_url: "https://internal-docs.smartx.com/iomesh_cn/1.2.0/user_guide/about-iomesh/iomesh-preface-generic"
sections: 49
---

# iomesh_cn/1.2.0/IOMesh 用户指南
## 关于本文档

# 关于本文档

本文档介绍了在 Kubernetes 集群和 OpenShift 平台部署 IOMesh 的要求和操作流程，以及如何使用和运维 IOMesh 集群。

阅读本文档的对象需了解 IOMesh 和 Kubernetes 集群，了解分布式块存储和 iSCSI 协议的相关技术知识，并具备在 Kubernetes 集群使用存储的相关操作经验。

---

## 更新信息

# 更新信息

**2024-12-13：配合 IOMesh 1.2.0 发布**

相较于 1.1.0 版本，本版本的主要更新如下：

- 刷新中文界面用语；
- 增加“配置常驻缓存”、“提升持久卷副本数”、“替换 Kubernetes 集群节点”小节；
- 增加 PV 容量必须为 2Gi 整数倍的限制；
- 增加纠删码的 PV 配置；
- 增加“IOMesh 安装完成后，其 Chunk、Meta 以及 Zookeeper Pod 将无法切换节点。”的说明；
- 增加“在虚拟机环境上部署 IOMesh 时，建议使用全闪配置模式。”的说明；
- 增加“在混闪配置下，不允许挂载未启用 WWN 的磁盘。您可以执行 udevadm info $devicePath | grep WWN 命令来查看磁盘是否启用 WWN。”的说明；
- 增加“CPU 核心绑定配置仅支持 Cgroup V1。如果您的 Linux 发行版使用了 Cgroup V2，则无法进行 IOMesh 绑核配置。”的说明；
- 增加“若已通过 Grafana 监控 IOMesh，则需重新导入 Grafana Dashboard。”的可选操作；
- 更正“设置 open-iscsi”的命令行；
- 更新“升级多集群”小节。

---

## 关于 IOMesh

# 关于 IOMesh

介绍 IOMesh 的主要功能和关键特性，以及一些基本概念。

---

## 关于 IOMesh > IOMesh 简介

# IOMesh 简介

## 什么是 IOMesh?

IOMesh 是一个 Kubernetes-native 的云原生存储及数据平台，可以管理和自动化运维 Kubernetes 集群内的存储资源，并对运行在 Kubernetes 上的各种数据类应用（如 MySQL、Cassandra、MongoDB 和中间件等）提供持久化存储、数据保护和迁移的能力。

## 关键特性

**Kubernetes 原生**

IOMesh 完全基于 Kubernetes 自身能力构建，通过声明式 API 实现“存储即代码”，并通过代码管控基础设施和部署环境的变更，以更好地支持 DevOps。

**高性能**

IOMesh 可以在容器环境中支撑数据库等 I/O 密集型应用高效运行。IOMesh 在获得高 IOPS 的同时保持了极低且稳定的延迟，可为目标应用的稳定运行提供强有力的保障。

**无 Kernel（内核）依赖**

IOMesh 完全运行在用户空间而不是内核系统，与同一节点上的其他应用程序完全隔离。当 IOMesh 故障时不会导致整个系统的故障，其他应用仍可以照常运行。在安装部署时，也不需要再额外安装任何内核模块或担心内核版本的兼容性问题。

**存储分层**

IOMesh 支持 SSD 和 HDD 混合部署，实现成本效益最大化。使用不同的存储介质分别做缓存盘和数据盘，既可以兼顾存储性能和容量，同时还可以降低成本。

**数据保护与安全**

IOMesh 在多个层级提供了数据保护的能力。节点间通过多副本机制确保数据安全可用，故障时，多节点并发的数据恢复能够时刻确保数据冗余度符合预期。PV 级的快照能力可将数据快速恢复至快照时的状态。同时，系统能够自动检测并隔离异常硬盘，降低对系统性能的影响，并减轻运维工作负担。

IOMesh 支持创建具有身份验证功能的 PV，只允许在提供正确的凭证后才能访问相关 PV，确保数据的安全性。

**充分融入 Kubernetes 生态**

IOMesh 通过 CSI 为有状态的应用程序灵活置备存储。同时与 Kubernetes 工具链无缝协作，例如使用 Helm Chart 即可轻松部署 IOMesh；通过与 Prometheus 和 Grafana 集成，提供标准化、可视化的监控和报警服务。

**可视化 UI**

IOMesh 提供可视化界面，部署完成后即可通过 UI 创建和管理 IOMesh 相关的资源，监控集群、节点和持久卷的性能，并可执行扩缩容、启用高级功能等运维操作，进一步简化了管理难度。

## 架构

![IOMesh 产品架构](https://cdn.smartx.com/internal-docs/assets/64bec3fb/iomesh_01.png)

---

## 关于 IOMesh > 基本概念

# 基本概念

在部署和使用 IOMesh 前，建议您提前熟悉以下基本概念。

[**Kubernetes**](https://kubernetes.io/)

Kubernetes（简称 "K8s"）是一个可移植、可扩展的开源平台，用于管理容器化的工作负载和服务，以便于声明式配置和自动化。

[**Master 节点**](https://kubernetes.io/docs/concepts/overview/components/#control-plane-components)

Master 节点上运行着 Kubernetes 集群的控制平面组件并管理一组 Worker 节点。通常情况下，一个 Kubernetes 集群有 1、3 或 5 个 Master 节点。

**Worker 节点**

Worker 节点上运行 Kubernetes 集群的[节点组件](https://kubernetes.io/zh-cn/docs/concepts/overview/components/#node-components)和容器化的用户工作负载。IOMesh 部署、安装、运行在 Worker 节点上。

[**kubectl**](https://kubernetes.io/docs/reference/kubectl/)

kubectl 是使用 Kubernetes API 与 Kubernetes 集群的控制面进行通信的命令行工具。

**有状态应用**

应用程序分为有状态应用和无状态应用。有状态应用将数据持久化保存到磁盘存储空间，以供服务器、客户端和其他应用使用。无状态应用在切换会话时，不会将客户端数据保存到服务器。

**IOMesh Block Storage**

IOMesh 底层的高性能块存储服务，用于保障分布式系统一致性与数据一致性，管理元数据和本地磁盘，提供 I/O 重定向和高可用的能力。

**IOMesh 节点**

Kubernetes 集群中安装了 Chunk Pod 的 Worker 节点。

**Chunk**

每个 IOMesh Block Storage 组件内提供存储服务的模块，负责管理本地磁盘、转换访问协议，并确保数据一致性。每个 Worker 节点上只运行一个 Chunk Pod。

**LSM**

LSM（Local Storage Manager）为 Chunk 内部处理磁盘 I/O 的组件，默认以单线程的形态运行。

**Meta**

每个 IOMesh Block Storage 组件内管理元数据的模块，负责管理存储对象、管理数据副本、控制访问权限和保障数据一致性等。每个 Worker 节点上只运行一个 Meta Pod。

**IOMesh CSI Driver**

SmartX 自主研发的符合 [Kubernetes CSI](https://github.com/kubernetes-csi) 规范的 CSI 驱动，使用 RPC (Remote Procedure Call) 的方式管理持久卷，为运行在 Kubernetes 上的数据类应用提供持久化存储。

每个 Kubernetes 持久卷对应 IOMesh 集群中的一个 iSCSI LUN。

**IOMesh Operator**

IOMesh 的自动化运维组件，支持 IOMesh 滚动升级、Chunk 节点扩容缩容和 GitOps，同时还负责块设备的自动发现、分配和管理。

[**名字空间**](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

名字空间（Namespace）提供一种机制，将同一集群中的资源划分为相互隔离的组。

[**存储类**](https://kubernetes.io/docs/concepts/storage/storage-classes/)

存储类（StorageClass）为管理员提供了一种描述存储类的方法，也是动态制备 PV 的模板，管理员可为存储类配置不同的参数。

[**持久卷**](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

持久卷（PersistentVolume，PV）是集群中的一块存储，可以由管理员事先制备，或者使用存储类（StorageClass）来动态制备。持久卷和普通的卷一样， 也是使用卷插件来实现的，只是它们拥有独立于任何使用持久卷的 Pod 的生命周期。

[**持久卷申领**](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

持久卷申领（PersistentVolumeClaim，PVC）表达的是用户对存储的请求，概念上与 Pod 类似。Pod 会耗用节点资源，而 PVC 会耗用 PV 资源。Pod 可以请求特定数量的资源（CPU 和内存），而 PVC 也可以请求特定的大小和访问模式。

[**卷快照**](https://kubernetes.io/docs/concepts/storage/volume-snapshots/)

卷快照（VolumeSnapshot）是用户对于卷的快照的请求，它类似于持久卷请求。

[**卷快照类**](https://kubernetes.io/docs/concepts/storage/volume-snapshot-classes/)

卷快照类（VolumeSnapshotClass）提供了一种在制备卷快照时描述存储类别的方法。它允许指定属于卷快照（VolumeSnapshot）的不同属性，而从存储系统的相同卷上获取的每个快照的这些属性都可能有所不同，因此不能通过使用与 PVC 相同的存储类来表示。

[**卷快照内容**](https://kubernetes.io/docs/concepts/storage/volume-snapshots/)

卷快照内容（VolumeSnapshotContent）是从一个卷获取的快照，该卷由管理员在集群中制备。类似持久卷是集群中的资源一样，它也是集群中的资源。

[**卷模式**](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#volume-mode)

卷模式（volumeMode）用来描述持久卷的具体模式，是一个可选的 API 参数。Kubernetes 支持以下两种卷模式：

- 文件系统（`filesystem`）：该卷会被 Pod 挂载到某个目录。
- 块（`block`）：将该卷作为一个裸设备使用，它为 Pod 提供了访问卷的最快方式，在 Pod 和卷之间没有任何文件系统层。

[**访问模式**](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes)

访问模式（Access Modes）指的是持久卷所支持的具体访问方式。

IOMesh 支持以下三种访问模式，但 `ReadWriteMany` 和 `ReadOnlyMany` 模式只适用于卷模式为 `block` 的持久卷。

- `ReadWriteOnce`：卷可以被一个节点以读写方式挂载。当多个 Pod 在同一个节点上运行时，此访问模式允许多个 Pod 访问该卷。
- `ReadWriteMany`：卷可以被多个节点以读写方式挂载。
- `ReadOnlyMany`：卷可以被多个节点以只读方式挂载。

[**Helm**](https://helm.sh/)

Helm 是 Kubernetes 的包管理器，帮助查找、分享和使用软件构建 Kubernetes。IOMesh 必须使用 Helm 进行部署。

[**Prometheus**](https://prometheus.io/)

Prometheus 是一个开源的系统监控和警报工具包，可与 IOMesh 集成，帮助实时监控 IOMesh 存储指标和提供报警。

[**Grafana**](https://grafana.com/)

Grafana 是一个开源网络应用程序，将 Grafana 连接至数据源，即可提供实时图表、可视化图形和报警。IOMesh 的监控可以被集成进 Prometheus，您可以将 IOMesh Dashboard 模板和报警规则导入至 Grafana，实现 IOMesh 存储指标的可视化。

**Deck**

支持插件化扩展的 Kubernetes Web UI 管理平台。以 Deployment 方式部署，可通过 NodePort、LoadBalancer 或 Ingress 暴露服务。

**IOMesh Deck Plugin**

提供 IOMesh 运维管理能力的 Deck 插件。以 DaemonSet 方式部署，确保 Deck 调度到任意节点都能加载 IOMesh 插件。

---

## 部署 IOMesh 集群

# 部署 IOMesh 集群

IOMesh 集群对其安装部署的环境，如 Kubernetes/OpenShift 集群版本及节点个数、Worker 节点的硬件配置等均有一定要求。建议认真阅读[构建 IOMesh 集群的要求](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prerequisites)，参考下面流程完成部署。

---

## 部署 IOMesh 集群 > 构建 IOMesh 集群的要求

# 构建 IOMesh 集群的要求

在安装部署 IOMesh 之前，请先确保其部署环境满足以下要求。

**注意事项**

IOMesh 不支持从一个集群扩容至多个集群，请在部署前提前考虑待部署的集群数量。若部署单个集群，请参考[安装 IOMesh](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/install-iomesh) 进行操作；若部署多个集群，请参考[部署多集群](/iomesh_cn/1.2.0/user_guide/advanced-functions/multiple-cluster-management#%E9%83%A8%E7%BD%B2%E5%A4%9A%E9%9B%86%E7%BE%A4)进行操作。

## 集群要求

运行 IOMesh 的 Kubernetes 集群或者 OpenShift 集群须满足以下几点：

- 单个集群最少包含 3 个 Worker 节点。
- Kubernetes 集群版本不低于 v1.17，且不高于 v1.27。
- OpenShift 集群版本不低于 v3.11，且不高于 v4.14。

## Worker 节点的硬件配置要求

使用社区版或商业版软件部署 IOMesh 集群，对每个 Worker 节点的硬件配置要求完全相同，节点的硬件配置需满足以下要求。

**CPU**

- CPU 架构须为 Intel x86\_64、Hygon x86\_64 或者鲲鹏 AArch64。
- 至少 8 线程。

**内存**

每个 Worker 节点至少分配 16 GB 内存。

**存储控制器**

使用以下任意一种存储控制器即可：

- SAS HBA 卡
- 支持直通模式（JBOD）的 RAID 卡

**系统盘**

1 块 SSD，并且 `/opt` 目录需至少预留 100GB 供 IOMesh 元数据存放。

**数据盘和缓存盘**

根据 IOMesh 集群是否采用存储分层模式决定：

- **分层模式**：使用高速介质做缓存，低速介质做容量。“高速”和“低速”是相对概念，例如将速度更快的 NVMe SSD 作为缓存盘，充分发挥硬件性能，而速度稍低的 SATA SSD 或者 HDD 作为数据盘。
- **不分层模式**：不设置缓存盘。除有的物理盘同时含有系统分区和数据分区外，其他的物理盘都作为数据盘使用。

IOMesh 集群使用存储分层模式时，只支持混闪配置；使用存储不分层模式时，只支持全闪配置。

单个 Worker 节点的硬盘配置要求如下：

| **部署模式** | **硬盘配置要求** |
| --- | --- |
| **混闪配置** | - 缓存盘：至少 1 块 SATA SSD、SAS SSD 或 NVMe SSD，每块 SSD 的容量须大于 60 GB。 - 数据盘：至少 1 块 SATA HDD 或 SAS HDD。 - 作为缓存盘的 SSD 与作为数据盘的 HDD 容量配比约为 10% ～ 20%。 |
| **全闪配置** | 至少 1 块 SSD，每块 SSD 的容量须大于 60 GB。 |

**网卡**

每个 Worker 节点至少配置 1 张 10 GbE 或 25 GbE 网卡。

## 网络要求

为避免其他应用抢占网络带宽，建议为 IOMesh 集群配置单独的存储网络。

- 规划 IOMesh 存储网络的 IP 网段 `DATA_CIDR`，运行 IOMesh 的每个 Worker 节点所对应的 IP 地址须位于该网段内。
- 集群的存储网络 Ping 延迟在 1 ms 以下。
- 集群中所有 Worker 节点必须连接到 L2 层网络。

如需[使用 IOMesh 作为外部存储](/iomesh_cn/1.2.0/user_guide/advanced-functions/external-storage)，建议为 IOMesh 配置单独的接入网络。

- 规划 IOMesh 接入网络的 IP 网段 `ACCESS_CIDR`，运行 IOMesh 的每个 Worker 节点须有一张独立的接入网卡，且对应的 IP 地址须位于该网段内。
- 集群的接入网络 Ping 延迟在 1 ms 以下。
- 集群中所有 Worker 节点必须连接到 L2 层网络。

---

## 部署 IOMesh 集群 > 准备 IOMesh 容器镜像

# 准备 IOMesh 容器镜像

在进行 IOMesh 部署或升级时，您需要参考本节说明提前准备 IOMesh 容器镜像。

支持通过如下两种方式准备所需容器镜像，您可根据实际环境中是否具有私有镜像仓库来选择其中一种方式。

- [手动加载 IOMesh 容器镜像](#%E6%89%8B%E5%8A%A8%E5%8A%A0%E8%BD%BD-iomesh-%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F)

  当您的实际环境中不具有私有镜像仓库时，您需要手动在 Kubernetes 集群的每个节点加载 IOMesh 容器镜像。
- [推送 IOMesh 容器镜像至私有镜像仓库](#%E6%8E%A8%E9%80%81-iomesh-%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F%E8%87%B3%E7%A7%81%E6%9C%89%E9%95%9C%E5%83%8F%E4%BB%93%E5%BA%93)

  当您的实际环境中具有私有镜像仓库时，建议根据待部署 IOMesh 的集群服务器的 CPU 架构类型，选择其中一种方式推送 IOMesh 容器镜像至私有镜像仓库。

  - [推送单架构镜像](#%E6%8E%A8%E9%80%81%E5%8D%95%E6%9E%B6%E6%9E%84%E9%95%9C%E5%83%8F)

    当待部署 IOMesh 的集群服务器的 CPU 架构均为同一种时，建议采用推送单架构镜像的方式准备 IOMesh 容器镜像。
  - [推送多架构镜像](#%E6%8E%A8%E9%80%81%E5%A4%9A%E6%9E%B6%E6%9E%84%E9%95%9C%E5%83%8F)

    当待部署 IOMesh 的集群服务器的 CPU 架构同时包括 Intel x86\_64 和鲲鹏 AArch64 时，需采用推送多架构镜像的方式准备 IOMesh 容器镜像。
  > **注意：**
  >
  > 仅支持以单架构镜像方式推送 Hygon x86\_64 IOMesh 容器镜像：
  >
  > - 当集群服务器的 CPU 架构包含 Intel x86\_64、Hygon x86\_64 和鲲鹏 AArch64 时，需采用单架构镜像方式推送 Hygon x86\_64 IOMesh 容器镜像，采用多架构镜像方式推送 Intel x86\_64 和鲲鹏 AArch64 IOMesh 容器镜像。
  > - 当集群服务器的 CPU 架构包含 Intel x86\_64 和 Hygon x86\_64、或者鲲鹏 AArch64 和 Hygon x86\_64 时，均需采用单架构镜像方式推送 IOMesh 容器镜像。

## 手动加载 IOMesh 容器镜像

1. 根据服务器的 CPU 架构，提前下载对应的 IOMesh 离线安装包至每个 Worker 节点和 Master 节点。
2. 根据服务器的 CPU 架构，执行对应的命令，在每个 Worker 节点和 Master 节点解压缩离线安装包。

   - **Intel x86\_64**

     ```
     tar -xf iomesh-offline-v1.2.0-amd64.tgz && cd iomesh-offline
     ```
   - **Hygon x86\_64**

     ```
     tar -xf iomesh-offline-v1.2.0-hygon-amd64.tgz && cd iomesh-offline
     ```
   - **鲲鹏 AArch64**

     ```
     tar -xf iomesh-offline-v1.2.0-arm64.tgz && cd iomesh-offline
     ```
3. 根据您所使用的容器工具，执行下述相应的脚本，在每个 Worker 节点和 Master 节点上加载 IOMesh 镜像。

   - **Docker**

     ```
     docker load --input ./images/iomesh-offline-images.tar
     ```
   - **Containerd**

     ```
     ctr --namespace k8s.io image import ./images/iomesh-offline-images.tar
     ```
   - **Podman**

     ```
     podman load --input ./images/iomesh-offline-images.tar
     ```
   > **说明：**
   >
   > 由于容器服务的 Socket 地址为非默认地址而导致加载 IOMesh 镜像失败时，需要通过参数显式指定 Socket 地址。

## 推送 IOMesh 容器镜像至私有镜像仓库

**前提条件**

- 请提前在私有镜像仓库中创建名为 `iomesh` 的项目，并将其访问级别设置为**公开**。
- 请提前获取登录私有镜像仓库的账号，并确保该账号具有 `iomesh` 项目的推送权限。

**注意事项**

以下均以 **Docker** 容器环境为例进行操作介绍，使用其他容器运行时则需替换为相应命令。

### 推送单架构镜像

1. 在任一可连接私有镜像仓库的节点上执行如下命令，以登录私有镜像仓库。

   `REGISTRY.YOURDOMAIN.COM:PORT`：私有镜像仓库地址，请根据实际情况进行替换。

   ```
   docker login <REGISTRY.YOURDOMAIN.COM:PORT>
   ```
2. 根据服务器的 CPU 架构，下载对应的 IOMesh 离线安装包至该节点。
3. 根据服务器的 CPU 架构，执行对应的命令，解压缩离线安装包。

   - **Intel x86\_64**

     ```
     tar -xf iomesh-offline-v1.2.0-amd64.tgz && cd iomesh-offline/images
     ```
   - **Hygon x86\_64**

     ```
     tar -xf iomesh-offline-v1.2.0-hygon-amd64.tgz && cd iomesh-offline/images
     ```
   - **鲲鹏 AArch64**

     ```
     tar -xf iomesh-offline-v1.2.0-arm64.tgz && cd iomesh-offline/images
     ```
4. 推送单架构镜像至私有镜像仓库。

   ```
   ./push-images.sh -l ./image-list.txt -i ./iomesh-offline-images.tar -r <REGISTRY.YOURDOMAIN.COM:PORT>
   ```

### 推送多架构镜像

1. 在任一可连接私有镜像仓库的节点上执行如下命令，以登录私有镜像仓库。

   `REGISTRY.YOURDOMAIN.COM:PORT`：私有镜像仓库地址，请根据实际情况进行替换。

   ```
   docker login <REGISTRY.YOURDOMAIN.COM:PORT>
   ```
2. 下载 Intel x86\_64 和鲲鹏 AArch64 的 IOMesh 离线安装包至该节点。
3. 推送 Intel x86\_64 IOMesh 容器镜像。

   1. 执行如下命令，解压缩 Intel x86\_64 IOMesh 离线安装包。

      ```
      mkdir intel-x86_64
      tar -xf iomesh-offline-v1.2.0-amd64.tgz -C intel-x86_64 && cd intel-x86_64/iomesh-offline/images
      ```
   2. 执行如下命令，推送 Intel x86\_64 IOMesh 容器镜像至私有镜像仓库。

      ```
      ./push-images.sh -l ./image-list.txt -i ./iomesh-offline-images.tar -r <REGISTRY.YOURDOMAIN.COM:PORT> --platform amd64
      ```
4. 推送鲲鹏 AArch64 IOMesh 容器镜像。

   1. 执行如下命令，解压缩鲲鹏 AArch64 IOMesh 离线安装包。

      ```
      mkdir kunpeng-AArch64
      tar -xf iomesh-offline-v1.2.0-arm64.tgz -C kunpeng-AArch64 && cd kunpeng-AArch64/iomesh-offline/images
      ```
   2. （可选）当 Docker 版本低于 20.10 时，执行以下命令，开启 `manifest` 相关功能。

      ```
      export DOCKER_CLI_EXPERIMENTAL=enabled
      ```
   3. 执行如下命令，推送 AArch64 镜像至私有镜像仓库。

      ```
      ./push-images.sh -l ./image-list.txt -i ./iomesh-offline-images.tar -r <REGISTRY.YOURDOMAIN.COM:PORT> --platform arm64 --create-manifest
      ```

---

## 部署 IOMesh 集群 > 安装 IOMesh

# 安装 IOMesh

IOMesh 支持在所有 Kubernetes 平台通过以下几种方式进行安装。您可以根据现场实际情况选择安装方式。Kubernetes 集群网络无法与外网连通时，可选择自定义离线安装方式。

- **一键在线安装**：使用文件里的默认设置，无法自定义参数。
- **自定义在线安装**：支持自定义参数。
- **自定义离线安装**：支持自定义参数。

## 一键在线安装

**前提条件**

- 运行 Kubernetes 集群的服务器的 CPU 架构须为 Intel x86\_64 或者鲲鹏 AArch64。
- 默认安装社区版的软件，并且只支持在 3 个 Worker 节点上进行部署。
- 只支持混闪模式的配置。

**操作步骤**

1. 登录 Master 节点。
2. 执行如下脚本文件，安装 IOMesh。执行命令时，请用实际网段替换 `10.234.1.0/24`。

   > **说明:**
   >
   > 脚本文件中已包含 Kubernetes 的包管理工具 Helm。若当前集群未安装 Helm，系统将为其自动安装。

   ```
   # 运行 IOMesh 的每个 Worker 节点所对应的 IP 地址必须位于 IOMESH_DATA_CIDR 网段内
   export IOMESH_DATA_CIDR=10.234.1.0/24; curl -sSL https://iomesh.run/install_iomesh.sh | bash -
   ```
3. 执行完脚本文件后等待几分钟，然后执行如下命令，检查每个 Worker 节点中所有 Pod 的运行状况。若 Pod 正常运行，表示已成功安装 IOMesh。

   ```
   watch kubectl get --namespace iomesh-system pods
   ```

   > **说明：**
   >
   > - 若安装失败，系统将保留执行以上脚本产生的 IOMesh 资源，以便帮助排除故障。您可以通过运行脚本 `curl -sSL https://iomesh.run/uninstall_iomesh.sh | sh -`，从 Kubernetes 集群中删除所有 IOMesh 资源。
   > - 首次安装 IOMesh 时，Kubernetes 集群中所有可调度的节点将自动启动 `prepare-csi` Pod 来安装和设置 `open-iscsi`。若所有节点的 `open-iscsi` 安装成功，系统将自动清理 `prepare-csi` Pod。若某个节点的 `open-iscsi` 安装失败，即 `prepare-csi` Pod 不断失败退出，则可以查看对应 Pod 日志或通过手动[设置 `open-iscsi`](/iomesh_cn/1.2.0/user_guide/appendices/setup-open-iscsi) 来确认 `open-iscsi` 安装失败的原因。
   > - 如果安装 IOMesh 后手动删除了 `open-iscsi`，那么重新安装 IOMesh 时不会自动启动 `prepare-csi` Pod 来自动安装 `open-iscsi`。此时，需要手动[设置 `open-iscsi`](/iomesh_cn/1.2.0/user_guide/appendices/setup-open-iscsi)。
   > - CoreOS 版本的 Linux 操作系统不支持 `prepare-csi`。当 Linux 操作系统的版本为 CoreOS 时，需要手动[设置 `open-iscsi`](/iomesh_cn/1.2.0/user_guide/appendices/setup-open-iscsi)。

## 自定义在线安装

**前提条件**

运行 Kubernetes 集群的服务器的 CPU 架构须为 Intel x86\_64、Hygon x86\_64 或者鲲鹏 AArch64。

**操作步骤**

1. 登录 Master 节点。
2. 在 Kubernetes 集群上安装 Kubernetes 的包管理工具 Helm。如果当前集群已安装 Helm，请跳过此步骤，直接进入下一步。

   ```
   curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
   chmod 700 get_helm.sh
   ./get_helm.sh
   ```

   更多细节请参考 Helm 官方文档 [Installing Helm](https://helm.sh/docs/intro/install/)。
3. 添加 IOMesh Helm Repository。

   ```
   helm repo add iomesh http://iomesh.com/charts
   ```
4. 导出 IOMesh 的默认配置文件 `iomesh.yaml`。

   ```
   helm show values iomesh/iomesh > iomesh.yaml
   ```
5. 修改 `iomesh.yaml`，自定义字段。

   - 设置全局镜像拉取地址 `registry`。

     系统默认将此字段的值设置为 `docker.io/`，即从 `docker.io` 拉取容器镜像。您可以通过将该参数修改为 `ccr.ccs.tencentyun.com/` 以加快镜像拉取速度。

     ```
     global:
       registry: "docker.io/" # global variable registry to locate the images.
     ```
   - 设置 `DATA_CIDR`，可参考[网络要求](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prerequisites#%E7%BD%91%E7%BB%9C%E8%A6%81%E6%B1%82)中所规划的 DATA\_CIDR 网段进行设置。

     ```
     iomesh:
       chunk:
         dataCIDR: "" # Fill in the DATA_CIDR you configured previously in Prerequisites.
     ```
   - 设置集群的部署模式 `diskDeploymentMode`：使用全闪或混闪配置。

     系统默认将此字段的值设置为 `hybridFlash`，即混闪配置模式，如果集群部署时采用全闪配置模式，需要将该字段的值修改为 `allFlash`。

     在虚拟机环境上部署 IOMesh 时，建议使用全闪配置模式。

     ```
     diskDeploymentMode: "hybridFlash" # Set the disk deployment mode.
     ```
   - 设置服务器的 CPU 架构。

     如果运行 Kubernetes 集群的服务器为 hygon\_x86\_64 服务器，请将此字段的值设置为 `hygon_x86_64`，否则请留空。

     ```
     platform: ""
     ```
   - 设置 IOMesh 部署的版本：社区版或者企业版。

     系统默认此字段空白，可以指定为 `community`（社区版）或者 `enterprise`（企业版）。如果不指定，系统将自动安装成社区版。

     若您购买的许可为企业版，请将该字段的值设置为 `enterprise`。社区版与企业版的区别可参考 [IOMesh 规格](https://www.iomesh.com/spec)。

     ```
     edition: "" # If left blank, Community Edition will be installed.
     ```
   - （可选）默认部署 3 个 IOMesh Chunk Pod，如果当前部署的版本为企业版，则支持部署 3 个以上的 Chunk Pod。

     ```
     iomesh:
       chunk:
         replicaCount: 3 # Specify the number of chunk pods.
     ```
   - （可选）如果期望 IOMesh 只使用部分 Kubernetes 节点的磁盘，请在 `chunk.podPolicy.affinity` 字段配置对应节点标签（label）。例如:

     ```
     iomesh:
       chunk:
         podPolicy:
           affinity:
             nodeAffinity:
               requiredDuringSchedulingIgnoredDuringExecution:
                 nodeSelectorTerms:
                 - matchExpressions:
                   - key: kubernetes.io/hostname 
                     operator: In
                     values:
                     - iomesh-worker-0 # Specify the values of the node label.
                     - iomesh-worker-1
     ```

     建议只配置 `values`，更多的配置信息可参考 [Pod Affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity)。
   - （可选）您可以通过配置 `podDeletePolicy` 字段，决定 Pod 所在的 Kubernetes 节点发生故障时，系统是否自动删除并在其他健康节点上重新创建该 Pod。此配置仅适用于以下情况的 Pod：必须挂载由 IOMesh 创建的 PVC，并且 PVC 访问模式限定为 `ReadWriteOnce`。

     若未指定该字段，系统默认值为 `no-delete-pod`，即 Pod 所在 Kubernetes 节点发生故障时，系统不会自动删除和重建 Pod。

     ```
     csi-driver:
       driver:
         controller:
           driver:
             podDeletePolicy: "no-delete-pod" # Supports "no-delete-pod", "delete-deployment-pod", "delete-statefulset-pod", or "delete-both-statefulset-and-deployment-pod".
     ```
   - （可选）您可以[配置 LSM 多线程](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/performance-tips#%E9%85%8D%E7%BD%AE-lsm-%E5%A4%9A%E7%BA%BF%E7%A8%8B)、[配置 CPU 核心绑定与独占](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/performance-tips#%E9%85%8D%E7%BD%AE-cpu-%E6%A0%B8%E5%BF%83%E7%BB%91%E5%AE%9A%E4%B8%8E%E7%8B%AC%E5%8D%A0)或[配置常驻缓存](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/performance-tips#%E9%85%8D%E7%BD%AE%E5%B8%B8%E9%A9%BB%E7%BC%93%E5%AD%98)，以优化 IOMesh 集群性能。
   - （可选）当需要使用 IOMesh 作为外部存储时，您可以[配置接入网络](/iomesh_cn/1.2.0/user_guide/advanced-functions/external-storage#%E5%8F%AF%E9%80%89%E9%85%8D%E7%BD%AE%E6%8E%A5%E5%85%A5%E7%BD%91%E7%BB%9C)来对外提供存储服务，以达到更好的存储性能和稳定性。
6. 部署 IOMesh 集群。

   ```
   helm install iomesh iomesh/iomesh \
           --create-namespace \
           --namespace iomesh-system \
           --values iomesh.yaml \
           --wait
   ```

   执行完上述命令后，您将看到如下结果：

   ```
   NAME: iomesh
   LAST DEPLOYED: Wed Jun 30 16:00:32 2021
   NAMESPACE: iomesh-system
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   ```
7. 检查部署结果。

   ```
   kubectl --namespace iomesh-system get pods
   ```

   执行完上述命令后，您将看到如下结果。如果所有 Pod 的状态均显示为 `Running`，则表示 IOMesh 安装成功。

   ```
   NAME                                                   READY   STATUS    RESTARTS      AGE
   iomesh-blockdevice-monitor-5b8b68b5fd-52q6t            1/1     Running   0             77m
   iomesh-blockdevice-monitor-prober-dqcth                1/1     Running   0             77m
   iomesh-blockdevice-monitor-prober-dsftk                1/1     Running   0             77m
   iomesh-blockdevice-monitor-prober-xhkq9                1/1     Running   0             77m
   iomesh-chunk-0                                         3/3     Running   2 (76m ago)   76m
   iomesh-chunk-1                                         3/3     Running   1 (76m ago)   76m
   iomesh-chunk-2                                         3/3     Running   0             76m
   iomesh-csi-driver-controller-plugin-66d7dbf68-65hk8    6/6     Running   0             77m
   iomesh-csi-driver-controller-plugin-66d7dbf68-l54xx    6/6     Running   0             77m
   iomesh-csi-driver-controller-plugin-66d7dbf68-xr6gg    6/6     Running   0             77m
   iomesh-csi-driver-node-plugin-hllf2                    3/3     Running   0             77m
   iomesh-csi-driver-node-plugin-smqld                    3/3     Running   0             77m
   iomesh-csi-driver-node-plugin-wdrxr                    3/3     Running   0             77m
   iomesh-deck-7c4749d7c6-mksxr                           1/1     Running   0             77m
   iomesh-deck-7c4749d7c6-s5bp8                           1/1     Running   0             77m
   iomesh-deck-plugin-iomesh-2s6ds                        1/1     Running   0             77m
   iomesh-deck-plugin-iomesh-s97pp                        1/1     Running   0             77m
   iomesh-deck-plugin-iomesh-xxbrf                        1/1     Running   0             77m
   iomesh-hostpath-provisioner-6wkks                      1/1     Running   0             77m
   iomesh-hostpath-provisioner-m896d                      1/1     Running   0             77m
   iomesh-hostpath-provisioner-qksfs                      1/1     Running   0             77m
   iomesh-iscsi-redirector-pnpz4                          2/2     Running   1 (76m ago)   76m
   iomesh-iscsi-redirector-sdknz                          2/2     Running   1 (76m ago)   76m
   iomesh-iscsi-redirector-ws4m7                          2/2     Running   1 (76m ago)   76m
   iomesh-localpv-manager-p8hdj                           4/4     Running   0             77m
   iomesh-localpv-manager-tzs78                           4/4     Running   0             77m
   iomesh-localpv-manager-xzb6w                           4/4     Running   0             77m
   iomesh-meta-0                                          2/2     Running   0             76m
   iomesh-meta-1                                          2/2     Running   0             76m
   iomesh-meta-2                                          2/2     Running   0             76m
   iomesh-openebs-ndm-cluster-exporter-5767fbbcfc-glfz5   1/1     Running   0             77m
   iomesh-openebs-ndm-node-exporter-9hpdt                 1/1     Running   0             77m
   iomesh-openebs-ndm-node-exporter-f4tvf                 1/1     Running   0             77m
   iomesh-openebs-ndm-node-exporter-x2r4w                 1/1     Running   0             77m
   iomesh-openebs-ndm-operator-646dbc445-j96z8            1/1     Running   0             77m
   iomesh-openebs-ndm-rpts5                               1/1     Running   0             77m
   iomesh-openebs-ndm-v9f27                               1/1     Running   0             77m
   iomesh-openebs-ndm-w5v79                               1/1     Running   0             77m
   iomesh-zookeeper-0                                     1/1     Running   0             77m
   iomesh-zookeeper-1                                     1/1     Running   0             77m
   iomesh-zookeeper-2                                     1/1     Running   0             76m
   iomesh-zookeeper-operator-585f4c89d9-plq9l             1/1     Running   0             77m
   operator-76c7996dbc-6fjdn                              1/1     Running   0             77m
   operator-76c7996dbc-tbpfm                              1/1     Running   0             77m
   operator-76c7996dbc-xqrj7                              1/1     Running   0             77m
   ```

   > **说明：**
   >
   > - 首次安装 IOMesh 时，Kubernetes 集群中所有可调度的节点将自动启动 `prepare-csi` Pod 来安装和设置 `open-iscsi`。若所有节点的 `open-iscsi` 安装成功，系统将自动清理 `prepare-csi` Pod。若某个节点的 `open-iscsi` 安装失败，即 `prepare-csi` Pod 不断失败退出，则可以查看对应 Pod 日志或通过手动[设置 `open-iscsi`](/iomesh_cn/1.2.0/user_guide/appendices/setup-open-iscsi) 来确认 `open-iscsi` 安装失败的原因。
   > - 如果安装 IOMesh 后手动删除了 `open-iscsi`，那么重新安装 IOMesh 时不会自动启动 `prepare-csi` Pod 来自动安装 `open-iscsi`。此时，需要手动[设置 `open-iscsi`](/iomesh_cn/1.2.0/user_guide/appendices/setup-open-iscsi)。
   > - CoreOS 版本的 Linux 操作系统不支持 `prepare-csi`。当 Linux 操作系统的版本为 CoreOS 时，需要手动[设置 `open-iscsi`](/iomesh_cn/1.2.0/user_guide/appendices/setup-open-iscsi)。
   > - IOMesh 安装完成后，其 Chunk、Meta 以及 Zookeeper Pod 将无法切换节点。

## 自定义离线安装

**前提条件**

- 运行 Kubernetes 集群的服务器的 CPU 架构须为 Intel x86\_64、Hygon x86\_64 或者鲲鹏 AArch64。
- 根据待部署 IOMesh 的集群服务器的 CPU 架构，提前下载对应的 IOMesh 离线安装包至任意一个 Master 节点。

**操作步骤**

1. [准备 IOMesh 容器镜像](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prepare-iomesh-images)。
2. 根据服务器的 CPU 架构，选择执行对应的命令，在 Master 节点解压缩离线安装包。

   - Intel x86\_64

     ```
     tar -xf iomesh-offline-v1.2.0-amd64.tgz && cd iomesh-offline
     ```
   - Hygon x86\_64

     ```
     tar -xf iomesh-offline-v1.2.0-hygon-amd64.tgz && cd iomesh-offline
     ```
   - 鲲鹏 AArch64

     ```
     tar -xf iomesh-offline-v1.2.0-arm64.tgz && cd iomesh-offline
     ```
3. 在 Master 节点上执行如下命令，导出 IOMesh 的默认配置文件 `iomesh.yaml`。

   ```
   ./helm show values charts/iomesh > iomesh.yaml
   ```
4. 修改 `iomesh.yaml`，自定义字段。

   - 设置全局镜像拉取地址 `registry`。

     系统默认将此字段的值设置为 `docker.io/`。

     若采用[手动加载 IOMesh 容器镜像](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prepare-iomesh-images#%E6%89%8B%E5%8A%A8%E5%8A%A0%E8%BD%BD-iomesh-%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F)至 Kubernetes 集群所有节点的方式准备容器镜像，则配置为默认值 `docker.io/` 即可；若已[推送 IOMesh 容器镜像至私有镜像仓库](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prepare-iomesh-images#%E6%8E%A8%E9%80%81-iomesh-%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F%E8%87%B3%E7%A7%81%E6%9C%89%E9%95%9C%E5%83%8F%E4%BB%93%E5%BA%93)，则需将此字段配置为私有镜像仓库名加 `/` 后缀。

     ```
     global:
       registry: "docker.io/" # global variable registry to locate the images.
     ```
   - 设置 `DATA_CIDR`，可参考[网络要求](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prerequisites#%E7%BD%91%E7%BB%9C%E8%A6%81%E6%B1%82)中所规划的 DATA\_CIDR 网段进行设置。

     ```
     iomesh:
       chunk:
         dataCIDR: "" # Fill in the DATA_CIDR you configured previously in Prerequisites.
     ```
   - 设置集群的部署模式 `diskDeploymentMode`：使用全闪或混闪配置。

     系统默认将此字段的值设置为 `hybridFlash`，即混闪配置模式，如果集群部署时采用全闪配置模式，需要将该字段的值修改为 `allFlash`。

     在虚拟机环境上部署 IOMesh 时，建议使用全闪配置模式。

     ```
     diskDeploymentMode: "hybridFlash" # Set the disk deployment mode.
     ```
   - 设置服务器的 CPU 架构。

     如果运行 Kubernetes 集群的服务器为 hygon\_x86\_64 服务器，请将此字段的值设置为 `hygon_x86_64`，否则请留空。

     ```
     platform: ""
     ```
   - 设置 IOMesh 部署的版本：社区版或者企业版。

     系统默认此字段空白，可以指定为 `community`（社区版）或者 `enterprise`（企业版）。如果不指定，系统将自动安装成社区版。

     若您购买的许可为企业版，请将该字段的值设置为 `enterprise`。社区版与企业版的区别可参考 [IOMesh 规格](https://www.iomesh.com/spec)。

     ```
     edition: "" # If left blank, Community Edition will be installed.
     ```
   - （可选）默认部署 3 个 IOMesh chunk pod，如果当前部署的版本为企业版，则支持部署 3 个以上的 chunk pod。

     ```
     iomesh:
       chunk:
         replicaCount: 3 # Specify the number of chunk pods.
     ```
   - （可选）如果期望 IOMesh 只使用部分 Kubernetes 节点的磁盘，请在 `chunk.podPolicy.affinity` 字段配置对应节点标签（label）。例如:

     ```
     iomesh:
       chunk:
         podPolicy:
           affinity:
             nodeAffinity:
               requiredDuringSchedulingIgnoredDuringExecution:
                 nodeSelectorTerms:
                 - matchExpressions:
                   - key: kubernetes.io/hostname 
                     operator: In
                     values:
                     - iomesh-worker-0 # Specify the values of the node label.
                     - iomesh-worker-1
     ```

     建议只配置 `values`，更多的配置信息可参考 [Pod Affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity)。
   - （可选）可以通过配置 `podDeletePolicy` 字段决定 Pod 所在的 Kubernetes 节点发生故障时，系统是否自动删除并在其他健康节点上重新创建该 Pod。此配置仅适用于以下情况的 Pod：必须挂载由 IOMesh 创建的 PVC，并且 PVC 访问模式限定为 `ReadWriteOnce`。

     若未指定该字段，系统默认值为 `no-delete-pod`，即 Pod 所在 Kubernetes 节点发生故障时，系统不会自动删除和重建 Pod。

     ```
     csi-driver:
       driver:
         controller:
           driver:
             podDeletePolicy: "no-delete-pod" # Supports "no-delete-pod", "delete-deployment-pod", "delete-statefulset-pod", or "delete-both-statefulset-and-deployment-pod".
     ```
   - （可选）您可以[配置 LSM 多线程](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/performance-tips#%E9%85%8D%E7%BD%AE-lsm-%E5%A4%9A%E7%BA%BF%E7%A8%8B)、[配置 CPU 核心绑定与独占](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/performance-tips#%E9%85%8D%E7%BD%AE-cpu-%E6%A0%B8%E5%BF%83%E7%BB%91%E5%AE%9A%E4%B8%8E%E7%8B%AC%E5%8D%A0)或[配置常驻缓存](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/performance-tips#%E9%85%8D%E7%BD%AE%E5%B8%B8%E9%A9%BB%E7%BC%93%E5%AD%98)，以优化 IOMesh 集群性能。
   - （可选）当需要使用 IOMesh 作为外部存储时，您可以[配置接入网络](/iomesh_cn/1.2.0/user_guide/advanced-functions/external-storage#%E5%8F%AF%E9%80%89%E9%85%8D%E7%BD%AE%E6%8E%A5%E5%85%A5%E7%BD%91%E7%BB%9C)来对外提供存储服务，以达到更好的存储性能和稳定性。
5. 部署 IOMesh 集群。

   ```
   ./helm install iomesh ./charts/iomesh \
       --create-namespace \
       --namespace iomesh-system \
       --values iomesh.yaml \
       --wait
   ```

   执行完上述命令后，您将看到诸如以下的输出：

   ```
   NAME: iomesh
   LAST DEPLOYED: Wed Jun 30 16:00:32 2021
   NAMESPACE: iomesh-system
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   ```
6. 检查部署结果。

   ```
   kubectl --namespace iomesh-system get pods
   ```

   执行完上述命令后，您将看到如下结果。如果所有 Pod 的状态均显示为 `Running`，则表示 IOMesh 安装成功。

   ```
   NAME                                                   READY   STATUS    RESTARTS      AGE
   iomesh-blockdevice-monitor-5b8b68b5fd-52q6t            1/1     Running   0             77m
   iomesh-blockdevice-monitor-prober-dqcth                1/1     Running   0             77m
   iomesh-blockdevice-monitor-prober-dsftk                1/1     Running   0             77m
   iomesh-blockdevice-monitor-prober-xhkq9                1/1     Running   0             77m
   iomesh-chunk-0                                         3/3     Running   2 (76m ago)   76m
   iomesh-chunk-1                                         3/3     Running   1 (76m ago)   76m
   iomesh-chunk-2                                         3/3     Running   0             76m
   iomesh-csi-driver-controller-plugin-66d7dbf68-65hk8    6/6     Running   0             77m
   iomesh-csi-driver-controller-plugin-66d7dbf68-l54xx    6/6     Running   0             77m
   iomesh-csi-driver-controller-plugin-66d7dbf68-xr6gg    6/6     Running   0             77m
   iomesh-csi-driver-node-plugin-hllf2                    3/3     Running   0             77m
   iomesh-csi-driver-node-plugin-smqld                    3/3     Running   0             77m
   iomesh-csi-driver-node-plugin-wdrxr                    3/3     Running   0             77m
   iomesh-deck-7c4749d7c6-mksxr                           1/1     Running   0             77m
   iomesh-deck-7c4749d7c6-s5bp8                           1/1     Running   0             77m
   iomesh-deck-plugin-iomesh-2s6ds                        1/1     Running   0             77m
   iomesh-deck-plugin-iomesh-s97pp                        1/1     Running   0             77m
   iomesh-deck-plugin-iomesh-xxbrf                        1/1     Running   0             77m
   iomesh-hostpath-provisioner-6wkks                      1/1     Running   0             77m
   iomesh-hostpath-provisioner-m896d                      1/1     Running   0             77m
   iomesh-hostpath-provisioner-qksfs                      1/1     Running   0             77m
   iomesh-iscsi-redirector-pnpz4                          2/2     Running   1 (76m ago)   76m
   iomesh-iscsi-redirector-sdknz                          2/2     Running   1 (76m ago)   76m
   iomesh-iscsi-redirector-ws4m7                          2/2     Running   1 (76m ago)   76m
   iomesh-localpv-manager-p8hdj                           4/4     Running   0             77m
   iomesh-localpv-manager-tzs78                           4/4     Running   0             77m
   iomesh-localpv-manager-xzb6w                           4/4     Running   0             77m
   iomesh-meta-0                                          2/2     Running   0             76m
   iomesh-meta-1                                          2/2     Running   0             76m
   iomesh-meta-2                                          2/2     Running   0             76m
   iomesh-openebs-ndm-cluster-exporter-5767fbbcfc-glfz5   1/1     Running   0             77m
   iomesh-openebs-ndm-node-exporter-9hpdt                 1/1     Running   0             77m
   iomesh-openebs-ndm-node-exporter-f4tvf                 1/1     Running   0             77m
   iomesh-openebs-ndm-node-exporter-x2r4w                 1/1     Running   0             77m
   iomesh-openebs-ndm-operator-646dbc445-j96z8            1/1     Running   0             77m
   iomesh-openebs-ndm-rpts5                               1/1     Running   0             77m
   iomesh-openebs-ndm-v9f27                               1/1     Running   0             77m
   iomesh-openebs-ndm-w5v79                               1/1     Running   0             77m
   iomesh-zookeeper-0                                     1/1     Running   0             77m
   iomesh-zookeeper-1                                     1/1     Running   0             77m
   iomesh-zookeeper-2                                     1/1     Running   0             76m
   iomesh-zookeeper-operator-585f4c89d9-plq9l             1/1     Running   0             77m
   operator-76c7996dbc-6fjdn                              1/1     Running   0             77m
   operator-76c7996dbc-tbpfm                              1/1     Running   0             77m
   operator-76c7996dbc-xqrj7                              1/1     Running   0             77m
   ```

   > **说明：**
   >
   > - 首次安装 IOMesh 时，Kubernetes 集群中所有可调度的节点将自动启动 `prepare-csi` Pod 来安装和设置 `open-iscsi`。若所有节点的 `open-iscsi` 安装成功，系统将自动清理 `prepare-csi` Pod。若某个节点的 `open-iscsi` 安装失败，即 `prepare-csi` Pod 不断失败退出，则可以查看对应 Pod 日志或通过手动[设置 `open-iscsi`](/iomesh_cn/1.2.0/user_guide/appendices/setup-open-iscsi) 来确认 `open-iscsi` 安装失败的原因。
   > - 如果安装 IOMesh 后手动删除了 `open-iscsi`，那么重新安装 IOMesh 时不会自动启动 `prepare-csi` Pod 来自动安装 `open-iscsi`。此时，需要手动[设置 `open-iscsi`](/iomesh_cn/1.2.0/user_guide/appendices/setup-open-iscsi)。
   > - CoreOS 版本的 Linux 操作系统不支持 `prepare-csi`。当 Linux 操作系统的版本为 CoreOS 时，需要手动[设置 `open-iscsi`](/iomesh_cn/1.2.0/user_guide/appendices/setup-open-iscsi)。
   > - IOMesh 安装完成后，其 Chunk、Meta 以及 Zookeeper Pod 将无法切换节点。

---

## 部署 IOMesh 集群 > 访问 Web UI

# 访问 Web UI

IOMesh UI 以 Deployment 的形式部署运行在 Kubernetes 集群内，并暴露一个 Service 对象：

```
kubectl get service -n iomesh-system | grep deck
```

该 Service 对象的类型默认为 `ClusterIP`，您可以使用 `kubectl port-forward` 来对其进行本地访问：

```
kubectl port-forward service/iomesh-deck -n iomesh-system 8080:80
```

此外，您也可以按需配置不同的访问方式，例如 NodePort、LoadBalancer 或 Ingress，以便更灵活地管理和访问服务，参考[设置 UI 访问方式](#%E8%AE%BE%E7%BD%AE-ui-%E8%AE%BF%E9%97%AE%E6%96%B9%E5%BC%8F)。

## 设置 UI 访问方式

### NodePort

您可以选择将 Service 对象的类型变更为 `NodePort`，从而可以通过任意节点的 IP 加端口的方式访问 UI。

**操作步骤**

1. 修改部署 IOMesh 时使用的 Helm values 文件 `iomesh.yaml`，指定 `deck.service.type` 字段值为 `NodePort`。

   ```
   deck:
     service:
       type: NodePort
   ```
2. 执行 `helm upgrade` 命令，使配置生效。

   ```
   helm upgrade iomesh iomesh/iomesh -n iomesh-system -f iomesh.yaml
   ```

### LoadBalancer

和 NodePort 类似的，您也可以选择将 Service 对象的类型变更为 `LoadBalancer`，通过外部分配的负载均衡器 IP 来访问 UI。

**操作步骤**

1. 修改 `iomesh.yaml`，指定 `deck.service.type` 字段值为 `LoadBalancer`。

   ```
   deck:
     service:
       type: LoadBalancer
   ```
2. 执行 `helm upgrade` 命令，使配置生效。

   ```
   helm upgrade iomesh iomesh/iomesh -n iomesh-system -f iomesh.yaml
   ```

### Ingress

如果您的集群已经部署了合适的 Ingress Controller，您也可选择通过 Ingress 来访问 UI。

**操作步骤**

1. 修改 `iomesh.yaml`，参考如下示例配置合适的 `deck.ingress`。

   ```
   deck:
     ingress:
       enabled: true
       className: nginx
       hosts:
       - host: deck.localhost
         paths:
           - path: /
             pathType: ImplementationSpecific
   ```

   > **说明：**
   >
   > 您需要根据集群的 Ingress 实际部署情况来替换 `deck.ingress` 中的各字段。
2. 执行 `helm upgrade` 命令，使配置生效。

   ```
   helm upgrade iomesh iomesh/iomesh -n iomesh-system -f iomesh.yaml
   ```

## 登录 Web UI

IOMesh 部署完成后会为 `admin` 管理员生成随机的初始密码。首次访问 UI 时，您需要使用如下命令获取初始密码。

```
kubectl get secret --namespace iomesh-system bootstrap-secret -o go-template='{{.data.bootstrapPassword|base64decode}}{{"\n"}}'
```

在浏览器中输入访问地址，使用 `admin` 账号及获取的初始密码登录 Web UI，即可管理 IOMesh 集群及其相关资源。

> **注意：**
>
> 强烈建议您在首次登录后，单击页面右上角的**修改密码**修改登录密码，以确保账号的安全性。设置的密码最小长度须为 `8`。

## UI 通用操作

- **更新 YAML**

  支持通过上传 YAML 的方式，在 Kubernetes 集群中创建或更新 YAML 文件。

  > **说明：**
  >
  > 可支持上传的 YAML 文件不限于 IOMesh 本身管理的资源，例如您可以使用该入口创建 Secret。

  **操作步骤**

  1. 单击页面右上角的上传图标，输入 YAML 文件内容。
  2. 单击**创建**或**应用**，创建或更新 YAML 文件。

     - **创建**：在集群中创建新的资源。
     - **应用**：在集群中创建或更新资源。即如果集群中不存在该资源，则创建资源；如果集群中已有该资源，则根据 YAML 内容更新资源。
- **告警**：当您已安装 Prometheus 和 Alertmanager，且[在 UI 中开启监控](/iomesh_cn/1.2.0/user_guide/monitor-iomesh/enable-ui-monitoring)后，单击页面右上角的告警图标，可查看当前 IOMesh 所在 Kubernetes 集群中的所有告警信息。
- **查看事件**：在资源列表的**菜单**列选择**查看事件**，或在资源详情页面选择**查看事件**，可以查看该资源相关的事件。事件的保留时长取决于 Kubernetes 集群的设置。
- **查看 YAML**：在资源列表的**菜单**列选择**查看 YAML**，或在资源详情页面选择**查看 YAML**，可以查看该资源对应的 YAML 文件。通过 `https` 方式访问 UI 时，支持一键复制 YAML 文件的内容。
- **编辑 YAML**：在资源列表的**菜单**列选择**编辑 YAML**，或在资源详情页面选择**编辑 YAML**，可以更新该资源对应的 YAML 文件。
- **删除**：在资源列表的**菜单**列选择**删除**，或在资源详情页面选择**删除**，可以删除资源。

---

## 部署 IOMesh 集群 > 设置 IOMesh

# 设置 IOMesh

安装部署完 IOMesh 后，需要将 Kubernetes Worker 节点上的磁盘（块设备）挂载到 IOMesh 集群，以便由 IOMesh 管理这些磁盘，并为 Kubernetes 集群提供存储服务。

## 查看块设备对象

在 IOMesh 中，每个块设备被视为一个块设备对象。在挂载块设备到 IOMesh 之前，需要确认哪些块设备对象是可用的。

IOMesh 使用 [OpenEBS node-disk-manager(NDM)](https://github.com/openebs/node-disk-manager) 管理 Kubernetes Worker 节点上的磁盘。部署 IOMesh 时，IOMesh 集群所在的名字空间（NameSpace）会同步创建 BlockDevice CR，您可以在该名字空间中查询可使用的块设备。

**操作步骤**

- **命令行方式**

  1. 执行如下命令，查看名字空间中所有的块设备。

     ```
     kubectl --namespace iomesh-system -o wide get blockdevice
     ```

     执行命令后，您将看到如下类似结果：

     ```
     NAME                                           NODENAME             PATH         FSTYPE   SIZE             CLAIMSTATE   STATUS   AGE
     blockdevice-648c1fffeab61e985aa0f8914278e9d0   iomesh-node-17-19    /dev/sda1    ext4     16000900661248   Unclaimed    Active   92d
     blockdevice-648c1fffeab61e985aa0f8914278e9d0   iomesh-node-17-19    /dev/sdb              16000900661248   Unclaimed    Active   92d
     blockdevice-f26f5b30099c20b1f6e993675614c301   iomesh-node-17-18    /dev/sdb              16000900661248   Unclaimed    Active   92d
     blockdevice-8b697bad8a194069fbfd544e6db2ddb8   iomesh-node-17-19    /dev/sdc              16000900661248   Unclaimed    Active   92d
     blockdevice-a3579a64869f799a623d3be86dce7c59   iomesh-node-17-18    /dev/sdc              16000900661248   Unclaimed    Active   92d
     ```

     > **说明：**
     >
     > - 每个 IOMesh 块设备的 `FSTYPE` 字段应该显示为空白。
     > - 只有在磁盘被拔下或插入时，块设备的状态才会更新。因此，如果对磁盘进行了分区或格式化，其状态不会立即更新。要更新磁盘分区和格式化的信息，请执行 `kubectl delete pod -n iomesh-system -l app=openebs-ndm` 命令来重启 NDM Pod，触发磁盘扫描以更新块设备状态。
  2. 执行如下命令，查看每个块设备对象的详细信息，其中 `<block_device_name>` 表示块设备的名称。

     ```
     kubectl --namespace iomesh-system -o yaml get blockdevice <block_device_name>
     ```

     执行上述命令后，您将看到如下类似结果。

     ```
     apiVersion: openebs.io/v1alpha1
     kind: BlockDevice
     metadata:
       annotations:
         internal.openebs.io/uuid-scheme: gpt
       generation: 1
       labels:
         iomesh.com/bd-devicePath: dev.sdb
         iomesh.com/bd-deviceType: disk
         iomesh.com/bd-driverType: SSD
         iomesh.com/bd-serial: 24da000347e1e4a9
         iomesh.com/bd-vendor: ATA
         kubernetes.io/hostname: iomesh-node-17-19
         ndm.io/blockdevice-type: blockdevice
         ndm.io/managed: "true"
       namespace: iomesh-system
       name: blockdevice-648c1fffeab61e985aa0f8914278e9d0
     # ...
     ```

     IOMesh 创建的块设备将带有 `iomesh.com/bd-` 标签，并会被应用于设备选择器。

     | 标签 | 描述 |
     | --- | --- |
     | `iomesh.com/bd-devicePath` | 显示 Worker 节点上的设备路径。 |
     | `iomesh.com/bd-deviceType` | 显示该设备是一块磁盘或分区。 |
     | `iomesh.com/bd-driverType` | 显示磁盘类别，包括 `HDD` 和 `SSD`。 |
     | `iomesh.com/bd-serial` | 显示磁盘序列号。 |
     | `iomesh.com/bd-vendor` | 显示磁盘供应商。 |
- **UI 方式**

  1. 在左侧导航栏中单击**块设备列表**，查看当前 Kubernetes 集群中的所有块设备对象。您可以通过 Namespace 或关键字快速筛选所需块设备。

     | 字段 | 描述 |
     | --- | --- |
     | 名称 | 块设备的名称。 |
     | 名字空间 | 块设备所属的 Namespace。 |
     | IOMesh 集群 | 块设备所属的 IOMesh 集群。  如为 Local PV 挂载的块设备，则该字段为空。 |
     | 节点名称 | 块设备所属的节点名称。 |
     | 类型 | 块设备类型，包括 `HDD` 和 `SDD`。 |
     | 用途 | 块设备的用途，包括 `Datastore`、`Cache with journal` 和 `Datastore with joural`。 |
     | 挂载状态 | 块设备的挂载状态，包括 `Unmounted` 和 `Mounted`。  如为 Local PV 挂载的块设备，则该字段为空。 |
     | 路径 | 块设备的路径，例如 `/dev/vdb`。 |
     | 文件系统类型 | 文件系统类型。 |
     | 容量 | 块设备的容量。 |
     | 申领状态 | 显示是否有块设备声明对应当前块设备，包括 `Claimed`、`Unclaimed` 和 `Released`。 |
     | 状态 | 块设备的状态，包括 `Active` 和 `Inactive`。 |
     | 创建时间 | 块设备被创建出的时长。 |
  2. 单击某一块设备对象的**名称**链接，查看块设备对象的详细信息。

     | 字段 | 描述 |
     | --- | --- |
     | 平均 IOPS | 展示块设备的平均每秒读写次数。 |
     | 平均延迟 | 展示块设备的平均延迟时间。 |
     | 平均吞吐量 | 展示块设备的平均吞吐量。 |
     | 健康状态 | 展示块设备是否为慢盘。 |
     | S.M.A.R.T. | 展示块设备的健康状况，包括温度、读取错误率等指标。 |
     | 剩余寿命 | 展示块设备的预期剩余使用寿命。 |
     | 标签 | 块设备的标签信息。 |
     | 注解 | 块设备的注解信息。 |
     | 属主 | 块设备的所有者。 |
  3. 单击某一块设备对象的**名字空间**、**IOMesh 集群**或**节点名称**链接，可查看相应资源的详细信息。

## 配置设备映射

在配置设备映射（DeviceMap）前，请先了解磁盘的挂载类型和设备选择器。

**挂载类型**

| 部署模式 | 挂载类型 |
| --- | --- |
| 混闪配置 | 必须配置 `cacheWithJournal` 和 `dataStore` 两种挂载类型。   - `cacheWithJournal`：用于存储池的性能层，必须挂载一个可分区的块设备，并且其容量须大于 60 GB。使用此挂载类型时，系统将分别创建一个 `journal` 分区和一个 `cache` 分区。推荐使用 SATA SSD 或 NVMe SSD。 - `dataStore`：用于存储池的容量层。推荐使用 SATA HDD 或 SAS HDD。 |
| 全闪配置 | 只需配置 `dataStoreWithJournal`。  该挂载类型用于存储池的容量层，必须挂载一个可分区的块设备，并且其容量须大于 60 GB。使用此挂载类型时，系统将分别创建一个 `journal` 分区和一个 `dataStore` 分区。推荐使用 SATA SSD 或 NVMe SSD。 |

> **说明：**
>
> 在混闪配置下，不允许挂载未启用 WWN 的磁盘。您可以执行 `udevadm info $devicePath | grep WWN` 命令来查看磁盘是否启用 WWN。

**设备选择器**

| 字段 | 取值 | 描述 |
| --- | --- | --- |
| `selector` | [metav1.LabelSelector](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#labelselector-v1-meta) | 通过标签选择器筛选出可用的块设备。 |
| `include` | 块设备名称（block-device-name） | 选择指定的块设备。 |
| `exclude` | 块设备名称（block-device-name） | 排除指定的块设备。 |

> **说明：**
>
> - 通过设备选择器选择到的块设备范围为 `selector` ∪ `include` - `exclude`。
> - 要获取有关设备选择器的更多详细信息，请访问 [Kubernetes 官网](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)。

**操作步骤**

- **命令行方式**

  1. 通过如下命令编辑 YAML 配置。

     ```
     kubectl edit --namespace iomesh-system iomesh
     ```

     执行完命令后, 定位至 `chunk` 字段:

     ```
     spec:
       chunk:
     ```
  2. 将以下示例代码中的 `deviceMap` 的内容复制并粘贴至 `chunk` 字段下，根据部署模式和块设备信息填写 `mount-type`、`matchLabels`、`matchExpressions`、`include`、`exclude` 字段。块设备标签信息 `<label-key>` 和 `<label-value>` 可参考[查看块设备对象](#%E6%9F%A5%E7%9C%8B%E5%9D%97%E8%AE%BE%E5%A4%87%E5%AF%B9%E8%B1%A1)的步骤 2。

     > **说明：**
     >
     > - 每个 IOMesh 块设备的 `FSTYPE` 字段应为空白。请确保选择的块设备未指定任何文件系统，或在配置 `deviceMap` 时排除已指定文件系统的块设备。
     > - 生产环境中，严禁在 `deviceMap` 中使用盘符，因为磁盘盘符可能会发生变化。

     ```
     spec:
       chunk:
         deviceMap:
           <mount-type>:
             selector:
               matchLabels:
                 <label-key>: <label-value> # Enter key and value as needed.
               matchExpressions:
               - key: <label-key> 
                 operator: In
                 values:
                 - <label-value>
             include:
             - <block-device-name> # Enter the device name to include it.
             exclude:
             - <block-device-name> # Enter the device name to exclude it.
     ```
  3. 验证配置结果。`deviceMap` 配置完成后，执行如下命令，确认目标块设备的 `CLAIMSTATE` 字段更新为 `Claimed`。

     ```
     kubectl --namespace iomesh-system -o wide get blockdevice
     ```

     执行上述命令后，您将看到以下类似结果：

     ```
     NAME                                           NODENAME             PATH         FSTYPE   SIZE             CLAIMSTATE   STATUS   AGE
     blockdevice-f001933979aa613a9c32e552d05a704a   iomesh-node-17-19    /dev/sda1    ext4     16000900661248   Unclaimed    Active   92d
     blockdevice-648c1fffeab61e985aa0f8914278e9d0   iomesh-node-17-19    /dev/sdb              16000900661248   Claimed      Active   92d
     blockdevice-f26f5b30099c20b1f6e993675614c301   iomesh-node-17-18    /dev/sdb              16000900661248   Claimed      Active   92d
     blockdevice-8b697bad8a194069fbfd544e6db2ddb8   iomesh-node-17-19    /dev/sdc              16000900661248   Claimed      Active   92d
     blockdevice-a3579a64869f799a623d3be86dce7c59   iomesh-node-17-18    /dev/sdc              16000900661248   Claimed      Active   92d
     blockdevice-a6652946c90d5c3fca5ca452aac5b826   iomesh-node-17-18    /dev/sdd              16000900661248   Unclaimed    Active   92d
     ```
- **UI 方式**

  1. 在左侧导航栏中单击**块设备列表**。
  2. 找到待挂载的块设备，在**菜单**列选择**挂载**。
  3. 参考挂载类型的说明，设置**用途**。

     - **混闪配置**：可选择 `Datastore` 或 `Cache with journal`。
     - **全闪配置**：自动设置为 `Datastore with joural`。
  4. 单击**挂载**。

     挂载成功后块设备的**挂载状态**为 `Mounted`，**申领状态**为 `Claimed`。

## 设备映射配置示例

下面将提供全闪和混闪两种不同配置的 `deviceMap` 示例。假设一个 Kubernetes 集群有 6 个块设备，详情如下：

```
NAME                                           NODENAME             PATH         FSTYPE   SIZE             CLAIMSTATE   STATUS   AGE
blockdevice-f001933979aa613a9c32e552d05a704a   iomesh-node-17-19    /dev/sda1    ext4     16000900661248   Unclaimed    Active   92d
blockdevice-648c1fffeab61e985aa0f8914278e9d0   iomesh-node-17-19    /dev/sdb              16000900661248   Unclaimed    Active   92d
blockdevice-f26f5b30099c20b1f6e993675614c301   iomesh-node-17-18    /dev/sdb              16000900661248   Unclaimed    Active   92d
blockdevice-8b697bad8a194069fbfd544e6db2ddb8   iomesh-node-17-19    /dev/sdc              16000900661248   Unclaimed    Active   92d
blockdevice-a3579a64869f799a623d3be86dce7c59   iomesh-node-17-18    /dev/sdc              16000900661248   Unclaimed    Active   92d
blockdevice-a6652946c90d5c3fca5ca452aac5b826   iomesh-node-17-18    /dev/sdd              16000900661248   Unclaimed    Active   92d
```

其中 `blockdevice-648c1fffeab61e985aa0f8914278e9d0`、`blockdevice-f26f5b30099c20b1f6e993675614c301`、`blockdevice-a6652946c90d5c3fca5ca452aac5b826` 为 SSD 盘；`blockdevice-f001933979aa613a9c32e552d05a704a`、`blockdevice-8b697bad8a194069fbfd544e6db2ddb8`、`blockdevice-a3579a64869f799a623d3be86dce7c59` 为 HDD 盘。

您可以通过在 `deviceMap` 中匹配块设备标签或直接指定块设备名来选择要在 IOMesh 中使用的块设备，通过筛选的块设备将会被自动挂载至 IOMesh 集群上。

### 混闪设备映射配置示例

如下 `deviceMap` 配置中，将 Kubernetes 集群中所有 SSD 盘用作 `cacheWithJournal`，所有 HDD 盘用作 `dataStore`，并将块设备 `blockdevice-a6652946c90d5c3fca5ca452aac5b826` 和 `blockdevice-f001933979aa613a9c32e552d05a704a` 排除在筛选范围之外。

```
spec:
  # ...
  chunk:
    # ...
    deviceMap:
      cacheWithJournal:
        selector:
          matchLabels:
            iomesh.com/bd-deviceType: disk
          matchExpressions:
          - key: iomesh.com/bd-driverType
            operator: In
            values:
            - SSD
        exclude:
        - blockdevice-a6652946c90d5c3fca5ca452aac5b826
      dataStore:
        selector:
          matchExpressions:
          - key: iomesh.com/bd-driverType
            operator: In
            values:
            - HDD
        exclude:
        - blockdevice-f001933979aa613a9c32e552d05a704a
    # ...
```

若使用上述配置，则之后任何加入节点的 SSD 或 HDD 磁盘都会立即被 IOMesh 纳管。如果您不希望使用这种自动管理行为，也可使用如下配置指定具体的块设备。

```
spec:
  # ...
  chunk:
    # ...
    deviceMap:
      cacheWithJournal:
        include:
        - blockdevice-648c1fffeab61e985aa0f8914278e9d0
        - blockdevice-f26f5b30099c20b1f6e993675614c301
      dataStore:
        include:
        - blockdevice-8b697bad8a194069fbfd544e6db2ddb8
        - blockdevice-a3579a64869f799a623d3be86dce7c59
    # ...
```

### 全闪设备映射配置示例

如下 `deviceMap` 配置中，将 Kubernetes 集群中所有 SSD 盘用作 `dataStoreWithJournal`，并将块设备 `blockdevice-a6652946c90d5c3fca5ca452aac5b826` 排除在筛选范围之外。

```
spec:
  # ...
  chunk:
    # ...
    deviceMap:
      dataStoreWithJournal:
        selector:
          matchLabels:
            iomesh.com/bd-deviceType: disk
          matchExpressions:
          - key: iomesh.com/bd-driverType
            operator: In
            values:
            - SSD
        exclude:
        - blockdevice-a6652946c90d5c3fca5ca452aac5b826
    # ...
```

若使用上述配置，则之后任何加入节点的 SSD 磁盘都会立即被 IOMesh 纳管。如果您不希望使用这种自动管理行为，也可使用如下配置指定具体的块设备。

```
spec:
  # ...
  chunk:
    # ...
    deviceMap:
      dataStoreWithJournal:
        include:
        - blockdevice-648c1fffeab61e985aa0f8914278e9d0
        - blockdevice-f26f5b30099c20b1f6e993675614c301
    # ...
```

---

## 部署 IOMesh 集群 > 激活许可

# 激活许可

IOMesh 提供两个软件版本：社区版和企业版，在首次部署时均默认生成试用许可。您可以将试用许可更新为订阅许可或永久许可。

- 社区版：可更新为永久许可。社区版的永久许可请直接访问 [IOMesh 官网](https://www.iomesh.com/license)免费申请，然后参考以下步骤进行更新。
- 企业版：可更新为订阅许可或永久许可。您可以从 SmartX 客户经理处获取订阅许可或永久许可的许可证码，并按照以下步骤进行更新。

IOMesh 社区版和企业版软件支持的最大 Worker 节点数和商业服务有所不同。

**操作步骤**

- **命令行方式**

  1. 将新的许可证码粘贴并保存在新建的 `license-code.txt` 文件中。
  2. 创建一个 Kubernetes Secret 对象。

     ```
     kubectl create secret generic iomesh-authorization-code -n iomesh-system --from-file=authorizationCode=./license-code.txt
     ```
  3. 执行如下命令，编辑新建的 Kubernetes Secret 对象，并填充 `spec.licenseSecretName` 字段，将其值设置为 `iomesh-authorization-code`。

     ```
     kubectl edit iomesh -n iomesh-system
     ```

     ```
     spec:
       licenseSecretName: iomesh-authorization-code
     ```
  4. 执行如下命令，确认已完成更新。

     ```
     kubectl describe iomesh -n iomesh-system # Whether the update is successful will be displayed in the events.
     ```

     若显示更新失败，请确认保存的许可证码是否正确。若更新再次失败，请重新设置 `spec.licenseSecretName` 字段。
  5. 验证许可证码的过期时间和其他内容是否符合预期。

     ```
     kubectl get iomesh -n iomesh-system -o=jsonpath='{.items[0].status.license}'
     ```
- **UI 方式**

  1. 在左侧导航栏中单击 **IOMesh 集群列表**。
  2. 找到待激活许可的集群，在**菜单**列选择**查看许可证**，将新的许可证码粘贴在**许可证码**区域。
  3. 单击**上传**。

---

## 部署 IOMesh 集群 > 优化 IOMesh 性能

# 优化 IOMesh 性能

## 配置 LSM 多线程

LSM（Local Storage Manager）为 Chunk 内部处理磁盘 I/O 的组件，默认情况下以单线程的形态运行。

如果您对 I/O 延迟和性能上限有更高的要求，并且 Worker 节点有足够的 CPU 资源，可以开启 LSM 多线程，为 Chunk 配置更多的 CPU 核心，以提高系统的并发处理能力。

> **说明：**
>
> - 使用[一键在线安装](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/install-iomesh#%E4%B8%80%E9%94%AE%E5%9C%A8%E7%BA%BF%E5%AE%89%E8%A3%85)的方式部署 IOMesh 时，默认未开启 LSM 多线程，您可以在集群部署完成后单独配置；如使用[自定义在线安装](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/install-iomesh#%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9C%A8%E7%BA%BF%E5%AE%89%E8%A3%85)或[自定义离线安装](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/install-iomesh#%E8%87%AA%E5%AE%9A%E4%B9%89%E7%A6%BB%E7%BA%BF%E5%AE%89%E8%A3%85)，则既可以在部署 IOMesh 的过程中直接配置，也可以在集群部署完成后单独配置。
> - 如您在部署 IOMesh 集群时配置 LSM 多线程，则配置完成后使用 `helm install` 直接进行集群部署即可；如为已部署的 IOMesh 集群，则配置完成后需使用 `helm upgrade` 进行集群配置更新。

**操作步骤**

下面以 IOMesh 集群已部署完成为例进行操作介绍。

1. 修改 `iomesh.yaml`，设置 `iomesh.chunk.extraEnvs` 字段。

   ```
   iomesh:
     chunk:
       extraEnvs:
         LSM_IO_THREAD_NUM: "2" # 配置 LSM 使用的独立线程数量，取值范围为 0-2，如果为 0 则代表不开启 LSM 多线程。
   ```
2. 执行如下命令，Chunk Pod 会逐个重启并生效配置。

   ```
   helm upgrade --namespace <iomeshcluster-namespace> <iomeshcluster-name> iomesh/iomesh --values iomesh.yaml # 根据实际环境替换<xx>
   ```

## 配置 CPU 核心绑定与独占

### 概述

IOMesh 属于性能敏感型应用。在默认情况下，IOMesh Pod 运行时不会绑定在任何 CPU 核心上，此时 IOMesh 虽然可以正常运行，但频繁的 CPU 切换和 CPU cache missing 会导致 IOMesh 性能波动较大，性能上限不理想。

为解决上述问题，IOMesh 提供了**基于 Kubelet CPUManager** 和**基于 Kernel Parameter** 的两种 CPU 核心绑定模式，并且支持所绑定的 CPU 被 IOMesh 独占。

- **Kubelet CPUManager 模式**：直接使用 Kubelet 为 Guaranteed 类型 Pod 预留的核心进行绑定，无需重启 IOMesh Pod 所在的 Kubernetes 节点即可生效。其优点在于操作简便，但缺点是由于 CPU 隔离性差，因此相比于 Kernel Parameter 模式性能较差，并且无法配置具体绑定的 CPU 核心，全部由 Kubelet 动态分配。
- **Kernel Parameter 模式**：支持绑定用户在 Kernel 层面隔离的 CPU 核心。其优点是性能较好、配置灵活，但缺点在于需重启 IOMesh Pod 所在的 Kubernetes 节点。

> **说明：**
>
> - CPU 核心绑定配置仅支持 Cgroup V1。如果您的 Linux 发行版使用了 Cgroup V2，则无法进行 IOMesh 绑核配置。
> - 如果您的集群可以接受 Kubernetes 节点重启，则推荐使用 Kernel Parameter 模式，否则推荐使用 Kubelet CPUManager 模式。
> - 同一时刻仅支持一种 CPU 核心绑定模式。如需要从其中一种模式切换至另一种模式，则需要完全回滚当前模式中所做的配置内容，再配置另一种模式。

### 配置基于 Kubelet CPUManager 的 CPU 核心绑定

> **说明：**
>
> CPU 核心绑定模式默认为 **Kubelet CPUManager**，因此 IOMesh 集群部署完成后直接执行`步骤 1` 设置 Kubelet，即可使核心绑定功能生效。

**操作步骤**

1. 设置 Kubelet 的 `cpuManagerPolicy` 和 `reservedSystemCPUs` 字段。

   依次对所有 Worker 节点执行如下操作：

   1. 执行如下命令，停止 `kebelet` 服务。

      ```
      systemctl stop kubelet
      ```
   2. 执行如下命令，删除当前的 CPU Manager 状态文件。该操作将会清除 CPUManager 维护的状态，以便新策略设置的 cpusets 不会与其冲突。

      ```
      rm /var/lib/kubelet/cpu_manager_state
      ```
   3. 修改 Kubelet 配置文件，增加如下配置。

      ```
      # 该文件路径默认为 /var/lib/kubelet/config.yaml
      cpuManagerPolicy: "static" # 设置为 static，保证 Guarantee 类型的 Pod 可以独占 CPU
      reservedSystemCPUs: "10-13"  # 预留给 K8s 核心服务和系统服务的 CPU 核心，配置方式可参考 https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/
      ```
   4. 启动 kubelet 服务。

      ```
      systemctl start kubelet
      ```
2. 配置 IOMesh 自动绑定 Kubelet 分配的 CPU。

   1. 修改 `iomesh.yaml`，设置 `iomesh.cpuExclusiveOptions.cpuExclusivePolicy` 字段。

      ```
      iomesh:
        cpuExclusiveOptions:
          # Cpu isolation and exclusive policy for IOMesh, support kubeletCpuManager/kernelCpuIsolation/noExclusive. 
          # The default value is kubeletCpuManager
          cpuExclusivePolicy: "kubeletCpuManager"
      ```
   2. 执行如下命令，使配置生效。

      ```
      helm upgrade --namespace <iomeshcluster-namespace> <iomeshcluster-name> iomesh/iomesh --values iomesh.yaml  # 根据实际环境替换<xx>
      ```

### 配置基于 Kernel Parameter 的 CPU 核心绑定

> **说明：**
>
> - 使用[一键在线安装](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/install-iomesh#%E4%B8%80%E9%94%AE%E5%9C%A8%E7%BA%BF%E5%AE%89%E8%A3%85)的方式部署 IOMesh 时，CPU 核心绑定模式默认为 **Kubelet CPUManager**，您可以在集群部署完成后按照如下操作配置为 **Kernel Parameter 模式**；如使用[自定义在线安装](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/install-iomesh#%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9C%A8%E7%BA%BF%E5%AE%89%E8%A3%85)或[自定义离线安装](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/install-iomesh#%E8%87%AA%E5%AE%9A%E4%B9%89%E7%A6%BB%E7%BA%BF%E5%AE%89%E8%A3%85)，则既可以在部署 IOMesh 的过程中直接配置，也可以在集群部署完成后单独配置。
> - 如您在部署 IOMesh 集群时配置 CPU 核心绑定，则配置完成后使用 `helm install` 直接进行集群部署即可；如为已部署的 IOMesh 集群，则配置完成后需使用 `helm upgrade` 进行集群配置更新。

**操作步骤**

下面以 IOMesh 集群已部署完成为例进行操作介绍。

1. 设置 Linux 内核启动参数，配置内核 CPU 隔离。

   > **说明：**
   >
   > 不同 Linux 发行版本，此步骤的操作方法可能会有所不同。

   1. 在 `grub` 配置文件中添加 `isolcpus` 内核启动参数至 `GRUB_CMDLINE_LINUX_DEFAULT` 字段，其值标识要隔离的 CPU。

      默认情况下，IOMesh 需要使用 4 个独占的 CPU 核心。其中，Chunk 服务独占 3 个 CPU，Meta 服务独占 1 个 CPU。当 Chunk 启用了 LSM 多线程后，Chunk 服务需要独占的核心数为 `3 + LSM 线程数`）。

      在以下示例中，假设集群的每个节点有 16 个 CPU 核心，第 0、1、2、10 号 CPU 核心专用于 IOMesh。

      ```
      # 该文件路径默认为 /etc/default/grub
      # 配置格式可参考 https://man7.org/linux/man-pages/man7/cpuset.7.html#FORMATS
      GRUB_CMDLINE_LINUX_DEFAULT="isolcpus=0-2,10"
      ```
   2. 执行如下命令，更新 `grub` 配置。

      ```
      grub2-mkconfig -o $(find /boot -name grub.cfg)
      ```
   3. 执行如下命令，重启集群的每个节点。

      ```
      reboot
      ```
   4. 执行如下命令，验证内核隔离 CPU 是否生效。

      ```
      cat /sys/devices/system/cpu/isolated
      ```

      返回如下内容时，说明配置已生效。

      ```
      0-2,10
      ```
2. 配置 IOMesh 绑定上一步中内核隔离的 CPU。

   1. 修改 `iomesh.yaml`。

      - 设置 `iomesh.cpuExclusiveOptions.cpuExclusivePolicy` 字段为 `kernelCpuIsolation`。
      - 在 `iomesh.cpuExclusiveOptions.exclusiveCpusets` 字段中配置 Chunk 和 Meta 服务独占的 CPU 序号。

      ```
      iomesh:
        cpuExclusiveOptions:
          # Cpu isolation and exclusive policy for IOMesh, support kubeletCpuManager/kernelCpuIsolation/noExclusive. 
          # The default value is kubeletCpuManager
          cpuExclusivePolicy: "kernelCpuIsolation"
          exclusiveCpusets:
            chunk: "0-2"
            meta: "10"
      ```
   2. 执行如下命令，使配置生效。

      ```
      helm upgrade --namespace <iomeshcluster-namespace> <iomeshcluster-name> iomesh/iomesh --values iomesh.yaml  # 根据实际环境替换<xx>
      ```

### 验证 CPU 核心绑定

- 在 Chunk Pod 所在的 Worker 节点上执行如下 `cat` 命令，验证 Chunk 服务是否已绑定到 3 个 CPU 上。

  如下命令的输出结果代表 Chunk 服务已成功绑定在 CPU `0`、`1`、`2` 上。若绑定未生效，则 `cpuset.cpus` 的值为空或提示该文件不存在。

  ```
  # cat /sys/fs/cgroup/cpuset/zbs/chunk-io/cpuset.cpus
  0
  # cat /sys/fs/cgroup/cpuset/zbs/chunk-main/cpuset.cpus
  1
  # cat /sys/fs/cgroup/cpuset/zbs/others/cpuset.cpus
  2
  ```

  如果 Chunk 开启了 LSM 多线程，则您可以通过如下 `cat` 命令验证 LSM 是否使用了独立的 cgroup 配置和核心。

  ```
  # cat /sys/fs/cgroup/cpuset/zbs/lsm-io/cpuset.cpus
  3,4
  ```
- 在 Meta Pod 所在的 Worker 上执行如下 `cat` 命令，验证 Meta 服务是否已绑定到 1 个 CPU 上。

  如下命令的输出结果代表 Meta 服务已成功绑定在 CPU `10` 上。若绑定未生效，则 `cpuset.cpus` 的值为空或提示该文件不存在。

  ```
  # cat /sys/fs/cgroup/cpuset/zbs/meta-main/cpuset.cpus
  10
  ```

## 配置常驻缓存

数据常驻缓存（Pin in Performance）是集群在混闪分层部署模式下可使用的一种存储优化策略。

分层部署的集群在默认情况下，存储卷中具有较高访问频率的数据将停留在速度更快的缓存层，访问频率较低的数据将下沉至速度相对较慢的数据层。在实际场景中，部分应用需要将所有数据始终保留在缓存层中以提供高性能服务。在此场景下，可以为这些应用的存储卷启用常驻缓存模式，将数据始终保留在缓存层。

> **说明：**
>
> 常驻缓存功能仅支持在 IOMesh 部署完成后进行配置。

### 配置 IOMesh 常驻缓存容量预留比例

**操作步骤**

1. 修改 `iomesh.yaml`，设置 `iomesh.chunk.defaultPrioSpaceRatio` 和 `iomesh.chunk.prioritizedSpaceRatioMap` 字段。

   - `prioritizedSpaceRatioMap`：每个节点预留的缓存空间百分比，格式为 `节点的 IOMesh 存储 IP:预留缓存空间百分比`，支持设置比例为 1% ～ 25%。
   - `defaultPrioSpaceRatio`：默认预留的缓存空间百分比，未在 `prioritizedSpaceRatioMap` 中配置预留缓存空间百分比的节点，将使用该字段配置的值，支持设置比例为 1% ～ 25%。

   如下示例表示 10.0.23.17、10.0.23.18、10.0.23.19 节点上分别预留 10%、12%、14% 的缓存空间；未单独配置的其他节点，如 10.0.23.20 节点预留的缓存空间为 5%。

   ```
   iomesh:
     chunk:
       prioritizedSpaceRatioMap:
         10.0.23.17: 10
         10.0.23.18: 12
         10.0.23.19: 14
       defaultPrioSpaceRatio: 5
   ```
2. 执行如下命令使配置生效。

   ```
   helm upgrade --namespace <iomeshcluster-namespace> <iomeshcluster-name> iomesh/iomesh --values iomesh.yaml # 根据实际环境替换<xx>
   ```

### 创建常驻缓存类型的持久卷申领

1. 通过 YAML 文件 `pvc.yaml` 定义一个 PVC，在该 PVC 的 `annotations` 字段中配置 `smartx.com/prioritized` 参数。

   ```
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: pvc-prioritized
     annotations:
        smartx.com/prioritized: "true" # 设为 "true" 表示开启，设为 "false" 表示关闭。支持在创建后更新。
   spec:
     storageClassName: iomesh-csi-driver
     accessModes:
     - ReadWriteOnce
     resources:
       requests:
         storage: 100Gi
     volumeMode: Filesystem
   ```
2. 执行如下命令，使 `pvc.yaml` 文件生效。

   ```
   kubectl apply -f pvc.yaml
   ```
3. 执行如下命令，查看新创建的 PVC。

   ```
   kubectl get pvc pvc-prioritized
   ```

   您将看到如下结果，`STATUS` 为 **Bound** 则表示 PVC 创建成功。

   ```
   NAME              STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS                  AGE
   pvc-prioritized   Bound    pvc-3aef0085-07be-4f32-9e08-681d611c82a5   100Gi      RWO            iomesh-csi-driver             24h
   ```

---

## 卷操作

# 卷操作

介绍创建存储类，创建、扩容和克隆持久卷以及为持久卷提升副本数的操作。

---

## 卷操作 > 创建存储类

# 创建存储类

IOMesh 支持通过动态卷制备的方式为 Pod 创建持久卷（PV）。要使用动态制备功能，您需要预先创建一个或多个存储类（StorageClass）。

IOMesh 提供一个默认的存储类 `iomesh-csi-driver`，您可以使用默认的存储类来创建持久卷，但是不可以修改字段的默认值（见**字段说明**）。也可以通过自定义字段来创建新的存储类，新建的存储类需符合字段说明的描述和取值要求。

支持如下三种类型（Type）：

- IOMesh
- LocalPV (HostPath)
- LocalPV (Device)

本节仅介绍 IOMesh 存储类的创建方式，LocalPV HostPath 存储类和 LocalPV Device 存储类请参考 [IOMesh LocalPV Manager](/iomesh_cn/1.2.0/user_guide/advanced-functions/localpv-manager)。

**字段说明**

| UI 字段 | 对应 YAML 字段 | 描述 | 默认值 |
| --- | --- | --- | --- |
| 名称 | `name` | 存储类的名称。 | `iomesh-csi-driver` |
| 制备器 | `provisioner` | 制备器，用于制备持久卷。 | `com.iomesh.csi-driver` |
| IOMesh 集群名称 | `meta.helm.sh/release-namespace`/ `meta.helm.sh/release-name` | 存储类所在的 IOMesh 集群。 | `iomesh-system/iomesh` |
| 卷绑定模式 | `volumeBindingMode` | PV 的绑定模式：   - `Immediate`：在创建 PVC 后，制备器会立即动态制备一个 PV 与 该 PVC 绑定。 - `WaitForFirstConsumerPV`​：在创建 PVC 后，制备器会等到有 Pod 指定该 PVC 后动态制备一个 PV 与该 PVC 绑定。 | `Immediate` |
| 冗余机制（副本） | `replicaFactor` | PV 的副本数量：`2` 或 `3` | `2` |
| 冗余机制（纠删码） | `ec_k` 和 `ec_m` | PV 的纠删码配置。设置该参数时，`replicatorFactor` 参数无效。 |  |
| 文件系统类型 | `csi.storage.k8s.io/fstype` | 支持的文件系统类型：   - `xfs` - `ext2` - `ext3` - `ext4` | `ext4` |
| IOPS 限制 | `smartx.com/iops` | PV 的 IOPS 限制。  可手动设置为 `0` 或大于等于 `50` 的整数，不配置或配置为 `0` 表示无 IOPS 限制。 | `0` |
| BPS 限制 | `smartx.com/bps` | PV 的带宽限制。  可手动设置为 `0` 或大于等于 `10Mi` 的整数或小数，不配置或配置为 `0` 表示无带宽限制。  存储容量单位必须为二进制或十进制，如 Gi/Mi 或 G/M。 | `0` |
| 精简置备 | `thinProvision` | 置备类型：   - `true`：精简置备 - `false`：厚置备 | `true` |
| 允许卷扩容 | `allowVolumeExpansion` | 是否允许卷扩容。 | `true` |
| 回收策略 | `reclaimPolicy` | 当 PVC 被删除时，此字段决定了是否保留 PV。   - `Retain`：删除 PVC 时，将会保留 PV 和对应的 IOMesh 卷。 - `Delete`：删除 PVC 时，PV 和相应的 IOMesh 卷将同时被删除。 | `delete` |
| -（不支持） | `enableClusterTopology` | 是否开启集群 topo 功能。  `true` 表示开启，开启后使用 IOMesh PVC 的 Pod 会被强制调度到对应 IOMesh 集群 Chunk Pod 所在节点上以实现最佳性能。 | `false` |

**操作步骤**

- **命令行方式**

  1. 通过 YAML 文件 `sc.yaml` 定义一个存储类，该存储类的字段取值如下。

     ```
     kind: StorageClass
     apiVersion: storage.k8s.io/v1
     metadata:
       name: iomesh-example-sc 
     provisioner: com.iomesh.csi-driver 
     reclaimPolicy: Delete # Specify the reclaim policy.
     allowVolumeExpansion: true 
     parameters:
       # Specify the filesystem type, including "ext4", "ext3", "ext2", and "xfs".
       csi.storage.k8s.io/fstype: "ext4"
       # Specify the replication factor, either "2" or "3".
       replicaFactor: "2"
       # Specify the provisioning type.
       thinProvision: "true"
     volumeBindingMode: Immediate
     ```
  2. 执行如下命令，使 `sc.yaml` 文件生效，系统自动创建一个存储类。

     ```
     kubectl apply -f sc.yaml
     ```
  3. 执行如下命令，查看新创建的存储类。

     ```
     kubectl get storageclass iomesh-example-sc
     ```

     执行上述命令后，您将看到如下结果，表明该存储类创建成功。

     ```
     NAME                  PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
     iomesh-example-sc     com.iomesh.csi-driver   Delete          Immediate           true                   24h
     ```
- **UI 方式**

  1. 在左侧导航栏中单击**存储类列表**。
  2. 单击 **+**。
  3. 设置存储类的**名称**，**类型**选择 **IOMesh**，并参考字段说明完成其他字段值的设置。
  4. 单击**创建**。

     创建完成后，您可以在**存储类列表**页面中查看已创建存储类的信息。

     - 单击某一存储类的**名称**链接，可查看该存储类的详细信息，以及相关的持久卷和持久卷申领信息。
     - 单击 **IOMesh 集群**链接，可跳转至 IOMesh 集群的详细信息页面。

---

## 卷操作 > 创建持久卷 > 创建普通持久卷

# 创建普通持久卷

IOMesh 支持通过创建一个带有特定存储容量和访问模式需求的持久卷申领（PersistentVolumeClaim，PVC）对象动态制备一个持久卷（PersistentVolume，PV），并将此 PVC 和 PV 绑定。

支持如下三种 PVC：

- IOMesh PVC（IOMesh 持久卷申领）
- LocalPV HostPath PVC（本地主机路径持久卷申领）
- LocalPV Device PVC（本地块设备持久卷申领）

本节仅介绍 IOMesh PVC 的创建方式，LocalPV HostPath PVC 和 LocalPV Device PVC 请参考 [IOMesh LocalPV Manager](/iomesh_cn/1.2.0/user_guide/advanced-functions/localpv-manager)。

**前提条件**

必须确保集群存在至少一个存储类。

**PVC 字段说明**

| UI 字段 | 对应 YAML 字段 | 描述 |
| --- | --- | --- |
| 名称 | `name` | PVC 的名称。 |
| 名字空间 | `namespace` | PVC 所属的名字空间。  使用该 PVC 的业务 Pod 需和 PVC 在同一名字空间才能挂载。 |
| 存储类名称 | `storageClassName` | PVC 使用的存储类。 |
| 卷模式 | `volumeMode` | PVC 使用的卷模式，包括 `Block` 和 `Filesystem`。 |
| 容量 | `capacity/storage` | PVC 的存储容量，单位为 Gi 或 Ti，大小必须为 2Gi 的整数倍。 |
| 访问模式 | `accessModes` | PVC 的访问模式，包括 `ReadWriteOnce`、`ReadOnlyMany` 和 `ReadWriteMany`。  **注意：**当 PV 以块（Block）的卷模式（volumeMode）挂载到 Pod 时，三种访问模式均可支持；当 PV 以文件系统（filesystem）的卷模式（volumeMode）挂载到 Pod 时，仅支持 `ReadWriteOnce`。 |
| 常驻缓存 | `annotations.smartx.com/prioritized` | PVC 是否开启常驻缓存特性。 |

其他字段说明请分别参考[创建具有 QoS 限速功能的持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/pv-qos)、[创建具有身份验证功能的持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/encrypt-pv)、[使用 PVC 创建 iSCSI LUN](/iomesh_cn/1.2.0/user_guide/advanced-functions/external-storage#%E4%BD%BF%E7%94%A8-pvc-%E5%88%9B%E5%BB%BA-iscsi-lun)和[创建常驻缓存类型的持久卷申领](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/performance-tips#%E5%88%9B%E5%BB%BA%E5%B8%B8%E9%A9%BB%E7%BC%93%E5%AD%98%E7%B1%BB%E5%9E%8B%E7%9A%84%E6%8C%81%E4%B9%85%E5%8D%B7%E7%94%B3%E9%A2%86)。

**操作步骤**

- **命令行方式**

  1. 通过 YAML 文件 `pvc.yaml` 定义一个 PVC，明确 PVC 的访问模式、存储容量和卷模式。

     ```
     apiVersion: v1
     kind: PersistentVolumeClaim
     metadata:
       name: iomesh-example-pvc
     spec:
       storageClassName: iomesh-csi-driver
       accessModes:
         - ReadWriteOnce # Specify the access mode. 
       resources:
         requests:
           storage: 10Gi # Specify the storage value, must be multiple of 2Gi.
       volumeMode: Filesystem # Specify the volume mode.
     ```

     更多细节请参考 [Kubernetes Documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)。
  2. 执行如下命令，使 `pvc.yaml` 文件生效，系统自动创建一个 PVC 和 PV。

     ```
     kubectl apply -f pvc.yaml
     ```
  3. 执行如下命令，查看新创建的 PVC，其中 `iomesh-example-pvc` 为 PVC 的名称。

     ```
     kubectl get pvc iomesh-example-pvc
     ```

     执行上述命令后，您将看到如下结果，`VOLUME` 列显示的即为新创建的 PV 的名称。

     ```
     NAME                                        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS        AGE
     iomesh-example-pvc                          Bound    pvc-34230f3f-47dc-46e8-8c42-38c073c40598   10Gi        RWO            iomesh-csi-driver   21h
     ```
  4. 执行如下命令，查看 PV 的详细信息。

     ```
     kubectl get pv pvc-34230f3f-47dc-46e8-8c42-38c073c40598
     ```

     执行上述命令后，您将看到如下结果，表明 PV 创建成功。

     ```
     NAME                                       CAPACITY   RECLAIM POLICY   STATUS   CLAIM                        STORAGECLASS
     pvc-34230f3f-47dc-46e8-8c42-38c073c40598   10Gi       Delete           Bound    default/iomesh-example-pvc   iomesh-csi-driver
     ```
- **UI 方式**

  1. 在左侧导航栏中单击**持久卷申领列表**。
  2. 单击 **+** > **新建 IOMesh 持久卷申领**。
  3. 参考字段说明设置相关字段的值。
  4. 单击**创建**。

     当**状态**为 `Bound` 时，表示 PVC 和 PV 已创建成功。

     您可以在**持久卷申领列表**页面中查看已创建 PVC 的信息。

     | 字段 | 描述 |
     | --- | --- |
     | 状态 | PVC 的状态，包括 `Pending`、`Bound` 和 `Lost`。 |
     | 卷 | PVC 关联的 PV 名称。 |
     | 创建时间 | PVC 被创建出的时长。 |

     - 单击某一 PVC 的**名称**链接，可查看该 PVC 的详细信息，以及相关的 Pods 和卷快照信息。
     - 单击**名字空间**链接，可查看名字空间的详细信息。
     - 单击**卷**链接，可查看自动创建的 PV 的详细信息。
     - 单击**存储类**链接，可查看存储类的详细信息。
  5. 在左侧导航栏中单击**持久卷列表**，可查看自动生成的 PV 的相关信息。

     - **列表**：部分字段介绍如下，其余与 PVC 类似，不再赘述。

       | 字段 | 描述 |
       | --- | --- |
       | 状态 | PV 的状态，包括 `Available`、`Bound`、`Released` 和 `Failed`。 |
       | 申领 | PV 对应的 PVC 的名称。 |
       | 已使用容量 | PV 已使用逻辑容量。 |
       | 独占容量 | PV 独占逻辑容量。 |
       | 共享容量 | PV 共享逻辑容量。 |
       | 理由 | PV 的故障描述。 |
     - **详细信息**：支持查看 PV 的基本信息和监控图表。

       > **说明：**
       >
       > 仅当 PV 所属的 IOMesh 集群可以访问 Promethues 时，可获取监控图表数据。

       | 图表 | 描述 |
       | --- | --- |
       | IOPS | 展示 PV 过去 2 小时内的总 IOPS、读 IOPS 和写 IOPS。 |
       | I/O 带宽 | 展示 PV 过去 2 小时内的总带宽、读带宽和写带宽。 |
       | I/O 平均延迟 | 展示 PV 过去 2 小时内的总平均延迟、读平均延迟和写平均延迟。 |
       | I/O 平均块大小 | 展示 PV 过去 2 小时内的总平均块大小、读平均块大小和写平均块大小。 |

---

## 卷操作 > 创建持久卷 > 创建具有 QoS 限速功能的持久卷

# 创建具有 QoS 限速功能的持久卷

使用 iSCSI 协议类型的存储类（StorageClass）制备持久卷（PV）时，IOMesh 支持对 PV 的 IOPS 和带宽进行限制，以创建一个具有 QoS 限速功能的 PV。

支持通过以下两种方式在创建 PV 时配置 QoS：

- 若您需要创建多个具有 QoS 限速功能的 PV，且每个 PV 的 QoS 限速相同，则建议[使用已配置 QoS 限速的存储类来创建持久卷](#%E4%BD%BF%E7%94%A8%E5%B7%B2%E9%85%8D%E7%BD%AE-qos-%E9%99%90%E9%80%9F%E7%9A%84%E5%AD%98%E5%82%A8%E7%B1%BB%E5%88%9B%E5%BB%BA%E6%8C%81%E4%B9%85%E5%8D%B7)。即在创建 StorageClass 时，统一配置 QoS IOPS 或 QoS BPS。
- 若您需要[创建单个具有 QoS 限速功能的持久卷](#%E5%88%9B%E5%BB%BA%E5%8D%95%E4%B8%AA%E5%85%B7%E6%9C%89-qos-%E9%99%90%E9%80%9F%E5%8A%9F%E8%83%BD%E7%9A%84%E6%8C%81%E4%B9%85%E5%8D%B7)，则建议在创建 PVC 时直接配置 QoS IOPS 或 QoS BPS。

**注意事项**

创建的 PV 的容量必须为 2Gi 的整数倍。

**字段说明**

| UI 字段 | 对应 YAML 字段 | 描述 |
| --- | --- | --- |
| IOPS 限制 | `smartx.com/iops` | PV 的 IOPS 限制。  可手动设置为 `0` 或大于等于 `50` 的整数，不配置或配置为 `0` 表示无 IOPS 限制。 |
| BPS 限制 | `smartx.com/bps` | PV 的带宽限制。  可手动设置为 `0` 或大于等于 `10Mi` 的整数或小数，不配置或配置为 `0` 表示无带宽限制。  存储容量单位必须为二进制或十进制，如 Gi/Mi 或 G/M。 |

其余字段请参考[创建普通持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/create-pv)。

## 使用已配置 QoS 限速的存储类创建持久卷

- **命令行方式**

  1. 在 `parameters` 字段中配置 `smartx.com/iops` 和 `smartx.com/bps` 参数，通过 YAML 文件 `sc-qos.yaml` 定义一个具有 QoS 限速功能的存储类。其他字段说明请参考[创建存储类](/iomesh_cn/1.2.0/user_guide/volume-operations/create-storageclass)。

     ```
     kind: StorageClass
     apiVersion: storage.k8s.io/v1
     metadata:
       name: iomesh-qos                   # The StorageClass name.
     provisioner: com.iomesh.csi-driver 
     reclaimPolicy: Delete                # Specify the reclaim policy.
     allowVolumeExpansion: true 
     parameters:
       csi.storage.k8s.io/fstype: "ext4"  # "ext4" / "xfs" 
       replicaFactor: "2"                 # "2" / "3"
       thinProvision: "true"              # "true" / "false"
       protocol: iscsi                    # "iscsi" / "nvmf"
       smartx.com/iops: "1000"             # volume iops    
       smartx.com/bps: "100Mi"             # volume bps
     volumeBindingMode: Immediate
     ```
  2. 执行如下命令，使 `sc-qos.yaml` 文件生效。

     ```
     kubectl apply -f sc-qos.yaml
     ```
  3. 通过 YAML 文件 `pvc.yaml` 定义一个使用该存储类的 PVC。

     ```
     apiVersion: v1
     kind: PersistentVolumeClaim
     metadata:
       name: pvc-qos-with-sc
     spec:
       storageClassName: iomesh-qos
       accessModes:
       - ReadWriteOnce
       resources:
         requests:
           storage: 100Gi
       volumeMode: Filesystem
     ```
  4. 执行如下命令，使 `pvc.yaml` 文件生效，系统自动创建一个 PVC 和具有 QoS 限速功能的 PV。

     ```
     kubectl apply -f pvc.yaml
     ```
- **UI 方式**

  1. 在左侧导航栏中单击**存储类列表**，单击 **+**。
  2. **类型**选择 `IOMesh`，设置 **IOPS 限制**或 **BPS 限制**，其他字段说明请参考[创建存储类](/iomesh_cn/1.2.0/user_guide/volume-operations/create-storageclass)。
  3. 单击**创建**，创建一个具有 QoS 限速功能的存储类。
  4. 在左侧导航栏中单击**持久卷申领列表**，单击 **+** > **新建 IOMesh 持久卷申领**。
  5. 选择上一步中创建的存储类。其它字段说明请参考[创建普通持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/create-pv)。
  6. 单击**创建**，创建一个 PVC 和具有 QoS 限速功能的 PV。

## 创建单个具有 QoS 限速功能的持久卷

- **命令行方式**

  1. 通过 YAML 文件 `pvc.yaml` 定义一个 PVC，并在 `annotations` 字段中配置 `smartx.com/iops` 和 `smartx.com/bps` 参数。

     ```
       apiVersion: v1
       kind: PersistentVolumeClaim
       metadata:
         name: pvc-qos
         annotations:
           smartx.com/iops: "1000"
           smartx.com/bps: "1000Mi"
       spec:
         storageClassName: <storageClassName> # 此处替换为具体的 StorageClass
         accessModes:
         - ReadWriteOnce
         resources:
           requests:
             storage: 100Gi
         volumeMode: Filesystem
     ```

     > **说明：**
     >
     > 若 PVC 所指定的 StorageClass 已配置 QoS 限速，且同时在 PVC 中配置了 `smartx.com/iops` 或 `smartx.com/bps` 参数，则最终创建的 PV 的 QoS 限速参数将取二者并集，重复配置的参数以 PVC 中设置的参数值为准。
     > 例如，在 StorageClass 中定义了 `smartx.com/iops: "500"` 和 `smartx.com/bps: "1000Mi"`，在 PVC 中定义了 `smartx.com/iops: "1000"`，则最终 PV 的 QoS 限速参数为 `smartx.com/iops: "1000"` 和 `smartx.com/bps: "1000Mi"`。
  2. 执行如下命令，使 `pvc.yaml` 文件生效，系统自动创建一个 PVC 和具有 QoS 限速功能的 PV。

     ```
     kubectl apply -f pvc.yaml
     ```
- **UI 方式**

  1. 在左侧导航栏中单击**持久卷申领列表**，单击 **+** > **新建 IOMesh 持久卷申领**。
  2. 设置 **IOPS 限制**或 **BPS 限制**，其他字段说明请参考[创建普通持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/create-pv)。

     > **说明：**
     >
     > 若 PVC 所指定的存储类已配置 QoS 限速，且同时在 PVC 中配置了 IOPS 限制或 BPS 限制，则最终创建的 PV 的 QoS 限速参数将取二者并集，重复配置的参数以 PVC 中设置的参数值为准。
     > 例如，在存储类中定义了 IOPS 限制为 `500`、BPS 限制为 `1000Mi`，在 PVC 中定义了 IOPS 限制为 `1000`，则最终 PV 的 IOPS 限制为 `1000`、BPS 限制为 `1000Mi`。
  3. 单击**创建**，创建一个 PVC 和具有 QoS 限速功能的 PV。
  4. 在左侧导航栏中单击**持久卷申领列表**，可查看自动生成的 PV 的相关信息。

---

## 卷操作 > 创建持久卷 > 创建具有身份验证功能的持久卷

# 创建具有身份验证功能的持久卷

IOMesh 允许使用 Kubernetes Secret 进行身份验证。身份验证功能通过存储类实现，要求在存储类中配置一个用于验证身份的 Secret 和一个带有身份认证信息的 Secret。每次 Pod 声明使用身份验证的 PVC 时，只有认证通过（两个 Secret 的数据完全匹配），该 PVC 才能被 Pod 正确使用。

**前提条件**

- 由于认证是通过 iSCSI CHAP 实现，根据 CHAP 协议的密码长度要求，Secret 的密码字符长度必须介于 12 ～ 16 之间。
- 为了确保已配置身份验证的存储类只被特定的用户访问，使用基于角色的访问控制（RBAC）很有必要。因为存储类不是一个仅限于特定名字空间的对象，而某些版本的 Kubernetes 允许所有名字空间的用户访问存储类。

**注意事项**

创建的 PV 的容量必须为 2Gi 的整数倍。

**字段说明**

| UI 字段 | 对应 YAML 字段 | 描述 |
| --- | --- | --- |
| 认证 Secret 名称 | `iomesh.com/key` | 仅当选择了启用了 PV 身份认证功能的存储类时才需要填写用于身份验证的 Secret，留空表示不为 PVC 配置验证信息。 |

其余字段请参考[创建普通持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/create-pv)。

**操作步骤**

1. 创建一个用于 PV 身份验证的 Secret。

   在下面的命令中，使用实际的用户名替换 `iomesh`，使用 IOMesh 集群所在的名字空间替换 `iomesh-system`，使用实际的密码替换 `abcdefghijklmn`。

   ```
   kubectl create secret generic volume-secret -n iomesh-system --from-literal=username=iomesh --from-literal=password=abcdefghijklmn
   ```
2. 创建一个带有身份认证信息的 Secret，其用户名和密码与步骤 1 中的 Secret 保持一致。

   ```
   kubectl create secret generic user-secret -n user-namespace --from-literal=username=iomesh --from-literal=password=abcdefghijklmn
   ```
3. 创建一个存储类，启用 PV 身份认证功能，并遵照下面的提示指定 Secret。

   > **说明：**
   >
   > 在**存储类列表**页面单击 **+** 创建存储类时，暂不支持启用 PV 身份认证功能。您可以通过命令行方式创建存储类，也可以在 UI 中通过**更新 YAML** 的方式创建存储类。

   ```
   # Source: authenticate-sc.yaml
   kind: StorageClass
   apiVersion: storage.k8s.io/v1
   metadata:
     name: per-storageclass-auth
   provisioner: com.iomesh.csi-driver
   reclaimPolicy: Delete
   allowVolumeExpansion: true
   parameters:
     csi.storage.k8s.io/fstype: "ext4"
     replicaFactor: "2"
     thinProvision: "true"
     # Enable PV authentication.
     auth: "true"
     # The secret for PV authentication.
     csi.storage.k8s.io/controller-publish-secret-name: volume-secret
     csi.storage.k8s.io/controller-publish-secret-namespace: iomesh-system
     # The secret that provides authentication information, which will be fetched from the `annotation` field of the PVC.
     csi.storage.k8s.io/node-stage-secret-name: ${pvc.annotations['iomesh.com/key']}
     csi.storage.k8s.io/node-stage-secret-namespace: ${pvc.namespace}
   ```

   ```
   kubectl apply -f authenticate-sc.yaml
   ```

   | 字段 | 描述 |
   | --- | --- |
   | `csi.storage.k8s.io/controller-publish-secret-name` | 步骤 1 中创建的用于身份认证的 Secret。 |
   | `csi.storage.k8s.io/controller-publish-secret-namespace` | 步骤 1 中创建的用于身份认证的 Secret 所在的名字空间。 |
   | `csi.storage.k8s.io/node-stage-secret-name` | 步骤 2 中创建的带有身份认证信息的 Secret。 |
   | `csi.storage.k8s.io/node-stage-secret-namespace` | 步骤 2 中创建的带有身份认证信息的 Secret 所在的名字空间。 |
4. 创建一个 PVC，并设置用于身份验证的 Secret。

   - **命令行方式**

     1. 通过 YAML 文件 `authenticate-pvc.yaml` 定义 PVC，指定 `annotations.iomesh.com/key` 字段的值为步骤 2 中创建的 Secret。

        ```
        # Source: authenticate-pvc.yaml
        kind: PersistentVolumeClaim
        apiVersion: v1
        metadata:
          name: user-pvc
          namespace: user-namespace
          # Specify the secret created in Step 2.
          annotations:
            iomesh.com/key: user-secret
        spec:
          storageClassName: per-storageclass-auth
          accessModes:
          - ReadWriteOnce
          resources:
            requests:
              storage: 2Gi
        ```
     2. 执行如下命令，使 `authenticate-pvc.yaml` 文件生效，系统自动创建一个 PVC 和具有身份验证功能的 PV。

        ```
        kubectl apply -f authenticate-pvc.yaml
        ```
   - **UI 方式**

     1. 在左侧导航栏中单击**持久卷申领列表**。
     2. 单击 **+** > **新建 IOMesh 持久卷申领**。
     3. 在**认证 Secret 名称**中设置步骤 2 中创建的 Secret，其他字段说明请参考[创建普通持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/create-pv)。
     4. 单击**创建**，系统自动创建一个 PVC 和具有身份验证功能的 PV。
     5. 在左侧导航栏中单击**持久卷列表**，可查看自动生成的 PV 的相关信息。

---

## 卷操作 > 扩容持久卷

# 扩容持久卷

在 YAML 中修改该持久卷对应的持久卷申领（PVC）中的 `storage` 字段或者在 UI 中对持久卷申领扩容，即可扩容持久卷。

**前提条件**

待扩容持久卷所对应的存储类类型须为 `IOMesh`，且 `allowVolumeExpansion`（允许卷扩容）字段需设置为 `true`。

- IOMesh 提供的默认存储类 `iomesh-csi-driver` 的 `allowVolumeExpansion` 的取值为 `true`。
- 若您创建了一个自定义参数的存储类，请确保其 `allowVolumeExpansion`（允许卷扩容）字段被设置为 `true`。

**注意事项**

扩容后的 PV 的容量必须为 2Gi 的整数倍。

**操作步骤**

- **命令行方式**

  下面以一个通过 YAML 文件 `pvc.yaml` 定义的 PVC 为例，描述扩容 PV 的操作步骤。该 PVC 的名称为 `iomesh-example-pvc`，容量为 `10Gi`。

  ```
  apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    name: iomesh-example-pvc
  spec:
    storageClassName: iomesh-csi-driver
    accessModes:
      - ReadWriteOnce
    resources:
      requests:
        storage: 10Gi # The original capacity of the PVC, must be multiple of 2Gi.
  ```

  1. 执行如下命令，查看待修改容量的 PVC。

     ```
     kubectl get pvc iomesh-example-pvc
     ```

     执行上述命令后，您将看到如下结果，`VOLUME` 和 `CAPACITY` 列显示的即为此 PVC 对应的 PV 的名称和容量。

     ```
     NAME                 STATUS   VOLUME                                     CAPACITY    ACCESS MODES   STORAGECLASS                AGE
     iomesh-example-pvc   Bound    pvc-b2fc8425-9dbc-4204-8240-41cb4a7fa8ca   10Gi        RWO            iomesh-csi-driver           11m
     ```
  2. 访问并修改 `pvc.yaml` 文件，为 `storage` 字段设置一个新的值。

     ```
     apiVersion: v1
     kind: PersistentVolumeClaim
     metadata:
       name: iomesh-example-pvc
     spec:
       storageClassName: iomesh-csi-driver
       accessModes:
         - ReadWriteOnce
       resources:
         requests:
           storage: 20Gi # Enter a new value greater than the original value, must be multiple of 2Gi.
     ```
  3. 执行如下命令，使修改后的 `pvc.yaml` 文件生效。

     ```
     kubectl apply -f pvc.yaml
     ```
  4. 执行如下命令，查看修改后的 PVC 的详细信息，以及对应的 PV。

     > **说明：**
     >
     > 修改 `pvc.yaml` 文件的 `storage` 字段后，系统将修改 PV 的容量，但不调整 PVC 的容量。只有 Pod 使用此 PVC 时，PVC 的容量才会自动调整。

     ```
     kubectl get pvc iomesh-example-pvc
     ```

     执行上述命令后，您将看到如下结果。

     ```
     NAME                 STATUS   VOLUME                                     CAPACITY    ACCESS MODES   STORAGECLASS                AGE
     iomesh-example-pvc   Bound    pvc-b2fc8425-9dbc-4204-8240-41cb4a7fa8ca   10Gi        RWO            iomesh-csi-driver           11m
     ```
  5. 执行如下命令，确认 PV 是否已扩容。您可从上一步骤的输出中，获取 PV 的名称。

     ```
     kubectl get pv pvc-b2fc8425-9dbc-4204-8240-41cb4a7fa8ca # The PV name you get in Step 4.
     ```

     其输出的信息如下所示，PV 的容量已经修改为 `20Gi`。

     ```
     NAME                                       CAPACITY   RECLAIM POLICY   STATUS   CLAIM                       STORAGECLASS
     pvc-b2fc8425-9dbc-4204-8240-41cb4a7fa8ca   20Gi       Delete           Bound    default/iomesh-example-pvc  iomesh-csi-driver
     ```
- **UI 方式**

  1. 在左侧导航栏中单击**持久卷申领列表**。
  2. 找到待扩容的 PVC，在**菜单**列选择**扩容**。
  3. 设置**新容量**。该值需大于扩容前的原分配容量，且大小必须为 2Gi 的整数倍，单位可填写 Gi 或 Ti。
  4. 单击**扩容**。

     > **说明：**
     >
     > 扩容后系统将修改 PV 的容量，但不调整 PVC 的容量。只有 Pod 使用此 PVC 时，PVC 的容量才会自动调整。
  5. 在左侧导航栏中单击**持久卷列表**，验证相应 PV 的**容量**是否修改成功。

---

## 卷操作 > 克隆持久卷

# 克隆持久卷

要克隆一个持久卷，您可以通过创建一个新的 PVC，并在 `dataSource` 字段中指定该值为待克隆的持久卷所对应的 PVC 来实现。

**注意事项**

- 源 PVC 和目标 PVC 必须在同一个名字空间中。
- 源 PVC 和目标 PVC 的存储类和卷模式的设置必须相同。
- 目标 PVC 与源 PVC 的容量必须相同。
- 通过命令行方式对具有 QoS 限速功能的持久卷进⾏克隆时，新⽣成的 PVC 将不包含源 PVC 的 QoS 相关配置，即不进行 QoS 限速。
  通过命令行方式对常驻缓存的持久卷进⾏克隆时，新⽣成的 PVC 默认不包含常驻缓存属性，但可以通过配置 annotation 的方式指定克隆出一个常驻缓存的持久卷。

**前提条件**

克隆持久卷前必须已经存在一个 PVC，且 PVC 使用的存储类类型须为 `IOMesh`。

**操作步骤**

- **命令行方式**

  1. 通过 YAML 文件 `clone.yaml` 定义一个 PVC，指定其源 PVC 的名称为 `existing-pvc`（`dataSource` 的 `name` 字段），克隆后的 PVC 名称为 `cloned-pvc`，容量为 `10Gi`。

     ```
     apiVersion: v1
     kind: PersistentVolumeClaim
     metadata:
       name: cloned-pvc
     spec:
       storageClassName: iomesh-csi-driver # The StorageClass must be the same as that of the source PVC.
       dataSource:
         name: iomesh-example-pvc # Specify the source PVC that should be from the same namespace as the target PVC. 
         kind: PersistentVolumeClaim
       accessModes:
         - ReadWriteOnce
       resources:
         requests:
           storage: 10Gi # The capacity value must be the same as that of the source volume.
       volumeMode: Filesystem # The volume mode must be the same as that of the source PVC.
     ```
  2. 执行如下命令，使 `clone.yaml` 文件生效，系统自动克隆出一个 PVC `cloned-pvc` 和对应的 PV。

     ```
     kubectl apply -f clone.yaml
     ```
  3. 执行如下命令，查看新克隆的 PVC。

     ```
     kubectl get pvc cloned-pvc
     ```

     执行完命令后，您将看到如下结果，`VOLUME` 列显示的即为新克隆的 PV 的名称。

     ```
     NAME                                        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS        AGE
     cloned-pvc                                  Bound    pvc-161b8c15-3b9f-4742-95db-dcd69c9a2931   10Gi        RWO            iomesh-csi-driver   12s
     ```
  4. 执行如下命令，查看克隆的 PV 的详细信息。

     ```
     kubectl get pv pvc-161b8c15-3b9f-4742-95db-dcd69c9a2931 # The PV name you get in Step 3.
     ```

     执行上述命令后，您将看到如下结果，表明 PV 克隆成功。

     ```
      NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                STORAGECLASS        REASON   AGE
      pvc-161b8c15-3b9f-4742-95db-dcd69c9a2931   10Gi       RWO            Delete           Bound    default/cloned-pvc   iomesh-csi-driver            122m
     ```
- **UI 方式**

  1. 在左侧导航栏中单击**持久卷申领列表**。
  2. 找到待克隆的 PVC，在**菜单**列选择**克隆**。
  3. 设置克隆后新 PVC 的**名称**，按需修改**访问模式**，并设置 **IOPS 限制**、**BPS 限制**、**认证 Secret 名称**等。

     相关字段说明请分别参考[创建普通持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/create-pv)、[创建具有 QoS 限速功能的持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/pv-qos)、[创建具有身份验证功能的持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/encrypt-pv)和[使用 PVC 创建 iSCSI LUN](/iomesh_cn/1.2.0/user_guide/advanced-functions/external-storage#%E4%BD%BF%E7%94%A8-pvc-%E5%88%9B%E5%BB%BA-iscsi-lun)。
  4. 单击**克隆**。

     当**状态**为 `Bound` 时，表示 PVC 和 PV 已创建成功。您可以在**持久卷申领列表**页面中查看已创建 PVC 的信息。
  5. 在左侧导航栏中单击**持久卷列表**，可查看自动生成的 PV 的相关信息。

---

## 卷操作 > 提升持久卷副本数

# 提升持久卷副本数

支持将数据冗余策略为 2 副本的 PV 提升至 3 副本。

**操作步骤**

- **命令行方式**

  1. 执行如下命令，准备编辑已绑定此 PV 的 PVC。其中 `<pvc_name>` 表示 PVC 的名称，`<pvc_namespace>` 表示 PVC 的名字空间。

     ```
     kubectl edit pvc <pvc_name> -n <pvc_namespace>
     ```
  2. 在 PVC 的 `annotations` 字段中配置 `smartx.com/scaleUpReplicas: "true"` 参数。

     ```
     metadata:
       annotations:
         smartx.com/scaleUpReplicas: "true"
     ```
  3. 执行如下命令，查看 PVC 的更新情况。

     ```
     kubectl describe pvc <pvc_name> -n <pvc_namespace>
     ```

     执行上述命令后，您将看到如下结果，表明与该 PVC 绑定的 PV 已提升至 3 副本。

     ```
     Scale up replicas for pvc <pvc_namespace>/<pvc_name> successfully, ReplicaNum: 3
     ```
- **UI 方式**

  1. 在左侧导航栏中单击**持久卷申领列表**。
  2. 找到待提升副本数的 PV 所绑定的 PVC，在**菜单**列选择**增加副本数**。
  3. 再次单击**增加副本数**。

     更新完成后，会弹出增加副本数成功的界面。

---

## 卷快照操作

# 卷快照操作

介绍创建卷快照类和卷快照，以及从卷快照恢复持久卷的操作。

---

## 卷快照操作 > 创建卷快照类

# 创建卷快照类

卷快照（VolumeSnapshot）指存储系统上现有持久卷（PV）的快照。每个卷快照都与一个卷快照类（VolumeSnapshotClass）绑定，在创建卷快照时，卷快照类用来描述快照的类别。

**字段说明**

| UI 字段 | 对应 YAML 字段 | 描述 |
| --- | --- | --- |
| 名称 | `name` | 卷快照类的名称。 |
| 驱动程序 | `driver` | 用于制备卷快照的 CSI 驱动程序。默认为 `com.iomesh.csi-driver`，不可修改。 |
| [删除策略](https://kubernetes.io/zh-cn/docs/concepts/storage/volume-snapshot-classes/#deletion-policy) | `deletionPolicy` | 用来决定在删除卷快照对象时，其对应的 VolumeSnapshotContent 使用的保留策略，包括保留（`Retain`）和删除（`Delete`）。默认为 `Delete`。 |

**操作步骤**

- **命令行方式**

  1. 通过 YAML 文件 `snc.yaml` 定义一个卷快照类，该卷快照类的 `driver` 和 `deletionPolicy` 字段的取值如下。

     ```
     apiVersion: snapshot.storage.k8s.io/v1beta1
     kind: VolumeSnapshotClass
     metadata:
       name: iomesh-csi-driver
     driver: com.iomesh.csi-driver  # The driver in iomesh.yaml.
     deletionPolicy: Delete # "Delete" is recommended.
     ```
  2. 执行如下命令，使 `sc.yaml` 文件生效，系统自动创建一个卷快照类。

     ```
     kubectl apply -f snc.yaml
     ```
  3. 执行如下命令，查看新创建的卷快照类。

     ```
     kubectl get volumesnapshotclass iomesh-csi-driver
     ```

     执行上述命令后，您将看到如下结果，表明该卷快照类创建成功。

     ```
     NAME                             DRIVER                  DELETIONPOLICY   AGE
     iomesh-csi-driver                com.iomesh.csi-driver   Delete           24s
     ```
- **UI 方式**

  1. 在左侧导航栏中单击**卷快照类列表**。
  2. 单击 **+**。
  3. 参考字段说明设置卷快照类的**名称**和**删除策略**。
  4. 单击**创建**。

     创建完成后，您可以在**卷快照类列表**页面中查看已创建卷快照类的信息。

     单击某一卷快照类的**名称**链接，可查看卷快照类的详细信息，以及相关的卷快照内容和卷快照信息。

---

## 卷快照操作 > 创建卷快照

# 创建卷快照

卷快照（VolumeSnapshot）是对持久卷执行快照的请求，类似于 PVC，而 VolumeSnapshotContent 则是从集群制备卷中获取的快照内容。

**前提条件**

创建卷快照前，必须已存在一个卷快照类。

**注意事项**

通过命令行方式对具有 QoS 限速功能的持久卷创建卷快照、并从卷快照恢复持久卷时，恢复的 PVC 不包含源 PVC 的 QoS 相关配置，即不进行 QoS 限速。

**操作步骤**

- **命令行方式**

  1. 通过 YAML 文件 `snapshot.yaml` 定义一个卷快照 `example-snapshot`，同时指定卷快照类和 PVC 的名称。

     ```
     apiVersion: snapshot.storage.k8s.io/v1beta1
     kind: VolumeSnapshot
     metadata:
       name: example-snapshot
     spec:
       volumeSnapshotClassName: iomesh-csi-driver # Specify a SnapshotClass such as `iomesh-csi-driver`.
       source:
         persistentVolumeClaimName: mongodb-data-pvc # Specify the PVC for which you want to take a snapshot such as `mongodb-data-pvc`.
     ```
  2. 执行如下命令，使 `snapshot.yaml` 文件生效，系统自动创建一个卷快照。同时还将自动生成一个对应卷快照的 VolumeSnapshotContent。

     ```
     kubectl apply -f snapshot.yaml
     ```
  3. 执行如下命令，查看新创建的卷快照和 VolumeSnapshotContent，其中 `example-snapshot` 为卷快照的名称。

     ```
     kubectl get Volumesnapshots example-snapshot
     ```

     执行上述命令后，您将看到如下结果，表明该卷快照和对应的 VolumeSnapshotContent 创建成功。

     ```
     NAME               SOURCEPVC            RESTORESIZE    SNAPSHOTCONTENT                                    CREATIONTIME
     example-snapshot   mongodb-data-pvc     6Gi            snapcontent-fb64d696-725b-4f1b-9847-c95e25b68b13   10h
     ```
- **UI 方式**

  1. 在左侧导航栏中单击**持久卷申领列表**。
  2. 找到待创建卷快照的 PVC，该 PVC 使用的存储类类型须为 `IOMesh`。在**菜单**列选择**新建快照**。
  3. 选择已创建的卷快照类，并设置卷快照的**名称**。
  4. 单击**创建**，创建卷快照。
  5. 在左侧导航栏中单击**卷快照列表**，可查看已创建的卷快照信息。

     | 字段 | 描述 |
     | --- | --- |
     | 名称 | 卷快照的名称。 |
     | 名字空间 | 卷快照所属的名字空间。 |
     | 可使用 | 卷快照是否已可使用。 |
     | 源持久卷申领 | 卷快照的源 PVC 名称。 |
     | 源卷快照内容 | 卷快照的源卷快照内容的名称。 |
     | 恢复容量 | 卷快照的恢复大小。 |
     | 快照类 | 卷快照所属的快照类。 |
     | 快照内容 | 卷快照关联的卷快照内容的名称。 |
     | 快照创建时间 | 快照本身（Volume Snapshot Content）被创建出的时长。 |
     | 创建时间 | 卷快照（Volume Snapshot）被创建出的时长。 |

     - 单击某一卷快照的**名称**链接，可查看卷快照的详细信息。
     - 单击**名字空间**链接，可查看卷快照所属名字空间的详细信息。
     - 单击**源持久卷申领**链接，可查看源 PVC 的详细信息，以及相关的 Pod 和卷快照信息。
     - 单击**卷快照类**链接，可查看所属卷快照类的详细信息，以及相关的卷快照内容和卷快照信息。
     - 单击**卷快照内容**链接，可查看对应卷快照内容的详细信息。
  6. 在左侧导航栏中单击**卷快照内容列表**，可查看已创建的卷快照内容的信息。

     | 字段 | 描述 |
     | --- | --- |
     | 名称 | 卷快照内容的名称。 |
     | 可使用 | 卷快照内容是否已可使用。 |
     | 恢复容量 | 卷快照内容的恢复大小。 |
     | 删除策略 | 在删除卷快照时，其对应的 VolumeSnapshotContent 使用的保留策略，包括保留（`Retain`）和删除（`Delete`）。 |
     | 驱动程序 | 用于制备卷快照的制备器。 |
     | 卷快照类 | 卷快照内容所属的卷快照类。 |
     | 卷快照 | 卷快照内容所属的卷快照。 |
     | IOMesh 集群 | 卷快照内容所属的 IOMesh 集群。 |
     | 创建时间 | 卷快照内容被创建出的时长。 |

     - 单击某一卷快照内容的**名称**链接，可查看卷快照内容的详细信息。
     - 单击**卷快照类**链接，可查看所属卷快照类的详细信息，以及相关的卷快照内容和卷快照信息。
     - 单击**卷快照**链接，可查看所属卷快照的详细信息。
     - 单击 **IOMesh 集群**链接，可查看所属 IOMesh 集群的详细信息。

---

## 卷快照操作 > 从卷快照恢复持久卷

# 从卷快照恢复持久卷

通过创建一个新的 PVC，并指定 `dataSource` 字段为目标卷快照，可以将此卷快照恢复为持久卷；您也可以在 UI 中找到目标卷快照，通过从卷快照创建新的 PVC 将其恢复为持久卷。

**注意事项**

通过卷快照恢复的持久卷与源持久卷的访问模式（accessModes）、卷模式（volumeMode）和存储容量（storage）必须相同。

**操作步骤**

- **命令行方式**

  1. 通过 YAML 文件 `restore.yaml` 定义一个 PVC `example-restore`，在 `spec` 中指明所引用的卷快照名称（dataSource.name），以及该卷快照对应的存储类（`storageClassName`）、访问模式（`accessModes`）和容量（`storage`）。

     ```
     apiVersion: v1
     kind: PersistentVolumeClaim
     metadata:
       name: example-restore 
     spec:
       storageClassName: iomesh-csi-driver
       dataSource:
         name: example-snapshot
         kind: VolumeSnapshot
         apiGroup: snapshot.storage.k8s.io
       accessModes:
         - ReadWriteOnce
       resources:
         requests:
           storage: 6Gi
     ```
  2. 执行如下命令，使 `restore.yaml` 文件生效，系统自动创建一个卷快照对应的 PVC 和 PV，并将此 PVC 和 PV 绑定。

     ```
     kubectl apply -f restore.yaml
     ```
  3. 执行如下命令，查看新创建的 PVC，其中 `example-restore` 为 PVC 的名称。

     ```
     kubectl get pvc example-restore
     ```

     执行上述命令后，您将看到如下结果，`VOLUME` 列显示的即为从卷快照恢复为持久卷的名称。

     ```
     NAME                                        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS        AGE
     example-restore                             Bound    pvc-54230f3f-47dc-46e8-8c42-38c073c40598   6Gi        RWO            iomesh-csi-driver   21h
     ```
  4. 执行如下命令，查看创建的 PV 的详细信息。

     ```
     kubectl get pv pvc-54230f3f-47dc-46e8-8c42-38c073c40598 # The PV name you get in Step 3.
     ```

     执行上述命令后，您将看到如下结果，表明从卷快照恢复为持久卷成功。

     ```
     NAME                                       CAPACITY   RECLAIM POLICY   STATUS   CLAIM                 STORAGECLASS
     pvc-54230f3f-47dc-46e8-8c42-38c073c40598   6Gi        Delete           Bound    example-restore       iomesh-csi-driver
     ```
- **UI 方式**

  1. 在左侧导航栏中单击**卷快照列表**。
  2. 找到待恢复的卷快照，在**菜单**列选择**恢复**。
  3. 设置 PVC 的名称及相关字段。

     > **说明：**
     >
     > - 当卷快照的快照源未被删除时，默认填充源 PVC 的存储类、卷模式和访问模式，默认填充的值不可修改；当卷快照的快照源已被删除时，您需要手动选择存储类、卷模式和访问模式，并且手动选择的卷模式、访问模式需和源 PVC 保持一致。
     > - 存储容量默认填充为卷快照的**恢复容量**，不可修改；如未自动填充，请参考该值自行填充。
     > - 配置 IOPS 限制、BPS 限制、认证 Secret 名称、外部使用或 IQN 准许列表字段后，如卷快照的快照源未被删除则此类字段默认填充源 PVC 的字段值，您可以按需修改；如已被删除则需要您按需手动配置。

     具体字段描述请参考[创建持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/create-pv)章节。
  4. 单击**创建**，创建 PVC 和 PV。
  5. 在左侧导航栏中单击**持久卷申领列表**，可查看从卷快照创建的 PVC 的相关信息；在左侧导航栏中单击**持久卷列表**，可查看自动生成的 PV 的相关信息。

---

## 使用 IOMesh 部署有状态应用

# 使用 IOMesh 部署有状态应用

使用 IOMesh 部署有状态的应用程序，例如 MySQL 和 MongoDB，可以在部署结束后，为这些应用提供持久化存储服务。

本章将以命令行方式为例进行介绍，您也可以使用 UI 创建存储类、PVC 等资源。

---

## 使用 IOMesh 部署有状态应用 > 使用 IOMesh 部署 MySQL

# 使用 IOMesh 部署 MySQL

**前提条件**

确保 IOMesh 集群已完成部署。

**注意事项**

下面示例不适用于运行在 AArch64 服务器上的 Kubernetes 集群。

**操作步骤**

1. 通过 YAML 文件 `iomesh-mysql-sc.yaml` 自定义一个新的存储类，也可以直接使用默认的存储类 `iomesh-csi-driver`，详细内容可参考[创建存储类](/iomesh_cn/1.2.0/user_guide/volume-operations/create-storageclass)。

   ```
   kind: StorageClass
   apiVersion: storage.k8s.io/v1
   metadata:
     name: iomesh-mysql-sc
   provisioner: com.iomesh.csi-driver # The driver.name in `values.yaml` when deploying IOMesh cluster.
   reclaimPolicy: Retain
   allowVolumeExpansion: true
   parameters:
     csi.storage.k8s.io/fstype: "ext4"
     replicaFactor: "2"
     thinProvision: "true"
   ```
2. 执行如下命令，使 `iomesh-mysql-sc.yaml` 文件生效，系统自动创建一个存储类。

   ```
   kubectl apply -f iomesh-mysql-sc.yaml
   ```
3. 通过 YAML 文件 `mysql-deployment.yaml` 定义一个新的 `PersistentVolumeClaim`、`Service` 和 `Deployment`。其中新建的 PVC 用于为每个 MySQL 所在的 Pod 制备持久卷，而 Service 和 Deployment 则用于创建一个新的 Pod 来使用新建的 PVC。

   ```
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: iomesh-mysql-pvc 
   spec:
     storageClassName: iomesh-mysql-sc
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 10Gi
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: mysql
   spec:
     ports:
     - port: 3306
     selector:
       app: mysql
     clusterIP: None
   ---
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: mysql
   spec:
     selector:
       matchLabels:
         app: mysql
     strategy:
       type: Recreate
     template:
       metadata:
         labels:
           app: mysql
       spec:
         containers:
         - image: mysql:5.6
           name: mysql
           env:
             # Enter a password to allow access to the database.
           - name: MYSQL_ROOT_PASSWORD
             value: "password"
           ports:
           - containerPort: 3306
             name: mysql
           volumeMounts:
           - name: mysql-persistent-storage
             mountPath: /var/lib/mysql
         volumes:
         - name: mysql-persistent-storage
           persistentVolumeClaim:
             claimName: iomesh-mysql-pvc
   ```

   您可以访问 [Kubernetes Service](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) 和 [Kubernetes Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) 了解更多详细信息。
4. 执行如下命令，使 `mysql-deployment.yaml` 文件生效。

   ```
   kubectl apply -f mysql-deployment.yaml
   ```

   执行完上述命令后，IOMesh 将为每个 MySQL 运行的 Pod 创建并挂载持久卷，而每个持久卷的设置与存储类里定义的文件系统类型和副本数保持一致。

   您可以对 MySQL 数据库所在的持久卷执行扩容、快照或克隆操作。详细操作可以参考[卷操作](/iomesh_cn/1.2.0/user_guide/volume-operations/volume-operations-1)和[卷快照操作](/iomesh_cn/1.2.0/user_guide/volumesnapshot-operations/volumesnapshot-operations-1)。

---

## 使用 IOMesh 部署有状态应用 > 使用 IOMesh 部署 MongoDB

# 使用 IOMesh 部署 MongoDB

**前提条件**

确保 IOMesh 集群已完成部署。

**注意事项**

下面示例不适用于运行在 AArch64 服务器上的 Kubernetes 集群。

**操作步骤**

1. 通过 YAML 文件 `iomesh-mongodb-sc.yaml` 自定义一个新的存储类，也可以直接使用默认的存储类 `iomesh-csi-driver`，详细内容可参考[创建存储类](/iomesh_cn/1.2.0/user_guide/volume-operations/create-storageclass)。

   ```
   kind: StorageClass
   apiVersion: storage.k8s.io/v1
   metadata:
     name: iomesh-mongodb-sc
   provisioner: com.iomesh.csi-driver 
   reclaimPolicy: Retain
   allowVolumeExpansion: true
   parameters:
     csi.storage.k8s.io/fstype: "ext4"
     replicaFactor: "2"
     thinProvision: "true"
   ```
2. 执行如下命令，使 `iomesh-mongodb-sc.yaml` 文件生效，系统自动创建一个存储类。

   ```
   kubectl apply -f iomesh-mongodb-sc.yaml
   ```
3. 通过 YAML 文件 `mongodb-service.yaml` 定义一个无头 service，用于在 MongoDB 的 Pod 和 IOMesh 集群的客户端之间进行 DNS 查询。

   ```
   apiVersion: v1
   kind: Service
   metadata:
     name: mongo
     labels:
       name: mongo
   spec:
     ports:
       - port: 27017
         targetPort: 27017
     clusterIP: None
     selector:
       role: mongo
   ```
4. 执行如下命令，使 `mongodb-service.yaml` 文件生效，系统自动创建一个无头 service。

   ```
   kubectl apply -f mongodb-service.yaml
   ```
5. 通过 YAML 文件 `mongodb-statefulset.yaml` 为 MongoDB 创建一个 StatefulSet，并将 `storageClassName` 字段的值设置为步骤 1 中所创建的存储类的名称。

   ```
   apiVersion: apps/v1beta1
   kind: StatefulSet
   metadata:
     name: mongo
   spec:
     selector:
       matchLabels:
         role: mongo
         environment: test
     serviceName: "mongo"
     replicas: 3
     template:
       metadata:
         labels:
           role: mongo
           environment: test
       spec:
         terminationGracePeriodSeconds: 10
         containers:
         - name: mongo
           image: mongo
           command:
             - mongod
             - "--replSet"
             - rs0
             - "--smallfiles"
             - "--noprealloc"
           ports:
             - containerPort: 27017
           volumeMounts:
             - name: mongo-persistent-storage
               mountPath: /data/db
         - name: mongo-sidecar
           image: cvallance/mongo-k8s-sidecar
           env:
             - name: MONGO_SIDECAR_POD_LABELS
               value: "role=mongo,environment=test"
     volumeClaimTemplates:
     - metadata:
         name: mongodb-data
       spec:
         accessModes: [ "ReadWriteOnce" ]
         storageClassName: iomesh-mongodb-sc # The StorageClass in Step 1.
         resources:
           requests:
             storage: 10Gi
   ```
6. 执行如下命令，使 `mongodb-statefulset.yaml` 文件生效，系统自动创建一个 StatefulSet。

   ```
   kubectl apply -f mongodb-statefulset.yaml
   ```

   执行完上述命令后，IOMesh 将为每个 MongoDB 运行的 Pod 创建并挂载持久卷，而每个持久卷的设置与存储类里定义的文件系统类型和副本数保持一致。

   您可以对 MongoDB 数据库所在的持久卷执行扩容、快照或克隆操作。详细操作可以参考[卷操作](/iomesh_cn/1.2.0/user_guide/volume-operations/volume-operations-1)和[卷快照操作](/iomesh_cn/1.2.0/user_guide/volumesnapshot-operations/volumesnapshot-operations-1)。

---

## 单集群运维

# 单集群运维

介绍单个 IOMesh 集群的相关运维操作。

**基本概念**

Chunk Pod：Worker 节点上提供存储服务的 Pod。

Meta Pod：Worker 节点上提供元数据管理的 Pod。

---

## 单集群运维 > 扩容集群

# 扩容集群

当 IOMesh 集群的软件版本为企业版时，可以在不影响集群业务的情况下，参考下述步骤在线扩容。使用 IOMesh 社区版的集群由于对节点数存在限制（不能超过 3 个），不支持扩容。

IOMesh 集群支持仅添加 Chunk Pod、仅添加 Meta Pod，或同时添加 Chunk Pod 和 Meta Pod。

**前提条件**

确保 Kubernetes 集群中有足够的 Worker 节点。
每个 Worker 节点只能运行一个 Chunk Pod 和一个 Meta Pod，因此，若 Worker 节点数量不足，则需提前在 Kubernetes 集群中创建用于添加 Pod 的 Worker 节点。

**注意事项**

- 单个 IOMesh 集群最少应包含 3 个 Chunk Pod，最大的 Chunk Pod 数量由 Kubernetes 集群包含的 Worker 节点数和 IOMesh 许可中的最大节点数共同决定，最多可达到企业版的最大规格 255 个。
- IOMesh 集群中支持的 Meta Pod 个数为 3 个或 5 个。

**操作步骤**

- **命令行方式**

  - **添加 Chunk Pod**

    若 IOMesh 集群中的容量不足，需要通过添加 Chunk Pod 来扩展容量，则执行以下操作添加 Chunk Pod。

    1. 编辑在安装部署集群时导出的 IOMesh 的默认配置文件 `iomesh.yaml`，定位至 `chunk`，然后编辑 `replicaCount` 字段。`replicaCount` 为扩容后 Chunk Pod 的总数。

       ```
       chunk:
         replicaCount: 5 # Enter the number of chunk pods.
       ```
    2. 执行如下命令，使上述修改生效。

       ```
       helm upgrade --namespace iomesh-system iomesh iomesh/iomesh --values iomesh.yaml
       ```
    3. 执行如下命令，查看修改结果。

       ```
       kubectl get pod -n iomesh-system | grep chunk
       ```

       若输出结果如下，则说明修改成功：

       ```
       iomesh-chunk-0                                         3/3     Running   0          5h5m
       iomesh-chunk-1                                         3/3     Running   0          5h5m
       iomesh-chunk-2                                         3/3     Running   0          5h5m
       iomesh-chunk-3                                         3/3     Running   0          5h5m
       iomesh-chunk-4                                         3/3     Running   0          5h5m
       ```
  - **添加 Meta Pod**

    部署 IOMesh 时，已在 IOMesh 集群中创建了 3 个 Meta Pod。若 Kubernetes 集群内的 IOMesh 节点数 ≥ 5，则建议将 Meta Pod 的数量由 3 个增加到 5 个。

    1. 编辑在安装部署集群时导出的 IOMesh 的默认配置文件 `iomesh.yaml`，定位至 `meta`，然后编辑 `replicaCount` 字段。`replicaCount` 为扩容后 Meta Pod 的总数。

       ```
       meta:
         replicaCount: 5 # Change the value to 5.
       ```
    2. 执行如下命令，使上述修改生效。

       ```
       helm upgrade --namespace iomesh-system iomesh iomesh/iomesh --values iomesh.yaml
       ```
    3. 执行如下命令，查看修改结果。

       ```
       kubectl get pod -n iomesh-system | grep meta
       ```

       若输出结果如下，则说明修改成功：

       ```
       iomesh-meta-0                                         2/2     Running   0          5h5m
       iomesh-meta-1                                         2/2     Running   0          5h5m
       iomesh-meta-2                                         2/2     Running   0          5h5m
       iomesh-meta-3                                         2/2     Running   0          5h5m
       iomesh-meta-4                                         2/2     Running   0          5h5m
       ```
- **UI 方式**

  1. 在左侧导航栏中单击 **IOMesh 集群列表**。
  2. 找到待扩容的集群，在**菜单**列选择**调整规模**，增加 **Chunk Pod 数量**或 **Meta Pod 数量**。
  3. 单击**调整规模**。

---

## 单集群运维 > 缩容集群

# 缩容集群

IOMesh 支持对集群进行缩容，即通过删除 Kubernetes 集群中 Worker 节点上的 Chunk Pod 或 Meta Pod 来缩小 IOMesh 集群的容量。

**注意事项**

- 仅支持删除 Chunk Pod 或 Meta Pod，不支持删除 Zookeeper Pod。
- 每次只能减少 1 个 Chunk Pod 或 Meta Pod。
- 每个 Chunk Pod 或 Meta Pod 在创建时都由 `StatefulSet` 进行了编号，删除 Chunk Pod 或 Meta Pod 必须与创建 Pod 的顺序正好相反。假设有 5 个 Chunk Pod：`iomesh-chunk-0`、`iomesh-chunk-1`、`iomesh-chunk-2`、`iomesh-chunk-3`、`iomesh-chunk-4`，则会自动从 `iomesh-chunk-4` 开始删除。
- 单个 IOMesh 集群最少应包含 3 个 Chunk Pod，当 Chunk Pod 数量大于 3 时您可以按需删除 Chunk Pod；单个 IOMesh 集群支持 3 个或 5 个 Meta Pod，当 Meta Pod 数量为 5 时，您可以按需删除 Meta Pod 至 3 个。

**操作步骤**

- **命令行方式**

  - **删除 Chunk Pod**

    下面示例描述的是通过删除 `k8s-worker-3` 节点上的 `iomesh-chunk-3` 来减少 Chunk Pod 数量的操作。

    1. 修改 `iomesh.yaml`，定位至 `chunk`，编辑 `replicaCount` 字段。

       ```
       chunk:
         replicaCount: 4 # Reduce the value to 3.
       ```
    2. 执行以下命令，使配置生效。

       ```
       helm upgrade --namespace iomesh-system iomesh iomesh/iomesh --values iomesh.yaml
       ```
    3. 验证 Chunk Pod 的个数是否已经减少。

       ```
       kubectl get pod -n iomesh-system | grep chunk
       ```

       执行命令后，您将看到如下输出，表示减少 Chunk Pod 个数成功。

       ```
       iomesh-chunk-0                                         3/3     Running   0          5h5m
       iomesh-chunk-1                                         3/3     Running   0          5h5m
       iomesh-chunk-2                                         3/3     Running   0          5h5m
       ```
  - **删除 Meta Pod**

    下面示例描述的是通过删除 `k8s-worker-4` 节点上的 `iomesh-meta-4` 和 `k8s-worker-3` 节点上的 `iomesh-meta-3` 来减少 Meta Pod 数量的操作。

    1. 修改 `iomesh.yaml`，定位至 `meta`，编辑 `replicaCount` 字段。

       ```
       meta:
         replicaCount: 5 # Reduce the value to 4.
       ```
    2. 执行以下命令，使配置生效。

       ```
       helm upgrade --namespace iomesh-system iomesh iomesh/iomesh --values iomesh.yaml
       ```
    3. 重复执行步骤 1 和步骤 2，将 Meta Pod 数量减少至 3 个。
    4. 验证 Meta Pod 的个数是否已经减少。

       ```
       kubectl get pod -n iomesh-system | grep meta
       ```

       执行命令后，您将看到如下输出，表示减少 Meta Pod 个数成功。

       ```
       iomesh-meta-0                                         2/2     Running   0          5h5m
       iomesh-meta-1                                         2/2     Running   0          5h5m
       iomesh-meta-2                                         2/2     Running   0          5h5m
       ```
- **UI 方式**

  1. 在左侧导航栏中单击 **IOMesh 集群列表**。
  2. 找到待缩容的集群，在**菜单**列选择**调整规模**，减少 **Chunk Pod 数量**或 **Meta Pod 数量**。
  3. 单击**调整规模**。

---

## 单集群运维 > 升级集群

# 升级集群

IOMesh 支持在线升级和离线升级，您可以从 1.0.1 或 1.1.0 版本升级至本版本。

**注意事项**

- 当存在只有 1 个 Meta Pod 或 Chunk Pod 的 IOMesh 集群时，不支持升级 IOMesh 集群。
- IOMesh 集群在升级过程中，可能会出现短暂的 I/O 延迟。
- 若基于[管理多集群](/iomesh_cn/1.2.0/user_guide/advanced-functions/multiple-cluster-management#%E7%AE%A1%E7%90%86%E5%A4%9A%E9%9B%86%E7%BE%A4)章节部署了多个 IOMesh 集群，完成升级步骤后所有集群均会进行升级。

## 在线升级

1. 执行如下命令，将 IOMesh Operator Deployment 的副本数改为 1。

   ```
   kubectl scale deploy operator --replicas=1 -n iomesh-system
   ```
2. 执行如下命令，暂时停用 IOMesh Webhook，以避免升级失败。升级成功后，IOMesh Webhook 将会自动重启。

   ```
   kubectl delete Validatingwebhookconfigurations iomesh-validating-webhook-configuration
   ```
3. 为避免在线升级过程中，镜像拉取速度慢导致服务中断时间过长，必须提前[手动加载 IOMesh 容器镜像](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prepare-iomesh-images#%E6%89%8B%E5%8A%A8%E5%8A%A0%E8%BD%BD-iomesh-%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F)。
4. 安装 IOMesh 1.2.0 CRD。

   ```
   kubectl apply -f https://iomesh.run/config/crd/iomesh-v1.2.0/iomesh.com_iomeshclusters.yaml
   kubectl apply -f https://iomesh.run/config/crd/iomesh-v1.2.0/deck.smartx.com_sessions.yaml
   kubectl apply -f https://iomesh.run/config/crd/iomesh-v1.2.0/deck.smartx.com_users.yaml
   ```
5. 获取 IOMesh 1.2.0 中添加的新字段和对应的值。

   ```
   wget https://iomesh.run/config/merge-values/v1.2.0.yaml -O merge-values.yaml
   ```
6. 升级 IOMesh 集群。升级时会在保留当前已有字段和值的前提下，同时将新添加的字段和值合入。

   ```
   helm repo update
   ```

   ```
   helm upgrade --namespace iomesh-system iomesh iomesh/iomesh --reuse-values -f merge-values.yaml --version v1.2.0
   ```
7. 执行如下命令，验证所有的 Pod 是否正在运行。当所有的 Pod 显示为 `Running` 状态时，表示 IOMesh 集群已成功升级。

   ```
   watch kubectl get pod --namespace iomesh-system
   ```
8. （可选）若已通过 Grafana 监控 IOMesh，则需重新[导入 Grafana Dashboard](/iomesh_cn/1.2.0/user_guide/monitor-iomesh/installing-iomesh-dashboard#%E5%AF%BC%E5%85%A5-Grafana-Dashboard)。

## 离线升级

**前提条件**

已提前下载 IOMesh 离线安装包。

**操作步骤**

1. 执行如下命令，将 IOMesh Operator Deployment 的副本数改为 1。

   ```
   kubectl scale deploy operator --replicas=1 -n iomesh-system
   ```
2. 执行如下命令，暂时停用 IOMesh Webhook，以避免升级失败。升级成功后，IOMesh Webhook 将会自动重启。

   ```
   kubectl delete Validatingwebhookconfigurations iomesh-validating-webhook-configuration
   ```
3. [准备 IOMesh 容器镜像](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prepare-iomesh-images)。
4. 安装 IOMesh 1.2.0 CRD。

   ```
   kubectl apply -f ./configs/crds/
   ```
5. 根据准备 IOMesh 容器镜像的方式，选择执行相应命令升级 IOMesh 集群。升级会在保留当前已有字段和值的前提下，同时将新添加的字段和值合入。

   - 当使用[手动加载 IOMesh 容器镜像](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prepare-iomesh-images#%E6%89%8B%E5%8A%A8%E5%8A%A0%E8%BD%BD-iomesh-%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F)方式准备 IOMesh 容器镜像时，执行如下命令升级。

     ```
     ./helm upgrade --namespace iomesh-system iomesh ./charts/iomesh --reuse-values -f ./configs/merge-values.yaml
     ```
   - 当使用[推送 IOMesh 容器镜像至私有镜像仓库](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prepare-iomesh-images#%E6%8E%A8%E9%80%81-iomesh-%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F%E8%87%B3%E7%A7%81%E6%9C%89%E9%95%9C%E5%83%8F%E4%BB%93%E5%BA%93)方式准备 IOMesh 容器镜像时，执行如下命令升级。

     ```
     ./helm upgrade --namespace iomesh-system iomesh ./charts/iomesh --reuse-values -f ./configs/merge-values.yaml --set global.registry=REGISTRY.YOURDOMAIN.COM:PORT/
     ```
6. 执行如下命令，验证所有的 Pod 是否正在运行。当所有的 Pod 显示为 `Running` 状态时，表示 IOMesh 集群已成功升级。

   ```
   watch kubectl get pod --namespace iomesh-system
   ```
7. （可选）若已通过 Grafana 监控 IOMesh，则需重新[导入 Grafana Dashboard](/iomesh_cn/1.2.0/user_guide/monitor-iomesh/installing-iomesh-dashboard#%E5%AF%BC%E5%85%A5-Grafana-Dashboard)。

---

## 单集群运维 > 卸载集群

# 卸载集群

**注意事项**

在执行卸载 IOMesh 集群操作前，必须先删除所有 IOMesh 创建的 PVC 和使用了 IOMesh PVC 的用户 Pod。否则，直接卸载 IOMesh 集群会导致所有数据未按用户预期的清理顺序并清空，并且会在重新部署 IOMesh 出现错误。

**操作步骤**

执行如下命令，卸载 IOMesh 集群。

```
helm uninstall --namespace iomesh-system iomesh
```

在卸载 IOMesh 后，如果出现由于网络或其他问题导致仍有 IOMesh 资源未被删除的情况，请执行以下命令，将这些资源全部删除。

```
curl -sSL https://iomesh.run/uninstall_iomesh.sh | sh -
```

---

## 单集群运维 > 更新许可

# 更新许可

IOMesh 提供两个软件版本：社区版和企业版，它们支持的最大 Worker 节点数和商业服务有所不同。

## 查看许可信息

- **命令行方式**

  执行如下命令，查看软件的许可信息。

  ```
  kubectl get iomesh -n iomesh-system -o=jsonpath='{.items[0].status.license}'
  ```

  然后您将看到如下输出，显示许可的详细信息。

  | 字段 | 描述 |
  | --- | --- |
  | `Expiration Date` | 许可证的过期时间。 |
  | `License Type` | IOMesh 的许可类型：  - 试用许可：部署 IOMesh 集群后自动生成，默认有效期 30 天。 - 订阅许可：用户根据需要所订阅的时长，至少 1 年。 - 永久许可：永久有效，永不过期。 |
  | `Max Chunk Num` | IOMesh 集群支持的最大 Worker 节点数。 |
  | `Max Physical Data Capacity` | IOMesh 集群的最大容量，`0` 表示没有限制。 |
  | `Max Physical Data Capacity Per Node` | IOMesh 集群中每个节点的最大容量，`0` 表示没有限制。 |
  | `Serial` | IOMesh 集群的序列号。 |
  | `Sign Date` | 许可证的签发日期。 |
  | `Software Edition` | IOMesh 的许可版本：社区版或企业版。 |
  | `Subscription Expiration Date` | 订阅许可的过期时间。 |
  | `Subscription Start Date` | 订阅许可的生效时间。 |
- **UI 方式**

  1. 在左侧导航栏中单击 **IOMesh 集群列表**。
  2. 找到待查看的集群，在**菜单**列选择**查看许可证**，可查看如下许可信息。

     | 字段 | 描述 |
     | --- | --- |
     | 序列号 | IOMesh 集群的序列号。 |
     | 类型 | IOMesh 的许可类型：  - `TRIAL`：试用许可，部署 IOMesh 集群后自动生成，默认有效期 30 天。 - `SUBCRIPTION`：订阅许可，用户根据需要所订阅的时长，至少 1 年。 - `PERPETUAL`：永久许可，永久有效，永不过期。 |
     | 版本 | IOMesh 的许可版本，包括 `COMMUNITY`（社区版）或 `ENTERPRICE`（企业版）。 |
     | 最大节点数 | 许可的最大节点数。 |
     | 过期时间 | IOMesh 集群许可的过期时间。 |

## 更新许可

当 IOMesh 面临以下情况时，需更新许可证码：

- 安装完 IOMesh 后激活许可，详细操作步骤可参见[激活许可](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/activate-license)。
- 当前的节点数已不能满足要求，需增加节点的数量。
- 延长试用许可，或者延长订阅许可的有效期。

**前提条件**

需提前获取新的许可证码。

- 社区版：登录 [IOMesh 官网](https://www.iomesh.com/license)免费申请新的许可证码。
- 企业版：联系 SmartX 客户经理获取新的许可证码。

**操作步骤**

- **命令行方式**

  1. 按顺序执行如下命令，删除旧版的 Kubernetes Secret 和 `iomesh` 对象中的 `spec.licenseSecretName` 字段。

     ```
     kubectl delete secret iomesh-authorization-code -n iomesh-system
     ```

     ```
     kubectl edit iomesh -n iomesh-system
     ```

     ```
     spec:
       licenseSecretName: iomesh-authorization-code # Delete this line.
     ```
  2. 将更新后的许可证码粘贴并保存在新建的 `license-code.txt` 文件中。
  3. 创建一个 Kubernetes Secret 对象。

     ```
     kubectl create secret generic iomesh-authorization-code -n iomesh-system --from-file=authorizationCode=./license-code.txt
     ```
  4. 增加 `spec.licenseSecretName` 字段，并填入在上面创建 Kubernetes Secret 对象时输入的 `iomesh-authorization-code`， 作为该字段的值。

     ```
     kubectl edit iomesh -n iomesh-system
     ```

     ```
     spec:
       licenseSecretName: iomesh-authorization-code
     ```
  5. 确认更新是否生效，其生效信息将显示在下面的输出结果中。

     ```
     kubectl describe iomesh -n iomesh-system # Whether the update is successful will be displayed in the events.
     ```

     若显示更新失败，请确认保存的许可证码是否正确。若更新再次失败，请重新设置 `spec.licenseSecretName` 字段。
  6. 验证许可证码的过期时间和其他内容是否符合预期。

     ```
     kubectl get iomesh -n iomesh-system -o=jsonpath='{.items[0].status.license}'
     ```
- **UI 方式**

  1. 在左侧导航栏中单击 **IOMesh 集群列表**。
  2. 找到待更新的集群，在**菜单**列选择**查看许可证**，将新的许可证码粘贴在**许可证码**区域。
  3. 单击**上传**。

---

## 单集群运维 > 更换硬盘

# 更换硬盘

在 IOMesh Dashboard 上可以查看物理盘的健康状态。当物理盘处于以下三种状态时，请尽快更换新的物理盘。

- 不健康（`Unhealthy`）
- 亚健康（`Subhealthy`）
- S.M.A.R.T 未通过（`S.M.A.R.T not passed`）

**操作步骤**

- **命令行方式**

  1. 执行如下命令，获取 meta leader pod 的名称。

     ```
     kubectl get pod -n iomesh-system -l=iomesh.com/meta-leader -o=jsonpath='{.items[0].metadata.name}'
     ```

     ```
     iomesh-meta-0
     ```
  2. 访问 meta leader pod。

     ```
     kubectl exec -it iomesh-meta-0 -n iomesh-system -c iomesh-meta bash
     ```
  3. 反复执行以下命令，直至确认集群中没有正在进行的迁移或恢复任务。

     确保执行命令后，下面字段的输出值全部为 0。若输出值为其他数字，请等待其变更为 0。

     ```
     /opt/iomesh/iomeshctl summary cluster | egrep "recovers|migrates"
     ```

     ```
     num_ongoing_recovers: 0
     num_pending_recovers: 0
     num_ongoing_migrates: 0
     num_pending_migrates: 0
       pending_migrates_bytes: 0
       pending_recovers_bytes: 0
           pending_migrates_bytes: 0
           pending_recovers_bytes: 0
           pending_migrates_bytes: 0
           pending_recovers_bytes: 0
           pending_migrates_bytes: 0
           pending_recovers_bytes: 0
       num_ongoing_recovers: 0
       num_pending_recovers: 0
       num_ongoing_migrates: 0
       num_pending_migrates: 0
         pending_migrates_bytes: 0
         pending_recovers_bytes: 0
     ```
  4. 执行如下命令，查看需要被替换的硬盘。在如下示例中，假设待更换的硬盘为 `blockdevice-66312cce9037ae891a099ad83f44d7c9`。

     ```
     kubectl --namespace iomesh-system get bd
     ```

     ```
     NAME                                           NODENAME      PATH       FSTYPE   SIZE          CLAIMSTATE   STATUS   AGE
     blockdevice-41f0c2b60f5d63c677c3aca05c2981ef   qtest-k8s-0   /dev/sdc            53687091200   Unclaimed    Active   29h
     blockdevice-66312cce9037ae891a099ad83f44d7c9   qtest-k8s-1   /dev/sdc            69793218560   Claimed      Active   44h
     blockdevice-7aff82fe93fac5153b14af3c82d68856   qtest-k8s-2   /dev/sdb            69793218560   Claimed      Active   44h
     ```
  5. 执行如下命令，编辑硬盘的 `deviceMap`，将需要更换的硬盘的名称添加到 `devicemap` 下的 `exclude` 字段。

     ```
     kubectl edit iomesh iomesh -n iomesh-system
     ```

     ```
         # ...
         deviceMap:
           # ...
           dataStore:
             selector:
               matchExpressions:
               - key: iomesh.com/bd-driverType
                 operator: In
                 values:
                 - HDD
               matchLabels:
                 iomesh.com/bd-deviceType: disk
             exclude:
             - blockdevice-66312cce9037ae891a099ad83f44d7c9
       # ...
     ```
  6. 重复执行步骤 2 和 3，直至确认集群中没有正在进行的迁移或恢复任务。
  7. 确认块设备处于 `unclaimed` 状态。

     ```
     kubectl get bd blockdevice-66312cce9037ae891a099ad83f44d7c9 -n iomesh-system
     ```

     ```
     NAME                                           NODENAME      PATH       FSTYPE   SIZE          CLAIMSTATE     STATUS   AGE
     blockdevice-66312cce9037ae891a099ad83f44d7c9   qtest-k8s-1   /dev/sdc            69793218560   Unclaimed      Active   44h
     ```
  8. 拔掉硬盘，硬盘进入 `Inactive` 状态。

     同时执行下面的命令，删除块设备和其相应的 `blockdeviceclaim`。

     > **说明：**
     >
     > 在执行如下命令清除 `bdc` 时，如系统提示“当前未找到 bdc”，属于正常情况。

     ```
     kubectl patch bdc/blockdevice-66312cce9037ae891a099ad83f44d7c9 -p '{"metadata":{"finalizers":[]}}' --type=merge -n iomesh-system
     kubectl patch bd/blockdevice-66312cce9037ae891a099ad83f44d7c9 -p '{"metadata":{"finalizers":[]}}' --type=merge -n iomesh-system
     kubectl delete bdc blockdevice-66312cce9037ae891a099ad83f44d7c9 -n iomesh-system
     kubectl delete bd blockdevice-66312cce9037ae891a099ad83f44d7c9 -n iomesh-system
     ```
  9. 插入新的硬盘，可参考[设置 IOMesh](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/setup-iomesh)，将硬盘挂载至 IOMesh 集群。
- **UI 方式**

  1. 参考命令行方式的步骤 1 ～ 3，确认集群中没有正在进行的迁移或恢复任务。
  2. 在左侧导航栏中单击**块设备列表**，找到待替换的块设备。
  3. 在**菜单**列选择**卸载**，卸载块设备。

     卸载后，块设备的**申领状态**变更为 `Unclaimed`。
  4. 拔掉硬盘，硬盘进入 `Inactive` 状态。

     参考命令行方式的步骤 8 删除 bdc，然后在**菜单**列选择**删除**以删除 bd。
  5. 插入新的硬盘，可参考[设置 IOMesh](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/setup-iomesh)，将硬盘挂载至 IOMesh 集群。

---

## 单集群运维 > 替换 Kubernetes 集群节点

# 替换 Kubernetes 集群节点

当需要替换运行有 IOMesh 服务的 Kubernetes 集群节点时，请参考本小节内容，优先完成操作前的检查，再从集群中删除旧节点，然后添加新节点，以确保 IOMesh 集群的服务延续性和数据安全性。

## 操作前检查

- 在 Meta Leader 的 Pod shell 中执行如下命令，检查集群没有正在进行的数据恢复和数据迁移。

  ```
  /opt/iomesh/iomeshctl summary cluster | grep -E 'recover|migrate'
  ```

  确认输出的数字都是 **0**。
- 确认删除节点后，Kubernetes 集群中有足够存储空间容纳当前 IOMesh 中的数据。
- 确认 Meta Leader Pod 和 ZooKeeper Leader Pod 均不在待删除的节点上。

  - 如果 Meta Leader Pod 在待删除的节点上，需手动触发一次 Meta 换主。
  - 如果 ZooKeeper Leader Pod 在待删除的节点上，需手动触发一次 ZooKeeper 换主，可简单通过删除该 ZooKeeper Leader Pod 来实现。

## 删除 Kubernetes 节点

1. 在 Meta Leader 的 Pod shell 中执行如下命令，注销 Chunk：

   ```
   /opt/iomesh/iomeshctl chunk unregister <chunk-id>
   ```

   您可以通过 `iomeshctl chunk list` 进行查询 chunk-id。
2. 执行如下命令 drain 待删除节点：

   ```
   kubectl drain --ignore-daemonsets --delete-emptydir-data <node-name>
   ```
3. 删除待删除节点上的 ZooKeeper、Meta 和 Chunk Pod 所使用的 hostpath 类型的 PVC。

   PVC 名称类似 `data-iomesh-zookeeper-?`、`db-data-iomesh-meta-?`、`coredump-iomesh-meta-?`、`base-dir-iomesh-chunk-?` 和 `coredump-iomesh-chunk-?`。

   > **注意**：
   >
   > 请谨慎操作，不可误删其他 PVC。
4. 执行如下命令删除节点：

   ```
   kubectl delete node <node-name>
   ```

   如果 Kubernetes 集群有足够调度 IOMesh 的节点，那么被删除节点上的 ZooKeeper、Meta 和 Chunk Pod 会在剩余可用节点中重新调度并启动；

   否则，对应的 ZooKeeper、Meta 和 Chunk Pod 会一直处于 `pending` 状态。

   > **注意**：
   >
   > 此时，您仍然可以正常使用 IOMesh 集群，请不要通过调整 IOMesh 的副本数来处理此问题，添加节点之后将重新启动这些 Pod。

## 添加 Kubernetes 新节点

1. 执行如下命令创建 token：

   ```
   kubeadm token create --print-join-command
   ```
2. 在待添加的节点上执行上述命令打印出来的命令内容。
3. 可选：如果之前删除 Kubernetes 节点时因为可调度资源不足，导致存在 `pending` 状态的 ZooKeeper、Meta 和 Chunk Pod，添加新节点后，这些 Pod 将在新节点上启动。

---

## 监控集群

# 监控集群

IOMesh 可提供标准化和可视化的监控与报警服务。

支持如下两种监控方式：

- [通过 Grafana 监控 IOMesh](/iomesh_cn/1.2.0/user_guide/monitor-iomesh/installing-iomesh-dashboard)
- [通过 UI 监控 IOMesh](/iomesh_cn/1.2.0/user_guide/monitor-iomesh/enable-ui-monitoring)

---

## 监控集群 > 通过 Grafana 监控 IOMesh > 安装 IOMesh Dashboard

# 安装 IOMesh Dashboard

IOMesh Dashboard 基于 Prometheus 和 Grafana 实现监控功能，在安装 IOMesh Dashboard 前，请确保您已安装 Prometheus 和 Grafana。

**注意事项**

若需查看 [Persistent Volume](/iomesh_cn/1.2.0/user_guide/monitor-iomesh/monitoring-iomesh#persistent-volume) 相关信息，则还需提前安装 kube-state-metrics。

## 启用 IOMesh 指标

1. 根据 IOMesh 安装方式，执行相应命令获取 `iomesh.yaml` 文件。

   - 在线安装

     ```
     helm -n iomesh-system get values iomesh -o yaml > iomesh.yaml
     ```
   - 离线安装

     ```
     ./helm -n iomesh-system get values iomesh -o yaml > iomesh.yaml
     ```
2. 编辑 `iomesh.yaml` 文件中的 `operator`、`iomesh` 和 `blockdevice monitor` 字段。

   - `operator`

     ```
     operator:
       metricsPort: 8080

       # Configure ServiceMonitor for Prometheus Operator.
       serviceMonitor:
         create: true # Set it to "true" to create a ServiceMonitor object, which defaults to "false".
         namespace: "" # Create a namespace for ServiceMonitor object. If left blank, "iomesh-system" will be specified.
         labels: {} # Set the label for ServiceMonitor object, which defaults to blank.

         # Configure Relabelings. See more information at <https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config>
         relabelings: [] # Set relabeling parameters for metrics, which defaults to blank.

       # Configure PrometheusRule for Prometheus Operator.
       prometheusRule:
         create: true # Set it to "true" to create a PrometheusRule object, which defaults to "false".
         namespace: "" # Create a namespace for PrometheusRule object.  If left blank, "iomesh-system" will be specified.
         labels: {} # Set the label for PrometheusRule object, which defaults to blank.
     ```
   - `iomesh`

     ```
     iomesh:
       # Configure ServiceMonitor for Prometheus Operator.
       serviceMonitor:
         create: true # Set it to true to create a serviceMonitor object, which defaults to false.
         namespace: "" # Create a namespace for serviceMonitor object. If left blank, "iomesh-system" will be specified.
         labels: {} # Set the label for serviceMonitor object, which defaults to blank.

      meta:
        serviceMonitor:
          # Configure Relabelings. See more information at <https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config>.
          relabelings: [] # Set relabeling parameters for metrics, which defaults to blank.
      chunk:
        serviceMonitor:
          # Configure Relabelings. See more information at <https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config>.
          relabelings: [] # Set relabeling parameters for metrics, which defaults to blank.
     ```
   - `blockdevice monitor`

     ```
     blockdevice-monitor:
       # Configure PodMonitor for Prometheus Operator.
       podMonitor:
         create: true # Set it to true to create a PodMonitor object, which defaults to false.
         namespace: "" # Create a namespace for PodMonitor object. If left blank, "iomesh-system" will be specified.
         labels: {} # Set the label for PodMonitor object, which defaults to blank.
       # Configure PrometheusRule for Prometheus Operator.
       prometheusRule:
         create: true # Set it to true to create a PrometheusRule object, which defaults to false.
         namespace: "" # Create a namespace for PrometheusRule object. If left blank, "iomesh-system" will be specified.
         labels: {} # Set the label for PrometheusRule object, which defaults to blank.

       blockdevicemonitor:
         podMonitor:
           # Configure Relabelings. See more information at <https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config>.
           relabelings: [] # Set relabelings parameters, which defaults to blank.

       prober:
         podMonitor:
           # Configure Relabelings. See more information at <https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config>.
           relabelings: [] # Set relabelings parameters, which defaults to blank.
     ```
3. 根据 IOMesh 安装方式，执行相应命令，使配置生效。

   - 在线安装

     ```
     helm -n iomesh-system upgrade iomesh iomesh/iomesh -f ./iomesh.yaml
     ```
   - 离线安装

     ```
     ./helm -n iomesh-system upgrade iomesh charts/iomesh -f ./iomesh.yaml
     ```
4. 确认相关的修改已生效。

   - `ServiceMonitor`

     ```
     kubectl -n iomesh-system get servicemonitor
     ```

     执行上述命令后，您将看到如下结果。

     ```
     NAME                 AGE
     iomesh               10m
     iomesh-operator      10m
     ```
   - `PodMonitor`

     ```
     kubectl -n iomesh-system get podmonitor
     ```

     执行上述命令后，您将看到如下结果。

     ```
     NAME                         AGE
     blockdevice-monitor          10m
     blockdevice-monitor-prober   10m
     ```
   - `PrometheusRule`

     ```
     kubectl -n iomesh-system get prometheusrule
     ```

     执行上述命令后，您将看到如下结果。

     ```
     NAME                 AGE
     blockdevicemonitor   10m
     iomesh               10m
     ```

## （可选）添加 Prometheus 权限

当 IOMesh 集群与 Prometheus 不在同一个名字空间下时，需要添加 Prometheus 权限以采集 IOMesh 指标。

**操作步骤**

下面以 IOMesh 集群所在名字空间为 `iomesh-cluster-1`，Prometheus 所在名字空间为 `monitoring` 为例进行介绍。

1. 编辑 ServiceMonitor 对象 `iomesh` 的 `spec.namespaceSelector.matchNames` 字段，添加需要监控的 IOMesh 集群的名字空间。

   ```
   kubectl -n iomesh-system edit servicemonitor iomesh
   ```

   ```
   apiVersion: monitoring.coreos.com/v1
   kind: ServiceMonitor
   metadata:
     name: iomesh
     namespace: iomesh-system
   spec:
     # ...
     namespaceSelector:
       matchNames:
         - iomesh-system
         - iomesh-cluster-1 # Add the namespace of the target IOMeshCluster.
     # ...
   ```
2. 编辑 IOMesh 集群所在名字空间下 RoleBinding 对象 `prometheus-iomesh` 的 `subjects` 字段，更新 Prometheus 所使用的 ServiceAccount 相关参数。

   ```
   kubectl -n iomesh-cluster-1 edit RoleBinding prometheus-iomesh
   ```

   ```
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     name: prometheus-iomesh
     namespace: iomesh-cluster-1
     # ...
   subjects:
     - kind: ServiceAccount
       name: prometheus # 更新为 Prometheus 所使用的 ServiceAccount 名。
       namespace: monitoring # 更新为 Prometheus 名字空间。
   ```
3. （可选）若 Kubernetes 集群中创建了多个与 Prometheus 不在同一名字空间的 IOMesh 集群，且均需进行监控，则每个 IOMesh 集群依次执行如上步骤即可。

## 导入 Grafana Dashboard

启用 IOMesh 指标后，请将 Grafana Dashboard 导入 Grafana。

**前提条件**

已提前下载 `json` 格式的 IOMesh Cluster Dashboard 文件。

> **说明：**
>
> 如果您之前选择的是离线安装 IOMesh，由于离线安装包中已包含 IOMesh Cluster Dashboard 文件（`iomesh-cluster-dashboard.json`），请从下载的 IOMesh 离线安装包中直接获取即可（位于 `iomesh-offline/configs` 目录下），无需重复下载该文件。

**操作步骤**

1. 登录 Grafana 网站。
2. 在 Dashboard 主页导入已下载的 IOMesh Cluster Dashboard 文件。导入成功后，您将在 Dashboard 中看到 IOMesh 相关的监控信息。

---

## 监控集群 > 通过 Grafana 监控 IOMesh > Grafana 监控信息

# Grafana 监控信息

成功导入 Grafana 后，您将看到如下所示的 Dashboard。若需要对 Dashboard 进行配置和调整，可参考 [Grafana 官方文档](https://grafana.com/docs/grafana/latest/dashboards/)。

![image](https://user-images.githubusercontent.com/102718816/234539619-1eb6988b-464f-48dd-8ca4-aad36430ef00.png)

IOMesh 从以下 5 个方面提供信息，以监控 IOMesh 存储。

- Overview
- Node
- Details of Node
- Physical Disk
- Persistent Volume

## Overview

**Overview** 展示 IOMesh 集群信息和资源使用情况。

| 面板 | 描述 |
| --- | --- |
| Alert | 展示当前 IOMesh 集群的所有报警，默认情况下展示报警名称、触发状态和持续时间等信息，可通过展开报警查看其严重程度、报警原因、影响和解决方案等。支持在 **Alerting** 页面设置 Alert Rules 的阈值。 |
| Cluster Info | 展示 IOMesh 集群的基本信息，包括 IOMesh 版本、IOMesh Block Storage 版本，CPU 架构，许可类型、许可版本、许可的最大节点数以及许可的过期时间。 |
| Node | 展示 IOMesh 集群中的总节点数，以及当前处于非健康状态的节点数。 |
| Physical Disk | 分类展示 IOMesh 集群中 SSD 和 HDD 的数量，包括所有 SSD 的数量、所有 HDD 的数量、所有处于非健康状态的 SSD 数量，以及所有处于非健康状态的 HDD 数量。 |
| Persistent Volume | 展示 IOMesh 集群中所有持久卷的数量。 |
| PV Status | 展示 IOMesh 集群中不同状态持久卷的数量。 |
| Total Storage Capacity | 展示 IOMesh 集群的总容量。 |
| Used Storage Capacity | 展示 IOMesh 集群的已使用容量。 |
| Total Storage Capacity Usage | 展示 IOMesh 集群已使用容量占集群总容量的百分比。 |
| Data Migrate & Recovery | 展示 IOMesh 集群中所有待迁移的数据量和迁移速度，待恢复的数据量和恢复速度。 |
| Cluster IOPS | 分别展示 IOMesh 集群在指定时间段的读、写、总 IOPS 的最小值/最大值/最新时间点的值。 |
| Cluster Average Latency | 分别展示 IOMesh 集群在指定时间段的读、写、总平均延迟的最小值/最大值/最新时间点的值。 |
| Cluster I/O Average Block Size | 分别展示 IOMesh 集群在指定时间段的读、写、总平均块大小的最小值/最大值/最新时间点的值。 |
| Cluster I/O Bandwidth | 分别展示 IOMesh 集群在指定时间段的读、写、总带宽的最小值/最大值/最新时间点的值。 |

## Node

**Node** 展示当前 IOMesh 集群中每个节点的基本信息。

| 字段 | 描述 | 示例 |
| --- | --- | --- |
| Name | 节点的名称。 | "node-1" |
| Namespace | 节点的名字空间。 | "iomesh-system" |
| Health Status | 节点的健康状态：   - `Initializing`：初始化中 - `Healthy`：健康 - `Error`：出错 | "Healthy" |
| Storage Capacity | 节点的总容量。 | "2 TiB" |
| Storage Capacity Usage | 节点的空间使用率。 | "20%" |
| Dirty Cache | 节点中脏数据占用的缓存空间。 | "5 GiB" |
| Cache Hit | 节点的读缓存命中率 \* 读操作比例 + 写缓存命中率 \* 写操作比例。 | "70%" |
| Overall IOPS | 节点的总 IOPS。 | "500 io/s" |
| Avg Latency | 节点的读写平均延迟。 | "1 us" |
| Migrate | 节点的数据迁移速度。 | "1000 B/s" |
| Recovery | 节点的数据恢复速度。 | "1000 B/s" |

## Details of Node

**Details of Node** 展示当前 IOMesh 集群中指定节点的数据迁移、数据恢复、性能数据等信息。

| 字段 | 描述 | 示例 |
| --- | --- | --- |
| Pending Migrate | 节点上待迁移的数据。 | "50.0 MiB" |
| Pending Recover | 节点上待恢复的数据。 | "50.0 MiB" |
| Invalid Cache Capacity | 节点中不可用的缓存空间。 | "50.0 MiB" |
| Invalid Storage Capacity | 节点中不可用的数据空间。 | "50.0 MiB" |
| Node IOPS | 节点在指定时间段的读、写 IOPS 的最小值/最大值/最新时间点的值。 | / |
| Node Average Latency | 节点在指定时间段的读、写平均延迟的最小值/最大值/最新时间点的值。 | / |
| Node I/O Average Block Size | 节点在指定时间段的读、写平均块大小的最小值/最大值/最新时间点的值。 | / |
| Node I/O Bandwidth | 节点在指定时间段的读、写带宽的最小值/最大值/最新时间点的值。 | / |

## Physical Disk

**Physical Disk** 展示当前 IOMesh 集群中物理盘的属性信息、健康状态、使用状态和用途。

| 字段 | 描述 | 示例 |
| --- | --- | --- |
| Device Name | 物理盘的名称。 | "dev/sdv" |
| Health Status | 物理盘的健康状态：   - `Healthy`：健康 - `Unhealthy`：不健康 - `Subhealthy`：亚健康 - `S.M.A.R.T not passed`：S.M.A.R.T. 不通过 | "Healthy" |
| Usage Status | 物理盘目前的使用状态：   - `Unmounted`：未挂载 - `Partially mounted`：部分挂载 - `Mounted`：已挂载 - `Unmounting`：卸载中 | "Mounted" |
| Remaining Lifetime | SSD 的剩余寿命。百分比值（%）越大，说明剩余寿命越长。 | "99%" |
| Type | 物理盘的种类，是物理盘的固有属性，包含 `SSD` 和 `HDD` 两种。 | "HDD" |
| Model | 硬盘自身的属性信息，可能会包含其品牌信息。 | "DL2400MM0159" |
| Serial Number | 物理盘的序列号。 | "WBM3C4TE" |
| Use | 物理盘的用途：   - `Datastore` - `Cache with journal` - `Datastore with journal` | "Datastore" |
| Capacity | 物理盘的总容量。 | "500 GiB" |
| Node | 物理盘所属的节点的名称。 | "node-1" |

## Persistent Volume

**Persistent Volume** 展示当前 IOMesh 集群中持久卷的属性信息、状态和使用情况。

| 字段 | 描述 | 示例 |
| --- | --- | --- |
| Name | PV 的名称。 | "Volume-1" |
| StorageClass | PV 所属的存储类的名称。 | "StorageClass1" |
| Status | PV 的状态：   - `Available`：PV 处于可用状态，尚未绑定到任何 PVC。 - `Bound`：PV 已经与某个 PVC 绑定。 - `Released`：PV 所绑定的 PVC 已删除，但资源尚未被集群回收。 - `Failed`：自动回收 PV 的操作失败。 - `Pending`：PV 已经创建成功，但需要等待 CSI 创建实体的存储资源。 | "Available" |
| Allocated Capacity | 分配给 PV 的逻辑容量。 | "50 GiB" |
| Exclusive Capacity | 此 PV 的独占逻辑容量。 | "25 GiB" |
| Shared Capacity | PV 和其他对象共享的逻辑容量。 | "10 GiB" |
| PV Provisioning | PV 的置备方式。  - `Thin provisioning`：精简置备 - `Thick provisioning`：厚置备 | "Thin provisioning" |
| Replicas | PV 的副本数, 包含 `2` 副本和 `3` 副本。 | "2" |
| Created Time | PV 的创建时间。 | "2022-12-08 14:45:00" |

---

## 监控集群 > 通过 UI 监控 IOMesh > 在 UI 中开启监控

# 在 UI 中开启监控

IOMesh 基于 Prometheus 和 Alertmanager 实现监控告警功能。在开启 UI 的监控功能前，请确保您已安装 Prometheus 和 Alertmanager。

## 启用 IOMesh 指标

1. 根据 IOMesh 安装方式，执行相应命令获取 `iomesh.yaml` 文件。

   - 在线安装

     ```
     helm -n iomesh-system get values iomesh -o yaml > iomesh.yaml
     ```
   - 离线安装

     ```
     ./helm -n iomesh-system get values iomesh -o yaml > iomesh.yaml
     ```
2. 编辑 `iomesh.yaml` 文件中的 `operator`、`iomesh` 和 `blockdevice monitor` 部分。

   - `operator`

     ```
     operator:
       metricsPort: 8080

       # Configure ServiceMonitor for Prometheus Operator.
       serviceMonitor:
         create: true # Set it to "true" to create a ServiceMonitor object, which defaults to "false".
         namespace: "" # Create a namespace for ServiceMonitor object. If left blank, "iomesh-system" will be specified.
         labels: {} # Set the label for ServiceMonitor object, which defaults to blank.

         # Configure Relabelings. See more information at <https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config>
         relabelings: [] # Set relabeling parameters for metrics, which defaults to blank.

       # Configure PrometheusRule for Prometheus Operator.
       prometheusRule:
         create: true # Set it to "true" to create a PrometheusRule object, which defaults to "false".
         namespace: "" # Create a namespace for PrometheusRule object.  If left blank, "iomesh-system" will be specified.
         labels: {} # Set the label for PrometheusRule object, which defaults to blank.
     ```
   - `iomesh`

     ```
     iomesh:
       # Configure ServiceMonitor for Prometheus Operator.
       serviceMonitor:
         create: true # Set it to true to create a serviceMonitor object, which defaults to false.
         namespace: "" # Create a namespace for serviceMonitor object. If left blank, "iomesh-system" will be specified.
         labels: {} # Set the label for serviceMonitor object, which defaults to blank.

      meta:
        serviceMonitor:
          # Configure Relabelings. See more information at <https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config>.
          relabelings: [] # Set relabeling parameters for metrics, which defaults to blank.
      chunk:
        serviceMonitor:
          # Configure Relabelings. See more information at <https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config>.
          relabelings: [] # Set relabeling parameters for metrics, which defaults to blank.
     ```
   - `blockdevice monitor`

     ```
     blockdevice-monitor:
       # Configure PodMonitor for Prometheus Operator.
       podMonitor:
         create: true # Set it to true to create a PodMonitor object, which defaults to false.
         namespace: "" # Create a namespace for PodMonitor object. If left blank, "iomesh-system" will be specified.
         labels: {} # Set the label for PodMonitor object, which defaults to blank.
       # Configure PrometheusRule for Prometheus Operator.
       prometheusRule:
         create: true # Set it to true to create a PrometheusRule object, which defaults to false.
         namespace: "" # Create a namespace for PrometheusRule object. If left blank, "iomesh-system" will be specified.
         labels: {} # Set the label for PrometheusRule object, which defaults to blank.

       blockdevicemonitor:
         podMonitor:
           # Configure Relabelings. See more information at <https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config>.
           relabelings: [] # Set relabelings parameters, which defaults to blank.

       prober:
         podMonitor:
           # Configure Relabelings. See more information at <https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config>.
           relabelings: [] # Set relabelings parameters, which defaults to blank.
     ```
3. 根据 IOMesh 安装方式，执行相应命令，使配置生效。

   - 在线安装

     ```
     helm -n iomesh-system upgrade iomesh iomesh/iomesh -f ./iomesh.yaml
     ```
   - 离线安装

     ```
     ./helm -n iomesh-system upgrade iomesh charts/iomesh -f ./iomesh.yaml
     ```
4. 确认相关的修改已生效。

   - `ServiceMonitor`

     ```
     kubectl -n iomesh-system get servicemonitor
     ```

     执行上述命令后，您将看到如下结果。

     ```
     NAME                 AGE
     iomesh               10m
     iomesh-operator      10m
     ```
   - `PodMonitor`

     ```
     kubectl -n iomesh-system get podmonitor
     ```

     执行上述命令后，您将看到如下结果。

     ```
     NAME                         AGE
     blockdevice-monitor          10m
     blockdevice-monitor-prober   10m
     ```
   - `PrometheusRule`

     ```
     kubectl -n iomesh-system get prometheusrule
     ```

     执行上述命令后，您将看到如下结果。

     ```
     NAME                 AGE
     blockdevicemonitor   10m
     iomesh               10m
     ```

## （可选）添加 Prometheus 权限

当 IOMesh 集群与 Prometheus 不在同一个名字空间下时，需要添加 Prometheus 权限以采集 IOMesh 指标。

**操作步骤**

下面以 IOMesh 集群所在名字空间为 `iomesh-cluster-1`，Prometheus 所在名字空间为 `monitoring` 为例进行介绍。

1. 编辑 ServiceMonitor 对象 `iomesh` 的 `spec.namespaceSelector.matchNames` 字段，添加需要监控的 IOMesh 集群的名字空间。

   ```
   kubectl -n iomesh-system edit servicemonitor iomesh
   ```

   ```
   apiVersion: monitoring.coreos.com/v1
   kind: ServiceMonitor
   metadata:
     name: iomesh
     namespace: iomesh-system
   spec:
     # ...
     namespaceSelector:
       matchNames:
         - iomesh-system
         - iomesh-cluster-1 # Add the namespace of the target IOMeshCluster.
     # ...
   ```
2. 编辑 IOMesh 集群所在名字空间下 RoleBinding 对象 `prometheus-iomesh` 的 `subjects` 字段，更新 Prometheus 所使用的 ServiceAccount 相关参数。

   ```
   kubectl -n iomesh-cluster-1 edit RoleBinding prometheus-iomesh
   ```

   ```
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     name: prometheus-iomesh
     namespace: iomesh-cluster-1
     # ...
   subjects:
     - kind: ServiceAccount
       name: prometheus # 更新为 Prometheus 所使用的 ServiceAccount 名。
       namespace: monitoring # 更新为 Prometheus 名字空间。
   ```
3. （可选）若 Kubernetes 集群中创建了多个与 Prometheus 不在同一名字空间的 IOMesh 集群，且均需进行监控，则每个 IOMesh 集群依次执行如上步骤即可。

## 为 UI 配置 Prometheus 连接

1. 根据 IOMesh 安装方式，执行相应命令获取 `iomesh.yaml` 文件。

   - 在线安装

     ```
     helm -n iomesh-system get values iomesh -o yaml > iomesh.yaml
     ```
   - 离线安装

     ```
     ./helm -n iomesh-system get values iomesh -o yaml > iomesh.yaml
     ```
2. 编辑 `iomesh.yaml` 文件中的 `deck` 部分。

   ```
   deck:
     alertmanager:
       address: alertmanager-operated.monitoring.svc.cluster.local:9093 # 需修改其中的 namespace 为 Alertmanager 所在的 namespace
       createNetworkPolicy: true
       matchLabels:
         app.kubernetes.io/name: alertmanager
       namespace: monitoring # 需修改为 Alertmanager 所在的 namespace
     prometheus:
       address: prometheus-operated.monitoring.svc.cluster.local:9090 # 需修改其中的 namespace 为 Prometheus 所在的 namespace
       createNetworkPolicy: true
       matchLabels:
         app.kubernetes.io/name: prometheus
       namespace: monitoring # 需修改为 Prometheus 所在的 namespace
   ```
3. 根据 IOMesh 安装方式，执行相应命令使修改生效。

   - 在线安装

     ```
     helm -n iomesh-system upgrade iomesh iomesh/iomesh -f ./iomesh.yaml
     ```
   - 离线安装

     ```
     ./helm -n iomesh-system upgrade iomesh charts/iomesh -f ./iomesh.yaml
     ```

**后续操作**

请在 UI 中为待监控的 IOMesh 集群开启监控。

1. 在左侧导航栏中单击 **IOMesh 集群列表**。
2. 找到待开启的集群，在**菜单**列选择**开启监控**，即可开启监控。

---

## 监控集群 > 通过 UI 监控 IOMesh > UI 监控信息

# UI 监控信息

## 集群总览

单击页面左上角的 **Deck**，可查看当前 Kubernetes 集群中所有 IOMesh 集群的概览信息。

- **基本信息**

  | 字段 | 描述 |
  | --- | --- |
  | IOMESH 集群 | 展示当前 IOMesh 集群的数量。 |
  | 节点 | 展示所有 IOMesh 节点的数量。 |
  | 持久卷 | 展示所有 IOMesh 相关的 PV 数量。 |
  | 存储 | 展示 IOMesh 集群的总容量、已使用容量和容量使用率。 |
- **性能监控**：当 IOMesh 集群可以访问 Promethues 时，可获取监控图表数据。

  | 图表 | 描述 |
  | --- | --- |
  | IOPS | 展示不同 IOMesh 集群过去 2 小时内的总 IOPS、读 IOPS 和写 IOPS。 |
  | I/O 带宽 | 展示不同 IOMesh 集群过去 2 小时内的总带宽、读带宽和写带宽。 |
  | I/O 平均延迟 | 展示不同 IOMesh 集群过去 2 小时内的总平均延迟、读平均延迟和写平均延迟。 |
  | I/O 平均块大小 | 展示不同 IOMesh 集群过去 2 小时内的总平均块大小、读平均块大小和写平均块大小。 |

## IOMesh 集群

1. 在左侧导航栏中单击 **IOMesh 集群列表**，可在列表中查看所有 IOMesh 集群的信息。

   | 字段 | 描述 |
   | --- | --- |
   | 名称 | 展示 IOMesh 集群的名称。 |
   | 名字空间 | 展示 IOMesh 集群所属的名字空间。 |
   | 版本号 | 展示 IOMesh 集群的版本。 |
   | 磁盘部署模式 | 展示 IOMesh 集群磁盘的配置类型，包括 `allFlash` 和 `hybridFlash`。 |
   | 就绪节点 | 展示 IOMesh 集群中的节点数量。 |
   | 总数据容量 | 展示 IOMesh 集群的总容量。 |
   | 已分配数据空间 | 展示 IOMesh 集群的已使用容量。 |
   | 创建时间 | 展示 IOMesh 集群被创建出的时长。 |
2. 单击某一 IOMesh 集群的**名称**链接，可查看该 IOMesh 集群的详细信息，以及相关的节点、块设备、Meta Pod、Chunk Pod 和存储类信息。

   - **基本信息**

     | 字段 | 描述 |
     | --- | --- |
     | 存储 | 展示 IOMesh 集群的总容量、已使用容量和容量使用率。 |
     | 许可证 | 展示 IOMesh 集群的许可过期时间，单击卡片可[查看许可信息](/iomesh_cn/1.2.0/user_guide/cluster-operations/manage-license#%E6%9F%A5%E7%9C%8B%E8%AE%B8%E5%8F%AF%E4%BF%A1%E6%81%AF)。 |
     | 迁移 | 展示 IOMesh 集群内待迁移的数据。 |
     | 恢复 | 展示 IOMesh 集群内待恢复的数据。 |
     | 标签 | 展示 IOMesh 集群的标签信息。 |
     | 注解 | 展示 IOMesh 集群的注释信息。 |
     | 属主 | 展示 IOMesh 集群的所有者。 |
     | 版本 | 展示 IOMesh 集群的部署版本，包括 `Community Edition` 和 `Enterprise Edition`。 |
     | 监控 | 当 IOMesh 集群开启监控时，展示为 `Enabled`，否则为 `Disabled`。 |
     | 外部 IP | 当使用 IOMesh 作为外部存储时，展示外部 IP。 |
   - **性能监控**：当 IOMesh 集群可以访问 Promethues 时，可获取监控图表数据。

     | 图表 | 描述 |
     | --- | --- |
     | IOPS | 展示当前 IOMesh 集群过去 2 小时内的总 IOPS、读 IOPS 和写 IOPS。 |
     | I/O 带宽 | 展示当前 IOMesh 集群过去 2 小时内的总带宽、读带宽和写带宽。 |
     | I/O 平均延迟 | 展示当前 IOMesh 集群过去 2 小时内的总平均延迟、读平均延迟和写平均延迟。 |
     | I/O 平均块大小 | 展示当前 IOMesh 集群过去 2 小时内的总平均块大小、读平均块大小和写平均块大小。 |

## 节点

1. 在集群详情页面单击**节点列表**可展开查看节点列表。

   | 字段 | 描述 |
   | --- | --- |
   | 名称 | 展示 IOMesh 节点的名称。 |
   | 状态 | 展示 IOMesh 节点的状态。 |
   | Chunk 状态 | 展示节点 Chunk 服务的健康状态。 |
   | 存储 IP | 展示节点的存储 IP。 |
   | 操作系统镜像 | 展示节点的 OS Image。 |
   | 存储容量 | 展示节点的总容量。 |
   | 已使用存储空间 | 展示节点的已使用容量。 |
   | 存储用量 | 展示节点的容量使用率。 |
2. 单击某一节点的**名称**链接，可查看该节点的详细信息，以及相关的块设备信息。当 IOMesh 集群可以访问 Promethues 时，可获取监控图表数据。

   - **基本信息**

     | 字段 | 描述 |
     | --- | --- |
     | 标签 | 展示节点的标签信息。 |
     | 注解 | 展示节点的注释信息。 |
     | 属主 | 展示节点的所有者。 |
     | IOMesh 集群 | 展示节点所属的 IOMesh 集群。 |
     | 脏缓存 | 展示节点中脏数据占用的缓存空间。 |
     | 失效缓存容量 | 展示节点中不可用的缓存空间。 |
     | 失效存储容量 | 展示节点中不可用的数据空间。 |
   - **性能监控**：当 IOMesh 集群可以访问 Promethues 时，可获取监控图表数据。

     | 图表 | 描述 |
     | --- | --- |
     | CPU 用量 | 展示节点过去 2 小时内的 CPU 平均使用率。 |
     | 内存用量 | 展示节点过去 2 小时内的 CPU 平均使用率。 |
     | IOPS | 展示节点过去 2 小时内的总 IOPS、读 IOPS 和写 IOPS。 |
     | I/O 带宽 | 展示节点过去 2 小时内的总带宽、读带宽和写带宽。 |
     | I/O 平均延迟 | 展示节点过去 2 小时内的总平均延迟、读平均延迟和写平均延迟。 |
     | I/O 平均块大小 | 展示节点过去 2 小时内的总平均块大小、读平均块大小和写平均块大小。 |

## 块设备

在集群详情页面单击**块设备列表** 可展开查看块设备信息，您也可以在左侧导航栏中单击**块设备列表**。相关字段说明请参考[查看块设备对象](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/setup-iomesh#%E6%9F%A5%E7%9C%8B%E5%9D%97%E8%AE%BE%E5%A4%87%E5%AF%B9%E8%B1%A1)。

## Meta Pods/Chunk Pods

1. 在集群详情页面单击 **Meta Pod 列表**或 **Chunk Pod 列表**可展开查看 Pods 信息。

   | 字段 | 描述 |
   | --- | --- |
   | 名称 | 展示 Pod 的名称。 |
   | 名字空间 | 展示 Pod 所属的名字空间。 |
   | 角色 | 如果是 Meta leader Pod，则显示 `Leader`。 |
   | 就绪 | 展示 Pod 内就绪的`容器数/容器总数`。 |
   | 状态 | 展示 Pod 的状态。 |
   | 重启次数 | 展示 Pod 中所有容器的累计重启次数以及上次重启时间。 |
   | 创建时间 | 展示 Pod 被创建出的时长。 |
   | IP | 展示 Pod 的 IP。 |
   | 节点 | 展示 Pod 所属的节点。 |
2. 单击某一 Pod 的**名称**链接，可查看该 Pod 的详细信息，以及相关的容器、卷、状况信息。

   - **基本信息**

     | 字段 | 描述 |
     | --- | --- |
     | 标签 | 展示 Pod 的标签信息。 |
     | 注解 | 展示 Pod 的注释信息。 |
     | 属主 | 展示管理该 Pod 的上层控制器或资源信息。 |
   - **性能监控**：当 IOMesh 集群可以访问 Promethues 时，可获取监控图表数据。

     | 图表 | 描述 |
     | --- | --- |
     | CPU 用量 | 展示 Pod 内的容器过去 2 小时内的 CPU 使用率。 |
     | 内存用量 | 展示 Pod 内的容器过去 2 小时内的内存使用率。 |
     | 磁盘 IOPS | 展示 Pod 内的容器过去 2 小时内的磁盘读 IOPS 和写 IOPS。 |
     | 网络带宽 | 展示 Pod 过去 2 小时内的网络接收带宽和传输带宽。 |
   - **容器**

     | 字段 | 描述 |
     | --- | --- |
     | 状态 | 展示容器当前的状态。 |
     | 就绪 | 展示容器是否已就绪。 |
     | 名称 | 展示容器的名称。 |
     | 镜像 | 展示容器使用的镜像名称。 |
     | Init | 展示该容器是否为初始化容器。 |
     | 重启次数 | 展示容器的重启次数。 |
     | 启动于 | 展示容器最后一次启动的时间。 |
   - **卷**

     | 字段 | 描述 |
     | --- | --- |
     | 名称 | 展示卷的名称。 |
     | 类型 | 展示卷的类型。 |
   - **状况**

     | 字段 | 描述 |
     | --- | --- |
     | 类型 | 展示条件的类型。 |
     | 状态 | 展示条件的状态。 |
     | 更新于 | 展示条件状态的最近变化时间。 |
     | 理由 | 展示条件状态改变的原因。 |
     | 消息 | 展示条件状态的详细信息。 |

## 存储类

在集群详情页面单击**存储类列表**可展开查看存储类信息，您也可以在左侧导航栏中单击**存储类列表**。相关字段说明请参考[创建存储类](/iomesh_cn/1.2.0/user_guide/volume-operations/create-storageclass)章节。

## 持久卷

在左侧导航栏中单击**持久卷列表**，可查看持久卷信息。相关字段说明请参考[创建持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/create-pv)章节。

## 持久卷申领

在左侧导航栏中单击**持久卷申领列表**，可查看持久卷申领信息。相关字段说明请参考[创建持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/create-pv)章节。

## 卷快照类

在左侧导航栏中单击**卷快照类列表**，可查看卷快照类列表信息。相关字段说明请参考[创建卷快照类](/iomesh_cn/1.2.0/user_guide/volumesnapshot-operations/create-snapshotclass)章节。

## 卷快照内容

在左侧导航栏中单击**卷快照内容列表**，可查看卷快照内容信息。相关字段说明请参考[创建卷快照](/iomesh_cn/1.2.0/user_guide/volumesnapshot-operations/create-volumesnapshot)章节。

## 卷快照

在左侧导航栏中单击**卷快照列表**，可查看卷快照信息。相关字段说明请参考[创建卷快照](/iomesh_cn/1.2.0/user_guide/volumesnapshot-operations/create-volumesnapshot)章节。

---

## 高级功能

# 高级功能

介绍 IOMesh 集群的高级功能，如部署、监控和管理多个集群，使用 IOMesh 作为外部存储等。

---

## 高级功能 > 管理多集群

# 管理多集群

在大规模 Kubernetes 集群中，可以通过部署多个 IOMesh 集群实现数据隔离。

所有 IOMesh 集群共享一个 IOMesh CSI Driver，这不仅方便连接，也减少了 CSI Driver 的 Pod 的个数。

![image](https://cdn.smartx.com/internal-docs/assets/64bec3fb/iomesh_02.png)

## 部署多集群

**前提条件**

- 确认部署环境满足[构建 IOMesh 集群的要求](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prerequisites)。
- IOMesh 的软件版本必须为 1.1.0 或以上。
- 单个 Kubernetes 集群最少应包含 6 个 Worker 节点。

**操作步骤**

下面以一个包含 6 个 Worker 节点的 Kubernetes 集群 `k8s-worker-{0-5}` 为例，描述在此 kubernetes 集群中部署 IOMesh 集群 `iomesh` 和 `iomesh-cluster-1` 的步骤。

| 集群名称 | 角色 | 名字空间 |
| --- | --- | --- |
| `iomesh` | IOMesh 集群 1 | `iomesh-system` |
| `iomesh-cluster-1` | IOMesh 集群 2 | `iomesh-cluster-1` |

### 部署第一个 IOMesh 集群 `iomesh`

**操作步骤**

参考[自定义在线安装](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/install-iomesh#%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9C%A8%E7%BA%BF%E5%AE%89%E8%A3%85)或[自定义离线安装](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/install-iomesh#%E8%87%AA%E5%AE%9A%E4%B9%89%E7%A6%BB%E7%BA%BF%E5%AE%89%E8%A3%85)方式部署 IOMesh，即可完成 `iomesh` 的部署。

（可选）在自定义在线安装或自定义离线安装的配置 `iomesh.yaml` 文件步骤，可增加如下配置以确保 Meta、Chunk、Zookeeper Pod 会被调度至 `k8s-worker-{0~2}` 节点。若不配置，则 Meta、Chunk、Zookeeper Pod 均会随机调度至 Kubernetes 集群中任意 3 个 Worker 节点上。

- 分别为 `iomesh.meta.podPolicy` 和 `iomesh.chunk.podPolicy` 配置 `nodeAffinity` 字段。

  ```
  iomesh:
    chunk:
      podPolicy:
        affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
              - matchExpressions:
                - key: kubernetes.io/hostname  # The key of the node label.
                  operator: In
                  values:  # The value of the node label.
                  - k8s-worker-0
                  - k8s-worker-1
                  - k8s-worker-2
    meta:
      podPolicy:
        affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
              - matchExpressions:
                - key: kubernetes.io/hostname  # The key of the node label.
                  operator: In
                  values:  # The value of the node label.
                  - k8s-worker-0
                  - k8s-worker-1
                  - k8s-worker-2
  ```
- 为 `iomesh.zookeeper` 设置 `nodeAffinity` 和 `podAntiAffinity` 字段。其中 `nodeAffinity` 字段将强制调度 Zookeeper Pod 至 `k8s-worker-{0~2}` 节点，而 `podAntiAffinity` 字段会确保每个节点仅运行一个 `zookeeper` Pod，以避免单点故障。

  1. 定位至 `iomesh.zookeeper.podPolicy` 字段，您将看到如下输出：

     ```
     ...
     iomesh:
     ...
       zookeeper:
         podPolicy:
           affinity:
     ```
  2. 复制并粘贴下面样例的代码，并设置 `key` 和 `values` 的取值。

     ```
      ...
      iomesh:
      ...
        zookeeper:
          podPolicy:
            affinity:
              nodeAffinity:
                requiredDuringSchedulingIgnoredDuringExecution:
                  nodeSelectorTerms:
                  - matchExpressions:
                    - key: kubernetes.io/hostname  # The key of the node label.
                      operator: In
                      values:  # The value of the node label.
                      - k8s-worker-0
                      - k8s-worker-1
                      - k8s-worker-2
              podAntiAffinity:
                preferredDuringSchedulingIgnoredDuringExecution:
                - podAffinityTerm:
                    labelSelector:
                      matchExpressions:
                      - key: app
                        operator: In
                        values:
                        - iomesh-zookeeper
                    topologyKey: kubernetes.io/hostname
                  weight: 20
     ```

### 部署第二个 IOMesh 集群 `iomesh-cluster-1`

1. 为 IOMesh 集群 `iomesh-cluster-1` 创建一个名字空间 `iomesh-cluster-1`。

   ```
   kubectl create namespace iomesh-cluster-1
   ```
2. 为 IOMesh 集群 `iomesh-cluster-1` 集群创建一个 Zookeeper 集群 `iomesh-cluster-1-zookeeper`。

   1. 创建一个 YAML 配置 `iomesh-cluster-1-zookeeper.yaml`，其详细信息如下。

      ```
      apiVersion: zookeeper.pravega.io/v1beta1
      kind: ZookeeperCluster
      metadata:
        namespace: iomesh-cluster-1
        name: iomesh-cluster-1-zookeeper
      spec:
        replicas: 3
        image:
          repository: iomesh/zookeeper
          tag: 3.5.9-20
          pullPolicy: IfNotPresent
        pod:
          securityContext:
            runAsUser: 0
          affinity:
            podAntiAffinity:
              preferredDuringSchedulingIgnoredDuringExecution:
              - podAffinityTerm:
                  labelSelector:
                    matchExpressions:
                    - key: app
                      operator: In
                      values:
                      - iomesh-cluster-1-zookeeper
                  topologyKey: kubernetes.io/hostname
                weight: 20
        persistence:
          reclaimPolicy: Delete
          spec:
            storageClassName: hostpath
            resources:
              requests:
                storage: 20Gi
      ```
   2. （可选）配置 `spec.image.repository` 字段。若在部署 IOMesh 集群 `iomesh` 时配置了 `global.registry` 参数，则需按照如下方式更新 zookeeper 集群 `iomesh-cluster-1-zookeeper` 中的 `repository` 字段，以确保可以从正确的镜像仓库拉取 zookeeper 镜像。

      ```
      spec:
        image:
          repository: <REGISTRY.YOURDOMAIN.COM:PORT>/iomesh/zookeeper
      ```
   3. （可选）配置 `spec.pod.affinity.nodeAffinity` 字段，以确保 Zookeeper Pod 被调度至 `k8s-worker-{3~5}` 节点。若不配置，则 Zookeeper Pod 会随机调度至 Kubernetes 集群中的任意 3 个 Worker 节点上。

      ```
      spec:
        pod:
          affinity:
            nodeAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                - matchExpressions:
                  - key: kubernetes.io/hostname  # The key of the node label.
                    operator: In
                    values:  # The value of the node label.
                    - k8s-worker-3
                    - k8s-worker-4
                    - k8s-worker-5
      ```
   4. 应用 `iomesh-cluster-1-zookeeper.yaml` 配置，创建 Zookeeper 集群 `iomesh-cluster-1-zookeeper`。

      ```
      kubectl apply -f iomesh-cluster-1-zookeeper.yaml
      ```
3. 创建 IOMesh 集群 `iomesh-cluster-1`。

   - **命令行方式**

     1. 创建一个 YAML 配置 `iomesh-cluster-1.yaml`，其详细信息和设置的字段如下。

        - 为 `spec.chunk` 和 `spec.redirector` 分别设置 `dataCIDR` 字段，其值为[网络要求](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prerequisites#%E7%BD%91%E7%BB%9C%E8%A6%81%E6%B1%82)中规划的 IOMesh 存储网络的 IP 网段 DATA\_CIDR。
        - 将 `spec.chunk.devicemanager.blockDeviceNamespace` 设置为 `iomesh-system`，管理组件和所有的块设备都位于该名字空间中。
        - 如果 CPU 架构为 Hygon x86\_64，需要将 `spec.platform` 字段设置为 `hygon_x86_64`，否则将自动安装 Intel 架构软件。
        - 如果使用的是企业版软件，需要将 `spec.edition` 字段设置为 `enterprise`，否则将自动安装社区版软件。
        - 根据实际的硬盘配置设置 `diskDeploymentMode`，可参考 [Worker 节点的硬件配置要求](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prerequisites#worker-%E8%8A%82%E7%82%B9%E7%9A%84%E7%A1%AC%E4%BB%B6%E9%85%8D%E7%BD%AE%E8%A6%81%E6%B1%82)进行确认。

        ```
        apiVersion: iomesh.com/v1alpha1
        kind: IOMeshCluster
        metadata:
          namespace: iomesh-cluster-1
          name: iomesh-cluster-1
        spec:
          diskDeploymentMode: hybridFlash
          platform: ""
          edition: ""
          storageClass: hostpath
          reclaimPolicy:
            volume: Delete
            blockdevice: Delete
          meta:
            replicas: 3
            image:
              repository: iomesh/zbs-metad
              pullPolicy: IfNotPresent
          chunk:
            dataCIDR: <your-data-cidr-here>  # Fill in IOMesh data CIDR.
            replicas: 3
            image:
              repository: iomesh/zbs-chunkd
              pullPolicy: IfNotPresent
            devicemanager:
              image:
                repository: iomesh/operator-devicemanager
                pullPolicy: IfNotPresent
              blockDeviceNamespace: iomesh-system
          redirector:
            dataCIDR: <your-data-cidr-here>  # Fill in IOMesh data CIDR.
            image:
              repository: iomesh/zbs-iscsi-redirectord
              pullPolicy: IfNotPresent
          probe:
            image:
              repository: iomesh/operator-probe
              pullPolicy: IfNotPresent
          toolbox:
            image:
              repository: iomesh/operator-toolbox
              pullPolicy: IfNotPresent
        ```
     2. （可选）配置 IOMesh 集群中所有 `image.repository` 字段。若在部署 IOMesh 集群 `iomesh` 时配置了 `global.registry` 参数，则需按照如下方式更新 IOMesh 集群 `iomesh-cluster-1` 中所有 `image.repository` 字段，以确保可以从正确的镜像仓库拉取 IOMeshCluster 相关镜像。

        ```
        spec:
          meta:
            image:
              repository: <REGISTRY.YOURDOMAIN.COM:PORT>/iomesh/zbs-metad
          chunk:
            image:
              repository: <REGISTRY.YOURDOMAIN.COM:PORT>/iomesh/zbs-chunkd
            devicemanager:
              image:
                repository: <REGISTRY.YOURDOMAIN.COM:PORT>/iomesh/operator-devicemanager
          redirector:
            image:
              repository: <REGISTRY.YOURDOMAIN.COM:PORT>/iomesh/zbs-iscsi-redirectord
          probe:
            image:
              repository: <REGISTRY.YOURDOMAIN.COM:PORT>/iomesh/operator-probe
          toolbox:
            image:
              repository: <REGISTRY.YOURDOMAIN.COM:PORT>/iomesh/operator-toolbox
        ```
     3. （可选）配置 `spec.iomesh.meta.podPolicy` 和 `spec.iomesh.chunk.podPolicy` 字段，以确保 Meta 和 Chunk Pod 会被调度至 `k8s-worker-{3~5}` 节点。若不配置，则 Meta Pod 会随机调度至 Kubernetes 集群中任意 3 个未启动 Meta 的 Worker 节点上；Chunk Pod 会随机调度至 Kubernetes 集群中任意 3 个未启动 Chunk 的 Worker 节点上。

        ```
        spec:
          meta:
            podPolicy:
              affinity:
                nodeAffinity:
                  requiredDuringSchedulingIgnoredDuringExecution:
                    nodeSelectorTerms:
                    - matchExpressions:
                      - key: kubernetes.io/hostname  # The key of the node label.
                        operator: In
                        values:  # The value of the node label.
                        - k8s-worker-3
                        - k8s-worker-4
                        - k8s-worker-5
          chunk:
            podPolicy:
              affinity:
                nodeAffinity:
                  requiredDuringSchedulingIgnoredDuringExecution:
                    nodeSelectorTerms:
                    - matchExpressions:
                      - key: kubernetes.io/hostname  # The key of the node label.
                        operator: In
                        values:  # The value of the node label.
                        - k8s-worker-3
                        - k8s-worker-4
                        - k8s-worker-5
        ```
     4. 应用 `iomesh-cluster-1.yaml` 配置，创建 IOMesh 集群 `iomesh-cluster-1`。

        ```
        kubectl apply -f iomesh-cluster-1.yaml -n iomesh-cluster-1
        ```
   - **UI 方式**

     1. 在左侧导航栏中单击 **IOMesh 集群列表**。
     2. 单击 **+**，创建 IOMesh 集群。
     3. 根据如下说明配置相关字段。

        | 字段 | 描述 |
        | --- | --- |
        | 名称 | IOMesh 集群的名称。 |
        | 名字空间 | IOMesh 集群所属的名字空间。您可以参考命令行方式的步骤 1 提前创建所需的名字空间。 |
        | 版本 | IOMesh 集群的部署版本，包括`社区版`和`企业版`。 |
        | 海光 x86\_64 平台 | 仅当平台类型为 Hygon x86\_64 时需勾选此项。 |
        | 磁盘部署模式 | IOMesh 集群的部署模式，包括`全闪`和`混闪`。 |
        | 存储网络 CIDR | IOMesh 集群存储网络的 IP 网段，请参考[网络规划](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prerequisites#%E7%BD%91%E7%BB%9C%E8%A6%81%E6%B1%82)要求填写。 |
        | Meta Pod 数量 | IOMesh 集群内 Meta Pod 数量，支持 3 或 5。 |
        | Chunk Pod 数量 | IOMesh 集群内 Chunk Pod 数量。  最小为 3，最大为当前 Kubernetes 集群中未部署 IOMesh 的 Worker Node 数。 |
        | 节点选择器 | 通过键值对设置 IOMesh 待部署的节点。 |
     4. 单击**创建**。

### 挂载硬盘

1. [查看块设备对象](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/setup-iomesh#%E6%9F%A5%E7%9C%8B%E5%9D%97%E8%AE%BE%E5%A4%87%E5%AF%B9%E8%B1%A1)，确认所有的块设备都位于同一个名字空间 `iomesh-system` 。

   ```
   kubectl --namespace iomesh-system -o wide get blockdevice
   ```
2. [配置设备映射](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/setup-iomesh#%E9%85%8D%E7%BD%AE%E8%AE%BE%E5%A4%87%E6%98%A0%E5%B0%84)。

   ```
   kubectl edit iomesh iomesh -n iomesh-system # Configure deviceMap for the first IOMesh cluster.
   kubectl edit iomesh iomesh-cluster-1 -n iomesh-cluster-1 # Configure deviceMap for the second IOMesh cluster.
   ```

### 为 IOMesh 集群创建存储类

在多集群场景下，只有随 IOMesh 安装时部署的 IOMesh 集群 `iomesh` 可以使用默认的存储类 `iomesh-csi-driver`，其余每个 IOMesh 集群均需为其创建一个单独的存储类。

**操作步骤**

下面以命令行方式为例介绍如何为 IOMesh 集群 `iomesh-cluster-1` 创建一个存储类，您也可以使用 UI 方式[创建存储类](/iomesh_cn/1.2.0/user_guide/volume-operations/create-storageclass)。

```
# Source: iomesh-cluster-1-sc.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: iomesh-cluster-1
parameters:
  csi.storage.k8s.io/fstype: ext4
  replicaFactor: "2"
  thinProvision: "true"
  iomeshCluster: "iomesh-cluster-1/iomesh-cluster-1" # The namespace and name of the IOMesh cluster.
volumeBindingMode: Immediate
provisioner: com.iomesh.csi-driver
reclaimPolicy: Delete
allowVolumeExpansion: true
```

执行如下命令，使配置生效。

```
kubectl apply -f iomesh-cluster-1-sc.yaml
```

### 验证部署结果

利用默认存储类 `iomesh-csi-driver` 和新存储类 `iomesh-cluster-1` 分别创建一个新的 PVC，以此验证 IOMesh 集群是否均已完成部署。

下面以命令行方式为例进行介绍，您也可以使用 UI 方式[创建持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/create-pv)。

1. 为 IOMesh 集群 `iomesh` 创建一个 PVC。

   ```
   # Source: iomesh-pvc.yaml
   kind: PersistentVolumeClaim
   apiVersion: v1
   metadata:
     name: iomesh-pvc
   spec:
     storageClassName: iomesh-csi-driver
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 1Gi
   ```

   ```
   kubectl apply -f iomesh-pvc.yaml
   ```
2. 为 IOMesh 集群 `iomesh-cluster-1` 创建一个 PVC。

   ```
   # Source: iomesh-cluster1-pvc.yaml
   kind: PersistentVolumeClaim
   apiVersion: v1
   metadata:
     name: iomesh-cluster-1-pvc
   spec:
     storageClassName: iomesh-cluster-1
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 1Gi
   ```

   ```
   kubectl apply -f iomesh-cluster1-pvc.yaml
   ```

## 监控多集群

要监控多个 IOMesh 集群，请参考[监控集群](/iomesh_cn/1.2.0/user_guide/monitor-iomesh/monitor-iomesh-1)配置监控。完成配置后，您可以选择目标集群及其名字空间，在 Grafana Dashboard 或 UI 上查看其存储性能。

## 多集群运维

多集群场景下，每个 IOMesh 集群的扩容、缩容、更新许可、更换硬盘操作步骤与[单集群运维](/iomesh_cn/1.2.0/user_guide/cluster-operations/cluster-operations-1)基本一致，只需在对应命令中指定需要操作的 IOMesh 集群；每个 IOMesh 集群的性能优化操作步骤也与[优化 IOMesh 性能](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/performance-tips)基本一致，仅需注意若[配置 CPU 核心绑定与独占](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/performance-tips#%E9%85%8D%E7%BD%AE-cpu-%E6%A0%B8%E5%BF%83%E7%BB%91%E5%AE%9A%E4%B8%8E%E7%8B%AC%E5%8D%A0)，则每个集群只能使用相同的核心绑定模式，即 **Kubelet CPUManager 模式**和 **Kernel Parameter 模式**只能二选一。

### 删除集群

**注意事项**

在执行删除 IOMesh 集群操作前，必须先删除所有 IOMesh 创建的 PVC 和使用了 IOMesh PVC 的用户 Pod。否则，直接删除 IOMesh 集群会导致所有数据未按用户预期的清理顺序清空，并且会在重新创建 IOMesh 集群时出现错误。

**操作步骤**

以删除[部署多集群](#%E9%83%A8%E7%BD%B2%E5%A4%9A%E9%9B%86%E7%BE%A4)时创建的 IOMesh 集群 `iomesh-cluster-1` 为例。

1. 删除 IOMesh 集群 `iomesh-cluster-1`。

   - **命令行方式**

     ```
     kubectl delete iomesh iomesh-cluster-1 -n iomesh-cluster-1
     ```
   - **UI 方式**

     1. 在左侧导航栏中单击 **IOMesh 集群列表**。
     2. 找到待删除的集群 `iomesh-cluster-1`，在**菜单**列选择**删除**。
     3. 在弹出的对话框中单击 **Confirm** 完成删除。
2. 删除 IOMesh 集群 `iomesh-cluster-1` 对应 zookeeper 集群 `iomesh-cluster-1-zookeeper`。

   - **命令行方式**

     ```
     kubectl delete zk iomesh-cluster-1-zookeeper -n iomesh-cluster-1
     ```
   - **UI 方式**

     删除 IOMesh 集群后即可自动进行 zookeeper 集群删除。
3. （可选）若已为 IOMesh 集群 `iomesh-cluster-1` [添加 Prometheus 权限](/iomesh_cn/1.2.0/user_guide/monitor-iomesh/installing-iomesh-dashboard#%E5%8F%AF%E9%80%89%E6%B7%BB%E5%8A%A0-prometheus-%E6%9D%83%E9%99%90)，则需删除权限。

   ```
   kubectl edit servicemonitor iomesh -n iomesh-system
   ```

   ```
   apiVersion: monitoring.coreos.com/v1
   kind: ServiceMonitor
   metadata:
     name: iomesh
     namespace: iomesh-system
   spec:
     # ...
     namespaceSelector:
       matchNames:
         - iomesh-system
         - iomesh-cluster-1 # 删除该行以删除 Prometheus 权限。
     # ...
   ```
4. （可选）删除 IOMesh 集群 `iomesh-cluster-1` 所在的名字空间。

   ```
   kubectl delete namespace iomesh-cluster-1
   ```

### 升级多集群

1. 执行单集群运维中[升级集群](/iomesh_cn/1.2.0/user_guide/cluster-operations/upgrade-cluster)的操作步骤，确保 IOMesh 相关 Pod 在执行升级完成后是 `running` 状态。
2. 对每一个非默认集群的 IOMesh Zookeeper 对象执行如下命令：

   ```
   kubectl edit zk -n <namespace>
   ```

   修改镜像版本号字段为 3.5.9-20

   ```
   spec:
    image:
      tag: 3.5.9-20 # 修改为 3.5.9-20
   ```
3. 执行如下命令验证所有 IOMesh Pod 最终进入 `running` 状态：

   `kubectl get pod -n <namespace>`

### 卸载多集群

与单集群运维中[卸载集群](/iomesh_cn/1.2.0/user_guide/cluster-operations/uninstall-cluster)的操作步骤完全一致，在执行卸载后所有 IOMesh 集群均会被卸载。

---

## 高级功能 > IOMesh LocalPV Manager

# IOMesh LocalPV Manager

## 简介

### 什么是 IOMesh LocalPV Manager？

IOMesh LocalPV Manager 是用于管理 Kubernetes Worker 节点本地存储的 CSI 驱动程序。一些有状态的应用如分布式对象存储 [Minio](https://min.io/)，分布式数据库 [TiDB](https://github.com/pingcap/tidb) 等在应用层即可实现数据的高可用。如果在多副本的 IOMesh PV 上运行它们会在数据路径中增加一层复制（目前 IOMesh 不支持单副本），这会导致一定程度的性能下降和空间浪费。

IOMesh LocalPV Manager 允许使用本地存储（如目录或块设备）创建 PV 来供 Pod 使用，成功地避免了此问题。

相较于 [Kubernetes HostPath Volume](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath) 和 [Kubernetes 原生的 local PV](https://kubernetes.io/docs/concepts/storage/volumes/#local)，IOMesh LocalPV Manager 具有如下优势：

- 使用 StorageClass、PVC 动态制备 PV，实现灵活访问存储，不需要管理员预先制备静态 PV。
- 允许使用块设备创建 PV，提供更卓越的 I/O 性能和更大的灵活性，而 Kubernetes local PV 只支持使用节点上的目录。
- 使用节点上的目录作为本地存储时，IOMesh LocalPV Manager 支持 PV 级别的容量限额。

### 架构

![image](https://cdn.smartx.com/internal-docs/assets/64bec3fb/iomesh_04.png)

IOMesh LocalPV Manager 由以下组件组成：

- **Controller Driver**

  标准的 CSI Controller Server 实现。每个 Kubernetes Worker 节点都有一个实例。Controller Driver 与 kube-apiserver 进行交互，负责创建和删除 local PV，以及管理 PV 与本地目录或块设备的关系映射。
- **Node Driver**

  标准的 CSI Node Server 实现。每个 Kubernetes Worker 节点都有一个实例。Node Driver 与 kubelet 进行交互，负责 LocalPV 的挂载与格式化。
- **Node Disk Manager**

  一个用于发现节点块设备，并将块设备抽象成 BlockDevice 对象的组件。Node Disk Manager 提供 BlockDeviceClaim 机制，确保某个 Pod 独占某个块设备。

### 支持的 Local PV 类型

IOMesh LocalPV Manager 制备的 Local PV 有两种类型：`HostPath` 和 `Device`。

- `HostPath`：使用节点上的本地目录创建的 Local PV 即为 `HostPath` 类型，支持启用 PV 级别的容量限制。
- `Device`：使用块设备创建的 Local PV 即为 `Device` 类型，可以挂载给 Pod 使用。

在选择卷类型时，需要考虑当前的应用或数据库的对存储的需要：如果需要独占一个磁盘或需要一个裸设备，则选择 Device；否则选择 HostPath 类型的 Local PV 也可满足要求。

## 部署 IOMesh LocalPV Manager

安装 IOMesh 过程中将自动安装 IOMesh LocalPV Manager，并作为一个 Pod 在每个 Worker 节点上运行。执行如下命令，查看 IOMesh LocalPV Manager Pod 的状态。

```
kubectl get pod -n iomesh-system | grep localpv-manager
```

```
NAME                                                           READY   STATUS             RESTARTS   AGE
iomesh-localpv-manager-rjg8j                                   4/4     Running            0          10s
iomesh-localpv-manager-vphz9                                   4/4     Running            0          10s
iomesh-localpv-manager-w4j8m                                   4/4     Running            0          10s
```

## 创建 HostPath Local PV

- **命令行方式**

  1. 部署 IOMesh LocalPV Manager 时，将同时创建一个默认的存储类，`volumeType` 字段的值设置为 `hostPath`。

     ```
     apiVersion: storage.k8s.io/v1
     kind: StorageClass
     metadata:
       name: iomesh-localpv-manager-hostpath
     parameters:
       volumeType: hostpath
       basePath: /var/iomesh/local
       enableQuota: "false" 
     provisioner: com.iomesh.iomesh-localpv-manager
     reclaimPolicy: Delete
     volumeBindingMode: WaitForFirstConsumer
     ```

     您也可以创建一个自定义的存储类，各字段的取值设置请参考下表，操作步骤可参考[创建存储类](/iomesh_cn/1.2.0/user_guide/volume-operations/create-storageclass)。

     | 字段 | 描述 |
     | --- | --- |
     | `parameters.volumeType` | Local PV 类型：`hostpath` 或者 `device`。该字段被设置为 `hostpath` 时表示 IOMesh Hostpath Local PV。 |
     | `parameters.basePath` | 创建的 local PV 的目录。如果该字段未被指定，系统将会为其创建一个默认的目录。  **说明：** `parameters.basePath` 的值必须设置为一个完整的路径。 |
     | `parameters.enableQuota` | 展示使用该存储类的 local PV 是否启用了容量限制，默认为不启用(`false`)。 |
     | `reclaimPolicy` | 当 PVC 被删除时，此字段决定了是否保留 Local PV。  - `Retain`：删除 PVC 将会保留 Local PV 以及对应节点上的 Volume 目录，即使手动删除 PV 也不会清理该目录。 - `Delete`：删除 PVC 将会删除 Local PV 以及对应节点上的 Volume 目录。 |
     | [`volumeBindingMode`](https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode) | 控制何时动态制备和卷绑定 local PV。IOMesh LocalPV 只支持 `WaitForFirstConsumer` 模式。 |
  2. 使用存储类创建一个 PVC。

     1. 按照如下内容创建一个 YAML 配置 `iomesh-localpv-hostpath-pvc.yaml`。

        ```
        kind: PersistentVolumeClaim
        apiVersion: v1
        metadata:
          name: iomesh-localpv-hostpath-pvc
        spec:
          storageClassName: iomesh-localpv-manager-hostpath # If you use a StorageClass with custom parameters, specify its name.
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: 2Gi
        ```
     2. 执行如下命令，使 YAML 配置生效，创建 PVC。

        ```
        kubectl apply -f iomesh-localpv-hostpath-pvc.yaml
        ```
     3. 查看 PVC。

        ```
        kubectl get pvc iomesh-localpv-hostpath-pvc
        ```

        您将看到 PVC 处于 `Pending` 状态，因为所使用的存储类的 `volumeBindingMode` 被配置为 `WaitForFirstConsumer`。只有当 PVC 绑定到某个 Pod，并且 Pod 所在的节点上创建了相应的 PV 时，PVC 才会转换到 `Bound` 状态。

        ```
        NAME                          STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS              AGE
        iomesh-localpv-hostpath-pvc   Pending                                      localpv-manager-hostpath  1m12s
        ```
  3. 创建一个 Pod，然后将其绑定到上一步骤所创建的 PVC。

     1. 按照如下内容创建一个 YAML 配置 `iomesh-localpv-hostpath-pod.yaml`，将 PVC 挂载到 Pod 所在的 `/mnt/iomesh/localpv` 目录。

        ```
        apiVersion: v1
        kind: pod
        metadata:
          name: iomesh-localpv-hostpath-pod
        spec:
          volumes:
          - name: iomesh-localpv-hostpath
            persistentVolumeClaim:
              claimName: iomesh-localpv-hostpath-pvc
          containers:
          - name: busybox
            image: busybox
            command:
              - sh
              - -c
              - 'while true; do sleep 30; done;'
            volumeMounts:
            - mountPath: /mnt/iomesh/localpv
              name: iomesh-localpv-hostpath
        ```
     2. 执行如下命令，使 YAML 配置生效，创建 Pod。

        ```
        kubectl apply -f iomesh-localpv-hostpath-pod.yaml
        ```
     3. 验证 Pod 处于 `Running` 状态。

        ```
        kubectl get pod iomesh-localpv-hostpath-pod
        ```
  4. 验证 PVC 处于 `Bound` 状态，以及与其对应的 PV 已经创建完毕。

     - 查看 PVC 的配置。

       ```
       kubectl get pvc iomesh-localpv-hostpath-pvc
       ```

       ```
       NAME                          STATUS   VOLUME                                     CAPACITY   ACCESS MODES     
       iomesh-localpv-hostpath-pvc   Bound    pvc-ab61547e-1d81-4086-b4e4-632a08c6537b   2G         RWO
       ```
     - 查看 PV 的配置。将下面命令中的 `pvc-ab61547e-1d81-4086-b4e4-632a08c6537b` 替换为从上述输出结果中获取的 PV 的名称。

       ```
       kubectl get pv pvc-ab61547e-1d81-4086-b4e4-632a08c6537b -o yaml
       ```

       ```
       apiVersion: v1
       kind: PersistentVolume
       metadata:
       ...
       spec:
       ...
         csi:
           driver: com.iomesh.iomesh-localpv-manager
           volumeAttributes:
             basePath: /var/iomesh/local
             csi.storage.k8s.io/pv/name: pvc-ab61547e-1d81-4086-b4e4-632a08c6537b
             csi.storage.k8s.io/pvc/name: iomesh-localpv-hostpath-pvc
             csi.storage.k8s.io/pvc/namespace: default
             enableQuota: "false"
             nodeID: iomesh-k8s-0
             quotaProjectID: "0"
             storage.kubernetes.io/csiProvisionerIdentity: 1675327643130-8081-com.iomesh.localpv-manager
             volumeType: hostpath
           volumeHandle: pvc-ab61547e-1d81-4086-b4e4-632a08c6537b
         nodeAffinity:
           required:
             nodeSelectorTerms:
             - matchExpressions:
               - key: topology.iomesh-localpv-manager.csi/node
                 operator: In
                 values:
                 - iomesh-k8s-0
       ...
       ```

       | 字段 | 描述 |
       | --- | --- |
       | `spec.csi.volumeAttributes.basePath` | `basePath` 由 IOMesh local PV 创建。以上述 YAML 配置为例，PV 的目录创建在 `iomesh-k8s-0` 节点的 `/var/iomesh/local/pvcab61547e-1d81-4086-b4e4-632a08c6537b`。 |
       | `spec.nodeAffinity` | PV 节点亲和性。PV 一旦创建后就会被绑定到指定的节点上，而不会移动到其他节点上。 |
- **UI 方式**

  1. 在左侧导航栏中单击**存储类列表**，创建存储类。

     部署 IOMesh LocalPV Manager 时，将同时创建一个**类型**为 `LocalPV（HostPath）` 的存储类；您也可以单击 **+** 自定义存储类，**类型**需选择 `LocalPV (HostPath)`，并设置相应字段。

     | 字段 | 描述 |
     | --- | --- |
     | [卷绑定模式](https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode) | 控制何时动态制备和卷绑定 local PV。IOMesh LocalPV 只支持 `WaitForFirstConsumer` 模式。 |
     | 基路径 | 创建的 local PV 的目录。如果该字段未被指定，系统将会为其创建一个默认的目录。  **说明：** 基路径的值必须设置为一个完整的路径。 |
     | 开启配额 | 展示使用该存储类的 local PV 是否启用了容量限制，默认为不启用。 |
     | 回收策略 | 当 PVC 被删除时，此字段决定了是否保留 Local PV。  - `Retain`：删除 PVC 将会保留 Local PV 以及对应节点上的 Volume 目录，即使手动删除 PV 也不会清理该目录。 - `Delete`：删除 PVC 将会删除 Local PV 以及对应节点上的 Volume 目录。 |
  2. 在左侧导航栏中单击**持久卷申领列表**，单击 **+** > **新建本地主机路径持久卷申领**，使用上述存储类创建 PVC。

     | 字段 | 描述 |
     | --- | --- |
     | 名称 | PVC 的名称。 |
     | 名字空间 | PVC 所属的名字空间。  使用该 PVC 的业务 Pod 需和 PVC 在同一名字空间才能挂载。 |
     | 存储类名称 | PVC 使用的存储类。 |
     | 卷模式 | PVC 使用的卷模式，仅支持 `Filesystem`。 |
     | 容量 | PVC 的存储容量，单位为 Ki、Mi、Gi 或 Ti。 |
     | 访问模式 | PVC 的访问模式，仅支持 `ReadWriteOnce`。 |
  3. 参考命令行方式中的步骤 3，创建一个 Pod，然后将其绑定到上一步骤所创建的 PVC。
  4. 在左侧导航栏中分别单击**持久卷申领列表**和**持久卷列表**，验证 PVC 和 PV 的状态。

## 为 HostPath Local PV 启用容量限制

上面命令行示例描述了在对应节点上的目录创建一个 2G 容量的 IOMesh HostPath Local PV 的步骤。默认情况下，对于写入该目录的数据量没有限制，允许写入超过 2G。但如果您有容量隔离的要求，可以对 HostPath Local PV 启用容量限制。

要使用 `xfs_quota` 工具的容量限制功能，存储类中的 `parameters.basePath` 应该是一个 XFS 格式的挂载点，并将挂载选项设置为启用 XFS `prjquota` 功能。一旦启用后，系统将创建一个配置 `xfs quota` 的 HostPath local PV，其容量为 PVC 中所声明的容量。

**操作步骤**

下面以在 `/var/iomesh/localpv-quota` 目录下创建 HostPath Local PV，其磁盘路径为 `/dev/sdx` 为例，描述创建启用容量限制的 PV 的方法。

1. 创建一个目录 `/var/iomesh/localpv-quota` 作为 `basePath`。

   ```
   mkdir -p /var/iomesh/localpv-quota
   ```
2. 将磁盘的文件系统格式化为 `xfs`，其中磁盘路径为 `/dev/sdx`。

   ```
   sudo mkfs.xfs /dev/sdx
   ```
3. 将磁盘挂载到 `/var/iomesh/localpv-quota` 目录，并将挂载选项设置为启用 XFS `prjquota`。

   ```
   mount -o prjquota /dev/sdx /var/iomesh/localpv-quota
   ```

   > **说明：**
   >
   > - 如果希望使用一个现有的 XFS 挂载点作为 basePath，执行 `umount /dev/sdx` 命令，卸载挂载点。然后通过 `prjquota` 挂载选项重新挂载它。
   > - 为了防止重启节点后挂载信息丢失，请将挂载信息写入 `/etc/fstab` 配置文件中。
4. 创建一个将这个挂载点当作 `basePath` 的存储类，设置 `parameters.enableQuota` 字段为 `true`。如您通过 UI 方式创建存储类，则需要勾选**开启配额**以启用容量限制。

   ```
   apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: iomesh-localpv-manager-hostpath-example
   parameters:
     volumeType: hostpath
     basePath: /var/iomesh/localpv-quota
     enableQuota: "true" # To enable capacity limit, set it to "true". Default value is "false".
   provisioner: com.iomesh.iomesh-localpv-manager
   reclaimPolicy: Delete
   volumeBindingMode: WaitForFirstConsumer
   ```
5. 使用上一步骤所创建的存储类创建一个 PVC。

   > **说明：**
   >
   > 本版本不支持调度器。该 Pod 可能会被调度到一个容量不足的节点上。此时应该手动修改这个 Pod 的节点亲和性，以便它可以被重新调度到一个合适的节点上。如何修改 Pod 的节点亲和性，请参考 Kubernetes 的官方文档 [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)。

## 创建 IOMesh Device Local PV

IOMesh Device Local PV 支持基于节点上的块状设备创建 Local PV，供 Pod 挂载使用。

**操作步骤**

- **命令行方式**

  1. IOMesh LocalPV Manager 部署成功后，将创建一个默认的存储类，如下图所示。其中 `volumeType` 字段设置为 `device`。

     ```
     apiVersion: storage.k8s.io/v1
     kind: StorageClass
     metadata:
       name: iomesh-localpv-manager-device
     parameters:
       volumeType: device
       csi.storage.k8s.io/fstype: "ext4"
       deviceSelector: ""
     provisioner: com.iomesh.iomesh-localpv-manager
     reclaimPolicy: Delete
     volumeBindingMode: WaitForFirstConsumer
     ```

     您也可以创建一个自定义的存储类，各字段的取值设置请参考下表，操作步骤可参考[创建存储类](/iomesh_cn/1.2.0/user_guide/volume-operations/create-storageclass)。

     | 字段 | 描述 |
     | --- | --- |
     | `parameters.volumeType` | Local PV 类型：`hostpath` 或者 `device`。该字段被设置为 `device` 时表示 IOMesh device local PV。 |
     | `parameters.deviceSelector` | 设备选择器，通过标签筛选块设备。如果该字段未被指定，则默认筛选所有的标签。 |
     | `parameters.csi.storage.k8s.io/fstype` | 文件系统类型，默认为 `ext4`，还可支持 `xfs`、`ext2`、`ext3`。 |
     | `reclaimPolicy` | 当 PVC 被删除时，此字段决定了是否保留 Local PV。  - `Retain`：删除 PVC 将会保留 Local PV 以及对应本地块设备中的数据，即使手动删除 PV 也不会清理该本地块设备。 - `Delete`：删除 PVC 将会删除 Local PV 并清理对应的本地块设备。 |
     | `volumeBindingMode` | 控制何时动态制备和卷绑定 local PV。IOMesh LocalPV 只支持 `WaitForFirstConsumer` 模式。 |

     创建自定义存储类时，您可以配置 `deviceSelector` 用以筛选磁盘。关于配置的细节，请参考[设备选择器](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/setup-iomesh#%E9%85%8D%E7%BD%AE%E8%AE%BE%E5%A4%87%E6%98%A0%E5%B0%84)和 [Kubernetes Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)。

     下面所示的 `iomesh.com/bd-driveType: SSD` 表示在创建 Local PV 时存储类将只筛选 SSD。

     ```
     apiVersion: storage.k8s.io/v1
     kind: StorageClass
     metadata:
       name: iomesh-localpv-manager-device-ssd
     parameters:
       volumeType: device
       deviceSelector: |
         matchLabels:
           iomesh.com/bd-driverType: SSD
     provisioner: com.iomesh.iomesh-localpv-manager
     reclaimPolicy: Delete
     volumeBindingMode: WaitForFirstConsumer
     ```

     > **说明：**
     >
     > 在存储类中配置 `parameters` 时，Kubernetes 只支持嵌套一级键/值，因此在 `deviceSelector` 字段中须添加 `|`，以确保系统将后续内容当作一个多行字符串进行处理。
  2. 使用存储类创建一个 PVC。

     为保证创建 PVC 成功，请确保每个 Kubernetes Worker 节点至少有 1 个可用裸设备，并且没有指定文件系统。

     1. 按照如下内容创建一个 YAML 配置 `iomesh-localpv-device-pvc.yaml`。根据文件系统格式化的要求，将 `volumeMode` 字段设置为 `filesystem` 或者 `block`。

        - `Filesystem`：作为一个文件系统来访问存储。设置为 `Filesystem` 后，块设备将被格式化为存储类的 `parametersfsType` 字段所指定的文件系统类型，并在 Pod 被绑定到这个 PVC 后，挂载给 Pod 使用。
        - `Block`：作为一个裸设备访问存储。它不需要格式化文件系统，可以直接提供给低延迟和高带宽要求的高性能应用来使用，如数据库或其他存储密集的工作负载。

        ```
        kind: PersistentVolumeClaim
        apiVersion: v1
        metadata:
          name: iomesh-localpv-device-pvc
        spec:
          storageClassName: iomesh-localpv-manager-device
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: 10Gi # Specify the storage value.
          volumeMode: Filesystem
        ```
     2. 执行如下命令，使 YAML 配置生效，创建 PVC。

        ```
        kubectl apply -f iomesh-localpv-device-pvc.yaml
        ```
     3. 查看 PVC 的状态。

        ```
        kubectl get pvc iomesh-localpv-device-pvc
        ```

        您将看到 PVC 处于 `Pending` 状态，因为所使用的存储类的 `volumeBindingMode` 被配置为 `WaitForFirstConsumer`只有当 PVC 绑定到某个 Pod，并且 Pod 所在的节点上创建了相应的 PV 时，PVC 才会转换到 `Bound` 状态。

        ```
        NAME                          STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS              AGE
        iomesh-localpv-device-pvc     Pending                                      localpv-manager-device    1m12s
        ```
  3. 创建一个 Pod，并将其与上一步骤所创建的 PVC 绑定。

     1. 按照如下内容创建一个 YAML 配置 `iomesh-localpv-device-pod.yaml`，挂载 PV 至 `/mnt/iomesh/localpv` 目录。

        ```
        apiVersion: v1
        kind: pod
        metadata:
          name: iomesh-localpv-device-pod
        spec:
          volumes:
          - name: iomesh-localpv-device
            persistentVolumeClaim:
              claimName: iomesh-localpv-device-pvc
          containers:
          - name: busybox
            image: busybox
            command:
              - sh
              - -c
              - 'while true; do sleep 30; done;'
            volumeMounts:
            - mountPath: /mnt/iomesh/localpv # The directory to mount the PV.
              name: iomesh-localpv-device
        ```
     2. 执行如下命令，使 YAML 配置生效，创建 Pod。

        ```
        kubectl apply -f iomesh-localpv-device-pod.yaml
        ```
     3. 确认 Pod 处于 `Running` 状态。

        ```
        kubectl get pod iomesh-localpv-device-pod
        ```

        > **说明：**
        >
        > 本版本不支持调度器。该 Pod 可能会被调度到一个容量不足的节点上。此时应该手动修改这个 Pod 的节点亲和性，以便它可以被重新调度到一个合适的节点上。如何修改 Pod 的节点亲和性，请参考 Kubernetes 的官方文档 [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)。
  4. 确认 PVC 处于 `Bound` 状态。

     ```
     kubectl get pvc iomesh-localpv-device-pvc
     ```

     执行上述命令后，您将看到 PVC 显示为 `Bound` 状态，并成功创建 PV。

     ```
     NAME                          STATUS   VOLUME                                     CAPACITY   ACCESS MODES     
     iomesh-localpv-device-pvc     Bound    pvc-72f7a6ab-a9c4-4303-b9ba-683d7d9367d4   10G        RWO
     ```
  5. 检查块设备是否处于 `Claimed` 状态。

     ```
     kubectl  get blockdevice --namespace iomesh-system -o wide
     ```

     ```
     NAMESPACE       NAME                                           NODENAME            SIZE             CLAIMSTATE   STATUS   AGE
     iomesh-system   blockdevice-072560a15c89a324aadf7eb4c9b233f2   iomesh-node-17-18   1920383410176    Claimed      Active   160m
     iomesh-system   blockdevice-1189c24046a6c43da37ddf0e40b5c1de   iomesh-node-17-19   1920383410176    Claimed      Active   160m
     ```

     上一步骤中 PVC 所绑定的 Pod 的节点上的块设备须满足以下两个要求：容量必须超过或等于 PVC 的容量，并且在所有可用的块设备中，该块设备的容量须最接近 PVC 的容量。

     例如，对于申报了一个 10GB 的 PVC，如果有 3 个块设备：

     - `BlockDevice-A`（9GB）
     - `BlockDevice-B`（15GB）
     - `BlockDevice-C`（20GB）

     则应选择 `BlockDevice-B` 进行绑定，因为其容量比 `BlockDevice-C` 更接近 10GB，而 `BlockDevice-A` 由于其容量限制而被排除。
  6. 查看新建的 PV 的配置信息。执行命令时请将 `pvc-72f7a6ab-a9c4-4303-b9ba-683d7d9367d4` 替换为步骤 4 中所查询到的 PV 的名称。

     ```
     kubectl get pv pvc-72f7a6ab-a9c4-4303-b9ba-683d7d9367d4 -o yaml
     ```

     您将看到如下输出：

     ```
     apiVersion: v1
     kind: PersistentVolume
     metadata:
     ...
     spec:
     ...
       csi:
         driver: com.iomesh.iomesh-localpv-manager
         volumeAttributes:
           csi.storage.k8s.io/pv/name: pvc-72f7a6ab-a9c4-4303-b9ba-683d7d9367d4
           csi.storage.k8s.io/pvc/name: iomesh-localpv-device-pvc
           csi.storage.k8s.io/pvc/namespace: default
           nodeID: iomesh-node-17-19
           quotaProjectID: "0"
           storage.kubernetes.io/csiProvisionerIdentity: 1675327673777-8081-com.iomesh.localpv-manager
           volumeType: device
         volumeHandle: pvc-72f7a6ab-a9c4-4303-b9ba-683d7d9367d4
       nodeAffinity:
         required:
           nodeSelectorTerms:
           - matchExpressions:
             - key: topology.iomesh-localpv-manager.csi/node
               operator: In
               values:
               - iomesh-node-17-19
     ...
     ```

     | 字段 | 描述 |
     | --- | --- |
     | `spec.csi.volumeAttributes.volumeHandle` | BlockDeviceClaim 的唯一标识。 |
     | `spec.nodeAffinity` | PV 节点亲和性。PV 在创建后，将会立即被绑定到指定的节点上，而且不会移动到其他节点。 |
- **UI 方式**

  1. 在左侧导航栏中单击**存储类列表**，创建存储类。

     部署 IOMesh LocalPV Manager 时，将同时创建一个**类型**为 `LocalPV（Device）` 的存储类；您也可以单击 **+** 自定义存储类，**类型**需选择 `LocalPV (Device)`，并设置相应字段。

     | 字段 | 描述 |
     | --- | --- |
     | 卷绑定模式 | 控制何时动态制备和卷绑定 local PV。IOMesh LocalPV 只支持 `WaitForFirstConsumer` 模式。 |
     | 文件系统类型 | 文件系统类型，默认为 `ext4`，还可支持 `xfs`、`ext2`、`ext3`。 |
     | 回收策略 | 当 PVC 被删除时，此字段决定了是否保留 Local PV。  - `Retain`：删除 PVC 将会保留 Local PV 以及对应本地块设备中的数据，即使手动删除 PV 也不会清理该本地块设备。 - `Delete`：删除 PVC 将会删除 Local PV 并清理对应的本地块设备。 |
  2. 在左侧导航栏中单击**持久卷申领列表**，单击 **+** > **新建本地块设备持久卷申领**，使用上述存储类创建 PVC。

     | 字段 | 描述 |
     | --- | --- |
     | 名称 | PVC 的名称。 |
     | 名字空间 | PVC 所属的名字空间。  使用该 PVC 的业务 Pod 需和 PVC 在同一名字空间才能挂载。 |
     | 存储类名称 | PVC 使用的存储类。 |
     | 卷模式 | PVC 使用的卷模式，支持 `Block` 和 `Filesystem`。 |
     | 容量 | PVC 的存储容量，单位为 Ki、Mi、Gi 或 Ti。 |
     | 访问模式 | PVC 的访问模式，仅支持 `ReadWriteOnce`。 |
  3. 参考命令行方式中的步骤 3，创建一个 Pod，然后将其绑定到上一步骤所创建的 PVC。
  4. 在左侧导航栏中分别单击**持久卷申领列表**和**持久卷列表**，验证 PVC 和 PV 的状态。

---

## 高级功能 > 使用 IOMesh 作为外部存储

# 使用 IOMesh 作为外部存储

除了为 IOMesh 所在的 Kubernetes 环境提供存储服务外，IOMesh 还支持通过 CSI Driver 向外部的 Kubernetes 集群提供存储服务，或使用标准 iSCSI 协议向 iSCSI 客户端提供存储服务。

## （可选）配置接入网络

为避免网卡资源抢占，建议使用单独的接入网络来对外提供存储服务，以达到更好的存储性能和稳定性。

> **说明：**
>
> - 使用[一键在线安装](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/install-iomesh#%E4%B8%80%E9%94%AE%E5%9C%A8%E7%BA%BF%E5%AE%89%E8%A3%85)的方式部署 IOMesh 时，默认未配置接入网络，您可以在集群部署完成后单独配置；如使用[自定义在线安装](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/install-iomesh#%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9C%A8%E7%BA%BF%E5%AE%89%E8%A3%85)或[自定义离线安装](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/install-iomesh#%E8%87%AA%E5%AE%9A%E4%B9%89%E7%A6%BB%E7%BA%BF%E5%AE%89%E8%A3%85)，则既可以在部署 IOMesh 的过程中直接配置，也可以在集群部署完成后单独配置。
> - 如您在部署 IOMesh 集群时配置接入网络，则配置完成后使用 `helm install` 直接进行集群部署即可；如为已部署的 IOMesh 集群，则配置完成后需使用 `helm upgrade` 进行集群配置更新。

**前提条件**

确认部署环境满足[构建 IOMesh 集群的要求](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prerequisites)章节中对于接入网络的[网络要求](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prerequisites#%E7%BD%91%E7%BB%9C%E8%A6%81%E6%B1%82)。

**操作步骤**

假设接入网络的网段规划为 `10.100.1.0/24`，下面以 IOMesh 集群已部署完成为例进行操作介绍。

1. 修改 IOMesh 配置文件 `iomesh.yaml`，在 `iomesh.chunk.extraEnvs` 字段中新增 `ACCESS_CIDR` 环境变量。

   ```
   iomesh:
     chunk:
       extraEnvs:
         ACCESS_CIDR: "10.100.1.0/24" # 参考网络要求修改为实际规划的接入网段
   ```
2. 执行如下命令，Chunk Pod 会逐个重启并生效配置。

   ```
   helm upgrade --namespace <iomeshcluster-namespace> <iomeshcluster-name> iomesh/iomesh --values iomesh.yaml # 根据实际环境替换<xx>
   ```

## 配置 iSCSI 接入点

通过 CSI Driver 或 iSCSI Target 使用 IOMesh 存储，首先必须配置一个 iSCSI 接入点。

IOMesh 采用 `LoadBalancer` 类型的 `iomesh-access` 服务，以确保 iSCSI 接入点的高可用性和 IP 地址的稳定性。使用该服务必须对外暴露 IP 地址，配置此 IP 的具体方法因部署 IOMesh 的云环境不同而有所不同。

- 若 IOMesh 部署在[支持负载均衡的云环境](https://kubernetes.io/docs/concepts/services-networking/service/#internal-load-balancer)中，请参考 [In-Tree LoadBalancer](#in-tree-loadbalancer)。
- 若 IOMesh 部署在裸金属或者其他不支持负载均衡的云环境中，请参考 [Out-of-Tree LoadBalancer](#out-of-tree-loadbalancer)。

### In-Tree LoadBalancer

若 IOMesh 部署在支持负载均衡（`LoadBalancer`）的云环境中，Kubernetes 将自动调用云提供商的 API，并为 `iomesh-access` 服务分配一个外部 IP。

**操作步骤**

1. 检查 IOMesh 集群所在名字空间下 `iomesh-access` 服务的状态，确保已经为其分配一个外部 IP。

   ```
   kubectl get service iomesh-access -n <iomeshcluster-namespace>
   ```

   ```
   NAME            TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)                                                          AGE
   iomesh-access   LoadBalancer   10.96.22.212   192.168.2.1     3260:32012/TCP,10206:31920/TCP,10201:31402/TCP,10207:31802/TCP   45h
   ```
2. 执行如下命令，将 IOMesh 集群的 `spec.redirector.iscsiVirtualIP` 字段设置为 `iomesh-access` 服务的外部 IP。完成编辑后，IOMesh 集群所在名字空间下的 `iomesh-iscsi-redirector` Pod 将自动重启，使配置生效。

   ```
   kubectl edit iomesh <iomeshcluster-name> -n <iomeshcluster-namespace>
   ```

   > **说明：**
   >
   > - `spec.redirector.iscsiVirtualIP` 字段的值必须设置为与外部 IP 相同，如果外部 IP 有更改，请对应更新 `spec.redirector.iscsiVirtualIP` 字段的值。
   > - 本步骤也可以通过 UI 方式操作：在 **IOMesh 集群列表**页面选择某一 IOMesh 集群，在**菜单**列选择**开启外部访问**，确认后即可将 `iscsiVirtualIP` 设置为 `iomesh-access` 服务的外部 IP。
3. （可选）若 Kubernetes 集群中创建了多个 IOMesh 集群，且均需提供外部存储，则每个 IOMesh 集群依次执行如上步骤即可。

### Out-of-Tree LoadBalancer

若 IOMesh 部署在裸金属上，或者在不支持 Kubernetes 负载均衡的云环境中，则必须安装 `MetalLB`，作为 Kubernetes 集群默认的负载均衡器（`LocalBalancer`）。

**操作步骤**

1. 确认 Kubernetes 集群满足 [MetalLB 安装要求](https://metallb.universe.tf/installation/#preparation)。
2. 安装 `MetalLB`。

   ```
   helm repo add metallb https://metallb.github.io/metallb
   helm install metallb metallb/metallb --version 0.13.12 -n metallb-system --create-namespace
   ```
3. 创建一个 `MetalLB` 的 IPAddressPool `iomesh-address-pools.yaml`。

   - 在 `addresses` 字段设置 IP 池。IP 池必须是一个 IP 范围，如 "192.168.1.100-192.168.1.110"；或者是一个 CIDR，如 "192.168.2.0/24"。此外，您可以通过配置子网掩码为 `32` 来指定唯一的 IP，如 "192.168.2.1/32"。
   - 如您配置了单独的接入网络，则 `addresses` 字段中设置的 IP 池必须属于 `ACCESS_CIDR` 网段。
   - 在 `serviceAllocation.namespaces` 字段设置 IOMesh 集群所在的名字空间。

   ```
   apiVersion: metallb.io/v1beta1
   kind: IPAddressPool
   metadata:
     namespace: metallb-system
     name: iomesh-access-address-pools
   spec:
     addresses:
     - <fill-in-your-ip-address-pool-here> # Fill in an IP pool.
     serviceAllocation:
       namespaces:
         - <iomeshcluster-namespace> # Fill in IOMeshCluster's namespace
   ```

   执行如下命令，使 YAML 配置生效。

   ```
   kubectl apply -f iomesh-address-pools.yaml
   ```
4. 再创建一个 `MetalLB` 的 L2Advertisement `iomesh-advertisement.yaml`。

   - `ipAddressPools` 设置为上一步中创建的 IPAddressPool 的名称。
   - `interfaces` 设置为 IOMesh 集群所在名字空间下 iomesh-chunk Pod 所在节点的存储网卡名。如您配置了单独的接入网络，则需配置为接入网卡名。
   - `nodeSelectors` 配置为 IOMesh 集群所在名字空间下 iomesh-chunk Pod 所在节点名，若后续进行 Chunk 扩缩容则需对应更新该配置。

   ```
   apiVersion: metallb.io/v1beta1
   kind: L2Advertisement
   metadata:
     name: iomesh-access-advertisement
     namespace: metallb-system
   spec:
     ipAddressPools:
     - iomesh-access-address-pools
     interfaces:
     - eth0
     nodeSelectors:
     - matchLabels:
         kubernetes.io/hostname: NodeA
     - matchLabels:
         kubernetes.io/hostname: NodeB
   ```

   执行如下命令，使 YAML 配置生效。

   ```
   kubectl apply -f iomesh-advertisement.yaml
   ```
5. 检查 IOMesh 集群所在名字空间下 `iomesh-access` 服务的状态，确保 `MetalLB` 已被分配来自 IP 池的外部 IP。

   ```
   kubectl get service iomesh-access -n <iomeshcluster-namespace>
   ```

   ```
   NAME            TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)                                                          AGE
   iomesh-access   LoadBalancer   10.96.22.212   192.168.2.1     3260:32012/TCP,10206:31920/TCP,10201:31402/TCP,10207:31802/TCP   45h
   ```
6. 执行如下命令，将 IOMesh 集群的 `spec.redirector.iscsiVirtualIP` 字段设置为 `iomesh-access` 服务的外部 IP。完成编辑后，IOMesh 集群所在名字空间下的 `iomesh-iscsi-redirector` Pod 将自动重启，使配置生效。

   ```
   kubectl edit iomesh <iomeshcluster-name> -n <iomeshcluster-namespace>
   ```

   > **说明：**
   >
   > - `spec.redirector.iscsiVirtualIP` 字段的值必须设置为与外部 IP 相同，如果外部 IP 有更改，请对应更新 `spec.redirector.iscsiVirtualIP` 字段的值。
   > - 本步骤也可以通过 UI 方式操作：在 **IOMesh 集群列表**页面选择某一 IOMesh 集群，在**菜单**列选择**开启外部访问**，确认后即可将 `iscsiVirtualIP` 设置为 `iomesh-access` 服务的外部 IP。
7. （可选）若 Kubernetes 集群中创建了多个 IOMesh 集群，且均需提供外部存储，则每个 IOMesh 集群依次执行如上步骤 3 ～ 6 即可。

## 使用 CSI Driver 从集群外部接入 IOMesh

配置完 iSCSI 接入点后，IOMesh 可以向外部 Kubernetes 集群提供存储服务。但在接入 IOMesh 存储前，请参考下面的步骤，在 Kubernetes 集群中**在线安装** IOMesh CSI Driver。

![image](https://cdn.smartx.com/internal-docs/assets/64bec3fb/iomesh_03.png)

**前提条件**

- 使用此功能前，应首先确保外部 Kubernetes 集群可以访问[网络要求](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prerequisites#%E7%BD%91%E7%BB%9C%E8%A6%81%E6%B1%82)中所规划的 IOMesh 存储网络的 IP 网段 `DATA_CIDR`。如您配置了单独的接入网络，则应确保外部 Kubernetes 集群可以访问接入网络的 IP 网段 `ACCESS_CIDR`。
- 当 Kubernetes 集群服务器的 CPU 架构为鲲鹏 AArch64 时，应确保其 Kubernetes 版本不低于 1.22。
- 请提前在 IOMesh 集群所在的 Kubernetes 集群中执行如下命令，获取 `iscsiVirtualIP` 和 `iscsiServerPort`。

  ```
  kubectl get iomesh <iomeshcluster-name> -n <iomeshcluster-namespace>
  ```

  如下输出所示，`iscsiVirtualIP` 对应 `ISCSIVIRTUALIP` 字段的值 `192.168.2.1`，`iscsiServerPort` 对应 `ISCSISERVERPORT` 字段的值 `3260`。

  ```
  NAME     VERSION      DISKDEPLOYMENTMODE   NODES   READYNODES   ISCSIVIRTUALIP   ISCSISERVERPORT   TOTALDATACAPACITY   ALLOCATEDDATASPACE   CLUSTERID   AGE
  iomesh   v1.2.0       hybridFlash          3       3            192.168.2.1      3260              1.38Ti              20.00Gi              1           10d
  ```

**操作步骤**

1. 在外部 Kubernetes 集群的 Worker 节点上[设置 open-iscsi](/iomesh_cn/1.2.0/user_guide/appendices/setup-open-iscsi)。
2. 添加 Helm chart repository。

   ```
   helm repo add iomesh http://iomesh.com/charts
   ```
3. 导出 IOMesh CSI Driver 配置文件 `csi-driver.yaml`。

   ```
   helm show values iomesh/csi-driver > csi-driver.yaml
   ```
4. 在 `csi-driver.yaml` 文件中编辑如下字段。

   ```
    fullnameOverride: "iomesh-csi-driver"
    # ...
    # Specify the container platform, either "kubernetes" or "openshift". 
    co: "kubernetes" 
    # Specify the container platform version, which should be the same as the version of the cluster hosting IOMesh.
    coVersion: "1.18"
    # ...
    storageClass:
      nameOverride: "iomesh-csi-driver"
      parameters:
        csi.storage.k8s.io/fstype: "ext4"
        replicaFactor: "2"
        thinProvision: "true"
    # ...
    driver:
      # ...
      # The Kubernetes cluster ID.
      clusterID: "my-iomesh"
      # IOMesh meta server iSCSI portal address.
      metaAddr: "iscsiVirtualIP:10206"
      # IOMesh chunk server iSCSI portal address.
      iscsiPortal: "iscsiVirtualIP:iscsiServerPort"
      # Total number of CSI Driver PVs that can be mounted on a single node.
      maxVolumesPerNode: "128"
      # Access IOMesh as external storage.
      deploymentMode: "EXTERNAL"
      # The unique CSI Driver name in the Kubernetes cluster.
      nameOverride: "com.iomesh.csi-driver"
      # ...
      controller:
        driver:
          podDeletePolicy: "no-delete-pod"
      node:
        driver:
          # ...
          # The root directory of `kubelet` service.
          kubeletRootDir: "/var/lib/kubelet"
      # ...
   ```

   | **字段** | **取值/示例** | **描述** |
   | --- | --- | --- |
   | fullnameOverride | `"iomesh-csi-driver"` | CSI Driver 名称。 |
   | co | `"kubernetes"` | 容器平台。如果您使用的是 OpenShift 平台，请设置为 `openshift`。 |
   | coVersion | `"1.18"` | 容器平台的版本，须与 IOMesh 所在的集群的容器平台版本相同。 |
   | storageClass.nameOverride | `"iomesh-csi-driver"` | 默认的存储类名称，在安装时可以自定义。 |
   | storageClass.parameters | `"parameters"` | 默认存储类的参数，该参数在安装过程中可以自定义。 |
   | driver.clusterID | `"my-iomesh"` | Kubernetes 集群 ID，当 IOMesh 为多个 Kubernetes 集群提供存储时，该 ID 用于识别集群。 |
   | driver.metaAddr | `"iscsiVirtualIP:10206"` | IOMesh Meta 服务器的 iSCSI 门户地址。 |
   | driver.iscsiPortal | `"iscsiVirtualIP:​iscsiServerPort"` | IOMesh Chunk 服务器的 iSCSI 门户地址。 |
   | driver.maxVolumesPerNode | `"128"` | 单节点可挂载 IOMesh CSI Driver PV 总数。取值范围为 `0 ～ 256`，不配置或配置为 `0` 时使用默认值 `128`。 |
   | driver.deploymentMode | `"EXTERNAL"` | `EXTERNAL` 表示使用 IOMesh 作外部存储。 |
   | driver.controller.driver​.podDeletePolicy | `"no-delete-pod"`（默认值）  `"delete-deployment-pod"`  `"delete-statefulset-pod"`  `"delete-both-statefulset-and-deployment-pod"` | 当使用 IOMesh CSI Driver 创建 PVC 时，该 PVC 将与一个 Pod 绑定。该字段决定当 Pod 原来的 Worker 节点出现故障时，是否允许自动删除 Pod，然后在另外一个健康的 Worker 节点上自动重建。 |
   | driver.node.driver​.kubeletRootDir | `"/var/lib/kubelet"` | `kubelet` 服务的根目录，用于管理 Pod 所挂载的卷。默认值 `/var/lib/kubelet`。 |
5. 部署 IOMesh CSI Driver。

   ```
   helm install csi-driver iomesh/csi-driver \
       --namespace iomesh-system \
       --create-namespace \
       --values csi-driver.yaml \
       --wait
   ```
6. 检查 IOMesh CSI Driver 是否已成功安装。当所有的 Pod 都显示为 `Running` 状态，则表示已成功安装。

   ```
   watch kubectl get --namespace iomesh-system pods
   ```

   ```
   NAME                                                   READY   STATUS    RESTARTS   AGE
   iomesh-csi-driver-controller-plugin-5dbfb48d5c-2sk97   6/6     Running   0          42s
   iomesh-csi-driver-controller-plugin-5dbfb48d5c-cfhwt   6/6     Running   0          42s
   iomesh-csi-driver-controller-plugin-5dbfb48d5c-drl7s   6/6     Running   0          42s
   iomesh-csi-driver-node-plugin-25585                    3/3     Running   0          39s
   iomesh-csi-driver-node-plugin-fscsp                    3/3     Running   0          30s
   iomesh-csi-driver-node-plugin-g4c4v                    3/3     Running   0          39s
   ```

安装完 IOMesh CSI Driver 后，请参考[卷操作](/iomesh_cn/1.2.0/user_guide/volume-operations/volume-operations-1)和[卷快照操作](/iomesh_cn/1.2.0/user_guide/volumesnapshot-operations/volumesnapshot-operations-1)进行后续的存储操作。

## 使用 iSCSI Target 接入 IOMesh 存储

IOMesh 提供外部 iSCSI 接入服务。您可以通过创建一个 PVC 来创建一个 iSCSI LUN，该 iSCSI LUN 支持通过任何 iSCSI 客户端进行访问，例如位于 Kubernetes 集群之外的 `open-iscsi`，可参考[设置 open-iscsi](/iomesh_cn/1.2.0/user_guide/appendices/setup-open-iscsi) 来进行 open-iscsi 的安装和配置。

**前提条件**

使用此功能前，应首先确保 iSCSI 客户端可以访问[网络要求](/iomesh_cn/1.2.0/user_guide/deploy-iomesh-cluster/prerequisites#%E7%BD%91%E7%BB%9C%E8%A6%81%E6%B1%82)中所规划的 IOMesh 存储网络的 IP 网段 `DATA_CIDR`。如您配置了单独的接入网络，则应确保外部 Kubernetes 集群可以访问接入网络的 IP 网段 `ACCESS_CIDR`。

### 使用 PVC 创建 iSCSI LUN

1. 创建一个 PVC 作为外部 iSCSI LUN。执行命令 `cat /etc/iscsi/initiatorname.iscsi` 可以获取 iSCSI 客户端的 IQN。

   | UI 字段 | 对应 YAML 字段 | 描述 |
   | --- | --- | --- |
   | 外部使用 | `iomesh.com/external-use` | PVC 是否可用于外部访问，默认为 `false`，可按需修改为 `true`。 |
   | IQN 准许列表 | `iomesh.com/iscsi-lun-iqn-allow-list` | 当外部使用为 `true` 时，您需要为作为 iSCSI LUN 的 PVC 设置 IQN 白名单。 - 留空时所有外部客户端均不能访问该 PVC。 - 当访问模式为 `ReadWriteOnce` 时，仅能设置一个外部客户端。 - 当访问模式为 `ReadWriteMany` 时，可配置多个客户端，须用 "," 隔开。 - 如需允许所有客户端访问该 PVC，则可将值设置为 `*/*`。 |

   - **命令行方式**

     参考如下 YAML 定义一个 PVC。

     ```
     apiVersion: v1
     kind: PersistentVolumeClaim
     metadata:
       name: external-iscsi
       annotations:
         # Mark this PVC as an iSCSI LUN for external use.
         iomesh.com/external-use: "true"
         # Set `initiator iqn acl` for iSCSI LUN. If left unspecified, all initiators will be prohibited from accessing this PVC.
         # If `accessModes` is `RWO`, you can only set 1 value in this field.
         # If `accessModes` is `RWX`, you can set multiple values in this field and separate them with the comma (,).
         # To allow all IQNs to access this PVC, set the value to "*/*".
         iomesh.com/iscsi-lun-iqn-allow-list: "iqn.1994-05.com.example:a6c97f775dcb"
     spec:
       storageClassName: iomesh-csi-driver
       accessModes:
         - ReadWriteOnce
       resources:
         requests:
           storage: 1Gi
     ```

     > **说明：**
     >
     > 您也可以在创建完 PVC 后再设置 `iomesh.com/iscsi-lun-iqn-allow-list` 字段的值。
   - **UI 方式**

     1. 在左侧导航栏中单击**持久卷申领列表**。
     2. 单击 **+** > **新建 IOMesh 持久卷申领**。
     3. 参考[创建普通持久卷](/iomesh_cn/1.2.0/user_guide/volume-operations/create-pv)的字段说明设置基础字段，并设置**外部使用**和 **IQN 准许列表**。
     4. 单击**创建**。
2. 一旦 PVC 转换至 `Bound` 状态，执行如下命令查看 `spec.volumeAttributes.iscsiEntrypoint` 字段。

   ```
   kubectl get pv pvc-d84b4657-7ab5-4212-9270-ce40e6a1356a -o jsonpath='{.spec.csi.volumeAttributes.iscsiEndpoint}'
   ```

   ```
   iscsi://cluster-loadbalancer-ip:3260/iqn.2016-02.com.smartx:system:54e7022b-2dcc-4b43-800c-e52b6fad07d3/1
   # The IP of iSCSI Portal is the cluster LoadBalancer IP, and port number is 3260.
   # The target is `iqn.2016-02.com.smartx:system:54e7022b-2dcc-4b43-800c-e52b6fad07d3`.
   # LUN ID is 1.
   ```

   从上述信息可知，您可以使用任意 iSCSI 客户端来访问 iSCSI LUN。例如，`cluster-loadbalancer-ip` 为 192.168.25.101，iscsiServerPort 为 3260，iSCSI 客户端为 `open-iscsi`，则可以执行以下命令来访问 LUN：

   ```
   iscsiadm -m discovery -t sendtargets  -p 192.168.25.101:3260 --discover
   iscsiadm -m node -T iqn.2016-02.com.smartx:system:54e7022b-2dcc-4b43-800c-e52b6fad07d3 -p 192.168.25.101:3260  --login
   ```

### 删除 PVC

为了删除 iSCSI LUN 对应的 PVC，需要确保 PVC 中的 `iomesh.com/iscsi-lun-iqn-allow-list` 字段为空白，或者该字段已经删除。

删除 PVC 后是否保留外部 iSCSI LUN，取决于 PVC 的存储类中的 `reclaimPolicy` 字段的取值为 `Delete` 还是 `Retain`。

---

## 附录 > 设置 open-iscsi

# 设置 open-iscsi

open-iscsi 是使用 RFC3720 iSCSI 协议实现的高性能 Initiator 程序。在安装并配置完 open-iscsi 后，Kubernetes 各节点可以直接访问 IOMesh 集群的 iSCSI 数据存储，像使用本地块存储服务一样方便。

在以下场景中，您需要手动安装并设置 `open-iscsi`：

- 首次安装 IOMesh 时，Kubernetes 集群中所有可调度的节点将自动启动 `prepare-csi` Pod 来安装和设置 `open-iscsi`。若所有节点的 `open-iscsi` 安装成功，系统将自动清理 `prepare-csi` Pod。若某个节点的 `open-iscsi` 安装失败，即 `prepare-csi` Pod 不断失败退出，则可以查看对应 Pod 日志或通过手动设置 open-iscsi 来确认 `open-iscsi` 安装失败的原因。
- 若安装 IOMesh 后手动删除了 `open-iscsi`，那么重新安装 IOMesh 时不会自动启动 `prepare-csi` Pod 来自动安装 `open-iscsi`。此时，需手动设置 open-iscsi。
- CoreOS 版本的 Linux 操作系统不支持 `prepare-csi`，因此当 Linux 操作系统的版本为 CoreOS 时，需手动设置 `open-iscsi`。

**操作步骤**

1. 在节点控制页面，执行如下命令，安装 `open-iscsi`。

   - **RHEL/CentOS**

     ```
     sudo yum install iscsi-initiator-utils -y
     ```
   - **Ubuntu**

     ```
     sudo apt-get install open-iscsi -y
     ```
   - **CoreOS**

     ```
     sudo rpm-ostree install iscsi-initiator-utils
     ```
2. 编辑 `/etc/iscsi/iscsid.conf` 文件，将 `node.startup` 字段设置为 `manual`。

   ```
   sudo sed -i 's/^node.startup = automatic$/node.startup = manual/' /etc/iscsi/iscsid.conf
   ```

   > **说明：**
   >
   > 在 `/etc/iscsi/iscsi.conf` 文件中，`MaxRecvDataSegmentLength` 的默认值为 32768，而允许 IOMesh 创建的最大 PV 数为 80000；如果 IOMesh 创建的 PV 数量可能超过 80000，建议将 `MaxRecvDataSegmentLength` 的值设置为 163840 及以上。
3. 禁用 SELinux。

   ```
   sudo setenforce 0
   sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
   ```
4. 加载 Kernel 内核模块 `iscsi_tcp`。

   ```
   sudo modprobe iscsi_tcp
   sudo bash -c 'echo iscsi_tcp > /etc/modules-load.d/iscsi_tcp.conf'
   ```
5. 启用 `iscsid` 服务。

   ```
   sudo systemctl enable --now iscsid
   ```

---

## 附录 > 监控指标

# 监控指标

IOMesh 使用 Prometheus 格式的指标来监控 IOMesh 集群、Chunk 或卷级别的存储。

## 集群指标

**集群许可**

| 指标 | 描述 |
| --- | --- |
| `zbs_cluster_license_already_expire` | 许可证是否已过期。 |
| `zbs_cluster_license_expire_day` | 许可证过期的时间。 |
| `zbs_cluster_license_subscription` `_expire_day` | 订阅许可过期的时间。 |
| `zbs_cluster_license_subscription` `_already_expire` | 订阅许可是否已过期。 |

**集群 IO**

| 指标 | 描述 |
| --- | --- |
| `zbs_cluster_read_iops` | 集群读 IOPS。 |
| `zbs_cluster_readwrite_iops` | 集群读写 IOPS。 |
| `zbs_cluster_write_iops` | 集群写 IOPS。 |
| `zbs_cluster_read_speed_bps` | 集群读速度。 |
| `zbs_cluster_write_speed_bps` | 集群写速度。 |
| `zbs_cluster_readwrite_speed_bps` | 集群读写速度。 |
| `zbs_cluster_avg_readwrite_latency_ns` | 集群读写平均延迟。 |
| `zbs_cluster_avg_write_latency_ns` | 集群写平均延迟。 |
| `zbs_cluster_avg_read_latency_ns` | 集群读平均延迟。 |
| `zbs_cluster_avg_write_size_bytes` | 集群平均写请求大小。 |
| `zbs_cluster_avg_read_size_bytes` | 集群平均读请求大小。 |
| `zbs_cluster_avg_readwrite_size_bytes` | 集群平均读写请求大小。 |

**集群缓存**

| 指标 | 描述 |
| --- | --- |
| `zbs_cluster_write_cache_hit_ratio` | 写缓存命中率。 |
| `zbs_cluster_failure_cache_space_bytes` | 故障的缓存空间。 |
| `zbs_cluster_cache_capacity_bytes` | 总缓存空间。 |
| `zbs_cluster_dirty_cache_space_bytes` | 脏数据的缓存空间。 |
| `zbs_cluster_readwrite_cache_hit_ratio` | 读写缓存命中率。 |
| `zbs_cluster_used_cache_space_bytes` | 已用缓存空间。 |
| `zbs_cluster_valid_cache_space_bytes` | 有效缓存空间。 |
| `zbs_cluster_dirty_cache_ratio` | 脏数据的缓存空间占总缓存空间的比例。 |
| `zbs_cluster_read_cache_hit_ratio` | 读缓存命中率。 |

**集群数据空间**

| 指标 | 描述 |
| --- | --- |
| `zbs_cluster_data_capacity_bytes` | 总的数据容量。 |
| `zbs_cluster_data_space_use_rate` | 置备空间和已使用空间两者中的最大值与有效数据空间的比值。 |
| `zbs_cluster_unique_logical_size_bytes` | 独占逻辑的大小。 |
| `zbs_cluster_shared_logical_size_bytes` | 共享逻辑的大小。 |
| `zbs_cluster_logical_size_bytes` | 总逻辑大小。 |
| `zbs_cluster_valid_data_space_bytes` | 有效数据空间。 |
| `zbs_cluster_used_data_space_bytes` | 已用数据空间。 |
| `zbs_cluster_failure_data_space_bytes` | 故障数据空间的大小。 |
| `zbs_cluster_provisioned_data_space_bytes` | 置备的数据空间的大小。 |
| `zbs_cluster_chunks_unsafe_failure_space` | 展示集群中是否存在 chunk 所使用的空间大于集群中未使用的空间。 |
| `zbs_cluster_temporary_replica_space_bytes` | 集群中的临时副本所消耗的数据空间。 |
| `zbs_cluster_temporary_replica_num` | 集群中的临时副本数。 |

**集群数据迁移与恢复**

| 指标 | 描述 |
| --- | --- |
| `zbs_cluster_pending_migrate_bytes` | 待迁移的数据总量。 |
| `zbs_cluster_pending_recover_bytes` | 待恢复的数据总量。 |
| `zbs_cluster_migrate_speed_bps` | 迁移速度。 |
| `zbs_cluster_recover_speed_bps` | 恢复速度。 |
| `zbs_cluster_recover_migrate_speed_bps` | 恢复与迁移速度之和。 |

## Chunk 指标

**Chunk 状态**

| 指标 | 描述 |
| --- | --- |
| `zbs_chunk_use_state` | Chunk 使用状态。 |
| `zbs_chunk_connect_status` | Chunk 服务的连接状态。 |
| `zbs_chunk_maintenance_mode` | Chunk 是否处于维护模式。 |

**Chunk IO**

| 指标 | 描述 |
| --- | --- |
| `zbs_chunk_read_iops` | Chunk 读 IOPS。 |
| `zbs_chunk_read_speed_bps` | Chunk 读带宽。 |
| `zbs_chunk_avg_read_size_bytes` | Chunk 平均读请求大小。 |
| `zbs_chunk_avg_read_latency_ns` | Chunk 读平均延迟。 |
| `zbs_chunk_write_iops` | Chunk 写 IOPS。 |
| `zbs_chunk_write_speed_bps` | Chunk 写带宽。 |
| `zbs_chunk_avg_write_size_bytes` | Chunk 平均写请求大小。 |
| `zbs_chunk_avg_write_latency_ns` | Chunk 写平均延迟。 |
| `zbs_chunk_readwrite_iops` | Chunk 读写 IOPS。 |
| `zbs_chunk_readwrite_speed_bps` | Chunk 读写带宽。 |
| `zbs_chunk_avg_readwrite_size_bytes` | Chunk 平均读写请求大小。 |
| `zbs_chunk_avg_readwrite_latency_ns` | Chunk 读写平均延迟。 |

**Chunk 缓存**

| 指标 | 描述 |
| --- | --- |
| `zbs_chunk_used_cache_space_bytes` | 已用缓存空间。 |
| `zbs_chunk_cache_capacity_bytes` | 缓存空间的总量。 |
| `zbs_chunk_read_cache_hit_ratio` | 读缓存命中率。 |
| `zbs_chunk_write_cache_hit_ratio` | 写缓存命中率。 |
| `zbs_chunk_readwrite_cache_hit_ratio` | 读写缓存命中率。 |
| `zbs_chunk_dirty_cache_ratio` | 脏数据的缓存空间占比总缓存空间。 |
| `zbs_chunk_dirty_cache_space_bytes` | 脏缓存空间。 |
| `zbs_chunk_valid_cache_space_bytes` | 有效缓存空间。 |
| `zbs_chunk_failure_cache_space_bytes` | 故障缓存空间。 |

**Chunk 数据空间**

| 指标 | 描述 |
| --- | --- |
| `zbs_chunk_used_data_space_bytes` | 已用数据空间。 |
| `zbs_chunk_data_capacity_bytes` | 数据空间的总量。 |
| `zbs_chunk_provisioned_data_space_bytes` | 已置备的数据空间。 |
| `zbs_chunk_data_space_use_rate` | 置备空间和已使用空间两者中的最大值与有效数据空间的比值。 |
| `zbs_chunk_valid_data_space_bytes` | 有效数据空间。 |
| `zbs_chunk_failure_data_space_bytes` | 故障数据空间。 |

**Chunk 临时副本**

| 指标 | 描述 |
| --- | --- |
| `zbs_chunk_temporary_replica_space_bytes` | 临时副本所使用的空间。 |
| `zbs_chunk_temporary_replica_num` | 临时副本数。 |

**Chunk 数据迁移与恢复**

| 指标 | 描述 |
| --- | --- |
| `zbs_chunk_pending_migrate_bytes` | 待迁移的数据总量。 |
| `zbs_chunk_pending_recover_bytes` | 待恢复的数据总量。 |
| `zbs_chunk_recover_speed_bps` | 恢复速度。 |
| `zbs_chunk_migrate_speed_bps` | 迁移速度。 |
| `zbs_chunk_recover_migrate_speed_bps` | 恢复与迁移速度之和。 |

## 卷指标

**卷空间**

| 指标 | 描述 |
| --- | --- |
| `zbs_volume_shared_logical_size_bytes` | 卷的共享逻辑大小。 |
| `zbs_volume_unique_logical_size_bytes` | 卷的独占逻辑大小。 |
| `zbs_volume_logical_size_bytes` | 卷的逻辑大小。 |

**卷 IO**

| 指标 | 描述 |
| --- | --- |
| `zbs_volume_readwrite_latency_ns` | 卷读写延迟。 |
| `zbs_volume_readwrite_speed_bps` | 卷读写带宽。 |
| `zbs_volume_readwrite_size_bytes` | 卷读写请求大小。 |
| `zbs_volume_readwrite_iops` | 卷读写 IOPS。 |
| `zbs_volume_readwrite_iop30s` | 卷每 30 秒的读写 IOPS。 |
| `zbs_volume_read_latency_ns` | 卷读延迟。 |
| `zbs_volume_read_speed_bps` | 卷读带宽。 |
| `zbs_volume_read_size_bytes` | 卷读请求大小。 |
| `zbs_volume_read_iops` | 卷读 IOPS。 |
| `zbs_volume_write_latency_ns` | 卷写延迟。 |
| `zbs_volume_write_speed_bps` | 卷写带宽。 |
| `zbs_volume_write_size_bytes` | 卷写请求大小。 |
| `zbs_volume_write_iops` | 卷写 IOPS。 |
| `zbs_volume_avg_iodepth` | 卷平均 I/O 深度。 |

---

## 附录 > FAQ

# FAQ

Q：在安装 IOMesh 过程中，拉取 docker 镜像失败，显示错误日志 “Too Many Requests - Server message: toomanyrequests: You have reached your pull rate limit.”

A：在出现上述问题的 Worker 节点登录或者更新您的 Docker 账户。这个问题一般发生在**在线安装** IOMesh 过程中，离线安装不会遇到此类问题。

---

## 版权信息

# 版权信息

版权所有 © 2024 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
