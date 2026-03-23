---
title: "sks_cn/1.5.1/SMTX Kubernetes 服务与第三方平台对接操作指南"
source_url: "https://internal-docs.smartx.com/sks_cn/1.5.1/sks_thirdparty_config/sks_thirdparty_config_preface"
sections: 8
---

# sks_cn/1.5.1/SMTX Kubernetes 服务与第三方平台对接操作指南
## 关于本文档

# 关于本文档

本文档介绍了 SMTX Kubernetes 服务与第三方平台进行对接的流程和操作步骤。

阅读本文档的对象需了解 SMTX Kubernetes 服务、CloudTower、SMTX OS 超融合软件和对应的第三方平台，以及虚拟化、容器、分布式存储等相关技术，并具备数据中心操作的丰富经验。

---

## 文档更新信息

# 文档更新信息

**2025-12-12：配合 SMTX Kubernetes 服务 1.5.1 正式发布**

---

## 使用灵雀云 ACP 纳管 SKS 工作负载集群

# 使用灵雀云 ACP 纳管 SKS 工作负载集群

灵雀云 ACP 是一个容器云平台，支持通过创建集群或接入集群的方式，对接多样化的 Kubernetes 集群作为业务集群。平台部署时，会部署一个标准的 Kubernetes 集群（global）作为管理集群，基于 global 集群，可对接多个业务集群。

SKS 工作负载集群支持接入灵雀云 ACP 进行管理，当前已验证可接入的版本为 ACP 3.10.2。下文介绍使用灵雀云 ACP 纳管 SKS 工作负载集群的流程和步骤。

**注意事项**

SKS 工作负载集群被纳管后，SKS 工作负载集群的生命周期管理相关操作，例如集群和节点的创建、编辑、升级、删除等操作， 仍需要在 CloudTower 的 **Kubernetes 服务**界面中完成。

**前提条件**

- SKS 工作负载集群的 K8s 版本为 1.25.x ~ 1.30.x。
- 灵雀云 ACP 所在的 K8s 集群（global 集群）与 SKS 工作负载集群的网络连通。

---

## 使用灵雀云 ACP 纳管 SKS 工作负载集群 > 为集群添加受信任的容器镜像仓库

# 为集群添加受信任的容器镜像仓库

为确保 SKS 工作负载集群能够从灵雀云 ACP 拉取纳管所需的组件镜像，需要让工作负载集群信任灵雀云私有容器镜像仓库。

具体方法如下：

- 如果未创建要纳管的 SKS 工作负载集群，请先参考《SMTX Kubernetes 服务管理指南》的[管理 SKS 服务设置 > 管理全局配置 > 配置受信任容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_93)章节，将需要使用的容器镜像仓库配置为全局受信任的容器镜像仓库，之后在创建要纳管的工作负载集群时，默认将信任该容器镜像仓库；也可以参考《SMTX Kubernetes 服务管理指南》中**创建工作负载集群**一章的**配置基本信息**小节，在创建 SKS 工作负载集群的过程中，直接为工作负载集群单独配置受信任的容器镜像仓库。
- 如果已创建要纳管的 SKS 工作负载集群，请参考《SMTX Kubernetes 服务管理指南》的[管理工作负载集群 > 管理受信任容器镜像仓库](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_65)章节，为单个 SKS 工作负载集群配置受信任的容器镜像仓库。

---

## 使用灵雀云 ACP 纳管 SKS 工作负载集群 > 配置集群的审计功能

# 配置集群的审计功能

如果需要通过灵雀云 ACP 采集 SKS 工作负载集群的审计数据，需要先按照如下操作步骤指定与审计相关的 K8s 参数。配置完成后，待集群接入灵雀云 ACP 后即可以在平台的**审计**界面查看集群的审计数据。

**操作步骤**

- 如果未创建要纳管的 SKS 工作负载集群，可参考《SMTX Kubernetes 服务管理指南》的**创建工作负载集群**一章的**配置 K8s 集群**小节，在创建工作负载集群时将如下配置写入**配置内容**，以更新 API Server 参数。

  ```
  controlPlane:
    clusterConfiguration:
      apiServer:
        extraArgs:
          allow-privileged: 'true'
          audit-log-mode: batch
    files:
      - content: |
          apiVersion: audit.k8s.io/v1 # This is required.
          kind: Policy
          # Don't generate audit events for all requests in RequestReceived stage.
          omitStages:
            - "RequestReceived"
          rules:
            # The following requests were manually identified as high-volume and low-risk,
            # so drop them.
            - level: None
              users:
                - system:kube-controller-manager
                - system:kube-scheduler
                - system:serviceaccount:kube-system:endpoint-controller
              verbs: ["get", "update"]
              namespaces: ["kube-system"]
              resources:
                - group: "" # core
                  resources: ["endpoints"]
            # Don't log these read-only URLs.
            - level: None
              nonResourceURLs:
                - /healthz*
                - /version
                - /swagger*
            # Don't log events requests.
            - level: None
              resources:
                - group: "" # core
                  resources: ["events"]
            # Don't log devops requests.
            - level: None
              resources:
              - group: "devops.alauda.io"
            # Don't log get list watch requests.
            - level: None
              verbs: ["get", "list", "watch"]
            # Don't log system's lease operation
            - level: None
              namespaces:
                [
                  "kube-system",
                  "cpaas-system",
                  "alauda-system",
                  "istio-system",
                  "kube-node-lease",
                ]
              resources:
                - group: "coordination.k8s.io"
                  resources: ["leases"]
            # Don't log access review and token review requests.
            - level: None
              resources:
                - group: "authorization.k8s.io"
                  resources: ["subjectaccessreviews", "selfsubjectaccessreviews"]
                - group: "authentication.k8s.io"
                  resources: ["tokenreviews"]
            # Secrets, ConfigMaps can contain sensitive & binary data,
            # so only log at the Metadata level.
            - level: Metadata
              resources:
                - group: "" # core
                  resources: ["secrets", "configmaps"]
            # Default level for known APIs
            - level: RequestResponse
              resources:
                - group: "" # core
                - group: "aiops.alauda.io"
                - group: "apps"
                - group: "app.k8s.io"
                - group: "authentication.istio.io"
                - group: "auth.alauda.io"
                - group: "autoscaling"
                - group: "asm.alauda.io"
                - group: "clusterregistry.k8s.io"
                - group: "crd.alauda.io"
                - group: "infrastructure.alauda.io"
                - group: "monitoring.coreos.com"
                - group: "networking.istio.io"
                - group: "networking.k8s.io"
                - group: "portal.alauda.io"
                - group: "rbac.authorization.k8s.io"
                - group: "storage.k8s.io"
                - group: "tke.cloud.tencent.com"
                - group: "devopsx.alauda.io"
                - group: "core.katanomi.dev"
                - group: "deliveries.katanomi.dev"
                - group: "integrations.katanomi.dev"
                - group: "builds.katanomi.dev"
                - group: "operators.katanomi.dev"
                - group: "tekton.dev"
                - group: "operator.tekton.dev"
                - group: "eventing.knative.dev"
                - group: "flows.knative.dev"
                - group: "messaging.knative.dev"
                - group: "operator.knative.dev"
                - group: "sources.knative.dev"
                - group: "operator.devops.alauda.io"
            # Default level for all other requests.
            - level: Metadata  
        owner: root:root
        path: /etc/kubernetes/auditpolicy.yaml
  ```
- 如果已创建要纳管的 SKS 工作负载集群，可参考《SMTX Kubernetes 服务管理指南》的[管理工作负载集群 > 编辑 K8s 集群配置](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_29)章节，在**配置内容**中按照上述配置更新 API Server 参数。

---

## 使用灵雀云 ACP 纳管 SKS 工作负载集群 > 将集群接入灵雀云 ACP

# 将集群接入灵雀云 ACP

1. 在 CloudTower 管理平台上，参考《SMTX Kubernetes 服务管理指南》中的[管理工作负载集群 > 下载 Kubeconfig 文件](/sks_cn/1.5.1/sks_administration_guide/sks_administration_guide_28#%E4%B8%8B%E8%BD%BD-kubeconfig-%E6%96%87%E4%BB%B6)小节，准备要接入的 SKS 工作负载集群的 Kubeconfig 文件。
2. 登录灵雀云 ACP，进入平台界面后，在界面左上角单击**全栈云原生开放平台**，选择**平台管理**。
3. 在**平台管理**界面中，在左侧导航栏单击**集群管理** > **集群**。
4. 在**集群**界面单击**接入集群**，设置接入集群参数，完成后单击**接入**。

   - **集群类型**：选择标准 Kubernetes 集群。
   - **名称**：填写 SKS 工作负载集群在灵雀云 ACP 的名称。
   - **显示名称**：填写 SKS 工作负载集群在灵雀云 ACP 的显示名称。
   - **集群信息**：单击**解析 KubeConfig 文件**，打开准备好的 Kubeconfig 文件。

完成上述步骤后，集群将处于**接入中**状态，此时灵雀云 ACP 正在刚接入的 SKS 工作负载集群中安装纳管所需要的组件，此过程耗时大约几分钟。接入成功后，如果集群状态显示**正常**，则可以通过灵雀云 ACP 管理 SKS 工作负载集群。

---

## 使用灵雀云 ACP 纳管 SKS 工作负载集群 > 为集群部署监控、日志插件

# 为集群部署监控、日志插件

SKS 工作负载集群接入灵雀云 ACP 后，为增强纳管体验，建议在灵雀云 ACP 上为集群部署以下插件。为避免资源浪费和插件冲突，建议在部署前，确保在 CloudTower 管理平台已关闭 SKS 工作负载集群的**监控**和**日志**插件。

- **日志存储插件**：用于存储集群中的日志、事件、审计数据，并提供消息分发能力。
- **日志采集组件**：用于收集并转发集群中 Linux 节点的日志数据。平台上需要至少有一个集群已部署了日志存储插件，才可以部署该组件。部署完成后，可以在**运维中心** > **日志** > **日志查询分析**查看集群的日志数据。
- **Prometheus**：用于采集、存储、查询、推送、可视化展示集群中节点的监控数据。部署完成后，可以在集群的**概览**和**监控**页面查看集群的监控数据。

**操作步骤**

1. 在**集群**界面单击刚刚接入的 SKS 工作负载集群，进入该集群的管理界面后，单击**插件**页签。
2. 在**插件**页面，部署上述插件，具体操作步骤可以参考灵雀云 ACP 的联机帮助。

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
