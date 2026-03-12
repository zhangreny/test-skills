---
title: "SMTXV2V/1.8.0/SMTX 迁移工具用户指南"
source_url: "https://internal-docs.smartx.com/smtxv2v/1.8.0/v2v_user_guide/v2v-guide-preface"
sections: 37
---

# SMTXV2V/1.8.0/SMTX 迁移工具用户指南
## 关于本文档

# 关于本文档

本文档介绍了 SMTX 迁移工具的适用场景，以及使用该工具将虚拟机迁移到 ELF 平台的操作方法。

阅读本文档的对象需要了解 SMTX OS 超融合软件，并具备数据中心操作的丰富经验。

---

## 更新信息

# 更新信息

**2026-03-06：配合 SMTX 迁移工具 1.8.0 正式发布**

相较于 1.7.2 版本，本版本更新内容如下：

- **迁移虚拟机** > **创建迁移任务**：
  - **第 2 步：选择待迁移的虚拟机**：在步骤 1 中增加待迁移的虚拟机版本要求。
  - **第 4 步：自定义虚拟机配置项**：在步骤 1 中增加设置数据加密算法的说明，以及在步骤 4 中增加迁移完成后目标端虚拟机自动卸载 VMware Tools 的说明。
- **迁移增量数据（仅源端虚拟机开机时操作）**：增加选择循环增量迁移源端虚拟机的步骤，若源端虚拟机已安装 VMware Tools，支持选择迁移增量数据并自动关机。

---

## SMTX 迁移工具简介

# SMTX 迁移工具简介

SMTX 迁移工具是一款用于跨平台迁移虚拟机的工具，支持将运行在 VMware ESXi 虚拟化平台的虚拟机迁移到 ELF 平台，或在两个 ELF 平台之间相互迁移虚拟机。使用 SMTX 迁移工具进行迁移时，虚拟机在迁移过程中的大部分时间可以保持在线，只需在迁移接近完成时关机以完成数据同步，对业务影响小。

---

## SMTX 迁移工具的版本配套说明

# SMTX 迁移工具的版本配套说明

在使用本版本的 SMTX 迁移工具进行虚拟机迁移前，请先了解该工具的版本配套说明。

---

## SMTX 迁移工具的版本配套说明 > 与服务器架构配套说明

# 与服务器架构配套说明

通过本版本的 SMTX 迁移工具执行迁移时，源端和目标端集群的节点支持的服务器架构如下。

| 源端集群节点 | 目标端集群节点 |
| --- | --- |
| Intel x86\_64 架构 | Intel x86\_64 架构 |
| Intel x86\_64 架构 | Hygon x86\_64 架构 |

---

## SMTX 迁移工具的版本配套说明 > 与 SMTX OS 或 SMTX ELF 版本配套说明

# 与 SMTX OS 或 SMTX ELF 版本配套说明

本版本的 SMTX 迁移工具支持以下版本的 SMTX OS（ELF）集群或 SMTX ELF 集群作为迁移的源端或目标端集群。

- **源端**：

  **SMTX OS（ELF）集群**：5.0.3 及以上的 5.x.x 和 6.x.x 版本
- **目标端**：

  - **SMTX OS（ELF）集群**：5.0.3 及以上的 5.x.x 和 6.x.x 版本
  - **SMTX ELF 集群**：6.0.0、6.2.0

---

## SMTX 迁移工具的版本配套说明 > 与 VMware vSphere 版本配套说明

# 与 VMware vSphere 版本配套说明

本版本的 SMTX 迁移工具支持从以下版本的 VMware ESXi 平台迁移虚拟机至 ELF 平台，并支持以下 vCenter 版本。

- ESXi 组件版本：5.0, 5.1, 5.5, 6.0, 6.5, 6.7, 7.0, 8.0
- vCenter 组件版本：6.0, 6.5, 6.7, 7.0, 8.0

---

## SMTX 迁移工具的版本配套说明 > 与虚拟机操作系统版本配套说明

# 与虚拟机操作系统版本配套说明

本版本的 SMTX 迁移工具不支持迁移 32 位操作系统的虚拟机。

本版本的 SMTX 迁移工具支持迁移操作系统版本和固件类型在《SMTX 迁移工具兼容性列表》上的虚拟机。您可单击[下载《SMTX 迁移工具 1.8.0 兼容性列表》](https://cdn.smartx.com/internal-docs/assets/5000be08/SMTX 迁移工具 1.8.0 兼容性列表.xlsx)，将文档下载至本地电脑查看。

对于操作系统版本和固件类型不在上述兼容性列表，但在 SMTX 虚拟机服务兼容性列表的 Windows 和 Linux 虚拟机也支持通过 SMTX 迁移工具迁移，但在迁移后可能将以 IDE 总线启动，需要手动安装 Virtio 驱动。

---

## 迁移虚拟机的要求

# 迁移虚拟机的要求

在部署 SMTX 迁移工具前，请先了解使用该工具迁移虚拟机的要求。

---

## 迁移虚拟机的要求 > 对迁移的源端和目标端的要求

# 对迁移的源端和目标端的要求

SMTX 迁移工具在不同迁移场景中对集群版本、待迁移虚拟机和目标端资源空间有不同的要求，如下。

---

## 迁移虚拟机的要求 > 对迁移的源端和目标端的要求 > 从 VMware ESXi 平台迁移虚拟机至 ELF 平台

# 从 VMware ESXi 平台迁移虚拟机至 ELF 平台

| 迁移要求 | 描述 |
| --- | --- |
| 对集群和虚拟机的版本配套要求 | 源端集群的 VMware vSphere 版本、待迁移虚拟机的固件类型和操作系统版本、以及目标端集群的 SMTX OS 或 SMTX ELF 版本为 [SMTX 迁移工具的版本配套说明](/smtxv2v/1.8.0/v2v_user_guide/v2v_userguide_09)中支持的版本。 |
| 对源端集群的许可要求 | 源端集群的 ESXi 主机使用的许可为非免费版。 |
| 对待迁移虚拟机的要求 | - 虚拟机处于`运行中`或`关机`状态。 - 已安装操作系统。 - 单个虚拟机的快照数量小于 32。 - 未配置 PCI 直通或 PCIe 直通。 - 单个虚拟机的虚拟磁盘数量不为 0。 - 虚拟磁盘文件为 `.vmdk` 格式。 - 若虚拟机正由依赖虚拟机快照功能的备份软件管理，则需要先停止对应的备份任务，然后再开始进行迁移。 - 若虚拟机挂载了 RDM 磁盘，请先将该磁盘移除，或者将虚拟机关机后再迁移。 - 若虚拟机挂载了共享属性为“多写入器”的磁盘，请先将共享属性修改为“未共享”后再迁移。 - 若虚拟机挂载了磁盘模式为“独立-持久”或“独立-非持久”的磁盘，请先将磁盘模式修改为“从属”，或者将虚拟机关机后再迁移。 - 若虚拟机的操作系统为 Linux 系统，且同时含有 SCSI 磁盘和 IDE 磁盘，且这些磁盘在虚拟机操作系统的 **/etc/fstab** 文件中的设备列是以盘符的形式写入的，请先将盘符更改为磁盘的 UUID 后再迁移。 - 虚拟机的 `/root` 分区容量大于 200 M，以用于 initramfs 备份。 |
| 对目标端资源空间的要求 | - 集群中可用的 CPU 资源足够支持迁移后的虚拟机正常运行。 - 集群的内存资源大于所有待迁移虚拟机的内存资源的总和。 - 集群中可用的数据空间大于预计需要的数据空间。 **不同存储策略对应的数据空间计算公式如下：**   - 冗余策略为**副本**:     - 置备方式为**精简置备**：预计需要数据空间 =（所有待迁移虚拟机的虚拟磁盘大小之和 + 5GiB）× 副本数     - 置备方式为**厚置备**：预计需要数据空间 =（所有待迁移虚拟机的虚拟磁盘大小之和 + 所有待迁移虚拟机的系统盘大小之和）× 副本数   - 冗余策略为**纠删码**（k + m）:     - 置备方式为**精简置备**：预计需要数据空间 =（所有待迁移虚拟机的虚拟磁盘大小之和 + 5GiB）× (k+m)/k     - 置备方式为**厚置备**：预计需要数据空间 =（所有待迁移虚拟机的虚拟磁盘大小之和 + 所有待迁移虚拟机的系统盘大小之和）× (k+m)/k 其中，“虚拟磁盘”包括数据盘和系统盘。目前，由于无法判断具体哪一块盘是系统盘，建议单个虚拟机的系统盘大小取该虚拟机中所有虚拟磁盘大小的平均值。 |

---

## 迁移虚拟机的要求 > 对迁移的源端和目标端的要求 > 在两个 ELF 平台之间相互迁移虚拟机

# 在两个 ELF 平台之间相互迁移虚拟机

| 迁移要求 | 描述 |
| --- | --- |
| 对集群的版本配套要求 | 源端和目标端集群的版本为 [SMTX 迁移工具的版本配套说明](/smtxv2v/1.8.0/v2v_user_guide/v2v_userguide_09)中支持的版本。 |
| 对待迁移虚拟机的要求 | - 已安装操作系统。 - 单个虚拟机的磁盘数量不为 0。 - 虚拟机的 `/root` 分区容量大于 200 M，以用于 initramfs 备份。 |
| 对目标端资源空间的要求 | - 集群中可用的 CPU 资源足够支持迁移后的虚拟机正常运行。 - 集群的内存资源大于所有待迁移虚拟机的内存资源的总和。 - 集群中可用的数据空间大于预计需要的数据空间。 **预计需要的数据空间计算公式：**  预计需要数据空间 = 所有待迁移虚拟机的磁盘大小之和 × 副本数 |

---

## 迁移虚拟机的要求 > 对网络环境的要求

# 对网络环境的要求

- SMTX 迁移工具必须连通源端和目标端集群的管理网络，当目标端集群为 SMTX ELF 集群时，SMTX 迁移工具还必须连通 SMTX ELF 集群关联的 SMTX ZBS 集群的接入网络。

  若要加速数据迁移，可以配置 SMTX 迁移工具与目标端的 SMTX OS（ELF）集群的存储网络或 SMTX ELF 集群的存储接入网络连通，以通过存储网络或存储接入网络传输数据。
- 若目标端集群已配置接入网络，请为 SMTX 迁移工具配置与目标端集群连通的接入网络，以访问 iSCSI 存储进行驱动注入。
- 若要迁移 VMware ESXi 平台的虚拟机至 ELF 平台，迁移虚拟机前，请根据目标端集群的类型，检查相应主体是否已开启防火墙，若已开启，请确保防火墙已开启相应的 TCP 端口。

  - SMTX OS（ELF）集群

    | 主体 | 需开通的 TCP 端口 | 描述 |
    | --- | --- | --- |
    | vCenter Server | 80, 443 | 用于 SMTX 迁移工具与 vCenter Server 通信 |
    | ESXi 主机 | 902 | 用于 SMTX 迁移工具与 ESXi 之间传输迁移数据 |
    | SMTX OS (ELF) 集群的主机 | 80, 443 | 用于 SMTX 迁移工具与 SMTX 虚拟机服务通信 |
    | 860, 3260, 3261 | 用于 SMTX 迁移工具与 iSCSI 服务之间通信 |
    | 10200 ~ 10207 | 用于 SMTX 迁移工具与块存储服务之间传输迁移数据以及通信 |
  - SMTX ELF 集群

    | 主体 | 需开通的 TCP 端口 | 描述 |
    | --- | --- | --- |
    | vCenter Server | 80, 443 | 用于 SMTX 迁移工具与 vCenter Server 通信 |
    | ESXi 主机 | 902 | 用于 SMTX 迁移工具与 ESXi 之间传输迁移数据 |
    | SMTX ELF 集群的主机 | 80, 443 | 用于 SMTX 迁移工具与 SMTX 虚拟机服务通信 |
    | SMTX ELF 集群关联的 SMTX ZBS 集群的主机 | 860, 3260, 3261 | 用于 SMTX 迁移工具与 iSCSI 服务之间通信 |
    | 10200 ~ 10207 | 用于 SMTX 迁移工具与块存储服务之间传输迁移数据以及通信 |

---

## 迁移虚拟机的局限

# 迁移虚拟机的局限

- SMTX 迁移工具单次最多可创建 30 个迁移任务，执行迁移任务时最多可以同时迁移 5 台虚拟机。
- 迁移完成后，虚拟机的部分配置可能发生改变：

  - 若源端虚拟机挂载了 CD-ROM 设备，则迁移后的虚拟机将不包含此设备。
  - 迁移后虚拟磁盘的编号顺序可能改变，且虚拟磁盘的容量大小将向上取整，例如，虚拟磁盘在迁移前的容量为 4.2 GB，则在迁移后容量将变为 5 GB。
- 迁移完成后，已开启高可用（HA）的虚拟机的重建优先级可能发生改变：当目标集群的版本低于 6.0.0 时，虚拟机将不包含重建优先级信息；当目标集群为 6.0.0 及以上版本时，虚拟机的重建优先级将设置为默认优先级（中级）。
- 迁移完成后，虚拟机的自动开机选项可能发生改变：当目标集群的版本低于 6.0.0 时，虚拟机将不包含自动开机选项信息；当目标集群为 6.0.0 及以上版本时，虚拟机的自动开机选项默认禁用。

---

## 部署 SMTX 迁移工具

# 部署 SMTX 迁移工具

SMTX 迁移工具可以部署在源端或目标端集群的虚拟机上，为加快数据传输，一般推荐在源端集群部署。

用户可以采用以下两种方式部署 SMTX 迁移工具：

- **通过 ISO 映像文件部署 SMTX 迁移工具**

  用户需在集群中创建虚拟机并挂载 ISO 映像文件，并手动在虚拟机中安装含有 SMTX 迁移工具的操作系统。
- **通过 OVF 文件部署 SMTX 迁移工具**

  用户无需手动安装 SMTX 迁移工具，直接通过 OVF 文件导入已安装 SMTX 迁移工具的虚拟机。

  > **说明**：
  >
  > 选择通过 OVF 文件部署 SMTX 迁移工具的方式效率更高，但在以下场景中，只能选择通过 ISO 映像文件部署 SMTX 迁移工具：
  >
  > - 用户需要自定义安装 SMTX 迁移工具的虚拟机的部分配置时，例如：磁盘大小、启动方式等。
  > - 待部署 SMTX 迁移工具的集群未与 CloudTower 关联。

下文将对两种部署方式进行详细介绍。

---

## 部署 SMTX 迁移工具 > 通过 ISO 映像文件部署 SMTX 迁移工具

# 通过 ISO 映像文件部署 SMTX 迁移工具

当用户选择通过 ISO 映像文件部署 SMTX 迁移工具时，需要在集群中按照推荐配置创建部署 SMTX 迁移工具的虚拟机，并手动在虚拟机中安装含有 SMTX 迁移工具的操作系统。

---

## 部署 SMTX 迁移工具 > 通过 ISO 映像文件部署 SMTX 迁移工具 > 创建部署 SMTX 迁移工具的虚拟机

# 创建部署 SMTX 迁移工具的虚拟机

**虚拟机的推荐配置**

在不同的虚拟化平台上创建虚拟机时，虚拟机的推荐配置如下：

- VMware ESXi 平台：

  - 客户机操作系统及版本：Linux，CentOS 7（64 位）
  - CPU：6
  - 内存：6 GB
  - 硬盘：30 GB
  - 网络适配器：至少 1 个
- ELF 平台：

  - 客户机操作系统类型：Linux
  - vCPU：6
  - 内存：6 GiB
  - 磁盘：30 GiB
  - 磁盘总线：VIRTIO
  - 虚拟网卡：至少 1 个
  - 虚拟网卡模式：VIRTIO

**操作步骤**

1. 将 SMTX 迁移工具的 ISO 映像文件上传至待部署的集群中。
2. 根据以上虚拟机的推荐配置创建空白虚拟机，并挂载 SMTX 迁移工具的 ISO 映像文件。

---

## 部署 SMTX 迁移工具 > 通过 ISO 映像文件部署 SMTX 迁移工具 > 安装 SMTX 迁移工具

# 安装 SMTX 迁移工具

1. 创建完虚拟机后，打开虚拟机控制台，选中 **Install SMTX-V2V OS**，单击 **Enter** 键。

   ![](https://cdn.smartx.com/internal-docs/assets/e4a61e8a/v2v_userguide_01.png)
2. 根据如下磁盘总线类型输入对应的安装盘，再单击 **Enter** 键。

   - Virtio：vda
   - SCSI：sda
   - IDE：hda

   ![](https://cdn.smartx.com/internal-docs/assets/e4a61e8a/v2v-disk.png)

   若 10 秒内未输入安装盘，则安装程序会自动选择一个磁盘进行安装，该磁盘为运行 `lsblk | grep disk` 命令后列出的第一个磁盘。
3. 等待自动安装完成后，用默认账户 `root` 登录 SMTX 迁移工具的操作系统。
4. 登录成功后，配置各个网卡的 IP 和网关，使 SMTX 迁移工具连通源端和目标端集群的管理网络，当目标端集群为 SMTX ELF 集群时，还需要连通 SMTX ELF 集群关联的 SMTX ZBS 集群的接入网络。若在此处没有手动配置网卡，则系统会默认使⽤ DHCP ⾃动获取⽹络配置。

   > **注意**：
   >
   > - SMTX 迁移工具的操作系统是基于 OpenEuler 20.03 开发的，请用 OpenEuler 20.03 的命令行来配置网卡。
   > - 若源端集群的 ESXi 主机以域名的形式添加，则还需要在此处配置 DNS 服务器，并确保其能正确解析相关域名地址。用户也可以在 SMTX 迁移工具部署完成后，再参考[检查 DNS 服务器](/smtxv2v/1.8.0/v2v_user_guide/v2v_userguide_04#%E6%A3%80%E6%9F%A5-dns-%E6%9C%8D%E5%8A%A1%E5%99%A8)进行操作。
   > - 若要加速数据迁移，可以在此处配置网卡连通 SMTX OS（ELF）集群的存储网络或 SMTX ELF 集群的存储接入网络。对于在 ELF 平台部署的虚拟机，需要先添加存储网卡（存储网络的 VLAN ID 必须为 0），再配置各个网卡的 IP 和网关，使 SMTX 迁移工具连通源端和目标端的管理网络，以及连通 SMTX OS（ELF）集群的存储网络或 SMTX ELF 集群的存储接入网络，以加速迁移。
5. 网络配置完成后，用浏览器访问 SMTX 迁移工具的 IP 地址。若看到如下欢迎界面，则表示部署成功，接着单击**同意协议并进入下一步**。

   ![](https://cdn.smartx.com/internal-docs/assets/e4a61e8a/v2v-deploy-end.png)
6. 部署成功后，在**创建账户**界面，输入用户名和密码，单击**创建并登录**，登录 SMTX 迁移工具。

   若在后续操作中忘记了在此处创建的用户名或密码，可以[重置 SMTX 迁移工具账户](/smtxv2v/1.8.0/v2v_user_guide/v2v_userguide_10)。

---

## 部署 SMTX 迁移工具 > 通过 OVF 文件部署 SMTX 迁移工具

# 通过 OVF 文件部署 SMTX 迁移工具

**前提条件**

- 若在 ELF 平台上导入 OVF 虚拟机，需提前将待部署 SMTX 迁移工具的集群和 CloudTower 关联。
- 请提前获取 OVF 文件，包括 `.ovf` 格式的文件和 `.vmdk` 格式的文件。

**虚拟机的推荐配置**

在不同的虚拟化平台上导入 OVF 虚拟机时，虚拟机的推荐配置如下：

- VMware ESXi 平台：

  按照界面指示进行配置即可。
- ELF 平台：

  - vCPU：6
  - 内存：6 GiB
  - 磁盘总线：VIRTIO
  - 虚拟网卡：至少 1 个
  - 虚拟网卡模式：VIRTIO

**操作步骤**

1. 若在 ELF 平台上导入 OVF 虚拟机，则在待部署 SMTX 迁移工具的集群界面单击右上角 **+ 创建**，选择**导入虚拟机**，弹出导入虚拟机对话框。

   若在 VMware ESXi 平台上导入 OVF 虚拟机，则在待部署 SMTX 迁移工具的集群界面单击左上角**操作**，选择**部署 OVF 模版**，弹出部署 OVF 模版对话框。
2. 上传提前获取的 OVF 文件，并按照上述推荐配置导入 OVF 虚拟机。
3. 导入 OVF 虚拟机后，打开虚拟机控制台，用默认账户 `root` 登录 SMTX 迁移工具的操作系统。
4. 登录成功后，配置各个网卡的 IP 和网关，使 SMTX 迁移工具连通源端和目标端集群的管理网络。当目标端集群为 SMTX ELF 集群时，还需要连通 SMTX ELF 集群关联的 SMTX ZBS 集群的接入网络。若在此处没有手动配置网卡，则系统会默认使⽤ DHCP ⾃动获取⽹络配置。

   > **注意**：
   >
   > - SMTX 迁移工具的操作系统是基于 OpenEuler 20.03 开发的，请用 OpenEuler 20.03 的命令行来配置网卡。
   > - 若源端集群的 ESXi 主机以域名的形式添加，则还需要在此处配置 DNS 服务器，并确保其能正确解析相关域名地址。用户也可以在 SMTX 迁移工具部署完成后，再参考[检查 DNS 服务器](/smtxv2v/1.8.0/v2v_user_guide/v2v_userguide_04#%E6%A3%80%E6%9F%A5-dns-%E6%9C%8D%E5%8A%A1%E5%99%A8)进行操作。
   > - 若要加速数据迁移，可以在此处配置网卡连通 SMTX OS（ELF）集群或 SMTX ELF 集群的存储接入网络。对于在 ELF 平台部署的虚拟机，需要先添加存储网卡（存储网络的 VLAN ID 必须为 0），再配置各个网卡的 IP 和网关，使 SMTX 迁移工具连通源端和目标端的管理网络，以及连通 SMTX OS（ELF）集群或 SMTX ELF 集群的存储接入网络，以加速迁移。
5. 网络配置完成后，用浏览器访问 SMTX 迁移工具的 IP 地址。若看到如下欢迎界面，则表示部署成功，接着单击**同意协议并进入下一步**。

   ![](https://cdn.smartx.com/internal-docs/assets/e4a61e8a/v2v-deploy-end.png)
6. 部署成功后，在**创建账户**界面，输入用户名和密码，单击**创建并登录**，登录 SMTX 迁移工具。

   若在后续操作中忘记了在此处创建的用户名或密码，可以[重置 SMTX 迁移工具账户](/smtxv2v/1.8.0/v2v_user_guide/v2v_userguide_10)。

---

## 迁移前的检查

# 迁移前的检查

部署完 SMTX 迁移工具后，在开始迁移任务前，为确保能成功迁移虚拟机，请先检查以下项目：

## 检查浏览器

确认已下载 Google Chrome 浏览器，用于访问 SMTX 迁移工具的网页界面。

## 检查 DNS 服务器

若集群的 ESXi 主机以域名形式添加，请确认已在 SMTX 迁移工具中配置 DNS 服务器以解析域名地址。否则，请参考下述步骤进行配置：

1. 单击 SMTX 迁移工具界面右上角的![](https://cdn.smartx.com/internal-docs/assets/e4a61e8a/DNS.png)图标，选择**配置 DNS 服务器**。
2. 在弹出的对话框中，输入待解析的服务器地址，单击**保存**。

## 检查 CPU 兼容性

若部署 SMTX 迁移工具的集群的虚拟化平台为 ELF 平台，则请确保已安装 SMTX 迁移工具的虚拟机的 CPU 兼容性为**物理机透传**，或者满足下表中对应的微架构最低要求。若部署 SMTX 迁移工具的集群的虚拟化平台为 VMware ESXi 平台，则请确保已安装 SMTX 迁移工具的虚拟机的 CPU 兼容性满足下表中对应的微架构最低要求。

| 虚拟机所属集群的服务器的 CPU 架构 | 微架构最低要求 |
| --- | --- |
| Intel x86\_64 | Sandy Bridge |
| Hygon x86\_64 | Opteron\_G4 |

若不满足，请参考下述步骤进行修改：

1. 确认虚拟机处于**关机**状态后，在虚拟机列表中选中虚拟机，弹出虚拟机详情面板。
2. 在虚拟机详情面板中的**高级**区域，单击 **CPU 兼容性**右侧的编辑按钮，弹出**编辑虚拟机 CPU 兼容性**对话框。
3. 在对话框中勾选单独为虚拟机指定 CPU 兼容性，并选择**物理机透传**，或根据上表选择相应的微架构。

---

## 迁移虚拟机

# 迁移虚拟机

完成[迁移前的检查](/smtxv2v/1.8.0/v2v_user_guide/v2v_userguide_04)后，即可参考后续步骤迁移虚拟机。SMTX 迁移工具在迁移虚拟机时，首先将对待迁移的虚拟机进行一次全量数据传输，全量数据传输完成后，若源端虚拟机处于开启状态，则用户可选择迁移增量数据或关闭虚拟机。

- 迁移增量数据

  在完成全量数据传输后，若用户无法及时关闭或忘记关闭源端虚拟机，则源端虚拟机将会生成大量增量数据。用户可选择手动迁移增量数据，在源端虚拟机关机前先进行增量数据的传输，以减少源端虚拟机关机后的数据传输时间。
- 关闭虚拟机

  关闭源端虚拟机，以完成最后的数据迁移。

**前提条件**

- 若源端或目标端集群的虚拟化平台为 ELF 平台，则请提前获取 root 账号密码。
- 请提前获取对应的 VMware vCenter 平台中对待迁移的虚拟机具有管理员角色的用户的名称和密码。可以参考 VMware 文档中的 [vCenter Server 系统角色](https://docs.vmware.com/cn/VMware-vSphere/7.0/com.vmware.vsphere.security.doc/GUID-93B962A7-93FA-4E96-B68F-AE66D3D6C663.html)章节了解“管理员角色”。

**注意事项**

在迁移任务开始和结束时，SMTX 迁移工具将分别对迁移虚拟机创建和删除快照。创建和删除快照的过程中可能会短暂地出现迁移虚拟机被冻结和性能下降的现象，从而影响运行在其上的业务。因此，建议您在业务空闲时段进行虚拟机迁移操作。

---

## 迁移虚拟机 > 添加站点

# 添加站点

当面临以下场景时，需要添加站点：

- 迁移工具中没有本次迁移的源端站点或目标站点。
- 迁移工具中已有本次迁移的源端站点，但在站点中填写的管理员账户下没有本次要迁移的虚拟机，可以再添加一次源端站点，并填写对要迁移的虚拟机具有管理员角色的账号。

**操作步骤**

1. 登录 SMTX 迁移工具，进入**站点**界面，在界面右上角单击**添加站点**，根据迁移的源端或目标端集群类型选择站点类型。

   - **VMware vCenter**：使用 VMware ESXi 平台的集群所对应的站点类型。
   - **SMTX 虚拟机服务集群**：SMTX OS（ELF）集群或 SMTX ELF 集群所对应的站点类型。
2. 在弹出的**添加站点**窗口中，根据所选的站点类型填写站点信息，完成后单击**添加站点**。

   | 站点类型 | 字段 | 说明 |
   | --- | --- | --- |
   | VMware vCenter | vCenter 地址 | 输入 vCenter 平台的 IP 地址和端口号。  如果填写的端口为加密端口，需要勾选**加密连接**。 |
   | 管理员用户名和密码 | 输入 vCenter 平台中，对要迁移的虚拟机具有管理员角色的用户的名称和密码。 |
   | 描述（选填） | 输入关于站点的描述。 |
   | SMTX 虚拟机服务集群 | 集群地址 | 输入 SMTX OS（ELF）集群或 SMTX ELF 集群的管理虚拟 IP 和端口号。  如果填写的端口为加密端口，需要勾选**加密连接**。 |
   | 管理员用户名和密码 | 输入 SMTX OS（ELF）集群或 SMTX ELF 集群的超级管理员的用户名（root）和密码。 |
   | 描述（选填） | 输入关于站点的描述。 |

   如果添加站点失败，可以查看窗口左下角提示的失败原因或者参考[添加站点失败，该怎么办？](/smtxv2v/1.8.0/v2v_user_guide/v2v_userguide_12)排查问题。请解决问题后再重新添加站点。
3. 重复以上步骤，直至本次迁移所需的站点均已添加完毕。

   添加完毕后，在**站点**界面可以编辑或删除已添加的站点。

---

## 迁移虚拟机 > 创建迁移任务

# 创建迁移任务

在 SMTX 迁移工具的**任务队列**界面的右上角单击**创建任务**，进入**创建迁移任务**界面后，根据 SMTX 迁移工具的引导完成以下 4 步配置，在界面右侧可查看已选择的项目。

**注意事项**

从创建迁移任务开始至迁移完成的期间，请勿对待迁移的虚拟机进行编辑操作，如增加或删除磁盘、删除虚拟机、删除虚拟机快照等，否则将导致迁移失败。

---

## 迁移虚拟机 > 创建迁移任务 > 第 1 步：选择源端和目标端

# 第 1 步：选择源端和目标端

1. 从已添加的站点中选择一个作为源端站点。当选择的站点类型为 VMware vCenter 站点时，请继续选择待迁移虚拟机所属的 vCenter 数据中心。
2. 从已添加的 SMTX 虚拟机服务集群站点中选择一个作为目标端站点。

   > **说明**：
   >
   > 当选择的目标端站点为 6.1.0 及以上版本的 SMTX ELF 集群，且关联了多个 SMTX ZBS 集群时，还需选择目标端站点关联的 SMTX ZBS 集群。
3. 单击**下一步**。

---

## 迁移虚拟机 > 创建迁移任务 > 第 2 步：选择待迁移的虚拟机

# 第 2 步：选择待迁移的虚拟机

1. 选择虚拟机所在的主机或集群，再在搜索框中输入虚拟机的名称（支持搜索中文名称）或 UUID 搜索待迁移的虚拟机，然后在虚拟机列表中单击 “+” 号添加一个或多个虚拟机。

   > **注意**：
   >
   > 若待迁移的虚拟机所属平台为 VMware ESXi，则请确保虚拟机的版本为 7.0 及以上，否则迁移任务将创建失败。
2. 在界面底部查看在此次迁移中，设置不同冗余策略时所需的数据空间（默认按虚拟机迁移后使用“精简置备”的置备策略计算），以及预计需要的内存，检查目标端可用的资源是否足够。

   > **说明**：
   >
   > - 若界面显示数据空间为 0，请检查浏览器缓存并刷新数据。
   > - 当选择的目标端为 SMTX ELF 集群时，若界面提示`获取可用资源失败`，请检查 SMTX 迁移工具和 SMTX ELF 集群关联的 SMTX ZBS 集群的接入网络是否连通。
3. 单击**下一步**。

---

## 迁移虚拟机 > 创建迁移任务 > 第 3 步：设置虚拟网络

# 第 3 步：设置虚拟网络

1. 为待迁移虚拟机所关联的每一个虚拟网络，分别指定一个目标端虚拟网络，建立映射关系。

   虚拟机迁移后，源端虚拟网络的网口将按照这一步设置的映射关系关联至对应的目标端虚拟网络。

   即使待迁移虚拟机没有虚拟网卡，也需要指定一个映射的目标端网络，迁移后的虚拟机将关联到该指定网络。
2. 单击**下一步**。

---

## 迁移虚拟机 > 创建迁移任务 > 第 4 步：自定义虚拟机配置项

# 第 4 步：自定义虚拟机配置项

当同时迁移多个虚拟机时，可以在操作窗口的左上方单击**批量编辑**，一次性按以下操作步骤设置所有虚拟机的配置项。

1. 为虚拟机选择迁移后适用的存储策略。目标端的 SMTX 虚拟机服务将按照此处设置的存储策略来创建虚拟卷。

   - **冗余策略**

     - 副本：包括 `2 副本`和 `3 副本`。
     - 纠删码：系统会根据迁移后集群内的节点数默认选择推荐的纠删码配比，您也可以单击下拉框重新进行选择。

       > **说明**：
       >
       > 若目标端为双活集群，则仅支持选择 3 副本的冗余策略。
   - **置备方式**：包括`精简置备`和`厚置备`。
   - **数据加密**：当目标集群为 6.2.0 及以上版本的 SMTX OS（ELF）集群或 SMTX ELF 集群，且目标集群已启用数据加密时，您还需选择是否为虚拟卷启用数据加密。启用后，数据写入虚拟卷后将自动被加密。若目标集群版本为 6.3.0 及以上，您还需要选择加密算法，可选择的加密算法和集群启用加密时选择的密钥管理服务有关，详情请参考 《SMTX OS 管理指南》的**管理静态数据加密**章节。

   在界面底部的`预计需要数据空间`数值会根据所选的存储策略进行更新。若该数据显示为 0，请检查浏览器缓存并刷新数据。
2. 选择是否为虚拟机迁移后的虚拟网卡进行以下配置。

   - **手动配置静态 IP**（仅当目标端存有 SMTX VMTools 映像时展示该选项）：勾选该项后，可手动配置网卡的 IP、子网掩码和网关。

     当源端虚拟机安装了 VMware Tools，且处于开机状态时，勾选该项后会自动填写源端虚拟机网卡的 IP、子网掩码和网关。用户也可手动修改这些信息，在选项右侧单击**置为源虚拟机 IP** 则将重置为源端虚拟机网卡的信息。配置完成后，若可以获取到源端虚拟机的 DNS 配置，则该配置也将被保留。

     > **注意**：
     >
     > - 由于网卡的命名规则在 VMware ESXi 与 ELF 两种虚拟化平台中存在差异，所以当迁移 VMware ESXi 平台的虚拟机至 ELF 平台时，网卡名称可能发生变化而导致原来的网卡配置文件不生效。因此，若要保留原有的或设置新的网卡配置，建议勾选该项进行设置。
     > - 若勾选该项，则在迁移完成后，虚拟机会自动开机并安装 SMTX VMTools。安装完成后，SMTX VMTools ISO 映像将自动被弹出。
     > - 在迁移完成后，若目标端虚拟机的虚拟网卡的静态 IP 未生效，请检查虚拟网卡的配置文件内容是否正确。
     > - 若源端虚拟机安装了 VMware Tools，则在迁移完成后目标端虚拟机将自动卸载 VMware Tools。支持的虚拟机操作系统版本请参考《SMTX 迁移工具 1.8.0 兼容性列表》。
   - **保留 MAC 地址**：勾选该项后，可保留源端虚拟网卡的 MAC 地址。

     > **注意**：
     >
     > 勾选该项后，若源端和目标端的虚拟机处于同一个局域网中，则在迁移完成后，应避免两个虚拟机同时处于开机状态，否则对这两个虚拟机的网络访问会出现故障。
3. 配置迁移选项：

   - **进行数据校验**：若勾选该选项，则在数据传输完成后将进行数据校验，该校验将导致源端虚拟机关机的时间较长。数据校验的时间与 SMTX 迁移工具实际迁移的数据量有关，数据量越大，校验时间越长。
   - **完成后自动开机**：若勾选该选项，则虚拟机迁移完成后将自动开机。
   - **限制传输速率**：勾选并设置限制传输速率值，设置后数据传输速率将被限制在设置值以内。
4. 单击**创建**。

创建完迁移任务后，会自动跳转到**任务队列**界面，该界面展示了迁移任务的执行状态，可参考[管理执行中的迁移任务](/smtxv2v/1.8.0/v2v_user_guide/v2v_userguide_25)小节对迁移任务进行相应操作。

> **说明**：
>
> 若迁移任务因虚拟机的快照未启用 CBT 而失败，则请根据提示删除虚拟机中的所有快照之后，再重新进行迁移。

---

## 迁移虚拟机 > 迁移增量数据（仅源端虚拟机开启时操作）

# 迁移增量数据（仅源端虚拟机开启时操作）

在完成全量数据传输后，若用户无法及时关闭或忘记关闭源端虚拟机，则源端虚拟机将会生成大量增量数据。用户可选择手动迁移增量数据，在源端虚拟机关机前先进行增量数据的传输，以减少源端虚拟机关机后的数据传输时间。若无需迁移增量数据，可直接[关闭源端虚拟机](/smtxv2v/1.8.0/v2v_user_guide/v2v_userguide_26)，以进行最终的数据同步。

具体操作如下：

1. 先确认需要对哪些迁移任务的源端虚拟机进行迁移增量数据的操作，再执行相应操作。

   - 迁移单个源端虚拟机的增量数据：在任务条目中单击**迁移增量数据**。
   - 批量迁移多个迁移任务的源端虚拟机的增量数据：勾选待迁移增量数据的迁移任务的任务条目，在右上方单击 **...**，选择**迁移增量数据**。
   - 迁移所有迁移任务的源端虚拟机的增量数据：在界面顶部的横幅右侧单击**查看**，并选择**迁移增量数据**。
2. 选择循环增量迁移源端虚拟机的方式：

   - **迁移增量数据**：执行增量数据迁移。单次增量数据迁移任务完成后，您可以选择继续迁移增量数据，或者[关闭源端虚拟机](/smtxv2v/1.8.0/v2v_user_guide/v2v_userguide_26)以完成最终数据同步。
   - **迁移增量数据并自动关机**：该选项仅在源端虚拟机已安装 VMware Tools 时支持选择。选择后，源端虚拟机在增量数据迁移完成后将自动关机。关机后，迁移工具将开始进行最终的数据同步。

单击迁移增量数据后，迁移任务条目下方将展示执行状态，您可参考[管理执行中的迁移任务](/smtxv2v/1.8.0/v2v_user_guide/v2v_userguide_25)小节对迁移任务进行相应操作。

单次增量数据迁移完成后，您可以选择继续迁移增量数据或[关闭源端虚拟机](/smtxv2v/1.8.0/v2v_user_guide/v2v_userguide_26)以完成最终数据同步。

---

## 迁移虚拟机 > 管理执行中的迁移任务

# 管理执行中的迁移任务

**任务队列**界面显示所有正在执行的迁移任务，包括全量数据传输和增量数据传输。移动鼠标至迁移任务条目右上方的 **...** 图标处，可以选择进行以下操作。

- **详情**：可以查看迁移虚拟机相关的 CPU、内存和数据空间占用等信息。
- **编辑限速**：若在创建迁移任务时，未启用限速功能，则您可以在迁移任务执行过程中启用并设置限制数据传输速率；若已启用限速功能，则您可以编辑限速值，或将该选项留空以取消限速。
- **暂停**/**继续**：暂停/恢复执行迁移任务。迁移任务处于数据传输开始前的准备过程时，可能无法暂停迁移任务。如在刚创建迁移任务，或者刚从暂停状态恢复迁移时。
- **停止**：取消迁移任务。迁移任务处于数据传输开始前的准备过程时，可能无法取消迁移任务。如在刚创建迁移任务，或者刚从暂停状态恢复迁移时。

  > **警告**：
  >
  > 迁移任务停止后不可恢复执行，操作请谨慎。
- **重试**（仅当迁移任务失败时展示）：重新执行迁移任务。迁移任务失败后，将展示数据传输失败的虚拟机，可单击**重试**，重新迁移数据传输失败的虚拟机的数据。

若要批量管理迁移任务，可以勾选任务条目前的复选框，再在界面右上方单击**暂停/继续**或**停止**。

---

## 迁移虚拟机 > 关闭源端虚拟机（仅源端虚拟机开启时操作）

# 关闭源端虚拟机（仅源端虚拟机开启时操作）

**注意事项**

若在迁移增量数据时选择了**迁移增量数据并自动关机**，则无需执行本操作。

**操作步骤**

1. 先确认要关闭哪些迁移任务的源端虚拟机，再执行相应操作。

   - 关闭单个迁移任务的源端虚拟机：在任务条目中单击**关闭源端虚拟机**。
   - 关闭所选迁移任务的源端虚拟机：勾选要关闭源端虚拟机的任务条目，在右上方单击 **...**，选择**关闭源端虚拟机**。
   - 关闭所有迁移任务的源端虚拟机：在界面顶部的横幅右侧单击**查看**，弹出**了解进一步操作**对话框。
2. 选择关闭源端虚拟机的方式。

   - **手动在源端站点上关闭虚拟机（推荐）**：登录源端站点，手动从操作系统层面关闭源端虚拟机。源端虚拟机关机成功后，单击**确认已关机**。
   - **通过迁移工具强制关闭源端虚拟机**：确认要关闭的虚拟机后，单击**强制关机**或**批量强制关机**，SMTX 迁移工具自动将源端虚拟机断电。
3. 确认源端虚拟机关机成功后，单击**确认已关机**。

确认关机后，SMTX 迁移工具将开始进行最终的数据同步。

---

## 迁移虚拟机 > 确认目标端虚拟机

# 确认目标端虚拟机

数据迁移完成后，请在目标端集群检查迁移后的虚拟机能否正常运作及非系统盘是否自动上线。

> **说明**：
>
> 若在 CloudTower 的虚拟机列表中未发现迁移后的虚拟机，可能是由于 CloudTower 未及时同步集群信息造成的。请在虚拟机列表上方单击刷新按钮以同步虚拟机数据，然后再重新确认。

- 若确认虚拟机运作正常且非系统盘已自动上线，则请单击**是，完成迁移任务**，迁移任务结束。
- 若确认虚拟机无法正常运作，则请先确认该虚拟机的操作系统版本和固件类型是否在 《SMTX 迁移工具兼容性列表》上：

  - **不在兼容性列表上**

    如果虚拟机的操作系统版本和固件类型不在兼容性列表上，则虚拟机无法正常运作可能是因为 Virtio 驱动注入失败，请按以下步骤操作。

    1. 单击**否，选择处理方式** > **重新创建未注入驱动的虚拟机**。

       SMTX 迁移工具将停止注入 Virtio 驱动，并在目标端创建一个名称带有 `retry` 字段的虚拟机，该虚拟机的磁盘使用 IDE 总线。
    2. 带有 `retry` 字段的虚拟机创建完成后，启动该虚拟机。

       - 如果虚拟机可以正常运作，请选择**是，完成迁移任务**，然后为虚拟机手动安装 Virtio 驱动，可以参考[为迁移或导入到 ELF 平台的虚拟机安装 Virtio 驱动](/smtxv2v/1.8.0/v2v_user_guide/administration_guide_097)进行操作。
       - 如果虚拟机无法正常运作，请勿单击任何按钮，以在任务队列中保留此任务，然后请直接联系售后技术支持排查该问题。
  - **在兼容性列表上**

    如果虚拟机的操作系统版本和固件类型在兼容性列表上，请勿单击任何按钮，以在任务队列中保留此任务，然后请直接联系售后技术支持排查该问题。
- 若 Windows 虚拟机的非系统盘未自动上线，则请先在硬盘管理器中手动上线，然后在 `cmd.exe` 中依次执行以下命令以将磁盘上线策略设置为 `OnlineAll`：

  ```
  Diskpart
  SAN Policy=OnlineAll
  ```

迁移任务完成后，任务详情将保存在**历史记录**界面，包括迁移任务用时情况、数据空间占用、总传输数据量等信息。

> **说明**：
>
> `总传输数据量`即 SMTX 迁移工具实际迁移的数据量。如果`总传输数据量`小于`数据空间占用`的值，可能是由于 SMTX 迁移工具实际仅迁移源虚拟机磁盘的有效数据。仅迁移有效数据的情况如下：
>
> - 虚拟机的源端为 VMware ESXi 6.x / 7.x / 8.x 平台，平台使用 VMFS、vSAN 或 VVol 的数据存储，且虚拟机的虚拟磁盘使用“精简置备“或”厚制备延迟置零“的置备策略。
> - 虚拟机的源端为 VMware ESXi 5.x 平台，平台使用 VMFS 的数据存储，且虚拟机的虚拟磁盘使用“精简置备“或”厚制备延迟置零“的置备策略。

---

## 重置 SMTX 迁移工具账户

# 重置 SMTX 迁移工具账户

如果忘记 SMTX 迁移工具的用户名或密码，可以重置密码，或重置用户名和密码。

**操作步骤**

以 root 用户登录 SMTX 迁移工具的操作系统，输入以下命令：

```
v2v-manage reset-v2v-user <username> <password>
```

其中，*`<username>`* 为需要重置密码的用户名或新的用户名；*`<password>`* 为新的密码。

示例：在以下示例中，SMTX 迁移工具用户 `migration-admin` 的密码被成功重置为 `abx123`。

```
[root@localhost ~]# v2v-manage reset-v2v-user migration-admin abx123
[7356] 2019-07-30 08:47:41,820, INFO, command.py:35, reset user successful!!!!
```

---

## 附录 > 为迁移或导入到 ELF 平台的虚拟机安装 Virtio 驱动

# 为迁移或导入到 ELF 平台的虚拟机安装 Virtio 驱动

部分虚拟机从非 KVM 平台迁移或导入到 ELF 平台后，无法自动安装 Virtio 驱动，为使虚拟机获得更好的性能，需要手动安装 Virtio 驱动。下文介绍了为各种操作系统的虚拟机手动安装 Virtio 驱动的操作方法。

---

## 附录 > 为迁移或导入到 ELF 平台的虚拟机安装 Virtio 驱动 > Windows 系统操作指导

# Windows 系统操作指导

**前提条件**

- 当前 CloudTower 的内容库中已有 Virtio 驱动的 ISO 映像（推荐使用 virtio-win-0.1.185 版本，但对于 Windows Server 2008 R2 及以下版本，建议使用 virtio-win-0.1.160 版本）。
- 确保已关闭所有防病毒软件或入侵检测软件，若有需要，可以在安装完 Virtio 驱动后再启用这些软件。

**操作步骤**

1. 检查虚拟机是否已关机，若未关机，先将虚拟机关机。
2. 单击虚拟机，在弹出的虚拟机详情面板中，在**磁盘**字段右侧单击**编辑**。
3. 在弹出的**编辑磁盘**窗口中，检查所有磁盘的总线是否为 **IDE**，若不是，先更改为 **IDE**。
4. 新建一个虚拟卷，总线选择 **VIRTIO**，其他设置可保留默认设置。
5. 挂载一个 CD-ROM，选择 Virtio 驱动的 ISO 映像进行添加，单击**保存**。
6. 在虚拟机详情面板中，在**网络设备**字段右侧单击**编辑**，在弹出的**编辑虚拟机网络设备**窗口中，检查是否有模式为 **VIRTIO** 的网卡，若没有，需要添加一个虚拟网卡，并将其模式设置为 **VIRTIO**。
7. 等待虚拟机完成更新后，单击虚拟机，在弹出的虚拟机详情面板中，单击**开机**。
8. 虚拟机启动后，单击**打开终端**，进入虚拟机操作界面，登录虚拟机后，打开虚拟机的设备管理器，更新 Virtio 磁盘驱动和网卡驱动。

   - **更新 Virtio 磁盘驱动**

     1. 在设备管理器窗口中，展开**其他设备**，右键单击 **SCSI 控制器**，选择**更新驱动程序软件**。

        ![](https://cdn.smartx.com/internal-docs/assets/8f96e4d9/administration_guide_024.png)
     2. 在弹出的**更新驱动程序软件**窗口中，单击**浏览计算机以查找驱动程序软件**，选择 Virtio 驱动的 CD 驱动器，单击**确定**，单击**下一步**。

        ![](https://cdn.smartx.com/internal-docs/assets/8f96e4d9/administration_guide_025.png)
     3. 在弹出的 **Windows 安全**对话框中，确认安装的驱动程序名称为 **Red Hat VirtIO SCSI controller** 后，单击**安装**。
     4. 等待驱动程序更新完后，若在设备管理器窗口中，在磁盘驱动器下显示 **Red Hat VirtIO SCSI Disk Device**，在存储控制器下显示 **Red Hat VirtIO SCSI controller**，说明 Virtio 磁盘驱动安装成功。

        ![](https://cdn.smartx.com/internal-docs/assets/8f96e4d9/administration_guide_021.png)
   - **更新 Virtio 网卡驱动**

     1. 在设备管理器窗口中，展开**其他设备**，右键单击 **以太网控制器**，选择**更新驱动程序软件**。

        ![](https://cdn.smartx.com/internal-docs/assets/8f96e4d9/administration_guide_022.png)
     2. 在弹出的**更新驱动程序软件**窗口中，单击**浏览计算机以查找驱动程序软件**，选择 Virtio 驱动的 CD 驱动器，单击**确定**，单击**下一步**。

        ![](https://cdn.smartx.com/internal-docs/assets/8f96e4d9/administration_guide_025.png)
     3. 在弹出的 **Windows 安全**对话框中，确认安装的驱动程序名称为 **Red Hat VirtIO Ethernet Adapter** 后，单击**安装**。
     4. 等待驱动程序更新完后，若在设备管理器窗口中，在网络适配器下显示 **Red Hat VirtIO Ethernet Adapter**，说明 Virtio 网卡驱动安装成功。

        ![](https://cdn.smartx.com/internal-docs/assets/8f96e4d9/administration_guide_023.png)

---

## 附录 > 为迁移或导入到 ELF 平台的虚拟机安装 Virtio 驱动 > Linux 系统操作指导

# Linux 系统操作指导

**前提条件**

- 对于使用 Linux 系统 Virtio 驱动的 Linux 虚拟机，其内核版本必须高于 2.6.24。
- 确保已关闭所有防病毒软件或入侵检测软件，若有需要，可以在安装完 Virtio 驱动后再启用这些软件。
- 所有磁盘的总线已设置为 IDE。若存在总线不为 IDE 的磁盘，可参考 [Windows 系统操作指导](/smtxv2v/1.8.0/v2v_user_guide/administration_guide_238#windows-%E7%B3%BB%E7%BB%9F%E6%93%8D%E4%BD%9C%E6%8C%87%E5%AF%BC)的步骤 1 ～ 3 更改磁盘的总线。

## CentOS / OpenEuler / Red Hat / Oracle Linux 系统操作指导

**前提条件**

- 操作系统版本满足以下要求：
  - CentOS：不低于 6.0 版本
  - OpenEuler：不低于 20.03 版本
  - Red Hat：不低于 6.0 版本
  - Oracle Linux：不低于 6.0 版本
- 已确认引导的虚拟文件系统，可通过查看 boot 目录下包含文件名 `initramfs` 还是 `initrd` 进行确认。

**操作步骤**

1. 使用 `vi /etc/dracut.conf` 命令打开 “/etc/dracut.conf” 文件。
2. 按 i 键进入编辑模式，在 `add_drivers` 项中添加 Virtio 驱动，如下，请根据实际操作系统的要求调整格式。

   ```
   [root@localhost ~]# vi /etc/dracut.conf 
   # additional kernel modules to the default 
   add_drivers+="virtio_blk virtio_scsi virtio_net virtio_pci virtio_ring virtio"
   ```

   > **注意**：
   >
   > 对于 OpenEuler 20.03 和 Red Hat Enterprise Linux 8.x 版本，`add_drivers` 项中仅需添加 `virtio_blk`、`virtio_scsi` 和 `virtio_net`，即 `add_drivers+="virtio_blk virtio_scsi virtio_net"`。
3. 按 Esc 键后，输入 `:wq`，按 Enter 键，保存设置并退出 “/etc/dracut.conf” 文件。
4. 参考以下命令，重新生成 initrd。

   ```
   dracut -f /boot/initramfs-`uname -r`.img
   ```

   > **注意**：
   >
   > 命令中 `uname -r` 两侧的符号为反引号（`）。

   如果引导的虚拟文件系统不是默认的 initramfs，则命令为

   ```
   dracut -f <name>
   ```

   其中，`<name>` 为实际使用的 initramfs 文件名或者 initrd 文件名，文件名可在 grub.cfg 配置（ `/boot/grub/grub.cfg` 或 `/boot/grub2/grub.cfg` 或 `/boot/grub/grub.conf`，不同操作系统的具体路径会有所区别）中获取。
5. 检查引导的虚拟文件系统是否已经成功添加 Virtio 驱动相应模块。

   - 若引导的虚拟文件系统是 initramfs，请输入以下命令。

     ```
     lsinitrd /boot/initramfs-`uname -r`.img | grep virtio
     ```
   - 若引导的虚拟文件系统是 initrd，请输入以下命令。

     ```
     lsinitrd /boot/initrd-`uname -r` | grep virtio
     ```

   以引导的虚拟文件系统是 initramfs 为例，回显信息如下所示：

   ```
   [root@localhost ~]# lsinitrd /boot/initramfs-`uname -r`.img | grep virtio 
   -rwxr--r--   1 root     root        23448 Nov 1 10:58 lib/modules/2.6.32-573.8.1.el6.x86_64/kernel/drivers/block/virtio_blk.ko 
   -rwxr--r--   1 root     root        50704 Nov 1 10:58 lib/modules/2.6.32-573.8.1.el6.x86_64/kernel/drivers/net/virtio_net.ko 
   -rwxr--r--   1 root     root        28424 Nov 1 10:58 lib/modules/2.6.32-573.8.1.el6.x86_64/kernel/drivers/scsi/virtio_scsi.ko 
   drwxr-xr-x   2 root     root            0 Nov 1 10:58 lib/modules/2.6.32-573.8.1.el6.x86_64/kernel/drivers/virtio 
   -rwxr--r--   1 root     root        14544 Nov 1 10:58 lib/modules/2.6.32-573.8.1.el6.x86_64/kernel/drivers/virtio/virtio.ko 
   -rwxr--r--   1 root     root        21040 Nov 1 10:58 lib/modules/2.6.32-573.8.1.el6.x86_64/kernel/drivers/virtio/virtio_pci.ko 
   -rwxr--r--   1 root     root        18016 Nov 1 10:58 lib/modules/2.6.32-573.8.1.el6.x86_64/kernel/drivers/virtio/virtio_ring.ko
   ```

   以上回显信息只是一个例子，若在回显信息中可看到 virtio\_net、 virtio\_blk 和 virtio\_scsi 驱动模块，则说明全部 Virtio 驱动模块已添加成功。
6. 关闭虚拟机，将虚拟机的磁盘总线改为 VIRTIO，将网卡模式改为 VIRTIO 模式，再启动虚拟机。若可以正常进入系统，则说明全部 Virtio 驱动安装成功。

## Ubuntu/Debian 系统操作指导

**前提条件**

操作系统版本满足以下要求：

- Ubuntu：不低于 18.04 版本
- Debian：不低于 9.0 版本

**操作步骤**

1. 使用 `vi /etc/initramfs-tools/modules` 命令打开 “modules” 文件。
2. 按 i 键进入编辑模式，添加 Virtio 驱动，请根据实际操作系统的要求调整格式。

   ```
   [root@localhost ~]#vi /etc/initramfs-tools/modules 
   …… 
   # Examples: 
   # 
   # raid1 
   # sd_mOd 
   virtio_blk
   virtio_scsi
   virtio_net
   virtio_pci
   virtio_ring
   virtio
   ```
3. 按 Esc 键后，输入 `:wq`，按 Enter 键。保存设置并退出 “/etc/initramfs-tools/modules” 文件。
4. 输入 `update-initramfs -u`，重新生成 initrd。
5. 输入以下命令，检查引导的虚拟文件系统是否已经成功添加 Virtio 驱动相应模块。

   ```
   lsinitramfs /boot/initrd.img-`uname -r` |grep virtio
   ```

   > **注意**：
   >
   > 命令中 `uname -r` 两侧的符号为反引号（`）。

   回显信息如下所示：

   ```
   [root@localhost ~]# lsinitramfs /boot/initrd.img-`uname -r` |grep virtio 
   -rwxr--r-- 1 root root 19248 Jun 22 2012 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/scsi/virtio_scsi.ko
   -rwxr--r-- 1 root root 23856 Jun 22 2012 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/block/virtio_blk.ko
   drwxr-xr-x 2 root root 0 Jul 12 14:53 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/virtio
   -rwxr--r-- 1 root root 15848 Jun 22 2012 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/virtio/virtio_ring.ko
   -rwxr--r-- 1 root root 20008 Jun 22 2012 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/virtio/virtio_pci.ko
   -rwxr--r-- 1 root root 12272 Jun 22 2012 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/virtio/virtio.ko
   -rwxr--r-- 1 root root 38208 Jun 22 2012 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/net/virtio_net.ko
   ```

   以上回显信息只是一个例子，若在回显信息中可看到 virtio\_net、 virtio\_blk 和 virtio\_scsi 驱动模块，则说明全部 Virtio 驱动模块已添加成功。
6. 关闭虚拟机，将虚拟机的磁盘总线改为 VIRTIO，将网卡模式改为 VIRTIO 模式，再启动虚拟机。若可以正常进入系统，则说明全部 Virtio 驱动安装成功。

## SUSE/openSUSE 系统操作指导

**前提条件**

- SUSE/openSUSE 系统版本不低于 11。
- 已确认引导的虚拟文件系统，可通过查看 boot 目录下包含文件名 `initramfs` 还是 `initrd` 进行确认。

### 版本低于SUSE 12 SP1 / openSUSE 13

1. 使用 `vi etc/sysconfig/kernel` 命令打开 “/etc/sysconfig/kernel” 文件。
2. 在 `INITRD_MODULES=""` 中添加 Virtio 驱动，如下，请根据实际操作系统的要求调整格式。完成后保存并退出该文件。

   ```
   [root@localhost ~]# vi /etc/sysconfig/kernel 
   # (like drivers for scsi-controllers, for lvm or reiserfs)
   #
   INITRD_MODULES="ata_piix ata_generic virtio_blk virtio_scsi virtio_net virtio_pci virtio_ring virtio"
   ```
3. 执行 mkinitrd 命令，重新生成 initrd。

   > **说明**：
   >
   > 如果引导的虚拟文件系统不是默认的 initramfs 或者 initrd，则命令为：`dracut -f 实际使用的 initramfs 或者 initrd 文件名`。“实际使用的 initramfs 或者 initrd 文件名”可在 menu.lst 或者 grub.cfg 配置（“/boot/grub/menu.lst”或“/boot/grub/grub.cfg”或“/boot/grub2/grub.cfg”）中获取。

   以 SUSE 11 SP4 为例，如下所示：

   ```
   default 0 
   timeout 10 
   gfxmenu (hd0,0)/boot/message 
   title sles11sp4_001_[_VMX_] 
   root (hd0,0) 
   kernel /boot/linux.vmx vga=0x314 splash=silent console=ttyS0,115200n8 console=tty0 net.ifnames=0 NON_PERSISTENT_DEVICE_NAMES=1 showopts 
   initrd /boot/initrd.vmx 
   title Failsafe_sles11sp4_001_[_VMX_] 
   root (hd0,0) 
   kernel /boot/linux.vmx vga=0x314 splash=silent ide=nodma apm=off noresume edd=off powersaved=off nohz=off highres=off processsor.max+cstate=1 nomodeset x11failsafe console=ttyS0,115200n8 console=tty0 net.ifnames=0 NON_PERSISTENT_DEVICE_NAMES=1 showopts 
   initrd /boot/initrd.vmx
   ```

   其中，`initrd` 所在行的 `/boot/initrd.vmx` 为实际使用的 initrd 文件，执行的时候请按照 `dracut -f /boot/initrd.vmx` 执行。如果 `initrd` 所在行的 initrd 文件不包含 /boot 目录，如 `/initramfs-xxx`，请在执行 dracut 命令时增加 /boot 目录，例如：`dracut -f /boot/initramfs-xxx`。
4. 执行如下命令，检查引导的虚拟文件系统是否已经成功添加 Virtio 驱动相应模块。

   - 若引导的虚拟文件系统是 initramfs，请输入以下命令。

     ```
     lsinitrd /boot/initramfs-`uname -r`.img | grep virtio
     ```

     > **注意**：
     >
     > 命令中 `uname -r` 两侧的符号为反引号（`）。
   - 若引导的虚拟文件系统是 initrd，请输入以下命令。

     ```
     lsinitrd /boot/initrd-`uname -r` | grep virtio
     ```

   以引导的虚拟文件系统是 initrd 为例，回显信息如下所示：

   ```
   [root@localhost ~]# lsinitrd /boot/initrd-`uname -r` | grep virtio
   -rwxr--r-- 1 root root 19248 Jun 22 2012 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/scsi/virtio_scsi.ko
   -rwxr--r-- 1 root root 23856 Jun 22 2012 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/block/virtio_blk.ko
   drwxr-xr-x 2 root root 0 Jul 12 14:53 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/virtio
   -rwxr--r-- 1 root root 15848 Jun 22 2012 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/virtio/virtio_ring.ko
   -rwxr--r-- 1 root root 20008 Jun 22 2012 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/virtio/virtio_pci.ko
   -rwxr--r-- 1 root root 12272 Jun 22 2012 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/virtio/virtio.ko
   -rwxr--r-- 1 root root 38208 Jun 22 2012 lib/modules/2.6.32-279.el6.x86_64/kernel/drivers/net/virtio_net.ko
   ```

   以上回显信息只是一个例子，若在回显信息中可看到 virtio\_net、 virtio\_blk 和 virtio\_scsi 驱动模块，则说明全部 virtio 驱动模块已添加成功。
5. 关闭虚拟机，将虚拟机的磁盘总线改为 VIRTIO，将网卡模式改为 VIRTIO 模式，再启动虚拟机。若可以正常进入系统，则说明全部 Virtio 驱动安装成功。

### 版本为 SUSE 12 SP1

1. 使用 `vi /etc/dracut.conf` 命令打开 “/etc/dracut.conf” 文件。
2. 按 i 键进入编辑模式，在 `add_drivers` 项中添加 Virtio 的驱动，如下，请根据实际操作系统的要求调整格式。

   ```
   [root@localhost ~]# vi /etc/dracut.conf 
   # additional kernel modules to the default
   add_drivers+="ata_piix ata_generic virtio_blk virtio_scsi virtio_net virtio_pci virtio_ring virtio"
   ```
3. 按 Esc 键后，输入 `:wq`，按 Enter 键。保存设置并退出 “/etc/dracut.conf” 文件。
4. 执行以下命令，重新生成 initrd。

   ```
   dracut -f /boot/initramfs-`uname -r`.img
   ```

   > **注意**：
   >
   > 命令中 `uname -r` 两侧的符号为反引号（`）。

   如果引导的虚拟文件系统不是默认的 initramfs，则命令为：

   ```
   dracut -f <name>
   ```

   其中，`<name>` 为实际使用的 initramfs 文件名或者 initrd 文件名，文件名可在 grub.cfg 配置（ `/boot/grub/grub.cfg` 或 `/boot/grub2/grub.cfg` 或 `/boot/grub/grub.conf`，不同操作系统的具体路径会有所区别）中获取。
5. 检查引导的虚拟文件系统是否已经成功添加 Virtio 驱动相应模块。

   - 若引导的虚拟文件系统是 initramfs，请输入以下命令。

     ```
     lsinitrd /boot/initramfs-`uname -r`.img | grep virtio
     ```
   - 若引导的虚拟文件系统是 initrd，请输入以下命令。

     ```
     lsinitrd /boot/initrd-`uname -r` | grep virtio
     ```

   以引导的虚拟文件系统是 initrd 为例，回显信息如下所示：

   ```
   [root@localhost ~]# lsinitrd /boot/initrd-`uname -r` | grep virtio
   -rw-r--r-- 1 root root 29335 Oct 26 2016 lib/modules/4.4.21-69-default/kernel/drivers/block/virtio_blk.ko
   -rw-r--r-- 1 root root 57007 Oct 26 2016 lib/modules/4.4.21-69-default/kernel/drivers/net/virtio_net.ko
   -rw-r--r-- 1 root root 32415 Oct 26 2016 lib/modules/4.4.21-69-default/kernel/drivers/scsi/virtio_scsi.ko
   drwxr-xr-x 2 root root 0 Sep 28 10:21 lib/modules/4.4.21-69-default/kernel/drivers/virtio
   -rw-r--r-- 1 root root 19623 Oct 26 2016 lib/modules/4.4.21-69-default/kernel/drivers/virtio/virtio.ko
   -rw-r--r-- 1 root root 38943 Oct 26 2016 lib/modules/4.4.21-69-default/kernel/drivers/virtio/virtio_pci.ko
   -rw-r--r-- 1 root root 24431 Oct 26 2016 lib/modules/4.4.21-69-default/kernel/drivers/virtio/virtio_ring.ko
   ```

   以上回显信息只是一个例子，若在回显信息中可看到 virtio\_net、 virtio\_blk 和 virtio\_scsi 驱动模块，则说明全部 Virtio 驱动模块已添加成功。
6. 关闭虚拟机，将虚拟机的磁盘总线改为 VIRTIO，将网卡模式改为 VIRTIO 模式，再启动虚拟机。若可以正常进入系统，则说明全部 Virtio 驱动安装成功。

### 版本高于 SUSE 12 SP1 / openSUSE 13

1. 使用 `vi /etc/dracut.conf` 命令打开 “/etc/dracut.conf” 文件。
2. 按 i 键进入编辑模式，在 `add_drivers` 项中添加 Virtio 的驱动，如下，请根据实际操作系统的要求调整格式。

   ```
   [root@localhost ~]# vi /etc/dracut.conf 
   # additional kernel modules to the default
   add_drivers+="ata_piix ata_generic virtio_blk virtio_scsi virtio_net virtio_pci virtio_ring virtio"
   ```
3. 按 Esc 键后，输入 `:wq`，按 Enter 键。保存设置并退出 “/etc/dracut.conf” 文件。
4. 执行以下命令，重新生成 initrd。

   ```
   dracut -f /boot/initramfs-`uname -r`.img
   ```

   > **注意**：
   >
   > 命令中 `uname -r` 两侧的符号为反引号（`）。

   如果引导的虚拟文件系统不是默认的 initramfs，则命令为：

   ```
   dracut -f <name>
   ```

   其中，`<name>` 为实际使用的 initramfs 文件名或者 initrd 文件名，文件名可在 grub.cfg 配置（ `/boot/grub/grub.cfg` 或 `/boot/grub2/grub.cfg` 或 `/boot/grub/grub.conf`，不同操作系统的具体路径会有所区别）中获取。
5. 检查引导的虚拟文件系统是否已经成功添加 Virtio 驱动相应模块。

   - 若引导的虚拟文件系统是 initramfs，请输入以下命令。

     ```
     lsinitrd /boot/initramfs-`uname -r`.img | grep virtio
     ```
   - 若引导的虚拟文件系统是 initrd，请输入以下命令。

     ```
     lsinitrd /boot/initrd-`uname -r` | grep virtio
     ```

   以引导的虚拟文件系统是 initrd 为例，回显信息如下所示：

   ```
   [root@localhost ~]# lsinitrd /boot/initrd-`uname -r` | grep virtio
   -rw-r--r-- 1 root root 29335 Oct 26 2016 lib/modules/4.4.21-69-default/kernel/drivers/block/virtio_blk.ko
   -rw-r--r-- 1 root root 57007 Oct 26 2016 lib/modules/4.4.21-69-default/kernel/drivers/net/virtio_net.ko
   -rw-r--r-- 1 root root 32415 Oct 26 2016 lib/modules/4.4.21-69-default/kernel/drivers/scsi/virtio_scsi.ko
   drwxr-xr-x 2 root root 0 Sep 28 10:21 lib/modules/4.4.21-69-default/kernel/drivers/virtio
   -rw-r--r-- 1 root root 19623 Oct 26 2016 lib/modules/4.4.21-69-default/kernel/drivers/virtio/virtio.ko
   -rw-r--r-- 1 root root 38943 Oct 26 2016 lib/modules/4.4.21-69-default/kernel/drivers/virtio/virtio_pci.ko
   -rw-r--r-- 1 root root 24431 Oct 26 2016 lib/modules/4.4.21-69-default/kernel/drivers/virtio/virtio_ring.ko
   ```

   以上回显信息只是一个例子，若在回显信息中可看到 virtio\_net、 virtio\_blk 和 virtio\_scsi 驱动模块，则说明全部 virtio 驱动模块已添加成功。
6. 关闭虚拟机，将虚拟机的磁盘总线改为 VIRTIO，将网卡模式改为 VIRTIO 模式，再启动虚拟机。若可以正常进入系统，则说明全部 Virtio 驱动安装成功。

---

## 附录 > FAQ

# FAQ

本节主要讲了在使用 SMTX 迁移工具过程中可能会遇到的一些问题，以及对应的解决办法。其中大部分问题仅列举了问题的常见原因，并不全面。在实际操作中，可先按照原因分析和对应的解决办法逐一排查问题。

## 添加站点失败，该怎么办？

**现象描述**

在站点页面，输入 VMware vCenter 站点的信息，或者 SMTX 虚拟机服务集群的信息后，单击**添加站点**，提示“添加 xx 站点失败”。

**可能原因**

导致站点添加失败的原因可能有多种，可先参考下面几种常见原因对问题进行排查。

- SMTX 迁移工具与待添加的站点间的网络无法连通。
- 输入的管理员用户名或密码不正确。
- 待添加的站点出现异常。例如，SMTX 虚拟机服务集群的磁盘空间已满。
- 防火墙的端口 80 和 443 无法正常连接。

## 在 Windows 安装补丁过程中迁移虚拟机，迁移失败，该怎么办？

**现象描述**

对于安装 Windows 操作系统的虚拟机，在安装最新的 Windows 补丁集后，虚拟机无法从 VMware ESXi 平台正常迁移到 ELF 平台，系统提示无法安装 Virtio 驱动。在使用 IDE 方式挂载启动盘后，系统锁死在 **Booting From Hard Disk** 进程，无法正常进入操作系统。

**可能原因**

在安装 Windows 补丁的过程中迁移虚拟机，导致迁移后读取注册表失败，从而没有注入驱动。

**解决方法**

建议用户在安装 Windows 补丁完全结束后，再启动迁移任务。

## 虚拟机执行迁移任务时，提示虚拟机驱动注入失败，该怎么办？

**现象描述**

虚拟机在开机的状态下进行迁移时，系统提示驱动注入失败，日志显示 `generate initramfs failed!` 。

**可能原因**

在全量迁移虚拟机的数据时，目标端站点的磁盘根目录空间已写满，导致虚拟机驱动注入失败。

**解决方法**

建议用户在清理磁盘空间后再执行迁移任务，或者在已创建好的虚拟机上手动注入驱动。

## 使用 Windows 2003 R2 操作系统的虚拟机在迁移结束后，再次开机并打开网络连接时系统卡死，该怎么办？

**现象描述**

对于安装 Windows 2003 R2 操作系统的虚拟机，在迁移结束后开机，发现操作虚拟控制台无反应。执行如下操作：

1. 强制关机后卸载虚拟机的其余虚拟卷，只挂载系统盘。
2. 重新启动虚拟机后发现可以操作虚拟控制台，系统提示识别到新硬件。根据提示依次手动安装硬件。
3. 安装完驱动并按照要求重启系统后，再次关机，重新挂载虚拟卷。
4. 重新开机，系统重启后右下角无网络标识，打开网络连接后系统卡死。
5. 关机并卸载其他虚拟卷，只保留系统盘。
6. 重新开机后对网卡进行配置，系统提示如下图：

   ![](https://cdn.smartx.com/internal-docs/assets/e4a61e8a/FAQ_001.png)

**可能原因**

Windows 2003 操作系统的虚拟机不支持在迁移时自动删除原有虚拟机的配置信息，导致迁移后的虚拟机可能包含源端的网卡配置信息，从而与当前的网卡配置产生冲突。

**解决方法**

1. 打开 **cmd** 窗口，执行如下命令：

   ```
   set devmgr_show_nonpresent_devices=1`
   ```
2. 继续执行如下命令：

   ```
   start devmgmt.msc
   ```
3. 在弹出的**设备管理器**界面，选择**查看** > **显示隐藏设备**，单击**网络适配器**，卸载提示的网卡。
4. 配置完 IP 后关机，挂载全部虚拟卷。
5. 重新启动虚拟机，使用 `ipconfig` 命令检查已配置的 IP，然后重新打开网络连接，系统显示正常。

## 虚拟机从 VMware ESXi 平台迁移至 ELF 平台后，为什么它的可用内存减少了？

**现象描述**

将虚拟机从 VMware ESXi 平台至 ELF 平台，在迁移完成后再开机，显示虚拟机的可用内存减少。

**原因分析**

宿主机运行虚拟机需占用额外内存（overhead memory），而多数情况下，在 KVM 虚拟化环境中运行虚拟机比在 VMware 虚拟化环境中运行所占用的内存更多。因此在完成迁移后再开机，虚拟机显示其可用内存减少。

**解决方法**

若用户存在定额内存的要求，给虚拟机分配内存时可以适当增大总量。

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
