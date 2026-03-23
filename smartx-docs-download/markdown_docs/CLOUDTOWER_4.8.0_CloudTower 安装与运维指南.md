---
title: "CLOUDTOWER/4.8.0/CloudTower 安装与运维指南"
source_url: "https://internal-docs.smartx.com/cloudtower/4.8.0/tower_installation_guide/tower_preface_generic"
sections: 50
---

# CLOUDTOWER/4.8.0/CloudTower 安装与运维指南
## 关于本文档

# 关于本文档

本文档介绍了在 SMTX OS 集群、SMTX ELF 集群和 SMTX ZBS 集群中安装部署 CloudTower 的流程和操作步骤，以及如何从低版本的 CloudTower 升级至本版本的操作方法。

SMTX ZBS 集群包含 SMTX ZBS 块存储集群（简称“块存储集群”）和部署在其上的 SMTX ZBS 文件存储集群（简称“文件存储集群”）。在 SMTX ZBS 集群中安装部署 CloudTower，其实质是在 SMTX ZBS 块存储集群中安装部署 CloudTower。

阅读本文档的对象需了解 SMTX OS 超融合软件、SMTX ELF 软件和 SMTX ZBS 块存储软件，了解虚拟化和分布式存储相关技术，并具备数据中心操作的丰富经验。

---

## 更新信息

# 更新信息

**2026-01-30：配合 CloudTower 4.8.0 发布**

相较于上一版本，本版本主要更新如下：

- 新增 **CloudTower 简介**章节，介绍 CloudTower 的两种部署模式：单点模式和高可用集群模式。
- 新增**部署 CloudTower 高可用集群**章节。
- 新增**配置系统设置**章节，介绍校准 CloudTower 时间和配置 DNS 服务器的方法。
- 在**变更 CloudTower 的配置**章节中新增**变更高可用集群的环境配置**小节。

---

## CloudTower 简介

# CloudTower 简介

CloudTower 是由北京志凌海纳科技股份有限公司（以下简称 “SmartX”）研发的 SmartX 多集群资源集中管理平台。CloudTower 运行在虚拟机内，通过使用少量的计算和存储资源便可管理上千台虚拟机。除虚拟机生命周期管理、存储管理、网络管理、硬件管理、监控和报警等基本服务外，CloudTower 还提供全局搜索、虚拟机资源优化、事件审计、虚拟机回收站和报表等功能，同时它也提供完整和标准的 RESTful API 和多种语言的 SDK，帮助运维管理员轻松管理和使用多个 SMTX OS、SMTX ZBS 和 SMTX ELF 集群。

CloudTower 支持部署在 SMTX OS 集群、SMTX ELF 集群和 SMTX ZBS 集群中，可运行在 Intel x86\_64、AMD x86\_64、Hygon x86\_64、兆芯 x86、鲲鹏 AArch64 架构或飞腾 AArch64 架构的服务器上。CloudTower 支持以单点模式和高可用集群模式进行部署，以满足不同应用场景下对管理平台连续性的要求。

---

## CloudTower 简介 > 相关概念

# 相关概念

**CloudTower**

SmartX 多集群资源集中管理平台，可统一管理多种类型的 SmartX 集群及其资源。

**SMTX OS 集群**

SMTX OS 集群属于逻辑概念。在实际生产环境中，一个 SMTX OS 集群至少由 3 个节点通过网络互连组成。

**SMTX ZBS 集群**

SMTX ZBS 集群包含块存储集群和文件存储集群，分别提供块存储服务和文件存储服务。文件存储集群需要在块存储集群安装部署完成后再进行部署。

**SMTX ELF 集群**

属于逻辑概念。在实际生产环境中，一个 SMTX ELF 集群至少由 3 个运行 SMTX ELF 软件的节点通过网络互连组成。

**CloudTower 单点模式**

CloudTower 以单虚拟机实例的方式部署。该模式架构轻量，资源占用少且部署便捷，但存在单点故障风险（SPOF）。适用于 POC 测试、边缘站点或对管理平台连续性要求不高的非关键业务场景。

**CloudTower 高可用（HA）集群**

CloudTower 高可用集群（简称“CloudTower HA 集群”）由主动节点、被动节点和仲裁节点组成，采用主-被架构，为管理平台提供持续可用能力。通过数据同步与自动故障切换机制，仲裁节点监控集群的运行状态，当主动节点或其所在环境发生故障时，触发自动故障转移，由被动节点接管服务，保证 CloudTower 管理能力不中断。

**主动节点**

高可用集群的核心工作节点。该节点负责承载所有的业务流量、处理用户 API 请求，并向被管集群下发指令。同时，它负责将数据变更同步给被动节点。

**被动节点**

高可用集群的热备节点。该节点通过同步复制机制保持与主动节点的数据强一致性（RPO=0）。被动节点平时不直接承载业务流量，当主动节点故障时自动升级为主动节点以接管服务。

**仲裁节点**

高可用集群的仲裁者。仲裁节点不存储业务数据，主要负责检测主动节点和被动节点的健康状态并响应处理。在特定故障场景下，发起自动故障转移，以保证 CloudTower 持续可用。

**故障转移**

也称为故障切换，指 CloudTower 主动节点或其所在环境发生故障时，业务由主动节点切换至被动节点以保持服务连续性的过程。该机制确保了管理平台在故障场景下的业务连续性 (RTO < 5 min)。

**CloudTower 管理 IP**

用于外部访问 CloudTower 的 IP 地址。

**CloudTower HA IP**

用于节点间内部通信，包括状态同步、心跳检测与健康状态上报。

---

## CloudTower 简介 > 部署模式

# 部署模式

CloudTower 支持单点和高可用集群两种部署模式，请根据您的实际需求选择其中一种模式进行部署。

---

## CloudTower 简介 > 部署模式 > CloudTower 单点模式

# CloudTower 单点模式

CloudTower 以单虚拟机实例的方式部署和运行。该模式架构轻量，资源占用少且部署便捷，但存在单点故障风险（SPOF）。适用于 POC 测试、边缘站点或对管理平台连续性要求不高的非关键业务场景。

---

## CloudTower 简介 > 部署模式 > CloudTower 高可用（HA）集群模式

# CloudTower 高可用（HA）集群模式

CloudTower 高可用集群（简称 “CloudTower HA 集群”）基于 Active-Passive（主被）架构设计，由主动节点、被动节点和仲裁节点协同工作，旨在为企业级管理平台提供持续的运行保障。

**核心优势与工作机制**

- **数据零丢失 (RPO = 0)**：集群实现了主动节点与被动节点间的数据实时强一致。被动节点通过持续的数据复制保持同步，确保故障场景下业务数据不丢失。
- **服务快速恢复 (RTO < 5 min)**：仲裁节点仅参与选主投票，不存储业务数据。它持续监控集群健康状态，一旦检测到主动节点故障，自动触发故障转移流程，由被动节点快速接管服务，有效消除管理平面的单点故障风险。

**部署要求**

为规避物理单点故障，三类节点必须遵循反亲和性原则，分散部署于不同的物理主机上。

- **主动节点或被动节点**： 必须部署在 SMTX OS (ELF) 集群或 SMTX ELF 集群中。
- **仲裁节点**： 支持部署在任意类型的集群中（含 SmartX 集群及第三方集群）。

**使用限制**

CloudTower HA 集群不支持部署 **SMTX Kubernetes 服务**，如果您需要使用 CloudTower 部署 SMTX Kubernetes 服务，请务必选择**单点模式**进行部署。

---

## 部署单点 CloudTower

# 部署单点 CloudTower

在 SMTX OS 集群、SMTX ELF 集群和 SMTX ZBS 集群中安装部署 CloudTower 的流程略有不同，请分别参考对应的内容完成操作。

**注意事项**

在集群中安装部署完 CloudTower 后， 请勿在 CloudTower 虚拟机中安装第三方插件，以免影响 CloudTower 虚拟机的稳定运行。

---

## 部署单点 CloudTower > 安装部署前的准备

# 安装部署前的准备

为了保证安装部署 CloudTower 顺利进行，请参考下面要求，完成部署前的准备工作。此外，待部署的集群与 CloudTower 的软件版本必须兼容，在部署 CloudTower 前，请务必参考随软件发布的文档《CloudTower 发布说明》，确认集群与本版本的 CloudTower 符合配套要求。

---

## 部署单点 CloudTower > 安装部署前的准备 > 确认浏览器版本兼容性要求

# 确认浏览器版本兼容性要求

安装部署 CloudTower 过程中需要使用 Web 浏览器访问 CloudTower Installer，为保证兼容性，我们建议您使用以下版本的浏览器，同时开启 Cookie 和 JavaScript。

| **浏览器** | **版本要求** |
| --- | --- |
| Google Chrome | 91 及以上版本 |
| Microsoft Edge | 107 及以上版本 |
| Mozilla Firefox | 107.0 及以上版本 |
| Apple Safari | 14.1 及以上版本 |

---

## 部署单点 CloudTower > 安装部署前的准备 > 规划 CloudTower 环境配置等级

# 规划 CloudTower 环境配置等级

CloudTower 环境配置分为两个等级：`低配`和`高配`，每个等级支持管理的集群数量、主机和虚拟机规模不同，并且占用的集群的资源也不同。

在集群中部署 CloudTower 前，请您根据实际需求做好 CloudTower 环境配置等级规划，并确保 CloudTower 所在的集群有足够的资源（CPU、内存和存储空间）可分配给部署 CloudTower 的虚拟机。

| **环境配置等级** | **CloudTower 管理能力** | **CloudTower 虚拟机占用的资源** |
| --- | --- | --- |
| **低配** | - 10 个集群 - 100 台主机 - 1000 个虚拟机 | - 4 核 vCPU - 12 GiB 内存 - 100 GiB 存储空间 |
| **高配** | - 100 个集群 - 1000 台主机 - 10000 个虚拟机 | - 8 核 vCPU - 19 GiB 内存 - 400 GiB 存储空间 |

---

## 部署单点 CloudTower > 安装部署前的准备 > 规划 CloudTower IP 和集群管理虚拟 IP

# 规划 CloudTower IP 和集群管理虚拟 IP

在 SMTX OS 集群、SMTX ELF 集群或 SMTX ZBS 集群中使用 CloudTower Installer 部署 CloudTower 时，配置页面要求输入集群的管理虚拟 IP 和 CloudTower IP 信息。建议在部署前做好两个 IP 的规划。

为集群设置管理虚拟 IP 是为了保证集群的高可用性。访问此 IP 时，可以自动通过集群内任一可用的主机管理 IP 访问集群。

但若在部署前已设置集群的管理虚拟 IP，进入 CloudTower Installer 后，系统将不再要求输入集群的管理虚拟 IP。此时，只需要规划 CloudTower 的 IP、子网掩码和网关即可。

CloudTower IP 和集群管理虚拟 IP 的设置需符合下述要求：

- 确保 CloudTower IP 与集群管理虚拟 IP 连通。
- 管理虚拟 IP 与集群节点的管理 IP 在同一个子网内。

  > **说明：**
  >
  > 如果待部署的 SMTX ZBS 集群版本为 5.6.0 及以上，则要求 SMTX ZBS 块存储集群的管理虚拟 IP 与其节点的块存储集群管理 IP 在同一个子网内。
- 管理虚拟 IP 不能与以下 CIDR 范围内的任何 IP 地址重叠：

  - 169.254.0.0/16
  - 240.0.0.0/4
  - 224.0.0.0/4
  - 198.18.0.0/15
  - 127.0.0.0/8
  - 0.0.0.0/8

---

## 部署单点 CloudTower > 安装部署前的准备 > 规划并开放网络端口

# 规划并开放网络端口

为了确保 CloudTower 的正常运行及相应功能的正常使用，被访问的目标端需要开放相应 TCP 端口，开放的端口及端口说明如下：

| 源端 | 目标端 | 目标端需开放的 TCP 端口 | 端口说明 |
| --- | --- | --- | --- |
| CloudTower 虚拟机 | 被管理的 SMTX OS 集群中的物理机 | 80、443 | CloudTower 虚拟机通过此端口访问 SMTX OS 集群的部分接口。 其中，`443` 端口还用于巡检中心和集群的 API 通信，以及用于升级中心获取集群主机的版本信息。 |
| 8000 | CloudTower 虚拟机通过此端口访问 `vnc-proxy` 服务。 |
| 8500 | CloudTower 的巡检中心服务通过此端口探测 SMTX OS 集群节点的连通性。 |
| 10000 | - CloudTower 的巡检中心服务通过此端口完成 Inspector agent 的部署和接口调用。 - CloudTower 的升级中心服务通过此端口安装 Upgrade agent。 |
| 10100 | CloudTower 虚拟机通过此端口访问 `zbs-metad` 服务，获取 ZBS 的部分元数据。 |
| 10201、10206 、10207 | CloudTower 虚拟机通过此端口访问 `zbs-chunkd` 服务并读写数据。 |
| 3260、3261 | CloudTower 使用此端口上传部署 CloudTower 代理时的镜像文件。 |
| CloudTower 虚拟机 | 被管理的 SMTX ELF 集群中的物理机 | 80、443 | CloudTower 虚拟机通过此端口访问 SMTX ELF 集群的部分接口。 其中，`443` 端口还用于巡检中心和集群的 API 通信，以及用于升级中心获取集群主机的版本信息。 |
| 8000 | CloudTower 虚拟机通过此端口访问 `vnc-proxy` 服务。 |
| 8500 | CloudTower 的巡检中心服务通过此端口探测 SMTX ELF 集群节点的连通性。 |
| 10000 | - CloudTower 的巡检中心服务通过此端口完成 Inspector agent 的部署和接口调用。 - CloudTower 的升级中心服务通过此端口安装 Upgrade agent。 |
| 3260、3261 | CloudTower 使用此端口上传部署 CloudTower 代理时的镜像文件。 |
| CloudTower 虚拟机 | 被管理的 SMTX ZBS 集群中的物理机 | 80、443 | CloudTower 虚拟机通过此端口访问 SMTX ZBS 集群的部分接口。 其中，`443` 端口还用于巡检中心和集群的 API 通信，以及用于升级中心获取集群主机的版本信息。 |
| 8000 | CloudTower 虚拟机通过此端口访问 `vnc-proxy` 服务。 |
| 8500 | CloudTower 的巡检中心服务通过此端口探测 SMTX ZBS 集群节点的连通性。 |
| 10000 | - CloudTower 的巡检中心服务通过此端口完成 Inspector agent 的部署和接口调用。 - CloudTower 的升级中心服务通过此端口安装 Upgrade agent。 |
| CloudTower 虚拟机 | CloudTower 代理虚拟机 | 22 | CloudTower 虚拟机通过此端口连接至 CloudTower 代理虚拟机，配置启动代理服务。 |
| CloudTower 代理虚拟机 | CloudTower 虚拟机 | 80、443 | CloudTower 代理虚拟机通过此端口连接到 CloudTower 虚拟机中的 Hub 服务。 |
| CloudTower 代理虚拟机 | 被管理的 SMTX OS 集群中的物理机 | 80、443 | CloudTower 代理虚拟机通过此端口访问 SMTX OS 集群的部分接口。 |
| 10100 | CloudTower 代理虚拟机通过此端口访问 `zbs-metad` 服务，获取 ZBS 的部分元数据。 |
| 10201、10206 、10207 | CloudTower 代理虚拟机通过此端口访问 `zbs-chunkd` 服务并读写数据。 |
| 客户端 | CloudTower 虚拟机 | 9000 | 客户端通过此端口获取 CloudTower 升级进度信息。 |

---

## 部署单点 CloudTower > 安装部署前的准备 > 获取安装文件

# 获取安装文件

CloudTower 可部署在 SMTX OS 集群、SMTX ELF 集群或 SMTX ZBS 集群中，并提供了多个版本的安装文件。请根据待部署 CloudTower 的集群类型，服务器的 CPU 架构，以及部署方式，下载适配的 CloudTower 安装文件和 CloudTower Installer 相关 RPM 文件。

## 在 SMTX OS 集群中部署

在 SMTX OS 集群中部署 CloudTower 时，您可以选择以下两种方式进行部署，每种部署方式所选择的安装文件格式不同。

- 通过 CloudTower Installer 安装部署

  必须选择 `tar.gz` 格式的 CloudTower 安装映像文件。
- 在集群中手动创建虚拟机后再进行部署

  必须选择 `ISO` 格式的 CloudTower 安装映像文件。

我们为每种格式都提供了适配不同服务器 CPU 架构的安装文件，如果待部署的 SMTX OS 集群为 `Intel x86_64` 架构，您还可以根据实际需求选择 CentOS 或 openEuler 操作系统的安装文件进行下载。

请根据根据集群的版本、服务器 CPU 架构和主机操作系统（在集群节点中执行 `cat /etc/os-release` 命令可进行确认），下载对应的 CloudTower Installer RPM 文件，并在部署前升级集群的 RPM。

| **SMTX OS 集群版本** | **服务器 CPU 架构** | **主机操作系统** | **CloudTower Installer RPM 文件** |
| --- | --- | --- | --- |
| 5.0.3 ~ 5.0.5 | Intel x86\_64、AMD x86\_64、Hygon x86\_64 或兆芯 x86 | CentOS | `fisheye-5.1.0-rc15.x86_64.rpm`  `cloudtower-installer-1.0.5-rc8.x86_64.rpm` |
| openEuler | `fisheye-5.1.0-rc15.oe1.x86_64.rpm`  `cloudtower-installer-1.0.5-rc8.x86_64.rpm` |
| 鲲鹏 AArch64 | CentOS | `fisheye-5.1.0-rc15.aarch64.rpm`  `cloudtower-installer-1.0.5-rc8.aarch64.rpm` |
| openEuler | `fisheye-5.1.0-rc15.oe1.aarch64.rpm`  `cloudtower-installer-1.0.5-rc8.aarch64.rpm` |
| - 5.0.6 及以上的 5.0.x 版本 - 5.1.0 及以上的 5.1.x 版本 - 6.0.0 ~ 6.1.1 版本 | Intel x86\_64、AMD x86\_64、Hygon x86\_64 或兆芯 x86 | CentOS 或 openEuler | `cloudtower-installer-1.0.5-rc8.x86_64.rpm` |
| 鲲鹏 AArch64 | CentOS 或 openEuler | `cloudtower-installer-1.0.5-rc8.aarch64.rpm` |

## 在 SMTX ZBS 集群中部署

SMTX ZBS 集群支持通过 CloudTower Installer 部署 CloudTower，我们提供了适配不同服务器 CPU 架构的 CloudTower 安装映像文件（`tar.gz` 格式）。

若 SMTX ZBS 集群的版本为 **5.2.0 ~ 5.6.1**，您还需根据集群的服务器 CPU 架构和使用的主机操作系统（在集群节点中执行 `cat /etc/os-release` 命令可进行确认），下载对应的 CloudTower Installer RPM 文件，在部署前升级集群的 RPM。

| **SMTX ZBS 集群版本** | **服务器 CPU 架构** | **主机操作系统** | **CloudTower Installer RPM 文件** |
| --- | --- | --- | --- |
| 5.2.0 ~ 5.4.1 | Intel x86\_64、AMD x86\_64 或 Hygon x86\_64 | CentOS | `fisheye.SMTX_ZBS-5.1.0-rc15.x86_64.rpm`  `cloudtower-installer-1.0.5-rc8.x86_64.rpm` |
| openEuler | `fisheye.SMTX_ZBS-5.1.0-rc15.oe1.x86_64.rpm`  `cloudtower-installer-1.0.5-rc8.x86_64.rpm` |
| 鲲鹏 AArch64 | CentOS | `fisheye.SMTX_ZBS-5.1.0-rc15.aarch64.rpm`  `cloudtower-installer-1.0.5-rc8.aarch64.rpm` |
| openEuler | `fisheye.SMTX_ZBS-5.1.0-rc15.oe1.aarch64.rpm`  `cloudtower-installer-1.0.5-rc8.aarch64.rpm` |
| 5.5.0 ~ 5.6.1 | Intel x86\_64、AMD x86\_64 或 Hygon x86\_64 | CentOS 或 openEuler | `cloudtower-installer-1.0.5-rc8.x86_64.rpm` |
| 鲲鹏 AArch64 | CentOS 或 openEuler | `cloudtower-installer-1.0.5-rc8.aarch64.rpm` |

## 在 SMTX ELF 集群中部署

SMTX ELF 集群支持通过 CloudTower Installer 部署 CloudTower，我们提供了适配不同服务器 CPU 架构的 CloudTower 安装映像文件（`tar.gz` 格式）。

若 SMTX ELF 集群的版本为 **6.0.0 ~ 6.1.1**，您还需根据集群的服务器 CPU 架构（在集群节点中执行 `cat /etc/os-release` 命令可进行确认），下载对应的 CloudTower Installer RPM 文件，并在部署前升级集群的 RPM。

| **SMTX ELF 集群版本** | **服务器 CPU 架构** | **CloudTower Installer RPM 文件** |
| --- | --- | --- |
| 6.0.0 ~ 6.1.1 | Intel x86\_64、AMD x86\_64、Hygon x86\_64 或兆芯 x86 | `cloudtower-installer-1.0.5-rc8.x86_64.rpm` |
| 鲲鹏 AArch64 | `cloudtower-installer-1.0.5-rc8.aarch64.rpm` |

---

## 部署单点 CloudTower > 执行部署 > 在 SMTX OS 集群中部署 CloudTower

# 在 SMTX OS 集群中部署 CloudTower

当在 SMTX OS 集群中部署 CloudTower 时，支持通过以下两种方式进行部署：

- **通过 CloudTower Installer 安装部署**
- **在集群中手动创建虚拟机后再进行部署**

在 SMTX OS（ELF）集群和 SMTX OS（VMware ESXi）集群中部署 CloudTower 的流程基本相同，下面以部署在被管理的 SMTX OS（ELF）集群中为例，描述其部署流程。

**注意事项**

CloudTower 支持在部署过程中修改时区，以使 CloudTower 时区和其所部署的集群的时区保持一致。当前版本的 CloudTower 仅支持通过**在集群中手动创建虚拟机后再进行部署**的方式在部署过程修改 CloudTower 时区。

---

## 部署单点 CloudTower > 执行部署 > 在 SMTX OS 集群中部署 CloudTower > 通过 CloudTower Installer 安装部署

# 通过 CloudTower Installer 安装部署

**前提条件**

- 根据集群的服务器 CPU 架构，已提前下载对应的 `tar.gz` 格式的 CloudTower 安装映像文件。若部署的 SMTX OS 集群为 5.0.3 及以上的 5.0.x、5.1.x、6.0.x 及 6.1.x 版本，还需下载集群对应的 CloudTower Installer 相关 RPM 文件。
- 已规划 CloudTower 的 IP 地址、子网掩码和网关，以及集群管理虚拟 IP。

**准备工作**

当待部署集群为 **5.0.3 及以上的 5.0.x、5.1.x、6.0.x 及 6.1.x** 版本时，请根据如下指示升级相关 RPM 文件。您可以选择在一个节点或每个节点升级 RPM 文件，建议在所有节点都执行升级操作，以确保每个节点的 cloudtower-installer 版本一致。

打开终端命令行工具，使用 SCP 命令将集群对应的 CloudTower Installer 相关 RPM 文件上传至集群待访问节点的 `/home/smartx/` 目录下，然后登录此节点，根据集群的服务器架构、版本和操作系统，升级对应的 RPM 文件。其中 **Cluster\_Node\_IP** 表示集群节点的管理 IP。

- **服务器 CPU 架构为 Intel x86\_64、AMD x86\_64、Hygon x86\_64 或兆芯 x86**

  - SMTX OS 版本为 **5.0.3 ~ 5.0.5**，根据集群使用的主机操作系统（可通过执行 `cat /etc/os-release` 命令进行确认），选择升级对应的 RPM 文件。

    - **CentOS 操作系统**：`fisheye-5.1.0-rc15.x86_64.rpm` 和 `cloudtower-installer-1.0.5-rc8.x86_64.rpm`（RPM 文件）

      ```
      scp cloudtower-installer-1.0.5-rc8.x86_64.rpm   smartx@Cluster_Node_IP:~/
      scp fisheye-5.1.0-rc15.x86_64.rpm smartx@Cluster_Node_IP:~/

      ssh smartx@Cluster_Node_IP
      sudo rpm -Uvh fisheye-5.1.0-rc15.x86_64.rpm
      sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.x86_64.rpm
      sudo service cloudtower-installer restart
      sudo service nginx reload
      ```
    - **openEuler 操作系统**：`fisheye-5.1.0-rc15.oe1.x86_64.rpm` 和 `cloudtower-installer-1.0.5-rc8.x86_64.rpm`（RPM 文件）

      ```
      scp fisheye-5.1.0-rc15.oe1.x86_64.rpm smartx@Cluster_Node_IP:~/
      scp cloudtower-installer-1.0.5-rc8.x86_64.rpm   smartx@Cluster_Node_IP:~/

      ssh smartx@Cluster_Node_IP
      sudo rpm -Uvh fisheye-5.1.0-rc15.oe1.x86_64.rpm
      sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.x86_64.rpm
      sudo service cloudtower-installer restart
      sudo service nginx reload
      ```
  - SMTX OS 版本为 **5.0.6 及以上的 5.0.x、5.1.x、6.0.x 和 6.1.x 版本**，升级 `cloudtower-installer-1.0.5-rc8.x86_64.rpm`（RPM 文件）

    ```
    scp cloudtower-installer-1.0.5-rc8.x86_64.rpm   smartx@Cluster_Node_IP:~/

    ssh smartx@Cluster_Node_IP
    sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.x86_64.rpm
    sudo service cloudtower-installer restart
    sudo service nginx reload
    ```
- **服务器 CPU 架构为鲲鹏 AArch64**

  - SMTX OS 版本为 **5.0.3 ~ 5.0.5**，根据集群使用的主机操作系统（可通过执行 `cat /etc/os-release` 命令进行确认），选择升级对应的 RPM 文件。

    - **CentOS 操作系统**：`cloudtower-installer-1.0.5-rc8.aarch64.rpm` 和 `fisheye-5.1.0-rc15.aarch64.rpm`（RPM 文件）

      ```
      scp fisheye-5.1.0-rc15.aarch64.rpm smartx@Cluster_Node_IP:~/
      scp cloudtower-installer-1.0.5-rc8.aarch64.rpm   smartx@Cluster_Node_IP:~/

      ssh smartx@Cluster_Node_IP
      sudo rpm -Uvh fisheye-5.1.0-rc15.aarch64.rpm
      sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.aarch64.rpm
      sudo service cloudtower-installer restart
      sudo service nginx reload
      ```
    - **openEuler 操作系统**：`cloudtower-installer-1.0.5-rc8.aarch64.rpm` 和 `fisheye-5.1.0-rc15.oe1.aarch64.rpm`（RPM 文件）

      ```
      scp fisheye-5.1.0-rc15.oe1.aarch64.rpm smartx@Cluster_Node_IP:~/
      scp cloudtower-installer-1.0.5-rc8.aarch64.rpm   smartx@Cluster_Node_IP:~/

      ssh smartx@Cluster_Node_IP
      sudo rpm -Uvh fisheye-5.1.0-rc15.oe1.aarch64.rpm
      sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.aarch64.rpm
      sudo service cloudtower-installer restart
      sudo service nginx reload
      ```
  - SMTX OS 版本为 **5.0.6 及以上的 5.0.x、5.1.x、6.0.x 和 6.1.x 版本**，执行如下命令升级 `cloudtower-installer-1.0.5-rc8.aarch64.rpm`（RPM 文件）

    ```
    scp cloudtower-installer-1.0.5-rc8.aarch64.rpm   smartx@Cluster_Node_IP:~/

    ssh smartx@Cluster_Node_IP
    sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.aarch64.rpm
    sudo service cloudtower-installer restart
    sudo service nginx reload
    ```

**操作步骤**

1. 根据部署的 SMTX OS 集群版本，在浏览器中输入相应网址进入 CloudTower Installer。

   - **5.1.5 及以上的 5.1.x 版本、6.3.0 及以上的 6.x.x 版本**：

     <https://SMTX_ManageIP_Address/operation-center-installer>

     进入 CloudTower Installer 之后，需要输入 SMTX OS（ELF）集群超级管理员账号 root 及对应的密码，并单击**下一步**进行校验。校验通过之后才能继续 CloudTower 的安装。
   - **6.2.0 版本**：

     <https://SMTX_ManageIP_Address/operation-center-installer/?hypervisor=ELF&username=root&password=abc123>
   - **5.0.3～5.0.7、5.1.0～5.1.4、6.0.0～6.1.1 版本**：

     <https://SMTX_ManageIP_Address/cloudtower-installer/?hypervisor=ELF&username=root&password=abc123>
   > **说明：**
   >
   > - *`SMTX_ManageIP_Address`* 表示 SMTX OS（ELF）集群的管理 IP。
   > - *`username=root`* 表示 SMTX OS（ELF）集群超级管理员 root。
   > - *`password=abc123`* 表示 SMTX OS（ELF）集群超级管理员 root 的密码，输入网址时请使用实际的密码替换 `abc123`。若密码包括除数字和字母以外的特殊字符，请先对密码进行 URL 编码，再将 `abc123` 替换为编码后的密码。
2. 选择**全新 CloudTower 环境**，并设置集群的管理虚拟 IP。单击**下一步**。

   > **说明：**
   >
   > 如果 SMTX OS 集群在部署 CloudTower 前已设置集群的管理虚拟 IP，进入 CloudTower Installer 后，系统将不再要求输入集群的管理虚拟 IP。
3. 上传 CloudTower 的安装映像。将本地 `tar.gz` 格式的 CloudTower 安装映像拖拽至文件区域，或者选择从本地上传文件。
4. 选择 CloudTower 的环境配置。选择**低配**或**高配**时，需考虑待管理的集群数量、主机和虚拟机规模，并确保集群有足够的资源（CPU、内存和存储空间）可分配给部署 CloudTower 的虚拟机（两个等级的配置区别请参见[规划 CloudTower 环境配置等级](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_05)）。

   > **说明**：
   >
   > 若需要通过 CloudTower 在 SMTX OS 集群中部署 SMTX Kubernetes 服务或 SMTX 文件存储，则环境配置必须选择**高配**。
5. 设置 CloudTower 的 IP 地址和子网掩码、网关信息。
6. 设置 CloudTower 的组织名称和超级管理员 **root** 的密码。
7. 单击**开始安装**，进入 CloudTower 的安装流程。安装完成后，系统将弹出提示框，单击**打开 CloudTower**。15 秒后系统提示即将离开此网站，单击**离开**后将自动跳转至 CloudTower 环境。

---

## 部署单点 CloudTower > 执行部署 > 在 SMTX OS 集群中部署 CloudTower > 在集群中手动创建虚拟机后再进行部署

# 在集群中手动创建虚拟机后再进行部署

**前提条件**

- 根据集群的服务器 CPU 架构，已提前下载对应的 CloudTower **ISO 映像**安装文件。
- 已规划 CloudTower 的 IP 地址、子网掩码和网关。

**注意事项**

CloudTower 的默认时区为 `Asia/Shanghai (UTC +8:00)`，请您在部署之前确认待部署集群的时区是否和 CloudTower 的默认时区一致。若不一致，建议您在部署过程中修改 CloudTower 时区，使其和所部署的集群的时区保持一致。

**操作步骤**

1. 在浏览器中输入 SMTX OS（ELF）集群中任意节点的管理 IP 或集群管理虚拟 IP（如已设置），使用 root 超级管理员的身份登入 Web 控制台管理界面。
2. 在左侧导航栏中选择 **计算管理** > **ISO 映像**，单击**上传 ISO 映像**，上传 CloudTower 的 ISO 映像⽂件。
3. 创建运行 CloudTower 的虚拟机。

   1. 在 Web 控制台管理界面的左侧导航栏中选择 **计算管理** > **虚拟机**，单击**创建虚拟机**，选择**创建空白虚拟机**。
   2. 在弹出的**创建虚拟机**对话框中，输入虚拟机的名称。
   3. 设置虚拟机的计算资源参数，并添加虚拟盘。您可综合考虑 CloudTower 待管理的集群数量，主机和虚拟机规模等信息，并结合集群主机的 CPU 利用率、内存余量和存储余量，为 CloudTower 虚拟机设置对应的计算资源参数。

      > **说明：**
      >
      > - 在添加虚拟盘时，请确保挂载的 ISO 映像在其他磁盘之后。
      > - CloudTower 环境配置分为`低配`和`高配`两个等级，其配置区别请参见[规划 CloudTower 环境配置等级](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_05)。
      > - 若需要通过 CloudTower 在 SMTX OS 集群中部署 SMTX Kubernetes 服务，则环境配置必须选择`高配`。

      若您无特殊要求，建议 **vCPU 分配**设置为 `8 vCPU`，**内存分配**选择 `19 GiB`，虚拟卷的**容量**设置为 `400 GiB`。
   4. 继续设置其它参数项，建议采用系统默认的参数值。
   5. 单击**载入 ISO**，加载 CloudTower 的 ISO 映像⽂件。
   6. 单击**创建**，完成虚拟机的设置。
4. 在虚拟机中完成 Guest OS 的安装。

   - 虚拟机 Guest OS 的默认用户名为 `cloudtower`。
5. 登录虚拟机 Guest OS，建议为管理网卡设置静态 IP 地址，并确认虚拟机可以 ping 通 SMTX OS 集群的节点管理 IP 或集群管理虚拟 IP。
6. 在虚拟机 Guest OS 中依次执行如下命令，安装 CloudTower。

   ```
   sudo bash
   cd /usr/share/smartx/tower
   sh ./preinstall.sh
   cd ./installer
   ./binary/installer deploy
   ```

   若不能通过默认的虚拟 IP 访问 CloudTower，例如该虚拟机绑定多个 IP，则需要执行如下命令安装 CloudTower。其中 `$VM_IP` 表示可访问 CloudTower 的 IP 地址。

   ```
   sudo bash
   cd /usr/share/smartx/tower
   sh ./preinstall.sh
   cd ./installer
   ./binary/installer deploy --vip $VM_IP
   ```

   执行上述命令后，系统将首先对安装环境进行预检查。

   - 若检查通过，系统将开始安装 CloudTower。
   - 若检查未通过，界面将显示失败信息，请根据[预检查失败处理方式](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_15)中提供的解决方案解决问题，并重新安装 CloudTower。

   安装过程大概持续 30 min。安装成功后，在浏览器中输入虚拟机的 IP 地址，进入 CloudTower 的初始化界面。

---

## 部署单点 CloudTower > 执行部署 > 在 SMTX ZBS 集群中部署 CloudTower

# 在 SMTX ZBS 集群中部署 CloudTower

在 SMTX ZBS 集群中部署 CloudTower，其实质是在 SMTX ZBS 块存储集群中部署 CloudTower，下面所有的操作均在块存储集群中完成。

**前提条件**

- 根据集群的服务器 CPU 架构，已提前下载 `tar.gz` 格式的 CloudTower 安装映像文件，若部署的 SMTX ZBS 集群为 5.2.0 ~ 5.6.1 版本，还需下载集群对应的 CloudTower Installer 相关 RPM 文件。
- 已规划 CloudTower 的 IP 地址、子网掩码和网关，以及集群管理虚拟 IP。

**准备工作**

当待部署集群为 **5.2.0 ~ 5.6.1** 版本时，请根据如下指示升级相关 RPM 文件。您可以选择在一个节点或每个节点升级 RPM 文件，建议在所有节点都执行升级操作，以确保每个节点的 cloudtower-installer 版本一致。

打开终端命令行工具，使用 SCP 命令将 CloudTower Installer 相关 RPM 文件上传至块存储集群待访问节点的 `/home/smartx/` 目录下，然后登录此节点，根据集群的服务器架构、版本和操作系统，升级集群的 RPM。其中 **Cluster\_Node\_IP** 表示集群节点的块存储集群管理 IP。

- **服务器 CPU 架构为 Intel x86\_64 或 Hygon x86\_64**

  - SMTX ZBS 版本为 **5.2.0 ~ 5.4.1**，根据集群使用的主机操作系统（可通过执行 `cat /etc/os-release` 命令进行确认），选择升级对应的 RPM 文件。

    - **CentOS 操作系统**：`fisheye.SMTX_ZBS-5.1.0-rc15.x86_64.rpm` 和 `cloudtower-installer-1.0.5-rc8.x86_64.rpm`（RPM 文件）

      ```
      scp fisheye.SMTX_ZBS-5.1.0-rc15.x86_64.rpm smartx@Cluster_Node_IP:~/
      scp cloudtower-installer-1.0.5-rc8.x86_64.rpm smartx@Cluster_Node_IP:~/

      ssh smartx@Cluster_Node_IP
      sudo rpm -Uvh fisheye.SMTX_ZBS-5.1.0-rc15.x86_64.rpm
      sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.x86_64.rpm
      sudo service cloudtower-installer restart
      sudo service nginx reload
      ```
    - **openEuler 操作系统**：`fisheye.SMTX_ZBS-5.1.0-rc15.oe1.x86_64.rpm` 和 `cloudtower-installer-1.0.5-rc8.x86_64.rpm`（RPM 文件）

      ```
      scp fisheye.SMTX_ZBS-5.1.0-rc15.oe1.x86_64.rpm smartx@Cluster_Node_IP:~/
      scp cloudtower-installer-1.0.5-rc8.x86_64.rpm smartx@Cluster_Node_IP:~/

      ssh smartx@Cluster_Node_IP
      sudo rpm -Uvh fisheye.SMTX_ZBS-5.1.0-rc15.oe1.x86_64.rpm
      sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.x86_64.rpm
      sudo service cloudtower-installer restart
      sudo service nginx reload
      ```
  - SMTX ZBS 版本为 **5.5.0 ~ 5.6.1**，升级 `cloudtower-installer-1.0.5-rc8.x86_64.rpm`（RPM 文件）

    ```
    scp cloudtower-installer-1.0.5-rc8.x86_64.rpm smartx@Cluster_Node_IP:~/

    ssh smartx@Cluster_Node_IP
    sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.x86_64.rpm
    sudo service cloudtower-installer restart
    sudo service nginx reload
    ```
- **服务器 CPU 架构为鲲鹏 AArch64**

  - SMTX ZBS 版本为 **5.2.0 ~ 5.4.1**，根据集群使用的主机操作系统（可通过执行 `cat /etc/os-release` 命令进行确认），选择升级对应的 RPM 文件。

    - **CentOS 操作系统**：`fisheye.SMTX_ZBS-5.1.0-rc15.aarch64.rpm` 和 `cloudtower-installer-1.0.5-rc8.aarch64.rpm`（RPM 文件）

      ```
      scp fisheye.SMTX_ZBS-5.1.0-rc15.aarch64.rpm smartx@Cluster_Node_IP:~/
      scp cloudtower-installer-1.0.5-rc8.aarch64.rpm smartx@Cluster_Node_IP:~/

      ssh smartx@Cluster_Node_IP
      sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.aarch64.rpm
      sudo rpm -Uvh fisheye.SMTX_ZBS-5.1.0-rc15.aarch64.rpm
      sudo service cloudtower-installer restart
      sudo service nginx reload
      ```
    - **openEuler 操作系统**：`fisheye.SMTX_ZBS-5.1.0-rc15.oe1.aarch64.rpm` 和 `cloudtower-installer-1.0.5-rc8.aarch64.rpm`（RPM 文件）

      ```
      scp cloudtower-installer-1.0.5-rc8.aarch64.rpm smartx@Cluster_Node_IP:~/
      scp fisheye.SMTX_ZBS-5.1.0-rc15.oe1.aarch64.rpm smartx@Cluster_Node_IP:~/

      ssh smartx@Cluster_Node_IP
      sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.aarch64.rpm
      sudo rpm -Uvh fisheye.SMTX_ZBS-5.1.0-rc15.oe1.aarch64.rpm
      sudo service cloudtower-installer restart
      sudo service nginx reload
      ```
  - SMTX ZBS 版本为 **5.5.0 ~ 5.6.1**，升级 `cloudtower-installer-1.0.5-rc8.aarch64.rpm`（RPM 文件）。

    ```
    scp cloudtower-installer-1.0.5-rc8.aarch64.rpm smartx@Cluster_Node_IP:~/

    ssh smartx@Cluster_Node_IP
    sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.aarch64.rpm
    sudo service cloudtower-installer restart
    sudo service nginx reload
    ```

**操作步骤**

通过 CloudTower Installer 在 SMTX OS 集群和 SMTX ZBS 集群中部署 CloudTower 的流程完全相同。您可以在浏览器中输入网址 <https://SMTX_ManageIP_Address/cloudtower-installer/?hypervisor=OTHER&username=root&password=abc123>，进入 CloudTower Installer。

![](https://cdn.smartx.com/internal-docs/assets/55fa06eb/tower_installation_guide_001.png)

请参考[通过 CloudTower Installer 安装部署](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_09)的**操作步骤**完成 CloudTower 的部署。

> **说明：**
>
> - *`SMTX_ManageIP_Address`* 表示 SMTX ZBS 块存储集群节点的块存储集群管理 IP。
> - *`username=root`* 表示 SMTX ZBS 集群超级管理员 root。
> - *`password=abc123`* 表示 SMTX ZBS 集群超级管理员 root 的密码，输入网址时请使用实际的密码替换 `abc123`。若密码包括除数字和字母以外的特殊字符，请先对密码进行 URL 编码，再将 `abc123` 替换为编码后的密码。
> - 如果 SMTX ZBS 集群为 5.3.0 及以上版本，且在部署 CloudTower 前已设置集群的管理虚拟 IP，进入 CloudTower Installer 后，系统将不再要求输入集群的管理虚拟 IP。请直接选择**全新 CloudTower 环境**，单击**下一步**，完成剩余的设置。

---

## 部署单点 CloudTower > 执行部署 > 在 SMTX ELF 集群中部署 CloudTower

# 在 SMTX ELF 集群中部署 CloudTower

**前提条件**

- 根据集群的服务器 CPU 架构，已提前下载 `tar.gz` 格式的 CloudTower 安装映像文件，若部署的 SMTX ELF 集群为 6.0.0 ~ 6.1.1 版本，还需下载集群对应的 CloudTower Installer 相关 RPM 文件。
- 已规划 CloudTower 的 IP 地址、子网掩码和网关，以及集群管理虚拟 IP。

**准备工作**

当待部署集群为 **6.0.0 ~ 6.1.1** 版本时，请根据如下指示升级相关 RPM 文件。您可以选择在一个节点或每个节点升级 RPM 文件，建议在所有节点都执行升级操作，以确保每个节点的 cloudtower-installer 版本一致。

打开终端命令行工具，使用 SCP 命令将集群对应的 CloudTower Installer 相关 RPM 文件上传至集群待访问节点的 `/home/smartx/` 目录下，然后登录此节点，根据集群的服务器架构、版本和操作系统，升级对应的 RPM 文件。其中 **Cluster\_Node\_IP** 表示集群节点的管理 IP。

- **服务器 CPU 架构为 Intel x86\_64、AMD x86\_64、Hygon x86\_64 或兆芯 x86**，升级 `cloudtower-installer-1.0.5-rc8.x86_64.rpm`（RPM 文件）。

  ```
  scp cloudtower-installer-1.0.5-rc8.x86_64.rpm   smartx@Cluster_Node_IP:~/

  ssh smartx@Cluster_Node_IP
  sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.x86_64.rpm
  sudo service cloudtower-installer restart
  sudo service nginx reload
  ```
- **服务器 CPU 架构为鲲鹏 AArch64**，升级 `cloudtower-installer-1.0.5-rc8.aarch64.rpm`（RPM 文件）。

  ```
  scp cloudtower-installer-1.0.5-rc8.aarch64.rpm   smartx@Cluster_Node_IP:~/

  ssh smartx@Cluster_Node_IP
  sudo rpm -Uvh cloudtower-installer-1.0.5-rc8.aarch64.rpm
  sudo service cloudtower-installer restart
  sudo service nginx reload
  ```

**操作步骤**

通过 CloudTower Installer 在 SMTX OS 集群和 SMTX ELF 集群中部署 CloudTower 的流程完全相同。你可以根据部署的 SMTX ELF 集群版本，在浏览器中输入相应网址进入 CloudTower Installer。

- **6.3.0 及以上的 6.x.x 版本**

  <https://SMTX_ManageIP_Address/operation-center-installer>

  进入 CloudTower Installer 之后，需要输入 SMTX ELF 集群超级管理员账号 root 及对应的密码，并单击下一步进行校验。校验通过之后才能继续 CloudTower 的安装。
- **6.2.0 及以上的 6.2.x 版本**：

  <https://SMTX_ManageIP_Address/operation-center-installer/?hypervisor=ELF&username=root&password=abc123>
- **6.2.0 以下版本**：

  <https://SMTX_ManageIP_Address/cloudtower-installer/?hypervisor=ELF&username=root&password=abc123>

请参考[通过 CloudTower Installer 安装部署](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_09)的**操作步骤**完成 CloudTower 的部署。

> **说明：**
>
> - *`SMTX_ManageIP_Address`* 表示 SMTX ELF 集群节点的管理 IP。
> - *`username=root`* 表示 SMTX ELF 集群超级管理员 root。
> - *`password=abc123`* 表示 SMTX ELF 集群超级管理员 root 的密码，输入网址时请使用实际的密码替换 `abc123`。若密码包括除数字和字母以外的特殊字符，请先对密码进行 URL 编码，再将 `abc123` 替换为编码后的密码。
> - 若部署 CloudTower 前已设置集群的管理虚拟 IP，进入 CloudTower Installer 后，系统将不再要求输入集群的管理虚拟 IP。请直接选择**全新 CloudTower 环境**，单击**下一步**，完成剩余的设置。

---

## 部署 CloudTower 高可用集群

# 部署 CloudTower 高可用集群

本章介绍 CloudTower 高可用集群的部署流程。您将首先部署并初始化一个满足规格要求的单点 CloudTower，随后通过管理界面将其扩展为包含被动节点与仲裁节点的高可用集群。

> **注意**：
>
> CloudTower HA 集群不支持部署 **SMTX Kubernetes 服务**，如果您需要使用 CloudTower 部署 SMTX Kubernetes 服务，请务必选择**单点模式**进行部署。

---

## 部署 CloudTower 高可用集群 > 部署流程概览

# 部署流程概览

CloudTower 高可用集群的整体部署流程如下：

**阶段一：准备单点 CloudTower**

首先准备一个满足 HA 规格的单点 CloudTower，在启用高可用后，该节点将作为主动节点。您既可以全新部署一个节点，也可以将现有的存量节点升级至最新版本。

> **注意**：
>
> 若使用存量节点，请确保其满足主动节点的配置要求。

**阶段二：安装被动节点**

初始化并登录 CloudTower，在已关联集群中完成被动节点的部署。

**阶段三：安装仲裁节点**

部署一个满足 HA 规格的仲裁节点，并配置 HA IP。

**阶段四：启用高可用**

完成所有节点的部署之后，根据界面指引完成高可用功能的启用。

---

## 部署 CloudTower 高可用集群 > 部署前的准备和要求

# 部署前的准备和要求

在正式部署前，请按照以下要求完成部署前准备。

---

## 部署 CloudTower 高可用集群 > 部署前的准备和要求 > 规划节点部署位置

# 规划节点部署位置

为了满足不同业务连续性等级的要求，您可以灵活规划主动节点、被动节点和仲裁节点的物理部署位置，以实现主机级、集群级或数据中心级的容灾能力。

根据容灾级别的不同，支持以下三种部署模式：

- **主机级别容灾**

  将三个节点分散部署在同一集群的不同主机上，以规避单台物理主机宕机导致服务中断的风险。
- **集群级别容灾**

  将三个节点分别部署在不同集群的主机中，以规避因存储池故障、集群网络瘫痪等原因导致单集群整体不可用的风险。
- **数据中心级别容灾**

  将主动节点和被动节点部署在同城中两个不同的数据中心，仲裁节点部署在第三站点。该方案可提供最高级别的容灾能力，抵御单个数据中心整体断电或断网的风险。

下面以一个典型示例说明 CloudTower 高可用集群的组成架构。

![](https://cdn.smartx.com/internal-docs/assets/55fa06eb/tower_installation_guide_003.png)

> **组件部署说明**：
>
> - CloudTower 高可用集群的主动节点和被动节点分别部署在故障域 A 和故障域 B，仲裁节点部署在和两个故障域之外的第三故障域 C。主动节点和被动节点仅支持部署在 SMTX OS（ELF）集群和 SMTX ELF 集群中，仲裁节点支持部署在任意类型的集群（包括 SmartX 集群和第三方集群）中。
> - Everoute Controller 工作节点在两个故障域内对等部署，其仲裁节点复用 CloudTower 仲裁节点，其对于 IP 地址分配的要求请参考[规划 IP 地址](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_29)小节。
> - 若环境中部署了双活集群，则双活集群仲裁节点部署在第三故障域 C。

---

## 部署 CloudTower 高可用集群 > 部署前的准备和要求 > 环境配置要求

# 环境配置要求

HA 集群中的每个节点的环境配置要求如下，请确保 CloudTower 所在的集群有足够的资源（CPU、内存和存储空间）可分配给部署 CloudTower 的虚拟机。

| 节点类型 | 配置等级 | CloudTower 虚拟机占用的资源 |
| --- | --- | --- |
| 主动节点 | 高配 | - 8 核 vCPU - 19 GiB 内存 - 400 GiB 存储空间 |
| 被动节点 | 高配 | - 8 核 vCPU - 19 GiB 内存 - 400 GiB 存储空间 |
| 仲裁节点 | - | - 4 核 vCPU - 8 GiB 内存 - 200 GiB 存储空间 |

> **说明**：
>
> 被动节点的环境配置需要和主动节点保持一致。若在部署后，主动节点的环境配置所有调整，则被动节点也需要同步调整。

---

## 部署 CloudTower 高可用集群 > 部署前的准备和要求 > 规划网络 > 网络类型与网络拓扑

# 网络类型与网络拓扑

CloudTower 高可用集群涉及两种独立网络：HA 网络和 CloudTower 管理网络（简称“管理网络”）。

- **HA 网络**

  主要用于节点间内部通信，包括状态同步、心跳检测与健康状态上报。
- **管理网络**

  主要用于提供外部访问入口（如客户端、管理工具等），以及作为 CloudTower 与被管集群之间的管理通信通道。

CloudTower 高可用集群支持多种[网络部署模式](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_49)。下图展示了模式二（即管理网络和 HA 网络分别属于不同网段，且三个 HA IP 同子网）的拓扑示例。

![](https://cdn.smartx.com/internal-docs/assets/55fa06eb/tower_installation_guide_004.png)

---

## 部署 CloudTower 高可用集群 > 部署前的准备和要求 > 规划网络 > 网络部署模式

# 网络部署模式

根据网络拓扑可知，每个节点需要配置的 IP 如下：

| 节点类型 | HA IP | 管理 IP |
| --- | --- | --- |
| 主动节点 | ✓ | ✓  **说明**：  若采用旧版本升级的方式准备单点 CloudTower，则无需规划管理 IP。启用高可用后，CloudTower 的 IP 地址将自动作为主动节点的管理 IP。 |
| 被动节点 | ✓ | ✓  **说明**：  被动节点和主动节点使用同一个管理 IP，无需配置独立的管理 IP。 |
| 仲裁节点 | ✓ | - |

支持以下五种网络部署模式，每种部署模式的 IP 地址分配要求如下：

| 网络部署模式 | IP 地址分配要求 |
| --- | --- |
| 模式一 | 管理 IP 与三个节点的 HA IP 均位于同一子网。 |
| 模式二 | 管理 IP 独立子网，三个 HA IP 位于同子网。 |
| 模式三 | 管理 IP、主动节点 HA IP、被动节点 HA IP、仲裁节点 HA IP 分别位于不同子网。 |
| 模式四 | 管理 IP 独立子网，主动节点 HA IP、被动节点 HA IP、仲裁节点 HA IP 任意两个同子网。 |
| 模式五 | 管理 IP、主动节点 HA IP、被动节点 HA IP 位于同一子网，仲裁节点 HA IP 独立子网。 |

---

## 部署 CloudTower 高可用集群 > 部署前的准备和要求 > 规划网络 > 网络配置要求

# 网络配置要求

部署前请根据网络部署模式在待部署集群中创建相应的虚拟机网络，要求如下：

| 网络类型 | 网络要求 | 带宽要求 | 网络延时 |
| --- | --- | --- | --- |
| HA 网络 | - VLAN 类型为 Access。 - HA 集群的三个节点之间可通过 L3 层 HA 网络进行连接。 | HA 网络和管理网络的带宽均不低于 **1 Gbps**。 | CloudTower HA 集群内各个节点间的 HA 网络和管理网络 ping 延时在 **10 ms** 及以下。 |
| 管理网络 | - VLAN 类型为 Access。 - CloudTower 管理网络必须与被管集群的管理网络实现 L3 层网络互通。 |

> **说明**：
>
> HA 网络和管理网络之间没有连通性要求，可以部署在同一网段或不同网段。

---

## 部署 CloudTower 高可用集群 > 部署前的准备和要求 > 规划网络 > 规划 IP 地址

# 规划 IP 地址

各节点的 IP 地址规划如下表所示：

| 节点类型 | 网络类型 | IP 地址 | 子网掩码 | 网关 | VLAN ID（可选） |
| --- | --- | --- | --- | --- | --- |
| 主动节点 | HA 网络 | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| 管理网络 | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| 被动节点 | HA 网络 | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| 管理网络 | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |
| 仲裁节点 | HA 网络 | xx.xx.xx.xx | xx.xx.xx.xx | xx.xx.xx.xx | xx |

网络管理员在分配节点的 HA IP 和管理 IP 时，必须遵循以下规则：

- HA IP 和管理 IP 均为静态 IP 地址。
- 若三个节点所属的 HA 网络不满足 L2 层互通，则必须为每个节点配置网关以确保可达性。
- Everoute Controller 仲裁节点支持复用 HA 仲裁节点，复用时，请确保高可用集群的管理网络和 HA 网络三层连通。
- 上述 IP 地址不能与以下 CIDR 范围内的任何 IP 地址重叠：
  - 169.254.0.0/16
  - 240.0.0.0/4
  - 224.0.0.0/4
  - 198.18.0.0/15
  - 127.0.0.0/8
  - 0.0.0.0/8

---

## 部署 CloudTower 高可用集群 > 部署前的准备和要求 > 规划网络 > 规划防火墙端口

# 规划防火墙端口

为了确保 CloudTower 高可用集群的正常运行及相应功能的正常使用，请在配置网络防火墙时，确保以下源端到目标端的端口通信畅通。

## **基础端口**

基础端口主要用于 CloudTower 与被管集群之前的通信，以及巡检服务和升级中心服务与被管理的集群相互通信。当**主动节点**和**被动节点**作为源端或目标端时，需要开放的基础端口请参考部署单点 CloudTower 的[规划并开放网络端口](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_06)。

## **高可用相关端口**

高可用相关端口主要用于集群内部节点通信（如节点间的心跳、数据同步）、客户端对管理平台的访问、以及系统服务和主被节点间的通信。

- **HA 集群内部通信**

  - **目标端为主动节点或被动节点**

    | 源端 | 类型 | 端口 | 说明 |
    | --- | --- | --- | --- |
    | 主动节点、被动节点或仲裁节点 | TCP | 22 | SSH 远程登录端口 |
    | 主动节点、被动节点或仲裁节点 | TCP | 80、443 | 内部 API 路由：集群内微服务间的 API 调用转发及组件健康检查 |
    | 主动节点或被动节点 | TCP | 2379 | Kubernetes 状态数据存储服务端口 |
    | 主动节点或被动节点 | TCP | 5050 | 主机代理端口，用于执行节点层面的管理操作 |
    | 主动节点或被动节点 | TCP | 5051 | HA 控制器端口，用于执行故障切换相关操作 |
    | 主动节点、被动节点或仲裁节点 | TCP | 5432 | 数据库端口，用于数据库主被复制与状态同步 |
    | 主动节点或被动节点 | UDP | 6081 | 容器网络通信端口（Overlay） |
    | 主动节点或被动节点 | TCP | 6443 | Kubernetes API 端口 |
    | 主动节点或被动节点 | TCP | 8428 | VictoriaMetrics 端口，用于存储监控指标 |
    | 主动节点或被动节点 | TCP | 8888 | 内部文件服务端口 |
    | 主动节点或被动节点 | TCP | 9000 | CloudTower 管理服务端口，用于提供初始化配置与引导服务 |
    | 主动节点、被动节点或仲裁节点 | TCP | 9428 | VictoriaLogs 端口，用于存储日志数据 |
    | 主动节点或被动节点 | TCP | 9443 | Kubernetes CNI 控制器端口，用于管理网络策略 |
    | 主动节点或被动节点 | TCP | 10250 | kubelet 端口，用于管理 Pod 生命周期 |
    | 主动节点或被动节点 | TCP | 10254 | Ingress 健康检查端口 |
    | 主动节点或被动节点 | TCP | 10256 | kube-proxy 健康检查端口 |
    | 主动节点、被动节点或仲裁节点 | UDP | 30123 | NTP 时间同步服务端口 |
  - **目标端为仲裁节点**

    | 源端 | 类型 | 端口 | 说明 |
    | --- | --- | --- | --- |
    | 主动节点或被动节点 | TCP | 22 | SSH 远程登录端口 |
    | 主动节点或被动节点 | TCP | 5433 | Postgresql 仲裁服务端口，用于监听主被节点状态并参与仲裁投票 |

    > **说明**：
    >
    > 当 Everoute Controller 仲裁节点复用 HA 仲裁节点时，需要在仲裁节点开放 Everoute 相关端口，请参考《Everoute 安装与升级指南》的**规划端口**小节。
- **客户端及系统服务通过管理 IP 访问**

  **目标端为主动节点或被动节点**

  | 源端 | 类型 | 端口 | 说明 |
  | --- | --- | --- | --- |
  | 客户端 | TCP | 80、443 | Web 控制台访问端口，提供 HTTP 自动跳转及 HTTPS 管理界面访问服务 |
  | 客户端 | TCP | 3000 | 监控日志可视化服务端口 |
  | 客户端 | TCP | 9000 | CloudTower 管理服务端口，用于访问 CloudTower 安装与配置引导界面 |
  | 备份服务虚拟机 | TCP | 31443 | 备份许可服务端口，提供备份许可验证功能 |

---

## 部署 CloudTower 高可用集群 > 部署前的准备和要求 > 软件与兼容性要求

# 软件与兼容性要求

部署 CloudTower 高可用集群之前，请确保软件的版本、许可满足要求，并获取满足 CPU 架构和操作系统要求的安装文件。

## 软件与兼容性要求

- **软件版本与许可**

  部署高可用集群需要使用 4.8.0 及以上版本的 CloudTower 企业版软件。请在部署前确认软件许可满足要求。
- **CPU 架构要求**

  高可用集群中的所有节点（主动节点、被动节点和仲裁节点）必须使用相同的 CPU 架构。

  - 如果主动节点部署在 x86\_64 架构的集群中，被动节点和仲裁节点也必须部署在 x86\_64 架构的集群中。
  - 不支持混合部署（如 x86\_64 与 aarch64 混用）。
- **操作系统限制**

  不支持使用主机操作系统为 `TencentOS` 的安装文件进行安装。

## 获取安装文件

请根据节点类型，参考下表准备对应的安装文件：

| 节点类型 | 安装文件要求 |
| --- | --- |
| 主动节点 | - **全新部署**：请参考部署单点 CloudTower 的[要求](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_03)，获取适配目标集群环境（SMTX OS 集群或 SMTX ELF 集群）的安装文件。 - **旧版本升级**：无需获取安装文件，请直接参考[升级 CloudTower](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_04) 章节进行操作。 |
| 被动节点和仲裁节点 | 请下载与主动节点 CPU 架构和操作系统一致的 CloudTower **ISO 映像文件**。 |

---

## 部署 CloudTower 高可用集群 > 准备单点 CloudTower

# 准备单点 CloudTower

准备一个满足 HA 规格的单点 CloudTower，在启用高可用后，该节点将作为高可用集群的主动节点。您可以通过旧版本升级或全新部署的方式进行准备，若采用全新部署的方式，请确保已规划主动节点的管理 IP，并提前获取 CloudTower 安装文件。

**操作步骤**

准备一个单点 CloudTower，其规格和配置要求如下：

| 要求 | 描述 |
| --- | --- |
| 版本和许可 | CloudTower 版本需为 4.8.0 及以上，软件许可为企业版且在有效期内。 |
| 运行环境 | 部署集群为 SMTX OS（ELF）集群或 SMTX ELF 集群，且已和当前 CloudTower 关联。 |
| 操作系统 | CloudTower 虚拟机的操作系统为 `CentOS` 或 `openEuler`，不支持 TencentOS。 |
| 环境配置 | 高配：vCPU >= 8 核、内存 >= 19 GiB、存储空间 >= 400 GiB。 |
| 文件系统 | 系统盘文件系统必须为 `ext4`，不支持 `XFS`。  **说明**：  对于 4.8.0 以下版本的 CloudTower，若采用通过 CloudTower Installer 安装部署，则系统盘文件系统为 `XFS`；若采用手动创建虚拟机进行部署，则系统盘文件系统为 `ext4`。 |
| 系统服务部署限制 | 环境中未部署 SMTX Kubernetes 服务。 |

请根据您的实际情况，选择以下一种方式准备单点 CloudTower。

- **方式一：旧版本升级**

  若您环境中已存在单点 CloudTower，请先仔细核对上述要求，若满足所有条件，则请参考[升级 CloudTower 章节](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_04)将其升级至最新版本。对于部分条件，若不满足，可以通过执行相应操作进行变更后进行升级：

  - **软件许可**：通过更新许可码将许可类型变更为企业版。
  - **环境配置**：通过修改环境配置增加 vCPU、内存和存储空间分配。

  若不满足，则请采用方式二重新部署。
- **方式二：全新部署**

  请参考[部署单点 CloudTower](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_08) 章节的步骤执行部署，并在部署后完成 CloudTower 的初始化和登录。

**配置结果**

已配置 CloudTower IP，该 IP 地址将作为主动节点的管理 IP。

---

## 部署 CloudTower 高可用集群 > 安装被动节点

# 安装被动节点

准备好单点 CloudTower 后，请按照如下步骤在 CloudTower 已关联集群中安装被动节点。

**前提条件**

- 被动节点待部署的集群已和当前 CloudTower 关联。
- 已提前下载和主动节点 CPU 架构和操作系统相同的 CloudTower ISO 映像。

**操作步骤**

1. 将 CloudTower ISO 映像上传至内容库并分发至待部署集群。
2. 创建空白虚拟机，并设置以下参数：

   | 配置信息 | 配置要求 |
   | --- | --- |
   | 基本信息 | 根据规划的节点位置，选择待部署的 SMTX OS（ELF）集群或 SMTX ELF 集群，并设置虚拟机名称。 |
   | 计算资源 | 和已部署的单点 CloudTower 保持一致。（**vCPU 分 配** >= 8 vCPU，**内存分配** >= 19 GiB） |
   | 磁盘 | - 虚拟卷的**容量**和已部署的单点 CloudTower 保持一致。（容量 >= 400 GiB） - 载入 CloudTower ISO 映像。 |
   | 网络设备 | **删除**默认添加的虚拟网卡。 |
   | 其他配置 | 建议采用系统默认的参数值。 |

**配置结果**

被动节点未安装任何虚拟网卡。

> **注意**：
>
> 请确保被动节点在此阶段未配置任何网络，其网络配置将在**启用 CloudTower 高可用**阶段完成。

---

## 部署 CloudTower 高可用集群 > 安装仲裁节点

# 安装仲裁节点

仲裁节点支持安装在 SmartX 集群或第三方集群，请参考如下步骤进行操作。

**前提条件**

- 已规划仲裁节点的 HA IP、子网掩码和网关。
- 已提前下载和主动节点 CPU 架构和操作系统相同的 CloudTower ISO 映像。

**操作步骤**

部署一个满足如下要求的 CloudTower 虚拟机。

- **环境配置要求**：vCPU >= 4 核、内存 >= 8 GiB、存储空间 >= 200 GiB。
- **网络要求**：配置虚拟网卡，并设置 HA IP、子网掩码和网关，要求 HA IP 为静态 IP。
- **ISO 映像**：使用提前获取的 **CloudTower ISO 映像**进行安装。

**配置结果**

仲裁节点配置了 HA IP。

---

## 部署 CloudTower 高可用集群 > 启用 CloudTower 高可用

# 启用 CloudTower 高可用

完成所有节点的部署后，您可根据如下步骤在 CloudTower 管理页面完成高可用的启用。

**前提条件**

- 当前 CloudTower 所在集群已和 CloudTower 关联。
- 当前 CloudTower 已配置管理 IP、仲裁节点已配置 HA IP，并提前获取规划的主动节点和被动节点的 HA IP。
- 请提前获取被动节点所在虚拟机的名称。
- 请确保网络连通性正常。
- CloudTower 未处于升级中状态。
- 当前账号具有 CloudTower 高可用管理的操作权限，若没有，请联系管理员获取。

**准备工作**

启用高可用将触发数据同步与集群组建。为确保操作顺利完成，并规避因意外情况导致的环境不可用风险，请务必提前完成如下准备工作：

- **创建 CloudTower 虚拟机快照**（推荐）

  建议在启用之前，手动为当前 CloudTower 创建虚拟机快照。若启用过程中出现异常，可通过快照快速将环境恢复至初始状态。
- **校准 CloudTower 时间**

  为了确保 CloudTower 高可用顺利启用，需要确保 CloudTower 时间的准确性。

  - 若当前 CloudTower 未配置 NTP 服务器，请参考[配置 NTP 服务器](/cloudtower/4.8.0/cloudtower_user_guide/cloudtower_user_guide_114)章节完成配置。建议为 CloudTower 配置至少三个 NTP 服务器。
  - 若当前 CloudTower 已配置 NTP 服务器，请在**系统配置** > **CloudTower 时间**页面确认 CloudTower 时间是否和 NTP 服务器时间保持同步。若二者偏差过大，则请参考[校准单点 CloudTower 的系统时间](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_45)小节手动校准时间。

**操作步骤**

1. 在 CloudTower 的**系统配置**主页面单击左侧导航栏中的 **CloudTower 高可用**，进入 **CloudTower 高可用（HA）** 页面。
2. 单击 **CloudTower 高可用（HA）** 页面的**启用高可用**，弹出**启用 CloudTower 高可用**对话框。
3. 为主动节点配置 HA 网络。根据网络规划，选择使用主动节点的管理网络或使用其他虚拟机网络。

   - **使用主动节点的管理网络**：

     配置提前规划的 IP 地址。
   - **使用其他虚拟机网络**：

     选择虚拟机网络，并配置 IP 地址、子网掩码和默认网关。
4. 选择作为被动节点的虚拟机，并为其配置管理网络和 HA 网络。

   - **管理网络**

     根据规划 IP 地址可知，被动节点的管理 IP 和主动节点相同，因此您只需选择管理网络，无需手动配置 IP 地址、子网掩码和默认网关。
   - **HA 网络**

     根据网络规划，选择提前创建的 HA 网络，并输入 IP 地址、子网掩码和默认网关。
5. 输入仲裁节点的 HA IP，以将仲裁节点关联至 HA 集群。
6. 单击**启用**。

**查看启用进度**

单击启用后，可在 CloudTower 高可用页面查看启用进度。若在网络配置或部署前检查阶段失败，可根据提示解决问题后进行重试：

- **网络配置**：单击启用失败提示信息右侧的**重试**按钮，在弹出的**启用 CloudTower 高可用**对话框中重新编辑配置信息。编辑完成后单击**启用**，以重新发起启用任务。
- **部署前检查**：根据启用进度条下方展示的异常检查项，进行问题排查和修复。解决后单击启用失败提示信息右侧的**重试**按钮，在弹出的**启用 CloudTower 高可用**对话框中单击**启用**，以重新发起启用任务。

> **说明**：
>
> - 启用期间请勿进行业务变更，启用过程中，CloudTower 将短暂无法访问，完成启用后即可正常访问 CloudTower。
> - 完成启用后，请及时将 CloudTower 和 1.2.0 及以上版本的可观测性服务关联，以获取高可用相关的报警信息。

启用后，您可在 **CloudTower 高可用（HA）** 页面查看 HA 集群的基本信息和主被切换记录，详细信息请参考《CloudTower 使用指南》的**管理 CloudTower 高可用**章节。

---

## 部署 CloudTower 高可用集群 > 高可用集群运维注意事项

# 高可用集群运维注意事项

启用高可用功能后，CloudTower 集群的架构与单点模式有显著差异。为了保障集群的稳定性及数据一致性，严禁在任意节点执行以下操作：

- 修改任意节点（主动节点、被动节点或仲裁节点）的管理 IP、HA IP 或网关地址。
- 使用命令行工具对 CloudTower 虚拟机进行导入导出操作。
- 修改任意节点的操作系统主机名称。
- 修改 CloudTower 时区。

---

## 升级 CloudTower

# 升级 CloudTower

CloudTower 支持通过命令行和管理界面的方式进行升级，请根据当前 CloudTower 的版本选择相应方式进行升级。

对于 4.6.0 以下版本的 CloudTower 仅支持通过命令行进行升级，4.6.0 及以上版本的 CloudTower 支持通过命令行和管理界面的方式升级至更高版本，建议您选择通过管理界面进行升级，以获得更加简单、可靠、透明和可观测的升级体验。

**注意事项**

- 将 CloudTower 从 4.6.0 以下版本升级至本版本之后，请及时执行以下操作以确保相应功能正常运行：

  - 将部署的 CloudTower 代理升级至 1.3.0 及以上版本，否则将影响数据传输。
  - 手动启用事件保留策略并设置事件保留范围，详情请参考[设置事件保留策略](/cloudtower/4.8.0/cloudtower_user_guide/cloudtower_user_guide_132)。
  - 开放 CloudTower 虚拟机的 `9000` 端口，否则无法正常查看 CloudTower 升级进度。
- 若 CloudTower 正在启用高可用，则在启用完成之前无法进行升级操作，请在完成启用后执行升级。
- 若 CloudTower 当前版本为 **4.7 P2**，则不支持升级至本版本，建议升级至 **4.8 P1** 及以上版本。

---

## 升级 CloudTower > 通过命令行升级 CloudTower

# 通过命令行升级 CloudTower

## 升级前的准备

在升级前，请登录 CloudTower 虚拟机后执行如下命令，确认当前 CloudTower 的版本和主机操作系统，并结合集群的服务器 CPU 架构，做好相应的准备。其中 `USER_NAME` 表示CloudTower 虚拟机操作系统的默认账户名、`TOWER_IP` 表示待升级的 CloudTower IP。

```
ssh USER_NAME@TOWER_IP
sudo su
# check cloudtower version
/usr/share/smartx/tower/installer/binary/installer info
# check os release version
cat /etc/os-release | grep ^NAME
```

- 根据集群的服务器 CPU 架构和 CloudTower 的主机操作系统，提前下载适配的 `tar.gz` 格式的软件升级文件。
- 若当前 CloudTower 的版本为 2.8.0 及以下，还需根据当前 CloudTower 的环境配置，手动修改 CloudTower 虚拟机的内存。若需要将 CloudTower 的环境配置从**低配**变更为**高配**，请在升级结束后，参考[变更 CloudTower 环境配置](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_07)进行操作。

  - **低配**：内存从 8 GiB 调整为 12 GiB
  - **高配**：内存从 16 GiB 调整为 19 GiB

  更新虚拟机配置后，重启虚拟机并等待 CloudTower 服务恢复正常。

## 升级步骤

以软件升级文件 **0\_x\_x-v4.8.0.upgrade.centos7.x86\_64.tar.gz** 为例，介绍在将此升级文件下载到本地后，升级 CloudTower 的操作步骤。执行升级操作时，请将下述命令中的 **0\_x\_x-v4.8.0.upgrade.centos7.x86\_64.tar.gz** 替换为实际的软件升级文件名称。

1. 打开终端命令行工具，使用 SCP 命令将软件升级文件上传至待升级 CloudTower 所在的虚拟机的 `/usr/share/smartx` 目录下。其中 `USER_NAME` 表示CloudTower 虚拟机操作系统的默认账户名、`TOWER_IP` 表示待升级的 CloudTower IP。

   ```
   scp 0_x_x-v4.8.0.upgrade.centos7.x86_64.tar.gz USER_NAME@TOWER_IP:~/
   ssh USER_NAME@TOWER_IP
   sudo su
   mv 0_x_x-v4.8.0.upgrade.centos7.x86_64.tar.gz /usr/share/smartx
   cd /usr/share/smartx/
   tar xvf 0_x_x-v4.8.0.upgrade.centos7.x86_64.tar.gz
   ```
2. 执行以下命令，升级 Kernel。

   ```
   sh ./4_2_x_upgrade_kernel.sh
   ```

   若提示 `kernel has been upgraded, skip upgrade`，则直接执行步骤 3，否则需执行 `reboot`命令重启虚拟机。
3. 执行以下命令，进行 CloudTower 版本的升级。

   ```
   ssh USER_NAME@TOWER_IP
   sudo su
   cd /usr/share/smartx/
   sh ./upgrade-cloudtower.sh
   ```

   执行上述命令后，系统将首先对升级环境进行预检查。

   - 若检查通过，系统将开始升级 CloudTower。
   - 若检查未通过，界面将显示失败信息，请根据[预检查失败处理方式](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_04)的解决方案解决问题，并重新升级 CloudTower。

   升级过程大概持续 1 h。在升级过程中，可根据界面提示访问独立升级页面查看升级进度及升级过程中产生的日志。

   升级完成后，相关日志会存储至 CloudTower 所在虚拟机的 `/var/log/cloudtower/` 目录下查看升级的相关日志。若升级前的 CloudTower 版本为 4.7.0 及以上，则升级完成后，相关升级记录将展示在 **CloudTower 升级**页面的**升级记录**页签下。

   > **说明**：
   >
   > - 若升级前 CloudTower 虚拟机操作系统的默认账户为 `smartx`，则完成升级后，系统将在 CloudTower 虚拟机操作系统中新增账户 `cloudtower`，同时保留原有账户 `smartx`。
   > - 若升级前的 CloudTower 版本为 4.6.0 及以上，则在升级过程中，CloudTower 界面顶部将提示 CloudTower 正在升级，升级完成后即可正常访问 CloudTower。

---

## 升级 CloudTower > 通过管理界面升级 CloudTower

# 通过管理界面升级 CloudTower

当 CloudTower 为 4.6.0 及以上版本时，不仅支持通过命令行升级，还支持通过管理界面将 CloudTower 升级至更高版本。建议您选择通过管理界面进行升级，以获得更加简单、可靠、透明和可观测的升级体验。

**前提条件**

- 请根据当前 CloudTower 的 CPU 架构和操作系统提前获取对应的升级文件，包括 `.tar.gz` 和 `JSON` 格式的文件。
- 仅超级管理员、运维管理员和分配了**CloudTower 升级**权限的用户可以执行 CloudTower 升级操作，请确保当前用户拥有相应的操作权限，若没有，请提前联系管理员获取。
- 由于 CloudTower 虚拟机不支持通过管理界面进行快照回滚、备份或恢复操作，因此在升级之前请提前使用命令行工具导出 CloudTower 虚拟机。

**操作步骤**

**上传升级文件**

1. 在 CloudTower **系统配置**主页面左侧的导航栏选择 **CloudTower 升级**，进入 CloudTower 升级页面。该页面展示了当前 CloudTower 的版本、内核版本、CPU 架构和操作系统。
2. 在**升级**页签下上传 CloudTower 升级文件，系统将对升级文件进行校验。校验通过后，页面将展示预览信息，确认升级文件的信息后，单击**上传**。

> **说明**：
>
> 高可用集群模式下，系统执行故障转移可能导致已上传的 CloudTower 文件丢失。请在页面删除当前文件并重新上传后，再进行后续步骤。

**检查环境**（可选）

在执行升级之前，您可以单击**检查环境**对升级环境进行预检查，以降低正式升级失败的风险。当所有的检查项目通过之后，才可发起升级。若不通过，请根据页面展示的不满足要求的检查项进行问题定位，解决问题后再次单击**检查环境**。

**执行升级**

您也可以不进行升级环境预检查，直接进行升级操作。但若您在升级之前对目标环境进行过环境检查，则必须在环境检查通过之后，才可进行升级操作。

单击**升级**，在弹出的**升级 CloudTower** 对话框中单击**升级**发起升级。发起升级后，页面将提示 `CloudTower 正在升级`，系统将首先对升级环境进行预检查，预检查通过后将直接执行升级。

发起升级后，您可单击**查看详情**跳转至升级页面，输入 CloudTower 虚拟机账户 `cloudtower` 的密码后，单击**查看进度**即可查看环境检查进度和 CloudTower 的升级进度。若环境检查未通过，则升级任务失败，请根据 **CloudTower 升级**页面的提示解决问题后重新发起升级。

在升级过程中，CloudTower 主页面将暂时不可访问。升级过程中产生的日志将展示在升级进度条下方，您可输入关键字搜索目标日志。升级完成后，您可单击升级页面的**打开 CloudTower** 跳转至 CloudTower 主页面，刷新页面后即可正常使用 CloudTower。

升级完成后，相关升级记录将展示在 **CloudTower 升级**页面的**升级记录**页签下。

---

## 变更 CloudTower 的配置

# 变更 CloudTower 的配置

若关联 CloudTower 的 SmartX 集群所承载的业务发生变化，可能需要对 CloudTower 虚拟机的相关配置发生变更。

---

## 变更 CloudTower 的配置 > 变更 CloudTower 环境配置

# 变更 CloudTower 环境配置

随着纳管集群规模的扩大或业务需求的增长，您可能需要对 CloudTower 进行垂直扩容。本章详细介绍了如何通过调整 vCPU、内存及磁盘空间来变更 CloudTower 的资源规格。

由于单点模式与高可用集群模式的变更流程存在显著差异，请根据您当前的部署架构，参考对应章节进行操作。

---

## 变更 CloudTower 的配置 > 变更 CloudTower 环境配置 > 变更单点 CloudTower 的环境配置

# 变更单点 CloudTower 的环境配置

在 CloudTower 部署成功后，可以通过修改 CloudTower 虚拟机的配置，例如增加 vCPU、内存资源和磁盘空间，将其配置等级由**低配**变更为**高配**。两个等级的配置区别请参见[规划 CloudTower 环境配置等级](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_05)。

CloudTower 虚拟机的配置变更结束后，重启虚拟机并等待 CloudTower 服务恢复正常。然后执行以下命令，更新配置。

```
sudo bash
cd /usr/share/smartx/tower/installer/
./binary/installer update --components all
```

---

## 变更 CloudTower 的配置 > 变更 CloudTower 环境配置 > 变更高可用集群的环境配置

# 变更高可用集群的环境配置

在 HA 模式下，主动节点和被动节点的环境配置必须保持一致。您可以通过增加 vCPU、内存资源和磁盘空间，提高高配的资源占用以满足特定场景下的管理需求。

请按照以下顺序依次变更被动节点和主动节点的环境配置。

**被动节点**

1. 调整被动节点的 vCPU、内存或磁盘资源。
2. 若调整了节点的 vCPU，则重启虚拟机。
3. 在 **CloudTower 高可用**页面确认被动节点状态恢复正常后，再变更新主动节点的环境配置。

**主动节点**

1. 调整主动节点的 vCPU、内存或磁盘资源。
2. 若调整了节点的 vCPU，则重启虚拟机。
3. 在 **CloudTower 高可用**页面确认主动节点状态是否恢复正常。

---

## 变更 CloudTower 的配置 > 变更 CloudTower IP

# 变更 CloudTower IP

**前提条件**

请确保 CloudTower 未启用高可用功能。若 CloudTower 已启用高可用功能，则禁止修改任意节点（主动节点、被动节点和仲裁节点）的管理 IP 和 HA IP。

**注意事项**

- CloudTower IP 变更后，CloudTower 中部署的 Everoute 服务、备份或复制服务和 CloudTower 代理将不能使用，可分别参考这三个产品对应的运维手册进行处理。
- CloudTower IP 变更后，如果 CloudTower 与文件存储集群的文件管理网络无法连通，此时文件存储集群将显示为`异常`状态，但不影响挂载了该文件存储集群中文件系统的计算端使用存储。
- 若变更的 CloudTower IP 为已废弃的 CloudTower 的 IP，则在变更 IP 后，系统将在 CloudTower 的登陆界面自动填充原 CloudTower 的用户信息。请先单击**切换用户**，然后输入用户名和密码进行登录。

**操作步骤**

1. 登录 CloudTower 虚拟机 Guest OS，手动为 CloudTower 设置新的 IP。

   1. 使用 `cd /etc/sysconfig/network-scripts/` 命令，进入网口配置文件的访问路径。
   2. 使用 `vi ifcfg-<port>` 命令，打开网口的配置文件，重新设置 CloudTower IP，其中 `<port>` 表示该网口的名称（例如 `eth0`），`CloudTower_NewIP_address` 表示新的 CloudTower IP。

      ```
      IPADDR=CloudTower_NewIP_address
      ```
2. 根据 CloudTower 的主机操作系统，执行相应的命令，重启集群网络。

   - **OpenEuler & TencentOS 操作系统**

     ```
     systemctl restart NetworkManager
     ```
   - **CentOS 操作系统**

     ```
     systemctl restart network
     ```
3. 执行以下命令，更新 CloudTower 服务配置。

   ```
   cd /usr/share/smartx/tower/installer/ && ./binary/installer update-ip --vip $ip
   ```

---

## 配置系统设置

# 配置系统设置

本章介绍 CloudTower 基础系统环境的配置方法。包括如何通过 NTP 服务器校准 CloudTower 时间，以及如何配置 DNS 服务器以实现域名解析，确保 CloudTower 与外部服务的正常通信。

---

## 配置系统设置 > 校准 CloudTower 时间

# 校准 CloudTower 时间

精确的时间同步是 CloudTower 稳定运行的基础。正常情况下，CloudTower 会自动进行时间同步。若发现时间偏差较大或同步失效，请根据您实际的部署架构（单点模式或高可用集群模式），参考相应章节执行手动校准。

---

## 配置系统设置 > 校准 CloudTower 时间 > 校准单点 CloudTower 的时间

# 校准单点 CloudTower 的时间

当 CloudTower 时间与外部 NTP 服务器时间存在偏差时，将影响任务、监控等功能的时间显示，或造成备份与容灾、Kubernetes 等其他系统服务的功能异常。请按照以下步骤手动校准 CloudTower 的时间。

**前提条件**

请确保当前 CloudTower 已配置 NTP 服务器，若未配置，请参考[配置 NTP 服务器](/cloudtower/4.8.0/cloudtower_user_guide/cloudtower_user_guide_114)章节进行配置。

**注意事项**

校准过程涉及重启系统核心组件及所有服务容器。执行期间，CloudTower 管理界面将暂时无法访问，请务必在维护窗口进行操作。

**操作步骤**

1. SSH 登录至 CloudTower 虚拟机，并切换至 root 用户。
2. 执行如下命令查看当前同步状态：

   ```
   kubectl -n cloudtower-system exec svc/ntpm -- /app/ntpm server show
   ```
3. 若显示未同步或时间偏差较大，则请执行以下命令强制同步时间：

   ```
   kubectl -n cloudtower-system exec svc/ntpm  -- /app/ntpm server sync
   crictl rm -f $(crictl ps -a -q)
   systemctl restart kubelet containerd
   ```
4. 执行命令之后，请等待服务恢复自动恢复，然后在 CloudTower 的**系统配置** > **CloudTower 时间**页面确认时间是否已同步。

---

## 配置系统设置 > 校准 CloudTower 时间 > 校准高可用集群的系统时间

# 校准高可用集群的系统时间

CloudTower 高可用集群对时间精度高度敏感。当节点系统时间与外部 NTP 服务器时间存在偏差时，可能会导致节点运行状态误判、数据库同步异常或日志时间戳混乱。

如果集群出现上述异常，请按照以下步骤手动校准所有节点的系统时间。

> **注意**：
>
> 本操作包含重启虚拟机的步骤，重启虚拟机将触发故障转移。重启期间，CloudTower 管理服务将暂时中断，请务必在计划内维护窗口执行此操作。

**前提条件**

请确保当前 CloudTower 已配置 NTP 服务器，若未配置，请参考[配置 NTP 服务器](/cloudtower/4.8.0/cloudtower_user_guide/cloudtower_user_guide_114)章节完成配置。

**操作步骤**

1. SSH 登录至**主动节点**、**被动节点**和**仲裁节点**，并切换至 root 用户。
2. 在每个节点上执行相应命令以强制更新时间：

   - **主动节点**

     ```
     kubectl -n cloudtower-system exec svc/ntpm  -- /app/ntpm server sync
     ```
   - **被动节点和仲裁节点**

     ```
     systemctl stop chronyd
     chronyd -q
     rm -f /var/run/chronyd.pid
     systemctl restart chronyd
     ```
3. 按照**仲裁节点**、**被动节点**、**主动节点**的顺序依次重启虚拟机。

重启主动节点后，请待系统服务完全启动后，登录 CloudTower 查看高可用集群是否运行正常，以及 CloudTower 系统时间和 NTP 服务器时间是否同步。

---

## 配置系统设置 > 配置 DNS 服务器

# 配置 DNS 服务器

CloudTower 高可用集群支持配置 DNS 服务器以实现域名解析，确保 CloudTower 与外部服务（如 NTP 服务器、邮件服务器或 LDAP 认证服务器）的正常通信。

**前提条件**

已架设好可用的 DNS 服务器。

**注意事项**

该操作仅需在**主动节点**执行，配置的 DNS 设置会自动同步至被动节点和仲裁节点。

**操作步骤**

1. SSH 登录至**主动节点**，并切换至 root 用户。
2. 执行以下命令，查看当前配置：

   ```
   launcher nameserver list
   ```
3. 清除原有配置并配置新的 DNS 服务器。

   ```
   launcher nameserver clean # 清除现有配置
   launcher nameserver set --values "dns_ip" # 设置新的 DNS 服务器
   ```

   > **说明**：
   >
   > 请将 `dns_ip` 替换为实际的 IP 地址，如需配置多个 DNS 服务器，请使用 “,” 隔开。如 “114.114.114.114 , 114.114.114.115”。
4. 再次执行以下命令，确认配置生效：

   ```
   launcher nameserver list
   ```

---

## 附录 > 预检查失败处理方式

# 预检查失败处理方式

若安装或升级 CloudTower 失败，请根据日志提示的失败信息及下表中的解决方案解决问题，解决问题后再重新安装或升级 CloudTower。

| 失败信息 | 失败原因 | 解决方案 |
| --- | --- | --- |
| checkDiskSpace | CloudTower 虚拟机的磁盘空间不足。 | 1. 清理磁盘。可清理 /usr/share/smartx 路径下的 `0_x_x-xxxxx.tar.gz` 安装包文件。 2. 然后重新安装或升级 CloudTower：    - 执行以下**任意一条**命令安装 CloudTower：      - `./binary/installer deploy`      - `./binary/installer deploy --vip $VM_IP`    - 执行以下命令升级 CloudTower：  `cd /usr/share/smartx/`  `sh ./upgrade-cloudtower.sh` |
| checkPkgArchDist | CloudTower 安装文件或升级文件的主机操作系统和 CPU 架构与 CloudTower 虚拟机的 Linux 发行版本和主机 CPU 架构不符合。 | - 安装 CloudTower：   1. 依次执行如下命令获取 CloudTower 虚拟机的 Linux 发行版本和主机 CPU 架构。  `cat /etc/os-release | grep ^ID=`  `arch`   2. 获取符合要求的安装文件，并在已创建的 CloudTower 中重新加载 ISO。   3. 再次执行步骤 4 ~ 6，以重新安装 CloudTower - 升级 CloudTower：  依次执行如下命令获取 CloudTower 虚拟机的 Linux 发行版本和主机 CPU 架构，并重新上传符合要求的升级文件。然后重新执行步骤 1 ~ 3 进行升级。  `cat /etc/os-release | grep ^ID=`  `arch` |
| checkVmSpec | CloudTower 虚拟机分配的 CPU 和内存不满足要求。 | 1. 根据规划的 [CloudTower 环境配置](/cloudtower/4.8.0/tower_installation_guide/tower_installation_guide_05)，将 CPU 和内存扩容至满足要求的大小。 2. 然后执行以下命令重新安装或升级 CloudTower：    - **安装 CloudTower**（选择其中一条执行）：      - `./binary/installer deploy`      - `./binary/installer deploy --vip $VM_IP`    - **升级 CloudTower**：  `cd /usr/share/smartx/`  `sh ./upgrade-cloudtower.sh` |
| checkPackageVersion | CloudTower 升级文件的版本低于当前 CloudTower 的版本。 | 获取高于当前版本的 CloudTower 升级文件，并重新执行升级步骤，完成升级。 |
| checkCAPPDirectoryUsage | CloudTower 中用于存放部分系统服务安装包的目录大小超过 20 GB。 | 在 CloudTower 上删除未使用的系统服务安装包后，重新执行升级步骤，完成升级。 |
| checkIOWait | CloudTower 虚拟机 I/O 延迟超过 30 ms。 | 解决 I/O 性能问题后，重新执行安装或升级步骤。 |
| checkConflictingProcess | CloudTower 虚拟机内存在冲突的进程。 | 在 CloudTower 上手动终止冲突的进程后，重新执行升级步骤，完成升级。 |
| checkMagicPatch | CloudTower 中存在临时补丁。 | 移除 CloudTower 中的临时补丁后，重新执行升级步骤，完成升级。 |

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
