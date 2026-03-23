---
title: "sks_cn/1.5.1/SMTX Kubernetes 服务管理指南"
source_url: "https://internal-docs.smartx.com/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_preface"
sections: 127
---

# sks_cn/1.5.1/SMTX Kubernetes 服务管理指南
## 关于本文档

# 关于本文档

本文档介绍了如何通过 SKS 创建和管理高可用的 Kubernetes 集群（工作负载集群）、管理 SKS 服务设置、管理管控集群、以及管理容器镜像仓库。

阅读本文档需了解 Kubernetes、CloudTower 和 SMTX OS 超融合软件，了解虚拟化、容器、分布式存储等相关技术，并具备数据中心操作的丰富经验。

---

## 文档更新信息

# 文档更新信息

- **2026-02-02：补充物理机集群启用 GPU 插件的准备工作**

  **创建工作负载集群前的准备 > 准备 GPU 资源**：为物理机集群补充禁用 nouveau 驱动并加载 video 模块的操作。
- **2025-12-12：配合 SMTX Kubernetes 服务 1.5.1 正式发布**

  相较于 1.5.0 版本，本文档主要进行了以下更新：

  - **了解 SKS** > **集群插件**：更新 EIC 插件版本。
  - **管理工作负载集群** > **管理节点组及节点**：

    - **编辑节点组**：新增编辑 Worker 节点组属性的说明。
    - 原**编辑节点**小节删除编辑节点属性的说明，修改标题为**编辑节点调度状态**。

---

## 了解 SKS > 产品特点

# 产品特点

- **简单易用**

  - 仅需简单几步操作，即可在几分钟内快速创建 Kubernetes 工作负载集群。可通过单一管理界面对所有集群的全生命周期进行管理，包括创建、配置、升级、扩缩容、删除等。
  - 通过监控、报警、日志、事件和审计等多种方式，全方位掌握集群运行状态，及时发现异常并优化集群性能。
  - 通过统一的图形界面和控制台实现全面、高效的集群和应用管理。
- **生产就绪**

  - 内置 SmartX 生产级分布式存储 CSI 插件，可为有状态应用提供稳定、高性能的持久卷。
  - 通过网络与安全产品 Everoute 以及容器网络接口（CNI）插件，能够以扁平化的方式实现虚拟机与容器的互联互通，还可对二者进行统一的安全策略管理。
  - 流量可视化功能可以帮助用户了解不同对象之间的访问关系，直观地获取访问细节，实现应用拓扑发现，辅助安全策略的配置；出现异常时，还可以快速定位异常区域，加速排障速度。
  - 通过虚拟机放置组将多个节点放置在不同的宿主机上，保证集群高可用。
  - 当集群虚拟机节点的宿主机宕机时，虚拟机会自动在正常的宿主机上重新拉起。
  - 当集群虚拟机节点出现故障时支持自动替换或者手动快速替换。
  - 支持集群滚动升级、升级失败回滚以保证业务连续性。
  - 当集群资源无法满足应用部署需求时，可以自动感知并触发虚拟机节点横向自动扩容。
  - 支持在双活集群上部署，自动化完成 Kubernetes 的跨站点扩容和容灾。
  - 针对企业组织架构，提供项目级别的资源可视化管理、配额管理与租户权限管理能力。
- **多环境适配**

  - 支持在多种 CPU 品牌的服务器上构建 Kubernetes 集群。
  - 支持物理机和虚拟机Kubernetes 集群并存，支持用户根据业务需求选择合适的集群类型、集群规模并进行统一管理。
  - 支持 GPU 直通、vGPU、MIG、MPS 等多种 GPU 共享方式，使 AI 工作负载能在虚拟机和容器上共享 GPU 资源，进一步提升资源利用率。
- **开放兼容**

  - 支持多个标准的Kubernetes 版本，用户可按需选择以构建集群。
  - 除预集成的常用软件外，还支持用户使用 CNCF 生态中的其他开源软件，无厂商锁定。

---

## 了解 SKS > 集群插件

# 集群插件

SKS 支持为其创建的 Kubernetes 集群安装如下类型的插件，您也可以按需安装其他同类应用。

**CNI（容器网络接口）**

| 插件名称及版本 | 插件说明 | 适用场景 |
| --- | --- | --- |
| [Calico CNI](https://docs.tigera.io/calico/latest/about)（3.28.4） | Calico 是一种开源的容器之间互通的网络方案。使用 BGP 协议在节点之间传输容器网络的路由信息，并使用 IP in IP 或 VXLAN 模式对容器流量进行封装，具有可靠、灵活、兼容其他网络方案等特点。 | 适用于多数场景，是一个稳定、功能丰富、且使用广泛的 CNI。 |
| EIC（1.2.4） | EIC（Everoute Integrated CNI）是 SmartX 基于 Everoute 自主研发的 CNI。  EIC 可以充分利用 SKS 服务与 SMTX OS 联动效应的优势，打通容器网络与 SMTX OS 虚拟化网络，实现容器网络和虚拟化网络的统一管理。同时，还可支持为 Kubernetes Pod 创建网络策略，以控制 Pod 之间的网络访问。 | 适用于如下场景：   - 需要统一管理 Kubernetes 网络和虚拟机网络，并创建统一的安全访问控制策略的场景。 - 对 BGP、Overlay 等网络技术不熟悉，希望容器网络尽量简单的场景。   **注意**：  对于从集群外部通过以 NodePort 或 LoadBalancer 方式对外暴露的 Ingress 控制器来访问部署在集群中的 Nginx 服务，并且访问频率较低的场景不适合使用 EIC。  此外，EIC 不支持 Service 配置 `externalTrafficPolicy` 属性，也不支持 kube-proxy 的 `IPVS` 模式。 |

**CSI（容器存储接口）**

| 插件名称及版本 | 插件说明 | 适用场景 |
| --- | --- | --- |
| SMTX ELF CSI（1.1.0） | SmartX 自主研发的 CSI 驱动。每个 Kubernetes 持久卷对应一个挂载到虚拟机中的虚拟卷，使用 SMTX ELF CSI 创建出的持久卷可以享受到本地化等性能优势。  支持在线扩容、卷快照、从快照制备卷和卷克隆操作，使用简单且无需额外配置。  根据 SMTX OS 集群的 CPU 架构不同，每个节点支持挂载的持久卷数量有所不同，具体请参见表格下方的说明。 | 适用于对性能有要求，但对每节点挂载的持久卷数量无过高要求的场景。 |
| SMTX ZBS CSI（2.8.1） | SmartX 自主研发的 CSI 驱动。通过存储网络将 ZBS 块存储服务的 iSCSI LUN 挂载到节点虚拟机中，并以持久卷的形式提供给 Kubernetes Pod 使用。  支持最多为每个节点挂载 128 个持久卷，且支持在线扩容、卷快照、从快照制备卷、卷克隆和卷身份验证操作。  使用时需为每个节点额外配置专用网卡，并为每个网卡分配 IP。 | 适用于对每节点挂载的持久卷数量有一定要求的场景。 |

**说明**：

SMTX ELF CSI 每节点挂载的持久卷数量如下：

- **x86\_64 架构**：支持最多为每个节点挂载 60 个持久卷。
- **AArch64 架构**：针对不同的 CNI 和 CSI 插件组合，支持挂载的持久卷数量也有所不同。

  - **Calico CNI + SMTX ELF CSI**：支持最多为每个节点挂载 33 个持久卷。
  - **Calico CNI + SMTX ELF CSI + SMTX ZBS CSI**：支持最多为每个节点挂载 32 个持久卷。
  - **EIC + SMTX ELF CSI**：支持最多为每个节点挂载 32 个持久卷。
  - **EIC + SMTX ELF CSI + SMTX ZBS CSI**：支持最多为每个节点挂载 31 个持久卷。

**节点组自动伸缩**

| 插件名称及版本 | 插件说明 |
| --- | --- |
| [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler)（根据 K8s 版本匹配：1.25.3-r1，1.26.8-r1，1.27.8，1.28.7，1.29.5，1.30.4） | Cluster Autoscaler 支持自动调整 Kubernetes 集群的节点数量。  当 Pod 由于资源不足无法在集群中运行时，可按需自动增加节点数量；当节点长时间未被充分利用时，可自动减少节点数量。 |

**GPU**

| 插件名称及版本 | 插件说明 |
| --- | --- |
| [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/overview.html)（23.6.2-sks.1） | NVIDIA GPU Operator 是一个由 NVIDIA 提供的开源工具，用于简化在 Kubernetes 集群上管理和配置 NVIDIA GPU 设备的过程。 |

**监控**

| 插件名称及版本 | 插件说明 |
| --- | --- |
| [kube-prometheus](https://prometheus.io/)（0.13.0-r3） | kube-prometheus 是一个集成了 Kubernetes 常见监控清单、Grafana 仪表板和 Prometheus 规则以及文档和脚本的集合项目。它使用 Prometheus Operator 和 Prometheus 提供易于操作的端到端 Kubernetes 集群监控。 Prometheus 是一款开源的监控和告警工具，用于收集、存储和查询应用程序和系统性能数据，以确保系统的可靠性和稳定性。 |
| obs-monitoring-agent（1.4.0） | 配合 kube-prometheus 使用，将 Prometheus 提供的监控数据采集并发送到 SmartX 可观测性服务。 |

**日志**

| 插件名称及版本 | 插件说明 |
| --- | --- |
| obs-logging-agent（1.0.0-r4） | obs-logging-agent 是 SmartX 可观测性服务的 Client，用于采集 Kubernetes 日志和节点文件日志，经过序列化处理后发送到可观测性服务端。 |

**事件**

| 插件名称及版本 | 插件说明 |
| --- | --- |
| obs-event-agent（1.0.0-r2） | obs-event-agent 是 SmartX 可观测性服务的 Client 与 event exporter 组件的集合，用与采集 Kubernetes event，经过序列化处理后发送到可观测性服务端。 |

**审计**

| 插件名称及版本 | 插件说明 |
| --- | --- |
| obs-aduit-agent（1.0.0-r2） | obs-aduit-agent 是 SmartX 可观测性服务的 Client，它仅采集 Kubernetes 审计日志，经过序列化处理后发送到可观测性服务端。 |

**外部负载均衡器**

| 插件名称及版本 | 插件说明 |
| --- | --- |
| [MetalLB](https://metallb.universe.tf/installation/)（0.14.8） | MetalLB 是一个开源的、基于 Kubernetes 的负载均衡器，用于为 Kubernetes 集群中的服务提供外部访问能力。 |

**Ingress 控制器**

| 插件名称及版本 | 插件说明 |
| --- | --- |
| [Contour](https://projectcontour.io/)（1.27.0-sks.1） | Contour 是一个开源的 Kubernetes Ingress 控制器，使用 Envoy 作为边缘代理，利用 Envoy 的高性能和强大的流量控制功能，提供高度灵活和可扩展的 Ingress 控制。 |

**证书管理**

| 插件名称及版本 | 插件说明 |
| --- | --- |
| [cert-manager](https://cert-manager.io/)（1.16.3） | cert-manager 是一个证书的自动化管理工具，用于在 Kubernetes 集群中自动为 Kubernetes 应用颁发与管理证书。 |

**时区**

| 插件名称及版本 | 插件说明 |
| --- | --- |
| [k8tz](https://github.com/k8tz/k8tz)（0.18.0） | k8tz 是一个 Kubernetes 准入控制器和一个将时区注入 Pod 的 CLI 工具，使用 k8tz 可以轻松地跨 Pod 和名字空间自动标准化所选时区。 |

**NTP 管理**

| 插件名称及版本 | 插件说明 |
| --- | --- |
| ntpm（1.1.0-rc15） | ntpm 是 SmartX 自研的 NTP 管理软件，用于自动化配置和管理操作系统的 NTP 服务。 |

**Agent**

| 插件名称及版本 | 插件说明 |
| --- | --- |
| host-config-agent（0.2.4） | host-config-agent 是 SmartX 自研的主机配置代理插件，用于接收节点配置任务并在节点主机上执行。在 SKS 集群中自动开启。 |
| warden（0.2.0） | warden 是 SmartX 自研的用于 SKS 多租户身份认证的组件。在 SKS 集群中自动开启。 |

**配额**

| 插件名称及版本 | 插件说明 |
| --- | --- |
| cluster-quota-enforcer（0.1.4） | cluster-quota-enforcer 是一个 Kubernetes 准入控制器，用于执行集群维度的资源配额限制，在 SKS 中负责处理项目配额。在 SKS 工作负载集群中自动开启。 |

---

## 了解 SKS > 相关概念

# 相关概念

在部署和运维 SKS 前，您需要先了解与 SKS 相关的一些概念，以帮助您更好地理解 SKS 的部署流程和功能。

**Kubernetes**

[Kubernetes](https://kubernetes.io/zh-cn/docs/concepts/overview/) 是一个可移植、可扩展的开源平台，用于管理容器化的工作负载和服务，可促进声明式配置和自动化。Kubernetes 拥有一个庞大且快速增长的生态，其服务、支持和工具的使用范围相当广泛。

**工作负载**

[工作负载](https://kubernetes.io/zh-cn/docs/concepts/workloads/)是在 Kubernetes 集群上运行的应用程序。Kubernetes 提供若干种内置的工作负载资源，包括 Deployment、StatefulSet、DaemonSet、Job、CronJob 等多种类型。

在 SKS 中，用户的工作负载应部署在工作负载集群。

**节点**

Kubernetes 通过将容器放入在节点上运行的 Pod 中来运行工作负载，节点可以是一个虚拟机或者物理机。

一个 Kubernetes 集群中包含两种不同角色的节点：Control Plane 节点和 Worker 节点。

- **Control Plane 节点**

  Control Plane 节点上运行 Kubernetes 集群的 [Control Plane 组件](https://kubernetes.io/zh-cn/docs/concepts/overview/components/#control-plane-components)（Control Plane Components）。一般一个 Kubernetes 集群中有 1 个、3 个或 5 个 Control Plane 节点。
- **Worker 节点**

  Worker 节点上运行 Kubernetes 集群的[节点组件](https://kubernetes.io/zh-cn/docs/concepts/overview/components/#node-components)和容器化的用户工作负载。

在 SKS 中，管控集群的每个节点和工作负载集群的每个 Control Plane 节点都是一个虚拟机，工作负载集群的 Worker 节点可以是一个虚拟机或者物理机。

**容器镜像**

[容器镜像](https://kubernetes.io/zh-cn/docs/concepts/containers/images/)所承载的是封装了应用程序及其所有软件依赖的二进制数据。容器镜像是轻量级、可执行的软件包，可以单独运行；该软件包对所处的运行环境具有良定（Well Defined）的假定。应用开发人员通常会创建应用的容器镜像并将其推送到某容器镜像仓库（Container Registry），然后在 Pod 中引用它。

**容器镜像仓库**

容器镜像仓库（Container Registry）是一个用于存储和管理容器镜像的中心化存储系统，提供了一个集中的位置供开发人员和运维人员访问、分享、存储容器镜像。

在 SKS 中，容器镜像仓库根据用途不同，可分为如下两类：

- **SKS 系统使用的容器镜像仓库**

  在 CloudTower 的 **Kubernetes 服务**界面中部署 SKS 时创建的唯一的 **SKS 容器镜像仓库**，用于存储和管理系统使用的容器镜像。

  部署 SKS 服务、创建工作负载集群时，将从该仓库拉取相应的系统镜像以构建管控集群和工作负载集群。
- **用户部署的 Kubernetes 工作负载使用的容器镜像仓库**

  该类容器镜像仓库用于存储和管理工作负载使用的容器镜像。SKS 支持为工作负载集群配置多个受信任的容器镜像仓库，使工作负载集群能够从相应容器镜像仓库中拉取工作负载需要使用的容器镜像。

  根据容器镜像仓库来源的不同，可分为如下两类：

  - **内部容器镜像仓库**

    在 CloudTower 的**容器镜像仓库**界面创建的容器镜像仓库，在 SKS 中可以直接配置给工作负载集群使用，以拉取相应的容器镜像。

    此外，该类容器镜像仓库亦可被其他标准的 Kubernetes 集群使用。下文中**容器镜像仓库**、**内部容器镜像仓库**均指该类仓库。
  - **外部容器镜像仓库**

    用户自行部署的其他容器镜像仓库，可通过域名或 IP 地址配置给工作负载集群使用，以拉取相应的容器镜像。

**SKS 系统服务**

SKS 系统服务是 SKS 相关服务的组件的总称，目前包含 SKS 管控集群和 SKS 容器镜像仓库。

**Control Plane 虚拟 IP**

Control Plane 虚拟 IP 是为管控集群或工作负载集群的 Control Plane 节点配置的虚拟 IP，是外部访问集群的入口，负责将外部访问请求自动转发到某一个 Control Plane 节点，以实现 Control Plane 的高可用。

**IP 池**

在管控集群和工作负载集群的生命周期中存在大量动态创建节点的场景。SKS 推荐给节点配置静态 IP 而不是 DHCP IP。为了解决给每一个节点配置静态 IP 太过繁琐的问题，SKS 提供了 IP 池功能。一个 IP 池可以自动管理一系列 IP，主要提供 IP 分配、回收等功能。

- **管控集群 IP 池**：为管控集群节点分配静态 IP，以及 Control Plane 虚拟 IP。
- **工作负载集群 IP 池**：为工作负载集群节点分配静态 IP，以及 Control Plane 虚拟 IP。

**名字空间**

[名字空间](https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/namespaces/)（Namespace）提供一种机制，将同一集群中的资源划分为相互隔离的组，可以在一个集群按需创建组并分开管理。

**CSI**

CSI（容器存储接口）定义了存储系统暴露给容器的标准接口。

**存储类**

[存储类](https://kubernetes.io/zh-cn/docs/concepts/storage/storage-classes/)（StorageClass）为管理员提供了描述存储**类**的方法，包含 provisioner、parameters 和 reclaimPolicy 等字段。这些字段会在 StorageClass 需要动态制备 PersistentVolume 时使用，也可以把存储类理解为 PV 动态制备的模板。这个类的概念在其他存储系统中有时被称为配置文件。

**持久卷**

[持久卷](https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes/)（PersistentVolume，PV）是集群中的一块存储，与节点相似，均为集群层面的资源。持久卷可以由管理员事先制备，或者使用存储类（StorageClass）来[动态制备](https://kubernetes.io/zh-cn/docs/concepts/storage/dynamic-provisioning/)。

**持久卷申领**

持久卷申领（PersistentVolumeClaim，PVC）表达的是用户对存储的请求。概念上与 Pod 类似。Pod 会耗用节点资源，而 PVC 申领会耗用 PV 资源。Pod 可以请求特定数量的资源（CPU 和内存）；同样 PVC 申领也可以请求特定大小和访问模式的 PV。

**卷模式**

卷模式（volumeMode）说明了卷的具体模式，有以下两种模式：

- **文件系统**（filesystem）

  volumeMode 属性设置为 filesystem 的卷会被 Pod 挂载（Mount）到某个目录。
- **块**（block）

  将 volumeMode 属性设置为 block 则可以将卷作为原始块设备来使用。

**访问模式**

访问模式（Access Modes）指的是持久卷所支持的具体访问方式。持久卷可以用资源提供者所支持的任何方式挂载到宿主系统上。资源提供者的能力不同，持久卷支持的访问模式也有所不同。访问模式有以下几种：

- **ReadWriteOnce**

  卷可以被一个节点以读写方式挂载。 ReadWriteOnce 访问模式也允许运行在同一节点上的多个 Pod 访问卷。
- **ReadOnlyMany**

  卷可以被多个节点以只读方式挂载。
- **ReadWriteMany**

  卷可以被多个节点以读写方式挂载。
- **ReadWriteOncePod**

  卷可以被单个 Pod 以读写方式挂载。 如果您需确保整个集群中只有一个 Pod 可以读取或写入该 PVC， 请使用 ReadWriteOncePod 访问模式。该模式仅支持 CSI 卷以及需要 Kubernetes 1.22 以上版本。

在 SKS 中支持 ReadWriteOnce、ReadOnlyMany 和 ReadWriteMany 三种访问模式。

**CNI**

CNI（容器网络接口）定义了给容器配置网络的标准接口。

**外部负载均衡器**

外部负载均衡器（LoadBalancer）为 Kubernetes Service 对象提供外部可访问的 IP 地址，可将流量发送到集群节点的正确端口上。

**Ingress**

[Ingress](https://kubernetes.io/zh-cn/docs/concepts/services-networking/ingress/) 是对集群中服务的外部访问进行管理的 API 对象，典型的访问方式是 HTTP。Ingress 可以提供负载均衡、SSL 终结和基于名称的虚拟托管。

**Kubeconfig 文件**

用于配置集群访问的文件称为 Kubeconfig 文件，其中包含集群、用户、名字空间和身份认证机制等信息。 例如可以通过 kubectl 命令行工具使用 kubeconfig 文件来查找、选择集群所需的信息，并与集群的 API 服务器进行通信。

**内容库**

内容库是 CloudTower 中管理虚拟机模板和 ISO 映像的功能。用户可以通过内容库功能对虚拟机模板和 ISO 映像统一管理。在多 SMTX OS 集群管理的场景中，用户可以在内容库中跨集群共享虚拟机模板和 ISO 映像，以在虚拟化平台为 ELF 的集群中灵活使用这些内容。在 SKS 的场景中，需要利用内容库来管理和分发 Kubernetes 节点模板（即节点相关文件）。

**vGPU 驱动**

NVIDIA 官方发布的 vGPU 软件包含 NVIDIA Virtual GPU Manager 和 NVIDIA Graphics Driver。其中 NVIDIA Virtual GPU Manager 是部署在虚拟化平台为虚拟机提供 vGPU 功能的驱动，SmartX 对 NVIDIA Virtual GPU Manager 进行了改造和适配，并随 SMTX OS 发布，后文将其称为 “vGPU 驱动”。

**滚动更新**

滚动更新是指分批创建新的节点来替换旧的节点，并将旧节点上的工作负载迁移到新节点上，从而保证用户业务可以连续运行。

**原地更新**

原地更新是指在更新集群或节点配置的过程中，依次更新各个节点配置而不重建节点，可以使配置变更快速生效，并避免节点重建带来的额外开销。

---

## 查看 SKS 概览

# 查看 SKS 概览

进入 CloudTower 的 **Kubernetes 服务**界面，在左侧导航栏中单击**概览**，可查看管控集群、工作负载集群、SKS 服务和 SKS 容器镜像仓库的概况。

具体包括如下卡片：

- **报警**：展示 SKS 系统服务和所有工作负载集群的未解决报警的类型和数量，以及最近触发的报警信息。按照报警项的严重和紧急程度，报警分为**严重警告**、**注意**和**信息**三种类型。单击报警信息可跳转至对应报警的详情界面。
- **管控集群**：展示管控集群的状态，以及 Control Plane 节点数和 Worker 节点数。单击卡片可[查看管控集群信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_95)。
- **管控集群插件状态**：展示管控集群中已开启的插件及其状态，鼠标悬浮在插件名称上可查看具体的插件版本。

  | 参数 | 描述 |
  | --- | --- |
  | 插件类型及名称 | 具体包含如下插件：  - **CNI**：calico - **CSI**：smtx-elf-csi - **日志**：obs-logging-agent - **监控**：kube-prometheus、obs-monitoring-agent - **事件**：obs-event-agent - **审计**：obs-audit-agent - **时区**：k8tz - **EIC Adapter**：ecp-adapter - **NTP 管理**：ntpm - **Agent**：host-config-agent |
  | 插件状态 | 插件可能出现的状态如下：  - **正常**：对应的插件已启用，已运行正常。 - **异常**：插件出现问题，无法工作。 - **启动中**：正在启动该插件。 |
- **工作负载集群**：展示已创建的工作负载集群总数及其状态。单击卡片可[查看工作负载集群信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_27)。
- **SKS 服务**：展示当前 SKS 服务的版本号以及管控集群所属 SMTX OS 集群的服务器 CPU 架构。单击卡片可进入**设置** > **服务升级**页面，您可以按需升级 SKS，详细操作可参考《SMTX Kubernetes 服务部署与升级指南》的[升级 SKS](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_31) 章节。
- **SKS 容器镜像仓库**：展示 SKS 容器镜像仓库的运行状态、IP 地址、域名等信息。单击卡片可[查看 SKS 容器镜像仓库信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_101)。

---

## 创建工作负载集群的要求

# 创建工作负载集群的要求

创建工作负载集群前，请确认已完成集群节点数量和插件的规划，并且已满足工作负载集群的资源、网络、防火墙端口配置要求。

若工作负载集群需要使用 GPU 设备，还需要满足[使用 GPU 设备要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_23)。

若工作负载集群需要使用在 CloudTower 的**容器镜像仓库**界面创建的容器镜像仓库，还需要满足[使用容器镜像仓库的要求](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_104)。

---

## 创建工作负载集群的要求 > 规划工作负载集群插件

# 规划工作负载集群插件

工作负载集群支持启用 CNI、CSI、节点组自动伸缩、GPU、外部负载均衡器、Ingress 插件、监控、报警、日志、事件和审计插件。您可参考[集群插件](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_22)了解各插件的详细介绍，并参考以下说明规划集群启用的插件。

## 插件启用要求

- 工作负载集群的类型不同时，对 CNI 和 CSI 插件的启用要求也不同，如下。
  - **虚拟机集群**：支持两种 CNI 和两种 CSI 插件，必须启用一种 CNI 插件和一种 CSI 插件，有以下 4 种组合方式：
    - Calico CNI 和 SMTX ELF CSI
    - EIC 和 SMTX ELF CSI
    - Calico CNI 和 SMTX ZBS CSI
    - EIC 和 SMTX ZBS CSI
  - **物理机集群**：对于 CNI 插件，仅支持 Calico CNI；对于 CSI 插件，您可以使用 SMTX ZBS CSI 插件，若不使用该插件，集群创建完成后，您也可以选择自行配置物理机的本地盘作为存储后端或自行安装第三方 CSI 插件等方式使用 Kubernetes 支持的各种卷。
- SKS 通过可观测性服务提供监控、报警、日志、事件和审计功能，如需启用对应插件，需确保可观测性服务的版本、虚拟机存储容量等符合要求，详细要求可参考[规划管控集群插件](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_14)。
- 若需启用 EIC 插件，需确保使用该插件的工作负载集群所在的 SMTX OS 集群已关联符合版本配套要求的 Everoute 服务。需要注意，使用 EIC 插件时不支持 Service 配置 `externalTrafficPolicy` 属性，也不支持 kube-proxy 的 `IPVS` 模式。
- 若需启用 SMTX ZBS CSI 插件，需确保提供存储服务的 SMTX ZBS 集群或 SMTX OS 集群符合版本配套要求。

> **说明**：
>
> 当工作负载集群部署在未启用双活特性的 SMTX OS 集群时，通过 SMTX ELF CSI、SMTX ZBS CSI 默认存储类创建的持久卷为 2 副本；当工作负载集群部署在启用双活特性的 SMTX OS 集群时，通过 SMTX ELF CSI、SMTX ZBS CSI 默认存储类创建的持久卷为 3 副本。

## 插件组合示例

您可参考以下示例了解不同插件组合的推荐业务场景，以及启用这些插件的集群中与业务流量相关的路径，再根据实际业务需求选择合适的插件组合。

### 示例一：虚拟机集群启用 Calico CNI、SMTX ELF CSI 和 Ingress 控制器插件

此组合适用于以下业务场景：

- 适用于一般业务负载，以及具有常规或更高 IO 性能要求的应用场景，例如 MES、ERP、门户类应用等常规业务系统。
- 适用于对外服务入口通过代理或网关接入，无需为集群分配公网 IP 的场景。应用访问路径示例：客户端（例如 MES 系统）→外部四层硬件负载均衡设备（例如 F5、Radware）或自建的 Nginx、LVS 或 HAProxy 负载均衡器 → SKS Ingress 控制器 → Service → Pod。

  > **说明**：
  >
  > 外部四层硬件负载均衡（如 F5/Radware）适用于有网络安全需求或有运维团队的用户；自建的 Nginx、LVS 或 HAProxy 负载均衡器适用于有自行搭建和管理能力的用户；对于预算受限的用户，可以直接访问 SKS 暴露的 NodePort 或 Ingress Controller 的外部 IP（MetalLB 提供），但可用性和安全性较低。

下图为工作负载集群启用该插件组合时，与业务相关的网络通信路径、存储访问路径和应用访问路径的示例。其中，集群使用的持久化存储为虚拟机集群所在的 SMTX OS 集群。

![](https://cdn.smartx.com/internal-docs/assets/2df79858/sks_deploy_guide_06.png)

### 示例二：虚拟机集群启用 Calico CNI、SMTX ZBS CSI、外部负载均衡器、Ingress 控制器插件

此组合适用于以下业务场景：

- 适用于存储与计算资源分离，或者跨 SMTX OS 集群异地部署，同时对数据卷的挂载数量有较高要求的场景。
- 适用于需要从企业网络访问的服务（例如部署在数据中心的 ERP、MES 系统）。应用访问路径示例：客户端浏览器或系统 → 企业内部网关/NAT → 客户侧公网网关/NAT → MetalLB 暴露的 IP → SKS Ingress 控制器（Contour）→ Service → Pod。

下图为工作负载集群启用该插件组合时，与业务相关的网络通信路径、存储访问路径和应用访问路径的示例。其中，集群使用的持久化存储是虚拟机集群所在 SMTX OS 集群之外的 SMTX OS 集群。

![](https://cdn.smartx.com/internal-docs/assets/2df79858/sks_deploy_guide_07.png)

### 示例三：虚拟机集群启用 EIC、SMTX ZBS CSI、外部负载均衡器和 Ingress 控制器插件

此组合适用于以下业务场景：

- 适用于对网络封控严格，或者安全要求高、不允许全网放通的场景。
- 适用于部署在客户数据中心、需通过公网域名访问的服务（例如 ERP、MES）。应用访问路径示例：客户端浏览器或系统 → 公网域名 → 客户侧公网网关/NAT → MetalLB 暴露的 IP → SKS Ingress 控制器（Contour）→ Service → Pod。

下图为工作负载集群启用该插件组合时，与业务相关的网络通信路径、存储访问路径和应用访问路径的示例。其中，集群使用的持久化存储是虚拟机集群所在 SMTX OS 集群之外的 SMTX OS 集群。

![](https://cdn.smartx.com/internal-docs/assets/2df79858/sks_deploy_guide_08.png)

### 示例四：虚拟机集群启用 EIC、SMTX ELF CSI 插件

此组合适用于以下业务场景：

- 适用于对租户网络隔离敏感，或者希望统一管理接口（例如运营商、自研 SaaS 平台）的场景。
- 适用于对网络封控严格、不同 VLAN 或机房之间访问隔离要求高的场景（例如制造行业异地站点）。
- 适用于对外服务入口通过代理或网关接入，无需为集群分配公网 IP 的场景。
  - **启用 SKS Ingress 控制器**的应用访问路径示例：客户端（如 MES 系统）→ 企业网关或总代理层（如 Nginx）→ SKS Ingress 控制器（Contour）→ Service → Pod。
  - **启用 Everoute 网络负载均衡器**的应用访问路径示例：客户端 → Everoute 网络负载均衡器 → Pod。

下图为工作负载集群启用 EIC、SMTX ELF CSI 和 Ingress 控制器插件时，与业务相关的网络通信路径、存储访问路径和应用访问路径的示例。其中，集群使用的持久化存储为虚拟机集群所在的 SMTX OS 集群。

![](https://cdn.smartx.com/internal-docs/assets/2df79858/sks_deploy_guide_09.png)

### 示例五：物理机集群启用 Calico CNI、SMTX ZBS CSI 插件

此组合适用于以下业务场景：

- 适用于需要极致性能的场景，例如 AI 模型训练、大数据处理、工业视觉分析场景。
- 适用于需要直通 GPU、FPGA 等硬件加速设备，或者对网络 I/O、存储 IOPS 有极端要求的业务，可以避免虚拟化带来的性能开销。
- 适用于金融、政企等行业客户因合规性要求或已有物理资源池，需要直接在物理机上部署 K8s 集群的场景。
- 适用于对外服务入口通过代理或网关接入，无需为集群分配公网 IP 的场景。**启用 Ingress 控制器插件**的应用访问路径示例：客户端（如 MES 系统）→ 企业网关或总代理层（如 Nginx）→ SKS Ingress 控制器（Contour）→ Service → Pod。
- 适用于部署在客户数据中心、需通过公网域名访问的服务（例如 ERP、MES）。**启用外部负载均衡器、Ingress 控制器插件**的应用访问路径示例：客户端浏览器或系统 → 公网域名 → 客户侧公网网关/NAT → MetalLB 暴露 IP → SKS Ingress 控制器（Contour）→ Service → Pod。

下图为工作负载集群启用 Calico CNI、SMTX ZBS CSI、外部负载均衡器、Ingress 控制器插件时，与业务相关的网络通信路径、存储访问路径和应用访问路径的示例。其中，集群使用的持久化存储为物理机集群的虚拟机节点所在的 SMTX OS 集群。

![](https://cdn.smartx.com/internal-docs/assets/2df79858/sks_deploy_guide_10.png)

---

## 创建工作负载集群的要求 > 规划工作负载集群节点数量

# 规划工作负载集群节点数量

## Control Plane 节点

一个工作负载集群中仅存在一个 Control Plane 节点组，且该节点组中的节点个数仅支持设置为 `1`、`3` 或 `5`，您可以根据高可用需求选择合适的节点个数，并确保运行工作负载集群的 SMTX OS 集群中可用的物理主机数量不小于所选的节点个数。

- **1**：Control Plane 没有高可用能力，一旦该 Control Plane 节点异常，则整个集群将不可用。
- **3**：最多允许 1 个 Control Plane 节点发生故障。
- **5**：最多允许 2 个 Control Plane 节点同时发生故障。

## Worker 节点

### 虚拟机集群的 Worker 节点

对于虚拟机类型的工作负载集群，集群中可存在多个 Worker 节点组，每个 Worker 节点组中包含一组资源配置完全相同的 Worker 节点，节点的数量可以设置为以下任一类型：

- **固定节点数**：节点数量固定不变。需要设置一个固定的节点个数，数量至少为 1。
- **自动伸缩**：节点数量根据节点工作负载的多少以及 Pod 是否可被调度等条件在一定范围内自动调整。调整范围需要通过设置最小、最大节点数来指定，最小节点数需至少为 3。

不同 Worker 节点组的节点资源配置和节点数类型可以不同。您可以根据实际业务需求规划合适的 Worker 节点组个数，以及每个 Worker 节点组内的节点数类型和节点个数，并计算出 Worker 节点的总数。计算节点个数时，对于节点数类型为**自动伸缩**的 Worker 节点组，节点个数需要以最大节点数计算。

### 物理机集群的 Worker 节点

对于物理机类型的工作负载集群，同一集群中可存在多个 CPU 架构相同的 Worker 节点组，同一个 Worker 节点组中物理机的型号、规格（除了 CPU 架构）可以不同，但为了方便管理，建议您将配置相近或具有某些共同特征的物理机划分在同一个节点组，例如，您可以将需要配置同一型号的 GPU 设备的物理机划分在同一节点组。

您可以根据实际业务需求规划合适的 Worker 节点组个数，以及每个 Worker 节点组内的节点个数，并计算出 Worker 节点的总数。

---

## 创建工作负载集群的要求 > 工作负载集群资源要求

# 工作负载集群资源要求

工作负载集群占用的资源主要为集群节点占用的资源。

- 集群的虚拟机节点，即虚拟机集群的所有节点和物理机集群的 Conrtol Plane 节点，将固定占用节点所在的 SMTX OS 集群资源。
- 集群的物理机节点，即物理机集群的 Worker 节点，将使用您自行准备的物理机的资源。

---

## 创建工作负载集群的要求 > 工作负载集群资源要求 > 集群虚拟机节点资源要求

# 集群虚拟机节点资源要求

请根据为工作负载集群规划的虚拟机节点数量，计算集群虚拟机节点在 SMTX OS 集群中需占用的资源。

不同角色的节点所在的虚拟机的资源要求如下表所示。

| 节点角色 | 单个节点所在的虚拟机的资源要求 | 所需的资源总量 |
| --- | --- | --- |
| Control Plane | - 至少 2 vCPU - 至少 6 GiB 内存 - 200 GiB 存储空间，即节点对应虚拟机的磁盘默认分配容量，该值不支持修改 | - 1 节点   - 至少 2 vCPU   - 至少 6 GiB 内存   - 200 GiB 存储空间 - 3 节点   - 至少 6 vCPU   - 至少 18 GiB 内存   - 600 GiB 存储空间 - 5 节点   - 至少 10 vCPU   - 至少 30 GiB 内存   - 1000 GiB 存储空间 |
| Worker | - 至少 4 vCPU - 至少 8 GiB 及以上内存 - 至少 200 GiB 存储空间，即节点对应虚拟机的磁盘默认分配容量 | 假定一共有 N 个 Worker 组，每个 Worker 节点组中有 M 个节点（在规划虚拟机集群 Worker 节点数量时确定的 Worker 节点组和节点数量）  - 至少 4 × M × N vCPU - 至少 8 × M × N GiB 内存 - 至少 200 × M × N GiB 存储空间 |

> **注意**：
>
> - CPU 非独占。
> - 若节点所在 SMTX OS 集群的服务器 CPU 架构为 AArch64，则单节点需至少分配 10 GiB 内存，以免工作负载集群插件开启过多时内存不足。
> - 存储策略为精简置备，通常所在集群未启用双活特性时为 2 副本、启用双活特性时为 3 副本。**特殊情况**：若工作负载集群使用的 Kubernetes 节点模板初始上传至启用双活特性的集群，即使实际部署在未启用双活特性的集群中，也为 3 副本。
> - 对于虚拟机集群，不同 Worker 节点组之间的节点资源配置可以相同，也可以不同。因此，Worker 节点所需的资源总量需结合 Worker 节点组数量、每个 Worker 节点组中的节点的数量，以及节点对应的资源配置具体计算。
> - 为确保工作负载集群高可用，Control Plane 节点将被强制放置在不同的物理主机。因此，您需要确保工作负载集群的虚拟机节点所在的 SMTX OS 集群中有足够的可用物理主机、以及充足的计算和存储资源，可以使一个工作负载集群中的每个 Control Plane 节点虚拟机分别运行在不同的物理主机，对于虚拟机集群，还需要可以使每个 Worker 节点虚拟机运行在相同或不同的物理主机。

---

## 创建工作负载集群的要求 > 工作负载集群资源要求 > 集群物理机节点资源要求

# 集群物理机节点资源要求

如果工作负载集群为物理机集群，则作为 Worker 节点的物理机需满足以下资源要求。

| 资源 | 要求 |
| --- | --- |
| 处理器 | 至少 8 核 |
| 内存 | 至少 16 GB |
| 存储设备 | 至少一块 100 GB 及以上的 SSD 或 HDD。 **说明**：物理机添加至 SKS 界面后，仍允许热添加物理盘。 |

> **说明**：
>
> 物理机的 CPU 架构与 Control Plane 节点所在 SMTX OS 集群的主机必须均为 x86\_64 架构或者 AArch64 架构。

---

## 创建工作负载集群的要求 > 工作负载集群网络要求 > 集群网络要求概述

# 集群网络要求概述

对工作负载集群的网络要求与集群类型、集群使用的 CNI 和 CSI 插件组合有关。

## 虚拟机集群网络要求

### 网卡要求

| 工作负载集群插件 | 网卡要求 |
| --- | --- |
| Calico CNI 和 SMTX ELF CSI | - 每个节点需配置 1 个虚拟网卡作为业务网卡，用于与 CloudTower 虚拟机、SKS 容器镜像仓库虚拟机、管控集群节点进行通信。 - 所有业务数据均通过该网卡传输。 |
| EIC 和 SMTX ELF CSI | - 每个节点需配置 1 个虚拟网卡作为业务网卡，除 Pod 之间的数据传输、以及 Pod 与外界通信使用 EIC 专用网卡外，其余业务数据均通过该网卡传输。 - 每个节点需为 EIC 配置一个专用网卡，用于 Pod 之间的数据传输以及 Pod 与外界通信。 |
| Calico CNI 和 SMTX ZBS CSI | - 每个节点需配置 1 个虚拟网卡作为业务网卡，用于节点之间相互通信。除节点上的 Pod 使用 SMTX ZBS CSI 专用网卡访问持久卷外，其余业务数据均通过该网卡传输。 - 每个节点需为 SMTX ZBS CSI 配置一个专用网卡，节点上的 Pod 通过此网卡可访问 SMTX ZBS CSI 使用目标存储创建的持久卷。 |
| EIC 和 SMTX ZBS CSI | - 每个节点需配置 1 个虚拟网卡作为业务网卡，用于与 CloudTower 虚拟机、SKS 容器镜像仓库虚拟机、管控集群节点进行通信。 - 每个节点需为 EIC 配置一个专用网卡，用于 Pod 之间的数据传输，以及 Pod 与外界通信。 - 每个节点需为 SMTX ZBS CSI 配置一个专用网卡，节点上的 Pod 通过此网卡可访问 SMTX ZBS CSI 使用目标存储创建的持久卷。 |

### IP 要求

| 工作负载集群插件 | IP 数量要求（N 表示集群内的节点总数；M 表示集群内的系统 Pod 总数） |
| --- | --- |
| Calico CNI 和 SMTX ELF CSI | 1 个 Control Plane 虚拟 IP + N 个节点 IP |
| EIC 和 SMTX ELF CSI | 1 个 Control Plane 虚拟 IP + N 个节点 IP + M 个 Pod IP |
| Calico CNI 和 SMTX ZBS CSI | 1 个 Control Plane 虚拟 IP + N 个节点 IP + N 个 SMTX ZBS CSI 专用网卡 IP |
| EIC 和 SMTX ZBS CSI | 1 个 Control Plane 虚拟 IP + N 个节点 IP + M 个 Pod IP + N 个 SMTX ZBS CSI 专用网卡 IP |

> **说明**：
>
> - 启用 EIC 插件时，集群内的系统 Pod 总数（M）可参考 EIC 专用网卡网络的 [IP 配置要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_20#ip-%E9%85%8D%E7%BD%AE%E8%A6%81%E6%B1%82)进行计算。
> - 若 IP 通过 IP 池自动分配，为保证后续集群能正常升级或滚动更新，建议额外预留至少 2 个空闲的节点 IP，预留的节点 IP 越多，升级或滚动更新速度越快。
> - 若需启用外部负载均衡器插件，还需规划该插件使用的 IP 范围。IP 范围需与 Kubernetes 集群的节点业务网卡所在的网络在同一网段，且未被使用，MetalLB 将从该范围为负载均衡服务分配 IP 地址。
> - 您还需要提前规划 Service IP CIDR、Pod IP CIDR（后者仅使用 Calico CNI 时需要），这些网段必须是未被使用或分配的，并且不能使用公网地址。不同的工作负载集群之间 Service IP CIDR 以及 Pod IP CIDR 可以使用相同网段。

具体网络配置要求参见[业务网卡网络要求](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_19)、[EIC 专用网卡网络要求](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_20)和 [SMTX ZBS CSI 专用网卡网络要求](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_21)。

## 物理机集群网络要求

### 网卡要求

对于物理机集群，集群网卡需要满足以下基本要求：

- 每个 Control Plane 节点需配置 1 个虚拟网卡作为业务网卡，用于与 CloudTower 虚拟机、SKS 容器镜像仓库虚拟机、管控集群节点进行通信。
- 每个 Worker 节点需配置 1 个速率至少为 1 Gbps 的物理网卡作为业务网卡，用于与 CloudTower 虚拟机、SKS 容器镜像仓库虚拟机、管控集群节点进行通信。

  建议再为每个 Worker 节点配置有效的 DNS 服务器。若一个 Worker 节点配置了多个网卡，通常仅需要为业务网卡配置默认网关。

若需启用 SMTX ZBS CSI 插件，则还需满足以下要求：

- 每个 Control Plane 节点需为 SMTX ZBS CSI 配置一个专用网卡，节点上的 Pod 通过此网卡可访问 SMTX ZBS CSI 使用目标存储创建的持久卷。
- 每个 Worker 节点需配置 1 个速率至少为 10 Gbps 的物理网卡作为 SMTX ZBS CSI 专用网卡，节点上的 Pod 通过此网卡可访问 SMTX ZBS CSI 使用目标存储创建的持久卷。可复用业务网卡，但为避免业务负载过高时影响业务的连续性，建议使用独立的网卡。

### IP 要求

| 工作负载集群插件 | IP 数量要求（N 表示集群内的节点总数） |
| --- | --- |
| Calico CNI | 1 个 Control Plane 虚拟 IP + N 个节点 IP |
| Calico CNI 和 SMTX ZBS CSI | 1 个 Control Plane 虚拟 IP + N 个节点 IP + N 个 SMTX ZBS CSI 专用网卡 IP |

> **说明**：
>
> - 若 IP 通过 IP 池自动分配，为保证后续集群能正常升级或滚动更新，建议额外预留至少 2 个空闲的节点 IP，预留的节点 IP 越多，升级或滚动更新速度越快。
> - 若需启用外部负载均衡器插件，还需规划该插件使用的 IP 范围。IP 范围需与 Kuernetes 集群的节点业务网卡所在的网络在同一网段，且未被使用，MetalLB 将从该范围为负载均衡服务分配 IP 地址。
> - 您还需要提前规划 Service IP CIDR 和 Pod IP CIDR，这些网段必须是未被使用或分配的，并且不能使用公网地址。不同的工作负载集群之间 Service IP CIDR 以及 Pod IP CIDR 可以使用相同网段。若 Calico CNI 需要使用 IPIPCrossSubnet 或 VXLANCrossSubnet 的封装模式，当物理机集群的 K8s 节点间存在防火墙时，请确保 Pod IP CIDR 内的不同 Pod IP 之间允许相互通信。

具体网络配置要求参见[业务网卡网络要求](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_19)和 [SMTX ZBS CSI 专用网卡网络要求](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_21)。

---

## 创建工作负载集群的要求 > 工作负载集群网络要求 > 业务网卡网络要求

# 业务网卡网络要求

工作负载集群中的每个节点需配置一个业务网卡，用于与 CloudTower 虚拟机、SKS 容器镜像仓库虚拟机、管控集群节点进行通信。

## 网络连接要求

- 工作负载集群虚拟机节点的业务网卡所在虚拟机网络（VLAN 类型必须为 Access）需与物理机节点所在网络三层互通。
- 工作负载集群节点的业务网卡所在网络需与 SKS 容器镜像仓库虚拟机、管控集群节点虚拟机和 CloudTower 虚拟机的虚拟网卡所在的虚拟机网络三层互通。
- 若工作负载集群需启用监控、报警、日志、事件或审计插件，则集群节点的业务网卡所在网络、可观测性服务虚拟机的虚拟网卡所在虚拟机网络两者之间需三层互通，以便后续为工作负载集群关联可观测性服务。

![](https://cdn.smartx.com/internal-docs/assets/2df79858/sks_deploy_guide_03.png)

## IP 配置要求

### IP 数量要求

您需要为工作负载集群中每个节点的业务网卡配置一个 IP。另外，为了保证 Control Plane 的高可用，还需要为工作负载集群配置一个 Control Plane 虚拟 IP。

不同节点角色下需要的最少 IP 数量如下表所示。

| 节点角色 | 节点数量 | 所需 IP 数量 | IP 用途 |
| --- | --- | --- | --- |
| Control Plane 节点 | 1 | 2 | - 1 个 Control Plane 虚拟 IP - 1 个节点 IP |
| 3 | 4 | - 1 个 Control Plane 虚拟 IP - 3 个节点 IP |
| 5 | 6 | - 1 个 Control Plane 虚拟 IP - 5 个节点 IP |
| Worker 节点 | N（在规划工作负载集群节点数量时确定的 Worker 节点总数） | N | N 个节点 IP |

> **说明**：
>
> 对于虚拟机集群，如果集群节点 IP 通过 IP 池自动分配，为保证后续集群能正常升级或滚动更新，除上述 IP 外，还需额外预留至少 2 个空闲的节点 IP，预留的节点 IP 越多，升级或滚动更新速度越快。节点 IP 的分配方式可参考下文。

### IP 分配方式及相应规划说明

- 虚拟机节点 IP 支持如下两种 IP 分配方式：

  - **通过 IP 池自动分配**

    IP 池可设置多个 IP 范围，请根据 IP 数量要求提前规划工作负载集群 IP 池的 IP 范围，并获取子网掩码、网关和 DNS 服务器信息。

    使用 IP 池管理时，您需要在部署完 SKS 服务后，先根据规划创建工作负载集群 IP 池，然后在创建工作负载集群时选择该 IP 池。系统将自动从 IP 池中为每个节点配置静态 IP。

    创建工作负载集群 IP 池后，您仍可以按需编辑工作负载集群 IP 池。
  - **通过 DHCP 服务器动态分配**

    使用 DHCP 服务器动态分配节点 IP 时，您需要提前在 DHCP 服务器中配置 IP 范围、网关和 DNS 服务器等必要参数。

    在创建工作负载集群时选择**启用网卡 DHCP**，即可向 DHCP 服务器申请并获取相应的节点 IP。

    > **注意**：
    >
    > 若节点 IP 需使用域名访问 SKS 容器镜像仓库、内部或外部容器镜像仓库，或者业务负载需通过域名访问任何外部系统（如外部数据库、API 服务、互联网等），则必须获取能解析对应域名的 DNS 服务器信息，否则可以使用公共的 DNS 服务器地址（例如 `1.1.1.1`）代替，但请勿使用 `127.0.0.1`。
- Control Plane 虚拟 IP 支持如下两种 IP 分配方式：

  - **通过 IP 池自动分配**

    系统将自动从工作负载集群 IP 池中为工作负载集群配置 Control Plane 虚拟 IP。
  - **通过手动输入方式设置**

    Control Plane 的虚拟 IP 除通过 IP 池自动分配外，也可以支持单独手动指定。您可以根据业务需求提前规划虚拟 IP，并在创建工作负载集群时输入该 IP。

> **注意**：
>
> 规划的 IP 地址均不能与以下 CIDR 范围内的任何 IP 地址重叠：
>
> - 169.254.0.0/16
> - 240.0.0.0/4
> - 224.0.0.0/4
> - 198.18.0.0/15
> - 127.0.0.0/8
> - 0.0.0.0/8
> - 工作负载集群的 Pod IP CIDR（通常与管控集群相同，默认为 172.16.0.0/16）
> - 工作负载集群的 Service IP CIDR（通常与管控集群相同，默认为 10.96.0.0/22）

---

## 创建工作负载集群的要求 > 工作负载集群网络要求 > EIC 专用网卡网络要求（仅适用于虚拟机集群）

# EIC 专用网卡网络要求（仅适用于虚拟机集群）

若规划工作负载集群使用 EIC 插件，则需要在工作负载集群的每个节点上为 EIC 单独配置一个专用网卡，用于 Pod 之间的数据传输、以及 Pod 与外界通信。

## 虚拟机网络要求

Kubernetes 集群在运行工作负载时将创建大量的 Pod，而每个 Pod 会占用至少一个 IP 并且在 Pod 重建时 IP 会发生变化。因此推荐您为 EIC 专用网卡创建专属的虚拟机网络，而不是与节点虚拟机的业务网卡共用一个虚拟机网络。使用专属的虚拟机网络可以避免子网中的 IP 很快被耗尽，减少 Pod IP 与外部服务发生冲突的可能性，还可以很方便地对这个子网单独设定网络策略，减少管理的混乱程度。

EIC 专用网卡所在的虚拟机网络（VLAN 类型必须为 Access）需在已关联 Everoute 服务的虚拟分布式交换机上创建，并且需要和业务网卡所在的虚拟机网络三层互通。

![](https://cdn.smartx.com/internal-docs/assets/2df79858/sks_deploy_guide_04.png)

## IP 配置要求

确认虚拟机网络后，请获取虚拟机网络对应的子网 CIDR 块（即虚拟机网络所在的子网）和网关信息，并根据业务需求在子网 CIDR 范围内规划出用于 Pod 使用的一个或多个 Pod IP 池。

> **注意**：
>
> Pod 内使用 IP 地址 `100.64.254.254/32` 用于路由，您需要保证此 IP 地址预留给 EIC 使用。

EIC 会从 Pod IP 池中为每个非 hostNetwork 的 Pod 分配一个从 Kubernetes 集群外部网络可连通的 IP。当 Pod IP 池包含子网的第一个 IP 或者最后一个 IP，则该 IP 并不会分配给 Pod 使用。

Pod IP 池支持以下两种配置方式：

- **地址范围**：指定起始 IP 和结束 IP。
- **CIDR 块**：指定一个 CIDR 块，并且可选择排除一个或多个 IP 地址或 IP 地址范围。

规划 Pod IP 数量时，请注意：

- 集群规模越大，所需的 IP 数量越多，需根据业务需求设置合适的地址范围和 CIDR 块掩码值，以免由于 IP 耗尽而导致无法创建 Pod。使用 CIDR 块配置 Pod IP 池时，假设工作负载集群的 Control Plane 节点数、Worker 节点数均为 3：

  - 若未开启除 CNI、CSI 以外的其他插件，Pod IP CIDR 的掩码值应小于等于 26。
  - 若开启除 CNI、CSI 以外的其他插件，Pod IP CIDR 的掩码值应小于等于 25。
- SKS 和 K8s 的系统组件也会消耗部分 Pod IP，具体数量可参考下表。规划时，请为“所属功能插件”类型为 `system` 的组件预留足够 IP；其他组件可根据对应功能插件的启用情况决定是否预留 IP。若插件全部启用，则需预留的 Pod IP 总数为：`17 + Control Plane 节点数 + 3 × N`。

  | 组件 | 所属功能插件 | 类型 | 消耗的 Pod IP 总数（N 表示集群节点总数） |
  | --- | --- | --- | --- |
  | coredns | system | Deployment | 2 |
  | snapshot-controller | system | Deployment | 2 |
  | contour-contour | Contour | Deployment | 1 |
  | contour-default-backend | Contour | Deployment | 1 |
  | contour-envoy | Contour | DaemonSet | N |
  | observability-audit-agent | 审计 | Deployment | Control Plane 节点数 |
  | observability-event-agent | 事件 | Deployment | 1 |
  | observability-logging-agent | 日志 | DaemonSet | N |
  | metallb-controller | MetalLB | Deployment | 1 |
  | grafana | 监控 | Deployment | 1 |
  | kube-state-metrics | 监控 | Deployment | 1 |
  | observability-monitoring-agent | 监控 | Deployment | 1 |
  | prometheus-adapter | 监控 | Deployment | 2 |
  | prometheus-operator | 监控 | Deployment | 1 |
  | sks-exporter | 监控 | Deployment | 1 |
  | cluster-quota-enforcer | system | Deployment | 2 |
  | ntpm | system | DaemonSet | N |

---

## 创建工作负载集群的要求 > 工作负载集群网络要求 > SMTX ZBS CSI 专用网卡网络要求

# SMTX ZBS CSI 专用网卡网络要求

若规划工作负载集群使用 SMTX ZBS CSI 插件，则需要在工作负载集群的每个节点上为 SMTX ZBS CSI 配置一个专用网卡，使节点上的 Pod 可通过此网卡访问 SMTX ZBS CSI 使用目标存储集群存储资源创建的持久卷。请根据以下要求规划网络环境与 IP。

## 网络连接要求

- 对于虚拟机节点，SMTX ZBS CSI 专用网卡所在的虚拟机网络（VLAN 类型必须为 Access）需通过节点所在 SMTX OS 集群的存储网络所在的虚拟分布式交换机创建，请您提前规划虚拟机网络的 VLAN ID 和名称。若目标存储集群不是节点所在的 SMTX OS 集群（简称“外部存储集群”），则节点所在 SMTX OS 集群的存储网络还需要与外部存储集群的接入网络二层互通。
- 对于物理机节点，SMTX ZBS CSI 专用网卡所在的网络需要与虚拟机节点所在 SMTX OS 集群的存储网络二层互通。若目标存储集群为外部存储集群，则 SMTX ZBS CSI 专用网卡所在的网络还需要与外部存储集群的接入网络二层互通。

![](https://cdn.smartx.com/internal-docs/assets/2df79858/sks_deploy_guide_05.png)

## IP 配置要求

您需要为工作负载集群每个节点的 SMTX ZBS CSI 专用网卡规划 IP。其中，对于虚拟机节点，ZBS CSI 专用网卡的 IP 仅支持通过 SKS 的 IP 池自动分配。请根据虚拟机节点数提前规划 SMTX ZBS CSI 专用网卡的 IP 池的 IP 范围，并获取子网掩码、网关和 DNS 服务器信息。

> **说明**：
>
> 使用 IP 池管理时，您需要在部署完 SKS 服务后，先根据规划创建 SMTX ZBS CSI 专用网卡的工作负载集群 IP 池，然后在创建工作负载集群时为 SMTX ZBS CSI 专用网卡选择该 IP 池，系统将自动从 IP 池中为每个虚拟机节点配置静态 IP。
>
> 创建完成后，您仍可以按需参考编辑该 IP 池。

您还需要获取目标存储集群的接入虚拟 IP，具体获取方式如下：

- 如果目标存储集群为 SMTX ZBS 集群或者已启用**为其他计算端提供块存储**功能的 SMTX OS 集群，您可以在 CloudTower 左侧导航树中选中目标集群，在右侧的概览界面中选择**全部 > 设置 > 虚拟 IP**，查看接入虚拟 IP。
- 如果目标存储集群为工作负载集群的虚拟机节点所在的 SMTX OS 集群并且未启用**为其他计算端提供块存储**功能，则表明还未设置集群的接入虚拟 IP，您仅需要为其规划接入虚拟 IP，在创建工作负载集群时填写该 IP 后系统可以自动为 SMTX OS 集群设置接入虚拟 IP。该 IP 须位于 SMTX OS 存储网络的子网中，以保证在完成配置后 SMTX OS 将该 IP 自动分配到存储网络中。

  > **说明**：
  >
  > 获取 SMTX OS 存储网络的子网步骤如下：
  >
  > 1. 在 CloudTower 左侧导航树中选中**集群**，在右侧的概览界面中选择**全部 > 系统网络**。
  > 2. 在系统网络列表中查看 **storage-network** 的**存储 IP** 和**子网掩码**，计算即可得出存储网络的子网。
- 如果目标存储集群为其他未启用**为其他计算端提供块存储**功能的 SMTX OS 集群，则表明还未设置集群的接入虚拟 IP，您需要参考对应 SMTX OS 版本的《SMTX OS 管理指南》的**为其他计算端提供块存储（ELF 平台）** 章节开启**为其他计算端提供块存储**功能，创建接入网络和设置接入虚拟 IP。

> **注意**：
>
> 规划的 IP 地址均不能与以下 CIDR 范围内的任何 IP 地址重叠：
>
> - 169.254.0.0/16
> - 240.0.0.0/4
> - 224.0.0.0/4
> - 198.18.0.0/15
> - 127.0.0.0/8
> - 0.0.0.0/8
> - 工作负载集群的 Pod IP CIDR（通常与管控集群相同，默认为 172.16.0.0/16）
> - 工作负载集群的 Service IP CIDR（通常与管控集群相同，默认为 10.96.0.0/22）

---

## 创建工作负载集群的要求 > 工作负载集群防火墙端口配置要求

# 工作负载集群防火墙端口配置要求

若工作负载集群节点对应的虚拟机或运行 SKS 工作负载集群的 SMTX OS 集群物理主机与 CloudTower 虚拟机、SKS 容器镜像仓库虚拟机等通信端点之间通信的网络存在防火墙，则防火墙需开放一些协议和端口，请参考以下要求提前规划需要开放的端口（若无特殊说明，下面列举的端口均为 TCP 端口）。

## 虚拟机集群防火墙端口配置要求

| 源端 | 目标端 | 开放的协议和端口 | 用途 |
| --- | --- | --- | --- |
| 工作负载集群节点对应的虚拟机 | CloudTower 虚拟机 | 443 | SMTX ELF CSI 连接 CloudTower API 服务 |
| 工作负载集群节点对应的虚拟机 | SKS 容器镜像仓库虚拟机 | 443 | 从 SKS 容器镜像仓库拉取镜像 |
| 访问工作负载集群的任意 IP | 工作负载集群 Control Plane 节点对应的虚拟机和 Control Plane 虚拟 IP | 6443 | 访问 kube-apiserver |
| 工作负载集群 Control Plane 节点对应的虚拟机 | 工作负载集群 Control Plane 节点对应的虚拟机 | 2379、2380 | Kubernetes etcd |
| 工作负载集群 Control Plane 节点对应的虚拟机 | 工作负载集群 Control Plane 节点对应的虚拟机 | 6440 | 工作负载集群用户访问认证 |
| 工作负载集群节点对应的虚拟机 | 工作负载集群节点对应的虚拟机 | - IP-in-IP 协议（使用默认的 IP-in-IP 模式） - TCP：179（使用 BGP 模式） - TCP：5473 - UDP：51820、51821 - UDP：4789（使用 VXLAN） | Calico CNI 插件，更详细的要求可参见 [Calico 官方文档](https://docs.tigera.io/calico/3.25/getting-started/kubernetes/requirements#network-requirements) |
| 9443 | EIC 插件 |
| 9912、9913 | ELF CSI 快照功能 |
| 9812 | SMTX ZBS CSI 插件 |
| - TCP：7946 - UDP：7946 | metallb speaker |
| 9100 | prometheus 抓取 node-exporter metrics |
| 10249 | prometheus 抓取 kube-proxy metrics |
| 工作负载集群节点对应的虚拟机 | Everoute Controller 虚拟机 | 6443 | SMTX Everoute API |
| 工作负载集群节点对应的虚拟机 | 工作负载集群 Control Plane 节点对应的虚拟机 | 10257 | Prometheus 抓取 kube-controller-manager metrics |
| 10259 | Prometheus 抓取 kube-schedule metrics |
| 工作负载集群 Control Plane 节点对应的虚拟机 | 工作负载集群节点对应的虚拟机 | 10250 | k8s apiserver 访问节点 kubelet api |
| 10100 | k8s apiserver 访问 kapp controller apiregistration |
| 4439 | k8s apiserver 访问 k8tz webhook |
| CloudTower 虚拟机 | 运行 SKS 工作负载集群的 SMTX OS 集群物理主机 | 10600 | SMTX ZBS CSI 插件 |
| 工作负载集群节点对应的虚拟机 | CloudTower 中配置的 NTP 服务器 IP | UDP：123 | 启用同步 CloudTower NTP 配置功能后与 NTP 服务器通讯 |
| 工作负载集群节点对应的虚拟机 | 可观测性服务虚拟机 IP | 80 | 关联可观测性服务时用于推送监控数据 |
| EIC 专用网卡网络的 Pod IP | 可观测性服务虚拟机 IP | 80 | 启用 EIC 插件并关联可观测性服务时用于推送监控数据 |
| 可观测性服务虚拟机 IP | 工作负载集群 Control Plane 虚拟 IP | 6443 | 网络流量可视化功能 |

## 物理机集群防火墙端口配置要求

| 源端 | 目标端 | 开放的协议和端口 | 用途 |
| --- | --- | --- | --- |
| 工作负载集群所有节点 | 工作负载集群所有节点 | ICMP | 确保节点间可互相通信 |
| 5473 | Calico typha |
| 179 | BGP 协议 |
| IPIP：4 | IPIP 协议，协议号 4 |
| UDP：4789 | VXLAN 协议 |
| - TCP：7946 - UDP：7946 | metallb speaker |
| 9100 | prometheus 抓取 node-exporter metrics |
| 10249 | prometheus 抓取 kube-proxy metrics |
| 9812 | SMTX ZBS CSI 插件 |
| 9912、9913 | ELF CSI 快照功能 |
| 工作负载集群所有节点 | SKS 容器镜像仓库虚拟机 | 443 | 从 SKS 容器镜像仓库拉取镜像 |
| 工作负载集群所有节点 | 工作负载集群 Control Plane 节点对应的虚拟机和 Control Plane 虚拟 IP | 6443 | 访问 kube-apiserver |
| 工作负载集群 Control Plane 节点对应的虚拟机 | 工作负载集群所有节点 | 10250 | k8s apiserver 访问节点kubelet api |
| 10100 | k8s apiserver 访问 kapp controller apiregistration |
| 4439 | k8s apiserver 访问 k8tz webhook |
| 工作负载集群 Control Plane 节点对应的虚拟机 | 工作负载集群 Control Plane 节点对应的虚拟机 | 2379、2380 | Kubernetes etcd |
| 工作负载集群 Control Plane 节点对应的虚拟机 | 工作负载集群 Control Plane 节点对应的虚拟机 | 6440 | 工作负载集群用户访问认证 |
| 工作负载集群所有节点 | 工作负载集群 Control Plane 节点对应的虚拟机 | 10257 | Prometheus 抓取 kube-controller-manager metrics |
| 10259 | Prometheus 抓取 kube-schedule metrics |
| 工作负载集群所有节点 | DNS 服务器 | - TCP：53 - UDP：53 | 如果有使用外部域名（如容器镜像仓库使用域名），需要允许访问 DNS 服务器 |
| 工作负载集群所有节点 | SMTX ZBS 块存储集群的接入虚拟 IP | 10206 | 启用 SMTX ZBS CSI 插件，并选择 SMTX ZBS 块存储集群作为目标存储集群时，需要允许访问集群的接入虚拟 IP |
| 工作负载集群所有节点 | CloudTower 中配置的 NTP 服务器 IP | UDP：123 | 启用同步 CloudTower NTP 配置功能后与 NTP 服务器通讯 |
| 工作负载集群所有节点 | 可观测性服务虚拟机 IP | 80 | 关联可观测性服务时用于推送监控数据 |
| 可观测性服务虚拟机 IP | 工作负载集群 Control Plane 虚拟 IP | 6443 | 网络流量可视化功能 |

---

## 创建工作负载集群的要求 > 工作负载集群使用 GPU 设备要求

# 工作负载集群使用 GPU 设备要求

如果工作负载集群需要使用 GPU 设备，则需要满足以下要求。

## 虚拟机集群使用 GPU 设备要求

在创建虚拟机集群或者编辑集群的 Worker 节点组时，您可以为虚拟机集群的 Worker 节点组配置 GPU 设备，系统将自动为节点组内的每个节点挂载所配置的 GPU 设备，同一个节点组只能挂载一种用途（直通或 vGPU）的 GPU 设备，但需要确保满足以下要求。

> **注意**：
>
> 若工作负载集群所在的 SMTX OS 集群启用了双活特性，则不支持使用 GPU 设备。

### 基本要求

- 虚拟机集群所在的 SMTX OS 集群为 5.1.x、6.0.x、6.1.x 或 6.2.x 版本。
- 虚拟机集群所在的 SMTX OS 集群存在满足以下要求的主机。
  - 服务器 CPU 架构为 Intel x86\_64 架构。

    > **风险提示**：
    >
    > 目前仅对 Intel x86\_64 架构的主机做了验证，选用 Hygon x86\_64 架构需谨慎。
  - 已挂载 GPU 设备，并且 GPU 型号必须是 SMTX OS 集群支持的型号，可参见对应 SMTX OS 版本的《SMTX OS 特性说明》。

    > **说明**：
    >
    > 下表为 NVIDIA 官方推荐的一些适用于云原生场景的 GPU 型号，您可结合下表与 SMTX OS 集群支持使用的 GPU 型号选择需要在 SKS 工作负载集群中使用的 GPU 型号。
    >
    > | 型号 | NVIDIA 推荐 GPU 用途 | 适用场景 |
    > | --- | --- | --- |
    > | Tesla V100-PCIE-16GB | 直通、vGPU | AI 训练、机器学习、高性能计算 |
    > | Tesla V100-PCIE-32GB | 直通、vGPU | AI 训练、机器学习、高性能计算 |
    > | [Tesla T4](https://www.nvidia.cn/data-center/tesla-t4/) | 直通、vGPU | 机器学习、分布式 AI 训练和推理、视频转码 |
    > | [A100](https://www.nvidia.com/en-us/data-center/a100/) | 直通、vGPU | AI 计算、高性能计算 |
    > | [A30](https://www.nvidia.com/en-us/data-center/products/a30-gpu/) | 直通、vGPU | AI 推理、高性能计算 |
    > | [A10](https://www.nvidia.com/en-us/data-center/products/a10-gpu/) | 直通、vGPU | AI 推理、图片或视频渲染 |

### 使用 GPU 直通要求

规划每个 Worker 节点组挂载的 GPU 设备时，可以为同一个 Worker 节点组分配多个不同型号的直通用途的 GPU，但建议仅分配一种型号，并且需确保虚拟机集群所在 SMTX OS 集群的主机上有足够的计算资源、存储资源、以及可挂载的 GPU 设备，可以用于创建和启动所有 Worker 节点虚拟机。

例如，假设虚拟机集群中有 2 个 Worker 节点分别被配置挂载 2 个 Tesla T4 型号的直通 GPU，则这两个节点可以运行在同一个主机上并使用其上的 4 个 Tesla T4 型号的直通 GPU，或者可以分别运行在两个主机上并使用其上的 2 个 Tesla T4 型号的直通 GPU，如图所示。

![](https://cdn.smartx.com/internal-docs/assets/62cb2be1/sks_user_guide_03.png)

![](https://cdn.smartx.com/internal-docs/assets/62cb2be1/sks_user_guide_02.png)

### 使用 vGPU 要求

规划每个 Worker 节点组挂载的 GPU 设备时，可以为同一个 Worker 节点组分配多个 vGPU，但需确保：

- 一个 Worker 节点组只能挂载同一种型号和切分规格的 vGPU。
- 虚拟机集群所在 SMTX OS 集群的主机上有足够的计算资源、存储资源、以及可挂载的 GPU 设备，可以用于创建和启动所有 Worker 节点虚拟机。

  例如，假设虚拟机集群中有 2 个 Worker 节点分别被配置挂载 2 个 Tesla T4 型号（规格：GRID T4-4C）的 vGPU，则这两个节点可以运行在同一个主机上并使用其上的 4 个此类型的 vGPU，或者可以分别运行在两个主机上并使用其上的 2 个此类型的 vGPU，如图所示。

  ![](https://cdn.smartx.com/internal-docs/assets/62cb2be1/sks_user_guide_05.png)

  ![](https://cdn.smartx.com/internal-docs/assets/62cb2be1/sks_user_guide_04.png)

## 物理机集群使用 GPU 设备要求

在创建物理机集群或者编辑集群的 Worker 节点组时，您可以为 Worker 节点组选择已挂载 GPU 设备的物理机，但需要确保满足以下要求。

- 物理机集群的 Control Plane 节点所在的 SMTX OS 集群为 5.1.x、6.0.x、6.1.x 或 6.2.x 版本。
- 物理机集群中物理机的服务器 CPU 架构为 Intel x86\_64 架构。

  > **风险提示**：
  >
  > 目前仅对 Intel x86\_64 架构的主机做了验证，选用 Hygon x86\_64 架构需谨慎。
- 物理机挂载的 GPU 设备的型号必须是 SMTX OS 集群支持的型号，可参见对应 SMTX OS 版本的《SMTX OS 特性说明》。

  > **说明**：
  >
  > 下表为 NVIDIA 官方推荐的一些适用于云原生场景的 GPU 型号，您可结合下表与 SMTX OS 集群支持使用的 GPU 型号选择需要在 SKS 工作负载集群中使用的 GPU 型号。
  >
  > | 型号 | NVIDIA 推荐 GPU 用途 | 适用场景 |
  > | --- | --- | --- |
  > | Tesla V100-PCIE-16GB | 直通、vGPU | AI 训练、机器学习、高性能计算 |
  > | Tesla V100-PCIE-32GB | 直通、vGPU | AI 训练、机器学习、高性能计算 |
  > | [Tesla T4](https://www.nvidia.cn/data-center/tesla-t4/) | 直通、vGPU | 机器学习、分布式 AI 训练和推理、视频转码 |
  > | [A100](https://www.nvidia.com/en-us/data-center/a100/) | 直通、vGPU | AI 计算、高性能计算 |
  > | [A30](https://www.nvidia.com/en-us/data-center/products/a30-gpu/) | 直通、vGPU | AI 推理、高性能计算 |
  > | [A10](https://www.nvidia.com/en-us/data-center/products/a10-gpu/) | 直通、vGPU | AI 推理、图片或视频渲染 |

---

## 创建工作负载集群的要求 > 工作负载集群使用容器镜像仓库要求

# 工作负载集群使用容器镜像仓库要求

如果工作负载集群需要使用在 CloudTower 的**容器镜像仓库**界面创建的容器镜像仓库，请确认满足对容器镜像仓库的资源、网络和防火墙端口配置要求。

---

## 创建工作负载集群的要求 > 工作负载集群使用容器镜像仓库要求 > 容器镜像仓库资源要求

# 容器镜像仓库资源要求

运行容器镜像仓库的虚拟机所需的计算和存储资源如下：

- vCPU：至少 4 vCPU，默认为 4 vCPU。x86\_64 架构下，不允许超过 240 vCPU；AArch64 架构下，不允许超过 123 vCPU。
- 内存：至少 8 GiB，默认为 8 GiB，不允许超过界面提示的最大可用内存。
- 系统盘：固定为 20 GiB。
- 数据盘：至少 160 GiB，默认为 400 GiB，不允许超过 64 TiB。

> **说明**：
>
> 存储策略为精简置备，所在集群未启用双活特性时为 2 副本、启用双活特性时为 3 副本。

---

## 创建工作负载集群的要求 > 工作负载集群使用容器镜像仓库要求 > 容器镜像仓库网络要求

# 容器镜像仓库网络要求

如果您的工作负载集群需要使用在 CloudTower 的**容器镜像仓库**界面创建的容器镜像仓库，在创建容器镜像仓库前需提前规划容器镜像仓库网络。

容器镜像仓库虚拟机需配置 1 个虚拟网卡，用于与 CloudTower 虚拟机以及工作负载集群节点通信。

容器镜像仓库虚拟机的虚拟网卡所在的虚拟机网络，需与工作负载集群节点的业务网卡所在网络、CloudTower 虚拟机的虚拟网卡所在的虚拟机网络三层互通。

![](https://cdn.smartx.com/internal-docs/assets/2df79858/sks_deploy_guide_11.png)

请提前规划容器镜像仓库虚拟机的虚拟网卡所在的虚拟机网络、为该网卡分配 IP 地址、并获取网关和子网掩码信息。

如需使用域名访问容器镜像仓库虚拟机，则需要提前规划域名，并按如下步骤完成配置：

1. 在 DNS 服务器配置域名和 IP 的双向解析记录。
2. 记录 DNS 服务器地址，确保访问容器镜像仓库时域名可以被正确解析。

---

## 创建工作负载集群的要求 > 工作负载集群使用容器镜像仓库要求 > 容器镜像仓库防火墙端口配置要求

# 容器镜像仓库防火墙端口配置要求

如果您的工作负载集群需要使用在 CloudTower 的**容器镜像仓库**界面创建的容器镜像仓库，当工作负载集群节点对应的虚拟机、CloudTower 虚拟机和容器镜像仓库虚拟机之间通信的网络存在防火墙时，防火墙需开放如下协议和端口（若无特殊说明，下面列举的端口均为 TCP 端口）。

| 源端 | 目标端 | 开放的协议和端口 | 用途 |
| --- | --- | --- | --- |
| CloudTower 虚拟机 | 容器镜像仓库虚拟机 | 22、443 | 管理容器镜像仓库 |
| ICMP（所有类型及代码） | 容器镜像仓库虚拟机连通性检查 |
| 工作负载集群节点对应的虚拟机、访问容器镜像仓库的其他 IP | 容器镜像仓库虚拟机 | 443 | 拉取容器镜像或者访问管理 UI |
| 容器镜像仓库虚拟机 | CloudTower 中配置的 NTP 服务器 IP | UDP：123 | 启用同步 CloudTower NTP 配置功能后与 NTP 服务器通讯 |

---

## 创建工作负载集群前的准备 > 准备 Kubernetes 节点模板

# 准备 Kubernetes 节点模板

SKS 通过 Kubernetes 节点模板（包含在节点相关文件中）部署管控集群和工作负载集群节点。

管控集群节点默认使用 Kubernetes 版本为 1.26.15 的节点模板。新创建的工作负载集群支持使用以下 Kubernetes 版本的节点模板。

- Kubernetes v1.25.16
- Kubernetes v1.26.15
- Kubernetes v1.27.16
- Kubernetes v1.28.15
- Kubernetes v1.29.15
- Kubernetes v1.30.13

部署完 SKS 容器镜像仓库和 SKS 服务后，系统默认提供 Kubernetes 版本为 1.26.15 的节点模板。当您需要使用其他 Kubernetes 版本的节点模板创建工作负载集群时，请按照如下步骤操作。

**操作步骤**

1. 下载所需的 Kubernetes 版本对应的节点相关文件。

   > **注意**：
   >
   > - 节点相关文件的 CPU 架构需与工作负载集群所属的 SMTX OS 集群的 CPU 架构保持一致。
   > - 不支持上传低于当前 SKS 版本中提供的节点相关文件。版本格式为`主版本号.次版本号.补丁版本号`，版本检查仅针对主版本号和次版本号，补丁版本号不受限制。
2. 上传节点相关文件。

   1. 进入 CloudTower 的 **Kubernetes 服务**界面，单击**设置** > **节点相关文件**，进入**节点相关文件**列表，单击**上传节点相关文件**。
   2. 在弹出的窗口中选择要上传的 `.tar`、`.tar.xz` 或 `.tar.gz` 格式的文件，并输入文件的 MD5 值。
   3. 单击**上传**。
   > **说明**：
   >
   > 根据上传的节点相关文件的 CPU 架构与管控集群所属的 SMTX OS 集群的 CPU 架构的异同，节点相关文件将被上传至不同位置：
   >
   > - **CPU 架构相同**：节点相关文件将被上传至管控集群所属的 SMTX OS 集群。
   > - **CPU 架构不同**：节点相关文件将被上传至一个与其 CPU 架构相同且满足要求的 SMTX OS 集群。目标集群需满足的要求如下：连接正常、虚拟化平台为 ELF。系统将优先选择启用了双活特性的 SMTX OS 集群；若无双活集群，则选择未启用双活特性的集群；若存在多个满足要求的集群，则从中选择最先被 CloudTower 关联的集群作为目标集群。
3. 进入 CloudTower 的**内容库**界面，在**虚拟机模板**页面找到已上传的节点相关文件对应的 Kubernetes 节点模板，并通过**编辑所属集群**的方式，将其分发至将要创建工作负载集群的 SMTX OS 集群。当节点相关文件已被上传至工作负载集群所属的 SMTX OS 集群时，可忽略本步骤。

---

## 创建工作负载集群前的准备 > 添加物理机

# 添加物理机

如果需要创建物理机类型的工作负载集群，在已准备符合规格要求的物理机后，请参考以下步骤添加物理机。

## 第 1 步：为物理机安装操作系统

请根据 CPU 架构为每个物理机选择兼容的操作系统进行安装。

> **注意**：
>
> 若已规划使用 GPU 设备，则需选择 Rocky Linux 8.10 进行安装，否则无法成功通过 SKS 界面直接启用 GPU 插件，您需要自行管理 GPU 资源。

| CPU 架构 | 兼容的操作系统 | 注意事项 |
| --- | --- | --- |
| Intel x86\_64 | Rocky Linux 8.10 | 本版本 SKS 也可以兼容 Rocky Linux 8.9，但建议使用 Rocky Linux 8.10。 |
| Ubuntu 22.04.3 | - |
| Hygon x86\_64 | openEuler 22.03 SP2 或 SP3 | - |
| Kylin V10 SP2 或 SP3 2403 | - |
| Ubuntu 22.04.3 | - |
| AArch64 | openEuler 22.03 SP2 或 SP3 | - |
| Kylin V10 SP2 或 SP3 2403 | 操作系统中的 audit 版本 3.0-5.se.06.ky10 存在内存泄漏问题，若物理机需要安装此操作系统，请先升级 audit 版本或关闭 audit 服务（SP3 2403 版本已默认关闭）。 |

## 第 2 步：为物理机配置网络信息

1. 根据[工作负载集群网络要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_18)为物理机配置网卡 IP、网关和 DNS 服务器。

   > **说明**：
   >
   > 建议使用静态 IP，如果使用 DHCP 配置 IP，请确保在 DHCP Server 中为物理机做 IP 保留，防止网络断开或重启系统后 IP 发生变更。
2. 按照以下要求创建用于 SKS 访问物理机的 SSH 账号。

   - 支持使用密码或密钥登录。
   - 非 root 账号可以免密码使用 sudo 权限。

## 第 3 步：在 SKS 界面添加物理机

**注意事项**

物理机添加到 SKS 后，当物理机操作系统中存在旧版本的 Docker 软件包时，可能会与 SKS 中提供的 Docker 软件包发生冲突，SKS 将会自动卸载这些软件包。

**操作步骤**

1. 在 CloudTower 的 **Kubernetes 服务**界面单击**设置** > **物理机管理** > **添加物理机**。
2. 在弹出的**添加物理机**窗口中，填写物理机的名称，主机地址和端口号。
3. 填写用于 SKS 访问物理机的 SSH 账号及其密码或密钥。
4. 单击**保存**。

添加完成后，在物理机管理列表中可以查看添加的物理机状态，物理机将先进入`初始化中`状态，当其状态变为`可用`时，则可以将物理机添加至物理机集群中。

---

## 创建工作负载集群前的准备 > 准备 GPU 资源

# 准备 GPU 资源

如果工作负载集群需要使用 GPU 设备，确认满足[使用 GPU 设备要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_23)后，请完成以下准备工作。

- 在 SKS 服务的**设置** > **节点相关文件**界面上传本版本 SKS 提供的 GPU 容器镜像文件。当在 SKS 容器镜像仓库的 Harbor UI 中可查看到对应该版本的 GPU 容器镜像时，表明文件已上传成功。
- 对于虚拟机集群，若需要使用直通用途的 GPU 设备，请确认虚拟机集群所在的 SMTX OS 集群上已挂载 GPU 设备的主机已有可使用的 GPU 直通设备。若没有，请执行以下操作。

  1. 为主机启用 IOMMU 并重启主机，可参考对应 SMTX OS 版本的《SMTX OS 管理指南》的[启用 IOMMU（ELF 平台）](/smtxos/6.1.1/os_administration_guide/os_administration_guide_136)小节。
  2. 为 GPU 设备选择“直通”用途，可参考对应 SMTX OS 版本的《SMTX OS 管理指南》的[切换 GPU 设备用途](/smtxos/6.1.1/os_administration_guide/os_administration_guide_154)小节。
- 对于虚拟机集群，若需要使用 vGPU，请确认虚拟机集群所在的 SMTX OS 集群上已挂载 GPU 设备的主机已有可使用的 vGPU 资源。若没有，请执行以下操作。

  1. 为主机安装 vGPU 驱动，可参考对应 SMTX OS 版本的《SMTX OS 特性说明》的[安装 vGPU 驱动](/smtxos/6.1.1/os_property_notes/os_property_notes_48)小节。
  2. 为主机启用 IOMMU 并重启主机，可参考对应 SMTX OS 版本的《SMTX OS 管理指南》的[启用 IOMMU（ELF 平台）](/smtxos/6.1.1/os_administration_guide/os_administration_guide_136)小节。
  3. 为 GPU 设备选择 “vGPU” 用途，并选择切分规格，可参考对应 SMTX OS 版本的《SMTX OS 管理指南》的[切换 GPU 设备用途](/smtxos/6.1.1/os_administration_guide/os_administration_guide_154)小节。
  > **注意**：
  >
  > 当虚拟机集群配置了 vGPU 时，SKS 将在 Worker 节点虚拟机上默认安装 535.216.01-grid 版本的 NVIDIA Graphics Driver，其匹配的驱动分支版本为 16.8，因此，建议在主机上安装的 vGPU 驱动也为对应版本。如果已在主机上安装其他版本的 vGPU 驱动，可参考[《SMTX OS 特性说明》](/smtxos/6.1.1/os_property_notes/os_property_notes_49)升级 vGPU 驱动。
- 对于物理机集群，请为已挂载 GPU 设备的物理机节点禁用 nouveau 驱动并加载 video 模块。以物理机节点使用 Rocky Linux 8.10 操作系统为例，您可登录已挂载 GPU 设备的物理机操作系统，然后参考以下步骤进行操作。

  1. 执行以下命令创建 nouveau 黑名单。

     ```
     sudo cat << EOF > /etc/modprobe.d/blacklist-nouveau.conf
     blacklist nouveau
     options nouveau modeset=0
     EOF
     ```
  2. 执行以下命令加载 video 模块。

     ```
     echo "video" > /etc/modules-load.d/video.conf
     ```
  3. 执行以下命令备份并重建 initramfs。

     ```
     sudo cp /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.bak
     sudo dracut --force
     ```
  4. 执行以下命令重启操作系统。

     ```
     sudo reboot
     ```

---

## 创建工作负载集群前的准备 > 创建 SMTX ZBS CSI 接入配置

# 创建 SMTX ZBS CSI 接入配置

若工作负载集群需要使用 SMTX ZBS CSI 插件，并且目标存储集群为工作负载集群的虚拟机节点所在的 SMTX OS 集群，则在创建工作负载集群前，还需创建 SMTX ZBS CSI 接入配置。

**注意事项**

为 SMTX OS 集群添加 SMTX ZBS CSI 接入配置信息后，这些配置信息除虚拟机网络名称外，其余内容均不可编辑。

**操作步骤**

1. 在 **Kubernetes 服务**界面单击**设置** > **SMTX ZBS CSI 接入配置**，进入配置界面。
2. 单击右上角的 **+ 添加接入配置**，在弹出的**添加接入配置**对话框中配置如下信息。具体的配置要求可参见 [SMTX ZBS CSI 专用网卡网络要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_21)。

   - **SMTX OS 集群的接入虚拟 IP**

     | 参数 | 描述 |
     | --- | --- |
     | 集群 | 需要添加 SMTX ZBS CSI 接入配置的 SMTX OS 集群。  SMTX OS 集群需符合版本配套要求。 |
     | 接入虚拟 IP | 输入为 SMTX OS 集群规划的接入虚拟 IP，须位于 SMTX OS 存储网络的子网中。 |
   - **SMTX ZBS CSI 专属网卡使用的虚拟机网络**

     | 参数 | 描述 |
     | --- | --- |
     | 虚拟分布式交换机 | 与 SMTX OS 存储网络关联的虚拟分布式交换机的名称，不允许修改。 |
     | VLAN ID | 输入提前规划的虚拟机网络 VLAN ID。 |
     | 虚拟机网络名称 | 创建的虚拟机网络的名称。 |
3. 单击**保存**，完成 SMTX ZBS CSI 接入信息的配置。

**后续操作**

参考[创建工作负载集群 IP 池](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_12)创建 SMTX ZBS CSI 专用网卡的 IP 池。

---

## 创建工作负载集群前的准备 > 创建工作负载集群 IP 池

# 创建工作负载集群 IP 池

当面临以下场景时，您需要在创建工作负载集群前创建工作负载集群 IP 池。

- 若工作负载集群的虚拟机节点 IP 需采用通过 IP 池自动分配的分配方式，则需为虚拟机节点创建业务网卡的 IP 池。
- 若工作负载集群需要使用 SMTX ZBS CSI 插件， 则需为虚拟机节点创建 SMTX ZBS CSI 专用网卡的 IP 池。

**操作步骤**

1. 在 **Kubernetes 服务**界面单击**设置** > **IP 池管理**，系统展示所有管控/工作负载集群的 IP 池列表。
2. 单击右上角的 **+ 创建工作负载集群 IP 池**，在弹出的对话框中，根据在确认[工作负载集群业务网卡网络要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_19#ip-%E9%85%8D%E7%BD%AE%E8%A6%81%E6%B1%82)时规划的 IP 范围进行设置。

   - 设置 IP 范围时，同时还需设置子网掩码长度（8 ~ 32）。
   - 业务网卡使用的 IP 池必须配置网关和 DNS 服务器地址信息；SMTX ZBS CSI 专用网卡使用的 IP 池无需配置网关和 DNS 服务器地址信息。
   - 支持为 IP 池添加多个 IP 范围。

---

## 创建工作负载集群前的准备 > 创建容器镜像仓库 > 创建前的准备

# 创建前的准备

**前提条件**

已获取本版本的容器镜像仓库安装包。

**操作步骤**

1. 进入 CloudTower 的**容器镜像仓库**界面，在左侧导航栏中单击**设置**，进入**安装包管理**页面。

   > **说明**：
   >
   > 当您尚未创建任何容器镜像仓库时，可在**概览**页面的配置向导中单击**安装包管理**链接，进入**安装包管理**页面。
2. 单击**上传安装包**，上传容器镜像仓库的安装包文件。
3. 单击**上传**，开始上传安装包。您可以在 CloudTower 页面右上方查看上传进度。

   上传成功后，可在安装包管理页面查看该安装包的**名称**、**版本**和**适用 CPU 架构**信息。也可以按需上传多个安装包。

**相关操作**

当容器镜像仓库的安装包未被任何容器镜像仓库使用时，您可以单击 **...** 后选择**删除**。

---

## 创建工作负载集群前的准备 > 创建容器镜像仓库 > 创建步骤

# 创建步骤

**前提条件**

- 已[上传容器镜像仓库安装包](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_76)。
- 请确保容器镜像仓库所在的 SMTX OS 集群符合版本配套要求，已完成[容器镜像仓库资源规划](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_73)和[容器镜像仓库网络规划](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_74)，并按照[容器镜像仓库防火墙端口配置要求](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_75)开放了防火墙的相关协议和端口。

**操作步骤**

1. 进入 CloudTower 的**容器镜像仓库**界面，在左侧导航栏中单击**容器镜像仓库**，单击 **+ 创建容器镜像仓库**。

   > **说明**：
   >
   > 当您尚未创建任何容器镜像仓库时，可在**概览**页面的配置向导中单击**创建容器镜像仓库**。
2. 配置容器镜像仓库的基本信息。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | 容器镜像仓库的名称，创建后支持修改。  - 仅支持大小写字母、数字、下划线（\_）、连字符（-）和英文句号（.）。 - 字符长度为 1 - 200。 - 不允许与已有容器镜像仓库重名。 |
   | 版本 | 已上传的容器镜像仓库安装包的版本。 |
   | 集群 | 容器镜像仓库虚拟机所在的 SMTX OS 集群。仅支持选择与容器镜像仓库安装包 CPU 架构一致的 SMTX OS（ELF）集群。  **说明**：  - 若选择的 SMTX OS 集群为启用双活特性的集群，则容器镜像仓库的虚拟机在资源充足时将默认部署在该双活集群的优先可用域，且高可用（HA）重建优先级为高。 - 优先可用域故障时，可在次级可用域中自动新建，优先可用域恢复后对应虚拟机不会自动切回。 - 当前仅基于双活集群的两个可用域进行部署，不涉及仲裁节点。 |
   | 主机 | 容器镜像仓库虚拟机所在的主机。  默认选择**自动调度至合适的主机**，即根据放置组策略、主机资源使用等情况为容器镜像仓库虚拟机自动分配主机。您也可以手动指定该虚拟机所在的主机。 |
3. 单击**下一步**，为容器镜像仓库配置计算资源、磁盘和网络。

   | 参数 | 描述 |
   | --- | --- |
   | 计算资源 | 根据[容器镜像仓库资源要求](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_73)为容器镜像仓库虚拟机分配计算资源。  - **vCPU 分配**：为容器镜像仓库虚拟机分配的 vCPU。 - **内存分配**：为容器镜像仓库虚拟机分配的内存。 |
   | 磁盘 | - **系统盘容量**：容器镜像仓库虚拟机占用的系统盘容量，固定为 `20 GiB`。 - **数据盘容量**：根据[容器镜像仓库资源要求](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_73)为容器镜像仓库虚拟机分配的数据盘容量。 |
   | 网络 | 根据[容器镜像仓库网络要求](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_74)为容器镜像仓库虚拟机配置网络信息。  - **虚拟机网络**：基于 SMTX OS 集群中关联了管理网络的虚拟分布式交换机所创建的虚拟机网络。仅允许选择 VLAN 类型为 Access 的虚拟机网络。 - **IP 地址**：管理网卡的 IP 地址。 - **子网掩码**：管理网络的子网掩码信息。 - **网关**：管理网络的网关信息。 |
4. 单击**下一步**，为容器镜像仓库配置访问参数。

   **Harbor 访问配置**

   | 参数 | 描述 |
   | --- | --- |
   | 用户名 | 访问容器镜像仓库的用户名，固定为 `admin`。 |
   | 密码 | 访问容器镜像仓库的密码。至少 8 字符，且需要包含大写英文字母、小写英文字母和数字。  **注意**：请妥善记录容器镜像仓库的 admin 账户密码。配置完毕后，admin 账户密码将不会显示于界面上。 |
   | 确认密码 | 再次输入密码，以对密码进行确认。 |

   **高级配置（可选）**

   | 参数 | 描述 |
   | --- | --- |
   | 域名 | 根据[容器镜像仓库网络要求](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_74)按需配置容器镜像仓库虚拟机的域名。该项留空时，您需要通过虚拟机 IP 地址访问容器镜像仓库。 |
   | CA 证书 | 容器镜像仓库仅支持通过 HTTPS 协议访问，可以为其配置一个 CA 签发的证书和证书密钥。如果不配置，则系统会自动生成一个自签名 CA 证书。  **说明**：如果配置 CA 签发的证书和证书密钥，则工作负载集群可直接从该容器镜像仓库拉取容器镜像，无需将该容器镜像仓库配置为工作负载集群的[受信任容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_65)；否则需要先将该容器镜像仓库配置为工作负载集群的[受信任容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_65)，才能从中拉取容器镜像。 |
5. 单击**创建**，开始创建容器镜像仓库。您可以在 CloudTower 的任务中心查看部署的状态。

   创建成功后，您可以查看容器镜像仓库信息、将其配置给工作负载集群使用或按需扩容容器镜像仓库。

**相关操作**

当容器镜像仓库不再使用时，您可以单击 **...** 后选择**删除**。

---

## 创建工作负载集群

# 创建工作负载集群

工作负载集群是一个 Kubernetes 集群，您可以根据实际情况创建所需规格的工作负载集群来运行工作负载，但请勿在工作负载集群节点对应的虚拟机中存储非临时数据。

工作负载集群创建时，将自动为节点设置如下资源预留值，以防止由于集群插件或业务负载的资源使用率过高而导致节点离线等集群异常情况。如需修改资源预留值，请联系 SmartX 售后工程师进行处理。

| 参数 | 描述 | 预留值 |
| --- | --- | --- |
| enforce-node-allocatable | 节点可分配约束 | Pods |
| system-reserved cpu | CPU 系统预留 | 100 m |
| system-reserved memory | Memory 系统预留 | 与为节点分配的内存有关，详见以下说明 |
| kubeReserved cpu | CPU 系统守护进程预留 | 200 m |
| kubeReserved memory | Memory 系统守护进程预留 | 250 Mi |
| eviction-hard | 资源硬驱逐阈值 | 300 Mi |

> **说明**：
>
> system-reserved memory 参数的预留值与为节点分配的内存有关，在创建集群过程中，假设为节点分配的内存值为 N（单位：GiB）：
>
> - 当 N 不超过 8 时，预留值需根据 N 的数值计算，计算公式为： 750Mi + 200Mi × (N - 4)。由于节点最低内存为 6 GiB，因此预留值范围为 1150Mi ~ 1550Mi。
> - 当 N 大于 8 时，预留值固定为 1550 Mi。

---

## 创建工作负载集群 > 创建虚拟机集群 > 配置基本信息

# 配置基本信息

**注意事项**

若需要开启 EIC 或 SMTX ZBS CSI 插件，则必须在创建虚拟机集群时开启。

**操作步骤**

1. 进入 CloudTower 的 **Kubernetes 服务**界面，在左侧导航栏中单击**工作负载集群**。
2. 单击 **+ 创建 > 创建虚拟机集群**，参考以下说明配置基本信息。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | 虚拟机集群在 API 层面的名称，一旦设定，不可修改。 |
   | 显示名称 | 虚拟机集群的显示名称，具有一定的业务语义，虚拟机集群创建完成后仍可在集群的管理界面右上角单击 **...** > **编辑集群显示名称**进行编辑。 |
   | 创建位置 | 选择用于创建虚拟机集群的 SMTX OS 集群。  虚拟机集群所在的 SMTX OS 集群需符合版本配套要求。  **说明**：  若选择的 SMTX OS 集群为启用双活特性的集群，则工作负载集群 Control Plane 节点和 Worker 节点虚拟机将默认部署在该双活集群的优先可用域，且高可用（HA）重建优先级为高。优先可用域资源不足时可在次级可用域中部署，不涉及仲裁节点。 |
   | Kubernetes 版本 | 选择所需的 Kubernetes 版本。  仅支持选择与所选 SMTX OS 集群的 CPU 架构一致且本 SKS 版本支持的节点模板。  如您选择的版本未分发至所选的 SMTX OS 集群，请先按照页面提示[准备 Kubernetes 节点模板](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_08)，否则可能导致创建超时失败。 |
   | CNI | 选择虚拟机集群需要启用的 CNI 插件，有以下两个选项：  - Calico - EIC 插件详细介绍，请参见[集群插件](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_22)。  **注意**：  使用 EIC 插件时不支持 Service 配置 `externalTrafficPolicy` 属性，也不支持 kube-proxy 的 `IPVS` 模式。 |
   | CSI | 选择虚拟机集群需要启用的 CSI 插件，有以下两个选项：  - SMTX ELF CSI - SMTX ZBS CSI 插件详细介绍，请参见[集群插件](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_22)。  **说明**：  当工作负载集群部署在未启用双活特性的 SMTX OS 集群时，通过 SMTX ELF CSI、SMTX ZBS CSI 默认存储类创建的持久卷为 2 副本；当工作负载集群部署在启用双活特性的 SMTX OS 集群时，通过 SMTX ELF CSI、SMTX ZBS CSI 默认存储类创建的持久卷为 3 副本。 |
   | 受信任容器镜像仓库（可选） | 为虚拟机集群配置一个或多个受信任的容器镜像仓库，使虚拟机集群能够从容器镜像仓库中拉取工作负载需要使用的容器镜像。  如果您已在 SKS 的**全局配置**中添加了受信任的容器镜像仓库，则默认显示已添加的受信任容器镜像仓库的信息，否则为空。具体操作请参见[配置受信任容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_93)。  您也可以单击 **+ 添加容器镜像仓库**，为该虚拟机集群配置受信任的容器镜像仓库。具体操作及注意事项请参见[管理受信任容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_65)。 |
   | 时区 | 虚拟机集群的时区，将会应用至虚拟机集群的所有组件。默认选择为 SKS 服务配置的时区。 |
3. 单击**下一步**。

---

## 创建工作负载集群 > 创建虚拟机集群 > 配置节点

# 配置节点

虚拟机集群包含一个 Control Plane 节点组和至少一个 Worker 节点组，同一个节点组中的节点配置相同。

## 节点组自动伸缩

如果当前创建的虚拟机集群需要包含节点数类型为**自动伸缩**的 Worker 节点组，可以在此处启用**节点组自动伸缩**，以便在后续创建步骤中为 Worker 节点组设置自动伸缩范围。

> **说明**：
>
> 在虚拟机集群创建完成后也可以启用或禁用**节点组自动伸缩**。

## Control Plane 节点组

1. 设置节点组的名称。
2. 设置节点组中的节点数量。您可选择 **1**、**3** 或 **5**，为保证虚拟机集群 Control Plane 的高可用，建议选择 3 个或 5 个节点。
3. 配置节点组中每个节点的资源。

   | 参数 | 描述 |
   | --- | --- |
   | CPU | 节点组中每个节点的 CPU 分配量，默认为 4 vCPU，需至少分配 2 vCPU。 |
   | 内存 | 节点组中每个节点的内存分配量，默认为 8 GiB，需至少分配 6 GiB。 **注意**：若节点所在 SMTX OS 集群的服务器 CPU 架构为 AArch64，则需至少分配 10 GiB 内存，以免工作负载集群插件开启过多时内存不足。 |
   | 存储 | 节点组中每个节点的存储分配量，即节点对应虚拟机的磁盘分配容量，默认为 200 GiB 且不支持修改。 |
4. （可选）若节点组中的节点数大于 1，可选择启用**故障节点自动替换**。

   启用该功能后，当节点组中的故障节点的占比未超过设置的最大故障节点比例时，系统会自动删除故障节点并创建新的节点。

   若工作负载集群部署在启用双活特性的 SMTX OS 集群，则优先在优先可用域中新建节点；优先可用域资源不足时可在次级可用域中新建，优先可用域恢复后对应虚拟机不会自动切回。

   启用该功能需要设置以下参数：

   | 参数 | 描述 |
   | --- | --- |
   | 故障节点判定 | 判定节点故障的条件。需要勾选所需的条件，并设置时长阈值。 **注意：**  - 如果需要设置节点未就绪或未知状态持续时长阈值，为避免已经通过高可用（HA）恢复故障的虚拟机仍被识别为故障节点，部署在未启用双活特性的 SMTX OS 集群时建议设置的阈值不小于 5 分钟，部署在启用双活特性的 SMTX OS 集群时建议设置的阈值不小于 11 分钟，因为虚拟机高可用功能需要一定的故障恢复时间，节点恢复可用也需要一定的时间。 - 如果需要设置节点持续未启动时长阈值，为避免节点在启动完毕前即被识别为故障节点，部署在未启用双活特性的 SMTX OS 集群时建议设置的阈值不小于 5 分钟，部署在启用双活特性的 SMTX OS 集群时建议设置的阈值不小于 11 分钟。 |
   | 最大故障节点比例 | 节点组中允许被自动替换的故障节点数的最大比例，若故障节点数超过该比例，则不支持自动替换。需要设置一个不大于 40% 的百分数。假设节点组的总节点数为 5，此项设置为 40%，则当节点组中的故障节点小于或等于 2 个时会被自动替换，大于 2 个时不会被替换。 |

## Worker 节点组

您需要创建至少一个 Worker 节点组。

1. 设置节点组的名称。
2. 设置节点组中的节点数量。

   - **固定节点数**：需输入一个节点数量，数量至少为 1。
   - **自动伸缩**（仅当已启用**节点组自动伸缩**时支持选择）：需输入最小、最大节点数指定节点数范围，最小节点数不能小于 3。集群创建完成后，当前节点组的初始节点数将等于最小节点数，后续节点数可在设置的范围内自动调整，具体调整机制如下。

     | 调整行为 | 描述 |
     | --- | --- |
     | 自动增加 | - 当虚拟机集群中有不可调度的 Pod，且支持增加新节点使 Pod 被调度时，系统会自动创建符合该 Pod 需求的新节点。 - 如果为节点组配置了 GPU 设备，当集群中 GPU 设备的可使用数量小于请求数量，并且主机中仍有可挂载的同类 GPU 设备时，系统会自动创建新节点并为新节点挂载 GPU 设备。 |
     | 自动减少 | 该行为的触发机制与节点组是否配置 GPU 设备有关： - 若未配置 GPU 设备，则当虚拟机集群中某一 Worker 节点的 CPU 或内存的请求（request）比率最大值持续 10 分钟小于 50% 时，并且该节点上的 Pod 可被驱逐时，系统会自动驱逐 Pod 并删除节点。其中，CPU 的请求比率 = CPU 的请求数量之和 / CPU 的总量，内存的请求比率 = 内存的请求数量之和 / 内存的总量。 - 若已配置 GPU 设备，则仅当 GPU 设备的请求（request）比率持续 10 分钟小于 50% 时，并且该节点上的 Pod 可被驱逐时，系统才会自动驱逐 Pod 并删除节点。GPU 设备的请求比率 = GPU 设备的请求数量之和/ GPU 设备的总量。 |

     > **说明**：
     >
     > 若部署在启用双活特性的 SMTX OS 集群中，则优先在优先可用域中新建节点、根据资源负载情况在优先可用域或次级可用域中减少节点。
3. 配置节点组中每个节点的资源。

   | 参数 | 描述 |
   | --- | --- |
   | CPU | 节点组中每个节点的 CPU 分配量，默认为 4 vCPU，需至少分配 4 vCPU。 |
   | 内存 | 节点组中每个节点的内存分配量，默认为 8 GiB，需至少分配 8 GiB。 **注意**：若节点所在 SMTX OS 集群的服务器 CPU 架构为 AArch64，则需至少分配 10 GiB 内存，以免工作负载集群插件开启过多时内存不足。 |
   | GPU（仅当虚拟机集群所在 SMTX OS 集群存在挂载 GPU 设备的主机时展示；SMTX OS 集群启用双活特性时不支持） | 节点组中每个节点的 GPU 配置，默认不配置。如果需要配置，可根据在[确认工作负载集群使用 GPU 设备要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_23)时规划的信息选择“直通”或 “vGPU” 用途，再设置每个节点挂载的直通 GPU 或 vGPU 的型号和数量。  **说明**：  在 GPU 型号下拉列表中，将鼠标悬浮在可使用数量后的信息图标 i 时，可以查看各个主机可使用的 GPU 数量。 |
   | 存储 | 节点组中每个节点的存储分配量，即节点对应虚拟机的磁盘分配容量，默认为 200 GiB，需至少分配 200 GiB。 |
4. （可选）启用**故障节点自动替换**。启用该功能后，当节点组中的故障节点数满足故障节点数量限制条件时，系统会自动删除故障节点并创建新的节点。

   若工作负载集群部署在启用双活特性的 SMTX OS 集群中，则优先在优先可用域中新建节点；优先可用域资源不足时可在次级可用域中新建，优先可用域恢复后对应虚拟机不会自动切回。

   启用该功能需要设置以下参数：

   | 参数 | 描述 |
   | --- | --- |
   | 故障节点判定 | 判定节点故障的条件。需要勾选所需的条件，并设置时长阈值。 **注意：**  - 如果需要设置节点未就绪或未知状态持续时长阈值，为避免已经通过高可用（HA）恢复故障的虚拟机仍被识别为故障节点，部署在未启用双活特性的 SMTX OS 集群时建议设置的阈值不小于 5 分钟，部署在启用双活特性的 SMTX OS 集群时建议设置的阈值不小于 11 分钟，因为虚拟机高可用功能需要一定的故障恢复时间，节点恢复可用也需要一定的时间。 - 如果需要设置节点持续未启动时长阈值，为避免节点在启动完毕前即被识别为故障节点，部署在未启用双活特性的 SMTX OS 集群时建议设置的阈值不小于 5 分钟，部署在启用双活特性的 SMTX OS 集群时建议设置的阈值不小于 11 分钟。 |
   | 故障节点数量限制 | 对可触发系统执行节点替换的故障节点数量的限制条件。需要选择以下任一一种维度进行限制： - **故障节点比例**：节点组中允许被自动替换的故障节点数的最大比例，若故障节点数超过该比例，则不支持自动替换。需要设置一个百分数。假设节点组的总节点数为 6，此项设置为 40%，则当节点组中的故障节点小于或等于 2 个时会被自动替换，大于 2 个时不会被替换。 - **故障节点数范围**：可触发系统执行节点替换的故障节点数范围。需要输入最小、最大故障节点数来指定范围。假设节点组的总节点数为 10，此处设置的范围是 6 ～ 8，则仅当节点组中的故障节点个数为 6、7 或 8 时，故障节点才会被自动替换，否则不会被替换。 |

## 节点访问配置

您需要配置用于访问虚拟机集群节点的默认账户密码或 SSH 公钥。

- **默认账户密码**：输入默认账户 `smartx` 的密码，留空代表不配置。您需要输入两次密码，以对密码进行确认。
- **SSH 公钥**：输入 SSH 公钥。可以手动输入或者从文件中提取，留空代表不配置。

---

## 创建工作负载集群 > 创建虚拟机集群 > 配置网络

# 配置网络

请根据规划的[工作负载集群的网络信息](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_18)，配置网络相关信息。

**操作步骤**

1. 配置 Control Plane 虚拟 IP。

   配置该虚拟 IP 后，即使 Control Plane 节点组中存在节点故障，只要在允许的故障范围内，即可通过该 IP 访问可用的 Control Plane 节点。

   有以下两种配置方式：

   - **IP 池自动分配**：选择根据规划[创建的工作负载集群 IP 池](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_12)，将从该 IP 池中自动分配一个 Control Plane 虚拟 IP 。
   - **手动输入**：输入规划的 Control Plane 虚拟 IP 地址。
2. 配置集群网络。

   | 参数 | 描述 |
   | --- | --- |
   | 业务网卡 | 选择业务网卡使用的虚拟机网络，并根据在[业务网卡网络要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_19)中规划的信息配置 IP，有以下两种配置方式： - IP 池自动分配 - 启动网卡 DHCP |
   | DNS 服务器地址（可选） | 若 DHCP Server 中未配置 DNS 服务器信息，则输入为其指定的 DNS 服务器地址，否则该项留空。DNS 服务器地址不能为 127.0.0.1。 |
   | SMTX ZBS CSI 专用网卡（仅当选择 SMTX ZBS CSI 插件时展示） | - 若规划虚拟机集群使用其所在 SMTX OS 集群的存储，请确保已[创建 SMTX ZBS CSI 接入配置](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_11)，创建完成后系统会自动填充网络和接入虚拟 IP 的信息，您只需要选择为 SMTX ZBS CSI 专用网卡创建的用于接入该 SMTX OS 集群的 IP 池。 **注意：**若该 SMTX ZBS CSI 接入配置是在 1.2.0 及之前版本的 SKS 服务上创建的（即含有 DHCP 配置），需要将自动填充的虚拟机网络修改为手动在 SMTX OS 存储网络所在虚拟分布式交换机上创建的虚拟机网络。 - 若规划虚拟机集群使用其他集群的存储，请根据实际规划选择集群节点的 SMTX ZBS CSI 专用网卡使用的虚拟机网络，填写目标存储集群的接入虚拟 IP，并选择为 SMTX ZBS CSI 专用网卡创建的用于接入该目标存储集群的 IP 池。**注意：**接入虚拟 IP 在虚拟机集群创建完成后不支持修改。 |
   | EIC 专用网卡（仅当已选择 EIC 插件时展示） | 根据在 [EIC 专用网卡网络要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_20)中规划的信息，填写网络、子网 CIDR 块、网关以及 Pod IP 池。 |
3. 配置 Service IP CIDR 和 Pod IP CIDR，该网段不能与集群网络使用的网段重合、不能使用公网地址。不同的集群之间 Service IP CIDR、以及 Pod IP CIDR 可以使用相同网段。

   | 参数 | 描述 |
   | --- | --- |
   | Service IP CIDR | 输入一段用于 Service 使用的 IP 地址。 |
   | Pod IP CIDR | 仅当所选的 CNI 插件为 Calico 时，需要配置该项。输入一段用于 Pod 使用的 IP 地址。 |
4. 单击**下一步**。

---

## 创建工作负载集群 > 创建虚拟机集群 > 配置 K8s 集群

# 配置 K8s 集群

SKS 对 etcd、kube-apiserver、kube-controller-manager、kube-scheduler、kubelet 等 K8s 组件的默认配置可参考[默认参数说明](#%E9%BB%98%E8%AE%A4%E5%8F%82%E6%95%B0%E8%AF%B4%E6%98%8E)。出于稳定性考虑，在 UI 界面仅允许编辑这些组件的部分参数，除组件参数外，您还可配置节点文件、系统参数调优、命令执行等高级配置，配置格式可参考 [YAML 配置文件](#yaml-%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6)，各个配置字段的含义可参考[参数配置说明](#%E5%8F%82%E6%95%B0%E9%85%8D%E7%BD%AE%E8%AF%B4%E6%98%8E)。

- 如需编辑集群配置，请在**配置内容**中填写变更的参数配置，然后单击**下一步**。
- 如需编辑 UI 界面不支持的组件参数（界面会提示错误），请联系 SmartX 售后工程师进行处理。
- 如无需编辑参数，可将**配置内容**留空，直接单击**下一步**。

> **注意**：
>
> 若 K8s 组件参数配置错误，则可能导致虚拟机集群创建失败。如非必要需求，请勿随意编辑参数配置。

## 默认参数说明

SKS 默认配置的 K8s 组件参数及说明如下。

### etcd

| 参数 | 默认值 | 描述 |
| --- | --- | --- |
| cipher-suites | "TLS\_AES\_128\_GCM\_​SHA256,​TLS\_AES\_256\_GCM\_SHA384,​TLS\_CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_RSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_RSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_ECDSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_RSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_RSA\_WITH\_AES\_​128\_GCM\_SHA256,​TLS\_RSA\_WITH\_AES\_​256\_GCM\_SHA384" | etcd 服务器端的加密算法列表，以英文逗号分隔。如果不设置，则使用 Go 语言加密包的默认算法列表。 |

### kube-apiserver

| 参数 | 默认值 | 描述 |
| --- | --- | --- |
| profiling | "false" | 是否通过 Web 接口 host:port/debug/pprof/ 启用性能分析。默认值为 false，即不启用性能分析。 |
| audit-log-batch-buffer-size | "102400" | 批处理和写入事件之前用于缓存事件的缓冲区大小。 仅在批处理模式下使用。 |
| audit-log-batch-max-size | "10" | 每个批次的最大大小。仅在批处理模式下使用。 |
| audit-log-batch-max-wait | 5s | 强制写入尚未达到最大大小的批次之前要等待的时间。 仅在批处理模式下使用。 |
| audit-log-path | /var/log/apiserver/audit.log | 指定用于存储 kube-apiserver 审计日志文件的路径，所有到达 API 服务器的请求均记录在该文件中。 |
| audit-log-maxage | "7" | 根据文件名中编码的时间戳保留旧审计日志文件的最大天数。 |
| audit-log-maxbackup | "5" | 指定需要保留的旧审计日志文件的个数上限。该值设置为 0 时表示对文件个数无限制。 |
| audit-log-maxsize | "100" | 审计日志文件的最大大小，以兆字节为单位。当审计日志文件达到指定的最大大小后，会将当前的审计日志文件重命名并创建一个新的审计日志文件，以便继续记录。 |
| audit-log-mode | batch | 用于发送审计事件的策略。已知的模式包含批处理（batch）、阻塞（blocking）、严格阻塞（blocking-strict）。 阻塞（blocking）表示发送事件应阻止服务器响应；批处理（batch）会在后端引发异步缓冲和写入事件。 |
| audit-log-truncate-enabled | "true" | 是否启用事件和批次截断。 |
| enable-admission-plugins | EventRateLimit | 除了默认启用的插件之外需要启用的准入插件，以英文逗号分隔。  默认启用的插件包括：  NamespaceLifecycle,​LimitRanger,​ServiceAccount,​TaintNodesByCondition,​PodSecurity,​Priority,​DefaultTolerationSeconds,​DefaultStorageClass,​StorageObjectInUseProtection,​PersistentVolumeClaimResize,​RuntimeClass,​CertificateApproval,​CertificateSigning,​ClusterTrustBundleAttest,​CertificateSubjectRestriction,​DefaultIngressClass,​MutatingAdmissionWebhook,​ValidatingAdmissionPolicy,​ValidatingAdmissionWebhook,​ResourceQuota |
| admission-control-config-file | /etc/kubernetes/admission.yaml | 指定准入控制配置文件的路径。 |
| audit-policy-file | /etc/kubernetes/auditpolicy.yaml | 指定审计策略配置文件的路径。 |
| request-timeout | "300s" | 指定向 Kubernetes API 服务器发出请求时的默认超时时间。对于特定类型的请求，该值可能会被 `--min-request-timeout` 等标志覆盖。 |
| tls-min-version | "VersionTLS12" | kube-apiserver 支持的最小 TLS 版本。 |
| tls-cipher-suites | "TLS\_AES\_128\_GCM\_​SHA256,​TLS\_AES\_256\_GCM\_SHA384,​TLS\_CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_RSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_RSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_ECDSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_RSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_RSA\_WITH\_AES\_​128\_GCM\_SHA256,​TLS\_RSA\_WITH\_AES\_​256\_GCM\_SHA384" | 服务器端的加密算法列表，以英文逗号分隔。如果不设置，则使用 Go 语言加密包的默认算法列表。 |

### kube-controller-manager

| 参数 | 默认值 | 描述 |
| --- | --- | --- |
| profiling | "false" | 是否通过 Web 接口 host:port/debug/pprof/ 启用性能分析。默认值为 false，即不启用性能分析。 |
| terminated-pod-gc-threshold | "10" | 在已终止 Pod 垃圾收集器删除已终止 Pod 之前，可以保留的已终止 Pod 的个数上限。若此值小于等于 0，则相当于禁止垃圾回收已终止的 Pod。 |
| tls-min-version | "VersionTLS12" | kube-controller-manager 支持的最小 TLS 版本。 |
| tls-cipher-suites | "TLS\_AES\_128\_GCM\_​SHA256,​TLS\_AES\_256\_GCM\_SHA384,​TLS\_CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_RSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_RSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_ECDSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_RSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_RSA\_WITH\_AES\_​128\_GCM\_SHA256,​TLS\_RSA\_WITH\_AES\_​256\_GCM\_SHA384" | 服务器端的加密算法列表，以英文逗号分隔。如果不设置，则使用 Go 语言加密包的默认算法列表。 |

### kube-scheduler

| 参数 | 默认值 | 描述 |
| --- | --- | --- |
| profiling | "false" | 是否通过 Web 接口 host:port/debug/pprof/ 启用性能分析。默认值为 false，即不启用性能分析。 |
| tls-min-version | "VersionTLS12" | kube-scheduler 支持的最小 TLS 版本。 |
| tls-cipher-suites | "TLS\_AES\_128\_GCM\_​SHA256,​TLS\_AES\_256\_GCM\_SHA384,​TLS\_CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_RSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_RSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_ECDSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_RSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_RSA\_WITH\_AES\_​128\_GCM\_SHA256,​TLS\_RSA\_WITH\_AES\_​256\_GCM\_SHA384" | 服务器端的加密算法列表，以英文逗号分隔。如果不设置，则使用 Go 语言加密包的默认算法列表。 |

### kubelet

- **kubeletExtraArgs**

  | 参数 | 默认值 | 描述 |
  | --- | --- | --- |
  | protect-kernel-defaults | "true" | 设置为 true 表示强制使用 kubelet 的默认内核配置。当任何内核可调参数与 kubelet 默认值不同时，kubelet 都会报错。 |
  | event-qps | "0" | 限制每秒可生成的事件数量，设置为 0 表示不限制。 |
  | tls-min-version | "VersionTLS12" | kubelet 支持的最小 TLS 版本。 |
  | tls-cipher-suites | "TLS\_AES\_128\_GCM\_​SHA256,​TLS\_AES\_256\_GCM\_SHA384,​TLS\_CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_RSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_RSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_ECDSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_RSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_RSA\_WITH\_AES\_​128\_GCM\_SHA256,​TLS\_RSA\_WITH\_AES\_​256\_GCM\_SHA384" | 服务器端的加密算法列表，以英文逗号分隔。如果不设置，则使用 Go 语言加密包的默认算法列表。 |
  | serialize-image-pulls | "false" | 设置为 true 表示 kubelet 每次仅拉取一个镜像。当前默认配置 `false`，即 kubelet 支持并发拉取多个镜像。 |
- **kubeletConfiguration**

  | 参数 | 默认值 | 描述 |
  | --- | --- | --- |
  | shutdownGracePeriod | 45s | 设置 Kubernetes 节点对应的虚拟机或物理机在正常关机时，Kubernetes 节点自身需要的延时以及为节点上运行的 Pod 提供的终止宽限期总时长。 |
  | shutdownGracePeriod​CriticalPods | 30s | 设置 Kubernetes 节点所在的虚拟机在正常关机时，Kubernetes 节点提供给关键性 Pod 的终止宽限期总时长。此时长要短于 shutdownGracePeriod。  例如：shutdownGracePeriod = 30s，​shutdownGracePeriod​CriticalPods = 10s。​Kubernetes 节点所在的虚拟机正常关机时，kubelet 先进行普通 Pod 的优雅退出，预留给普通 Pod 的终止宽限期为 shutdownGracePeriod - shutdownGracePeriod​CriticalPods = 20s，​之后进行关键性 Pod 的优雅退出，预留给系统关键性 Pod 的终止宽限期为 10s。 |

## YAML 配置文件

YAML 配置文件示例如下。以下配置均为 SKS 的默认配置，您可按需粘贴参数至**配置内容**框中修改。

```
controlPlane:
  clusterConfiguration:
    # Refer to https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/
    apiServer:
      extraArgs:
        audit-log-maxage: '7'
        audit-log-maxbackup: '5'
        audit-log-maxsize: '100'
        request-timeout: 300s
      extraVolumes:
        - hostPath: /var/log/apiserver
          mountPath: /var/log/apiserver
          name: apiserver-log
          pathType: DirectoryOrCreate
        - hostPath: /etc/kubernetes/admission.yaml
          mountPath: /etc/kubernetes/admission.yaml
          name: admission-config
          pathType: FileOrCreate
          readOnly: true
        - hostPath: /etc/kubernetes/auditpolicy.yaml
          mountPath: /etc/kubernetes/auditpolicy.yaml
          name: audit-policy
          pathType: FileOrCreate
          readOnly: true
    controllerManager:
      # Refer to https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/
      extraArgs:
        terminated-pod-gc-threshold: '10'
    etcd:
      local:
        # Refer to https://etcd.io/docs/v3.5/op-guide/configuration/#command-line-flags
        extraArgs: {}
    scheduler:
      # Refer to https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/
      extraArgs: {}
  files:
    - content: |
        apiVersion: apiserver.config.k8s.io/v1
        kind: AdmissionConfiguration
        plugins:
          - name: EventRateLimit
            configuration:
              apiVersion: eventratelimit.admission.k8s.io/v1alpha1
              kind: Configuration
              limits:
                - type: Server
                  burst: 20000
                  qps: 5000
      owner: root:root
      path: /etc/kubernetes/admission.yaml
    - content: |
        apiVersion: audit.k8s.io/v1
        kind: Policy
        metadata:
          creationTimestamp: null
        omitManagedFields: true
        omitStages:
        - RequestReceived
        - ResponseStarted
        rules:
        - level: None
          userGroups:
          - system:nodes
          - system:serviceaccounts:kube-system
          - system:unauthenticated
        - level: None
          users:
          - system:kube-scheduler
          - system:volume-scheduler
          - system:kube-controller-manager
          - system:serviceaccount:sks-system:sks-packages-sa
          - system:serviceaccount:kapp-controller:kapp-controller-sa
          - system:serviceaccount:sks-system:tigera-operator
          - system:serviceaccount:sks-system-monitoring:prometheus-operator
        - level: None
          nonResourceURLs:
          - /api*
          - /version
          - /healthz*
          - /swagger*
          - /ready*
        - level: None
          resources:
          - group: coordination.k8s.io
            resources:
            - leases
          - group: authentication.k8s.io
            resources:
            - tokenreviews
          - group: authorization.k8s.io
        - level: Metadata
          verbs:
          - create
          - delete
          - deletecollection
          - patch
          - update
      owner: root:root
      path: /etc/kubernetes/auditpolicy.yaml
      permissions: '0644'
  initConfiguration:
    nodeRegistration:
      kubeletExtraArgs:
        event-qps: '0'
  joinConfiguration:
    nodeRegistration:
      kubeletExtraArgs:
        event-qps: '0'
  preKubeadmCommands: []
  postKubeadmCommands: []
  nodeIdempotentCommands: []
  sysctlParams: {}
workers:
  joinConfiguration:
    nodeRegistration:
      kubeletExtraArgs:
        event-qps: "0"
  preKubeadmCommands: []
  postKubeadmCommands: []
  nodeIdempotentCommands: []
  sysctlParams: {}
  files: []
# kubeletConfiguration is a patch for the KubeletConfiguration to modify the default or current values in the global kubelet-config ConfigMap of the cluster.
kubeletConfiguration:
  shutdownGracePeriod: 45s
  shutdownGracePeriodCriticalPods: 30s
```

## 参数配置说明

### KubernetesConfiguration

KubernetesConfiguration 定义了 Kubernetes 集群的参数配置，是当前 UI 中 **K8s 集群配置**的顶层结构。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `controlPlane` （可选） | [RoleConfiguration](#roleconfiguration) | Control Plane 节点的配置 |
| `workers` （可选） | [RoleConfiguration](#roleconfiguration) | Worker 节点的配置 |
| `kubeletConfiguration` （可选） | runtime.RawExtension | [Kubelet 配置文件](https://kubernetes.io/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/)，YAML 格式，以 patch 形式作用于集群 |

### RoleConfiguration

RoleConfiguration 指定了 Kubernetes 集群中特定角色的配置，部分字段只生效于特定角色。

> **注意**：
>
> 默认情况下，Control Plane 节点的 `initConfiguration`、`joinConfiguration` 以及 Worker 节点的 `joinConfiguration` 三处配置相同，在 UI 中仅修改 `initConfiguration` 时，系统会自动将修改同步至其余两处配置。若需避免系统同步修改，可以在 UI 中以声明式方式填写两处 `joinConfiguration` 的配置。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `clusterConfiguration` （可选） | [ClusterConfiguration](#clusterconfiguration) | 集群级别的配置，主要包含 `controlPlane` 组件的配置，只在 `controlPlane` 中生效 |
| `initConfiguration` （可选） | [InitConfiguration](#initconfiguration) | kubeadm init 配置，作用于第一个 Control Plane 节点，用于设置 kubelet 的启动参数，只在 `controlPlane` 中生效 |
| `joinConfiguration` （可选） | [JoinConfiguration](#joinconfiguration) | kubeadm join 配置，作用于后续的 Control Plane 节点及 Worker 节点 |
| `files` （可选） | [[]File](#file) | 需要在节点上创建的文件列表 |
| `preKubeadmCommands` （可选） | []string | 在节点创建时 kubeadm 运行前执行的命令，节点创建后不再执行 |
| `postKubeadmCommands` （可选） | []string | 在节点创建时 kubeadm 运行后执行的命令，节点创建后不再执行 |
| `sysctlParams` （可选） | map[string]string | 在节点上设置的 sysctl 参数 |
| `nodeIdempotentCommands` （可选） | []string | 可以在节点上运行的命令，会在节点创建后及原地更新中被执行，由于会多次执行，请保证命令的幂等性 |

### ClusterConfiguration

ClusterConfiguration 包含集群范围的 kubeadm 集群配置。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `etcd` （可选） | [Etcd](#etcd-1) | Etcd 配置 |
| `apiServer` （可选） | [ControlPlaneComponent](#controlplanecomponent) | API Server 配置 |
| `controllerManager` （可选） | [ControlPlaneComponent](#controlplanecomponent) | Controller Manager 配置 |
| `scheduler` （可选） | [ControlPlaneComponent](#controlplanecomponent) | Scheduler 配置 |

### Etcd

Etcd 包含 Etcd 配置的元素。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `local` （可选） | [LocalEtcd](#localetcd) | 本地 Etcd 集群配置 |

### LocalEtcd

LocalEtcd 描述 kubeadm 应该在本地运行 Etcd 集群。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `extraArgs` （可选） | map[string]string | Etcd 的额外命令行参数 |

### ControlPlaneComponent

ControlPlaneComponent 包含控制平面组件通用的设置。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `extraArgs` （可选） | map[string]string | 控制平面组件的额外命令行参数 |
| `extraVolumes` （可选） | [[]HostPathMount](#hostpathmount) | 控制平面组件的额外卷挂载 |

### HostPathMount

HostPathMount 包含描述从主机挂载的卷的元素。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `name` （必需） | string | 卷的名称 |
| `hostPath` （必需） | string | 主机上的路径 |
| `mountPath` （必需） | string | 容器内的挂载路径 |
| `readOnly` （可选） | bool | 是否以只读模式挂载 |
| `pathType` （可选） | string | 主机路径的类型 |

### InitConfiguration

InitConfiguration 是特定于 "kubeadm init" 的配置。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `nodeRegistration` （可选） | [NodeRegistrationOptions](#noderegistrationoptions) | 与节点注册相关的字段 |

### JoinConfiguration

JoinConfiguration 是特定于 "kubeadm join" 的配置。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `nodeRegistration` （可选） | [NodeRegistrationOptions](#noderegistrationoptions) | 与节点注册相关的字段 |

### NodeRegistrationOptions

NodeRegistrationOptions 包含节点注册相关的字段。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `kubeletExtraArgs` （可选） | map[string]string | Kubelet 的额外命令行参数 |

### File

File 定义了在节点中生成文件所需的输入字段。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `path` （必需） | string | 指定存储文件的磁盘完整路径 |
| `owner` （可选） | string | 指定文件的所有权，例如 `root:root` |
| `permissions` （可选） | string | 指定分配给文件的权限，例如 `'0640'` |
| `encoding` （可选） | string | 指定文件内容的编码，可选值：`base64`，`gzip`，`gzip+base64` |
| `append` （可选） | bool | 指定当路径已存在时，是否将内容追加到现有文件。若不追加，新内容将覆盖原有内容 |
| `content` （可选） | string | 文件的实际内容 |

---

## 创建工作负载集群 > 创建虚拟机集群 > 配置集群插件

# 配置集群插件

创建虚拟机集群时，您可以修改 Calico CNI、SMTX ELF CSI、节点组自动伸缩和 GPU 插件的默认参数；也可以根据业务需求启用**可观测性**、**日志**、**外部负载均衡器**和 **Ingress 控制器**相关插件，并配置相关插件参数。

配置完成后单击**创建**，即可开始创建虚拟机集群。

> **说明**：
>
> EIC 插件使用默认参数，不支持修改。

## 配置 Calico CNI

您可以通过 UI 界面或 YAML 配置 [Calico CNI](https://docs.tigera.io/calico/latest/about) 插件。

该插件仅在创建虚拟机集群时支持修改参数配置，创建完成后不可通过 UI 界面修改。

- **通过 UI 界面配置**

  1. 选择**网络封装方式**。

     - **None**：无封装模式，即容器之间的通信不进行封装，直接使用标准的 IP 路由进行通信。
     - **IPIP**：使用 IP-in-IP 封装模式，将容器的 IP 数据包封装在另一个 IP 数据包中，实现容器之间的跨节点通信。
     - **VXLAN**：使用 VXLAN 封装模式，将容器的 IP 数据包封装在 UDP 数据包中，实现容器之间的跨节点通信。
  2. 设置是否**启用 BGP**。

     - 当**网络封装方式**为 **None** 和 **IPIP** 时，默认启用 BGP，不可修改。
     - 当**网络封装方式**为 **VXLAN** 时，默认不启用 BGP，不可修改。
- **通过 YAML 配置**

  YAML 示例如下，您可以按需修改 `encapsulation` 和 `cidr` 参数。

  ```
  installation:
    calicoNetwork:
      bgp: Enabled   # 指定是否启用 BGP，不允许修改
      ipPools:    # 仅支持配置一个 IP 池
        - encapsulation: IPIP  # 指定网络封装方式
          cidr: 172.16.0.0/16   # 指定 IP Pool 的 CIDR，需在 Pod IP CIDR 的地址范围内；该范围不能与集群使用的网络重合，且不能使用公网地址，不同的集群之间可以使用相同网段。
  ```

## 配置 SMTX ELF CSI

您可以通过 YAML 配置 SMTX ELF CSI 插件。

**参数说明**

支持配置的参数如下表所示。

| 参数 | | | 描述 |
| --- | --- | --- | --- |
| driver | maxSnapshotsPerVolume | | 每个卷的快照最大创建数量，默认为 `3`。 |
| preferredVolumeBusType | | 卷优先挂载到的虚拟机总线，默认为 `VIRTIO`。 |
| storageClass | parameters | storagePolicy | 默认创建的 StorageClass 配置的卷存储策略。  工作负载集群部署在未启用双活特性的集群时，默认为 `REPLICA_2_THIN_PROVISION`，​工作负载集群部署在启用双活特性的集群时，默认为 `REPLICA_3_THIN_PROVISION`。  支持配置为​ `REPLICA_2_THIN_PROVISION`、​`REPLICA_3_THIN_PROVISION`、​`REPLICA_2_THICK_PROVISION` 或 ​`REPLICA_3_THICK_PROVISION`。 |
| csi.storage.k8s.io/fstype | 默认创建的 StorageClass 配置的卷默认挂载文件类型，默认为 `ext4`，支持配置为 `ext2`、`ext3`、 `ext4` 或 `xfs`。 |
| reclaimPolicy | | 默认创建的 StorageClass 配置的卷删除策略，默认为 `Delete`。 |

**YAML 示例**

```
driver:
  maxSnapshotsPerVolume: 3
  preferredVolumeBusType: VIRTIO
storageClass:
  reclaimPolicy: Delete
  parameters:
    storagePolicy: REPLICA_2_THIN_PROVISION
    csi.storage.k8s.io/fstype: ext4
```

## 配置 SMTX ZBS CSI

当您在**基本信息**界面选择了 SMTX ZBS CSI 插件时，将默认开启该插件，不支持关闭，您可以通过 YAML 配置 SMTX ZBS CSI 插件。

**参数说明**

支持配置的参数如下表所示。

| 参数 | | | 描述 |
| --- | --- | --- | --- |
| driver | | maxVolumesPerNode | 单节点可挂载的 PV 的最大数量，默认为 `128`。 |
| controller.driver.​podDeletePolicy | 当挂载了由 SMTX ZBS CSI 插件创建的 PVC 的 Pod 所在的 Worker 节点发生故障时，是否自动删除该 Pod 并在其他健康的 Worker 节点重建，默认为 `no-delete-pod`，还支持配置为 `delete-deployment-pod`、`delete-statefulset-pod`、`delete-both-statefulset-and-deployment-pod`。 |
| storageClass | parameters | csi.storage.k8s.io/fstype | 使用默认创建的 StorageClass 制备的 PV 的文件系统类型，默认为 `ext4`，还支持配置为 `xfs`。 |
| replicaFactor | - 工作负载集群部署在未启用双活特性的 SMTX OS 集群时，使用默认创建的 StorageClass 制备的 PV 的副本数默认为 `2`，还支持配置为 `3`。 - 工作负载集群部署在启用双活特性的 SMTX OS 集群时，使用默认创建的 StorageClass 制备的 PV 的副本数默认为 `3`。   **注意**：若工作负载集群部署在未启用双活特性的 SMTX OS 集群，但 SMTX ZBS CSI 对接的外部存储集群为双活集群，需要手动更新副本数为 3，以确保插件可用。 |
| thinProvision | 使用默认创建的 StorageClass 制备的 PV 的置备类型，默认为 `true`（精简置备），还支持配置为 `false`（厚置备）。 |

**YAML 示例**

```
driver:
  maxVolumesPerNode: 128
    controller:
      driver:
        podDeletePolicy: delete-deployment-pod
storageClass:
  parameters:
    csi.storage.k8s.io/fstype: "ext4"
    replicaFactor: "2"
    thinProvision: "true"
```

## 配置节点组自动伸缩

当您在**节点配置**界面开启节点组自动伸缩后，即可通过 YAML 配置 [cluster-autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) 插件的参数。

**参数说明**

支持配置的参数如下表所示。

| 参数 | | 描述 |
| --- | --- | --- |
| extraArgs | skip-nodes-with-local-storage | 设置是否跳过具有本地存储的节点，默认为 `false`。当此参数设置为 `true` 时，Cluster Autoscaler 不会将具有本地存储的节点作为 scale-down 的目标。 |
| new-pod-scale-up-delay | 指定从发现新 Pod 到实际开始扩容节点的延时，默认为 `1m`。 |
| scale-down-enabled | 指定是否对集群缩容，默认为 `true`。 |
| scale-down-delay-after-add | 指定扩容节点后多久可恢复缩减节点操作，默认为 `10m`。 |
| scale-down-delay-after-delete | 指定删除节点后多久可恢复缩减节点操作，默认为 `10s`。 |
| scale-down-unneeded-time | 指定节点被标记为不需要后，多久可进行节点删除操作。默认为 `10m`。 |
| scale-down-utilization-threshold | 指定节点缩减的资源利用率阈值，低于该阈值后可缩减节点。默认为 `0.5`，即 50%。 |
| scan-interval | 指定集群进行扩展或缩减节点操作的频率，默认为 `10s`。 |

**YAML 示例**

YAML 示例如下，您可以按需修改相关参数值。

```
extraArgs:
  skip-nodes-with-local-storage: false
  new-pod-scale-up-delay: 1m
  scale-down-enabled: true
  scale-down-delay-after-add: 10m
  scale-down-delay-after-delete: 10s
  scale-down-unneeded-time: 10m 
  scale-down-utilization-threshold: 0.5
  scan-interval: 10s
```

## 配置 GPU

当您在**节点配置**界面为任一 Worker 节点组挂载了 GPU 设备时，将展示 **NVIDIA GPU Operator** 插件的配置项，并自动开启。您还可通过 YAML 配置该插件的参数，如果在此处不配置，也可以在集群创建成功后再进行配置。

> **注意**：
>
> - 如果关闭此插件，需要手动在集群中安装 [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/install-gpu-operator-vgpu.html)，否则将导致 GPU 的相关功能异常。
> - 如果集群配置了 vGPU，必须通过配置 `licensingConfig` 参数来配置 NVIDIA vGPU 许可，否则将影响 vGPU 功能的使用。

**参数说明**

支持配置的参数如下表所示。

| 参数 | | | 描述 |
| --- | --- | --- | --- |
| devicePlugin | config | | 启用集群的 TimeSlicing 功能的配置，详细配置可参考 YAML 示例。  **风险提示：**  启用 TimeSlicing 功能后，单个直通 GPU/ vGPU 可以同时分配给多个 Pod 使用，如果同时启用监控插件，GPU 监控采集器将无法识别正在使用 GPU 资源的 Pod，导致无法查看依赖于 Pod 标签的监控视图下的 GPU 图表。 |
| driver | licensingConfig | nlsEnabled | 是否启用 NVIDIA vGPU 许可系统，默认为 `false`，当集群配置了 vGPU 时 SKS 会自动将此项配置为 `true`。 |
| clientConfiguration​Token | NVIDIA vGPU 许可，默认不配置，如果需要配置，可参考 [NVIDIA 官方文档](https://docs.nvidia.com/license-system/latest/nvidia-license-system-quick-start-guide/index.html)自行向 NVIDIA 申请许可并在此项填入许可。 |

**YAML 示例**

YAML 示例如下，您可以按需修改相关参数值。

```
devicePlugin:
  config:
    create: true
    name: time-slicing
    default: any
    data:
      any: |-
        sharing:
          timeSlicing:
            resources:
            - name: nvidia.com/gpu
              replicas: 4
driver:
  licensingConfig:
    nlsEnabled: true
    clientConfigurationToken: "test-fake-token"
```

## 配置可观测性

建议您为虚拟机集群关联可观测性服务，以便启用监控、报警、日志、事件、审计功能。

> **注意**：
>
> 为集群关联可观测性服务前，请确保集群节点的业务网卡所在虚拟机网络、可观测性服务虚拟机的虚拟网卡所在虚拟机网络两者之间三层互通，并且建议先[为 SKS 系统服务关联可观测性服务](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_109)。

### 关联可观测性服务

启用**关联可观测性服务**，然后选择需要关联的可观测性服务。

### 启用监控

您可以启用**监控**，以查看集群的监控信息。

启用后，您还可通过 YAML 配置 OBS-Monitoring-Agent 和 Prometheus 参数。

**配置 OBS-Monitoring-Agent 参数**

- **参数说明**

  | 参数 | | | 描述 |
  | --- | --- | --- | --- |
  | metrics | remote\_write\_global | labels | 自定义键值对，为发送到外部系统的 metrics 添加特定标签，通常用于标识数据源。默认不配置。 |
  | remote\_write | url | 接收监控数据的目标地址，默认不配置。 |
  | tls\_insecure\_skip\_​verify | 是否跳过 TLS 证书的验证，默认为 `false`。 **注意：**如果 URL 使用 HTTPS 协议并且证书为自签名，则需设置为 `true`。 |
  | send\_timeout | 发送请求时的超时时间，默认为 `1m`。 |
  | headers | HTTP 请求头，默认不配置。 |
  | bearer\_auth.token | 用于 Bearer 认证的 token，默认不配置。 |
  | basic\_auth.username | BasicAuth 用户名，默认不配置。 |
  | basic\_auth.password | BasicAuth 密码，默认不配置。 |
  | resources | requests | cpu | CPU 请求值，默认为 `250m`。 |
  | memory | 内存请求值，默认为 `300Mi`。 |
  | limits | cpu | CPU 限额，默认为 `"2"`。 |
- **YAML 示例**

  ```
  agent:
    # 用于将 metrics 发送到外部系统
    metrics:
      remote_write_global:
        labels:
          # 为发送到远端的 metrics 添加特定 label，通常可用于标识数据源
          # 非必填
          source: sks-monitor
          my_key: my_value
      remote_write:
      - url: https://remote-prometheus.example.com/api/v1/write
        tls_insecure_skip_verify: true
        send_timeout: 30s
        # 多种认证方式，根据需要选择，无认证则不需要

        # 直接在 header 中插入字段
        headers:
          Authorization: 'Bearer eyJhbGciOiJ...'

        bearer_auth:
          token: 'eyJhbGciOiJ...'

        basic_auth:
          username: remote
          password: my_secret

    # 调整 agent 资源配置
    resources:
      requests:
        cpu: 250m
        memory: 300Mi
      limits:
        cpu: "2"
  ```

**配置 Prometheus 参数**

- **参数说明**

  | 参数 | | | | 描述 |
  | --- | --- | --- | --- | --- |
  | grafana | resources | limits | cpu | CPU 限额，默认为 `500m`。 |
  | memory | 内存限额，默认为 `300Mi`。 |
  | requests | cpu | CPU 请求值，默认为 `10m`。 |
  | memory | 内存请求值，默认为 `100Mi`。 |
  | persistent | enable | | 是否启用持久化存储，默认为 `true`。 |
  | storageClassName | | 持久化存储使用的存储类名称。 |
  | accessModes | | 持久卷的访问方式，默认为 `ReadWriteOnce`。 |
  | size | | 持久卷的大小，默认为 `1Gi`。 |
  | config | [auth.​anonymous] | enabled | 是否开启匿名登录，默认为 `true`。 |
  | [security] | admin\_password | 指定 Grafana Web UI 的 admin 账号的密码，默认值请参见 [Grafana 官方文档](https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/)。 |
  | prometheus | scrapeInterval | | | 从目标抓取度量数据的时间间隔，默认为 `30s`。 |
  | scrapeTimeout | | | 单次抓取的最大超时时间，默认为 `10s`。 |
  | prometheus​Overrides | monitorExtraNamespaces | | | 指定 SKS 定义的 namespace 之外的名字空间列表，以便从这些名字空间中抓取 prometheus CR 资源，例如自定义 namespace 中的 serviceMonitor。默认不配置。 |
- **YAML 示例**

  YAML 示例如下，您可以按需修改相关参数值。

  ```
  grafana:
    persistent:
      size: 1Gi
    config: |
      [security]
      admin_password = ***  # 指定 Grafana Web UI 的 admin 账号的密码
      [auth.anonymous]
      enabled = true
      [date_formats]
      default_timezone = Asia/Shanghai
      use_browser_locale = true
      default_timezone = browser
      [dashboards]
      # Path to the default home dashboard. If this value is empty, then Grafana uses StaticRootPath + "dashboards/home.json"
      default_home_dashboard_path = /grafana-dashboard-definitions/0/k8s-resources-cluster/k8s-resources-cluster.json

  prometheus:
      scrapeInterval: 30s
      scrapeTimeout: 10s

  prometheusOverrides:
    monitorExtraNamespaces:
      - my-ns1
      - my-ns2
  ```

### 启用报警

当**监控**已启用时，您可以启用**报警**。

启用后，您不仅可以查看报警信息，还可以在 CloudTower 的**报警**主界面查看和编辑报警规则、以及配置报警通知。

### 启用日志

您可以启用**日志**，以查看集群的日志信息。

启用后，您还可通过 YAML 配置 OBS-Logging-Agent 参数。

**YAML 示例**

YAML 示例如下，您可以按需修改相关参数值。

```
# Add additional labels to log
extraDataLabels:

extraEnvs: [ ]
#  - name: KEY_NAME
#    value: values

extraFileInput: []
#  - /opt/logs/*.log

extraVolumeMounts: [ ]
#  - mountPath: /opt/logs
#    name: hostlogs
#    readOnly: true
#  - mountPath: /etc/test
#    name: test
#    readOnly: true

extraVolumes: []
#  - name: hostlogs
#    hostPath:
#      path: /opt/logs
#      type: DirectoryOrCreate
#  - name: test
#    secret:
#      secretName: test
#      defaultMode: 420
extraArgs: [ ]

# Sending logs to external systems
extraSinks: {}
#  dump_k8s_to_file:
#    type: file
#    path: /tmp/dump-k8s-log-%Y-%m-%d.log
#    encoding:
#      codec: json
#    inputs:
#      - tf_kubernetes
#  my_sink_id:
#    encoding:
#      codec: json
#    type: loki
#    remove_label_fields: true
#    out_of_order_action: accept
#    labels:
#      "*": "{{ labels }}"
#    inputs:
#      - tf_kubernetes
#      - tf_os_logs
#    endpoint: http://example-loki-host

resources:
  requests:
    cpu: 10m
    memory: 200Mi
  limits:
    cpu: "1"
    memory: 512Mi
```

### 启用事件

您可以启用**事件**，以查看集群的事件信息。

启用后，您还可通过 YAML 配置 OBS-Event-Agent 参数。

**YAML 示例**

YAML 示例如下，您可以按需修改相关参数值。

```
agent:
 # Add additional labels to log
 extraDataLabels:
 # Sending logs to external systems
 extraSinks: { }
   #  my_sink_id:
   #    type: loki
   #    inputs:
   #      - tf_kubernetes
   #      - tf_os_logs
   #    endpoint: http://my-loki.example.com:3100
 extraEnvs: [ ]
 #  - name: KEY_NAME
 #    value: values

 extraVolumeMounts: [ ]
 #  - mountPath: /etc/test
 #    name: test
 #    readOnly: true

 extraVolumes: [ ]
 #  - name: test
 #    secret:
 #      secretName: test
 #      defaultMode: 420
 extraArgs: [ ]

 resources:
   requests:
     cpu: 5m
     memory: 100Mi
   limits:
     cpu: 500m
     memory: 256Mi
```

### 启用审计

您可以启用**审计**，以查看集群的审计信息。

- 启用后，您需要选择审计策略，以指定审计信息的详细程度。若选择**自定义策略**，您需要自行通过 YAML 配置审计策略。

  **YAML 示例**

  审计策略 YAML 示例如下，您可以按需修改相关参数值。

  ```
  apiVersion: audit.k8s.io/v1
  kind: Policy
  omitManagedFields: true
  rules:
  - level: None
    userGroups:
      # Don't log k8s internal operator on userGroups
      - system:nodes
      - system:serviceaccounts:kube-system
      # Do not log unauthenticated requests, and all responses are rejected.
      - system:unauthenticated
  - level: None
    users:
      # Don't log k8s internal operator on users
      - system:kube-scheduler
      - system:volume-scheduler
      - system:kube-controller-manager
      # Do not record the operations of the kapp/calico tigera-operator controller because they are too frequent and unnecessary
      - system:serviceaccount:sks-system:sks-packages-sa
      - system:serviceaccount:kapp-controller:kapp-controller-sa
      - system:serviceaccount:sks-system:tigera-operator
      - system:serviceaccount:sks-system-monitoring:prometheus-operator
  # Don't log requests to certain non-resource URL paths.
  - level: None
    nonResourceURLs:
      - "/api*" # Wildcard matching.
      - "/version"
      - "/healthz*"
      - "/swagger*"
      - "/ready*"
  # Do not record these built-in objects so generated too often
  - level: None
    resources:
      # Do not record leaks, they are used for controller election
      - group: coordination.k8s.io
        resources: [ "leases" ]
      - resources: [ "tokenreviews" ]
        group: "authentication.k8s.io"
      - group: "authorization.k8s.io"
  - level: Request
    resources:
      - group: apps
      - group: projectcontour.io
    verbs:
      - create
      - delete
      - deletecollection
      - patch
      - update
      - get
      - list
  ```
- 启用后，您还可以通过 YAML 配置 OBS-Audit-Agent 参数。

  **YAML 示例**

  ```
  # Add additional labels to log
  extraDataLabels:

  extraEnvs: [ ]
  #  - name: KEY_NAME
  #    value: values

  extraFileInput: []
  #  - /opt/logs/*.log

  extraVolumeMounts: [ ]
  #  - mountPath: /opt/logs
  #    name: hostlogs
  #    readOnly: true
  #  - mountPath: /etc/test
  #    name: test
  #    readOnly: true

  extraVolumes: []
  #  - name: hostlogs
  #    hostPath:
  #      path: /opt/logs
  #      type: DirectoryOrCreate
  #  - name: test
  #    secret:
  #      secretName: test
  #      defaultMode: 420
  extraArgs: [ ]

  # Sending logs to external systems
  extraSinks: {}
  #  dump_k8s_to_file:
  #    type: file
  #    path: /tmp/dump-k8s-log-%Y-%m-%d.log
  #    encoding:
  #      codec: json
  #    inputs:
  #      - tf_kubernetes
  #  my_sink_id:
  #    encoding:
  #      codec: json
  #    type: loki
  #    remove_label_fields: true
  #    out_of_order_action: accept
  #    labels:
  #      "*": "{{ labels }}"
  #    inputs:
  #      - tf_kubernetes
  #      - tf_os_logs
  #    endpoint: http://example-loki-host

  resources:
    requests:
      cpu: 10m
      memory: 200Mi
    limits:
      cpu: "1"
      memory: 512Mi
  ```

## 启用外部负载均衡器

外部负载均衡器用于为 LoadBalancer 类型的 Kubernetes Service 对象提供外部可访问的 IP 地址，并将外部流量转发到集群节点的正确端口上。

SKS 提供 MetalLB 插件作为外部负载均衡器，您可以按需启用 **MetalLB** 插件，并通过 UI 界面或 YAML 配置一个或多个 **IP 范围**。

> **注意**：
>
> - IP 范围需与 Kubernetes 集群的节点业务网卡所在的网络在同一网段，且未被使用。MetalLB 将从该范围内为负载均衡服务分配 IP 地址。
> - 添加多个 IP 范围时，多个 IP 范围之间的 IP 地址不能重合。
> - 由于 MetalLB 插件的 `avoidBuggyIPs` 参数默认为 `true`，以 `.0` 和 `.255` 结尾的 IP 地址将会被避免分配使用。

IP 范围输入格式支持 IP 段或 CIDR 块：

- IP 段：格式为 `<起始 IP> - <结束 IP>`，例如 `192.168.2.1-192.168.3.255`。仅需添加一个 IP 地址时，也需要使用 IP 段的格式，例如 `192.168.1.1-192.168.1.1`。
- CIDR 块：格式为 `IP 地址/子网掩码位数`，例如 `192.168.1.1/32`。

**YAML 示例**

YAML 示例如下，您可以按需修改 IP 范围。

```
layer2IPAddressPools:
  - 10.0.0.5/24
```

## 启用 Ingress 控制器

Ingress 是对集群中服务的外部访问进行管理的 API 对象，典型的访问方式是 HTTP。Ingress 可以提供负载均衡、SSL 终结和基于名称的虚拟托管。

SKS 提供的 Contour 插件作为 Ingress 控制器，您可以按需启用 [Contour](https://projectcontour.io/) 插件，并通过 YAML 调整插件的参数。

> **注意**：
>
> - 当 Service 类型为 LoadBalancer 时，Ingress 组件 IP 将从外部负载均衡器的 IP 范围中自动分配，使用前需要事先部署外部负载均衡器。您可以直接启用内置的 MetalLB 插件，也可按需安装其他外部负载均衡器。
> - 当工作负载集群使用 EIC 插件时，不支持配置 `externalTrafficPolicy` 属性。

**参数说明**

支持配置的参数如下表所示。

| 参数 | | | | 描述 |
| --- | --- | --- | --- | --- |
| envoy | resources | limits | cpu | CPU 限额，默认为 `500m`。 |
| memory | 内存限额，默认为 `256Mi`。 |
| requests | cpu | CPU 请求值，默认为 `10m`。 |
| memory | 内存请求值，默认为 `64Mi`。 |
| service | type | | 设置 Service 类型，可选 NodePort、​LoadBalancer。 |
| contour | resources | limits | cpu | CPU 限额，默认为 `500m`。 |
| memory | 内存限额，默认为 `256Mi`。 |
| requests | cpu | CPU 请求值，默认为 `10m`。 |
| memory | 内存请求值，默认为 `64Mi`。 |
| configInline | timeouts | request-timeout | | 设置 Ingress 请求的默认超时时间。 |

**YAML 示例**

YAML 示例如下，您可以按需修改相关参数值。

```
# 请确保节点具有充足的资源，否则将导致部署失败
envoy:
  service:
    type: LoadBalancer 
  resources:
    limits:
      cpu: 500m
      memory: 256Mi
    requests:
      cpu: 10m
      memory: 64Mi
contour:
  resources:
    limits:
      cpu: 500m
      memory: 256Mi
    requests:
      cpu: 10m
      memory: 64Mi
configInline: 
  timeouts:
    request-timeout: 60s
```

---

## 创建工作负载集群 > 创建物理机集群 > 配置基本信息

# 配置基本信息

1. 进入 CloudTower 的 **Kubernetes 服务**界面，在左侧导航栏中单击**工作负载集群**。
2. 单击 **+ 创建 > 创建物理机集群**，参考以下说明配置基本信息。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | 物理机集群在 API 层面的名称，一旦设定，不可修改。 |
   | 显示名称 | 物理机集群的显示名称，具有一定的业务语义，物理机集群创建完成后仍可在集群的管理界面右上角单击 **...** > **编辑集群显示名称**进行编辑。 |
   | Control Plane 节点位置 | 选择用于创建 Control Plane 节点的 SMTX OS 集群。  SMTX OS 集群需符合版本配套要求。  **说明**：  若选择的 SMTX OS 集群为启用双活特性的集群，则工作负载集群 Control Plane 节点虚拟机将默认部署在该双活集群的优先可用域，且高可用（HA）重建优先级为高。优先可用域资源不足时可在次级可用域中部署，不涉及仲裁节点。 |
   | Kubernetes 版本 | 为 Control Plane 节点选择节点模板，仅支持选择与所选 SMTX OS 集群的 CPU 架构一致且本 SKS 版本支持的节点模板。SKS 也将自动为 Worker 节点安装所选版本的 K8s 软件。  如您选择的版本未分发至所选的 SMTX OS 集群，请先按照界面提示[准备 Kubernetes 节点模板](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_08)，否则可能导致创建超时失败。 |
   | CNI | 选择物理机集群需要启用的 CNI 插件，仅支持选择 **Calico**。  插件详细介绍，请参见[集群插件](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_22)。 |
   | CSI | 根据实际规划选择为物理机集群启用 SMTX ZBS CSI 插件或暂不选择。  插件详细介绍，请参见[集群插件](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_22)。 |
   | 受信任容器镜像仓库（可选） | 为物理机集群配置一个或多个受信任的容器镜像仓库，使物理机集群能够从容器镜像仓库中拉取工作负载需要使用的容器镜像。  如果您已在 SKS 的**全局配置**中添加了受信任的容器镜像仓库，则默认显示已添加的受信任容器镜像仓库的信息，否则为空。具体操作请参见[配置受信任容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_93)。  您也可以单击 **+ 添加容器镜像仓库**，为该物理机集群配置受信任的容器镜像仓库。具体操作及注意事项请参见[管理受信任容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_65)。 |
   | 时区 | 物理机集群的时区，将会应用至物理机集群的虚拟机节点的所有组件和物理机节点的操作系统。默认选择为 SKS 服务配置的时区。 |
3. 单击**下一步**。

---

## 创建工作负载集群 > 创建物理机集群 > 配置节点

# 配置节点

## Control Plane 节点组

1. 设置节点组的名称。
2. 设置节点组中的节点数量。您可选择 **1**、**3** 或 **5**，为保证物理机集群 Control Plane 的高可用，建议选择 3 个或 5 个节点。
3. 配置节点组中每个节点的资源。

   | 参数 | 描述 |
   | --- | --- |
   | CPU | 节点组中每个节点的 CPU 分配量，默认为 4 vCPU，需至少分配 2 vCPU。 |
   | 内存 | 节点组中每个节点的内存分配量，默认为 8 GiB，需至少分配 6 GiB。 **注意**：若节点所在 SMTX OS 集群的服务器 CPU 架构为 AArch64，则需至少分配 10 GiB 内存，以免工作负载集群插件开启过多时内存不足。 |
   | 存储 | 节点组中每个节点的存储分配量，即节点对应虚拟机的磁盘分配容量，默认为 200 GiB 且不支持修改。 |
4. （可选）若节点组中的节点数大于 1，可选择启用**故障节点自动替换**。启用该功能后，当节点组中的故障节点的占比未超过设置的最大故障节点比例时，系统会自动删除故障节点并创建新的节点。

   若工作负载集群部署在启用双活特性的 SMTX OS 集群，则优先在优先可用域中新建节点；优先可用域资源不足时可在次级可用域中新建，优先可用域恢复后对应虚拟机不会自动切回。

   启用该功能需要设置以下参数：

   | 参数 | 描述 |
   | --- | --- |
   | 故障节点判定 | 判定节点故障的条件。需要勾选所需的条件，并设置时长阈值。 **注意：**  - 如果需要设置节点未就绪或未知状态持续时长阈值，为避免已经通过高可用（HA）恢复故障的虚拟机仍被识别为故障节点，部署在未启用双活特性的 SMTX OS 集群时建议设置的阈值不小于 5 分钟，部署在启用双活特性的 SMTX OS 集群时建议设置的阈值不小于 11 分钟，因为虚拟机高可用功能需要一定的故障恢复时间，节点恢复可用也需要一定的时间。 - 如果需要设置节点持续未启动时长阈值，为避免节点在启动完毕前即被识别为故障节点，部署在未启用双活特性的 SMTX OS 集群时建议设置的阈值不小于 5 分钟，部署在启用双活特性的 SMTX OS 集群时建议设置的阈值不小于 11 分钟。 |
   | 最大故障节点比例 | 节点组中允许被自动替换的故障节点数的最大比例，若故障节点数超过该比例，则不支持自动替换。需要设置一个不大于 40% 的百分数。假设节点组的总节点数为 5，此项设置为 40%，则当节点组中的故障节点小于或等于 2 个时会被自动替换，大于 2 个时不会被替换。 |

## Worker 节点组

您需要创建至少一个 Worker 节点组。

1. 设置节点组的名称。
2. 根据名称辨认并选择需要添加至节点组的物理机，系统将自动计算节点数。

   若物理机挂载了符合要求的 GPU 设备，在**物理机节点**下拉框中可查看 GPU 设备的型号和数量。

## 节点访问配置

您已在[添加物理机](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_10)阶段配置了 用于访问 Worker 节点的 SSH 账号信息，您还需要在此处配置用于访问 Control Plane 节点的默认账户密码或 SSH 公钥。

- **默认账户密码**：输入默认账户 `smartx` 的密码，留空代表不配置。您需要输入两次密码，以对密码进行确认。
- **SSH 公钥**：输入 SSH 公钥。可以手动输入或者从文件中提取，留空代表不配置。

---

## 创建工作负载集群 > 创建物理机集群 > 配置网络

# 配置网络

请根据规划的[工作负载集群的网络信息](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_18)，配置网络相关信息。

**操作步骤**

1. 配置 Control Plane 虚拟 IP。

   配置该虚拟 IP 后，即使 Control Plane 节点组中存在节点故障，只要在允许的故障范围内，即可通过该 IP 访问可用的 Control Plane 节点。

   有以下两种配置方式：

   - **IP 池自动分配**：选择根据规划[创建的工作负载集群 IP 池](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_12)，将从该 IP 池中自动分配一个 Control Plane 虚拟 IP 。
   - **手动输入**：输入规划的 Control Plane 虚拟 IP 地址。
2. 配置集群网络。请先单击**查看节点 IP**，确认已添加的物理机符合网络规划，再参考下表配置 Control Plane 节点的网卡。

   | 参数 | 描述 |
   | --- | --- |
   | 业务网卡 | 选择 Control Plane 节点的业务网卡使用的虚拟机网络，并根据在[业务网卡网络要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_19)中规划的信息配置 IP，有以下两种配置方式： - IP 池自动分配 - 启动网卡 DHCP |
   | SMTX ZBS CSI 专用网卡（仅当选择 SMTX ZBS CSI 插件时展示） | - 若规划物理机集群使用 Control Plane 节点所在 SMTX OS 集群的存储，请确保已[创建 SMTX ZBS CSI 接入配置](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_11)，创建完成后系统会自动填充网络和接入虚拟 IP 的信息，你只需要选择为 SMTX ZBS CSI 专用网卡创建的用于接入该 SMTX OS 集群的 IP 池。 **注意：**若该 SMTX ZBS CSI 接入配置是在 1.2.0 及之前版本的 SKS 服务上创建的（即含有 DHCP 配置），需要将自动填充的虚拟机网络修改为手动在 SMTX OS 存储网络所在虚拟分布式交换机上创建的虚拟机网络。 - 若规划物理机集群使用其他集群的存储，请根据实际规划选择 Control Plane 节点的 SMTX ZBS CSI 专用网卡使用的虚拟机网络，填写目标存储集群的接入虚拟 IP，并选择为 SMTX ZBS CSI 专用网卡创建的用于接入该目标存储集群的 IP 池。**注意：**接入虚拟 IP 在物理机集群创建完成后不支持修改。 |
3. 配置 Service IP CIDR 和 Pod IP CIDR，该网段不能与集群网络使用的网段重合、不能使用公网地址。不同的集群之间 Service IP CIDR、以及 Pod IP CIDR 可以使用相同网段。

   | 参数 | 描述 |
   | --- | --- |
   | Service IP CIDR | 输入一段用于 Service 使用的 IP 地址。 |
   | Pod IP CIDR | 输入一段用于 Pod 使用的 IP 地址。 |
4. 单击**下一步**。

---

## 创建工作负载集群 > 创建物理机集群 > 配置 K8s 集群

# 配置 K8s 集群

SKS 对 etcd、kube-apiserver、kube-controller-manager、kube-scheduler、kubelet 等 K8s 组件的默认配置可参考[默认参数说明](#%E9%BB%98%E8%AE%A4%E5%8F%82%E6%95%B0%E8%AF%B4%E6%98%8E)。出于稳定性考虑，在 UI 界面仅允许编辑这些组件的部分参数，除组件参数外，您还可配置节点文件、系统参数调优、命令执行等高级配置，配置格式可参考 [YAML 配置文件](#yaml-%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6)，各个配置字段的含义可参考[参数配置说明](#%E5%8F%82%E6%95%B0%E9%85%8D%E7%BD%AE%E8%AF%B4%E6%98%8E)。

- 如需编辑集群配置，请在**配置内容**中填写变更的参数配置，然后单击**下一步**。
- 如需编辑 UI 界面不支持的组件参数（界面会提示错误），请联系 SmartX 售后工程师进行处理。
- 如无需编辑参数，可将**配置内容**留空，直接单击**下一步**。

> **注意**：
>
> 若 K8s 组件参数配置错误，则可能导致物理机集群创建失败。如非必要需求，请勿随意编辑参数配置。

## 默认参数说明

SKS 默认配置的 K8s 组件参数及说明如下。

### etcd

| 参数 | 默认值 | 描述 |
| --- | --- | --- |
| cipher-suites | "TLS\_AES\_128\_GCM\_​SHA256,​TLS\_AES\_256\_GCM\_SHA384,​TLS\_CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_RSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_RSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_ECDSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_RSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_RSA\_WITH\_AES\_​128\_GCM\_SHA256,​TLS\_RSA\_WITH\_AES\_​256\_GCM\_SHA384" | etcd 服务器端的加密算法列表，以英文逗号分隔。如果不设置，则使用 Go 语言加密包的默认算法列表。 |

### kube-apiserver

| 参数 | 默认值 | 描述 |
| --- | --- | --- |
| profiling | "false" | 是否通过 Web 接口 host:port/debug/pprof/ 启用性能分析。默认值为 false，即不启用性能分析。 |
| audit-log-batch-buffer-size | "102400" | 批处理和写入事件之前用于缓存事件的缓冲区大小。 仅在批处理模式下使用。 |
| audit-log-batch-max-size | "10" | 每个批次的最大大小。仅在批处理模式下使用。 |
| audit-log-batch-max-wait | 5s | 强制写入尚未达到最大大小的批次之前要等待的时间。 仅在批处理模式下使用。 |
| audit-log-path | /var/log/apiserver/audit.log | 指定用于存储 kube-apiserver 审计日志文件的路径，所有到达 API 服务器的请求均记录在该文件中。 |
| audit-log-maxage | "7" | 根据文件名中编码的时间戳保留旧审计日志文件的最大天数。 |
| audit-log-maxbackup | "5" | 指定需要保留的旧审计日志文件的个数上限。该值设置为 0 时表示对文件个数无限制。 |
| audit-log-maxsize | "100" | 审计日志文件的最大大小，以兆字节为单位。当审计日志文件达到指定的最大大小后，会将当前的审计日志文件重命名并创建一个新的审计日志文件，以便继续记录。 |
| audit-log-mode | batch | 用于发送审计事件的策略。已知的模式包含批处理（batch）、阻塞（blocking）、严格阻塞（blocking-strict）。 阻塞（blocking）表示发送事件应阻止服务器响应；批处理（batch）会在后端引发异步缓冲和写入事件。 |
| audit-log-truncate-enabled | "true" | 是否启用事件和批次截断。 |
| enable-admission-plugins | EventRateLimit | 除了默认启用的插件之外需要启用的准入插件，以英文逗号分隔。  默认启用的插件包括：  NamespaceLifecycle,​LimitRanger,​ServiceAccount,​TaintNodesByCondition,​PodSecurity,​Priority,​DefaultTolerationSeconds,​DefaultStorageClass,​StorageObjectInUseProtection,​PersistentVolumeClaimResize,​RuntimeClass,​CertificateApproval,​CertificateSigning,​ClusterTrustBundleAttest,​CertificateSubjectRestriction,​DefaultIngressClass,​MutatingAdmissionWebhook,​ValidatingAdmissionPolicy,​ValidatingAdmissionWebhook,​ResourceQuota |
| admission-control-config-file | /etc/kubernetes/admission.yaml | 指定准入控制配置文件的路径。 |
| audit-policy-file | /etc/kubernetes/auditpolicy.yaml | 指定审计策略配置文件的路径。 |
| request-timeout | "300s" | 指定向 Kubernetes API 服务器发出请求时的默认超时时间。对于特定类型的请求，该值可能会被 `--min-request-timeout` 等标志覆盖。 |
| tls-min-version | "VersionTLS12" | kube-apiserver 支持的最小 TLS 版本。 |
| tls-cipher-suites | "TLS\_AES\_128\_GCM\_​SHA256,​TLS\_AES\_256\_GCM\_SHA384,​TLS\_CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_RSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_RSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_ECDSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_RSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_RSA\_WITH\_AES\_​128\_GCM\_SHA256,​TLS\_RSA\_WITH\_AES\_​256\_GCM\_SHA384" | 服务器端的加密算法列表，以英文逗号分隔。如果不设置，则使用 Go 语言加密包的默认算法列表。 |

### kube-controller-manager

| 参数 | 默认值 | 描述 |
| --- | --- | --- |
| profiling | "false" | 是否通过 Web 接口 host:port/debug/pprof/ 启用性能分析。默认值为 false，即不启用性能分析。 |
| terminated-pod-gc-threshold | "10" | 在已终止 Pod 垃圾收集器删除已终止 Pod 之前，可以保留的已终止 Pod 的个数上限。若此值小于等于 0，则相当于禁止垃圾回收已终止的 Pod。 |
| tls-min-version | "VersionTLS12" | kube-controller-manager 支持的最小 TLS 版本。 |
| tls-cipher-suites | "TLS\_AES\_128\_GCM\_​SHA256,​TLS\_AES\_256\_GCM\_SHA384,​TLS\_CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_RSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_RSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_ECDSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_RSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_RSA\_WITH\_AES\_​128\_GCM\_SHA256,​TLS\_RSA\_WITH\_AES\_​256\_GCM\_SHA384" | 服务器端的加密算法列表，以英文逗号分隔。如果不设置，则使用 Go 语言加密包的默认算法列表。 |

### kube-scheduler

| 参数 | 默认值 | 描述 |
| --- | --- | --- |
| profiling | "false" | 是否通过 Web 接口 host:port/debug/pprof/ 启用性能分析。默认值为 false，即不启用性能分析。 |
| tls-min-version | "VersionTLS12" | kube-scheduler 支持的最小 TLS 版本。 |
| tls-cipher-suites | "TLS\_AES\_128\_GCM\_​SHA256,​TLS\_AES\_256\_GCM\_SHA384,​TLS\_CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_RSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_RSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_ECDSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_RSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_RSA\_WITH\_AES\_​128\_GCM\_SHA256,​TLS\_RSA\_WITH\_AES\_​256\_GCM\_SHA384" | 服务器端的加密算法列表，以英文逗号分隔。如果不设置，则使用 Go 语言加密包的默认算法列表。 |

### kubelet

- **kubeletExtraArgs**

  | 参数 | 默认值 | 描述 |
  | --- | --- | --- |
  | protect-kernel-defaults | "true" | 设置为 true 表示强制使用 kubelet 的默认内核配置。当任何内核可调参数与 kubelet 默认值不同时，kubelet 都会报错。 |
  | event-qps | "0" | 限制每秒可生成的事件数量，设置为 0 表示不限制。 |
  | tls-min-version | "VersionTLS12" | kubelet 支持的最小 TLS 版本。 |
  | tls-cipher-suites | "TLS\_AES\_128\_GCM\_​SHA256,​TLS\_AES\_256\_GCM\_SHA384,​TLS\_CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_RSA\_WITH\_​AES\_128\_GCM\_SHA256,​TLS\_ECDHE\_ECDSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_RSA\_WITH\_​AES\_256\_GCM\_SHA384,​TLS\_ECDHE\_ECDSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_ECDHE\_RSA\_WITH\_​CHACHA20\_POLY1305\_​SHA256,​TLS\_RSA\_WITH\_AES\_​128\_GCM\_SHA256,​TLS\_RSA\_WITH\_AES\_​256\_GCM\_SHA384" | 服务器端的加密算法列表，以英文逗号分隔。如果不设置，则使用 Go 语言加密包的默认算法列表。 |
  | serialize-image-pulls | "false" | 设置为 true 表示 kubelet 每次仅拉取一个镜像。当前默认配置 `false`，即 kubelet 支持并发拉取多个镜像。 |
- **kubeletConfiguration**

  | 参数 | 默认值 | 描述 |
  | --- | --- | --- |
  | shutdownGracePeriod | 45s | 设置 Kubernetes 节点对应的虚拟机或物理机在正常关机时，Kubernetes 节点自身需要的延时以及为节点上运行的 Pod 提供的终止宽限期总时长。 |
  | shutdownGracePeriod​CriticalPods | 30s | 设置 Kubernetes 节点对应的虚拟机或物理机在正常关机时，Kubernetes 节点提供给关键性 Pod 的终止宽限期总时长。此时长要短于 shutdownGracePeriod。  例如：shutdownGracePeriod = 30s，​shutdownGracePeriod​CriticalPods = 10s。​Kubernetes 节点对应的虚拟机或物理机在正常关机时，kubelet 先进行普通 Pod 的优雅退出，预留给普通 Pod 的终止宽限期为 shutdownGracePeriod - shutdownGracePeriod​CriticalPods = 20s，​之后进行关键性 Pod 的优雅退出，预留给系统关键性 Pod 的终止宽限期为 10s。 |

## YAML 配置文件

YAML 配置文件示例如下。以下配置均为 SKS 的默认配置，您可按需粘贴参数至**配置内容**框中修改。

```
controlPlane:
  clusterConfiguration:
    # Refer to https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/
    apiServer:
      extraArgs:
        audit-log-maxage: '7'
        audit-log-maxbackup: '5'
        audit-log-maxsize: '100'
        request-timeout: 300s
      extraVolumes:
        - hostPath: /var/log/apiserver
          mountPath: /var/log/apiserver
          name: apiserver-log
          pathType: DirectoryOrCreate
        - hostPath: /etc/kubernetes/admission.yaml
          mountPath: /etc/kubernetes/admission.yaml
          name: admission-config
          pathType: FileOrCreate
          readOnly: true
        - hostPath: /etc/kubernetes/auditpolicy.yaml
          mountPath: /etc/kubernetes/auditpolicy.yaml
          name: audit-policy
          pathType: FileOrCreate
          readOnly: true
    controllerManager:
      # Refer to https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/
      extraArgs:
        terminated-pod-gc-threshold: '10'
    etcd:
      local:
        # Refer to https://etcd.io/docs/v3.5/op-guide/configuration/#command-line-flags
        extraArgs: {}
    scheduler:
      # Refer to https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/
      extraArgs: {}
  files:
    - content: |
        apiVersion: apiserver.config.k8s.io/v1
        kind: AdmissionConfiguration
        plugins:
          - name: EventRateLimit
            configuration:
              apiVersion: eventratelimit.admission.k8s.io/v1alpha1
              kind: Configuration
              limits:
                - type: Server
                  burst: 20000
                  qps: 5000
      owner: root:root
      path: /etc/kubernetes/admission.yaml
    - content: |
        apiVersion: audit.k8s.io/v1
        kind: Policy
        metadata:
          creationTimestamp: null
        omitManagedFields: true
        omitStages:
        - RequestReceived
        - ResponseStarted
        rules:
        - level: None
          userGroups:
          - system:nodes
          - system:serviceaccounts:kube-system
          - system:unauthenticated
        - level: None
          users:
          - system:kube-scheduler
          - system:volume-scheduler
          - system:kube-controller-manager
          - system:serviceaccount:sks-system:sks-packages-sa
          - system:serviceaccount:kapp-controller:kapp-controller-sa
          - system:serviceaccount:sks-system:tigera-operator
          - system:serviceaccount:sks-system-monitoring:prometheus-operator
        - level: None
          nonResourceURLs:
          - /api*
          - /version
          - /healthz*
          - /swagger*
          - /ready*
        - level: None
          resources:
          - group: coordination.k8s.io
            resources:
            - leases
          - group: authentication.k8s.io
            resources:
            - tokenreviews
          - group: authorization.k8s.io
        - level: Metadata
          verbs:
          - create
          - delete
          - deletecollection
          - patch
          - update
      owner: root:root
      path: /etc/kubernetes/auditpolicy.yaml
      permissions: '0644'
  initConfiguration:
    nodeRegistration:
      kubeletExtraArgs:
        event-qps: '0'
  joinConfiguration:
    nodeRegistration:
      kubeletExtraArgs:
        event-qps: '0'
  preKubeadmCommands: []
  postKubeadmCommands: []
  nodeIdempotentCommands: []
  sysctlParams: {}
workers:
  joinConfiguration:
    nodeRegistration:
      kubeletExtraArgs:
        event-qps: "0"
  preKubeadmCommands: []
  postKubeadmCommands: []
  nodeIdempotentCommands: []
  sysctlParams: {}
  files: []
# kubeletConfiguration is a patch for the KubeletConfiguration to modify the default or current values in the global kubelet-config ConfigMap of the cluster.
kubeletConfiguration:
  shutdownGracePeriod: 45s
  shutdownGracePeriodCriticalPods: 30s
```

## 参数配置说明

### KubernetesConfiguration

KubernetesConfiguration 定义了 Kubernetes 集群的参数配置，是当前 UI 中 **K8s 集群配置**的顶层结构。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `controlPlane` （可选） | [RoleConfiguration](#roleconfiguration) | Control Plane 节点的配置 |
| `workers` （可选） | [RoleConfiguration](#roleconfiguration) | Worker 节点的配置 |
| `kubeletConfiguration` （可选） | runtime.RawExtension | [Kubelet 配置文件](https://kubernetes.io/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/)，YAML 格式，以 patch 形式作用于集群 |

### RoleConfiguration

RoleConfiguration 指定了 Kubernetes 集群中特定角色的配置，部分字段只生效于特定角色。

> **注意**：
>
> 默认情况下，Control Plane 节点的 `initConfiguration`、`joinConfiguration` 以及 Worker 节点的 `joinConfiguration` 三处配置相同，在 UI 中仅修改 `initConfiguration` 时，系统会自动将修改同步至其余两处配置。若需避免系统同步修改，可以在 UI 中以声明式方式填写两处 `joinConfiguration` 的配置。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `clusterConfiguration` （可选） | [ClusterConfiguration](#clusterconfiguration) | 集群级别的配置，主要包含 `controlPlane` 组件的配置，只在 `controlPlane` 中生效 |
| `initConfiguration` （可选） | [InitConfiguration](#initconfiguration) | kubeadm init 配置，作用于第一个 Control Plane 节点，用于设置 kubelet 的启动参数，只在 `controlPlane` 中生效 |
| `joinConfiguration` （可选） | [JoinConfiguration](#joinconfiguration) | kubeadm join 配置，作用于后续的 Control Plane 节点及 Worker 节点 |
| `files` （可选） | [[]File](#file) | 需要在节点上创建的文件列表 |
| `preKubeadmCommands` （可选） | []string | 在节点创建时 kubeadm 运行前执行的命令，节点创建后不再执行 |
| `postKubeadmCommands` （可选） | []string | 在节点创建时 kubeadm 运行后执行的命令，节点创建后不再执行 |
| `sysctlParams` （可选） | map[string]string | 在节点上设置的 sysctl 参数 |
| `nodeIdempotentCommands` （可选） | []string | 可以在节点上运行的命令，会在节点创建后及原地更新中被执行，由于会多次执行，请保证命令的幂等性 |

### ClusterConfiguration

ClusterConfiguration 包含集群范围的 kubeadm 集群配置。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `etcd` （可选） | [Etcd](#etcd-1) | Etcd 配置 |
| `apiServer` （可选） | [ControlPlaneComponent](#controlplanecomponent) | API Server 配置 |
| `controllerManager` （可选） | [ControlPlaneComponent](#controlplanecomponent) | Controller Manager 配置 |
| `scheduler` （可选） | [ControlPlaneComponent](#controlplanecomponent) | Scheduler 配置 |

### Etcd

Etcd 包含 Etcd 配置的元素。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `local` （可选） | [LocalEtcd](#localetcd) | 本地 Etcd 集群配置 |

### LocalEtcd

LocalEtcd 描述 kubeadm 应该在本地运行 Etcd 集群。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `extraArgs` （可选） | map[string]string | Etcd 的额外命令行参数 |

### ControlPlaneComponent

ControlPlaneComponent 包含控制平面组件通用的设置。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `extraArgs` （可选） | map[string]string | 控制平面组件的额外命令行参数 |
| `extraVolumes` （可选） | [[]HostPathMount](#hostpathmount) | 控制平面组件的额外卷挂载 |

### HostPathMount

HostPathMount 包含描述从主机挂载的卷的元素。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `name` （必需） | string | 卷的名称 |
| `hostPath` （必需） | string | 主机上的路径 |
| `mountPath` （必需） | string | 容器内的挂载路径 |
| `readOnly` （可选） | bool | 是否以只读模式挂载 |
| `pathType` （可选） | string | 主机路径的类型 |

### InitConfiguration

InitConfiguration 是特定于 "kubeadm init" 的配置。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `nodeRegistration` （可选） | [NodeRegistrationOptions](#noderegistrationoptions) | 与节点注册相关的字段 |

### JoinConfiguration

JoinConfiguration 是特定于 "kubeadm join" 的配置。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `nodeRegistration` （可选） | [NodeRegistrationOptions](#noderegistrationoptions) | 与节点注册相关的字段 |

### NodeRegistrationOptions

NodeRegistrationOptions 包含节点注册相关的字段。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `kubeletExtraArgs` （可选） | map[string]string | Kubelet 的额外命令行参数 |

### File

File 定义了在节点中生成文件所需的输入字段。

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `path` （必需） | string | 指定存储文件的磁盘完整路径 |
| `owner` （可选） | string | 指定文件的所有权，例如 `root:root` |
| `permissions` （可选） | string | 指定分配给文件的权限，例如 `'0640'` |
| `encoding` （可选） | string | 指定文件内容的编码，可选值：`base64`，`gzip`，`gzip+base64` |
| `append` （可选） | bool | 指定当路径已存在时，是否将内容追加到现有文件。若不追加，新内容将覆盖原有内容 |
| `content` （可选） | string | 文件的实际内容 |

---

## 创建工作负载集群 > 创建物理机集群 > 配置集群插件

# 配置集群插件

创建物理机集群时，您可以修改 Calico CNI、SMTX ZBS CSI 和 GPU 插件的默认参数；也可以根据业务需求启用**可观测性**、**日志**、**外部负载均衡器**和 **Ingress 控制器**相关插件，并配置相关插件参数。

配置完成后单击**创建**，即可开始创建物理机集群。

## 配置 Calico CNI

您可以通过 UI 界面或 YAML 配置 [Calico CNI](https://docs.tigera.io/calico/latest/about) 插件。

该插件仅在创建物理机集群时支持修改参数配置，创建完成后不可通过 UI 界面修改。

- **通过 UI 界面配置**

  1. 选择**网络封装方式**

     - **None**：无封装模式，即容器之间的通信不进行封装，直接使用标准的 IP 路由进行通信。
     - **IPIP**：使用 IP-in-IP 封装模式，将容器的 IP 数据包封装在另一个 IP 数据包中，实现容器之间的跨节点通信。
     - **IPIPCrossSubnet**：当容器之间的通信需要跨子网时，使用 IP-in-IP 封装模式，将容器的 IP 数据包封装在另一个 IP 数据包中，实现容器之间的跨节点通信。其他情况直接使用标准的 IP 路由进行通信。
     - **VXLAN**：使用 VXLAN 封装模式，将容器的 IP 数据包封装在 UDP 数据包中，实现容器之间的跨节点通信。
     - **VXLANCrossSubnet**：当容器之间的通信需要跨子网时，使用 VXLAN 封装模式，将容器的 IP 数据包封装在 UDP 数据包中，实现容器之间的跨节点通信。其他情况直接使用标准的 IP 路由进行通信。
  2. 设置是否**启用 BGP**。

     - 当**网络封装方式**为 **IPIPCrossSubnet**、**None** 或 **IPIP** 时，默认启用 BGP，不可修改。
     - 当**网络封装方式**为 **VXLAN** 或 **VXLANCrossSubnet** 时，默认不启用 BGP，不可修改。
- **通过 YAML 配置**

  YAML 示例如下，您可以按需修改 `encapsulation` 和 `cidr` 参数。

  ```
  installation:
    calicoNetwork:
      bgp: Enabled # 指定是否启用 BGP，不允许修改
      ipPools:    # 仅支持配置一个 IP 池
        - encapsulation: IPIP  # 指定网络封装方式
          cidr: 172.16.0.0/16   # 指定 IP Pool 的 CIDR，需在 Pod IP CIDR 的地址范围内；该范围不能与集群使用的网络重合，且不能使用公网地址，不同的集群之间可以使用相同网段。
  ```

## 配置 SMTX ZBS CSI

当您在**基本信息**界面选择了 SMTX ZBS CSI 插件时，将默认开启该插件，不支持关闭，您可以通过 YAML 配置 SMTX ZBS CSI 插件。

**参数说明**

支持配置的参数如下表所示。

| 参数 | | | 描述 |
| --- | --- | --- | --- |
| driver | | maxVolumesPerNode | 单节点可挂载的 PV 的最大数量，默认为 `128`。 |
| controller.driver.​podDeletePolicy | 当挂载了由 SMTX ZBS CSI 插件创建的 PVC 的 Pod 所在的 Worker 节点发生故障时，是否自动删除该 Pod 并在其他健康的 Worker 节点重建，默认为 `no-delete-pod`，还支持配置为 `delete-deployment-pod`、`delete-statefulset-pod`、`delete-both-statefulset-and-deployment-pod`。 |
| storageClass | parameters | csi.storage.k8s.io/fstype | 使用默认创建的 StorageClass 制备的 PV 的文件系统类型，默认为 `ext4`，还支持配置为 `xfs`。 |
| replicaFactor | - 工作负载集群部署在未启用双活特性的 SMTX OS 集群时，使用默认创建的 StorageClass 制备的 PV 的副本数默认为 `2`，还支持配置为 `3`。 - 工作负载集群部署在启用双活特性的 SMTX OS 集群时，使用默认创建的 StorageClass 制备的 PV 的副本数默认为 `3`。   **注意**：若工作负载集群部署在未启用双活特性的 SMTX OS 集群，但 SMTX ZBS CSI 对接的外部存储集群为双活集群，需要手动更新副本数为 3，以确保监控插件可用。 |
| thinProvision | 使用默认创建的 StorageClass 制备的 PV 的置备类型，默认为 `true`（精简置备），还支持配置为 `false`（厚置备）。 |

**YAML 示例**

```
driver:
  maxVolumesPerNode: 128
    controller:
      driver:
        podDeletePolicy: delete-deployment-pod
storageClass:
  parameters:
    csi.storage.k8s.io/fstype: "ext4"
    replicaFactor: "2"
    thinProvision: "true"
```

## 配置 GPU

**NVIDIA GPU Operator** 插件的配置项默认关闭。当您在**节点配置**界面为任一 Worker 节点组选择了挂载 GPU 设备的物理机时，如果需要使用 GPU 设备，请开启该插件，您还可通过 YAML 配置该插件的参数，如果在此处不配置，也可以在集群创建成功后再进行配置。

> **注意**：
>
> 若物理机节点使用的操作系统不是 Rocky Linux 8.10，则无法成功开启该插件，您需要自行管理 GPU 资源。

**参数说明**

支持配置的参数如下表所示。

| 参数 | | 描述 |
| --- | --- | --- |
| devicePlugin | config | 启用集群的 TimeSlicing 功能的配置，详细配置可参考 YAML 示例。  **风险提示：**  启用 TimeSlicing 功能后，单个 GPU 设备可以同时分配给多个 Pod 使用，如果同时启用监控插件，GPU 监控采集器将无法识别正在使用 GPU 资源的 Pod，导致无法查看依赖于 Pod 标签的监控视图下的 GPU 图表。 |

**YAML 示例**

YAML 示例如下，您可以按需修改相关参数值。

```
devicePlugin:
  config:
    create: true
    name: time-slicing
    default: any
    data:
      any: |-
        sharing:
          timeSlicing:
            resources:
            - name: nvidia.com/gpu
              replicas: 4
```

## 配置可观测性

建议您为物理机集群关联可观测性服务，以便启用监控、报警、日志、事件、审计功能。

> **注意**：
>
> 为集群关联可观测性服务前，请确保集群节点的业务网卡所在网络、可观测性服务虚拟机的虚拟网卡所在虚拟机网络两者之间三层互通，并且建议先[为 SKS 系统服务关联可观测性服务](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_109)。

### 关联可观测性服务

启用**关联可观测性服务**，然后选择需要关联的可观测性服务。

### 启用监控

当您在**基本信息**界面选择了 SMTX ZBS CSI 插件时，集群中将配置默认存储类，您可以在关联可观测性服务后启用**监控**，以便查看集群的监控信息。

启用后，您还可通过 YAML 配置 OBS-Monitoring-Agent 和 Prometheus 参数。

**配置 OBS-Monitoring-Agent 参数**

- **参数说明**

  | 参数 | | | 描述 |
  | --- | --- | --- | --- |
  | metrics | remote\_write\_global | labels | 自定义键值对，为发送到外部系统的 metrics 添加特定标签，通常用于标识数据源。默认不配置。 |
  | remote\_write | url | 接收监控数据的目标地址，默认不配置。 |
  | tls\_insecure\_skip\_​verify | 是否跳过 TLS 证书的验证，默认为 `false`。 **注意：**如果 URL 使用 HTTPS 协议并且证书为自签名，则需设置为 `true`。 |
  | send\_timeout | 发送请求时的超时时间，默认为 `1m`。 |
  | headers | HTTP 请求头，默认不配置。 |
  | bearer\_auth.token | 用于 Bearer 认证的 token，默认不配置。 |
  | basic\_auth.username | BasicAuth 用户名，默认不配置。 |
  | basic\_auth.password | BasicAuth 密码，默认不配置。 |
  | resources | requests | cpu | CPU 请求值，默认为 `250m`。 |
  | memory | 内存请求值，默认为 `300Mi`。 |
  | limits | cpu | CPU 限额，默认为 `"2"`。 |
- **YAML 示例**

  ```
  agent:
    # 用于将 metrics 发送到外部系统
    metrics:
      remote_write_global:
        labels:
          # 为发送到远端的 metrics 添加特定 label，通常可用于标识数据源
          # 非必填
          source: sks-monitor
          my_key: my_value
      remote_write:
      - url: https://remote-prometheus.example.com/api/v1/write
        tls_insecure_skip_verify: true
        send_timeout: 30s
        # 多种认证方式，根据需要选择，无认证则不需要

        # 直接在 header 中插入字段
        headers:
          Authorization: 'Bearer eyJhbGciOiJ...'

        bearer_auth:
          token: 'eyJhbGciOiJ...'

        basic_auth:
          username: remote
          password: my_secret

    # 调整 agent 资源配置
    resources:
      requests:
        cpu: 250m
        memory: 300Mi
      limits:
        cpu: "2"
  ```

**配置 Prometheus 参数**

- **参数说明**

  | 参数 | | | | 描述 |
  | --- | --- | --- | --- | --- |
  | grafana | resources | limits | cpu | CPU 限额，默认为 `500m`。 |
  | memory | 内存限额，默认为 `300Mi`。 |
  | requests | cpu | CPU 请求值，默认为 `10m`。 |
  | memory | 内存请求值，默认为 `100Mi`。 |
  | persistent | enable | | 是否启用持久化存储，默认为 `true`。 |
  | storageClassName | | 持久化存储使用的存储类名称。 |
  | accessModes | | 持久卷的访问方式，默认为 `ReadWriteOnce`。 |
  | size | | 持久卷的大小，默认为 `1Gi`。 |
  | config | [auth.​anonymous] | enabled | 是否开启匿名登录，默认为 `true`。 |
  | [security] | admin\_password | 指定 Grafana Web UI 的 admin 账号的密码，默认值请参见 [Grafana 官方文档](https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/)。 |
  | prometheus | scrapeInterval | | | 从目标抓取度量数据的时间间隔，默认为 `30s`。 |
  | scrapeTimeout | | | 单次抓取的最大超时时间，默认为 `10s`。 |
  | prometheus​Overrides | monitorExtraNamespaces | | | 指定 SKS 定义的 namespace 之外的名字空间列表，以便从这些名字空间中抓取 prometheus CR 资源，例如自定义 namespace 中的 serviceMonitor。默认不配置。 |
- **YAML 示例**

  YAML 示例如下，您可以按需修改相关参数值。

  ```
  grafana:
    persistent:
      size: 1Gi
    config: |
      [security]
      admin_password = ***  # 指定 Grafana Web UI 的 admin 账号的密码
      [auth.anonymous]
      enabled = true
      [date_formats]
      default_timezone = Asia/Shanghai
      use_browser_locale = true
      default_timezone = browser
      [dashboards]
      # Path to the default home dashboard. If this value is empty, then Grafana uses StaticRootPath + "dashboards/home.json"
      default_home_dashboard_path = /grafana-dashboard-definitions/0/k8s-resources-cluster/k8s-resources-cluster.json

  prometheus:
      scrapeInterval: 30s
      scrapeTimeout: 10s

  prometheusOverrides:
    monitorExtraNamespaces:
      - my-ns1
      - my-ns2
  ```

### 启用报警

当**监控**已启用时，您可以启用**报警**。

启用后，您不仅可以查看报警信息，还可以在 CloudTower 的**报警**主界面查看和编辑报警规则、以及配置报警通知。

### 启用日志

您可以启用**日志**，以查看集群的日志信息。

启用后，您还可通过 YAML 配置 OBS-Logging-Agent 参数。

**YAML 示例**

YAML 示例如下，您可以按需修改相关参数值。

```
# Add additional labels to log
extraDataLabels:

extraEnvs: [ ]
#  - name: KEY_NAME
#    value: values

extraFileInput: []
#  - /opt/logs/*.log

extraVolumeMounts: [ ]
#  - mountPath: /opt/logs
#    name: hostlogs
#    readOnly: true
#  - mountPath: /etc/test
#    name: test
#    readOnly: true

extraVolumes: []
#  - name: hostlogs
#    hostPath:
#      path: /opt/logs
#      type: DirectoryOrCreate
#  - name: test
#    secret:
#      secretName: test
#      defaultMode: 420
extraArgs: [ ]

# Sending logs to external systems
extraSinks: {}
#  dump_k8s_to_file:
#    type: file
#    path: /tmp/dump-k8s-log-%Y-%m-%d.log
#    encoding:
#      codec: json
#    inputs:
#      - tf_kubernetes
#  my_sink_id:
#    encoding:
#      codec: json
#    type: loki
#    remove_label_fields: true
#    out_of_order_action: accept
#    labels:
#      "*": "{{ labels }}"
#    inputs:
#      - tf_kubernetes
#      - tf_os_logs
#    endpoint: http://example-loki-host

resources:
  requests:
    cpu: 10m
    memory: 200Mi
  limits:
    cpu: "1"
    memory: 512Mi
```

### 启用事件

您可以启用**事件**，以查看集群的事件信息。

启用后，您还可通过 YAML 配置 OBS-Event-Agent 参数。

**YAML 示例**

YAML 示例如下，您可以按需修改相关参数值。

```
agent:
 # Add additional labels to log
 extraDataLabels:
 # Sending logs to external systems
 extraSinks: { }
   #  my_sink_id:
   #    type: loki
   #    inputs:
   #      - tf_kubernetes
   #      - tf_os_logs
   #    endpoint: http://my-loki.example.com:3100
 extraEnvs: [ ]
 #  - name: KEY_NAME
 #    value: values

 extraVolumeMounts: [ ]
 #  - mountPath: /etc/test
 #    name: test
 #    readOnly: true

 extraVolumes: [ ]
 #  - name: test
 #    secret:
 #      secretName: test
 #      defaultMode: 420
 extraArgs: [ ]

 resources:
   requests:
     cpu: 5m
     memory: 100Mi
   limits:
     cpu: 500m
     memory: 256Mi
```

### 启用审计

您可以启用**审计**，以查看集群的审计信息。

- 启用后，您需要选择审计策略，以指定审计信息的详细程度。若选择**自定义策略**，您需要自行通过 YAML 配置审计策略。

  **YAML 示例**

  审计策略 YAML 示例如下，您可以按需修改相关参数值。

  ```
  apiVersion: audit.k8s.io/v1
  kind: Policy
  omitManagedFields: true
  rules:
  - level: None
    userGroups:
      # Don't log k8s internal operator on userGroups
      - system:nodes
      - system:serviceaccounts:kube-system
      # Do not log unauthenticated requests, and all responses are rejected.
      - system:unauthenticated
  - level: None
    users:
      # Don't log k8s internal operator on users
      - system:kube-scheduler
      - system:volume-scheduler
      - system:kube-controller-manager
      # Do not record the operations of the kapp/calico tigera-operator controller because they are too frequent and unnecessary
      - system:serviceaccount:sks-system:sks-packages-sa
      - system:serviceaccount:kapp-controller:kapp-controller-sa
      - system:serviceaccount:sks-system:tigera-operator
      - system:serviceaccount:sks-system-monitoring:prometheus-operator
  # Don't log requests to certain non-resource URL paths.
  - level: None
    nonResourceURLs:
      - "/api*" # Wildcard matching.
      - "/version"
      - "/healthz*"
      - "/swagger*"
      - "/ready*"
  # Do not record these built-in objects so generated too often
  - level: None
    resources:
      # Do not record leaks, they are used for controller election
      - group: coordination.k8s.io
        resources: [ "leases" ]
      - resources: [ "tokenreviews" ]
        group: "authentication.k8s.io"
      - group: "authorization.k8s.io"
  - level: Request
    resources:
      - group: apps
      - group: projectcontour.io
    verbs:
      - create
      - delete
      - deletecollection
      - patch
      - update
      - get
      - list
  ```
- 启用后，您还可以通过 YAML 配置 OBS-Audit-Agent 参数。

  **YAML 示例**

  ```
  # Add additional labels to log
  extraDataLabels:

  extraEnvs: [ ]
  #  - name: KEY_NAME
  #    value: values

  extraFileInput: []
  #  - /opt/logs/*.log

  extraVolumeMounts: [ ]
  #  - mountPath: /opt/logs
  #    name: hostlogs
  #    readOnly: true
  #  - mountPath: /etc/test
  #    name: test
  #    readOnly: true

  extraVolumes: []
  #  - name: hostlogs
  #    hostPath:
  #      path: /opt/logs
  #      type: DirectoryOrCreate
  #  - name: test
  #    secret:
  #      secretName: test
  #      defaultMode: 420
  extraArgs: [ ]

  # Sending logs to external systems
  extraSinks: {}
  #  dump_k8s_to_file:
  #    type: file
  #    path: /tmp/dump-k8s-log-%Y-%m-%d.log
  #    encoding:
  #      codec: json
  #    inputs:
  #      - tf_kubernetes
  #  my_sink_id:
  #    encoding:
  #      codec: json
  #    type: loki
  #    remove_label_fields: true
  #    out_of_order_action: accept
  #    labels:
  #      "*": "{{ labels }}"
  #    inputs:
  #      - tf_kubernetes
  #      - tf_os_logs
  #    endpoint: http://example-loki-host

  resources:
    requests:
      cpu: 10m
      memory: 200Mi
    limits:
      cpu: "1"
      memory: 512Mi
  ```

## 启用外部负载均衡器

外部负载均衡器用于为 LoadBalancer 类型的 Kubernetes Service 对象提供外部可访问的 IP 地址，并将外部流量转发到集群节点的正确端口上。

SKS 提供 MetalLB 插件作为外部负载均衡器，您可以按需启用 **MetalLB** 插件，并通过 UI 界面或 YAML 配置一个或多个 **IP 范围**。

> **注意**：
>
> - IP 范围需与 Kubernetes 集群的节点业务网卡所在的网络在同一网段，且未被使用。MetalLB 将从该范围内为负载均衡服务分配 IP 地址。
> - 添加多个 IP 范围时，多个 IP 范围之间的 IP 地址不能重合。
> - 由于 MetalLB 插件的 `avoidBuggyIPs` 参数默认为 `true`，以 `.0` 和 `.255` 结尾的 IP 地址将会被避免分配使用。

IP 范围输入格式支持 IP 段或 CIDR 块：

- IP 段：格式为 `<起始 IP> - <结束 IP>`，例如 `192.168.2.1-192.168.3.255`。仅需添加一个 IP 地址时，也需要使用 IP 段的格式，例如 `192.168.1.1-192.168.1.1`。
- CIDR 块：格式为 `IP 地址/子网掩码位数`，例如 `192.168.1.1/32`。

**YAML 示例**

YAML 示例如下，您可以按需修改 IP 范围。

```
layer2IPAddressPools:
  - 10.0.0.5/24
```

## 启用 Ingress 控制器

Ingress 是对集群中服务的外部访问进行管理的 API 对象，典型的访问方式是 HTTP。Ingress 可以提供负载均衡、SSL 终结和基于名称的虚拟托管。

SKS 提供的 Contour 插件作为 Ingress 控制器，您可以按需启用 [Contour](https://projectcontour.io/) 插件，并通过 YAML 调整插件的参数。

> **注意**：
>
> 当 Service 类型为 LoadBalancer 时，Ingress 组件 IP 将从外部负载均衡器的 IP 范围中自动分配，使用前需要事先部署外部负载均衡器。您可以直接启用内置的 MetalLB 插件，也可按需安装其他外部负载均衡器。

**参数说明**

支持配置的参数如下表所示。

| 参数 | | | | 描述 |
| --- | --- | --- | --- | --- |
| envoy | resources | limits | cpu | CPU 限额，默认为 `500m`。 |
| memory | 内存限额，默认为 `256Mi`。 |
| requests | cpu | CPU 请求值，默认为 `10m`。 |
| memory | 内存请求值，默认为 `64Mi`。 |
| service | type | | 设置 Service 类型，可选 NodePort、​LoadBalancer。 |
| contour | resources | limits | cpu | CPU 限额，默认为 `500m`。 |
| memory | 内存限额，默认为 `256Mi`。 |
| requests | cpu | CPU 请求值，默认为 `10m`。 |
| memory | 内存请求值，默认为 `64Mi`。 |
| configInline | timeouts | request-timeout | | 设置 Ingress 请求的默认超时时间。 |

**YAML 示例**

YAML 示例如下，您可以按需修改相关参数值。

```
# 请确保节点具有充足的资源，否则将导致部署失败
envoy:
  service:
    type: LoadBalancer 
  resources:
    limits:
      cpu: 500m
      memory: 256Mi
    requests:
      cpu: 10m
      memory: 64Mi
contour:
  resources:
    limits:
      cpu: 500m
      memory: 256Mi
    requests:
      cpu: 10m
      memory: 64Mi
configInline: 
  timeouts:
    request-timeout: 60s
```

---

## 管理工作负载集群

# 管理工作负载集群

创建工作负载集群后，您可以进行查看工作负载集群信息、下载 Kubeconfig 文件、编辑 K8s 集群配置、管理节点、管理工作负载等操作。

> **注意**：
>
> - 工作负载集群的 Control Plane 证书存放于 Control Plane 节点，由每个节点独立维护。证书默认有效期为 1 年，过期后工作负载集群将不再可用。
> - 系统从 Control Plane 节点创建之日起开始计算证书的有效期，当 Control Plane 证书距离过期时间剩余 30 天时，系统自动触发证书更新操作，Control Plane 节点将依次进行滚动更新以更新证书，请确保工作负载集群 IP 池中存在未被使用的 IP。更新证书期间可能会导致大约 15 秒无法连接至工作负载集群，若希望避免此影响，可参考以下任一方法操作：
>   - 当 Control Plane 证书距离过期时间大于 30 天时，选择合适时机手动替换所有 Control Plane 节点以更新证书。
>   - 每年定期升级工作负载集群，以重建 Control Plane 节点，刷新 Control Plane 证书过期时间。

---

## 管理工作负载集群 > 查看工作负载集群信息

# 查看工作负载集群信息

1. 在左侧导航栏单击**工作负载集群**，可在列表中查看当前所有工作负载集群的信息。其中，**状态**一列展示工作负载集群的当前状态，具体如下表所示。

   | 状态 | 描述 |
   | --- | --- |
   | 创建中 | 工作负载集群正在创建。 |
   | 运行中 | 工作负载集群中的所有节点已就绪，但已开启的集群插件没有全部就绪。 |
   | 就绪 | 工作负载集群中的所有节点和已开启的集群插件均已就绪，集群已达到可以正常服务的状态。 |
   | 更新中 | 工作负载集群正在更新至配置修改后的状态。  可能导致更新的操作有升级 SKS 服务版本、创建节点组、删除节点组、编辑节点组中的节点数量、替换节点、系统自动伸缩节点数量。 |
   | 升级中 | 工作负载集群正在升级。 |
   | 暂停同步中 | 工作负载集群已暂停同步。  暂停同步后，即使 Kubernetes 集群的当前运行状态与期望状态不符，也不会主动更新。 |
   | 异常 | 工作负载集群出现异常，可能无法正常运行。  可能导致异常的原因包括`创建失败`、`升级失败`、`更新失败`、`集群插件状态异常`等。 |
   | 删除中 | 工作负载集群正在删除，相关数据正在被清除。 |
   | 回滚中 | 工作负载集群正在回滚到升级前的状态。 |

   > **说明**：
   >
   > 当工作负载集群已配置 GPU 设备时，您还可在集群列表的设置项中勾选 **GPU 数量**和 **GPU 型号**以查看对应数据。
2. 单击列表中某一集群的显示名称，可进入**概览**页面查看工作负载集群的概况。

   **报警**

   展示当前未解决报警的类型和数量，以及最近触发的报警信息。

   按照报警项的严重和紧急程度，报警分为**严重警告**、**注意**和**信息**三种类型。

   您可通过单击该卡片跳转至集群的**报警**界面，查看每条报警的详细信息。

   **集群基本信息**

   | 参数 | 描述 |
   | --- | --- |
   | 所属 SMTX OS 集群 | 展示工作负载集群所属 SMTX OS 集群的名称，单击名称链接可跳转至相应集群的概览页面。 |
   | CPU 架构 | 展示工作负载集群所属 SMTX OS 集群的 CPU 架构。 |
   | 创建时间 | 展示工作负载集群开始创建的时间，精确到秒。 |
   | 时区 | 展示为工作负载集群配置的时区。 |
   | Control Plane 虚拟 IP | 展示为工作负载集群配置的 Control Plane 虚拟 IP。 |
   | 存储集群接入虚拟 IP | 当工作负载集群使用 SMTX ZBS CSI 插件时，展示对应存储集群的接入虚拟 IP。 |

   **版本信息**

   | 参数 | 描述 |
   | --- | --- |
   | Kubernetes 版本 | 展示工作负载集群中已安装的 Kubernetes 的版本。  若当前集群可以升级，则在 Kubernetes 版本右侧将展示**可升级**标识，单击该标识后将弹出**集群升级**对话框，您可以执行升级操作。 |
   | SKS 版本 | 展示创建、更新或升级工作负载集群时对应 SKS 服务的版本。 |
   | SKS 功能版本 | 展示工作负载集群内置功能对应的 SKS 版本。 |

   **节点**

   单击**节点**卡片可跳转至工作负载集群的**节点**管理页面。

   | 参数 | 描述 |
   | --- | --- |
   | 节点数量 | 展示工作负载集群当前 Control Plane 节点和 Worker 节点的节点总数。 |
   | Control Plane | 展示工作负载集群的 Control Plane 节点数量。  当存在节点处于`未就绪`或`未知`状态时，可查看相应状态下的节点数量。 |
   | Worker | 展示工作负载集群的 Worker 节点数量。 |
   | Control Plane 节点操作系统 | 展示工作负载集群的 Control Plane 节点虚拟机中安装的操作系统名称。 |
   | 节点模板的 SKS 版本 | 展示工作负载集群当前使用的节点模板对应的 SKS 版本。每个 SKS 版本在发布时会同时提供多个 Kubernetes 版本的节点模板。 |
   | 系统存储 | 展示工作负载集群所有节点的存储分配量之和。 |

   **集群插件状态**

   展示工作负载集群中已开启的插件及其状态，鼠标悬浮在插件名称上可查看具体的插件版本。

   | 参数 | 描述 |
   | --- | --- |
   | 插件类型及名称 | 具体包含如下插件：  - **CNI**：calico、ecp - **CSI**：smtx-zbs-csi、smtx-elf-csi - **节点组自动伸缩**：cluster-autoscaler - **GPU**：nvidia-gpu-operator - **日志**：obs-logging-agent - **监控**：kube-prometheus、obs-monitoring-agent - **事件**：obs-event-agent - **审计**：obs-audit-agent - **证书管理**：cert-manager - **Ingress**：contour - **外部负载均衡器**：metallb - **DNS**：externaldns - **时区**：k8tz - **NTP 管理**：ntpm - **Agent**：host-config-agent、warden - **配额**：cluster-quota-enforcer |
   | 插件状态 | 插件可能出现的状态如下：  - **正常**：对应的插件已启用，已运行正常。 - **异常**：插件出现问题，无法工作。 - **启动中**：正在启动该插件。 - **关闭中**：正在关闭该插件。 |

   **CPU**

   当监控插件启用时，将展示工作负载集群的 CPU 数据：

   - 对于虚拟机集群，将展示集群中所有节点的 CPU 分配量之和，以及当前的 CPU 使用率。
   - 对于物理机集群，将分别展示集群的 Worker 节点、Control Plane 节点的 CPU 分配量之和以及当前的 CPU 使用率。

   **内存**

   当监控插件启用时，展示工作负载集群中所有节点的内存分配量之和，并分别展示**可分配**、**已使用**以及**系统预留**的内存大小和百分比。

   **GPU**

   仅当工作负载集群已配置 GPU 设备并已开启 GPU 插件时在概览中展示 GPU 卡片，当监控插件启用时可获取数据。

   在 GPU 卡片右上角可切换查看已挂载的 GPU 设备的**显存利用率**、**GPU 利用率**和**显卡使用率**。

   **Pod**

   | 参数 | 描述 |
   | --- | --- |
   | 总容量 | 展示工作负载集群中可创建的 Pod 总量。  总容量 = 节点数量 × 110 |
   | 已置备量 | 展示工作负载集群中已创建的 Pod 数量。 |
   | 可置备量 | 展示工作负载集群中剩余可创建的 Pod 数量。  可置备量 = 总容量 - 已置备量 |
   | 置备率 | 展示工作负载集群中已创建的 Pod 数量占可创建的 Pod 总容量的百分比。  置备率 = 已置备量 / 总容量 |

   **事件**

   展示工作负载集群最近一小时发生的事件。您可参考[查看事件信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_61)了解事件列表中各项参数的含义，在事件信息右侧单击 **...** > **查看详情**，可以查看详细的事件信息。

   若您已为集群启用事件功能，在事件列表右上方单击**查看更多**，可跳转至工作负载集群的**事件**界面[查看事件信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_61)。

---

## 管理工作负载集群 > 下载 Kubeconfig 文件

# 下载 Kubeconfig 文件

Kubeconfig 文件中包含了访问工作负载集群所需的访问地址和认证凭据，可结合 kubectl 命令行工具或其他客户端来使用。当工作负载集群创建完成并需要交付给使用者时，创建者可参考以下步骤获取集群的 Kubeconfig 文件内容并发送给使用者，使用者则可以根据自己的情况选择不同的方式来访问工作负载集群，具体的访问方式可以参见 Kubernetes 官网的[访问集群](https://kubernetes.io/zh-cn/docs/tasks/access-application-cluster/access-cluster/)章节。

**注意事项**

工作负载集群创建完成后，Kubeconfig 文件每隔 183 天将更新一次，每份文件的有效期均为一年，具体计算方式如下：

- Kubeconfig 文件更新之前，Kubeconfig 文件的过期时间 = 集群创建时间 + 365 天
- Kubeconfig 文件更新之后，Kubeconfig 文件的过期时间 = 文件最近更新时间 + 365 天

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在右上角单击**下载 Kubeconfig**图标。
3. 在弹出的**下载 Kubeconfig** 对话框中将展示 Kubeconfig 文件的具体内容，选择以下方式中的一种获取内容：

   - 在对话框右下角单击**下载**，下载整个文件。
   - 在对话框左下角单击**复制**，复制文件的内容。

---

## 管理工作负载集群 > 打开集群控制台

# 打开集群控制台

集群控制台内置了 kubectl、Helm、node-shell、kustomize、vi、vim、curl、git、jq、yq 等常用工具。您可以在集群控制台中使用命令行管理和操作整个工作负载集群，例如查看集群状态、管理集群资源。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在右上角单击**集群控制台**，此时在界面下方将弹出当前工作负载集群的控制台窗口。窗口名称为 `kubectl: 集群显示名称`，您可以在窗口右上角对窗口执行展开/收起、全屏/退出全屏、新建窗口、关闭窗口操作。
3. 在控制台窗口中执行命令管理集群。您还可以在控制台中执行以下操作：

   - 在窗口右上角搜索控制台中的命令、调整字体大小、下载控制台日志、清空命令行。
   - 在窗口左上角的下拉框中选择其他集群进入对应的控制台窗口。

**配置示例**

如果您想通过 Helm 安装 Nginx，请确保集群能够访问互联网，然后在控制台中执行以下命令。

```
# 如果没有添加 Bitnami 的 Helm 仓库，可使用以下命令添加
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# 安装 Nginx Chart
helm install my-nginx bitnami/nginx

# 检查安装状态
kubectl get pods
kubectl get svc
```

---

## 管理工作负载集群 > 导入 YAML

# 导入 YAML

您可以通过 YAML 文件创建 Kubernetes 资源对象，系统将使用 `kubectl apply` 命令来创建或更新资源，可支持原生 Kubernetes 资源对象和用户自定义资源对象（CRD）。

**前提条件**

请确保 YAML 文件符合 Kubernetes 资源定义规范且格式正确。

**注意事项**

- YAML 文件中的多个资源对象之间请使用 `---` 分隔符进行分隔。
- 一次导入的 YAML 文件最多支持 100000 行。

**操作步骤**

1. 在工作负载集群列表中，单击目标工作负载集群的显示名称，进入工作负载集群**概览**页面。
2. 在右上角单击**导入 YAML**。
3. 使用如下任一方式导入 YAML。

   - **导入文件**：在左上角单击**选择文件**导入单个文件，或单击**选择文件夹**批量导入多个文件。支持 `.yaml` 或 `.json` 格式的文件。
   - **输入 YAML 内容**：在**配置内容**区域输入或粘贴 YAML 内容。在配置内容的右上角可复制 YAML、重置 YAML 或查看 YAML 改动。
4. 导入的 YAML 内容将高亮显示语法标记并自动进行格式校验，您也可以按需编辑 YAML 内容。
5. 在右上角选择指定的**名字空间**。

   - 未选择名字空间：使用 YAML 中定义的名字空间。
   - 选择指定名字空间：无论 YAML 文件中是否定义名字空间，均以所选名字空间为准。
   - 未选择且 YAML 中也未定义名字空间：使用 `default` 名字空间。
6. 单击**导入**，开始部署资源对象。

   导入完成后，页面将显示导入结果。

   - **状态**：包括 `成功` 和 `失败`。导入失败的 YAML 将展示失败原因，请根据提示调整 YAML 配置后重新导入。
   - **变更类型**：

     - `创建`：当导入的 YAML 资源对象不存在时，系统将创建资源。
     - `更新`/`未更新`：当导入的 YAML 资源对象已存在时，系统将更新资源。
7. 单击**关闭**，完成导入操作。

   导入完成后，您可以在工作负载集群详情页面左侧导航栏中，选择相应的资源类型，查看已导入的资源对象详情。

**配置示例**

以下示例展示如何通过 YAML 文件部署一个 Nginx 应用，并通过 Service 为该应用提供集群内的网络访问。

```
# 创建一个 Nginx Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp  # 应用名称
  labels:
    app: myapp
spec:
  replicas: 3  # 副本数量
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp 
    spec:
      containers:
      - name: nginx
        image: nginx:latest  # 使用最新版本的 Nginx 镜像
        ports:
        - containerPort: 80  # 容器内 Nginx 服务监听的端口
---
# 创建一个 Service 来暴露 Nginx Deployment
apiVersion: v1
kind: Service
metadata:
  name: myapp-service  # Service 名称
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80        # Service 监听的端口
      targetPort: 80  # 映射至 Pod 的 80 端口
  type: ClusterIP  # 仅支持集群内部访问
```

---

## 管理工作负载集群 > 编辑 K8s 集群配置

# 编辑 K8s 集群配置

当工作负载集群的状态为**就绪**、**运行中**或**异常**时，您可以根据需求对工作负载集群的 kube-apiserver、kube-controller-manager、etcd、kube-scheduler、kubelet、kubeletConfiguration 等 K8s 组件的参数进行调整。编辑配置后，SKS 将原地更新集群中相关节点的配置。

**注意事项**

- 若 K8s 组件参数配置错误，则可能导致工作负载集群运行异常。如非必要需求，请勿随意编辑参数配置。
- 默认情况下，Control Plane 节点的 `initConfiguration`、`joinConfiguration` 以及 Worker 节点的 `joinConfiguration` 三处配置相同，但在 UI 中默认仅显示 `initConfiuration` 的配置，若仅修改该配置，系统会自动将修改同步至其余两处配置。若需避免系统同步修改，可以在 UI 中以声明式方式填写两处 `joinConfiguration` 的配置。
- 编辑 sysctl 参数或 kubelet 类别的系统参数后，SKS 将原地更新集群配置并驱逐节点上的 Pod。

**操作步骤**

1. 在工作负载集群列表中，单击目标工作负载集群的显示名称，进入工作负载集群**概览**页面。
2. 在右上角单击 **...**，选择**编辑 K8s 集群配置**。
3. 在弹出的**编辑 K8s 集群配置**对话框中，按需编辑**配置内容**。

   具体参数说明请按需参见[创建虚拟机集群 > 配置 K8s 集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_18)或[创建物理机集群 > 配置 K8s 集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_24)小节。
4. 单击**配置内容**窗口右上角的图标，可复制、重置或查看改动，编辑前后的差异内容将被高亮展示。
5. 编辑完成后，单击**保存**。

---

## 管理工作负载集群 > 下载集群规格文件

# 下载集群规格文件

集群规格文件包含了工作负载集群的元数据以及插件等所有配置信息，您可以通过该文件快速了解集群配置，以便进行故障排查等操作。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在右上角单击 **...**，选择**下载集群规格文件**。
3. 在弹出的**下载集群规格文件**对话框中将展示集群规格文件的具体内容。

   - 单击**下载**，可下载整个文件。下载的文件默认命名为 `<工作负载集群显示名称>-spec.yaml`。
   - 单击**复制**，可复制整个文件的内容。

---

## 管理工作负载集群 > 暂停/恢复同步工作负载集群

# 暂停/恢复同步工作负载集群

Kubernetes 采用声明式的机制来定义某个资源的期望状态，并保证资源的实际状态与期望状态一致。当资源的实际状态与用户定义的期望状态不一致时，Kubernetes 会自动执行必要的更改，以确保二者保持一致，该过程即为**同步**。

当您需要进行集群维护、故障排查等操作时，可使用**暂停同步**功能，暂时停止集群同步。暂停同步后，即使集群的实际状态与期望状态不一致，也不会自动调整。操作完成后，您可以使用**恢复同步**功能，将集群状态恢复至期望状态。

**注意事项**

- 处于**暂停同步中**状态的工作负载集群，不支持升级、编辑 K8s 集群配置、管理节点组、管理节点、管理插件等操作。
- 当工作负载集群处于**删除中**状态时，不支持**暂停同步**。
- 暂停同步会导致集群的资源状态与期望状态不一致，请避免集群长期处于暂停同步状态。

**操作步骤**

1. 在工作负载集群列表中，单击目标工作负载集群的显示名称，进入工作负载集群**概览**页面。
2. 在右上角单击 **...**，选择**暂停同步**或**恢复同步**。

---

## 管理工作负载集群 > 管理节点组及节点

# 管理节点组及节点

工作负载集群创建完成后，您可以查看和编辑集群的所有节点组，对于 Worker 节点组可以执行创建、删除操作。您还可以查看工作负载集群的所有节点信息，编辑节点或对出现故障的节点进行替换操作。

---

## 管理工作负载集群 > 管理节点组及节点 > 查看节点组

# 查看节点组

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**节点管理** > **节点组**，可在列表中查看工作负载集群的所有节点组信息。

   > **说明**：
   >
   > - 在列表中的设置项中勾选**节点类型**，可以查看节点组中的节点为虚拟机还是物理机。
   > - 当工作负载集群已配置 GPU 设备并已开启监控插件时，您还可在列表中的设置项中勾选 **GPU 显存总分配量**以查看节点组挂载的所有 GPU 设备的显存资源总量。
3. 在节点组列表中单击某一节点组，在弹出的详情面板中可以查看该节点组的配置信息。

   > **说明**：
   >
   > 对于挂载了 GPU 设备的节点组，您还可以查看 **GPU 使用方式**、**GPU 型号**和 **GPU 显存总分配量**。其中，仅当工作负载集群已开启监控插件时，才可以获取 **GPU 显存总分配量**的数据。
4. 单击**节点**页签，可查看节点组中的所有节点。单击节点名称右侧的 **>** 图标可以跳转到节点的详情页面查看节点的详细信息。

---

## 管理工作负载集群 > 管理节点组及节点 > 编辑节点组

# 编辑节点组

您可以编辑工作负载集群中的节点组配置，或批量为 Worker 节点组中的节点配置自定义标签、注解和污点。

## 编辑节点组配置

编辑不同类型的节点组配置有不同的前提条件和注意事项，建议阅读后再进行编辑操作。

### 编辑 Control Plane 节点组

**前提条件**

- 工作负载集群处于`就绪`、`运行中`或`异常`状态。
- 若需要增加节点数，建议提前做好以下准备：
  - 参考[工作负载集群资源要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_12)的描述，确保工作负载集群所属的 SMTX OS 集群的剩余资源满足增加节点的要求。
  - 当节点的业务网卡 IP 是由 IP 池自动分配时，请确保 IP 池中的可用 IP 足够分配给所有新增的节点。

**注意事项**

- 不支持将节点数量从 3 或 5 减少到 1。
- 若节点组中的节点数为 1，则不支持启用故障节点自动替换功能。

### 编辑虚拟机类型的 Worker 节点组

**前提条件**

- 工作负载集群处于`就绪`、`运行中`或`异常`状态。
- 若编辑后的节点数上限大于当前的节点数上限，建议提前做好以下准备：
  - 参考[工作负载集群资源要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_12)的描述，确保为工作负载集群提供资源的集群满足增加节点上限的要求。
  - 当节点的业务网卡 IP 是由 IP 池自动分配时，请确保 IP 池中的可用 IP 足够分配给所有可能新增的节点。
- 若需要将节点数类型从**固定节点数**切换为**自动伸缩**，请确保工作负载集群的节点组自动伸缩开关已开启，可参考[管理节点组自动伸缩](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_64)进行启用。
- 若需要为节点组挂载 GPU 设备，请先确认[虚拟机集群使用 GPU 设备要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_23#%E8%99%9A%E6%8B%9F%E6%9C%BA%E9%9B%86%E7%BE%A4%E4%BD%BF%E7%94%A8-gpu-%E8%AE%BE%E5%A4%87%E8%A6%81%E6%B1%82)并[准备 GPU 资源](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_09)。

**注意事项**

- 节点组的资源规格仅支持增大，不支持减小。
- 若选择冷扩容的方式更新 CPU，SKS 将滚动更新节点组中的相关节点，可能产生业务中断的风险，建议您在业务空闲期进行更改。
- 更改节点组的资源规格（冷扩容 CPU 除外）后，SKS 将原地更新集群中相关节点的配置，但仍建议您在业务空闲期进行更改。若更改 CPU 和内存，SKS 将驱逐节点上的 Pod。
- 若工作负载集群未配置 GPU 设备，在为节点组挂载 GPU 设备后，NVIDIA GPU Operator 插件将会自动开启，如果挂载的是 vGPU，则还需要再对该插件进行配置以添加 NVIDIA vGPU 许可证。关于该插件的配置可参考[配置 GPU](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_19#%E9%85%8D%E7%BD%AE-gpu)。
- 若 Worker 节点组已挂载 GPU 设备，您可以根据实际负载情况按需增加 GPU 数量，需注意：
  - 增加直通 GPU 或 vGPU 数量时，若当前可挂载的 GPU 设备数量不足，将会导致增加失败。

    > **说明**：
    >
    > 当挂载 GPU 设备的虚拟机未被永久删除时，SKS 不支持将对应 GPU 设备挂载至工作负载集群中的 Worker 节点虚拟机。
  - 增加直通 GPU 或 vGPU 数量时，系统将通过 Pod 迁移确保节点上工作负载的业务连续性。当工作负载的业务负载过高时可能导致 Pod 迁移受影响，进而产生业务中断的风险，建议您在业务空闲期进行更改。
- 若将节点数类型从**自动伸缩**切换到**固定节点数**，固定节点数将默认显示当前的节点数量。

### 编辑物理机类型的 Worker 节点组

**前提条件**

若需要添加物理机节点，请确认已在符合要求的物理机上安装兼容的操作系统，完成网络配置，并在 CloudTower 的 **Kubernetes 服务**界面上完成物理机添加操作，操作指导可参考[添加物理机](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_10)。

**注意事项**

若移除物理机节点：

- 被移除节点上的 Pod 将被驱逐，负载过高的情况下可能会影响业务的连续性。
- SKS 将解除组中的物理机与集群的关联，并清除 SKS 在物理机被添加到集群阶段为其安装的配置文件和其他参数设置，物理机仍可被添加至其他物理机集群。

### 操作步骤

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**节点管理** > **节点组**。
3. 在待编辑的节点组右侧单击 **...** > **编辑**，按需修改节点组的配置。配置指导可参考[创建工作负载集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)中的**配置节点**小节。
4. 编辑完成后，单击**保存**。

## 编辑 Worker 节点组属性

您可以批量为节点组中的节点配置自定义标签、注解或污点属性。

**注意事项**

页面中仅显示您通过本操作配置的标签、注解和污点，节点上通过其他来源添加的属性不会显示。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**节点管理** > **节点组**。
3. 在节点组列表页面按需编辑节点组中节点的属性，包括标签、注解和污点。

   - 单击 **...** > **编辑标签**，添加、修改或移除标签。
   - 单击 **...** > **编辑注解**，添加、修改或移除注解。
   - 单击 **...** > **编辑污点**，添加、修改或移除污点。支持配置污点效果，包括`仅阻止调度`、`尽可能阻止调度`和`阻止调度并驱逐 Pod`。鼠标悬浮在效果后的图标上，可查看每种效果的具体生效机制。
   - 在**编辑标签**、**编辑注解**或**编辑污点**页面，单击**查看格式要求**链接，可查看标签、注解和污点的键值填写格式要求。
4. 单击**保存**。

---

## 管理工作负载集群 > 管理节点组及节点 > 创建 Worker 节点组

# 创建 Worker 节点组

**前提条件**

- 工作负载集群处于**就绪**、**异常**或**运行中**状态。
- 参考[工作负载集群资源要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_12)中的描述，确保为工作负载集群提供资源的集群满足增加节点数量的要求。
- 当工作负载集群为虚拟机集群时：
  - 如果节点业务网卡的 IP 是由 IP 池自动分配的，则需要确保 IP 池中的可用 IP 足够分配给新创建的 Worker 节点组的节点。
  - 如果需要启用节点组自动伸缩功能，请确保工作负载集群的节点组自动伸缩开关已开启，可参考[管理节点组自动伸缩](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_64)进行启用。
  - 如果需要为节点组挂载 GPU 设备，请先[确认使用 GPU 设备要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_23)并[准备 GPU 资源](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_09)。
- 当工作负载集群为物理机集群时，请确认已在符合要求的物理机上安装兼容的操作系统，完成网络配置，并在 CloudTower 的 **Kubernetes 服务**界面上完成物理机添加操作，操作指导可参考[添加物理机](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_10)。

**注意事项**

- 对于虚拟机集群，如果集群未配置 GPU 设备，在为新 Worker 节点组挂载 GPU 设备后，NVIDIA GPU Operator 插件将会自动开启，如果挂载的是 vGPU，则还需要再对该插件进行配置以添加 NVIDIA vGPU 许可证。关于该插件的配置可参考[配置 GPU](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_19#%E9%85%8D%E7%BD%AE-gpu)。
- 对于物理机集群，如果新创建的 Worker 节点组需要使用 GPU 设备，节点组创建完成后，还需要在集群的管理界面中单击**设置** > **插件管理**，开启 **NVIDIA GPU Operator** 插件。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**节点管理** > **节点组**。
3. 单击 **+ 创建节点组**。
4. 在弹出的**创建节点组**对话框中，配置新创建的节点组。配置指导可参考[创建工作负载集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)中对于 Worker 节点组的配置说明。
5. （可选）若需要创建多个节点组，请单击 **+ 添加节点组**进行创建。
6. 配置完成后，单击**创建**。

---

## 管理工作负载集群 > 管理节点组及节点 > 删除 Worker 节点组

# 删除 Worker 节点组

在工作负载集群中，当有多个 Worker 节点组时，可以按需删除 Worker 节点组。

**前提条件**

工作负载集群处于**就绪**、**运行中**或**异常**状态。

**注意事项**

- 当工作负载集群中仅存在一个 Worker 节点组时，不允许删除。
- 对于物理机集群，删除 Worker 节点组后，SKS 将解除组中的物理机与集群的关联，并清除 SKS 在物理机被添加到集群阶段为其安装的配置文件和其他参数设置，物理机仍可添加至其他物理机集群。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**节点管理** > **节点组**。
3. 单击目标 Worker 节点组，在弹出的详情面板中单击**删除**。
4. 在弹出的**删除节点组**对话框中单击**删除**。

---

## 管理工作负载集群 > 管理节点组及节点 > 查看节点

# 查看节点

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**节点管理** > **节点**，可在列表中查看工作负载集群的所有节点信息。

   其中，**状态**一列展示节点当前的状态，具体如下表所示。

   | 状态 | 描述 |
   | --- | --- |
   | 就绪 | 节点健康并已经准备好接收 Pod。 |
   | 未就绪 | 节点当前无法接收 Pod，可能在创建中或节点不健康。 |
   | 未知 | 节点控制器在最近 node-monitor-grace-period 期间（默认 40 秒）未收到节点的消息。 |
   | 更新中 | 节点正在更新配置。 |
   | 待更新 | 节点在等待更新的队列中，尚未开始更新。 |

   > **说明**：
   >
   > - 在列表中的设置项中还可以勾选**节点类型**、**更新时间**等以查看更多信息。
   > - 物理机节点的名称与添加物理机时设置的物理机名称相同。
   > - 当工作负载集群已配置 GPU 设备并已开启监控插件时，您还可在列表中的设置项中勾选 **GPU 显存**和 **GPU 显存使用率**以查看对应数据。
3. 在节点列表中单击某一节点，在详情页面中可以查看该节点的详细信息。

   **详情**

   - **基本信息**

     | 参数 | 描述 |
     | --- | --- |
     | 节点角色 | 节点的角色，有以下两种类型： - Control Plane - Worker |
     | 可否调度 | 节点是否允许调度新的 Pod，有以下两种状态： - `是`：节点可以接收新的 Pod。 - `否`：节点无法接收新的 Pod。 |
     | 节点类型 | 节点的类型，包括`物理机`和`虚拟机`。 |
     | 业务网卡 IP | 节点业务网卡的 IP。 |
     | 节点组 | 节点所属节点组的名称。单击名称链接，可跳转至节点组详情页面。 |
     | 操作系统版本 | 节点对应的虚拟机的操作系统版本。 |
     | 容器运行时版本 | 节点上安装的容器运行时的版本。 |
     | kubelet 版本 | 节点的 kubelet 版本。 |
     | kube-proxy 版本 | 节点的 kube-proxy 版本。 |
     | 更新时间 | 节点最近一次通过原地更新的方式完成配置更新或者 Kubernetes 版本升级的时间。 |
     | 创建时间 | 节点的创建时间。 |
     | 所属 SMTX OS 集群（仅虚拟机节点展示） | 节点对应的虚拟机的所属 SMTX OS 集群。单击名称链接，可跳转至集群概览页面。 |
     | 所属可用域（仅 SMTX OS 双活集群虚拟机节点展示） | 节点对应的虚拟机的所属可用域。 |
     | 所属主机（仅虚拟机节点展示） | 节点对应的虚拟机的所属主机。单击名称链接，可跳转至主机概览页面。 |
     | 对应虚拟机（仅虚拟机节点展示） | 节点对应的虚拟机。单击虚拟机名称链接，可跳转至虚拟机详情页面；单击名称后的图标，可打开虚拟机终端。 |
     | 对应物理机（仅物理机节点展示） | 节点对应的物理机。 |
     | 标签 | 展示节点具有的 Kubernetes 标签，用于标识和选择节点。该标签与通过 CloudTower 创建的标签不同，是 Kubernetes 内部的标签。 |
     | 注解 | 展示节点具有的 Kubernetes 注解，用于存储非标识性元数据。 |
     | 其他 IP | 节点上除业务网卡 IP 之外的其他 IP 地址。 |
   - **运行状态**

     > **说明**：
     >
     > - 对于磁盘空间压力、内存压力和进程压力：绿色表示无压力、红色表示有压力、黄色表示未知。
     > - 对于网络可用性：绿色表示可用，红色表示不可用，黄色表示未知。

     | 参数 | 描述 |
     | --- | --- |
     | 磁盘空间压力 | 节点的磁盘空间使用情况是否有压力。 |
     | 内存压力 | 节点的内存使用情况是否有压力。 |
     | 进程压力 | 节点是否有进程压力。 |
     | 网络可用性 | 节点的网络是否可用。 |
   - **资源用量**

     > **说明**：
     >
     > 仅当监控插件启用时可获取资源用量数据。

     | 参数 | 描述 |
     | --- | --- |
     | CPU | 展示节点的 CPU 使用量、分配量以及使用率。 |
     | 内存 | 展示节点的内存使用量、分配量以及使用率。 |
     | GPU 显存（仅当工作负载集群已配置 GPU 设备时展示该参数） | 展示节点上挂载的 GPU 设备的显存使用量、分配量以及使用率。 |
     | 系统存储 | 展示节点的系统存储使用量、总容量、分配量以及使用率。 |
     | Pod | 展示节点中已创建的 Pod 数量、可创建的 Pod 数量以及 Pod 的置备率。 |
   - **污点**

     用于排斥某些类型的 Pod 调度到该节点。

     | 参数 | 描述 |
     | --- | --- |
     | 键 | 污点的键。 |
     | 值 | 污点的值。 |
     | 效果 | 污点的效果，包括`仅阻止调度`、`尽可能阻止调度`和`阻止调度并驱逐 Pod`。 |
   - **状况**

     展示节点的状况信息，包括状况的类型、状态、状态最新变更时间、状态变更原因以及变更的详细信息。

   **Pod**

   单击 **Pod** 页签，可查看节点包含的所有 Pod 列表，具体参数说明请参见[查看 Pod](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_45#%E6%9F%A5%E7%9C%8B-pod)。

   **事件**

   单击**事件**页签，可查看节点相关的事件列表，包括事件的类型、原因、事件信息以及事件最近一次的发生时间。

   **监控**

   仅当工作负载集群启用了监控插件时，可以查看节点的监控信息。支持设置监控查询的时间范围，以及监控信息的刷新频率。

   - 启用监控插件请参见[创建工作负载集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)中的**配置集群插件** > **配置可观测性**小节。
   - 展示的监控图表类型与工作负载集群的 `Node Exporter / Nodes` 监控视图下的监控图表类型一致。

---

## 管理工作负载集群 > 管理节点组及节点 > 打开节点控制台

# 打开节点控制台

您可以在节点控制台中使用命令行进行操作系统级别的调试，例如进行 Kubernetes 系统组件配置、组件运行状态监控。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**节点管理** > **节点**，然后在节点列表中单击某一节点，进入节点的**详情**页面。
3. 在**详情**页面右上方单击**节点控制台**，此时在界面下方将弹出当前节点的控制台窗口。窗口名称为 `node: 节点名称`，将鼠标悬浮在名称右侧的信息图标 i 时可查看所属集群名称，您还可以在窗口右上角对窗口执行展开/收起、全屏/退出全屏、新建窗口、关闭窗口操作。
4. 在控制台窗口中执行命令管理节点。您还可以在窗口右上角搜索控制台中的命令、调整字体大小、下载控制台日志、清空命令行。

**配置示例**

若需要查看 kubelet 的状态，您可在节点控制台中执行以下命令。

```
systemctl status kubelet
```

---

## 管理工作负载集群 > 管理节点组及节点 > 编辑节点调度状态

# 编辑节点调度状态

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**节点管理** > **节点**。
3. 编辑节点调度状态。

   - 对于不可调度的节点，在节点列表页面可单击 **...** > **恢复调度**。
   - 对于可以调度的节点，在节点列表页面可单击 **...** > **停止调度**。适用于节点维护、故障排查等场景。

---

## 管理工作负载集群 > 管理节点组及节点 > 替换节点（仅适用于虚拟机节点）

# 替换节点（仅适用于虚拟机节点）

当某一节点出现故障时，可以参考以下步骤手动替换节点，替换后系统将自动创建一个新的节点，并删除异常节点。

**前提条件**

需被替换的异常节点不是工作负载集群中唯一一个 Control Plane 节点。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**节点管理** > **节点**。
3. 在节点列表中单击某一节点，在弹出的详情面板中单击**替换节点**。
4. 在弹出的**替换节点**对话框中，确认要替换的节点名称。
5. 单击**替换**。

---

## 管理工作负载集群 > 管理名字空间

# 管理名字空间

[名字空间](https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/namespaces/)为 Kubernetes 中的资源提供了一种组织方式，允许用户将同一集群中的资源划分为相互隔离的组，使得它们既可以共享同一个集群的服务，也能够互不干扰。

## 创建名字空间

**注意事项**

当名字空间的名称与 `System` 项目中的名字空间同名时，该名字空间将自动关联至系统项目。为避免自动关联，请确保自定义名字空间与 `System` 项目中的名字空间未重名。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**名字空间**。
3. 单击 **+ 创建名字空间**。
4. 输入名字空间的名称。名称仅支持小写字母、数字、连字符（-），且必须以小写字母或数字开头和结尾，长度为 1 ～ 63 个字符。
5. 单击**创建**。

> **说明**：
>
> 项目允许将多个名字空间作为一个组统一管理，并在其中执行 Kubernetes 操作。一个名字空间只能属于一个项目。名字空间创建完成后，请为其关联项目，关联后可被项目内的成员访问，以实现集群内资源的有效隔离。

## 查看名字空间

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**名字空间**，可在列表中查看工作负载集群的所有名字空间信息。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | 名字空间的名称。 |
   | 状态 | 名字空间当前的状态。  - `活跃`：名字空间正常运行。 - `删除中`：名字空间正在被删除，所有资源将依次被清理和删除。 |
   | 所属项目 | 名字空间所属项目的名称。单击项目名称链接可跳转至项目详情页面。 |
   | CPU 使用量 | 名字空间内的 CPU 资源使用量。 |
   | 内存使用量 | 名字空间内的内存资源使用量。 |
   | Pod 数量 | 名字空间内的 Pod 数量，显示为`就绪数量/总数`。 |
   | 创建时间 | 名字空间的创建时间。 |
3. 单击名字空间的名称链接，进入名字空间详情页面。

   除名字空间列表中包含的参数外，对于不属于 `system` 项目的名字空间，还可展示其设置的**名字空间配额**，以及该名字空间内各类资源配额的已分配量和使用率。

## 编辑名字空间配额

名字空间配额受项目配额限制，设置名字空间配额前，请先了解**项目配额与名字空间配额间的约束关系**，并进行合理规划：

- 项目下各名字空间可以单独设置资源配额。虽然所有名字空间设置的配额总和可以超过所在项目的配额，但实际名字空间的资源使用上限不可超过项目配额。
- 若项目设置配额，但名字空间未设置配额，则名字空间的资源实际使用量受项目配额限制，多个名字空间可共享项目的剩余资源。

  例如，项目 A 的 CPU 限制配额为 8 core，名字空间 A1、A2 没有限制配额，那么名字空间 A1 在名字空间 A2 未使用任何资源时，最多可以使用 8 core。
- 若项目与名字空间均设置配额，则需同时满足两层配额限制。即名字空间的资源实际使用量不能超过名字空间的配额，项目下所有名字空间的资源实际使用量也不能超过项目配额。

  例如，项目 A 的 CPU 限制配额为 8 core，名字空间 A1 的 CPU 限制配额为 5 core，名字空间 A2 的 CPU 限制配额为 5 core。此时，名字空间 A1 的资源使用量不能超过 5 core，名字空间 A2 的资源使用量不能超过 5 core，两个名字空间合计的总 CPU 使用量不能超过 8 core。
- 当资源使用量接近配额（默认阈值为配额的 80%）时，系统将触发报警，以便您能够及时调整资源分配。如需调整报警阈值，请参考《CloudTower 使用指南》的**管理报警** > **管理报警规则** > **编辑内置规则**小节。当资源使用量超出配额时，将阻止新的资源创建，但不会影响存量资源。

**注意事项**

属于 `System` 项目的名字空间不支持设置配额。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**名字空间**。
3. 在某一名字空间右侧单击 **...** > **编辑名字空间配额**。默认不限制配额，设置为 `0` 表示禁止该名字空间申请或使用此类资源。

   | 参数 | 描述 |
   | --- | --- |
   | CPU 请求 | 预留给名字空间内所有 Pod 使用的最小 CPU 量。 |
   | CPU 限制 | 分配给名字空间内所有 Pod 使用的最大 CPU 量。 |
   | 内存请求 | 预留给名字空间内所有 Pod 使用的最小内存量。 |
   | 内存限制 | 分配给名字空间内所有 Pod 使用的最大内存量。 |
   | 持久卷申领 | 名字空间中允许存在的持久卷声明的最大总量。 |
   | GPU 数量 | 名字空间中允许使用的 GPU 资源的最大数量。 |
4. 单击**保存**。

## 删除名字空间

**注意事项**

- 属于 `System` 项目的名字空间和 `default` 名字空间不支持删除。
- 删除名字空间将同时删除该名字空间下的所有资源。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**名字空间**。
3. 对于不再需要使用的名字空间，单击 **...** > **删除**。
4. 在弹出的确认对话框中，确认删除操作。

---

## 管理工作负载集群 > 管理工作负载

# 管理工作负载

[工作负载](https://kubernetes.io/zh-cn/docs/concepts/workloads/)是在 Kubernetes 集群上运行的应用程序，您可以在 Kubernetes 上的一组或多组 Pod 中运行它。工作负载通常通过工作负载资源（如 Deployment、StatefulSet 等）来定义和管理。

在 SKS 中，工作负载应部署在工作负载集群。工作负载集群创建完成后，您可以按需创建并管理各类工作负载资源，以便有效地运行和维护您的应用程序。

---

## 管理工作负载集群 > 管理工作负载 > 管理 CronJob

# 管理 CronJob

[CronJob](https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/cron-jobs/) 根据调度时间表重复调度 Job，适用于执行排期操作（例如备份、数据定时同步等），以确保 Job 在预定的时间间隔内可靠地运行。

## 创建 CronJob

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**工作负载** > **CronJob**。
3. 单击 **+ 创建 CronJob**。
4. **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

   ```
   apiVersion: batch/v1
   kind: CronJob    # 资源的类型，该段 YAML 配置定义了一个 CronJob
   metadata:
     name: example    # CronJob 的名称
     namespace: default    # CronJob 所属的名字空间
   spec:
     schedule: '@daily'    # 指定 CronJob 的调度周期，填写方式可参考 Cron 时间表语法（https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/cron-jobs/#cron-schedule-syntax）
     jobTemplate:    # 为 CronJob 创建 Job 定义模板
       spec:
         template:    
           spec:    # Job 中定义的 Pod 模板
             containers:
               - name: example    # 容器的名称
                 image: registry.smtx.io/kubesmart/alpine:3    # 容器使用的镜像
                 args:    # 容器启动时执行的命令和参数
                   - /bin/sh
                   - '-c'
                   - date; echo Hello from the Kubernetes cluster
             restartPolicy: OnFailure    # Pod 的重启策略
   ```

   在配置内容的右上角可复制 YAML、重置 YAML 或查看 YAML 改动。
5. 单击**创建**。

## 查看 CronJob

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**工作负载** > **CronJob**，可在列表中查看工作负载集群的所有 CronJob 信息。您可以根据一个或多个名字空间进行快速筛选。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | CronJob 的名称。 |
   | 状态 | CronJob 的状态，包括`运行中`和`已挂起`。 |
   | 名字空间 | CronJob 所属的名字空间。 |
   | 容器镜像 | CronJob 执行时使用的容器镜像，镜像中封装了应用程序及其所有软件依赖的二进制数据。 |
   | 调度时间表 | CronJob 的调度时间表，具体含义可参考 [Cron 时间表语法](https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/cron-jobs/#cron-schedule-syntax)。 |
   | 上次调度时间 | CronJob 上次执行的时间。 |
   | 创建时间 | CronJob 的创建时间。 |
3. 单击 CronJob 的名称链接，可查看 CronJob 的详细信息。

   - **基本信息**：除 CronJob 列表中包含的参数外，还可展示 CronJob 的标签和注解信息。
   - **Job**：展示 CronJob 创建并管理的 Job，具体参数说明请参见[查看 Job](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_43#%E6%9F%A5%E7%9C%8B-job)。
4. 单击**事件**页签，可查看 CronJob 相关的事件列表，包括事件的类型、原因、事件信息以及事件最近一次的发生时间。

## CronJob 相关操作

在 CronJob 列表页面选择 **...**，可完成如下操作；您也可以进入 CronJob 的详情页面执行相应操作。

- **编辑 YAML**：编辑 CronJob 的 YAML 配置，具体参数说明可参考[创建 CronJob](#%E5%88%9B%E5%BB%BA-cronjob)。保存成功后，新的配置将在下一个调度周期开始时生效。
- **下载 YAML**：下载 CronJob 的 YAML 文件。
- **暂停或恢复**：对于**运行中**状态的 CronJob，可**暂停**调度；对于**已挂起**状态的 CronJob，可**恢复**调度。
- **删除**：对于不再需要使用的 CronJob，可执行删除操作。

---

## 管理工作负载集群 > 管理工作负载 > 管理 DaemonSet

# 管理 DaemonSet

[DaemonSet](https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/daemonset/) 确保全部（或者某些）节点上仅运行一个 Pod 副本。当有新节点加入集群时，DaemonSet 会为该节点新增一个 Pod；当有节点从集群移除时，DaemonSet 也会自动回收相应的 Pod。

## 创建 DaemonSet

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**工作负载** > **DaemonSet**。
3. 单击 **+ 创建 DaemonSet**。
4. **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

   ```
   apiVersion: apps/v1
   kind: DaemonSet    # 资源的类型，即该段 YAML 配置定义了一个 DaemonSet
   metadata:
     name: example    # DaemonSet 的名称
     namespace: default    # DaemonSet 所属的名字空间
   spec:
     selector:    # 选择器，用于指定哪些 Pod 由该 DaemonSet 管理
       matchLabels: 
         app: daemonset-example    # 匹配标签为 app: daemonset-example 的 Pods
     template:    # Pod 模板，定义了由 DaemonSet 创建的 Pods 的规格
       metadata:
         labels:
           app: daemonset-example    # 定义 Pod 的标签，需与 selector 匹配
       spec:
         containers:    # 定义 Pod 中的容器
           - name: daemonset-example    # 容器的名称
             image: registry.smtx.io/kubesmart/bitnami/nginx:1.25.2-debian-11-r2    # 容器使用的镜像
             ports:
               - containerPort: 8080    # 容器暴露的端口
   ```

   在配置内容的右上角可复制 YAML、重置 YAML 或查看 YAML 改动。
5. 单击**创建**。

## 查看 DaemonSet

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**工作负载** > **DaemonSet**，可在列表中查看工作负载集群的所有 DaemonSet 信息。您可以根据一个或多个名字空间进行快速筛选。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | DaemonSet 的名称。 |
   | 状态 | DaemonSet 的状态，包括`已就绪`和`更新中`。 |
   | 名字空间 | DaemonSet 所属的名字空间。 |
   | 容器镜像 | DaemonSet 执行时使用的容器镜像，镜像中封装了应用程序及其所有软件依赖的二进制数据。 |
   | Pod 数量 | 展示 Pod 的`就绪数量/预期数量`。 - **Pod 就绪数量**：DaemonSet 需要创建和管理的 Pod 中处于就绪状态的 Pod 数量。 - **Pod 预期数量**：DaemonSet 需要创建和管理的 Pod 数量。 |
   | 重启次数 | DaemonSet 中所有 Pod 的容器自创建以来由于失败而被重新启动的总次数。 |
   | 创建时间 | DaemonSet 的创建时间。 |
3. 单击 DaemonSet 的名称链接，可查看 DaemonSet 的详细信息。

   - **基本信息**：除 DaemonSet 列表中包含的参数外，还可展示 DaemonSet 的标签和注解信息。
   - **Pod**：展示 DaemonSet 包含的 Pod 列表，具体参数说明请参见[查看 Pod](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_45#%E6%9F%A5%E7%9C%8B-pod)。
   - **状况**：展示 DaemonSet 的 Condition 信息，包括 Conditon 的类型、状态、状态最新变更时间、状态变更原因以及变更的详细信息。
4. 单击**事件**页签，可查看 DaemonSet 相关的事件列表，包括事件的类型、原因、事件信息以及事件最近一次的发生时间。
5. 当监控插件启用时，单击**监控**页签，可查看 DaemonSet 的监控信息。支持设置监控查询的时间范围，以及监控信息的刷新频率。

   - 启用监控插件请参见[创建工作负载集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)中的**配置集群插件** > **配置可观测性**小节。
   - 展示的监控图表类型与工作负载集群的 `Kubernetes / Compute Resources / Workload` 监控视图下的监控图表类型一致。

## DaemonSet 相关操作

在 DaemonSet 列表页面选择 **...**，可完成如下操作；您也可以进入 DaemonSet 的详情页面执行相应操作。

- **编辑 YAML**：编辑 DaemonSet 的 YAML 配置，具体参数说明可参考[创建 DaemonSet](#%E5%88%9B%E5%BB%BA-daemonset)。
- **下载 YAML**：下载 DaemonSet 的 YAML 文件。
- **重新部署**：根据当前的配置以及更新策略，触发 DaemonSet 的重新部署。
- **删除**：对于不再需要使用的 DaemonSet，可执行删除操作。

---

## 管理工作负载集群 > 管理工作负载 > 管理 Deployment

# 管理 Deployment

[Deployment](https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/deployment/) 为 Pod 和 [ReplicaSet](https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/replicaset/) 提供声明式的更新能力，用于管理无状态应用的部署和运行，例如 Nginx。无状态应用在运行中始终不保存任何数据或状态，所有 Pod 都是相同的，可以随时替换或扩展而不会丢失数据。

## 创建 Deployment

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**工作负载** > **Deployment**。
3. 单击 **+ 创建 Deployment**。
4. **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

   ```
   apiVersion: apps/v1
   kind: Deployment    # 资源的类型，即该段 YAML 配置定义了一个 Deployment
   metadata:
     name: example    # Deployment 的名称
     namespace: default    # Deployment 所属的名字空间
   spec:
     selector:    # 选择器，用于指定哪些 Pod 由该 Deployment 管理
       matchLabels:
         app: deployment-example    # 匹配标签为 app: deployment-example 的 Pods
     replicas: 3    # 期望运行的 Pod 副本数量
     template:    # Pod 模板，定义了由 Deployment 创建的 Pods 的规格
       metadata:
         labels:
           app: deployment-example    # Pod 的标签，必须与 selector 中的标签匹配
       spec:
         containers:    # 定义 Pod 中的容器
           - name: deployment-example    # 容器的名称
             image: registry.smtx.io/kubesmart/bitnami/nginx:1.25.2-debian-11-r2    # 容器使用的镜像
             ports:
               - containerPort: 8080    # 容器暴露的端口
                 protocol: TCP    # 使用的协议
     strategy:
       type: RollingUpdate    # 更新策略类型，支持 RollingUpdate 和 Recreate
       rollingUpdate:    # 当前为滚动更新
         maxSurge: 25%    # 更新过程中最多可以额外创建 25% 的 Pod
         maxUnavailable: 25%    # 更新过程中最多可以有 25% 的 Pod 不可用
   ```

   在配置内容的右上角可复制 YAML、重置 YAML 或查看 YAML 改动。
5. 单击**创建**。

## 查看 Deployment

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**工作负载** > **Deployment**，可在列表中查看工作负载集群的所有 Deployment 信息。您可以根据一个或多个名字空间进行快速筛选。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | Deployment 的名称。 |
   | 状态 | Deployment 的状态，包括`已就绪`、`已停止`和`更新中`。 |
   | 名字空间 | Deployment 所属的名字空间。 |
   | 容器镜像 | Deployment 执行时使用的容器镜像，镜像中封装了应用程序及其所有软件依赖的二进制数据。 |
   | Pod 数量 | 展示 Pod 的`就绪数量/预期数量`。 - **Pod 就绪数量**：Deployment 需要创建和管理的 Pod 中处于就绪状态的 Pod 数量。 - **Pod 预期数量**：Deployment 需要创建和管理的 Pod 数量。 |
   | 重启次数 | Deployment 中所有 Pod 的容器自创建以来由于失败而被重新启动的总次数。 |
   | 创建时间 | Deployment 的创建时间。 |
3. 单击 Deployment 的名称链接，可查看 Deployment 的详细信息。

   - **基本信息**：除 Deployment 列表中包含的参数外，还可展示 Deployment 的标签和注解信息。
   - **Pod**：展示 Deployment 包含的 Pod 列表，具体参数说明请参见[查看 Pod](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_45#%E6%9F%A5%E7%9C%8B-pod)。
   - **状况**：展示 Deployment 的 Condition 信息，包括 Conditon 的类型、状态、状态最新变更时间、状态变更原因以及变更的详细信息。
4. 单击**事件**页签，可查看 Deployment 相关的事件列表，包括事件的类型、原因、事件信息以及事件最近一次的发生时间。
5. 当监控插件启用时，单击**监控**页签，可展示 Deployment 的监控信息。支持设置监控查询的时间范围，以及监控信息的刷新频率。

   - 启用监控插件请参见[创建工作负载集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)中的**配置集群插件** > **配置可观测性**小节。
   - 展示的监控图表类型与工作负载集群的 `Kubernetes / Compute Resources / Workload` 监控视图下的监控图表类型一致。

## Deployment 相关操作

在 Deployment 列表页面选择 **...**，可完成如下操作；您也可以进入 Deployment 的详情页面相应操作。

- **编辑 YAML**：编辑 Deployment 的 YAML 配置，具体参数说明可参考[创建 Deployment](#%E5%88%9B%E5%BB%BA-deployment)。
- **下载 YAML**：下载 Deployment 的 YAML 文件。
- **重新部署**：根据当前的配置以及更新策略，触发 Deployment 的重新部署。
- **编辑预期副本数**：编辑 Deployment 的 Pod 预期数量。
- **删除**：对于不再需要使用的 Deployment，可执行删除操作。

---

## 管理工作负载集群 > 管理工作负载 > 管理 Job

# 管理 Job

[Job](https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/job/) 会创建一个或者多个 Pod，用于管理一次性或者短暂的任务，例如生成报表、数据导入导出等。Job 可以确保任务成功完成，即使在执行过程中 Pod 可能会因故障而重新启动。

## 创建 Job

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**工作负载** > **Job**。
3. 单击 **+ 创建 Job**。
4. **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

   ```
   apiVersion: batch/v1
   kind: Job    # 资源的类型，该段 YAML 配置定义了一个 Job
   metadata:
     name: example    # Job 的名称
     namespace: default    # Job 所属的名字空间
   spec:
     selector: {}    # 选择器，用于指定该 Job 管理的 Pod
     template:    # 定义 Pod 模板
       metadata:
         name: job-example    # Pod 的名称
       spec:    # Pod 的详细规格
         containers:
           - name: job-example    # 容器的名称
             image: registry.smtx.io/kubesmart/alpine:3    # 容器使用的镜像
             command:     # 容器启动时执行的命令和参数
               - /bin/sh
               - '-c'
               - date; echo Hello from the Kubernetes cluster
         restartPolicy: Never    # 容器的重启策略，当前表示容器在终止后不应自动重启
   ```

   在配置内容的右上角可复制 YAML、重置 YAML 或查看 YAML 改动。
5. 单击**创建**。

## 查看 Job

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**工作负载** > **Job**，可在列表中查看工作负载集群的所有 Job 信息。您可以根据一个或多个名字空间进行快速筛选。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | Job 的名称。 |
   | 状态 | Job 的状态，包括`运行中`、`已挂起`、`已完成`和`异常`。 |
   | 名字空间 | Job 所属的名字空间。 |
   | 容器镜像 | Job 执行时使用的容器镜像，镜像中封装了应用程序及其所有软件依赖的二进制数据。 |
   | Pod 数量 | 展示 Pod 的`已完成数量/预期数量`。 - **Pod 已完成数量**：Job 中已成功运行的 Pod 数量。 - **Pod 预期数量**：Job 需要成功运行的 Pod 数量。 |
   | 重启次数 | Job 中所有 Pod 的容器自创建以来由于失败而被重新启动的总次数。 |
   | 持续时间 | Job 的持续时间。 |
   | 创建时间 | Job 的创建时间。 |
3. 单击 Job 的名称链接，可查看 Job 的详细信息。

   - **基本信息**：除 Job 列表中包含的参数外，还可展示 Job 的标签和注解信息。
   - **Pod**：展示 Job 包含的 Pod 列表，具体参数说明请参见[查看 Pod](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_45#%E6%9F%A5%E7%9C%8B-pod)。
   - **状况**：展示 Job 的 Condition 信息，包括 Conditon 的类型、状态、状态最新变更时间、状态变更原因以及变更的详细信息。
4. 单击**事件**页签，可查看 Job 相关的事件列表，包括事件的类型、原因、事件信息以及事件最近一次的发生时间。

## Job 相关操作

在 Job 列表页面选择 **...**，可完成如下操作；您也可以进入 Job 的详情页面执行相应操作。

- **编辑 YAML**：编辑 Job 的 YAML 配置，具体参数说明可参考[创建 Job](#%E5%88%9B%E5%BB%BA-job)。
- **下载 YAML**：下载 Job 的 YAML 文件。
- **删除**：对于不再需要使用的 Job，可执行删除操作。

---

## 管理工作负载集群 > 管理工作负载 > 管理 StatefulSet

# 管理 StatefulSet

[StatefulSet](https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/statefulset/) 用于管理有状态应用的部署和运行，例如 MySQL。与无状态应用不同，有状态应用在运行过程中会保存数据或状态。

StatefulSet 为每个 Pod 维护了一个有粘性的 ID，无论怎么调度，每个 Pod 都有一个永久不变的 ID，从而保证每个 Pod 都能保持其数据和状态。

## 创建 StatefulSet

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**工作负载** > **StatefulSet**。
3. 单击 **+ 创建 StatefulSet**。
4. **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

   ```
   apiVersion: apps/v1
   kind: StatefulSet    # 资源的类型，即该段 YAML 配置定义了一个 StatefulSet
   metadata:
     name: example    # StatefulSet 的名称
     namespace: default    # StatefulSet 所属的名字空间
   spec:
     serviceName: statefulset-example    # 指定了由 StatefulSet 管理的 Pod 的服务名称  
     replicas: 3    # 期望运行的 Pod 副本数量
     selector:    # 选择器，用于指定哪些 Pod 由该 StatefulSet 管理
       matchLabels:
         app: statefulset-example    # 匹配标签为 app: statefulset-example 的 Pods
     template:    # Pod 模板，定义了由 StatefulSet 创建的 Pods 的规格
       metadata:
         labels:
           app: statefulset-example    # 匹配标签为 app: statefulset-example 的 Pods
       spec:
         terminationGracePeriodSeconds: 10   # Pod 的终止宽限期
         containers:
           - name: statefulset-example     # 容器的名称
             image: registry.smtx.io/kubesmart/fileserver:v1.0.0     # 容器使用的镜像
             command:    # 容器启动时执行的命令
               - dufs
             args:    # 传递给容器的参数
               - '-A'
               - '--render-try-index'
               - /data
             ports:
               - containerPort: 5000    # 容器暴露的端口
                 name: http    # 端口的名称
             volumeMounts:
               - name: file    # 挂载的卷的名称
                 mountPath: /data    # 挂载到容器内部的路径
     volumeClaimTemplates:    # 定义了 StatefulSet 使用的持久化存储卷的规格
       - metadata:
           name: file    # 持久化存储卷的名称
         spec:
           accessModes:    # 卷的访问模式
             - ReadWriteOnce    
           resources:    # 卷请求的存储空间
             requests:
               storage: 1Gi
   ```

   在配置内容的右上角可复制 YAML、重置 YAML 或查看 YAML 改动。
5. 单击**创建**。

## 查看 StatefulSet

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**工作负载** > **StatefulSet**，可在列表中查看工作负载集群的所有 StatefulSet 信息。您可以根据一个或多个名字空间进行快速筛选。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | StatefulSet 的名称。 |
   | 状态 | StatefulSet 的状态，包括`已就绪`、`已停止`和`更新中`。 |
   | 名字空间 | StatefulSet 所属的名字空间。 |
   | 容器镜像 | StatefulSet 执行时使用的容器镜像，镜像中封装了应用程序及其所有软件依赖的二进制数据。 |
   | Pod 数量 | 展示 Pod 的`就绪数量/预期数量`。 - **Pod 就绪数量**：StatefulSet 需要创建和管理的 Pod 中处于就绪状态的 Pod 数量。 - **Pod 预期数量**：StatefulSet 需要创建和管理的 Pod 数量。 |
   | 重启次数 | StatefulSet 中所有 Pod 的容器自创建以来由于失败而被重新启动的总次数。 |
   | 创建时间 | StatefulSet 的创建时间。 |
3. 单击 StatefulSet 的名称链接，可查看 StatefulSet 的详细信息。

   - **基本信息**：除 StatefulSet 列表中包含的参数外，还可展示 StatefulSet 的标签和注解信息。
   - **Pod**：展示 StatefulSet 包含的 Pod 列表，具体参数说明请参见[查看 Pod](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_45#%E6%9F%A5%E7%9C%8B-pod)。
   - **状况**：展示 StatefulSet 的 Condition 信息，包括 Conditon 的类型、状态、状态最新变更时间、状态变更原因以及变更的详细信息。
4. 单击**事件**页签，可查看 StatefulSet 相关的事件列表，包括事件的类型、原因、事件信息以及事件最近一次的发生时间。
5. 当监控插件启用时，单击**监控**页签，可展示 StatefulSet 的监控信息。支持设置监控查询的时间范围，以及监控信息的刷新频率。

   - 启用监控插件请参见[创建工作负载集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)中的**配置集群插件** > **配置可观测性**小节。
   - 展示的监控图表类型与工作负载集群的 `Kubernetes / Compute Resources / Workload` 监控视图下的监控图表类型一致。

## StatefulSet 相关操作

在 StatefulSet 列表页面选择 **...**，可完成如下操作；您也可以进入 StatefulSet 的详情页面执行相应操作。

- **编辑 YAML**：编辑 StatefulSet 的 YAML 配置，具体参数说明可参考[创建 StatefulSet](#%E5%88%9B%E5%BB%BA-statefulset)。
- **下载 YAML**：下载 StatefulSet 的 YAML 文件。
- **重新部署**：根据当前的配置以及更新策略，触发 StatefulSet 的重新部署。
- **编辑预期副本数**：编辑 StatefulSet 的 Pod 预期数量。
- **删除**：对于不再需要使用的 StatefulSet，可执行删除操作。

---

## 管理工作负载集群 > 管理工作负载 > 管理 Pod

# 管理 Pod

[Pod](https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/) 是 Kubernetes 中创建和管理的最小可部署计算单元，代表了一个独立的应用程序运行实例，该实例可能由单个容器或者几个紧耦合在一起的容器组成。通常，Pod 不是直接创建的，而是通过工作负载资源（如 Deployment、StatefulSet）来创建和管理。

## 创建 Pod

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**工作负载** > **Pod**。
3. 单击 **+ 创建 Pod**。
4. **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

   ```
   apiVersion: v1
   kind: Pod    # 资源的类型，即该段 YAML 配置定义了一个 Pod
   metadata:
     name: example    # Pod 的名称
     namespace: default    # Pod 所属的名字空间
     labels:    # Pod 的标签
       app: example    # 定义了一个标签 app: example 
   spec:    # 定义了 Pod 的规格
     securityContext:    # Pod 的安全设置
       runAsNonRoot: true    # 指定容器中的进程以非 root 用户身份运行
       seccompProfile:    # 配置容器的 seccomp 策略
         type: RuntimeDefault
     containers:
       - name: example    # 容器的名称
         image: registry.smtx.io/kubesmart/bitnami/nginx:1.25.2-debian-11-r2    # 容器使用的镜像
         ports:
           - containerPort: 8080    # 容器暴露的端口
         securityContext:    # 容器的安全设置
           allowPrivilegeEscalation: false    # 是否允许容器内的进程获得比其父进程更高的特权
           capabilities:    # 容器的 Linux 容器功能设置
             drop:    # 指定要从容器中删除的 Linux 容器功能列表
               - ALL    # 移除所有特权功能
   ```

   在配置内容的右上角可复制 YAML、重置 YAML 或查看 YAML 改动。

   **说明**：

   当工作负载集群使用 EIC 插件时，您可以通过设置 `annotations` 为 Pod 指定需要使用的 IP 池，并按需分配静态 IP。

   ```
   metadata:
     annotations:
       ipam.everoute.io/pool: my-ip-pool  # 指定 IP 池名称
       ipam.everoute.io/static-ip: "192.168.1.10"  # 为 Pod 从 IP 池中指定静态 IP
   ```

   指定静态 IP 地址时，需要同时配置 `ipam.everoute.io/pool` 和 `ipam.everoute.io/static-ip`；若只配置 `ipam.everoute.io/pool`，则会从指定 IP 池中随机分配 IP。
5. 单击**创建**。

## 查看 Pod

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**工作负载** > **Pod**，可在列表中查看工作负载集群的所有 Pod 信息，您可以根据一个或多个名字空间进行快速筛选。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | Pod 的名称。 |
   | 状态 | Pod 的状态，包括`运行中`、`未知`、`已成功终止`、`待处理`、`终止中`和`异常`。 |
   | 名字空间 | Pod 所属的名字空间。 |
   | 容器镜像 | Pod 执行时使用的容器镜像，镜像中封装了应用程序及其所有软件依赖的二进制数据。 |
   | 容器数量 | 展示容器的`就绪数量/预期数量`。 - **容器就绪数量**：Pod 中已就绪的容器数量。 - **容器预期数量**：Pod 预期的容器数量。 |
   | IP 地址 | Pod 的 IP 地址。 |
   | 所属节点 | Pod 所属节点的名称。单击节点名称链接，可跳转至节点详情页面。 单击节点名称后的控制台图标，可[打开节点控制台](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_114)对节点进行运维操作。 |
   | 工作负载 | Pod 所属的工作负载，即通过哪个工作负载创建而来。  如为 SKS 已支持的工作负载，则单击工作负载的名称链接，可跳转至工作负载的详情页面。 |
   | 重启次数 | Pod 的所有容器自创建以来由于失败而被重新启动的总次数。 |
   | 创建时间 | Pod 的创建时间。 |
3. 单击 Pod 的名称链接，可查看 Pod 的详细信息。

   - **基本信息**：除 Pod 列表中包含的参数外，还可展示 Pod 的标签和注解信息。
   - **容器**：展示 Pod 包含的容器列表。

     | 参数 | 描述 |
     | --- | --- |
     | 名称 | 容器的名称。 |
     | 状态 | 容器的状态，包括`运行中`、`等待中`和`已终止`。 |
     | 容器镜像 | 容器使用的镜像，镜像中封装了应用程序及其所有软件依赖的二进制数据。 |
     | 类型 | 容器的类型，包括`普通容器`和`初始化容器`。 |
     | 重启次数 | 容器自创建以来由于失败而被重新启动的总次数。 |
     | 创建时间 | 容器的创建时间。 |
   - **持久卷申领**：展示 Pod 中使用的持久卷申领列表，具体参数说明请参见[查看持久卷申领](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_55#%E6%9F%A5%E7%9C%8B%E6%8C%81%E4%B9%85%E5%8D%B7%E7%94%B3%E9%A2%86)。
   - **状况**：展示 Pod 的 Condition 信息，包括 Conditon 的类型、状态、状态最新变更时间、状态变更原因以及变更的详细信息。
4. 单击**事件**页签，可查看 Pod 相关的事件列表，包括事件的类型、原因、事件信息以及事件最近一次的发生时间。
5. 当监控插件启用时，单击**监控**页签，可展示 Pod 的监控信息。支持设置监控查询的时间范围，以及监控信息的刷新频率。

   - 启用监控插件请参见[创建工作负载集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)中的**配置集群插件** > **配置可观测性**小节。
   - 展示的监控图表类型与工作负载集群的 `Kubernetes / Compute Resources / Pod` 监控视图下的监控图表类型一致。
6. 单击**日志**页签，可查看 Pod 中所有容器的日志。

   支持如下操作：

   - 切换查看容器的**实时日志**或**上次启动日志**
   - 切换容器
   - 日志自动换行
   - 暂停或恢复日志打印

## 打开 Pod 控制台

您可以在 Pod 控制台中使用命令行查看特定容器中的进程信息，并进入指定容器中进行应用级别的调试，例如进行网络连通性验证、服务链路调试、环境变量校验。

**前提条件**

目标 Pod 处于`运行中`状态。

**注意事项**

Pod 控制台可能由于用户的镜像没有 bash/sh 等 shell 而导致打开失败。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**工作负载** > **Pod**，然后在 Pod 列表中单击某一 Pod，进入 Pod 的**详情**页面。
3. 在**详情**页面右上方单击 **Pod 控制台**，此时在界面下方将弹出当前 Pod 的控制台窗口。窗口名称为 `pod: pod 名称`，将鼠标悬浮在名称右侧的信息图标 i 时可查看所属集群名称，您还可以在窗口右上角对窗口执行展开/收起、全屏/退出全屏、新建窗口、关闭窗口操作。
4. 在控制台窗口中执行命令管理 Pod 中的容器。您还可以在控制台中执行以下操作：

   - 在窗口右上角搜索控制台中的命令、调整字体大小、上传/下载文件、下载控制台日志、清空命令行。
   - 窗口左上角的下拉框中选择当前 Pod 中的其他容器进入对应的控制台窗口。

## Pod 相关操作

在 Pod 列表页面选择 **...**，可完成如下操作；您也可以进入 Pod 的详情页面执行相应操作。

- **编辑 YAML**：编辑 Pod 的 YAML 配置，具体参数说明可参考[创建 Pod](#%E5%88%9B%E5%BB%BA-pod)。
- **下载 YAML**：下载 Pod 的 YAML 文件。
- **上传文件**：上传文件到 Pod 中的指定容器。仅当 Pod 处于`运行中`状态时，才支持该操作。
- **下载文件**：下载 Pod 中指定容器的文件。仅当 Pod 处于`运行中`状态时，才支持该操作。
- **删除**：对于不再需要使用的 Pod，可执行删除操作。

---

## 管理工作负载集群 > 管理服务与网络

# 管理服务与网络

[服务与网络](https://kubernetes.io/zh-cn/docs/concepts/services-networking/)是在 Kubernetes 集群中管理应用程序之间以及应用程序与外部系统之间通信的机制。您可以按需创建并管理 Ingress、Service 和 NetworkPolicy，以确保应用程序的高效、可靠和安全的运行。

---

## 管理工作负载集群 > 管理服务与网络 > 管理 Ingress

# 管理 Ingress

[Ingress](https://kubernetes.io/zh-cn/docs/concepts/services-networking/ingress/) 是对集群中服务的外部访问进行管理的 API 对象，提供从集群外部到集群内服务的 HTTP 和 HTTPS 路由。

使用 Ingress 前必须先安装 Ingress 控制器，您可以使用 SKS 提供的 Contour 插件作为 Ingress 控制器，具体操作请参见[启用 Ingress 控制器](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_19#%E5%90%AF%E7%94%A8-ingress-%E6%8E%A7%E5%88%B6%E5%99%A8)。

## 创建 Ingress

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**服务与网络** > **Ingress**。
3. 单击 **+ 创建 Ingress**。
4. **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

   ```
   apiVersion: networking.k8s.io/v1
   kind: Ingress    # 资源的类型，即该段 YAML 配置定义了一个 Ingress
   metadata:
     name: example    # Ingress 的名称
     namespace: default    # Ingress 所属的名字空间
   spec:
     rules:    # Ingress 的规则
       - host: example.com    # 指定处理的主机名
         http:    # HTTP 路由
           paths:
             - path: /testpath    # 指定匹配的路径
               pathType: Prefix    # 路径的类型
               backend:    # 后端服务
                 service:    
                   name: test    # 服务的名称
                   port:
                     number: 80    # 服务的端口号
   ```

   在配置内容的右上角可复制 YAML、重置 YAML 或查看 YAML 改动。
5. 单击**创建**。

## 查看 Ingress

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**服务与网络** > **Ingress**，可在列表中查看工作负载集群的所有 Ingress 信息。您可以根据一个或多个名字空间进行快速筛选。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | Ingress 的名称。 |
   | 名字空间 | Ingress 所属的名字空间。 |
   | 规则 | Ingress 的流量转发规则，包含请求端和目标端。  单击请求端或目标端的链接可跳转至相应页面。 |
   | 默认后端 | Ingress 是否配置默认后端 `defaultBackend`。  配置后未匹配任何 Ingress 规则的请求将被路由至默认后端服务。 |
   | Ingress 类 | Ingress 类用于定义 Ingress 资源应由哪个特定的 Ingress 控制器来管理。  同一个 Kubernetes 集群中可以并行运行多个不同类型的 Ingress 控制器，每个控制器负责处理特定的 Ingress 配置和路由规则。 |
   | 创建时间 | Ingress 的创建时间。 |
3. 单击 Ingress 的名称链接，可查看 Ingress 的详细信息。

   - **基本信息**：除 Ingress 列表中包含的参数外，还可展示 Ingress 的标签和注解信息。
   - **规则**：展示 Ingress 中设置的流量转发规则。每条规则包含的参数如下表所示。

     | 参数 | 描述 |
     | --- | --- |
     | 路径类型 | 用于指定路径匹配的方式。  - `ImplementationSpecific`：匹配方式取决于 Ingress 类。 - `Exact`：精确匹配 URL 路径。 - `Prefix`：基于以 `/` 分隔的 URL 路径前缀匹配。 |
     | 路径 | 用于指定匹配的路径，形式为 URL，单击可支持跳转。 |
     | 后端 | 用于指定请求匹配到路径规则后，应该路由到的后端服务，单击可支持跳转。  后端包括 Service 和 Resource 两种类型，不可同时配置。 |
     | 端口 | 当后端类型为 Service 时，可展示后端端口号。 |
     | Secret | 用于配置 TLS 协议的证书名称，在 Ingress 中引用对应的 Secret 即可提供安全的 HTTPS 访问，单击可支持跳转。 |

## Ingress 相关操作

在 Ingress 列表页面选择 **...**，可完成如下操作；您也可以进入 Ingress 的详情页面执行相应操作。

- **编辑 YAML**：编辑 Ingress 的 YAML 配置，具体参数说明可参考[创建 Ingress](#%E5%88%9B%E5%BB%BA-ingress)。
- **下载 YAML**：下载 Ingress 的 YAML 文件。
- **删除**：对于不再需要使用的 Ingress，可执行删除操作。

---

## 管理工作负载集群 > 管理服务与网络 > 管理 NetworkPolicy

# 管理 NetworkPolicy

[NetworkPolicy](https://kubernetes.io/zh-cn/docs/concepts/services-networking/network-policies/) 是一种以应用为中心的结构，用于设置如何允许 Pod 与网络上的各类网络实体通信。

NetworkPolicy 支持的能力取决于集群的网络插件的能力，在创建工作负载集群时您可以按需启用 EIC 或 Calico CNI 插件。默认情况下，如果名字空间中不存在任何网络策略，则所有进出该名字空间的 Pod 流量都将被允许。

> **注意**：
>
> 当工作负载集群使用 EIC 插件，且配套的 Everoute 为 3.2.0 及以上版本时，推荐使用 Everoute 的 Pod 安全策略。支持统一配置 Pod 和虚拟机的安全策略，还可以通过流量可视化预览策略配置情况和查看 Pod 流量信息。如需使用 NetworkPolicy，请避免同时启用 Everoute 的 Pod 安全策略。

## 创建 NetworkPolicy

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**服务与网络** > **NetworkPolicy**。
3. 单击 **+ 创建 NetworkPolicy**。
4. **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

   ```
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy    # 资源的类型，即该段 YAML 配置定义了一个 NetworkPolicy
   metadata:
     name: example    # NetworkPolicy 的名称
     namespace: default    # NetworkPolicy 所属的名字空间
   spec:    # 定义网络策略的规格
     podSelector: {}    # 标签选择器，用于设置 NetworkPolicy 对哪些 Pods 生效
     policyTypes: []    # 网络策略类型，支持 Ingress、Egress 或二者同时配置
   ```

   在配置内容的右上角可复制 YAML、重置 YAML 或查看 YAML 改动。
5. 单击**创建**。

## 查看 NetworkPolicy

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**服务与网络** > **NetworkPolicy**，可在列表中查看工作负载集群的所有 NetworkPolicy 信息。您可以根据一个或多个名字空间进行快速筛选。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | NetworkPolicy 的名称。 |
   | 名字空间 | NetworkPolicy 所属的名字空间。 |
   | Pod 选择算符 | 指定 NetworkPolicy 对哪些 Pod 生效。 |
   | 创建时间 | NetworkPolicy 的创建时间。 |
3. 单击 NetworkPolicy 的名称链接，可查看 NetworkPolicy 的详细信息。

   - **基本信息**：除 NetworkPolicy 列表中包含的参数外，还可展示 NetworkPolicy 的标签和注解信息。
   - **Pod 选择算符**：NetworkPolicy 通过设置 Pod 关联的标签键值对来选择一组 Pod，展示 NetworkPolicy 所设置的标签键值对。
   - **Ingress 规则**：通过 YAML 定义 Pod 的入站流量规则。

     示例如下：

     ```
     - from:    # 定义允许入站流量的来源
       - ipBlock:    # 来源为特定的 IP 地址块
           cidr: 172.17.0.0/16   # 允许来自该 CIDR 范围的流量
           except:    # 排除以下子网范围
           - 172.17.1.0/24
       - namespaceSelector:    # 来源为特定的名字空间
           matchLabels:
             project: myproject    # 允许来自带有标签 project=myproject 的名字空间的流量
       - podSelector:   # 来源为特定的 Pod
           matchLabels:
             role: frontend    # 允许来自带有标签 role=frontend 的 Pods 的流量
       ports:
         - protocol: TCP    # 允许的协议类型
           port: 6379    # 允许的端口号
     ```
   - **Egress 规则**：通过 YAML 定义 Pod 的出站流量规则。

     示例如下：

     ```
     - to:    # 定义允许出站流量的目标
       - ipBlock:    # 目标为特定的 IP 地址块
           cidr: 10.0.0.0/24    # 允许流向该 CIDR 范围的流量
       ports:
         - protocol: TCP    # 允许的协议类型
           port: 5978    # 允许的端口号
     ```

## NetworkPolicy 相关操作

在 NetworkPolicy 列表页面选择 **...**，可完成如下操作；您也可以进入 NetworkPolicy 的详情页面执行相应操作。

- **编辑 YAML**：编辑 NetworkPolicy 的 YAML 配置，具体参数说明可参考[创建 NetworkPolicy](#%E5%88%9B%E5%BB%BA-networkpolicy)。
- **下载 YAML**：下载 NetworkPolicy 的 YAML 文件。
- **删除**：对于不再需要使用的 NetworkPolicy，可执行删除操作。

---

## 管理工作负载集群 > 管理服务与网络 > 管理 Service

# 管理 Service

[Service](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/) 提供一种抽象的方法，将运行在一个或一组 Pod 上的应用程序公开为网络服务。

Service 有多种类型，如 ClusterIP、NodePort 和 LoadBalancer，不同类型的 Service 用于满足不同的网络访问需求，例如在集群内部、集群外部或负载均衡器之间分发流量，从而实现高可用性和可扩展性。

## 创建 Service

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**服务与网络** > **Service**。
3. 单击 **+ 创建 Service**。
4. **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

   ```
   apiVersion: v1
   kind: Service    # 资源的类型，即该段 YAML 配置定义了一个 Service
   metadata:
     name: example    # Service 的名称
     namespace: default    # Service 所属的名字空间
   spec:
     selector:    # 定义该 Service 选择的 Pod 标签
       app: example    # 选择带有标签 app=example 的 Pods
     ports:    # 定义 Service 暴露的端口
       - name: example    # 端口名称
         port: 8080    # Service 暴露的端口号
         protocol: TCP    # 使用的协议
         targetPort: 8080    # 目标 Pods 上的端口号
     sessionAffinity: None    # 会话亲和性配置
     type: ClusterIP    # Service 的类型，ClusterIP 表示仅在集群内部可访问
   ```

   在配置内容的右上角可复制 YAML、重置 YAML 或查看 YAML 改动。

   > **注意**：
   >
   > 当工作负载集群使用 EIC 插件时，不支持配置 `externalTrafficPolicy` 属性。
5. 单击**创建**。

## 查看 Service

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**服务与网络** > **Service**，可在列表中查看工作负载集群的所有 Service 信息。您可以根据一个或多个名字空间进行快速筛选。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | Service 的名称。 |
   | 名字空间 | Service 所属的名字空间。 |
   | 类型 | Service 的类型。  - `ClusterIP`：用于在集群内部互相访问的场景，通过 ClusterIP 访问 Service。 - `NodePort`：用于从集群外部访问的场景，通过节点上的端口访问 Service。 - `LoadBalancer`：用于从集群外部访问的场景，通过一个特定的 LoadBalancer 访问 Service。 - `ExternalName`：用于将集群内的 Service 映射到集群外部的 DNS 名称。该类型的 Service 不会分配 ClusterIP，也不提供负载均衡功能，而是通过返回配置的外部 DNS 名称来解析访问请求。 - `Headless`：用于 Pod 间的互相发现，该类型的 Service 并不会分配单独的 ClusterIP，集群也不会进行负载均衡和路由。 |
   | DNS 记录 | 用于提供 Service 发现和解析的功能，格式为 `Service 名称.名字空间名称`。 |
   | 集群内访问方式 | 在集群内部访问 Service 的方式。  - 当 Service 类型为 `ClusterIP`、`NodePort` 或 `LoadBalancer` 时，展示集群的 Cluster IP。 - 当 Service 类型为 `ExternalName` 时，展示 DNS 记录。 - 当 Service 类型为 `Headless` 时，展示 `-`。 |
   | 集群外访问方式 | 从集群外部访问集群内的 Service 的方式。  - 当 Service 类型为 `ClusterIP` 时，展示`不支持`。 - 当 Service 类型为 `NodePort` 时，展示`集群 VIP:nodeport`，单击链接可访问服务。 - 当 Service 类型为 `LoadBalancer` 时，展示 `ingress[*].ip`。 - 当 Service 类型为 `ExternalName` 时，展示 `external-ip`。 |
   | Pod 选择算符 | 通过标签选择提供 Service 的 Pod。 |
   | 端口映射 | 展示 Service 端口与 Pod 端口的映射关系，以及使用的协议。 |
   | 创建时间 | Service 的创建时间。 |
3. 单击 Service 的名称链接，可查看 Service 的详细信息。

   - **基本信息**：除 Service 列表中包含的参数外，还可展示 Service 的标签和注解信息。
   - **Pod**：展示 Service 包含的 Pod 列表，具体参数说明请参见[查看 Pod](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_45#%E6%9F%A5%E7%9C%8B-pod)。
   - **端口**：展示 Service 端口与 Pod 端口的映射信息。

     | 参数 | 描述 |
     | --- | --- |
     | 名称 | Service 端口的名称。 |
     | Service 端口 | Service 暴露的端口号。 |
     | 协议 | Service 使用的协议。 |
     | Pod 端口 | 目标 Pod 上的端口号。 |
     | NodePort | `NodePort` 类型 Service 的外部端口。 |
   - **状况**：展示 Service 的 Condition 信息，包括 Conditon 的类型、状态、状态最新变更时间、状态变更原因以及变更的详细信息。
   - **Pod 选择算符**：展示 Pod 选择算符的**键**和**值**。
4. 当监控功能和 Ingress 控制器插件已启用时，单击**监控**页签，可展示 Service 的监控信息。支持设置监控查询的时间范围，以及监控信息的刷新频率。

   - 启用监控功能请参见[创建工作负载集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)中的**配置可观测性**小节。
   - 展示的监控图表类型与工作负载集群的 Contour Ingress Metrics 监控视图下的监控图表类型一致。

## Service 相关操作

在 Service 列表页面选择 **...**，可完成如下操作；您也可以进入 Service 的详情页面执行相应操作。

- **编辑 YAML**：编辑 Service 的 YAML 配置，具体参数说明可参考[创建 Service](#%E5%88%9B%E5%BB%BA-service)。
- **下载 YAML**：下载 Service 的 YAML 文件。
- **删除**：对于不再需要使用的 Service，可执行删除操作。

---

## 管理工作负载集群 > 管理配置

# 管理配置

[配置](https://kubernetes.io/zh-cn/docs/concepts/configuration/)是指管理和存储应用程序设置、参数和其他信息的机制。您可以按需创建并管理 ConfigMap 和 Secret，以确保应用程序在不同环境中的一致性以及敏感信息的安全性。

---

## 管理工作负载集群 > 管理配置 > 管理 ConfigMap

# 管理 ConfigMap

[ConfigMap](https://kubernetes.io/zh-cn/docs/concepts/configuration/configmap/) 用来将非机密性的数据保存到键值对中。常用于存储工作负载所需的配置信息，应用程序会从配置文件、命令行参数或环境变量中读取相应配置。

## 创建 ConfigMap

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**配置** > **ConfigMap**。
3. 单击 **+ 创建 ConfigMap**。
4. **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

   ```
   apiVersion: v1
   kind: ConfigMap    # 资源的类型，即该段 YAML 配置定义了一个 ConfigMap
   metadata:
     name: example    # ConfigMap 的名称
     namespace: default    # ConfigMap 所属的名字空间
   data:
     key: value    # 存储的配置信息，以键值对形式表示
   immutable: false    # 是否将 ConfigMap 设置为不可变，false 表示可变
   ```

   在配置内容的右上角可复制 YAML、重置 YAML 或查看 YAML 改动。
5. 单击**创建**。

## 查看 ConfigMap

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**配置** > **ConfigMap**，可在列表中查看工作负载集群的所有 ConfigMap 信息。您可以根据一个或多个名字空间进行快速筛选。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | ConfigMap 的名称。 |
   | 名字空间 | ConfigMap 所属的名字空间。 |
   | 数据 | ConfigMap 的配置信息，展示键值对中的 `key` 值。 |
   | 创建时间 | ConfigMap 的创建时间。 |
3. 单击 ConfigMap 的名称链接，可查看 ConfigMap 的详细信息。

   - **基本信息**：除 ConfigMap 列表中包含的参数外，还可展示 ConfigMap 的标签和注解信息。
   - **数据**：展示键值对中 `key` 和 `value` 的值。

## ConfigMap 相关操作

在 ConfigMap 列表页面选择 **...**，可完成如下操作；您也可以进入 ConfigMap 的详情页面执行相应操作。

- **编辑 YAML**：编辑 ConfigMap 的 YAML 配置，具体参数说明可参考[创建 ConfigMap](#%E5%88%9B%E5%BB%BA-configmap)。
- **下载 YAML**：下载 ConfigMap 的 YAML 文件。
- **删除**：对于不再需要使用的 ConfigMap，可执行删除操作。

---

## 管理工作负载集群 > 管理配置 > 管理 Secret

# 管理 Secret

[Secret](https://kubernetes.io/zh-cn/docs/concepts/configuration/secret/) 是一种包含少量敏感信息，例如密码、令牌或密钥的对象。使用 Secret 意味着不需要在应用程序代码中包含机密数据，从而提高安全性。

## 创建 Secret

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**配置** > **Secret**。
3. 单击 **+ 创建 Secret**。
4. **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

   ```
   apiVersion: v1
   kind: Secret    # 资源的类型，即该段 YAML 配置定义了一个 Secret
   metadata:
     name: example    # Secret 的名称
     namespace: default    # Secret 所属的名字空间
   type: Opaque    # Secret 的类型，Opaque 表示任意二进制数据或文本
   data:
     key: value    # 存储的配置信息，以键值对形式表示
   ```

   在配置内容的右上角可复制 YAML、重置 YAML 或查看 YAML 改动。
5. 单击**创建**。

## 查看 Secret

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**配置** > **Secret**，可在列表中查看工作负载集群的所有 Secret 信息。您可以根据一个或多个名字空间进行快速筛选。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | Secret 的名称。 |
   | 名字空间 | Secret 所属的名字空间。 |
   | 类型 | Secret 的类型，如 `Opaque`、`kubernetes.io/basic-auth` 等。 |
   | 数据 | Secret 的配置信息，展示键值对中的 `key` 值。 |
   | 创建时间 | Secret 的创建时间。 |
3. 单击 Secret 的名称链接，可查看 Secret 的详细信息。

   - **基本信息**：除 Secret 列表中包含的参数外，还可展示 Secret 的标签和注解信息。
   - **数据**：展示键值对中 `key` 和 `value` 的值。其中，`value` 默认为加密状态，您可以单击**显示数值**以查看具体的 `value` 值，之后也可以再次**隐藏数值**。

## Secret 相关操作

在 Secret 列表页面选择 **...**，可完成如下操作；您也可以进入 Secret 的详情页面执行相应操作。

- **编辑 YAML**：编辑 Secret 的 YAML 配置，具体参数说明可参考[创建 Secret](#%E5%88%9B%E5%BB%BA-secret)。
- **下载 YAML**：下载 Secret 的 YAML 文件。
- **删除**：对于不再需要使用的 Secret，可执行删除操作。

---

## 管理工作负载集群 > 管理存储

# 管理存储

工作负载集群的存储资源包含持久卷、持久卷申领和存储类。

---

## 管理工作负载集群 > 管理存储 > 管理持久卷

# 管理持久卷

[持久卷](https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes/)是集群中的一块存储，为集群层面的资源。

持久卷的创建有动态创建和静态创建两种方式。动态创建是指通过创建持久卷申领的方式间接创建出所需要的持久卷，此方式必须使用存储类；静态创建是指管理员事先制备好持久卷，然后与持久卷申领进行绑定使用。

## 创建持久卷

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**存储** > **持久卷**。
3. 单击 **+ 创建持久卷**。
4. **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

   ```
   apiVersion: v1
   kind: PersistentVolume    # 资源的类型，该段 YAML 配置定义了一个持久卷
   metadata:
     name: pvc-hostpath    # 持久卷的名称
   spec:
     accessModes:
       - ReadWriteOnce    # 持久卷的访问模式
     capacity:
       storage: 10Gi    # 持久卷的容量
     hostPath:
       type: DirectoryOrCreate    # 持久卷的类型
       path: /root/test    # 持久卷的路径
     persistentVolumeReclaimPolicy: Delete    # 回收策略
     volumeMode: Filesystem    # 卷模式
   ```

   在配置内容的右上角可复制 YAML、重置 YAML 或查看 YAML 改动。
5. 单击**创建**。

## 查看持久卷

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**存储** > **持久卷**，可在列表中查看工作负载集群的所有持久卷信息。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | 持久卷的名称。 |
   | 状态 | 持久卷的状态，包括`可用`、`已绑定`、`待处理`、`失败`和`已释放`。 |
   | 持久卷申领 | 持久卷对应的持久卷申领的名称。单击名称链接，可跳转至持久卷申领详情页面。 |
   | 访问模式 | 持久卷的访问模式，支持的访问模式与所选存储类对应的 CSI 和所选卷模式有关，如下： - SMTX ZBS CSI   - 文件系统：ReadWriteOnce   - 块：ReadWriteOnce、ReadWriteMany、​ReadOnlyMany - SMTX ELF CSI   - 文件系统：ReadWriteOnce、ReadOnlyMany   - 块：ReadWriteOnce、ReadWriteMany、​ReadOnlyMany |
   | 容量 | 持久卷的存储容量，单位为 Mi、Gi 或 Ti。 |
   | CSI driver | 持久卷使用的 CSI 驱动名称，用于标识存储插件。系统内置 `com.smartx.elf-csi-driver` 和 `com.smartx.zbs-csi-driver`。 |
   | 存储类 | 持久卷所属的存储类名称，用于定义持久卷的制备方式。单击名称链接，可跳转至存储类详情页面。 |
   | 卷模式 | 持久卷的存储模式，包括： - `文件系统`：以文件系统形式挂载。 - `块`：以块设备形式挂载。 |
   | 创建时间 | 持久卷的创建时间。 |
3. 单击持久卷的名称链接，可查看持久卷的详细信息。除持久卷列表中包含的参数外，还可展示持久卷的标签和注解信息。
4. 单击**事件**页签，可查看持久卷相关的事件列表，包括事件的类型、原因、事件信息以及事件最近一次的发生时间。

## 持久卷相关操作

在持久卷列表页面选择 **...**，可完成如下操作；您也可以进入持久卷的详情页面执行相应操作。

- **编辑 YAML**：编辑持久卷的 YAML 配置，具体参数说明可参考[创建持久卷](#%E5%88%9B%E5%BB%BA%E6%8C%81%E4%B9%85%E5%8D%B7)。
- **下载 YAML**：下载持久卷的 YAML 文件。
- **删除**：对于不再需要使用的持久卷，可执行删除操作。

---

## 管理工作负载集群 > 管理存储 > 管理持久卷申领

# 管理持久卷申领

[持久卷申领](https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes/)表达对存储的特定请求，例如大小、访问模式等。持久卷申领会耗用持久卷资源。

## 创建持久卷申领

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**存储** > **持久卷申领**。
3. 单击 **+ 创建持久卷申领**。
4. 在弹出的**创建持久卷申领**对话框中，配置持久卷申领。

   - 通过**表单**创建

     | 参数 | 描述 |
     | --- | --- |
     | 名称 | 输入持久卷申领的名称。 |
     | 名字空间 | 选择需要使用该持久卷的应用所在的名字空间。 |
     | 存储类 | 选择创建所使用的存储类。 |
     | 卷模式 | 选择持久卷的卷模式。有以下选项： - 文件系统 - 块 |
     | 访问模式 | 选择持久卷的访问模式。支持的访问模式与所选存储类对应的 CSI 和所选卷模式有关，如下： - SMTX ZBS CSI   - 文件系统：ReadWriteOnce   - 块：ReadWriteOnce、ReadWriteMany、​ReadOnlyMany - SMTX ELF CSI   - 文件系统：ReadWriteOnce、ReadOnlyMany   - 块：ReadWriteOnce、ReadWriteMany、​ReadOnlyMany |
     | 分配量 | 输入持久卷申领的容量。  **注意**：假设此处输入的分配量为 `N GiB`，当持久卷申领所选存储类对应的 CSI 为 SMTX ZBS CSI 时，若 N 为奇数，则实际创建的持久卷容量将自动向上对齐至偶数，即 `N+1 GiB`。 |
   - 通过 **YAML** 创建

     **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

     ```
     apiVersion: v1
     kind: PersistentVolumeClaim    # 资源的类型，该段 YAML 配置定义了一个持久卷申领
     metadata:
       name: ''    # 持久卷申领的名称
       namespace: default    # 名字空间
     spec:
       accessModes: []
       resources:
         requests:
           storage: 10Gi    # 分配量
       storageClassName: ''
       volumeMode: Filesystem    # 卷模式
     ```

     > **注意**：
     >
     > 从 YAML 页面切换至表单页面时，不会保留对 YAML 文件的所有更改。
5. 单击**创建**。

   持久卷申领创建完成后，系统会自动创建并绑定相应的持久卷。

## 查看持久卷申领

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**存储** > **持久卷申领**，可在列表中查看工作负载集群的所有持久卷申领信息。您可以根据一个或多个名字空间进行快速筛选。

   | 参数 | 描述 |
   | --- | --- |
   | 状态 | 持久卷申领的状态，包括`待处理`、`已绑定`和`卷不可用`。 |
   | 持久卷 | 持久卷申领绑定的持久卷。单击持久卷名称可跳转至持久卷详情页面。 |
   | 总容量 | 持久卷申领绑定的持久卷的总存储容量。 |
   | 使用量 | 持久卷申领当前已使用的存储容量。 |
   | 使用率 | 持久卷申领的存储已使用的百分比。 |
   | 创建时间 | 持久卷申领的创建时间。 |

   其余参数说明，请参考[创建持久卷申领](#%E5%88%9B%E5%BB%BA%E6%8C%81%E4%B9%85%E5%8D%B7%E7%94%B3%E9%A2%86)中通过表单创建的参数介绍。
3. 单击持久卷申领的名称链接，可查看持久卷申领的详细信息。

   - **基本信息**、**资源用量**：除持久卷申领列表中包含的参数外，还可展示持久卷申领的标签和注解信息。
   - **Pod**：展示使用该持久卷申领的 Pod 列表，具体参数说明请参见[查看 Pod](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_45#%E6%9F%A5%E7%9C%8B-pod)。
   - **状况**：展示持久卷申领的 Condition 信息，包括 Conditon 的类型、状态、状态最新变更时间、状态变更原因以及变更的详细信息。
4. 单击**事件**页签，可查看持久卷申领相关的事件列表，包括事件的类型、原因、事件信息以及事件最近一次的发生时间。
5. 当监控插件启用时，单击**监控**页签，可查看持久卷申领的监控信息。支持设置监控查询的时间范围，以及监控信息的刷新频率。

   - 启用监控插件请参见[创建工作负载集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)中的**配置集群插件** > **配置可观测性**小节。
   - 展示的监控图表类型与工作负载集群的 `Kubernetes / Persistent Volumes` 监控视图下的监控图表类型一致。

## 持久卷申领相关操作

在持久卷申领列表页面选择 **...**，可完成如下操作；您也可以进入持久卷申领的详情页面执行相应操作。

- **下载 YAML**：下载持久卷申领的 YAML 文件。
- **删除**：对于不再需要使用的持久卷申领，可执行删除操作。

当存储类允许卷扩容时，在详情页面的**分配量**后单击**编辑**，可修改持久卷申领的存储容量，仅支持扩容。修改完成后，系统会自动调整绑定的持久卷容量。

---

## 管理工作负载集群 > 管理存储 > 管理存储类

# 管理存储类

[存储类](https://kubernetes.io/zh-cn/docs/concepts/storage/storage-classes/)用于定义持久卷动态供应的方式，指定了存储的类型、配置参数以及对应的制备器。

SKS 支持使用 SMTX ELF CSI、SMTX ZBS CSI 或其他第三方制备器创建存储类。

若工作负载集群部署在未启用双活特性的 SMTX OS 集群中，则使用 SMTX ELF CSI 和 SMTX ZBS CSI 默认存储类所创建的持久卷对应的虚拟卷的存储策略为 2 副本、精简置备；若工作负载集群部署在启用双活特性的 SMTX OS 集群中，则使用 SMTX ELF CSI 和 SMTX ZBS CSI 默认存储类所创建的持久卷对应的虚拟卷的存储策略为 3 副本、精简置备。

您也可以按需创建其他不同副本数的存储类，其可用副本数取决于所使用的底层集群的类型。例如：若工作负载集群部署在启用双活特性的 SMTX OS 集群中，且使用该集群的存储，则副本数需为 3；若仅部署在启用双活特性的 SMTX OS 集群中，但对接的外部存储为非双活集群，则副本数可以为 2。

**注意事项**

工作负载集群所在的 SMTX OS 集群转换为双活集群后，副本数调整如下：

- **默认存储类副本数自动调整**

  - 工作负载集群中 SMTX ELF CSI、SMTX ZBS CSI 默认存储类自动调整为 3 副本。
  - 通过 SMTX ELF CSI、SMTX ZBS CSI 默认存储类创建的持久卷也将自动调整为 3 副本。
  - 副本数变更过程不影响节点上 Pod 的正常运行。
- **自定义存储类副本数不自动调整**

  - 若原先存在自定义的存储类为 2 副本，则不会自动调整。继续使用该自定义存储类创建持久卷，会因副本数不足而导致创建失败。
  - 为确保存储可用性，建议将原有的自定义 2 副本存储类替换为同名的 3 副本存储类。
- **特殊情况**

  若 SMTX ZBS CSI 对接的是外部存储集群，则需要根据外部存储集群是否为双活集群，创建具有相应副本数的存储类。即对接的外部存储集群为非双活集群时，需要创建至少 2 副本的存储类；对接的外部存储集群为双活集群时，需要创建 3 副本的存储类。

## 创建存储类

开启了 CSI 插件的工作负载集群会默认生成一个存储类，其文件系统设置为 **ext4**。如果需要包含不同文件系统设置的存储类，可以创建一个新的存储类。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**存储** > **存储类**。
3. 单击 **+ 创建存储类**。
4. 在弹出的**创建存储类**对话框中，配置存储类。

   - 通过**表单**创建

     | 参数 | 描述 |
     | --- | --- |
     | 名称 | 输入存储类的名称。 |
     | 制备器 | 选择制备持久卷的 CSI 插件。  可选项为 `SMTX ELF CSI（仅适用于虚拟机集群）` 和 `SMTX ZBS CSI`，但仅支持选择已开启的 CSI 插件。 |
     | 文件系统 | 选择基于该存储类创建出的持久卷的文件系统类型。  可选项为 `ext2`、`ext3`、`ext4（默认）` 和 `xfs`。 |
     | 回收策略 | 定义删除持久卷申领后，持久卷的处理方式。可选项为：  - `删除`：删除持久卷及其底层存储资源。 - `保留`：保留持久卷及其底层存储资源。 |
   - 通过 **YAML** 创建

     **配置内容**中提供如下默认 YAML 模板，您可以按需配置相关参数。

     ```
     apiVersion: storage.k8s.io/v1
     kind: StorageClass    # 存储类的类型
     metadata:
       name: ''
     parameters:
       csi.storage.k8s.io/fstype: ext4    # 存储类的文件系统类型
       elfCluster: dbd824d7-82dd-4764-9a6b-13cb67e66a29  # 仅 SMTX ELF CSI 配置
     provisioner: ''
     reclaimPolicy: Delete    # 存储类的回收策略
     allowVolumeExpansion: true    # 是否允许扩容卷
     volumeBindingMode: Immediate    # 卷绑定模式
     ```

     如需自定义存储类副本数，需根据不同 CSI 类型在存储类的 `parameters` 中增加如下配置项：

     - **SMTX ELF CSI**

       ```
       parameters:
         storagePolicy: REPLICA_2_THIN_PROVISION    # 2 副本精简置备；可以按需配置为​ REPLICA_3_THIN_PROVISION、​REPLICA_2_THICK_PROVISION 或 ​REPLICA_3_THICK_PROVISION
       ```
     - **SMTX ZBS CSI**

       ```
       parameters:
         replicaFactor: "2"    # 2 副本；可以按需配置为 "3"，即 3 副本
       ```
     > **注意**：
     >
     > 从 YAML 页面切换至表单页面时，不会保留对 YAML 文件的所有更改。
5. 单击**创建**。

## 查看存储类

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**存储** > **存储类**，可在列表中查看工作负载集群的所有存储类信息。

   | 参数 | 描述 |
   | --- | --- |
   | 默认存储类 | 标识该存储类是否为集群的默认存储类。默认存储类用于未指定存储类的持久卷申领。 |
   | 卷扩容 | 标识基于该存储类创建的持久卷是否支持扩容。若支持卷扩容，则持久卷申领的存储容量可动态增加。 |
   | 创建时间 | 存储类的创建时间。 |

   其余参数说明，请参考[创建存储类](#%E5%88%9B%E5%BB%BA%E5%AD%98%E5%82%A8%E7%B1%BB)中通过表单创建的参数介绍。
3. 单击存储类的名称链接，可查看存储类的详细信息。

   - **基本信息**：除存储类列表中包含的参数外，还可展示存储类的标签和注解信息。
   - **持久卷申领**：展示基于该存储类创建的所有持久卷申领信息，具体参数说明请参考[查看持久卷申领](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_55#%E6%9F%A5%E7%9C%8B%E6%8C%81%E4%B9%85%E5%8D%B7%E7%94%B3%E9%A2%86)。

## 存储类相关操作

在存储类列表页面选择 **...**，可完成如下操作；您也可以进入存储类的详情页面执行相应操作。

- **下载 YAML**：下载存储类的 YAML 文件。
- **删除**：对于不再需要使用的存储类，可执行删除操作。删除存储类后，不会删除基于该存储类创建出的持久卷。

---

## 管理工作负载集群 > 管理项目、角色和成员

# 管理项目、角色和成员

**项目、角色和成员的关系**

项目是一个逻辑隔离环境，用于组织和管理集群中的相关资源，以支持多租户应用部署和资源隔离。一个项目可以包含一个或多个名字空间，一个名字空间只能属于一个项目，用于实现资源的逻辑分组和权限控制。

角色用于定义集群项目内资源的访问控制权限，支持预定义角色和自定义角色。

成员是 SKS 工作负载集群中的用户，通过关联的角色定义其权限范围。

每个项目可以有多个成员，一个成员可以属于一个或多个项目，每个成员在单个项目中只能拥有一个角色。各项目内的资源权限相互独立，互不影响。

**前提条件**

- 具有创建项目、角色和成员的权限，即用户需在 CloudTower 中具有**编辑工作负载集群**的权限，具体说明请参考[权限管理](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_102)。
- 对于已在 SKS 1.4.0 之前的版本中创建的工作负载集群，升级至本版本后，**概览**页面将提示用户与权限功能不可用。如需使用本功能，请先在**概览**页面单击 **...** > **功能版本更新**，原地更新集群的功能版本，即原地更新工作负载集群内置功能对应的 SKS 版本至最新版本。

  > **说明**：
  >
  > SKS 服务升级至本版本后，工作负载集群中将自动创建 `System` 项目，但不会自动创建预定义角色。只有将工作负载集群的**功能版本**更新至本版本后，才会自动创建预定义角色。
- 请在 CloudTower 中为用户分配**工作负载集群使用者**角色，仅具有该角色的用户可以被添加为项目成员。**工作负载集群使用者**为系统预定义的角色，您需要将其关联至相应用户。创建或编辑用户的相关操作，请参考《CloudTower 使用指南》的**管理用户与权限** > **用户管理**章节。

---

## 管理工作负载集群 > 管理项目、角色和成员 > 管理项目

# 管理项目

使用前请先了解[项目、角色和成员的关系](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_116)，并根据实际业务需求规划项目结构以及角色和成员的对应关系。

## 创建项目

工作负载集群创建完成后，自动创建 `System` 项目，其下包含 Kubernetes 使用的名字空间和 SKS 系统组件使用的名字空间。`System` 项目及其下的名字空间均不支持设置配额。

您可以按需创建其他项目来隔离名字空间、应用和资源。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**项目管理** > **项目**。
3. 单击 **+ 创建项目**。
4. 输入项目名称。名称仅支持小写字母、数字、连字符（-），且必须以小写字母或数字开头和结尾，长度为 1 ～ 32 个字符。
5. （可选）选择项目需要关联的名字空间，关联后成员才能访问名字空间中的资源。

   下拉列表中仅支持选择集群中[已创建](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_115#%E5%88%9B%E5%BB%BA%E5%90%8D%E5%AD%97%E7%A9%BA%E9%97%B4)且未关联至其他项目的名字空间。
6. （可选）单击 **+ 添加**，关联成员，关联后用户在项目中将拥有角色对应的操作权限，可访问工作负载集群中关联名字空间的相应资源。单击 **x**，可移除成员。

   - **用户名**：下拉列表中仅支持选择 CloudTower 中具有**工作负载集群使用者**角色的用户。创建或编辑用户的相关操作，请参考 《CloudTower 使用指南》的**管理用户与权限** > **用户管理**章节。
   - **角色**：设置用户在项目中的角色，系统内置**应用运维管理员**和**应用开发者**角色，您也可以选择自定义的角色。内置角色说明以及创建角色的相关操作，请参考[管理角色](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_118)章节。
7. 设置项目配额，即限制项目内所有名字空间的资源使用总量，以实现资源的合理分配。默认不限制资源配额，设置为 `0` 表示禁止该项目申请或使用此类资源。

   设置项目配额前，请先了解**集群资源、项目配额、名字空间配额间的约束关系**，并进行合理规划：

   - 项目配额受工作负载集群资源限制

     - 工作负载集群中，所有项目的配额总和不得超过当前可用的集群资源总量。
     - 若项目配额总量超出集群可用资源上限时，系统允许保存配置。
     - 当节点变更导致集群资源减少时，系统可自动校验剩余可分配的资源总量。
   - 名字空间配额受项目配额限制

     - 项目下各名字空间可以单独设置资源配额。虽然所有名字空间设置的配额总和可以超过所在项目的配额，但实际名字空间的资源使用上限不可超过项目配额。
     - 若项目设置配额，但名字空间未设置配额，则名字空间的资源实际使用量受项目配额限制，多个名字空间可共享项目的剩余资源。

       例如，项目 A 的 CPU 限制配额为 8 core，名字空间 A1、A2 没有限制配额，那么名字空间 A1 在名字空间 A2 未使用任何资源时，最多可以使用 8 core。
     - 若项目与名字空间均设置配额，则需同时满足两层配额限制。即名字空间的资源实际使用量不能超过名字空间的配额，项目下所有名字空间的资源实际使用量也不能超过项目配额。

       例如，项目 A 的 CPU 限制配额为 8 core，名字空间 A1 的 CPU 限制配额为 5 core，名字空间 A2 的 CPU 限制配额为 5 core。此时，名字空间 A1 的资源使用量不能超过 5 core，名字空间 A2 的资源使用量不能超过 5 core，两个名字空间合计的总 CPU 使用量不能超过 8 core。
     - 当资源使用量接近配额（默认阈值为配额的 80%）时，系统将触发报警，以便您能够及时调整资源分配。如需调整报警阈值，请参考《CloudTower 使用指南》的**管理报警** > **管理报警规则** > **编辑内置规则**小节。当资源使用量超出配额时，将阻止新的资源创建，但不会影响存量资源。

   | 参数 | 描述 |
   | --- | --- |
   | CPU 请求 | 预留给项目内所有 Pod 使用的最小 CPU 量。 |
   | CPU 限制 | 分配给项目内所有 Pod 使用的最大 CPU 量。 |
   | 内存请求 | 预留给项目内所有 Pod 使用的最小内存量。 |
   | 内存限制 | 分配给项目内所有 Pod 使用的最大内存量。 |
   | 持久卷申领 | 项目中允许存在的持久卷声明的最大总量。 |
   | GPU 数量 | 项目中允许使用的 GPU 资源的最大数量。 |
8. 设置默认容器配额，用于限制项目内所有名字空间的单个容器默认的资源申请和使用量，以确保容器资源合理分配。默认不限制。

   | 参数 | 描述 |
   | --- | --- |
   | CPU 请求 | 预留给 Pod 中单个容器使用的最小 CPU 量。 |
   | CPU 限制 | 分配给 Pod 中单个容器使用的最大 CPU 量。 |
   | 内存请求 | 预留给 Pod 中单个容器使用的最小内存量。 |
   | 内存限制 | 分配给 Pod 中单个容器使用的最大内存量。 |

   > **注意**：
   >
   > - 新设置的默认容器配额仅对新建或重新创建的 Pod 生效，不影响已经运行的 Pod，且仅在容器未设置资源限制和资源请求时被应用。
   > - 如果仅给 Pod 的容器设置了资源限制而未设置资源请求，系统将会默认使用资源限制值作为资源请求值，不会采用默认容器配额的设置，可能会导致资源预留不准确。
9. 单击**创建**。

## 查看项目

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的概览页面。
2. 在左侧导航栏单击**项目管理** > **项目**，可在列表中查看工作负载集群的所有项目信息。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | 项目的名称。 |
   | 状态 | 项目的状态。  - `活跃`：项目正常运行。 - `删除中`：项目正在被删除，所有资源将依次被清理和删除。 |
   | 名字空间数量 | 项目内包含的名字空间数量，显示为`就绪数量/总数量`。 |
   | 成员数量 | 项目内包含的成员数量。 |
   | CPU 使用量 | 项目内的 CPU 资源使用量。 |
   | 内存使用量 | 项目内的内存资源使用量。 |
   | 持久卷使用量 | 项目内的持久卷资源使用量。 |
   | 创建时间 | 项目的创建时间。 |
3. 在项目列表中单击某一项目，在详情页面中可以查看该项目的详细信息。

   **详情**

   除项目列表中包含的参数外，还可展示设置的**默认容器配额**和**项目配额**，以及该项目中各类资源配额的已分配量和使用率。

   **名字空间**

   单击**名字空间**页签，可查看项目中包含的所有名字空间信息，参数说明请参考[查看名字空间](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_115#%E6%9F%A5%E7%9C%8B%E5%90%8D%E5%AD%97%E7%A9%BA%E9%97%B4)。

   - 单击 ... > **编辑名字空间配额**，可单独设置某个名字空间的 CPU、内存、持久卷申领、GPU 数量配额，具体操作请参考[编辑名字空间配额](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_115#%E7%BC%96%E8%BE%91%E5%90%8D%E5%AD%97%E7%A9%BA%E9%97%B4%E9%85%8D%E9%A2%9D)。
   - 单击 ... > **解除关联**，可解除某个名字空间与当前项目的关联关系。

   **成员**

   单击**成员**页签，可查看项目中包含的所有成员信息，参数说明请参考[查看成员](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_119#%E6%9F%A5%E7%9C%8B%E6%88%90%E5%91%98)。

   单击 ... > **解除关联**，可解除某个成员与当前项目的关联关系。

## 项目相关操作

在项目列表页面选择 **...**，可完成如下操作：

- **编辑项目**：对于 `System` 项目，您可以为其关联成员；对于自定义的项目，您可以修改项目名称、添加或移除关联名字空间、添加或移除成员、添加或修改项目配额、添加或修改默认容器配额。具体操作请参考[创建项目](#%E5%88%9B%E5%BB%BA%E9%A1%B9%E7%9B%AE)。
- **删除项目**：对于不再需要使用的项目，可执行删除操作。

  - 删除项目时，您可以按需勾选**同步删除项目内的名字空间**，将同时删除名字空间以及该名字空间下的所有资源。未勾选则名字空间类型将变更为无归属项目。
  - `System` 项目不支持删除。
  - 项目内包含 `default` 名字空间时，不支持**同步删除项目内的名字空间**。

---

## 管理工作负载集群 > 管理项目、角色和成员 > 管理角色

# 管理角色

使用前请先了解[项目、角色和成员的关系](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_116)，并根据实际业务需求规划项目结构以及角色和成员的对应关系。

工作负载集群项目内支持以下预定义角色，预定义角色不支持编辑或删除。您也可以按需创建自定义角色。

| 角色类型 | 权限 |
| --- | --- |
| 应用运维管理员 | 支持管理指定项目内的所有资源与配置。  支持管理项目内名字空间配额和所有工作负载、服务与网络、配置以及其他归属于名字空间的资源，如自定义资源、ReplicaSets 等；不支持创建名字空间。 |
| 应用开发者 | 支持在指定项目内部署并操作工作负载及相关资源。   - 管理项目中的持久卷申领。 - 管理项目中的工作负载，包括 CronJob、DaemonSet、Deployment、Job、StatefulSet 和 Pod。 - 管理项目中的服务与网络资源，包括 Ingress、NetworkPolicy 和 Service。 - 管理项目中的配置资源，包括 ConfigMap 和 Secret。 |

CloudTower 针对 SKS 提供的角色与可分配权限的相关说明，请参考[权限管理](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_102)。

## 创建自定义角色

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**项目管理** > **角色**。
3. 单击 **+ 创建自定义角色**。
4. 输入角色名称和描述。名称仅支持小写字母、数字、连字符（-），且必须以小写字母或数字开头和结尾，长度为 1 ～ 32 个字符。
5. 设置角色的权限并选择权限生效范围。鼠标浮动在权限或范围描述上，可查看详细的权限说明。
6. 单击**创建**。

## 查看角色

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的概览页面。
2. 在左侧导航栏单击**项目管理** > **角色**，可在列表中查看工作负载集群的所有角色信息。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | 角色的名称。 |
   | 描述 | 角色的描述信息。 |
   | 权限范围 | 角色包含的权限范围说明，例如 `4 项操作权限`。 |
   | 关联用户数 | 角色关联的用户数量。 |
   | 创建时间 | 角色的创建时间。 |
3. 单击某一角色，在右侧的详情面板中可查看具体的操作权限信息。

## 角色相关操作

在角色列表页面选择 **...**，可完成如下操作；您也可以进入角色的详情面板执行相应操作。

- **编辑角色**：对于自定义的角色，您可以修改角色名称、描述，以及角色的权限和范围。修改后，具有该角色的用户将自动更新相应的权限。具体操作请参考[创建自定义角色](#%E5%88%9B%E5%BB%BA%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%92%E8%89%B2)。
- **删除角色**：对于不再需要使用的自定义角色，可执行删除操作。删除角色前，请确保该角色下未关联任何用户。

---

## 管理工作负载集群 > 管理项目、角色和成员 > 管理成员

# 管理成员

使用前请先了解[项目、角色和成员的关系](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_116)，根据实际业务需求规划项目结构以及角色和成员的对应关系，并在 CloudTower 中创建具有**工作负载集群使用者**角色的相应用户。

由于 CloudTower 中的用户和工作负载集群的用户数据同步存在延时，添加成员前可先同步成员数据，以获取最新的用户信息。

## 同步成员数据

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**项目管理** > **成员**。
3. 单击**同步成员数据**，以获取 CloudTower 中最新的用户信息。

## 添加成员

**前提条件**

已创建待管理的[项目](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_117#%E5%88%9B%E5%BB%BA%E9%A1%B9%E7%9B%AE)和需要分配给成员的[角色](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_118#%E5%88%9B%E5%BB%BA%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%92%E8%89%B2)。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**项目管理** > **成员**。
3. 单击 **+ 添加成员**。
4. 选择一个或多个用户，仅支持未关联项目的**工作负载集群使用者**角色的 CloudTower 用户。
5. 选择项目以及用户在该项目中的角色，用户根据角色定义的操作权限范围访问工作负载集群的相应资源。

   - 单击 **+ 添加**，可为用户配置在多个项目中的角色。
   - 单击 **x**，可移除已添加的项目和角色。
6. 单击**创建**。

## 查看成员

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**项目管理** > **成员**，可在列表中查看工作负载集群的所有成员信息。

   | 参数 | 描述 |
   | --- | --- |
   | 用户名 | 成员的用户名，即 CloudTower **用户管理**页面中配置的用户名。 |
   | 姓名 | 成员的姓名，即 CloudTower **用户管理**页面中配置的姓名。 |
   | 项目 | 成员关联的项目数量。 |
   | 角色 | 成员在关联的项目中的角色。 |
   | 创建时间 | 成员的创建时间，即该成员首次被添加至项目的时间。 |
3. 单击某一成员，在右侧的详情面板中可查看具体项目与角色的对应关系，以及成员被添加进该项目的时间。

## 成员相关操作

在成员列表页面选择 **...**，可完成如下操作；您也可以进入成员的详情面板执行相应操作。

- **编辑成员**：您可以修改成员关联的项目以及在该项目中的角色、为成员添加或移除项目角色。具体操作请参考[添加成员](#%E6%B7%BB%E5%8A%A0%E6%88%90%E5%91%98)。
- **下载 Kubeconfig 文件**：您可以为成员下载 Kubeconfig 文件，用于该成员访问工作负载集群。成员通过该 Kubeconfig 文件访问工作负载集群时，将根据关联项目中的角色授予其相应项目中资源的操作权限。具体的访问方式可以参见 Kubernetes 官网的[访问集群](https://kubernetes.io/zh-cn/docs/tasks/access-application-cluster/access-cluster/)章节。
- **移除成员**：对于不再需要访问工作负载集群中任何项目资源的成员，可执行移除成员操作。移除成员后，不会删除 CloudTower 中的用户数据，该用户仍可再次被添加为项目成员。

此外，在详情面板的**项目角色**区域，单击 **...** > **移除**，可移除成员在工作负载集群中访问某个项目资源的权限。

---

## 管理工作负载集群 > 管理项目、角色和成员 > 配置示例

# 配置示例

假设 `user-A` 是 SKS 集群超级管理员，需要为当前 CloudTower 中用户 `user-B` 分配 SKS 工作负载集群运维管理员角色，为用户 `user-C` 分配工作负载集群使用者角色。

- **SKS 工作负载集群运维管理员**：拥有工作负载集群的完全管理权限。
- **工作负载集群使用者**：仅能管理被授权的工作负载集群中项目的相应资源。

SKS 工作负载集群运维管理员 `user-B` 需要为工作负载集群使用者 `user-C` 分配工作负载集群 `cluster-1` 中指定项目的角色。

- 项目 `project-1` 包含两个名字空间 `ns-1` 和 `ns-2`。
- 角色 `cluster-role` 具有**管理工作负载**和**管理服务与网络**的操作权限。

**操作流程**

用户 `user-A` 登录 CloudTower，进入**设置** > **系统配置**页面，参考《CloudTower 使用指南》的**管理用户与权限**章节完成如下操作：

1. 单击**角色管理**，创建自定义角色。角色名称为 SKS 工作负载集群运维管理员，操作权限选择工作负载集群所有权限。
2. 单击**用户管理**，为用户 `user-B` 分配自定义的 SKS 工作负载集群运维管理员角色，为用户 `user-C` 分配系统默认的工作负载集群使用者角色。

用户 `user-B` 登录 CloudTower，进入 **Kubernetes 服务**页面。单击工作负载集群 `cluster-1`，进入工作负载集群概览页面，完成如下操作：

1. 单击**名字空间**，创建两个名字空间 `ns-1` 和 `ns-2`，操作方式请参考[创建名字空间](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_115#%E5%88%9B%E5%BB%BA%E5%90%8D%E5%AD%97%E7%A9%BA%E9%97%B4)。
2. 单击**项目管理** > **角色**，创建自定义角色 `cluster-role`，角色范围选择**管理工作负载**和**管理服务与网络**，操作方式请参考[创建自定义角色](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_118#%E5%88%9B%E5%BB%BA%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%92%E8%89%B2)。
3. （可选）单击**项目管理** > **成员**，同步成员数据，确保获取 `user-C` 用户的信息。
4. 单击**项目管理** > **项目**，创建项目 `project-1`，操作方式请参考[创建项目](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_117#%E5%88%9B%E5%BB%BA%E9%A1%B9%E7%9B%AE)。

   - 关联名字空间：选择 `ns-1` 和 `ns-2`。
   - 关联成员：用户选择 `user-C`，角色选择 `cluster-role`。

用户 `user-C` 登录 CloudTower，进入[工作负载集群使用者视图](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_120)，可在列表中查看 `cluster-1` 工作负载集群的详细信息。`user-C` 用户还可以通过集群控制台或 Kubeconfig 文件管理 `project-1` 项目中 `ns-1` 和 `ns-2` 名字空间下的工作负载以及服务与网络资源。

---

## 管理工作负载集群 > 工作负载集群使用者视图

# 工作负载集群使用者视图

具有**工作负载集群使用者**角色的用户仅可访问工作负载集群使用者视图，管理其被授权的工作负载集群中的项目资源。

**前提条件**

- 用户具有**工作负载集群使用者**角色。
- 已在 SKS 中为用户配置工作负载集群特定项目资源的访问权限。具体操作请参考[管理项目、角色和成员](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_116)章节。

**操作步骤**

1. 使用具有**工作负载集群使用者**角色的用户名、密码登录 CloudTower，进入**我的工作负载集群**页面。列表中显示了用户有权限管理的所有工作负载集群的详细信息。

   | 参数 | 描述 |
   | --- | --- |
   | 显示名称 | 工作负载集群的显示名称，具有一定的业务语义。 |
   | 名称 | 工作负载集群的唯一标识名称。 |
   | 状态 | 工作负载集群的当前状态，包括`创建中`、`运行中`、`就绪`等，具体内容请参考[查看工作负载集群信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_27)中的状态说明。 |
   | Control Plane 虚拟 IP | 工作负载集群配置的 Control Plane 虚拟 IP。 |
   | Control Plane 节点数量 | 工作负载集群配置的 Control Plane 节点数量，显示为`就绪数量/预期数量`。 |
   | Worker 节点数量 | 工作负载集群的 Worker 节点数量，显示为`就绪数量/预期数量`。 |
   | 插件数量 | 工作负载集群中已安装的插件数量，显示为`就绪数量/总数量`。 |
   | Kubernetes 版本 | 工作负载集群中运行的 Kubernetes 的版本。 |
   | Worker 节点类型 | 工作负载集群 Worker 节点的类型，包括`虚拟机`和`物理机`。 |
   | Control Plane 节点 CPU 分配量 | 工作负载集群中所有 Control Plane 节点 CPU 分配量之和。 |
   | Worker 节点 CPU 分配量 | 工作负载集群中所有 Worker 节点 CPU 分配量之和。 |
   | GPU 数量 | 工作负载集群中配置的 GPU 设备数量，物理机集群显示为 `-`。 |
   | GPU 型号 | 工作负载集群中配置的 GPU 的型号，物理机集群显示为 `-`。 |
   | 内存分配量 | 工作负载集群中所有节点的内存分配量之和。 |
   | 系统存储 | 工作负载集群所有节点的存储分配量之和，物理机集群显示为 `-`。 |
   | SMTX OS 集群 | 工作负载集群所属 SMTX OS 集群的名称。 |
   | CPU 架构 | 工作负载集群所属 SMTX OS 集群的 CPU 架构。 |
   | 创建时间 | 工作负载集群开始创建的时间。 |
   | SKS 版本 | 创建、更新或升级工作负载集群时对应 SKS 服务的版本。 |
   | 功能版本 | 工作负载集群内置功能对应的 SKS 版本信息。 |
   | 节点模板的 SKS 版本 | 工作负载集群当前使用的节点模板对应的 SKS 版本。 |
2. 单击某一工作负载集群右侧的 **...**，可以执行以下操作：

   - **打开集群控制台**：您可以通过集群控制台管理已被授权的工作负载集群中的项目资源，具体操作请参考[打开集群控制台](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_113)。
   - **下载 Kubeconfig**：您可以下载用于访问该工作负载集群的 Kubeconfig 文件，通过 kubectl 命令行工具管理已被授权的工作负载集群中的项目资源。下载后请妥善保管该文件，具体的访问方式可以参见 Kubernetes 官网的[访问集群](https://kubernetes.io/zh-cn/docs/tasks/access-application-cluster/access-cluster/)章节。
3. 单击某一工作负载集群的名称链接，可进入工作负载集群的详情页面。您可以管理已被授权的工作负载集群中的项目资源：

   - **名字空间**：支持查看您所属项目关联的名字空间列表，具体参数说明请参考[查看名字空间](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_115#%E6%9F%A5%E7%9C%8B%E5%90%8D%E5%AD%97%E7%A9%BA%E9%97%B4)。当您具有**管理名字空间配额**权限时，还可以编辑名字空间配额以及查看名字空间的详情。
   - **工作负载**：当您具有**管理工作负载**权限时，可管理 CronJob、DaemonSet、Deployment、Job、StatefulSet 和 Pod。具体操作及参数说明，请参考[管理工作负载](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_39)。

     > **说明**：
     >
     > 当前暂不支持查看相应资源的**事件**和**监控**信息。
   - **服务与网络**：当您具有**管理服务与网络**权限时，可管理 Ingress、Service 和 NetworkPolicy。具体操作及参数说明，请参考[管理服务与网络](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_46)。
   - **配置**：当您具有**管理配置**权限时，可管理 ConfigMap 和 Secret。具体操作及参数说明，请参考[管理配置](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_50)。
   - **存储**：当您具有**管理持久卷申领**权限时，可管理持久卷申领。具体操作及参数说明，请参考[管理存储 > 管理持久卷申领](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_55)。
   - **项目**：支持查看您所属项目的项目列表，具体参数说明请参考[查看项目](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_117#%E6%9F%A5%E7%9C%8B%E9%A1%B9%E7%9B%AE)。
4. 在工作负载集群详情页的右上方单击**导入 YAML**，可通过 YAML 文件创建 Kubernetes 资源对象，具体操作请参考[导入 YAML](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_107)。导入 YAML 时，请选择名字空间或在 YAML 文件中设置名字空间。
5. 在页面右上角可通过**个人设置**管理个人信息、账号安全及 CloudTower 的界面语言。具体操作请参考《CloudTower 使用指南》的**个人设置**章节。

---

## 管理工作负载集群 > 管理插件

# 管理插件

在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。在左侧导航栏单击**设置** > **插件管理**，可根据实际需求管理 GPU、外部负载均衡器、Ingress 控制器插件和可观测性相关插件。对于虚拟机集群，您还可以管理 EIC 和 SMTX ELF CSI 插件；对于物理机集群，您还可以管理 SMTX ZBS CSI 插件。

> **说明**：
>
> - Calico CNI 插件仅在创建工作负载集群时可以修改插件参数，创建后不可通过 UI 界面修改。
> - 仅当工作负载集群处于**就绪**、**运行中**或**异常**状态时，可启用、禁用或编辑插件。
> - 禁用插件后再次启用，插件参数将还原为默认配置。

---

## 管理工作负载集群 > 管理插件 > 管理 EIC 插件（仅适用于虚拟机集群）

# 管理 EIC 插件（仅适用于虚拟机集群）

仅当您在创建虚拟机集群的**基本信息**界面已选择 EIC 插件时，**插件管理**界面才会展示 EIC 插件的配置，并且该插件自动启用，不支持关闭。

您可以查看 Pod IP 池的 IP 总数和剩余可用的 IP 数量，展开**参数配置**，还可以查看 EIC 专用网卡的网络配置，按需新建、编辑 Pod IP 池，以及删除未被使用的 Pod IP 池，暂不支持其他操作。

---

## 管理工作负载集群 > 管理插件 > 管理 SMTX ZBS CSI 插件

# 管理 SMTX ZBS CSI 插件

## 启用 SMTX ZBS CSI 插件（仅适用于物理机集群）

当您在创建工作负载集群的**基本信息**界面已选择 SMTX ZBS CSI 插件时，将默认启用该插件。否则，物理机集群默认不启用，虚拟机集群不支持启用。

如需为物理机集群启用 SMTX ZBS CSI 插件，请先参考[SMTX ZBS CSI 专用网卡网络要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_21)做好规划。

**操作步骤**

1. 进入**插件管理**页面，在 **CSI** 类型下启用 **SMTX ZBS CSI**。
2. 根据实际规划选择虚拟机节点的 SMTX ZBS CSI 专用网卡的虚拟机网络，填写目标存储集群的虚拟 IP，并选择为 SMTX ZBS CSI 专用网卡创建的 IP 池。
3. （可选）通过 YAML 配置该插件的参数。具体配置方式请参见[配置 SMTX ZBS CSI](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_25#%E9%85%8D%E7%BD%AE-smtx-zbs-csi)。
4. 单击**保存**。

当物理机集群**概览**页面的**集群插件状态**中显示 smtx-zbs-csi 状态正常时，说明该插件已成功启用。启用成功后，SKS 会自动创建一个默认存储类。

## 禁用 SMTX ZBS CSI 插件（仅适用于物理机集群）

仅当物理机集群中无 SMTX ZBS CSI 插件对应的持久卷时才支持禁用 SMTX ZBS CSI 插件。如需禁用该插件，请先删除集群中对应的持久卷。

## 编辑 SMTX ZBS CSI 插件

启用 SMTX ZBS CSI 插件后，您仍可以通过 YAML 修改该插件的相关参数。

> **说明**：
>
> 若工作负载集群部署在未启用双活特性的 SMTX OS 集群，但 SMTX ZBS CSI 对接的外部存储集群为双活集群，需要手动更新副本数为 3，以确保监控插件可用。

---

## 管理工作负载集群 > 管理插件 > 管理 SMTX ELF CSI 插件（仅适用于虚拟机集群）

# 管理 SMTX ELF CSI 插件（仅适用于虚拟机集群）

## 启用 SMTX ELF CSI 插件

仅当您在创建虚拟机集群的**基本信息**界面已选择 SMTX ZBS CSI 插件时，才支持在创建集群后开启 SMTX ELF CSI 插件；否则请忽略该操作。

具体配置方式请参见[配置 SMTX ELF CSI](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_19#%E9%85%8D%E7%BD%AE-smtx-elf-csi)。

**操作步骤**

1. 进入**插件管理**页面，在 **CSI** 类型下启用 **SMTX ELF CSI**。
2. 单击**保存**。

   当工作负载集群**概览**页面的**集群插件状态**中显示 smtx-elf-csi 状态正常时，说明插件已成功启用。启用成功后，SKS 会自动创建一个默认存储类。

## 编辑 SMTX ELF CSI 插件

启用 SMTX ELF CSI 插件后，您仍可以通过 YAML 修改 SMTX ELF CSI 插件的相关参数。

---

## 管理工作负载集群 > 管理插件 > 管理 GPU 插件

# 管理 GPU 插件

物理机集群始终展示 GPU 插件的配置项，虚拟机集群仅当已配置 GPU 设备时才展示。

## 启用 GPU 插件

当工作负载集群的任一 Worker 节点组配置了 GPU 设备时，对于虚拟机集群，系统将默认开启 **NVIDIA GPU Operator** 插件；对于物理机集群，您可以按需开启该插件，如需启用，请确保已参考[准备 GPU 资源](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_09)完成相关准备工作。

> **注意**：
>
> 对于物理机集群，若物理机节点使用的操作系统不是 Rocky Linux 8.10，则无法成功开启该插件，您需要自行管理 GPU 资源。

您还可以按需通过 YAML 配置该插件的参数。具体配置方式请参见[创建工作负载集群 > 创建虚拟机/物理机集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)的**配置集群插件 > 配置 GPU** 小节。

当工作负载集群**概览**页面的**集群插件状态**中显示 nvidia-gpu-operator 状态正常时，说明插件已成功启用。

## 禁用 GPU 插件

当您为虚拟机集群的任一 Worker 节点组挂载了 GPU 设备时，不建议禁用 GPU 插件。如果禁用，必须手动在集群中安装特定版本的 [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/install-gpu-operator-vgpu.html)，否则将导致 GPU 的相关功能异常。

## 编辑 GPU 插件

启用 GPU 插件后，您可以通过 YAML 修改 GPU 插件的相关参数。

---

## 管理工作负载集群 > 管理插件 > 管理可观测性插件

# 管理可观测性插件

建议您为集群关联可观测性服务，以便启用监控、报警、日志、事件和审计功能。

> **注意**：
>
> 为集群关联可观测性服务前，请确保集群节点的业务网卡所在网络、可观测性服务虚拟机的虚拟网卡所在虚拟机网络两者之间三层互通，并且建议先[为 SKS 系统服务关联可观测性服务](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_109)。

## 关联可观测性服务

启用**关联可观测性服务**，然后选择需要关联的可观测性服务。

保存成功后，当前界面将展示**关联状态**，当该状态显示`已关联`时，表明工作负载集群与可观测性服务已关联成功。

## 启用/禁用监控

您可以选择启用或禁用**监控**。对于物理机集群，仅当集群已安装 CSI 插件并且集群中已存在 CSI 对应的默认存储类时，才支持启用**监控**。

- 启用后，您还可通过 YAML 配置该插件的 OBS-Monitoring-Agent 和 Prometheus 参数，详细配置说明可参考[创建工作负载集群 > 创建虚拟机/物理机集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)的**配置集群插件 > 配置可观测性 > 启用监控**小节。

  保存成功后，当工作负载集群**概览**页面的**集群插件状态**中显示 kube-prometheus 和 obs-monitoring-agent 状态正常时，说明监控已成功启用，您可以在工作负载集群的**监控**界面[查看监控信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_66)。
- 禁用并保存成功后，无法查看监控信息，但保存期限内的监控数据不会清除，可观测性服务未更换时，重新启用后仍可查看。

## 启用/禁用报警

您可以选择启用或禁用**报警**。如需启用**报警**，需先启用**监控**。

- 启用并保存成功后，您可以在工作负载集群的**报警**界面[查看报警信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_108)，还可以进行以下操作：
  - 在 CloudTower 的**报警** > **报警规则**界面查看、编辑报警规则。您可以在界面顶部搜索框中的**资源类型**选项中，通过 `SKS 系统服务`、`SKS 容器镜像仓库`、`SKS 集群`、`SKS 集群节点`、`持久卷`或`持久卷申领`字段筛选出与 SKS 相关的报警规则。
  - 在 CloudTower 的**报警** > **通知配置**界面配置报警通知，详细操作说明可参考《可观测性平台用户指南》的**管理报警功能**章节。
- 禁用并保存成功后，无法查看报警信息，关闭前未解决的报警将自动解决，但报警数据不会清除。

## 启用/禁用日志

您可以选择启用或禁用**日志**。

- 启用后，您还可以通过 YAML 配置 OBS-Logging-Agent 参数，详细配置说明可参考[创建工作负载集群 > 创建虚拟机/物理机集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)的**配置集群插件 > 配置可观测性 > 启用日志**小节。

  保存成功后，当工作负载集群**概览**页面的**集群插件状态**中显示 obs-logging-agent 状态正常时，说明日志功能已成功启用，您可以[查看日志信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_67)。
- 禁用并保存成功后，无法查看日志信息，但保存期限内的日志数据不会清除，可观测性服务未更换时，重新启用后仍可查看。

## 启用/禁用事件

您可以选择启用或禁用**事件**。

- 启用后，您还可以通过 YAML 配置 OBS-Event-Agent 参数，详细配置说明可参考[创建工作负载集群 > 创建虚拟机/物理机集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)的**配置集群插件 > 配置可观测性 > 启用事件**小节。

  保存成功后，当工作负载集群**概览**页面的**集群插件状态**中显示 obs-event-agent 状态正常时，说明事件功能已成功启用，您可以[查看事件信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_61)。
- 禁用并保存成功后，无法查看事件信息，但保存期限内的事件数据不会清除，可观测性服务未更换时，重新启用后仍可查看。

## 启用/禁用审计

您可以选择启用或禁用**审计**。

- 启用后，您需要选择审计策略，以指定审计信息的详细程度，若选择**自定义策略**，您需要自行配置审计策略 YAML。

  您还可以通过 YAML 配置 OBS-Audit-Agent 参数，详细配置说明可参考[创建工作负载集群 > 创建虚拟机/物理机集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_05)的**配置集群插件 > 配置可观测性 > 启用审计**小节。

  保存成功后，当工作负载集群**概览**页面的**集群插件状态**中显示 obs-audit-agent 状态正常时，说明审计功能已成功启用，您可以[查看审计信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_72)。

  > **注意**：
  >
  > 若在启用成功后切换审计策略，将导致 API Server 重启，进而可能导致需要访问 API Server 的服务短时间不可用或自动重连。
- 禁用并保存成功后，无法查看审计信息，但保存期限内的审计数据不会清除，可观测性服务未更换时，重新启用后仍可查看。

## 更换可观测性服务

若需要更换可观测性服务，可直接切换可观测性服务，再单击**保存**。

切换后，您将无法查看切换前的监控、日志、事件和审计信息，切换前未解决的报警将自动解决。

---

## 管理工作负载集群 > 管理插件 > 管理外部负载均衡器插件

# 管理外部负载均衡器插件

## 启用/禁用外部负载均衡器插件

您可以按需启用或禁用外部负载均衡器插件，启用时的具体配置方式请参见[启用外部负载均衡器](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_19#%E5%90%AF%E7%94%A8%E5%A4%96%E9%83%A8%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1%E5%99%A8)。

当工作负载集群**概览**页面的**集群插件状态**中显示 metallb 状态正常时，说明插件已成功启用。启用后，您可以在工作负载集群中创建 LoadBalancer 类型的 Service。

## 编辑外部负载均衡器插件

启用外部负载均衡器插件后，您仍可以增加 **IP 范围**，或通过 YAML 配置其他参数。

---

## 管理工作负载集群 > 管理插件 > 管理 Ingress 控制器插件

# 管理 Ingress 控制器插件

## 启用/禁用 Ingress 控制器插件

您可以按需启用或禁用 Ingress 控制器插件，启用时的具体配置方式请参见[启用 Ingress 控制器](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_19#%E5%90%AF%E7%94%A8-ingress-%E6%8E%A7%E5%88%B6%E5%99%A8)。

当工作负载集群**概览**页面的**集群插件状态**中显示 contour 状态正常时，说明插件已成功启用。

当 Service 类型为 LoadBalancer 时，启用后过一段时间，可以看到 Ingress 组件 IP。如需使用域名访问 Ingress，则需要在 DNS 服务器中添加域名解析记录以解析到该 IP。

## 编辑 Ingress 控制器插件

启用 Ingress 控制器插件后，您仍可以通过 YAML 配置其他参数。

## 配置示例

Contour 支持使用多种资源，如 Ingress 资源、HTTPProxy 资源。

- Ingress 资源支持通过 UI 或命令行创建。UI 操作方式请参考[创建 Ingress](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_47#%E5%88%9B%E5%BB%BA-ingress)，配置方式请参考 [Kubernetes 官方文档](https://kubernetes.io/zh-cn/docs/concepts/services-networking/ingress/)。
- HTTPProxy 资源仅支持通过命令行创建，配置方式请参考如下示例。

如需了解更多内容，请参考 [Contour 官方文档](https://projectcontour.io/docs/1.27/architecture/)。

**示例一**

配置一个 HTTPProxy 资源（即一种原生 Ingress 资源的增强替代 API），将特定的虚拟主机（Virtual Host）域名路由到一个后端服务（Service）。

如下所示，配置后访问 `http://httpbin.example.com` 的所有请求，都将被路由至 `httpbin` Service。

```
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: httpbin
spec:
  virtualhost:
    fqdn: httpbin.example.com
  routes:
    - conditions:
        - prefix: /
      services:
        - name: httpbin
          port: 80
```

**示例二**

配置一个 HTTPProxy 资源，将特定的虚拟主机（Virtual Host）域名路由到多个后端服务（Service）。

如下所示，配置后访问 `http://httpbin.example.com` 的所有请求，都将通过负载分担的方式被路由至 `httpbin` 和 `nginx` Service。

```
# httpproxy-lb-request-hash-ip.yaml
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: lb-request-hash
  namespace: default
spec:
  virtualhost:
    fqdn: request-hash.example.com  
  routes:
    - conditions:
        - prefix: /
      services:
        - name: httpbin
          port: 80
        - name: nginx
          port: 80
      loadBalancerPolicy:
        strategy: RequestHash
        requestHashPolicies:
          # 使用源地址哈希策略，确保来自相同的客户端请求被分发至同一个后端服务
          - hashSourceIP: true
```

**示例三**

配置一个 HTTPProxy 资源，将特定的虚拟主机（Virtual Host）域名通过多 path 路由到多个后端服务（Service）。

如下所示，配置后访问 `multi-path.example.com` 的请求，将根据请求的路径前缀及匹配规则被路由至不同的后端服务。同时，还配置了路径重写策略，以满足 Service 对于路径的要求。

```
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: multiple-paths
spec:
  virtualhost:
    fqdn: multi-path.example.com
  routes:
    - conditions:
        # 使用 URL Prefix 前缀匹配模式
        # 默认规则，表示匹配所有。当 URL 不匹配其他任何 conditions 时将匹配本规则。
        - prefix: /
      services:
        # 匹配后将被路由至 swaggerapi
        - name: swaggerapi
          port: 80
    - conditions:
        # 匹配 httpbin 前缀
        # 客户端请求 URL  http://multi-path.example.com/httpbin/page
        # 后端服务收到 URL    http://multi-path.example.com/httpbin/page
        - prefix: /httpbin
      services:
        # 匹配后将被路由至 httpbin
        - name: httpbin
          port: 80
    - conditions:
        # 匹配 /apis 前缀，包括 multi-path.example.com/apis 和 multi-path.example.com/apis/*
        - prefix: /apis
      pathRewritePolicy:
        # 替换 prefix，使其发送到后端的请求中不包含 /apis
        # 客户端请求 URL http://multi-path.example.com/apis/users
        # 后端服务收到 URL   http://multi-path.example.com/users
        replacePrefix:
          - replacement: /
      services:
        # 匹配后将被路由至 apis
        - name: apis
          port: 80
```

**示例四**

配置一个 HTTPProxy 资源，为特定虚拟主机（Virtual Host）域名提供 HTTPS 支持，同时仍允许继续使用 HTTP。

如下所示，配置后访问 `https://tls-termination.example.com` 的所有请求，都将被路由至 `httpbin` Service。

```
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: tls-termination-example
  namespace: default
spec:
  virtualhost:
    fqdn: tls-termination.example.com
    tls:
      # 请确保名字空间中存在该 Secret
      secretName: tls-termination-example
      # LTS 版本，支持 1.2 或 1.3，默认为 1.2
      minimumProtocolVersion: "1.2"
  routes:
    - services:
        - name: httpbin
          port: 80
      # 允许继续使用 HTTP，否则请求 HTTP 会默认重定向至 HTTPS 
      permitInsecure: true
```

手动创建 TLS 证书方式如下：

```
apiVersion: v1
kind: Secret
type: kubernetes.io/tls
metadata:
  name:  tls-termination-example
  stringData:
    tls.crt: |-
      -----BEGIN CERTIFICATE-----
      you are cert with ca
      -----END CERTIFICATE-----
    tls.key: |-
      -----BEGIN RSA PRIVATE KEY-----
      you are key
      -----END RSA PRIVATE KEY-----
```

---

## 管理工作负载集群 > 管理节点组自动伸缩（仅适用于虚拟机集群）

# 管理节点组自动伸缩（仅适用于虚拟机集群）

如果需要为虚拟机集群的某一 Worker 节点组的节点数类型设置为**自动伸缩**，需要先参考以下步骤开启节点组自动伸缩。

如果需要将虚拟机集群的所有 Worker 节点组的节点数类型一键切换为**固定节点数**，也可以参考以下步骤禁用节点组自动伸缩。

**前提条件**

虚拟机集群处于**就绪**、**运行中**或**异常**状态。

**注意事项**

当虚拟机集群中已有 Worker 节点组使用了**自动伸缩**的节点数类型，如果禁用节点组自动伸缩，则该节点组的节点数类型将自动切换为**固定节点数**，节点数量为关闭该功能时的节点数量。

## 启用/禁用节点组自动伸缩

1. 在虚拟机集群列表中单击目标虚拟机集群的显示名称，进入虚拟机集群的**概览**页面。
2. 在左侧导航栏单击**设置** > **节点组自动伸缩**，在右侧界面启用或禁用 **Cluster Autoscaler**。

## 编辑节点组自动伸缩

启用节点组自动伸缩后，您仍可以通过 YAML 配置 cluster-autoscaler 插件的 `extraArgs` 参数，具体配置方式可参考[配置节点组自动伸缩](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_19#%E9%85%8D%E7%BD%AE%E8%8A%82%E7%82%B9%E7%BB%84%E8%87%AA%E5%8A%A8%E4%BC%B8%E7%BC%A9)。

---

## 管理工作负载集群 > 管理受信任容器镜像仓库

# 管理受信任容器镜像仓库

您可以为已有的工作负载集群添加、删除一个或多个受信任的容器镜像仓库，使工作负载集群能够从容器镜像仓库中拉取工作负载需要使用的容器镜像。

**前提条件**

- 添加内部容器镜像仓库前，请确保已根据[管理容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_70)章节成功创建了容器镜像仓库。
- 添加外部容器镜像仓库前，请提前获取外部容器镜像仓库的访问地址和 CA 证书（可选），并确保工作负载集群可以正常连接至容器镜像仓库。

**注意事项**

添加或删除受信任容器镜像仓库后，SKS 将原地更新集群配置并驱逐节点上的 Pod。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**设置 > 受信任容器镜像仓库**。
3. 单击 **+ 添加容器镜像仓库**，参考如下说明完成配置。

   - **内部容器镜像仓库**：在 CloudTower 的**容器镜像仓库**界面直接创建的容器镜像仓库。

     | 参数 | 描述 |
     | --- | --- |
     | 名称 | 请在下拉菜单中选择已创建的容器镜像仓库。  **说明**：仅支持选择[创建容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_77)时未配置 CA 签发的证书和证书密钥的容器镜像仓库。如在创建容器镜像仓库时已配置 CA 签发的证书和证书密钥，则工作负载集群可直接从该容器镜像仓库拉取容器镜像，无需配置为受信任的容器镜像仓库。 |
     | 访问地址 | 显示所选容器镜像仓库的访问地址。将优先显示域名，如未配置域名则显示 IP 地址。 |
     | CA 证书 | 显示所选容器镜像仓库在[创建容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_77)时是否配置 CA 签发的证书和证书密钥。  **说明**：由于仅支持选择[创建容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_77)时未配置 CA 签发的证书和证书密钥的容器镜像仓库，因此 CA 证书的参数值均为`跳过验证`。 |
   - **外部容器镜像仓库**：自行部署的其他容器镜像仓库。

     | 参数 | 描述 |
     | --- | --- |
     | 名称 | 输入容器镜像仓库的名称，不允许与已配置的容器镜像仓库重名。 |
     | 访问地址 | 输入容器镜像仓库的访问地址，支持配置域名或 IP 地址。  请直接输入域名或 IP 地址，若访问地址需通过 HTTP 方式访问，请再加上 `http://` 前缀。如容器镜像仓库的服务端口非 `443`，则需要指定端口号，例如 `example.registry.com:9443`。 |
     | CA 证书 | 单击**从文件提取**，上传 CA 证书。请选择一个扩展名为 `.crt` 的文件。  留空则表示跳过 CA 证书验证，即从容器镜像仓库获取容器镜像时忽略 SSL 证书验证。 |
4. 单击**保存**。

---

## 管理工作负载集群 > 查看监控信息

# 查看监控信息

**前提条件**

工作负载集群已关联可观测性服务，并且监控功能已启用成功。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**监控**，可以查看工作负载集群的详细监控信息。监控信息默认保存 1 年。

   - 在界面顶部单击日历图标，可以设置需要查询的时间范围。

     - **绝对时间段**：支持自定义起始时间和结束时间，设置完成后单击**应用时间段**。
     - **快速时间段**：支持快速选择 **Last 10 minutes**、**Last 1 hour**、**Last 3 hours**、**Last 24 hours** 以及 **Last 3 days**。
   - 在界面右上方单击刷新图标，可以手动刷新一次监控信息。单击图标右侧的下拉菜单，可以设置自动刷新频率。
   - 在界面顶部单击筛选下拉框，可以选择不同的视图查看监控信息。部分视图还可以进一步设置一个或多个筛选条件，以便快速筛选出需要查看的监控信息。

     > **注意**：
     >
     > 每个视图包含多个图表，仅当工作负载集群已配置 GPU 设备时才支持查看 GPU 相关图表。如果集群已开启 TimeSlicing 功能，则仅支持在以下视图中查看 GPU 相关图表。
     >
     > - **Node Exporter / USE Method / Cluster**
     > - **Node Exporter / USE Method / Node**
     > - **Node Exporter / Nodes**
     > - **Kubernetes / Compute Resource / GPU**

---

## 管理工作负载集群 > 查看报警信息

# 查看报警信息

**前提条件**

工作负载集群已关联可观测性服务，并且报警功能已启用成功。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**报警**，可以查看工作负载集群的所有未解决和已解决的报警。
3. 单击任一报警，将弹出该报警的详情面板，在详情面板中可以查看报警的触发原因、影响、解决方法等信息。

---

## 管理工作负载集群 > 查看日志信息

# 查看日志信息

**前提条件**

工作负载集群已关联可观测性服务，并且日志功能已启用成功。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**日志**，可以查看工作负载集群的详细日志信息。日志信息默认保存 30 天。

   - 在界面顶部单击日历图标，可以设置需要查询的时间范围。
   - 在界面右上方单击**实时**，可以实时查看**日志详情**。
   - 在界面右上方单击**运行查询**，可以手动刷新一次日志。单击图标右侧的下拉菜单，可以设置自动刷新频率。
   - 界面上方默认添加名称为 `A` 的查询面板，在面板中可通过以下操作设置日志查询条件。此外，您还可以编辑面板的名称，在面板右上角对面板执行复制、禁用、移除操作，以及在查询面板下方单击**添加查询**添加查询面板（多个查询面板之间的关系为逻辑与）。

     - 在**标签**区域，可以通过标签筛选日志。

       - 系统默认添加 key 为 `cluster` 和`日志类型`的两个标签，默认筛选当前工作负载集群的日志，并且需要您手动选择筛选的日志类型。默认标签不支持移除。
       - 您可以自行添加其他标签，若添加了多个标签筛选条件，则查询结果将展示同时满足这些条件的日志。

       **标签匹配符号说明**

       | 符号 | 说明 |
       | --- | --- |
       | =~ | 正则表达式匹配。筛选所选对象对应的日志，可选择一个或多个对象。 |
       | = | 完全等于。筛选所选对象对应的日志。 |
       | != | 不等于。筛选排除所选对象后的所有对象对应的日志。 |
       | !~ | 排除正则表达式匹配。筛选排除所选对象后的所有对象对应的日志，可选择一个或多个对象。 |
     - 在**标签**区域下方，可以通过目标文本筛选日志。如添加了多个目标文本筛选条件，查询结果将展示同时满足这些条件的日志。
     - 在**选项**区域，可以设置**日志详情**的数量上限（最高支持 `5000`）和**日志数量**的分辨率。

       分辨率用于调整日志数量面板中的数据点聚合度，影响数据点间的时间间隔。所选分辨率的分母越大，数据点间的时间间隔越大，两个数据点间被忽略的数据点也越多，从而降低统计精度，使面板上最终呈现的结果更侧重于展示数据的分布情况，而不是准确的数据量统计。

---

## 管理工作负载集群 > 查看事件信息

# 查看事件信息

**前提条件**

工作负载集群已关联可观测性服务，并且事件功能已启用成功。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**事件**，可以查看工作负载集群的事件信息。事件信息默认保存 7 天。

   - 您可参考下表了解事件列表各项参数的含义。

     | 参数 | 描述 |
     | --- | --- |
     | 名字空间 | 发生该事件的名字空间的名称。 若与事件关联的资源对象类型不属于名字空间，则展示 `-`。 |
     | 类型 | 包括如下两种事件类型： - 正常：集群运行正常，事件内容仅供参考。 - 警告：集群可能出现问题。 |
     | 原因 | 事件原因的简单总结。 |
     | 对象类型 | 与事件关联的资源对象的类型。 |
     | 对象 | 与事件关联的资源对象。 |
     | 事件信息 | 事件的详细说明。 |
     | 来源 | 生成事件的组件。 若事件为用户手动创建，则展示 `-`。 |
     | 发生次数 | 事件发生的次数。 |
     | 最近发生时间 | 事件最近发生的时间。 |
     | 首次发生时间 | 事件第一次发生的时间。 |
   - 在事件信息右侧单击 **...** > **查看详情**，可以查看详细的事件信息。
   - 在界面顶部单击筛选图标，可以设置筛选条件筛选事件信息，筛选结果将展示同时满足所有筛选条件的事件信息。对于同一筛选条件，若添加了多个值，则系统将筛选出满足任一值的结果。
   - 在界面顶部单击日历图标，可以设置需要查询的时间范围。
   - 在界面右上方单击刷新图标，可以手动刷新一次事件信息。单击图标右侧的下拉菜单，可以设置自动刷新频率。

---

## 管理工作负载集群 > 查看审计信息

# 查看审计信息

**前提条件**

工作负载集群已关联可观测性服务，并且审计功能已启用成功。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在左侧导航栏单击**审计**，可以查看工作负载集群的审计信息。审计信息默认保存 3 个月。

   - 您可参考下表了解审计列表各项参数的含义。

     | 参数 | 描述 |
     | --- | --- |
     | 操作者 | 执行请求的用户。 |
     | 操作 | 执行的操作对应的 API 操作类型。 |
     | 名字空间 | 请求的目标对象所在的名字空间。 若请求操作不涉及某一明确的资源对象，或者资源对象是集群级别的，则展示 `-`。 |
     | 资源类型 | 请求的目标对象的类型。 若请求操作不涉及某一明确的资源对象，则展示 `-`。 |
     | 资源名称 | 请求的目标对象的名称。 若请求操作不涉及某一明确的资源对象，则展示 `-`。 |
     | 鉴权结果 | 根据鉴权情况展示相应的结果： - 允许：请求已通过授权检查，被明确允许执行。 - 拒绝：请求被授权机制（如 RBAC、ABAC 或 Webhook）明确拒绝。 - -：请求未经过 Kubernetes 授权层。 |
     | 请求 IP | 请求从原始用户端到 Kubernetes API Server 的完整传输路径中经过的节点 IP。表格中仅展示第一个 IP，完整的 IP 信息可在审计详情中获取。 |
     | 操作时间 | 执行请求的时间。 |
   - 在审计信息右侧单击 **...** > **查看详情**，可以查看详细的审计信息。
   - 在界面顶部单击筛选图标，可以设置筛选条件筛选审计信息，筛选结果将展示同时满足所有筛选条件的审计信息。对于同一筛选条件，若添加了多个值，则系统将筛选出满足任一值的结果。
   - 在界面顶部单击日历图标，可以设置需要查询的时间范围。
   - 在界面右上方单击刷新图标，可以手动刷新一次审计信息。单击图标右侧的下拉菜单，可以设置自动刷新频率。

---

## 管理工作负载集群 > 升级工作负载集群

# 升级工作负载集群

**前提条件**

- 工作负载集群处于**就绪**、**运行中**或**异常**状态。
- 管控集群未处于**异常**或**升级中**状态。
- 目标节点模板文件的 CPU 架构与待升级的工作负载集群的 CPU 架构一致，且节点模板文件的操作系统与当前工作负载集群虚拟机节点的操作系统一致。
- 目标节点模板文件的 SKS 版本不得低于待升级的工作负载集群使用的节点模板的 SKS 版本。
- 目标 Kubernetes 版本的节点模板文件已上传至内容库，并分发至待升级的工作负载集群的虚拟机节点所属的 SMTX OS 集群。如该节点模板未分发至相应的 SMTX OS 集群，请先按照界面提示[准备 Kubernetes 节点模板](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_08)。
- 确保已为每个用于分配节点 IP 的工作负载集群 IP 池分别预留至少 2 个空闲 IP，预留的 IP 越多，升级速度越快。

**注意事项**

- Kubernetes 版本格式为**主版本号.次版本号.补丁版本号**，工作负载集群不支持跨次版本升级。例如集群升级前的 Kubernetes 版本如果为 1.24.x，则需先升级至 1.25.x，再升级至 1.26.x，1.24.x 不支持直接升级至 1.26.x。
- 升级过程对⼯作负载集群将有以下影响：
  - 集群的每⼀个虚拟机节点将依次被重建，您在虚拟机中存储的⽂件和对操作系统的修改将不会保留。
  - 集群的监控、⽇志相关组件将会更新，更新期间监控和⽇志信息可能⽆法查看，并且信息的采集会发⽣短时间中断。
  - 集群上运行的有状态业务可能会发生短时间中断。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在右上角单击 **...**，选择**升级集群**。
3. 在弹出的**升级集群**对话框中，选择 Kubernetes 版本。下拉菜单中仅显示与当前集群匹配的可升级版本。
4. 单击**升级**。

   在 CloudTower 的任务中心可以查看升级进度。

   - 若 Control Plane 节点升级失败，可以在工作负载集群列表中的目标集群右侧单击 **...**，选择**集群回滚**，先将集群回滚到升级前的状态，待排查完失败原因后再重新升级。
   - 若 Control Plane 节点升级成功，Worker 节点升级失败，请联系 SmartX 售后工程师进行问题定位和处理。

---

## 管理工作负载集群 > 删除工作负载集群

# 删除工作负载集群

**注意事项**

- 工作负载集群删除后不可恢复。集群中的虚拟机会全部被删除；物理机则仅被解除与集群的关联，并清除 SKS 在物理机被添加到集群阶段为其安装的配置文件和其他参数设置，仍可添加至其他物理机集群。
- 如果工作负载集群使用了 SMTX ZBS CSI 插件，并且目标存储集群与 SKS 管控集群不被同一个 CloudTower 管理，在删除集群时，请先删集群中由您或您的工作负载创建的持久卷，否则对应的存储资源将会残留在目标存储集群中。

**操作步骤**

1. 在工作负载集群列表中单击目标工作负载集群的显示名称，进入工作负载集群的**概览**页面。
2. 在右上角单击 **...**，选择**删除集群**。
3. 在弹出的**删除集群**对话框中，确认要删除的工作负载集群名称。
4. 单击**删除**。

---

## 管理容器镜像仓库

# 管理容器镜像仓库

您可以在 CloudTower 的**容器镜像仓库**界面创建容器镜像仓库，用于存储和管理您的容器镜像。

创建完成后，您可以在 SKS 中将其作为**内部容器镜像仓库**配置给工作负载集群使用，使工作负载集群能够从中拉取工作负载需要使用的容器镜像；也可以在其他标准的 Kubernetes 集群中使用。

---

## 管理容器镜像仓库 > 创建容器镜像仓库

# 创建容器镜像仓库

详细操作请参考[创建容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_77)。

---

## 管理容器镜像仓库 > 查看容器镜像仓库信息

# 查看容器镜像仓库信息

1. 进入 CloudTower 的**容器镜像仓库**界面，在左侧导航栏中单击**概览**，可通过**容器镜像仓库**卡片查看当前系统中已创建的容器镜像仓库总数及其状态。

   | 状态 | 描述 |
   | --- | --- |
   | 创建中 | 容器镜像仓库正在创建。 |
   | 就绪 | 容器镜像仓库已就绪，可以正常提供服务。 |
   | 更新中 | 容器镜像仓库正在更新配置参数，暂时不能提供服务。 |
   | 升级中 | 容器镜像仓库正在升级。 |
   | 异常 | 容器镜像仓库出现异常导致无法运行。可能导致异常的原因包括：`创建失败`、`更新失败`、`升级失败`、`删除失败`等。 |
   | 删除中 | 容器镜像仓库正在删除，相关数据正在被清除。 |
2. 单击**容器镜像仓库**卡片或左侧导航栏的**容器镜像仓库**，可查看容器镜像仓库列表。选中某一容器镜像仓库，可查看该容器镜像仓库的详细信息。

   - 列表和详情中将展示容器镜像仓库虚拟机当前的 **CPU 使用率**、**内存使用率**以及**数据盘存储使用率**，其余参数说明请参见[创建容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_77)。
   - 单击**域名**或 **IP 地址**链接，可访问 Harbor Web 控制台。
   - 单击**所属 SMTX OS 集群**链接、**所属主机**链接或**所属虚拟机**链接，可跳转至相应页面查看集群、主机或虚拟机的详情。

---

## 管理容器镜像仓库 > 扩容容器镜像仓库

# 查看容器镜像仓库信息

1. 进入 CloudTower 的**容器镜像仓库**界面，在左侧导航栏中单击**概览**，可通过**容器镜像仓库**卡片查看当前系统中已创建的容器镜像仓库总数及其状态。

   | 状态 | 描述 |
   | --- | --- |
   | 创建中 | 容器镜像仓库正在创建。 |
   | 就绪 | 容器镜像仓库已就绪，可以正常提供服务。 |
   | 更新中 | 容器镜像仓库正在更新配置参数，暂时不能提供服务。 |
   | 升级中 | 容器镜像仓库正在升级。 |
   | 异常 | 容器镜像仓库出现异常导致无法运行。可能导致异常的原因包括：`创建失败`、`更新失败`、`升级失败`、`删除失败`等。 |
   | 删除中 | 容器镜像仓库正在删除，相关数据正在被清除。 |
2. 单击**容器镜像仓库**卡片或左侧导航栏的**容器镜像仓库**，可查看容器镜像仓库列表。选中某一容器镜像仓库，可查看该容器镜像仓库的详细信息。

   - 列表和详情中将展示容器镜像仓库虚拟机当前的 **CPU 使用率**、**内存使用率**以及**数据盘存储使用率**，其余参数说明请参见[创建容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_77)。
   - 单击**域名**或 **IP 地址**链接，可访问 Harbor Web 控制台。
   - 单击**所属 SMTX OS 集群**链接、**所属主机**链接或**所属虚拟机**链接，可跳转至相应页面查看集群、主机或虚拟机的详情。

---

## 管理许可

# 管理许可

SKS 有**试用许可**、**订阅许可**和**永久许可**三种许可类型，并提供按 **vCPU 数**许可和按 **CPU 插槽数**许可两种许可方式。

首次使用自动生成试用许可，具体许可信息如下表所示。

| 参数 | 描述 |
| --- | --- |
| 序列号 | SKS 的序列号 |
| 版本 | 标准版 |
| 许可类型 | 试用许可 |
| 过期时间 | 90 天（自首次试用的日期开始计算）  **说明**：试用许可过期后仍可再次安装 SKS，但会保持试用许可的过期状态。 |
| 许可单元 | - 许可方式：同时支持**按 vCPU 数**许可和**按 CPU 插槽数**许可 - 许可单元数量：不限 |

试用到期后您可以参考[许可说明](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_81)按需购买许可，在 CloudTower 中可以查看许可和更新许可码。

---

## 管理许可 > 许可说明

# 许可说明

SKS 管控集群不占用许可数量，仅工作负载集群会占用许可数量。

由于工作负载集群支持**虚拟机集群**和**物理机集群**两种类型，下面将分别介绍不同类型下许可方式的选择和许可数量计算。

- 当您计划仅使用虚拟机集群时，支持按 vCPU 数许可和按 CPU 插槽数许可两种方式，推荐使用按 vCPU 数许可的方式。

  - **按 vCPU 数许可**：该许可方式规定了工作负载集群 Control Plane 节点和 Worker 节点对应的虚拟机所分配的 vCPU 总数。
  - **按 CPU 插槽数许可**：该许可方式规定了可用于创建工作负载集群的 SMTX OS（ELF）集群的物理 CPU 插槽总数。
- 当您计划仅使用物理机集群时，仅可以使用按 CPU 插槽数许可的方式。该许可方式规定了工作负载集群 Worker 节点所属物理机的物理 CPU 插槽总数。
- 当您计划同时使用虚拟机集群和物理机集群时，可以统一使用按 CPU 插槽数许可的方式，也可以虚拟机集群使用按 vCPU 数许可、物理机集群使用按 CPU 插槽数许可。推荐统一使用按 CPU 插槽数许可的方式。

  - **统一按 CPU 插槽数许可**：该许可方式规定了虚拟机集群类型的工作负载集群所属 SMTX OS（ELF）集群的物理 CPU 插槽数以及物理机集群类型的工作负载集群 Worker 节点所属物理机的物理 CPU 插槽数的总和。对于虚拟机集群与物理机集群各自的 CPU 插槽数不作限制，您可以在 CPU 插槽总数的许可范围内按需调整使用比例。

    > **说明**：
    >
    > 如您原先已购买按 vCPU 数方式的许可，希望统一使用按 CPU 插槽数的许可时，请联系 SmartX 客户经理帮助您完成许可转换。
  - **虚拟机集群按 vCPU 数、物理机集群按 CPU 插槽数许可**：该许可方式分别规定了虚拟机集群 Control Plane 节点和 Worker 节点对应的虚拟机所分配的 vCPU 总数，以及物理机集群 Worker 节点所属物理机的物理 CPU 插槽总数。

**计算示例**

假设规划的工作负载集群如下表所示：

| 工作负载集群名称 | vCPU 总数 | 所属 SMTX OS（ELF）集群或所属物理机集群 | 物理 CPU 插槽总数 |
| --- | --- | --- | --- |
| 工作负载集群 A | 32 vCPU | SMTX OS（ELF）集群 A | 8 psocket |
| 工作负载集群 B | 40 vCPU | SMTX OS（ELF）集群 A | 8 psocket |
| 工作负载集群 C | 32 vCPU | SMTX OS（ELF）集群 C | 4 psocket |
| 工作负载集群 D | - | 物理机集群 D | 16 psocket |

统一按 CPU 插槽数许可时，所需的许可单元点数为 `8 + 4 + 16 = 28 psocket`；虚拟机集群按 vCPU 数、物理机集群按 CPU 插槽数许可时，虚拟机集群需要的许可单元点数为 `32 + 40 + 32 = 104 vCPU`，物理机集群需要的许可点数为 `16 psocket`。

---

## 管理许可 > 查看许可

# 查看许可

在 CloudTower 的 **Kubernetes 服务**界面，单击**设置** > **软件许可**，即可查看 SKS 的许可信息。

| 参数 | 描述 |
| --- | --- |
| 序列号 | SKS 的序列号。 |
| 版本 | SKS 的软件版本，目前只有一种软件版本，即标准版。 |
| 许可类型 | SKS 有以下三种许可类型：  - 试用许可：首次部署 SKS 服务后的许可类型，默认有效期为 90 天，且不限制许可单元数量。 - 永久许可：有效期为永不过期。 - 订阅许可：根据需要选择订阅时长，更为灵活。 |
| 过期时间 | 当许可类型为**试用许可**或**订阅许可**时，展示许可的过期时间。 **说明**：许可过期后，所有工作负载集群将切换至`暂停同步中`状态，并且您无法对工作负载集群执行生命周期管理相关的操作，例如集群和节点的创建、编辑、升级等操作，也无法配置集群插件和节点组自动伸缩。 |
| 许可单元 | 按 vCPU 数许可：   - 总额度：当前许可方式允许使用的 vCPU 总数。 - 已用额度：当前已使用的 vCPU 数。 - 可用额度：当前剩余可使用的 vCPU 数。 |
| 按 CPU 插槽数许可：   - 总额度：当前许可方式允许管理的 CPU 插槽总数。 - 已用额度：当前已使用的 CPU 插槽数。 - 可用额度：当前剩余可使用的 CPU 插槽数。 |

---

## 管理许可 > 更新许可

# 更新许可

当 SKS 面临以下情况时，需更新许可码：

- 更新许可类型：

  - 试用许可更新为订阅许可或永久许可。
  - 订阅许可更新为永久许可。
- 增加订阅许可或永久许可的许可单元数量。
- 延长试用许可或订阅许可的有效期。

更新许可时，需将当前软件许可信息及 SKS 软件版本号提供给 SmartX 客户经理，在完成商务流程后，客户经理将提供新的许可码。

**操作步骤**

1. 在 CloudTower 的 **Kubernetes 服务**界面，单击**设置** > **软件许可**，将许可码粘贴在**新许可码**后的信息栏中。
2. 单击输入框外部的空白区域，载入新许可信息。
3. 确认无误后，单击**更新**完成许可更新。

---

## 管理 SKS 服务设置 > 创建 SMTX ZBS CSI 接入配置

# 创建 SMTX ZBS CSI 接入配置

若工作负载集群需要使用 SMTX ZBS CSI 插件，并且目标存储集群为工作负载集群的虚拟机节点所在的 SMTX OS 集群，则在创建工作负载集群前，还需创建 SMTX ZBS CSI 接入配置。

**注意事项**

为 SMTX OS 集群添加 SMTX ZBS CSI 接入配置信息后，这些配置信息除虚拟机网络名称外，其余内容均不可编辑。

**操作步骤**

1. 在 **Kubernetes 服务**界面单击**设置** > **SMTX ZBS CSI 接入配置**，进入配置界面。
2. 单击右上角的 **+ 添加接入配置**，在弹出的**添加接入配置**对话框中配置如下信息。具体的配置要求可参见 [SMTX ZBS CSI 专用网卡网络要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_21)。

   - **SMTX OS 集群的接入虚拟 IP**

     | 参数 | 描述 |
     | --- | --- |
     | 集群 | 需要添加 SMTX ZBS CSI 接入配置的 SMTX OS 集群。  SMTX OS 集群需符合版本配套要求。 |
     | 接入虚拟 IP | 输入为 SMTX OS 集群规划的接入虚拟 IP，须位于 SMTX OS 存储网络的子网中。 |
   - **SMTX ZBS CSI 专属网卡使用的虚拟机网络**

     | 参数 | 描述 |
     | --- | --- |
     | 虚拟分布式交换机 | 与 SMTX OS 存储网络关联的虚拟分布式交换机的名称，不允许修改。 |
     | VLAN ID | 输入提前规划的虚拟机网络 VLAN ID。 |
     | 虚拟机网络名称 | 创建的虚拟机网络的名称。 |
3. 单击**保存**，完成 SMTX ZBS CSI 接入信息的配置。

**后续操作**

参考[创建工作负载集群 IP 池](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_12)创建 SMTX ZBS CSI 专用网卡的 IP 池。

---

## 管理 SKS 服务设置 > 管理节点相关文件

# 管理节点相关文件

节点相关文件包含用于创建管控集群和工作负载集群节点对应的虚拟机的节点模板文件（即虚拟机模板）和容器镜像文件，每个节点模板文件包含了预置的操作系统和某个特定 Kubernetes 版本的二进制安装文件。

## 上传节点相关文件

节点相关文件随当前 SKS 版本一起发布，请提前获取，并保存至本地。具体上传操作请参见[准备 Kubernetes 节点模板](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_08)。

## 查看节点相关文件

进入 CloudTower 的 **Kubernetes 服务**界面，单击**设置 > 节点相关文件**，可查看已上传的节点相关文件信息。

| 参数 | 描述 |
| --- | --- |
| 名称 | 节点相关文件的名称。 |
| Kubernetes 版本 | 节点相关文件对应的 Kubernetes 版本。 |
| 操作系统 | 节点相关文件对应的节点操作系统版本。 |
| CPU 架构 | 节点相关文件适用的 CPU 架构。 |
| 模板版本 | 节点相关文件的虚拟机模板版本。 |
| SKS 版本 | 节点相关文件对应的 SKS 版本。每个 SKS 版本在发布时会同时提供多个 Kubernetes 版本的节点相关文件。 |

## 删除节点相关文件

**注意事项**

当前被管控集群使用的节点相关文件，以及被现存工作负载集群所使用的节点相关文件均无法删除。

**操作步骤**

在**节点相关文件**列表中选中其中一个文件，单击 **...** 后选择**删除**，即可删除此文件。

---

## 管理 SKS 服务设置 > 管理物理机

# 管理物理机

在 CloudTower 的 **Kubernetes 服务**界面，单击**设置 > 物理机管理**，可以添加新的物理机至 SKS，也可以编辑、移除已添加至 SKS 的物理机。

---

## 管理 SKS 服务设置 > 管理物理机 > 查看物理机

# 查看物理机

## 查看物理机的基本信息

在物理机管理列表中，可以查看物理机的名称、状态、所属集群等基本信息。其中，**状态**一列展示物理机的当前状态，具体说明如下表所示。

| 状态 | 说明 |
| --- | --- |
| 可用 | 当前未被添加至某个物理机集群中作为 Worker 节点使用。 |
| 连接失败 | 无法被 SKS 控制器访问，此时**出错操作**一列将显示 SKS 最后一次执行的操作，请根据此操作检查对应的设置是否正确。 |
| 系统信息收集失败 | 收集操作系统包管理类型、CPU 架构、sudo 权限状态失败。请检查网络连接是否正常，物理机是否关机。 |
| 系统验证失败 | 系统信息收集成功，但操作系统、CPU 架构或包管理器不受支持，或者无 root 或 sudo 权限。请检查物理机的操作系统、CPU 架构、SSH 账号是否符合要求。 |
| 初始化中 | 信息已注册至 SKS，正在安装相关必要组件等，使其达到“可用”状态。 |
| 初始化失败 | 相关必要组件安装失败。请联系 SmartX 售后工程师进行处理。 |
| 元数据收集中 | 操作系统和硬件信息正在被收集中。 |
| 元数据收集失败 | 操作系统和硬件信息收集失败。请联系 SmartX 售后工程师进行处理。 |
| 制备中 | “可用”到“使用中”的中间态，正在将控制权交给 Provider。 |
| 制备失败 | Provider Agent 启动失败。请联系 SmartX 售后工程师进行处理。 |
| 使用中 | 当前已被添加至某个物理机集群中作为 Worker 节点使用。 |
| 清理中 | 已解除与物理机集群的关联，正在清理集群配置文件，使其恢复至“可用”的状态。 |
| 清理失败 | 集群配置文件清理失败。请联系 SmartX 售后工程师进行处理。 |

## 查看物理机的详细信息

您还可以通过物理机的 Custom Resource YAML 文件查看物理机的硬件配置、网络设置、操作系统版本以及元数据信息。

**操作步骤**

1. 在物理机管理列表中，在需要编辑的物理机右侧单击 **...** > **查看物理机详细信息**。
2. 在弹出的**查看物理机详细信息**对话框中，查看物理机的 Custom Resource YAML 文件的具体内容。此外，您还可以选择以下方式中的一种获取内容：
   - 在对话框右下角单击**下载**，下载整个文件。
   - 在对话框左下角单击**复制**，复制文件的内容。

---

## 管理 SKS 服务设置 > 管理物理机 > 添加物理机

# 添加物理机

详细操作请参考[在 SKS 界面添加物理机](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_10#%E7%AC%AC-3-%E6%AD%A5%E5%9C%A8-sks-%E7%95%8C%E9%9D%A2%E6%B7%BB%E5%8A%A0%E7%89%A9%E7%90%86%E6%9C%BA)。

---

## 管理 SKS 服务设置 > 管理物理机 > 编辑物理机

# 编辑物理机

**注意事项**

物理机名称不支持编辑。如果物理机已添加至集群，则仅支持修改 SSH 账号的密码和密钥。

**操作步骤**

1. 在物理机管理列表中，在需要编辑的物理机右侧单击 **...** > **编辑物理机**。
2. 在弹出的**编辑物理机**对话框中，修改物理机的配置信息。
3. 单击**保存**。

编辑完成后，请在物理机管理列表的物理机右侧单击 **...** > **刷新主机信息**。

---

## 管理 SKS 服务设置 > 管理物理机 > 移除物理机

# 移除物理机

**注意事项**

- 仅支持移除未添加至物理机集群的物理机。
- 如果物理机曾被添加到集群，则移除后可能无法完全恢复到物理机添加至 SKS 前的状态，会残留一些集群配置文件，如后续需再添加该物理机建议先重启物理机。
- 移除操作无法撤回。
- 若需要移除的物理机节点的**连接状态**为`失败`，建议先排查失败原因并解决问题，使**连接状态**恢复为`成功`，再进行移除操作，否则移除后物理机上可能会有 K8s 集群的文件和配置残留，需要自行重装操作系统或联系 SmartX 售后工程师手动清理。

**操作步骤**

1. 在物理机管理列表中，在需要移除的物理机右侧单击 **...** > **移除物理机**。
2. 在弹出的**移除物理机**对话框中，确认要移除的物理机的名称。
3. 单击**移除**。

---

## 管理 SKS 服务设置 > 管理 IP 池

# 管理 IP 池

SKS 通过 IP 池来池化 IP 资源，一个 IP 池可以有多个 IP 范围。

IP 池有两种类型：管控集群 IP 池和工作负载集群 IP 池。

- 管控集群 IP 池在部署 SKS 时创建，只有一个，不可删除，可以在创建后进行编辑。
- 工作负载集群 IP 池在创建工作负载集群前创建，后续也可以编辑和删除。支持创建多个工作负载集群 IP 池。

## 创建工作负载集群 IP 池

详细操作请参考[创建工作负载集群 IP 池](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_12)。

## 编辑管控/工作负载集群 IP 池

1. 在 **Kubernetes 服务**界面单击**设置** > **IP 池管理**，系统展示所有管控/工作负载集群的 IP 池列表。
2. 在列表中选中待编辑的管控/工作负载集群 IP 池，单击 **...** 后选择**编辑**，即可修改管控/工作负载集群的 IP 范围。

## 删除工作负载集群 IP 池

**注意事项**

如果 IP 池中有正在使用的 IP，则不支持删除该 IP 池。

**操作步骤**

1. 在 **Kubernetes 服务**界面单击**设置** > **IP 池管理**，系统展示所有管控/工作负载集群的 IP 池列表。
2. 在列表中选中待删除的工作负载集群 IP 池，单击 **...** 后选择**删除**，即可删除工作负载集群 IP 池。

---

## 管理 SKS 服务设置 > 管理全局配置 > 配置受信任容器镜像仓库

# 配置受信任容器镜像仓库

支持全局配置一个或多个受信任的容器镜像仓库。

全局配置的容器镜像仓库将作为创建工作负载集群时受信任容器镜像仓库的默认值，使工作负载集群能够从容器镜像仓库中拉取工作负载需要使用的容器镜像。修改全局配置仅对之后创建的工作负载集群生效。

**前提条件**

- 添加内部容器镜像仓库前，请确保已根据[管理容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_70)章节成功创建了容器镜像仓库。
- 添加外部容器镜像仓库前，请提前获取外部容器镜像仓库的访问地址和 CA 证书（可选），并确保工作负载集群可以正常连接至容器镜像仓库。

**操作步骤**

1. 进入 CloudTower 的 **Kubernetes 服务**界面，在左侧导航栏中单击**设置 > 全局配置**，默认进入**全局配置 > 容器镜像仓库**页面。
2. 单击 **+ 添加容器镜像仓库**。

   具体参数说明与为工作负载集群配置受信任的容器镜像仓库一致，请参见[管理受信任容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_65)。
3. 单击**保存**。

---

## 管理 SKS 服务设置 > 管理全局配置 > 配置服务时间

# 配置服务时间

NTP（Network Time Protocol，网络时间协议）用于在分布式系统中同步时间。配置 NTP 服务器可确保 SKS 容器镜像仓库、管控集群以及所有工作负载集群内的节点时间同步。

由于 SKS 通过 CloudTower 进行管理，当前支持同步 CloudTower 中已配置的 NTP 服务器信息。

**前提条件**

请确保 SKS 容器镜像仓库虚拟机、管控集群节点虚拟机、以及所有工作负载集群的节点虚拟机与 NTP 服务器之间网络连通。

**注意事项**

对于新部署的 SKS 集群，默认将**自动同步 CloudTower 中的 NTP 配置**。如果 CloudTower 中还未配置 NTP 服务器，请先参考《CloudTower 使用指南》的**配置 NTP 服务器**章节，添加 NTP 服务器地址。

**操作步骤**

1. 进入 CloudTower 的 **Kubernetes 服务**界面，在左侧导航栏中单击**设置 > 全局配置**，默认进入**全局配置 > 容器镜像仓库**页面。
2. 单击**服务时间**页签，查看当前的时间配置。

   - **NTP 服务器**：展示 CloudTower 中已配置的所有 NTP 服务器地址。当 CloudTower 中未配置 NTP 服务器时，该项显示为 `-`。单击**去配置**可跳转至 **CloudTower 时间**页面，为 CloudTower 配置 NTP 服务器。
   - **自动同步 CloudTower 中的 NTP 配置**：

     - 勾选该项后，系统每 10 分钟将自动同步 CloudTower 中已配置的 NTP 服务器信息。
     - 取消勾选该项后，系统将保留最近一次的 NTP 配置，不再进行自动同步。
   - **立即同步**：勾选**自动同步 CloudTower 中的 NTP 配置**后，您还可以通过单击**立即同步**，手动触发配置同步。
3. 单击**保存**。

   当 **NTP 服务未同步**或**节点时钟与 NTP 服务器出现偏差**时，系统将自动触发相应报警，您可以在 CloudTower 的**报警**页面查看并处理报警信息，具体操作请参考[查看报警信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_108)。

---

## 管理 SKS 系统服务

# 管理 SKS 系统服务

在 **Kubernetes 服务**界面的**设置**界面中，您可以为 SKS 系统服务关联可观测性服务、查看 SKS 系统服务的监控信息和报警信息，以及查看 SKS 容器镜像仓库信息。另外，针对管控集群，您还可以查看集群的相关信息、下载集群的 Kubeconfig 文件、提升集群至高可用模式、以及暂停/恢复同步集群；

> **注意**：
>
> - 管控集群的 Control Plane 证书存放于 Control Plane 节点，由每个节点独立维护。证书默认有效期为 1 年，过期后管控集群将不再可用。
> - 系统从 Control Plane 节点创建之日起开始计算证书的有效期，当 Control Plane 证书距离过期时间剩余 30 天时，系统自动触发证书更新操作，Control Plane 节点将依次进行滚动更新以更新证书，请确保管控集群 IP 池中存在未被使用的 IP。更新证书期间可能会导致大约 15 秒无法连接至管控集群，若希望避免此影响，您可在 Control Plane 证书距离过期时间大于 30 天时，选择合适时机手动替换所有 Control Plane 节点以更新证书。

---

## 管理 SKS 系统服务 > 为 SKS 系统服务启用监控、报警、日志、事件和审计功能

# 为 SKS 系统服务启用监控、报警、日志、事件和审计功能

**关联规则**

SKS 系统服务仅能被一个可观测性服务关联。

**前提条件**

- 管控集群处于`就绪`状态。
- 当前 CloudTower 环境中已准备符合要求的可观测性服务，具体要求可参考《SKS 部署与升级指南》中的[规划管控集群插件](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_14)小节。
- SKS 容器镜像仓库虚拟机、管控集群节点虚拟机的虚拟网卡所在虚拟机网络均与可观测性服务虚拟机的虚拟网卡所在虚拟机网络三层互通。
- 为需要关联的可观测性服务配置与 CloudTower 相同的 NTP 服务器，以免影响监控、日志等信息的正常获取。详细配置说明参考《可观测性平台用户指南》的**配置 NTP 服务器**章节。

**操作步骤**

1. 在 **Kubernetes 服务**界面单击**设置** > **可观测性配置**，进入可观测性配置界面。
2. 在可观测性配置界面中启用**关联可观测性服务**。
3. 选择需要关联的可观测性服务。
4. 启用**功能启用状态**，一键启用监控、报警、日志、事件和审计功能。
5. 单击**保存**。

   保存成功后：

   - 当前界面将展示**关联状态**，当该状态显示`已关联`时，表明 SKS 系统服务与可观测性服务已关联成功。
   - 您可以在 **Kubernetes 服务** > **概览**界面的**管控集群插件状态**中，通过查看监控、日志、事件、审计对应的插件状态是否正常来判断功能是否成功启用。您可参考[查看 SKS 概览](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_04)了解各功能对应的插件。

     启用成功后，在 **Kubernetes 服务** > **设置**界面单击**监控**、**报警**、**日志**、**事件**、**审计**可以分别查看对应的数据信息，查询操作与工作负载集群类似，可参考[查看监控信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_66)、[查看报警信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_108)、[查看日志信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_67)、[查看事件信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_61)、[查看审计信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_72)。其中，SKS 容器镜像仓库的监控信息可通过在**监控**界面的筛选下拉框中选择 **System Service/ Registry Harbor** 进行筛选。
   - 若关闭**功能启用状态**，您将无法查看相关功能数据，关闭前未解决的报警将自动解决。可观测性服务未更换时，您可以在重新启用后查看保存期限内的监控、日志、事件和审计信息。

**后续操作**

- 若需要更换可观测性服务，可直接在**可观测性配置**界面中切换可观测性服务，再单击**保存**。

  切换后，您将无法查看切换前的监控、日志、事件和审计信息，切换前未解决的报警将自动解决。
- 若需要查看、编辑报警规则，可以进入 CloudTower 的**报警** > **报警规则**界面，在界面顶部搜索框中的**资源类型**选项中，通过 `SKS 系统服务`、`SKS 容器镜像仓库`、`SKS 集群`、`SKS 集群节点`、`持久卷`或`持久卷申领`字段筛选出与 SKS 相关的报警规则。
- 若需要配置报警通知，可以在 CloudTower 的**报警** > **通知配置**界面创建通知配置，详细操作说明可参考《可观测性平台用户指南》的**管理报警功能**章节。

---

## 管理 SKS 系统服务 > 查看管控集群信息

# 查看管控集群信息

在 **Kubernetes 服务**界面单击**设置** > **管控集群**，可查看 SKS 管控集群的集群信息、节点信息和集群事件。

## 集群信息

| 参数 | 描述 |
| --- | --- |
| Control Plane 虚拟 IP | 管控集群的 Control Plane 虚拟 IP。 |
| Kubernetes 版本 | 管控集群的 Kubernetes 版本。 |
| 状态 | 管控集群当前所处的状态，分为以下几种：   - 运行中：管控集群中的所有节点已就绪。 - 就绪：管控集群中的所有节点和插件均已就绪，集群已达到可以正常服务的状态。 - 更新中：管控集群正在提升至高可用模式。 - 升级中：管控集群正在升级。 - 暂停同步中：管控集群被[暂停同步](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_98)。暂停同步后，即使 Kubernetes 集群当前状态与期望状态不符，也不会主动更新。 - 异常：管控集群出现异常。可能导致异常的原因有升级失败和更新失败等。 |
| 部署模式 | 部署管控集群时所使用的部署模式。节点角色、个数、以及单个节点所在的虚拟机所占用的资源与部署模式有关。   - 高可用模式 - 普通模式 |
| 所属 SMTX OS 集群 | 管控集群节点对应的虚拟机所在的 SMTX OS 集群。 |
| vCPU 使用率 | 管控集群已使用的 vCPU 占集群中总 vCPU 的百分比。 |
| 内存使用率 | 管控集群已使用的内存占集群中总内存的百分比。 |
| 时区 | 管控集群的时区。 |

## 节点信息

| 参数 | 描述 |
| --- | --- |
| 名称 | 集群节点的名称。 |
| 节点角色 | 集群节点的角色，包括 Control Plane 节点和 Worker 节点两种。 |
| 状态 | 节点当前的状态   - 就绪 - 未就绪 - 未知 |
| IP | 节点的 IP。 |
| 所属主机 | 节点所属的主机的名称。 |
| CPU | 为节点分配的 vCPU 数量。 |
| CPU 使用率（%） | 节点已使用的 vCPU 占集群中可分配 vCPU 的百分比。 |
| 内存 | 节点中可使用的内存总量。 |
| 内存使用率（%） | 节点已使用的内存占集群中可使用内存的百分比。 |
| 存储使用率（%） | 节点已使用的存储占比存储总分配量。 |
| 磁盘空间压力 | 节点的磁盘空间使用情况是否具有压力，可能有以下几种状态：   - 无压力 - 有压力 - 未知 |
| 内存压力 | 节点的内存使用情况是否具有压力，可能有以下几种状态：   - 无压力 - 有压力 - 未知 |
| 进程压力 | 节点的进程是否具有压力，可能有以下几种状态：   - 无压力 - 有压力 - 未知 |
| 网络可用性 | 节点的网络是否可用，可能有以下几种状态：   - 可用 - 不可用 - 未知 |
| 创建时间 | 节点的创建时间，精确到秒。 |

## 事件

展示管控集群最近一小时发生的事件。您可参考[查看事件信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_61)了解事件列表中各项参数的含义，在事件信息右侧单击 **...** > **查看详情**，可以查看详细的事件信息。

若您已[为 SKS 系统服务启用监控、报警、日志、事件和审计功能](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_109)，在事件列表右上方单击**查看更多**，即可跳转至**设置 > 事件**界面查看事件信息，查询操作与工作负载集群类似，可参考[查看事件信息](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_61)。

---

## 管理 SKS 系统服务 > 提升管控集群至高可用模式

# 提升管控集群至高可用模式

当管控集群的部署模式为普通模式时，可平滑提升至高可用模式，但需提前确认管控集群所属的 SMTX OS 集群的剩余资源和管控集群的 IP 池满足提升要求，详细操作方式请参考《SMTX Kubernetes 服务部署与升级指南》的[提升 SKS 至高可用模式](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_25)小节。

---

## 管理 SKS 系统服务 > 下载管控集群 Kubeconfig 文件

# 下载管控集群 Kubeconfig 文件

Kubeconfig 文件中包含了访问管控集群所需的访问地址和认证凭据，可结合 kubectl 命令行工具或其他客户端来使用。您可参考以下步骤获取集群的 Kubeconfig 文件内容，然后选择不同的方式来访问管控集群，具体的访问方式可以参见 Kubernetes 官网的[访问集群](https://kubernetes.io/zh-cn/docs/tasks/access-application-cluster/access-cluster/)章节。

**注意事项**

管控集群创建完成后，Kubeconfig 文件每隔 183 天将更新一次，每份文件的有效期均为一年，具体计算方式如下：

- Kubeconfig 文件更新之前，Kubeconfig 文件的过期时间 = 集群创建时间 + 365 天
- Kubeconfig 文件更新之后，Kubeconfig 文件的过期时间 = 文件最近更新时间 + 365 天

**操作步骤**

1. 在 **Kubernetes 服务**界面单击**设置** > **管控集群**，在界面右上角单击**下载 Kubeconfig**。
2. 在弹出的**下载 Kubeconfig** 对话框中将展示 Kubeconfig 文件的具体内容，选择以下方式中的一种获取内容：
   - 在对话框右下角单击**下载**，下载整个文件。
   - 在对话框左下角单击**复制**，复制文件的内容。

---

## 管理 SKS 系统服务 > 暂停/恢复同步管控集群

# 暂停/恢复同步管控集群

Kubernetes 采用声明式的机制来定义某个资源的期望状态，并保证资源的实际状态与期望状态一致。当资源的实际状态与用户定义的期望状态不一致时，Kubernetes 会自动执行必要的更改，以确保二者保持一致，该过程即为**同步**。

当您需要进行集群维护、故障排查等操作时，可使用**暂停同步**功能，暂时停止集群同步。暂停同步后，即使集群的实际状态与期望状态不一致，也不会自动调整。操作完成后，您可以使用**恢复同步**功能，将集群状态恢复至期望状态。

**注意事项**

- 处于**暂停同步中**状态的管控集群，不支持提升 SKS 至高可用模式或升级 SKS 服务版本。
- 暂停同步会导致集群的资源状态与期望状态不一致，请避免集群长期处于暂停同步状态。

**操作步骤**

1. 单击**设置** > **管控集群**，进入管控集群详情界面。
2. 在右上角单击 **...**，选择**暂停同步**或**恢复同步**。

---

## 管理 SKS 系统服务 > 查看 SKS 容器镜像仓库信息

# 查看 SKS 容器镜像仓库信息

进入 CloudTower 的 **Kubernetes 服务**界面，在左侧导航栏中单击**设置 > SKS 容器镜像仓库**，可查看 SKS 容器镜像仓库的信息。

> **注意**：
>
> SKS 容器镜像仓库仅用于存放 SKS 使用的系统容器镜像，请勿将业务镜像上传至 SKS 容器镜像仓库，否则将导致该仓库不可用。业务镜像请上传至容器镜像仓库，创建容器镜像仓库的操作可参考[管理容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_70)小节。

| 参数 | 描述 |
| --- | --- |
| 状态 | SKS 容器镜像仓库的状态。   - **就绪**：SKS 容器镜像仓库已就绪，可以正常提供服务。 - **升级中**：SKS 容器镜像仓库正在升级。 - **异常**：SKS 容器镜像仓库出现异常导致无法运行。 |
| 版本 | SKS 容器镜像仓库安装包的版本。 |
| IP 地址 | SKS 容器镜像仓库的访问地址。 |
| 域名 | SKS 容器镜像仓库的域名，如未配置则显示为 `-`。 |
| 所属 SMTX OS 集群 | SKS 容器镜像仓库虚拟机所在的 SMTX OS 集群，单击名称链接可跳转至集群概览页面。 |
| 所属主机 | SKS 容器镜像仓库虚拟机所在的主机，单击名称链接可跳转至主机概览页面。 |
| 对应虚拟机 | SKS 容器镜像仓库所在的虚拟机，单击名称链接可跳转至虚拟机详情页面。 |
| 子网掩码 | SKS 容器镜像仓库虚拟机的管理网卡的子网掩码。 |
| 网关 | SKS 容器镜像仓库虚拟机的管理网卡的网关。 |
| 虚拟机网络 | SKS 容器镜像仓库虚拟机的管理网卡所使用的虚拟机网络。 |
| vCPU 使用率 | SKS 容器镜像仓库虚拟机的 vCPU 使用率。 |
| 内存使用率 | SKS 容器镜像仓库虚拟机的内存使用率。 |
| 数据盘存储使用率 | SKS 容器镜像仓库虚拟机的数据盘存储使用率。 |

---

## 权限管理

# 权限管理

SKS 通过 CloudTower 进行运维管理。CloudTower 提供两种类型的角色：默认角色和自定义角色，并对不同角色赋予不同的操作权限。为用户分配角色后，该用户即可具有角色对应的操作权限。

- **默认角色**：相关权限说明请参见《CloudTower 使用指南》的**角色管理**章节。其中，具有**工作负载集群使用者**角色的用户可访问[工作负载集群使用者视图](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_120)。为用户分配该角色后，您还需要在工作负载集群的**项目管理**功能中进行项目内资源的权限分配，才可以管理工作负载集群中的相关资源。具体操作方式及项目内角色的权限说明，请参考[管理项目、角色与成员](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_116)章节。
- **自定义角色**：您可以根据业务需求在 CloudTower 的**角色管理**功能中创建自定义角色，对角色按照可分配权限项（如下表）的细分粒度赋予其操作权限，用于管理或运维 SKS 服务、工作负载集群等。详细步骤可参见《CloudTower 使用指南》的**创建自定义角色**小节。

  | 类别 | 可分配权限项 | 对应的操作权限 |
  | --- | --- | --- |
  | SKS 服务 | SKS 服务管理 | - 部署 SKS - 卸载 SKS - 暂停同步 - 恢复同步 - 升级 SKS - 提升 SKS 至高可用模式 - 下载管控集群 Kubeconfig 文件 |
  | SKS 许可管理 | 更新 SKS 许可 |
  | SKS 服务配置管理 | - 创建 SMTX ZBS CSI 接入配置 - 编辑 SMTX ZBS CSI 接入配置 - 删除 SMTX ZBS CSI 接入配置 - 上传节点相关文件 - 删除节点相关文件 - 编辑全局配置（添加、删除受信任容器镜像仓库） - 添加物理机 - 编辑物理机 - 移除物理机 |
  | 工作负载集群 | 创建工作负载集群 | 创建一个或多个工作负载集群 |
  | 删除工作负载集群 | 删除一个或多个工作负载集群 |
  | 编辑工作负载集群 | - 编辑集群显示名称 - 编辑 K8s 集群配置 - 管理节点组、节点 - 管理存储类 - 管理持久卷 - 管理工作负载、服务与网络、配置资源 - 管理插件 - 管理工作负载集群节点组自动伸缩 - 升级工作负载集群 - 打开集群控制台 - 打开节点控制台 - 打开 Pod 控制台 - 通过 YAML 创建任意 K8s 资源对象 - 管理项目 - 管理名字空间 - 管理项目成员 - 管理项目角色 |
  | 同步状态管理 | - 暂停同步 - 恢复同步 |
  | 下载工作负载集群 Kubeconfig 文件 | 下载工作负载集群 Kubeconfig 文件 |
  | 下载工作负载集群的集群规格文件 | 下载工作负载集群的集群规格文件 |
  | 容器镜像仓库（指在 CloudTower 的**容器镜像仓库**界面创建的容器镜像仓库） | 容器镜像仓库管理 | - 创建容器镜像仓库 - 编辑容器镜像仓库 - 删除容器镜像仓库 |

---

## 事件审计

# 事件审计

SKS 会以事件的形式记录您的下列操作，并支持在 CloudTower 的**事件**功能中进行查看。

| 类别 | 事件 |
| --- | --- |
| SKS 服务 | - 部署 SKS - 卸载 SKS - 升级 SKS - 提升 SKS 至高可用模式 |
| 软件许可 | 更新 SKS 软件许可 |
| SKS 容器镜像仓库 | - 部署 SKS 容器镜像仓库 - 卸载 SKS 容器镜像仓库 |
| IP 池 | - 创建工作负载集群 IP 池 - 编辑管控集群 IP 池 - 编辑工作负载集群 IP 池 - 删除工作负载集群 IP 池 |
| SMTX OS 集群的 SMTX ZBS CSI 接入配置 | - 创建 SMTX OS 集群的 SMTX ZBS CSI 接入配置 - 编辑 SMTX OS 集群的 SMTX ZBS CSI 接入配置 - 删除 SMTX OS 集群的 SMTX ZBS CSI 接入配置 |
| 节点相关文件 | - 上传节点相关文件 - 删除节点相关文件 |
| 工作负载集群 | - 创建工作负载集群 - 删除工作负载集群 |
| 容器镜像仓库（指在 CloudTower 的**容器镜像仓库**界面创建的容器镜像仓库） | - 创建容器镜像仓库 - 编辑容器镜像仓库 - 删除容器镜像仓库 |
| 物理机注册 | - 添加物理机 - 编辑物理机 - 移除物理机 |

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
