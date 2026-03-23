ZBS 块存储
    chunk自动剔除磁盘
ZBS 网络故障处理改进
    针对网卡的异常检测和隔离
        基本功能 -- 基于 bond 类型
            ovs ab bonding，支持隔离网卡
                ovs ab bond，nic1 故障被隔离后，nic2 也发生故障，之后恢复 nic1，nic2 保持故障，会先将 nic1 加回 bond，再检测到 nic2 故障并隔离 nic2 - https://cs.smartx.com/cases/detail?id=1069870
zbs 双活
    安装部署
        zbs-5.6.0 及之后部署默认开启 vhost
        zbs-5.6.0 及之后版本支持常驻缓存
    双活转换与仲裁节点重建
        非双活转双活
    UI 测试
        集群概览
            可用域之间网关
        机架
            添加/删除机架
            添加/删除 机箱
            机箱带节点迁移
            机箱不带节点迁移
            节点同机箱迁移
            节点同机架跨机箱迁移
            节点跨机架迁移
        告警
            可用域
                健康: 数据空间足够,完全可以支持恢复数据至 3 副本。
                集群数据空间超过授权限制（注意）
                不同可用域空间差大于集群总数据空间的 { .threshold }%
                如果其他可用域整体失效，则可用域： zone-master 数据空间不足以恢复当前全部数据至 2 副本
                如果其他可用域整体失效，则可用域： zone-master 数据空间不足以恢复当前全部数据至 1 副本
                如果其他可用域整体失效，则可用域： { .labels.name } 数据空间不足以恢复当前全部数据至 { .threshold } 副本
                机架 { .labels.rack } 的总数据空间大于当前集群总数据空间的 { .threshold }
                健康: 系统时间差均不超过 30 秒。
                主机 { .labels.hostname } 和集群系统时间相差大于 { .threshold }
                健康:所有主机均处于运 行中状态。
                严重警告:部分主机的工 作状态未知。
                健康: 所有主机的存储服务可用
                严重警告: 主机的存储服务异常
                健康:所有主节点 zbs-metad / zookeeper /mongod 服务正在运行中
                严重警告:主机的 zbs-metad / zookeeper /mongod 服务未运行
            仲裁节点
                健康: 仲裁节点处于运行 中状态
                严重警告:仲裁节点的工 作状态未知
                健康:系统时间差不超过 30 秒
                严重警告:仲裁节点 { .labels.hostname } 和集群系统时间相差大于 { .threshold }
                健康:仲裁节点的mongod / zbs-ntpd /zookeeper / ntpd /master-monitor 服务正在运行中。
                严重警告:仲裁节点的 mongod / zbs-ntpd / zookeeper / ntpd /master-monitor 服务未运行。
                健康:仲裁节点的 CPU 使用率未超过 80%,或者 CPU 使用率虽超过 80%,但其持续时间不超过 5 分钟。
                注意:仲裁节点的 CPU 使用率超过 80%,且持续时间超过 5 分钟
                严重警告:仲裁节点的 CPU 使用率超过 90%,且持续时间超过 5 分钟
                健康: 仲裁节点的系统分区空间使用率未超过 90%
                严重: 仲裁节点 { .labels.hostname } 的系统分区空间使用率已经超过 { .threshold }
            可用域之间网络
                健康:在 5 分钟内,仲裁节点到优先可用域及次级可用域的任一主机的最差往返延迟的平均值不超过10 毫秒。
                注意:仲裁节点到 { .labels.target_zone_name } 的最差往返延迟5分钟 P{ .quantile } 值超过 { .threshold }
                严重警告:仲裁节点到 { .labels.target_zone_name } 的最差往返延迟5分钟 P{ .quantile } 值超过 { .threshold }
                健康:仲裁节点与优先可用域之间,以及仲裁节点与次级可用域之间的存储网络连接正常
                严重警告:仲裁节点与优先可用域之间,或者仲裁节点与次级可用域之间的存储网络连接异常
            可用域之间节点
                “主机 { .labels.hostname } 和主机 { .labels.to_hostname } 之间的存储网络 ping 延迟 5 分钟内 P{ .quantile } 值超过 { .threshold}”告警不能跨可用域，只能检查可用域内节点之间的网络
        节点
            仲裁节点
                健康检查
                    仲裁节点的工作状态
                    仲裁节点的系统时间
                    仲裁节点的系统服务 mongod 的运行状态
                    仲裁节点的系统服务 zbs-ntpd 的运行状态
                    仲裁节点的系统服务 zookeeper 的运行状态
                    仲裁节点的系统服务 ntpd 的运行状态
                    仲裁节点的系统服务 master-monitor 的运行状态
                    仲裁节点的 CPU 使用率
                    仲裁节点的系统空间使用率
                基本信息
                    IP 地址（仅存储）
                    CPU 分配（核心数）
                    内存分配
                    系统总空间
                    系统已使用/空闲空间
                监控信息
                    两小时内，节点 CPU 使用率
                    两小时内，节点内存使用率
                    22 项服务状态
            存储节点
                具有跳跃功能，可以跳到对应的可用域
                健康检查
                    可用域总数据空间
                    可用域内主机的系统时间
                    可用域内的主机电源状态
                    可用域内主机工作状态
                    可用域内主机存储健康状态
                    可用域内主节点的系统服务 zbs-metad 运行状态
                    可用域内主节点的系统服务 zookeeper 运行状态
                    可用域内主节点的系统服务 mongod 运行状态
                基本信息
                    可用域内主机个数
                    点击数据中心，具有跳转功能
                    存储总空间
                    系统已使用空间
                    系统失效空间
                    系统空闲空间
    POC 验收测试
        自主研发
        机架感知功能验证
        支持部署双活集群，并可以监控双活架构状态
        测试 A或B 站点故障，即单可用域全部节点故障对集群及业务的影响
        测试仲裁节点故障对集群及业务的影响
        测试可用域之间存储网络中断故障对集群及业务的影响
        测试可用域与仲裁网络之间中断故障对集群及业务的影响
        节点运维
            UI 重启
            UI 关机
            优先可用域的 manage node 进入维护模式
            优先可用域的 storage node 进入维护模式
            次级可用域的 manage node 进入维护模式
            次级可用域的 storage node 进入维护模式
            优先可用域添加节点
            次级可用域添加节点
            分层部署添加节点
            不分层部署添加节点
            配置静态路由添加节点
            优先可用域移除 manage node
            优先可用域移除 storage node
            次级可用域移除 manage node
            次级可用域移除 storage node
            配置静态路由移除节点
            高水位移除节点
            master 转为 storage
            storage 转为 master
    基本功能
        快照
            快照删除
            快照回滚
            快照计划
        克隆
            创建克隆卷
            对克隆卷创建快照
            对克隆卷进行克隆
        磁盘管理
            磁盘管理 -  添加数据盘
            磁盘管理 -  移除数据盘
    可靠性测试
        磁盘故障
            系统盘故障
            数据盘故障
            缓存盘故障
    license
        双活集群添加非双活 license（预期有拦截）
安装部署&升级&运维
    部署
        rdma & nvmf
            部署时 enable storage rdma ( 要查流控 )
            部署时 enable nvme over tcp / rdma
        网络融合部署
            管理网和接入网融合
            存储网和接入网融合
            全部融合
    升级
        版本升级
            ZBS-5.2.0
                Vhost
                    升级到 zbs-5.6.0 及之后的版本后 enable vhost (zbs-cluster vhost enable)
            ZBS-5.3.0
                Vhost
                    升级到 zbs-5.6.0 及之后的版本后 enable vhost (zbs-cluster vhost enable)
            ZBS-5.4.1
                Vhost
                    升级到 zbs-5.6.0 及之后的版本后 enable vhost (zbs-cluster vhost enable)
            ZBS-5.5.0
                Vhost
                    升级到 zbs-5.6.0 及之后的版本后 enable vhost (zbs-cluster vhost enable)
            ZBS-5.6.1
                分层场景
                    升级前覆盖不同规格数据，iscsi/nvmf，thin/thick，是否pin in perf，snapshot
                    升级过程中进行io
                    空间使用率达到80%之后进行升级
                    disable/prepare/enable阶段：对老卷持续进行fio，快照，重建，回滚操作
                    disable/prepare/enable阶段：创建新卷进行fio，快照，删除，触发创建新格式元数据
                    disable/prepare/enable阶段：校验升级前与升级后卷的md5，进行一致性校验
                    disable/prepare阶段：创建pin in perf卷，写入cap层，perf暂无数据
                    enable阶段：创建pin in per卷，打快照，并重建，再删除，写入perf层
                    disable/prepare阶段：创建ec卷失败/sink失败
                    enable阶段：创建ec卷成功；sink成功
                    disable阶段：被动更新元数据，确认日志"UPGRADE FOR TIERING"
                    prepare阶段：主动更新元数据，确认日志"UPGRADE FOR TIERING"
                    disable/prepare/enable阶段：停chunk触发recover
                    disable/prepare/enable阶段：对老卷进行resize / update / reserve触发被动更新元数据
                    disable阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为false
                    prepare阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为true
                    enable阶段：zbs-meta cluster summary对应值为 True；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为true
                Vhost
                    升级到 zbs-5.6.0 及之后的版本后 enable vhost (zbs-cluster vhost enable)
                不分层场景
                    升级前覆盖不同规格数据，iscsi/nvmf，thin/thick，是否pin in perf，snapshot
                    升级过程中进行io
                    空间使用率达到80%之后进行升级
                    disable/prepare阶段：对老卷持续进行fio，快照，重建，回滚操作
                    disable/prepare阶段：创建新卷进行fio，快照，删除，触发创建新格式元数据
                    disable/prepare阶段：校验升级前与升级后卷的md5，进行一致性校验
                    disable/prepare阶段：创建ec卷失败/sink失败
                    disable阶段：被动更新元数据，确认日志"UPGRADE FOR TIERING"
                    prepare阶段：主动更新元数据，确认日志"UPGRADE FOR TIERING"
                    disable/prepare阶段：停chunk触发recover
                    disable/prepare阶段：对老卷进行resize / update / reserve触发被动更新元数据
                    disable阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为false
                    prepare阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为true
            ZBS-5.6.0
                分层场景
                    升级前覆盖不同规格数据，iscsi/nvmf，thin/thick，是否pin in perf，snapshot
                    升级过程中进行io
                    空间使用率达到80%之后进行升级
                    disable/prepare/enable阶段：对老卷持续进行fio，快照，重建，回滚操作
                    disable/prepare/enable阶段：创建新卷进行fio，快照，删除，触发创建新格式元数据
                    disable/prepare/enable阶段：校验升级前与升级后卷的md5，进行一致性校验
                    disable/prepare阶段：创建pin in perf卷，写入cap层，perf暂无数据
                    enable阶段：创建pin in per卷，打快照，并重建，再删除，写入perf层
                    disable/prepare阶段：创建ec卷失败/sink失败
                    enable阶段：创建ec卷成功；sink成功
                    disable阶段：被动更新元数据，确认日志"UPGRADE FOR TIERING"
                    prepare阶段：主动更新元数据，确认日志"UPGRADE FOR TIERING"
                    disable/prepare/enable阶段：停chunk触发recover
                    disable/prepare/enable阶段：对老卷进行resize / update / reserve触发被动更新元数据
                    disable阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为false
                    prepare阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为true
                    enable阶段：zbs-meta cluster summary对应值为 True；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为true
                不分层场景
                    升级前覆盖不同规格数据，iscsi/nvmf，thin/thick，是否pin in perf，snapshot
                    升级过程中进行io
                    空间使用率达到80%之后进行升级
                    disable/prepare阶段：对老卷持续进行fio，快照，重建，回滚操作
                    disable/prepare阶段：创建新卷进行fio，快照，删除，触发创建新格式元数据
                    disable/prepare阶段：校验升级前与升级后卷的md5，进行一致性校验
                    disable/prepare阶段：创建ec卷失败/sink失败
                    disable阶段：被动更新元数据，确认日志"UPGRADE FOR TIERING"
                    prepare阶段：主动更新元数据，确认日志"UPGRADE FOR TIERING"
                    disable/prepare阶段：停chunk触发recover
                    disable/prepare阶段：对老卷进行resize / update / reserve触发被动更新元数据
                    disable阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为false
                    prepare阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为true
                Vhost
                    升级到 zbs-5.6.0 及之后的版本后 enable vhost (zbs-cluster vhost enable)
            ZBS-5.6.2
                分层场景
                    升级前覆盖不同规格数据，iscsi/nvmf，thin/thick，是否pin in perf，snapshot
                    升级过程中进行io
                    空间使用率达到80%之后进行升级
                    disable/prepare/enable阶段：对老卷持续进行fio，快照，重建，回滚操作
                    disable/prepare/enable阶段：创建新卷进行fio，快照，删除，触发创建新格式元数据
                    disable/prepare/enable阶段：校验升级前与升级后卷的md5，进行一致性校验
                    disable/prepare阶段：创建pin in perf卷，写入cap层，perf暂无数据
                    enable阶段：创建pin in per卷，打快照，并重建，再删除，写入perf层
                    disable/prepare阶段：创建ec卷失败/sink失败
                    enable阶段：创建ec卷成功；sink成功
                    disable阶段：被动更新元数据，确认日志"UPGRADE FOR TIERING"
                    prepare阶段：主动更新元数据，确认日志"UPGRADE FOR TIERING"
                    disable/prepare/enable阶段：停chunk触发recover
                    disable/prepare/enable阶段：对老卷进行resize / update / reserve触发被动更新元数据
                    disable阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为false
                    prepare阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为true
                    enable阶段：zbs-meta cluster summary对应值为 True；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为true
                不分层场景
                    升级前覆盖不同规格数据，iscsi/nvmf，thin/thick，是否pin in perf，snapshot
                    升级过程中进行io
                    空间使用率达到80%之后进行升级
                    disable/prepare阶段：对老卷持续进行fio，快照，重建，回滚操作
                    disable/prepare阶段：创建新卷进行fio，快照，删除，触发创建新格式元数据
                    disable/prepare阶段：校验升级前与升级后卷的md5，进行一致性校验
                    disable/prepare阶段：创建ec卷失败/sink失败
                    disable阶段：被动更新元数据，确认日志"UPGRADE FOR TIERING"
                    prepare阶段：主动更新元数据，确认日志"UPGRADE FOR TIERING"
                    disable/prepare阶段：停chunk触发recover
                    disable/prepare阶段：对老卷进行resize / update / reserve触发被动更新元数据
                    disable阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为false
                    prepare阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为true
                Vhost
                    升级到 zbs-5.6.0 及之后的版本后 enable vhost (zbs-cluster vhost enable)
            ZBS-5.6.3
                分层场景
                    升级前覆盖不同规格数据，iscsi/nvmf，thin/thick，是否pin in perf，snapshot
                    升级过程中进行io
                    空间使用率达到80%之后进行升级
                    disable/prepare/enable阶段：对老卷持续进行fio，快照，重建，回滚操作
                    disable/prepare/enable阶段：创建新卷进行fio，快照，删除，触发创建新格式元数据
                    disable/prepare/enable阶段：校验升级前与升级后卷的md5，进行一致性校验
                    disable/prepare阶段：创建pin in perf卷，写入cap层，perf暂无数据
                    enable阶段：创建pin in per卷，打快照，并重建，再删除，写入perf层
                    disable/prepare阶段：创建ec卷失败/sink失败
                    enable阶段：创建ec卷成功；sink成功
                    disable阶段：被动更新元数据，确认日志"UPGRADE FOR TIERING"
                    prepare阶段：主动更新元数据，确认日志"UPGRADE FOR TIERING"
                    disable/prepare/enable阶段：停chunk触发recover
                    disable/prepare/enable阶段：对老卷进行resize / update / reserve触发被动更新元数据
                    disable阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为false
                    prepare阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为true
                    enable阶段：zbs-meta cluster summary对应值为 True；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为true
                不分层场景
                    升级前覆盖不同规格数据，iscsi/nvmf，thin/thick，是否pin in perf，snapshot
                    升级过程中进行io
                    空间使用率达到80%之后进行升级
                    disable/prepare阶段：对老卷持续进行fio，快照，重建，回滚操作
                    disable/prepare阶段：创建新卷进行fio，快照，删除，触发创建新格式元数据
                    disable/prepare阶段：校验升级前与升级后卷的md5，进行一致性校验
                    disable/prepare阶段：创建ec卷失败/sink失败
                    disable阶段：被动更新元数据，确认日志"UPGRADE FOR TIERING"
                    prepare阶段：主动更新元数据，确认日志"UPGRADE FOR TIERING"
                    disable/prepare阶段：停chunk触发recover
                    disable/prepare阶段：对老卷进行resize / update / reserve触发被动更新元数据
                    disable阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为false
                    prepare阶段：zbs-meta cluster summary对应值为 False；zbs-meta cluster show_ability_state | grep "upgrade_for_tiering"为true
                Vhost
                    升级到 zbs-5.6.0 及之后的版本后 enable vhost (zbs-cluster vhost enable)
        系统盘独占物理盘升级
            zbs-5.6.1  系统盘独占物理盘，升级到5.6.2 及以上系统
        故障注入测试
            升级 meta 服务时，部分节点升级，部分节点还没有升级，重启 meta leader 触发迁移。（覆盖不同的新 meta + 旧 meta 组合）
            升级 chunk 服务时，部分节点升级，部分节点还没有升级，对新或者旧的 chunkd 注入一点故障。（前期可以先注入网络 reset 故障，覆盖 rdma/非 rdma）
    运维场景
        维护模式
            meta leader所在节点进入维护模式：主动触发切主，无io中断
            meta follower所在节点进入维护模式：不会进行切主，无io中断
            存储节点进入维护模式：不会进行切主，无io中断
数据静态加密
    UI 验证
        570-回收站相关
            备份+导入：普通卷加入回收站：密钥正常备份，同时导入密钥后，恢复卷io正常
            备份+导入：克隆卷加入回收站，父卷存在（有相同的meta data id），密钥正常备份，同时导入密钥后，恢复卷io正常
            备份+导入：克隆卷加入回收站，父卷不存在（无相同的meta data id），密钥正常备份，同时导入密钥后，恢复卷io正常
            编辑集群加密设置：加密卷处于回收站时，前后端禁止编辑
            轮换密钥：处于回收站的加密卷，也需要进行密钥轮换，轮换后，恢复加密卷io正常
            所有集群——使用不同加密算法的卷移入回收站后，详情页中加密字段展示与移入回收站之前一致
            SMTX OS（ELF）/SMTX ZBS—— 回收站中的卷可以恢复到任意加密设置的 pool 中，恢复后卷的加密设置与回收站中一致
            SMTX OS（vmvare）——回收站中的卷只能恢复到与卷加密算法一致的 export 中，恢复后卷的加密设置与回收站中一致
    回收站相关
        备份导入密钥 - 普通卷加入回收站：密钥正常备份，同时导入密钥后，恢复卷io正常
        备份导入密钥 - 普通卷加入回收站：克隆卷，父卷存在，正常备份，同时导入密钥后，恢复卷io正常
        备份导入密钥 - 普通卷加入回收站：克隆卷，父卷不存在，正常备份，同时导入密钥后，恢复卷io正常
        集群加密设置 - 加密卷处于回收站时，前后端禁止编辑
        轮换密钥 - 处于回收站的加密卷，也需要进行密钥轮换，轮换后，恢复加密卷io正常
    支持国密及 Native KMS - OS 6.3.0 & ZBS 5.7.1
        UI 验证
            密钥管理服务
                添加密钥管理服务 - 文案
                添加密钥管理服务 - 校验
                添加密钥管理服务 - 交互
                编辑基本信息 - 校验
                编辑基本信息 - 交互
                建立可信连接 - 上传证书和私钥 - 文案
                建立可信连接 - 上传证书和私钥 -  校验
                建立可信连接 - 生成 CSR - 文案
                建立可信连接 - 生成 CSR - 校验
                建立可信连接 - 生成 CSR - 交互
                建立可信连接 - 上传密钥管理服务签名的证书 - 文案
                建立可信连接 - 上传密钥管理服务签名的证书 - 校验
                密钥管理服务列表 - 已添加密钥管理服务
                秘钥管理服务详情
            集群加密设置
                开启集群加密 - 文案
                开启集群加密 - 页面展示 - 数据加密切换至开启
                开启集群加密 - 页面展示 - 数据加密已开启
            加密加速
                集群已开启加密加速——集群设置加密界面展示正确：加密加速已开启，hover 正确
                集群已开启加密加速——选择密钥管理服务时可以选择仅支持 SM4 的 KMS
                集群已开启加密加速——关联外部 KMS 或者内置 KMS，创建存储资源可以选择 SM4
                集群未开启加密加速——集群设置加密页面展示正确：加密加速未开启，hover 展示正确
                集群未开启加密加速——关联外部 KMS 或者内置 KMS，创建存储资源时禁止选择 SM4，右端展示禁用原因
                集群未开启加密加速——选择密钥管理服务时禁止选择仅支持 SM4 的 KMS，其他可选场景下的 KMS 关联正常
            存储资源
                Target/Subsystem - 新建 - 校验
                Target/Subsystem - 新建 - 集群未开启数据加密
                Target/Subsystem - 新建 - 集群已开启数据加密
                Target/Subsystem - 编辑 - Target/Subsystem 未开启数据加密
                Target/Subsystem - 编辑 - Target/Subsystem 已开启数据加密
                Target/Subsystem - 列表
                Target/Subsystem - 详情
                LUN/NS - 新建 - 校验
                LUN/NS - 新建 - 集群未开启数据加密
                LUN/NS - 新建 - 集群已开启数据加密
                LUN/NS - 编辑 - 集群未开启数据加密
                LUN/NS - 编辑 - 集群已开启数据加密，且 LUN/NS 也开启数据加密
                LUN/NS - 编辑 - 集群已开启数据加密，但 LUN/NS 未开启数据加密
                LUN/NS - 列表
                LUN/NS - 详情
                Arcfra - 所有加密资源隐藏「加密算法」相关展示
        基础功能
            外部 KMS
                密钥管理服务
                    添加密钥管理服务 - 加密算法配置
                    建立可信连接 - 上传证书和私钥 - 与旧版本一致，参考原有用例
                    建立可信连接 - 生成 CSR
                    建立可信连接 - 首次建立可信连接 - 上传证书和私钥 - 部分密钥管理服务器连接正常 - 创建成功
                    建立可信连接 - 首次建立可信连接 - 上传密钥管理服务签名的证书 - 部分密钥管理服务器连接正常 - 创建成功
                    建立可信连接 - 首次建立可信连接 - 上传证书和私钥 - 证书或私钥文件错误，所有密钥管理服务器连接异常 - 创建失败
                    建立可信连接 - 首次建立可信连接 - 上传证书和私钥 - 加密算法与 KMS 不匹配，所有密钥管理服务器连接异常 - 创建失败
                    建立可信连接 - 首次建立可信连接 - 上传密钥管理服务签名的证书 - 签名证书错误，所有密钥管理服务器连接异常 - 创建失败
                    建立可信连接 - 首次建立可信连接 - 上传密钥管理服务签名的证书 - 加密算法与 KMS 不匹配，所有密钥管理服务器连接异常 - 创建失败
                    建立可信连接 - 首次建立可信连接 - 不生成CSR，直接上传签名证书 - 创建失败
                    建立可信连接 - 首次建立可信连接 - 生成CSR与上传签名证书不匹配 - 创建失败
                    建立可信连接 - 修改当前可信连接 - 生成CSR与上传签名证书不匹配 - 修改失败
                    建立可信连接 - 修改当前可信连接 - 上传证书和私钥 - 上传新的证书和私钥，存在连接正常的密钥管理服务器 - 修改成功
                    建立可信连接 - 修改当前可信连接 - 上传证书和私钥 - 上传新的密钥管理服务签名的证书，存在连接正常的密钥管理服务器 - 修改成功
                    建立可信连接 - 修改当前可信连接 - 上传密钥管理服务签名的证书 - 修改为「上传证书和私钥」，存在连接正常的密钥管理服务器 - 修改成功
                    建立可信连接 - 修改当前可信连接 - 上传密钥管理服务签名的证书 - 上传新的密钥管理服务签名的证书，存在连接正常的密钥管理服务器 - 修改成功
                    建立可信连接 - 修改当前可信连接 - 上传证书和私钥 - 上传新的证书和私钥，但所有密钥管理服务器连接异常 - 修改失败
                    建立可信连接 - 修改当前可信连接 - 上传密钥管理服务签名的证书 - 上传新的密钥管理服务签名的证书，但所有密钥管理服务器连接异常 - 修改失败
                    建立可信连接 - 修改当前可信连接 - 上传证书和私钥 - 修改为「上传密钥管理服务签名的证书」，但所有密钥管理服务器连接异常 - 修改失败
                    建立可信连接 - 修改当前可信连接 - 上传密钥管理服务签名的证书 - 修改为「上传证书和私钥」，但所有密钥管理服务器连接异常 - 修改失败
                    编辑基本信息 - 未建立可信连接
                    编辑基本信息 - 已建立可信连接 - 修改加密算法，且 KMS 支持新增算法 - 修改成功
                    编辑基本信息 - 已建立可信连接 - 修改加密算法，但 KMS 不支持新增算法 - 修改成功，但下发到集群失败
                    编辑基本信息 - 已建立可信连接 - 修改 IP/端口(与当前 KMS 不匹配) - 修改失败
                    删除密钥管理服务 - 密钥管理服务未被集群使用 - 删除成功
                    删除密钥管理服务 - 密钥管理服务已被集群使用 - 无法删除，且展示关联的集群名称
                    导出密钥管理服务 - 存在密钥管理服务 - 导出成功
                存储资源配置
                    Target/Subsystem - 新建 - 加密算法: AES256 - 创建成功
                    Target/Subsystem - 新建 - 加密算法: SM4 - 创建成功
                    Target/Subsystem - 编辑 - 加密算法: AES256 -> SM4  - 修改成功
                    Target/Subsystem - 编辑 - 加密算法: SM4 -> AES256  - 修改成功
                    Target/Subsystem - 列表导出 - 导出成功，数据加密字段值正确
                    Target/Subsystem - 高级筛选 - 加密算法 - 筛选结果符合预期
                    LUN/NS - 新建 - 加密算法: AES256 - 创建成功
                    LUN/NS - 新建 - 加密算法: SM4 - 创建成功
                    LUN/NS - 新建 - 连续创建大量加密卷 - 创建成功
                    LUN/NS - 新建 - 加密卷连续创建大量快照 - 创建成功
                    LUN/NS - 新建 - 连续大量克隆加密卷 - 克隆成功
                    LUN/NS - 编辑 - 无可用 KMS，且 KEK 缓存丢失，修改加密卷非加密参数 - 修改成功
                    LUN/NS - 列表导出 - 列表包含已开启加密/未开启加密的卷 - 导出成功，且数据加密字段值正确
                    LUN/NS - 高级筛选 - 加密算法 - 筛选结果符合预期
            内置 KMS
                集群加密设置
                    开启数据加密 - 选择内置密钥管理服务 - 开启成功，其状态正常
                    开启数据加密 - 开启时，Meta Leader 故障 - 开启失败，Meta Leader 切主后，再次开启可成功
                    开启数据加密 - 开启时，KMS 处于重建失败状态 - 开启失败
                    关闭数据加密 - 集群已开启数据加密，但无加密卷 - 关闭成功
                    关闭数据加密 - 集群存在加密卷 - 数据加密按钮置灰禁用，屏蔽入口
                    关闭数据加密 - 关闭时，Meta Leader 故障 - 关闭失败，Meta Leader 切主后，再次关闭可成功
                    关闭数据加密 - 关闭时，KMS 处于重建失败状态 - 关闭成功
                    修改密钥管理服务 - 集群无加密卷 - 外部 KMS -> 内置 KMS - 修改成功
                    修改密钥管理服务 - 集群无加密卷 - 内置 KMS  -> 外部 KMS ->  - 修改成功
                    修改密钥管理服务 - 集群存在加密卷 - 密钥管理服务选项框置灰禁选，屏蔽入口
                    修改密钥管理服务 - 内置 KMS -> 外部 KMS - Meta Leader 故障 - 修改失败，内置 KMS 可正常使用
                    修改密钥管理服务 - 内置 KMS -> 外部 KMS - 外部 KMS 异常 - 修改失败，内置 KMS 可正常使用，外部 KMS 恢复后，再次修改可成功
                    修改密钥管理服务 - 内置 KMS -> 外部 KMS - 内置 KMS 处于重建失败状态 - 修改成功
                    修改密钥管理服务 - 外部 KMS -> 内置 KMS - Meta Leader 故障 - 修改失败，外部 KMS 可正常使用
                    修改密钥管理服务 - 外部 KMS -> 内置 KMS - 内置 KMS 处于重建失败状态 - 修改失败，外部 KMS 可正常使用
                    关联已开启并激活内置 KMS 的集群 - 正确展示集群加密信息：数据加密状态/密钥管理服务/服务状态
                存储资源配置
                    Target/Subsystem - 新建 - 加密算法：AES256  - 新建成功
                    Target/Subsystem - 新建 - 加密算法：SM4  - 新建成功
                    Target/Subsystem - 新建 - 内置 KMS 处于重建失败状态  - 新建成功
                    Target/Subsystem - 编辑 - 修改加密算法：AES256 -> SM4 - 修改成功
                    Target/Subsystem - 编辑 - 修改加密算法：SM4 -> AES256 - 修改成功
                    Target/Subsystem - 编辑 - 内置 KMS 处于重建失败状态 - 修改成功
                    Target/Subsystem - 删除 - 删除开启加密的 Target/Subsystem  - 删除成功
                    Target/Subsystem - 删除 - KMS 处于重建失败状态，删除 Target/Subsystem  - 删除成功
                    Target/Subsystem - 列表导出 - 列表包含已开启加密/未开启加密的 Target/Subsystem - 导出成功，数据加密字段值正确
                    LUN/NS - 新建 - 加密算法: AES256 - 新建成功
                    LUN/NS - 新建 - 加密算法: SM4 - 新建成功
                    LUN/NS - 新建 - 连续创建大量加密卷 - 创建成功
                    LUN/NS - 新建 - 加密卷连续进行大量快照 - 创建成功
                    LUN/NS - 新建 - 连续大量克隆加密卷 - 克隆成功
                    LUN/NS - 新建 - 内置 KMS 处于重建失败状态 - 创建失败，KMS 恢复后，重新创建可成功
                    LUN/NS - 编辑 - 内置 KMS 处于重建失败状态，修改非加密参数 - 修改成功
                    LUN/NS - 删除 - 删除加密卷 - 删除成功
                    LUN/NS - 删除 - 内置 KMS 处于重建失败状态，删除加密卷 - 删除成功
                    LUN/NS - 列表导出 - 列表包含已开启加密/未开启加密的卷 - 导出成功，数据加密字段值正确
        Native KMS 专项
            KMS Key
                启停/激活
                    启动 - 非双活 - 集群节点数: 3-5，share 下发到所有节点
                    启动 - 非双活 - 集群节点数大于 5，share 下发到 5 个节点，且 share 节点符合拓扑安全
                    启动 - 非双活 - 节点故障后，开启 native kms - 故障后健康节点 3-5 个 - 下发 share 所有健康节点，native kms 成功启动
                    启动 - 非双活 - 节点故障后，开启 native kms - 故障后健康节点 > 5 个 - 下发 share 到 5 个健康节点，native kms 成功启动，且节点选择满足拓扑安全
                    启动 - 非双活 - 节点故障后，开启 native kms - 故障后健康节点 < 3 个 - native kms 开启失败，并 1min 频率一直重试
                    启动 - 非双活 - 开启 Native KMS 时，下发 shard 的节点故障 - share 下发到故障节点，5s 超时
                    启动 - 双活 - 两个可用域节点数在 3-5 个之间 - share 分发到本地可用域所有节点，并分发 k-1 个 share 到远端可用域
                    启动 - 双活 - 存在节点数大于 5 的可用域 - 节点数大于 5 的可用域只分发 share 到 5 个节点，并分发 k-1 个 share 到远端可用域
                    启动 - 双活 - 存在节点数量小于 3 的可用域 - 开启失败，后台会一直重试，间隔 1min
                    启动 - 双活 - 可用域节点故障后，开启 Native KMS - 故障后可用域健康节点 3-5 个  -  分发 share 到可用域所有健康节点以及对应的 k-1 share 到远端可用域
                    启动 - 双活 - 可用域节点故障后，开启 Native KMS - 故障后可用域健康节点 > 5 个 - 分发 share 到可用域 5 个健康节点以及对应 k-1 个 share 到远端可用域
                    启动 - 双活 - 可用域节点故障后，开启 Native KMS - 故障后可用域健康节点 < 3 个 - 开启失败，后台会一直重试，间隔 1min
                    启动 - 双活 - 开启 Native KMS 时，下发 shard 的节点故障 - 下发 shard 到节点故障，5s 超时
                    关闭 - 集群已激活 native kms - 关闭失败，提示： EKMSClusterExist
                    关闭 - 集群未激活 native kms - 关闭成功，native kms 状态为：NK_STATE_UNCERTAIN
                    激活 - 非双活 - native kms 为运行状态：NK_STATE_RUNNING 且 protect-leve = 4: All shares have acked - 激活成功
                    激活 - 非双活 - native kms 为运行状态：NK_STATE_RUNNING 且 protect-leve = 3:  KMS key is recoverable - 激活成功
                    激活 - 非双活 - native kms 为运行状态：NK_STATE_RUNNING 且 protect-leve = 2: Plain key exists - 激活失败
                    激活 - 非双活 - native kms 为关闭状态： NK_STATE_UNCERTAIN - 激活失败
                    激活 - 非双活 - native kms 为创建状态： NK_STATE_CREATING - 激活失败
                    激活 - 双活 - native kms 为运行状态：NK_STATE_RUNNING ，两个可用域 protect-leve >=3 - 激活成功
                    激活 - 双活 - native kms 为运行状态：NK_STATE_RUNNING ，1 个可用域 protect-leve >=3，1 个可用域 protect-leve < 3 - 激活成功
                    激活 - 双活 - native kms 为运行状态：NK_STATE_RUNNING ，两个可用域 protect-leve < 3 - 激活失败
                    激活 - 双活 - native kms 为关闭状态：NK_STATE_UNCERTAIN  - 激活失败
                    激活 - 双活 -  native kms 为创建状态：NK_STATE_CREATING - 激活失败
                    删除 - native kms 为运行状态：NK_STATE_RUNNING 且 protect-leve = 4: All shares have acked - 删除成功
                    删除 - native kms 为运行状态：NK_STATE_RUNNING 且 protect-leve = 3:  KMS key is recoverable - 删除成功
                    删除 - native kms 为运行状态：NK_STATE_RUNNING 且 protect-leve = 2: Plain key exists - 删除成功
                    删除 - 存在加密卷/快照 - 删除失败
                    删除 - 加密卷/快照在回收站 - 删除失败
                Auto Redist
                    非双活 - 添加节点 - 节点添加后，节点数量 3-5 个 - 触发 redist
                    非双活 - 添加节点 - 节点添加后，节点数量 > 5个 - 不触发 redist
                    非双活 - 移除节点 - 节点移除后，节点数量 3-4 个 - 触发 redist
                    非双活 - 移除节点 - 移除 share 节点 ，且节点移除后，节点数量  >= 5 个 - 触发 redist
                    非双活 - 移除节点 - 移除非 share 节点 ，且节点移除后，节点数量  >= 5 个 - 不触发 redist
                    非双活 - 节点故障恢复 - 3 节点集群，故障 1 个节点 - 不触发 redist
                    非双活 - 节点故障恢复 - 4 节点集群，故障 1 个节点 - 不触发 redist
                    非双活 - 节点故障恢复 - 4 节点集群，故障 2 个节点 - 不触发 redist
                    非双活 - 节点故障恢复 - 5 节点集群，故障 1-2 个节点 - 触发 redist
                    非双活 - 非双活 - 节点故障恢复 - 集群节点数 > 5 ，故障 share 节点，故障后健康节点 >= min(N/2, 5) - 触发 redist
                    非双活 - 节点故障恢复 - 集群节点数 > 5 ，故障 share 节点，故障后健康节点 < min(N/2, 5) - 不触发 redist
                    非双活 - 节点故障恢复 - 集群节点数 > 5 ，故障非 share节点 - 不触发 redist
                    非双活 - 节点故障恢复 - 3 节点集群，1 故障节点，节点恢复后 - 不触发 redist
                    非双活 - 节点故障恢复 - 4 节点集群，1 故障节点，节点恢复后 - 不触发 redist
                    非双活 - 节点故障恢复 - 3 节点集群，2 故障节点，节点恢复后 - 不触发 redist
                    非双活 - 节点故障恢复 - 4 节点集群，1 -2 故障节点，节点恢复后 - 触发 redist
                    非双活 - 节点故障恢复 -  节点故障后，可用域健康节点数 > 5，节点故障恢复后 - 不触发 redist
                    非双活 - 拓扑调整 - 集群节点数 3-5 个，移动任意节点 - 不触发 redist
                    非双活 - 拓扑调整 - 集群节点数 > 个，节点未加入机架 - 移动任意节点  -不触发 redist
                    非双活 - 拓扑调整 - 集群节点数 > 5个，节点已加入机架 -移动节点后，当前 share 节点满足最佳拓扑 - 不触发 redist
                    非双活 - 拓扑调整 - 集群节点数 > 5个，节点已加入机架 -移动节点后，当前 share 节点拓扑降价 - 触发 redist，新的 share 节点满足拓扑安全
                    双活 - 添加节点 - 节点添加后，可用域节点数量 3-5 - 本地可用域触发 redist
                    双活 - 添加节点 - 节点添加后，可用域节点数量 >5  - 本地可用域不触发 redist
                    双活 - 移除节点 - 节点移除后，可用域节点数量 3-4 - 本地可用域触发 redist
                    双活 - 移除节点 - 移除 share 节点，节点移除后，可用域节点数量 >=5 - 本地可用域触发 redist
                    双活 - 移除节点 - 移除非 share 节点，节点移除后，可用域节点数量 >=5 - 本地可用域不触发 redist
                    双活 - 移除节点 - 移除非 share 节点，节点移除后，可用域节点数量 2 个 - 本地可用域不触发 redist
                    双活 - 节点故障恢复 - 3 节点可用域，故障 1 个节点 - 不触发本地可用域 redist
                    双活 - 节点故障恢复 - 4 节点可用域，故障 1 个节点 - 不触发本地可用域 redist
                    双活 - 节点故障恢复 - 5 节点可用域，故障 1-2 个节点 - 本地可用域触发 redist
                    双活 - 节点故障恢复 - 可用域节点数 > 5 ，故障 share 节点，故障后健康节点 >= min(N/2, 5) - 本地可用域触发 redist
                    双活 - 节点故障恢复 - 可用域节点数 > 5 ，故障 share 节点，故障后健康节点 < min(N/2, 5) - 本地可用域不触发 redist
                    双活 - 节点故障恢复 - 可用域节点数 > 5 ，故障非 share节点 - 本地可用域不触发 redist
                    双活 - 节点故障恢复 - 远端可用域备用 share 节点故障，且远端可用域存在健康节点 - 本地可用域触发 redist
                    双活 - 节点故障恢复 - 远端可用域备用 share 节点故障，且远端可用域不存在健康节点 - 本地可用域不触发 redist
                    双活 - 节点故障恢复 - 3 节点可用域，1  故障节点，节点故障恢复后 - 本地可用域不触发 redist
                    双活 - 节点故障恢复 - 4 节点可用域，1-2 故障节点，节点故障恢复后 - 本地可用域不触发 redist
                    双活 - 节点故障恢复 - 5 节点可用域，1 -2 故障节点，节点故障恢复后 - 本地可用域触发 redist
                    双活 - 节点故障恢复 - 节点故障后，可用域健康节点数 > 5，节点故障恢复后 - 本地可用域不触发 redist
                    双活 - 拓扑调整 - 可用域节点数 3-5 ，可用域内任意移动节点 - 本地可用域不触发 redist
                    双活 - 拓扑调整 - 可用域节点数 3-5 ，跨可用域移动节点 - 本地可用域触发 redist
                    双活 - 拓扑调整 - 可用域节点数 > 5，可用域内移动节点后，当前可用域 share 节点满足最佳拓扑距离 - 本地可用域不触发 redist
                    双活 - 拓扑调整 - 可用域节点数 > 5，可用域内移动节点后，当前可用域 share 节点拓扑降级 - 本地可用域触发 redist
                    双活 - 拓扑调整 - 可用域节点数 > 5，跨可用域移动 share 节点，本地可用域触发 redist
                    双活 - 拓扑调整 - 可用域节点数 > 5，跨可用域移动非 share 节点，本地可用域不触发 redist
                    双活 - 拓扑调整 - 远端可用域 2 个备份节点，远端可用域内移动备份节点后，备份节点满足最佳拓扑距离 - 本地可用域不触发 redist
                    双活 - 拓扑调整 - 远端可用域 2 个备份节点，远端可用域内移动备份节点后，备份节点拓扑降级 - 本地可用域触发 redist，远端可用域备份节点满足拓扑安全
                    双活 - 拓扑调整 - 跨可用域移动节点，节点移动后可用域节点数量为 2 - 2 节点可用域不触发 redist，且拓扑和节点移动前一致
                Rotation
                    自动 - 非双活 - kms key 重建失败，但集群未激活 native kms - 触发 rotate
                    自动 - 非双活 - kms key 重建失败，且集群已激活 native kms - 不触发 rotate
                    自动 - 非双活 - kms key 重建失败，但集群已激活 native kms，删除 native kms 后 - 触发 rotate
                    自动 - 非双活 - rotate period 到期 后，所有节点健康 - 触发 rotate
                    自动 - 非双活 - rotate period 到期 后，存在故障节点 - 不触发 rotate，但会 1.5s 频率一直重试
                    自动 - 非双活 - rotate period 到期后，存在故障节点，rotate 重试过程中 - 构造 redist 条件 - 触发 redist
                    自动 - 非双活 - rotate period 到期后，存在故障节点，rotate 重试过程中 - 所有故障节点恢复 - 节点 30s 稳定后，触发 rotate
                    自动 - 非双活 - 限制条件 - 集群健康节点数量不满足： > 3 且 >= min(N/2, min)  - 不触发 rotate
                    自动 - 双活 - kms key 重建失败，但集群未激活 native kms - 触发 rotate
                    自动 - 双活 - kms key 重建失败，且集群已激活 native kms - 不触发 rotate
                    自动 - 双活 - kms key 重建失败，但集群已激活 native kms，删除 native kms 后 - 触发 rotate
                    自动 - 双活 - 可用域增减 - 非双活转双活 - 触发 rotate
                    自动 - 双活 - 特殊场景 -  通过移动节点，构造 2 节点可用域，并手动出发 rotate - 移动  1 个节点到 2 节点可用域  - 触发 rotate
                    自动 - 双活 - rotate period 到期 - 2 个可用域所有节点健康，且可用域节点 >= 3  - 触发 rotate
                    自动 - 双活 - rotate period 到期 - 2 个可用域所有节点健康，且存在可用域节点 < 3  - 触发 rotate
                    自动 - 双活 - rotate period 到期 - 单个可用域存在故障节点 - 不触发 rotate，但会 1.5s 频率一直重试
                    自动 - 双活 - rotate period 到期 - 单个可用域存在故障节点 ，且 rotate 重试期间，构造 redist 条件 - 触发 redist
                    自动 - 双活 - rotate period 到期 - 单个可用域存在故障节点 ，且 rotate 重试期间，故障节点恢复 - 节点 30s 稳定后，触发 rotate
                    自动 - 双活 - 限制条件 - 存在可用域健康节点数量不满足： > 3 且 >= min(N/2, min) - 不触发 rotate
                    手动 - 非双活 - 集群节点数 <  3 - rotate 失败，提示节点数不足
                    手动 - 非双活 - 健康节点数不满足 >= min(N/2, min) - rotate 失败
                    手动 - 非双活 - 健康节点数满足 > 3 且 >= min(N/2, min) - rotate 成功
                    手动 - 双活 -  存在 2 节点可用域 - rotate 成功，但 2 节点可用域拓扑丢失，上报告警
                    手动 - 双活 -  存在可用域健康节点数满足 > 3 且 >= min(N/2, min) - rotate 成功
                重建
                    非双活 - 集群 share 存活数量在 k~n 个之间，meta leader 切主 - kms key 重建成功
                    非双活 - kms key 重建过程中，meta leader 再次故障 - kms key 最终重建成功
                    非双活 - 集群 share 存活数量不足 k 个，meta leader 切主  - kms key 重建失败
                    非双活 - kms Key 重建失败场景下， 故障的 share 节点恢复健康，存活数量满足 k 个 - kms key 重建成功
                    双活 - 2 个可用域本地 share 存活数量都在 k~n 个之间，meta leader 切主  - kms key 重建成功
                    双活 - 仅单个可用域本地 share 存活数量在 k~n 个之间，另一个可用域无存活 share，meta leader 切主  - kms key 重建成功
                    双活 - 2 个可用域本地 share 存活数量均不足 k 个，但有 1 个可用域本地 share 存活数量 + 远端备用 share 存活数量在 k~n 个之间，meta leader 切主 - kms key 重建成功
                    双活 - 2 个可用域本地 share 存活数量 + 远端备用 share 存活数量均不足 k 个，meta leader 切主 - kms key 重建失败
                    双活 - kms key 重建失败场景下，故障的 share 节点恢复健康，且满足可用域本地 share 存活数量 + 远端备用 share 存活数量达到 k 个 - kms key 重建成功
            Master Key
                密钥轮转
                    集群存在加密卷 - 轮转成功，加密卷正常
                    集群存在大量加密卷 - 密钥轮转成功，轮转时长即资源占用无明显异常
                    密钥轮换期间，再次发起密钥轮换 - 最后一次轮换执行失败，并提示正在轮转
                    密钥轮换期间，对加密卷创建快照 - 密钥轮换成功，快照正常
                    密钥轮换期间，新建加密卷 - 密钥轮换成功，新建加密卷正常
                    密钥轮换期间，克隆加密卷 - 密钥轮换成功，克隆卷正常
                    密钥轮换期间，基于加密快照克隆 - 密钥轮换成功，克隆卷正常
                    密钥轮换期间，Meta leader 切主，但 KMS key 重建正常 - 密钥轮换成功
                    KMS key 重建失败情况下，触发密钥轮换 - 密钥轮换失败
                    密钥轮换期间，Meta Leader 切主，且 KMS key 重建失败 - 密钥轮换失败，KMS key 重建成功后，可再次进行轮换
                密钥备份
                    仅加密卷 - 备份成功，备份 metadata_id 及数量正确
                    加密卷存在快照 - 备份成功，备份 metadata_id 及数量正确
                    加密卷及克隆卷 - 备份成功，备份 metadata_id 及数量正确
                    DEK 缓存丢失，备份密钥 - 备份成功，备份 metadata_id 及数量正确
                    备份期间，Meta leader 切主 - 备份失败/备份成功(取决于请求时机)，如果备份成功，备份 metadata_id 及数量正确
                    KMS key 重建失败，且 KEK/DEK 缓存丢失 - 备份失败
                密钥恢复
                    密钥备份后，加密卷全部存在，导入密钥 - 导入成功，且可正常恢复 IO
                    密钥备份后，全部加密卷已删除进入回收站，导入密钥  - 导入成功，加密卷从回收站恢复后可正常恢复 IO
                    密钥备份后，部分加密卷已删除且GC  - 导入成功，且已存在加密卷可正常恢复 IO
                    使用错误密码导入  - 导入失败
                    密钥备份后，所有加密卷已删除并 GC  - 导入失败，提示：[ECipherKeyCorrupt] no valid cipher key.
        基础 I/O
            卷扩容 - 加密卷正常 I/O时，对卷进行扩容 - 加密卷读写无 I/O Error，无数据不一致
            密钥轮换 - 加密卷正常 I/O时，进行密钥轮换 - 加密卷读写无 I/O Error，无数据不一致
            密钥轮换 - 密钥轮换后，清除 DEK 缓存 - 加密卷读写无 I/O Error，无数据不一致
            密钥轮换 - 加密卷正常 I/O时，进行密钥轮换，并在密钥轮换期间导入密钥 - 加密卷读写无 I/O Error，无数据不一致
            快照克隆 - 加密卷 I/O 时，创建快照 - 快照读无 I/O Error，无数据不一致
            快照克隆 - 加密卷从快照回滚 - 加密卷无 I/O Error，无数据不一致
            快照克隆 - 加密卷完全克隆 - 克隆到加密卷  - 克隆卷读写无 I/O Error，无数据不一致
            快照克隆 - 加密卷完全克隆 - 克隆到非加密卷  - 克隆卷读写无 I/O Error，无数据不一致
            快照克隆 - 非加密卷完全克隆 - 克隆到加密卷 - 克隆卷读写无 I/O Error，无数据不一致
            快照克隆 - 从加密快照克隆 - 克隆卷读写无 I/O Error，无数据不一致
            密钥导入 - 加密卷正常 I/O时，导入密钥 - 加密读写无 I/O Error，无数据不一致
            密钥导入 - 加密卷无法 I/O时，导入密钥 - 加密卷读写无 I/O Error，无数据不一致
            密钥导入 - 加密卷在导入密钥正常 I/O 后，DEK 缓存丢失 - 加密卷无法 I/O
            故障场景 - 加密卷 I/O 过程中，DEK 缓存丢失 - 加密读写无 I/O Error，无数据不一致
            故障场景 - 加密卷 I/O 过程中，KEK 及 DEK 缓存丢失，但 KMS(外部/内置) 可用 - 加密读写无 I/O Error，无数据不一致
            故障场景 - 加密卷 I/O 过程中，KEK 及 DEK 缓存丢失,且 KMS 不可用(外部/内置) - 加密卷无法 I/O
            故障场景 - KEK 及 DEK 缓存丢失，且 KMS(外部/内置) 不可用，对加密卷进行 I/O - 加密卷无法 I/O
        长稳/故障
            大量加密卷持续进行 I/O，并在过程中，持续进行卷转换/扩容/快照/克隆混合业务，此外再叠加集群内故障以及 KMS 故障
        升级部署
            部署 - 非双活 - 集群节点数: 3-5 - native kms 成功自动启动，share 下发所有节点
            部署 - 非双活 - 集群节点数: > 5 - native kms 成功自动启动，share 下发 5 个节点，且满足最佳拓扑
            部署 - 双活 - 两个可用域节点数在 3-5 -  native kms 成功自动启动，share 下发到本地可用域所有节点，并分发 k-1 个 share 到远端可用域
            部署 - 双活 - 两个可用域节点数 > 5 - native kms 成功自动启动，节点数大于 5 的可用域只分发 share 到 5 个节点，且满足最佳拓扑，并分发 k-1 个 share 到远端可用域
            部署 - 双活 - 存在节点数量小于 3 的可用域  - native kms 启动失败，后台会一直重试，间隔 1min
            升级 - 非双活 - smtxos 6.2.0 升级到该版本 ，且集群节点数: 3-5，并开启数据加密 - native kms 成功自动启动，share 下发所有节点
            升级 - 非双活 - smtxos 6.2.0 升级到该版本 ，且集群节点数 > 5 - native kms 成功自动启动，share 下发 5 个节点，且 share 节点符合最佳拓扑
            升级 - 非双活 - smtxos 5.1.5 升级到该版本 ，且集群节点数: 3-5 - native kms 成功自动启动，share 下发所有节点
            升级 - 非双活 - smtxos 5.1.5 升级到该版本 ，且集群节点数 > 5 - native kms 成功自动启动，share 下发 5 个节点，且 share 节点符合最佳拓扑
            升级 - 双活 - smtxos 6.2.0 升级到该版本 ，1 个可用域节点数量 3-5，另一个可用域节点数 > 5，且集群开启数据加密 - native kms 成功自动启动，3-5 节点可用域 share 下发到所有节点，节点数 > 5 可用域，share 下发到5个节点，且符合最佳拓扑
            升级 - 双活 - smtxos 6.2.0 升级到该版本 ，存在节点数量为 2 的可用域 - native kms 自动启动失败，并一直重试
            升级 - 双活 - smtxos 5.1.5 升级到该版本，1 个可用域节点数量 3-5，另一个可用域节点数 > 5 - native kms 成功自动启动，3-5 节点可用域 share 下发到所有节点，节点数 > 5 可用域，share 下发到5个节点，且符合最佳拓扑
            升级 - 双活 - smtxos 5.1.5 升级到该版本 ，存在节点数量为 2 的可用域 - native kms 自动启动失败
        监控报警
            集群正在恢复内置 KMS 密钥
            集群存在未恢复的内置 KMS 密钥，已有加密资源当前可能无法使用
            可用域 { .labels.name } 无法提供内置 KMS 的拓扑结构保护
            当前内置 KMS 密钥保护的期望存活分片数量为 { .labels.expect_count }，实际存活分片数量为 { .labels.alive_count }。
        CLI
            zbs-meta native_key show
            zbs-meta native_key rotate
            zbs-meta native_key reload
            zbs-meta native_key destroy
            zbs-meta kms list
            zbs-meta kms list_master_key
            zbs-meta kms rotate_key
            zbs-meta kms export_key
            zbs-meta kms import_key
            zbs-meta kms create_kmip
            zbs-meta kms delete_kmip
            zbs-meta kms refresh_kmip
            zbs-meta kms update_kmip_attr
            zbs-meta kms update_kmip_auth
            zbs-meta kms update_kmip_server
            zbs-meta kms list_kmip_server
            zbs-meta kms create_native
            zbs-meta kms delete_native
            zbs-meta kms update_native
            zbs-meta kms show_native
卷快照计划
    快照组管理
        回滚
            回滚快照组 - 正常场景 - 文案：lun/ns/一致性组：可回滚
            回滚快照组 - 说明文案 - 正常场景 - lun或者ns属于一致性组：随一致性组回滚
            回滚快照组 - 说明文案 - 异常场景 - lun/ns：不可回滚：快照组中不包含该快照/快照对象已经移出快照计划
            回滚快照组 - 说明文案 - 异常场景 - lun或者ns：不可回滚：包含不存在的快照对象/包含已移出快照计划的快照对象/包含已移出一致性组的快照对象
        重建
            重建 - 选择快照对象 - 支持查看一致性组成员（同创建）
            重建 - 配置 - 当lun/ns属于一致性组时，在源卷的名称下方添加展示所属一致性组名称
            重建 - namespace配置：均衡策略需要选择卷分组
            重建快照组 - 目标target/subsystem数量校验：默认目标target/subsystem的卷数量为255，目标target/subsystem置空
            重建快照组 - 目标target/subsystem数量校验：选择目标target/subsystem的卷数量+该目标target也有lun数量>255，弹出报错文案：选择该target的lun与target已有lun总数已达上限（255）
DataChannel 支持多路径
    部署
        tcp 模式
            新部署 zbs 5.7.0，存储单网卡，chunk 默认开启多路径。
            新部署 zbs 5.7.0，存储 2 网卡 + ovs ab，chunk 默认开启多路径。
            新部署 zbs 5.7.0，存储 4 网卡 + ovs balance-tcp，chunk 默认开启多路径。
            新部署 zbs 5.7.0，存储 3 网卡 + balance-slb，chunk 默认开启多路径。
        rdma 模式
            新部署 zbs 5.7.0，存储单网卡，chunk 默认开启多路径。
            新部署 zbs 5.7.0，存储 2 网卡 + ovs ab，chunk 默认开启多路径。
            新部署 zbs 5.7.0，存储 4 网卡 + ovs balance-tcp，chunk 默认开启多路径。
            新部署 zbs 5.7.0，存储多网卡，无法使用 balance-slb。
    升级
        tcp 模式
            v1 ovs ab 升级到 ZBS 5.7.0，chunk 默认开启多路径
            v2 ovs balance-slb 升级到 ZBS 5.7.0，chunk 默认开启多路径
            v1 ovs balance-tcp(交换机是 src-dst-mac) 升级到 ZBS 5.7.0，chunk 默认开启多路径
            v2 ovs balance-tcp(交换机是 src-dst-port) 升级到 ZBS 5.7.0，chunk 默认开启多路径
        RDMA 模式
            v1 rdma + ovs balance-slb 升级到 ZBS 5.7.0，chunk 默认开启多路径
            v1 rdma + ovs balance-tcp（交换机是 src-dst-mac） 升级到 ZBS 5.7.0，chunk 默认开启多路径
            v2 rdma + linux ab 升级到 ZBS 5.7.0，chunk 默认开启多路径
            v2 rdma + linux 802.3 ad 升级到 ZBS 5.7.0，chunk 默认开启多路径
    多路径开启与关闭
        无论如何编辑 bond mode，chunk 侧的多路径都不会被自动关闭。只能临时手动关闭。
    流控
        RDMA 模式下，开启多路径，测试流控
        TCP 模式下，开启多路径，测试流控
        集群开启多路径的情况下，简单跑下单卷 / 多卷性能，确保每个路径流量差不多，且基本能跑满。
        修改存储网卡的 bond name 之后，测试流控
    连接数检查
        正常情况下，节点 AB 间连接数 = min(nic_num_A, nic_num_B)
        发生故障时连接可能被 shutdown，但故障恢复后，连接数要能恢复
        网口下线，RDMA 模式下需要重启 chunkd，dcc 和 dcs 中该网口的连接都会被断开。
        网口下线，TCP 模式下无需重启 chunkd，预期该节点 chunk 会断开使用该网卡的 dcc 连接（本地到其他节点），但不会清理 dcs 的连接（其他节点到本地），避免影响其他节点 IO。
        多实例场景下，多实例之间只会产生单个连接
    cli
        tcp + 多实例 + enable 多路径，zbs-chunk dc get_server_info / zbs-chunk dc get_manager_info
        tcp + 单实例 + disable 多路径，zbs-chunk dc get_server_info / zbs-chunk dc get_manager_info
        rdma + 多实例 + disable 多路径，zbs-chunk dc get_server_info / zbs-chunk dc get_manager_info
        rdma + 单实例 + enable 多路径，zbs-chunk dc get_server_info / zbs-chunk dc get_manager_info
    运维操作
        修改存储网口
            TCP 模式，通过 tower 将单网卡修改为多网卡，并设置 bond 为 balance-tcp，chunk 侧多路径保持开启
            TCP 模式，通过 tower 将 2 网卡（ovs ab）修改为 4 网卡（balance-tcp），chunk 侧多路径保持开启，修改交换机端 load balance 策略为 src-dst-port，连接数动态增加。
            TCP 模式，通过 tower 将 4 网卡（balance-tcp 且交换机为 src-dst-port）修改为 3 网卡（balance-tcp），chunk 侧多路径保持开启，检查连接数, 不应 IO Generation 乱序导致剔副本
            TCP 模式，通过 tower 将 2 网卡（nic1 + nic2 组成的balance-tcp）修改为 3 网卡（nic3 + nic4 + nic5 组成的 balance-tcp），相当于同时移除和添加 nic，检查连接数，预期该节点 chunk 会断开使用 nic1 / nic2 的 dcc 连接（本地到其他节点），但不会清理 dcs 的连接（其他节点到本地），也不会发生 IO Generation 乱序导致踢副本。
            RDMA 模式，通过 network-tool 将 3 网卡（ovs balance-tcp）修改为 2 网卡（ab），chunk 侧多路径保持开启，内部会自动重启 chunk，检查连接数变为单路径。
            RDMA 模式，通过 network-tool 将单网卡修改为 4 网卡（balance-tcp），chunk 侧多路径保持开启，内部会自动重启 chunk，检查连接数变为多路径。
            RDMA 模式，通过 network-tool 将单节点 4 网卡（balance-tcp）修改为 3 网卡，chunk 侧多路径保持开启，内部会自动重启 chunk，检查连接数:节点 AB 间连接数 = min(nic_num_A, nic_num_B)
            RDMA 模式，通过 network-tool 将 2 网卡（nic1+nic2 组成的 ab）修改为 3 网卡（nic3-5 组成的 balance-tcp），相当于同时移除和添加，内部会自动重启 chunk，检查连接数，预期连接数发生变化，且仅有 nic3-5。
        修改存储 bond 类型和模式
            RDMA + linux ab 可转为 ovs ab / balance-tcp，操作正常，多路径状态取决于 bond type + 交换机配置（v2 升级而来）
            RDMA + linux xor 可转为 ovs ab / balance-tcp，操作正常，多路径状态取决于 bond type + 交换机配置（v2 升级而来）
            RDMA + linux 802.3ad 可转为 ovs ab / balance-tcp，操作正常，多路径状态取决于 bond type + 交换机配置（v2 升级而来）
            RDMA + ovs ab 可转为 balance-tcp / 单网卡，操作正常，多路径状态取决于 bond type + 交换机配置（v2 升级而来）
            RDMA + ovs balance-tcp 可转为 ovs ab / 单网卡，操作正常，多路径状态取决于 bond type + 交换机配置（v2 升级而来）
            RDMA 不支持修改目的 bond mode 为 balance-slb
            TCP 单网卡 -> balance-tcp，交换机配置正确后，多路径正常开启，检查连接数。
            TCP balance-tcp -> balance-slb，多路径正常关闭，检查连接数。
        集群扩缩容（节点数变更）
            原本集群均是单网口，新加节点只能是单网口，不能开 bond，但新节点 chunk 多路径是开启的。
            原本集群是 balance-tcp（且均为 2 网口），新加节点并且 storage_nic=3，bond 模式也只能是 balance-tcp，预期集群多路径正常。检查连接数。
            原本集群是 balance-tcp，新加节点并且选择单网口，该节点 chunk 虽开启多路径，但实际该节点保持单路径，其他节点多路径正常。
            开启多路径（balance-tcp），移除节点流程正常。
            关闭多路径（chunk 开启，但 bond 非 balance-tcp），移除节点流程正常。
            集群存储网为 linux bond，移除节点成功，添加节点后，节点 bond 和集群已有节点的 bond 一致
            集群存储网开启了 RDMA，bond 为 balance-slb，移除节点成功，添加节点后，新节点 bond 也是 balance-slb
        交换机运维
            交换机堆叠或 m-lag
            交换机升级 / 固件升级
            TCP 模式下，交换机配置 trunk vlan
    故障
        主机端故障
            网卡故障下的 IO 测试
            服务故障下的 IO 测试
            节点电源故障下的 IO 测试
        交换机侧故障
            多路径下，交换机个别/多个端口持续 shutdown
            多路径下，交换机电源故障
            多路径下，交换机配置 load-balance 策略为非 src-dst-port
            多路径下，交换机 lacp 配置错误
            多路径下，交换机电源故障
    异常场景
        低版本 zbs 使用 RDMA + balance-slb 升级至 ZBS 5.7.0，观察半天到一天并跑一些基础 IO 测试
    metric 测试
        zbs-chunk show_polling_stats 观察 chunk cpu 开销，预期不会额外增长太多
RDMA 支持跨网卡并改用 ovs bonding
    部署
        RDMA + 同一网卡间 bond（cx4 / cx5 / cx6 任意选一即可）+ ovs ab，功能正常，流控正常。
        RDMA + 跨网卡 bond（4 网口，cx4 / cx5）+ ovs balance-tcp，功能正常，流控正常，多路径正常。
        开启 RDMA，部署时不支持 balance-slb bond
        部署时存储网启用 RDMA，选择关联网口时，可以选择不同网卡的网口
        部署时存储网启用 RDMA，关联网口选择多个后，展示网口绑定模式，默认选择 active-backup，仅支持选择 active-backup 和 balance-tcp
    升级
        v1 + rdma + 同一网卡间 bond + ovs balance-tcp，升级至 zbs 5.7.0，功能正常，流控正常，升级后修改交换机配置为 src-dst-port，多路径正常。
        v1 + rdma + 跨网卡 bond（balance-slb），升级至 zbs 5.7.0，功能正常，流控正常，升级后修改 bond 模式为 balance-tcp，并修改交换机配置为 src-dst-port，多路径正常
        v2 + rdma + linux xor，升级至 zbs 5.7.0，功能正常，流控正常，并可通过 network-tool 修改为 balance-tcp，配合交换机 src-dst-port，多路径正常
        v2 + rdma + linux 802.3ad，升级至 zbs 5.7.0，功能正常，流控正常，后期可转为 balance-tcp，配合 src-dst- port，多路径正常
    交换机相关
        开启 RDMA，部署时选择的网卡跨交换机（M-LAG 或堆叠），bond 可以选择（ovs-ab / ovs balance-tcp），balance-tcp 必须验证。部署正常，集群可正常工作。
        开启 RDMA，部署时选择的网卡跨交换机（M-LAG 或堆叠），bond 可以选择（ovs-ab / ovs-balance-tcp），升级正常，集群可正常工作。
        交换机故障（比如 lacp 配置不正确，交换机断电，交换机升级，固件升级等），连接正常？
    metric 测试
        host_network_rdma_receive_bytes: RDMA 网口数据接收总量
        host_network_rdma_transmit_bytes: RDMA 网口数据发送总量
        host_network_rdma_receive_speed_bitps: RDMA 网口数据接收速度
        host_network_rdma_transmit_speed_bitps RDMA 网口数据发送速度
        host_network_rdma_receive_packets: RDMA 网口收包总量
        host_network_rdma_transmit_packets: RDMA 网口发包总量
    故障测试
        rdma + ovs ab / balance-tcp，FI
        rdma + ovs balance-tcp，长稳。
        跨网卡 bond 中，网口 / 交换机端口 / 故障或频繁故障。
    添加主机
        集群存储网启用了 RDMA 且为 ovs bond 时，添加主机选择关联网口时，支持选择不同网卡上的网口
        集群存储网启用了 RDMA 且为 linux bond 时，添加主机选择关联网口时，禁止选择不同网卡上的网口
ZBS 卷回收站
    Tower UI
        回收站 widget
            Tower organization 层
            集群层（ZBS 集群）
            集群层 - OS（VMware ESXi）版本低于630，不展示widget
            集群层 - OS（VMware ESXi）版本>=630未开启回收站，不展示widget
            集群层 - OS（VMware ESXi）版本>=630且开启回收站，widget展示NFS文件计数
            集群层 - OS（ELF）未开启块存储：仅展示虚拟机计数
            集群层 - OS（ELF）开启块存储，版本低于630：仅展示虚拟机计数
            集群层 - OS（ELF）开启块存储，版本>=630：展示虚拟机和LUN计数
            集群层 - ELF集群：仅展示虚拟机计数
            集群层 - 点击widget跳转 - 筛选出对应集群资源：OS（ELF）/ELF跳转至回收站虚拟机页面，只展示当前集群虚拟机
            集群层 - 点击widget跳转 - 筛选出对应集群资源：ZBS跳转至回收站LUN页面，只展示当前集群LUN
            集群层 - 点击widget跳转 - 筛选出对应集群资源：OS（VMware ESXi）跳转至回收站NFS文件页面，只展示当前集群NFS文件
            org层、DC层 - 点击widget跳转 - 跳转至回收站功能导航第一个页面
            org层、DC层 - 展示所有资源总数，格式为“共N个”
            widget - 删除info icon
        回收站入口（导航栏）
            新安装 Tower 各种资源为空（未关联集群），不显示回收站入口
            Tower 仅关联 os 集群时，展示回收站入口，回收站页面的子列表仅展示「虚拟机」列表
            Tower 仅关联 zbs 570 及以上集群，且没有卸载该集群内的系统服务时，展示回收站入口，回收站页面的子列表仅展示「LUN」和「Namespace」列表
            Tower 仅关联 zbs 570 及以上集群，该集群内的系统服务被卸载后，回收站页面的子列表展示「虚拟机」「LUN」和「Namespace」列表
            Tower 仅关联 570 以下的 zbs 集群，不展示回收站入口
            Tower 同时关联 os 集群 和 570 及以上的 zbs 集群，展示回收站入口，回收站页面的子列表展示「虚拟机」「LUN」「Namespace」
            towe-480:去掉全部资源对象功能页
            tower480:仅关联低于630版本的OS（VMware ESXi）集群 - 一级导航不展示回收站
            tower480：仅关联OS（ELF）集群 - 集群启用块存储且版本为630及以上 - 回收站导航展示LUN和虚拟机
            tower480：仅关联OS（ELF）集群 - 集群不启用块存储且版本为630及以上 - 回收站导航仅展示虚拟机
            tower480：仅关联OS（ELF）集群 - 集群版本低于630 - 回收站导航仅展示虚拟机
            tower480: 仅关联低于630版本的OS（VMware ESXi）集群 - 一级导航不展示回收站
            tower480: 仅关联630及以上版本的OS（VMware ESXi）集群 - 一级导航展示回收站
            tower480: 仅关联630及以上版本的OS（VMware ESXi）集群 - 回收站仅展示NFS文件
            tower480:同时关联OS（ELF）集群或者ELF集群和570及以上版本的zbs集群 -一级导航展示回收站，回收站导航展示虚拟机和LUN、Namespace
            tower480:同时关联OS（ELF）集群或者ELF集群和630及以上版本的OS（VMware ESXi）集群 - 一级导航展示回收站，回收站导航展示虚拟机和NFS文件
            tower480:同时关联570及以上版本的zbs集群和630及以上版本的OS（VMware ESXi）集群 - 一级导航展示回收站，回收站导航展示LUN、Namespace和NFS文件
            tower480:同时关联OS（ELF）、570及以上版本的zbs、630及以上版本的OS（VMware ESXi）集群 - 一级导航展示回收站，回收站导航展示虚拟机、LUN、Namespace和NFS文件
        回收站：资源 Table
            开启常驻缓存的卷的恢复
            开启加密的卷的恢复
            批量卷恢复，选择不同白名单配置
            tower 480 - 去掉全部资源对象
            一键清空
                虚拟机 table - 一键清空（列表超长）
                一键清空时，单个集群中的待清理资源不超过阈值
                    全部资源 table - 一键清空（允许一键清空）
                    全部资源 table - 一键清空（不允许一键清空，比如权限问题）
                    全部资源 table - 所有 zbs 集群在回收站中的资源都不超过阈值：等于阈值，小于阈值，一键清空成功，任务均展示详情
                    虚拟机 table - 一键清空（允许一键清空）
                    虚拟机 table - 一键清空（不允许一键清空，比如权限问题）
                    lun table - 一键清空（允许一键清空）
                    lun table - 一键清空（不允许一键清空，比如权限问题）
                    lun table - 所有 zbs 集群在回收站中的 lun 都不超过阈值：等于阈值，小于阈值，一键清空成功，任务均展示详情
                    lun table - 一键清空失败（存在卷已被删除，只是由于未及时同步依然显示在列表）
                    ns table - 一键清空（允许一键清空）
                    ns table - 一键清空（不允许一键清空，比如权限问题）
                    ns table - 所有 zbs 集群在回收站中的 ns 都不超过阈值：等于阈值，小于阈值，一键清空成功，任务均展示详情
                    ns table - 一键清空失败（存在卷已被删除，只是由于未及时同步依然显示在列表）
                    集群在回收站中的 lun 和 ns 数量均没有超出阈值：cli 发起一键清空 lun 任务后，tower 上触发 ns 列表中的一键清空任务，任务成功
                    NFS文件 table - 一键清空（允许一键清空）
                    NFS文件 table - 一键清空（存在跳过资源：跳过tip）
                    NFS文件 table - 所有 zbs 集群在回收站中的 NFS 都不超过阈值：等于阈值，小于阈值，一键清空成功，任务均展示详情
                    存在集群的待删除资源超过1000个 - 文案：N个集群的带删除资源超过1000个，对应集群的删除任务将不提供任务详情，N个集群 hover展示tooltip，具体集群列表
                    NFS文件 table - 一键清空失败（存在卷已被删除，只是由于未及时同步依然显示在列表）
                    NFS文件 table - 弹窗ui：标题文案/内容文案/描述文案/submit btn
                一键清空时，单个集群中的待清理资源超过了阈值
                    全部资源 table - 一键清空（列表超长）
                    lun table - 一键清空（列表超长）
                    ns table - 一键清空（列表超长）
                    相同集群，发起一键清空 LUN 任务后，立刻发起一键清空 ns 或者一键清空所有资源任务时，该集群在回收站中的 lun 数量超过阈值时，后续任务都会失败（后端报错）
                    相同集群，发起一键清空 LUN 任务后，立刻发起一键清空 ns 或者一键清空所有资源任务时，该集群在回收站中的 lun 数量没有超过阈值时，后续任务都会成功
                    tower 中，发起一键清空 ns 任务后，在回收站的 LUN 列表发起一键清空 LUN 的任务，存在集群在回收站中均有 LUN 和 ns，且该集群在回收站中的 LUN 数量超过了阈值，该集群一键清空 LUN 任务失败
                    tower 中，发起一键清空 ns 任务后，在回收站的 LUN 列表发起一键清空 LUN 的任务，存在集群在回收站中均有 LUN 和 ns，且该集群在回收站中的 LUN 数量未超过阈值，该集群一键清空 LUN 任务成功
                    tower 中，发起一键清空 lun/ns 任务后，卷可以继续移入回收站，后续移入回收站的卷可以进行单个或批量的恢复和永久删除，仅删除发起一键清空任务时刻回收站的所有 lun/ns
                    tower 中，发起一键清空 lun/ns 任务后，在回收站的虚拟机列表，发起一键清空任务成功
                    cli 发起一键清空 lun 任务，该任务没有结束时，在 tower 上发起一键清空 ns 任务，存在 lun 和 ns 均在回收站中的集群则 tower 上的一键清空任务失败
                    tower 上发起一键清空任务时，同时存在待删除资源超出阈值和未超出阈值的集群，任务结束后，仅未超出阈值的集群生成的任务可以查看详情
                    tower 中，发起一键清空 NFS文件 任务后，卷可以继续移入回收站，后续移入回收站的卷可以进行单个或批量的恢复和永久删除，仅删除发起一键清空任务时刻回收站的所有 NFS文件
                    tower 中，发起一键清空OS（ELF）的 lun 任务后，在回收站的虚拟机列表，发起一键清空任务成功
                    tower 上发起NFS文件一键清空任务时，同时存在待删除资源超出阈值和未超出阈值的集群，任务结束后，仅未超出阈值的集群生成的任务可以查看详情
            全部资源对象（471）
                全部资源 table - UI 元素检查
                全部资源 table - 单个恢复
                全部资源 table - 单个永久删除
                全部资源 table - 批量恢复
                全部资源 table - 批量永久删除
            虚拟机
                虚拟机 table - UI 元素检查
                虚拟机 table - 单个恢复：新增常驻缓存说明：虚拟机将以关机状态恢复至原所属主机
                虚拟机 table - 单个恢复：新增常驻缓存说明：若原名称已被使用，恢复指定新名称
                虚拟机 table - 单个恢复：新增常驻缓存说明：新增重名校验：集群内的虚拟机不允许重名
                虚拟机 table - 单个永久删除
                虚拟机 table - 批量恢复
                虚拟机 table - 批量恢复：新增常驻缓存说明：虚拟机将以关机状态恢复至原所属主机
                虚拟机 table - 批量恢复：新增常驻缓存说明：若原名称已被使用，恢复指定新名称
                虚拟机 table - 批量恢复：新增常驻缓存说明：新增重名校验：集群内的虚拟机不允许重名
                虚拟机 table - 批量永久删除
            ZBS/OS（ELF）集群LUN
                lun table - UI 元素检查
                lun table - 单个恢复成功
                lun table - 单个恢复失败（name / id 被占用）
                lun table - 单个恢复失败（已被删除，未同步原因导致还显示）
                lun table - 单个永久删除成功
                lun table - 单个永久删除失败（已被删除，未同步原因导致还显示）
                lun table - 批量恢复成功
                lun table - 批量恢复失败（name / id 被占用）
                lun table - 批量恢复失败（卷已被删除，只是由于未及时同步导致显示在列表）
                lun table - 批量永久删除成功
                单个卷恢复，选择不同白名单配置的 target
            ZBS集群ns
                lun table - 批量永久删除失败（卷已被删除，同步原因导致依然显示）
                ns table - UI 元素检查
                ns table - 单个恢复成功
                ns table - 单个恢复失败（name / id 被占用）
                ns table - 单个恢复失败（恢复一个已经被删除的卷，只是由于未及时同步导致显示在列表）
                ns table - 单个永久删除成功
                ns table - 单个永久删除失败（卷已被删除，只是由于未及时同步依然显示在列表）
                ns table - 批量恢复成功
                ns table - 批量恢复失败（name / id 被占用）
                ns table - 批量恢复失败（包含已经被删除的卷，只是由于未及时同步导致显示在列表）
                ns table - 批量永久删除成功
                ns table - 批量永久删除失败（存在卷已被删除，只是由于未及时同步依然显示在列表）
                ns 为共享卷时的恢复
                单个卷恢复，选择不同白名单配置的 subsystem
            NFS文件
                左侧菜单：icon、NFS文件、可释放空间
                table标题：NFS文件，hover info icon：如需恢复回收站内的NFS文件，请联系售后提供支持。
                table字段 - 名称：默认展示，不支持交互，支持排序、支持筛选
                table字段 - 所属NFS文件夹：默认展示、支持交互，不支持排序，支持筛选：NFS export未被删除：hover变蓝，点击跳转至NFS 文件夹详情页
                table字段 - 所属NFS文件夹：默认展示、支持交互，不支持排序，支持筛选：NFS export被删除：hover展示tooltip 已删除
                table字段 - 所属NFS export：默认展示、支持交互，不支持排序，支持筛选：NFS export未被删除：hover变蓝，点击跳转至NFS export详情页
                table字段 - 所属NFS export：默认展示、支持交互，不支持排序，支持筛选：NFS export被删除：NFS export被删除：取值“已删除”
                table字段 - 所属集群：默认展示、支持交互、不支持排序、支持筛选：hover变蓝，点击跳转至所属集群概览
                table字段 - 所属数据中心：默认展示、支持交互、不支持排序、支持筛选：hover变蓝，点击跳转至所属DC概览
                table字段 - 可释放空间：默认展示、不支持交互、支持排序、支持筛选
                table字段 - 保留时间：默认展示，支持交互、不支持排序、不支持筛选（实际实现不支持筛选）
                table字段 - 保留时间：hover 显示tooltip ：将于 2025-09-09 12:12:12 自动永久删除
                table字段 - 保留时间 - 取值：24小时以上，向下取整
                table字段 - 保留时间 - 取值：24小时内，显示“不足1天”
                table字段 - 保留时间 - 取值：3天以下，标红
                table字段 - 移至回收站时间：默认不展示，不支持交互，支持排序，支持筛选
                table空白状态：回收站内无NFS文件
                可释放空间校验
                导出报表
                单个NFS文件详情 - NFS icon，只有永久删除btn
                单个NFS文件展示内容
                批量删除 - 弹窗ui
                单个永久删除 - 弹窗ui
                删除任务 - 文案：永久删除集群xx回收站内的N个资源对象，多个集群的批量删除任务会按照集群分别生成任务
                删除任务 -查看详情 - 任务执行中：永久删除详情/资源对象：icon、NFS文件名/进度：所有资源进度均为“删除中”
                删除任务 -查看详情 - 任务执行中：进度：已删除/删除失败
                其他系统服务使用NFS，默认不进入回收站
        设置-回收站规则 table
            新部署 tower 回收站默认启用，30 天
            升级 tower 不改变回收站状态。（tower 4.5 关闭回收站，升级至 4.7）
            升级 tower 不改变回收站状态。（tower 4.6 启用回收站，升级至 4.7）
            Tower 已关联 ZBS，全局为开启，无特例规则，为集群创建特例规则与全局规则一致，展示为特例规则，修改全局规则不影响特例规则
            Tower 4.5 开启回收站并关联 ZBS 5.6.0，升级 Tower 至 4.7 并升级 ZBS 至 5.7.0，最终会经过同步会自动为 ZBS 打开回收站，与全局一致。
            Tower 4.6 关闭回收站并关联 ZBS 5.6.0，升级 Tower 至 4.7 并升级 ZBS 至 5.7.0，最终同步后也不会创建特例规则。且两端均保持关闭。
            删除特例规则，集群回收站设置为 tower 的默认规则
            创建集群特例规则时，默认展示为 30 天
            编辑集群特例规则，由关闭回收站到开启回收站，保留时间默认展示为 30 天
            编辑特例规则，保留天数设置为 1 天，保留天数已大于 1 天的卷将在 30min 内被永久删除
            tower 480：规则页 info icon文案修改
            Tower 已关联 OS（VMware ESXi），全局为开启，无特例规则，为集群创建特例规则与全局规则一致，展示为特例规则，修改全局规则不影响特例规则
            Tower 4.5 开启回收站并关联 OS（VMware ESXi） 620，升级 Tower 至 4.7 并升级 OS（VMware ESXi） 至 630，最终会经过同步会自动为 OS（VMware ESXi） 打开回收站，与全局一致。
            Tower 4.6 关闭回收站并关联 OS（VMware ESXi） 620，升级 Tower 至 4.7 并升级 OS（VMware ESXi） 至 630，最终同步后也不会创建特例规则。且两端均保持关闭。
            ELF集群回收站设置与ZBS集群回收站设置分开管理
            集群首次关联 tower
                新部署 tower + 新部署 zbs 5.7.0，关联集群后自动为 zbs 集群设置为与全局一致
                Tower 开 ZBS 开，关联后两边不一致时同步之后创建特例规则，修改全局规则为与 zbs 集群规则一致，该集群的特例规则仍存在
                Tower 关 ZBS 开，关联后为集群创建特例规则，tower 不变
                Tower 关 ZBS 关，关联集群后无特例规则，两侧回收站均保持关闭
                Tower 开 ZBS 关，关联后，会根据全局规则为集群打开回收站，不会创建特例规则。
                tower 开 ZBS 开，关联后两边不一致时同步之后创建特例规则，以 ZBS 侧为准
                tower 开 ZBS 开，关联后两边一致时同步之后不会创建特例规则，集群会跟随全局。
                Tower 关 ZBS 开，关联后为集群创建特例规则，tower 不变
                tower 关闭回收站，zbs 集群设置回收站保留时间为 10 天之后关闭回收站，tower 关联该 zbs 集群，默认不创建特例规则
                tower 关闭回收站，zbs 集群设置回收站保留时间为 10 天之后关闭回收站，tower 关联该 zbs 集群，启用全局回收站，并设置保留时间为 20 天，zbs 集群回收站同步更改，不会自动创建特例规则
            集群再次关联同一个 tower
                首次关联 tower 创建了特例规则，不修改 tower 和集群配置，再次关联展示与之前一致
                首次关联 tower 创建了特例规则，仅修改 tower 全局规则，再次关联集群仍为之前的特例规则
                首次关联 tower 创建了特例规则，仅 cli 修改集群回收站配置，再次关联展示为特例规则，且为修改后的设置
                首次关联 tower 未创建特例规则，再次关联与首次关联行为一致
            cli 编辑回收站规则
                Tower 已关联 ZBS，且全局为开启，不存在特例规则，当前回收站有卷，通过 cli disable，预期可能会有卷被删除，但最终 Tower 会根据全局开启 ZBS 回收站。
                Tower 已关联 ZBS，且全局为开启，不存在特例规则，通过 cli 修改保留时间（缩短或延长），超出保留时间的卷被删除，最终 Tower 生成特例规则，并展示为后端设置。
                Tower 已关联 ZBS，且全局为开启，存在特例规则，通过 cli 修改保留时间（缩短或延长），超出保留时间的卷被删除，最终 Tower 展示为后端设置。
                Tower 已关联 ZBS，且全局为开启，存在特例规则为开启，当前回收站有卷，通过 cli disable，预期可能会有卷被删除，但最终 Tower 会根据特例规则开启 ZBS 回收站。
                Tower 已关联 ZBS，且全局为开启，存在特例规则为关闭，通过 cli enable，预期最终 Tower 会同步到 ZBS 配置并同步修改特例规则。
                Tower 已关联 ZBS，且全局为关闭，不存在特例规则，通过 cli enable，预期最终 Tower 会同步到 ZBS 配置并自动创建特例规则。
                Tower 已关联 ZBS，且全局为关闭，存在特例规则为开启，当前回收站有卷，通过 cli disable，预期可能会有卷被删除，但最终 Tower 会根据特例规则开启 ZBS 回收站。
                Tower 已关联 ZBS，且全局为关闭，存在特例规则，通过 cli 修改保留时间（缩短或延长），超出保留时间的卷被删除，最终 Tower 展示为后端设置。
                Tower 已关联 ZBS，且全局为关闭，存在特例规则为关闭，通过 cli enable，预期最终 Tower 会同步到 ZBS 配置并同步修改特例规则。
                Tower 已关联 ZBS，无特例规则，ZBS 跟随全局且全局为开，重启 zbs 服务不会出现误删除卷。
                tower 已关联 zbs，zbs 跟随全局且全局为关，cli 编辑 zbs 回收站保留时间为 5 天，前端不会为该集群创建特例规则
            OS（VMware ESXi）集群
                新部署集群：未关联tower，zbs回收站默认关闭
                新部署集群 - 未关联tower，手动设置zbs开启回收站设置，再关联tower：tower根据zbs回收站创建特例规则
                新部署集群 - 关联tower，zbs回收站随tower默认规则设置，无特例规则：tower关闭回收站，则zbs关闭回收站
                新部署集群 - 关联tower，zbs回收站随tower默认规则设置，无特例规则：tower打开回收站，则zbs打开回收站且配置与tower一致
                升级集群 - 未关联tower，zbs默认关闭回收站
                升级集群 - 关联了tower，tower 开启回收站，则zbs回收站规则被tower更新为开启，且与tower规则保持一致，无特例规则
                升级集群 - 关联了tower：tower关闭回收站，zbs保持关闭
                升级集群 - 手动给zbs设置规则，再关联tower：tower创建一条特例规则
                tower修改回收站规则场景 - 回收站设置从关闭设置为开启：VC操作删除磁盘或者虚拟机，对应NFS文件移入回收站，保留天数与规则一致，可永久删除NFS文件
                tower修改回收站规则场景 - 回收站设置从开启设置为关闭：回收站内的NFS会自动清理，VC操作删除磁盘或者虚拟机，对应NFS文件永久删除
                tower修改回收站规则场景 - 保留天数调大：回收站中的NFS文件保留天数更新，新加入回收站的NFS文件保留天数按新规则
                tower修改回收站规则场景 - 保留天数调小：存在资源保留天数超过当前回收站规则，自动清理，保留天数未超过当前回收站规则，更新NFS文件保留天数
                cli 编辑回收站规则
                    Tower 已关联 OS（VMware ESXi），且全局为开启，不存在特例规则，当前回收站有卷，通过 cli disable，预期可能会有卷被删除，但最终 Tower 会根据全局开启 ZBS 回收站。
                    Tower 已关联 OS（VMware ESXi），且全局为开启，不存在特例规则，通过 cli 修改保留时间（缩短或延长），超出保留时间的卷被删除，最终 Tower 生成特例规则，并展示为后端设置。
                    Tower 已关联 OS（VMware ESXi），且全局为开启，存在特例规则，通过 cli 修改保留时间（缩短或延长），超出保留时间的卷被删除，最终 Tower 展示为后端设置。
                    Tower 已关联 OS（VMware ESXi），且全局为开启，存在特例规则为开启，当前回收站有卷，通过 cli disable，预期可能会有卷被删除，但最终 Tower 会根据特例规则开启 ZBS 回收站。
                    Tower 已关联 OS（VMware ESXi），且全局为开启，存在特例规则为关闭，通过 cli enable，预期最终 Tower 会同步到 ZBS 配置并同步修改特例规则。
                    Tower 已关联 OS（VMware ESXi），且全局为关闭，不存在特例规则，通过 cli enable，预期最终 Tower 会同步到 ZBS 配置并自动创建特例规则。
                    Tower 已关联 OS（VMware ESXi），且全局为关闭，存在特例规则为开启，当前回收站有卷，通过 cli disable，预期可能会有卷被删除，但最终 Tower 会根据特例规则开启 ZBS 回收站。
                    Tower 已关联 OS（VMware ESXi），且全局为关闭，存在特例规则，通过 cli 修改保留时间（缩短或延长），超出保留时间的卷被删除，最终 Tower 展示为后端设置。
                    Tower 已关联 OS（VMware ESXi），且全局为关闭，存在特例规则为关闭，通过 cli enable，预期最终 Tower 会同步到 ZBS 配置并同步修改特例规则。
                    Tower 已关联 OS（VMware ESXi），无特例规则，ZBS 跟随全局且全局为开，重启 zbs 服务不会出现误删除卷。
                    tower 已关联 OS（VMware ESXi），OS（VMware ESXi） 跟随全局且全局为关，cli 编辑 zbs 回收站保留时间为 5 天，前端不会为该集群创建特例规则
            OS（ELF）
                新部署集群 - 未关联tower：默认VM回收站none，zbs回收站关闭
                新部署集群 - 关联tower：vm回收站与zbs回收站被设置成tower默认规则
                新部署集群 - 手动设置zbs回收站后，关联tower：tower回收站关闭，根据zbs回收站配置创建开启回收站的特例规则
                新部署集群 - 手动设置zbs回收站后，关联tower：tower回收站开启，zbs回收站规则与tower一致，则无变化，不创建特例规则
                新部署集群 - 手动设置zbs回收站后，关联tower：tower回收站开启，zbs回收站规则与tower不一致，则创建特例规则
                升级集群 - 未关联tower：zbs回收站保持关闭
                升级集群 - 已关联tower：根据vm的回收站规则设置zbs回收站
                手动设置zbs回收站 - zbs手动开启，且规则与tower一致，关联tower：zbs无变化，无特例规则
                手动设置zbs回收站 - zbs手动开启，tower关闭，关联tower：zbs无变化，tower添加一条开启的特例规则，适用于vm&zbs
                手动设置zbs回收站 -zbs手动开启，tower开启，但是天数不一致，关联tower：zbs无变化，tower添加一条开启的特例规则，适用于vm&zbs
        回收站外：存储卷 table
            lun table
                开启回收站
                    lun 被 smtx elf 使用，不允许移至回收站
                    复制计划创建的副本资源，不允许移至回收站
                    lun 属于一致性组，不允许移至回收站
                    lun 属于快照计划，不允许移至回收站
                    lun 白名单为指定 iqn / 指定业务主机 / 白名单与所属 target 一致，不允许移至回收站
                    lun 白名单为全部允许，但所属 target 白名单为指定 IP 或指定 IQN，不允许移至回收站
                    单个移至回收站 - 不包含快照
                    单个移至回收站(包含快照)-选择同时删除快照
                    单个移至回收站(包含快照)-选择保留快照，如果之后恢复该 lun，那么快照属于 target 而不是该 lun
                    批量移至回收站 - 不包含快照
                    批量移至回收站(包含快照)-选择同时删除快照
                    批量移至回收站(包含快照)-选择保留快照，如果之后恢复 lun，那么快照属于 target 而不是 lun
                    批量移至回收站，有资源筛查（存在 lun 不可被移至回收站）
                未开启回收站
                    lun 被 smtx elf 使用，不允许永久删除
                    复制计划创建的副本资源，不允许永久删除
                    lun 属于一致性组，不允许永久删除
                    lun 属于快照计划，不允许永久删除
                    lun 白名单为指定 iqn / 指定业务主机 / 白名单与所属 target 一致，不允许永久删除
                    lun 白名单为全部允许，但所属 target 白名单为指定 IP 或指定 IQN，不允许永久删除
                    单个永久删除 - 不包含快照
                    单个永久删除(包含快照)-选择同时删除快照
                    单个永久删除(包含快照)-选择保留快照，快照属于 target
                    批量永久删除 - 不包含快照
                    批量永久删除(包含快照)-选择同时删除快照
                    批量永久删除(包含快照)-选择保留快照，快照属于 target
                    批量永久删除，有资源筛查（存在 lun 不可被永久删除），只要存在不可被删除的 lun 就无法触发任务
            ns table
                开启回收站
                    ns 属于一致性组，不允许移至回收站
                    ns 属于快照计划，不允许移至回收站
                    ns 白名单为指定 nqn / 指定业务主机 / 白名单与所属 subsystem 一致，不允许移至回收站
                    单个移至回收站 - 不包含快照
                    单个移至回收站(包含快照)-选择同时删除快照
                    单个移至回收站(包含快照)-选择保留快照，如果之后恢复该 ns，那么快照属于 subsystem 而不是该 ns
                    批量移至回收站 - 不包含快照
                    批量移至回收站(包含快照)-选择同时删除快照
                    批量移至回收站(包含快照)-选择保留快照，如果之后恢复 ns，那么快照属于 subsystem 而不是 ns
                    批量移至回收站，有资源筛查（存在 ns 不可被移至回收站）
                未开启回收站
                    ns 属于一致性组，不允许永久删除
                    ns 属于快照计划，不允许永久删除
                    ns 白名单为指定 nqn / 指定业务主机 / 白名单与所属 subsystem 一致，不允许永久删除
                    单个永久删除 - 不包含快照
                    单个永久删除(包含快照)-选择同时删除快照
                    单个永久删除(包含快照)-选择保留快照，快照属于 subsystem
                    批量永久删除 - 不包含快照
                    批量永久删除(包含快照)-选择同时删除快照
                    批量永久删除(包含快照)-选择保留快照，快照属于 subsystem
                    批量永久删除，有资源筛查（存在 ns 不可被永久删除），只要存在不可被删除的 ns 就无法触发任务
            NFS文件
                tower上无法操作NFS文件删除
                开启回收站
                    系统服务使用的NFS文件不会进入回收站，默认直接删除
                    在VC中删除磁盘 - 确认tower回收站同步到对应NFS文件：文件夹未删除，export未删除
                    在VC中删除虚拟机 - 确认tower回收站同步到对应NFS文件：文件夹已删除，export未删除
                    通过cli恢复NFS文件 - 在VC中可重新挂载磁盘：磁盘md5与删除前一致，且io正常
                    通过cli恢复NFS文件 - 在VC中重新恢复虚拟机： 虚拟机正常运行，io正常
                    NFS文件过期自动清理 - tower回收站无过期NFS文件，空间回收正常
                未开启回收站
                    在VC中删除磁盘，确认集群对应NFS文件被删除，回收站为空，空间回收完成
                    在VC中删除虚拟机，确认集群对应NFS文件被删除，回收站为空，空间回收完成
        回收站外：其他
            vm table
                EFL集群虚拟机 - 待删除的虚拟机所属集群：620版本的EFL+570 ZBS（启用回收站）
                ELF集群虚拟机 - 待删除的虚拟机所属集群：EFL集群部分低于630，部分为630+570
                ELF集群虚拟机 -待删除的虚拟机所属集群：630版本的ELF + 570 ZBS
                开启回收站
                    SMTX OS（ELF）集群
                    SMTX ELF 集群
                未开启回收站
                    SMTX OS（ELF）集群
                    SMTX ELF 集群
            虚拟卷 table
                EFL集群虚拟机 - 待删除的虚拟卷所属集群：620版本的EFL+570 ZBS（启用回收站）
                ELF集群虚拟机 - 待删除的虚拟卷所属集群：EFL集群部分低于630，部分为630+570
                ELF集群虚拟机 -待删除的虚拟卷所属集群：630版本的ELF + 570 ZBS
                开启回收站
                    SMTX OS（ELF）集群
                    SMTX ELF 集群
                未开启回收站
                    SMTX OS（ELF）集群
                    SMTX ELF 集群
            内容库 table
                开启回收站
                    SMTX OS（ELF）集群
                    SMTX ELF 集群
                未开启回收站
                    SMTX OS（ELF）集群
                    SMTX ELF 集群
        事件与任务
            恢复回收站内的卷成功会触发「回收站内卷被恢复」事件
            将卷「移至回收站」事件
            将卷「永久删除」事件
            回收站中创建集群特例规则
            回收站中编辑集群特例规则
            回收站中删除集群特例规则
            回收站中编辑回收站默认规则/开启/关闭全局回收站
        报表导出
            回收站相关 table 的报表导出
        权限管理
            回收站相关操作（比如 lun / ns 等资源）的用户权限
            回收站- NFS文件相关操作的用户权限
    ZBS CLI
        所有涉及删除卷资源的命令均添加 --delete_permanently 选项
            lun
            ns
            inode
            export
        回收站新增命令行
            zbs-meta recycle_bin enable
            zbs-meta recycle_bin disable
            zbs-meta recycle_bin update_default_expired_hours
            zbs-meta recycle_bin show_pool
            zbs-meta recycle_bin show_config
            zbs-meta recycle_bin show_usage
            zbs-meta recycle_bin sweep_immediate
            zbs-meta recycle_bin show_volume
            zbs-meta recycle_bin list_volumes
            zbs-meta recycle_bin list_snapshots
            zbs-meta recycle_bin restore_volume_to_lun
            zbs-meta recycle_bin restore_volume_to_ns
            zbs-meta recycle_bin restore_volume_to_file
            zbs-meta recycle_bin restore_snapshot
            zbs-meta recycle_bin restore_volume
            zbs-meta recycle_bin batch_sweep_volumes
            zbs-meta cluster show 查询集群回收站
            zbs-meta cluster update --enable_recycle_bin
            zbs-meta cluster update --default_vol_expired_hours
    回收站特性
        卷被移至回收站后会立即释放 name/id，因此相关 cli 均不可用
    metric 测试
        zbs_cluster_recycle_bin_logical_size_bytes
        zbs_cluster_recycle_bin_logical_used_size_bytes
        zbs_cluster_recycle_bin_sweep_size_bytes_until_today_end
        zbs_cluster_recycle_bin_sweep_size_bytes_in_3_days
        zbs_cluster_recycle_bin_sweep_size_bytes_after_30_days
        zbs_cluster_recycle_bin_sweep_size_bytes_in_7_days
        zbs_cluster_recycle_bin_sweep_size_bytes_in_30_days
    运维操作
        ZBS 5.7.0 集群卸载系统服务，系统 vm 会进入回收站
        OS 6.3.0 集群卸载系统服务，系统 vm 会进回收站
        Tower 已关联集群，且集群未开启回收站，添加节点，不影响回收站状态
        Tower 已关联集群，且集群已启用回收站，添加节点，不影响回收站状态
        集群升级前创建 zbs-trash-pool，升级到 zbs 570，回收站对应的 zbs-trash-pool 创建成功，移入回收站成功且展示正确
    快照计划与回收站
        lun 快照计划
            原所属 target 中该卷 id 被占用/未被占用，执行快照计划失败
            允许永久删除该 lun。
            不改变配置恢复该 lun，tower 中 lun 属于原快照计划，执行快照计划成功。但 lun 原有快照不属于 lun 了，而是 target
            仅指定 lun name 恢复该 lun，tower 中 lun 属于原快照计划，「快照对象」列表同步更改，执行快照计划成功。但 lun 原有快照不属于 lun 了，而是 target
            仅指定 lun id 恢复该 lun，tower 中 lun 属于原快照计划，「快照对象」列表同步更改，执行快照计划失败。lun 原有快照不属于 lun 了，而是 target
            指定 lun name 和 lun id 恢复该 lun（原 target 中存在同时占用了该 lun name 和 id 的 lun），tower 中 lun 属于原快照计划，「快照对象」列表同步更改，执行快照计划失败。lun 原有快照不属于 lun 了，而是 target
            指定新 target 恢复该 lun，tower 中 lun 属于原快照计划，「快照对象」列表同步更改，执行快照计划失败
            指定新 target 和 lun id（与原 lun id 相同/不同）恢复该 lun，tower 中 lun 属于原快照计划，「快照对象」列表同步更改，执行快照计划失败
            编辑快照计划后，不改变配置恢复该卷，tower 中该卷不属于原快照计划
        ns 快照计划
            原所属 subsystem 中该卷 id 被占用/未被占用，执行快照计划失败
            允许永久删除该 ns
            不改变配置恢复该 ns，tower 中 ns 属于原快照计划，执行快照计划成功。但 ns 原有快照不属于 ns 了，而是 subsystem
            仅指定 ns name 恢复该 ns，tower 中 ns 属于原快照计划，「快照对象」列表同步更改，执行快照计划成功。但 ns 原有快照不属于 ns 了，而是 subsystem
            仅指定 ns id 恢复该 ns，tower 中 ns 属于原快照计划，「快照对象」列表同步更改，执行快照计划失败。ns 原有快照不属于 ns 了，而是 subsystem
            指定 ns name 和 ns id 恢复该 ns（原 subsystem 中存在同时占用了该 ns name 和 id 的 ns），tower 中 ns 属于原快照计划，「快照对象」列表同步更改，执行快照计划失败。ns 原有快照不属于 ns 了，而是 subsystem
            指定新 subsystem 恢复该 ns，tower 中 ns 属于原快照计划，「快照对象」列表同步更改，执行快照计划失败
            指定新 subsystem 和 ns id（与原 ns id 相同/不同）恢复该 ns，tower 中 ns 属于原快照计划，「快照对象」列表同步更改，执行快照计划失败
    空间检查
        将卷移至回收站，检查集群分配空间，不会释放。
        将卷从回收站恢复，检查集群分配空间，无变化。
        将卷从回收站永久删除，检查集群分配空间，正常释放。
        检查 zbs-meta cluster summary 的 recycle_bin_size_info
        将 ZBS 解除关联后，回收站中的卷会被删除，检查空间。
    Tower 同步检查
        开启回收站，zbs 通过 cli 将卷移至回收站，预期 tower 最终可以同步。（tower 回收站资源 1h 同步一次）
        开启回收站，zbs 通过 cli 清理回收站资源，预期 tower 最终可以同步。（tower 回收站资源 1h 同步一次）
        集群同时关联不同 tower，在 tower A 操作恢复 / 删除，预期 2 个 tower 的回收站资源最终均可同步到。
        集群同时关联不同 tower（tower 全局默认规则均为开），均无特例规则，在 tower A 创建 ZBS 集群的特例规则为关，tower B 应该还是会根据全局默认规则配置 ZBS，导致回收站为 enable？
zbs-5.7.0 安装部署运维
    安装部署
        目标版本
            smtxzbs-5.7.0 支持多实例部署
            smtxos-6.3.0 支持多实例部署
            SMTX ELF 6.2.0 及以上，搭配 SMTX ZBS 5.7.0 使用可以利用到 Chunk 多实例带来的性能优势，SMTX ELF 本身无需调整
            多实例适配 tower-4.7
            intel 支持多实例
            hygon 支持多实例
            arm 支持多实例
            支持双活开启多实例
            支持非双活开启 多实例
            多实例支持 RDMA & Boost & NVMF, 且验证各类网络的 bond 模式
        产品架构
            部署集群或者添加节点时可选择实例数量
            不同硬盘池必须为相同的分层模式
            集群部署后不支持修改节点的硬盘池数量
            磁盘池数量上限为 255（qa 覆盖 12*4 即可）
            单硬盘池数据分区容量上限为 256TiB，缓存分区总容量上限为 51TiB
            同一集群允许不同的系统盘部署方式（软 RAID 1 or 独立硬 RAID 1）
            支持融合部署，管理网和存储网融合
            支持融合部署，管理网和接入网融合
            支持融合部署，存储网和接入网融合
            配置静态路由
        集群部署
            Normal
                规格
                    单 CPU 最小物理核心数 8 ，总逻辑核心数量(HT 之后) ≥ 32
                    CPU 内每个 NUMA Node 包含的物理核心数 ≤ 6，推荐 ≥ 8
                    内存最小 128G
                    查看 /etc/zbs/node_zbs_spec 为 Normal
                    系统分区空间消耗符合预期
                    若缓存分区总容量超出容量规格 * 20%，需按照缓存分区总容量计算要预留的内存
                分层
                    混闪配置或多种类型 SSD 全闪配置时，单节点限制
                    单一类型 SSD 全闪配置时，单节点限制
                    OS 安装在独立的硬 RAID1
                        混闪配置
                        多种类型 SSD
                        单一 SSD, 缓存盘和数据盘共享（默认）
                        单一 SSD, 缓存盘和数据盘独占（如果有一块缓存盘）
                    OS 安装在软 RAID1
                        混闪配置
                        多种类型 SSD
                        单一 SSD，缓存盘和数据盘共享（默认）
                        单一 SSD，缓存盘和数据盘独占（可选）
                不分层
                    单节点数据空间容量最大 128TiB，缓存 26TiB
                    数据盘和系统盘总数量不可超过 32
                    OS 安装在独立的硬 RAID1
                        OS 安装在独立的硬 RAID 1
                    OS 安装在软 RAID1
                        OS 安装在软 RAID 1
            Large
                规格
                    单 CPU 最小物理核心数 12 ，总逻辑核心 （HT 之后） >=48
                    CPU 内每个 NUMA Node 包含的物理核心数  >=8, 推荐 >=12
                    单实例，CPU 内每个 NUMA Node 包含的物理核心数  = 8，不开启 zbs/iscsi
                    单实例，CPU 内每个 NUMA Node 包含的物理核心数 =10，开启 zbs/iscsi
                    2个实例，开启 zbs/iscs，占用 23 核
                    最小内存 256G
                    查看 /etc/zbs/node_zbs_spec 为 Large
                分层
                    OS 安装在独立的硬 RAID1
                        1 实例
                            混闪配置
                            多种类型 SSD
                            单一 SSD, 缓存盘和数据盘共享（默认）
                            单一 SSD, 缓存盘和数据盘独占（如果有一块缓存盘）
                        2 实例
                            混闪配置
                            多种类型 SSD
                            单一 SSD, 缓存盘和数据盘共享（默认）
                            单一 SSD, 缓存盘和数据盘独占（如果有一块缓存盘）
                        规格
                            缓存盘和数据盘共享
                            缓存盘和数据盘独占
                    OS 安装在软 RAID1
                        1 实例
                            混闪配置
                            多种类型 SSD 全闪配置
                            单一 SSD，缓存盘和数据盘共享（默认）
                            单一 SSD，缓存盘和数据盘独占
                        2 实例
                            混闪配置
                            多种类型 SSD 全闪配置
                            单一 SSD，缓存盘和数据盘共享（默认）
                            单一 SSD，缓存盘和数据盘独占
                        规格
                            缓存盘和数据盘共享
                            缓存盘和数据盘独占
                不分层
                    OS 安装在独立硬 RAID1
                        1 实例
                            OS 安装在独立的硬 RAID1
                        2 实例
                            OS 安装在独立的硬 RAID1
                        规格
                            缓存盘和数据盘共享
                            缓存盘和数据盘独占
                    OS 安装在软 RAID1
                        1 实例
                            OS 安装在软 RAID 1
                        2 实例
                            OS 安装在软 RAID 1
                        规格
                            缓存盘和数据盘共享
                            缓存盘和数据盘独占
            xLarge
                规格
                    单 CPU 最小物理核心数 16 ，总逻辑核心 （HT 之后） >=64
                    CPU 内每个 NUMA Node 包含的物理核心数 >=8，推荐 >=18
                    单实例，CPU 内每个 NUMA Node 包含的物理核心数 <10，不开启 zbs/iscs
                    单实例，CPU 内每个 NUMA Node 包含的物理核心数 >=10，开启 zbs/iscs
                    2 个实例，开启 zbs/iscsi
                    4 个实例，开启 zbs/iscsi
                    内存要求最小 256GB
                    查看 /etc/zbs/node_zbs_spec 为 xLarge
                存储分层
                    OS 安装在独立的硬 RAID1
                        1 实例
                            混闪配置
                            多种类型 SSD
                            单一 SSD, 缓存盘和数据盘共享（默认）
                            单一 SSD, 缓存盘和数据盘独占（如果有一块缓存盘）
                        2 实例
                            混闪配置
                            多种类型 SSD
                            单一 SSD, 缓存盘和数据盘共享（默认）
                            单一 SSD, 缓存盘和数据盘独占（如果有一块缓存盘）
                        4 实例
                            混闪配置
                            多种类型 SSD
                            单一 SSD, 缓存盘和数据盘共享（默认）
                            单一 SSD, 缓存盘和数据盘独占（如果有一块缓存盘）
                        规格
                            缓存盘和数据盘共享
                            缓存盘和数据盘独占
                    OS 安装在软 RAID1
                        1 实例
                            混闪配置
                            多种类型 SSD
                            单一 SSD，缓存盘和数据盘共享（默认）
                            单一 SSD，缓存盘和数据盘独占
                        2 实例
                            混闪配置
                            多种类型 SSD
                            单一 SSD，缓存盘和数据盘共享（默认）
                            单一 SSD，缓存盘和数据盘独占
                        4 实例
                            混闪配置
                            多种类型 SSD
                            单一 SSD，缓存盘和数据盘共享（默认）
                            单一 SSD，缓存盘和数据盘独占
                        规格
                            缓存盘和数据盘共享
                            缓存盘和数据盘独占
                存储不分层
                    OS 安装在独立硬 RAID1
                        1 实例
                            OS 安装在独立的硬 RAID1
                        2 实例
                            OS 安装在独立的硬 RAID1
                        4 实例
                            OS 安装在独立的硬 RAID1
                        规格
                            缓存盘和数据盘共享
                            缓存盘和数据盘独占
                    OS 安装在软RAID1
                        1 实例
                            OS 安装在软 RAID 1
                        2 实例
                            OS 安装在软 RAID 1
                        4 实例
                            OS 安装在软 RAID 1
                        规格
                            缓存盘和数据盘共享
                            缓存盘和数据盘独占
    运维
        Normal
            分层
                OS 安装在独立硬 RAID 1
                    混闪配置
                        节点运维
                            节点添加
                                OS 安装在独立的硬 RAID1，混闪节点（分层）
                                OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                                OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                OS 安装在软 RAID1，混闪节点（分层）
                                OS 安装在软 RAID1，多种 SSD 节点（分层）
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            主机强制关机/重启
                                提交关机前的提示 —— 原校验
                                提交关机前的提示 —— 新校验
                                提交关机失败后的提示 —— 原提示
                                提交关机失败后的提示 —— 新提示
                                提交重启前的提示 —— 原校验
                                提交重启前的提示 —— 新校验
                                提交重启失败后的提示 —— 原提示
                                提交重启失败后的提示 —— 新提示
                            角色转换
                                存储节点转为主节点
                                主节点转为存储节点
                            维护模式
                                原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                            节点移除
                                移除处于健康状态的主机
                                移除处于维护模式的主机
                                移除处于无响应状态的主机
                                移除当前主机后，集群中 chunk 服务健康且非移除中的主机是不满足纠删码卷的要求，预期移除检查不通过
                                集群中主节点数量不否满足要求
                                集群中其他主机的 chunk 实例处于 idle 状态
                                集群中其他主机的空闲 perf 存储空间是否充足
                                集群中其他主机的空闲 pin 存储空间是否充足
                                集群中其他主机的空闲 cap 存储空间是否充足
                                集群中存在正在添加的主机，等待主机完成当前进行中的任务
                                集群中存在正在进入维护模式的主机，等待主机完成当前进行中的任务
                                集群中存在处于维护模式的其他主机，先完成其维护任务、并退出维护模式
                                集群中存在正在移除或移除失败的其他主机，先完成其移除主机任务
                                集群中存在正在转换角色或转换失败的主机，先完成其角色转换任务
                                集群中存在数据恢复，等待数据恢复完成
                                集群不处于升级中状态
                                双活集群
                        磁盘运维
                            添加
                                磁盘推荐 —— NVMe SSD，SATA/SAS SSD，默认推荐为缓存盘，可选为数据盘
                                磁盘推荐 —— HDD，数据盘
                                节点数据分区容量上限 128TiB，缓存分区总容量上限 26TiB
                            卸载
                                预检查 —— 不能有待恢复数据
                                预检查 —— 不能有 dead extent
                                预检查 —— 物理盘卸载空间校验
                                原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                数据迁移
                                不支持卸载系统盘
                            异常处理
                                磁盘掉线，告警信息描述节点和chunk信息
                                分区故障，告警信息描述节点和chunk信息
                                物理盘隔离
                        集群升级
                            SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                            OS 安装在软 RAID1—全闪分层
                            OS 安装在软 RAID1—混闪分层
                            OS 安装在的软 RAID1—不分层
                            OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                            zbs-5.2.0 升级到 zbs-5.7.0
                            zbs-5.4.1 升级到 zbs-5.7.0
                            zbs-5.6.2 升级到 zbs-5.7.0
                            升级内核
                            不升级内核
                            部署 sfs 之后内核升级
                            升级前准备
                            升级后检查
                            升级后检查并开启 RDMA
                            升级后检查 DSA 硬件加速
                    多种 SSD
                        节点运维
                            节点添加
                                OS 安装在独立的硬 RAID1，混闪节点（分层）
                                OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                                OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                OS 安装在软 RAID1，混闪节点（分层）
                                OS 安装在软 RAID1，多种 SSD 节点（分层）
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                        磁盘运维
                            添加
                                磁盘推荐 —— NVMe SSD，默认推荐为缓存盘，可选为数据盘
                                磁盘推荐 —— SATA/SAS SSD，默认为数据盘，可选为缓存盘
                                磁盘推荐 —— HDD, 数据盘（优先级低）
                                节点数据分区容量上限 128TiB，缓存分区总容量上限 26TiB
                    单一 SSD（缓存盘和数据盘独立部署 or 共享磁盘）
                        节点运维
                            节点添加
                                OS 安装在独立的硬 RAID1，混闪节点（分层），检查不通过
                                OS 安装在独立的硬 RAID1，多种 SSD 节点（分层），检查不通过
                                OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                OS 安装在软 RAID1，混闪节点（分层），检查不通过
                                OS 安装在软 RAID1，多种 SSD 节点（分层），检查不通过
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            节点移除
                                移除处于健康状态的主机
                        磁盘运维
                            添加
                                磁盘推荐 ——  集群全为 NVME SSD，添加 NVME SSD 为数据盘
                                磁盘推荐 —— HDD，不允许挂载
                                磁盘推荐 ——  集群全为 NVME SSD，添加 SATA/SAS SSD, 可挂载为数据盘
                                节点数据分区容量上限 128TiB，缓存分区总容量上限 26TiB
                            卸载
                                预检查 —— 不能有待恢复数据
                                预检查 —— 不能有 dead extent
                                预检查 —— 物理盘卸载空间校验
                                原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                数据迁移
                                不支持卸载系统盘
                            异常处理
                                磁盘掉线，告警信息描述节点和chunk信息
                                分区故障，告警信息描述节点和chunk信息
                                物理盘隔离
                        集群升级
                            SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                            OS 安装在软 RAID1—全闪分层
                            OS 安装在软 RAID1—混闪分层
                            OS 安装在的软 RAID1—不分层
                            OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                            zbs-5.2.0 升级到 zbs-5.7.0
                            zbs-5.4.1 升级到 zbs-5.7.0
                            zbs-5.6.2 升级到 zbs-5.7.0
                            升级内核
                            不升级内核
                            部署 sfs 之后内核升级
                            升级前准备
                            升级后检查
                            升级后检查并开启 RDMA
                            升级后检查 DSA 硬件加速
                OS 安装在软 RAID 1
                    混闪配置
                        节点运维
                            节点添加
                                OS 安装在独立的硬 RAID1，混闪节点（分层）
                                OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                                OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                OS 安装在软 RAID1，混闪节点（分层）
                                OS 安装在软 RAID1，多种 SSD 节点（分层）
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            角色转换
                                存储节点转为主节点
                                主节点转为存储节点
                            维护模式
                                原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                            节点移除
                                移除处于健康状态的主机
                        磁盘运维
                            添加
                                磁盘推荐 —— SSD
                                磁盘推荐 —— HDD
                                节点数据分区容量上限 128TiB，缓存分区总容量上限 26TiB
                            卸载
                                数据盘卸载
                                缓存盘卸载
                                系统盘卸载
                            异常处理
                                磁盘掉线，告警信息描述节点信息
                                分区故障，告警信息描述节点信息
                                物理盘隔离
                        集群升级
                            SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                            OS 安装在软 RAID1—全闪分层
                            OS 安装在软 RAID1—混闪分层
                            OS 安装在的软 RAID1—不分层
                            OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                            zbs-5.2.0 升级到 zbs-5.7.0
                            zbs-5.4.1 升级到 zbs-5.7.0
                            zbs-5.6.2 升级到 zbs-5.7.0
                            升级内核
                            不升级内核
                            部署 sfs 之后内核升级
                            升级前准备
                            升级后检查
                            升级后检查并开启 vhost
                            升级后检查 DSA 硬件加速
                    多种类型 SSD
                        节点运维
                            节点添加
                                OS 安装在独立的硬 RAID1，混闪节点（分层）
                                OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                                OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                OS 安装在软 RAID1，混闪节点（分层）
                                OS 安装在软 RAID1，多种 SSD 节点（分层）
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            主机强制关机/重启
                                主节点
                                存储节点
                            节点移除
                                移除处于健康状态的主机
                        磁盘运维
                            添加
                                磁盘推荐 —— NVMe SSD
                                磁盘推荐 —— SATA/SAS SSD
                                磁盘推荐 —— HDD
                            卸载
                                预检查 —— 不能有待恢复数据
                                预检查 —— 不能有 dead extent
                                预检查 —— 物理盘卸载空间校验
                                原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                数据迁移
                            异常处理
                                磁盘掉线，告警信息描述节点信息
                                分区故障，告警信息描述节点信息
                                物理盘隔离
                        集群升级
                            SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                            OS 安装在软 RAID1—全闪分层
                            OS 安装在软 RAID1—混闪分层
                            OS 安装在的软 RAID1—不分层
                            OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                            zbs-5.2.0 升级到 zbs-5.7.0
                            zbs-5.4.1 升级到 zbs-5.7.0
                            zbs-5.6.2 升级到 zbs-5.7.0
                            升级内核
                            不升级内核
                            部署 sfs 之后内核升级
                            升级前准备
                            升级后检查
                            升级后检查并开启 RDMA
                            升级后检查 DSA 硬件加速
                    单一 SSD，缓存盘和数据盘共享（默认）
                        节点运维
                            节点添加
                                OS 安装在独立的硬 RAID1，混闪节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，但需要保证为 SSD，所以 HDD 磁盘不能挂载
                                OS 安装在独立的硬 RAID1，多种 SSD 节点（分层），，新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，所以只能挂载一种 SSD
                                OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘），可以添加
                                OS 安装在软 RAID1，混闪节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，但需要保证为 SSD，所以 HDD 磁盘不能挂载
                                OS 安装在软 RAID1，多种 SSD 节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，所以只能挂载一种 SSD
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘），可以添加
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘），可以添加
                            主机强制关机/重启
                                提交关机前的提示 —— 原校验
                                提交关机前的提示 —— 新校验
                                提交关机失败后的提示 —— 原提示
                                提交关机失败后的提示 —— 新提示
                                提交重启前的提示 —— 原校验
                                提交重启前的提示 —— 新校验
                                提交重启失败后的提示 —— 原提示
                                提交重启失败后的提示 —— 新提示
                            角色转换
                                存储节点转为主节点
                                主节点转为存储节点
                            维护模式
                                原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                            节点移除
                                移除处于健康状态的主机
                                移除处于维护模式的主机
                                移除处于无响应状态的主机
                                移除当前主机后，集群中 chunk 服务健康且非移除中的主机是不满足纠删码卷的要求，预期移除检查不通过
                                集群中主节点数量不否满足要求
                                集群中其他主机的 chunk 实例处于 idle 状态
                                集群中其他主机的空闲 perf 存储空间是否充足
                                集群中其他主机的空闲 pin 存储空间是否充足
                                集群中其他主机的空闲 cap 存储空间是否充足
                                集群中存在正在添加的主机，等待主机完成当前进行中的任务
                                集群中存在正在进入维护模式的主机，等待主机完成当前进行中的任务
                                集群中存在处于维护模式的其他主机，先完成其维护任务、并退出维护模式
                                集群中存在正在移除或移除失败的其他主机，先完成其移除主机任务
                                集群中存在正在转换角色或转换失败的主机，先完成其角色转换任务
                                集群中存在数据恢复，等待数据恢复完成
                                集群不处于升级中状态
                                双活集群
                        磁盘运维
                            添加
                                磁盘推荐 —— SSD
                                磁盘推荐 —— HDD，不允许挂载
                            异常处理
                                磁盘掉线，告警信息描述节点信息
                                分区故障，告警信息描述节点信息
                                物理盘隔离
                        集群升级
                            SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                            OS 安装在软 RAID1—全闪分层
                            OS 安装在软 RAID1—混闪分层
                            OS 安装在的软 RAID1—不分层
                            OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                            zbs-5.2.0 升级到 zbs-5.7.0
                            zbs-5.4.1 升级到 zbs-5.7.0
                            zbs-5.6.2 升级到 zbs-5.7.0
                            升级内核
                            不升级内核
                            部署 sfs 之后内核升级
                            升级前准备
                            升级后检查
                            升级后检查并开启 RDMA
                            升级后检查 DSA 硬件加速
                    单一SSD，缓存盘和数据盘独占（可选）
                        节点运维
                            节点添加
                                OS 安装在独立的硬 RAID1，混闪节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，但需要保证为 SSD，所以 HDD 磁盘不能挂载
                                OS 安装在独立的硬 RAID1，多种 SSD 节点（分层），，新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，所以只能挂载一种 SSD
                                OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘），可以添加
                                OS 安装在软 RAID1，混闪节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，但需要保证为 SSD，所以 HDD 磁盘不能挂载
                                OS 安装在软 RAID1，多种 SSD 节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，所以只能挂载一种 SSD
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘），可以添加
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘），可以添加
                            角色转换
                                存储节点转为主节点
                                主节点转为存储节点
                            维护模式
                                原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                            节点移除
                                移除处于健康状态的主机
                        磁盘运维
                            添加
                                磁盘推荐 —— SSD
                                磁盘推荐 —— HDD
                            异常处理
                                磁盘掉线，告警信息描述节点信息
                                分区故障，告警信息描述节点信息
                                物理盘隔离
                        集群升级
                            SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                            OS 安装在软 RAID1—全闪分层
                            OS 安装在软 RAID1—混闪分层
                            OS 安装在的软 RAID1—不分层
                            OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                            zbs-5.2.0 升级到 zbs-5.7.0
                            zbs-5.4.1 升级到 zbs-5.7.0
                            zbs-5.6.2 升级到 zbs-5.7.0
                            升级内核
                            不升级内核
                            部署 sfs 之后内核升级
                            升级前准备
                            升级后检查
                            升级后检查并开启 RDMA
                            升级后检查 DSA 硬件加速
            不分层
                OS 安装在独立硬 RAID 1
                    节点运维
                        节点添加
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点（分层）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                        角色转换
                            存储节点转为主节点
                            主节点转为存储节点
                        维护模式
                            主节点
                            存储节点
                        节点移除
                            移除处于健康状态的主机
                    磁盘运维
                        添加
                            磁盘推荐 —— SSD
                            磁盘推荐 —— HDD
                        卸载
                            不支持卸载系统盘
                        异常处理
                            磁盘掉线，告警信息描述节点信息
                            分区故障，告警信息描述节点信息
                            物理盘隔离
                    集群升级
                        SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                        OS 安装在软 RAID1—全闪分层
                        OS 安装在软 RAID1—混闪分层
                        OS 安装在的软 RAID1—不分层
                        OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                        zbs-5.2.0 升级到 zbs-5.7.0
                        zbs-5.4.1 升级到 zbs-5.7.0
                        zbs-5.6.2 升级到 zbs-5.7.0
                        升级内核
                        不升级内核
                        部署 sfs 之后内核升级
                        升级前准备
                        升级后检查
                        升级后检查并开启 RDMA
                        升级后检查 DSA 硬件加速
                OS 安装在软 RAID 1
                    节点运维
                        节点添加
                            OS 安装在独立的硬 RAID1，混闪节点
                            OS 安装在独立的硬 RAID1，多种 SSD 节点
                            OS 安装在独立的硬 RAID1，单一 SSD 节点
                            OS 安装在软 RAID1，混闪节点
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点
                        角色转换
                            存储节点转为主节点
                            主节点转为存储节点
                        节点移除
                            移除处于健康状态的主机
                    磁盘运维
                        添加
                            磁盘推荐 —— SSD
                            磁盘推荐 —— HDD
                        异常处理
                            磁盘掉线，告警信息描述节点信息
                            分区故障，告警信息描述节点信息
                            物理盘隔离
                    集群升级
                        SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                        OS 安装在软 RAID1—全闪分层
                        OS 安装在软 RAID1—混闪分层
                        OS 安装在的软 RAID1—不分层
                        OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                        zbs-5.2.0 升级到 zbs-5.7.0
                        zbs-5.4.1 升级到 zbs-5.7.0
                        zbs-5.6.2 升级到 zbs-5.7.0
                        升级内核
                        不升级内核
                        部署 sfs 之后内核升级
                        升级前准备
                        升级后检查
                        升级后检查并开启 RDMA
                        升级后检查 DSA 硬件加速
        Large
            分层
                OS 安装在独立硬 RAID 1
                    集群包含 1，2 两种实例节点
                        混闪配置
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层）
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，混闪节点（分层）
                                    OS 安装在软 RAID1，多种 SSD 节点（分层）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                                主机强制关机/重启
                                    1 实例节点
                                    2 实例节点
                                角色转换
                                    存储节点转为主节点
                                    主节点转为存储节点
                                维护模式
                                    原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                    新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                                    正常进入维护模式
                                    正常退出维护模式
                                    进入维护模式过程中节点异常导致失败
                                    退出维护模式过程中节点异常导致失败
                                节点移除
                                    移除处于健康状态的主机
                                    移除处于维护模式的主机
                                    移除处于无响应状态的主机
                                    移除当前主机后，集群中 chunk 服务健康且非移除中的主机是不满足纠删码卷的要求，但是 chunk 实例数量满足要求，预期移除检查不通过
                                    集群中主节点数量不否满足要求，但是主节点的 chunk 实例数量满足要求
                                    集群中其他主机的 chunk 实例处于 idle 状态
                                    集群中其他主机的空闲 perf 存储空间是否充足
                                    集群中其他主机的空闲 pin 存储空间是否充足
                                    集群中其他主机的空闲 cap 存储空间是否充足
                                    集群中存在正在添加的主机，等待主机完成当前进行中的任务
                                    集群中存在正在进入维护模式的主机，等待主机完成当前进行中的任务
                                    集群中存在处于维护模式的其他主机，先完成其维护任务、并退出维护模式
                                    集群中存在正在移除或移除失败的其他主机，先完成其移除主机任务
                                    集群中存在正在转换角色或转换失败的主机，先完成其角色转换任务
                                    集群中存在数据恢复，等待数据恢复完成
                                    集群不处于升级中状态
                                    双活集群
                                    UI 不提供增加/移除某个实例这样的操作
                                    移除主机，所有硬盘池对应的 chunk 都需要从存储池中移除
                                    多 chunk 实例，任一 chunk 移除失败
                            磁盘运维
                                添加
                                    磁盘推荐 —— NVMe SSD，SATA/SAS SSD，默认推荐为缓存盘，可选为数据盘
                                    磁盘推荐 —— HDD，数据盘
                                    节点数据分区容量上限 256TiB，缓存分区总容量上限 52TiB
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 分层+缓存盘独立部署，允许卸载最后一块数据盘
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                                异常处理
                                    磁盘掉线，告警信息描述节点和chunk信息
                                    分区故障，告警信息描述节点和chunk信息
                                    物理盘隔离
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 RDMA
                                升级后检查 DSA 硬件加速
                        多种类型 SSD
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层）
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，混闪节点（分层）
                                    OS 安装在软 RAID1，多种 SSD 节点（分层）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                                主机强制关机/重启
                                    提交关机前的提示 —— 原校验
                                    提交关机前的提示 —— 新校验
                                    提交关机失败后的提示 —— 原提示
                                    提交关机失败后的提示 —— 新提示
                                    提交重启前的提示 —— 原校验
                                    提交重启前的提示 —— 新校验
                                    提交重启失败后的提示 —— 原提示
                                    提交重启失败后的提示 —— 新提示
                                角色转换
                                    存储节点转为主节点
                                    主节点转为存储节点
                                维护模式
                                    原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                    新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                                节点移除
                                    移除处于健康状态的主机
                            磁盘运维
                                添加
                                    磁盘推荐 —— NVMe SSD，默认推荐为缓存盘，可选为数据盘
                                    磁盘推荐 —— SATA/SAS SSD，默认为数据盘，可选为缓存盘
                                    磁盘推荐 —— HDD, 数据盘（优先级低）
                                    节点数据分区容量上限 128TiB，缓存分区总容量上限 26TiB
                                异常处理
                                    磁盘掉线，告警信息描述节点和chunk信息
                                    分区故障，告警信息描述节点和chunk信息
                                    物理盘隔离
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—全闪分层
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在的软 RAID1—不分层
                                zbs-5.5.1 升级到 zbs-5.7.0
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 RDMA
                                升级后检查 DSA 硬件加速
                        单一 SSD（集群部署时缓存盘和数据盘独立 ，添加节点覆盖缓存和数据共享磁盘）
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层），检查不通过
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层），检查不通过
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，混闪节点（分层），检查不通过
                                    OS 安装在软 RAID1，多种 SSD 节点（分层），检查不通过
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                                角色转换
                                    存储节点转为主节点
                                    主节点转为存储节点
                                节点移除
                                    移除处于健康状态的主机
                            磁盘运维
                                添加
                                    磁盘推荐 ——  集群全为 NVME SSD，添加 NVME SSD 为数据盘
                                    磁盘推荐 —— HDD，允许挂载
                                    磁盘推荐 ——  集群全为 NVME SSD，添加 SATA/SAS SSD, 可挂载为数据盘
                                    节点数据分区容量上限 128TiB，缓存分区总容量上限 26TiB
                                异常处理
                                    磁盘掉线，告警信息描述节点和chunk信息
                                    分区故障，告警信息描述节点和chunk信息
                                    物理盘隔离
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—全闪分层
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在的软 RAID1—不分层
                                OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 RDMA
                                升级后检查 DSA 硬件加速
                OS 安装在软 RAID 1
                    集群包含 1，2 两种实例节点
                        混闪配置
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层）
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，混闪节点（分层）
                                    OS 安装在软 RAID1，多种 SSD 节点（分层）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                                角色转换
                                    存储节点转为主节点
                                    主节点转为存储节点
                                节点移除
                                    移除处于健康状态的主机
                            磁盘运维
                                添加
                                    磁盘推荐 —— SSD
                                    磁盘推荐 —— HDD
                                    节点数据分区容量上限 128TiB，缓存分区总容量上限 26TiB
                                异常处理
                                    磁盘掉线，告警信息描述节点信息
                                    分区故障，告警信息描述节点信息
                                    物理盘隔离
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—全闪分层
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在的软 RAID1—不分层
                                zbs-5.5.0 升级到 zbs-5.7.0
                                zbs-5.6.2 升级到 zbs-5.7.0
                                zbs-5.6.3 升级到 zbs-5.7.0
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 vhost
                                升级后检查 DSA 硬件加速
                        多种类型 SSD 全闪配置
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层）
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，混闪节点（分层）
                                    OS 安装在软 RAID1，多种 SSD 节点（分层）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                                角色转换
                                    存储节点转为主节点
                                    主节点转为存储节点
                                维护模式
                                    原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                    新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                                节点移除
                                    移除处于健康状态的主机
                            磁盘运维
                                添加
                                    磁盘推荐 —— NVMe SSD
                                    磁盘推荐 —— SATA/SAS SSD
                                    磁盘推荐 —— HDD
                                异常处理
                                    磁盘掉线，告警信息描述节点信息
                                    分区故障，告警信息描述节点信息
                                    物理盘隔离
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—全闪分层
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在的软 RAID1—不分层
                                zbs-5.5.0 升级到 zbs-5.7.0
                                zbs-5.6.2 升级到 zbs-5.7.0
                                zbs-5.6.3 升级到 zbs-5.7.0
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 RDMA
                                升级后检查 DSA 硬件加速
                                zbs-5.6.3 升级到 zbs-5.7.0
                        单一 SSD，缓存盘和数据盘共享（默认）
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘），可以添加
                                    OS 安装在软 RAID1，混闪节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类
                                    OS 安装在软 RAID1，多种 SSD 节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘），可以添加
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据独占磁盘），可以添加
                                角色转换
                                    存储节点转为主节点
                                    主节点转为存储节点
                                维护模式
                                    原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                    新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                                节点移除
                                    移除处于健康状态的主机
                            磁盘运维
                                添加
                                    磁盘推荐 —— SSD
                                    磁盘推荐 —— HDD，不允许挂载
                                异常处理
                                    磁盘掉线，告警信息描述节点信息
                                    分区故障，告警信息描述节点信息
                                    物理盘隔离
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—全闪分层
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在的软 RAID1—不分层
                                zbs-5.5.0 升级到 zbs-5.7.0
                                zbs-5.6.2 升级到 zbs-5.7.0
                                zbs-5.6.3 升级到 zbs-5.7.0
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 vhost
                                升级后检查 DSA 硬件加速
                        单一 SSD，缓存盘和数据盘独占
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，但需要保证为 SSD，所以 HDD 磁盘不能挂载
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层），，新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，所以只能挂载一种 SSD
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘），可以添加
                                    OS 安装在软 RAID1，混闪节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，但需要保证为 SSD，所以 HDD 磁盘不能挂载
                                    OS 安装在软 RAID1，多种 SSD 节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，所以只能挂载一种 SSD
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘），可以添加
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘），可以添加
                                角色转换
                                    存储节点转为主节点
                                    主节点转为存储节点
                                维护模式
                                    原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                    新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                                节点移除
                                    移除处于健康状态的主机
                            磁盘运维
                                添加
                                    磁盘推荐 —— SSD
                                    磁盘推荐 —— HDD
                                异常处理
                                    磁盘掉线，告警信息描述节点信息
                                    分区故障，告警信息描述节点信息
                                    物理盘隔离
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—全闪分层
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在的软 RAID1—不分层
                                OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                                zbs-5.5.0 升级到 zbs-5.7.0
                                zbs-5.6.2 升级到 zbs-5.7.0
                                zbs-5.6.3 升级到 zbs-5.7.0
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 RDMA
                                升级后检查 DSA 硬件加速
            不分层
                OS 安装在独立硬 RAID 1
                    集群包含 1，2 两种实例节点
                        节点运维
                            节点添加
                                OS 安装在独立的硬 RAID1，混闪节点
                                OS 安装在独立的硬 RAID1，多种 SSD 节点
                                OS 安装在独立的硬 RAID1，单一 SSD 节点
                                OS 安装在软 RAID1，混闪节点
                                OS 安装在软 RAID1，多种 SSD 节点
                                OS 安装在软 RAID1，单一 SSD 节点
                            角色转换
                                存储节点转为主节点
                                主节点转为存储节点
                            维护模式
                                原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                            节点移除
                                移除处于健康状态的主机
                        磁盘运维
                            添加
                                磁盘推荐 —— SSD
                                磁盘推荐 —— HDD
                            异常处理
                                磁盘掉线，告警信息描述节点信息
                                分区故障，告警信息描述节点信息
                                物理盘隔离
                            卸载
                                预检查 —— 不能有待恢复数据
                                预检查 —— 不能有 dead extent
                                预检查 —— 物理盘卸载空间校验
                                原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                数据迁移
                                不支持卸载系统盘
                                移除磁盘需要明确的指定实例
                        集群升级
                            SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                            OS 安装在软 RAID1—全闪分层
                            OS 安装在软 RAID1—混闪分层
                            OS 安装在的软 RAID1—不分层
                            OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                            zbs-5.5.0 升级到 zbs-5.7.0
                            zbs-5.6.2 升级到 zbs-5.7.0
                            zbs-5.6.3 升级到 zbs-5.7.0
                            升级内核
                            不升级内核
                            部署 sfs 之后内核升级
                            升级前准备
                            升级后检查
                            升级后检查并开启 vhost
                            升级后检查 DSA 硬件加速
                OS 安装在软 RAID 1
                    集群包含 1，2 两种实例节点
                        节点运维
                            节点添加
                                OS 安装在独立的硬 RAID1，混闪节点
                                OS 安装在独立的硬 RAID1，多种 SSD 节点
                                OS 安装在独立的硬 RAID1，单一 SSD 节点
                                OS 安装在软 RAID1，混闪节点
                                OS 安装在软 RAID1，多种 SSD 节点
                                OS 安装在软 RAID1，单一 SSD 节点
                            角色转换
                                存储节点转为主节点
                                主节点转为存储节点
                            维护模式
                                原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                            节点移除
                                移除处于健康状态的主机
                        磁盘运维
                            添加
                                磁盘推荐 —— SSD
                                磁盘推荐 —— HDD
                            异常处理
                                磁盘掉线，告警信息描述节点信息
                                分区故障，告警信息描述节点信息
                                物理盘隔离
                            卸载
                                预检查 —— 不能有待恢复数据
                                预检查 —— 不能有 dead extent
                                预检查 —— 物理盘卸载空间校验
                                原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                数据迁移
                                不支持卸载系统盘
                                移除磁盘需要明确的指定实例
                        集群升级
                            SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                            OS 安装在软 RAID1—全闪分层
                            OS 安装在软 RAID1—混闪分层
                            OS 安装在的软 RAID1—不分层
                            OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                            zbs-5.5.0 升级到 zbs-5.7.0
                            zbs-5.6.2 升级到 zbs-5.7.0
                            zbs-5.6.3 升级到 zbs-5.7.0
                            升级内核
                            不升级内核
                            部署 sfs 之后内核升级
                            升级前准备
                            升级后检查
                            升级后检查并开启 vhost
                            升级后检查 DSA 硬件加速
        XLarge
            分层
                OS 安装在独立硬 RAID 1
                    集群包含 1，2 ，4 三种实例节点
                        混闪配置
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层）
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，混闪节点（分层）
                                    OS 安装在软 RAID1，多种 SSD 节点（分层）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                                主机强制关机/重启
                                    提交关机前的提示 —— 原校验
                                    提交关机前的提示 —— 新校验
                                    提交关机失败后的提示 —— 原提示
                                    提交关机失败后的提示 —— 新提示
                                    提交重启前的提示 —— 原校验
                                    提交重启前的提示 —— 新校验
                                    提交重启失败后的提示 —— 原提示
                                    提交重启失败后的提示 —— 新提示
                                角色转换
                                    存储节点转为主节点
                                    主节点转为存储节点
                                维护模式
                                    原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                    新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                                    正常 & 异常 进入维护模式
                                    正常退出维护模式
                                    进入维护模式过程中节点异常导致失败
                                    退出维护模式过程中节点异常导致失败
                                节点移除
                                    移除处于健康状态的主机
                                    移除处于维护模式的主机
                                    移除处于无响应状态的主机
                                    移除当前主机后，集群中 chunk 服务健康且非移除中的主机是不满足纠删码卷的要求，但是 chunk 实例数量满足要求，预期移除检查不通过
                                    集群中主节点数量不否满足要求，但是主节点的 chunk 实例数量满足要求
                                    集群中其他主机的 chunk 实例处于 idle 状态
                                    集群中其他主机的空闲 perf 存储空间是否充足
                                    集群中其他主机的空闲 pin 存储空间是否充足
                                    集群中其他主机的空闲 cap 存储空间是否充足
                                    集群中存在正在添加的主机，等待主机完成当前进行中的任务
                                    集群中存在正在进入维护模式的主机，等待主机完成当前进行中的任务
                                    集群中存在处于维护模式的其他主机，先完成其维护任务、并退出维护模式
                                    集群中存在正在移除或移除失败的其他主机，先完成其移除主机任务
                                    集群中存在正在转换角色或转换失败的主机，先完成其角色转换任务
                                    集群中存在数据恢复，等待数据恢复完成
                                    集群不处于升级中状态
                                    双活集群
                                    UI 不提供增加/移除某个实例这样的操作
                                    移除主机，所有硬盘池对应的 chunk 都需要从存储池中移除
                                    多 chunk 实例，任一 chunk 移除失败
                            磁盘运维
                                添加
                                    磁盘推荐 —— NVMe SSD，SATA/SAS SSD，默认推荐为缓存盘，可选为数据盘
                                    磁盘推荐 —— HDD，数据盘
                                    节点数据分区容量上限 128TiB，缓存分区总容量上限 26TiB
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                                异常处理
                                    磁盘掉线，告警信息描述节点信息
                                    分区故障，告警信息描述节点信息
                                    物理盘隔离
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—全闪分层
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在的软 RAID1—不分层
                                OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                                zbs-5.2.0 升级到 zbs-5.7.0
                                zbs-5.4.1 升级到 zbs-5.7.0
                                zbs-5.6.2 升级到 zbs-5.7.0
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 vhost
                                升级后检查 DSA 硬件加速
                        多种类型 SSD
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层）
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，混闪节点（分层）
                                    OS 安装在软 RAID1，多种 SSD 节点（分层）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                                角色转换
                                    存储节点转为主节点
                                    主节点转为存储节点
                                维护模式
                                    原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                    新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                                节点移除
                                    移除处于健康状态的主机
                            磁盘运维
                                添加
                                    磁盘推荐 —— NVMe SSD，默认推荐为缓存盘，可选为数据盘
                                    磁盘推荐 —— SATA/SAS SSD，默认为数据盘，可选为缓存盘
                                    磁盘推荐 —— HDD, 数据盘（优先级低）
                                    节点数据分区容量上限 128TiB，缓存分区总容量上限 26TiB
                                异常处理
                                    磁盘掉线，告警信息描述节点信息
                                    分区故障，告警信息描述节点信息
                                    物理盘隔离
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—全闪分层
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在的软 RAID1—不分层
                                OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                                zbs-5.2.0 升级到 zbs-5.7.0
                                zbs-5.4.1 升级到 zbs-5.7.0
                                zbs-5.6.2 升级到 zbs-5.7.0
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 RDMA
                                升级后检查 DSA 硬件加速
                        单一 SSD（集群部署时缓存和数据共享磁盘 ，添加节点覆盖缓存盘和数据盘独立）
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层），检查不通过
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层），检查不通过
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，混闪节点（分层），检查不通过
                                    OS 安装在软 RAID1，多种 SSD 节点（分层），检查不通过
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                                角色转换
                                    存储节点转为主节点
                                    主节点转为存储节点
                                维护模式
                                    原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                    新校验 —— 除当前节点外，包含健康且非移除中的存储服务的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                节点移除
                                    移除处于健康状态的主机
                            磁盘运维
                                添加
                                    磁盘推荐 ——  集群全为 NVME SSD，添加 NVME SSD 为数据盘
                                    磁盘推荐 —— HDD，不允许挂载
                                    磁盘推荐 ——  集群全为 NVME SSD，添加 SATA/SAS SSD, 可挂载为数据盘
                                    节点数据分区容量上限 128TiB，缓存分区总容量上限 26TiB
                                异常处理
                                    磁盘掉线，告警信息描述节点信息
                                    分区故障，告警信息描述节点信息
                                    物理盘隔离
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—全闪分层
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在的软 RAID1—不分层
                                OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                                zbs-5.2.0 升级到 zbs-5.7.0
                                zbs-5.4.1 升级到 zbs-5.7.0
                                zbs-5.6.2 升级到 zbs-5.7.0
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 vhost
                                升级后检查 DSA 硬件加速
                OS 安装在软 RAID 1
                    集群包含 1，2 ，4 三种实例节点
                        混闪配置
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层）
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，混闪节点（分层）
                                    OS 安装在软 RAID1，多种 SSD 节点（分层）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据独占磁盘）
                                角色转换
                                    存储节点转为主节点
                                    无响应主节点转为存储节点
                                维护模式
                                    原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                    新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                                节点移除
                                    移除无响应状态的主机
                            磁盘运维
                                添加
                                    磁盘推荐 —— SSD
                                    磁盘推荐 —— HDD
                                    节点数据分区容量上限 128TiB，缓存分区总容量上限 26TiB
                                异常处理
                                    磁盘掉线，告警信息描述节点信息
                                    分区故障，告警信息描述节点信息
                                    物理盘隔离
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 可以卸载最后一块包含数据分区的物理盘（只有缓存分区，新增）
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—全闪分层
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在的软 RAID1—不分层
                                OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                                zbs-5.2.0 升级到 zbs-5.7.0
                                zbs-5.4.1 升级到 zbs-5.7.0
                                zbs-5.6.2 升级到 zbs-5.7.0
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 RDMA
                                升级后检查 DSA 硬件加速
                        多种类型 SSD 全闪配置
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层）
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，混闪节点（分层）
                                    OS 安装在软 RAID1，多种 SSD 节点（分层）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                                角色转换
                                    存储节点转为主节点
                                    主节点转为存储节点
                                维护模式
                                    原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                    新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                                节点移除
                                    移除处于健康状态的主机
                            磁盘运维
                                添加
                                    磁盘推荐 —— NVMe SSD
                                    磁盘推荐 —— SATA/SAS SSD
                                    磁盘推荐 —— HDD
                                异常处理
                                    磁盘掉线，告警信息描述节点信息
                                    分区故障，告警信息描述节点信息
                                    物理盘隔离
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—全闪分层
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在的软 RAID1—不分层
                                OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                                zbs-5.2.0 升级到 zbs-5.7.0
                                zbs-5.4.1 升级到 zbs-5.7.0
                                zbs-5.6.2 升级到 zbs-5.7.0
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 RDMA
                                升级后检查 DSA 硬件加速
                        单一 SSD，缓存盘和数据盘共享（默认）
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，但需要保证为 SSD，所以 HDD 磁盘不能挂载
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层），，新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，所以只能挂载一种 SSD
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘），可以添加
                                    OS 安装在软 RAID1，混闪节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，但需要保证为 SSD，所以 HDD 磁盘不能挂载
                                    OS 安装在软 RAID1，多种 SSD 节点（分层），新添加节点必须为单一类型 SSD, 不强要求新添加节点的 SSD 与 集群 SSD 是一类，所以只能挂载一种 SSD
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘），可以添加
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘），可以添加
                                角色转换
                                    存储节点转为主节点
                                    主节点转为存储节点
                                维护模式
                                    原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                    新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                                节点移除
                                    移除处于健康状态的主机
                            磁盘运维
                                添加
                                    磁盘推荐 —— SSD
                                    磁盘推荐 —— HDD，不允许挂载
                                异常处理
                                    磁盘掉线，告警信息描述节点信息
                                    分区故障，告警信息描述节点信息
                                    物理盘隔离
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—全闪分层
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在的软 RAID1—不分层
                                OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                                zbs-5.2.0 升级到 zbs-5.7.0
                                zbs-5.4.1 升级到 zbs-5.7.0
                                zbs-5.6.2 升级到 zbs-5.7.0
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 RDMA
                                升级后检查 DSA 硬件加速
                        单一 SSD，缓存盘和数据盘独占
                            节点运维
                                节点添加
                                    OS 安装在独立的硬 RAID1，混闪节点（分层），不允许添加（新增节点也需要是全闪，全 NVMe 或 全 SATA/SAS）
                                    OS 安装在独立的硬 RAID1，多种 SSD 节点（分层），不允许添加（新增节点也需要是全闪，全 NVMe 或 全 SATA/SAS）
                                    OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘），可以添加
                                    OS 安装在软 RAID1，混闪节点（分层），不允许添加（新增节点也需要是全闪，全 NVMe 或 全 SATA/SAS）
                                    OS 安装在软 RAID1，多种 SSD 节点（分层），不允许添加（新增节点也需要是全闪，全 NVMe 或 全 SATA/SAS）
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘），可以添加
                                    OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘），可以添加
                                角色转换
                                    存储节点转为主节点
                                    主节点转为存储节点
                                维护模式
                                    原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                    新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                                节点移除
                                    移除主机
                            磁盘运维
                                添加
                                    磁盘推荐 —— SSD
                                    磁盘推荐 —— HDD
                                异常处理
                                    磁盘掉线，告警信息描述节点信息
                                    分区故障，告警信息描述节点信息
                                    物理盘隔离
                                卸载
                                    预检查 —— 不能有待恢复数据
                                    预检查 —— 不能有 dead extent
                                    预检查 —— 物理盘卸载空间校验
                                    原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                    原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                    数据迁移
                                    不支持卸载系统盘
                                    移除磁盘需要明确的指定实例
                            集群升级
                                SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                                OS 安装在软 RAID1—全闪分层
                                OS 安装在软 RAID1—混闪分层
                                OS 安装在的软 RAID1—不分层
                                OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                                zbs-5.2.0 升级到 zbs-5.7.0
                                zbs-5.4.1 升级到 zbs-5.7.0
                                zbs-5.6.2 升级到 zbs-5.7.0
                                升级内核
                                不升级内核
                                部署 sfs 之后内核升级
                                升级前准备
                                升级后检查
                                升级后检查并开启 RDMA
                                升级后检查 DSA 硬件加速
            不分层
                OS 安装在独立硬 RAID 1
                    集群包含 1，2 ，4 三种实例节点
                        节点运维
                            节点添加
                                OS 安装在独立的硬 RAID1，混闪节点（分层）
                                OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                                OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                OS 安装在软 RAID1，混闪节点（分层）
                                OS 安装在软 RAID1，多种 SSD 节点（分层）
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            角色转换
                                存储节点转为主节点
                                主节点转为存储节点
                            维护模式
                                原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                            节点移除
                                移除处于健康状态的主机
                        磁盘运维
                            添加
                                磁盘推荐 —— SSD
                                磁盘推荐 —— HDD
                            异常处理
                                磁盘掉线，告警信息描述节点和chunk信息
                                分区故障，告警信息描述节点和chunk信息
                                物理盘隔离
                            卸载
                                预检查 —— 不能有待恢复数据
                                预检查 —— 不能有 dead extent
                                预检查 —— 物理盘卸载空间校验
                                原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                数据迁移
                                不支持卸载系统盘
                                移除磁盘需要明确的指定实例
                        集群升级
                            SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                            OS 安装在软 RAID1—全闪分层
                            OS 安装在软 RAID1—混闪分层
                            OS 安装在的软 RAID1—不分层
                            OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                            zbs-5.2.0 升级到 zbs-5.7.0
                            zbs-5.4.1 升级到 zbs-5.7.0
                            zbs-5.6.2 升级到 zbs-5.7.0
                            升级内核
                            不升级内核
                            部署 sfs 之后内核升级
                            升级前准备
                            升级后检查
                            升级后检查并开启 RDMA
                            升级后检查 DSA 硬件加速
                OS 安装在软 RAID 1
                    集群包含 1，2 ，4 三种实例节点
                        节点运维
                            节点添加
                                OS 安装在独立的硬 RAID1，混闪节点，预期不可添加有 HDD 盘的节点
                                OS 安装在独立的硬 RAID1，多种 SSD 节点
                                OS 安装在独立的硬 RAID1，单一 SSD 节点
                                OS 安装在软 RAID1，混闪节点（分层）
                                OS 安装在软 RAID1，多种 SSD 节点（分层）
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                                OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            角色转换
                                存储节点转为主节点
                                主节点转为存储节点
                            维护模式
                                原校验 —— 除当前节点外，chunk 服务健康且非移除中的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性
                                新校验 —— 除当前节点外，包含健康且非移除中的硬盘池的节点不足 %K+M% 个，无法保证纠删码卷的数据安全性（还是检查节点数）
                            节点移除
                                移除处于健康状态的主机
                        磁盘运维
                            添加
                                磁盘推荐 —— SSD
                                磁盘推荐 —— HDD
                            异常处理
                                磁盘掉线，告警信息描述节点和chunk信息
                                分区故障，告警信息描述节点和chunk信息
                                物理盘隔离
                            卸载
                                预检查 —— 不能有待恢复数据
                                预检查 —— 不能有 dead extent
                                预检查 —— 物理盘卸载空间校验
                                原检查 —— 不能卸载最后一块包含数据分区的物理盘
                                新检查 —— 不能卸载最后一块包含数据分区的物理盘
                                原检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                新检查 —— 不能卸载最后一块包含 Journal 分区的物理盘
                                数据迁移
                                不支持卸载系统盘
                                移除磁盘需要明确的指定实例
                        集群升级
                            SMTX ZBS 限制了单 cpu 核心 < 6 不能部署和升级
                            OS 安装在软 RAID1—全闪分层
                            OS 安装在软 RAID1—混闪分层
                            OS 安装在的软 RAID1—不分层
                            OS 安装在独立的硬 RAID1—分层（zbs-5.6.1）
                            zbs-5.2.0 升级到 zbs-5.7.0
                            zbs-5.4.1 升级到 zbs-5.7.0
                            zbs-5.6.2 升级到 zbs-5.7.0
                            升级内核
                            不升级内核
                            部署 sfs 之后内核升级
                            升级前准备
                            升级后检查
                            升级后检查并开启 RDMA
                            升级后检查 DSA 硬件加速
    监控告警
        监控分析
            资源类型，在「主机」与「物理盘」之间新增「物理盘池」选项
            主机IO和容量相关的指标均为主机上所有硬盘池对应指标的聚合信息
            新增资源类型“硬盘池”，支持指标与之前主机l〇和容量相关的指标一致
            新增资源类型“硬盘池”，支持选择固定对象或Top N，选择固定对象时，下拉列表需同时展示主机名称和硬盘池ID
            新增资源类型“硬盘池”，图标名称和图例需要同时展示主机名称和硬盘池ID
            模式支持选定对象和资源 Top N
            资源对象（模式选择「选定对象」后，展示「资源对象」字段）
        报警项
            zbs-5.7.0 之前版本，平均延迟
            zbs-5.7.0 及之后版本，平均延迟
            zbs-5.7.0 之前版本，存储健康状态
            zbs-5.7.0 及之后版本，存储健康状态
            zbs-5.7.0 之前版本，存储空间使用率
            zbs-5.7.0 及之后版本，存储空间使用率
            zbs-5.7.0 之前版本，热点数据大于主机总缓存空间
            zbs-5.7.0 及之后版本，热点数据大于主机总缓存空间
            zbs-5.7.0 之前版本，I/O 总带宽
            zbs-5.7.0 及之后版本，I/O 总带宽
            zbs-5.7.0 之前版本，读带宽
            zbs-5.7.0 及之后版本，读带宽
            zbs-5.7.0 之前版本，写带宽
            zbs-5.7.0 及之后版本，写带宽
    前端适配多实例
        安装部署
            扫描集群
                节点展示容量规格 Normal/Large/xLarge
                节点展示系统盘，操作系统与缓存/数据共享物理盘
                节点展示系统盘，操作系统使用独立物理盘
                选中的 N 台主机的操作系统部署模式不同时，展示 tip: "建议同一集群内的主机使用相同的操作系统部署模式"，非强制策略
                容量规格必须相同，选择 normal with large，报错 “请选择相同容量规格的主机”
                容量规格必须相同，选择 normal with xlarge，报错 “请选择相同容量规格的主机”
                容量规格必须相同，选择 large with xlarge，报错 “请选择相同容量规格的主机”
                normal 规格，数据分区总容量超过 128TiB, 报错“数据分区总容量不允许超过 128TiB, 否则部署失败”（前端不校验了，最后部署时检查不通过兜底）
                Large 规格，数据分区总容量超过 256TiB, 报错“数据分区总容量不允许超过 256TiB, 否则部署失败”（前端不校验了，最后部署时检查不通过兜底）
                XLarge 规格，数据分区总容量超过 512TiB, 报错“数据分区总容量不允许超过 512TiB, 否则部署失败”（前端不校验了，最后部署时检查不通过兜底）
            配置存储
                物理盘用途提示：请根据主机的硬件配置，为每个主机配置物理盘池数量和每个池中的物理盘用途。为提升容错能力，建议每个池中至少包含2块SSD
                样式更新，主机间增加分割线
                物理盘池-池数
                物理盘-按池分组
                物理盘-不挂载
                物理盘 —— 移动 btn
                物理盘 —— 移动 btn 的 tooltip
                物理盘 —— 用途更改
                系统盘独立部署，SMTX 系统盘，不属于任何池，固定展示在第一个池上方
                集群最多可配置 255 个物理盘
                最小盘数校验 —— 1 个实例 + OS 安装在独立的硬 RAID 1
                最小盘数校验 —— 1 个实例 + OS 安装在软 RAID 1
                最小盘数校验 —— 2 个实例 + OS 安装在独立的硬 RAID 1
                最小盘数校验 —— 2 个实例 + OS 安装在软 RAID 1
                最小盘数校验 —— 4 个实例 + OS 安装在独立的硬 RAID 1
                最小盘数校验 —— 4 个实例 + OS 安装在软 RAID 1
                分层＋所有主机的所有盘是单一类型 SSD + 含元数据分区的数据盘（包含系统盘部署在软 RAID 1 的节点为必要条件）
                分层＋所有主机的所有盘是单一类型SSD＋含元数据分区的缓存盘（包含系统盘部署在软 RAID 1 的节点为必要条件）
                分层＋所有主机的所有盘是单一类型SSD＋部分节点为 OS 安装在软 RAID 1,部分节点为 OS 安装在独立硬 RAID 1
                展示存储池和磁盘的 NUMA Node
            检查配置
                检查配置 —— 物理盘，新增所属磁盘池
                检查配置 —— 物理盘，不挂载的盘，所属物理盘池为[不挂载]，用途为 [不挂载]
                检查配置 —— 物理盘，SMTX 系统盘，所属物理盘池取值为空，用途为 SMTX 系统盘
        添加节点
            选择主机-规格检查（normal 添加 xlarge）
            选择主机-规格检查（large 添加 xlarge）
            选择主机-规格检查（xlarge 添加 normal）
            选择主机-规格检查（xlarge 添加 large）
            配置主机，新增固定文案
            配置主机，新增选择池数量入口
            将盘分组展示在各个池内
            磁盘池标展示格式为 [%chunk-id% 池]
            如果池内没有盘，则“池内”展示[无物理盘]
            用户可以更改池的数量，用户更改后，需自动刷新
            用户可以更改盘的所属池及用途，用户更改后，需自动刷新
            多个池时，提供移动按钮
            只有一个池时，提供移除按钮
            不挂载的盘（即“未加入池的盘”）单独成组，用途取值为空
            如果没有“不挂载的盘”，则不展示该分组
            不挂载的磁盘提供“加入池按钮”
            提供展开和收起功能按钮
            磁盘数量最小验证，池 %chunk-id-1%、%chunk-id-2% 缺少缓存盘
            磁盘数量最小验证，池 %chunk-id-1%、%chunk-id-2% 缺少物理盘
            物理盘池数量规格，集群最多可配置 255 个磁盘池
            系统盘部署于任何池，固定展示在第一个池上方
            英文界面检查
            zbs-5.6.2 版本节点添加
        添加磁盘
            磁盘按池分组
            磁盘用途指定
            移动按钮、加入池按钮
            任务中心新增报错，新增 XXLarge 容量规格的主机上限为512 TiB
            任务中心新增报错，物理盘池%chunk-id-1%、%chunk-id-2%数据分区总容量不可超过256 TiB。
            任务中心新增报错，物理盘池%chunk-id-1%、%chunk-id-2%缓存分区总容量不可超过51TiB
            任务中心新增报错，分层-缓存和数据盘独立部署︰「物理盘池%chunk-id-1%、%chunk-id-2%已挂载64块物理盘，达到上限
            任务中心新增报错，不分层;分层-缓存和数据共享所有物理盘︰「物理盘池%chunk-id-1%、%chunk-id-2%已挂载32块物理盘，达到上限。」
        物理盘
            新增 NUMA 节点，默认不展示，默认位于「剩余寿命」列后;支持排序
            新增所属物理盘池
            从池的物理盘 Table 进入盘详情面板
            盘详情面板新增字段
        磁盘池
            导航，集群层，可用域层，主机层展示
            池 Table，主机层，集群层展示
            池详情面板 —— 详情Tab
            池详情面板 —— 物理盘Tab
            池详情面板 —— Header 异常
        主机
            列表和详情
            主机状态
            主机 Table —— 状态列
            主机 Table —— 新增物理盘池数列
            主机概览 —— 异常提示
            主机概览 —— 主机信息
            拓扑展示
            NUMA展示
            硬盘池列表 —— 基本信息
            硬盘池列表 —— 物理盘信息
            硬盘池列表 —— 容量使用情况
            磁盘池列表 —— 异常展示
        网口
            网口 Talbe，新增 NUMA 节点
            网口详情面板，新增 NUMA 节点字段
        支持 DSA 硬件加速功能
            前端可以展示，也可以开启
            支持集群异构，可以全部开启也可以部分开启
            后端命令行可以开启
        集群操作
            tower 添加集群
            tower 移除集群
            升级中心升级集群
            关联可观测
            部署高级监控
            日志收集
    License
        License 中限制的最大节点数依旧代表节点，节点数不等价于 Chunk 数。
        ZBS 本身使用容量授权，实例数不影响容量，也无需调整
zbs-5.7.0 数据块制备类型调整
    Pin volume 创建
        创建 pin volume，不指定 volume 的属性（随所属 target 的属性）
        创建 pin volume，属性为 thin
        创建 pin volume，属性为 thick
    Pin volume 转换
        Thin Volume 转为 Pin
        Thick Volume 转为 Pin
        thin pin volume 转为非 pin
        thick pin volume 转为非 pin
    thick & thin 转换
        thick 转 thin 测试
        thin 转为 thick 测试
    数据下沉的不同阶段转换
        数据下沉前转换
        数据下沉后加载至读缓存再次转换
        数据下沉过程中转换
        数据完全下沉后转换
    集成测试
        Thin Volume 转为 Pin 后，再转为 Thick
        Thick Volume 转为 Pin 后，再转为 Thin
        Thin Pin Volume 转为非 Pin 后，再转为 Thick
        Thick Pin Volume 转为非 Pin 后，再转为 Thin
    冗余模式
        2 副本，先转换再提升副本
        2 副本，先提升副本再转换
        3 副本直接转换
    协议与客户端测试用例
        iSCSI 协议下转换测试（CentOS/ESXi/Windows）
        nvmf 协议下转换测试（Centos）
        NFS 协议下（file -> lun 与 lun -> file）转换后测试
    快照 & 克隆
        多层快照及快照转换测试
        多层克隆及克隆转换测试
        克隆与快照混合操作
        快照计划转换测试
    回收站与恢复
        回收站恢复测试
    高负载
        高负载与高并发转换
        cap 空间用尽，创建 pin volume
业务主机/主机组
    业务主机组
        创建
            入口：zbs 570 以上集群层右上角「创建」菜单，在业务主机 tab 页高亮展示
            「集群」——在集群层创建时，默认选中当前集群，创建成功
            「集群」——在集群层创建时，下拉菜单展示当前 tower 中所有 570 及以上的 zbs 集群，选择其他集群，创建成功
            「集群」——在非集群层创建时，默认为空，为空时创建失败
            「集群」——在非集群层创建时，下拉菜单展示当前 tower 中所有 570 及以上的 zbs 集群，选择集群后创建成功
            「名称」——字段校验
            「描述」——字段校验
        编辑
            弹窗展示「名称」「描述」
            编辑「名称」
            编辑「描述」
        删除
            主机组不含业务主机时，删除成功，弹窗展示正确
            主机组含有业务主机时，删除入口禁用
            主机组不包含主机，但存在关联的存储资源，删除失败，后端返回错误码
        任务和事件
            创建业务主机组
            编辑业务主机组
            删除业务主机组
    业务主机
        创建
            入口检查—— zbs 570 及以上集群层右上角「创建」菜单，在业务主机 tab 页高亮展示
            「名称」——字段校验
            「描述」——字段校验
            「业务主机组」——默认为空，展示正确，为空时创建成功
            「业务主机组」——当前集群中无业务主机组时下拉菜单展示，创建业务主机组成功
            「业务主机组」——当前集群中有业务主机组时下拉菜单展示，创建业务主机组成功
            「启动器」——表单中展示正确
            「启动器」——为空时禁止提交表单
            「启动器」——业务主机未选择已关联存储资源或不为空的主机组时，仅配置IQN /仅配置 NQN /仅配置 IP /同时配置标识符和 IP ，创建成功
            「启动器」——「标识符」字段校验
            「启动器」——「IP」字段校验
            「启动器」——「名称」随启动器的配置变化
            「启动器」——「CHAP 认证」，仅配置了标识符为 IQN 时展示 CHAP 认证选项
            「启动器」——「CHAP 认证」，字段校验
            「启动器」——「移除」，仅有一个启动时不展示
            「启动器」——「移除」，启动器数量 > 1 时，所有启动器均展示移除 icon，hover 展示「移除」
            选择「业务主机组」时，该组已关联存储资源时的提示信息和启动器的地址校验
                「业务主机组」——选择的业务主机组仅关联了 target，target 关联的主机仅均配置了 IP，提示需配置 IP 地址
                「业务主机组」——选择的业务主机组仅关联了 target，target 关联的主机均配置了 IP 和 NQN，提示需配置 IP 地址
                「业务主机组」——选择的业务主机组仅关联了 target，target 关联的主机仅均配置了 IQN，提示需配置 IQN 地址
                「业务主机组」——选择的业务主机组仅关联了 target，target 关联的主机均配置了 IP 和 IQN，提示需配置 IQN 地址（或 IP 地址）
                「业务主机组」——选择的业务主机组关联了 target，同时存在关联主机仅配置了 IP 和仅配置了 IQN 的 target，提示需配置 IQN 地址、IP 地址
                「业务主机组」——选择的业务主机组关联了 target，同时存在关联主机仅配置了 IP 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址（可选）、IP 地址
                「业务主机组」——选择的业务主机组关联了 target，同时存在关联主机仅配置了 IQN 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址（可选）
                「业务主机组」——选择的业务主机组关联了 target，同时存在关联主机仅配置了 IP、仅配置了 IQN 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址
                「业务主机组」——选择的业务主机组关联了 target 和 LUN，target 关联的主机仅均配置了 IP，提示需配置 IQN 地址、IP 地址
                「业务主机组」——选择的业务主机组关联了 target 和 LUN，target 关联的主机均配置了 IQN 和 NQN，提示需配置 IQN 地址
                「业务主机组」——选择的业务主机组关联了 target 和 LUN，target 关联的主机仅均配置了 IQN，提示需配置 IQN 地址
                「业务主机组」——选择的业务主机组关联了 target 和 LUN，target 关联的主机均配置了 IP 和 IQN，提示需配置 IQN 地址、IP 地址（可选）
                「业务主机组」——选择的业务主机组关联了 target 和 LUN，同时存在关联主机仅配置了 IP 和仅配置了 IQN 的 target，提示需配置 IQN 地址、IP 地址
                「业务主机组」——选择的业务主机组关联了 target 和 LUN，同时存在关联主机仅配置了 IP 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址
                「业务主机组」——选择的业务主机组关联了 target 和 LUN，同时存在关联主机仅配置了 IQN 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址（可选）
                「业务主机组」——选择的业务主机组关联了 target 和 LUN，同时存在关联主机仅配置了 IP、仅配置了 IQN 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址
                「业务主机组」——选择的业务主机组仅关联了 subsystem 或 ns，提示需配置 NQN 地址
                「业务主机组」——选择的业务主机组同时关联了 target 和 subsystem，在上述关联 target 用例基础上，提示中增加需配置 NQN 地址
                「业务主机组」——选择的业务主机组关联了 target，同时该 target 中存在与所属 target 一致的 lun，target 关联的主机仅均配置了 IP，提示需配置 IP 地址
                「业务主机组」——选择的业务主机组仅关联了一个 target，且该 target 仅关联了该空主机组，提示需配置 IQN 地址（或 IP 地址）
            选择「业务主机组」时，该组未关联存储资源，但是不为空时的提示信息和启动器的地址校验
                该组内主机仅均配置了 IP，提示需配置 IP 地址
                该组内主机仅均配置了 IQN，提示需配置 IQN 地址
                该组内主机均配置了 IP 和 IQN，提示需配置 IQN 地址或 IP 地址
                该组内主机仅均配置了 NQN，提示需配置 NQN 地址
                该组内主机仅均配置了 IP 和 NQN，提示需配置 NQN 地址或 IP 地址
                该组内主机仅均配置了 IQN 和 NQN，提示需配置 IQN 地址或 NQN 地址
                该组内主机均配置了 IP、IQN 和 NQN，不展示提示
        编辑
            不同「编辑」入口，均可以拉起「编辑」弹窗
            弹窗展示——标题，名称，描述，启动器常驻展示信息正确
            「已有启动器展示」，每个启动器一个框，默认展开，点击可收起，展示内容与创建时一致
            「已有启动器展示」，启动器数量 >1 时，每个启动器右上角展示删除图标
            编辑弹窗最下方存在「添加启动器」，点击新增空白启动器框，添加成功
            编辑已有启动器——更改已有启动器 IP/标识符，启动器名称变化
            配置地址的提示
                该业务主机未关联存储资源，且不属于任何主机组时不展示该提示
                该业务主机以及所属的业务主机组均未关联存储资源，且所属主机组中仅包含该业务主机时不展示该提示
                该业务主机自身关联了存储资源时，表单展示提示信息
                    「提示需配置 xxx 地址」——选择的业务主机仅关联了 target，target 关联的主机仅均配置了 IP，提示需配置 IP 地址
                    「提示需配置 xxx 地址」——选择的业务主机仅关联了 target，target 关联的主机均配置了 IP 和 NQN，提示需配置 IP 地址
                    「提示需配置 xxx 地址」——选择的业务主机仅关联了 target，target 关联的主机仅均配置了 IQN，提示需配置 IQN 地址
                    「提示需配置 xxx 地址」——选择的业务主机仅关联了 target，target 关联的主机均配置了 IP 和 IQN，提示需配置 IQN 地址（或 IP 地址）
                    「提示需配置 xxx 地址」——选择的业务主机关联了 target，同时存在关联主机仅配置了 IP 和仅配置了 IQN 的 target，提示需配置 IQN 地址、IP 地址
                    「提示需配置 xxx 地址」——选择的业务主机关联了 target，同时存在关联主机仅配置了 IP 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址（可选）、IP 地址
                    「提示需配置 xxx 地址」——选择的业务主机关联了 target，同时存在关联主机仅配置了 IQN 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址（可选）
                    「提示需配置 xxx 地址」——选择的业务主机关联了 target，同时存在关联主机仅配置了 IP、仅配置了 IQN 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址
                    「提示需配置 xxx 地址」——选择的业务主机关联了 target 和 LUN，target 关联的主机仅均配置了 IP，提示需配置 IQN 地址、IP 地址
                    「提示需配置 xxx 地址」——选择的业务主机关联了 target 和 LUN，target 关联的主机均配置了 IP 和 NQN，提示需配置 IQN 地址、IP 地址
                    「提示需配置 xxx 地址」——选择的业务主机关联了 target 和 LUN，target 关联的主机仅均配置了 IQN，提示需配置 IQN 地址
                    「提示需配置 xxx 地址」——选择的业务主机关联了 target 和 LUN，target 关联的主机均配置了 IP 和 IQN，提示需配置 IQN 地址、IP 地址（可选）
                    「提示需配置 xxx 地址」——选择的业务主机关联了 target 和 LUN，同时存在关联主机仅配置了 IP 和仅配置了 IQN 的 target，提示需配置 IQN 地址、IP 地址
                    「提示需配置 xxx 地址」——选择的业务主机关联了 target 和 LUN，同时存在关联主机仅配置了 IP 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址
                    「提示需配置 xxx 地址」——选择的业务主机关联了 target 和 LUN，同时存在关联主机仅配置了 IQN 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址（可选）
                    「提示需配置 xxx 地址」——选择的业务主机关联了 target 和 LUN，同时存在关联主机仅配置了 IP、仅配置了 IQN 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址
                    「提示需配置 xxx 地址」——选择的业务主机仅关联了 subsystem 或 ns，提示需配置 NQN 地址
                    「提示需配置 xxx 地址」——选择的业务主机同时关联了 target 和 subsystem，在上述关联 target 用例基础上，提示中增加需配置 NQN 地址
                    「提示需配置 xxx 地址」——选择的业务主机关联了 target，target 中存在与所属 target 一致的 lun，target 关联的主机仅均配置了 IP，提示需配置 IP 地址
                该业务主机仅通过主机组关联了存储资源时，表单展示提示信息
                    所属组仅关联了 target，target 关联的主机仅均配置了 IP，提示需配置 IP 地址
                    所属组仅关联了 target，target 关联的主机均配置了 IP 和 NQN，提示需配置 IP 地址
                    所属组仅关联了 target，target 关联的主机仅均配置了 IQN，提示需配置 IQN 地址
                    所属组仅关联了 target，target 关联的主机均配置了 IP 和 IQN，提示需配置 IQN 地址（或 IP 地址）
                    所属组仅关联了 target，同时存在关联主机仅配置了 IP 和仅配置了 IQN 的 target，提示需配置 IQN 地址、IP 地址
                    所属组仅关联了 target，同时存在关联主机仅配置了 IP 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址（可选）、IP 地址
                    所属组仅关联了 target，同时存在关联主机仅配置了 IQN 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址（可选）
                    所属组仅关联了 target，同时存在关联主机仅配置了 IP、仅配置了 IQN 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址
                    所属组关联了 target 和 LUN，target 关联的主机仅均配置了 IP，提示需配置 IQN 地址、IP 地址
                    所属组关联了 target 和 LUN，target 关联的主机均配置了 IQN 和 NQN，提示需配置 IQN 地址
                    所属组关联了 target 和 LUN，target 关联的主机仅均配置了 IQN，提示需配置 IQN 地址
                    所属组关联了 target 和 LUN，target 关联的主机均配置了 IP 和 IQN，提示需配置 IQN 地址、IP 地址（可选）
                    所属组仅关联了 target 和 LUN，同时存在关联主机仅配置了 IP 和仅配置了 IQN 的 target，提示需配置 IQN 地址、IP 地址
                    所属组仅关联了 target 和 LUN，同时存在关联主机仅配置了 IP 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址
                    所属组仅关联了 target 和 LUN，同时存在关联主机仅配置了 IQN 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址（可选）
                    所属组仅关联了 target 和 LUN，同时存在关联主机仅配置了 IP、仅配置了 IQN 和配置了 IP 和 IQN 的 target，提示需配置 IQN 地址、IP 地址
                    所属组仅关联了 subsystem 或 ns，提示需配置 NQN 地址
                    所属组同时关联了 target 和 subsystem，在上述关联 target 用例基础上，提示中增加需配置 NQN 地址
                    所属组仅关联了 target，target 中存在与所属 target 一致的 lun，target 关联的主机仅均配置了 IP，提示需配置 IP 地址
                该业务主机及其所属主机组均未关联存储资源，所属主机组中包含了其他业务主机
                    该组内其他主机仅均配置了 IP，提示需配置 IP 地址
                    该组内其他主机仅均配置了 IQN，提示需配置 IQN 地址
                    该组内其他主机均配置了 IP 和 IQN，提示需配置 IQN 地址或 IP 地址
                    该组内其他主机仅均配置了 NQN，提示需配置 NQN 地址
                    该组内其他主机仅均配置了 IP 和 NQN，提示需配置 NQN 地址或 IP 地址
                    该组内其他主机仅均配置了 IQN 和 NQN，提示需配置 IQN 地址或 NQN 地址
                    该组内其他主机均配置了 IP、IQN 和 NQN，不展示提示
                该业务主机同时通过自身和业务主机组关联了存储资源时，表单提示信息
                    业务主机：关联业务主机的 IP 地址；业务主机组：关联业务主机的 IP 地址。提示 IP
                    业务主机：关联业务主机的 IP 地址；业务主机组：关联业务主机的 IQN 地址（仅 IQN）。提示 IQN、IP
                    业务主机：关联业务主机的 IP 地址；业务主机组：关联业务主机的 IQN 地址（同时配置了 IP 和 IQN）。提示 IP、IQN（可选）
                    业务主机：关联业务主机的 IQN 地址（仅 IQN）；业务主机组：关联业务主机的 IP 地址。提示 IQN、IP
                    业务主机：关联业务主机的 IQN 地址（仅 IQN）；业务主机组：关联业务主机的 IQN 地址（仅 IQN）。提示 IQN
                    业务主机：关联业务主机的 IQN 地址（仅 IQN）；业务主机组：关联业务主机的 IQN 地址（同时配置了 IP 和 IQN）。提示 IQN、IP（可选）
                    业务主机：关联业务主机的 IQN 地址（同时配置了 IP 和 IQN）；业务主机组：关联业务主机的 IP 地址。提示 IQN（可选）、IP
                    业务主机：关联业务主机的 IQN 地址（同时配置了 IP 和 IQN）；业务主机组：关联业务主机的 IQN 地址（仅 IQN）。提示 IQN、IP（可选）
                    业务主机：关联业务主机的 IQN 地址（同时配置了 IP 和 IQN）；业务主机组：关联业务主机的 IQN 地址（同时配置了 IP 和 IQN）。提示 IQN 或 IP
                    业务主机不管以什么方式关联了 subsystem 或者 ns，都会要求配置 NQN
            该主机关联了存储资源，编辑启动器对存储资源白名单的影响
                该主机仅关联至 target，target 白名单为所选业务主机的 IP 地址
                    删除某个启动器中的 IP / 删除某个仅有 IP 的启动器后，target 关联的所有主机（组）仍仅均配置了 IP，target 白名单不变，该 IP 对应的客户端无法连接该 target
                    编辑/删除某个启动器中的 IQN / 某个仅有 IQN 的启动器，target 白名单前后端均不变，可连接该 target 的客户端不变
                    新增 IQN 后，target 关联的所有主机（组）仍仅均配置了 IP，target 白名单前后端均不变，可连接该 target 的客户端不变
                    新增 IQN 后，target 关联的所有主机（组）变为均配置了 IP 和 IQN，target 白名单变为所选业务主机的 IQN 地址
                    新增 IP，target 白名单不变，原有连接正常，新增 IP 对应客户端可连接至该 target
                    编辑 IP，target 白名单不变，修改前的 IP 对应的客户端无法连接 target，修改后的 IP 对应客户端可以连接 target
                该主机仅关联至 target，target 白名单为所选业务主机的 IQN 地址
                    添加/编辑/删除 IP，target 白名单不变，可连接该 target 的客户端不变
                    添加/编辑 IQN，target 白名单不变，新增/编辑后的 IQN 可以连接存储，编辑前的 IQN 无法再连接存储，其他连接正常
                    删除 IQN 后，target 关联的所有主机（组）变为仅均配置了 IP，target 白名单变为所选业务主机的 IP 地址
                    删除 IQN 后，target 关联的所有主机（组）仍为均配置了 IP 和 IQN，target 白名单不变，删除的 IQN 对应的客户端无法连接到 target
                该主机关联至 target 和 lun，target 白名单为所选业务主机的 IP 地址
                    IP 地址对应客户端的 IQN 地址在 lun 白名单中，编辑为其他 IP 或删除该 IP，该客户端无法连接到该 target 和 lun，编辑后的 IP 对应客户端 B 可连接到 target，但只有 B 的 IQN 在 lun 白名单中时才能连接到 lun
                    IP 地址对应客户端的 IQN 地址不在 lun 白名单中，编辑为其他 IP 或删除该 IP，该客户端无法连接到该 target，编辑后的 IP 对应客户端 B 可连接到 target，对 lun 的白名单和原有连接没有影响，只有 B 的 IQN 在 lun 白名单中时才能连接到 lun
                    删除 IQN，target 白名单不变，可连接该 target 的客户端不变，该 IQN 对应的客户端无法连接到该 LUN（区分之前可以连接到 LUN 和之前不可以连接到 LUN 的情况）
                    添加 IQN，target 白名单不变，可连接该 target 的客户端不变；新增 IQN 对应客户端的 IP 在 target IP 白名单中，该客户端可以连接到该 lun，否则该客户端仍无法连接到该 target 和 lun
                    编辑 IQN，target 白名单不变，可连接该 target 的客户端不变；编辑前的 IQN 对应客户端无法连接该 LUN，编辑后的 IQN 对应客户端的 IP 在 target 白名单中，可以连接到该 LUN，否则仍无法连接该 target 和 lun
                该主机关联至 target 和 lun，target 白名单为所选业务主机的 IQN 地址
                    添加/编辑/删除 IP，target / lun 白名单不变，可连接该 target / lun 的客户端不变
                    添加/编辑 IQN，target / lun 白名单不变，新增/编辑后的 IQN 可以连接存储，编辑前的 IQN 无法再连接存储，其他连接正常
                    删除 IQN，target / lun 白名单不变，删除的 IQN 对应的客户端无法连接到 target
                该主机关联至 subsystem / ns
                    添加/编辑/删除 IP/IQN，存储资源白名单不变，可连接存储的客户端不变
                    添加/编辑/删除 NQN，存储资源白名单不变，新增/编辑后的 NQN 可以连接存储，编辑前/被删除的 NQN 无法再连接存储，其他连接正常
        展示
            列表页
                入口：含 zbs 570 及以上的组织层/数据中心层，zbs 570 及以上集群层的导航栏中展示「业务主机」，常用功能（加星标），点击进入业务主机列表页
                「筛选框」——默认为「全部业务主机」，列表展示当前层级下所有业务主机
                「筛选框」——「下拉菜单」：当前层级没有业务主机时的展示，在当前层级下的集群创建业务主机组，查看下拉菜单展示，创建成功
                「筛选框」——「下拉菜单」：当前层级没有业务主机时，在不属于当前层级的集群创建业务主机组，查看下拉菜单展示，创建成功
                「筛选框」——「下拉菜单」：当前层级有业务主机时的展示，以集群为粒度，集群名称+主机组名称、描述
                「筛选框」——「下拉菜单」：当前层级有业务主机时，在当前层级下的集群创建业务主机组，查看下拉菜单展示，创建成功
                「筛选框」——「下拉菜单」：当前层级有业务主机，在不属于当前层级的集群创建业务主机组，查看下拉菜单展示，创建成功
                「筛选框」——选择「未加入业务主机组」：列表展示当前层级下所有未加入业务主机组的业务主机
                「筛选框」——选择「指定业务主机组」：列表展示加入该业务主机组的业务主机（当前层级下其他集群中存在同名业务主机组，检查展示）
                「筛选框」——选择「指定业务主机组」，该主机组描述不为空时，展示 info icon
                「筛选框」——选择「指定业务主机组」，展示 more button
                「列表页」——无业务主机时的展示
                「列表页」——「名称」，默认展示，可排序，不可取消展示
                「列表页」——「描述」，默认展示，可排序，可取消展示
                「列表页」——「所属业务主机组」，默认展示，不可排序，可取消展示
                「列表页」——「关联卷数」，默认展示，不可排序，可取消展示，包含关联的 LUN 和 ns 总数，去重
                「列表页」——「启动器数」，默认展示，可排序，可取消展示
                「列表页」——「所属集群」，仅在组织层/数据中心层默认展示，集群层不展示，不可排序，可取消展示，hover 变蓝，点击跳转至集群概览页
                「列表页」——「所属数据中心」，仅在组织层/数据中心层默认展示，集群层不展示，不可排序，可取消展示，hover 变蓝，点击跳转至数据中心概览页
                「列表页」——「标签」，默认不展示，不可排序，可选择展示
                「列表页」——「more btn」，每一行最右端展示，根据该主机是否加入主机组展示不同的功能菜单
                「列表页」——编辑单个主机
                「列表页」——将单个主机加入主机组
                「列表页」——将单个主机移出主机组
                「列表页」——编辑单个主机的标签
                「列表页」——删除单个主机
                「列表页」——多选框选中主机，列表上方展示功能按钮
                「列表页」——导出
            详情页
                业务主机列表中点击业务主机，进入详情页
                当前主机已加入主机组：展示「编辑」「加入业务主机组」「删除」，各项操作成功
                当前主机未加入主机组：展示「编辑」「移出业务主机组」「删除」，各项操作成功
                「详情」——描述，与创建时一致
                「详情」——「业务主机组」
                「详情」——「关联卷数」，计算所有关联的 lun 和 ns，去重
                「详情」——「启动器」，启动器分组展示，展示与配置一致
                「详情」——「启动器」，右上角展示「编辑」入口，编辑成功
                「详情」——「启动器」，右上角展示「^」，默认展开，可收起
                「关联卷」——无关联卷时展示「无关联卷」
                「关联卷」——仅关联了 LUN / ns，不展示 section，直接展示卷列表
                「关联卷」——同时关联了 LUN 和 ns，分 section 展示
                「关联卷」——列表，字段校验
                「关联卷」——列表——搜索框，展示正确，搜索结果正确（仅支持搜索卷名称）
                「关联卷」——列表，存储资源详情
            操作
                加入主机组
                    单个操作弹窗展示正确，小弹窗
                    单个操作——未选择主机组，禁止提交表单
                    单个操作——仅允许选择一个，再次选择被覆盖，加入成功
                    单个操作——选择的主机组关联了存储资源时，弹窗展示提示
                    批量操作——大弹窗展示正确，在集群/数据中心/tower 层级的业务主机列表均可以发起批量操作
                    批量操作——展示选中的主机数和可加入主机组的主机数。若选中的主机存在已加入主机组的，展示将跳过的数量，hover 逐个展示
                    批量操作——选择业务主机组，支持批量选择，存在多个集群时，每个集群列表提供一个「批量选择」入口，仅影响本集群内的业务主机
                    批量操作——存在业务主机未选择业务主机组时禁止提交表单
                    批量操作——分别为业务主机选择不同的主机组，表单提交成功
                    批量操作——当选择的主机组存在已关联存储资源的，表单提示：加入后，所属主机组的关联资源的白名单将包含选中的业务主机。
                    选择的主机组关联了存储资源，加入该主机组后，会发生的变化——所有场景下都会发生的变化
                    选择的主机组关联了存储资源，加入该主机组后，存储资源白名单变化
                    选择的主机组未关联存储资源，加入该主机组后，仅业务主机列表中以该业务组筛选得到的结果改变
                    所选主机关联存储资源，加入组不会影响连接，可正常使用
                    批量操作——批量选择，选中的主机组为空且未关联存储资源时，对表单中的业务主机启动器进行地址校验，无法加入同一个组则展示提示信息
                    批量操作——批量选择，选中的主机组为空但关联了 target，该 target 仅关联空主机组，表单地址校验
                    批量操作——批量选择，选中的主机组为空但关联了 lun，该 lun 及所属 target 仅关联空主机组，表单地址校验
                    批量操作——批量选择，选中的主机组为空但关联了 subsystem/ns，该存储资源仅关联空主机组，表单地址校验
                    批量操作——批量选择，选中的主机组未关联存储资源，组内主机均配置了多种类型地址，要求表单中选中的业务主机均配置最少一种相同类型的地址
                    「业务主机组」选择业务主机组时不可选择，hover 展示提示
                        所选组未关联存储资源，组内业务主机仅均配置了 IP，业务主机未配置 IP 不可选：该组内的业务主机均已配置 IP 启动器，当前业务主机未配置 IP 启动器
                        所选组未关联存储资源，组内业务主机仅均配置了 IQN，业务主机未配置 IQN 不可选：该组内的业务主机均已配置 IQN 启动器，当前业务主机未配置 IQN 启动器
                        所选组未关联存储资源，组内业务主机仅均配置了 NQN，业务主机未配置 NQN 不可选：该组内的业务主机均已配置 NQN 启动器，当前业务主机未配置 NQN 启动器
                        所选组未关联存储资源，组内业务主机仅均配置了 IP 和 IQN，业务主机仅配置 IP/IQN 或同时配置了 IP 和 IQN 均可选
                        所选组未关联存储资源，组内业务主机仅均配置了 IP 和 IQN，业务主机仅配置 NQN 不可选：该组内的业务主机均已配置 IQN、IP 启动器，当前业务主机未配置 IQN 或 IP 启动器
                        所选组未关联存储资源，组内业务主机仅均配置了 IP 和 NQN，业务主机仅配置 IQN 不可选：该组内的业务主机均已配置 NQN、IP 启动器，当前业务主机未配置 NQN 或 IP 启动器
                        所选组未关联存储资源，组内业务主机仅均配置了 IQN 和 NQN，业务主机仅配置 IP 不可选：该组内的业务主机均已配置 IQN、NQN 启动器，当前业务主机未配置 IQN 或 NQN 启动器
                        所选组未关联存储资源，组内业务主机均配置了 IP、IQN 和 NQN，业务主机不为空时均可选
                        所选组关联了 target，target 关联的业务主机（组）同时配置了 ip 和 IQN，业务主机仅配置 IP/IQN 或同时配置了 IP 和 IQN 时可选
                        所选组关联了 target，target 关联的业务主机（组）同时配置了 ip 和 IQN，业务主机仅配置 NQN 时不可选，提示：该组已关联 iSCSI target。关联 Target 的关联业务主机均已配置 IQN 和 IP 启动器，但当前业务主机未配置 IQN 或 IP 启动器。
                        所选组关联了 target，target 关联的业务主机（组）仅都配置了 IP，业务主机未配置 IP 时不可选，提示：该组已关联 iSCSI target。关联 Target 的关联业务主机均已配置  IP 启动器，但当前业务主机未配置 IP  启动器。
                        所选组关联了 target，target 关联的业务主机（组）仅都配置了 IQN，业务主机未配置 IQN 时不可选，提示：该组已关联 iSCSI target。关联 Target 的关联业务主机均已配置  IQN 启动器，但当前业务主机未配置 IQN  启动器。
                        所选组关联了 target，关联的 target 中存在仅配置了 IP 和仅配置了 IQN 的，业务主机未配置 IP 和 IQN 时不可选，提示：该组已关联 iSCSI target。关联 Target 的关联业务主机均已配置 IQN 或 IP 启动器，但当前业务主机未配置 IQN 和 IP 启动器。
                        所选组关联了 target，关联的 target 中存在仅配置了 IP 和同时配置了 IP 和 IQN 的，业务主机未配置 IP 时不可选，提示：该组已关联 iSCSI target。关联 Target 的关联业务主机均已配置 IP 启动器，但当前业务主机未配置 IP 启动器。
                        所选组关联了 target，关联的 target 中存在仅配置了 IQN 和同时配置了 IP 和 IQN 的，业务主机未配置 IQN 时不可选，提示：该组已关联 iSCSI target。关联 Target 的关联业务主机均已配置 IQN 启动器，但当前业务主机未配置 IQN 启动器。
                        所选组关联了 target，关联的 target 中存在仅配置了 IP、仅配置了 IQN 和同时配置了 IP 和 IQN 的，业务主机未配置 IP 和 IQN 时不可选，提示：该组已关联 iSCSI target。关联 Target 的关联业务主机均已配置 IQN 或 IP 启动器，但当前业务主机未配置 IQN 和 IP 启动器。
                        所选组关联了 lun，业务主机未配置 IQN 时不可选，提示：该组已关联 LUN，当前业务主机未配置 IQN 启动器。
                        所选组关联了 subsystem/ns，业务主机未配置 NQN 时不可选，提示：该组已关联 NVMe subsystem 或 Namespace，当前业务主机未配置 NQN 启动器。
                        所选组为空组，该组关联了一个 target，且该 target 仅关联了空组，业务主机仅配置了 NQN 不可选：该组已关联 iSCSI Target。关联 Target 仅关联了空的业务主机组，但当前业务主机未配置 IQN 或 IP 启动器。
                        所选组为空组，该组关联了 target，存在 target 仅关联该空组，也存在 target 关联了业务主机或非空主机组，仅根据后者展示提示信息
                        所选组关联存储资源，同时存在以上多种不可选情况时，折行展示多种原因
                移出主机组
                    单个操作——弹窗展示正确
                    当存在选择的业务主机所属组关联了存储资源时，展示提示信息：无法访问
                    批量操作——全部可执行，弹窗展示正确
                    批量操作——部分可执行，展示选中的业务主机总数，可移出的主机数，跳过的主机数
                    批量操作——移出不同主机组的主机，成功
                    批量操作——移出不同集群主机组的主机，成功
                    批量操作——将一个主机组中的所有主机移出，成功
                    所属组关联了存储资源，移出主机组后会发生的变化 ——所有场景下都会发生的变化
                    所属组关联了存储资源，移出主机组，存储资源白名单变化
                    所属组未关联存储资源，移出主机组后，仅业务主机列表中以该业务组筛选得到的结果改变
                    所选主机关联存储资源，移出组不会影响连接，可正常使用
                删除
                    单个删除——该主机未加入组，同时未关联存储资源，删除成功，弹窗展示正确
                    单个删除——该主机加入了组，但主机组和该主机均未关联存储资源，删除成功，弹窗展示正确
                    单个删除——该主机仅通过所属主机组关联了存储资源，不可被删除，弹窗仅展示「其所属业务主机组存在关联的存储资源。。。。。。」
                    单个删除——仅该主机自身关联了存储资源，不可被删除，弹窗仅展示该主机本身关联的存储资源列表
                    单个删除——该主机自身和所属组均关联了存储资源，不可被删除，弹窗同时展示提示和该主机本身关联的存储资源列表
                    批量删除——全部可删除，弹窗展示选中的业务主机总数，hover 逐个展示
                    批量删除——部分可删除，展示选中的业务主机总数，可删除的主机数（hover 逐个展示），跳过的主机数
                    批量删除——部分可删除，展示无法删除的原因
                    批量删除——全部不可删除，逐个展示原因
                    单个删除成功
                    批量删除，全部可删除时，删除成功
                    批量删除，部分可删除时，删除成功
        任务和事件
            创建业务主机
            编辑业务主机
            删除单个业务主机
            批量删除业务主机
            将单个业务主机加入业务主机组
            将多个业务主机加入业务主机组
            将单个业务主机移出业务主机组
            将多个业务主机移出业务主机组
    target
        创建
            创建表单，顺序调整：先「白名单」，后「登录认证」
            表单默认选中「使用业务主机」，不启用「自适应」，不选择任何主机（组），IP 和 IQN 白名单展示正确
            仅选择「使用业务主机」且未选择任何主机/主机组时，展示无法访问的提示信息
            「资源选择列表」默认展示为「业务主机」，展示当前集群中的所有业务主机，当前集群中存在/不存在业务主机时，展示正确
            「资源选择列表」——「搜索框」，仅支持搜索业务主机/主机组名称
            「资源选择列表」——「全选」，当前列表中存在仅配置了 IP 和仅配置了 IQN 的业务主机时，全选不可点击
            「业务主机列表」——选择业务主机，右侧点击被选中，再次点击取消被选中，列表右上角展示已选择的业务主机数
            「业务主机列表」——选择业务主机，无法被选择的场景
            「业务主机列表」——「预览」，未选择业务主机/主机组时，禁用「预览」；已选择业务主机/主机组，点击「预览」查看关联业务主机详情
            「业务主机列表」——「全选」，无业务主机时不可用；有业务主机时，全选会选中当前页的所有可选项；点击「全选」后，右上角变为「取消全选」
            「业务主机组列表」，无业务主机组时，展示「无业务主机组」
            「业务主机组列表」，有业务主机组时，folder 形式分组展示，默认收起，点击可展开，主机组为空/不为空时展示正确
            「业务主机组列表」——选择业务主机组，右侧点击被选中，再次点击取消被选中，列表右上角展示已选择的业务主机组数
            「业务主机组列表」——选择业务主机组，无法被选择的场景
            「业务主机组列表」——「预览」，未选择业务主机/主机组时，禁用「预览」；已选择业务主机/主机组，点击「预览」后展示与主机列表中一致
            「业务主机组列表」——「全选」，无业务主机组时不可用；有业务主机组时，全选会选中当前页的所有可选项；点击「全选」后，右上角变为「取消全选」
            「IP/IQN 白名单」使用业务主机 + 不启用自适应，不选择主机（组），IP 白名单为全部禁止，IQN 白名单为所选业务主机的 IQN 地址
            「IP/IQN 白名单」使用业务主机 + 不启用自适应，已选择主机（组）
            使用业务主机 + 启用自适应，不展示资源选择列表，IP 全部允许，IQN 自适应
            选择「手动配置」，默认 IP 白名单为全部允许，IQN 白名单为自适应
            选择「手动配置」，IP/IQN 白名单选为全部禁止，则展示无法访问的提示，否则不展示
            「登录认证」使用业务主机 + 不启用自适应，仅支持配置 Target CHAP，默认不勾选，勾选后展示名称和密码的输入框
            「登录认证」其他白名单配置方式下，密码默认展示为密文，点击右侧可切换为明文，其他无变化
            使用业务主机 + 启用自适应，配置 initiator chap 和 target chap，创建均成功
            手动配置白名单时，配置 initiator chap 和 target chap，创建均成功
            使用业务主机 + 不启用自适应，配置 target chap 成功
        编辑
            target 使用业务主机 + 不启用自适应，增减主机组
                增加业务主机（组）——原有业务主机（组）均已配置 IP 和 IQN，增加了一个仅配置了 IP 的业务主机
                增加业务主机（组）——原有业务主机（组）均已配置 IP 和 IQN，增加了一个仅配置了 IQN 的业务主机组：包含 2 个业务主机
                增加业务主机（组）——原有业务主机（组）仅均配置 IP，增加了一个配置了 IP 的业务主机（组）
                增加业务主机（组）——选择业务主机，无法被选择的场景
                增加业务主机后，在该 target 中创建 lun，业务主机选择列表中将展示该业务主机（组）
                移除业务主机（组）——原有业务主机（组）仅均配置了 IP，移除唯一一个没有配置 IQN 的业务主机
                移除业务主机（组）——原有业务主机（组）仅均配置了 IP，移除其中一个配置了 IP 的主机（组）
                移除业务主机（组）——原有业务主机（组）均配置了 IQN，移除一个配置 IQN 的业务主机
                移除业务主机（组）——移除空主机组
                移除业务主机（组）——主机（组）被 target 中的卷单独关联，编辑时禁止取消选择，hover 展示关联卷列表
                移除业务主机后，在该 target 中创建 lun，业务主机选择列表中将不再展示该业务主机（组）
                移除业务主机（组），创建时禁止添加的主机（组），编辑前若已经被选中，允许移除，表单提交后禁止在此勾选
            target 使用业务主机，改变配置方式
                自适应：不启用 --> 启用，存在卷白名单为与父级资源一致，禁止启用自适应，展示提示信息，hover 展示白名单为「与父级资源一致」的卷
                自适应：不启用 --> 启用，不存在卷白名单为与父级资源一致，允许启用自适应
                自适应：不启用 --> 启用，创建卷的表单变化
                自适应：启用 --> 不启用，target 内所有卷均使用业务主机，允许关闭自适应，表单中展示业务主机选择列表，自动选择 target 内卷已关联业务主机的并集
                自适应：启用 --> 不启用，initiator CHAP 变化
                自适应：启用 --> 不启用，创建卷的表单变化
                自适应：启用 --> 不启用，target 内存在 LUN 白名单为手动配置，禁止关闭自适应，hover 展示手动配置白名单的卷
                使用业务主机 --> 手动配置，target 中存在卷白名单使用业务主机，禁止改为手动配置，展示提示，hover 逐个展示使用业务主机的卷
                使用业务主机 --> 手动配置，target 中不存在卷白名单使用业务主机，允许改为手动配置
                使用业务主机 --> 手动配置，创建卷的表单变化
            target 为手动配置
                改为使用业务主机，存在 LUN 使用手动配置，默认选择自适应，禁止取消，编辑成功后原有连接不受影响
                改为使用业务主机，不存在 LUN 使用手动配置，选择启用自适应成功
                改为使用业务主机，不存在 LUN 使用手动配置，取消勾选自适应，选择指定业务主机后编辑成功
                改为使用业务主机，创建卷的表单变化
                未启用自适应 + 指定 IQN，IQN 被 target 中的卷单独关联，禁止删除/编辑，展示提示。存在多个被卷单独关联的 IQN 时的展示
                未启用自适应 + 指定 IQN，编辑/删除未被 target 中的卷单独关联的 IQN，成功，仅 target 白名单变化
                自适应：不启用 --> 启用，存在卷为「全部允许」，展示提示，hover 逐个展示全部允许的卷
                自适应：不启用 --> 启用，不存在「全部允许」的卷，原有配置不受影响
                自适应/全部允许 --> 指定 IQN，自动填充 target 内卷的指定 IQN 并集
                自适应/全部允许 --> 指定 IQN，并增加 IQN，编辑成功，仅 target 白名单变化
                IQN 白名单编辑为「全部禁止」，存在卷白名单不是全部禁止，禁止选择全部禁止，hover info icon 展示不是全部禁止的卷
                IQN 白名单编辑为「全部禁止」，所有卷白名单中都是全部禁止，选择全部禁止，编辑成功
        列表页
            新增「关联业务主机数」字段，默认展示，在「IP 白名单」前，不支持排序
            「关联业务主机数」——target 白名单为使用业务主机，展示具体数量，包含主机组中的主机，去重
            「关联业务主机数」——target 白名单为手动配置，展示「未使用业务主机」
            「Target CHAP」——原名称为「CHAP」，取值：未启用/已启用
            「活跃连接数」——新增字段，默认展示，在「LUN 数」前，不支持排序
            「列表页」——导出
        详情页——「访问设置」
            字段展示顺序：访问模式，白名单配置方式，IP 白名单，IQN 白名单，Initiator CHAP，Target CHAP
            白名单配置方式为手动配置，字段展示和创建时一致，initiator CHAP 和 target CHAP 中不展示密码
            target 关联主机/主机组时，详情页的白名单配置方式行右侧会展示「详情」，点击查看关联主机详情
            使用业务主机 + 不启用自适应 + 已关联主机（组），关联的主机（组）中所有主机仅均配置了 IP，IP 白名单为「关联业务主机的 IP 地址」，IQN 白名单为「全部允许」
            使用业务主机 + 不启用自适应 + 已关联主机（组），关联的主机（组）中所有主机均配置了 IQN，IQN 白名单为「关联业务主机的 IQN 地址」，IP 白名单为「全部允许」
            使用业务主机 + 不启用自适应 + 未关联主机（组），IP 白名单为「全部禁止」，IQN 白名单为「关联业务主机的 IQN 地址」
            使用业务主机 + 不启用自适应 ，「Initiator CHAP」展示下划线，hover 展示提示，自动填充为 target 关联业务主机中设置的所有 initiator chap 并集
            使用业务主机 + 启用自适应 ，IP 白名单：「全部允许」，IQN 白名单：「自适应」+ 下方提示信息，Initiator CHAP 启用时分组展示每个 IQN + 名称，未启用则展示为「_」
            target 仅关联空主机组时，target 详情页中 IP 白名单为全部禁止，IQN 白名单为「关联业务主机的 IQN 地址」，白名单配置方式中展示「详情」，点击可查看关联的业务主机组
            「Target CHAP」，启用时展示「已启用」+ 名称，未启用则展示「未启用」
        事件
            创建使用业务主机的 target，事件展示与创建时一致
            创建手动配置的 target，事件展示与创建时一致
            编辑使用业务主机的 target，事件展示与编辑前后的配置一致
            编辑手动配置的 target，事件展示与编辑前后的配置一致
            事件中不展示 chap 的密码
    LUN
        创建
            创建 lun 的表单中「所属 Target 的 IP/IQN 白名单」与 target 的 IP/IQN 白名单一致，为「关联业务主机的 IP/IQN 地址」时，下方展示提示信息，点击「详情」可查看关联业务主机详情
            target 使用业务主机 + 启用自适应，卷白名单默认选择「使用业务主机」，展示业务主机选择列表，列表中展示集群内所有的业务主机（组）
            target 使用业务主机 + 启用自适应，卷白名单选择「手动配置」，不展示业务主机选择列表，IQN 白名单与之前版本一致，创建成功后，LUN 详情页展示与创建时一致
            target 未启用自适应 + 已关联主机（组），默认勾选「与所属 Target 一致」，不展示业务主机选择列表，IQN 白名单为全部允许
            target 未启用自适应 + 已关联主机（组），取消勾选「与所属 Target 一致」，展示业务主机选择列表，列表中仅展示 target 已关联的业务主机（组），不自动选中任何项
            target 使用业务主机 + 未启用自适应 + 未关联主机（组），创建 lun
            target 使用业务主机 + 未启用自适应 + 仅关联空主机组，创建 lun
            创建 lun 时的业务主机选择列表，不可选择场景
            target 白名单为「所选业务主机的 IP 地址」时，只有 lun 所选 IQN 对应客户端的 ip 在 target 白名单中的客户端可连接该 lun
            target 白名单为「所选业务主机的 IQN 地址」时，lun 白名单中 IQN 对应客户端均可连接该 lun
            target 手动配置 + IQN 全部允许/自适应，创建卷时默认选择「手动配置」，禁止选择「使用业务主机」，展示提示信息
            target 手动配置 + 指定 IQN，创建卷时不展示「白名单配置方式」字段，选择「全部允许」创建成功，连通性检查
            target 手动配置 + 指定 IQN，创建卷时不展示「白名单配置方式」字段，选择「全部禁止」创建成功，连通性检查
            target 手动配置 + 指定 IQN，创建卷时不展示「白名单配置方式」字段，选择「允许指定 IQN」，所属 target 的 IQN 白名单仅有一个对象时，卷白名单自动填充该值，并禁止编辑，展示提示
            target 手动配置 + 指定 IQN，选择「允许指定 IQN」，所属 target 的 IQN 白名单有 >1 个对象时，仅允许填入 target 白名单中的 IQN 地址
            target 手动配置 + 仅 IP 白名单为全部禁止，卷的 IQN 白名单可正常进行配置，表单中会展示无法访问的提示，创建成功，该卷无法访问
            target 手动配置 + IQN 白名单为全部禁止，卷的 IQN 白名单默认为「全部禁止」，不可编辑，表单展示无法访问的提示，创建成功，该卷无法访问
        编辑
            target 使用业务主机 + 启用自适应 + 卷使用业务主机，未选择主机（组）--> 选择业务主机（组），IQN 白名单变为「所选业务主机的 IQN 地址」，无法访问提示消失
            target 使用业务主机 + 启用自适应 + 卷使用业务主机，未选择主机（组）--> 改为「手动配置」，成功
            target 使用业务主机 + 启用自适应 + 卷使用业务主机，已选择主机（组）--> 增减业务主机（组），编辑成功，检查白名单展示和连通性
            target 使用业务主机 + 启用自适应 + 卷使用业务主机，已选择主机（组）--> 改为「手动配置」，成功，已选择的主机（组）被清空
            target 使用业务主机 + 启用自适应 + 卷手动配置，更改为使用业务主机，编辑成功
            target 使用业务主机 + 未启用自适应 + 已关联主机（组），卷勾选「与所属 Target 一致」--> 取消勾选，展示业务主机选择列表，表中仅展示 target 关联的主机（组），自动勾选所有可选项，编辑成功
            target 使用业务主机 + 未启用自适应 + 已关联主机（组），卷未勾选「与所属 Target 一致」--> 增减已选择的业务主机（组），可清空
            target 使用业务主机 + 未启用自适应 + 已关联主机（组），卷未勾选「与所属 Target 一致」--> 勾选，不展示业务主机选择列表，编辑成功
            target 使用业务主机 + 未启用自适应 + 未关联主机（组），编辑 target 关联主机后，选择「与所属 Target 一致」的卷白名单同步变化，连通性变化
            target 手动配置白名单 + 全部允许/自适应，展示白名单配置方式，但禁止选择「使用业务主机」，target 选择指定 IQN / 全部禁止，不展示「白名单配置方式」
            target 手动配置白名单 + 允许指定 IQN + 白名单中仅有一个 IQN，卷为指定 IQN 时禁止添加/编辑/删除 IQN
            target 手动配置白名单 + 允许指定 IQN + 白名单中仅有一个 IQN，卷的白名单可以在三种模式下切换，选择「指定 IQN」时默认填充 target 唯一的 IQN，禁止编辑
            target 手动配置白名单 + 允许指定 IQN + 白名单中有 >1 个 IQN，卷白名单在 target 白名单范围内增减 IQN，成功，增加 target 未关联的 IQN，失败
            target 手动配置白名单 + IQN 白名单为全部禁止，禁止编辑卷白名单。编辑 target IQN 白名单不为全部禁止后，可编辑卷白名单
            lun 使用业务主机时，仅关联空主机组，编辑时弹窗展示提示信息，允许取消关联
        列表页
            「关联业务主机数」——新增字段，默认在「存储使用率」后，不支持排序，展示关联的业务主机数，包括主机组内主机，去重。未使用业务主机时展示「未使用业务主机」
            「列表页」——导出
        快照/克隆
            克隆/从快照重建卷时，选择父级资源的下拉框，去掉子级资源的数量展示，新增父级资源的白名单展示
            单个卷的克隆/从快照重建，选择的父级资源为「使用业务主机 + 未启用自适应」，重建成功
            单个卷的克隆/从快照重建，选择的父级资源为「使用业务主机 + 已启用自适应」，重建成功
            单个卷的克隆/从快照重建，选择的父级资源为「手动配置 + 自适应」，重建成功
            单个卷的克隆/从快照重建，选择的父级资源为「手动配置 + 全部允许」，重建成功
            单个卷的克隆/从快照重建，选择的父级资源为「手动配置 + 指定 IQN」，重建成功
            单个卷的克隆/从快照重建，选择的父级资源为「手动配置 + 全部禁止」，重建成功
            从一致性快照组/卷快照计划快照组重建卷，表单新增常驻提示
            从一致性快照组/卷快照计划快照组重建卷，选择不同的父级资源，新卷白名单设置正确
            从快照回滚卷，不改变当前卷的白名单设置
        事件
            创建使用业务主机的 lun，事件展示与创建时一致
            创建手动配置的 lun，事件展示与创建时一致
            编辑使用业务主机的 lun，事件展示与编辑前后的配置一致
            编辑手动配置的 lun，事件展示与编辑前后的配置一致
    subsystem
        创建
            表单默认展示
            业务主机选择列表，除无法选择业务主机（组）的条件之外，其他与创建 target 时一致
            业务主机选择列表——未配置 NQN，或已选择数量达到上限时不可选择业务主机，单个原因/多个原因的展示
            业务主机组选择列表——无业务主机/包含未配置 NQN 启动器的业务主机/已选择数量达到上限时不可选择业务主机，单个原因/多个原因的展示
            使用业务主机 + 不启用自适应，选择主机（组），IP 白名单为全部允许，NQN 白名单为所选业务主机的 NQN 地址
            使用业务主机 + 不启用自适应，未选择主机（组），IP 白名单为全部禁止，NQN 白名单为所选业务主机的 NQN 地址，展示无法访问提示
            使用业务主机 + 不启用自适应，仅选择空组，IP 白名单为全部禁止，NQN 白名单为所选业务主机的 NQN 地址，展示无法访问提示
            使用业务主机 + 启用自适应，不展示业务主机（组）选择列表，IP 白名单为全部允许，NQN 白名单为自适应
            手动配置，表单与不支持主机组时一致。IP 或 NQN 白名单为全部禁止时，展示无法访问提示
        编辑
            subsystem 使用业务主机 + 不启用自适应，仅支持增加全部配置了 NQN 启动器的业务主机（组），编辑成功
            subsystem 使用业务主机 + 不启用自适应，移除未被 ns 单独关联的业务主机（组），编辑成功。仅 subsystem 白名单变化，关联主机数减少
            subsystem 使用业务主机 + 不启用自适应，被 ns 单独关联的业务主机（组），禁止取消选择，hover 展示已加入以下 Namespace 的白名单
            subsystem 使用业务主机 + 不启用自适应，允许移除空主机组
            subsystem 使用业务主机，自适应：不启用 --> 启用，存在选择与所属 subsystem 一致的 ns 时，禁止勾选自适应，提示信息展示选择与父级一致的卷，hover 逐个展示
            subsystem 使用业务主机，自适应：不启用 --> 启用，不存在选择与所属 subsystem 一致的 ns，允许勾选自适应，业务主机选择列表取消展示，IP 白名单：全部允许，NQN 白名单：自适应
            subsystem 使用业务主机，自适应：启用 --> 不启用，subsystem 内的 ns 全部使用业务主机，允许关闭自适应，展示业务主机选择列表，列表自动选中 subsystem 中卷已关联业务主机的并集
            subsystem 使用业务主机，自适应：启用 --> 不启用，subsystem 中存在 ns 白名单为手动配置，禁止关闭自适应，提示信息展示白名单为手动配置的卷，hover 逐个展示
            subsystem 使用业务主机，改为手动配置，subsystem 内存在 ns 使用业务主机，禁止改为手动配置，提示信息展示使用业务主机的卷，hover 逐个展示
            subsystem 使用业务主机，改为手动配置，subsystem 内不存在 ns 使用业务主机，改为手动配置成功
            subsystem 手动配置，改为使用业务主机，存在 ns 使用手动配置，默认选择自适应，禁止取消，编辑成功，原有连接不受影响
            subsystem 手动配置，改为使用业务主机，不存在使用手动配置的 ns，自适应可选，开启/不开启自适应，编辑成功，原有连接不受影响
            subsystem 手动配置 + 允许指定 NQN，选择开启自适应，编辑成功，subsystem 白名单展示变化，ns 的连接不受影响
            subsystem 手动配置 + 允许指定 NQN，NQN 已被其中的卷单独关联，禁止编辑，禁止移除，输入框下展示提示信息
            subsystem 手动配置 + 允许指定 NQN，编辑/删除未被其中的卷单独关联的 NQN，编辑成功，仅 subsystem 白名单变化
            subsystem 手动配置 + NQN 白名单为自适应/全部允许，编辑为指定 NQN，自动填充其中卷的白名单并集
            subsystem 手动配置，存在卷白名单不是全部禁止，禁止将 subsystem NQN 白名单编辑为全部禁止，展示 info icon，hover 展示不是全部禁止的卷
            subsystem 手动配置，所有卷都为全部禁止/ subsystem 为空，可以选择全部禁止，选择后出现无法访问提示，编辑成功
        列表页
            新增「关联业务主机数」字段，默认展示，在「IP 白名单」前，不支持排序
            「关联业务主机数」——subsystem 白名单为使用业务主机，展示具体数量，包含主机组中的主机，去重
            「关联业务主机数」——subsystem 白名单为手动配置，展示「未使用业务主机」
            「活跃连接数」——新增字段，默认展示，在「Namespace 数」前，不支持排序
            「列表页」——导出
        详情页
            字段展示顺序：白名单配置方式，IP 白名单，NQN 白名单
            白名单配置方式为手动配置，字段展示和创建时一致
            使用业务主机 + 不启用自适应 + 已关联主机（组），IP 白名单：全部允许，NQN 白名单：「关联业务主机的 NQN 地址」
            使用业务主机 + 不启用自适应 + 未关联主机（组），IP 白名单：「全部禁止」，NQN 白名单：「关联业务主机的 NQN 地址」
            使用业务主机 + 启用自适应 ，IP 白名单：「全部允许」，NQN 白名单：「自适应」+ 下方提示信息
            subsystem 仅关联空主机组，详情页中 IP 白名单为全部禁止，NQN 白名单为关联业务主机的 NQN 地址，「白名单配置方式」行展示「详情」，可查看关联的主机组
            subsystem 关联主机/主机组时，在白名单配置方式行右侧展示「详情」入口，点击查看关联业务主机详情
        事件
            创建使用业务主机的 subsystem，事件展示与创建时一致
            创建手动配置的 subsystem，事件展示与创建时一致
            编辑使用业务主机的 subsystem，事件展示与编辑前后的配置一致
            编辑手动配置的 subsystem，事件展示与编辑前后的配置一致
    namespace
        创建
            创建 ns 的表单中「所属 Subsystem 的 IP/NQN 白名单」与 subsystem 的 IP/NQN 白名单一致，为「关联业务主机的 NQN 地址」时，下方展示提示信息，点击「详情」可查看关联业务主机详情
            subsystem 使用业务主机 + 启用自适应，卷白名单默认选择「使用业务主机」，展示业务主机选择列表，列表中展示集群内所有的业务主机（组）
            subsystem 使用业务主机 + 启用自适应，卷白名单选择「手动配置」，不展示业务主机选择列表，NQN 白名单与之前版本一致，创建成功后，ns 详情页展示与创建时一致
            subsystem 未启用自适应 + 已关联主机（组），默认勾选「与所属 Subsystem 一致」，不展示业务主机选择列表，NQN 白名单为关联业务主机的 NQN 地址
            subsystem 未启用自适应 + 已关联主机（组），取消勾选「与所属 Subsystem 一致」，展示业务主机选择列表，列表中仅展示 subsystem 已关联的业务主机（组），默认勾选所有可选项
            subsystem 使用业务主机 + 未启用自适应 + 未关联主机（组），创建 ns
            subsystem 使用业务主机 + 未启用自适应 + 仅关联空组，创建 ns
            创建 ns 时的业务主机选择列表，不可选择场景
            subsystem 手动配置 + NQN 全部允许/自适应，创建卷时默认选择「手动配置」，禁止选择「使用业务主机」，展示提示信息
            subsystem 手动配置 + 指定 NQN，创建卷时不展示「白名单配置方式」字段，选择「全部禁止」创建成功，连通性检查
            subsystem 手动配置 + 指定 NQN，创建卷时不展示「白名单配置方式」字段，默认选择「允许指定 NQN」，所属 subsystem 的 NQN 白名单仅有一个对象时，卷白名单自动填充该值，并禁止编辑，展示提示
            subsystem 手动配置 + 指定 NQN，选择「允许指定 NQN」，所属 subsystem 的 NQN 白名单有 >1 个对象时，仅允许填入 subsystem 白名单中的 NQN 地址
            subsystem 手动配置 + 仅 IP 白名单为全部禁止，卷的 NQN 白名单可正常进行配置，表单中会展示无法访问的提示，创建成功，该卷无法访问
            subsystem 手动配置 + NQN 白名单为全部禁止，卷的 NQN 白名单默认为「全部禁止」，不可编辑，表单展示无法访问的提示，创建成功，该卷无法访问
        编辑
            subsystem 使用业务主机 + 启用自适应 + 卷使用业务主机，未选择主机（组）--> 选择业务主机（组），NQN 白名单变为「所选业务主机的 NQN 地址」，无法访问提示消失
            subsystem 使用业务主机 + 启用自适应 + 卷使用业务主机，未选择主机（组）--> 改为「手动配置」，成功
            subsystem 使用业务主机 + 启用自适应 + 卷使用业务主机，已选择主机（组）--> 增减业务主机（组），编辑成功，检查白名单展示和连通性
            subsystem 使用业务主机 + 启用自适应 + 卷使用业务主机，已选择主机（组）--> 改为「手动配置」，成功，已选择的主机（组）被清空
            subsystem 使用业务主机 + 启用自适应 + 卷手动配置，更改为使用业务主机，编辑成功
            subsystem 使用业务主机 + 未启用自适应 + 已关联主机（组），卷勾选「与所属 Subsystem 一致」--> 取消勾选，展示业务主机选择列表，表中仅展示 subsystem 关联的主机（组），选中所有可选项，编辑成功
            subsystem 使用业务主机 + 未启用自适应 + 已关联主机（组），卷未勾选「与所属 Subsystem 一致」--> 增减已选择的业务主机（组），可清空
            subsystem 使用业务主机 + 未启用自适应 + 已关联主机（组），卷未勾选「与所属 Subsystem 一致」--> 勾选，不展示业务主机选择列表，编辑成功
            subsystem 使用业务主机 + 未启用自适应 + 未关联主机（组），编辑 subsystem 关联主机后，选择「与所属 Subsystem 一致」的卷白名单同步变化，连通性变化
            subsystem 手动配置白名单 + 全部允许/自适应，展示白名单配置方式，但禁止选择「使用业务主机」，subsystem 选择指定 NQN / 全部禁止，不展示「白名单配置方式」
            subsystem 手动配置白名单 + 允许指定 NQN + 白名单中仅有一个 NQN，卷为指定 NQN 时禁止添加/编辑/删除 NQN
            subsystem 手动配置白名单 + 允许指定 NQN + 白名单中仅有一个 NQN，可在两种模式中切换，选择「指定 NQN」时默认填充 subsystem 唯一的 NQN，禁止编辑
            subsystem 手动配置白名单 + 允许指定 NQN + 白名单中有 >1 个 NQN，卷白名单在 subsystem 白名单范围内增减 NQN，成功，增加 subsystem 未关联的 NQN，失败
            subsystem 手动配置白名单 + NQN 白名单为全部禁止，禁止编辑卷白名单。编辑 subsystem NQN 白名单不为全部禁止后，可编辑卷白名单
            使用业务主机的 ns，移除空主机组成功
        列表页和详情页
            「关联业务主机数」——新增字段，默认在「存储使用率」后，不支持排序，展示关联的业务主机数，包括主机组内主机，去重。未使用业务主机时展示「未使用业务主机」
            「列表页」——导出
        快照/克隆
            克隆/从快照重建卷时，选择父级资源的下拉框，去掉子级资源的数量展示，新增父级资源的白名单展示
            单个卷的克隆/从快照重建，选择的父级资源为「使用业务主机 + 未启用自适应」，重建成功
            单个卷的克隆/从快照重建，选择的父级资源为「使用业务主机 + 已启用自适应」，重建成功
            单个卷的克隆/从快照重建，选择的父级资源为「手动配置」，重建成功
            从一致性快照组/卷快照计划快照组重建卷，表单新增常驻提示
            从一致性快照组/卷快照计划快照组重建卷，选择不同的父级资源，新卷白名单设置正确
            从快照回滚卷，不改变当前卷的白名单设置
        事件
            创建使用业务主机的 ns，事件展示与创建时一致
            创建手动配置的 ns，事件展示与创建时一致
            编辑使用业务主机的 ns，事件展示与编辑前后的配置一致
            编辑手动配置的 ns，事件展示与编辑前后的配置一致
    活跃连接列表
        入口：集群层「活跃连接」，target/subsystem 详情页切换 tab 可进入活跃连接列表
        「客户端标识符」——新增字段，默认展示，在「客户端端口」后，为客户端的 IQN/NQN，支持排序
        「业务主机」——新增字段，默认展示，在「客户端标识符」后，不支持排序，不存在时展示为空，存在时点击可跳转至该业务主机详情页
        「业务主机」——客户端仅标识符/仅 IP 在业务主机的启动器中，展示对应的业务主机
        「业务主机」——客户端的 IP 和标识符在不同的业务主机中，仅展示标识符所属业务主机
        「所属业务主机组」——新增字段，默认展示，在「业务主机」后，不支持排序
        「所属业务主机组」——业务主机属于某个主机组，存储资源仅关联了该业务主机，业务主机组仍会展示所属的主机组，与是否关联无关。未加入组时展示为空
        lun 手动配置白名单时指定 IQN A，将 IQN A 配置到某个业务主机中或从业务主机中移出，活跃连接列表中的「业务主机」同步变化
        lun 直接关联了业务主机 A，将 A 加入主机组或从主机组移出，活跃连接列表中的「业务主机组」同步变化
        「列表页」——导出
    权限管理
        新增权限：业务主机（组）管理，没有该权限禁止创建/编辑/删除业务主机（组），但创建资源时可以选择使用业务主机
    升级
        升级前为存储资源设置了白名单，升级后不编辑可以正常使用
        升级前各种白名单的存储资源，升级后编辑为使用业务主机，编辑成功后可以正常使用
        升级后创建新的存储资源，并使用业务主机配置白名单，创建成功，可以正常使用
    cli
        前后端同步：一端操作后，另一端同步变化
        业务主机 cli
            zbs-meta host list
            zbs-meta host list_by_group
            zbs-meta host list_by_group_id
            zbs-meta host show
            zbs-meta host show_by_id
            zbs-meta host create
            zbs-meta host delete
            zbs-meta host delete_by_id
            zbs-meta host batch_delete_by_id
            zbs-meta host update
            zbs-meta host batch_add_hosts_to_group
            zbs-meta host batch_remove_hosts_from_group
        业务主机组 cli
            zbs-meta host_group list
            zbs-meta host_group show
            zbs-meta host_group show_by_id
            zbs-meta host_group create
            zbs-meta host_group delete
            zbs-meta host_group delete_by_id
            zbs-meta host_group update
        存储资源相关 cli
            zbs-iscsi target create
            zbs-iscsi target update，更新白名单，更新 target CHAP
            zbs-iscsi target show --show_chap，target 在所有配置下均生效
            zbs-iscsi intiator_chap create，target 为使用业务主机 + 不启用自适应时不生效
            zbs-iscsi initiator_chap update，target 为使用业务主机 + 不启用自适应时不生效
            zbs-iscsi initiator_chap remove，target 为使用业务主机 + 不启用自适应时不生效
            zbs-iscsi lun create
            zbs-iscsi lun update
            zbs-iscsi lun add_allowed_initiators，lun 使用业务主机时不生效
            zbs-iscsi lun remove_allowed_initiators，lun 使用业务主机时不生效
            zbs-iscsi lun clone，同 UI
            zbs-nfs file convert_from_lun，使用业务主机的 lun 转换成功
            zbs-nvmf subsystem create
            zbs-nvmf subsystem update
            zbs-nvmf ns create
            zbs-nvmf ns update
            zbs-nvmf ns clone
            zbs-iscsi lun move
                src target 使用业务主机 + 自适应，lun 使用业务主机，dst target 使用业务主机 + 自适应，move 成功，lun 白名单不变，两个 target 白名单均发生变化
                src target 使用业务主机 + 自适应，lun 使用业务主机，dst target 使用业务主机 + 不启用自适应，lun 关联的业务主机（组）均在 dst target 白名单中，move 成功，lun 白名单无变化。仅 src target 白名单变化
                src target 使用业务主机 + 自适应，lun 使用业务主机，dst target 使用业务主机 + 不启用自适应，lun 关联的业务主机（组）存在不在 dst target 白名单中的，move 失败
                src target 使用业务主机 + 不启用自适应，lun 与所属 Target 一致，dst target 使用业务主机 + 自适应，move 失败
                src target 使用业务主机 + 不启用自适应，lun 与所属 Target 一致，dst target 使用业务主机 + 不启用自适应，move 成功。target 白名单均无变化，lun白名单在后端均为全部允许，但前端详情页中的关联主机详情变化，lun 连通性变化
                src target 使用业务主机 + 不启用自适应，lun 未选择与所属 Target 一致，dst target 使用业务主机 + 不启用自适应：lun 关联的业务主机均在 dst target 白名单中，move 成功，白名单均不变
                src target 使用业务主机 + 不启用自适应，lun 未选择与所属 Target 一致，dst target 使用业务主机 + 不启用自适应：lun 关联的业务主机存在不在 dst target 白名单中的，move 失败
                lun 使用业务主机，dst target 手动配置，move 失败
                lun 手动配置，dst target 使用业务主机 + 自适应，move 成功，lun 白名单不变，dst target 白名单变化，若 src target 开启了自适应，白名单也会变
                lun 手动配置，dst target 手动配置 + 自适应，move 成功，lun 白名单不变，dst target 白名单变化，若 src target 开启了自适应，白名单也会变
                lun 手动配置，dst target 手动配置 + 指定 IQN + lun 指定 IQN，lun 白名单中 IQN 全部都在 dst target 白名单中，move 成功，lun 白名单不变，dst target 白名单不变，若 src target 开启了自适应，白名单也会变
                lun 手动配置，dst target 手动配置 + 指定 IQN + lun 指定 IQN，lun 白名单中 IQN 存在不在 dst target 白名单中的，move 失败
            zbs-iscsi lun convert_from_nfs
                dst target 使用业务主机 + 开启自适应
                dst target 使用业务主机 + 未启用自适应
                dst target 手动配置 + 自适应
                dst target 手动配置 + 全部允许
                dst target 手动配置 + 指定 IQN
                dst target 手动配置 + 全部禁止
            快照的重建和克隆
                dst target 使用业务主机 + 开启自适应
                dst target 使用业务主机 + 未启用自适应
                dst target 手动配置 + 自适应
                dst target 手动配置 + 全部允许
                dst target 手动配置 + 指定 IQN
                dst target 手动配置 + 全部禁止
                dst subsystem 使用业务主机 + 开启自适应
                dst subsystem 使用业务主机 + 未启用自适应
                dst subsystem 手动配置 + 自适应
                dst subsystem 手动配置 + 全部允许
                dst subsystem 手动配置 + 指定 NQN
                dst subsystem 手动配置 + 全部禁止
chunk自动剔除磁盘
    partition - checksum error > 100：触发踢盘，不健康盘，触发告警，自动隔离，数据完成修复后自动踢盘
    partition - checksum error <= 100：健康盘，无告警
    partition - io error > 300:不健康盘，触发告警，errflag=4，自动隔离，数据完成修复后自动踢盘
    partition - io error <= 300:健康盘，无告警
    cache - io error > 300:不健康盘，触发告警，errflag=4，自动隔离，数据完成修复后自动踢盘
    cache - io error <= 300:健康盘，无告警
iouring
    升级集群 - 不升级内核：不开启iouring
    升级集群 - 升级内核：开启iouring
    部署集群 - 默认开启iouring
    修改配置 - 手动开启iouring
    修改配置 - 手动关闭iouring
    开启iouring - intel
    开启iouring - hygon
    开启iouring - arm
    开启iouring - 分层集群
    开启iouring - 不分层集群
    开启iouring - 单实例集群
    开启iouring - 多实例集群
    开启iouring - nvme系统盘卸载/挂载
    开启iouring - nvme缓存盘卸载/挂载
    开启iouring - nvme数据盘卸载/挂载
    开启iouring - 添加节点
    开启iouring - 移除节点
    开启iouring - 长稳/故障测试
zbs-5.7.0 Cgroup 资源配置调整
    CPU 核心分配（有啥物理环境测试啥，后续按需补充一下确保 1\2\4实例都cover到；6 8 12 16  24及以上至少cover 一遍，以及要cover一遍特性全部开启的情况）
        zbs 570 下 飞腾不支持
        chunk配置项
            SMTX ZBS 下当实例数为 1 时仅在探测到单一 NUMA Node 物理核心数量 >= 10 或实例数 >= 2 时，Chunk 配置文件中注入 ISCSI_USE_THREAD=true
            废弃： CHUNK_RUN_DCC_IN_NEW_THREAD=true 
 CHUNK_RUN_DCS_IN_NEW_THREAD=true 
 CHUNK_DC_SHARE_THREAD=false
            LSM_IO_THREAD_NUM=2
            DATA_CHANNEL_THREAD_NUM=N // N -开启 DC 独立核心的模式下 1 实例 2，2 实例和 4 实例为 1 。
                开启RDMA：DATA_CHANNEL_THREAD_NUM = [2,1,1]
                未开启RDMA：DATA_CHANNEL_THREAD_NUM = 预期应该是[2,1,1] (N 代表整个节点上单个实例的 DC 核心数)
        NUMA 分组检查
            B1组（numa 优选组）
                B1 组 为numa 优选组
                在分组 ins1  ->zbs/aurora 和nvmf->dc1  如果 B1 上还有位置 则剩余填充剩余填充的优先级是  （ins2+dc2）（ins3+dc3）zbs/iscsi > zbs/others > zbs/chunk-cprs
                如果 保证填充 zbs/iscsi > zbs/others > zbs/chunk-cprs 之后剩余位置还够 ins2+ dc2  则ins2 和 dc2 会填充到 zbs/iscsi > zbs/others > zbs/chunk-cprs 之前，否则不填充 ins2+ dc2...
                不适用cpu0
            A组
                不使用CPU 0
                组内的不同核心可以在不同的 NUMA 上（尽量在同一个）- 物理核心数少的看一下，比方6或者8核心 B1 没有在一个numa上
                分配顺序：在分组 B1（ins1） ->zbs/aurora 和nvmf->dc1
 如果 B1 上还有位置，则剩余填充的优先级是 zbs/iscsi > zbs/others > zbs/chunk-cprs   （aurora/nvmf  优先于 chunk-dcN  分配？）
                在单一 NUMA node 上只有 <=9 个物理核心时&单实例情况下，不开启 zbs/iscsi 核心；
                多实例情况下固定开启 zbs/iscsi 核心；或者 numa node >=10 开启 zbs/iscsi 核心；
                双活单实例集群下开启 1个 zbs/chunk-cprs， 双活多实例不开启 chunk-cprs
            B组 - Chunk 实例分组和 DC 分组
                不使用 CPU 0
                每个实例分组都需要保证自己在同一个 NUMA 上
                chunk-dcN 的分配顺序是（上面A组剩余的）-> chunk-insN -> chunk-dcN,(chunk-dcN 尽量的靠近对应的 chunk-ins)
                根据实例数设置 lsm-db 数量，预期在meta 之前，和B组在一起
            C组- Meta 分组
                不使用 CPU 0
                meta-main 所在核心
                NUMA 优先选择 A，B 所在 NUMA 之外的其他 NUMA，尽可能离 Group B1 远
                尽量不使用 Polling 核心对应的另外一个 HT 核心
                尽量不使用 Polling 核心（polling核心：aurora、nvmf、zbs-dynamic/aurora-ha、zbs/chunk-dcN、zbs/chunk-insN）对应的另外一个 HT 核心
                如果没有更多 NUMA，则可以选择 B
                    A 所在的 NUMA
                        只有2个numa
                        只有1个numa
            D组- 其他服务分组
                优先选择 A，B 所在 NUMA 之外的其他 NUMA，尽可能离 Group B1 远
                app 和  zbs-dynamic/aurora-ha 所在核心
                如果没有更多 NUMA，则可以选择 B > A 所在的 NUMA
                在没有其他核心可用的情况下，可以使用 CPU 0
            单独验证点检查
                NUMA 分组比较紧张的时候，aurora-ha 可以分配到 aurora 核心对应的 HT 核心上，但是不要分配到其他 Polling 核心对应的 HT 核心上；
                分组 A 和 B 的核心目前几乎都变化为 Polling 模式（lsm-db 不是）
                在 ZBS 单实例时的最小核心数需求为 8（不开启 iscsi 独立核心，chunk-dc 数量为 1）
                预期不出现 2 个 Polling 核心归属于同一个物理核心的的两个 HT 核心的情况
                因为要避免 Polling 核心在同一个物理核心的两个 HT 核心上，所以即便 4 个实例的时候，NUMA B 上有 30-39 对称的 40-49 HT 核心也不要用 Chunk 的关键 IO 核心分配。
            numa 选择优先级策略 （测试时候下面的规则要顺道看下）
                有 HBA 卡，且没有NVMe- 选择HBA 卡对应的numa，通常 numa 0 作为优选；不考虑多张HBA 卡的情况
                NVMe SSD +  HDD/SATA SSD 的环境下， NVMe 磁盘/网卡连接总数之和较多的 NUMA Node 作为优选 NUMA ，不需要考虑HBA 卡
                纯 NVMe SSD 的环境下，网卡/NVMe 磁盘连接计数之和，连接较多的成为优选
                numa UI 展示
                    物理盘池
                        物理盘池1 显示对应ins1 所在numa id
                        物理盘池2 显示对应ins 2 所在numa id
                        物理盘池 3 显示对应ins3 所在numa id
                        物理盘池4 显示对应ins 4 所在numa id
                        单独numa 16 物理核心，2实例 情况下 1和 2 盘池都在同一个numa id
                    磁盘
                        HDD 使用对应的 HBA 卡 NUMA 作为自己的 NUMA
                        SAS HDD  使用对应的 HBA 卡 NUMA 作为自己的 NUMA
                        SATA 使用对应的 HBA 卡 NUMA 作为自己的 NUMA
                        上面几个如果没有HBA卡呢？
                        NVME 显示自己的 NUMA 信息
                    网卡
                        2个网卡（存储和管理）
                        多网卡的情况
            关键服务所在核心组
                zbs/chunk-insN
                    zbs/lsm-io  （线程：c1-lsm-io-0 &1）
                    zbs/chunk-main
                    zbs/chunk-io （线程：c1-lsm）
                zbs/chunk-dcN
                    Chunk-dc
                zbs/lsm-dbN
                    chunk-lsm db + env + disk sync
                meta-main
                    meta
                    zk
                zbs/app
                    taskd
                    iscsi-redirectord
                    timemachine 等
                    zbs/app (从 network 中改回app组)
                        ovsdb-server
                        ovs-vswitchd
                zbs/iscsi**
                    chunk-iscsi
                zbs/others
                    chunk-rpc-x
                    chunk-其他
                    auroramaster
                    session-follower
                    service-registry
                    zoo-io
                    zoo-completion
                zbs/aurora
                    vHost polling
                zbs/nvmf
                    nvmf
                zbs-dynamic/aurora-ha***
                    vHost polling
        不同 NUMA 核心数量 -先不管OS -尽量cover到不同的numa 和实例组合
            单 NUMA < 6 物理核心
                不可以部署 ZBS
            单 NUMA 6 物理核心
                不支持开启多实例
                不支持开启 RDMA，且不开启 lsm-io 能力
                chunk-dc，iscsi，aurora，cprs  不存在
                hygon 6核心
            单 NUMA 8 物理核心
                单实例不开启 iscsi 独立核心
                开启超线程&单实例
                2实例
                4实例
            单 NUMA 12 物理核心
                单实例
                2实例
                4实例
            单 16 物理核心
                1实例或者2实例有环境的话就看一下
                4实例
                节点物理核心数>=64的情况（nvmf 8核心要看下 ）
            单 NUMA 24 物理核心
                1实例或者2实例有环境的话就看一下
                一个numa 能排开 A组和B组
                4 实例
    内存、内存预留、cpu 资源占用数量检查 以及chunk 配置检查 - 剪枝？确保RDMA NVMF 6种组合至少覆盖一遍，1、2、4 实例至少覆盖一遍  & 按照客户的常用配置优先级？
        在 ZBS 不同的节点规格下，如果用户挂载的缓存容量超过节点规格的最大估计。（ Normal 128 T * 20% = 25 T， Large 256 T * 20 = 51 T， XLarge 512 T* 20 % =  102 T） ，则也按照每 8 TiB Cache 增加 2 G 内存的模式增加 Chunk 的缓存。 最终实现为效果是每4TiB  +1GiB&  超过 25 T 就 + 1 G
        normal & 单实例
            存储未开启 RDMA & 接入未开启 NVMe over RDMA or TCP
                内存预留 + 5G 内核 =  64    (os_normal_memory_used 57)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        52+7
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        37+7
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        28+7
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用14 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1  1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 不开启
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    DATA_CHANNEL_THREAD_NUM= 2
                    LSM_IO_THREAD_NUM=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储未开启 RDMA，接入开启 NVMe over  TCP，但未开启 over RDMA
                内存预留 + 5G 内核 =  83  (os_normal_memory_used 57)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        52+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        37+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        28+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用15 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1  1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 1(<8 核心)或者2、4、8
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_TCP=true
                    DATA_CHANNEL_THREAD_NUM= 2
                    LSM_IO_THREAD_NUM=2
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储未开启 RDMA，接入开启 NVMe over  TCP & RDMA
                内存预留 + 5G 内核 =  83     (os_normal_memory_used 57)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        52+26
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        37+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        28+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用15 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1  1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 1(<8 核心)或者2、4、8
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_RDMA=true
                    CHUNK_ENABLE_NVMF_TCP=true
                    DATA_CHANNEL_THREAD_NUM=2
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_ACCESS_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_QOS_MODE=dscp
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储 RDMA & 接入未开启  NVMe over TCP or RDMA
                内存预留 + 5G 内核 =  64    (os_normal_memory_used 57)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        52+7
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        37+7
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        28+7
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用14 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1  1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 不开启
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_NUM= 2
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储 RDMA & 接入开启 NVMe over TCP 但未开启 over RDMA
                内存预留 + 5G 内核 =  83    (os_normal_memory_used 57)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        52+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        37+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        28+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用15 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1  1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 1(<8 核心)或者2、4、8
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_TCP=true
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_NUM= 2
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储 RDMA & 接入 NVMe over RDMA & 接入 NVMe over TCP
                内存预留 + 5G 内核 =  83  (os_normal_memory_used 57)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        52+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        37+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        28+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用15 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1  1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 1(<8 核心)或者2、4、8
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_RDMA=true
                    CHUNK_ENABLE_NVMF_TCP=true
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_NUM= 2
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_QOS_MODE=dscp
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
        large & 单实例
            存储未开启 RDMA & 接入未开启 NVMe over RDMA or TCP
                内存预留 + 5G 内核 =  77    (os_normal_memory_used 70)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        65+7
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        50+7
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        41+7
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用14 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1  1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 不开启
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    DATA_CHANNEL_THREAD_NUM= 2
                    LSM_IO_THREAD_NUM=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储未开启 RDMA，接入开启 NVMe over  TCP，但未开启 over RDMA
                内存预留 + 5G 内核 =  96   (os_normal_memory_used 70)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        65+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        50+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        41+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用16 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db 1  1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 2( 2、4、8）
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_TCP=true
                    DATA_CHANNEL_THREAD_NUM= 2
                    LSM_IO_THREAD_NUM=2
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储未开启 RDMA，接入开启 NVMe over  TCP & RDMA
                内存预留 + 5G 内核 =  96    (os_normal_memory_used 70)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        65+26
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        50+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        41+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用16 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1  1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 1(<8 核心)或者2、4、8
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk 配置
                    "ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_RDMA=true
                    CHUNK_ENABLE_NVMF_TCP=true
                    DATA_CHANNEL_THREAD_NUM= 2
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_ACCESS_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_QOS_MODE=dscp
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储 RDMA & 接入未开启  NVMe over TCP or RDMA
                内存预留 + 5G 内核 =  77    (os_normal_memory_used 70)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        65+7
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        50+7
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        41+7
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用14 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1  1
                    zbs/chunk-dc1  1
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 不开启
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_NUM=1
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_COUNT= 2
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储 RDMA & 接入开启 NVMe over TCP 但未开启 over RDMA
                内存预留 + 5G 内核 =  96     (os_normal_memory_used 70)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        65+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        50+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        41+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用16 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1  1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启2(2、4、8）
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_TCP=true
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_NUM= 2
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储 RDMA & 接入 NVMe over RDMA & 接入 NVMe over TCP
                内存预留 + 5G 内核 =  96    (os_normal_memory_used 70)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        65+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        50+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        41+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用16 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db 1  1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 2 （2、4、8）
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_RDMA=true
                    CHUNK_ENABLE_NVMF_TCP=true
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_NUM= 2
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_QOS_MODE=dscp
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
        large & 2实例
            存储未开启 RDMA & 接入未开启 NVMe over RDMA or TCP
                内存预留 + 5G 内核 =  85   (os_normal_memory_used 78)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        73+7
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        58+7
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        49+7
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用20 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi 1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1 & db2  2
                    zbs/chunk-dc1& dc2   2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 不开启
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2 8
                        zbs/lsm-io 2*2
                        zbs/chunk-main 1*2
                        zbs/chunk-io 1*2
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    DATA_CHANNEL_THREAD_NUM= 1
                    LSM_IO_THREAD_NUM=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储未开启 RDMA，接入开启 NVMe over  TCP，但未开启 over RDMA
                内存预留 + 5G 内核 =  104   (os_normal_memory_used 78)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        73+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        58+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        49+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用24 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app 2
                    zbs/iscsi  1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1& db2  2
                    zbs/chunk-dc1&dc2   2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 4 (<8 核心)或者2、4、8
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2 8
                        zbs/lsm-io 2*2
                        zbs/chunk-main 1*2
                        zbs/chunk-io 1*2
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_TCP=true
                    DATA_CHANNEL_THREAD_NUM= 1
                    LSM_IO_THREAD_NUM=2
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储未开启 RDMA，接入开启 NVMe over  TCP & RDMA
                内存预留 + 5G 内核 =  107   (os_normal_memory_used 78)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        73+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        58+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        49+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用24 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi  1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1& db2  2
                    zbs/chunk-dc1&dc2   2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 4 (<8 核心)或者2、4、8
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2 8
                        zbs/lsm-io 2*2
                        zbs/chunk-main 1*2
                        zbs/chunk-io 1*2
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_RDMA=true
                    CHUNK_ENABLE_NVMF_TCP=true
                    DATA_CHANNEL_THREAD_NUM=1
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_ACCESS_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_QOS_MODE=dscp
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储 RDMA & 接入未开启  NVMe over TCP or RDMA
                内存预留 + 5G 内核 =  85   (os_normal_memory_used 78)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        73+7
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        58+7
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        49+7
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用20 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi 1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1 & db2  2
                    zbs/chunk-dc1& dc2   2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 不开启
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2 8
                        zbs/lsm-io 2*2
                        zbs/chunk-main 1*2
                        zbs/chunk-io 1*2
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_TCP=true
                    CHUNK_NUM=2
                    DATA_CHANNEL_THREAD_COUNT= 1
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储 RDMA & 接入开启 NVMe over TCP 但未开启 over RDMA
                内存预留 + 5G 内核 =  104
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        73+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        58+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        49+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用24 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi  1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1& db2  2
                    zbs/chunk-dc1&dc2   2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 4 (<8 核心)或者2、4、8
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2 8
                        zbs/lsm-io 2*2
                        zbs/chunk-main 1*2
                        zbs/chunk-io 1*2
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_TCP=true
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_COUNT= 1
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储 RDMA & 接入 NVMe over RDMA & 接入 NVMe over TCP
                内存预留 + 5G 内核 =  107   (os_normal_memory_used 78)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        73+29（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        58+29
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        49+29
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用24 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi  1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1& db2  2
                    zbs/chunk-dc1&dc2   2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 4 (<8 核心)或者2、4、8
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2 8
                        zbs/lsm-io 2*2
                        zbs/chunk-main 1*2
                        zbs/chunk-io 1*2
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_RDMA=true
                    CHUNK_ENABLE_NVMF_TCP=true
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_COUNT= 1
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_QOS_MODE=dscp
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
        xlarge & 单实例
            存储未开启 RDMA & 接入未开启 NVMe over RDMA or TCP
                内存预留 + 5G 内核 =  111    (os_normal_memory_used 104)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        99+7
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        84+7
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        75+7
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用14 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db 1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 不开启
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    DATA_CHANNEL_THREAD_COUNT= 2
                    LSM_IO_THREAD_NUM=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储未开启 RDMA，接入开启 NVMe over  TCP，但未开启 over RDMA
                内存预留 + 5G 内核 =  130   (os_normal_memory_used 104)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        99+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        84+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        75+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用18 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app 2
                    zbs/iscsi  （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db 1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 2(<8 核心)或者2、4、8
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_TCP=true
                    DATA_CHANNEL_THREAD_COUNT= 2
                    LSM_IO_THREAD_NUM=2
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储未开启 RDMA，接入开启 NVMe over  TCP & RDMA
                内存预留 + 5G 内核 =  130   (os_normal_memory_used 78)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        99+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        84+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        75+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用18 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi  （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db 1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 4(<8 核心)或者2、4、8
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk 配置
                    "ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_RDMA=true
                    CHUNK_ENABLE_NVMF_TCP=true
                    DATA_CHANNEL_THREAD_COUNT= 2
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_ACCESS_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_QOS_MODE=dscp
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120"
            存储 RDMA & 接入未开启  NVMe over TCP or RDMA
                内存预留 + 5G 内核 =  111    (os_normal_memory_used 104)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        99+7
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        84+7
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        75+7
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用14 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db 1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 不开启
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_NUM=1
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_NUM= 2
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储 RDMA & 接入开启 NVMe over TCP 但未开启 over RDMA
                内存预留 + 5G 内核 =  130    (os_normal_memory_used 78)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        99+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        84+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        75+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用18 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi  （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db 1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 4(<8 核心)或者2、4、8
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_TCP=true
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_COUNT= 2
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
            存储 RDMA & 接入 NVMe over RDMA & 接入 NVMe over TCP
                内存预留 + 5G 内核 =  130    (os_normal_memory_used 104)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        99+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        84+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        75+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用16 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi  （CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db 1
                    zbs/chunk-dc1  2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 2(<8 核心)或者2、4、8
                    双活开启 zbs/chunk-cprs
                    chunk-ins1 4
                        zbs/lsm-io 2
                        zbs/chunk-main 1
                        zbs/chunk-io 1
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_RDMA=true
                    CHUNK_ENABLE_NVMF_TCP=true
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_COUNT= 2
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_QOS_MODE=dscp
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=5368709120
        xlarge & 2实例
            存储未开启 RDMA & 接入未开启 NVMe over RDMA or TCP
                内存预留 + 5G 内核 =  119   (os_normal_memory_used 112)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice       107+7
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        92+7
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        83+7
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用20 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi 1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1 & db2  2
                    zbs/chunk-dc1& dc2   2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 不开启
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2 8
                        zbs/lsm-io 2*2
                        zbs/chunk-main 1*2
                        zbs/chunk-io 1*2
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    DATA_CHANNEL_THREAD_COUNT= 1
                    LSM_IO_THREAD_NUM=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储未开启 RDMA，接入开启 NVMe over  TCP，但未开启 over RDMA
                内存预留 + 5G 内核 =  138 (os_normal_memory_used 112)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        107+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        92+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        83+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用24 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi  1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1& db2  2
                    zbs/chunk-dc1&dc2   2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 4 (<8 核心)或者2、4、8
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2 8
                        zbs/lsm-io 2*2
                        zbs/chunk-main 1*2
                        zbs/chunk-io 1*2
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_TCP=true
                    DATA_CHANNEL_THREAD_COUNT= 1
                    LSM_IO_THREAD_NUM=2
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储未开启 RDMA，接入开启 NVMe over  TCP & RDMA
                内存预留 + 5G 内核 =  104   (os_normal_memory_used 78)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        107+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        92+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        83+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用24 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi  1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1& db2  2
                    zbs/chunk-dc1&dc2   2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 4 (<8 核心)或者2、4、8
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2 8
                        zbs/lsm-io 2*2
                        zbs/chunk-main 1*2
                        zbs/chunk-io 1*2
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_RDMA=true
                    CHUNK_ENABLE_NVMF_TCP=true
                    DATA_CHANNEL_THREAD_COUNT=1
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_ACCESS_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_QOS_MODE=dscp
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储 RDMA & 接入未开启  NVMe over TCP or RDMA
                内存预留 + 5G 内核 =  119  (os_normal_memory_used 112)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice       107+7
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        92+7
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        83+7
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用20 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi 1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1 & db2  2
                    zbs/chunk-dc1& dc2   2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 不开启
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2 8
                        zbs/lsm-io 2*2
                        zbs/chunk-main 1*2
                        zbs/chunk-io 1*2
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_NUM=2
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_COUNT= 1
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储 RDMA & 接入开启 NVMe over TCP 但未开启 over RDMA
                内存预留 + 5G 内核 =  119  (os_normal_memory_used 112)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice       107+7
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        92+7
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        83+7
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用20 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi 1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1 & db2  2
                    zbs/chunk-dc1& dc2   2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 不开启
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2 8
                        zbs/lsm-io 2*2
                        zbs/chunk-main 1*2
                        zbs/chunk-io 1*2
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_TCP=true
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_COUNT= 1
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储 RDMA & 接入 NVMe over RDMA & 接入 NVMe over TCP
                内存预留 + 5G 内核 =  138  (os_normal_memory_used 112)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice       107+29
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        92+29
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        83+29
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用24 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi 1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1 & db2  2
                    zbs/chunk-dc1& dc2   2
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 4 (<8 核心)或者2、4、8
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2 8
                        zbs/lsm-io 2*2
                        zbs/chunk-main 1*2
                        zbs/chunk-io 1*2
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_RDMA=true
                    CHUNK_ENABLE_NVMF_TCP=true
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_COUNT= 1
                    LSM_IO_THREAD_NUM=2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_QOS_MODE=dscp
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
        xlarge & 4 实例
            存储未开启 RDMA & 接入未开启 NVMe over RDMA or TCP
                内存预留 + 5G 内核 =  135  (os_normal_memory_used 128)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice       123+7
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        108+7
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        99+7
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用32 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi 1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1-db4  4
                    zbs/chunk-dc1- dc4   4
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 不开启
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2&ins 3& ins4  16
                        zbs/lsm-io 2*4
                        zbs/chunk-main 1*4
                        zbs/chunk-io 1*4
                chunk 配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    DATA_CHANNEL_THREAD_COUNT= 1
                    LSM_IO_THREAD_NUM=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储未开启 RDMA，接入开启 NVMe over  TCP，但未开启 over RDMA
                内存预留 + 5G 内核 =  154  (os_normal_memory_used 128)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        123+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        108+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        99+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用36 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi  1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1- db4 4
                    zbs/chunk-dc1-dc4   4
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 4 (<8 核心)或者2、4、8
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1- ins4 16
                        zbs/lsm-io 2*4
                        zbs/chunk-main 1*4
                        zbs/chunk-io 1*4
                        zbs/lsm-io 2*4
                        zbs/chunk-main 1*4
                        zbs/chunk-io 1*4
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_TCP=true
                    DATA_CHANNEL_THREAD_COUNT= 1
                    LSM_IO_THREAD_NUM=2
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储未开启 RDMA，接入开启 NVMe over TCP & RDMA
                内存预留 + 5G 内核 =  154  (os_normal_memory_used 128)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice 123+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice 6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice 108+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        99+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice 9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用36 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi  1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1- db4 4
                    zbs/chunk-dc1-dc4   4
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 4 (<8 核心)或者2、4、8
                    双活也不开启 zbs/chunk-cprs
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_RDMA=true
                    CHUNK_ENABLE_NVMF_TCP=true
                    DATA_CHANNEL_THREAD_COUNT= 1
                    LSM_IO_THREAD_NUM= 2
                    CHUNK_SERVER_ACCESS_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_QOS_MODE=dscp
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储 RDMA & 接入未开启  NVMe over TCP or RDMA
                内存预留 + 5G 内核 =  135  (os_normal_memory_used 128)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice       123+7
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        108+7
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        99+7
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用32 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi 1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1-db4  4
                    zbs/chunk-dc1- dc4   4
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 不开启
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1& ins2&ins 3& ins4  16
                        zbs/lsm-io 2*4
                        zbs/chunk-main 1*4
                        zbs/chunk-io 1*4
                chunk 配置
                    "ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_NUM=4
                    DATA_CHANNEL_THREAD_COUNT= 1
                    LSM_IO_THREAD_NUM= 2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储 RDMA & 接入开启 NVMe over TCP 但未开启 over RDMA
                内存预留 + 5G 内核 =  154  (os_normal_memory_used 128)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                smtx.slice        123+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        108+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        99+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用36 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi  1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1- db4 4
                    zbs/chunk-dc1-dc4   4
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 4 (<8 核心)或者2、4、8
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1- ins4 16
                        zbs/lsm-io 2*4
                        zbs/chunk-main 1*4
                        zbs/chunk-io 1*4
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_TCP=true
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_COUNT= 1
                    LSM_IO_THREAD_NUM= 2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
            存储 RDMA & 接入 NVMe over RDMA & 接入 NVMe over TCP
                内存预留 + 5G 内核 =  154  (os_normal_memory_used 128)
                ARM 额外给 Chunk 分组增加 2 GB 内存
                内存：smtx.slice        123+26（huge）
                    smtx-elf.slice        2
                    smtx-tuna.slice        4
                    smtx-network.slice        2
                    smtx-lcm.slice        5
                    smtx-infra.slice        6
                        smtx-infra-mongod.slice        3
                        smtx-infra-zk.slice        2
                        smtx-infra-jc.slice        1
                        smtx-infra-common.slice        2
                    smtx-zbs.slice        108+26
                        smtx-zbs-metamain.slice        6
                        smtx-zbs-chunkd.slice        99+26
                        smtx-zbs-others.slice        3
                    smtx-obs.slice        9
                        smtx-obs-prometheus.slice        8
                cpu 总核心占用36 +
                    zbs/meta-main  2
                    zbs/others 1
                    zbs/app  2
                    zbs/iscsi  1（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2 开启）
                    zbs/lsm-db1- db4 4
                    zbs/chunk-dc1-dc4   4
                    zbs/aurora 1
                    zbs-dynamic/aurora-ha 1
                    nvmf 开启 4 (<8 核心)或者2、4、8
                    双活也不开启 zbs/chunk-cprs
                    chunk-ins1- ins4 16
                        zbs/lsm-io 2*4
                        zbs/chunk-main 1*4
                        zbs/chunk-io 1*4
                chunk配置
                    ISCSI_USE_THREAD=true（CPU 单 NUMA 物理核心数量 >=10 或实例数 >=2）
                    CHUNK_ENABLE_NVMF_RDMA=true
                    CHUNK_ENABLE_NVMF_TCP=true
                    CHUNK_USE_RDMA=true
                    DATA_CHANNEL_THREAD_NUM= 1
                    LSM_IO_THREAD_NUM= 2
                    CHUNK_SERVER_DATA_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_IBDEV_NAME=
                    CHUNK_SERVER_ACCESS_QOS_MODE=dscp
                    ZBS_NVMF_MAX_IO_QUEUES=2
                    ZBS_DMALLOC_USES_HUGEPAGE=true
                    ZBS_DMALLOC_MEMORY_SIZE=8589934592
    运维场景&故障检查（随机穿插在上面的各种特性组合中测试）
        新部署环境
        master 节点
        storage 节点
        实例数混合的环境看一下
        数据盘扩容-预期不影响
        内存扩容- 预期不影响
        分层不分层不影响内存资源
        升级环境
            未开启boost 的集群 -   旧版本升级上来
            开启boost动作之后检查资源配置
            旧版本就已经开启了boost
            numa 紧张的情况看下
            升级集群涉及numa 优选变化
                NVME 和 HBA 接 不同的numa node上-升级场景看一下
                检查升级之后的numa 绑定符合预期
                cpuset 和内存符合预期
        扩容节点
            numa 检查要加一下
        双活环境
            仲裁节点没有cgroup 配置
            可用域节点
            多实例没有链路压缩，单实例有cprs
        角色转换
            master->storage
            storage -> master
        主机重启之后
            异常掉电重启
            tower UI上面重启
        HBA 卡 增加|减少 、网卡增加|减少、NVME 增加|减少，预期重启的时候要重新计算优选numa
            NVMe
                增加
                减少
            网卡
                增加
                减少
            HBA 卡 - 场景很低概率发生-可以不用测试
                增加
                减少
        关键服务重启
            meta
            chunk
            cgconfig
        缓存盘扩容
            ZBS Normal 如果挂载超过20%，需要为 ZBS.Chunk 每 8 TiB 分配 2 G 内存的方式扩张 （(cache_total - partition_capacity * 0.2) / 8TiB * 2GiB  结果取整到GiB。 效果是每4TiB  +1GiB。）
            large 和 xlarge 也要做的内存调整
            单实例不允许超过 51 TiB 缓存盘；2实例不超过102 T（根据单个磁盘池来检查，每个不能超过51T）；4 实例不超过204 T（根据单个磁盘池子检查，每个不能超过51T）
    tuna 实现逻辑调整
        svcresctl-upgrade-check RPM 安装后，下一个版本的资源规格定义存放位置为:  /usr/share/tuna/svcres/specs-next/
        全局资源规格定义安装的位置为： /usr/share/tuna/svcres/specs/
            升级后环境
            新部署环境
        cgroup 资源规格定义
            cgroups-smtx.yaml 符合新的层级结构
            检查里面各个组的内存 和limit
            memory reservation 内存预留规格 (system_reservation.yaml)
            检查里面 cpuset cgroup
                chunk 关键组的优先级
                polling 的不能和其他共用
        几个命令简单看下
            svcresctl chunk-numa-nodes update
            zbs-deploy-manage show_cgroup
            chunk实例和NUMA node 的绑定关系的维护不再作为 cgroup config 中的一部分，而是作为独立的配置步骤，在需要进行更新的运维动作中才执行这个步骤。
            svcresctl chunk-numa-nodes advise --numa-dev-num '{"0":2, "1":1}' -e '{"platform": "san"}； 结合上面  numa 选择优先级策略一起测试
                2个numa
                4 个numa
                8个numa
            zbs-deploy-manage config_cgroup
                参数磁盘总量
                缓存总量
    升级场景下的资源预检查（zbs 场景下、硬件部署的要求是足够的，不支持业务虚拟机、预期升级不会有问题）简单通过虚拟机构造场景看下
        vhost 环境下内存不足
        CPU 不足
        内存不足
            总内存量不足
            可用内存量不足
    架构 -（随机穿插在上面的各种特性组合中测试）
        hygon
        双活环境单独看下
        intel
            centos
            oe 不支持
        arm
            飞腾不支持
            鲲鹏
    回归 - 开启资源指标
        选取1-2个服务看下内存超限告警
        cpu 组的采集情况看下
        cpu 组 放置的告警
meta辅助卸载磁盘
    cache盘：开启/关闭辅助卸载，观察卸载速度是否提升
    partition盘：开启/关闭辅助卸载，观察卸载速度是否提升
    副本卷数据：可以进行辅助卸载
    EC卷数据：不可以进行辅助卸载
    dst cid选取：健康，不健康节点不能作为dst cid
    dst cid选取：inuse，移除中节点不能作为dst cid
    dst cid选取：非isolate
    dst cid选取：有迁移命令生成配额
    dst cid选取：：不是目标卸载磁盘的节点
    dst cid选取：拓扑安全
    src cid选取：健康节点，不健康节点不能作为src cid
    src cid选取：inuse/removing stat
    src cid选取：不是目标卸载磁盘的节点
    src cid选取：有迁移命令生成配额
    src cid散不同cid，dst cid :首选prefer local
    辅助卸载盘：先 cap 后 perf、多 umounting chunk 间轮转
    zbs-meta migrate 新增cli
    快照链上的extent，lsm不上报
    双活集群：dst cid跟replace cid在一个zone
    集群节点负载不均衡，部分节点高负载，部分节点低负载，触发低负载节点卸载磁盘，优先容量均衡，且src cid/dst cid可以为umounting cid
    集群节点负载不均衡，部分节点中负载，部分节点低负载，卸载低负载节点磁盘，src cid/dst cid不为umounting cid
    同时卸载多个节点磁盘，一次 migrate distribute 中有多个磁盘的 umounting migrate
NetGuard 自动配置流控
    安装
        全新安装 zbs570，存储网和接入网均不启用 RDMA，netgurad 配置文件中 storageQosType 和 accessQosType 默认为 dscp
        全新安装 zbs570，仅存储网启用 RDMA，netguard 配置文件中 storageQosType 和 accessQosType 默认为 dscp，流控正常
        全新安装，仅接入网启用 NVMe over rdma，netguard 配置文件中 storageQosType 和 accessQosType 默认为 dscp，流控正常
        全新安装，存储网和接入网均启用了 RDMA，netguard 配置文件展示正确，流控正常
    升级
        集群存储网和接入网均未启用 RDMA，升级后 netguard 配置文件符合预期
        集群仅存储网启用了 RDMA，且配置为 dscp，升级后 netguard 配置文件符合预期，流控正常
        集群仅接入网启用了 RDMA，且配置为 global，升级后 netguard 配置文件符合预期，流控正常
        集群存储网和接入网均启用了 RDMA，且配置为 dscp，升级后 netguard 配置文件符合预期，流控正常
        集群存储网和接入网均启用了 RDMA，且配置为 global，升级后 netguard 配置文件符合预期，流控正常
        升级成功后，netguard 运行正常，配置文件正确，网口运维时 netguard 行为符合预期
    运维
        集群存储网和接入网均未启用 RDMA，进行网口增减，不会触发 netguard
        存储网启用了 RDMA，存储网口增加，netguard 自动为增加的网口配置流控，流控类型和 netgurad 配置文件中一致；netguard 开始监控新增的网口；流控正常
        存储网启用了 RDMA，存储网口减少，netguard 取消对该网口的监控，该网口 ifdown 之后 ifup，不会触发 netguard；流控正常
        接入网启用了 RDMA，接入网口增加，netguard 自动为增加的网口配置流控，流控类型和 netgurad 配置文件中一致；netguard 开始监控新增的网口；流控正常
        接入网启用了 RDMA，接入网口减少，netguard 取消对该网口的监控，该网口 ifdown 之后 ifup，不会触发 netguard；流控正常
        修改配置文件，启用 RDMA，netguard 开始监控对应网络的配置文件和其中的网口，网口运维或故障会自动触发 netguard；流控正常
        修改配置文件，关闭 RDMA，netguard 通知监控对应网络的配置文件和其中的网口，网口运维或故障不会触发 netguard
    故障
        存储网/接入网未启用 RDMA，ifdown 网口之后 ifup，不会触发 netguard
        存储网启用了 RDMA，ifdown 网口之后 ifup，会自动触发 netguard 为该网口配置流控，流控类型和 netguard 配置文件中一致；流控正常
        存储网/接入网未启用 RDMA，network 服务重启，不会触发 netguard
        存储网/接入网启用了 RDMA，network 服务重启，netguard 仅为启用了 RDMA 的网络内的网口配置流控，流控类型和 netguard 配置文件中一致，流控正常
        存储网/接入网启用了 RDMA，zbs-chunkd 服务重启，过程中不强制要求执行 zbs_config_rdma_qos.sh，多网口环境中 IO 中断时间降低
zbs-5.7.0 多实例 cli
    zbs-meta
        cluster
            zbs-meta cluster summary
            zbs-meta cluster show_chunk_connectivity
            zbs-meta cluster get_chunk_connectivities
        node
            zbs-meta node list
            zbs-meta node show
            zbs-meta node set_prs_ratio
            zbs-meta node get_prs_ratio
        chunk
            zbs-meta chunk set_maintenance --single_chunk
            zbs-meta chunk set_failslow --single_chunk
            zbs-meta chunk set_prs_ratio
            zbs-meta chunk get_prs_ratio
            zbs-meta chunk register
            zbs-meta chunk list
            zbs-meta chunk show
            zbs-meta chunk list_pid
            zbs-meta chunk get_maintenance
            zbs-meta chunk remove
        volume
            zbs-meta volume create --chunk_instances
            zbs-meta volume update --chunk_instances
            zbs-meta volume show
            zbs-meta volume show_by_id
            zbs-meta volume report_access
        snapshot
            zbs-meta  snapshot show_by_id
        topo
            zbs-meta topo list
            zbs-meta topo show
        reposition
            zbs-meta reposition show
            zbs-meta reposition update
            zbs-meta reposition summary
        internal_io
            zbs-meta internal_io show
        storage_pool
            zbs-meta storage_pool add_chunk
            zbs-meta storage_pool remove_chunk
            zbs-meta storage_pool cancel_remove
    zbs-chunk
        partition/cache
            zbs-chunk partition/cache format
            zbs-chunk partition/cache mount
            zbs-chunk partition/cache umount
            zbs-chunk partition/cache cancel-umount
            zbs-chunk partition/cache set-unhealthy
            zbs-chunk partition/cache set-healthy
            zbs-chunk partition/cache isolate
        journal
            zbs-chunk journal format
            zbs-chunk journal mount
            zbs-chunk journal umount
            zbs-chunk journal cancel-umount
            zbs-chunk journal set-unhealthy
            zbs-chunk journal set-healthy
        recover
            zbs-chunk recover list
        migrate
            zbs-chunk migrate  list
        extent
            zbs-chunk extent list
            zbs-chunk extent promote
            zbs-chunk extent invalidate
        sink
            zbs-chunk sink list
        metric
            zbs-chunk metric sink
            zbs-chunk metric app
            zbs-chunk metric reposition
            zbs-chunk metric fc
            zbs-chunk metric ifc
        cap_io
            zbs-chunk cap_io get
            zbs-chunk cap_io set
        internal_io
            zbs-chunk internal_io get
            zbs-chunk internal_io set
        summary
            zbs-chunk summary
        counter
            zbs-chunk counter list '*'
        address
            zbs-chunk address show
        verify
            zbs-chunk verify
    zbs-iscsi
        lun
            zbs-iscsi lun create  --chunk_instances
            zbs-iscsi lun update --chunk_instances
            zbs-iscsi lun show
    zbs-nvmf
        ns
            zbs-nvmf ns create  --chunk_instances
            zbs-nvmf ns update --chunk_instances
            zbs-nvmf ns show
    zbs-deploy-manage
        mount-disk
            zbs-deploy-manage mount-disk --chunk_ins_id
        mount-cache-disk
            zbs-deploy-manage mount-cache-disk --chunk_ins_id
        mount-extent-disk
            zbs-deploy-manage mount-extent-disk --chunk_ins_id
保证扩容节点 NVMF 配置一致性
    新部署（zbs-5.7.0）
        部署集群，不开启 NVMF，配置正确写入（同开启 NVMe over TCP）。
        部署集群，开启 NVMe over TCP
        部署集群，开启 NVMe over RDMA 与 NVMe over TCP
        节点扩容，扩容 storage 节点后，/etc/sysconfig/zbs-metad 配置正确更新
        节点扩容，转为 master 节点，配置文件正确
        节点扩容，扩容节点变为 meta leader，配置生效
        节点替换，配置文件检查通过
        双活集群部署，配置文件检查通过
        linux 客户端
        esxi 客户端
    旧版本升级到 zbs-5.7.0
        存在 NVMF 配置
            配置一致性检查
            Meta 节点配置注入
            特殊版本路径（5.6.0–5.7.0, 内存 ≥ 128G）
            linux 客户端
            esxi 客户端
        不存在 NVMF 配置
            Meta 节点配置注入
            zbs-5.0.0 升级到 zbs-5.7.0
            zbs-5.4.1 升级到 zbs-5.7.0
            zbs-5.3.0 升级到 zbs-5.7.0
            zbs-5.4.0 升级到 zbs-5.7.0
            zbs-5.4.1 升级到 zbs-5.7.0
            zbs-5.5.0 升级到 zbs-5.7.0
            zbs-5.5.1 升级到 zbs-5.7.0
            zbs-5.6.0 升级到 zbs-5.7.0(没有 NVMF 配置)
            zbs-5.6.4 升级到 zbs-5.7.0（内存小于 128G，双活集群）
            5.1.0 → 5.2.0 → 5.3.0 → 5.6.0  →  5.7.0(缓存超过 128G)
            linux 客户端
            esxi 客户端
        升级后扩容验证
            扩容 Storage 节点
            扩容实例数量选择
            转换为 Master 节点
            扩容节点成为 Meta Leader
            场景组合
device_id生成规则改动
    device_id生成规则 - UDEV存在ID_SCSI_SERIAL：针对 scsi-， ata-， nvme-， virtio- ，统一增加 hwid 前缀
    device_id生成规则 - UDEV存在ID_SCSI_SERIAL：针对 scsi 盘，device_id生成基于 ID_SCSI_SERIAL
    device_id生成规则 - UDEV不存在ID_SCSI_SERIAL：针对 scsi-， ata-， nvme-， virtio- 统一增加 hwid 前缀
    device_id生成规则 - UDEV不存在ID_SCSI_SERIAL：针对 scsi 盘，device_id生成基于 ID_SERIAL
    case场景
    新部署
        统一增加hwid前缀：nvme、scsi、ata、wirtio
        新部署 - 回归磁盘运维场景，检查device_id是否符合预期
        新部署 - 回归节点运维场景，检查device_id是否符合预期
    升级
        device_id未变化 - nvme：统一增加hwid前缀，lsm device id不变
        device_id未变化 - scsi：统一增加hwid前缀，lsm device id不变
        device_id未变化 -ata：统一增加hwid前缀，lsm device id不变
        device_id未变化 - virtio：统一增加hwid前缀，lsm device id不变
        升级后回归磁盘/节点运维：无异常
        device_id变化 - 确认nvme、scsi、ata、virtio增加hwid前缀
        device_id变化 - 升级过程中io正常
        device_id变化 - 升级后，回归磁盘/节点运维
        device_id变化 - 升级前存在异常盘，升级后异常盘记录不丢失
存储、接入网卡中断绑定
    Mellanox 网卡
        全新部署
            部署后检查节点上新增脚本
            检查当前存储网卡中断绑定的 CPU：离 dc* 最近的 6 个空闲 CPU
            检查当前接入网卡中断绑定的 CPU：离 nvmf/iscsi 最近的 6 个空闲 CPU
            检查存储、接入网卡的中断是否受 irq balance 管理
            网口运维——增加存储网 bond 中的网口，irqbalance 服务自动重启，一直属于存储和接入网的网口中断绑定不变；增加的网口的中断可能发生变化，之后不会被 irqbalance 管理
            网口运维——减少存储网 bond 中的网口，irqbalance 服务自动重启，一直属于存储和接入网的网口中断绑定不变；移除的网口的中断可能发生变化，之后会被 irqbalance 管理
            网口运维——增加接入网 bond 中的网口，irqbalance 服务自动重启，一直属于存储和接入网的网口中断绑定不变；增加的网口的中断可能发生变化，之后不会被 irqbalance 管理
            网口运维——减少接入网 bond 中的网口，irqbalance 服务自动重启，一直属于存储和接入网的网口中断绑定不变；移除的网口的中断可能发生变化，之后会被 irqbalance 管理
            网口运维——管理网 bond 中的网口增减，irqbalance 不会自动重启，也不会对中断进行重新绑定
            故障——ifdown + ifup 存储网网口，该网口的中断仍在之前绑定的 CPU 上，也不会被 irqbalance 管理；irqbalance 不会重启
            故障——ifdown + ifup 接入网网口，该网口的中断仍在之前绑定的 CPU 上，也不会被 irqbalance 管理；irqbalance 不会重启
            故障——ifdown + ifup 管理网网口/空闲网口，该网口的中断可能会发生变化，仍被 irqbalance 管理；irqbalance 不会重启
            添加节点——新添加的节点配置与已有节点一致
        升级
            升级后节点新增脚本检查：/etc/sysconfig/irqbalance 中无新增字段；重启 irqbalance 不会自动执行 zbs_irq_policy_script.sh
            所有网卡中断都会被 irqbalance 管理
            存储、接入网的网口增减，irqbalance 自动重启，但是也不会配置网卡中断绑定：执行 zbs_config_nic.py 时会自动退出
            添加节点——新添加的节点配置与新部署的节点一致
    华为网卡
        全新部署
            节点新增脚本同 mellanox 网卡新部署；但重启 irqbalance 时执行 zbs_irq_policy_script.sh 会被校验住，不会生效
            所有网卡中断都会被 irqbalance 管理
            存储、接入网的网口增减，irqbalance 自动重启，但是也不会配置网卡中断绑定：执行 zbs_config_nic.py 时会自动退出
            添加节点——新添加的节点配置与已有节点一致
        升级
            升级后节点新增脚本检查：/etc/sysconfig/irqbalance 中无新增字段；重启 irqbalance 不会自动执行 zbs_irq_policy_script.sh
            所有网卡中断都会被 irqbalance 管理
            存储、接入网的网口增减，irqbalance 自动重启，但是也不会配置网卡中断绑定：执行 zbs_config_nic.py 时会自动退出
            添加节点——新添加的节点配置与已有节点一致
存储卷 IO 监控指标支持整卷 - ui
    第一阶段：支持所有集群，os/zbs
    创建监控图表 - table：新增层级选项：卷/接入点
    创建监控图表 - table：层级选项默认选择卷
    创建监控图表 - table：层级选择接入点，默认选中全部接入点，可取消选择
    创建监控图表 - 层级为卷是不可选择TOP  N模式（第二阶段再支持）
    创建监控图表 - lun/ns - 层级为卷：IOPS总
    创建监控图表 - lun/ns - 层级为卷：IOPS读
    创建监控图表 - lun/ns - 层级为卷：IOPS写
    创建监控图表 - lun/ns - 层级为卷：IOPS读，写
    创建监控图表 - lun/ns - 层级为卷：IO带宽总
    创建监控图表 - lun/ns - 层级为卷：IO带宽读
    创建监控图表 - lun/ns - 层级为卷：IO带宽写
    创建监控图表 - lun/ns - 层级为卷：IO带宽读，写
    修改监控图表 - 修改层级：卷-》接入点
    修改监控图表 - 修改层级：接入点-》卷
    修改监控图表 - 修改指标：不支持层级指标修改为支持层级的指标
    修改监控图表 - 修改指标：支持层级指标修改为不支持层级的指标
    删除监控图表：包含层级
    卷详情 - 监控 - lun：查看卷级别监控，可切换查看接入点
    卷详情 - 监控 - ns：查看卷级别监控，可切换查看接入点
    卷详情-添加到监控视图 - lun：iops-总：添加到监控视图
    卷详情-添加到监控视图 - lun：带宽-总：添加到监控视图
    卷详情-添加到监控视图 - ns：iops-总：添加到监控视图
    卷详情-添加到监控视图 - ns：带宽-总：添加到监控视图
    升级场景：升级前存在图表层级为接入点，编辑图表可切换为卷
    事件描述 - 创建监控图表：新增“层级”选项
    事件描述 - 编辑监控图表：新增“层级”选项