---
title: "visualization_cn/1.4.3/可观测性平台技术白皮书"
source_url: "https://internal-docs.smartx.com/visualization_cn/1.4.3/visualization_whitepaper/visualization_whitepaper_preface_generic"
sections: 39
---

# visualization_cn/1.4.3/可观测性平台技术白皮书
## 关于本文档

# 关于本文档

本文档主要介绍了在分布式系统变得日益复杂，给系统的运维、调试、排障带来全新挑战的背景下，SmartX 提供的可观测性解决方案。文档详细描述了 SmartX 可观测性平台的基本架构与组件，以及实现机制。

---

## 文档更新信息

# 文档更新信息

**2026-02-06：配合可观测性平台 1.4.3 正式发布**

---

## 概述

# 概述

随着分布式系统的广泛应用，软件系统的规模和复杂性不断增加，软件系统常常由许多相互连接的组件和服务组成。当系统发生故障时，可能涉及多个组件、服务和依赖关系，而传统的调试和故障排查方法已不再足够有效。此外，用户对系统高可用的期望也越来越高。因此，为了应对现代软件系统的复杂性、分布式架构和高可用需求，监控和理解每个组件和服务的行为，可观测性(Observability) 应运而生。

可观测性是指在系统运行过程中，通过从各种数据源收集和解析数据（例如日志、报警指标、数据流路径等），实现对系统内部运行状态和行为的跟踪和洞察。目前，可观测性已经成为现代分布式服务框架和大型系统中的重要一环，可以帮助开发和运维人员主动诊断、分析问题，并追踪问题根源，是构建稳定、高效和可靠系统的关键要素。

**产品功能**

SmartX 推出的可观测性平台包含网络流量可视化、指标监控、报警管理和日志管理功能。

- 网络流量可视化

  网络流量可视化支持自动生成的逻辑拓扑或列表直观展示网络连接情况，可高效支撑网络监控、日常巡检、网络运维、问题定位。同时，配合网络安全功能，网络流量可视化还可对网络安全策略进行监控和分析。
- 指标监控

  指标监控功能支持采集多集群的指标数据，为 CloudTower 及其他服务提供统一的指标存储及查询入口，用户可以针对不同集群、主机、虚拟机、物理盘等资源创建多种指标查询视图。
- 报警管理

  可观测性平台支持灵活可自定义的报警功能，支持多种报警源，通知策略的配置。报警涵盖 CloudTower 中的多种应用场景，包括系统服务的异常报警、集群虚拟机网络和系统网络的异常报警、虚拟机的自定义报警，并且可扩展集群的报警功能，为集群报警提供更丰富的通知配置，并根据需求配置灵活的静默、聚合通知策略。
- 日志管理

  日志功能可以收集集群中各服务运行产生的日志，并在 CloudTower 管理界面统一呈现。用户可以根据集群、节点、服务、级别和关键字进行日志查询，并支持将日志导入外部的 Syslog 服务器进行统一分析。

---

## 架构与组件 > 整体架构

# 整体架构

可观测性平台的架构如下图所示。

![](https://cdn.smartx.com/internal-docs/assets/0c1d230d/wp1.png)

下文将分别介绍在 CloudTower 虚拟机、可观测性服务虚拟机、与可观测性服务关联的 SmartX 集群和系统服务中运行的核心组件。

---

## 架构与组件 > CloudTower 核心组件

# CloudTower 核心组件

CloudTower 主要为用户提供可观测性服务的相关功能入口。在 CloudTower 虚拟机中运行的核心组件如下。

## Observability Operator

Observability Operator 是 SmartX 开发的基于 CloudTower K8s 底座的可观测性平台生命周期管理服务。该组件接收来自于 CloudTower 的调用请求，管理可观测性服务的生命周期（包括但不限于安装包管理、服务部署、升级、提高配置、卸载）、集群的关联、系统服务的关联等。

## Observability Manager

Observability Manager 是 SmartX 开发的基于 CloudTower K8s 底座的可观测性平台功能管理服务。该组件通过纳管 CloudTower 上已部署的所有可观测性服务，提供整合式的平台增强功能，例如为关联至可观测性服务的资源配置自定义报警的功能等。

## Application Manager

Application Manager 是 SmartX 开发的基于 SMTX 虚拟化能力和 CloudTower K8s 底座的应用框架，提供 CloudTowerApplication 包管理和服务管理功能，通过虚拟机与镜像分发的形式，在 CloudTower 上快速创建应用虚拟机实例，提供多种 CloudTower 系统服务。

## Host Plugin Operator

Host Plugin Operator 是 SmartX 开发的适用于 SmartX 集群的基础架构组件之一，可以对集群节点上的镜像容器组进行生命周期管理。

## Metrics Query Proxy

Metrics Query Proxy 是 SmartX 开发的基于 CloudTower K8s 底座的指标查询代理服务。集群的指标监控系统为了保证可靠性，可能同时存在多个数据源（集群本地监控、高级监控、可观测性服务），对指标查询带来了不便。Metrics Query Proxy 服务可以接收来自于 CloudTower、用户或其他服务的查询请求，并自动将查询请求转发至合适的数据源。

---

## 架构与组件 > 可观测性服务虚拟机核心组件

# 可观测性服务虚拟机核心组件

可观测性服务虚拟机包含的核心组件如下图所示。

![](https://cdn.smartx.com/internal-docs/assets/0c1d230d/wp2.png)

## 数据处理

可观测性服务使用 Vector 来充当数据管道，[Vector](https://github.com/vectordotdev/vector) 是一款开源的高性能、端到端的可观测性数据管道，同时支持 Agent 模式与 Aggregator 模式。Vector 提供了多种采集数据源（source）、灵活的数据处理配置（transform），并支持指定多种远端传输协议（sink）。Vector 支持配置多种消息重传策略、消息缓存策略，提供消息确保送达（delivery guarantee）的机制。

集群和系统服务的数据进行采集后将通过 Vector 进行发送，数据进入可观测性服务虚拟机的 Vector 服务后，通过预定义的数据管道，将不同类型的数据经过处理后写入对应的存储端。对于指标数据将写入 VictoriaMetrics 时序数据库，对于日志数据将写入 Loki 日志数据库，对于网络流量数据将首先写入 Network Analyzer，经过其流量分析后再聚合写入 Clickhouse 列式数据库。

## 数据存储

可观测性平台的数据存储由多个组件构成，其中包括开源的 [Loki](https://github.com/grafana/loki)、[VictoriaMetrics](https://github.com/VictoriaMetrics/VictoriaMetrics)、[Clickhouse](https://github.com/ClickHouse/ClickHouse) 和 [PostgreSQL](https://github.com/postgres/postgres)。

Loki 是一个轻量级高性能的日志聚合系统，设计灵感来源于 Prometheus，日志以由 labels 区分的 log stream 的形式存储。可观测性平台使用 Loki 存储日志数据。

VictoriaMetrics 是一个高性能的时序数据库，兼容所有的 Prometheus 查询语句并在其基础上扩展了更多实用的功能。可观测性平台使用 VictoriaMetrics 存储时序指标数据。

Clickhouse 是一个高性能的列式数据库，适用于海量结构化数据的 OLAP 应用。可观测性平台使用 Clickhouse 存储网络流量数据。

PostgreSQL 是一个高性能、稳定可靠的关系型数据库。可观测性平台使用 PostgreSQL 存储可观测性平台的元数据，包括但不限于报警规则、产生的报警、报警通知渠道、报警通知渠道匹配规则、关联的集群信息、租户鉴权信息、采集配置。

## 数据查询

可观测性平台的数据查询请求由用户发起，指标、日志和流量可视化的查询请求会发往各自的存储，然后把结果返回给 CloudTower，由 CloudTower 处理后做展示。

可观测性平台的数据查询将首先经过 Traefik 网关，[Traefik](https://github.com/traefik/traefik) 是一款开源的反向代理和负载均衡器，易于部署微服务，拥有灵活的中间件，包括负载均衡、API 网关、鉴权转发等。

根据查询数据类型的不同，查询路径也有所差异，对于日志和流量可视化数据查询，会经过 Grafana 组件。[Grafana](https://github.com/grafana/grafana) 是一个开源的支持多种数据源的强大查询引擎，提供了多种聚合查询方式，并且能够自定义开发查询数据源（Data Source）。

日志查询将使用 Grafana 的 Loki Data Source，通过 Log Stream 的过滤与聚合，查询出结构化日志。

流量可视化查询将使用 SmartX 开发的 Traffic Virtualization Data Source 和 Queryloader 聚合查询 Clickhouse 中的流量数据，以得到可视化数据。

指标查询将使用位于 CloudTower 的 metrics-query-proxy Pod 直接查询 VictoriaMetrics 时序数据库以获取指标数据。

## 控制面

可观测性平台的控制面主要用于控制可观测性平台的各项功能，用户的控制请求会发送给控制面组件进行处理和执行。控制面主要包括集群关联关系、采集解析配置生成、报警规则、多租户、鉴权、健康探测等信息。

Configcenter 是 SmartX 开发的可观测性平台组件之一，在可观测性平台纳管多个集群和多个系统服务的场景下，能够为每个集群生成指标和日志的采集（抓取）配置、数据处理（解析）配置以及存储配置，同时支持配置包括流量可视化、指标、日志在内的多种类型报警规则，并将报警规则转换为实际报警引擎支持的配置。

Configcenter Agent 可以将由 Configcenter 生成的配置抓取到对应的服务路径下（例如每个集群节点上的 Vector 工作路径），并且监听来自于 Configcenter 的配置更新事件。

Authcenter 是 SmartX 开发的可观测性平台组件之一，支持租户管理与鉴权，在可观测性服务关联多个集群与系统服务的场景下，使用租户将采集数据、报警等隔离开，并为每个租户提供访问可观测性 API 的权限管理。

Admin 是 SmartX 开发的可观测性平台组件之一，通过探测可观测性服务中的每个组件健康状态与业务链路，给出可观测性平台整体的健康状态，并且能够针对不健康的服务做出报警。

## 报警链路

可观测性平台的报警链路包含多个组件，其中包括开源的 [Vmalert](https://github.com/VictoriaMetrics/VictoriaMetrics/tree/master) 和 [Alertmanager](https://github.com/prometheus/alertmanager)。

Vmalert 提供了基于指标类型的报警触发引擎。

Network Analyzer 是 SmartX 开发的可观测性平台组件之一，支持基于 Clickhouse 中的流量数据进行聚合查询与报警。

Alertmanager 是一款开源的报警接收、处理组件，提供了报警预处理（去重、分组等）的能力。可观测性服务的报警链路使用 Alertmanager 接收报警并对报警进行预处理。

Alertmanager Extension 是 SmartX 开发的可观测性平台组件之一，支持将报警处理后进行二次渲染与持久化。该组件包含以下功能：

- 对 Alertmanager 的报警进行持久化，按照业务需求对报警数据进行处理。
- 通过配置文件对报警进行渲染。
- 提供 API，包括报警的查询与手动解决。
- 根据聚合配置将报警按照对象和规则分组聚合后向 Notifycenter 发送通知。
- 根据静默配置判断当前是否需要向 Notifycenter 发送通知。

Notifycenter 是 SmartX 开发的可观测性平台组件之一，支持将报警通过灵活的匹配机制和多种消息通知渠道发送到外部，其消息确保送达机制保证了报警的可靠性。该组件包含以下功能：

- 对 Alertmanager Extension 发送的通知信息进行处理，最终发送给用户配置的外部通知服务。
- 对于集群转发的报警，在每次发送通知消息后会进行 Callback。
- 提供 API，包含通知渠道和报警发送规则。
- 通知渠道扩展能力。提供更多的通知方式，当前已经支持 SMTP、SNMP 等。

## 多租户

一个软件实例可以为多个不同用户提供服务，这是租户概念的来源。在可观测性平台中，租户是用来区分不同数据所有者（来源）的一种方式。

当前可观测性平台的租户包括集群和系统服务。在可观测性平台中，租户的管理主要由 Authcenter 组件管理，一个租户主要包含以下信息：

- api\_key
- tenant\_id
- status (ACTIVE/INACTIVE)

SmartX 集群资源在可观测性平台中也是以租户的形式区分，集群 tenant\_id 为 cluster\_uuid；而对于系统服务，在关联时，会先向 authcenter 注册租户，生成 api\_key, tenant\_id。

在可观测性平台中，每个租户的数据并没有进行硬隔离，是通过 tenant\_id 来区分来自于不同租户的数据，例如：

- 指标、日志：数据的 labels 中由 \_tenant\_id 字段来过滤不同租户数据。
- 报警规则、报警：通过 tenant\_id 字段来过滤不同租户数据。

## 网关鉴权

进入可观测性平台的网络请求都会经过 Traefik 网关，网关为可观测性服务虚拟机中的每个服务配置了多种访问和鉴权（指验证用户是否拥有访问系统的权利）方式：

- HTTP Basic Auth 鉴权，账号密码匹配后直接放行请求。
- HTTP Header X-API-Key 鉴权，请求会先被转发至 Authcenter，Authcenter 会将该租户对应的 tenant\_id 注入 Header 中再将请求发送至下游。
- gRPC 无鉴权，但需要在 Header Grpc-Service 中指定需要访问的服务。

针对第二点举个例子，如下图，在关联系统服务时，会由 Observability Operator 向 Authcenter 注册租户，在获取到 API Key 后，会使用该 API Key 向 Configcenter 注册对应系统服务的报警规则，此时 Configcenter 即可从 Header 中获取当前注册报警规则的租户（tenant\_id），从而将当前报警规则以及该报警规则产生的报警都打上这个租户的标签。

![](https://cdn.smartx.com/internal-docs/assets/0c1d230d/wp3.png)

---

## 架构与组件 > Agent 组件

# Agent 组件

Agent 主要负责日志、指标和流量可视化数据的采集和处理，并将数据压缩后发送到可观测性虚拟机。

---

## 架构与组件 > Agent 组件 > 集群中 Agent 组件

# 集群中 Agent 组件

SmartX 集群（包含 SMTX OS 集群、SMTX ZBS 集群和 SMTX ELF 集群）可以在 CloudTower 上关联至可观测性服务，关联后 Observability Operator 将调用 Host Plugin Operator 为集群节点下发可观测性服务 Agent 镜像，并启动 Agent 容器进行数据采集。

![](https://cdn.smartx.com/internal-docs/assets/0c1d230d/wp4.png)

集群中的 Agent 包含的组件如下。

## Vector

在 Agent 端 Vector 主要用于采集节点日志和充当数据管道，其他采集器所采集上来的数据也会发往 Vector 服务，统一交由 Vector 进行预处理后，以不同形式的 payload 发往可观测性服务虚拟机。

## Vmagent

[Vmagent](https://github.com/VictoriaMetrics/VictoriaMetrics) 是一款开源的指标数据抓取轻量级代理，通过拉取和推送协议接收指标，对其进行转换并发送到兼容 Prometheus Remote Write 协议的远端。

在 Agent 端 Vmagent 主要用于采集节点的 Exporter 暴露出来的指标，并通过 Prometheus Remote Write 协议推送给本地的 Vector，再经由 Vector 推送到可观测性服务虚拟机。

## Network Collector

Network Collector 是 SmartX 开发的用于采集各节点的多元网络信息元数据的组件，包括活动的虚拟机网卡信息、虚拟机之间的连接信息、主机系统网络的连接信息、流量统计、计数统计等，并根据数据类型（如 Port Counter、CT Flow 等）对数据进行过滤，然后对相同类型的数据进行初始聚合，将分散的数据点映射成完整的信息流，合并为连接信息、流量统计信息。

在 Agent 端 Network Collector 采集的信息会推送到本地的 Vector 服务，经由 Vector 推送到可观测性服务虚拟机。

## Configcenter Agent

Configcenter Agent 是 SmartX 开发的用于拉取、监听配置变更的组件，通过与可观测性服务虚拟机中的 Configcenter 建立长连接（gRPC），从而能够及时地监听到配置的变更事件，通过配置多组指定的 labels 即可拉取到对应的服务配置（包括 Vector 的日志抓取配置、Vmagent 的指标采集配置等）。

---

## 架构与组件 > Agent 组件 > 系统服务中 Agent 组件

# 系统服务中 Agent 组件

系统服务有一些指标、日志的采集需求和异常报警需求。但系统服务跟 SmartX 集群的节点存在不同，它们没有统一的 Containerd API 可以下发镜像并启动容器，系统服务的可观测性依赖各系统服务集成可观测性平台提供的 Agent，Agent 的设计主要有以下几点：

- 负责管理 Vector 和 Vmagent 进程的生命周期和采集配置。
- 需要通过鉴权（合法租户）才可以向可观测性服务发送数据。
- 通过 Management API 对外暴露 Agent 的生命周期控制。

---

## 数据处理链路 > 数据发送

# 数据发送

![](https://cdn.smartx.com/internal-docs/assets/0c1d230d/wp5.png)

可观测性服务的数据管道主要由 Vector 构成，数据以 Batch Payload 的形式发送，通过 HTTP Request + Gzip + Basic Auth 的方式发送至可观测性服务虚拟机的网关上，通过鉴权后再执行后续动作。

Batch Payload 通常为 JSON 数组，每秒发送一次，所以可观测性服务虚拟机所承受的来自于集群的 QPS （Queries Per Second，每秒请求数）约为所关联集群节点总数 × 3（指标、日志、流量数据的 Batch Payload 互相独立）。

不同 Batch Payload 的 Request Size 分别约为：

- 指标：~25 KiB/s
- 日志：~4 KiB/s
- 流量：~60 KiB/s

因此，集群中用于可观测数据传输的流量大小计算方式为：关联到可观测性服务的集群节点数量 × 89 KiB/s，例如关联了 20 个节点到可观测性服务上，则管理网中所消耗的流量约为 1.74 MiB/s，按两倍峰值流量计算（考虑查询等流量），约为 3.48 MiB/s。

Vector 的消息确保送达机制依赖了 in-memory buffer（也有提供 disk buffer，但考虑到不为节点新增额外的 IO 压力，所以没有使用 disk buffer），若数据发送至下游出现异常，数据将被缓存到内存中，不同的数据类型有不同的发送缓存策略：

- 指标：最大缓存 500 个 event，buffer 满时阻塞请求，无限重试上限，最大重试间隔 1h。
- 日志：最大缓存 500 个 event，buffer 满时阻塞请求，重试次数上限为 20 次，最大重试间隔 30s。
- 流量：最大缓存 50 个 event，buffer 满时丢弃新的数据，重试次数上限为 3 次，最大重试间隔 15s。

指标数据 event 通常较小，且发送数据至下游（prometheus\_remote\_write 协议）时不会出现不可重试的错误（例如 Bad Request），并且如果丢弃数据会造成时序数据断点，所以重试次数设置为无限。

日志数据 event 通常也不会很大，但发送至下游时可能会出现不可重试的错误（例如 schema 解析失败、时间戳大于当前 Loki 允许写入的时间窗口），所以设置了重试次数上限。但又希望在网络不稳定时尽量减少丢弃的事件，所以重试次数上限设为了 20 次，最大重试间隔为 30s（即容忍的网络异常时间上限为 10 分钟，超过以后开始丢弃日志 event）。

流量数据报文 event 通常较大，所以最大缓存 50 个 event，且流量数据较多，为了保证业务的性能，不希望阻塞采集，所以采用的策略是 buffer 满时丢弃数据，且重试次数设置的较少。

---

## 数据处理链路 > 数据接收

# 数据接收

![](https://cdn.smartx.com/internal-docs/assets/0c1d230d/wp6.png)

可观测性服务虚拟机通过 Traefik 网关处理所有请求，其中包括 Vector 发来的数据，网关通过 Url Path 路由不同服务的 api 请求，例如：

- /vector/sources/metrics
- /vector/sources/logging
- /vector/sources/traffic
- /configcenter/api/v3/alertingRules
- /victoriametrics/api/v1/query
- /alertmanager-extension/api/v3/alerts

经过 Traefik 网关的请求大部分都会经过鉴权组件 Authcenter，该组件验证 X-Api-Key 或 Basic Auth 合法后，再路由请求到下游组件，这些请求包括 Agent 发来的数据，不同的数据类型会发往不同的 Url Path，网关将根据不同的 Url Path 转发到可观测性服务虚拟机中 Vector 的不同端口上：

- /vector/sources/metrics -> vector:20001 (metrics source)
- /vector/sources/logging -> vector:20002 (logging source)
- /vector/sources/traffic -> vector:20003 (traffic source)

将不同类型的数据路由到不同容器端口上的原因是 Vector 的反压机制（Back Pressure）保证了端到端的网络异常阻塞，即如果下游请求失败，将会阻塞源头数据接收。例如，若 Loki 组件异常，日志无法存储，则集群节点上的 Vector 将无法发送 logging payload，请求将被阻塞（反映到日志上是 request timeout）。若不同类型的数据共用一个 Vector 容器端口，日志的反压会导致 metrics payload 请求也被阻塞。

---

## 数据处理链路 > 数据处理

# 数据处理

不同类型的数据到达可观测性服务虚拟机的 Vector 后，会经过不同的处理路径：

- 指标：由于指标在采集时即已在 Agent 端附加好了标签（cluster\_uuid, tenant\_id, instance），所以数据到达可观测性服务虚拟机后将直接下沉到存储端 VictoriaMetrics 时序数据库。
- 日志：重点需要处理的部分，因为把日志解析的规则放在 Agent 端会增加集群节点的 CPU、内存占用，为了节省节点的计算资源，日志解析都放到可观测性服务虚拟机中进行，日志解析规则会在关联集群前生成。这里的解析规则主要就是用正则来匹配日志中的时间戳（timestamp）、日志级别（severity），然后以 Structure Log 的形式存入 Loki。
- 流量：转发给 Network Analyzer 进行处理分析，然后由 Analyzer 存入 Clickhouse。

---

## 服务基础运维管理

# 服务基础运维管理

可观测性服务虚拟机的服务基础运维管理主要包括部署可观测性服务、关联 SmartX 集群和关联系统服务的操作，这些操作均由 CloudTower 中的 Observability Operator 组件控制。在 CloudTower 上关联 SmartX 集群（包含 SMTX OS 集群、SMTX ZBS 集群和 SMTX ELF 集群）与可观测性服务时，Observability Operator 将通过 Host Plugin Operator 下发并启动 Agent 进行数据采集，然后将数据发送至可观测性服务虚拟机；在 CloudTower 上关联系统服务与可观测性服务时，Observability Operator 会将关联信息下发至系统服务虚拟机中的 Agent，Agent 开始采集并发送数据至可观测性服务虚拟机。可观测性服务对数据进行处理与存储后，CloudTower 可访问其 API 查询对应数据。

---

## 服务基础运维管理 > 部署可观测性服务

# 部署可观测性服务

可观测性服务是 CloudTower 的系统服务之一，安装部署等运维操作通过运行在 CloudTower 中的 Observability Operator 实施，可观测性服务的部署主要依赖 Application Manager（负责通过虚拟机模板和镜像分发的形式快速部署应用）和 Host Plugin（负责镜像分发，控制 SmartX 集群节点上的容器服务）两个组件，如下图所示，可观测性服务安装包中的内容即各服务的镜像文件，在实际部署时下发到对应远端。

![](https://cdn.smartx.com/internal-docs/assets/0c1d230d/wp7.png)

---

## 服务基础运维管理 > 关联集群

# 关联集群

在可观测性服务关联集群之前，需要先为目标集群生成采集配置，因为可观测性服务需要兼容多种集群版本，不同集群版本可能会有不同的采集、解析配置。生成配置的组件为可观测性服务虚拟机中的 Configcenter，在关联集群时，Configcenter 会先通过集群的接口获取集群信息，进而生成指标、日志的采集、抓取配置，并存放在 Configcenter 中。

准备好抓取配置后，会向 CloudTower 中的 Host Plugin Operator 下发创建 Host Plugin 的请求，其会向目标集群的所有节点下发安装包中所包含的镜像（通过 Containerd API），然后拉起配置文件中声明的容器（类似于 Compose 配置）。

在声明的容器中，首先会执行的是 ovm-agent-init 容器，该容器主要初始化了 Configcenter Agent 的配置，以及集群 envoy-xds 服务的配置（服务发现），这样一来集群上的服务可在无需知晓可观测性服务 IP 的情况下访问可观测性服务提供的 API。

在初始化容器执行完毕后，将启动主要的几个组件容器：

- Configcenter Agent 从可观测性服务虚拟机上的 Configcenter 服务拉取配置，提供给 Vector 和 Vmagent 服务。
- Vector 服务负责日志的采集和数据推送。
- Vmagent 和 Network Collector 会将采集到的数据推送给 Vector 服务，由 Vector 服务将数据发送至可观测性服务虚拟机。

![](https://cdn.smartx.com/internal-docs/assets/0c1d230d/wp8.png)

---

## 服务基础运维管理 > 关联系统服务

# 关联系统服务

关联系统服务到可观测性服务，将由 Observability Operator 控制执行以下关联步骤：：

- Observability Operator 向可观测性服务注册租户，生成 API Key。
- Observability Operator 向可观测性服务注册当前租户的报警规则。
- Observability Operator 将租户信息（包括 API Key）通过 Agent Management API 发送至系统服务中的 Agent 服务。
- 系统服务中的 Agent 在通过租户鉴权后，开始启动 Vector 和 Vmagent 进程抓取并发送数据，即开始采集并向可观测性服务发送监控指标。

![](https://cdn.smartx.com/internal-docs/assets/0c1d230d/wp9.png)

---

## 功能实现 > 网络流量可视化

# 网络流量可视化

网络流量可视化的核心原理是利用数据可视化技术对网络流量数据进行可视化呈现。具体实现流程如下：

1. 数据采集

   在虚拟化场景中，网络数据源分布在集群的各个主机上，数据分散且种类多。网络流量可视化通过分布在各节点的分布式采集器实时采集各节点虚拟化环境中的网络数据，并进行数据的过滤和初始聚合，然后送往分析平台进行后续处理。
2. 数据分析

   分布式采集器的网络数据包含大量 IP 地址和端口名称等信息，这些信息不足以直观的反映虚拟机或者主机的流量详情，在发送至分析平台后，分析平台相关组件将对其进行统计、聚合、分析等处理，以提取有用的信息。此外，还会从 CloudTower 和 Kubernetes 集群同步与虚拟机、网卡、Pod 有关的元数据。
3. 数据可视化

   分析处理后的数据，通过 CloudTower 进行图形化展示，便于用户实时、直观地监控网络流量。

---

## 功能实现 > 网络流量可视化 > 数据采集

# 数据采集

网络流量可视化在每个节点均有一个 Network Collector 组件，用于采集各节点的多元网络信息元数据，包括活动的虚拟机网卡信息、虚拟机之间的连接信息、主机系统网络的连接信息，流量统计，计数统计等，并根据数据类型（如 ARP 报文、Port Counter、CT Flow 等），对数据进行过滤，然后对相同类型的数据进行初始聚合，将分散的数据点映射成完整的信息流，合并为连接信息、流量统计信息。

最终，Network Collector 将采集数据上送至节点的 Vector 组件，进一步上传至可观测虚拟机。Vector 具有数据压缩和数据缓存的能力，可完成高效可靠的数据传输。

---

## 功能实现 > 网络流量可视化 > 数据分析

# 数据分析

数据的分析和处理主要由 Network Analyzer 组件完成。Network Analyzer 会对端到端的网络数据和安全策略相关数据进行解析。解析后的数据可以与 CloudTower 中的数据相结合，最终在可视化 UI 界面上呈现节点和节点之间、虚拟机和虚拟机之间的网络通信情况，以及流量被生效的安全策略或监控模式下的安全策略允许或拒绝的情况。

完成数据分析后，Network Analyzer 将数据缓存至本地存储，并定时推送到 Clickhouse 中存储。整个数据接入过程中采用了 protobuf 进一步压缩数据。

---

## 功能实现 > 网络流量可视化 > 数据可视化

# 数据可视化

网络数据经过分析处理后，存入 Clickhouse 组件中。当用户在 CloudTower 界面进行流量可视化查看和操作时，CloudTower UI 通过 REST API 向 CloudTower Server 发起请求，CloudTower Server 会将请求转发至 Grafana，Grafana 通过 SQL 从 Search Engine 查询和获取相关数据，返回给 CloudTower，最终由 CloudTower UI 进行 Web 前端渲染，在界面通过概览视图、拓扑视图、表格视图以及多种交互方式向用户展示虚拟机网络及系统网络中的流量信息。

---

## 功能实现 > 指标监控

# 指标监控

指标管理是指将集群中多个服务的 Exporter 及系统服务的 Exporter 所暴露的指标数据，经过采集器抓取后，以时序数据的形式统一存储在可观测性服务中，用户可基于这些数据创建监控视图，并基于这些时序数据创建报警规则。

---

## 功能实现 > 指标监控 > 指标采集

# 指标采集

可观测性服务使用 Vmagent 作为指标采集器。对于集群节点上的 Exporter 指标采集，在将集群关联至可观测性服务时，Configcenter 会向集群 API 请求集群的服务注册信息，获取需要抓取的指标 Exporter 配置（包含 URL、端口等），并生成 Vmagent 的抓取配置。节点上的Vmagent 启动采集后，会将采集到的数据转发至当前节点的 Vector 数据管道，Vector 数据管道会对收集到的指标数据注入一些当前节点的信息，包括 cluster\_uuid, \_tenant\_id 和 instance label。

---

## 功能实现 > 指标监控 > 指标存储

# 指标存储

到达可观测性服务虚拟机的指标数据会经由虚拟机的 Vector 组件下沉至 VictoriaMetrics 时序数据库。指标数据将在时序数据库中存储一年的时间。

---

## 功能实现 > 指标监控 > 指标查询

# 指标查询

由于集群的指标监控体系较为复杂，在没有可观测性平台之前，集群监控系统由本地监控和高级监控组成，在加入可观测性平台后，指标查询一共有三处数据源，分别是：

- 集群本地监控，数据源为集群节点上的 Prometheus，查询接口通过 Octopus API 提供。
- 集群高级监控，数据源为高级监控虚拟机上的 Prometheus，查询接口通过 Octopus API 提供。
- 可观测性服务，数据源为可观测性服务虚拟机上的 VictoriaMetrics，查询接口通过 VictoriaMetrics API 提供。

多处数据源对前端和用户查询造成了不便，为了简化查询，在 CloudTower 中提供了 Metrics Query Proxy 组件，该组件的作用是根据查询目标，自动选择数据源。对于已关联到可观测性服务的集群，将直接查询可观测性服务虚拟机上的 VictoriaMetrics 数据源；对于未关联的集群，会将查询代理到集群节点上的 Octopus 服务，Octopus 服务决定转发至高级监控还是本地监控。

![](https://cdn.smartx.com/internal-docs/assets/0c1d230d/wp10.png)

---

## 功能实现 > 指标监控 > SNMP 传输

# SNMP 传输

可观测性服务通过 SNMP Extension 组件将关联集群的监控指标数据通过 SNMP 协议对外提供，第三方监控软件（例如 Zabbix）仅需关联一个可观测性虚拟机即可获取所有纳管集群的监控指标，同时 SNMP Extension 会根据纳管集群自动生成对接所需的模板文件，对接时可一键导入。

---

## 功能实现 > 报警管理

# 报警管理

![](https://cdn.smartx.com/internal-docs/assets/0c1d230d/wp11.png)

可观测性服务的报警来源根据报警触发通路的方式分为以下几种：

- 直接由报警发送方投递报警给 Alertmanager：
  - 关联集群转发的报警：指定版本的集群关联可观测性服务时，集群本地的报警会由 Siren 转发给可观测性服务。
  - 流量可视化报警：可观测虚拟机中的 Network Analyzer 容器会监控网络数据指标，若相关指标报警规则中设置的阈值，将触发报警，并将报警发送至 Alertmanager。
- 注册 Vmalert 报警规则，由 Vmalert 投递报警给 Alertmanager。当前系统服务可观测的报警、自定义报警均通过该方式触发报警。

投递到可观测的报警按照解决方式可以分为以下两类：

- 自动解决类：需要持续投递给 Alertmanager，一段时间不投递 Alertmanager 就会自动发送 Webhook 解决 Alertmanager Extension 中持久化的报警。
- 手动解决类：只需要投递一次，投递后一直为未解决状态（Alertmanager Extension 会忽略 Alertmanager 的自动解决 Webhook），只能被用户手动解决。

---

## 功能实现 > 报警管理 > 报警规则

# 报警规则

## 报警规则管理

可观测性服务通过 Configcenter 服务对外提供报警规则管理 API，在 CloudTower 中调用方主要来自于：

- cloudtower-server: 调用 Configcenter 提供的报警规则相关 API，为用户提供查看内置报警规则、修改阈值和禁用内置报警规则功能。
- observability-operator: 关联系统服务时，系统服务调用方通过该服务提供的接口进行关联，该服务将通过 Configcenter API 注册相关内置报警规则。
- observability-manager: 自定义报警规则通过该服务进行统一管理，该服务将自定义报警规则转发至对应可观测性服务的 Configcenter API 注册相关自定义报警规则。
- 其他系统服务调用方

同时，Configcenter 将同步报警规则相关的修改，并将报警规则以配置文件或 API 的形式下发至 Network Analyzer、Alertmanager Extension 和 Vmalert。

## 自定义报警

自定义报警功能主要由位于 CloudTower 中的 observability-manager 组件完成，该功能主要由两个功能模块构成：

- 报警规则配置功能模块：用于计算自定义报警规则中的报警对象对应到不同可观测性服务上的报警表达式。
- 元数据缓存功能模块：用于管理不同可观测性服务上对于集群、虚拟机名称等元数据的缓存。

### 报警规则配置

自定义报警规则配置功能模块负责处理用户创建的自定义报警规则，并将其转换为可观测性服务可识别的报警表达式。

observability-manager 组件通过以下步骤管理自定义报警规则的配置：

1. **规则接收与验证**：接收来自 CloudTower 的自定义报警规则请求，验证规则的有效性和完整性。
2. **规则转换**：将高级抽象的自定义报警规则转换为具体的报警表达式。根据不同的报警对象类型（如虚拟机等）生成相应的查询语句。
3. **表达式计算**：基于报警规则中设置的报警对象、阈值、持续时间和报警级别，计算出完整的报警判定表达式。
4. **规则下发**：将计算好的报警表达式通过 Configcenter API 注册到对应的可观测性服务上。系统会将自定义报警规则转写为 Vmalert 服务的配置文件，由 Vmalert 周期性执行查询并触发报警。
5. **规则同步**：当报警规则发生变更（如修改、禁用或删除）或报警对象发生变更时，及时同步更新至所有相关的可观测性服务。

### 元数据缓存

元数据缓存功能模块负责同步和下发来自 CloudTower 的元数据缓存至不同可观测性服务，确保报警通知文案中的虚拟机名称等内容为最新的元数据。

observability-manager 组件实现了资源变更事件监听机制，具体包括：

1. **元数据同步**：从 CloudTower 获取集群、虚拟机组、虚拟机等元数据信息，如名称、UUID、关联关系等。
2. **缓存建立**：将采集到的元数据信息建立本地缓存，提高自定义报警规则的转换和查询效率。
3. **事件监听**：从 CloudTower 监听资源的变更事件，包括资源的创建、修改、删除等操作。
4. **实时更新**：当资源发生变更时，实时更新本地元数据缓存，确保报警规则始终能够关联到最新的监控对象。
5. **命名解析**：将报警规则中使用的资源名称正确映射到可观测性服务中的资源标识符。
6. **缓存下发**：同步的缓存将通过全量或增量的方式下发至对应资源所关联的可观测性服务。

元数据缓存的存在使得自定义报警规则能够在资源发生变化（如虚拟机迁移、重命名等）时仍然能够正确地关联资源和触发报警，提高了自定义报警功能的可靠性和稳定性。

---

## 功能实现 > 报警管理 > 报警源

# 报警源

Configcenter 将报警规则下发至相应组件后，各组件将根据报警规则验证并触发报警，并发送至 Alertmanager 中：

- 流量可视化报警：Network Analyzer 会监控网络数据指标，若网络数据超过相关指标报警规则中设置的阈值，将触发报警，并将报警发送至 Alertmanager 中。
- 系统服务报警：Vmalert 根据系统服务注册的报警规则触发报警发送至 Alertmanger。
- 关联集群转发的报警：集群在关联可观测性服务后新产生的所有报警，都会通过本地服务发现投递给可观测性服务的 Alertmanager。
- 自定义报警：Vmalert 根据自定义报警规则触发报警发送至 Alertmanager。

Alertmanager 收到报警后，会将报警以 Webhook 方式发送至 Alertmanager Extension 进行进一步处理。

综上，当前报警触发源共有 3 处：

- Vmalert 服务，专门针对 metrics 类型数据的报警，周期性在 VictoriaMetrics 中执行查询语句，判定报警规则是否符合条件，并决定是否向下游（Alertmanager）发送报警。目前包含如下业务报警：
  - 集群额外报警规则（仅在内部启用，包含 cgroup、systemd 之类的报警）
  - 系统服务异常报警（CPU、内存、磁盘、时钟）
  - 自定义报警（虚拟机）
- Network Analyzer 服务，专门针对流量类型数据的报警，周期性在 Clickhouse 中执行查询语句，判定报警规则是否符合条件，并决定是否向下游（Alertmanager）发送报警。
- 在可观测性以外的服务也可以向可观测性服务虚拟机投递报警（通过 Alertmanager 接口），目前会向可观测性服务投递报警的服务有集群上的 Siren 服务。集群被关联至可观测性服务后，集群本地监控所产生的报警将被 Siren 服务转发至可观测性服务虚拟机，以统一报警源，使用可观测性更丰富的报警通知功能。

---

## 功能实现 > 报警管理 > 报警处理

# 报警处理

Alertmanager Extension 在接收到 Alertmanager 发送的报警信息后，会进行如下处理:

1. 根据报警来源，采用不同方式计算 fingerprint 并持久化存储到 PostgreSQL 数据库。
2. 如果这个报警是一个没有报警文案的报警，会将报警信息和 Configcenter 下发的报警规则进行匹配，获取原始的未渲染的报警内容。
3. 根据用户配置、报警阈值和实时信息，周期性渲染或更新报警内容的部分字段，并更新报警信息。
4. 根据报警是否解决生成不同报警通知模版，然后调用 Notifycenter API 将处理后的报警通知模版写入或更新到 PostgreSQL 数据库 。

Alertmanager Extension 还会对报警进行如下处理以应对复杂或异常业务场景：

- 报警去重：过滤重复报警。
- 报警级别抑制：当同时触发了高级别和低级别的报警时，将抑制低级别报警的发送。
- 过期报警处理：对长时间未变化报警进行过期处理。
- 报警聚合：根据用户配置聚合一段时间内触发的相同对象、相同规则的报警。
- 报警静默：根据用户配置静默指定时间段内指定对象触发的所有报警通知。

---

## 功能实现 > 报警管理 > 报警查询与通知

# 报警查询与通知

用户在 CloudTower 查看报警时，CloudTower 会调用 Alertmanager Extension 提供的报警相关的 API，为用户提供查看报警和手动解决报警的功能。

可观测性平台支持将报警通过 SMTP 发送至外部邮箱，或者通过 SNMP V2 Trap 将报警信息发送至第三方监控平台。CloudTower 可调用 Notifycenter 的通知渠道相关 API，向用户提供 SMTP 和 SNMP Trap V2 的配置功能，用户可以在 CloudTower 配置多个 SMTP 和 SNMP Trap V2 接收者且自定义报警通知语言（中文或英文）。

报警通知主要由 Notifycenter 完成。Notifycenter 包含分发模块和通知模块。分发模块会定时获取 PostgreSQL 中所有处于活跃状态的报警通知模版，为其创建对应的发送任务并写入到 PostgreSQL 中，已经解决的报警会在创建一次发送任务后，将报警通知模版标记为非活跃状态。通知模块会每秒轮询 PostgreSQL 中的发送任务。

对于关联集群转发的报警，为保证集群转发的报警在可观测性服务异常时仍能够通过集群本地兜底发送，增加了报警 Callback 机制，Notifycenter 会在成功通过任意通知渠道发送成功后，回调集群的报警 Callback 接口，此时集群便不再通过本地兜底发送。

---

## 功能实现 > 报警管理 > 服务异常自监控报警

# 服务异常自监控报警

自监控报警能力是提高可观测性平台服务产品质量的重要环节。

当某一可观测性服务虚拟机的报警链路发生故障时，CloudTower 报警列表中会显示报警链路异常报警。同时，对于配置了报警渠道的可观测性服务虚拟机（服务异常自监控报警**当前仅支持邮件类型的报警渠道**），Observability Operator 会向该邮箱发出报警邮件（需保证 Observability Operator 所在的虚拟机与所配置的 SMTP 服务器网络联通）。

所谓报警链路，是体现在可观测性服务虚拟机内部 Vmalert、VictoriaMetrics、Alertmanager、Alertmanager Extension、Notifycenter、PostgreSQL 这六个容器上，换言之，一条报警信息，会经由这六个组件进行传递，最后发送给用户。一旦这六个组件中的任一组件出现故障，都会导致用户无法接收到报警。

为此，在 Observability Operator 控制面引入对可观测性服务虚拟机报警链路的监控，同时，在可观测性服务虚拟机内部引入 Admin 容器，Admin 容器的能力体现在：

- 对可观测性服务虚拟机中运行的核心容器的探活能力。
- 接收在可观测性服务虚拟机内持续触发的 e2e 报警，用于模拟真实报警信息。

一旦 Observability Operator 控制面无法感知某一可观测性服务虚拟机的 Admin 组件正常工作，或者某一可观测性服务虚拟机的 Admin 组件的报警链路健康状态不正常，则会触发服务异常自监控报警。

这在很大程度上解决了可观测性服务虚拟机异常场景下，用户无法感知以及收到任何报警的问题。

---

## 功能实现 > 日志管理

# 日志管理

日志相关的数据流交互主要包括日志采集、日志处理、日志存储、日志查询和日志传输。

1. **原始日志采集**

   通过部署在集群节点上的日志采集器，实时采集各节点产生的原始日志数据，进行初步处理后发送到可观测性虚拟机进行后续处理。
2. **日志处理**

   从节点采集的原始日志信息较为分散，格式不够统一，可观测性虚拟机在接收到从节点采集的原始日志后，会将对日志进行进一步处理，例如解析日志级别、增加服务标签、解析时间戳等，以提取格式完整和统一的日志数据。
3. **日志存储**

   经过处理后的数据将进行存储，并对日志建立标签索引，将具有相同标签的日志归类为同一日志流，便于用户在查找时能够快速准确地定位某一类日志。
4. **日志查询**

   用户可以在日志查询界面通过指定日志标签或输入关键词，查询日志存储系统中的数据。
5. **日志传输**

   用户也可以通过配置将从节点采集的日志文件实时传输到外部的 Syslog 服务器中以便进行进一步的分析。

---

## 功能实现 > 日志管理 > 原始日志采集

# 原始日志采集

集群日志采集由集群中的 Agent 的 Vector 组件完成。可观测性服务在关联集群后，Configcenter 会为集群下发 Vector 配置，配置生效后 Vector 组件会立即开始监听并采集节点上各服务的日志文件。采集过程中，如果可观测性虚拟机处于不可达状态，日志采集会停止；Vector 仅采集集群关联可观测性服务后产生的日志，不采集已产生的历史日志。日志采集完成后会在 Vector 内部进行处理后发往可观测性虚拟机。

---

## 功能实现 > 日志管理 > 日志处理

# 日志处理

日志处理由集群的 Agent 中的 Vector 和可观测性虚拟机中的 Vector 共同完成。

集群的 Agent 中的 Vector 会对采集到的日志进行以下初步的处理：

- 识别多行属于同一条日志的行，并拼接为一行完整的日志。
- 通过日志文件路径推断产生日志的系统服务名称，为每条日志添加 service 标签。
- 为来自同一个集群的所有日志添加一个共同的 cluster\_uuid 标签，同时集群 uuid 也会作为集群的租户 id 标签 \_tenant\_id。

集群的 Agent 中的 Vector 完成初步处理后的日志发送到可观测性虚拟机中的 Vector，对日志进一步进行如下处理：

- 通过日志内容提取日志级别，为日志添加 severity label，如果未提取到正确的级别会设置为 info。
- 通过日志内容解析时间戳，作为日志字段 log\_timestamp 的值。
- 为可观测性服务内部服务组件添加系统服务标签。
- 部分 JSON 格式的日志在采集时会保存为文本，针对这类日志会将文本解析成 JSON 后存储到 message 字段。

日志在经过 Vector 处理后写入到 Loki 进行存储。

---

## 功能实现 > 日志管理 > 日志存储

# 日志存储

在可观测性虚拟机中，经由 Vector 处理后的日志将存入 Loki 组件。Loki 中存储的日志由日志标签和日志内容组成。Loki 为每条日志分配了一个或多个标签，并建立标签与日志的映射关系，具有相同标签组合的日志会进入同一个日志流（stream），这使得大量日志可以被高效分类与过滤。

- **日志标签**

  可观测性服务采集并存储的日志会携带如下标签。用户在查询时可以通过日志标签对日志流进行过滤，也可以输入关键词对日志内容进行过滤，也可以组合上述两种方式进行过滤。

  | 标签 | 说明 | 示例 |
  | --- | --- | --- |
  | \_tenant\_id | 租户 id，唯一标识产生日志的来源。 | BACKUP\_SERVICE-cltpa8e8a117t29ud70rf8q04\_fCqB |
  | cluster\_uuid | 表示产生日志的集群。 | d73d1a37-6e4b-4238-acd0-64ca8f496af8 |
  | instance | 表示产生日志的节点的存储 IP。 | 10.200.0.114 |
  | service | 表示产生日志的服务。 | mongod |
  | severity | 表示日志的级别。 | info |
- **识别字段**

  Loki 将日志内容统一以 JSON 格式进行存储，不同服务的日志可能会解析出不同的字段，包括但不限于：

  | 字段 | 说明 | 示例 |
  | --- | --- | --- |
  | file | 采集的日志文件路径。 | "/var/log/mongodb/mongod.log" |
  | log\_timestamp | 表示从日志中解析的时间戳。 | "2023-06-25T07:23:51.850Z" |
  | message | 原始日志内容。若原始日志为 JSON 格式，在解析后原始的 JSON 日志会保留在本字段中，形成一个嵌套的 JSON 结构。 | {"attr":{"connectionCount":276,​"connectionId":5387,"remote":​"10.200.0.113:36378",​"uuid":"ff0dc285-a436-4ce6-8bc2-adecbffa70dc"},​"c":"NETWORK","ctx":"conn5387",​"id":22944,"msg":"Connection ended",​"s":"I","t":​{"$date":"2023-06-25T15:23:51​.850+08:00"}} |
  | source\_type | 日志源。file 表示日志来源是节点的日志文件，internal 表示日志来源是 Vector 内部日志。 | "file" |

在日志存储时，timestamp 使用了采集时间戳，而日志的实际时间被记录到了 log\_timestamp 字段，原因如下：

1. Loki 对于写入的数据有时间上的要求，不像 VictoriaMetrics 可以写入任意时间点的时序数据，Loki 在内存中维护了一个时间窗口（在我们的设置中这个时间窗口为 1h，即当前时间的前后 30m，若超出这个时间窗口，将写入失败），所以当网络异常一段时间并恢复后，产生的日志重传可能导致日志时间掉出这个时间窗口，从而导致日志写入失败。
2. 并非所有的日志时间戳都精确到纳秒，若日志内容中只记录了秒级的时间戳，则可能多行日志解析出来的时间戳都是在同一秒，在查询时，若时间戳相同，日志时间排序将会失效（无法从查询结果上看出日志的先后顺序），而 Vector 生成的默认的采集时间戳是精确到纳秒的。

---

## 功能实现 > 日志管理 > 日志查询

# 日志查询

可观测性服务的日志查询页面入口在 CloudTower 集群管理界面的**全部** > **日志**，由于日志是以结构化日志的形式存在 Loki 中的，所以查询时需要指定上面提到的 Log Stream labels 之一（cluster\_uuid, \_tenant\_id, instance, service, severity），目前进入 CloudTower 的日志查询页面，会固定 cluster\_uuid 这个标签。用户可以在 CloudTower 界面通过标签和关键词对日志进行过滤和查询。用户的查询请求会通过 CloudTower 转发到可观测性虚拟机中的 Grafana，再由 Grafana 转发到 Loki。

---

## 功能实现 > 日志管理 > 日志传输

# 日志传输

用户可以使用日志传输功能，将集群的日志实时导入到 Syslog 服务器中进行进一步分析。

当用户通过 CloudTower 管理界面配置了 Syslog 服务器后，可观测性虚拟机的 Configcenter 将下发导出配置到集群的 Agent 中的 Vector 组件上，在收到导出配置生效后，Vector 会将简单处理后的日志直接发送至已配置好的 Syslog 服务器中。在此过程中，日志无需被二次采集，也不会影响日志被发送至可观测性虚拟机进行正常的处理、存储和查询。

需要注意的是，如果可观测性虚拟机不可用，日志也会终止传输至 Syslog 服务器。如果 Syslog 服务器不可用，Vector 会缓存 500 条日志，并在缓存满后丢弃后续日志。

Syslog 服务器接收到的日志格式为 JSON 格式，字段信息如下：

| 字段 | 说明 | 示例 |
| --- | --- | --- |
| file | 采集的日志文件路径。 | "/var/log/mongodb/mongod.log" |
| log\_timestamp | 从日志中解析的时间戳。 | "2023-06-25T07:23:51.850Z" |
| message | 原始日志内容。若原始日志为 JSON 格式，在解析后原始的 JSON 日志会保留在本字段中，形成一个嵌套的 JSON 结构。 | {"attr":{"connectionCount":276,​"connectionId":5387,"remote":​"10.200.0.113:36378","uuid":​"ff0dc285-a436-4ce6-8bc2-adecbffa70dc"},"c":"NETWORK",​"ctx":"conn5387","id":22944,​"msg":"Connection ended","s":"I","t":​{"$date":"2023-06-25T15:23:​51.850+08:00"}} |
| source\_type | 日志源。 | "file" |
| cluster\_uuid | 表示产生日志的集群。 | d73d1a37-6e4b-4238-acd0-64ca8f496af8 |

---

## 可观测性平台与集群监控系统

# 可观测性平台与集群监控系统

可观测性平台是在 CloudTower 层面针对多个集群与系统服务而提出的可观测性功能。为保证集群报警的可靠性，可观测性平台与集群的监控系统不是替换关系，而是增强、扩展关系，具体如下：

- 集群的本地监控系统采集指标并产生报警，该功能不会因为关联可观测性服务而改变。

  本地监控数据采集路径如图中绿色路径所示，在集群中，本地监控会在每个节点上启动 Prometheus 时序数据库，但仅在 Octopus leader 节点启动采集器 Vmagent，由该 Vmagent 采集所有节点的 Exporter 指标数据，并向所有节点的 Prometheus 发送采集到的数据。
- 可观测性服务的指标采集通路与集群的本地监控系统指标采集通路互不影响。

  可观测性服务的数据采集路径如图中蓝色路径所示，若集群关联了可观测性服务，可观测性服务将为每个节点下发 Vmagent 容器，与本地监控不同的是，可观测性服务的 Vmagent 采集器仅会采集当前节点的 exporter 指标数据，并通过 Vector 数据管道发送至可观测性服务虚拟机，最终存储至 VictoriaMetrics 时序数据库。
- 集群的高级监控将被被替换，其能力迁移至可观测性服务，且可观测性服务提供了迁移高级监控数据的功能。

  若集群关联至可观测性服务，则可以在 CloudTower 上选择将高级监控的数据迁移至可观测性服务，或直接卸载高级监控。在迁移完成后，高级监控也将被自动卸载。
- 可观测性服务的报警规则与集群的本地监控系统报警规则没有交集。
- 集群关联至可观测性服务后，集群本地监控系统产生的报警将转发至可观测性服务。

  报警会由 Siren 服务转发至可观测性服务虚拟机，若转发请求失败持续 6 分钟，则 Siren 会直接将报警发出。
- 在查询指标时，如图中红色路径所示：

  - 若集群关联了可观测性服务，则直接将查询请求转发至对应的可观测性服务虚拟机上。
  - 若集群未关联可观测性服务，则将查询请求发送至集群纳管至 CloudTower 时填写的 IP，若该 IP 对应的节点不是 Octopus Leader 节点，则会将查询请求转发至 Octopus Leader。

![](https://cdn.smartx.com/internal-docs/assets/0c1d230d/wp12.png)

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
