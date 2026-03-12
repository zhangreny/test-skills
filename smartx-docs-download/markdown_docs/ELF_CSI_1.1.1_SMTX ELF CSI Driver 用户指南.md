---
title: "ELF_CSI/1.1.1/SMTX ELF CSI Driver 用户指南"
source_url: "https://internal-docs.smartx.com/elf-csi/1.1.1/elf_csi_driver_user_guide/elf_csi_driver_user_guide_preface_generic"
sections: 24
---

# ELF_CSI/1.1.1/SMTX ELF CSI Driver 用户指南
## 关于本文档

# 关于本文档

本文档介绍了 SMTX ELF CSI Driver（简称为 “ELF CSI Driver”）的功能和架构，描述了将 ELF CSI Driver 部署在 Kubernetes 集群（简称 “K8s 集群”）的流程，以及如何使用和配置 ELF CSI Driver。 K8s 集群通过运行在 CSI Pod 上的 ELF CSI Driver 可以从 K8s 集群所在的 SMTX OS（ELF）集群中获得持久化存储服务。

阅读本文档需具备在 K8s 集群使用存储的相关操作经验。

---

## 文档更新信息

# 文档更新信息

**2025-11-10：配合 SMTX ELF CSI Driver 1.1.1 正式发布**

---

## 概述

# 概述

SMTX ELF CSI Driver（简称为 “ELF CSI Driver”）是 SmartX 开发的符合 [K8s CSI 规范](https://github.com/container-storage-interface/spec/blob/master/spec.md)的一种 CSI 驱动插件，在 SMTX OS 超融合场景下为标准化 K8s 集群提供持久化存储能力。它实现了对附加到 K8s 集群节点的虚拟卷的生命周期管理，支持通过 PersistentVolumeClaim（简称 “PVC”） 在 K8s 集群中动态创建、挂载 K8s 集群所在 SMTX OS（ELF）集群的虚拟卷给 K8s Pod 使用。

---

## 概述 > 相关概念

# 相关概念

在使用 ELF CSI Driver 前，您需要先了解与其相关的一些概念，以更好地帮助您理解该插件的使用场景、部署流程和功能。

**Kubernetes**

[Kubernetes](https://kubernetes.io/zh-cn/docs/concepts/overview/) 是一个可移植、可扩展的开源平台，用于管理容器化的工作负载和服务，方便进行声明式配置和自动化。Kubernetes 拥有一个庞大且快速增长的生态，其服务、支持和工具的使用范围相当广泛。Kubernetes 简称 “K8s”。

**工作负载**

[工作负载](https://kubernetes.io/zh-cn/docs/concepts/workloads/)是在 K8s 集群上运行的应用程序。K8s 提供若干种内置的工作负载资源，包括 Deployment、StatefulSet、DaemonSet、Job、CronJob 等多种类型。

**Control Plane 节点**

Control Plane 节点上运行 K8s 集群的 [Control Plane 组件](https://kubernetes.io/zh-cn/docs/concepts/overview/components/#control-plane-components)（Control Plane Components）和少数用户的工作负载。

**Worker 节点**

Worker 节点上运行 K8s 集群的[节点组件](https://kubernetes.io/zh-cn/docs/concepts/overview/components/#node-components)和用户的容器化工作负载。

**容器镜像**

[容器镜像](https://kubernetes.io/zh-cn/docs/concepts/containers/images/)所承载的是封装了应用程序及其所有软件依赖的二进制数据。容器镜像是轻量级、可执行的软件包，可以单独运行；该软件包对所处的运行环境具有良定（Well Defined）的假定。应用开发人员通常会创建应用的容器镜像并将其推送到某容器镜像仓库（Container Registry），然后在 Pod 中引用它。

**容器镜像仓库**

容器镜像仓库（Container Registry）是一个用于存储和管理容器镜像的中心化存储系统，提供了一个集中的位置供开发人员和运维人员访问、分享、存储容器镜像。

**存储类**

[存储类](https://kubernetes.io/zh-cn/docs/concepts/storage/storage-classes/)（StorageClass）为管理员提供了描述存储类的方法，包含 provisioner、parameters 和 reclaimPolicy 等字段。这些字段会在 StorageClass 需要动态制备 PersistentVolume 时使用，也可以把存储类理解为 PV 动态制备的模板。这个类的概念在其他存储系统中有时被称为配置文件。

**持久卷**

[持久卷](https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes/)（PersistentVolume，PV）是集群中的一块存储，与节点相似，均为集群层面的资源。持久卷可以由管理员事先制备，或者使用存储类（StorageClass）来[动态制备](https://kubernetes.io/zh-cn/docs/concepts/storage/dynamic-provisioning/)。

**持久卷申领**

持久卷申领（PersistentVolumeClaim，PVC）表达的是用户对存储的请求。概念上与 Pod 类似。Pod 会耗用节点资源，而 PVC 申领会耗用 PV 资源。Pod 可以请求特定数量的资源（CPU 和内存）；同样 PVC 申领也可以请求特定大小和访问模式的 PV。

**[卷快照类](https://kubernetes.io/docs/concepts/storage/volume-snapshot-classes/)**

卷快照类（VolumeSnapshotClass）提供了一种在制备卷快照时描述存储类别的方法。它允许指定属于卷快照（VolumeSnapshot）的不同属性，而从存储系统的相同卷上获取的每个快照的这些属性都可能有所不同，因此不能通过使用与 PVC 相同的存储类来表示。

**[卷快照](https://kubernetes.io/docs/concepts/storage/volume-snapshots/)**

卷快照（VolumeSnapshot）是用户对于卷的快照的请求，它类似于持久卷申领。

---

## 概述 > 产品架构

# 产品架构

![](https://cdn.smartx.com/internal-docs/assets/de5e3891/elf_csi_driver_user_guide.png)

ELF CSI Driver 以 Pod 的形式部署在需要使用该 CSI 的 K8s 集群中，该 K8s 集群的所有节点都必须运行在同一 SMTX OS（ELF）集群中。ELF CSI Driver 中不同的 Pod 提供不同的功能，如下。

- controller-plugin Pod

  controller-plugin Pod 以多副本（默认为 2 副本）的形式运行在 K8s 集群上，负责存储对象（Volume）的生命周期管理。运行在 controller-plugin Pod 中的 ELF CSI Driver 容器主要提供控制服务，包括创建和删除 CSI Volume，对 CSI Volume 执行 Attach/Detach，以及快照等操作。
- node-plugin Pod

  node-plugin Pod 运行在 K8s 集群中的每个节点上，并与节点上的 kubelet 交互，负责为调度到所在节点上的 Pod 准备 Volume。运行在 node-plugin Pod 中的 ELF CSI Driver 容器主要提供节点服务，执行当前节点上的 Volume 挂载、卸载、扩容等操作。

ELF CSI Driver 使用 SMTX OS（ELF）集群的虚拟卷实现 K8s PV。SMTX OS（ELF）集群的虚拟卷实际对应一个 iSCSI LUN，进一步对应到 ZBS Volume，具备超融合系统中 IO 本地化的高性能优势。

---

## 概述 > 最大配置

# 最大配置

建议您在部署 ELF CSI Driver 前，了解 ELF CSI Driver 支持的最大配置，以方便您提前做好规划。

| 项目 | 最大配置 |
| --- | --- |
| 单节点可挂载的 PV 数量 | 与 K8s 集群所在 SMTX OS（ELF）集群的服务器架构有关：  - x86\_64 架构：60 - AArch64 架构：*N*，*N* = 34 - 节点中的虚拟网卡总数 |
| 单个 PV 的容量 | 64 TiB |
| K8s 集群的 VolumeSnapshot 总数 | 100,000（建议不超过 25,000 以保证最佳性能） |

---

## 部署 ELF CSI Driver

# 部署 ELF CSI Driver

ELF CSI Driver 当前仅支持离线部署，本章将介绍离线部署 ELF CSI Driver 的准备工作和部署操作。

---

## 部署 ELF CSI Driver > 准备工作

# 准备工作

部署 ELF CSI Driver 前，请先做好以下准备工作。

## 确认版本配套要求

请参考《SMTX ELF CSI Driver 发布说明》中的[版本配套说明](/elf-csi/1.1.1/release_notes/release_notes_02)，确认 K8s 集群节点的 K8s 软件和操作系统、K8s 集群所在的 SMTX OS（ELF）集群、以及该 SMTX OS（ELF）集群所关联的 CloudTower 满足版本要求。

## 确认 K8s 节点名称与其所在虚拟机名称一致

ELF CSI Driver 通过 K8s 节点名称与虚拟机关联，因此需确保 K8s 节点的名称与节点所在虚拟机的名称一致。

## 开放防火墙协议及端口

为确保 ELF CSI Driver 能正常工作，若以下源端和目标端之间存在防火墙，则需开放相应的协议和端口：

| 源端 | 目标端 | 开放的协议和端口 | 用途 |
| --- | --- | --- | --- |
| K8s 集群节点对应的虚拟机 | K8s 集群所在 SMTX OS（ELF）集群关联的 CloudTower 虚拟机 | TCP：443 | ELF CSI Driver 连接 CloudTower API 服务 |
| K8s 集群节点对应的虚拟机 | K8s 集群节点对应的虚拟机 | TCP：9912, 9913 | ELF CSI Driver 内部访问端口 |

## 获取 ELF CSI Driver 安装文件

离线部署 ELF CSI Driver 时，由于部署的环境无法连接外网，您需在外网环境下提前下载 ELF CSI Driver 的安装文件。

## 准备容器镜像仓库

1. 准备一个可被 K8s 集群使用的私有容器镜像仓库，并获取登录凭据。
2. 登录仓库，新建或指定用于存储 ELF CSI Driver 相关容器镜像的 project。
3. 确保当前账号具有该 project 的镜像推送权限。

---

## 部署 ELF CSI Driver > 执行部署

# 执行部署

以下步骤可以在任一可连接 K8s 集群 apiserver 和私有镜像仓库的节点上执行。

**操作步骤**

1. 上传 ELF CSI Driver 安装文件至当前节点。
2. 在当前节点执行以下命令解压缩 ELF CSI Driver 安装文件。其中 `<CSI_DRIVER_VERSION>` 表示 ELF CSI Driver 安装文件的版本，例如 `v1.x.x`，请根据实际情况进行替换。

   ```
   unzip csi-driver-offline-<CSI_DRIVER_VERSION>.zip && cd csi-driver-offline
   ```
3. 执行以下命令生成 ELF CSI Driver 配置文件的模板 **csi-driver.yaml**。

   ```
   ./bin/linux-$(uname -m)/helm show values ./chart/elf-csi-driver.tgz > csi-driver.yaml
   ```
4. 执行以下命令，以推送 ELF CSI Driver 容器镜像至指定的私有容器镜像仓库。

   ```
   export IMAGE_NAMESPACE=docker.io/elf-csi # docker.io/elf-csi 仅为私有容器镜像仓库地址的示例，请按需进行替换。

   for file in images/*; do
      ./bin/linux-$(uname -m)/crane push --index $file $IMAGE_NAMESPACE/${file##*/}
   done
   ```

   执行以上命令后，若返回 UNAUTHORIZED，请执行以下命令登录私有容器镜像仓库后再次尝试。其中 `<IMAGE_REGISTRY>` 表示私有容器镜像仓库地址，`<USERNAME>` 表示私有容器镜像仓库的用户名，`<PASSWORD>` 表示私有容器镜像仓库的密码，请根据实际情况进行替换。

   ```
   ./bin/linux-$(uname -m)/crane auth login <IMAGE_REGISTRY> -u <USERNAME> -p <PASSWORD>
   ```
5. 执行以下命令，以在 csi-driver.yaml 文件中同步指定上一步的容器镜像拉取地址。

   ```
   ./bin/linux-$(uname -m)/yq -i ".imageNamespaceOverride = \"$IMAGE_NAMESPACE\"" ./csi-driver.yaml
   ```
6. 根据如下参数说明表配置 csi-driver.yaml。无默认值（ 默认值列显示 “-”）的参数必须手动配置，已有默认值的参数可根据您的需要进行修改。

   **支持配置的参数说明**

   | 参数 | | 默认值 | 描述 |
   | --- | --- | --- | --- |
   | storageClass | create | `true` | 是否创建 StorageClass。 |
   | default | `true` | 是否配置为 K8s 集群默认的 StorageClass。 |
   | parameters.csi.​storage.k8s.io/fstype | `ext4` | 创建的 StorageClass 配置的卷默认挂载文件类型。支持配置为 `ext4` 或 `xfs`。 |
   | parameters.storage​Policy | `REPLICA_2_THIN_​PROVISION` | 创建的 StorageClass 配置的卷存储策略。支持配置为 `REPLICA_2_THIN_​PROVISION`、`REPLICA​_3_THIN_PROVISION`、`​REPLICA_2_THICK_​PROVISION` 或 `REPLICA_3_​THICK_PROVISION`。当 SMTX OS（ELF）集群为双活集群时，则必须配置为 `REPLICA_3_THIN_PROVISION` 或 `REPLICA_3_THICK_PROVISION`。 |
   | parameters.elfCluster | - | 制备虚拟卷使用的 SMTX OS（ELF）集群的 LocalID，可在集群**概览**页的**集群**卡片右上角单击**复制 UUID** 获取。 **注意**：请确保填写的集群为部署 ELF CSI Driver 的 K8s 集群所在的 SMTX OS（ELF）集群。该 K8s 集群的所有节点需要运行在同一 SMTX OS（ELF）集群中。 |
   | reclaimPolicy | `Delete` | 创建的 StorageClass 配置的卷删除策略。支持配置为 `Delete` 或 `Retain`。 |
   | snapshotClass | Create | `true` | 是否创建 VolumeSnapshotClass。 |
   | default | `true` | 是否配置为 K8s 集群默认的 VolumeSnapshotClass。 |
   | deletionPolicy | `Delete` | 创建的 VolumeSnapshotClass 配置的快照删除策略。支持配置为 `Delete` 或 `Retain`。 |
   | driver | clusterID | `my-cluster` | K8s 集群的唯一 ID，可由您自行配置，当有多个 K8s 集群利用 SMTX OS（ELF）集群提供存储服务时，此 ID 的取值为 K8s 集群的唯一标识。 |
   | preferredVolumeBus​Type | `VIRTIO` | 卷优先挂载到的虚拟机总线。支持配置为 `VIRTIO` 或 `SCSI`。 |
   | maxSnapshotsPer​Volume | `3` | 每个卷的快照最大创建数量，默认为 `3`，建议不超过 32 以保证最佳性能。 |
   | defaultStoragePolicy | `REPLICA_2_THIN_​PROVISION` | 当`storageClass` 中的 `storagePolicy` 未配置、配置为空、或者配置为不支持的值时，将以该参数值作为默认值。支持配置为 `REPLICA_2_THIN_​PROVISION`、`REPLICA_3​_THIN_PROVISION`、​`REPLICA_2_THICK_​PROVISION` 或 `REPLICA_3_THICK_​PROVISION`。当 SMTX OS（ELF）集群为双活集群时，则必须配置为 `REPLICA_3_THIN_​PROVISION` 或 `REPLICA_3_THICK_​PROVISION`。 |
   | cloudTowerServer.​create | `false` | 创建访问 SMTX OS（ELF）集群所关联的 CloudTower 的普通访问密钥。若配置为 `false`，将会使用部署 CSI Driver 的 namespace 下已存在的 cloudtower-server 密钥。 |
   | cloudTowerServer.​server | - | SMTX OS（ELF）集群所关联的 CloudTower 的访问域名或者 IP 地址。 |
   | cloudTowerServer.​authMode | - | SMTX OS（ELF）集群所关联的 CloudTower 的身份验证模式。支持配置为 `LDAP` 或 `LOCAL`。 |
   | cloudTowerServer.​username | - | SMTX OS（ELF）集群所关联的 CloudTower 的普通用户名。 |
   | cloudTowerServer.​password | - | SMTX OS（ELF）集群所关联的 CloudTower 的普通用户密码。 |
   | cloudTowerAdmin.​create | `false` | 创建访问 SMTX OS（ELF）集群所关联的 CloudTower 的管理员访问密钥。若配置为 `false`，将会使用部署 CSI Driver 的 namespace 下已存在的 cloudtower-admin 密钥。 |
   | cloudTowerAdmin.​username | - | SMTX OS（ELF）集群所关联的 CloudTower 的管理员用户名。 |
   | cloudTowerAdmin.​password | - | SMTX OS（ELF）集群所关联的 CloudTower 的管理员用户密码。 |
   | imageNamespaceOverride | | - | 私有容器镜像仓库地址。配置该参数前，需先将 ELF CSI Driver 容器镜像推送至对应的仓库地址。步骤 4 和 5 已完成镜像推送和该参数的配置操作。 |
   | imagePullSecrets | | - | 拉取私有容器镜像仓库的镜像所使用的密钥，具体使用方式可参考 [K8s 官方文档](https://kubernetes.io/zh-cn/docs/tasks/configure-pod-container/pull-image-private-registry/)。 示例：  `imagePullSecrets:`  `- name: harbor` |
7. 执行以下命令部署 ELF CSI Driver。

   ```
   ./bin/linux-$(uname -m)/helm install elf-csi-driver ./chart/elf-csi-driver.tgz -n smtx-system --create-namespace -f csi-driver.yaml --wait
   ```
8. ELF CSI Driver 部署结束后，执行以下命令检查 ELF CSI Driver 是否部署成功。

   ```
   kubectl get pods -n smtx-system
   ```

   若显示如下输出结果，则表明部署成功。

   ```
   NAME                                                     READY   STATUS    RESTARTS   AGE
   smtx-elf-csi-driver-controller-plugin-675d9f79b6-j7z25   6/6     Running   0          21h
   smtx-elf-csi-driver-controller-plugin-675d9f79b6-lfh8l   6/6     Running   0          21h
   smtx-elf-csi-driver-node-plugin-j69sq                    3/3     Running   0          21h
   smtx-elf-csi-driver-node-plugin-zlwgk                    3/3     Running   0          21h
   ```

   > **说明**：
   >
   > ELF CSI Driver 部署成功后，如果需要修改 csi-driver.yaml 的配置，请参考[更新 ELF CSI Driver](/elf-csi/1.1.1/elf_csi_driver_user_guide/elf_csi_driver_user_guide_20) 进行操作。
9. 若部署 ELF CSI Driver 前 K8s 集群中未安装 [snapshot-controller](https://github.com/kubernetes-csi/external-snapshotter/tree/master/cmd/snapshot-controller)，并且 csi-driver.yaml 中的 `snapshotClass.Create` 参数配置为 `true`，则请执行以下命令创建对应的 VolumeSnapshotClass 资源。

   ```
   ./bin/linux-$(uname -m)/helm upgrade elf-csi-driver ./chart/elf-csi-driver.tgz -n smtx-system -f csi-driver.yaml
   ```

---

## 卷管理

# 卷管理

本章主要介绍如何创建存储类（StorageClass），以及如何创建、扩容和克隆持久卷（PV）。

---

## 卷管理 > 创建存储类

# 创建存储类

ELF CSI Driver 支持通过动态卷制备的方式为 pod 创建 PV。要使用动态制备功能，您需要预先创建一个或多个 StorageClass。

若在 ELF CSI Driver 部署时在 csi-driver.yaml 配置创建 StorageClass，则部署成功后，将会自动创建一个名称为 smtx-elf-csi-driver 的 StorageClass。您可以使用该 StorageClass 来创建 PV，也可以参考本小节的操作步骤通过自定义参数来创建新的 StorageClass。新建的 StorageClass 需符合下表描述中的取值要求。

| 参数 | | 描述 | 缺省值 | smtx-elf-csi-driver 中的取值 |
| --- | --- | --- | --- | --- |
| parameters | csi.storage.k8s.io/fstype | 创建的 StorageClass 配置的卷默认挂载文件类型。支持配置为 `ext4` 或 `xfs`。 | `ext4` | 保持与部署时自定义的数值一致，若部署时未修改该参数值，则该值为 `ext4`。 |
| storagePolicy | 创建的 StorageClass 配置的卷存储策略。支持配置为 `REPLICA_2_THIN_​PROVISION`、​`REPLICA_3_THIN_​PROVISION`、​`REPLICA_2_THICK_​PROVISION` 或 `REPLICA_3_THICK_​PROVISION`。当 SMTX OS（ELF）集群为双活集群时，则必须配置为 `REPLICA_3_THIN_PROVISION` 或 `REPLICA_3_THICK_PROVISION`。 | `REPLICA_2_THIN_​PROVISION` | 保持与部署时自定义的数值一致，若部署时未修改该参数值，则该值为 `REPLICA_2_THIN_​PROVISION`。 |
| elfCluster | 制备虚拟卷使用的 SMTX OS（ELF）集群的 LocalID，可在集群**概览**页的**集群**卡片右上角单击**复制 UUID** 获取。 **注意**：使用 ELF CSI Driver 创建 PV 时，请确保填写的集群为部署 ELF CSI Driver 的 K8s 集群所在的 SMTX OS（ELF）集群。该 K8s 集群的所有节点需要运行在同一 SMTX OS（ELF）集群中。 | - | 保持与部署时自定义的数值一致。 |
| provisioner | | 制备器，用于制备 PV。使用 ELF CSI Driver 创建 PV 时，必须配置为 `com.smartx.elf-csi-driver`。 | - | `com.smartx.elf-csi-driver` |
| reclaimPolicy | | 当 PVC 被删除时，此参数决定了是否保留 PV。支持配置为 `Delete` 或 `Retain`。 | `Delete` | 保持与部署时自定义的数值一致，若部署时未修改该参数值，则该值为 `Delete`。 |
| allowVolumeExpansion | | 是否允许卷扩容。支持配置为 `true` 或 `false`。 | `true` | `true` |

**操作步骤**

以下步骤均在任一可连接 K8s 集群 apiserver 的节点上执行。

1. 通过 YAML 文件 sc.yaml 定义一个 StorageClass。

   **YAML 示例**

   ```
   ​​apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: elf-csi-driver-sc
   parameters:
     csi.storage.k8s.io/fstype: ext4 # file system type
     storagePolicy: REPLICA_2_THIN_PROVISION  # storagePolicy
     elfCluster: fake_elf_cluster # elf cluster id
   provisioner: com.smartx.elf-csi-driver
   reclaimPolicy: Delete
   allowVolumeExpansion: true
   ```
2. 执行以下命令，使 sc.yaml 文件生效，系统将自动创建一个 StorageClass。

   ```
   kubectl apply -f sc.yaml
   ```
3. 执行以下命令查看新创建的 StorageClass，其中 `<storageclass_name>` 为 StorageClass 的名称。

   ```
   kubectl get storageclass <storageclass_name>
   ```

   若显示如下输出结果，则表明该 StorageClass 创建成功。

   ```
   NAME                            PROVISIONER                 RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
   elf-csi-driver-sc               com.smartx.elf-csi-driver   Delete          Immediate           true                   129d
   ```

---

## 卷管理 > 创建持久卷

# 创建持久卷

ELF CSI Driver 支持通过创建一个配置有特定存储容量、卷模式、访问模式的持久卷声明（PVC）来动态制备一个 PV，并将此 PV 和 PVC 绑定，然后就能将此 PV 挂载给 Kubernetes 集群的 pod 使用。

**注意事项**

- 创建的 PV 大小必须为 1Gi 的整数倍。
- PV 创建完成后，请勿在当前 K8s 集群所在的 SMTX OS（ELF）集群中删除 PV 对应的虚拟卷，以免导致 PV 状态异常。

**操作步骤**

以下步骤均在任一可连接 K8s 集群 apiserver 的节点上执行。

1. 通过 YAML 文件 pvc.yaml 定义一个 PVC，明确 PVC 的访问模式、存储容量和卷模式。

   **参数说明**

   | 参数 | 描述 |
   | --- | --- |
   | accessModes | PVC 的访问模式。 - 若卷模式为 Block，则支持配置为 `ReadWriteOnce`、`ReadOnlyMany` 或 `ReadWriteMany`。 - 若卷模式为 Filesystem，则支持配置为 `ReadWriteOnce`。 |
   | resources.requests.storage | PVC 的存储容量。支持配置为 `1Gi` ～ `65536Gi`。 |
   | storageClassName | 使用 ELF CSI Driver 创建 PV 时，请选择当前 K8s 集群中 provisioner 参数为 `com.smartx.elf-csi-driver` 的 storageClass。 |
   | volumeMode | PVC 的卷模式。支持配置为 `Block` 或 `Filesystem`。 |

   **YAML 示例**

   ```
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: elf-csi-driver-pvc
     namespace: default
   spec:
     storageClassName: elf-csi-driver-sc
     accessModes:
     - ReadWriteOnce
     resources:
       requests:
         storage: 2Gi
     volumeMode: Block
   ```

   更多细节请参见 [Kubernetes Documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)。
2. 执行以下命令，使 pvc.yaml 文件生效，系统自动创建一个 PVC，并制备一个 PV。

   ```
   kubectl apply -f pvc.yaml
   ```
3. 执行以下命令查看新创建的 PVC，其中 `<pvc_name>` 为 PVC 的名称。

   ```
   kubectl get pvc <pvc_name>
   ```

   输出示例如下，`VOLUME` 列将显示新创建的 PV 的名称。当 `STATUS` 取值为 `Bound` 时，表示 PVC 已经创建完成，并且和 PV 绑定成功。

   ```
   NAME                      STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS          AGE
   elf-csi-driver-pvc        Bound    pvc-a8413608-f9bc-4909-a008-6a398aa73084   2Gi        RWO            elf-csi-driver-sc     43s
   ```
4. 执行以下命令查看 PV 的详细信息，其中 `<pv_name>` 为 PV 的名称。

   ```
   kubectl get pv <pv_name>
   ```

   若显示如下输出结果，则表明 PV 创建成功。

   ```
   NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                             STORAGECLASS          REASON   AGE
   pvc-a8413608-f9bc-4909-a008-6a398aa73084   2Gi        RWO            Delete           Bound    default/elf-csi-driver-pvc        elf-csi-driver-sc              2m13s
   ```

---

## 卷管理 > 扩容持久卷

# 扩容持久卷

若要扩容 PV，您只需更新该 PV 对应 PVC 中的 `spec.resources.requests.storage` 字段。

**前提条件**

待扩容 PV 所对应的 StorageClass 的 `allowVolumeExpansion` 参数已设置为 `true`。

**注意事项**

扩容后的 PV 大小必须为 1Gi 的整数倍。

**操作步骤**

下面以一个通过 YAML 文件 pvc.yaml 定义的 PVC 为例，描述扩容 PV 的操作步骤。该 PVC 的名称为 example-pvc，容量为 10Gi。

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
 name: example-pvc
 namespace: default
spec:
 storageClassName: elf-csi-driver-sc
 accessModes:
 - ReadWriteOnce
 resources:
   requests:
     storage: 10Gi # The original capacity of the PVC.
```

以下步骤均在任一可连接 K8s 集群 apiserver 的节点上执行。

1. 执行以下命令查看待修改容量的 PVC。

   ```
   kubectl get pvc example-pvc
   ```

   输出示例如下，其中 `VOLUME` 和 `CAPACITY` 参数分别表示此 PVC 对应的 PV 的名称和 PVC 的容量。

   ```
   NAME               STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS          AGE
   example-pvc        Bound    pvc-585689b2-7e56-43a9-96f5-1bbcb9043bc2   10Gi       RWO            elf-csi-driver-sc     3m12s
   ```
2. 执行以下命令更新 PVC 中的 `spec.resources.requests.storage` 字段为 20Gi。

   ```
   kubectl patch -p "{\"spec\":{\"resources\":{\"requests\":{\"storage\":\"20Gi\"}}}}" pvc/example-pvc
   ```
3. 执行以下命令查看修改后的 PVC 的详细信息，并获取 PV 的名称。

   ```
   kubectl get pvc example-pvc
   ```

   > **说明**：
   >
   > PVC 更新后，系统将修改 PV 的容量，但不调整 PVC 的容量。只有 Pod 使用此 PVC 时，PVC 的容量才会自动调整。如下示例中的 `example-pvc` 为未被 Pod 使用的 PVC。

   输出示例如下。

   ```
   NAME               STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS          AGE
   example-pvc        Bound    pvc-585689b2-7e56-43a9-96f5-1bbcb9043bc2   10Gi       RWO            elf-csi-driver-sc     7m54s
   ```
4. 执行以下命令确认 PV 是否已扩容。

   ```
   kubectl get pv pvc-585689b2-7e56-43a9-96f5-1bbcb9043bc2
   ```

   输出示例如下，若 `CAPACITY` 参数显示为 `20Gi`，则表明 PV 的容量已经修改为 20Gi。

   ```
   NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                      STORAGECLASS          REASON   AGE
   pvc-585689b2-7e56-43a9-96f5-1bbcb9043bc2   20Gi       RWO            Delete           Bound    default/example-pvc        elf-csi-driver-sc              8m28s
   ```

---

## 卷管理 > 克隆持久卷

# 克隆持久卷

若要克隆一个 PV，您可以通过创建一个新的 PVC，并指定 `dataSource` 参数为待克隆的 PV 所对应的 PVC 来实现。

**前提条件**

克隆 PV 前已存在一个 PVC。

**注意事项**

- 目标 PVC 和源 PVC 必须在同一个命名空间中。
- 目标 PVC 和源 PVC 的 StorageClass、卷模式和容量必须相同。

**操作步骤**

以下步骤均在任一可连接 K8s 集群 apiserver 的节点上执行。

1. 通过 YAML 文件 clone.yaml 定义一个与源 PVC 在同一命名空间的 PVC，在 `spec` 中指明源 PVC 的名称（`dataSource.name`），以及与源 PVC 相同的 StorageClass 名称（`storageClassName`）、卷模式（`volumeMode`）和容量（`storage`）。

   **YAML 示例**

   ```
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: cloned-pvc
     namespace: default
   spec:
     storageClassName: elf-csi-driver-sc # The StorageClass must be the same as that of the source PVC.
     dataSource:
       name: example-pvc # Specify the source PVC that should be from the same namespace as the target PVC.
       kind: PersistentVolumeClaim
     accessModes:
     - ReadWriteOnce
     resources:
       requests:
         storage: 20Gi # The capacity value must be the same as that of the source volume.
     volumeMode: Filesystem # The volume mode must be the same as that of the source PVC.
   ```
2. 执行以下命令，使 clone.yaml 文件生效，系统自动克隆出一个 PVC 和对应的 PV。

   ```
   kubectl apply -f clone.yaml
   ```
3. 执行以下命令查看新克隆的 PVC，其中 `<cloned_pvc_name>` 为新克隆的 PVC 名称。

   ```
   kubectl get pvc <cloned_pvc_name>
   ```

   输出示例如下，当 `STATUS` 取值为 `Bound` 时，表示 PV 克隆成功。

   ```
   NAME         STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS          AGE
   cloned-pvc   Bound    pvc-b872ed5f-f6f2-4474-8012-a501164e4e07   20Gi       RWO            elf-csi-driver-sc     43s
   ```

---

## 卷快照管理

# 卷快照管理

本章主要介绍如何创建卷快照类（VolumeSnapshotClass）和卷快照（VolumeSnapshot），以及如何从 VolumeSnapshot 恢复 PV。

---

## 卷快照管理 > 创建卷快照类

# 创建卷快照类

每个 VolumeSnapshot 都需指定一个 VolumeSnapshotClass，在创建 VolumeSnapshot 时，VolumeSnapshotClass 用来描述快照的类别。

**操作步骤**

以下步骤均在任一可连接 K8s 集群 apiserver 的节点上执行。

1. 通过 YAML 文件 vsc.yaml 定义一个 VolumeSnapshotClass。

   **参数说明**

   | 参数 | 描述 |
   | --- | --- |
   | driver | 制备快照的 CSI 驱动程序。使用 ELF CSI Driver 创建 VolumeSnapshot 时，必须配置为 `com.smartx.elf-csi-driver`。 |
   | deletionPolicy | 在删除 VolumeSnapshot 对象时，其对应的 VolumeSnapshotContent 使用的保留策略。支持配置为 `Retain` 或 `Delete`。 |

   **YAML 示例**

   ```
   apiVersion: snapshot.storage.k8s.io/v1
   kind: VolumeSnapshotClass
   metadata:
     name: elf-csi-driver-vsc
   driver: com.smartx.elf-csi-driver # Specify the driver, which defaults to the driver in csi-driver.yaml.
   deletionPolicy: Delete # Specify the deletion policy.
   ```
2. 执行以下命令，使 vsc.yaml 文件生效，系统自动创建一个 VolumeSnapshotClass。

   ```
   kubectl apply -f vsc.yaml
   ```
3. 执行以下命令查看新创建的 VolumeSnapshotClass，其中 `<snapshotclass_name>` 为 VolumeSnapshotClass 的名称。

   ```
   kubectl get volumesnapshotclass <snapshotclass_name>
   ```

   若显示如下输出结果，则表明该 VolumeSnapshotClass 创建成功。

   ```
   NAME                       DRIVER                      DELETIONPOLICY   AGE
   elf-csi-driver-vsc       com.smartx.elf-csi-driver   Delete           24s
   ```

---

## 卷快照管理 > 创建卷快照

# 创建卷快照

VolumeSnapshot 是对 PV 创建快照的请求，类似于 PVC。

**前提条件**

- 创建 VolumeSnapshot 前，必须已存在一个 VolumeSnapshotClass 和一个与 PV 绑定的 PVC。
- VolumeSnapshot 必须与源 PVC 在同一个命名空间中。

**操作步骤**

以下步骤均在任一可连接 K8s 集群 apiserver 的节点上执行。

1. 通过 YAML 文件 snapshot.yaml 定义一个 VolumeSnapshot，同时指定 VolumeSnapshotClass 和 PVC 的名称。

   **YAML 示例**

   ```
   apiVersion: snapshot.storage.k8s.io/v1
   kind: VolumeSnapshot
   metadata:
     name: example-snapshot
     namespace: default
   spec:
     volumeSnapshotClassName: elf-csi-driver-vsc # Specify a SnapshotClass such as `smtx-csi-driver-default`.
     source:
       persistentVolumeClaimName: example-pvc # Specify the PVC for which you want to take a snapshot such as `mongodb-data-pvc`.
   ```
2. 执行以下命令，使 snapshot.yaml 文件生效，系统自动创建一个 VolumeSnapshot。

   ```
   kubectl apply -f snapshot.yaml
   ```
3. 执行以下命令查看新创建的 VolumeSnapshot，其中 `<snapshot_name>`为 VolumeSnapshot 的名称。

   ```
   kubectl get Volumesnapshots <snapshot_name>
   ```

   输出示例如下，当 `READYTOUSE` 取值为 `true` 时，表明卷快照创建成功。

   ```
   NAME               READYTOUSE   SOURCEPVC          SOURCESNAPSHOTCONTENT   RESTORESIZE   SNAPSHOTCLASS                 SNAPSHOTCONTENT                                    CREATIONTIME   AGE
   example-snapshot   true         example-pvc                                20Gi          elf-csi-driver-vsc            snapcontent-d060e214-f2eb-4b78-9dbd-0e10e2506c4d   82s            18m
   ```

---

## 卷快照管理 > 从卷快照恢复持久卷

# 从卷快照恢复持久卷

通过创建一个新的 PVC，并指定 `dataSource` 参数为目标 VolumeSnapshot，可以从 VolumeSnapshot 恢复 PV。

**注意事项**

通过 VolumeSnapshot 恢复的 PV 与源 PV 的命名空间、StorageClass、访问模式、卷模式和存储容量必须相同。

**操作步骤**

以下步骤均在任一可连接 K8s 集群 apiserver 的节点上执行。

1. 通过 YAML 文件 restore.yaml 定义一个 PVC，在 `spec` 中指明所引用的 VolumeSnapshot 名称（`dataSource.name`），以及与源 PV 相同的命名空间（`namespace`）、StorageClass 名称（`storageClassName`）、访问模式（`accessModes`）、卷模式（`volumeMode`）和容量（`storage`）。

   **YAML 示例**

   ```
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: example-restore
     namespace: default
   spec:
     storageClassName: elf-csi-driver-sc
     dataSource:
       name: example-snapshot
       kind: VolumeSnapshot
       apiGroup: snapshot.storage.k8s.io
   accessModes:
   - ReadWriteOnce
   resources:
     requests:
       storage: 20Gi
   ```
2. 执行以下命令，使 restore.yaml 文件生效，系统自动创建一个 VolumeSnapshot 对应的 PVC 和 PV，并将此 PVC 和 PV 绑定。

   ```
   kubectl apply -f restore.yaml
   ```
3. 执行以下命令查看新创建的 PVC，其中 `<pvc_name>` 为 PVC 的名称。

   ```
   kubectl get pvc <pvc_name>
   ```

   输出示例如下，当 `STATUS` 取值为 `Bound` 时，表示从卷快照恢复持久卷成功。

   ```
   kubectl get pvc example-restore
   NAME              STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS          AGE
   example-restore   Bound    pvc-41fd38ad-7ff2-4f0e-837a-fae0d0d5b60a   20Gi       RWO            elf-csi-driver-sc   81s
   ```

---

## ELF CSI Driver 运维 > 更新 ELF CSI Driver

# 更新 ELF CSI Driver

ELF CSI Driver 部署完成后，若您需要修改 ELF CSI Driver 的配置，可参考以下步骤进行操作。

**操作步骤**

以下步骤均在任一可连接 K8s 集群 apiserver 的节点上执行。

1. 执行以下命令，以进入离线部署 ELF CSI Driver 时解压好的 csi-driver-offline 目录。

   ```
   cd ./csi-driver-offline
   ```
2. 打开 csi-driver.yaml，参考[执行部署](/elf-csi/1.1.1/elf_csi_driver_user_guide/elf_csi_driver_user_guide_10)中对 csi-driver.yaml 的参数说明按需修改 csi-driver.yaml 中的参数配置。
3. 执行以下命令进行更新。

   ```
   ./bin/linux-$(uname -m)/helm upgrade elf-csi-driver ./chart/elf-csi-driver.tgz -n smtx-system -f csi-driver.yaml
   ```
4. 执行以下命令查看 K8s 集群中 CSI Pod 的状态。

   ```
   kubectl get pods -n smtx-system
   ```

   当所有 CSI Pod 均处于 running 状态时，表示 ELF CSI Driver 更新成功。

---

## ELF CSI Driver 运维 > 升级 ELF CSI Driver

# 升级 ELF CSI Driver

ELF CSI Driver 当前仅支持离线升级。升级操作不影响已挂载 PVC 的 Pod 的正常运行。

**操作步骤**

以下步骤均在任一可连接 K8s 集群 apiserver 的节点上执行。

1. 上传新版本 ELF CSI Driver 安装文件至当前节点。
2. 在当前节点执行以下命令，以解压缩 ELF CSI Driver 安装文件。其中 `<CSI_DRIVER_VERSION>` 表示当前 ELF CSI Driver 安装文件的版本，例如 `v1.x.x`，请根据实际情况进行替换。

   ```
   unzip csi-driver-offline-<CSI_DRIVER_VERSION>.zip && cd csi-driver-offline
   ```
3. 执行以下命令，以推送 ELF CSI Driver 容器镜像至指定的私有容器镜像仓库。

   ```
   export IMAGE_NAMESPACE=docker.io/elf-csi # docker.io/elf-csi 仅为私有容器镜像仓库地址的示例，请按需进行替换。

   for file in images/*; do
      ./bin/linux-$(uname -m)/crane push --index $file $IMAGE_NAMESPACE/${file##*/}
   done
   ```

   执行以上命令后，若返回 UNAUTHORIZED，请执行以下命令登录私有容器镜像仓库后再次尝试。其中 `<IMAGE_REGISTRY>` 表示私有容器镜像仓库地址，`<USERNAME>` 表示私有容器镜像仓库的用户名，`<PASSWORD>` 表示私有容器镜像仓库的用户密码，请根据实际情况进行替换。

   ```
   ./bin/linux-$(uname -m)/crane auth login <IMAGE_REGISTRY> -u <USERNAME> -p <PASSWORD>
   ```
4. 执行以下命令进行升级。

   ```
   ./bin/linux-$(uname -m)/helm upgrade elf-csi-driver ./chart/elf-csi-driver.tgz -n smtx-system --reuse-values --set imageNamespaceOverride=$IMAGE_NAMESPACE --set driver.defaultStoragePolicy=REPLICA_2_THIN_PROVISION
   ```
5. 执行以下命令查看 K8s 集群中 CSI Pod 的状态。

   ```
   kubectl get pods -n smtx-system
   ```

   当所有 CSI Pod 均处于 running 状态时，表示 ELF CSI Driver 升级成功。

---

## ELF CSI Driver 运维 > 卸载 ELF CSI Driver

# 卸载 ELF CSI Driver

ELF CSI Driver 当前仅支持离线卸载。卸载 ELF CSI Driver 后，K8s 集群中的 Pod 将无法继续使用其创建的持久卷或者利用其执行卷操作和卷快照操作。

**注意事项**

建议在卸载前先删除使用该 ELF CSI Driver 创建的存储资源，否则卸载完成后将无法删除这些存储资源。

**操作步骤**

以下步骤均在任一可连接 K8s 集群 apiserver 的节点上执行。

1. 执行以下命令，以进入离线部署 ELF CSI Driver 时解压好的 csi-driver-offline 目录。

   ```
   cd ./csi-driver-offline
   ```
2. 执行以下命令卸载 ELF CSI Driver。

   ```
   ./bin/linux-$(uname -m)/helm uninstall elf-csi-driver -n smtx-system
   ```
3. 执行以下命令查看 K8s 集群中 CSI Pod 的状态，确保所有 CSI Pod 已删除。

   ```
   kubectl get pods -n smtx-system
   ```

   若输出结果不显示任何 Pod 信息，则表明所有 CSI Pod 已删除，ELF CSI Driver 卸载成功。

---

## 附录 > CSI Spec RPC 接口实现列表

# CSI Spec RPC 接口实现列表

| RPC Function Name | RPC service | Implemented |
| --- | --- | --- |
| GetPluginInfo | Identity | Yes |
| GetPluginCapabilities | Identity | Yes |
| Probe | Identity | Yes |
| CreateVolume | Controller | Yes |
| DeleteVolume | Controller | Yes |
| ControllerPublishVolume | Controller | Yes |
| ControllerUnpublishVolume | Controller | Yes |
| ValidateVolumeCapabilities | Controller | Yes |
| ListVolumes | Controller | No |
| GetCapacity | Controller | No |
| ControllerGetCapabilities | Controller | No |
| CreateSnapshot | Controller | Yes |
| DeleteSnapshot | Controller | Yes |
| ListSnapshots | Controller | No |
| ControllerExpandVolume | Controller | Yes |
| ControllerGetVolume | Controller | No |
| NodeStageVolume | Node | Yes |
| NodeUnstageVolume | Node | Yes |
| NodePublishVolume | Node | Yes |
| NodeUnpublishVolume | Node | Yes |
| NodeGetVolumeStats | Node | Yes |
| NodeExpandVolume | Node | Yes |
| NodeGetCapabilities | Node | Yes |
| NodeGetInfo | Node | Yes |

---

## 附录 > CSI 特性支持情况

# CSI 特性支持情况

| CSI 特性 | K8s 版本 | SMTX ELF CSI Driver | 补充说明 |
| --- | --- | --- | --- |
| Secret - StroageClass | 无关 | 暂不支持 | - |
| Secret - Snapshot | 无关 | 暂不支持 | - |
| Topology | 1.17 | 暂不支持 | - |
| Raw Block Volume | 1.18 | 支持 | - |
| Skip Attach | 1.18 | 不支持 | 该特性仅用于类文件存储的场景 |
| Pod Info on Mount | 1.18 | 默认不支持，用户可以打开 | 该特性仅面向开发者，对用户透明 |
| Volume Expansion | 1.16 | 支持 | - |
| Data Source - Clone | 1.18 | 支持 | - |
| Data Source - Snapshot | 1.17 (Beta) | 支持 | - |
| Ephemeral Local Volume | 1.16 | 暂不支持 | - |
| Volume Limits | 1.17 | 支持 | - |
| Storage Capacity Tracking | 1.19 (Alpha) | 不支持 | 该特性适用于依赖本地存储的 CSI，ZBS 是网络存储 |
| Volume Health Monitoring | Alpha (Sidecar 0.1.0) | 暂不支持 | - |
| Token Requests | 1.22 | 不支持 | - |
| FSGroup Support | 1.23 | 不支持 | - |
| CSI Windows | 1.19 | 不支持 | - |

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
