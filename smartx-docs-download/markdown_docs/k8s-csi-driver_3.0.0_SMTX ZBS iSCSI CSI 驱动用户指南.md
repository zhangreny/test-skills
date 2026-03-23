---
title: "k8s-csi-driver/3.0.0/SMTX ZBS iSCSI CSI 驱动用户指南"
source_url: "https://internal-docs.smartx.com/k8s-csi-driver/3.0.0/k8s_iscsi_csi_driver_user_guide/k8s_iscsi_csi_driver_user_guide_preface"
sections: 34
---

# k8s-csi-driver/3.0.0/SMTX ZBS iSCSI CSI 驱动用户指南
## 关于本文档

# 关于本文档

本文档介绍了 SMTX ZBS iSCSI CSI 驱动（以下简称“本驱动”）的功能、架构、安装步骤和使用方法。

阅读本文档需对 SMTX ZBS 块存储集群和 Kubernetes 容器编排平台的存储管理功能有一定了解。

---

## 更新信息

# 更新信息

**2025-12-01**：文档随 SMTX ZBS iSCSI CSI 驱动 3.0.0 正式发布。

---

## 概述

# 概述

SMTX ZBS iSCSI CSI 驱动程序（下文简称“本驱动”）是由 SmartX 开发的一款符合 [Kubernetes CSI 规范](https://github.com/container-storage-interface/spec/blob/master/spec)的 CSI Driver 插件，支持 Kubernetes 集群使用 iSCSI 协议从 SMTX ZBS 块存储集群和以分离式部署的 SMTX OS 集群（以下统称 “SMTX ZBS 块存储集群”）获得持久化存储服务。

---

## 概述 > 背景

# 背景

在容器化发展的早期，容器主要承载轻量级的无状态服务，数据通常通过临时本地文件或远程日志系统、数据库等外部存储进行管理。这种模式降低了应用与数据的耦合度，但也带来两个问题：

- Kubernetes 无法统一管理数据；
- 每个应用需单独连接外部存储，增加了复杂性和安全风险。

为解决这一问题，SMTX ZBS 块存储搭配本驱动提供了一体化的持久化存储方案。本驱动以 Pod 的形式运行在 Kubernetes 集群中，通过远程调用（RPC）管理持久卷的生命周期（创建、删除、挂载、卸载等）。  
在这种模式下：

- Kubernetes 通过本驱动接入 SMTX ZBS 块存储集群；
- 每个持久卷对应 SMTX ZBS 块存储集群中的一个 iSCSI LUN；
- 当 Pod 申请存储时，本驱动会在 Pod 所在节点挂载对应的持久卷，并按需创建文件系统，再将其挂载至 Pod 内指定的目录。

通过本驱动， SMTX ZBS 块存储集群可为 Kubernetes 集群中的有状态应用提供稳定可靠的持久化存储，真正实现计算资源和存储资源的解耦与灵活组合。

此外，本驱动还可搭配 **Node Down Pod Handler** 使用，以提升有状态应用在 Kubernetes 节点异常场景下的可恢复性。当运行有状态 Pod 的节点意外宕机时，该工具可检测到节点失联状态，并自动清理故障节点上已失效的 Pod 和持久卷挂载记录，从而使控制器能够在健康节点上快速重建 Pod 并重新挂载卷。配合 SMTX ZBS 的接入点切换机制，Node Down Pod Handler 可显著缩短节点故障后的业务恢复时间，提升系统的高可用性与稳定性。

---

## 概述 > 功能特性

# 功能特性

本驱动程序支持的功能特性如下：

- **卷制备**

  本驱动支持两种持久卷创建方式：**动态创建**与**静态创建**。

  - **动态创建**：由 Kubernetes 根据持久卷申领和存储类定义自动调用本驱动生成持久卷，适用于存储需求变化频繁的场景。
  - **静态创建**：使用 SMTX ZBS 块存储集群中已有的 iSCSI LUN 手动创建持久卷，适用于存储需求固定或对资源有特定要求的场景。
- **卷扩容**

  支持通过修改持久卷申领中的容量规格来扩展持久卷的大小，满足业务数据快速增长的需求。
- **卷克隆**

  支持基于现有的持久卷克隆完整副本。
- **块模式卷**

  支持将 SMTX ZBS 块存储集群的 iSCSI LUN 以原始块设备的形式提供给 Kubernetes 集群使用。
- **卷属性修改**

  支持通过卷属性类或持久卷申领注解动态调整持久卷的属性（例如副本数、IOPS 或吞吐量等），以满足业务在不同阶段的性能要求。
- **卷快照**

  支持动态创建和导入 SMTX ZBS 块存储集群的 iSCSI LUN 快照，并可基于快照恢复原卷。

---

## 概述 > 产品架构

# 产品架构

Kubernetes 集群支持通过本驱动使用 iSCSI 协议接入 SMTX ZBS 块存储集群。整体部署形态及关键组件如下：

![](https://cdn.smartx.com/internal-docs/assets/548a5e98/k8s_csi_driver_installation_guide_01.png)

- **CSI Plugin Pod**

  本驱动程序以 Pod 的形式部署在 Kubernetes 集群中，不同类型的 Pod 提供不同功能。

- **Controller Plugin Pod**

  通常以多副本（默认 2 副本）形式部署在 Kubernetes 集群的多个节点上。主要负责持久卷的生命周期管理，包括：

  - 创建与删除持久卷
  - 持久卷的挂接与分离
  - 卷快照的创建与恢复
- **Node Plugin Pod**

  Node Plugin Pod 运行在 Kubernetes 集群的每一个节点，并与节点上的 Kubelet 交互，负责为调度到本节点的 Pod 提供存储准备工作，包括：

  - 在本节点上挂载或卸载持久卷
  - 执行卷的扩容操作

- **Access Network**

  Kubernetes 集群和 SMTX ZBS 块存储集群通过 Access Network（接入网络）进行通信，该网络独立于 Kubernetes 集群中的业务网络和 SMTX ZBS 块存储集群使用的存储网络。

  Kubernetes 集群可通过接入网络使用 iSCSI 协议访问 SMTX ZBS 块存储集群的存储服务。
- **iSCSI Initiator**

  部署在 Kubernetes 节点上 iSCSI 客户端组件（可为软件或硬件形式），负责与 SMTX ZBS 块存储集群建立连接并完成数据传输。每个节点上的 iSCSI Initiator 会连接至 SMTX ZBS 块存储集群的接入虚拟 IP，从而实现 Kubernetes 集群与存储集群之间的数据交互。
- **iSCSI Target**

  iSCSI Target 是 iSCSI Initiator 访问的存储设备，用于响应 Initiator 的存储访问请求。iSCSI Target 可以提供一个或多个 LUN 供 Kubernetes 集群使用。
- **iSCSI Redirector**

  SMTX ZBS 块存储集群使用 iSCSI Redirector 模式提供 iSCSI 接入服务。SMTX ZBS 块存储集群部署完后会配置一个接入虚拟 IP。iSCSI Initiator 会连接至 SMTX ZBS 块存储集群的接入虚拟 IP，然后由 iSCSI Redirector 引导 Initiator 连接至可用的 iSCSI Target。若 iSCSI Target 发生异常， iSCSI Redirector 将重定向至其他健康 Target，保证高可用性。在重定向之后，所有的数据请求仅在 iSCSI Initiator 与 iSCSI Target 之间进行，无需经过 Redirector。

---

## 概述 > 功能规格

## 功能规格

| 条目 | 最大配置 |
| --- | --- |
| 持久卷总数 | - SMTX ZBS 5.1.0 及以上：100,000 - SMTX ZBS 5.0.0：30,000 - SMTX OS 4.0.7 ~ 4.0.10（分离式部署模式）：30,000 |
| 单卷大小 | 64 TiB |
| 单节点可挂载持久卷数量 | 256 |
| 卷快照总数量 | 100,000 |

---

## 部署驱动 > 部署前准备 > 确认集群和操作系统版本

# 确认集群和操作系统版本

在部署本驱动前，必须参考《SMTX ZBS iSCSI CSI 驱动发布说明》中的版本配套说明，确认 Kubernetes 集群、Linux 操作系统，以及 SMTX ZBS 块存储集群的版本与本驱动版本兼容。

> **说明**：
>
> - 请确保 kube-apiserver 带有 `--allow-privileged=true` 启动参数（大部份情况下，它是默认开启的）。
> - 请确保 Kubernetes 节点上的 9811 端口未被占用。否则，您可以在安装时将 `node.sidecars.livenessProbe.httpPort` 设置为其他合适的端口号以避免端口冲突。

---

## 部署驱动 > 部署前准备 > 安装命令行工具（仅在线部署/升级/卸载需要）

# 安装命令行工具（仅在线部署/升级/卸载需要）

在线部署/升级/卸载本驱动时，需要安装如下工具：

- **Helm**：请参考 [Helm 文档](https://helm.sh/zh/docs/intro/install/)进行安装。
- **yq**：请参考 [yq 文档](https://github.com/mikefarah/yq?tab=readme-ov-file#install)进行安装。
- **kubectl**：请参考 [Kubernetes 文档](https://kubernetes.io/docs/tasks/tools/#kubectl)进行安装。

---

## 部署驱动 > 部署前准备 > 安装 Open-iSCSI

# 安装 Open-iSCSI

Open-iSCSI 是使用 RFC3720 iSCSI 协议实现的高性能 Initiator 程序。在安装并配置完 open-iscsi 后，Kubernetes 各节点可以直接访问 SMTX ZBS 块存储集群的 iSCSI 存储。

当 Kubernetes 节点的操作系统属于以下列表，且已配置可用的软件包源时，本驱动程序会自动安装 **Open-iSCSI** 软件包，并启动 iscsid 系统服务：

- CentOS
- Debian
- Fedora
- Rocky
- Ubuntu

若您的 Kubernetes 节点的操作系统不在上述列表之中，或者未配置有可访问的软件包源，请参考如下操作，手动安装 Open-iSCSI 软件包。手动安装完成后，本驱动程序会自动跳过安装步骤，继续配置并启动 iscsid 系统服务。

**手动安装 Open-iSCSI 操作步骤：**

在 Kubernetes 的每一个工作节点上执行如下命令：

- **CentOS**

  `sudo yum install iscsi-initiator-utils`
- **SUSE/openSUSE**

  `sudo zypper install open-iscsi`
- **Debian/Ubuntu**

  `sudo apt-get install open-iscsi`
- **CoreOS**

  `sudo rpm-ostree install iscsi-initiator-utils`

---

## 部署驱动 > 部署前准备 > 配置 SMTX ZBS 块存储集群的接入虚拟 IP

# 配置 SMTX ZBS 块存储集群的接入虚拟 IP

SMTX ZBS 块存储集群支持配置接入虚拟 IP，用于对外提供统一的块存储接入服务。配置完成后，所有 iSCSI 请求将通过该接入虚拟 IP 接入，并由 iSCSI 重定向服务转发至集群内可用的存储节点。当某一存储节点发生异常时，iSCSI 服务会自动重定向至新的可用节点，从而确保存储服务的高可用性。

本驱动程序依赖 SMTX ZBS 块存储集群的接入虚拟 IP 与 Kubernetes 集群通信。因此，在安装本驱动程序之前，请先确保 SMTX ZBS 块存储集群已配置了接入虚拟 IP。该接入虚拟 IP 在安装本驱动程序时将使用，请务必提前记录该 IP。

接入虚拟 IP 的配置，请参考如下步骤：

1. 登录 CloudTower，进入 SMTX ZBS 块存储集群的管理界面，单击**设置**，选择**虚拟 IP**。
2. 填写接入虚拟 IP 地址。
3. 单击**保存**。

> **说明**：
>
> - 接入虚拟 IP 与接入网络必须属于同一网段。
> - 对于 4.0.7 ~ 4.0.10 版本的 SMTX OS 集群（分离式部署模式），可通过单击集群的 Web 控制台主界面的**设置**按钮，选择**虚拟 IP** > **编辑**，在弹出的对话框中的 **iSCSI 服务虚拟 IP** 栏，填写该集群对应的接入虚拟 IP。

---

## 部署驱动 > 执行部署 > 在线部署

# 在线部署

您可以在 Kubernetes 集群中，通过 Helm 工具完成本驱动程序的在线部署。

1. 执行以下命令，添加 SmartX Chart 仓库：

   ```
   helm repo add smartx https://smartx.com/charts
   helm repo update smartx
   ```
2. 导出默认 values.yaml 文件。

   values.yaml 文件用于定义本驱动安装参数。在部署本驱动时，Helm 会根据该文件内容生成最终的 Kubernetes 资源清单。默认的 values.yaml 文件已提供初始参数。您可以在部署前通过编辑此文件，自定义安装参数以适配您的集群环境。

   ```
   helm show values --version v3.0.0 smartx/csi-driver-zbs-iscsi > ./values.yaml
   ```
3. 配置 SMTX ZBS 块存储集群的虚拟接入 IP，用于本驱动和 SMTX ZBS 块存储集群的连接。

   ```
   export ZBS_IP=<access_vip> # 请指定 SMTX ZBS 集群的接入虚拟 IP。

   yq -i ".zbsIP = \"$ZBS_IP\"" ./values.yaml
   ```
4. 在 Kubernetes 集群中任意一个节点上执行 `ps \-ef | grep kubelet | grep root-dir` 命令。若输出为空或者 `/var/lib/kubelet`，可跳过这一步。否则代表集群的 kubelet 目录路径做了定制，需要配置定制后的 kubelet 目录路径。

   ```
   export KUBELET_DIR=/var/lib/kubelet # 请指定定制后的 kubelet 目录路径。

   yq -i ".node.kubeletDir = \"$KUBELET_DIR\"" ./values.yaml
   ```
5. （可选）本驱动默认使用 Docker Hub 上的容器镜像。如果 Kubernetes 集群无法访问 Docker Hub，可以选择切换到腾讯云容器镜像仓库。

   ```
   export IMAGE_NAMESPACE=ccr.ccs.tencentyun.com/smartxworks

   yq -i ".imageNamespaceOverride = \"$IMAGE_NAMESPACE\"" ./values.yaml
   ```
6. 查看修改后的 values.yaml 文件。如有必要，可进行其他修改。

   ```
   cat ./values.yaml | less
   ```
7. 执行以下命令安装本驱动程序。

   ```
   export NAMESPACE=kube-system     # 请指定安装本驱动的名字空间。
   export NAME=csi-driver-zbs-iscsi # 请指定安装本驱动的名称。

   helm install --version v3.0.0 -f ./values.yaml -n $NAMESPACE $NAME smartx/csi-driver-zbs-iscsi
   ```
8. 执行以下命令检查各组件的运行状态是否正常。

   ```
   kubectl get pods -n $NAMESPACE -l app.kubernetes.io/instance=$NAME -w
   ```

   示例输出如下，若各组件状态为 `Running`，说明运行正常：

   ```
    NAME                                               READY   STATUS    RESTARTS   AGE
    csi-driver-zbs-iscsi-controller-649c7dff4d-s29gh   7/7     Running   0          49s
    csi-driver-zbs-iscsi-node-c52d9                    3/3     Running   0          49s
    csi-driver-zbs-iscsi-node-g5hsz                    3/3     Running   0          44s
    csi-driver-zbs-iscsi-node-q6fp5                    3/3     Running   0          46s
   ```
9. 安装[卷快照控制器](https://github.com/kubernetes-csi/external-snapshotter)，并检查卷快照控制器的组件状态。若各组件状态为 Running，说明运行正常。

   本驱动程序的卷快照功能依赖于独立于任何 CSI 驱动程序的卷快照控制器。若 Kubernetes 集群中已安装卷快照控制器，可跳过这一步。

   - **对于 1.20 及以上版本的 Kubernetes 集群**

     ```
     kubectl create --save-config -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/groupsnapshot.storage.k8s.io_volumegroupsnapshotclasses.yaml
     kubectl create --save-config -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/groupsnapshot.storage.k8s.io_volumegroupsnapshotcontents.yaml
     kubectl create --save-config -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/groupsnapshot.storage.k8s.io_volumegroupsnapshots.yaml
     kubectl create --save-config -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/snapshot.storage.k8s.io_volumesnapshotclasses.yaml
     kubectl create --save-config -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/snapshot.storage.k8s.io_volumesnapshotcontents.yaml
     kubectl create --save-config -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/snapshot.storage.k8s.io_volumesnapshots.yaml
     kubectl create --save-config -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/deploy/kubernetes/snapshot-controller/rbac-snapshot-controller.yaml
     kubectl create --save-config -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/deploy/kubernetes/snapshot-controller/setup-snapshot-controller.yaml
     kubectl get pods -n kube-system -l app.kubernetes.io/name=snapshot-controller -w
     ```
   - **对于低于 1.20 版本的 Kubernetes 集群**

     ```
     kubectl create --save-config -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/client/config/crd/snapshot.storage.k8s.io_volumesnapshotclasses.yaml
     kubectl create --save-config -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/client/config/crd/snapshot.storage.k8s.io_volumesnapshotcontents.yaml
     kubectl create --save-config -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/client/config/crd/snapshot.storage.k8s.io_volumesnapshots.yaml
     kubectl create --save-config -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/deploy/kubernetes/snapshot-controller/rbac-snapshot-controller.yaml
     kubectl create --save-config -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/deploy/kubernetes/snapshot-controller/setup-snapshot-controller.yaml
     kubectl get pods -n default -l app=snapshot-controller -w
     ```
10. （可选）安装 Node Down Pod Handler。 Node Down Pod Handler 可加速有状态应用在节点故障时的跨节点恢复，建议安装。

    1. 导出 Node Down Pod Handler 的默认 values.yaml 文件。

       ```
       helm show values --version v1.0.0 smartx/node-down-pod-handler > ./node-down-pod-handler-values.yaml
       ```
    2. （可选）Node Down Pod Handler 默认使用 Docker Hub 上的容器镜像。若 Kubernetes 集群无法访问 Docker Hub，可选择切换到腾讯云容器镜像仓库。

       ```
       export NODE_DOWN_POD_HANLDER_IMAGE_NAMESPACE=ccr.ccs.tencentyun.com/smartxworks

       yq -i ".image.repository = \"$NODE_DOWN_POD_HANLDER_IMAGE_NAMESPACE/node-down-pod-handler\"" ./node-down-pod-handler-values.yaml
       ```
    3. 查看修改后的 values.yaml 文件。如有必要，可进行其他修改。

       ```
       cat ./node-down-pod-handler-values.yaml | less
       ```
    4. 安装 Node Down Pod Handler，并检查组件状态。若各组件状态为 `Running`，说明运行正常。

       ```
       export NODE_DOWN_POD_HANDLER_NAMESPACE=kube-system      # 指定安装 Node Down Pod Handler 的名字空间。
       export NODE_DOWN_POD_HANDLER_NAME=node-down-pod-handler # 指定安装 Node Down Pod Handler 的名称。

       helm install --version v1.0.0 -f ./node-down-pod-handler-values.yaml -n $NODE_DOWN_POD_HANDLER_NAMESPACE $NODE_DOWN_POD_HANDLER_NAME smartx/node-down-pod-handler
       kubectl get pods -n $NODE_DOWN_POD_HANDLER_NAMESPACE -l app.kubernetes.io/instance=$NODE_DOWN_POD_HANDLER_NAME -w
       ```

---

## 部署驱动 > 执行部署 > 离线部署

# 离线部署

本驱动支持在离线环境通过安装包部署。离线安装包已包含了安装本驱动程序所需的Helm charts、容器镜像和必要的命令行工具，依赖内部私有镜像仓库，即可实现离线部署。

部署前，请提前获取离线安装包。

**操作步骤**

以下命令均需在离线安装包目录内执行。

1. 解压离线安装包，并进入安装包目录：

   ```
   tar xf csi-driver-zbs-iscsi-v3.0.0-airgap.tar.gz && cd csi-driver-zbs-iscsi-v3.0.0-airgap
   ```
2. 导出默认的 values.yaml 文件。

   values.yaml 文件用于定义本驱动安装参数。在部署本驱动时，Helm 会根据该文件内容生成最终的 Kubernetes 资源清单。默认的 values.yaml 文件已提供初始参数。您可以在部署前通过编辑此文件，自定义安装参数以适配您的集群环境。

   ```
   ./bin/linux-$(uname -m)/helm show values ./charts/csi-driver-zbs-iscsi-v3.0.0.tgz > ./values.yaml
   ```
3. 配置 SMTX ZBS 块存储集群的接入虚拟 IP，用于本驱动和 SMTX ZBS 块存储集群的连接。

   ```
   export ZBS_IP=10.0.0.1 # SMTX ZBS 块存储集群的接入虚拟 IP。

   ./bin/linux-$(uname -m)/yq -i ".zbsIP = \"$ZBS_IP\"" ./values.yaml
   ```
4. 在 Kubernetes 集群中任意一个节点上执行 `ps \-ef | grep kubelet | grep root-dir` 命令。若输出为空或者 `/var/lib/kubelet`，可跳过这一步。否则代表集群的 kubelet 目录路径做了定制，需要配置定制后的 kubelet 目录路径。

   ```
   export KUBELET_DIR=/var/lib/kubelet # 请指定定制后的 kubelet 目录路径。

   ./bin/linux-$(uname -m)/yq -i ".node.kubeletDir = \"$KUBELET_DIR\"" ./values.yaml
   ```
5. 将本驱动的容器镜像推送到私有镜像仓库，并更新配置文件中镜像地址，确保安装过程可从私有仓库拉取镜像。

   ```
   export IMAGE_NAMESPACE=ccr.ccs.tencentyun.com/smartxworks # 指定私有容器镜像仓库，此处以 ccr.ccs.tencentyun.com/smartxworks 为例。

   for file in images/*; do
     ./bin/linux-$(uname -m)/crane push --index $file $IMAGE_NAMESPACE/${file##*/}
   done
   ./bin/linux-$(uname -m)/yq -i ".imageNamespaceOverride = \"$IMAGE_NAMESPACE\"" ./values.yaml
   ```

   > **注意**：
   >
   > 若上述命令报错 `UNAUTHORIZED`，请执行 `./bin/linux-$(uname \-m)/crane auth login` 命令登录私有镜像仓库后再次尝试。
6. 查看修改后的 values.yaml 文件。如有必要，可进行其他修改。

   ```
   cat ./values.yaml | less
   ```
7. 执行以下命令安装本驱动程序：

   ```
   export NAMESPACE=kube-system     # 请指定安装本驱动的名字空间，此处以 kube-system 为例。 
   export NAME=csi-driver-zbs-iscsi # 请指定安装本驱动的名称，此处以 csi-driver-zbs-iscsi 为例。 

   ./bin/linux-$(uname -m)/helm install -f ./values.yaml -n $NAMESPACE $NAME ./charts/csi-driver-zbs-iscsi-v3.0.0.tgz
   ```
8. 执行以下命令检查本驱动各组件的运行状态是否正常：

   ```
   ./bin/linux-$(uname -m)/kubectl get pods -n $NAMESPACE -l app.kubernetes.io/instance=$NAME -w
   ```

   示例输出如下，若各组件状态为 Running，说明运行正常：

   ```
    NAME                                               READY   STATUS    RESTARTS   AGE
    csi-driver-zbs-iscsi-controller-649c7dff4d-s29gh   7/7     Running   0          49s
    csi-driver-zbs-iscsi-node-c52d9                    3/3     Running   0          49s
    csi-driver-zbs-iscsi-node-g5hsz                    3/3     Running   0          44s
    csi-driver-zbs-iscsi-node-q6fp5                    3/3     Running   0          46s
   ```
9. 安装[卷快照控制器](https://github.com/kubernetes-csi/external-snapshotter)，并检查组件状态。若各组件状态为 Running，说明运行正常。

   本驱动程序的卷快照功能依赖于独立于任何 CSI 驱动程序的卷快照控制器。若 Kubernetes 集群中已安装卷快照控制器，可跳过这一步。

   - **对于 1.20 及以上版本的 Kubernetes 集群**

     ```
     export SNAPSHOT_CONTROLLER_IMAGE_NAMESPACE=ccr.ccs.tencentyun.com/smartxworks # 指定私有容器镜像仓库，此处以 ccr.ccs.tencentyun.com/smartxworks 为例。
     export SNAPSHOT_CONTROLLER_NAMESPACE=kube-system                              # 指定安装卷快照控制器的名字空间，此处以 kube-system 为例。

     ./bin/linux-$(uname -m)/yq -i "(.images.[] | select(.name == \"registry.k8s.io/sig-storage/snapshot-controller\").newName) = \"$SNAPSHOT_CONTROLLER_IMAGE_NAMESPACE/snapshot-controller\"" ./manifests/snapshot-controller-v7.0.2/kustomization.yaml
     ./bin/linux-$(uname -m)/yq -i ".namespace = \"$SNAPSHOT_CONTROLLER_NAMESPACE\"" ./manifests/snapshot-controller-v7.0.2/kustomization.yaml
     ./bin/linux-$(uname -m)/kubectl create --save-config -k ./manifests/snapshot-controller-v7.0.2/
     ./bin/linux-$(uname -m)/kubectl get pods -n $SNAPSHOT_CONTROLLER_NAMESPACE -l app.kubernetes.io/name=snapshot-controller -w
     ```
   - **对于低于 1.20 版本的 Kubernetes 集群**

     ```
     export SNAPSHOT_CONTROLLER_IMAGE_NAMESPACE=ccr.ccs.tencentyun.com/smartxworks # 指定私有容器镜像仓库，此处以 ccr.ccs.tencentyun.com/smartxworks 为例。
     export SNAPSHOT_CONTROLLER_NAMESPACE=kube-system                              # 指定安装卷快照控制器的名字空间，此处以 kube-system 为例。

     ./bin/linux-$(uname -m)/yq -i "(.images.[] | select(.name == \"k8s.gcr.io/sig-storage/snapshot-controller\").newName) = \"$SNAPSHOT_CONTROLLER_IMAGE_NAMESPACE/snapshot-controller\"" ./manifests/snapshot-controller-v3.0.3/kustomization.yaml
     ./bin/linux-$(uname -m)/yq -i ".namespace = \"$SNAPSHOT_CONTROLLER_NAMESPACE\"" ./manifests/snapshot-controller-v3.0.3/kustomization.yaml
     ./bin/linux-$(uname -m)/kubectl create --save-config -k ./manifests/snapshot-controller-v3.0.3/
     ./bin/linux-$(uname -m)/kubectl get pods -n $SNAPSHOT_CONTROLLER_NAMESPACE -l app=snapshot-controller -w
     ```
10. （可选）安装 Node Down Pod Handler。Node Down Pod Handler 可加速有状态应用在节点故障时的跨节点恢复，建议安装。

    1. 导出 Node Down Pod Handler 的默认 values.yaml 文件。

       ```
       ./bin/linux-$(uname -m)/helm show values ./charts/node-down-pod-handler-v1.0.0.tgz > ./node-down-pod-handler-values.yaml
       ```
    2. 更新配置文件中镜像地址，确保安装过程可从私有仓库拉取镜像。

       ```
       export NODE_DOWN_POD_HANLDER_IMAGE_NAMESPACE=ccr.ccs.tencentyun.com/smartxworks # 指定私有容器镜像仓库，此处以 ccr.ccs.tencentyun.com/smartxworks 为例。

       ./bin/linux-$(uname -m)/yq -i ".image.repository = \"$NODE_DOWN_POD_HANLDER_IMAGE_NAMESPACE/node-down-pod-handler\"" ./node-down-pod-handler-values.yaml
       ```
    3. 查看修改后的 values.yaml 文件。如有必要，可进行其他修改。

       ```
       cat ./node-down-pod-handler-values.yaml | less
       ```
    4. 安装 Node Down Pod Handler，并检查组件状态。若各组件状态为 `Running`，说明运行正常。

       ```
       export NODE_DOWN_POD_HANDLER_NAMESPACE=kube-system      # 指定安装 Node Down Pod Handler 的名字空间，此处以 kube-system 为例。
       export NODE_DOWN_POD_HANDLER_NAME=node-down-pod-handler # 指定安装 Node Down Pod Handler 的名称，此处以 node-down-pod-handler 为例。

       ./bin/linux-$(uname -m)/helm install -f ./node-down-pod-handler-values.yaml -n $NODE_DOWN_POD_HANDLER_NAMESPACE $NODE_DOWN_POD_HANDLER_NAME ./charts/node-down-pod-handler-v1.0.0.tgz
       ./bin/linux-$(uname -m)/kubectl get pods -n $NODE_DOWN_POD_HANDLER_NAMESPACE -l app.kubernetes.io/instance=$NODE_DOWN_POD_HANDLER_NAME -w
       ```

---

## 管理持久卷

# 管理持久卷

在 Kubernetes 中，持久卷与持久卷申领是访问外部存储的基础机制。本驱动通过存储类与 SMTX ZBS 块存储集群交互，实现持久卷的动态创建。

持久卷管理涉及以下几个核心对象：

- **存储类**：定义如何通过本驱动向 SMTX ZBS 块存储集群申请存储资源。可设置副本数、纠删码配置、I/O 限速、加密算法等多种参数。
- **持久卷申领**：声明 Pod 的存储需求，例如持久卷的容量和访问模式。持久卷申领提交将自动触发本驱动在 SMTX ZBS 块存储集群创建卷。
- **持久卷**：本驱动在 SMTX ZBS 块存储集群创建的存储资源，在与持久卷申领一对一绑定后供 Pod 使用。
- **Pod**：通过挂载持久卷申领使用持久卷。

---

## 管理持久卷 > 创建持久卷

# 创建持久卷

本驱动支持两种持久卷的创建方式：

- **动态创建**

  Kubernetes 根据持久卷申领的请求和预定义的存储类自动调用本驱动在 SMTX ZBS 块存储集群创建持久卷，并在与持久卷申领绑定后供 Pod 挂载使用。此方式无需手动创建持久卷，适用于存储需求变化频繁的场景。
- **静态创建**

  支持使用 SMTX ZBS 块存储集群已有的 iSCSI LUN 静态创建持久卷，并在和持久卷申领绑定后供 Pod 使用。此方式适用于存储需求固定且对存储资源有特定要求的场景。

---

## 管理持久卷 > 创建持久卷 > 动态创建持久卷

# 动态创建持久卷

1. 在执行操作前，请设置以下参数和值并导出为环境变量，以便后续命令调用。

   ```
   export DRIVER_NAME=iscsi.zbs.csi.smartx.com 
   export NAMESPACE=default      
   export SC_NAME=zbs-iscsi-sc   
   export PVC_NAME=zbs-iscsi-pvc 
   export VOLUME_CAPACITY=2Gi
   ```

   参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `DRIVER_NAME` | 指定使用的 CSI 驱动名称。本驱动默认值为 `iscsi.zbs.csi.smartx.com`。若本版本由从 3.0.0 以下版本升级而来，请修改为 `com.smartx.csi-driver`。 | `iscsi.zbs.csi.smartx.com` |
   | `NAMESPACE` | 指定持久卷申领所在的命名空间，可自定义。 | `default` |
   | `SC_NAME` | 指定存储类名称，可自定义。 | `zbs-iscsi-sc` |
   | `PVC_NAME` | 指定持久卷申领的名称，可自定义。 | `zbs-iscsi-pvc` |
   | `VOLUME_CAPACITY` | 指定新建卷的容量。卷容量必须为 2Gi 的整数倍，若设置的值非 2Gi 整数倍，将自动向上调整为最近的 2Gi 整数倍。 | `2Gi` |
2. 创建存储类。如果使用已存在的存储类，可跳过此步骤。

   ```
   kubectl create -f - <<EOF
   apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: $SC_NAME             # 存储类名称
   provisioner: $DRIVER_NAME    # 置备持久卷的 CSI 驱动名称。
   allowVolumeExpansion: true  
   parameters:                  
   EOF
   ```

   主要参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `allowVolumeExpansion` | 是否允许对持久卷进行扩容。 - **true**: 可对持久卷扩容 - **false**: 不允许对持久卷扩容 | `true` |
   | `parameters` | 定义持久卷属性（冗余策略、分层策略、数据加密、I/O 限速等）。支持设置的具体 Parameters 参数见 [API 参考](/k8s-csi-driver/3.0.0/k8s_iscsi_csi_driver_user_guide/k8s_iscsi_csi_driver_user_guide_30)。 **注意**：  - 副本参数和纠删码参数不允许同时设置。 - 若接入的集群为 SMTX ZBS 双活集群，则必须使用副本策略，且副本数必须设置为 3。 - 纠删码参数仅支持在卷创建时指定，不支持修改。 - 新建持久卷默认采用分层模式：较高访问频率的数据停留在速度更快的性能层，访问频率较低的数据下沉至速度相对较慢但容量较大的容量层。您也可以指定分层策略为 `None`，将卷数据始终保留在性能层，从而获得更稳定的高性能。 | `-` |
3. 创建持久卷申领。

   持久卷申领定义了 Pod 对存储的需求，Kubernetes 会根据其规格与存储类的定义，调用本驱动在 SMTX ZBS 块存储集群动态创建实际的持久卷。

   ```
   kubectl create -f - <<EOF
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: $PVC_NAME              # 持久卷申领名称
     namespace: $NAMESPACE        # 持久卷申领所在的名字空间
   spec:
     storageClassName: $SC_NAME   # 存储类名称
     volumeMode: Filesystem
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: $VOLUME_CAPACITY
   EOF
   ```

   主要参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `volumeMode` | 指定卷在 Pod 中以何种形式使用。默认为 `Filesystem`。  - **Filesystem**：持久卷以文件系统形式挂载到 Pod 中，适用于大多数通用场景。 - **Block**：持久卷以原始块设备形式直接挂载到 Pod。 | `Filesystem` |
   | `accessModes` | 指定持久卷的访问模式。  其中 `Block` 类型的持久卷支持以下四种访问模式，而 `Filesystem` 类型的持久卷仅支持 ReadWriteOnce 和 ReadWriteOncePod。  - **ReadWriteOnce**：持久卷可被单个节点以读写方式挂载。 - **ReadOnlyMany**：持久卷可被多个节点同时以只读方式挂载。 - **ReadWriteMany**：持久卷可被多个节点同时以读写方式挂载。 - **ReadWriteOncePod**：持久卷仅可被单个节点上的一个 Pod 以读写方式挂载。 | `ReadWriteOnce` |
   | `storage` | 指定持久卷的容量。 | `$VOLUME_CAPACITY` |
4. 等待持久卷申领和持久卷绑定。持久卷申领与持久卷需绑定后才能被 Pod 使用。

   ```
   kubectl wait --for jsonpath='{.status.phase}'=Bound -n $NAMESPACE pvc/$PVC_NAME
   ```
5. （可选）创建一个临时 Pod 并挂载持久卷申领，验证持久卷的可用性以及容量是否符合预期。若 Pod 无法正常挂载持久卷申领，请联系 SmartX 售后工程师处理。

   ```
   export POD_NAME=zbs-iscsi-pod # 请指定 Pod 名称。

   kubectl create -f - <<EOF
   apiVersion: v1
   kind: Pod
   metadata:
     name: $POD_NAME
     namespace: $NAMESPACE
   spec:
     restartPolicy: OnFailure
     containers:
       - name: busybox
         image: busybox
         imagePullPolicy: IfNotPresent
         args:
           - df
           - -h
           - /data
         volumeMounts:
           - name: data
             mountPath: /data
     volumes:
       - name: data
         persistentVolumeClaim:
           claimName: $PVC_NAME
   EOF

   kubectl wait --for jsonpath='{.status.phase}'=Succeeded -n $NAMESPACE pod/$POD_NAME
   kubectl logs -n $NAMESPACE $POD_NAME
   ```

   示例输出：

   ```
   Filesystem                Size      Used Available Use% Mounted on
   /dev/sda                  1.9G     24.0K      1.9G   0% /data
   ```

---

## 管理持久卷 > 创建持久卷 > 静态创建持久卷

# 静态创建持久卷

本驱动程序支持使用 SMTX ZBS 块存储集群已有的 iSCSI LUN 静态创建持久卷，并在和持久卷申领绑定后供 Kubernetes 集群使用。

**操作步骤**

1. 登录 CloudTower，进入 SMTX ZBS 块存储集群，查看要使用的 iSCSI LUN 的 UUID 和容量大小。
2. 请设置以下参数和值并导出为环境变量，以便后续命令调用。

   ```
   export DRIVER_NAME=iscsi.zbs.csi.smartx.com
   export VOLUME_UUID=9e01f32d-eccb-444e-a6ed-60eda2593342  
   export VOLUME_CAPACITY=2Gi                               
   export NAMESPACE=default                                 
   export PV_NAME=zbs-iscsi-pv-import                      
   export PVC_NAME=zbs-iscsi-pvc-import
   ```

   参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `DRIVER_NAME` | 指定使用的 CSI 驱动名称。本驱动默认值为 `iscsi.zbs.csi.smartx.com`。若本版本由从 3.0.0 以下版本升级而来，请修改为 `com.smartx.csi-driver`。 | `iscsi.zbs.csi.smartx.com` |
   | `VOLUME_UUID` | 输入持久卷要使用的 SMTX ZBS iSCSI LUN 的 UUID。 | `9e01f32d-eccb-444e-a6ed-60eda2593342` |
   | `VOLUME_CAPACITY` | 请输入要使用的 SMTX ZBS iSCSI LUN 的容量。 | `2Gi` |
   | `NAMESPACE` | 指定持久卷申领所在的命名空间，可自定义。 | `default` |
   | `PV_NAME` | 指定新建持久卷的名称，可自定义。 | `zbs-iscsi-pv-import` |
   | `PVC_NAME` | 指定新建持久卷申领的名称，可自定义。 | `zbs-iscsi-pvc-import` |
3. 创建持久卷。

   ```
   kubectl create -f - <<EOF
   apiVersion: v1
   kind: PersistentVolume
   metadata:
     name: $PV_NAME                        # 持久卷名称
   spec:
     persistentVolumeReclaimPolicy: Retain
     csi:
       driver: $DRIVER_NAME                # CSI 驱动名称
       volumeHandle: $VOLUME_UUID          # 持久卷使用的 iSCSI LUN 的 UUID
     capacity:
       storage: $VOLUME_CAPACITY           
     volumeMode: Filesystem
     accessModes:
       - ReadWriteOnce
     claimRef:
       name: $PVC_NAME                     
       namespace: $NAMESPACE               
   EOF
   ```

   主要参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `persistentVolumeReclaimPolicy` | 持久卷的回收策略，用于定义持久卷关联的持久卷申领被删除后，对持久卷的处理方式。  - **Retain**：持久卷不会被删除，仍将被保留。 - **Delete**：持久卷将被删除。 | `Retain` |
   | `volumeMode` | 指定持久卷在 Pod 中以何种形式使用。默认为 `Filesystem`。  - **Filesystem**：持久卷以文件系统形式挂载到 Pod 中，适用于大多数通用场景。 - **Block**：持久卷以原始块设备形式直接挂载到 Pod。 | `Filesystem` |
   | `accessModes` | 指定持久卷的访问模式。其中 `Block` 类型的持久卷支持以下四种访问模式，而 `Filesystem` 类型的持久卷仅支持 ReadWriteOnce 和 ReadWriteOncePod。  - **ReadWriteOnce**：持久卷可被单个节点以读写方式挂载。 - **ReadOnlyMany**：持久卷可被多个节点同时以只读方式挂载。 - **ReadWriteMany**：持久卷可被多个节点同时以读写方式挂载。 - **ReadWriteOncePod**：持久卷仅可被单个节点上的一个 Pod 以读写方式挂载。 | `ReadWriteOnce` |
4. 创建持久卷申领。

```
kubectl create -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: $PVC_NAME
  namespace: $NAMESPACE
spec:
  storageClassName: ""
  volumeName: $PV_NAME
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: $VOLUME_CAPACITY
EOF
```

5. 等待持久卷申领和持久卷绑定。持久卷申领与持久卷需绑定后才能被 Pod 使用。

   ```
   kubectl wait --for jsonpath='{.status.phase}'=Bound -n $NAMESPACE pvc/$PVC_NAME
   ```
6. （可选）创建一个临时 Pod 并挂载持久卷申领，验证持久卷的可用性以及容量是否符合预期。若 Pod 无法正常挂载持久卷申领，请联系 SmartX 售后工程师处理。

   ```
   export POD_NAME=zbs-iscsi-pod # 请指定 Pod 名称。

   kubectl create -f - <<EOF
   apiVersion: v1
   kind: Pod
   metadata:
     name: $POD_NAME
     namespace: $NAMESPACE
   spec:
     restartPolicy: OnFailure
     containers:
       - name: busybox
         image: busybox
         imagePullPolicy: IfNotPresent
         args:
           - df
           - -h
           - /data
         volumeMounts:
           - name: data
             mountPath: /data
     volumes:
       - name: data
         persistentVolumeClaim:
           claimName: $PVC_NAME
   EOF

   kubectl wait --for jsonpath='{.status.phase}'=Succeeded -n $NAMESPACE pod/$POD_NAME
   kubectl logs -n $NAMESPACE $POD_NAME
   ```

   示例输出：

   ```
   Filesystem                Size      Used  Available  Use%  Mounted on
   /dev/sda                  1.9G     24.0K      1.9G   0%   /data
   ```

---

## 管理持久卷 > 修改持久卷

# 修改持久卷

本驱动支持通过持久卷申领注解，来对持久卷的相关属性进行修改。

1. 请设置以下参数和值并导出为环境变量，以便后续命令引用。此处以修改将持久卷的最大吞吐量修改为 10 Mib 为例。您也可以自定义修改其他属性。

   ```
   export DRIVER_NAME=iscsi.zbs.csi.smartx.com  
   export NAMESPACE=default  
   export PVC_NAME=zbs-iscsi-pvc  
   export PARAM_NAME=throughput  
   export PARAM_VALUE=10Mi
   ```

   主要参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `DRIVER_NAME` | 指定使用的 CSI 驱动名称。本驱动默认值为 `iscsi.zbs.csi.smartx.com`。  若本版本由从 3.0.0 以下版本升级而来，请修改为 `com.smartx.csi-driver`。 | `iscsi.zbs.csi.smartx.com` |
   | `NAMESPACE` | 指定要修改的持久卷所在的名字空间。 | `default` |
   | `PVC_NAME` | 指定要修改持久卷绑定的持久卷申领名称。 | `zbs-iscsi-pvc` |
   | `PARAM_NAME` | 指定要修改的持久卷的参数名称。支持修改的卷参数见 [API 参考](/k8s-csi-driver/3.0.0/k8s_iscsi_csi_driver_user_guide/k8s_iscsi_csi_driver_user_guide_30)。  **注意**：副本参数和纠删码参数不允许同时设置。  副本数仅允许提升，不允许降低。  不支持修改纠删码参数。 | `throughput` |
   | `PARAM_VALUE` | 指定修改后的参数值。 | `10Mi` |
2. 更新持久卷申领注解。

   ```
   kubectl annotate -n $NAMESPACE pvc/$PVC_NAME $DRIVER_NAME/$PARAM_NAME=$PARAM_VALUE
   ```
3. 等待持久卷修改完成。

   ```
   kubectl wait --for jsonpath="{.metadata.annotations['${DRIVER_NAME//./\\.}/$PARAM_NAME']}"=$PARAM_VALUE pv/$(kubectl get -o jsonpath='{.spec.volumeName}' -n $NAMESPACE pvc/$PVC_NAME)
   ```

---

## 管理持久卷 > 扩容持久卷

# 扩容持久卷

1. 请设置以下参数和值并导出为环境变量，以便后续命令调用。

   ```
   export NAMESPACE=default
   export PVC_NAME=zbs-iscsi-pvc
   export VOLUME_CAPACITY=4Gi
   ```

   参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `NAMESPACE` | 指定要扩容的持久卷所在的名字空间。 | `default` |
   | `PVC_NAME` | 指定要扩容的持久卷绑定的持久卷申领名称。 | `zbs-iscsi-pvc` |
   | `VOLUME_CAPACITY` | 指定要持久卷扩容后的容量。卷容量必须为 2Gi 的整数倍，若设置的值非 2Gi 整数倍，将自动向上调整为最近的 2Gi 整数倍。 | `4Gi` |
2. 更新持久卷申领的 `spec.resources.requests.storage` 字段。

   ```
   kubectl patch -p "{\"spec\":{\"resources\":{\"requests\":{\"storage\":\"$VOLUME_CAPACITY\"}}}}" -n $NAMESPACE pvc/$PVC_NAME
   ```
3. 等待持久卷扩容完成。

   ```
   kubectl wait --for jsonpath='{.spec.capacity.storage}'=$VOLUME_CAPACITY pv/$(kubectl get -o jsonpath='{.spec.volumeName}' -n $NAMESPACE pvc/$PVC_NAME)
   ```
4. （可选）创建一个临时 Pod 并挂载持久卷申领，验证持久卷的可用性以及容量是否符合预期。若 Pod 无法正常挂载持久卷申领，请联系 SmartX 售后工程师处理。

   ```
   export POD_NAME=zbs-iscsi-pod # 请指定 Pod 名称。

   kubectl create -f - <<EOF
   apiVersion: v1
   kind: Pod
   metadata:
     name: $POD_NAME
     namespace: $NAMESPACE
   spec:
     restartPolicy: OnFailure
     containers:
       - name: busybox
         image: busybox
         imagePullPolicy: IfNotPresent
         args:
           - df
           - -h
           - /data
         volumeMounts:
           - name: data
             mountPath: /data
     volumes:
       - name: data
         persistentVolumeClaim:
           claimName: $PVC_NAME
   EOF

   kubectl wait --for jsonpath='{.status.phase}'=Succeeded -n $NAMESPACE pod/$POD_NAME
   kubectl logs -n $NAMESPACE $POD_NAME
   ```

   示例输出：

   ```
   Filesystem                Size      Used  Available  Use%  Mounted on
   /dev/sda                  3.9G     24.0K      3.9G   0%   /data
   ```

---

## 管理持久卷 > 克隆持久卷

# 克隆持久卷

Kubernetes 支持通过持久卷申领克隆现有持久卷，从而快速创建一个与源卷相同的新卷。

1. 请设置以下参数和值并导出为环境变量，以便后续命令调用。

   ```
   export NAMESPACE=default
   export SOURCE_SC_NAME=zbs-iscsi-sc
   export SOURCE_PVC_NAME=zbs-iscsi-pvc
   export SOURCE_VOLUME_CAPACITY=2Gi
   export CLONE_PVC_NAME=zbs-iscsi-pvc-clone
   ```

   参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `NAMESPACE` | 指定源持久卷申领所在的名字空间。源持久卷申领和克隆持久卷申领必须位于同一名字空间。 | `default` |
   | `SOURCE_SC_NAME` | 指定源存储卷使用的存储类名称。 | `zbs-iscsi-sc` |
   | `SOURCE_PVC_NAME` | 指定源持久卷申领的名称。 | `zbs-iscsi-pvc` |
   | `SOURCE_VOLUME_CAPACITY` | 指定源持久卷的容量大小。克隆持久卷的容量需和源持久卷的容量相同。 | `2Gi` |
   | `CLONE_PVC_NAME` | 指定克隆的持久卷申领的名称，可自定义。 | `zbs-iscsi-pvc-clone` |
2. 创建克隆持久卷申领。通过 datasource 字段引用源持久卷申领的名称，Kubernetes 将识别该请求为卷克隆操作，并对持久卷进行克隆。

   ```
   kubectl create -f - <<EOF
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: $CLONE_PVC_NAME
     namespace: $NAMESPACE
   spec:
     storageClassName: $SOURCE_SC_NAME
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: $SOURCE_VOLUME_CAPACITY
     dataSource:
       kind: PersistentVolumeClaim
       name: $SOURCE_PVC_NAME
   EOF
   ```
3. 等待持久卷申领和持久卷绑定。持久卷申领与持久卷需绑定后才能被 Pod 使用。

   ```
   kubectl wait --for jsonpath='{.status.phase}'=Bound -n $NAMESPACE pvc/$CLONE_PVC_NAME
   ```
4. （可选）创建一个临时 Pod 并挂载持久卷申领，验证持久卷的可用性以及容量是否符合预期。若 Pod 无法正常挂载持久卷申领，请联系 SmartX 售后工程师处理。

   ```
   export POD_NAME=zbs-iscsi-pod # 请指定 Pod 名称。

   kubectl create -f - <<EOF
   apiVersion: v1
   kind: Pod
   metadata:
     name: $POD_NAME
     namespace: $NAMESPACE
   spec:
     restartPolicy: OnFailure
     containers:
       - name: busybox
         image: busybox
         imagePullPolicy: IfNotPresent
         args:
           - df
           - -h
           - /data
         volumeMounts:
           - name: data
             mountPath: /data
     volumes:
       - name: data
         persistentVolumeClaim:
           claimName: $CLONE_PVC_NAME
   EOF

   kubectl wait --for jsonpath='{.status.phase}'=Succeeded -n $NAMESPACE pod/$POD_NAME
   kubectl logs -n $NAMESPACE $POD_NAME
   ```

   示例输出：

   ```
   Filesystem                Size      Used  Available  Use%  Mounted on
   /dev/sda                  1.9G     24.0K      1.9G   0%   /data
   ```

---

## 管理卷快照

# 管理卷快照

卷快照是持久卷在某一时间点的副本，用于记录某一时刻持久卷的数据状态，可用于数据保护、备份、恢复和测试等场景。

卷快照的管理涉及以下几个核心对象：

- **卷快照**（VolumeSnapshot）：用户发起的快照请求对象，用于描述对持久卷关联的持久卷申领的快照请求。
- **卷快照类**（VolumeSnapshotClass）：定义使用哪个 CSI 驱动创建快照以及对卷快照内容采用何种保留策略等。
- **卷快照内容**（VolumeSnapshotContent）：底层存储中实际的快照实体。

---

## 管理卷快照 > 创建卷快照

# 创建卷快照

1. 请设置以下参数和值并导出为环境变量，以便后续命令调用。

   ```
   export DRIVER_NAME=iscsi.zbs.csi.smartx.com
   export NAMESPACE=default
   export PVC_NAME=zbs-iscsi-pvc
   export VSCLASS_NAME=zbs-iscsi-vsclass
   export VS_NAME=zbs-iscsi-vs
   ```

   参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `DRIVER_NAME` | 指定使用的 CSI 驱动名称。本驱动默认值为 `iscsi.zbs.csi.smartx.com`。若本版本由从 3.0.0 以下版本升级而来，请修改为 `com.smartx.csi-driver`。 | `iscsi.zbs.csi.smartx.com` |
   | `NAMESPACE` | 指定快照对象所属的名字空间，请与源持久卷申领所在的名字空间保持一致。 | `default` |
   | `PVC_NAME` | 指定要创建快照的源持久卷申领的名称。 | `zbs-iscsi-pvc` |
   | `VSCLASS_NAME` | 指定用于创建卷快照的卷快照类名称。 | `zbs-iscsi-vsclass` |
   | `VS_NAME` | 指定新建卷快照的名称。 | `zbs-iscsi-vs` |
2. 执行以下命令创建卷快照类。若已有卷快照类，可跳过这一步。

   ```
   kubectl create -f - <<EOF
   apiVersion: snapshot.storage.k8s.io/v1
   kind: VolumeSnapshotClass
   metadata:
     name: $VSCLASS_NAME
   driver: $DRIVER_NAME
   deletionPolicy: Delete
   EOF
   ```

   主要参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `driver` | 指定使用的 CSI 驱动名称。本驱动默认值为 `iscsi.zbs.csi.smartx.com`。若本版本由从 3.0.0 以下版本升级而来，请修改为 `com.smartx.csi-driver`。 | `iscsi.zbs.csi.smartx.com` |
   | `deletionPolicy` | 定义删除卷快照对象时，其对应的 VolumeSnapshotContent 使用的保留策略。默认为 Delete。  - **Retain**：删除 VolumeSnapshot 时保留 VolumeSnapshotContent。 - **Delete**：删除 VolumeSnapshot 时同时删除 VolumeSnapshotContent。 | `Delete` |
3. 执行以下命令创建卷快照对象。

   ```
   kubectl create -f - <<EOF
   apiVersion: snapshot.storage.k8s.io/v1
   kind: VolumeSnapshot
   metadata:
     name: $VS_NAME
     namespace: $NAMESPACE
   spec:
     volumeSnapshotClassName: $VSCLASS_NAME
     source:
       persistentVolumeClaimName: $PVC_NAME
   EOF
   ```

   主要参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `volumeSnapshotClassName` | 指定创建快照所用的卷快照类。 | `$VSCLASS_NAME` |
   | `persistentVolumeClaimName` | 指定卷快照的源持久卷申领。 | `$PVC_NAME` |
4. 等待卷快照可供使用。

   ```
   kubectl wait --for jsonpath='{.status.readyToUse}'=true -n $NAMESPACE vs/$VS_NAME
   ```

---

## 管理卷快照 > 导入卷快照

# 导入卷快照

若 SMTX ZBS 块存储集群已有 iSCSI LUN 快照，可通过手动创建卷快照内容（VolumeSnapshotContent）和卷快照对象（VolumeSnapshot） 实现卷快照的导入。

1. 登录 SMTX ZBS 块存储集群任一节点，执行如下命令，查看要导入的 iSCSI LUN 快照的 UUID。

   ```
   zbs-iscsi snapshot list <target_name> [--lun_id <LUN_ID>]
   ```

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `target_name` | iSCSI LUN 所属的 Target 名称。 | `-` |
   | `LUN_ID` | 快照所属的 iSCSI LUN 的 ID。 | `-` |
2. 请设置以下参数和值并导出为环境变量，以便后续命令调用。

   ```
   export DRIVER_NAME=iscsi.zbs.csi.smartx.com
   export SNAPSHOT_UUID=a314701b-953b-4d6e-85ad-05853b851041
   export NAMESPACE=default
   export VSC_NAME=zbs-iscsi-vsc-import
   export VS_NAME=zbs-iscsi-vs-import
   ```

   参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `DRIVER_NAME` | 指定使用的 CSI 驱动名称。本驱动默认值为 `iscsi.zbs.csi.smartx.com`。若本版本由从 3.0.0 以下版本升级而来，请修改为 `com.smartx.csi-driver`。 | `iscsi.zbs.csi.smartx.com` |
   | `SNAPSHOT_UUID` | 指定需要导入 `SMTX ZBS iSCSI LUN` 快照的 UUID。 | `a314701b-953b-4d6e-85ad-05853b851041` |
   | `NAMESPACE` | 指定卷快照所属的名字空间。 | `default` |
   | `VSC_NAME` | 指定新建卷快照内容的名称，可自定义。 | `zbs-iscsi-vsc-import` |
   | `VS_NAME` | 指定新建卷快照的名称，可自定义。 | `zbs-iscsi-vs` |
3. 创建卷快照内容。

   ```
   kubectl create -f - <<EOF
   apiVersion: snapshot.storage.k8s.io/v1
   kind: VolumeSnapshotContent
   metadata:
     name: $VSC_NAME
   spec:
     deletionPolicy: Retain
     driver: $DRIVER_NAME
     source:
       snapshotHandle: $SNAPSHOT_UUID
     sourceVolumeMode: Filesystem
     volumeSnapshotRef:
       name: $VS_NAME
       namespace: $NAMESPACE
   EOF
   ```

   参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `deletionPolicy` | 指定在删除卷快照对象时，其对应的 VolumeSnapshotContent 使用的保留策略。默认为 Delete。  - **Retain**：删除 VolumeSnapshot 时保留 VolumeSnapshotContent。 - **Delete**：删除 VolumeSnapshot 时同时删除 VolumeSnapshotContent。 | `Retain` |
   | `sourceVolumeMode` | 持久卷类型，请保持与源卷类型相同。 | `Filesystem` |
4. 创建卷快照对象。

   ```
   kubectl create -f - <<EOF
   apiVersion: snapshot.storage.k8s.io/v1
   kind: VolumeSnapshot
   metadata:
     name: $VS_NAME
     namespace: $NAMESPACE
   spec:
     source:
       volumeSnapshotContentName: $VSC_NAME
   EOF
   ```
5. 等待卷快照可供使用。

   ```
   kubectl wait --for jsonpath='{.status.readyToUse}'=true -n $NAMESPACE vs/$VS_NAME
   ```

---

## 管理卷快照 > 从快照恢复卷

# 从快照恢复卷

通过快照恢复卷（即通过卷快照对象创建新的持久卷申领），可以基于某个历史时间点的快照数据，重新创建出一个独立的持久卷。

从快照恢复的卷与源卷在创建快照时的状态一致，可用于故障恢复等场景。

1. 在执行操作前，请设置以下参数和值并导出为环境变量，以便后续命令调用。

   ```
   export DRIVER_NAME=iscsi.zbs.csi.smartx.com
   export NAMESPACE=default
   export VS_NAME=zbs-iscsi-vs
   export SC_NAME=zbs-iscsi-sc
   export PVC_NAME=zbs-iscsi-pvc-restore
   export VOLUME_CAPACITY=2Gi
   ```

   参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `DRIVER_NAME` | 指定使用的 CSI 驱动名称。本驱动默认值为 `iscsi.zbs.csi.smartx.com`。若本版本由从 3.0.0 以下版本升级而来，请修改为 `com.smartx.csi-driver`。 | `iscsi.zbs.csi.smartx.com` |
   | `NAMESPACE` | 指定名字空间，请保持和源持久卷申领的所在的名字空间相同。 | `default` |
   | `VS_NAME` | 指定新建卷快照的名称。 | `zbs-iscsi-vs` |
   | `SC_NAME` | 指定恢复持久卷申领所使用的存储类的名称，可自定义。 | `zbs-iscsi-sc` |
   | `PVC_NAME` | 指定恢复后新建持久卷申领的名称，可自定义。 | `zbs-iscsi-pvc-restore` |
   | `VOLUME_CAPACITY` | 指定恢复卷的容量，请保持和源卷一致。 | `2Gi` |
2. 创建存储类。如果使用已存在的存储类，可跳过此步骤。

   ```
   kubectl create -f - <<EOF
   apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: $SC_NAME
   provisioner: $DRIVER_NAME
   allowVolumeExpansion: true
   EOF
   ```

   主要参数说明：

   | 参数 | 说明 | 示例 |
   | --- | --- | --- |
   | `provisioner` | 置备持久卷的 CSI 驱动名称（即本驱动）。 | `$DRIVER_NAME` |
   | `allowVolumeExpansion` | 是否允许对恢复后的持久卷进行扩容。  - `true`：可对持久卷扩容 - `false`：不允许对持久卷扩容 | `true` |
3. 创建持久卷申领。

   ```
   kubectl create -f - <<EOF
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: $PVC_NAME
     namespace: $NAMESPACE
   spec:
     storageClassName: $SC_NAME
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: $VOLUME_CAPACITY
     dataSource:
       apiGroup: snapshot.storage.k8s.io
       kind: VolumeSnapshot
       name: $VS_NAME
   EOF
   ```
4. 等待持久卷申领和持久卷绑定。

   `kubectl wait --for jsonpath='{.status.phase}'=Bound -n $NAMESPACE pvc/$PVC_NAME`
5. （可选）通过创建一个临时 Pod 挂载持久卷申领，验证持久卷的可用性以及容量是否符合预期。

   ```
   export POD_NAME=zbs-iscsi-pod # 请指定 Pod 名称。

   kubectl create -f - <<EOF
   apiVersion: v1
   kind: Pod
   metadata:
     name: $POD_NAME
     namespace: $NAMESPACE
   spec:
     restartPolicy: OnFailure
     containers:
       - name: busybox
         image: busybox
         imagePullPolicy: IfNotPresent
         args:
           - df
           - -h
           - /data
         volumeMounts:
           - name: data
             mountPath: /data
     volumes:
       - name: data
         persistentVolumeClaim:
           claimName: $PVC_NAME
   EOF

   kubectl wait --for jsonpath='{.status.phase}'=Succeeded -n $NAMESPACE pod/$POD_NAME
   kubectl logs -n $NAMESPACE $POD_NAME
   ```

   示例输出：

   ```
   Filesystem                Size      Used  Available  Use%  Mounted on
   /dev/sda                  1.9G     24.0K      1.9G   0%   /data
   ```

---

## 使用 Node Down Pod Handler 加速有状态 Pod 的跨节点恢复

# 使用 Node Down Pod Handler 加速有状态 Pod 的跨节点恢复

当 Kubernetes 节点意外宕机时，控制故障 Pod 的控制器会尝试在其他可用节点上重建 Pod。对于无状态 Pod，这一过程通常可在 6 分钟内完成。然而，对于使用持久卷的有状态 Pod，由于 Kubernetes 需要避免存储访问冲突，恢复过程可能长期停滞，甚至无法完成，导致应用持续处于降级或不可用状态。

Kubernetes 通过 kubelet 的心跳机制判断节点的就绪状态。如果节点上的 kubelet 停止报告其状态，该节点会在约 50 秒后被视为“未就绪”。随后，kube-controller-manager 会在等待 pod-eviction-timeout（默认为 5 分钟）后，开始驱逐该无响应节点上的 Pod。驱逐过程会将这些 Pod 标记为终止状态。如果这些 Pod 由 Deployment、ReplicaSet 或 StatefulSet 等控制器管理，控制器会根据副本数要求创建新的 Pod 并调度到健康节点上。

然而，当故障节点上的 Pod 挂载了访问模式为 **ReadWriteOnce** 或 **ReadWriteOncePod** 的持久卷时，Kubernetes 必须先确保故障节点上的持久卷已卸载，才能将其挂载到其他节点。但由于故障节点的 kubelet 已断开连接，实际已无法完成卸载操作，导致新节点上的 Pod 无法重新挂载该卷，从而导致 Pod 恢复失败。

为解决此问题，我们推出了可独立运行的辅助组件 Node Down Pod Handler，结合 SMTX ZBS 块存储具备的接入点控制功能，可在 Kubernetes 节点发生故障后加速有状态应用的跨节点恢复。

当 Kubernetes 检测到节点长期处于异常状态并开始驱逐 Pod 时，Node Down Pod Handler 会：

- **强制删除被驱逐的 Pod**，以触发控制器立即在健康节点上重建 Pod；
- **强制删除 Pod 关联的 VolumeAttachment**，以触发 SMTX ZBS 块存储集群执行卷接入点切换，从而强制卸载故障节点上的存储卷；

通过这一机制，Node Down Pod Handler 可显著缩短节点故障导致的有状态应用恢复时间。

Node Down Pod Handler 仅适用于以下条件均满足的 Pod：

- Pod 由控制器（如 Deployment、ReplicaSet、StatefulSet 等）管理；
- Pod 使用的持久卷访问模式为 ReadWriteOnce 或 ReadWriteOncePod；
- 持久卷所在的存储系统支持接入点切换（SMTX ZBS 的 iSCSI LUN 即具备此能力）。

对于符合上述条件的 Pod，可通过添加 k8s.smartx.com/pod-force-deletion-policy: IfNodeDown 注解，将其纳入 Node Down Pod Handler 的管理。以下以 StatefulSet 控制器举例说明：

```
apiVersion: apps/v1
kind: StatefulSet
spec:
  template:
    metadata:
      annotations:
        k8s.smartx.com/pod-force-deletion-policy: IfNodeDown
# ...
```

---

## 升级和卸载驱动 > 升级驱动

# 升级驱动

本章节介绍了如何通过在线和离线方式将低版本的 SMTX ZBS CSI 驱动升级至本版本。

> **说明**：
>
> - 仅支持 **2.5.0** 及以上版本的 SMTX ZBS CSI 驱动升级至本版本。
> - 若 SMTX ZBS CSI 驱动存在以下任一情况，则不支持升级至本版本：
>   - 已启用 NVMe-oF 协议接入 SMTX ZBS 块存储集群；
>   - 使用 iSCSI 协议接入时启用了 CHAP 认证；
>   - 已配置多集群连接功能。

---

## 升级和卸载驱动 > 升级驱动 > 在线升级

# 在线升级

在线升级适用于 Kubernetes 集群可以访问外部网络的场景。升级操作会将已安装的旧版本 CSI 驱动替换为新版本，并保留原有的配置。

**操作步骤**

1. 执行以下命令更新 SmartX chart 仓库，确保可获得最新版本的驱动程序。

   ```
   helm repo update smartx
   ```
2. 通过 helm list 查询当前已安装的驱动的名字空间和名称信息，并导出到环境变量，供后续步骤引用。

   ```
   export NAMESPACE=$(helm list -A | grep csi-driver | awk '{print $2}')
   export NAME=$(helm list -A | grep csi-driver | awk '{print $1}')
   ```

   > **注意**：
   >
   > 若集群中存在其他含 csi-driver 关键字的 Helm release，上述命令可能返回错误的名字空间和名称。请检查 `NAMESPACE` 和 `NAME` 值是否与实际安装情况一致。
3. 转换 values.yaml 文件，将旧版本驱动的配置参数迁移至新版本。

   ```
   helm get values -a -n $NAMESPACE $NAME > ./old_values.yaml
   helm show values --version v3.0.0 smartx/csi-driver-zbs-iscsi > ./values.yaml

   cat <<'EOF' > convert-values.sh
   #!/usr/bin/env bash

   if [[ $(yq '.nameOverride // ""' ./old_values.yaml) != '' ]]; then
     echo 'Error: .nameOverride in ./old_values.yaml must be empty.'
     exit 1
   fi

   if [[ $(yq '.driver.deploymentMode // "EXTERNAL"' ./old_values.yaml) != 'EXTERNAL' ]]; then
     echo 'Error: .driver.deploymentMode in ./old_values.yaml must be "EXTERNAL".'
     exit 1
   fi

   if [[ $(yq '.driver.nvmf.enable // false' ./old_values.yaml) != 'false' ]]; then
     echo 'Error: .driver.nvmf.enable in ./old_values.yaml must be "false".'
     exit 1
   fi

   if [[ $(yq '.driver.controller.driver.podDeletePolicy // "no-delete-pod"' ./old_values.yaml) != 'no-delete-pod' ]]; then
     echo 'Error: .driver.controller.driver.podDeletePolicy in ./old_values.yaml must be "no-delete-pod".'
     exit 1
   fi

   if [[ $(yq '.driver.node.driver.iscsi // {}' ./old_values.yaml) != '{}' ]]; then
     echo 'Error: .driver.node.driver.iscsi in ./old_values.yaml must be "{}".'
     exit 1
   fi

   declare -A fields=(
     ['zbsIP']='driver.metaAddr | split(":")[0]'
     ['configureHost']='prepareCSI.enabled'
     ['driverName']='driver.nameOverride | select(length != 0) // "com.smartx.csi-driver"'
     ['driverID']='driver.clusterID'
     ['nameOverride']='nameOverride'
     ['fullnameOverride']='fullnameOverride'
     ['controller.replicaCount']='driver.controller.replicas'
     ['controller.serviceAccount.create']='serviceAccount.create'
     ['controller.resources']='driver.controller.resources'
     ['controller.nodeSelector']='driver.controller.nodeSelector'
     ['controller.toleration']='driver.tolerations'
     ['controller.affinity']='driver.controller.affinity'
     ['controller.sidecars.provisioner.resources']='sidecar.resources.csi_provisioner'
     ['controller.sidecars.attacher.resources']='sidecar.resources.csi_attacher'
     ['controller.sidecars.resizer.resources']='sidecar.resources.csi_resizer'
     ['controller.sidecars.snapshotter.resources']='sidecar.resources.csi_snapshotter'
     ['controller.sidecars.livenessProbe.httpPort']='driver.controller.driver.ports.health'
     ['controller.sidecars.livenessProbe.resources']='sidecar.resources.liveness_probe'
     ['node.serviceAccount.create']='serviceAccount.create'
     ['node.resources']='driver.node.resources'
     ['node.nodeSelector']='driver.node.nodeSelector'
     ['node.tolerations']='driver.tolerations'
     ['node.affinity']='driver.node.affinity'
     ['node.kubeletDir']='driver.node.driver.kubeletRootDir'
     ['node.maxVolumes']='driver.maxVolumesPerNode'
     ['node.sidecars.nodeDriverRegistrar.resources']='sidecar.resources.driver_registrar'
     ['node.sidecars.livenessProbe.httpPort']='driver.node.driver.ports.health'
     ['node.sidecars.livenessProbe.resources']='sidecar.resources.liveness_probe'
   )

   for key in "${!fields[@]}"; do
     yq -i ".$key = (load(\"./old_values.yaml\").${fields[$key]})" ./values.yaml
   done
   EOF

   bash ./convert-values.sh
   ```
4. （可选）切换镜像仓库。本驱动默认使用 Docker Hub 上的容器镜像，若 Kubernetes 集群无法访问 Docker Hub，可选择切换至腾讯云容器镜像仓库。

   ```
   export IMAGE_NAMESPACE=ccr.ccs.tencentyun.com/smartxworks

   yq -i ".imageNamespaceOverride = \"$IMAGE_NAMESPACE\"" ./values.yaml
   ```
5. 查看并确认 values.yaml 文件配置是否正确。如有必要，可进行其他修改。

   ```
   cat ./values.yaml | less
   ```
6. 执行如下命令升级驱动，并检查升级后的组件状态是否正常。

   ```
   helm upgrade --version v3.0.0 -f ./values.yaml -n $NAMESPACE $NAME smartx/csi-driver-zbs-iscsi
   kubectl get pods -n $NAMESPACE -l app.kubernetes.io/instance=$NAME -w
   ```

   > **说明**：
   >
   > 若出现如下错误，则说明升级前检查未通过，不支持升级：
   >
   > ```
   > Error: UPGRADE FAILED: pre-upgrade hooks failed: 1 error occurred:
   >   * job csi-driver-pre-upgrade failed: BackoffLimitExceeded
   > ```
   >
   > 此时请执行如下命令回退驱动版本。若出现错误，请重复执行该命令直至回退成功：
   >
   > ```
   > helm rollback -n $NAMESPACE $NAME $(helm history -o yaml -n $NAMESPACE $NAME | yq '.[] | select(.status == "deployed") | .revision')
   > ```
7. 升级[卷快照控制器](https://github.com/kubernetes-csi/external-snapshotter)，并检查卷快照控制器的组件状态。若您的 Kubernetes 集群中的卷快照控制器并非按照本文档提供的方式安装，请跳过这一步。

   - **对于 1.20 及以上版本的 Kubernetes 集群**

     ```
     kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/groupsnapshot.storage.k8s.io_volumegroupsnapshotclasses.yaml
     kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/groupsnapshot.storage.k8s.io_volumegroupsnapshotcontents.yaml
     kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/groupsnapshot.storage.k8s.io_volumegroupsnapshots.yaml
     kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/snapshot.storage.k8s.io_volumesnapshotclasses.yaml
     kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/snapshot.storage.k8s.io_volumesnapshotcontents.yaml
     kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/snapshot.storage.k8s.io_volumesnapshots.yaml
     kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/deploy/kubernetes/snapshot-controller/rbac-snapshot-controller.yaml
     curl https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/deploy/kubernetes/snapshot-controller/setup-snapshot-controller.yaml | sed 's/v6\.3\.1/v7.0.2/g' | kubectl apply -f -
     kubectl get pods -n kube-system -l app.kubernetes.io/name=snapshot-controller -w
     ```

     > **说明：**
     >
     > 若遇到 `The Deployment "snapshot-controller" is invalid: spec.selector: Invalid value: {"matchLabels":{"app":"snapshot-controller","app.kubernetes.io/name":"snapshot-controller"}}: field is immutable` 报错，请执行 `kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/deploy/kubernetes/snapshot-controller/setup-snapshot-controller.yaml` 命令，删除旧版本的卷快照控制器后再重试上述步骤。
   - **对于低于 1.20 版本的 Kubernetes 集群**

     ```
     kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/client/config/crd/snapshot.storage.k8s.io_volumesnapshotclasses.yaml
     kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/client/config/crd/snapshot.storage.k8s.io_volumesnapshotcontents.yaml
     kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/client/config/crd/snapshot.storage.k8s.io_volumesnapshots.yaml
     kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/deploy/kubernetes/snapshot-controller/rbac-snapshot-controller.yaml
     kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/deploy/kubernetes/snapshot-controller/setup-snapshot-controller.yaml
     kubectl get pods -n default -l app=snapshot-controller -w
     ```
8. （可选）升级 Node Down Pod Handler。若 Kubernetes 集群未安装 Node Down Pod Handler，请跳过这一步并建议安装 Node Down Pod Handler。

   1. 通过 helm list 查询当前已安装 Node Down Pod Handler 的名字空间和名称信息，并导出到环境变量，供后续步骤引用。

      ```
      export NODE_DOWN_POD_HANDLER_NAMESPACE=$(helm list -A | grep node-down-pod-handler | awk '{print $2}')
      export NODE_DOWN_POD_HANDLER_NAME=$(helm list -A | grep node-down-pod-handler | awk '{print $1}')
      ```

      > **注意**：
      >
      > 若集群中存在其他含 node-down-pod-handler 关键字的 Helm release，上述命令可能返回错误的名字空间和名称。请检查 `NODE_DOWN_POD_HANDLER_NAMESPACE` 和 `NODE_DOWN_POD_HANDLER_NAME` 值是否与实际安装情况一致。
   2. 转换 values.yaml 文件，将旧版本驱动的配置参数迁移至新版本。

      ```
      helm get values -a -n $NODE_DOWN_POD_HANDLER_NAMESPACE $NODE_DOWN_POD_HANDLER_NAME > ./node-down-pod-handler-old_values.yaml
      helm show values --version v1.0.0 smartx/node-down-pod-handler > ./node-down-pod-handler-new_values.yaml
      yq eval-all '. as $item ireduce ({}; . * $item)' ./node-down-pod-handler-new_values.yaml ./node-down-pod-handler-old_values.yaml > ./node-down-pod-handler-values.yaml
      ```
   3. （可选）Node Down Pod Handler 默认使用 Docker Hub 上的容器镜像。若 Kubernetes 集群无法访问 Docker Hub，可以选择切换到腾讯云容器镜像仓库。

      ```
      export NODE_DOWN_POD_HANDLER_IMAGE_NAMESPACE=ccr.ccs.tencentyun.com/smartxworks

      yq -i ".image.repository = \"$NODE_DOWN_POD_HANDLER_IMAGE_NAMESPACE/node-down-pod-handler\"" ./node-down-pod-handler-values.yaml
      ```
   4. 查看修改后的 values.yaml 文件。如有必要，可进行其他修改。

      ```
      cat ./node-down-pod-handler-values.yaml | less
      ```
   5. 升级 Node Down Pod Handler，并检查组件状态。若各组件状态为 Running，说明运行正常。

      ```
      helm upgrade --version v1.0.0 -f ./node-down-pod-handler-values.yaml -n $NODE_DOWN_POD_HANDLER_NAMESPACE $NODE_DOWN_POD_HANDLER_NAME smartx/node-down-pod-handler
      kubectl get pods -n $NODE_DOWN_POD_HANDLER_NAMESPACE -l app.kubernetes.io/instance=$NODE_DOWN_POD_HANDLER_NAME -w
      ```

---

## 升级和卸载驱动 > 升级驱动 > 离线升级

# 离线升级

离线升级适用于 Kubernetes 集群无法访问外部网络的场景。操作逻辑与在线升级类似，只是需要依赖在线安装包提供的 Helm charts、容器镜像和工具。

**前提条件**

- 已下载并解压离线本版本驱动的安装包（包含 Helm charts、容器镜像和必要工具）。
- 已配置可被 Kubernetes 集群访问的私有容器镜像仓库。

**操作步骤**

下列命令均需在离线安装包目录内执行。

1. 通过 helm list 查询当前已安装驱动的名字空间和名称信息，并导出到环境变量，供后续步骤引用。

   ```
   export NAMESPACE=$(./bin/linux-$(uname -m)/helm list -A | grep csi-driver | awk '{print $2}')
   export NAME=$(./bin/linux-$(uname -m)/helm list -A | grep csi-driver | awk '{print $1}')
   ```

   > **注意**：
   >
   > 若集群中存在其他含 csi-driver 关键字的 Helm release，上述命令可能返回错误的名字空间和名称。请检查 `NAMESPACE` 和 `NAME` 值与实际安装情况一致。
2. 转换 values.yaml 文件，将旧版本驱动的配置参数迁移至新版本。

   ```
   ./bin/linux-$(uname -m)/helm get values -a -n $NAMESPACE $NAME > ./old_values.yaml
   ./bin/linux-$(uname -m)/helm show values ./charts/csi-driver-zbs-iscsi-v3.0.0.tgz > ./values.yaml
   ./scripts/convert-values.sh
   ```
3. 将容器镜像推送至私有仓库，并指定相应的容器镜像拉取地址。

   ```
   export IMAGE_NAMESPACE=ccr.ccs.tencentyun.com/smartxworks # 请替换为实际私有仓库，此处以 ccr.ccs.tencentyun.com/smartxworks 为例。

   for file in images/*; do
     ./bin/linux-$(uname -m)/crane push --index $file $IMAGE_NAMESPACE/${file##*/}
   done
   ./bin/linux-$(uname -m)/yq -i ".imageNamespaceOverride = \"$IMAGE_NAMESPACE\"" ./values.yaml
   ```

   > **注意**：
   >
   > 若执行上述命令出现 `UNAUTHORIZED` 报错，请执行 `./bin/linux-$(uname -m)/crane auth login` 命令登录私有镜像仓库并再次尝试。
4. 查看并确认 values.yaml 文件配置是否正确。如有必要，可进行其他修改。

   ```
   cat ./values.yaml | less
   ```
5. 执行如下命令升级驱动，并检查升级后的组件状态是否正常。

   ```
   ./bin/linux-$(uname -m)/helm upgrade -f ./values.yaml -n $NAMESPACE $NAME ./charts/csi-driver-zbs-iscsi-v3.0.0.tgz
   ./bin/linux-$(uname -m)/kubectl get pods -n $NAMESPACE -l app.kubernetes.io/instance=$NAME -w
   ```

   > **说明**：
   >
   > 若出现如下错误，则说明升级前检查未通过，不支持升级：
   >
   > ```
   > Error: UPGRADE FAILED: pre-upgrade hooks failed: 1 error occurred:
   >   * job csi-driver-pre-upgrade failed: BackoffLimitExceeded
   > ```
   >
   > 此时请执行如下命令回退驱动版本。若出现错误，请重复执行该命令直至回退成功：
   >
   > ```
   > ./bin/linux-$(uname -m)/helm rollback -n $NAMESPACE $NAME $(./bin/linux-$(uname -m)/helm history -o yaml -n $NAMESPACE $NAME | ./bin/linux-$(uname -m)/yq '.[] | select(.status == "deployed") | .revision')
   > ```
6. 升级[卷快照控制器](https://github.com/kubernetes-csi/external-snapshotter)，并检查卷快照控制器的组件状态。若您的 Kubernetes 集群中的卷快照控制器并非按照本文档提供的方式安装，请跳过这一步。

   - **对于 1.20 及以上版本的 Kubernetes 集群**

     ```
     export SNAPSHOT_CONTROLLER_IMAGE_NAMESPACE=ccr.ccs.tencentyun.com/smartxworks # 指定私有容器镜像仓库，此处以 ccr.ccs.tencentyun.com/smartxworks 为例。
     export SNAPSHOT_CONTROLLER_NAMESPACE=kube-system                              # 指定用于安装卷快照控制器的名字空间，此处以 kube-system 为例。

     ./bin/linux-$(uname -m)/yq -i "(.images.[] | select(.name == \"registry.k8s.io/sig-storage/snapshot-controller\").newName) = \"$SNAPSHOT_CONTROLLER_IMAGE_NAMESPACE/snapshot-controller\"" ./manifests/snapshot-controller-v7.0.2/kustomization.yaml
     ./bin/linux-$(uname -m)/yq -i ".namespace = \"$SNAPSHOT_CONTROLLER_NAMESPACE\"" ./manifests/snapshot-controller-v7.0.2/kustomization.yaml
     ./bin/linux-$(uname -m)/kubectl apply -k ./manifests/snapshot-controller-v7.0.2/
     ./bin/linux-$(uname -m)/kubectl get pods -n $SNAPSHOT_CONTROLLER_NAMESPACE -l app.kubernetes.io/name=snapshot-controller -w
     ```

     > **说明**：
     >
     > 若遇到 `The Deployment "snapshot-controller" is invalid: spec.selector: Invalid value: {"matchLabels":{"app":"snapshot-controller","app.kubernetes.io/name":"snapshot-controller"}}: field is immutable` 报错，请执行 `./bin/linux-$(uname -m)/kubectl delete -f ./manifests/snapshot-controller-v7.0.2/setup-snapshot-controller.yaml` 命令，删除旧版本的卷快照控制器后再重试上述步骤。
   - **对于低于 1.20 版本的 Kubernetes 集群**

     ```
     export SNAPSHOT_CONTROLLER_IMAGE_NAMESPACE=ccr.ccs.tencentyun.com/smartxworks # 指定私有容器镜像仓库，此处以 ccr.ccs.tencentyun.com/smartxworks 为例。
     export SNAPSHOT_CONTROLLER_NAMESPACE=kube-system                              # 指定用于安装卷快照控制器的名字空间，此处以 kube-system 为例。

     ./bin/linux-$(uname -m)/yq -i "(.images.[] | select(.name == \"k8s.gcr.io/sig-storage/snapshot-controller\").newName) = \"$SNAPSHOT_CONTROLLER_IMAGE_NAMESPACE/snapshot-controller\"" ./manifests/snapshot-controller-v3.0.3/kustomization.yaml
     ./bin/linux-$(uname -m)/yq -i ".namespace = \"$SNAPSHOT_CONTROLLER_NAMESPACE\"" ./manifests/snapshot-controller-v3.0.3/kustomization.yaml
     ./bin/linux-$(uname -m)/kubectl apply -k ./manifests/snapshot-controller-v3.0.3/
     ./bin/linux-$(uname -m)/kubectl get pods -n $SNAPSHOT_CONTROLLER_NAMESPACE -l app=snapshot-controller -w
     ```
7. （可选）升级 Node Down Pod Handler。若 Kubernetes 集群未安装 Node Down Pod Handler，请跳过这一步并建议安装 Node Down Pod Handler。

   1. 通过 helm list 查询当前已安装 Node Down Pod Handler 的名字空间和名称信息，并导出到环境变量，供后续步骤引用。

      ```
      export NODE_DOWN_POD_HANDLER_NAMESPACE=$(./bin/linux-$(uname -m)/helm list -A | grep node-down-pod-handler | awk '{print $2}')
      export NODE_DOWN_POD_HANDLER_NAME=$(./bin/linux-$(uname -m)/helm list -A | grep node-down-pod-handler | awk '{print $1}')
      ```

      > **注意**：
      >
      > 若集群中存在其他含 node-down-pod-handler 关键字的 Helm release，上述命令可能返回错误的名字空间和名称。请检查 `NODE_DOWN_POD_HANDLER_NAMESPACE 和 NODE_DOWN_POD_HANDLER_NAME` 值是否与实际安装情况一致。
   2. 转换 values.yaml 文件，将旧版本驱动的配置参数迁移至新版本。

      ```
      ./bin/linux-$(uname -m)/helm get values -a -n $NODE_DOWN_POD_HANDLER_NAMESPACE $NODE_DOWN_POD_HANDLER_NAME > ./node-down-pod-handler-old_values.yaml
      ./bin/linux-$(uname -m)/helm show values ./charts/node-down-pod-handler-v1.0.0.tgz > ./node-down-pod-handler-new_values.yaml
      ./bin/linux-$(uname -m)/yq eval-all '. as $item ireduce ({}; . * $item)' ./node-down-pod-handler-new_values.yaml ./node-down-pod-handler-old_values.yaml > ./node-down-pod-handler-values.yaml
      ```
   3. 指定容器镜像拉取地址。

      ```
      export NODE_DOWN_POD_HANDLER_IMAGE_NAMESPACE=ccr.ccs.tencentyun.com/smartxworks # 指定私有容器镜像仓库，此处以 ccr.ccs.tencentyun.com/smartxworks 为例。

      ./bin/linux-$(uname -m)/yq -i ".image.repository = \"$NODE_DOWN_POD_HANDLER_IMAGE_NAMESPACE/node-down-pod-handler\"" ./node-down-pod-handler-values.yaml
      ```
   4. 查看修改后的 values.yaml 文件。如有必要，可进行其他修改。

      ```
      cat ./node-down-pod-handler-values.yaml | less
      ```
   5. 升级 Node Down Pod Handler，并检查组件状态。若各组件状态为 Running，说明运行正常。

      ```
      ./bin/linux-$(uname -m)/helm upgrade -f ./node-down-pod-handler-values.yaml -n $NODE_DOWN_POD_HANDLER_NAMESPACE $NODE_DOWN_POD_HANDLER_NAME ./charts/node-down-pod-handler-v1.0.0.tgz
      ./bin/linux-$(uname -m)/kubectl get pods -n $NODE_DOWN_POD_HANDLER_NAMESPACE -l app.kubernetes.io/instance=$NODE_DOWN_POD_HANDLER_NAME -w
      ```

---

## 升级和卸载驱动 > 卸载驱动

# 卸载驱动

您可以通过在线或离线的方式卸载驱动。

> **注意**：
>
> 卸载本驱动后，通过本驱动创建的持久卷将无法正常使用。因此，请在卸载前确保 Kubernetes 集群中已无持久卷。

---

## 升级和卸载驱动 > 卸载驱动 > 在线卸载

# 在线卸载

若您的 SMTX ZBS iSCSI CSI 驱动是通过在线方式安装，请通过在线方式卸载。

**操作步骤**

1. 通过 helm list 查询当前已安装的驱动的名字空间和名称信息，并导出到环境变量，供后续步骤引用。

   ```
   export NAMESPACE=$(helm list -A | grep csi-driver | awk '{print $2}')
   export NAME=$(helm list -A | grep csi-driver | awk '{print $1}')
   ```

   > **注意**：
   >
   > 若集群中存在其他含 csi-driver 关键字的 Helm release，上述命令可能返回错误的名字空间和名称。请检查 `NAMESPACE` 和 `NAME` 值与实际安装情况一致。
2. 执行如下命令卸载本驱动程序。

   ```
   helm uninstall -n $NAMESPACE $NAME
   ```
3. 卸载卷快照控制器。若您的 Kubernetes 集群中的卷快照控制器并非按照本文档提供的方式安装，请跳过这一步。

   - **对于 1.20 及以上版本的 Kubernetes 集群**

     ```
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/groupsnapshot.storage.k8s.io_volumegroupsnapshotclasses.yaml
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/groupsnapshot.storage.k8s.io_volumegroupsnapshotcontents.yaml
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/groupsnapshot.storage.k8s.io_volumegroupsnapshots.yaml
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/snapshot.storage.k8s.io_volumesnapshotclasses.yaml
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/snapshot.storage.k8s.io_volumesnapshotcontents.yaml
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/client/config/crd/snapshot.storage.k8s.io_volumesnapshots.yaml
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/deploy/kubernetes/snapshot-controller/rbac-snapshot-controller.yaml
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v7.0.2/deploy/kubernetes/snapshot-controller/setup-snapshot-controller.yaml
     ```
   - **对于低于 1.20 版本的 Kubernetes 集群**

     ```
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/client/config/crd/snapshot.storage.k8s.io_volumesnapshotclasses.yaml
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/client/config/crd/snapshot.storage.k8s.io_volumesnapshotcontents.yaml
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/client/config/crd/snapshot.storage.k8s.io_volumesnapshots.yaml
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/deploy/kubernetes/snapshot-controller/rbac-snapshot-controller.yaml
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/refs/tags/v3.0.3/deploy/kubernetes/snapshot-controller/setup-snapshot-controller.yaml
     ```
4. （可选）卸载 Node Down Pod Handler。

   1. 通过 helm list 查询当前已安装 Node Down Pod Handler 的名字空间和名称信息，并导出到环境变量，供后续步骤引用。

      ```
      export NODE_DOWN_POD_HANDLER_NAMESPACE=$(helm list -A | grep node-down-pod-handler | awk '{print $2}')
      export NODE_DOWN_POD_HANDLER_NAME=$(helm list -A | grep node-down-pod-handler | awk '{print $1}')
      ```

      > **注意**：
      >
      > 若集群中存在其他含 node-down-pod-handler 关键字的 Helm release，上述命令可能返回错误的名字空间和名称。请检查 `NODE_DOWN_POD_HANDLER_NAMESPACE` 和 `NODE_DOWN_POD_HANDLER_NAME` 值是否与实际安装情况一致。
   2. 卸载 Node Down Pod Handler。

      ```
      helm uninstall -n $NODE_DOWN_POD_HANDLER_NAMESPACE $NODE_DOWN_POD_HANDLER_NAME
      ```

---

## 升级和卸载驱动 > 卸载驱动 > 离线卸载

# 离线卸载

若您的 SMTX ZBS iSCSI CSI 驱动是通过离线方式安装，请通过离线方式卸载。

**操作步骤**

以下命令均需在离线安装包目录内执行。

1. 通过 helm list 查询当前已安装的驱动的名字空间和名称信息，并导出到环境变量，供后续步骤引用。

   ```
   export NAMESPACE=$(./bin/linux-$(uname -m)/helm list -A | grep csi-driver | awk '{print $2}')
   export NAME=$(./bin/linux-$(uname -m)/helm list -A | grep csi-driver | awk '{print $1}')
   ```
2. 执行如下命令卸载本驱动程序。

   ```
   ./bin/linux-$(uname -m)/helm uninstall -n $NAMESPACE $NAME
   ```
3. 卸载卷快照控制器。若您的 Kubernetes 集群中的卷快照控制器并非按照本文档提供的方式安装，请跳过这一步。

- **对于 1.20 及以上版本的 Kubernetes 集群**

  ```
  export SNAPSHOT_CONTROLLER_NAMESPACE=kube-system # 指定安装卷快照控制器的名字空间，此处以 kube-system 为例。

  ./bin/linux-$(uname -m)/yq -i ".namespace = \"$SNAPSHOT_CONTROLLER_NAMESPACE\"" ./manifests/snapshot-controller-v7.0.2/kustomization.yaml
  ./bin/linux-$(uname -m)/kubectl delete -k ./manifests/snapshot-controller-v7.0.2/
  ```
- **对于低于 1.20 版本的 Kubernetes 集群**

  ```
  export SNAPSHOT_CONTROLLER_NAMESPACE=kube-system # 指定安装卷快照控制器的名字空间，此处以 kube-system 为例。

  ./bin/linux-$(uname -m)/yq -i ".namespace = \"$SNAPSHOT_CONTROLLER_NAMESPACE\"" ./manifests/snapshot-controller-v3.0.3/kustomization.yaml
  ./bin/linux-$(uname -m)/kubectl delete -k ./manifests/snapshot-controller-v3.0.3/
  ```

4. （可选）卸载 Node Down Pod Handler。

   1. 通过 helm list 查询当前已安装 Node Down Pod Handler 的名字空间和名称信息，并导出到环境变量，供后续步骤引用。

      ```
      export NODE_DOWN_POD_HANDLER_NAMESPACE=$(./bin/linux-$(uname -m)/helm list -A | grep node-down-pod-handler | awk '{print $2}')
      export NODE_DOWN_POD_HANDLER_NAME=$(./bin/linux-$(uname -m)/helm list -A | grep node-down-pod-handler | awk '{print $1}')
      ```

      > **注意**：
      >
      > 若集群中存在其他含 node-down-pod-handler 关键字的 Helm release，上述命令可能返回错误的名字空间和名称。请检查 `NODE_DOWN_POD_HANDLER_NAMESPACE` 和 `NODE_DOWN_POD_HANDLER_NAME` 值是否与实际安装情况一致。
   2. 卸载 Node Down Pod Handler。

      ```
      helm uninstall -n $NODE_DOWN_POD_HANDLER_NAMESPACE $NODE_DOWN_POD_HANDLER_NAME
      ```

---

## 附录 > API 参考

# API 参考

| 卷参数 | 取值 | 描述 |
| --- | --- | --- |
| `csi.storage.k8s.io/fstype` | `xfs` 或 `ext4`（默认 ext4） | 设置卷的文件系统类型，区分大小写。 |
| `replication.n` | `2` 或 `3`，默认为 SMTX ZBS 块存储集群的 iSCSI LUN 的副本数 | 当卷使用副本模式作为冗余策略时，通过此参数设置卷的副本数，用于保证数据的高可用性。  **注意**：   - 该参数与 erasureCoding.k、erasureCoding.m 互斥，不能同时配置。 - 卷创建后仅允许提升副本数，不允许降低。 |
| `erasureCoding.k` | - `erasureCoding.m` 取值为 1 或 2 时，erasureCoding.k 可设置为 [2, 22] 内的偶数 - `erasureCoding.m` 取值为 3 或 4 时，`erasureCoding.k` 可设置为 [4, 8] 内的偶数 | 当卷使用纠删码模式作为冗余策略时，通过此参数纠删码的数据分片数。  **注意**：   - 此参数必须和 `erasureCoding.m` 同时配置。 - 此参数不能和 `replication.n` 同时配置。 - 此参数仅允许在创建持久卷时设置，创建后不允许修改。 |
| `erasureCoding.m` | [1, 4] 内的整数 | 当卷使用纠删码模式作为冗余策略时，通过此参数设置纠删码的冗余分片数。  **注意**：   - 此参数必须和 `erasureCoding.k` 同时配置。 - 此参数不能和 `replication.n` 同时配置。 - 此参数仅允许在创建持久卷时设置，创建后不允许修改。 |
| `thinProvisioning` | `true` 或 `false`，默认为 `true`   - `true`：启用精简置备。 - `false`：不启用精简置备（即厚置备）。 | 持久卷是否启用精简置备。 |
| `encryptionAlgorithm` | `None` 或 `AES-256`，默认为 `None`，即不加密。 | 设置卷的加密算法。此参数区分大小写。 |
| `tieringPolicy` | `Auto` 或 `None`，默认为 `Auto`。   - `Auto`：自动分层。卷数据将根据访问情况动态分布于性能层和容量层。 - `None`：不分层。卷数据将全部分布于性能层。 | 设置卷的分层策略。此参数区分大小写，且支持修改。  新建持久卷默认采用分层模式。即较高访问频率的数据将停留在速度更快的性能层，而访问频率较低的数据将下沉至速度相对较慢但容量较大的容量层。您也可以指定分层策略为 `None`，将卷数据始终保留在性能层，从而获得更稳定的高性能。 |
| `throughput` | 不小于 10Mi 的整数，未指定或 0 表示不限制 | 设置卷的最大吞吐量（每秒 MB）。支持在卷创建后修改。 |
| `iops` | 不小于 50 的整数，未指定或 0 表示不限制 | 设置卷的最大 IOPS（每秒 I/O 请求数）。支持在卷创建后修改。 |

---

## 附录 > 术语表

# 术语表

持久卷（Persistent Volume，PV）
:   持久卷是 Kubernetes 集群中可供 Pod 挂载使用，但独立于 Pod 的存储资源。持久卷可以由管理员静态置备，或通过存储类动态置备。在存储节点中创建持久卷后，计算节点上的 Pod 即可通过持久卷申领使用该存储，实现计算与存储的分离。

存储类（StorageClass）
:   存储类是 Kubernetes 用于定义如何为持久卷申领动态创建持久卷的模板，可定义置备持久卷的CIS 驱动、卷属性以及回收策略等。

持久卷申领（Persistent Volume Claim ，PVC）
:   持久卷申领在 Kubernetes 中用来声明对存储的需求（如容量、访问模式等）。Kubernetes 会将持久卷申领与符合条件的持久卷进行绑定。 Pod 挂载 PVC 后，Kubernetes 会将与 PVC 绑定的持久卷挂载给 Pod 使用。

持久卷申领注解（PVC Annotation）
:   持久卷申领注解是通过在持久卷申领中添加特定的注解来扩展，来允许 CSI 驱动传递额外指令，从而动态调整持久卷的属性。

名字空间（Namespace）
:   Kubernetes 中的一种逻辑隔离机制，用于将资源（Pod、PVC 等）按组分隔，以区分不同业务、环境或租户的资源。

卷快照（VolumeSnapshot）
:   卷快照是某个 PVC 的时间点副本，用于记录卷在特定时间的完整数据状态。卷快照对象用于描述快照请求，但并不直接存储数据。创建快照时，系统会在底层存储中生成对应的卷快照内容。

卷快照类（VolumeSnapshotClass）
:   卷快照类定义卷快照的类别和行为，包括使用的 CSI 驱动、删除策略（deletionPolicy）等。用户在创建 VolumeSnapshot 时指定卷快照类，系统根据该类调用存储驱动创建底层快照。

卷快照内容（VolumeSnapshotContent）
:   卷快照内容是底层存储系统中实际存在的快照实体。

精简置备
:   在创建卷时，系统并不立即为其分配整个指定空间，而是根据需要动态分配，只有在实际写入数据时才会分配实际的存储空间，未写入时不占用存储空间资源。

厚置备
:   在创建卷时，系统会立即为其分配所指定的所有空间，即使卷实际上仅使用了部分容量，但整个指定空间都会始终被其占用，无法被其他资源所使用。

副本
:   一种数据冗余机制，指在多个节点上存放相同数据的多个副本，以保障数据的高可用性。多副本为数据提供了冗余机制，即使某个节点发生故障，其他健康节点依然还有完整的副本，可保证数据正常的 I/O 读写。

纠删码（Erasure Coding，EC）
:   一种数据冗余机制。它通过特定的算法对 K 个原始数据块（Data Block）进行处理，生成 M 个校验块（Parity Block）。在损坏数据块的数量不超过 M 的情况下，可通过纠删码算法，利用 K 个可用的数据块和校验块即可重建出损坏的数据块，实现数据的恢复和容错能力。通过纠删码，即使部分数据丢失，仍然可以恢复完整的数据，能够有效地提高存储系统的可靠性和容量利用率。

数据加密
:   对卷内部的数据内容进行加密处理，确保即使存储介质被读取也无法直接获得明文数据。

SMTX ZBS
:   SMTX ZBS（读作 SmartX ZBS）是由北京志凌海纳科技股份有限公司（以下简称 “SmartX” ）研发的分布式存储软件，提供块存储、文件存储和运维管理服务。其中，块存储服务支持 iSCSI 协议和 NVMe-oF 协议，文件存储服务支持 NFS 协议和 HDFS 协议。

iSCSI Target
:   iSCSI Target 是 iSCSI Initiator 访问的存储设备，用于响应 Initiator 的存储访问请求。iSCSI Target 将存储资源虚拟化为逻辑单元（LUNs）并提供给远程客户端使用。对于 Initiator 来说，iSCSI Target 提供的 LUN 类似于本地连接的存储设备。SMTX ZBS 块存储集群支持 Initiator 通过统一的接入虚拟 IP 访问 iSCSI Target，无需为每个 iSCSI Target 配置不同的 IP 地址。

iSCSI LUN（iSCSI Logical Unit Number）
:   iSCSI LUN（iSCSI Logical Unit Number）是在 iSCSI 存储服务中用于唯一标识存储设备上逻辑单元的编号。iSCSI Initiator 与 iSCSI Target 进行通信，请求访问特定的 iSCSI LUN，iSCSI Target 接收到请求后，根据 LUN 的标识符将请求路由到相应的存储资源，然后将响应返回给 Initiator，使得 iSCSI Initiator 可以像使用本地存储一样使用 SMTX ZBS 块存储。
:   本驱动中每个持久卷通常映射为一个 iSCSI LUN。

UUID（Universally Unique Identifier）
:   通用唯一标识符，用于唯一标识资源（如卷 ID）。

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
