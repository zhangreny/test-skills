CSI 3.0
    默认副本数
        ISCSI
            创建sc 不设置副本数 使用zbs双活集群作为存储 使用sc创建pvc 自动生成的pv为3副本
            创建sc 不设置副本数 使用zbs单活集群作为存储 使用sc创建pvc 自动生成的pv为2副本（是否有target target副本数来决定pv副本数---case只检查创建出来的是副本pv就行）
            创建sc 设置副本数为3副本 使用zbs单活集群作为存储 创建pvc 自动生成的pv为3副本
            sc 不设置副本数 使用zbs双活集群作为存储 克隆 检查克隆的pv为3副本
            sc 不设置副本数 使用zbs单活集群作为存储 克隆 克隆的pv为2副本
            sc 不设置副本数 使用zbs双活集群作为存储 创建快照并恢复 检查恢复的pv为3副本
            sc 不设置副本数 使用zbs单活集群作为存储 创建快照并恢复 恢复的pv为2副本
    支持卷加密
        ISCSI
            创建sc加密字段设置为空“” - 创建pvc使用sc 自动生成pv不加密
            创建sc加密字段设置为空None - 创建pvc使用sc 自动生成pv不加密
            创建sc加密字段设置为非加密算法 - 创建pvc 使用sc 自动生成pv报错
            创建sc 不使用加密字段 - 创建pvc使用sc 自动生成pv不加密
            创建sc 加密字段设置为符合条件的加密算法 - 配置成功
            创建sc指定加密算法 创建block类型pvc 使用sc 检查block类型pv 加密存储
            创建sc指定加密算法 创建filesystem类型pvc 使用sc 检查filesystem类型pv 加密存储
            克隆使用加密sc的pvc 检查克隆出来的pv 加密
            克隆使用不加密sc的pvc 检查克隆出来的pv 不加密
            克隆前重建sc从加密改为不加密 克隆加密pvc 检查克隆pv报错
            对使用加密sc的pvc进行扩容 pod绑定对应pv pv扩容成功
            使用加密sc的pvc创建快照 创建成功
            使用快照恢复pv 检查pv加密
            使用快照恢复pv前重建sc为不加密 检查恢复的pv报错
            删除使用加密sc创建的pvc 自动删除pv成功
            创建sc设置加密 同时设置qos 使用sc创建pvc 自动生成pv 检查pv加密同时qos生效 （全部参数都进行设置后检查pv正常）
            csi使用没有关联加密服务器的ZBS集群作为存储 创建加密sc 使用sc创建pvc 自动生成pv报错
            csi 使用不支持加密的zbs集群 使用加密sc 创建pv成功 为不加密
    开启常驻缓存后可指定精简置备
        ISCSI
            创建sc设置分层模式为None 精简制备 使用sc创建pvc 检查pv开启常驻缓存且为精简制备
            创建sc设置分层模式为None 厚制备 使用sc创建pvc 检查pv开启常驻缓存且为厚制备
            将开启常驻缓存精简制备 pvc 改为厚制备 检查pv开启常驻缓存且为厚制备
            pv开启常驻缓存 精简制备 编辑pvc设置为关闭常驻缓存 检查pv关闭常驻缓存且为精简制备
            pv开启常驻缓存 厚制备 编辑pvc设置为关闭常驻缓存 检查pv关闭常驻缓存且为厚制备
            pv关闭常驻缓存 精简制备 编辑pvc设置为开启常驻缓存 检查pv开启常驻缓存且为精简制备
            pv关闭常驻缓存 厚制备 编辑pvc设置为开启常驻缓存 检查pv开启常驻缓存且为厚制备
            创建sc设置为开启常驻缓存 精简制备 pvc设置为关闭常驻缓存 检查pv为关闭常驻缓存 精简制备
            创建sc设置为关闭常驻缓存 精简制备 pvc设置为开启常驻缓存 检查pv为开启常驻缓存 精简制备
            sc不进行分层模式设置 精简制备 创建pvc时设置为None 检查pv开启常驻缓存且为精简制备
            sc不进行分层模式设置 精简制备 创建pvc时设置为Auto 检查pv关闭常驻缓存且为精简制备
    平滑升级
        集群存在开启了nvmf的sc 升级检查不通过 升级失败
        集群存在开启了chap的sc 升级检查不通过 升级失败
        集群存在开启了topo的sc 升级检查不通过 升级失败
        集群存在开启了multiCluster的sc 升级检查不通过 升级失败
        集群存在开启了nvmf的pv 升级检查不通过 升级失败
        集群存在开启了chap的pv 升级检查不通过 升级失败
        集群存在开启了topo的pv 升级检查不通过 升级失败
        集群存在开启了multiCluster的pv 升级检查不通过 升级失败
        集群不存在开启了nvmf/chap/topo/multiCluster的sc和pv 升级检查通过 升级成功
        集群存在开启了nvmf/chap/topo/multiCluster的sc和pv 升级检查不通过 ；升级失败后 删除这些sc和pvc/pv 环境中不存在开启了nvmf/chap/topo/multiCluster的sc和pv 升级检查通过 升级成功
        升级前设置支持的所有参数创建sc pvc 自动生成pv  升级后检查sc参数更新为新的值 pv参数不变
        升级后使用升级前创建的sc 创建pvc 自动生成pv成功
        升级后检查升级前创建/克隆/恢复的pvc和pv可正常使用 进行扩容可生效
        升级后对升级前的pvc进行快照和恢复 任务成功 pv自动生成
        升级后使用升级前创建的快照进行恢复 pv创建成功
        升级后对升级前的pvc进行克隆 任务成功 pv创建成功
        升级后旧的pvc删除成功 pv根据策略删除或保留成功
        升级后检查绑定升级前pv的 pod 可进行迁移节点 检查iqn被清理 mount被清理
        升级后创建新的sc pvc 自动生成pv 绑定pod使用正常
        升级后对新建的 pvc 创建快照成功
        升级后使用新建快照进行恢复成功
        升级后使用新建的 pvc 进行克隆  pv创建成功
        在线升级：使用腾讯云
        在线升级：使用docker hub
        离线升级：使用私有镜像仓库
        升级后，当节点个数>=controller replica count(默认2），controller pod应该分布在不同节点
        升级到csi3.0，sidecar检查
    故障测试
        ZBS集群 chunk服务down「stop」
        ZBS集群 chunk服务down「kill」
        ZBS集群 接入网卡down「无bonding」
        ZBS集群 接入网卡down「有bonding」
        ZBS集群 主机关机
        ZBS集群 增加主机
        ZBS集群 减少主机
        ZBS集群 接入ip变更
        ZBS集群 所有接入点异常
        ZBS 存储网 down
        K8S集群 接入网卡ifdown/ifup
        K8S集群 主机关机 pod迁移
        K8S集群 csi pod down
        K8S集群  业务pod down
        隔离chunk/OP发生failslow
    安装卸载
        在线安装测试：腾讯云
        在线安装测试：dockerhub
        离线安装：私有镜像
        卸载
        新部署csi3.0，sidecar检查
        全新安装后，当节点个数>controller replica count(默认2），controller pod应该分布在不同节点
    【行为变化】自动配置open-iscsi
        部署后检查所有节点open-iscsi 状态为running
    【行为变化】手动 umount stage 目录导致新pod直接挂载到节点目录上
        新部署csi，业务 pod 挂载 pvc 后手动 umount stage 目录，相同节点新建业务 pod 会无法正常启动
    【行为变化】支持配置节点最大可挂载 PV 数
        部署csi 默认配置 单个节点挂载128个pv 可挂载成功
        离线部署csi默认配置 单个节点挂载129个pv 挂载失败
        离线部署csi修改配置 maxVolumes为256 单个节点挂载256个pv 可挂载成功
        离线部署csi修改配置 maxVolumes为256 单个节点挂载257个pv 挂载失败
        离线部署csi修改配置maxVolumes为10 集群单个节点挂载10个pv 修改配置maxVolumes为20 更新csi 集群每个节点挂载20个pv 挂载成功
        离线部署csi修改配置maxVolumes为10 集群单个节点挂载10个pv 修改配置maxVolumes为5 更新csi
    【行为变化】iscsi vip 切换
        ZBS集群更改vip 更新csi 更改ZBS_IP重启deployment的pod在相同节点  --- 检查连接点为原ZBS_IP不变 新pod重启成功
        ZBS集群更改vip 更新csi 更改ZBS_IP扩容deployment 新建pod在相同节点  --- 检查新建连接点为原ZBS_IP不变 新pod启动成功
        ZBS集群更改vip 更新csi 更改ZBS_IP新建deployment 新建pod在不同节点  --- 检查新建连接点为更改后ZBS_IP新pod启动成功
        ZBS集群更改vip 更新csi 更改ZBS_IP重启statefulset的pod 在相同节点--- 检查连接点变为新ZBS_IP pod重启成功
        ZBS集群更改vip 更新csi 更改ZBS_IP 扩容statefulset新建pod在相同节点--- 检查新建连接点为新ZBS_IP 新pod启动成功
Arcfra CSI 3.0
    Arcfra 适配改动测试
        在线部署helm命令中 Helm Chart名称从csi-driver-zbs-iscsi 更改为 csi-driver-abs-iscsi 部署成功
        使用腾讯云仓库部署csi 仓库名称ccr.ccs.tencentyun.com/smartxworks 更改为 ccr.ccs.tencentyun.com/arcfra 在线部署成功
        在线部署helm命令中镜像名称 csi-driver-zbs-iscsi 更改为 csi-driver-abs-iscsi 部署成功
        在线部署csi export  zbsIP 字段改为 absIP 部署成功
        使用公共镜像仓库部署csi 在线部署成功后 获取values.yaml文件检查 仓库名称 更改为 docker.io/arcfra
        在线部署csi成功后 检查values.yaml中  driverName 更改为  iscsi.abs.csi.arcfra.com
        检查创建的PVC annotation 中前缀更改为 iscsi.abs.csi.arcfra.com
        离线部署csi 安装包名称 csi-driver-zbs-iscsi-v3.0.0-airgap.tar.gz 更改为 csi-driver-abs-iscsi-v3.0.0-airgap.tar.gz 离线部署成功
        离线部署使用私有镜像仓库 仓库名称路径为arcfra 部署成功
        离线部署csi export zbsIP 字段改为 absIP 部署成功
        离线部署 export 驱动名称更改为 csi-driver-abs-iscsi 部署成功
        使用私有镜像仓库部署成功后 获取values.yaml文件检查仓库名称为arcfra路径
        离线部署csi成功后 检查values.yaml中  driverName 更改为  iscsi.abs.csi.arcfra.com
        检查创建的PVC annotation 中前缀更改为 iscsi.abs.csi.arcfra.com
    x86 基础功能回归
        安装部署卸载升级
            在线安装测试：腾讯云
            在线安装测试：dockerhub
            离线安装：私有镜像
            卸载
            新部署csi3.0，sidecar检查
            全新安装后，当节点个数>controller replica count(默认2），controller pod应该分布在不同节点
            在线升级：使用腾讯云
            在线升级：使用docker hub
            离线升级：使用私有镜像仓库
            升级后，当节点个数>=controller replica count(默认2），controller pod应该分布在不同节点
            升级到csi3.0，sidecar检查
            升级后创建新的sc pvc 自动生成pv 绑定pod使用正常
            升级前创建的绑定pod的pvc，升级后可正常使用
        默认副本数
            ISCSI
                创建sc 不设置副本数 使用zbs双活集群作为存储 使用sc创建pvc 自动生成的pv为3副本
                创建sc 不设置副本数 使用zbs单活集群作为存储 使用sc创建pvc 自动生成的pv为2副本
        支持卷加密
            ISCSI
                创建sc加密字段设置为空None - 创建pvc使用sc 自动生成pv不加密
                创建sc 加密字段设置为符合条件的加密算法 - 配置成功
                创建sc指定加密算法 创建block类型pvc 使用sc 检查block类型pv 加密存储
        开启常驻缓存后可指定精简置备
            ISCSI
                创建sc设置分层模式为None 精简制备 使用sc创建pvc 检查pv开启常驻缓存且为精简制备
                创建sc设置分层模式为None 厚制备 使用sc创建pvc 检查pv开启常驻缓存且为厚制备
                创建sc设置为关闭常驻缓存 精简制备 pvc设置为开启常驻缓存 检查pv为开启常驻缓存 精简制备
    arm基础功能回归
        安装部署卸载升级
            在线安装测试：腾讯云
            在线安装测试：dockerhub
            离线安装：私有镜像
            卸载
            新部署csi3.0，sidecar检查
            全新安装后，当节点个数>controller replica count(默认2），controller pod应该分布在不同节点
            在线升级：使用腾讯云
            在线升级：使用docker hub
            离线升级：使用私有镜像仓库
            升级后，当节点个数>=controller replica count(默认2），controller pod应该分布在不同节点
            升级到csi3.0，sidecar检查
            升级后创建新的sc pvc 自动生成pv 绑定pod使用正常
            升级前创建的绑定pod的pvc，升级后可正常使用