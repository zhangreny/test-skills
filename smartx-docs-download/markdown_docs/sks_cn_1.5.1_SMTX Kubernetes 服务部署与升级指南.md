---
title: "sks_cn/1.5.1/SMTX Kubernetes 服务部署与升级指南"
source_url: "https://internal-docs.smartx.com/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_preface"
sections: 41
---

# sks_cn/1.5.1/SMTX Kubernetes 服务部署与升级指南
## 关于本文档

# 关于本文档

本文档介绍了如何通过 CloudTower 部署 SMTX Kubernetes 服务（以下简称 “SKS”）、升级 SKS、以及卸载 SKS。

阅读本文档需了解 Kubernetes、CloudTower 和 SMTX OS 超融合软件，了解虚拟化、容器、分布式存储等相关技术，并具备数据中心操作的丰富经验。

---

## 文档更新信息

# 文档更新信息

- **2026-01-05：完善日志功能相关的 SKS 升级准备工作和后续操作说明**
- **2025-12-12：配合 SMTX Kubernetes 服务 1.5.1 正式发布**

  相较于 1.5.0 版本，本文档主要进行了以下更新：

  - **概述** > **集群插件**：更新 EIC 插件版本。
  - **升级 SKS**：更新升级前准备和升级步骤中的版本相关描述。

---

## 概述

# 概述

SMTX Kubernetes 服务（SMTX Kubernetes Service，简称 “SKS”）是 SmartX 企业云基础设施提供的 Kubernetes 服务，由北京志凌海纳科技股份有限公司自主研发。

通过预集成 Kubernetes 常用基础应用，以及整合业界领先的 SmartX 虚拟化、分布式存储、网络与安全等产品组件，帮助企业 IT 运维团队在多种 CPU 架构的服务器上轻松部署和管理生产级 Kubernetes 集群。

---

## 概述 > 产品架构

# 产品架构

SKS 产品的整体架构如图所示。

![](https://cdn.smartx.com/internal-docs/assets/62cb2be1/sks_user_guide_62.png)

---

## 概述 > 集群插件

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

## 概述 > 相关概念

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

## 部署前的规划

# 部署前的规划

CloudTower 为 SKS 提供 UI 界面，SKS 可通过 CloudTower 部署和管理，物理机类型的工作负载集群的 Conrtol Plane 节点、虚拟机类型的工作负载集群、管控集群以及 SKS 容器镜像仓库均运行在 SMTX OS 集群中。

下图为 SKS 的网络拓扑示例。SKS 容器镜像仓库与管控集群必须部署在同一个 SMTX OS 集群；CloudTower、管控集群、工作负载集群既可部署在同一个 SMTX OS 集群，也可以分别部署在不同的 SMTX OS 集群。

![](https://cdn.smartx.com/internal-docs/assets/62cb2be1/sks_user_guide_01.png)

实际部署场景与上述示例可能不同，SKS 集群使用的插件、集群的节点数量不同时，对资源、网络等要求也会有所不同。因此，在部署 SKS 前，请根据实际业务需求做好如下规划工作：

1. [确认版本配套要求](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_05)。
2. 根据[规划插件](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_14)中的说明，确认集群使用的插件。
3. 根据[规划集群节点数量](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_06)中的说明，确认集群的节点个数。
4. 根据[规划资源](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_09)中对 SKS 容器镜像仓库、管控集群以及工作负载集群资源要求的说明，确认待使用的集群中预留了足够的计算和存储资源。
5. 根据[规划网络](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_15)中对 SKS 容器镜像仓库、管控集群以及工作负载集群网络要求的说明，完成网络配置和 IP 规划。
6. 根据 [SKS 系统服务防火墙端口配置要求](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_26)和[工作负载集群防火墙端口配置要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_27)，在防火墙开放相应的协议和端口，以确保源端、目标端通信正常。
7. 若工作负载集群需要使用 GPU 设备，请根据[工作负载集群使用 GPU 设备要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_23)确认待使用的 SMTX OS 集群或物理机可满足使用 GPU 设备的要求。
8. 若工作负载集群需要使用在 CloudTower 的**容器镜像仓库**界面创建的容器镜像仓库，请根据[工作负载集群使用容器镜像仓库要求](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_104)进行准备。

---

## 部署前的规划 > 确认版本配套要求

# 确认版本配套要求

请参考《SMTX Kubernetes 服务发布说明》的[版本配套说明](/sks_cn/1.5.1/sks_release_notes/sks_release_notes_03)，确认您准备使用的所有 SMTX OS 集群和已安装的 CloudTower 满足配套要求。

---

## 部署前的规划 > 规划插件 > 规划管控集群插件

# 规划管控集群插件

管控集群将默认使用 Calico CNI、SMTX ELF CSI，也支持在集群部署后一键启用监控、报警、日志、事件和审计插件，您可参考[集群插件](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_22)了解各插件的详细介绍。

SKS 通过可观测性服务提供监控、报警、日志、事件和审计功能，如需启用对应插件，需确保可观测性服务满足以下要求。

- 版本为 1.4.2 及以上。
- 未关联除 SKS 系统服务、工作负载集群以外的其他集群或系统服务。

  建议一个可观测性服务关联的 SKS 对象不超过 10 个。
- 可观测性服务虚拟机的存储容量至少为 256 GiB，后续可按需扩容。
- 可观测性服务虚拟机的 CPU Steal Time 值不超过 5。

  可通过 SSH 方式登录至虚拟机并执行 top 命令查看该值，如下图。

  ![](https://cdn.smartx.com/internal-docs/assets/2df79858/sks_deploy_guide_12.png)

---

## 部署前的规划 > 规划插件 > 规划工作负载集群插件

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

## 部署前的规划 > 规划集群节点数量 > 规划管控集群节点数量

# 规划管控集群节点数量

请根据您的业务需求选择合适的 SKS 服务部署模式。不同部署模式下，管控集群中 Control Plane 节点和 Worker 节点的数量有所不同，具体说明如下表所示。

| 部署模式 | 适用场景 | 管控集群中节点的角色与数量 |
| --- | --- | --- |
| 高可用模式 | 适用于生产环境，可保证 Control Plane 高可用。 | 3 个 Control Plane 节点 |
| 3 个 Worker 节点 |
| 普通模式 | 适用于开发测试环境，可平滑提升至高可用模式。 | 1 个 Control Plane 节点 |
| 1 个 Worker 节点 |

---

## 部署前的规划 > 规划集群节点数量 > 规划工作负载集群节点数量

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

## 部署前的规划 > 规划资源

# 规划资源

物理机类型的工作负载集群的 Worker 节点将使用您自行准备的物理机资源。因此，若要创建物理机集群，您需要对作为 Worker 节点的物理机资源进行规划。

物理机类型的工作负载集群的 Conrtol Plane 节点、虚拟机类型的工作负载集群、管控集群、SKS 容器镜像仓库、以及在 CloudTower 的**容器镜像仓库**界面创建的容器镜像仓库均运行在 SMTX OS 集群中。因此，在部署前，您还需要结合实际环境、根据相关资源要求对待使用的 SMTX OS 集群进行资源规划，确保集群的计算和存储资源充足。

> **注意**：
>
> SKS 容器镜像仓库与管控集群必须部署在同一个 SMTX OS 集群中，因此需同时考虑 SKS 容器镜像仓库与管控集群对 SMTX OS 集群的资源要求。

---

## 部署前的规划 > 规划资源 > SKS 容器镜像仓库资源要求

# SKS 容器镜像仓库资源要求

运行 SKS 容器镜像仓库的虚拟机占用的计算和存储资源如下：

- vCPU：4 vCPU
- 内存：8 GiB
- 系统盘：20 GiB
- 数据盘：400 GiB

> **说明**：
>
> 存储策略为精简置备，所在集群未启用双活特性时为 2 副本、启用双活特性时为 3 副本。

---

## 部署前的规划 > 规划资源 > 管控集群资源要求

# 管控集群资源要求

管控集群占用的资源主要为集群节点占用的资源。不同 SKS 部署模式下，所需的资源用量有所不同。

请根据您选择的 SKS 部署模式，参考下表计算管控集群所需的资源。

| 部署模式 | 集群中节点的角色和数量 | 单个节点所在的虚拟机的资源要求 | 所需的资源总量 |
| --- | --- | --- | --- |
| 高可用模式 | 3 个 Control Plane 节点 | - 4 vCPU - 8 GiB 内存 - 200 GiB 存储空间 | - 36 vCPU - 72 GiB 内存 - 1200 GiB 存储空间 |
| 3 个 Worker 节点 | - 8 vCPU - 16 GiB 内存 - 200 GiB 存储空间 |
| 普通模式 | 1 个 Control Plane 节点 | - 4 vCPU - 8 GiB 内存 - 200 GiB 存储空间 | - 12 vCPU - 24 GiB 内存 - 400 GiB 存储空间 |
| 1 个 Worker 节点 | - 8 vCPU - 16 GiB 内存 - 200 GiB 存储空间 |

> **注意**：
>
> - CPU 非独占。
> - 存储策略为精简置备，所在集群未启用双活特性时为 2 副本、启用双活特性时为 3 副本。
> - 为确保管控集群高可用，Control Plane 节点将被强制放置在不同的物理主机。因此，您需要确保管控集群所在的 SMTX OS 集群中有足够的可用物理主机、以及充足的计算和存储资源，可以使每个 Control Plane 节点虚拟机分别运行在不同的物理主机，且每个 Worker 节点虚拟机运行在相同或不同的物理主机。

---

## 部署前的规划 > 规划资源 > 工作负载集群资源要求

# 工作负载集群资源要求

工作负载集群占用的资源主要为集群节点占用的资源。

- 集群的虚拟机节点，即虚拟机集群的所有节点和物理机集群的 Conrtol Plane 节点，将固定占用节点所在的 SMTX OS 集群资源。
- 集群的物理机节点，即物理机集群的 Worker 节点，将使用您自行准备的物理机的资源。

---

## 部署前的规划 > 规划资源 > 工作负载集群资源要求 > 集群虚拟机节点资源要求

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

## 部署前的规划 > 规划资源 > 工作负载集群资源要求 > 集群物理机节点资源要求

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

## 部署前的规划 > 规划网络

# 规划网络

为保证 CloudTower 虚拟机、SKS 容器镜像仓库、管控集群节点、工作负载集群节点之间能够正常通信，部署前请结合实际环境、根据相关网络要求提前做好规划。

---

## 部署前的规划 > 规划网络 > SKS 容器镜像仓库网络要求

# SKS 容器镜像仓库网络要求

SKS 容器镜像仓库虚拟机需配置 1 个虚拟网卡，用于与 CloudTower 虚拟机、管控集群节点、以及所有工作负载集群节点通信。

- SKS 容器镜像仓库虚拟机、管控集群节点虚拟机和 CloudTower 虚拟机的虚拟网卡所在的虚拟机网络之间需三层互通，并与工作负载集群节点的业务网卡所在网络三层互通。
- 若管控集群需启用监控、报警、日志、事件和审计插件，则 SKS 容器镜像仓库虚拟机与可观测性服务虚拟机的虚拟网卡所在的虚拟机网络之间需三层互通，以便后续为 SKS 系统服务关联可观测性服务。

![](https://cdn.smartx.com/internal-docs/assets/2df79858/sks_deploy_guide_01.png)

请提前规划 SKS 容器镜像仓库虚拟机的虚拟网卡所在的虚拟机网络、为该网卡分配 IP 地址、并获取网关和子网掩码信息。

如需使用域名访问 SKS 容器镜像仓库虚拟机，请提前规划域名，并按如下步骤完成配置：

1. 在 DNS 服务器中，配置 SKS 容器镜像仓库虚拟机域名与 IP 的双向解析记录。
2. 记录该 DNS 服务器的地址。
3. 登录 CloudTower 虚拟机，执行如下命令配置该 DNS 服务器地址。

   1. 查看当前 nameserver 配置。

      ```
      installer nameserver list
      ```
   2. 添加新的 nameserver 配置。

      ```
      installer nameserver set --values "114.114.114.114"    # 请在引号中按需追加或替换新的 DNS 地址，多个地址请使用半角逗号分隔
      ```

---

## 部署前的规划 > 规划网络 > 管控集群网络要求

# 管控集群网络要求

管控集群默认启用 SMTX ELF CSI 与 Calico CNI 插件，每个节点需配置 1 个虚拟网卡，用于与 CloudTower 虚拟机、容器镜像仓库虚拟机和工作负载集群节点进行通信。

## 网络连接要求

- SKS 容器镜像仓库虚拟机、管控集群节点虚拟机和 CloudTower 虚拟机的虚拟网卡所在的虚拟机网络之间需三层互通，并与工作负载集群节点的业务网卡所在网络三层互通。
- 若管控集群需启用监控、报警、日志、事件和审计插件，则集群节点虚拟机与可观测性服务虚拟机的虚拟网卡所在的虚拟机网络之间需三层互通，以便后续为 SKS 系统服务关联可观测性服务。

![](https://cdn.smartx.com/internal-docs/assets/2df79858/sks_deploy_guide_02.png)

## IP 配置要求

**IP 数量要求**

确认所在的虚拟机网络后，您需要为管控集群中每个节点的虚拟网卡配置一个 IP。另外，为了保证 Control Plane 的高可用，还需要为管控集群配置一个 Control Plane 虚拟 IP。

Control Plane 虚拟 IP 将被配置在管控集群的某一个节点上，之后即可通过该虚拟 IP 统一访问管控集群。

不同 SKS 服务部署模式下需要的最少 IP 数量如下表所示。

| 部署模式 | 所需 IP 数量 | IP 用途 |
| --- | --- | --- |
| 高可用模式 | 9 | - 1 个 Control Plane 虚拟 IP - 3 个 Control Plane 节点 IP - 3 个 Worker 节点 IP - 至少 2 个预留的节点 IP，用于后续 SKS 服务升级。预留的节点 IP 越多，升级速度越快 |
| 普通模式 | 5 | - 1 个 Control Plane 虚拟 IP - 1 个 Control Plane 节点 IP - 1 个 Worker 节点 IP - 至少 2 个预留的节点 IP，用于后续 SKS 服务升级。预留的节点 IP 越多，升级速度越快 |

**IP 分配方式及相应规划说明**

- 节点 IP 支持**通过 IP 池**自动分配

  IP 池可设置多个 IP 范围，请根据 IP 数量要求提前规划管控集群 IP 池的 IP 范围，并获取子网掩码、网关和 DNS 服务器信息。

  > **注意**：
  >
  > 若节点 IP 需使用域名访问 SKS 容器镜像仓库虚拟机，则必须获取能解析该域名的 DNS 服务器信息，否则可以使用公共的 DNS 服务器地址（例如 `1.1.1.1`）代替，但请勿使用 `127.0.0.1`。

  部署 SKS 时请根据规划配置管控集群 IP 池，系统将自动从该 IP 池中为每个节点配置静态 IP。

  部署 SKS 完成后，您仍可以按需编辑管控集群 IP 池。
- Control Plane 虚拟 IP 支持如下两种 IP 分配方式：

  - **通过 IP 池自动分配**

    系统将自动从管控集群 IP 池中为管控集群配置 Control Plane 虚拟 IP。
  - **通过手动输入方式设置**

    Control Plane 的虚拟 IP 除通过 IP 池自动分配外，也可以支持单独手动指定。您可以根据业务需求提前规划虚拟 IP，并在部署 SKS 时输入该 IP。

> **注意**：
>
> 上述 IP 地址均不能与以下 CIDR 范围内的任何 IP 地址重叠：
>
> - 169.254.0.0/16
> - 240.0.0.0/4
> - 224.0.0.0/4
> - 198.18.0.0/15
> - 127.0.0.0/8
> - 0.0.0.0/8
> - 管控集群的 Pod IP CIDR（默认为 172.16.0.0/16）
> - 管控集群的 Service IP CIDR（默认为 10.96.0.0/22）

---

## 部署前的规划 > 规划网络 > 工作负载集群网络要求 > 集群网络要求概述

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

## 部署前的规划 > 规划网络 > 工作负载集群网络要求 > 业务网卡网络要求

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

## 部署前的规划 > 规划网络 > 工作负载集群网络要求 > EIC 专用网卡网络要求（仅适用于虚拟机集群）

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

## 部署前的规划 > 规划网络 > 工作负载集群网络要求 > SMTX ZBS CSI 专用网卡网络要求

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

## 部署前的规划 > 规划防火墙端口 > SKS 系统服务防火墙端口配置要求

# SKS 系统服务防火墙端口配置要求

若管控集群节点对应的虚拟机、SKS 容器镜像仓库虚拟机、CloudTower 虚拟机和部署 SKS 服务的 SMTX OS 集群物理主机之间通信的网络存在防火墙，则防火墙需开放如下协议和端口（若无特殊说明，下面列举的端口均为 TCP 端口）。

| 源端 | 目标端 | 开放的协议和端口 | 用途 |
| --- | --- | --- | --- |
| 管控集群节点对应的虚拟机 | CloudTower 虚拟机 | 443 | CAPE、SMTX ELF CSI、EIC Adapter 等组件连接到 CloudTower API 服务 |
| 30443 | 管控集群热更新时访问 SKS-FileServer |
| CloudTower 虚拟机、管控集群节点对应的虚拟机、工作负载集群所有节点、访问 SKS 容器镜像仓库的其他 IP | SKS 容器镜像仓库虚拟机 | 443 | 拉取容器镜像或者访问管理 UI |
| CloudTower 虚拟机 | SKS 容器镜像仓库虚拟机 | 22 | 管理 SKS 容器镜像仓库 |
| ICMP（所有类型及代码） | SKS 容器镜像仓库虚拟机连通性检查 |
| 管控集群节点对应的虚拟机 | SKS 容器镜像仓库虚拟机 | 9090、9100、10414 | 获取 SKS 容器镜像仓库的指标 |
| CloudTower 虚拟机 | 管控集群节点对应的虚拟机和 Control Plane 虚拟 IP | 6443 | Kubernetes API Server |
| 30080 | SKS API Server |
| ICMP | 检测节点网络状态 |
| CloudTower 虚拟机 | 部署 SKS 服务的 SMTX OS 集群物理主机 | 3260、3261 | 上传系统服务所需虚拟机镜像 |
| 管控集群节点对应的虚拟机 | 管控集群节点对应的虚拟机 | 10100 | SKS 包管理器 |
| - IP-in-IP 协议（使用默认的 IP-in-IP 模式） - TCP：179（使用 BGP 模式） - TCP：5473 - UDP：51820、51821 - UDP：4789（使用 VXLAN 模式） | Calico CNI 插件，更详细的要求可参见 [Calico 官方文档](https://docs.tigera.io/calico/3.25/getting-started/kubernetes/requirements#network-requirements) |
| 9100 | Prometheus Node Exporter |
| 10249、10250、​10257、10259 | Kubernetes 组件的 Metrics API |
| 2379、2380 | Kubernetes etcd |
| 10250 | Kubernetes kubelet API |
| 9912、9913 | SMTX ELF CSI 插件 |
| 30443 | SKS 组件访问 SKS-FileServer |
| 管控集群 Control Plane 节点对应的虚拟机 | 管控集群 Control Plane 节点对应的虚拟机 | 10257 | Kubernetes kube-controller-manager |
| 10259 | Kubernetes kube-scheduler |
| 管控集群节点对应的虚拟机 | Everoute Controller 虚拟机 | 6443 | SMTX Everoute API |
| 管控集群节点对应的虚拟机 | 工作负载集群的 Control Plane 节点对应虚拟机和 Control Plane 虚拟 IP | 6443 | Kubernetes API Server |
| ICMP | 检测节点网络状态 |
| 管控集群节点对应的虚拟机 | 管控集群 Control Plane 节点对应的虚拟机和 Control Plane 虚拟 IP | 6443 | Kubernetes API Server |
| 工作负载集群所有节点 | 管控集群节点对应的虚拟机 | 30443 | 物理机、原地更新流程访问 SKS-FileServer |
| 管控集群节点对应的虚拟机 | 物理机类型的工作负载集群的 Worker 节点 | 22 | SKS 组件使用 SSH 访问物理机。如果有自定义的 SSH 端口，需要额外开放这些端口 |
| 18301 | SKS 组件访问物理机的 host-config-agent |
| 物理机类型的工作负载集群所有节点 | 管控集群节点对应的虚拟机 | ICMP | 允许管控集群与物理机之间互相通信 |
| 管控集群节点对应的虚拟机 | 物理机类型的工作负载集群所有节点和 Control Plane 虚拟 IP | ICMP | 允许管控集群与物理机之间互相通信 |
| 管控集群节点对应的虚拟机和 SKS 容器镜像仓库虚拟机 | CloudTower 中配置的 NTP 服务器 IP | UDP：123 | 启用同步 CloudTower NTP 配置功能后与 NTP 服务器通讯 |
| 管控集群节点对应的虚拟机和 SKS 容器镜像仓库虚拟机 | 可观测性服务虚拟机 IP | 80 | 关联可观测性服务时用于推送监控数据 |

---

## 部署前的规划 > 规划防火墙端口 > 工作负载集群防火墙端口配置要求

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

## 部署前的规划 > 工作负载集群使用 GPU 设备要求

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

## 部署前的规划 > 工作负载集群使用容器镜像仓库要求

# 工作负载集群使用容器镜像仓库要求

如果工作负载集群需要使用在 CloudTower 的**容器镜像仓库**界面创建的容器镜像仓库，请确认满足对容器镜像仓库的资源、网络和防火墙端口配置要求。

---

## 部署前的规划 > 工作负载集群使用容器镜像仓库要求 > 容器镜像仓库资源要求

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

## 部署前的规划 > 工作负载集群使用容器镜像仓库要求 > 容器镜像仓库网络要求

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

## 部署前的规划 > 工作负载集群使用容器镜像仓库要求 > 容器镜像仓库防火墙端口配置要求

# 容器镜像仓库防火墙端口配置要求

如果您的工作负载集群需要使用在 CloudTower 的**容器镜像仓库**界面创建的容器镜像仓库，当工作负载集群节点对应的虚拟机、CloudTower 虚拟机和容器镜像仓库虚拟机之间通信的网络存在防火墙时，防火墙需开放如下协议和端口（若无特殊说明，下面列举的端口均为 TCP 端口）。

| 源端 | 目标端 | 开放的协议和端口 | 用途 |
| --- | --- | --- | --- |
| CloudTower 虚拟机 | 容器镜像仓库虚拟机 | 22、443 | 管理容器镜像仓库 |
| ICMP（所有类型及代码） | 容器镜像仓库虚拟机连通性检查 |
| 工作负载集群节点对应的虚拟机、访问容器镜像仓库的其他 IP | 容器镜像仓库虚拟机 | 443 | 拉取容器镜像或者访问管理 UI |
| 容器镜像仓库虚拟机 | CloudTower 中配置的 NTP 服务器 IP | UDP：123 | 启用同步 CloudTower NTP 配置功能后与 NTP 服务器通讯 |

---

## 部署 SKS

# 部署 SKS

SKS 以 Kubernetes 集群的形式部署在选定的 SMTX OS 集群中，并作为管控集群来供系统使用，负责管理其他工作负载集群。

部署 SKS 需要首先部署 SKS 容器镜像仓库，再部署 SKS 服务。SKS 容器镜像仓库用于存放和管理 SKS 使用的所有系统容器镜像。

在部署 SKS 容器镜像仓库和 SKS 服务前，需要确认现场的部署环境满足相应的要求，并完成相关准备，建议您认真阅读[部署前的规划](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_04)。

---

## 部署 SKS > 部署 SKS 容器镜像仓库

# 部署 SKS 容器镜像仓库

SKS 容器镜像仓库用于存放和管理 SKS 使用的所有系统容器镜像，包括 SKS 组件的容器镜像、Kubernetes 组件的容器镜像等。SKS 容器镜像仓库运行在 SMTX OS 集群的一个虚拟机中，部署 SKS 时可以从仓库中自动拉取镜像。

**注意事项**

SKS 容器镜像仓库仅用于存放 SKS 使用的系统容器镜像，请勿将业务镜像上传至 SKS 容器镜像仓库，否则将导致该仓库不可用。业务镜像请上传至容器镜像仓库，创建容器镜像仓库的操作可参考《SMTX Kubernetes 服务管理指南》中的[管理容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_70)小节。

**前提条件**

- SKS 容器镜像仓库所在的 SMTX OS 集群符合版本配套要求。
- 已获取本版本的 SKS 容器镜像仓库安装文件，且安装文件的 CPU 架构需与 SKS 容器镜像仓库所在的 SMTX OS 集群的 CPU 架构保持一致。
- 已完成 [SKS 容器镜像仓库资源规划](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_10)和 [SKS 容器镜像仓库网络规划](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_16)。

**操作步骤**

1. 登录 CloudTower，进入 **Kubernetes 服务**的概览界面，系统提示当前 CloudTower 尚未部署 SMTX Kubernetes Service。
2. 单击**开始部署 SKS 容器镜像仓库**，在弹出的**部署 SKS 容器镜像仓库**对话框中输入以下信息。

   | 参数 | 描述 |
   | --- | --- |
   | SKS 容器镜像仓库安装文件 | 部署 SKS 容器镜像仓库所需要的安装文件，可以选择将本地的安装文件拖拽至文件区域，或者单击**选择文件**后从本地选择文件进行上传。 |
   | 集群 | 选择即将运行 SKS 容器镜像仓库的虚拟机所在的 SMTX OS 集群。  **说明**：  - 若选择的 SMTX OS 集群为启用双活特性的集群，则 SKS 容器镜像仓库的虚拟机在资源充足时将默认部署在该双活集群的优先可用域，且高可用（HA）重建优先级为高。 - 优先可用域故障时，可在次级可用域中自动新建，优先可用域恢复后对应虚拟机不会自动切回。 - 当前仅基于双活集群的两个可用域进行部署，不涉及仲裁节点。 |
   | 网络 | 设置 SKS 容器镜像仓库所在虚拟机的管理网卡的虚拟机网络、IP 地址、网关和子网掩码等信息。  - **虚拟机网络**：基于 SMTX OS 集群中关联了管理网络的虚拟分布式交换机所创建的虚拟机网络。要求 SKS 管控集群和工作负载集群节点对应的虚拟机所在的虚拟机网络与 SKS 容器镜像仓库虚拟机的虚拟机网络保证连通。 - **IP 地址**：管理网卡的 IP 地址。 - **网关**：管理网络的网关信息。 - **子网掩码**：管理网络的子网掩码信息。 |
   | 域名（可选） | 输入为 SKS 容器镜像仓库虚拟机规划的域名。  请确保已完成[域名相关配置](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_16)，以便 SKS 容器镜像仓库可被正确解析与访问。  如果该项留空，则需要通过虚拟机 IP 地址访问 SKS 容器镜像仓库。 |
   | CA 证书（可选） | SKS 容器镜像仓库仅支持通过 HTTPS 协议访问，可以为其配置一个 CA 签发的证书和证书密钥。  如果不指定，则系统会自动生成一个自签名 CA 证书。 |
3. 单击**确定**，开始部署 SKS 容器镜像仓库。在 CloudTower 的任务中心可以查看部署的状态。

---

## 部署 SKS > 部署 SKS 服务

# 部署 SKS 服务

SKS 容器镜像仓库部署成功后，系统提示可以继续部署 SKS 服务。部署完 SKS 服务后，系统将创建一个 SKS 管控集群。SKS 核心服务运行在 SKS 管控集群中，提供 SKS 的核心功能（如 SKS 集群管理器、SKS 集群插件管理器等）和 API。

**前提条件**

- 已成功部署 SKS 容器镜像仓库。
- 已获取 SKS 服务安装文件，且安装文件的 CPU 架构需与 SKS 容器镜像仓库所在 SMTX OS 集群的 CPU 架构保持一致。
- 已按照[部署前的规划](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_04)，完成管控集群相应的规划和准备工作。
- 若待部署管控集群的 SMTX OS 集群的主机 CPU 属于海光一号或二号处理器系列，则请确保 SMTX OS 集群的“虚拟机 CPU 兼容性”设置满足以下要求，否则请修改设置。

  | CPU 处理器系列 | SMTX OS 集群的“虚拟机 CPU 兼容性”要求 |
  | --- | --- |
  | 海光一号 | `主机透传`或 `Opteron_G3` |
  | 海光二号 | `EPYC`、`EPYC-IBPB` 或 `Opteron_G3` |

**操作步骤**

1. 在 CloudTower 的 **Kubernetes 服务**的概览界面，单击**开始部署 SKS 服务**，系统弹出**部署 SKS 服务**对话框。
2. 上传 SKS 服务安装文件并输入 MD5 码。

   可以选择将本地的安装文件拖拽至文件区域，或者单击**选择文件**后从本地上传文件。
3. 单击**下一步**，开始为 SKS 管控集群选择部署模式。

   关于每种部署模式的适用场景和所需占用的资源，可参考[管控集群资源要求](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_11)中的描述。

   > **说明**：
   >
   > - 若 SKS 服务部署在启用双活特性的 SMTX OS 集群中，则管控集群的 Control Plane 节点和 Worker 节点虚拟机将默认部署在该双活集群的优先可用域，且高可用（HA）重建优先级为高。优先可用域资源不足时可在次级可用域中部署，不涉及仲裁节点。
   > - 因优先可用域中部分主机异常而在次级可用域中新建的虚拟机，在优先可用域中主机恢复后不会自动切回。
4. 为 SKS 服务选择时区。系统默认选择浏览器的时区。

   此处所选时区将会作为管控集群的时区和工作负载集群的默认时区。管控集群的时区在 SKS 服务部署完成后无法编辑，工作负载集群的时区在集群创建时可以重新选择。
5. 单击**下一步**，根据[管控集群网络要求](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_17)，开始为 SKS 管控集群配置网络信息。

   - **节点网络**：为管控集群的每个节点配置通信的网络，可以选择 SKS 服务所在的 SMTX OS 集群中管理网络所在的虚拟分布式交换机上的一个 VLAN 为 Access 类型的虚拟机网络。
   - **管控集群 IP 池**：配置管控集群的 IP 池，配置完成后，可以为节点以及 Control Plane 虚拟 IP 灵活分配静态 IP，并负责 IP 的管理与回收。

     为集群的 IP 池设置 IP 范围时，同时还需设置子网掩码长度（8 ~ 32）和网关信息，并配置 DNS 服务器。支持为 IP 池添加多个 IP 范围。其中，DNS 服务器地址不能为 `127.0.0.1`。
   - **Control Plane 虚拟 IP 配置**：可选择通过手动输入 IP 地址或通过 IP 池为其自动分配的方式进行设置。

     选择 **IP 池自动分配**时，系统将从管控集群 IP 池中为集群分配一个静态 IP。
6. 单击**部署**，开始部署 SKS 服务。在 CloudTower 的任务中心可以查看部署的状态。

   部署结束后，可以在**概览**页面查看 SKS 管控集群的当前状态，以及集群的 Control Plane 节点和 Worker 节点的信息。单击**管控集群**卡片，可以查看管控集群更详细的信息。

**后续操作**

SKS 系统服务使用可观测性服务管理监控、报警、日志、事件和审计数据，如需查看对应数据，您可参考《SMTX Kubenetes 服务管理指南》的[管理 SKS 系统服务 > 为 SKS 系统服务启用监控、报警、日志、事件和审计功能](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_109)章节进行操作。

---

## 升级 SKS

# 升级 SKS

升级 SKS 会对管控集群和工作负载集群有一定的影响，并且在升级前也需要完成一些准备工作，因此，为确保能顺利进行升级，建议您在升级前先认真阅读[升级说明](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_32)。

---

## 升级 SKS > 升级说明

# 升级说明

您可参考以下说明了解升级至本版本的准备工作和影响。

## 升级前准备

- 若当前存在已启用监控功能的 SKS 系统服务或工作负载集群，请确保监控功能均已通过可观测性服务提供，否则需关闭监控功能或将其切换至可观测性服务。
- 确认 CloudTower 版本配套要求，确保与 SKS 搭配使用的 CloudTower 已升级到与目标 SKS 服务版本兼容的版本。
- 确认升级前的 SKS 为 1.4.0 或 1.5.0 版本，否则不支持直接升级至本版本，请先参考 1.4.0 版本的《SMTX Kubernetes 服务部署与升级指南》将 SKS 升级至 1.4.0 版本。
- 提前获取本版本的 SKS 服务安装文件，安装文件的 CPU 架构必须与管控集群所在 SMTX OS 集群的一致。
- 升级 SKS 服务前，确保管控集群处于`就绪`、`运行中`或`异常`状态。所有工作负载集群处于`就绪`、`运行中`、`异常`、`暂停同步中`或`更新中`状态。
- 参考[管控集群资源要求](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_11)和[工作负载集群资源要求](/sks_cn/1.5.1/sks_administration_guide/sks_deploy_guide/sks_deploy_guide_12)确保管控集群和工作负载集群各自所在 SMTX OS 集群的存储空间满足要求。如不满足要求，您可以根据实际情况手动释放出足够的资源空间或者扩容 SMTX OS 集群。
- 确保已为管控集群 IP 池预留至少 2 个空闲 IP，预留的 IP 越多，升级和滚动更新速度越快。
- 若升级前的 SKS 版本为 1.4.0，请确保当前所有工作负载集群的 Kubernetes 版本均为本版本 SKS 兼容的 Kubernetes 版本（1.25.x 和 1.26.x 版本），否则请先[升级工作负载集群](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_68)。
- 若升级前的 SKS 版本为 1.4.0，请确保当前所有工作负载集群的功能版本不低于 1.4.0，如不满足要求，请进入工作负载集群的**概览**界面，在界面右上方单击 **...** > **功能版本更新**完成更新操作。
- SKS 1.5.0 版本开始使用可观测性服务管理日志数据，若升级前的 SKS 版本为 1.4.0，请确认是否需要迁移旧的日志数据。

  - 若需迁移旧日志数据，请根据以下说明确认各集群旧日志数据的存储容量，并计算所有集群的总容量（设为 *N*）。
    - 管控集群：若部署模式为普通模式，则需约 40 GiB 存储容量；若部署模式为高可用模式，则需约 120 GiB 存储容量。
    - 已启用日志插件的工作负载集群：在集群的**设置** > **插件管理**界面中，查看为 **EFK** 插件配置的存储容量。
  - 若无需迁移旧日志数据，对于已启用日志插件的工作负载集群，请先临时关闭日志插件，升级完成后再参考[后续操作](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_33#%E5%90%8E%E7%BB%AD%E6%93%8D%E4%BD%9C)重新启用。
- 若升级前的 SKS 版本为 1.4.0，并且在管控集群和启用 Calico CNI 插件的虚拟机集群中，虚拟机节点所属 SMTX OS 集群的主机 CPU 属于海光一号或二号处理器系列，则请确保 SMTX OS 集群的“虚拟机 CPU 兼容性”设置满足以下要求，否则请修改设置。

  | CPU 处理器系列 | SMTX OS 集群的“虚拟机 CPU 兼容性”要求 |
  | --- | --- |
  | 海光一号 | `主机透传`或 `Opteron_G3` |
  | 海光二号 | `EPYC`、`EPYC-IBPB` 或 `Opteron_G3` |

## 升级影响

- SKS 服务升级过程中，将有以下影响：

  - 管控集群的每一个节点对应的虚拟机将依次被删除并重建，您在虚拟机中存储的文件和对操作系统的修改将不会保留。
  - 管控集群的监控、日志相关组件将会更新，更新期间监控和日志信息可能无法查看，并且信息的采集会发生短时间中断。
  - 工作负载集群中的插件将会更新。
  - 对于未添加至物理机集群的物理机，其操作系统上由 SKS 安装的软件及相关配置文件将会自动更新。
- 若在升级前，SKS 版本为 1.4.0，并且您已通过命令行为启用日志功能的工作负载集群配置应用日志的采集，则在升级完成后，SKS 将使用可观测性服务管理日志数据，原命令行配置将失效，需单独构建日志系统采集应用日志。
- 若升级前 SKS 部署在未启用双活特性的 SMTX OS 集群中，升级后您希望将该集群转换为双活集群，需先将 SKS 服务升级至本版本，然后联系售后工程师进行集群的转换操作。转换完成后，建议重启 `sks-controller` 服务以快速感知 SMTX OS 集群的最新类型。

  - 集群转换过程可能影响日志、监控等系统插件，建议在业务低峰期进行操作。
  - 转换为双活集群后，已部署在该集群上的 SKS 容器镜像仓库虚拟机、管控集群节点虚拟机、工作负载集群节点虚拟机均将自动调整为 3 副本，副本数变更过程不影响节点上 Pod 的正常运行。
  - 部署在该集群的工作负载集群中 SMTX ELF CSI、SMTX ZBS CSI 默认存储类自动调整为 3 副本，通过 SMTX ELF CSI、SMTX ZBS CSI 默认存储类创建的持久卷也将自动调整为 3 副本，副本数变更过程不影响节点上 Pod 的正常运行。更多详细说明，请参考《SMTX Kubernetes 服务管理指南》中[管理存储类](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_54)的注意事项。

---

## 升级 SKS > 升级步骤

# 升级步骤

## 操作步骤

1. 在 **Kubernetes 服务**界面单击**设置** > **服务升级**。
2. 在**服务升级**页面中选择本版本的 SKS 服务安装文件进行上传，并输入文件的 MD5 值。
3. 单击**升级**。

   管控集群的状态将显示为`升级中`。当管控集群的状态恢复为`就绪`，并且在**服务升级**界面查看到 SKS 服务版本为 `1.5.1` 时，表明 SKS 升级成功。

   如果升级失败，请联系 SmartX 售后工程师进行问题定位和处理。

## 后续操作

SKS 1.5.0 版本开始使用可观测性服务管理日志数据，因此若升级前的 SKS 版本为 1.4.0，则升级完成后请务必完成以下操作，否则后续日志功能将无法使用。

1. 在当前 CloudTower 环境中准备满足以下要求的可观测性服务。可观测性服务的部署、升级、提升资源配置等操作说明可参考《可观测性平台用户指南》。

   - 版本为 1.4.2 及以上。
   - 未关联除 SKS 系统服务、工作负载集群以外的其他集群或系统服务。

     建议一个可观测性服务关联的 SKS 对象不超过 10 个。
   - 可观测性服务虚拟机的存储容量满足以下要求：

     - 若需迁移旧日志数据，则存储容量至少为：*N* × 3 GiB。其中，*N* 为[升级前准备](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_32#%E5%8D%87%E7%BA%A7%E5%89%8D%E5%87%86%E5%A4%87)阶段计算的旧日志数据所需存储容量总和。
     - 若无需迁移旧日志数据，则存储容量至少为 256 GiB，后续可按需扩容。
   - 可观测性服务虚拟机的 CPU Steal Time 值不超过 `5`。

     可通过 SSH 方式登录至虚拟机并执行 `top` 命令查看该值，如下图。

     ![](https://cdn.smartx.com/internal-docs/assets/2df79858/sks_deploy_guide_12.png)
2. 在 **Kubernetes 服务**主界面的**设置** > **可观测性配置**界面中，将关联的**可观测性服务**切换至步骤 1 准备的可观测性服务，再根据是否迁移旧日志数据参考以下说明操作。

   - 若需迁移旧日志数据，请勾选**切换为新版日志并实现旧数据迁移**并单击**保存**。

     迁移完成后，SKS 系统服务的事件和审计功能也将自动启用。
   - 若无需迁移旧日志数据，请勾选**关闭旧版日志功能并清除旧数据**并单击**保存**，再勾选**启用新版日志功能**并单击**保存**。
3. 在需启用日志功能的工作负载集群的**设置** > **插件管理**界面中，在**可观测性**配置中将关联的**可观测性服务**切换至步骤 1 准备的可观测性服务，再根据是否迁移旧日志数据参考以下说明操作。

   - 若需迁移旧日志数据，请勾选**切换为新版日志并实现旧数据迁移**并单击**保存**。

     迁移完成后，您还可选择启用**事件**、**审计**功能，相关配置操作可参考《SMTX Kubernetes 服务管理指南》的[管理工作负载集群 > 管理插件 > 管理可观测性插件](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_60)小节。
   - 若无需迁移旧日志数据，请直接启用**日志**并单击**保存**。

---

## 提升 SKS 至高可用模式

# 提升 SKS 至高可用模式

当 SKS 服务的部署模式为普通模式时，可平滑提升 SKS 至高可用模式。

**注意事项**

使用普通模式与高可用模式创建的 SKS 管控集群的 Control Plane 节点和 Worker 节点数量不同。若需要从普通模式提升至高可用模式，则需要提前为管控集群分配更多的计算和存储资源，以及 IP。因此建议在提升前，参考[管控集群资源要求](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_11)和[管控集群网络要求](/sks_cn/1.5.1/sks_deploy_guide/sks_deploy_guide_17)的描述，提前确认 SKS 管控集群所属的 SMTX OS 集群的剩余资源和管控集群的 IP 池满足提升要求。

**前提条件**

- 管控集群当前的部署模式为**普通模式**。
- 管控集群处于**就绪**状态。

**操作步骤**

1. 在 **Kubernetes 服务**界面单击**设置** > **管控集群**，在右侧的**部署模式**区域框中单击**提升**。
2. 在弹出的**提升至高可用模式**对话框中，确认高可用模式的配置后，单击**提升**，开始启动集群的部署模式提升。

   提升结束后，如果在**管控集群**界面的**集群信息**中确认**状态**为`就绪`，并且在**节点信息**中查看到 3 个 Control Plane 节点和 3 个 Worker 节点，则表明提升成功。

---

## 卸载 SKS

# 卸载 SKS

SKS 支持一键式卸载 SKS，即卸载 SKS 管控集群和 SKS 容器镜像仓库，并取消 SKS 系统服务和可观测性服务的关联关系。

**前提条件**

卸载 SKS 前，需要删除所有的工作负载集群。

**操作步骤**

在 **Kubernetes 服务**界面选择**设置**后单击**卸载服务**，再在弹出的**卸载 SKS 服务**对话框中单击**卸载**。

完成上述操作后，系统开始卸载 SKS 管控集群、SKS 容器镜像仓库、SKS 组件以及由 SKS 服务所产生的资源（例如标签、节点模板）。可在任务中心查看此项任务的进度。

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
