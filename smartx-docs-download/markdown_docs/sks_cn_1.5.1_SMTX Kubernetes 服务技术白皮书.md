---
title: "sks_cn/1.5.1/SMTX Kubernetes 服务技术白皮书"
source_url: "https://internal-docs.smartx.com/sks_cn/1.5.1/sks_whitepaper/sks_whitepaper_preface"
sections: 46
---

# sks_cn/1.5.1/SMTX Kubernetes 服务技术白皮书
## 关于本文档

# 关于本文档

本文档详细介绍了 SMTX Kubernetes 服务（SMTX Kubernetes Service，简称 “SKS”）的产品架构，以及 SKS 管控集群和 SKS 工作负载集群的服务和组件。

阅读本文档需要了解 [Kubernetes](https://kubernetes.io/zh-cn/docs/concepts/overview/)（简称 “K8s”）、CloudTower 和 SMTX OS 超融合软件，了解虚拟化、容器、分布式存储等相关技术。

---

## 文档更新信息

# 文档更新信息

**2025-12-12：配合 SMTX Kubernetes 服务 1.5.1 正式发布**

---

## 概述

# 概述

SMTX Kubernetes 服务（简称 “SKS”）是 SmartX 企业云平台提供的 Kubernetes 服务。SKS 基于 SmartX 虚拟化，可自动创建多台虚拟机以构建高可用的 Kubernetes 集群，也可使用物理机作为集群工作节点，并支持通过 GPU 资源为集群提供并行计算能力；通过 SmartX 生产级分布式存储和 CSI（容器存储接口） 插件，可为有状态应用提供稳定、高性能的持久卷；通过 SmartX 网络与安全产品和 CNI（容器网络接口）插件，能够以扁平化的方式实现虚拟机和容器的互联互通以及统一的网络安全策略管理。

SKS 预集成了云原生生态中的服务发布、应用发布、监控、日志等插件，缩短了 Kubernetes 集群就绪时间；同时，SKS 也支持用户使用其他 Kubernetes 生态中的应用。运维人员通过统一的图形界面可以对所有集群和容器应用进行全生命周期管理，还可以查看其监控、日志、事件和审计信息。

通过以上特性，企业运维团队可在多种 CPU 架构的服务器上轻松部署、管理和使用生产级 Kubernetes 集群，降低企业云原生转型难度，加速应用现代化进程。

**技术特点**

- 方便快捷的 K8s 集群生命周期管理
  - 依托 CloudTower 实现简单易用的图形化界面。
  - 基于 K8s 社区成熟的开源项目 Cluster API 实现声明式 K8s 集群编排引擎。
  - 深度集成 SMTX OS 超融合架构，快速构建生产级高可用、易运维的 K8s 集群；支持 SMTX OS 双活集群，实现跨数据中心的高可用性和业务连续性。
  - 自研的 Cluster API provider 支持多样化的基础设施环境，有 x86\_64 和 AArch64 架构、虚拟机和物理机节点类型、以及多种操作系统和 K8s 版本可供选择。
  - 集成 NVIDIA GPU Operator 实现设备直通（Passthrough）与 vGPU 分时调度（Time-Slicing）双模式。
  - 基于节点组提供自动伸缩和故障节点自动替换能力，实现集群的弹性伸缩和高可用。
  - 基于 SmartX 虚拟化和节点配置代理插件，实现集群和节点配置的原地更新。
  - 接入可观测性平台，提供统一的监控与报警能力。
- 可扩展的集群插件管理
  - 以插件形式支持多种常用的 K8s 基础服务。
  - 支持一键开启或关闭插件，且可按需配置插件参数。
- 高性能的 K8s 容器持久化存储
  - 通过 SMTX ELF CSI 驱动直接挂载 SMTX OS 虚拟磁盘作为持久卷（PV）。
  - 通过 SMTX ZBS CSI 驱动对接 ZBS iSCSI LUN 提供持久卷（PV）。
- 安全可靠的 Everoute Integrated CNI
  - 实现扁平化的容器网络，打破容器网络和虚拟机网络的界限。
  - 协同调度容器网络安全和虚拟化微分段服务。
- 企业级 K8s 集群运维及使用体验
  - 在 CloudTower UI 中统一管理 K8s 资源。
  - 基于 RBAC 权限控制，以项目为维度组织名字空间，实现资源访问策略的租户级隔离。
  - 基于 K8s TokenReview API 的 Webhook 令牌认证机制，实现集群访问的身份认证。
  - 基于 K8s 原生资源配额机制进行扩展优化，支持项目级、命名空间级配额的精细化资源管理。
  - 基于用户权限模型和 API 网关代理，实现租户级别的 Kubernetes 资源可视化管理。
  - 基于 CloudShell 的 Web 终端代理，提供便捷的集群、节点和 Pod 访问入口。

---

## 产品架构 > 整体架构

# 整体架构

SKS 集成了 K8s 社区中知名且应用广泛的开源项目 [Cluster API](https://github.com/kubernetes-sigs/cluster-api) 进行 K8s 集群的生命周期管理，其关键设计思想是通过一个 K8s 管控集群提供的 Kubernetes [CustomResourceDefinition](https://kubernetes.io/zh-cn/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/) API（简称 “K8s CRD API”） 来创建和管理多个 K8s 集群。SKS 整体技术架构如下图。

![](https://cdn.smartx.com/internal-docs/assets/645336b7/sks_whitepaper_01.png)

---

## 产品架构 > 核心组件 > SKS 容器镜像仓库

# SKS 容器镜像仓库

SKS 容器镜像仓库用于存放 SKS 在离线环境下使用的所有容器镜像，包括 SKS 组件容器镜像、K8s 组件镜像等。SKS 容器镜像仓库使用了最流行的开源 Harbor 容器镜像仓库服务，运行在一个专用的虚拟机中。

---

## 产品架构 > 核心组件 > SKS Manager

# SKS Manager

SKS Manager 是 CloudTower 内置的 SKS 管理器，它运行在 CloudTower 虚拟机上的 K8s 集群中，负责以下工作：

1. 部署 SKS 容器镜像虚拟机，以存放 SKS 在离线环境下使用的所有容器镜像。
2. 安装和卸载 SKS 引导集群。
3. 上传用于创建 K8s 节点对应虚拟机的节点模板文件。
4. 调用 SKS 引导集群的 API 创建、升级、删除 SKS 管控集群。

---

## 产品架构 > 核心组件 > SKS 引导集群

# SKS 引导集群

SKS 引导集群（SKS Bootstrap Cluster）是一个部署了 SKS 核心服务的 K8s 集群，仅用于通过 Cluster API 创建、升级、删除系统中唯一的 SKS 管控集群，不负责管理 SKS 工作负载集群。它是 K8s Cluster API 架构中的必需组件。在安装 SKS 的过程中，SKS 引导集群的组件被安装在 CloudTower 虚拟机上的 K8s 集群中。

---

## 产品架构 > 核心组件 > SKS 管控集群

# SKS 管控集群

SKS 管控集群（SKS Management Cluster）是一个高可用的 K8s 集群。 在 SKS 安装过程中，系统会自动通过 SKS 引导集群创建出一个 SKS 工作负载集群，然后在其上安装 SKS 核心服务，从而将这个 SKS 工作负载集群转换成 SKS 管控集群。SKS 管控集群通过 Cluster API 创建和管理多个 SKS 工作负载集群。用户的各种工作负载不应部署在 SKS 管控集群中，而应部署在 SKS 工作负载集群中。

---

## 管控集群

# SKS 管控集群

SKS 管控集群（SKS Management Cluster）是一个高可用的 K8s 集群。 在 SKS 安装过程中，系统会自动通过 SKS 引导集群创建出一个 SKS 工作负载集群，然后在其上安装 SKS 核心服务，从而将这个 SKS 工作负载集群转换成 SKS 管控集群。SKS 管控集群通过 Cluster API 创建和管理多个 SKS 工作负载集群。用户的各种工作负载不应部署在 SKS 管控集群中，而应部署在 SKS 工作负载集群中。

---

## 管控集群 > SKS 核心服务

# 管控集群

SKS 管控集群（SKS Management Cluster）是一个 K8s 集群，其上运行着 SKS 核心服务和其他服务。它使用 Cluster API 管理多个 SKS 工作负载集群，并对外暴露 API 和提供 CLI。CloudTower 的 Kubernetes 服务 UI 通过调用 SKS 管控集群的 API 进行 SKS 工作负载集群的创建、扩缩容、更新、升级、删除等操作。

SKS 管控集群中运行的服务和组件包括：

- K8s 集群组件
- SKS 核心服务
- SKS 包管理器
- SKS 集群插件

---

## 管控集群 > SKS 核心服务 > Cluster API

# Cluster API

[Cluster API](https://cluster-api.sigs.k8s.io/)（简称 “CAPI”）是 K8s 社区中一个非常开放、活跃和成熟的开源项目，遵循 Apache License v2.0。Cluster API 项目创建于 2018 年，由 K8s Cluster Lifecycle Special Interest Group 负责管理。Cluster API 吸纳了其他开源的 K8s 部署工具的优点，提供一套声明式的 K8s 风格的 API 以及相关工具来简化 K8s 集群的创建、扩容、缩容、更新配置、升级、删除等完整的 K8s 集群生命周期管理操作。Cluster API 实现了灵活可扩展的框架以支持在 vSphere、AWS、Azure、GCP、OpenStack 等多种云平台中部署 K8s 集群。开发人员可以增加新的 Cluster API Cloud Provider 以支持更多的云平台。Cluster API 还支持配置 K8s 集群组件的参数、K8s Control Plane 高可用、自动替换故障节点、节点自动伸缩等高级功能。

Cluster API 已被多个开源项目和商业产品使用，比如 VMware Tanzu、Red Hat OpenShift、SUSE Rancher、Kubermatic、腾讯云 TKE、青云 KubeSphere 等。

---

## 管控集群 > SKS 核心服务 > Cluster API Provider for ELF

# Cluster API

[Cluster API](https://cluster-api.sigs.k8s.io/)（简称 “CAPI”）是 K8s 社区中一个非常开放、活跃和成熟的开源项目，遵循 Apache License v2.0。Cluster API 项目创建于 2018 年，由 K8s Cluster Lifecycle Special Interest Group 负责管理。Cluster API 吸纳了其他开源的 K8s 部署工具的优点，提供一套声明式的 K8s 风格的 API 以及相关工具来简化 K8s 集群的创建、扩容、缩容、更新配置、升级、删除等完整的 K8s 集群生命周期管理操作。Cluster API 实现了灵活可扩展的框架以支持在 vSphere、AWS、Azure、GCP、OpenStack 等多种云平台中部署 K8s 集群。开发人员可以增加新的 Cluster API Cloud Provider 以支持更多的云平台。Cluster API 还支持配置 K8s 集群组件的参数、K8s Control Plane 高可用、自动替换故障节点、节点自动伸缩等高级功能。

Cluster API 已被多个开源项目和商业产品使用，比如 VMware Tanzu、Red Hat OpenShift、SUSE Rancher、Kubermatic、腾讯云 TKE、青云 KubeSphere 等。

---

## 管控集群 > SKS 核心服务 > Cluster API Provider for KubeSmartPhysicalHost

# Cluster API Provider for KubeSmartPhysicalHost

Cluster API Provider for KubeSmartPhysicalHost（简称 “CAP-KSPH”）是 SmartX 基于 Cluster API 框架自主研发的一种 Cluster API Cloud Provider，用于将已被 SKS 纳管的物理机作为 Worker 节点来部署 K8s 集群。

---

## 管控集群 > SKS 核心服务 > SKS 集群管理器

# SKS 集群管理器

SKS 集群管理器包含 KubeSmartCluster Controller（一个 [K8s Controller](https://kubernetes.io/zh-cn/docs/concepts/architecture/controller/)）和一些 K8s [Webhook](https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/)，并定义了 KubeSmartCluster [Custom Resource](https://kubernetes.io/zh-cn/docs/concepts/extend-kubernetes/api-extension/custom-resources/)（简称 “KubeSmartCluster CR”）。

KubeSmartCluster CR 用来描述一个 SKS 工作负载集群的规格和配置。SKS 集群管理器根据每一个 KubeSmartCluster CR 中的配置，对内置的 YAML 模板文件进行渲染，生成并创建 Cluster API 所需的多个 CR 对象，从而创建出一个 SKS 工作负载集群。具体过程详见下图。

![](https://cdn.smartx.com/internal-docs/assets/645336b7/sks_whitepaper_02.png)

---

## 管控集群 > SKS 核心服务 > SKS 集群插件管理器

# SKS 集群插件管理器

SKS 集群插件管理器（Addon Manager）包含运行在 SKS 管控集群中的 Addon Controller（一个 [K8s Controller](https://kubernetes.io/zh-cn/docs/concepts/architecture/controller/)）和运行在 SKS 工作负载集群中的 SKS 包管理器，并定义了 Addon CR。

Addon CR 用来描述一个 SKS 工作负载集群中安装的插件（Addon）。一个 Addon 代表在一个 SKS 集群中部署的应用包（Package）。 一个 Package 就是一个打包成容器镜像的 K8s 应用，比如可以将以下应用打包为 Package：Calico CNI、SMTX ELF CSI、Elasticsearch、Prometheus、MetalLB 等。每个 Addon CR 可以指定 Package 的名称、版本和配置参数，并支持随时更新配置参数。

---

## 管控集群 > SKS 核心服务 > SKS 许可证管理器

# SKS 许可证管理器

SKS 许可证管理器包含 License Controller（一个 [K8s Controller](https://kubernetes.io/zh-cn/docs/concepts/architecture/controller/)）和一些 K8s [Webhook](https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/)，并定义了 License CR。

License CR 用来描述 SKS 的许可证信息。SKS 许可证管理器依据 License CR 指定的能力范围来限制 SKS 管控集群在管理 SKS 工作负载集群时的行为。

---

## 管控集群 > SKS 核心服务 > SKS 物理机管理器

# SKS 物理机管理器

SKS 物理机管理器包含 ServerInstance Controller（一个 [K8s Controller](https://kubernetes.io/zh-cn/docs/concepts/architecture/controller/)）和一些 K8s [Webhook](https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/)，并定义了 ServerInstance CR。

ServerInstance CR 用于描述被 SKS 纳管的物理机的信息。SKS 物理机管理器将对注册的物理机执行必要的初始化动作，包括通过 ServerInstance CR 中记录的连接方式在操作系统中安装 containerd、CNI Plugin、Ansible，设置 Kernel 参数等，并收集操作系统和硬件设备信息。初始化完成之后，物理机即可被选中作为 Worker 节点加入到物理机类型的工作负载集群中。

---

## 管控集群 > SKS 核心服务 > SKS 控制台管理器

# SKS 控制台管理器

SKS 使用 CloudTTY 作为控制台管理器。[CloudTTY](https://github.com/cloudtty/cloudtty) 是一款专用于 Kubernetes 的开源 Cloud Shell Operator，提供集群、节点和 Pod 级别的 Shell 访问能力。

---

## 管控集群 > SKS 核心服务 > SKS 可观测性平台服务管理器

# SKS 可观测性平台服务管理器

SKS 将管控集群与工作负载集群的监控和报警功能统一接入了可观测性平台。SKS 可观测性平台服务管理器用于处理集群和可观测性服务对象的注册、注销和清理操作，为集群加载和同步默认的监控和报警规则，确保这些规则在可观测性平台中正确应用和更新。

SKS 可观测性平台服务管理器包含 ObservabilitySystemService Controller，并定义了 ObservabilitySystemService CR。ObservabilitySystemService CR 用来描述一个集群与可观测性平台的关联关系与功能状态。

---

## 管控集群 > SKS 核心服务 > SKS 原地更新管理器

# SKS 原地更新管理器

原地更新是 SKS 对于 CAPI 的能力扩展，可以实现在不重建节点的前提下，对集群和现有节点的配置进行更新。

SKS 原地更新管理器包含 InplaceUpdateMachineGroup 和 InplaceUpdateMachine Controller，并定义了 InplaceUpdateMachineGroup CR 和 InplaceUpdateMachine CR。

- InplaceUpdateMachineGroup CR 用来描述一个节点组的原地更新信息，对应 CAPI 的 KubeadmControlPlane 或 MachineDeployment，负责集群配置的更新，以及控制节点的并发更新数量。
- InplaceUpdateMachine CR 用来描述单个节点的原地更新信息，对应 CAPI 的 Machine，负责单个节点的更新操作。

原地更新管理器与 CAPI 配合，协调各级配置的同步，确保从管控集群到工作负载集群，从集群到节点组再到节点各个维度的配置一致性。

---

## 管控集群 > SKS 核心服务 > SKS 项目管理器

# SKS 项目管理器

SKS 通过项目管理一个或多个名字空间，可对用户访问集群的请求进行 [RBAC 鉴权](https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/rbac/)，用户拥有的权限取决于其集群对应项目中被分配的角色。SKS 项目管理器将用户权限信息同步至 SKS 工作负载集群，当用户使用自身的 kubeconfig 文件访问集群时，Kubernetes 通过 RBAC 鉴权决定用户是否有权限访问集群中相应的资源。

SKS 项目管理器包含 Project Controller、ProjectRole Controller 和 ProjectRoleBinding Controller，并定义了 Project CR、ProjectRole CR 和 ProjectRoleBinding CR。

- Project CR 用于描述集群中的一个项目，项目以名字空间为维度划分资源进行管理。
- ProjectRole CR 用于描述一个项目角色，不同的项目角色拥有项目内不同资源的访问和操作权限。
- ProjectRoleBinding CR 用于描述一个用户与项目角色的绑定关系，该用户在项目中将拥有项目角色对应的权限。

---

## 管控集群 > SKS 核心服务 > SKS 用户管理器

# SKS 用户管理器

SKS 可对用户访问集群的请求进行 [Webhook 令牌身份认证](https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/authentication/#webhook-token-authentication)。SKS 用户管理器将用户认证信息同步至 SKS 工作负载集群，当用户使用其专属的 kubeconfig 文件访问集群时，请求会由 warden 认证服务根据认证令牌信息进行身份认证。

SKS 用户管理器包含运行在 SKS 管控集群中的 User Controller、ClusterToken Controller、以及运行在 SKS 工作负载集群中的 warden 认证服务，并定义了 User CR 和 ClusterToken CR。

- User CR 用于描述一个用户，从 CloudTower 同步而来。
- ClusterToken CR 用于描述一个用户访问集群的认证令牌信息，用于生成用户的 Kubeconfig。

---

## 管控集群 > SKS 核心服务 > SKS REST API Server

# SKS REST API Server

SKS REST API Server 封装了管控集群的 K8s CRD API，并实现了其他相关功能。该组件以 REST API 的形式对外暴露服务，并使用 JWT token 进行用户认证。SKS REST API Server 也支持将针对 SKS 工作负载集群的 K8s API 请求转发至 SKS 工作负载集群，使客户端无需单独为每一个工作负载集群提供认证信息。

---

## 管控集群 > SKS 核心服务 > SKS File Server

# SKS File Server

SKS File Server 是一个 SKS 内部的文件服务器，用于存放内部流程使用的文件，部署物理机集群时可以作为软件源实现软件离线安装。该文件服务器启动时可以根据 ConfigMap 配置从镜像仓库同步并解压镜像文件，并将镜像内容存储在持久卷中。

---

## 管控集群 > SKS 包管理器

# SKS 包管理器

SKS 包管理器（Package Manager）是 SKS 集群插件管理器在 SKS 管控集群和工作负载集群中的代理（SKS Agent），负责将 Addon CR 指定的 Package 安装到工作负载集群中。SKS 包管理器使用开源项目 [kapp-controller](https://carvel.dev/kapp-controller/docs/v0.40.0/packaging/) 进行包管理。kapp-controller 定义了 PackageInstall/Package/PackageRepository/App 等 CRD 来管理打包成容器镜像的 Package。Addon CR 是对 PackageInstall 和 Package 的封装。当在管控集群中创建一个 Addon CR 后，Addon Controller 会根据 Addon CR 中指定的 Package 信息和配置参数在 Addon CR 指定的工作负载集群中创建 PackageInstall CR。工作负载集群中的 kapp-controller 会 reconcile 这个 PackgeInstall CR，并依据指定的 Package CR 中定义的模板和配置参数生成 YAML 清单，应用到工作负载集群中。

---

## 管控集群 > SKS 集群插件

# SKS 集群插件

SKS 管控集群中默认安装了以下集群插件（Addon）以提供相关功能。

- 时区插件
- Calico CNI 插件
- SMTX ELF CSI 插件
- 监控插件
- 日志插件
- EIC Adapter 插件
- 网络时间协议管理插件
- 节点配置代理插件

---

## 工作负载集群

# 工作负载集群

SKS 工作负载集群（SKS Workload Cluster）是由 SKS 管理员创建的交付给普通用户的 K8s 集群，在其上可以部署和运行各种用户指定的 K8s [工作负载](https://kubernetes.io/zh-cn/docs/concepts/workloads/)，比如 Web 应用、数据服务、AI 应用等。

---

## 工作负载集群 > 工作负载集群的组件

# 工作负载集群的组件

SKS 工作负载集群的每个节点对应一个虚拟机或物理机。集群节点按节点组划分，包含一个 Control Plane 节点组（用于运行 K8s 集群的 Control Plane ），以及一个或多个 Worker 节点组（用于运行 K8s 集群的工作节点）。根据集群节点类型的差异，可将 SKS 工作负载集群分为虚拟机类型的工作负载集群（简称“虚拟机集群”）和物理机类型的工作负载集群（简称“物理机集群”）。

- 虚拟机集群是 Control Plane 节点和 Worker 节点均为虚拟机的工作负载集群。
- 物理机集群是以虚拟机作为 Control Plane 节点、物理机作为 Worker 节点的工作负载集群。用户可以通过 SKS UI 界面填写 SSH 等信息，以方便地将物理机注册到 SKS 服务中，之后再选择创建物理机集群，即选择多个物理机作为 Worker 节点来搭建 K8s 集群。

SKS 还在工作负载集群中安装了 kube-vip、SKS 包管理器和一些预置的 SKS 集群插件（如下），以提供集群 Control Plane 高可用、CNI、CSI、监控、日志、Ingress Controller、LoadBalancer、节点配置、身份认证等基础服务。

- 时区插件
- Calico CNI 插件
- EIC 插件（仅虚拟机集群支持）
- SMTX ELF CSI 插件（仅虚拟机集群支持）
- SMTX ZBS CSI 插件
- 监控插件
- 日志插件
- Ingress Controller 插件
- LoadBalancer 插件
- ExternalDNS 插件
- 令牌身份认证插件
- 网络时间协议管理插件
- 节点配置代理插件
- GPU Operator 插件
- 配额插件

SKS 工作负载集群的组件如下图所示。

![](https://cdn.smartx.com/internal-docs/assets/645336b7/sks_whitepaper_04.png)

---

## 工作负载集群 > 集群 Control Plane 高可用

# 集群 Control Plane 高可用

[kube-vip](https://kube-vip.io/) 是一个为 K8s 集群的 Control Plane 和 LoadBalancer 类型的 Service 对象提供虚拟 IP 和负载均衡能力的开源项目，不依赖于其他软件或硬件设备。SKS 在创建管控集群或工作负载集群时，会自动在集群中部署 kube-vip 服务，并把用户指定的虚拟 IP 配置为管控集群或工作负载集群 Control Plane 的虚拟 IP，从集群外部可以始终使用这个虚拟 IP 访问集群。同时，SKS 还利用了虚拟机的放置组规则，将 Control Plane 节点虚拟机分别放置在不同的物理主机。当管控集群或工作负载集群的 Control Plane 节点数量为 3 或 5 时，就实现了集群 Control Plane 的高可用。

---

## 工作负载集群 > 节点组自动伸缩

# 节点组自动伸缩

[Cluster Autoscaler on Cluster API](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler/cloudprovider/clusterapi) 是 K8s 社区的开源项目，用于实现 Kubernetes 集群的自动伸缩功能。SKS 集成了 Cluster Autoscaler on Cluster API，将其作为集群插件 Cluster Autoscaler 提供给用户使用。

启用插件后，用户可以通过 SKS UI 界面轻松配置虚拟机集群的节点组自动伸缩参数，以实现节点组自动伸缩。该功能可以实时监测 K8s 集群的 CPU 和内存资源使用量，并根据用户配置的参数动态地调整节点组的节点数量，在满足工作负载需求的前提下有效地管理集群资源。当集群节点缺少足够的资源调度新创建的 Pod 时，自动扩容相应节点组的节点数量，以确保 Pod 正常运行；当集群节点的资源处于闲置状态时，自动缩容相应节点组的节点数量，从而释放节点虚拟机占用的资源，以提升资源的利用率。

---

## 工作负载集群 > 故障节点自动替换

# 故障节点自动替换

[MachineHealthCheck](https://cluster-api.sigs.k8s.io/tasks/automated-machine-management/healthchecking.html) 是 Cluster API 提供的故障节点自动替换解决方案。SKS 利用 Cluster API 部署和管理 SKS 工作负载集群，并自动集成了 MachineHealthCheck 功能。用户可以通过 SKS UI 界面为每个虚拟机类型的节点组配置故障节点判定条件和自动替换阈值。当 SKS 检测到节点符合故障判定条件和自动替换阈值时，将自动删除故障节点及其对应的虚拟机，并创建新的节点来替换此故障节点，以保证集群的高可用。

---

## 工作负载集群 > 原地更新

# 原地更新

CAPI 遵循[机器不可变](https://cluster-api.sigs.k8s.io/user/concepts#machine-immutability-in-place-upgrade-vs-replace)原则，即集群或节点配置的变更通过重建节点的方式实现。SKS 在 CAPI 的基础上进行扩展，基于 SmartX 虚拟化和节点配置代理插件，实现在不重建节点的前提下，对集群和现有节点的配置进行原地更新，以减少更新时间，并避免节点重建带来的负面影响。目前 SKS 在大部分配置场景下均支持原地更新，例如热扩容节点资源规格、编辑 K8s 集群配置。此外，SKS 仍然保留节点替换、故障节点自动替换等重建节点的能力。

---

## 工作负载集群 > 容器网络

# 容器网络

[集群网络系统](https://kubernetes.io/zh-cn/docs/concepts/cluster-administration/networking/)是 K8s 的核心部分，负责容器间通信、Pod 间通信、Pod 与 Service 间通信、外部与 Service 间通信等。Kubernetes [Container Network Interface](https://github.com/containernetworking/cni)（简称 “K8s CNI”）是 [CNCF](https://cncf.io) 定义的一组规范，用于编写 CNI 插件以提供 K8s 集群的容器网络和安全功能。

SKS 支持在工作负载集群中使用开源容器网络解决方案 [Calico](https://projectcalico.docs.tigera.io/about/about-calico) 及其 CNI，或使用 SmartX 自研的 Everoute Integrated CNI（简称 “EIC”）。

---

## 工作负载集群 > 容器网络 > Calico CNI

# Calico CNI

[Calico](https://projectcalico.docs.tigera.io/about/about-calico) 是一种开源的网络和网络安全解决方案，适用于容器、K8s、虚拟机和裸机上的工作负载。Calico CNI 是一种被广泛使用的 K8s CNI。

---

## 工作负载集群 > 容器网络 > EIC

# EIC

EIC 是一种 SmartX 自研的 K8s 网络解决方案，主要包含两个模块：EIC CNI 和 EIC Adapter。依托 SMTX OS 集群中部署的 Everoute 服务、和 SKS 管控集群中部署的 EIC Adapter 和 SKS 工作负载集群（虚拟机类型）中部署的 EIC CNI，EIC 实现了 K8s Pod 的网络连通性和网络安全策略。

与其他 K8s 网络方案相比，EIC 的作用范围不再局限于 K8s 集群内部，它将 K8s Pod 与 K8s 节点所在虚拟机的网络打通，并且可以从 K8s 集群外部直接访问到 Pod IP。

## EIC CNI

EIC CNI 位于每一个工作负载集群的内部，负责配置和初始化容器网络。

![](https://cdn.smartx.com/internal-docs/assets/645336b7/sks_whitepaper_05.png)

## EIC Adapter

EIC Adapter 位于 SKS 管控集群中，一个 EIC Adapter 服务可以管理多个工作负载集群。EIC Adapter 从工作负载集群中获取 Pod 和 NetworkPolicy 信息，适配并同步到 Everoute 服务中，从而实现安全策略的功能。

![](https://cdn.smartx.com/internal-docs/assets/645336b7/sks_whitepaper_06.png)

---

## 工作负载集群 > 容器持久化存储

# 容器持久化存储

[容器存储接口](https://kubernetes.io/zh-cn/docs/concepts/storage/volumes/#csi)（Container Storage Interface，简称 “CSI”）为 K8s 等容器编排系统定义标准接口，以将任意存储系统暴露给它们的容器工作负载。SmartX 自研了两种 CSI 插件：SMTX ELF CSI 和 SMTX ZBS CSI。使用 SKS 创建工作负载集群时，用户可以在集群中安装 SMTX ELF CSI（仅适用于虚拟机集群）或 SMTX ZBS CSI，为容器工作负载提供持久化存储。

特性对比如下表所示：

| 特性 | SMTX ELF CSI | SMTX ZBS CSI |
| --- | --- | --- |
| 卷制备方式 | 动态制备 | 动态制备 |
| 数据本地化 | ✓ | × |
| 单节点最大挂载卷数量 | 根据 SMTX OS 集群的服务器 CPU 架构不同，每个节点支持挂载的持久卷数量有所不同，具体如下。   - **x86\_64 架构**：支持最多为每个节点挂载 60 个持久卷。 - **AArch64 架构**：针对不同的 CNI 和 CSI 插件组合，支持挂载的持久卷数量也有所不同。   - **Calico CNI + SMTX ELF CSI**：支持最多为每个节点挂载 33 个持久卷。   - **Calico CNI + SMTX ELF CSI + SMTX ZBS CSI**：支持最多为每个节点挂载 32 个持久卷。   - **EIC + SMTX ELF CSI**：支持最多为每个节点挂载 32 个持久卷。   - **EIC + SMTX ELF CSI + SMTX ZBS CSI**：支持最多为每个节点挂载 31 个持久卷。 | 128 |
| 卷模式以及访问模式 | - 文件系统：ReadOnlyMany、​ReadWriteOnce - 块：ReadOnlyMany、​ReadWriteOnce、​ReadWriteMany | - 文件系统：ReadWriteOnce - 块：ReadOnlyMany、​ReadWriteOnce、​ReadWriteMany |
| 卷在线扩容 | ✓ | ✓ |
| 卷快照 | ✓ | ✓ |
| 从快照制备卷 | ✓ | ✓ |
| 卷克隆 | ✓ | ✓ |
| 卷身份验证 | × | ✓ |

---

## 工作负载集群 > 容器持久化存储 > SMTX ELF CSI

# SMTX ELF CSI

SMTX ELF K8s CSI Driver 是 SmartX 开发的符合 [K8s CSI 规范](https://github.com/container-storage-interface/spec/blob/master/spec.md)的一种 CSI 驱动插件，在 SMTX OS 超融合场景下为 SKS 管控集群和工作负载集群（虚拟机类型）提供持久化存储能力。它实现了对附加到 ELF 虚拟机（即工作负载集群的节点）上的虚拟卷的生命周期管理，支持通过 PersistentVolumeClaim 在 K8s 集群中动态创建、挂载 ELF 虚拟卷给 K8s Pod 使用。

SMTX ELF CSI 使用 ELF 虚拟卷实现 K8s PersistentVolume。ELF 虚拟卷实际对应一个 iSCSI LUN，进一步对应到 ZBS Volume，具备超融合系统中 IO 本地化的高性能优势。

![](https://cdn.smartx.com/internal-docs/assets/645336b7/sks_whitepaper_07.png)

---

## 工作负载集群 > 容器持久化存储 > SMTX ZBS CSI

# SMTX ZBS CSI

SMTX ZBS K8s CSI Driver 是 SmartX 开发的符合 [K8s CSI 规范](https://github.com/container-storage-interface/spec/blob/master/spec.md) 的一种 CSI 驱动插件，支持 K8s 通过 iSCSI 从 SMTX OS 集群或 SMTX ZBS 集群中获得高性能的分布式持久化存储服务。它通过存储网络将 ZBS 块存储服务的 iSCSI LUN 挂载到节点中，使其以持久卷的形式提供给 K8s Pod 使用。

![](https://cdn.smartx.com/internal-docs/assets/645336b7/sks_whitepaper_08.png)

---

## 工作负载集群 > 服务访问

# 服务访问

在 K8s 集群中部署应用时，K8s 支持通过 NodePort、LoadBalancer、Ingress 等方式把应用的服务接口暴露给外部使用。SKS 内置了多种集群插件来支持用户应用的服务访问。

---

## 工作负载集群 > 服务访问 > LoadBalancer

# LoadBalancer

[MetalLB](https://metallb.universe.tf/) 是一款开源的 [LoadBalancer](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/#loadbalancer) 实现，支持 L2 和 BGP 两种模式。SKS 提供了 MetalLB 插件，支持使用 LoadBalancer 类型的 Service 对外暴露 K8s 应用服务。

---

## 工作负载集群 > 服务访问 > Ingress Controller

# Ingress Controller

[Contour](https://github.com/projectcontour/contour) 是一款开源的基于 [Envoy proxy](https://www.envoyproxy.io/) 技术的 [Ingress Controller](https://kubernetes.io/zh-cn/docs/concepts/services-networking/ingress-controllers/) 实现。SKS 提供了Contour 插件，支持使用 Ingress 方式对外暴露 K8s 应用服务。

---

## 工作负载集群 > 服务访问 > ExternalDNS

# ExternalDNS

[external-dns](https://github.com/kubernetes-sigs/external-dns) 是一款开源的 DNS 工具。当 K8s 应用服务以 LoadBalancer 或 Ingress 形式对外暴露时，external-dns 可以动态地在 DNS 服务器中添加和删除 DNS 记录，把指定的 hostname 解析为 LoadBalancer 或 Ingress Controller 的 IP 地址。SKS 提供了 External DNS 插件，以配合 MetalLB 和 Ingress Controller 插件一起提供灵活多样的服务访问方式。

---

## 工作负载集群 > 可观测性 > 监控

# 监控

监控功能是 SKS 可观测性的核心能力之一，该功能可以实时记录 K8s 集群的运行状态数据，帮助用户快速获知系统中各个组件的运行指标。SKS 的监控功能已接入 SmartX 的可观测性服务，由可观测性服务提供监控和报警功能。

监控系统包含以下三个部分：

- 基于开源项目 Prometheus Operator 的部署集合 [kube-prometheus](https://github.com/prometheus-operator/kube-prometheus)，用于提供采集对象 API 和 dashboard，在 SKS 中封装为 kube-prometheus 插件。
- 集群可观测性服务 client observability-monitoring-agent 插件，用于抓取 kube-prometheus 提供的采集目标并发送 metrics 数据到可观测性服务。
- 集成在 sks-controller-manager 中的 observability controller，用于维护报警规则的生命周期。

SKS 还基于 Grafana API 提供了定制化的监控系统查询 Web UI。报警策略可在 CloudTower 中进行自定义。

---

## 工作负载集群 > 可观测性 > 报警

# 报警

报警功能是 SKS 可观测性的核心能力之一，该功能可以对监控数据进行实时分析，在监控数据超过阈值时触发报警，帮助用户及时发现系统中的异常情况。SKS 的报警功能基于可观测性平台提供，SKS 将默认报警规则同步到可观测性平台，实现对集群的监控和报警。用户可以通过 Web UI 查看监控数据和报警信息，以及设置报警规则参数。

---

## 工作负载集群 > 可观测性 > 日志采集和查询

# 日志采集和查询

日志采集和查询功能是 SKS 可观测性的核心能力之一，该功能可以实时收集 K8s 集群中各种系统组件和应用的日志，帮助用户使用丰富的过滤条件快速查询系统的运行日志。SKS 的日志功能已接入基于 Vector/Loki 技术栈的 SmartX 可观测性服务，由可观测性服务提供日志存储和查询功能。

日志系统包含以下三个部分：

- 可观测性服务 client observability-logging-agent，以 DaemonSet 方式运行于集群各节点，用于采集 Pod 日志、节点系统日志和内核日志。
- 封装 event-exporter 与 observability-agent 的 observability-event-agent，以 Deployment 方式运行于集群中，用于采集 Kubernetes 事件信息。
- 可观测性服务 client observability-audit-agent，以 DaemonSet 方式运行于集群控制平面节点，用于采集 kube-apiserver 审计日志。

SKS 利用可观测性服务提供的 Grafana 直接访问 Loki API，提供高性能的日志查询体验。灵活的集群配置支持内置的通用审计策略（normal、simple、detailed）及用户自定义审计策略，并可独立控制日志、事件、审计信息的持久化收集。

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
