---
title: "SMTXOS/6.3.0/SMTX OS 特性说明"
source_url: "https://internal-docs.smartx.com/smtxos/6.3.0/os_property_notes/preface-generic"
sections: 96
---

# SMTXOS/6.3.0/SMTX OS 特性说明
## 关于本文档

# 关于本文档

SMTX OS（读作 SmartX OS）是由北京志凌海纳科技股份有限公司（以下简称 “SmartX” ）研发的超融合软件，提供分布式块存储、计算虚拟化和网络、数据保护及运维管理服务，可帮助企业快速构建稳定可靠的 IT 基础架构。

SMTX OS 支持如下几种关键特性：Boost 模式、双活特性、RDMA 功能、SR-IOV 特性、海光 HCT 特性、GPU 直通、vGPU 功能、常驻缓存模式和深度安全防护功能，通过启用以上特性，可以帮助 SMTX OS 集群增强虚拟机的性能，降低 IO 延迟，实现跨数据中心数据实时同步，还能提升存储引擎、计算和网络软件的性能，加速 ZBS 读写能力，改进时延、吞吐能力等性能指标，对敏感数据的加密保护等。

启用上述特性对部署 SMTX OS 的服务器 CPU 架构、软硬件配置等均提出了一系列要求，并且每种特性所运行的虚拟化环境和使用场景均有一定限制。本文档即为您详细描述这些要求和限制，同时提供这些特性的部署和配置操作。

阅读本文档需了解 SMTX OS 超融合软件，了解虚拟化、块存储等相关技术背景知识，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

- **2026-03-04：深度安全防护功能新增端口配置要求**
- **2026-02-04：配合 SMTX OS 6.3.0 正式发布**

  相较于 SMTX OS 6.2.0，本版本主要进行了如下更新：

  - 新增**双活特性**章节。
  - 新增**深度安全防护功能**章节。
  - 更新**配置网卡 SR-IOV 直通**小节。
  - 在 **vGPU 功能**章节中增加使用 NVIDIA L20 时需使用开放驱动的说明。
  - 在**RDMA 功能**章节，更新了 RDMA 功能的使用限制和影响；增加了在线开启和关闭 RDMA 的介绍。

---

## Boost 模式

# Boost 模式

您可以在未启用双活特性的 SMTX OS（ELF）集群或启用双活特性的 SMTX OS（ELF）集群中启用 Boost 模式，提升虚拟机性能、降低 IO 延时。

---

## Boost 模式 > 概述

# 概述

在超融合环境下，随着存储设备硬件性能的不断提升，对于存储引擎、计算和网络软件的性能要求也在攀升。在 SMTX OS 软件架构中，一个 IO 请求会经过计算虚拟化层、网络层和存储层。每经过一层系统，就会带来额外的性能开销。在普通模式下，ELF 采用 virtio 半虚拟化的方式来加速 IO 处理，整个 IO 过程可以在节点内部转发、无需经过网络传输。但由于 QEMU 的主线程中还运行着其他重要逻辑，virtio 处理 IO 请求时的资源有限，且 IO 路径需要通过 TCP 协议传输至存储服务 ZBS，以及 iSCSI 协议会对数据的封装会引起性能开销，这三点使系统产生了性能瓶颈。因此引入 Boost 模式对 IO 路径进行优化，从而提升虚拟机的性能，并充分发挥硬件性能。

---

## Boost 模式 > 概述 > 功能介绍

# 功能介绍

当集群启用 Boost 模式后，vhost 协议将 Guest OS、QEMU、ZBS 三者之间的内存共享，实现以下两方面的优化，从而提升虚拟机性能、降低 IO 延时。

- 在 IO 请求处理方面，ZBS 可以直接访问到 Guest OS 的内存获取 IO 请求并进行处理，不再需要 QEMU 的参与，绕开了由 QEMU 处理 IO 请求的线程资源有限所造成的瓶颈，大幅提升了处理 IO 请求的能力。
- 在数据传输方面，ZBS 可以直接与 Guest OS 共享数据，不再需要依靠 iSCSI 协议来传输数据，从而避免了使用 iSCSI over TCP 模式在本地网络协议栈传输带来的性能衰减和使用 iSCSI 协议对数据封装造成的性能开销，使得虚拟机读写的性能都得到优化。

![](https://cdn.smartx.com/internal-docs/assets/fb82c05e/boost_01.png)

---

## Boost 模式 > 概述 > 应用场景

# 应用场景

由于 Boost 模式能够明显提升虚拟机性能、降低 IO 延时，建议在对性能有较高要求的场景中（如运行数据库）启用 Boost 模式。

---

## Boost 模式 > 配置要求

# 配置要求

如需在 SMTX OS（ELF）集群中启用 Boost 模式，在安装部署 SMTX OS 前，请确保您的环境满足以下所有配置要求。

---

## Boost 模式 > 配置要求 > 虚拟化平台要求

# 虚拟化平台要求

SMTX OS 集群的虚拟化平台必须为 ELF。

---

## Boost 模式 > 配置要求 > 硬件要求

# 硬件要求

## CPU 架构

服务器的 CPU 架构必须为以下类型：

- Intel x86\_64 架构
- AMD x86\_64 架构
- Hygon x86\_64 架构
- 兆芯 x86 架构
- 鲲鹏 AArch64 架构
- 飞腾 AArch64 架构

## 缓存盘

为避免 SSD 成为性能瓶颈，推荐使用 NVMe SSD 作为缓存盘。

---

## Boost 模式 > 配置要求 > 系统资源占用

# 系统资源占用

本版本支持在 SMTX OS（ELF）集群中启用 Boost 模式，启用与否会对主机 CPU 和内存占用产生差异。详细说明见《SMTX OS 配置与管理规格》中的**系统资源占用** > **ELF 平台** > [**系统对主机 CPU 和内存的占用**](/smtxos/6.3.0/config_specs/config_specs_10)章节。

---

## Boost 模式 > 使用限制及影响

# 使用限制及影响

启用 Boost 模式有其使用限制，并且可能影响其他功能。

## 使用限制

- 不支持从 3.5.x 和 4.0.x 版本升级至本版本的 SMTX OS 集群开启此特性。
- 不支持在集群升级过程中变更 Boost 模式的启用状态，需要在集群升级前后保持统一，可在升级完成后通过命令行启用。
- 集群扩容时，系统将自动根据集群的 Boost 模式启用情况决定添加的节点是否开启此特性。

## 对其他功能的影响

启用 Boost 模式后：

- IO 请求不再经过 QEMU，而是使用基于 ZBS iSCSI LUN 实现的 IO 限速方式，虚拟磁盘限速将只支持针对虚拟盘的独立限速，不支持针对虚拟机的整体限速。
- 支持为主机配置多个物理池。
- 跨集群迁移仅支持对内存数据进行加密，磁盘数据不进行加密。
- 不支持深度安全防护功能。

---

## Boost 模式 > 启用 Boost 模式

# 启用 Boost 模式

启用集群的 Boost 模式只需在部署 SMTX OS（ELF）集群时，在**集群设置**阶段，选择 **SMTX 虚拟机服务**计算平台的同时，勾选**启用 Boost 模式**复选框，无需再进行其他设置。

---

## 双活特性

# 双活特性

启用双活特性的 SMTX OS 集群（简称为 “双活集群”）以拉伸形态部署在两个数据中心和第三方站点，实现跨数据中心数据实时同步。当一个数据中心发生故障时，SMTX OS 系统能自动将业务的数据访问切换至另一个数据中心，结合跨站点的虚拟机高可用机制，使得故障数据中心的业务虚拟机可以在短时间内自动在另一可用域的数据中心重建并恢复服务，从而保障系统的高可靠性和业务的连续性。

---

## 双活特性 > 概述

# 概述

传统基础架构的数据中心在遭遇物理服务器、网络或物理盘等硬件故障时，往往缺乏足够的冗余保障和快速恢复能力。一旦发生严重的数据中心站点级别的故障，极易导致业务中断，给客户造成重大经济损失。而传统容灾方案又面临建设成本高、架构复杂、容灾时间长等问题，难以满足关键业务对快速故障恢复的核心要求：即极短的故障切换时间（RPO 趋近于零）和业务的快速自动恢复。

针对上述挑战，SMTX OS 推出双活集群的解决方案。该方案将位于同一城市、具备一定物理距离的两个数据中心的物理节点构建为统一的拉伸集群，实现跨数据中心的数据实时同步，确保无数据丢失（RPO=0）。当发生数据中心站点级别的故障时，SMTX OS 能在分钟级内将故障数据中心内的业务虚拟机在健康的数据中心内自动恢复，显著提升系统的高可用性。

---

## 双活特性 > 概述 > 特性简介

# 特性简介

双活特性作为 SMTX OS 的一种数据保护和容灾机制，可应对生产环境中数据中心站点级别的故障，提供 RPO（数据恢复点目标）为 0，RTO（恢复时间目标）为分钟级的站点失效容错能力。

SMTX OS 双活集群由两个可用域和一个仲裁节点组成。两个可用域之间、可用域与仲裁节点之间均通过网络连接通信。

**优先/次级可用域**

双活集群的两个可用域通常部署在同一个园区内、具备独立供电系统的不同建筑内的数据中心，或者同一个城市有一定距离的物理节点所在的数据中心。两个可用域一般规划为优先可用域和次级可用域：前者所在的数据中心设定为主要业务运行站点，后者所在的数据中心设定为业务容灾站点。

在双活集群正常运行时，两个可用域内的主机上都同时运行着业务虚拟机。每个业务虚拟机的数据块将在集群的两个可用域内分别保存不同数量的副本，其中业务虚拟机当前接入点所在的可用域保存 2 个副本，另外一个可用域保存 1 个副本。在双活集群中，所有数据写入操作必须在两个可用域的物理盘上同步完成并确认成功后，系统才会返回写入成功的信息，因此两个可用域之间的数据始终保持实时同步。

对于双活集群共享的数据，例如虚拟机模板数据，其副本分配遵循在集群层级的优先可用域保存 2 个副本，次级可用域保存 1 个副本的原则，并且各可用域内虚拟机模板的数据副本均匀分布在所有节点上。

优先可用域与次级可用域的主机通过 L2 层网络直接连接。为保障数据同步和故障切换速度，降低网络延迟，优先可用域与次级可用域之间的存储网络通常应为光纤直连，存储网络带宽至少为 10 Gbps 及以上。

**仲裁节点**

在双活集群方案中引入仲裁节点，是为了在单一可用域异常，或者优先可用域和次级可用域之间网络中断时，提供独立的第三方判定机制，安全地判定使用哪个可用域继续对外提供服务，并帮助业务在优先和次级可用域之间实现自动化地切换。仲裁节点仅参与双活集群的选举和健康状态的判定，而且只保存少部分用于仲裁所需要的元数据，不存放任何用户数据。

双活集群的仲裁节点可以是物理机或虚拟机，需要部署在与优先可用域和次级可用域不同的物理故障区。一般情况下，仲裁节点与优先可用域、次级可用域均位于不同的数据中心。如果仲裁节点与可用域位于同一故障区，例如同一个 IDC 机房内，在遭遇该 IDC 整体下线的场景时，双活集群将无法自动恢复服务。

仲裁节点与优先/次级可用域的节点之间通过 L2 层或 L3 层存储网络进行连接。若仲裁节点与两个可用域间通过 L3 层存储网络连接，则还需要为其配置静态路由。

综上所述，双活集群具有以下特点：

- 数据实时同步，几乎零丢失

  集群的所有写入操作需在两个可用域的物理盘上同时落盘并确认成功后才返回写成功。优先可用域和次级可用域实时同步数据，确保两个可用域数据的一致性，任何单可用域的故障都不会导致已提交业务数据丢失。
- 故障自动切换，业务快速恢复

  故障检测、仲裁决策、虚拟机重建等均由系统自动完成。当优先可用域发生故障时，业务虚拟机自动在次级可用域恢复运行，保证业务连续性。
- 网络延迟低

  两个可用域位于同一个城市的不同的数据中心，可用域间物理距离有限，网络延迟较低，数据同步和故障切换速度较快。

---

## 双活特性 > 概述 > 双活实现原理

# 双活实现原理

![](https://cdn.smartx.com/internal-docs/assets/fb82c05e/active-active_01.png)

一个典型的同城双活集群的部署图如上图所示，优先可用域、次级可用域以及仲裁节点分别位于三个不同物理区域的数据中心 IDC A、IDC B 和 IDC C。双活集群已启用虚拟机 HA 特性并配置放置组策略，优先可用域（IDC A）与次级可用域（IDC B）中的主机上都同时运行着业务虚拟机。双活集群的数据存储策略统一设置为 3 副本模式。

下面阐述当双活集群正常运行时，写 I/O 和读 I/O 处理机制，以及当其中一个可用域出现故障时，集群的故障切换过程。

---

## 双活特性 > 概述 > 双活实现原理 > 写 I/O 机制

# 写 I/O 机制

![](https://cdn.smartx.com/internal-docs/assets/fb82c05e/active-active_02.png)

在双活集群正常运行时，当其中一个可用域节点上的虚拟机（VM1）发起数据写入请求：

1. SMTX OS 系统将该写 I/O 请求优先发往虚拟机所在节点（节点 N），并请求该节点的 ZBS（块存储系统）提供存储服务。
2. 当虚拟机所在节点（节点 N）、与虚拟机所在节点处于相同可用域且拓扑距离最远的节点（节点 A），以及与虚拟机所在节点不在同一可用域的其他节点（节点 M）均有充足的剩余空间且健康运行时，ZBS 将写 I/O 请求同时发往这 3 个节点。
3. 3 个节点收到写 I/O 请求后将数据写入节点，并向发起请求的 ZBS 返回写入成功或者失败的记录信息。
4. 在 3 个节点均返回结果后，ZBS 向虚拟机返回写入成功信息。此时 3 个节点上分别存放一份副本，因此两个可用域间的数据是实时同步的。

在虚拟机写入数据过程中，若 ZBS 希望存放副本的其他两个节点，即与虚拟机所在节点处于相同可用域的节点，或者与虚拟机所在节点不在同一可用域的其他节点，运行出现异常，导致这些节点无法保存副本，则 ZBS 的 I/O 处理逻辑如下：

1. 虚拟机（VM2）发起数据写入请求，SMTX OS 系统将该写 I/O 请求优先发往虚拟机所在节点（节点 B），并请求该节点的 ZBS 提供存储服务。
2. ZBS 将写 I/O 请求同时发往节点 B、与节点 B 处于相同可用域且拓扑距离最远的节点 M，以及与节点 B 不在同一可用域的节点 A。
3. 节点 B、节点 M 和节点 A 收到写 I/O 请求后立即将数据写入节点。节点 A 由于发生故障导致该节点上的数据写入失败，因而节点 A 的副本保存异常，但节点 B 和节点 M 仍可正常写入数据和保存副本。此时 ZBS 将节点 A 标记为数据写入失败，并将对应的数据副本剔除，节点 B 和 节点 M 标记为数据写入成功。
4. 由于节点 B 和 节点 M 写入数据成功，ZBS 将向虚拟机 VM2 返回写入成功，虚拟机可正常进行后续的 I/O 处理，不会被阻塞，虚拟机运行正常。
5. 由于异常节点 A 与虚拟机 VM2 所在的节点 B 位于不同的可用域，两个可用域的数据会进入临时不同步的状态。ZBS 将会立即触发数据恢复任务，尝试在异常节点 A 所在的可用域内寻找其他健康的节点，并在该节点上恢复一个完整的数据副本。当数据恢复完成后，两个可用域的数据进入完全同步状态。
6. 特殊情况下，如果异常节点 A 所在的可用域内已不存在健康的其他节点，或者该节点的整个可用域与虚拟机 VM2 所在的可用域出现整体失联，在故障未清除前，ZBS 将仅在虚拟机 VM2 所在的可用域内以 2 副本的方式写入数据并保存。在故障清除结束后，系统可自动触发数据恢复任务，将两个可用域重新恢复至数据同步的状态。

---

## 双活特性 > 概述 > 双活实现原理 > 读 I/O 机制

# 读 I/O 机制

![](https://cdn.smartx.com/internal-docs/assets/fb82c05e/active-active_03.png)

在双活集群正常运行时，当其中一个可用域的节点上的虚拟机（VM1）发起数据读取请求：

1. SMTX OS 系统将该读 I/O 请求优先发往虚拟机所在节点（节点 N），并请求该节点的 ZBS（块存储系统）提供存储服务。
2. ZBS 遵循尽量从距离虚拟机最近的存放副本的节点中读取数据，以减少网络延时，特别是跨可用域网络消耗带来的延时。参照上面的拓扑示意图，将按照如下优先级顺序（节点 N > 节点 A > 节点 M），逐一尝试从保存副本的各节点获取数据：

   1. 虚拟机所在节点（节点 N）
   2. 与虚拟机所在节点处于相同可用域的节点（节点 A）
   3. 与虚拟机所在节点不在同一可用域的其他节点（节点 M）
3. 只要从以上 3 个节点中的任意 1 个节点读取数据成功，ZBS 将立即向虚拟机返回读取的数据并记录读 I/O 请求成功。

一般情况下，ZBS 会在虚拟机所在的节点存放一份数据副本，因此虚拟机的读 I/O 请求只需要向虚拟机所在节点的 ZBS 读取数据即可完成。但当虚拟机发生热迁移，或者节点出现物理盘等故障时，虚拟机所在的节点上没有可访问的数据副本，此时只能从存放副本的其他节点完成数据的读请求。当虚拟机在新的节点运行一段时间后，或所在节点清除故障并恢复正常运行后，ZBS 会自动触发数据迁移或数据恢复，直至虚拟机所在节点上恢复保存一份数据副本的状态。

---

## 双活特性 > 概述 > 双活实现原理 > 故障自动切换流程

# 故障自动切换流程

一般情况下，在双活集群启用虚拟机 HA 功能，并正确配置机架拓扑和虚拟机放置组规则后，当其中一个可用域的单个节点或节点中的某个物理盘出现故障时，该故障节点或物理盘上保存的数据副本将立即触发数据恢复，最终恢复至节点所在的可用域保持 2 副本，另一可用域保持 1 副本的状态。如果是节点级别的故障，只要故障所在可用域的其他节点存在足够的计算资源（ CPU 和内存），故障节点上的虚拟机将遵循虚拟机放置组规则进行 HA 调度，自动 HA 至同一个可用域内的其他节点上运行，对业务影响较小。

但若双活集群运行时遭遇多个节点故障，或者仲裁节点故障，以及两个可用域与仲裁节点间的网络连接中断等比较复杂的场景，集群可能会自动完成故障切换，但也可能对业务产生影响，建议您查阅《SMTX OS 故障场景说明》的 [**双活集群故障**](/smtxos/6.3.0/failure_scenario_guide/failure_scenario_guide_35)章节，以了解在不同故障发生时，双活集群的容灾处理方式和对业务的影响。

---

## 双活特性 > 概述 > 应用场景

# 应用场景

SMTX OS 双活集群需要部署在同一个城市的两个数据中心，且要求数据中心之间具备高带宽、低延迟的稳定网络连接，建设成本较高。该方案一般应用在对业务连续性和数据实时性要求很高的行业，例如金融（银行或证券）、医疗、制造业等，利用 ​​SMTX OS 双活提供的数据强一致可靠性​​和高可用（HA）机制​​，在业务运行站点发生故障时，自动在健康站点重建虚拟机，并通过业务容灾站点进行数据访问，从而实现​​ RPO 为分钟级的业务恢复。

---

## 双活特性 > 配置要求

# 配置要求

[《STMX OS 双活集群安装部署指南（ELF 平台）》](/smtxos/6.3.0/elf_multiactive_installation/elf_multiactive_installation_05)和[《STMX OS 双活集群安装部署指南（VMware ESXi 平台）》](/smtxos/6.3.0/vmware_multiactive_installation/vmware_multiactive_installation_05)的**构建双活集群的要求**章节列举了在不同的虚拟化平台部署双活集群的详细规划和设计要求，建议根据即将采用的虚拟化平台：ELF 平台或 VMware ESXi 平台，在规划和部署双活集群前参考对应的内容完成相应的准备。

---

## 双活特性 > 配置要求 > 虚拟化平台要求

# 虚拟化平台要求

SMTX OS 支持采用 SmartX 原生虚拟化 ELF 或者搭配 VMware ESXi 虚拟化部署为双活集群。

---

## 双活特性 > 配置要求 > 集群规模要求

# 集群规模要求

SMTX OS 双活集群最少应包含 5 个节点，其中优先可用域 2 个节点，次级可用域 2 个节点，1 个仲裁节点。为了保证双活集群的高可用性和节点故障时的数据访问性能，推荐为优先可用域和次级可用域分别配置 3 个及以上节点，集群规模不少于 7 个节点。

---

## 双活特性 > 配置要求 > 网络配置要求

# 网络配置要求

SMTX OS 双活集群与不启用双活特性的 SMTX OS 集群的管理网络的配置要求完全相同。

由于双活集群里两个可用域的数据是实时同步的，在遭遇单个可用域故障时，系统能将数据访问自动切换至另一可用域。因此双活集群的优先可用域、次级可用域和仲裁节点之间的存储网络配置需要满足以下特殊要求。

## 存储网络带宽

优先可用域和次级可用域之间的存储网络一般应为光纤直连，存储网络带宽必须为 10 Gbps 及以上。

仲裁节点与优先/次级可用域的存储网络之间的带宽应不小于 100 Mbps。

## 存储网络连接

优先可用域与次级可用域的主机需连接到双活集群的 L2 层存储网络。

仲裁节点与优先/次级可用域的节点之间通过 L2 层或 L3 层存储网络进行连接，但两个节点通过存储网络连接时不支持 NAT 地址转换。若仲裁节点与两个可用域的节点通过 L3 层存储网络连接，还需要配置仲裁节点与可用域节点间的静态路由。

## 存储网络 ping 延时

优先可用域与次级可用域之间的存储网络 ping 延时在 5 ms 以下。

仲裁节点与优先可用域或次级可用域之间的存储网络 ping 延时在 100 ms 以下。

---

## 双活特性 > 配置要求 > 存储策略要求

# 存储策略要求

双活集群必须设置 3 副本的存储策略。

---

## 双活特性 > 硬件要求 > 系统资源占用

# 系统资源占用

SMTX OS 集群在启用双活特性时，还可同时启用 Boost 模式。集群单独启用双活特性与同时启用双活特性和 Boost 模式会对主机 CPU 和内存占用产生差异。详细说明见《SMTX OS 配置与管理规格》：

- **ELF 平台**：请参考**系统资源占用** > **ELF 平台** > [**系统对主机 CPU 和内存的占用**](/smtxos/6.3.0/config_specs/config_specs_10)章节。
- **VMware ESXi 平台**：请参考**系统资源占用** > **VMware ESXi 平台** > [**系统对主机 CPU 和内存的占用**](/smtxos/6.3.0/config_specs/config_specs_09)章节。

---

## 双活特性 > 硬件要求 > 优先/次级可用域节点配置要求

# 优先/次级可用域节点配置要求

双活集群的优先可用域和次级可用域节点与不启用双活特性的 SMTX OS 集群的节点的计算资源、存储设备和网络设备的配置要求基本相同。

---

## 双活特性 > 硬件要求 > 仲裁节点配置要求

# 仲裁节点配置要求

仲裁节点可以是物理机或虚拟机，但仲裁节点所在主机的 CPU 架构与可用域节点的 CPU 架构必须相同。请确认仲裁节点所在主机的最低配置符合下面的要求。

## ELF 平台

| **组件** | **配置要求** | **数量** |
| --- | --- | --- |
| CPU | 4 vCPU | 1 |
| CPU 微架构：  - Intel x86\_64：最低版本为 Sandy Bridge - AMD x86\_64：最低版本为 Zen - Hygon x86\_64：最低版本为 Dhyana - 兆芯 x86\_64：最低版本为永丰 - 鲲鹏 AArch64：最低版本为 Taishan v110 - 飞腾 AArch64：最低版本为 ARMv8 |
| 内存 | 8 GB 以上 | 1 |
| SSD 盘 | 308 GB 以上 | 1 |
| 网口 | 支持 100 MB/s 及以上带宽 | 至少 1 个 |
| 支持 10 MB/s 及以上带宽 | 至少 1 个 |

## VMware ESXi 平台

| **组件** | **配置要求** | **数量** |
| --- | --- | --- |
| CPU | 4 vCPU | 1 |
| CPU 微架构：  - Intel x86\_64：最低版本为 Sandy Bridge - AMD x86\_64：最低版本为 Zen |
| 内存 | 8 GB 以上 | 1 |
| SSD 盘 | 308 GB 以上 | 1 |
| 网口 | 支持 100 MB/s 及以上带宽 | 至少 1 个 |
| 支持 10 MB/s 及以上带宽 | 至少 1 个 |

---

## 双活特性 > 软件版本和许可要求

# 软件版本和许可要求

在不同的虚拟化平台上部署 SMTX OS 双活集群对软件有特定的版本要求。此外，双活功能需要单独购买许可。

- **ELF 平台**：SMTX OS 敏捷版、标准版或企业版软件
- **VMware ESXi 平台**：SMTX OS 标准版和企业版软件

---

## 双活特性 > 使用限制

# 使用限制

集群启用双活特性时有如下限制：

- 当 SMTX OS 搭配 VMware ESXi 平台部署时，只支持在新部署集群时启用双活特性。
- 在 SMTX OS 双活集群扩容时，新增节点需要满足启用双活特性的[配置要求](/smtxos/6.3.0/os_property_notes/os_property_notes_101)。
- 双活集群只支持配置 3 副本的冗余策略，不支持纠删码。
- 支持在双活集群中启用常驻缓存模式，但要求每个可用域中至少有 2 个节点为常驻缓存卷预留缓存容量。
- 不支持在双活集群中启用 RDMA 功能和 SR-IOV 特性。

---

## 双活特性 > 启用双活特性

# 启用双活特性

SMTX OS 双活集群为跨数据中心的拉伸集群，对于待部署的新集群，可根据即将采用的虚拟化平台：ELF 平台或 VMware ESXi 平台，参考[《SMTX OS 双活集群安装部署指南（ELF 平台）》](/smtxos/6.3.0/elf_multiactive_installation/elf_multiactive_installation_preface)或者[《SMTX OS 双活集群安装部署指南（VMware ESXi 平台）》](/smtxos/6.3.0/vmware_multiactive_installation/vmware_multiactive_installation_preface)，在集群的规划和部署阶段完成相应的准备和操作。集群在完成部署后即可实现双活。

若数据中心正在运行的 SMTX OS（ELF）集群未启用双活特性，同时未启用 RDMA 功能和 SR-IOV 特性，而且集群中不包含使用纠删码为冗余策略的 iSCSI Target 和虚拟卷，您可以联系 SmartX 工程师，通过添加节点，将该集群转化成为 SMTX OS（ELF）双活集群。

---

## RDMA 功能

# RDMA 功能

SMTX OS 通过将 RDMA 能力引入 ZBS 以优化远程节点写入延迟、改进吞吐能力，实现了集群性能的显著提升。

---

## RDMA 功能 > 概述

# 概述

本章主要介绍了 RDMA 功能简介、技术实现方案和特性优势。

---

## RDMA 功能 > 概述 > 特性简介

# 特性简介

在传统的计算机系统中，CPU 负责执行所有的计算任务和数据传输任务。当数据需要从外部设备（如硬盘、显卡、网卡等）传输到内存或者从内存传输到外部设备时，CPU 必须介入进行控制，这导致了 CPU 的处理能力成了系统性能瓶颈。在此背景下出现了 DMA（Direct Memory Access，直接内存访问）技术。DMA 可通过专门的控制器实现外部设备直接读取系统内存，而不需要 CPU 参与处理，可以有效减少 CPU 的负担，使 CPU 可以专注于处理其他任务，提高系统的处理效率。

RDMA（Remote Direct Memory Access）是 DMA 在网络通信领域的扩展和演进，其核心功能为允许计算机通过传输网络直接读取远端计算机的内存，整个过程无需两端的 CPU 介入。RDMA 技术可降低 CPU 负载，解决传统数据传输方式中的瓶颈问题，实现高性能、低延迟的数据传输。

![](https://cdn.smartx.com/internal-docs/assets/fb82c05e/rdma_01.png)

---

## RDMA 功能 > 概述 > 技术实现

# 技术实现

RDMA 的技术实现方案主要有三种：InfiniBand（IB）、RoCE 和 iWARP。

- **InfiniBand**（IB）

  InfiniBand 是最早实现的 RDMA 技术。InfiniBand 不依赖于以太网，包含编程接口、自身独有的网络协议栈（数据链路层、网络层、传输层）、网卡、网卡接口和交换机等一整套 RDMA 解决方案，拥有从硬件到软件的全栈全场景的技术集成。InfiniBand 可以为 RDMA 提供高性能的传输，但需要专门的硬件支持，部署成本较为高昂。
- **RoCE**（RDMA over Converged Ethernet）

  RoCE 支持在标准以太网基础设施上使用 RDMA 技术，实现 RDMA over Ethernet。RoCE 支持 RoCEv1 和 RoCEv2 两个版本。

  - **RoCEv1**

    RoCEv1 是通过以太网链路层实现的 RDMA 协议。通过使用 IB 网络层代替传统的 TCP/IP 网络层，从而在最大程度上保留 InfiniBand 的性能和特性，同时在以太网上实现对 RDMA 的支持。但同样因为使用了 IB 网络层替代了 TCP/IP 网络层， RoCEv1 仅支持在二层网络实现 RDMA，无法在三层网络实现 IP 路由功能。
  - **RoCEv2**

    RoCEv2 是对 RoCEv1 的改进。 RoCEv2 使用 UDP/IP 协议，通过以太链路层、UDP、IP 和传统的以太链路层协议栈进行数据传输，这使得 RoCEv2 可以跨越不同子网进行 RDMA 通信。RoCEv2 是目前最流行的实现 RDMA 的协议，得到了广泛的采用和支持。
- **iWARP**（Internet Wide Area RDMA Protocol）

  iWARP 是一种基于 TCP/IP 协议，可在标准以太网实现 RDMA 的技术。iWARP 支持在标准以太网基础设施上使用 RDMA，具有良好的互操作性和可扩展性，但必须要求网卡支持 iWARP，且由于其协议架构比较复杂，实现和部署相对更为困难，且性能相对更低。

在综合比较中，基于 RoCEv2 具备高灵活性、支持 IP 路由、无需使用专用硬件等优势，SMTX OS 选择 RoCEv2 技术作为 RDMA 的实现方案，使其适用于各类网络环境，同时在性能和成本之间取得了平衡。

---

## RDMA 功能 > 概述 > 特性优势

# 特性优势

- **零拷贝**（Zero Copy）

  RDMA 允许网卡直接读取或写入内存，数据可以直接在内存之间传递，避免了数据操作系统的缓冲区之间的拷贝，实现了不同节点之间的分布式块存储服务直接通讯，有效降低延时。
- **内核旁路**（Kernel Bypass）

  RDMA 避免了传统传输过程中应用内存和内核之间的数据复制，在不需要任何内核参与的条件下，数据能够从应用内存发送到本地网卡并通过网络发送给远程网卡。内核旁路功能使得 RDMA 在大规模集群和分布式系统中表现出色，系统可以更轻松地处理大量节点之间的数据传输需求。
- **CPU 卸载**（CPU Offload）

  RDMA 技术通过直接在网络适配器上执行数据传输和处理，在高带宽压力下对 CPU 占用极低，能够使 CPU 更专注于计算任务而非数据传输的管理，提高系统的吞吐量和效率。这种机制适用于高并发和大规模数据处理环境，可有效减轻系统瓶颈。

---

## RDMA 功能 > 配置要求

# 配置要求

如需启用 RDMA 功能，在安装部署 SMTX OS 集群时，该集群不仅要满足构建集群的基础要求，还需满足下述要求。

---

## RDMA 功能 > 配置要求 > 硬件要求

# 硬件要求

## CPU 架构

服务器的 CPU 架构须为以下类型：

- Intel x86\_64
- AMD x86\_64
- Hygon x86\_64
- 兆芯 x86
- 鲲鹏 AArch64

## 网卡

每个节点必须至少包含一张支持 RDMA 功能的存储网卡，目前已验证支持 Mellanox Technologies 厂商的网卡型号如下：

| **型号** | **固件版本要求** | **备注** |
| --- | --- | --- |
| MT27710 Family [ConnectX-4 Lx] 25Gb | - ELF 平台：14.24.80.00 及以上版本 - VMware ESXi 平台：不高于 14.26.4012 | 在配合 VMware ESXi 平台使用时，为避免在固件中开启 SR-IOV 后出现 RDMA 性能抖动的问题，需要确保 Mellanox 网卡的固件版本不高于 14.26.4012。  如果固件版本高于 14.26.4012，则需要在安装部署过程中进行固件降级，详细的操作步骤可参考《 SMTX OS 集群安装部署指南（VMware ESXi 平台）》的[固件降级](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_92)。 |
| MT27800 Family [ConnectX-5] 25Gb | - ELF 平台：16.25.1020 及以上版本 - VMware ESXi 平台：无要求 | - |
| MT27800 Family [ConnectX-5] 100Gb |
| MT2892 Family [ConnectX-6 Dx] 25 Gb | ELF 平台：22.37.1014 及以上版本 | 不支持配合 VMware ESXi 平台使用 |
| MT28841 Family [ConnectX-6 Dx] 25 Gb |
| MT28850 Family [ConnectX-6 Dx] 25 Gb |
| MT28851 Family [ConnectX-6 Dx] 25 Gb |
| MT2894 Family [ConnectX-6 Lx] 25 Gb | ELF 平台：26.37.1014 及以上版本 | 不支持配合 VMware ESXi 平台使用 |
| MT2910 Family [ConnectX-7] 25 Gb | - | 不支持配合 VMware ESXi 平台使用 |
| MT2910 Family [ConnectX-7] 100 Gb | - | 不支持配合 VMware ESXi 平台使用 |

## 交换机

交换机必须支持以下任意一种流量控制方式：

- L3 DSCP 流控
- Global Pause 流控

## 缓存盘

推荐使用 NVMe SSD 作为缓存盘。

---

## RDMA 功能 > 配置要求 > 软件版本要求

# 软件版本要求（VMware ESXi 平台）

## SMTX OS 版本

SMTX OS 软件版本为基础版、标准版、敏捷版或企业版。

## VMware ESXi 版本

- 版本为企业版
- 版本号为：
  - ESXi 7.0b
  - ESXi 7.0U1
  - ESXi 7.0U2
  - ESXi 7.0U3f
  - ESXi 8.0U1a
  - ESXi 8.0U2
  - ESXi 8.0U3

---

## RDMA 功能 > 配置要求 > 系统资源占用

# 系统资源占用

本版本软件支持启用 RDMA 功能，启用与否会对主机 CPU 和内存占用产生差异。详细说明见《SMTX OS 配置与管理规格》：

- **ELF 平台**：请参考**系统资源占用** > **ELF 平台** > [**系统对主机 CPU 和内存的占用**](/smtxos/6.3.0/config_specs/config_specs_10)章节。
- **VMware ESXi 平台**：请参考**系统资源占用** > **VMware ESXi 平台** > [**系统对主机 CPU 和内存的占用**](/smtxos/6.3.0/config_specs/config_specs_09)章节。

---

## RDMA 功能 > 使用限制和影响

# 使用限制和影响

## 使用限制

启用 RDMA 时，集群、存储网络以及存储网络所属的虚拟分布式交换机需满足如下要求。

- 集群配置需满足如下条件：

  - 集群未启用双活特性；
  - 为已启用 RDMA 的集群扩容时，新增节点必须同样开启 RDMA 功能，并满足所有配置要求；
  - 集群未处于升级过程中，包括升级中心执行的各类任务，如集群升级、内核升级、扩容系统分区等；
  - 集群不存在正在进入维护模式或处于维护模式的节点。
  - 所有节点均处于`健康`状态。
- 存储网络需满足如下条件：

  - 未启用 QoS 策略；
  - VLAN ID 必须设置为 `0`。
- 存储网络所属虚拟分布式交换机需满足如下条件：

  - 存储网络须使用独立的虚拟分布式交换机，不可与其他系统网络共用；
  - 每个节点上，虚拟分布式交换机所关联的物理网口均需支持 RDMA，且 RDMA 网卡需运行在 RoCE 模式；
  - 网口绑定模式必须为 OVS Bonding，且仅支持 `active-backup` 或 `balance-tcp` 模式；
  - 未关联 Everoute 分布式防火墙和网络安全导流。

## 对其他功能的影响

- **ELF 平台**

  在 RDMA 功能开启或关闭过程中：

  - 集群禁止添加新的节点。
  - 禁止对存储网络及其存储网络所属的虚拟分布式交换机进行编辑。
  - 创建系统网络（包括接入网络、迁移网络和镜像出口网络）时，禁止选择存储网络所属的虚拟分布式交换机。
  - 迁移系统网络（包括管理网络、接入网络和迁移网络）时，禁止选择存储网络所属的虚拟分布式交换机。

  启用 RDMA 功能后：

  - 物理交换机只能配置为 Access 模式，不支持 Trunk 模式。
- **VMware ESXi 平台**

  启用 RDMA 功能后：

  - 物理交换机只能配置为 Access 模式，不支持 Trunk 模式。
  - 连接存储网络的物理交换机不支持启用 LACP 动态链路聚合。
  - 如需对多个网口进行绑定，SCVM 将根据自己的策略自动选择某个物理网络适配器作为活动适配器，不支持手动指定，但不影响 ESXi 存储网络标准交换机的绑定和故障切换策略。

---

## RDMA 功能 > 配置 RDMA

# 配置 RDMA

如需启用 SMTX OS 集群的 RDMA 功能，则应在该集群中完成相应的配置，配置流程如下。

---

## RDMA 功能 > 配置 RDMA > ELF 平台

# ELF 平台

## 启用 RDMA

RDMA 功能支持在集群的部署阶段启用，也支持在集群部署后在线开启。

启用 RDMA 时，请确保集群满足 RDMA 的[配置要求](/smtxos/6.3.0/os_property_notes/os_property_notes_19)。

### 部署集群时启用 RDMA

1. 部署集群时，在[第 5 步：配置网络](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_37)阶段，选择**分离式部署**，并在配置存储网络所关联的虚拟分布式交换机时，勾选**启用 RDMA**。
2. 部署后，分别在交换机和主机中[为 RDMA 功能配置流量控制](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_47)。

### 在线启用 RDMA

1. 在 CloudTower 的集群管理页面选中要启用 RDMA 的集群，单击**全部** > **系统网络**，进入系统网络页面。
2. 单击存储网络名称，进入详情页面。
3. 单击**启用 RDMA**，确认当前集群已满足 RDMA 启用条件。
4. 单击**启用 RDMA** 按钮。
5. 启用 RDMA 后，请分别在交换机和主机中[为 RDMA 功能配置流量控制](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_47)。

## 在线关闭 RDMA

**操作步骤**

1. 在 CloudTower 的集群管理页面选中要启用 RDMA 的集群，单击**全部** > **系统网络**，进入系统网络页面。
2. 单击存储网络名称，进入详情页面。
3. 单击**关闭 RDMA**，确认当前集群已满足 RDMA 关闭条件。
4. 单击**关闭 RDMA** 按钮。

---

## RDMA 功能 > 配置 RDMA > VMware ESXi 平台

# VMware ESXi 平台

1. 部署前操作：

   1. 确认待部署集群满足 RDMA [配置要求](/smtxos/6.3.0/os_property_notes/os_property_notes_19)。
   2. 在网络规划阶段为[集群节点规划 IP](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_21) 时，为每个节点规划一个 VMware 接入网络 IP，用于节点的 SCVM 虚拟机与 ESXi 主机通信。
2. 部署时操作：

   1. 在设置 ESXi 阶段，先[为启用 RDMA 功能设置 ESXi 主机](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_31)，再[为 RDMA 功能配置流量控制](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_35)。
   2. 在配置存储网络阶段，[创建新的 vSphere 标准交换机](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_43)时，将 RDMA 网卡的指定网口分配给新创建的交换机。然后[为 RDMA 网络创建标准交换机](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_46)。
   3. 在 ESXi 节点上创建 SCVM 虚拟机阶段，[为 SCVM 虚拟机配置虚拟硬件](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_54)时配置 RDMA 相关内容。
   4. 在部署 SMTX OS 集群的[第 5 步：配置网络](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_64)阶段，启用 RDMA 功能。
3. 部署后，在设置 SMTX OS 的高可用性阶段，[部署 IO 重路由脚本和 SCVM 自动重启脚本](/smtxos/6.3.0/vmware_installation_guide/vmware_installation_guide_85)，配置 SCVM 节点的 VMware 接入网络。

---

## SR-IOV 特性

# SR-IOV 特性

SMTX OS 支持 SR-IOV (Single Root - I/O Virtualization) 直通功能。您可以在使用 ELF 平台的 SMTX OS 集群中启用网卡和加密控制器的 SR-IOV 特性。

---

## SR-IOV 特性 > 特性简介

# 特性简介

SR-IOV 是一种基于硬件的虚拟化解决方案，将一个硬件设备虚拟化为多个独立的虚拟设备的技术，从而提高性能，降低硬件成本。启用了 SR-IOV 的 PCIe 设备可以显示为多个单独的物理设备，以达到单个 I/O 资源被多个虚拟机共享的目的。

SR-IOV 包括如下两种功能类型：

- **物理功能 (Physical Function，PF)**

  PF 用于支持和管理 SR-IOV 功能，是全功能的 PCIe 功能，可像其他任何 PCIe 设备一样进行发现、管理和处理。

  PF 拥有完全配置资源，可用于配置或控制 PCIe 设备。一个 PF 可以切割出多个 VF。
- **虚拟功能 (Virtual Function，VF)**

  VF 是一种轻量级的 PCIe 功能，与 PF 以及与同一 PF 关联的其他 VF 共享一个或多个物理资源。

  VF 仅允许拥有用于其自身行为的配置资源。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 概述

# 概述

在传统的虚拟化环境中，虚拟机通过虚拟交换机进行网络通信。由于引入了额外的软件层，因而限制了虚拟机对网络资源的直接访问，特别是在处理大规模网络流量的场景下，软件层可能成为性能瓶颈。

PCI 直通（PCIe Passthrough）允许虚拟机直接访问物理机上的 PCIe（Peripheral Component Interconnect Express，快速外设组件互连）设备，绕过虚拟交换机等软件层，实现了对设备的直接控制。然而，PCI 直通通常仅适用于单一虚拟机的直通。

启用网卡的 SR-IOV 特性，并配置低延时网卡加速允许在多个虚拟机之间高效共享网卡，使得虚拟机能够获得更接近于物理主机的网络性能，从而大幅降低虚拟机的网络延时。

一个支持 SR-IOV 的物理网口可虚拟化出多个 SR-IOV 直通网卡（即 VF），每个 VF 可以作为一个 SR-IOV 直通网卡，被虚拟机直接挂载使用。

![](https://cdn.smartx.com/internal-docs/assets/fb82c05e/SR-IOV_01.png)

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 概述 > 特性优势

# 特性优势

![](https://cdn.smartx.com/internal-docs/assets/fb82c05e/SR-IOV_02.png)

与**传统虚拟网卡**相比，SR-IOV 直通网卡具有如下特性：

- 可绕过虚拟化层、缩短数据传输的路径，在网络延时上可获得与传统物理网卡接近的网络 I/O 性能。
- 可结合低延时网卡的加速方案使用，绕过内核协议栈、缩短网络包的传输路径，虚拟机的网络 I/O 延时可以超过物理机直连的性能。

与 **PCI 直通网卡**相比，SR-IOV 直通网卡具备更高的可伸缩性。

SMTX OS 支持 Solarflare 和 Mellanox 系列网卡的加速方案，具体说明如下：

- **Solarflare 系列网卡**：可使用 OpenOnload 加速方案。

  [OpenOnload](https://github.com/Xilinx-CNS/onload) 是一个高性能的运行于用户态的网络堆栈，它为使用 BSD 套接字 API 的应用程序加速 TCP 和 UDP 网络 I/O。

  建议访问 [OpenOnload 官方网站](https://www.xilinx.com/support/download/nic-software-and-drivers.html#open)下载最新发布的 OpenOnload Release Package，并参考《Onload User Guide》完成安装并使用。
- **Mellanox 系列网卡**：可使用 VMA 加速方案。

  Mellanox 的消息传递加速器（VMA）提高了基于消息和流媒体应用程序的性能，例如在金融服务市场数据环境和 Web2.0 集群中发现的应用程序。它允许通过标准套接字 API 编写的应用程序从用户态通过网络运行，并绕过内核协议栈直接操作网卡。

  建议访问 [NVIDIA 官网](https://docs.nvidia.com/networking/display/vmav970#src-99404722_safe-id-TlZJRElBTWVzc2FnaW5nQWNjZWxlcmF0b3IoVk1BKURvY3VtZW50YXRpb25SZXY5LjcuMC1Tb2Z0d2FyZURvd25sb2Fk)下载 VMA，同时参考 [VMA 文档](https://docs.nvidia.com/networking/display/vmav970/installing+vma)完成安装并使用。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 概述 > 应用场景

# 应用场景

SR-IOV 直通网卡适用于对网络性能要求较高、希望使用有限的物理网卡满足多台虚拟机共享使用需求的业务场景，例如低延时高吞吐业务、多租户环境、网络密集型应用等。

- **低延时高吞吐业务**

  在金融领域，例如期货投资交易，低延时和高吞吐量至关重要。通过使用 SR-IOV 直通网卡可以为虚拟机提供接近于物理机的网络性能，确保交易系统能够迅速响应市场变化，从而提高交易效率和可靠性。
- **多租户环境**

  在云计算或托管服务提供商的多租户环境中，不同租户可能共享同一组物理资源。通过使用 SR-IOV 直通网卡可以有效地划分和分配网络资源，确保不同租户之间的网络隔离的同时提供良好的网络性能。
- **网络密集型应用**

  对于处理大规模网络流量的应用，如视频流处理、实时数据分析等，通过使用 SR-IOV 直通网卡可以优化网络 I/O 性能、降低网络延时，确保流畅的数据传输和处理。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 配置要求

# 配置要求

如需在 SMTX OS 集群中启用网口的 SR-IOV 特性，则在安装部署 SMTX OS 前，请确保您的环境满足以下所有配置要求。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 配置要求 > 虚拟化平台要求

# 虚拟化平台要求

SMTX OS 集群的虚拟化平台须为 ELF。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 配置要求 > 硬件要求

# 硬件要求

## 网卡

网卡须支持 SR-IOV 特性，不同 CPU 架构下适配 SR-IOV 特性的网卡型号有所差异，具体如下所示。

- **Intel x86\_64 架构**

  | 品牌 | 系列 | 型号 |
  | --- | --- | --- |
  | Solarflare | X2 系列 | Solarflare XtremeScale X2522-25G Adapter |
  | 8000 系列 | Solarflare Flareon Ultra 8000 Series 10G Adapter |
  | Mellanox | CX-4 | Mellanox Technologies MT27710 Family [ConnectX-4 Lx] |
  | CX-5 | Mellanox Technologies MT27800 Family [ConnectX-5] |
  | CX-6 | Mellanox Technologies MT2892 Family [ConnectX-6 Dx] |
  | Intel | X710 | Intel Corporation Ethernet Controller X710 for 10GbE SFP+ (rev 02) |
  | 网迅 | RP1000 | Beijing Wangxun Technology Co., Ltd. Ethernet Controller RP1000 for 10GbE SFP+ (rev 03) |
- **Hygon x86\_64 架构**

  | 品牌 | 系列 | 型号 |
  | --- | --- | --- |
  | Mellanox | CX-4 | Mellanox Technologies MT27710 Family [ConnectX-4 Lx] |
  | CX-5 | Mellanox Technologies MT27800 Family [ConnectX-5] |
  | CX-6 | Mellanox Technologies MT2892 Family [ConnectX-6 Dx] |
  | Intel | X710 | Intel Corporation Ethernet Controller X710 for 10GbE SFP+ (rev 02) |
- **AMD x86\_64 架构**

  | 品牌 | 系列 | 型号 |
  | --- | --- | --- |
  | Mellanox | CX-5 | Mellanox Technologies MT27800 Family [ConnectX-5] |
- **鲲鹏 AArch64 架构**

  | 品牌 | 系列 | 型号 |
  | --- | --- | --- |
  | Mellanox | CX-5 | Mellanox Technologies MT27800 Family [ConnectX-5] |

> **说明**：
>
> Solarflare 系列网卡、Mellanox 系列网卡可结合低延时网卡加速方案进一步提升虚拟机的网络性能、降低网络延时，具体说明请参见[特性优势](/smtxos/6.3.0/os_property_notes/os_property_notes_34)。

## 主机

主机须满足如下要求：

- 支持并启用 IOMMU 和 SR-IOV。
- 已安装物理网卡（PF 网卡）驱动。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 配置要求 > 客户端操作系统要求

# 客户端操作系统要求

客户端操作系统及版本与节点所配置的网卡需满足兼容性要求，已验证的兼容列表如下所示。

- **Intel x86\_64 架构**

  | 网卡型号 | Guest OS 类型 | Guest OS 版本 |
  | --- | --- | --- |
  | Solarflare XtremeScale X2522-25G Adapter | Red Hat Enterprise Linux | - RHEL 6.10 - RHEL 7.6、7.7、7.8 - RHEL 8.1、8.2、8.3、8.4 |
  | Ubuntu Server | Ubuntu 18.04 |
  | Debian GNU/Linux | Debian 9 |
  | Solarflare Flareon Ultra 8000 Series 10G Adapter | Red Hat Enterprise Linux | - RHEL 6.10 - RHEL 7.6、7.7、7.8 - RHEL 8.1、8.2、8.3、8.4 |
  | Ubuntu Server | Ubuntu 18.04 |
  | Debian GNU/Linux | Debian 9 |
  | Mellanox Technologies MT27710 Family [ConnectX-4 Lx] | Red Hat Enterprise Linux | - RHEL 7.4、7.5、7.6、7.7、7.8 - RHEL 8.0、8.1、8.2、8.3、8.4、8.5 |
  | CentOS | - CentOS 7.4、7.5、7.6、7.7、7.8 - CentOS 8.0、8.1、8.2、8.3、8.4 |
  | Ubuntu Server | - Ubuntu 16.04 - Ubuntu 18.04 |
  | Windows Server | Windows Server 2016 DC |
  | Mellanox Technologies MT27800 Family [ConnectX-5] | Red Hat Enterprise Linux | - RHEL 7.4、7.5、7.6、7.7、7.8 - RHEL 8.0、8.1、8.2、8.3、8.4、8.5 |
  | CentOS | - CentOS 7.4、7.5、7.6、7.7、7.8 - CentOS 8.0、8.1、8.2、8.3、8.4 |
  | Ubuntu Server | - Ubuntu 16.04（需手动安装 VF 驱动，参见说明 ①） - Ubuntu 18.04 |
  | Windows Server | - Windows Server 2016 - Windows Server 2019 |
  | Mellanox Technologies MT2892 Family [ConnectX-6 Dx] | Red Hat Enterprise Linux | RHEL 8.5 |
  | CentOS | CentOS 8.5 |
  | SUSE | SLES 15 SP2 |
  | Ubuntu Server | Ubuntu 20.04 |
  | Windows Server | Windows Server 2022 |
  | OpenEuler | - OpenEuler 20.03（需手动安装 VF 驱动，参见说明②） - OpenEuler 22.03 |
  | Beijing Wangxun Technology Co., Ltd. Ethernet Controller RP1000 for 10GbE SFP+ (rev 03) | 银河麒麟 | 银河麒麟桌面操作系统 V10 |
- **Hygon x86\_64 架构**

  | 网卡型号 | Guest OS 类型 | Guest OS 版本 |
  | --- | --- | --- |
  | Mellanox Technologies MT27710 Family [ConnectX-4 Lx] | OpenEuler | - OpenEuler 20.03 - OpenEuler 22.03 |
  | Mellanox Technologies MT27800 Family [ConnectX-5] | OpenEuler | - OpenEuler 20.03 - OpenEuler 22.03 |
  | Mellanox Technologies MT2892 Family [ConnectX-6 Dx] | OpenEuler | - OpenEuler 20.03（需手动安装 VF 驱动，参见说明②） - OpenEuler 22.03 |
  | Intel Corporation Ethernet Controller X710 for 10GbE SFP+ (rev 02) | OpenEuler | - OpenEuler 20.03 - OpenEuler 22.03 |
- **AMD x86\_64 架构**

  | 网卡型号 | Guest OS 类型 | Guest OS 版本 |
  | --- | --- | --- |
  | Mellanox Technologies MT27800 Family [ConnectX-5] | Red Hat Enterprise Linux | - RHEL 7.4、7.5、7.6、7.7、7.8 - RHEL 8.0、8.1、8.2、8.3、8.4、8.5 |
  | CentOS | - CentOS 7.4、7.5、7.6、7.7、7.8 - CentOS 8.0、8.1、8.2、8.3、8.4 |
  | Ubuntu Server | - Ubuntu 16.04（需手动安装 VF 驱动，参见说明 ①） - Ubuntu 18.04 |
  | Windows Server | - Windows Server 2016 - Windows Server 2019 |
- **鲲鹏 AArch64 架构**

  | 网卡型号 | Guest OS 类型 | Guest OS 版本 |
  | --- | --- | --- |
  | Mellanox Technologies MT27800 Family [ConnectX-5] | OpenEuler | - OpenEuler 20.03 - OpenEuler 22.03 |

部分客户端操作系统需手动安装 VF 驱动，请参见如下说明。

- **说明 ①**

  对于使用 Mellanox Technologies MT27800 Family [ConnectX-5] 网卡的主机，当客户端操作系统为 `Ubuntu 16.04` 时，需要在客户端操作系统中手动安装 VF 驱动。请登录 [NVIDIA 官方网站](https://network.nvidia.com/products/ethernet-drivers/linux/mlnx_en/)，下载并安装适用于 Ubuntu 16.04 的网络适配器驱动程序。
- **说明 ②**

  对于使用 Mellanox Technologies MT2892 Family [ConnectX-6 Dx] 网卡的主机，当客户端操作系统为 `OpenEuler 20.03` 时，需要在客户端操作系统中手动安装 VF 驱动。请登录 [NVIDIA 官方网站](https://network.nvidia.com/products/infiniband-drivers/linux/mlnx_ofed/)，下载并安装适用于 OpenEuler 20.03 的网络适配器驱动程序。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 使用限制及影响

# 使用限制及影响

开启网口的 SR-IOV 特性有其使用限制，并且可能影响其他功能。

## 使用限制

- 允许集群中仅有部分主机支持 SR-IOV 特性，而其他主机不支持。
- 不支持在双活集群中启用网口的 SR-IOV 特性。

## 对其他功能的影响

使用 SR-IOV 直通网卡对其他功能的影响请参考《SMTX OS 管理指南》[挂载 SR-IOV 直通网卡或 PCI 直通网卡的影响](/smtxos/6.3.0/os_administration_guide/os_administration_guide_255)。

---

## SR-IOV 特性 > 网卡 SR-IOV 直通 > 配置网卡 SR-IOV 直通

# 配置网卡 SR-IOV 直通

使用网卡的 SR-IOV 特性时需在 SMTX OS 集群中完成相应的配置，具体配置流程如下图所示。

![](https://cdn.smartx.com/internal-docs/assets/fb82c05e/SR-IOV_03.png)

**注意事项**

每次只允许对一个主机的一个网口进行 SR-IOV 相关配置，包括切换网口用途至 **SR-IOV 直通**和编辑 SR-IOV 直通网卡个数，不可同时对两个网口进行操作。

**配置流程**

1. 部署 SMTX OS 集群前，在需要启用 SR-IOV 特性的所有主机的 BIOS 中开启 IOMMU 和 SR-IOV。

   - 对于新部署的 SMTX OS 集群，以及从 5.0.1 及以上版本升级至本版本的 SMTX OS 集群，请参考《SMTX OS 集群安装部署指南（ELF 平台）》的[检查 BIOS 设置](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_23)小节设置 BIOS。
   - 对于从 4.0.x 和 5.0.0 版本升级至本版本的 SMTX OS 集群，请先参考《SMTX OS 升级指南》的[手动升级内核](/smtxos/6.3.0/upgrade_guide/upgrade_guide_11) 小节手动升级内核，再[设置 BIOS](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_23)。
2. 登录 CloudTower，在需要启用 SR-IOV 特性的主机上启用 IOMMU。

   具体操作请参考《SMTX OS 管理指南》的[启⽤ IOMMU（ELF 平台）](/smtxos/6.3.0/os_administration_guide/os_administration_guide_136)小节，启用后主机 IOMMU 状态变更为`待重启`。

   > **说明**：
   >
   > 进入主机的网口列表，如果 **SR-IOV 状态**显示为`驱动未就绪`，则需单击**重配**，重新配置网口的 SR-IOV 驱动，相关配置将在主机重启后生效。
3. 重启主机。

   具体操作请参考《SMTX OS 运维指南》的[重启节点](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_99)小节。
4. 编辑需要启用 SR-IOV 特性的网口，将**网口用途**切换为 **SR-IOV 直通**，并设置直通网卡个数。

   具体操作请参考《SMTX OS 管理指南》的[切换网口用途](/smtxos/6.3.0/os_administration_guide/os_administration_guide_163)小节。

   配置完成后，如需修改 SR-IOV 直通网卡数量，可以参考《SMTX OS 管理指南》的[重新切分 SR-IOV 直通网卡数量](/smtxos/6.3.0/os_administration_guide/os_administration_guide_164)小节，重新设置直通网卡个数。
5. 返回主机的网口列表，确认上述步骤中所编辑的网口已增加如下信息，表明此网口已启用 SR-IOV。

   - **所属主机 IOMMU 状态**：`已生效`
   - **SR-IOV 状态**：`已启用`
   - **SR-IOV 直通网卡数量**：显示步骤 4 中设置的值
   - **SR-IOV 直通网卡已使用数量**：`0`
6. 参考上述步骤 2 ~ 5，为其他主机中支持 SR-IOV 特性的网口启用 SR-IOV。
7. 在包含启用 SR-IOV 特性的网口所在的主机上，为虚拟机挂载 SR-IOV 直通网卡。

   - 创建虚拟机并挂载 SR-IOV 直通网卡：请参考《SMTX OS 管理指南》的[创建虚拟机](/smtxos/6.3.0/os_administration_guide/os_administration_guide_012)小节。
   - 为已有虚拟机挂载 SR-IOV 直通网卡：请参考《SMTX OS 管理指南》的[编辑网络设备](/smtxos/6.3.0/os_administration_guide/os_administration_guide_043)小节。
8. 进入虚拟机列表，选中已挂载 SR-IOV 直通网卡的虚拟机，在右侧弹出的虚拟机详情面板中查看**网络设备**，SR-IOV 直通网卡的图标中将带有 **SR** 字样。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 概述

# 概述

数据加密是保障关键敏感信息机密性、完整性和有效性的重要手段之一，加密控制器（又称加密卡、密码卡等）是一种能够在虚拟化环境中提供加密保障的 PCIe 设备。

在传统虚拟化架构下，一个加密控制器只能服务一个虚拟机，造成资源的低效利用，增加了硬件使用成本也影响了业务扩展。

通过支持 SR-IOV，一个加密控制器可以虚拟化出多个虚拟加密控制器，即 VF，每个 VF 都可以分别被不同的虚拟机挂载使用，从而显著提升加密控制器的利用率，降低硬件成本，提高加密处理效率。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 概述 > 特性优势

# 特性优势

与传统的加密控制器应用方式相比，基于 SR-IOV 技术实现加密控制器的直通具有如下优势：

- 实现一个物理加密控制器服务多台虚拟机，减少对硬件设备的需求，降低硬件使用成本。
- 在多个虚拟环境中并发进行加密任务，且多个虚拟环境间操作互不影响，有效提高加密处理的效率与稳定性。
- 提供灵活的资源分配与管理能力，根据实际业务需求动态调整 VF 的数量和分配方式，能够迅速响应业务变化，实现更高的扩展性。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 概述 > 应用场景

# 应用场景

加密控制器 SR-IOV 直通适用于对数据安全要求较高、希望使用有限的物理加密控制器满足多台虚拟机共享加密功能的业务场景，例如含敏感数据业务、多租户环境等。

- **含敏感数据业务**

在金融、医疗等领域，存在例如个人身份信息、财务数据、医疗记录等大量敏感数据，将加密控制器通过 SR-IOV 直通给虚拟机使用，实现对敏感数据的加密保护，并帮助企业达成行业的数据合规要求。

- **多租户环境**

在云计算或托管服务提供商的多租户环境中，通过使用 SR-IOV 有效地划分和分配加密控制器，确保多租户共享同一组物理硬件，并允许各租户独立进行加密操作。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 配置要求

# 配置要求

如需在 SMTX OS 集群中使用 SR-IOV 加密控制器，则在安装部署 SMTX OS 前，请确保您的环境满足以下所有配置要求。

## 虚拟化平台要求

SMTX OS 集群的虚拟化平台须为 ELF。

## 硬件要求

### CPU 架构

服务器的 CPU 架构须为以下类型：

- Intel x86\_64
- Hygon x86\_64
- 鲲鹏 AArch64

### 加密控制器

加密控制器须为以下型号，如需使用其他型号，请联系 SmartX 确认是否可用。

- 渔翁 PCIe V7.1
- 三未信安 SJK1727(ZQ-H)

### 主机

主机须支持并启用 IOMMU 和 SR-IOV。

## 客户端操作系统要求

虚拟机操作系统中已安装驱动。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 对其他功能的影响

# 对其他功能的影响

使用 SR-IOV 加密控制器对其他功能的影响请参考《SMTX OS 管理指南》[挂载加密控制器的影响](/smtxos/6.3.0/os_administration_guide/os_administration_guide_279)。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 使用加密控制器 SR-IOV 直通

# 使用加密控制器 SR-IOV 直通

使用 SR-IOV 特性时需在 SMTX OS 集群中完成相应的配置，具体配置流程如下图所示。

![](https://cdn.smartx.com/internal-docs/assets/fb82c05e/SR-IOV_04.png)

**注意事项**

配置加密控制器 SR-IOV 直通时，需要将主机进入维护模式以及重启主机，建议每次只在一台主机上操作。

**准备工作**

- 部署 SMTX OS 集群前，在需要启用 SR-IOV 特性的所有主机的 BIOS 中开启 IOMMU 和 SR-IOV。

  - 对于新部署的 SMTX OS 集群，以及从 5.0.1 及以上版本升级至本版本的 SMTX OS 集群，请参考《SMTX OS 集群安装部署指南（ELF 平台）》的[检查 BIOS 设置](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_23)小节设置 BIOS。
  - 对于从 4.0.x 和 5.0.0 版本升级至本版本的 SMTX OS 集群，请先参考《SMTX OS 升级指南》的[手动升级内核](/smtxos/6.3.0/upgrade_guide/upgrade_guide_11) 小节手动升级内核，再[设置 BIOS](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_23)。
- 根据主机当前的内核版本和加密控制器品牌，获取对应的加密控制器驱动包。

  执行命令 `uname -a` ，可以查看该主机当前的内核版本。

**配置流程**

1. 登录 CloudTower，在需要启用 SR-IOV 特性的加密控制器所在主机上启用 IOMMU。

   具体操作请参考《SMTX OS 管理指南》的[启⽤ IOMMU（ELF 平台）](/smtxos/6.3.0/os_administration_guide/os_administration_guide_136)小节，启用后主机 IOMMU 状态变更为`待重启`。
2. 设置主机进入维护模式。

   具体操作请参考《SMTX OS 运维指南》的[进入维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)小节。
3. 在主机上配置加密控制器主机驱动。

   根据加密控制器的品牌参考对应的配置方式：

   - 渔翁

     1. 在主机上执行如下命令，安装加密控制器驱动包：

        ```
        rpm -ivh <fisec_rpm_name>
        ```
     2. 编辑配置文件 `/etc/modprobe.d/fisec.conf`，设置 SR-IOV 直通 VF 数量。
     3. 编辑配置文件 `/etc/modules-load.d/fisec.conf`，声明在系统启动时自动加载对应驱动。
   - 三未信安

     1. 在主机上执行如下命令，安装加密控制器驱动包：

        ```
        rpm -ivh <swcsm_rpm_name>
        ```
     2. 编辑配置文件 `/etc/modprobe.d/sw.conf`，设置 SR-IOV 直通 VF 数量。
     3. 编辑配置文件 `/etc/modules-load.d/swcsm.conf`，声明在系统启动时自动加载对应驱动。
4. 重启主机。

   具体操作请参考《SMTX OS 运维指南》的[重启节点](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_99)小节。
5. 返回主机的 PCI 设备列表，确认上述步骤中所编辑的加密控制器已增加如下信息，表明此加密控制器已启用 SR-IOV。

   - **所属主机 IOMMU 状态**：`已生效`
   - **设备用途**：`SR-IOV 直通`
   - **直通状态**：`已启用`
   - **设备切分数量**：显示步骤 3 中设置的值
   - **设备切分已使用数量**：`0`
6. 参考上述步骤 1 ~ 5，为其他主机中支持 SR-IOV 特性的加密控制器启用 SR-IOV。
7. 在 CloudTower 中将该主机退出维护模式。

   具体操作请参考《SMTX OS 运维指南》的[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)小节。
8. 为该主机上的虚拟机挂载 SR-IOV 直通加密控制器。

   - 创建虚拟机并挂载 SR-IOV 直通加密控制器：请参考《SMTX OS 管理指南》的[创建虚拟机](/smtxos/6.3.0/os_administration_guide/os_administration_guide_012)小节。
   - 为已有虚拟机挂载 SR-IOV 直通加密控制器：请参考《SMTX OS 管理指南》的[挂载或卸载加密控制器](/smtxos/6.3.0/os_administration_guide/os_administration_guide_280)小节。
9. 在挂载了加密控制器的虚拟机的操作系统上安装加密控制器的虚拟机驱动。
10. 进入虚拟机列表，选中已挂载 SR-IOV 直通加密控制器的虚拟机，在右侧弹出的虚拟机详情面板中查看**加密控制器**。

---

## SR-IOV 特性 > 加密控制器 SR-IOV 直通 > 重新切分加密控制器

# 重新切分加密控制器

本节描述的操作步骤仅适用于在 SMTX OS（ELF）集群中重新切分加密控制器的场景。

**准备工作**

将主机上所有挂载了该加密控制器的虚拟机关机，或确认当前没有虚拟机挂载该加密控制器。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间切分加密控制器，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间重新切分加密控制器，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，将待重新切分加密控制器的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 编辑加密控制器驱动配置文件，重新设置 SR-IOV 直通 VF 数量。

   不同品牌的加密控制器配置文件不同：

   - 渔翁：`/etc/modprobe.d/fisec.conf`
   - 三未信安：`/etc/modprobe.d/sw.conf`
3. 执行如下命令，更新加密控制器驱动中的 SR-IOV 直通 VF 数量：

   ```
   echo <new_vf_num> >/sys/bus/pci/devices/<bus_location_id>/sriov_numvfs
   ```

   其中 `<new_vf_num>` 是上一步骤中设置的 SR-IOV 直通 VF 数量；`<bus_location_id>` 是加密控制器的总线 ID ，可在 CloudTower 的 **PCI 设备**页面查看。
4. 执行如下命令，查看当前加密控制器的分配信息，在输出结果中确认该加密控制器的 `device_id`。

   ```
   zbs-node pci list_assign_info
   ```
5. 执行如下命令，更新加密控制器的配置信息。

   ```
   zbs-node pci update_target_device --device_id <device_id>
   ```

   其中 `<device_id>` 是上一步骤中查询的结果。
6. 在 CloudTower 中将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。

---

## 海光 HCT 特性

# 海光 HCT 特性

海光 HCT（Hygon Cryptographic Technology）是海光基于密码协处理器和密码指令集设计和研发的一套密码算法加速技术软件开发套件，能够提供软硬件结合的国密算法加密服务。SMTX OS 支持将 CCP（Crypto Coprocessor）设备通过 MDEV 形式透传给虚拟机使用，直接利用 CPU 资源高效执行国密算法，具备硬件成本低、系统架构简单、加密处理效率高等优势。

海光 HCT 适用于对敏感数据低成本保护、高吞吐量和低延时等业务场景。

- **敏感数据保护**

  海光 HCT 可为需要保护敏感信息的业务场景提供加密支持，如个人身份信息、支付数据、医疗记录等，无需其他硬件支持即可确保数据在存储和传输过程中得到加密保护，低成本实现防止数据泄露或篡改。
- **高吞吐量、低延迟业务**

  在需要处理大量数据并确保快速响应的业务场景中，HCT 基于硬件模块提升数据加解密处理速度，满足在例如实时通信、在线交易等包含大量数据的场景下提高响应速度的需求。

---

## 海光 HCT 特性 > 配置要求

# 配置要求

如需在 SMTX OS 集群中使用 HCT 特性，则在安装部署 SMTX OS 前，请确保您的环境满足以下所有配置要求。

## 虚拟化平台要求

SMTX OS 集群的虚拟化平台须为 ELF。

## 硬件要求

### CPU

服务器的 CPU 架构必须为 Hygon x86\_64，当前支持海光二代和海光三代。

### 主机

- 支持并已启用 IOMMU。
- 内核版本为 4.19 或 5.10。

## 客户端操作系统要求

虚拟机操作系统中已安装驱动。

---

## 海光 HCT 特性 > 对其他功能的影响

# 对其他功能的影响

使用 CCP 设备 MDEV 直通对其他功能的影响请参考《SMTX OS 管理指南》[挂载加密控制器的影响](/smtxos/6.3.0/os_administration_guide/os_administration_guide_279)。

---

## 海光 HCT 特性 > 使用 CCP 设备 MDEV 直通

# 使用 CCP 设备 MDEV 直通

使用海光 HCT 特性时需在 SMTX OS 集群中完成相应的配置，具体配置流程如下图所示。

![](https://cdn.smartx.com/internal-docs/assets/fb82c05e/hct_01.png)

**注意事项**

配置 CCP 设备 MDEV 直通时，需要将主机进入维护模式，建议每次只在一台主机上操作。

**配置流程**

1. 设置主机进入维护模式。

   具体操作请参考《SMTX OS 运维指南》的[进入维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)小节。
2. 登录 CloudTower，在需要使用 CCP 设备 MDEV 直通的虚拟机所在主机上启用 IOMMU。若主机 IOMMU 状态为`已启用`，请直接进行第 4 步。

   具体操作请参考《SMTX OS 管理指南》的[启⽤ IOMMU（ELF 平台）](/smtxos/6.3.0/os_administration_guide/os_administration_guide_136)小节。
3. 重启主机。

   具体操作请参考《SMTX OS 运维指南》的[重启节点](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_99)小节。
4. 在主机的 BIOS 中开启 IOMMU 并设置 HCT 相关配置。

   具体操作请参考《SMTX OS 集群安装部署指南（ELF 平台）》的[检查 BIOS 设置](/smtxos/6.3.0/elf_installation_guide/elf_installation_guide_23)小节设置 BIOS。
5. 为主机导入安全证书。若主机已存在安全证书请直接进行下一步。

   具体操作请参考[龙蜥社区文档](https://openanolis.cn/sig/Hygon-Arch/doc/865622274698254162)。
6. 证书导入成功后，执行如下命令清除主机因 hag 产生的大页内存：

   ```
   $ rm -f /dev/hugepages/tkm_page_0
   ```
7. 在主机上执行如下命令，切分 CCP 设备：

   ```
   $ zbs-node hct create_mdev_instances [--count <count>]
   ```

   其中 `[--count <count>]` 为可选参数，不配置该参数则默认会在每个 CCP 设备上创建出 32 个 mdev 实例，配置 `<count>` 参数则可以指定出其他数量的 mdev 实例，允许配置为 1～128。

   > **说明**：
   >
   > 对于 PSP 类型的 CCP 设备，由于主机驱动程序的技术要求，系统会保留 1 个完整的 PSP CCP 设备不进行切分，以确保主机核心功能的正常运行。剩余的 PSP CCP 设备将按照指定的数量进行切分。
8. 在主机上执行如下命令，同步数据：

   ```
   $ zbs-node hct update_devices
   $ zbs-deploy-manage config_cgroup;zbs-deploy-manage config_hugepage --need_restart
   $ systemctl restart job-center-worker
   ```
9. 返回主机的 PCI 设备列表，确认上述步骤中所编辑的 CCP 设备已增加如下信息，表明此 CCP 设备已启用 MDEV 直通。

   - **所属主机 IOMMU 状态**：`已生效`
   - **设备用途**：`MDEV 直通`
   - **直通状态**：`已启用`
   - **设备切分数量**：显示步骤 7 中设置的值
   - **设备切分已使用数量**：`0`
10. 参考上述步骤 1 ~ 9，为其他包含 CCP 设备的主机进行配置。
11. 在 CloudTower 中将该主机退出维护模式。

```
具体操作请参考《SMTX OS 运维指南》的[退出维护模式](../os_operation_maintenance/os_operation_maintenance_119.md)小节。
```

12. 为该主机上的虚拟机挂载 CCP 设备。

    - 创建虚拟机并挂载：请参考《SMTX OS 管理指南》的[创建虚拟机](/smtxos/6.3.0/os_administration_guide/os_administration_guide_012)小节。
    - 为已有虚拟机挂载：请参考《SMTX OS 管理指南》的[挂载或卸载加密控制器](/smtxos/6.3.0/os_administration_guide/os_administration_guide_280)小节。
13. 在挂载了 CCP 设备的虚拟机的操作系统上安装 HCT 驱动。

    具体操作请参考[龙蜥社区文档](https://openanolis.cn/sig/Hygon-Arch/doc/1110520213566721211)。
14. 进入虚拟机列表，选中已挂载 MDEV 直通 CCP 设备的虚拟机，在右侧弹出的虚拟机详情面板中查看**加密控制器**。

---

## 海光 HCT 特性 > 重新切分 CCP 设备

# 重新切分 CCP 设备

本节描述的操作步骤仅适用于在 SMTX OS（ELF）集群中重新切分海光 CCP 设备的场景。

**准备工作**

将主机上所有挂载了该 CCP 设备的虚拟机关机，或确认当前没有虚拟机挂载该 CCP 设备。

**操作建议**

由于执行快照将造成主机维护模式下的敏捷恢复机制失效，建议您在执行快照之外的其他时间切分 CCP 设备，以避免在主机维护模式期间执行快照操作。

若集群遇到特殊情况必须在快照执行期间重新切分 CCP 设备，请您知悉上述风险后进行操作。

**操作步骤**

1. 登录 CloudTower，将待重新切分 CCP 设备的节点[置为维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 在主机上执行如下命令，清理当前的 CCP 设备：

   ```
   $ zbs-node hct clean_all_mdevs
   ```
3. 在主机上执行如下命令，更新 CCP 设备的切分数量并同步数据：

   ```
   $ zbs-node hct create_mdev_instances [--count INTEGER] 
   $ zbs-node hct update_devices
   ```
4. 在 CloudTower 中将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。

---

## GPU 直通功能

# GPU 直通功能

GPU 直通是指将物理 GPU 完整地透传给虚拟机使用的功能。

通过 GPU 直通，一台虚拟机将独占一个或多个物理 GPU，拥有物理 GPU 所提供的极强的图像加速处理能力和浮点计算能力，在短时间内能够完成并行的图形处理和海量计算，从而⽀持机器学习模型、高性能计算等，如金融行业使用的反欺诈、交易算法。

---

## GPU 直通功能 > 配置要求

# 配置要求

如需在 SMTX OS 集群中使用 GPU 直通功能，SMTX OS 集群需满足以下配置要求。

## 虚拟化平台要求

SMTX OS 集群的虚拟化平台为 ELF。

## 硬件要求

- **CPU 架构**

  服务器的 CPU 架构为 Intel x86\_64、Hygon x86\_64 或鲲鹏 AArch64。如需在其他架构下使用 GPU 直通功能，请联系 SmartX 确认是否可用。
- **GPU 型号**

  请通过[SMTX OS 硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/?tab=0)，根据您使用的服务器机型确认当前可选择的 GPU 设备型号。

> **注意**：
>
> 当您使用 NVIDIA RTX 4090、RTX A6000 和 T1000 时，请先参考[前置操作](/smtxos/6.3.0/os_property_notes/os_property_notes_52)解绑该 GPU 的声卡驱动。

---

## GPU 直通功能 > 驱动要求

# 驱动要求

使用 GPU 直通时请您在即将挂载和使用 GPU 的虚拟机上安装 GPU 驱动。

---

## GPU 直通功能 > 特定 GPU 型号的前置操作

# 特定 GPU 型号的前置操作

NVIDIA RTX 4090、RTX A6000 和 T1000 的 GPU 设备将在操作系统上占用两个 PCI 地址，分别对应一个显卡设备和一个声卡设备，而声卡设备在主机开机时会自动绑定到声卡驱动上。当您使用这类 GPU 前，请务必参考本小节内容解绑该 GPU 的声卡驱动，否则挂载该直通 GPU 的虚拟机将无法开机。

请您登录 GPU 所属的主机执行以下步骤：

1. 执行如下命令获取声卡设备的 PCI 地址：

   ```
   ls /sys/bus/pci/devices/<PCI Address of Graphics Card>/iommu_group/devices/
   ```

   其中 `<PCI Address of Graphics Card>` 应根据实际情况替换为显卡设备的 PCI 地址即 CloudTower 展示的 GPU ID。

   输出结果中包含的另一个 PCI 地址即为声卡设备的 PCI 地址。
2. 执行如下命令获取声卡设备绑定的的声卡驱动的名称：

   ```
   ll /sys/bus/pci/devices/<PCI Address of Sound Card>/driver/module/drivers
   ```

   其中 `<PCI Address of Sound Card>` 应根据实际情况替换为步骤 1 中获取的声卡设备的 PCI 地址。

   **示例**

   ```
   ll /sys/bus/pci/devices/0000:86:00.1/driver/module/drivers
   total 0
   lrwxrwxrwx 1 root root 0 Sep 12 13:27 pci:snd_hda_intel -> ../../../bus/pci/drivers/snd_hda_intel
   ```

   表示 PCI 地址为 `0000:86:00.1` 的声卡设备绑定的声卡驱动的名称为 `snd_hda_intel`。
3. 执行如下命令将 GPU 设备从当前绑定的声卡驱动中解绑：

   ```
   echo "<PCI Address of Sound Card>" > /sys/bus/pci/devices/<PCI Address of Sound Card>/driver/unbind
   ```
4. 执行如下命令将声卡驱动加入黑名单，使其不会在主机开机时被自动加载：

   ```
   echo "blacklist <Sound Card Driver>" > /etc/modprobe.d/blacklist_snd_hda_intel.conf
   ```

   其中 `<Sound Card Driver>` 应根据实际情况替换为步骤 2 中获取的声卡驱动名称。

---

## GPU 直通功能 > 对其他功能的影响

# 对其他功能的影响

使用 GPU 直通对其他功能的影响请参考《SMTX OS 管理指南》[挂载 GPU 直通设备或 vGPU 的影响](/smtxos/6.3.0/os_administration_guide/os_administration_guide_260)。

---

## GPU 直通功能 > 使用 GPU 直通

# 使用 GPU 直通

在主机上安装 GPU 设备后，参照本节操作完成相关配置后即可在虚拟机上使用 GPU 设备。

![](https://cdn.smartx.com/internal-docs/assets/fb82c05e/gpu_passthrough_01.png)

**准备工作**

获取虚拟机 GPU 驱动。请您根据 GPU 型号、虚拟机操作系统和 GPU 设备厂商官⽅⽀持的驱动版本，从 GPU 设备厂商的官网获取。

**操作流程**

1. 如使用 NVIDIA GPU，请登录主机执行命令以禁用 nouveau 驱动。

   1. 执行以下命令，创建两个配置文件：

      ```
      cat <<_EOF_ > /etc/modprobe.d/gpu-passthrough-disable-nouveau.conf
      blacklist nouveau
      options nouveau modeset=0
      _EOF_
      ```

      ```
      cat <<_EOF_ > /usr/lib/modprobe.d/gpu-passthrough-disable-nouveau.conf
      blacklist nouveau
      options nouveau modeset=0
      _EOF_
      ```
   2. 执行以下命令卸载 nouveau 模块：

      ```
      modprobe -r nouveau
      ```
2. 登录 CloudTower 为 GPU 设备所在主机[开启 IOMMU](/smtxos/6.3.0/os_administration_guide/os_administration_guide_136) 并重启主机，详情请参考《SMTX OS 管理指南》。
3. 选择 GPU 设备⽤途为直通。

   如⾸次使⽤该 GPU 设备，设备⽤途默认为直通，请直接参照第 4 步进⾏操作；如此前已将 GPU 设备切分为 vGPU，则先将 [GPU 设备⽤途切换为直通](/smtxos/6.3.0/os_administration_guide/os_administration_guide_154#%E7%BC%96%E8%BE%91-gpu-%E8%AE%BE%E5%A4%87%E7%94%A8%E9%80%94)，详情请参考《SMTX OS 管理指南》。
4. [挂载 GPU 设备给虚拟机](/smtxos/6.3.0/os_administration_guide/os_administration_guide_156)，详情请参考《SMTX OS 管理指南》。
5. 为虚拟机安装 GPU 驱动，需参考 GPU 设备厂商提供的官方技术文档。
6. 重启虚拟机。

---

## vGPU 功能

# vGPU 功能

vGPU 是将物理 GPU 通过虚拟化技术切割得到的逻辑形态，一个物理 GPU 可以切割为多个 vGPU，vGPU 可以作为虚拟显卡分配给虚拟机。

通过 vGPU 功能，管理员可以根据需求灵活分配有限的 GPU 资源，使多台虚拟机共享一个物理 GPU 的图像加速处理能力和浮点计算能力，从而满足机器学习推理、三维设计与建模、游戏开发、图像渲染等相关应⽤开发与测试的共享需求，还可以为 VDI 提供可运⾏ 2D/3D 开发设计软件的环境。

---

## vGPU 功能 > 配置要求

# 配置要求

如需在 SMTX OS 集群中使用 vGPU 功能，SMTX OS 集群需满足以下配置要求。

## 虚拟化平台要求

集群的虚拟化平台为 ELF。

## 硬件要求

- **CPU 架构**

  服务器的 CPU 架构为 Intel x86\_64 架构。如需在其他架构下使用 vGPU 功能，请联系 SmartX 确认是否可用。
- **GPU 型号**

  请通过[SMTX OS 硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/?tab=0)，根据您使用的服务器机型确认当前可选择的 GPU 设备型号。

---

## vGPU 功能 > 驱动要求

# 驱动要求

使用 vGPU 需要同时配套 vGPU 软件。

---

## vGPU 功能 > 驱动要求 > 驱动介绍

# 驱动介绍

NVIDIA 官方发布的 vGPU 软件包含 NVIDIA Virtual GPU Manager 和 NVIDIA Graphics Driver。

- NVIDIA Virtual GPU Manager 是部署在虚拟化平台为虚拟机提供 vGPU 功能的驱动，包含专有驱动和开放驱动。SmartX 对 NVIDIA Virtual GPU Manager 进行了改造和适配，并随 SMTX OS 发布，后文将其称为 **vGPU 驱动**。
- NVIDIA Graphics Driver 是部署在使用 GPU 的虚拟机中使其可以使用 GPU 设备的驱动，后文将其称为 **GPU 驱动**。

在 SMTX OS 集群中的虚拟机使用 vGPU 时需提前获取这两个驱动。其中 **vGPU 驱动**需从 SmartX 获取，并参考[安装 vGPU 驱动](/smtxos/6.3.0/os_property_notes/os_property_notes_48)章节内容将其安装在 GPU 设备所在的主机上；**GPU 驱动**需从 NVIDIA 获取，并参考 [NVIDIA 官方文档](https://docs.nvidia.com/grid/latest/grid-vgpu-user-guide/index.html#installing-grid-vgpu-display-drivers)的指引将其安装在即将挂载和使用 vGPU 的虚拟机上。

---

## vGPU 功能 > 驱动要求 > 驱动版本选择

# 驱动版本选择

- **vGPU 驱动版本**

  参考 NVIDIA 官方提供的发布说明及 SMTX OS 版本配套的 vGPU 驱动版本，选择 NVIDIA Virtual GPU Manager 版本，也就是 **vGPU 驱动**版本。
- **GPU 驱动版本**

  根据所选择的 vGPU 驱动版本和 NVIDIA 官方提供的兼容性列表，选择与主机 vGPU 驱动版本适配的虚拟机 GPU 驱动版本。

---

## vGPU 功能 > 驱动要求 > 安装和升级 vGPU 驱动 > 安装 vGPU 驱动

# 安装 vGPU 驱动

使用 vGPU 前需参照本节内容在主机上安装 vGPU 驱动。

**准备工作**

- 执行命令 `uname -a` ，查看该主机当前的内核版本。
- 根据内核版本和所需的 vGPU 驱动版本，获取驱动安装包。

  > **说明**：
  >
  > 使用 NVIDIA L20 时请选择开放驱动。

**操作步骤**

1. 登录 CloudTower，设置主机[进入维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 上传驱动安装包到该主机的 `/home/smartx` 路径下。
3. 执行如下命令，完成安装。

   ```
   cd /home/smartx && rpm -ivh <rpm_name>
   ```
4. 通过命令 `rpm -qi Nvidia-vGPU`，查看已安装的驱动信息，确认安装成功。示例输出如下：

   ```
   $rpm -qi Nvidia-vGPU
   Name        : Nvidia-vGPU
   Version     : 14.2
   Release     : 4.18.0_193.28.1.el7.smartx.11
   Architecture: x86_64
   Install Date: Fri 03 Mar 2023 02:58:24 PM CST
   Group       : Unspecified
   Size        : 69359565
   License     : GPL
   Signature   : (none)
   Source RPM  : Nvidia-vGPU-14.2-4.18.0_193.28.1.el7.smartx.11.src.rpm
   Build Date  : Thu 09 Feb 2023 11:19:37 AM CST
   Build Host  : 5e21f91597c8
   Relocations : (not relocatable)
   URL         : http://www.smartx.com
   Summary     : Nvidia vGPU driver
   Description :
   Dynamically create, increase and shrink
   ```
5. 通过 CloudTower 或 IPMI 管理界面重启该主机。
6. 重启完成后，执行命令 `nvidia-smi`，输出 GPU 信息，则证明驱动功能正常。示例输出如下：

   ```
   $nvidia-smi
   Fri Apr 14 10:27:43 2023
   +-----------------------------------------------------------------------------+
   | NVIDIA-SMI 510.85.03    Driver Version: 510.85.03    CUDA Version: N/A      |
   |-------------------------------+----------------------+----------------------+
   | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
   | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
   |                               |                      |               MIG M. |
   |===============================+======================+======================|
   |   0  Tesla V100-PCIE...  On   | 00000000:2F:00.0 Off |                    0 |
   | N/A   32C    P0    25W / 250W |     50MiB / 16384MiB |      0%      Default |
   |                               |                      |                  N/A |
   +-------------------------------+----------------------+----------------------+

   +-----------------------------------------------------------------------------+
   | Processes:                                                                  |
   |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
   |        ID   ID                                                   Usage      |
   |=============================================================================|
   |  No running processes found                                                 |
   +-----------------------------------------------------------------------------+
   ```
7. 在 CloudTower 中将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。

---

## vGPU 功能 > 驱动要求 > 安装和升级 vGPU 驱动 > 升级 vGPU 驱动

# 升级 vGPU 驱动

当前用户所使用的 vGPU 版本无法支持用户所需特性或应用时，或集群升级了内核版本时，需要升级主机上的 vGPU 驱动。

**准备工作**

- 执行命令 `uname -a` ，查看该主机当前的内核版本。根据内核版本和所需的 vGPU 驱动版本，获取驱动安装包。

  > **说明**：
  >
  > 使用 NVIDIA L20 时请选择开放驱动。
- 待升级驱动所在主机上挂载了 vGPU 的虚拟机均处于关机状态。

**操作步骤**

1. 登录 CloudTower，设置主机[进入维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_118)。
2. 上传驱动安装包到该主机的 `/home/smartx` 路径下。
3. 执行如下命令，删除现有的驱动。

   ```
   rpm -e Nvidia-vGPU
   ```
4. 删除后执行命令 `rpm -qi Nvidia-vGPU`，确认驱动已删除成功，示例输出如下：

   ```
   $rpm -qi Nvidia-vGPU
   package Nvidia-vGPU is not installed
   ```
5. 执行如下命令，完成新驱动包安装。

   ```
   cd /home/smartx && rpm -ivh <new_rpm_name>
   ```
6. 通过命令 `rpm -qi Nvidia-vGPU`，查看已安装的驱动信息，确认安装成功。示例输出如下：

   ```
   $rpm -qi Nvidia-vGPU
   Name        : Nvidia-vGPU
   Version     : 14.2
   Release     : 4.18.0_193.28.1.el7.smartx.11
   Architecture: x86_64
   Install Date: Fri 03 Mar 2023 02:58:24 PM CST
   Group       : Unspecified
   Size        : 69359565
   License     : GPL
   Signature   : (none)
   Source RPM  : Nvidia-vGPU-14.2-4.18.0_193.28.1.el7.smartx.11.src.rpm
   Build Date  : Thu 09 Feb 2023 11:19:37 AM CST
   Build Host  : 5e21f91597c8
   Relocations : (not relocatable)
   URL         : http://www.smartx.com
   Summary     : Nvidia vGPU driver
   Description :
   Dynamically create, increase and shrink
   ```
7. 通过 CloudTower 或 IPMI 管理平台重启该主机。
8. 重启完成后，执行命令 `nvidia-smi`，输出 GPU 信息，则证明驱动功能正常。示例输出如下：

   ```
   $nvidia-smi
   Fri Apr 14 10:27:43 2023
   +-----------------------------------------------------------------------------+
   | NVIDIA-SMI 510.85.03    Driver Version: 510.85.03    CUDA Version: N/A      |
   |-------------------------------+----------------------+----------------------+
   | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
   | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
   |                               |                      |               MIG M. |
   |===============================+======================+======================|
   |   0  Tesla V100-PCIE...  On   | 00000000:2F:00.0 Off |                    0 |
   | N/A   32C    P0    25W / 250W |     50MiB / 16384MiB |      0%      Default |
   |                               |                      |                  N/A |
   +-------------------------------+----------------------+----------------------+

   +-----------------------------------------------------------------------------+
   | Processes:                                                                  |
   |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
   |        ID   ID                                                   Usage      |
   |=============================================================================|
   |  No running processes found                                                 |
   +-----------------------------------------------------------------------------+
   ```
9. 在 CloudTower 中将该节点[退出维护模式](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_119)。

---

## vGPU 功能 > 使用限制及影响

# 使用限制及影响

使用 vGPU 功能有其使用限制，并且可能影响其他功能。

## 使用限制

GPU 设备启用 MIG 模式时，无法使用 vGPU 功能。请参考 [NVIDIA 官方文档](https://docs.nvidia.com/grid/index.html) 《Virtual GPU Software User Guide》> **Installing and Configuring NVIDIA Virtual GPU Manager** > **Disabling MIG Mode for One or More GPUs** 关闭此模式。

## 对其他功能的影响

使用 vGPU 对其他功能的影响请参考《SMTX OS 管理指南》[挂载 GPU 直通设备或 vGPU 的影响](/smtxos/6.3.0/os_administration_guide/os_administration_guide_260)。

---

## vGPU 功能 > 使用 vGPU

# 使用 vGPU

在主机上安装 GPU 设备后，参照本节操作进行配置即可在虚拟机上使用 vGPU。

![](https://cdn.smartx.com/internal-docs/assets/fb82c05e/vgpu_01.png)

**注意事项**

使用 vGPU 需同时参考 NVIDIA 官方文档进行配置。请在 [NVIDIA 官网](https://docs.nvidia.com/grid/index.html)查看 vGPU 软件版本相对应的文档或章节。本章节内提及的所有 NVIDIA 官方文档的名称和查找路径均以 15.3 为例，其他版本可能略有不同。

**准备⼯作**

- 根据主机架构、主机内核版本和所选择的 vGPU 驱动版本，从 SmartX 获取主机 vGPU 驱动安装包。
- 根据所选择的主机 vGPU 驱动版本和兼容性列表，在 NVIDIA 获取与主机 vGPU 驱动版本适配的虚拟机 GPU 驱动。
- 购买 vGPU 授权或[申请试⽤版](https://enterpriseproductregistration.nvidia.com/?LicType=EVAL&ProductFamily=vGPU)。
- 准备另⼀个虚拟机，在其中部署并配置 NVIDIA vGPU software License Server。详情请参考 [NVIDIA 官方文档](https://docs.nvidia.com/grid/index.html)《Client Licensing User Guide》。

  > **说明：**
  >
  > 请您确保部署 License Server 的虚拟机与安装 GPU 驱动的虚拟机网络连通。

**操作流程**

1. 在 GPU 设备所在主机上[安装 vGPU 驱动](/smtxos/6.3.0/os_property_notes/os_property_notes_48)。
2. 在 CloudTower 完成如下操作：

   1. 为 GPU 设备所在主机[开启 IOMMU](/smtxos/6.3.0/os_administration_guide/os_administration_guide_136) 并重启主机，详情请参考《SMTX OS 管理指南》。
   2. 将 [GPU ⽤途切换为 vGPU](/smtxos/6.3.0/os_administration_guide/os_administration_guide_154#%E7%BC%96%E8%BE%91-gpu-%E8%AE%BE%E5%A4%87%E7%94%A8%E9%80%94)，并选择切分规格，详情请参考《SMTX OS 管理指南》。
   3. [挂载 vGPU 给虚拟机](/smtxos/6.3.0/os_administration_guide/os_administration_guide_156#%E5%9C%A8%E5%A1%AB%E5%86%99%E8%99%9A%E6%8B%9F%E6%9C%BA%E7%9A%84%E9%85%8D%E7%BD%AE%E5%8F%82%E6%95%B0%E6%97%B6%E6%8C%82%E8%BD%BD%E5%8D%B8%E8%BD%BD-gpu-%E8%AE%BE%E5%A4%87)，详情请参考《SMTX OS 管理指南》。
3. 在挂载 vGPU 的虚拟机上完成如下操作：

   1. 为虚拟机安装 GPU 驱动并重启虚拟机。具体请参考 [NVIDIA 官方文档](https://docs.nvidia.com/grid/index.html)《Virtual GPU Software User Guide》中 **Installing the NVIDIA vGPU Software Graphics Driver** 章节。
   2. 在虚拟机 GPU 驱动中关联 License Server，配置 License Server IP 及端⼝信息。具体请参考 [NVIDIA 官方文档](https://docs.nvidia.com/grid/index.html)《Client Licensing User Guide》。

---

## 常驻缓存模式

# 常驻缓存模式

数据常驻缓存（Volume pinning）是集群在分层部署（包括混闪分层部署和全闪分层部署）模式下可使用的一种存储优化策略，通过将虚拟卷或 NFS 文件保留在缓存层中，可保障关键业务持续保持高性能。

---

## 常驻缓存模式 > 概述

# 概述

本章主要介绍了常驻缓存模式的功能、优势和应用场景。

---

## 常驻缓存模式 > 概述 > 特性简介

# 特性简介

分层部署的集群在默认情况下，存储卷中具有较高访问频率的数据将停留在速度更快的缓存层，访问频率较低的数据将下沉至速度相对较慢的数据层。在实际场景中，部分应用需要将所有数据始终保留在缓存层中以提供高性能服务。在此场景下，可以为这些应用的虚拟卷或 NFS 文件启用常驻缓存模式，将数据始终保留在缓存层，从而获得更稳定的高性能。

---

## 常驻缓存模式 > 概述 > 特性优势

# 特性优势

常驻缓存模式具有如下优点：

- **为关键应用提供稳定的高性能**

  通过将特定存储卷始终保持在缓存层，可以使关键应用在任何时刻都能够以低延迟访问数据，且可避免数据下沉至底层存储系统而导致大量请求穿透缓存直接访问底层存储的情况，确保应用可持续保持高性能。
- **提升成本效益**

  无需采用成本更高的不分层部署模式或使用全闪的分层部署模式，通过仅将特定虚拟卷保留在缓存层，可在满足部分关键应用持续高性能的同时控制整体的存储成本。

---

## 常驻缓存模式 > 概述 > 应用场景

# 应用场景

常驻缓存模式主要应用场景如下：

- **关键应用持续保持高性能**

  一些关键应用，例如金融交易数据库、在线支付系统，对实时性能和数据访问的延迟具有高度敏感性，任何性能波动都可能对业务产生重大影响。在这种场景下，启用常驻缓存模式可确保关键应用数据始终在高性能缓存中，为数据提供稳定的低延迟访问，并可防止大量请求穿透缓存直接访问底层存储系统，保障关键业务的稳定性和可靠性。
- **低频率、高延迟敏感数据访问**

  某些应用中，数据在长时间内访问频率较低，但一旦被访问，对存取速度有较高要求。在分层部署的集群中，默认按照数据的冷热程度自动分层，访问频率较低的数据会下沉到性能较低的存储中，导致再次访问时速度较慢。常驻缓存模式通过将特定存储卷保留在高性能缓存，一旦需要访问，仍可从缓存中快速获取，满足对访问速度的要求。

---

## 常驻缓存模式 > 配置要求

# 配置要求

如需启用集群的常驻缓存模式，安装部署时，该集群不仅要满足构建集群的基础要求，还需满足下述要求。

## 软件版本要求

SMTX OS 软件版本为基础版、敏捷版、标准版或企业版。

## 硬件要求

### 存储设备要求

安装部署 SMTX OS 集群时，该集群必须采用存储分层模式（混闪配置或多种类型 SSD 全闪配置），主机上的存储设备（即物理盘）必须满足《SMTX OS 安装部署指南》中分层模式下的[存储设备配置要求](/smtxos/6.3.0/config_specs/elf_installation_guide/elf_installation_guide_59#%E5%AD%98%E5%82%A8%E8%AE%BE%E5%A4%87%E9%85%8D%E7%BD%AE%E8%A6%81%E6%B1%82)。

### 缓存盘容量要求

配置常驻缓存时，为避免其占满缓存空间、影响其他卷性能，需要合理规划缓存盘容量。规划原则是：扣除常驻缓存容量后，缓存盘的剩余容量与数据盘总容量之比仍应大于 10%。

- 若集群尚未部署，应在规划阶段评估常驻缓存需求，并预留足够的缓存盘容量以支撑未来负载。
- 若集群已部署，但现有缓存盘不足以满足新增常驻缓存需求，则需按所需容量进行扩容，避免因缓存不足而无法启用常驻缓存。

**参数说明**：

| 参数 | 说明 |
| --- | --- |
| 缓存盘容量 | 对于标准容量规格节点，缓存盘容量上限为 25 TB；对于大容量规格节点，缓存盘容量上限为 50 TB。若计算得出数值小于上限值，容量可配置为计算值，否则只能配置为上限值。 |
| 热数据比例 | 数据盘中访问频率较高的数据所占的比例，一般为 10% ~ 20%。 |
| X% | 预留常驻缓存比例，为常驻缓存容量占写缓存容量的比例，且取值需为整。写缓存容量为总缓存容量的 80%。 |

#### 已知常驻缓存所需容量

若已知常驻缓存所需的具体容量，可以根据该需求来规划集群需要配置的缓存盘容量。在规划时，需要综合考虑常驻缓存卷的逻辑容量和卷的冗余策略，从而计算所需的总缓存容量。具体说明如下：

1. 确定常驻缓存卷所需的容量。通常建议预留的常驻缓存容量比所需容量大 10% ~ 20%。
2. 考虑冗余策略对常驻缓存容量的影响。

   假设集群常驻缓存卷的逻辑容量为 a，考虑冗余策略后，`需预留常驻缓存容量 = a * 副本数`。

   副本数的确定规则如下：

   - 若卷采用了副本策略，副本数为副本策略设置的副本数
   - 若卷采用了纠删码策略，副本数根据纠删码的配置确定：

     - 当 m = 1 时，副本数为 2；
     - 当 m = 2、3、4 时，副本数为 3。
3. 计算集群所需的总缓存容量。

   `集群所需总缓存容量 = 预留常驻缓存容量 / X% / 80%`
4. 确定每个节点需配置的缓存盘容量。

   `每个节点需配置的缓存盘容量 = 集群所需总缓存容量 / 节点数量 + 系统占用的缓存容量`

   > **说明**：
   >
   > 系统占用的缓存容量请参考[《SMTX OS 配置和管理规格》](/smtxos/6.3.0/config_specs/config_specs_01)。

**示例**：

假设一个集群由 3 个标准容量规格节点组成，每节点配置 2 块含元数据分区的缓存盘。需启用常驻缓存的卷逻辑容量为 1 TiB，采用 2 副本机制，则计算如下：

```
启用常驻缓存所需的缓存容量为 1 TiB * 2 = 2 TiB。

对应集群的总缓存容量至少为 2 TiB / 50% / 80% = 5 TiB。

每节点缓存盘至少需配置 5 TiB / 3 + 305 GiB * 2 = 2.26 TiB。
```

#### 未知常驻缓存所需容量

在常驻缓存卷容容量未知时，可以根据节点数据盘容量、热数据比例和预留常驻缓存比例来估算缓存盘所需容量。

因此，综合考虑热数据和常驻缓存卷的需求，规划缓存盘容量时，请采用如下公式计算：

`缓存盘容量 =（数据盘容量 * 热数据比例）/（1 - 0.8 * X%）`

**示例**

在一个数据中心中采用标准容量规格节点部署 SMTX OS 集群，单个节点的数据盘容量为 10 TB。根据业务分析，该集群中的热数据约占总数据量的 15%。此外为确保关键数据一直保持高性能，希望为常驻缓存卷预留 20% 的缓存空间。

根据如上需求，单节点所需缓存盘容量计算如下：

```
缓存盘容量 =（数据盘容量 * 热数据比例）/（1 - 0.8 * X%）
         =（10 TB * 15%）/（1 - 0.8* 20%）
         ≈ 1.786 TB
```

计算出的缓存盘容量未超过缓存盘的容量上限，建议将缓存盘容量设置为约 2 TB。

#### 计算常驻缓存卷最大可配置容量

单个常驻缓存卷最大可配置容量取决于集群预留的总常驻缓存容量和冗余策略设置。

`单个常驻缓存卷最大可配置容量 = 集群预留常驻缓存总量 / 副本数 = 集群总缓存容量 * 0.8 * X% / 副本数`

其中，副本数的确定规则如下：

- 若卷采用了副本策略，副本数为副本策略设置的副本数
- 若卷采用了纠删码策略，副本数根据纠删码的配置确定：

  - 当 m = 1 时，副本数为 2；
  - 当 m = 2、3、4 时，副本数为 3。

---

## 常驻缓存模式 > 使用限制

# 使用限制

使用常驻缓存模式具有如下使用限制：

- **部署要求**：仅支持分层部署集群，且集群内所有物理盘不能为单一类型单一属性 SSD 全闪配置。
- **主机配置要求**：

  - 非双活集群：至少需为集群内 3 个主机的物理盘池设置预留缓存比例；
  - 双活集群：至少需为每个可用域内 2 个主机的物理盘池设置预留缓存比例。
- **为常驻缓存卷预留的缓存比例**：

  - 默认预留缓存比例可设置为 1% ~ 75%；
  - 若针对单个物理盘池设置：
    - 含数据分区的物理盘池：可设置为 0% ～ 75%；
    - 不含数据分区的物理盘池：可设置为 0% ～ 100%。

---

## 常驻缓存模式 > 配置常驻缓存

# 配置常驻缓存

如需启用 SMTX OS 集群的常驻缓存模式，应在该集群中完成相应的配置，配置流程如下：

1. 部署前，确认待部署集群的主机满足启用常驻缓存的[配置要求](/smtxos/6.3.0/os_property_notes/os_property_notes_72)。
2. 部署时，在配置存储阶段选择存储分层模式。详情请根据使用的虚拟化平台，参考《SMTX OS 集群安装部署指南（ELF 平台）》或《SMTX OS 集群安装部署指南（VMware ESXi 平台）》。
3. 部署后，启用常驻缓存模式：
   1. 在集群的**设置**界面中开启[允许数据常驻缓存](/smtxos/6.3.0/os_administration_guide/os_administration_guide_219)，并为常驻缓存卷预留缓存容量，详情请参考《SMTX OS 管理指南》。
   2. 为虚拟卷或 NFS 文件开启常驻缓存模式。
      - 为虚拟卷开启常驻缓存模式：参考《SMTX OS 管理指南》，通过编辑虚拟卷的方式为虚拟卷开启常驻缓存。
      - 为 NFS 文件开启常驻缓存模式：参考《SMTX OS 管理指南》的[编辑 NFS 文件的常驻缓存模式](/smtxos/6.3.0/os_administration_guide/os_administration_guide_126) ，通过编辑 NFS 文件的常驻缓存模式开启。

---

## 深度安全防护功能

# 深度安全防护功能

随着虚拟化和云技术的发展，业务系统规模和网络复杂度不断增加，病毒、恶意软件及网络攻击的威胁也日益复杂。传统依赖单机或代理式防护的方式，在大规模虚拟化环境中已难以满足实时防护和统一管理的需求。

为保障业务连续性、数据安全及网络环境稳定，SMTX OS 提供了深度安全防护功能，针对病毒查杀、恶意流量识别、异常行为监测等多类安全风险进行实时检测与拦截，为虚拟机提供高效、统一的安全防护能力。

---

## 深度安全防护功能 > 概述

# 概述

深度安全防护功能集成亚信的信舱云主机安全 DeepSecurity，通过在集群中统一部署**安全防护虚拟机（SVM，Security Virtual Machine）**，以无代理的方式提供了虚拟机粒度的病毒查杀、以及虚拟网卡粒度的深度包检测能力，能够有效阻止病毒入侵并对网络流量进行深度分析，保障整体网络环境的安全性。

配置深度安全防护功能后，可为业务虚拟机提供如下功能：

- **防病毒**：支持防恶意软件，对病毒、间谍软件、木马等威胁进行查杀，并提供资产管理和入侵检测功能。
- **深度包检测**：配合 Everoute 中的**网络安全导流**功能，可支持 Web 信誉、防火墙和入侵防御功能，检测虚拟机出入站流量并保护操作系统和应用程序免受攻击。

---

## 深度安全防护功能 > 配置要求

# 配置要求

如需使用深度安全防护功能，请确保您的环境满足以下所有配置要求。

## 集群要求

- 集群的虚拟化平台为 ELF。
- 集群服务器的 CPU 架构为 x86\_64。
- 集群未启用 Boost 模式。
- 集群中的每台主机需额外预留 800 MB 内存。

## 端口要求

为了确保深度安全防护功能的正常使用，当源端访问目标端时，目标端需要开放如下端口。下表如无特殊说明，端口的传输端协议均为 TCP。

| 源端 | 目标端 | 目标端需开放的端口 | 端口说明 |
| --- | --- | --- | --- |
| 深度安全防护系统管理平台（DSM） | 安全防护虚拟机（SVM） | 4118 | DSM 与 SVM 之间通信的端口 |
| 22 | 快速部署 |
| SVM | DSM | 4119 | SVM 与 DSM GUI 或 API 建立会话连接的通信端口 |
| 4120 | DSM 波动信号端口 |
| DSM | CloudTower | 443 | DSM 从 CloudTower 获取虚拟机信息的通信端口 |

## 客户端操作系统要求

- 满足亚信 DeepSecurity 软件对客户端操作系统的兼容要求，具体说明请参考亚信的官方文档。
- 满足 SMTX 虚拟机工具（即 SMTX VMTools）对客户端操作系统的兼容要求，具体说明请参考相应版本《SMTX 虚拟机工具发布说明》的**版本配套说明**小节。

---

## 深度安全防护功能 > 使用限制及影响

# 使用限制及影响

使用深度防护功能存在一定的使用限制，并且可能影响其他功能。

## 使用限制

- 系统服务虚拟机不支持使用深度安全防护功能。
- 当集群从之前的版本升级至本版本后，对于升级前已存在的业务虚拟机，如需使用防病毒功能，需先执行关机再重新开机。
- 关闭防病毒功能将会自动删除隔离区文件。如需保留隔离区文件，建议在功能关闭前先解除隔离。

## 对其他功能的影响

如果业务虚拟机使用了深度安全防护功能，将会有以下影响。

**对配置虚拟机参数的影响**

- 开启深度包检测功能的虚拟网卡，不支持启用虚拟网卡镜像模式。
- 开启深度包检测功能的虚拟网卡在修改虚拟机网络时，禁止选择所属虚拟分布式交换机未关联至 Everoute 网络安全导流功能的虚拟机网络。
- 开启防病毒或深度包检测功能的虚拟机，在启用虚拟机高可用后，若重建的主机不满足功能启用要求，则防病毒功能将会自动关闭、深度包检测功能将无法使用。

**对虚拟机电源操作的影响**

- 开启防病毒功能的虚拟机支持自动调度至满足功能启用要求的主机，或指定所属主机。若目标主机不满足功能启用要求，则虚拟机将无法开机。您可以关闭防病毒功能后再重新开机，或更换目标主机。
- 开启深度包检测功能的虚拟机不支持自动调度至满足功能启用要求的主机。若目标主机不满足功能启用要求，则虚拟机开机后将无法使用该功能。

**对虚拟机模板、虚拟机快照和克隆虚拟机的影响**

- 将虚拟机克隆或转化为虚拟机模板后，生成的模板中不包含防病毒和深度包检测功能的配置。
- 为虚拟机创建快照时，快照中不包含防病毒和深度包检测功能的配置。
- 将虚拟机回滚至快照状态后，不影响回滚前虚拟机已有的防病毒和深度包检测功能的配置。
- 克隆虚拟机默认关闭防病毒和深度包检测功能，您可以在克隆完成后手动开启。

**对导出虚拟机的影响**

导出的虚拟机中不包含防病毒和深度包检测功能的配置。

**对迁移虚拟机的影响**

- 开启防病毒功能的虚拟机，在进行集群内迁移后，虚拟机仍包含该功能的配置。

  - 冷迁移：若目标主机不满足功能启用要求，则迁移后虚拟机无法开机。
  - 热迁移：若目标主机不满足功能启用要求，则无法迁移。
- 开启深度包检测功能的虚拟机，在进行集群内迁移后，虚拟机仍包含该功能的配置。若目标主机不满足功能启用要求，则迁移后该功能将无法使用。
- 开启防病毒或深度包检测功能的虚拟机，在进行跨集群迁移前，将自动关闭相应功能。

**对快照、复制、备份计划的影响**

- 创建快照计划时，快照中不包含防病毒和深度包检测功能的配置。
- 创建复制或备份计划时，复制或备份的目标虚拟机中不包含防病毒和深度包检测功能的配置。

---

## 深度安全防护功能 > 使用深度安全防护

# 使用深度安全防护

使用深度安全防护功能时，需在 SMTX OS 集群中完成相应的配置，具体配置流程如下图所示。

![](https://cdn.smartx.com/internal-docs/assets/fb82c05e/security_01.png)

**前提条件**

- 请提前获取 SVM 模板（OVF 文件包），包含 `.ovf` 文件和 `.vmdk` 文件。
- 为业务虚拟机配置安全防护功能前，请确保已部署深度安全防护系统管理平台（DSM），且 DSM 管理网络与 CloudTower 管理网络需保持连通。DSM 提供云主机深度安全防护系统的 Web 控制台，具体操作方式请参考亚信 DeepSecurity 软件的官方文档。
- 请确保已按照[端口要求](/smtxos/6.3.0/os_property_notes/os_property_notes_114#%E7%AB%AF%E5%8F%A3%E8%A6%81%E6%B1%82)完成相关端口的开放与网络连通性检查。

**操作步骤**

1. 登录 CloudTower，进入集群的**设置**页面，为集群开启深度安全防护功能。

   具体操作请参考《SMTX OS 管理指南》的[为集群开启深度安全防护](/smtxos/6.3.0/os_administration_guide/os_administration_guide_324)小节。
2. 在集群中批量部署安全防护虚拟机（SVM）。集群中的每台主机需部署一个 SVM，用于为该主机中的虚拟机提供深度安全防护。

   1. 导入 SVM 模板（OVF 文件包）。

      具体操作请参考《SMTX OS 管理指南》的[部署安全防护虚拟机（SVM）> 导入 SVM 模板](/smtxos/6.3.0/os_administration_guide/os_administration_guide_325#%E5%AF%BC%E5%85%A5-svm-%E6%A8%A1%E6%9D%BF)小节。
   2. 部署 SVM。

      具体操作请参考《SMTX OS 管理指南》的[部署安全防护虚拟机（SVM）> 创建 SVM](/smtxos/6.3.0/os_administration_guide/os_administration_guide_325#%E5%88%9B%E5%BB%BA-svm) 小节。
3. 如需为业务虚拟机开启深度包检测功能，请在 Everoute 中配置网络安全导流功能。如您仅需开启防病毒功能，可直接跳转至步骤 4。

   1. 进入**网络与安全**页面，部署 Everoute 服务并启用网络安全导流功能。

      具体操作请参考《Everoute 安装与升级指南》的**部署前的准备**和**安装部署 Everoute** 小节。
   2. 进入 Everoute 服务的**服务设置** > **网络安全导流**页面，添加关联集群。您需要关联计划使用深度包检测功能的集群及其虚拟分布式交换机，并在该虚拟分布式交换机已关联的每台主机的 SVM 上配置一对导流网卡。

      具体操作请参考《Everoute 网络安全导流管理指南》的**关联集群**小节。
4. 为业务虚拟机配置深度安全防护功能。

   > **说明**：
   >
   > 仅支持在虚拟机创建完成后，通过**编辑虚拟机**的方式开启防病毒或深度包检测功能。

   - **开启防病毒功能**

     1. 确认集群中已上传 4.1.0 及以上版本的 SMTX VMTools 安装包，且业务虚拟机已安装 4.1.0 及以上版本的 VMTools。

        - 如未上传或安装，请参考《SMTX 虚拟机工具用户指南》的**安装 SMTX 虚拟机工具**小节。
        - 如版本不符合要求，请参考《SMTX 虚拟机工具用户指南》的**升级 SMTX 虚拟机工具**小节。
     2. 编辑虚拟机，开启防病毒功能。支持批量开启，启用后可支持防恶意软件、资产管理及入侵检测功能。

        具体操作请参考《SMTX OS 管理指南》的[编辑虚拟机 > 编辑基本信息](/smtxos/6.3.0/os_administration_guide/os_administration_guide_040)小节。
   - **开启深度包检测功能**

     编辑虚拟机，为虚拟网卡开启深度包检测功能。支持批量开启，启用后可支持 Web 信誉、防火墙、入侵检测及虚拟机补丁功能。

     具体操作请参考《SMTX OS 管理指南》的[编辑虚拟机 > 编辑基本信息](/smtxos/6.3.0/os_administration_guide/os_administration_guide_040)小节。
5. 登录 DSM 控制台，管理 SVM 并为已启用深度安全防护功能的业务虚拟机配置相关安全策略。具体操作请参考亚信 DeepSecurity 软件的官方文档。

**相关操作**

- **集群扩容**

  当集群后续进行扩容时，为确保新增主机能够正常使用深度安全防护功能，请按照如下步骤操作：

  1. 完成集群扩容操作。

     具体操作请参考《SMTX OS 运维指南》的[为 SMTX OS（ELF）集群添加新节点](/smtxos/6.3.0/os_operation_maintenance/os_operation_maintenance_46)小节。
  2. 进入集群的**设置** > **深度安全防护**页面，为新增主机创建 SVM。

     具体操作请参考《SMTX OS 管理指南》的[部署安全防护虚拟机（SVM）> 创建 SVM](/smtxos/6.3.0/os_administration_guide/os_administration_guide_325#%E5%88%9B%E5%BB%BA-svm) 小节。
  3. 如您之前已使用网络安全导流功能，则需在网络安全导流已关联的虚拟分布式交换机上为新增主机关联对应的物理网口。已在步骤 1 中为虚拟分布式交换机完成关联网口操作时，可忽略本步骤。

     具体操作请参考《SMTX OS 管理指南》的[编辑或删除虚拟分布式交换机 > 编辑虚拟分布式交换机](/smtxos/6.3.0/os_administration_guide/os_administration_guide_108#%E7%BC%96%E8%BE%91%E8%99%9A%E6%8B%9F%E5%88%86%E5%B8%83%E5%BC%8F%E4%BA%A4%E6%8D%A2%E6%9C%BA)小节。
  4. 进入 Everoute 服务的**服务设置** > **网络安全导流**页面，编辑关联集群，为新增主机配置一对导流网卡。

     具体操作请参考《Everoute 网络安全导流管理指南》的**编辑或解除关联集群**小节。
- **SVM 升级**

  当您需要升级 SVM 时，请直接在 DSM 中进行操作，CloudTower 无需进行任何额外配置。

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
