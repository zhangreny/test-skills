---
title: "SMTXOS/6.3.0/SMTX OS 内部服务说明"
source_url: "https://internal-docs.smartx.com/smtxos/6.3.0/service-list/preface_generic"
sections: 6
---

# SMTXOS/6.3.0/SMTX OS 内部服务说明
## 关于本文档

# 关于本文档

本文档介绍了 SMTX OS 的内部服务的功能、适用的虚拟化平台和部署的节点，以及服务占用的端口和服务失效的影响。

---

## 文档更新信息

# 文档更新信息

**2026-02-04：配合 SMTX OS 6.3.0 正式发布**

相较于 SMTX OS 6.2.0，本版本更新如下：

- 新增 `zbx-chunkd` 相关端口。
- 更新 `SSH`、`SCP` 的默认端口为 22，并支持自定义修改。
- 新增 `consul-exporter` 服务。

---

## 服务功能描述

# 服务功能描述

内部服务是指保证 SMTX OS（读作 SmartX OS）的存储、计算和运维功能正常运行所需要的服务。系统既包括 SmartX 独立开发的服务，也包含所依赖的第三方服务。

下表介绍了 SMTX OS 内部服务的功能、使用的虚拟化平台和部署的节点。

## 块存储相关服务

| **服务名** | **适用虚拟化平台** | **部署节点** | **功能** |
| --- | --- | --- | --- |
| zbs-metad | ELF  VMware ESXi | 主节点  双活集群的仲裁节点 | - 提供 ZBS 存储元数据服务。 - 管理 ZBS，包括添加、删除、监控数据服务器；恢复和迁移数据。 |
| zbs-chunkd | ELF  VMware ESXi | 主节点  存储节点 | 提供 ZBS 存储数据服务。 |
| zbs-taskd | ELF  VMware ESXi | 主节点  存储节点 | 调度和执行长时间运行任务，包括：  - 跨存储池移动存储对象。 - 跨站点移动存储对象。 |
| vipservice | ELF  VMware ESXi | 主节点  存储节点 | 提供 VIP 服务。 |
| zbs-iscsi-redirectord | ELF  VMware ESXi | 主节点  存储节点 | 提供 iSCSI HA 服务。 |
| zbs-aurora-monitord | ELF  VMware ESXi | 主节点  存储节点 | 在 boost 模式下监控 zbs-chunkd，并当 zbs-chunkd 异常时启动 zbs-aurorad。 |
| zbs-inspectord | ELF  VMware ESXi | 主节点  存储节点 | 提供周期性执行数据巡检的功能。 |
| zbs-aurorad | ELF | 主节点  存储节点 | 提供 vhost 的 IO 重定向功能。 |
| timemachine | ELF  VMware ESXi | 主节点  存储节点 | 提供定时快照的功能。 |
| zbs-watchdogd | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 提供 HTTP 接口，返回 Chunk 上操作系统是否卡住的结果。 |

## 虚拟机相关服务

| **服务名** | **适用虚拟化平台** | **部署节点** | **功能** |
| --- | --- | --- | --- |
| job-center-worker | ELF  VMware ESXi | 主节点  计算节点 | 负责执行异步任务。 |
| job-center-scheduler | ELF  VMware ESXi | 主节点 | 负责发起定时任务。 |
| elf-vm-monitor | ELF | 主节点  存储节点 | 该服务是虚拟机 HA 的基础进程，提供 HA 心跳更新、节点文件系统只读检查、业务网络故障检查、触发 HA 等功能。 |
| elf-vm-scheduler | ELF | 主节点 | 负责虚拟机自动调度。 |
| master-monitor | ELF  VMware ESXi | 双活集群的仲裁节点 | 监控双活集群中 MongoDB 状态，确保 MongoDB 和 Meta Leder 在一个节点上。 |
| elf-dhcp | ELF | 主节点 | 提供 DHCP 配置功能。 |
| elf-exporter | ELF | 主节点  存储节点 | 采集监控数据。 |
| vnc-proxy | ELF | 主节点  存储节点 | 提供 Web VNC 控制台服务。 |
| vmtools-agent | ELF  VMware ESXi | 主节点  存储节点 | 收集虚拟机中运行的 guest agent 汇报的静态信息和性能参数，并将用户需要虚拟机执行的指令发送给虚拟机。 |
| elf-fs | ELF | 主节点  存储节点 | 用于存储和管理 OVF 导入过程中用户上传的文件以及 OVF 的导出结果。 |

## 运维相关服务

| **服务名** | **适用虚拟化平台** | **部署节点** | **功能** |
| --- | --- | --- | --- |
| zbs-rest-server | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | - 提供计算资源、硬件资源、存储资源管理的 REST API。 - 将性能数据存入 API。 |
| zbs-deploy-server | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | - 提供部署服务。 - 提供运维服务：添加主机、修改管理 IP。 - 提供部署环境配置信息的 API。 |
| cluster-upgrader | ELF  VMware ESXi | 主节点  存储节点 | 提供一键升级集群功能。 |
| tuna-rest-server | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 提供集群软、硬件管理 RESTful API。 |
| usbredir-manager | ELF | 主节点  存储节点 | 管理 usbredirserver 进程，以使本节点的 USB 设备可以被其他节点的虚拟机访问。 |
| ntpm | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 提供主机时间同步的功能。 |

## 监控和微服务平台相关服务

| **服务名** | **适用虚拟化平台** | **部署节点** | **功能** |
| --- | --- | --- | --- |
| octopus | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | - 从 exporter 中采集数据 - 将采集的数据通过 API 提供给外部查询 - 报警检查，并将报警信息发送到 siren。 |
| oscar | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 管理监控可视化服务的视图和图表。 |
| siren | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 接收从 octopus 发来的报警条目，并根据邮件和 SNMP 配置将报警进一步通知出去。 |
| aquarium | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 提供各服务的注册信息。 |
| harbor | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 该服务把主机请求的 RESTful API 转化为 GRPC 返回给主机。 |
| crab | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 提供用户认证授权功能。 |
| dolphin | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 提供应用管理服务，目前仅管理高级监控应用。 |
| seal | ELF  VMware ESXi | 主节点 | 提供事件审计服务。 |
| fluent-bit | ELF  VMware ESXi | 主节点  存储节点 | 收集当前节点的审计日志并发给事件中心。 |
| snmpd | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | - 提供 SNMP 数据查询服务。 - 支持通过 SNMP 协议暴露集群监控数据。 |
| network-monitor | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 提供网络监控服务。 |
| disk-healthd | ELF  VMware ESXi | 主节点  存储节点 | 监控磁盘健康状态。 |
| sd-offline | ELF  VMware ESXi | 主节点  存储节点 | 自动下线导致 HBA 卡阻塞的盘。 |
| tuna-exporter | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 采集监控数据。 |
| svcresctld | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | - 采集节点中 cgroup、服务、进程等不同粒度的监控数据。 - 提供集群服务状态信息接口。 |
| netreactor | ELF  VMware ESXi | 主节点 | 对节点的存储网络进行亚健康检测和隔离。 |
| l2ping@storage | ELF  VMware ESXi | 主节点  存储节点 | 对节点的存储网卡进行网络亚健康检测和隔离。当集群部署在 VMware ESXi 平台上时，该服务仅在集群已启用 RDMA 的前提下启动。 |
| l2ping@access | ELF | 主节点  存储节点 | 对节点的接入网卡进行网络亚健康检测和隔离。该服务仅在集群存在接入网络时启动。 |
| vmagent | ELF  VMware ESXi | 主节点，仅在一个主节点部署。 | 采集监控指标。 |
| vmagent-prod（可观测性） | ELF | 主节点  存储节点 | 采集监控指标，并将监控指标发送到 vector。 |
| vector（可观测性） | ELF | 主节点  存储节点 | 接收监控指标，采集日志，并将监控指标和日志发送到可观测性服务虚拟机。 |
| consul-exporter | ELF  VMware ESXi | 主节点  存储节点 | 提供 consul-server 的状态指标。 |
| node-exporter | ELF  VMware ESXi | 主节点  存储节点 | 提供主机硬件和操作系统相关指标。 |
| net-health-check | ELF | 主节点  存储节点 | 提供网口健康检查功能。 |

## 第三方服务

| **服务名** | **适用虚拟化平台** | **部署节点** | **功能** |
| --- | --- | --- | --- |
| mongod | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 提供以下服务：  - 存储告警信息。 - 存储虚拟机服务数据库。 - 存储用户数据。 - 存储异步任务。 - 存储注册中心数据。 - 存储多集群的关联信息。 - 存储应用中心的数据。 |
| nginx | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 提供 API 反向代理和 Web 控制台服务。 |
| chronyd | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 提供主机时间同步的功能。 |
| zookeeper | ELF  VMware ESXi | 主节点、双活集群的仲裁节点 | 提供分布式一致性协议。 |
| envoy | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | - 提供 nginx 反向代理。 - 提供跨集群的反向代理。 - 集群应用负载均衡。 |
| envoy-xds | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 提供集群内服务之间的网络功能。 |
| libvirtd | ELF | 主节点  存储节点 | 控制虚拟机生命周期。 |
| prometheus | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 采集监控数据。 |
| consul | ELF  VMware ESXi | 主节点  存储节点  双活集群的仲裁节点 | 提供注册和发现集群内服务的功能。 |
| consul-server | ELF  VMware ESXi | 主节点、双活集群的仲裁节点 | 提供注册和发现集群内服务的功能。 |
| containerd | ELF | 主节点  存储节点 | 提供主机容器管理能力 |
| everoute-agent | ELF | 关联了网络与安全功能的 VDS 的物理网口所在节点 | 为网络与安全功能在 SMTX OS 节点上提供本地代理，主要负责学习所在节点虚拟机的 IP 地址和下发网络安全规则。  **说明**：everoute-agent 服务只有在节点的 VDS 关联了网络与安全功能后才会出现和生效。 |
| everoute-collector | ELF | 关联了可观测性服务并已启用网络流量可视化功能的集群中的节点 | 采集节点流量数据，获取并关联 everoute 策略信息，并上报给可视化分析器。 |
| rpcbind | ELF  VMware ESXi | 存储节点 | ZBS NFS 服务器向 rpcbind 服务注册监听端口和该服务器所服务的 rpc program。 |
| network-firewall | ELF | 主节点  存储节点 | 提供主机防火墙功能。 |

---

## 服务占用端口

# 服务占用端口

为了保证 SMTX OS 的服务或功能正常使用，用户必须要确保以下 TCP 或 UDP 端口处于可用或者开放状态，并注意：

- 当一个服务使用多个端口时，请确保每个端口随时可被此服务使用。
- 当一个服务只使用某一个端口时，请确保此端口不被其他服务占用。

## 服务占用的固定端口

| 服务名 | 使用端口 |
| --- | --- |
| zbs-metad | 10100～10104 |
| zbs-chunkd | 10200～10203、10206～10207、3261、4420、8009（当节点上配置了多个物理盘池时，该服务还会使用 12201、14201、16201）  开启 RDMA 时使用端口：11201（当节点上配置了多个物理盘池时，该服务还会使用 13201、15201、17201）  集成 VMware ESXi 平台时使用的端口：20048、2049、111 |
| zbs-taskd | 10600、10601 |
| vipservice | 8777（本地） |
| zbs-iscsi-redirectord | 3260 |
| zbs-aurorad | 无 |
| zbs-aurora-monitord | 无 |
| zbs-inspectord | 10700、10701 |
| timemachine | 9912、32768～52768 |
| zbs-watchdogd | 10300 |
| ntpm | 10414 |
| job-center-worker | 无 |
| job-center-scheduler | 无 |
| zbs-rest-server | 10402 |
| zbs-deploy-server | 10403 |
| elf-vm-monitor | 10416 |
| elf-vm-scheduler | 10443 |
| master-monitor | 无 |
| elf-dhcp | 6767 |
| tuna-exporter | 10404 |
| log-collector | 10406 |
| elf-exporter | 10405 |
| vmtools-agent | 10809 |
| vnc-proxy (elf) | 8000（本地）、 5900～5999（本地，虚拟机可能用到的） |
| cluster-upgrader | 8090（仅升级期间 ISO 镜像 repo 使用） |
| turbot | 10409 |
| network-monitor | 10410 |
| disk-healthd | 10415，10480（UDP 端口） |
| sd-offline | 10480、10490（UDP 端口） |
| octopus | 9900 |
| oscar | 无 |
| siren | 9903 |
| aquarium | 无 |
| harbor | 9980、 20801、 20802、 20803 |
| crab | 9999 |
| dolphin | 9909 |
| envoy | 10000（containerd proxy 端口）、10900、10901、10902 |
| consul | 8301 |
| consul-server | 8300、8311(TCP & UDP)、8510 |
| seal | 9923、 9924 |
| snmpd | 1705、161（UDP） |
| mongod | 27017 |
| nginx | 80、443、8500（consul proxy 端口）、9100（node-exporter proxy 端口）、9091（prometheus proxy 端口） |
| chronyd | 123、323（UDP） |
| zookeeper | 2181、2888、3888 |
| libvirtd | 16509、16514 |
| prometheus | 9090 |
| SSH、SCP | 22（默认端口，可自定义修改） |
| rpcbind | 111 |
| containerd | 10000 |
| everoute-agent | 30002 |
| everoute-collector | 无 |
| tuna-rest-server | 10411 |
| elf-fs | 28080 |
| svcresctld | 10413 |
| usbredir-manager | 7999（本地）、 7000～7015（虚拟机跨节点访问 USB 设备时使用） |
| netreactor | 9914 |
| l2ping@storage | 9915 |
| l2ping@access | 9916 |
| vmagent | 8429 |
| vmagent-prod（可观测性） | 8430（仅在关联可观测性服务后使用） |
| vector（可观测性） | 8686（仅在关联可观测性服务后使用） |
| node-exporter | 9100 |
| net-health-check | 12889 |
| network-firewall | 12888 |

## 随机端口说明

在实际场景中，NFS 服务和客户端本地也可能使用一些随机端口，具体说明如下：

- NFS 服务除了使用 `2049` 和 `111` 两个固定端口外，还会启动其他进程（如 status、nlockmgr 等），这些进程的端口由 RPC 服务进行随机分配，每次启动 NFS 服务时使用的端口均不相同。

  若需查看 NFS 当前使用的所有端口，或查看某一未知的端口对应的进程，可采用如下方法：

  - 查看 NFS 当前使用的随机端口：在主机执行 `rpcinfo -p` 命令查看。
  - 查看某一端口对应的服务进程：在主机执行 `netstat -nlp` 命令查看。
- 客户端本地也可能启用一些随机端口对接集群服务。若扫描到此类未知的本地端口，可在主机执行 `netstat -nlp` 命令，查看该端口对应的源端口或目的端口，并根据 SMTX OS 服务使用的固定端口，确定本地端口对应的集群服务。

---

## 服务失效影响

# 服务失效影响

## 块存储相关服务

| **服务名** | **在单节点失效影响** | **整体失效影响** |
| --- | --- | --- |
| zbs-metad | - 在 Leader 节点失效：存储服务短暂性不可访问（约 40s）。 - 在 Follower 节点失效：无影响。 | 条件：少于半数 meta 节点存活  - 集群存储不可用。 - 所有虚拟机 I/O 超时。 - SMTX 虚拟机服务和存储服务相关操作不可用。 |
| zbs-chunkd | - 失效节点的数据无法访问。 - 触发数据恢复。 - 虚拟机 I/O 短暂性卡顿。 - 本地 Hypervisor 上的磁盘存储服务将转由远端提供，可能出现短暂卡顿。 | 条件：全部失效   - 存储不可用，IO 中断。 |
| zbs-taskd | 失效节点无法执行长时运行任务 | 条件：全部失效   - 集群失去长时任务调度及运行能力。 |
| vipservice | 失效节点无法承载 VIP | 条件：全部失效   - VIP 服务不可用。 |
| zbs-iscsi-redirectord | - 失效节点无法建立新的 iSCSI 连接。 - 失效节点已经建立的 iSCSI 连接不受影响。 | 条件：全部失效   - 集群无法建立新的 iSCSI 连接。 - 集群已经建立的 iSCSI 连接不受影响。 |
| zbs-aurora-monitord | 失效节点中 vhost 模式的虚拟机 HA 功能失效，从而导致虚拟机在存储故障时无法读写。 | 条件：全部失效  - vhost 模式的虚拟机无法启动。 - 已经启动的虚拟机无法读写。 |
| zbs-inspectord | 失效节点无法进行数据巡检 | 条件：全部失效 集群失去数据巡检能力。 |
| zbs-aurorad | 失效节点中 vhost 模式的虚拟机 HA 功能失效，从而导致虚拟机在存储故障时无法读写。 | 条件：所有节点的 zbs-chunkd 服务和 zbs-aurorad 服务失效。 集群不可用，IO 中断。 |
| timemachine | 只有 Meta Leader 所在节点的 timemachine 可以对外提供服务，该节点 timemachine 失效后集群无法提供定时快照的服务，其余节点失效无影响。 | 条件：全部失效   - 定时快照功能失效。 |
| zbs-watchdogd | 若 Zookeeper leader 节点上的 zbs-watchdogd 服务异常，则当节点的操作系统异常时，Zookeeper 服务可能无法快速重新选举。 | - |

## 虚拟机相关服务

| **服务名** | **在单节点失效影响** | **整体失效影响** |
| --- | --- | --- |
| timemachine | 只有 Leader 所在节点的 timemachine 可以对外提供服务，该节点 timemachine 失效后集群无法提供定时快照服务，其余节点失效无影响。 | 条件：全部失效   - 定时快照功能失效。 - 跨站点备份/回滚/克隆服务失效。 |
| job-center-worker | - 无法对失效节点上的虚拟机进行管理操作。 - 无法对失效节点进行修改，如修改管理IP、修改该节点 VDS 和对该节点进行插拔盘操作。 - 无法将失效节点的系统资源和服务信息更新到数据库。 - 无法将失效节点的虚拟机运行状态更新到数据库。 | - |
| job-center-scheduler | 无影响 | 条件：全部失效   - 虚拟机管理不可用。 - 监控报警失效。 |
| elf-vm-monitor | 失效节点上的虚拟机无法触发 HA。 | 条件：少于 2 个 有效   - 集群虚拟机 HA 功能失效。 |
| elf-vm-scheduler | - 如果是 Meta Leader 节点上的此服务失效，则虚拟机自动调度功能失效。 - 如果是非 Meta Leader 节点上此服务失效，无影响。 | - |
| master-monitor | 当优先可用域和次级可用域名之间网络失联时，有可能导致 REST API 不可用。 | - |
| elf-dhcp | - 如果是 Meta Leader 节点上的此服务失效，则虚拟机网络DHCP配置功能失效。 - 如果是非 Meta Leader 节点上此服务失效，无影响。 | 条件：在 Leader 节点上失效 无法为虚拟机网络提供 DHCP 配置功能。 |
| elf-exporter | 失效期间，失效节点的监控数据无法获取。 | 条件：全部失效 集群监控整体失效。 |
| vnc-proxy | 失效节点无法提供 VNC Web 控制台服务。 | - |
| vmtools-agent | - 无法实时汇报该主机上运行的虚拟机的静态信息及性能数据。 - 无法配置该节点上虚拟机的 IP、DNS 等网络信息。 | 条件：全部失效   - 无法通过虚拟机工具实时获取集群所有虚拟机静态数据及性能数据。 - 无法配置集群中所有虚拟机的 IP、DNS 等网络信息。 |
| elf-fs | 不影响失效节点和整个集群的虚拟机导入导出功能。失效节点无法响应虚拟机导入导出请求，CloudTower 将向其他正常节点发出请求。 | 条件：全部失效 集群的 OVF 导入导出功能无法使用。 |

## 运维相关服务

| **服务名** | **在单节点失效影响** | **整体失效影响** |
| --- | --- | --- |
| zbs-rest-server | - 失效节点的 API 无法访问。 - 失效期间，失效节点的性能数据无法存储。 | - |
| zbs-deploy-server | 无法添加主机。 | - |
| cluster-upgrader | - | 条件：全部失效   - 无法执行一键升级。 - 无法展示历史升级记录。 |
| tuna-rest-server | 失效节点硬件信息 API 无法访问。 | - |
| usbredir-manager | 虚拟机无法访问失效节点的 USB 设备。 | - |
| ntpm | 失效节点无法执行修改 NTP 配置。 | 条件：全部失效   - 集群无法提供 NTP HA 服务。 - 集群可能出现节点时钟不同步导致存储系统不可用。 |

## 监控和微服务平台服务

| **服务名** | **在单节点失效影响** | **整体失效影响** |
| --- | --- | --- |
| octopus | 该节点上的 Octopus API 不可用，无法通过此节点查询监控数据。 | 条件：全部失效   - 不产生新的监控数据。 - 不产生新的报警。 - 监控数据查询失败。 |
| oscar | 该节点上的 oscar 服务不可用。 | 条件：全部失效 所有 oscar 服务不可用。 |
| siren | - 在 Meta Leader 上失效：   - 无法接收从 octopus 发来的报警信息。   - 已经实际解决的报警无法显示为解决。   - 无法标记报警已解决。 - 在其他节点失效：该节点上的 siren API 不可用。 | 条件：在 Leader 节点上失效   - 不发送新的报警通知邮件。 - 报警信息查询失效。 - 无法标记报警已解决。 |
| aquarium | 该节点上的 aquarium 服务不可用，该节点的虚拟机无法访问 aquarium 服务。 | 条件：全部失效   - 无法提供注册信息。 |
| harbor | 该节点上的所有 v3 API 不可用。 | 条件：全部失效   - 无法提供 v3 API。 |
| crab | 该节点对应的大部分 API 无法使用。 | 条件：全部失效   - 该集群的大部分 API 无法使用。 |
| dolphin | - 在 Meta Leader 节点上失效：无法部署或停用高级监控。 - 在其他节点失效：该节点上的 dolphin API 不可用。 | 条件：在 Leader 节点上失效   - 无法部署或停用高级监控。 - dolphin API 不可用。 |
| seal | 无影响 | 条件：全部失效   - 事件审计不可用。 |
| fluent-bit | 当前节点的审计日志不会被收集。 | 条件：全部失效   - 集群所有失效节点的审计日志不会被收集。 |
| snmpd | 失效节点无法通过 SNMP 获取数据。 | 条件：全部失效 所有节点无法通过 SNMP 获取数据。 |
| network-monitor | 无法获取当前节点网络监控数据。 | 条件：全部失效   - 无法获取网络监控数据。 |
| disk-healthd | - 失效节点的磁盘健康状态无法更新。 - 失效节点无法触发新的磁盘健康状态告警。 - 失效节点已经触发的磁盘健康告警可能与磁盘当前健康状态不符。 | - |
| sd-offline | 当存在某个盘导致 HBA 卡阻塞时，该盘可能无法自动下线。 | - |
| consul-exporter | 失效节点无法获取 consul-server 的状态监控数据。 | 条件：全部失效 consul-server 的状态监控整体失效。 |
| tuna-exporter | 失效期间，失效节点的监控数据无法获取。 | 条件：全部失效 集群监控整体失效。 |
| svcresctld | - 失效节点的服务状态异常和资源使用异常的监控告警失效。 - 失效节点的服务状态信息无法获取。 | - 集群整体的服务状态异常和资源使用异常监控告警失效。 - 集群整体的服务状态信息无法获取。 |
| netreactor | - 在 Meta Leader 上失效：集群无法提供针对节点的网络亚健康检测和隔离服务。 - 在其他节点失效：无影响 | 条件：在 leader 上失效  集群无法提供针对节点的网络亚健康检测和隔离服务。 |
| l2ping@storage | 条件：全部失效 该节点无法对自身存储网卡进行网络亚健康检测和隔离。 | 所有节点无法对自身存储网卡进行网络亚健康检测和隔离。 |
| l2ping@access | 该节点无法对自身接入网卡进行网络亚健康检测和隔离。 | 条件：全部失效 所有节点无法对自身接入网卡进行网络亚健康检测和隔离。 |
| vmagent | 无法采集监控指标数据。 | - |
| vmagent-prod（可观测性） | 无法采集监控指标数据。 | 条件：全部失效 所有节点无法采集监控指标数据。 |
| vector（可观测性） | 该节点无法接收监控指标、无法采集日志，且无法将监控指标和日志发送给可观测性服务虚拟机。 | 条件：全部失效 所有节点无法接收监控指标数据、无法采集日志，且无法将数据发送给可观测性服务虚拟机。 |
| net-health-check | 该节点无法检查网口健康，可能影响其他节点检查结果。 | - |

## 第三方服务

| **服务名** | **在单节点失效影响** | **整体失效影响** |
| --- | --- | --- |
| mongod | 无影响 | 条件：半数及以上失效   - 所有服务的 API 都无法工作。 - Job Center 无法工作。 |
| nginx | 失效节点的 API 和 Web 控制台无法使用。 | - |
| chronyd | - 影响失效节点和其他节点的时钟同步，积累形成时钟差异。 - 时钟差异会导致：    - 部分 I/O 延迟升高。   - 虚拟机 HA 功能出现误判，导致虚拟机意料外的关机。 | - |
| zookeeper | 无影响 | 条件：在超过半数的节点上服务失效   - 集群所有节点的存储无法访问。 - 虚拟机操作大部分不可用。 - 所有虚拟机 I/O 超时。 |
| envoy | - 失效节点的 API 无法使用。 - 失效节点无法进行 ZBS 异步备份。 | - |
| envoy-xds | 失效节点上的 API 无法正常使用。 | 条件：全部失效   - 所有 API 无法正常使用。 |
| consul | 失效节点上的 API 无法正常使用。 | 条件：全部失效   - 所有 API 无法正常使用。 |
| consul-server | 无影响 | 条件：半数及以上失效   - 所有 API 无法正常使用。 |
| libvirtd | 无法控制失效节点上的虚拟机生命周期。 | - |
| prometheus | - Meta Leader 上失效：所有监控服务不可用。 - 其他失效：正常情况 | 条件：Meta Leader 失效且无新的 Meta Leader 产生。   - 不产生新的监控数据。 - 不产生新的报警。 - 监控数据查询失败。 |
| containerd | 失效节点的容器无法被管理。 | - |
| everoute-agent | - 失效节点无法下发新的网络安全规则。 - 失效节点无法获取虚拟机的 IP 地址。 | - |
| everoute-collector | 失效节点流量信息丢失。 | 条件：全部失效 集群流量信息丢失。 |
| rpcbind | 失效节点上使用 rpcbind 的服务无法接收 I/O。 | 条件：全部失效 集群中使用 rpcbind 的服务无法接收 I/O。 |
| network-firewall | 失效节点无法修改防火墙，可能导致该节点和集群设置不同步。 | - |

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
