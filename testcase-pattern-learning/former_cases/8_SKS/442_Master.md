SKS1.1
    ecp cni网卡配置优化
        ecp cni网卡配置优化-创建集群，设置子网cidr与service cidr重叠，子网cidr输入框提示“子网 CIDR 与 Service IP CIDR 重叠。”
        ecp cni网卡配置优化-子网cidr为空，子网cidr输入框提示“请填写子网 CIDR。”
        ecp cni网卡配置优化-子网cidr格式不正确，子网cidr输入框提示“请填写正确格式的 CIDR。”
        ecp cni网卡配置优化-网关格式不正确，网关输入框提示“请填写正确格式的 网关。”
        ecp cni网卡配置优化-pod cidr格式不正确，输入框提示“请填写正确格式的 Pod IP CIDR。”
        ecp cni网卡配置优化-pod cidr为空，输入框提示“请填写 Pod IP CIDR。”
        ecp cni网卡配置优化-网关为空，网关输入框提示“请填写网关。”
SKS1.2
    SKS支持GPU
        SKS 支持 NVIDIA GPU 驱动预编译  --- TBD
            集群配置GPU - 插件设置页面手动关闭gpu-operator插件，驱动卸载失败，检查VM会残留挂载点，再重新打开，不会产生多个/run/nvidia/driver 相关目录的挂载点
        已有功能影响
            监控 - 新增图表
                Kubernetes/Compute Resource/GPU - GPU Energy Draw Total（Last 1h）
                Kubernetes/Compute Resource/GPU - GPU Energy Draw Total（Last 24h）
        场景测试
            GPU卡用尽 - 集群2张GPU卡，集群1+1（worker节点配置2张GPU卡）- 编辑节点组节点数量和GPU数量（2worker每个worker1张GPU卡）- 先创建新节点，GPU卡数量不足，failed
            GPU卡充足 - 集群3张GPU卡，集群1+1（worker节点配置2张GPU卡）- 编辑节点组节点数量和GPU数量（2worker每个worker1张GPU卡）- 先创建新节点，集群滚动更新成功
独立ELF CSI
    Kubernetes Node 名称和所在的虚拟机名称不一致 - 部署elf-csi前 - 修改虚拟机名称 - elf-csi不能正常使用,node-plugin pod无法启动
    裸k8s集群
        安装部署 -部署方式（离线部署）
            SKS集群 - Kubernetes版本升级 - v1.25.x升级到v1.26.x - 升级成功，elf-csi正常使用
            私有镜像仓库场景
                通过命令把配置的私有容器镜像仓库地址写入csi-driver.yaml文件
        支持配置参数
            安装部署时修改
                修改csi-driver.yaml后部署 - storageClass.parameters.storagePolicy - 双活集群，有缺省值：REPLICA_2_THIN_PROVISION - 部署成功，pv创建报错
                修改csi-driver.yaml后部署 - storageClass.parameters.storagePolicy - 为空，有缺省值：REPLICA_2_THIN_PROVISION
                修改csi-driver.yaml后部署 - storageClass.parameters.elfCluster - 设置为空 - 创建成功，创建pvc使用时pv有报错
                修改csi-driver.yaml后部署 - driver.defaultStoragePolicy - 单活 - 配置为空，default的sc 的 storagePolicy 默认为 2 副本精简 - 部署失败，controller pod无法正常启动
                修改csi-driver.yaml后部署 - driver.defaultStoragePolicy - 双活 - 配置为空，default的sc 的 storagePolicy 默认为 2 副本精简 - 部署失败，csi controller pod无法正常启动
                修改csi-driver.yaml后部署 - driver.defaultStoragePolicy - 单活/双活 - 配置为支持的存储策略（2副本/3副本），default的sc.storagePolicy 配置为空， 部署成功，default的sc的storagePolicy默认与driver.defaultStoragePolicy配置的值保持一致
                修改csi-driver.yaml后部署 - driver.defaultStoragePolicy - 单活/双活 - 配置为不支持的存储策略 - 部署失败，controller pod 无法正常启动
                修改csi-driver.yaml后部署 - driver.defaultStoragePolicy - 双活 - sc未配置且driver.defaultStoragePolicy 为 2 副本 - 部署成功，无法创建 pv
                修改csi-driver.yaml后部署 - driver.defaultStoragePolicy - 双活 - sc未配置且driver.defaultStoragePolicy 为 3 副本 - 部署成功，可以创建 pv
        升级 - 离线升级  - TBD
            discard - ELF CSI 1.0.1 升级到1.1.1  ---TBD
        部署成功后验证
            存储类管理
                使用独立ELF-CSI - 创建自定义存储类 - parameters.elfCluster - 为空 - 创建成功但创建pvc失败,制备pv失败
            动态置备持久卷
                独立ELF-CSI - 创建pv - spec.resources.requests.storage - 创建大于64TiB的pvc，describe pvc 查看对应报错
                独立ELF-CSI - 创建pv - 卷挂载 - 挂载到不同os的节点 - 挂载失败报错：不在同一个 OS 集群 the VM %s is not found in Tower or not in the same cluster
 --- TBD
                独立ELF-CSI - 创建pv - 卷挂载 - 卷不存在 - 挂载失败报错：pvc不存在 persistentvolumeclaim "xxx" not found
            快照管理
                独立ELF-CSI - 异常创建快照 - 卷不存在 - error报错：failed to find volum
            卷克隆
                独立ELF-CSI - 异常克隆 - 源pv不存在 - 克隆失败有报错信息：failed to provision volume with...
                独立ELF-CSI - 异常克隆 - 源pv的访问模式与克隆的pv不一致 - 克隆失败有报错信息：the volume sharing %v must equal to..
            场景测试   --- TBD
                SKS-3744 - 独立ELF-CSI - 创建集群节点同名虚拟机，移入回收站，创建pod启动在该节点，pod启动成功
                SKS-3744 - 裸k8s集群 - 创建worker节点同名虚拟机，移入回收站后 - 部署独立elf-csi - elf csi pod 正常启动，基本功能正常可用
                SKS-3805 - 部署独立elf-csi - 创建未配置elfcluster参数的sc - 创建成功，创建pvc使用该sc - pv创建失败
                SKS - 3927 - 独立elf-csi默认部署成功后 - 检查sidecar和csi-resizer默认resources配置更新
    discard
        discard - 独立ELF-CSI - 创建pv - spec.accessModes/volumeMode - Filesystem/block - 不支持的访问模式 unknown access mode
SKS1.4
    支持集群配置原地更新
        SKS升级
            SKS升级 - 已有虚拟机工作负载集群 - 磁盘大小200G，ytt版本1.2 - 新增节点 - 扩容成功,不会触发原地更新，disckSize不写入ksc
            SKS升级 - 已有虚拟机工作负载集群 - 磁盘大小200G，ytt版本1.2升级到1.4 - 扩容磁盘大小 - 扩容成功,触发原地更新，disckSize写入ksc
        SKS1.4节点资源热更新
            CPU&内存热更新设计调整
                SKS-4116 - CPU热扩容 - 热扩容后检查cgroups cpuset.cpus同步更新
    SKS监控重构+报警+关联可观测性
        SKS关联可观测性
            obs关联交互实现逻辑
                实现变更
                    新增CRD - ObservabilitySystemService
                        new当前操作状态 - ObservabilitySystemService.status:CleanUpFailed 清理失败，在取消注册之前的任务，可检查其event查看原因
            前提条件
                状态要求
                    SKS系统服务要求
                        SKS关联 - 可观测性服务正常 - SKS系统服务（registry异常） - 关联OBS操作无法完成，异常恢复后，关联成功
                        SKS关联 - 可观测性服务正常 - SKS系统服务（管控集群就绪） - 可正常关联OBS
                        SKS关联 - 可观测性服务正常 - SKS系统服务（管控集群就绪） - 可正常关联OBS，关联失败，每2min重试一次
                        SKS关联 - 可观测性服务正常 - SKS系统服务（管控集群running） - 无法关联OBS - 入口禁用
                        SKS关联 - 可观测性服务正常 - SKS系统服务（管控集群updating） - 无法关联OBS - 关联入口禁用
                        SKS关联 - 可观测性服务正常 - SKS系统服务（管控集群upgrading） - 无法关联OBS - 关联入口禁用
                        SKS关联 - 可观测性服务正常 - SKS系统服务（管控集群暂停同步中）- 无法关联OBS - 关联入口禁用
                        SKS关联 - 可观测性服务正常 - SKS系统服务（管控集群failed） - 无法关联OBS - 关联入口禁用
            已有功能影响
                可观测性服务
                    切换obs - SKS试用许可过期 - 切换已开启监控，日志的SKS到obs -  成功切换，数据自动迁移
        SKS报警
            CloudTower新增报警规则
                预制报警规则列表 - 触发默认报警规则
                    1.5-集群 {{ $labels.cluster }} 名字空间 {{ $labels.namespace }} 中控制台控制器的组件 Deployment/sks-cloudtty-controller-manager 异常持续 15 分钟。｜注意｜无｜ SKS集群「仅管控集群」
                    集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中的 NTP 管理器组件 {{ $labels.daemonset }} 异常持续 15 分钟。
｜注意｜无｜ SKS集群
                    集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中的主机配置代理组件 {{ $labels.daemonset }} 异常持续 15 分钟。
｜注意｜无｜ SKS集群
                    集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中的项目认证代理组件 {{ $labels.daemonset }} 异常持续 15 分钟。
｜注意｜无｜ SKS集群 「仅工作负载集群」
                预制报警规则详情页
                    集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中的 NTP 管理器组件 {{ $labels.daemonset }} 异常持续 15 分钟。默认阈值：15m且不可配置
                    集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中的主机配置代理组件 {{ $labels.daemonset }} 异常持续 15 分钟。默认阈值：15m且不可配置
                    集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中的项目认证代理组件 {{ $labels.daemonset }} 异常持续 15 分钟。默认阈值：15m且不可配置 「仅工作负载集群」
    多租户 - 用户与权限
        项目管理
            项目资源管理
                角色
                    用户场景
                        从sks1.3升级sks1.4- 升级后还未更新功能版本，不会增加内置角色
        场景验证
            升级-SKS1.3升级sks1.4，升级后更新工作集群「功能版本更新」，displayname不变
    支持配置 NTP Server
        升级 SKS
            NTP - 已有手动添加的 不合法NTP 配置 - 仅对 Control plane 配置，升级到 1.4 后，工作集群可完成更新，配置合并到从 Tower 同步的全局配置
            NTP - 已有手动添加的 不合法NTP 配置 - 仅对 Worker 配置，升级到 1.4 后，工作集群可完成更新，配置合并到从 Tower 同步的全局配置
            NTP - 已有手动添加的 不合法NTP 配置 - 对 ControlPlane 和Worker 配置不同的 ntp，升级到 1.4 后，工作集群可完成更新，配置合并到从 Tower 同步的全局配置
            NTP - 已有手动添加的 不合法NTP 配置 - 对 ControlPlane 和Worker 配置和全局配置有重复的 ntp，升级到 1.4 后，工作集群可完成更新，配置合并到从 Tower 同步的全局配置可自动去重
    SKS 1.4 改进
        模板漏扫修复
            1.4改进 - 漏扫修复 - Rocky - 1.25 - 节点在集群的生命周期（创建，添加，删除）正常可完成 + 原地更新可完成
            1.4改进 - 漏扫修复 - Rocky - 1.26 - 节点在集群的生命周期（创建，添加，删除）正常可完成 + 原地更新可完成
            1.4改进 - 漏扫修复 - openeuler x86 - 1.25 - 节点在集群的生命周期（创建，添加，删除）正常可完成 + 原地更新可完成
            1.4改进 - 漏扫修复 - openeuler x86 - 1.26 - 节点在集群的生命周期（创建，添加，删除）正常可完成 + 原地更新可完成
            1.4改进 - 漏扫修复 - openeuler arm - 1.25 - 节点在集群的生命周期（创建，添加，删除）正常可完成 + 原地更新可完成
            1.4改进 - 漏扫修复 - openeuler arm - 1.26 - 节点在集群的生命周期（创建，添加，删除）正常可完成 + 原地更新可完成
        vGPU license校验
            UI - 实时校验 - 创建vGPU集群 - GPU operator配置无效的vGPU许可 - Inline提示：vGPU许可无效
            UI - 实时校验 - 创建vGPU集群后编辑 - GPU operator配置无效的vGPU许可 - Inline提示：vGPU许可无效
            UI - 实时校验 - 创建vGPU集群 - GPU operator配置已过期的vGPU许可 - Inline提示：vGPU已过期
            UI - 实时校验 - 创建vGPU集群后编辑 - GPU operator配置已过期的vGPU许可 - Inline提示：vGPU已过期
            UI - 许可配置成功后，vGPU许可即将过期 - 1-10天 - Notice Tip:vGPU许可将于x天后过期，请及时更新许可。
            UI - 许可配置成功后，vGPU许可即将过期 - 不足1天 - Notice Tip:vGPU许可有效期不足1天，请及时更新许可。
            UI - 许可配置成功后，vGPU已过期  - Notice Tip:vGPU许可已过期，请重新配置避免影响vGPU功能的使用。
            UI文案优化 - 创建集群时，选择了vGPU但是GPU Operator未配置license - 提示文案：请配置 vGPU 许可，否则将影响 vGPU 功能的使用。
            UI文案优化 - 集群创建后，选择了vGPU但是GPU Operator未配置license - 插件部分提示文案：请配置 vGPU 许可，否则将影响 vGPU 功能的使用。
            UI文案优化 - 集群创建后，选择了vGPU但是GPU Operator未配置license - 插件部分提示文案：请配置 vGPU 许可，否则将影响 vGPU 功能的使用 - 配置了有效且未过期的许可后 - 提示文案消失
            UI文案优化 - 集群创建后，选择了vGPU但是GPU Operator未配置license - 集群概览页上方提示文案：未配置 vGPU 许可，将影响 vGPU 功能的使用。- 提示后「配置vGPU许可」按钮可跳转
    Tower 一键提升副本数兼容系统服务
        [Deprecated] 需求变更—SKS 随系统提升才需检查
            提升副本 - 已存在 1.4 版本 User registry - 提升OS集群副本，User registry 副本数提升为3
            提升副本 - 已存在 1.4 SKS 服务 - 提升OS集群副本，SKS registry 副本数提升为 3
            提升副本 - 已存在 1.4 SKS 服务 - 提升OS集群副本，管控集群虚拟机虚拟卷副本数随之提升为 3
            提升副本 - 已存在 1.4 SKS 服务 - 提升OS集群副本，管控集群虚拟机挂载的 PV 对应虚拟卷的副本数随之提升为 3
            提升副本 - 已存在 1.4 SKS 集群 - 提升OS集群副本，工作集群虚拟机虚拟卷副本数随之提升为 3
            提升副本 - 已存在 1.4 SKS 集群 - 提升OS集群副本，已开启监控日志插件的工作集群虚拟机挂载的使用 ELF CSI 创建的 PV 对应虚拟卷的副本数随之提升，监控日志工作正常
            提升副本 - 已存在 1.4 SKS 集群 - 提升OS集群副本，扩容工作集群虚拟机挂载的使用 ELF CSI 创建的 PV 对应虚拟卷，可成功扩容
            提升副本 - 已存在 1.4 SKS 集群 - 提升OS集群副本，新增工作集群节点，新节点虚拟机副本数为 2 - TBD
            提升副本 - 已存在 1.4 SKS 集群 - 提升OS集群副本，新建工作集群，节点模板已存在当前集群，节点虚拟机副本数仍然为 2 （模板的副本数未提升）
            提升副本 - 已存在 1.4 SKS 集群 - 一次提升后新建节点和 pv，再次执行提升副本可成功将新节点和 PV 副本数提升到 3
            提升副本 - 已存在 1.4 SKS 集群 - 提升OS集群副本，然后开启工作集群监控/日志插件，插件可开启，ELF CSI 创建的 PV 副本数为 2 - TBD
            提升副本 - 已存在 1.4 SKS 集群 - 未提升OS集群副本，克隆使用 ELF CSI 创建的 PV，副本数为 2
            提升副本 - 已存在 1.4 SKS 集群 - 提升OS集群副本，克隆使用 ELF CSI 创建的 PV，副本数为 3
            提升副本 - 已存在 1.4 SKS 集群 - 提升OS集群副本后，使用 ELF CSI 新创建 PV，克隆 PV，副本数为 2
            提升副本 - 已存在 1.4 SKS 集群 - 未提升OS集群副本，对使用 ELF CSI 创建的 PV 创建快照并重建 PV，可成功重建，副本数为 2
            提升副本 - 已存在 1.4 SKS 集群 - 提升OS集群副本，对使用 ELF CSI 创建的 PV 创建快照并重建 PV，可成功重建，副本数为 3
            提升副本 - 已存在 1.4 SKS 集群 - 提升OS集群副本后，对使用 ELF CSI 新创建的 PV 创建快照，从快照重建 PV，可成功重建，副本数为 2
            提升副本 - 已存在 1.4 SKS 集群 - 对使用 ELF CSI 创建的 PV 创建快照，提升OS集群副本，从快照重建 PV，可成功重建，副本数为 2 - TBD
            提升副本 - 已存在 1.4 SKS 集群 - 对使用 ELF CSI 创建的 PV 创建快照，提升OS集群副本，并重建 PV，可成功重建，副本数为 3
            提升副本 - 已存在旧版 Tower 部署的 1.3或以下 版本的 User registry - 提升OS集群副本，User registry 副本数提升为 3
            提升副本 - 已存在 1.3 版本 User registry - 提升OS集群副本，User registry 副本数提升为3
            提升副本 - 已存在 1.3 SKS 服务 - 提升OS集群副本，SKS registry 副本数提升为 3
            提升副本 - 已存在 1.3 SKS 服务 - 提升OS集群副本，管控集群虚拟机虚拟卷副本数提升为 3
            提升副本 - 已存在 1.3 SKS 服务 - 提升OS集群副本，管控集群 pv 对应虚拟卷的副本数不变
            提升副本 - 已存在 1.3 SKS 集群 - 提升OS集群副本，工作集群虚拟机虚拟卷副本数提升为 3
            提升副本 - 已存在 1.3 SKS 集群 - 提升OS集群副本，工作集群 ELF CSI 创建的已挂载 pv 对应虚拟卷的副本数不变
            提升副本 - 已存在 1.3 SKS 集群 - 提升OS集群副本，工作集群ELF CSI 创建的未挂载的 pv 对应虚拟卷的副本数不变
    AKE 1.4 支持 K8s v1.30
        K8s v 1.30 验证
            支持 K8s v1.30 - autoscaler 版本更新为 1.26.8-sks.1
            支持 K8s v1.30 - releaseinfo 中 compatibleKubeVersions 增加 v1.30
            支持 K8s v1.30 - v1.30 节点文件可成功上传，上传模板标记为系统模板
            支持 K8s v1.30 - 被集群使用的 v1.30 节点文件不可删除
            支持 K8s v1.30 - 无集群使用时，v1.30 节点文件可删除
            支持 K8s v1.30 - v1.30 集群的 CP节点 /var/lib/kubelet/kubeadm-flags.env 中，无 --container-runtime=remote 配置
            支持 K8s v1.30 - v1.30 集群的 worker节点 /var/lib/kubelet/kubeadm-flags.env 中，无 --container-runtime=remote 配置
            支持 K8s v1.30 - 使用v1.30 模板创建使用Calico + ELF CSI 的虚拟机集群，可成功创建，监控报警日志可开启
            支持 K8s v1.30 - 使用v1.30 模板创建使用 ZBS CSI 的虚拟机集群，可成功创建，监控报警日志可开启
            支持 K8s v1.30 - 使用v1.30 模板创建使用 EIC CNI 的虚拟机集群，可成功创建，监控报警日志可开启
            支持 K8s v1.30 - 使用v1.30 模板创建虚拟机集群，并开启全部插件，集群可成功删除
            支持 K8s v1.30 - 使用v1.30 模板的虚拟机集群，自动伸缩节点组功能正常工作
            支持 K8s v1.30 - 使用v1.30 模板的虚拟机集群可完成原地更新 - 节点组配置可更新
            支持 K8s v1.30 - 使用v1.30 模板的虚拟机集群可完成原地更新 - K8s 配置可更新
            支持 K8s v1.30 - 使用v1.30 模板的虚拟机集群可完成原地更新 - 受信任容器镜像仓库可更新
            支持 K8s v1.30 - 使用v1.30 模板的虚拟机集群，可手动添加删除节点
            支持 K8s v1.30 - 使用v1.30 模板的虚拟机集群，故障节点自动替换功能正常工作
            支持 K8s v1.30 - 使用v1.30 模板的虚拟机集群，metallb + contour 插件开启后可正常工作
            支持 K8s v1.30 - 使用v1.30 模板的虚拟机集群，可同步 NTP Server 配置
            支持 K8s v1.30 - 使用v1.30 模板的虚拟机集群，节点信息及 K8s 版本信息正常显示
            支持 K8s v1.30 - 使用v1.30 模板的虚拟机集群，可使用集群控制台
            支持 K8s v1.30 - 使用v1.30 模板的虚拟机集群，可使用节点控制台
            支持 K8s v1.30 - 使用v1.30 模板的虚拟机集群，可使用 pod 控制台
            支持 K8s v1.30 - 使用v1.30 模板的虚拟机集群，可应用租户权限控制
        已有功能影响范围验证
            支持 K8s v1.30 - 创建 v1.24 版本集群，可成功创建，监控报警日志可开启
            支持 K8s v1.30 - 创建 v1.25 版本集群，可成功创建，监控报警日志可开启
            支持 K8s v1.30 - 创建 v1.26 版本集群，可成功创建，监控报警日志可开启
            支持 K8s v1.30 -  v1.24 版本虚拟机集群，自动伸缩节点组功能正常工作
            支持 K8s v1.30 -  v1.25 版本虚拟机集群，自动伸缩节点组功能正常工作
            支持 K8s v1.30 -  v1.26 版本虚拟机集群，自动伸缩节点组功能正常工作
            支持 K8s v1.30 -  v1.24 版本虚拟机集群可完成原地更新
            支持 K8s v1.30 -  v1.25 版本虚拟机集群可完成原地更新
            支持 K8s v1.30 -  v1.26 版本虚拟机集群可完成原地更新
            支持 K8s v1.30 - v1.24 虚拟机节点 /var/lib/kubelet/kubeadm-flags.env 中，存在 --container-runtime=remote 配置
            支持 K8s v1.30 - v1.25 虚拟机节点 /var/lib/kubelet/kubeadm-flags.env 中，存在 --container-runtime=remote 配置
            支持 K8s v1.30 - v1.26 虚拟机集群 CP 节点 /var/lib/kubelet/kubeadm-flags.env 中，无 --container-runtime=remote 配置
            支持 K8s v1.30 - v1.24 物理机节点 /var/lib/kubelet/kubeadm-flags.env 中，存在 --container-runtime=remote 配置
            支持 K8s v1.30 - v1.25 物理机节点 /var/lib/kubelet/kubeadm-flags.env 中，存在 --container-runtime=remote 配置
            支持 K8s v1.30 - v1.26 物理机集群 CP 节点 /var/lib/kubelet/kubeadm-flags.env 中，无 --container-runtime=remote 配置
            支持 K8s v1.30 - SKS 1.4 新创建的 v1.26 worker节点 /var/lib/kubelet/kubeadm-flags.env 中，无 --container-runtime=remote 配置
            支持 K8s v1.30 - 前序 SKS 版本创建的 v1.26 集群节点，在发生原地更新后 /var/lib/kubelet/kubeadm-flags.env 中，--container-runtime=remote 配置被移除
AKE1.4
    AKE - OBS - OBS 不可用时，工作集群概览页 card loading 动画不能是 tower 图案
    多租户
        关联项目 - 添加LabelProjectName 和 LabelProjectNamespace 绑定项目
        关联项目 - 同个成员根据角色，一个Namespace对应一个RoleBinding
        Namespace从非项目移入项目 - 已关联成员，创建ProjectRoleBinding对应的RoleBinding，增加label
        Namespace从项目1 移入 项目2 - 已关联成员，移除原Project的RoleBinding，创建新Project的Rolebinding，label更新
        Namespace从项目移除 - 已关联成员，移除原RoleBinding
        系统Project - 维护固定namespace-configmap
        系统Project - 定义source: system 为系统项目
        自定义Project - 定义source: custom 为自定义项目
        删除Project - 删除所属所有ProjectRoleBinding，异步删除工作集群上关联的RoleBinding，移除 ProjectFinalizer
        删除Project - 若有ProjectForceDeleteAnnotation，仅移除所有namespace
        删除Project - 若没有ProjectForceDeleteAnnotation，将删除所有namespace
        用户加入项目时， 创建ProjectRoleBinding
        一个用户对应多个ProjectRoleBinding
        删除ProjectRoleBinding - 同步删除ProjectRoleBinding， 异步删除工作集群关联的RoleBinding等资源
        用户手动创建RoleBinding，若与SKS创建的重名，则会被覆盖
        用户每下载一次Kubeconfig，生成一个ClusterToken
        每个用户在每个集群可创建多个ClusterToken
        用户自下载创建的ClusterToken - 手动下载Kubeconfig时自动创建
        系统使用的ClusterToken - 系统使用的kubeconfig，用于shell 等场景使用
        控制器管理ClusterToken，并同步到对应的工作集群
        认证 - Warden服务使用ClusterToken进行认证
        删除ClusterToken - 删除时管控集群ClusterToken马上删除，后异步删除工作集群ClusterToken
        删除ClusterToken - 所属用户被删除时，ClusterToken一起被删除
        删除ClusterToken - 所属集群被删除时，ClusterToken一起被删除
        ClusterToken - 数量限制-无数量限制，会在管控集群中持续累积
        用户手动创建ClusterToken使用无效
        用户手动删除工作集群ClusterToken - 管控集群会自动同步回来，最多15m延迟
        用户手动修改工作集群ClusterToken - 管控集群会自动覆盖修改的内容，最多15m延迟
        ClusterToken资源定义
        删除ClusterToken-从后端手动删除长期未使用的token，根据lastUserAt（最近使用的时间）判断
        删除用户 - 当用户被删除/集群使用者角色就触发 SKS 后台自动删除该用户
        删除用户 - 同步删除用户在管控集群的数据，工作集群数据异步删除
        删除用户 - 删除所有用户的ProjectRoleBinding，删除所有的ClusterToken
        User资源定义
        系统角色模板 - sks-system-core/sks-role-template-admin「管理所有资源与配置」
        系统角色模板 - sks-system-core/sks-role-template-manage-config「管理配置」
        系统角色模板 - sks-system-core/sks-role-template-manage-network「管理服务与网络」
        系统角色模板 - sks-system-core/sks-role-template-manage-pvc「管理持久卷申领」
        系统角色模板 - sks-system-core/sks-role-template-manage-workload「管理工作负载」
        系统角色模板 - sks-system-core/sks-role-template-viewer「查看所有资源与配置」
        系统角色 - default/{cluster-name}-workload-developer 「应用开发者」
        系统角色 - default/{cluster-name}-workload-operator 「应用运维管理员」
        角色继承 - 系统角色和用户角色的rules继承自角色模板-spec.aggregationRoles
        工作集群 - 每个ProjectRole对应一个ClusterRole，通过控制器从管控集群同步至工作集群
        工作集群 - 更新ProjectRole后，查看对应ClusterRole，权限更新
        ProjectRole删除 - 删除所有ProjectRoleBinding，删除ClusterRole，移除ProjectRoleFinalizer
        ProjectRole删除 - 删除ProjectRoleBinding时，异步删除工作集群上RoleBinding等资源
        ProjectRole删除 - 关联用户的ProjectRole从后端删除后，验证用户无对应权限
        用户在工作集群自定义创建ClusterRole，若与SKS创建的重名-会被覆盖
        多租户 - 验证登陆工作集群使用者视角下展示正常
        多租户 - 验证登陆工作集群使用者视角后，集群控制台功能正常
    控制台
        热启动池-workpool-pod名称：cloudshell-worker-10字符
        热启动池-workpool-集群控制台的cloudshell关联pod，在删除cloudshell时，pod会被一并删除
        热启动池-workpool-检查有多少可用的空闲池-kubectl get pods -l 'worker.cloudtty.io/owner-name='
        热启动池-workpool-热启动，当前有空闲pod，创建cloudshell时申请pod，从空闲pod中分配
        热启动池-workpool-冷启动，当前无空闲pod，创建cloudshell时申请pod，会创建新的pod分配给cloudshell
        cloudshell- 集群控制台名称：clustername-cluster-xxxxxx
        cloudshell- Pod控制台名称：clustername-pod-xxxxxx
        cloudshell- 节点控制台名称：clustername-node-xxxxxx
        cloudshell- 控制台名称，创建集群名称最长32字符，查看使用是否正常
        cloudshell-集群控制台CloudShell-使用流程
        cloudshell-集群控制台shell，annotation：cloudshell.cloudtty.io/delete-worker-on-deletion: "true"
        cloudshell-节点控制台CloudShell-使用流程
        节点控制台- node-shell - 在节点启动特权pod-nsenter，通过node-shell插件管理
        节点控制台- node-shell - 清理，当断开连接时，删除cloudshell，自动删除该nsenter pod
        cloudshell-pod控制台CloudShell
        cloudshell-pod控制台，当删除pod时，断开连接，删除控制台后自动清理cloudshell
        cloudshell-删除工作集群的时候会自动清理对应集群相关的 CloudShell
        cloudshell-每创建一个控制台，产生一个cloudshell
        cloudshell-删除控制台，删除对应cloudshell
        资源回收-开启一个控制台，在管控集群中创建default/cloud-shell-worker-xxx运行实例pod
        资源回收 - 控制台设置 300s 的 TTL，当持续使用时，自动增加TTL-cloudshell cr
        cloudshell 检查 ：label.kubesmart.smtx.io/user-name
        cloudshell 检查 ：spec.secretRef.name
        terminal权限 - /root/.kube/config 权限- 600
        terminal - k 支持补全
        sks-cloudtty-controller-manager 的资源分配检查-request/limit
        cloudtower中不应该有sks-cloudtty-controller-manager
        pod控制台验证上传文件
        pod控制台验证下载文件
    一键导入yaml
        验证yaml可正常导入
        验证从单个文件导入
        验证选择文件夹导入
        验证json可正常导入
        验证导入时选择namespace
    EUC
        验证overlay模式-执行e2e
        验证underlay模式-执行e2e
    用户容器镜像仓库
        用户容器镜像仓库 - 1.4 版本用户容器镜像仓库可部署
        用户容器镜像仓库 - 1.4 版本用户容器镜像仓库可加入 AKE 工作集群的受信任容器镜像仓库
    物理机集群
        物理机集群 - Rocky 8.10 可创建物理机集群
        物理机集群 - Rocky 8.10 物理机集群可升级 K8s 版本
        物理机集群 - Ubuntu 22.04 可创建物理机集群
        物理机集群 - Rocky 8.9 可创建物理机集群
    NTP
        NTP - 可从 AOC 同步 NTP 配置到registry、管控集群和所有工作集群
        NTP - 点击手动同步可立即同步更新后的 NTP 配置
        NTP - 自动同步开启的情况下，AOC NTP 配置变动，一段时间后 AKE 自动同步到各集群
SKS 1.5
    日志切换到可观测性
        功能介绍
            实现 - 修改grafana的数据源 - http://ovm_ip/grafana/explore - loki
            使用前提
                可观测性服务要求
                    SKS关联 - 可观测性服务 - 正在部署 - 无法选择进行关联 - 禁用原因：无法关联
                    SKS1.5new - SKS关联 - 可观测性服务 - 部署失败 - 无法选择进行关联 - 禁用原因：无法关联
                    SKS关联 - 可观测性服务 - 正在卸载 - 无法选择进行关联 - 禁用原因：无法关联
                    SKS1.5new - SKS关联 - 可观测性服务 - 卸载失败 - 无法选择进行关联 - 禁用原因：无法关联
                    SKS关联 - 可观测性服务 - 正在升级 - 无法选择进行关联 - 禁用原因：无法关联
                    SKS关联 - 可观测性服务 - 升级异常 - 无法选择进行关联 - 禁用原因：无法关联
                    SKS关联 - 可观测性服务 - 正在启用流量可视化功能 - 无法选择进行关联 - 禁用原因：无法关联
                    SKS关联 - 可观测性服务 - 正在禁用流量可视化功能 - 无法选择进行关联 - 禁用原因：无法关联
                    SKS1.5discard - SKS关联 - 可观测性服务 - 服务状态异常 - 无法选择进行关联 - 禁用原因：无法关联
                    SKS1.5new - SKS关联 - 可观测性服务 - 管理网络异常或健康检查失败 - 无法选择进行关联 - 禁用原因：无法关联
                    SKS1.5new - SKS关联 - 可观测性服务 - 运行服务的虚拟机状态异常 - 无法选择进行关联 - 禁用原因：无法关联
                    SKS关联 - 可观测性服务 - 可观测性服务容器异常 - 无法选择进行关联 - 禁用原因：无法关联
                    SKS1.5new - SKS关联 - 可观测性服务 - 告警链路异常 - 无法选择进行关联 - 禁用原因：无法关联
                    SKS关联 - 可观测性服务 - 可观测性服务与该对象正在关联/取消关联 - 无法选择进行关联 - 禁用原因：已与该对象关联
                工作负载集群要求
                    SKS关联 - 可观测性服务正常 - 工作负载集群就绪 - 可正常关联OBS
                    SKS关联 - 可观测性服务正常 - 工作负载集群运行中 - 可正常关联OBS
                    SKS关联 - 可观测性服务正常 - 工作负载集群failed - 可正常关联OBS
                    SKS关联 - 可观测性服务正常 - 工作负载集群updating - 无法关联OBS
                关联关系
                    单个可观测性服务可对应多个对象（SKS系统服务/工作负载集群）- 无关联上限
                    1个对象（SKS系统服务/工作负载集群）只能关联一个可观测性服务
                    对象（SKS系统服务/工作负载集群）- 关联OBS后才可以启用监控，报警，日志，审计，事件功能
                    对象（SKS1.5新建工作负载集群）- 关闭「关联可观测性服务」，监控、日志、报警、事件、审计随之一起关闭
                    对象（SKS系统服务）- 关闭「关联可观测性服务」，「功能启用状态」随之一起关闭
                    对象（SKS系统服务/工作负载集群）- 关联OBS后修改obs name - 大概2min左右会同步到插件页面的输入框中
            新部署SKS1.5
                管控集群 - 新部署 - 默认不开启日志，监控，报警，事件，审计 - 功能启用状态按钮关闭
                管控集群 - 仅关联obs但不开启日志，监控，报警，事件，审计 - 保存成功后检查ksc - monitoring的 obsinstance 字段有值，但是logging的obsinstance部分enabled:false不展示
                管控集群 - 关联obs后监控,日志,事件,审计,报警全开 - 成功后检查ksc.spec.component.logging/monitoring/alert以及ksc.status.externalServices
                管控集群 - 监控,报警,日志,事件,审计全开后全部关闭 - obss被删除，检查ksc.spec.components以及ksc.status.externalServices
                管控集群 - 监控,报警,日志,事件,审计全开后切换obs - 切换成功，obss新建重新绑定
                管控集群 - 监控,报警,日志,事件,审计全开后切换obs - 切换成功，切换前未解决的报警将自动解决，
已解决的报警数据不会被清除，依旧展示在已解决列表中，
且所有报警的详情页的报警规则部分均展示：报警规则不存在
                新建工作负载集群 - 默认不开启关联可观测性服务「日志，监控，报警，事件，审计 」
                新建工作负载集群 - 仅关联obs但不开启日志，监控，报警，事件，审计 - 创建成功后检查ksc - monitoring的 obsinstance 字段有值，但是logging的obsinstance部分enabled:false不展示
                新建工作负载集群 - 关联obs后未开启监控仅开启日志 - 新建对应的obss - 检查注册信息ObservabilitySystemService.status.register
                新建工作负载集群 - 关联obs后仅开启监控 - addon部分增加obs-monitoring-agent和kube-prometheus
                新建工作负载集群 - 关联obs后仅开启日志 - 检查新建obss被logging使用，spec.features:logging:true
                新建工作负载集群 - 关联obs后先开启监控,报警后再开启日志，事件，审计 - 检查无新建obss，使用已有的obss，检查obss.spec.feature.monitoring/alert/logging:true
                新建工作负载集群 - 关联obs后监控,日志，事件，审计，报警全开 - 成功后检查ksc.spec.component.logging/monitoring/alert以及ksc.status.externalServices
                新建工作负载集群 - 监控,报警,日志,事件,审计全开 - 编辑ksc，logging.obsinstance 和 monitoring.obsinstance 字段obs修改为不同值 - 编辑失败
                新建工作负载集群 - 监控,报警,日志,事件,审计全开 - 关闭监控报警 - obss不会被删除，仅删除obss.spec.feature.monitoring/alert:false，ksc.spec.components.monitoring.obsinstance字段保持不被清理
                新建工作负载集群 - 监控,报警,日志,事件,审计全开 - 关闭日志 - obss不会被删除，仅更新obss.spec.feature.logging:false
                新建工作负载集群 - 监控,报警,日志,事件,审计全开 - 仅关闭日志，事件和审计保持开启 - ksc.spec.components.logging.obsinstance字段还在，表示obs未解除关联
                新建工作负载集群 - 监控,报警,日志,事件,审计全开 - 关闭日志后切换新的obs后再开启日志 - ksc.spec.components.monitoring.obsinstance更新为新的obs
                编辑工作负载集群 - 监控,报警,日志,事件,审计全开后全部关闭但是保持obs关联 - obss不会被删除，检查ksc.spec.components以及ksc.status.externalServices
                编辑工作负载集群 - 日志,事件,审计依次关闭 - 所有日志组件关闭成功时，obss.spec.components.logging.enabled 设置为 false
                编辑工作负载集群 - 监控,报警,日志,事件,审计全开后全部关闭并关闭obs服务 - 再次开启 - obss重新创建，重新绑定到ksc.spec.components.logging.obsinstance
                编辑工作负载集群 - 监控,报警,日志,事件,审计全开后切换obs - 切换成功，obss新建重新绑定
                编辑工作负载集群 - 监控,报警,日志,事件,审计全开后切换obs - 切换成功，obss新建重新绑定，obss event记录解绑和重新关联过程
                编辑工作负载集群 - 监控,报警,日志,事件,审计全开后切换obs - 切换成功，返回obs服务部分查看 - 关联系统服务对象从obs A切换到obs B
                编辑工作负载集群 - 监控,报警,日志,事件,审计全开后切换其他obs - 切换成功，监控、日志、事件、审计的数据从切换后开始记录展示
                删除工作负载集群 - 监控,报警,日志,事件,审计全开 - 集群正常删除，与obs服务正常解除关联关系
                删除工作负载集群 - 开启日志,事件,审计 - 集群正常删除，与obs服务正常解除关联关系
                卸载SKS集群 - 集群监控,报警,日志,事件,审计全开 - 集群正常卸载，与obs服务正常解除关联关系
                新增addon
                    管控集群 - 新部署 - 开启日志 - 新增addon - obs-logging-agent（daemonset）
                    管控集群/工作负载集群 - 新部署 - 开启日志 - 新增addon - obs-logging-agent - 版本 （1.0.0-r4）
                    管控集群 - 新部署 - 开启日志 - 新增addon - obs-event-agent - 版本（1.0.0-r2）
                    管控集群 - 新部署 - 开启日志 - 新增addon - obs-audit-agent - 版本 (1.0.0-r2)
                    新建工作负载集群 - 开启事件 - 新增addon - obs-event-agent（deployment）- 127.0.0.1:2280 监听端口
                    obs-event-agent - 参数配置在event-configmap和observability-event-agent
            升级场景 - 旧数据迁移
                管控/工作负载集群 - 迁移前ovm可用容量检查 - 容量不足，obs服务返回异常，迁移继续，扩容ovm容量/手动清理迁移数据步骤：ksc手动关闭日志
                管控/工作负载集群 - 迁移前ovm可用容量检查 - 多个对象同时迁移到一个ovm，迁移过程中容量不足，迁移继续，obs服务异常 - 需要手动清理：编辑ksc关闭日志
                管控/工作负载集群 - ksc新增annotation - kubesmart.smtx.io/logging-migrate-done: 迁移结束或者不需要迁移
                管控/工作负载集群 - ksc新增annotation - kubesmart.smtx.io/logging-migrate-start:触发日志迁移开始，开始后自动移除
                管控/工作负载集群 - ksc新增annotation - kubesmart.smtx.io/logging-migrate-running:日志正在迁移中
                管控集群 - logging-event-migrate,logging-log-migrate job Completed - 迁移完成，migrate pod日志中可以看到实时进度
                管控集群 - logging-event-migrate,logging-log-migrate job Completed - 迁移完成后migrate job会自动删除
                管控/工作负载集群 - 迁移日志过程中，可以从ksc event看到迁移进度
                工作负载集群 - 迁移日志过程中，使用ovm的grafana页面查看迁移数据是否可查询：http://192.xxx/grafana/explore
                管控/工作负载集群 - 迁移成功后，删除旧存储es的pv/pvc，tower中对应的volume等资源
                管控/工作负载集群 - 迁移成功后，开启事件，旧事件数据全部迁移，在OBS下一个清理周期清理事件至7天
                管控/工作负载集群 - 迁移成功后，更新插件参数配置，ksc变化 - 旧日志组件关闭，新的组件开启
                工作负载集群（修改日志默认配置）- 迁移成功后，自动更新插件参数配置 - 去掉保留时间、存储容量的配置框，清空 YAML 配置框
                管控/工作负载集群 - 迁移成功后，日志默认保存30d，关闭后不删除，选择同一个obs重新开启，关闭前的日志正常展示
                管控/工作负载集群 - 迁移前日志保留手动设置超过30d，迁移成功后，日志数据全部迁移，等obs下一次清理周期，超过30d时间的日志会被清理
                管控/工作负载集群 - 迁移成功后，日志大概3min后可查看，搜索
                管控/工作负载集群 - 迁移成功后，日志标签pod_name无法使用，旧日志数据中筛选的key中无此标签，新产生的日志可以通过此标签筛选
                管控/工作负载集群 - 迁移成功后，日志标签pod_node_name无法使用
                管控/工作负载集群 - 迁移日志量超过30d的集群，记录迁移速度以及迁移量和迁移时间
                工作负载集群 - 先切换到新版日志再开启审计 - 集群先updating状态更新kube-apiserver参数，原地更新和迁移日志数据同时进行
            启用/关闭日志
                启用日志 - SKS系统服务 - 部署后 - 未关联OBS - 无法启用
                启用日志 - SKS系统服务 - 部署后 - 关联1.4.2以下的OBS - 无法选择关联，obs列表只展示142及以上的obs
                启用日志 - SKS系统服务 - 部署后 - 关联1.4.2及以上的OBS - 关联成功并启用成功
                启用日志 - 工作负载集群（ZBS/ELF）/（虚拟机/物理机）- 创建时启用 - 关联1.4.2及以上的OBS - 关联成功并启用成功
                启用日志 - 工作负载集群（ZBS/ELF）/（虚拟机/物理机）- 创建时启用 - 关联1.4.2以下的OBS - 无法关联，不支持的版本会被过滤不在列表展示
                启用日志 - 工作负载集群（ZBS/ELF）/（虚拟机/物理机）- 创建后启用 - 关联1.4.2及以上的OBS - 关联成功并启用成功
                启用日志 - 工作负载集群（ZBS/ELF）/（虚拟机/物理机）- 创建后启用 - 关联1.4.2以下的OBS - 无法关联，不支持的版本会被过滤不在列表展示
                启用日志 - 工作负载集群（ZBS/ELF）/（虚拟机/物理机）- 日志默认保留30d，30d以上的数据自动清理
                关闭日志 - SKS系统服务 - 仅关闭日志不关闭关联obs - 关闭后日志数据保留不清理
                关闭日志 - SKS系统服务 - 关闭日志后一段时间，日志还在节点上且未发生轮转 - 重新开启日志后，可以查询到关闭时间段产生的日志
                关闭日志 - SKS系统服务 - 关闭日志后重新开启选择同一个obs - 关闭前的旧数据正常展示
                关闭日志 - 工作负载集群（ZBS/ELF）/（虚拟机/物理机）- 关闭日志后重新开启，切换新的obs - 旧数据不展示
            日志标签查询 --- TBD
                A - 日志查询 - 所有SKS logs筛选条件添加{source_service="SKS"}
                日志查询 - 新建工作负载集群，曾经开启过日志，关闭一段时间后再开启 - 上次关闭至本次开启时间段内还在主机上的log，超过30min会被刷新为当前时间
                日志查询 - 最大label数量无限制 - 配置超过15个label - 可正常筛选
                日志查询 - 使用label筛选 - 在grafana中使用loki语句查询 - 比对UI和grafana以及原始日志数据，保持一致
                日志查询 - 不采集非SKS组件的日志 - 创建新的nginx容器产生新的日志 - 预期Loki查询不到数据
                日志查询 - 创建新的容器产生新的日志 - 比对UI和grafana以及原始日志数据，保持一致 - 需要先配置自定义参数
                kubenetes容器日志 - {cluster="xxxx",source_type="kubernetes_logs"}
                特定container日志 - {cluster="xxxx",source_type="kubernetes_logs",container_name="xxxx"}
                指定pod label的日志 - {cluster="xxxx",source_type="kubernetes_logs",pod_label_xxx="xxxx"}
                特定pod日志 - {cluster="xxxx",source_type="kubernetes_logs",pod_name="xxxx"}
                特定pod所在的node日志 - {cluster="xxxx",source_type="kubernetes_logs",pod_node_name="xxxx"}
                特定pod所在的namespace日志 - {cluster="xxxx",source_type="kubernetes_logs",pod_namespace="xxxx"}
                指定节点文件日志 - {cluster="xxxx",source_type="os_file",hostname="xxx"}
                指定文件路径日志 - {cluster="xxxx",source_type="os_file",file="来源文件路径"}
                节点文件日志 - {cluster="xxxx",source_type="os_file"}
                指定节点文件日志 - {cluster="xxxx",source_type="os_file",hostname="xxx"}
                指定节点内核文件日志 - {cluster="xxxx",source_type="os_file",hostname="xxx",file="/var/log/messages"}
                节点journald日志 - {cluster="xxxx",source_type="journald"} - 查询该时间段所有节点的 systemd 服务日志
                指定节点journald日志 - {cluster="xxxx",source_type="journald",hostname="xxx"}
                指定服务journald日志 - {cluster="xxxx",source_type="journald",systemd_unit=“xxx”}
                kubernetes审计日志 - {cluster="xxxx",module="kube-apiserver-audit"} - 默认策略
                特定名字查询kube-apiserver审计日志 - {cluster="xxxx",module="kube-apiserver-audit",objectref_name="xxx"}
                loki label限制
                    UI标签查询 - SKS采集日志时自动删除系统自动生成的标签：kapp.k14s.io/association
                    UI标签查询 - SKS采集日志时自动删除系统自动生成的标签：app.kubernetes.io/part-of
                    UI标签查询 - SKS采集日志时自动删除系统自动生成的标签：controller-revision-hash
                    UI标签查询 - SKS采集日志时自动删除系统自动生成的标签：pod-template-generation
                    UI标签查询 - SKS采集日志时自动删除系统自动生成的标签：pod-template-hash
                    UI标签查询 - SKS采集日志时自动删除系统自动生成的标签：kapp.k14s.io/app
                    UI标签查询 - 标签key中的包含的 /  -  . 符号均不支持，会被替换为下划线 _(举例：kubernetes.labels.cluster_x-k8s_io/provider会被替换为kubernetes_labels_cluster_x_k8s_io_provider)
                    UI标签查询 - 无法与es保持一致直接查询pod label，现查询label格式：pod_label_xxx=xxx
                    UI标签查询 - list展示label 时移除前缀pod_label_ 确保和k8s中看到的一致
                    UI标签查询 - pod label展示只保留6个，多余的丢弃，logging-agent中会有warn log
        已有功能影响
            插件参数配置  --- TBD
                工作负载集群 - 迁移成功后，自动更新插件参数配置 - 新增可配置参数
                工作负载集群 - 迁移成功后，清空obs-logging-agent的yaml配置框
                新建工作负载集群 - 插件参数配置 - 新增可配置参数 - 默认不配置 - 创建成功后只有resource的默认值
                创建工作负载集群 - 插件参数配置 - 新增可配置参数 - 配置extraDataLabels，extraEnvs
                创建工作负载集群 - 插件参数配置 - 新增可配置参数 - 配置extraArgs
                创建工作负载集群 - 插件参数配置 - 新增可配置参数 - 配置非默认的resources - 创建成功后检查，非默认resources值
                编辑工作负载集群 - 插件参数配置 - 新增可配置参数 - 采集主机的 /opt/logs 目录日志，配置extraFileInput，extraVolumeMounts，extraVolumes
                编辑工作负载集群 - 插件参数配置 - 新增可配置参数 - 发送日志到外部系统，配置extraSinks
                编辑工作负载集群 - 插件参数配置 - 可配置参数 - 编辑配置非默认的resources - 编辑成功后检查，是配置的resources值
                编辑工作负载集群 - 插件参数配置 - 删除所有已增加的配置参数 - 删除成功
            插件展示
                已有管控/工作负载集群 - 升级到1.5，保持旧版日志，概览页插件保持不变
                已有管控集群 - 升级到1.5，切换到新版日志，概览页插件移除elasticsearch，elasticCurator，kibana，fluentbit，logging-operator，event-exporter新增obs-logging-agent，obs-event-agent,obs-audit-agent
                已有工作负载集群 - 升级到1.5，切换到新版日志但未开启事件、审计，概览页插件移除elasticsearch，elasticCurator，kibana，fluentbit，logging-operator新增obs-logging-agent
            解除关联可观测性与启用监控的绑定关系
                管控集群 - 仅关联obs但不开启日志，监控，报警，事件，审计 - 保存成功后,返回可观测性服务页面，不允许卸载
                管控集群 - 仅关联obs但不开启日志，监控，报警，事件，审计 - 关闭关联obs - 可观测性服务允许卸载
                管控集群 - 仅关联obs但不开启日志，监控，报警，事件，审计 - 关联成功后再开启监控，报警、事件、审计、日志 - 开启成功
                工作负载集群 - 编辑仅关联obs但不开启监控，报警 - 编辑保存成功
                工作负载集群 - 编辑关闭监控，报警 - obs可保持开启不关闭 - 关闭成功
            日志UI不再依赖监控是否开启
                新部署管控集群 - 关联obs后开启日志、监控，报警、事件、审计 - 日志数据正常展示
                新建工作负载集群 - 关联obs后仅开日志不开启监控，报警 - 日志数据正常展示
                管控集群 - SKS1.4开启日志升级到SKS1.5 - 不切换新版日志，旧版EFK组件继续运行，无ksc.components.logging.obsinstance字段
                工作负载集群 - SKS1.4仅开启日志升级到SKS1.5 - 切换新版日志，旧数据迁移，迁移成功后可以看到UI展示日志数据
            报警规则
                集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中日志的组件 {{ $labels.deployment }}{{ $labels.daemonset }}{{ $labels.statefulset }} 异常持续 15 分钟。默认阈值：15m且不支持配置阈值 - 详情页展示字段
                切换到新版日志后，自动移除旧日志报警规则 - KubeSmartClusterPluginLoggingStatusAbnormal
                集群开启日志组件，才会创建规则到ovm
            放开已有限制
                工作负载集群（物理机集群） - 无CSI - 可开启关联可观测性服务
                工作负载集群（物理机集群） - 无CSI，无sc - 限制无法开启监控
                升级 - 已有工作负载集群（物理机集群）无CSI，无sc - 允许关联obs服务，但是限制无法开启监控，允许开启日志，事件，审计
                工作负载集群 - 无CSI，无SC - 可开启日志，事件，审计
                工作负载集群 - 已开启监控，日志，事件，审计 - worker节点数量 - 大于等于 3 的集群允许缩容到小于 3
        升级场景
            SKS1.4.0 - 关联了可观测性1.4.0，且开启了监控、日志 - 允许升级到SKS1.5.0 - 升级后不升级可观测性版本，监控+旧版日志正常运行，但是旧版日志不可用
            SKS1.4.0 - 关联了可观测性1.4.0，且开启了监控、日志 - 允许升级到SKS1.5.0 - 升级后不升级可观测性版本，监控+旧版日志正常运行，无法触发旧日志迁移
            SKS1.4.0 - 关联了可观测性1.4.0，且开启了监控、日志 - 允许升级到SKS1.5.0 - 升级后先升级可观测性版本至1.4.2，手动触发日志的旧数据迁移
            SKS1.4.0 - 关联了可观测性1.4.0，且开启了监控、日志 - 升级后先升级至obs1.4.2 - ksc.status.externalServices.monitoringObservability 字段废弃，数据自动迁移到 observabilityService 字段中
            SKS1.4.0 - 关联了可观测性1.4.1，且开启了监控、日志 - 允许升级到SKS1.5.0 - 升级后手动触发日志的旧数据迁移
            SKS1.4.0 - 关联了可观测性1.4.1，且开启了监控、日志 - 允许升级到SKS1.5.0 - 升级后监控+旧版日志正常运行，但旧版日志不可看
            SKS1.4.0以下开启监控日志升级到SKS1.4.0 - 未关联可观测性 - 不允许升级到SKS1.5.0，升级失败报错 - 需要先关联可观测性1.4.0/1.4.1后处理监控后才可以升级
            仅工作负载集群 - SKS1.4.0关联了可观测性1.4.0，且开启了监控未开启日志 - SKS允许升级到SKS1.5.0
            仅工作负载集群 - SKS1.4.0关联了可观测性1.4.0，且开启了监控未开启日志 - 允许升级到SKS1.5.0，升级后无法开启日志
            仅工作负载集群 - SKS1.4.0 关联了可观测性1.4.0，且开启了监控未开启日志 - 允许升级到SKS1.5.0，升级后ksc.status.externalServices.monitoringObservability 字段废弃，数据自动迁移到 observabilityService 字段中
            仅工作负载集群 - SKS1.4.0关联了可观测性1.4.0，且开启了监控未开启日志 - 允许升级到SKS1.5.0，升级后无法开启日志，升级可观测性服务至1.4.1，启用日志成功
            仅工作负载集群 - SKS1.4.0关联了可观测性1.4.1，且开启了监控未开启日志 - 允许升级到SKS1.5.0
            仅工作负载集群 - SKS1.4.0关联了可观测性1.4.1，且开启了监控未开启日志 - 允许升级到SKS1.5.0，升级后可以开启日志，无旧数据迁移
            SKS1.4.0以下仅开启监控升级到SKS1.4 - 未关联了可观测性 - 不允许升级到SKS1.5.0，会导致升级失败 - 需要先在SKS1.4为监控关联可观测性1.4.0/1.4.1后才允许升级
            SKS1.4.0 - 未关联可观测性，仅开启了日志 - 允许升级到SKS1.5.0
            SKS1.4.0 - 未关联可观测性，仅开启了日志 - 允许升级到SKS1.5.0 - 升级后关联可观测性1.4.0 - 无法选择，只能选择obs1.4.1及以上版本
            SKS1.4.0 - 未关联可观测性，仅开启了日志 - 允许升级到SKS1.5.0 - 升级后关联可观测性1.4.1 - 可以手动触发日志旧数据迁移
            SKS1.4.0 - 未关联可观测性，未开启监控、日志 - 允许升级到SKS1.5.0
            SKS1.4.0 - 未关联可观测性，未开启监控、日志 - 允许升级到SKS1.5.0 - 升级后关联可观测性1.4.2，可开启监控，日志，报警，事件，审计
            升级限制
                SKS1.3.2 - 升级到SKS1.5.0 - 不支持该版本升级路径 - 错误码：INSTALLED_SKS_TOO_OLD（不支持升级至该版本）
                YTT版本 - 有ytt1.3.2的SKS1.4.0 - 升级到1.5.0 - 存在不在 SKS 版本兼容范围内的工作集群。 - 错误码：CLUSTER_SKS_VERSION_NOT_IN_COMPATIBLE_RANGE
                SKS1.4.0工作负载集群 - 未关联obs但开启旧监控 - 升级管控集群到SKS1.5.0及以上版本 - 升级失败有报错
                SKS1.5.0管控集群 - 监控、日志必须全切到OBS - 否则无法升级到SKS1.5.0以上版本 - 升级报错
                SKS1.5.0工作负载集群 - 监控、日志必须全切到OBS - 否则无法升级到SKS1.5.0以上版本 - 升级报错
                SKS1.5.0工作负载集群 - 插件全部关闭，未关联obs - 升级到SKS1.5.0以上版本 - 允许升级
        UI校验
            日志切换到可观测性
                日志对接可观测性服务
                    展示位置 - 新部署SKS系统服务 - 设置 - 可观测性配置 - 功能启用状态按钮
                    展示位置 - 创建工作负载集群 - 插件配置 - 可观测性 - 日志（启用button下有可观测性服务版本的提示文案）
                    展示位置 - 编辑工作负载集群 - 插件管理 - 可观测性 - 日志（展示在报警下）
                    新部署SKS系统服务 - 设置 - 可观测性配置 - 不允许选择1.4.2以下版本的可观测性服务关联
                    新部署SKS系统服务 - 设置 - 可观测性配置 - 选择1.4.2及以上版本的可观测性服务关联 - 功能启用状态按钮 - 可选择开启，监控报警日志事件审计一键全开
                    创建工作负载集群 - 插件配置 - 可观测性 - 不允许选择1.4.2以下版本的可观测性服务关联
                    创建工作负载集群 - 插件配置 - 可观测性 - 选择1.4.1及以上版本的可观测性服务关联 - 可以开启日志
                    编辑工作负载集群 - 插件管理 - 可观测性 - 不允许选择1.4.1以下版本的可观测性服务关联
                    编辑工作负载集群 - 插件管理 - 可观测性 - 选择1.4.1及以上版本的可观测性服务关联 - 可以开启日志
                    新部署SKS系统服务 - 设置 - 可观测性配置 - 仅关闭「功能启用状态」按钮 - 允许关闭，监控、报警、日志、事件、审计一键全关
                    新部署SKS系统服务 - 设置 - 可观测性配置 - 关闭「关联可观测性服务」- 功能启用状态（监控、报警、日志、事件、审计）一键全关
                    工作负载集群 - 插件管理 - 可观测性 - 仅关闭「日志」- 允许单独关闭
                    工作负载集群 - 插件管理 - 可观测性 - 关闭「关联可观测性服务」-  日志随之关闭，日志页面不再展示相关数据
                    展示内容变更
                        工作负载管理 - 插件管理 - 可观测性 - 新版日志 - 开启后默认展示「OBS-Logging-Agent 参数配置」，参数配置框默认为收起状态
                        工作负载管理 - 插件管理 - 可观测性 - 新版日志 - 开启后去掉保留时间、存储容量配置框
                        工作负载管理 - 插件管理 - 可观测性 - 新版日志 - 开启后更新 YAML 配置框参数 - 默认为空
                        SKS系统服务 - 概览页 - 管控集群插件状态card - 新版日志 - 移除插件「elasticsearch」「kibana」「curator」「logging-operator」「fluent-bit」
                        SKS系统服务 - 概览页 - 管控集群插件状态card - 新版日志 - 新增插件：「obs-logging-agent」
                日志查询替换为Grafana Explore方案
                    集群未升级维持旧版日志 - 查询方式也不变，维持旧版
                    集群升级后-维持旧版日志 - 旧版日志不可用，需要切换为新版日志才可查询
                    新版日志查询方案变更 - 替换为Grafana Explore方案，仅支持通过标签匹配和关键字搜索
                    时间和查询间隔控制 - 时间选择框「根据viewport宽度自适应」，查询间隔控制「宽度随交互行为动态显示」
                    时间范围选择器 - 相对时间 - 默认「过去10分钟」，预定义的相对时间范围与旧版日志保持一致「10min，1h，3h,24h，3d」
                    时间范围选择器 - 绝对时间 - 最大值为当前时间，禁用大于最大值的日期
                    实时日志流 - 实时检测日志的变动，有新增日志会立刻展示，hover展示提示文案：开启日志实时数据流
                    实时日志流 - 点击「实时」按钮后，开启日志实时数据流，操作栏隐藏「时间选择框」和「运行查询」，仅展示「暂停」和「退出实时模式」（按钮右侧显示）
                    discard - 实时日志流 - 点击「实时」按钮后，开启日志实时数据流 - 点击日志详情部分的「时间倒序」- 按照时间倒序滚动
                    实时日志流 - 点击「实时」按钮后，开启日志实时数据流 - 查询条件header部分的「复制查询」，「关闭查询」，「移除查询」按钮禁用
                    实时日志流 - 点击「实时」按钮后，开启日志实时数据流 -「添加查询」处于禁用状态，隐藏日志数量面板
                    实时日志流 - 点击「实时」按钮后，开启日志实时数据流 - 日志详情页面板下方显示「暂停」、「退出实时模式」和接收日志时间的描述
                    实时日志流 - 点击「实时」按钮后，开启日志实时数据流 - 点击「退出实时模式」- 退出并恢复至常规状态
                    实时日志流 - 点击「实时」按钮后，开启日志实时数据流，再点击「暂停」，按钮切换为「恢复」- 暂停实时数据流
                    实时日志流 - 暂停实时数据流 - 选择一条日志展开查看详情 - 日志部分不滚动
                    实时日志流 - 点击「实时」按钮后，再点击「暂停」- 暂停实时数据流 - 点击日志详情下的「退出实时模式」- 退出并恢复至常规状态
                    实时日志流 - 点击「实时」按钮后，开启日志实时数据流，再点击日志详情下方的「暂停」，两个按钮均切换为「恢复」- 暂停实时数据流
                    实时日志流 - 点击「实时」按钮后，开启日志实时数据流，用户在日志详情面板，存在滚动操作时，触发暂停日志实时数据流
                    实时日志流 - 点击「实时」按钮后，用户在日志详情面板存在滚动操作时，触发暂停日志实时数据流 - 再点击「退出实时模式」- 退出并恢复至常规状态
                    实时日志流 - 点击「实时」按钮后，开启日志实时数据流，用户在日志详情面板，存在滚动操作时，触发暂停日志实时数据流 - 再点击「恢复」- 继续日志实时数据流状态
                    实时日志流 - 点击「实时」按钮后，开启日志实时数据流，再点击「恢复」，实时按钮变成「暂停」 - 恢复开启实时数据流成功
                    运行查询 - 手动刷新日志 - 点击「运行查询」，按钮变为「取消」，日志页面重新查询
                    运行查询 - 自动刷新日志 - 切换设置自动刷新时间：关闭，5s，10s，30s，1m，5m，默认30s
                    查询区域 - 默认1个查询条件，支持移除
                    查询区域 - 默认1个查询条件，可添加多个，关系为「或」，数量无上限
                    查询区域 - 查询条件header - 名称 - 默认为A（新添加的名称默认依次为B、C等），支持原位修改
                    查询区域 - 查询条件header - summary - 对应原始查询内容，header展开时不展示，收起时展示
                    查询区域 - 查询条件header - 复制查询按钮 - hover tooltip 显示“复制查询”，点击后下方新增相同的查询面板
                    查询区域 - 查询条件header -「开启/关闭查询」按钮 - 开启时，hover tooltip显示“关闭查询”，点击后按钮变关闭查询状态，此时summary前提示文字提示：已禁用
                    查询区域 - 查询条件header -「开启/关闭查询」按钮 - 开启时，点击后按钮变关闭查询状态，此时hover tooltip显示“开启查询”，再次点击，成功开启查询，summary前的提示文字消失
                    查询区域 - 查询条件header -「移除查询」按钮 - hover tooltip 显示“移除查询”，点击后移除当前查询面板
                    查询区域 - 查询条件标签 - 集群选项默认置灰展示，只能查看当前集群 - 不可删除
                    查询区域 - 查询条件标签 - 日志类型（log type）的key默认置灰展示，value有3个可选：容器日志，节点操作系统日志，节点文件日志
                    查询区域 - 查询条件标签 - 日志类型：容器日志 - source_type:kubernetes_logs
                    查询区域 - 查询条件标签 - 日志类型：节点操作系统日志 - source_type:journald
                    查询区域 - 查询条件标签 - 日志类型：节点文件日志 - source_type:os_file
                    查询区域 - 查询条件标签 - key分类：系统预定义(翻译)，用户自定义 - 系统预定义的key展示在用户自定义key的前面，支持搜索
                    查询区域 - 查询条件标签 - 系统预定义key:命名空间-namespace(namesapce,pod_namesapce) - value 是这两部分的合集
                    查询区域 - 查询条件标签 - 系统预定义key:节点-node(pod_node_name，hostname)
                    查询区域 - 查询条件标签 - 系统预定义key:pod-pod(pod_name)
                    查询区域 - 查询条件标签 - 系统预定义key:容器- container(container_name)
                    查询区域 - 查询条件标签 - 系统预定义key:Systemd服务-systemd service(systemd_unit)
                    查询区域 - 查询条件标签 - 系统预定义key:文件路径-file_path(file)
                    查询区域 - 查询条件标签 - 用户自定义key:除系统预定义的key以外举例：involvedobject_apiversion
                    查询区域 - 查询条件标签 - 用户自定义key - 查询展示pod_label_{用户自定义key}
                    查询区域 - 查询条件目标文本筛选 - 包含目标文本的日志
                    查询区域 - 多查询条件目标文本筛选 - 多个相同的条件筛选，删除某个条件 - 其他条件可正常筛选文本
                    查询区域 - 查询条件目标文本筛选 - 排除目标文本的日志
                    查询区域 - 查询条件目标文本筛选 - 匹配正则表达式的日志
                    查询区域 - 查询条件目标文本筛选 - 不匹配正则表达式的日志
                    查询区域 - 多查询条件目标文本筛选 - 不匹配正则表达式的日志+包含目标文本的日志，多个条件之间为逻辑与
                    查询区域 - 查询条件 原始查询 - 原始查询语句，与标签部分完全匹配，原始查询随着标签的增加而同步变化
                    查询区域 - 查询条件 选项 - 默认为展开状态，收起时显示summary，分别是「数量上限」和「分辨率」
                    查询区域 - 查询条件 选项 - 默认为收起状态，展开后，当前header不显示summary
                    查询区域 - 查询条件 选项 - 展开后，数量上限默认值1000，最大值5000，hover info icon,tooltip显示：返回的日志数量上限
                    查询区域 - 查询条件 选项 - 展开后，修改数量上限默认值，修改后日志详情部分数量上限随之变化
                    查询区域 - 查询条件 选项 - 分辨率默认1/1，展开后有6个选项，可切换
                    查询区域 - 查询条件 选项 - 分辨率默认1/1，切换非默认分辨率  - 日志数量部分的图表随之变化
                    异常 - 查询区域 - 查询条件 - 输入超大数量上限值，出现查询error，error信息展示在header部分
                    日志数量 - 空状态 - 视图范围内无数据
                    日志数量 - 空状态 - 查询中，loading页面
                    日志数量 - 根据筛选内容正确展示数量
                    日志详情 - 共有标签:根据用户在查询面板中选择的标签对应显示 value 值，单个标签最大宽度 235px（无法展示完整，打点，hover 显示完整标签名称）
                    日志详情 - 数量上限：日志已达数量上限 1000，当前展示的时间范围为（9sec），占查询范围（1h）的 0.26%。
                    日志详情 - 已处理的总字节数：xxx MB
                    日志详情 - 日志中可能包含转移错误的字符「转义换行符」，hover 时 tooltip 提示“已修复日志中转义错误的换行符和制表符。请手动查询结果，确认替换是否正确”。
                    日志详情 - 筛选结果默认按照「时间倒序」进行展示
                    日志详情 - 筛选结果默认按照「时间倒序」进行展示，切换为「时间正序」，筛选结果列表随之切换
                    日志详情 - 空状态 - 视图范围内无数据
            SKS系统服务 - 可观测性配置
                新部署SKS1.5.0
                    新部署SKS1.5.0 - 未开启日志功能 - 日志tab下空状态展示
                    新部署SKS1.5.0 - 关联1.4.2及以上版本的obs - 「功能启用状态」按钮解除禁用
                    新部署SKS1.5.0 - 关联1.4.2及以上版本的obs并开启「功能启用状态」按钮 - 监控、报警、日志、事件、审计开启成功
                规则调整
                    允许仅关联可观测性服务 - 不启用监控和报警
                    允许直接切换可观测性服务 - 不需要先关闭再开启
                    启用 - 未选择可观测性服务，「功能启用状态」按钮不可开启，有提示文案：需关联可观测性服务
                升级版本后的界面影响
                    监控 - 升级后迁移监控数据，迁移过程中，在按钮下方显示「loading icon」+文案：旧监控数据迁移中
                    升级前，未关联可观测性服务，开启日志
                        升级前，仅开启日志，未关联可观测性服务 - 升级后，可观测性配置页面展示变更
                        升级前，仅开启日志，未关联可观测性服务 - 升级后，旧版日志保持开启状态（UI不展示），且功能无法使用
                        升级前，仅开启日志，未关联可观测性服务 - 升级后，勾选「关闭旧版日志并清除旧数据」，保存成功后相关提示不再显示
                        升级后，仅关联1.4.1及以上版本的obs，不开启「功能启用状态」按钮 - 关联obs成功后，obs服务展示已关联状态且「功能启用状态」按钮下出现提示：旧版日志功能无法使用+关闭旧版日志..按钮+切换为新版日志功能后，事件...
                        升级后，仅关联1.4.2及以上版本的obs，可观测性服务下文案更新：仅支持选择版本为 1.4.2及以上的可观测性服务。若无可用服务，可在系统配置中设置。「系统服务」link可点击跳转
                        升级后，关联1.4.1及以上版本的obs，选择可观测性服务下拉列表 - 仅展示1.4.1及以上版本的可观测性服务
                        升级后，关联1.4.1及以上版本的obs，选择可观测性服务下拉列表 - 1.4.1及以上版本的可观测性服务异常，禁用并展示原因
                        升级后，关联1.4.1及以上版本的obs保存后，再开启「功能启用状态」- 出现「切换为新版日志并实现旧数据迁移」按钮，勾选后，提示全部消失
                        升级后，关联1.4.1及以上版本的obs，并开启「功能启用状态」- 旧版日志Notice Tip提示消失，增加「旧日志数据迁移」选项
                        升级后，关联1.4.1及以上版本的obs，并开启「功能启用状态」后不保存直接关闭「功能启用状态」- 页面保持原状，仅展示Notice Tip和关闭旧版日志功能并清除旧数据勾选框
                        升级后，关联obs，并开启「功能启用状态」后直接保存 - 监控、报警、日志功能开启，各自的tab页面有数据，日志无旧数据
                        升级后，关联obs，并开启「功能启用状态」后直接保存 - 保存后再关闭「功能启用状态」- 变成仅关联obs状态，按钮下有「旧日志数据会清除」提示
                        升级后，关联obs，开启「功能启用状态」后保存后关闭再开启- 监控、报警、日志、事件、审计开启且日志部分无旧数据也没有notice tip提示
                        升级后，关联obs，开启「功能启用状态」- 勾选「旧日志数据迁移」保存时检查obs可用容量是否满足需求，不满足保存失败，有serious tip显示原因
                        升级后，关联obs，开启「功能启用状态」- 勾选「旧日志数据迁移」保存成功，开始迁移数据
                        升级后，关联obs，开启「功能启用状态」- 勾选「旧日志数据迁移」保存成功，开始迁移数据，迁移过程中关闭「关联可观测性服务」- 按钮开启且禁用，不可关闭
                        升级后，关联obs，开启「功能启用状态」- 勾选「旧日志数据迁移」保存成功，开始迁移数据，迁移过程中关闭「功能启用状态」 - 按钮开启且禁用，不可关闭，不可终止迁移过程
                        升级后，关联obs，开启「功能启用状态」- 勾选「旧日志数据迁移」保存成功，开始迁移数据，若迁移失败，默认job有重试可以继续迁移，如果超过限制可以手动删除job，控制器会重新创建job继续重试，如果还失败，需要手动清理（关闭es插件）
                        升级后，关联obs，开启「功能启用状态」- 勾选「旧日志数据迁移」保存成功，迁移完成，按钮解禁，可查看日志旧数据
                        升级后，关联obs，开启「功能启用状态」并勾选「旧日志数据迁移」- 迁移完成后关闭「功能启用状态」再开启，旧日志依旧保留
                        升级后，关联obs，开启「功能启用状态」并勾选「旧日志数据迁移」- 迁移完成，可观测性服务输入框不禁用，且输入框下「查看服务详情」link
                        升级后，关联obs，开启「功能启用状态」并勾选「旧日志数据迁移」，迁移完成 - 切换obs服务 - 切换成功，监控、日志数据从切换成功时间点开始展示
                        升级后，迁移旧日志数据完成 - 关联的obs异常 - 常规显示 - 可观测性服务输入框后展示error icon,hover展示：可观测性服务状态异常
                        升级后，迁移旧日志数据完成 - 关联的obs异常 - 极限值显示 - 名称无法展示完全，hover时tooltip展示完全，可观测性服务输入框后展示error icon,hover展示：可观测性服务状态异常
                        升级后，迁移旧日志数据完成 - 关闭「关联可观测性服务」- 出现serious tip提示文案，保存后消失不展示
                    升级前，关联可观测性服务，开启日志
                        升级前，关联的obs1.4.2版本
                            升级后，监控、报警、旧日志保持启用状态 - 可观测性配置页面展示变更
                            升级后，监控、报警、旧日志保持启用状态 - 支持选择「切换为新版日志并实现旧数据迁移」
                            升级后，关闭「关联可观测性服务」-「功能启用状态」按钮随之关闭 - 检查可观测性配置页面serious tip
                            升级后，关闭「关联可观测性服务」-「功能启用状态」按钮随之关闭 - 监控、报警关闭成功，旧版日志不会随之关闭，事件，审计保持未开启状态
                            升级后，关闭「关联可观测性服务」-「功能启用状态」按钮随之关闭 - 保存成功后展示「旧版日志无法使用」，「关闭旧版日志...」、「切换为新版日志后。。。」的提示
                            升级后，关闭「功能启用状态」- 保存成功，监控、报警被关闭 - 未解决报警自动标记为已解决，旧版日志保持开启但是UI无法查看
                            升级后，关闭「功能启用状态」- 保存成功，勾选「关闭旧版日志功能并清除旧数据」- 保存后，旧日志数据被清除
                            升级后，关闭「功能启用状态」，勾选「关闭旧版日志功能并清除旧数据」- 保存后，旧日志数据被清除 - 再重新开启「功能启用状态」，监控、报警、日志被开启，日志不展示旧数据
                            A - 升级后，勾选「切换为新版日志并实现旧数据迁移」- 「旧版日志功能无法使用」、「关闭旧版日志功能并清除旧数据」和「切换新版日志。。。。。」不再显示
                            升级后，勾选「切换为新版日志并实现旧数据迁移」- 「旧版日志功能无法使用」、「关闭旧版日志功能并清除旧数据」和「切换为新版日志。。。。」不再显示，取消勾选，恢复显示
                            升级后，勾选「切换为新版日志并实现旧数据迁移」- 保存成功，「功能启用状态」保持开启且禁用状态，并在下方显示「旧日志数据迁移中」
                            升级后，勾选「切换为新版日志并实现旧数据迁移」- 保存后迁移失败，「功能启用状态」保持开启，「切换为新版日志并实现旧数据迁移」可重新勾选
                            升级后，勾选「切换为新版日志并实现旧数据迁移」- 保存后迁移成功，「功能启用状态」按钮解除禁用
                            升级后，勾选「关闭旧版日志功能并清除旧数据」- 「切换为新版日志并实现旧数据迁移」按钮禁用不可选择
                            升级后，勾选「关闭旧版日志功能并清除旧数据」-  保存成功后，Notice Tip 不再显示，复选框更新为「启用新版日志功能」
                            升级后，勾选「关闭旧版日志功能并清除旧数据」-  保存成功后，监控、报警保持开启，日志、事件、审计关闭状态
                            升级后，勾选「关闭旧版日志功能并清除旧数据」-  保存成功后，勾选「启用新版日志功能」- 新版日志启用成功，从成功起开始记录日志，事件和审计也一并开启
                        升级前，关联的obs1.4.0版本
                            升级后，监控、报警、日志保持启用状态 - 可观测性配置页面中可观测性服务输入框变成可编辑
                            升级后，监控、报警、日志保持启用状态 - 可观测性配置页面变更检查
                            升级后，监控、报警、日志保持启用状态 - 监控、报警可正常使用，旧版日志无法使用，UI不展示
                            升级后，由于obs1.4.0版本 - 不支持开启新版日志功能，无「切换为新版日志并实现旧数据迁移」按钮
                            升级后，升级已关联的obs至1.4.1版本 - 「功能启用状态」按钮下的文案消失，「切换为新版日志并实现旧数据迁移」按钮展示
                            升级后，升级已关联的obs至1.4.1 - 关闭「关联可观测性服务」-「功能启用状态」按钮随之关闭 - 检查可观测性配置页面serious tip
                            升级后，升级已关联的obs至1.4.1 - 关闭「关联可观测性服务」-「功能启用状态」按钮随之关闭 - 保存成功后展示「旧版日志无法使用」，「关闭旧版日志...」，「切换为新版日志功能后，事件和审计...」的提示
                            升级后，升级已关联的obs至1.4.1 - 关闭「关联obs服务」- 保存成功，监控、报警被关闭 - 未解决报警自动标记为已解决，旧版日志保持开启但是UI无法查看
                            升级后，升级已关联的obs至1.4.2 - 关闭「功能启用状态」- 保存成功，勾选「关闭旧版日志功能并清除旧数据」- 保存后，旧日志数据被清除
                            升级后，升级已关联的obs至1.4.2 - 关闭「功能启用状态」，勾选「关闭旧版日志功能并清除旧数据」- 保存后，旧日志数据被清除 - 再重新开启「功能启用状态」，日志开启但不展示旧数据
                            升级后，升级已关联的obs至1.4.2 - 勾选「切换为新版日志并实现旧数据迁移」- 「旧版日志功能无法使用」、「关闭旧版日志功能并清除旧数据」、「切换为新版日志功能后，事件和..」不再显示，取消勾选，恢复显示
                            升级后，升级已关联的obs至1.4.2 - 勾选「切换为新版日志并实现旧数据迁移」- 保存成功，「功能启用状态」保持开启且禁用状态，并在下方显示「旧日志数据迁移中」
                            升级后，升级已关联的obs至1.4.1 - 勾选「关闭旧版日志功能并清除旧数据」- 「切换为新版日志并实现旧数据迁移」按钮禁用不可选择
                            升级后，升级已关联的obs至1.4.1 - 勾选「关闭旧版日志功能并清除旧数据」-  保存成功后，Notice Tip 不再显示，复选框更新为「启用新版日志功能」
                            升级后，升级已关联的obs至1.4.1 - 勾选「关闭旧版日志功能并清除旧数据」-  保存成功后，勾选「启用新版日志功能」- 新版日志启用成功，从成功起开始记录日志
                            升级后，切换1.4.1版本的obs - 「功能启用状态」按钮下的文案消失，「切换为新版日志并实现旧数据迁移」按钮展示
                            升级后，切换1.4.1版本的obs - 监控数据从切换后时间点开始展示，日志保持旧版UI无法展示
                            升级后，切换1.4.1版本的obs - 关闭「关联可观测性服务」-「功能启用状态」按钮随之关闭 - 检查可观测性配置页面serious tip
                            升级后，切换1.4.1版本的obs - 关闭「关联可观测性服务」-「功能启用状态」按钮随之关闭 - 保存成功后展示「旧版日志无法使用」，「关闭旧版日志...」，「切换为新版日志，，，，」的提示
                            升级后，切换1.4.1版本的obs - 关闭「功能启用状态」- 保存成功，监控、报警被关闭 - 未解决报警自动标记为已解决，旧版日志保持开启但是UI无法查看
                            升级后，切换1.4.1版本的obs - 关闭「功能启用状态」- 保存成功，勾选「关闭旧版日志功能并清除旧数据」- 保存后，旧日志数据被清除
                            升级后，切换1.4.1版本的obs - 关闭「功能启用状态」，勾选「关闭旧版日志功能并清除旧数据」- 保存后，旧日志数据被清除 - 再重新开启「功能启用状态」，监控、报警、日志、事件、审计被开启，日志不展示旧数据
                            升级后，切换1.4.2版本的obs - 勾选「切换为新版日志并实现旧数据迁移」- 保存成功，「功能启用状态」保持开启且禁用状态，并在下方显示「旧日志数据迁移中」
                            升级后，切换1.4.1版本的obs - 勾选「关闭旧版日志功能并清除旧数据」-  保存成功后，监控、报警开启，日志事件审计关闭状态，勾选「启用新版日志功能」- 新版日志、事件、审计启用成功，从成功起开始记录日志
            工作负载集群 - 可观测性
                创建工作负载集群
                    创建工作负载集群 - 插件配置 - 默认可观测性部分全部关闭
                    创建工作负载集群 - 插件配置 - 仅关联可观测性服务 - 仅可选择1.4.2及以上版本，输入框下提示更新
                    创建工作负载集群 - 插件配置 - 仅关联可观测性服务 - 仅可选择1.4.1及以上版本，选择后监控和日志解除禁用
                    创建工作负载集群 - 插件配置 - 关联可观测性服务并开启监控 - 创建成功
                    创建工作负载集群 - 插件配置 - 关联可观测性服务并开启监控、报警 - 监控下方出现提示：关闭后，报警功能也会自动关闭。
                    创建工作负载集群 - 插件配置 - 关联可观测性服务并开启监控、报警 - 创建成功
                    创建工作负载集群 - 插件配置 - 关联可观测性服务并开启日志 - 创建成功
                    创建工作负载集群 - 插件配置 - 关联可观测性服务并开启监控、报警、日志 - 创建成功
                规则调整
                    允许仅关联可观测性服务 - 不启用监控和报警
                    允许直接切换可观测性服务 - 不需要先关闭再开启
                    仅最新版可观测性服务（obs1.4.1及以上）才支持开启新版日志
                    「英文文案」启用 - 未选择可观测性服务，监控、报警、日志、事件、审计不可开启，按钮禁用，按钮下提示禁用原因
                    启用 - 关联obs1.4.1及以上，监控、日志可选择开启，报警需监控开启后才可开启
                    关闭 - 关闭「关联可观测性服务」后，监控、报警、日志、事件、审计一起随之关闭
                    关闭 - 报警和日志可独立关闭
                升级版本后的界面影响
                    升级前，未关联可观测性服务，未开启日志
                        升级后，查看工作负载集群插件管理页面 - 关联可观测性服务保持关闭，监控、报警、日志启用按钮禁用并展示原因
                        升级后，工作负载集群插件管理页面 - 关联1.4.2及以上的obs服务，关联成功，监控和日志可选择开启，报警需要监控开启后才可以开启
                        升级后，工作负载集群插件管理页面 - 仅关联1.4.1及以上的obs服务，关联成功
                        升级后，工作负载集群插件管理页面 - 关联1.4.1及以上的obs服务，并开启监控、报警、日志 - 保存成功，监控、日志数据从保存成功开启起记录
                    升级前，未关联可观测性服务，开启日志
                        升级后，保持未关联obs，日志保持开启状态，但是功能无法使用，插件管理页面的日志按钮下有提示
                        升级后，保持未关联obs，监控、报警无法开启，日志保持开启状态，但是功能无法使用，日志页面提示：日志功能不可用
                        升级后，保持未关联obs，监控、报警无法开启，日志保持开启状态，但是功能无法使用，关闭旧版日志serious tip提示旧数据会被清除
                        升级后，保持未关联obs，监控、报警无法开启，日志保持开启状态，但是功能无法使用，关闭旧版日志 - 关闭成功，旧数据被清除，相关pv被清理
                        升级后，关联obs1.4.1及以上 - 监控、报警保持关闭状态，日志下方显示「切换为新版日志并实现数据迁移」选项，并且依旧提示：旧版日志功能无法使用
                        升级后，关联obs1.4.1及以上 - 监控、报警保持关闭状态，日志保持旧版 - 关联成功
                        升级后，关联obs1.4.1及以上 - 开启监控、报警，日志保持旧版 - 监控、报警开启成功
                        升级后，关联obs1.4.2及以上 - 开启监控、报警，日志切换为新版并迁移旧数据 - 监控、日志开启成功，日志旧数据迁移成功，可成功展示
                        discard - 升级后，关联obs1.4.1及以上 - 日志切换为新版并迁移旧数据 - 迁移过程中关闭日志，后再仅开启事件/审计 - 事件/审计开启成功「最终结论，迁移过程中不允许关闭日志」
                        升级后，关联obs1.4.1及以上 - 日志切换为新版并迁移旧数据 - 迁移过程中切换obs服务 - 不允许切换
                        升级后，关联obs1.4.1及以上 - 仅日志切换为新版并迁移旧数据 - 日志旧数据迁移成功，可成功展示，迁移完成后，按钮解除禁用状态
                        升级后，关联obs1.4.1及以上 - 再关闭关联obs服务，旧版日志保持开启，obs服务关闭成功
                    升级前，关联可观测性服务，未开启日志
                        升级前，已关联obs1.4.0
                            升级前，已关联obs1.4.0，仅开启监控 - 升级后，obs保持关联，监控保持开启，报警关闭状态，插件页面日志是禁用不可开启状态
                            升级前，已关联obs1.4.0，仅开启监控 - 升级后，升级obs至1.4.1及以上，监控保持开启，报警关闭状态，日志按钮解除禁用，可开启
                            升级前，已关联obs1.4.0，仅开启监控 - 升级后，切换obs1.4.1及以上，监控保持开启，报警关闭状态，日志按钮解除禁用，可开启
                            升级前，已关联obs1.4.0，开启监控、报警 - 升级后，obs保持关联，监控、报警保持开启，插件页面日志是禁用不可开启状态
                            升级前，已关联obs1.4.0，开启监控、报警 - 升级后，升级obs至1.4.1及以上，监控、报警保持开启，日志按钮解除禁用，可开启
                            升级前，已关联obs1.4.0，开启监控、报警 - 升级后，切换obs1.4.1及以上，监控、报警保持开启，日志按钮解除禁用，可开启
                        升级前，已关联obs1.4.1及以上
                            升级前，已关联obs1.4.1及以上，仅开启监控 - 升级后，关联可观测性服务和监控保持开启，报警和日志关闭状态
                            升级前，已关联obs1.4.1及以上，仅开启监控 - 升级后，关联可观测性服务和监控保持开启，报警和日志手动开启 - 新版日志开启成功，显示新版插件配置项
                            升级前，已关联obs1.4.1及以上，开启监控、报警 - 升级后，关联可观测性服务和监控、报警保持开启，日志关闭状态
                            升级前，已关联obs1.4.2及以上，开启监控、报警 - 升级后，关联可观测性服务和监控、报警保持开启，日志手动开启 - 新版日志开启成功，显示新版插件配置项
                    升级前，关联可观测性服务，开启日志
                        升级前，已关联obs1.4.0
                            升级前，已关联obs1.4.0，开启监控、日志
                                升级前，开启kibana - 升级后，切换为新版日志，kibana一并被清理关闭
                                升级后，obs保持关联，监控、日志保持开启，但是旧版日志无法使用，报警关闭状态
                                升级后，obs保持关联，监控、日志保持开启，日志页面空状态不可用
                                升级后，升级已关联的obs至1.4.1及以上 - 日志下方出现「切换为新版日志并实现旧数据迁移」选项，以及提示：旧版日志功能无法使用
                                升级后，切换已关联的obs至1.4.1及以上 - 切换obs成功，日志保持旧版日志
                                升级后，切换已关联的obs至1.4.1及以上 - 切换obs成功，切换新版日志 - 日志迁移过程中，关闭日志 - 不支持关闭，日志按钮开启且禁用
                                升级后，切换已关联的obs至1.4.1及以上 - 切换新版日志 - 日志迁移过程中，关闭「关联可观测性服务」 -  按钮开启且禁用，不支持关闭
                                升级后，切换已关联的obs至1.4.1及以上 - 切换新版日志并且日志迁移成功后 - 关联可观测性服务和日志 按钮解除禁用状态，可编辑
                                升级后，切换已关联的obs至1.4.1及以上 - 切换obs成功，检查可观测性服务部分，对象成功切换至新的obs关联的系统服务下
                                升级后，切换已关联的obs至1.4.1及以上 - 关闭「关联可观测性服务」，提示文案更新：关联可观测性服务关闭后，监控、报警、日志、事件和审计功能也会自动关闭。
                                升级后，切换已关联的obs至1.4.1及以上 - 关闭「关联可观测性服务」，监控随之关闭
                                升级后，切换已关联的obs至1.4.1及以上 - 关闭「关联可观测性服务」后再关闭旧版日志功能，serious tip：旧日志数据将会清除
                                升级后，切换已关联的obs至1.4.1及以上 - 关闭「关联可观测性服务」和旧版日志功能 - 保存成功，旧日志数据被清除，相关pv被清理，可观测性服务的关联系统服务也一并被清理
                            升级前，已关联obs1.4.0，开启监控、报警、日志
                                升级后，obs保持关联，监控、报警、日志保持开启，但是旧版日志无法使用
                                升级后，升级已关联的obs至1.4.2及以上 - 监控、报警保持开启，日志下方显示「切换为新版日志并实现旧数据迁移」复选框，并提示旧版日志不可用
                                升级后，升级已关联的obs至1.4.1及以上 - 监控、报警保持开启，关闭旧版日志 - 旧日志数据被清理
                                升级后，升级已关联的obs至1.4.1及以上 - 关闭「关联可观测性服务」- 监控、报警随之关闭，旧版日志还保持开启
                                升级后，升级已关联的obs至1.4.2及以上 - 关闭「关联可观测性服务」- 监控、报警随之关闭，出现Notice tip提示
                                升级后，升级已关联的obs至1.4.1及以上并切换为新版日志 - 关闭「关联可观测性服务」- 监控、报警、日志随之关闭
                        升级前，已关联obs1.4.1及以上
                            升级前，已关联obs1.4.1及以上，开启监控、日志 - 升级后，关联可观测性服务和监控、日志保持开启，报警关闭状态
                            升级前，已关联obs1.4.2及以上，开启监控、日志 - 升级后，旧版日志保持开启但是无法使用
                            升级前，已关联obs1.4.1及以上，开启监控、报警、日志 - 升级后，关联可观测性服务和监控、报警、日志保持开启
                            升级前，已关联obs1.4.2及以上，开启监控、报警、日志 - 升级后，勾选「切换为新版日志并实现旧数据迁移」后保存 - 旧数据迁移成功
                            升级前，已关联obs1.4.1及以上，开启监控、报警、日志 - 升级后，关闭旧版日志，serious tip提示：旧日志数据将会清除
                            升级前，已关联obs1.4.1及以上，开启监控、报警、日志 - 升级后，关闭旧版日志，旧日志数被清除，相关pv等资源被清理
                            升级前，已关联obs1.4.2及以上，开启监控、报警、日志 - 升级后，关闭旧版日志，打开新版日志，日志数据从打开成功起开始记录展示
                            升级前，已关联obs1.4.1及以上，开启监控、报警、日志 - 升级后，关闭「关联可观测性服务」，旧版日志不会随之一起关闭，notice tip：关联可观测性服务关闭后，监控、报警、日志、事件和审计功能也会自动关闭。
            提示调整
                A - 管控集群概览页 - 未关联可观测性服务 - Notice Tip文案调整：SKS 系统服务未关联可观测性服务，无法启用监控、报警、日志、事件和审计功能。
                管控集群概览页 - 关联可观测性服务后 - Notice Tip文案消失不展示
                管控集群概览页 - SKS系统服务与可观测性服务关联异常 - Serious Tip文案调整：SKS 系统服务与可观测性服务%name%关联异常，监控、报警、日志、事件和审计功能将无法正常使用。
                管控集群概览页 - SKS系统服务与可观测性服务关联异常恢复后 - Serious Tip文案消失不展示
                管控集群概览页 - 已关联的可观测性服务状态异常 - 新增Serious Tip：可观测性服务 %obs-name% 状态异常，监控、报警、日志、事件和审计功能将无法正常使用。
                可观测性配置页面 - 已关联的可观测性服务状态异常 - 可观测性服务选择框，已选择的obs服务后有error icon，hover提示：可观测性服务状态异常
                管控集群概览页 - 已关联的可观测性服务状态异常恢复后 - Serious Tip消失不展示
                工作负载集群详情页 - 工作负载集群与可观测性服务关联异常 -Serious Tip文案调整：集群与可观测性服务%name%关联异常，监控、报警、日志、事件和审计功能将无法正常使用。
                工作负载集群详情页 - 工作负载集群与可观测性服务关联异常恢复 -Serious Tip文案消失不展示
                工作负载集群详情页 - 已关联的可观测性服务状态异常 - 新增Serious Tip文案：可观测性服务 %obs-name% 状态异常，监控、报警、日志、事件和审计功能将无法正常使用。
                工作负载集群详情页 - 已关联的可观测性服务状态异常恢复 - Serious Tip文案消失不展示
        错误码验证
            编辑ksc.components.logging/monitoring.obsinstance - 配置不同值 - SKS_MONITORING_AND_LOGGING_MUST_USE_SAME_OBS_INSTANCE
            编辑ksc.components.logging - 删除obsinstance - SKS_LOGGING_FUNCTION_MUST_ASSIGN_OBS_INSTANCE
            编辑ksc.components.logging - 开启日志但是插件全关 - SKS_LOGGING_FUNCTION_REQUIRE_AGENT
            新建SKS1.5.0集群 - 编辑ksc.components.logging开启旧版组件 - SKS_LOGGING_FUNCTION_NOT_ALLOW_USE_LEGACY_SOLUTION
            旧版集群迁移日志后 - 编辑ksc.components.logging开启旧版组件 - 报错error
        性能测试
            3+3管控集群插件全开， 默认审计策略（system策略） - 每小时数据增长量
            3+3集群插件全开， 默认审计策略（基础策略） - 每小时数据增长量
            3+3集群插件全开， 详细审计策略 - 每小时数据增长量
        自定义参数
            采集所有pod日志 - 配置obs-logging-agent addon参数，kubernetes.namespaceFilter.enabled:false
            采集节点上的日志文件 - 配置obs-logging-agent addon参数，配置extraFileInput，extraVolumeMounts，extraVolumes
            发送日志到外部系统 - 使用Loki作为接收端，配置obs-logging-agent addon参数，配置extraSinks
        权限
            OBS权限 - 有可观测性服务权限 - 关联对象后可以看到SKS服务以及详情可以看到对象展示
            OBS权限 - 无可观测性服务权限 - 关联对象后可以看到SKS服务以及详情可以看到对象展示
            SKS权限 - 有「SKS服务管理」权限 - 可以关联obs并同时开启监控、报警、日志、事件、审计
            SKS权限 - 有「SKS服务管理」权限到无权限 - 关联obs并同时开启监控、报警、日志、事件、审计 - 不刷新页面操作，后端拦截
            SKS权限 - 无「SKS服务管理」权限 - 无法关联/取消关联obs并开启/关闭监控、报警、日志、事件、审计
            SKS权限 - 有编辑工作负载集群权限 - 可以关联obs并开启监控、报警、日志、事件、审计
            SKS权限 - 编辑有编辑工作负载集群权限到取消权限 - 操作关联obs并开启监控、报警、日志、事件、审计，不刷新页面，后端拦截
            SKS权限 - 无编辑工作负载集群权限 - 无法关联/取消关联obs并开启/关闭监控、报警、日志、事件、审计
            SKS权限 - 只读用户 - SKS系统服务 - 无法关联/取消关联obs并开启/关闭监控、报警、日志、事件、审计
            SKS权限 - 只读用户 - 工作负载集群 - 无法关联/取消关联obs并开启/关闭监控、报警、日志、事件、审计
            SKS权限 - 只读用户 - 工作负载集群 - 无法编辑日志、事件、审计addon 参数
    UI支持灵活配置EIC Pod IP 池
        创建EIC集群
            EIC网卡配置 - 子网CIDR - hover时tooltip展示「子网 CIDR块 需为所选网络的 L3 子网」
            EIC网卡配置 - 子网CIDR - 输入cidr主机号不全为0，报错「子网CIDR主机号必须全为0」
            EIC网卡配置 - Pod IP 池 -hover时tooltip展示「在子网内划分出允许由 EIC 管理并分配给 Pod 使用的 IP 地址范围。」
            EIC网卡配置 - 原布局调整及文案验证 - 展示正确，无溢出
            EIC网卡配置 - Pod IP池交互 - 根据IP池数量展示ippool个数
            EIC网卡配置 - Pod IP池交互 - 点击「收起」，折叠IP池展示，按钮切换为「编辑」，再次点击「编辑」重新展开
            EIC网卡配置 - Pod IP池交互 - 点击「添加」增加一个Ip池填写区域，展示移除按钮，hover展示tooltip「移除Pod IP池」
            EIC网卡配置 - Pod IP池交互 - 名称校验 - 为空时提交「请填写Pod IP 池名称」
            EIC网卡配置 - Pod IP池交互 - 名称校验 - 字符数 - 「名称支持的字符长度范围为1-63」
            EIC网卡配置 - Pod IP池交互 - 名称校验 - 字符限制-「仅支持小写字母、数字、连字符（-），并且必须以小写字母或数字开头和结尾。」
            EIC网卡配置 - Pod IP池交互 - 名称校验 - 重名 - 「名称已存在」
            EIC网卡配置 - Pod IP池交互 - 地址范围 - 为空 「请填写IP地址范围」
            EIC网卡配置 - Pod IP池交互 - 地址范围 - IP格式 「IP地址格式错误」
            EIC网卡配置 - Pod IP池交互 - 地址范围 - 起始IP大于结束IP-「结束IP不可小于起始IP」
            EIC网卡配置 - Pod IP池交互 - 地址范围 - 多个IP池范围存在重叠-「IP地址重复」
            EIC网卡配置 - Pod IP池交互 - 地址范围 - IP不在子网CIDR范围-「IP 地址范围中有 IP 地址不在子网范围内。」
            EIC网卡配置 - Pod IP池交互 - 从地址范围切换CIDR块 - 切换后展示对应配置项，来回切换，已填写内容不会清空
            EIC网卡配置 - Pod IP池交互 -CIDR块 - 为空「请填写CIDR块。」
            EIC网卡配置 - Pod IP池交互 -CIDR块 - 格式不正确「CIDR块格式错误」
            EIC网卡配置 - Pod IP池交互 -CIDR块 - 多个IP池间存在IP重复「IP地址重复」
            EIC网卡配置 - Pod IP池交互 -CIDR块 - CIDR块中整个或一部分IP不在子网范围内「CIDR块中有IP地址不在子网范围内。」
            EIC网卡配置 - Pod IP池交互 -排除IP - 输入框提示语「可配置 IP 地址或 IP 地址范围，多条使用 “,” 隔开。」
            EIC网卡配置 - Pod IP池交互 -排除IP - IP格式错误「排除IP格式错误」
            EIC网卡配置 - Pod IP池交互 -排除IP - 输入范围，起始大于结束IP-「结束IP不可小于起始IP」
            EIC网卡配置 - Pod IP池交互 -排除IP - 排除IP内部存在重复「IP地址或IP地址范围存在重复IP」
            EIC网卡配置 - Pod IP池交互 -排除IP - 排除IP不在子网CIDR「排除IP不在CIDR块范围内。」
            EIC网卡配置 - Pod IP池交互 -排除IP - 输入框输入多个IP地址/IP范围组合时，能正确换行，输入后能正确展示
            EIC网卡配置 - Pod IP池交互 - 添加多个IP池配置项，可正常展开页面，无溢出
            EIC网卡配置 - Pod IP池交互 - 输入框出现错误提示，输入正确内容后提示隐藏
            创建EIC集群 - 仅配置一个EIC IP池「地址范围」，可正常创建，pod可分配ip，查看ksc及工作集群ippool配置，配置正确
            创建EIC集群 - 仅配置一个EIC IP池「CIDR」不排除IP，可正常创建，pod可分配ip，查看ksc及工作集群ippool配置，配置正确
            创建EIC集群 - 仅配置一个EIC IP池「CIDR」排除多个不连续IP，可正常创建，pod可分配ip，不包括排除IP，查看ksc及工作集群ippool配置，配置正确
            创建EIC集群 - 仅配置一个EIC IP池「CIDR」排除连续IP范围，可正常创建，pod可分配ip，不包括排除IP，查看ksc及工作集群ippool配置，配置正确
            创建EIC集群 - 配置2个EIC IP池「地址范围」，可正常创建，pod可从不同ippool分配ip，查看ksc及工作集群ippool配置，配置正确
            创建EIC集群 - 配置2个EIC IP池「地址范围」+「CIDR」，可正常创建，pod可从不同ippool分配ip，查看ksc及工作集群ippool配置，配置正确
            创建EIC集群 - 配置2个EIC IP池「地址范围」+「CIDR」排除IP，可正常创建，pod可从不同ippool分配ip，且不包含排除IP，查看ksc及工作集群ippool配置，配置正确
            创建EIC集群 - 配置n个EIC IP池组合，可正常创建，pod可从不同ippool分配ip，查看ksc及工作集群ippool配置，配置正确
            创建EIC集群 -当前集群 EIC IP池中Ip与已创建的集群的EIC Ippool中ip重叠，阻止创建-SKS_ECP_IP_POOL_OVERLAP_CONFLICT
            创建EIC集群 -当前集群 EIC IP池中Ip与已创建的集群的静态 Ippool中ip重叠，阻止创建
            创建EIC集群 -当前集群 EIC IP池中Ip与当前集群的静态 Ippool中ip重叠，阻止创建
            创建EIC集群 -当前集群 EIC IP池中Ip与其他集群的VIP冲突，阻止创建
            创建EIC集群 -当前集群 EIC IP池中Ip与其他集群的节点ip冲突，阻止创建
            创建EIC集群 -当前集群 EIC IP池中Ip与当前集群的VIP冲突，阻止创建
            创建EIC集群 -当前集群 EIC IP池中Ip与已关联物理机（service instance）IP冲突，阻止创建
        EIC插件配置
            插件展示 - CNI 下 EIC 插件，默认开启，按钮禁用，展示剩余可用IP数量，参数配置收起
            插件展示 - 剩余可用IP数量-统计所有ippool计数总和，与工作集群ippool中计数一致-剩余（allocated_count），总数（total_count）
            插件展示 - 剩余可用IP数量- 当有pod增加/减少时，统计值能实时更新，剩余可用的增加/减少数与pod增减一致
            插件展示 - 剩余可用IP数量- 若编辑IP池，增加或减少ip总数，统计值可实时更新，增加或减少值与配置一致
            插件展示 - 展开配置内容 -Pod IP 池默认为展开状态，与创建时一致，虚拟机网络、子网 CIDR、网关和 Pod IP 池名称仅展示不支持编辑。
            插件展示 - 展开配置内容 -Pod IP 池 展示文案与创建时一致
            插件展示 - 展开配置内容 -Pod IP 池 按钮交互与创建时一致，包括收起/编辑、移除按钮hover、配置方式切换展示
            插件配置 - 新增IP池 - 名称及IP地址校验同创建
            插件配置 - 新增IP池 - 添加一个IP池「地址范围」，可添加成功，ksc配置更新，工作集群新增一个ippool，新建pod可从新ippool中分配
            插件配置 - 新增IP池 - 添加一个IP池「CIDR」排除IP，可添加成功，ksc配置更新，工作集群新增一个ippool，新建pod可从新ippool中分配，且不包含排除IP
            插件配置 - 编辑IP池「地址范围」-缩小范围，被删减的IP已被分配pod使用，保存时footer报错（异步）-「%Pod IP 池名称%中的IP地址已被使用。」
            插件配置 - 编辑IP池「地址范围」-缩小范围，被删减的IP未被分配，可编辑成功，ksc及工作集群ippool更新，新增pod分配ip正确
            插件配置 - 编辑IP池「地址范围」-扩大范围，可编辑成功，ksc及工作集群ippool更新，新增pod分配ip正确
            插件配置 - 编辑IP池「CIDR」-缩小CIDR，被删减的IP已被分配pod使用，保存时footer报错（异步）-「%Pod IP 池名称%中的IP地址已被使用。」
            插件配置 - 编辑IP池「CIDR」-缩小CIDR，被删减的IP未被分配，可编辑成功，ksc及工作集群ippool更新，新增pod分配ip正确
            插件配置 - 编辑IP池「CIDR」-扩大CIDR，可编辑成功，ksc及工作集群ippool更新，新增pod分配ip正确
            插件配置 - 编辑IP池「CIDR」-添加排除IP，IP未被使用，可编辑成功，ksc及工作集群ippool更新，排除的IP不会被分配
            插件配置 - 编辑IP池「CIDR」-添加排除IP，IP已被使用，编辑失败，footer报错提示
            插件配置 - 编辑IP池「CIDR」-删除已排除IP，编辑成功，ksc及工作集群ippool更新，删除的排除IP可重新被分配给pod
            插件配置 - 编辑IP池 从「地址范围」切换为CIDR，设置相同CIDR，是否可编辑成功并正常应用
            插件配置 - 编辑IP池 从「地址范围」切换为CIDR，设置CIDR大于地址范围，是否可编辑成功并正常应用
            插件配置 - 编辑IP池 从「地址范围」切换为CIDR，设置CIDR小于地址范围，缩减IP未被使用，是否可编辑成功并正常应用
            插件配置 - 编辑IP池 从「CIDR」切换为地址范围，设置相同地址范围，是否可编辑成功并正常应用
            插件配置 - 编辑IP池 从「CIDR」切换为地址范围，设置地址范围大于CIDR，是否可编辑成功并正常应用
            插件配置 - 编辑IP池 从「CIDR」切换为地址范围，设置地址范围小于CIDR，缩减IP未被使用，是否可编辑成功并正常应用
            插件配置 - 多个IP池，删除已被使用的IP池，保存时提交失败「%Pod IP 池名称% 中的 IP 地址已被使用。」
            插件配置 - 多个IP池，删除未被使用的IP池，保存成功，ksc更新，工作集群删除该ippool，新增pod不会从其分配Ip
            插件配置 - 多个IP池，UI操作移除IP池，再重新添加成原有配置（名称、范围均一致），保存后不会有任何更新
            插件配置 - 多个IP池，移除IP池保存，再重新添加成原有配置（名称、范围均一致），保存后重新添加新的ippool，可正常分配ip
            插件配置 -当前集群 EIC IP池中Ip与已创建的集群的EIC Ippool中ip重叠，阻止配置
            插件配置 -当前集群 EIC IP池中Ip与已创建的集群的静态 Ippool中ip重叠，阻止配置
            插件配置 -当前集群 EIC IP池中Ip与当前集群的静态 Ippool中ip重叠，阻止配置
            插件配置 -当前集群 EIC IP池中Ip与其他集群的VIP冲突，阻止配置
            插件配置-当前集群 EIC IP池中Ip与当前集群的VIP冲突，阻止配置
            插件配置 -当前集群 EIC IP池中Ip与已关联物理机（service instance）IP冲突，阻止配置
        ipam-Annotation
            ipam - 创建pod时，添加annotation（ipam.everoute.io/pool:ippool-1）,创建pod后，自动从ippool-1中分配IP
            ipam - 创建pod时，添加ippool annotation，若ippool已无剩余ip，则pod不会被分配ip，pod无法创建
            ipam - 创建statefulset时，添加annotation（ipam.everoute.io/pool:ippool-1）,创建后产生的pod，自动从ippool-1中分配IP
            ipam - 创建statefulset时，添加ippool annotation，若ippool已无剩余ip，则pod不会被分配ip，pod无法创建
            ipam - 创建pod时，添加annotation（ipam.everoute.io/static-ip:ipaddr，ipam.everoute.io/pool:ippool-1）,创建pod后，ip指定为ippool-1中的staticip
            ipam - 创建pod时，添加static-ip annotation，若static ip已被使用，则pod不会被分配该ip，pod无法创建
            ipam - 创建statefulset时，添加annotation（ipam.everoute.io/ip-list，ipam.everoute.io/pool:ippool-1）,创建后产生的pod，自动从ippool-1中的list中分配IP
            ipam - 创建statefulset时，添加ip-list annotation，若replicas数超过ip-list数，则有部分pod无法创建
            ipam - 创建statefulset时，添加ip-list annotation，若list中有ip已被使用，则pod不会被分配该ip
            ipam - 创建pod/stateful时添加annotation，创建pod成功，已分配记录在ippool中，计入统计值
            ipam - 创建pod/stateful时添加annotation，创建pod成功，已分配记录在ippool中，此时删除或缩减，也会触发已被使用报错
        Webhook拦截
            ksc直接添加ippool，设置gateway不在subnet中，添加失败
            ksc直接添加ippool，同时设置cidr和start-end，添加失败
            ksc直接添加ippool，设置start-end时，增加except，添加失败
            ksc直接添加ippool，设置start-end时start大于end，添加失败
            ksc直接添加ippool，设置start-end 不在subnet中，添加失败
            ksc直接编辑ippool，cidr中添加except，ip已被使用，编辑失败
            ksc直接编辑ippool，修改cidr后，cidr不包括已被使用ip，编辑失败
            ksc直接编辑ippool，修改start-end后，不包括已被使用ip，编辑失败
            ksc直接添加ippool，gateway等于subnet，编辑失败
        场景测试
            并发测试 - 并发创建100pod，在并发创建50，分别记录创建时间
            并发测试 - 并发创建250，在并发创建50，分别记录创建时间
            并发测试 - 并发创建500，在并发创建50，分别记录创建时间
            并发测试 - 并发创建750，在并发创建50，分别记录创建时间
            并发测试 - 并发创建1000，在并发创建50，分别记录创建时间
            创建EIC集群 - 初始化创建，pod ip正常分配，正常创建无延迟
            创建EIC集群 - 开插件创建，pod ip正常分配，正常创建无延迟
            替换节点 - pod删除后创建，ip的分配及回收正常
            删除节点 - pod删除，ip的回收正常
            新建节点 - pod分配正常
            集群参数更新 - pod删除后创建，ip的分配及回收正常
            集群升级 - pod删除后创建，ip的分配及回收正常
            SKS升级，集群addon更新 - pod删除后创建，ip的分配及回收正常
            ippool设置地址范围，执行k8s-e2e，执行成功，测试通过
            ippool设置CIDR 并排除IP，执行k8s-e2e，执行成功，测试通过
            SKS升级 - （1.4-1.5）1.4创建的EIC集群，默认一个ippool-0（cidr），插件配置页面展示，并可配置以及增加修改
            SKS升级 - （1.4-1.5）1.4创建的EIC集群，手动ksc添加过多个ippool，插件配置页面展示，并可配置以及增加修改
            SKS升级 - 1.4创建的EIC集群，SKS升级到1.5后，升级工作集群k8s版本，可正常升级成功
        Discard
            discard-ipam - 创建pod时，添加annotation（ipam.everoute.io/ip-list，ipam.everoute.io/pool:ippool-1）,创建pod后，自动从ippool-1中的list中分配IP
            【discard】ipam - 创建pod时，添加ip-list annotation，若list中有ip已被使用，则pod不会被分配该ip
            discard - EIC网卡配置 - Pod IP池交互 -排除IP - 多个IP池间存在IP重复「IP地址重复」
    支持双活集群
        CRD 变更
            双活 - ElfCluster - 新增 spec.clusterType 字段，创建在双活集群 clusterType 值为 "Stretched"
            双活 - ElfCluster - 新增 spec.clusterType 字段，创建在非双活集群 clusterType 值为 "Standard"
            双活 - ElfCluster - 新增 spec.clusterType 字段，升级上来的非双活管控集群设置为 "Standard"
            双活 - ElfCluster - 新增 spec.clusterType 字段，升级上来的单活宿主上的虚拟机工作集群自动添加该字段，value 为 Standard
            双活 - ElfCluster - 新增 spec.clusterType 字段，升级上来的单活宿主上的物理机工作集群自动添加该字段，value 为 Standard
            双活 - ElfMachine - 新增 status.zone 字段，非双活集群的节点对应的 elfmachine 无该属性
            双活 - ElfMachine - 新增 status.zone 字段，双活集群位于优先域的节点对应的 elfmachine 中 status.zone 值为 "Preferred"
            双活 - ElfMachine - 新增 status.zone 字段，双活集群位于次级域的节点对应的 elfmachine 中 status.zone 值为 "Secondary"
            双活 - ElfMachine - 从优先域迁移节点到次级域，迁移后的 elfmachine 记录的 status.zone 值更新为 "secondary" - 10min 内刷新
            双活 - ElfMachine - 从次级域迁移节点到优先域，迁移后的 elfmachine 记录的 status.zone 值更新为 "preferred" - 10min刷新
            双活 - Node - 虚拟机节点新增 label cape.infrastructure.cluster.x-k8s.io/zone-id，记录节点所属可用域的 tower ID
            双活 - Node - 虚拟机节点新增 label cape.infrastructure.cluster.x-k8s.io/zone-type，记录节点所属可用域的类型
            双活 - Node - 非双活集群的虚拟机节点 node 中无 cape.infrastructure.cluster.x-k8s.io/zone-id label
            双活 - Node - 非双活集群的虚拟机节点 node 中无 cape.infrastructure.cluster.x-k8s.io/zone-type label
            双活 - Node - 双活环境物理机集群的 CP 节点 node 中有 cape.infrastructure.cluster.x-k8s.io/zone-id label
            双活 - Node - 双活环境物理机集群的 CP 节点 node 中有 cape.infrastructure.cluster.x-k8s.io/zone-type label
            双活 - Node - 双活环境物理机集群的 worker 节点 node 中无 cape.infrastructure.cluster.x-k8s.io/zone-id label
            双活 - Node - 双活环境物理机集群的 worker 节点 node 中无 cape.infrastructure.cluster.x-k8s.io/zone-type label
            双活 - Node - 虚拟机节点的可用域发生改变时，节点的 label 在 10min 内可感知，并完成更新
            双活 - KSC - 新增 spec.elfClusterType 字段，新创建在双活集群 elfClusterType 值为 "stretched"
            双活 - KSC - 新增 spec.elfClusterType 字段，新创建在非双活集群 elfClusterType 值为 "standard"
            双活 - KSC - 新增 spec.elfClusterType 字段，升级上来的管控集群设置为 "standard"
            双活 - KSC - 新增 spec.elfClusterType 字段，升级上来的单活宿主上的虚拟机工作集群自动添加该字段，value 为 Standard
            双活 - KSC - 新增 spec.elfClusterType 字段，升级上来的单活宿主上的物理机工作集群自动添加该字段，value 为 Standard
        SKS 服务部署
            SKS Registry
                双活 - 服务部署(Registry) - UI - 选中 amd64 安装包，集群选择列表允许选择 x86 intel 双活集群
                双活 - 服务部署(Registry) - UI - 选中 amd64 安装包，集群选择列表允许选择 x86 hygon 双活集群
                双活 - 服务部署(Registry) - UI - 选中 amd64 安装包，集群选择列表不展示 aarch64 双活集群
                双活 - 服务部署(Registry) - UI - 选中 arm64 安装包，集群选择列表允许选择 aarch64 双活集群
                双活 - 服务部署(Registry) - UI - 选中 arm64 安装包，集群选择列表不展示 x86 intel 双活集群
                双活 - 服务部署(Registry) - UI - 选中 arm64 安装包，集群选择列表不展示 x86 hygon 双活集群
                双活 - 服务部署(Registry) - UI - 集群选择列表展示版本为 6.0.x 及以上的双活集群
                双活 - 服务部署(Registry) - UI - 集群选择列表不展示版本低于 6.0.0 的双活集群
                img双活 - 服务部署(Registry) - UI - 「集群」字段的提示文案修改为「仅支持版本为 5.0.5 及以上且 CPU 架构与安装文件一致的 SMTX OS（ELF） 集群（双活集群要求版本为 6.0.0 及以上）」
                img双活 - 服务部署(Registry) - UI - 「集群」下拉列表显示的集群为双活集群，信息行标注「双活集群」
                双活 - 服务部署(Registry) - UI - 虚拟机网络选择列表中仅有 Access 模式的虚拟机网络
                双活 - 服务部署(Registry) - SKS registry 可在 x86 intel 双活集群上部署，产生虚拟机存储使用 3 副本精简策略
                双活 - 服务部署(Registry) - SKS registry 可在 aarch64 双活集群上部署，产生虚拟机存储使用 3 副本精简策略
                双活 - 服务部署(Registry) - SKS registry 可在 x86 hygon 双活集群上部署，产生虚拟机存储使用 3 副本精简策略
                双活 - 服务部署(Registry) - 存在多个同架构双活集群的情况下，SKS registry 部署在指定双活集群
                双活 - 服务部署(Registry) - 在优先域计算资源可满足部署需求的情况下，SKS registry 一定部署在优先域
                双活 - 服务部署(Registry) - 部署完成的 SKS registry 虚拟机 HA 优先级设置为：高
                双活 - 服务部署(Registry) - 在优先域计算资源不满足部署需求时，SKS registry 部署在次级域
                双活 - 服务部署(Registry) - 在优先域不可用时，部署SKS registry，可在次级域完成部署
                双活 - 服务部署(Registry) - SKS registry 虚拟机可以手动进行从优先域 -> 次级域的迁移
                双活 - 服务部署(Registry) - SKS registry 虚拟机可以手动进行从次级域 -> 优先域的迁移
            SKS 部署
                双活 - 服务部署(SKS) - UI - 部署 SKS 服务的集群选框不可编辑，正确展示双活集群名
                双活 - 服务部署(SKS) - UI - 集群中优先域和次级域可用节点总共不足3个时，高可用模式部署不成功
                双活 - 服务部署(SKS) - UI - 集群中优先域计算资源不足，算上次级域后资源充足，则高可用模式可部署
                双活 - 服务部署(SKS) - UI - 集群剩余计算资源不足以部署全部高可用模式节点时，高可用模式部署不成功
                双活 - 服务部署(SKS) - UI - 节点网络选择列表中仅有 Access 模式的虚拟机网络
                img双活 - 服务部署(SKS) - UI - 网络配置 - 子网掩码长度输入框减少，新增占位符提示「8-32」
                img双活 - 服务部署(SKS) - UI - 网络配置 - DNS 服务器地址输入 127.0.0.1，新增对应 inline 提示「127.0.0.1 不可用。」
                双活 - 服务部署(SKS) - 产生管控集群 CP 和 worker 虚拟机均使用 3 副本精简策略
                双活 - 服务部署(SKS) - 普通模式 - 创建 1 个使用必须放置在不同主机策略的放置组，1 CP 节点加入放置组
                双活 - 服务部署(SKS) - 普通模式 - 1 个 CP 节点始终部署在优先域
                双活 - 服务部署(SKS) - 普通模式 - 仅一个优先域主机满足部署需求，CP 节点部署在该主机
                双活 - 服务部署(SKS) - 普通模式 - 组件副本数检查 同单活
                双活 - 服务部署(SKS) - 普通模式 - 部署完成的所有管控集群虚拟机 HA 优先级设置为：高
                双活 - 服务部署(SKS) - 高可用模式 - 创建 1 个使用必须放置在不同主机策略的放置组，3 CP 节点加入放置组
                双活 - 服务部署(SKS) - 高可用模式 - 计算资源允许虚拟机创建时，3 个 CP 节点始终部署在优先域不同主机
                双活 - 服务部署(SKS) - 高可用模式 - 仅 2 个优先域主机满足部署需求，2 个 CP 节点部署在优先域不同主机，1 个 CP 节点部署在次级域
                双活 - 服务部署(SKS) - 高可用模式 - 仅 1 个优先域主机满足部署需求，1 CP 节点部署在该优先域主机，2 个 CP 节点部署在次级域
                双活 - 服务部署(SKS) - 高可用模式 - 3 主机的优先域中 1 主机处于维护模式，可部署，1 CP 节点放置在次级域
                双活 - 服务部署(SKS) - 高可用模式 - 部署完成的所有管控集群虚拟机 HA 优先级设置为：高
                双活 - 服务部署(SKS) - 高可用模式 - 后端触发 CP 节点替换，新的 CP 节点仍然部署在优先域 - TBD 试一下
                双活 - 服务部署(SKS) - 高可用模式 - 组件副本数检查 - 同单活
                双活 - 服务部署(SKS) - 高可用模式 - 部署完成后，优先域主机进入维护模式，1 CP 节点移动至次级域，退出维护模式时可自动迁回优先域原宿主主机
                双活 - 服务部署(SKS) - 模式提升 - 普通模式提升到高可用模式，新创建的 2 个 CP 节点加入必须放置组，且始终部署在优先域的不同主机
                双活 - 服务部署(SKS) - 模式提升 - 提升模式新增的管控集群虚拟机 HA 优先级设置为：高
                双活 - 服务部署(SKS) - 模式提升 - 剩余可用主机不足2个时，普通模式提升到高可用模式不成功
                双活 - 服务部署(SKS) - worker 节点 - 仅创建一个 优先放置在不同节点的放置组，worker 节点全部加入该放置组
                双活 - 服务部署(SKS) - worker 节点 - worker 节点分布服从 ELF 调度，有可能出现跨域部署
                双活 - 服务部署(SKS) - 未部署过 SKS 的 Tower 使用双活集群部署 SKS，生成对应的 90 天试用license
            服务信息详情
                双活 - 设置 - UI - SKS registry 详情页上，点击集群名称，跳转到双活集群页面
                双活 - 设置 - UI - SKS registry 详情页上，点击主机名称，跳转到可用域下的主机页面
                双活 - 设置 - UI - SKS registry 详情页上，点击主机名称，跳转到集群下的对应虚拟机，展开虚拟机详情侧边栏
                双活 - 设置 - UI - 管控集群详情页上，点击集群名称，跳转到双活集群页面
                双活 - 设置 - UI - 管控集群详情页上，点击主机名称，跳转到可用域下的主机页面
        节点模板
            同构上传
                双活 - 模板上传 - 部署 SKS 到 x86 intel 双活集群，v1.26 版本 Rokcy 节点模板上传到目标双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 intel 双活集群，上传节点文件 v1.25 Rocky OS，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 intel 双活集群，上传节点文件 v1.27 Rocky OS，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 intel 双活集群，上传节点文件 v1.28 Rocky OS，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 intel 双活集群，上传节点文件 v1.29 Rocky OS，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 intel 双活集群，上传节点文件 v1.30 Rocky OS，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 intel 双活集群，上传节点文件 v1.25 openEuler x86，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 intel 双活集群，上传节点文件 v1.26 openEuler x86，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 intel 双活集群，上传节点文件 v1.27 openEuler x86，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 intel 双活集群，上传节点文件 v1.28 openEuler x86，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 intel 双活集群，上传节点文件 v1.29 openEuler x86，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 intel 双活集群，上传节点文件 v1.30 openEuler x86，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 部署 SKS 到 x86 hygon 双活集群，v1.26 版本 OpenEuler 节点模板上传到目标双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 hygon 双活集群，上传节点文件 v1.25 openEuler x86，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 hygon 双活集群，上传节点文件 v1.27 openEuler x86，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 hygon 双活集群，上传节点文件 v1.29 openEuler x86，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 hygon 双活集群，上传节点文件 v1.25 Rocky OS，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 hygon 双活集群，上传节点文件 v1.26 Rocky OS，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 hygon 双活集群，上传节点文件 v1.28 Rocky OS，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 hygon 双活集群，上传节点文件 v1.30 Rocky OS，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 部署 SKS 到 aarch64 双活集群，v1.26 版本 OpenEuler 节点模板上传到目标双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 aarch64 双活集群，上传节点文件 v1.25 openEuler aarch64，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 aarch64 双活集群，上传节点文件 v1.27 openEuler aarch64，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 aarch64 双活集群，上传节点文件 v1.28 openEuler aarch64，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 aarch64 双活集群，上传节点文件 v1.29 openEuler aarch64，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 aarch64 双活集群，上传节点文件 v1.30 openEuler aarch64，节点模板上传到管控集群的宿主双活集群，虚拟卷副本数 3
            异构上传
                双活 - 模板上传 - 服务部署在 x86 intel 双活集群，已关联 aarch64 双活集群，上传 openEuler aarch64 节点文件，节点模板上传到 aarch64 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 服务部署在 x86 hygon 双活集群，已关联 aarch64 双活集群，上传 openEuler aarch64 节点文件，节点模板上传到 aarch64 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 服务部署在 aarch64 双活集群，已关联 x86 双活集群，上传 x86 节点文件，节点模板上传到 x86 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 服务部署在 aarch64 集群，仅关联 intel x86 双活集群，上传 rocky 节点文件，节点模板上传到 intel x86 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 服务部署在 aarch64 集群，仅关联 intel x86 双活集群，上传 openEuler x86 节点文件，节点模板上传到 intel x86 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 服务部署在 aarch64 集群，仅关联 hygon x86 双活集群，上传 rocky 节点文件，节点模板上传到 hygon x86 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 服务部署在 aarch64 集群，仅关联 hygon x86 双活集群，上传 openEuler x86 节点文件，节点模板上传到 hygon x86 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 服务部署在 aarch64 集群，同时关联 多个x86 双活集群，上传 rocky 节点文件，节点模板上传到第一个可用的 x86 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 服务部署在 aarch64 集群，同时关联 多个x86 双活集群，上传 openEuler 节点文件，节点模板上传到第一个可用的 x86 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 服务部署在 aarch64 集群，先关联 x86 单活集群，再关联 x86 双活集群，上传 x86 节点文件，节点模板上传到 x86 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 服务部署在 aarch64 集群，先关联 x86 单活集群，再关联 x86 双活集群，双活集群失联，上传 x86 节点文件，节点模板上传到 x86 单活集群，虚拟卷副本数 2
                [Deprecated]双活 - 模板上传 - 服务部署在 aarch64 集群，先关联 x86 单活集群，再关联 x86 双活集群，双活集群资源不足，上传 x86 节点文件，节点模板上传到 x86 单活集群，虚拟卷副本数 2
                双活 - 模板上传 - SKS 部署在 aarch64 双活集群，仅关联x86 双活集群到 tower，无 x86 单活集群，上传 x86 节点文件，节点模板上传到 x86 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 服务部署在 x86 双活集群，先关联 aarch64 单活集群，再关联 aarch64 双活集群，上传 aarch64 节点文件，节点模板上传到 aarch64 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - 服务部署在 x86 双活集群，先关联 aarch64 单活集群，再关联 aarch64 双活集群，双活集群失联，上传 aarch64 节点文件，节点模板上传到 aarch64 单活集群，虚拟卷副本数 2
                [Deprecated]双活 - 模板上传 - 服务部署在 x86 双活集群，先关联 aarch64 单活集群，再关联 aarch64 双活集群，双活集群资源不足，上传 aarch64 节点文件，节点模板上传到 aarch64 单活集群，虚拟卷副本数 2
                双活 - 模板上传 - 服务部署在 x86 intel 双活集群，未关联 aarch64 双活集群，上传 openEuler aarch64 节点文件，节点模板上传到第一个可用的 aarch64 单活集群，虚拟卷副本数 2
                双活 - 模板上传 - 服务部署在 x86 hygon 双活集群，未关联 aarch64 双活集群，上传 openEuler aarch64 节点文件，节点模板上传到第一个可用的 aarch64 单活集群，虚拟卷副本数 2
                双活 - 模板上传 - 服务部署在 aarch64 集群，未关联 x 86 双活集群，上传 rocky 节点文件，节点模板上传到第一个可用的 x86 单活集群，虚拟卷副本数 2
                双活 - 模板上传 - 服务部署在 aarch64 集群，未关联 x 86 双活集群，上传 openEuler x86 节点文件，节点模板上传到第一个可用的 x86 单活集群，虚拟卷副本数 2
                双活 - 模板上传 - 服务部署在 aarch64 集群，仅关联版本低于 6.0.0 的 x86 双活集群，上传 rocky 节点文件，节点模板上传到第一个可用的 x86 单活集群，虚拟卷副本数 2
                双活 - 模板上传 - 服务部署在 aarch64 集群，先关联版本低于 6.0.0 的 x86 双活集群，再关联版本高于 6.0.0 的 x86 双活集群，上传 openEuler 节点文件，节点模板上传到版本高于6.0.0的 x86 双活集群，虚拟卷副本数 2
                双活 - 模板上传 - SKS 部署在 aarch64 单活集群，先后关联x86 单活集群和 x86 双活集群到 tower，上传 x86 节点文件，节点模板上传到 x86 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 单活集群，先后关联aarch64 单活集群和 aarch64 双活集群到 tower，上传 aarch64 节点文件，节点模板上传到 aarch64 双活集群，虚拟卷副本数 3
                双活 - 模板上传 - SKS 部署在 x86 单活集群，仅关联aarch64 双活集群到 tower，无 aarch64 单活集群，上传 aarch64 节点文件，节点模板上传到 aarch64 双活集群，虚拟卷副本数 3
            模板分发
                双活 - 模板分发 - x86 双活集群上部署 SKS 生成的模板，可分发到其他 x86 双活集群，分发后副本数为 3
                双活 - 模板分发 - x86 双活集群上部署 SKS 生成的模板，可分发到其他 x86 单活集群，分发后副本数为 3
                双活 - 模板分发 - aarch64 双活集群上部署 SKS 生成的模板，可分发到其他 aarch64 双活集群，分发后副本数为 3
                双活 - 模板分发 - aarch64 双活集群上部署 SKS 生成的模板，可分发到其他 aarch64 单活集群，分发后副本数为 3
                双活 - 模板分发 - x86 单活集群上部署 SKS 生成的模板，可分发到其他 x86 双活集群，分发后副本数为 3
                双活 - 模板分发 - x86 单活集群上部署 SKS 生成的模板，可分发到其他 x86 单活集群，分发后副本数为 2
                双活 - 模板分发 - aarch64 单活集群上部署 SKS 生成的模板，可分发到其他 aarch64 双活集群，分发后副本数为 3
                双活 - 模板分发 - aarch64 单活集群上部署 SKS 生成的模板，可分发到其他 aarch64 单活集群，分发后副本数为 2
                双活 - 模板分发 - 上传到 x86 双活集群生成的模板，可分发到其他 x86 双活集群，分发后副本数为 3
                双活 - 模板分发 - 上传到 x86 双活集群生成的模板，可分发到其他 x86 单活集群，分发后副本数为 3
                双活 - 模板分发 - 上传到 x86 单活集群生成的模板，可分发到其他 x86 双活集群，分发后副本数为 3
                双活 - 模板分发 - 上传到 x86 单活集群生成的模板，可分发到其他 x86 单活集群，分发后副本数为 2
                双活 - 模板分发 - 上传到 aarch64 双活集群生成的模板，可分发到其他 aarch64 双活集群，分发后副本数为 3
                双活 - 模板分发 - 上传到 aarch64 双活集群生成的模板，可分发到其他 aarch64 单活集群，分发后副本数为 3
                双活 - 模板分发 - 上传到 aarch64 单活集群生成的模板，可分发到其他 aarch64 双活集群，分发后副本数为 3
                双活 - 模板分发 - 上传到 aarch64 单活集群生成的模板，可分发到其他 aarch64 单活集群，分发后副本数为 2
            模板删除
                双活 - 节点模板删除 - 上传到双活集群的节点模板可以被删除
                双活 - 节点模板删除 - 上传到双活集群且被双活上工作集群使用的节点模板不能被删除，提示正在使用模板的集群
                双活 - 节点模板删除 - 上传到双活集群，分发后被单活集群中工作集群使用的节点模板不能被删除，提示正在使用模板的集群
                双活 - 节点模板删除 - 上传到双活集群且已被分发到其他双活和单活的集群的节点模板可以被删除
                双活 - 节点模板删除 - 上传到单活集群且已被分发到双活集群的节点模板可以被删除
        服务卸载
            双活 - 服务卸载 - x86 intel - 卸载 SKS 服务，SKS 管控集群虚拟机、SKS registry 虚拟机从双活集群中删除，Tower 中无SKS组件残留
            双活 - 服务卸载 - aarch64 - 卸载 SKS 服务，SKS 管控集群虚拟机、SKS registry 虚拟机从双活集群中删除，Tower 中无SKS组件残留
            双活 - 服务卸载 - x86 hygon - 卸载 SKS 服务，SKS 管控集群虚拟机、SKS registry 虚拟机从双活集群中删除，Tower 中无SKS组件残留
            双活 - 服务卸载 - x86 intel - 部署 SKS registry 未部署 SKS，卸载 SKS registry，capp 卸载成功安装包完成清理，虚拟机删除后移入回收站
            双活 - 服务卸载 - x86 hygon - 部署 SKS registry 未部署 SKS，卸载 SKS registry，capp 卸载成功安装包完成清理，虚拟机删除后移入回收站
            双活 - 服务卸载 - aarch64 - 部署 SKS registry 未部署 SKS，卸载 SKS registry，capp 卸载成功安装包完成清理，虚拟机删除后移入回收站
            双活 - 服务卸载 - x86 intel - 双活集群关闭回收站，部署 SKS registry 未部署 SKS，卸载 SKS registry，capp 卸载成功安装包完成清理，虚拟机被彻底删除
            双活 - 服务卸载 - x86 hygon - 双活集群关闭回收站，部署 SKS registry 未部署 SKS，卸载 SKS registry，capp 卸载成功安装包完成清理，虚拟机被彻底删除
            双活 - 服务卸载 - aarch64 - 双活集群关闭回收站，部署 SKS registry 未部署 SKS，卸载 SKS registry，capp 卸载成功安装包完成清理，虚拟机被彻底删除
        ZBS CSI 接入配置
            双活 - ZBS CSI 接入配置 - UI - 「集群」字段的提示文案修改为「仅支持版本为 5.0.5 及以上的 SMTX OS（ELF） 集群（双活集群要求版本为 6.0.0 及以上）。」
            双活 - ZBS CSI 接入配置 - UI - 「集群」下拉列表显示的集群为双活集群，信息行标注「双活集群」
            双活 - ZBS CSI 接入配置 - 可对双活集群配置 ZBS CSI 接入信息，配置后 ZBS VIP 可成功设置，存储虚拟机网络成功创建
            双活 - ZBS CSI 接入配置 - 可删除为双活集群配置的 ZBS CSI 接入信息，ZBS VIP 被清除，存储虚拟机网络被删除
            双活 - ZBS CSI 接入配置 - 使用 ZBS CSI 接入配置，创建使用 ZBS CSI 的集群，集群创建成功，可以正常创建 PV 使用双活集群存储
        虚拟机工作集群
            双活 - 虚拟机工作集群 - UI - 部署工作集群的集群选框中包含6.0.0及以上版本的双活集群和集群信息（版本、架构、关联ip）
            双活 - 虚拟机工作集群 - UI - 部署工作集群的集群选框中不显示6.0.0以下版本的双活集群
            双活 - 虚拟机工作集群 - UI - 1+4+4集群中优先域不可用，5 CP 选项不可选
            双活 - 虚拟机工作集群 - UI - 集群中部分主机进入离线和维护模式，导致可用主机总计小于 5，5 CP 选项不可选
            双活 - 虚拟机工作集群 - UI - 集群中计算资源不足，导致可用主机总计小于 5，5 CP 选项不可选
            双活 - 虚拟机工作集群 - UI - 「创建位置」字段的提示文案修改为「仅支持版本为 5.0.5 及以上且 CPU 架构与安装文件一致的 SMTX OS（ELF） 集群（双活集群要求版本为 6.0.0 及以上）」
            双活 - 虚拟机工作集群 - UI - 「创建位置」下拉列表显示的集群为双活集群，信息行标注「双活集群」
            双活 - 虚拟机工作集群 - UI - 节点配置 - 双活集群有 GPU，创建集群的节点配置中不显示 GPU 相关配置 UI
            双活 - 虚拟机工作集群 - UI - 虚拟机节点列表和详情页上，点击集群名称，跳转到双活集群页面
            双活 - 虚拟机工作集群 - UI - 虚拟机节点列表和详情页上，点击主机名称，跳转到可用域下的主机页面
            双活 - 虚拟机工作集群 - UI - 虚拟机节点列表和详情页上，点击虚拟机名称，跳转到集群下的对应虚拟机，展开虚拟机详情侧边栏
            双活 - 虚拟机工作集群 - UI - 集群列表中，双活集群上的虚拟机工作集群的 GPU 相关数据列（GPU 数量/GPU 型号）显示为「-」
            双活 - 虚拟机工作集群 - HA 设置 - 6.0.0 及以上版本双活集群上创建的所有工作集群 CP 节点虚拟机的 HA 优先级使用默认值：高
            双活 - 虚拟机工作集群 - 创建 1 CP 工作集群，CP 节点 加入必须放置在不同主机的放置组，部署在优先域
            双活 - 虚拟机工作集群 - 创建 3 CP 工作集群，CP 节点 加入同一个必须放置在不同主机的放置组，部署在优先域不同主机
            双活 - 虚拟机工作集群 - 创建 5 CP 工作集群，CP 节点 加入必须放置在不同主机的放置组，分别在优先域放置 3 节点，次级域放置 2 节点
            双活 - 虚拟机工作集群 - 创建单 worker 节点组多 worker 节点的虚拟机工作集群，worker 节点加入同一个优先放置在不同节点的放置组，实际放置服从 ELF 调度（资源使用均衡的情况下，可调度到不同节点）
            双活 - 虚拟机工作集群 - 创建多 worker 节点组多 worker 节点的虚拟机工作集群，不同节点组的 worker 节点加入不同的优先放置组，同组内优先分散放置，实际放置服从 ELF 调度
            双活 - 虚拟机工作集群 - CP 扩容 - 1 CP 扩容到 3 CP，新增 CP 节点加入已有的放置组，放置在优先域不同主机
            双活 - 虚拟机工作集群 - CP 扩容 - 1 CP 扩容到 5 CP，新增 CP 节点加入已有的放置组，分别在优先域放置 3 节点，次级域放置 2 节点
            双活 - 虚拟机工作集群 - CP 扩容 - 3 CP 扩容到 5 CP，新增 CP 节点加入已有的放置组，超出优先域可用主机数部分放置在次级域
            双活 - 虚拟机工作集群 - CP 缩容 - 5 CP 缩容到 3 CP，减少的 CP 节点为先创建的节点
            双活 - 虚拟机工作集群 - CP 节点替换 - 手动替换 CP 节点组位于优先域主机的节点，节点可替换，替换后的节点仍然放置于优先域
            双活 - 虚拟机工作集群 - CP 节点替换 - 手动替换 CP 节点组位于次级域主机的节点，节点可替换，替换后的节点放置于优先域
            双活 - 虚拟机工作集群 - CP 节点替换 - CP 节点组发生故障自动替换，位于优先域主机的节点，替换后的节点仍然放置于优先域
            双活 - 虚拟机工作集群 - CP 节点替换 - CP 节点组发生故障自动替换，优先域有可放置的主机，位于次级域主机的节点被替换，替换后的节点放置于优先域
            双活 - 虚拟机工作集群 - CP 节点组滚动更新 - 优先域 3 主机可用，升级 1 CP集群触发滚动更新后，CP 节点组中的节点按顺序更新，新 CP 节点在优先域其他节点启动
            双活 - 虚拟机工作集群 - CP 节点组滚动更新 - 优先域 3 主机可用，升级 3 CP 集群触发滚动更新后，CP 节点组中的节点按顺序更新，先更新的 1 CP 节点将调度到次级域
            双活 - 虚拟机工作集群 - CP 节点组滚动更新 - 优先域多于 3 主机可用，升级 3 CP 集群触发滚动更新后，CP 节点组中的节点按顺序更新，新 CP 节点仍然分布在优先域
            双活 - 虚拟机工作集群 - worker 同组扩容 - 同节点组 1 worker 扩容到 多 worker，新增 worker 节点加入已有的放置组，优先分散放置，实际放置主机服从 ELF 调度
            双活 - 虚拟机工作集群 - worker 添加节点组 - 添加一个节点组，创建新放置组，新增 worker 节点加入新的放置组，优先分散放置，实际放置主机服从 ELF 调度
            双活 - 虚拟机工作集群 - worker 添加节点组 - 添加多个节点组，创建多个新放置组，新增 worker 节点分别加入各自节点组对应的放置组，优先分散放置，实际放置主机服从 ELF 调度
            双活 - 虚拟机工作集群 - worker 缩容 - 多个 worker 的节点组缩容，删除缩容量对应的 worker 节点，对应放置组中虚拟机数量更新
            双活 - 虚拟机工作集群 - worker 缩容 - 1 节点组 3 worker节点的集群可缩容至1worker，对应放置组中虚拟机数量更新
            双活 - 虚拟机工作集群 - worker 缩容 - 2 节点组，每节点组 2 worker 节点的集群可删除其中一个节点组缩容至 2worker，对应放置组删除
            双活 - 虚拟机工作集群 - worker 节点组滚动更新 - 单节点组集群 - 升级集群触发滚动更新后，worker 节点组中的节点按顺序更新，优先分散放置，实际放置主机服从 ELF 调度
            双活 - 虚拟机工作集群 - worker 节点组滚动更新 - 多节点组集群 - 升级集群触发滚动更新后，同节点组中的 worker 节点按顺序更新，不同节点组间并行更新，优先分散放置，实际放置主机服从 ELF 调度
            双活 - 虚拟机工作集群 - 编辑 worker 节点组 - 扩容节点存储，可完成 worker 节点虚拟机存储的原地更新扩容
            双活 - 虚拟机工作集群 - worker 节点组自动伸缩 - 节点组配置自动伸缩，增加负载后，节点组可完成自动扩容，新增 worker 节点加入已有的放置组，优先分散放置，实际放置主机服从 ELF 调度
            双活 - 虚拟机工作集群 - worker 节点组自动伸缩 - 节点组配置自动伸缩，减少负载后，节点组可完成自动缩容，删除 worker 节点，对应放置组中虚拟机数量更新
        物理机工作集群
            双活 - 物理机工作集群 - UI - 「Control Plane 节点位置」字段的提示文案修改为「仅支持版本为 5.0.5 及以上且 CPU 架构与安装文件一致的 SMTX OS（ELF） 集群（双活集群要求版本为 6.0.0 及以上）」
            双活 - 物理机工作集群 - UI - 「Control Plane 节点位置」下拉列表显示的集群为双活集群，信息行标注「双活集群」
            [Deprecated] 双活 - 物理机工作集群 - UI - 节点配置 - 节点配置中不显示 GPU 相关配置
            img双活 - 物理机工作集群 - UI - 「Control Plane 节点位置」选择双活集群，出现警告信息「Control Plane 节点可通过双活集群机制在故障后恢复，但物理机节点无法跨站点恢复。」
            双活 - 物理机工作集群 - UI - 「Control Plane 节点位置」选择双活集群，再选择单活集群，警告信息在切换选项后消失
            双活 - 物理机工作集群 - UI - CP 节点列表和详情页上，点击集群名称，跳转到双活集群页面
            双活 - 物理机工作集群 - UI - CP 节点列表和详情页上，点击主机名称，跳转到可用域下的主机页面
            双活 - 物理机工作集群 - UI - CP 节点列表和详情页上，点击虚拟机名称，跳转到集群下的对应虚拟机，展开虚拟机详情侧边栏
            双活 - 物理机工作集群 - 部署 1 + 1 集群，可成功部署并开启插件
            双活 - 物理机工作集群 - 部署 3 + 3 集群，可成功部署并开启插件
            双活 - 物理机工作集群 - 部署 5 + 3 集群，可成功部署并开启插件
            双活 - 物理机工作集群 - 可部署使用 ZBS CSI 的工作集群
            双活 - 物理机工作集群 - HA 设置 - 6.0.0 及以上版本宿主 OS 集群上创建的所有 CP 节点虚拟机的 HA 优先级使用默认值：高
            双活 - 物理机工作集群 - CP 扩容 - 1 CP 扩容到 3 CP，新增 CP 节点加入已有的放置组，放置在优先域不同主机
            双活 - 物理机工作集群 - CP 缩容 - 5 CP 缩容到 3 CP，减少的 CP 节点为先创建的节点
            双活 - 物理机工作集群 - CP 节点替换 - 手动替换 CP 节点组位于优先域主机的节点，节点可替换，替换后的节点仍然放置于优先域 - TBD
            双活 - 物理机工作集群 - CP 节点替换 - 手动替换 CP 节点组位于次级域主机的节点，节点可替换，替换后的节点放置于优先域
            双活 - 物理机工作集群 - CP 节点替换 - CP 节点组发生故障自动替换，位于优先域主机的节点，替换后的节点仍然放置于优先域
            双活 - 物理机工作集群 - CP 节点替换 - CP 节点组发生故障自动替换，优先域有可放置的主机，位于次级域主机的节点被替换，替换后的节点放置于优先域
            双活 - 物理机工作集群 - CP 节点组滚动更新 - 优先域 3 主机可用，升级 3 CP 集群触发滚动更新后，CP 节点组中的节点按顺序更新，先更新的 1 CP 节点将调度到次级域
            双活 - 物理机工作集群 - CP 节点组滚动更新 - 优先域多于 3 主机可用，升级 3 CP 集群触发滚动更新后，CP 节点组中的节点按顺序更新，新 CP 节点仍然分布在优先域
        相关 UI 变更
            img双活 - UI - 创建物理机集群 - 提示「CP 节点可通过双活集群机制在故障后恢复，但物理机节点无法跨站点恢复。」
            img双活 - UI - 节点 - 节点列表新增「所属可用域」列，位于「所属 SMTX OS 集群」后，无交互，可排序，默认不显示，勾选可显示
            双活 - UI - 节点 - 节点列表「所属可用域」列，双活集群虚拟机节点当前所在主机属于优先域，显示「优先可用域」
            双活 - UI - 节点 - 节点列表「所属可用域」列，双活集群虚拟机节点当前所在主机属于次级域，显示「次级可用域」
            双活 - UI - 节点 - 节点列表「所属可用域」列，迁移优先域节点到次级域，显示改变为「次级可用域」
            双活 - UI - 节点 - 节点列表「所属可用域」列，迁移次级域节点到优先域，显示改变为「优先可用域」
            非双活 - UI - 节点 - 节点列表「所属可用域」列，单活集群中虚拟机节点在该列显示「-」
            非双活 - UI - 节点 - 节点列表「所属可用域」列，单活集群中物理机节点在该列显示「-」
            双活 - UI - 节点 - 节点列表「所属可用域」列，双活集群中物理机节点在该列显示「-」
            img双活 - UI - 节点 - 双活集群虚拟机节点的节点详情中增加「所属可用域」显示
            双活 - UI - 节点 - 双活集群虚拟机节点当前所在主机属于优先域，双活集群虚拟机节点的节点详情中「所属可用域」显示「优先可用域」
            双活 - UI - 节点 - 双活集群虚拟机节点当前所在主机属于次级域，双活集群虚拟机节点的节点详情中「所属可用域」显示「次级可用域」
            双活 - UI - 节点 - 双活集群物理机节点的节点详情中不显示「所属可用域」
            非双活 - UI - 节点 - 单活集群虚拟机节点的节点详情中不显示「所属可用域」
            非双活 - UI - 节点 - 单活集群物理机节点的节点详情中不显示「所属可用域」
        CSI  副本数
            img双活 - UI - 存储类资源列表页 UI 增加提示「工作负载集群创建位置为双活集群时，通过系统默认创建的存储类创建的持久卷为 3 副本，若需创建 2 副本持久卷，可自行创建存储类并将冗余策略设置为 2 副本。」，仅双活集群提示，单活集群无该提示
            双活 - UI - 存储类资源列表页 UI 的提示「工作负载集群...冗余策略设置为 2 副本。」提示可手动关闭，再次进入任意集群的存储类页面不再显示该提示
            ELF CSI
                双活 - ELF CSI 默认配置变更 - 向双活集群部署 SKS 服务后，管控集群中生成默认 storageclass 配置副本数为 REPLICA_3_THIN_PROVISION
                双活 - ELF CSI 默认配置变更 - SKS 服务部署在双活，在双活集群创建 ELF CSI 虚拟机工作集群后，工作集群中生成默认 storageclass 配置副本数为 REPLICA_3_THIN_PROVISION
                双活 - ELF CSI 默认配置变更 - SKS 服务部署在单活，向双活集群创建 ELF CSI 虚拟机工作集群后，工作集群中生成默认 storageclass 配置副本数为 REPLICA_3_THIN_PROVISION
                双活 - ELF CSI 默认配置变更 - 在双活集群创建 ELF CSI 虚拟机工作集群中，新建 storageclass，默认不配置副本数，用该 SC 创建出的 PV 使用 3 副本精简策略，PV 资源的yaml 中无副本数对应参数
                双活 - ELF CSI - 创建 SC 时指定副本数为 2，SC 可创建
                双活 - ELF CSI - 创建 SC 时指定副本数为 3，SC 可创建
                双活 - ELF CSI - 删除指定副本数为 2 的 SC，可删除
                双活 - ELF CSI - 删除指定副本数为 3 的 SC，可删除
                双活 - ELF CSI - 使用 副本数为 2 的 SC 创建 PVC，无法成功创建 PV，后端有报错 ELF_STORAGE_POLICY_NOT_FOUND
                非双活 - 管控集群组件配置变更 - 向单活集群部署 SKS 服务后，管控集群中生成默认 storageclass 配置副本数为 REPLICA_2_THIN_PROVISION
                非双活 - ELF CSI 默认配置变更 - 在单活集群创建 ELF CSI 虚拟机工作集群后，工作集群中生成默认 storageclass 配置副本数为 REPLICA_2_THIN_PROVISION
                非双活 - ELF CSI 缺省值 - 在单活集群创建 ELF CSI 虚拟机工作集群中，新建 storageclass，默认不配置副本数，用该 SC 创建出的 PV 使用 2 副本精简策略
                非双活 - ELF CSI - 创建 SC 时指定副本数为 2，SC 可创建
                非双活 - ELF CSI - 创建 SC 时指定副本数为 3，SC 可创建
                非双活 - ELF CSI - 删除指定副本数为 2 的 SC，可删除
                非双活 - ELF CSI - 删除指定副本数为 3 的 SC，可删除
                非双活 - ELF CSI - 使用副本数为 2 的 SC 创建 PVC，可成功创建 PV，对应虚拟卷为 2 副本
                非双活 - ELF CSI - 使用副本数为 3 的 SC 创建 PVC，可成功创建 PV，对应虚拟卷为 3 副本
                非双活 - 升级 - ELF CSI 缺省值 - 1.5 之前版本创建的 ELF CSI 虚拟机工作集群，升级到 1.5 后，用原有 SC 新创建出的 PV 仍使用 2 副本数精简策略
                非双活 - 升级 - ELF CSI 缺省值 - 1.5 之前版本创建的 ELF CSI 虚拟机工作集群，升级到 1.5 后，扩容原有 SC 创建出的 PV，可完成扩容，副本数保持 2
                非双活 - 升级 - ELF CSI 缺省值 - 1.5 之前版本创建的 ELF CSI 虚拟机工作集群，升级到 1.5 后，克隆原有 SC 创建出的 PV，可完成克隆，副本数保持 2
                非双活 - 升级 - ELF CSI 缺省值 - 1.5 之前版本创建的 ELF CSI 虚拟机工作集群，升级到 1.5 后，对原有 SC 创建出的 PV 打快照并重建，可完成重建，副本数保持 2
            ZBS CSI
                双活 - ZBS CSI 默认配置变更 - 在双活集群创建 ZBS CSI 虚拟机工作集群后，工作集群中生成默认 storageclass 配置副本数为 3
                双活 - ZBS CSI 默认配置变更 - SKS 服务部署在双活，在双活集群创建 ZBS CSI 虚拟机工作集群后，工作集群中生成默认 storageclass 配置副本数为 3
                双活 - ZBS CSI 默认配置变更 - SKS 服务部署在单活，在双活集群创建 ZBS CSI 虚拟机工作集群后，工作集群中生成默认 storageclass 配置副本数为 3
                双活 - ZBS CSI 默认配置变更 - 在双活集群创建 ZBS CSI 虚拟机工作集群中，新建 storageclass，默认不配置副本数，用该 SC 创建出的 PV 使用 3 副本精简策略， PV 资源的yaml中无副本数相关参数
                双活 - ZBS CSI - 创建 SC 时指定副本数为 2，SC 可创建
                双活 - ZBS CSI - 创建 SC 时指定副本数为 3，SC 可创建
                双活 - ZBS CSI - 删除指定副本数为 2 的 SC，可删除
                双活 - ZBS CSI - 删除指定副本数为 3 的 SC，可删除
                双活 - ZBS CSI - 双活上的工作集群，挂载本集群存储，使用副本数为 2 的 SC 创建 PVC，无法成功创建 PV，后端有报错：Cannot set replica num to 2 in stretched cluster
                双活 - ZBS CSI - 双活上的工作集群，挂载本集群存储，使用自创建副本数未配置的 SC 创建 PVC，因识别 KSC 宿主OS 集群为双活，副本数缺省为 3，可成功创建 PV
                双活 - ZBS CSI - 双活上的工作集群，挂载单活集群存储，使用副本数为 2 的 SC 创建 PVC，可成功创建 PV
                双活 - ZBS CSI - 双活上的工作集群，挂载单活集群存储，使用默认 的 SC 创建 PVC，可成功创建 PV，副本数为 3
                非双活 - ZBS CSI 默认配置变更 - 在单活集群创建 ZBS CSI 虚拟机工作集群后，工作集群中生成默认 storageclass 配置副本数为 2
                非双活 - ZBS CSI 缺省值不变 - 在单活集群创建 ZBS CSI 虚拟机工作集群中，新建 storageclass，默认不配置副本数，用该 SC 创建出的 PV 使用 2 副本精简策略
                非双活 - ZBS CSI - 创建 SC 时指定副本数为 2，SC 可创建
                非双活 - ZBS CSI - 创建 SC 时指定副本数为 3，SC 可创建
                非双活 - ZBS CSI - 删除指定副本数为 2 的 SC，可删除
                非双活 - ZBS CSI - 删除指定副本数为 3 的 SC，可删除
                非双活 - ZBS CSI - 单活上的工作集群，挂载本集群存储，使用副本数为 2 的 SC 创建 PVC，可成功创建 PV
                非双活 - ZBS CSI - 单活上的工作集群，挂载本集群存储，使用副本数为 3 的 SC 创建 PVC，可成功创建 PV
                非双活 - ZBS CSI - 单活上的工作集群，挂载其他单活集群存储，使用副本数为 2 的 SC 创建 PVC，可成功创建 PV
                非双活 - ZBS CSI - 单活上的工作集群，挂载其他单活集群存储，使用副本数为 3 的 SC 创建 PVC，可成功创建 PV
                非双活 - 升级 - ZBS CSI 缺省值不变 - 1.5 之前版本创建的 ZBS CSI 虚拟机工作集群，升级到 1.5 后，用原有 SC 新创建出的 PV 使用 2 副本数精简策略
                非双活 - 升级 - ZBS CSI 缺省值不变 - 1.5 之前版本创建的 ZBS CSI 虚拟机工作集群，升级到 1.5 后，扩容原有 SC 创建出的 PV，可完成扩容，副本数保持 2
                非双活 - 升级 - ZBS CSI 缺省值不变 - 1.5 之前版本创建的 ZBS CSI 虚拟机工作集群，升级到 1.5 后，克隆原有 SC 创建出的 PV，可完成克隆，副本数保持 2
                非双活 - 升级 - ZBS CSI 缺省值不变 - 1.5 之前版本创建的 ZBS CSI 虚拟机工作集群，升级到 1.5 后，对原有 SC 创建出的 PV 打快照并重建，可完成重建，副本数保持 2
        双活环境集群通用功能检查
            双活 - 服务部署(SKS) - 使用 IP Pool 可部署
            双活 - 服务部署(SKS) - 手动指定 VIP 可部署
            双活 - 服务部署(SKS) - 时区设置有效，且所有工作集群默认沿用管控集群的时区
            双活 - 服务部署(SKS) - 部署后可关联 OBS 1.4.1，开启监控、报警、日志、审计
            双活 - 虚拟机工作集群 - 可部署配置 EIC CNI 的工作集群
            暂时不用）双活 - 虚拟机工作集群 - 可部署配置 ER CNI 的工作集群
            双活 - 虚拟机工作集群 - 可关联 OBS 1.4.1，开启监控、报警、日志、审计
            双活 - 物理机工作集群 - 可部署不配置 CSI 的工作集群
            双活 - 物理机工作集群 - 可关联 OBS 1.4.1，开启监控、报警、日志、审计
            虚拟机集群
                双活 - 虚拟机工作集群 - 部署 1 + 1 集群，可成功部署并开启插件
                双活 - 虚拟机工作集群 - 部署 3 + 3 集群，可成功部署并开启插件
                双活 - 虚拟机工作集群 - 部署 5 + 3 集群，可成功部署并开启插件
                双活 - 虚拟机工作集群 - 可部署使用 ELF CSI 的工作集群
                双活 - 虚拟机工作集群 - 可部署使用 ZBS CSI 通过存储网络接入宿主集群存储的工作集群
                双活 - 虚拟机工作集群 - 可部署使用 ZBS CSI 通过接入网络接入单活 ZBS 集群存储的工作集群
                双活 - 虚拟机工作集群 - 可部署使用 ZBS CSI 通过接入网络接入双活 ZBS 集群存储的工作集群
                双活 - 虚拟机工作集群 - 可部署使用 Calico CNI 的工作集群
                双活 - 虚拟机工作集群 - 可部署使用 EIC CNI 的工作集群
                双活 - 虚拟机工作集群 - 可部署多个节点组的工作集群
                双活 - 虚拟机工作集群 - 配置故障自动替换，注入节点故障，可触发并完成自动替换
                双活 - 虚拟机工作集群 - 可完成 worker 节点的手动替换
                双活 - 虚拟机工作集群 - 可创建 v1.25 Rocky OS 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.26 Rocky OS 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.27 Rocky OS 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.28 Rocky OS 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.29 Rocky OS 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.30 Rocky OS 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.25 openEuler x86 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.26 openEuler x86 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.27 openEuler x86 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.28 openEuler x86 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.29 openEuler x86 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.30 openEuler x86 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.25 openEuler aarch64 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.26 openEuler aarch64 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.27 openEuler aarch64 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.28 openEuler aarch64 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.29 openEuler aarch64 工作集群
                双活 - 虚拟机工作集群 - 可创建 v1.30 openEuler aarch64 工作集群
                双活 - 虚拟机工作集群 - x86 可升级集群 K8s 版本：1.25 -> 1.26
                双活 - 虚拟机工作集群 - x86 可升级集群 K8s 版本：1.26 -> 1.27
                双活 - 虚拟机工作集群 - x86 可升级集群 K8s 版本：1.27 -> 1.28
                双活 - 虚拟机工作集群 - x86 可升级集群 K8s 版本：1.28 -> 1.29
                双活 - 虚拟机工作集群 - x86 可升级集群 K8s 版本：1.29 -> 1.30
                双活 - 虚拟机工作集群 - aarch64 可升级集群 K8s 版本：1.25 -> 1.26
                双活 - 虚拟机工作集群 - aarch64 可升级集群 K8s 版本：1.26 -> 1.27
                双活 - 虚拟机工作集群 - aarch64 可升级集群 K8s 版本：1.27 -> 1.28
                双活 - 虚拟机工作集群 - aarch64 可升级集群 K8s 版本：1.28 -> 1.29
                双活 - 虚拟机工作集群 - aarch64 可升级集群 K8s 版本：1.29 -> 1.30
            物理机集群
                双活 - 物理机工作集群 - 可使用 rocky 8.10 x86 物理机创建工作集群
                双活 - 物理机工作集群 - 可使用 rocky 8.9 x86 物理机创建工作集群
                双活 - 物理机工作集群 - 可使用 openEuler 22.03 sp2 x86 物理机创建工作集群
                双活 - 物理机工作集群 - 可使用 openEuler 22.03 sp2 aarch64 物理机创建工作集群
                双活 - 物理机工作集群 - 可使用 openEuler 22.03 sp3 x86 物理机创建工作集群
                双活 - 物理机工作集群 - 可使用 openEuler 22.03 sp3 aarch64 物理机创建工作集群
                双活 - 物理机工作集群 - 可使用 ubuntu 22.04.3 x86 物理机创建工作集群
                双活 - 物理机工作集群 - 可使用 kylin v10 sp2 x86 物理机创建工作集群
                双活 - 物理机工作集群 - 可使用 kylin v10 sp2 aarch64 物理机创建工作集群
                双活 - 物理机工作集群 - 可使用 kylin v10 sp3 2403 x86 物理机创建工作集群
                双活 - 物理机工作集群 - 可使用 kylin v10 sp3 2403 aarch64 物理机创建工作集群
        相关组件功能
            双活 - ZBS PROXY - 删除工作负载集群，使用 ZBS CSI 连接双活的 ZBS 存储，用户创建的 PV 对应的存储对象可完成清理
        混合集群类型交叉使用场景
            双活 - 双活服务 - 向单活集群创建虚拟机工作集群，集群可成功创建
            双活 - 双活服务 - 向单活集群创建物理机工作集群，集群可成功创建
            双活 - 非双活服务 - 向双活集群创建虚拟机工作集群，集群可成功创建
            双活 - 非双活服务 - 向双活集群创建物理机工作集群，集群可成功创建
            Tower 位置关系
                双活 - Tower 在双活集群 - SKS 部署在双活集群 - 工作集群创建在双活集群
                双活 - Tower 在双活集群 - SKS 部署在双活集群 - 工作集群创建在单活集群
                双活 - Tower 在双活集群 - SKS 部署在单活集群 - 工作集群创建在双活集群
                双活 - Tower 在双活集群 - SKS 部署在单活集群 - 工作集群创建在单活集群
                双活 - Tower 在单活集群 - SKS 部署在双活集群 - 工作集群创建在双活集群
                双活 - Tower 在单活集群 - SKS 部署在双活集群 - 工作集群创建在单活集群
                双活 - Tower 在单活集群 - SKS 部署在单活集群 - 工作集群创建在双活集群
                双活 - Tower 在单活集群 - SKS 部署在单活集群 - 工作集群创建在单活集群
        异常场景
            双活 - 异常 - Registry 所在优先域主机异常 - 如优先域资源较次级域空闲，Registry 可 HA 到优先域
            双活 - 异常 - Registry 所在优先域主机异常 - 如优先域资源紧张，Registry 可 HA 到次级域
            双活 - 异常 - 优先域部分主机故障 - 2 min内触发 HA，HA 目标主机服从 ELF 调度，不一定在优先域
            双活 - 异常 - 优先域故障 - 2 min内触发 HA，次级域资源充足的情况下，所有集群 VM 在次级域恢复
            双活 - 异常 - 优先域故障 - 2 min内触发 HA，次级域资源不足的情况下，仅部分 VM 可在次级域恢复
            双活 - 异常 - 优先域故障 - 全域故障的情况下，SKS 高可用模式服务未关联 OBS 的情况下，集群恢复的时间在 30 分钟以内
            双活 - 异常 - 优先域故障 - 全域故障的情况下，SKS 6节点工作负载集群已关联 OBS 的情况下，集群恢复的时间在 30 分钟以内
            双活 - 异常 - 优先域故障 - 全域故障的情况下，SKS 高可用模式服务已关联 OBS 的情况下，集群恢复的时间在 30 分钟以内
            双活 - 异常 - 优先域故障 - 全域故障且次级域资源不足以承接优先域所有虚拟机 HA 时，SKS 服务虚拟机可优先于其他集群虚拟机在次级域恢复- 实测：并不能，都是HA优先级「高」的情况下顺序不定
            双活 - 异常 - 次级域部分主机故障 - 2 min内触发 HA，HA 目标主机服从 ELF 调度，不一定在次级域
            双活 - 异常 - 次级域故障 - 2 min内触发 HA，优先域资源充足的情况下，所有集群 VM 在优先域恢复
            双活 - 异常 - 虚拟机节点关机重启，集群可恢复
        其他场景
            双活 - 维护模式 - 优先域主机进入维护模式，其上的虚拟机节点可正常迁移并在退出维护模式后成功回迁
            双活 - 维护模式 - 次级域主机进入维护模式，其上的虚拟机节点可正常迁移并在退出维护模式后成功回迁
            双活 - DRS - 集群开启 DRS，调度策略执行后依然遵循节点虚拟机放置原则
        补充需求 - 双活的自动故障替换时间更改
            双活 - 创建虚拟机集群 - CP 节点组故障自动替换的默认故障判定时间默认为 11 min
            双活 - 创建虚拟机集群 - worker 节点组故障自动替换的默认故障判定时间默认为 11 min
            双活 - 创建物理机集群 - CP 节点组故障自动替换的默认故障判定时间默认为 11 min
            双活 - 编辑 CP 节点组 - 开启 CP 节点组故障自动替换，默认故障判定时间默认为 11 min
            双活 - 编辑 worker 节点组 - 开启 worker 节点组故障自动替换，默认故障判定时间默认为 11 min
            双活 - 编辑节点组 - 开启节点组故障自动替换，修改故障判定时间保存，故障判定时间可生效
            非双活 - 创建虚拟机集群 - worker 节点组故障自动替换的默认故障判定时间默认仍然为 5 min
            非双活 - 创建物理机集群 - CP 节点组故障自动替换的默认故障判定时间默认仍然为 5 min
            非双活 - 编辑 CP 节点组 - CP 节点组故障自动替换的默认故障判定时间默认仍然为 5 min
        非双活集群影响
            非双活 - 服务部署(Registry) - 6.0.x 及以上版本 OS 上部署完成的 SKS registry 虚拟机 HA 优先级为默认值：中
            非双活 - 服务部署(Registry) - Registry 虚拟机受新版本 capp 管控，统一使用 2 副本精简策略
            非双活 - 服务部署(SKS) - 产生管控集群 CP 和 worker 虚拟机仍然使用 2 副本精简策略
            非双活 - 服务升级(SKS) - 升级 SKS 完成后，管控集群 CP 和 worker 虚拟机及挂载的虚拟卷仍然使用 2 副本精简策略
            非双活 - 服务部署(SKS) - HA 设置 - 6.0.0 及以上版本宿主 OS 集群上SKS 可正常部署，部署的服务虚拟机 HA 优先级为默认值：中
            非双活 - 服务部署(SKS) - HA 设置 - 6.0.0 以下版本宿主 OS 集群上SKS 可正常部署，部署的服务虚拟机无 HA 优先级设置
            非双活 - 虚拟机工作集群 - worker 缩容 - 多个 worker 的节点组缩容，删除缩容量对应的 worker 节点，对应放置组中虚拟机数量更新
            非双活 - 虚拟机工作集群 - worker 缩容 - 1 节点组 3 worker节点的集群可缩容至1worker，对应放置组中虚拟机数量更新
            非双活 - 虚拟机工作集群 - worker 缩容 - 2 节点组，每节点组 2 worker 节点的集群可删除其中一个节点组缩容至 2worker，对应放置组删除
            非双活 - 虚拟机工作集群 - worker 缩容 - 升级到1.5环境中的使用旧日志的工作集群，工作节点数不小于 3，编辑节点组缩容，不允许缩容到 3 节点以下
            非双活 - 虚拟机工作集群 - worker 缩容 - 升级到1.5环境中的使用旧日志的工作集群，工作节点数不小于 3，删除节点组缩容，不允许缩容到 3 节点以下
            非双活 - 虚拟机工作集群 - worker 缩容 - 升级到1.5环境中的使用旧日志的工作集群，工作节点数不小于 3，切换日志到obs 后，编辑节点组缩容，可缩容到 3 节点以下
            非双活 - 虚拟机工作集群 - worker 缩容 - 升级到1.5环境中的使用旧日志的工作集群，工作节点数不小于 3，切换日志到obs 后，删除节点组缩容，可缩容到 3 节点以下
            非双活 - 虚拟机工作集群 - worker 缩容 - 升级到1.5环境中的使用旧日志的工作集群，工作节点数不小于 3，关闭日志插件，编辑节点组缩容，可缩容到 3 节点以下
            非双活 - 虚拟机工作集群 - worker 缩容 - 升级到1.5环境中的使用旧日志的工作集群，工作节点数不小于 3，关闭日志插件，删除节点组缩容，可缩容到 3 节点以下
            非双活 - 虚拟机工作集群 - 滚动升级 - 使用新的 1.5 模板升级 ELF CSI 集群，滚动完成后，CP 和 worker 虚拟机虚拟卷仍使用 2 副本精简策略
            非双活 - 虚拟机工作集群 - 滚动升级 - 使用新的 1.5 模板升级 ELF CSI 集群，滚动完成后，原有存量 PV 仍然为 2 副本
            非双活 - 虚拟机工作集群 - 滚动升级 - 使用新的 1.5 模板升级 ELF CSI 集群，滚动完成后，使用默认 sc 新创建的 PV 仍为 2 副本
            非双活 - 物理机工作集群 - 滚动升级 - 使用新的 1.5 模板升级 ZBS CSI 集群，滚动完成后，CP 节点虚拟机虚拟卷仍使用 2 副本精简策略
            非双活 - 物理机工作集群 - 滚动升级 - 使用新的 1.5 模板升级 ZBS CSI 集群，滚动完成后，原有存量 PV 仍然为 2 副本
            非双活 - 物理机工作集群 - 滚动升级 - 使用新的 1.5 模板升级 ZBS CSI 集群，滚动完成后，使用默认 sc 新创建的 PV 仍为 2 副本
            节点虚拟机副本数调整
                非双活 - 虚拟机工作集群 - 可创建 v1.25 Rocky OS 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.26 Rocky OS 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.27 Rocky OS 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.28 Rocky OS 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.29 Rocky OS 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.30 Rocky OS 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.25 openEuler x86 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.26 openEuler x86 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.27 openEuler x86 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.28 openEuler x86 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.29 openEuler x86 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.30 openEuler x86 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.25 openEuler aarch64 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.26 openEuler aarch64 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.27 openEuler aarch64 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.28 openEuler aarch64 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.29 openEuler aarch64 工作集群，节点虚拟机虚拟卷副本数为 2
                非双活 - 虚拟机工作集群 - 可创建 v1.30 openEuler aarch64 工作集群，节点虚拟机虚拟卷副本数为 2
        补充需求 - 单活转双活场景验证
            SKS 服务
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - SKS registry 虚拟机状态正常，虚拟卷副本数提升为 3 副本
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - SKS 服务状态正常，节点虚拟机及挂载的 PV 副本数均提升为 3 副本
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 管控集群默认 SC 副本数配置变为 3 副本，开关 OBS 关联，可成功创建/销毁 PV
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 转换完成后，管控集群 spec.elfClusterType 字段值更新为 "stretched"
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 转换完成后，管控集群 node label 增加 cape.infrastructure.cluster.x-k8s.io/zone-id 和 zone-type 信息
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 转换完成后，服务可卸载，服务虚拟机及存储资源可清理
            创建新的工作负载集群
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 可成功创建新的使用 ELF CSI 的工作负载集群
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 可成功创建新的使用 ZBS CSI 的工作负载集群
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 可成功创建新的使用 EIC CNI 的工作负载集群
            虚拟机集群
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 转换完成后，虚拟机工作集群所有 node label 增加 cape.infrastructure.cluster.x-k8s.io/zone-id 和 zone-type 信息
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 转换完成后，虚拟机工作集群所有节点的 elfmachine 对象 status 添加对应的 zone 信息
                ELF CSI
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ELF CSI 的虚拟机集群 spec.elfClusterType 字段值更新为 "stretched"
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ELF CSI 的虚拟机集群的所有节点虚拟机虚拟卷副本数均提升为 3 副本
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ELF CSI 开启了全部插件的虚拟机集群状态正常
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ELF CSI 的虚拟机集群关闭监控插件重新开启可正常工作
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ELF CSI 的虚拟机集群可完成节点替换
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ELF CSI 的虚拟机集群可完成节点扩容
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ELF CSI 的虚拟机集群可完成新的 PV 创建，新 PV 副本数为 3
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ELF CSI 的虚拟机集群可完成已有 PV 扩容
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ELF CSI 的虚拟机集群可完成 K8s 版本升级
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - ELF CSI 集群默认 SC storagePolicy 配置变为 REPLICA_3_THIN_PROVISION
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - ELF CSI 集群使用默认 SC 创建出的 PV 副本数为 3 副本
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - ELF CSI 集群已创建的用户自定义 SC 的 storagePolicy 配置保持 REPLICA_2_THIN_PROVISION - 需要手动替换原有默认 SC 为3副本配置，替换后可创建新的持久卷 - TBD 这里需要验证的除了创建还需不需要有别的操作？比如：克隆和快照重建
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - ELF CSI 集群已创建的用户自定义 PV 对应的 storagePolicy 配置保持 REPLICA_2_THIN_PROVISION
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - ELF CSI 集群已创建的用户自定义 PV 对应的实际虚拟卷变更为 3 副本
                ZBS CSI
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ZBS CSI 的虚拟机集群 spec.elfClusterType 字段值更新为 "stretched"
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ZBS CSI 的虚拟机集群的所有节点虚拟机虚拟卷副本数均提升为 3 副本
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ZBS CSI 开启了全部插件的虚拟机集群状态正常
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ZBS CSI 的虚拟机集群关闭监控插件重新开启可正常工作
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ZBS CSI 的虚拟机集群可完成节点替换
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ZBS CSI 的虚拟机集群可完成节点扩容
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ZBS CSI 的虚拟机集群可完成新的 PV 创建，使用默认 SC 新创建出的 PV replicaFactor 配置为3， 实际副本数也为 3
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ZBS CSI 的虚拟机集群，可完成已有 PV 扩容
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 使用 ZBS CSI 的虚拟机集群可完成 K8s 版本升级
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - ZBS CSI 集群默认 SC 副本数配置变为 3 副本
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - ZBS CSI 集群使用默认 SC 创建出的原有 PV 的 replicaFactor 配置仍为 2
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - ZBS CSI 集群已创建的用户自定义 SC 中无显式副本数配置则自动适应为3副本
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - ZBS CSI 集群使用本集群存储创建的用户自定义 PV 对应的虚拟卷实际副本数变更为 3
                    单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - ZBS CSI 集群使用其他集群存储创建的用户自定义 PV 对应的虚拟卷保持 2 副本不变
            物理机集群
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 未配置 CSI 的物理机集群的 spec.elfClusterType 字段值更新为 "stretched"
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 配置了 ZBS CSI 的物理机集群的 spec.elfClusterType 字段值更新为 "stretched"
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 转换完成后，物理机工作集群所有 CP 节点 node label 增加 cape.infrastructure.cluster.x-k8s.io/zone-id 和 zone-type 信息，worker 节点不变
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 转换完成后，物理机工作集群所有 CP 节点 elfmachine 对象 status 添加对应的 zone 信息，worker 节点不变
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 物理机集群的所有 CP 节点虚拟机虚拟卷副本数均提升为 3 副本
                单活转双活 - 所有相关虚拟机宿主 OS（包括 Tower）转双活 - 可创建新的物理机工作负载集群
            其他
                单活转双活 - 转换完成后，存储在该 OS 集群中的节点模板虚拟卷副本数仍为 2，但不影响新建节点
                单活转双活 - 转换完成后，服务虚拟机 HA 优先级「中」不变
                单活转双活 - 转换完成后，工作集群虚拟机 HA 优先级「中」不变
                单活转双活 - 仅工作集群虚拟机宿主转双活 - 工作集群状态正常
                单活转双活 - 工作集群使用 ZBS CSI 对接的存储集群转双活 - 我们目前处理这种情况吗？- 需手动处理 addon 配置后适配
    多租户
        资源配额
            项目资源配额
                创建项目
                    创建项目 - 创建弹窗新增项目配额/默认容器配额，查看UI弹窗及文案展示
                    创建项目 - 默认不配置保存，不受配额限制，不创建ClusterResourceQuota且不产生事件
                    创建项目 - CPU请求/CPU限制，默认单位 core，允许切换为m
                    创建项目 - CPU请求/CPU限制，输入值校验 - 仅允许输入大于等于0的整数，为0时表示禁用
                    创建项目 - CPU请求/CPU限制，输入值校验 - 请求值大于限制时，报错「资源请求不能超过资源限制」
                    创建项目 - CPU请求/CPU限制，输入值校验 - 当所有项目中输入值总和大于集群总和时，允许保存
                    创建项目 - 内存请求/内存限制，默认单位 GiB，允许切换为MiB/TiB
                    创建项目 - 内存请求/内存限制，输入值校验 - 仅允许输入大于等于0的整数，为0时表示禁用
                    创建项目 - 内存请求/内存限制，输入值校验 - 请求值大于限制时，报错「资源请求不能超过资源限制」
                    创建项目 - 内存请求/内存限制，输入值校验 - 当所有项目中输入值总和大于集群总和时，允许保存
                    创建项目 - 持久卷申领，默认单位 GiB，允许切换为MiB/TiB
                    创建项目 - 持久卷申领，输入值校验 - 仅允许输入大于等于0的整数，为0时表示禁用
                    创建项目 - 持久卷申领，输入值校验 - 无数值上限，超过csi所在集群存储，可保存
                    创建项目 - GPU数量，输入值校验 - 仅允许输入大于等于0的整数，为0时表示表示禁用
                    创建项目 - GPU数量，输入值校验 - 无数值上限，输入超过宿主所挂载GPU数量，可保存
                    创建项目 - 创建时关联已存在资源的ns，ns下资源已使用超过资源分配-可保存，无提示，无法创建新资源
                    创建项目 - 设置项目配额，保存成功，查看ClusterResourceQuota资源，参数正确
                    创建项目 - 设置项目配额，保存成功，查看项目列表展示
                    创建项目 - 创建成功后，在项目下ns创建新资源，受资源配额限制，当超过时阻止创建
                编辑项目
                    编辑项目 - System项目，编辑弹窗无配额项，仅关联ns和成员
                    编辑项目 - 创建项目时，关联ns资源使用量已大于配置的资源限制，编辑弹窗中展示notice tip，可保存成功，ClusterResourceQuota不更新
                    编辑项目 - 创建项目时，配置的资源配额大于已使用，缩小配额但依旧大于已使用，编辑弹窗中依旧展示notice tip，可保存成功，ClusterResourceQuota更新
                    编辑项目 - 创建项目时，配置的资源配额大于已使用，缩小配额小于已使用，不展示notice tip，可保存成功，ClusterResourceQuota更新
                    编辑项目 - 创建项目时，不设置资源配额，编辑弹窗中设置配额，配额值小于已使用，不展示notice tip，可保存成功，创建ClusterResourceQuota
                    编辑项目 - 创建项目时，不设置资源配额，编辑弹窗中设置配额，配额值大于已使用，可保存成功，创建ClusterResourceQuota
                    编辑项目 - 编辑未使用配额的项目，设置资源配置值小于0，不应该展示notice tip，无法保存成功
                    编辑项目 - 编辑资源配额大于集群资源，可保存成功，ClusterResourceQuota更新
                    编辑项目 - 编辑后资源配额小于已使用，阻止新创建资源
                    编辑项目 - 编辑前资源配额小于已使用，新创建资源被阻止，编辑配额到满足新创建资源需求，保存后新资源创建成功
                    编辑项目 - 编辑前资源配额小于已使用，新创建资源被阻止，编辑配额大于已使用但不满足新创建资源需求，保存后新资源依旧阻止创建
                    编辑项目 - 编辑入口及弹窗 - 从项目列表morebutton编辑，编辑后查看更新
                    编辑项目 - 编辑入口及弹窗 - 从项目详情morebutton编辑，编辑后查看详情更新
                    编辑项目 - 创建时设置资源配额，清空所有项目配额，保存成功，ClusterResourceQuota资源清空，ns资源不再受资源配额限制
                删除项目
                    删除项目 - System项目，morebutton新增删除按钮，禁用状态，hover tip「不支持删除」
                    删除项目 - 不配置资源配额，删除项目与1.4保持一致
                    删除项目 - 配置资源配额，删除项目同时删除ns，删除成功后，ns下所有资源删除，ClusterResourceQuota删除
                    删除项目 - 配置资源配额，删除项目不删除ns，删除成功后，ClusterResourceQuota删除，ns下资源正常
                    删除项目 - 配置资源配额，删除项目不删除ns，删除前由于已分配资源大于配额值阻止了ns资源创建，删除后ns资源创建成功
                    删除项目 - 入口 - 从项目列表morebutton删除，删除后列表删除
                    删除项目 - 入口 - 从项目详情morebutton删除，删除后回退到列表
                项目详情
                    项目详情 - System项目，不展示资源配额及默认容器配额，仅展示基本信息
                    项目详情 - 基本信息展示，使用量从监控获取，与列表展示一致
                    项目详情 - 默认容器配额，与配置内容一致，根据配置变更更新
                    项目详情 - 项目配额，配额值与ClusterResourceQuota内容一致，根据配置及资源分配变更更新
                    项目详情 - 项目配额，已分配title，hover时tooltip提示「资源对象申请占用的配额数量」
                    项目详情 - 项目配额，当不配置任何资源配额时（即未创建ClusterResourceQuota），查看列表展示 - 配额均为「不限」，已分配和使用率展示为空
                    项目详情 - 项目配额，当配置资源配额为0时，查看列表展示 - 配额展示为「0+单位」，已分配「数值或 -」，使用率柱形图填充为红色，数值为「-」
                    项目详情 - 项目配额，当单个资源类型不配置配额（创建ClusterResourceQuota，但无该字段配置），查看列表展示 - 配额为「不限」，已分配和使用率展示为空
                    项目详情 - 项目配额，有配置配额，但无资源创建或未关联ns，查看列表展示 - 已分配和使用率展示为0
                    项目详情 - 项目配额，有设置配额，使用率（0 < X < 80）时，样式展示
                    项目详情 - 项目配额，有设置配额，使用率（80 ≤ X < 90）时，样式展示
                    项目详情 - 项目配额，有设置配额，使用率（X ≥ 90）时，样式展示
                    项目详情 - 项目配额，有设置配额，使用率（X = 0）时，样式展示
                    项目详情 - 项目配额，有设置配额，使用率计算百分比与ClusterResourceQuota.status.used中对应计算值百分比一致
                    项目详情 - 项目状态 - 展示与列表一致 「活跃/删除中」
                    名字空间
                        项目详情 - 名字空间，切换名字空间展示，与名字空间资源列表字段展示一致，无所属项目
                        项目详情 - 名字空间，创建项目时不选择名字空间，列表展示为空
                        项目详情 - 名字空间，创建项目时选择名字空间，列表展示所属项目下的名字空间
                        项目详情 - 名字空间，编辑项目时新增或删除名字空间，列表展示所属项目下的名字空间更新
                        项目详情 - 名字空间，在名字空间资源列表删除，列表展示对应ns状态「删除中」，删除成功后列表删除
                        项目详情 - 名字空间 ，morebutton「编辑名字空间配额」，操作与名字空间页面一致
                        项目详情 - 名字空间 ，morebutton「解除关联」，点击后直接从项目移除该ns，并toast反馈
                        项目详情 - 名字空间 - 解除关联ns，解除后，项目详情中对应资源信息更新
                        项目详情 - 名字空间 - 支持跳转，hover至名称时变蓝，点击跳转至名字空间详情页
                        项目详情 -名字空间 - System项目详情名字空间列表，morebutton-不允许编辑名字空间配额，不允许解除关联
                    成员
                        项目详情 - 成员，切换成员展示，与成员资源列表字段展示一致，无所属项目
                        项目详情 - 成员，创建项目时不关联成员，列表展示为空
                        项目详情 - 成员，创建项目时关联成员，列表展示所属项目下的成员，所展示角色为「项目内的角色」
                        项目详情 - 成员，编辑项目时关联或解除成员，列表展示所属项目下的成员更新
                        项目详情 - 成员 ，morebutton「解除关联」，点击后直接从项目删除成员，并toast反馈
                        项目详情 - 成员，解除关联成员后，删除RoleBinding，成员列表删除用户角色或用户
                        项目详情 - 成员，从成员页面列表添加成员关联该项目，保存后详情成员列表更新
                        项目详情 - 成员，从成员页面列表删除成员，保存后详情成员列表删除
                        项目详情 - 成员，对应用户角色变更导致的删除，更新同步后，项目详情成员列表删除
                        项目详情 - 成员，对应用户姓名变更，同步后，项目详情成员列表删除
                        项目详情 - 成员，从成员详情编辑项目角色，更新后项目详情成员列角色更新
            Namespace配额
                Namespace列表
                    创建NS - 仅支持输入名称，不支持设置配额
                    NS列表 - 更新相关字段，hover至所属项目时点击可跳转到项目详情
                    NS列表 - System 名字空间，点击morebutton- 「编辑名字空间配额」「删除」按钮禁用，hover时展示「不支持编辑/删除」
                    NS列表 - default 名字空间，点击morebutton - 「删除」按钮禁用，hover时展示「不支持删除」
                    NS列表 - default 名字空间，点击morebutton - 「编辑名字空间配额」按钮点击后展示编辑弹窗
                编辑Namespace
                    编辑NS - 编辑入口及弹窗 ，从NS列表morebutton点击编辑名字空间配额，编辑后查看配置
                    编辑NS - 编辑入口及弹窗 ，从NS详情morebutton点击编辑名字空间配额，编辑后详情查看配置
                    编辑NS - 编辑入口及弹窗 ，从项目详情NS列表morebutton点击编辑名字空间配额，编辑后查看
                    编辑NS - 新创建的ns，点击编辑配额，弹窗默认展示均为不限制
                    编辑NS - CPU请求/CPU限制，默认单位 core，允许切换为m
                    编辑NS - CPU请求/CPU限制，输入值校验 - 仅允许输入大于等于0的整数，为0时表示禁用
                    编辑NS - CPU请求/CPU限制，输入值校验 - 请求值大于限制时，报错「资源请求不能超过资源限制」
                    编辑NS - CPU请求/CPU限制，输入值校验 - 当所有项目中输入值总和大于集群总和时，允许保存
                    编辑NS - 内存请求/内存限制，默认单位 GiB，允许切换为MiB/TiB
                    编辑NS - 内存请求/内存限制，输入值校验 - 仅允许输入大于等于0的整数，为0时表示禁用
                    编辑NS - 内存请求/内存限制，输入值校验 - 请求值大于限制时，报错「资源请求不能超过资源限制」
                    编辑NS - 内存请求/内存限制，输入值校验 - 当所有项目中输入值总和大于集群总和时，允许保存
                    编辑NS - 持久卷申领，默认单位 GiB，允许切换为MiB/TiB
                    编辑NS - 持久卷申领，输入值校验 - 仅允许输入大于等于0的整数，为0时表示禁用
                    编辑NS - 持久卷申领，输入值校验 - 无数值上限，超过csi所在集群存储，可保存
                    编辑NS - GPU数量，输入值校验 - 仅允许输入大于等于0的整数，为0时表示禁用
                    编辑NS - GPU数量，输入值校验 - 无数值上限，输入超过宿主所挂载GPU数量，可保存
                    编辑NS - 编辑配置配额后保存，创建ResourceQuota，查看配置参数一致
                    编辑NS - 配置ns配额保存，已经在ns下创建的资源，若请求资源超过分配值，正常运行
                    编辑NS - 配置ns配额保存，在ns下创建资源，若请求资源超过分配值，阻止创建
                    编辑NS - 配置ns配额保存，在ns下创建资源，再次编辑ns配额，缩小参数，缩小后资源使用量超过配额，显示Notice tip
                    编辑NS - 配置ns配额保存，在ns下创建资源，再次编辑ns配额，缩小参数，缩小后资源使用量未超过配额，不显示Notice tip
                    编辑NS - 新创建的ns且创建资源，配置ns配额时，配置额度小于已使用资源量，保存时不会出现notice tip，再次编辑时弹窗展示
                    编辑NS - 所编辑ns属于某项目，已配置项目配额，ns配额的设置大于项目配额，可保存成功，但资源创建不会超过项目配额
                    编辑NS - 设置ns配额保存，再次编辑清空所有ns配额，保存成功，ResourceQuota资源清空，ns资源不再受配额限制
                删除Namespace
                    删除NS - 不属于项目，删除设置ns配额的NS，删除成功，同时删除ns下所有资源，删除ResourceQuota
                    删除NS - 属于项目，删除设置ns配额的NS，删除成功，同时删除ns下所有资源，删除ResourceQuota
                    删除NS - 配置ns配额，属于项目，在项目内移除ns，移除成功，不会删除ns及资源，不会删除ResourceQuota
                    删除NS - 配置ns配额，属于项目，删除项目时不删除ns，移除成功，不会删除ns及资源，不会删除ResourceQuota
                    删除NS - 配置ns配额，属于项目，删除项目时删除ns，删除成功，同时删除ns及资源，删除ResourceQuota
                    删除NS - 删除入口 - ns列表morebutton删除，提交后列表删除
                    删除NS - 删除入口 - ns详情morebutton删除，提交后返回列表并删除
                Namespace详情
                    NS详情 - System名字空间，不支持编辑配额，仅展示基本信息，与列表一致
                    NS详情 - Ns基本信息，CPU/内存使用量从监控 metric统计
                    NS详情 - 名字空间配额，配额值与创建的ResourceQuota status一致，根据配置及资源分配变更更新
                    NS详情 - 名字空间配额，已分配title，hover时tooltip提示「资源对象申请占用的配额数量」
                    NS详情 - 名字空间配额，当不配置NS资源配额时（即未创建ResourceQuota），查看列表展示 - 配额均为「不限」，已分配和使用率展示为空
                    NS详情 - 名字空间配额，当配置NS资源配额为0时，查看列表展示 - 配额展示为「0+单位」，已分配「数值或 -」，使用率柱形图填充为红色，数值为「-」
                    NS详情 - 名字空间配额，当单个资源类型不配置配额（创建ResourceQuota，但无该字段配置），查看列表展示 - 配额为「不限」，已分配和使用率展示为空
                    NS详情 - 名字空间配额，有配置配额，但无资源创建，查看列表展示 - 已分配和使用率展示为0
                    NS详情 - 名字空间配额，有设置配额，使用率（0 < X < 80）时，样式展示
                    NS详情 - 名字空间配额，有设置配额，使用率（80 ≤ X < 90）时，样式展示
                    NS详情 - 名字空间配额，有设置配额，使用率（X ≥ 90）时，样式展示
                    NS详情 - 名字空间配额，有设置配额，使用率（X = 0）时，样式展示
                    NS详情 - 名字空间配额，有设置配额，使用率计算百分比与ResourceQuota.status.used中对应计算值百分比一致
                    NS详情 - 名字空间状态 - 展示与列表一致 「活跃/删除中」
            默认容器配额
                创建项目
                    创建项目 - 不配置默认容器配额，保存后，project中containerDefaultResourceLimit为空，关联ns下不会生成LimitRange
                    创建项目 - 不配置默认容器配额，创建pod时若不设置resources，则不会自动配置
                    创建项目 - 默认容器配置，CPU请求/CPU限制，默认单位 m，允许切换为core
                    创建项目 - 默认容器配置，CPU请求/CPU限制，输入值校验 - 仅允许输入大于0的整数
                    创建项目 - 默认容器配置，CPU请求/CPU限制，输入值校验 - 请求值大于限制时，报错「资源请求不能超过资源限制」
                    创建项目 - 默认容器配置，CPU请求/CPU限制，输入值校验 - 设置容器配额大于项目配额，允许保存
                    创建项目 - 默认容器配置，内存请求/内存限制，默认单位 MiB，允许切换为GiB/TiB
                    创建项目 -默认容器配置， 内存请求/内存限制，输入值校验 - 仅允许输入大于0的整数
                    创建项目 - 默认容器配置，内存请求/内存限制，输入值校验 - 请求值大于限制时，报错「资源请求不能超过资源限制」
                    创建项目 - 默认容器配置，内存请求/内存限制，输入值校验 -  设置容器配额大于项目配额，允许保存
                    创建项目 - 设置默认容器配额，保存成功，查看Project资源，spec增加containerDefaultResourceLimit，参数正确
                    创建项目 - 设置默认容器配额，保存成功，项目关联的ns下，创建LimitRange资源，查看参数正确
                    创建项目 - 设置默认容器配额，保存成功，项目内创建pod时自动为其分配对应resources-limit/request
                    创建项目 - 不设置资源配置，仅设置默认容器配额，允许保存
                    创建项目 - 不设置资源配置，仅设置默认容器配额，项目关联ns设置资源配额，允许保存
                    创建项目 - 设置资源配置，设置默认容器配额，项目关联ns设置资源配额，允许保存
                    创建项目 - 设置默认容器配额，不关联任何ns，保存后，project仅生成containerDefaultResourceLimit，不会创建LimitRange
                编辑项目
                    编辑项目 - 创建时未设置默认容器配额，可在编辑弹窗中设置，参数校验与创建一致
                    编辑项目 - 创建时未设置默认容器配额，项目内已创建pod，编辑容器配额保存，保存后不影响已有pod，自动创建containerDefaultResourceLimit / LimitRange
                    编辑项目 - 创建时设置默认容器配额，项目内已创建pod，修改容器配额，配额值小于当前pod resources，可保存成功，不影响当前pod
                    编辑项目 - 创建时设置默认容器配额，项目内已创建pod，修改容器配额，配额值大于当前pod resources，可保存成功，不影响当前pod
                    编辑项目 - 创建时设置默认容器配额，修改默认容器配额保存，自动更新containerDefaultResourceLimit / LimitRange
                    编辑项目  - 修改默认容器配额保存，保存后项目详情对应值更新，新建pod会被分配已修改的容器配额值
                    编辑项目 - 创建时设置默认容器配额，清空所有容器配额，保存成功，Project中containerDefaultResourceLimit清空，LimitRange资源清空，不再受默认容器配额限制
                    编辑项目 - 创建时设置默认容器配额，但不关联ns，编辑项目关联ns，保存成功，ns下创建LimitRange
                    编辑项目 - 创建时设置默认容器配额，关联ns，编辑项目移除ns，保存成功，ns下删除LimitRange
                删除项目
                    删除项目 - 不配置默认容器配额，删除项目流程不变
                    删除项目 - 配置默认容器配额，删除项目时不删除ns，删除后project删除，LimitRange删除，已创建的pod不受影响
                    删除项目 - 配置默认容器配额，删除项目时不删除ns，删除后project删除，LimitRange删除，在ns下创建pod时不受limitrange支配
                    删除项目 - 配置默认容器配额，删除项目时删除ns，删除后project删除，LimitRange删除，ns下所有资源删除
                    删除项目 - 配置默认容器配额，但不关联ns，删除项目流程不变
            用户场景
                使用规则
                    新建项目，仅配置资源配额，关联ns未配置配额，创建pod时资源限制仅受限于资源配额
                    新建项目，仅配置资源配额，关联ns未配置配额，ns下资源使用已超过配额限制，新创建pod时不允许
                    编辑项目，仅配置资源配额，关联ns未配置配额，资源创建超出限制，编辑扩大限额后，创建成功
                    编辑项目，仅配置资源配额，关联ns未配置配额，资源创建超出限制，编辑项目移除对应ns，资源创建成功
                    删除项目，仅配置资源配额，关联ns未配置配额，资源创建超出限制，删除项目但不删除ns，资源创建成功
                    项目设置资源配额，关联ns设置配额，ns下创建资源时，不可超过ns配额限制
                    项目设置资源配额，关联ns设置配额，ns下创建资源时，超过ns配额限制，编辑ns配额，创建成功
                    项目设置资源配额，关联ns设置配额，多个ns下创建资源总和，不可超过资源配额，超过不允许创建
                    项目设置资源配额，关联ns设置配额，多个ns下创建资源总和超过资源配额，移除ns，创建成功
                    项目设置资源配额，关联ns设置配额，多个ns下创建资源总和超过资源配额，扩大资源配额，创建成功
                    设置默认容器配额，关联ns不设置配额，创建pod时不申明resoucres，根据默认容器配额设置
                    设置默认容器配额，关联ns不设置配额，创建pod时申明限制，不申明请求，根据pod申明limit设置
                    设置默认容器配额，关联ns不设置配额，创建pod时申明请求，不申明限制，limit根据默认容器配额设置
                    设置资源配额，设置默认容器配额，关联ns不设置配额，创建pod资源请求总合超过资源配额，阻止创建
                    设置资源配额，设置默认容器配额，关联ns不设置配额，容器配额限制超过资源配额，阻止创建
                    设置资源配额，设置默认容器配额，关联ns设置配额，创建pod时的资源总量受三种影响
                    不设置资源配额，设置默认容器配额，关联ns不设置配额，创建pod时仅limitrange影响，创建资源仅受限于集群本身资源
                    不设置资源配额，设置默认容器配额，关联ns设置配额，创建pod时limitrange和resourcequota影响，受限于ns配额
                    不设置资源配额和默认容器配额，关联ns设置配额，创建pod时仅受限于ns配额
                    可对不关联项目的ns设置资源配额，创建pod同样受限于ns配额-仅admin权限
                    仅设置ns资源配额，创建pod时不指定request/limit，pod阻止创建，已分配及使用率无变化，不消耗配额
                    设置ns资源配额和默认容器配额，创建pod时不指定request/limit，pod创建成功，已分配及使用率增加，消耗配额
                    仅设置项目资源配额，创建pod时不指定request/limit，pod阻止创建，已分配及使用率无变化，不消耗配额
                    设置项目资源配额和默认容器配额，创建pod时不指定request/limit，pod创建成功，已分配及使用率增加，消耗配额
                    仅设置ns资源配额，创建pod时指定request/limit，检查pod创建，已分配及使用率增加，消耗配额
                    仅设置项目资源配额，创建pod时指定request/limit，检查pod创建，已分配及使用率增加，消耗配额，超出配额时阻止创建
                    未设置任何配额，创建pod时不指定request/limit，pod创建成功；再创建ns资源配额，检查已分配及使用率无变化，不消耗配额
                    未设置任何配额，创建pod时不指定request/limit，pod创建成功；再创建项目资源配额，检查已分配及使用率无变化，不消耗配额
                    配额设置GPU，仅支持request，当pod中设置 requests.nvidia.com/gpu时，生效限制
                    配额限制PVC总量，单个CSI集群，使用单一sc创建pvc，总量受配额限制
                    配额限制PVC总量，单个CSI集群，创建多个sc，并使用不同sc创建pvc，所有pvc总量受配额限制
                    配额限制PVC总量，多个CSI的集群，使用不同sc创建pvc，所有pvc总量受配额限制
                    配置项目资源配额，设置额度为0时，验证禁用行为（CPU/内存/pvc/gpu）
                    配置名字空间配额，设置额度为0时，验证禁用行为（CPU/内存/pvc/gpu）
                集群影响
                    操作配额相关配置，不会触发集群滚动更新和原地更新
                    配置资源配额，触发替换节点，集群不受影响
                    配置资源配额，触发扩容节点，集群不受影响
                    配置资源配额，触发缩容节点，集群不受影响
                    配置资源配额，触发升级k8s版本，集群不受影响
                    配置资源配额，触发原地更新，集群不受影响
                    配置资源配额，触发SKS升级，集群不受影响
                    验证不同k8s版本下的资源配额是否有影响 - v1.25
                    验证不同k8s版本下的资源配额是否有影响 - v1.26
                    验证不同k8s版本下的资源配额是否有影响 - v1.27
                    验证不同k8s版本下的资源配额是否有影响 - v1.30
                    验证不同架构的k8s集群资源配额是否有影响 - x86 - rocky/oe
                    验证不同架构的k8s集群资源配额是否有影响 - Arrch - oe
                    SKS1.4版本创建的项目及ns，升级至SKS1.5后，可通过UI设置配额，原有资源不受影响
                    SKS1.4版本不创建权限，升级至SKS1.5后，可通过UI设置配额，功能正常
                    Addon - 工作集群默认开系统addon：cluster-quota-enforcer，管控集群不开启
                    配置资源配额，触发节点重建行为，在设置配额前已有的 Pod 没配 resources，重建可能失败（未配置默认容器配额）
                    配置资源配额，触发节点重建行为，在设置配额前已有的 Pod 没配 resources，重建可能失败（有默认容器配额但超出项目/ns配额）
                    配置资源配额，触发扩容节点，daemonset资源配额 used 会增加可能超出配额被拦截
                用户限制
                    用户自定义创建ResourceQuota，不阻止创建，创建后不展示在UI中
                    用户自定义在ns1创建ResourceQuota，同时ui端ns1下同样创建，限制值依据k8s机制，取最小值
                    用户在后端修改SKS创建的ResourceQuota，修改后不会自动更新回原本设置
                    用户自定义创建LimitRange，不阻止创建，创建后不展示在UI中
                    用户自定义在ns1创建LimitRange，同时ui端ns1下同样创建，限制值依据k8s机制，取最小值
                    用户在后端修改SKS创建的LimitRange，修改后再次编辑更新回原本设置
                    用户在后端手动删除SKS创建的LimitRange，自动重新创建，不影响使用
                    用户在后端手动删除SKS创建的ResourceQuota，不会自动重新创建，可在UI再次编辑和保存
                异常处理
                    后端操作 - 为系统项目创建配额 - 报错 SKS_CREATE_SYSTEM_PROJECT_QUOTA_NOT_ALLOWED
                    后端操作 - 为自定义项目再次创建配额 - 报错 SKS_PROJECT_QUOTA_ALREADY_EXISTS
                    后端操作 - 为系统ns创建配额 - 报错SKS_CREATE_SYSTEM_NAMESPACE_QUOTA_NOT_ALLOWED
                    后端操作 - 为自定义ns再次创建配额 - 报错 SKS_NAMESPACE_QUOTA_ALREADY_EXISTS
                项目变更
                    项目A关联ns1且设置资源配额，变更ns1关联到项目B，原ns1下已存在资源正常不受影响，项目A使用率减少，项目B使用率增加
                    项目A关联ns1且设置资源配额，变更ns1关联到项目B，ns1新创建资源规则项目B的资源配额限制
                    项目A关联ns1并设置默认容器配额，项目B设置默认容器配置小于A，迁移ns1到项目B，LimitRange重新创建，原pod不受影响，不会被驱逐
                    项目A关联ns1并设置默认容器配额，项目B设置默认容器配置小于A，迁移ns1到项目B，LimitRange重新创建，ns1下新创建pod，resources设置为B
                    项目A关联ns1并设置默认容器配额，项目B设置默认容器配置小于A，迁移ns1到项目B，LimitRange重新创建，ns1下重建原pod，resources设置为B
                    项目A关联ns1并设置默认容器配额，项目B设置默认容器配置大于A，迁移ns1到项目B，LimitRange重新创建，原pod不受影响，新创建受限于B
                    项目A关联ns1且设置资源配额，设置默认容器配额；变更ns1关联到项目B未设置默认容器配额，ns1新创建pod时若不设置limit/request，将阻止创建
            事件
                创建项目，设置项目配额，创建成功，产生CreateProjectQuota 事件
                编辑项目，设置项目配额，编辑成功，产生UpdateProjectQuota 事件
                编辑项目，更新项目配额，编辑成功，产生UpdateProjectQuota事件，记录difference
                编辑项目，清空项目配额，编辑成功，产生DeleteProjectQuota事件
                删除项目，删除项目配额，删除成功，产生DeleteProjectQuota事件
                编辑名字空间，设置资源配额，编辑成功，产生CreateNamespaceQuota事件
                编辑名字空间，更新资源配额，编辑成功，产生UpdateNamespaceQuota事件，记录difference
                编辑名字空间，清空资源配额，编辑成功，产生DeleteNamespaceQuota事件
                删除名字空间，删除资源配额，删除成功，不会产生DeleteNamespaceQuota事件
                删除项目同时删除名字空间，删除资源配额，删除成功，不会产生DeleteNamespaceQuota事件
                创建项目，设置默认容器配额，创建成功，产生的ProjectCreated事件
                编辑项目，设置默认容器配额，编辑成功，产生的ProjectUpdated事件，更新containerDefaultResourceLimit
                编辑项目，更新默认容器配额，编辑成功，产生的ProjectUpdated事件，更新containerDefaultResourceLimit
                编辑项目，清空默认容器配额，编辑成功，产生的ProjectUpdated事件，清除containerDefaultResourceLimit
                删除项目，删除默认容器配额，删除成功，产生的ProjectDeleted事件
                创建项目，关联ns，设置默认容器配额，创建成功，产生CreateLimitRange事件
                编辑项目，关联ns，设置默认容器配额，编辑成功，产生CreateLimitRange事件
                编辑项目，已关联ns，更新默认容器配额，编辑成功，产生UpdateLimitRange事件
                编辑项目，关联新的ns，编辑成功，产生CreateLimitRange事件
                编辑项目，移除ns，编辑成功，产生DeleteLimitRange事件
                编辑项目，已关联ns，清空默认容器配额，编辑成功，产生DeleteLimitRange事件
                删除项目，不删除关联ns，删除默认容器配额，删除成功，产生DeleteLimitRange事件
                有名字空间配额权限的租户，操作名字空间配额，产生对应NamespaceQuota事件，在admin视角下可查看到
            报警/监控
                报警规则
                    项目配额
                        项目配额 - 资源配额使用率在0 - 80%之间，不会触发报警
                        项目配额 - 资源配额使用率在持续15分钟达到80%（used/hard），触发报警ProjectQuotaAlmostFull，默认报警级别「注意」
                        项目配额 - 资源配额使用率达到80%（used/hard），在15分钟内修改配额值使其低于80%，不会触发报警ProjectQuotaAlmostFull
                        项目配额 - 资源配额使用率达到80%（used/hard），在15分钟内移除占用ns或删除负载，使其低于80%，不会触发报警ProjectQuotaAlmostFull
                        项目配额 - 资源配额使用率达到80%（used/hard），在15分钟内删除项目，不会触发报警ProjectQuotaAlmostFull
                        项目配额 - 资源配额使用率，触发报警ProjectQuotaAlmostFull，更新配额值使其总比率低于80%，报警标记已处理
                        项目配额 - 资源配额使用率，触发报警ProjectQuotaAlmostFull，调整资源负载使其总比率低于80%，报警标记已处理
                        项目配额 - 资源配额使用率在持续15分钟达到100%（used=hard），触发报警ProjectQuotaFullyUsed，默认报警级别「严重警告」
                        项目配额 - 资源配额使用率，触发报警ProjectQuotaFullyUsed，调整配额使其总比率下降，若大于80%，触发ProjectQuotaAlmostFull
                        项目配额 - 资源配额使用率，触发报警ProjectQuotaFullyUsed，调整配额使其总比率下降至正常范围，报警标记已解决
                        项目配额 - 资源配额使用率在持续15分钟超过100%（used>hard），触发报警ProjectQuotaExceeded，默认报警级别「严重警告」
                        项目配额 - 资源配额使用率，触发报警ProjectQuotaExceeded，调整配额使其比率下降，等于100%，触发ProjectQuotaAlmostFull
                        项目配额 - 资源配额使用率，触发报警ProjectQuotaExceeded，调整配额使其比率下降至正常范围，报警标记已解决
                    NS配额
                        NS配额 - NS配额使用率在0 - 80%之间，不会触发报警
                        NS配额 - NS配额使用率在持续15分钟达到80%（used/hard），触发报警KubeQuotaAlmostFull，默认报警级别「注意」
                        NS配额 - NS配额使用率达到80%（used/hard），在15分钟内修改配额值使其低于80%，不会触发报警KubeQuotaAlmostFull
                        NS配额 - NS配额使用率达到80%（used/hard），在15分钟内移除占用ns或删除负载，使其低于80%，不会触发报警KubeQuotaAlmostFull
                        NS配额 - NS配额使用率达到80%（used/hard），在15分钟内删除NS，不会触发报警KubeQuotaAlmostFull
                        NS配额 - NS配额使用率，触发报警KubeQuotaAlmostFull，更新配额值使其总比率低于80%，报警标记已处理
                        NS配额 - NS配额使用率，触发报警KubeQuotaAlmostFull，调整资源负载使其总比率低于80%，报警标记已处理
                        NS配额 - NS配额使用率在持续15分钟达到100%（used=hard），触发报警KubeQuotaFullyUsed，默认报警级别「严重警告」
                        NS配额 - NS配额使用率，触发报警KubeQuotaFullyUsed，调整配额使其总比率下降，若大于80%，触发KubeQuotaAlmostFull
                        NS配额 - NS配额使用率，触发报警KubeQuotaFullyUsed，调整配额使其总比率下降至正常范围，报警标记已解决
                        NS配额 - 资源配额使用率在持续15分钟超过100%（used>hard），触发报警KubeQuotaExceeded，默认报警级别「严重警告」
                        NS配额 - NS配额使用率，触发报警KubeQuotaExceeded，调整配额使其比率下降，等于100%，触发KubeQuotaFullyUsed
                        NS配额 - NS配额使用率，触发报警KubeQuotaExceeded，调整配额使其比率下降至正常范围，报警标记已解决
                    调整阈值
                        默认资源配额报警阈值 - 80%
                        调整资源配额报警阈值 - 如调整至60%，则Project/KubeQuotaAlmostFull 达到60%触发报警
            权限
                项目配额 - 集群纬度权限，仅admin用户可操作项目配额，租户无权限
                项目配额 -  admin配置的配额，租户视角下创建资源，受到配额限制
                项目默认容器配额 - 集群纬度权限，仅admin用户可操作默认容器配额
                项目默认容器配额 - admin配置的配额，租户视角下创建资源，配置生效
                LimitRange - 工作集群内ns级别资源，属于租户权限「管理namespace配额」，无UI入口
                LimitRange - 租户开放权限「管理namespace配额」时，可使用集群控制台或kubeconfig自定义limitrange
                ns配额/ResourceQuota - 分配租户权限「管理名字空间配额」，租户可UI编辑配额
                ns配额/ResourceQuota -  admin用户在ns下配置的配额，在有权限的租户视角，编辑名字空间配额弹窗中，可看到相同配置
                ns配额/ResourceQuota - admin用户配置的ns配额，有权限的租户可对该配额进行编辑，且两边配置均生效
                ns配额/ResourceQuota - admin用户不配置ns配额，有权限的租户可对项目内ns增加配额限制，且两边配置均生效
                ns配额/ResourceQuota -  admin配置的配额，租户视角下创建资源，受到配额限制
                ns配额/ResourceQuota -  租户配置的ns配额，admin视角下创建资源，受到配额限制
                角色管理 - 新增角色范围「管理名字空间配额」，hover时tooltip展示文案
                角色管理 - 对应新增ProjectRole模板-role-template-manage-quota
                角色管理 - 更新角色描述「管理所有资源与配置」hover时tooltip展示文案
                租户视角创建资源，在admin项目详情中可看到使用率更新
                租户视角创建资源，在admin名字空间详情中可看到使用率更新
                租户视角创建资源，触发对应的报警，在admin工作集群概览可看到对应报警信息
                只读用户 - 可查看Namespace/项目详情
                具有编辑权限的用户 - 可编辑及查看资源配额
        租户级资源可视化管理
            基础展示
                工作集群使用者登录 - 默认展示已分配权限的集群列表，展示内容不变，同1.4
                工作集群使用者登录 - hover至显示名称变蓝，点击显示名称，进入集群详情页面，默认展示 「名字空间」
                集群列表 - morebutton 展示不变，显示「下载kubeconfig」「集群控制台」「导入YAML」按钮，功能可用
                集群详情 - 显示「下载Kubeconfig」「集群控制台」「导入YAML」按钮，morebutton不展示
                集群详情 - 展示集群状态，更新状态跟随改变
                集群详情 - 展示集群显示名称，admin更新显示名称跟随改变
                集群详情 - 验证「下载Kubeconfig」功能，下载弹窗及下载文件，均为受限kubeconfig
                集群详情 - 验证「下载Kubeconfig」功能，使用下载的kubeconfig，权限受限
                集群详情 - 验证「集群控制台」功能，可正常使用，使用的kubeconfig受权限控制
                导入YAML - 导入yaml弹窗，文案及按钮与admin一致
                导入YAML - 导入弹窗，namespace过滤器，仅展示项目内关联的namespace，展示「不选择」
                导入YAML - 选择文件导入，导入时不指定ns，yaml中也未指定ns，导入时footer报错提示「请指定名字空间」
                导入YAML - 选中文件导入，导入后转换内容及格式正确，无影响（yaml/json）
                导入YAML - 选中文件导入，导入的资源均有权限，可导入成功，展示导入结果
                导入YAML - 选中文件导入，导入的资源中有资源无权限，部分导入成功，展示导入结果，并返回k8s报错信息
                导入YAML - 选中文件导入，导入时不指定ns，文件内指定的ns为项目内，导入成功
                导入YAML - 选中文件导入，导入时不指定ns，文件内指定的ns不属于项目，导入失败，报错
                导入YAML - 选中文件导入，导入时指定ns，导入后创建资源到指定ns，导入成功，查看所创建资源状态
                导入YAML - 选中文件夹批量导入，可正常导入，规则同导入文件
                资源状态 - 资源的更新可以实时watch
                资源yaml 创建schema校验-需和admin视角一致
            项目级资源
                工作负载
                    CronJob
                        CronJob - 检查资源列表页面 - 「标题及描述」、列表信息、按钮
                        CronJob  - 点击名称进入详情，检查详情页面 - 资源名称及状态、详情列表、按钮，事件不展示
                        CronJob - 创建CronJob，可创建成功，列表及详情展示正确，有toast
                        CronJob - 编辑Yaml，可编辑成功，资源信息更新 （列表/详情），有toast
                        CronJob - 下载Yaml，可下载成功，Yaml文件可读（列表/详情）
                        CronJob - 暂停，可暂停及恢复cronjob，对应状态实时更新（列表/详情），有toast
                        CronJob - 跳转，有「编辑名字空间配额」权限，点击名字空间，可跳转至对应详情（列表/详情）
                        CronJob - 跳转，无「编辑名字空间配额」权限，点击名字空间，不支持跳转（列表/详情）
                        CronJob - 跳转，点击详情中 Job列表名称，可跳转至对应Job详情
                        CronJob - 删除，可删除cronjob资源，同时删除对应Job及pod，有toast
                    DaemonSet
                        DaemonSet - 检查资源列表页面 - 「标题及描述」、列表信息、按钮
                        DaemonSet  - 点击名称进入详情，检查详情页面 - 资源名称及状态、详情列表、按钮，监控事件隐藏不展示
                        DaemonSet - 创建DaemonSet，可创建成功，列表及详情展示正确，有toast
                        DaemonSet - 编辑Yaml，可编辑成功，资源信息更新 （列表/详情），有toast
                        DaemonSet - 下载Yaml，可下载成功，Yaml文件可读（列表/详情）
                        DaemonSet - 重新部署，可执行成功，对应状态实时更新（列表/详情），有toast
                        DaemonSet - 跳转，有「编辑名字空间配额」权限，点击名字空间，可跳转至对应详情（列表/详情）
                        DaemonSet - 跳转，无「编辑名字空间配额」权限，点击名字空间，不支持跳转（列表/详情）
                        DaemonSet - 跳转，点击详情中 Pod列表名称，可跳转至对应pod详情
                        DaemonSet - 跳转，点击详情中 Pod列表，所属节点，不支持跳转
                        DaemonSet - 删除，可删除资源，同时删除对应pod，有toast
                    Deployment
                        Deployment - 检查资源列表页面 - 「标题及描述」、列表信息、按钮
                        Deployment  - 点击名称进入详情，检查详情页面 - 资源名称及状态、详情列表、按钮，监控、事件隐藏不展示
                        Deployment - 创建Deployment，可创建成功，列表及详情展示正确，有toast
                        Deployment - 编辑Yaml，可编辑成功，资源信息更新 （列表/详情），有toast
                        Deployment - 下载Yaml，可下载成功，Yaml文件可读（列表/详情）
                        Deployment - 重新部署，可执行成功，对应状态实时更新（列表/详情），有toast
                        Deployment - 跳转，有「编辑名字空间配额」权限，点击名字空间，可跳转至对应详情（列表/详情）
                        Deployment - 跳转，无「编辑名字空间配额」权限，点击名字空间，不支持跳转（列表/详情）
                        Deployment - 跳转，点击详情中 Pod列表名称，可跳转至对应pod详情
                        Deployment - 跳转，点击详情中 Pod列表，所属节点，不支持跳转
                        Deployment - 删除，可删除资源，同时删除对应pod，有toast
                        Deployment - 编辑副本数， 可保存成功，编辑后创建/删除相应pod，有toast
                    Job
                        Job - 检查资源列表页面 - 「标题及描述」、列表信息、按钮
                        Job  - 点击名称进入详情，检查详情页面 - 资源名称及状态、详情列表、按钮，事件不展示
                        Job - 创建Job，可创建成功，列表及详情展示正确，有toast
                        Job - 编辑Yaml，可编辑成功，资源信息更新 （列表/详情），有toast
                        Job - 下载Yaml，可下载成功，Yaml文件可读（列表/详情）
                        Job - 跳转，有「编辑名字空间配额」权限，点击名字空间，可跳转至对应详情（列表/详情）
                        Job - 跳转，无「编辑名字空间配额」权限，点击名字空间，不支持跳转（列表/详情）
                        Job - 跳转，点击详情中 pod列表名称，可跳转至对应pod详情
                        Job - 跳转，点击详情中 Pod列表，所属节点，不支持跳转
                        Job - 删除，可删除job资源，同时删除对应pod，有toast
                    StatefulSet
                        StatefulSet - 检查资源列表页面 - 「标题及描述」、列表信息、按钮
                        StatefulSet  - 点击名称进入详情，检查详情页面 - 资源名称及状态、详情列表、按钮
                        StatefulSet  - 点击名称进入详情，检查详情页面 - 事件、监控不展示
                        StatefulSet - 创建StatefulSet，可创建成功，列表及详情展示正确，有toast
                        StatefulSet - 编辑Yaml，可编辑成功，资源信息更新 （列表/详情），有toast
                        StatefulSet - 下载Yaml，可下载成功，Yaml文件可读（列表/详情）
                        StatefulSet - 重新部署，可执行成功，对应状态实时更新（列表/详情），有toast
                        StatefulSet - 跳转，有「编辑名字空间配额」权限，点击名字空间，可跳转至对应详情（列表/详情）
                        StatefulSet - 跳转，无「编辑名字空间配额」权限，点击名字空间，不支持跳转（列表/详情）
                        StatefulSet - 跳转，点击详情中 Pod列表名称，可跳转至对应pod详情
                        StatefulSet - 跳转，点击详情中 Pod列表，所属节点，不支持跳转
                        StatefulSet - 删除，可删除资源，同时删除对应pod，pvc解除挂载，有toast
                        StatefulSet - 编辑副本数， 可保存成功，编辑后创建/删除相应pod，pvc挂载/解除挂载，有toast
                    Pod
                        Pod - 检查资源列表页面 - 「标题及描述」、列表信息、按钮
                        Pod  - 点击名称进入详情，检查详情页面 - 资源名称及状态、详情列表、事件tab、日志tab，按钮，隐藏监控tab
                        Pod  - 点击名称进入详情，检查详情页面 - 事件、监控tab不展示
                        Pod - 创建Pod，可创建成功，列表及详情展示正确，有toast
                        Pod - 编辑Yaml，可编辑成功，资源信息更新 （列表/详情），有toast
                        Pod - 下载Yaml，可下载成功，Yaml文件可读（列表/详情）
                        Pod - 跳转，有「编辑名字空间配额」权限，点击名字空间，可跳转至对应详情（列表/详情）
                        Pod - 跳转，无「编辑名字空间配额」权限，点击名字空间，不支持跳转（列表/详情）
                        Pod - 跳转，点击详情中工作负载，可支持跳转，点击后跳转至所属工作负载详情
                        Pod - 删除，可删除Pod资源，有toast
                        Pod - 跳转，所属节点，应不支持跳转，隐藏「节点控制台」按钮
                        Pod - 挂载pvc的pod（如statefulset创建的pod），有「查看持久卷」权限，点击持久卷名称，可跳转至对应详情
                        Pod - 挂载pvc的pod（如statefulset创建的pod），有「查看持久卷」权限，展示pvc列表，有「编辑名字空间配额」权限，点击可跳转到ns详情
                        Pod - 挂载pvc的pod（如statefulset创建的pod），有「查看持久卷」权限，展示pvc列表，无「编辑名字空间配额」权限，ns不可跳转
                        Pod - 挂载pvc的pod（如statefulset创建的pod），有「查看持久卷」权限，展示pvc列表，持久卷不支持跳转
                        Pod - 挂载pvc的pod（如statefulset创建的pod），有「查看持久卷」权限，展示pvc列表，存储类不支持跳转
                        Pod - 挂载pvc的pod（如statefulset创建的pod），无「查看持久卷」权限，隐藏pvc列表
                        Pod - Pod控制台，点击后可打开pod控制台，进入容器内操作，控制台操作与admin一致
                        Pod - 上传文件，打开pod控制台或直接点击上传文件，可向容器内上传文件
                        Pod - 下载文件，打开pod控制台或直接点击下载文件，可选中容器内文件下载
                        Pod - 查看实时日志，点击详情日志tab，可查看pod实时日志
                服务与网络
                    Ingress
                        Ingress - 检查资源列表页面 - 「标题及描述」、列表信息、按钮
                        Ingress  - 点击名称进入详情，检查详情页面 - 资源名称、详情规则列表、按钮
                        Ingress - 创建Ingress，可创建成功，列表及详情展示正确，有toast
                        Ingress - 编辑Yaml，可编辑成功，资源信息更新 （列表/详情），有toast
                        Ingress - 下载Yaml，可下载成功，Yaml文件可读（列表/详情）
                        Ingress - 跳转，有「编辑名字空间配额」权限，点击名字空间，可跳转至对应详情（列表/详情）
                        Ingress - 跳转，无「编辑名字空间配额」权限，点击名字空间，不支持跳转（列表/详情）
                        Ingress - 删除，可删除Ingress资源，有toast
                        Ingress - 跳转，backend对应service，点击可跳转至对应servie详情（列表/详情）
                    NetworkPolicy
                        NetworkPolicy - 检查资源列表页面 - 「标题及描述」、列表信息、按钮
                        NetworkPolicy  - 点击名称进入详情，检查详情页面 - 资源名称、详情列表、Ingress/Egress规则，按钮
                        NetworkPolicy - 创建NetworkPolicy，可创建成功，列表及详情展示正确，有toast
                        NetworkPolicy - 编辑Yaml，可编辑成功，资源信息更新 （列表/详情），有toast
                        NetworkPolicy - 下载Yaml，可下载成功，Yaml文件可读（列表/详情）
                        NetworkPolicy - 跳转，有「编辑名字空间配额」权限，点击名字空间，可跳转至对应详情（列表/详情）
                        NetworkPolicy - 跳转，无「编辑名字空间配额」权限，点击名字空间，不支持跳转（列表/详情）
                        NetworkPolicy - 删除，可删除NetworkPolicy资源，有toast
                        NetworkPolicy - 验证实际生效范围是否受权限影响
                    Service
                        Service - 检查资源列表页面 - 「标题及描述」、列表信息、按钮
                        Service  - 点击名称进入详情，检查详情页面 - 资源名称、详情列表、按钮，监控隐藏不展示
                        Service - 创建Service，可创建成功，列表及详情展示正确，有toast
                        Service - 编辑Yaml，可编辑成功，资源信息更新 （列表/详情），有toast
                        Service - 下载Yaml，可下载成功，Yaml文件可读（列表/详情）
                        Service - 跳转，有「编辑名字空间配额」权限，点击名字空间，可跳转至对应详情（列表/详情）
                        Service - 跳转，无「编辑名字空间配额」权限，点击名字空间，不支持跳转（列表/详情）
                        Service - 删除，可删除Service资源，有toast
                        Service - 跳转，有「管理工作负载资源」/「查看所有资源与配置」权限，点击pod列表名称，可跳转至pod详情
                        Service - 跳转，无「管理工作负载资源」/「查看所有资源与配置」权限，不展示pod列表
                        Service - 跳转，pod列表中所属节点，不支持跳转
                        Service - NodePort类型，点击集群外访问方式，可正常点击并跳转至「vip：nodeport」页面
                配置
                    ConfigMap
                        ConfigMap - 检查资源列表页面 - 「标题及描述」、列表信息、按钮
                        ConfigMap  - 点击名称进入详情，检查详情页面 - 资源名称、基本信息、数据、按钮
                        ConfigMap - 创建ConfigMap，可创建成功，列表及详情展示正确，有toast
                        ConfigMap - 编辑Yaml，可编辑成功，资源信息更新 （列表/详情），有toast
                        ConfigMap - 下载Yaml，可下载成功，Yaml文件可读（列表/详情）
                        ConfigMap - 跳转，有「编辑名字空间配额」权限，点击名字空间，可跳转至对应详情（列表/详情）
                        ConfigMap - 跳转，无「编辑名字空间配额」权限，点击名字空间，不支持跳转（列表/详情）
                        ConfigMap - 删除，可删除ConfigMap资源，有toast
                    Secret
                        Secret - 检查资源列表页面 - 「标题及描述」、列表信息、按钮
                        Secret  - 点击名称进入详情，检查详情页面 - 资源名称、基本信息、数据、按钮
                        Secret - 创建Secret，可创建成功，列表及详情展示正确，有toast
                        Secret - 编辑Yaml，可编辑成功，资源信息更新 （列表/详情），有toast
                        Secret - 下载Yaml，可下载成功，Yaml文件可读（列表/详情）
                        Secret - 跳转，有「编辑名字空间配额」权限，点击名字空间，可跳转至对应详情（列表/详情）
                        Secret - 跳转，无「编辑名字空间配额」权限，点击名字空间，不支持跳转（列表/详情）
                        Secret - 删除，可删除Secret资源，有toast
                存储
                    PVC
                        PVC - 检查资源列表页面 - 「标题及描述」、列表信息、按钮
                        PVC  - 点击名称进入详情，检查详情页面 - 资源名称、基本信息、列表信息按钮
                        PVC  - 点击名称进入详情，检查详情页面 - 事件、监控、资源用量均不展示
                        PVC - 创建PVC，表单中「存储类」展示-输入框，不展示任何sc
                        PVC - 创建PVC，表单中「名字空间」，仅展示关联所属项目下的namespace名称
                        PVC - 创建PVC，从表单填写，可创建成功，列表及详情展示正确，有toast
                        PVC - 创建PVC，切换yaml填写，可创建成功，列表及详情展示正确，有toast
                        PVC - 创建PVC，创建成功，admin查看对应pv，创建成功
                        PVC - 下载Yaml，可下载成功，Yaml文件可读（列表/详情）
                        PVC - 跳转，有「编辑名字空间配额」权限，点击名字空间，可跳转至对应详情（列表/详情）
                        PVC - 跳转，无「编辑名字空间配额」权限，点击名字空间，不支持跳转（列表/详情）
                        PVC - 删除，可删除PVC资源，有toast
                        PVC - 详情页，编辑分配量，编辑成功，有toast
                        PVC - 跳转，对应的持久卷，点击不支持跳转（列表/详情）
                        PVC - 跳转，对应的存储类，点击不支持跳转（列表/详情）
                        PVC - 跳转，pod关联pvc，有「管理工作负载」/「查看所有资源与配置」权限，展示相关pod列表，点击可跳转pod详情
                        PVC - 跳转，pod关联pvc，无「管理工作负载」/「查看所有资源与配置」权限，不展示相关pod列表
                权限控制
                    无「管理xx」权限 - 相应分配的父级和子级资源tab均不展示
                    从有「管理xx」权限切换无权限 - 相关资源，点击操作提交时权限拒绝
                    仅有「查看所有资源与配置」权限 - 所有资源均只支持查看列表及详情，可支持「下载Yaml」，其余操作按钮隐藏
                    无「管理持久卷申领」权限 - 创建StatefulSet时，可创建pvc，对应pod可挂载pv，但无法查看pvc
                    仅有「查看所有资源与配置」权限 - Pod无控制台权限，隐藏pod控制台、上传文件、下载文件入口（需要有pod/exec权限）
                    仅有「管理某类资源」权限 - k8s后端查看资源对应事件，无权限
                    有「查看所有资源」权限 - k8s后端查看资源对应事件，有权限
                    有「查看所有资源」权限 - UI 负载详情中，隐藏事件，不展示
                    watch-从管理员权限切换项目成员权限，当前负载资源的列表展示全部，刷新后切换为项目内资源
                    watch-从项目成员权限切换管理员权限，当前负载资源的列表展示为项目成员权限列表，刷新后切换为全部
                    watch-从项目成员有资源权限切换无权限，当前负载资源的列表展示为有权限列表，刷新后无权限查看
                    watch-从项目成员无资源权限切换有权限，当前负载资源的列表无权限查看，刷新展示有权限列表
                    k8s 原生 Watch 不会实时感知权限的变化，以 Watch 那个时刻的权限为准
            集群级资源
                名字空间
                    名字空间 - 仅展示属于项目的ns，描述及列表项与admin一致，无创建名字空间按钮
                    名字空间 - 点击列表morebutton查看，仅「编辑名字空间配额」按钮，无「删除」按钮
                    名字空间 - 点击「编辑名字空间配额」按钮，打开展示弹窗及校验规则与admin一致
                    名字空间 - 租户编辑名字空间配额，编辑内容可正常生效
                    名字空间 - hover至名称变蓝，点击名称进入名字空间详情，展示详情与admin展示方式一致 - System ns 不展示名字空间配额
                    名字空间 - 点击详情morebutton查看，仅「编辑名字空间配额」按钮，无「删除」按钮
                    名字空间 - admin创建ns并加入该使用者项目，刷新页面，新增ns列表
                    名字空间 - admin在项目中移除ns，刷新页面，对应ns移除列表
                    名字空间 - admin删除一个所属项目但不删除ns，刷新页面，所有属于该项目的ns均移除
                    名字空间 - admin删除一个所属项目且删除ns，刷新页面，所有属于该项目的ns均移除
                    名字空间 - 列表状态（活跃/删除中），跟随ns资源实时更新
                    名字空间 - 列表CPU/内存使用量，监控数据不展示
                    名字空间 - admin更新项目名称，列表中所属项目字段更新
                    名字空间 - 所属项目不支持点击跳转
                    名字空间 - 有「管理名字空间配额」权限，点击可进去详情，详情与admin视角一致
                    名字空间 - 名字空间详情，基本信息不展示CPU/内存使用量
                    名字空间 - 属于System项目的namespace，展示操作按钮「编辑名字空间配额」但不支持操作
                    名字空间 - Pod数量，不具有pod查看权限时，展示为「-」
                    租户视角，编辑名字空间配额，admin视角验证产生CreateNamespaceQuota事件
                    租户视角，更新名字空间配额，admin视角验证产生UpdateNamespaceQuota事件
                    租户视角，清空名字空间配额，admin视角验证产生DeleteNamespaceQuota事件
                项目列表
                    项目列表 - 仅展示成员所属项目，无查看详情及操作功能，列表数据与admin一致
                    项目列表 - admin更新项目名称，刷新页面，列表名称更新
                    项目列表 - 状态更新（活跃/删除中），根据项目状态实时更新
                    项目列表 - admin创建项目并关联成员，项目列表新增项目
                    项目列表 - admin变更关联ns数量，项目列表名字空间数量更新
                    项目列表 - 成员数量展示为所有项目成员数量
                    项目列表 - 列表CPU使用量、内存使用量、存储使用量不展示
                    项目列表 - admin移除成员对应的一个项目，项目列表更新，移除该项目
                权限控制
                    名字空间 - 不具有「管理名字空间配额」的用户，不展示morebutton「编辑名字空间配额」按钮
                    名字空间 - 不具有「管理名字空间配额」的用户，点击名字空间名称，无交互，不会进入详情
                    名字空间 - 从有「管理名字空间配额」权限切换无权限，不刷新页面，点击编辑名字空间配额，提交时拒绝
                    项目列表 - 项目不在权限控制，被加入项目的用户，始终展示所属项目列表
                    名字空间 - 具有「查看所有资源与配置」权限的用户，点击可以查看名字空间详情
                    名字空间 - 具有「管理所有资源与配置」权限的用户，点击可以查看名字空间详情，可以编辑名字空间配额
            名字空间筛选
                admin视角
                    过滤器
                        默认展示 - 全部名字空间，点击下拉框，均未勾选
                        默认展示 - 根据名字空间归属项目分类展示，System固定最前，最后为无归属项目
                        选择任意项目名称-展示关联该项目下的所有namespace，计数及列表数一致
                        选择无归属项目-展示所有未关联项目的namespace，计数及列表数一致
                        选择类别下单个namespace点击勾选 - 筛选框展示已选择namesapce名称，下拉组件统计勾选数
                        同时选择不同类别下的namespace点击勾选 - 筛选框展示已选择namesapce名称，下拉组件统计勾选数
                        勾选整个项目，项目下所有namespace均被选中，筛选框展示名称，组件计数统计正确
                        勾选多个项目，项目下namespace均被选中，筛选框展示名称，从筛选框删除ns，删除后组件中ns不被选中，计数减少
                        点击全选 - 所有类别及namespace均被选中，筛选框展示全部ns名称，组件计数统计正确
                        点击全选后，点击取消全选，所有namespace均不被选中，计数恢复为0，筛选框清空
                        选择ns后，在筛选框清空全部，namespace均不被选中，计数恢复为0
                        搜索 - 搜索中交互状态反馈
                        搜索 - 无搜索结果时交互反馈
                        搜索 - 模糊匹配，有匹配结果，高亮展示，以%父级项%/%子级项%形式平铺展示匹配项
                        搜索 - 有匹配结果，点击直接勾选，搜索不会清空，可多次选择
                    生效范围
                        筛选 - 在下拉组件内选中后，直接生效过滤，查看所在页对应过滤资源，过滤正确
                        筛选 - 选中过滤ns后，切换不同资源，过滤依旧生效
                        筛选 - 选中过滤ns后，切换不同集群，过滤依旧生效
                        筛选 - 选中过滤ns后，在另一页面修改过滤器，修改后生效，切换页面依旧生效
                        筛选 - 选中过滤ns后，在另一页面清空过滤器，清空后恢复全部资源，切换页面依旧生效
                    过滤项变更
                        创建名字空间  - 创建后查看过滤器，无归属项目内展示该ns
                        删除名字空间  - 删除后查看过滤器，无归属项目内不展示该ns
                        创建项目关联名字空间 - 创建后查看过滤器，展示对应项目，项目内展示关联ns
                        创建项目不关联名字空间 - 创建后查看过滤器，不会展示空项目
                        编辑已有项目关联名字空间 -编辑后查看过滤器，项目内新增关联ns
                        编辑已有项目移除名字空间 -编辑后查看过滤器，项目内移除ns，无归属项目内新增ns
                        删除项目但不删除名字空间 - 删除后查看过滤器，不展示删除项目，项目内ns在无归属项目中展示
                        删除项目且删除名字空间 - 删除后查看过滤器，不展示删除项目和相关ns
                租户视角
                    过滤器交互 - 与admin视角相同
                    租户视角 - 仅展示当前租户所属项目类别下的ns
                    租户视角 - 勾选ns进行过滤，列表展示正确
                    租户视角 - 搜索ns对象，展示所属项目内所有ns匹配项，展示正确
                    租户视角 - admin创建名字空间，租户页面刷新，查看过滤器，不会展示新创建的ns
                    租户视角 - admin创建项目关联名字空间，关联租户，租户页面刷新，查看过滤器，新增项目及关联ns
                    租户视角 - admin创建项目不关联名字空间，关联租户，租户页面刷新，查看过滤器，不会展示新增项目
                    租户视角 - admin编辑项目关联名字空间，关联租户，租户页面刷新，查看过滤器，新增项目及关联ns
                    租户视角 - admin编辑项目移除名字空间，关联租户，租户页面刷新，查看过滤器，项目下移除ns
                    租户视角 - admin删除项目但不删除名字空间，租户页面刷新，查看过滤器，不展示删除项目及ns
                    租户视角 - admin删除项目且删除名字空间，租户页面刷新，查看过滤器，不展示删除项目及ns
                    租户视角 - admin删除项目内名字空间，租户页面刷新，查看过滤器，对应项目不会展示删除的ns
                    租户视角 - 增加ns过滤项后，切换资源，过滤依旧生效
                    租户视角 - 增加ns过滤项后，切换集群 ，过滤依旧生效
                    租户视角 - 增加ns过滤项后，切换页面，修改过滤，切换页面新过滤依旧生效
                    租户视角 -增加ns过滤后，切换无ns页面，展示默认，再切回有ns页面，过滤依旧生效
            用户场景
                创建集群，添加系统项目运维管理员用户，登录用户查看默认初始化状态下资源展示
                系统项目管理员，在开关监控相关组件状态下查看资源展示，资源的实时状态更新
                系统项目管理员，在扩缩节点Updating 状态下查看资源展示，资源的实时状态更新
                系统项目管理员，在触发原地更新 状态下查看资源展示，资源的实时状态更新
                系统项目管理员，在升级k8s版本Upgrading 状态下查看资源展示，资源的实时状态更新
                系统项目管理员，在升级SKS 各状态下查看资源展示，资源的实时状态更新，更新工作集群阶段有更新
                admin视角操作项目成员范围内资源，在项目成员视角查看资源更新
                升级SKS - 从sks1.4升级sks1.5，升级后不会展示更新ytt版本提示，可将1.4 ytt版本更新至1.5，不影响权限
                升级SKS - 从sks1.4升级sks1.5，1.4未创建项目成员，升级后1.5可正常创建及生效
                升级SKS - 从sks1.4升级sks1.5，1.4创建的项目及租户权限，在1.5正常生效，租户视角可展示集群详情
                升级SKS - sks1.3升级到sks1.4，未更新过ytt版本，再继续升级sks1.5，升级失败，需要更新ytt版本后可再次升级
                升级SKS - sks1.3升级到sks1.4，未更新过ytt版本，无法升级，更新ytt版本后升级sks1.5，权限生效，且原有ksc配置不会被覆盖，displayname正常显示
                升级SKS - sks1.3升级到sks1.4，更新过ytt版本，再继续升级sks1.5，升级后权限直接生效，可再次更新ytt版本
    SKS 1.5 改进
        升级
            1.5 改进 - 升级 - 不兼容旧监控 - 管控集群仍然使用旧监控，升级 1.5 任务报错「存在使用旧版监控系统的 SKS 集群。」
            1.5 改进 - 升级 - 不兼容旧监控 - 存在工作集群仍然使用旧监控，升级 1.5 任务报错「存在使用旧版监控系统的 SKS 集群。」
            1.5 改进 - 升级 - 不兼容旧监控 - 管控集群监控未开启，可升级1.5
            1.5 改进 - 升级 - 不允许跨 minor 版本升级 - 1.3.2 版本升级 1.5.0，升级任务失败，报错提示「不支持升级至该版本。」
        展示 ZBS VIP
            1.5 改进 - 展示ZBS VIP - Control Plane 虚拟 IP 移入集群基本信息卡片中展示
            1.5 改进 - 展示ZBS VIP - 集群基本信息卡片中展示 ZBS VIP，无ZBS VIP 配置时不展示
            1.5 改进 - 展示 ZBS VIP - SKS 版本移入「版本信息」卡片展示
            1.5 改进 - 展示 ZBS VIP - 版本信息卡片增加展示 SKS 功能版本，hover 显示tooltip「工作负载集群内置功能对应的 SKS 版本信息。」
            1.5 改进 - 展示 ZBS VIP - 版本信息卡片集群升级状态展示升级中，hover 展示tooltip，Kubernetes 版本位于下方
        统一节点 kubenetes cni plugin 版本
            虚拟机集群
                部署
                    1.5 改进 - cni plugin 版本 - 部署 1.25 版本虚拟机集群，检查虚拟机节点 kubernetes-cni 安装版本应为 1.2.0
                    1.5 改进 - cni plugin 版本 - 部署 1.26 版本虚拟机集群，检查虚拟机节点 kubernetes-cni 安装版本应为 1.2.0
                    1.5 改进 - cni plugin 版本 - 部署 1.27 版本虚拟机集群，检查虚拟机节点 kubernetes-cni 安装版本应为 1.2.0
                    1.5 改进 - cni plugin 版本 - 部署 1.28 版本虚拟机集群，检查虚拟机节点 kubernetes-cni 安装版本应为 1.2.0
                    1.5 改进 - cni plugin 版本 - 部署 1.29 版本虚拟机集群，检查虚拟机节点 kubernetes-cni 安装版本应为 1.3.0
                    1.5 改进 - cni plugin 版本 - 部署 1.30 版本虚拟机集群，检查虚拟机节点 kubernetes-cni 安装版本应为 1.4.0
                升级
                    1.5 改进 - cni plugin 版本 - 依次升级 1.25 版本虚拟机集群到 1.28 版本，检查物理机节点 kubernetes-cni 版本保持 1.2.0 不变
                    1.5 改进 - cni plugin 版本 - 升级 1.28 版本虚拟机集群到 1.29 版本，检查虚拟机节点 kubernetes-cni 版本由 1.2.0 升级为 1.3.0
                    1.5 改进 - cni plugin 版本 - 升级 1.29 版本虚拟机集群到 1.30 版本，检查虚拟机节点 kubernetes-cni 版本由 1.3.0 升级为 1.4.0
            物理机
                1.5 改进 - cni plugin 版本 - file server 的 binary-package 目录中不再有 cni-plugins 的包
                1.5 改进 - cni plugin 版本 - 初始化 rocky 8.9 x86 物理机， 不再安装 kubernetes-cni
                1.5 改进 - cni plugin 版本 - 初始化 rocky 8.10 x86 物理机， 不再安装 kubernetes-cni
                1.5 改进 - cni plugin 版本 - 初始化 ubuntu 22.04.3 x86 物理机， 不再安装 kubernetes-cni
                1.5 改进 - cni plugin 版本 - 初始化 openEuler 22.03 sp2 x86 物理机， 不再安装 kubernetes-cni
                1.5 改进 - cni plugin 版本 - 初始化 openEuler 22.03 sp3 x86 物理机， 不再安装 kubernetes-cni
                1.5 改进 - cni plugin 版本 - 初始化 openEuler 22.03 sp2 aarch64 物理机， 不再安装 kubernetes-cni
                1.5 改进 - cni plugin 版本 - 初始化 openEuler 22.03 sp3 aarch64 物理机， 不再安装 kubernetes-cni
                1.5 改进 - cni plugin 版本 - 初始化 kylin v10 sp2 aarch64 物理机， 不再安装 kubernetes-cni
                1.5 改进 - cni plugin 版本 - 初始化 kylin v10 sp3 2403 aarch64 物理机， 不再安装 kubernetes-cni
                1.5 改进 - cni plugin 版本 - 初始化 kylin v10 sp2 x86 物理机， 不再安装 kubernetes-cni
                1.5 改进 - cni plugin 版本 - 初始化 kylin v10 sp3 2403 x86 物理机， 不再安装 kubernetes-cni
            物理机集群
                部署
                    1.5 改进 - cni plugin 版本 - 部署 1.25 版本物理机集群，检查 rocky 8.9 x86 物理机节点 kubernetes-cni 安装版本应为 1.2.0
                    1.5 改进 - cni plugin 版本 - 部署 1.28 版本物理机集群，检查 ubuntu 22.04.3 x86 物理机节点 kubernetes-cni 安装版本应为 1.2.0
                    1.5 改进 - cni plugin 版本 - 部署 1.27 版本物理机集群，检查 kylin v10 x86 物理机节点 kubernetes-cni 安装版本应为 1.2.0
                    1.5 改进 - cni plugin 版本 - 部署 1.26 版本物理机集群，检查 openEuler 22.03 sp2 x86 物理机节点 kubernetes-cni 安装版本应为 1.2.0
                    1.5 改进 - cni plugin 版本 - 部署 1.29 版本物理机集群，检查 rocky 8.10 x86 物理机节点 kubernetes-cni 安装版本应为 1.3.0
                    1.5 改进 - cni plugin 版本 - 部署 1.30 版本物理机集群，检查 rocky 8.10 x86 物理机节点 kubernetes-cni 安装版本应为 1.4.0
                    1.5 改进 - cni plugin 版本 - 部署 1.29 版本物理机集群，检查 ubuntu 22.04.3 x86 物理机节点 kubernetes-cni 安装版本应为 1.3.0
                    1.5 改进 - cni plugin 版本 - 部署 1.30 版本物理机集群，检查 ubuntu 22.04.3 x86 物理机节点 kubernetes-cni 安装版本应为 1.4.0
                    1.5 改进 - cni plugin 版本 - 部署 1.29 版本物理机集群，检查 kylin v10 x86 物理机节点 kubernetes-cni 安装版本应为 1.3.0
                    1.5 改进 - cni plugin 版本 - 部署 1.30 版本物理机集群，检查 kylin v10 x86 物理机节点 kubernetes-cni 安装版本应为 1.4.0
                    1.5 改进 - cni plugin 版本 - 部署 1.29 版本物理机集群，检查 openEuler 22.03 sp3 x86 物理机节点 kubernetes-cni 安装版本应为 1.3.0
                    1.5 改进 - cni plugin 版本 - 部署 1.30 版本物理机集群，检查 openEuler 22.03 sp3 x86 物理机节点 kubernetes-cni 安装版本应为 1.4.0
                    1.5 改进 - cni plugin 版本 - 部署 1.29 版本物理机集群，检查 kylin v10 aarch64 物理机节点 kubernetes-cni 安装版本应为 1.3.0
                    1.5 改进 - cni plugin 版本 - 部署 1.30 版本物理机集群，检查 kylin v10 aarch64 物理机节点 kubernetes-cni 安装版本应为 1.4.0
                    1.5 改进 - cni plugin 版本 - 部署 1.29 版本物理机集群，检查 openEuler 22.03 sp3 aarch64 物理机节点 kubernetes-cni 安装版本应为 1.3.0
                    1.5 改进 - cni plugin 版本 - 部署 1.30 版本物理机集群，检查 openEuler 22.03 sp3 aarch64 物理机节点 kubernetes-cni 安装版本应为 1.4.0
                升级
                    1.5 改进 - cni plugin 版本 - 依次升级 1.25 版本物理机集群到 1.28 版本，检查物理机节点 kubernetes-cni 版本保持 1.2.0 不变
                    1.5 改进 - cni plugin 版本 - 升级 1.28 版本物理机集群到 1.29 版本，检查物理机节点 kubernetes-cni 版本由 1.2.0 升级为 1.3.0
                    1.5 改进 - cni plugin 版本 - 升级 1.29 版本物理机集群到 1.30 版本，检查物理机节点 kubernetes-cni 版本由 1.3.0 升级为 1.4.0
        tower中不再部署不需要的 SKS 组件
            1.5 改进 - SKS 组件 - 新部署的 SKS 1.5 及以上版本，tower 中不再部署 cloudtty 组件
            1.5 改进 - SKS 组件 - 升级 SKS 1.4 到 SKS 1.5 及以上版本，tower 中 cloudtty 组件副本数缩容到0
        优化CA的k8s版本映射逻辑
            创建v1.25版本集群并开启自动伸缩，验证addon版本-1.25.3，且与使用镜像版本相同
            创建v1.26版本集群并开启自动伸缩，验证addon版本-1.26.8，且与使用镜像版本相同
            创建v1.27版本集群并开启自动伸缩，验证addon版本-1.27.8，且与使用镜像版本相同
            创建v1.28版本集群并开启自动伸缩，验证addon版本-1.28.7，且与使用镜像版本相同
            创建v1.29版本集群并开启自动伸缩，验证addon版本-1.29.5，且与使用镜像版本相同
            创建v1.30版本集群并开启自动伸缩，验证addon版本-1.30.4，且与使用镜像版本相同
            连续从v1.25版本升级到v1.30，验证升级addon版本随之升级，且实际使用镜像版本升级
            验证v1.26版本集群自动伸缩功能是否可正常扩缩
        移除升级SKS自动触发滚动集群的相关代码
            SKS1.4升级SKS1.5，验证升级流程，不会触发工作集群滚动更新，升级中滚动管控集群节点时addon不会暂停更新
            SKS1.4升级到SKS1.5后，首次触发原地更新，不会自动触发滚动更新
            SKS1.4升级到SKS1.5后，首次编辑节点组，不会自动触发滚动更新
            SKS1.4升级到SKS1.5后，升级工作集群k8s版本，触发滚动更新， 可正常升级成功
            SKS1.4升级SKS1.5，升级1+1dev管控集群
            SKS1.4升级SKS1.5，升级3+3 高可用管控集群
    事件独立展示
        使用前提
            功能启用/关闭 - SKS系统服务 - 设置 - SKS服务运维 - 可观测性配置 - 功能启用状态
            SKS系统服务 - 已关联obs1.4.2及以上且开启了「启用功能状态」按钮 - 事件页面可展示数据
            SKS系统服务 - 已关联obs1.4.1及以上且开启了「启用功能状态」按钮 - 检查ksc.spec.components.logging.eventagent以及status.externalServices.observabilityServices
            工作负载集群 - 已关联obs1.4.2及以上且插件管理页面开启了事件 - 事件页面可展示数据
            升级 - 工作负载集群 - 已关联obs1.4.0且插件管理页面开启了日志的低于1.5版本 - 旧版日志，事件页面不启用
            关闭事件 - 工作负载集群 - 插件管理 - 事件 - 删除event addon
            关闭事件 - SKS系统服务 - 设置 - SKS服务运维 - 可观测性配置 -  关闭「关联可观测性服务」- 事件随之关闭
            SKS系统服务 - 事件关闭后，不切换obs，再次开启事件，7天内旧数据还存在
            SKS系统服务 - 事件关闭后，切换obs再重新开启事件，无旧数据展示
            工作负载集群 - 事件关闭后，不切换obs，再次开启事件，7天内旧数据还存在
            工作负载集群 - 事件关闭后，切换obs再重新开启事件，无旧数据展示
        UI校验
            功能入口 - SKS系统服务 - 可观测性设置 - 「功能启用状态」统一配置监控、报警、日志、事件和审计功能的启用与关闭
            SKS系统服务 - 可观测性设置 - Outstanding Tip文案更新：统一配置监控、报警、日志、事件和审计功能的启用状态。
            功能入口 - 工作负载集群 - 插件管理 - 可观测性 - 与监控、报警、日志、审计同一层级
            SKS系统服务 - 事件页面表单
                筛选 - 筛选框 - 最小宽度370px，根据viewport宽度自适应
                筛选 - 筛选框 - 筛选项展示规则 - 筛选项展示规则：对象数组类筛选不展示逻辑符号「举例：包含xxx及N项」
                筛选 - 筛选框 - 筛选项展示规则 - 筛选项展示规则：字符串类筛选的逻辑符号为「包含」（审计筛选没有该类型，事件筛选存在）
                筛选 - 筛选框 - 筛选项展示规则 - 筛选项展示规则：数值类筛选的逻辑符号统一使用运算符数学符号而非汉字（当前筛选没有该类型）
                筛选 - 筛选框 - 筛选项展示规则 - 筛选项展示规则：筛选 tag最大宽度为 300px，若第一项显示空间不足时，截断打点显示
                筛选 - 筛选框 - 单个筛选条件标签 - 包含单个label时 - 全部展示
                筛选 - 筛选框 - 单个筛选条件标签 - 包含多个label  - 仅展示第一个label，剩下以「及N项」展示，hover时tooltip展示完整的筛选内容及逻辑关系
                筛选 - 筛选框 - 单个筛选条件标签 - 包含多个label  - 筛选结果取并集「筛选条件之间显示为“或”」
                筛选 - 筛选框 - 多个筛选条件标签 - 筛选结果取交集「筛选条件之间显示为“且”」
                筛选 - 筛选框 - 多个筛选条件标签 - 当筛选输入框宽度无法完整显示筛选条件标签时，其余筛选标签以「… 及 N 个条件」显示
                筛选 - 筛选框 - 多个筛选条件标签 - 宽度不够时，省略展示，并在 hover 时 tooltip 显示其余完整的筛选条件：     展示格式为：%序号%+%端点范围%+%筛选项%+%逻辑符号%+%筛选条件%，若仅有一个条件，则不展示序号。
                筛选 - 筛选框 - 多个筛选条件标签 - 文字距离清空筛选条件按钮最小为 8px
                筛选 - 筛选框 - 清空筛选条件 - hover 时tooltip 提示“清空筛选条件”
                筛选 - 筛选菜单 - 所有筛选条件默认值为空（范围是全部），有默认填充placeholder文案
                筛选 - 筛选菜单 - 时间段内实际有的对象/参数才会成为筛选项，非直接展示全部
                筛选 - 筛选菜单 - 筛选示意 - 筛选框提供搜索能力
                筛选 - 筛选菜单 - 筛选示意 - 对象数组类型通常为多选输入框（Token Field），下拉菜单第一选项为「全部」
                筛选 - 筛选菜单 - 筛选项 - 留空则视为全部对象，不针对该条件进行筛选
                筛选 - 筛选菜单 - 名字空间、对象类型和对象 - 3个筛选条件层级并列，选择一个筛选条件后，其他的筛选条件的选项需要做相应调整以符合已选项的限定范围
                筛选 - 筛选菜单 - 名字空间、对象类型和对象 - 清除任意筛选条件，另外2个筛选条件不会联动同步清除
                筛选 - 筛选菜单 - 筛选项（名字空间）- 字段类型（对象数组「多选」）- 取值（全部、事件关联的资源类型所在的名字空间（非必有，筛选项可能为空））
                筛选 - 筛选菜单 - 筛选项（名字空间）- 取值：空 - 筛选出该字段为空的事件
                筛选 - 筛选菜单 - 筛选项（类型）- 字段类型（对象数组「多选」）- 取值（全部、正常、警告）
                筛选 - 筛选菜单 - 筛选项（原因）- 字段类型（对象数组「多选」）- 取值（全部、采取行动的原因（如create））
                筛选 - 筛选菜单 - 筛选项（对象类型）- 字段类型（对象数组「多选」）- 取值（全部、事件所涉及的对象类型）
                筛选 - 筛选菜单 - 筛选项（对象）- 字段类型（对象数组「多选」）- 取值（全部、事件所涉及的对象名称）
                筛选 - 筛选菜单 - 筛选项（事件信息）- 字段类型（字符串「需先选逻辑：包含/不包含，默认为包含」）- 取值（输入关键字搜索）
                筛选 - 筛选菜单 - 筛选项（来源）- 字段类型（对象数组「多选」）- 取值（全部、事件来源组件（如kubelet，用户手动创建则无该字段））
                时间范围选择器 - 选定时间后，对应的语义为：查看「最近发生时间」在特定时间段内的事件信息。
                时间范围选择器 - 预定义的相对时间范围默认10min
                时间范围选择器 - 预定义的相对时间范围与旧版日志保持一致：过去10分钟/1小时/3小时/24小时/3天
                时间范围选择器 - 绝对时间最大值为当前时间，大于最大值的时间需禁用处理
                时间范围选择器 - 日期选择输入框固定为 328px。刷新按钮最小宽度为 63px，最大宽度根据自动刷新时间变化
                时间范围选择器 - 自动刷新时间与旧版日志保持一致：关闭/5s/10s/30s/1m/5m，默认选择关闭
                时间范围选择器 - 关闭自动刷新时间，事件列表不再自动刷新
                表格
                    表格数据 - 不分页，默认加载 1000 条（若事件内容数量小于默认值时，以实际内容数为准）
                    表格数据 - 不分页，默认加载 1000 条（若超出默认加载数量时，滚动加载，表格下方显示「加载中…」示意加载状态。）
                    表格字段 - 所有列均可调节宽度，最小宽度均为 90px，文字过长时打点截断，hover 展示完整名称 tooltip
                    表格字段 - 默认排序规则为：按照最近发生时间倒序排序（最新的事件信息展示在最上方）
                    表格字段 - 名字空间 - 取值&示例「default」- 列默认宽度：150px - 不支持交互/不支持排序/默认显示
                    表格字段 - 名字空间 - 没有值时展示「-」
                    表格字段 - 类型 - 取值&示例「正常/警告」- 列默认宽度：100px - 不支持交互/不支持排序/默认显示
                    表格字段 - 原因 - 取值&示例「Pulled」- 列默认宽度：100px - 不支持交互/不支持排序/默认显示
                    表格字段 - 对象类型 - 取值&示例「Pod」- 列默认宽度：120px - 不支持交互/不支持排序/默认显示
                    表格字段 - 对象 - 取值&示例「nginx-xxx」- 列默认宽度：150px - 不支持交互/不支持排序/默认显示
                    表格字段 - 事件信息 - 取值&示例「xxx」- 列默认宽度：200px - 不支持交互/不支持排序/默认显示
                    表格字段 - 来源 - 取值&示例「kubelet」- 列默认宽度：100px - 不支持交互/不支持排序/默认显示
                    表格字段 - 来源 - 没有值时展示「-」
                    表格字段 - 发生次数 - 取值&示例「数值」- 列默认宽度：100px - 不支持交互/不支持排序/默认显示
                    表格字段 - 最近发生时间 - 取值&示例「2025-05-10 07:42:34」- 列默认宽度：150px - 不支持交互/不支持排序/默认显示
                    表格字段 - 首次发生时间 - 取值&示例「2025-05-10 07:42:34」- 列默认宽度：150px - 不支持交互/不支持排序/默认显示
                    more button - 任意事件后more button，点击「查看详情」- 弹出事件详情弹窗
                    more button - 任意事件后more button，点击「查看详情」- 弹出事件详情弹窗 - 弹窗内字体与颜色填充校验
                    more button - 任意事件后more button，点击「查看详情」- 弹出事件详情弹窗 - 事件详情弹窗规格宽度1024px，高度640px，内容无法展示完整时，body内滚动，header吸顶
                不同状态下的页面展示
                    空状态 - 未开启事件功能 - 页面提示：在可观测性配置中可开启事件功能，按钮点击可跳转
                    空状态 - 无匹配筛选条件的事件 - 展示：没有匹配筛选条件的事件，「清空筛选条件」按钮点击可返回原始页面
                    空状态 - 当前时间段内无数据 - 展示提示文案：当前时间段内无数据
            SKS系统服务 - 集群事件功能优化
                展示位置保持不变 - 管控集群信息页 - 事件
                展示位置保持不变 - 管控集群信息页 - 事件 - hover事件后的info icon时，tooltip提示：实时展示集群1小时内的事件信息
                展示列表字段 - 与「事件」页面对齐：名字空间，类型，原因，对象类型，对象，事件信息，来源，发生次数，最近发生时间，首次发生时间，所有字段默认展示
                展示列表字段 - 与「事件」页面对齐，点击自定义列按钮，可取消勾选展示列
                展示列表more button - 任意事件后more button可点击「查看详情」，弹出事件详情弹窗
                展示列表more button - 任意事件后more button可点击「查看详情」，弹出事件详情弹窗，弹窗规格宽度1024px,高度640px
                展示列表more button - 任意事件后more button可点击「查看详情」，弹出事件详情弹窗，点击右上角「x」关闭弹窗
                展示列表 - 查看更多 - 点击，可跳转至SKS系统服务的设置页面
                展示列表 - 分页 - 每页展示20条数据，可正常切换分页跳转
                空状态 - 暂无数据 - 1小时内没有新生成的事件数据展示
                空状态 - 暂无数据 - 点击「查看更多」- 跳转到SKS系统服务设置页面
                空状态 - 获取数据遇到问题 - 点击「重试」按钮可进行重新获取数据展示
                空状态 - 获取数据遇到问题 - 点击「查看更多」- 跳转到SKS系统服务设置页面
                插件展示
                    概览页 - 管控集群插件状态card - 开启事件后，新增obs-event-agent插件
                    概览页 - 管控集群插件状态card - 关闭事件后，obs-event-agent插件被清理
                    概览页 - 管控集群插件状态card - 开启事件后，新增obs-event-agent插件 - 就绪展示
                    概览页 - 管控集群插件状态card - 开启事件后，新增obs-event-agent插件 - 异常展示
                    概览页 - 管控集群插件状态card - 开启事件后，新增obs-event-agent插件 - 开启中展示
                    概览页 - 管控集群插件状态card - 开启事件后，新增obs-event-agent插件 - 关闭中展示
                    概览页 - 管控集群插件状态card - 开启事件后，新增obs-event-agent插件 - reconciling展示
            工作负载集群
                功能入口 - 创建工作负载集群 - 插件配置 - 可观测性 - 事件「日志和审计之间」
                功能入口 - 编辑工作负载集群 - 插件管理 - 可观测性 - 事件「日志和审计之间」
                功能启用 - 需要关联1.4.1及以上版本的可观测性服务后，才可单独开启事件
                功能启用 - 已关联1.4.2及以上版本的可观测性服务后，单独开启事件，可在事件页面查看事件信息
                功能关闭 - 事件功能开启后，可独立关闭
                功能关闭 - 事件功能开启后，关闭「关联可观测性服务」，事件功能也随之关闭
                功能关闭 - 事件功能关闭后，不切换其他obs，使用旧obs再次开启，7天内的旧数据还可以查看
                功能关闭 - 事件功能关闭后，切换其他obs后再次开启，数据从开启后开始展示
                创建工作负载集群
                    创建虚拟机工作负载集群 - 插件配置 - 可观测性 - 未关联1.4.2及以上的obs服务，事件无法开启，按钮禁用有提示
                    创建虚拟机工作负载集群 - 插件配置 - 可观测性 - 已关联1.4.2及以上的obs服务，事件可以开启，按钮解除禁用提示消失
                    创建物理机工作负载集群 - 插件配置 - 可观测性 - 已关联1.4.2及以上的obs服务，开启事件，默认展示OBS-Event-Agent参数配置
                    编辑工作负载集群 - 插件管理 - 可观测性 - 开启事件后可配置的OBS-Event-Agent参数配置
                    新建工作负载集群 - 插件参数配置 - 新增可配置参数 - 默认不配置 - 创建成功后只有resource的默认值
                    创建工作负载集群 - 插件参数配置 - 新增可配置参数 - 配置extraDataLabels - 向日志数据添加额外的标签，配置成功后在新生成的event的log中查询
                    创建工作负载集群 - 插件参数配置 - 新增可配置参数 - 配置extraArgs - 校验pod中应用成功
                    创建工作负载集群 - 插件参数配置 - 新增可配置参数 - 配置非默认的resources - 创建成功后检查，非默认resources值
                    编辑工作负载集群 - 插件参数配置 - 新增可配置参数 - 采集主机的事件，配置agent.extraVolumeMounts，extraVolumes
                    编辑工作负载集群 - 插件参数配置 - 新增可配置参数 - 发送事件到外部系统，配置extraSinks
                    编辑工作负载集群 - 插件参数配置 - 可配置参数 - 编辑配置非默认的resources - 编辑成功后检查，是配置的resources值
                    编辑工作负载集群 - 插件参数配置 - 删除所有已增加的配置参数 - 删除成功
                事件页面列表表单
                    筛选
                        筛选 - 筛选框 - 单个筛选条件标签 - 包含单个label时 - 全部展示
                        筛选 - 筛选框 - 单个筛选条件标签 - 包含多个label  - 仅展示第一个label，剩下以「及N项」展示，hover时tooltip展示完整的筛选内容及逻辑关系
                        筛选 - 筛选框 - 单个筛选条件标签 - 包含多个label  - 筛选结果取并集「筛选条件之间显示为“或”」
                        筛选 - 筛选框 - 多个筛选条件标签 - 筛选结果取交集「筛选条件之间显示为“且”」
                        筛选 - 筛选框 - 多个筛选条件标签 - 当筛选输入框宽度无法完整显示筛选条件标签时，其余筛选标签以「… 及 N 个条件」显示
                        筛选 - 筛选框 - 多个筛选条件标签 - 宽度不够时，省略展示，并在 hover 时 tooltip 显示其余完整的筛选条件：     展示格式为：%序号%+%端点范围%+%筛选项%+%逻辑符号%+%筛选条件%，若仅有一个条件，则不展示序号。
                        筛选 - 筛选框 - 清空筛选条件 - hover 时tooltip 提示“清空筛选条件”
                        筛选 - 筛选菜单 - 所有筛选条件默认值为空（范围是全部），有默认填充placeholder文案
                        筛选 - 筛选菜单 - 时间段内实际有的对象/参数才会成为筛选项，非直接展示全部
                        筛选 - 筛选菜单 - 筛选示意 - 筛选框提供搜索能力
                        筛选 - 筛选菜单 - 筛选示意 - 对象数组类型通常为多选输入框（Token Field），下拉菜单第一选项为「全部」
                        筛选 - 筛选菜单 - 筛选项 - 留空则视为全部对象，不针对该条件进行筛选
                        筛选 - 筛选菜单 - 名字空间、对象类型和对象 - 3个筛选条件层级并列，选择一个筛选条件后，其他的筛选条件的选项需要做相应调整以符合已选项的限定范围
                        筛选 - 筛选菜单 - 名字空间、对象类型和对象 - 清除任意筛选条件，另外2个筛选条件不会联动同步清除
                        时间范围选择器 - 预定义的相对时间范围与旧版日志保持一致：过去10分钟/1小时/3小时/24小时/3天
                        时间范围选择器 - 绝对时间最大值为当前时间，大于最大值的时间需禁用处理
                        时间范围选择器 - 自动刷新时间与旧版日志保持一致：关闭/5s/10s/30s/1m/5m
                        时间范围选择器 - 关闭自动刷新时间，事件列表不再自动刷新
                    表格
                        表格数据 - 不分页，默认加载 1000 条（若事件内容数量小于默认值时，以实际内容数为准）
                        表格数据 - 不分页，默认加载 1000 条（若超出默认加载数量时，滚动加载，表格下方显示「加载中…」示意加载状态。）
                        表格字段 - 默认排序规则为：按照最近发生时间倒序排序（最新的事件信息展示在最上方）
                        表格字段 - 名字空间 - 取值&示例「default」- 列默认宽度：150px - 不支持交互/不支持排序/默认显示
                        表格字段 - 类型 - 取值&示例「正常/警告」- 列默认宽度：100px - 不支持交互/不支持排序/默认显示
                        表格字段 - 原因 - 取值&示例「Pulled」- 列默认宽度：100px - 不支持交互/不支持排序/默认显示
                        表格字段 - 对象类型 - 取值&示例「Pod」- 列默认宽度：120px - 不支持交互/不支持排序/默认显示
                        表格字段 - 对象 - 取值&示例「nginx-xxx」- 列默认宽度：150px - 不支持交互/不支持排序/默认显示
                        表格字段 - 事件信息 - 取值&示例「xxx」- 列默认宽度：200px - 不支持交互/不支持排序/默认显示
                        表格字段 - 发生次数 - 取值&示例「数值」- 列默认宽度：100px - 不支持交互/不支持排序/默认显示
                        表格字段 - 最近发生时间 - 取值&示例「2025-05-10 07:42:34」- 列默认宽度：150px - 不支持交互/不支持排序/默认显示
                        表格字段 - 首次发生时间 - 取值&示例「2025-05-10 07:42:34」- 列默认宽度：150px - 不支持交互/不支持排序/默认显示
                        more button - 任意事件后more button，点击「查看详情」- 弹出事件详情弹窗
                        more button - 任意事件后more button，点击「查看详情」- 弹出事件详情弹窗 - 事件详情弹窗规格宽度1024px，高度640px，内容无法展示完整时，body内滚动，header吸顶
                    不同状态下的页面展示
                        空状态 - 未开启事件功能 - 页面提示：需要在可观测性配置中开启事件功能，按钮点击可跳转
                        空状态 - 无匹配筛选条件的事件 - 展示：没有匹配筛选条件的事件，「清空筛选条件」按钮点击可返回原始页面
                        空状态 - 当前时间段内无数据 - 展示提示文案：当前时间段内无数据
                        空状态 - 可观测性异常 - 展示提示文案：可观测性服务数据获取异常
                        空状态展示优先级 - 可观测性服务异常/集群与可观测性服务关联异常时，监控、报警、日志、事件和审计页面优先展示：可观测性服务数据获取异常
                集群概览页 - 集群事件功能优化
                    展示位置保持不变 - 集群概览页 - 事件
                    展示位置保持不变 - 集群概览页 - 事件card尺寸：宽度随 Viewport 自适应；最小高度：113px，最大高度：400px。表格高度随内容项变化
                    展示位置保持不变 - 集群概览页 - 事件 - hover事件后的info icon时，tooltip提示：实时展示集群1小时内的事件信息
                    展示列表字段 - 与「事件」页面对齐，点击自定义列按钮，可取消勾选展示列
                    展示列表more button - 任意事件后more button可点击「查看详情」，弹出事件详情弹窗
                    展示列表more button - 任意事件后more button可点击「查看详情」，弹出事件详情弹窗，弹窗规格宽度1024px,高度640px
                    展示列表more button - 任意事件后more button可点击「查看详情」，弹出事件详情弹窗，点击右上角「x」关闭弹窗
                    展示列表 - 查看更多 - 点击，可跳转至「事件」页面
                    展示列表 - 分页 - 每页展示20条数据，可正常切换分页跳转，空间不足，卡片内滚动查看
                    空状态 - 暂无数据 - 1小时内没有新生成的事件数据展示
                    空状态 - 获取数据遇到问题 - 点击「重试」按钮可进行重新获取数据展示
                    概览页插件展示
                        概览页 - 管控集群插件状态card - 开启事件后，新增obs-event-agent插件
                        概览页 - 管控集群插件状态card - 关闭事件后，obs-event-agent插件被清理
            升级版本后的页面影响
                升级后，内置和默认策略保存在全局 ClusterConfiguration 中,predefinedPolicy.name:system/normal/simple/detailed
                升级前，未关联可观测性服务，未开启日志
                    升级后，未关联obs - 无法开启事件、审计
                    升级后，关联obs1.4.0 - 无法关联，仅支持选择1.4.2及以上，无法开启事件、审计
                    升级后，可观测性部分保持关闭，监控、报警、日志、事件、审计均保持关闭状态
                    升级后，关联obs1.4.2及以上，不开启日志，事件、审计可以开启
                    升级后，已有工作负载集群 - 其他操作触发yttManifests更新，原地更新成功，apiserver audit相关参数保持不变
                    升级后，已有工作负载集群 - 原地更新后，再开启审计，配置审计策略(非默认) - 再次原地更新后，查看ksc有添加的audit策略（与设置的保持一致）
                    升级后，已有工作负载集群 - 直接开启审计配置审计策略 - 开启成功，集群ytt版本会同步更新到1.5，ksc未更新audit策略
                升级前，关联可观测性服务，未开启日志
                    升级前，已关联obs1.4.0 - 升级后，日志禁用，事件、审计也无法开启
                    升级前，已关联obs1.4.0 - 升级后，升级obs至1.4.2及以上且集群功能版本>=1.5,可开启日志、事件、审计
                    升级前，已关联obs1.4.0 - 升级后，切换新的obs1.4.2及以上,可开启日志、事件、审计
                    升级前，已关联obs1.4.2及以上 - 升级后，可直接开启事件、审计
                升级前，未关联可观测性服务，开启日志
                    工作负载集群 - 升级后，仅旧版日志默认开启，事件、审计禁用不可开启，事件、审计页面是未开启的空状态
                    工作负载集群 - 升级后，关联obs1.4.2及以上但保持旧版日志不切换 - 事件、审计禁用不可开启
                    工作负载集群 - 升级后，关联obs1.4.1及以上且切换为新版日志 - 事件、审计解除禁用状态，可独立开启
                    工作负载集群 - 升级后，关联obs1.4.2及以上且切换为新版日志 - 事件、审计解除禁用状态，可独立开启，事件开启后，旧事件数据随日志迁移过来的正常展示
                    管控集群 - 升级后，旧版日志默认开启但是不可用，事件、审计不可开启，关联obs后才可以开启「功能启用状态」
                    A - 管控集群 - 升级后，审计策略预期自动更新设置为 system - 检查ksc中审计策略文件参数与clusterconfiguration 中定义的system一致
                    管控集群 - 升级后，开启关联可观测性服务并开启「功能启用状态」- 保存成功后，审计、事件一并开启成功
                升级前，已关联可观测性服务，已开日志
                    工作负载集群 - 升级前，已关联obs1.4.2及以上并开启日志 - 升级后，可观测性保持关联，旧版日志保持开启，事件、审计禁用不可开启，提示需切换为新版日志功能后才能开启
                    工作负载集群 - 升级前，已关联obs1.4.2及以上并开启日志 - 升级后，切换为新版日志并迁移旧数据，事件、审计解除禁用状态，可独立开启
                    工作负载集群 - 升级前，已关联obs1.4.1及以上并开启日志 - 升级后，切换为新版日志并迁移旧数据，切换后，事件host、involvedObject_name标签在筛选中不可用
                    工作负载集群 - 升级前，已关联obs1.4.0并开启日志 - 升级后，旧版日志保持开启，事件、审计需要切换新版日志后才能开启
                    工作负载集群 - 升级前，已关联obs1.4.0并开启日志 - 升级后，升级已关联obs至1.4.1及以上版本，切换日志为新版日志后，事件、审计解除禁用状态，可独立开启
                    工作负载集群 - 升级前，已关联obs1.4.0并开启日志 - 升级后，直接切换为obs1.4.1及以上版本，并切换日志为新版日志后，事件、审计解除禁用状态，可独立开启
                    管控集群 - 升级前，已关联obs1.4.2及以上并开启日志 - 升级后，保持旧版日志，提示：旧版日志不可用，需要切换新版日志，事件、审计才可启用
                    管控集群 - 升级前，已关联obs1.4.1及以上并开启日志 - 升级后，关闭旧版日志并清除旧数据 - 勾选「关闭旧版日志并清除旧数据」按钮后保存 - 清除成功，日志相关pv等资源被清理
                    管控集群 - 升级前，已关联obs1.4.1及以上并开启日志 - 升级后，先关闭旧版日志并清除旧数据再启用新版日志功能 - 勾选「启用新版日志功能」按钮后保存 - 启用成功，事件、审计被一并启用
                    管控集群 - 升级前，已关联obs1.4.2及以上并开启日志 - 升级后，直接切换为新版日志并迁移旧数据 - 启用成功，事件、审计被一并启用，notice tip提示消失
                    管控集群 - 升级前，已关联obs1.4.0并开启日志 - 升级后，旧版日志保持开启，无法开启新版日志、事件、审计
                    管控集群 - 升级前，已关联obs1.4.0并开启日志 - 升级后，升级已关联的obs至1.4.2及以上，切换为新版日志 - 事件、审计随之开启
                    管控集群 - 升级前，已关联obs1.4.0并开启日志 - 升级后，切换为obs1.4.1及以上，切换为新版日志 - 事件、审计随之开启
        筛选事件信息
            单筛选条件 - 名字空间/类型/原因/对象类型/对象/事件信息/来源 - 任选一筛选条件 - 正确匹配筛选结果
            单筛选条件 - 时间区间筛选 - 正确匹配筛选结果
            多筛选条件 - 时间区间+筛选字段 - 正确匹配筛选结果
            多筛选条件 - 筛选条件数量限制上限 - 无上限
            loki label筛选事件
                kubenetes事件 - {cluster="xxxx",source_type="kubernetes_events"} - 与kubectl结果比对
                指定namespace下的事件 - {cluster="xxxx",source_type="kubernetes_events", involvedobject_namespace ="xxx"}
                指定type的事件 - {cluster="xxxx",source_type="kubernetes_events",type="Normal/Warning"}
                指定reason的事件 - {cluster="xxxx",source_type="kubernetes_events",reason="xxx"}
                指定involved object事件 - {cluster="xxxx",source_type="kubernetes_events",involvedobject_kind="Pod"}
                指定component的事件 - {cluster="xxxx",source_type="kubernetes_events",component="xxx"}
                指定involvedobject_name的事件 - {cluster="xxxx",source_type="kubernetes_events",involvedobject_name="xxx"}
                指定involved object的namspace的事件 - {cluster="xxxx",source_type="kubernetes_events",involvedobject_namespace="xxx"}
                指定message关键字的事件 - {cluster="xxxx",source_type="kubernetes_events",message="xxx"}
                指定对象apiVersion的事件 - {cluster="xxxx",source_type="kubernetes_events",involvedobject_apiversion="xxx"}
        已有功能影响
            报警
                新增报警规则 - 集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中事件的组件 {{ $labels.daemonset }} 异常持续 15 分钟。
                新增报警规则 - 集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中审计的组件 {{ $labels.daemonset }} 异常持续 15 分钟。 - 开启审计日志时创建规则，在ovm rule里检查
                触发新增报警规则 - 集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中事件的组件 {{ $labels.daemonset }} 异常持续 15 分钟。
    SKS审计
        功能入口 - 创建工作负载集群 - 插件配置 - 可观测性 - 「事件」功能之下
        功能入口 - 编辑工作负载集群 - 插件管理 - 可观测性 - 「事件」功能之下
        功能入口 - SKS系统服务 - 可观测性设置 - 「功能启用状态」统一配置监控、报警、日志、事件和审计功能的启用与关闭
        使用前提
            功能启用/关闭 - SKS系统服务 - 设置 - SKS服务运维 - 可观测性配置 - 功能启用状态
            SKS系统服务 - 已关联obs1.4.2及以上且开启了「启用功能状态」按钮 - 审计页面可展示数据，启用后配置默认的审计策略:ksc.clusterConfiguration.audit.kubeAPIServer.usePolicy: system
            SKS系统服务 - 已关联obs1.4.2及以上且开启了「启用功能状态」按钮 - 检查ksc.spec.components.logging.auditagent以及status.externalServices.observabilityServices
            工作负载集群 - 已关联obs1.4.2及以上且插件管理页面开启了审计 - 审计页面可展示数据，启用时需要选择一种审计策略
            关闭审计 - 工作负载集群 - 插件管理 - 审计 - 删除audit addon
            关闭审计 - SKS系统服务 - 设置 - SKS服务运维 - 可观测性配置 -  关闭「关联可观测性服务」- 审计随之关闭
            SKS系统服务 - 审计关闭后，不切换obs，再次开启审计，3个月内旧数据还存在
            SKS系统服务 - 审计关闭后，切换obs再重新开启审计，无旧数据展示
            工作负载集群 - 审计关闭后，不切换obs，再次开启审计，3个月内旧数据还存在
            工作负载集群 - 审计关闭后，切换obs再重新开启审计，无旧数据展示
        UI校验
            工作负载集群
                创建工作负载集群
                    创建虚拟机工作负载集群 - 插件配置 - 可观测性 - 未关联1.4.2及以上的obs服务，审计无法开启，按钮禁用有提示
                    创建虚拟机工作负载集群 - 插件配置 - 可观测性 - 已关联1.4.1及以上的obs服务，审计可以开启，按钮解除禁用提示消失
                    创建物理机工作负载集群 - 插件配置 - 可观测性 - 已关联1.4.2及以上的obs服务，开启审计，显示「审计策略」和「OBS-Audit-Agent参数配置」参数配置框默认收起状态
                    创建工作负载集群时开启审计，「审计策略」默认选项为「基础策略」- 创建成功后检查ksc.spec.clusterConfiguration.audit.kubeAPIServer.usePolicy: normal
                    创建工作负载集群 - 插件配置 - 可观测性 - 仅关联obs不开启审计 - 创建成功,默认审计策略配置为normal策略
                    创建工作负载集群 - 插件配置 - 可观测性 - 仅关联obs不开启审计 - 创建成功后，开启审计并选择默认审计策略：基础策略，保存后，集群不会进入原地更新
                    创建工作负载集群 - 插件配置 - 可观测性 - 仅关联obs不开启审计 - 创建成功后，开启审计更换审计策略为精简策略 - 集群原地更新后ready
                    创建工作负载集群时开启审计，「审计策略」默认选项为「基础策略」- 审计策略下拉框展开，可选策略：精简策略
                    创建工作负载集群时开启审计，「审计策略」默认选项为「基础策略」- 审计策略下拉框展开，可选策略：详细策略
                    创建工作负载集群时开启审计，「审计策略」默认选项为「基础策略」- 切换为「自定义策略」，下方显示yaml配置框，用户可按需自行配置审计策略yaml
                    编辑工作负载集群审计，「审计策略」切换为「自定义策略」，配置错误的yaml内容，异步校验，错误提示在底部反馈
                    创建工作负载集群时开启审计，「审计策略」切换为「自定义策略」，rules中的level为Metadata但是不配置resources或verbs字段，异步校验，错误提示在底部反馈
                    编辑工作负载集群 - 插件管理 - 可观测性 - 开启审计后可配置的OBS-Audit-Agent参数配置
                    新建工作负载集群 - 插件参数配置 - 新增可配置参数 - 默认不配置 - 创建成功后只有resource的默认值
                    创建工作负载集群 - 插件参数配置 - 新增可配置参数 - 配置extraDataLabels:key=value，loki中查询，新生成的审计日志增加label
                    创建工作负载集群 - 插件参数配置 - 新增可配置参数 - 配置extraArgs ，校验pod中应用成功
                    创建工作负载集群 - 插件参数配置 - 新增可配置参数 - 配置非默认的resources - 创建成功后检查，非默认resources值
                    编辑工作负载集群 - 插件参数配置 - 新增可配置参数 - 采集xxx路径的审计日志，配置extraFileInput，extraVolumeMounts，extraVolumes
                    编辑工作负载集群 - 插件参数配置 - 新增可配置参数 - 发送审计到外部系统，配置extraSinks
                    编辑工作负载集群 - 插件参数配置 - 可配置参数 - 编辑配置非默认的resources - 编辑成功后检查，是配置的resources值
                    编辑工作负载集群 - 插件参数配置 - 删除所有已增加的配置参数 - 删除成功
                集群详情 - 插件配置
                    编辑工作负载集群 - 插件管理 - 审计 - 切换审计策略 - 新增Notice tip（英文检查）:切换策略会导致 API Server 重启，需要访问 API Server 的服务可能短时间不可用或自动重连。
                    编辑工作负载集群 - 插件管理 - 审计 - 切换审计策略，保存后集群原地更新，检查ksc是否生效
                    编辑工作负载集群 - 插件管理 - 审计 - 关闭后再开启，保留「审计策略」配置项
                    编辑工作负载集群 - 插件管理 - 关闭「关联可观测性服务」，Notice tip文案调整：关联可观测性服务关闭后，监控、报警、日志、事件和审计功能也会自动关闭。
                概览页 - 集群插件状态card
                    概览页 - 集群插件状态card - 开启审计后，新增obs-audit-agent插件
                    概览页 - 集群插件状态card - 关闭审计后，obs-audit-agent插件被清理
            SKS系统服务
                部署SKS1.5 - 默认不开启审计日志收集功能
                概览页  - 集群插件状态card
                    概览页 - 集群插件状态card - 开启审计后，新增obs-audit-agent插件
                    概览页 - 集群插件状态card - 关闭审计后，obs-audit-agent插件被清理
            审计
                筛选
                    筛选 - 筛选框 - 最小宽度370px，根据viewport宽度自适应
                    筛选 - 筛选框 - 筛选项展示规则 - 筛选项展示规则：对象数组类筛选不展示逻辑符号「举例：包含xxx及N项」
                    筛选 - 筛选框 - 筛选项展示规则 - 筛选项展示规则：筛选 tag最大宽度为 300px，若第一项显示空间不足时，截断打点显示
                    筛选 - 筛选框 - 单个筛选条件标签 - 包含单个label时 - 全部展示
                    筛选 - 筛选框 - 单个筛选条件标签 - 包含多个label  - 仅展示第一个label，剩下以「及N项」展示，hover时tooltip展示完整的筛选内容及逻辑关系
                    筛选 - 筛选框 - 单个筛选条件标签 - 包含多个label  - 筛选结果取并集「筛选条件之间显示为“或”」
                    筛选 - 筛选框 - 多个筛选条件标签 - 筛选结果取交集「筛选条件之间显示为“且”」
                    筛选 - 筛选框 - 多个筛选条件标签 - 当筛选输入框宽度无法完整显示筛选条件标签时，其余筛选标签以「… 及 N 个条件」显示
                    筛选 - 筛选框 - 多个筛选条件标签 - 宽度不够时，省略展示，并在 hover 时 tooltip 显示其余完整的筛选条件：     展示格式为：%序号%+%端点范围%+%筛选项%+%逻辑符号%+%筛选条件%，若仅有一个条件，则不展示序号。
                    筛选 - 筛选框 - 多个筛选条件标签 - 文字距离清空筛选条件按钮最小为 8px
                    筛选 - 筛选框 - 清空筛选条件 - hover 时tooltip 提示“清空筛选条件”
                    筛选 - 筛选菜单 - 所有筛选条件默认值为空（范围是全部），有默认填充placeholder文案
                    筛选 - 筛选菜单 - 时间段内实际有的对象/参数才会成为筛选项，非直接展示全部
                    筛选 - 筛选菜单 - 筛选示意 - 筛选框提供搜索能力
                    筛选 - 筛选菜单 - 筛选示意 - 对象数组类型通常为多选输入框（Token Field），下拉菜单第一选项为「全部」
                    筛选 - 筛选菜单 - 筛选项 - 留空则视为全部对象，不针对该条件进行筛选
                    筛选 - 筛选菜单 - 名字空间、资源类型和资源名称 - 3个筛选条件层级并列，选择一个筛选条件后，其他的筛选条件的选项需要做相应调整以符合已选项的限定范围
                    筛选 - 筛选菜单 - 名字空间、资源类型和资源名称 - 清除任意筛选条件，另外2个筛选条件不会联动同步清除
                    筛选 - 筛选菜单 - 筛选项（操作者）- 字段类型（对象数组「多选」）- 取值（全部、执行请求的操作者名称（如Alice））
                    筛选 - 筛选菜单 - 筛选项（操作）- 字段类型（对象数组「多选」）- 取值（全部、get、list、create、update、patch、delete、deletecollection、watch）
                    筛选 - 筛选菜单 - 筛选项（名字空间）- 字段类型（对象数组「多选」）- 取值（全部、目标对象所在的名字空间（非必有，筛选项可能为空））
                    筛选 - 筛选菜单 - 筛选项（资源类型）- 字段类型（对象数组「多选」）- 取值（全部、目标对象的类型（非必有，筛选项可能为空））
                    筛选 - 筛选菜单 - 筛选项（资源名称）- 字段类型（对象数组「多选」）- 取值（全部、目标对象的名称（非必有，筛选项可能为空））
                    筛选 - 筛选菜单 - 筛选项（鉴权结果）- 字段类型（对象数组「多选」）- 取值（全部、允许、拒绝、空）
                    时间范围选择器 - 预定义的相对时间范围默认10min
                    时间范围选择器 - 预定义的相对时间范围与旧版日志保持一致：过去10分钟/1小时/3小时/24小时/3天
                    时间范围选择器 - 自动刷新时间与旧版日志保持一致：关闭/5s/10s/30s/1m/5m
                    时间范围选择器 - 默认关闭自动刷新时间，切换自动刷新时间10s - 审计列表自动刷新
                表格
                    表格数据 - 不分页，默认加载 1000 条（若事件内容数量小于默认值时，以实际内容数为准）
                    表格数据 - 不分页，默认加载 1000 条（若超出默认加载数量时，滚动加载，表格下方显示「加载中…」示意加载状态。）
                    表格字段 - 所有列均可调节宽度，最小宽度均为 90px，文字过长时打点截断，hover 展示完整名称 tooltip
                    表格字段 - 默认排序规则为：按照操作时间倒序排序（最新的审计信息展示在最上方）
                    表格字段 - 操作者 - 取值&示例「Alice」- 列默认宽度：150px - 不支持交互/不支持排序/默认显示
                    表格字段 - 操作 - 取值&示例「get、list、create、update、patch、delete、deletecollection、watch」- 列默认宽度：100px - 不支持交互/不支持排序/默认显示
                    表格字段 - 名字空间 - 取值&示例「default」- 列默认宽度：150px - 不支持交互/不支持排序/默认显示 - 没有值时展示「-」
                    表格字段 - 资源类型 - 取值&示例「Pod」- 列默认宽度：120px - 不支持交互/不支持排序/默认显示 - 没有值时展示「-」
                    表格字段 - 资源名称 - 取值&示例「nginx-xxx」- 列默认宽度：150px - 不支持交互/不支持排序/默认显示 - 没有值时展示「-」
                    表格字段 - 鉴权结果 - 取值&示例「允许、拒绝」- 列默认宽度：100px - 不支持交互/不支持排序/默认显示 - 请求未经过Kubernetes授权层，没有该字段时展示「-」
                    表格字段 - 请求IP - 取值&示例「192.168.1.100」- 列默认宽度：100px - 不支持交互/不支持排序/默认显示
                    表格字段 - 操作时间（requestReceivedTimestamp） - 取值&示例「2024-09-10 05:41:40」- 列默认宽度：150px - 不支持交互/不支持排序/默认显示
                    more button - 任意审计后more button，点击「查看详情」- 弹出审计详情弹窗
                    SKS系统服务 - 审计详情弹窗叠加示意
                不同状态下的页面展示
                    空状态 - 未开启审计功能 - 工作负载集群 - 页面提示：在插件管理中可开启审计功能，「插件管理」按钮可跳转
                    空状态 - 未开启审计功能 - SKS系统服务 - 页面提示：需要在可观测性配置中开启审计功能，按钮点击可跳转
                    空状态 - 无匹配筛选条件的审计 - 展示：没有匹配筛选条件的审计，「清空筛选条件」按钮点击可返回原始页面
                    空状态 - 当前时间段内无数据 - 展示提示文案：当前时间段内无数据
                    空状态 - 可观测性异常 - 展示提示文案：可观测性服务数据获取异常
                审计日志查询
                    单筛选条件 - 操作者 - 比对UI、audit.log和Loki查询结果一致
                    单筛选条件 - 操作 - 比对UI、audit.log和Loki查询结果一致
                    单筛选条件 - 资源类型 - 比对UI、audit.log和Loki查询结果一致
                    单筛选条件 - 鉴权结果 - 比对UI、audit.log和Loki查询结果一致
                    多筛选条件 - 操作者+操作+资源类型+鉴权结果 - 比对UI、audit.log和Loki查询结果一致
        错误码校验
            管控/工作负载集群 - 编辑ksc.clusterConfiguration.audit.kubeAPIServier.usePolicy:xxx 配置为不存在的预定义策略，SKS_UNDEFINED_KUBE_APISERVER_AUDIT_POLICY
            管控/工作负载集群 - 编辑ksc.clusterConfiguration.audit.kubeAPIServier.usePolicy:xxx 配置为空，SKS_INVALID_KUBE_APISERVER_AUDIT_POLICY
            管控/工作负载集群 - 编辑ksc.clusterConfiguration.audit.kubeAPIServier配置为无效的自定义策略，SKS_INVALID_KUBE_APISERVER_AUDIT_POLICY
            旧版集群 - 未配置审计策略时打开审计日志，SKS_LOGGING_AUDIT_AGENT_ENABLE_INSUFFICIENT_REQUIREMENTS
        已有功能影响
            报警规则
                新增报警规则 - 集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中审计记录采集组件 {{ $labels.daemonset }} 异常持续 15 分钟。
                集群开启审计组件，才会创建规则到ovm
            编辑k8s集群参数
                编辑k8s集群参数 - 修改controlPlane.clusterConfiguration.apiServer.extraArgs.audit-policy-file - 无法修改，不支持该参数，参数被保护不展示
                编辑k8s集群参数 - 修改controlPlane.clusterConfiguration.apiServer.extraArgs.audit-log-path - 无法修改，不支持该参数，参数被保护不展示
                编辑k8s集群参数 - 修改错误controlPlane.clusterConfiguration.apiServer.extraVolumes{name=audit-policy} 参数 - 修改不生效，保存后更新失败，不做处理
                编辑k8s集群参数 - 修改controlPlane.files{path=/etc/kubernetes/auditpolicy.yaml} - 修改files.content不生效，保存后会被系统默认值覆盖
                编辑k8s集群参数 - 修改controlPlane.files{path=/etc/kubernetes/auditpolicy.yaml} - 修改files.content不生效，保存后不会触发原地更新
                编辑k8s集群参数 - 修改controlPlane.clusterConfiguration.apiServer.extraArgs.audit-log-maxage - 修改生效，集群cp节点组原地更新
        审计日志配置
            审计 - 审计日志配置 - 默认值 - audit-log-maxage: 7
            审计 - 审计日志配置 - 默认值 - audit-log-maxbackup: 5
            审计 - 审计日志配置 - 默认值 - audit-log-maxsize: 100
            审计 - 审计日志配置 - 默认值 - audit-log-truncate-enabled: true
            审计 - 审计日志配置 - 默认值 - audit-log-path: /var/log/apiserver/audit.log
            审计 - 审计日志配置 - 默认值 - audit-policy-file: /etc/kubernetes/audit-policy.yaml
            审计 - 审计日志配置 - 创建集群时，启用审计日志收集，审计日志可正常写入节点的默认目录 /var/log/apiserver/audit.log，并被 OBS 采集
            审计 - 审计日志配置 - 创建集群时，UI 不启用审计日志收集，审计日志可正常写入节点的默认目录 /var/log/apiserver/audit.log，不采集
            审计 - 审计日志配置 - 创建集群时，在 k8s 参数中配置日志文件在节点上保留的最大天数 audit-log-maxage，配置可生效
            审计 - 审计日志配置 - 创建集群时，在 k8s 参数中配置日志文件的轮转备份数量 audit-log-maxbackup，配置可生效
            审计 - 审计日志配置 - 创建集群时，在 k8s 参数中配置日志文件的单个文件最大大小（MB） audit-log-maxsize，配置可生效
            审计 - 审计日志配置 - 编辑集群ksc，在 k8s 参数中指定 webhook 配置的文件路径 audit-webhook-config-file， 配置可生效 - TBD 没使用，能配吗？
            审计 - 审计日志配置 - 编辑已启用审计采集的集群，CP 节点中人为移除 auditpolicy.yaml file，重启节点后，节点内自动补充auditpolicy.yaml空文件，节点内将不生成审计信息
            审计 - 审计日志配置 - 多 CP 节点集群中，审计在每个 CP 节点中保存对应配置
            审计 - 审计日志配置 - 创建 3/5 CP 节点集群，API server pod 所在的节点产生各自的审计日志
            审计 - 审计日志配置 - 审计日志仅在 CP 节点中生成，worker 节点无审计日志
            审计 - 审计日志配置 - 节点替换导致 API server pod 发生节点转移，转移前后的审计日志记录在不同的 CP 节点中，均可被收集
            受保护参数
                审计 - 审计日志配置 - 创建集群时，在 k8s 参数中配置 audit-log-path 并启用审计采集，该参数配置被丢弃，审计日志仍使用默认目录，并被 OBS 采集
                审计 - 审计日志配置 - 创建集群时，在 k8s 参数中修改用于 audit 的 extraVolumes的name audit-policy，该参数的修改被丢弃，审计日志的 policy 文件可正常写入默认目录
                审计 - 审计日志配置 - 创建集群时，在 k8s 参数中修改用于 audit 的 Policy files 的 path，该参数的修改被丢弃，审计日志的 policy 文件可正常写入默认目录
                审计 - 审计日志配置 - 创建集群时，在 k8s 参数中修改 audit-log-path，该参数的修改被丢弃，审计日志可正常写入默认目录，并被 OBS 采集
                审计 - 审计日志配置 - 创建集群时，在 k8s 参数中移除 audit-policy-file，该参数的修改被丢弃，移除不生效 - TBD
        审计策略
            配置策略
                审计 - 审计日志策略 - KSC 中可查看当前集群的内嵌审计策略配置内容
                审计 - 审计日志策略 - 创建集群，默认审计策略配置在 /etc/kubernetes/auditpolicy.yaml, 基础策略的内容正确
                审计 - 审计日志策略 - 创建集群时，开启审计采集，策略默认策略为「基础策略」
                审计 - 审计日志策略 - 创建集群时，不开启审计采集，策略默认使用「基础策略」
                审计 - 审计日志策略 - 创建集群时，设置「精简策略」，创建完成后，检查策略可被正确配置到 API server
                审计 - 审计日志策略 - 创建集群时，设置「基础策略」，创建完成后，检查策略可被正确配置到 API server
                审计 - 审计日志策略 - 创建集群时，设置「详细策略」，创建完成后，检查策略可被正确配置到 API server
                审计 - 审计日志策略 - 创建集群时，设置「自定义策略」，创建完成后，检查策略可被正确配置到 API server
                审计 - 审计日志策略 -  集群创建后，开启审计采集，默认策略使用「基础策略」
                审计 - 审计日志策略 - 集群创建后，开启审计采集，设置「精简策略」，检查策略可被正确配置到 API server
                审计 - 审计日志策略 - 集群创建后，开启审计采集，设置「基础策略」，检查策略可被正确配置到 API server
                审计 - 审计日志策略 - 集群创建后，开启审计采集，设置「详细策略」，检查策略可被正确配置到 API server
                审计 - 审计日志策略 - 集群创建后，开启审计采集，设置「自定义策略」，检查策略可被正确配置到 API server
                审计 - 审计日志策略 - 自定义策略 - rule 字段为空，UI editor 报错「插件配置内容中存在不合法的值。」，无法提交
                审计 - 审计日志策略 - 自定义策略 - level 字段不合法，UI editor 提示「插件配置内容中存在不合法的值。」
                审计 - 审计日志策略 - 自定义策略 - 不填写apiVersion 和 kind，可成功提交，自动填充
            策略切换
                审计 - 审计日志策略 - 编辑已启用审计的集群，从「精简策略」切换到「基础策略」，api server 重启，新策略生效
                审计 - 审计日志策略 - 编辑已启用审计的集群，从「精简策略」切换到「详细策略」，api server 重启，新策略生效
                审计 - 审计日志策略 - 编辑已启用审计的集群，从「精简策略」切换到「自定义策略」，api server 重启，新策略生效
                审计 - 审计日志策略 - 编辑已启用审计的集群，从「基础策略」切换到「精简策略」，api server 重启，新策略生效
                审计 - 审计日志策略 - 编辑已启用审计的集群，从「基础策略」切换到「详细策略」，api server 重启，新策略生效
                审计 - 审计日志策略 - 编辑已启用审计的集群，从「基础策略」切换到「自定义策略」，api server 重启，新策略生效
                审计 - 审计日志策略 - 编辑已启用审计的集群，从「详细策略」切换到「精简策略」，api server 重启，新策略生效
                审计 - 审计日志策略 - 编辑已启用审计的集群，从「详细策略」切换到「基础策略」，api server 重启，新策略生效
                审计 - 审计日志策略 - 编辑已启用审计的集群，从「详细策略」切换到「自定义策略」，api server 重启，新策略生效
                审计 - 审计日志策略 - 编辑已启用审计的集群，从「自定义策略」切换到任意内置策略，api server 重启，新策略生效
        审计日志采集
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，开启审计日志采集，配置「精简策略」，策略生效，审计日志正常采集
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，开启审计日志采集，配置「基础策略」，策略生效，审计日志正常采集
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，开启审计日志采集，配置「详细策略」，策略生效，审计日志正常采集
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，开启审计日志采集，配置「自定义策略」，策略生效，审计日志正常采集
            审计 - 审计日志采集 - 审计日志已经产生轮转后，启用日志采集，所有轮转日志文件中的审计日志都可被 OBS 采集
            审计 - 审计日志采集 - 记录在不同的 CP 节点中的日志都能被采集汇总，并按时间序展示
            审计 - 审计日志采集 - 开启审计日志采集，扩容 CP 节点组，新增的 CP 节点中审计配置正确，审计日志正常采集
            审计 - 审计日志采集 - 开启审计日志采集，替换多个 CP 节点中的一个，替换后的 CP 节点中审计配置正确，审计日志正常采集
            审计 - 审计日志采集 - 关闭审计日志采集后，后端审计日志仍然保持生成，再次开启审计日志收集，可继续进行收集
        资源用量
            审计 - 资源用量 - 对同一个集群配置不同策略，观察 CPU/内存资源使用情况变化
            审计 - 资源用量 - 3+3 集群配置不同策略，执行同样操作，观察审计日志存储增量变化
        后端资源变更
            审计 - ClusterConfiguration - tower 和 管控集群的 default-v1.5.0 clusterconfiguration 中均保存有 SKS 的预定义策略（system，simple，normal，detailed）
            审计 - ClusterConfiguration - tower 和 管控集群的 default-v1.5.0 clusterconfiguration 中 spec.audit.usePolicy = normal，定义工作集群的默认策略
            审计 - 检查 ClusterConfiguration 中的预定义 Policy 内容符合预期
            审计 - KSC - 用户若采用自定义策略，自定义策略内容记入工作集群 ksc 的 spec.clusterConfiguration.audit.kubeAPIServer.customizedPolicy 中
            审计 - KSC - 查看管控集群 ksc，管控集群始终使用 预定义策略 system, spec.clusterConfiguration.audit.kubeAPIServer.usePolicy = system
            审计 - KSC - 修改工作集群 ksc，更改 usePolicy 为 clusterconfiguration 中不存在的预定义值，更改不成功，后端报错
            审计 - KSC - 修改工作集群 ksc，没有 customizedPolicy 定义的情况下，移除 usePolicy，更改不成功，后端报错
            审计 - KSC - 修改工作集群 ksc，配置 customizedPolicy 定义的情况下， 保存后 usePolicy 配置被移除
            审计 - ClusterConfiguration - user-default 中定义同名 policy，再次创建集群，user -default 中配置覆盖系统默认内置配置
            审计 - ClusterConfiguration - user-default 中定义同名 policy，创建集群后，切换其他配置后再切换回修改过的内置配置，仍然使用系统设定值，user-default 中修改值仅对创建生效
            审计 - ClusterConfiguration - user-default 中修改默认 policy 为 simple，创建新集群，不开启审计日志，查看CP 节点默认 policy，为修改后的 simple policy 的内容
        升级
            审计 - 升级 - 从 1.4 升级到 1.5，管控集群升级完成，未关联 OBS，audit 策略已更新为 system
            审计 - 升级 - 从 1.4 升级到 1.5，管控集群升级完成，未关联 OBS，audit 相关配置已更新为新版本的默认值
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，直接关联 OBS 开启审计日志采集，自动触发 ytt 版本升级后完成开启
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，审计功能和策略保持集群原有状态，审计日志正常生成
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，升级到 1.5 并完成功能版本提升后，audit-log-maxage 保持原有配置不变
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，升级到 1.5 并完成功能版本提升后，audit-log-maxsize 保持原有配置不变
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，升级到 1.5 并完成功能版本提升后，audit-log-maxbackup 保持原有配置不变
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，升级到 1.5 并完成功能版本提升后，关联 OBS 开启审计采集，新的审计策略代替旧的策略生效，审计日志可正常采集
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，触发更新功能版本，未开启审计采集，ksc 中 userpolicy不会自动添加为normal，原有策略继续生效
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，开启审计采集，选择【精简策略】替代原有策略生效
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，开启审计采集，选择【基础策略】替代原有策略生效
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，开启审计采集，选择【详细策略】替代原有策略生效
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，开启审计采集，配置【自定义策略】替代原有策略生效
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，开启审计采集，原有的审计日志相关配置中，未保护参数作为customized value 保持之前的设置不变，不会同步为新版本的默认值
            审计 - 升级 - 从 1.5 之前版本升级上来的工作集群，开启审计采集，原有的审计日志相关配置中，受保护参数被覆盖为新版本的默认值
        新部署
            审计 - 新部署 - 部署 SKS 1.5完成，服务未关联 OBS，管控集群的 audit 策略设置为 system
            审计 - 新部署 - 部署 SKS 1.5完成，服务未关联 OBS，管控集群的 audit 相关配置设置为新版本的默认值
    Deprecated（已作废用例，不用看）
        双活 - 模板上传 - 服务部署在 x86 intel 双活集群，已关联 aarch64 双活集群，上传 openEuler aarch64 节点文件，节点模板上传到 aarch64 双活集群，虚拟卷副本数 3
        双活 - 模板上传 - 服务部署在 x86 hygon 双活集群，已关联 aarch64 双活集群，上传 openEuler aarch64 节点文件，节点模板上传到 aarch64 双活集群，虚拟卷副本数 3
        双活 - 模板上传 - 服务部署在 aarch64 双活集群，仅关联 intel x86 双活集群，上传 rocky 节点文件，节点模板上传到 intel x86 双活集群，虚拟卷副本数 3
        双活 - 模板上传 - 服务部署在 aarch64 双活集群，仅关联 intel x86 双活集群，上传 openEuler x86 节点文件，节点模板上传到 intel x86 双活集群，虚拟卷副本数 3
        双活 - 模板上传 - 服务部署在 aarch64 双活集群，仅关联 hygon x86 双活集群，上传 rocky 节点文件，节点模板上传到 hygon x86 双活集群，虚拟卷副本数 3
        双活 - 模板上传 - 服务部署在 aarch64 双活集群，仅关联 hygon x86 双活集群，上传 openEuler x86 节点文件，节点模板上传到 hygon x86 双活集群，虚拟卷副本数 3
        双活 - 模板上传 - 服务部署在 aarch64 双活集群，同时关联 多个x86 双活集群，上传 rocky 节点文件，节点模板上传到第一个可用的 x86 双活集群，虚拟卷副本数 3
        双活 - 模板上传 - 服务部署在 aarch64 双活集群，同时关联 多个x86 双活集群，上传 openEuler 节点文件，节点模板上传到第一个可用的 x86 双活集群，虚拟卷副本数 3
        双活 - 模板上传 - 服务部署在 aarch64 双活集群，先关联 x86 单活集群，再关联 x86 双活集群，上传 x86 节点文件，节点模板上传到 x86 双活集群，虚拟卷副本数 3
        双活 - 模板上传 - 服务部署在 aarch64 双活集群，先关联 x86 单活集群，再关联 x86 双活集群，双活集群失联，上传 x86 节点文件，节点模板上传到 x86 单活集群，虚拟卷副本数 3 - TBD
        双活 - 模板上传 - 服务部署在 aarch64 双活集群，先关联 x86 单活集群，再关联 x86 双活集群，双活集群资源不足，上传 x86 节点文件，节点模板上传到 x86 单活集群，虚拟卷副本数 3 - TBD
        双活 - 模板上传 - 服务部署在 x86 双活集群，先关联 aarch64 单活集群，再关联 aarch64 双活集群，上传 aarch64 节点文件，节点模板上传到 aarch64 双活集群，虚拟卷副本数 3
        双活 - 模板上传 - 服务部署在 x86 双活集群，先关联 aarch64 单活集群，再关联 aarch64 双活集群，双活集群失联，上传 aarch64 节点文件，节点模板上传到 aarch64 单活集群，虚拟卷副本数 3 - TBD
        双活 - 模板上传 - 服务部署在 x86 双活集群，先关联 aarch64 单活集群，再关联 aarch64 双活集群，双活集群资源不足，上传 aarch64 节点文件，节点模板上传到 aarch64 单活集群，虚拟卷副本数 3 - TBD
        双活 - 模板上传 - 服务部署在 x86 intel 双活集群，未关联 aarch64 双活集群，上传 openEuler aarch64 节点文件，节点模板上传到第一个可用的 aarch64 单活集群，虚拟卷副本数 3 - TBD
        双活 - 模板上传 - 服务部署在 x86 hygon 双活集群，未关联 aarch64 双活集群，上传 openEuler aarch64 节点文件，节点模板上传到第一个可用的 aarch64 单活集群，虚拟卷副本数 3 - TBD
        双活 - 模板上传 - 服务部署在 aarch64 双活集群，未关联 x 86 双活集群，上传 rocky 节点文件，节点模板上传到第一个可用的 x86 单活集群，虚拟卷副本数 3 - TBD
        双活 - 模板上传 - 服务部署在 aarch64 双活集群，未关联 x 86 双活集群，上传 openEuler x86 节点文件，节点模板上传到第一个可用的 x86 单活集群，虚拟卷副本数 3 - TBD
        双活 - 模板上传 - 服务部署在 aarch64 双活集群，仅关联版本低于 6.0.0 的 x86 双活集群，上传 rocky 节点文件，节点模板上传到第一个可用的 x86 单活集群，虚拟卷副本数 3 - TBD
        双活 - 模板上传 - 服务部署在 aarch64 双活集群，先关联版本低于 6.0.0 的 x86 双活集群，再关联版本高于 6.0.0 的 x86 双活集群，上传 openEuler 节点文件，节点模板上传到版本高于6.0.0的 x86 双活集群，虚拟卷副本数 3
        双活 - 模板上传 - SKS 部署在 aarch64 单活集群，先后关联x86 双活集群和 x86 单活集群到 tower，上传 x86 节点文件，节点模板上传到 x86 单活集群，虚拟卷副本数 3 - TBD
        双活 - 模板上传 - SKS 部署在 aarch64 单活集群，仅关联x86 双活集群到 tower，无 x86 单活集群，上传 x86 节点文件，节点模板上传到 x86 双活集群，虚拟卷副本数 3
        双活 - 模板上传 - SKS 部署在 x86 单活集群，先后关联aarch64 双活集群和 x86 单活集群到 tower，上传 aarch64 节点文件，节点模板上传到 aarch64 单活集群，虚拟卷副本数 3 - TBD
        双活 - 模板上传 - SKS 部署在 x86 单活集群，仅关联aarch64 双活集群到 tower，无 aarch64 单活集群，上传 aarch64 节点文件，节点模板上传到 aarch64 双活集群，虚拟卷副本数 3
        双活 - 虚拟机工作集群 - HA 设置 - 6.0.0 以下版本非双活集群上创建的所有工作集群 CP 节点虚拟机无 HA 优先级配置，集群可正常创建
新 K8s 版本模板验证
    按节点模板执行验证
        新模板验证 - K8s conformance test
        新模板验证 - x86 版本模板可上传，正确显示版本，并被识别为系统模板
        新模板验证 - 无集群使用时，节点模板可删除，删除后在版本选择列表中不可见
        新模板验证 - 使用新模板创建使用Calico + ELF CSI 的虚拟机集群，开启全部插件，可成功创建
        新模板验证 - 使用新模板创建使用 ZBS CSI 的虚拟机集群，开启全部插件，可成功创建
        新模板验证 - 使用新模板创建使用 EIC CNI 的虚拟机集群，开启全部插件，可成功创建
        新模板验证 - 重启集群节点虚拟机后集群可恢复
        新模板验证 - 使用新模板创建的虚拟机集群可完成原地更新 - 节点组配置可更新
        新模板验证 - 使用新模板创建的虚拟机集群可完成原地更新 - K8s 配置可更新
        新模板验证 - 使用新模板创建的虚拟机集群可完成原地更新 - 受信任容器镜像仓库可更新
        新模板验证 - 使用新模板创建的虚拟机集群，metallb + contour 插件开启后可正常工作
        新模板验证 - 使用新模板可创建物理机集群，并开启全部插件
        新模板验证 - 使用新模板创建的集群，可同步 NTP Server 配置
        新模板验证 - 使用新模板创建的集群，节点信息及 K8s 版本信息正常显示
        新模板验证 - 使用新模板创建的集群，可使用 pod 控制台
        新模板验证 - 使用新模板可升级已有的工作负载集群
        新模板验证 - 使用新模板创建的集群，虚拟机节点操作系统版本及架构信息符合预期
        新模板验证 - 使用新模板创建的集群，虚拟机节点中进程的最大内存映射区数量设置为 262144
    按 K8s 版本执行验证
        新模板验证 - releaseinfo CR 中 compatibleKubeVersion 包含该 K8s 版本
        新模板验证 - 工作集群 CP 节点 /var/lib/kubelet/kubeadm-flags.env 中，无 --container-runtime=remote 配置 （这个配置从1.26开始）
        新模板验证 - 工作集群 worker 节点 /var/lib/kubelet/kubeadm-flags.env 中，无 --container-runtime=remote 配置
        新模板验证 - 使用新模板创建的虚拟机集群，自动伸缩节点组功能正常工作
        新模板验证 - 使用新模板创建的虚拟机集群，故障节点自动替换功能正常工作
        新模板验证 - 使用新模板创建的集群，可使用集群控制台
        新模板验证 - 使用新模板创建的集群，可使用节点控制台
        新模板验证 - 使用新模板创建的集群，可应用租户权限控制
        新模板验证 - 检查集群中的 coredns 实际使用的镜像版本，与 kubeadm config images list --kubernetes-version <k8s-version> 里获取的信息相同
        新模板验证 - 检查 pause 实际使用的镜像版本，与 kubeadm config images list --kubernetes-version <k8s-version> 里获取的信息相同
        新模板验证 - 使用新模板创建的集群，查看 cluster-autoscaler addon 版本，符合 releaseinfo 中的版本映射关系
        新模板验证 - 节点中执行命令 kubeadm version，检查 kubeadm 版本，与当前模板的 k8s 版本定义一致
        新模板验证 - 节点中执行命令 kubectl version，检查 kubectl 版本，与当前模板的 k8s 版本定义一致
        新模板验证 - 节点中执行命令 kubelet --version，检查 kubelet 版本，与当前模板的 k8s 版本定义一致
        新模板验证 - 节点中执行命令 /opt/cni/bin/bridge --version，检查 kubernetes-cni 版本，满足官方版本映射要求
        新模板验证 - 节点中执行命令 containerd --version，检查 containerd 版本，符合模板对应的 SKS 版本的 containerd 版本要求
    按 Base OS 执行验证
        新模板验证 - 模板中 fdisk -l 查看分区，home 分区（kylin上为 backup 分区）和 root 分区大小分别为 20/179G
SKS 1.6
    管理网络业务网络分离
        创建集群
            网络配置
                网络分离 - 创建 - 网络配置 - Info 信息增加「每节点最多可配置 6 张网卡。」img
                网络分离 - 创建 - 网络配置 - 节点默认网卡调整为「节点网卡 1」
                网络分离 - 创建 - 网络配置 - 节点网络选框 label 统一调整为 「虚拟机网络」
                网络分离 - 创建 - 网络配置 - EIC 专用网卡网络选框 label 调整为 「虚拟机网络」
                网络分离 - 创建 - 网络配置 - 默认仅1张管理网卡的情况下显示 Outstanding Tip「当前为单网卡配置，此网卡将同时用于 SKS 服务管理和集群的应用业务流量。如需将管理与业务网络分离，请添加第二张节点网卡。」
                网络分离 - 创建 - 网络配置 - 添加新的节点网卡后， Outstanding Tip 改变为「当前为多网卡配置， SKS 服务管理和集群的应用业务网络分离。」，全部删除后恢复单卡的提示
                网络分离 - 创建 - 网络配置 - EIC 专用网卡网路选框添加说明「需确保该网络的虚拟机路由可与 Kubelet 接口的网卡互通，或选择与 Kueblet 接口一致的虚拟机网络。」
                网络分离 - 创建 - 网络配置 - 点击「添加节点网卡」，新增网卡显示「节点网卡2」，标记「业务网卡」标签，网卡1标记「管理网卡」标签 img
                网络分离 - 创建 - 网络配置 - 点击「添加节点网卡」，新增多张网卡并填写配置，删除网卡2，后续网卡编号，递减1，配置保持不变
                网络分离 - 创建 - 网络配置 - 点击「添加节点网卡」，新增多张网卡，仅业务网卡可删除
                网络分离 - 创建 - 网络配置 - Calico + ELF CSI 虚拟机集群，点击「添加节点网卡」，新增5张网卡后，「添加节点网卡」按钮禁用
                网络分离 - 创建 - 网络配置 - Calico + ZBS CSI 虚拟机集群，点击「添加节点网卡」，新增4张网卡后，「添加节点网卡」按钮禁用
                网络分离 - 创建 - 网络配置 - EIC CNI + ZBS CSI 虚拟机集群，点击「添加节点网卡」，新增3张网卡后，「添加节点网卡」按钮禁用
                网络分离 - 创建 - 网络配置 - 节点网卡选择 DHCP 时，DNS 服务器地址输入框提示更新为 「为启用 DHCP 的节点网卡配置 DNS 服务器，最多配置 3 个。」
                网络分离 - 创建 - 网络配置 - 多个节点网卡，选择同样的 IP 池，选择了同样 IP 池的选框位置均 (Blur + Onchange) inline 报错「与集群内其他网卡关联的 IP 池存在重复 IP 地址。」
                [Deprecated] 网络分离 - 创建 - 网络配置 - 多个节点网卡，选择不同但有 IP 重叠的 IP 池，对应的多个选框位置均 (Blur + Onchange) inline 报错「与集群内其他网卡关联的 IP 池存在重复 IP 地址。」- IP 池创建时不允许不同池 IP段重叠
                网络分离 - 创建 - 网络配置 - 配置多网卡，存在未填写完全的网卡信息，点击「下一步」产生对应位置的 inline 报错提示
            高级配置
                网络分离 - 创建 - 网络高级配置 - 默认展开状态，不可折叠
                网络分离 - 创建 - 网络高级配置 - 配置后翻页再回到网络配置页，高级配置处于展开状态，自定义的配置信息保持
                网络分离 - 创建 - 网络高级配置 - 未配置网卡时，高级配置仅有网卡 title 信息，网络和 IP配置 为空
                网络分离 - 创建 - 网络高级配置 - Calico 集群配置单张节点网卡，高级配置中所有选框自动配置为该网卡，不可编辑，可添加静态路由
                网络分离 - 创建 - 网络高级配置 - EIC 集群配置单张节点网卡，高级配置中默认路由出口和kubelet 接口自动配置为该网卡，不可编辑，可添加静态路由
                网络分离 - 创建 - 网络高级配置 - EIC 集群配置单张节点网卡，CNI 主接口只能设置为「EIC专用网卡」，不可修改
                网络分离 - 创建 - 网络高级配置 - Calico 集群配置多张节点网卡，高级配置中默认路由出口和kubelet 接口默认配置为「节点网卡 2」，可修改，CNI 主接口默认为「跟随 Kubelet 接口」，可修改
                网络分离 - 创建 - 网络高级配置 - EIC 集群配置多张节点网卡，高级配置中默认路由出口和kubelet 接口默认配置为「节点网卡 2」，可修改
                网络分离 - 创建 - 网络高级配置 - EIC 集群配置多张节点网卡，CNI 主接口只能设置为「EIC专用网卡」，不可修改
                网络分离 - 创建 - 网络高级配置 - 删除了的节点网卡不再出现在高级配置的选择列表中
                网络分离 - 创建 - 网络高级配置 - 配置多网卡后删除高级配置中选中的节点网卡，高级配置中除静态路由外均重置为默认值
                网络分离 - 创建 - 网络高级配置 - 显示 Notice tip：若已配置网卡被移除，默认路由出口、Kubelet 接口和 CNI 主接口将重置为默认网卡。- img
                默认路由出口
                    网络分离 - 创建 - 网络高级配置 - 默认路由列表包含所有节点网卡，不包含 ZBS CSI 和 EIC CNI 专用网卡
                    网络分离 - 创建 - 网络高级配置 - 默认路由出口网卡选择列表中换行显示配置的虚拟机网络，使用 IP 池展示 IP 池名，DHCP 不展示 IP 池
                    网络分离 - 创建 - 网络高级配置 - 默认路由出口网卡选择列表中 节点网卡1使用蓝标签显示「管理网卡」，其余为绿标签「业务网卡」
                    网络分离 - 创建 - 网络高级配置 - 默认路由出口网卡使用 DHCP，选框下展示 warning「当前网卡使用 DHCP， 需自行确保其 DHCP 服务器能正确下发网关。」
                    网络分离 - 创建 - 网络高级配置 - 默认路由出口网卡使用 IP 池，所配置 IP 池无 网关配置，「下一步」inline 报错：网卡对应 IP 池缺少网关或 DNS 配置
                    网络分离 - 创建 - 网络高级配置 - 默认路由出口网卡使用 IP 池，所配置 IP 池无 DNS 配置，「下一步」inline 报错：网卡对应 IP 池缺少网关或 DNS 配置
                    网络分离 - 创建 - 网络高级配置 - 默认路由出口网卡使用 IP 池，所配置 IP 池缺少网关和DNS 配置，「下一步」inline 报错：网卡对应 IP 池缺少网关或 DNS 配置，更换 IP 池后提示消失
                    网络分离 - 配置 - 高级配置 - 默认路由出口 - 配置默认路由出口后替换节点，默认路由出口对替换后节点继续生效
                    网络分离 - 配置 - 高级配置 - 默认路由出口 - 配置默认路由出口后扩容新节点，默认路由出口对新节点继续生效
                    网络分离 - 配置 - 高级配置 - 默认路由出口 - 配置默认路由出口后创建新节点组，默认路由出口对新节点组继续生效
                    网络分离 - 配置 - 高级配置 - 默认路由出口 - 配置默认路由出口后升级集群，默认路由出口对滚动后的新节点继续生效
                kubelet 接口
                    网络分离 - 创建 - 网络高级配置 - Kubelet 接口网卡选择列表中，包含所有节点网卡，不包含 ZBS CSI 和 EIC CNI 专用网卡
                    网络分离 - 配置 - 高级配置 - kubelet 接口 - 配置kubelet 接口后替换节点，kubelet 接口对替换后节点继续生效
                    网络分离 - 配置 - 高级配置 - kubelet 接口 - 配置kubelet 接口后扩容新节点，kubelet 接口对新节点继续生效
                    网络分离 - 配置 - 高级配置 - kubelet 接口 - 配置kubelet 接口后创建新节点组，kubelet 接口对新节点组继续生效
                    网络分离 - 配置 - 高级配置 - kubelet 接口 - 配置kubelet 接口后升级集群，kubelet 接口对滚动后的新节点继续生效
                CNI 主接口
                    网络分离 - 创建 - 网络高级配置 - 使用 Calico 的集群 CNI 主接口网卡列表选项，包含「跟随 Kubelet 接口」和所有节点网卡
                    网络分离 - 配置 - 高级配置 - CNI 主接口 - 配置CNI 主接口后替换节点，CNI 主接口对替换后节点继续生效
                    网络分离 - 配置 - 高级配置 - CNI 主接口 - 配置CNI 主接口后扩容新节点，CNI 主接口对新节点继续生效
                    网络分离 - 配置 - 高级配置 - CNI 主接口 - 配置CNI 主接口后创建新节点组，CNI 主接口对新节点组继续生效
                    网络分离 - 配置 - 高级配置 - CNI 主接口 - 配置CNI 主接口后升级集群，CNI 主接口对滚动后的新节点继续生效
                静态路由
                    网络分离 - 创建 - 网络高级配置 - 添加静态路由，不填写目标网段，（Blur+Onchange，submit）inline 报错「请填写目标网段。」
                    网络分离 - 创建 - 网络高级配置 - 添加静态路由，不填写下一跳地址，（Blur+Onchange，submit）inline 报错「请填写下一跳地址。」
                    网络分离 - 创建 - 网络高级配置 - 添加静态路由，目标网段不满足 CIDR 块格式，（Blur+Onchange）inline 报错「CIDR 块格式错误。」
                    网络分离 - 创建 - 网络高级配置 - 添加静态路由，下一跳地址不满足 IP 格式，（Blur+Onchange）inline 报错「IP 地址格式错误。」
                    网络分离 - 创建 - 网络高级配置 - 添加多条冲突的静态路由，后端 webhook 校验不通过，提交透传报错「Duplicate value：map[string]interface {}{"subnet":"%目标网段%"}」
                    网络分离 - 创建 - 网络高级配置 - 不配置静态路由，可正常创建集群
                    网络分离 - 创建 - 网络高级配置 - 添加 1 条静态路由，设置应用到所有节点
                    网络分离 - 创建 - 网络高级配置 - 添加 多条静态路由，设置应用到所有节点
                    网络分离 - 创建 - 网络高级配置 - 配置了静态路由，创建集群后，启动staticroute-operator 插件，静态路由生效
        编辑网络配置
            网络分离 - 配置 - 集群详情页的「设置」层级下新增「网络配置」，选择后显示集群的网络配置页面，默认展示「集群网卡」Tab页
            网络分离 - 配置 - 单节点网卡集群的「节点网卡」页布局检查 img
            网络分离 - 配置 - 多节点网卡集群详情页的「节点网卡」页布局检查 img
            网络分离 - 配置 - 节点网卡 - 支持添加节点网卡
            网络分离 - 配置 - 节点网卡 - 添加节点网卡，IP 配置选择使用 IP 池，但不配置 IP 池，提交报错
            网络分离 - 配置 - ZBS CSI 专用网卡 - 已配置的虚拟机网络/接入虚拟IP/IP 池均不支持编辑，可正确展示
            网络分离 - 配置 - EIC 专用网卡 - EIC 网卡的 网络配置从插件管理中移动至网络配置页，检查UI 布局 img
            网络分离 - 配置 - EIC 专用网卡 - 已配置的虚拟机网络、子网、网关不支持编辑，可正确展示
            网络分离 - 配置 - EIC 专用网卡 - 已配置的 Pod IP pool 可正确展示，可配置
            网络分离 - 网络配置 - 集群网卡- 创建集群时添加了使用 DHCP 的节点网卡，且配置了 DNS 信息，「集群网卡」tab 显示 DNS 配置，但不可编辑
            网络分离 - 网络配置 - 集群网卡- 创建集群时仅添加使用 IP pool 的节点网卡，「集群网卡」tab 无 DNS 配置显示
            网络分离 - 网络配置 - 集群网卡- 创建集群时添加了使用 DHCP 的节点网卡，但未配置 DNS 信息，「集群网卡」tab 无 DNS 配置显示
            网络分离 - 网络配置 - 集群网卡- 仅有使用 IP pool 的节点网卡的集群，在「集群网卡」tab 中新添加一张 DHCP 节点网卡，DNS 配置 UI 禁用
            高级配置
                网络分离 - 配置 - 选择「网络配置」中「高级配置」tab，切换到高级配置页面
                网络分离 - 配置 - 高级配置 - 只读展示默认路由出口，Kubelet 接口，CNI 主接口信息，与实际配置相符 img
                网络分离 - 配置 - 高级配置 - 未配置静态路由的集群，静态路由无条目显示
                网络分离 - 配置 - 高级配置 - 已配置静态路由成功的集群，正确展示所配置静态路由的「目标网段」、「下一跳地址」和「网络接口」信息 img
                网络分离 - 配置 - 高级配置 - 静态路由 - 添加 - 点击「添加规则」保存后可添加静态路由并更新到所有节点
                网络分离 - 配置 - 高级配置 - 静态路由 - 添加 - 新添加的静态路由在节点更新完成前，网络接口显示为「待读取」img
                网络分离 - 配置 - 高级配置 - 静态路由 - 添加 - 新添加的静态路由无法配置成功，网络接口显示为「待读取」
                网络分离 - 配置 - 高级配置 - 静态路由 - 添加 - 未配置静态路由的集群添加静态路由保存成功后，staticroute-operator 插件启动，在sks-system ns 中启动 static-route-operator daemonset
                网络分离 - 配置 - 高级配置 - 静态路由 - 添加 - 为集群已存在的路由的子网添加一条冲突的静态路由，提交后后端 webhook 校验不通过，报子网冲突
                网络分离 - 配置 - 高级配置 - 静态路由 - 添加 - 为集群已存在的路由的子网添加一条冲突的静态路由，提交报错，修改正确后再次提交，保存成功，报错信息消失
                网络分离 - 配置 - 高级配置 - 静态路由 - 编辑 - 修改规则的下一跳地址，保存后可更新所有节点
                网络分离 - 配置 - 高级配置 - 静态路由 - 编辑 - 修改规则的目标网段，保存后可更新所有节点
                网络分离 - 配置 - 高级配置 - 静态路由 - 删除 - 删除其中一条静态路由配置，保存后可更新到所有节点
                网络分离 - 配置 - 高级配置 - 静态路由 - 删除 - 删除所有静态路由配置，保存后可更新到所有节点，静态路由无条目显示
                网络分离 - 配置 - 高级配置 - 静态路由 - 删除 - 删除所有静态路由后，staticroute-operator 插件自动关闭，ds 删除
                网络分离 - 配置 - 高级配置 - 静态路由 - 配置静态路由后替换节点，静态路由对替换后节点继续生效
                网络分离 - 配置 - 高级配置 - 静态路由 - 配置静态路由后扩容新节点，静态路由对新节点继续生效
                网络分离 - 配置 - 高级配置 - 静态路由 - 配置静态路由后创建新节点组，静态路由对新节点组继续生效
                网络分离 - 配置 - 高级配置 - 静态路由 - 配置静态路由后升级集群，静态路由对滚动后的新节点继续生效
        权限
            网络分离 - 配置 - 权限 - 无工作集群编辑权限的用户，无法编辑网络配置
            网络分离 - 配置 - 权限 - 被取消工作集群编辑权限的用户，编辑网络配置提示无权限
        其他功能影响
            网络分离 - 其他功能影响 - EIC 参数配置从插件配置中移除，在 IP 数量下增加跳转提示「可在网络配置中对 EIC 专用网卡修改 IP 配置」，点击可跳转到网络配置页 EIC 网卡位置 img
            网络分离 - 其他功能影响 - 节点列表 - 「业务网卡 IP」列名修改为「节点主 IP」，展示节点默认路由出口所在网卡的 IP，默认显示列
            网络分离 - 其他功能影响 - 节点列表 - Hover「节点主 IP」列名，显示 tooltip「此 IP 是节点在控制平面中的唯一标识。核心运维操作，如节点状态检查、Pod 调度定位及事件溯源，均基于此 IP 进行。」img
            网络分离 - 其他功能影响 - 节点列表 - 「其他 IP」列展示除节点主 IP 之外该节点上网卡的其他 IP 地址的数量（不包括 EIC IP），默认不显示列
            网络分离 - 其他功能影响 - 节点列表 - 节点无其他 IP 时，「其他 IP」列显示「-」
            网络分离 - 其他功能影响 - 节点列表 - 点击「其他 IP」列展示数字的 info icon，可弹出详情显示 img
            网络分离 - 其他功能影响 - 节点详情 - 「业务网卡 IP」修改为「节点主 IP」，展示节点默认路由出口所在网卡的 IP
            网络分离 - 其他功能影响 - 节点详情 - Hover「节点主 IP」，显示 tooltip「此 IP 是节点在控制平面中的唯一标识。核心运维操作，如节点状态检查、Pod 调度定位及事件溯源，均基于此 IP 进行。」
            网络分离 - 其他功能影响 - 节点详情 - 「其他 IP」位置从最末移动到「节点主 IP」 之后，展示其他 IP 地址的数量
            网络分离 - 其他功能影响 - 节点详情 - 点击「其他 IP」数字的 info icon，可弹出详情显示 img
            网络分离 - 其他功能影响 - 节点详情 - 使用管理网卡为kubelet 接口的集群，「其他 IP」详情中没有管理网卡
            网络分离 - 其他功能影响 - 节点详情 - 使用业务网卡为kubelet 接口的双网卡集群，「其他 IP」详情中没有业务网卡
            网络分离 - 其他功能影响 - 节点详情 - 使用其中一张业务网卡为kubelet 接口的3网卡集群，「其他 IP」详情中没有该业务网卡
            网络分离 - 其他功能影响 - 物理机集群 - 未配置 CSI 的物理机集群，查看网络配置页，可只读显示 CP 节点组的网络配置，无 ZBS CSI 网卡
            网络分离 - 其他功能影响 - 物理机集群 - 配置 ZBS CSI 的物理机集群，查看网络配置页，可只读显示 CP 节点组的管理网卡和 ZBS CSI 网卡配置
            网络分离 - 其他功能影响 - 物理机集群 - 物理机集群网络配置页不展示 高级配置 tab（设计变更）
            网络分离 - 其他功能影响 - 物理机集群 - 高级设置显示 CP 节点组的配置，可移除静态路由，保存后应用到所有节点（包括物理机）
            网络分离 - 其他功能影响 - 物理机集群 - 高级设置显示 CP 节点组的配置，除静态路由外无可编辑信息
            网络分离 - 其他功能影响 - 虚拟机集群创建 - 单节点网卡 ELF CSI 虚拟机工作集群可成功创建
            网络分离 - 其他功能影响 - 虚拟机集群创建 - 单节点网卡 ZBS CSI 虚拟机工作集群可成功创建
            网络分离 - 其他功能影响 - 虚拟机集群创建 - 单节点网卡 EIC CNI 虚拟机工作集群可成功创建
            网络分离 - 其他功能影响 - 升级 - 升级 SKS 服务到 1.6，未更新 ytt 版本，ksc 中网络配置保持 1.5 格式不变，部分必要属性自动添加，但不引起集群滚动/原地更新
            网络分离 - 其他功能影响 - 升级 - 升级 SKS 服务到 1.6，未更新 ytt 版本，添加节点网卡，提交后端报错
            网络分离 - 其他功能影响 - 升级 - 升级 SKS 服务到 1.6，未更新 ytt 版本，替换 集群 VIP 所在节点，可成功替换，VIP 漂移到其他 CP 节点的管理网卡
            网络分离 - 其他功能影响 - 升级 - 升级 SKS 服务到 1.6，更新 ytt 版本到 1.6.0，ksc 中网络配置不变，原有网卡 tag 保持default
            网络分离 - 其他功能影响 - 升级 - 升级 SKS 服务到 1.6，更新 ytt 版本到 1.6.0，ksc 中网络配置不变，替换集群 VIP 所在节点，可成功替换，VIP 漂移到其他 CP 节点的管理网卡
            网络分离 - 其他功能影响 - 升级 - 升级 SKS 服务到 1.6，更新 ytt 版本到 1.6.0，添加节点网卡，节点原地更新完成业务网卡添加
            网络分离 - 其他功能影响 - 升级 - 升级 SKS 服务到 1.6，未更新 ytt 版本，自动添加 property.acceptDefaultRouteDNS 配置到原有管理网卡，添加默认CNI 主接口网卡配置到 cni 配置
            网络分离 - 其他功能影响 - 监控 - 默认路由在管理网卡，kubelet 接口、CNI 主接口在业务网卡，查看监控面板，可获取数据
            网络分离 - 其他功能影响 - 监控 - 默认路由、kubelet 接口、CNI 主接口都在业务网卡，查看监控面板，可获取数据
            网络分离 - 其他功能影响 - 监控 - 默认路由在管理网卡，kubelet 接口在业务网卡1， CNI 主接口在业务网卡2，查看监控面板，可获取数据
        实际配置验证
            网络分离 - 默认网关 - 默认路由出口指定管理网卡，默认网关使用管理网卡的网关（使用 route -n 查看）
            网络分离 - 默认网关 - 默认路由出口指定业务网卡，默认网关使用业务网卡的网关
            网络分离 - 默认网关 - 默认路由出口指定的网卡使用 IP 池，默认网关为 IP 池的网关
            网络分离 - 默认网关 - 默认路由出口指定的网卡使用 DHCP，默认网关为 DHCP 的网关配置
            网络分离 - 默认网关 - 创建时配置 0.0.0.0/0 + gw 的静态路由，节点默认网关使用配置的网关地址，保存报「节点静态路由无效」，无法提交
            网络分离 - 默认网关 - 为集群添加 0.0.0.0/0 + gw 的静态路由，配置报错「节点静态路由无效」，无法提交
            网络分离 - 节点 IP - kubelet 接口指定管理网卡，节点 IP 展示为管理网卡 IP
            网络分离 - 节点 IP - kubelet 接口指定管理网卡（IP pool），可创建新节点组，节点 IP 为管理网卡 IP
            网络分离 - 节点 IP - kubelet 接口指定管理网卡（DHCP），替换节点，新节点 IP 为管理网卡 IP
            网络分离 - 节点 IP - kubelet 接口指定管理网卡，查看 kubelet 参数，新增配置 ExecStartPre =/etc/kubernetes/node-ip.sh %管理网卡interface% 和 EnvironmentFile=-/etc/sysconfig/kubelet-option
            网络分离 - 节点 IP - kubelet 接口指定业务网卡，节点 IP 展示为业务网卡 IP
            网络分离 - 节点 IP - kubelet 接口指定业务网卡（DHCP），可创建新节点组，节点 IP 为业务网卡 IP
            网络分离 - 节点 IP - kubelet 接口指定业务网卡（IP pool），替换节点，新节点 IP 为业务网卡 IP
            网络分离 - 节点 IP - 多张业务网卡，kubelet 接口指定业务网卡2，节点 IP 展示为业务网卡2 IP
            网络分离 - 节点 IP - kubelet 接口指定业务网卡，systemctl cat kubelet.service，查看 kubelet 参数，新增配置 ExecStartPre =/etc/kubernetes/node-ip.sh %业务网卡interface% 和 EnvironmentFile=-/etc/sysconfig/kubelet-option
            网络分离 - CNI 主接口 - CNI 主接口指定管理网卡，Calico 使用该网卡进行 pod 间通信，验证跨节点 pod 间网络连通性
            网络分离 - CNI 主接口 - CNI 主接口指定业务网卡，Calico 使用该网卡进行 pod 间通信，验证跨节点 pod 间网络连通性
            网络分离 - CNI 主接口 - Kubelet 接口指定管理网卡，CNI 主接口指定跟随 Kubelet 接口，Calico 使用管理网卡进行 pod 间通信，验证 pod 间网络连通性
            网络分离 - CNI 主接口 - Kubelet 接口指定业务网卡，CNI 主接口指定跟随 Kubelet 接口，Calico 使用业务网卡进行 pod 间通信，验证 pod 间网络连通性
            网络分离 - CNI 主接口 - EIC 集群始终使用 EIC CNI 网卡进行 pod 间通信，确认 pod IP 并验证 pod 间网络连通性
            网络分离 - 集群 VIP - 默认路由出口指定管理网卡，集群 VIP 绑定在管理网卡
            网络分离 - 集群 VIP - 默认路由出口指定业务网卡，集群 VIP 绑定在管理网卡
            网络分离 - 集群 VIP - kubelet 接口指定业务网卡，集群 VIP 绑定在管理网卡
            网络分离 - 节点网卡 - 创建多节点网卡的 EIC CNI + ZBS CSI 集群，查看节点中网卡配置，网卡顺序为：管理网卡、EIC CNI 网卡、ZBS CSI 网卡、业务网卡
            网络分离 - OBS - 使用与 ovm 所在子网（192.168.16.0/20）不通的虚拟机网络（10.254）作为业务网络，使用（10.255）为管理网络和默认路由出口，监控报警可正常工作 - （需确认10.254是否确实跟192.168不通）
            网络分离 - OBS - 使用与 ovm 所在子网（192.168.16.0/20）不通的虚拟机网络（10.254）作为业务网络，使用（192.168）为管理网络和默认路由出口，监控报警可正常工作
            网络分离 - OBS - 使用与 ovm 所在子网 (192.168.16.0/20) 不通的虚拟机网络（10.254）作为业务网络和默认路由出口，监控报警不能正常工作（节点其他网卡没有 192.168.16.0/20子网）
            网络分离 - ntpm - 使用与 tower 配置的 ntp server 所在网络 (192.168.16.0/20) 不通的虚拟机网络（10.254）作为业务网络和默认路由出口，ntpm 插件不能正常工作（节点其他网卡没有 192.168.16.0/20子网）
            网络分离 - ntpm - 使用与 tower 配置的 外网 ntp server 不通的虚拟机网络（10.254）作为业务网络和默认路由出口，ntpm 插件不能正常工作，节点上有其他网卡能通过L3与NTP Server通讯的情况下，添加静态路由后可正常工作
            网络分离 - metallb - 管理网卡（默认路由出口） + 1 业务网卡，开启metallb + contour 插件，使用与管理网卡同子网的地址池，通过 LB IP 可正常访问对应服务
            网络分离 - metallb - 管理网卡 + 1 业务网卡（默认路由出口），开启metallb + contour 插件，使用与业务网卡同子网的地址池，通过 LB IP 可正常访问对应服务 - TBD
        添加节点网卡
            网络分离 - 添加节点网卡 - Rocky OS base 集群添加新的业务网卡，节点 VM 通过原地更新可成功完成网卡热添加
            网络分离 - 添加节点网卡 - oe x86 base 集群添加新的业务网卡，节点 VM 通过原地更新可成功完成网卡热添加
            网络分离 - 添加节点网卡 - oe aarch64 base 集群添加新的业务网卡，节点 VM 通过原地更新可成功完成网卡热添加
            网络分离 - 添加节点网卡 - tl3 x86 base 集群添加新的业务网卡，节点 VM 通过原地更新可成功完成网卡热添加
            网络分离 - 添加节点网卡 - tl3 aarch64 base 集群添加新的业务网卡，节点 VM 通过原地更新可成功完成网卡热添加
            网络分离 - 添加节点网卡 - kylin x86 base 集群添加新的业务网卡，节点 VM 通过原地更新可成功完成网卡热添加
            网络分离 - 添加节点网卡 - kylin aarch64 base 集群添加新的业务网卡，节点 VM 通过原地更新可成功完成网卡热添加
            网络分离 - 添加节点网卡 - 添加使用 IP pool 的业务网卡，节点 VM 通过原地更新完成网卡热添加并成功获取 IP
            网络分离 - 添加节点网卡 - 添加使用 DHCP 的业务网卡，节点 VM 通过原地更新完成网卡热添加并成功获取 IP
            网络分离 - 添加节点网卡 - 添加的节点网卡后检查节点上的网卡配置，新增的网卡追加到已有网卡列表的最后，接口名顺序生成
            网络分离 - 添加节点网卡 - 添加使用 IP 池的节点网卡，查看节点中对应接口状态为 UP，对应网络配置文件生成，分配静态 IP
            网络分离 - 添加节点网卡 - 添加使用 DHCP 的节点网卡，查看节点中对应接口状态为 UP，对应网络配置文件生成，DHCP 获取到 IP
            网络分离 - 添加节点网卡 - 对应 inplaceupdatemachine 资源进入 Updating phase，更新完成转为 Ready
            网络分离 - 添加节点网卡 - rocky template 集群一次添加多张节点网卡后检查节点上的网卡配置，新增的网卡追加到已有网卡列表的最后，接口名顺序生成
            网络分离 - 添加节点网卡 - openeuler x86 template 集群一次添加多张节点网卡后检查节点上的网卡配置，新增的网卡追加到已有网卡列表的最后，接口名顺序生成
            网络分离 - 添加节点网卡 - openeuler aarch64 template 集群一次添加多张节点网卡后检查节点上的网卡配置，新增的网卡追加到已有网卡列表的最后，接口名顺序生成
            网络分离 - 添加节点网卡 - kylin x86 template 集群一次添加多张节点网卡后检查节点上的网卡配置，新增的网卡追加到已有网卡列表的最后，接口名顺序生成
            网络分离 - 添加节点网卡 - kylin aarch64 template 集群一次添加多张节点网卡后检查节点上的网卡配置，新增的网卡追加到已有网卡列表的最后，接口名顺序生成
            网络分离 - 添加节点网卡 - tencentOS x86 template 集群一次添加多张节点网卡后检查节点上的网卡配置，新增的网卡追加到已有网卡列表的最后，接口名顺序生成
            网络分离 - 添加节点网卡 - tencentOS aarch64 template 集群一次添加多张节点网卡后检查节点上的网卡配置，新增的网卡追加到已有网卡列表的最后，接口名顺序生成
        后端资源
            网络分离 - KSC - 创建多节点网卡集群，ksc 中管理网卡 tag 标记为 management，网络和 IP 配置正确
            网络分离 - KSC - 创建多节点网卡集群，ksc 中业务网卡 tag 标记为 default，网络和 IP 配置正确
            网络分离 - KSC - 创建多节点网卡集群，指定管理网卡为默认路由出口，ksc 为管理网卡配置 property.acceptDefaultRouteDNS: true
            网络分离 - KSC - 创建多节点网卡集群，指定一张业务网卡为默认路由出口，ksc 为每个节点组的对应业务网卡配置 property.acceptDefaultRouteDNS: true
            网络分离 - KSC - 添加 1 张业务网卡，ksc 中业务网卡 tag 标记为 default，网络和 IP 配置正确
            网络分离 - KSC - 使用 KSC yaml 文件创建集群，不同worker 节点组的不同网卡配置 property.acceptDefaultRouteDNS: true，webhook 拒绝
            网络分离 - KSC - 使用 KSC yaml 文件创建集群，为指定为默认路由出口的网卡配置无 gateway 和 DNS 的 IP pool，创建失败，webhook 拒绝
            [Deprecated]网络分离 - KSC - 使用 KSC yaml 文件创建集群，第一张为管理网卡，不按顺序配置多张其他网卡，节点中实际网卡接口生成顺序遵循 management > storage > ecp > multus > default
            网络分离 - KSC - 使用 KSC yaml 文件创建集群，不按顺序配置多张网卡，第一张网卡不是管理网卡，提交失败，webhook拒绝
            网络分离 - KSC - 物理机集群的 KSC 中有 property.acceptDefaultRouteDNS 配置但不生效
            网络分离 - KSC - 创建多节点网卡集群，指定管理网卡为kubelet 接口，ksc 为每个节点组的管理网卡配置 property.nodeInternalIP: true
            网络分离 - KSC - 创建多节点网卡集群，指定业务网卡为kubelet 接口，ksc 为每个节点组的业务网卡配置 property.nodeInternalIP: true
            网络分离 - KSC - 创建多业务网卡集群，指定业务网卡2为kubelet 接口，ksc 为每个节点组的业务网卡2配置 property.nodeInternalIP: true
            网络分离 - KSC - 多节点网卡集群中，更改kubelet 接口，将 property.nodeInternalIP: true 配置更换到其他节点网卡，集群节点不发生滚动，节点热更新后 IP 更换为新指定网卡的 IP
            网络分离 - KSC - 多节点网卡集群中，更改kubelet 接口，将部分节点组的 property.nodeInternalIP: true 配置更换到其他节点网卡，节点组节点发生热更新，节点 IP 更换为新指定网卡的 IP，集群可用（calico 主接口指向kubelet 接口，要求新旧网卡的IP  L3 可达）
            网络分离 - KSC - 创建多网卡集群，为默认路由出口和kubelet 接口设置不同的节点网卡，ksc 为对应的网卡分别配置 property.acceptDefaultRouteDNS: true 和 property.nodeInternalIP: true
            网络分离 - KSC - 创建多节点网卡集群，配置 CNI 主接口为 「跟随 Kubelet 接口」，spec.network.cni.config.calicoNetwork.nodeAddresssAutodetectiongV4 配置 kubernetes: NodeInternalIP
            网络分离 - KSC - 创建多节点网卡集群，配置 CNI 主接口为 指定节点网卡，spec.network.cni.config.calicoNetwork.nodeAddresssAutodetectiongV4 配置 interface: %指定网卡名% （如：ens5）
            网络分离 - KSC - 配置静态路由成功，KSC 中 spec.network 中添加 staticRoutes 配置
            网络分离 - KSC - 配置了1条静态路由，删除静态路由，KSC 中 spec.network 中移除 staticRoutes 配置，staticroute-operator 插件关闭
            网络分离 - KSC - 配置了多条静态路由，删除一条静态路由，KSC 中 spec.network 中移除 对应的 staticRoutes 配置，插件仍然开启
            网络分离 - KSC - 配置了多条静态路由，删除全部静态路由后，KSC 中 staticroute-operator 插件关闭
            网络分离 - KSC - 编辑 ksc，对于已存在于路由表中的子网，添加冲突的静态路由，webhook 校验不通过
            网络分离 - KSC - 在 KSC 中 status.staticRoutes 中体现每个节点上静态路由的生效状态，使用 iface 记录路由生效的网络接口
            网络分离 - KSC - 配置了静态路由的集群添加新节点，在 KSC 中 status.staticRoutes 中静态路由中增加新的节点配置
            网络分离 - KSC - 配置了静态路由的集群替换新节点，在 KSC 中 status.staticRoutes 中静态路由节点名更新
            网络分离 - KSC - 配置了静态路由的集群升级，在 KSC 中 status.staticRoutes 中静态路由节点更新
            网络分离 - StaticRoute - 添加一条静态路由，对应创建名为 rount-子网IP-prefix 格式的 staticroute 资源，记录 subnet 和下一跳的 gateway 配置
            网络分离 - StaticRoute - 添加多条静态路由，正确生成对应的 staticroute 资源
            网络分离 - StaticRoute - 添加一条静态路由，使用当前节点网络不可达的网关，staticroute 资源可创建，但配置失败，nodestatus 中报错“given gateway IP is not directly routable, cannot setup the route”
            网络分离 - StaticRoute - 添加一条静态路由，设置默认网关为下一跳, staticroute 资源可创建，可配置成功
            网络分离 - StaticRoute - 添加一条静态路由，目标网段填写不存在的子网，staticroute 资源可创建，但配置失败，nodestatus 中报错“no such device”
            网络分离 - StaticRoute - 删除无法配置成功的静态路由，对应的 staticroute 资源被删除
            网络分离 - StaticRoute - 编辑一条已生效的静态路由，使用当前节点网络非直连网络可达的网关，应用失败，staticroute 资源更新且status有error信息，但节点中已生效的配置保持不变
            网络分离 - StaticRoute - 编辑一条下一跳不可达的静态路由，修改下一跳网关为直连网络可达的网关地址，原 staticroute 资源 name 不变，配置更新，路由配置对已有节点生效，修改后原不可达网络可达
            网络分离 - StaticRoute - 编辑一条未生效的报错静态路由，修改为有效子网地址和网关，原 staticroute 资源重建，配置更新，路由配置对已有节点生效
            网络分离 - StaticRoute - 编辑一条已生效的静态路由，修改子网地址和网关为不存在的配置，原 staticroute 资源重建，配置失败，原有静态路由被删除
            网络分离 - StaticRoute - 后端 KSC 中修改 StaticRoute 的配置，staticroute 资源对应修改，前端可读取新的配置进行展示
            网络分离 - StaticRoute - 后端 staticroute cr 中进行配置修改，reconcile 后被 ksc 的配置覆盖
            网络分离 - 静态路由 - 配置静态路由后，检查 sks-system ns 中启动的 DS static-route-operator 工作负载 resources 配置 requests 5m/20Mi 和 limits 200m/200Mi
            网络分离 - 静态路由 - 插件 - staticroute-operator 插件版本：0.1.0
        特定限制
            网络分离 - 创建 - 网络配置 - 创建物理机集群 UI 中无网络分离相关的 UI，包括设置和提示文案
            网络分离 - 配置 - 节点网卡 - 已添加的节点网卡配置从前端不允许修改，不允许删除
            网络分离 - 配置 - 节点网卡 - 已添加的节点网卡的网络配置可从后端可修改
            网络分离 - 配置 - 节点网卡 - 已添加的节点网卡配置从后端允许删除 ，删除后节点滚动更新
            网络分离 - 配置 - 网络高级配置 - 「默认路由出口」在集群创建完成后不允许修改
            网络分离 - 配置 - 网络高级配置 - 「默认路由出口」在集群创建后不允许后端修改
            网络分离 - 配置 - 网络高级配置 - 「Kubelet 接口」在集群创建完成后不允许从 UI 修改
            网络分离 - 配置 - 网络高级配置 - 「Kubelet 接口」在集群创建完成后可从后端修改
            网络分离 - 配置 - 网络高级配置 - 「CNI 主接口」在集群创建完成后不允许前端修改
            网络分离 - 配置 - 网络高级配置 - 「CNI 主接口」在集群创建完成后可从后端修改
            网络分离 - 创建 - 网络配置 - 为多张节点网卡的 ip pool 配置不同的 DNS，默认路由出口指向的网卡的 DNS 将被设置到所有节点虚拟机
            网络分离 - 创建 - 网络配置 - 为启用 DHCP 的节点网卡配置 DNS，默认路由出口指向 DHCP 的网卡， DNS 配置将被设置到所有节点虚拟机
        配置组合
            同子网
                网络分离 - 创建 - 创建 1 管理网卡 + 1 业务网卡的集群，使用同一个子网，默认路由出口指定管理网卡，kubelet 接口和 CNI 主接口使用默认（业务网卡/随kubelet），可创建成功
                网络分离 - 创建 - 创建 1 管理网卡 + 1 业务网卡的集群，使用同一个子网，默认路由出口指定管理网卡，kubelet 接口和 CNI 主接口指定业务网卡，可创建成功
                网络分离 - 创建 - 创建 1 管理网卡 + 1 业务网卡的集群，使用同一个子网，默认路由出口/Kubelet 接口/CNI 主接口都指定管理网卡，可创建成功
                网络分离 - 创建 - 创建 1 管理网卡 + 1 业务网卡的集群，使用同一个子网，默认路由出口/Kubelet 接口都指定管理网卡，CNI 主接口指定业务网卡，可创建成功
                网络分离 - 创建 - 创建 1 管理网卡 + 2 业务网卡的集群，使用同一个子网，默认路由出口指定管理网卡，可创建成功
                网络分离 - 创建 - 创建 1 管理网卡 + 5 业务网卡的集群，使用同一个子网，默认路由出口指定管理网卡，可创建成功
            不同子网
                网络分离 - 创建 - 创建 1 管理网卡 + 1 业务网卡的集群，使用互通的不同 L3 子网，默认路由出口指定管理网卡，可创建成功
                网络分离 - 创建 - 创建 1 管理网卡 + 1 业务网卡的集群，使用 不互通 的不同 L3 子网，默认路由出口指定管理网卡，可创建成功 - TBD
                网络分离 - 创建 - 创建 1 管理网卡 + 1 业务网卡的集群，使用互通的不同 L3 子网，默认路由出口指定业务网卡，可创建成功
                网络分离 - 创建 - 创建 1 管理网卡 + 2 业务网卡的集群，使用互通的不同 L3 子网，默认路由出口指定业务网卡2，可创建成功
                网络分离 - 创建 - 创建 1 管理网卡 + 2 业务网卡的集群，使用不互通的不同 L3 子网，默认路由出口指定管理网卡，kubelet接口指定业务网卡，CNI主接口指定业务网卡2，可创建成功 - TBD
                网络分离 - 创建 - 创建 1 管理网卡 + 2 业务网卡的集群，业务网卡1 使用互通的不同 L3 子网，默认路由出口指定业务网卡1，可创建成功
                网络分离 - 创建 - 创建 1 管理网卡 + 2 业务网卡的集群，业务网卡2 使用互通的不同 L3 子网，默认路由出口指定业务网卡2，可创建成功
                网络分离 - 创建 - 创建 1 管理网卡 + 1 业务网卡的集群，配置默认路由出口在业务网卡，且子网与 IDC 其他网络不通，添加静态路由，下一跳指向当前节点可达的其他可连通 IDC 网络的子网网关，添加后 IDC 其他网络可访问集群 VIP
            不支持创建的配置
                网络分离 - 不支持配置 - 默认路由出口为业务网卡，管理网卡配置了同一个子网，创建失败
                网络分离 - 不支持配置 - 默认路由出口为业务网卡，另一张业务网卡配置了同一个子网，管理网卡使用不同子网，创建失败
                网络分离 - 创建 - 创建 1 管理网卡 + 1 业务网卡的集群，使用 不互通 的不同 L3 子网，默认路由出口指定业务网卡，创建失败
            IP 池配置
                网络分离 - 创建 - 默认路由出口为管理网卡，业务网卡配置了同一个子网，使用同一个 IP 池，不允许创建，提示「与集群内其他网卡关联的 IP 池存在重复 IP 地址。」
                网络分离 - 创建 - 默认路由出口为管理网卡，业务网卡配置了同一个子网，使用不同 IP 池，创建时监控插件不能完成开启，跨节点pod 不通
                网络分离 - 创建 - 默认路由出口为管理网卡，业务网卡配置了同一个子网，分别使用 DHCP 和 IP 池，可创建成功
        EC
            网络分离 - EC - 添加的虚拟网卡没有获取到 Mac 地址 -SKS_VM_WAITING_FOR_NETWORK_MAC_ADDRESS：节点 { node } 对应的虚拟机未获取到 Mac 地址。 - the VM for K8s node {node} does not get MAC address.
            网络分离 - EC - Tower 未返回添加虚拟网卡结果 - SKS_VM_ADDING_NETWORK_NIC：节点 { node } 对应的虚拟机正在添加虚拟网卡。- the VM for K8s node {node} is adding virtual NIC.
            网络分离 - EC - Tower 返回添加虚拟网卡失败 - SKS_VM_ADDING_NETWORK_NIC_FAILED - 节点 { node } 对应的虚拟机添加虚拟网卡失败。- failed to add the VM virtual NIC for K8s node {node}.
            网络分离 - EC - hostConfigAgent 还没有返回配置虚拟网卡结果 - SKS_VM_SETTING_NETWORK_NIC_CONFIGURATION：节点 { node } 对应的虚拟机正在配置虚拟网卡。- the VM for K8s node {node} is setting virtual NIC configuration.
            网络分离 - EC - hostConfigAgent 返回配置虚拟网卡失败 - SKS_VM_SETTING_NETWORK_NIC_CONFIGURATION_FAILED：节点 { node } 对应的虚拟机配置虚拟网卡失败。- failed to set the VM virtual NIC configuration for K8s node {node}.
            网络分离 - EC - 节点网卡 type 参数与 tag 参数不匹配 - SKS_NODE_NETWORK_TYPE_INVALID：节点网卡的类型参数无效。- Invalid node NIC type. the current NIC type and tag combination is invalid.
            网络分离 - EC - 网卡 property 参数重复或者位置错误 - SKS_NODE_NETWORK_PROPERTY_INVALID：节点网卡的属性无效。- The node NIC property is invalid.
            网络分离 - EC - 网卡 tag 参数重复或者位置错误 - SKS_NODE_NETWORK_TAG_INVALID：节点网卡的标签无效。- The node NIC tag is invalid.
            网络分离 - EC - 引用的 IP 池不存在或者缺少 gateway/dns 参数 - SKS_NODE_NETWORK_IP_POOL_INVALID：节点网卡指定的 IP 池无效。- The IP pool specified by the node's NIC is invalid.
            网络分离 - EC - 静态路由校验错误，如错误的 subnet 或者 gateway 参数 - SKS_STATIC_ROUTE_INVALID：节点静态路由无效。- The node static route is invalid.
    Pod 支持多网卡
        创建集群
            Pod多网卡 - 创建 - 填写不同的 IP 地址范围和CIDR 块，使用 IP 地址范围提交，IP 地址范围生效
            Pod多网卡 - 创建 - 填写不同的 IP 地址范围和CIDR 块，使用 CIDR 块提交，CIDR 块生效
            Pod多网卡 - 创建 - 配置 Pod 专用网卡，不启用「全局配置」，拉起用户负载，Pod 中不使用 Pod 网卡
            Pod多网卡 - 创建 - 配置 Pod 专用网卡，启用「全局配置」，拉起用户负载，查看非系统ns 中的所有 Pod，均配置使用 Pod 网卡
            Pod多网卡 - 创建 - 配置 Pod 专用网卡，启用「全局配置」，在系统 ns 中启动用户负载，查看系统 ns 中的所有 Pod，均未配置 Pod 网卡
            Pod多网卡 - 创建 - 配置 多块 Pod 专用网卡，全部启用「全局配置」，拉起用户负载，查看非系统 ns 中的 Pod，均配置了所有 Pod 网卡
            Pod多网卡 - 创建 - 配置 多块 Pod 专用网卡，部分启用「全局配置」，拉起用户负载，查看非系统 ns 中的 Pod，仅配置了开启全局配置的 Pod 网卡
            Pod多网卡 - 创建 - 配置多块 Pod 专用网卡，使用同样的虚拟机网络和子网 CIDR，不同的 IP 池范围，不开启全局配置，可正常创建集群
            Pod多网卡 - 创建 - 配置多块 Pod 专用网卡，使用同样的虚拟机网络和子网 CIDR，不同的 IP 池范围，其中之一开启全局配置，可正常创建集群
            Pod多网卡 - 创建 - 配置多块 Pod 专用网卡，使用同样的虚拟机网络和子网 CIDR，不同的 IP 池范围，都开启全局配置，可正常创建集群
            Pod多网卡 - 创建 - 配置多块 Pod 专用网卡，使用不同的虚拟机网络和子网 CIDR，可正常创建集群
            UI
                Pod多网卡 - 创建 - 物理机集群无 Pod 多网卡相关 UI
                Pod多网卡 - 创建 - EIC CNI 的虚拟机集群无 Pod 多网卡相关 UI
                Pod多网卡 - 创建 - EUC CNI 的虚拟机集群无 Pod 多网卡相关 UI
                Pod多网卡 - 创建 - CNI 选项为 Calico 时，提示「支持在网络配置（步骤三）添加 Pod 专用网卡。」 img
                Pod多网卡 - 创建 - CNI 选项从 Calico 切换为其他选项，隐藏提示「支持在网络配置（步骤三）添加 Pod 专用网卡。」
                Pod多网卡 - 创建 - Calico 虚拟机集群的网络配置页默认不配置 Pod 网卡，提供「添加 Pod 专用网卡」button img
                Pod多网卡 - 创建 - Calico + ELF CSI 虚拟机集群添加 5 张节点网卡，「添加 Pod 专用网卡」button 禁用
                Pod多网卡 - 创建 - Calico + ZBS CSI 虚拟机集群添加 4 张节点网卡，「添加 Pod 专用网卡」button 禁用
                Pod多网卡 - 创建 - 添加 Pod 专用网卡直到「添加 Pod 专用网卡」button 禁用，所有类型网卡数量总和为 6
                Pod多网卡 - 创建 - 点击「添加 Pod 专用网卡」，新增网卡显示「Pod 专用网卡1」，检查配置表单布局 img
                Pod多网卡 - 创建 - 点击「添加 Pod 专用网卡」，新增多张网卡并填写配置，删除网卡2，后续网卡编号，递减1，配置保持不变
                Pod多网卡 - 创建 - 点击「添加 Pod 专用网卡」，新增的 Pod 专用网卡配置，点击「x」可移除
                Pod多网卡 - 创建 - 点击「添加 Pod 专用网卡」，新增的 Pod 专用网卡配置，向前向后翻页后仍存在
                Pod多网卡 - 创建 - 虚拟机网络 - 为空，提示「请填写虚拟机网络。」（Blur + Onchange，submit）
                Pod多网卡 - 创建 - 子网 CIDR 块 - hover 展示 tooltip 提示「子网 CIDR 块需为所选网络的 L3 子网。」
                Pod多网卡 - 创建 - 子网 CIDR 块 - 为空，提示「请填写 CIDR 块。」（Blur + Onchange，submit）
                Pod多网卡 - 创建 - 子网 CIDR 块 - 格式错误，提示「CIDR 块格式错误。」（Blur + Onchange）
                Pod多网卡 - 创建 - 子网 CIDR 块 - CIDR 主机号输入子网中 IP，提示「子网 CIDR 主机号必须全为 0」（Blur + Onchange）
                Pod多网卡 - 创建 - 子网 CIDR 块 - 输入与 Pod IP CIDR 相同的范围，提交时透传后端报错
                Pod多网卡 - 创建 - 子网 CIDR 块 - 输入与 Service IP CIDR 相同的范围，提交时透传后端报错
                Pod多网卡 - 创建 - 子网 CIDR 块 - 输入节点默认路由指定网卡所选择网络的子网 CIDR，提交时透传后端报错
                Pod多网卡 - 创建 - 子网 CIDR 块 - 输入保留的 CIDR 块（127.0.0.0/8, 169.254.0.0/16, 224.0.0.0/4, 0.0.0.0/0），提交时透传后端报错
                Pod多网卡 - 创建 - 名称 - 为空，提示「请填写名称。」（Blur + Onchange，submit）
                Pod多网卡 - 创建 - 名称 - 支持1-63字符，超出提示「名称支持的字符长度范围为 1-63。」（Blur + Onchange）
                Pod多网卡 - 创建 - 名称 - 仅支持小写字母、数字、连字符（-）,以字母数字开头和结束，不满足提示「仅支持小写字母、数字和连字符（-），并且必须以小写字母或数字开头和结尾。」（Blur + Onchange）
                Pod多网卡 - 创建 - 名称 - 输入存在重名，提示「名称已存在。」（Blur + Onchange）
                Pod多网卡 - 创建 - 手动配置详情 - 点击名称下方「手动配置详情」，显示为 Pod 配置附加网卡的步骤提示 img
                Pod多网卡 - 创建 - 默认使用「地址范围」配置
                Pod多网卡 - 创建 - IP 地址范围 - 为空，提示「请填写 IP 地址范围。」（Blur + Onchange，submit）
                Pod多网卡 - 创建 - IP 地址范围 - 格式错误，提示「IP 地址格式错误。」（Blur + Onchange）
                Pod多网卡 - 创建 - IP 地址范围 - 起始IP大于结束IP，提示「结束 IP 不可小于起始 IP。」（Blur + Onchange）
                Pod多网卡 - 创建 - IP 地址范围 - 起始IP输入子网首地址，提示「不支持使用网络地址（第一个 IP）或广播地址（最后一个 IP）。」（Blur + Onchange）
                Pod多网卡 - 创建 - IP 地址范围 - 结束IP输入子网尾地址，提示「不支持使用网络地址（第一个 IP）或广播地址（最后一个 IP）。」（Blur + Onchange）
                Pod多网卡 - 创建 - IP 地址范围 - 超出子网范围，提示「IP 地址范围中有 IP 地址不在子网范围内。」（Blur + Onchange）
                Pod多网卡 - 创建 - CIDR 块 - 为空，提示「请填写 CIDR 块。」（Blur + Onchange，submit）
                Pod多网卡 - 创建 - CIDR 块 - 格式错误，提示「CIDR 块格式错误。」（Blur + Onchange）
                Pod多网卡 - 创建 - CIDR 块 - 超出子网范围，提示「CIDR 块中有 IP 地址不在子网范围内。」（Blur + Onchange）
                Pod多网卡 - 创建 - 排除 IP - 格式不符合IP或IP范围，提示「排除 IP 格式错误。」（Blur + Onchange）
                Pod多网卡 - 创建 - 排除 IP - 起始IP大于结束IP，提示「结束 IP 不可小于起始 IP。」（Blur + Onchange）
                Pod多网卡 - 创建 - 排除 IP - 多个排除 IP或IP范围存在重复，提示「IP 地址或 IP 地址范围存在重复 IP。」（Blur + Onchange）
                Pod多网卡 - 创建 - 排除 IP - 排除不在已配置的IP地址范围的 IP，提示「排除 IP 不在 IP 地址范围内。」（Blur + Onchange）
                Pod多网卡 - 创建 - 排除 IP - 排除超出已配置的IP地址范围的 IP 范围，提示「排除 IP 不在 IP 地址范围内。」（Blur + Onchange）
                Pod多网卡 - 创建 - 排除 IP - 排除不在已配置的CIDR块范围的 IP，提示「排除 IP 不在 CIDR 块范围内。」（Blur + Onchange）
                Pod多网卡 - 创建 - 排除 IP - 排除 IP 输入多行，行间不使用「，」分隔， 提示「排除 IP 格式错误。」
                Pod多网卡 - 创建 - 默认不启用「全局配置」
                Pod多网卡 - 创建 - 创建时配置了Pod 网卡后切换 CNI 到 EIC，Pod 网卡隐藏，且不参与网卡总数计数
                Pod多网卡 - 创建 - 创建时先添加网卡，再切换到自带网卡的 CNI/CSI 类型，使得网卡数量超出6，点击下一步，报错提示「每节点最多可配置 6 张网卡。」
            地址冲突
                Pod多网卡 - 创建 - 地址冲突 - Pod IP 池中地址与 集群 VIP 冲突，提交报错
                Pod多网卡 - 创建 - 地址冲突 - Pod IP 池中地址与 集群节点网卡 子网冲突，提交报错
                Pod多网卡 - 创建 - 地址冲突 - Pod IP 池中地址与 集群节点网卡 IP 池地址冲突，提交报错
                Pod多网卡 - 创建 - 地址冲突 - Pod IP 池中地址与 MetalLB 插件配置的 IP 范围冲突，提交报错
                Pod多网卡 - 创建 - 地址冲突 - Pod IP 池中地址与其他 Pod 专用网卡配置的 IP 范围重叠，可正常保存 - TBD
                Pod多网卡 - 创建 - 地址冲突 - Pod IP 池中子网与 Service IP CIDR 的 IP 范围重叠，提交报错
                Pod多网卡 - 创建 - 地址冲突 - Pod IP 池中子网与 Pod IP CIDR 的 IP 范围重叠，提交报错
                Pod多网卡 - 创建 - 地址冲突 - Pod IP 池中地址与集群VIP使用的地址池冲突，提交报错
                Pod多网卡 - 编辑 - 地址冲突 - Pod IP 池中地址与 集群节点网卡 IP 地址冲突，提交报错
                Pod多网卡 - 创建 - 地址冲突 - Pod IP 池中地址与其他集群 Pod 专用网卡配置的 IP 范围冲突，无影响，可正常创建
        编辑网络配置
            Pod多网卡 - 编辑 - Calico 虚拟机集群「网络配置」的「节点网卡」tab 中可查看已配置的 Pod 专用网卡 img
            Pod多网卡 - 编辑 - 物理机集群「网络配置」的「节点网卡」tab 中无「添加 Pod 专用网卡」入口
            Pod多网卡 - 编辑 - EIC 集群「网络配置」的「节点网卡」tab 中无「添加 Pod 专用网卡」入口
            Pod多网卡 - 编辑 - EUC CNI 集群「网络配置」的「节点网卡」tab 中无「添加 Pod 专用网卡」入口
            Pod多网卡 - 编辑 - 未配置 Pod 专用网卡的 Calico 虚拟机集群可在此启用 Pod 专用网卡
            Pod多网卡 - 编辑 - 未配置 Pod 专用网卡，不显示提示「修改子网 CIDR 块、IP 地址范围、CIDR 块或排除 IP，仅对新创建的 Pod 有效。」
            Pod多网卡 - 编辑 - 已配置 Pod 专用网卡，显示提示「修改子网 CIDR 块、IP 地址范围、CIDR 块或排除 IP，仅对新创建的 Pod 有效。」
            Pod多网卡 - 编辑 - 已配置 Pod 专用网卡的集群添加 Pod 专用网卡，可成功保存并更新虚拟机网卡
            Pod多网卡 - 编辑 - 已配置的 Pod 专用网卡不可前端删除（移除按钮不再显示）
            Pod多网卡 - 编辑 - 已配置未使用的 Pod 专用网卡可通过后端正常删除，节点对应移除该网卡
            Pod多网卡 - 编辑 - 已配置的 Pod 专用网卡名称和虚拟机网络不可编辑
            Pod多网卡 - 编辑 - 编辑子网 CIDR 块，可成功保存并更新后端资源
            Pod多网卡 - 编辑 - 修改地址范围/CIDR 块，扩大 IP 池，可成功保存并更新后端资源
            Pod多网卡 - 编辑 - 修改地址范围/CIDR 块，缩小 IP 池，释放部分未使用的 IP，可成功保存并更新后端资源
            Pod多网卡 - 编辑 - 修改地址范围/CIDR 块，释放部分已使用的 IP，可成功保存，已被使用的 IP 继续被 pod 使用直到 pod 删除后释放
            Pod多网卡 - 编辑 - 切换 IP 配置方式，并配置相同的 IP 地址范围，可成功保存并更新后端资源
            Pod多网卡 - 编辑 - 切换 IP 配置方式，并扩大 IP 地址范围，可成功保存并更新后端资源
            Pod多网卡 - 编辑 - 切换 IP 配置方式，并缩小 IP 地址范围，可成功保存并更新后端资源
            Pod多网卡 - 编辑 - 排除 IP 中添加尚未被使用的 IP，保存后更新后端资源，继续创建 Pod，会跳过该 IP
            Pod多网卡 - 编辑 - 排除 IP 中添加尚未被使用的 IP 范围，保存后更新后端资源，继续创建 Pod，会跳过该 IP 范围
            Pod多网卡 - 编辑 - 排除 IP 中添加已被使用的 IP，可成功提交，pod 销毁重建将不再被使用
            Pod多网卡 - 编辑 - 排除 IP 中移除 IP，保存后更新后端资源，继续创建 Pod，该 IP 可被使用
            Pod多网卡 - 编辑 - 移除所有排除 IP，保存后更新后端资源，IP 池中所有 IP 可被使用
            Pod多网卡 - 编辑 - 排除 IP - 排除 IP 可多行输入，保存后自动格式化展示
            Pod多网卡 - 编辑 - 开启一张 Pod 网卡的全局配置，之后创建的非系统 ns 中 pod 会配置该网卡，已创建的 pod 不受影响
            Pod多网卡 - 编辑 - 开启多张 Pod 网卡的全局配置，之后创建的非系统 ns 中 pod 会配置多张网卡，已创建的 pod 不受影响
            Pod多网卡 - 编辑 - 关闭 Pod 网卡的全局配置，之后创建的非系统 ns 中 pod 不自动配置该网卡，已创建的 pod 不受影响
            Pod多网卡 - 编辑 - 「排除名字空间」配置中不包含系统名字空间
            Pod多网卡 - 编辑 - 「排除名字空间」配置中包含当前所有非系统名字空间，包括 default
            Pod多网卡 - 编辑 - 集群中新建一个非系统 ns后，「排除名字空间」列表中立即增加该 ns
            Pod多网卡 - 编辑 - 集群中删除一个非系统 ns后，「排除名字空间」中立即移除该 ns
            Pod多网卡 - 编辑 - 1 张 Pod 专用网卡，设置「排除名字空间」配置，被排除的非系统 ns 中 pod 不配置该网卡
            Pod多网卡 - 编辑 - 多张 Pod 专用网卡，设置「排除名字空间」配置，被排除的非系统 ns 中 pod 不配置任何 Pod 网卡
            Pod多网卡 - 编辑 - 设置「排除名字空间」配置后，被排除 ns 中新创建的 pod 不再配置 Pod 网卡
            Pod多网卡 - 编辑 - 设置「排除名字空间」配置之前，被排除 ns 中已创建的 pod 已配置 Pod 网卡不受影响
            Pod多网卡 - 编辑 - 设置「排除名字空间」后，关闭所有 Pod 网卡的全局配置，保存 - 排除名字空间不写入配置，再次展示时为空
            Pod多网卡 - 编辑 - 设置「排除名字空间」后，新创建名字空间然后创建 pod，pod 配置专用网卡
            Pod多网卡 - 编辑 - 设置「排除名字空间」后，删除 ns， 再添加同名 ns 并创建 pod，排除配置依然对同名 ns 生效，pod 不配置专用网卡
            Pod多网卡 - 排除系统名字空间 - 全局配置 Pod 专用网卡，向系统名字空间中创建 pod，pod 不会配置 pod 专用网卡
            Pod多网卡 - 排除名字空间 - 被排除的名字空间中的 pod 仍然可通过手动配置配置对应的 pod 专用网卡
            Pod多网卡 - 编辑 - Rocky OS base 集群添加新的 Pod 专用网卡，节点 VM 通过原地更新完成网卡热添加
            Pod多网卡 - 编辑 - oe x86 集群添加新的 Pod 专用网卡，节点 VM 通过原地更新完成网卡热添加
            Pod多网卡 - 编辑 - oe aarch64 集群添加新的 Pod 专用网卡，节点 VM 通过原地更新完成网卡热添加
            Pod多网卡 - 编辑 - tl3 x86 集群添加新的 Pod 专用网卡，节点 VM 通过原地更新完成网卡热添加
            Pod多网卡 - 编辑 - tl3 aarch64 集群添加新的 Pod 专用网卡，节点 VM 通过原地更新完成网卡热添加
            Pod多网卡 - 编辑 - kylin x86 集群添加新的 Pod 专用网卡，节点 VM 通过原地更新完成网卡热添加
            Pod多网卡 - 编辑 - kylin aarch64 集群添加新的 Pod 专用网卡，节点 VM 通过原地更新完成网卡热添加
            Pod多网卡 - 编辑 - 同时添加节点网卡和 Pod 专用网卡，可成功保存并更新后端资源
            Pod多网卡 - 编辑 - 同时修改多个 Pod 专用网卡配置，可成功保存并更新后端资源
            Pod多网卡 - 添加 Pod 专用网卡完成后，查看节点中对应接口状态为 UP，pod 专用网卡对应配置文件生成，不配置 IP
            Pod多网卡 - 添加 Pod 专用网卡，对应 inplaceupdatemachine 资源进入 Updating phase，更新完成转为 Ready
            Pod多网卡 - 编辑 - 集群 Ready 状态下，可以添加 Pod 专用网卡
            Pod多网卡 - 编辑 - 集群 Running 状态下，可以添加 Pod 专用网卡
            Pod多网卡 - 编辑 - 集群可访问但处于 Failed 状态（节点异常），仍可以添加 Pod 专用网卡，但不能顺利完成，节点恢复后可完成
            Pod多网卡 - 编辑 - 集群可访问但处于 Failed 状态（插件异常），仍可以添加 Pod 专用网卡，可完成
            Pod多网卡 - 编辑 - 添加多块 Pod 专用网卡，使用和已有 pod 网卡相同的虚拟机网络和子网 CIDR，配置不同 IP 池范围，开启全局配置，扩容已有用户负载，新增 pod 均配置新网卡
            Pod多网卡 - 编辑 - 添加多块 Pod 专用网卡，使用和已有 pod 网卡相同的虚拟机网络和子网 CIDR，配置不同 IP 池范围，开启全局配置，重启已有用户负载，用户负载重启后的 pod 均配置新网卡
            UI
                Pod多网卡 - 添加 - 名称 - 为空，提示「请填写名称。」（Blur + Onchange，submit）
                Pod多网卡 - 添加 - 名称 - 支持1-63字符，超出提示「名称支持的字符长度范围为 1-63。」（Blur + Onchange）
                Pod多网卡 - 添加 - 名称 - 仅支持小写字母、数字、连字符（-）,以字母数字开头和结束，不满足提示「仅支持小写字母、数字和连字符（-），并且必须以小写字母或数字开头和结尾。」（Blur + Onchange）
                Pod多网卡 - 添加 - 名称 - 输入存在重名，提示「名称已存在。」（Blur + Onchange）
                Pod多网卡 - 添加 - 默认不启用「全局配置」
                Pod多网卡 - 编辑 - 子网 CIDR 块 - hover 展示 tooltip 提示「子网 CIDR 块需为所选网络的 L3 子网。」
                Pod多网卡 - 编辑 - 子网 CIDR 块 - 为空，提示「请填写 CIDR 块。」（Blur + Onchange，submit）
                Pod多网卡 - 编辑 - 子网 CIDR 块 - 格式错误，提示「CIDR 块格式错误。」（Blur + Onchange）
                Pod多网卡 - 编辑 - 子网 CIDR 块 - CIDR 主机号输入子网中 IP，提示「子网 CIDR 的主机号必须全为 0」（Blur + Onchange）
                Pod多网卡 - 编辑 - 子网 CIDR 块 - 输入与 Pod IP CIDR 相同的范围，提交时透传后端报错？？？ - TBD
                Pod多网卡 - 编辑 - 子网 CIDR 块 - 输入与 Service IP CIDR 相同的范围，提交时透传后端报错？？？ - TBD
                Pod多网卡 - 编辑 - 子网 CIDR 块 - 输入节点默认路由指定网卡所选择网络的子网 CIDR（无论DHCP或pool），提交时透传后端报错
                Pod多网卡 - 编辑 - 子网 CIDR 块 - 输入保留的 CIDR 块（127.0.0.0/8, 169.254.0.0/16, 224.0.0.0/4, 0.0.0.0/0），提交时透传后端报错？？？ - TBD
                Pod多网卡 - 编辑 - 手动配置详情 - 点击名称下方「手动配置详情」，显示为 Pod 配置附加网卡的步骤提示 img
                Pod多网卡 - 编辑 - IP 地址范围 - 为空，提示「请填写 IP 地址范围。」（Blur + Onchange，submit）
                Pod多网卡 - 编辑 - IP 地址范围 - 格式错误，提示「IP 地址格式错误。」（Blur + Onchange）
                Pod多网卡 - 编辑 - IP 地址范围 - 起始IP大于结束IP，提示「结束 IP 不可小于起始 IP。」（Blur + Onchange）
                Pod多网卡 - 编辑 - IP 地址范围 - 起始IP输入子网首地址，提示「不支持使用网络地址（第一个 IP）或广播地址（最后一个 IP）。」（Blur + Onchange）
                Pod多网卡 - 编辑 - IP 地址范围 - 结束IP输入子网尾地址，提示「不支持使用网络地址（第一个 IP）或广播地址（最后一个 IP）。」（Blur + Onchange）
                Pod多网卡 - 编辑 - IP 地址范围 - 超出子网范围，提示「IP 地址范围中有 IP 地址不在子网范围内。」（Blur + Onchange）
                Pod多网卡 - 编辑 - CIDR 块 - 为空，提示「请填写 CIDR 块。」（Blur + Onchange，submit）
                Pod多网卡 - 编辑 - CIDR 块 - 格式错误，提示「CIDR 块格式错误。」（Blur + Onchange）
                Pod多网卡 - 编辑 - CIDR 块 - 超出子网范围，提示「CIDR 块中有 IP 地址不在子网范围内。」（Blur + Onchange）
                Pod多网卡 - 编辑 - 排除 IP - 格式不符合IP或IP范围，提示「排除 IP 格式错误。」（Blur + Onchange）
                Pod多网卡 - 编辑 - 排除 IP - 起始IP大于结束IP，提示「结束 IP 不可小于起始 IP。」（Blur + Onchange）
                Pod多网卡 - 编辑 - 排除 IP - 多个排除 IP或IP范围存在重复，提示「IP 地址或 IP 地址范围存在重复 IP。」（Blur + Onchange）
                Pod多网卡 - 编辑 - 排除 IP - 排除不在已配置的IP地址范围的 IP，提示「排除 IP 不在 IP 地址范围内。」（Blur + Onchange）
                Pod多网卡 - 编辑 - 排除 IP - 排除超出已配置的IP地址范围的 IP 范围，提示「排除 IP 不在 IP 地址范围内。」（Blur + Onchange）- TBD
                Pod多网卡 - 编辑 - 排除 IP - 排除不在已配置的CIDR块范围的 IP，提示「排除 IP 不在 CIDR 块范围内。」（Blur + Onchange）
                Pod多网卡 - 编辑 - 排除 IP - 排除 IP 输入多行，行间不使用「，」分隔， 提示「排除 IP 格式错误。」
                Pod多网卡 - 编辑 - 所有 Pod 专用网卡均未启用全局配置， 不显示「排除名字空间」配置
                Pod多网卡 - 编辑 - 对任意一张 Pod 专用网卡启用全局配置， 显示「排除名字空间」配置
        权限
            Pod多网卡 - 配置 - 权限 - 无工作集群编辑权限的用户，无法编辑 Pod 专用网卡
            Pod多网卡 - 配置 - 权限 - 被取消工作集群编辑权限的用户，编辑 Pod 专用网卡提示无权限
        插件 & 其他
            Pod多网卡 - 插件 - 配置了 Pod 专用网卡的集群，启动 multus-cni 插件，版本 4.2.2
            Pod多网卡 - 插件 - 对比使用情况检查 multus-cni 插件相关工作负载的 resources 配置 requests/limits 在合理的范围
            Pod多网卡 - 插件参数 - multus-cni 插件的参数可通过 ksc.spec.systemComponents 修改相关组件的 resources 分配及 loglevel 配置，前端不开放配置
            Pod多网卡 - 插件参数 - 后端修改 multus-cni 插件的资源配置，并检查修改生效
        后端资源
            Pod多网卡 - 添加 Pod 网卡，multus-cni 启用后，cni 配置文件目录 /etc/cni/net.d 中添加 00-multus.conf
            Pod多网卡 - 检查 00-multus.conf 中的 defaultNetworks，配置了开启了全局配置的所有pod 网卡名
            Pod多网卡 - KSC - 配置 Pod 专用网卡后，KSC 中 cp 和 worker 的 network devices 中均添加网卡配置 networkType: NONE,tag: multus, vlan: %vlanID%
            Pod多网卡 - KSC - 配置 Pod 专用网卡，KSC spec.network.multiNetwork.nad 中添加对应网卡配置（interface/name/subnet/type：macvlan/ pod 网卡 ip 池配置）
            Pod多网卡 - KSC - 配置 Pod 专用网卡，开启全局配置, KSC 中记录配置 spec.network.multiNetwork.nad.defaultNetwork: true
            Pod多网卡 - KSC - 配置 Pod 专用网卡，未开启全局配置, KSC 中不配置 spec.network.multiNetwork.nad.defaultNetwork
            Pod多网卡 - KSC - 配置 Pod 专用网卡，开启后关闭全局配置, KSC 中配置变更为  spec.network.multiNetwork.nad.defaultNetwork: false，ksc 里面不再能看到该配置
            Pod多网卡 - KSC - 对 Pod 专用网卡 设置排除 IP/IP段，KSC spec.network.multiNetwork.nad.excludeSubnet 列表中正确记录所有排除的 IP/IP 段
            Pod多网卡 - KSC - 对 Pod 专用网卡 设置排除 namespace，KSC spec.network.multiNetwork.excludeNamespaces.user 列表中正确记录所有排除的非系统 namespace
            Pod多网卡 - 检查 00-multus.conf 配置 systemNamespaces 中记录所有排除的 namespace
            Pod多网卡 - 每添加一张 Pod 网卡，集群生成对应 NetworkAttachmentDefinition CR，查看 CR 配置与用户设置相符
            Pod多网卡 - 检查配置 IP 地址范围的 NetworkAttachmentDefinition CR 的 ipam 设置
            Pod多网卡 - 检查配置 CIDR 块的 NetworkAttachmentDefinition CR 的 ipam 设置
            Pod多网卡 - 检查配置排除 IP 后的 NetworkAttachmentDefinition CR 的 ipam 设置
            Pod多网卡 - 检查 NetworkAttachmentDefinition CR 中默认设置 - {"cniVersion":"0.3.1","plugins":[{"type":"macvlan","mode":"bridge","ipam":{"type":"whereabouts"}}]}
            Pod多网卡 - Rocky OS 中 NetworkAttachmentDefinition CR 中 spec.config.plugins.master 与实际网卡相符
            Pod多网卡 - Openeuler OS 中 NetworkAttachmentDefinition CR 中 spec.config.plugins.master 与实际网卡相符
            Pod多网卡 - TencentOS 中 NetworkAttachmentDefinition CR 中 spec.config.plugins.master 与实际网卡相符
            Pod多网卡 - Kylin OS 中 NetworkAttachmentDefinition CR 中 spec.config.plugins.master 与实际网卡相符
            Pod多网卡 - multus-cni 插件开启新建 ns sks-system-multus-cni，部署 DaemonSet kube-multus-ds 和 whereabouts, Deployment whereabouts-controller
            Pod多网卡 - 检查新增的 DS 工作负载 kube-multus-ds 的 resources 配置 requests 10m/100Mi 和 limits 1/800Mi
            Pod多网卡 - 检查新增的 DS 工作负载 whereabouts 的 resources 配置 requests 10m/20Mi 和 limits 100m/200Mi
            Pod多网卡 - 检查新增的 Deployment 工作负载 whereabouts-controller 的 resources 配置 requests 1m/10Mi 和 limits 200m/200Mi
            Pod多网卡 - 后端移除所有 Pod 网卡后，multus-cni 插件自动关闭，对应 ns 和 工作负载被删除
            Pod多网卡 - route -n 检查使用 pod 专用网卡的 pod 中的路由，仅有默认路由和附加网卡的直连路由
            Pod多网卡 - multus 负载 - 1+1 集群上并发创建 100 个 pod，multus 相关负载的状态正常，无重启，资源使用大部分在requests 范围，不超出 limits范围
            Pod多网卡 - multus 负载 - 1+1 集群上带有 100 个以上使用 pod 网卡的工作负载 pod，重启集群节点，multus 和工作负载pod 可正常启动
        Pod 挂载网卡
            Pod多网卡 - 手动配置 - 为工作负载的 pod template 添加 annotation 配置 pod 网卡，创建工作负载，检查 pod 中网络配置
            Pod多网卡 - 手动配置 - 编辑 pod，添加 annotation 配置 1 张 pod 网卡，检查 pod 中网络配置
            Pod多网卡 - 手动配置 - 创建 pod，annotation 中配置多张 pod 网卡，检查 pod 中网络配置
            Pod多网卡 - 手动配置 - 编辑 pod，添加 annotation 配置不存在的 Pod 网卡，pod 创建不成功，产生对应事件 k8s.cni.cncf.io "xxx" not found
            Pod多网卡 - 自动配置 - 对单张 pod 专用网卡开启全局配置，新创建 pod，检查 pod 中网络配置，添加了 pod 网卡
            Pod多网卡 - 自动配置 - 对多张 pod 专用网卡开启全局配置，新创建 pod，检查 pod 中网络配置，添加了多张 pod 网卡
            Pod多网卡 - 自动配置 - 对单张 pod 专用网卡开启全局配置，重建已存在的 pod，检查 pod 中网络配置，添加了 pod 网卡
            Pod多网卡 - 全局配置优先 - 对1张 pod 专用网卡开启全局配置，为工作负载指定其他 pod 网卡，全局配置的网络先于手动配置添加
            Pod多网卡 - Event - 新创建挂载附加网卡的 pod，触发事件：Addedinterface from：multus msg：Add %interface% [%IP/PREFIX%] fromsks-system-multus-cni/%网卡名%
            Pod多网卡 - Event - 集群添加 Pod 多网卡但未使用，multus-cni 被启动，创建任意 pod，触发 multus 事件：Addedinterface from：multus msg：Add %interface% [%IP/PREFIX%] from k8s-pod-network
            Pod多网卡 - annotation - 挂载 pod 专用网卡的 pod，annotation 中将自动添加 k8s.v1.cni.cncf.io/network-status 字段，值为当前 pod 的网络配置情况和 IP 分配情况
            Pod多网卡 - 为 pod 同时配置K8s 网络和 1个 Pod 网络，检查 pod 中网络配置和 annotation 中的 k8s.v1.cni.cncf.io/network-status
            Pod多网卡 - 为 pod 同时配置K8s 网络和 多个 Pod 网络，检查 pod 中网络配置和 annotation 中的 k8s.v1.cni.cncf.io/network-status
            Pod多网卡 - 为 pod 仅配置 Pod 网络，检查 pod 中网络配置和 annotation 中的 k8s.v1.cni.cncf.io/network-status
            检查网络连通性
                Pod多网卡 - 检查网络连通 - 为工作负载的 pod template 添加 annotation 配置 pod 网卡，检查多副本 pod 间网络连通性
                Pod多网卡 - 检查网络连通 - 为不同工作负载的 pod 配置同一张 pod 网卡，检查 pod 间网络连通性
                Pod多网卡 - 检查网络连通 - 为工作负载配置多张 pod 网卡，检查工作负载 pod 间网络连通性
                Pod多网卡 - 检查网络连通 - 为工作负载配置多张 pod 网卡，检查同一个 pod 中不同网络间 ip 互通
                Pod多网卡 - 检查网络连通 - 配置了 pod 专用网卡的 pod 和未配置 pod 专用网卡的 pod间，不连通？？？ - TBD
                Pod多网卡 - 检查网络连通 - 使用 pod 专用网卡的 pod 可通过 service 域名访问其他配置了同样专用网卡的 pod
                Pod多网卡 - 检查网络连通 - 使用 pod 专用网卡的 pod 可通过 pod IP 访问其他配置同样专用网卡的 pod
                Pod多网卡 - 检查网络连通 - 未配置 pod 专用网卡的 pod 可通过 service 域名访问配置了 pod 专用网卡的 pod
                Pod多网卡 - 检查网络连通 - 未配置 pod 专用网卡的 pod 可通过 pod IP 访问配置了 pod 专用网卡的 pod — TBD
                Pod多网卡 - 检查网络连通 - 使用 pod 专用网卡的 pod 可访问集群外部网络 pod - TBD 这个对于节点网络的要求是什么
                Pod多网卡 - 检查网络连通 - 通过集群外部网络可访问 pod 专用网卡的 pod IP ？？？- TBD
        运维场景配置一致性
            Pod多网卡 - 添加多张 Pod 网卡后，（后端）删除前序网卡，VM 更新后，nad 配置中 master 接口名和 实际网卡接口名不会自动更新，需要手动调整
            Pod多网卡 - 添加多张 Pod 网卡后，（后端）删除前序网卡，替换集群节点，检查 nad 配置中 master 接口名和 实际网卡接口名一致？？？ - TBD 多张 pod 网卡删前置位会影响它自己后置位的接口名？
            Pod多网卡 - 添加了单个 Pod 网卡的集群，手动扩容节点组，新增加的节点正确应用 Pod 网卡配置
            Pod多网卡 - 添加了多个 Pod 网卡的集群，手动扩容节点组，新增加的节点正确应用 Pod 网卡配置
            Pod多网卡 - 添加了 Pod 网卡的集群，升级集群 K8s 版本触发滚动更新，滚动后的节点正确应用 Pod 网卡配置
            Pod多网卡 - 添加了 Pod 网卡的集群，手动替换节点，替换后的节点正确继承同样的 Pod 网卡配置
            Pod多网卡 - 添加了 Pod 网卡的集群，触发故障自动替换节点，替换后的节点正确继承同样的 Pod 网卡配置
        节点虚拟机中的网卡顺序
            Pod多网卡 - 创建 - 创建时同时配置了业务网卡和 Pod 网卡，查看节点中网卡配置，Pod 网卡在业务网卡之后
            Pod多网卡 - 创建 - 创建时同时配置了业务网卡，ZBS CSI 网卡和 Pod 网卡，查看节点中网卡配置，网卡接口生成顺序应为：管理网卡 -> 业务网卡 -> ZBS CSI 网卡 -> Pod 网卡
            Pod多网卡 - 创建 - 创建时同时配置了业务网卡、EIC CNI 网卡和 ZBS CSI 网卡，查看节点中网卡配置，网卡接口生成顺序应为：管理网卡 -> 业务网卡 -> EIC CNI 网卡 -> ZBS CSI 网卡
            Pod多网卡 - 创建 - 查看节点中网卡配置，管理网卡始终处于最前
            Pod多网卡 - 编辑 - 创建时配置了 Pod 网卡，创建完成后添加了业务网卡，查看节点中网卡配置，Pod 网卡在业务网卡之前
            Pod多网卡 - 编辑 - 创建时配置了业务网卡，创建完成后添加了 Pod 网卡，查看节点中网卡配置，Pod 网卡在业务网卡之后
            Pod多网卡 - 编辑 - 创建时配置了业务网卡，创建完成后同时添加添加了1张 业务网卡和1张 Pod 网卡，查看节点中网卡配置，Pod 网卡在新业务网卡之后
            Pod多网卡 - 编辑 - 创建时仅配置管理网卡，创建完成后一次性添加3张节点网卡和2张pod网卡，查看节点中网卡接口名顺序，pod网卡在后
            Pod多网卡 - 编辑 - 创建时仅配置管理网卡，创建完成后一次性添加3张节点网卡和2张pod网卡，添加完成后新创建节点，新节点中网卡接口名顺序和旧节点相符
            Pod多网卡 - 编辑 - 创建时仅配置管理网卡，创建完成后一次性添加3张节点网卡和2张pod网卡，添加完成后滚动更新集群节点，更新后节点中网卡接口名顺序和原有节点相符
            Pod多网卡 - 编辑 - 创建时仅配置管理网卡，创建完成交错添加pod 网卡和节点网卡，实际网卡顺序和interface name 顺序按照添加顺序排列
            Pod多网卡 - 编辑 - 创建时仅配置管理网卡，创建完成交错添加pod 网卡和节点网卡，新建节点，新节点中网卡接口名顺序和旧节点一致
            Pod多网卡 - 编辑 - 创建时仅配置管理网卡，创建完成交错添加pod 网卡和节点网卡，滚动更新集群，新节点中网卡接口名顺序和旧节点一致
            Pod多网卡 - 编辑 - 创建时配置管理网卡和 pod 网卡，创建完成添加节点网卡，滚动更新集群，新节点中网卡接口名顺序和旧节点一致
        IP 池使用
            Pod多网卡 - 获取 IP - 全局配置开启，在非系统 ns 中创建用户负载，pod 依次使用 Pod 网卡 IP 池中的 IP
            Pod多网卡 - 获取 IP - 全局配置关闭，在非系统 ns 中创建用户负载，为部分负载手动配置 pod 网卡，仅带有annotation 的 pod 配置对应的网络和取得 IP 池中的 IP
            Pod多网卡 - 获取 IP - 创建用户负载，使得 pod 数量超出 Pod 网卡 IP 池中的可用 IP 数量，超出部分的 pod 无法就绪
            Pod多网卡 - 获取 IP - 创建用户负载，使得 pod 数量超出 Pod 网卡 IP 池中的可用 IP 数量，扩容 IP 池，超出部分的 pod 可就绪
            Pod多网卡 - 获取 IP - 创建用户负载，使得 pod 数量恰好用尽 Pod 网卡 IP 池中的可用 IP，pod 可就绪
            Pod多网卡 - 获取 IP - 配置 排除 IP，在非系统 ns 中创建配置了 Pod 网卡的用户负载，最多可创建 （IP 池中数量 - 排除 IP 数量）的 pod，超出的 pod 无法就绪
            Pod多网卡 - 获取 IP - 配置 排除 IP 范围，创建用户负载，使得使用 Pod 网卡的 pod 数量超出可用 IP 数，去掉部分排除 IP 配置，释放出的 IP 数量对应的 pod 可就绪
            Pod多网卡 - 获取 IP - 配置的 IP 池 CIDR 与子网的 CIDR 相同，使用 IP 时自动排除网络地址或广播地址 - TBD
            Pod多网卡 - 获取 IP - 配置的 CIDR 块中包括了 subnet 中的子网的网络地址或广播地址，自动排除
            Pod多网卡 - 获取 IP - 配置 IP 范围的可分配 IP 范围中包括起始 IP 和结束 IP
        报警 & EC
            Pod多网卡 - 报警 - 对管控集群开启监控报警，才可产生 Pod 附加网络的可分配 IP 情况的报警
            Pod多网卡 - 报警 - 对工作负载集群开启监控报警，才可产生 pod 多网卡插件异常报警
            Pod多网卡 - 报警规则 - 新增集群Pod多网卡插件异常报警规则 - Critical - KubeSmartClusterPluginPodMultiCNIStatusAbnormal
            Pod多网卡 - 报警 - 对虚拟机集群触发集群Pod多网卡插件异常报警，检查报警信息，修复问题报警可解决
            Pod多网卡 - 报警规则 - 新增集群Pod 专用网卡 IP 池可分配 IP 不足报警规则 - Notice - SKSPodNetworkAttachmentDefinitionOutOfAvailableIP
            Pod多网卡 - 报警 - 对虚拟机集群触发集群Pod 专用网卡 IP 池可分配 IP 不足报警，检查报警信息，修复问题报警可解决
            Pod多网卡 - 报警 - 调整集群Pod 专用网卡 IP 池可分配 IP 不足报警阈值，触发报警，检查报警信息
            Pod多网卡 - EC - NAD 相关字段校验错误，如无效的 subnet 或者 IP，范围错误等 - SKS_NETWORK_ATTACHMENT_DEFINITIONS_INVALID：Pod 网络附加定义配置无效。- Pod network attachment definition configuration is invalid.
        其他功能影响
            Pod多网卡 - 其他功能影响 - 升级 - 升级 SKS 服务到 1.6，需要更新已有集群功能版本为 1.6.0，才能支持 Pod 多网卡
            Pod多网卡 - 其他功能影响 - pod 列表 - 配置了多网卡的 pod 在 pod 资源列表中「IP 地址」列显示以逗号分隔的多个IP 地址
            Pod多网卡 - 其他功能影响 - pod 详情 - 配置了多网卡的 pod 在 pod 详情页中「IP 地址」中平铺显示以逗号分隔的多个IP 地址
            Pod多网卡 - 系统命名空间保护 - 配置了 Pod 专用网卡的工作集群，开启 SKS 插件，新增加的系统 namespace 下的 pod 不配置 Pod 网卡
            Pod多网卡 - 升级环境 - 前序版本创建的 Calico 虚拟机集群ytt升级1.6后，可配置 Pod 专用网卡，重启用户应用 Pod 完成网卡切换
            Pod多网卡 - 升级环境 - 前序版本创建的 Calico 虚拟机集群未提升ytt版本，无法配置 Pod 专用网卡
    SKS1.6 多租户增强
        内置角色权限变更
            权限变更 - 应用开发者，原工作负载资源管理能力不变
            权限变更 - 应用开发者，新增权限项 - 其他项目内所有ns的资源管理权限
            权限变更 - 应用开发者，不拥有对Namespace本身管理权限 - 创建、编辑、删除
            权限变更 - 应用开发者，新增权限项 - 拥有管理名字空间配额的权限
            权限变更 - 应用运维管理员，原权限 - 项目内所有资源权限
            权限变更 - 应用运维管理员，新增权限 - 项目内Namespace的管理权限 - 创建、编辑、删除
            权限变更 - 集群范围权限 - PV - 租户可查看与其关联的pvc下pv的详情，无法创建和删除
            权限变更 - 集群范围权限 - SC - 租户可查看与其关联的pvc所选sc的详情，无法创建和删除
            权限变更 - 集群范围权限 - SC - 租户创建PVC时可选择SC
            权限变更 - 集群范围权限 - IngressClass - 租户可查看IngressClass详情，创建Ingress可UI选择
            权限变更 - 集群范围权限 - ApiServices - 租户可查看ApiServices详情，某些高级应用可检查API Services状态
            权限变更 - 集群范围权限 - IPPools - 租户可查看Calico的IP 池详情
            权限变更 - 其他资源 - IPPools - 有sks-system-ecp权限的查看所有资源与配置权限的租户可查看Everoute的IP 池详情
        UI 项权限变更
            UI - 应用开发者详情，权限展示 - 管理资源与配置
            UI - 应用运维管理员详情，权限展示 - 管理资源与配置、管理名字空间
            UI - 应用运维管理员列表，权限范围更新「5项操作权限+1项查看权限」
            UI - 创建自定义角色，新增 - 管理名字空间
            UI - 创建自定义角色 - 管理名字空间，hover时查看tooltip描述
            UI - 创建自定义角色 - 管理名字空间配额移动至管理资源与配置下
            UI - 创建自定义角色 - 管理资源与配置，hover时查看tooltip描述
            UI - 创建自定义角色 - 管理所有资源与配置，hover时查看tooltip描述
            UI - 创建名字空间 -增加关联项目选项，下拉展示项目列表
            UI - 创建名字空间 - 创建时选择不关联项目，创建成功
            UI - 创建名字空间 - 创建时选择关联项目，创建成功，项目详情增加新创建ns
            UI - 创建名字空间 - 租户创建时，项目展示为所属项目列表
            UI - 创建名字空间 - 租户创建时，若不选择关联项目 - 报错，必须选择项目
            UI - 创建名字空间 - 租户创建时，选择关联项目，可创建成功，并成功关联项目
            UI - 租户可删除名字空间，删除成功，删除相关资源
            UI - 租户创建持久卷申领 - 可选择存储类
            UI - 租户创建持久卷申领 - 选择存储类，可创建pvc成功
        升级影响
            应用开发者租户 - 升级前-仅对工作负载有管理权限，对名字空间配额、其他负载资源，无权限
            应用开发者租户 - 升级后 - 刷新页面，可编辑已有名字空间配额
            应用开发者租户 - 升级后 - 可通过控制台管理其他工作负载资源
            应用开发者租户 - 升级后 - 原赋予的权限管理效果不变
            应用运维管理员租户 - 升级前-对所有工作负载有管理权限，对名字空间无管理权限
            应用运维管理员租户 - 升级后 - 刷新页面，可创建名字空间
            应用运维管理员租户 - 升级后 - 刷新页面，可删除已有名字空间
            应用运维管理员租户 - 升级后 - 可通过控制台对项目内Namespace使用其他管理权限
            应用运维管理员租户 - 升级后 - 原赋予的权限管理效果不变
            任意角色租户 - 升级前，使用控制台操作PV- 无任何权限
            任意角色租户 - 升级后，使用控制台查看PV（get，list，watch）- 可查看租户内PVC相关的PV
            任意角色租户 - 升级后，使用控制台创建PV，权限禁止
            任意角色租户 - 升级后，使用控制台删除PV，权限禁止
            任意角色租户 - 升级前，使用控制台操作SC- 无任何权限
            任意角色租户 - 升级后，使用控制台查看SC（get，list，watch）- 有权限
            任意角色租户 - 升级后，使用控制台创建SC，权限禁止
            任意角色租户 - 升级后，使用控制台删除SC，权限禁止
            任意角色租户 - 升级前，使用控制台操作IngressClass- 无任何权限
            任意角色租户 - 升级后，使用控制台查看IngressClass（get，list，watch）- 有权限
            任意角色租户 - 升级后，使用控制台对IngressClass进行其他操作，权限禁止
            任意角色租户 - 升级前，使用控制台操作apiservices- 无任何权限
            任意角色租户 - 升级后，使用控制台查看apiservices（get，list，watch）- 有权限
            任意角色租户 - 升级后，使用控制台对apiservices进行其他操作，权限禁止
            任意角色租户 - 升级前，使用控制台操作ippools- 无任何权限
            任意角色租户 - 升级后，使用控制台查看ippools（get，list，watch）- 有权限
            任意角色租户 - 升级后，使用控制台对ippools进行其他操作，权限禁止
            自定义角色租户 - 升级后，所定义的角色项目内权限不变
            自定义角色租户 - 升级后，编辑角色修改权限范围，可修改成功，权限生效
            自定义角色租户 - 升级前后权限单独验证 - 管理名字空间配额
            自定义角色租户 - 升级前后权限单独验证 - 管理工作负载
            自定义角色租户 - 升级前后权限单独验证 - 管理服务与网络
            自定义角色租户 - 升级前后权限单独验证 - 管理配置
            自定义角色租户 - 升级前后权限单独验证 - 管理持久卷申领
            自定义角色租户 - 升级前后权限单独验证 - 查看所有资源与配置
            创建纯数字名称的工作集群-可创建成功，权限相关资源可正常创建
        工作负载
            工作负载资源
                仅管理工作负载权限使用者-登陆UI，创建Deployment表单，可选择项目内名字空间
                有管理工作负载和名字空间权限的使用者-登陆UI，创建Deployment表单，可创建名字空间，名字空间必须选择关联项目
                仅管理工作负载权限使用者-登陆UI，创建Deployment表单，镜像拉取秘钥为输入框，仅支持输入Secret，不支持选择
                有管理工作负载和管理配置使用者-登陆UI，创建Deployment表单，可创建Secret用于拉取镜像
                有管理工作负载和管理配置使用者-登陆UI，创建Deployment表单，可选择同ns已有Secret用于拉取镜像
                仅管理工作负载权限使用者-登陆UI，创建Deployment表单，容器配置时选择容器镜像，应只能输入公网镜像，无法获取到用户容器镜像
                容器镜像仓库和工作负载集群使用者租户-创建Deployment表单，容器配置时选择容器镜像，可展示已有用户容器镜像列表
                容器镜像仓库和工作负载集群使用者租户，有管理配置权限-创建Deployment表单，容器配置时首次选择用户容器镜像，创建时自动创建镜像拉取秘钥
                容器镜像仓库和工作负载集群使用者租户，无管理配置权限-创建Deployment表单，容器配置时首次选择用户容器镜像，创建时跳过Secret创建
                租户场景-登陆UI，创建Deployment表单，节点调度策略，不支持指定选择节点，为输入框
                租户场景-登陆UI，创建Deployment表单，pod调度策略，规则组中拓扑域不支持选择节点标签，为输入框
                仅管理工作负载权限使用者-登陆UI，创建Deployment表单，在环境变量配置中，ConfigMap选择时无权限，展示为暂无数据，创建按钮隐藏
                仅管理工作负载权限使用者-登陆UI，创建Deployment表单，在环境变量配置中，Secret选择时无权限，展示为暂无数据，创建按钮隐藏
                有管理工作负载和配置权限使用者-登陆UI，创建Deployment表单，在环境变量配置中，ConfigMap选择时展示已有资源
                有管理工作负载和配置权限使用者-登陆UI，创建Deployment表单，在环境变量配置中，Secret选择时展示已有资源
                仅管理工作负载权限使用者-登陆UI，创建Deployment表单，在数据存储配置中，PVC列表为空，创建pvc按钮隐藏
                仅管理工作负载权限使用者-登陆UI，创建Deployment表单，访问方式由于无网络权限，隐藏整个step3
                有管理工作负载和服务与网络权限的使用者-登陆UI，创建Deployment表单，访问方式中，可获取相关Serivce和Ingress，展示列表信息
                有管理工作负载和服务与网络权限的使用者-登陆UI，创建Deployment表单，访问方式中，可创建关联Service和Ingress
                仅有管理工作负载权限使用者-登陆UI，创建Deployment表单，可创建成功，pod状态正常
                仅有管理工作负载权限使用者-登陆UI，查看工作负载列表，可正常展示，仅展示所属项目的名字空间下的工作负载
                仅有管理工作负载权限使用者-登陆UI，查看工作负载列表，可正常切换单一的工作负载列表
                仅有管理工作负载权限使用者-登陆UI，查看工作负载列表，跟据名称搜索工作负载，能正确匹配及展示
                仅有管理工作负载权限使用者-登陆UI，进入工作负载详情，详情信息可正常展示，无管理服务访问权限，访问方式Tab隐藏
                仅有管理工作负载权限使用者-登陆UI，进入工作负载查看详情，详情信息可正常展示，无管理配置权限，容器详情内ConfigMap和SecretTab隐藏
                仅有管理工作负载权限使用者-登陆UI，进入工作负载查看详情，详情信息可正常展示，无管理配置和持久卷申领权限，容器详情内数据存储Tab相关表隐藏
                任意使用者-登陆UI，进入工作负载详情，详情信息可正常展示，无法查看事件，tab隐藏
                任意使用者-登陆UI，进入工作负载详情，详情信息可正常展示，监控Tab隐藏，无obs权限
                任意使用者-登陆UI，pod详情，详情信息可正常展示，无obs和事件权限，监控和事件icon隐藏
                任意使用者-登陆UI，可查看IngressClass列表及详情，但操作按钮隐藏，无法创建、编辑及删除
                有管理服务与网络权限的使用者-登陆UI，创建Ingress选择IngressClass时，能列出对应列表信息
                任意使用者-登陆UI，可查看持久卷列表及详情，但操作按钮隐藏，无法创建、编辑及删除
                任意使用者-登陆UI，可查看存储类列表及详情，但操作按钮隐藏，无法创建、编辑及删除
                有管理持久卷申领的使用者-登陆UI，创建持久卷申领选择存储类时，能列出对应存储类信息
                有管理持久卷申领的使用者-登陆UI，创建持久卷申领后，可在持久卷申领详情查看到新创建的持久卷
            其他资源
                自定义资源 - tower管理员用户，查看作用域为Cluster范围的CRD及其CR，可展示全部
                自定义资源 - tower管理员用户，查看作用域为Namespaced范围的CRD及其CR，可展示全部
                自定义资源 - tower管理员用户，通过yaml导入创建Cluster范围CRD成功
                自定义资源 - tower管理员用户，通过yaml导入创建Namespace范围CRD成功
                自定义资源 - tower管理员用户，通过yaml导入创建Cluster范围CR成功
                自定义资源 - tower管理员用户，通过yaml导入创建Namespace范围CR成功
                自定义资源 - tower管理员用户，编辑Cluster范围CRD成功
                自定义资源 - tower管理员用户，编辑Namespace范围CRD成功
                自定义资源 - tower管理员用户，删除Cluster范围CRD成功，同时删除相关CR
                自定义资源 - tower管理员用户，删除Namespace范围CRD成功，同时删除相关CR
                自定义资源 - tower管理员用户，进入详情，编辑Cluster范围CR成功
                自定义资源 - tower管理员用户，进入详情，编辑Namespaced范围CR成功
                自定义资源 - tower管理员用户，进入详情，删除Cluster范围CR成功
                自定义资源 - tower管理员用户，进入详情，删除Namespaced范围CR成功
                自定义资源 - 有「查看资源与配置」权限的租户，可查看其项目内namespace范围的CRD及详情的CR
                自定义资源 - 有「管理资源与配置」权限的租户，可查看其项目内namespace范围的CRD及详情的CR
                自定义资源 - 有「管理所有资源与配置」权限的租户，可查看其项目内namespace范围的CRD及详情的CR
                自定义资源 - 有「管理资源与配置」权限的租户，CRD列表不展示morebutton「编辑YAML」和「删除」按钮
                自定义资源 - 有「管理资源与配置」权限的租户，CRD详情「编辑YAML」和 morebutton「删除」按钮不展示
                自定义资源 - 有「管理资源与配置」权限的租户，CRD详情「自定义资源」tab列表，展示morebutton「编辑YAML」和「删除」按钮
                自定义资源 - 有「管理资源与配置」权限的租户，CRD详情「自定义资源」tab列表，morebutton「编辑YAML」，可查看相关资源yaml配置
                自定义资源 - 有「管理资源与配置」权限的租户，CRD详情「自定义资源」tab列表，morebutton「编辑YAML」，修改yaml配置，可保存成功
                自定义资源 - 有「管理资源与配置」权限的租户，CRD详情「自定义资源」tab列表，morebutton「删除」，删除自定义资源成功
                自定义资源 - 有「管理资源与配置」权限的租户，通过导入YAML创建Cluster范围的CRD，创建失败
                自定义资源 - 有「管理资源与配置」权限的租户，通过导入YAML创建Namespace范围的CRD，创建失败
                自定义资源 - 有「管理资源与配置」权限的租户，通过导入YAML创建项目内namespace范围的CRD下的CR，创建成功，可在CRD详情查看到新增
                集群资源 - tower管理员用户，对集群资源有管理权限
                集群资源-工作集群使用者用户，仅对集群资源有查看权限
                集群资源-工作集群使用者用户，可查看「持久卷」列表，无操作权限
                集群资源-工作集群使用者用户，可查看「存储类」列表，无操作权限
                集群资源-工作集群使用者用户，可查看「IngressClass」列表，无操作权限
                集群资源-工作集群使用者用户，可通过集群控制台查看calico cni集群ippools资源
                集群资源-工作集群使用者用户，可通过集群控制台查看apiservice资源
                名字空间 - 租户有「管理名字空间」的权限，可创建名字空间，创建时必须选择加入项目
                名字空间 - 租户有「管理名字空间」的权限，可通过kubeconfig对名字空间增加标签，如将名字空间修改为其他项目标签
                名字空间 - 租户有「管理名字空间」的权限，可删除名字空间，删除后将从项目移除，清理名字空间下所有资源
                名字空间 - 租户有「管理名字空间」的权限，不能通过集群控制台list ns-即执行kubectl get ns获取全部ns
                名字空间 - 租户有「管理名字空间」的权限，能通过集群控制台get项目内的ns-如kubectl get ns capi
                名字空间 - 租户有「管理名字空间」的权限，创建名字空间时选择加入项目，应不允许选择System项目
                名字空间 - 移除租户的「管理名字空间」的权限，UI创建名字空间失败
                名字空间 - 移除租户的「管理名字空间」的权限，UI删除名字空间失败
                名字空间 - 移除租户的「管理名字空间」的权限，使用控制台编辑名字空间失败
                名字空间 - 租户有「管理名字空间」的权限，创建名字空间并指定项目，产生NamespaceCreated事件
                名字空间 - 管理员用户，创建名字空间并指定项目，产生NamespaceCreated事件
                项目管理 - 工作集群使用者，可查看项目管理-项目，所属项目列表，与SKS1.5一致
                项目管理 - 容器镜像仓库和工作集群使用者，可查看项目管理-项目，所属项目列表，与SKS1.5一致
    UI表单部署管理应用
        工作负载展示及交互
            工作负载 - 位置 - 侧导航栏名字空间下，原导航取消二级菜单
            工作负载 - 页面描述 - 统一展示Kubernetes工作负载资源
            工作负载 - 统一展示资源类型：Deployment、DaemonSet、CronJob、Job、StatefulSet、Pod
            工作负载 - 全部资源类型 -可展示资源类型 Pod 仅展示独立Pod资源，其余由工作负载创建的展示在工作负载详情
            工作负载 - 创建按钮 - 点击下拉项，分别展示创建各类负载资源按钮
            工作负载 - 创建按钮 - 切换单一资源，创建按钮不变，点击下拉项，分别展示创建各类负载资源按钮
            工作负载 - 列表展示项及交互
            工作负载-名字空间过滤器 -默认为「全部名字空间」，点击可选择过滤项目及其他无归属名字空间，交互与1.5一致
            工作负载-搜索，根据列表资源名称搜索
            工作负载-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
            工作负载-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
            工作负载-搜索-切换单个资源-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
            工作负载-切换资源，默认为「工作负载」，展示全部资源列表
            工作负载 -切换资源，点击下拉菜单，可切换其他单独资源，Deployment、DaemonSet、CronJob、Job、StatefulSet、Pod
            工作负载 -切换资源，点击切换「Deployment」，展示deployment资源列表，列表字段同1.5
            工作负载 -切换资源，点击切换「StatefulSet」，展示StatefulSet资源列表，列表字段同1.5
            工作负载 -切换资源，点击切换「DaemonSet」，展示DaemonSet资源列表，列表字段同1.5
            工作负载 -切换资源，点击切换「CronJob」，展示CronJob资源列表，列表字段同1.5
            工作负载 -切换资源，点击切换「Job」，展示Job资源列表，列表字段同1.5
            工作负载 -切换资源，点击切换「Pob」，展示Pob资源列表，列表字段同1.5,展示全部pod
            工作负载-全类型列表，过滤名字空间+搜索名称，展示所有可匹配的资源，匹配正确
            工作负载-过滤名字空间+切换单个工作负载+搜索名称，展示所有可匹配的资源，匹配正确
            工作负载-全部工作负载列表，点击创建Deployment等资源，创建成功后查看列表新增及更新
            工作负载-切换Deployment列表，点击创建Deployment，创建成功后查看列表新增及更新
            工作负载-切换Deployment列表，点击创建其他工作负载，创建成功后当前列表不会新增，切换所创建资源可查看新增列表
            工作负载-资源跳转-从全部资源，点击任意类型资源进入详情，详情展示正确
            工作负载-资源跳转-从全部资源，点击任意类型资源进入详情，root展示返回「工作负载」
            工作负载-资源跳转-选择单个资源类型，点击列表名称进入资源详情，root展示返回「%单个资源类型%」
            工作负载列表-点击morebutton，编辑YAML-展示原始yaml信息，可直接编辑及保存成功，同1.5
            工作负载列表-点击morebutton，编辑%工作负载%-展示编辑表单信息，与配置一致，修改后可保存成功，有toast提醒
            工作负载列表-点击morebutton，下载YAML-下载原始yaml信息，与yaml配置一致
            工作负载列表-点击morebutton，编辑预期副本数-可打开弹窗，可正常编辑并提交成功并生效，有toast提醒
            工作负载列表-点击morebutton，点击重新部署-可并提交成功并生效，有toast提醒
            工作负载列表-点击morebutton，点击暂停调度-可并提交成功并生效，有toast提醒，列表及详情增加「暂停调度」状态
            工作负载列表-点击morebutton，cronjob资源点击暂停-可并提交成功并生效，有toast提醒，列表及详情更新为「已挂起」状态
            工作负载列表-点击morebutton，cronjob资源点击恢复-可并提交成功并生效，有toast提醒，列表及详情更新为「运行中」状态
        应用部署与管理
            工作负载
                Deployment
                    创建Deployment
                        基本信息
                            工作负载配置
                                创建Deployment - 弹窗区域展示，文案提示
                                创建Deployment - 基本信息：工作负载配置 - 名称，为空校验：请填写名称
                                创建Deployment - 基本信息：工作负载配置 - 名称，字符数限制：名称支持的字符长度范围为1-253
                                创建Deployment - 基本信息：工作负载配置 - 名称，特殊字符开头及结尾限制：仅支持小写字母、数字、连字符和点，并且必须以小写字母或数字开头和结尾
                                创建Deployment - 基本信息：工作负载配置 - 名称，同一名字空间不允许重名：名称已存在
                                创建Deployment - 基本信息：工作负载配置 - 名字空间，为空校验：请选择名字空间
                                创建Deployment - 基本信息：工作负载配置 - 名字空间，选择器展示，支持搜索
                                创建Deployment - 基本信息：工作负载配置 - 名字空间，选择器展示，租户视角，仅展示所属项目下的ns
                                创建Deployment - 基本信息：工作负载配置 - 名字空间，选择器内创建名字空间按钮，租户无该权限时不展示创建
                                创建Deployment - 基本信息：工作负载配置 - 名字空间，创建名字空间，弹窗校验
                                创建Deployment - 基本信息：工作负载配置 - 名字空间，创建名字空间，管理员用户关联项目，可选择不关联
                                创建Deployment - 基本信息：工作负载配置 - 名字空间，创建名字空间时选择不关联项目，创建后可展示在列表中
                                创建Deployment - 基本信息：工作负载配置 - 名字空间，创建名字空间时选择项目，应不包含System项目
                                创建Deployment - 基本信息：工作负载配置 - 名字空间，创建名字空间，租户关联项目，必须选择，且列表仅展示所属项目
                                创建Deployment - 基本信息：工作负载配置 - 名字空间，创建名字空间后自动回填入配置项，自动选中
                                创建Deployment - 基本信息：工作负载配置 - 副本数，默认值为1
                                创建Deployment - 基本信息：工作负载配置 - 副本数，状态交互
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，默认展示收起状态
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，点击展开后默认项展示
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略，默认配置项-滚动更新，maxSurge 25%，maxUnavailable 25%
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略，滚动更新 文案校验
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略 -maxSurge，输入框仅允许属于阿拉伯数字
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略 -maxSurge，为空校验-请填写maxSurge。
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略 -maxUnavailable，输入框仅允许属于阿拉伯数字
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略 -maxUnavailable，为空校验-请填写maxUnavailable。
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略 -maxSurge，单位切换，默认%，可切换为个
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略 -maxUnavailable，单位切换，默认%，可切换为个
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略 -maxSurge，单位切换，切换为个，值根据副本数向上取整
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略 -maxUnavailable，单位切换，切换为个，值根据副本数向下取整
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略 -maxSurge/maxUnavaiable，单位为个时，修改副本数，其值根据规则联动自动计算
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略 -maxSurge/maxUnavaiable，修改默认值
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略 -maxSurge/maxUnavaiable，为0可保存成功并生效
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略，切换为替换更新，切换后文案更新
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，升级策略，切换为替换更新，切换后maxSurge/maxUnavaiable参数隐藏
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，标签 - 默认仅展示「添加标签」按钮
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，标签 - 点击添加标签展示输入框Textarea
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，标签 - 键，为空校验
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，标签 - 键，格式校验
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，标签 - 值，格式校验
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，标签 - 值，可选择不输入
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，标签 - 移除标签
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，标签 - 添加多个标签
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，标签 - 查看格式要求，popover展示格式要求
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，注解 - 默认仅展示「添加注解」按钮
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，注解 - 点击添加注解展示输入框Textarea
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，注解 - 键，为空校验
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，注解 - 键，格式校验
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，注解 - 值，格式不限制
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，注解 - 值，可选择不输入
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，注解 - 移除注解
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，注解 - 添加多个注解
                                创建Deployment - 基本信息：工作负载配置 - 高级设置，注解 - 查看格式要求，popover展示格式要求
                            Pod配置
                                镜像拉取秘钥
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，文案提示
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，下拉列表，支持搜索
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，可同时选择多个Secret
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，管理员用户，点击下拉列表，可点击创建Secret
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，有Secret权限的租户，点击下拉列表，可点击创建Secret，创建时自动填充相同的ns
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，无创建Secret权限的租户，Secret参数为输入框
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，有权限的租户，仅展示所属ns下的Secret
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，创建Secret后，自动回显至输入框中
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，创建Secret弹窗校验规则同单独创建Secret资源弹窗
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，用户首次登录并创建资源，无可选Secret，在选择用户仓库镜像后自动创建imagepullSecret
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，用户再次创建资源，可选相同Secret，不会再自动创建imagepullSecret
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，用户再次创建时同ns资源可选择同一镜像仓库的imagepullSecret，在选择镜像时可选对应仓库的镜像
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，用户再次创建时可选择不同用户镜像仓库的镜像，在选择镜像后自动创建所选仓库的imagepullSecret
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，用户再次创建不同ns资源时选择同用户镜像仓库的镜像，在选择镜像后自动创建新的imagepullSecret
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，用户使用其他自建仓库的镜像，可选择下拉列点击创建Secret，创建后回填
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，用户创建的其他自建仓库的镜像Secret，可在下次创建时使用
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，用户创建时没有Secret权限，手动输入同ns已创建的imagepullSecret，创建后pull镜像成功-多租户
                                    创建Deployment - 基本信息：Pod配置 - 镜像拉取秘钥，用户创建时没有Secret权限，镜像输入用户镜像仓库的镜像，创建时imagepullSecret自动创建失败
                                调度策略
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，勾选后展示配置项，文案校验
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，勾选后配置，再取消勾选不展示配置，再次勾选时保留配置
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 - 默认勾选「任何可用节点」且其他选项为禁用状态
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 - 取消勾选「任何可用节点」其他选项启用可勾选状态
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 - 勾选「根据节点名称选择节点」其他选项为禁用状态
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 - 取消勾选「根据节点名称选择节点」其他选项启用可勾选状态
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 - 勾选「根据节点选择器选择节点」前两项禁用不可选择，第4项可同时选择
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 - 勾选「根据节点亲和性选择节点」前两项禁用不可选择，第3项可同时选择
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点名称选择节点」展示节点名称选择器，下拉展示节点信息
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点名称选择节点」不选择节点时，为空校验：请选择节点
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点名称选择节点」租户为输入框，不输入节点时，为空校验：请填写节点名称
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」展示标签键值对选择节点
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」键为空时报错：请填写键
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」键格式不正确时报错：格式错误
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」值允许为空
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」值格式不正确时报错：格式错误
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」添加多个标签
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」移除标签
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」引用节点标签，点击popover展示弹窗
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」引用节点标签，展示节点所有标签键值对及所属节点名称
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」引用节点标签，所属节点多个时展示数量，hover时展示节点名称
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」引用节点标签，可勾选多个节点标签
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」引用节点标签，未勾选节点标签时，「添加」按钮禁用
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」引用节点标签，勾选后添加，退出弹窗展示所选，可二次编辑
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」引用节点标签，无节点标签时popover展示
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」引用节点标签，当节点名称较长时下拉及展示正确
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点选择器选择节点」租户视角时不展示引用节点标签
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」展示规则组
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则组条件，默认为「必须满足」
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则组条件，切换「尽量满足」，显示权重
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则组条件「尽量满足」，权重输入框仅允许输入阿拉伯数字
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则组条件「尽量满足」，权重输入框为空报错：请填写权重
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则组条件「尽量满足」，权重仅支持1-100之间的整数
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则：键/值默认为输入框
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则：操作符默认为「在列表中」
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则：键/值为空校验：请填写键/值
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则：键/值格式校验：格式错误
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则：操作符下拉可切换项展示
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则：hover值键时展示规则
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则：操作符选择在列表中/不在列表中，值输入框可输入多个
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则：操作符选择大于/小于，值输入框仅支持输入整数值
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则：操作符选择存在/不存在，输入框禁用
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」同规则组，添加多个标签规则
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」同规则组，移除标签规则
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」同规则组，引用节点标签
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」同规则组，租户视角不展示引用节点标签
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」添加多个规则组
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」多个规则组时移除
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」多个规则组间为「或」关系
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，节点调度策略 -「根据节点亲和性选择节点」规则组内为「与」关系
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 - 可同时或单独选择「亲和性」和「反亲和性」，文案及默认展示
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组条件，默认「必须满足」
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组条件，切换为「尽量满足」，展示权重
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组条件，「尽量满足」权重仅允许输入阿拉伯数字
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组条件，「尽量满足」权重为空时报错：请填写权重
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组条件，「尽量满足」权重仅支持1-100之间的整数
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组「名字空间」默认为空，提示「留空则和Pod使用相同的名字空间」
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组「名字空间」可支持多选和搜索ns
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组「名字空间」租户场景时，仅允许选择项目内名字空间，可选择多个
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchLabels，展示标签键值对，值选填
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchLabels，可添加多个标签键值对
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchLabels，多个标签键值对时移除标签
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchLabels，点击「引用Pod标签」显示popover弹窗
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchLabels，「引用Pod标签」不选择pod时添加按钮禁用
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchLabels，「引用Pod标签」可选择pod对应选择namespace下的所有pod
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchLabels，「引用Pod标签」未选择名字空间，则展示deployment对应ns下所有pod
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchLabels，「引用Pod标签」选择多个ns时，展示pod并集
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchLabels，「引用Pod标签」搜索ns下pod，可对应匹配选择
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchLabels，「引用Pod标签」选择pod后添加，展示该pod所有标签
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchLabels，「引用Pod标签」可对选择pod展示标签进行二次编辑
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchLabels，「引用Pod标签」当pod名称过长时，选中及下拉展示正确
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，展示标签键值对以及操作符
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，操作符默认「在列表中」，点击展示其他操作符
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，hover值时tooltip展示规则
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，键/值格式校验：格式错误
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，键/值为空校验：请填写键/值
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，操作符选择在列表中/不在列表中，值输入框可输入多个
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，操作符选择存在/不存在，输入框禁用
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，可添加多个标签键值对
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，多个标签键值对时移除标签
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，「引用Pod标签」，校验与matchLabels相同
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，拓扑域必填项校验 ：请选择拓扑域
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，拓扑域选择框提示：请选择节点的标签
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，多租户场景拓扑域必填项校验 ：请填写拓扑域
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，多租户场景拓扑域为输入框，提示语：请输入节点的标签
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，拓扑域点击下展示节点中标签的键
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组勾选matchExpressions，拓扑域选择节点标签后回显展示，可匹配到对应节点
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  规则组同时勾选matchLabels和matchExpressions
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  亲和性/反亲和性规则组校验一致
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  添加多个亲和性规则组
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  添加多个反亲和性规则组
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  移除一个规则组
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  仅勾选亲和性，仅可添加亲和性规则组
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  仅勾选反亲和性，仅可添加反亲和性规则组
                                    创建Deployment - 基本信息：Pod配置 - 调度策略，Pod调度策略 -  同时勾选亲和性/反亲和性，添加多个亲和性/反亲和性规则组
                                容忍
                                    创建Deployment - 基本信息：Pod配置 - 容忍，勾选后展示配置项，文案校验
                                    创建Deployment - 基本信息：Pod配置 - 容忍，操作符为「等于」时，键必填项校验
                                    创建Deployment - 基本信息：Pod配置 - 容忍，操作符为「存在」时，键为选填项
                                    创建Deployment - 基本信息：Pod配置 - 容忍，键格式校验，同其他键格式
                                    创建Deployment - 基本信息：Pod配置 - 容忍，操作符，默认选中展示「等于」，下拉查看可选项
                                    创建Deployment - 基本信息：Pod配置 - 容忍，值，当操作符为「等于」时为选填项
                                    创建Deployment - 基本信息：Pod配置 - 容忍，值，切换操作符为「存在」，输入框禁用
                                    创建Deployment - 基本信息：Pod配置 - 容忍，效果，默认展示「全部」，下拉查看可选项
                                    创建Deployment - 基本信息：Pod配置 - 容忍，容忍时间（选填），非必填项，默认禁用状态，单位显示秒
                                    创建Deployment - 基本信息：Pod配置 - 容忍，容忍时间（选填），切换效果为「阻止调度并驱逐Pod」时，输入框可输入整数
                                    创建Deployment - 基本信息：Pod配置 - 容忍，添加多条容忍规则
                                    创建Deployment - 基本信息：Pod配置 - 容忍，多条规则时移除规则
                                    创建Deployment - 基本信息：Pod配置 - 容忍，引用节点污点，点击popover「指定节点」弹窗，默认添加按钮禁用
                                    创建Deployment - 基本信息：Pod配置 - 容忍，引用节点污点，可勾选多个节点污点
                                    创建Deployment - 基本信息：Pod配置 - 容忍，引用节点污点，当无节点污点时，展示为空
                                    创建Deployment - 基本信息：Pod配置 - 容忍，引用节点污点，若此时手动移除节点污点，勾选其并添加 - 应该可添加成功
                                    创建Deployment - 基本信息：Pod配置 - 容忍，引用节点污点，此时对节点增加新的污点，再次点击引用时展示，可添加成功
                                    创建Deployment - 基本信息：Pod配置 - 容忍，引用节点污点，勾选后点击添加，展示容忍规则，可以二次编辑
                                    创建Deployment - 基本信息：Pod配置 - 容忍，引用节点污点，租户视角时不展示按钮
                                    创建Deployment - 基本信息：Pod配置 - 容忍，当引用节点污点时，操作符为空，默认展示为「等于」
                                网络
                                    创建Deployment - 基本信息：Pod配置 - 网络，勾选后展示配置项，文案校验
                                    创建Deployment - 基本信息：Pod配置 - 网络，网络模式 - 默认选中「容器网络」，可切换「主机网络」
                                    创建Deployment - 基本信息：Pod配置 - 网络，网络模式 - 切换「主机网络」，配置后查看hostNetwork: true是否配置成功
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 默认关闭，编辑开启展示配置
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - DNS策略，默认为「ClusterFirst」，点击查看其他策略项
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - DNS策略，切换其他策略，可切换成功并展示
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 点击添加域名服务器，输入框为空校验：请填写域名服务器。
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 域名服务器，IP地址格式校验
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 域名服务器，一个输入框仅支持填写1个域名服务器
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 域名服务器，可添加多个域名服务器
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 域名服务器，多个域名服务器时移除
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 域名服务器，添加重复的IP地址，提交后实际配置去重---TBD
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 域名服务器，添加3个IP地址时添加按钮禁用，最多支持添加3个
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 点击添加搜索域，输入框为空校验：请填写搜索域
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 搜索域，可添加多个搜索域
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 搜索域，多个搜索域时点击移除
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 搜索域，搜索域格式校验
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 搜索域，添加32搜索域时，添加按钮禁用，最多支持32个
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 添加Options，展示配置项，输入框为空校验：请填写配置项
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 添加Options，配置值选填，可不配置
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - Options，添加多个配置
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - Options，多个配置时移除
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 添加主机别名，IP地址输入框为空校验：请填写IP地址
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 添加主机别名，域名输入框为空校验：请填写域名
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 添加主机别名，IP地址输入框格式校验：IP地址格式错误
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 添加主机别名，域名输入框格式校验：域名格式错误
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 主机别名，1个IP地址可设置多个域名，域名输入框中多个域名间用“，”隔开
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 主机别名，可添加多个
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 主机别名，添加多个主机别名时移除
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 开启后使用默认配置，不添加任何配置，可进行下一步
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 开启后使用添加任意配置输入框但不填写，无法进入下一步，移除后配置后可提交
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 配置后进入pod查看/etc/resolv.conf域名配置是否一致
                                    创建Deployment - 基本信息：Pod配置 - 网络，DNS配置 - 配置后进入pod查看/etc/hosts主机别名配置是否一致
                                高级设置
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，默认收起，点击展开配置
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - 勾选展示相关配置项
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - 点击开启或关闭 runAsNonRoot，默认为关闭
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - runAsUser参数选填，可不输入
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - runAsUser 输入框仅允许输入整数值
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - runAsUser检查配置后是否生效
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - runAsGroup参数选填，可不输入
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - runAsGroup 输入框仅允许输入整数值
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - runAsGroup 检查配置后是否生效
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - fsGroup参数选填，可不输入
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - fsGroup 输入框仅允许输入整数值
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - fsGroup 检查配置后是否生效
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - supplementalGroups参数选填，可不输入
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - supplementalGroups 输入框仅允许输入整数值
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - supplementalGroups 可添加多个参数框
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - supplementalGroups 添加多个输入框时点击移除
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，安全上下文 - supplementalGroups 当有设置fsGroup时，自动配置相同的值
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，标签 - 默认自动设置为「app：%工作负载名称%」，禁用不可修改及移除
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，标签 - 添加额外标签，格式校验同其他，可移除
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，标签 - 查看格式要求
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，标签 - 添加注解，格式校验同其他
                                    创建Deployment - 基本信息：Pod配置 - 高级设置，标签 - 添加多个注解，可移除
                            配置切换
                                创建Deployment - 基本信息- 从工作负载配置切换Pod配置，工作负载有任意校验问题（错误或为空），不允许切换或进入下一步
                                创建Deployment - 基本信息 - Pod配置为选填项，可不做任何操作进行下一步容器配置
                                创建Deployment - 基本信息 - Pod配置中某一项不设置或不勾选配置时，可再切换回工作负载配置
                                创建Deployment - 基本信息 - Pod配置勾选checkbox展开配置，内容为空，不允许再切换回工作负载配置
                                创建Deployment - 基本信息 - Pod配置勾选checkbox，内容为空，取消勾选checkbox，可切换回工作负载配置
                                创建Deployment - 基本信息 - Pod配置勾选checkbox，展开子项中有部分必填项未填写，不允许切换或进入下一步
                                创建Deployment - 基本信息- Pod配置勾选checkbox，展开子项中有任意项格式错误，不允许切换或进入下一步
                                创建Deployment - 基本信息- Pod配置项展开并均设置正确，允许切换回工作负载配置或进入下一步
                                创建Deployment - 基本信息- 配置后点击取消退出创建，再次点开时配置还原
                                创建Deployment - 基本信息- 配置后切换YAML，可查看yaml中当前配置项已写入，且参数格式正确
                                创建Deployment - 基本信息- 切换至YAML后修改配置，可直接从yaml编辑配置提交创建，参数生效
                                创建Deployment - 基本信息- 切换至YAML后修改配置，再次切换回表单时不保留yaml修改内容，但表单配置保留，无变化
                                创建Deployment - 基本信息- 切换至YAML后再切回表单，有编辑表单弹窗提示
                        容器设置
                            交互设置
                                创建Deployment - 容器配置 - Tab Bar，显示和管理不同容器的配置项，UI检查
                                创建Deployment - 容器配置 - Tab Bar，每个标签显示对应的容器名称，与配置中容器名称相同，修改容器名称tab对应更新
                                创建Deployment - 容器配置 - Tab Bar，添加多个配置时，可移除配置，无数量限制
                                创建Deployment - 容器配置 - Tab Bar，容器名称添加多个无法完整展示时收入折叠项，点击折叠展开列表展完整名称
                                创建Deployment - 容器配置 - Tab Bar，首项容器tab名称超长无法展示全，截断打点展示
                                创建Deployment - 容器配置 - Tab Bar，多个容器配置表单，表单中有必填项未填写或选填项展开配置，切换时，错误容器tab展示error图标
                                创建Deployment - 容器配置 - Tab Bar，有错误时，无法提交下一步或创建
                                创建Deployment - 容器配置 - Tab Bar，多个容器配置表单，有error图标，填写配置或修正错误后，error图标隐藏
                                创建Deployment - 容器配置 - 填写完容器配置后，可直接点击创建，访问方式为选填项
                                创建Deployment - 容器配置 - 填写完容器配置后，可点进入上一步修改
                                创建Deployment - 容器配置 - 填写完容器配置后，可点击进入下一步配置访问方式
                                创建Deployment - 容器配置 - 填写完容器配置后，点击取消退出创建，再次点开时配置还原
                                创建Deployment - 容器配置 - 切换yaml后再切回表单，配置不变，yaml修改内容不保存
                                创建Deployment - 容器配置 - 配置完成后可直接点击创建，创建成功，查看配置
                                创建Deployment - 容器配置 - 配置中有必填项未填写时，不允许创建或下一步/上一步
                                创建Deployment - 容器配置 - 配置中有配置错误，不允许创建或下一步/上一步
                                创建Deployment - 容器配置 - 配置完成后，点击切换YAML配置，查看YAML中参数填充正确
                                创建Deployment - 容器配置 - 配置切换YAML后，在YAML中修改，可直接提交创建
                                创建Deployment - 容器配置 - 高级设置，默认收起，点击展开配置
                                创建Deployment - 容器配置 - 配置多个容器，切换YAML查看配置信息是否正确
                            基本信息
                                创建Deployment - 容器配置 - 基本信息，容器类型 - 默认项为「工作容器」，可切换初始化容器，切换后高级设置不显示「健康检查」
                                创建Deployment - 容器配置 - 基本信息，容器名称 - 默认填充container-0，添加多个时依次增加数，与标签栏联动
                                创建Deployment - 容器配置 - 基本信息，容器名称 - 清空名称，为空报错：请填写容器名称
                                创建Deployment - 容器配置 - 基本信息，容器名称 - 字符限制，名称支持的字符长度范围为1-63
                                创建Deployment - 容器配置 - 基本信息，容器名称 - 支持小写字母、数字、连字符，必须小写字母、数字开头和结尾
                                创建Deployment - 容器配置 - 基本信息，容器名称 - 多个容器配置tab时不允许重名：名称已存在
                                创建Deployment - 容器配置 - 基本信息，容器镜像 - 为空时报错：请填写容器镜像
                                创建Deployment - 容器配置 - 基本信息，容器镜像 - 有用户容器-用户输入搜索一次后清空，点击下拉菜单可显示所有符合用户权限的镜像仓库名称
                                创建Deployment - 容器配置 - 基本信息，容器镜像 - 当前有用户容器-输入关键词，下拉菜单自动筛选符合字段的选项
                                创建Deployment - 容器配置 - 基本信息，容器镜像 - 输入字段无相关匹配内容，不显示下拉菜单
                                创建Deployment - 容器配置 - 基本信息，容器镜像 - 使用管理员用户，可展示所有用户容器镜像公共仓库的相关镜像
                                创建Deployment - 容器配置 - 基本信息，容器镜像 - 使用租户登录，可展示有镜像仓库权限的用户容器镜像仓库的镜像
                                创建Deployment - 容器配置 - 基本信息，容器镜像 - 用户有权限的多个用户容器镜像仓库，可展示多个镜像仓库的镜像
                                创建Deployment - 容器配置 - 基本信息，容器镜像 - 可直接输入公网镜像，展示正确
                                创建Deployment - 容器配置 - 基本信息，容器镜像 - 可添加私有镜像仓库的镜像 ，前提时已创建私有镜像imagepullsecret，创建后pull镜像成功
                                创建Deployment - 容器配置 - 基本信息，容器镜像 - 选择镜像后自动填充至输入框，展示正确，无溢出
                                创建Deployment - 容器配置 - 基本信息，镜像版本 - 当未选择容器镜像时，镜像版本为禁用状态，选择镜像后启用
                                创建Deployment - 容器配置 - 基本信息，镜像版本 - 根据容器镜像输入自动匹配并填充最新时间的版本（用户容器镜像）
                                创建Deployment - 容器配置 - 基本信息，镜像版本 - 当选择容器镜像对应多个版本时，可下拉选择其他版本
                                创建Deployment - 容器配置 - 基本信息，镜像版本 - 用户可手动修改到其他的镜像版本
                                创建Deployment - 容器配置 - 基本信息，镜像版本 - 当输入的容器镜像为手动输入的其他仓库镜像时，匹配不到版本，需手动输入
                                创建Deployment - 容器配置 - 基本信息，镜像版本 - 可选择不填写镜像版本
                                创建Deployment - 容器配置 - 基本信息，镜像版本 - 当输入公网镜像自带tag时如（nginx:latest），可不填写镜像版本
                                创建Deployment - 容器配置 - 基本信息，镜像拉取策略 - 默认选择「Always」，点击查看可选项
                                创建Deployment - 容器配置 - 基本信息，镜像拉取策略 - 选择切换其他镜像拉取策略
                                创建Deployment - 容器配置 - 基本信息，启动命令 - 勾选后展示相关配置项，查看配置项及描述
                                创建Deployment - 容器配置 - 基本信息，启动命令 - 勾选后，命令未填写，可允许为空
                                创建Deployment - 容器配置 - 基本信息，启动命令 - 勾选后，参数未填写，可允许为空
                                创建Deployment - 容器配置 - 基本信息，启动命令 - 命令，输入单一命令，可正常解析
                                创建Deployment - 容器配置 - 基本信息，启动命令 - 命令，输入多个命令组，可正常解析
                                创建Deployment - 容器配置 - 基本信息，启动命令 - 命令，输入多组命令后，输入框自动调整高度，展示完整
                                创建Deployment - 容器配置 - 基本信息，启动命令 - 参数，输入单一参数，可正常解析
                                创建Deployment - 容器配置 - 基本信息，启动命令 - 参数，输入多个参数组，可正常解析
                                创建Deployment - 容器配置 - 基本信息，启动命令 - 参数，输入多组参数后，输入框自动调整高度，展示完整
                                创建Deployment - 容器配置 - 基本信息，启动命令 - 输入命令、参数后查看yaml中填充，分隔正确
                                创建Deployment - 容器配置 - 基本信息，启动命令 - 输入命令、参数正确时，创建deployment能正常执行
                                创建Deployment - 容器配置 - 基本信息，容器配额 - 勾选后展示相关配置项，查看配置项及描述
                                创建Deployment - 容器配置 - 基本信息，容器配额 - 可不输入配置，为空不限制，GPU默认为空
                                创建Deployment - 容器配置 - 基本信息，容器配额 - 所有资源对象均仅允许输入阿拉伯数字
                                创建Deployment - 容器配置 - 基本信息，容器配额 - 仅允许输入非负整数，输入负数报错：仅支持大于等于0的整数
                                创建Deployment - 容器配置 - 基本信息，容器配额 - 当输入CPU/内存请求超过限制时报错：资源请求不能超过资源限制
                                创建Deployment - 容器配置 - 基本信息，容器配额 - 当设置为0时表示无法使用该资源，谨慎配置
                                创建Deployment - 容器配置 - 基本信息，容器配额 - CPU 请求/CPU 限制 - 默认单位为m，可切换为core
                            高级设置
                                容器端口
                                    创建Deployment - 容器配置 - 高级设置，容器端口 - 勾选展示相关配置项
                                    创建Deployment - 容器配置 - 高级设置，容器端口 - 名称，可不输入
                                    创建Deployment - 容器配置 - 高级设置，容器端口 - 名称，输入时字符长度1-15
                                    创建Deployment - 容器配置 - 高级设置，容器端口 - 名称，输入时，仅支持小写字母、数字和连字符
                                    创建Deployment - 容器配置 - 高级设置，容器端口 - 名称，需以小写字母或数字开头结尾
                                    创建Deployment - 容器配置 - 高级设置，容器端口 - 名称，添加多个端口时，不允许重名
                                    创建Deployment - 容器配置 - 高级设置，容器端口 - 端口，必填项：请填写端口
                                    创建Deployment - 容器配置 - 高级设置，容器端口 - 端口，仅支持1-65535之间的整数
                                    创建Deployment - 容器配置 - 高级设置，容器端口 - 协议，可选择TCP/UDP
                                    创建Deployment - 容器配置 - 高级设置，容器端口 - 添加多个不同端口配置
                                    创建Deployment - 容器配置 - 高级设置，容器端口 - 添加多个时移除端口
                                环境变量
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 勾选展开配置项，默认为「键值对」
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 键值对，变量名必填：请填写变量名
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 键值对，变量名：仅支持字母、数字、连字符和下划线，且必须以字母或下划线开头
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 键值对，若添加多个，不允许重名：名称已存在。
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 键值对，值为必填项：请填写值
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 资源引用，变量名必填：请填写变量名
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 资源引用，变量名：仅支持字母、数字、连字符和下划线，且必须以字母或下划线开头
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 资源引用，若添加多个，不允许重名：名称已存在。
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 资源引用，容器名称选填
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 资源引用，容器名称，输入其他当前添加的容器名称
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 资源引用，键为必选项：请选择键
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 资源引用，键查看可选项，选择不同配置
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap Key，变量名必填：请填写变量名
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap Key，变量名：仅支持字母、数字、连字符和下划线，且必须以字母或下划线开头
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap Key，若添加多个，不允许重名：名称已存在。
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap Key，下拉选择ConfigMap，不选择时报错：请选择ConfigMap
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap Key，下拉选择ConfigMap时，可点击创建ConfigMap，弹窗校验同单独创建ConfigMap
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap Key，点击创建ConfigMap，创建后自动回填选择新创建的ConfigMap
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap Key，可选择对应ns下所有，选择ConfigMap后，下拉键展示对应所选ConfigMap中所有键
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap Key，租户无ConfigMap权限，下拉选择ConfigMap时获取无数据
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap Key，租户无ConfigMap权限，下拉列隐藏「创建ConfigMap」按钮
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap Key，键必填项，不选择时报错：请选择键
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap Key，可添加多个环境变量设置同一个ConfigMap并选择不同的键
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret Key，变量名必填：请填写变量名
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret Key，变量名：仅支持字母、数字、连字符和下划线，且必须以字母或下划线开头
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret Key，若添加多个，不允许重名：名称已存在。
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret Key，下拉选择Secret，不选择时报错：请选择Secret
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret Key，下拉选择Secret时，可点击创建Secret，弹窗校验同单独创建Secret
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret Key，点击创建Secret，创建后自动回填选择新创建的Secret
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret Key，可选择ns下所有，选择Secret后，下拉键展示对应所选Secret中所有键
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret Key，租户无Secret权限，下拉选择Secret时获取无数据
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret Key，租户无Secret权限，下拉列隐藏「创建Secret」按钮
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret Key，键必填项，不选择时报错：请选择键
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret Key，可添加多个环境变量设置同一个Secret并选择不同的键
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 字段引用，变量名必填：请填写变量名
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 字段引用，变量名：仅支持字母、数字、连字符和下划线，且必须以字母或下划线开头
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 字段引用，若添加多个，不允许重名：名称已存在。
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - 字段引用，键为必选项：请填写键
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap，前缀格式：仅支持字母、数字和下划线，且必须以字母或下划线开头
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap，下拉选择ConfigMap，不选择时报错：请选择ConfigMap
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap，下拉选择ConfigMap时，可点击创建ConfigMap，弹窗校验同单独创建ConfigMap
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap，点击创建ConfigMap，创建后自动回填选择新创建的ConfigMap
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap ，租户无ConfigMap权限，下拉选择ConfigMap时获取无数据
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - ConfigMap ，租户无ConfigMap权限，下拉列隐藏「创建ConfigMap」按钮
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret，前缀格式：仅支持字母、数字和下划线，且必须以字母或下划线开头
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret，下拉选择Secret，不选择时报错：请选择Secret
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret，下拉选择Secret时，可点击创建Secret，弹窗校验同单独创建Secret
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret，点击创建Secret，创建后自动回填选择新创建的Secret
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret，租户无Secret权限，下拉选择Secret时获取无数据
                                    创建Deployment - 容器配置 - 高级设置，环境变量 - Secret，租户无Secret权限，下拉列隐藏「创建Secret」按钮
                                健康检查
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 当选择配置容器为初始化容器时，不展示该项
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 勾选展开配置项，默认均未开启
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，开启后展示配置项
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「HTTP请求」- 可选择协议HTTP、HTTPS，默认HTTP
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「HTTP请求」- 端口必填项：请填写端口
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「HTTP请求」- 端口格式：仅支持 1-65535 之间的整数或字符串。
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「HTTP请求」-  路径必填项：请填写路径
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「HTTP请求」- 格式校验：请以“/”开头
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「HTTP请求」- 添加请求头后，必填项校验：请填写名称/请填写值
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「HTTP请求」-  添加多个请求头，允许移除
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查 -「延时时间」输入限制：仅允许输入阿拉伯数字，单位秒
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查 -「延时时间」需输入非负整数：仅支持大于等于0的整数，默认值0
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查 -「超时时间」输入限制：仅允许输入阿拉伯数字，单位秒
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查 -「超时时间」需输入大于0的整数：仅支持大于0的整数，默认值1
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查 -「检测周期」输入限制：仅允许输入阿拉伯数字，单位秒
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查 -「检测周期」需输入大于0的整数：仅支持大于0的整数，默认值10
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查 -「成功阈值」不可修改，默认值1
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查 -「失败阈值」输入限制：仅允许输入阿拉伯数字
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查 -「失败阈值」需输入大于0的整数：仅支持大于0的整数，默认值3
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「TCP连接」- 端口必填项：请填写端口
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「TCP连接」- 端口格式：可输入数字或字符串
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「命令」- 命令必填项：请填写命令
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「命令」- 输入命令行，可允许输入多个，输入框自动扩展
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「gRPC」- 端口必填项：请填写端口
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「gRPC」- 端口格式：仅支持 1-65535 之间的整数或字符串。
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 启动检查，检查方式「gRPC」- 服务名称：选填，可不输入
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 存活检查 -「成功阈值」不可修改，默认值1
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 存活检查 - 其余输入项同启动检查
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 就绪检查 -「成功阈值」输入限制：仅允许输入阿拉伯数字
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 就绪检查 -「成功阈值」需输入大于0的整数：仅支持大于0的整数，默认值1
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 就绪检查 - 其余输入项同启动检查
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 开启并配置多项不同检查内容，可配置成功
                                    创建Deployment - 容器配置 - 高级设置，健康检查 - 配置后关闭开关，收起配置项，不关闭页面再次打开时配置依旧展示
                                数据存储
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 勾选展开配置项，默认均未开启
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 数据卷默认类型选择「持久卷申领」，点击可选择切换其他类型
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 持久卷申领，为空校验：请选择持久卷申领
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 持久卷申领，下拉可选择已有ns下存在的PVC
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 持久卷申领，已存在的PVC为RWO模式且已被挂载，不允许选择，提示已被使用
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 持久卷申领，可选择创建PVC，创建后自动回显并展示新创建pvc
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 无存储权限的租户，持久卷申领下拉列为空数据
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 无存储权限的租户，持久卷申领下拉列隐藏创建按钮
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 子路径，默认选择subPath，选填项
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 子路径，subPath 格式校验：不能以“/”开头且不能包含“..”
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 子路径，subPath  可输入文件或子路径
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 子路径，切换选择subPathExpr
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 子路径，subPathExpr 格式校验：不能包含“..”
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 子路径，subPathExpr  输入后配置正确
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 容器挂载路径，必填项：请填写容器挂载路径
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 容器挂载路径，格式校验：请以“/”开头
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 权限，默认选择为「读写」，允许切换为「只读」
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 类型选择「临时路径」，配置项展示，相同配置校验同持久卷申领
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 类型选择「主机路径」，配置项展示，相同配置校验同持久卷申领
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 主机路径，必填项校验：请填写宿主机路径
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 主机路径，格式校验：请以“/”开头
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 类型选择「ConfigMap」，配置项展示，相同配置校验同持久卷申领
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，下拉选择已有ConfigMap，展示相应ns下全部
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，可选择创建新的ConfigMap，弹窗校验同单独创建
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，创建新的ConfigMap后自动填充选择
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，必选项：请选择ConfigMap
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，无配置权限的租户，下拉选择时无数据
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，无配置权限的租户，下拉列创建按钮隐藏
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，勾选ConfigMap Key，展示映射键配置项
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，勾选ConfigMap Key，键必选项：请选择键
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，勾选ConfigMap Key，可选择ConfigMap下所有key，包含data和binaryData的key
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，无配置权限的租户，ConfigMap Key下拉列无数据
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，勾选ConfigMap Key，路径必填项：请填写路径
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，勾选ConfigMap Key，路径格式-可能以“/”开头，相对路径
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，勾选ConfigMap Key，可添加多个映射键，支持移除
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - ConfigMap，勾选ConfigMap Key，添加多个映射键，切换Secret，配置清空恢复默认
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - 类型选择「Secret」，配置项展示，相同配置校验同持久卷申领
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - Secret，下拉选择已有Secret，展示相应ns下全部
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - Secret，可选择创建新的Secret，弹窗校验同单独创建
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - Secret，创建新的Secret后自动填充选择
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - Secret，必选项：请选择Secret
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - Secret，无配置权限的租户，下拉选择时无数据
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - Secret，无配置权限的租户，下拉列创建按钮隐藏
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - Secret，勾选Secret Key，展示映射键配置项，校验同ConfigMap Key
                                    创建Deployment - 容器配置 - 高级设置，数据存储 - Secret，无配置权限的租户，Secret Key下拉列无数据
                                生命周期钩子
                                    创建Deployment - 容器配置 - 高级设置，生命周期钩子 - 勾选展开配置项，默认均未勾选
                                    创建Deployment - 容器配置 - 高级设置，生命周期钩子 - PostStart 点击开启查看配置项
                                    创建Deployment - 容器配置 - 高级设置，生命周期钩子 - 检查方式「HTTP请求」- 可选择协议HTTP、HTTPS，默认HTTP
                                    创建Deployment - 容器配置 - 高级设置，生命周期钩子 - 检查方式「HTTP请求」- 端口必填项：请填写端口
                                    创建Deployment - 容器配置 - 高级设置，生命周期钩子 - 检查方式「HTTP请求」-  路径必填项：请填写路径
                                    创建Deployment - 容器配置 - 高级设置，生命周期钩子 - 检查方式「HTTP请求」- 路径格式校验：请以“/”开头
                                    创建Deployment - 容器配置 - 高级设置，生命周期钩子 - 检查方式「HTTP请求」- 添加请求头后，必填项校验：请填写名称/请填写值
                                    创建Deployment - 容器配置 - 高级设置，生命周期钩子 - 检查方式「HTTP请求」-  添加多个请求头，允许移除
                                    创建Deployment - 容器配置 - 高级设置，生命周期钩子 - 检查方式「TCP连接」- 端口必填项：请填写端口
                                    创建Deployment - 容器配置 - 高级设置，生命周期钩子 - 检查方式「命令」- 命令必填项：请填写命令
                                    创建Deployment - 容器配置 - 高级设置，生命周期钩子 - 检查方式「命令」- 输入命令行，可允许输入多个，输入框自动扩展
                                    创建Deployment - 容器配置 - 高级设置，生命周期钩子 - PreStop 点击开启查看配置项，与PostStart相同
                                    创建Deployment - 容器配置 - 高级设置，生命周期钩子 - PreStop 配置项校验与PostStart相同
                                安全上下文
                                    创建Deployment - 容器配置 - 高级设置，安全上下文 - 勾选展开配置项，默认均未勾选
                                    创建Deployment - 容器配置 - 高级设置，安全上下文 - 启用privileged，启用后allowPrivilegeEscalation默认启用并禁用
                                    创建Deployment - 容器配置 - 高级设置，安全上下文 - 不启用privileged，可单独启用allowPrivilegeEscalation
                                    创建Deployment - 容器配置 - 高级设置，安全上下文 - 启用readOnlyRootFilesystem，查看描述
                                    创建Deployment - 容器配置 - 高级设置，安全上下文 - 启用readOnlyRootFilesystem，查看配置效果
                                    创建Deployment - 容器配置 - 高级设置，安全上下文 - 启用runAsNonRoot，查看描述
                                    创建Deployment - 容器配置 - 高级设置，安全上下文 - 启用runAsNonRoot，查看配置效果
                                    创建Deployment - 容器配置 - 高级设置，安全上下文 - runAsUser为选填，输入框需输入整数
                                    创建Deployment - 容器配置 - 高级设置，安全上下文 - runAsGroup为选填，输入框需输入整数
                                    创建Deployment - 容器配置 - 高级设置，安全上下文 - Add Capabilites为选填，从下拉框选择配置，可选择多个
                                    创建Deployment - 容器配置 - 高级设置，安全上下文 - Drop Capabilites为选填，从下拉框选择配置，可选择多个
                                    创建Deployment - 容器配置 - 高级设置，安全上下文 - runAsUser设置后，查看是否生效
                                    创建Deployment - 容器配置 - 高级设置，安全上下文 - runAsGroup设置后，查看是否生效
                        访问方式
                            Service
                                创建Deployment - 访问方式 - Service，若已创建service匹配当前标签（app：deployment.name），在列表展示
                                创建Deployment - 访问方式 - Service，列表可点击的链接均不支持跳转
                                创建Deployment - 访问方式 - Service，无匹配service，当前页面展示空「无Service」
                                创建Deployment - 访问方式 - Service，创建Service，弹窗展示
                                创建Deployment - 访问方式 - Service，创建Service，基本信息 - 名称校验，与单独创建Service相同
                                创建Deployment - 访问方式 - Service，创建Service，基本信息 - 名字空间，自动填入与Deployment一致的ns，禁用不可修改
                                创建Deployment - 访问方式 - Service，创建Service，基本信息 - 类型，交互方式同单独创建Service
                                创建Deployment - 访问方式 - Service，创建Service，基本信息 - 标签选择器，根据pod配置中pod标签自动填入，禁用不可修改
                                创建Deployment - 访问方式 - Service，创建Service，基本信息 - 标签选择器，可点击添加其他标签
                                创建Deployment - 访问方式 - Service，创建Service，基本信息 - 标签选择器，标签校验同独立创建Service
                                创建Deployment - 访问方式 - Service，创建Service，基本信息 - 标签选择器，指定工作负载popover禁用，不可点击
                                创建Deployment - 访问方式 - Service，创建Service，基本信息 - 端口配置，校验同单独创建Service
                                创建Deployment - 访问方式 - Service，创建Service，基本信息 - 端口配置，配置容器时指定了端口，添加端口时自动填充容器端口和名称等相关信息
                                创建Deployment - 访问方式 - Service，创建Service，基本信息 - 端口配置，可修改自动填入内容，可修改为容器端口名称
                                创建Deployment - 访问方式 - Service，创建Service，高级设置 - 默认收起，可选择不配置，点击展开配置项
                                创建Deployment - 访问方式 - Service，创建Service，高级设置 - 会话保持交互同单独创建Service
                                创建Deployment - 访问方式 - Service，创建Service，高级设置 - 类型为NodePort或LoadBalancer时可展示外部流量策略，交互同单独创建Service
                                创建Deployment - 访问方式 - Service，创建Service，高级设置 - 标签，点击添加标签，自动设置与depolyment配置一致的标签，禁用不可修改
                                创建Deployment - 访问方式 - Service，创建Service，高级设置 - 标签，可添加其他自定义标签，校验同单独创建Service
                                创建Deployment - 访问方式 - Service，创建Service，高级设置 - 注解，点击添加注解，交互与deployment一致
                                创建Deployment - 访问方式 - Service，创建Service，高级设置 - 注解，可添加其他自定义注解，校验同单独创建Service
                                创建Deployment - 访问方式 - Service，创建Service成功后，自动展示在当前列表中，查看列表内容
                                创建Deployment - 访问方式 - Service，点击列表morebutton，可操作按钮同单独Service列表
                                创建Deployment - 访问方式 - Service，可创建多个Service，创建后均可展示在页面列表
                                创建Deployment - 访问方式 - Service，点击列表中Service编辑，弹窗同单独编辑Service
                                创建Deployment - 访问方式 - Service，编辑列表Service，可编辑成功，列表自动更新
                                创建Deployment - 访问方式 - Service，点击列表Service下载Yaml，可下载成功，yaml内容正确
                                创建Deployment - 访问方式 - Service，点击列表Service删除，可删除成功，列表不再展示
                                创建Deployment - 访问方式 - 返回Deployment第一步修改名字空间，再进入访问方式，对应ns下service列表变更
                                创建Deployment - 访问方式 - 返回Deployment第一步修改标签，再进入访问方式创建service，相应填充的标签更新
                                创建Deployment - 访问方式 - 返回Deployment第一步修改名字空间，再进入访问方式创建service，相应自动填充的ns变更
                                创建Deployment - 访问方式 - 返回Deployment容器配置修改端口，再进入访问方式创建service，相应自动填充的端口配置变更
                                创建Deployment - 访问方式 - 增加Service配置后可直接点击创建，创建Deployment成功，查看配置正确
                            Ingress
                                创建Deployment - 访问方式 - Ingress，当Service页面无Service时，显示tip“需创建Service”，创建Ingress按钮禁用
                                创建Deployment - 访问方式 - Ingress，列表可点击的链接均不支持跳转
                                创建Deployment - 访问方式 - Ingress，当Service页面有Service时，隐藏tip，创建Ingress按钮可用
                                创建Deployment - 访问方式 - Ingress，当已有Ingress目标服务指定了Service页面的Service时，展示对应Ingress列表
                                创建Deployment - 访问方式 - Ingress，当Service页面有Service，但暂未有Ingress指定，则展示为空列表「无Ingress」
                                创建Deployment - 访问方式 - Ingress，已创建Ingress，切回Service，删除仅有一个的Service后，切回Ingress，展示tip，按钮禁用
                                创建Deployment - 访问方式 - Ingress，创建Ingress - 名称校验同单独创建
                                创建Deployment - 访问方式 - Ingress，创建Ingress - 名字空间，自动填入与Deployment一致的ns，禁用不可修改
                                创建Deployment - 访问方式 - Ingress，创建Ingress - IngressClass，校验同单独创建
                                创建Deployment - 访问方式 - Ingress，创建Ingress - 路由规则，自动填入目标服务和目标服务端口
                                创建Deployment - 访问方式 - Ingress，创建Ingress - 路由规则，支持修改目标服务和端口，校验同单独创建
                                创建Deployment - 访问方式 - Ingress，创建Ingress - 路由规则，域名选填，校验同单独创建
                                创建Deployment - 访问方式 - Ingress，创建Ingress - 路由规则，协议选择HTTPS时，展示Secret选项，校验同单独创建
                                创建Deployment - 访问方式 - Ingress，创建Ingress - 路由规则，路径校验同单独创建
                                创建Deployment - 访问方式 - Ingress，创建Ingress - 高级设置，点击展开配置
                                创建Deployment - 访问方式 - Ingress，创建Ingress - 高级设置，标签自动填充Deployment一致的标签，禁用不可修改
                                创建Deployment - 访问方式 - Ingress，创建Ingress - 高级设置，可添加多个其他标签，可修改和移除
                                创建Deployment - 访问方式 - Ingress，创建Ingress - 高级设置，可添加注解，校验同deployment
                                创建Deployment - 访问方式 - Ingress，创建Ingress - 高级设置，可添加多个其他注解，可修改和移除
                                创建Deployment - 访问方式 - Ingress，创建Ingress成功后，自动展示在当前列表中，列表内容与创建一致
                                创建Deployment - 访问方式 - Ingress，可创建多个Ingress，列表展示多行，查看列表
                                创建Deployment - 访问方式 - Ingress，点击列表morebutton，可操作按钮同单独Ingress列表
                                创建Deployment - 访问方式 - Ingress，点击列表中Ingress编辑，弹窗同单独编辑Ingress
                                创建Deployment - 访问方式 - Ingress，编辑列表Ingress，可编辑成功，列表自动更新
                                创建Deployment - 访问方式 - Ingress，点击列表Ingress下载Yaml，可下载成功，yaml内容正确
                                创建Deployment - 访问方式 - Ingress，点击列表Ingress删除，可删除成功，列表不再展示
                                创建Deployment - 访问方式 - 返回Deployment第一步修改名字空间，再进入访问方式，对应ns下Ingress列表变更
                                创建Deployment - 访问方式 - 返回Deployment第一步修改标签注解，再进入访问方式创建Ingress，相应填充的标签注解更新
                                创建Deployment - 访问方式 - 返回Deployment第一步修改名字空间，再进入访问方式创建Ingress，相应自动填充的ns变更
                                创建Deployment - 访问方式 - 增加Service和Ingress配置后点击创建，创建Deployment成功，查看配置正确
                    Deployment管理
                        基本信息
                            Deployment详情-基本信息-查看展示内容
                            Deployment详情-基本信息-编辑Deployment弹窗，查看弹窗展示
                            Deployment详情-基本信息-编辑Deployment-修改基本信息，保存修改内容，编辑成功，查看更新
                            Deployment详情-基本信息-编辑Deployment-修改容器配置，保存修改内容，编辑成功，查看更新
                            Deployment详情-基本信息-编辑Deployment-修改访问方式，保存修改内容，编辑成功，查看更新
                            Deployment详情-基本信息-编辑Deployment-切换YAML配置修改，修改成功，查看更新
                            Deployment详情-基本信息-点击morebutton，编辑YAML-展示原始yaml信息，可直接编辑及保存，同1.5
                            Deployment详情-基本信息-点击morebutton，下载YAML-下载成功，查看yaml文件及配置正常
                            Deployment详情-基本信息-点击more button，重新部署-提交成功，可重新部署
                            Deployment详情-基本信息-点击more button，暂停调度-点击后切换「恢复调度」，Deployment状态更新为「暂停调度」
                            Deployment详情-基本信息-点击more button，恢复调度 - 点击后切换「暂停调度」，Deployment状态恢复
                            Deployment详情-基本信息-点击more button，删除 - 查看删除弹窗，选择删除或取消
                            Deployment详情-基本信息-点击more button，删除 - 选择删除Deployment，提交后更删除成功退出详情，列表删除
                            Deployment列表-查看morebutton-新增按钮调整，操作同详情
                            Deployment详情-基本信息-编辑预期副本数，从弹窗修改pod预期数量，修改成功
                            Deployment详情-基本信息-编辑升级策略，滚动更新弹窗展示，编辑参数成功
                            Deployment详情-基本信息-编辑升级策略，替换更新弹窗展示，切换升级策略，编辑成功
                        Pod
                            基本信息
                                Deployment详情-Pod-默认展示，均折叠展示，根据创建时间倒序排列，查看样式
                                Deployment详情-Pod-基本信息栏展示状态、操作图标以及morebutton
                                Deployment详情-Pod-基本信息栏，点击Pod控制台，弹出pod控制台，操作交互同1.5
                                Deployment详情-Pod-基本信息栏，点击监控，弹出监控弹窗，展示内容与1.5一致
                                Deployment详情-Pod-基本信息栏，点击日志，弹出日志弹窗，展示内容与1.5一致
                                Deployment详情-Pod-基本信息栏，点击事件，弹出事件弹窗，展示内容与1.5一致
                                Deployment详情-Pod-基本信息栏，morebutton点击下载YAML，可下载成功，文件为原始yaml，可读
                                Deployment详情-Pod-基本信息栏，morebutton点击上传文件，可上传成功
                                Deployment详情-Pod-基本信息栏，morebutton点击下载文件，可下载成功
                                Deployment详情-Pod-基本信息栏，morebutton点击删除pod，删除成功，当前pod列删除，pod重建后根据时间倒序展示在最上方
                                Deployment详情-Pod-基本信息栏，触发deployment滚动更新，当前pod列删除，pod重建后根据时间倒序展示在最上方
                                Deployment详情-Pod-点击pod列展开基本信息栏，查看pod信息
                                Deployment详情-Pod-查看pod信息，CPU、内存请求/限制为其下所属容器之和，若其中有容器不限制，则展示为不限制
                                Deployment详情-Pod-查看pod信息，主机名字空间共享，仅展示设置项名称，若均未设置，则展示为「未启用」
                                Deployment详情-Pod-修改deployment配置后滚动更新，重新查看pod信息对应更新
                                Deployment详情-Pod-查看pod信息，pod下所属容器，默认折叠展示，查看容器信息栏
                                Deployment详情-Pod-查看pod信息，点击展开全部容器，页面展示正常，有滚动条
                                Deployment详情-Pod-查看pod信息，展开全部容器后点击收起，仅展示pod基础信息---TBD
                                Deployment详情-Pod-查看pod信息，展开全部容器后，收起其中一个容器信息，可正常收起
                                Deployment详情-Pod-查看pod信息，展开全部pod及容器信息，页面正常，有滚动条
                            容器
                                Deployment详情-pod详情-容器-点击展开查看基本信息展示
                                Deployment详情-pod详情-容器详情-编辑容器镜像，点击展示弹窗交互
                                Deployment详情-pod详情-容器详情-编辑容器镜像，修改镜像后保存，立即生效，查看更新效果
                                Deployment详情-pod详情-容器详情-容器镜像，点击可粘贴容器镜像url，粘贴正确
                                Deployment详情-pod详情-容器详情-编辑镜像拉取策略，点击展示弹窗交互
                                Deployment详情-pod详情-容器详情-编辑镜像拉取策略，修改策略保存，立即生效，查看更新效果
                                Deployment详情-pod详情-容器详情-端口，格式及展示规则
                                Deployment详情-pod详情-容器详情-生命周期Tab，默认展示该Tab，查看基本展示
                                Deployment详情-pod详情-容器详情-生命周期Tab，启动命令-展示「命令」和「参数」，与配置内容一致
                                Deployment详情-pod详情-容器详情-生命周期Tab，启动命令-未配置启动命令时展示空状态
                                Deployment详情-pod详情-容器详情-生命周期Tab，PostStart/PreStop-未配置时展示空状态
                                Deployment详情-pod详情-容器详情-生命周期Tab，PostStart/PreStop-与配置内容一致，单行展示不下时打点处理，hover时tooltip展示完整信息
                                Deployment详情-pod详情-容器详情-生命周期Tab，PostStart/PreStop-HTTP请求时展示内容
                                Deployment详情-pod详情-容器详情-生命周期Tab，PostStart/PreStop-TCP连接时展示内容
                                Deployment详情-pod详情-容器详情-生命周期Tab，PostStart/PreStop-配置命令时展示内容
                                Deployment详情-pod详情-容器详情-环境变量Tab，查看基本展示
                                Deployment详情-pod详情-容器详情-环境变量Tab，键值对展示内容
                                Deployment详情-pod详情-容器详情-环境变量Tab，ConfigMap展示内容
                                Deployment详情-pod详情-容器详情-环境变量Tab，ConfigMap Key展示内容
                                Deployment详情-pod详情-容器详情-环境变量Tab，Secret展示内容
                                Deployment详情-pod详情-容器详情-环境变量Tab，Secret Key展示内容
                                Deployment详情-pod详情-容器详情-环境变量Tab，资源引用展示内容
                                Deployment详情-pod详情-容器详情-环境变量Tab，字段引用展示内容
                                Deployment详情-pod详情-容器详情-环境变量Tab，可配置多种参数，展示多个列表
                                Deployment详情-pod详情-容器详情-健康检查Tab，查看基本展示
                                Deployment详情-pod详情-容器详情-健康检查Tab，启动检查展示内容
                                Deployment详情-pod详情-容器详情-健康检查Tab，存活检查展示内容
                                Deployment详情-pod详情-容器详情-健康检查Tab，就绪检查展示内容
                                Deployment详情-pod详情-容器详情-健康检查Tab，gRPC展示内容
                                Deployment详情-pod详情-容器详情-健康检查Tab，可配置多种参数，展示多个列表
                                Deployment详情-pod详情-容器详情-ConfigMap Tab，查看基本展示
                                Deployment详情-pod详情-容器详情-ConfigMap Tab，查看列表morebutton操作按钮
                                Deployment详情-pod详情-容器详情-ConfigMap Tab，点击列表morebutton编辑ConfigMap，可编辑成功
                                Deployment详情-pod详情-容器详情-ConfigMap Tab，点击列表morebutton下载YAML，可下载成功，文件正确且可读
                                Deployment详情-pod详情-容器详情-ConfigMap Tab，点击列表morebutton删除，可删除成功，列表信息删除
                                Deployment详情-pod详情-容器详情-Secret Tab，查看基本展示
                                Deployment详情-pod详情-容器详情-Secret Tab，查看列表morebutton操作按钮
                                Deployment详情-pod详情-容器详情-Secret Tab，点击列表morebutton编辑Secret，可编辑成功
                                Deployment详情-pod详情-容器详情-Secret Tab，点击列表morebutton下载YAML，可下载成功，文件正确且可读
                                Deployment详情-pod详情-容器详情-Secret Tab，点击列表morebutton删除，可删除成功，列表信息删除
                                Deployment详情-pod详情-容器详情-数据存储 Tab，查看基本展示
                                Deployment详情-pod详情-容器详情-数据存储 Tab，持久卷申领展示内容
                                Deployment详情-pod详情-容器详情-数据存储 Tab，临时路径展示内容
                                Deployment详情-pod详情-容器详情-数据存储 Tab，主路径展示内容
                                Deployment详情-pod详情-容器详情-数据存储 Tab，ConfigMap展示内容
                                Deployment详情-pod详情-容器详情-数据存储 Tab，Secret展示内容
                                Deployment详情-pod详情-容器详情-数据存储Tab，可配置多种类型，展示多个列表
                                Deployment详情-pod详情-容器详情-数据存储Tab，子路径展示，区分subPath/subPathExpr-「类型：路径」
                                Deployment详情-pod详情-容器详情-安全上下文 Tab，查看基本展示
                            调度策略
                                Deployment详情-pod详情-调度策略Tab，节点调度策略「任何可用节点」展示内容
                                Deployment详情-pod详情-调度策略Tab，节点调度策略「根据节点名称选择节点」展示内容
                                Deployment详情-pod详情-调度策略Tab，节点调度策略「根据节点名称选择节点」，点击展示编辑节点名称选择节点弹窗
                                Deployment详情-pod详情-调度策略Tab，节点调度策略「根据节点名称选择节点」，编辑切换为其他节点，可保存成功，触发滚动更新，查看新的配置
                                Deployment详情-pod详情-调度策略Tab，节点调度策略「根据节点名称选择节点」，租户视角，节点名称不可点击跳转
                                Deployment详情-pod详情-调度策略Tab，节点调度策略「根据节点名称选择节点」，租户视角，展示编辑按钮，弹窗为输入框，可修改成功
                                Deployment详情-pod详情-调度策略Tab，节点调度策略「根据节点选择器选择节点」展示内容
                                Deployment详情-pod详情-调度策略Tab，节点调度策略「根据节点亲和性选择节点」展示内容
                                Deployment详情-pod详情-调度策略Tab，节点调度策略「根据节点选择器选择节点」和「根据节点亲和性选择节点」可同时展示
                                Deployment详情-pod详情-调度策略Tab，Pod调度策略「亲和性/反亲和性」展示内容，可同时展示
                                Deployment详情-pod详情-调度策略Tab，编辑Deployment修改节点调度策略，修改成功，触发滚动更新，查看新的pod配置生效
                                Deployment详情-pod详情-调度策略Tab，编辑Deployment修改pod调度策略，修改成功，触发滚动更新，查看新的pod配置生效
                            容忍
                                Deployment详情-pod详情-容忍Tab，展示内容，与配置一致
                                Deployment详情-pod详情-容忍Tab，编辑Deployment修改容忍策略，修改成功，触发滚动更新，查看新的pod配置生效
                                Deployment详情-pod详情-容忍Tab，原始tolerations配置中，没有key时，键展示为「-」，操作符展示「存在」，值展示「」---TBD
                                Deployment详情-pod详情-容忍Tab，原始tolerations配置中，有key，无操作符，无值时展示---TBD
                                Deployment详情-pod详情-容忍Tab，原始tolerations配置中，有key，有操作符，有值，展示与配置操作符一致
                                Deployment详情-pod详情-容忍Tab，原始tolerations配置中，有key，无操作符，有值时，展示---TBD
                                Deployment详情-pod详情-容忍Tab，原始tolerations配置中，有key，无操作符，无值时，展示---TBD
                                Deployment详情-pod详情-容忍Tab，原始tolerations配置中，没有effect时，默认展示为「全部」---TBD
                            网络
                                Deployment详情-pod详情-网络Tab，网络模式，展示模式选择内容
                                Deployment详情-pod详情-网络Tab，DNS配置，不开启时kubernetes自动设置开启并设置dnsPolicy: ClusterFirst
                                Deployment详情-pod详情-网络Tab，DNS配置，开启时查看配置项
                                Deployment详情-pod详情-网络Tab，编辑网络配置后，修改成功，触发滚动更新，查看新的pod配置生效
                            安全上下文
                                Deployment详情-pod详情-安全上下文Tab，展示配置内容
                                Deployment详情-pod详情-安全上下文Tab，编辑Deployment修改安全上下文，修改成功，触发滚动更新，查看新的pod配置生效
                            状况
                                Deployment详情-pod详情-状况Tab，展示实时信息
                                Deployment详情-pod详情-状况Tab，当pod状态触发变更时，实时更新，展示正常
                            标签与注解
                                Deployment详情-pod详情-标签与注解Tab，展示内容，与配置一致
                                Deployment详情-pod详情-标签与注解Tab，未添加标签或注解时展示
                                Deployment详情-pod详情-标签与注解Tab，添加或删除标签或注解，实时更新，查看展示
                        访问方式
                            Deployment详情-访问方式-默认展示Service相关配置，查看内容
                            Deployment详情-访问方式-无Service配置，查看空状态展示
                            Deployment详情-访问方式-创建Service，弹窗校验同Deployment中创建Service弹窗
                            Deployment详情-访问方式-创建Service后退出弹窗，列表自动新增service配置列表，与创建配置一致
                            Deployment详情-访问方式-Service列表morebutton，查看可操作按钮
                            Deployment详情-访问方式-Service列表morebutton点击编辑Service，可编辑成功，列表配置更新
                            Deployment详情-访问方式-Service列表morebutton点击下载YAML，下载成功，查看YAML文件配置一致
                            Deployment详情-访问方式-Service列表morebutton点击删除，可删除Service，删除后列表移除
                            Deployment详情-访问方式-切换Ingress配置，查看内容
                            Deployment详情-访问方式-无Service且无Ingress时，空状态展示，显示General Tip，创建Ingress禁用
                            Deployment详情-访问方式-有Service无Ingress时，展示空状态，创建Ingress按钮可点击，隐藏tip
                            Deployment详情-访问方式-创建Ingress，弹窗校验同Deployment中创建Ingress弹窗
                            Deployment详情-访问方式-创建Ingress后退出弹窗，列表自动新增ingress配置列表，与创建配置一致
                            Deployment详情-访问方式-Ingress列表morebutton，查看可操作按钮
                            Deployment详情-访问方式-Ingress列表morebutton点击编辑Ingress，可编辑成功，列表配置更新
                            Deployment详情-访问方式-Ingress列表morebutton点击下载YAML，下载成功，查看YAML文件配置一致
                            Deployment详情-访问方式-Ingress列表morebutton点击删除，可删除Ingress，删除后列表移除
                            Deployment详情-访问方式-租户无服务访问权限时，隐藏访问方式Tab
                            Deployment详情-访问方式-租户进有查看权限时，隐藏创建按钮及morebutton编辑和删除按钮
                        历史版本
                            Deployment详情-历史版本-默认展示，当前版本/历史版本列表
                            Deployment详情-历史版本-当前版本，morebutton点击查看YAML，展示弹窗，展示当前配置，不可编辑
                            Deployment详情-历史版本-历史版本，morebutton点击查看YAML，展示弹窗，展示对应revision配置，不可编辑
                            Deployment详情-历史版本-历史版本，morebutton点击回滚，展示回滚弹窗
                            Deployment详情-历史版本-历史版本，morebutton点击回滚，确认回滚，弹窗二次确认，提交回滚成功
                            Deployment详情-历史版本-历史版本，一页最多展示10条
                            Deployment详情-历史版本-从历史版本回滚，回滚后所选历史版本更新为当前版本，之前的当前版本更新为历史版本（最新）
                        监控/事件/状况
                            Deployment详情-监控-展示内容与1.5一致，展示数据正确
                            Deployment详情-监控-未开启obs时展示为未开启插件，点击可跳转至设置页面开启
                            Deployment详情-事件-展示内容与1.5一致，展示数据正确
                            Deployment详情-事件-触发deployment滚动更新等操作，产生事件可实时更新展示
                            Deployment详情-状况-展示内容与1.5一致，展示数据正确
                            Deployment详情-状况-触发deployment滚动更新等操作，状况发生变化可实时更新展示
                        标签与注解
                            Deployment详情-标签与注解，展示内容，与配置一致
                            Deployment详情-标签与注解，未添加标签或注解时展示
                            Deployment详情-标签与注解，添加或删除标签或注解，实时更新，查看展示
                StatefulSet
                    创建StatefulSet
                        创建StatefulSet-基本信息-打开创建弹窗后默认展示内容
                        创建StatefulSet-基本信息，工作负载配置-名称校验同创建Deployment
                        创建StatefulSet-基本信息，工作负载配置-名字空间校验同创建Deployment
                        创建StatefulSet-基本信息，工作负载配置-副本数校验同创建Deployment
                        创建StatefulSet-基本信息，工作负载配置-服务名称，与StatefulSet名称同步，输入工作负载名称时，自动填充服务名称
                        创建StatefulSet-基本信息，工作负载配置-服务名称，修改服务名称，为空时提示：请填写服务名称
                        创建StatefulSet-基本信息，工作负载配置-服务名称，修改服务名称，字符数量限制：名称支持的字符长度范围为1-63
                        创建StatefulSet-基本信息，工作负载配置-服务名称，修改服务名称，特殊字符：仅支持小写字母、数字、连字符，并且必须以小写字母或数字开头和结尾
                        创建StatefulSet-基本信息，工作负载配置-服务名称，修改服务名称，同一名字空间重名： 可允许重名，可填入已存在服务
                        创建StatefulSet-基本信息，工作负载配置-高级设置，升级策略-默认展示为滚动更新，查看默认配置项
                        创建StatefulSet-基本信息，工作负载配置-高级设置，升级策略-滚动更新，maxUnavailable，默认值为1
                        创建StatefulSet-基本信息，工作负载配置-高级设置，升级策略-滚动更新，maxUnavailable，仅允许输入阿拉伯数字
                        创建StatefulSet-基本信息，工作负载配置-高级设置，升级策略-滚动更新，maxUnavailable，可允许为空，选填项
                        创建StatefulSet-基本信息，工作负载配置-高级设置，升级策略-滚动更新，maxUnavailable，单位可切换，支持%和个
                        创建StatefulSet-基本信息，工作负载配置-高级设置，升级策略-滚动更新，partition，默认值为0
                        创建StatefulSet-基本信息，工作负载配置-高级设置，升级策略-滚动更新，partition，仅允许输入阿拉伯数字
                        创建StatefulSet-基本信息，工作负载配置-高级设置，升级策略-滚动更新，partition，为空校验：请填写partition
                        创建StatefulSet-基本信息，工作负载配置-高级设置，升级策略-滚动更新，可切换配置为「手动删除更新」，切换后maxUnavailable/partition配置隐藏
                        创建StatefulSet-基本信息，工作负载配置-高级设置，添加标签，校验同创建Deployment
                        创建StatefulSet-基本信息，工作负载配置-高级设置，添加注解，校验同创建Deployment
                        创建StatefulSet-基本信息，Pod配置-校验内容与Deployment一致
                        创建StatefulSet-基本信息，Pod配置-网络配置部分1.6暂不支持配置，隐藏该部分配置
                        创建StatefulSet-容器配置-基本信息，容器类型，支持切换工作容器或初始化容器
                        创建StatefulSet-容器配置-基本信息，容器名称，校验同创建Deployment
                        创建StatefulSet-容器配置-基本信息，容器镜像/版本，校验同创建Deployment，支持搜索选择镜像及autofill镜像版本
                        创建StatefulSet-容器配置-基本信息，镜像拉取策略，默认Always，支持切换IfNotPresent和Never
                        创建StatefulSet-容器配置-基本信息，启动命令，选项及子项校验同创建Deployment
                        创建StatefulSet-容器配置-基本信息，容器配额，选项及子项校验同创建Deployment
                        创建StatefulSet-容器配置-高级设置，容器端口，选项及子项校验同创建Deployment
                        创建StatefulSet-容器配置-高级设置，环境变量，选项及子项校验同创建Deployment
                        创建StatefulSet-容器配置-高级设置，健康检查，选项及子项校验同创建Deployment
                        创建StatefulSet-容器配置-高级设置，数据存储，勾选展示相关配置项「数据卷申领模板」「数据卷」，默认展示一个，支持移除
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，持久卷申领名称，为空校验：请填写持久卷申领名称
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，持久卷申领名称，数量限制：名称支持的字符长度范围为1-253
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，持久卷申领名称，特殊字符：仅支持小写字母、数字、连字符和点，且必须以小写字母或数字开头结尾
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，存储类为空：请选择存储类
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，选择存储类，展示已创建的存储类
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，卷模式，默认为「文件系统」，支持切换为「块」
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，访问模式，默认禁用，选择存储类后启用，启用选择关系同创建pvc
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，访问模式，未选择时提示：请选择访问模式
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，容量为空：请填写容量
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，容量，仅支持输入数字
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，容量单位：默认GiB，支持切换MiB
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，子路径，选填，路径校验同创建Deployment
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，容器挂载路径，校验同创建Deployment
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷申领模板，权限，默认只读，支持切换读写
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷，默认类型为持久卷申领，校验同创建Deployment
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷，切换类型为临时路径，校验同创建Deployment
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷，切换类型为主机路径，校验同创建Deployment
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷，切换类型为ConfigMap，校验同创建Deployment
                        创建StatefulSet-容器配置-高级设置，数据存储-数据卷，切换类型为Secret，校验同创建Deployment
                        创建StatefulSet-容器配置-高级设置，生命周期钩子-校验同创建Deployment
                        创建StatefulSet-容器配置-高级设置，安全上下文-校验同创建Deployment
                        创建StatefulSet-容器配置-添加多个容器配置，校验同创建Deployment
                        创建StatefulSet-容器配置-添加完成后直接创建，可创建成功
                        创建StatefulSet-访问方式-未关联任何Headless的Service时展示提示
                        创建StatefulSet-访问方式-已创建关联Service时展示提示
                        创建StatefulSet-访问方式-创建Service，创建时名称自动填充为基本信息中服务名称，可修改
                        创建StatefulSet-访问方式-创建Service，已创建同名称的Service展示在列表，再点击创建时自动填充为名称，重名，修改名称后可创建
                        创建StatefulSet-访问方式-创建Service，其余校验同创建Deployment中创建Service
                        创建StatefulSet-访问方式-可在已有service列表morebutton点击编辑Service，校验一致
                        创建StatefulSet-访问方式-可在已有service列表morebutton点击删除Service，删除后列表移除，可再次创同名service
                        创建StatefulSet-访问方式-切换Ingress，校验规则与创建Deployment时相同
                    StatefulSet管理
                        StatefulSet详情-点击进入详情，查看基本信息展示
                        StatefulSet详情-基本信息，编辑pod数量，可编辑成功
                        StatefulSet详情-基本信息，点击编辑升级策略，展开编辑弹窗，显示配置信息
                        StatefulSet详情-基本信息，编辑滚动更新升级策略，修改参数配置，可保存成功，参数生效（前提开启MaxUnavailableStatefulSet gate）
                        StatefulSet详情-基本信息，编辑滚动更新升级策略，升级策略切换为手动删除更新，可保存成功，参数生效，信息展示更新
                        StatefulSet详情-基本信息，编辑手动更新升级策略，切换为滚动更新并配置参数，可保存成功，参数生效，展示信息更新
                        StatefulSet详情-基本信息，点击编辑StatefulSet，展开编辑弹窗，查看已配置信息展示
                        StatefulSet详情-基本信息，编辑StatefulSet，名称及名字空间不可编辑
                        StatefulSet详情-基本信息，编辑StatefulSet，基本信息其他编辑项校验同创建
                        StatefulSet详情-基本信息，编辑StatefulSet，容器配置，数据卷申请模板不支持编辑、删除以及新增
                        StatefulSet详情-基本信息，编辑StatefulSet，容器配置其他编辑项校验同创建
                        StatefulSet详情-基本信息，编辑StatefulSet，访问方式编辑项校验同创建
                        StatefulSet详情-基本信息，编辑StatefulSet，修改参数后保存，可修改成功，根据升级策略不同滚动或手动更新后生效
                        StatefulSet详情-基本信息，编辑StatefulSet，从编辑页面切换YAML，查看参数配置
                        StatefulSet详情-基本信息，编辑StatefulSet，从编辑页面切换YAML，修改yaml参数保存，可修改成功
                        StatefulSet详情-基本信息，编辑StatefulSet，从编辑页面切换YAML，修改后切换回表单，yaml修改不保留
                        StatefulSet详情-基本信息，morebutton查看可操作按钮
                        StatefulSet详情-基本信息，morebutton点击编辑YAML，展示原始yaml信息，可编辑及保存yaml生效
                        StatefulSet详情-基本信息，morebutton点击下载YAML，下载成功，yaml文件正常可读
                        StatefulSet详情-基本信息，morebutton点击重新部署，提交成功，根据升级策略执行部署
                        StatefulSet详情-基本信息，点击morebutton删除 - 查看删除弹窗，选择删除或取消
                        StatefulSet详情-基本信息，morebutton点击删除，提交成功，资源本身及pod被删除
                        StatefulSet列表-morebutton查看可操作按钮调整
                        StatefulSet详情-Pod列表，默认折叠展示，交互同Deployment详情
                        StatefulSet详情-Pod列表，可点打开pod控制台并操作
                        StatefulSet详情-Pod列表，可点打开查看pod监控信息
                        StatefulSet详情-Pod列表，可点打开查看pod实时日志
                        StatefulSet详情-Pod列表，可点打开查看pod实时事件
                        StatefulSet详情-Pod列表，可点击morebutton上传文件、下载文件
                        StatefulSet详情-Pod列表，可点击morebutton直接删除pod，删除后滚动更新
                        StatefulSet详情-点击展开Pod详情，基本信息展示正确，交互同Deployment详情
                        StatefulSet详情-Pod详情，默认展示折叠容器列表，显示信息正确，交互同Deployment详情
                        StatefulSet详情-Pod详情，点击展开容器详情，显示正确的配置信息，交互同Deployment详情
                        StatefulSet详情-Pod详情，容器详情-生命周期，展示正确信息，校验同Deployment详情
                        StatefulSet详情-Pod详情，容器详情-环境变量，展示正确信息，校验同Deployment详情
                        StatefulSet详情-Pod详情，容器详情-健康检查，展示正确信息，校验同Deployment详情
                        StatefulSet详情-Pod详情，容器详情-ConfigMap，展示正确信息，校验同Deployment详情
                        StatefulSet详情-Pod详情，容器详情-Secret，展示正确信息，校验同Deployment详情
                        StatefulSet详情-Pod详情，容器详情-数据存储，数据卷信息展示，校验同Deployment详情
                        StatefulSet详情-Pod详情，容器详情-数据存储，数据卷申领模板，展示pvc信息
                        StatefulSet详情-Pod详情，容器详情-安全上下文，展示正确信息，校验同Deployment详情
                        StatefulSet详情-Pod详情-调度策略，展示正确信息，校验同Deployment详情
                        StatefulSet详情-Pod详情-容忍，展示正确信息，校验同Deployment详情
                        StatefulSet详情-Pod详情-网络，展示正确信息，校验同Deployment详情
                        StatefulSet详情-Pod详情-安全上下文，展示正确信息，校验同Deployment详情
                        StatefulSet详情-Pod详情-状况，展示正确信息，校验同Deployment详情
                        StatefulSet详情-Pod详情-标签与注解，展示正确信息，校验同Deployment详情
                        StatefulSet详情-访问方式，展示正确信息，校验同Deployment详情
                        StatefulSet详情-历史版本，展示正确信息，校验同Deployment详情
                        StatefulSet详情-历史版本，点击提交回滚版本，根据升级策略选择生效模式
                        StatefulSet详情-监控，展示正确信息，校验同Deployment详情
                        StatefulSet详情-事件，展示正确信息，校验同Deployment详情
                        StatefulSet详情-状况，展示正确信息，校验同Deployment详情
                        StatefulSet详情-标签与注解，展示正确信息，校验同Deployment详情
                DaemonSet
                    创建DaemonSet
                        创建DaemonSet-基本信息-打开创建弹窗后默认展示内容
                        创建DaemonSet-基本信息，工作负载配置-名称校验同创建Deployment
                        创建DaemonSet-基本信息，工作负载配置-名字空间校验同创建Deployment
                        创建DaemonSet-基本信息，工作负载配置-高级设置，升级策略-默认展示为滚动更新，查看默认配置项
                        创建DaemonSet-基本信息，工作负载配置-高级设置，升级策略-滚动更新，maxUnavailable，仅允许输入阿拉伯数字
                        创建DaemonSet-基本信息，工作负载配置-高级设置，升级策略-滚动更新，maxUnavailable，为空校验：请填写maxUnavailable
                        创建DaemonSet-基本信息，工作负载配置-高级设置，升级策略-滚动更新，可切换配置为「手动删除更新」，切换后maxUnavailable配置隐藏
                        创建DaemonSet-基本信息，工作负载配置-高级设置，添加标签，校验同创建Deployment
                        创建DaemonSet-基本信息，工作负载配置-高级设置，添加注解，校验同创建Deployment
                        创建DaemonSet-基本信息，Pod配置-校验内容与Deployment一致
                        创建DaemonSet-基本信息，Pod配置-网络配置部分1.6暂不支持配置，隐藏该部分配置
                        创建DaemonSet-容器配置-基本信息，容器类型，支持切换工作容器或初始化容器
                        创建DaemonSet-容器配置-基本信息，容器名称，校验同创建Deployment
                        创建DaemonSet-容器配置-基本信息，容器镜像/版本，校验同创建Deployment，支持搜索选择镜像及autofill镜像版本
                        创建DaemonSet-容器配置-基本信息，镜像拉取策略，默认Always，支持切换IfNotPresent和Never
                        创建DaemonSet-容器配置-基本信息，启动命令，选项及子项校验同创建Deployment
                        创建DaemonSet-容器配置-基本信息，容器配额，选项及子项校验同创建Deployment
                        创建DaemonSet-容器配置-高级设置，容器端口，选项及子项校验同创建Deployment
                        创建DaemonSet-容器配置-高级设置，环境变量，选项及子项校验同创建Deployment
                        创建DaemonSet-容器配置-高级设置，健康检查，选项及子项校验同创建Deployment
                        创建DaemonSet-容器配置-高级设置，数据存储-默认类型为持久卷申领，校验同创建Deployment
                        创建DaemonSet-容器配置-高级设置，数据存储-切换类型为临时路径，校验同创建Deployment
                        创建DaemonSet-容器配置-高级设置，数据存储-切换类型为主机路径，校验同创建Deployment
                        创建DaemonSet-容器配置-高级设置，数据存储-切换类型为ConfigMap，校验同创建Deployment
                        创建DaemonSet-容器配置-高级设置，数据存储-切换类型为Secret，校验同创建Deployment
                        创建DaemonSet-容器配置-高级设置，生命周期钩子-校验同创建Deployment
                        创建DaemonSet-容器配置-高级设置，安全上下文-校验同创建Deployment
                        创建DaemonSet-容器配置-添加多个容器配置，校验同创建Deployment
                        创建DaemonSet-容器配置-添加完成后直接创建，可创建成功
                        创建DaemonSet-访问方式-Service，校验同创建Deployment中创建Service
                        创建DaemonSet-访问方式-切换Ingress，校验规则与创建Deployment时相同
                    DaemonSet管理
                        DaemonSet详情-点击进入详情，查看基本信息展示
                        DaemonSet详情-基本信息，pod数量，不可编辑
                        DaemonSet详情-基本信息，点击编辑DaemonSet，展开编辑弹窗，查看已配置信息展示
                        DaemonSet详情-基本信息，编辑DaemonSet，名称及名字空间不可编辑
                        DaemonSet详情-基本信息，编辑DaemonSet，基本信息其他编辑项校验同创建
                        DaemonSet详情-基本信息，编辑DaemonSet，容器配置其他编辑项校验同创建
                        DaemonSet详情-基本信息，编辑DaemonSet，访问方式编辑项校验同创建
                        DaemonSet详情-基本信息，编辑DaemonSet，修改参数后保存，可修改成功，根据升级策略不同滚动或手动更新后生效
                        DaemonSet详情-基本信息，编辑DaemonSet，从编辑页面切换YAML，查看参数配置
                        DaemonSet详情-基本信息，编辑DaemonSet，从编辑页面切换YAML，修改yaml参数保存，可修改成功
                        DaemonSet详情-基本信息，编辑DaemonSet，从编辑页面切换YAML，修改后切换回表单，yaml修改不保留
                        DaemonSet详情-基本信息，morebutton查看可操作按钮
                        DaemonSet详情-基本信息，morebutton点击编辑YAML，展示原始yaml信息，可编辑及保存yaml生效
                        DaemonSet详情-基本信息，morebutton点击下载YAML，下载成功，yaml文件正常可读
                        DaemonSet详情-基本信息，morebutton点击重新部署，提交成功，根据升级策略执行部署
                        DaemonSet详情-基本信息，点击morebutton删除 - 查看删除弹窗，选择删除或取消
                        DaemonSet详情-基本信息，morebutton点击删除，提交成功，资源本身及pod被删除
                        DaemonSet列表-morebutton查看可操作按钮调整
                        DaemonSet详情-基本信息，点击编辑升级策略，展开编辑弹窗，显示配置信息
                        DaemonSet详情-基本信息，编辑滚动更新升级策略，修改maxUnavailable参数配置，可保存成功，参数生效
                        DaemonSet详情-基本信息，编辑滚动更新升级策略，升级策略切换为手动删除更新，可保存成功，参数生效，信息展示更新
                        DaemonSet详情-基本信息，编辑手动更新升级策略，切换为滚动更新并配置参数，可保存成功，参数生效，展示信息更新
                        DaemonSet详情-Pod列表，默认折叠展示，交互同Deployment详情
                        DaemonSet详情-Pod列表，可点打开pod控制台并操作
                        DaemonSet详情-Pod列表，可点打开查看pod监控信息
                        DaemonSet详情-Pod列表，可点打开查看pod实时日志
                        DaemonSet详情-Pod列表，可点打开查看pod实时事件
                        DaemonSet详情-Pod列表，可点击morebutton上传文件、下载文件
                        DaemonSet详情-Pod列表，可点击morebutton直接删除pod，删除后滚动更新
                        DaemonSet详情-点击展开Pod详情，基本信息展示正确，交互同Deployment详情
                        DaemonSet详情-Pod详情，默认展示折叠容器列表，显示信息正确，交互同Deployment详情
                        DaemonSet详情-Pod详情，点击展开容器详情，显示正确的配置信息，交互同Deployment详情
                        DaemonSet详情-Pod详情，容器详情-生命周期，展示正确信息，校验同Deployment详情
                        DaemonSet详情-Pod详情，容器详情-环境变量，展示正确信息，校验同Deployment详情
                        DaemonSet详情-Pod详情，容器详情-健康检查，展示正确信息，校验同Deployment详情
                        DaemonSet详情-Pod详情，容器详情-ConfigMap，展示正确信息，校验同Deployment详情
                        DaemonSet详情-Pod详情，容器详情-Secret，展示正确信息，校验同Deployment详情
                        DaemonSet详情-Pod详情，容器详情-数据存储，校验同Deployment详情
                        DaemonSet详情-Pod详情，容器详情-安全上下文，展示正确信息，校验同Deployment详情
                        DaemonSet详情-Pod详情-调度策略，展示正确信息，校验同Deployment详情
                        DaemonSet详情-Pod详情-容忍，展示正确信息，校验同Deployment详情
                        DaemonSet详情-Pod详情-网络，展示正确信息，校验同Deployment详情
                        DaemonSet详情-Pod详情-安全上下文，展示正确信息，校验同Deployment详情
                        DaemonSet详情-Pod详情-状况，展示正确信息，校验同Deployment详情
                        DaemonSet详情-Pod详情-标签与注解，展示正确信息，校验同Deployment详情
                        DaemonSet详情-访问方式，展示正确信息，校验同Deployment详情
                        DaemonSet详情-历史版本，展示正确信息，校验同Deployment详情
                        DaemonSet详情-历史版本，点击提交回滚版本，根据升级策略选择生效模式
                        DaemonSet详情-监控，展示正确信息，校验同Deployment详情
                        DaemonSet详情-事件，展示正确信息，校验同Deployment详情
                        DaemonSet详情-状况，展示正确信息，校验同Deployment详情
                        DaemonSet详情-标签与注解，展示正确信息，校验同Deployment详情
                Pod
                    创建Pod
                        创建Pod - 打开创建弹窗，默认展示
                        创建Pod - 基本信息，名称-必填项校验：请填写名称
                        创建Pod - 基本信息，名称-字符数量限制：名称支持的字符长度范围为1-253
                        创建Pod - 基本信息，名称-特殊字符开头结尾：仅支持小写字母、数字、连字符和点，并且必须以小写字母或数字开头和结尾
                        创建Pod - 基本信息，名称-重名规则，统一名字空间不允许重名：名称已存在
                        创建Pod - 基本信息，名字空间-可选择或点击创建，校验规则同创建Deployment
                        创建Pod - 基本信息，高级设置-镜像拉取秘钥，可选择或自助创建，校验规则同创建Deployment中pod配置
                        创建Pod - 基本信息，高级设置-镜像拉取秘钥，选择已存在秘钥，可拉取到镜像
                        创建Pod - 基本信息，高级设置-镜像拉取秘钥，选择创建自定义秘钥，可拉取到镜像
                        创建Pod - 基本信息，高级设置-重启策略，默认选择Always，可切换Never/OnFailure
                        创建Pod - 基本信息，高级设置-调度策略，选项及校验同创建Deployment中pod配置
                        创建Pod - 基本信息，高级设置-容忍，选项及校验同创建Deployment中pod配置
                        创建Pod - 基本信息，高级设置-网络，选项及校验同创建Deployment中pod配置
                        创建Pod - 基本信息，高级设置-安全上下文，选项及校验同创建Deployment中pod配置
                        创建Pod - 基本信息，高级设置-添加标签，选项及校验同创建Deployment中pod配置
                        创建Pod - 基本信息，高级设置-添加注解，选项及校验同创建Deployment中pod配置
                        创建Pod - 容器配置，基本信息 - 可切换容器类型，工作容器/初始化容器
                        创建Pod - 容器配置，基本信息 - 容器名称，校验同创建Deployment中容器配置
                        创建Pod - 容器配置，基本信息 - 容器镜像，校验同创建Deployment中容器配置
                        创建Pod - 容器配置，基本信息 - 镜像版本，选择容器镜像后启用，校验同创建Deployment中容器配置
                        创建Pod - 容器配置，基本信息 - 镜像拉取策略，默认Always，可切换IfNorPresent或Never
                        创建Pod - 容器配置，基本信息 - 启动命令，可配置项及校验同创建Deployment中容器配置
                        创建Pod - 容器配置，基本信息 - 容器配额，可配置项及校验同创建Deployment中容器配置
                        创建Pod - 容器配置，高级设置 - 容器端口，可配置项及校验同创建Deployment中容器配置
                        创建Pod - 容器配置，高级设置 - 环境变量，可配置项及校验同创建Deployment中容器配置
                        创建Pod - 容器配置，高级设置 - 健康检查，可配置项及校验同创建Deployment中容器配置
                        创建Pod - 容器配置，高级设置 - 数据存储，可配置项及校验同创建Deployment中容器配置
                        创建Pod - 容器配置，高级设置 - 生命周期钩子，可配置项及校验同创建Deployment中容器配置
                        创建Pod - 容器配置，高级设置 - 安全上下文，可配置项及校验同创建Deployment中容器配置
                        创建Pod - 容器配置-可添加多个容器配置
                        创建Pod - 切换YAML，可查看当前已配置项，在yaml添加必填项配置后可直接提交创建，创建成功
                        创建Pod - 切换YAML，修改yaml配置，再次切回表单时yaml更改配置不保留
                    Pod管理
                        Pod详情-查看基本信息，展示正确，交互同Deployment详情页Pod
                        Pod详情-root栏点击图标，打开pod控制台，可正常操作
                        Pod详情-root栏点击图标，打开pod监控，弹窗展示当前监控数据，metrics及交互同1.5pod监控
                        Pod详情-root栏点击图标，打开pod监控，当未开启obs监控时，查看展示---TBD
                        Pod详情-root栏点击图标，打开pod日志，弹窗展示当前日志，可实时查看日志信息，交互同1.5
                        Pod详情-root栏点击图标，打开pod事件，弹窗展示当前事件，可实时查看事件信息，交互同1.5
                        Pod详情-隐藏编辑Pod入口，不支持编辑Pod
                        Pod列表-隐藏编辑Pod入口，不支持编辑Pod
                        Pod详情-点击morebutton查看可操作项
                        Pod列表-点击morebutton查看可操作项更新
                        Pod详情-点击morebutton编辑YAML，展示原始yaml信息，可编辑及保存yaml生效
                        Pod详情-点击morebutton下载YAML，可下载成功，YAML正确可读
                        Pod详情-点击morebutton上传文件，可上传文件成功
                        Pod详情-点击morebutton下载文件，可下载pod文件成功
                        Pod详情-默认展示折叠容器列表，显示信息正确，同Deployment详情
                        Pod详情-点击展开容器详情，显示正确的配置信息，交互同Deployment详情
                        Pod详情-容器详情-编辑容器镜像，编辑成功，查看效果
                        Pod详情-容器详情-编辑镜像拉取策略，编辑成功，查看效果
                        Pod详情-容器详情-容器镜像，点击可粘贴容器镜像url，粘贴正确
                        Pod详情-容器详情-生命周期，展示正确信息，校验同Deployment详情
                        Pod详情-容器详情-环境变量，展示正确信息，校验同Deployment详情
                        Pod详情-容器详情-健康检查，展示正确信息，校验同Deployment详情
                        Pod详情-容器详情-ConfigMap，展示正确信息，校验同Deployment详情
                        Pod详情-容器详情-Secret，展示正确信息，校验同Deployment详情
                        Pod详情-容器详情-数据存储，校验同Deployment详情
                        Pod详情-容器详情-安全上下文，展示正确信息，校验同Deployment详情
                        Pod详情-调度策略，节点调度策略-根据节点名称选择节点，展示节点信息，不可编辑
                        Pod详情-调度策略，节点调度策略-其余类型调度策略展示，同Deployment详情
                        Pod详情-调度策略，Pod调度策略-调度策略展示，同Deployment详情
                        Pod详情-容忍，展示正确信息，校验同Deployment详情
                        Pod详情-网络，展示正确信息，校验同Deployment详情
                        Pod详情-安全上下文，展示正确信息，校验同Deployment详情
                        Pod详情-状况，展示正确信息，校验同Deployment详情
                        Pod详情-标签与注解，展示正确信息，校验同Deployment详情
                CronJob
                    创建CronJob
                        创建CronJob-打开创建弹窗，查看基本信息展示
                        创建CronJob -基本信息-工作负载配置-名称，为空提示：请填写名称
                        创建CronJob -基本信息-工作负载配置-名称，数量限制：名称支持的字符长度范围为1-52
                        创建CronJob -基本信息-工作负载配置-名称，特殊字符：仅支持小写字母、数字和连字符，并且必须以小写字母或数字开头和结尾
                        创建CronJob -基本信息-工作负载配置-名称，同名字空间不允许重名：名称已存在
                        创建CronJob -基本信息-工作负载配置-名字空间，可选择或创建，校验同创建Deployment
                        创建CronJob -基本信息-工作负载配置-并发策略，默认选择Allow，可切换Forbid或Replace
                        创建CronJob -基本信息-工作负载配置-暂停调度，默认关闭，可点击开启
                        创建CronJob -基本信息-工作负载配置-定时规则，默认选中「小时」，默认为1分钟
                        创建CronJob -基本信息-工作负载配置-定时规则，默认选中「小时」，分钟输入框范围：0-59，超过报错
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「日」，默认为用户点击时「此刻」的时间
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「日」，修改时间交互
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「日」，删除时间为空时，展示placeholder「请选择时间」
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「周」，默认为「星期一」，时间为用户点击的「此刻」
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「周」，可修改周期以及时间
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「周」，删除时间为空，展示placeholder「请选择时间」
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「月」，默认为每月的「1」号，时间为用户点击的「此刻」
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「月」，可修改日期以及时间
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「月」，日期范围1-31，超过报错
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「月」，删除时间为空，展示placeholder「请选择时间」
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「自定义」，默认Cron表达式，展示为当前时刻
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「自定义」，表达式格式错误：Cron表达式格式错误
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「自定义」，清空表达式，placeholder提示格式示意
                        创建CronJob -基本信息-工作负载配置-定时规则，切换「自定义」，提交时为空报错：请填写Cron表达式
                        创建CronJob -基本信息-工作负载配置-成功任务保留数量，默认值为3，选填项
                        创建CronJob -基本信息-工作负载配置-成功任务保留数量，仅允许输入阿拉伯数字
                        创建CronJob -基本信息-工作负载配置-成功任务保留数量，需输入正整数：仅支持大于等于1的整数
                        创建CronJob -基本信息-工作负载配置-失败任务保留数量，默认值为1，选填项
                        创建CronJob -基本信息-工作负载配置-失败任务保留数量，仅允许输入阿拉伯数字
                        创建CronJob -基本信息-工作负载配置-失败任务保留数量，需输入正整数：仅支持大于等于1的整数
                        创建CronJob -基本信息-工作负载配置-延迟开始期限，默认不设置，单位为秒，选填项
                        创建CronJob -基本信息-工作负载配置-延迟开始期限，仅允许输入阿拉伯数字
                        创建CronJob -基本信息-工作负载配置-延迟开始期限，需输入非负整数：仅支持大于等于0的整数
                        创建CronJob -基本信息-工作负载配置-添加标签，校验同创建Deployment
                        创建CronJob -基本信息-工作负载配置-添加注解，校验同创建Deployment
                        创建CronJob -基本信息，可选择不切换其他配置，点击下一步配置容器
                        创建CronJob -基本信息，切换Job配置，查看默认展示配置项
                        创建CronJob -基本信息-Job配置-并发Pod数，默认值为1
                        创建CronJob -基本信息-Job配置-并发Pod数，仅允许输入阿拉伯数字
                        创建CronJob -基本信息-Job配置-并发Pod数，需输入正整数：仅支持大于等于1的整数
                        创建CronJob -基本信息-Job配置-目标完成数量，默认值3
                        创建CronJob -基本信息-Job配置-目标完成数量，仅允许输入阿拉伯数字
                        创建CronJob -基本信息-Job配置-目标完成数量，需输入非负整数：仅支持大于等于0的整数
                        创建CronJob -基本信息-Job配置-超时时间，默认不设置，单位秒
                        创建CronJob -基本信息-Job配置-超时时间，仅允许输入阿拉伯数字
                        创建CronJob -基本信息-Job配置-超时时间，需输入非负整数：仅支持大于等于0的整数
                        创建CronJob -基本信息-Job配置-重试次数，默认值6
                        创建CronJob -基本信息-Job配置-重试次数，仅允许输入阿拉伯数字
                        创建CronJob -基本信息-Job配置-重试次数，需输入非负整数：仅支持大于等于0的整数
                        创建CronJob -基本信息-Job配置-完成后存活时间，默认不设置，单位秒
                        创建CronJob -基本信息-Job配置-完成后存活时间，仅允许输入阿拉伯数字
                        创建CronJob -基本信息-Job配置-完成后存活时间，需输入非负整数：仅支持大于等于0的整数
                        创建CronJob -基本信息-Job配置-添加标签，校验同创建Deployment
                        创建CronJob -基本信息-Job配置-添加注解，校验同创建Deployment
                        创建CronJob -基本信息，切换Pod配置，查看默认展示配置项
                        创建CronJob -基本信息-Pod配置-重启策略，默认选择Never，可选择切换OnFailure
                        创建CronJob -基本信息-Pod配置-镜像拉取秘钥，校验同创建Deployment中Pod配置
                        创建CronJob -基本信息-Pod配置-调度策略，校验同创建Deployment中Pod配置
                        创建CronJob -基本信息-Pod配置-容忍，校验同创建Deployment中Pod配置
                        创建CronJob -基本信息-Pod配置-网络，校验同创建Deployment中Pod配置
                        创建CronJob -基本信息-Pod配置-安全上下文，校验同创建Deployment中Pod配置
                        创建CronJob -基本信息-Pod配置-标签/注解，校验同创建Deployment中Pod配置
                        创建CronJob -容器配置-配置项同校验创建Deployment
                        创建CronJob - 容器配置，基本信息 - 可切换容器类型，工作容器/初始化容器
                        创建CronJob - 容器配置，基本信息 - 容器名称，校验同创建Deployment中容器配置
                        创建CronJob - 容器配置，基本信息 - 容器镜像，校验同创建Deployment中容器配置
                        创建CronJob - 容器配置，基本信息 - 镜像版本，选择容器镜像后启用，校验同创建Deployment中容器配置
                        创建CronJob - 容器配置，基本信息 - 镜像拉取策略，默认Always，可切换IfNorPresent或Never
                        创建CronJob - 容器配置，基本信息 - 启动命令，可配置项及校验同创建Deployment中容器配置
                        创建CronJob - 容器配置，基本信息 - 容器配额，可配置项及校验同创建Deployment中容器配置
                        创建CronJob - 容器配置，高级设置 - 容器端口，可配置项及校验同创建Deployment中容器配置
                        创建CronJob - 容器配置，高级设置 - 环境变量，可配置项及校验同创建Deployment中容器配置
                        创建CronJob - 容器配置，高级设置 - 健康检查，可配置项及校验同创建Deployment中容器配置
                        创建CronJob - 容器配置，高级设置 - 数据存储，可配置项及校验同创建Deployment中容器配置
                        创建CronJob - 容器配置，高级设置 - 生命周期钩子，可配置项及校验同创建Deployment中容器配置
                        创建CronJob - 容器配置，高级设置 - 安全上下文，可配置项及校验同创建Deployment中容器配置
                        创建CronJob - 容器配置-可添加多个容器配置
                        创建CronJob - 切换YAML，可查看当前已配置项，在yaml添加必填项配置后可直接提交创建，创建成功
                        创建CronJob - 切换YAML，修改yaml配置，再次切回表单时yaml更改配置不保留
                    CronJob管理
                        CronJob详情-基本信息-查看展示内容
                        CronJob详情-基本信息-点击编辑CronJob打开编辑弹窗，名字及名字空间不可编辑，其他配置项同创建CronJob
                        CronJob详情-基本信息-编辑CronJob，修改参数后保存，查看配置更新
                        CronJob详情-基本信息-点击morebutton查看可操作按钮
                        CronJob列表-点击morebutton查看可操作按钮更新
                        CronJob详情-基本信息-点击morebutton编辑YAML，展示原始yaml信息，可编辑及保存yaml生效
                        CronJob详情-基本信息-点击morebutton下载YAML，下载成功，yaml文件正常可读
                        CronJob详情-基本信息-点击morebutton暂停，暂停按钮更新为恢复，cronjob暂停成功
                        CronJob详情-基本信息-点击morebutton恢复，按钮更新为暂停，cronjob恢复调度
                        CronJob详情-基本信息-点击morebutton删除，删除cronjob资源及其下关联job和pod
                        CronJob详情-基本信息-定时规则，展示为Cron表达式，与创建时配置规则转换后表达式一致
                        CronJob详情-基本信息-Job数量，hover时tooltip展示「完成数量/全部数量」，与Job展示数量及状态一致
                        CronJob详情-基本信息-上次调度时间，hover展示绝对时间，与最新完成的Job创建时间一致
                        CronJob详情-基本信息-其他配置，与创建时配置内容一致
                        CronJob详情-Job-默认展示，均折叠展示，根据创建时间倒序排列，查看样式
                        CronJob详情-Job-点击展开Job，查看展示信息
                        CronJob详情-Job-点击查看morebutton可操作按钮
                        CronJob详情-Job-点击morebutton重启Job，重启成功，重新创建并执行新的Job
                        CronJob详情-Job-点击查看morebutton删除Job，删除成功，删除其下Pod
                        CronJob详情-Job-Pod列表，默认折叠展示，交互同Deployment详情
                        CronJob详情-Job-Pod列表，可点打开pod控制台并操作，仅运行中pod
                        CronJob详情-Job-Pod列表，可点打开查看pod监控信息
                        CronJob详情-Job-Pod列表，可点打开查看pod实时日志
                        CronJob详情-Job-Pod列表，可点打开查看pod实时事件
                        CronJob详情-Job-Pod列表，可点击morebutton上传文件、下载文件，仅运行中pod
                        CronJob详情-Job-Pod列表，可点击morebutton直接删除pod，已完成pod删除后移除列表
                        CronJob详情-Job-点击展开Pod详情，基本信息展示正确，交互同Deployment详情
                        CronJob详情-Job-Pod详情，默认展示折叠容器列表，显示信息正确，交互同Deployment详情
                        CronJob详情-Job-Pod详情，点击展开容器详情，显示正确的配置信息，交互同Deployment详情
                        CronJob详情-Job-Pod详情，容器详情-编辑容器镜像，编辑成功，查看效果
                        CronJob详情-Job-Pod详情，容器详情-编辑镜像拉取策略，编辑成功，查看效果
                        CronJob详情-Job-Pod详情，容器详情-容器镜像，点击可粘贴容器镜像url，粘贴正确
                        CronJob详情-Job-Pod详情，容器详情-生命周期，展示正确信息，校验同Deployment详情
                        CronJob详情-Job-Pod详情，容器详情-环境变量，展示正确信息，校验同Deployment详情
                        CronJob详情-Job-Pod详情，容器详情-健康检查，展示正确信息，校验同Deployment详情
                        CronJob详情-Job-Pod详情，容器详情-ConfigMap，展示正确信息，校验同Deployment详情
                        CronJob详情-Job-Pod详情，容器详情-Secret，展示正确信息，校验同Deployment详情
                        CronJob详情-Job-Pod详情，容器详情-数据存储，校验同Deployment详情
                        CronJob详情-Job-Pod详情，容器详情-安全上下文，展示正确信息，校验同Deployment详情
                        CronJob详情-Job-Pod详情-调度策略，展示正确信息，校验同Deployment详情
                        CronJob详情-Job-Pod详情-容忍，展示正确信息，校验同Deployment详情
                        CronJob详情-Job-Pod详情-网络，展示正确信息，校验同Deployment详情
                        CronJob详情-Job-Pod详情-安全上下文，展示正确信息，校验同Deployment详情
                        CronJob详情-Job-Pod详情-状况，展示正确信息，校验同Deployment详情
                        CronJob详情-Job-Pod详情-标签与注解，展示正确信息，校验同Deployment详情
                        CronJob详情-Job-事件，展示实时事件，校验同Deployment详情
                        CronJob详情-Job-状况，展示实时状况，校验同Deployment详情
                        CronJob详情-Job-标签与注解，展示正确信息，校验同Deployment详情
                        CronJob详情-事件，展示CronJob实时事件，列表同Deployment详情
                        CronJob详情-标签与注解，展示CronJob标签与注解，正确展示，同Deployment详情
                Job
                    创建Job
                        创建Job-打开创建弹窗，查看基本信息展示
                        创建Job -基本信息-工作负载配置-名称，为空提示：请填写名称
                        创建Job -基本信息-工作负载配置-名称，数量限制：名称支持的字符长度范围为1-63
                        创建Job -基本信息-工作负载配置-名称，特殊字符：仅支持小写字母、数字和连字符，并且必须以小写字母或数字开头和结尾
                        创建Job -基本信息-工作负载配置-名称，同名字空间不允许重名：名称已存在
                        创建Job -基本信息-工作负载配置-名字空间，可选择或创建，校验同创建Deployment
                        创建Job -基本信息-并发Pod数，默认值为1
                        创建Job -基本信息-并发Pod数，仅允许输入阿拉伯数字
                        创建Job -基本信息-并发Pod数，需输入正整数：仅支持大于等于1的整数
                        创建Job -基本信息-目标完成数量，默认值3
                        创建Job -基本信息-目标完成数量，仅允许输入阿拉伯数字
                        创建Job -基本信息-目标完成数量，需输入非负整数：仅支持大于等于0的整数
                        创建Job -基本信息-超时时间，默认不设置，单位秒
                        创建Job -基本信息-超时时间，仅允许输入阿拉伯数字
                        创建Job -基本信息-超时时间，需输入非负整数：仅支持大于等于0的整数
                        创建Job -基本信息-重试次数，默认值6
                        创建Job -基本信息-重试次数，仅允许输入阿拉伯数字
                        创建Job -基本信息-重试次数，需输入非负整数：仅支持大于等于0的整数
                        创建Job -基本信息-完成后存活时间，默认不设置，单位秒
                        创建Job -基本信息-完成后存活时间，仅允许输入阿拉伯数字
                        创建Job -基本信息-完成后存活时间，需输入非负整数：仅支持大于等于0的整数
                        创建Job -基本信息-添加标签，校验同创建Deployment
                        创建Job -基本信息-添加注解，校验同创建Deployment
                        创建Job -基本信息，切换Pod配置，查看默认展示配置项
                        创建Job -基本信息-Pod配置-镜像拉取秘钥，校验同创建Deployment中Pod配置
                        创建Job -基本信息-Pod配置-重启策略，默认选择Never，可选择切换OnFailure
                        创建Job -基本信息-Pod配置-调度策略，校验同创建Deployment中Pod配置
                        创建Job -基本信息-Pod配置-容忍，校验同创建Deployment中Pod配置
                        创建Job -基本信息-Pod配置-网络，校验同创建Deployment中Pod配置
                        创建Job -基本信息-Pod配置-安全上下文，校验同创建Deployment中Pod配置
                        创建Job -基本信息-Pod配置-状况，校验同创建Deployment中Pod配置
                        创建Job -基本信息-Pod配置-标签/注解，校验同创建Deployment中Pod配置
                        创建Job -容器配置-配置项同校验创建Deployment
                        创建Job - 容器配置，基本信息 - 可切换容器类型，工作容器/初始化容器
                        创建Job - 容器配置，基本信息 - 容器名称，校验同创建Deployment中容器配置
                        创建Job - 容器配置，基本信息 - 容器镜像，校验同创建Deployment中容器配置
                        创建Job - 容器配置，基本信息 - 镜像版本，选择容器镜像后启用，校验同创建Deployment中容器配置
                        创建Job - 容器配置，基本信息 - 镜像拉取策略，默认Always，可切换IfNorPresent或Never
                        创建Job - 容器配置，基本信息 - 启动命令，可配置项及校验同创建Deployment中容器配置
                        创建Job - 容器配置，基本信息 - 容器配额，可配置项及校验同创建Deployment中容器配置
                        创建Job - 容器配置，高级设置 - 容器端口，可配置项及校验同创建Deployment中容器配置
                        创建Job - 容器配置，高级设置 - 环境变量，可配置项及校验同创建Deployment中容器配置
                        创建Job - 容器配置，高级设置 - 监控检查，可配置项及校验同创建Deployment中容器配置
                        创建Job - 容器配置，高级设置 - 数据存储，可配置项及校验同创建Deployment中容器配置
                        创建Job - 容器配置，高级设置 - 生命周期钩子，可配置项及校验同创建Deployment中容器配置
                        创建Job - 容器配置，高级设置 - 安全上下文，可配置项及校验同创建Deployment中容器配置
                        创建Job - 容器配置-可添加多个容器配置
                        创建Job - 切换YAML，可查看当前已配置项，在yaml添加必填项配置后可直接提交创建，创建成功
                        创建Job - 切换YAML，修改yaml配置，再次切回表单时yaml更改配置不保留
                    Job管理
                        Job详情-基本信息-查看展示内容
                        Job详情-基本信息-点击编辑Job打开编辑弹窗，名字及名字空间不可编辑，其他配置项同创建Job
                        Job详情-基本信息-编辑Job，修改参数后保存，查看配置更新
                        Job详情-基本信息-其他配置，与创建时配置内容一致
                        Job详情-基本信息-点击morebutton查看可操作按钮
                        Job列表-点击morebutton查看可操作按钮更新，「编辑」改为「编辑Job」
                        Job详情-基本信息-点击morebutton编辑YAML，展示原始yaml信息，可编辑及保存yaml生效
                        Job详情-基本信息-点击morebutton下载YAML，下载成功，yaml文件正常可读
                        Job详情-点击morebutton重启Job，重启成功，重新创建并执行Job
                        Job详情-点击查看morebutton删除Job，删除成功，删除其下Pod
                        Job详情-Pod列表，默认折叠展示，交互同Deployment详情
                        Job详情-Pod列表，可点打开pod控制台并操作，仅运行中pod
                        Job详情-Pod列表，可点打开查看pod监控信息
                        Job详情-Pod列表，可点打开查看pod实时日志
                        Job详情-Pod列表，可点打开查看pod实时事件
                        Job详情-Pod列表，可点击morebutton上传文件、下载文件，仅运行中pod
                        Job详情-Pod列表，可点击morebutton直接删除pod，已完成pod删除后移除列表
                        Job详情-点击展开Pod详情，基本信息展示正确，交互同Deployment详情
                        Job详情-Pod，默认展示折叠容器列表，显示信息正确，交互同Deployment详情
                        Job详情-Pod，点击展开容器详情，显示正确的配置信息，交互同Deployment详情
                        Job详情-Pod，容器详情-编辑容器镜像，编辑成功，查看效果
                        Job详情-Pod，容器详情-编辑镜像拉取策略，编辑成功，查看效果
                        Job详情-Pod，容器详情-容器镜像，点击可粘贴容器镜像url，粘贴正确
                        Job详情-Pod，容器详情-生命周期，展示正确信息，校验同Deployment详情
                        Job详情-Pod，容器详情-环境变量，展示正确信息，校验同Deployment详情
                        Job详情-Pod，容器详情-健康检查，展示正确信息，校验同Deployment详情
                        Job详情-Pod，容器详情-ConfigMap，展示正确信息，校验同Deployment详情
                        Job详情-Pod，容器详情-Secret，展示正确信息，校验同Deployment详情
                        Job详情-Pod，容器详情-数据存储，校验同Deployment详情
                        Job详情-Pod，容器详情-安全上下文，展示正确信息，校验同Deployment详情
                        Job详情-Pod-调度策略，展示正确信息，校验同Deployment详情
                        Job详情-Pod-容忍，展示正确信息，校验同Deployment详情
                        Job详情-Pod-网络，展示正确信息，校验同Deployment详情
                        Job详情-Pod-安全上下文，展示正确信息，校验同Deployment详情
                        Job详情-Pod-状况，展示正确信息，校验同Deployment详情
                        Job详情-Pod-标签与注解，展示正确信息，校验同Deployment详情
                        Job详情-事件，展示实时事件，校验同Deployment详情
                        Job详情-状况，展示实时状况，校验同Deployment详情
                        Job详情-标签与注解，展示正确信息，校验同Deployment详情
            服务访问
                Service
                    创建Service
                        创建Service -打开创建弹窗，查看基本信息展示
                        创建Service - 基本信息 - 名称，为空校验：请填写名称
                        创建Service - 基本信息 - 名称，字符数限制：名称支持的字符长度范围为1-63
                        创建Service - 基本信息 - 名称，字符开头结尾：仅支持小写字母、数字和连字符，并且必须以小写字母或数字开头和结尾
                        创建Service - 基本信息 - 名称，同一名字空间内不允许重名：名称已存在
                        创建Service - 基本信息 - 名字空间，为空校验：请选择名字空间
                        创建Service - 基本信息 - 名字空间，选择器展示，支持搜索已存在的ns
                        创建Service - 基本信息 - 名字空间，租户视角，仅展示所属项目下的ns
                        创建Service - 基本信息 - 名字空间，选择器内创建名字空间按钮，租户无该权限时不展示创建
                        创建Service - 基本信息 - 名字空间，创建名字空间，弹窗校验同单独创建弹窗
                        创建Service - 基本信息 - 名字空间，管理员用户关联项目，可选择不关联
                        创建Service - 基本信息 - 名字空间，创建名字空间后自动回填入配置项
                        创建Service - 基本信息 - 类型，默认选项为ClusterIP，可下拉切换NodeIP或LoadBalancer
                        创建Service - 基本信息 - 类型，选择ClusterIP时，下方展示Headless Service配置项，默认关闭，可点击开启，选择其他类型时不展示
                        创建Service - 基本信息 - 类型，选择ClusterIP，开启Headless Service，再切换其他类型，开关隐藏
                        创建Service - 基本信息 - Pod 选择算符，键为空校验：请填写键
                        创建Service - 基本信息 - Pod 选择算符，键值格式校验：格式错误，popover查看格式要求
                        创建Service - 基本信息 - Pod 选择算符，添加多组标签，可支持移除
                        创建Service - 基本信息 - Pod 选择算符，指定工作负载，点击按钮popover展示指定工作负载弹窗
                        创建Service - 基本信息 - Pod 选择算符，指定工作负载弹窗，类型默认为Deployment，点击可切换StatefulSet和DaemonSet
                        创建Service - 基本信息 - Pod 选择算符，指定工作负载弹窗，未选择工作负载时添加按钮禁用，选择工作负载后可点击
                        创建Service - 基本信息 - Pod 选择算符，指定工作负载弹窗，点击选择工作负载展示已有可选工作负载列表
                        创建Service - 基本信息 - Pod 选择算符，指定工作负载弹窗，租户仅展示同项目内可以选工作负载
                        创建Service - 基本信息 - Pod 选择算符，指定工作负载弹窗，选择类型和工作负载后点击添加，自动回填展示该匹配该工作负载的所有标签选择器
                        创建Service - 基本信息 - Pod 选择算符，从指定工作负载添加的工作负载标签，可进行二次编辑
                        创建Service - 基本信息 - 端口配置，默认展示配置项，为必填项
                        创建Service - 基本信息 - 端口配置，可添加多个端口，支持移除
                        创建Service - 基本信息 - 端口配置，协议默认为TCP，可切换UDP
                        创建Service - 基本信息 - 端口配置，名称长度限制：名称支持的字符长度范围为1-63
                        创建Service - 基本信息 - 端口配置，名称字符限制：仅支持小写字母、数字和连字符，并且必须以小写字母或数字开头和结尾
                        创建Service - 基本信息 - 端口配置，名称同一Service内，不允许重名：名称已存在
                        创建Service - 基本信息 - 端口配置，名称，单个端口时，可允许为空，hover时展示tooltip："端口数量为 1 时，名称为选填项；大于 1 时，名称为必填项。"
                        创建Service - 基本信息 - 端口配置，名称选填，当添加多个端口时，名称必填-后端返回报错
                        创建Service - 基本信息 - 端口配置，服务端口/容器端口 - 不允许为空：请填写服务端口/容器端口
                        创建Service - 基本信息 - 端口配置，服务端口 - 数值范围：仅支持1-65535之间的整数
                        创建Service - 基本信息 - 端口配置，容器端口 - 数值范围：仅支持 1-65535 之间的整数或字符串。
                        创建Service - 基本信息 - 端口配置，仅当NodePort和LoadBalancer类型时展示「节点端口」，其他类型不展示
                        创建Service - 基本信息 - 端口配置，节点端口 - 默认为自动生成，可切换指定端口
                        创建Service - 基本信息 - 端口配置，节点端口 - 指定端口时，检查是否为空：请填写指定端口
                        创建Service - 基本信息 - 端口配置，节点端口 - 指定端口时，检查端口冲突：端口已被占用
                        创建Service - 基本信息 - 端口配置，节点端口 - 指定端口时，数值范围：仅支持30000-32767之间的整数
                        创建Service - 高级设置 - 默认收起，可选择不配置，点击展开配置项
                        创建Service - 高级设置 - 会话保持，默认关闭，点击开关开启，展示配置项
                        创建Service - 高级设置 - 会话保持，最大会话保持时间，默认10800秒
                        创建Service - 高级设置 - 会话保持，最大会话保持时间，为空校验：请填写最大会话保持时间
                        创建Service - 高级设置 - 会话保持，最大会话保持时间，数值范围：仅支持1-86400之间的整数
                        创建Service - 高级设置 - 类型为NodePort或LoadBalancer时，展示外部流量策略配置项，其余类型不展示
                        创建Service - 高级设置 - 外部流量策略，默认选择Cluster，可切换Local
                        创建Service - 高级设置 - 标签 - 点击添加标签 - 键/值格式校验，popover查看格式要求
                        创建Service - 高级设置 - 标签 - 点击添加标签 - 键不允许为空
                        创建Service - 高级设置 - 标签 - 点击添加标签 - 可添加多个标签，支持移除
                        创建Service - 高级设置 - 注解 - 点击添加注解 - 键/值格式校验，popover查看格式要求
                        创建Service - 高级设置 - 注解 - 点击添加注解 - 键不允许为空
                        创建Service - 高级设置 - 注解 - 点击添加注解 - 可添加多个注解，支持移除
                        创建Service - 基本信息- 配置后切换YAML，可查看yaml中当前配置项已写入，且参数格式正确
                        创建Service - 基本信息- 切换至YAML后修改配置，可直接从yaml编辑配置提交创建，参数生效
                        创建Service - 基本信息- 切换至YAML后修改配置，再次切换回表单时不保留yaml修改内容，但表单配置保留，无变化
                        创建Service - 基本信息- 切换至YAML后再切回表单，有编辑表单弹窗提示
                    Service管理
                        Service列表入口-「服务与网络」修改为「服务访问」
                        Service列表调整-「端口映射」更改为「服务端口->容器端口/协议」
                        Service列表morebutton调整-「编辑」修改为「编辑Service」
                        Service详情-点击列表名称进入详情，查看详情展示
                        Service详情-基本信息，Pod选择算符-独立整行展示，以标签样式
                        Service详情-点击编辑Service，展示编辑Service页面，名称和名字空间不可编辑，其余配置与创建Service相同
                        Service详情-编辑Service，修改配置信息后保存，可编辑成功，配置更新
                        Service详情-点击morebutton查看可操作项
                        Service详情-点击morebutton下载YAML，可下载成功，yaml文件正常可读
                        Service详情-点击morebutton删除，service删除成功，退出详情，列表删除
                        Service详情-基本信息，外部流量策略-当Service类型为LoadBalancer或NodePort时，显示字段，其他类型时隐藏该字段
                        Service详情-端口，查看端口列表信息调整，对比1.5
                        Service详情-Pod，展示Pod列表，字段同Pod列表展示
                        Service详情-监控，展示service监控数据，同1.5
                        Service详情-事件，展示事件信息，service一般为空状态
                        Service详情-状况，展示为空，同1.5
                        Service详情-标签与注解，展示信息同Deployment详情
                        Service-搜索-支持根据名称进行搜索
                        Service-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
                        Service-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
                        Service-选择名字空间过滤后，搜索列表，可根据搜索字段及名字空间检索列表
                Ingress
                    创建Ingress
                        创建Ingress -打开创建弹窗，查看基本信息展示
                        创建Ingress - 基本信息 - 名称，为空校验：请填写名称
                        创建Ingress - 基本信息 - 名称，字符数限制：名称支持的字符长度范围为1-63
                        创建Ingress - 基本信息 - 名称，字符开头结尾：仅支持小写字母、数字和连字符，并且必须以小写字母或数字开头和结尾
                        创建Ingress - 基本信息 - 名称，同一名字空间内不允许重名：名称已存在
                        创建Ingress - 基本信息 - 名字空间，为空校验：请选择名字空间
                        创建Ingress - 基本信息 - 名字空间，选择器展示，支持搜索已存在的ns
                        创建Ingress - 基本信息 - 名字空间，租户视角，仅展示所属项目下的ns
                        创建Ingress - 基本信息 - 名字空间，选择器内创建名字空间按钮，租户无该权限时不展示创建
                        创建Ingress - 基本信息 - 名字空间，创建名字空间，弹窗校验同单独创建弹窗
                        创建Ingress - 基本信息 - 名字空间，管理员用户关联项目，可选择不关联
                        创建Ingress - 基本信息 - 名字空间，创建名字空间后自动回填入配置项
                        创建Ingress - 基本信息 - IngressClass，为选填项，可不选择
                        创建Ingress - 基本信息 - IngressClass，若未创建IngressClass，则默认选项为空
                        创建Ingress - 基本信息 - IngressClass，已创建IngressClass，则默认展示，多条时支持切换
                        创建Ingress - 基本信息 - 路由规则，域名为选填项，可不填写
                        创建Ingress - 基本信息 - 路由规则，域名长度限制：名称支持的字符长度范围为1-253
                        创建Ingress - 基本信息 - 路由规则，域名字符限制：仅支持小写字母、数字、连字符和点，并且必须以小写字母或数字开头和结尾
                        创建Ingress - 基本信息 - 路由规则，协议可选择HTTP或HTTPS，默认HTTP
                        创建Ingress - 基本信息 - 路由规则，协议切换HTTPS时，展示Secret选项
                        创建Ingress - 基本信息 - 路由规则，HTTPS协议，Secret必填校验：请选择Secret
                        创建Ingress - 基本信息 - 路由规则，HTTPS协议，Secret可下拉选择已有TLS类型的秘钥，其余类型的Secret不展示
                        创建Ingress - 基本信息 - 路由规则，HTTPS协议，Secret可在下拉框点击创建，创建Secret弹窗校验同单独创建
                        创建Ingress - 基本信息 - 路由规则，HTTPS协议，创建Secret时秘钥类型自动指定为TLS(kubernetes.io/tls)，可修改为其他类型
                        创建Ingress - 基本信息 - 路由规则，HTTPS协议，创建TLS类型Secret后，自动回填选中该秘钥
                        创建Ingress - 基本信息 - 路由规则，转发策略 - 匹配方式，默认为Prefix，可切换Exact或ImplementationSpecific
                        创建Ingress - 基本信息 - 路由规则，转发策略 - 路径为空提示：请填写路径
                        创建Ingress - 基本信息 - 路由规则，转发策略 - 路径格式：请以“/”开头
                        创建Ingress - 基本信息 - 路由规则，转发策略 - 目标服务为空提示：请选择目标服务
                        创建Ingress - 基本信息 - 路由规则，转发策略 - 目标服务，可下拉选择已有匹配的Service，选择后自动更新目标服务端口
                        创建Ingress - 基本信息 - 路由规则，转发策略 - 目标服务，选择已有Service，service端口有name时，自动填写name，没有name则填入port
                        创建Ingress - 基本信息 - 路由规则，转发策略 - 目标服务端口，选择Service后自动填充对应目前服务端口，可进行修改
                        创建Ingress - 基本信息 - 路由规则，转发策略 - 目标服务端口，为空提示：请填写目标服务端口
                        创建Ingress - 基本信息 - 路由规则，转发策略 - 目标服务端口，格式校验：仅支持1-65535之间的整数或字符串。
                        创建Ingress - 基本信息 - 路由规则，可添加多个路由规则
                        创建Ingress - 高级设置 - 默认收起，点击可展开配置
                        创建Ingress - 高级设置 - 标签 - 点击添加标签 - 键/值格式校验，popover查看格式要求
                        创建Ingress - 高级设置 - 标签 - 点击添加标签 - 键不允许为空
                        创建Ingress - 高级设置 - 标签 - 点击添加标签 - 可添加多个标签，支持移除
                        创建Ingress - 高级设置 - 注解 - 点击添加注解 - 键/值格式校验，popover查看格式要求
                        创建Ingress - 高级设置 - 注解 - 点击添加注解 - 键不允许为空
                        创建Ingress - 高级设置 - 注解 - 点击添加注解 - 可添加多个注解，支持移除
                        创建Ingress - 基本信息- 配置后切换YAML，可查看yaml中当前配置项已写入，且参数格式正确
                        创建Ingress - 基本信息- 切换至YAML后修改配置，可直接从yaml编辑配置提交创建，参数生效
                        创建Ingress - 基本信息- 切换至YAML后修改配置，再次切换回表单时不保留yaml修改内容，但表单配置保留，无变化
                        创建Ingress - 基本信息- 切换至YAML后再切回表单，有编辑表单弹窗提示
                    Ingress管理
                        Ingress列表入口-「服务与网络」修改为「服务访问」
                        Ingress列表展示-「规则」列内容展示方式调整
                        Ingress列表morebutton调整-「编辑」修改为「编辑Ingress」
                        Ingress详情-点击列表名称进入详情，查看详情展示
                        Ingress详情-点击编辑Ingress，展示编辑Ingress页面，名称和名字空间不可编辑，其余配置与创建Ingress相同
                        Ingress详情-编辑Ingress，修改配置信息后保存，可编辑成功，配置更新
                        Ingress详情-点击morebutton查看可操作项
                        Ingress详情-点击morebutton下载YAML，可下载成功，yaml文件正常可读
                        Ingress详情-点击morebutton删除，Ingress删除成功，退出详情，列表删除
                        Ingress详情-规则，查看字段标题调整，其余同1.5
                        Ingress详情-Service，展示关联service，列表展示同Service列表，不支持操作
                        Ingress详情-事件，展示事件，展示Ingress实时事件，一般为无，与Deployment详情一致
                        Ingress详情-标签与注解，展示信息同Deployment详情
                        Ingress-搜索-支持根据名称进行搜索
                        Ingress-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
                        Ingress-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
                        Ingress-选择名字空间过滤后，搜索列表，可根据搜索字段及名字空间检索列表
                IngressClass
                    创建IngressClass
                        支持从导入Yaml创建IngressClass
                        从导入Yaml创建IngressClass，创建后查看列表更新及展示
                        创建IngressClass-点击打开创建Ingress弹窗，展示yaml配置框，提供基本字段示例
                        创建IngressClass-修改示例配置内容后点击创建，可创建成功，展示在列表
                        创建IngressClass-粘贴自定义配置文件，点击创建，可创建成功，展示在列表
                        创建IngressClass-修改示例配置内容后点击重置，可恢复初始化配置
                        创建IngressClass-修改示例配置内容后点击查看改动，展示改动内容
                        创建IngressClass-创建后可在创建Ingress时选择
                    IngressClass管理
                        IngressClass列表入口-「服务访问」主菜单，Ingress子菜单下同级
                        IngressClass列表-查看IngressClass表格字段展示及交互
                        IngressClass列表-默认IngressClass，点击morebutton查看可操作项
                        IngressClass列表-默认IngressClass，点击morebutton取消默认，toast %IngressClass名称%取消默认成功/失败
                        IngressClass列表-默认IngressClass，点击morebutton取消默认成功，列表默认IngressClass更新为「否」，morebutton中按钮更新为「设为默认」
                        IngressClass列表-非默认IngressClass，当不存在默认IngressClass时，点击morebutton展示为「设为默认」，按钮可点击
                        IngressClass列表-非默认IngressClass，当已存在默认IngressClass时，点击morebutton展示为「设为默认」，按钮禁用
                        IngressClass列表-非默认IngressClass，当不存在默认IngressClass时，morebutton点击「设为默认」，toast%IngressClass名称%设为默认成功/失败
                        IngressClass列表-非默认IngressClass，当不存在默认IngressClass时，morebutton点击「设为默认」，按钮更新为「取消默认」
                        IngressClass列表-仅允许设置一个默认IngressClass
                        IngressClass列表-点击morebutton编辑YAML，展开YAML配置框，修改后保存成功
                        IngressClass列表-点击morebutton删除，展开删除IngressClass弹窗，确认删除后列表删除
                        IngressClass详情-点击列表名称进入详情查看具体信息
                        IngressClass详情-Controller，名称-展示完整名称
                        IngressClass详情-Controller，类型-可取值：NodePort、LoadBalancer、ClusterIP
                        IngressClass详情-Controller，名字空间-点击可跳转名字空间详情
                        IngressClass详情-Controller，Service-展示servce名称，点击可跳转service详情
                        IngressClass详情-Controller，Service-相关联数据面 service 展示正确
                        IngressClass详情-Controller，集群外访问地址-格式：IP：端口
                        IngressClass详情-Controller，集群外访问地址-可以有多个值，多个时每个独立行展示，单行过长打点展示
                        IngressClass详情-Controller，服务端口-格式：服务端口->容器端口/协议
                        IngressClass详情-Controller，服务端口-可以有多个值，多个时每个独立行展示，单行过长打点展示
                        IngressClass详情-点击编辑YAML，打开编辑弹窗，可编辑成功
                        IngressClass详情-点击morebutton下载YAML，可下载成功，yaml可读
                        IngressClass详情-点击morebutton取消默认，取消成功/失败
                        IngressClass详情-点击morebutton设为默认，设置成功/失败
                        IngressClass详情-点击morebutton删除，退出详情，列表删除
                        IngressClass-搜索-支持根据名称进行搜索
                        IngressClass-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
                        IngressClass-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
                        IngressClass-过滤-IngressClass为全局资源，不受ns过滤影响，可正常展示
            配置
                ConfigMap
                    创建ConfigMap
                        创建ConfigMap-打开创建弹窗，基本信息展示
                        创建ConfigMap-基本信息，名称-为空提示：请填写名称
                        创建ConfigMap-基本信息，名称-字符数限制：名称支持的字符长度范围为1-253
                        创建ConfigMap-基本信息，名称-特殊字符：仅支持小写字母、数字、连字符和点，并且必须以小写字母或数字开头和结尾
                        创建ConfigMap-基本信息，名称-同一名字空间不允许重名：名称已存在
                        创建ConfigMap - 基本信息，名字空间-为空校验：请选择名字空间
                        创建ConfigMap - 基本信息，名字空间-选择器展示，支持搜索已存在的ns
                        创建ConfigMap - 基本信息，名字空间-租户视角，仅展示所属项目下的ns
                        创建ConfigMap - 基本信息，名字空间-选择器内创建名字空间按钮，租户无该权限时不展示创建
                        创建ConfigMap - 基本信息，名字空间-创建名字空间，弹窗校验同单独创建弹窗
                        创建ConfigMap - 基本信息，名字空间-管理员用户关联项目，可选择不关联
                        创建ConfigMap - 基本信息，名字空间-创建名字空间后自动回填入配置项
                        创建ConfigMap - 基本信息，数据/二进制数据-可同时不填写，保存成功
                        创建ConfigMap - 基本信息，数据/二进制数据-可同时添加或添加其中一个，可保存成功
                        创建ConfigMap - 基本信息，数据-默认展开一个键/值配置，当输入「值」后，「键」为必填项，无「值」时，单独「键」可保存成功
                        创建ConfigMap - 基本信息，数据-键值对，可添加多个，支持移除
                        创建ConfigMap - 基本信息，数据-键值格式：同其他键值
                        创建ConfigMap - 基本信息，数据-值，可输入长格式值，无溢出，无格式错误，保存后能够正确展示
                        创建ConfigMap - 基本信息，数据-键值对，输入多行文本/配置文件类型，保存后可正确展示及应用
                        创建ConfigMap - 基本信息，数据-键值对，输入JSON/XML 配置文件类型，保存后可正确展示及应用
                        创建ConfigMap - 基本信息，数据-键值对，输入环境变量配置类型，保存后可正确展示及应用
                        创建ConfigMap - 基本信息，数据-键值对，输入命令行参数配置，保存后可正确展示及应用
                        创建ConfigMap - 基本信息，二进制数据-添加二进制数据，可正常配置，保存后可正确展示及应用
                        创建ConfigMap - 基本信息，数据-同时添加数据和二进制数据，可正常配置，保存后可正确展示及应用
                        创建ConfigMap - 基本信息，数据-点击从文件读取，文件格式，任意
                        创建ConfigMap - 基本信息，数据-点击从文件读取，可正确解析文件名及文件内容，自动识别填充至键和值的位置
                        创建ConfigMap - 基本信息，二进制数据-点击从文件读取，可正确解析文件名及文件内容，自动识别填充至键和值的位置
                        创建ConfigMap - 高级设置 - 默认折叠，点击展开高级配置
                        创建ConfigMap - 高级设置 - 标签 - 点击添加标签 - 键/值格式校验，popover查看格式要求
                        创建ConfigMap - 高级设置 - 标签 - 点击添加标签 - 键不允许为空
                        创建ConfigMap - 高级设置 - 标签 - 点击添加标签 - 可添加多个标签，支持移除
                        创建ConfigMap - 高级设置 - 注解 - 点击添加注解 - 键/值格式校验，popover查看格式要求
                        创建ConfigMap - 高级设置 - 注解 - 点击添加注解 - 键不允许为空
                        创建ConfigMap - 高级设置 - 注解 - 点击添加注解 - 可添加多个注解，支持移除
                        创建ConfigMap - 基本信息- 配置后切换YAML，可查看yaml中当前配置项已写入，且参数格式正确
                        创建ConfigMap - 基本信息- 切换至YAML后修改配置，可直接从yaml编辑配置提交创建，参数生效
                        创建ConfigMap - 基本信息- 切换至YAML后修改配置，再次切换回表单时不保留yaml修改内容，但表单配置保留，无变化
                        创建ConfigMap - 基本信息- 切换至YAML后再切回表单，有编辑表单弹窗提示
                    ConfigMap管理
                        ConfigMap列表 - 入口及列表字段值不变
                        ConfigMap列表 - 点击列表morebutton，「编辑」按钮更新为「编辑ConfigMap」
                        ConfigMap详情 - 点击列表名称进去详情，查看详情展示
                        ConfigMap详情 - 点击编辑ConfigMap，展示编辑页面，名称和名字空间不可编辑，其余配置与创建ConfigMap相同
                        ConfigMap详情-编辑ConfigMap，修改配置信息后保存，可编辑成功，配置更新
                        ConfigMap详情-点击morebutton查看可操作项「下载YAML」「删除」
                        ConfigMap详情-点击morebutton下载YAML，可下载成功，yaml文件正常可读
                        ConfigMap详情-点击morebutton删除，ConfigMap删除成功，退出详情，列表删除
                        ConfigMap详情-数据，key/value形式多行展示，展示样式与1.5一致
                        ConfigMap详情-关联资源，以列表形式展示，展示容器列表
                        ConfigMap详情-标签与注解，展示信息与Deployment详情-标签与注解一致
                        ConfigMap-搜索-支持根据名称进行搜索
                        ConfigMap-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
                        ConfigMap-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
                        ConfigMap-选择名字空间过滤后，搜索列表，可根据搜索字段及名字空间检索列表
                Secret
                    创建Secret
                        创建Secret-打开创建弹窗，基本信息展示
                        创建Secret-基本信息，名称-为空提示：请填写名称
                        创建Secret-基本信息，名称-字符数限制：名称支持的字符长度范围为1-253
                        创建Secret-基本信息，名称-特殊字符：仅支持小写字母、数字、连字符和点，并且必须以小写字母或数字开头和结尾
                        创建Secret-基本信息，名称-同一名字空间不允许重名：名称已存在
                        创建Secret - 基本信息，名字空间-为空校验：请选择名字空间
                        创建Secret - 基本信息，名字空间-选择器展示，支持搜索已存在的ns
                        创建Secret - 基本信息，名字空间-租户视角，仅展示所属项目下的ns
                        创建Secret - 基本信息，名字空间-选择器内创建名字空间按钮，租户无该权限时不展示创建
                        创建Secret - 基本信息，名字空间-创建名字空间，弹窗校验同单独创建弹窗
                        创建Secret - 基本信息，名字空间-管理员用户关联项目，可选择不关联
                        创建Secret - 基本信息，名字空间-创建名字空间后自动回填入配置项
                        创建Secret - 基本信息，类型-默认项为「Opaque」，可切换为「镜像仓库凭证」「TLS」「用户名和密码」
                        创建Secret - 基本信息，类型-Opaque，配置「数据」，查看默认展示
                        创建Secret - 基本信息，类型-Opaque，「数据」可选填，选择不输入任何数据
                        创建Secret - 基本信息，类型-Opaque，数据-展开一个键/值配置，当输入「值」后，「键」为必填项
                        创建Secret - 基本信息，类型-Opaque，数据-键值对，可添加多个，支持移除
                        创建Secret - 基本信息，类型-Opaque，数据-值，可输入长格式值，无溢出，无格式错误，保存后能够正确展示
                        创建Secret - 基本信息，类型-Opaque，数据-键格式：与其他相同
                        创建Secret - 基本信息，类型-Opaque，数据-点击从文件读取，可正确解析文件名及文件内容，自动识别填充至键和值的位置
                        创建Secret - 基本信息，类型-Opaque，数据-可创建成功，yaml中解析正确，可正常使用
                        创建Secret - 基本信息，类型-镜像仓库凭证，切换后展示需配置内容：「仓库地址」「用户名」「密码」
                        创建Secret - 基本信息，类型-镜像仓库凭证，仓库地址-为空提示：请填写仓库地址
                        创建Secret - 基本信息，类型-镜像仓库凭证，仓库地址-提示文案：支持输入 IP 地址或完整的 HTTP(S) 地址。
                        创建Secret - 基本信息，类型-镜像仓库凭证，仓库地址-输入IP或http/https协议的url，错误提示隐藏
                        创建Secret - 基本信息，类型-镜像仓库凭证，用户名-为空提示：请填写用户名
                        创建Secret - 基本信息，类型-镜像仓库凭证，密码-为空提示：请填写密码
                        创建Secret - 基本信息，类型-镜像仓库凭证，密码-默认输入为加密模式，可切换明文
                        创建Secret - 基本信息，类型-镜像仓库凭证-可创建成功，yaml中解析正确，可正常使用
                        创建Secret - 基本信息，类型-TLS，切换后展示需配置内容：「证书」「私钥」
                        创建Secret - 基本信息，类型-TLS，证书-为空提示：请填写证书
                        创建Secret - 基本信息，类型-TLS，证书-支持输入及粘贴，过长时自动撑开，展示格式正确，支持PEM编码
                        创建Secret - 基本信息，类型-TLS，证书-从文件读取，解析正常，自动填充后格式正确
                        创建Secret - 基本信息，类型-TLS，私钥-为空提示：请填写私钥
                        创建Secret - 基本信息，类型-TLS，私钥-支持输入及粘贴，过长时自动撑开，展示格式正确，支持PEM编码
                        创建Secret - 基本信息，类型-TLS，私钥-从文件读取，解析正常，自动填充后格式正确
                        创建Secret - 基本信息，类型-TLS-可创建成功，yaml中解析正确，可正常使用
                        创建Secret - 基本信息，类型-用户名和密码，切换后展示需配置内容：「用户名」「密码」
                        创建Secret - 基本信息，类型-用户名和密码，用户名-为空提示：请填写用户名
                        创建Secret - 基本信息，类型-用户名和密码，密码-为空提示：请填写密码
                        创建Secret - 基本信息，类型-用户名和密码，密码-默认输入为加密模式，可切换明文
                        创建Secret - 基本信息，类型-用户名和密码-可创建成功，yaml中解析正确，可正常使用
                        创建Secret - 高级设置 - 默认折叠，点击展开高级配置
                        创建Secret - 高级设置 - 标签 - 点击添加标签 - 键/值格式校验，popover查看格式要求
                        创建Secret - 高级设置 - 标签 - 点击添加标签 - 键不允许为空
                        创建Secret - 高级设置 - 标签 - 点击添加标签 - 可添加多个标签，支持移除
                        创建Secret - 高级设置 - 注解 - 点击添加注解 - 键/值格式校验，popover查看格式要求
                        创建Secret - 高级设置 - 注解 - 点击添加注解 - 键不允许为空
                        创建Secret - 高级设置 - 注解 - 点击添加注解 - 可添加多个注解，支持移除
                        创建Secret - 基本信息- 配置后切换YAML，可查看yaml中当前配置项已写入，且参数格式正确
                        创建Secret - 基本信息- 切换至YAML后修改配置，可直接从yaml编辑配置提交创建，参数生效
                        创建Secret - 基本信息- 切换至YAML后修改配置，再次切换回表单时不保留yaml修改内容，但表单配置保留，无变化
                        创建Secret - 基本信息- 切换至YAML后再切回表单，有编辑表单弹窗提示
                    Secret管理
                        Secret列表 - 入口及列表字段值不变
                        Secret列表 - 点击列表morebutton，「编辑」按钮更新为「编辑Secret」
                        Secret详情 - 点击列表名称进去详情，查看详情展示
                        Secret详情 - 点击编辑Secret，展示编辑页面，名称和名字空间不可编辑，其余配置与创建Secret相同
                        Secret详情-编辑Secret，修改配置信息后保存，可编辑成功，配置更新
                        Secret详情-点击morebutton查看可操作项「下载YAML」「删除」
                        Secret详情-点击morebutton下载YAML，可下载成功，yaml文件正常可读
                        Secret详情-点击morebutton删除，Secret删除成功，退出详情，列表删除
                        Secret详情-数据，key/value形式多行展示，默认隐藏数值，点击可显示数值，展示样式与1.5一致
                        Secret详情-关联资源，以列表形式展示，展示容器列表
                        Secret详情-标签与注解，展示信息与Deployment详情-标签与注解一致
                        Secret详情 - 查看创建deployment时自动创建的镜像仓库凭证（kubernetes.io/dockerconfigjson）
                        Secret详情 - 查看Opaque类型的凭证
                        Secret详情 - 查看创建deployment时手动创建的凭证（kubernetes.io/dockerconfigjson）
                        Secret详情 - 查看TLS（kubernetes.io/tls）类型的凭证
                        Secret详情 - 查看用户名和密码（kubernetes.io/basic-auth）类型的凭证
                        Secret-搜索-支持根据名称进行搜索
                        Secret-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
                        Secret-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
                        Secret-选择名字空间过滤后，搜索列表，可根据搜索字段及名字空间检索列表
            存储
                持久卷
                    持久卷列表-展示列表及字段不变，同1.5
                    创建持久卷-创建弹窗及形式不变，yaml形式创建
                    持久卷详情-点击列表名称进入，查看默认展示，基本信息展示优化，信息不变
                    持久卷详情-Volume，ELF CSI类型的卷，查看详情展示
                    持久卷详情-Volume，ELF CSI类型的卷，详情-名称，点击跳转至虚拟卷详情，详情展示正确
                    持久卷详情-Volume，ELF CSI类型的卷，详情-UUID，获取子虚拟卷UUID，展示一致
                    持久卷详情-Volume，ELF CSI类型的卷，详情-操作系统设备名，从「虚拟卷-详情-客户机操作系统设备名」获取，展示一致
                    持久卷详情-Volume，ELF CSI类型的卷，详情-挂载点，从「虚拟机详情-文件系统分区-挂载点路径」获取，展示一致（6.x以上elf集群）
                    持久卷详情-Volume，ELF CSI类型的卷，详情-冗余策略，从「虚拟卷详情-存储策略-冗余策略」获取，展示一致
                    持久卷详情-Volume，ELF CSI类型的卷，详情-置备方式，从「虚拟卷详情-存储策略-置备方式」获取，展示一致
                    持久卷详情-Volume，ELF CSI类型的卷，详情-分配容量，hover tooltip：分配给虚拟卷的逻辑容量
                    持久卷详情-Volume，ELF CSI类型的卷，详情-已使用容量，hover tooltip：已使用逻辑容量
                    持久卷详情-Volume，ELF CSI类型的卷，详情-分配容量，与虚拟卷详情分配容量一致
                    持久卷详情-Volume，ELF CSI类型的卷，详情-已使用容量，与虚拟卷详情已使用容量一致
                    持久卷详情-Volume，ZBS CSI类型的卷，查看详情展示
                    持久卷详情-Volume，ZBS CSI类型的卷，详情-名称，点击跳转至LUN详情，详情展示正确
                    持久卷详情-Volume，ZBS CSI类型的卷，详情-冗余策略，从「LUN详情-存储策略-冗余策略」获取，展示一致
                    持久卷详情-Volume，ZBS CSI类型的卷，详情-置备方式，从「LUN详情-存储策略-置备方式」获取，展示一致
                    持久卷详情-Volume，ZBS CSI类型的卷，详情-分配容量，与LUN详情分配容量一致
                    持久卷详情-Volume，ZBS CSI类型的卷，详情-已使用容量，与LUN详情分配容量一致
                    持久卷详情-事件，展示事件，展示持久卷变更触发的实时事件，与Deployment详情样式一致
                    持久卷详情-标签与注解，展示信息同Deployment详情
                    持久卷详情-租户页面不展示详情
                    持久卷-搜索-支持根据名称进行搜索
                    持久卷-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
                    持久卷-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
                持久卷申领
                    持久卷申领列表-展示列表及字段不变，同1.5
                    创建持久卷申领-创建弹窗及表单模式不变，表单宽度调整为648px
                    持久卷申领详情-点击列表名称进入，查看默认展示，基本信息展示优化
                    持久卷申领详情-基本信息，资源用量-单独展示一行数据，查看展示样式
                    持久卷申领详情-基本信息，资源用量-资源加载中时展示
                    持久卷申领详情-基本信息，资源用量-资源加载失败时展示
                    持久卷申领详情-基本信息，资源用量-监控功能未开启时展示
                    持久卷申领详情-基本信息，资源用量-监控功能开启但无数据时展示
                    持久卷申领详情-持久卷，展示持久卷详情信息
                    持久卷申领详情-持久卷，点击展开，展示持久卷下Volume信息，与持久卷中Volume信息一致
                    持久卷申领详情-持久卷，查看ELF CSI对应的持久卷详情信息
                    持久卷申领详情-持久卷，查看ZBS CSI对应的持久卷详情信息
                    持久卷申领详情-关联资源，展示持久卷申领所关联的工作负载列表
                    持久卷申领详情-关联资源，当单独创建pvc未关联工作负载时，展示为空
                    持久卷申领详情-监控，展示内容同1.5
                    持久卷申领详情-事件，展示实时触发的事件，同1.5
                    持久卷申领详情-状况，展示pvc状况，列表同Deployment详情状况
                    持久卷申领详情-标签与注解，展示列表同Deployment详情状况
                    持久卷申领-搜索-支持根据名称进行搜索
                    持久卷申领-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
                    持久卷申领-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
                    持久卷申领-选择名字空间过滤后，搜索列表，可根据搜索字段及名字空间检索列表
                存储类
                    存储类列表-展示列表及字段不变，同1.5
                    创建存储类-创建弹窗及表单模式不变，表单宽度调整为648px
                    存储类详情-点击列表进入详情，查了详情展示信息
                    存储类详情-持久卷申领，展示列表信息，同1.5
                    存储类详情-标签与注解，展示信息同Deployment详情标签与注解
                    存储类-搜索-支持根据名称进行搜索
                    存储类-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
                    存储类-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
                    存储类-选择名字空间过滤后，搜索列表，可根据搜索字段及名字空间检索列表
            网络
                NetworkPolicy
                    NetworkPolicy-入口切换，从原「服务与网络」切换为新导航「网络」
                    NetworkPolicy列表-列表信息展示，同1.5
                    NetworkPolicy详情-点击列表进入详情，查看详情布局更新
                    NetworkPolicy详情-pod选择算符，展示形式同Service选择算符
                    NetworkPolicy详情-Ingress规则，展示from配置，YAML显示框自适应规则
                    NetworkPolicy详情-Egress规则，展示to配置，YAML显示框自适应规则同Ingress
                    NetworkPolicy详情-标签与注解，展示同Deployment详情标签与注解
                    NetworkPolicy-搜索-支持根据名称进行搜索
                    NetworkPolicy-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
                    NetworkPolicy-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
                    NetworkPolicy-选择名字空间过滤后，搜索列表，可根据搜索字段及名字空间检索列表
            自定义资源
                自定义资源列表-从「自定义资源」一级菜单点击进入自定义资源列表，默认展示
                自定义资源列表-列表字段信息及交互
                自定义资源列表-搜索栏展示，默认搜索类型「名称」，支持切换为「组」或「类型」
                自定义资源列表-搜索「名称」，根据名称字段模糊匹配，给出列表结果域搜索一致
                自定义资源列表-搜索「名称」，当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
                自定义资源列表-搜索「组」，根据组模糊匹配，给出列表结果域搜索一致
                自定义资源列表-搜索「组」，当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
                自定义资源列表-搜索「类型」，根据类型字段模糊匹配，给出列表结果域搜索一致
                自定义资源列表-搜索「类型」，当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
                自定义资源列表-搜索，输入搜索字段筛选列表，从结果列表点击进入详情，再返回时搜索条件及结果依旧保留
                自定义资源列表-搜索，输入搜索字段筛选列表，切换搜索类型，清空搜索条件，恢复全部列表
                自定义资源列表-搜索，输入搜索字段筛选列表，从搜索框清空，恢复全部列表
                自定义资源列表-morebutton，点击编辑YAML，弹窗展示完整yaml内容，弹窗交互同其他yaml弹窗
                自定义资源列表-morebutton，点击编辑YAML，修改配置内容保存，保存成功，配置更新
                自定义资源列表-morebutton，点击删除，展示删除自定义资源弹窗
                自定义资源列表-morebutton，点击删除，确认删除后退出弹窗，删除CRD成功，其下CR一并删除成功
                创建自定义资源-从导入YAML直接创建
                创建自定义资源-停留在自定义资源列表，点击「导入YAML」创建自定义资源，创建成功后退出弹窗，自定义资源列表新增创建的资源
                自定义资源详情-点击列表名称进入详情，查看详情信息展示
                自定义资源详情-自定义资源，展示CRD下CR资源列表及搜索框
                自定义资源详情-自定义资源，列表字段定义及交互
                自定义资源详情-自定义资源，搜索-支持根据资源名称进行搜索
                自定义资源详情-自定义资源，搜索-根据名称字段模糊匹配，给出列表结果域搜索一致
                自定义资源详情-自定义资源，搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
                自定义资源详情-自定义资源，morebutton，点击编辑YAML，弹出编辑CR的yaml弹窗，展示完整yaml配置
                自定义资源详情-自定义资源，morebutton，点击编辑YAML，修改配置保存，退出弹窗，资源更新
                自定义资源详情-自定义资源，morebutton，删除，弹出删除CR资源弹窗
                自定义资源详情-自定义资源，morebutton，删除，确认删除后，从列表移除
                自定义资源详情-点击编辑YAML，弹窗展示完整yaml内容，弹窗交互同其他yaml弹窗
                自定义资源详情-点击编辑YAML，修改配置内容保存，保存成功，配置更新
                自定义资源详情-点击morebutton删除，弹出删除自定义资源弹窗，展示同列表删除
                自定义资源详情-点击morebutton删除，确认删除后退出详情，自定义资源从列表移除，相关CR删除
                自定义资源-查看创建工作集群后，默认创建的自定义资源列表及详情
                自定义资源-查看工作集群开启全部插件后，自动创建的自定义资源列表及详情
                自定义资源-查看工作集群自动创建的自定义资源详情中，所属CR的增加、更新和清理
        集群资源搜索
            节点列表-搜索-支持根据节点名称进行搜索
            节点列表-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
            节点列表-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
            名字空间-搜索-支持根据ns名称进行搜索
            名字空间-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
            名字空间-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
            项目-搜索-支持根据项目名称进行搜索
            项目-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
            项目-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
            成员-搜索-支持根据成员名称进行搜索
            成员-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
            成员-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
            角色-搜索-支持根据角色名称进行搜索
            角色-搜索-输入名称字段模糊匹配，给出列表结果域搜索一致
            角色-搜索-当无搜索结果时，展示「无搜索结果」，可点击「清空搜索条件」，清空后恢复全部列表
        其他改动
            导入YAML弹窗- 选择名字空间，菜单根据「项目名称」标题分类
            导入YAML弹窗- 选择名字空间，菜单新增创建名字空间按钮
            导入YAML弹窗- 选择名字空间，菜单点击创建名字空间，弹窗校验同创建名字空间
            导入YAML弹窗- 选择名字空间，创建名字空间后自动填充至选择框
            导入YAML弹窗- 选择名字空间，选择后可选择移除名字空间重新选择
            导入YAML弹窗- 选择名字空间，选择后导入yaml功能不变，与1.5一致
            导入YAML弹窗-租户页面，选择名字空间，仅有所属项目内名字空间，其余一致
            导入YAML - 使用yaml导入创建的资源，编辑表单，编辑后配置生效，不会丢失
            导入YAML - 创建的表单资源，使用yaml修改资源
            表单不支持字段，在下载yaml中查看原始配置，可以正常展示
            工作负载资源-Volumemount参数下配置，可支持的展示完全，未支持的字段，在yaml中可查看完整展示
            创建名字空间 - 创建时可选择关联已有项目，不包括System项目
        OIDC
            容器镜像仓库和工作负载集群使用者
                tower角色-列表新增-「容器镜像仓库和工作负载集群使用者」角色
                tower角色-容器镜像仓库和工作负载集群使用者」角色详情-操作权限-在容器镜像仓库和工作负载集群中自定义配置
                tower用户 - 创建用户，角色可选择「容器镜像仓库和工作负载集群使用者」角色
                SKS-项目管理-成员，同步用户后，可添加「容器镜像仓库和工作负载集群使用者」角色的用户为成员，并关联项目
                登陆二合一租户-默认展工作集群使用者页面，与单独「工作集群使用者」角色的用户，无区别，有项目权限的才可看到
                登陆二合一租户-操作工作集群使用者详情页面，与单独「工作集群使用者」角色的用户，无区别，有权限的才可查看和操作
                登陆二合一租户-可通过一级导航，切换「容器镜像仓库」页面，一级导航仅展示「Kubernetes服务」和「容器镜像仓库」
                登陆二合一租户-切换「容器镜像仓库」页面，可查看到用户容器镜像仓库列表，不可查看详情及创建、编辑、删除等权限
                登陆二合一租户-在创建Deployment等资源时，可获取到用户容器镜像仓库的中有权限的项目镜像列表
                登陆二合一租户-不拥有其他无权限资源的api权限
                登陆二合一租户-不拥有其他无权限资源的tower api权限
            容器镜像仓库
                admin用户-创建容器镜像仓库，SKS后台可实时watch进度
                admin用户-创建成功容器镜像仓库，登陆registry查看用户管理，能正确同步tower已有用户（本地及LDAP）
                admin用户-使用域名创建容器镜像仓库，可创建成功，用户同步正常
                admin用户-删除registry，SKS后台同步删除
                admin用户-删除registry，删除后使用同一IP创建新regsitry，可创建成功，状态正常，同步用户正常
                regsitry-登陆，原admin账号可正常登录，可查看用户管理用户同步正常
                registry-登陆，通过OIDC登录，使用本地用户，无邮箱，可登录OIDC
                registry-登陆，通过OIDC登录，使用LDAP户登录，可登录成功
                管理员权限的用户OIDC登录-可看到全部权限，同admin账户页面
                tower用户权限 - 运维管理员用户OIDC-管理员权限
                tower用户权限 - 只读用户OIDC-无管理员权限
                tower用户权限 - 安全审计员OIDC-无管理员权限
                tower用户权限 - 用户管理员OIDC-无管理员权限
                tower用户权限 - 虚拟机使用者OIDC-无管理员权限
                tower用户权限 - 工作集群使用者OIDC-无管理员权限
                tower用户权限 - 容器镜像仓库和工作集群使用者OIDC-无管理员权限
                无管理员权限的用户-登录后权限，可查看有权限的项目及镜像
                无管理员权限的用户-登录后权限，可创建自己的项目及上传镜像
                tower添加用户，管理员登录registry查看用户同步，可立即同步展示新增用户
                tower删除用户，管理员登录registry查看用户同步，可立即同步展示移除用户
                tower将用户设置为管理员，该用户重新登录，可拥有管理员权限
                tower将用户设置为非管理员，该管理员用户重新登录，不具有管理员权限
                registry-与sks-registry区别，user-regsitry中额外运行oidc-client,不会授权OIDC
                registry-不同用户api list，仅可获取有权限的私有项目的镜像
                架构 - x86环境用户registry
                架构 - arrch环境用户registry
                registry-公开仓库，所有用户可访问其内镜像
                registry-私有仓库，创建者，可访问其内镜像
                registry-私有仓库，将用户加入私有仓库成为成员，可访问其内镜像
                registry-私有仓库，非成员不可访问其内镜像
                镜像拉取 - 有仓库项目权限的用户，创建资源时使用secret拉取镜像，可拉取成功
                镜像拉取 - 无仓库项目权限的用户，创建资源时使用相同secret拉取镜像，拉取失败
                镜像拉取 - 将无权限的用户，添加到项目中，创建资源时使用相同secret拉取镜像成功
                镜像拉取 - 将有权限的用户，移除项目，创建资源时使用相同secret拉取镜像失败
                镜像拉取 - 将有权限的用户从tower端删除，创建资源时使用相同secret拉取镜像失败
                镜像拉取 - 已删除的用户，重新创建同名用户，创建资源时使用相同secret拉取镜像失败
                tower创建含特殊字符用户名的用户，regsitry可正常识别及展示
                tower创建含特殊字符用户名的用户，创建secret及拉取镜像正常
                使用租户的密钥进行镜像上传，可上传成功
            升级
                未升级SKS1.6的低版本的user-registry-不支持OIDC，租户无法获取镜像
                user-resgitry升级到SKS1.6支持的版本 - 自动支持OIDC
                升级SKS1.6的sks-resgitry - 不支持OIDC
                user-resgitry升级到SKS1.6支持的版本 - 自动创建secret，创建正确
                user-resgitry升级到SKS1.6支持的版本 - 使用secret拉取镜像，拉取成功
                user-resgitry升级到SKS1.6支持的版本 - 同步用户，可正确同步
                仅升级tower至4.9.0，新增支持oidc的api，旧版本SKS1.5.1展示正常
                仅升级tower至4.9.0，新增支持oidc的api，旧版本SKS1.5.1，能正常创建工作负载资源
                仅升级tower至4.9.0，新增支持oidc的api，user-registry页面正常
                升级tower至4.9.0，SKS和registry升级至1.6.0，oidc功能可正常使用
        场景测试
            升级 - 从SKS1.5升级到SKS1.6，管理员用户，刷新页面，工作集群详情页更新为1.6，点击查看每个页面api返回正常
            升级 - 从SKS1.5升级到SKS1.6，多租户用户，刷新页面，工作集群详情页更新为1.6，点击查看每个有权限的页面api返回正常
            升级 - 升级后管理员创建工作负载资源，使用表单部署，可正常创建，关联资源根据规则交互正确
            升级 - 升级后租户创建工作负载资源，使用表单部署，可正常创建，关联资源根据规则交互正确
            升级 - 升级后管理员编辑已有工作负载资源，可正常编辑
            升级 - 升级后租户编辑已有工作负载资源，可正常编辑
            升级 - 升级后管理员删除已有工作负载资源，可正常编辑
            升级 - 升级后租户删除已有工作负载资源，可正常编辑
            升级 - 升级后创建新的工作负载集群，可正常操作工作负载资源
            全新创建的tower4.9.0 + SKS1.6.0环境，创建工作集群后，可正常操作工作负载资源
            k8s版本 - SKS1.6 - v1.26版本集群，操作工作负载资源
            k8s版本 - SKS1.6 - v1.27版本集群，操作工作负载资源
            k8s版本 - SKS1.6 - v1.28版本集群，操作工作负载资源
            k8s版本 - SKS1.6 - v1.29版本集群，操作工作负载资源
            k8s版本 - SKS1.6 - v1.30版本集群，操作工作负载资源
            x86环境 - SKS1.6 - 工作集群上操作工作负载资源
            arm环境 - SKS1.6 - 工作集群上操作工作负载资源
            物理集群 - SKS1.6 - 操作工作负载资源
            虚拟机集群 - SKS1.6 - 操作工作负载资源
            Calico CNI - SKS1.6 - 操作工作负载资源
            EIC CNI - SKS1.6 - 操作工作负载资源
            ELF CSI - SKS1.6 - 操作工作负载资源
            ZBS CSI - SKS1.6 - 操作工作负载资源
        discard
            Pod详情-morebutton点击编辑Pod，打开编辑pod弹窗，查看展示，交互同创建pod---discard
            Pod详情-morebutton点击编辑Pod，修改配置项保存，可修改成功，pod更新---discard
    适配 Cloudtower HA
        TowerHA - tower 490 不允许部署 SKS 1.6.0之前版本的 SKS
        480
            TowerHA - 480 - x86 tower - Single 模式下，部署 SKS registry，启用 HA 模式的入口被隐藏
            TowerHA - 480 - aarch64 tower - Single 模式下，部署 SKS registry，启用 HA 模式的入口被隐藏
            TowerHA - 480 - oe x86 tower - Single 模式下，部署 SKS registry，启用 HA 模式的入口被隐藏
            TowerHA - 480 - Single 模式下，卸载 SKS，启用 HA 模式的入口重新可见
            TowerHA - 480 - Single 模式升级到 490， 启用 HA 模式的入口可见
            TowerHA - 480 - 启用 HA 模式，一级导航中 SKS 的入口被隐藏
            TowerHA - 480 - 启用 HA 模式，sks-manager deployment 副本数缩为 0
            TowerHA - 480 - 470升级480 - x86 tower - sks registry 已部署，升级后启用 HA 模式的入口不可见
            TowerHA - 480 - 470升级480 - aarch64 tower - sks registry 已部署，升级后启用 HA 模式的入口不可见
            TowerHA - 480 - 470升级480 - oe x86 tower - sks registry 已部署，升级后启用 HA 模式的入口不可见
            TowerHA - 480 - 470升级480 - 仅 sks registry 1.4.1 已部署，升级480后可成功卸载 sks registry
            TowerHA - 480 - 470升级480 - 已部署的 sks registry 安装包转存到 fileserver，数据库记录更新 fileId 信息
            TowerHA - 480 - 470升级480 - sks1.5 已部署，升级480后可卸载 sks1.5
            TowerHA - 480 - 470升级480 - sks1.5 已部署，升级480后可上传节点模板
            TowerHA - 480 - 470升级480 - sks1.5 已部署，升级480后服务关机下线后可以重新正常上线
            TowerHA - 480 - 470升级480 - sks1.5 已部署，升级480后可关联 OBS 并开启管控集群所有插件
            TowerHA - 480 - 470升级480 - sks1.5 已部署，升级480后可解除 OBS 关联
            TowerHA - 480 - 470升级480 - sks1.5 已部署，升级480后可原地更新服务虚拟机
            TowerHA - 480 - 470升级480 - sks1.4 已部署，升级480后可卸载 sks1.4
            TowerHA - 480 - 470升级480 - sks1.4 已部署，升级480后可升级到 sks1.5
            TowerHA - 480 - 470升级480 - 可部署 sks1.5
            TowerHA - 480 - 470升级480 - user registry 已部署，升级后可正常删除
            TowerHA - 480 - 470升级480 - user registry 已部署，升级后可关机下线后重新上线
            TowerHA - 480 - 470升级480 - user registry 安装包已上传，升级后未使用的安装包可删除
            TowerHA - 480 - 470升级480 - 升级后可新上传 user registry 安装包并成功部署 user registry
            TowerHA - 480 - 470升级480 - 升级后，可新上传 user registry 安装包，然后成功删除
            TowerHA - 480 - 470升级480 - 已上传的多个 user registry 安装包转存到 fileserver，数据库记录更新fileId 信息
            TowerHA - 480 - 470升级480 - 可使用之前已上传的 user registry 1.4.1 安装包新部署 user registry
            TowerHA - 480 - 新部署 SKS - sks registry 可成功部署
            TowerHA - 480 - 新部署 SKS - sks registry 部署后，sks registry 安装包存入 fileserver，数据库记录更新 fileId 信息
            TowerHA - 480 - 新部署 SKS - sks1.5 普通模式服务可成功部署
            TowerHA - 480 - 新部署 SKS - sks1.5 服务可成功提升模式
            TowerHA - 480 - 新部署 SKS - sks1.5 高可用模式服务可成功部署
            TowerHA - 480 - 新部署 SKS - sks1.5 服务可成功完成 OBS 关联并开启插件
            TowerHA - 480 - 新部署 SKS - sks1.5 可成功上传同构节点模板
            TowerHA - 480 - 新部署 SKS - sks1.5 可成功上传异构节点模板
            TowerHA - 480 - 新部署 SKS - sks1.5 可原地更新服务虚拟机
            TowerHA - 480 - 新部署 SKS - sks1.5 可成功卸载
            TowerHA - 480 - 新部署 SKS - x86 rocky 可成功部署
            TowerHA - 480 - 新部署 SKS - x86 oe 可成功部署
            TowerHA - 480 - 新部署 SKS - aarch64 oe 可成功部署
            TowerHA - 480 - 新部署 user registry - v1.4.1 安装包可成功上传，新上传的 user registry 安装包存入 fileserver
            TowerHA - 480 - 新部署 user registry - v1.4.1 registry 可部署
            TowerHA - 480 - 新部署 user registry - 部署完成 registry 可成功卸载
            TowerHA - 480 - 新部署 user registry - 卸载后的安装包可成功删除，fileserver 中的安装包可成功删除
            TowerHA - 480HA - 新部署 user registry - v1.4.1 安装包可成功上传，新上传的 user registry 安装包存入 fileserver, 同步至备节点
            TowerHA - 480HA - 新部署 user registry - v1.4.1 registry 可部署
            TowerHA - 480HA - 新部署 user registry - 部署完成 registry 可成功卸载
            TowerHA - 480HA - 新部署 user registry - 卸载后的安装包可成功删除
            TowerHA - 480HA - 新部署 user registry - x86 registry 可成功部署
            TowerHA - 480HA - 新部署 user registry - aarch64 registry 可成功部署
        490
            Single
                470升级490
                    TowerHA - single - 470升级490 - x86 tower - sks registry 1.4.x已部署，升级后启用 HA 模式的入口不可见
                    TowerHA - single - 470升级490 - aarch64 tower - sks registry v1.4.x 已部署，升级后启用 HA 模式的入口不可见
                    TowerHA - single - 470升级490 - oe x86 tower - sks registry v1.4.1 已部署，升级后启用 HA 模式的入口不可见
                    TowerHA - single - 470升级490 - 已部署的 sks registry 安装包转存到 fileserver，数据库记录更新 fileId 信息
                    TowerHA - single - 470带1.5升级490 - 启用 HA UI 不可见
                    TowerHA - single - 470升级490 - sks1.5 已部署，升级490后可卸载 sks1.5
                    TowerHA - single - 470升级490 - sks1.5 已部署，升级490后可上传节点模板
                    TowerHA - single - 470升级490 - sks1.5 已部署，升级490后服务关机下线后可以重新正常上线
                    TowerHA - single - 470升级490 - sks1.5 已部署，升级490后可关联 OBS 并开启管控集群所有插件
                    TowerHA - single - 470升级490 - sks1.5 已部署，升级490后可解除 OBS 关联
                    TowerHA - single - 470升级490 - sks1.5 已部署，升级490后可原地更新工作集群虚拟机
                    TowerHA - single - 470升级490 - sks1.4 已部署，升级490后可卸载 sks1.4
                    TowerHA - single - 470升级490 - sks1.4 已部署，升级490后可升级到 sks1.5 再升级到 sks1.6
                    TowerHA - single - 470升级490 - 可部署 sks1.6
                    TowerHA - single - 470升级490 - user registry 已部署，升级后可正常删除
                    TowerHA - single - 470升级490 - user registry 已部署，升级后可关机下线后重新上线
                    TowerHA - single - 470升级490 - user registry 安装包已上传，升级后未使用的安装包可删除
                    TowerHA - single - 470升级490 - 升级后可新上传 user registry 1.6.0 安装包并成功部署 user registry
                    TowerHA - single - 470升级490 - 升级后，可新上传 user registry 安装包，然后成功删除
                    TowerHA - single - 470升级490 - 已上传的多个 user registry 安装包转存到 fileserver，数据库记录更新fileId 信息
                    TowerHA - single - 470升级490 - 可使用之前已上传的 user registry 1.4.1 安装包新部署 user registry
                480带1.5升级490
                    TowerHA - single - 480带1.5升级490 - 启用 HA UI 不可见
                    TowerHA - single - 480带1.5升级490 - 升级后可上传节点文件
                    TowerHA - single - 480带1.5升级490 - 升级后可提升服务模式
                    TowerHA - single - 480带1.5升级490 - 升级后服务可卸载，卸载后 HA 入口可见
                    TowerHA - single - 480带1.5升级490 - 升级后 sks registry 可升级到 1.6.0
                    TowerHA - single - 480带1.5升级490 - 升级后 sks registry 1.4.1 安装包可成功删除，fileserver 中的安装包可成功删除
                    TowerHA - single - 480带1.5升级490 - 升级后服务可升级到 1.6.0，sks registry 和 sks 服务均升级完成后 HA 入口可见
                新部署
                    TowerHA - single - 新部署 SKS 后，启用 HA UI 可见
                    TowerHA - single - 新部署 SKS - sks registry 可成功部署
                    TowerHA - single - 新部署 SKS - sks registry 部署后，sks registry 安装包存入 fileserver，数据库记录更新 fileId 信息
                    TowerHA - single - 新部署 SKS - sks1.6 部署完成后，sks registry 中 DNS，ntp 配置更新
                    TowerHA - single - 新部署 SKS - sks1.6 普通模式服务可成功部署
                    TowerHA - single - 新部署 SKS - sks1.6 服务可成功提升模式
                    TowerHA - single - 新部署 SKS - sks1.6 高可用模式服务可成功部署
                    TowerHA - single - 新部署 SKS - sks1.6 服务可成功完成 OBS 关联并开启插件
                    TowerHA - single - 新部署 SKS - sks1.6 可成功上传同构节点模板
                    TowerHA - single - 新部署 SKS - sks1.6 可成功上传异构节点模板
                    TowerHA - single - 新部署 SKS - sks1.6 可原地更新服务虚拟机
                    TowerHA - single - 新部署 SKS - sks1.6 可成功卸载
                    TowerHA - single - 新部署 SKS - sks1.6 可完成升级
                    TowerHA - single - 新部署 SKS - sks1.6 x86 rocky 版本可成功部署
                    TowerHA - single - 新部署 SKS - sks1.6 x86 oe 版本可成功部署
                    TowerHA - single - 新部署 SKS - sks1.6 aarch64 oe 版本可成功部署
                    TowerHA - single - 新部署 SKS - sks1.6 x86 tl3 版本可成功部署
                    TowerHA - single - 新部署 SKS - sks1.6 aarch64 tl3 版本可成功部署
                    TowerHA - single - 新部署 user registry - v1.6.0 安装包可成功上传，新上传的 user registry 安装包存入 fileserver
                    TowerHA - single - 新部署 user registry - v1.6.0 registry 可部署
                    TowerHA - single - 新部署 user registry - 部署完成 registry 可成功卸载
                    TowerHA - single - 新部署 user registry - 卸载后的安装包可成功删除，fileserver 中的安装包可成功删除
                    TowerHA - single - 新部署 user registry - x86 rocky registry 可成功部署/卸载
                    TowerHA - single - 新部署 user registry - aarch64 rocky registry 可成功部署/卸载
                    TowerHA - single - 新部署 user registry - x86 tl3 registry 可成功部署/卸载
                    TowerHA - single - 新部署 user registry - aarch64 tl3 registry 可成功部署/卸载
                运维
                    TowerHA - single - 运维 - Tower VM 关机重启后 - SKS 管控集群可正常暂停/恢复
                    TowerHA - single - 运维 - Tower VM 关机重启后 - SKS 可完成节点上传
                    TowerHA - single - 运维 - Tower VM 关机重启后 - sks-fileserver 中内容可正常访问
            HA
                480HA升级490HA
                    TowerHA - HA - 从480HA升级490HA - Tower 主节点 中 sks-manager deployment 副本数恢复为1
                    TowerHA - HA - 从480HA升级490HA - 已部署 user registry，升级后可卸载 user registry
                    TowerHA - HA - 从480HA升级490HA - 已部署 user registry，升级后可正常上下线
                    TowerHA - HA - 从480HA升级490HA - 已上传的 user registry 安装包可删除
                    TowerHA - HA - 从480HA升级490HA - 已上传的 user registry 安装包可部署 user registry
                    TowerHA - HA - 从480HA升级490HA - sks1.6 普通模式服务可成功部署
                    TowerHA - HA - 从480HA升级490HA - sks1.6 服务可成功提升模式
                    TowerHA - HA - 从480HA升级490HA - sks1.6 服务可成功完成 OBS 关联并开启插件
                    TowerHA - HA - 从480HA升级490HA - sks1.6 可成功上传节点文件
                    TowerHA - HA - 从480HA升级490HA - sks1.6 可原地更新服务虚拟机
                    TowerHA - HA - 从480HA升级490HA - sks1.6 可成功卸载
                    TowerHA - HA - 从480HA升级490HA - sks-manager 数据库同步到备节点数据库 - ？？？480HA时有sks-manager的表？
                    TowerHA - HA - 从480HA升级490HA - 部署 480 HA 后主备发生过一次切换，可成功升级到 490 HA
                新部署
                    TowerHA - HA - 新部署 SKS - sks registry 可成功部署，安装包存入 fileserver，主备节点数据库记录 fileId 信息
                    TowerHA - HA - 新部署 SKS - sks1.6 部署完成后，sks registry 中 DNS，ntp 配置更新
                    TowerHA - HA - 新部署 SKS - sks1.6 普通模式服务可成功部署
                    TowerHA - HA - 新部署 SKS - sks1.6 服务可成功提升模式
                    TowerHA - HA - 新部署 SKS - sks1.6 高可用模式服务可成功部署
                    TowerHA - HA - 新部署 SKS - sks1.6 服务可成功完成 OBS 关联并开启插件
                    TowerHA - HA - 新部署 SKS - sks1.6 可成功上传同构节点模板
                    TowerHA - HA - 新部署 SKS - sks1.6 可成功上传异构节点模板
                    TowerHA - HA - 新部署 SKS - sks1.6 可原地更新服务虚拟机
                    TowerHA - HA - 新部署 SKS - sks1.6 可成功卸载，主备节点的sks-manager数据库记录清空，fileserver 中的安装包可成功删除
                    TowerHA - HA - 新部署 SKS - sks1.6 x86 rocky 版本可成功部署
                    TowerHA - HA - 新部署 SKS - sks1.6 x86 oe 版本可成功部署
                    TowerHA - HA - 新部署 SKS - sks1.6 aarch64 oe 版本可成功部署
                    TowerHA - HA - 新部署 SKS - 不可部署 sks1.6 之前版本 SKS
                    TowerHA - HA - 新部署 SKS - sks-manager 数据库数据可正确写入主节点数据库并同步到备节点数据库
                    TowerHA - HA - 新部署 user registry - v1.6.0 安装包可成功上传，新上传的 user registry 安装包存入 fileserver
                    TowerHA - HA - 新部署 user registry - v1.6.0 registry 可部署
                    TowerHA - HA - 新部署 user registry - 部署完成 registry 可成功卸载
                    TowerHA - HA - 新部署 user registry - 卸载后的安装包可成功删除，fileserver 中的安装包可成功删除
                    TowerHA - HA - 新部署 user registry  - user registry 部署后，包和数据库信息同步到备节点
                    TowerHA - HA - 新部署 user registry - x86 rocky registry 可成功部署
                    TowerHA - HA - 新部署 user registry - x86 tl3 registry 可成功部署
                    TowerHA - HA - 新部署 user registry - aarch64 rocky registry 可成功部署
                HA 模式下tower 故障及恢复
                    TowerHA - HA - sks 未部署，主节点故障，备节点已接管 tower，单点工作 - sks 完整生命周期检查
                    TowerHA - HA - sks 已部署，主节点故障，备节点已接管 tower，单点工作 - 可成功卸载 sks
                    TowerHA - HA - sks 已部署，主节点故障，备节点已接管 tower，单点工作 - 可提升管控集群模式
                    TowerHA - HA - sks 已部署，主节点故障，备节点已接管 tower，单点工作 - 可原地更新服务虚拟机
                    TowerHA - HA - sks 已部署，主节点故障，备节点已接管 tower，单点工作 - 可完成 sks 服务上下线
                    TowerHA - HA - sks 已部署，主节点故障，备节点已接管 tower，单点工作 - 可完成节点文件上传
                    TowerHA - HA - sks 已部署，主节点故障，备节点已接管 tower，单点工作 - 已有的 sks 服务及插件状态正常
                    TowerHA - HA - sks 已部署，主节点故障，备节点已接管 tower，单点工作 - 已有的 sks 服务可正常运维工作集群及资源
                    TowerHA - HA - sks 已部署，主节点故障，备节点已接管 tower，单点工作 - 更新 tower ntp，sks 服务及工作集群可完成同步更新
                    TowerHA - HA - sks 已部署，主节点故障，备节点已接管 tower，单点工作 - 可完成 sks 升级
                    TowerHA - HA - sks 已部署，原主节点故障恢复后，原备节点为主节点 - sks-manager 数据库从已成为主节点的原备节点同步回原主节点数据库
                    TowerHA - HA - sks 已部署，原主节点故障恢复后，原备节点为主节点 - 可成功卸载 sks，主备节点数据库完成数据清理
                    TowerHA - HA - sks 已部署，原主节点故障恢复后，原备节点为主节点 - 可提升管控集群模式
                    TowerHA - HA - sks 已部署，原主节点故障恢复后，原备节点为主节点 - 可原地更新服务虚拟机
                    TowerHA - HA - sks 已部署，原主节点故障恢复后，原备节点为主节点 - 可完成 sks 服务上下线
                    TowerHA - HA - sks 已部署，原主节点故障恢复后，原备节点为主节点 - 可完成节点文件上传，主备数据库更新数据
                    TowerHA - HA - sks 已部署，原主节点故障恢复后，原备节点为主节点 - 已有的 sks 服务可正常运维工作集群及资源
                    TowerHA - HA - sks 已部署，原主节点故障恢复后，原备节点为主节点 - 更新 tower ntp，sks 服务及工作集群可完成同步更新
                    TowerHA - HA - sks 已部署，原主节点故障恢复后，原备节点为主节点 - 可完成 sks 升级
                    TowerHA - HA - 仲裁节点故障 - 不影响 Tower 运行，sks 完整生命周期可成功执行
                    TowerHA - HA - 仲裁节点故障 - 部署 sks，上传节点文件，主备数据库可完成同步？？？ - TBD
                    TowerHA - HA - 备节点故障 - sks 服务状态无影响，服务可运维
                    TowerHA - HA - 备节点故障 - 部署 sks，上传节点文件，可完成，上传文件仅记录在主节点本地，不更新 fileserver 内容
                    TowerHA - HA - 备节点故障 - 部署 sks，上传节点文件 - 备节点恢复后，无需同步数据
                    TowerHA - HA - 备节点故障 - 卸载 sks - 主节点完成 sks 卸载，备节点恢复后，备节点 sks-manager 数据库清空
                    TowerHA - HA - 备节点故障 - 可完成 sks 升级，数据记录仅写入主节点数据库，恢复后同步到备节点数据库
                    TowerHA - HA - 备节点故障 - 可完成 sks 扩容
                    TowerHA - HA - 备节点+仲裁故障 - sks 服务状态无影响，服务可运维
                    TowerHA - HA - 主节点+仲裁故障 - tower 无法访问，sks 服务无法运维，工作集群正常运行
                    TowerHA - HA - 主备节点故障 - tower 无法访问，sks 服务无法运维，工作集群正常运行
                HA 模式下的手动切换主节点
                    TowerHA - HA - sks 未部署，主节点故障，备节点已接管 tower，单点工作 - sks 完整生命周期检查
                    TowerHA - HA - sks 已部署，手动切换主节点后 - 可成功卸载 sks，主备节点数据库完成数据清理
                    TowerHA - HA - sks 已部署，手动切换主节点后 - 可提升管控集群模式
                    TowerHA - HA - sks 已部署，手动切换主节点后 - 可原地更新服务虚拟机
                    TowerHA - HA - sks 已部署，手动切换主节点后 - 可完成 sks 服务上下线
                    TowerHA - HA - sks 已部署，手动切换主节点后 - 可完成节点文件上传，数据记录写入主节点数据库，同步到备节点数据库
                    TowerHA - HA - sks 已部署，手动切换主节点后 - 已有的 sks 服务及插件状态正常
                    TowerHA - HA - sks 已部署，手动切换主节点后 - 已有的 sks 服务可正常运维工作集群及资源
                    TowerHA - HA - sks 已部署，手动切换主节点后 - 更新 tower ntp，sks 服务及工作集群可完成同步更新
                    TowerHA - HA - sks 已部署，手动切换主节点后 - 可完成 sks 升级，数据记录写入主节点数据库，同步到备节点数据库
            490 single 转 HA
                TowerHA - single转HA - 已存在 sks1.5 版本服务，不支持 tower 转 HA 模式
                TowerHA - single转HA - 已存在 sks1.5 版本服务，升级到 1.6 后，允许 Tower 转 HA 模式
                TowerHA - single转HA - 已部署 sks1.6，转换为 HA 模式后，可成功卸载 sks
                TowerHA - single转HA - 已部署 sks1.6，转换为 HA 模式后，可上传节点文件/镜像文件
                TowerHA - single转HA - 已部署 sks1.6，转换为 HA 模式后，可提升管控集群模式
                TowerHA - single转HA - 已部署 sks1.6，转换为 HA 模式后，sks 服务下线后可以重新正常上线
                TowerHA - single转HA - 已部署 sks1.6，转换为 HA 模式后，可取关/重新关联 OBS
                TowerHA - single转HA - 已部署 sks1.6，转换为 HA 模式后，可创建新虚拟机集群
                TowerHA - single转HA - 已部署 sks1.6，转换为 HA 模式后，可创建新物理机集群
                TowerHA - single转HA - 已部署 sks1.6，转换为 HA 模式后，主备 tower 上的 sks-manager 数据库数据同步检查
                TowerHA - single转HA - 已部署 user registry 1.4.1，转换为 HA 模式后，可成功卸载 user registry
                TowerHA - single转HA - 已部署 user registry 1.6.0，转换为 HA 模式后，可成功卸载 user registry
                TowerHA - single转HA - 已上传 user registry 1.6.0 pkg，转换为 HA 模式后，可成功部署 user registry
                TowerHA - single转HA - 已上传 user registry 1.6.0 pkg，转换为 HA 模式后，可成功删除 user registry pkg
            运维过程中的故障场景
                TowerHA - HA - 上传 sks registry 安装包时主节点故障，安装包上传失败，发生主备切换后可重传
                TowerHA - HA - 部署 sks registry 时主节点故障，部署失败，发生主备切换后可重新部署成功
                TowerHA - HA - 上传 安装包过程中主节点故障，部署中止，发生主备切换后可重新部署
                TowerHA - HA - 部署 sks 过程中主节点故障，部署中止，发生主备切换后需清理环境，再重新部署
            Tower fileserver/sks 组件改造
                新数据存储
                    TowerHA - sks-manager - sks-upload-pvc - sks 安装包上传方式不变，仍然使用 pvc 挂载 50G 本地存储作为临时存储 - TBD
                    TowerHA - sks-manager - sks-upload-pvc - 主备切换后，sks 节点文件包上传，使用新的节点 50G 本地存储作为临时存储 - TBD
                    TowerHA - sks-manager - sks-upload-pvc - sks 节点文件包上传方式不变，仍然使用本地存储作为临时存储
                    TowerHA - sks-manager - sks-upload-pvc - sks GPU 镜像文件包上传方式不变，仍然使用本地存储作为临时存储
                    TowerHA - sks-manager - sks-upload-pvc - 切换主备后，临时存储中的内容不会同步，无法恢复
                    TowerHA - sks-manager - sks-upload-pvc - 切换主备后，临时存储中的内容丢失，对节点功能无影响
                    TowerHA - sks-manager - sks-opt-pvc - sks 部署时，解压后将 ksctl及shell脚本 上传至 tower fileserver, 生成目录 /sks-manager/sks/{PackageVersion}/tools/ 放置
                    TowerHA - sks-manager - sks-opt-pvc - sks 组件部署及卸载时，使用本地缓存的 ksctl 进行部署（/opt/sks/{PackageVersion}/bin/）
                    TowerHA - sks-manager - sks-opt-pvc - 删除本地缓存的 ksctl，sks 卸载时，从 tower fileserver 中重新获取到本地后执行
                    TowerHA - sks-manager - sks-opt-pvc - 切换主备后，sks 卸载时，sks 从 tower fileserver 中重新获取 ksctl 到本地/opt/sks/{PackageVersion}/bin/
                    TowerHA - sks-manager - sks-opt-pvc - sks 升级时，解压后将新的 ksctl 上传至 tower fileserver，以版本进行区分
                    TowerHA - sks-manager - sks-opt-pvc - 同版本的 sks dev build 升级时，解压后将新的 ksctl及shell脚本 上传至 tower fileserver，替换已有的 ksctl ？？？ - TBD
                    TowerHA - sks-manager - sks-opt-pvc - sks 升级到更高版本后，tower fileserver 中旧版本的 ksctl 及 shell 脚本被删除 ？？？ - TBD
                    TowerHA - sks-manager - sks-opt-pvc - sks 升级失败，tower fileserver 中旧版本的 ksctl 及 shell 脚本保持不变 - TBD 有没有可能因为失败时机靠后已经被新版替换了？
                    TowerHA - sks-manager - sks-opt-pvc - sks 卸载后，tower fileserver 中 ksctl 被删除
                    TowerHA - sks-fileserver - single 模式下，tower 中的 fileserver 从 registry 中拉取并存放 bootstrap 集群使用的 playbook 到容器磁盘，，不再挂载 pv
                    TowerHA - sks-fileserver - HA 模式下，tower 中的 sks-fileserver 从 registry 中拉取并存放 bootstrap 集群使用的 playbook 到容器磁盘，，不再挂载 pv
                    TowerHA - sks-fileserver - 切换主备后，在新节点拉起的 sks-fileserver 重新从 registry 中获取 playbook 到容器磁盘
                    TowerHA - sks-fileserver - sks 升级后，在新节点拉起的 sks-fileserver 重新从 registry 中获取新版本的 playbook 到容器磁盘
                    TowerHA - capp - 部署 sks-registry，安装包上传后，检查本地放置 /var/lib/fileserver/data/capp/packages/{id}/images.tar
                    TowerHA - capp - 部署 sks-registry，安装包从本地上传到 fileserver 中，同时记录fileserver 中的 path 在 capp package 表的 images 数据中
                    TowerHA - capp - 部署 user-registry，安装包上传后，检查本地放置 /var/lib/fileserver/data/capp/packages/{id}/images.tar
                    TowerHA - capp - 部署 user-registry，安装包从本地上传到 fileserver 中，同时记录 fileserver 中的 path 在 capp package 表的 images 数据中
                已有数据的迁移
                    TowerHA - sks-manager - sks-opt-pvc - 升级470到490后，/opt/sks/ksctl （不包括 shell 脚本）将被上传到 tower fileserver
                    TowerHA - sks-manager - sks-opt-pvc - 升级470到490后，/opt/sks/ksctl （不包括 shell 脚本）将迁移到本地 /opt/sks/{PackageVersion}/bin/ 目录 - TBD
                    TowerHA - sks-manager - sks-upload-pvc - 升级470到490后，/uploads 目录被清理 - TBD
                    TowerHA - sks-manager - sks-opt-pvc - 升级480到490后，/opt/sks/ksctl (不包括 shell 脚本）将被上传到 tower fileserver
                    TowerHA - sks-manager - sks-opt-pvc - 升级480到490后，/opt/sks/ksctl（不包括 shell 脚本）将迁移到本地 /opt/sks/{PackageVersion}/bin/ 目录 - TBD
                    TowerHA - sks-manager - sks-upload-pvc - 升级480到490后，/uploads 目录被清理 - TBD
                    TowerHA - sks-fileserver - 升级tower到490后升级 sks1.6，tower 中的 fileserver 从 registry 中拉取并存放 bootstrap 集群使用的 playbook 到容器磁盘，不再挂载 pv，原有 pvc 删除，pv 还存在
                    TowerHA - sks-fileserver - 升级tower到490后升级 sks1.6，管控集群的 sks-fileserver 同步变动，不再使用 pv 存储文件，使用节点的 local 存储拉取 registry 中物料
                已有数据的更新
                    TowerHA - sks-manager - 升级 sks 到新版本（1.6 dev 版本更新），tower 本地保存的 ksctl 将被更新
                    TowerHA - sks-manager - 升级 sks 到新版本（1.6 dev 版本更新），tower fileserver 中 ksctl 将被更新
                    [Future] TowerHA - sks-manager - 升级 sks 到新版本（1.6+ 版本更新），tower 本地保存的 ksctl 及 shell 脚本存储于新版本目录，旧版本目录仍存在？？？ - TBD
                    [Future] TowerHA - sks-manager - 升级 sks 到新版本（1.6+ 版本更新），tower fileserver 中 ksctl 及 shell 脚本将上传到新版本目录下，旧版本目录仍存在？？？ - TBD
                    TowerHA - sks-fileserver - 升级 sks 到新版本（1.6 dev 版本更新），fileserver data 中的 playbook 将重新获取
                    [Future] TowerHA - sks-fileserver - 升级 sks 到新版本（1.6+ 版本更新），fileserver data 中的 playbook 将重新获取到新版本目录下，旧版本目录仍存在？？？ - TBD
                数据补偿
                    TowerHA - fileserver 中ksctl 及shell 脚本文件丢失，可通过 fileserver api 上传对应二进制文件完成补偿 - TBD 怎么传？？
                    TowerHA - sks-fileserver - 删除 sks-fileserver 中的 playbook 文件，触发管控集群原地更新，sks-fileserver 重新从 registry 中获取 playbook 到容器磁盘
            根据变更补充
                TowerHA - 490 - sks fileserver 变更 - tower 中sks fileserver 使用empty dir，不再使用csi 创建 pv，管控集群可拉取到playbook完成原地更新
                TowerHA - 490 - sks fileserver 变更 - 管控集群中 sks fileserver 使用empty dir，不再使用csi 创建 pv，sks-fileserver 中原地更新/物理机物料 可获取
                TowerHA - 490 - sks fileserver 变更 - 升级上来的管控集群中sks fileserver 中内容可支持-1版本的集群和物理机使用
                TowerHA - 490 - sks fileserver 变更 - 升级后的 tower 中 sksfileserver 中内容重新拉取，仅有支持管控集群原地更新的物料
                TowerHA - 490 - HA- sks fileserver 变更 - tower 发生主备切换后，sks fileserver pod 重建，其中内容重新拉取
                TowerHA - 490 - HA- tower 发生主备切换后，检查 sks-manager 中环境变量 PATH 是否正确
                TowerHA - 490 - 下载到 /opt/sks/{version}/bin/ksctl 的 ksctl 已 chmod 0755
                TowerHA - 490 - 本地 ksctl 删掉，会在使用到的时候（部署或卸载 sks 组件）自动从 tower fileserver 下载
                TowerHA - 490 - IP 部署 sks registry，harbor 证书可上传到文件服务器，验证路径/etc/containerd/certs.d/{hostname}/registry.crt 正确
                TowerHA - 490 - 域名部署 sks registry，harbor 证书可上传到文件服务器，验证路径/etc/containerd/certs.d/{hostname}/registry.crt 正确
                TowerHA - 470升级490 - 验证 ksctl 和 registry 证书的上传
                TowerHA - 490 - 重新部署 SKS， registry 证书和 ksctl 会重新上传到 fileserver
                TowerHA - 490 - 卸载 SKS后， registry 证书 和 ksctl 从 tower fileserver 中清理
                TowerHA - 490 - 升级 SKS后， 无效了的 ksctl 从 tower fileserver 中被清理
                TowerHA - 490 - HA - 切换到备节点后，可成功上传节点文件
                TowerHA - 490 - HA - 切换到备节点后，在原主节点上可以完成registry 升级
                TowerHA - 490 - HA - 切换备节点后，可卸载并重新部署 SKS 1.6
                TowerHA - 490 - HA - tower 仅单节点降级模式工作时，部署 SKS，fileserver 数据可在当前active 节点上传，等待 passive 节点恢复后才能完成同步
    SKS1.6 兼容 SMTX OS 630  [SKS-4157]
        SKS 1.6 兼容适配条带数默认 8 需求
            在SMTX OS630及以上新建SKS1.6
                registry -  部署 - 磁盘容量取决于scos模板，默认400G - 无影响，部署成功
                registry -  部署 - 部署成功后查看registry虚拟机使用的存储策略条带数：8条带
                registry - 升级 - 无影响，升级成功
                用户容器镜像仓库 - 新建 - 设置磁盘容量 - 奇数 - 限制允许输入奇数，但是强制hover提示并且自动向上取偶
                用户容器镜像仓库 - 新建 - 设置磁盘容量 - 偶数 - 实际创建出来的volume数值与设置的保持一致
                用户容器镜像仓库 - 编辑 - 编辑磁盘容量 - 奇数 - 限制允许设置奇数，但是强制hover提示，失焦后自动向上取偶
                用户容器镜像仓库 - 编辑 - 编辑磁盘容量 - 偶数 - 编辑成功后查看volume的数值，与编辑的保持一致
                SKS系统服务 - 部署SKS1.5 - 部署成功? 但是无法开启监控，日志等插件 --TBD
                SKS系统服务 - 部署SKS1.6 - 部署成功，支持开启监控，日志等插件 - 查看grafana对应的pvc分配量1G，pv容量2G
                SKS系统服务 - 部署SKS1.6 - 部署成功后提升模式 - 提升成功无影响
                新建工作负载集群 - ELF_CSI - 1+1集群开启监控日志等插件 - 开启成功 - 查看grafana对应的pvc分配量1G，pv容量2G
                新建工作负载集群 - ELF_CSI - 1+1集群开启监控日志等插件 - 扩容到3+3 - 扩容成功，节点正常创建
                新建工作负载集群 - ELF_CSI - 节点组 - worker - 存储 - 输入奇数 - UI限制不允许输入，有提示
                新建工作负载集群 - ELF_CSI - 节点组 - worker - 存储 - 输入偶数 - UI限制提示消失，校验通过
                新建工作负载集群 - ELF_CSI - 节点组 - 新增worker节点组 - 存储 - 输入奇数 - UI限制不允许
                新建工作负载集群 - ZBS_CSI（8条带）- 1+1集群开启监控日志等插件 - 开启成功 - 查看grafana对应的pvc分配量1G，pv容量2G -与OS版本无关，与CSI版本有关（ZBS-CSI2.8-SKS1.5）
                新建工作负载集群 - ZBS-CSI（8条带）- 节点组 - 新增worker节点组 - 存储 - 输入奇数 - UI允许输入 - 强制hover tooltip向上取偶 - 与CSI无关，与模板条带数有关
                已有工作负载集群 - 新建节点组 - 存储 - 设置为奇数 - UI限制不允许，有提示
                已有工作负载集群 - 新建节点组 - 存储 - 设置为偶数 - 新建节点组成功
                已有工作负载集群 - 编辑节点组 - 存储 - 修改为偶数 - 允许修改并且可以修改成功 - 原地更新
                已有工作负载集群 - 编辑节点组 - 存储 - 修改为奇数 - 允许修改强制hover tip展示提示文案并且自动向上取偶
                已有工作负载集群 - 编辑节点组 - 扩容节点数量 - 存储 - 设置为偶数 - 可以保存 - 扩容成功
                已有工作负载集群 - 编辑节点组 - 扩容节点数量 - 存储 - 设置为奇数 - 允许修改强制hover tip展示提示文案并且自动向上取偶，可以保存
                新建工作负载集群 - 跨版本模板分发 - 从630以下分发到630及以上 - 创建时分发 - 分发成功后条带数不变保持4条带 - 创建奇数虚拟卷 - 不自动向上取偶
                新建工作负载集群 - 跨版本模板分发 - 从630以下分发到630及以上 - 先分发后创建 - 分发成功后不变保持4条带 - 创建奇数pvc - 实际pv容量与pvc保持一致
                新建工作负载集群 - 跨版本模板分发 - 从630及以上分发到630以下 - 创建时分发 - 允许分发,条带数降级为4条带，容量不变
                新建工作负载集群 - 跨版本模板分发 - 从630及以上分发到630以下 - 分发成功后新建节点存储设置为奇数 - 创建成功，可设置奇数，不会自动向上取偶
                新建工作负载集群 - 跨版本模板分发 - 从630及以上分发到630以下 - 先分发（内容库）后创建 - 允许分发,条带数降级为4条带，容量不变
                创建持久卷申领 - yaml/导入yaml/kubectl apply -f
                    ELF-CSI - 新建自定义pvc - 分配量输入奇数 - UI不限制，创建成功，实际创建的pv容量自动向上取偶
                    ELF-CSI - 新建自定义pvc - 分配量输入偶数 - 创建成功，实际创建的pv容量与pvc分配量保持一致
                    ELF-CSI - 自定义pvc - 在线扩容 - 扩容为奇数 - 实际触发向上取偶 - pvc分配量和pv容量不一致
                    ELF-CSI - 自定义pvc - 在线扩容 - 扩容为偶数 - pvc分配量和pv容量一致
                    ELF-CSI - 自定义pvc - 克隆 - 源pvc storage是奇数，pv容量向上取偶 - 克隆pvc大小与源pvc一致（奇数）- 克隆后pvc分配量(奇数)和pv容量(pvc分配量向上取偶)
                    ELF-CSI - 自定义pvc - 克隆 - 源pvc storage是偶数 - 克隆pvc大小与源pvc一致 - 克隆成功 - 克隆后pvc分配量和pv容量一致
                    ELF-CSI - 新建自定义pvc - 快照 - 源pvc storage是奇数，pv容量是偶数 - 快照后 - 快照参数条带数（8条带）和大小不变（偶数）
                    ELF-CSI - 存量自定义pvc - 快照 - 源pvc storage是偶数 - 快照后 -- 快照的条带数（4条带）和容量大小不变 - TBD
                    ELF-CSI - 新建自定义pvc - 快照恢复 - 源pvc storage是奇数，pv容量是偶数 - 快照恢复时pvc 配置奇数 - 恢复失败，报错 requested volume size {size} is less than the size {size} for the source snapshot {vsName}
                    ELF-CSI - 自定义pvc - 快照恢复 - 源pvc storage是偶数 - 快照后恢复 - pvc分配量和pv容量一致
                    ZBS-CSI - 新建自定义pvc - 分配量输入奇数 - UI不限制，创建成功，实际创建的pv容量自动向上取偶
                    ZBS-CSI - 新建自定义pvc - 分配量输入偶数 - 创建成功，实际创建的pv容量与pvc分配量保持一致
                    ZBS-CSI - 自定义pvc - 在线扩容 - 扩容为奇数 - 实际触发向上取偶 - pvc分配量和pv容量不一致
                    ZBS-CSI - 自定义pvc - 在线扩容 - 扩容为偶数 - pvc分配量和pv容量一致
            在SMTX OS630以下新部署SKS1.6
                registry -  部署 - 磁盘容量取决于scos模板，默认400G - 无影响，部署成功
                用户容器镜像仓库 - 新建 - 设置磁盘容量 - 奇数 - 允许输入，创建成功，实际创建出来的虚拟卷是与设置的奇数保持一致
                用户容器镜像仓库 - 新建 - 设置磁盘容量 - 偶数 - 实际创建出来的volume数值与设置的保持一致
                用户容器镜像仓库 - 编辑 - 编辑磁盘容量 - 奇数 - 无UI限制，允许设置奇数并且可以编辑成功
                SKS系统服务 - 部署SKS1.6 - 部署成功，支持开启监控，日志等插件 - 查看grafana对应的pvc分配量1G，pv容量1G
                新建工作负载集群 - 1+1集群开启监控日志等插件 - 开启成功 - 查看grafana对应的pvc分配量1G，pv容量1G
                新建工作负载集群 - 节点组 - worker - 存储 - 输入奇数 - UI不限制，允许输入，并且创建成功
                新建工作负载集群 - 节点组 - worker - 存储 - 输入偶数 - UI不限制，允许输入，并且创建成功
                已有工作负载集群 - 新建节点组 - 存储 - 设置为奇数 - UI不限制，新节点创建成功
                已有工作负载集群 - 编辑节点组 - 存储 - 修改为奇数 - 允许修改不限制，原地更新成功
                ELF-CSI - 新建自定义pvc - 分配量输入奇数 - UI不限制，创建成功，实际创建的pv容量与pvc设置的分配量保持一致
                ELF-CSI - 新建自定义pvc - 分配量输入偶数 - 创建成功，实际创建的pv容量与pvc分配量保持一致
                ELF-CSI - 自定义pvc - 在线扩容 - 扩容为奇数 - 扩容成功 - pvc分配量和pv容量一致
                ELF-CSI - 自定义pvc - 克隆 - 源pvc storage是奇数 - 克隆后pvc分配量和pv容量一致
                ELF-CSI - 自定义pvc - 快照 - 源pvc storage是奇数，pv容量保持一致 - 快照后 - restoresize字段与pvc容量保持一致（奇数）
                ELF-CSI - 自定义pvc - 快照恢复 - 源pvc storage是奇数，pv容量保持一致 - 快照后恢复 - pvc分配量和pv容量保持奇数且一致
                ZBS-CSI - 新建自定义pvc - 分配量输入奇数 - UI不限制，创建成功，实际创建的pv容量自动向上取偶（从SKS1.5开始自动向上取偶）
                ZBS-CSI - 新建自定义pvc - 分配量输入偶数 - 创建成功，实际创建的pv容量与pvc分配量保持一致
                新建工作负载集群 - 跨版本模板分发 - 从630以下分发到630及以上 - 先分发后创建 - 分发成功后条带数不变，容量不变 - 创建奇数pvc - 实际pv容量（pvc向上取偶）
                升级SMTX OS至630及以上
                    registry - 已有registry - 正常运行无影响
                    已有用户容器镜像仓库 - 编辑 - 编辑磁盘容量 - 奇数 - UI不限制，可编辑成功
                    用户容器镜像仓库 - 新建 - 设置磁盘容量 - 奇数 - UI限制不允许输入，有提示
                    SKS系统服务 - 已部署SKS1.6 - 监控，日志等插件保持开启 - 查看grafana对应的pvc分配量1G，pv容量1G
                    SKS系统服务 - 已部署SKS1.6 - 关闭监控，日志等插件后重新开启 - 查看grafana对应的pvc分配量1G，pv容量2G
                    已有工作负载集群 - 编辑节点组 - 存储 - 修改为奇数 - UI不限制，允许修改成功，无提示
                    已有工作负载集群 - 新建节点组 - 存储 - 修改为奇数 - UI限制，不允许修改，有提示
                    新建工作负载集群 - 1+1集群开启监控日志等插件 - 开启成功 - 查看grafana对应的pvc分配量1G，pv容量2G
                    新建工作负载集群 - 节点组 - worker - 存储 - 输入奇数 - UI限制不允许输入，有提示
                    新建工作负载集群 - 节点组 - worker - 存储 - 输入偶数 - UI限制提示消失，校验通过
                    新建工作负载集群 - 跨版本模板分发 - 从630及以上分发到630以下 - 创建时分发 - 允许分发，8条带变成4条带，容量不变
                    创建持久卷申领 - UI表单/yaml/导入yaml/kubectl apply -f
                        ELF-CSI - 存量pvc - 在线扩容 - 扩容为奇数 - 实际不会触发向上取偶 - pvc分配量和pv容量一致
                        ELF-CSI - 存量pvc - 在线扩容 - 扩容为偶数 - pvc分配量和pv容量一致
                        ZBS-CSI - 存量自定义pvc - 在线扩容 - 扩容为奇数 - 实际触发向上取偶 - pvc分配量和pv容量不一致
                        ZBS-CSI - 存量自定义pvc - 在线扩容 - 扩容为偶数 - pvc分配量和pv容量一致
                        ELF-CSI - 新建自定义pvc - 分配量输入奇数 - UI不限制，创建成功，实际创建的pv容量自动向上取偶
                        ELF-CSI - 自定义pvc - 克隆 - 源pvc storage是奇数 - 克隆后pvc分配量和pv容量不一致 - pv是pvc向上取偶 - 克隆卷条带数和大小与源卷保持一致
                        ELF-CSI - 存量自定义pvc - 克隆 - 源pv storage是奇数 - 克隆成功 - 克隆卷条带数和大小与源卷保持一致
                        ELF-CSI - 自定义pvc - 快照 - 源pvc storage是奇数，pv容量是偶数 - 快照后 - 快照的条带数和大小与源卷保持一致
                        ELF-CSI - 自定义pvc - 快照恢复 - 源pvc storage是奇数，pv容量是偶数 - 快照后恢复 - 与快照参数保持一致 - 快照恢复，pvc 配置奇数，恢复失败，报错 requested volume size {size} is less than the size {size} for the source snapshot {vsName}
                        ELF-CSI - 自定义pvc - 快照恢复 - 源pvc storage是偶数 - 快照后恢复 - 与快照参数保持一致 - 恢复成功
                        ZBS-CSI - 新建自定义pvc - 分配量输入奇数 - UI不限制，创建成功，实际创建的pv容量自动向上取偶
                        ZBS-CSI - 新建自定义pvc - 分配量输入偶数 - 创建成功，实际创建的pv容量与pvc分配量保持一致
            SMTX OS630以下部署SKS1.5后SMTX OS 升级到630及以上
                registry - OS升级前已部署 - 正常运行无影响
                registry - 已有registry升级 - 无影响，升级成功
                registry - 卸载后重新部署 - 磁盘容量取决于scos模板，默认400G - 无影响，部署成功
                用户容器镜像仓库 - 编辑已有磁盘容量 - 奇数 - 输入奇数 - UI不限制，实际编辑失败？？？-- TBD
                用户容器镜像仓库 - 编辑已有磁盘容量 - 偶数 - 编辑成功后查看volume的数值，与编辑的保持一致
                用户容器镜像仓库 - 新建 - 设置磁盘容量 - 奇数 - 允许输入奇数，创建失败？
                用户容器镜像仓库 - 新建 - 设置磁盘容量 - 偶数 - 实际创建出来的volume数值与设置的保持一致
                SKS系统服务 - OS升级前已开启监控，日志等所有插件 - 升级后监控，日志等插件保持开启，正常运行
                SKS系统服务 - OS升级前已开启监控，日志等所有插件 - 升级后关闭在开启 - 无法创建1G pvc导致开启后addon不ready
                SKS系统服务 - OS升级前已开启监控，日志等所有插件 - 升级后提升模式 - 提升成功 -- TBD
                已有工作负载集群 - 已开启监控，日志等插件 - OS升级后正常运行
                已有工作负载集群 - OS升级后关闭监控，日志等插件后重新开启 - 无法创建grafana对应1GiB的pvc导致addon无法就绪
                已有工作负载集群 - 已有节点组 - 存储（升级前为奇数）- OS升级后，保持不受影响
                已有工作负载集群 - 编辑已有节点组 扩容 - 存储（升级前为奇数）- 新建节点报错？？
                已有工作负载集群 - 编辑已有节点组 - 存储 - 修改为奇数 - 允许修改，但是更新不成功？
                已有工作负载集群 - 编辑节点组 - 扩容节点数量 - 存储 - 设置为偶数 - 可以保存 - 扩容成功
                已有工作负载集群 - 编辑节点组 - 扩容节点数量 - 存储 - 设置为奇数 - 可以保存，实际创建新节点失败？
                新建工作负载集群 - 集群开启监控日志等插件 - 无法开启 - 因为无法置备grafana对应的1G的pvc
                新建工作负载集群 - 节点组 - worker - 存储 - 输入奇数 - 允许设置，但是实际创建不成功？
                ELF-CSI - 新建自定义pvc - 分配量输入奇数 - UI不限制，但是置备pv不成功
                ELF-CSI - 存量自定义pvc - 在线扩容 - 扩容为奇数 - 扩容成功不受影响
                ELF-CSI - 存量自定义pvc - 克隆 - 源pvc storage是奇数 - 克隆成功不受影响，pvc和pv一致是奇数
                ELF-CSI - 存量自定义pvc - 快照 - 源pvc storage是奇数 - 快照成功不影响
                ELF-CSI - 自定义pvc - 快照恢复 - 源pvc storage是奇数 - 快照后恢复 - 恢复后的pvc和pv一致是奇数不影响
                ZBS-CSI - 新建自定义pvc - 分配量输入奇数 - UI不限制，创建成功，实际创建的pv容量自动向上取偶
                升级SKS1.5到1.6及以上
                    obs服务 - OS升级前已部署 - ovm存储空间分配是奇数 - 正常运行无影响
                    obs服务 - OS升级前已部署 - ovm存储空间分配是奇数 - 升级obs服务 - 正常升级无影响 --TBD
                    obs服务 - 新部署 - ovm存储空间分配是奇数 - UI限制不允许 - Tower-20786
                    registry - OS升级前已部署 - 正常运行无影响
                    用户容器镜像仓库 - 新建 - 设置磁盘容量 - 奇数 - 限制不允许输入奇数，有提示
                    用户容器镜像仓库 - 编辑已有磁盘容量 - 奇数 - 输入奇数 - UI限制无法输入，有提示
                    用户容器镜像仓库 - 编辑 - 编辑磁盘容量 - 偶数 - 编辑成功后查看volume的数值，与编辑的保持一致
                    SKS系统服务 - OS升级前已开启监控，日志等所有插件 - 升级后保持开启 - 查看grafana对应的pvc分配量1G，pv容量1G
                    SKS系统服务 - OS升级前已开启监控，日志等所有插件 - 升级后关闭 - 升级到SKS1.6后再开启 - 开启成功，查看grafana对应的pvc分配量1G，pv容量2G
                    已有工作负载集群 - OS升级后关闭监控，日志等插件后升级到1.6后重新开启 - 开启成功
                    已有工作负载集群 - 已有节点组 - 存储（升级前为奇数）- OS升级后，保持不受影响
                    已有工作负载集群 - 存储（升级前为奇数）- OS升级后，升级kubernetes版本，为8条带的模板 - 升级前增加提示，需要把存储变成偶数后才可以升级
                    已有工作负载集群 - 存储（升级前为偶数）- OS升级后，升级kubernetes版本，为8条带的模板 - 平滑升级成功
                    已有工作负载集群 - 存储（升级前为偶数）- OS升级后，升级kubernetes版本，为8条带的模板（触发模板分发）- 模板分发成功后平滑升级成功
                    已有工作负载集群 - 编辑已有节点组 扩容 - 存储（升级前为奇数）- 新建节点报错实际存储取值向上取偶
                    已有工作负载集群 - 编辑已有节点组（使用原有4条带模板）- 存储 - 修改为奇数 - UI不限制允许，修改成功
                    已有工作负载集群 - 编辑节点组 - 扩容节点数量 - 存储 - 设置为奇数 - UI限制不允许，有提示
                    新建工作负载集群 - 1+1集群开启监控日志等插件 - 开启成功 - 查看grafana对应的pvc分配量1G，pv容量2G
                    新建工作负载集群 - 节点组 - worker - 存储 - 输入奇数 - UI限制不允许输入，有提示
                    新建工作负载集群（1.26-8条带-偶数）- 升级k8s版本 - v1.27（SKS版本1.5）- 升级成功
                    ELF-CSI - 新建自定义pvc - 分配量输入奇数 - UI不限制，创建成功，实际创建的pv容量自动向上取偶
                    ELF-CSI - 自定义pvc - 在线扩容 - 扩容为奇数 - 实际触发向上取偶 - pvc分配量和pv容量不一致
                    ELF-CSI - 自定义pvc - 克隆 - 源pvc storage是奇数 - 克隆后pvc分配量和pv容量不一致 - pv是pvc向上取偶
                    ELF-CSI - 自定义pvc - 快照 - 源pvc storage是奇数，pv容量是偶数 - 快照后 - 快照大小与源 pv 一致，为偶数
                    ELF-CSI - 自定义pvc - 快照恢复 - 源pvc storage是奇数，pv容量是偶数 - 快照后恢复 - 快照恢复，pvc 配置奇数，恢复失败，报错 requested volume size {size} is less than the size {size} for the source snapshot {vsName}
                    ZBS-CSI - 新建自定义pvc - 分配量输入奇数 - UI不限制，创建成功，实际创建的pv容量自动向上取偶
            UI页面
                虚拟机集群worker节点组
                    创建虚拟机集群 - 节点配置 - worker节点组
                        存储 - 查询到模板条带数8 - 增加info icon，hover展示tooltip
                        存储 - 查询到模板条带数4 - 无增加info icon，hover展示tooltip
                        存储 - 查询到模板条带数8 - 输入奇数，onchange判定，强制tooltip进入hover状态，blur自动向上取偶 - 创建成功
                        存储 - 查询到模板条带数8 - 输入奇数，blur自动向上取偶 - 创建成功后检查虚拟机volume的数值，向上取偶后的数值
                        存储 - 查询到模板条带数8 - 输入奇数，blur自动向上取偶，再修改为其他偶数 - 不做变动
                        存储 - 查询到模板条带数8 - 输入偶数，不作变动
                        存储 - 查询到模板条带数4 - 输入奇数，不作变动
                        存储 - 查询到模板条带数4 - 输入偶数，不作变动
                    编辑已有虚拟机集群 - 节点组
                        存储 - 查询到模板条带数8 - 增加info icon，hover展示tooltip
                        存储 - 查询到模板条带数4 - 无增加info icon，hover展示tooltip
                        存储 - 查询到模板条带数8 - 修改为奇数，onchange判定，强制tooltip进入hover状态，blur自动向上取偶 - 创建成功
                        存储 - 查询到模板条带数8 - 修改为奇数，blur自动向上取偶 - 创建成功后检查虚拟机volume的数值，向上取偶后的数值
                        存储 - 查询到模板条带数8 - 修改为偶数，不作变动 - 保存后修改成功 - 原地更新
                        存储 - 查询到模板条带数4 - 修改为奇数，数值不作变动 - 保存成功
                        存储 - 查询到模板条带数4 - 修改为偶数，数值不作变动 - 保存成功
                持久卷申领
                    创建持久卷申领 - UI表单
                        创建pvc - 字段变更 - 「分配量」->「申请量」
                        创建pvc - 字段变更 - 「分配量」->「申请量」- UI表单切换到yaml
                        ELF-CSI - 创建pvc - 模板条带数8 - 分配量输入奇数 - 创建成功后检查对应volume的容量，向上取偶后的数值
                        ELF-CSI - 创建pvc - 模板条带数8 - 分配量输入偶数，不做变更 - 创建成功后检查对应volume的容量，与设置的数值保持一致
                        ELF-CSI - 创建pvc - 模板条带数4 - 分配量输入奇数，不做变更，创建成功后对应volume的容量与设置的数值保持一致
                        ELF-CSI - 创建pvc - 模板条带数4 - 分配量输入偶数，不做变更，创建成功后对应volume的容量与设置的数值保持一致
                        ZBS-CSI - 创建pvc - 模板条带数4 - 分配量输入奇数，不做变更，创建成功后对应volume的容量与设置的数值保持一致
                        ZBS-CSI - 创建pvc - 模板条带数4 - 分配量输入偶数，不做变更，创建成功后对应volume的容量与设置的数值保持一致
                        ZBS-CSI - 创建pvc - 模板条带数8 - 分配量输入奇数 - 创建成功后检查对应volume的容量，向上取偶后的数值
                        ZBS-CSI - 创建pvc - 模板条带数8 - 分配量输入偶数，不做变更 - 创建成功后检查对应volume的容量，与设置的数值保持一致
                    持久卷申领详情 - 分配容量
                        持久卷详情页 - pvc分配容量 - 字段取值更新：status.capacity.storage
                        pvc列表 - 新增字段 - 申请容量（Requested capacity）- 取值spec.resources.requests.storage
                        pvc详情页 - 新增「申请量」显示在「分配量」之后，申请量支持编辑，分配量不支持编辑
                        pvc详情页 - 新增「申请量」- 点击编辑 - 弹出「编辑申请量」弹窗
                        ELF-CSI - 编辑pvc分配量 - 模板条带数8 - 输入奇数 - 成功后检查对应volume的容量，向上取偶后的数值
                        ELF-CSI - 编辑pvc分配量 - 模板条带数8 - 输入偶数，不做变更 - 创建成功后检查对应volume的容量，与设置的数值保持一致
                        ELF-CSI - 编辑pvc分配量 - 模板条带数4 - 输入奇数，不做变更，编辑成功后对应volume的容量与设置的数值保持一致
                        ELF-CSI - 编辑pvc分配量 - 模板条带数4 - 输入偶数，不做变更，编辑成功后对应volume的容量与设置的数值保持一致
                        ZBS-CSI - 编辑pvc分配量 - 模板条带数8 - 输入奇数 - 成功后检查对应volume的容量，向上取偶后的数值
                        ZBS-CSI - 编辑pvc分配量 - 模板条带数8 - 输入偶数，不做变更 - 创建成功后检查对应volume的容量，与设置的数值保持一致
                        ZBS-CSI - 编辑pvc分配量 - 模板条带数4 - 输入奇数，不做变更，创建成功后对应volume的容量与设置的数值保持一致
                        ZBS-CSI - 编辑pvc分配量 - 模板条带数4 - 输入偶数，不做变更，创建成功后对应volume的容量与设置的数值保持一致
                持久卷
                    创建持久卷 - yaml/导入yaml/kubectl apply -f
                        新建自定义pv - 不选择CSI - 容量输入奇数 - UI不限制，创建成功,实际创建volume与设置数值一致
                        新建自定义pv - 不选择CSI - 容量输入偶数 - UI不限制，创建成功,实际创建volume与设置数值一致 --- TBD
                        ELF-CSI - 新建自定义pv - 模板条带数8 - 容量输入奇数 - UI不限制，创建成功，实际创建的pv容量自动向上取偶
                        ELF-CSI - 新建自定义pv - 模板条带数8 - 容量输入偶数 - 创建成功，实际创建的volume容量与设置数值保持一致
                        ELF-CSI - 新建自定义pv - 模板条带数4 - 输入奇数，不做变更，创建成功后对应volume的容量与设置的数值保持一致
                        ELF-CSI - 新建自定义pv - 模板条带数4 - 输入偶数，不做变更，创建成功后对应volume的容量与设置的数值保持一致
                        ZBS-CSI - 新建自定义pv - 模板条带数8 - 分配量输入奇数 - UI不限制，创建成功，实际创建的pv容量自动向上取偶
                        ZBS-CSI - 新建自定义pv - 模板条带数8 - 分配量输入偶数 - 创建成功，实际创建的pv容量与pvc分配量保持一致
                        ZBS-CSI - 新建自定义pv - 模板条带数4 - 输入奇数，不做变更，创建成功后对应volume的容量与设置的数值保持一致
                        ZBS-CSI - 新建自定义pv - 模板条带数4 - 输入偶数，不做变更，创建成功后对应volume的容量与设置的数值保持一致
                    编辑持久卷 - 持久卷详情页 - 编辑yaml
                        新建自定义pv - 不选择CSI - 容量编辑为奇数 - UI不限制，保存成功后实际创建volume与设置数值一致 --- TBD
                        新建自定义pv - 不选择CSI - 容量编辑为偶数 - UI不限制，保存成功后实际创建volume与设置数值一致 --- TBD
                        ELF-CSI - 编辑pv容量 - 模板条带数8 - 输入偶数 - 保存成功后，实际创建的volume容量与设置数值保持一致
                        ELF-CSI - 编辑pv容量 - 模板条带数8 - 输入奇数 - 保存成功后，实际创建的volume容量向上取偶
                        ELF-CSI - 编辑pv容量 - 模板条带数4 - 输入偶数 - 保存成功后，实际创建的volume容量与设置数值保持一致
                        ELF-CSI - 编辑pv容量 - 模板条带数4 - 输入奇数 - 保存成功后，实际创建的volume容量与设置数值保持一致
                        ZBS-CSI - 编辑pv容量 - 模板条带数8 - 输入偶数 - 保存成功后，实际创建的volume容量与设置数值保持一致
                        ZBS-CSI - 编辑pv容量 - 模板条带数8 - 输入奇数 - 保存成功后，实际创建的volume容量向上取偶
                        ZBS-CSI - 编辑pv容量 - 模板条带数4 - 输入偶数 - 保存成功后，实际创建的volume容量与设置数值保持一致
                        ZBS-CSI - 编辑pv容量 - 模板条带数4 - 输入偶数 - 保存成功后，实际创建的volume容量与设置数值保持一致
                容器镜像仓库
                    创建容器镜像仓库 - 资源配置
                        数据盘容量 - 查询到模板条带数8 - 增加info icon，hover展示tooltip
                        数据盘容量 - 查询到模板条带数4 - 无增加info icon，hover展示tooltip
                        数据盘容量 - 查询到模板条带数8 - 输入奇数，onchange判定，强制tooltip进入hover状态，blur自动向上取偶 - 创建成功
                        数据盘容量 - 查询到模板条带数8 - 输入奇数，blur自动向上取偶 - 创建成功后检查虚拟机volume的数值，向上取偶后的数值
                        数据盘容量 - 查询到模板条带数8 - 输入奇数，blur自动向上取偶，再修改为其他偶数 - 不做变动
                        数据盘容量 - 查询到模板条带数8 - 输入偶数，不作变动
                        数据盘容量 - 查询到模板条带数4 - 输入偶数，不作变动
                        数据盘容量 - 查询到模板条带数4 - 输入奇数，不作变动
                    编辑容器镜像仓库 - 磁盘
                        数据盘容量 - 查询到模板条带数8 - 增加info icon，hover展示tooltip
                        数据盘容量 - 查询到模板条带数4 - 无增加info icon，hover展示tooltip
                        数据盘容量 - 查询到模板条带数8 - 输入奇数，onchange判定，强制tooltip进入hover状态，blur自动向上取偶 - 创建成功
                        数据盘容量 - 查询到模板条带数8 - 输入偶数，不作变动
                        数据盘容量 - 查询到模板条带数4 - 输入偶数，不作变动 - 无相关tootip提示
                        数据盘容量 - 查询到模板条带数4 - 输入奇数，不作变动
                升级工作负载集群
                    工作负载集群 - 4条带模板，worker节点组存储为奇数 - 升级为4条带模板 - 升级成功，无Notice Tip展示
                    工作负载集群 - 4条带模板，worker节点组存储为奇数 - 升级为8条带模板 - 升级弹窗有Notice Tip展示，此时升级按钮禁用
                    工作负载集群 - 4条带模板，worker节点组存储为偶数 - 升级为4条带模板 - 升级成功，无Notice Tip展示
                    工作负载集群 - 4条带模板，worker节点组存储为偶数 - 升级为8条带模板 - 升级弹窗无Notice Tip展示，可升级成功
                    工作负载集群 - 4条带模板，worker节点组存储为奇数 - 升级为8条带模板 - 升级弹窗有Notice Tip展示，此时升级按钮禁用 - 勾选checkbox后，升级按钮解除禁用
                    工作负载集群 - 4条带模板，worker节点组存储为奇数 - 升级为8条带模板 - 升级弹窗中勾选checkbox，升级成功后查看worker节点组存储 - 向上取偶
                    工作负载集群 - 升级Tip调整，「不支持跨次版本升级」Tip调整至选择框上方
            日志与事件
                日志 - 创建pvc - 日志中可以查看相关日志
                日志 - 编辑pvc - 日志中可以查看相关日志
                事件 - 创建pvc - 事件中可以查看相关事件
                事件 - 编辑pv/pvc - 事件中可以查看相关日志
            discard
                ELF-CSI - 创建pvc - 模板条带数8 - 分配量字段后增加info icon，hover展示tooltip
                ELF-CSI - 创建pvc - 模板条带数4 - 分配量字段后无增加info icon
                ELF-CSI - 创建pvc - 模板条带数8 - 分配量输入奇数，onchange判定，强制tooltip进入hover状态，blur自动向上取偶 - 创建成功
                ZBS-CSI - 创建pvc - 模板条带数8 - 分配量字段后增加info icon，hover展示tooltip
                ZBS-CSI - 创建pvc - 模板条带数4 - 分配量字段后无增加info icon
                ZBS-CSI - 创建pvc - 模板条带数8 - 分配量输入奇数，onchange判定，强制tooltip进入hover状态，blur自动向上取偶 - 创建成功
                ELF-CSI - 编辑pvc分配量 - 模板条带数8 - 分配量字段后增加info icon，hover展示tooltip
                ELF-CSI - 编辑pvc分配量 - 模板条带数4 - 分配量字段后无增加info icon
                ELF-CSI - 编辑pvc分配量 - 模板条带数8 - 输入奇数，onchange判定，强制tooltip进入hover状态，blur自动向上取偶 - 保存成功
                ZBS-CSI - 编辑pvc分配量 - 模板条带数8 - 分配量字段后增加info icon，hover展示tooltip
                ZBS-CSI - 编辑pvc分配量 - 模板条带数4 - 分配量字段后无增加info icon
    SKS-4169 升级nvidia-gpu-operator，适配rocky9.x系统
        升级GPU驱动版本 - GPU：580.126.09 ，cuda13.0
        升级GPU驱动版本 - vGPU：SMTX620匹配版本 550.127.05 
CUDA 12.4
        升级GPU驱动版本 - vGPU - SKS集群创建在低于620版本的集群上并开启vGPU - 开启失败，vgpu要求版本必须匹配
        vGPU - 集群需要配置合法的vGPU license - 新建集群/升级后不受影响
        升级驱动版本 - 虚拟机集群-GPU - SKS1.6默认驱动版本 570.195.03-rocky9.6升级到更新的 580.126.09-rocky9.7 - 升级成功
        升级驱动版本 - 虚拟机集群-vGPU - SKS1.6默认驱动更新，版本保持 550.127.05-rocky9.7 - 升级成功
        升级驱动版本 - 物理机集群 - SKS1.6默认驱动版本 570.195.03 升级到更新的 580.126.09 - 升级成功
        集群中所有GPU卡均被使用 - 重启nvidia-driver-xx daemonset - 预期自动驱逐节点上的GPU负载，完成驱动安装后自动重新调度
        SKS1.6新建工作负载集群
            新建虚拟机集群（rocky9.x）
                创建前未上传新驱动镜像 - 新建集群k8sv1.26～28 - 创建时开启GPU - GPU operator无法开启有提示
                创建前未上传新驱动镜像 - 新建集群k8sv1.26～28 - 创建后配置GPU，插件部分开启GPU operator - GPU operator无法开启有提示
                创建前未上传新驱动镜像 - 新建集群k8sv1.29～31 - 创建时默认开启GPU - GPU operator加载新驱动无法ready
                创建前未上传新驱动镜像 - 新建集群k8sv1.29～31 - 创建后开启GPU - GPU operator加载新驱动无法ready
                新建集群k8sv1.29～31 - 创建时开启GPU - GPU operator加载新驱动无法ready - 上传新版驱动镜像 - operator加载新驱动成功，25.3.4
                创建前未上传新驱动镜像 - 新建集群k8sv1.26～28 - 创建时开启vGPU - GPU operator无法开启有提示
                创建前未上传新驱动镜像 - 新建集群k8sv1.26～28 - 创建后插件部分开启vGPU - GPU operator按钮禁用，无法开启有提示：仅支持 Kubernetes 版本为 1.29 及以上的集群。
                创建前未上传新驱动镜像 - 新建集群k8sv1.29～31 - 创建时开启vGPU - GPU operator加载新驱动无法ready
                创建前未上传新驱动镜像 - 新建集群k8sv1.29～31 - 创建后开启vGPU - GPU operator加载新驱动无法ready
                新建集群k8sv1.29～31 - 创建时开启vGPU - GPU operator加载新驱动无法ready - 上传新版驱动镜像 - operator加载新驱动成功
                创建前已上传新驱动镜像 - 新建集群k8sv1.26～28 - 创建时开启GPU - GPU operator无法开启
                创建前已上传新驱动镜像 - 新建集群k8sv1.26～28 - 创建后插件部分开启GPU - GPU operator无法开启有提示
                创建前已上传新驱动镜像 - 新建集群k8sv1.29～31-rocky9.6 - 创建时开启GPU - GPU operator开启成功，新operator加载新版驱动 - GPU：580.126.09 ，cuda12.8
                创建前已上传新驱动镜像 - 新建集群k8sv1.29～31-rocky9.7 - 创建后开启GPU - GPU operator开启成功，新operator加载新版驱动 - GPU：580.126.09 ，cuda13.0
                创建前已上传新驱动镜像 - 新建集群k8sv1.26～28 - 创建时开启vGPU - GPU operator无法开启
                创建前已上传新驱动镜像 - 新建集群k8sv1.26～28 - 创建后插件部分开启vGPU - GPU operator无法开启有提示
                创建前已上传新驱动镜像 - 新建集群k8sv1.29～31-rocky9.7 - 创建时开启vGPU - GPU operator开启成功，新operator加载新版驱动 - 550.127.05，CUDA 12.4
                创建前已上传新驱动镜像 - 新建集群k8sv1.29～31-rocky9.6 - 创建后开启vGPU - GPU operator开启成功，新operator加载新版驱动 - 550.127.05，CUDA 12.4
                创建前已上传新驱动镜像 - 新建集群k8sv1.29～31 - 创建后开启vGPU - GPU operator开启成功，新operator加载新版驱动 - 检查license正常配置成功
                新建集群k8sv1.29～31 - 创建时开启GPU - operator加载新驱动成功 - 关闭operator - 关闭成功
                新建集群k8sv1.29～31 - 创建后开启vGPU - operator加载新驱动成功 - 关闭operator - 关闭成功
                新建集群k8sv1.29～31 - 创建时开启GPU - operator加载新驱动成功 - 删除开启operator的集群 - 删除成功
                新建集群k8sv1.29～31 - 创建后开启vGPU - operator加载新驱动成功 - 关闭operator后重新开启 - 开启成功，加载新驱动成功
            新建物理机集群（rocky9.x）
                创建前未上传新驱动镜像 - 新建集群k8sv1.29～31 - 创建时开启GPU - GPU operator加载新驱动无法ready
                创建前未上传新驱动镜像 - 新建集群k8sv1.29～31 - 创建后开启GPU - GPU operator加载新驱动无法ready
                新建集群k8sv1.29～31 - 创建时开启GPU - GPU operator加载新驱动无法ready - 上传新版驱动镜像 - operator加载新驱动成功
                创建前已上传新驱动镜像 - 新建集群k8sv1.29～31-rocky9.7 - 创建时开启GPU - GPU operator开启成功，新operator加载新版驱动 - GPU：580.126.09 ，cuda13.0
                创建前已上传新驱动镜像 - 新建集群k8sv1.29～31-rocky9.7 - 创建后开启GPU - GPU operator开启成功，新operator加载新版驱动 - GPU：580.126.09 ，cuda13.0
                新建集群k8sv1.29～31 - 创建时开启GPU - operator加载新驱动成功 - 关闭operator - 关闭成功
                新建集群k8sv1.29～31 - 配置GPU - operator开启后关闭 - 关闭成功后检查节点上nvidia模版是否有残留lsmod | grep nvidia
                新建集群k8sv1.29～31 - 创建后开启GPU - operator加载新驱动成功 - 删除开启operator的集群 - 删除成功
                新建集群k8sv1.29～31 - 创建后开启GPU - operator加载新驱动成功 - 删除开启operator的集群 - 删除成功,检查gpu节点有nvidia模块残留，手动卸载或者重启节点
                新建集群k8sv1.29～31 - kylin/openeuler - 开启operator - 匹配不到驱动，使用默认值（rocky9.6驱动）- 驱动安装失败
            新建物理机集群（rocky8.10）
                创建前未上传新驱动镜像 - 新建集群k8sv1.29～31 - 创建时开启GPU - GPU operator正常开启，新operator加载旧驱动 - 535
                创建前未上传新驱动镜像 - 新建集群k8sv1.29～31 - 创建后开启GPU - GPU operator正常开启，新operator加载旧驱动 - 535
                创建前已上传新驱动镜像 - 新建集群k8sv1.29～31 - 创建时开启GPU - GPU operator正常开启，新operator加载旧驱动 - 535
                创建前已上传新驱动镜像 - 新建集群k8sv1.29～31 - 创建后开启GPU - GPU operator正常开启，新operator加载旧驱动 - 535
                新建集群k8sv1.29～31 - 创建后开启GPU - GPU operator正常开启，新operator加载旧驱动 - 关闭operator - 关闭成功
                新建集群k8sv1.29～31 - 创建后开启GPU - GPU operator正常开启，新operator加载旧驱动 - 删除集群 - 删除成功，gpu相关清理干净，物理机节点释放可再次使用
                新建集群k8sv1.29～31 - 新建后开启gpu-operator - 升级worker节点系统版本到rocky9.x - 升级后需要手动重新初始化 serverInstance - 升级后新operator加载新驱动
        已有工作负载集群
            虚拟机集群
                升级SKS1.6前低于1.29版本，且rocky8.10及以下
                    升级前已开启 operator
                        升级后 - 检查集群pkgi已暂停，GPU operator组件和GPU负载运行不受影响
                        升级后未上传1.6驱动镜像 - 暂停GPU operator addon保持当前继续用旧的驱动，addon的annotation中有特定标记
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭operator - 关闭成功，operator相关清理，会残留/run/nvidia/driver 挂载点
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭后再开启 - 不支持启用按钮下有提示：仅支持Kubernetes版本为1.29及以上的集群。
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 直接升级k8s版本到v1.29及以上 - 自动解除暂停并升级为新版operator,但operator不ready
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭后再升级k8s版本到v1.29及以上 - 升级成功，operator可再次开启，operator ImagePullBackOff
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭后再升级k8s版本到v1.29以下但rocky9.7 - 升级成功后operator addon保持暂停
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭后再升级k8s版本到v1.29及以上但升级为rocky9.x - 升级成功后operator开启成功，新operator不ready
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动，addon的annotation中有特定标记
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭operator - 关闭成功，operator相关清理
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭后再开启 - 不支持有提示：仅支持Kubernetes版本为1.29及以上的集群。
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 直接升级k8s版本到v1.29及以上且rocky9.x - 自动解除暂停并升级为新版operator
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 直接升级k8s版本到v1.29及以上且rocky8.10 - 保持新operator加载旧驱动
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭后再升级k8s版本到v1.29及以上且rocky9.x - 升级成功，operator可再次开启，新operator加载新驱动
                    升级前未开启 operator
                        升级后未上传1.6驱动镜像 - rocky810+k8s-v1.29以下 - 插件配置页面不支持开启gpu-operator - 启用按钮下有提示：仅支持Kubernetes版本为1.29及以上的集群。
                        升级后未上传1.6驱动镜像 - 升级k8s版本低于v1.29+但是rocky9.7 - 不支持开启，开启按钮有禁用文案
                        升级后未上传1.6驱动镜像 - 升级k8s版本v1.29+但是rocky9.x - 支持开启，新operator加载新驱动，但operator不ready
                        升级后已上传1.6驱动镜像 - 插件配置页面不支持开启gpu-operator - 启用按钮下有提示：仅支持Kubernetes版本为1.29及以上的集群。
                        升级后已上传1.6驱动镜像 - 升级k8s版本v1.29+但是rocky8.10 - 支持开启，新operator加载旧驱动
                        升级后已上传1.6驱动镜像 - 升级k8s版本v1.29+且rocky9.7 - 支持开启，新operator加载新驱动
                升级SKS1.6前1.29及以上版本但rocky8.10及以下
                    升级前已开启 operator
                        升级后未上传1.6驱动镜像 - GPU operator组件自动更新加载旧驱动，gpu负载会被自动驱逐重建
                        升级后未上传1.6驱动镜像 - 关闭operator - 关闭成功，operator相关清理
                        升级后未上传1.6驱动镜像 - 关闭后再开启 - 支持开启且新operator加载旧驱动，但未上传1.6GPU包，gpu所有pod ImagePullBackOff
                        升级后未上传1.6驱动镜像 - 直接升级节点系统版本到rocky9.6 - 升级后新operator自动更新加载新驱动，但operator不ready
                        升级后未上传1.6驱动镜像 - 关闭operator后升级节点系统版本到rocky9.6 - 升级后新operator可开启，加载新驱动，但operator不ready
                        升级后已上传1.6驱动镜像 - GPU operator组件自动更新加载旧驱动
                        升级后已上传1.6驱动镜像 - 关闭operator - 关闭成功，operator相关清理
                        升级后已上传1.6驱动镜像 - 关闭后再开启 - 支持开启，新operator加载旧驱动
                        升级后已上传1.6驱动镜像 - 直接升级节点系统版本到rocky9.6 - 升级后新operator自动更新加载新驱动
                        升级后已上传1.6驱动镜像 - 关闭operator后升级节点系统版本到rocky9.7 - 升级后新operator可开启，加载新驱动
                    升级前未开启operator
                        升级后未上传1.6驱动镜像 - 允许开启operator，GPU operator加载旧驱动，但operator不ready
                        升级后未上传1.6驱动镜像 - 直接升级节点系统版本到rocky9.6 - 升级后新operator自动更新加载新驱动，但operator不ready
                        升级后已上传1.6驱动镜像 - 允许开启operator，GPU operator加载旧驱动
                        升级后已上传1.6驱动镜像 - 直接升级节点系统版本到rocky9.6 - 升级后新operator自动更新加载新驱动
            物理机集群
                升级SKS1.6前低于1.29版本，且rocky8.10及以下
                    升级前已开启 operator
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭operator - 关闭成功，operator相关清理
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭后再开启 - 启用按钮不支持开启有提示：仅支持Kubernetes版本为1.29及以上的集群。
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 直接升级k8s版本到v1.29及以上 - 自动解除暂停并升级为新版operator,但operator不ready
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭后再升级k8s版本到v1.29及以上但worker保持rocky8.10 - 升级成功后operator开启成功，新operato加载旧驱动
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭operator - 关闭成功，operator相关清理
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭后再开启 - 启用按钮不支持开启有提示：仅支持Kubernetes版本为1.29及以上的集群。
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 直接升级k8s版本到v1.29及以上且rocky8.10 - 保持新operator加载旧驱动
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭后再升级k8s版本到v1.29及以上且worker升级rocky9.x - 升级成功后operator开启成功，新operato加载新驱动
                    升级前未开启 operator
                        升级后未上传1.6驱动镜像 - 插件配置页面不支持开启gpu-operator - 有提示：仅支持Kubernetes版本为1.29及以上的集群。
                        升级后未上传1.6驱动镜像 - 升级k8s版本v1.29+且升级worker节点系统为rocky9.x - 支持开启，新operator加载新驱动，但operator不ready
                        升级后已上传1.6驱动镜像 - 插件配置页面不支持开启gpu-operator - 有提示：仅支持Kubernetes版本为1.29及以上的集群。
                        升级后已上传1.6驱动镜像 - 升级k8s版本v1.29+但是rocky8.10 - 支持开启，新operator加载旧驱动
                        升级后已上传1.6驱动镜像 - 升级k8s版本v1.29+且升级worker节点系统版本为rocky9.x - 支持开启，新operator加载新驱动
                升级SKS1.6前1.29及以上版本，但rocky8.10及以下
                    升级前已开启 operator
                        升级后未上传1.6驱动镜像 - GPU operator自动更新加载旧驱动
                        升级后未上传1.6驱动镜像 - 关闭后再开启 - 支持开启且新operator加载旧驱动
                        升级后未上传1.6驱动镜像 - 直接升级worker节点系统版本到rocky9.6 - 升级后新operator自动更新，节点就绪后使用新驱动，但operator不ready
                        升级后已上传1.6驱动镜像 - GPU operator自动更新加载旧驱动
                        升级后已上传1.6驱动镜像 - 关闭后再开启 - 支持开启，新operator加载旧驱动
                        升级后已上传1.6驱动镜像 - 关闭operator后升级worker节点系统版本到rocky9.6 - 升级后新operator可开启，加载新驱动
                    升级前未开启 operator
                        升级后未上传1.6驱动镜像 - 允许开启operator，GPU operator加载旧驱动
                        升级后未上传1.6驱动镜像 - 允许开启operator，GPU operator加载旧驱动 - 开启后关闭 - 关闭成功
                        升级后未上传1.6驱动镜像 - 直接升级worker节点系统版本到rocky9.6 - 升级后新operator自动更新加载新驱动，但operator不ready
                        升级后已上传1.6驱动镜像 - 允许开启operator，GPU operator加载旧驱动
                        升级后已上传1.6驱动镜像 - 允许开启operator，GPU operator加载旧驱动 - 开启后关闭再开启 - 不升级worker节点系统，保持新operator加载旧驱动
                        升级后已上传1.6驱动镜像 - 直接升级worker节点系统版本到rocky9.6 - 升级后新operator自动更新加载新驱动
                升级SKS1.6前1.29及以上版本，且rocky9.7
                    升级前已开启 operator
                        升级后未上传1.6驱动镜像 - 升级后新operator自动更新加载新驱动，但operator不ready
                        升级后已上传1.6驱动镜像 - 升级后新operator自动更新加载新驱动
                        升级后已上传1.6驱动镜像 - 升级后新operator自动更新加载新驱动 - 升级k8s版本 - 驱动加载不受影响
                        升级后已上传1.6驱动镜像 - 手机后关闭后再开启 - 支持开启，新operator加载新驱动
                    升级前未开启 operator
                        升级后未上传1.6驱动镜像 - 允许开启operator，GPU operator加载新驱动，operator不ready
                        升级后已上传1.6驱动镜像 - 允许开启operator，GPU operator加载新驱动
                升级SKS1.6前低于1.29版本，但rocky8.10以上
                    升级前已开启 operator
                        升级后未上传1.6驱动镜像 - 暂停GPU operator addon保持当前继续用旧的驱动
                        升级后未上传1.6驱动镜像 - 暂停GPU operator addon保持当前继续用旧的驱动 - 检查集群UI概览页集群插件状态card中gpu-operator paused状态
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭operator - 关闭成功，operator相关清理
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭后再开启 - 不支持有提示：仅支持Kubernetes版本为1.29及以上的集群。
                        升级后未上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 直接升级k8s版本到v1.29及以上 - 自动解除暂停并升级为新版operator,但operator不ready --TBD
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭operator - 关闭成功，operator相关清理
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 关闭后再开启 - 不支持有提示：仅支持Kubernetes版本为1.29及以上的集群。
                        升级后已上传1.6驱动镜像 - 暂停GPU operator 保持当前继续用旧的驱动 - 升级k8s版本到v1.29及以上 - 升级GPU operator 解除addon暂停，更新operator并使用新版驱动，GPU负载自动重新调度运行
                    升级前未开启 operator
                        升级后未上传1.6驱动镜像 - 插件配置页面不支持开启gpu-operator - 有提示：仅支持Kubernetes版本为1.29及以上的集群。
                        升级后未上传1.6驱动镜像 - 升级k8s版本v1.29+但rocky8.10 - 支持开启，新operator加载旧驱动 --- TBD
                        升级后已上传1.6驱动镜像 - 插件配置页面不支持开启gpu-operator - 有提示：仅支持Kubernetes版本为1.29及以上的集群。
                        升级后已上传1.6驱动镜像 - 升级k8s版本v1.29+且rocky9.x - 支持开启，新operator加载新驱动
        已有功能影响
            监控
                虚拟机集群
                    集群开启监控后 - gpu-operator相关监控图表数据正常展示
                    集群开启监控后 - 升级前开启监控，升级后数据图表正常展示
                    集群开启监控后 - 升级前开启operator，升级后自动切换新版驱动后，图表数据正常展示
                物理机集群
                    集群开启监控后 - gpu-operator相关监控图表数据正常展示
                    集群开启监控后 - 升级前开启监控，升级后数据图表正常展示
                    集群开启监控后 - 升级前开启operator，升级后自动切换新版驱动后，图表数据正常展示
            报警
                新增报警规则 - 集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中 NVIDIA GPU Operator 的组件 {{ $labels.deployment }}{{ $labels.daemonset }} 异常持续 15 分钟。 注意  15m
                报警规则列表检查新增报警规则 - 集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中 NVIDIA GPU Operator 的组件 {{ $labels.deployment }}{{ $labels.daemonset }} 异常持续 15 分钟。
                触发报警规则 - 集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中 NVIDIA GPU Operator 的组件 {{ $labels.deployment }}{{ $labels.daemonset }} 异常持续 15 分钟。
        UI改动
            新建集群版本低于1.29 - 不可开启NVIDIA GPU Operator - 开启按钮禁用，有提示
            新建集群版本1.29及以上 - 可开启NVIDIA GPU Operator - 开启按钮不禁用，无提示
            已有集群 - 版本从低于1.29升级到1.29及以上 - 可开启NVIDIA GPU Operator - 开启按钮不禁用，禁用提示消失
            新建虚拟机集群低于1.29 - 不配置GPU - 成功后新建节点组 - 配置GPU - Notice Tip更新 - 创建成功，但是operator无法自动开启 - 插件页面operator保持关闭且有提示
            新建虚拟机集群低于1.29 - 不配置vGPU - 成功后新建节点组 - 配置vGPU - Notice Tip更新 - 创建成功，但是operator无法自动开启 - 插件页面operator保持关闭且有提示
            新建虚拟机集群低于1.29 - 不配置GPU - 成功后编辑已有节点组 - 切换为配置GPU - Notice Tip更新 - 保存成功，但是operator无法自动开启 - 插件页面operator保持关闭且有提示
            新建虚拟机集群低于1.29 - 不配置vGPU - 成功后编辑已有节点组 - 切换为配置vGPU - Notice Tip更新 - 保存成功，但是operator无法自动开启 - 插件页面operator保持关闭且有提示
            新建虚拟机集群低于1.29 - 不配置GPU - 成功后升级k8s版本1.29及以上后 - 切换为配置GPU - Notice Tip保持 - 切换成功后operator自动开启 - 插件页面operator开启
            新建虚拟机集群低于1.29 - 配置vGPU但未开启operator - 升级至1.29及以上成功后 - operator保持关闭 - 插件页面operator可开启，没有禁用文案
            新建虚拟机集群1.29及以上 - 不配置GPU - 创建后已有节点组切换为配置GPU - Notice Tip:配置硬件加速器资源后将自动开启 NVIDIA GPU Operator 插件。 - 切换成功后operator自动开启 - 插件页面operator开启
            新建虚拟机集群1.29及以上 - 不配置vGPU - 创建成功后切换为配置vGPU - Notice Tip:配置硬件加速器资源后将自动开启 NVIDIA GPU Operator 插件。需在插件中配置 vGPU license，否则将影响 vGPU 功能的使用。 - 保存成功，operator自动开启 - 插件页面operator开启
    1.6改进
        SKS-2748 使用ZBS CSI删除集群后，产生的iscsi target需要被清理
            删除SKS流程变更 - 删除pvc清理lun（开启监控，grafana pvc）->csi-driver 确定 target 中无 lun 以后清理 target -> 删除 sks
            删除SKS流程变更（未开启监控）- 删除pvc清理lun->csi-driver 确定 target 中无 lun 以后清理 target -> 删除 sks - 省略前两步直接删除SKS
            卸载SKS流程变更 - 删除pvc清理lun（开启监控，grafana pvc）->csi-driver 确定 target 中无 lun 以后清理 target -> 卸载sks
            删除SKS流程变更 - 删除pvc清理lun（用户自创建pvc）->csi-driver 确定 target 中无 lun 以后清理 target（SKS集群与存储在同一个tower） -> 删除sks
            zbs-csi集群（OS集群开启块存储）与SKS集群在同一个tower - 删除SKS集群 - 删除成功后，自动清理产生的iscsi target
            zbs-csi集群（ZBS集群）与SKS集群在同一个tower - 删除SKS集群 - 删除成功后，自动清理产生的iscsi target
            zbs-csi集群（ZBS集群）与SKS集群在不同的tower - 用户创建的pvc-删除SKS集群 - 删除成功后，不会自动清理产生的iscsi target以及lun
            zbs-csi集群与SKS集群在不同的tower - 删除SKS物理机集群 - 删除成功后，不会自动清理产生的iscsi target和lun，需要手动清理
            删除SKS - zbs集群(同一个tower) - 用户创建pv，删除集群后，pv对应的lun在相应集群中随删除清理
            删除SKS - OS集群(同一个tower) - 用户创建pv，删除集群后，pv对应的lun在相应集群中随删除清理
            删除SKS - zbs/OS集群 - SKS创建pv+用户创建pv，删除集群后，所有pv对应的lun在相应集群中随删除清理，使用的target也一并清理成功
        SKS-4036 优化插件、节点数量展示 + 新增插件报警
            管控集群概览页面 - UI - 查看管控集群插件状态card - 启用的addon以及状态展示以及规则调整
            工作负载集群概览页面 - UI - 查看集群插件状态card - 启用的addon以及状态展示以及规则调整
            工作负载集群列表 - UI - 对「x/y」类型数量展示优化 - controlplane节点数量 - 「已就绪/总数」
            工作负载集群列表 - UI - 对「x/y」类型数量展示优化 - worker节点数量 - 「已就绪/总数」
            工作负载集群列表 - UI - 对「x/y」类型数量展示优化 - 插件数量 - 「已就绪/总数」
            新增报警规则 - 集群 {{ $labels.cluster }} 的名字空间 {{ $labels.namespace }} 中节点组自动伸缩的组件 {{ $labels.deployment }}{{ $labels.daemonset }}{{ $labels.statefulset }} 异常持续 15 分钟。
        项目计划未单列的改进 ticket
            SKS-3161 部署容器镜像仓库增加子网掩码校验
                1.6改进 - SKS3161 - 创建容器镜像仓库，子网掩码输入符合 IP 规范，但不满足掩码规范的 IP 值，报格式错
                1.6改进 - SKS3161 - 创建容器镜像仓库，子网掩码输入 0.0.0.0，报格式错
                1.6改进 - SKS3161 - 创建容器镜像仓库，子网掩码输入 255.255.255.255，可接受，不报错
            SKS-4065 虚拟机模板升级 containerd 版本至 1.7.28
                1.6改进 - containerd 升级 - rocky 9.6 x86 节点虚拟机模板中 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - openeuler 22.03 x86 节点虚拟机模板中 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - openeuler 22.03 aarch64 节点虚拟机模板中 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - tencentOS 3.3 x86 节点虚拟机模板中 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - tencentOS 3.3 aarch64 节点虚拟机模板中 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - kylin v10 x86 节点虚拟机模板中 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - kylin v10 aarch64 节点虚拟机模板中 containerd 版本为 1.7.28
            SKS-4066 SKS1.6 模板升级 vmtools 至 4.0.0
                1.6改进 - vmtools版本 - rocky 9.6 x86 vmtools 版本为 4.0.0
                1.6改进 - vmtools版本 - openeuler 22.03 x86 vmtools 版本为 4.0.0
                1.6改进 - vmtools版本 - openeuler 22.03 aarch64 vmtools 版本为 4.0.0
                1.6改进 - vmtools版本 - tencentOS 3.3 x86 vmtools 版本为 4.0.0
                1.6改进 - vmtools版本 - tencentOS 3.3 aarch64 vmtools 版本为 4.0.0
                1.6改进 - vmtools版本 - kylin v10 x86 vmtools 版本为 4.0.0
                1.6改进 - vmtools版本 - kylin v10 aarch64 vmtools 版本为 4.0.0
            SKS-4073 物理机支持 rocky 9 OS
                1.6改进 - rocky9.7物理机 - 可成功添加 rocky 9.7 x86_64 物理机
                1.6改进 - rocky9.7物理机 - 使用 rocky 9.7 x86_64 物理机创建物理机集群，集群创建成功
                1.6改进 - rocky9.7物理机 - 可在 rocky 9.7 x86_64 物理机节点上创建用户负载
                1.6改进 - rocky9.7物理机 - 可从物理机集群中移除 rocky 9.7 x86_64 物理机节点，物理机被成功释放
                1.6改进 - rocky9.7物理机 - 可删除带有 rocky 9.7 x86_64 物理机节点的物理机集群，物理机被成功释放
                1.6改进 - rocky9.7物理机 - 从集群释放的物理机加入不同 K8s 版本的物理机集群，加入节点成功，可在节点上启动用户负载
                1.6改进 - rocky9.7物理机 - 可成功移除 rocky 9.7 x86_64 物理机
            SKS-4087 物理机 containerd 升级 1.7.28
                1.6改进 - containerd 升级 - 新添加 rocky x86物理机 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - 新添加 ubuntu x86物理机 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - 新添加 openeuler x86 物理机 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - 新添加 openeuler aarch64 物理机 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - 新添加 tencentOS x86 物理机 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - 新添加 tencentOS aarch64 物理机 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - 新添加 kylin v10 x86 物理机 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - 新添加 kylin v10 aarch64 物理机 containerd 版本为 1.7.28
                1.6改进 - containerd 升级 - sks 升级1.6，已有的未使用 rocky x86物理机自动触发初始化，containerd 版本更新为 1.7.28
                1.6改进 - containerd 升级 - sks 升级1.6，已有的未使用 ubuntu x86物理机自动触发初始化，containerd 版本更新为 1.7.28
                1.6改进 - containerd 升级 - sks 升级1.6，已有的未使用 openeuler x86物理机自动触发初始化，containerd 版本更新为 1.7.28
                1.6改进 - containerd 升级 - sks 升级1.6，已有的未使用 openeuler aarch64物理机自动触发初始化，containerd 版本更新为 1.7.28
                1.6改进 - containerd 升级 - sks 升级1.6，已有的未使用 kylin v10 x86物理机自动触发初始化，containerd 版本更新为 1.7.28
                1.6改进 - containerd 升级 - sks 升级1.6，已有的未使用 kylin v10 aarch64物理机自动触发初始化，containerd 版本更新为 1.7.28
                1.6改进 - containerd 升级 - sks 升级1.6，已有的已使用的物理机，containerd 版本不变
                1.6改进 - containerd 升级 - sks 升级1.6后，升级集群 K8s 版本，已使用的物理机，containerd 版本更新为 1.7.28
            SKS-4132 [vmTemplate] 优化内核参数
                1.6改进 - 内核参数优化 - rocky 9.6 x86 节点虚拟机模板中内核参数变更检查
                1.6改进 - 内核参数优化 - openeuler 22.03 x86 节点虚拟机模板中内核参数变更检查
                1.6改进 - 内核参数优化 - openeuler 22.03 aarch64 节点虚拟机模板中内核参数变更检查
                1.6改进 - 内核参数优化 - tencentOS 3.3 x86 节点虚拟机模板中内核参数变更检查
                1.6改进 - 内核参数优化 - tencentOS 3.3 aarch64 节点虚拟机模板中内核参数变更检查
                1.6改进 - 内核参数优化 - kylin v10 x86 节点虚拟机模板中内核参数变更检查
                1.6改进 - 内核参数优化 - kylin v10 aarch64 节点虚拟机模板中内核参数变更检查
            SKS-4143 sks-manager 升级 SKS 移除 ecp-adapter 参数
                1.6改进 - 移除 ecp-adapter 组件 - 部署sks，管控集群不再部署 ecp-adapter
                1.6改进 - 移除 ecp-adapter 组件 - 升级 sks1.5 到 1.6，管控集群不再部署 ecp-adapter
            SKS-4180 升级工作负载集群时只能选择当前 majon.minor 版本的模板
                1.6改进 - 升级工作集群，仅提供当前 minor 版本的新模板可选，旧版本模板不再列出
            SKS-4207 1.6 中创建升级物理机集群不再支持选择1.29以下版本的 K8s 版本
                1.6改进 - 物理机集群版本 - 上传1.6 所有版本节点模板，创建物理机集群，可选择的 K8s 版本为 1.29 及以上版本
                1.6改进 - 物理机集群版本 - 上传1.6 所有版本节点模板，升级物理机集群，可选择的 K8s 版本为 1.29 及以上版本
        SKS-4044 Harbor 升级到 2.12
            Harbor2.12 - 新部署 sks registry x86，部署完成 harbor 版本为2.12
            Harbor2.12 - 新部署 sks registry aarch64，部署完成 harbor 版本为2.12
            Harbor2.12 - 升级 sks reistry v1.4.1 x86 到 v1.6.0，harbor 版本更新到 2.12
            Harbor2.12 - 升级 sks reistry v1.4.1 aarch64 到 v1.6.0，harbor 版本更新到 2.12
            Harbor2.12 - 新部署 user registry x86，部署完成 harbor 版本为2.12
            Harbor2.12 - 新部署 user registry aarch64，部署完成 harbor 版本为2.12
        ER版本兼容范围调整为3.2.0及以上
            UI - 部署3.2.0以下版本ER且关联elf集群，创建工作集群时选择该elf集群，CNI中下拉EIC选项禁用，无法选择
            UI - 将3.2.0以下的ER升级至3.2.0+，再次创建工作集群时选择该elf集群，CNI中下拉可选择EIC，EIC集群创建成功，功能正常
            UI - 增加3.2.0+兼容版本提示----文案TBD
            UI - 部署3.2.0+版本ER且关联elf集群，创建工作集群时选择该elf集群，CNI中下拉可选择EIC，EIC集群创建成功，功能正常
            升级 - SKS升级至1.6.0，管控集群中移除ecp-adapter插件
            升级-SKS1.5环境，有部署3.2.0以下版本ER，并创建EIC工作集群，升级SKS1.6前，必须先升级ER至3.2.0以上
            升级-SKS1.5环境，由3.2.0以下版本ER创建的EIC工作集群，升级ER至3.2.0+，再升级SKS1.6，升级成功，集群正常工作
            升级-SKS1.5环境，由3.2.0+版本ER创建的EIC工作集群，升级SKS1.6，升级成功，集群正常工作
            升级-SKS1.5环境，在关联ER集群上创建的calico集群，升级SKS1.6，升级成功，集群正常工作
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - 升级ytt版本，正常
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - 升级k8s版本，正常
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - 增加删除节点，正常
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - 开关obs插件，正常
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - 删除集群，正常
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - e2e测试，正常
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - 编辑EIC IPpool配置，增加IPPOOL，正常
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - 编辑EIC IPpool配置，删除IPPOOL，正常
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - 编辑EIC IPpool配置，修改ip范围，正常
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - 查看控制台，正常
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - 使用工作负载资源，正常
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - 项目管理，正常
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - 同节点pod通信正常
            升级-3.2.0以下ER创建的EIC集群，升级后验证 - 跨节点pod通信正常
            升级-SKS1.5环境，有部署3.2.0以下版本ER，并创建EIC工作集群，若未升级ER至3.2.0+，已升级SKS1.6，查看EIC集群状态---TBD
            升级-SKS1.5环境，有部署3.2.0以下版本ER，并创建EIC工作集群，若未升级ER至3.2.0+，已升级SKS1.6，再升级ER3.2.0+，查看EIC集群是否恢复正常--TBD
            API - SKS1.6环境，使用api在3.2.0以下的ER关联的集群上创建EIC工作集群，是否创建失败，pod间网络不通
            部署 - 新部署的SKS1.6环境，管控集群上不创建ecp-adapter插件
            部署 - 新部署的SKS1.6环境，创建3.2.0+以上ER，创建的EIC集群正常
            部署-3.2.0+以上ER创建的EIC集群-执行原地更新，正常
            部署-3.2.0+以上ER创建的EIC集群-执行增加删除节点，正常
            部署-3.2.0+以上ER创建的EIC集群-升级k8s版本，正常
            部署-3.2.0+以上ER创建的EIC集群-开关obs插件，正常
            部署-3.2.0+以上ER创建的EIC集群-e2e测试，正常
            部署-3.2.0+以上ER创建的EIC集群-编辑EIC IPPOOL配置，增加IPPOOL，正常
            部署-3.2.0+以上ER创建的EIC集群-编辑EIC IPPOOL配置，删除IPPOOL，正常
            部署-3.2.0+以上ER创建的EIC集群-编辑EIC IPPOOL配置，修改ip范围，正常
            部署-3.2.0+以上ER创建的EIC集群-使用控制台，正常
            部署-3.2.0+以上ER创建的EIC集群-测试工作负载资源，正常
            部署-3.2.0+以上ER创建的EIC集群-项目管理，正常
            部署-3.2.0+以上ER创建的Calico集群-工作正常
            架构 - x86环境验证
            架构 - arm环境验证
    SKS 1.6 系统服务及容器镜像仓库支持 Tencent OS、openEuler
        物料支持
            tower/SMTX OS（515-P1）：Tencent - 常规物料 （内置 Rocky/openEuler）-  部署成功，无限制
            tower/SMTX OS：非Tencent（centos） - Tencent OS 专用物料 - 部署成功，无限制
            tower/SMTX OS：非Tencent（open Euler） - Tencent OS 专用物料 - 部署成功
            x86hygon - tower/SMTX OS：非Tencent - 常规物料 （内置 Rocky/openEuler） - 部署registry，管控集群成功{openeuler}
            aarch64鲲鹏 - tower/SMTX OS：非Tencent - 常规物料 （内置 openEuler） - 部署registry（rocky8.9），管控集群成功{openeuler22.03}
            x86 hygon - tower/SMTX OS：Tencent - 管控集群小版本升级 - 升级成功
            aarch64鲲鹏 - tower/SMTX OS：Tencent - 管控集群小版本升级 - 升级成功
            物料支持 - hygon x86/aarch64鲲鹏 - registry安装包 - 增加支持Tencent OS和open Euler（1.6暂不支持）
            物料支持 - hygon x86/aarch64鲲鹏 - 用户容器镜像仓库安装包 - 增加支持Tencent OS和open Euler（1.6暂不支持）
            物料支持 - hygon x86/aarch64鲲鹏 - SKS安装包 - 增加Tencent OS专用 安装包
        新部署SKS1.6 - Tencent os
            tower是Tencent os
                SMTX os是单活Tencent os
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署registry - 部署成功，harbor版本v2.12.2-73072d0d
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 升级registry - 升级成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署管控集群 - 部署成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署registry,管控集群后卸载 - 卸载成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 创建虚拟机工作负载集群 - 创建成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 创建物理机工作负载集群 - 创建成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 删除工作负载集群 - 删除成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署用户容器镜像仓库 - 部署成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 卸载用户容器镜像仓库 - 卸载成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - registry+管控集群 - 导入/拉取镜像正常
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 集群配置用户容器镜像仓库 - 导入/拉取镜像正常
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署registry - 部署成功 - Tencent OS3.3
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 升级registry - 升级成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署管控集群 - 部署成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署registry,管控集群成功后卸载 - 卸载成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 创建虚拟机工作负载集群 - 创建成功
                    鲲鹏 AArch64- 使用Tencent OS Server 3.3物料 - 创建物理机工作负载集群 - 创建成功
                    鲲鹏 AArch64- 使用Tencent OS Server 3.3物料 - 删除工作负载集群 - 删除成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署用户容器镜像仓库 - 部署成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 卸载用户容器镜像仓库 - 卸载成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - registry+管控集群 - 导入/拉取镜像正常
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 集群配置用户容器镜像仓库 - 导入/拉取镜像正常
                    x86 hygon - 常规物料 - registry，SKS服务安装部署 - 部署成功，无限制
                    aarch64鲲鹏 - 常规物料（内置openeuler） - 用户容器镜像仓库安装部署 - 部署成功无限制 - tencentos
                    hygon x86_64 - Registry - 架构不一致 - 向x86集群上传aarch64架构的Tencent os安装包 - 部署失败
                    鲲鹏 AArch64 - Registry - 架构不一致 - 向aarch64集群上传x86架构的tencent os安装包 - 部署失败
                SMTX os是双活Tencent os - SMTXOS-6.2.1
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署registry - 部署成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 升级registry - 升级成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署管控集群 - 部署成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署registry,管控集群后卸载 - 卸载成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 删除工作负载集群 - 删除成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 卸载用户容器镜像仓库 - 卸载成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 创建虚拟机工作负载集群 - 创建成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 创建物理机工作负载集群 - 创建成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署用户容器镜像仓库 - 部署成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - registry+管控集群 - 导入/拉取镜像正常
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 集群配置用户容器镜像仓库 - 导入/拉取镜像正常
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署registry - 部署成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 升级registry - 升级成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署管控集群 - 部署成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署registry,管控集群成功后卸载 - 卸载成功
                    鲲鹏 AArch64- 使用Tencent OS Server 3.3物料 - 删除工作负载集群 - 删除成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 卸载用户容器镜像仓库 - 卸载成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 创建虚拟机工作负载集群 - 创建成功
                    鲲鹏 AArch64- 使用Tencent OS Server 3.3物料 - 创建物理机工作负载集群 - 创建成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署用户容器镜像仓库 - 部署成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - registry+管控集群 - 导入/拉取镜像正常
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 集群配置用户容器镜像仓库 - 导入/拉取镜像正常
                    x86 hygon - 常规物料 - 用户容器镜像仓库安装部署 - 部署成功，无限制
                    aarch64鲲鹏 - 常规物料 - registry，SKS服务安装部署 - 部署成功，无限制
                    hygon x86_64 - Registry - 架构不一致 - 向x86集群上传aarch64架构的Tencent os安装包 - 部署失败
                    鲲鹏 AArch64 - Registry - 架构不一致 - 向aarch64集群上传x86架构的tencent os安装包 - 部署失败
            tower是非Tencent os
                SMTX os是非Tencent os - open Euler22.03 SP3
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署registry（rocky8.9） - 部署成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署用户容器镜像仓库（rocky8.9） - 部署成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署管控集群（TencentOS server3.3） - 部署成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署registry,管控集群（TencentOS server3.3）后卸载 - 卸载成功
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署用户容器镜像仓库（rocky）后卸载 - 卸载成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署registry - 部署成功无限制，目前是rocky8.9（scos支持oe后是oe）
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署管控集群（TencentOS server3.3） - 部署成功无限制
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署用户容器镜像仓库 - 部署成功无限制 - 目前是rocky（scos支持oe后是oe）
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署registry,管控集群（TencentOS server3.3）后卸载 - 卸载成功
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署用户容器镜像仓库后卸载 - 卸载成功
                    x86 hygon - 常规物料 - 用户容器镜像仓库安装成功 - 节点系统目前rocky8.9，依赖scos支持，版本openEuler 22.03 SP3待定
                    x86 hygon - 常规物料 - registry安装成功 - 节点系统目前rocky8.9，依赖scos支持，版本openEuler 22.03 SP3待定
                    x86 hygon - 常规物料 - 部署SKS管控集群 - 部署成功 - 节点系统openEuler 22.03 SP3
                    aarch64鲲鹏 - 常规物料 - registry安装成功 - 节点系统目前rocky，依赖scos支持，版本openEuler 22.03 SP3待定
                    aarch64鲲鹏 - 常规物料 - 部署SKS管控集群 - 部署成功 - 节点系统openEuler 22.03 SP3
                    aarch64鲲鹏 - 常规物料 - 用户容器镜像仓库安装成功 - 节点系统目前rocky，依赖scos支持，版本openEuler 22.03 SP3待定
                SMTX os是非Tencent os - centos
                    x86 hygon - 常规物料 - registry，部署成功 - 节点系统rocky8.9
                    x86 hygon - 常规物料 - SKS管控集群部署成功 - 节点系统open Euler22.03 sp3
                    aarch64鲲鹏 - 常规物料 - registry安装成功 - 节点系统rocky8.9 ？？
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署registry（rocky8.9） - 部署成功无限制
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署用户容器镜像仓库（rocky8.9） - 部署成功无限制
                    Hygon x86_64 - 使用Tencent OS Server 3.3物料 - 部署管控集群（TencentOS server3.3） - 部署成功无限制
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署registry（rocky） - 部署成功无限制
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署管控集群（TencentOS server3.3） - 部署成功无限制
                    鲲鹏 AArch64 - 使用Tencent OS Server 3.3物料 - 部署用户容器镜像仓库（rocky） - 部署成功无限制
            资源要求
                SKS容器镜像仓库 - 4vCPU, 8GiB 内存, 20GiB 系统盘, 400GiB 数据盘
                SKS管控集群cp节点 - 4vCPU/8GiB 内存/200GiB 存储
                SKS管控集群worker节点 - 8vCPU/16GiB 内存/200GiB 存储
                网络和防火墙要求 --- TBD
                用户容器镜像仓库 - 最小值 4vCPU, 8GiB 内存, 160GiB 数据盘
                用户容器镜像仓库 - 默认值 4vCPU, 8GiB 内存, 400GiB 数据盘
        升级
            低于SKS1.6 - registry升级到1.6适配版本 - 升级成功
            低于SKS1.6 - registry升级到1.6Tencent os专用版本 - 不支持升级
            低于SKS1.6 - SKS服务升级到1.6适配版本 - 升级成功
            低于SKS1.6 - SKS服务升级到1.6Tencent os专用版本 - 不支持升级
        其他场景测试
            信创支持 - 节点文件 - 列表查看K8s版本、操作系统、适用架构、模板版本信息
            工作负载集群 - 详情页Node card展示os系统信息 - Tencent OS 3.3
            SKS-3538 - 用户容器镜像仓库密码包含特殊字符组合时，可以通过密码正常登录
            SKS-3334 - 修改用户容器镜像仓库docker container默认使用的网段:172.17.0.0/16开始修改为172.30.181.0/24 降低冲突概率
            SKS-4023 - 升级harbor版本至v2.12.2 - rocky - registry
            SKS-4023 - 升级harbor版本至v2.12.2 - rocky - 用户容器镜像仓库
            SKS-4023 - 升级harbor版本至v2.12.2 - openeuler
            SKS-4023 - 升级harbor版本至v2.12.2 - tencent os
            SKS-4052 - registry nginx 升级至 1.29.3 - rocky
            SKS-4052 - registry nginx 升级至 1.29.3 - openEuler
            SKS-4052 - registry nginx 升级至 1.29.3 - Tencent OS
    SKS 1.6 节点操作系统支持
        已适配节点OS支持
            Rocky Linux 9.7 版本的支持
                新部署SKS1.6 - 管控集群节点模板版本 - default - k8s版本：1.27节点系统版本：rocky9.6
                discard - 新部署SKS1.6 - 管控集群节点模板版本 - k8s版本升级 - 1.26->1.27
                新部署SKS1.6 - 管控集群节点模板版本 - k8s版本升级 - 1.27->1.28
                新部署SKS1.6 - 管控集群节点模板版本 - k8s版本升级 - 1.28->1.29
                新部署SKS1.6 - 管控集群节点模板版本 - k8s版本升级 - 1.29->1.30
                新部署SKS1.6 - 管控集群节点模板版本 - k8s版本升级 - 1.30->1.31
                升级SKS1.6 - 管控集群节点模板版本替换 - k8s1.26+rocky8.10 -> k8s1.27+rocky9.7
                新建工作负载集群 - 虚拟机集群 - 新建v1.26版本的集群,插件全开 - 创建成功
                新建工作负载集群 - 虚拟机集群 - 创建v1.27版本的集群,插件全开 - 创建成功
                新建工作负载集群 - 虚拟机集群 - 创建v1.28版本的集群,插件全开 - 创建成功
                新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                新建工作负载集群 - 虚拟机集群 - 新建集群后功能验证
                新建工作负载集群 - 虚拟机集群 - 新建集群后升级k8s版本（例如：1.27->1.28）
                新建工作负载集群 - 物理机集群 - 选择rocky8.10版本的节点 - 创建成功不受影响
                新建工作负载集群 - 物理机集群 - 新建低于v1.29版本的集群 - 无法创建，UI过滤掉低于v1.29版本的节点模板
                新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                已有工作负载集群 - 虚拟机集群 - rocky8.10 - 维持正常运行
                已有工作负载集群 - 虚拟机集群 - rocky8.10升级到rocky9.7(同k8s版本) - 升级成功
                已有工作负载集群 - 物理机集群 - 低于1.29版本的rocky8.10 - 维持正常运行
                已有工作负载集群 - 物理机集群 - 低于1.29版本的rocky8.10 - 无法升级 - workaround：升级SKS到1.28及以上后再升级到1.29版本
            信创 - openEuler 22.03 SP3 维持性维护
                工作负载集群：openEuler22.03
                    x86hygon-新部署SKS1.6 - 管控集群节点模板版本default - registry：rocky8.9+ k8s版本：1.27节点系统版本：openEuler 22.03 SP3
                    aarch64鲲鹏-新部署SKS1.6 - 管控集群节点模板版本default - registry：rocky8.9+ k8s版本：1.27节点系统版本：openEuler 22.03 SP3
                    Hygon x86_64/鲲鹏 AArch64 - 新部署SKS1.6 - 管控集群节点模板版本 - k8s版本升级 - 1.27->1.28
                    Hygon x86_64/鲲鹏 AArch64 - 新部署SKS1.6 - 管控集群节点模板版本 - k8s版本升级 - 1.28->1.29
                    Hygon x86_64/鲲鹏 AArch64 - 新部署SKS1.6 - 管控集群节点模板版本 - k8s版本升级 - 1.29->1.30
                    Hygon x86_64/鲲鹏 AArch64 - 新部署SKS1.6 - 管控集群节点模板版本 - k8s版本升级 - 1.30->1.31
                    升级SKS1.6 - 管控集群节点模板版本维持：openEuler22.03 SP3 - k8s版本升级到1.27
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.27版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.28版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.27版本的集群,插件全开 - 创建成功
                    鲲鹏AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.28版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    鲲鹏AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    新建工作负载集群 - 虚拟机集群 - 新建集群后功能验证
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                    已有工作负载集群 - 虚拟机集群 - k8s1.26版本 - 维持正常运行
                    已有工作负载集群 - 虚拟机集群 - k8s1.26升级到K8S1.27(无同k8s版本) - 升级成功
            ubuntu 22.04.4 LTS维护性维护
                Intel x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                Intel x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                Intel x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                已有工作负载集群 - 物理机集群 - 低于1.29版本的集群 - 无法升级 - workaround：升级SKS到1.28及以上后再升级到1.29版本
        新增信创 OS 支持
            Tencent OS Server 3.3「单活/双活」
                支持向强信创迁移路径 - Hygon x86_64/鲲鹏aarch64 - cloudtower/SMTX OS:open Euler - SKS系统服务OS:openEuler2203-v1.27 - 工作负载集群：TencentOS
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    新建工作负载集群 - 虚拟机集群 - 新建集群后功能验证
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                    Hygon x86_64/鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机/物理机集群 - v1.29版本的集群升级到v1.30 - 升级成功
                全栈Tencent OS主推方案 - hygonx86/鲲鹏 AArch64 - cloudtower/SMTX OS:Tencent OS - SKS系统服务OS:TencentOS-v1.29 - 工作负载集群：TencentOS
                    x86hygon-新部署SKS1.6 - 管控集群节点模板版本default - registry：Tencent OS Server 3.3 + 管控集群k8s版本：1.29/节点系统版本：Tencent OS Server 3.3
                    aarch64鲲鹏-新部署SKS1.6 - 管控集群节点模板版本default - registry：Tencent OS Server 3.3+ k8s版本：1.29/节点系统版本：Tencent OS Server 3.3
                    Hygon x86_64/鲲鹏 AArch64 - 新部署SKS1.6 - 管控集群节点模板版本 - k8s版本升级 - 1.29->1.30
                    Hygon x86_64/鲲鹏 AArch64 - 新部署SKS1.6 - 管控集群节点模板版本 - k8s版本升级 - 1.30->1.31
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    新建工作负载集群 - 虚拟机集群 - 新建集群后功能验证
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                    Hygon x86_64/鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机/物理机集群 - v1.30版本的集群升级到v1.31 - 升级成功
                支持向强信创迁移路径 - Hygon x86_64/鲲鹏aarch64 - cloudtower/SMTX OS:openEuler - SKS系统服务OS:TencentOS-v1.29 - 工作负载集群：TencentOS
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    新建工作负载集群 - 虚拟机集群 - 新建集群后功能验证
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                    Hygon x86_64/鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机/物理机集群 - v1.30版本的集群升级到v1.31 - 升级成功
            Kylin V10 SP3 2203
                满足特定 Kylin 工作负载需求 - Hygon x86_64/鲲鹏aarch64 - cloudtower/SMTX OS:open Euler - SKS系统服务OS:openEuler2203-v1.27 - 工作负载集群：kylin OS
                    x86hygon-新部署SKS1.6 - registry：rocky8.9 + 管控集群k8s版本：1.27节点系统版本：open Euler22.03
                    aarch64鲲鹏-新部署SKS1.6 - registry：rocky8.9+ k8s版本：1.27节点系统版本：open Euler22.03
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    新建工作负载集群 - 虚拟机集群 - 新建集群后功能验证
                    Hygon x86_64/AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64/AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64/AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                    Hygon x86_64/鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机/物理机集群 - v1.29版本的集群升级到v1.30 - 升级成功
                满足特定 Kylin 工作负载需求 - hygonx86/鲲鹏 AArch64 - cloudtower/SMTX OS:TencentOS - SKS系统服务OS:TencentOS-v1.29 - 工作负载集群：Kylin OS
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    新建工作负载集群 - 虚拟机集群 - 新建集群后功能验证
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                    Hygon x86_64/鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机/物理机集群 - v1.29版本的集群升级到v1.30 - 升级成功
                满足特定kylin工作负载需求 - hygon64/鲲鹏 AArch64 - cloudtower/SMTX OS:openEuler - SKS系统服务OS:TencentOS-v1.29 - 工作负载集群：Kylin OS
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.29版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.30版本的集群,插件全开 - 创建成功
                    鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机集群 - 创建v1.31版本的集群,插件全开 - 创建成功
                    新建工作负载集群 - 虚拟机集群 - 新建集群后功能验证
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                    Hygon x86_64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.29版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.30版本的集群,插件全开 - 创建成功
                    AArch64 - 新建工作负载集群 - 物理机集群 - 新建v1.31版本的集群,插件全开 - 创建成功
                    新建工作负载集群 - 物理机集群 - 新建集群后功能验证
                    Hygon x86_64/鲲鹏 AArch64 - 新建工作负载集群 - 虚拟机/物理机集群 - v1.30版本的集群升级到v1.31 - 升级成功
            特供版节点模板升级后影响
                discard - 有特供k8s-v1.30的集群升级SKS到1.6 - 升级后，旧特供节点模板更新（含适配 K8s 1.30 的 Tencent OS 节点模板和适配 K8s 1.30 的 Rocky OS 节点模版）？？？？
                有特供k8s-v1.30的集群升级SKS到1.6 - 升级后，虚拟机集群可正常使用
                有特供k8s-v1.30的集群升级SKS到1.6 - 升级后，集群可正常扩/缩容节点组
                有特供k8s-v1.30的集群升级SKS到1.6 - 升级后，集群可正常升级到1.6提供的v1.30版本
                有特供k8s-v1.30的集群升级SKS到1.6 - 升级后，集群可正常升级到1.6提供的v1.31版本
                有特供k8s-v1.30的集群升级SKS到1.6 - 升级后，使用旧特供模板新建虚拟机工作负载集群 - UI不展示旧模板可选
        其他功能影响
            核心操作 - 集群创建成功后，滚动升级k8s版本 - 升级成功不受影响
            核心操作 - 集群创建成功后，编辑k8s参数/扩容磁盘 - 原地更新
            专项测试 - 集群创建成功后，k8s一致性测试  - tencentos/kylin v10/rocky9.6
            专项测试 - 集群创建成功后，漏洞扫描 -- TBD
            SKS升级 - x86/Aarch64 - 管控集群rocky/openeuler - 上传Tencent OS的升级包 - 升级失败？？
        必须适配的组合场景 --- TBD registry待补充
            x86
                标准非信创部署模式 - Intel x86_64 - cloudtower/SMTX OS:centos - SKS系统服务OS:Rocky Linux9.6 - 工作负载集群：Rocky Linux9.6
                标准非信创部署模式 - Intel x86_64 - cloudtower/SMTX OS:centos - 用户容器镜像仓库 OS:Rocky Linux8.9
                全栈open Euler - Hygon x86_64 - cloudtower/SMTX OS:open Euler - SKS系统服务OS:openEuler - 工作负载集群：openEuler
                全栈open Euler - Hygon x86_64 - cloudtower/SMTX OS:open Euler - SKS系统服务OS:openEuler - 工作负载集群：Kylin OS
                全栈open Euler - Hygon x86_64 - cloudtower/SMTX OS:open Euler - SKS系统服务OS:openEuler - 工作负载集群：TencentOS
                全栈open Euler - Hygon x86_64 - cloudtower/SMTX OS:open Euler - 用户容器镜像仓库OS:rocky8.9
                满足特定kylin工作负载需求 - Hygon x86_64 - cloudtower/SMTX OS:openEuler - SKS系统服务OS:TencentOS - 工作负载集群：Kylin OS
                满足特定kylin工作负载需求 - Hygon x86_64 - cloudtower/SMTX OS:openEuler - SKS系统服务OS:TencentOS - 工作负载集群：TencentOS
                满足特定kylin工作负载需求 - Hygon x86_64 - cloudtower/SMTX OS:openEuler - 用户容器镜像仓库OS:rocky8.9
                全栈Tencent OS主推方案 - Hygon x86_64 - cloudtower/SMTX OS:TencentOS - SKS系统服务OS:TencentOS - 工作负载集群：Kylin OS
                全栈Tencent OS主推方案 - Hygon x86_64 - cloudtower/SMTX OS:Tencent OS - SKS系统服务OS:TencentOS - 工作负载集群：TencentOS
                全栈Tencent OS主推方案 - Hygon x86_64 - cloudtower/SMTX OS:Tencent OS - 用户容器镜像仓库OS:TencentOS
            aarch64
                全栈open Euler - 鲲鹏 AArch64 - cloudtower/SMTX OS:open Euler - SKS系统服务OS:openEuler - 工作负载集群：openEuler
                全栈open Euler - 鲲鹏 AArch64 - cloudtower/SMTX OS:open Euler - SKS系统服务OS:openEuler - 工作负载集群：Kylin OS
                全栈open Euler - 鲲鹏 AArch64 - cloudtower/SMTX OS:open Euler - SKS系统服务OS:openEuler - 工作负载集群：TencentOS
                全栈open Euler - 鲲鹏 AArch64 - cloudtower/SMTX OS:open Euler - 用户容器镜像仓库OS:rocky8.9
                满足特定kylin工作负载需求 - 鲲鹏 AArch64 - cloudtower/SMTX OS:openEuler - SKS系统服务OS:TencentOS - 工作负载集群：Kylin OS
                满足特定kylin工作负载需求 - 鲲鹏 AArch64 - cloudtower/SMTX OS:openEuler - SKS系统服务OS:TencentOS - 工作负载集群：TencentOS
                满足特定kylin工作负载需求 - 鲲鹏 AArch64 - cloudtower/SMTX OS:openEuler - 用户容器镜像仓库OS:rocky8.9
                全栈Tencent OS主推方案 - 鲲鹏 AArch64 - cloudtower/SMTX OS:TencentOS - SKS系统服务OS:TencentOS - 工作负载集群：Kylin OS
                全栈Tencent OS主推方案 - 鲲鹏 AArch64 - cloudtower/SMTX OS:Tencent OS - SKS系统服务OS:TencentOS - 工作负载集群：TencentOS
                全栈Tencent OS主推方案 - 鲲鹏 AArch64 - cloudtower/SMTX OS:Tencent OS - 用户容器镜像仓库OS:TencentOS
    SKS 支持昇腾 NPU
        适配SKS1.6 + ARM + SMTX OS621单活 + open Euler 22.03 SP3/Tencent OS 3.3/kylin V10 SP3 2403
        支持的昇腾GPU卡型号 - Atlas 300I Duo
        支持的昇腾GPU卡型号 - Atlas 300I Pro
        NPU Operator管理的组件
            新增CRD - NPUClusterPolicy - 配置NPU组件
            新增addon - ascend-npu-operator(25.11.4)
            组件 - ascend-npu-operator-node-feature-discovery-gc-xx（deployment）-（v0.16.4）
            组件 - ascend-npu-operator-node-feature-discovery-master-xx（deployment）-（v0.16.4）
            组件 - ascend-npu-operator-node-feature-discovery-worker-xx（daemonset）-（v0.16.4）
            组件 - npu-feature-discovery-xx（daemonset）-（v25.11.1）
            组件 - ascend-device-plugin-xx（daemonset）-（v7.1.RC1）
            组件 - ascend-runtime-containerd-xx（daemonset）-（v25.11.2）
            组件 - npu-driver-xx（daemonset）-（v25.11.2）
            组件 - npu-operator-xx（deployment）-（v25.11.2）
            组件 - npu-exporter-xx（daemonset）-（v7.1.RC1）
            组件 - ascend-npu-operator-node-feature-discovery-prune-xx（job）-（v0.16.4）- operator运行后变成completed状态
            ascend-runtime-containerd - npu-container-toolkit - 集群未配置NPU - 检查/etc/containerd/config.toml配置
            ascend-runtime-containerd - npu-container-toolkit - 集群配置NPU并开启operator - 检查/etc/containerd/config.toml配置变更
            ascend-runtime-containerd - npu-container-toolkit - 集群配置NPU并开启operator后关闭operator - 检查/etc/containerd/config.toml配置回滚，并重启containerd
            组件镜像检查 - harbor中检查默认dump镜像
            driver安装方式
                离线安装（默认）- 依赖的工具包和驱动使用镜像中的离线包安装
                安装驱动 - 默认创建UID=1001的用户HwHiAiUser
                安装驱动 - 资源不足（6c2g）- 驱动安装失败，需要手动卸载清理
                安装驱动（虚拟机集群）- 资源不足（6c2g）- 驱动安装失败 - 扩容资源 - 手动清理后再安装kernel-devel、kernel-headers、dkms工具后驱动自动安装成功
                open Euler - 卸载驱动 - 不支持自动卸载（关闭operator）- 手动卸载，需要一并卸载npu-smi工具
                Tencent OS - 卸载驱动 - 不支持自动卸载（关闭operator）- 手动卸载，需要一并卸载npu-smi工具
                kylin v10 - 卸载驱动 - 不支持自动卸载（关闭operator）- 手动卸载，需要一并卸载npu-smi工具
        版本和架构
            discard - 新建虚拟机集群 - open Euler 22.03 SP3 - k8s版本v1.26 - 配置昇腾NPU卡 - 新建成功
            新建虚拟机集群 - open Euler 22.03 SP3 - k8s版本v1.27 - 配置昇腾NPU卡 - 新建成功
            新建虚拟机集群 - open Euler 22.03 SP3 - k8s版本v1.28 - 配置昇腾NPU卡 - 新建成功
            新建虚拟机集群 - open Euler 22.03 SP3 - k8s版本v1.29 - 配置昇腾NPU卡 - 新建成功
            新建虚拟机集群 - open Euler 22.03 SP3 - k8s版本v1.30 - 配置昇腾NPU卡 - 新建成功
            新建虚拟机集群 - open Euler 22.03 SP3 - k8s版本v1.31 - 配置昇腾NPU卡 - 新建成功
            新建虚拟机集群 - Tencent OS 3.3 - k8s版本v1.29 - 配置昇腾GPU卡 - 新建成功
            新建虚拟机集群 - Tencent OS 3.3 - k8s版本v1.30 - 配置昇腾GPU卡 - 新建成功
            新建虚拟机集群 - Tencent OS 3.3 - k8s版本v1.31 - 配置昇腾GPU卡 - 新建成功
            新建虚拟机集群 - kylin V10 SP3 2403 - k8s版本v1.29 - 配置昇腾GPU卡 - 新建成功
            新建虚拟机集群 - kylin V10 SP3 2403 - k8s版本v1.30 - 配置昇腾GPU卡 - 新建成功
            新建虚拟机集群 - kylin V10 SP3 2403 - k8s版本v1.31 - 配置昇腾GPU卡 - 新建成功
            新建物理机集群 - 创建成功后，安装了驱动和固件之后，需要手动 reboot，UI已增加header tip提示
            新建物理机集群 - open Euler 22.03 SP3 - k8s版本v1.29 - 配置昇腾GPU卡 - 新建成功
            新建物理机集群 - open Euler 22.03 SP3 - k8s版本v1.30 - 配置昇腾GPU卡 - 新建成功
            新建物理机集群 - open Euler 22.03 SP3 - k8s版本v1.31 - 配置昇腾GPU卡 - 新建成功
            新建物理机集群 - Tencent OS 3.3 - k8s版本v1.29 - 配置昇腾GPU卡 - 新建成功
            新建物理机集群 - Tencent OS 3.3 - k8s版本v1.30 - 配置昇腾GPU卡 - 新建成功
            新建物理机集群 - Tencent OS 3.3 - k8s版本v1.31 - 配置昇腾GPU卡 - 新建成功
            新建物理机集群 - kylin V10 SP3 2403 - k8s版本v1.29 - 配置昇腾GPU卡 - 新建成功
            新建物理机集群 - kylin V10 SP3 2403 - k8s版本v1.30 - 配置昇腾GPU卡 - 新建成功
            新建物理机集群 - kylin V10 SP3 2403 - k8s版本v1.31 - 配置昇腾GPU卡 - 新建成功
        已有功能影响
            新增监控图表
                集群中有NPU相关 - 开启监控 - 新增NPU dashboard，tag使用ascend
                监控 - Ascend NPU Overview - 筛选 - 通过instance筛选 - 正确展示相关图表
                监控 - Ascend NPU Overview - 筛选 - 通过npu_id筛选 - 正确展示相关图表
                监控 - Ascend NPU Overview - 筛选时间 - 默认1h，可切换
                监控 - Ascend NPU Overview - 图表与grafana图表比对 - 完全一致
                监控 - Ascend NPU Overview - 昇腾AI处理器数目
                监控 - Ascend NPU Overview - 昇腾AI名称和ID
                监控 - Ascend NPU Overview - 昇腾AI处理器健康状态
                监控 - Ascend NPU Overview - 昇腾AI处理器AI Core利用率
                监控 - Ascend NPU Overview - 昇腾AI处理器功耗
                监控 - Ascend NPU Overview - 昇腾AI处理器的AI Core当前频率
                监控 - Ascend NPU Overview - 昇腾AI处理器进程占用内存信息
                监控 - Ascend NPU Overview - 昇腾AI处理器温度
                监控 - Ascend NPU Overview - 昇腾AI处理器HBM内存（暂不支持）
                监控 - Ascend NPU Overview - 昇腾AI处理器DDR内存
                监控 - Ascend NPU Overview - 昇腾AI处理器网口实时发送速率（暂不支持）
                监控 - Ascend NPU Overview - 昇腾AI处理器网口实时接收速率（暂不支持）
                监控 - Ascend NPU Overview - 昇腾AI处理器网络健康状态（暂不支持）
                监控 - Ascend NPU Overview - 昇腾AI处理器网口Link状态（暂不支持）
            日志/事件
                分类新增 - source_type:kubernetes_logs - sks-system-ascend-npu - ascend-npu-operator 相关日志
                日志收集 - 昇腾NPU相关的节点事件
            时区
                sks-system-ascend-npu - npu-operator-xxx - 配置文件与工作负载集群设置的时区保持一致
                sks-system-ascend-npu - ascend-npu-operator-node-feature-discovery-master-xxx - 配置文件与工作负载集群设置的时区保持一致
                sks-system-ascend-npu - ascend-npu-operator-node-feature-discovery-worker-xxx - 配置文件与工作负载集群设置的时区保持一致
                sks-system-ascend-npu - npu-feature-discovery-xxx - 配置文件与工作负载集群设置的时区保持一致
                sks-system-ascend-npu - ascend-device-plugin-xxx - 配置文件与工作负载集群设置的时区保持一致
                sks-system-ascend-npu - ascend-runtime-containerd-xxx - 配置文件与工作负载集群设置的时区保持一致
                sks-system-ascend-npu - npu-driver-xxx - 配置文件与工作负载集群设置的时区保持一致
                sks-system-ascend-npu - npu-operator-xxx - 配置文件与工作负载集群设置的时区保持一致
                sks-system-ascend-npu - npu-exporter-xxx - 配置文件与工作负载集群设置的时区保持一致
                sks-system-ascend-npu - npu-container-toolkit-xxx - 配置文件与工作负载集群设置的时区保持一致
            物理机工作负载集群 - npu
                添加物理机 - 节点已配置NPU卡 - 添加成功并且驱动安装成功后查看 - npu-smi info
                添加物理机 - 节点有NPU卡 - 添加前需要手动安装kernel-devel、kernel-headers 和 dkms，kernel-devel 和 kernel-headers 的版本需要和内核版本保证一致
                添加物理机 - 节点已配置NPU卡 - 没有安装kernel-devel、kernel-headers和dkms直接加入集群，npu驱动安装失败，需要手动处理
                创建/删除工作负载集群
                    创建物理机工作负载集群 - EIC+SMTX ZBS CSI - 配置昇腾NPU节点 - 验证？？？-- TBD
                    创建物理机工作负载集群 - calico+SMTX ZBS CSI - 配置昇腾 NPU节点
                    创建物理机工作负载集群 - calico+no-csi - 配置昇腾 NPU节点 - 可正常跑NPU测试
                    创建物理机工作负载集群 - 节点配置昇腾NPU - ksc检查 - ksc.sepc.components.npu
                    创建物理机工作负载集群 - 物理机节点列表 - 下拉展示物理机节点信息，包含GPU卡信息 - tooltip展示具体型号和对应数量
                    创建物理机工作负载集群 - 节点组 - control plane - 不支持配置昇腾NPU卡
                    创建物理机工作负载集群 - 节点组 - 1worker - 配置一张NPU卡 - 创建成功
                    创建物理机工作负载集群 - 节点组 - 1worker - 配置多张同类型NPU卡 - 创建成功
                    创建工作负载集群 - 节点组 - 1worker - 配置多张不同类型NPU卡(数量是所有主机上的该型号的卡的总和) - 无法提交有报错
                    创建物理机工作负载集群 - 节点选择了昇腾NPU资源 - operator默认关闭，可开启，开启后提供ascend-npu-operator插件yaml配置入口 - 默认为空，1.6不提供可配置参数
                    创建物理机工作负载集群 - 节点无昇腾NPU资源 - operator插件默认关闭可开启，开启后提供ascend-npu-operator插件yaml配置入口 -- TBD
                    删除物理机工作负载集群 - 删除成功 - 相关资源被清理，NPU资源节点释放，可再次被使用
                ascend-npu-operator参数配置 --- TBD
                    物理机工作负载集群 - 配置昇腾NPU - 手动开启operator后关闭 - 关闭成功，相关资源正常清理
                    物理机工作负载集群 - 配置昇腾NPU - 手动关闭operator后开启 - 开启成功，相关资源正常创建
                节点组管理
                    创建节点组 - 昇腾GPU
                        创建节点组 - NPU卡列表获取 - 节点上所有型号，规格NPU卡
                        已有工作负载集群（节点无GPU卡）- 创建新的worker节点组 - 选择有NPU卡的节点 - 创建成功，手动打label后，operator需手动开启
                        已有工作负载集群（节点无GPU卡）- 创建新的worker节点组 - 选择有NPU卡的节点 - 创建成功，operator需手动开启，关闭operator - 关闭成功
                        已有工作负载集群 - 创建新的worker节点组 - 选择无NPU卡的节点 - 创建成功
                        已有工作负载集群 - 已有worker节点组添加节点 - 节点上的NPU卡不满足节点组配置 - 集群更新失败 --- TBD
                    编辑节点组 - 昇腾NPU
                        编辑节点组 - 无NPU卡的节点组 - 增加有GPU卡的节点 - 编辑成功，需要手动开启operator
                        编辑节点组 - 移除有NPU卡的节点 - 编辑成功 - operator不会自动关闭，需要手动关闭以及清理驱动？？-- TBD
                        编辑节点组 - 已有NPU卡的节点，且开启ascend npu operator - 增加无NPU卡的节点 - 编辑成功，operator保持开启状态
                        编辑节点组 - 有NPU卡的节点，移除无NPU卡的节点 - 编辑成功
                        编辑节点组 - 有NPU卡的节点组 - 移除后新加入其他有NPU卡的节点 - 编辑成功
                    删除节点组 - 昇腾NPU
                        删除节点组 - 有NPU卡的节点组 - 删除后，节点释放可加入其他节点组
                工作负载集群升级
                    Kubernetes版本升级 - 升级前挂载昇腾NPU卡，升级后保持挂载，NPU卡正常使用
                资源共享与隔离
                    单 Pod 独占节点上的单 NPU 卡（310P）
                    单 Pod 独占节点上的多张 NPU 卡
            虚拟机工作负载集群 - NPU
                创建工作负载集群
                    创建虚拟机工作负载集群 - 节点配置昇腾NPU - ElfMachine.spec.gpuDevice检查 - 新增brand:NVIDIA 和 HUAWEI
                    创建虚拟机工作负载集群 - 创建时不配置昇腾NPU卡 - ascend-npu-operator插件不展示
                    创建虚拟机工作负载集群 - 创建时配置昇腾NPU卡 - 创建后ascend-npu-operator插件不ready - 手动给worker节点组打label: masterselector: dls-master-node后operator ready
                    创建虚拟机工作负载集群 - 创建时配置NPU - 节点配置 - 自动伸缩禁用，hover info icon 可查看 tooltip：节点组暂不支持同时挂载 NPU 和配置自动伸缩。
                    创建虚拟机工作负载集群 - 创建时先配置自动伸缩 - 节点配置 - 选择硬件加速器直通时，NPU 卡禁用处理，禁用原因：节点组暂不支持同时挂载 NPU 和配置自动伸缩。
                    创建虚拟机工作负载集群 - 创建时不配置NPU - 节点配置 - 自动伸缩功能可正常开启
                删除节点组
                    删除节点组 - 节点配置NPU卡 - 节点组删除成功，NPU卡释放可再使用
                创建节点组
                    已有工作负载集群 - 创建节点组 - 先开启自动伸缩 - 选择硬件加速器直通时，NPU 卡禁用处理，禁用原因：节点组暂不支持同时挂载 NPU 和配置自动伸缩。
                    已有工作负载集群 - 创建节点组 - 先选择NPU卡 - 自动伸缩禁用，hover info icon 可查看 tooltip：节点组暂不支持同时挂载 NPU 和配置自动伸缩。
                编辑节点组
                    编辑节点组（未配置NPU）- 先开启自动伸缩 - 选择硬件加速器直通时，NPU 卡禁用处理，禁用原因：节点组暂不支持同时挂载 NPU 和配置自动伸缩。
                    编辑节点组（未配置NPU）- 先开启自动伸缩 - 选择硬件加速器直通时，NPU 卡禁用处理 - 切换到「固定节点数」- NPU卡可选，禁用解除
                    编辑节点组（已配置NPU）- 无法开启自动伸缩，开启按钮禁用，hover info icon 可查看 tooltip：节点组暂不支持同时挂载 NPU 和配置自动伸缩。
        使用场景测试
            3️⃣tencentos - NPU虚拟机工作负载集群 - 运行官方 AscendCL图片分类应用 + Ascend DMI压力测试
            2️⃣openeuler - NPU虚拟机工作负载集群 - 运行官方 AscendCL图片分类应用 + Ascend DMI压力测试
            1️⃣kylin - NPU虚拟机工作负载集群 - 运行官方 AscendCL图片分类应用 + Ascend DMI压力测试
            open Euler - NPU物理机工作负载集群 - 运行官方 AscendCL图片分类应用 + Ascend DMI压力测试
            Tencent OS - NPU物理机工作负载集群 - 运行官方 AscendCL图片分类应用 + Ascend DMI压力测试
            kylin - NPU物理机工作负载集群 - 运行官方 AscendCL图片分类应用 + Ascend DMI压力测试
        UI
            工作负载集群
                创建工作负载集群
                    创建虚拟机集群
                        节点配置 - worker节点组，文案调整：GPU-> 硬件加速器，默认选中不配置
                        节点配置 - 工作负载集群所在OS集群有昇腾硬件时，worker节点组展示「硬件加速器」配置项
                        节点配置 - 工作负载集群所在OS集群没有昇腾硬件时，worker节点组不展示「硬件加速器」配置项
                        节点配置 - worker节点组展示「硬件加速器」配置项 - 默认选中不配置，vGPU保持展示，但是无可选型号（昇腾硬件暂不支持vGPU）
                        节点配置 - 切换为直通 - 硬件加速器型号与数量为必填项，默认展示一行，不显示移除按钮
                        节点配置 - 切换为直通 - 点击「添加」可增加一行，配置大于1行时，显示移除按钮，点击可移除
                        节点配置 - 切换为直通 - 点击「添加」可增加一行，最后一行配置不可移除，至少保留一行配置
                        节点配置 - 切换为直通（昇腾GPU）- GPU不足错误提示文案调整：当前配置下，每节点最多可挂载N个硬件加速器。
                        节点配置 - 切换为直通（nvidia GPU）- GPU不足错误提示文案调整：当前配置下，每节点最多可挂载N个硬件加速器。
                        节点配置 - 切换为直通 - 硬件加速器型号列表展示，列表可筛选
                        节点配置 - 切换为直通 - 硬件加速器型号可使用后的tooltip文案调整
                        节点配置 - 切换为直通（昇腾GPU）- 硬件加速器不可选，展示禁用原因
                        节点配置 - 切换为直通（选择昇腾GPU卡）- 新增提示:确保 NPU 驱动成功部署，每个配置 NPU 的节点至少预留 6 vCPU 和 2 GiB 内存。
                        节点配置 - 切换为直通（选择昇腾GPU卡）- 创建成功后，详情页增加header tip提示给节点打label，否则operator不ready
                        插件配置 - 节点配置昇腾GPU - 插件小标题文案调整：GPU->硬件加速器
                        插件配置 - 节点配置Nvidia GPU - 插件小标题文案调整：GPU->硬件加速器
                        插件配置 - 节点不配置昇腾GPU - 不展示硬件加速器插件部分
                        插件配置 - 节点配置昇腾GPU - 自动开启Ascend NPU Operator -  位置在CSI之后
                        插件配置 - 节点配置昇腾GPU - 自动开启Ascend NPU Operator -   可关闭，检查关闭时的提示 - 创建成功后，集群插件页面保持一致关闭状态且有提示
                        插件配置 - 节点配置Nvidia GPU - 自动开启NVIDIA NPU Operator -   检查关闭时的提示文案调整，以及创建成功后，集群插件页面的文案提示
                        插件配置 - 节点配置昇腾GPU - 自动开启Ascend NPU Operator -   Ascend NPU Operator YAML配置框，默认为空
                        插件配置 - 节点配置昇腾GPU - Ascend NPU Operator YAML配置可配置参数 - 创建成功后，插件部分展示在yaml配置框中 --- TBD
                    创建物理机集群
                        节点配置 - 选择物理机节点列表下拉菜单 - 物理机节点有/无GPU资源，均不展示
                        节点配置 - 选择物理机节点列表下拉菜单 - 物理机节点有昇腾GPU资源，文案调整：GPU->硬件加速器（不展示）
                        节点配置 - 选择物理机节点列表下拉菜单 - 物理机节点有NVIDIA GPU资源，文案调整：GPU->硬件加速器
                        节点配置 - 选择物理机节点下拉菜单 - 物理机节点有昇腾GPU资源，不展示「硬件加速器」和「数量」
                        插件配置 - 硬件加速器tab - Ascend NPU Operator 插件和 NVIDIA GPU Operator 插件并列展示
                        插件配置 - 物理机节点无昇腾/Nvidia GPU - Ascend NPU Operator 插件和 NVIDIA GPU Operator 插件，默认始终展示，并默认关闭
                        插件配置 - 物理机节点有昇腾/Nvidia GPU - Ascend NPU Operator 插件和 NVIDIA GPU Operator 插件，默认始终展示，并默认关闭
                        插件配置 - 物理机节点有昇腾 GPU - Ascend NPU Operator 插件默认关闭 - 创建成功，插件页面保持统一关闭状态且有提示
                        插件配置 - 物理机节点有昇腾 GPU - 手动开启Ascend NPU Operator 插件 - 创建成功，operator正确开启
                        插件配置 - 物理机节点有昇腾 GPU - Ascend NPU Operator 插件默认关闭 - 创建成功后插件页面开启operator - 开启成功
                工作负载集群列表
                    工作负载集群列表 - 字段文案调整：GPU数量->硬件加速器数量
                    工作负载集群列表 - 字段文案调整：GPU型号->硬件加速器型号
                工作负载集群详情页
                    概览页 - 虚拟机集群 - card标题文案调整：GPU->硬件加速器；监控切换菜单文案调整：GPU利用率->硬件加速器利用率
                    概览页 - 物理机集群 - card标题文案调整：GPU->硬件加速器；监控切换菜单文案调整：GPU利用率->硬件加速器利用率
                    概览页 - 物理机集群 - 节点有/无昇腾GPU，硬件加速器card始终展示
                    概览页 - 物理机集群 - 节点无昇腾GPU，硬件加速器card展示 - 空状态：无数据
                    概览页 - 物理机集群 - 节点有昇腾GPU但是无数据，硬件加速器card展示 - 空状态：无数据
                    概览页 - 虚拟机集群（仅配置GPU）- 硬件加速器卡片显示内容保持不变。默认显示 显存利用率，支持切换 硬件加速器利用率 和 显卡使用率
                    概览页 - 物理机集群（仅配置GPU）- 硬件加速器卡片显示内容保持不变。默认显示 显存利用率，支持切换 硬件加速器利用率 和 显卡使用率
                    概览页 - 虚拟机集群（仅配置NPU）- 硬件加速器卡片默认显示 显存利用率，支持切换 硬件加速器利用率
                    概览页 - 物理机集群（仅配置NPU）- 硬件加速器卡片默认显示 显存利用率，支持切换 硬件加速器利用率
                    虚拟机集群 - 设置 - 插件管理 - 插件标题：GPU->硬件加速器，插件名称为Ascend NPU Operator
                    物理机集群 - 设置 - 插件管理 - 插件标题：GPU->硬件加速器，插件名称为Ascend NPU Operator，与NVIDIA GPU Operator同一层级
                    虚拟机集群 - Header Tip - 集群配置了NPU，集群层面提示：集群已配置 NPU 资源，选择一个 Worker 节点组为其打上 MasterSelector 标签，以保证 NPU 能够正常运行。
                    虚拟机集群 - Header Tip - 集群配置了NPU，手动在NPU节点组打标签后，header tip自动消失
                    虚拟机集群 - Header Tip - 集群配置了NPU，手动在任意节点组打标签后，header tip自动消失后再移除label，header tip再次提示
                    物理机集群 - Header Tip - 集群配置了NPU，集群层面提示：当集群中已配置 NPU 资源，需选择一个 Worker 节点组为其打上 MasterSelector 标签，以保证 NPU 能够正常运行。
                    物理机集群 - Header Tip - 集群配置了NPU，集群层面有header tip提示，提示可手动关闭
                    物理机集群 - Header Tip - 集群未配置NPU，集群层面有header tip提示，提示可手动关闭
                    物理机集群 - Header Tip - 集群NPU Addon就绪后集群层面有header tip:NPU 驱动已安装，节点重启后生效，请手动重启。重启将影响节点上 Pod 的正常运行。
                    物理机集群 - Header Tip - 集群NPU Addon就绪后，集群层面有「节点重启」header tip提示，提示可手动关闭，关闭后不再提示
                    物理机集群 - Header Tip - 集群NPU Addon就绪后，集群层面有「节点重启」header tip提示，手动重启节点后，提示不会自动消失
                    物理机集群 - Header Tip - 集群NPU Addon就绪后，集群层面有「节点重启」header tip提示，除手动重启节点外其他操作不影响提示展示
                    物理机集群 - Header Tip - 集群NPU Addon就绪后，集群层面有「节点重启」header tip提示，移除最后一个NPU节点后，addon保持开启，ready后提示依旧展示
                    物理机集群 - 配置了NPU，集群层面有「节点重启」header tip提示，移除非最后一个NPU节点后，提示消失后addon ready后重新展示？？？？
                设置 - 物理机管理
                    物理机列表 - 字段调整: GPU型号 -> 硬件加速器型号
                    物理机列表 - 字段调整: GPU型号 -> 硬件加速器型号「英文调整检查」
                    物理机列表 - 物理机节点有NVIDIA GPU - 硬件加速器型号显示为「GPU 卡具体型号比如：Tesla V100-PCIE-16GB」
                    物理机列表 - 物理机节点有昇腾GPU - 硬件加速器型号显示为「-」
            节点组与节点
                节点组 - 虚拟机集群
                    创建/编辑节点组
                        创建节点组 - 首次配置GPU资源，General tip文案调整:配置硬件加速器资源后将自动开启 Ascend NPU Operator 插件。
                        创建节点组 - 首次配置GPU资源，General tip文案调整:配置硬件加速器资源后将自动开启 Ascend NPU Operator 插件。「英文文案校验」
                        创建节点组 - 配置GPU资源，添加单个节点组 - 创建成功
                        创建节点组 - 配置GPU资源，添加多个节点组 - 创建成功
                        创建节点组 - 文案调整：GPU-> 硬件加速器，默认选中不配置
                        创建节点组 - 工作负载集群所在OS集群有昇腾硬件时，worker节点组展示「硬件加速器」配置项
                        创建节点组 - 工作负载集群所在OS集群没有昇腾硬件时，worker节点组不展示「硬件加速器」配置项
                        创建节点组 - 展示「硬件加速器」配置项 - vGPU保持展示，但是无可选型号（昇腾硬件暂不支持vGPU）
                        创建节点组 - 硬件加速器切换为直通 - 型号与数量为必填项，默认展示一行，不显示移除按钮
                        创建节点组 - 硬件加速器切换为直通（昇腾GPU）- GPU不足错误提示文案调整：当前配置下，每节点最多可挂载N个硬件加速器。
                        创建节点组 - 硬件加速器切换为直通（nvidia GPU）- GPU不足错误提示文案调整：当前配置下，每节点最多可挂载N个硬件加速器。
                        创建节点组 - 硬件加速器切换为直通 - 硬件加速器型号列表展示，列表可筛选
                        创建节点组 - 硬件加速器切换为直通 - 硬件加速器型号可使用后的tooltip文案调整
                        创建节点组 - 硬件加速器切换为直通（昇腾GPU）- 硬件加速器不可选，展示禁用原因
                        创建节点组 - 选择昇腾GPU卡 - 新增提示:确保 NPU 驱动成功部署，每个配置 NPU 的节点至少预留 6 vCPU 和 2 GiB 内存。
                        编辑节点组 - 不配置切换为直通并选择NPU，General tip文案调整:配置硬件加速器资源后将自动开启 Ascend NPU Operator 插件。
                        编辑节点组 - 直通切换为不配置，保存成功后，NPU-operator自动关闭
                        编辑节点组 - 文案调整：GPU-> 硬件加速器，默认选中不配置
                        编辑节点组 - 工作负载集群所在OS集群有昇腾硬件时，worker节点组展示「硬件加速器」配置项
                        编辑节点组 - 工作负载集群所在OS集群没有昇腾硬件时，worker节点组不展示「硬件加速器」配置项
                        编辑节点组 - 展示「硬件加速器」配置项 - vGPU保持展示，但是无可选型号（昇腾硬件暂不支持vGPU）
                        编辑节点组 - 硬件加速器切换为直通（昇腾GPU）- GPU不足错误提示文案调整：当前配置下，每节点最多可挂载N个硬件加速器。
                        编辑节点组 - 硬件加速器切换为直通（nvidia GPU）- GPU不足错误提示文案调整：当前配置下，每节点最多可挂载N个硬件加速器。
                        编辑节点组 - 硬件加速器切换为直通 - 硬件加速器型号列表展示，列表可筛选
                        编辑节点组 - 硬件加速器切换为直通 - 硬件加速器型号可使用后的tooltip文案调整
                        编辑节点组 - 硬件加速器切换为直通（昇腾GPU）- 硬件加速器不可选，展示禁用原因
                        编辑节点组 - 选择昇腾GPU卡 - 新增提示:确保 NPU 驱动成功部署，每个配置 NPU 的节点至少预留 6 vCPU 和 2 GiB 内存。
                    节点组列表
                        列表字段文案调整：GPU显存总分配量->硬件加速器显存总分配量
                    节点组详情
                        详情页字段文案调整：GPU使用方式->硬件加速器使用方式
                        详情页字段文案调整：GPU型号->硬件加速器型号
                        详情页字段文案调整：GPU显存总分配量->硬件加速器显存总分配量
                节点
                    节点列表 - 虚拟机集群
                        列表字段文案调整：GPU显存->硬件加速器显存
                        列表字段文案调整：GPU显存使用率->硬件加速器显存使用率
                    节点详情 - 虚拟机集群
                        详情页资源用量文案调整：GPU显存->硬件加速器显存（节点有nvidia GPU卡）
                        节点有NPU配置 - 详情页资源用量 - 硬件加速器显存card（不展示）
                    节点详情 - 物理机集群
                        详情页资源用量文案调整：GPU显存->硬件加速器显存
                        物理机集群，节点无NPU配置 - 详情页资源用量 - 硬件加速器显存card（不展示）
                        物理机集群，节点有NPU配置 - 详情页资源用量 - 硬件加速器显存card（不展示）
                节点组 - 物理机集群
                    节点组详情
                        详情页字段文案调整：GPU使用方式->硬件加速器使用方式
                        详情页字段文案调整：GPU型号->硬件加速器型号
                        详情页字段文案调整：GPU显存总分配量->硬件加速器显存总分配量
            项目与名字空间
                项目
                    创建/编辑项目
                        创建项目 - 项目配额字段调整：GPU数量->硬件加速器数量
                        编辑项目 - 项目配额字段调整：GPU数量->硬件加速器数量
                    项目详情
                        项目详情页 - 项目配额字段调整：GPU数量->硬件加速器数量
                名字空间
                    编辑名字空间配额 - 字段调整：GPU数量->硬件加速器数量
                    名字空间详情 - 名字空间配额 - 字段调整：GPU数量->硬件加速器数量
    控制平面证书更新机制优化
        CP证书管理 - 手动更新 - 手动更新证书使用原地更新，不引起节点滚动，节点 IP 保持不变
        CP证书管理 - 手动更新 - 手动更新过程中，节点展示为「更新中」状态，直到更新完成
        CP证书管理 - 手动更新 - 手动更新证书仅作用于 CP 节点，worker 节点无动作
        集群状态条件约束
            CP证书管理 - 集群状态约束 - 集群处于就绪状态，可触发手动更新
            CP证书管理 - 集群状态约束 - 集群处于运行中状态，可触发手动更新
            CP证书管理 - 集群状态约束 - 集群处于异常状态，可触发手动更新
            CP证书管理 - 集群状态约束 - 集群处于创建中状态，不可触发手动更新，更新按钮禁用
            CP证书管理 - 集群状态约束 - 集群处于删除中状态，不可触发手动更新，更新按钮禁用
            CP证书管理 - 集群状态约束 - 集群处于更新中状态，不可触发手动更新，更新按钮禁用
            CP证书管理 - 集群状态约束 - 集群处于暂停状态，不可触发手动更新，更新按钮禁用
            CP证书管理 - 集群状态约束 - 集群处于升级中状态，不可触发手动更新，更新按钮禁用
            CP证书管理 - 集群状态约束 - 更新证书过程中暂停集群，剩余 CP 节点不再更新，恢复后可继续更新直至完成
            CP证书管理 - 集群状态约束 - 更新证书期间不允许执行集群 K8s 版本升级操作
            CP证书管理 - 集群状态约束 - 更新证书期间不允许执行节点组编辑操作，可编辑标签/注解/污点
            CP证书管理 - 集群状态约束 - 更新证书期间可触发节点替换操作，更新完成后进行替换
            CP证书管理 - 集群状态约束 - 更新证书期间不允许执行编辑集群 K8s 参数操作
            CP证书管理 - 集群状态约束 - 更新证书期间不允许执行插件开关操作
        管控集群
            CP证书管理 - 管控集群 - UI - 管控集群添加「基本信息」tab，展示原有信息，默认显示该页
            CP证书管理 - 管控集群 - UI - 管控集群添加「集群证书管理」tab，选择后正确展示证书管理 UI - img
            CP证书管理 - 管控集群 - UI - 普通模式管控集群，展示 CP 节点 apiserver 证书的到期时间（YYYY-MM-DD HH:MM）
            CP证书管理 - 管控集群 - UI - 高可用模式管控集群，展示 CP 节点 apiserver 证书的到期时间（YYYY-MM-DD HH:MM）
            CP证书管理 - 管控集群 - UI - 普通模式管控集群提升到高可用模式，集群证书管理 tab 显示的节点信息行随之增加
            CP证书管理 - 管控集群 - 点击管控集群「更新集群证书」按钮，触发 CP 节点原地更新操作
            CP证书管理 - 管控集群 - 证书原地更新过程中，管控集群状态为「更新中」
            CP证书管理 - 管控集群 - 管控集群开始更新证书后，「更新集群证书」按钮转为 loading 状态，不可重复点击
            CP证书管理 - 管控集群 - 管控集群更新证书过程中，刷新页面，「更新集群证书」按钮仍然为 loading 状态
            CP证书管理 - 管控集群 - UI - 管控集群更新完成后，「更新集群证书」按钮恢复正常，弹出 toast「更新集群证书成功」
            CP证书管理 - 管控集群 - UI - 管控集群 CP 节点证书更新失败，「更新集群证书」按钮恢复正常，「集群证书管理」tab UI 显示error「更新集群证书失败。错误信息：xxx」
            CP证书管理 - 管控集群 - UI - 管控集群 CP 节点证书更新失败，「更新集群证书」按钮可再次点击触发更新，重新进入更新中状态，最终更新成功后 error 信息清除
            CP证书管理 - 管控集群 - 管控集群 CP 节点依次原地更新，更新完的节点的证书过期时间显示变更为一年后，与后端 apiserver 证书显示时间相符
            CP证书管理 - 管控集群 - 普通模式管控集群可手动更新 CP 证书
            CP证书管理 - 管控集群 - 普通模式提升到高可用模式，管控集群可手动更新 CP 证书
            CP证书管理 - 管控集群 - 高可用模式管控集群可手动更新 CP 证书
            CP证书管理 - 管控集群 - UI 显示更新完成后，在 CP 节点中执行 kubeadm certs check-expiration 查看所有 10 项控制平面证书，过期时间均已更新为一年后
            CP证书管理 - 管控集群 - 手动更新过控制平面证书完成后，可反复发起更新，每次按照更新时间生成新的期限的证书
        工作负载集群
            CP证书管理 - 工作集群 - UI - 工作集群「设置」中增加「集群证书管理」项，选择后对照设计检查集群证书管理页 - img
            CP证书管理 - 工作集群 - UI - 单 CP 节点工作负载集群，展示 CP 节点 apiserver 证书的到期时间（YYYY-MM-DD HH:MM）
            CP证书管理 - 工作集群 - UI - 多 CP 节点工作负载集群，展示 CP 节点各自 apiserver 证书的到期时间 （YYYY-MM-DD HH:MM）
            CP证书管理 - 工作集群 - UI - 1 CP 工作负载集群扩容 CP 节点组（1 -> 3 -> 5），集群证书管理页显示的节点信息行对应增加
            CP证书管理 - 工作集群 - UI - 5 CP 工作负载集群缩容 CP 节点组到 3 节点，集群证书管理页显示的节点信息行对应减少
            CP证书管理 - 工作集群 - 点击工作集群「更新集群证书」按钮，触发 CP 节点原地更新操作
            CP证书管理 - 工作集群 - 更新过程中工作集群状态为「更新中」
            CP证书管理 - 工作集群 - 工作集群开始更新证书后，「更新集群证书」按钮转为 loading 状态，不可重复点击
            CP证书管理 - 工作集群 - UI - 工作集群更新完成后，「更新集群证书」按钮恢复正常，弹出 toast 显示「更新集群证书成功」
            CP证书管理 - 工作集群 - UI - 工作集群 CP 节点证书更新失败，「更新集群证书」按钮恢复正常，「集群证书管理」页 UI 显示error「更新集群证书失败。错误信息：xxx」
            CP证书管理 - 工作集群 - UI - 工作集群 CP 节点证书更新失败，「更新集群证书」按钮可再次点击触发更新，重新进入更新中状态
            CP证书管理 - 工作集群 - 工作集群 CP 节点依次原地更新，更新完的节点的证书过期时间显示变更为一年后，与后端 apiserver 证书显示时间相符
            CP证书管理 - 工作集群 - UI 显示更新完成后，在 CP 节点中执行 kubeadm certs check-expiration 查看所有 10 项控制平面证书，过期时间均已更新为一年后
            CP证书管理 - 工作集群 - 手动更新过控制平面证书完成后，可反复发起更新，每次按照更新时间生成新的期限的证书
            CP证书管理 - 工作集群 - 1 CP 虚拟机工作负载集群可手动更新 CP 证书
            CP证书管理 - 工作集群 - 3 CP 虚拟机工作负载集群可手动更新 CP 证书
            CP证书管理 - 工作集群 - 5 CP 虚拟机工作负载集群可手动更新 CP 证书
            CP证书管理 - 工作集群 - 1 CP 物理机工作负载集群可手动更新 CP 证书
            CP证书管理 - 工作集群 - 3 CP 物理机工作负载集群可手动更新 CP 证书
            CP证书管理 - 工作集群 - 5 CP 物理机工作负载集群可手动更新 CP 证书
            CP证书管理 - 工作集群 - 集群控制平面证书更新后，可创建和管理工作负载
        临期自动更新
            CP证书管理 - 自动更新 - 未手动更新的管控集群 CP 节点，距离过期时间点不足 7 天触发自动更新，逐个原地更新全部 CP 节点，重新签发证书，有效期 1 年
            CP证书管理 - 自动更新 - 未手动更新的工作负载集群 CP 节点，距离过期时间点不足 7 天触发自动更新，逐个原地更新全部 CP 节点，重新签发证书，有效期 1 年
            CP证书管理 - 自动更新 - 临期集群成功进行手动更新后，证书有效期已延长，不再触发自动更新
            CP证书管理 - 自动更新 - 手动更新过程中，到达自动更新时间点，不再触发自动更新，仅执行手动更新
            CP证书管理 - 自动更新 - 距离自动更新时间点大于7天不足8天,不触发自动更新
        后端新增
            CP证书管理 - HostOperationJob - 证书刷新生成独立的 HostOperationJob 执行
            CP证书管理 - Ansible - kubeadm certs renew all -v=5 命令执行成功
            CP证书管理 - Ansible - 4 个 K8s CP 组件 Pod 正确重启(crictl stop 命令执行成功)，组件容器运行状态检查通过，不发生 pod 驱逐
            CP证书管理 - Ansible - 执行 kubeadm certs check-expiration 验证证书更新成功
            CP证书管理 - KSC - 已存在的 KSC 中配置的 rolloutBefore.CertificatesExpiryDays 默认值保持原有值 30 天
            CP证书管理 - KSC - 新建集群 KSC 中配置的 rolloutBefore.CertificatesExpiryDays 默认值修改为 7 天
            CP证书管理 - KSC - 向 KSC 添加 kubesmart.smtx.io/need-renew-control-plane-certs annotation 触发更新，webhook 同时生成 kubesmart.smtx.io/renew-cp-certs-issued-before annotation 并记录当前时间
            CP证书管理 - KSC - kubesmart.smtx.io/renew-control-plane-certs-issued-before annotation 记录的时间格式为 RFC3339 格式
            CP证书管理 - ExtraConfig - 新增certificateRenewalTime 字段正确记录证书刷新时间
            CP证书管理 - ExtraConfig - certificateRenewalTime 发生改变时，触发原地更新
            CP证书管理 - KCP - 新创建集群不再填入 rolloutBefore.certificatesExpiryDay 字段
            CP证书管理 - KCP - SKS 升级后的集群原有 rolloutBefore.certificatesExpiryDay 字段被清空
            CP证书管理 - Machine - cp 节点对应的 machine.Status.CertificatesExpiryDate 中记录过期时间
            CP证书管理 - 使用 cp 节点对应的最早的 machine.Status.CertificatesExpiryDate 和 KSC 中配置的 CertificatesExpiryDays 计算出的更新时间到达后，触发自动原地更新
            CP证书管理 - 证书签发时间 - 从 CP 节点对应的 kubeadmconfig 资源的 machine.cluster.x-k8s.io/certificates-expiry annotation 获取过期时间，向前推 1 年为签发时间
            CP证书管理 - 证书签发时间 - CP 组件证书签发时间早于 CertificateRenewalTime 时触发更新
            CP证书管理 - 原地更新优化 - 其他配置更新引起的 CP 节点原地更新不会刷新证书时间
            CP证书管理 - 原地更新优化 - 存量证书过期时间不对齐的集群,手动刷新后全部证书时间重新对齐
            CP证书管理 - IUM - 节点证书更新过程中，对应 IUM 中 CertificateRenewal condition 的 status 记录为 False
            CP证书管理 - IUM - 节点证书更新完成，对应 IUM 中 CertificateRenewal condition 的 status 记录为 True
            CP证书管理 - IUMG - CP 节点组中还有节点处于证书更新过程中，对应 IUMG 中 CertificateRenewal condition 的 status 记录为 False
            CP证书管理 - IUMG - CP 节点组中所有节点证书更新完成，对应 IUMG 中 CertificateRenewal condition 的 status 记录为 True
            CP证书管理 - KSC - KSC 中 CertificateRenewal condition 的 status 同步 IUMG 中 status
            CP证书管理 - condition - reason - 节点证书更新过程中，reason 记录为 CertificateRenewalInProgress
            CP证书管理 - condition - reason - 节点证书更新 HostOperationJob 创建失败，reason 记录为 CertificateRenewalCreateJobFailed
            CP证书管理 - condition - reason - 节点证书更新失败，reason 记录为 CertificateRenewalFailed
        Event/日志
            CP证书管理 - Event - 手动更新节点证书成功，生成对应的原地更新成功事件
            CP证书管理 - Event - 手动更新节点证书失败，生成对应的原地更新失败事件
            CP证书管理 - Event - 自动更新节点证书成功，生成对应的原地更新成功事件
            CP证书管理 - Event - 自动更新节点证书失败，生成对应的原地更新失败事件
            CP证书管理 - Event - 手动触发证书更新产生对应事件记录
            CP证书管理 - Audit - 手动触发证书更新产生对应的审计信息
            CP证书管理 - 日志 - 证书刷新开始时记录日志
            CP证书管理 - 日志 - 证书刷新成功时记录日志
            CP证书管理 - 日志 - 证书刷新失败时记录详细错误日志
            CP证书管理 - 日志 - HostOperationJob 执行过程记录详细日志
        权限
            CP证书管理 - 权限 - root 超级管理员用户，可更新管控集群和工作集群证书
            CP证书管理 - 权限 - 系统管理员用户，可更新管控集群和工作集群证书
            CP证书管理 - 权限 - 只读用户，不可更新管控集群和工作集群证书，更新按钮不可见
            CP证书管理 - 权限 - 仅授予了 SKS 服务管理权限的用户，可以更新管控集群证书，更新按钮可见
            CP证书管理 - 权限 - 仅授予了 SKS 服务管理权限的用户，不可更新工作集群证书，更新按钮不可见
            CP证书管理 - 权限 - 无 SKS 服务管理权限的用户，无法更新管控集群证书，更新按钮不可见
            CP证书管理 - 权限 - 被取消 SKS 服务管理权限的用户，不刷新 UI，点击管控集群「更新集群证书」按钮，提示无权限，返回 403
            CP证书管理 - 权限 - 仅授予了编辑工作负载集群权限的用户，不可更新管控集群证书，更新按钮不可见
            CP证书管理 - 权限 - 仅授予了编辑工作负载集群权限的用户，可以更新工作集群证书，更新按钮可见
            CP证书管理 - 权限 - 无编辑工作负载集群权限的用户，无法更新工作集群证书，更新按钮不可见
            CP证书管理 - 权限 - 被取消编辑工作负载集群权限的用户，不刷新 UI，点击「更新集群证书」按钮，提示无权限，返回 403
        报警
            CP证书管理 - 报警 - 检查报警规则
            CP证书管理 - 报警 - 单 CP 节点距离自动更新时间点 30 天触发 Notice 级别报警
            CP证书管理 - 报警 - 单 CP 节点距离自动更新时间点 7 天触发 Critical 级别报警
            CP证书管理 - 报警 - 多个 CP 节点过期时间不同，其中任意一个距离自动更新时间点不足 30 天，即触发 Notice 级别报警
            CP证书管理 - 报警 - 多个 CP 节点过期时间不同，其中任意一个距离自动更新时间点不足 7 天，即触发 Critical 级别报警
            CP证书管理 - 报警 - 调整 KubeAPIServeCertificateAutomaticallyUpdatedSoon Notice 级别阈值，可按时触发/解决报警
            CP证书管理 - 报警 - 调整 KubeAPIServeCertificateAutomaticallyUpdatedSoon Critical 级别阈值，可按时触发报警
            CP证书管理 - 报警 - 管控集群产生 KubeAPIServeCertificateAutomaticallyUpdatedSoon Notice 报警后，手动更新集群证书，报警解除
            CP证书管理 - 报警 - 管控集群产生 KubeAPIServeCertificateAutomaticallyUpdatedSoon Critical 报警后，手动更新集群证书，报警解除
            CP证书管理 - 报警 - 工作集群产生 KubeAPIServeCertificateAutomaticallyUpdatedSoon Notice 报警后，手动更新集群证书，报警解除
            CP证书管理 - 报警 - 工作集群产生 KubeAPIServeCertificateAutomaticallyUpdatedSoon Critical 报警后，手动更新集群证书，报警解除
            CP证书管理 - 报警 - 工作集群产生 KubeAPIServeCertificateAutomaticallyUpdatedSoon 报警后，升级集群 K8s 版本，报警解除
            CP证书管理 - 报警 - 工作集群产生 KubeAPIServeCertificateAutomaticallyUpdatedSoon 报警后，替换集群临期 CP 节点，报警解除
            CP证书管理 - 报警 - 调整过自动更新触发时间的集群，报警时间按照调整后的更新时间点计算和触发（但目前 UI hardcode 提示7天）
            CP证书管理 - 报警 - 多个集群同时触发报警，每个集群独立报警，在各自集群中可查看报警详情
        其他
            CP证书管理 - 幂等检查 - 快速多次点击更新按钮，只触发一次更新
            CP证书管理 - 并发 - 可同时触发多个集群的证书更新
            CP证书管理 - 升级兼容 - 旧版本升级到 1.6.0 的 SKS 集群，ytt 版本未更新，更新证书，仅更新KSC annotation，不触发实际更新动作
            CP证书管理 - 升级兼容 - 旧版本升级到 1.6.0 的 SKS 集群，ytt 版本已更新，证书更新功能可用
            CP证书管理 - 更新耗时 - 记录单 CP 节点证书更新时间，在合理范围内，同宿主集群约为单节点 1 倍
            CP证书管理 - 更新耗时 - 记录 3 CP 节点证书更新时间，在合理范围内，同宿主集群约为单节点 3 倍
            CP证书管理 - 更新耗时 - 记录 5 CP 节点证书更新时间，在合理范围内，同宿主集群约为单节点 5 倍
            K8s 版本兼容性
                CP证书管理 - K8s 版本 - K8s v1.26 集群，证书更新功能可用
                CP证书管理 - K8s 版本 - K8s v1.27 集群，证书更新功能可用
                CP证书管理 - K8s 版本 - K8s v1.28 集群，证书更新功能可用
                CP证书管理 - K8s 版本 - K8s v1.29 集群，证书更新功能可用
                CP证书管理 - K8s 版本 - K8s v1.30 集群，证书更新功能可用
                CP证书管理 - K8s 版本 - K8s v1.31 集群，证书更新功能可用
            Base OS 兼容性
                CP证书管理 - Base OS - Rocky 8.10 集群，证书更新功能可用
                CP证书管理 - Base OS - Rocky 9.6 集群，证书更新功能可用
                CP证书管理 - Base OS - OpenEuler 22.03 x86_64 集群，证书更新功能可用
                CP证书管理 - Base OS - OpenEuler 22.03 aarch64 集群，证书更新功能可用
                CP证书管理 - Base OS - TencentOS 3.3 x86_64 集群，证书更新功能可用
                CP证书管理 - Base OS - TencentOS 3.3 aarch64 集群，证书更新功能可用
                CP证书管理 - Base OS - Kylin v10 x86_64 集群，证书更新功能可用
                CP证书管理 - Base OS - Kylin v10 aarch64 集群，证书更新功能可用
        异常
            CP证书管理 - 更新失败 - UI 展示更新失败的错误信息
            CP证书管理 - 更新失败 - 集群状态 failed 后，可再次触发手动更新，
            CP证书管理 - 异常 - CP 节点处于未就绪状态时，CP 组件状态正常，则证书更新操作可能成功，但原地更新流程会因节点异常而阻塞，导致集群更新失败
            CP证书管理 - 异常 - 更新过程中 CP 节点重启，更新证书失败，可自动重试后成功
            CP证书管理 - 异常 - 更新过程中管控集群重启，更新证书失败，重启完成后可自动恢复重试
            CP证书管理 - 异常 - 网络异常 CP 节点失去连接处于未知状态时，证书更新会因 hoj 一直无响应阻塞在更新中，最终集群更新失败
            CP证书管理 - 异常 - 3 CP 节点中仅有1个证书过期，可以成功更新
            CP证书管理 - 异常 - 5 CP 节点中仅有2个证书过期，可以成功更新
            CP证书管理 - 异常 - 特定 CP 节点证书更新失败后，会持续 reconcile 重试，集群状态一段时间后会被标记为失败，并显示原因
            CP证书管理 - 异常 - 证书更新过程中出现上级集群和 CP 节点间的管理网络中断，更新失败，网络恢复后，更新可成功
            CP证书管理 - 异常 - kubeadm certs renew all 命令执行失败时可正确报错
            CP证书管理 - 异常 - CP 组件 Pod 重启失败时可正确报错
            CP证书管理 - EC - 创建 HostOperationJob 失败时，返回错误码 SKS_INPLACE_UPDATE_CERTIFICATE_RENEWAL_CREATE_JOB_FAILED: 无法为节点 {node} 创建证书更新任务
            CP证书管理 - EC - 更新任务一直处于进行中状态时，返回错误码 SKS_INPLACE_UPDATE_CERTIFICATE_RENEWAL_IN_PROGRESS: 正在等待节点 { node } 的证书更新任务完成。
            CP证书管理 - EC - HostOperationJob 执行失败时，返回错误码 SKS_INPLACE_UPDATE_CERTIFICATE_RENEWAL_JOB_FAILED: 节点 {node} 的证书更新任务失败。
        其他会引起证书更新的场景
            CP证书管理 - 其他更新场景 - 替换 CP 节点后，特定 CP 节点的所有控制平面证书更新，有效期 1 年
            CP证书管理 - 其他更新场景 - 升级集群 K8s 版本后，所有 CP 节点的控制平面证书更新
            CP证书管理 - 其他更新场景 - 引起 CP 节点组滚动的后端操作均会引起 CP 节点控制平面证书更新
            CP证书管理 - 其他更新场景 - 升级有模板变更的 SKS 服务版本后，管控集群节点滚动更新，所有 CP 节点的控制平面证书更新
            CP证书管理 - 其他更新场景 - 无模板变更的 SKS 服务版本升级，管控集群节点不发生滚动，CP 节点的证书不发生更新
    SKS 1.6 智能安全策略集成
        ER策略环境感知
            SKS服务管理
                SKS部署-无域名和CA的Registry可正常部署成功
                SKS部署-使用域名的Registry可正常部署成功
                SKS部署-添加CA证书的Registry可正常部署成功
                SKS部署-SKS服务可正常部署成功，镜像拉取正常
                SKS部署-tower带ntp，Registry可正常部署成功，NTP可正常配置
                SKS部署-tower带ntp，SKS服务可正常部署成功，镜像拉取正常
                SKS部署-管控集群使用默认pod/service cidr配置，可正常部署成功
                SKS部署-管控集群自定义pod/service cidr配置，可正常部署成功
                SKS部署-服务部署成功后，管控集群关联obs并开启可观测性服务，可关联成功，功能正常
                SKS管理-开启OBS的管控集群，关闭obs服务，可保存成功，相关组建清理
                SKS管理-关联全局容器镜像仓库，可配置成功，镜像拉取正常，创建工作集群时自动配置
                SKS管理-添加SMTX ZBS CSI接入配置，可添加成功，创建zbs csi工作集群时正常，创建卷正常 - 需要提前放通端口
                SKS管理-上传节点相关文件，可正常上传
                SKS管理-删除节点相关文件，可正常删除
                SKS管理-添加物理机，可添加成功，连接正常，创建物理机时正常
                SKS管理-编辑物理机信息，可编辑成功，连接正常
                SKS管理-删除物理机，可删除成功，连接正常
                SKS管理-创建工作集群IP池，可创建成功，创建工作集群时正常使用及分配ip
                SKS管理-编辑工作集群IP池，可编辑成功，工作集群时正常使用及分配ip
                SKS管理-删除工作集群IP池，可删除成功
                SKS管理-创建zbs csi使用的IP池，可创建成功，创建zbs csi工作集群时csi正常使用及分配ip
                SKS管理-更新软件许可，更新成功，许可正常使用
                SKS管理-全局配置，检查ntp配置自动同步，正常同步
                SKS管理-全局配置，手动点击同步NTP配置，可同步成功，时间同步
                SKS管理-全局配置，配置ntp服务，配置成功，时间同步
                SKS管理-暂停及恢复同步管控集群，可触发成功
                SKS管理-管控集群下载Kubeconfig，可下载成功，本地使用kubeconfig访问管控集群正常
                SKS管理-管控集群提升模式，可提升成功，服务正常
                SKS管理-升级管控集群，可正常升级，升级后服务正常
                SKS管理-升级管控集群k8s版本，可正常升级，多次升级成功，升级后服务正常
                SKS管理-卸载管控集群，可卸载成功，相关联资源完全清理无残留
                SKS管理-卸载管控集群后清理registry，可删除成功，相关联资源完全清理无残留
                未关联ER的SMTX OS集群-正常创建SKS服务后，关联ER服务，关联成功，SKS服务正常不受影响
                创建SKS服务后关联ER服务-操作SKS服务的管理，服务正常
                有SKS服务的SMTX OS集群取消关联ER服务-未创建工作集群，取消关联成功，SKS服务正常不受影响
            创建工作集群
                创建工作集群 - 在SKS服务同SMTX OS集群上创建工作集群，可正常创建成功，镜像拉取正常
                创建工作集群 - 在未关联ER的SMTX OS集群上创建工作集群，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建虚拟机工作集群，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建物理机工作集群，物理节点在其他集群，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建虚拟机工作集群，网卡为单网卡配置，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建虚拟机工作集群，网卡为多网卡配置，同子网，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建虚拟机工作集群，网卡为多网卡配置，不同子网，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建虚拟机工作集群，CNI为Calico，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建虚拟机工作集群，CNI为EIC，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建虚拟机工作集群，CSI为ELF，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建虚拟机工作集群，CSI为ZBS，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建虚拟机工作集群，使用静态ippool分配ip，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建虚拟机工作集群，使用DHCP分配ip，可正常创建成功，镜像拉取正常-需额外开放端口
                创建工作集群 - tower配置ntp并在SKS同步，创建工作集群，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建工作集群时关联obs并开启监控日志等插件，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建工作集群时开启lb/ingress插件，可正常创建成功，镜像拉取正常
                创建工作集群 - 创建工作集群时开启全插件，可正常创建成功，镜像拉取正常
            管理工作集群
                已有工作集群-关联OBS服务并开启监控日志等组件，可正常开启，镜像拉取正常
                已有工作集群-开启LB/Ingress，配置Ip，可正常开启，镜像拉取正常
                已有工作集群-添加容器镜像仓库，可添加成功，镜像拉取正常
                已有工作集群-已开启监控、日志、事件、审计组件时，查看后续数据获取，获取正常
                已有工作集群-更新k8s集群配置，触发原地更新，可更新成功
                已有工作集群-编辑节点组，删除节点，可删除成功，集群恢复正常
                已有工作集群-编辑节点组，增加节点，可创建成功，集群恢复正常
                已有工作集群-手动替换节点，可替换成功，集群恢复正常
                已有工作集群-开启自动伸缩，触发节点自动伸缩，功能正常
                已有工作集群-开启故障节点自动替换，触发自动替换，功能正常
                已有工作集群-升级k8s版本，可正常升级，升级后功能正常
                已有工作集群-取消关联OBS服务，可取消成功，相关组建可正常清理
                已有工作集群-点击查看集群控制台，可正常连接，命令执行正常，控制台交互正常
                已有工作集群-编辑集群显示名称，可编辑成功，显示名称更新
                已有工作集群-暂停同步/恢复同步，执行成功
                已有工作集群-点击查看节点控制台，可正常连接，命令执行正常，控制台交互正常
                已有工作集群-点击查看pod控制台，可正常连接，命令执行正常，控制台交互正常
                已有工作集群-在pod控制台上传/下载文件，可正常上传下载
                已有工作集群-创建持久卷，可正常创建
                已有工作集群-删除持久卷，可正常删除
                已有工作集群-创建PVC，可正常创建
                已有工作集群-编辑PVC分配量，可正常编辑
                已有工作集群-删除PVC，可正常删除，持久卷清理
                已有工作集群-管理员用户，管理应用负载资源，功能正常
                已有工作集群-集群使用者用户，管理应用负载资源，功能正常，权限正常
                已有工作集群-管理员用户，管理项目相关资源，功能正常
                已有工作集群-集群使用者用户，查看租户集群及详情，功能正常，权限正常
                已有工作集群-工作集群使用者和容器镜像仓库用户，查看租户集群及详情，功能正常，权限正常
                已有工作集群-工作集群使用者和容器镜像仓库用户，查看用户镜像仓库页面，展示正常
                删除工作集群-无其他ER策略关联，删除成功，资源完全清理
                删除工作集群-有其他ER策略通过标签关联，删除成功，资源除标签外清理---TBD
                创建在未关联ER的SMTX OS上的工作集群-不受ER策略影响，运行正常
                创建在未关联ER的SMTX OS上的工作集群-不受ER策略影响，可正常删除
                有多个ER服务，关联不同SMTX OS集群，均创建工作负载集群，相互不受影响
                创建工作集群时未关联ER-创建后关联ER，集群工作正常，开关插件正常
            用户容器镜像仓库
                创建用户容器镜像仓库 - 在关联ER的集群上创建user-registry，可正常创建成功
                创建用户容器镜像仓库 - 在关联ER的集群上创建user-registry，使用域名，可正常创建成功
                使用用户容器镜像仓库-已创建的工作集群添加用户容器镜像仓库，可正常添加成功
                使用用户容器镜像仓库-在工作集群中创建工作负载时，拉取用户容器镜像仓库的镜像，可正常创建Secret，正常拉取镜像
                在未关联ER的SMTX OS上创建容器镜像仓库-可正常创建，不受影响
                未关联ER时创建容器镜像仓库-创建后关联ER服务，关联后镜像可正常使用，不受影响
                已关联ER-编辑容器镜像仓库，扩容成功，不受影响
                已关联ER-删除容器镜像仓库，可删除成功，资源清理完全
        安全策略自动创建及更新
            tower k8s中新增CRD「Everoutesecuritypolicie」- sks-controller 在监测到符合创建条件时创建和reconcile
            默认安全策略描述-This policy is automatically created by the SKS system to ensure the normal operation of core cluster services. Do not manually modify or delete.
            tower 上所有开启了分布式防火墙且已关联 elf 集群的 ER 服务，且开启全局拒绝-均会创建 SKS 容器镜像仓库虚拟机安全策略
            UI编辑默认策略-增加端口配置，保存 - 保存后刷回 esp 中的配置
            UI编辑默认策略-删除端口配置，保存 - 保存后刷回 esp 中的配置
            检查registry默认策略配置
            已有SKS容器镜像仓库，关联ER-在tower k8s中自动创建registry 「Everoutesecuritypolicies - esp」
            已有SKS容器镜像仓库，关联ER-在er上自动创建默认安全策略，更新esp.spec.securityPolicy，与UI安全策略对应一致
            已关联ER，新创建SKS容器镜像仓库-在tower k8s中自动创建registry 「Everoutesecuritypolicies - esp」
            已关联ER，新创建SKS容器镜像仓库-在er上自动创建默认安全策略，更新esp.spec.securityPolicy，与UI安全策略对应一致
            已有用户容器镜像仓库，与SKS容器镜像仓库同集群-自动加入regsitry安全策略
            已关联ER，新创建用户容器镜像仓库与SKS容器镜像仓库同集群-自动加入regsitry安全策略
            已有用户容器镜像仓库，与SKS容器镜像仓库不同集群，但关联同ER-自动加入regsitry安全策略
            已关联ER，新创建用户容器镜像仓库与SKS容器镜像仓库不同集群但同ER-自动加入regsitry安全策略
            已有用户容器镜像仓库，与SKS容器镜像仓库不同集群，且关联不同的ER-可生效registry安全策略
            已关联ER，新创建用户容器镜像仓库与SKS容器镜像仓库不同集群且不同ER-自动生效regsitry安全策略
            已创建SKS管控集群，关联ER-在tower k8s中自动创建mgmt 「Everoutesecuritypolicies - esp」
            已创建SKS管控集群，关联ER-在er上自动创建默认安全策略，更新esp.spec.securityPolicy，与UI安全策略对应一致
            已关联ER，新创建SKS服务-在tower k8s中自动创建mgmt 「Everoutesecuritypolicies - esp」
            已关联ER，新创建SKS服务-在er上自动创建默认安全策略，更新esp.spec.securityPolicy，与UI安全策略对应一致
            检查SKS服务默认策略配置
            已创建工作集群，关联ER同SKS服务-在管控集群 k8s中自动创建「Everoutesecuritypolicies - esp」
            已创建工作集群，关联ER同SKS服务-在er上自动创建默认安全策略，更新esp.spec.securityPolicy，与UI安全策略对应一致
            已关联ER，新创建工作集群-在管控集群 k8s中自动创建「Everoutesecuritypolicies - esp」
            已关联ER，新创建工作集群-在er上自动创建默认安全策略，更新esp.spec.securityPolicy，与UI安全策略对应一致
            创建工作集群，所在SMTXOS集群未关联ER-不会创建安全策略
            创建工作集群，所在SMTXOS集群关联 不同ER-自动创建安全策略
            关联ER的管控集群-关联可观测服务并开启插件，自动更新安全策略，增加相关端口
            关联ER的工作集群-关联可观测服务并开启插件，自动更新安全策略，增加相关端口
            检查工作集群默认策略配置
            tower配置ntp服务 - 在esp中自动添加ntp相关安全策略，同时安全策略中新增
            tower更新ntp服务 - 在esp中自动添加ntp相关安全策略，同时安全策略中新增
            SKS服务关联OBS - 在esp中自动添加obs相关安全策略，同时安全策略中新增
            SKS服务取消关联OBS - 在esp中自动清理obs相关安全策略，同时安全策略中删除
            工作集群关联OBS - 在工作集群对应的esp中自动添加obs相关安全策略，同时安全策略中新增
            工作集群取消关联OBS - 在工作集群对应的esp中自动清理obs相关安全策略，同时安全策略中删除
            同个ER -创建多个用户容器镜像仓库，均加入同个registry安全策略，策略生效正常
            多个ER关联不同集群 - 创建多个不同集群上用户容器镜像仓库 - 策略生效正常
            已有工作集群 - 增加或删除节点，可自动加入或移除安全策略，不影响集群运行
            SKS管控集群 - 升级时增加/删除节点，可自动加入或移除安全策略，不影响SKS服务运行
            SKS管控集群 - 提升模式节点，可自动加入安全策略，不影响SKS服务运行
        安全策略命名及标签
            registry esp名称 - sks-security-policy-registry，namespace与管控集群ksc一致
            registry安全策略名称 - sks-security-policy-registry，与esp一致
            管控集群 esp名称 - sks-mgmt-${sksClusterUID 前8位}，namespace与管控集群ksc一致
            管控集群 安全策略 - sks-mgmt-${sksClusterUID 前8位}，与esp一致
            工作集群 esp名称 - ${clustername}-${sksClusterUID 前8位}，namespace与ksc一致
            工作集群 安全策略 - ${clustername}-${sksClusterUID 前8位}，与esp一致
            registry虚拟机 新增标签 - sks/ake-security-policy:registry
            SKS管控集群复用已有标签 -  sks/ake-cluster-name:sks/ake-mgmt，sks/ake-namespace:default
            工作集群复用已有标签 - sks/ake-cluster-name:{{ksc.name}}，sks/ake-namespace:{{ksc.namespace}}
            删除registry虚拟机标签，一段时间后自动重新关联，期间策略失效，重新关联后生效
            删除管控集群虚拟机标签，一段时间后自动重新关联，期间策略失效，重新关联后生效
            删除工作集群虚拟机标签，一段时间后自动重新关联，期间策略失效，重新关联后生效
        安全策略的清理
            删除工作负载集群 - 删除成功，策略自动清理，删除成功，删除esp上finalizeresp.kubesmart.smtx.io
            删除工作负载集群 - ksc删除成功，ksc-controller自动删除对应esp
            卸载SKS服务，删除管控集群-删除成功，策略自动清理，删除成功，删除esp上finalizeresp.kubesmart.smtx.io
            卸载SKS服务，删除管控集群 - ksc删除成功，ksc-controller自动删除对应esp
            卸载SKS服务，删除容器镜像仓库-删除成功，策略自动清理，删除成功，删除esp上finalizeresp.kubesmart.smtx.io
            卸载SKS服务，删除容器镜像仓库 - 删除成功，ksc-controller自动删除对应esp
            卸载SKS服务成功 - esp对应的CRD自动删除
            手动删除ER安全策略-可删除成功，一段时间后自动重建
            手动删除esp-ER安全策略同时自动删除 ，一段时间后esp和ER安全策略自动重建
            SKS服务正常，删除同ER上用户容器镜像仓库-删除成功，策略中user-registry的vm清理，策略不会自动清理，正常运行，不受影响
            同ER有用户容器镜像仓库，卸载SKS服务删除容器镜像仓库-删除成功，策略中sks-registry的vm清理，策略会自动清理，用户仓库受影响
            SKS服务正常，删除不同ER上用户容器镜像仓库-删除成功，策略不会清理
            有ER关联的SKS服务，工作正常 - 取消关联ER服务，取消关联成功，SKS服务及集群不受影响，工作正常
        升级处理
            未部署ER的SKS1.5环境-升级SKS1.6环境，正常升级成功，不受任何影响
            部署了3.2.0+ER的SKS1.5环境 - 未关联obs，升级SKS1.6环境，升级成功，自动创建registry、管控集群、工作集群安全策略
            部署了3.2.0+ER的SKS1.5环境 - 未关联obs，升级SKS1.6环境，升级成功，管理obs开启插件，开启成功，拉取镜像正常
            部署了3.2.0+ER的SKS1.5环境 - 关联obs开启插件，升级SKS1.6环境，升级成功，自动创建registry、管控集群、工作集群安全策略
            部署了3.2.0+ER的SKS1.5环境 - 关联obs开启插件，升级SKS1.6环境，升级成功，关闭并重开查看，可开启成功
            部署了3.2.0+ER的SKS1.5环境 - 升级SKS1.6环境，升级成功，创建新的工作集群，创建成功，插件开启正常
            部署了3.2.0+ER的SKS1.5环境 - 升级SKS1.6环境，升级成功，升级工作集群ytt版本，原地更新成功，工作正常
            部署了3.2.0+ER的SKS1.5环境 - 升级SKS1.6环境，升级成功，升级工作集群k8s版本，滚动成功，工作正常
            部署了3.2.0+ER的SKS1.5环境 - 升级SKS1.6环境，升级成功，删除工作集群，可正常删除成功
            部署了3.2.0+ER的SKS1.5环境 - 升级SKS1.6环境，升级成功，卸载SKS服务，可正常卸载成功
            部署了3.2.0+ER的SKS1.5环境 - 仅升级tower至4.9.0，不会触发策略自动创建
            部署了3.2.0+ER的SKS1.5环境 - 不升级sks registry，升级SKS服务，升级完成，sks-registry会新增标签并自动创建安全策略，工作正常
            部署了3.2.0+ER的SKS1.5环境 - 不升级sks registry，升级SKS服务，升级完成后，升级sks-registry，可正常升级成功，工作正常
            部署了3.2.0+ER的SKS1.5环境 - 升级SKS服务，升级完成，user-registry会新增标签并自动增加安全策略，工作正常
            部署了3.2.0+ER的SKS1.5环境 - 升级SKS服务，升级完成后，升级user-registry，可正常升级成功，工作正常
            部署了3.2.0+ER的SKS1.5环境 - 升级SKS服务，升级完成后，查看原EIC集群工作正常
            部署了3.2.0+ER的SKS1.5环境 - 升级SKS服务，升级完成后，查看原Calico集群工作正常
            部署了3.2.0+ER的SKS1.5环境 - 升级SKS服务，升级完成后，同步ntp配置，可正常同步
            部署了3.2.0+ER的SKS1.5环境 - 升级SKS服务，升级完成后工作正常，取消关联ER，取消成功，工作正常
            部署了3.2.0+ER的SKS1.5环境 - 有通过标签创建自定义安全策略，升级成功后，验证相互策略是否影响
            部署了3.2.0+ER的SKS1.5环境 - 升级SKS服务，升级完成后工作正常，升级ER至最新版本，可升级成功，期间SKS不受影响
        关联验证
            EIC集群，不影响e2e执行
            EIC集群，对ippool功能不受影响
            EIC集群，为pod分配固定ip后重启pod后，arp外网可ping通
            Event-registry的esp创建，tower k8s记录事件
            Event-registry的esp更新，tower k8s记录事件
            Event-registry的esp删除，tower k8s记录事件
            Event-管控集群的esp创建，tower k8s不会记录事件，有sks-controller日志
            Event-管控集群的esp更新，tower k8s记录事件
            Event-管控集群的esp删除，tower k8s不会记录事件，有sks-controller日志
            Event-工作集群的esp创建，管控集群记录事件
            Event-工作集群的esp更新，管控集群记录事件
            Event-工作集群的esp删除，管控集群不会记录事件，有sks-controller日志
    支持管控集群升级K8s 版本
        SKS 服务升级前置检查
            管控集群 K8s 升级 - 服务升级 UI 变更 - 前置检查页面布局 - img
            管控集群 K8s 升级 - SKS 升级前置检查 - 上传前置检查文件仅 JSON 格式文件可选
            管控集群 K8s 升级 - SKS 升级前置检查 - UI- 上传新版本安装包的 metadata JSON 文件，「升级前检查按钮」变更为可用状态
            管控集群 K8s 升级 - SKS 升级前置检查 - UI- 页面上选中前置检查文件和升级文件后，重新选择前置检查文件，升级文件上传 UI 被隐藏，需要重新触发升级前检查并上传升级文件
            检查通过可直接升级
                管控集群 K8s 升级 - SKS 升级前置检查 - UI - 上传升级目标版本K8s version 为 v1.27 的 metadata JSON 文件，点击「升级前检查」，显示「升级前检查通过，可进行服务升级。」并显示升级 UI
                管控集群 K8s 升级 - SKS 升级前置检查 - UI - 上传升级目标版本K8s version 为 v1.28 的 metadata JSON 文件，点击「升级前检查」，显示「升级前检查通过，可进行服务升级。」并显示升级 UI
                管控集群 K8s 升级 - SKS 升级前置检查 - UI - 前置检查通过，检查服务升级 UI - img
                管控集群 K8s 升级 - SKS 升级前置检查 - UI - 前置检查通过，切换 UI，再回到服务升级页，服务升级 UI 被隐藏，前置检查文件需重新选择
            检查未通过
                管控集群 K8s 升级 - SKS 升级前置检查 - UI - 前置检查未通过，展示 error 文案及「升级管控集群 Kubernetes 版本」link - img
                管控集群 K8s 升级 - SKS 升级前置检查 - UI - 前置检查未通过，不提供 SKS 服务升级入口
                管控集群 K8s 升级 - SKS 升级前置检查 - UI - 前置检查未通过，移除前置检查文件，UI 恢复为前置检查初始页面
                管控集群 K8s 升级 - SKS 升级前置检查 - UI - 上传升级目标版本K8s version 为 v1.29 的 metadata JSON 文件，点击「升级前检查」，检查不通过，显示「无法升级到 %目标版本%。当前的管控集群 Kubernetes 版本为 v1.27，低于此版本要求的最低版本 v1.28。」
                管控集群 K8s 升级 - SKS 升级前置检查 - UI - 上传升级目标版本K8s version 为 v1.32 的 metadata JSON 文件，点击「升级前检查」，检查不通过，显示「无法升级到 %目标版本%。当前的管控集群 Kubernetes 版本为 v1.27，低于此版本要求的最低版本 v1.31。」
                管控集群 K8s 升级 - SKS 升级前置检查 - UI - 一次升级后，再上传升级目标版本K8s version 为 v1.32 的 metadata JSON 文件，点击「升级前检查」，检查不通过，显示「无法升级到 %目标版本%。当前的管控集群 Kubernetes 版本为 v1.28，低于此版本要求的最低版本 v1.31。」
                管控集群 K8s 升级 - SKS 升级前置检查 - UI - metadata JSON 中 K8s 的 major.minor 版本号小于当前管控集群 K8s 版本，点击「升级前检查」，前端报错：Kubernetes 版本低于当前管控集群的版本，不支持降级。- img
        服务升级
            管控集群 K8s 升级 - 服务升级 - 选择的 metadata JSON 文件和安装包的文件名不匹配，（Blur+Onchange，submit）报错：前置检查文件和 SKS 升级文件名称不一致。
            管控集群 K8s 升级 - 服务升级SKS dev 版本 - 前置检查可通过，无需升级管控集群版本，可直接升级服务，md5 码从 metadata JSON 文件中获取
            管控集群 K8s 升级 - 服务升级 - 服务升级开始后，升级 UI 恢复升级前检查状态
            管控集群 K8s 升级 - 服务升级 - 服务升级开始后，关闭升级 UI 再重新打开，UI 重新回到初始的前置检查状态，再次升级需重新上传 json 文件触发前置检查
            管控集群 K8s 升级 - 服务升级 - 服务升级开始后，「升级」按钮被禁用
            管控集群 K8s 升级 - 服务升级 - 服务升级完成后，可再次进行新版本升级
            [Future] 管控集群 K8s 升级 - 服务升级 1.7 版本 - 前置检查不通过，升级管控集群版本后，可直接升级服务，md5 码从 metadata JSON 文件中获取
        管控集群 K8s 升级
            管控集群 K8s 升级 - 升级 K8s 版本 - UI - 点击动态展示的「升级管控集群 Kubernetes 版本」link，打开升级对话框，检查布局 - img
            管控集群 K8s 升级 - 升级 K8s 版本 - UI - 点击动态展示的「升级管控集群 Kubernetes 版本」link，打开升级对话框，点击「取消」关闭对话框后，可再次点击 link 打开
            管控集群 K8s 升级 - 升级 K8s 版本 - UI - 点击展开升级对话框中的「Kubernetes 版本」下拉菜单，检查下拉菜单布局 - img
            管控集群 K8s 升级 - 升级 K8s 版本 - UI - 升级对话框中选择「Kubernetes 版本」后，升级按钮可用，并展示 Notice Tip，检查提示内容及布局：「升级期间，通过 SKS UI 或 API 进行的管理操作可能会短暂地不可用或出现延迟，如创建集群、删除集群、修改集群配置等所有与 SKS 管控平面交互的功能。」 - img
            升级版本选择
                管控集群 K8s 升级 - 升级版本选择 - 第一次升级 - 升级下拉列表中仅 1.6.0 版本的同架构同OS K8s v1.28 版本模板可选择
                管控集群 K8s 升级 - 升级版本选择 - 第二次升级 - 升级下拉列表中仅 1.6.0 版本的同架构同OS K8s v1.29 版本模板可选择
                管控集群 K8s 升级 - 升级版本选择 - 第三次升级 - 升级下拉列表中仅 1.6.0 版本的同架构同OS K8s v1.30 版本模板可选择
                管控集群 K8s 升级 - 升级版本选择 - 第四次升级 - 升级下拉列表中仅 1.6.0 版本的同架构同OS K8s v1.31 版本模板可选择
                管控集群 K8s 升级 - 升级版本选择 - 带有SKS 1.5 所有节点模板的情况下，升级下拉列表中 1.6 版本之外的其他 SKS 发布版本的节点模板不可见
                管控集群 K8s 升级 - 升级版本选择 - 未上传升级所需的其他 K8s 版本节点模板，升级下拉列表为空，placeholder显示「无可升级的 Kubernetes 版本」，升级按钮不可用
            升级 K8s 版本
                管控集群 K8s 升级 - toast - 点击升级按钮，弹出 toast「升级管控集群 Kubernetes 版本」，icon 状态为进行中
                管控集群 K8s 升级 - 任务 - 点击升级按钮，开始升级后，升级对话框关闭，生成「升级管控集群 Kubernetes 版本」的 tower 任务
                管控集群 K8s 升级 - toast - 升级成功后，toast「升级管控集群 Kubernetes 版本」，icon 状态为成功
                管控集群 K8s 升级 - 任务 - 升级成功后，「升级管控集群 Kubernetes 版本」的 tower 任务状态转为成功
                管控集群 K8s 升级 - toast - 升级失败后，toast「升级管控集群 Kubernetes 版本」，icon 状态为失败
                管控集群 K8s 升级 - 任务 - 升级失败后，「升级管控集群 Kubernetes 版本」的 tower 任务状态转为失败，并显示对应 error message
                管控集群 K8s 升级 - 任务 - 升级失败后，服务概览页显示 Serious tip：管控集群升级失败，请尽快排查并处理。
                管控集群 K8s 升级 - K8s 升级 - SKS 1.6 管控集群经过一次升级到 v1.28，升级完成后，服务正常运行
                管控集群 K8s 升级 - K8s 升级 - SKS 1.6 管控集群经过二次升级到 v1.29，升级完成后，服务正常运行
                管控集群 K8s 升级 - K8s 升级 - SKS 1.6 管控集群经过三次升级到 v1.30，升级完成后，服务正常运行
                管控集群 K8s 升级 - K8s 升级 - SKS 1.6 管控集群经过四次升级到 v1.31，升级完成后，服务正常运行
                管控集群 K8s 升级 - K8s 升级 - 管控集群 K8s 版本升级过程中，管控集群状态显示为「升级中」
                管控集群 K8s 升级 - K8s 升级 - 管控集群 K8s 版本升级开始后，回到升级前检查 UI，重新点击「升级前检查」，如满足升级条件则展示服务升级入口
                管控集群 K8s 升级 - K8s 升级 - 管控集群 K8s 版本升级开始后，返回升级前检查 UI，重新点击「升级前检查」，升级前检查按钮处于disable 状态
                管控集群 K8s 升级 - K8s 升级 - 管控集群 K8s 版本升级开始后，关闭升级 UI 再重新打开，显示升级前检查 UI
                管控集群 K8s 升级 - K8s 升级 - 管控集群 K8s 版本升级开始后，UI 重新回到初始的前置检查状态，再次升级需重新上传 json 文件触发前置检查
            其他覆盖
                管控集群 K8s 升级 - K8s 升级 - K8s 升级过程，管控集群节点串行进行滚动更新
                管控集群 K8s 升级 - K8s 升级 - 普通模式 SKS 1.6 管控集群经过四次升级到 v1.31，升级完成后，可正常卸载服务
                管控集群 K8s 升级 - K8s 升级 - 高可用模式 SKS 1.6 管控集群经过四次升级到 v1.31，升级完成后，可正常卸载服务
                管控集群 K8s 升级 - K8s 升级 - Rocky OS x86_64 的 SKS 1.6 管控集群可成功升级到 v1.31
                管控集群 K8s 升级 - K8s 升级 - openEuler x86_64 的 SKS 1.6 管控集群可成功升级到 v1.31
                管控集群 K8s 升级 - K8s 升级 - openEuler aarch64 的 SKS 1.6 管控集群可成功升级到 v1.31
                管控集群 K8s 升级 - K8s 升级 - tencentOS x86_64 的 SKS 1.6 管控集群可成功升级到 v1.31
                管控集群 K8s 升级 - K8s 升级 - tencentOS aarch64 的 SKS 1.6 管控集群可成功升级到 v1.31
                管控集群 K8s 升级 - K8s 升级 - 关联了 OBS 的 SKS 1.6 管控集群可经过四次升级更新到 v1.31，升级完成后，可正常卸载服务
        权限
            管控集群 K8s 升级 - 权限 - 只读用户不可升级管控集群 K8s 版本，「升级前检查」按钮不可见
            管控集群 K8s 升级 - 权限 - 仅授予了 SKS 服务管理权限的用户，可以升级管控集群 K8s 版本
            管控集群 K8s 升级 - 权限 - 无 SKS 服务管理权限的用户，无法升级管控集群 K8s 版本，「升级前检查」按钮不可见
            管控集群 K8s 升级 - 权限 - 被取消 SKS 服务管理权限的用户，点击「升级前检查」按钮提示无权限
            管控集群 K8s 升级 - 权限 - 被取消 SKS 服务管理权限的用户，点击管控集群 K8s 版本升级对话框中的「升级」按钮提示无权限
            管控集群 K8s 升级 - 权限 - 被取消 SKS 服务管理权限的用户，点击服务升级的「升级」按钮提示无权限
    支持配置 Pod/Service IP CIDR
        管控集群
            配置 Pod/SVC IP CIDR - 管控集群 - 部署 SKS 的网络配置页底部增加「其他配置」UI 提供 Service/Pod IP CIDR 输入 - img
            配置 Pod/SVC IP CIDR - 管控集群 - 管控集群 Service IP CIDR 默认值为 10.250.252.0/22
            配置 Pod/SVC IP CIDR - 管控集群 - 管控集群 Pod IP CIDR 默认值为 172.31.224.0/20
            配置 Pod/SVC IP CIDR - 管控集群 - Pod IP CIDR 输入框下增加提示：请确保子网足够大，以确保至少可为每个节点分配 /26 的地址块。创建后不可更改。
            配置 Pod/SVC IP CIDR - 管控集群 - 使用默认配置部署 sks，部署后检查 KSC 和实际pod/svc ip，默认配置生效
            配置 Pod/SVC IP CIDR - 管控集群 - 仅修改 SKS 管控集群 Service IP CIDR 默认配置，部署后部 Service IP CIDR 使用自定义配置
            配置 Pod/SVC IP CIDR - 管控集群 - 仅修改 SKS 管控集群 Pod IP CIDR 默认配置，部署后部 Pod IP CIDR 使用自定义配置
            配置 Pod/SVC IP CIDR - 管控集群 - 修改 SKS 管控集群 Service 和 Pod IP CIDR 默认配置，部署后均使用自定义配置
            配置 Pod/SVC IP CIDR - 管控集群 - Service IP CIDR 为空，（Blur+Onchange，Submit）inline 提示错误：请填写 Service IP CIDR 块。
            配置 Pod/SVC IP CIDR - 管控集群 - Pod IP CIDR 为空，（Blur+Onchange，Submit）inline 提示错误：请填写 Pod IP CIDR 块。
            配置 Pod/SVC IP CIDR - 管控集群 - 输入错误格式的 Service IP CIDR，（Blur+Onchange）inline 提示错误：CIDR 块格式错误。
            配置 Pod/SVC IP CIDR - 管控集群 - 输入错误格式的 Pod IP CIDR，（Blur+Onchange）inline 提示错误：CIDR 块格式错误。
            配置 Pod/SVC IP CIDR - 管控集群 - 长度校验 - Service IP CIDR 掩码长度设置为大于 26，（Blur+Onchange）inline 提示错误：子网掩码长度仅支持 12–26 的整数。
            配置 Pod/SVC IP CIDR - 管控集群 - 长度校验 - Service IP CIDR 掩码长度设置为小于 12，（Blur+Onchange）inline 提示错误：子网掩码长度仅支持 8–26 的整数。
            配置 Pod/SVC IP CIDR - 管控集群 - 长度校验 - Service IP CIDR 掩码长度设置为 12-26 间的任意自然数，无报错，可配置
            配置 Pod/SVC IP CIDR - 管控集群 - 长度校验 - 普通模式管控集群，Pod IP CIDR 掩码长度设置为 23及以上的数字，（Blur+Onchange）inline 提示错误：子网掩码长度仅支持 8–22 的整数。
            配置 Pod/SVC IP CIDR - 管控集群 - 长度校验 - 高可用模式管控集群，Pod IP CIDR 掩码长度设置为 24及以上的数字，（Blur+Onchange）inline 提示错误：子网掩码长度仅支持 8–23 的整数。
            配置 Pod/SVC IP CIDR - 管控集群 - 长度校验 - Pod IP CIDR 掩码长度设置为小于 8，（Blur+Onchange）inline 提示错误：子网掩码长度仅支持 8–24 的整数。（高可用为 8-23）
            配置 Pod/SVC IP CIDR - 管控集群 - 长度校验 - 普通模式管控集群，Pod IP CIDR 掩码长度设置为 8-24 间的任意自然数，无报错，可配置
            配置 Pod/SVC IP CIDR - 管控集群 - 长度校验 - 高可用模式管控集群，Pod IP CIDR 掩码长度设置为 8-23 间的任意自然数，无报错，可配置
            配置 Pod/SVC IP CIDR - 管控集群 - 边界值 - Service/Pod IP CIDR 掩码长度设置为 26和24，部署普通模式SKS 服务，插件全开
            配置 Pod/SVC IP CIDR - 管控集群 - IP 转换 - Service/Pod IP CIDR 仅修改掩码长度为16，为不合法配置，部署失败
            配置 Pod/SVC IP CIDR - 管控集群 - 冲突检测- Service 和 Pod 的 IP CIDR 间有重叠，（Blur+Onchange）inline 提示错误：IP 地址重复。
            配置 Pod/SVC IP CIDR - 管控集群 - 冲突检测- Service IP CIDR 与节点 IP pool 有重叠，部署管控集群步骤失败
            配置 Pod/SVC IP CIDR - 管控集群 - 冲突检测- Pod IP CIDR 与节点 IP pool 有重叠，部署管控集群步骤失败
            配置 Pod/SVC IP CIDR - 管控集群 - 冲突检测- Service IP CIDR 与手动配置的集群 VIP 有重叠，部署失败 - TBD
            配置 Pod/SVC IP CIDR - 管控集群 - 冲突检测- Pod IP CIDR 与手动配置的集群 VIP 有重叠，部署失败 - TBD
        工作集群
            配置 Pod/SVC IP CIDR - 工作集群 - 创建虚拟机工作集群时，Service IP CIDR 默认值显示为 10.250.252.0/22
            配置 Pod/SVC IP CIDR - 工作集群 - 创建虚拟机工作集群时，Pod IP CIDR 默认值显示为 172.31.224.0/20
            配置 Pod/SVC IP CIDR - 工作集群 - 创建物理机工作集群时，Service IP CIDR 默认值显示为 10.250.252.0/22
            配置 Pod/SVC IP CIDR - 工作集群 - 创建物理机工作集群时，Pod IP CIDR 默认值显示为 172.31.224.0/20
            配置 Pod/SVC IP CIDR - 工作集群 - 使用默认值成功创建工作负载集群，默认值生效
            配置 Pod/SVC IP CIDR - 工作集群 - 修改工作负载集群 Service 和 Pod IP CIDR 默认配置，修改后配置生效
            配置 Pod/SVC IP CIDR - 工作集群 - 长度校验 - Service IP CIDR 掩码长度设置为大于 26，（Blur+Onchange）inline 提示错误：子网掩码长度仅支持 8–26 的整数。
            配置 Pod/SVC IP CIDR - 工作集群 - 长度校验 - Service IP CIDR 掩码长度设置为小于 8，（Blur+Onchange）inline 提示错误：子网掩码长度仅支持 8–26 的整数。
            配置 Pod/SVC IP CIDR - 工作集群 - 长度校验 - Service IP CIDR 掩码长度设置为 8-26 间的任意自然数，无报错，可配置
            配置 Pod/SVC IP CIDR - Calico 工作集群 - Pod IP CIDR 输入框下增加提示：请确保子网足够大，以确保至少可为每个节点分配 /26 的地址块。创建后不可更改。
            配置 Pod/SVC IP CIDR - Calico 工作集群 - 长度校验 - 1+1 集群 Pod IP CIDR 掩码长度设置为 25 及以上自然数，（Blur+Onchange）inline 提示错误：子网掩码长度仅支持 8–24 的整数。
            配置 Pod/SVC IP CIDR - Calico 工作集群 - 长度校验 - 3+3 集群 Pod IP CIDR 掩码长度设置为 24 及以上自然数，（Blur+Onchange）inline 提示错误：子网掩码长度仅支持 8–23 的整数。
            配置 Pod/SVC IP CIDR - Calico 工作集群 - 长度校验 - 3+3~10 节点自动伸缩集群 Pod IP CIDR 掩码长度设置为 23 及以上自然数，（Blur+Onchange）inline 提示错误：子网掩码长度仅支持 8–22 的整数。
            配置 Pod/SVC IP CIDR - Calico 工作集群 - 长度校验 - 3+128 集群 Pod IP CIDR 掩码长度设置为 19 及以上自然数，（Blur+Onchange）inline 提示错误：子网掩码长度仅支持 8–18 的整数。
            配置 Pod/SVC IP CIDR - Calico 工作集群 - 长度校验 - Pod IP CIDR 掩码长度设置为小于 8，（Blur+Onchange）inline 提示错误：子网掩码长度仅支持 8–%26-log2(集群当前配置可达到的最大节点数)%的整数。
            配置 Pod/SVC IP CIDR - Calico 工作集群 - 长度校验 - 1+1 集群 Pod IP CIDR 掩码长度设置为 8-24 间的任意自然数，无报错，可配置
            配置 Pod/SVC IP CIDR - Calico 工作集群 - 长度校验 - 3+3 集群 Pod IP CIDR 掩码长度设置为 8-23 间的任意自然数，无报错，可配置
            配置 Pod/SVC IP CIDR - Calico 工作集群 - 长度校验 - 3+3~10 节点自动伸缩集群 Pod IP CIDR 掩码长度设置为 8-22 间的任意自然数，无报错，可配置
            配置 Pod/SVC IP CIDR - 工作集群 - 前缀长度校验 - EUC CNI Pod IP CIDR 不限制前缀长度
            配置 Pod/SVC IP CIDR - 工作集群 - 前缀长度校验 - Pod 网卡的 IP CIDR 不限制前缀长度
            配置 Pod/SVC IP CIDR - 工作集群 - 冲突检测- Service 和 Pod 的 IP CIDR 间有重叠，（Blur+Onchange）inline 提示错误：IP 地址重复。
            配置 Pod/SVC IP CIDR - 工作集群 - 冲突检测- Service IP CIDR 与 手动指定的 control plane VIP 有重叠，可提交 - TBD 没有拦截，创建时没出冲突能创建成功，用起来可能会有问题
            配置 Pod/SVC IP CIDR - 工作集群 - 冲突检测- Service IP CIDR 与 control plane VIP pool 有重叠，提交报错，后端拦截
            配置 Pod/SVC IP CIDR - 工作集群 - 冲突检测- Service IP CIDR 与 管理网卡 IP pool 有重叠，提交报错，后端拦截
            配置 Pod/SVC IP CIDR - 虚拟机工作集群 - 冲突检测- Service IP CIDR 与 任意业务网卡 IP pool 有重叠，提交报错，后端拦截
            配置 Pod/SVC IP CIDR - Calico 工作集群 - 冲突检测- Pod IP CIDR 与 control plane VIP 有重叠，可提交 - TBD 冲突之后集群会有问题
            配置 Pod/SVC IP CIDR - Calico 工作集群 - 冲突检测- Pod IP CIDR 与 control plane VIP pool 有重叠，提交报错，后端拦截
            配置 Pod/SVC IP CIDR - Calico 工作集群 - 冲突检测- Pod IP CIDR 与 管理网卡 IP pool 有重叠，提交报错，后端拦截
            配置 Pod/SVC IP CIDR - Calico 虚拟机工作集群 - 冲突检测- Pod IP CIDR 与 任意业务网卡 IP pool 有重叠，提交报错，后端拦截
            配置 Pod/SVC IP CIDR - ZBS CSI 工作集群 - 冲突检测- service IP CIDR 与 ZBS CSI 网卡的 IP pool 有重叠，提交报错，后端拦截
            配置 Pod/SVC IP CIDR - ZBS CSI 工作集群 - 冲突检测- Pod IP CIDR 与 ZBS CSI 网卡的 IP pool 有重叠，提交报错，后端拦截
            配置 Pod/SVC IP CIDR - EIC 虚拟机工作集群 - 冲突检测- EIC 网卡 IP CIDR 与手动设置的 control plane VIP 有重叠，提交报错，后端拦截
            配置 Pod/SVC IP CIDR - EIC 虚拟机工作集群 - 冲突检测- EIC 网卡 IP CIDR 与 control plane VIP pool 有重叠，提交报错，后端拦截
            配置 Pod/SVC IP CIDR - EIC 虚拟机工作集群 - 冲突检测- EIC 网卡 IP CIDR 与 管理网卡 IP pool 有重叠，提交报错，后端拦截
            配置 Pod/SVC IP CIDR - EIC 虚拟机工作集群 - 冲突检测- EIC 网卡 IP CIDR 与 任意业务网卡 IP pool 有重叠，提交报错，后端拦截
            配置 Pod/SVC IP CIDR - 工作负载集群创建 - 同时自定义 Service IP CIDR 和 Pod IP CIDR 可成功创建工作负载集群，自定义配置生效
            配置 Pod/SVC IP CIDR - 边界值 - 使用最小 pod CIDR 范围 (/24)创建 1+1 虚拟机工作负载集群可正常分配 IP
            配置 Pod/SVC IP CIDR - 边界值 - 使用最大 CIDR 范围 (/8) 创建 3+1 虚拟机工作负载集群可正常分配 IP
            配置 Pod/SVC IP CIDR - 边界值 - calico 工作集群配置262145个节点，报错「集群节点数过大，无法配置有效的 Pod 子网。」，减少一个节点，可配置掩码8
            配置 Pod/SVC IP CIDR - 边界值 - calico 工作集群配置131073个节点，报错「子网掩码长度必须为 8。」，减少一个节点，可配置掩码8或9
            配置 Pod/SVC IP CIDR - 升级兼容 - 旧版本升级到 1.6.0 后已有集群 IP 段不受影响
    Deprecated
        [Deprecated] CP证书管理 - 异常 - 证书验证步骤只打印不会失败
        [Deprecated] 管控集群 K8s 升级 - SKS 升级前置检查 - UI- 上传安装包的 metadata JSON 文件，点击「升级前检查按钮」，升级按钮进入短暂进入 loading 状态，不可重复点击，文件选择器控件禁用 - （设计移除了这个状态）
        # todo
        配置 Pod/SVC IP CIDR - EIC 虚拟机工作集群 - 长度校验 - EIC 网卡 IP CIDR 掩码长度设置为 8-26 间的任意自然数，无报错，可配置
SKS 1.5.1
    支持按节点组配置标签、注解、污点
        节点组配置 - 其他功能影响 - 虚拟机集群节点列表中移除编辑标签、编辑注解、编辑污点的入口
        节点组配置 - 其他功能影响 - 物理机集群节点列表中移除编辑标签、编辑注解、编辑污点的入口
        节点组配置 - 其他功能影响 - 虚拟机节点详情中移除编辑标签、编辑注解、编辑污点的入口
        节点组配置 - 其他功能影响 - 物理机节点详情中移除编辑标签、编辑注解、编辑污点的入口
        节点组配置 - 虚拟机集群 - CP 节点组 - 不提供编辑标签、注解、污点入口
        节点组配置 - 虚拟机集群 - worker 节点组 - more button 弹出 action 菜单有编辑节点组标签、注解、污点的入口
        节点组配置 - 物理机集群 - CP 节点组 - 不提供编辑标签、注解、污点入口
        节点组配置 - 物理机集群 - worker 节点组 - more button 弹出 action 菜单有编辑节点组标签、注解、污点的入口
        Label
            节点组配置 - label - 可为虚拟机 worker 节点组成功添加标签
            节点组配置 - label - 可为物理机 worker 节点组成功添加标签
            节点组配置 - label - 初次编辑节点组标签，显示为空白页，仅显示「+添加标签」按钮及格式要求，系统及组件自动添加及管理的标签不在此展示
            节点组配置 - label - 「查看格式要求」可展开标签格式要求
            节点组配置 - label - 添加标签，key 置空，提交不成功，inline 报错「请填写键。」
            节点组配置 - label - 添加标签，key/value 填入不满足格式要求的不合法值，提交不成功，inline 报错「格式错误。」
            节点组配置 - label - 添加标签，配置同样 key，不同 value 的标签，提交后仅最后一组 key-value 生效
            节点组配置 - label - 添加与非用户自定义标签 key 相同 value 不同的标签，可提交，部分受其他controller 管理的会在 reconcile 周期后被反复修改，再次编辑，显示该标签
            节点组配置 - label - 添加空值标签，保存，标签被应用到该节点组所有 node CR，查看 node label 和节点详情页标签，原有系统和组件自动添加及管理的标签不变，包含新添加的标签
            节点组配置 - label - 添加1个合法标签，保存，标签被应用到该节点组所有 node CR，查看 node label 和节点详情页标签，原有系统和组件自动添加及管理的标签不变，包含新添加的标签
            节点组配置 - label - 添加多个合法标签，保存，标签被应用到该节点组所有 node CR，查看 node label 和节点详情页标签，原有系统和组件自动添加及管理的标签不变，包含新添加的标签
            节点组配置 - label - 对2个不同的 worker 节点组分别添加不同的标签，保存，标签被应用到各自节点组内的所有 node
            节点组配置 - label - 编辑用户自定义标签的key，保存，修改被应用到该节点组所有 node CR，查看 node label 和节点详情页标签，修改生效
            节点组配置 - label - 编辑用户自定义标签的value，保存，修改被应用到该节点组所有 node CR，查看 node label 和节点详情页标签，修改生效
            节点组配置 - label - 同时改变用户自定义标签的key 和 value，保存，修改被应用到该节点组所有 node CR，查看 node label 和节点详情页标签，修改生效，原标签被替换
            节点组配置 - label - 删除部分用户自定义标签，保存，删除被应用到该节点组所有 node CR，查看 node label 和节点详情页标签，删除生效
            节点组配置 - label - 删除所有用户自定义标签，保存，删除被应用到该节点组所有 node CR，查看 node label 和节点详情页标签，删除生效，仅剩余原有系统和组件自动添加及管理的标签
            节点组配置 - label - 删除了节点组的所有用户自定义标签后，编辑页重新回到空白状态
            节点组配置 - label - 配置了用户自定义标签的节点组扩容节点，新节点配置了自定义标签
            节点组配置 - label - 多个节点组，其中一个配置了自定义标签，未配置用户自定义标签的节点组扩容节点，新节点不带有自定义标签
            节点组配置 - label - 配置了用户自定义标签的节点组替换节点，新节点配置了自定义标签
            节点组配置 - label - 配置了用户自定义标签的节点组发生自动伸缩，新节点配置了自定义标签
            节点组配置 - label - 升级集群 K8s 版本，滚动更新后，配置了用户自定义标签的节点组的节点配置了自定义标签
        Annotation
            节点组配置 - annotation - 可为虚拟机 worker 节点组成功添加注解
            节点组配置 - annotation - 可为物理机 worker 节点组成功添加注解
            节点组配置 - annotation - 初次编辑节点组注解，显示为空白页，仅显示「+添加注解」按钮及格式要求，系统及组件自动添加及管理的注解不在此展示
            节点组配置 - annotation - 「查看格式要求」可展开注解格式要求
            节点组配置 - annotation - 添加注解，key 置空，提交不成功，inline 报错「请填写键。」
            节点组配置 - annotation - 添加注解，key 填入不满足格式要求的不合法值，提交不成功，inline 报错「格式错误。」
            节点组配置 - annotation - 添加注解，配置同样 key，不同 value 的注解，提交后仅最后一组 key-value 生效
            节点组配置 - annotation - 添加与非用户自定义注解 key 相同 value 不同的注解，可提交，部分会立即被修正，部分 reconcile 周期后被修正，再此编辑，显示该注解
            节点组配置 - annotation - 添加空值注解，保存，注解被应用到该节点组所有 node CR，查看 node annotation 和节点详情页注解，原有系统和组件自动添加及管理的注解不变，包含新添加的注解
            节点组配置 - annotation - 添加1个合法注解，保存，注解被应用到该节点组所有 node CR，查看 node annotation 和节点详情页注解，原有系统和组件自动添加及管理的注解不变，包含新添加的注解
            节点组配置 - annotation - 添加多个合法注解，保存，注解被应用到该节点组所有 node CR，查看 node annotation 和节点详情页注解，原有系统和组件自动添加及管理的注解不变，包含新添加的注解
            节点组配置 - annotation - 对2个不同的 worker 节点组分别添加不同的注解，保存，注解被应用到各自节点组内的所有 node
            节点组配置 - annotation - 编辑用户自定义注解的key，保存，修改被应用到该节点组所有 node CR，查看 node annotation 和节点详情页注解，修改生效
            节点组配置 - annotation - 编辑用户自定义注解的value，保存，修改被应用到该节点组所有 node CR，查看 node annotation 和节点详情页注解，修改生效
            节点组配置 - annotation - 同时改变用户自定义注解的key 和 value，保存，修改被应用到该节点组所有 node CR，查看 node annotation 和节点详情页注解，修改生效，原注解被替换
            节点组配置 - annotation - 删除部分用户自定义注解，保存，删除被应用到该节点组所有 node CR，查看 node annotation 和节点详情页注解，删除生效
            节点组配置 - annotation - 删除所有用户自定义注解，保存，删除被应用到该节点组所有 node CR，查看 node annotation 和节点详情页注解，删除生效，剩余原有系统和组件自动添加及管理的注解
            节点组配置 - annotation - 删除了节点组的所有用户自定义注解后，编辑页重新回到空白状态
            节点组配置 - annotation - 配置了用户自定义注解的节点组扩容节点，新节点配置了自定义注解
            节点组配置 - annotation - 多个节点组，其中一个配置了自定义注解，未配置用户自定义注解的节点组扩容节点，新节点不带有自定义注解
            节点组配置 - annotation - 配置了用户自定义注解的节点组替换节点，新节点配置了自定义注解
            节点组配置 - annotation - 配置了用户自定义注解的节点组发生自动伸缩，新节点配置了自定义注解
            节点组配置 - annotation - 升级集群 K8s 版本，滚动更新后，配置了用户自定义注解的节点组的节点配置了自定义注解
        Taint
            节点组配置 - taint - 可为虚拟机 worker 节点组成功添加污点
            节点组配置 - taint - 可为物理机 worker 节点组成功添加污点
            节点组配置 - taint - 初次编辑节点组污点，显示为空白页，仅显示「+添加污点」按钮及格式要求系统和组件自动添加及管理的污点不在此展示
            节点组配置 - taint - 「查看格式要求」可展开污点格式要求
            节点组配置 - taint - 添加污点，key 置空，提交不成功，inline 报错「请填写键。」
            节点组配置 - taint - 添加污点，effect 默认值为「仅阻止调度」
            节点组配置 - taint - 添加污点，key/value 填入不满足格式要求的不合法值，提交不成功，inline 报错「格式错误。」
            节点组配置 - taint - 添加两个 key+effect 相同的污点，提交失败，返回后端 duplicate 报错
            节点组配置 - taint - 添加 node.kubernetes.io/disk-pressure、memory-pressure 等系统污点，可提交，迅速被kubelet更新覆盖
            节点组配置 - taint - 添加空值污点，保存，污点被应用到该节点组所有 node CR，查看 node taint 和节点详情页污点，原有系统和组件自动添加及管理的污点不变，包含新添加的污点
            节点组配置 - taint - 添加1个合法污点，保存，污点被应用到该节点组所有 node CR，查看 node taint 和节点详情页污点，原有系统和组件自动添加及管理的污点不变，包含新添加的污点
            节点组配置 - taint - 添加多个合法污点，保存，污点被应用到该节点组所有 node CR，查看 node taint 和节点详情页污点，原有系统和组件自动添加及管理的污点不变，包含新添加的污点
            节点组配置 - taint - 对2个不同的 worker 节点组分别添加不同的污点，保存，污点被应用到各自节点组内的所有 node
            节点组配置 - taint - 添加一个用户自定义污点，和系统自有污点的 key 相同，effect 不同，提交后创建新的污点
            节点组配置 - taint - 编辑用户自定义污点的key，保存，修改被应用到该节点组所有 node CR，查看 node taint 和节点详情页污点，修改生效
            节点组配置 - taint - 编辑用户自定义污点的value，保存，修改被应用到该节点组所有 node CR，查看 node taint 和节点详情页污点，修改生效
            节点组配置 - taint - 编辑用户自定义污点的effect，保存，修改被应用到该节点组所有 node CR，查看 node taint 和节点详情页污点，修改生效
            节点组配置 - taint - 同时改变用户自定义污点的key 和 value，保存，修改被应用到该节点组所有 node CR，查看 node taint 和节点详情页污点，修改生效，原污点被替换
            节点组配置 - taint - 删除部分用户自定义污点，保存，删除被应用到该节点组所有 node CR，查看 node taint 和节点详情页污点，删除生效
            节点组配置 - taint - 删除所有用户自定义污点，保存，删除被应用到该节点组所有 node CR，查看 node taint 和节点详情页污点，删除生效，仅剩余原有系统和组件自动添加及管理的污点
            节点组配置 - taint - 删除了节点组的所有用户自定义污点后，编辑页重新回到空白状态
            节点组配置 - taint - 配置了用户自定义污点的节点组扩容节点，新节点配置了自定义污点
            节点组配置 - taint - 多个节点组，其中一个配置了自定义污点，未配置用户自定义污点的节点组扩容节点，新节点不带有自定义污点
            节点组配置 - taint - 配置了用户自定义污点的节点组替换节点，新节点配置了自定义污点
            节点组配置 - taint - 配置了用户自定义污点的节点组发生自动伸缩，新节点配置了自定义污点
            节点组配置 - taint - 升级集群 K8s 版本，滚动更新后，配置了用户自定义污点的节点组的节点配置了自定义污点
        其他综合检查
            节点组配置 - 配置了自定一标签、注解、污点的节点组扩容节点，新节点带有全部自定义配置
            节点组配置 - 删除配置了自定一标签、注解、污点的节点组，节点组可被正常删除
            节点组配置 - 多个节点组配置各自不同的标签、注解、污点，升级集群 K8s 版本，滚动更新后，仍各自应用不同的自定义配置
            节点组配置 - 多个节点组配置各自不同的标签、注解、污点，升级集群 K8s 版本，添加新的节点组，新节点无任何自定义配置
        CR
            节点组配置 - KSC - ksc 中的 spec.topology 中的对每个节点组以 nodeAttributes.labels 记录对应的用户自定义标签信息
            节点组配置 - KSC - ksc 中的 spec.topology 中的对每个节点组以 nodeAttributes.annotations 记录对应的用户自定义注解信息
            节点组配置 - KSC - ksc 中的 spec.topology 中的对每个节点组以 nodeAttributes.taints 记录用户手动添加的污点信息
            节点组配置 - KSC - 集群的节点组未配置任何用户自定义标签/注解/污点时，ksc 中的 spec.topology 中对应节点组 nodeAttributes 信息为空
            节点组配置 - KSC - 集群的节点组删除了所有用户自定义标签/注解/污点时，ksc 中的 spec.topology 中对应节点组 nodeAttributes 信息为空
            节点组配置 - KSC - 从1.4升级到1.5后，ytt版本未提升的 ksc 中的 spec.topology 中对应节点组 nodeAttributes 信息为空
            节点组配置 - KSC - 后端编辑 ksc，为特定 worker 节点组配置 nodeAttributes 信息，配置可生效，UI 编辑时可正确读取
            节点组配置 - KSC - 后端编辑 ksc，为 CP 节点组配置 nodeAttributes 信息，配置可生效，所有 CP 节点配置更新，节点详情页可正确读取
            节点组配置 - KSC - 后端编辑 ksc，移除 CP 节点组配置的 nodeAttributes 信息，配置可生效，所有 CP 节点配置更新
            节点组配置 - node - 配置过节点组的标签/注解/污点后，节点增加3个annotation，记录应用的用户配置元数据
            EC
                节点组配置 - KSC - 编辑 ksc，为特定节点组配置不满足 K8s 格式要求的 label key，保存报错 SKS_NODE_LABEL_KEY_INVALID：Invalid node label key { labelKey }: { reason }
                节点组配置 - KSC - 编辑 ksc，为特定节点组配置不满足 K8s 格式要求的 label value，保存报错 SKS_NODE_LABEL_VALUE_INVALID：Invalid node label value { labelValue }: { reason }
                节点组配置 - KSC - 编辑 ksc，为特定节点组配置不满足 K8s 格式要求的 annotation key，保存报错 SKS_NODE_ANNOTATION_KEY_INVALID：Invalid node annotation key { annotationKey }: { reason }
                节点组配置 - KSC - 编辑 ksc，为特定节点组配置不满足 K8s 格式要求的 taint，保存报错 SKS_NODE_TAINT_INVALID：Invalid node taint { taint }: { reason }
    节点组配置修改不更新网络配置
        编辑节点组 - 对于手动配置不同节点组网络的集群，依次编辑 worker 节点组，热扩容集群资源规格，节点组网络配置不受影响
        编辑节点组 - 对于手动配置不同节点组网络的集群，依次编辑 worker 节点组，冷扩容集群资源规格，节点组网络配置不受影响
        编辑节点组 - 对于手动配置不同节点组网络的集群，依次编辑 worker 节点组，扩容节点组，节点组网络配置不受影响
        编辑节点组 - 对于手动配置不同节点组网络的集群，依次编辑 worker 节点组，缩容节点组，节点组网络配置不受影响
        编辑节点组 - 对于手动配置不同节点组网络的集群，依次编辑 worker 节点组，开启/关闭节点组自动伸缩，节点组网络配置不受影响
        编辑节点组 - 对于手动配置不同节点组网络的集群，依次编辑 worker 节点组，开启/关闭节点组故障自动替换，节点组网络配置不受影响
        编辑节点组 - 对于手动配置不同节点组网络的集群，编辑 cp 节点组，扩容 CP 节点组，节点组网络配置不受影响
        编辑节点组 - 对于手动配置不同节点组网络的集群，编辑 cp 节点组，开启/关闭故障节点自动替换，节点组网络配置不受影响
        编辑节点组 - 对于手动配置不同节点组网络的集群，创建新的 worker 节点组，节点组使用与 第1个worker节点组相同的网络配置
        编辑节点组 - 对于手动配置不同节点组网络的集群，删除其中一个网络配置不同的 worker 节点组，节点组可正常删除，再创建新节点组，节点组使用与 CP 节点组相同的网络配置
        相关区域回归
            编辑节点组 - 编辑网络配置统一的单网卡虚拟机节点组，可正常增减节点
            编辑节点组 - 编辑网络配置统一的单网卡虚拟机集群，可正常增减节点组
            编辑节点组 - 编辑网络配置统一的多网卡（带 ZBS CSI 网卡）虚拟机节点组，可正常扩容节点
            编辑节点组 - 编辑网络配置统一的多网卡（带 ZBS CSI 网卡）虚拟机集群，可正常增减节点组
            编辑节点组 - 编辑网络配置统一的多网卡（带 EIC CNI 网卡）虚拟机节点组，可正常增减节点
            编辑节点组 - 编辑网络配置统一的多网卡（带 EIC CNI 网卡）虚拟机集群，可正常增减节点组
            编辑节点组 - 编辑物理机节点组，可正常增减节点
    【SKS-4168】http 受信任容器镜像仓库扩容后配置错误不生效
        受信任容器镜像仓库配置 - 创建集群时添加 http 容器镜像仓库为受信任仓库，创建完成后，现有节点 containerd 配置正确，可从该仓库拉取镜像
        受信任容器镜像仓库配置 - 编辑集群添加 http 容器镜像仓库为受信任仓库，集群更新完成后，现有节点 containerd 配置正确，可从该仓库拉取镜像
        受信任容器镜像仓库配置 - 已配置 http 容器镜像仓库为受信任仓库，添加新节点组，新加入的节点 containerd 配置正确，可从该仓库拉取镜像
        受信任容器镜像仓库配置 - 已配置 http 容器镜像仓库为受信任仓库，扩容节点组，新加入的节点 containerd 配置正确，可从该仓库拉取镜像
        受信任容器镜像仓库配置 - 编辑集群添加 https 容器镜像仓库为受信任仓库，集群更新完成后，现有节点 containerd 配置正确，可从该仓库拉取镜像
        受信任容器镜像仓库配置 - 已配置 https 容器镜像仓库为受信任仓库，添加新节点，新加入的节点containerd 配置正确，可从该仓库拉取镜像
    【SKS-4209】EIC CNI 新建 pod 未在 vrf 中宣告 arp
        升级1.5.1-eic组件版本更新-从1.2.3更新至1.2.4
        升级1.5.1-升级后，eic工作集群，pod可正常通信，集群组件工作正常
        升级1.5.1-升级前，eic集群创建deployment设置分配静态ip，升级后外部可与pod正常通信
        升级1.5.1-升级前，eic集群创建deployment设置分配静态ip，升级后删除pod重建，外部可与pod正常通信
        升级1.5.1-升级前，eic集群设置小范围ippool，升级后组件pod重建可成功，通信正常
        升级1.5.1-升级前，eic集群设置小范围ippool，升级后重复开关插件，可正常创建pod，通信正常
        升级1.5.1-升级后，eic工作集群，升级k8s版本，可升级成功，集群组件正常工作
        升级1.5.1-升级后，eic工作集群，执行pod-e2e测试
        升级1.5.1-升级后，EIC 自动化case执行
    patch 版本更新测试
        自动化验证 - SKS Smoke Test
        自动化验证 - LCM FVT
        升级 minor 版本
            patch版本更新 - 1.4.0 版本升级 1.5.1 版本 - 升级成功，服务版本为 1.5.1
            patch版本更新 - 1.4.0 版本升级 1.5.1 版本 - 工作负载集群状态正常，可正常添加节点
            patch版本更新 - 1.4.0 版本升级 1.5.1 版本 - 工作负载集群状态正常，可成功提升 ytt 版本
            patch版本更新 - 1.4.0 版本升级 1.5.1 版本 - Tower file-server 拉取物料到 v1.5.1 目录
            patch版本更新 - 1.4.0 版本升级 1.5.1 版本 - 管控集群 file-server 拉取物料到 v1.5.1 目录
        升级 patch 版本
            patch版本更新 - 1.5.0 版本升级 1.5.1 版本 - 升级成功，服务版本为 1.5.1
            patch版本更新 - 1.5.0 版本升级 1.5.1 版本 - 工作负载集群状态正常，可正常添加节点
            patch版本更新 - 1.5.0 版本升级 1.5.1 版本 - 工作负载集群状态正常，可成功提升 ytt 版本
            patch版本更新 - 1.5.0 版本升级 1.5.1 版本 - 工作负载集群状态正常，可正常升级 K8s 版本
            patch版本更新 - 1.5.0 版本升级 1.5.1 版本 - Tower file-server 拉取物料到 v1.5.1 目录
            patch版本更新 - 1.5.0 版本升级 1.5.1 版本 - 管控集群 file-server 拉取物料到 v1.5.1 目录
        新部署
            patch版本更新 - 部署 1.5.1 版本 - 部署成功，服务版本为 1.5.1
            patch版本更新 - 部署 1.5.1 版本 - 部署成功，模板版本为 1.5.0
            patch版本更新 - 在 1.5.1 中上传 1.5.0 模板 - 可上传，版本展示为 1.5.0
            patch版本更新 - 在 1.5.1 中使用 1.5.0 模板 - 可新建集群，ytt 版本为 1.5.1
            patch版本更新 - 在 1.5.1 中上传 1.5.0 GPU 镜像文件 - 可上传
            patch版本更新 - 部署 1.5.1 版本 - Tower file-server 拉取物料到 v1.5.1 目录
            patch版本更新 - 部署 1.5.1 版本 - 管控集群 file-server 拉取物料到 v1.5.1 目录