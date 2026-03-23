cluster installer 1.4.0
    SMTXOS 不同的容量规格
        裸金属安装
            配置存储页面 - 批量设置：容量规格 - 选择“标准容量规格”
                zbs 5.5.0
                zbs 5.6.0
                smtxos 6.1.0
                smtxos 6.2.0 p1
                zbs 5.4.0
                    不支持配置规格
                zbs 5.7.0
                    当前版本不支持zbs 5.7.0（不支持chunk 多实例）
                smtxos 5.1.5
                    不支持配置规格
                smtxos 6.0.0
                    不支持配置规格
            配置存储页面 - 批量设置：容量规格 - 选择“大容量规格”
                zbs 5.5.0
                zbs 5.6.0
                smtxos 6.1.0
                smtxos 6.2.0 p1
                zbs 5.4.0
                    不支持配置规格
                zbs 5.7.0
                    当前版本不支持zbs 5.7.0（不支持chunk 多实例）
                smtxos 5.1.5
                    不支持配置规格
                smtxos 6.0.0
                    不支持配置规格
            UI 改动
                配置存储页面  - 所有版本文案更新：请为每台主机选择容量规格，并指定 1 块容量最多为 2 TiB 的物理盘作为 SMTX 引导盘、2 块 SSD 作为 SMTX 系统盘。
                配置存储页面 - 文案提示：请为每台主机选择部署模式和容量规格。同一集群中所有主机的容量规格必须相同。
                配置存储页面 - 单个主机容量规格 - 默认与批量设置一致
                配置存储页面 - 修改单个主机容量规格后 多次批量修改容量规格 - 单个主机容量规格随批量主机容量规格变动
        部署
            smtxos 5.1.4
                不支持配置容量规格
            smtxos 5.1.5
                不支持配置容量规格
            smtxos 6.0.0
                不支持配置规格
            smtxos 6.1.0
                配置存储页面 - 批量设置：容量规格 - 默认为标准容量规格
                配置存储页面 - 批量设置：容量规格 - 标准容量规格提示：单个主机容量不超过 128 TB。需为每个主机指定 2 块容量至少 330 GiB 的 SSD 作为含元数据分区的%缓存盘%。
                配置存储页面 - 批量设置：容量规格 - 选择“标准容量规格” 部署成功
                配置存储页面 - 批量设置：容量规格 - “大容量规格” 提示：单个主机容量不超过 256 TB。需为每个主机指定 2 块容量至少 685 GiB 的 SSD 作为含元数据分区的%缓存盘%。
                配置存储页面 - 批量设置：容量规格 - 选择“大容量规格” 部署成功
            smtxos 6.2.0 p1
                配置存储页面 - 批量设置：容量规格 - 选择“标准容量规格” 部署成功
                配置存储页面 - 批量设置：容量规格 - 选择“大容量规格” 部署成功
                配置存储页面 - 批量设置：容量规格 - 标准容量规格提示：单个主机容量不超过 128 TB。需为每个主机指定 2 块容量至少 330 GiB 的 SSD 作为含元数据分区的%缓存盘%。
                配置存储页面 - 批量设置：容量规格 - “大容量规格” 提示：单个主机容量不超过 256 TB。需为每个主机指定 2 块容量至少 685 GiB 的 SSD 作为含元数据分区的%缓存盘%。
            配置存储页面 -  删除主文案「请为每台主机指定 2 块容量至少为 130GiB 的 SSD 作为含元数据分区的%缓存/数据%盘。」
                smtxos 6.0.0 - 不变
                smtxos 6.1.0 - 文案更改
                smtxos 6.2.0 - 文案更改
                smtxos 5.1.4
                    smtxos-514 提高系统分区大小到 185G
                smtxos 5.1.5
                    smtxos-514 提高系统分区大小到 185G
            配置存储页面 - 元数据分区盘大小检查
                smtxos 5.1.5
                标准容量规格
                    smtxos 6.1.0 - 文案更改
                        指定的磁盘大于330GiB - 部署成功
                        指定的磁盘小于330GIB - 报错：标准容量规格的 SMTX 系统盘的容量至少为 330 GiB。
                            提示：标准容量规格的含元数据分区的物理盘的容量至少为 330 GiB。
                    smtxos 6.2.0 - 文案更改
                        指定的磁盘大于480GB - 安装成功
                        指定的磁盘小于330GIB - 报错：标准容量规格的 SMTX 系统盘的容量至少为 330 GiB。
                            大容量规格的含元数据分区的物理盘的容量至少为 685 GiB。
                大容量规格
                    指定的磁盘大于960GB - 安装成功
                    指定的磁盘小于685 GIB - 报错：标准容量规格的 SMTX 系统盘的容量至少为 330 GiB。
                        大容量规格的含元数据分区的物理盘的容量至少为 685 GiB。
                smtxos 5.1.4
                    smtxos-514 提高根分区大小到 185G
                smtxos 6.0.0 - 不变（130G）
                    选择150G 的磁盘作为元数据分区的盘 - 检查通过
        连续安装部署
            smtxos 5.1.4
                不支持配置规格
            smtxos 5.1.5
                不支持配置规格
            smtxos 6.0.0
                不支持配置规格
            smtxos 6.1.0
                配置存储页面 - 批量设置：容量规格 - 选择“标准容量规格”
                配置存储页面 - 批量设置：容量规格 - 选择“大容量规格”
            smtxos 6.2.0
                配置存储页面 - 批量设置：容量规格 - 选择“标准容量规格”
                配置存储页面 - 批量设置：容量规格 - 选择“大容量规格”
        扩容
            smtxos 5.1.5
                不支持配置规格
            smtxos 6.0.0
                不支持配置规格
            smtxos 6.1.0
                集群为标准容量规格 - 扩容成功后节点为标准容量规格
                集群为大容量规格 - 扩容成功后节点为大容量规格
            smtxos 6.2.0 p1
                集群为标准容量规格 - 扩容成功后节点为标准容量规格
                集群为大容量规格 - 扩容成功后节点为大容量规格
        连续安装扩容
            smtxos 5.1.5
                不支持配置规格
            smtxos 6.0.0
                不支持配置规格
            smtxos 6.1.0
                集群为标准容量规格 - 扩容成功后节点为标准容量规格
                集群为大容量规格 - 扩容成功后节点为大容量规格
            smtxos 6.2.0 p1
                集群为标准容量规格 - 扩容成功后节点为标准容量规格
                集群为大容量规格 - 扩容成功后节点为大容量规格
    操作系统使用独立物理盘
        裸金属安装
            配置存储页面 - 批量设置：部署模式 - 操作系统与缓存/数据共享物理盘
                smtxos 5.1.5
                smtxos 6.1.0
                smtxos 6.2.0
                zbs 570
                smtxos 5.1.4
                    不支持配置
                    tl3
                smtxos 6.0.0
                    不支持配置
                zbs 560
                    不支持配置
            配置存储页面 - 批量设置：部署模式 - 操作系统使用独立物理盘
                smtxos 5.1.5
                批量设置 - 存在提示：N 台主机选择“操作系统使用独立物理盘”，我已确保：硬件 RAID 的 Write cache 已设置为 Write through 策略，否则存在数据丢失隐患。
                单个主机设置 - 存在提示：N 台主机选择“操作系统使用独立物理盘”，我已确保：硬件 RAID 的 Write cache 已设置为 Write through 策略，否则存在数据丢失隐患。
                不勾选 - submit 后报错 - 请确保硬件 RAID 的 Write cache 已设置为 Write through 策略。
                勾选 - 可以进行下一步
                smtxos 5.1.4
                    不支持配置
                    tl3
                smtxos 6.0.0
                    不支持配置
                smtxos 6.1.0
                    独立系统盘 + 标准容量规格
                        指定一块大于480GB 的系统盘 - 安装成功
                        未指定系统盘 - 报错：请指定 1 块物理盘作为 SMTX 系统盘。
                        指定的系统盘小于410GIB - 报错：标准容量规格的 SMTX 系统盘的容量至少为 410 GiB。
                            提示信息正确
                    独立系统盘 + 大容量规格
                        指定一块大于960GB 的系统盘 - 安装成功
                        未指定系统盘 - 报错：请指定 1 块物理盘作为 SMTX 系统盘。
                        指定的系统盘小于920GB - 报错：大容量规格的 SMTX 系统盘的容量至少为 920 GiB。
                smtxos 6.2.0
                    独立系统盘 + 标准容量规格
                        指定一块大于480GB 的系统盘 - 安装成功
                        未指定系统盘 - 报错：请指定 1 块物理盘作为 SMTX 系统盘。
                        指定的系统盘小于410GIB - 报错：标准容量规格的 SMTX 系统盘的容量至少为 410 GiB。
                            报错：标准容量规格的 SMTX 系统盘的容量至少为 410 GiB。
                    独立系统盘 + 大容量规格
                        指定一块大于960GB 的系统盘 - 安装成功
                        未指定系统盘 - 报错：请指定 1 块物理盘作为 SMTX 系统盘。
                        指定的系统盘小于920GB - 报错：大容量规格的 SMTX 系统盘的容量至少为 685 GiB。
                zbs 560
                    不支持配置
                zbs 570
                    独立系统盘 + 标准容量规格
                        指定一块大于480GB 的系统盘 - 安装成功
                        未指定系统盘 - 报错：请指定 1 块物理盘作为 SMTX 系统盘。
                        指定的系统盘小于330GIB - 报错：标准容量规格的 SMTX 系统盘的容量至少为 410 GiB。
                    独立系统盘 + 大容量规格
                        指定一块大于960GB 的系统盘 - 安装成功
                        未指定系统盘 - 报错：请指定 1 块物理盘作为 SMTX 系统盘。
                        指定的系统盘小于920GB - 报错：大容量规格的 SMTX 系统盘的容量至少为 920 GiB。
    ZBS 层次化改造
        「SSD」 细分为「NVMe SSD」「SATA/SAS SSD」
            裸金属安装
                smtxos 5.1.5  - 不区分
                smtxos 6.0.0 - 不区分
                smtxos 6.1.0 - 可以区分
                smtxos 6.2.0 - 可以区分
                zbs 5.5.0 - 不区分
                zbs 5.6.0 - 可以区分
                zbs 5.7.0  - 可以区分
            集群部署
                smtxos 6.0.0 - 不区分
                smtxos 6.1.0 - 可以区分
                smtxos 6.2.0 - 可以区分
        （部署）配置存储页面 - 分层模式文案改动 - 将物理盘的部分容量或高速物理盘作为缓存使用。
            smtxos 6.0.0 - 不变
            smtxos 6.1.0 - 文案更改
            smtxos 6.2.0 - 文案更改
            smtxos 5.1.4 - 文案不变
            smtxos 5.1.5 - 文案不变
        （连续安装部署）配置存储页面 - 分层模式文案改动 - 将物理盘的部分容量或高速物理盘作为缓存使用。
            smtxos 6.0.0 - 不变
            smtxos 6.1.0 - 文案更改
            smtxos 6.2.0 - 文案更改
            smtxos 5.1.4 - 文案不变
            smtxos 5.1.5 - 文案不变
        （部署）配置存储页面 - 系统盘用途
            所有主机的所有磁盘均是单一类型的nvme（开启 replica_cap_only  ） - 部署成功
            部分节点磁盘全是sata ssd，部分节点磁盘全是nvme - 部署成功（不开启replica_cap_only）
            不分层部署 - 全闪ssd  - 部署成功，（不开启replica_cap_only）
            不分层部署- 全闪nvme  - 部署成功，（不开启replica_cap_only）
            smtxos 6.1.0
            smtxos 6.2.0
            系统盘独立ssd - 不支持
            不挂载磁盘 - 部署成功
            连续安装部署 - 配置存储页面 - 磁盘用途更新 - 「SMTX OS 引导盘」更新为「SMTX 引导盘」
            连续安装部署 - 配置存储页面 - 文案更新 ：请为每台主机指定 1 块容量至少为 32 GiB 的物理盘作为 ESXi 系统盘。
            所有主机的所有磁盘均是单一类型的ssd（开启 replica_cap_only ） - 部署成功
                提示：所有主机的物理盘是同一类型 SSD。分层模式下，副本卷将仅使用容量层，仅纠删码卷会使用缓存层。
                元数据分区磁盘 - 用途为含元数据分区的数据盘
            部分节点是单一类型ssd，部分节点不是 - 部署成功（不开启replica_cap_only）
                元数据分区磁盘 - 用途为含元数据分区的缓存盘
            将磁盘用途切换为非推荐用途 - 提示：
                该用途不符合系统推荐用途。一般只有当系统判断的物理盘类型有误时，才需要手动修改用途。请谨慎修改。
        （扩容）
            全闪分层集群 - 扩容非全闪节点 - 禁止扩容
            所有主机的所有磁盘均是单一类型的ssd（开启 replica_cap_only ） - 部署成功
                提示：所有主机的物理盘是同一类型 SSD。分层模式下，副本卷将仅使用容量层，仅纠删码卷会使用缓存层。
                元数据分区磁盘 - 用途为含元数据分区的数据盘
            部分节点是单一类型ssd，部分节点不是 - 部署成功（不开启replica_cap_only）
                元数据分区磁盘 - 用途为含元数据分区的缓存盘
            不分层部署 - 全闪ssd  - 部署成功，（不开启replica_cap_only）
                元数据分区磁盘 - 用途为含元数据分区的数据盘
    支持部署和扩容时设置 ssh 登陆账号密码
        6.1.0 及以上
        zbs - 5.7.0 及以上
        （部署）配置scvm 密码
            导航新增 - 配置scvm密码
            配置scvm - 配置scvm密码 - 可以成功设置密码
            配置scvm - 配置scvm密码 - 密码默认加密
            配置scvm - 配置scvm密码 - 点击密码栏的小眼睛 - 可以正确显示密码
            配置scvm - 配置scvm密码 - 密码校验
                输入7位密码 - 报错：至少 8 位字符，必须包含数字、大小写英文字母和特殊字符。
                输入30位密码
                密码未包含数字
                密码未包含大写英文
                密码未包含小写英文
                密码未包含特殊字符
                空 - 部署成功 - 密码为： HC!r0cks + 序列号前8位
                密码包含空字符
                特殊字符密码：" \ < ©•¶§#$([{,<&|!HC!r0cks
                    中文，笑脸
        连续安装部署
            配置scvm - 配置scvm密码 - 可以成功设置密码
        扩容
            配置scvm - 配置scvm密码 - 可以成功设置密码
        连续安装扩容
            配置scvm - 配置scvm密码 - 可以成功设置密码
            密码与集群一致
            密码与集群不一致
            空 - 扩容成功 - 密码为：HC!r0cks + 序列号前8位
    部署集群/扩容时可以选择部分磁盘不加入存储池中
        部署
        连续安装部署
        扩容
        连续安装扩容
        大容量规格
        标准容量规格
        6.1.0
        5.1.5
    ISO 安装时调大 boot 分区 size
        5.1.4 - 回归
        6.1.0 - 回归(保持不变)
        安装
            smtxos 5.1.5
                arm
                    oe
                    tls
                hygon
                    oe
                    tls
                x86
                    oe
                    el7
            smtxos 6.2.0
                arm
                    oe
                hygon
                    oe
                x86
                    oe
                    el7
        部署
            5.1.5
            6.2.0
        连续安装部署
            5.1.5
            6.2.0
        扩容
            5.1.5
            6.2.0
        连续安装扩容
            5.1.5
            6.2.0
    适配鲲鹏天池服务器
        6.1.1
            arm
                oe
        6.2.0
            arm
                oe
        5.1.5
            arm
                oe
                tos
        5.1.4 回归
            arm
                oe
        5.0.7 回归
            arm
                oe
    应用场景
        同时安装标准容量规格与大容量规格
        同时安装系统盘独立ssd主机与 开启软raid主机
        6.2.0 集群添加 6.2.0 p1 节点
    支持新版本&旧版本回归
        安装
            smtxos
                6.1.0
                    arm
                        oe
                    hygon
                        oe
                    x86
                        oe
                        el7
                6.1.1
                    arm
                        oe
                    hygon
                        oe
                    x86
                        oe
                        el7
                6.2.0
                    acos
                    arm
                        oe
                            620 or 620 p1
                    hygon
                        oe
                    x86
                        oe
                        el7
                5.1.5
                    arm
                        oe
                        tos
                    hygon
                        oe
                        tos
                    x86
                        oe
                        el7
                6.0.0 回归
                    arm
                        oe
                    hygon
                        oe
                    x86
                        oe
                        el7
                5.1.4 回归
                    arm
                        oe
                        tos
                    hygon
                        oe
                    x86
                        oe
                        el7
                5.0.7 回归
                    arm
                        oe
                    hygon
                        oe
                    x86
                        oe
                        el7
            smtxelf
                6.0.0
                    arm
                    hygon
                    x86
                6.1.0
                    arm
                    hygon
                    x86
                6.2.0
                    arm
                    hygon
                    x86
            smtxzbs
                5.5.0 回归
                5.6.0
                5.6.1
        部署
            6.1.0
                x86
                    oe
                    el7
            6.1.1
                x86
                    oe
                    el7
            6.2.0
                x86
                    oe
                    el7
            5.1.5
                x86
                    oe
                    el7
            6.0.0 回归
                x86
                    oe
                    el7
            5.1.4 回归
                x86
                    oe
                    el7
            5.0.7 回归
                x86
                    oe
                    el7
        连续安装部署
            6.1.0
                x86
                    oe
                    el7
            6.1.1
                x86
                    oe
                    el7
            6.2.0
                x86
                    oe
                    el7
            5.1.5
                x86
                    oe
                    el7
            6.0.0 回归
                x86
                    oe
                    el7
            5.1.4 回归
                x86
                    oe
                    el7
            5.0.7 回归
                x86
                    oe
                    el7
        连续安装扩容
            6.1.0
                x86
                    oe
                    el7
            6.1.1
                x86
                    oe
                    el7
            6.2.0
                x86
                    oe
                    el7
            5.1.5
                x86
                    oe
                    el7
            6.0.0 回归
                x86
                    oe
                    el7
            5.1.4 回归
                x86
                    oe
                    el7
            5.0.7 回归
                x86
                    oe
                    el7
        tower
            4.5.0
            4.6.0
            4.4.1
            smtxos 5.0.7 hp1 + tower 3.4.5
            4.4.2
                回归
                tos
cluster installer 1.4.1
    arcfra版本
        测试范围
            没有中文
            logo 替换
            文案遮挡、溢出
            后台关键字
            文档
            关键字替换
                smartx
                smtx
                elf
                tower
            翻译内容
                界面上面文案翻译 - 没有严重的翻译错误
                部分报错文案、提示文案不容易触发，仅在代码中比较，需要研发帮忙提供代码中的中英文文案
                    http://gitlab.smartx.com/frontend/cluster-installer-ui/-/tree/CLUS-759/src/locales/en-US
                    英文比中文长很多的
            url 链接，kvm关键字
                http://172.20.206.33/installation/kvm/
            api
                x-smartx-token
        版本覆盖
            版本覆盖（arcfra）
                aocs
                    6.1.1
                    6.2.0
                        正式版本
                        hot fix版本
                esxi
                    7.0.3
                    8.0.2
                    8.0.3
                AOC
                    4.4.3
                    4.7.1
        功能覆盖
            esxi 安装
            acos 安装
                软raid
                硬raid
            vmware 部署
                rdma
                非rdma
            vmware 连续安装部署
                rdma
                非rdma
            VMware 连续安装扩容
                rdma
                非rdma
            aoc 安装
                大规格
                标准规格
    英文版
        版本覆盖&功能覆盖
            tower 4.7.1
            部署 vmware  -   6.1.1
            连续安装扩容vmware-     8.0U2d
            smtx elf 安装-   6.2.0
            smtx zbs 安装     -5.6.0
            安装smtxos
                配置信息页面
                    系统盘
                        硬raid 安装
                            6.2.0
        测试范围
            没有中文
            不存在acos\arcfra\aoc 关键字
            文案遮挡、溢出
            翻译内容
                执行用例时顺便执行，其余部分等英文文案出来后在代码中进行对比
        关键字保持smtx\tower
            通用页面
                开始新项目 - 选择功能
                登录页
                    登录页 - 服务条款
                    登录页 - 中英文切换 - 存在
                    登录页 - Copyright © 2022 SmartX Inc. All rights reserved.
                    登录页 - 左上角logo
                首页
                    首页 - 右上角切换语言
                    首页 - 右上角 - 关于- logo
                    首页 - 右上角 - 关于- copyright 替换
                    首页 - 全部项目 - 集群类型
                        SMTX OS（ELF 平台）
                        SMTX OS（VMware ESXi 平台）
                        首页 - 全部项目 - 功能
                            SMTX OS 安装
            查看项目配置
                SMTX OS 安装
                ESXi 安装
                部署vmware
                扩容VMware
                连续安装部署vmware
                连续安装扩容VMware
                smtx zbs 安装
                smtx elf安装
    中文版本（回归）
        版本覆盖&功能覆盖
            tower 4.4.3
            smtxos 安装
                软raid
                    5.1.5
            vmware 连续安装部署
                6.1.1
            VMware 扩容
                esxi
                    8.0U3e
        通用页面（关键字保持smtx\tower）
            开始新项目 - 选择功能
            登录页
                登录页 - 服务条款
                登录页 - 中英文切换 - 不存在
                登录页 - Copyright © 2022 SmartX Inc. All rights reserved.
                登录页 - 左上角logo
            首页
                首页 - 右上角切换语言
                首页 - 右上角 - 关于- logo
                首页 - 右上角 - 关于- copyright 替换
                首页 - 全部项目 - 功能   -  SMTX OS 安装
                首页 - 全部项目 - 集群类型
                    SMTX OS（ELF 平台）
                    SMTX OS（VMware ESXi 平台）
    适配新机型
        浪潮 CS5280H3
        联想 SR658H V2
    arcfra 版本关键字替换（UI）
        通用页面
            选择项目后上方：SMTX OS（VMware ESXi 平台）
            选择项目后上方：SMTX OS（ELF 平台）
            登录页
                登录页 - 服务条款 - 同acos 6.2.0
                浏览器标签名称
                登录页 - 中英文切换 - 不存在
                登录页 - Copyright © 2022 SmartX Inc. All rights reserved. - Copyright © 2025 Arcfra Pte. Ltd. All rights reserved.
                登录页 - 左上角logo替换
                登录页 - 用户名 - root
            首页
                首页 - 右上角切换语言 - 不允许
                首页 - 右上角 - 关于- logo替换
                首页 - 右上角 - 关于- copyright 替换
                首页 - 全部项目 - 集群类型     SMTX OS（ELF 平台）
                首页 - 全部项目 -  SMTX OS（VMware ESXi 平台）
                首页 - 全部项目 - 功能     SMTX OS 安装
                首页 - 新项目入口
                    支持：SMTX OS 安装。
                    SMTX OS（ELF 平台）
                    SMTX OS（VMware ESXi 平台）
                开始新项目 - 集群类型     SMTX OS（VMware ESXi 平台）     SMTX OS（ELF 平台）
                    SMTX OS（VMware ESXi 平台）
                    SMTX OS（ELF 平台）
                开始新项目 - 选择功能
                    配置 ESXi 主机 -> 创建 SCVM 并安装 SMTX OS -> 部署计算平台为 VMware ESXi 的 SMTX OS 集群。
                    在物理服务器中安装 ESXi 并配置管理网络 → 配置 ESXi 主机 → 创建 SCVM 并安装 SMTX OS →  部署计算平台为 VMware ESXi 的 SMTX OS 集群。
                    配置 ESXi 主机 → 创建 SCVM 并安装 SMTX OS →  将节点添加到计算平台为 VMware ESXi 的 SMTX OS 集群。
                    在物理服务器中安装 ESXi 并配置管理网络 → 配置 ESXi 主机 → 创建 SCVM 并安装 SMTX OS →  将节点添加到计算平台为 VMware ESXi 的 SMTX OS 集群。
                    SMTX OS 安装
                    在物理服务器中安装 SMTX OS。完成安装的服务器可用于部署新集群或加入已有集群。
        查看项目配置
            SMTX OS 安装
                安装文件名称
                功能 - SMTX OS 安装
                软件     - SMTX OS 5.1.0
                集群类型   -  SMTX OS（ELF 平台）
                物理盘用途
                    smtx 引导盘
                    smtx 系统盘
                        软raid 1 安装
                        独立ssd 安装
            部署vmware
                功能
                安装文件名称
                软件  -   SMTX OS 5.1.0
                集群类型     - SMTX OS（VMware ESXi 平台）
                物理盘      - ESXi 系统盘和 SMTX OS 引导盘
                smartx 密码
                tower 配置展示
                    替换为aoc
                    配置全新tower
                    右侧基本信息展示 - tower 替换
            扩容VMware
                功能
                安装文件名称
                软件     SMTX OS 5.1.0
                集群类型     SMTX OS（VMware ESXi 平台）
                物理盘   -  ESXi 系统盘和 SMTX OS 引导盘
                smartx 密码
            连续安装部署vmware
                功能
                安装文件名称
                软件     - SMTX OS 5.1.0
                集群类型  -   SMTX OS（VMware ESXi 平台）
                物理盘用途   -  ESXi 系统盘和 SMTX 引导盘 替换
                smartx 密码
                tower 配置展示
                    替换为aoc
                    关联已有tower
                    右侧基本信息展示 - tower 替换
                物理盘用途
                    ESXi 系统盘和 SMTX 引导盘 替换
            连续安装扩容VMware
                功能
                安装文件名称
                软件  -   SMTX OS 5.1.0
                集群类型  -   SMTX OS（VMware ESXi 平台）
                smartx 密码
                物理盘用途
                    ESXi 系统盘和 SMTX 引导盘 替换
            ESXi 安装
                集群类型     SMTX OS（VMware ESXi 平台）
        安装acos
            左上角功能名称替换     SMTX OS 5.1.0
            集群规模页面
                集群规模页面 - 关键字替换：填写待安装 SMTX OS 的主机 IPMI 信息，以获取 CPU 架构等信息。
            安装文件页面
                安装文件页面 - 选择文件下面 - SMTX OS
                安装文件页面 - 选择acos 文件
                安装文件页面 - 选择smtxos文件 - 不允许
                安装文件页面 - 为空安装文件 - 错误提示”请选择 SMTX OS 安装文件。“替换
                安装文件页面 - 错误提示”md5sum.txt 文件中未包含 SMTX OS 安装文件的 md5 值。“ 替换
                安装文件页面- 错误文案”md5sum.txt 文件中 SMTX OS 安装文件的 md5 值与所选文件不一致 。“ 替换
            配置信息页面
                配置信息页面 - 关键字替换：如不选择物理网口，则自动化安装 SMTX OS 后，Cluster Installer 将在操作系统中预制包含管理网络信息的配置脚本，可进入操作系统中选择物理网口并执行脚本，完成管理网络配置。
                执行安装弹窗 - 关键字替换：确认开始执行自动化安装 SMTX OS？
                系统盘
                    配置信息页面- 配置存储 - 磁盘类型替换：SMTX 系统盘
                    配置信息页面- 配置存储 - 关键字替换：请指定 2 块 SSD 作为 SMTX OS 系统盘。
                    配置信息页面- 配置存储 - 关键字替换：SMTX OS 系统盘的容量至少为 130 GiB。
                    配置存储 - 需为每个主机指定 1 块容量最多为 2 TiB 的物理盘作为 SMTX 引导盘、2 块 SSD 作为 SMTX 系统盘。
                    配置存储 - 需为每个主机指定 1 块盘作为 SMTX 系统盘。建议通过 Raid 控制器做 Raid1，且不与其他盘共用存储控制器。
                    配置存储 - 请指定 1 块物理盘作为 SMTX 系统盘。
                    配置存储 - 标准容量规格的 SMTX 系统盘的容量至少为 410 GiB。（硬raid）
                    配置存储 - 标准容量规格的 SMTX 系统盘的容量至少为 330 GiB。
                    配置存储 - 大容量规格的 SMTX 系统盘的容量至少为 920 GiB。（硬raid）
                    配置存储 - 大容量规格的 SMTX 系统盘的容量至少为 685 GiB。
                引导盘
                    配置信息页面 - 文案替换：请为每台主机指定 1 块容量最多为 2 TiB 的物理盘作为 SMTX OS 引导盘，2 块容量至少为 130 GiB 的 SSD 作为 SMTX OS 系统盘。
                    配置信息页面- 配置存储 - 关键字替换：请指定 1 块物理盘作为 SMTX OS 引导盘。
                    配置信息页面- 配置存储 - 关键字替换：SMTX OS 引导盘的容量最多为 2 TiB。
            自动化执行页面
                自动化执行页面 - 关键字替换：安装 SMTX OS
                自动化执行页面 - 关键字替换：正在安装 SMTX OS...
                自动化执行页面 - 关键字替换：安装 SMTX OS 失败
                关键字替换：SMTX OS 安装成功
        安装smtxzbs
            没有入口
        安装smtxelf
            没有入口
        安装esxi
            右上角功能名称替换
            livecd 文件 之前默认提供了一个smtxos版本的livecd文件
        部署 vmware
            右上角功能名称替换
            安装文件页面
                smtxos
                    安装文件页面 - 选择文件下面 - SMTX OS
                    安装文件页面 - 选择文件 - acos文件
                    安装文件页面 - 选择smtxos文件 - 不允许
                    安装文件页面 - 安装文件为空 - 错误提示”请选择 SMTX OS 安装文件。“替换
                    安装文件页面 - 错误提示”md5sum.txt 文件中未包含 SMTX OS 安装文件的 md5 值。“ 替换
                    安装文件页面- 错误文案”md5sum.txt 文件中 SMTX OS 安装文件的 md5 值与所选文件不一致 。“ 替换
                tower
                    安装文件页面 - 选择文件下面 - cloudtower
                    不使用 CloudTower
                    关联已有 CloudTower
                    部署全新 CloudTower
                        请选择 CloudTower 安装文件。
                        安装文件页面 - 错误提示”md5sum.txt 文件中未包含 CloudTower 安装文件的 md5 值。“ 替换
                        安装文件页面- 错误文案”md5sum.txt 文件中 CloudTower 安装文件的 md5 值与所选文件不一致 。“ 替换
            配置信息页面
                右侧目录 - 配置 CloudTower
                流量控制方式
                    开启rdma文案：执行部署前，请根据 SMTX OS 安装部署指南，在物理交换机中配置流量控制。
                配置 CloudTower
                    可选配置方式
                        配置全新 CloudTower
                        关联已有 CloudTower
                    部署全新 CloudTower
                        CloudTower IP
                        CloudTower 超级管理员用户名
                        CloudTower 超级管理员密码
                        CloudTower-子网掩码
                        请填写 CloudTower 超级管理员密码。
                        请填写 CloudTower IP。
                        请确认 CloudTower 集群超级管理员密码。
                        不属于 CloudTower 网络网段。
                    关联已有 CloudTower
                        CloudTower IP
                        连接 CloudTower
                        连接 CloudTower 成功。
                        无法连接 CloudTower IP 地址，请确认网络连通性。
                        请确认 CloudTower 的管理员用户名和密码正确。
                        请连接 CloudTower。
                配置集群
                    SMTX OS 集群名称
                    集群名称为空 - 请填写 SMTX OS 集群名称。
                    集群超级管理员密码为空 - 请填写 SMTX OS 集群超级管理员密码。
                    确认密码为空 - 请确认 SMTX OS 集群超级管理员密码。
            自动化执行页面
                部署成功 - 打开 CloudTower
                开启rdma部署成功提示：已自动为 ESXi 主机配置%流控方式%。请根据 SMTX OS 安装部署指南，在 SCVM 中验证流量控制的配置结果。
                安装 SMTX OS
                部署 SMTX OS 集群
                安装 CloudTower
        扩容vmware
            右上角功能名称替换
            关联集群弹窗
                关联集群弹窗  - SMTX OS 集群 IP
                关联集群成功后集群软件 - SMTX OS 5.1.0
            安装文件页面
                安装文件页面 - 选择文件下面 - SMTX OS
                安装文件页面 - 选择文件 - acos文件
                安装文件页面 - 选择smtxos文件 - 不允许
                安装文件页面 - 安装文件为空 - 错误提示”请选择 SMTX OS 安装文件。“替换
                安装文件页面 - 错误提示”md5sum.txt 文件中未包含 SMTX OS 安装文件的 md5 值。“ 替换
                安装文件页面- 错误文案”md5sum.txt 文件中 SMTX OS 安装文件的 md5 值与所选文件不一致 。“ 替换
            配置信息页面
                流量控制方式
                    开启rdma文案：执行部署前，请根据 SMTX OS 安装部署指南，在物理交换机中配置流量控制。
                配置集群
                    SMTX OS 集群名称
                    集群名称为空 - 请填写 SMTX OS 集群名称。
                    集群超级管理员密码为空 - 请填写 SMTX OS 集群超级管理员密码。
                    确认密码为空 - 请确认 SMTX OS 集群超级管理员密码。
            自动化执行页面 - 扩容集群中
                开启rdma部署成功提示：已自动为 ESXi 主机配置%流控方式%。请根据 SMTX OS 安装部署指南，在 SCVM 中验证流量控制的配置结果。
                安装 SMTX OS
                部署 SMTX OS 集群
        连续安装部署VMware
            右上角功能名称替换
            安装文件页面
                smtxos
                    安装文件页面 - 选择文件下面 - SMTX OS
                    安装文件页面 - 选择文件 - acos文件
                    安装文件页面 - 选择smtxos文件 - 不允许
                    安装文件页面 - 安装文件为空 - 错误提示”请选择 SMTX OS 安装文件。“替换
                    安装文件页面 - 错误提示”md5sum.txt 文件中未包含 SMTX OS 安装文件的 md5 值。“ 替换
                    安装文件页面- 错误文案”md5sum.txt 文件中 SMTX OS 安装文件的 md5 值与所选文件不一致 。“ 替换
                tower
                    安装文件页面 - 选择文件下面 - cloudtower
                    部署全新 CloudTower
                    关联已有 CloudTower
                    不使用 CloudTower
                    部署全新 CloudTower
                        请选择 CloudTower 安装文件。
                        安装文件页面 - 错误提示”md5sum.txt 文件中未包含 CloudTower 安装文件的 md5 值。“ 替换
                        安装文件页面- 错误文案”md5sum.txt 文件中 CloudTower 安装文件的 md5 值与所选文件不一致 。“ 替换
            配置信息页面
                右侧目录 - 配置 CloudTower
                配置密码 - Set the password for the default account of the SCVM's ACOS system.
                配置存储
                    配置存储 - 磁盘用途：ESXi 系统盘和 SMTX OS 引导盘
                    配置存储 - 磁盘用途下拉框 - ESXi 系统盘和 SMTX OS 引导盘
                流量控制方式
                    开启rdma文案：执行部署前，请根据 SMTX OS 安装部署指南，在物理交换机中配置流量控制。
                配置 CloudTower
                    可选配置方式
                        配置全新 CloudTower
                        关联已有 CloudTower
                    部署全新 CloudTower
                        CloudTower IP
                        CloudTower 超级管理员用户名
                        CloudTower 超级管理员密码
                        CloudTower-子网掩码
                        请填写 CloudTower 超级管理员密码。
                        请填写 CloudTower IP。
                        请确认 CloudTower 集群超级管理员密码。
                        不属于 CloudTower 网络网段。
                    关联已有 CloudTower
                        CloudTower IP
                        连接 CloudTower
                        连接 CloudTower 成功。
                        无法连接 CloudTower IP 地址，请确认网络连通性。
                        请确认 CloudTower 的管理员用户名和密码正确。
                        请连接 CloudTower。
                配置集群
                    SMTX OS 集群名称
                    集群名称为空 - 请填写 SMTX OS 集群名称。
                    集群超级管理员密码为空 - 请填写 SMTX OS 集群超级管理员密码。
                    确认密码为空 - 请确认 SMTX OS 集群超级管理员密码。
            自动化执行页面
                部署成功 - 打开 CloudTower
                开启rdma部署成功提示：已自动为 ESXi 主机配置%流控方式%。请根据 SMTX OS 安装部署指南，在 SCVM 中验证流量控制的配置结果。
                安装 SMTX OS
                部署 SMTX OS 集群
                安装 CloudTower
        连续安装扩容vmware
            右上角功能名称替换
            关联集群弹窗
                关联集群弹窗  - SMTX OS 集群 IP
                关联集群成功后集群软件 - SMTX OS 5.1.0
                当前集群的 SMTX OS 版本为 %版本号%。
            安装文件页面
                安装文件页面 - 选择文件下面 - SMTX OS
                安装文件页面 - 选择文件 - acos文件
                安装文件页面 - 选择smtxos文件 - 不允许
                安装文件页面 - 安装文件为空 - 错误提示”请选择 SMTX OS 安装文件。“替换
                安装文件页面 - 错误提示”md5sum.txt 文件中未包含 SMTX OS 安装文件的 md5 值。“ 替换
                安装文件页面- 错误文案”md5sum.txt 文件中 SMTX OS 安装文件的 md5 值与所选文件不一致 。“ 替换
            配置信息页面
                流量控制方式
                    开启rdma文案：执行部署前，请根据 SMTX OS 安装部署指南，在物理交换机中配置流量控制。
                配置集群
                    SMTX OS 集群名称
                    集群名称为空 - 请填写 SMTX OS 集群名称。
                    集群超级管理员密码为空 - 请填写 SMTX OS 集群超级管理员密码。
                    确认密码为空 - 请确认 SMTX OS 集群超级管理员密码。
            自动化执行页面 - 扩容集群中
                开启rdma部署成功提示：已自动为 ESXi 主机配置%流控方式%。请根据 SMTX OS 安装部署指南，在 SCVM 中验证流量控制的配置结果。
                安装 SMTX OS
                部署 SMTX OS 集群
    arcfra /英文版（UI）
        目标
            没有中文
            文案遮挡、溢出
            logo 替换
            翻译内容
                执行其他用例时顺便执行，其余部分等英文文案出来后在代码中进行对比
        弹窗
            acos 安装
                集群规模页面
                    重新获取主机信息
                    未获取到bmc信息时 - 手动选择弹窗
                    arm/hygon 的机器，需要禁止吗
                安装文件页面
                    重新收集硬件配置
                配置信息页面
                    执行安装失败
                    选择网卡时存储网络网速小于10G
                    选择网卡时网卡连接断开
                自动化执行页面
                    停止安装
                    重新执行
                    失败后退出
            esxi 安装
                集群规模页面
                    重新获取主机信息
                    未获取到bmc信息时 - 手动选择弹窗
                安装文件页面
                    重新收集硬件配置
                配置信息页面
                    执行安装失败
                    选择网卡时存储网络网速小于10G
                    选择网卡时网卡连接断开
                    配置过程中退出 button
                自动化执行页面
                    停止安装
                    重新执行
                    失败后退出
            部署
                集群规模页面
                    重新获取主机信息
                安装文件页面
                    重新收集硬件配置
                配置信息页面
                    执行部署失败
                    vcenter 选择主机故障响应
                    vcenter 选择主机隔离的响应
                    删除虚拟交换机
                    负载均衡模式选择
                    配置过程中退出 button
                自动化执行页面
                    停止安装
                    重新执行
                    失败后退出
            连续安装部署
                集群规模页面
                    重新获取主机信息
                安装文件页面
                    重新收集硬件配置
                配置信息页面
                    执行部署失败
                    vcenter 选择主机故障响应
                    vcenter 选择主机隔离的相响应
                    删除虚拟交换机
                    负载均衡模式选择
                    配置过程中退出 button
                自动化执行页面
                    停止安装
                    重新执行
                    失败后退出
            扩容
                集群规模页面
                    重新获取主机信息
                安装文件页面
                    重新收集硬件配置
                配置信息页面
                    执行部署失败
                    删除虚拟交换机
                    负载均衡模式选择
                    配置过程中退出 button
                自动化执行页面
                    停止安装
                    重新执行
                    失败后退出
            连续安装扩容
                集群规模页面
                    重新获取主机信息
                安装文件页面
                    重新收集硬件配置
                配置信息页面
                    执行部署失败
                    删除虚拟交换机
                    负载均衡模式选择
                    配置过程中退出 button
                自动化执行页面
                    停止安装
                    重新执行
                    失败后退出
        其他路径
            smtxelf 安装
            smtxzbs 安装
            esxi 安装
                等待时间过长提示
                管理网络
                    配置
                    未配置
            部署
                配置信息页面
                    分层部署
                    不分层部署
                    安装文件不存在
                    不开启rdma     - 无法启用 RDMA
                    配置过程中退出 button
                    网络相关
                        ip被占用
                        存储网络MTU 9000
                        分离部署
                        融合部署
                        移除关联网络
                        创建虚拟交换机
                        删除虚拟交换机
                        不开启rdma     无法启用 RDMA
                        新建关联网络
                            more button
                            分配物理网络适配器     -注意速率小于10G网卡的提示
                            网络选择
                        检查存储网络连通性
                            成功
                            失败
                    开启rdma
                        固件版本 Tip
                        流量控制方式
                自动化执行页面
                    失败后退出
                    等待时间过长提示
            连续安装部署
                配置信息页面
                    分层部署
                    不分层部署
                    安装文件不存在
                    不开启rdma     - 无法启用 RDMA
                    配置过程中退出 button
                    esxi主机 名称显示正确
                    网络相关
                        ip被占用
                        存储网络MTU 9000
                        分离部署
                        融合部署
                        移除关联网络
                        创建虚拟交换机
                        删除虚拟交换机
                        新建关联网络
                            more button
                            网络选择
                            分配物理网络适配器     - 注意速率小于10G网卡的提示
                        检查存储网络连通性
                            成功
                            失败
                    开启rdma
                        固件版本 Tip
                        流量控制方式
                自动化执行页面
                    失败后退出
                    等待时间过长提示
            smtxos 安装
                系统盘
                    硬raid 安装
                    软raid 安装
                管理网络
                    配置
                    未配置
                    等待时间过长提示