虚拟化管理
    ELF ( SMTX OS )
        虚拟机
            生命周期管理（资源变更）
                OVF 导入导出 【6.0.0 整理】
                    性能测试
                        OVF文件规格
                            虚拟机挂载尽可能多的设备类型（网卡·、磁盘等设备），导出OVF文件大于80kb，再导入，预期解析成功
            虚拟机属性
                基本信息属性
                    非 boost 模式磁盘队列数保持 1  （SMTXOS 620 P4）
                        新部署场景
                            vhost集群，查询/etc/libvirt/qemu.conf ：max_num_queues = 4
                            非vhost集群，查询/etc/libvirt/qemu.conf ：max_num_queues = 1
                        升级场景
                            vhost集群，从610升级到620P4，查询/etc/libvirt/qemu.conf ：max_num_queues = 4
                            非vhost集群，从610升级到620P4，查询/etc/libvirt/qemu.conf ：max_num_queues = 1
                        转换场景
                            非 vhost 转 vhost，zbs-cluster vhost enable 重启libvirtd,max_num_queues 由 1 变成 4
                            vhost 转非 vhost，zbs-cluster vhost disable ,重启libvirtd：max_num_queues 由 4 变成 1
                        安装hotfix
                            hotfix 安装场景：vhost集群，620安装620 HP4补丁，max_num_queues = 4
                            hotfix 安装场景：非vhost集群，620安装620 HP4补丁，max_num_queues = 1
                磁盘属性
                    虚拟卷支持TRIM/UNMAP【SMTXOS/ELF 6.0.0】
                        功能测试
                            discard 有效性检查
                                vmtools 磁盘默认驱动 + Windows 检查
                                    630-vmtools 4.1.0-widows 检查
                                        windows10 + vmtools4.1.0（默认驱动 virtio-win-0.1.266） - fio 10G 数据 trim unmap 磁盘空间回收检查成功
                                        windows11 + vmtools4.1.0（默认驱动 virtio-win-0.1.266） - fio 10G 数据 trim unmap 磁盘空间回收检查成功
                                        windows server 2016 + vmtools4.1.0（默认驱动 virtio-win-0.1.266） - fio 10G 数据 trim unmap 磁盘空间回收检查成功
                                        windows server 2019 + vmtools4.1.0（默认驱动 virtio-win-0.1.266） - fio 10G 数据 trim unmap 磁盘空间回收检查成功
                                        windows server 2022 + vmtools4.1.0（默认驱动 virtio-win-0.1.266） - fio 10G 数据 trim unmap 磁盘空间回收检查成功
                                        windows server 2025 + vmtools4.1.0（默认驱动 virtio-win-0.1.266） - fio 10G 数据 trim unmap 磁盘空间回收检查成功
                    支持 vhost-user-blk/scsi 硬件多队列【6.0.0】
                        兼容性测试
                            系统平台
                                SMTX OS
                                    x86
                                        Intel
                                            x86：Intel tencentos  vhost
                                            x86：Intel tencentos 非 vhost
                                        Hygon
                                            x86：hygon tencentos vhost
                                            x86：Intel tencentos 非 vhost
                                    Arm
                                        kunpeng
                                            arm：kunpeng tencentos vhost
                                            arm：kunpeng tencentos 非 vhost
                                        feiteng
                                            arm：feiteng tencentos vhost
                                            arm：feiteng tencentos 非vhost
        关联项目
            ELF 关联 SRE 功能
                ELF 报警
                    虚拟机开启 HA ，因其他主机内存不足触发报警
    虚拟化工具
        v2v
            功能测试
                v2v 工具安装
                    创建v2v 虚拟机-挂载 v2v iso，磁盘空间不够，安装 v2v iso
                    创建v2v 虚拟机-挂载 v2v iso，1 个 cpu，安装 v2v iso
                    创建v2v 虚拟机-挂载 v2v iso，1G mem，安装 v2v iso
                    创建v2v 虚拟机-挂载 v2v iso，没有网卡，安装 v2v iso
                    创建v2v 虚拟机-挂载 v2v iso，lsblk 返回的第一块盘不是 vd/sd，安装 v2v iso
                    创建v2v 虚拟机，添加多个磁盘，挂载 v2v iso，安装 v2v iso
                    创建v2v 虚拟机，系统盘是virto总线，挂载 v2v iso，安装 v2v iso
                    创建v2v 虚拟机，系统盘是scsi总线，挂载 v2v iso，安装 v2v iso
                    创建v2v 虚拟机，系统盘是ide总线，挂载 v2v iso，安装 v2v iso
                    网卡配置
                        v2v 配置了存储网络，驱动注入成功，迁移成功
                        v2v配置了接入网络，驱动注入成功，迁移成功
                    安装在 vmware
                        vmware 集群上传  arcfra v2v iso，创建虚拟机挂载 v2v iso 安装
                    安装在 elf 集群
                        通过 SMTX V2V  iso 安装
                        通过 SMTX V2V  ovf + vmdk安装
                        通过 ARCFRA V2V iso 安装
                        通过 ARCFRA V2V ovf + vmdk安装
                    安装在 ACOS 集群
                        通过 arcfra v2v iso 安装
                        通过 arcfra v2v ovf+vmdk 安装
                        安装在 ACOS 集群
                v2v 站点关联
                    修改站点的描述
                    添加站点的 api 里不能有明文密码
                    添加站点 v2v 日志里不能有明文密码
                    smtx 站点
                        添加  SMTXELF 站点（关联一个zbs存储）
                        添加 smtxelf 集群（关联多个zbs存储） -- v2v 1.6.1 里不支持
                        添加 smtxelf 站点，存储为 smtxos集群 -- v2v 1.6.1 里不支持
                        修改站点的用户名
                        修改站点的密码
                        修改站点的用户名和密码
                        集群配有接入网络
                v2v 任务
                    创建任务
                        选择源端和目标端
                            不同源端
                                从 vcenter 6.x 迁移
                                从 esxi 8.x 迁移
                                从 esxi 7.x 迁移
                                源端为 SMTXOS 6.2.X
                                源端为 ACOS 6.1.x
                                源端为 ACOS 6.2.x
                                源端为 SMTXOS 6.1.X
                                源端为 SMTXOS 6.0.X
                                源端为 SMTXOS 5.1.X
                                源端为 SMTXOS 5.0.X
                                源端为 SMTXOS  双活集群
                                源端为 SMTXOS intel vhost集群
                                源端为 SMTXOS  hygon 集群
                                源端为 SMTXOS 6.2.X EC 存储
                                源端为 SMTXOS 6.2.X 副本存储
                                源端为 SMTXOS 6.2.X EC 策略比源端高
                                源端为 SMTXOS 6.2.X EC 策略比源端低
                            不同目标集群
                                迁移到 smtxos 6.3.0 集群
                                迁移到 smtxos intel e7 集群
                                迁移到 smtxos intel oe 集群
                                迁移到 smtxos hygon oe 集群
                                迁移到 smtxelf 6.2.x  集群
                                迁移到 smtxelf 6.0x  集群
                                迁移到 smtxelf intel oe集群
                                迁移到 smtxelf hygon oe集群
                                迁移到 ACOS 6.3.X 集群
                                迁移到 ACOS 6.1.X 集群
                                迁移到 ACOS 集群（EC 存储）
                                迁移到 ACOS 集群（副本）
                                迁移到 兆芯 smtxos620 hp3 集群
                                迁移到 acos intel el7 集群
                                目标集群存储策略降级为副本后创建迁移任务，预期不展示EC 策略
                        选择待迁移的虚拟机
                            虚拟机/boot分区空间不够，迁移失败，错误信息里明确提示空间不足
                            windows uefi 虚拟机，驱动注入成功，迁移成功
                            windows bios 虚拟机，驱动注入成功，迁移成功
                            linux bios 虚拟机，驱动注入成功，迁移成功
                            linux uefi 虚拟机器，驱动注入成功，迁移成功
                            虚拟机不同磁盘配置
                                虚拟机有1个快照，迁移成功
                                虚拟机有 virtio、scsi和 ide磁盘
                                源端虚拟机磁盘为 IDE
                                源端虚拟机磁盘为 SCSI
                                源端虚拟机磁盘为 VIRTIO
                                迁移虚拟机 usb 挂载着 vmtools，迁移到 目标端检查虚拟机挂载的 vmtools iso已自动移除
                                迁移虚拟机 cdrom 挂载着 vmtools 和 cloud-init
                            资源预估
                                elf-elf，为副本时预计需要的数据空间大小=磁盘总大小*副本数，不区分精简置备和厚置备，ec 的计算公式与vmware-efl一样
                                elf-elf，为 EC时，预计需要的数据空间大小与 vmware - elf 一致
                                预计需要的数据空间不区分精简还是厚置备
                            虚拟机不同网卡配置
                                虚拟机有 VPC 网卡
                        自定义虚拟机配置项
                            虚拟机网卡配置
                                设置静态IP
                                    smtxos 迁移到 acos，自定义虚拟机配置-虚拟机网卡项没有设置静态IP地址的项
                                    acos 迁移到 acos，自定义虚拟机配置-虚拟机网卡项没有设置静态IP地址的项
                                    acos 迁移到 smtxos，自定义虚拟机配置-虚拟机网卡项没有设置静态IP地址的项
                            预估需要的数据空间和可用空间
                                elf-elf时选副本策略，精简置备和后置备锁需要的数据空间相同
                                elf-elf时选副本策略，预计需要的数据空间大小直接用磁盘总大小*副本数
                    任务队列
                        任务操作
                            任务执行过程中v2v日志里不能有明文密码
                            全量迁移
                                虚拟机存储在 NFS 上，迁移的数据大小为磁盘的总大小
                                虚拟机存储在 VMFS、vSAN 或 VVol上，只迁移有效数据，迁移数据大小为磁盘已使用大小
                            任务完成
                                迁移成功
                                    迁移成功数据确认
                                        磁盘检查
                                            目标端 windows 虚拟机的所有磁盘自动 online
            兼容性测试
                Guest OS 兼容性
                    vmware to elf
                        Rocky >=8.7
                        ubuntu >+22.04
                        windows 2016
                        windows 2019
                        windows 2022
                        windows 2025
                        rhel9
                        ubuntu24
                        openEuler22.03
                        oraclelinux9.2
                路径兼容性测试
                    vmware - ELF
                        vmware8 - SMTXOS intel vhost 6.2.x
                        vmware8 - SMTXELF(关联一个zbs) intel 6.2.x
                        vmware7 - SMTXOS hygon  6.1.x
                        vmware7 - SMTXOS oe vhost 5.1.x
                        vmware7 - SMTXELF(关联一个zbs)
                        vmware6 - SMTXOS intel non-vhost 5.0.x
                        vmware6 - SMTXELF(关联一个zbs) intel non-vhost 6.0.x
                    vmware -AVE
                        vmware8 -ACOS 6.2.x
                        vmware7 - ACOS  6.2.x
                        vsphere client5  - ACOS  6.1.x
                    ELF-AVE
                        SMTXOS intel vhost 6.2.x - ACOS 6.2.x
                        SMTXOS hygon 6.1.x - ACOS 6.1.x
                        SMTXOS 双活  5.1.x - ACOS 6.2.x
                        SMTXOS 6.0.x - ACOS 6.2.X
                        SMTXOS 5.0.X - ACOS 6.2.X
                        SMTXOS 5.0.5+ - ACOS 6.2.X
                        smtxos 5.0.5+ - smtxos 6.2.x
                    ELF-ELF
                        SMTXOS 双活  5.1.x - SMTXOS 6.2.x
                        SMTXOS 双活  5.1.x - SMTXELF(关联一个zbs) intel 6.2.x
                        smtxos 6.2.x  - smtxos 6.2.x
                        smtxos 6.1.x - smtxos 6.2.x
                        smtxos 6.0.x - smtxos 6.2.x
                        smtxos 5.0.x - smtxos 6.2.x
                        intel - hygon，迁移关机的虚拟机
                        hygon  - intel，迁移开机的虚拟机
                        intel - arm，迁移关机的虚拟机，任务失败【以后会禁止这条迁移路径】
                        arm - intel，任务成功，但虚拟机在目标端开机后无法进入系统
                    AVE-AVE
                        ACOS 6.2.x inte el7 - ACOS 6.2.x
                        ACOS 6.1.X - ACOS 6.2.X
                        ACOS 6.2.X - SMTXOS 6.2.X
            故障测试
                数据异常
                    驱动注入失败
                        设置静态IP
                            少于4个磁盘的虚拟机，目标端创建虚拟机，磁盘为 ide
                            ide cdrom 挂载 vmtools iso
                                4个磁盘的虚拟机，目标端创建虚拟机，前3个磁盘为 ide，其余为 scsi
                                35个磁盘的虚拟机，目标端创建虚拟机，前3个磁盘为 ide，其余32个为 scsi
                                36个磁盘的虚拟机，任务失败，目标端无法创建虚拟机
                            usb cdrom 挂载 vmtools iso
                                4个磁盘的虚拟机，目标端创建虚拟机，前4个磁盘均为 ide
                                36个磁盘的虚拟机，目标端创建虚拟机，前4个磁盘为 ide，其余32个磁盘为 scsi
                                37个磁盘的虚拟机，任务失败，目标端无法创建虚拟机
                        不设置静态IP
                            4个磁盘的虚拟机，目标端创建虚拟机，磁盘均为 ide
                            36个磁盘的虚拟机，目标端创建虚拟机，前4个磁盘为ide，其余为scsi
                            37个磁盘的虚拟机，任务失败，目标端不创建虚拟机
            安全测试
                绿盟扫描 ARCFRA V2V
                绿盟扫描 SMTX V2V
                端口扫描
                Qualys 漏扫
            bugfix
                v2v 日志里站点连接的密码是 **** 替代
                vmware 到 smtx 的迁移，虚拟机4+磁盘且驱动注入失败场景，预期迁移成，前4块盘是ide，后面的磁盘是scsi
            目标虚拟机回归测试
                smtxos
                    虚拟机编辑（cpu、mem、disk、net）
                    虚拟机电源操作
                    虚拟机集群内迁移
                    虚拟机跨集群迁移 - 热迁移
                    虚拟机跨集群迁移 - 分段迁移
                    VMTools 基本功能
                    vmtools 升级
                    vmtools 编辑网卡
                smtxelf
                    虚拟机编辑
                    虚拟机电源操作
                    虚拟机集群内迁移
                    虚拟机跨集群迁移 - 热迁移
                    虚拟机跨集群迁移 - 分段迁移
                    VMTools 基本功能
                    vmtools 升级
                    vmtools 编辑网卡
                acos
                    虚拟机编辑
                    虚拟机电源操作
                    虚拟机集群内迁移
                    虚拟机跨集群迁移 - 热迁移
                    虚拟机跨集群迁移 - 分段迁移
                    VMTools 基本功能
                    vmtools 升级
                    vmtools 编辑网卡
            final buiild 测试
                smtxos iso final build 检查
                    final 包 准备
                    final 版本回归
                    final 版本安全扫描
                    Smartx v2v  UI 信息检查(logo及各处文案)
                arcfra iso final build 检查
                    final 包 准备
                    final 版本回归
                    final 版本安全扫描
                    Arcfra v2v  UI 信息检查(logo及各处文案)
            版本更新
                Tower 纳管 v2v
                    多个 tower 纳管同一个 v2v，tower1 创建迁移任务，tower2里的v2v自动更新
                    多个 tower 纳管同一个 v2v，tower2 暂停此迁移任务，tower1里的v2v自动更新
                    多个 tower 纳管同一个 v2v，tower1 停止迁移任务，tower2 里的 v2v 自动更新
                    通过纳管从 SMTXOS 迁移虚拟机到 ACOS
                    通过纳管从 VMWARE 迁移虚拟机到 ACOS
                    通过纳管从 ACOS 迁移虚拟机到 ACOS
                    通过纳管从 ACOS 迁移虚拟机到 SMTXOS
                    添加 SMT 迁移工具
                        没有添加 v2v 时的初始展示
                        关闭添加 STMX 迁移工具小弹窗
                        取消添加 STMX 迁移工具
                        添加token 已过期的 v2v，操作成功
                        添加 v2v 服务停止的 v2v，操作失败
                        添加已关机的v2v，操作失败
                        变更v2v 用户名的密码后再添加v2v
                        删除已添加的 v2v后再次添加
                        添加多个 SMTX 迁移工具
                        添加部署在 vmware 集群上的 SMTX 迁移工具
                        添加部署在 ELF 集群上的 SMTX 迁移工具
                        添加 v2v 160
                        添加 v2v 150
                        添加 v2v 140
                        添加 暂停状态的 v2v ，操作失败
                        添加  SMTX V2V
                        添加 ARCFRA 2V
                        IP地址
                            输入正确的 IP 地址
                            输入的IP地址前后多加空格
                            输入不匹配的IP地址
                            输入非IP 格式的地址
                            输入已添加的 v2v 的 IP地址
                            输入IP地址带端口 :80
                            输入IP地址带端口 :443
                            不输入IP地址
                        用户名
                            输入正确的用户名
                            输入匹配的用户名但前后有空格
                            输入不匹配的用户名
                            不输入用户名
                        密码
                            输入正确的密码
                            输入不匹配的密码
                            不输入密码
                        描述
                            输入有效的描述
                            输入多段有效的描述，有换行
                            输入超长的描述
                            输入含有特殊字符的描述
                            输入含中文的描述
                            拉长描述输入框
                    删除迁移工具
                        删除 - 确定，删除成功
                        删除 - 取消
                        删除已不存在的v2v(v2v ip 地址变了)，删除成功
                        删除token已过期的v2v，删除成功
                        删除已关机的v2v，删除成功
                        v2v 有迁移任务时删除，删除成功
                        删除 ARCFRA V2V
                        删除 SMTX V2V
                    alpha 插件的安装和卸载
                        arm 平台 安装 tower + 安装 arm 版 alpha 插件
                        Intel x86 平台 安装 tower + 安装 amd64 版 alpha 插件
                        hygon x86 平台 安装 tower + 安装 amd64 版 alpha 插件
                        Intel x86 tower 升级，alpha 插件的使用不受影响
                        hygon x86 tower 升级，alpha 插件的使用不受影响
                        arm tower 升级，alpha 插件使用不受影响
                        卸载 intel x86 上的 alpha 插件
                        卸载 hyon x86 上的 alpha 插件
                        卸载 arm上的 alpha 插件
                        卸载 arm上的 alpha 插件后再次安装 alpha 插件
                        卸载 Intel x86 上的 alpha 插件后再次安装 alpha 插件
                        tower 460
                        tower 450
                        tower 441
                        更新 alpha 插件
                    打开迁移工具
                        打开 SMTX 迁移工具管理窗口
                        打开运行中的 v2v
                        打开v2v用户密码已变更的v2v
                        打开 token 已过期的v2v，操作成功，token自动更新了
                        打开已关机的 v2v，v2v展示：获取任务列表遇到问题
                        打开已暂停的 v2v，v2v展示：获取任务列表遇到问题
                        打开 v2v 服务已停止的 v2v，v2v展示：获取任务列表遇到问题
                        打开已被删除的 v2v（v2v的 IP变了），v2v提示：获取任务列表遇到问题
                        切换不同的 v2v 窗口
                        关闭迁移工具窗口
                        打开 ARCFRA V2V
                        打开 SMTX V2V
                v2v 1.6.0定制版  +  vmtools3.2.1 定制版-上海普洛斯投资
                    v2v1.6.0 及 rpm 包的安装和配置
                        安装 v2v 1.6.0 正式发布版 iso，并配置 v2v
                        下载 v2v rpm包
                        升级 v2v rpm包
                        添加源端站点
                        添加源端站点
                    创建迁移任务
                        运行中的虚拟机，设置静态IP
                        关机的虚拟机，设置静态IP
                        4+个磁盘运行中的虚拟机，设置静态IP
                        批量迁移多个虚拟机（覆盖：运行中，关机、设置静态IP、不设置静态IP）
                        运行中多网卡多虚拟机网络的虚拟机，设置静态IP
                        自动安装 vmtools 3.2.1
                        自动移除 vmtools 3.2.1 iso
                        RHEL 7.9
                        RHEL 8.7
                        CentOS 7.6
                        Ubuntu 20.04
                        目标集群没有 vmtools3.2.1 iso
                        虚拟机内执行 uninstall 卸载 vmtools321
                        通过 编辑磁盘-添加cdrom-挂载 vmtools 321 再次安装
                        迁移 linux 虚拟机（禁用了usb_storage和删除了tmp 目录）
                        迁移 linux 虚拟机（没有禁用 usb_storage也没删除tmp 目录）
                        迁移windows server 2022设置静态IP
                        源端虚拟机配置了2个网卡（分别设置vmnetwork 和 zbs 网络的静态 IP），迁移时保留源端虚拟机IP
                    故障测试
                        v2v 安装 vmtools 321 iso 失败后，vmtools321 iso 自动移除，通过tower编辑磁盘cdrom，挂载 vmtools321 iso，安装，再移除 iso
                        vmtools 321 iso 遗留在目标端虚拟机内，通过 tower 编辑磁盘cdrom，移除 vmtools321 iso
                        构造 4个 磁盘虚拟机驱动注入失败，vmtools iso 挂载失败场景，设置静态IP
                        构造 自动移除 vmtools 3.2.1 iso 失败，通过 tower 手动移除
                        构造 vmtools 3.2.1 安装成功，但设置静态IP失败的场景
                        构造自动安装 vmtools 3.2.1 失败
                        构造 4+个 磁盘虚拟机驱动注入失败，任务失败36，目标端无法创建虚拟机
                        虚拟机一个磁盘（驱动注入失败），设置静态IP，虚拟机迁移到目标端，磁盘ide，vmtools 安装，静态IP设置成功。
                v2v 1.6.1 支持从 smtxos 迁移至 acos
                    站点
                        通过 集群 ip 添加 smtx 站点，443 端口
                        通过集群 ip 添加 acos 站点，80 端口
                        smtx v2v - info API 返回 vendor 信息为SMTX
                        arcfra v2v - info API 返回 vendor 信息为 ARCFRA
                        ARCFRA V2V 添加SMTXOS站点
                        ARCFRA V2V 添加 ACOS 站点
                        ARCFRA V2V 创建任务时源端站点下拉框可选项：vmware，SMTX 站点， ACOS站点
                        ARCFRA V2V 创建任务时目标站点下来框可选项：ACOS 站点、 SMTX站点
                        ARCFRA V2V 编辑 SMTXOS 站点
                        ARCFRA V2V 添加 SMTXOS 站点后删除，再添加
                        ARCFRA V2V  添加 SMTXO 站点但输入 ACOS 集群的信息，失败
                        ARCFRA V2V  添加 ACOS 站点但输入 SMTXOS 集群的信息，失败
                        ACOS 站点授权过期
                        ACOS 站点账户密码变更
                        SMTX V2V 添加 SMTXOS 站点
                        SMTX V2V 创建任务时源端站点下拉框可选项有：vmware，SMTX 站点， ACOS 站点
                        SMTX V2V 创建任务时目标站点下来框可选项：ACOS 站点、 SMTX站点
                        SMTX V2V 添加 ACOS 站点
                        SMTX V2V 修改 ACOS 站点的用户名和密码
                        SMTX V2V 添加 ACOS 站点后删除，再添加
                        SMTX V2V 添加 ACOS 站点但输入 SMTXOS 集群的信息，失败
                        SMTX V2V  添加 SMTXOS 站点但输入 ACOS 集群的信息，失败
                    cross-vendor 开关
                        cross-vendor 开关（api /api/v3/v2v/info 里 cross_vendor_enabled）默认为 false
                        ARCFRA V2V 禁用 cross-vendor，无法添加 SMTXOS 站点
                        SMTX V2V 禁用 cross-vendor，无法添加 ACOS 站点
                        smtx v2v 启用 cross-vendor，能添加 ACOS 站点
                        arcfra v2v 启用 cross-vendor，能添加 smtxos 站点
                        arcfra v2v 启用 cross-vendor后，能编辑 smtxos 站点
                        禁用 cross-vendor，站点里不展示已添加的 cross-vendor 节点
                        禁用 cross-vendor，导出迁移到 ACOS 站点的任务，操作成功
                        禁用cross-vendor，ARCFRA V2V 无法创建 ELF 到 ACOS 的迁移任务
                        禁用cross-vendor，SMTX V2V 无法创建 ELF 到 ACOS 的迁移任务
                        从 SMTX 迁移到 ACOS 过程（全量迁移）中禁用 cross-vendor
                        从 SMTX 迁移到 ACOS 过程（增量迁移）中禁用 cross-vendor
                        从 SMTX 迁移到 ACOS 过程（cutover）中禁用 cross-vendor
                        从 SMTX 迁移到 ACOS 过程（一致性校验）中禁用 cross-vendor
                        stmx v2v 启用 cross-vendor后，编辑 acos 站点
                    设置静态IP（v2v1.6.1里不支持）
                        没安装 vmtools 且运行中的虚拟机迁移到目标端且设置静态IP
                        没安装 vmtools  且关机的虚拟机迁移到目标端且设置静态IP
                        没安装 vmtools  且未知状态的虚拟机迁移到目标端且设置静态IP
                        已安装 vmtools 且 svt运行中的虚拟机迁移到目标端且设置静态IP
                        已安装 vmtools 但 svt 服务未运行的虚拟机迁移到目标端且设置静态IP
                        已安装 vmtools 且关机状态的虚拟机迁移到目标端且设置静态IP
                        已安装 vmtools 且 暂停的虚拟机迁移到目标端且设置静态IP
                        已安装 vmtools 且未知状态的虚拟机迁移到目标端且设置静态IP
                        已安装 vmtools 且有 static ipv4 网卡的虚拟机迁移到目标端，设置静态IP
                        已安装 vmtools 且有 static ipv4 和 ipv6  网卡的虚拟机迁移到 目标端，设置静态IP
                        源端虚拟机已通过 vmtools 配置 dns，迁移到目标端且设置ip
                        源端虚拟机未通过 vmtools 配置 dns，迁移到目标端且设置ip
                        已安装低版本 vmtools 虚拟机，迁移到目标集群（高版本 vmtools）且设置静态IP
                        已安装高版本 vmtools 虚拟机，迁移到目标集群（低版本vmtools）且设置静态IP
                    存储策略
                        创建任务设置2副本精简存储策略
                        创建任务设置3副本后置备存储策略
                        创建任务设置 EC 存储策略
                        多磁盘，设置副本和 EC 存储策略迁移到目标端（默认为副本策略）
                        多磁盘，设置副本和 EC 存储策略迁移到目标端（默认EC策略）
                        创建迁移任务时存储策略选择：与源端保存一致（v2v 1.6.1 里不支持）
                    源端虚拟机配置
                        虚拟机只有系统盘（ide 总线），迁移后添加 scsi + virtio 磁盘
                        虚拟机只有系统盘（scsi总线），迁移后添加 vritio 盘
                        虚拟机只有系统盘（virtio 总线），迁移后添加 scsi 盘
                        虚拟机有虚拟卷
                        虚拟机有共享虚拟卷，目标端此卷的 type 类型变更为 虚拟卷
                        虚拟机有 cdrom且挂载了 iso
                        虚拟机 usb 挂载了vmtools 映像，目标端虚拟机没有挂载 vmtools
                        没安装 vmtools 且运行中的虚拟机迁移到目标端
                        没安装 vmtools  且关机的虚拟机迁移到目标端
                        没安装 vmtools  且未知状态的虚拟机迁移到目标端，无法提交迁移任务
                        已安装 vmtools 且 svt运行中的虚拟机迁移到目标端
                        已安装 vmtools 但 svt 服务stopped的虚拟机，目标端虚拟机开机后 svt 服务自启动
                        已安装 vmtools 且关机状态的虚拟机迁移到目标端，无法提交迁移任务
                        已安装 vmtools 且 暂停的虚拟机迁移到目标端，提交任务失败【1.6.1,170里将优化为不可选】
                        已安装 vmtools 且未知状态的虚拟机迁移到目标端
                        已安装 vmtools 且有 static ipv4 网卡的虚拟机迁移到目标端，开机后虚拟机没有获取到IP
                        已安装 vmtools 且有 static ipv4 和 ipv6  网卡的虚拟机迁移到 目标端，开机后虚拟机没有获取到IP
                        源端虚拟机已通过 vmtools 配置 dns，迁移到目标端
                        源端虚拟机未通过 vmtools 配置 dns，迁移到目标端
                        dhcp 网卡的虚拟机迁移到目标端
                        网络服务stop的虚拟机迁移到目标端
                        源端虚拟机有sriov 网卡，目标端移除了sriov，替换为普通网卡
                        源端虚拟机有pci网卡，目标端删除了pci 网卡，比源端少一块网卡
                        源端虚拟机有挂载usb设备，目标端虚拟机不保留这个usb 设置
                        源端虚拟机网卡配置trunk网络，创建迁移任务时保持这个网络
                        源端虚拟机网卡配置storage网络，创建迁移任务时保持这个网络
                        源端虚拟机网卡有流量限制且目标集群高于50x
                        源端虚拟机网卡流量限制且目标端集群为50x时，目标端虚拟机不保留源端设置的流量限制
                        源端虚拟机有定义放置组规则只在某个主机开机，目标端虚拟机不保留放置组规则
                        源端虚拟机cpu独占，目标端虚拟机不保留cpu独占属性
                        源端虚拟机vcpu 配置了 QoS 策略，目标端不保留 QoS 策略
                        源端虚拟机有快照，目标端虚拟机不保留快照
                        源端虚拟机快照个数限制
                        源端集群和目标端集群都开启了数据加密且虚拟机的虚拟卷已开启数据加密，迁移成功，目标端虚拟机磁盘按开启了数据加密？？？-待产品定义
                        源端集群版本为 6.2.x且虚拟机的虚拟卷已开启数据加密，但目标集群没有开启数据加密，迁移成功，目标集群虚拟机磁盘没有开启加密
                        源端虚拟机开启恢复时同步时间，目标集群版本高于等于505
                        源端虚拟机开启恢复时同步时间，目标集群版本低于505，迁移到目标端后虚拟机没有此属性
                        源端虚拟机挂载了加密控制器或 GPU（没有加密控制器，挂载 GPU），目标端虚拟机没有挂载此设备
                        源端虚拟机磁盘开启常驻缓存迁移时保留默认设置2副本精简，且目标集群也开启了常驻缓存，目标端虚拟机磁盘保留厚置备和启用常驻缓存
                        源端虚拟机磁盘开启常驻缓存，但目标集群没有开启常驻缓存，创建迁移任务磁盘使用默认设置，目标端虚拟机磁盘策略是精简没有常驻缓存
                        源端虚拟机正在进行集群内迁移
                        源端虚拟机正在进行跨集群迁移，创建迁移任务成功，只需要源端虚拟机还在，迁移不受影响
                        源端虚拟机有 关联VPC 网卡，迁移到目标集群，目标端虚拟机没有此网卡
                        迁移由 cloud-init 创建的虚拟机
                            迁移已由cloud-init 设置静态IP的虚拟机到目标端
                            迁移cloud-init 虚拟机（没有设置静态IP）到目标端
                            迁移 cloud-init虚拟机（有初始化DNS）到目标端
                            迁移  cloud-init 虚拟机（没有初始化DNS）到目标端
        SMTX VMTools
            故障测试
                虚拟机内部故障
                    虚拟机根分区不足
                        虚拟机磁盘空间不够安装 vmtools 失败
                        虚拟机磁盘空间不够自动升级 vmtools 失败
                    虚拟机网络服务故障
                        NetworkManager
                            安装 VMTools
                                虚拟机内 NM 服务低于 1.0  （rhel 6.5）时安装 vmtools
                                虚拟机内 NM 服务为 1.0 或1.0以上版本时安装 vmtools
                                虚拟机内 NM 服务停止时安装 vmtools
                            升级 VMTools
                                虚拟机内 NM 服务低于 1.0  （rhel 6.5）时升级 vmtools
                                虚拟机内 NM 服务为 1.0 或1.0以上版本时升级 vmtools
                                虚拟机内 NM 服务停止时升级vmtools
                            虚拟机设置网卡
                                虚拟机内 NM 服务停止时编辑网卡设置IPv4
                                虚拟机内 NM 服务停止时编辑网卡设置IPv6
                                虚拟机内 NM 服务停止时编辑网卡设置IPv4 和 ipv6
                        systemd-networkd
                            虚拟机内 systemd-networkd 服务停止时安装 vmtools
                            虚拟机内 systemd-networkd 服务停止时升级 vmtools
                            虚拟机内 systemd-networkd 服务停止时编辑网卡设置ipv4
                            虚拟机内 systemd-networkd 服务停止时编辑网卡设置ipv6
                            虚拟机内 systemd-networkd 服务停止时编辑网卡设置ipv4 和ipv6
                        networking
                            虚拟机内 networking 服务停止时安装 vmtools
                            虚拟机内 networking 服务停止时升级 vmtools
                            虚拟机内 networking 服务停止时编辑网卡设置ipv4
                            虚拟机内 networking 服务停止时编辑网卡设置ipv6
                            虚拟机内 networking 服务停止时编辑网卡设置ipv4 和 ipv6
                        network-scripts
                            虚拟机内 network 服务停止时安装 vmtools
                    网卡配置异常
                        网卡配置文件 HWADDR 不是当前 mac 地址
                            虚拟机网卡设置 ipv4 静态 ip， 预期设置成功
                            虚拟机网卡设置 ipv6 静态 ip， 预期设置成功
                VMTools ISO 故障
                    上传 VMTools ISO 过程中，删除本地 VMTools ISO 文件
            功能测试
                SVT 状态
                    Restricted
                        虚拟机做升级虚拟机工具，同时在虚拟机内部做 cdrom 弹出 iso，会概率出现 Restricted
                虚拟机工具的安装和卸载
                    虚拟机工具外部操作 ISO
                        USB 挂载和弹出【OS 5.0.5】
                            挂载 虚拟机工具 ISO
                                虚拟机以usb cdom 方式挂载 vmtools iso后热插拔磁盘
                                虚拟机以ide cdrom 方式挂载 vmtools iso后热插拔磁盘
                                虚拟机ide cdrom 加满后挂载vmtools iso，然后热插拔磁盘
                                不受 CDROM 个数限制
                                    虚拟机有4个ide磁盘，热插拔其他类型磁盘后挂载虚拟机工具或升级虚拟机工具
                    虚拟机内部操作脚本
                        安装 VMTOOLS
                            环境检查
                                windows10虚拟机注册表里HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows NT\CurrentVersion 的 ProductName不为 Windows 10，安装vmtools
                            安装
                                虚拟机内 NM 服务正常运行时安装 vmtools
                                虚拟机内 network 服务正常运行时安装 vmtools
                                虚拟机内 systemd-networkd (ubuntu-server 20.04)正常运行时安装 vmtools
                GuestOS信息收集与展示
                    SVT 运行时
                        虚拟机详情显示最近收集到的 GuestOS 静态信息 - 虚拟机操作系统版本
                        虚拟机详情显示最近收集到的 GuestOS 静态信息 - 虚拟机内核版本
                        虚拟机详情显示最近收集到的 GuestOS 静态信息 - 虚拟机网卡的 ipv4 信息
                        虚拟机详情显示最近收集到的 GuestOS 静态信息 - 虚拟机网卡的 ipv6 信息
                        虚拟机详情显示最近收集到的 GuestOS 静态信息 - 虚拟机的 dns
                        虚拟机详情显示最近收集到的 GuestOS 静态信息 - 虚拟机工具状态和版本信息
                        前端显示最近收集到的 GuestOS 静态信息 - 虚拟机磁盘内部设备名
                        前端显示最近收集到的 GuestOS 静态信息 - 虚拟机磁盘大小
                        前端显示最近收集到的 GuestOS 静态信息 - 虚拟机磁盘分区使用量
                        虚拟机内部 staic 网卡断开后，vmtools 数据采集，不同 guestos行为不同
                        虚拟机列表展示虚拟机的ipv4和ipv6地址
                        虚拟机列表展示虚拟机工具版本
                        虚拟机列表展示虚拟机工具状态
                        虚拟机列表展示虚拟机客户机操作系统
                        虚拟机列表展示虚拟机cpu使用率
                        虚拟机列表展示虚拟机内存使用率
                        性能数据采集
                            日志检查，使用 qga-qmp 命令获取
                            在线增加 vcpu ，新一轮性能数据采集正常
                            在线增加 vcpu 到20以上，查看新一轮采集到的 cpu 数据
                            在线增加 mem，新一轮性能数据采集正常
                            虚拟机内 SMTX VMTools/svt 服务重新启动后，恢复性能数据采集
                            宿主机 vmtools-agent服务重启后，恢复性能数据采集正常
                            虚拟机暂停恢复后，恢复性能数据采集正常
                            虚拟机集群内迁移，新一轮性能数据采集正常
                            虚拟机跨集群热迁移后，新一轮性能数据采集正常
                            虚拟机跨集群分段迁移后，新一轮性能数据采集正常
                            虚拟机跨集群冷迁移后，新一轮性能数据采集正常
                            如果 /proc/meminfo 中有 MemAvailable 字段，则使用 MemAvailable 代替可用内存来计算内存使用率
                            如果没有 MemAvailable 字段，则使用cal_mem.sh脚本算 available 内存
                        VMTools 支持采集/设置项
                            虚拟机内核版本，展示正确
                            虚拟机主机名，设置/展示 正确
                            虚拟机 ip，修改静态 ipv4、ipv6 正确，展示正确
                            虚拟机 DNS， 设置/展示 正确
                            客户机操作系统的 NTP 服务器，设置成功
                            客户机操作系统的账户密码， 设置成功
                            虚拟机工具状态和版本，展示正确
                            虚拟机磁盘分区使用率，展示正确
                            虚拟机 CPU、内存性能采集项，展示正确
                            虚拟机 vmtools 版本低于3.2.0，手动给网卡配置ipv6，集群版本低于620，前端不展示ipv6
                GuestOS信息修改和展示
                    网卡信息编辑(ipv4,vmtools320以前)
                        修改网卡
                            虚拟机内网卡mac地址和网卡配置文件里的mac地址不一致时设置静态IP，成功
                    重置 NTP 服务器
                        设置 NTP 后重启虚拟机， NTP 不会丢失
                    DNS 编辑
                        网卡配置文件末尾没有换行符时设置dns成功
                    虚拟机账户密码编辑
                        重置账户后重启虚拟机，重置的密码依然生效
                    支持 IPv6 地址配置（VMTools 320 + smtxos620）
                        禁用 ipv6 路由的虚拟机，vmtools 能正常采集和配置数据
                        IP地址格式
                            ipv6
                                网关为长格式
                                网关为压缩格式
                        多网卡配置
                            添加网卡
                                添加 nic1（ipv4和ipv6均为 dhcp），nic2仅设置ipv4不设置默认网关，nic3 仅设置ipv6不设置默认网关
                                添加nic1（ipv4和ipv6均为 dhcp），nic2仅设置 ipv4和默认网关，nic3 仅设置ipv6和默认网关
                                添加nic1（ipv4和ipv6均dhcp），nic2同时设置ipv4和ipv6，均不设置默认网关，nic3同时设置ipv4和ipv6且均设置默认网关
                        不支持ipv6的场景
                            虚拟机内的ipv6 路由禁用时，vmtools正常工作
                    IP 冲突检测（tower450+smtxos620）
                        自动检测
                            两个网卡设置相同的ipv6地址，但一个是长格式，一个是宿写格式
                对已有资源的操作
                    虚拟机克隆
                        虚拟机普通克隆， 新虚拟机展示虚拟机工具版本和原虚拟机展示一致
                        虚拟机完全拷贝克隆， 新虚拟机展示虚拟机工具版本和原虚拟机展示一致
                        有cloudinit创建的有静态IP的虚拟机克隆后，修改新虚拟机的网卡IP，成功
                    虚拟机迁移
                        Tower 跨集群迁移
                            跨集群热迁移
                                非 vhost 低版本（如515）迁移到高版本（如620）
                                vhost 低版本（如515）迁移到高版本（如620）
                            跨集群分段迁移
                                当前版本（如515）迁移到高版本（如620）
                                当前版本（如515）迁移到同版本（如515）
                                当前版本（如515）迁移到底版本（如507）
                            跨集群冷迁移
                                当前版本（如515）迁移到高版本（如620）
                                当前版本（如515）迁移到同版本（如515）
                                当前版本（如515）迁移到底版本（如507）
                        集群内热迁移
                            集群内冷迁移成功，开机后虚拟机工具保持运行状态
                            集群内热迁移成功，虚拟机工具保持运行状态
                VMTools 支持执行脚本【vmtools3.2.3及以上】
                    ELF 记录虚拟机 EXECUTE_COMMAND 事件-成功
                    ELF 记录虚拟机 EXECUTE_COMMAND 事件-失败
                    记录成功的用户事件「使用虚拟机工具执行命令行」，包含：path，args，env
                    记录失败的用户事件「使用虚拟机工具执行命令行」，包含：path，args，env
                    API 请求参数
                        args
                            执行单条有效命令
                            执行单条无效命令
                            执行多条有效命令
                            一个参数里写多个命令用分号分隔（存在异常命令），全部都会执行，分别返回 stdout 和 stderr
                            一个参数里写多个命令用&&分隔（存在异常命令），失败后的命令不会继续执行
                            多个参数里各对应命令（存在异常命令），执行到异常命令后结束，后续的命令仅是作为参数不会执行
                            执行单个有效脚本
                            执行单个无效脚本
                            执行多个脚本，中间存在异常脚本
                            执行脚本，有权限
                            执行脚本，没有权限
                            支持 sh
                            支持 bash
                            支持 Cshell（unix）
                            支持 Zsh（macOS (≥ Catalina)）
                            支持 Ksh（IBM AIX、部分商业 Unix）
                            支持 Dash（轻量级Shell，ubuntu 6.10 开始）
                            支持 windows cmd
                            支持 windows powershell
                            脚本输入字符长度在 160k 以内的命令
                            脚本输入字符长度超过160k 的命令
                            不传 args
                            传 args ，值为空或none
                            args 含有多个参数
                            含有单引号
                            含有双引号
                            含有转义符号
                            含有中文字符
                            含有管道
                            含有代码段
                            含有重定向到文件，有写权限
                            含有重定向到文件，没有写权限
                        envs
                            传有效的 envs，一个环境变量
                            传 envs，多个有效的环境变量
                            传 envs，多个有环境变量，第一个为无效的后面的有效
                            不传 envs
                            传 envs 但值为空
                        path
                            不传 path，提示：'path' is required\"
                            传有效的 path
                            传 path，含中文目录
                            传path，子目录层级多
                            传 path，目录名称含特殊字符
                            windows 路径
                        capture_output
                            capture_output 为 true
                            capture_output 为 false，无输出
                            不传 caputre_output，默认为false
                            capture_output 设置为字符串
                        timeout
                            timeout 字符类型
                            timeout 为 0，按默认20秒执行
                            传timeout，值为空，执行失败，报语法错
                            timeout 值前后含有空格，自动过滤掉
                            不传 capture_output，按默认20秒执行
                            timeout 为 有效值
                            timeout 值中间有空格，执行失败
                            itmoue 设置为超过最大值 2147483648，执行失败，提示：got invalid value
                            timeout设置为最大值 2147483642（2147483647依然提示超过最大值）
                    API 响应参数
                        输出 小于1M
                        输出大于1M，输出自动截断
                        stderr 小于1M
                        stderr 大于1M，输出自动截断
                        输出内容含有中文
                        输出内容为英文
                        脚本执行成功，return code=0
                        脚本执行失败，return_code 返回 非0，且有 error信息
                        脚本执行中主动终止
                        脚本执行中被动终止
                    虚拟机不同状态时执行脚本
                        虚拟机关机时执行脚本，失败，提示：SVT_DOMAIN_NOT_RUNNING
                        虚拟机暂停时执行脚本，失败，提示：SVT_SERVICE_NOT_CONNECTED
                        虚拟机svt未运行时执行脚本，失败，提示：SVT_SERVICE_NOT_CONNECTED
                        虚拟机集群内热迁移时执行脚本，期间会 SVT_DOMAIN_NOT_RUNNINNG
                        虚拟机未知状态时执行脚本，失败
                        虚拟机重启时时执行脚本，期间会有SVT_SERVICE_NOT_CONNECTED
                        虚拟机在回收站时执行脚本，失败，提示：SVT_DOMAIN_NOT_RUNNING
                        虚拟机彻底删除后执行脚本，失败，提示：Domain not found
                        虚拟机导出时执行脚本，失败，提示：SVT_DOMAIN_NOT_RUNNING
                        虚拟机跨集群热迁移时执行脚本
                        打一致性时执行脚本，是否成功？
                    脚本类型
                        执行 fio 加负载命令
                        执行网络配置命令，例如：配置网卡IP
                        执行用户管理命令，例如：创建用户，修改密码
                        执行磁盘管理的命令。例如：磁盘分区、格式化
                        执行文件复制删除命令
                        执行文件传输命令
                        含有安装命令： yum install -y xxx
                        含有常用命令：find、cat、grep、sed、awk、wc
                        含有 echo，print
                        执行 python 脚本
                        执行 shell 脚本
                        执行 java 脚本
                        执行 db 脚本
                        执行 bat
                        执行 .exe
                        执行 .msi
                    异常场景
                        内存不够时执行命令失败：REST_UNKNOWN_ERROR
                        磁盘空间不够时执行命令成功，返回: no space left
                        执行过程中写文件冲突，执行失败：REST_UNKNOWN_ERROR
                        执行过程中超时，返回：SVT_TIMEOUT
                        虚拟机没有安装 vmtools 时执行脚本失败
                        虚拟机的vmtools版本低于3.2.2时执行脚本失败
                        虚拟机 CPU 使用率极高时执行脚本，没有影响
                        宿主机 libvirt 服务未运行时执行脚本失败
                        宿主机 vmtools-agent 未运行时执行脚本失败
                    安全设置
                        通过命令行 开启 支持执行脚本
                        通过命令行 关闭  支持执行脚本
                        tower 登录账户有「通过虚拟机工具变更虚拟机」角色，可以执行脚本
                        tower 登录账户没有「通过虚拟机工具变更虚拟机」角色，无法执行脚本
                        集群启用 execute_guest_command，可以执行脚本
                        集群禁用 execute_guest_command，执行脚本失败，提示：SVT_CLUSTER_CAPABILITY_DISABLED
            UI 测试
                虚拟机工具管理
                    升级虚拟机工具
                        已安装低版本，已挂载同版本 VMTools ISO
                            【VMTools >= 4.0.0, 且集群 >= OS515 or OS630】， 触发虚拟机挂载虚拟机工具映像 ， 升级虚拟机工具
                            【VMTools < 4.0.0, 集群 < OS515 or OS630】， 不支持触发虚拟机内部升级 VMTools
                        已安装低版本，已挂载高版本 VMTools ISO
                            手动给虚拟机 cdrom 挂载一个比集群版本高的vmtools iso，执行升级虚拟机工具
                        升级入口
                            FIsheye UI 升级 - 不再维护
                                单个虚拟机做升级虚拟机工具
                            Tower UI 升级
                                单个升级【仅挂载高版本 VMTools ISO】（smtxos514\smtxos620）
                                    Tower 虚拟机列表，虚拟机详情做升级虚拟机工具，可以触发自动升级。
                                单个升级【挂载 VMTools ISO + 虚拟机内部自动升级】(smtxos515\smtxos630)
                                    Tower 虚拟机列表，虚拟机详情做升级虚拟机工具，可以触发自动升级。
                                批量升级【挂载 VMTools ISO + 虚拟机内部自动升级】(smtxos630)
                                    Tower 虚拟机列表，批量选择虚拟机做批量升级虚拟机工具，可以触发自动升级。（任务中心是一个虚拟机一个任务）
                                    Tower 虚拟机列表，选择一个虚拟机做批量升级虚拟机工具，可以触发自动升级。
                            不支持升级的场景
                                检查虚拟机类型
                                    Tower 回收站， 不支持（UI 没有操作入口）
                                    副本虚拟机，不支持（UI 没有操作入口）
                                    系统服务虚拟机，不允许对系统服务虚拟机做升级虚拟机工具（UI 没有操作入口）
                                    虚拟机未安装虚拟机工具，UI 没有升级操作入口
                                低版本 VMTools 已采集数据且虚拟机内部已卸载 SVT
                                    【VMTools >= 4.0.0, 且集群 >= OS515 or OS630】， 触发虚拟机挂载最新 VMTools ISO ，不能触发升级虚拟机工具
                                    【VMTools < 4.0.0, 集群 < OS515 or OS630】， 触发虚拟机挂载最新 VMTools ISO
                        后端任务
                            j集群已上传的VMTools >= 4.0.0
                                集群 6.x >=  OS630 或 5.x >= OS515
                                    触发虚拟机挂载最新 VMTools ISO ， 同时自动触发虚拟机内部升级 VMTools
                                    虚拟机工具升级任务成功后，自动弹出 VMTools ISO
                                    虚拟机工具升级任务失败后，保留 VMTools ISO（不做弹出，保留环境做定位）。
                                集群 6.x <  OS630 或 5.x < OS515
                                    触发虚拟机挂载最新 VMTools ISO
                            集群上已上传的VMTools < 4.0.0
                                触发虚拟机挂载最新 VMTools ISO
                        未安装最新版本 VMtools
                            【集群已上传的VMTools >= 4.0.0, 且集群 >= OS515 or OS630】，虚拟机已挂载未安装最新版本， UI  可以触发升级
            集群运维
                集群新部署
                    5.1.5
                        新部署 （SMTX OS 5.1.5+ ）， 上传 VMTools 4.0.0 升级虚拟机工具到 4.0.0， 虚拟机工具升级触发的是：自动升级
                    6.3.0
                        新部署 （SMTX OS 6.3.0+）， 上传 VMTools 4.0.0 升级虚拟机工具到 4.0.0， 虚拟机工具升级触发的是 ： 自动升级， 可以批量触发自动升级
                集群升级+vmtools升级
                    低版本版本升级到最新集群版本，上传最新 VMTools
                        SMTX OS 4.0.10 （ VMTools 2.12.1 ）升级到到新 SMTX OS + VMTools 版本
                        SMTX OS 5.0.3 （ VMTools  3.0.0 ） 升级到到新 SMTX OS + VMTools 版本
                        SMTX OS 5.0.5 （ VMTools  3.0.1 ） 升级到到新 SMTX OS + VMTools 版本
                        SMTX OS 5.0.7 （ VMTools  3.0.2 ） 升级到到新 SMTX OS + VMTools 版本
                        SMTX OS 5.1.3 （ VMTools  3.0.2 ） 升级到到新 SMTX OS + VMTools 版本
                        SMTX OS 5.1.4 （ VMTools  3.1.1 ） 升级到到新 SMTX OS + VMTools 版本
                        SMTX OS 5.1.5 （ VMTools  4.0.0 ）升级到到新 SMTX OS + VMTools 版本
                        SMTX OS 6.0.0 （ VMTools  3.0.3 ）升级到到新 SMTX OS + VMTools 版本
                        SMTX OS 6.1.1-hp1 （ VMTools  3.1.0 ）升级到到新 SMTX OS + VMTools 版本
                        SMTX OS 6.2.0-hp1 （ VMTools  3.2.0 ）升级到到新 SMTX OS + VMTools 版本
                    支持自动升级的版本升级到高版本
                        SMTX OS 5.1.5/6.3.0 升级到 SMTX OS 6.3.0+ ， 可以升级，保持有自动升级功能
                    【cdrom 方式挂载】 升级到 【usb 方式挂载】
                        集群从低于505的版本升到505，然后从505升到最新版本
                        vmtools3.2.2 升级到最新版本
                        vmtools3.2.0 升级到最新版本
                        vmtools3.1.1 升级到最新版本
                        vmtools3.1.0 升级到最新版本
                        vmtools3.0.3升级到最新版本
                        vmtools3.0.2升级到最新版本
                        vmtools3.0.1升级到最新版本
                        vmtools3.0.0升级到最新版本
                        vmtools2.12.1升级到最新版本
                        windows 虚拟机 vmtools1.0.0升级到最新版本
            VMTools - 版本更新
                4.0.0
                    批量升级虚拟机工具【5.1.5】
                        批量触发（全部支持做升级）
                            连续多次触发，累计 100 个虚拟机做自动升级（如 2 分钟内触发 100 个虚拟机做自动升级）
                            批量选择 - 运行中虚拟机，已安装不同低版本虚拟机工具（windows、linux）- 批量升级成功
                        批量选择（部分支持升级）， UI 检查
                            批量选择 - 不同状态虚拟机 - 不允许触发批量升级
                            批量选择 - 虚拟机已安装不同版本虚拟机工具（含最新版本）- 不允许触发批量升级
                        批量选择（全部不支持升级）， UI 检查
                            批量选择 - 非运行状态虚拟机 - 不允许触发批量升级
                            批量选择 - 虚拟机已安装最新版本虚拟机工具 - 不允许触发批量升级
                    自动升级 VMTOOLS【5.1.5/6.3.0】
                        已有 SVT 不同状态做升级
                            SVT 未运行
                                有挂载低版本虚拟机工具，UI 不支持触发升级，仅支持安装
                                未挂载低版本虚拟机工具，UI 不支持升级，仅支持安装
                            SVT 运行中
                                有挂载低版本虚拟机工具，支持触发升级
                                未挂载低版本虚拟机工具，支持触发升级
                            SVT 已卸载
                                有挂载低版本虚拟机工具，不支持触发升级，仅支持安装
                                未挂载低版本虚拟机工具，不支持升级，仅支持安装
                        故障场景
                            自动升级触发的挂载 ISO 失败
                                虚拟机有其他异步任务，自动升级任务因资源锁问题失败
                                USB 控制器挂载数量已满， 预期本次任务失败
                                升级过程中虚拟机内强制弹出的 vmtools iso /dev/srx，任务失败
                            自动升级触发的虚拟机内部升级失败
                                执行升级脚本过程
                                    安装文件所在分区空间不足【本次新增，升级有检查，安装过程暂时没有检查】，升级失败
                                    有脚本 SMTX_VMTools_UPGRADER.sh 但是无法执行（如没有执行权限） ，升级失败
                                    ip-manager、gspawn-win64-helper.exe 、qga   交叉新旧版本，检查版本不一致情况 （ 升级失败的情况下存在版本不一致的情况 ），升级成功
                                    VMTools 获取（读/写）锁失败，升级失败
                                    虚拟机内部本地 version 文件手动修改为其他版本号， 升级成功
                                    获取版本，执行 guest-info 失败， 升级失败。
                            升级结果判断
                                升级执行超时失败
                                升级后 qga 不稳定（频繁重启），升级失败
                                虚拟机安装或升级高版本 qga， UI 不支持做升级
                            自动升级 VMTools 过程中对虚拟机做操作
                                kill vm qemu pid，预期本次任务失败
                                虚拟机 crash，预期本次任务失败
                                虚拟机所属主机存储网络故障，预期本次任务失败，HA 成功
                                虚拟机系统盘只读（zbs 命令行设置只读或者没有磁盘所权限），升级失败
                                虚拟机内部重启，预期本次任务失败
                                虚拟机内部关机，预期本次任务失败
                                虚拟机内部 kill qga pid，预期本次任务失败
                                虚拟机内部 qga hang（ 暂停进程来模拟， kill -STOP [进程号] ），预期本次任务失败
                            服务异常
                                虚拟机所属主机 VMTools-agent 服务重启， 升级成功 或者 失败，其中失败信息不包含服务异常。
                                虚拟机所属主机 job-center-worker 服务重启，升级失败。
                            升级任务自动弹出 VMTools iso 失败
                                弹出 vmtools iso
                        升级过程中同步执行其他操作
                            虚拟机触发重启、关机、暂停 ， 检查任务失败，提示资源被锁住
                            触发一致性快照， 检查任务失败，提示资源被锁住
                            VMTools 设置项 ，界面上不允许操作，API 操作会提示获取锁失败
                    VMTools Linux 安装脚本移除对 /tmp 目录依赖
                        安装
                            虚拟机内部没有  /tmp 目录，VMTools 安装成功
                            虚拟机内部有  /tmp 目录但是没有权限，VMTools 安装成功
                        升级
                            虚拟机内部没有  /tmp 目录，VMTools 升级成功
                            虚拟机内部有  /tmp 目录但是没有权限，VMTools 升级成功
                    VMTools  Windows 安装升级时同步安装 ballooon 驱动
                        安装
                            虚拟机内部没 balloon 驱动时， 安装 VMTools 后自动完成 balloon 驱动安装
                            虚拟机内部有 balloon 驱动时， 安装 VMTools 时 balloon 不会重新安装
                        升级
                            虚拟机内部没 balloon 驱动时， 升级 VMTools 后自动完成 balloon 驱动安装
                            虚拟机内部有 balloon 驱动时， 升级 VMTools 时 balloon 不会重新安装
                    OS515 + VMTools 4.0.0 自动升级匹配兼容性
                        集群、Tower、VMTools 版本兼容
                            Tower 4.4.2 + SMTX OS 5.1.5 + VMTools 4.0.0， 支持自动升级
                            Tower 4.6.0 + SMTX OS 5.1.5  + VMTools 4.0.0， 支持单个自动升级，不支持批量操作
                            Tower 4.x (适配 OS 630 )  + SMTX OS 5.1.5 + VMTools 4.0.0， 支持批量自动升级
                            Tower 4.x (适配 OS 630 ) + SMTX OS 6.3.0 / 5.1.5 + VMTools 4.0.0， 支持批量自动升级
                            SMTX OS 5.1.5 / SMTX OS 6.3.0 + VMTools 小于 4.0.0 的版本， 不支持自动升级
                            低于 SMTX OS 5.1.5 / SMTX OS 6.3.0 + VMTools 4.0.0， 不支持自动升级
                4.1.0
                    包含 virtio win 266 驱动
                        windows server 2016 安装 vmtools
                        windows server 2019 安装 vmtools
                        windows server 2022 安装 vmtools
                        windows server 2025 安装 vmtools
                        windows 10 安装 vmtools
                        windows 11 安装 vmtools
                        没有安装过 vmtools 的虚拟机安装新版本 vmtools
                        卸载虚拟机的老版本驱动和vmtools后安装新版本 vmtools
                        虚拟机系统盘为 IDE的虚拟机安装 vmtools新版本，之后修改虚拟机系统盘总线为vritio，开机系统能识别
                        虚拟机系统盘为 scsi 的虚拟机安装 vmtools新版本（不需要）
                        虚拟机系统盘为 virtio 的虚拟机安装 vmtools新版本（不需要）
                        检查虚拟机 QGA 版本升级到指定版本（不需要）
                        通过 ELF API 更新驱动（不需要）
                        安装 vmtools 后修改系统盘（原为 ide）总线为 virtio，开机后系统正常运行（不需要，自动化里执行）
                        安装 vmtools 后热添加 virtio+scsi 磁盘，操作成功能虚拟机内能识别（不需要自动化里执行）
                        安装 vmtools 后关机冷添加 ide磁盘和cdrom，挂载 iso，开机后虚拟机内能正常识别（不需要自动化里执行）
                        安装 vmtools 后重启虚拟机，虚拟机正常
                        安装 vmtools 后再次安装 vmtools，不再安装驱动
                        windows 7 不在支持范围，安装 vmtools，驱动是 172
                    新增 GuestOS 兼容性
                        新增 windows server 2025 vmtools 兼容性测试
                        新增 Tencent OS 4.2 vmtools 兼容性测试
                        Tencent OS 4.2 设置 dns，成功，重启虚拟机 dns 保持不变
                        NM 的状态不影响设置DNS：Tencent OS 4.2 停止 NM 服务后设置 dns，成功且 NM 服务不受影响依旧是停止状态
                        Tencent OS 3.1设置 dns，成功
                    一致性快照优化+优化采集磁盘分区文件系统使用率
                        虚拟机磁盘挂载到/mnt/后从tower UI上删除磁盘，创建一致性快照成功，数据同步后成功获取磁盘分区使用率
                        虚拟机磁盘挂载到/mnt/后从tower UI上卸载磁盘，创建一致性快照成功，数据同步后成功获取磁盘分区使用率
                        虚拟机多个数据盘，挂载到不同目录，然后删除一个磁盘，卸载一个磁盘，还有磁盘保持正常mount，创建一致性快照，数据同步后成功获取磁盘分区使用率
                    性能采集优化
                        通过给lnux虚拟机(uos)续增加 cpu 负载，观察 采集的 cpu  与实际一致，没有高于100% 和负值
                        测试 windows 虚拟机，持续增加 cpu 负载，观察 采集的 cpu 与实际一致，没有高于100% 和负值
                        ubuntu 22.04 虚拟机，stop  SVT 服务，虚拟机内执行脚本注入故障，宿主机执行ext-guest-get-perf-stats 返回 -nan，不影响执行 guest-info
                    安装优化
                        支持 NM 且版本高于 1.0.0 的虚拟机，安装 vmtools 成功
                        支持 NM 但版本低于1.0.0, 的虚拟机，安装 vmtools 成功
                        不支持 NM 的虚拟机，安装 vmtools 成功
                        给 opensuse11.4 桌面版虚拟机安装 vmtools ，成功
                        支持 NM 且版本高于 1.0.0 的虚拟机，升级 vmtools，操作成功
                        支持 NM 但版本低于1.0.0, 的虚拟机，升级vmtools，操作 成功
                        不支持 NM 的虚拟机，升级vmtools，操作成功
                        opensuse11.4 虚拟机升级 vmtools，操作成功
                        虚拟机不存在 /usr/lib/systemd/system 目录，安装vmtools 成功
                        虚拟机构造存在 /usr/lib/systemd/system，且存在 /usr/lib/udev/rules.d 的场景，安装 vmtools 成功
                        虚拟机 ubuntu 18.04.6 构造存在 /usr/lib/systemd/system，但不存在/usr/lib/udev/rules.d 的场景，安装 vmtools 成功
                    僵尸进程问题
                        arm 集群 uos 1070a 虚拟机安装老版本 vmtools运行一段时间看到僵尸进程后升级vmtools到410，再观察一段时间，检查虚拟机内没有僵尸进程 defunct
                    安全检查
                        绿盟漏扫已安装vmtools的虚拟机
                    升级测试
                        smtxos 5.0.3 + vmtools 2.12.1及其他低版本，集群升级到 smtxos 6.3.0 + vmtools升级到 4.1.0 ，再将 vmtools升到4.2.0
                        smtxos 5.1.5 + vmtools 4.0.0，集群升级到 smtxos 6.3.0 + vmtools升级到 4.1.0 ，再将 vmtools升到4.2.0
                    SMTX vmtools 集成回归
                        给集群上传 vmtools iso
                        安装 vmtools，再次安装 vmtools，操作成功，驱动不再安装
                        升级 vmtools
                        卸载 vmtools
                        SVT 或 SMTX VMTools 服务启、停、重启
                        vmtools 基础功能回归测试 - 编辑虚拟机主机名
                        vmtools 基础功能回归测试 - 编辑网卡ipv4，重启虚拟机
                        vmtools 基础功能回归测试 - 编辑网卡ipv6，重启虚拟机
                        vmtools 基础功能回归测试 - 编辑网卡ipv4 和 ipv6，重启虚拟机
                        vmtools 基础功能回归测试 - 编辑 DNS，重启虚拟机
                        vmtools 基础功能回归测试 - 重置 NTP
                        vmtools 基础功能回归测试 - 重置账户密码
                        vmtools 基础功能回归测试 - 设置恢复时同步
                        vmtools 基础功能回归测试 - 创建一致性快照
                        热添加虚拟机，cpu、内存、磁盘，cdrom
                        虚拟机 cpu、mem 性能数据采集
                        虚拟机磁盘文件系统分区使用量采集
                        vmtools 基础功能回归测试 - 执行指定命令
                        通过 v2v 从vmware 迁移过来的虚拟机（dhcp），安装 vmtools，数据采集及编辑IP，设置dns，重启虚拟机，操作均成功
                        通过 v2v 从vmware 迁移过来的虚拟机,升级 vmtools，数据采集及编辑IP，设置dns，重启虚拟机，操作均成功
                        通过 v2v 从smtxos迁移到 acos的虚拟机，安装 vmtools，数据采集、编辑IP，设置dns，重启虚拟机，操作均成功
                        通过 v2v 从smtxos迁移到 acos的虚拟机，升级 vmtools，数据采集、编辑IP，设置dns，重启虚拟机，操作均成功
                        通过 v2v 从smtxos迁移到 acos的虚拟机卸载 vmtools后再安装 vmtools，数据采集、编辑IP，设置dns，重启虚拟机，操作均成功
                        通过 cloud-init 创建出来的虚拟机，安装 vmtools，数据采集、编辑IP、设置dns，重启虚拟机，操作均成功
                        通过 cloud-init 创建出来的虚拟机，升级 vmtools，数据采集、编辑IP、设置dns，重启虚拟机，操作均成功
                        集群内迁移和跨集群热迁移
                    arcfra vmtools 回归【跟研发确认下测试范围】
                        给集群上传 vmtools iso
                        安装 vmtools，再次安装 vmtools
                        升级 vmtools
                        卸载 vmtools
                        SVT 或 SMTX VMTools 服务启、停、重启
                        vmtools 基础功能回归测试 - 编辑虚拟机主机名
                        vmtools 基础功能回归测试 - 编辑网卡ipv4，重启虚拟机
                        vmtools 基础功能回归测试 - 编辑网卡ipv6，重启虚拟机
                        vmtools 基础功能回归测试 - 编辑网卡ipv4 和 ipv6，重启虚拟机
                        vmtools 基础功能回归测试 - 编辑 DNS，重启虚拟机
                        vmtools 基础功能回归测试 - 重置 NTP
                        vmtools 基础功能回归测试 - 重置账户密码
                        vmtools 基础功能回归测试 - 设置恢复时同步
                        vmtools 基础功能回归测试 - 创建一致性快照
                        热添加虚拟机，cpu、内存、磁盘，cdrom
                        虚拟机磁盘文件系统分区使用量采集
                        vmtools 基础功能回归测试 - 执行指定命令
                4.2.0
                    需求&改进
                        设置IP优化方式
                            支持 QGA 配置 IPv4 网络
                                NM 版本等于或大于1.0.0 的虚拟机
                                    给某个网卡设置静态IPv4
                                    dhcp 网卡设置为 静态IPv4
                                    dhcp 网卡设置为 静态IPv6
                                    dhcp 网卡同时设置为 静态IPv4和 ipv6
                                    dhcp 网卡同时设置为 静态IPv4和 ipv6且设置两者的默认网关
                                    NM 版本等于 1.0.0 的虚拟机，修改static网卡的ipv4
                                    NM 版本等于 1.0.0 的虚拟机，修改static网卡的ipv6
                                    NM 版本等于 1.0.0 的虚拟机，修改static网卡的ipv4和ipv6
                                    NM 版本等于 1.0.0 的虚拟机，修改static网卡的ipv4和ipv6且设置两者的默认为网关
                                    NM 版本大于1.0.0 的虚拟机，网卡设置ipv4
                                    NM 版本大于 1.0.0 的虚拟机，网卡设置ipv4和默认网关
                                    NM 版本大于 1.0.0 的虚拟机，网卡同时设置ipv4和ipv6
                                    NM 版本大于 1.0.0 的虚拟机，网卡同时设置ipv4和ipv6及两者的默认为网关
                                    给多个网卡设置IP
                                    给网卡设置冲突的 ipv4
                                    给网卡设置冲突的 ipv6
                                    给网卡同时设置冲突的 ipv4 和 ipv6
                                    给 vmtools版本低于3.2.0 的虚拟机设置IPv4
                                    给vmtools 3.2.0 虚拟机设置ipv4
                                    给vmtools 4.0.0 的虚拟机设置ipv4和ipv6
                                    修改 static 网卡的虚拟机网络
                                    修改 static 虚拟机 ipv4 的默认网关
                                    修改static 虚拟机 ipv4 的默认网关同时修改ipv4
                                    修改static 虚拟机 ipv6 的默认网关同时修改ipv6
                                    修改 static 虚拟机 ipv4 和 ipv6的默认网关和ipv4和ipv6
                                    修改 static 网卡的虚拟机网络同时修改ipv4
                                    修改 static 网卡的虚拟机网络同时修改ipv6
                                    修改 static 网卡的虚拟机网络同时修改ipv4和ipv6
                                    禁用 static网卡后修改IPv4和ipv6，再启用网卡
                                    禁用 static网卡后重启虚拟机
                                    禁用 static网卡后启用
                                    debian 10 桌面版虚拟机
                                    opensuse 11.4
                                    kylin server v10 sp3 (NM+network)
                                    uos 20-desktop 1020
                                    kylin server v10 sp1 (NM+ifup/ifdown)
                                    debian 12 桌面版 (NM+ifup/ifdown)
                                    删除虚拟机上的 set network脚本后设置ipv4,成功，没有set network 脚本创建
                                NM 版本低于1.0.0 的虚拟机
                                    NM 版本低于 1.0.0 的虚拟机，修改static网卡的ipv4任务成功,通过脚本设置
                                    NM 版本低于 1.0.0 的虚拟机，修改static网卡的ipv6任务失败
                                    NM 版本低于 1.0.0 的虚拟机，修改static网卡的ipv4和ipv6，任务失败，无法设置ipv6
                                    NM 版本低于 1.0.0 的虚拟机，修改static网卡的ipv4和ipv6且设置两者的默认为网关，任务设置失败，无法设置ipv6
                                非 NM 配置网络的虚拟机
                                    windows虚拟机
                                        windows 虚拟机，网卡设置ipv4
                                        windows 虚拟机，网卡设置ipv4和默认网关
                                        windows 虚拟机，网卡同时设置ipv4和ipv6
                                        windows 虚拟机，网卡同时设置ipv4和ipv6及两者的默认为网关
                                【qga】windows 虚拟机采集配置 ipv4 的能力
                                    删除 windows 的vmtools脚本，给网卡设置静态ipv4 成功且没有 set network 脚本创建
                            支持使用 netplan 命令行配置 IP
                                使用 netplan配置网络的虚拟机
                                    使用 netplan 配置网络的虚拟机，添加网卡设置静态 ipv4
                                    使用 netplan 配置网络的虚拟机，添加网卡设置静态 ipv4设置默认网关
                                    使用 netplan 配置网络的虚拟机，添加网卡设置静态 ipv4 和 ipv6
                                    使用 netplan 配置网络的虚拟机，添加网卡设置静态 ipv6
                                    使用 netplan 配置网络的虚拟机，添加网卡设置静态 ipv6和默认网关
                                    使用 netplan 配置网络的虚拟机，添加网卡设置静态 ipv4 和ipv6和两者的默认网关
                                    使用 netplan 配置网络的虚拟机，DHCP 转 static，设置静态 ipv4
                                    使用 netplan 配置网络的虚拟机，DHCP 转 static，设置静态 ipv4和默认网关
                                    使用 netplan 配置网络的虚拟机，DHCP 转 static，设置静态 ipv6
                                    使用 netplan 配置网络的虚拟机，DHCP 转 static，设置静态 ipv6和默认网关
                                    使用 netplan 配置网络的虚拟机，DHCP 转 static，设置静态 ipv4 和 ipv6
                                    使用 netplan 配置网络的虚拟机，DHCP 转 static，设置静态 ipv4 和 ipv6及各自的默认网关
                                    使用 netplan 配置网络的虚拟机，修改 static 网卡，仅修改ipv4
                                    使用 netplan 配置网络的虚拟机，修改 static 网卡，仅修改ipv4和其网关
                                    使用 netplan 配置网络的虚拟机，修改 static 网卡，仅修改ipv6
                                    使用 netplan 配置网络的虚拟机，修改 static 网卡，仅修改ipv6 和其网关
                                    使用 netplan 配置网络的虚拟机，修改 static 网卡，同时修改ipv4和ipv6以及两者的默认网关
                                    使用 netplan 配置网络的虚拟机，修改 static 网卡，移除ipv4的默认网关
                                    使用 netplan 配置网络的虚拟机，修改 static 网卡，移除ipv6的默认网关
                                    同时编辑多个网卡：添加网卡设置ipv4，修改网卡设置ipv4和ipv6，dhcp转static设置ipv4
                                    同时修改多个 static 网卡，移除ipv4的默认网关，移除ipv6的默认网关，修改ipv4，修改ipv6，设置ipv4和ipv6网关
                                    使用 netplan 配置网络的虚拟机，修改 static 网卡的虚拟机网络同时修改ipv4
                                    使用 netplan 配置网络的虚拟机，修改 static 网卡的虚拟机网络同时修改ipv6
                                    使用 netplan 配置网络的虚拟机，修改 static 网卡的虚拟机网络同时修改ipv4和ipv6
                                    使用 netplan 配置网络的虚拟机，禁用 static网卡后修改IPv4和ipv6，再启用网卡
                                    使用 netplan 配置网络的虚拟机，禁用 static网卡后重启虚拟机
                                    使用 netplan 配置网络的虚拟机，禁用 static网卡后启用网卡
                                    使用 netplan 配置网络，ubuntu desktop（版本>=18） 虚拟机编辑网卡设置ipv4和ipv6
                                    使用 netplan 配置网络，ubuntu server（版本>=18）虚拟机编辑网卡设置ipv4和ipv6
                                    设置IP后重启虚拟机，IP设置没有变化
                                    同一个网卡多次设置IP，操作成功，历史设置的IP保留在网卡配置文件里
                                使用 network 配置网络的虚拟机
                                    使用 network 配置网络的虚拟机，添加网卡设置ipv4
                                    使用 network 配置网络的虚拟机，添加网卡设置ipv4和默认网关
                                    使用 network 配置网络的虚拟机，添加网卡设置ipv4和ipv6
                                    使用 network 配置网络的虚拟机，添加网卡设置ipv4和ipv6及两者的默认为网关
                                    使用 network 配置网络的虚拟机，修改网卡设置静态 ipv4
                                    使用 network 配置网络的虚拟机，修改网卡设置静态 ipv4和默认网关
                                    使用 network 配置网络的虚拟机，修改网卡设置静态 ipv6
                                    使用 network 配置网络的虚拟机，修改网卡设置静态 ipv6和默认网关
                                    使用 network 配置网络的虚拟机，修改网卡设置静态 ipv4 和ipv6
                                    使用 network 配置网络的虚拟机，修改网卡设置静态 ipv4 和ipv6及两者的默认网关
                                    suse11sp4
                                    设置IP后重启虚拟机，IP设置没有变化
                                使用 ifup/ifdow配置网络的虚拟机
                                    使用 ifup/ifdown 配置网络的虚拟机，添加网卡设置ipv4和默认网关
                                    使用  ifup/ifdown 配置网络的虚拟机，添加网卡设置ipv4和ipv6,ipv4设置成功，iPV6设置失败
                                    使用  ifup/ifdown 配置网络的虚拟机，添加网卡设置ipv4和ipv6及两者的默认为网关，ipv4设置成功，iPV6设置失败
                                    使用 ifup/ifdown 配置网络的虚拟机，修改网卡设置静态 ipv4
                                    使用 ifup/ifdown 配置网络的虚拟机，修改网卡设置静态 ipv4 和ipv6,ipv4设置成功，iPV6设置失败
                                    使用 ifup/ifdown 配置网络的虚拟机，修改网卡设置静态 ipv6，设置失败
                                    使用 networking 配置网络的虚拟机，添加网卡设置ipv4
                                    使用ifup/ifdown配置网络，ubuntu desktop（版本低于18）虚拟机编辑网卡设置ipv4和ipv6，,ipv4设置成功，iPV6设置失败
                                    使用ifup/ifdown配置网络，ubuntu server（版本低于18）虚拟机编辑网卡设置iPV6失败
                                    使用ifup/ifdown配置网络，debian 服务器版虚拟机，编辑网卡ipv4
                                    使用ifup/ifdown配置网络，debian 服务器版虚拟机，编辑网卡设置iPV6失败
                                    设置IP后重启虚拟机，IP设置没有变化
                        vmtools 不依赖 powershell
                            使用 qga 操控 guestof信息（新方法）
                                删除虚拟机内的guest_get脚本，qga采集正常
                                vmtools 2.12.1 升到 最新版本，qga 采集正常
                                vmtools 3.0.0 升到 最新版本，qga 采集正常
                                vmtools 3.0.1升到 最新版本，qga 采集正常
                                vmtools 3.0.2升到 最新版本，qga 采集正常
                                vmtools 3.0.3升到 最新版本，qga 采集正常
                                vmtools 3.1.0升到 最新版本，qga 采集正常
                                vmtools 3.1.1升到 最新版本，qga 采集正常
                                vmtools 3.2.0升到 最新版本，qga 采集正常
                                vmtools 3.2.2升到 最新版本，qga 采集正常
                                vmtools 3.2.3升到 最新版本，qga 采集正常
                                vmtools 4.0.0 升到 最新版本，qga 采集正常
                                vmtools 4.1.0升到 最新版本，qga 采集正常
                                移除对脚本 guest_get_static_data 的依赖
                                    采集 hostname
                                    采集 os info，os 发行版本和 kernel 版本
                                    qga 采集 网卡信息
                                    虚拟机 SVT 服务停止一段时候启动，qga 采集正常
                                    虚拟机暂停一段时候恢复，qga 采集正常
                                    虚拟机关机一段时候开机，qga 采集正常
                                    虚拟机集群内迁移后，qga采集正常
                                    大批量虚拟机关机后开机，qga 采集正常
                                    大批量虚拟机升级 vmtools版本，qga 采集正常
                                    linux 虚拟机，qga 采集正常
                                    windows 虚拟机，qga 采集正常
                                    虚拟机有性能负载时，qga 采集情况
                                    虚拟机磁盘空间不足时，qga 采集情况
                                    HA故障恢复后，qga 采集正常
                                    虚拟机重启，采集正常
                                    tower 修改虚拟机的主机名，qga 采集正常
                                    tower 修改虚拟机的网卡配置，qga 采集正常
                                    从虚拟机内修改主机名，qga 采集正常
                                    从虚拟机内修改网卡配置，qga 采集正常
                                    虚拟机网卡没有IP时
                                    虚拟机网卡禁用时
                                    虚拟机没有设置网关时
                                    虚拟机没有网卡，不影响其他采集
                                使用 qga 获取虚拟机的 dns 配置
                                    tower 修改虚拟机的dns，qga 采集正常
                                    从虚拟机内修改dns，qga 采集正常
                                    虚拟机没有dns，qga 采集正常
                                移除对脚本 guest-get-storage-data 的依赖
                                    使用qga 采集 文件系统分区使用率
                                    使用qga 采集磁盘数据
                                    linux 虚拟机磁盘使用qga 采集 storage数据
                                    虚拟机存在 lvm 在同一个挂载点跨2个磁盘，采集磁盘使用量，used 为null
                                    虚拟机的 lvm挂载点均不跨磁盘，各磁盘的used有值
                                    虚拟机磁盘混合场景：存在lvm挂载点跨不同磁盘，存在lvm挂载点在同磁盘不同分区，采集到used
                                    采集windows  虚拟机磁盘数据和文件系统分区使用率
                                    采集windows 虚拟机系统保留分区的大小和使用量
                                    虚拟机没有disk，storage 采集不到，不影响其他采集
                            使用脚本 采集 guestos 信息（老方法）
                                采集static数据正常
                                采集存储数据
                                采集 perf 数据正常
                                tower 修改虚拟机的主机名，qga 采集正常
                                tower 修改虚拟机的dns，qga 采集正常
                                tower 修改虚拟机的网卡配置，qga 采集正常
                                从虚拟机内修改主机名，qga 采集正常
                                从虚拟机内修改dns，qga 采集正常
                                从虚拟机内修改网卡配置，qga 采集正常
                                qga 采集不到 dns，会额外通过脚本采集
                                qga 采集不到  gateway，会额外通过脚本采集
                                qga 采集不到 ip_type，会额外通过脚本采集
                                qga 采集不到 os_version ，是否需要额外再用脚本采集一次
                                虚拟机安装的vmtools4.0.0，使用脚本收集
                                虚拟机安装的vmtools3.1.0，使用脚本收集
                        vmtools 4.2.0 强关联 smtxos6.3.0
                            支持 QGA 配置 IPv4 网络
                                kylin server v10 虚拟机（vmtools 4.1.0），设置ipv4，操作成功
                                kylin server v10 虚拟机（vmtools 4.1.0），设置ipv6，操作成功
                                kylin server v10 虚拟机（vmtools 4.1.0），同时设置ipv4 和ipv6，操作成功
                                kylin server v10 虚拟机（vmtools 4.2.0），设置ipv4，操作成功
                                kylin server v10 虚拟机（vmtools 4.2.0），同时设置 ipv4 和 ipv6，操作成功
                                kylin server v10 虚拟机（vmtools 4.2.0 且删除虚拟机内配置网络的脚本），设置ipv4和默认网关，操作成功
                                kylin server v10 虚拟机（vmtools 4.2.0 且删除虚拟机内配置网络的脚本），设置ipv6和默认网关，操作成功
                                uos desktop 虚拟机（vmtools 低于4.1.0 ），设置 ipv4，操作成功
                                uos destkop 虚拟机(vmtools 4.2.0)，修改静态ipv4网卡的虚拟机网络，同时修改ipv4和ipv6和各自的默认网关，操作成功
                                uos destkop 虚拟机(vmtools 4.2.0)，禁用设置了ipv4和ipv6 网卡，然后重启虚拟机启用网卡
                                uos destkop 虚拟机(vmtools 4.2.0)，禁用设置了ipv4和ipv6 网卡后，修改网卡 ipv4和ipv6，然后启用网卡
                                uos desktop 虚拟机编辑多网卡：添加一块网卡设置ipv4，dhcp转static设置ipv4和ipv6，修改默认网关
                                windows 虚拟机（vmtools 4.2.0），设置ipv4和ipv6，操作成功
                                v2v 从 vmware 迁移虚拟机到 smtxos 6.3.0，设置静态IP，迁移成功，目标端修改ipv4成功
                                cloud-init 创建虚拟机时设置静态IP4，创建成功，然后修改 ipv4 和设置ipv6 成功
                            移除对脚本 guest_get_static_data 的依赖
                                kylin server v10 虚拟机（vmtools 4.1.0），正常采集操作系统版本
                                kylin server v10 虚拟机（vmtools 4.1.0），正常采集 hostname
                                kylin server v10 虚拟机（vmtools 4.1.0），正常采集 dns
                                kylin server v10 虚拟机（vmtools 4.1.0），正常采集 网卡信息
                                kylin server v10虚拟机（vmtools 4.1.0），设置静态IPv6，正常采集 网卡信息
                                kylin server v10 虚拟机（vmtools 4.2.0 且删除虚拟机内收集信息的脚本），正常采集 dns
                                kylin server v10虚拟机（vmtools 4.2.0 且删除虚拟机内收集信息的脚本），正常采集 网卡信息
                                kylin server  v10 虚拟机（vmtools 4.2.0），正常采集磁盘设备名称
                                kylin server  v10 虚拟机（vmtools 4.2.0），正常采集磁盘文件系统分区使用量
                                windows server 2025虚拟机（vmtools 4.2.0且删除脚本），正常采集磁盘信息（设备名称和文件系统分区使用量）
                                kylin server  v10 虚拟机（vmtools 4.2.0，配置较复杂的 多个 lvm），正常采集磁盘信息
                                windows server 2025虚拟机（vmtools4.2.0，配置跨区卷等复杂分区），正常采集磁盘信息
                                uos server  虚拟机（vmtools 4.2.0，删除虚拟机内的收集信息的脚本），dhcp转 static设置ipv4和ipv6及网关后，正常采集guets_info 信息
                                uos server  虚拟机（vmtools 4.2.0，删除虚拟机内的收集信息的脚本），手动修改虚拟机的主机名，dns和网卡配置文件，以及消耗此空间后，正常采集guets_info 信息
                                虚拟机 SVT 服务停止一段时间后启动，qga 采集正常
                                虚拟机暂停一段时间后恢复，qga 采集正常
                                虚拟机关机一段时候后开机，qga 采集正常
                                虚拟机集群内热迁移后，qga采集正常
                                虚拟机集群内冷迁移后，开机后 qga采集正常
                                v2v 从 vmware 迁移虚拟机到 smtxos 6.3.0，设置静态IP，迁移成功，正常采集 guestinfo信息
                                cloud-init 创建虚拟机时设置静态IP4，创建成功，正常采集 guestinfo 信息
                                HA故障恢复后，qga 采集正常
                                虚拟机有性能负载时，qga 采集情况
                                虚拟机（vmtools 4.2.0且删除脚本），正常采集cpu&mem
                                windows server 2025 虚拟机（vmtools 4.2.0且删除脚本），正常采集cpu&mem
                            支持使用 netplan 命令行配置 IP
                                使用 netplan 配置网络，DHCP 转static，设置静态 ipv4
                                使用 netplan 配置网络，DHCP 转static，设置静态 ipv6
                                使用 netplan 配置网络，DHCP 转 static，设置静态 ipv4 和 ipv6及各自的默认网关
                                使用 netplan 配置网络，添加网卡设置静态 ipv4 和ipv6和两者的默认网关
                                使用 netplan 配置网络，添加网卡，设置静态 ipv4
                                使用 netplan 配置网络，添加网卡，设置静态 ipv6和默认网关
                                使用 netplan 配置网络，同时修改ipv4和ipv6以及两者的默认网关
                                使用 netplan 配置网络，修改dns 后配置网卡ipv4和ipv6，dns保存不变
                                使用 netplan 配置网络，dhcp转 static设置iPv4，添加网卡设置ipv4和ipv6，修改static网卡ipv6
                                使用 netplan 配置网络，仅修改 static 网卡的虚拟机网络，IP不受影响
                                使用 netplan 配置网络，修改 static 网卡的虚拟机网络同时修改ipv4和ipv6
                                使用 netplan 配置网络，禁用 static网卡后重启虚拟机，启用网卡
                                使用 netplan 配置网络，禁用 static网卡后修改IPv4和ipv6，再启用网卡
                                使用 netplan 配置网络，设置dns 和IP后重启虚拟机，IP和dns 没有变化
                                使用 network 配置网络，修改网卡设置静态 ipv4 和ipv6
                                使用 network 配置网络，设置dns和IP后重启虚拟机，IP和dns均保持不变
                                使用ifup/ifdown配置网络，编辑网卡ipv4和ipv6
                                使用ifup/ifdown配置网络，ubuntu desktop（版本低于18）虚拟机编辑网卡设置ipv4和ipv6
                                使用ifup/ifdown配置网络，ubuntu server（版本低于18）虚拟机编辑网卡设置ipv4和ipv6
                                使用 ifup/ifdown 配置网络，设置dns和IP后重启虚拟机，IP和dns均保持不变
                                ubuntu-desktop 22.04（netplan 版本0.104） 设置静态IPv4和ipv6
                                ubuntu-desktop 18.04（netplan低 0.99），设置静态IPv4和ipv6
                                ubuntu-server 22.04（netplan版本0.106），设置静态IPv4和ipv6
                    安全检查
                        绿盟漏扫已安装vmtools的虚拟机
                    升级测试
                        smtxos 5.0.3 + vmtools 2.12.1及其他低版本，集群升级到 smtxos 6.3.0 + vmtools升级到 4.1.0 ，再将 vmtools升到4.2.0
                        smtxos 5.1.5 + vmtools 4.0.0，集群升级到 smtxos 6.3.0 + vmtools升级到 4.1.0 ，再将 vmtools升到4.2.0
                        从 vmtools 2.12.1 升到 4.2.0
                        从 vmtools 3.0.0升到 4.2.0
                        从 vmtools 3.0.1升到 4.2.0
                        从 vmtools 3.0.2 升到 4.2.0
                        从 vmtools 3.0.3升到 4.2.0
                        从 vmtools 3.1.0升到 4.2.0
                        从 vmtools 3.1.1升到 4.2.0
                        从 vmtools 3.2.0升到 4.2.0
                        从 vmtools 3.2.2升到 4.2.0
                        从 vmtools 3.2.3升到 4.2.0
                        从 vmtools 4.0.0升到 4.2.0
                        从 vmtools 4.1.0升到 4.2.0
                    集成回归
                        vmtools 基础功能检查
                            给集群上传 vmtools iso
                            安装 vmtools，再次安装 vmtools，操作成功，驱动不再安装
                            升级 vmtools
                            卸载 vmtools
                            SVT 或 SMTX VMTools 服务启、停、重启
                            vmtools 基础功能回归测试 - 编辑虚拟机主机名
                            vmtools 基础功能回归测试 - 编辑网卡ipv4，重启虚拟机
                            vmtools 基础功能回归测试 - 编辑网卡ipv6，重启虚拟机
                            vmtools 基础功能回归测试 - 编辑网卡ipv4 和 ipv6，重启虚拟机
                            vmtools 基础功能回归测试 - 编辑 DNS，重启虚拟机
                            vmtools 基础功能回归测试 - 重置 NTP
                            vmtools 基础功能回归测试 - 重置账户密码
                            vmtools 基础功能回归测试 - 设置恢复时同步
                            vmtools 基础功能回归测试 - 创建一致性快照
                            热添加虚拟机，cpu、内存、磁盘，cdrom
                            虚拟机 cpu、mem 性能数据采集
                            虚拟机磁盘文件系统分区使用量采集
                            vmtools 基础功能回归测试 - 执行指定命令
                            通过 v2v 从vmware 迁移过来的虚拟机（dhcp），安装 vmtools，数据采集及编辑IP，设置dns，重启虚拟机，操作均成功
                            通过 v2v 从vmware 迁移过来的虚拟机,升级 vmtools，数据采集及编辑IP，设置dns，重启虚拟机，操作均成功
                            通过 v2v 从smtxos迁移到 acos的虚拟机，安装 vmtools，数据采集、编辑IP，设置dns，重启虚拟机，操作均成功
                            通过 v2v 从smtxos迁移到 acos的虚拟机，升级 vmtools，数据采集、编辑IP，设置dns，重启虚拟机，操作均成功
                            通过 v2v 从smtxos迁移到 acos的虚拟机卸载 vmtools后再安装 vmtools，数据采集、编辑IP，设置dns，重启虚拟机，操作均成功
                            通过 cloud-init 创建出来的虚拟机，安装 vmtools，数据采集、编辑IP、设置dns，重启虚拟机，操作均成功
                            通过 cloud-init 创建出来的虚拟机，升级 vmtools，数据采集、编辑IP、设置dns，重启虚拟机，操作均成功
                            集群内迁移和跨集群热迁移
                        GuestOS兼容性
                            CentOS/Redhat 7.1 - 最新兼容的版本
                            Ubuntu Desktop 16.04 - 最新兼容的版本
                            Ubuntu Server 20.04.4 - 最新兼容的版本
                            Fedora 25 - 最新兼容的版本
                            Oracle Linux 7.1 - 最新兼容的版本
                            UOS Server 20
                            UOS S Desktop 20
                            Kylin Server v10
                            Kylin Desktop v10
                            windows server 2008R2 - 最新兼容的 Server 版本
                            windows7 - 最新兼容的 Desktop 版本
                        低版本 SMTXOS 对 VMTools 4.2.0 的兼容性
                            smtxos6.x
                            smtxos5.1.x
                            smtxos5.0.x
                            smtxos4.1.x
                    物料发布检查
                        iso md5 检查及上传
            Tower 版本更新
                4.6.0
                    虚拟机的虚拟机工具 【安装、升级、弹出 】按钮触发条件变更
                        虚拟机已挂载 VMTools ISO,  展示卸载按钮
                        虚拟机未挂载 VMTools ISO,  展示挂载按钮
                        虚拟机的 SVT 运行中且版本低于集群最新 VMtools ISO,  展示升级按钮
                4.8.0
                    TOWER-19502 VMTools 批量升级
                        虚拟机列表 - 单个操作
                            虚拟机列表 - 虚拟机记录右侧的更多操作 - 增加【升级虚拟机工具】
                            选中1个虚拟机执行批量升级
                        虚拟机列表 - 批量操作
                            虚拟机列表 - 批量操作栏，增加【升级虚拟机工具】
                            批量选择 1 个虚拟机， 触发批量【升级虚拟机工具】
                            批量选择多个虚拟机， 触发批量【升级虚拟机工具】
                            集群版本为 6.3.0，tower 版本为 4.8.0，选择多个虚拟机，全部批量升级，升级成功
                            集群版本为 5.1.5，tower 版本为 4.8.0，选中多个虚拟机，全部批量升级，升级成功
                            选择多个虚拟机，含升级失败的虚拟机
                            选择多个虚拟机，含已安装 410的虚拟机，提示跳过
                            选择多个虚拟机，含已安装低版本但vmtools 状态为 未运行的虚拟机，提示跳过
                            选择多个虚拟机，含关机的虚拟机
                            选择多个虚拟机，中含暂停的虚拟机
                            选择多个虚拟机中含未知状态的虚拟机
                            选择多个虚拟机，含未安装 vmtools 的虚拟机，
                            选择多个虚拟机，含已挂载低版本 vmtools 的虚拟机
                            选择多个虚拟机，含已挂载 vmtools410的虚拟机
                            选择多个虚拟机，含多个无法支持的虚拟机，部分批量升级，升级成功
                            选择多个虚拟机，均无法升级
                            选择最大支持数的虚拟机
                            集群版本低于 630或5.1.5，tower为 4.8.0，选中多个虚拟机，不支持批量升级
                            集群版本为 630，tower 版本低于 4.8.0，选中多个虚拟机，不支持批量升级
                            集群版本低于 630或5.1.5，tower 版本低于 4.8.0，选中多个虚拟机，不支持批量升级
                            批量升级虚拟机工具弹窗中选择取消
                            批量升级虚拟机工具弹窗中关闭弹窗
                            无法选中系统服务虚拟机，不支持批量升级
                            无法选中正在执行任务时（跨集群迁移、开关机等）的虚拟机，不支持批量升级
                        增加事件审计
                            挂载虚拟机工具映像
                            升级虚拟机工具
                            弹出虚拟机工具
                        批量升级 - 任务检查
                            虚拟机列表，批量选择多个开机且已安装已运行低版本 VMTools 的虚拟机， 批量按钮可以触发批量升级
        Cloud-init
            功能测试
                cloud-init 创建虚拟机
                    user-data 检查
                        ELF API 从 cloud-init 模版创建虚拟机传入 34K user-data 可以创建成功，虚拟机内部 cloud-init 配置成功
                ELF-CLOUD-INIT-1.1.0
                    卸载 cloud-init
                    虚拟机安装cloud-init 后关机再开机，不会实例化
                    虚拟机安装cloud-init 转化为 cloud-init模版后再转化为虚拟机，开机不会实例化
                    卸载 cloud-init 后再安装cloud-init
    ELF 集成测试
        系统集成测试
            SMTX ELF（4 节点集群）+ SMTX ZBS
                功能测试
                    虚拟机配置
                        计算资源
                            热添加 CPU、内存，检查业务虚拟机（Tower、CAPP、数据库等）服务正常，业务不中断
    SMTX OS
        6.2.1-hp1
            ELF-7307 CPU 独占功能优化
                虚拟机生命周期检查
                    升级
                        升级前已开启独占的开机虚拟机 - 升级补丁后 - 独占cpu 不变
                        升级前已开启独占的开机虚拟机 - 升级补丁后 - 编辑独占cpu个数，按最新规则分配 独占 pcpu，内存绑定 numa virsh edit 最新数据更新，下次调度内存绑定numa 更新
                        升级前已开启cpuqos 开机虚拟机 - 升级补丁后 - 编辑开启独占cpu，按最新规则分配 独占 pcpu，内存绑定 numa virsh edit 最新数据更新，下次调度内存绑定numa 更新
                        升级前已开启独占开机虚拟机 - 升级补丁后 - 编辑切换为 cpuqos，虚拟机使用共享 pcpu
                        升级前关机配置独占的虚拟机 - 升级后开机 - 按最新规则分配独占 pcpu，内存绑定 numa virsh dumpxml 最新数据更新
                        升级前关机配置cpuqos的虚拟机 - 升级后开机 - 使用共享 pcpu，cpuqos 预留、份额计算正确
                        升级前已开启cpuqos 开机虚拟机 - 升级补丁后 - 编辑cpuqos 参数，cpuqos 预留、份额计算正确更新数据
                算法优化检查（1个chunk 实例）
                    vcpu 对应 pcpu numa
                        三、socket 的 completely_free_thread_group 分配
                            筛选使用的 socket
                                仅 一组 socket 的 completely_free_thread_group pcpu 总量可以容纳 vCPU
                                    选 socket 上的 numa
                                        1、分配独占 n vpcu 的 A个核心使用的 numa node
                                            1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                        2、分配独占 n vpcu 的（n- A）个核心使用的 numa node
                                            1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                有多组 socket 的 completely_free_thread_group pcpu 总量可以容纳 vCPU
                                    1、选择距离 Chunk 最近的 completely_free_thread_group
                                        选 socket 上的 numa
                                            1、分配独占 n vcpu vm 的 第一个 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                            2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                    【620-hp1 不支持】如果有多个 completely_free_thread_group 距离相同，选择剩余内存较多的
                                        选 socket 上的 numa
                                            1、分配独占 n vcpu vm 的 第一个 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                            2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                    3、如果还有相同的，选择一个最小的 completely_free_thread_group
                                        选 socket 上的 numa
                                            1、分配独占 n vcpu vm 的 第一个 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                            2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                    4、如果还有多个候选 completely_free_thread_group ，选择 Group 中第一个 vCPU id 较小的；
                                        选 socket 上的 numa
                                            1、分配独占 n vcpu vm 的 第一个 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                            2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                        四、free_thread_group 分配（排除 chunk_week_group 数据 ）
                            筛选 numa node 下的 cpu
                                1、把 larger_free 中的 completely free 占满；
                                2、把 larger _free 中的非 completely free 占满；
                                3、把 smaller_free 中的 非completely_free 占满；
                                4、把 smaller_free 中的 completely_free 占满；
                            2、socket上的 free_thread_group 分配
                                筛选 socket
                                    仅有 1个 socket 的 free_thread_group 满足独占
                                        选择 socket 的 numa
                                            1、分配独占 n vcpu vm 的 第一个 numa node
                                                1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                2、如果还有多个，则优先 Chunk 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free 的核心；
                                                【620-hp1 不支持】3、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                4、如果还有多个，则优先 free group 本身数量最小
                                                5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                            2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                2、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                3、如果还有多个，则优先 Chunk 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free 的核心；
                                                【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                6、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                                    有多个 socket 的 free_thread_group 满足独占
                                        1、completely_free 数量最多的 socket
                                            1、筛选 completely_free 数量最大的 socket 作为独占目标 socket
                                        2、 距离 Chunk 最近的 socket
                                            2、如果有重复的，选择 距离chunkd 最近的 socket 作为目标socket
                                            选择 socket 的 numa
                                                1、分配独占 n vcpu vm 的 第一个 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先距离 chunk numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    6、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                                        【620-hp1 不支持】3、剩余内存更多 的 socket
                                            【620-hp1 不支持】3、如果有重复 socket 选择内存较多的 - 作为目标socket
                                            选择 socket 的 numa
                                                1、分配独占 n vcpu vm 的 第一个 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先距离chunkd numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    6、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                                        4、socket free group 最小 socket
                                            4、如果有重复的 选socket free_thread_cpu group 内数量 最小 - 作为目标 socket
                                            选择 socket 的 numa
                                                1、分配独占 n vcpu vm 的 第一个 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先距离chunk numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    5、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                                        5、socket Gruop 内第一个 vCPU id 最小 socket
                                            5、如果有重复，选socket free_thread_cpu group内第一个 vCPU id 最小的 -  作为目标socket
                                            选择 socket 的 numa
                                                1、分配独占 n vcpu vm 的 第一个 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先 Chunk 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free 的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    6、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                        五、使用 多socket pcpu 的分配
                            筛选 numa node 下的 cpu
                                1、把 larger_free 中的 completely free 占满；
                                2、把 larger _free 中的非 completely free 占满；
                                3、把 smaller_free 中的 非completely_free 占满；
                                4、把 smaller_free 中的 completely_free 占满；
                            后续 socket 使用(N-SUM(A))
                                1、分配独占 n vcpu vm 的 第一个 numa node
                                    1、有多个Socket free_thread_group 的 numa node 满足，优先 completely_free 数量最多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    2、如果还有多个，优先 free 数量大的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    3、如果还有多个，则优先 Chunk 最近的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                    1、有多个Socket free_thread_group 的 numa node 满足，优先 completely_free 数量最多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    2、如果还有多个，优先 free 数量大的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    3、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                    6、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                        六、多 socket 不够用时，使用 chunk_numa_weak_cpus
                            使用了多个 socket 后 CPU 还不够，会使用 chunk_numa_weak_cpus，使用的顺序为 CPU ID 的字母序。
                            非chunk_numa_weak_cpus 独占使用完后，检查 多个vm 独占使用 chunk_numa_weak_cpus 数量 正确， 不会重复使用 【630/620-u1 修复 ELF-8278】
                    算法规则覆盖检查
                        规则1、2 、3、4.1 SingleNUMAFreePolicy 的 独占数量不足时，需继续分配独占 cpu ，优先使用规则4.2 ：SingleSocketFreePolicy
                        使用规则6 chunk_numa_weak_cpus  进行独占（嵌套环境验证）
                系统配置检查
                    分配独占 numa 日志检查
                        elf-vm-schedule 日志中查看 虚拟机所属节点 numa 可分配的 共享cpu、独占 pcpu 集合
                        elf-vm-schedule 日志中查看 每个节点 socket 上numa 分配的  completely_free_thread_group 的 cpu 集合，区分 smaller 和 larger
                        elf-vm-schedule 日志中查看 每个节点 socket 上numa 分配的  free_thread_group 的 cpu 集合，区分 smaller 、larger  总数free cpu 数
                        elf-vm-schedule 日志中查看 每个节点 chunk_cpu_info信息
                        elf-vm-schedule 日志中展示选定的虚拟机cpu 独占策略：ChunkNUMAFreePolicy
                        elf-vm-schedule 日志中展示选定的虚拟机cpu 独占策略：SingleNUMACompletelyFreePolicy
                        elf-vm-schedule 日志中展示选定的虚拟机cpu 独占策略：SingleSocketCompletelyFreePolicy
                        elf-vm-schedule 日志中展示选定的虚拟机cpu 独占策略：SingleNUMAFreePolicy
                        elf-vm-schedule 日志中展示选定的虚拟机cpu 独占策略：SingleSocketFreePolicy
                        elf-vm-schedule 日志中展示选定的虚拟机cpu 独占策略：MultipleSocketsPolicy 日志： Using free threads, ordered sockets
                        在一个 Policy 中，可以通过 sorted plans are 关键字判断目前有可用方案排序后有哪些
                        在一个 socket 中选择 NUMA 时，关键字是 with previous node={}, remained_vcpu_count={}, remained_numa_nodes={}, choose node={} as best node, selected_pcpus={}
                    numa   chunk 距离计算
                        api/v2/management/hosts 可以查看 chunk 所属numa node ：host.data[0].cgroup.chunk_numa_node
                        在 api/v2/management/hosts 接口或 命令行 numactl -H 可以查看各 numa 之间的距离
            ELF-7309 手动配置 cpu 独占规则
                手动绑定使用
                    检查点
                        绑定
                            查看虚拟机独占是手动分配、还是自动分配， 使用 elf-tool elf_vm show_cpu_pin <vm_uuid>  - 查看Active cpu_pins 和 Manual cpu_pins 相同
                            开启独占的虚拟机 - 手动绑定cpu 核心在一个 numa 一个 thread 内 - 绑定成功，检查 cpu 独占配置文件，和 numa 内存绑定正确
                            开启独占的虚拟机 - 手动绑定cpu 核心在一个 numa 不同 thread 内 - 绑定成功，检查 cpu 独占配置文件，和 numa 内存绑定正确
                            开启独占的虚拟机 - 手动绑定cpu 核心在一个 socket 下 不通 numa 不同 thread 内 - 绑定成功，检查 cpu 独占配置文件，和 numa 内存绑定正确
                            开启独占的虚拟机 - 手动绑定cpu 核心在多个 socket 下 不通 numa 不同 thread 内 - 绑定成功，检查 cpu 独占配置文件，和 numa 内存绑定正确
                            开启独占的虚拟机 - 手动绑定cpu 核心在chunk_numa_free_cpu成功，检查 cpu 独占配置文件，和 numa 内存绑定正确
                            开启独占的虚拟机 - 手动绑定cpu 核心在chunk_numa_weak_cpu成功，检查 cpu 独占配置文件，和 numa 内存绑定正确
                            开启独占的虚拟机 - 手动绑定cpu 核心不能绑定在chunk_dynamic_cpus，有校验 【ELF-7365】
                            检查手动独占降级为自动独占时，cpu 独占绑定核心、内存绑定numa 正确
                            虚拟机名称含各种字符：“autov3_vmcreate__240527181223_44c1001e_????中文にほ한국12-=~(（）)_+[【】]{},.ab^_^o(∩_∩)o~ ” - 进行手动绑定独占 - 成功
                        取消
                            手动绑定独占的虚拟机 - 取消自动绑定成功，虚拟机能正常使用，下次调度前虚拟机独占、内存numa 绑定不变
                            手动绑定独占的虚拟机 - 取消自动绑定成功，发起新调度使用自动绑定独占，虚拟机能正常使用，虚拟机独占、内存numa 绑正确更新
                            虚拟机名称含各种字符：“autov3_vmcreate__240527181223_44c1001e_????中文にほ한국12-=~(（）)_+[【】]{},.ab^_^o(∩_∩)o~ ” - 取消手动绑定独占 - 成功
                        主机空闲 可独占 pcpu
                            elf-tool elf_cluster show_cpu_pin 展示不包含主机系统服务使用的 cpu
                            elf-tool elf_cluster show_cpu_pin 展示不包含的 chunk_dynaminc cpu
                            主机自动、手动更新独占核心后，elf-tool elf_cluster show_cpu_pin 剩余主机空闲 可独占 快速准确展示
        5.1.5
            515 支持 vhost-user-blk/scsi 硬件多队列【需求 revent】
                跨集群迁移
                    两集群自动多队列配置一致
                        支持自动多队列版本间迁移
                            515 到 6.0.x 迁移
                                跨集群热迁移
                                    跨集群热迁移后 - 检查已有 virtio 卷、virtio-scsi 控制器的 queues 不变
                                    仅 ide vm - 目标端热添加 virtio、scsi卷 - 检查新增 virtio 卷、virtio-scsi 控制器  queues：目标端 MIN(max_num_queues, 初始 nvCPU)
                                    仅 virtio vm - 目标端热添加 virtio、scsi 卷- 检查新增 virtio-scsi 控制器 queues:源端 MIN(max_num_queues,初始 nvCPU)， virtio 与已卷一致
                                    仅 scsi vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷 queues：源端 MIN(max_num_queues,初始 nvCPU)，virtio-scsi 控制器 与源控制器一致
                                    无 scsi 卷但含未卸载的 virtio-scsi 控制器 vm - 目标端热添加 8scsi 卷 -  检查已有和新增 virtio-scsi 控制器 queues：与源控制器一致
                                    含 virtio、scsi ide vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷、virtio-scsi 控制器 queues：源端MIN(max_num_queues，初始 nvCPU)
                                    源端热添加 vcpu 数 - 目标端热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：源端 MIN(max_num_queues，初始 nvCPU)
                                    目标端热添加 vcpu 数、热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：源端 MIN(max_num_queues，初始 nvCPU)
                                    目标端热添加 vcpu 数和 virtio、7scsi 卷- 关机重新开机 - 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，最新nvCPU)
                                跨集群分段迁移
                                    源端保留 vm，源端重新开机 - 检查已有卷：源端采用源端配置，目标端采用目标端配置
                                    源端不保留 vm，目标端开机 - 检查已有卷：目标端：MIN(max_num_queues，初始 nvCPU)
                                    含 virtio、scsi ide vm - 目标端热添加 virtio、7scsi 卷 - 检查已有和新增卷、控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    仅 ide vm - 目标端热添加 virtio、scsi卷 - 检查新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    仅 virtio vm - 目标端热添加 virtio、scsi 卷- 检查新增 virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    仅 scsi vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    无 scsi 卷但含未卸载的 virtio-scsi 控制器 vm - 目标端热添加 8scsi 卷 -  检查已有和新增 virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    源端热添加 vcpu 数 - 目标端热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    目标端热添加 vcpu 数、热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    目标端热添加 vcpu 数和 virtio、7scsi 卷- 关机重新开机 - 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                跨集群冷迁移
                                    跨集群冷迁移后，虚拟机开机 - 检查已有卷、控制器 queues：目标端 MIN(max_num_queues，最新 nvCPU)
                                    跨集群冷迁移后，虚拟机开机 - 热添加 virtio、7scsi 卷- 检查已有新增卷、控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                            515 到 6.1.x 及以上迁移
                                跨集群热迁移
                                    跨集群热迁移后 - 检查已有 virtio 卷、virtio-scsi 控制器的 queues 不变
                                    仅 ide vm - 目标端热添加 virtio、scsi卷 - 检查新增 virtio 卷、virtio-scsi 控制器  queues：目标端 MIN(max_num_queues, 初始 nvCPU)
                                    仅 virtio vm - 目标端热添加 virtio、scsi 卷- 检查新增 virtio-scsi 控制器 queues:源端 MIN(max_num_queues,初始 nvCPU)， virtio 与已卷一致
                                    仅 scsi vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷 queues：源端 MIN(max_num_queues,初始 nvCPU)，virtio-scsi 控制器 与源控制器一致
                                    无 scsi 卷但含未卸载的 virtio-scsi 控制器 vm - 目标端热添加 8scsi 卷 -  检查已有和新增 virtio-scsi 控制器 queues：与源控制器一致
                                    含 virtio、scsi ide vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷、virtio-scsi 控制器 queues：源端MIN(max_num_queues，初始 nvCPU)
                                    源端热添加 vcpu 数 - 目标端热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：源端 MIN(max_num_queues，初始 nvCPU)
                                    目标端热添加 vcpu 数、热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：源端 MIN(max_num_queues，初始 nvCPU)
                                    目标端热添加 vcpu 数和 virtio、7scsi 卷- 关机重新开机 - 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，最新nvCPU)
                                跨集群分段迁移
                                    源端保留 vm，源端重新开机 - 检查已有卷：源端采用源端配置，目标端采用目标端配置
                                    源端不保留 vm，目标端开机 - 检查已有卷：目标端：MIN(max_num_queues，初始 nvCPU)
                                    含 virtio、scsi ide vm - 目标端热添加 virtio、7scsi 卷 - 检查已有和新增卷、控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    仅 ide vm - 目标端热添加 virtio、scsi卷 - 检查新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    仅 virtio vm - 目标端热添加 virtio、scsi 卷- 检查新增 virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    仅 scsi vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    无 scsi 卷但含未卸载的 virtio-scsi 控制器 vm - 目标端热添加 8scsi 卷 -  检查已有和新增 virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    源端热添加 vcpu 数 - 目标端热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    目标端热添加 vcpu 数、热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    目标端热添加 vcpu 数和 virtio、7scsi 卷- 关机重新开机 - 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                跨集群冷迁移
                                    跨集群冷迁移后，虚拟机开机 - 检查已有卷、控制器 queues：目标端 MIN(max_num_queues，最新 nvCPU)
                                    跨集群冷迁移后，虚拟机开机 - 热添加 virtio、7scsi 卷- 检查已有新增卷、控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                            6.0.x 到 515迁移
                                跨集群热迁移
                                    自动多队列配置开机虚拟机 - 跨集群热迁移 - 不支持迁移
                                跨集群分段迁移
                                    源端保留 vm，源端重新开机 - 检查已有卷：源端采用源端自动多队列配置，目标端采用目标端静态配置
                                    源端不保留 vm，目标端开机 - 检查已有卷：目标端：目标端静态配置
                                    含 virtio、scsi vm - 目标端热添加 virtio、7scsi 卷 - 检查已有和新增卷、控制器 queues：目标端静态配置
                                    仅 ide vm - 目标端热添加 virtio、scsi卷 - 检查新增 virtio 卷、virtio-scsi 控制器 queues：目标端静态配置
                                    仅 virtio vm - 目标端热添加 virtio、scsi 卷- 检查新增 virtio-scsi 控制器 queues：目标端静态配置
                                    仅 scsi vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷、virtio-scsi 控制器 queues：目标端静态配置
                                    无 scsi 卷但含未卸载的 virtio-scsi 控制器 vm - 目标端热添加 8scsi 卷 -  检查已有和新增 virtio-scsi 控制器 queues：目标端静态配置
                                    源端热添加 vcpu 数 - 目标端热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端静态配置
                                    目标端热添加 vcpu 数、热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端静态配置
                                    目标端热添加 vcpu 数和 virtio、7scsi 卷- 关机重新开机 - 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端静态配置
                                跨集群冷迁移
                                    跨集群冷迁移后，虚拟机开机 - 检查已有卷、控制器 queues：目标端静态配置
                                    跨集群冷迁移后，虚拟机开机 - 热添加 virtio、7scsi 卷- 检查已有新增卷、控制器 queues：目标端静态配置
                            6.1.x 到 515 迁移
                                跨集群热迁移
                                    自动多队列配置开机虚拟机 - 跨集群热迁移 - 不支持迁移
                                跨集群分段迁移
                                    源端保留 vm，源端重新开机 - 检查已有卷：源端采用源端自动多队列配置，目标端采用目标端静态配置
                                    源端不保留 vm，目标端开机 - 检查已有卷：目标端：目标端静态配置
                                    含 virtio、scsi vm - 目标端热添加 virtio、7scsi 卷 - 检查已有和新增卷、控制器 queues：目标端静态配置
                                    仅 ide vm - 目标端热添加 virtio、scsi卷 - 检查新增 virtio 卷、virtio-scsi 控制器 queues：目标端静态配置
                                    仅 virtio vm - 目标端热添加 virtio、scsi 卷- 检查新增 virtio-scsi 控制器 queues：目标端静态配置
                                    仅 scsi vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷、virtio-scsi 控制器 queues：目标端静态配置
                                    无 scsi 卷但含未卸载的 virtio-scsi 控制器 vm - 目标端热添加 8scsi 卷 -  检查已有和新增 virtio-scsi 控制器 queues：目标端静态配置
                                    源端热添加 vcpu 数 - 目标端热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端静态配置
                                    目标端热添加 vcpu 数、热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端静态配置
                                    目标端热添加 vcpu 数和 virtio、7scsi 卷- 关机重新开机 - 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端静态配置
                                跨集群冷迁移
                                    跨集群冷迁移后，虚拟机开机 - 检查已有卷、控制器 queues：目标端静态配置
                                    跨集群冷迁移后，虚拟机开机 - 热添加 virtio、7scsi 卷- 检查已有新增卷、控制器 queues：目标端静态配置
                    两集群自动多队列配置不一致
                        支持多队列自动配置的版本间迁移
                            515跨集群迁移到60.x
                                跨集群迁移
                                    跨集群热迁移
                                        跨集群热迁移后 - 检查已有 virtio 卷、virtio-scsi 控制器的 queues 不变
                                        仅 ide vm - 目标端热添加 virtio、scsi卷 - 检查新增 virtio 卷、virtio-scsi 控制器  queues：目标端 MIN(max_num_queues, 初始 nvCPU)
                                        仅 virtio vm - 目标端热添加 virtio、scsi 卷- 检查新增 virtio-scsi 控制器 queues:源端 MIN(max_num_queues,初始 nvCPU)， virtio 与已卷一致
                                        仅 scsi vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷 queues：源端 MIN(max_num_queues,初始 nvCPU)，virtio-scsi 控制器 与源控制器一致
                                        无 scsi 卷但含未卸载的 virtio-scsi 控制器 vm - 目标端热添加 8scsi 卷 -  检查已有和新增 virtio-scsi 控制器 queues：与源控制器一致
                                        含 virtio、scsi ide vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷、virtio-scsi 控制器 queues：源端MIN(max_num_queues，初始 nvCPU)
                                        源端热添加 vcpu 数 - 目标端热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：源端 MIN(max_num_queues，初始 nvCPU)
                                        目标端热添加 vcpu 数、热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：源端 MIN(max_num_queues，初始 nvCPU)
                                        目标端热添加 vcpu 数和 virtio、7scsi 卷- 关机重新开机 - 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，最新nvCPU)
                                    跨集群分段迁移
                                        源端保留 vm，源端重新开机 - 检查已有卷：源端采用源端配置，目标端采用目标端配置
                                        含 virtio、scsi vm - 目标端热添加 virtio、7scsi 卷 - 检查已有和新增卷、控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    跨集群冷迁移
                                        跨集群冷迁移后，虚拟机开机 - 检查已有卷、控制器 queues：目标端 MIN(max_num_queues，最新 nvCPU)
                                        跨集群冷迁移后，虚拟机开机 - 热添加 virtio、7scsi 卷- 检查已有新增卷、控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                            515跨集群迁移到61.x及以上
                                跨集群迁移
                                    跨集群热迁移
                                        跨集群热迁移后 - 检查已有 virtio 卷、virtio-scsi 控制器的 queues 不变
                                        仅 ide vm - 目标端热添加 virtio、scsi卷 - 检查新增 virtio 卷、virtio-scsi 控制器  queues：目标端 MIN(max_num_queues, 初始 nvCPU)
                                        仅 virtio vm - 目标端热添加 virtio、scsi 卷- 检查新增 virtio-scsi 控制器 queues:源端 MIN(max_num_queues,初始 nvCPU)， virtio 与已卷一致
                                        仅 scsi vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷 queues：源端 MIN(max_num_queues,初始 nvCPU)，virtio-scsi 控制器 与源控制器一致
                                        无 scsi 卷但含未卸载的 virtio-scsi 控制器 vm - 目标端热添加 8scsi 卷 -  检查已有和新增 virtio-scsi 控制器 queues：与源控制器一致
                                        含 virtio、scsi ide vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷、virtio-scsi 控制器 queues：源端MIN(max_num_queues，初始 nvCPU)
                                        源端热添加 vcpu 数 - 目标端热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：源端 MIN(max_num_queues，初始 nvCPU)
                                        目标端热添加 vcpu 数、热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：源端 MIN(max_num_queues，初始 nvCPU)
                                        目标端热添加 vcpu 数和 virtio、7scsi 卷- 关机重新开机 - 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端 MIN(max_num_queues，最新nvCPU)
                                    跨集群分段迁移
                                        源端保留 vm，源端重新开机 - 检查已有卷：源端采用源端配置，目标端采用目标端配置
                                        含 virtio、scsi vm - 目标端热添加 virtio、7scsi 卷 - 检查已有和新增卷、控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                                    跨集群冷迁移
                                        跨集群冷迁移后，虚拟机开机 - 检查已有卷、控制器 queues：目标端 MIN(max_num_queues，最新 nvCPU)
                                        跨集群冷迁移后，虚拟机开机 - 热添加 virtio、7scsi 卷- 检查已有新增卷、控制器 queues：目标端 MIN(max_num_queues，初始 nvCPU)
                            6.0.x 迁移到 515
                                跨集群热迁移
                                    源端通过procurator配置了多队列且不为1 - 含 virtio、scis 卷虚拟机 - 跨集群热迁移 - QEMU 报错
                                    源端通过procurator配置了多队列且不为1 - 仅 ide vm - 跨集群热迁移到高版本 - 迁移成功
                                分段迁移
                                    源端保留 vm，源端重新开机 - 检查已有卷：源端采用源端自动多队列配置，目标端采用目标端自动多队列配置
                                    含 virtio、scsi vm - 目标端热添加 virtio、7scsi 卷 - 检查已有和新增卷、控制器 queues：目标端自动多队列配置
                                冷迁移
                                    跨集群冷迁移后，虚拟机开机 - 检查已有卷、控制器 queues：目标端自动多队列配置
                                    跨集群冷迁移后，虚拟机开机 - 热添加 virtio、7scsi 卷- 检查已有新增卷、控制器 queues：目标端自动多队列配置
                            6.1.x 迁移到515
                                跨集群热迁移
                                    源端通过procurator配置了多队列且不为1 - 含 virtio、scis 卷虚拟机 - 跨集群热迁移 - QEMU 报错
                                    源端通过procurator配置了多队列且不为1 - 仅 ide vm - 跨集群热迁移到高版本 - 迁移成功
                                分段迁移
                                    源端保留 vm，源端重新开机 - 检查已有卷：源端采用源端自动多队列配置，目标端采用目标端自动多队列配置
                                    含 virtio、scsi vm - 目标端热添加 virtio、7scsi 卷 - 检查已有和新增卷、控制器 queues：目标端自动多队列配置
                                冷迁移
                                    跨集群冷迁移后，虚拟机开机 - 检查已有卷、控制器 queues：目标端自动多队列配置
                                    跨集群冷迁移后，虚拟机开机 - 热添加 virtio、7scsi 卷- 检查已有新增卷、控制器 queues：目标端自动多队列配置
                    升级场景
                        支持自动多队列版本间迁移
                            515 存量 vm 迁移到 60.x
                                含 virtio、scsi ide vm - 跨集群热迁移后 - 检查已有 virtio 卷、virtio-scsi 控制器 queues 保持为1
                                含 virtio、scsi ide vm - 跨集群热迁移后，目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷、virtio-scsi 控制器 强制 queues 为1
                                含 virtio、scsi ide vm - 分段迁移后 - 检查已有卷：源端采用源端配置，目标端采用目标端配置
                                含 virtio、scsi ide vm - 冷迁移后开机 - 检查已有卷：源端采用源端配置，目标端采用目标端配置
                            515 存量 vm 迁移到 61.x
                                含 virtio、scsi ide vm - 跨集群热迁移后 - 检查已有 virtio 卷、virtio-scsi 控制器 queues 保持为1
                                含 virtio、scsi ide vm - 跨集群热迁移后，目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷、virtio-scsi 控制器 强制 queues 为1
                                含 virtio、scsi ide vm - 分段迁移后 - 检查已有卷：源端采用源端配置，目标端采用目标端配置
                                含 virtio、scsi ide vm - 冷迁移后开机 - 检查已有卷：源端采用源端配置，目标端采用目标端配置
            支持 boost 跨集群热迁移
                Tower UI
                    集群 xxx 版本低于 5.1.5，不支持 Boost 模式集群间热迁移
                        【源端目标端都开启 vhost】源端集群低于 515, 不允许跨集群热迁移
                        【源端目标端都开启 vhost】目标端集群低于 515, 不允许跨集群热迁移
                    Boost 模式启用状态不一致
                        【源端目标端都大于等于 515】源端开启 vhost，目标端未开启  vhost, 不允许跨集群热迁移
                        【源端目标端都大于等于 515】源端未开启 vhost，目标端开启  vhost, 不允许跨集群热迁移
                    源集群 xxx 版本号为 xxx，不支持热迁移到 xxx 版本的集群。
                        【源端集群大于目标端集群】都开启 vhost, 不允许跨集群热迁移
                    源集群和目标集群的 CPU 供应商不一致。
                        hygon 集群虚拟机跨集群热迁移到 intel 集群，不允许迁移，提示文案
                    相同版本
                        OS 5.1.5 vhost intel el7 跨集群热迁移到 OS 5.1.5 vhost intel el7， 迁移成功
                        OS 5.1.5 vhost hygon oe 跨集群热迁移到 OS 5.1.5 vhost hygon oe， 迁移成功
                        OS 5.1.5 vhost arm oe 跨集群热迁移到 OS 5.1.5 vhost arm oe， 迁移成功
                        OS 5.1.5 vhost hygon oe 跨集群热迁移到 OS 5.1.5 vhost hygon tl3， 迁移成功
                        OS 5.1.5 vhost arm tl3 跨集群热迁移到 OS 5.1.5 vhost arm oe， 迁移成功
                    相同版本系列，如 5.1.x
                        OS 5.1.5 intel el7 跨集群热迁移到 OS 5.1.4 intel el7， 不允许迁移【因版本低于 515不允许迁移】（是否开启 vhost 都不允许迁移）
                        OS 5.1.4 vhost intel el7 跨集群热迁移到 OS 5.1.5 vhost intel el7， 不允许迁移【因版本低于 515不允许迁移】
                        OS 5.1.4 intel el7 非 vhost 跨集群热迁移到 OS 5.1.5 intel el7 非 vhost， 迁移成功
                    低版本到高版本
                        OS 5.0.7 intel el7 vhost 跨集群热迁移到 OS 5.1.5 intel el7 vhost， 不允许迁移【因版本低于 515不允许迁移】
                        OS 5.1.4  intel el7 vhost 跨集群热迁移到 OS 5.1.5 intel el7 vhost， 不允许迁移【因版本低于 515不允许迁移】
                        OS 5.1.5 vhost intel el7 跨集群热迁移到 OS 6.0.x vhost intel el7， UI 不允许迁移
                        OS 5.1.5 vhost intel el7 跨集群热迁移到 OS 6.1.1 vhost intel el7， UI 允许迁移，迁移任务失败 PRECHECK_VOLUME_PROPERTIES_CHANGE_AFTER_ACM
                        OS 5.1.5 vhost intel el7 跨集群热迁移到 OS 6.2.0 vhost intel el7， UI 允许迁移，迁移任务失败 PRECHECK_VOLUME_PROPERTIES_CHANGE_AFTER_ACM
                功能测试
                    OS 515 vhost intel el7 迁移到 OS 515 vhost intel el7， 迁移前后检查虚拟机属性一致
                故障测试
                    服务故障
                        zbs-chunkd
                            vhost 跨集群热迁移触发，源端主机服务故障
                            vhost 跨集群热迁移触发，目标端主机服务故障
                    主机故障
                        vhost 跨集群热迁移触发，源端主机重启
                        vhost 跨集群热迁移触发，目标端主机重启
                集群运维
                    vhost 转化
                        vhost 关闭转为开启的集群1，历史虚拟机跨集群热迁移虚拟机到 vhost 集群2， 迁移成功
                        vhost 开启转为关闭的集群1，历史虚拟机跨集群热迁移虚拟机到非 vhost 集群2， 迁移成功
                    集群扩容
                        vhost 集群1 扩容 1 个节点，历史虚拟机跨集群热迁移虚拟机到 vhost 集群2， 迁移成功
            使用 libvirt 6.2 和 qemu 6.2 以支持 boost 模式改进
                迁移限制
                    SMTXOS 515 跨集群热迁移到 低版本（vhost 和 非 vhost） - 不允许迁移
                    SMTXOS 515 跨集群热迁移到 6.0.x（vhost 和 非 vhost） - 不允许迁移
            禁止 515 跨集群热迁移到 60x 及 515 之前版本集群
                515 跨集群热迁移到 60x 集群，UI 约束不允许
                515 跨集群热迁移到小于515 的 51x 集群，UI 约束不允许
                515 跨集群热迁移到 50x 集群.，UI 约束不允许
                515 跨集群热迁移到 40x 集群，UI 约束不允许
            Boost 模式下保证虚拟卷属性不变
                虚拟机生命周期
                    创建虚拟机，检查虚拟机虚拟卷属性
                        创建新虚拟卷
                        挂载普通虚拟卷
                        挂载共享虚拟卷
                        挂载 NFS 虚拟卷
                    克隆虚拟机，新生成的虚拟卷属性与源虚拟机不保持一致
                        快速克隆
                        完全拷贝克隆
                        创建新虚拟卷
                        挂载共享虚拟卷
                    虚拟机模板
                        模板转化为虚拟机，虚拟卷属性与源虚拟机不保持一致
                        虚拟机克隆为模板，模板不包含(product, vendor, serial, wwn)属性
                        虚拟机转化为模板，模板不包含(product, vendor, serial, wwn)属性
                        从模板创建虚拟机，新生成的虚拟卷属性与源虚拟机不保持一致
                            快速克隆
                            完全拷贝克隆
                            创建新虚拟卷
                            挂载共享虚拟卷
                    快照
                        创建虚拟机快照，虚拟机快照不保存磁盘属性
                        快照回滚虚拟机，虚拟卷属性保持一致
                        快照重建虚拟机，虚拟卷属性与源虚拟机不保持一致
                            快速克隆
                            完全拷贝克隆
                            创建新虚拟卷
                            挂载普通虚拟卷
                            挂载共享虚拟卷
                            挂载 NFS 虚拟卷
                    编辑虚拟机，虚拟卷属性保持一致
                        新建虚拟卷
                        挂载其他虚拟卷
                        虚拟卷扩容
                        普通虚拟卷卸载再挂载
                        共享虚拟卷卸载再挂载
                    虚拟机状态变更，虚拟卷属性保持一致
                        虚拟机关机再开机
                        虚拟机暂停再恢复
                        虚拟机重启，强制重启
                虚拟卷
                    创建普通虚拟卷
                    创建共享虚拟卷
                    创建 NFS 虚拟卷
                    共享虚拟卷挂载到不同虚拟机，虚拟卷属性保持一致
                    普通虚拟卷，卸载再挂载到不同虚拟机，虚拟卷属性保持不变
                OVF
                    导入虚拟机
                    导入虚拟机，新建卷
                    导入虚拟机，挂载共享卷
                    虚拟机导出再导入，属性不保持
                    导入虚拟卷
                    虚拟卷导出再导入，属性不保持
                迁移
                    集群内迁移 - 虚拟卷属性保持一致
                        集群内热迁移
                        集群内冷迁移
                    跨集群热迁移
                        低版本集群（4.0.x、5.0.x、5.1.x）迁移到 5.1.5，虚拟卷属性变更
                        5.1.5 迁移到 5.1.5，虚拟卷属性保持一致
                        5.1.5 迁移到 6.2.0，源集群未关闭虚拟卷属性检查，迁移失败
                        5.1.5 迁移到 6.2.0，源集群关闭虚拟卷属性检查，迁移成功，虚拟卷属性不保持一致
                    跨集群冷迁移
                        5.1.5 迁移到 5.1.5，虚拟卷属性保持一致
                        5.1.5 迁移到 6.2.1 \ 6.3.0，虚拟卷属性保持一致
                        低版本集群（4.0.x、5.0.x、5.1.x） 迁移到 5.1.5，虚拟卷属性不保持一致
                        5.1.5 迁移到 6.2.0，虚拟卷属性不保持一致
                        5.1.5 迁移到低版本集群（4.0.x、5.0.x、5.1.x），虚拟卷属性不保持一致
                    跨集群分段迁移
                        5.1.5 迁移到 5.1.5，虚拟卷属性保持一致
                        5.1.5 迁移到 6.2.1 \ 6.3.0，虚拟卷属性保持一致
                        低版本集群（4.0.x、5.0.x、5.1.x） 迁移到 5.1.5，虚拟卷属性不保持一致
                        5.1.5 迁移到 6.2.0，虚拟卷属性不保持一致
                        5.1.5 迁移到低版本集群（4.0.x、5.0.x、5.1.x），虚拟卷属性不保持一致
                    SMTX ELF 集群
                        仅迁移计算
                            仅迁移计算，虚拟卷属性保持一致
                        仅迁移存储
                            仅迁移存储，虚拟卷属性保持一致
                        迁移计算与存储
                            迁移计算与存储，虚拟卷属性保持一致
                集群开关 Boost 模式
                    集群开启 Boost，虚拟机虚拟卷属性保持不变
                    集群关闭 Boost，虚拟机虚拟卷属性保持不变
                集群升级
                    低版本虚拟机包含 NFS 虚拟卷，升级后检查
                        克隆创建虚拟机
                        从快照回滚虚拟机
                        快照重建虚拟机
                        转化为模板
                    低版本虚拟机模板
                        从模板创建虚拟机
                        模板转化为虚拟机
                    低版本虚拟机快照
                        从快照重建虚拟机
                        回滚虚拟机快照
                    低版本虚拟机，升级后，检查虚拟机虚拟卷属性与升级前保持一致
                        关机再开机
                        重启虚拟机
                        虚拟机包含挂载给多个虚拟机的共享卷
                        编辑虚拟机添加/删除磁盘
                        创建虚拟机快照，从快照回滚虚拟机
                        创建虚拟机快照，从快照重建虚拟机
                        克隆创建虚拟机
                        虚拟机转化为模板
                        集群内迁移
                        跨集群热迁移
                        跨集群冷迁移
                        跨集群分段迁移
                    升级版本覆盖
                        非 boost 模式集群升级
                            4.0.4 升级到 5.1.5
                            4.0.14 升级到 5.1.5
                            5.0.0 升级到 5.1.5
                            5.0.5 升级到 5.1.5
                            5.0.0 升级到 5.0.5 升级到 5.0.7 再升级到 5.1.5
                            5.0.7 hp1 升级到 5.1.5
                            5.1.4 升级到 5.1.5
                            5.1.4升级到630
                        boost 模式集群升级
                            5.1.2 升级到 5.1.5
                            5.1.4 升级到 5.1.5
                            5.1.2 升级到 6.3.0
                            5.1.4 升级到 6.3.0
                            5.1.5升级到6.3.0
                API 变更
                    POST /api/v2/vms，磁盘支持指定 vendor、product、serial、wwn
                    POST /api/v2/volumes，磁盘支持指定 vendor、product、serial、wwn
                CLI 变更
                    查看虚拟卷属性 elf-tool elf_volume show_properties <volume_uuid>
                    修改未被开机虚拟机挂载的虚拟卷属性 elf-tool elf_volume update_properties，修改成功
                    修改被关机虚拟机挂载到虚拟卷属性 elf-tool elf_volume update_properties，修改失败
                    查看虚拟卷属性检查配置默认启用， elf-tool elf_cluster show_acm_volume_properties_check
                    禁用虚拟卷属性检查， elf-tool elf_cluster update_acm_volume_properties_check disable
                    启用虚拟卷属性检查， elf-tool elf_cluster update_acm_volume_properties_check enable
                Tower 变更
                    graphql 检查虚拟机虚拟卷增加 vendor、product、serial 和 wwn 四个字段
                    跨集群迁移，虚拟卷属性检查（迁移章节的用例覆盖）
                    升级前后，虚拟机磁盘内部设备名展示正常
            ELF-7391 kvm internal error 触发 HA
                kvm internal error 触发 HA（本地重建）
                unsafe-stop 触发 HA（本地重建）
                virsh suspend 触发 HA ( 本地重建 )
            ELF-6537 对[完全克隆] 操作限速
                验收测试
                    默认配置信息检查
                        检查命令行修改速率工具可用：elf-tool copy_volume --help  - 执行正常不报错
                        检查限速配置：elf-tool copy_volume show_capability - 展示限速配置：enabled: False
total_tasks_max_bps: 900 MB/s
task_max_bps: 300 MB/s
                        检查系统配置的全局最大数据是 900MB/S，即：db.cluster_capabilities.find().pretty()的 "type" : "copy_volume_max_bps"，total_tasks_max_bps=7549747200
                    限速开启
                        开默认限速：从模版 - 完全克隆创建5个虚拟机3个 大小一致的卷  - 检查 初始速率是 90MB/s(754974720bps)
                        开默认限速：克隆虚拟机 - 完全克隆创建5个虚拟机3个 大小不一致的卷  - 检查 初始速率是 90MB/s(754974720bps)
                        开默认限速：克隆虚拟机 - 完全克隆创建5个虚拟机3个 大小一致的卷  - 检查60s 定时任务后， 速率都更新为 60M(503316480bps)
                        开默认限速：从模版 - 完全克隆创建 5 个虚拟机 3个 大小不一致的卷  - 有 10 个卷任务已结束，检查60s 定时任务，速率都更新为 180MB/s(1342177280bps)
                        开默认限速：并发 3个快照重建含3个卷的虚拟机 - 检查初始速率 90MB/S，有1个虚拟机创建结束，60s时后定时任务速率更新为 150 MB/S(1258291200bps)
                功能测试
                    限速开关检查
                        低版本升级到515的集群 - 检查 限速配置为关闭:elf-tool copy_volume show_capability 的 enable:False
                        新部署的515的集群 - 检查 限速配置为关闭:elf-tool copy_volume show_capability 的 enable:False
                        低版本升级到515的集群 - 开启限速 成功 elf-tool copy_volume enable ，限速生效
                        新部署 515的集群 - 开启限速 成功 elf-tool copy_volume enable ，限速生效
                        限速配置关闭 - 批量完全克隆多个 vm：N个卷  - 每个任务 bps 默认为 300MB/s（2516582400），且不随任务数量变化
                        限速配置开启，使用默认配置状态下 - 批量完全克隆多个 vm：N 个卷  - 任务初始速率 90MB/s，60s 后触发动态限速，任务速率跟随数量变化：速率（900/N）
                        限速配置开启，是用自定义配置（总速率800MB/s，单个速率 200MB/s）状态下 - 批量完全克隆多个 vm ：N个卷 - 任务初始速率 300MB/s，60s 后触发动态限速，任务速率跟随数量变化(800/N)
                        限速配置关闭 - 批量完全克隆多个 vm 共 N个卷 ---> 任务未结束时调整为限速配置开启：自定义限速 总速率800MB/S，单个速率 200MB/S） ---> 关闭限速配置 - 可以观察到限速配置变化：300MB/s ---> (800/N) MB/S--->300MB/s
                    限速适用范围检查
                        elf 发起的任务限速
                            覆盖各类卷类型
                                创建 3个含 2nfs 卷的虚拟机 完全克隆 - 检查 初始速率是 90MB/s(754974720Mbps)，60s 后同步速率是 150MB/S (1258291200)
                                创建 3个含 1scsi+2nfs 卷的虚拟机 完全克隆 - 检查 初始速率是 90MB/s(754974720Mbps)，定时任务 60s 后同步速率是 100MB/S (838860800)，3个小容量 nfs 任务结束，定时任务同步速率是：150MB/S(1258291200)
                                创建 3个含 1ec +1副本 卷的虚拟机 完全克隆 - 检查 初始速率是 90MB/s(754974720Mbps)，60s 后同步速率是 150MB/S (1258291200)
                        集群
                            新部署515 版本 - 批量创建完全克隆虚拟机 - 检查正常可用，限速正确
                            低版本升级到515 版本 - 批量完全克隆虚拟机 -检查正常可用，限速正确
                    场景测试
                        最大速率不超过指定的最大速率
                            完全克隆创建1个虚拟机1个卷  - 检查 初始速率是 90MB/s(754974720Mbps)，60s 后同步速率是 300MB/S (2516582400)，一直到任务结束
                            完全克隆创建2个虚拟机1个卷  - 检查 初始速率是 90MB/s(754974720Mbps)，60s 后同步速率是 300MB/S (2516582400)，一直到任务结束
                        速率随当前卷数量变化
                            完全克隆创建容量大小不同的6卷 - 初始速率 90MB/S - 检查限速是根据当前卷数量计算：定时任务60s 调整时，剩余5个卷，限速 160MB/S，120s时，剩余金额2个卷 300MB/S
                            发起 20个单个虚拟卷的定时任务 - 间隔 60s 定时任务更新后速率为 45MB/S
                            分批次发起任务，如：发起 5 个完全克隆任务，1分钟后再次发起 15 个完全克隆任务 - 在周期任务调整下每个任务的速率变化为 90 -> 180 -> 45（第二个任务15个看了任务初始速率90MB/s）
                        限速效果测试
                            发起5个完全克隆任务，观察集群 IO 带宽 - 克隆任务带来的 IO 带宽增加与 total_tasks_max_bps 限制接近
                    命令行检查
                        配置检查
                            检查限速配置：elf-tool copy_volume show_capability - 展示限速配置：enabled: False
total_tasks_max_bps: 900 MB/s
task_max_bps: 300 MB/s
                            调整全局速率：elf-tool copy_volume set_total_tasks_max_bps xxx （单位MB/S）- 输入合法数据，如：1000 配置成功
                            调整单个任务最大速率：elf-tool copy_volume set_task_max_bps xxx （单位MB/S） - 输入合法数据，如：200 配置成功
                            调整单个任务最大速率：elf-tool copy_volume set_task_max_bps xxx （单位MB/S） - 输入非法数据，如：abc，报错， 配置失败
                            调整全局速率：elf-tool copy_volume set_total_tasks_max_bps xxx （单位MB/S）- 输入非法数据，如：abc，报错， 配置失败
                            手动插入一个重复的 copy_volume_max_bps 配置，然后 elf-tool 修改最大速率限制 - 重复的配置被移除，且配置修改正常生效
                            elf-tool copy_volume 【全局速率set_total_tasks_max_bps 】小于【单个任务最大速率elf-tool copy_volume set_task_max_bps 】有校验无法保存
                            开启限速：elf-tool copy_volume enable
                            关闭限速：elf-tool copy_volume disenable
                            输入错误命令：开启限速：elf-tool copy_volume enable1 - 报错
                            关闭限速时调整总任务、单个速率：能配置，后续开启限速时生效
                            开启限速时调整总任务、单个速率：能配置，触发任务时生效
                        有效性检查
                            减少全局速率和单个任务最大速率
                                完全克隆创建1个虚拟机5个卷  - 检查 初始速率是 90MB/s(754974720Mbps)，60s 后同步速率是 160MB/S ，有3个虚拟卷创建结束 - 第二个60s 同步速率：单个任务最大限速生效 200MB/S
                            增大全局速率和单个任务速率
                                配置单个任务速率大于全局速率 - 检查最终是全局限速生效
                                完全克隆创建1个虚拟机3个卷  - 检查 初始速率是 90MB/s(754974720Mbps)，60s 后同步速率是 333.33MB/S ，又一个虚拟卷创建结束 - 第二个60s 同步速率：单个任务最大限速生效：350MB/S
                性能测试
                    并发 克隆10个任务 - 观察存储网络ping 是否有延迟
                    并发 克隆20个任务 -  观察存储网络ping 是否有延迟
                    并发 克隆50个任务 - 观察io延时（初始速率90MB/S） 观察存储网络ping 是否有延迟
                    含 68 个卷的虚拟机进行完全克隆 - 初始速率90MB/s ，总体速率可能超过900 MB， 观察存储网络ping 是否有延迟
                故障测试
                    发起完全克隆后，在 zbs task 运行中停止节点的 job-center-worker；zbs task 运行结束后再启动 job-center-worker，发起 5 个完全克隆任务 - 不回进行速率调整默认90MB，任务结束请例残留的 elf tasks
                    发起完全克隆后，在 zbs task 运行中所有停止节点的 job-center-worker； - zbs task 结束后 elf_tasks 中存在残留记录，10分钟后被清除
                    发起完全克隆后，copy volume 运行中取消 zbs task 任务 （执行 zbs-task task cancel {task_id} 取消）- elf_tasks 记录正常删除
                    并发问题模拟测试： 在 create_task 后插入 sleep 60，模拟 create_task -> 周期任务 -> create zbs_task 场景 - 第一次周期任务不会删除 elf_task，create zbs_task 后 bps 正常调整，运行结束后，elf_task 正常移除【后续模拟】
                    并发问题模拟测试： 在 elf_tasks 数据库中插入一个不存在对应 zbs_task 的记录，mtime 为当前时间 - 600s 后，该记录被移除
                    发起完全克隆后，停止集群所有节点 zbs-taks任务 - 预期完全克隆失败
                系统信息检查
                    数据库
                        数据库 - 升级515 新增 - smartx.cluster_capabilities 表中存在 新类型：copy_volume_max_bps 配置类型的数据,默认关闭
                        数据库：新增记录 resources.elf_tasks 表中存在 新类型：copy_volume 配置类型的数据，bps 是实际速率（单位 bps） - 关闭限速，速率始终为 300MB/S（2516582400）;开启限速，会动态变化，按当前定时任务 60s 同步时的数据量平分900M/s)
                        完全克隆任务结束后检查 resources.elf_task 记录被删除，只有在有完全克隆进行中才能观察到记录
                        新部署 515 集群 - 检查数据库有  smartx.cluster_capabilities 表中存在 新类型：copy_volume_max_bps 配置类型的数据
                    zbs 命令检查
                        zbs 检查实际速率：zbs-task task show {task_id} - 检查zbs task 的 bps（单位 Byte per second，Bps）
                        完全克隆任务结束后，zbs-task task show {task_id} 记录仍然保留，- zbs task 的 bps 是最后一次更新后的速率
                        zbs 检查当前正在执行完全克隆的task - zbs-task task list_by_status {unfinished/finished} --task_type copy_volume
                    日志检查
                        定时任务间隔 60s：less job-center-scheduler.INFO|grep "adjust_copy_volume_speed"  - 检查间隔 60s 发送定时任务给 job-center-worker
                        定时任务更新正常：可能在集群运行 job-center-worker 的任意节点：grep "adjust_copy_volume_speed" job-center-worker.INFO | grep update - 间隔60s
            ELF-7479 快照重建虚拟机保持网卡 PCI 地址不变
                快照中多块网卡 PCI 地址连续
                    快照重建虚拟机，保持原网卡配置，检查网卡 PCI 地址不变
                    快照重建虚拟机，新增网卡，检查原网卡 PCI 地址不变
                    快照重建虚拟机，删除一块原网卡，检查未删除的网卡 PCI 地址不变
                    快照重建虚拟机，删除一块原 VIRTIO 网卡，新增一块 E1000 网卡，不保证网卡 PCI 地址不变
                    快照重建虚拟机，删除一块原 E1000 网卡，新增一块 VIRTIO 网卡，不保证网卡 PCI 地址不变
                    快照重建虚拟机，新增网卡，并调整网卡顺序，不保证网卡 PCI 地址不变
                    快照重建虚拟机，新增 SRIOV 网卡，原网卡 PCI 地址不变
                快照中多块网卡 PCI 地址不连续
                    快照重建虚拟机，保持原网卡配置，检查网卡 PCI 地址不变
                    快照重建虚拟机，新增网卡，检查原网卡 PCI 地址不变
                    快照重建虚拟机，删除一块原网卡，检查未删除的网卡 PCI 地址不变
                    快照重建虚拟机，删除一块原 VIRTIO 网卡，新增一块 E1000 网卡，不保证网卡 PCI 地址不变
                    快照重建虚拟机，删除一块原 E1000 网卡，新增一块 VIRTIO 网卡，不保证网卡 PCI 地址不变
                    快照重建虚拟机，新增网卡，并调整网卡顺序，不保证网卡 PCI 地址不变
                    快照重建虚拟机，新增 SRIOV 网卡，原网卡 PCI 地址不变
            ELF-7633 SMTXOS 515 禁用磁盘 TRIM/UNMAP 特性
                虚拟机生命周期
                    非 vhost 环境含 scsi+virtio的 Linux虚拟机 - 检查 虚拟机内部：scsi 卷discard 开启、virtio关闭，实际都不支持trim回收
                    非 vhost 环境含 scsi+virtio的 windows 虚拟机 - 检查 虚拟机内部：scsi 卷discard 开启、virtio关闭，实际都不支持trim回收
                    vhost 环境含 scsi+virtio的 Linux虚拟机 - 检查 虚拟机内部：scsi 、virtio 卷 discard 关闭，实际都不支持trim回收
                    vhost 环境含 scsi+virtio的 windows 虚拟机 - 检查 虚拟机内部：scsi 、virtio 卷 discard 关闭，实际都不支持trim回收
                    非vhost集群 - windows  虚拟机热添加 virtio 、scsi 卷 - 检查虚拟机内部： scsi 卷discard 开启、virtio关闭，实际都不支持trim回收
                    vhost集群 - linux 虚拟机热添加 virtio 、scsi 卷 - 检查虚拟机内部： virtio 、scsi 卷discard 关闭，实际都不支持trim回收
                迁移
                    集群内
                        非 vhost 集群含 virtio 、scsi 的 linux 虚拟机 - 集群内热迁移到其他节点 - 检查 虚拟机内部：scsi 卷discard 开启、virtio关闭，实际都不支持trim回收
                        非 vhost 集群含 virtio 、scsi 的关机 windows 虚拟机 - 集群内冷迁移到其他节点后开机 - 检查 虚拟机内部：scsi 卷discard 开启、virtio关闭，实际都不支持trim回收
                        vhost 集群含 virtio 、scsi 的 windows 虚拟机 - 集群内热迁移到其他节点 - 检查 虚拟机内部：scsi、virtio 卷 discard 关闭，实际都不支持trim回收
                        vhost 集群含 virtio 、scsi 的关机 linux 虚拟机 - 集群内冷迁移到其他节点后开机 - 检查 虚拟机内部：scsi、virtio 卷 discard 关闭，实际都不支持trim回收
                    跨集群
                        同版本
                            非 vhost 集群 - 含 virtio、scsi卷的 linux 虚拟机 - 热迁移到 515 集群 - 迁移成功，目标端集群：scsi 卷discard 开启、virtio关闭，实际都不支持trim回收
                            非 vhost 集群 - 含 virtio、scsi卷的 windows 虚拟机 - 热迁移到 515 集群 - 迁移成功，目标端集群：热添加 scsi 、virtio,检查 scsi 卷discard 开启、virtio关闭，实际都不支持trim回收
                            非 vhost 集群 - 含 virtio、scsi卷的 linux 虚拟机 - 热迁移到 515 集群 - 迁移成功，目标端集群：热添加 scsi 、virtio,关机重新开机 - 检查已有和热添加卷：scsi 卷discard 开启、virtio关闭，实际都不支持trim回收
                            非 vhost 集群 - 含 virtio、scsi卷的linux 虚拟机 - 分段迁移到515集群 - 迁移成功，目标端集群：scsi 卷discard 开启、virtio关闭，实际都不支持trim回收
                            vhost 集群 - 含 virtio、scsi卷的 linux 虚拟机 - 热迁移到 515 集群 - 迁移成功，目标端集群：scsi、virtio 卷 discard 关闭，实际都不支持trim回收
                            vhost 集群 - 含 virtio、scsi卷的 windows 虚拟机 - 热迁移到 515 集群 - 迁移成功，目标端集群：热添加 scsi 、virtio,检查 scsi、virtio 卷 discard 关闭，实际都不支持trim回收
                            vhost 集群 - 含 virtio、scsi卷的 linux 虚拟机 - 热迁移到 515 集群 - 迁移成功，目标端集群：热添加 scsi 、virtio,关机重新开机 - 检查已有和热添加卷：scsi、virtio 卷 discard 关闭，实际都不支持trim回收
                            vhost 集群 - 含 virtio、scsi卷的 windows 虚拟机 - 冷迁移到515集群开机 - 迁移成功，目标端集群：scsi、virtio 卷 discard 关闭，实际都不支持trim回收
                        不同版本间迁移
                            6.00 及以上迁移到5.1.5
                                开启 discard 属性 scsi、virtio 虚拟卷的虚拟机 - 跨集群热迁移 - 不支持迁移
                                vhost 620 开启 discard 属性 scsi、virtio 虚拟卷的 Linux 虚拟机 - 跨集群分段迁移 - 在源端保留虚拟机 - 源端开机生效、目标端discard 禁用
                                非 vhost 600 开启 discard 属性 scsi、virtio 虚拟卷的 windows 虚拟机 - 跨集群冷迁移 - 在源端保留虚拟机 - 源端开机生效、目标端开机 discard 禁用
                                检查高版本分段/冷迁移到高版本后 - scsi virtio 检查不发生trim磁盘空间清理
                            低版本 迁移到 515
                                非 vhost 集群 - 含 virtio、scsi卷的 linux 虚拟机 - 热迁移到 515 集群 - 迁移成功，目标端集群后、热添加scsi、virtio 后，及关机重新开机后 - scsi 卷discard 开启、virtio关闭，实际都不支持trim回收
                                vhost 集群 - 含 virtio、scsi卷的 linux 虚拟机 - 热迁移到 515 集群 - 迁移成功，目标端集群后、热添加scsi、virtio 后，及关机重新开机后 - scsi virtio 卷 discard 关闭，实际都不支持trim回收
                            515 迁移到 600
                                含 virtio、scsi卷的linux 虚拟机 - 热迁移到 600 集群 - tower ui禁止热迁移
                                vhost 集群 - 含 virtio、scsi卷的linux 虚拟机 - 分段迁移到600集群 - 迁移成功，目标端集群：scsi 、virtio卷支持trim回收
                                非 vhost 集群 - 含 virtio、scsi卷的linux 虚拟机 - 分段迁移到600集群 - 迁移成功，目标端集群：scsi 、virtio卷支持trim回收
                            515 迁移到 610（vhost）
                                含 virtio、scsi卷的windows  虚拟机 - 热迁移到610集群 - 迁移成功，目标端集群：virtio不支持trim回收，scsi 卷按情况支持
                                含 virtio、scsi卷的linux 虚拟机 - 热迁移到610集群 - 迁移成功，目标端集群：热添加 scsi 、virtio、网卡、修改vm名称，检查已有 virtio 卷不支持trim回收，scsi 按情况支持，热添加 scsi 、virtio 都支持 trim
                                含 virtio、scsi卷的windows 虚拟机 - 热迁移到610集群 - 迁移成功，目标端集群：热添加 scsi 、virtio,关机重新开机 - 检查已有和热添加  scsi 、virtio卷支持trim回收
                                含 virtio、scsi卷的linux 虚拟机 - 分段迁移到610集群 - 迁移成功，目标端集群：scsi 、virtio卷支持trim回收
                                含 virtio、scsi卷的linux 虚拟机 - 热迁移到610目标端集群后 - 创建虚拟机快照 01 - 虚拟机关机回滚到快照 01  - 重新开机：scsi 、virtio卷支持trim回收
                                含 virtio、scsi卷的linux 虚拟机 - 热迁移到610目标端集群后 - 集群内热迁移 virtio卷 不支持trim回收，scsi 根据情况支持
                                含 virtio、scsi卷的linux 虚拟机 - 热迁移到610目标端集群后,热添加 scsi、virtio - 跨集群热迁移到其他 620 -  已有 virtio卷 不支持trim回收，scsi 根据情况支持，热添加 scsi+virtio 支持回收
                                含 virtio、scsi卷的linux 虚拟机 - 热迁移到610目标端集群后 - 跨集群分段迁移到其他 600 -  scsi 、virtio卷 支持trim回收
                            515 迁移到 620(非 vhost)
                                含 virtio、scsi卷的linux 虚拟机 - 热迁移到620集群 - 迁移成功，目标端集群：scsi 卷discard 开启、virtio关闭，实际都不支持trim回收
                                含 virtio、scsi卷的 windows 虚拟机 - 热迁移到620集群 - 迁移成功，目标端集群：热添加 scsi 、virtio、网卡、修改vm名称,检查 scsi 卷discard 开启、virtio关闭，实际都不支持trim回收
                                含 virtio、scsi卷的linux 虚拟机 - 热迁移到620集群 - 迁移成功，目标端集群：热添加 scsi 、virtio,关机重新开机 - 检查已有和热添加  scsi 、virtio卷支持trim回收
                                含 virtio、scsi卷的linux 虚拟机 - 分段迁移到620集群 - 迁移成功，目标端集群：scsi 、virtio卷支持trim回收
                                含 virtio、scsi卷的linux 虚拟机 - 热迁移到620目标端集群后 - 创建虚拟机快照 01 - 快照重建vm,开机：scsi 、virtio卷支持trim回收
                                含 virtio、scsi卷的linux 虚拟机 - 热迁移到620目标端集群后 - 集群内热迁移 scsi 、virtio卷 不支持trim回收
                                含 virtio、scsi卷的 linux 虚拟机 - 热迁移到620目标端集群后 - 跨集群热迁移到其他 620 -  scsi 、virtio卷 不支持trim回收
                                含 virtio、scsi卷的linux 虚拟机 - 热迁移到620目标端集群后 - 跨集群分段迁移到其他 600 -  scsi 、virtio卷 支持trim回收
                                含 virtio、scsi卷的linux 虚拟机 - 分段迁移到620目标端集群后 - 跨集群分段迁移到其他 610 -  scsi 、virtio卷 支持trim回收
                                含 virtio、scsi卷的linux 虚拟机 - 热迁移到620目标端集群后 - 跨集群分段迁移到其他 620 -  scsi 、virtio卷 支持trim回收
                515unmap 配置检查
                    虚拟机 domain 中 disk 没有 discard unmap 相关属性
                    linux 在515 不支持 unmap - 预期执行 lsblk -discard 的 DISC-GRAN、DISC-MAX 为0 不支持 unmap，fstim -v /dev/sda 失败
                    windows 在515 不支持 unmap - 预期执行 fsutil fsinfo sectorinfo F: 为不支持剪裁，执行 回收 Optimize-Volume -DriveLetter F -ReTrim -Verbose 失败
                    非 vhost scsi 卷，Guest os 会展示为discard 开启，但实际不能回收 ZBS-13268
            SMTXOS 5.1.5 非 Boost 模式跨集群热迁移时磁盘数据迁移支持仅迁移有效数据
                功能测试
                    给磁盘格式化文件系统，对多个磁盘分区同时反复写零和非零，发起热迁移
                    给磁盘格式化文件系统，不写数据，发起热迁移
                    5.1.5新建虚拟机跨集群热迁移到5.1.5：	全零检测打开-仅迁移有效数据
                    5.1.5新建虚拟机跨集群热迁移到6.20：	全零检测关闭-迁移所有数据
                    从5.1.2升级到5.1.5存量开机虚拟机跨集群热迁移到5.1.5：	全零检测关闭-迁移所有数据
                    5.1.4开机虚拟机跨集群热迁移到5.1.5：	全零检测关闭-迁移所有数据
                    5.1.1开机虚拟机跨集群热迁移到5.1.5：	不支持跨集群热迁移
                功能配置字段
                    SMTXOS  6.2.0版本：迁移任务发起后use resources db.multi_cluster_migrate_info.find({migrate_state:"migrating"}, {detect_zeroes: 1})； detect_zeroes 是 1
                    SMTXOS 5.1.5版本：grep "QEMU_MONITOR_RECV_REPLY" /var/log/zbs/libvirtd.log | grep <vm uuid> |grep "mon="；grep blockdev-add /var/log/zbs/libvirtd.log | grep QEMU_MONITOR_IO_WRITE | grep <monitor 地址>；detect-zeroes 为 unmap
                性能测试
                    SMTXOS 5.1.5迁移到 SMTXOS 5.1.5 :迁移全部数据的性能测试   Intel
                        有系统虚拟机-50G数据盘，给磁盘分区但不挂载，随机写入5G全零0x00数据     发起跨集群热迁移，查看fisheye迁移耗时
                        有系统虚拟机-50G数据盘，给磁盘分区但不挂载，随机写5G非零0xFF数据      发起跨集群热迁移，查看fisheye迁移耗时
                    SMTXOS 5.1.5迁移到 SMTXOS 5.1.5 :仅迁移有效数据的性能测试  ARM
                        有系统虚拟机-50G数据盘，给磁盘分区但不挂载，随机写入5G全零0x00数据     发起跨集群热迁移，查看fisheye迁移耗时
                        有系统虚拟机-50G数据盘，给磁盘分区但不挂载，随机写5G非零0xFF数据      发起跨集群热迁移，查看fisheye迁移耗时
                        有系统虚拟机-50G数据盘，给磁盘分区但不挂载，不写数据      发起跨集群热迁移，查看fisheye迁移耗时
                        有系统虚拟机-50G数据盘，给磁盘分区但不挂载，随机写入50G全零0x00数据     发起跨集群热迁移，查看fisheye迁移耗时
                        有系统虚拟机-50G数据盘，给磁盘分区但不挂载，随机写50G非零0xFF数据      发起跨集群热迁移，查看fisheye迁移耗时
                        有系统虚拟机-50G数据盘，给磁盘分区但不挂载，顺序写入50G全零0x00数据     发起跨集群热迁移，查看fisheye迁移耗时
                        有系统虚拟机-50G数据盘，给磁盘分区但不挂载，顺序写50G非零0xFF数据      发起跨集群热迁移，查看fisheye迁移耗时
                    SMTXOS 5.1.5迁移到 SMTXOS 5.1.5 :迁移全部数据的性能测试  hygon
                        有系统虚拟机-50G数据盘，给磁盘分区但不挂载，随机写入5G全零0x00数据     发起跨集群热迁移，查看fisheye迁移耗时
                        有系统虚拟机-50G数据盘，给磁盘分区但不挂载，随机写5G非零0xFF数据      发起跨集群热迁移，查看fisheye迁移耗时
            ELF-7655  515 禁用 磁盘自动对队列
                515 集群检查
                    检查集群只有静态多队列配置文件 - cat /etc/libvirt/qemu.conf - 队列数 1
                    创建 5vcpu vm  - 检查 virtio 卷、virtio-scsi 控制器 queues：为1
                    5vcpu vm - 热添加 1virtio+7scsi 卷 -  检查：virtio 卷、virtio-scsi 控制器 queues：为1
                    2vcpu vm热添加到 5vcpu   - 检查已有 virtio 卷、virtio-scsi 控制器 queues：为1
                    2vcpu vm热添加到 5vcpu   - 检查热添加 1virtio+7scsi 卷 - virtio 卷、virtio-scsi 控制器 queues：为1
                    含 virtio、scsi 卷的5vcpu vm - 集群内热迁移 -  检查：virtio 卷、virtio-scsi 控制器 queues：为1
                    含 virtio、scsi 卷的 5vcpu vm - 跨集群热迁移 -  检查：已有virtio 卷、virtio-scsi 控制器 queues：为1
                    含 virtio、scsi 卷的 5vcpu vm - 跨集群热迁移后，热添加  1virtio+7scsi-  检查：virtio 卷、virtio-scsi 控制器 queues：为1
                    仅含 ide 卷的 5vcpu vm - 跨集群热迁移后，热添加  1virtio+7scsi-  检查：virtio 卷、virtio-scsi 控制器 queues：为1
                低版本迁移至 515集群
                    跨集群热迁移后 - 检查已有 virtio 卷、virtio-scsi 控制器 queues 强制为1
                    仅 ide vm - 目标端热添加 virtio、scsi卷 - 检查新增 virtio 卷、virtio-scsi 控制器  queues：为1
                    仅 virtio vm - 目标端热添加 virtio、scsi 卷- 检查新增 virtio-scsi 控制器 queues:目标端 强制为1
                    仅 scsi vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷 queues：目标端端 为1
                    无 scsi 卷但含未卸载的 virtio-scsi 控制器 vm - 目标端热添加 8scsi 卷 -  检查已有和新增 virtio-scsi 控制器 queues强制为1
                    含 virtio、scsi ide vm - 目标端热添加 virtio、7scsi 卷- 检查新增 virtio 卷、virtio-scsi 控制器 queues 强制为1
                    源端热添加 vcpu 数 - 目标端热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：1
                    目标端热添加 vcpu 数、热添加 virtio、7scsi 卷- 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：1
                    目标端热添加 vcpu 数和 virtio、7scsi 卷- 关机重新开机 - 检查已有和新增 virtio 卷、virtio-scsi 控制器 queues：目标端 为1
            ELF-7648 新增 metric  支持 elf_vm_basic_os_info
                访问 http://172.20.147.117:10405/api/v2/exporter/elf/vm 会返回主机上开机虚拟机的 elf_vm_basic_os_info 信息
            515 支持 vmtools 执行命令行
                ELF 事件审计
                    执行成功的记录
                    执行失败的记录【事件里正常记录触发的命令行，不包含执行返回信息】
                集群级别设置
                    开启 【vmtools 执行命令行】功能
                    关闭 【vmtools 执行命令行】功能
                    集群默认配置为关闭
                    集群关闭功能，对虚拟机只命令行失败，SVT_CLUSTER_CAPABILITY_DISABLED
                    集群开启功能，对虚拟机执行命令行成功
                API 文档
                    预期 api 文档中不包含  【vmtools 执行命令行】支持范围的 api 描述
            ELF-7719虚拟卷限速失效
                限速配置检查
                    vhost 含 virtio、scsi、ide 的开机虚拟机 - 编辑vm 配置虚拟卷限速 - 所有卷带宽、iops  设置为动态限速 - 检查 zbs 限速配置正确
                    vhost 含 virtio、scsi、ide 的开机虚拟机 - 编辑vm 配置虚拟卷限速 - 所有卷 iops  动态、带宽强制限速 - 检查 zbs 限速配置正确
                    vhost 含 virtio、scsi、ide 的开机虚拟机 - 编辑vm 配置虚拟卷限速 - 所有卷带宽 动态、 iops 强制限速 - 检查 zbs 限速配置正确
                    vhost 含 virtio、scsi、ide 的开机虚拟机 - 编辑vm 配置虚拟卷限速 - 所有卷带宽、 iops 强制限速 - 检查 zbs 限速配置正确
                场景测试检查
                    iops 动态限速大于 233
                        vhsot 开机虚拟机后，配置 ide 卷：iops动态限速 > 233，iops 留空 - fio 检查带宽动态 bust限速符合预期
                    Iops 动态限速小于 233 bytes
                        vhsot 开机虚拟机后，配置 virtio 卷：iops动态限速 < 233，iops 留空 - fio 检查带宽动态 bust限速符合预期
                        vhsot 开机虚拟机后，配置 scsi 卷：iops动态限速 = 233，iops 留空 - fio 检查带宽动态 bust限速符合预期
                    带宽动态限速
                        vhsot 开机虚拟机后，配置virtio\scsi\ide卷 带宽动态限速，iops 留空 - fio 检查带宽动态 bust限速符合预期
        515-p1
            ELF-7935 修复 elf exporter pg metric 缓存问题
                复现：515 集群创建虚拟机 A（host1）、B（host2） - 配置虚拟机组：要求 vm A、B 在不同主机上 - 操作虚拟机A 迁移到主机host2上，触发放置组报错 - 将 vm B 迁移到 host1  - 报警不消失问题复现
                515 临时解决方案验证：在复现问题的 515 集群上重启 所有节点 elf-exporter 服务，重新采集信息 - 错误的放置组报警消失
                升级（515-p1 或 630）：预期升级前触发的报警 - 升级 ；会重启 elf-exporter 修复问题，无法判断为是515-p1 修复 ELF-7935  - 检查升级报警消失即可
                升级后 - 集群创建虚拟机 A（host1）、B（host2） - 配置虚拟机组：要求 vm A、B 在不同主机上 - 操作虚拟机A 迁移到主机host2上 - 能正常触发放置组报警
                升级后 - 集群创建虚拟机 A（host1）、B（host2） - 配置虚拟机组：要求 vm A、B 在不同主机上 - 操作虚拟机A 迁移到主机host2上，触发放置组报警 - 将 vm B 迁移到 host1  - 报警消失
        6.2.0-hp2
            【ELF-7654】不允许 vCPU 数量小于等于 4 的 windows VM 执行 CPU 热扩容
                windows 虚拟机
                    关机虚拟机
                        编辑 vcpu 2 到 5 ，5 到 6 编辑成功
                    开机虚拟机
                        guest_os_type 配置为 windows 的虚拟
                            vcpu <= 4
                                vcpu 1 * 1  修改为 1 * 4 失败， ELF API 返回 VM_CPU_HOTPLUG_ON_WINDOWS_CHK_FAILED
                                vcpu 1 * 4 修改为 1 * 5 失败
                            vcpu > 4
                                vcpu 2 * 3  修改为 2* 4 成功
                        开启 windwos 优化的虚拟机
                            vcpu <= 4
                                vcpu 1 * 1  修改为 1 * 4 失败， ELF API 返回 VM_CPU_HOTPLUG_ON_WINDOWS_CHK_FAILED
                                vcpu 1 * 4 修改为 1 * 5 失败
                            vcpu > 4
                                vcpu 2 * 3  修改为 2* 4 成功
                        guest_os_type != windows 且 未开启 windwos 优化
                            虚拟机安装 VMTools 且采集系统是 windwos
                                vcpu <= 4
                                    vcpu 1 * 1  修改为 1 * 4 失败， ELF API 返回 VM_CPU_HOTPLUG_ON_WINDOWS_CHK_FAILED
                                    vcpu 1 * 4 修改为 1 * 5 失败
                                vcpu > 4
                                    vcpu 2 * 3  修改为 2* 4 成功
                            虚拟机安装 VMTools 且采集系统不是 windwos
                                编辑 vcpu 2 到 5 ，5 到 6 编辑成功
                            虚拟机未安装 VMTools
                                编辑 vcpu 2 到 5 ，5 到 6 编辑成功
                Linux 虚拟机
                    编辑 vcpu 2 到 5 ，5 到 6 编辑成功
                UI 文案翻译
                    Tower 442/461 翻译 VM_CPU_HOTPLUG_ON_WINDOWS_CHK_FAILED
        发布前关联产品测试
            VMTools 适配测试
                集群上传 VMTools ISO 成功
                虚拟机安装 VMTools 成功
                虚拟机升级 VMTools 成功
                虚拟机卸载并弹出 VMTools 成功
                vmtools 数据采集正确
                vmtools 设置静态IPv4和 ipv6成功
                vmtools 修改dns 成功
            V2V 适配测试
                虚拟机从 VMware 迁移到 SMTXOS ( ELF )  成功
                虚拟机从 VMware 迁移到 SMTX ELF  成功
                虚拟机从  SMTXOS 迁移到 ACOS 成功
                迁移时设置静态IP，迁移成功，目标端虚拟机安装了vmtools 且网卡为静态IP
                不设置静态IP，迁移成功，目标端虚拟机没有安装vmtools且网卡是dhcp
            Cloud-init 适配测试
                linux 虚拟机 安装、卸载、再次安装 cloud-init 成功
                linux 虚拟机安装 cloud-init 后克隆为 cloud-init 模版 成功
                windows 虚拟机 安装、卸载、再次安装 cloud-init 成功
                windows 虚拟机安装部署 cloud-init 后克隆为 cloud-init 模版 成功
                cloud-init 模版创建单个虚拟机 ，配置所有初始化参数，虚拟机开机成功，初始化设置生效
                cloud-init 模版批量创建虚拟机 ，配置所有初始化参数，虚拟机开机成功，初始化设置生效
                cloud-init 虚拟机开机后禁用 cloud-init 成功
                清理 cloud-init 数据 成功
            DRS 适配测试
                DRS 开启成功
                DRS 迁移建议生成 - 成功
            ISO 加载测试
                SMTXOS ( ELF )  intel
                    记录 windows 10 iso  安装耗时，1、开机到加载出安装选项的耗时，2、开机搭配安装完成的耗时
                    记录 windows server 2022 iso  安装耗时，1、开机到加载出安装选项的耗时，2、开机搭配安装完成的耗时
                    记录 rhel 9 iso  安装耗时，1、开机到加载出安装选项的耗时，2、开机搭配安装完成的耗时
                SMTXOS ( VMware )  intel
                    记录 windows 10 iso  安装耗时，1、开机到加载出安装选项的耗时，2、开机搭配安装完成的耗时
                    记录 windows server 2022 iso  安装耗时，1、开机到加载出安装选项的耗时，2、开机搭配安装完成的耗时
                    记录 rhel 9 iso  安装耗时，1、开机到加载出安装选项的耗时，2、开机搭配安装完成的耗时
            跨集群迁移测试
                跨集群热迁移
                    迁移到同版本
                    迁移到高版本
                跨集群分段迁移
                    迁移到同版本
                    迁移到 6.3.x
                    迁移到 6.2.x
                    迁移到 6.1.x
                    迁移到 6.0.x
                    迁移到 5.1.x
                    迁移到 5.0.x
                跨集群冷迁移
                    迁移到同版本
                    迁移到 6.3.x
                    迁移到 6.2.x
                    迁移到 6.1.x
                    迁移到 6.0.x
                    迁移到 5.1.x
                    迁移到 5.0.x
        620-p4
            ELF-7872 为 ELF 虚拟卷配置默认 initiator IQN 访问
                620-p4新建集群检查
                    Boost 环境
                        创建虚拟卷 - iSCSI IQN 为 Allowlist 为空、SingleAccess为true
                        创建共享卷 - iSCSI IQN 为 Allowlist 为空、SingleAccess为false
                        挂载到关机普通虚拟机的 virtio、scsi、ide 虚拟卷 - iSCSI IQN 为 Allowlist 为空、SingleAccess为true
                        挂载到关机 vm 的 virtio、scsi、ide 共享虚拟卷 - iSCSI IQN 为 Allowlist 为空、SingleAccess为false
                        挂载到开机 vm 的 virtio、scsi、ide 普通虚拟卷 - iSCSI IQN 的 virtio/scsi 为 Allowlist 为空、SingleAccess为 true，ide 使用虚拟机白名单
                        挂载到开机 vm 的 virtio、scsi、ide 共享虚拟卷 - iSCSI IQN 的 virtio/scsi 为 Allowlist 为空、SingleAccess 为 false，ide 使用虚拟机白名单
                    非 boost 环境（仅回归）
                        创建虚拟卷 - iSCSI IQN 为 Allowlist 为空、SingleAccess为false
                        创建共享卷 - iSCSI IQN 为 Allowlist 为空、SingleAccess为false
                        挂载到关机普通虚拟机的 virtio、scsi、ide 虚拟卷 - iSCSI IQN 为 Allowlist 为空、SingleAccess为 false
                        挂载到关机 vm 的 virtio、scsi、ide 共享虚拟卷  - iSCSI IQN 为 Allowlist 为空、SingleAccess为false
                        挂载到关机 vm 的 virtio、scsi、ide 虚拟卷 - iSCSI IQN virtio、scsi、ide 使用虚拟机白名单
                        挂载到开机 vm 的 virtio、scsi、ide 普通虚拟卷  - iSCSI IQN 的 virtio、scsi、ide 使用虚拟机白名单
                        挂载到开机 vm 的 virtio、scsi、ide 共享虚拟卷  - iSCSI IQN 的 virtio、scsi、ide 使用虚拟机白名单
                    跨集群迁移
                        620-p4 集群热迁移到 630 - 迁移成功 - iSCSI IQN 的 virtio/scsi 为 Allowlist 为空、SingleAccess为 true，(含 ide 卷禁止迁移)，虚拟机卷 io 正常不中断
                        620-p4 集群间热迁移 - 迁移成功 - iSCSI IQN 的 virtio/scsi 为 Allowlist 为空、SingleAccess为 true，(含 ide 卷禁止迁移)，虚拟机卷 io 正常不中断
                        620-p4 集群热迁移到低版本集群 - 禁止迁移
                        515 跨集群迁移到 620-p4 - iSCSI iqn：virtio/scsi/ide 卷为空SingleAccess为 true，ide 使用虚拟机白名单,虚拟机卷 io 正常不中断
                        610 跨集群迁移到 620-p4 - iSCSI iqn:virtio/scsi 卷为空，ide 卷白名单为当前虚拟机，虚拟机卷 io 正常不中断
                集群升级
                    4010 升级到 620-p4（iscsi 集群）
                        已有未挂载共享卷/普通卷 - 升级后 iSCSI IQN 为 普通卷Allowlist  为*/*、SingleAccess为true，共享卷 Allowlist  为*/*、SingleAccess为False
                        已有挂载关机vm的 共享/普通卷 - 升级后 virtio、scsi、ide 卷 iSCSI IQN  普通卷Allowlist  为*/*、SingleAccess为true，共享卷 Allowlist  为*/*、SingleAccess为False
                        已有挂载开机vm的 共享/普通卷 - 升级后 virtio、scsi、ide 卷 iSCSI IQN 为 Allowlist  为 */*、SingleAccess为false，虚拟机卷 io 正常不中断
                    610 集群升级至620-p4（vhost）
                        已有未挂载共享卷/普通卷 - 升级后iSCSI IQN 普通卷 为 Allowlist  为空、SingleAccess为true，共享卷 Allowlist 为*/*、SingleAccess为False
                        已有挂载关机vm的 共享/普通卷 - 升级后 virtio、scsi、ide 卷 iSCSI IQN 普通卷 为 Allowlist  为空、SingleAccess为true，共享卷 Allowlist 为*/*、SingleAccess为False
                        已有挂载开机vm的 共享/普通卷 - 升级后 virtio、scsi 卷 iSCSI IQN 普通卷为 Allowlist  为空、SingleAccess为false，ide 卷配置白名单，共享virtio/scsi/ide 卷 Allowlist 为*/*、SingleAccess为False ，虚拟机卷 io 正常不中断
                    620-p3 升级到 620-p4(vhost)
                        已有未挂载共享卷/普通卷 - 升级后iSCSI IQN 为 Allowlist  为空、SingleAccess为true
                        已有挂载关机vm的 共享/普通卷 - 升级后 virtio、scsi、ide 卷 iSCSI IQN 为 Allowlist  为空、SingleAccess为false
                        已有挂载开机vm的 共享/普通卷 - 升级后 virtio、scsi 卷 iSCSI IQN 为 Allowlist  为空、SingleAccess为false，ide 卷配置白名单，，虚拟机卷 io 正常不中断
                    升级检查
                        检查升级时执行 数据变更elf post_update ，在 /var/log/zbs/cluster_upgrade.log 日志有记录
                        可手动执行 - 预期执行后 调整存量普通虚拟卷白名单 Allowlist 为空、SingleAccess 为 false
                        检查集群升级过程中 fio 不中断
                    非 vhost 集群
                        保持未挂载/关机虚拟机上的virtio scsi ide 卷白名单为*/*
                        已有挂载开机虚拟机 共享/普通卷 - 升级后 virtio、scsi 卷 iSCSI IQN 为 Allowlist 为空、SingleAccess为True，ide 卷配置白名单，虚拟机卷 io 正常不中断
            ELF-7961 HA 重建故障后， 增加虚拟机其他功能操作
                HA 重建故障后（如存储网络故障）， 虚拟机手动迁移到其他主机， 检查虚拟机不会触发 HA 重建任务
        6.3.0
            ELF-7636 OVF 导入建议默认使用 SCSI 总线（前提是ovf文件里没有指定总线时）
                SMTXOS 导出导入 SMTXOS
                    导入虚拟机
                        SMTXOS 导出（虚拟机包含所有磁盘总线） OVF 再导入 SMTXOS虚拟机， UI 展示导入的磁盘总线和源虚拟机一致
                    导入虚拟机模版
                        SMTXOS 导出虚拟机模版（虚拟机包含所有磁盘总线） OVF 再导入 SMTXOS 虚拟机模版，UI 展示导入的磁盘总线和源虚拟机一致
                VMware 导出导入 SMTXOS 6.3.0
                    导入虚拟机
                        VMware 虚拟机配置 SCSI 总线磁盘，VMware 导出再导入 SMTXOS 时磁盘总线识别为 SCSI（已知问题 ELF-8109 VMware的VirtualSCSI，smtx 识别为 virtio）
                        VMware 虚拟机配置 ide 总线磁盘，VMware 导出再导入 SMTXOS 时磁盘总线识别为 ide
                        VMware 虚拟机配置其他总线磁盘（SATA、NVME），VMware 导出再导入 SMTXOS 时磁盘总线识别为 SCSI
                        VMware 虚拟机磁盘混合着整数磁盘和小数磁盘，导出后导如smtxos，磁盘大小识别准确
                        VMware 虚拟机磁盘含有 4种不同控制器，导出后导入
                    导入内容库虚拟机模版
                        VMware 虚拟机配置 SCSI 总线磁盘，VMware 导出再导入 SMTXOS，，模版里磁盘总线识别为 SCSI（已知问题 ELF-8109 VMware的VirtualSCSI，smtx 识别为 virtio）
                        VMware 虚拟机配置 ide 总线磁盘，VMware 导出再导入 SMTXOS，模版里磁盘总线识别为 ide
                        VMware 虚拟机配置其他总线磁盘（SATA、NVME），VMware 导出再导入 SMTXOS，模版里磁盘总线识别为 SCSI
                        VMware 虚拟机磁盘混合着整数磁盘和小数磁盘，导出后导如smtxos，模版里磁盘大小识别准确
                        VMware 虚拟机磁盘含有 4种不同控制器，导出后导入
                VMware 导出导入 SMTX-ELF 6.3.0
                    导入虚拟机
                        修复版本，如 SMTXELF 6.3.0
                            VMware 虚拟机配置 SCSI 总线磁盘，VMware 导出再导入 SMTXELF 时磁盘总线识别为 SCSI（已知问题 ELF-8109 VMware的VirtualSCSI，smtx 识别为 virtio）
                            VMware 虚拟机配置 ide 总线磁盘，VMware 导出再导入 SMTXELF 时磁盘总线识别为 ide
                            VMware 虚拟机配置其他总线磁盘（SATA、NVME），VMware 导出再导入 SMTXELF 时磁盘总线识别为 SCSI
                            VMware 虚拟机磁盘含有 4种不同控制器，导出后导入
                    导入内容库虚拟机模版
                        未修复版本，如 SMTXZBS-5.7.0, SMTXOS 6.2.0-
                            VMware 虚拟机配置 ide 总线磁盘，VMware 导出再导入【关联存储集群】时磁盘总线识别为 ide
                            VMware 虚拟机配置其他总线磁盘（SCSI、SATA、NVME），VMware 导出再导入【关联存储集群】时磁盘总线识别为 VIRTIO
                            VMware 虚拟机磁盘含有 4种不同控制器，导出后导入
                        修复版本，如 SMTXEXL 6.3.0
                            VMware 虚拟机配置 ide 总线磁盘，VMware 导出再导入【关联存储集群】时磁盘总线识别为 ide
                            VMware 虚拟机配置其他总线磁盘（SCSI、SATA、NVME），VMware 导出再导入【关联存储集群】时磁盘总线识别为 SCSI（已知问题 ELF-8109 VMware的VirtualSCSI，smtx 识别为 virtio）
                            VMware 虚拟机磁盘含有 4种不同控制器，导出后导入
                GuestOS 覆盖检查
                    windows 虚拟机（如 windows 10）
                    Linux 虚拟机（如 centos 8.5 ）
                    信创 os （如 Kylin v10 server ）
            ELF-7465 增强 OVF 导入对 OVF 格式的兼容性
                从 vmware 导出，再导入 smtxos
                    ovf 里虚拟机名称前后有空格，导入成功，空格被过滤掉
                    ovf 里虚拟机名称中间有1个空格，导入成功，替换为下划线
                    ovf 里虚拟机名称中间有多个连续空格，导入成功
                    ovf 里磁盘名称前后有空格，导入成功，空格被过滤掉
                    ovf 里磁盘名称中间有1个空格，导入成功
                    ovf 里磁盘名称中间有多个空格，导入成功
                    ovf 里某个磁盘item没有 InstanceID，导入成功，跳过此 item
                    ovf 里所有磁盘的item都没有 InstanceID，导入成功，跳过此 item
                    ovf 里某个conroller的item 没有InstanceID，解析失败
                    ovf 里 cpu、内存的前后有空格，导入成功，空格被过滤掉
                    ovf 里 AllocationUnits 为 Mebibyte(MiB) 时，导入成功
                    ovf 里 AllocationUnits 为 MegaBytes（MB） 时，导入成功
                    ovf 里 AllocationUnits 为 Kilobyte时，导入成功
                    ovf 里 AllocationUnits 为 Gigabyte时，导入成功
                    ovf 里磁盘有小数时，导入
                    ovf 里 AllocationUnits 为 Byte 时，导入成功
            ELF-7306 ELF API 删除资源支持 EnableDeletePermanently
                SMTXOS 6.3.0, 默认开启 ZBS 回收站
                    ISO
                        Tower 删除 ISO，直接删除不进入 ZBS 回收站
                        ISO 上传失败（如 非 ISO 格式），检查上传 ISO 过程中的 lun 删除不会进入回收站
                    虚拟机
                        Tower 删除虚拟机
                            Tower 直接删除虚拟机，删除成功
                            Tower 回收站删除虚拟机，删除成功
                        ELF API 删除单个虚拟机
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟机 lun 进入 ZBS 回收站
                        ELF API 批量删除虚拟机
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟机 lun 进入 ZBS 回收站
                    删除虚拟机模版
                        Tower 删除内容库模版
                            Tower 删除内容库虚拟机模版，删除成功
                        ELF API 删除虚拟机模版
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟机模版 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟机模版 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟机模版 lun 进入 ZBS 回收站
                    删除虚拟卷
                        Tower 删除虚拟卷
                            Tower 删除虚拟卷，删除成功
                        ELF API 删除虚拟卷
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟卷 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟卷 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟卷 lun 进入 ZBS 回收站
                SMTXOS 6.3.0, 设置关闭 ZBS 回收站
                    删除 ISO
                        删除 ISO 成功
                    删除虚拟机
                        Tower 删除虚拟机
                            Tower 直接删除虚拟机，删除成功
                            Tower 回收站删除虚拟机，删除成功
                        ELF API 删除单个虚拟机
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                        ELF API 批量删除虚拟机
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                    删除虚拟机模版
                        Tower 删除内容库模版
                            Tower 删除内容库虚拟机模版，删除成功
                        ELF API 删除虚拟机模版
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟机模版 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟机模版 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟机模版 lun 不进入 ZBS 回收站
                    删除虚拟卷
                        Tower 删除虚拟卷
                            Tower 删除虚拟卷，删除成功
                        ELF API 删除虚拟卷
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟卷 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟卷 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟卷 lun 不进入 ZBS 回收站
                SMTXELF 6.3.0 + 开启 ZBS 回收站的存储集群
                    删除 VMTool ISO
                        删除 VMTool ISO， 直接删除不进入 ZBS 回收站
                    ISO
                        Tower 删除 ISO，直接删除不进入 ZBS 回收站
                        ISO 上传失败（如 非 ISO 格式），检查上传 ISO 过程中的 lun 删除不会进入回收站
                    虚拟机
                        Tower 删除虚拟机
                            Tower 直接删除虚拟机，删除成功
                            Tower 回收站删除虚拟机，删除成功
                        ELF API 删除单个虚拟机
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟机 lun 进入 ZBS 回收站
                        ELF API 批量删除虚拟机
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟机 lun 进入 ZBS 回收站
                    删除虚拟机模版
                        Tower 删除内容库模版
                            Tower 删除内容库虚拟机模版，删除成功
                        ELF API 删除虚拟机模版
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟机模版 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟机模版 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟机模版 lun 进入 ZBS 回收站
                    删除虚拟卷
                        Tower 删除虚拟卷
                            Tower 删除虚拟卷，删除成功
                        ELF API 删除虚拟卷
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟卷 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟卷 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟卷 lun 进入 ZBS 回收站
                SMTXELF 6.3.0 + 不支持 ZBS 回收站的存储集群
                    删除 VMTool ISO
                        删除 VMTool ISO， 直接删除不进入 ZBS 回收站
                    删除 ISO
                        删除 ISO 成功
                    删除虚拟机
                        Tower 删除虚拟机
                            Tower 直接删除虚拟机，删除成功
                            Tower 回收站删除虚拟机，删除成功
                        ELF API 删除单个虚拟机
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                        ELF API 批量删除虚拟机
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟机 lun 不进入 ZBS 回收站
                    删除虚拟机模版
                        Tower 删除内容库模版
                            Tower 删除内容库虚拟机模版，删除成功
                        ELF API 删除虚拟机模版
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟机模版 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟机模版 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟机模版 lun 不进入 ZBS 回收站
                    删除虚拟卷
                        Tower 删除虚拟卷
                            Tower 删除虚拟卷，删除成功
                        ELF API 删除虚拟卷
                            ELF API 不传入 delete_permanently， 删除成功， 虚拟卷 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = True， 删除成功， 虚拟卷 lun 不进入 ZBS 回收站
                            ELF API 传入 delete_permanently = False， 删除成功， 虚拟卷 lun 不进入 ZBS 回收站
                API 检查
                    DELETE /api/v2/volumes/<volume_uuid>  - 新增参数 {"delete_permanently": {"type": "boolean"}}
                    DELETE /api/v2/vms/<vm_uuid> 新增参数 {"delete_volume_permanently": {"type": "boolean"}}
                    DELETE /api/v2/vm_templates/<vm_template_uuid> {"delete_volume_permanently": {"type": "boolean"}}
                    DELETE /api/v2/batch/vms 新增参数 {"delete_volume_permanently": {"type": "boolean"}}
            ELF-7482 elf API+tower UI支持虚拟卷完全克隆限速
                ELF API
                    新增 api
                        获取集群完全克隆限速配置情况 - GET /api/v2/elf/cluster_copy_volume_capabilities - smtx os（ELF）/smtx elf 630 获取成功
                        设置集群完全克隆限速 - PUT /api/v2/elf/cluster_copy_volume_capabilities -  smtx os（ELF）630 配置开启限速，配置合法total_tasks_max_bps（全局限速）、task_max_bps（单个任务限速） 成功
                    api 配置检查
                        集群配置设置集群完全克隆限速 - PUT /api/v2/elf/cluster_copy_volume_capabilities -  smtx os（ELF）630 配置开启限速 失败：SET_COPY_VOLUME_CAPABILITIES_FAILED 设置完全克隆限速配置失败，message 展示失败详情
                        API 检查配置：第一次操作集群 - 开启限速，不输入限速值 - 预期配置成功，api 响应和cmd、数据库检查集群：限速开启使用默认限速值
                        API 检查配置：默认限速的集群 - 开启限速，total_tasks_max_bps 指定值 - 预期配置成功，api 响应和cmd检查集群：限速开启，total_tasks_max_bps使用指定值，task_max_bps 使用默认限速值
                        API 检查配置：已配置限速的集群 - 开启限速，task_max_bps 指定制 - 预期配置成功，api 响应和cmd、数据库检查集群：限速开启，task_max_bps 使用指定值，total_tasks_max_bps 使用之前的限速值
                        配置过限速但关闭限速的集群，API 检查配置：开启限速，输入total_tasks_max_bps、task_max_bps 限速值 - 预期配置成功，api 响应和cmd、数据库检查集群：限速开启，限速使用指定值
                        已开启限速的集群 ，API 检查配置：关闭限速 - 预期配置成功，api 响应和cmd、数据库检查集群：限速关闭，限速使用上次配置的速率值
                        已开启限速集群，API 检查配置：开启限速，输入total_tasks_max_bps、task_max_bps 减小限速值 - 预期配置成功，api 响应和cmd、数据库检查集群：限速开启，限速使用指定值
                        已开启限速集群，API 检查配置：开启限速，输入total_tasks_max_bps、task_max_bps 增大限速值 - 预期配置成功，api 响应和cmd、数据库检查集群：限速开启，限速使用指定值
                        已开启限速集群，API 检查配置：关闭限速，输入total_tasks_max_bps 限速值 - 预期配置成功，api 响应和cmd、数据库检查集群：限速关闭，限速使用指定值
                        未开启限速集群，API 检查配置：开启限速，只输入total_tasks_max_bps 限速值 - 预期配置成功，api 响应和cmd、数据库检查集群：限速开启，限速使用指定值
                        已开启限速集群，API 检查配置：关闭限速，只输入task_max_bps 限速值 - 预期配置成功，api 响应和cmd、数据库检查集群：限速关闭，限速使用指定值
                        未开启限速集群，API 检查配置：开启限速，输入 task_max_bps 限速值 - 预期配置成功，api 响应和cmd、数据库检查集群：限速开启，限速使用指定值
                        api 配置限速时 ，total_tasks_max_bps < task_max_bps，配置失败，报错：SET_COPY_VOLUME_CAPABILITIES_FAILED 设置完全克隆限速配置失败，message 展示失败详情
                        api 配置限速时 ，total_tasks_max_bps = task_max_bps，配置成功
                        api 配置限速时 ，total_tasks_max_bps > task_max_bps，配置成功
                        api 配置限速时 ，total_tasks_max_bps =0，配置失败，报错：REST_FORM_ERROR，message 展示 详情 0 is less than the minimum of 1
                        api 配置限速时 ，task_max_bps =0，配置失败，报错：REST_FORM_ERROR，message 展示 详情 0 is less than the minimum of 1
                    有效性检查
                        从模版创建完全克隆 -  含1个虚拟卷的虚拟机 - 检查虚拟卷初始速率 90MB/s(754974720 bps)，60s 定时任务后使用最大速率 200MB/s(209715200 bps)
                        快照重建完全克隆 -  含2个大小不同卷的虚拟机 - 检查虚拟卷初始速率 90MB/s(754974720 bps)，60s 定时任务后，使用最大速率 200MB/s(209715200 bps)
                        克隆创建完全克隆 -  3个不同大小卷的5个虚拟机 - 检查虚拟卷初始速率 90MB/s(754974720 bps)，有1个 vm 创建完成，60s 定时任务后，使用最大速率 80MB/s(83886080 bps)
                tower 功能测试
                    UI
                        UI 检查 完全克隆有调整带宽的相关提示语，中英文正确
                        集群 - 设置 - 虚拟化：完全克隆选项 - 操作配置限速开关和限速带宽大小
                        smtx os（ELF） 6.3.0+ 集群 - 有完全克隆选项 - 默认关闭
                        smtx elf 6.3.0 集群 - 没有完全克隆选项
                        开启【完全克隆限速】 - 展示 最大带宽输入框：默认为900，单位 MiB/S，同步到默认 tower 数据库的值
                        未开启【完全克隆限速】 -  数据库保持默认设置：限速未开启，全局最大速率 900MB/s，单个任务最大速率默认300M
                        开启 【完全克隆限速】 - 配置最大带宽 1000 MiB/s (tower server 传入单个任务速率 = 最大速率 - 1=999 MiB/s) -  配置成功数据库配置正确
                        关闭【完全克隆限速】 - 修改限速为空/0/其它值后，关闭限速 - 关闭限速成功，后端限速关闭，total_tasks_max_bps、task_max_bps 大小与上一次生效时的大小一致不变
                        开启【完全克隆限速】 - 展示 最大带宽输入框，只能输入阿拉伯数字，其他字符无法输入
                        开启【完全克隆限速】 - 展示 最大带宽输入框：为空 - 保存，校验提示：请填写最大带宽
                        开启【完全克隆限速】 - 展示 最大带宽输入框：为 0 - 保存，校验提示：禁止支持大于0的整数
                        开启【完全克隆限速】 - 展示 最大带宽输入框：字符长度 不限制 TOWER-20142
                        开启 【完全克隆限速】集群调整增大限速 - 配置成功数据库为：开启限速 ，限速为指定值（task_max_bps=total_tasks_max_bps - 1）
                        开启 【完全克隆限速】集群调整减小限速 - 配置成功数据库为：开启限速 ，限速为指定值（task_max_bps=total_tasks_max_bps - 1）
                    集群升级
                        未配置限速的集群 - 升级到 630 - 完全克隆限速保持关闭，保持之前默认设置：tower grapql：关闭 全局限速900MiB ,后端配置:关闭，集群最大速率 900MB/S，单个任务最大速率 300MB/S
                        后续515 已在命令行配置过限速的集群，升级到 630 集群，限速配置与 515 集群一致 - tower 会同步到限速数据
                    数据同步
                        elf API 设置的速率后 - tower 同步周期结束后，会同步到 tower UI  同步周期时间（无快速同步，默认同步 1h）
                        elf cmd 设置的速率后 - tower 同步周期结束后，会同步到 tower UI  同步周期时间（无快速同步，默认同步 1h）
                    graphql 检查
                        graphql 接口：updateCluster mutation
                        graphql 触发 smtx elf  开启限速，配置失败，error code：SET_COPY_VOLUME_CAPABILITIES_FAILED，检查文案正确： 设置完全克隆限速配置失败，error message 展示失败详情
                        graphql 触发 total_tasks_max_bps < task_max_bps，配置失败，error code：SET_COPY_VOLUME_CAPABILITIES_FAILED，检查文案正确： 设置完全克隆限速配置失败，error message 展示失败详情
                        graphql 配置限速时 ，total_tasks_max_bps =0，配置失败，报错message 展示失败详情 ，不会触发任务不在UI 展示报错文案
                        graphql 配置限速时 ，tasks_max_bps =0，配置失败，报错message 展示失败详情 ，不会触发任务不在UI 展示报错文案
                        graphql 配置限速时 ，total_tasks_max_bps 、tasks_max_bps 都是非必填项，可以省略，但不能单个配置 tasks_max_bps
                        graphql 配置限速时 ，配置 限速开启 + total_tasks_max_bps 配置成功 - 数据库检查集群：限速开启，限速使用指定值 （tasks_max_bps=total_task_max_bps - 1)
                        graphql 配置限速时 ，配置 限速开启 + tasks_max_bps - 不支持单独配置单个任务限速
                        graphql 关闭限速时，支持配置 total_tasks_max_bps、task_max_bps ？
                        已开启限速的集群，graphql  操作关闭限速 ，是否清空  total_tasks_max_bps、task_max_bps 还是保留原值
                        未开启限速的集群，graphql  操作开启限速 ，配置  total_tasks_max_bps、task_max_bps  成功 - 后端 数据库检查集群：限速开启，限速使用指定值
                    有效性检查
                        从模版创建完全克隆 -  含1个虚拟卷的虚拟机 - 检查虚拟卷初始速率 90MB/s(754974720 bps)，60s 定时任务后使用最大速率 999MB/s(8380219392 bps)
                        快照重建完全克隆 -  含2个大小不同卷的虚拟机 - 检查虚拟卷初始速率 90MB/s(754974720 bps)，60s 定时任务后，使用最大速率 499 MB/s(209715200 bps)
                        克隆创建完全克隆 -  3个不同大小卷的5个虚拟机 - 检查虚拟卷初始速率 90MB/s(754974720 bps)，有1个 vm 创建完成，60s 定时任务后，使用最大速率 80MB/s(83886080 bps)
                    场景测试
                        卷类型覆盖
                            创建 3个含 2nfs 卷的虚拟机 完全克隆 - 检查 初始速率是 90MiB/s(754974720 bps)，60s 后同步速率是 200MiB/S (209715200 bps)
                            创建 3个含 1scsi+2nfs 卷的虚拟机 完全克隆 - 检查 初始速率是 90MiB/s(754974720 bps)，定时任务 60s 后同步速率是 133MiB/S (139810133 bps)，3个小容量 nfs 任务结束，定时任务同步速率是：200MiB/S(209715200 bps)
                            创建 3个含 1ec +1副本 卷的虚拟机 完全克隆 - 检查 初始速率是 90MiB/s(754974720Mbps)，60s 后同步速率是 200MiB/S (209715200)
                        速率随当前卷数量变化
                            完全克隆创建1个虚拟机1个卷 - 检查初始速率是 90MiB/s(754974720 bps)，60s 后同步速率是 1199MiB/S (2516582400)，一直到任务结束
                            完全克隆创建容量大小不同的6卷 - 初始速率 90MiB/S - 检查限速是根据当前卷数量计算：定时任务60s 调整时，剩余5个卷，限速 240MiB/S，120s时，剩余2个卷 600MiB/S
                            发起 20个单个虚拟卷的定时任务 - 初始速率90 MiB/s，间隔 60s 定时任务更新后速率为 60MB/S
                            分批次发起任务，如：发起 5 个完全克隆任务，1分钟后再次发起 15 个完全克隆任务 - 在周期任务调整下第一组卷每个任务的速率变化为 90 -> 240 -> 60，第二组15个卷速率90 ->60
                        限速效果检查
                            监控视图检查 - 发起5个完全克隆任务，观察集群 IO 带宽 - 克隆任务带来的 IO 带宽增加与 total_tasks_max_bps 限制接近
                            减少全局速率为(1200-->800MB/s) - 完全克隆创建1个虚拟机5个卷 - 检查 初始速率是 90MiB/s(754974720 bps)，60s 后同步速率是 160MiB/s ，有3个虚拟卷创建结束 - 第二个60s 同步速率：单个任务最大限速生效 400MiB/s
                            增大全局速率由 (800->1000MB/s) - 完全克隆创建1个虚拟机3个卷 - 检查 初始速率是 90MB/s(754974720Mbps)，60s 后同步速率是 333.33MiB/s ，有一个虚拟卷创建结束 - 第二个60s 同步速率：单个任务最大限速生效：400MiB/s
                            限速为900MB/s的集群 - 完全克隆创建3个挂载5个卷的vm  - 初始限速 90MB/s，60s 后限速 60MB/s - 调整集群增大限速为 1500MB/s - 第二个60s 时，单个任务最大速率为100MB/s
                            限速为900MB/s的集群 - 完全克隆创建3个挂载5个卷的vm  - 初始限速 90MB/s，60s 后限速 60MB/s - 调整集群减小限速为 600MB/s - 第二个60s 时，单个任务最大速率为40MB/s
                        边缘场景检查
                            检查限速为100% 存储网络时 - 进行完全克隆时，对其他业务的影响？
                            检查限速为1 MB/s时 - 进行完全克隆 40GB 卷 vm 时，完全克隆是否能正常进行？
                            构造集群存储网络压力大（跨集群迁移使用存储网络）时，全局限速大小占存储网络带宽 50% 的场景下，集群业务和完全克隆40GB 卷的 克隆时长
                tower 与 elf 限速配置交互
                    elf api 配置开启限速，total_tasks_max_bps 900 MiB/s，task_max_bps 300 MiB/s - TOWER UI 调整限速到 300MiB/s - 调整限速成功为：total_tasks_max_bps 300 MiB/s，task_max_bps 299 MiB/s
                    elf cmd 配置开启限速，total_tasks_max_bps 900 MiB/s，task_max_bps 300 MiB/s - TOWER UI 调整限速到 300MiB/s - 调整限速成功为：total_tasks_max_bps 300 MiB/s，task_max_bps 299 MiB/s
                事件记录
                    未开启限速集群：开启限速 - 用户事件记录：编辑集群设置变化，含完全克隆限速状态、最大带宽记录（ 启用时与关闭时限速不一致记录限速值变化 ）
                    已开启限速集群：调整限速大小 - 用户事件记录：编辑集群设置变化，包含最大带宽变化
                    已开启限速集群：关闭限速 - 用户事件记录：编辑集群设置变化，开启--->关闭，不展示最大带宽
                用户角色权限
                    UI 仅 SMTX OS (ELF) 630 + tower 480 有完全克隆限速入口，smtx elf 无入口
                    graphql  仅 SMTX OS (ELF) 630 + tower 480 有完全克隆限速配置成功，smtx elf 不支持配置
                    ELF API   仅 SMTX OS (ELF) 630 + tower 480 有完全克隆限速配置成功，smtx elf 不支持配置
                    ELF CMD 命令行   仅 SMTX OS (ELF) 630 + tower 480 有完全克隆限速配置成功，smtx elf  暂无校验
            ELF-7838 支持取消完全克隆（仅ELF API/CLI）
                功能测试
                    新增 API： POST /api/v2/elf/tasks/cancel 取消完全克隆 - 操作取消完全克隆任务，成功
                    Harbor 检查新增 api： POST /api/v2/elf/tasks/cancel 取消完全克隆 - 中英文文档正确
                    新增 CLI 检查支持取消动作 - elf-tool task --help  包含 cancel_tasks_by_job
                    CLI 操作取消完全克隆：elf-tool task cancel_tasks_by_job  <job-id> - 操作取消完全克隆任务，成功
                    含1个卷的虚拟机进行完全克隆 - api 取消克隆成功
                    含多个卷的虚拟机进行完全克隆 - 取消克隆成功
                    模版批量完全克隆创建 vm (走批量接口只有一个job-id) - 取消完全克隆成功，所有vm 停止创建
                    虚拟机克隆批量完全克隆创建 vm (走单个接口有多个job-id) - 取消完全克隆成功，当前job 的vm 停止创建
                    虚拟机快照重建 - 完全克隆创建 vm - 取消完全克隆成功，vm 停止创建
                场景测试
                    完全克隆任务：job 进行中task 已完成 - api 取消克隆时没有找到与 Job ID 对应的 task 正在运行时，返回错误码 ELF_TASK_NOT_FOUND。
                    完全克隆任务进行中，停止所有节点  zbs-task 服务 - 触发：取消所有 task 任务失败，返回错误码 ELF_TASK_CANCEL_FAILED 和各task 失败原因
                    完全克隆任务进行中，部分 task的创建结束，停止所有节点zbs-task 服务 - 操作取消完全克隆，取消克隆部分taskd失败 ELF_TASK_CANCEL_FAILED，返回取消失败的 task id 和原因
                    并发操作取消同一个任务 - 取消成功，相互间不会校验（下发取消后，实际的完全克隆 Job 会经过一次轮询5～10后才会真的停止，所以并发请求取消，也会返回同样的内容）
                    完全克隆 job 下的全部 task 取消失败 ELF_TASK_CANCEL_FAILED - 预期触发错误提示：fisheye_job:jcd.jErr_JOB_RSYNC_TASK_FAILED（tower文案：拷贝 Volume 任务失败。）或 fisheye_job: JOB_ZK_CONNECTION_TIMEOUT（tower文案：连接 ZooKeeper 超时）
                    完全克隆 job 下的部分 task 取消失败 ELF_TASK_CANCEL_FAILED - 预期触发错误提示：fisheye_job:jcd.jErr_JOB_RSYNC_TASK_FAILED（tower文案：拷贝 Volume 任务失败。）或 fisheye_job: JOB_ZK_CONNECTION_TIMEOUT（tower文案：连接 ZooKeeper 超时）
            ELF-7815  虚拟机 「强制重启」行为改为：强制关机 + 开机
                任务变更
                    OS630 集群触发强制重启， elf 子任务只有一个，强制重启虚拟机
                升级场景
                    存量 vm_version 为低版本的虚拟机， 强制重启后 vm_version 更新为最新版本
                已有功能回归
                    开机虚拟机添加网卡， 检查网卡添加成功，虚拟机内部可以识别到设备
                    关机虚拟机添加磁盘， 检查磁盘添加成功，开机可以识别到设备
                    虚拟机开机， 检查开机成功，子任务未发生变更
                    虚拟机关机， 检查关机成功，子任务未发生变更
                含直通设备做强制重启
                    含直通设备（如 SR-IOV 网卡）的虚拟机做强制重启， 检查重启成功
                    含直通设备（如 GPU ）的虚拟机做强制重启，检查重启成功
                    含相同 PCI 直通网卡的虚拟机， 1 个虚拟机做强制重启 和 1 个虚拟机做开机， 同时触发检查强制重启成功，开机失败（预期调度失败）
            ELF-7332  跨集群冷迁移/分段迁移、克隆、快照重建虚拟机支持保持 vNIC PCI Addr 不变
                迁移场景【620P4/515P1/630 + Tower 4.7.1】
                    SMTXOS 集群内迁移（冷、热）【回归】
                        含 vlan access 网卡的虚拟机集群内迁移，检查网卡 PCI 地址不变
                        含 vlan trunk  网卡的虚拟集群内迁移，检查网卡 PCI 地址不变
                        含 vpc 网卡的虚拟机集群内迁移，检查网卡 PCI 地址不变
                        含 PCI 直通网卡的虚拟机,  热迁移不支持，冷迁移会自动移除 PCI 网卡，其他网卡的内部 PCI 保持不变
                        含 SR-IOV 网卡的虚拟机,  迁移会自动移除 SR-IOV 网卡，其他网卡的内部 PCI 保持不变
                        含其他直通设备（USB）的虚拟机， 网卡  vNIC PCI 地址保持不变（不受干扰）
                    SMTXELF 集群内迁移（冷、热）
                        含 vlan access 网卡的虚拟机集群内迁移，检查网卡 PCI 地址不变
                        含 vlan trunk  网卡的虚拟集群内迁移，检查网卡 PCI 地址不变
                        含 vpc 网卡的虚拟机集群内迁移，检查网卡 PCI 地址不变
                        含 PCI 直通网卡的虚拟机, 热迁移不支持，冷迁移会自动移除 PCI 网卡，其他网卡的内部 PCI 保持不变
                        含 SR-IOV 网卡的虚拟机,  迁移会自动移除 SR-IOV 网卡，其他网卡的内部 PCI 保持不变
                        含其他直通设备（USB）的虚拟机， 网卡  vNIC PCI 地址保持不变（不受干扰）
                    跨集群迁移
                        跨集群热迁移【仅回归】
                            SMTXOS 到 SMTXOS 跨集群热迁移， 保持网卡 PCI 地址不变
                            SMTXOS 到 SMTXELF， 跨集群热迁移， 迁移计算加存储
                            SMTXELF 到 SMTXOS， 跨集群热迁移， 迁移计算加存储
                            【SMTXELF1 + 关联集群1】 到【SMTXELF2 + 关联集群2】，跨集群热迁移， 迁移计算加存储
                            【SMTXELF1 + 关联集群1】 到【SMTXELF2 + 关联集群1】，跨集群热迁移， 仅迁移计算
                            【SMTXELF1 + 关联集群1】 到【SMTXELF1 + 关联集群2】，跨集群热迁移， 仅迁移存储
                            SMTXOS 6.2.0  跨集群热迁移到 SMTXOS 6.3.0,  虚拟机内部网卡 vNIC PCI 不保持
                            SMTXELF 6.2.0-P4 跨集群热迁移到 SMTXOS 6.3.0，保持网卡 PCI 地址不变
                            含 PCI 网卡的虚拟机，SMTXOS 跨集群热迁移时会自动卸载 PCI 网卡， 其余网卡 PCI 地址保持一致
                            含 SR-IOV 网卡的虚拟机，SMTXOS 跨集群热迁移时会自动卸载 SR-IOV 网卡， 其余网卡 PCI 地址保持一致
                        跨集群分段迁移
                            SMTXOS 到 SMTXOS 跨集群分段迁移， 保持网卡 PCI 地址不变
                            SMTXOS 5.1.5-P1 跨集群分段迁移到 SMTXOS 6.2.0-P4， 保持网卡 PCI 地址不变
                            SMTXOS 5.1.5-P1 跨集群分段迁移到 SMTXOS 6.3.0，保持网卡 PCI 地址不变
                            SMTXOS 6.2.0-P4 跨集群分段迁移到 SMTXOS 6.3.0，保持网卡 PCI 地址不变
                            跨集群迁移到 5.0.x  ( 不支持  pci_address 字段的集群 )， 预期迁移成功， 不保持 pci_address 不变
                        跨集群冷迁移
                            SMTXOS 到 SMTXOS 跨集群冷迁移， 保持网卡 PCI 地址不变
                            SMTXOS 5.1.5-P1 跨集群冷迁移到 SMTXOS 6.2.0-P4， 保持网卡 PCI 地址不变
                            SMTXOS 5.1.5-P1 跨集群冷迁移到 SMTXOS 6.3.0，保持网卡 PCI 地址不变
                            SMTXOS 6.2.0-P4 跨集群冷迁移到 SMTXOS 6.3.0，保持网卡 PCI 地址不变
                            跨集群迁移到 5.0.x  ( 不支持  pci_address 字段的集群 )， 预期迁移成功， 不保持 pci_address 不变
                快照场景【515/630】
                    快照重建
                        源虚拟机含 PCI 网卡（非最后一个网卡），快照重建虚拟机时不包含 PCI 网卡，已有网卡不保证网卡 PCI 地址不变
                        源虚拟机含 SR-IOV 网卡（非最后一个网卡），快照重建虚拟机时不包含 SR-IOV 网卡，已有网卡不保证网卡 PCI 地址不变
                    快照回滚
                        虚拟机创建快照后不编辑网卡，回滚， 检查 vNIC PCI 地址和快照一致（和创建快照时虚拟机的配置一致）
                        虚拟机创建快照后，虚拟机添加一个网卡，快照回滚，检查 vNIC PCI 地址和快照一致
                克隆场景【630】
                    快速克隆
                        源虚拟机只包含普通网卡
                            克隆虚拟机时，保持原网卡配置，检查网卡 PCI 地址不变
                            克隆虚拟机时，删除一块原网卡，检查未删除的网卡 PCI 地址不变
                            克隆虚拟机时，新增网卡，检查原网卡 PCI 地址不变
                            克隆虚拟机时，删除一块原 VIRTIO 网卡，新增一块 E1000 网卡，不保证网卡 PCI 地址不变
                            克隆虚拟机时，删除一块原 E1000 网卡，新增一块 VIRTIO 网卡，不保证网卡 PCI 地址不变
                            克隆虚拟机时，网卡关联虚拟机网络修改（如管理网络 vlan 修改为存储网络 vlan），不保证网卡 PCI 地址不变
                            克隆虚拟机时，新增 SRIOV 网卡，原网卡 PCI 地址不变
                            克隆虚拟机时，新虚拟机更换全部网卡，不保证网卡 PCI 地址不变
                        源虚拟机含直通网卡
                            含 PCI 网卡，克隆时默认不带 PCI 网卡，其他网卡的 vNIC PCI 保持不变
                            含 SR-IOV 网卡，克隆时默认会带 SR-IOV网卡，预期所有网卡的 vNIC PCI 保持不变
                    完全克隆
                        克隆虚拟机时，保持原网卡配置，检查网卡 PCI 地址不变
                        克隆虚拟机时，删除一块原网卡，检查未删除的网卡 PCI 地址不变
                        克隆虚拟机时，新增网卡，检查原网卡 PCI 地址不变
                回收站【回归】
                    虚拟机移动到回收站再恢复虚拟机， 网卡 PCI 地址不变
                不保留  vNIC PCI  的场景
                    检查虚拟机克隆为模版，模版再创建新虚拟机，新虚拟机和源虚拟机的  vNIC PCI 地址不保证一致
                    导出的  OVF 配置文件不包含  vNIC PCI
                    虚拟机导出 OVF  再导入 OVF， 检查新导入虚拟机和源虚拟机的 vNIC PCI 不保证一致
                集群升级
                    存量虚拟机升级后，get vm api 的 nics[*].pci_address 字段补齐，检查 api 的 pci_address 和 虚拟机内部的 pci_address 一致
                    存量虚拟机升级后，tower 4.7.1 触发的跨集群冷迁移和分段迁移会保持 pci_address 不变
                ELF API 检查【620P4/515P1/630】
                    查询虚拟机的接口, get api/v2/vms/uuid 增加字段 nics[*].pci_address
                    创建虚拟机接口,  指定有效的 vNIC pci_address 创建虚拟机，创建成功
                    创建虚拟机接口,  指定重复的 pci_address， 创建失败， api 返回对应说明
                    创建虚拟机接口,  指定无效的 pci_address 格式，创建失败， api 返回对应说明
            ELF-6489:业务网络异常触发虚拟机 HA（可配置关机 HA）
                UI测试（Tower480和SMTXOS630）
                    集群设置-高可用-高可用故障场景虚拟机网络故障开关，下拉框有热迁移虚拟机和重建虚拟机，默认为热迁移虚拟机
                    文案-热迁移虚拟机-保证业务连续性与数据完整性，但迁移时长受集群状态和虚拟机负载影响，HA 重建时长不可控。同时，挂载直通设备的虚拟机不支持以此种方式进行 HA 重建。
                    文案-重建虚拟机-将会强制关闭虚拟机，更快完成 HA 重建，但可能导致部分 I/O 数据丢失。
                    集群设置-高可用-高可用故障场景虚拟机网络故障开关，下拉框选择重建虚拟机，保存成功；预期保留重建虚拟机的设置
                    集群设置-高可用-高可用故障场景虚拟机网络故障开关，下拉框选择重建虚拟机，不保存；预期保留热迁移虚拟机的默认设置
                    集群设置-高可用-高可用故障场景虚拟机网络故障开关，下拉框选择重建虚拟机，刷新页面；预期保留热迁移虚拟机的设置
                    版本组合、升级测试
                        Tower480：SMTXOS从620升级到630，集群设置业务网络HA的设置默认为热迁移虚拟机，开关为否。下拉菜单支持选择重建
                        Tower480：新建SMTXOS 630集群，集群设置业务网络HA的设置默认为热迁移虚拟机，开关为否。下拉菜单支持选择重建
                        Tower470关联630，升级到480，集群设置业务网络HA的设置默认为热迁移虚拟机，开关为否。下拉菜单支持选择重建
                        Tower470关联620，升级到480，集群设置业务网络HA的设置默认为热迁移虚拟机，没有重建选项
                        Tower470关联620，升级到630，集群设置业务网络HA的设置默认为热迁移虚拟机，没有重建选项
                功能测试
                    集群业务网络HA默认为热迁移虚拟机，查询数据库network_ha_policy 默认 migrate
                    创建两个运行中虚拟机，一个安装 OS、一个不安装 OS，一个关机虚拟机，触发业务网络故障：开机虚拟机触发成功，关机虚拟机不受影响
                    stop 虚拟机所在节点的 Libvirtd，正常关机时失败：不会触发 recover，下一周期继续重试关机
                    stop 其他网络正常节点的 Libvirtd；关机成功，recover  kvm_vm_create 失败；下一轮重试 recover，但不再执行关机
                    关机成功后，recover 前手动把虚拟机换节点开机；不触发 recover 任务，且虚拟机 _expect_status 字段被正常移除
                    关机成功，recover  kvm_vm_create 失败，恢复故障；虚拟机处于 rebuilding，继续触发远端重建
                    关机成功，recover 阶段 kvm_vm_start 失败；目标端触发本地重建
                    关机后，recover 前，恢复故障；如果 recover 前先触发本地重建，则 recover 不再执行
                    Network HA 周期任务执行过程中，重启 job-center-worker；重启后正常触发 HA 重试
                    业务网络故障时，未连接故障端口的虚拟机可正常触发本地重建
                    系统事件-中英文正常显示业务网络故障触发重建事件
                    回归测试：热迁移配置下，触发业务网络故障
                    回归测试：存储网络故障，触发远端重建
                    制造业务网络 HA 故障,等待虚拟机关机后，将所有健康节点的 Libvirtd 关闭。让重建任务一定失败，且清理调度资源失败:重建失败，调度预留资源被清理。 job-center-worker.INFO 关键字  DirtyScheduleResultCleaner: successfully
                    制造业务网络 HA 故障 ,将虚拟机所在节点 Libvirtd 停止，则无法关机:反复关机失败，调度预留资源被不断生成和清理
                    给 kvm_vm_start 增加代码 sleep (60) ,虚拟机开机;在虚拟机开机任务期间，多次查询数据库有该虚拟机调度结果 且 dirty_scan_time 大于 2。db.vm_scheduler_result.find({},{"host_uuid":1, "results": {"dirty_scan_time": 1, "job_id": 1, "vm_uuid": 1} })
                    系统时间-主机{{主机名1}}上的虚拟机{{虚拟机名}}因虚拟机网络故障触发高可用，迁移至主机{{主机名2}}。
                    系统时间-主机{{主机名1}}上的虚拟机{{虚拟机名}}因虚拟机网络故障触发高可用，重建至主机{{主机名2}}。
            ELF-7483:挂载 SR-IOV 、hygon HCT、vGPU 设备的虚拟机支持 HA
                UI测试
                    挂载直通设备的虚拟机支持 HA
                        通用改动
                            虚拟机未开启HA：vGPU-下拉菜单-选择设备：设备在其他主机上具备相同标识的 GPU 设备，展示 HA 标识及设备可用数量；hover，HA变蓝色
                            虚拟机未开启HA：vGPU-下拉菜单-选择设备：设备在其他主机上具备相同标识的 GPU 设备，但是可用数量为0 ，展示 HA 标识及设备可用数量；hover，HA变红色
                            虚拟机已开启HA：编辑虚拟机vGPU-下拉菜单-选择设备：设备在其他主机上不具备相同标识的 GPU 设备；禁用不支持HA的设备，tip『设备不支持启用HA』
                            虚拟机已开启HA：编辑虚拟机vGPU-下拉菜单-选择设备：设备在其他主机上具备相同标识的 GPU 设备，但是可使用设备为0；禁用不支持HA的设备，tip『设备不支持启用HA』
                            SR-IOV网卡-虚拟机未启用HA-下拉菜单-选择设备：设备已设置设备关联标识，且其他主机上存在具有相同标识的网口；展示HA标识及可用数量，hover HA变蓝色
                            SR-IOV网卡-虚拟机未启用HA-下拉菜单-选择设备：设备已设置设备关联标识，且其他主机上存在具有相同标识的网口但是可用数量为0 ；展示HA标识及可用数量，hover HA变红色
                            SR-IOV网卡-虚拟机启用HA-编辑网络设备-选择设备：设备已设置设备关联标识，且其他主机上不具有相同标识的网口；禁用不支持HA的设备，tip『设备不支持启用HA』
                            SR-IOV网卡-虚拟机启用HA-编辑网络设备-选择设备：设备已设置设备关联标识，且其他主机上不具有相同标识的网口但是可使用数量为0；禁用不支持HA的设备，tip『设备不支持启用HA』
                            加密控制器-虚拟机未启用HA-下拉菜单-选择设备：若设备已设置设备关联标识，且其他主机上存在具有相同标识的加密控制器）；展示 HA 标识及设备可用数量；hover，HA变蓝色
                            加密控制器-虚拟机未启用HA-下拉菜单-选择设备：若设备已设置设备关联标识，且其他主机上存在具有相同标识的加密控制器，打但是数量为0）；展示 HA 标识及设备可用数量；hover，HA变红色
                            加密控制器-虚拟机启用HA-编辑加密控制器-选择设备：若设备已设置设备关联标识，且其他主机上不具有相同标识的加密控制器）；禁用不支持HA的设备，tip『设备不支持启用HA』
                            加密控制器-虚拟机启用HA-编辑加密控制器-选择设备：若设备已设置设备关联标识，主机上具有相同标识的加密控制器，数量为0）；禁用不支持HA的设备，tip『设备不支持启用HA』
                        创建虚拟机
                            创建空白虚拟机
                                创建空白虚拟机-计算资源-选择GPU-下拉菜单显示HA标识
                                创建空白虚拟机-网络设备-选择物理网口-下拉菜单显示HA标识
                                创建空白虚拟机-网络设备-选择物理网口-下拉菜单选择带HA的网口，展示tip：若虚拟机开启HA，但未安装虚拟机工具，重建后，IP可能发生变化
                                创建空白虚拟机-其他配置-虚拟机选择不支持高可用的GPU，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                创建空白虚拟机-其他配置-虚拟机选择不支持高可用的加密控制器，高可用开关禁用，展示tip『其他设备包含无法高可用的加密控制器，无法开启高可用』；加密控制器开关禁用
                                创建空白虚拟机-其他配置-虚拟机选择支持高可用的GPU，高可用开关启用，开启HA成功
                                创建空白虚拟机-其他配置-虚拟机选择支持高可用的SR-IOV网口，高可用开关启用，开启HA成功
                                创建空白虚拟机-其他配置-虚拟机选择不支持高可用的SR-IOV，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                创建空白虚拟机-其他配置-虚拟机选择不支持高可用的PCI，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                创建空白虚拟机-其他配置-虚拟机选择支持高可用的SR-IOV网口，高可用开关启用，可以选择加密控制器
                            从模板创建虚拟机
                                从模板创建虚拟机-计算资源-选择GPU-下拉菜单显示HA标识
                                从模板创建虚拟机-网络设备-选择物理网口-下拉菜单显示HA标识
                                从模板创建虚拟机-网络设备-选择物理网口-下拉菜单选择带HA的网口，展示tip：若虚拟机开启HA，但未安装虚拟机工具，重建后，IP可能发生变化
                                从模板创建虚拟机-其他配置-虚拟机选择不支持高可用的GPU，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                从模板创建虚拟机-其他配置-虚拟机选择不支持高可用的GPU，高可用开关禁用，展示tip『其他设备包含无法高可用的加密控制器，无法开启高可用』；加密控制器开关禁用
                                从模板创建虚拟机-其他配置-虚拟机选择支持高可用的GPU，高可用开关启用，开启HA成功
                                从模板创建虚拟机其他配置-虚拟机选择支持高可用的PCI网口，高可用开关启用，开启HA成功
                                从模板创建虚拟机-其他配置-虚拟机选择支持高可用的SR-IOV网口，高可用开关启用，开启HA成功
                                从模板创建虚拟机-其他配置-虚拟机选择不支持高可用的SR-IOV，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                从模板创建虚拟机-其他配置-虚拟机选择不支持高可用的PCI，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                从模板创建虚拟机-其他配置-虚拟机选择支持高可用的SR-IOV网口，高可用开关启用，可以选择加密控制器
                            克隆虚拟机
                                克隆创建虚拟机-计算资源-选择GPU-下拉菜单显示HA标识
                                克隆创建虚拟机-网络设备-选择物理网口-下拉菜单显示HA标识
                                克隆创建虚拟机-网络设备-选择物理网口-下拉菜单选择带HA的网口，展示tip：若虚拟机开启HA，但未安装虚拟机工具，重建后，IP可能发生变化
                                克隆创建虚拟机-其他配置-虚拟机选择不支持高可用的GPU，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                克隆创建虚拟机-其他配置-虚拟机选择不支持高可用的GPU，高可用开关禁用，展示tip『其他设备包含无法高可用的加密控制器，无法开启高可用』；加密控制器开关禁用
                                克隆创建虚拟机-其他配置-虚拟机选择支持高可用的GPU，高可用开关启用，开启HA成功
                                克隆创建虚拟机其他配置-虚拟机选择支持高可用的PCI网口，高可用开关启用，开启HA成功
                                克隆创建虚拟机-其他配置-虚拟机选择支持高可用的SR-IOV网口，高可用开关启用，开启HA成功
                                克隆创建虚拟机-其他配置-虚拟机选择不支持高可用的SR-IOV，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                克隆创建虚拟机-其他配置-虚拟机选择不支持高可用的PCI，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                克隆创建虚拟机-其他配置-虚拟机选择支持高可用的SR-IOV网口，高可用开关启用，可以选择加密控制器
                            导入虚拟机
                                导入创建虚拟机-计算资源-选择GPU-下拉菜单显示HA标识
                                导入创建虚拟机-网络设备-选择物理网口-下拉菜单显示HA标识
                                导入创建虚拟机-网络设备-选择物理网口-下拉菜单选择带HA的网口，展示tip：若虚拟机开启HA，但未安装虚拟机工具，重建后，IP可能发生变化
                                导入创建虚拟机-其他配置-虚拟机选择不支持高可用的GPU，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                导入创建虚拟机-其他配置-虚拟机选择不支持高可用的GPU，高可用开关禁用，展示tip『其他设备包含无法高可用的加密控制器，无法开启高可用』；加密控制器开关禁用
                                导入创建虚拟机-其他配置-虚拟机选择支持高可用的GPU，高可用开关启用，开启HA成功
                                导入创建虚拟机其他配置-虚拟机选择支持高可用的PCI网口，高可用开关启用，开启HA成功
                                导入创建虚拟机-其他配置-虚拟机选择支持高可用的SR-IOV网口，高可用开关启用，开启HA成功
                                导入创建虚拟机-其他配置-虚拟机选择不支持高可用的SR-IOV，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                导入创建虚拟机-其他配置-虚拟机选择不支持高可用的PCI，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                导入创建虚拟机-其他配置-虚拟机选择支持高可用的SR-IOV网口，高可用开关启用，可以选择加密控制器
                            重建虚拟机
                                快照重建创建虚拟机-计算资源-选择GPU-下拉菜单显示HA标识
                                快照重建创建虚拟机-网络设备-选择物理网口-下拉菜单显示HA标识
                                快照重建创建虚拟机-网络设备-选择物理网口-下拉菜单选择带HA的网口，展示tip：若虚拟机开启HA，但未安装虚拟机工具，重建后，IP可能发生变化
                                快照重建创建虚拟机-其他配置-虚拟机选择不支持高可用的GPU，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                快照重建创建虚拟机-其他配置-虚拟机选择不支持高可用的GPU，高可用开关禁用，展示tip『其他设备包含无法高可用的加密控制器，无法开启高可用』；加密控制器开关禁用
                                快照重建创建虚拟机-其他配置-虚拟机选择支持高可用的GPU，高可用开关启用，开启HA成功
                                快照重建创建虚拟机其他配置-虚拟机选择支持高可用的PCI网口，高可用开关启用，开启HA成功
                                快照重建创建虚拟机-其他配置-虚拟机选择支持高可用的SR-IOV网口，高可用开关启用，开启HA成功
                                快照重建创建虚拟机-其他配置-虚拟机选择不支持高可用的SR-IOV，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                快照重建创建虚拟机-其他配置-虚拟机选择不支持高可用的PCI，高可用开关禁用，展示tip『虚拟机已配置不支持HA的GPU、PCI设备，无法开启高可用』
                                快照重建创建虚拟机-其他配置-虚拟机选择支持高可用的SR-IOV网口，高可用开关启用，可以选择加密控制器
                        编辑高可用
                            虚拟机挂载了不支持高可用的GPU设备：高可用禁用，且tip虚拟机已配置不支持HA的GPU、SR-IOV、PCI、加密控制器，无法开启HA
                            虚拟机挂载了不支持高可用的SR-IOV设备：高可用禁用，且tip虚拟机已配置布支持HA的GPU、SR-IOV、PCI、加密控制器，无法开启HA
                            虚拟机挂载了不支持高可用的加密控制器设备：高可用禁用，且tip虚拟机已配置布支持HA的GPU、SR-IOV、PCI、加密控制器，无法开启HA
                            虚拟机挂载了同时配置支持HA的GPU1和不支持HA的GPU2：高可用开关禁用
                            虚拟机挂载了同时配置支持HA的GPU1和不支持HA的SR-IOV：高可用开关禁用
                            虚拟机挂载了同时配置支持HA的GPU1和不支持HA的加密控制器：高可用禁用
                            批量选择2个虚拟机（一个支持HA、一个挂载了不支持高可用的GPU）-支持开启HA的可开启HA，同时tip：『1个虚拟机无法启用HA,VMNAME虚拟机已配置布支持HA的GPU、SR-IOV、PCI、加密控制器』
                        编辑直通设备
                            编辑虚拟机基本信息-启用HA-选择GPU设备，GPU设备可选，tip『虚拟机已开启高可用，无法挂载直通GPU设备』
                            编辑虚拟机基本信息-启用HA-选择GPU设备，GPU设备可选，下来菜单增加HA标识
                            编辑虚拟机网络设备-启用HA-未安装vmtools，tip『虚拟机未安装vmtool，重建后，IP可能会发生变化』
                            编辑虚拟机网络设备-启用HA-下拉菜单增加HA标识
                            编辑虚拟机网络设备-启用HA-添加SR-IOV网口可选；tip『虚拟机已开启HA，无法添加PCI直通网卡』
                            虚拟详情页面-虚拟机开启HA-不再禁用挂载加密控制器选项
                            虚拟详情页面-虚拟机开启HA-选择加密控制器，下拉菜单增加HA标识
                    直通设备新增「设备标识」字段
                        编辑设备表标识弹窗
                            单个编辑
                                编辑网口设备标识
                                    单个编辑-设置网口 %device-name% 的设备标识。
                                    单个编辑-设备标识-只支持非中文-中文校验
                                    单个编辑-设备标识-只支持中文-长度校验：1个字符
                                    单个编辑-设备标识-只支持中文-长度校验：200个字符
                                    单个编辑-设备标识-只支持中文-输入数字，无法保存
                                    单个编辑-设备标识-只支持中文-输入特殊符号@%*，无法保存
                                    单个编辑-设备标识-只支持中文-输入因为你addd，无法保存
                                    单个编辑-设备标识-已存在『suggest』的标识，则输入s时，给出已有suggest标识的提示
                                    单个编辑-设备标识-已存在『suggestzkzkclsclslclsclcslsc』的标识，则输入s时，给出已有标识的提示，文字过长时打点截断，hover 展示完整 tooltip
                                    单个编辑-设备标识-已存在『xxxuggest』的标识，则输入s时，不给出已有标识的提示（不存在匹配的则没有提示）
                                    单个编辑-设备标识-已存在『suggest、sjjgjg、sskkk』的标识，则输入s时，给出已有的3个s开头标识的提示
                                    单个编辑-设备标识-已存在『suggest、sjjgjg、sskkk、xxxx』的标识，则输入s时，给出已有的3个s开头标识的提示，不给x开头的提示
                                加密控制器设备标识
                                    单个编辑-设置加密控制器 %device-name% 的设备标识。
                                    单个编辑-设备标识-只支持中文-中文校验
                                    单个编辑-设备标识-只支持中文-长度校验：1个字符
                                    单个编辑-设备标识-只支持中文-长度校验：200个字符
                                    单个编辑-设备标识-只支持中文-输入数字，无法保存
                                    单个编辑-设备标识-只支持中文-输入特殊符号@%*，无法保存
                                    单个编辑-设备标识-只支持中文-输入因为你addd，无法保存
                                    单个编辑-设备标识-已存在『suggest』的标识，则输入s时，给出已有suggest标识的提示
                                    单个编辑-设备标识-已存在『suggestzkzkclsclslclsclcslsc』的标识，则输入s时，给出已有标识的提示，文字过长时打点截断，hover 展示完整 tooltip
                                    单个编辑-设备标识-已存在『xxxuggest』的标识，则输入s时，不给出已有标识的提示（不存在匹配的则没有提示）
                                    单个编辑-设备标识-已存在『suggest、sjjgjg、sskkk』的标识，则输入s时，给出已有的3个s开头标识的提示
                                    单个编辑-设备标识-已存在『suggest、sjjgjg、sskkk、xxxx』的标识，则输入s时，给出已有的3个s开头标识的提示，不给x开头的提示
                            批量编辑
                                编辑网口设备标识
                                    批量编辑-批量设置N个设置网口的设备标识。
                                    批量编辑-设备标识-只支持中文-中文校验-设备1写中文，设备2写中文；可以保存
                                    批量编辑-设备标识-只支持中文-长度校验：全部设备1个字符
                                    批量编辑-设备标识-只支持中文-长度校验：全部设备200个字符
                                    批量编辑-设备标识-只支持中文-全部设备输入数字，无法保存
                                    批量编辑-设备标识-只支持中文-全部设备输入特殊符号@%*，无法保存
                                    批量编辑-设备标识-只支持中文-全部设备输入因为你addd，无法保存
                                    批量编辑-设备标识-全部设备已存在『suggest』的标识，则输入s时，给出已有suggest标识的提示
                                    批量编辑-设备标识-全部设备已存在『suggestzkzkclsclslclsclcslsc』的标识，则输入s时，给出已有标识的提示，文字过长时打点截断，hover 展示完整 tooltip
                                    批量编辑-设备标识-全部设备已存在『xxxuggest』的标识，则输入s时，不给出已有标识的提示（不存在匹配的则没有提示）
                                    批量编辑-设备标识-全部设备已存在『suggest、sjjgjg、sskkk』的标识，则输入s时，给出已有的3个s开头标识的提示
                                    批量编辑-设备标识-全部设备已存在『suggest、sjjgjg、sskkk、xxxx』的标识，则输入s时，给出已有的3个s开头标识的提示，不给x开头的提示
                                    批量编辑-设备标识-设备1已存在『suggest』的标识，设备2存在『xxxx』则输入s时，则给出两个提示
                                编辑加密控制器设备标识
                                    批量编辑-批量设置N个加密控制器的设备标识。
                                    批量编辑-设备标识-只支持中文-中文校验-设备1写中文，设备2写中文；可以保存
                                    批量编辑-设备标识-只支持中文-长度校验：全部设备1个字符
                                    批量编辑-设备标识-只支持中文-长度校验：全部设备200个字符
                                    批量编辑-设备标识-只支持中文-全部设备输入数字，无法保存
                                    批量编辑-设备标识-只支持中文-全部设备输入特殊符号@%*，无法保存
                                    批量编辑-设备标识-只支持中文-全部设备输入因为你addd，无法保存
                                    批量编辑-设备标识-全部设备已存在『suggest』的标识，则输入s时，给出已有suggest标识的提示
                                    批量编辑-设备标识-全部设备已存在『suggestzkzkclsclslclsclcslsc』的标识，则输入s时，给出已有标识的提示，文字过长时打点截断，hover 展示完整 tooltip
                                    批量编辑-设备标识-全部设备已存在『xxxuggest』的标识，则输入s时，不给出已有标识的提示（不存在匹配的则没有提示）
                                    批量编辑-设备标识-全部设备已存在『suggest、sjjgjg、sskkk』的标识，则输入s时，给出已有的3个s开头标识的提示
                                    批量编辑-设备标识-全部设备已存在『suggest、sjjgjg、sskkk、xxxx』的标识，则输入s时，给出已有的3个s开头标识的提示，不给x开头的提示
                                    批量编辑-设备标识-设备1已存在『suggest』的标识，设备2存在『xxxx』则输入s时，则给出两个提示
                        网口列表
                            设备标识
                                点击网口设置-勾选「设备标识」，在网口用途和 SR-IOV 状态之间展示「设备标识」字段；
                                点击网口设置-反勾选「设备标识」，在网口用途和 SR-IOV 状态隐藏「设备标识」字段；
                                点击网口-「点击设备标识」，再多次点击，可以进行排序，
                                点击网口-不未设置设备标识的网口，显示为  -
                            批量编辑
                                选择1网口，网口用途为「SR-IOV 直通」，展示「编辑设备标识」入口，点击后打开编辑弹窗
                                选择2网口，网口用途都为「SR-IOV 直通」，展示「批量编辑设备标识」入口，点击后打开批量编辑弹窗
                                选择2网口，网口用途不全是「SR-IOV 直通」，不展示「批量编辑设备标识」入口
                                选择2网口，网口用途全不是「SR-IOV 直通」，不展示「批量编辑设备标识」入口
                            morebutton
                                选择1网口，网口用途为「SR-IOV 直通」，展示「编辑设备标识」入口，点击后打开弹窗
                                选择1网口，网口用途不为「SR-IOV 直通」，不展示「编辑设备标识」入口
                            网口详情面板
                                网口用途为「SR-IOV 直通」的网口新增「设备标识」tab，展示网口的设备标识和具备相同标识的网口
                                网口用途不为「SR-IOV 直通」的网口，保持历史原状
                                网口用途为「SR-IOV 直通」的网口-设备标识-点击打开「编辑设备标识」弹窗
                                网口用途为「SR-IOV 直通」的网口新增「设备标识」tab，无关联设备，展示空白
                                网口用途为「SR-IOV 直通」的网口新增「设备标识」tab，展示网口的设备标识和具备相同标识的网口;展示主机列表
                                网口用途为「SR-IOV 直通」的网口新增「设备标识」tab，展示网口的设备标识和具备相同标识的网口;展示SR-IOV状态
                                网口用途为「SR-IOV 直通」的网口新增「设备标识」tab，展示网口的设备标识和具备相同标识的网口;展示SR-IOV直通网卡数量
                                网口用途为「SR-IOV 直通」的网口新增「设备标识」tab，展示网口的设备标识和具备相同标识的网口;展示SR-IOV网口已使用数量
                        GPU设备列表
                            设备标识
                                点击GPU设备设置-勾选「设备标识」，在GPU和 vGPU规格之间展示「设备标识」字段；
                                点击GPU设备设置-反勾选「设备标识」，在GPU和 vGPU规格之间展示隐藏「设备标识」字段；
                                点击GPU设备-「点击设备标识」，再多次点击，可以进行排序，
                                点击GPU设备-GPU设备标识不支持编辑
                            GPU详设备情面板
                                用途为「vGPU」的设备新增「设备标识」tab，展示后端自动生成的设备标识和具备相同标识的 GPU 设备，不可编辑
                                用途为「GPU直通」的设备不展示
                                用途为「vGPU」的设备新增「设备标识」tab，无法编辑设备标识
                                用途为「vGPU」的设备新增「设备标识」tab：无关联设备，展示空白
                                用途为「vGPU」的设备新增「设备标识」tab，展示后端自动生成的设备标识和具备相同标识的 GPU 设备：展示名称
                                用途为「vGPU」的设备新增「设备标识」tab，展示后端自动生成的设备标识和具备相同标识的 GPU 设备：展示所属主机
                                用途为「vGPU」的设备新增「设备标识」tab，展示后端自动生成的设备标识和具备相同标识的 GPU 设备：展示vGPU数量
                        PCI设备列表
                            设备标识
                                点击PCI设置-勾选「设备标识」，在设备用途和 直通状态之间展示「设备标识」字段；
                                点击PCI设置-反勾选「设备标识」，在设备用途和 直通状态之间隐藏「设备标识」字段；
                                点击PCI-「点击设备标识」，再多次点击，可以进行排序，
                                点击PCI-未设置设备标识的PCI，显示为  -
                            批量编辑
                                选择1加密控制器，用途为「MDEV 直通」，展示「编辑设备标识」入口，点击后打开编辑弹窗
                                选择2加密控制器，用途都为「MDEV 直通」，展示「批量编辑设备标识」入口，点击后打开批量编辑弹窗
                                选择2加密控制器，用途不全为「MDEV 直通」，不展示「编辑设备标识」入
                                选择1加密控制器，用途全不为「MDEV 直通」，不展示「编辑设备标识」入口
                                选择1加密控制器、1其他PCI设备，用途为「MDEV 直通」，不展示「批量编辑设备标识」入口
                                选择2其他PCI设备，不展示「批量编辑设备标识」入口
                            morebutton
                                选择1加密控制器，用途为「MDEV 直通」，展示「编辑设备标识」入口，点击后打开弹窗
                                选择1加密控制器，用途不为「MDEV 直通」，不展示「编辑设备标识」入口
                                选择1其他PCI，不展示「编辑设备标识」入口
                            PCI设备详情面板
                                加密控制器用途为「MDEV直通」的新增「设备标识」tab，展示设备标识和具备相同标识的设备
                                加密控制器用途不为「MDEV直通」的不展示「设备标识」tab
                                加密控制器用途为「MDEV直通」-设备标识-点击打开「编辑设备标识」弹窗
                                加密控制器用途为「MDEV直通新增「设备标识」tab，无关联设备，展示空白
                                加密控制器用途为「MDEV直通」新增「设备标识」tab，展示设备标识关联设备，展示主机名称
                                加密控制器用途为「MDEV直通」新增「设备标识」tab，展示设备标识关联设备，展示所属主机
                                加密控制器用途为「MDEV直通」新增「设备标识」tab，展示设备标识关联设备，展示直通状态
                                加密控制器用途为「MDEV直通」新增「设备标识」tab，展示设备标识关联设备，展示设备切分数量
                                加密控制器用途为「MDEV直通」新增「设备标识」tab，展示设备标识关联设备，展示设备已使用数量
                                其他PCI设备，不展示「设备标识」tab，保持历史原样
                功能测试
                    直通设备 HA 关联管理
                        SR-IOV 网卡-设置设备标识-一个网卡仅可设置一个标识
                        MDEV 直通的加密控制器-设置设备标识-一个设备仅可设置一个标识
                        非MDEV 直通的加密控制器-设置设备标识-不可设置
                        vGPU 设备：vGPU 的设备标识不支持设置，系统自动生成
                    虚拟机 HA 行为调整
                        SR-IOV网卡直通HA
                            虚拟机业务网络故障
                                挂载SR-IOV网卡开启HA的虚拟机，集群层面配置业务网故障HA动作为热迁移，但是该虚拟机不会触发热迁移
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机存在相同标识网卡，且可用数量>0。主机存储网故障，虚拟机重建到对应主机，SR—IOV功能正常
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机不存在相同标识网卡。主机存储网故障，虚拟机暂停，故障恢复，虚拟机本地恢复，SR—IOV功能正常
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机存在相同标识网卡，且可用数量=0。主机存储网故障，虚拟机暂停，故障恢复，虚拟机本地恢复，SR—IOV功能正常
                                SR-IOV-网卡的虚拟机，存储网故障重建到目标主机，MAC和PCI地址保持不变
                                SR-IOV-网卡的虚拟机，存储网故障，重建到目标主机，安装了 VMTools 时 SR-IOV 网卡 IP 地址应与重建前一致
                                SR-IOV-网卡的虚拟机，存储网故障重建到目标主机，未安装 VMTools 时 SR-IOV 网卡 IP 地址和重建前一致
                            主机存储网故障
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机存在相同标识网卡，且可用数量>0。主机存储网故障，虚拟机重建到对应主机，SR—IOV功能正常
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机不存在相同标识网卡。主机存储网故障，虚拟机暂停，故障恢复，虚拟机本地恢复，SR—IOV功能正常
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机存在相同标识网卡，且可用数量=0。主机存储网故障，虚拟机暂停，故障恢复，虚拟机本地恢复，SR—IOV功能正常
                                SR-IOV-网卡的虚拟机，存储网故障重建到目标主机，MAC和PCI地址保持不变
                                SR-IOV-网卡的虚拟机，存储网故障，重建到目标主机，安装了 VMTools 时 SR-IOV 网卡 IP 地址应与重建前一致
                                SR-IOV-网卡的虚拟机，存储网故障重建到目标主机，未安装 VMTools 时 SR-IOV 网卡 IP 地址不保证和重建前一致
                            主机断电
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机存在相同标识网卡，且可用数量>0。主机断电故障，虚拟机重建到对应主机，SR—IOV功能正常
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机不存在相同标识网卡。主机断电故障，虚拟机暂停，故障恢复，虚拟机本地恢复，SR—IOV功能正常
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机存在相同标识网卡，且可用数量=0。主机断电故障，虚拟机暂停，故障恢复，虚拟机本地恢复，SR—IOV功能正常
                                SR-IOV-网卡的虚拟机，主机断电故障重建到目标主机，MAC和PCI地址保持不变
                                SR-IOV-网卡的虚拟机，主机断电故障，重建到目标主机，安装了 VMTools 时 SR-IOV 网卡 IP 地址应与重建前一致
                                SR-IOV-网卡的虚拟机，主机断电故障重建到目标主机，未安装 VMTools 时 SR-IOV 网卡 IP 地址不保证和重建前一致
                            虚拟机操作系统故障
                                开启HA的虚拟机，挂载SR-IOV网卡，虚拟机OS故障，原主机重启虚拟机后仍应保持原直通设备挂载
                            虚拟机源主机本地重建
                                开启HA的虚拟机，挂载SR-IOV网卡，虚拟机 virsh destroy，原主机虚拟机重建后仍应保持原直通设备挂载
                                开启HA的虚拟机，挂载SR-IOV网卡，虚拟机 、kill qemu进程，原主机虚拟机重建后仍应保持原直通设备挂载
                            ZBS-RPC失联（vhost环境）
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机存在相同标识网卡，且可用数量>0。主机存储网故障，虚拟机重建到对应主机，SR—IOV功能正常
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机不存在相同标识网卡。主机存储网故障，虚拟机暂停，故障恢复，虚拟机本地恢复，SR—IOV功能正常
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机存在相同标识网卡，且可用数量=0。主机存储网故障，虚拟机暂停，故障恢复，虚拟机本地恢复，SR—IOV功能正常
                                SR-IOV-网卡的虚拟机，存储网故障重建到目标主机，MAC和PCI地址保持不变
                                SR-IOV-网卡的虚拟机，存储网故障，重建到目标主机，安装了 VMTools 时 SR-IOV 网卡 IP 地址应与重建前一致
                                SR-IOV-网卡的虚拟机，存储网故障重建到目标主机，未安装 VMTools 时 SR-IOV 网卡 IP 地址不保证和重建前一致
                            主机操作系统只读
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机存在相同标识网卡，且可用数量>0。主机存储网故障，虚拟机重建到对应主机，SR—IOV功能正常
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机不存在相同标识网卡。主机存储网故障，虚拟机暂停，故障恢复，虚拟机本地恢复，SR—IOV功能正常
                                开启HA的虚拟机，挂载SR-IOV网卡，其他主机存在相同标识网卡，且可用数量=0。主机存储网故障，虚拟机暂停，故障恢复，虚拟机本地恢复，SR—IOV功能正常
                                SR-IOV-网卡的虚拟机，存储网故障重建到目标主机，MAC和PCI地址保持不变
                                SR-IOV-网卡的虚拟机，存储网故障，重建到目标主机，安装了 VMTools 时 SR-IOV 网卡 IP 地址应与重建前一致
                                SR-IOV-网卡的虚拟机，存储网故障重建到目标主机，未安装 VMTools 时 SR-IOV 网卡 IP 地址不保证和重建前一致
                        vGPU设备HA
                            虚拟机业务网络故障
                                开启HA的虚拟机，挂载vGPU，其他主机存在相同标识网卡，且可用数量>0。触发故障，虚拟机重建到对应主机，vGPU功能正常
                                开启HA的虚拟机，挂载vGPU，其他主机不存在相同标识vGPU。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，vGPU功能正常
                                开启HA的虚拟机，挂载vGPU，其他主机存在相同标识vGPU，且可用数量=0。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，vGPU功能正常
                            主机存储网故障
                                开启HA的虚拟机，挂载vGPU，其他主机存在相同标识网卡，且可用数量>0。触发故障，虚拟机重建到对应主机，vGPU功能正常
                                开启HA的虚拟机，挂载vGPU，其他主机不存在相同标识vGPU。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，vGPU功能正常
                                开启HA的虚拟机，挂载vGPU，其他主机存在相同标识vGPU，且可用数量=0。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，vGPU功能正常
                            主机断电
                                开启HA的虚拟机，挂载vGPU，其他主机存在相同标识网卡，且可用数量>0。触发故障，虚拟机重建到对应主机，vGPU功能正常
                                开启HA的虚拟机，挂载vGPU，其他主机不存在相同标识vGPU。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，vGPU功能正常
                                开启HA的虚拟机，挂载vGPU，其他主机存在相同标识vGPU，且可用数量=0。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，vGPU功能正常
                            虚拟机操作系统故障
                                开启HA的虚拟机，挂载vGPU，虚拟机OS故障，原主机重启虚拟机后仍应保持原直通设备挂载
                            虚拟机源主机本地重建
                                开启HA的虚拟机，挂载vGPU，虚拟机 virsh destroy，原主机虚拟机重建后仍应保持原直通设备挂载
                                开启HA的虚拟机，挂载vGPU，虚拟机 、kill qemu进程，原主机虚拟机重建后仍应保持原直通设备挂载
                            ZBS-RPC失联（vhost环境）
                                开启HA的虚拟机，挂载vGPU，其他主机存在相同标识网卡，且可用数量>0。触发故障，虚拟机重建到对应主机，vGPU功能正常
                                开启HA的虚拟机，挂载vGPU，其他主机不存在相同标识vGPU。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，vGPU功能正常
                                开启HA的虚拟机，挂载vGPU，其他主机存在相同标识vGPU，且可用数量=0。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，vGPU功能正常
                            主机操作系统只读
                                开启HA的虚拟机，挂载vGPU，其他主机存在相同标识网卡，且可用数量>0。触发故障，虚拟机重建到对应主机，vGPU功能正常
                                开启HA的虚拟机，挂载vGPU，其他主机不存在相同标识vGPU。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，vGPU功能正常
                                开启HA的虚拟机，挂载vGPU，其他主机存在相同标识vGPU，且可用数量=0。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，vGPU功能正常
                        加密控制器设备HA
                            虚拟机业务网络故障
                                开启HA的虚拟机，挂载加密控制器且类型为MDEV 直通，其他主机存在相同标识加密控制器，且可用数量>0。触发故障，虚拟机重建到对应主机，加密控制器功能正常
                                开启HA的虚拟机，挂载加密控制器，其他主机不存在相同标识加密控制器。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，加密控制器功能正常
                                开启HA的虚拟机，挂载加密控制器，其他主机存在相同标识加密控制器，且可用数量=0。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，加密控制器功能正常
                            主机存储网故障
                                开启HA的虚拟机，挂载加密控制器且类型为MDEV 直通，其他主机存在相同标识加密控制器，且可用数量>0。触发故障，虚拟机重建到对应主机，加密控制器功能正常
                                开启HA的虚拟机，挂载加密控制器且类型为不是MDEV 直通，其他主机存在相同标识加密控制器，且可用数量>0。触发故障，虚拟机不会触发重建
                                开启HA的虚拟机，挂载加密控制器，其他主机不存在相同标识加密控制器。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，加密控制器功能正常
                                开启HA的虚拟机，挂载加密控制器，其他主机存在相同标识加密控制器，且可用数量=0。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，加密控制器功能正常
                            主机断电
                                开启HA的虚拟机，挂载加密控制器且类型为MDEV 直通，其他主机存在相同标识加密控制器，且可用数量>0。触发故障，虚拟机重建到对应主机，加密控制器功能正常
                                开启HA的虚拟机，挂载加密控制器且类型为不是MDEV 直通，其他主机存在相同标识加密控制器，且可用数量>0。触发故障，虚拟机不会触发重建
                                开启HA的虚拟机，挂载加密控制器，其他主机不存在相同标识加密控制器。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，加密控制器功能正常
                                开启HA的虚拟机，挂载加密控制器，其他主机存在相同标识加密控制器，且可用数量=0。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，加密控制器功能正常
                            虚拟机操作系统故障
                                开启HA的虚拟机，挂载加密控制器，虚拟机OS故障，原主机重启虚拟机后仍应保持原直通设备挂载
                            虚拟机源主机本地重建
                                开启HA的虚拟机，挂载加密控制器，虚拟机 virsh destroy，原主机虚拟机重建后仍应保持原直通设备挂载
                                开启HA的虚拟机，挂载加密控制器，虚拟机 、kill qemu进程，原主机虚拟机重建后仍应保持原直通设备挂载
                            ZBS-RPC失联（vhost环境）
                                开启HA的虚拟机，挂载加密控制器且类型为MDEV 直通，其他主机存在相同标识加密控制器，且可用数量>0。触发故障，虚拟机重建到对应主机，加密控制器功能正常
                                开启HA的虚拟机，挂载加密控制器且类型为不是MDEV 直通，其他主机存在相同标识加密控制器，且可用数量>0。触发故障，虚拟机不会触发重建
                                开启HA的虚拟机，挂载加密控制器，其他主机不存在相同标识加密控制器。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，加密控制器功能正常
                                开启HA的虚拟机，挂载加密控制器，其他主机存在相同标识加密控制器，且可用数量=0。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，加密控制器功能正常
                            主机操作系统只读
                                开启HA的虚拟机，挂载加密控制器且类型为MDEV 直通，其他主机存在相同标识加密控制器，且可用数量>0。触发故障，虚拟机重建到对应主机，加密控制器功能正常
                                开启HA的虚拟机，挂载加密控制器且类型为不是MDEV 直通，其他主机存在相同标识加密控制器，且可用数量>0。触发故障，虚拟机不会触发重建
                                开启HA的虚拟机，挂载加密控制器，其他主机不存在相同标识加密控制器。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，加密控制器功能正常
                                开启HA的虚拟机，挂载加密控制器，其他主机存在相同标识加密控制器，且可用数量=0。主机故障，虚拟机暂停，故障恢复，虚拟机本地恢复，加密控制器功能正常
                            不同Hygon型号之间的HA
                                开启HA的虚拟机，Hygon3挂载加密控制器且类型为MDEV 直通，其他Hygon4主机存在相同标识加密控制器，且可用数量>0。触发故障，虚拟机重建到对应主机，加密控制器功能正常
                                开启HA的虚拟机，Hygon3挂载加密控制器且类型为MDEV 直通，其他Hygon2主机存在相同标识加密控制器，且可用数量>0。触发故障，虚拟机重建到对应主机，加密控制器功能正常
                        同时挂载多种类型直通设备的HA
                            多种直通设备不全满足直通HA条件
                                开启HA的虚拟机，挂载SR-IOV网卡、vGPU设备，其他主机存在相同标识网卡，但是不存在相同标识vGPU设备；主机故障，虚拟机无法重建到目标主机
                                开启HA的虚拟机，挂载SR-IOV网卡、加密控制器设备，其他主机存在相同标识网卡，但是不存在相同标识加密控制器设备；主机故障，虚拟机无法重建到目标主机
                                开启HA的虚拟机，挂载SR-IOV网卡、vGPU设备，其他主机存在相同标识网卡，存在相同标识vGPU设备，但是可用为0；主机故障，虚拟机无法重建到目标主机
                                开启HA的虚拟机，挂载SR-IOV网卡、加密控制器设备，其他主机存在相同标识网卡和加密控制器，但是加密控制器不是MDEV直通；主机故障，虚拟机无法重建到目标主机
                                开启HA的虚拟机，挂载vGPU设备、加密控制器，其他主机存在相同标识vGPU，存在相同标识加密控制器，但是不是MDEV直通；主机故障，虚拟机无法重建到目标主机
                                开启HA的虚拟机，挂载2个SR-IOV网卡，其他只存在1个相同标识网卡；主机故障，虚拟机无法重建到目标主机
                                开启HA的虚拟机，挂载2个SR-IOV网卡，其他存在2个相同标识网卡，但是其中一个可用数量为0；主机故障，虚拟机无法重建到目标主机
                                开启HA的虚拟机，挂载2个vGPU设备，其他只存在1个相同标识vGPU；主机故障，虚拟机无法重建到目标主机
                                开启HA的虚拟机，挂载2个vGPU，其他存在2个相同标识vGPU，但是其中一个可用数量为0；主机故障，虚拟机无法重建到目标主机
                                开启HA的虚拟机，挂载2个加密控制器，其他只存在1个相同标识加密控制器；主机故障，虚拟机无法重建到目标主机
                                开启HA的虚拟机，挂载加密控制器，其他存在2个相同标识设备，但是其中类型不是MVDEV直通；主机故障，虚拟机无法重建到目标主机
                            多种直通设备全满足直通HA条件
                                开启HA的虚拟机，挂载SR-IOV网卡、加密控制器、vGPU设备，其他主机存在相同标识网卡，存在全部相同标识设备；主机故障，虚拟机在目标主机重建，全部设备都正常
                                开启HA的虚拟机，挂载2个SR-IOV网卡，其他存在2个相同标识网卡；主机故障，虚拟机重建到目标主机，且网卡全部正常
                                开启HA的虚拟机，挂载2个不同类型vGPU，其他存在2个相同标识设备；主机故障，虚拟机重建到目标主机，且不同类型vGPU全部正常
                                开启HA的虚拟机，挂载2个加密控制器，其他存在2个相同标识设备，且都是MDEV直通；主机故障，虚拟机重建到目标主机，设备全部正常
                            不满足HA条件的直通设备，调整条件后，满足HA
                                开启HA的虚拟机，挂载SR-IOV网卡、vGPU设备，其他主机存在相同标识网卡，但是不存在相同标识vGPU设备；卸载vGPU设备，主机故障，虚拟机可以重建到目标主机
                                开启HA的虚拟机，挂载vGPU设备、加密控制器，其他主机存在相同标识vGPU，存在相同标识加密控制器，将非MDEV改为MDEV直通；主机故障，虚拟机可以重建到目标主机
                                开启HA的虚拟机，挂载2个vGPU，其他存在2个相同标识vGPU，但是其中一个可用数量为0；将目标主机的vGPU释放出来一部分，主机故障，虚拟机可以重建到目标主机
                                开启HA的虚拟机，挂载2个SR-IOV网卡，其他存在2个相同标识网卡，但是其中一个可用数量为0；将目标主机SR-IOV网卡释放一部分，主机故障，虚拟机可以重建到目标主机
                    直通设备HA报警
                        开启HA的虚拟机，挂载SR-IOV网卡，其他主机没有相同标识设备，报警文案：主机 { .labels.hostname } 上部分开启 HA 的虚拟机因其他主机可用直通设备不足无法重建
                        开启HA的虚拟机，挂载SR-IOV网卡，其他主机有相同标识设备，但是可用数量为0，报警文案：主机 { .labels.hostname } 上部分开启 HA 的虚拟机因其他主机可用直通设备不足无法重建
                        开启HA的虚拟机，挂载SR-IOV网卡和vGPU，其他主机没有相同标识网卡，打但是有相同标识vGPU，仍会报警，报警文案：主机 { .labels.hostname } 上部分开启 HA 的虚拟机因其他主机可用直通设备不足无法重建
                        开启HA的虚拟机，挂载vGPU，其他主机没有相同标识设备，报警文案：主机 { .labels.hostname } 上部分开启 HA 的虚拟机因其他主机可用直通设备不足无法重建
                        开启HA的虚拟机，挂载vGPU，主机有相同标识设备，但是可用数量为0，报警文案：主机 { .labels.hostname } 上部分开启 HA 的虚拟机因其他主机可用直通设备不足无法重建
                        开启HA的虚拟机，挂载SR-IOV网卡和加密控制器，其他主机有相同标识设备，但是加密控制器类型不是MDEV直通，仍会报警，报警文案：主机 { .labels.hostname } 上部分开启 HA 的虚拟机因其他主机可用直通设备不足无法重建
                        开启HA的虚拟机，挂载加密控制器，其他主机没有相同标识设备，报警文案：主机 { .labels.hostname } 上部分开启 HA 的虚拟机因其他主机可用直通设备不足无法重建
                        开启HA的虚拟机，挂载加密控制器，其他主机有相同标识设备，但是不是MDEV直通。报警文案：主机 { .labels.hostname } 上部分开启 HA 的虚拟机因其他主机可用直通设备不足无法重建
                        开启HA的虚拟机，挂载SR-IOV网卡，关闭HA，报警消失
                        开启HA的虚拟机，挂载SR-IOV网卡，不满足HA报警后；其他主机设置一个相同设备标识的SR-IOV网卡，报警消失
                        开启HA的虚拟机，挂载SR-IOV网卡，不满足HA报警后；其他主机虚拟机释放一部分相同标识SR-IOV网卡满足HA要求，报警消失
                        开启HA的虚拟机，挂载vGPU，不满足HA报警后；其他主机设置一个相同设备标识的vGPU，报警消失
                        开启HA的虚拟机，挂载vGPU，不满足HA报警后；其他主机虚拟机释放一部分设备标识的vGPU，报警消失
                        开启HA的虚拟机，挂载加密控制器，不满足MDEV直通，HA报警后；其他主机将加密控制器改为MVEV直通，，报警消失
            ELF-7656 elf-vm-monitor HA：ELF HA 服务 watchdog
                暂停掉 elf-vm-monitor 进程 （kill -STOP <pid>）:300s 后 elf-vm-monitor 服务被强制重启（SIGKILL），不会生成 coredump
                模拟 leader & follower 节点的 worker 线程 hang 住，集群正常:300s 后 elf-vm-monitor 会强制重启（SIGKILL），不会生成 coredump
                模拟 leader 节点上的 worker 线程 hang 住，集群此时有其他节点故障:leader 节点 elf-vm-monitor 不会重启，直到离线节点恢复
                基于上个 case，集群节点从心跳丢失状态恢复正常，继续 hang 住 HA worker 线程:leader 节点 elf-vm-monitor 触发超时重启
                更改 /etc/elfvirt/elfvirt.conf 中的 ha_worker_watchdog_timeout 为 0:后续 worker 线程 hang 住不会触发重启
                更改 /etc/elfvirt/elfvirt.conf 中的 ha_worker_watchdog_timeout 为 100:worker 线程 hang 住，100s 会触发重启
                回归已有各功能HA场景正常
            ELF-7452:SFS 虚拟机本地重建优化
                API支持
                    ​创建虚拟机：POST /api​/v2​/vms {..., “local_ha_policy”: “destroy_and_start_if_paused”}
                    获取虚拟机：GET /api/v2/vms/{vm_uuid}
                    更新虚拟机配置： PUT /api/v2/vms/{vm_uuid} {..., “local_ha_policy”: “destroy_and_start_if_paused”}
                    手动配置虚拟机的local_ha_policy为recover；存储网故障，SFS HA依然先恢复VM（暂停状态 VM 进行关机，然后移除磁盘，最后开机）
                    手动配置虚拟机的local_ha_policy为destroy_and_start_if_paused；存储网故障，SFS HA恢复VM（暂停状态 VM ，先执行 destroy 再执行虚拟机 start 操作））
                    手动配置虚拟机的local_ha_policy不传值；存储网故障，SFS HA恢复VM（暂停状态 VM ，先执行 destroy 再执行虚拟机 start 操作））
                SFS 和SMTXOS 的新HA逻辑
                    新建虚拟机，创建多个文件系统：主机存储网故障，local_ha_policy为destroy_and_start_if_paused的虚拟机，ELF HA失败后，SFS先执行 destroy 再执行虚拟机 start 操作，本地重建成功
                    克隆虚拟机：主机存储网故障，local_ha_policy为destroy_and_start_if_paused的虚拟机，ELF HA失败后，SFS先执行 destroy 再执行虚拟机 start 操作，本地重建成功
                    虚拟机集群内冷迁移：主机存储网故障，local_ha_policy为destroy_and_start_if_paused的虚拟机，ELF HA失败后，SFS先执行 destroy 再执行虚拟机 start 操作，本地重建成功
                    虚拟机内热迁移：主机存储网故障，local_ha_policy为destroy_and_start_if_paused的虚拟机，ELF HA失败后，SFS先执行 destroy 再执行虚拟机 start 操作，本地重建成功
                    转化为虚拟机模板：再创建虚拟机：保留local_ha_policy 行为配置
                    克隆为虚拟机模板：再创建虚拟机：保留local_ha_policy 行为配置
                    导出虚拟机：再导入新虚拟机：不保留local_ha_policy 行为配置
                    创建虚拟机快照：快照回滚虚拟机：保留local_ha_policy 行为配置
                    创建虚拟机快照：快照重建虚拟机：保留local_ha_policy 行为配置
                    跨集群热迁移虚拟机：保留local_ha_policy 行为配置
                    跨集群冷迁移虚拟机：不保留local_ha_policy 行为配置
                    跨集群分段迁移虚拟机：不保留local_ha_policy 行为配置
                SFS和SMTXOS版本组合
                    老SFS和老SMTXOS版本，存储网故障，SFS HA依然先恢复VM（暂停状态 VM 进行关机，然后移除磁盘，最后开机）
                    新SFS和老SMTXOS版本，存储网故障，SFS HA依然先恢复VM（暂停状态 VM 进行关机，然后移除磁盘，最后开机）
                    老SFS和新SMTXOS版本，存储网故障，SFS HA依然先恢复VM（暂停状态 VM 进行关机，然后移除磁盘，最后开机）
                    新SFS和新SMTXOS版本，存储网故障，SFS HA先VM（暂停状态 VM ，先执行 destroy 再执行虚拟机 start 操作）
                升级路径
                    低版本SFS升级到新SFS，配合SMTXOS630：存储网故障，SFS HA先VM（暂停状态 VM ，先执行 destroy 再执行虚拟机 start 操作）
                    低版本SMTXOS升级到新SMTXOS630，配合新SFS：存储网故障，SFS HA先VM（暂停状态 VM ，先执行 destroy 再执行虚拟机 start 操作）
            ELF-7266:Kunpeng 920 异构集群热迁移兼容性改进及 AArch64 虚拟机规格调整
                AArch64 虚拟机规格调整
                    UI测试
                        编辑虚拟机vCPU最大支持512
                        创建虚拟机vCPU最大支持512
                        快照重建虚拟机vCPU最大支持512
                        克隆虚拟机vCPU最大支持512
                        编辑虚拟机内存最大支持1TiB
                        创建虚拟机内存最大支持1TiB
                        快照重建虚拟机内存最大支持1TiB
                        克隆虚拟机内存最大支持1TiB
                    新建630集群的新建虚拟机
                        创建内存的1TiB的虚拟机，正常启动
                        快照重建内存的1TiB的虚拟机，正常启动
                        导入虚拟机：内存的1TiB的虚拟机，正常启动
                        导入虚拟机模板：内存的1TiB的虚拟机，正常启动
                        编辑虚拟机：内存12GiB的虚拟机扩容到1TiB，正常启动
                        创建vCPU 数量的 512的虚拟机，正常启动
                        快照重建vCPU 数量的 512的虚拟机，正常启动
                        导入虚拟机：vCPU 数量的 512的虚拟机，正常启动
                        导入虚拟机模板：vCPU 数量的 512的虚拟机，正常启动
                        编辑虚拟机：vCPU 数量12的虚拟机扩容到512，正常启动
                        编辑虚拟机：vCPU 数量12的虚拟机扩容到513，编辑失败
                        编辑虚拟机：内存128GiB的虚拟机扩容到2TiB，扩容失败
                    512存量虚拟机升级到SMTXOS 630
                        vCPU数量15个的虚拟机升级到最新版本，依然不支持编辑到512
                        内存128GiB虚拟机升级到最新版本，依然不支持编辑到1TiB
                        vCPU数量15个的虚拟机升级到最新版本，依然不支持编辑到512；关机再开机虚拟机，支持编辑到512
                        内存128GiB的虚拟机升级到最新版本，依然不支持编辑到1TiB；关机再开机虚拟机，支持编辑到1TiB
                    620存量虚拟机升级到SMTXOS 630
                        vCPU数量15个的虚拟机升级到最新版本，依然不支持编辑到512
                        内存128GiB虚拟机升级到最新版本，支持编辑到1TiB
                AArch64 架构下同型号普通和性能版节点间支持集群内热迁移
                    鲲鹏 同一型号普通版集群内热迁移到性能版，stress压力，迁移成功
                    鲲鹏 同一型号普通版集群内热迁移到普通版，stress压力，迁移成功
                    鲲鹏 同一型号性能版集群内热迁移到性能版，stress压力，迁移成功
                    鲲鹏 同一型号普通版集群内热迁移到普通版，stress压力，迁移成功
                    鲲鹏 同一型号普通版集群内热迁移到性能版，stress压力，取消迁移成功
                    鲲鹏 同一型号普通版集群内热迁移到普通版，stress压力，存储迁移阶段，取消迁移成功
                    鲲鹏 同一型号性能版集群内热迁移到性能版，stress压力，内存迁移阶段，取消迁移成功
                    鲲鹏 同一型号普通版集群内热迁移到普通版，stress压力，取消迁移成功
                    性能、故障测试
                        512vCPU和1TiB内存的虚拟机热迁移成功
                        虚拟机使用当前节点最大可用的物理 CPU 数量，开机启动
                        512vCPU和1TiB内存的虚拟机热迁移成功，存储迁移阶段取消迁移成功
                        512vCPU和1TiB内存的虚拟机热迁移成功，内存迁移阶段取消迁移成功
                        512vCPU和1TiB内存的虚拟机热迁移成功，存储迁移阶段，源端jc重启
                        512vCPU和1TiB内存的虚拟机热迁移成功，存储迁移阶段，目标jc重启
                        512vCPU和1TiB内存的虚拟机热迁移成功，存储迁移阶段，源端libvirt 重启
                        512vCPU和1TiB内存的虚拟机热迁移成功，存储迁移阶段，目标libvirt 重启
                        512vCPU和1TiB内存的虚拟机热迁移成功，存储迁移阶段，源端kill  虚拟机qemu
                        512vCPU和1TiB内存的虚拟机热迁移成功，存储迁移阶段，源端虚拟机内部重启
                        512vCPU和1TiB内存的虚拟机热迁移成功，存储迁移阶段，源端虚拟机内部关机
                        512vCPU和1TiB内存的虚拟机热迁移成功，存储迁移阶段，源端存储网故障
                        512vCPU和1TiB内存的虚拟机热迁移成功，存储迁移阶段，目标存储网故障
                        512vCPU和1TiB内存的虚拟机热迁移成功，存储迁移阶段，源端断电故障
                        512vCPU和1TiB内存的虚拟机热迁移成功，存储迁移阶段，目标断电故障
                AArch64 架构不同型号同版本支持集群内热迁移
                    在 HUAWEI Kunpeng 920 5220 和 HUAWEI Kunpeng 920 7260 两个节点间进行,迁成功
                    在 HUAWEI Kunpeng 920 5220 和 HUAWEI Kunpeng 920 7260 两个节点间进行,存储迁移阶段，取消迁移成功
                    在 HUAWEI Kunpeng 920 5220 和 HUAWEI Kunpeng 920 7260 两个节点间进行,内存迁移阶段，取消迁移成功
                AArch64 架构不兼容的型号不支持集群内热迁移
                    在不支持的型号两个节点间进行,迁移失败报错
            ELF-7272:虚拟机热迁移支持 TLS 流量加密
                UI测试
                    集群设置-加密(Tower 480 && SMTX OS(SMTX ELF) 630)
                        SMXTOS 非vhost：集群设置 - 加密选项中增加「热迁移加密」选项，默认为未启用，点击启用成功
                        SMXTOS vhost：集群设置 - 热迁移选项中增加「热迁移加密」选项，默认为未启用，提示『Boost 模式下，仅支持内存数据加密，暂不支持磁盘数据加密』
                        SMXTELF 非vhost：集群设置 - 热迁移选项中增加「热迁移加密」选项，默认为未启用，点击启用成功
                        升级测试
                            Tower 470升级到480，SMXTOS  630非vhost：集群设置 - 热迁移选项中显示热迁移加密」选项
                            Tower 48关联SMXTOS  620升级到630非vhost：集群设置 - 热迁移选项显示热迁移加密」选项
                            Tower 470升级到480，SMXT ELF  630非vhost：集群设置 - 热迁移选项中显示热迁移加密」选项
                            Tower 480关联SMTXELF 620升级到630非vhost：集群设置 - 热迁移选项显示热迁移加密」选项
                        Tower和SMTXOS新老版本组合
                            Tower 480，SMXTOS  630非vhost：集群设置 - 热迁移选项中不显示热迁移加密」选项
                            Tower470  ，SMXTOS 630 非vhost：集群设置 - 热迁移选项中不显示热迁移加密」选项
                            Tower 480，SMXTELF  630非vhost：集群设置 - 热迁移选项中不显示热迁移加密」选项
                            Tower470  ，SMXTELF 630 非vhost：集群设置 - 热迁移选项中不显示热迁移加密」选项
                    迁移虚拟机
                        跨集群迁移-选择集群
                            OS—OS：源端启用热迁移加密，选择集群菜单中新增「热迁移数据加密」标识，标识已启用热迁移加密功能的集群，hover 展示 tooltip
                            OS—OS：源端不启用热迁移加密，选择集群不展示热迁移加密标识
                            ELF—ELF仅迁移计算：源端启用热迁移加密，选择集群菜单中新增「热迁移数据加密」标识，标识已启用热迁移加密功能的集群，hover 展示 tooltip
                            ELF—ELF跨集群迁移计算和存储：源端启用热迁移加密，选择集群菜单中新增「热迁移数据加密」标识，标识已启用热迁移加密功能的集群，hover 展示 tooltip
                            ELF—ELF仅迁移计算：源端不要启用热迁移加密，选择集群不展示热迁移加密标识
                            ELF—ELF跨集群迁移计算和存储：源端不要启用热迁移加密，选择集群不展示热迁移加密标识
                        热迁移加密选项
                            集群内热迁移
                                OS vhost集群开机虚拟机内迁移，源端开启热迁移加密：展示热迁移数据加密，已启用；Tip热迁移前，将会对内存和磁盘数据进行加密（若集群已启用 Boost 模式，磁盘数据将不进行加密）。热迁移后，将会解密。
                                ELF开机虚拟机仅迁移计算，源端开启热迁移加密：展示热迁移数据加密，已启用；Tip热迁移前，将会根据迁移类型对内存或磁盘数据进行加密。热迁移后，将会解密
                                ELF开机虚拟机仅迁移存储，源端开启热迁移加密：展示热迁移数据加密，已启用；Tip热迁移前，将会根据迁移类型对内存或磁盘数据进行加密。热迁移后，将会解密
                                OS vhost集群开机虚拟机内迁移，源端开启热迁移加密：展示热迁移数据加密，已启用；Tip热迁移前，将会对内存和磁盘数据进行加密（若集群不启用 Boost 模式，磁盘数据将不进行加密）。热迁移后，将会解密。
                            跨集群热迁移
                                OS 跨集群迁移至 ELF 且集群均已启用热迁移加密：热迁移前，将会对内存和磁盘数据进行加密（若集群已启用 Boost 模式，磁盘数据将不进行加密）。热迁移后，将会解密
                                ELF 跨集群仅迁移计算且集群均已启用热迁移加密：热迁移前，将会根据迁移类型对内存或磁盘数据进行加密。热迁移后，将会解密
                                ELF 跨集群迁移计算和存储且集群均已启用热迁移加密：热迁移前，将会根据迁移类型对内存或磁盘数据进行加密。热迁移后，将会解密
                                OS 跨集群迁移至 ELF 且目标集群不启用热迁移加密：启用状态未启用，tip目标端集群未启用热迁移加密，热迁移时将不会进行流量加密
                                ELF 跨集群仅迁移计算且目标集群不启用热迁移加密：启用状态未启用，tip目标端集群未启用热迁移加密，热迁移时将不会进行流量加密
                                ELF 跨集群迁移计算和存储且目标集群不启用热迁移加密：启用状态未启用，tip目标端集群未启用热迁移加密，热迁移时将不会进行流量加密
                    迁移选项:
                        OS vhost 跨集群热迁移至 OS:源和目标都开启热迁移加密，展示『热迁移数据机密』为已启用，tip热迁移前，将会对内存和磁盘数据进行加密（若集群已启用 Boost 模式，磁盘数据将不进行加密）。热迁移后，将会解密
                        OS 非vhost跨集群热迁移至 OS:源和目标都开启热迁移加密，展示『热迁移数据机密』为已启用，tip热迁移前，将会对内存和磁盘数据进行加密（若集群已启用 Boost 模式，磁盘数据将不进行加密）。热迁移后，将会解密
                        OS 跨集群热迁移至 OS:目标不开启热迁移加密，展示『热迁移数据加密』为未启用，tip目标端集群未启用热迁移加密，热迁移时将不会进行流量加密。
                功能测试
                    集群内迁移
                        vhost OS集群：开启加密，迁移成功，只加密内存数据，且抓包命令没有输出
                        vhost OS集群：关闭加密，迁移成功，不加密内存数据，且抓包命令有输出
                        非vhost OS集群：开启加密，迁移成功，加密存储和内存数据，且抓包命令没有输出
                        非vhost OS集群：关闭加密，迁移成功，不加密存储和内存数据，且抓包命令有输出
                        ELF集群仅迁移存储：开启加密，迁移成功，加密磁盘数据，且抓包命令没有输出
                        ELF集群仅迁移存储：关闭加密，迁移成功，不加密内存数据，且抓包命令有输出
                    跨集群迁移
                        vhost OS -OS ：开启加密，迁移成功，只加密内存数据，且抓包命令没有输出
                        vhost OS-OS：关闭加密，迁移成功，不加密内存数据，且抓包命令有输出
                        非vhost OS - OS：开启加密，迁移成功，加密存储和内存数据，且抓包命令没有输出
                        非vhost OS-OS：关闭加密，迁移成功，不加密存储和内存数据，且抓包命令有输出
                        ELF集群仅迁移计算：开启加密，迁移成功，加密内存数据，且抓包命令没有输出
                        ELF集群仅迁移计算：关闭加密，迁移成功，不加密数据，且抓包命令有输出
                        ELF集群迁移计算和存储-ELF：开启加密，迁移成功，加密内存和存储数据，且抓包命令没有输出
                        ELF集群迁移计算和存储-ELF：关闭加密，迁移成功，不加密内存和存储数据
                        ELF集群迁移计算和存储-OS：开启加密，迁移成功，加密内存和存储数据，且抓包命令没有输出
                        OS-ELF：开启加密，迁移成功，加密内存和存储数据，且抓包命令没有输出
                    升级路径
                        SMTXOS620携带存量虚拟机升级到630，开启数据加密，存量虚拟机依然不会被加密
                        SMTXOS620携带存量虚拟机升级到630，开启数据加密，存量虚拟机关机再开机，迁移会被加密
                    性能、故障测试
                        跨集群热迁移迁移500Gb数据的数据，加密方式，耗时
                        跨集群热迁移迁移100GB数据的数据，加密方式，耗时
                        OS—OS跨集群热迁移迁移1TB数据的数据，迁移到存储阶段，取消迁移成功
                        OS—OS跨集群热迁移迁移1TB数据的数据，迁移到内存阶段，取消迁移成功
                        跨集群热迁移迁移500Gb数据，加密迁移:存储迁移阶段，源端jc重启
                        跨集群热迁移迁移500Gb数据，加密迁移:存储迁移阶段，目标jc重启
                        跨集群热迁移迁移500Gb数据，加密迁移:存储迁移阶段，源端libvirt 重启
                        跨集群热迁移迁移500Gb数据，加密迁移:存储迁移阶段，目标libvirt 重启
                        跨集群热迁移迁移500Gb数据，加密迁移:存储迁移阶段，源端kill  虚拟机qemu
                        跨集群热迁移迁移500Gb数据，加密迁移:存储迁移阶段，源端虚拟机内部重启
                        跨集群热迁移迁移500Gb数据，加密迁移:存储迁移阶段，源端虚拟机内部关机
                        跨集群热迁移迁移500Gb数据，加密迁移:存储迁移阶段，源端存储网故障
                        跨集群热迁移迁移500Gb数据，加密迁移:存储迁移阶段，目标存储网故障
                        跨集群热迁移迁移500Gb数据，加密迁移:存储迁移阶段，源端断电故障
                        跨集群热迁移迁移500Gb数据，加密迁移:存储迁移阶段，目标断电故障
                        跨集群热迁移迁移500Gb数据，加密迁移:内存迁移阶段，源端存储网故障
                        跨集群热迁移迁移500Gb数据，加密迁移:内存迁移阶段，源端libvirtd故障
                        跨集群热迁移迁移500Gb数据，加密迁移:内存迁移阶段，源端掉电故障
                        跨集群热迁移迁移500Gb数据，加密迁移:内存迁移阶段，源端虚拟机内部关机故障
                        跨集群热迁移迁移500Gb数据，加密迁移:内存迁移阶段，源端kill 虚拟机qemu进程故障
            ELF-7825:HA：增加虚拟机 HA 告警
                远程重建成功告警
                    在节点上创建关机 / 暂停 / 运行中状态的虚拟机,制造节点故障,手动解决暂停虚拟机的告警
                    对同一个虚拟机制造连续的节点故障： 1. 虚拟机处于节点一，节点一故障 2.虚拟机重建到节点二后，节点一恢复，节点二故障:虚拟机产生两个重建成功的告警
                    远程重建成功的报警需要用户手动标记解决
                    远程告警失败:   本地故障恢复，本地重建成功后，远程重建失败告警消失
                    远程告警失败:   本地故障恢复，本地重建失败，远程重建告警持续存在
                    本地重建失败告警 ：即使本地重建一直失败，产生的告警也可以由用户自行标记为解决
                远程重建 HA 失败告警
                    资源调度不足调度失败： 1.将集群内所有节点的内存全部分配给虚拟机 2.对任意节点制造故障
                    在上个case基础释放其他节点内存资源，让远程重建成功
                    重建任务执行失败： 1.在节点创建运行中和暂停的虚拟机 2.修改代码让 kvm_vm_create 执行失败；3 制造节点故障
                    在上个case恢复代码，重启目的节点JC；让重建任务成功，失败告警消失，产生重建成功告警
                本地重建失败告警
                    虚拟机本地重建失败： 1.在节点创建运行中和暂停的虚拟机 2.修改代码让 kvm_vm_start 执行失败 3.通过 virsh destroy 命令将运转中和暂停虚拟机 kill 虚拟机 4.执行 3 后，立即停止 libvirtd
                    1.创建运行中和暂停的虚拟机 2.修改代码让 kvm_vm_create 失败 3.制造节点故障 4.远程重建任务失败后，恢复节点，等待 30s 左右 5. 回滚代码，让 kvm_vm_create 正常执行
                业务网络 HA 恢复成功告警
                    热迁移恢复,1.热迁移成功 2.产生成功的告警
                    重建恢复;1.重建成功 2.产生成功的告警
                    业务网络 HA 恢复成功：重建成功和热迁移成功的告警都可手动解决
                业务网络 HA 恢复失败
                    由于其他节点资源不足，热迁移恢复失败： 1.将其他节点内存占满 2.制造业务网络故障
                    在 上面的基础上恢复虚拟机，失败的告警自动解除
                    热迁移任务失败： 1.将其他节点的 libvirtd 停止 2.制造业务网络故障：1.提交热迁移任务，任务执行失败 3.产生恢复失败的告警
                    重建恢复失败： 1.通过停止 libvirtd 和其他节点资源不足均可制造重建恢复失败：产生恢复失败的告警，HA 方式为重建
                    业务网络HA调度失败：预期2min内只会产生一个失败事件
                    业务网络HA调度失败：预期2min内只会产生一个失败事件,其他主机资源不足，业务网络恢复，再次网络故障，再产生一个调度失败事件
                依赖故障测试（新引入依赖 Siren）
                    1. 停止本地节点的 siren 服务，其他节点 siren 正常工作 2.触发远程重建 HA:1.远程重建 HA 成功 2.产生成功的告警
                    1.停止所有节点的 siren 服务 2.触发远程重建 HA:1.远程重建 HA 成功，重建任务状态为成功 2. 无法产生成功的告警
                英文翻译
                    远程重建成功告警
                    远程重建调度失败事件
                    远程重建失败告警
                    本地重建失败告警
                    业务网络 HA 恢复成功告警
                    业务网络 HA 调度失败事件
                    业务网络 HA 恢复失败告警
                告警规则-用户修改全局规则和设置特例规则
                    远程 HA 重建成功告警： 1.设置全局规则：关闭 2.触发远程重建-不产生虚拟机重建成功告警
                    在上述case的基础上： 1.设置全局规则：开启，等级设置为 info 2.触发远程成功 3.产生告警后，点击解决
                    远程 HA 重建成功告警： 1.设置特例规则：关闭--不产重建成功生告警
                    在上述case基础上：1.设置特例规则：开启，等级设置为 Critical 2.触发远程成功 3.产生告警后，点击解决
                    本地重建失败告警： 1.设置全局规则：关闭--不产生虚拟机重建失败告警
                    本地重建失败告警： 1.设置特例规则：开启，等级设置为 Info
                    业务网络  HA 重建成功告警： 1.设置全局规则：关闭--不产生告警
                    业务网络  HA 重建成功告警： 1.设置特例规则：开启，等级设置为 Info
                    远程 HA 重建失败告警： 1.设置全局规则：开启，等级设置为 Info
            ELF-7670 支持调整虚拟机网卡队列长度
                集群设置
                    设置前，elf-tool elf_cluster show_txqueuelen 返回  N/A
                    命令行设置 elf-tool elf_cluster set_txqueuelen <txqueuelen>
                    同步数据 elf-tool elf_cluster sync_txqueuelen
                虚拟机设置 nic_txqueuelen
                    命令行查询 elf-tool elf_vm show_txqueuelen
                    命令行设置 elf-tool elf_vm set_txqueuelen <vm uuid> <txqueuelen>  （命令行实际调用了 api ）
                    api 设置 POST /api/v2/vms/{vm-uuid}/update_nic_txqueuelen
                    虚拟机设置 txqueuelen = 2000 后添加网卡， 开机关机操作，网卡配置都时 2000
                set_txqueuelen 后虚拟机变更
                    快照重建、模版、克隆都不保持 txqueuelen，按目标集群默认值生效
                    虚拟机跨集群迁移（热、冷、分段）, 不保持 txqueuelen， 按目标集群默认值生效
                    集群内热迁移，所有网卡保持 txqueuelen = 2000
                虚拟机 vnet 检查
                    配置并开机后，虚拟机所属主机对应  /sys/class/net/vnetX/tx_queue_len 的内容和 Actual Txqueuelen 一致
            ELF-7810 支持虚拟机粒度对磁盘属性 disk_options 进行配置
                集群设置
                    配置文件  /etc/libvirt/qemu.conf
                虚拟机设置（优先使用）
                    创建虚拟机，不允许设置 ( 默认 3 个字段都是 None  )
                    开机虚拟机不允许设置， API 返回  PRECHECK_VMS_STATE_UNMATCH
                    关机虚拟机（含所有总线磁盘）elf-tool elf_vm set_disk_options 设置成功
                    关机虚拟机 POST /api/v2/vms/{$vm_uuid}/update_disk_options
                    GET /api/v2/vms/{vm_uuid} ， GET /api/v2/vms 返回信息增加 disk_options
                    查看配置 查看 elf-tool elf_vm show_disk_options
                升级场景
                    620 升级到 630，升级后虚拟机补齐 3 个字段（都是 None）, 预期可以开机成功
                    手动补齐字段的命令行 elf-tool upgrade_cluster post_update_cluster
                参数传递
                    创建虚拟机
                        创建空白虚拟机，disk_options 的子项默认值 None
                        虚拟机克隆为虚拟机，disk_options 的子项默认值 None
                        OVF 导入 ，disk_options 的子项默认值 None
                        模版克隆虚拟机，disk_options 的子项默认值 None
                        模版转化虚拟机，disk_options 的子项默认值 None
                        从快照重建虚拟机，disk_options 的子项默认值 None
                    模版
                        虚拟机克隆为模版， 模版不包含 disk_options
                        虚拟机转化为模版， 模版不包含 disk_options
                    快照
                        创建快照，快照 api 不包含 disk_options
                        快照和虚拟机的 disk_options 配置不同时回滚，回滚成功后虚拟机 disk_options 不变（不会覆盖为快照的配置）
                    编辑
                        开机虚拟机热添加 virtio 磁盘，disk_options 磁盘配置不变
                        开机虚拟机已有 scsi 磁盘，在热添加 scsi 磁盘，disk_options 磁盘配置不变
                        开机虚拟机不包含 scsi 磁盘，热添加 scsi 磁盘时，disk_options 磁盘配置按最新配置生效
                    迁移
                        集群内热迁移，磁盘配置保持一致
                        跨集群热迁移，磁盘配置保持一致
                        跨集群分段、冷迁移， 不支持保留配置
                虚拟机内部检查
                    disk_options 对应虚拟机内部配置检查
            ELF-7840 通过命令行为虚拟机开启 iothread
                命令行设置 iothread
                    设置  elf-tool elf_vm update_iothread  $vm_uuid --num $iothread_num
                    查询 elf-tool elf_vm show_iothread $vm_uuid
                数据库设置
                    虚拟机 POST /api/v2/vms/{vm_uuid}/update_iothread
                    GET /api/v2/vms/{vm_uuid} ， GET /api/v2/vms 返回信息增加 iothread
                集群升级
                    升级后，虚拟机都包含  {“iothread”: {“num”: 0}}
                参数传递
                    虚拟机创建入口，iothread 默认关闭（ 0 ）
                        创建空白虚拟机
                        虚拟机克隆为虚拟机
                        OVF 导入
                        模版克隆虚拟机
                        模版转化虚拟机
                        从快照重建虚拟机
                    模版
                        从虚拟机克隆模版， 模版 api 不包含  iothread
                        从虚拟机转化为模版， 模版 api 不包含  iothread
                    快照
                        创建快照，快照 api 不包含 iothread
                        快照和虚拟机的 iothread 配置不同时回滚，回滚成功后虚拟机 disk_options 不变（不会覆盖为快照的配置）
                    迁移
                        集群内热迁移，iothread 配置保持一致
                        跨集群热迁移，iothread 配置保持一致
                        跨集群分段、冷迁移， 不支持保留配置， 迁移后 iothread 默认关闭（ 0 ）
                虚拟机检查
                    虚拟机内部向 virtio/scsi 盘写入数据，虚拟机所属主机 top 观察到 iothread 存在负载
                    检查虚拟机 qemu 进程， 包含 iothread
            【revert】ELF-7977 虚拟机粒度配置网卡队列数 queues
                虚拟机设置网卡队列数
                    开机虚拟机设置， 返回 PRECHECK_VMS_STATE_UNMATCH
                    虚拟机设置  elf-tool elf_vm set_nic_queues <vm uuid> <num>,  设置 num = 3， 检查设置成功
                    虚拟机设置  elf-tool elf_vm set_nic_queues <vm uuid> <num>,  设置 num = 0， 检查设置成功
                    虚拟机设置  elf-tool elf_vm set_nic_queues <vm uuid> <num>,  设置 num  不符合预期范围或类型， 检查设置失败
                参数传递
                    创建虚拟机，  不允许设置， 保持 vCPU 数量自适应
                        创建空白虚拟机
                        快照重建虚拟机
                        虚拟机克隆为虚拟机
                        从虚拟机模版创建新虚拟机
                        OVF 导入虚拟机
                    虚拟机操作
                        关机设置队列后，虚拟机开机， 此时网卡按新队列生效
                        虚拟机集群内迁移， 网卡队列数不变
                虚拟机内部检查
                    Linux 虚拟机设置后，在虚拟机内部检查
            ELF-7455  对接亚信无代理杀毒
                集群设置
                    集群 - 设置
                        导航菜单增加【安全】，子项包含 ：深度安全防护
                        其中【深度安全防护】有展示约束
                    深度安全防护下面检查【深度安全防护】设置
                        提示文案
                        提示文案点击 remove icon【右上角 X 】后不再提示
                        描述文案
                        设置深度安全防护为 开启， 点保存
                        设置深度安全防护为 关闭， 点保存
                        开关未开启时，页面只展示【深度安全防护】设置项
                        开关开启后，页面增加展示部署引导模块
                        开关开启后，不满足如下条件时，禁用按钮并展示原因，提示文案
                    【深度安全防护】设置
                        启用【深度安全防护】
                            集群未开启状态，开启成功
                            Tower UI 已同步到集群已开启防病毒， UI 禁止再次做开启
                        关闭【深度安全防护】
                            集群未开启状态，没有关闭入口
                            集群 SVM 未卸载， 不允许集群关闭【深度安全防护】
                            集群关联到 ER 的导流功能，不允许集群关闭【深度安全防护】
                            集群 SVM 已卸载且未关联到 ER 导流功能， 关闭【深度安全防护】成功
                            自动删除 SVM 放置组  Anti-Malware-Placement-Group
                        新关联集群行为
                            新集群不存在 SVM, 则 Tower 默认记录集群未开启【深度安全防护】
                            新集群如存在 SVM, 则 Tower 默认记录集群已开启【深度安全防护】并标记 SVM 放置组(不重复创建)
                            Tower 关联集群进行中（关联任务未结束） - 设置启用【深度安全防护】， 预期不允许设置
                    Tower 移除集群
                        已开启安全防护，未导入 SVM 模版的集群，移除集群成功
                        最后一个  SVM 模版关联模版的集群，移除集群时应提示移除后 SVM 模版将不可用
                        已部署 SVM 虚拟机的集群，未关联 ER 导流的集群， 不允许做移除集群，有提示
                        已关联 ER 导流的集群，不允许做移除集群，有提示
                SVM 模版版本检查
                    OVF 物料检查（OVF 和 vmdk 文件名检查），预期符合亚信命名要求
                    OVF， vmdk  导入集群作为 SVM 模版，预期导入成功
                    SVM 模版创建多个 SVM 虚拟机， 检查 SVM 虚拟机配置
                安全防护服务虚拟机（SVM）
                    部署状态展示
                        默认部署状态和部署流程
                            模块名称位置可展开收起部署流程展示，已部署时默认收起，未部署和部署中默认展开
                            集群所有主机都不存在 SVM 时展示【未部署】
                            集群部分主机存在  SVM 时展示【部分未部署】
                            集群所有主机都存在 SVM 时展示【已部署】
                        展示部署流程中 2 个步骤的实际状态
                            步骤1：导入安全防护虚拟机模板， 备注文案： 导入特定 OVF 及 VMDK  文件。
                            步骤2：创建安全防护虚拟机， 备注文案：从安全防护虚拟机模板为主机创建安全防护虚拟机。
                            展示每个步骤的状态（未开始，成功）
                            Tower 也没有 SVM OVF  模版， 步骤1 完成前，步骤2 的【创建】按钮是禁用的
                            步骤1 完成后，步骤1 【导入】和步骤2【创建】都可以点击
                            Tower 存在 SVM 模版（不管所属集群），步骤1 都展示成功
                            集群  SVM 为已部署时， Tower 即使没有  SVM 模版 也会展示 步骤1 成功
                        展示导入操作按钮和创建操作按钮
                            点击【导入】打开【导入虚拟机模版】弹窗，在基本信息步骤中展示【作为安全防护虚拟机（SVM）模版】
                            点击【创建】打开【创建安全防护虚拟机】弹窗
                            已导入 【SVM OVF 模版】的情况下，再次点击【导入】可以再次导入，允许导入多个 SVM 模版（不同模版有重名校验）
                            集群每个主机已部署 SVM 的情况下，再次点击【创建】，在第一个页面因放置组策略不满足被阻止部署
                            一个集群导入 SVM 模版， 另一个集群部署 SVM,  预期可以部署
                    OVF 导入 SVM  模版
                        SVM 模版 OVF 维护
                            发布前亚信会提供支持的版本号
                        Tower UI
                            UI 集群 - 设置 - 安全 - 深度安全防护页 - 部署安全防护虚拟机（SVM）步骤一 （导入安全防护虚拟机模版）
                            导入弹窗 - 选择文件页面
                            导入弹窗 - 基本信息页面
                            导入弹窗 - 计算资源页面
                            导入弹窗 - 磁盘页面
                            导入弹窗 - 网卡页面
                            导入弹窗 - 其他配置页面
                            导入弹窗 - Cloud-init：自动设置为 cloud_init_supported
                            安全防护模版详情
                            Tower 内容库模版的 OVF 常规的导入不支持设置【 SVM 模板】
                            错误校验
                                导入  SVM OVF 模版，配置已存在的模版名称，预期 UI 检查重新提示需要修改名称
                                导入 SVM  OVF 模版，选择不满足部署 SVM 的集群（如低于 630 的集群）【产品不约束所属集群选项，允许选不支持的集群】
                        导入 SMTXOS 集群
                            仅 SMTXOS 630+ 支持导入 SVM 模版
                            ACOS、ARM、vhost 集群不展示 UI: 集群 - 设置- 安全 - 深度安全防护， ELF 不约束
                        导入 SMTXELF 集群
                            导入 SMTXELF 630 + ZBS562 集群， 选 x86 架构
                            导入 SMTXELF 630 + ZBS570 集群， 选 x86 架构
                            导入 SMTXELF 630 + OS630 集群， 选 x86 架构
                            导入 SMTXELF 630 + ZBS570 集群， 选 arrch64  架构
                        SVM 模版使用
                            仅部署 SVM 时可以选择  SVM 模版
                            从内容库模版创建虚拟机时无法选择 SVM 模版
                        多次导入
                            多次导入 OVF SVM 模版，导入成功
                    部署 SVM
                        Tower UI
                            操作入口
                                UI 集群 - 设置 - 安全 - 深度安全防护页 - 部署安全防护虚拟机（SVM）步骤二【创建安全防护虚拟机】
                            SVM 模版选择
                                Tower  - 内容库 SVM 模版 - 不展示【创建虚拟机】
                                创建 SVM 的弹窗中，模版菜单会展示 Tower 中所有的 SVM 模版， 按名称选择可用版本
                            【创建安全防护虚拟机】弹窗检查
                                弹窗不同页面展示信息汇总
                                    基本信息页面
                                    计算资源页面
                                    磁盘页面
                                    网络设备页面
                                    初始化配置 - 和普通虚拟机一致
                                    其他配置页面
                                基本信息页面
                                    SVM 模版名称包含 version， 来区分不同模版的版本差异
                                    默认参数部署，部署成功
                                    集群每个主机都有  SVM 的情况下，再次部署 SVM,  预期不允许部署，UI 提示不符合放置组要求
                                    集群部分部署，再次部署 SVM,  数量输入大于剩余可部署数量，UI 提示不符合放置组要求
                        创建到 SMTXOS 集群
                            不同部署时机
                                SMTXOS 集群第一次部署等于节点主机数的 SVM
                                SMTXOS 集群第一次部署 1 个 SVM， 第二次部署剩余全部的 SVM
                                SMTXOS 集群扩容节点后部署 SVM
                            不同集群部署
                                SMTXOS - intel x86 el7  非 vhsot 集群，部署 SVM
                                SMTXOS - intel x86 oe  非 vhsot 集群，部署 SVM
                                SMTXOS - hygon x86 oe  非 vhsot 集群，部署 SVM
                                SMTXOS - hygon x86 tl3  非 vhsot 集群，部署 SVM
                                SMTXOS - vhost 转 非 vhost 集群， 部署 SVM
                                SMTXOS - 非 vhost 转 vhost 集群， 隐藏 UI 入口【集群 - 设置- 安全 - 深度安全防护】
                                ELF 侧禁止部署 SVM 到 vhost ， arm ， 非 smartx 产品
                            异常情况
                                SMTXOS 集群第一次批量部署 SVM 时， 部分 SVM 因主机内存不足开机失败
                                Tower1 对 cluster1 部署 1 个 SVM,  Tower2 对 Cluster1 部署 1 个 SVM, 预期 2 个都部署成功，放置组使用同一个
                            不同模版来源
                                部署 SVM 时【模版】选择其他 SMTXOS 集群模版
                                部署 SVM 时【模版】选择其他 SMTXZBS 集群模版
                        创建到 SMTXELF 集群
                            不同集群部署
                                SMTXELF - intel x86 oe  部署 SVM
                                SMTXELF - hygon x86 oe  部署 SVM
                                SMTXELF + 单存储集群， 部署 SVM
                                SMTXELF + 多存储集群， 部署 SVM
                                部署 SVM 时【关联存储集群】选择 SMTXOS 集群
                                部署 SVM 时【关联存储集群】选择 SMTXZBS 集群
                            不同模版来源
                                部署 SVM 时【模版】选择其他 SMTXOS 集群模版
                                部署 SVM 时【模版】选择其他 SMTXZBS 集群模版
                            异常情况
                                部署 SVM 时候， 关联存储失联,  任务中心创建 SVM 的任务失败，提示： 连接存储服务失败
                        部署 SVM 后关联资源检查
                            集群已创建一个放置组，约束 SVM 必须放置在不同的主机上
                            检查配置文件  /etc/elfvirt/vs.conf
                            SVM 已分配好共享内存和串口设备
                            SVM 支持的 GVM 规格， 集群内每个主机是均等的
                            部署 SVM 后分配的共享内存预计占用 800M 左右， 需要配置对应 cgroup 做预留
                        SVM 模版和 SVM 虚拟机不同配置检查
                            基本信息
                                设置超长(如 255 字符)名称部署 SVM
                                设置超长虚拟机描述(如 3000 字符)名称部署 SVM
                                部署 SVM 页面设置虚拟机组和更多用户（如包含虚拟机使用者用户），部署 SVM 成功
                            计算资源
                                配置 cpu 独占， 部署 SVM
                                增加内存， 配置 SVM
                                检查 vcpu 内存 修改小于默认值部署， 检查 SVM 运行情况
                                配置 vcpu 较低的份额， 部署 SVM 观察运行情况
                            网卡
                                SVM 模版配置网卡启用，部署 SVM 时【管理网卡】- 配置启用
                                SVM 模版配置网卡禁用，部署 SVM 时【管理网卡】- 配置启用
                                SVM 模版配置 E1000 网卡， 部署 SVM 时【管理网卡】- 网卡模式 - E1000
                                SVM 模版配置 E1000 网卡， 部署 SVM 时【管理网卡】- 网卡模式 - VIRTIO
                                SVM 模版配置 VIRTIO 网卡， 部署 SVM 时【管理网卡】- 网卡模式 - E1000
                                SVM 模版配置 VIRTIO 网卡， 部署 SVM 时【管理网卡】- 网卡模式 - VIRTIO
                                SVM 模版最后一个网口不启用镜像模式，部署 SVM 时【管理网卡】- 不开启镜像模式
                                SVM 模版最后一个网口不启用镜像模式，部署 SVM 时【管理网卡】- 开启镜像模式
                                SVM 模版最后一个网口启用镜像模式，部署 SVM 时【管理网卡】- 不开启镜像模式
                                SVM 模版最后一个网口启用镜像模式，部署 SVM 时【管理网卡】- 开启镜像模式
                                SVM 模版默认保留 3 个网口，部署 SVM 时【管理网卡】是最后一个，前面的都是导流网口，
                                SVM 模版增加网口数量（如 5 个），部署 SVM 时【管理网卡】是最后一个，前面的都是导流网口
                                SVM 模版删除部分网口，部署 SVM， 预期无法部署， 或者模版不允许删除网卡？
                                SVM 模版保持默认配置， 部署 SVM 时 - 管理网卡 - 虚拟机网络 - 选择 vlan access 网络
                                SVM 模版保持默认配置， 部署 SVM 时 - 管理网卡 - 虚拟机网络 - 选择 vlan trunk 网络
                                SVM 模版保持默认配置， 部署 SVM 时 - 管理网卡配置 vnic qos， 部署  SVM
                            磁盘
                                修改磁盘名称
                                设置磁盘总线 - VIRTIO， 部署 SVM
                                设置磁盘总线 -  SCSI， 部署 SVM
                                设置磁盘总线 -  IDE， 部署 SVM
                            固件
                                部署 SVM 时【开机选项 - 固件】选择 BIOS
                                部署 SVM 时【开机选项 - 固件】选择 UEFI
                            随主机开机
                                部署 SVM 时【随主机开机】开启
                                部署 SVM 时【随主机开机】不开启
                            创建方式
                                【创建方式】快速克隆创建， 部署 SVM
                                【创建方式】完全拷贝克隆创建， 部署 SVM
                            初始化配置
                                管理网口配置【静态 ip】【ip、网关、掩码 不匹配】， 预期网卡位置校验不通过
                                管理网口配置【静态 ip】【正确配置】， 部署 SVM
                                管理网口配置【启用网卡 DHCP 】， 部署 SVM
                                管理网口配置【不配置 】， 部署 SVM
                                初始化配置 - 设置主机名， 默认账号密码， dns， 用户数据
                            其他配置页面
                                【创建完成后自动开机】勾选， 部署 SVM
                                【创建完成后自动开机】不勾选， 部署 SVM
                    卸载 SVM
                        SMTXOS intel 非 vhost 集群，卸载全部  SVM  成功
                        SMTXOS intel 非 vhost 集群，部署 SVM 后转集群为开启 vhost，可以再次卸载 SVM
                        SMTXELF intel 集群，卸载全部  SVM  成功
                        卸载 SVM 后关联资源检查
                    SVM 虚拟机操作
                        编辑
                            编辑网卡
                                编辑网卡弹窗有提示文案
                                编辑约束
                                管理网卡修改 ip
                                管理网卡配置 qos
                                管理网卡修改为镜像模式
                        放置组
                            SVM 关联一个放置组，配置必须放置在不同的主机上
                        开机
                            开机弹窗文案检查
                            SVM 虚拟机启动成功， 只能在当前主机开机（放置组约束）
                        关机
                            关机弹窗文案检查
                            普通关机，关机成功
                            强制关机，关机成功
                            关机时， disconnect vs-controller 失败时（stop 服务）， 关机任务成功
                        暂停
                            暂停弹窗文案检查
                        重启
                            重启弹窗文案检查
                        迁移
                            UI 没有操作入口
                        DRS
                            有放置组约束无法迁移， 无法迁移
                        HA
                            SVM 虚拟机不允许开启 HA
                        移动到回收站
                            不支持移动到回收站
                        永久删除
                            有 GVM 关联有 ER 导流关联,  不允许删除
                            只有 ER 导流关联， 不允许删除
                            有 GVM 关联,  不允许删除
                            虚拟机已关机，且 节点上没有 GVM 没有 ER 留空关联，满足条件，删除 SVM 虚拟机成功
                            删除共享内存失败（只能修改代码制造场景），返回 JOB_ASIAINFO_SVM_SHM_DELETE_FAILED
                            关机 SVM 和 虚拟机开启 AM 同时操作时，预期结果未其中一个失败
                        快照
                            创建编辑快照计划，选择虚拟机的位置， 禁止选择 SVM 虚拟机，提示文案
                            创建编辑备份计划，选择虚拟机的位置， 禁止选择 SVM 虚拟机，提示文案
                            创建编辑复制计划，选择虚拟机的位置， 禁止选择 SVM 虚拟机，提示文案
                        OVF
                            仅支持导入 OVF  SVM 模版， 不支持导入 SVM 虚拟机
                    SVM 虚拟机权限控制
                        虚拟机列表
                            列表的多虚拟机选中框被禁用
                            列表更多操作， 部分保留，部分隐藏
                        虚拟机详情
                            更换虚拟机 icon 并展示字段「安全防护虚拟机（SVM）
                        虚拟机详情操作栏
                            保留： 打开终端、关机、重启、暂停、部分编辑项
                            不允许创建快照， 实际隐藏创建入口， ELF API 校验报错（不触发异步任务）error code
                            不允许克隆未模版， 实际隐藏创建入口，ELF API 校验报错同上
                            不允许转化为模版， 实际隐藏创建入口，ELF API 校验报错同上
                            不允许克隆新虚拟机， 实际隐藏创建入口， ELF API 校验报错同上
                            不允许迁移， 实际隐藏创建入口， ELF API 有配置不可迁移字段
                            不允许编辑高可用，  实际隐藏创建入口， ELF API 不受传入参数约束，默认设置为 ha = false
                            不允许编进防病毒，Tower 隐藏， ELF API 也不允许
                            不允许编辑放置组， 实际隐藏创建入口
                            不允许产看网络链路，实际隐藏创建入口
                        虚拟机详情操作栏 - 更多项
                            支持: 隔离、查看网络流量、导出、挂载虚拟机工具映像、移至回收站
                        虚拟机详情 -  tag 切换项
                            详情 tab 展示， 部分保留，部分隐藏
                        虚拟机详情 tag  - 详情
                            基本信息 - 隐藏编辑入口： 高可用、防病毒、虚拟机放置组
                            网卡设备 - nic0, nic1 导流网卡不展示网卡信息，不支持展开， 管理网口支持展开， 包含展示【深度包检测】
                            隐藏 USB、加密控制器、GPU 的展示
                        虚拟机详情 tag - 监控
                            计算性能、存储性能、网络流量，都正常展示
                        虚拟机详情 tag - 事件
                            正常记录用户事件和系统事件
                        虚拟机详情 tag - 标签
                            可正常 关联、取消 标签
                    SVM 虚拟机故障
                        系统 crash， 无法提供防护能力， 仅 DSM 报警
                        磁盘只读， 无法提供防护能力，仅 DSM 报警
                        磁盘读写慢（比如集群缓存击穿的情况）， 仅 DSM 管理， 可能有报警
                        CPU 等待就绪较高（比如超分较大的情况），仅 DSM 管理， 可能有报警
                        重启， 防护能力会中断一段时间
                        关机，无法提供防护能力，有警告
                        SVM 关联的导流网卡异常，影响主机导流功能时，触发告警
                被防护虚拟机（GVM）
                    Tower UI 变更
                        在 集群开启防病毒后，增加项
                            虚拟机详情 - 操作项 - 编辑 - 增加【编辑防病毒】和【编辑深度包检测】编辑项
                            普通虚拟机详情 - 详情 tab - 基本信息 - 增加【防病毒】和【深度包检测】配置展示和编辑入口
                            虚拟机详情 tab - 网卡设备 - 网卡展开详情 - 增加展示【深度包检测】
                            虚拟机列表 - 批量操作项 - 编辑 - 增加【编辑防病毒】和【编辑深度包检测】编辑项
                            虚拟机列表 - 增加字段
                            虚拟机列表 - 【防病毒】和【深度包检测】字段支持排序和高级筛选
                        【防病毒】状态
                            虚拟开启 AM 后【虚拟机详情 tab - 基本信息 - 防病毒】展示为已开启
                            已启用未生效， 展示提示
                        【深度包检测】( DPI ) 状态
                            只要有一个网卡开启，【虚拟机详情 tab - 基本信息 - 深度包检测】就展示已启用,
                            对应网卡的网卡展开详情【虚拟机详情 tab - 网卡设备 - 网卡展开详情 - 深度包检测】展示已启用
                            已启用未生效，展示提示
                        系统服务虚拟机
                            系统服务虚拟机（含 SVM）隐藏【防病毒】和【深度包检测】编辑入口， ( ELF 后端未做限制 )
                    编辑防病毒 ( AM )
                        设置 AM
                            创建时不支持设置 AM， 仅支持编辑
                            已启用 AM 的虚拟机克隆为新虚拟机，克隆时不支持设置 AM， 新虚拟机不包含 AM 字段
                            已启用 AM 的虚拟机克隆、转化 模版，模版不包含 AM 字段， 克隆转化弹窗有文案提示
                            已启用 AM 的虚拟机创建快照，快照不包含 AM 字段
                            从模版在创建虚拟机，创建时不支持设置 AM
                            从快照重建虚拟机，创建时不支持设置 AM， 创建快照弹窗有文案提示
                            OVF 导出,   OVF 不包含 AM 字段， 有文案提示
                            OVF 导入， 不支持设置 AM
                            未配置状态，有相关字段：anti_malware_enabled ： false
                        UI 弹窗检查
                            单个虚拟机编辑虚拟机防病毒弹窗
                                可以启用时
                                无法启用时
                                单个关闭
                            批量编辑虚拟机防病毒弹窗
                                默认信息
                                选择【启用防病毒】
                                选择【关闭防病毒】
                        虚拟机启用 AM
                            开启成功
                                需要满足条件, 启用成功
                            开启失败
                                虚拟机所属主机没有开机 SVM,  不允许开启 AM， API 开启会返回 PRECHECK_VMS_ENABLE_AM_INVALID_STATE
                                关机虚拟机，不允许开启 AM
                                未安装 VMTools， 不允许开启 AM
                                VMTools < 4.1.0， 不允许开启 AM
                                VMTools 4.1.0+  非运行状态，不允许开启 AM
                                超过节点允许开启 AM 的虚机数，不允许开启 AM， API 开启会返回 JOB_PORT_NOT_ENOUGH_FOR_ASIAINFO_AM_DEVICE
                                虚拟机已经开启 AM 时不允许再次开启 AM， ELF API 有约束
                                参数不满足（ product != asiainfo）返回 PRECHECK_VMS_AM_UNKNOWN_PRODUCT
                                满足条件，但是虚拟机 domain 异常（不是开机，比如操作中），返回 JOB_VM_ENABLE_AM_INVALID_STATE
                            不同来源的虚拟机启用 AM
                                新创建开机虚拟机, 预期启用成功
                                【残留 DS 驱动的虚拟机】已启用 AM 的虚拟机克隆新虚拟机, 预期启用成功
                                已启用 AM 的虚拟机克隆为模版，再从模版创建虚拟机, 预期启用成功
                                已启用 AM 的虚拟机创建快照，再从快照重建虚拟机, 预期启用成功
                                已启用 AM 的虚拟机， OVF 导出再导入, 在开启 AM, 预期启用成功
                                已启用 AM 的虚拟机在关机后禁用 AM, 开机后再次启用 AM, 预期启用成功
                        虚拟机禁用 AM
                            禁用成功
                                SVM 状态正常，开机 GVM 禁用 AM 成功
                                SVM 状态异常（如关机）， 禁用 AM 成功
                            禁用失败
                                已禁用 AM 的虚拟机再次禁用预期失败， ELF API 报错 PRECHECK_VMS_DISABLE_AM_INVALID_STATE
                                参数不满足（ product != asiainfo）返回 PRECHECK_VMS_AM_UNKNOWN_PRODUCT
                                满足条件，但是虚拟机 domain 异常（操作中，迁移中），返回 JOB_VM_DISABLE_AM_INVALID_STATE
                                vs-controller  stop， 禁用失败
                                SVM 状态正常，禁用 AM 失败 ， 预期：已删除的设备不会回退
                    编辑深度包检测（DPI）
                        设置 DPI
                            创建时不支持设置 DPI， 仅支持编辑
                            已启用 DPI 的虚拟机克隆为新虚拟机，克隆时不支持设置 DPI， 新虚拟机不包含 DPI 字段
                            已启用 DPI 的虚拟机克隆、转化 模版，模版不包含 DPI 字段
                            已启用 DPI 的虚拟机创建快照，快照不包含 DPI 字段
                            从模版在创建虚拟机，创建时不支持设置 DPI
                            从快照重建虚拟机，创建时不支持设置 DPI  - 创建快照时会有文案提示不保留 DPI
                            OVF 导出,   OVF 不包含 DPI 字段
                            OVF 导入， 不支持设置 DPI
                            虚拟机未配置 DPI 对应字段 dpi_enabled ： false， 未配置 AM 时的字段是 anti_malware_enabled： false
                        UI 弹窗检查 （Tower 维护是否开启字段）
                            单个编辑
                                可以启用时
                                无法启用时
                                单个关闭
                            批量编辑
                                批量编辑弹窗
                        启用 DPI
                            1 个虚拟机仅包含 1 个 vlan 网卡启用 DPI 成功
                            1 个虚拟机仅包含 2 个网卡，仅 1 个网卡启用 DPI
                            1 个虚拟机仅包含 3 个网卡，其中 1 个网卡是多 ip， 1 个网卡有 1 个 ip ,  1 个网卡对应网络名称超长且没有 ip，全部网卡开启 DPI
                            1 个虚拟机仅包含 2 个网卡，无可选网卡， 启用 DPI， 无法启用，有提示
                            批量启用， 1 个虚拟机没有网卡支持卡其 DPI，1 个虚拟机 部分虚拟机支持开启 DPI, 1  个虚拟机全部网卡支持开启 DPI
                        禁用 DPI
                            1 个虚拟机仅包含 2 个网卡，仅 1 个网卡禁用 DPI
                            1 个虚拟机仅包含 2 个网卡，全部网卡禁用 DPI
                        虚拟机限制，禁止启用 DPI
                            虚拟机所属主机没有运行中的 SVM, 不支持启用 DPI , 有文案提示
                            虚拟机状态不是运行中，不支持启用 DPI , 有文案提示
                            虚拟机所有网卡的虚拟机网络，都没有关联 ER 导流
                            虚拟机网卡没有满足 vlan
                            虚拟机 0 网卡，不支持启用 DPI , 有文案提示
                        网卡类型限制，禁止启用 DPI
                            虚拟机网卡不包含 vlan 网卡，如网卡为：PCI 直通、 SR-IOV 网卡、VPC 网卡， 不支持启用 DPI , 有文案提示
                            虚拟机网卡都开启镜像模式，不支持启用 DPI , 有文案提示
                            虚拟机网卡未关联 ER 导流网卡， 不支持启用 DPI , 有文案提示
                    GVM 虚拟机操作
                        状态变更
                            关机、强制关机
                                虚拟机 crash， 普通关机超时失败
                                虚拟机 crash， 强制关机成功
                                stop vm-security-controller， 虚拟机关机成功
                            开机
                                自动调度开机成功
                                指定主机开机成功
                                批量开机成功
                                单个开机，因 AM 不支持开机失败时，任务提示：当前虚拟机已启用防病毒功能，目标主机不满足功能启用要求。
                                单个虚拟机开机，因 DPI 不满足条件（如迁移到网口未关联导流的主机），实际可以开机，只是 DPI 不生效
                                AM 和 DPI 都不满足的情况下，和 AM 不满足一致
                                批量开机， 部分虚拟机因 AM 不支持开机失败时，任务提示：当前虚拟机已启用防病毒功能，目标主机不满足功能启用要求。
                                GVM 虚拟机开机时， vs-controller 服务不可用（stop），GVM 开机失败
                            重启，强制重启 = 关机再开机
                                GVM 重启成功
                                GVM 强制重启成功
                        编辑
                            编辑网卡 - 切换网络
                                已开启 DPI 的网卡， 编辑切换虚拟机网络时， 可选虚拟机网络菜单禁用未关联 ER 导流的虚拟机网络
                                已开启 DPI 的网卡，不允许编辑开启镜像模式， 有文案：虚拟网卡已启用深度包检测功能，不支持开启镜像模式。
                                未开启 DPI 网卡， 编辑切换虚拟机网络为已关联 ER 导流的 VDS， 切换成功
                            热添加网卡
                                vs-controller 服务不可用（stop）, 添加网卡失败
                                vs-controller 服务可用( running）, 添加网卡成功
                            热删除网卡
                                vs-controller 服务不可用（stop）, 删除网卡失败
                                vs-controller 服务可用( running）, 删除网卡成功
                        删除
                            删除成功， 释放关联设备
                        HA
                            编辑 HA 配置
                                单个虚拟机编辑高可用
                                批量虚拟机编辑高可用
                            HA 任务
                                源端主机 vs-controller 服务不可用（stop）,  HA 成功， 源端主机残留数据有定时任务处理
                                目标主机 vs-controller 服务不可用（stop）, HA 会失败
                            HA 优先调度 AM - 目标虚拟机关闭 AM 的场景
                                目标主机未配置 SVM
                                目标主机已配置 SVM，但  SVM 已关机
                                目标主机已配置 SVM， 但 GVM 规格已用完
                            HA 重建因 DPI 不满足
                                HA 重建因 DPI 不满足（如网口未关联到导流）导致没有可选目标主机时， 会 HA 重建成功 ， 最终目标主机虚拟机 DPI 不生效
                        迁移
                            集群内迁移
                                SMTXOS 集群内冷迁移， 保持 AM 和 DPI 设置，迁移成功 （迁移后虚拟机开机时单独按开机条件提示）
                                SMTXOS 集群内热迁移到【目标主机未配置 SVM】的主机， 迁移失败有提示
                                SMTXOS 集群内热迁移到【目标主机已配置 SVM，但  SVM 未开机】的主机， 迁移失败有提示
                                SMTXOS 集群内热迁移到【目标主机已配置 SVM， 但 GVM 规格已用完】的主机， 迁移失败有提示
                                源端 vs-controller 服务不可用（stop）， 热迁移成功， 源端残留数据有定时任务处理
                                目标端 vs-controller 服务不可用（stop）， 热迁移失败
                                迁移触发时  SVM 是开机的，但是迁移任务执行过程中 SVM 关机了， 此时可能迁移任务不会失败，目标虚拟机可能 AM 、DPI 不生效
                                目标主机不满足 DPI 时， 迁移成功，虚拟机在目标主机 DPI 不生效
                                SMTXELF 仅迁移存储允许（保留 AM DPI 配置）
                            跨集群迁移
                                【跨集群热迁移计算存储】 和 【跨集群热迁移仅迁移计算】，对应迁移弹窗，提示迁移会自动关闭 AM 和 DPI， 可以迁移成功
                                跨集群【分段/冷】迁移，迁移后不保留防病毒开关，需重新配置， 迁移弹窗有提示文案
                            跨集群迁移（热、分段、冷），目标虚拟机配置开启 AM 和 DPI
                                迁移目标虚拟机， 开启 AM 成功
                                迁移目标虚拟机， 开启 DPI 成功
                                主机 vs-controller stop ， 开启 AM 失败
                        OVF
                            GVM 导出再导入， 源导流网卡变更为普通网卡， AM, DPI 不会保留， 虚拟机内部 DS 驱动不会被定时任务清理
                        快照
                            创建快照弹窗，提示不包含xxx
                            创建编辑快照计划，选择虚拟机的位置， 新增文案提示不包含xxx
                            创建编辑备份计划，选择虚拟机的位置， 新增文案提示不包含xxx
                            创建编辑复制计划，选择虚拟机的位置， 新增文案提示不包含xxx
                        克隆，转化为模版
                            克隆为模版，包含提示： 模版不包含xxx
                            转化为模版，包含提示： 模版不包含xxx
                            克隆为虚拟机， 都不携带 AM 和 DPI
                    GVM 无法被保护场景
                        SVM 已关机情况
                            启用 DPI 的虚拟机迁移或则 HA 到已部署 SVM 但 SVM 关机的主机
                                集群 - 虚拟机页面表头提示
                                主机 - 虚拟机页面表头提示
                            已开启 AM 的虚拟机所属主机的 SVM 关机
                                集群 - 虚拟机页面表头提示
                                主机 - 虚拟机页面表头提示
                        主机未配置导流网卡
                            启用 DPI 的虚拟机迁移或则 HA 到未配置导流网卡的主机
                                集群 - 虚拟机页面表头提示
                                主机 - 虚拟机页面表头提示
                DS 驱动
                    虚拟机启用 AM 时自动触发为虚拟机安装 DS 驱动
                    虚拟机禁用 AM 时自动触发为虚拟机卸载 DS 驱动
                    已开启 AM 的 GVM 克隆新的虚拟机包含残留的 DS,  此时启用 AM 时触发强制安装 DS 驱动
                    虚拟机关机状态禁用 AM 时，跳过卸载 DS 驱动，预期等待下次开机时，定时任务扫描到进行处理
                    开机虚拟机 VMTools 未运行或已卸载，不允许虚拟机禁用 AM【要求 VMTools 运行且版本大于等于 4.1.0 才支持触发禁用 AM】
                    亚信 DS 驱动兼容的 GuestOS VM， 开启 AM 成功（DS 驱动安装成功）
                    SMTXOS 6.3,0 + VMTools 4.1.0 定制  DS 驱动版本为 20.0.2
                    ARCFRA_VMTOOLS 不包含 DS 驱动
                集群运维 （SRE）
                    630 新集群部署
                        检查配置文件 /etc/elfvirt/vs.conf （是 vs-controller rpm 安装时带上的）
                    服务监控
                        新增服务 vs-controller
                            需要分配 CPU、memory ， cgroup 配置
                            需要提供日志位置，日志截断规则，保留大小
                            需要可以创建服务监控图标
                            需要有服务 stop 报警
                            vs-controller 命令行
                            主机服务 vs-controller stop， 主机上的 虚拟机 开启 AM 失败
                    集群升级
                        检查配置文件 /etc/elfvirt/vs.conf （是 vs-controller rpm 安装时带上的） ，的内容已固定 （产品上不允许手动修改）
                        存量虚拟机信息检查
                        存量虚拟机热删除网卡，预期删除成功
                        存量虚拟机热添加网卡，检查热添加成功
                        存量虚拟机开机
                        存量虚拟机关机
                        存量开机虚拟机需要关机再开机后，启用 AM（有文案）, 再关闭 AM
                        存量开机虚拟机启用 DPI   再关闭 DPI
                        新创建虚拟机检查
                    维护模式
                        进入维护模式
                            进入维护模式第一个页面的忽略放置组，需要排除 SVM
                            勾选将无法迁出的虚拟机关机后，可以触发进入维护模式
                        退出维护模式
                            关机的  SVM 在源主机开机【退出维护模式的开机任务队列中， SVM 优先于 GVM 开机】
                            被迁移的 GVM 迁移回源主机
                            关机的 GVM 在源主机开机
                    集群扩容
                        扩容新节点加入集群步骤不变， 加入后部署  SVM 的位置展示部分部署
                    集群缩容
                        删除主机时要求主机上没有虚拟机，需要在删除主机之前手动迁移存留的 GVM， 删除存留的 SVM【删除主机位置的文档需要描述一下】
                    主机关机重启
                        进入维护模式，再做关机重启，预期操作成功
                        不进入维护模式做关机、重启， 有提示
                    boost 开启切换
                        非 boost 转 boost
                            初始非 boost 集群检查和准备
                                集群开启安全防护，部署 SVM, 并虚拟机配置开启 AM 和 DPI
                                vm batch1 开启 AM
                                vm batch2 开启 DPI
                                vm batch3 开启 AM & DPI
                            集群开启 boost
                                集群所有虚拟机关机，执行 zbs-cluster vhost  enable 开启 vhost
                            开启 boost 后检查
                                集群 - 设置 - 安全 -  【深度安全防护】 不展示
                                存量关机虚拟机属性检查， AM 和 DPI 配置保持开启
                                集群 - 虚拟机页面 / 主机 - 虚拟机页面，有 SVM 未开机的警告提示
                                存量关机虚拟机【已开启 AM 】触发开机， 预期返回不允许 （ELF-7985 ）
                                存量关机虚拟机【已开启 AM】，关闭 AM,  关闭成功
                                存量关机虚拟机【已开启 DPI】，关闭 DPI,  关闭成功
                                存量 SVM 触发开机，预期失败
                                新创建开机虚拟机，开启 AM 或者 DPI， 不允许开启
                                删除 SVM 成功
                        boost 转非 boost
                            初始 boost 集群检查和准备
                                集群 - 设置 - 安全 -  【深度安全防护】 不展示
                                准备开机，关机虚拟机
                            集群关闭 boost
                                集群所有虚拟机关机， 执行命令行 zbs-cluster vhost  disable 关闭 vhost
                            关闭 boost 后检查
                                集群 - 设置 - 安全 -  【深度安全防护】 正常展示， 可以设置开启
                                存量关机虚拟机触发开机， 预期开机成功
                                集群部署 SVM , 预期部署成功
                                集群配置 ER 导流，预期配置成功
                                存量关机虚拟机，开启后，配置开启 AM, DPI, 预期开启成功
                                新创建开机虚拟机，配置开启 AM, DPI, 预期开启成功
                故障场景
                    DSM 与 SVM 之间网络异常
                        SVM 关机后，主机集群的虚拟机列表位置有告警提示
                    服务 vm-security-controller 不可用
                        集群有服务不可用报警
                定时任务
                    kvm_vm_check_gvm_resources
                    kvm_vm_check_unexpected_ds_driver
                Tower 任务事件
                    任务
                        开 AM,  任务：编辑虚拟机 %vmname% 的防病毒功能
                        关闭 AM 任务：编辑虚拟机 %vmname% 的防病毒功能
                        开启 DPI 任务：编辑虚拟机 %vmname% 的深度包检测功能
                        关闭 DPI 任务：编辑虚拟机 %vmname% 的深度包检测功能
                    事件
                        编辑深度安全防护
                        导入 OVF SVM 模板 - 事件描述中增加一句话描述
                        创建 SVM 虚拟机 - 事件描述中增加一句话说明
                        为虚拟机开启/关闭防病毒或为虚拟机的任一 vNIC 开启/关闭 DPI
                        虚拟机高可用重建 - HA 后自动关闭虚拟机防病毒功能，在高可用重建事件中增加描述
                        虚拟机因网络故障触发高可用 - HA 重建后自动关闭虚拟机防病毒功能，在高可用重建事件中增加描述。
                Tower 权限
                    自定义权限
                        不分配【深度安全防护】权限, 检查部署 SVM,  预期没有部署入口
                        分配【深度安全防护】权限， 不分配【模版导入导出】权限, 无法导入 SVM 模版， 入口不展示
                        分配【深度安全防护】权限， 不分配【虚拟机创建】权限, 不支持部署 SVM
                        分配【深度安全防护】权限， 不分配【虚拟机放置组】权限, 可以正常部署 SVM
                        分配【深度安全防护】权限， 不分配【安装虚拟机工具、通过虚拟机工具变更虚拟机】权限， 可以正常开启 AM
                    虚拟机使用者视图
                        GVM 在虚拟机使用者视图下的操作权限检查
                        SVM 在虚拟机使用者视图下的操作权限检查
                        GVM, SVM 在虚拟机使用者试图下，监控数据正常展示
                Tower OAPI
                    虚拟机
                        获取虚拟机接口，增加「安全防护虚拟机」标识，用于识别虚拟机是否为 SVM
                        增加获取虚拟网卡 DPI 配置接口，用于识别虚拟网卡是否启用了 DPI 功能
                        查询 SVM 虚拟机，返回 "usage": "SVM",
                        查询 S VM 放置组，返回 "usage": "SVM",
                    内容库模版
                        查询模版 /api/get-content-library-vm-templates  返回 "usage": "SVM",
                Tower 用户
                    DSM 操作使用定制账户，方便 tower 上查看 DSM 操作历史
                不同集群特殊处理
                    ACOS
                        AOC + ACOS 集群不展示【深度安全防护】
                        创建空白虚拟机时创建 SVM，UI 没有入口， ELF API  返回 PRECHECK_VMS_INTERNAL_PRODUCT_CANNOT_BE_CREATED
                        从模版创建 SVM， UI 没有入口， ELF API 返回 PRECHECK_VMS_INTERNAL_PRODUCT_CANNOT_BE_CREATED
                    boost 集群
                        Tower 4.8.0 + boost 集群不展示【深度安全防护】
                        创建空白虚拟机时创建 SVM，UI 没有入口， ELF API  返回PRECHECK_VMS_INTERNAL_PRODUCT_CANNOT_BE_CREATED
                        从模版创建 SVM， UI 没有入口， ELF API 返回 PRECHECK_VMS_INTERNAL_PRODUCT_CANNOT_BE_CREATED
                        非 boost 部署 SVM 在转为 boost 后，SVM 开机， ELF API 返 PRECHECK_VMS_INTERNAL_PRODUCT_UNSUPPORTED
                    arm 集群
                        Tower 4.8.0 + boost 集群不展示【深度安全防护】
                        创建空白虚拟机时创建 SVM，UI 没有入口， ELF API  返回 PRECHECK VMS INTERNAL PRODUCT CANNOT BE CREATED
                        从模版创建 SVM， UI 没有入口， ELF API 返回 PRECHECK VMS INTERNAL PRODUCT CANNOT BE CREATED
            ELF-7519  适配 SMTX ZBS 引入的 ZBS Chunk 多实例 - CPU 独占功能优化
                虚拟机独占可用 cpu 计算
                    /api/v2/compute/vms_summary API 收集虚拟机相关的计算资源信息，检查剩余可独占的 CPU 数量 available_exclusive_cpu 、可预留 cpu 与计算一致
                    低版本升级630 集群(allow_chunk_weak_for_exclusive=Ture) 后 - 检查 cpu_count_cannot_be_exclusive 数量包含：chunk_dynamic_cpus +   cpu 0 - 检查剩余可独占、可预留cpu 数量正确
                    高版集群默认 (allow_chunk_weak_for_exclusive=False ) - 检查 cpu_count_cannot_be_exclusive 数量包含：chunk_dynamic_cpus +   cpu 0 + chunk_numa_weak_cpus - 检查剩余可独占、可预留cpu 数量正确
                    高版集群默认 (allow_chunk_weak_for_exclusive=Ture ) - 检查 cpu_count_cannot_be_exclusive 数量包含：chunk_dynamic_cpus +   cpu 0 - 检查剩余可独占、可预留cpu 数量正确
                    计算剩余可独占计算公式 available_exclusive_cpu = cpu_count_for_vm - max(cpu_qos_reserverd_count, min_shared_cpu_count, cpu_count_cannot_be_exclusive) - exclusive_cpu_count - 与接口数据一致
                    节点有独占vm ,max(cpu_qos_reserverd_count, min_shared_cpu_count, cpu_count_cannot_be_exclusive)  中，已使用cpu qos 数 cpu_qos_reserverd_count最大时 - 剩余独占计算正确
                    节点有独占vm ,max(cpu_qos_reserverd_count, min_shared_cpu_count, cpu_count_cannot_be_exclusive)  中，已使用cpu qos 数 min_shared_cpu_count 最大时 - 剩余独占计算正确
                    节点有独占vm ,max(cpu_qos_reserverd_count, min_shared_cpu_count, cpu_count_cannot_be_exclusive)  中，已使用cpu qos 数 cpu_count_cannot_be_exclusive 最大时 - 剩余独占计算正确
                    计算剩余最大预留频率 available_cpu_reservation_hz =（( N(qemu) - N(exclusive) ) * F(per core)）*0.8 - cpu_reservation_hz - 与接口数据一致
                    tower UI 剩余可独占数量 - vms_summary.available_exclusive_cpu 直接获取 - 创建 vm  - 指定主机 - 展示的当前主机剩余独占数量正确
                    tower UI 剩余可独占数量 - vms_summary.available_exclusive_cpu 直接获取 - 创建 vm  - 自动调度主机 - 展示的集群剩余数量最大主机的剩余独占数量正确
                    tower 剩余可用预留 -  MIN( vms_summary.available_cpu_reservation_hz , N(vcpu) * F(per core) )- 创建 vm - 指定主机 - 展示的当前主机剩余独占数量正确
                    tower 剩余可用预留 -  MIN( vms_summary.available_cpu_reservation_hz , N(vcpu) * F(per core) )- 创建 vm - 自动调度主机 - 展示的集群剩余数量最大主机的剩余独占数量正确
                    tower 主机列选项 可独占cpu 数、已独占 cpu 数、cpu 共享分配量、共享分配比、活跃（共享）分配量、分配比 展示正确
                    tower 集群概览 - cpu 分配：系统预留、已独占、共享 cpu 数展示正确
                    chunk numa weak cpu Ture/false 导致的 可独占数量的变化 -   	/api/v2/compute/vms_summary  不会及时响应会 5min 后同步到
                算法优化检查（多chunk 实例）
                    vcpu 对应 pcpu numa
                        特例：
                            630 版本 - 所有场景不使用 CPU 0 作为独占 CPU
                            630 默认不使用 chunk_numa_weak_cpus 进行独占；
                            低版本集群升级前已使用 cpu 0 - 升级后 - 下一次调度时排除不使用 0 号 cpu
                            手动指定虚拟机独占 0 cpu - 配置成功，虚拟机开机不生效使用自动配置独占cpu
                        一、chunk ins1 对应的 chunk_numa_free_cpus 足以容纳 vCPU
                            cpu 独占虚拟机使用的独占数量<= [chunk ins1 对应的 chunk_numa_free_cpus] 空闲个数 - 则将 vCPU 绑定在[chunk ins1 对应的 chunk_numa_free_cpus] 上；
                        二、numa node 的 completely_free_thread_group 分配
                            仅有1个numa node 有足够可用 completely_free_thread_group
                                存在一个 NUMA node 的一个 completely_free_thread_group 足以容纳 vCPU，则将 vCPU 绑定在该 NUMA 上
                            若有多个 NUMA node 的 completely_free_thread_group 足以容纳 vCPU
                                1、选择距离[chunk ins1 所在numa node] 最近的 NUMA Node
                                【620-hp1 不支持】2、如果有多个 NUMA node 距离相同，选择剩余内存较多的（扣减之前已经分配出去的绑定 VM 所占用的内存和系统预留内存之后）：
                                3、如果还有相同的，选择一个completely_free_thread_group 最少的 NUMA node（以减少碎片产生）；
                                4、如果还有多个候选 NUMA node，选择 NUMA ID 较小的；
                        三、socket 的 completely_free_thread_group 分配
                            筛选使用的 socket
                                仅 一组 socket 的 completely_free_thread_group pcpu 总量可以容纳 vCPU
                                    选 socket 上的 numa
                                        1、分配独占 n vpcu 的 A个核心使用的 numa node
                                            1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                            2、如果有多个，则优先填充和 [chunk ins1 所在numa node] 距离小的；
                                            【620-hp1 不支持】3、如果还有多个，则优先填充和剩余内存多；
                                            4、如果还有多个，则优先填充第一个 vCPU id 小的；
                                        2、分配独占 n vpcu 的（n- A）个核心使用的 numa node
                                            1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                            2、如果有 numa node 满足使用 （n-A）vcpu 独占，则优先填充和 和上一次分配的 NUMA Node 距离近的
                                            【620-hp1 不支持】3、如果还有多个，则优先填充和剩余内存多；
                                            4、如果还有多个，则优先填充第一个 vCPU id 小的；
                                            5、如过 （n-A） vcpu 独占没有分配完，重复以上步骤（上一次numa node 对比）
                                有多组 socket 的 completely_free_thread_group pcpu 总量可以容纳 vCPU
                                    1、选择距离[chunk ins1 所在numa node]最近的 completely_free_thread_group
                                        选 socket 上的 numa
                                            1、分配独占 n vcpu vm 的 第一个 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                                2、如果有多个Socket 的 completely_free_thread_group 的 numa node 满足使用 Avcpu 独占，则优先填充和 [chunk ins1 所在numa node] 距离小的；
                                                【620-hp1 不支持】3、如果还有多个，则优先填充和剩余内存多；
                                                4、如果还有多个，则优先填充第一个 vCPU id 小的；
                                            2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                                2、如果有 numa node 满足使用 （n-A）vcpu 独占，则优先填充和 和第一次分配的 NUMA Node 距离近的
                                                【620-hp1 不支持】3、如果还有多个，则优先填充和剩余内存多；
                                                4、如果还有多个，则优先填充第一个 vCPU id 小的；
                                                5、如过 （n-A） vcpu 独占没有分配完，重复以上步骤
                                    【620-hp1 不支持】如果有多个 completely_free_thread_group 距离相同，选择剩余内存较多的
                                        选 socket 上的 numa
                                            1、分配独占 n vcpu vm 的 第一个 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                                2、如果有多个Socket 的 completely_free_thread_group 的 numa node 满足使用 Avcpu 独占，则优先填充和 [chunk ins1 所在numa node]  距离小的；
                                                【620-hp1 不支持】3、如果还有多个，则优先填充和剩余内存多；
                                                4、如果还有多个，则优先填充第一个 vCPU id 小的；
                                            2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                                2、如果有 numa node 满足使用 （n-A）vcpu 独占，则优先填充和 和第一次分配的 NUMA Node 距离近的
                                                【620-hp1 不支持】3、如果还有多个，则优先填充和剩余内存多；
                                                4、如果还有多个，则优先填充第一个 vCPU id 小的；
                                                5、如过 （n-A） vcpu 独占没有分配完，重复以上步骤
                                    3、如果还有相同的，选择一个最小的 completely_free_thread_group
                                        选 socket 上的 numa
                                            1、分配独占 n vcpu vm 的 第一个 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                                2、如果有多个Socket 的 completely_free_thread_group 的 numa node 满足使用 Avcpu 独占，则优先填充和 [chunk ins1 所在numa node] 距离小的；
                                                【620-hp1 不支持】3、如果还有多个，则优先填充和剩余内存多；
                                                4、如果还有多个，则优先填充第一个 vCPU id 小的；
                                            2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                                2、如果有 numa node 满足使用 （n-A）vcpu 独占，则优先填充和 和第一次分配的 NUMA Node 距离近的
                                                【620-hp1 不支持】3、如果还有多个，则优先填充和剩余内存多；
                                                4、如果还有多个，则优先填充第一个 vCPU id 小的；
                                                5、如过 （n-A） vcpu 独占没有分配完，重复以上步骤
                                    4、如果还有多个候选 completely_free_thread_group ，选择 Group 中第一个 vCPU id 较小的；
                                        选 socket 上的 numa
                                            1、分配独占 n vcpu vm 的 第一个 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                                2、如果有多个Socket 的 completely_free_thread_group 的 numa node 满足使用 Avcpu 独占，则优先填充和[chunk ins1 所在numa node] 距离小的；
                                                【620-hp1 不支持】3、如果还有多个，则优先填充和剩余内存多；
                                                4、如果还有多个，则优先填充第一个 vCPU id 小的；
                                            2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                1、如果还没有任何核心被分配，则选择在同一个 NUMA Node 内 compeletely_free_thread 最多的优先填充
                                                2、如果有 numa node 满足使用 （n-A）vcpu 独占，则优先填充和 和第一次分配的 NUMA Node 距离近的
                                                【620-hp1 不支持】3、如果还有多个，则优先填充和剩余内存多；
                                                4、如果还有多个，则优先填充第一个 vCPU id 小的；
                                                5、如过 （n-A） vcpu 独占没有分配完，重复以上步骤
                        四、free_thread_group 分配（排除 chunk_week_group 数据 ）
                            筛选 numa node 下的 cpu
                                1、把 larger_free 中的 completely free 占满；
                                2、把 larger _free 中的非 completely free 占满；
                                3、把 smaller_free 中的 非completely_free 占满；
                                4、把 smaller_free 中的 completely_free 占满；
                            1、numa 上的 free_thread_group 分配
                                1、1个 NUMA Node 的 free_thread_group 满足 独占
                                    只存在一个 NUMA node 的一个 free_thread_group 足以容纳 vCPU，则将 vCPU 绑定在该 NUMA 上
                                2、多个numa node 的 free_thread_group 满足独占
                                    1、选择 group 内 completely_free 数量最多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    2、如果还有多个，选择 距离 [chunk ins1 所在numa node] 最近的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    【620-hp1 不支持】3、如果还有多个， 选择剩余内存较多 的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    4、如果还有多个， 选择  free_thread_group  数量最小 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    5、如果还有多个， 选择 NUMA ID 更小 的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                            2、socket上的 free_thread_group 分配
                                筛选 socket
                                    仅有 1个 socket 的 free_thread_group 满足独占
                                        选择 socket 的 numa
                                            1、分配独占 n vcpu vm 的 第一个 numa node
                                                1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                2、如果还有多个，则优先 [chunk ins1 所在numa node]  最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free 的核心；
                                                【620-hp1 不支持】3、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                4、如果还有多个，则优先 free group 本身数量最小
                                                5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                            2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                3、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                6、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                                    有多个 socket 的 free_thread_group 满足独占
                                        1、completely_free 数量最多的 socket
                                            1、筛选 completely_free 数量最大的 socket 作为独占目标 socket
                                            选择 socket 的 numa
                                                1、分配独占 n vcpu vm 的 第一个 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先 [chunk ins1 所在numa node] 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free 的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    6、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                                        2、 距离 [chunk ins1 所在numa node] 最近的 socket
                                            2、如果有重复的，选择 距离[chunk ins1 所在numa node] 最近的 socket 作为目标socket
                                            选择 socket 的 numa
                                                1、分配独占 n vcpu vm 的 第一个 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先距离 [chunk ins1 所在numa node]  最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    6、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                                        【620-hp1 不支持】3、剩余内存更多 的 socket
                                            【620-hp1 不支持】3、如果有重复 socket 选择内存较多的 - 作为目标socket
                                            选择 socket 的 numa
                                                1、分配独占 n vcpu vm 的 第一个 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先距离[chunk ins1 所在numa node]  最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    6、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                                        4、socket free group 最小 socket
                                            4、如果有重复的 选socket free_thread_cpu group 内数量 最小 - 作为目标 socket
                                            选择 socket 的 numa
                                                1、分配独占 n vcpu vm 的 第一个 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先距离[chunk ins1 所在numa node] 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    5、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                                        5、socket Gruop 内第一个 vCPU id 最小 socket
                                            5、如果有重复，选socket free_thread_cpu group内第一个 vCPU id 最小的 -  作为目标socket
                                            选择 socket 的 numa
                                                1、分配独占 n vcpu vm 的 第一个 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先 [[chunk ins1 所在numa node] ins1 所在numa node] 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free 的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                                    1、如果只有一个 nuam 满足，就选这个，有多个满足，优先 completely_free 数量最多的 numa，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    2、如果还有多个，优先 free 最数量最多的 numa，优先分配 larger_free 中的 completely free的核心；
                                                    3、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                                    6、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                        五、使用 多socket pcpu 的分配
                            虚拟机独占vcpu数量需要使用多 socket 上 cpu - 检查：分配时先分配剩余 free_thread_group 数量较多的 socket作为第一组socket:分配 numa、分配 cpu_id - 后续选择 socket 继续分配 numa 分配cpu
                            筛选 numa node 下的 cpu
                                1、把 larger_free 中的 completely free 占满；
                                2、把 larger _free 中的非 completely free 占满；
                                3、把 smaller_free 中的 非completely_free 占满；
                                4、把 smaller_free 中的 completely_free 占满；
                            第一组socket 分配 SUM（A）个CPU
                                一个socket 剩余 free + 一个 socket 未使用 - 此时较大数量cpu 独占，也是按 free 数量分配 - 与规则4一致，先使用 complate_free
                                选择 socket 的 numa
                                    1、分配独占 n vcpu vm 的 第一个 numa node
                                        1、有多个Socket free_thread_group 的 numa node 满足，优先 completely_free 数量最多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                        2、如果还有多个，优先 free 数量大的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                        3、如果还有多个，则优先 [chunk ins1 所在numa node] 最近的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                        【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                        5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                    2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                        1、有多个Socket free_thread_group 的 numa node 满足，优先 completely_free 数量最多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                        2、如果还有多个，优先 free 数量大的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                        3、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                        【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                        5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                        6、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                            后续 socket 使用(N-SUM(A))
                                1、分配独占 n vcpu vm 的 第一个 numa node
                                    1、有多个Socket free_thread_group 的 numa node 满足，优先 completely_free 数量最多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    2、如果还有多个，优先 free 数量大的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    3、如果还有多个，则优先 [chunk ins1 所在numa node] 最近的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                2、分配剩余独占（n- A) vcpu 核心使用的 numa node
                                    1、有多个Socket free_thread_group 的 numa node 满足，优先 completely_free 数量最多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    2、如果还有多个，优先 free 数量大的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    3、如果还有多个，则优先 上一次numa 最近的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    【620-hp1 不支持】4、如果还有多个，则优先剩余内存多的 numa - 选定 numa 后，Group 内优先分配 completely_free 的核心；
                                    5、如果还有多个，numa id 更小的 numa - 选定 numa 后，Group 内优先分配 larger_free 中的 completely free的核心；
                                    6、如果还有 独占 vcpu 没分配完，继续重复以上步骤分配
                        六、多 socket 不够用时，allow_chunk_weak_for_exclusive=True，使用 chunk_numa_weak_cpus
                            创建vm 使用（总可独占 vcpu 数 -  chunk_numa_weak_cpus数 ）个 vpcu  - 检查cpu 独占不使用  chunk_numa_weak_cpus
                            （总可独占 vcpu 数 -  chunk_numa_weak_cpus ）个 vpcu 已使用完 -创建独占 vm - vm 使用 chunk_numa_weak_cpus
                            allow_chunk_weak_for_exclusive=false 时，chunk_numa_weak_cpus 使用情况检查:使用了多个 socket 后 CPU 还不够，会使用 chunk_numa_weak_cpus，使用的顺序为 CPU ID 的字母序。
                    算法规则覆盖检查
                        开机虚拟机使用节点所有 可独占 vcpu - 检查 vcpu to pcpu 分配，符合最新规则1~6
                        开机虚拟机使用节点（总可独占数- chun_numa_weak_cpus数）个 vcpu - 检查 vcpu to pcpu 分配，符合最新规则1~5
                        开机虚拟机使用 cpu 独占个数 小于chunk_numa_free 数量，使用规则1：ChunkIns1NUMAFreePolicy
                        开机虚拟机使用 cpu 独占个数大于chunk_numa_free 数量，优先规则2:SingleNUMACompletelyFreePolicy
                        chunk_numa_free 数量分配完时，后续分配优先规则二:SingleNUMACompletelyFreePolicy
                        规则1、2 独占数量不足时，需继续分配独占 cpu ，优先使用规则3 cpu:SingleSocketCompletelyFreePolicy
                        规则1、2 、3独占数量不足时，需继续分配独占 cpu ，优先使用规则4.1 SingleNUMAFreePolicy
                        规则1、2 、3、4.1 SingleNUMAFreePolicy 的 独占数量不足时，需继续分配独占 cpu ，优先使用规则4.2 ：SingleSocketFreePolicy
                        规则1、2 、3、4独占数量不足时，需继续分配独占 cpu ，优先使用规则5 cpu：MultipleSocketsPolicy，日志关键字 Using free threads, ordered sockets
                        使用规则6 chunk_numa_weak_cpus  进行独占（嵌套环境验证）
                场景测试覆盖
                    实例数量 1
                        虚拟机独占数量小于 等于 chunk_numa_free_cpus - 使用 chunk_numa_free_cpus 内 cpu 做独占，内存绑定正确
                        虚拟机独占数量 大于 chunk_numa_free_cpus - 按【单实例 chunk 规则】分配独占 cpu，内存绑定正确
                        创建 cpu qos 虚拟机 - 检查预留、cpu 独占数量 UI 配置正确，/sys/fs/cgroup/cpset/machine.slice/ 预留、cpu 独占正确
                    实例数量 2
                        虚拟机独占数量小于 等于 chunk_numa_free_cpus - 使用  chunk ins1 对应的 chunk_numa_free_cpus 内 cpu 做独占，内存绑定正确
                        虚拟机独占数量 大于 chunk_numa_free_cpus - 按【多实例 chunk 规则】分配独占 cpu，内存绑定正确
                        创建 cpu qos 虚拟机 - 检查预留、cpu 独占数量 UI 配置正确，/sys/fs/cgroup/cpset/machine.slice/ 预留、cpu 独占正确
                    实例数量 4
                        虚拟机独占数量小于 等于 chunk_numa_free_cpus - 使用  chunk ins1 对应的 chunk_numa_free_cpus 内 cpu 做独占，内存绑定正确
                        虚拟机独占数量 大于 chunk_numa_free_cpus - 按【多实例 chunk 规则】分配独占 cpu，内存绑定正确
                        创建 cpu qos 虚拟机 - 检查预留、cpu 独占数量 UI 配置正确，/sys/fs/cgroup/cpset/machine.slice/ 预留、cpu 独占正确
                    chunk_weak_for_exclusive的使用
                        单实例 - allow_chunk_weak_for_exclusive=True  - 多个 socket 后 CPU 还不够，会使用 chunk_numa_weak_cpus，使用的顺序为 CPU ID 的字母序。
                        多实例 - allow_chunk_weak_for_exclusive=True  - 多个 socket 后 CPU 还不够，会使用 chunk_numa_weak_cpus，使用的顺序为 CPU ID 的字母序。
                系统配置检查
                    单实例集群升级场景
                        低版本升级630 为单实例集群 - 630 以下版本vm 独占的 cpu  升级时被作为 630 系统服务cpu - 该部分虚拟机会后端操作关机重新开机分配独占cpu
                        低版本升级630 为单实例集群 - 630 以下版本vm 使用完所有的独占cpu - 升级时部分独占的 cpu 被作为 630 系统服务cpu - 该部分虚拟机会后端操作关机重新开机分配独占cpu
                    CLI 检查
                        新增 CLI 检查
                            新增 elf-tool elf_cluster update_allow_chunk_weak_for_exclusive $value  - 设置 allow_chunk_weak_for_exclusive 的取值，为 boolean 类型， True 时表示允许使用 chunk_numa_weak_cpus 进行独占， False 时不允许；
                            新增 elf-tool elf_cluster show_allow_chunk_weak_for_exclusive  - 显示 allow_chunk_weak_for_exclusive 的取值
                            新建 630 集群 elf-tool elf_cluster show_allow_chunk_weak_for_exclusive 的  allow_chunk_weak_for_exclusive=False，手动独占使用 chunk_numa_weak_cpus 成功但虚拟机开机时降级为自动独占 630 规则
                            低版本升级 630 集群 elf-tool elf_cluster show_allow_chunk_weak_for_exclusive 的  allow_chunk_weak_for_exclusive=Ture，保持低版本兼容性允许独占使用 chunk_weak_cpu
                            630 集群 配置  allow_chunk_weak_for_exclusive=Ture - 配置成功，vm 独占可分配 chunk_numa_weak_cpus
                            独占vm 已使用 chunk_numa_weak_cpus，集群升级 630 后 - 操作关闭：elf-tool elf_cluster update_allow_chunk_weak_for_exclusive False -  命令行执行成功，不校验 - 后续重新调度 会触发自动分配非 chunk_weak_cpus(不足时调度失败)
                        已有 CLI 修改检查
                            elf-tool elf_cluster show_cpu_pin 功能：显示集群所有节点的 CPU 独占信息 - 显示「预留 CPU 数量」和 「可独占 CPU」两个信息。
                            630 时 elf-tool elf_cluster show_cpu_pin  展示的独占可以 cpu 不包含 0 号 cpu
                            低版本升级至630 后，elf-tool elf_cluster show_cpu_pin  展示的独占可以 cpu 不包含 0 号 cpu
                            630 时默认   chunk_numa_weak_cpus  False  - 检查 elf-tool elf_cluster show_cpu_pin  展示的独占 cpu 不包含 chunk_numa_weak_cpus
                            630 集群修改 chunk_numa_weak_cpus  False 为 Ture   - 检查 elf-tool elf_cluster show_cpu_pin  展示的独占 cpu 包含 chunk_numa_weak_cpus
                            低版本升级默认    chunk_numa_weak_cpus  Ture  - 检查 elf-tool elf_cluster show_cpu_pin  展示的独占 cpu 包含 chunk_numa_weak_cpus
                    numa   chunk 距离计算
                        api/v2/management/hosts 可以查看 chunk_ins1 所属numa node ：data[0].chunk_list[0].numa_node
                        在 api/v2/management/hosts 接口或 命令行 numactl -H 可以查看各 numa 之间的距离
                        socket 到chunkd 距离计算：将 group 内包含的所有 NUMA Node 距离 Chunk_ins 所在 NUMA 上的平均距离作为 Socket 和 Chunk Node 之间的距离
                    分配独占 numa 日志检查（630 待更新关键字）
                        查看 cgroup 各系统服务配置对应的 pcpu 核心
                        elf-vm-schedule 日志中查看 虚拟机所属节点 numa 可分配的 共享cpu、独占 pcpu 集合
                        elf-vm-schedule 日志中查看 每个节点 numa 分配的  completely_free_thread_group 的 cpu 集合，区分 smaller 、larger
                        elf-vm-schedule 日志中查看 每个节点 numa 分配的  free_thread_group 的 cpu 集合，区分 smaller 和 larger、总free cpu 数
                        elf-vm-schedule 日志中查看 每个节点 socket 上numa 分配的  completely_free_thread_group 的 cpu 集合，区分 smaller 和 larger
                        elf-vm-schedule 日志中查看 每个节点 socket 上numa 分配的  free_thread_group 的 cpu 集合，区分 smaller 、larger  总数free cpu 数
                        elf-vm-schedule 日志中查看 每个节点 chunk_cpu_info信息
                        elf-vm-schedule 日志中展示选定的虚拟机cpu 独占策略：ChunkIns1NUMAFreePolicy
                        elf-vm-schedule 日志中展示选定的虚拟机cpu 独占策略：SingleNUMACompletelyFreePolicy
                        elf-vm-schedule 日志中展示选定的虚拟机cpu 独占策略：SingleSocketCompletelyFreePolicy
                        elf-vm-schedule 日志中展示选定的虚拟机cpu 独占策略：SingleNUMAFreePolicy
                        elf-vm-schedule 日志中展示选定的虚拟机cpu 独占策略：SingleSocketFreePolicy
                        elf-vm-schedule 日志中展示选定的虚拟机cpu 独占策略：MultipleSocketsPolicy 日志： Using free threads, ordered sockets
                        在一个 Policy 中，可以通过 sorted plans are 关键字判断目前有可用方案排序后有哪些
                        在一个 socket 中选择 NUMA 时，关键字是 with previous node={}, remained_vcpu_count={}, remained_numa_nodes={}, choose node={} as best node, selected_pcpus={}
            ELF-7343:双活集群按可用域配置放置组规则
                UI测试
                    创建虚拟机放置组
                        可用域放置策略：必须放置在优先可用域上
                        可用域放置策略：优先放置在优先可用域上
                        可用域放置策略：必须放置在次级可用域上
                        可用域放置策略：优先放置在次级可用域上
                        禁用规则：勾选可用域放置策略，禁用「必须/优先放置在选定主机上」策略
                        禁用规则：勾选必须放置在选定主机上」策略，禁用可用域放置策略
                        禁用规则：勾选优先放置在选定主机上策略，禁用可用域放置策略
                        禁用规则：同时勾选必须和优先放置在选定主机上」策略，禁用可用域放置策略
                    放置组详情面板
                        放置组详情-策略-成员虚拟机{必须}放置在{优先可用域}上。
                        放置组详情-策略-成员虚拟机{优先}放置在{优先可用域}上。
                        放置组详情-策略-成员虚拟机{必须}放置在{次级可用域}上。
                        放置组详情-策略-成员虚拟机{优先}放置在{次级可用域}上。
                功能测试
                    HA
                        虚拟机在次级可用域，放置组要求「必须」优先可用域，所在主机存储网故障HA；虚拟机调度到优先可用域
                        虚拟机在优先可用域，放置组要求「必须」次级可用域，所在主机存储网故障HA；虚拟机调度到次级可用域
                        虚拟机在优先可用域，放置组要求「优先不」在优先可用域，所在主机存储网故障HA；虚拟机调度到次级可用域
                    虚拟机开机调度
                        虚拟机在次级可用域，放置组要求「必须」优先可用域，进行自动调度开机；虚拟机调度到优先可用域
                        虚拟机在优先可用域，放置组要求「必须」次级可用域，进行自动调度开机；虚拟机调度到次级可用域
                        虚拟机在优先可用域，放置组要求「必须」次级可用域，选择优先可用于主机开机；虚拟机开机失败
                        虚拟机在次级可用域，放置组要求「必须」优先可用域，选择次级可用于主机开机；虚拟机开机失败
                        虚拟机在优先可用域，放置组要求「优先不」在优先可用域，选择优先可用域主机进行开机，开机成功
                        虚拟机在优先可用域，放置组要求「优先不」在优先可用域，选择自动调度；虚拟机调度到次级可用域
                    集群内迁移
                        虚拟机在次级可用域，放置组要求「必须」优先可用域，热迁移到优先可用域主机；虚拟机调度到优先可用域
                        虚拟机在优先可用域，放置组要求「必须」次级可用域，热迁移到次级可用域主机；虚拟机调度到次级可用域
                        虚拟机在优先可用域，放置组要求「必须」次级可用域，热迁移到优先可用域主机；提交迁移任务失败
                        虚拟机在次级可用域，放置组要求「必须」优先可用域，热迁移到次级可用域主机，提交迁移任务失败
                        虚拟机在优先可用域，放置组要求「优先不」在优先可用域，热迁移到优先可用域，迁移成功
                        虚拟机在优先可用域，放置组要求「优先不」在优先可用域，热迁移到次级可用域主机，迁移成功
                    维护模式
                        虚拟机在次级可用域，放置组要求「必须」优先可用域，主机进入维护模式，虚拟机调度到优先可用域
                        虚拟机在次级可用域，放置组要求「必须」优先可用域，主机进入维护模式，虚拟机调度到优先可用域；退出维护模式，虚拟机维持在主机不变
                    DRS
                        放置组:vm1 vm2 vm3 优先放置次级域;分布:vm1、vm2在优先域，vm3在次级域；负载资源充足;预期vm1、2迁移到次级域
                        放置组:vm1 vm2 vm3 优先放置次级域;分布:vm1、vm2在优先域，vm3在次级域；负载资源只满足vm1;预期vm1迁移到次级域
                        放置组:vm1 vm2 vm3 优先放置次级域;分布:vm1、vm2在优先域，vm3在次级域；负载资源充足，但次级域主机不可用;预期vm1、2不生成迁移到次级域建议
                        DRS：不产生违反可用域规则的迁移建议  （满足放置组规则>资源调度） 3vm在次级可用域，次级可用域资源不足，优先可用域资源充足，DRS不产生迁移到优先可用域的建议
                    可用域放置组告警
                        虚拟机在次级可用域，放置组要求「必须」优先可用域；产生放置组违反规则告警
                        虚拟机在次级可用域，放置组要求「必须」优先可用域；产生放置组违反规则告警；移除放置组策略，告警消失
                        虚拟机在次级可用域，放置组要求「必须」优先可用域；产生放置组违反规则告警；虚拟机调度到优先可用域，告警消失
            ELF-7746 海光平台 CPU 透传行为修改
                新部署 630 集群
                    创建空白虚拟机（cpu model = 透传）， 检查虚拟机内部  Vendor ID = HygonGenuine， model name = 主机 cpu 型号
                    OVF 导入虚拟机，cpu mode 默认是集群配置，修改为透传， 检查虚拟机内部 Vendor ID = HygonGenuine
                    虚拟机克隆为虚拟机， 新虚拟机的 cpu model 默认是源虚拟机配置， 修改为 透传， 检查虚拟机内部 Vendor ID = HygonGenuine
                    虚拟机快照重建， 新虚拟机的 cpu model 默认是源虚拟机配置， 修改为 透传， 检查虚拟机内部 Vendor ID = HygonGenuine
                    从模版克隆虚拟机， 新虚拟机的 cpu model 默认是源虚拟机配置， 修改为 透传， 检查虚拟机内部 Vendor ID = HygonGenuine
                    虚拟机关机修改 cpu mode = 透传， 虚拟机开机后 Vendor ID = HygonGenuine
                620 升级到 630 集群
                    创建空白虚拟机（cpu model = 透传）， 检查虚拟机内部  Vendor ID = HygonGenuine， model name = 主机 cpu 型号
                    存量（cpu model = 透传）虚拟机 Vendor ID = AuthenticAMD（保持不变）
                    存量虚拟机关机再开机，Vendor ID 保持不变
                    存量虚拟机（非透传）关机修改 cpu mode = 透传 再开机，Vendor ID 变更为  HygonGenuine
                Tower UI 修改
                    集群 CPU 兼容性配置，增加提示
                    虚拟机 CPU 兼容性编辑弹窗，增加提示
                    虚拟机迁移弹窗，增加提示
                跨集群迁移
                    跨集群热迁移，低版本 到 630， 保持 AuthenticAMD
                        源虚拟机 cpu mode = 指定模型， 目标集群默认 cpu mode = 物理透传， 迁移后目标虚拟机的 cpu mode = 指定模型，Vendor ID = AuthenticAMD
                        源虚拟机 cpu mode = 指定透传， 目标集群默认 cpu mode = 物理透传， 迁移后目标虚拟机的 cpu mode = 透传，Vendor ID = AuthenticAMD（主机透传场景存在兼容性问题，可能开机进入操作系统）
                        源虚拟机 cpu mode = 集群默认（透传）， 目标集群默认 cpu mode = 物理透传， 迁移后目标虚拟机的 cpu mode = 透传，Vendor ID = AuthenticAMD
                    跨集群热迁移，630 到 630， 保持 HygonGenuine
                        源虚拟机 cpu mode = 透传， 目标集群默认 cpu mode = 透传， 迁移后目标虚拟机的 cpu mode = 透传，Vendor ID  不变
                        源虚拟机 cpu model = EPYC， 目标集群不支持 EPYC， 跨集群热迁移会提示：虚拟机 CPU 兼容性与目标主机冲突。
                    跨集群分段迁移、冷迁移， 620 到 630
                        源虚拟机 cpu mode = 指定模型，目标集群默认 cpu mode = 指定模型， 跨集群冷迁移后目标虚拟机的 cpu mode = 集群默认（指定模型），开机 vm Vendor ID = AuthenticAMD （和新创建指定模型一致）
                        源虚拟机 cpu mode = 指定模型，目标集群默认 cpu mode = 指定模型， 跨集群分段迁移后目标虚拟机的 cpu mode = 集群默认（指定模型）， Vendor ID = AuthenticAMD （和新创建指定模型一致）
                        源虚拟机 cpu mode = 指定模型，目标集群默认 cpu mode = 透传， 跨集群冷迁移后目标虚拟机的 cpu mode = 集群默认（透传），开机 vm Vendor ID = HygonGenuine （和新创建指定透传一致）
                        源虚拟机 cpu mode = 主机透传，目标集群默认 cpu mode = 主机透传， 跨集群冷迁移后目标虚拟机的 cpu mode = 集群默认（主机透传），开机 vm Vendor ID = HygonGenuine（和新创建指定模型一致）
            ELF-7119 虚拟机快照支持编辑名称与描述
                虚拟机 - 快照 tab
                    创建快照弹窗
                        创建虚拟卷快照 - 5.0.0 及以上版本支持配置名称和描述 - smxt os 5.x 集群创建快照配置名称描述，创建成功
                        创建虚拟卷快照 - 5.0.0 及以上版本支持配置名称和描述 - smtxos 6.x  集群创建快照配置名称描述，创建成功
                        创建虚拟卷快照 - 5.0.0 及以上版本支持配置名称和描述 - smtxelf 6.x  集群创建快照配置名称描述，创建成功
                        虚拟机创建快照时 - 可编辑虚拟机名称和描述
                        快照名称 - 必填项，为空有校验
                        快照名称字符长度 -不支持分号（;）、反斜杠（\\）和双引号（\"）。- 有校验
                        快照名称字符长度 - 长度不能大于255 - 有校验
                        快照名称字符长度 - 不支持以空格开头或结尾 - 有校验
                        快照名称字符长度 - 不支持连续输入多个空格,有校验 - 单个空格成功
                        快照名称字符长度 - 关联至同一虚拟机的快照不能重名 - 有校验
                        快照描述 - 非必填项，可以为空
                        快照描述 - 无限制，可使用非法字符，无长度、空格限制
                        创建虚拟机普通快照时 - 仅名称重命名，描述留空 - 创建成功
                        创建虚拟机一致性快照时 - 名称，描述自定义 - 创建成功
                        创建快照 - 虚拟机快照名称 -同一个集群内可重名 - 虚拟机内不允许重名
                    快照详情弹窗
                        查看虚拟机快照详情 - 新增描述字段
                        查看虚拟机快照详情 - 新增描述字段，超过 2行断点展示
                        更新快照名称/描述后 - 查看虚拟机快照详情名称/描述更新正确
                    虚拟机详情列表 - 列选项操作
                        列选项 设置 - 新增 [描述]字段 ，可勾选可调整顺序（默认不勾选）
                        列选项 - 新增的 [描述]字段 - 默认不展示该字段，需设置列选项才展示
                        描述字段 - 支持排序 - 按 ASCII 码排序成功
                    虚拟机 - 快照详情 - 编辑
                        入口：虚拟机 - 快照tab - 快照操作：回滚下方，新增「编辑基本信息」按钮，点击后打开「编辑虚拟机快照基本信息」弹窗
                        低于 630 以下的 smtx elf  集群 -虚拟机情况 -  快照列表 - 无快照编辑基本信息入口，630 以上的 smtx elf 集群 编辑快照成功
                        低于 630 以下的 smtx os  集群 -虚拟机情况 -  快照列表 - 无快照编辑基本信息入口，630 以上的 smtx os 编辑快照成功
                        编辑虚拟机快照时 - 可编辑虚拟机名称和描述
                        快照名称 - 必填项，为空有校验
                        快照名称字符长度 -不支持分号（;）、反斜杠（\\）和双引号（\"）。- 有校验
                        快照名称字符长度 - 长度不能大于255 - 有校验
                        快照名称字符长度 - 不支持以空格开头或结尾 - 有校验
                        快照名称字符长度 - 不支持连续输入多个空格,有校验 - 单个空格成功
                        快照名称字符长度 - 关联至同一虚拟机的快照不能重名 - 有校验
                        快照描述 - 非必填项可以为空
                        快照描述 - 无限制，可使用非法字符，无长度、空格限制
                        编辑虚拟机快照详情，保存后 - 检查成功弹窗和失败，触发成功提示
                        编辑虚拟机快照详情，保存后 - 检查弹窗和任务失败，触发失败提示
                        同时编辑虚拟机一致性快照名称和描述 - 编辑成功
                        编辑虚拟机普通快照名称成功
                        编辑虚拟机快照一致性描述成功
                        创建/编辑过程中操作中的vm ,再次操作编辑该快照有校验
                        编辑快照 - 虚拟机快照名称 -同一个集群内可重名 - 虚拟机内不允许重名
                    虚拟机快照管理Tab
                        虚拟机详情列选项
                            6.3.0 及以上 smtx elf/os - 快照管理列表，列选项：新增快照描述列选项：默认不展示，在列选项设置勾选后展示
                            快照管理列表 csv 下载，检查列选项：新增快照 [描述] 列
                            资产列表 - 虚拟机快照列表：列选项，新增快照 [描述] 列
                        编辑快照
                            低于 630 以下的 smtx os  集群 - 快照管理列表 - 无快照编辑基本信息入口
                            低于 630 以下的 smtx elf  集群 - 快照管理列表 - 无快照编辑基本信息入口
                            入口：虚拟机快照管理 - 选中普通快照，检查可操作项：回滚下方，新增「编辑基本信息」按钮，点击后打开「编辑虚拟机快照基本信息」弹窗，编辑成功
                            入口：虚拟机快照管理 - 选中一致性快照，检查可操作项：回滚下方，新增「编辑基本信息」按钮，点击后打开「编辑虚拟机快照基本信息」弹窗，编辑成功
                            入口：虚拟机快照管理 - 选中无源虚拟机快照（跨集群热迁移遗留），检查可操作项：回滚下方，新增「编辑基本信息」按钮，点击后打开「编辑虚拟机快照基本信息」弹窗
                            入口：虚拟机快照管理 - 选中快照计划虚拟机快照，检查可操作项：回滚下方，新增「编辑基本信息」按钮，点击后打开「编辑虚拟机快照基本信息」弹窗
                            入口：虚拟机快照管理 - 选中复制计划副本虚拟机快照，检查可操作项：无编辑基本信息入口
                            入口：虚拟机快照管理 - 选中备份计划副本虚拟机快照，检查可操作项：无编辑基本信息入口
                            编辑虚拟机快照时 - 可编辑虚拟机名称和描述
                            快照名称 - 必填项，为空有校验
                            快照名称字符长度 -不支持分号（;）、反斜杠（\\）和双引号（\"）。- 有校验
                            快照名称字符长度 - 长度不能大于255 - 有校验
                            快照名称字符长度 - 不支持以空格开头或结尾 - 有校验
                            快照名称字符长度 - 不支持连续输入多个空格,有校验 - 单个空格成功
                            快照名称字符长度 - 关联至同一虚拟机的快照不能重名 - 有校验
                            快照描述 - 非必填项可以为空
                            快照描述 - 无限制，可使用非法字符，无长度、空格限制
                            同时编辑虚拟机快照计划快照名称和描述 - 编辑成功，编辑后快照仍然在原快照计划中
                            编辑虚拟机一致性快照名称成功
                            编辑虚拟机普通快照描述成功
                            编辑快照 - 虚拟机快照名称 -同一个集群内可重名 - 虚拟机内不允许重名
                场景测试
                    快照操作
                        虚拟快照回滚 - 不回滚快照名称和描述：快照1自定义快照名称1和描述1 - 修改为名称2和描述2并创建快照2 - 回滚到快照1，名称描述不变使用：名称2、描述2，其他快照信息回滚正确
                        快照重建时 - 使用已编辑的最新快照名称，描述使用快照重建默认描述
                    集群异常
                        smtx os 集群失联时 - 不支持快照详情、快照管理页面编辑快照名称和描述
                        smtx elf/os 集群过期时 - 支持快照详情、快照管理页面编辑快照名称和描述
                        smtx elf 集群失联时 - 不支持快照详情、快照管理页面编辑快照名称和描述
                        smtx elf 集群关联存储异常时 - 支持快照详情、快照管理页面编辑快照名称和描述
                        smtx elf 集群关联存储未关联至tower时 - 支持快照详情、快照管理页面编辑快照名称和描述
                        smtx elf 集群关联存储过期时 - 支持快照详情、快照管理页面编辑快照名称和描述
                    虚拟机使用者用户
                        虚拟机使用者用户 - 虚拟机tab：创建快照时可编辑快照名称和描述
                        虚拟机使用者用户 -  虚拟机快照 tab 可编辑快照修改快照名称和描述
                        虚拟机使用者用户 -  虚拟机快照 管理tab 可编辑快照修改快照名称和描述
                事件记录
                    创建虚拟机快照时的事件记录：展示快照名称和描述
                    虚拟机 快照 tab 页面 - 编辑虚拟机名称和描述 - 事件记录正确
                    快照管理 tab 页面 - 编辑虚拟机名称和描述 - 事件记录正确
            ELF-7695 存储策略支持条带数 8
                UI 检查
                    新建虚拟卷
                        各方式创建虚拟卷时，虚拟卷容量 - 新增提示：该卷的条带数为 8，容量必须为偶数，填入奇数将会自动向上调整为偶数。
                        容量输入奇数时，触发提示容量必须为偶数，点击其他地方自动 +1 调整为偶数
                    编辑虚拟卷【废弃】
                        编辑虚拟机 磁盘时 - 虚拟卷容量 - 新增提示：该卷的条带数为 8，容量必须为偶数，填入奇数将会自动向上调整为偶数。
                        若已有磁盘包含容量为奇数的卷 - 编辑磁盘时提示：虚拟卷 %volume-name1%、%volume-name2% 的容量为奇数，已自动向上调整为偶数。 - 检查这些卷的容量展示为偶数
                        容量为偶数的卷手动调整容量为奇数后，触发提示容量必须为偶数，点击其他地方容量自动+1 调整为偶数
                        检查编辑已有的被自动调整为偶数的奇数卷 - 减少容量 - 保存检查能正确校验到容量不可减少
                    ovf
                        导入虚拟机、导入虚拟机模板 - 卷容量为奇数，则自动向上取偶数，并展示 Tip 说明
                        导入虚拟卷 - 无法获取容量，固定展示：磁盘容量将会自动向上调整为正偶数
                vm 生命周期检查
                    各方式创建vm
                        创建空白vm
                            通用功能
                                创建空白虚拟机 - 默认虚拟卷，容量默认为 40 ，创建成功，检查创建卷条带数为8
                                创建空白虚拟机 -  新增卷（virtio+scsi+ide+cd-rom）容量奇数自动调整为偶数，创建成功，检查创建卷条带数为8
                                创建空白虚拟机 -  新增卷容量奇数操作复制新建卷，复制卷容量为自动+1偶数 - 创建vm 成功，条带数为8
                                创建空白虚拟机 - 挂载：630 新建卷（共享/非共享 偶数）+ 存量卷（共享/非共享 偶数+奇数） - 创建vm 成功，630 卷 容量偶数、 8条带，存量卷容量、条带数不变
                            不同集群类型创建vm
                                smtx os 630 创建空白虚拟机 - 检查虚拟卷：副本卷 + ec卷，存储策略：偶数卷，8 条带
                                smtxelf630 + 任意zbs集群（zbs570 及以上）：创建空白虚拟机 - 检查虚拟机卷：副本卷 + ec卷 - 仅支持偶数卷，存储策略：8 条带
                                smtxelf630 + 任意zbs集群（zbs570 及下）：创建空白虚拟机 - 检查虚拟机卷：副本卷 + ec卷 - 仅支持偶数卷，存储策略：8 条带
                                smtxelf630 + 任意 os 集群（os630 及以上）：创建空白虚拟机 - 检查虚拟机卷：副本卷 + ec卷 - 仅支持偶数卷，存储策略：8 条带
                                smtxelf630 + 任意 os 集群（os630 以下）：创建空白虚拟机 - 检查虚拟机卷：副本卷 + ec卷 - 仅支持偶数卷，存储策略：8 条带
                                smtxelf620 + os630 及以上：创建空白虚拟机 - 检查虚拟机卷：副本卷 + ec卷 - 可使用奇数卷，存储策略：4 条带
                        快照
                            源630 以下 集群存量vm (含奇数卷) 快照 - 快照重建建vm  - 源快照已有卷容量（奇数）不变、新增卷容量为奇数自动调整为偶数、挂载：630 新建卷（偶数）+ 存量卷 - 创建vm 成功，630 卷容量偶数、8条带，存量卷容量、条带数不变
                            源630 以下 集群 存量vm (含奇数卷) 快照计划 - 快照组重建建vm  - 源快照已有卷容量（奇数）不变、新增卷容量为奇数自动调整为偶数、挂载：630 新建卷（偶数）+ 存量卷 - 创建vm 成功，630 卷容量偶数、 8条带，存量卷容量、条带数不变
                            630 vm 快照 - 快照重建vm  - 已有卷是偶数8条带、新增卷容量为奇数自动调整为偶数、挂载：630 新建卷（偶数）+ 存量卷 - 创建vm 成功，630 卷 容量偶数、8条带，存量卷容量、条带数不变
                            630 快照计划 - 快照组重建建vm  - 源快已有带卷容量不变、新增卷容量为奇数自动调整为偶数、挂载：630 新建卷（偶数）+ 存量卷 - 创建vm 成功，630 卷容量偶数、 8条带，存量卷容量、条带数不变
                            低版本集群升级到 630 级以上版本：os 存量虚拟机新增卷后 - 快照回滚 vm 到存量快照（含奇数卷） - 回滚后的虚拟机卷容量奇数、条带数不变
                            低版本集群升级到 630 级以上版本：os 存量虚拟机的快照计划块招租（含奇数卷） - 快照组回滚 vm - 回滚后的虚拟机卷 容量、条带数不变
                            存量虚拟机含存量快照1（含奇数卷） - 升级 630 后新增卷创建快照2 -  回滚快照1后卷容量奇数、条带数不变，回滚快照2后存量卷容量奇数、条带数不变，新增卷偶数 8条带
                        克隆
                            源630 以下 集群存量vm (含奇数卷) - 克隆创建vm  - 源已有卷容量（奇数）不变、新增卷容量为奇数自动调整为偶数、挂载：630 新建卷（偶数）+ 存量卷 - 创建vm 成功，630 卷容量偶数、8条带，存量卷容量、条带数不变
                            630 vm - 克隆创建vm  - 已有卷是偶数8条带、新增卷容量为奇数自动调整为偶数、挂载：630 新建卷（偶数）+ 存量卷 - 创建vm 成功，630 卷容量偶数、8条带，存量卷容量、条带数不变
                    编辑 vm 虚拟机卷
                        存量数据
                            存量虚拟机（含奇数容量卷） - 升级后 ，编辑虚拟机磁盘时 - 将已有虚拟卷容量自动 +1 调整为偶数 - 编辑成功，虚拟卷容量为偶数，条带数不变
                            存量虚拟机2副本精简制备 - 集群升级630后，调整存储策略为 3副本后制备 - 编辑成功，使用 4 条带存储策略
                            存量虚拟机 ec2+1 精简制备 - 集群升级630后，调整存储策略为  ec 2+2 厚制备 - 编辑成功，使用 4 条带存储策略
                            存量虚拟机 - 集群升级 630 后，卷 扩容、开启常驻缓存、加密，操作成功
                        新数据
                            630 编辑虚拟机磁盘时 - 调整已有虚拟卷容量为奇数时自动 +1 调整为偶数 - 编辑成功，虚拟卷容量为偶数，条带数 8
                            升级到630 集群 - 新建vm 编辑卷2副本精简 - 调整存储策略为 3 副本后制备 - 编辑成功，使用 8 条带存储策略
                            升级到630 集群 - 新建vm 编辑卷ec 2+1 副本精简 - 调整存储策略为 ec 2+2 厚制备 - 编辑成功，使用 8 条带存储策略
                            升级到630 集群 - 新建vm 编辑卷  - 卷 扩容、开启常驻缓存、加密，操作成功
                    虚拟卷
                        创建虚拟卷 - 输入奇数自动+1 调整为偶数 - 创建成功（共享卷/非共享卷）
                        低版本升级后 vm 克隆存量虚拟卷（奇数） - 克隆卷是奇数卷，条带数不变为4
                        630 vm 克隆虚拟卷 - 克隆卷是偶数数卷，条带数8
                ovf
                    导入导出 vm
                        os630 及以上 ovf 导入vm （含奇数、偶数卷） -  已有卷容量（奇数）自动调整为偶数有提示 - 导入卷 os 630 卷容量偶数、8条带
                        os 630 以下集群，ovf导入 vm - 已有卷容量（奇数）+ 新增卷容量奇数 - 不触发提升为偶数卷提示，导入vm 成功：奇数卷 4 条带
                        (elf630 及以上 + 任意存储）集群，ovf 导入vm （含奇数、偶数卷） -  已有卷容量（奇数）自动调整为偶数有提示 - 导入卷 os 630 卷容量偶数、8条带
                        (elf630 以下 + 任意存储） 集群，ovf导入 vm - 已有卷容量（奇数）+ 新增卷容量奇数 - 不触发提升为偶数卷提示，导入vm 成功：奇数卷 4 条带
                        导出 os 630及以上 虚拟机 - 8 条带偶数卷 - 导出成功
                        导出 （elf630及以上 +任意存储） 虚拟机 - 8 条带偶数卷 - 导出成功
                        os 630及以上, 新导出vm - 重新 ovf 导入vm到集群 -  已有为偶数（无提示）- 创建vm 成功，导入卷、630 卷容量偶数、8条带
                        (elf 630及以上 + 任意存储) 新导出vm -重新 ovf 导入vm 到集群 -  已有为偶数（无提示）- 创建vm 成功，导入卷、630 卷容量偶数、8条带
                    导入导出 模版
                        os630及以上 -  ovf 导入 vm 模版（含奇数、偶数卷） -  已有卷容量（奇数）自动调整为偶数有提示 - 导入卷 os 630 卷容量偶数、8条带
                        os 630 以下集群，ovf 导入 vm 模版 - 已有卷容量（奇数）-  不触发提升为偶数卷提示，导入vm 成功：奇数卷 4 条带
                        zbs 580 以下集群导入虚拟机模版 - 检查卷条带数为 4
                        zbs 580 及以上集群导入虚拟机模版 - 检查卷条带数为 8
                        630 新导出vm 模版，ovf 导入 vm 模版 -  已有为偶数（无提示）、新增卷容量为奇数自动调整为偶数、挂载：630 新建卷（偶数）+ 存量卷 - 创建vm 成功，导入卷、630 卷容量偶数、8条带，挂载的存量卷容量、条带数不变
                        os 630 及以上模版 - 偶数卷 8 条带 - ovf 导出成功
                        任意zbs 上 偶数卷 8 条带模版 - ovf 导出成功
                        zbs 580 及以下 奇数卷 4 条带模版 - ovf 导出成功
                    导入导出虚拟卷
                        os630及以上集群， ovf 导入虚拟卷（奇数） - 提示调整为偶数 - 创建后检查卷是偶数卷，条带数为8
                        os630以下集群，ovf 导入虚拟卷（奇数） -  不提示调整为偶数 - 创建后检查卷保持奇数卷，条带数为4
                        (elf630 及以上 + 任意存储）集群，ovf 导入 奇数卷） -  触发奇数卷自动调整为偶数有提示 - 导入卷卷容量偶数、8条带
                        (elf630 以下 + 任意存储） 集群，ovf导入 奇数卷 - 不触发提升为偶数卷提示，导入卷：容量奇数 4 条带
                        os 630 及以上 偶数卷 8 条带 - 导出虚拟卷成功
                        （elf 630 及以上  + 任意存储）偶数卷 8 条带 - 导出虚拟卷成功
                内容库 iso
                    zbs 580 及以上集群 - url 上传 iso - 检查 条带数 为 4
                    zbs 580 以下集群 - 本地上传 iso - 检查 条带数 为 4
                    os 630 及以上集群 - 本地上传 iso - 检查 条带数 为 4
                    os 630 以下集群 - url 上传 iso - 检查 条带数 为 4
                一键副本提升
                    os 630 集群，新建卷资源 2副本 - 集群一键副本提升副本数 - 提升成功 8 条带 3副本
                    os 620 升级到 630 集群，含 2副本 4 条带和 8 条带数据卷 - 集群一键副本提升副本数 - 提升成功存量资源 4 条带，新建资源 8 条带3副本
                相关组件支持跟踪
                    tower480 及以上 + smtx elf/os 630 及以上 - 各组件各自跟踪，含系统服务虚拟机部署扩容、升级时的配置 - 都需要兼容 使用8条带 容量偶数
                    tower480 及以上 + smtx elf/os 630 以下 - 各组件各自跟踪，含系统服务虚拟机部署扩容、升级时的配置 - 保持使用4 条带 存储策略，可使用奇数卷无提升
                    tower 480及以上 + smtx zbs 580以下 上 - 各组件各自跟踪，含系统服务虚拟机部署扩容、升级时的配置 - 保持使用 4条带存储策略，可使用奇数卷无提示
                    tower 480及以上 + smtx zbs 580及以 上 - 各组件各自跟踪，含系统服务虚拟机部署扩容、升级时的配置 - 需使用 8 条带存储策略 偶数卷
                    v2v:确认目前最新版1.6.1 v2v 迁移 VMware vm 到 os630 卷存储策略副本/ec条带数4 - 后续 v2v 1.7.0 支持8条带V2V-522
                系统配置检查
                    数据有效性检查
                        os/elf 集群 - 检查虚拟卷使用 条带数 ，多种方式
                        zbs 集群上的 vm - 检查虚拟卷使用 条带数
                        获取内容库模版id - tower 内容库 - 查看模版详情 - 模版 url 结尾 uuid 是内容库模版 id
                        graphql 查询：使用模版 id 查询 contentLibraryVmTemplates - 获取zbs 模版的 os 的 vm_templates.vm_disks.path - 然后命令行查询 lun 条带数
                        graphql 查询：使用模版 id 查询 contentLibraryVmTemplates - 获取zbs 模版的 zbs 存的zbs_storage_info.iscsi_lun_snapshot_uuid
                        graphql 查询：使用 iscsi_lun_snapshot_uuid 在 iscsiLunSnapshots 查询 - 获取 该 zbs 模版的 target name、lun_name
                        内容库 iso lun 查看 存储策略方式：zbs 集群在 tower 搜索同名 lun 查看条带，os 集群 fieheye elf api + zbs 命令行【tower 后续优化 TOWER-20670】
                    存储策略配置检查
                        630 新部署集群创建的 elf 默认 default 存储策略 - 条带数为 8
                        630 新部署smtx os 集群，关联至tower，检查：elf 后端只创建 3种8条带存储策略（default 已创建2副本8条带，不在重复创建），新建卷存储策略使用 8 条带数
                        smtx elf 630集群 - 关联至 tower - 只创建8 条带存储策略更新成功
                        smtx os 集群 - 低版本升级 630  - 检查:新建4种副本 8条带存储策略，且新建卷默认存储策略使用带数 8
                        630 新部署smtx os 双活集群，关联至tower，检查：elf 后端只创建 1种 3 副本厚制备的8条带存储策略（default 已创建3副本精简制备 8条带，不再重复创建），新建卷存储策略使用 8 条带数
                        smtx os 双活集群 - 低版本升级 630后 - 只新建3副本精简制备/厚制备的 8条带 存储策略
                        630 新集群以 ec 策略关联至tower - 只创建 4种8 条带存储策略，不创建 ec 策略，只有使用ec 时才创建对应 8 条带存储策略
                        低版本 os 集群关联至 tower480 只创建 4种4条带存储策略
                        POST ​​/api/v2/storage_policies - 新建存储策略：不配置条带数 - 创建出的存储策略使用 8 条带 API 检查测试符合预期-- （其他场景已有 tower 自动痛不集群数据时覆盖）
                        检查集群接口 获取  Get /api/v2/elf/cluster_capabilities  其中包含 supportStoragePolicyStripeNum8 表示集群支持创建条带数 8 的存储策略
                        480 tower 数据同步后 -  关联的 os/elf 630及以上 集群不自动创建 4 条带的存储策略，关联的低版本 os/elf 630 以下不自动创建 8 条带
                        特例：630 以下 低版本集群 - 预期无入口触发创建8条带存储策略（高版本8条带分段/冷迁移到低版本、8条第啊模版分发到0s620，使用 4 条带）
                        特例：630 以下smtx elf 创建8 条带存储策略场景：elf620 + zbs/os630 4条带卷 - 转换/克隆为 vm 过程中 的lun 使用会创建 8 条带存储策略
                        特例：新部署 630及以上 os/elf 创建 4条带存储策略场景：低版本集群热迁移 /分段迁移/冷迁移 到高版本迁移时\\创建、4条带模版创建 vm  时，使用的 4条带存储策略
                        特例：oapi 支持在os/elf 630 及以上集群创建 vm指定 4 条带时 - 自动创建指定的 4条带存储策略
                        低版本的 default 4 条带存储策略 - 升级 630 后这个 default 存储策略预期保持 4条带--tower 有边缘场景使用这里，tower 确认下场景以及是否有影响————————
                变更：TOWER-21056 存量卷支持奇数容量
                    存量数据
                        存量虚拟机（含奇数容量卷） - 升级后 ，编辑虚拟机磁盘时 - 不会将已有虚拟卷容量自动为偶数 - 不会触发已有卷的提示，可继续使用奇数，是4条带
                        存量虚拟机含（奇数+偶数）卷 - 编辑磁盘扩容为偶数：不会触发提示，编辑成功，偶数4条带
                        存量虚拟机（奇数+偶数）卷 - 编辑磁盘扩容为奇数：不会触发提示，编辑成功，奇数4条带
                        存量虚拟机2副本精简制备4条带(奇数+偶数)卷 - 集群升级630后，调整存储策略为 3副本后制备 - 编辑成功，使用 4 条带3副本(奇数+偶数)卷
                        存量虚拟机4条带（奇数+偶数）卷 - 集群升级 630 后，卷 扩容、开启常驻缓存，操作属性开启成功，4条带（奇数+偶数）卷
                        检查编辑已有的（奇数+偶数）卷 - 减少容量 - 保存检查能正确校验到容量不可减少
                        630 集群新建vm，挂在存量（奇数+偶数）卷后 - 编辑虚拟卷 - 不要求必须为偶数，可扩容为奇数成功
                        smtx os 630 集群 - 编辑存量虚拟机可使用（奇数+偶数）卷4条带，新建虚拟卷应使用偶数卷8 条带
                        smtx elf 630 集群 - 编辑存量虚拟机可使用（奇数+偶数）卷4条带，新建虚拟卷应使用偶数卷8 条带
                    630 新建卷
                        低版本升级的存量虚拟机 - 升级 630 后 - 编辑磁盘添加卷，卷容量校验提示需要为偶数，输入奇数时自动向上取整为偶数，8条带
                        630 已新建虚拟机喊8条带偶数卷 - 编辑磁盘：从偶数调整为奇数，有校验提示容量应为偶数，失焦后自动调整为偶数 - 编辑成功，8条带偶数卷
                        新增卷容量为奇数时，操作 copy 卷，copy 触发提示容量应为偶数，点击其他地方容量自动+1 调整为偶数
                        升级到630 集群 - 新建vm 编辑卷2副本精简 - 调整存储策略为 3 副本后制备 - 编辑成功，使用 8 条带存储策略
                        升级到630 集群 - 新建vm 编辑卷  - 卷 扩容、开启常驻缓存，操作成功
                        630 集群新建vm，挂在新建偶数卷后 - 编辑虚拟卷 - 要求必须为偶数，仅可扩容为偶数成功
                    一键提升
                        os 620 升级到 630 集群，含 2副本 4 条带（奇数+偶数）卷和 8 条带偶数卷 - 集群一键副本提升副本数 - 提升成功存量资源：3副本 4 条带（奇数+偶数）卷，新建资源 8 条带偶数卷
                    虚拟卷
                        低版本升级后 vm 克隆存量虚拟卷（奇数） - 克隆卷是奇数卷，条带数不变为4
                        新建卷 - 校验容量必须为偶数 - 创建数据 偶数 8 条带
                变更：TOWER-21071 内容库和 TOWER-20911 迁移
                    迁移
                        集群内迁移
                            确认 虚拟卷条带检查不进行集群内迁移的检查
                        跨集群迁移
                            高版本迁移
                                smtx os 迁移
                                    630 及以上 vm(无需考虑卷条带情况) - 跨集群热迁移 到 smtx os 630以下 - 禁止迁移
                                    630 及以上 vm(无需考虑卷条带情况) - 跨集群热迁移 到 smtx elf 630以下 - 禁止迁移
                                    源端 ：仅 8 条带偶数卷
                                        跨集群热迁移
                                            630 及以上新建 vm 8条带偶数卷 - 跨集群热迁移 到 smtx os 630及以上 - 迁移成功，8条带偶数卷
                                            630 及以上新建 vm 8条带偶数卷 - 跨集群热迁移 到 （smtxelf 630及以上 +任意存储） - 迁移成功，8条带偶数卷
                                        跨集群分段/冷迁移
                                            630 及以上新建 vm 8条带偶数卷 - 跨集群分段迁移 到 smtx os 630及以上 - 迁移成功，8条带偶数卷
                                            630 及以上新建 vm 8条带偶数卷 - 跨集群冷迁移 到 smtx os 630及以上 - 迁移成功，8条带偶数卷
                                            630 及以上新建 vm 8条带偶数卷 - 跨集群分段迁移 到 smtx os 630以下 - 迁移成功，4条带偶数卷
                                            630 及以上新建 vm 8条带偶数卷 - 跨集群冷迁移 到 smtx os 630以下 - 迁移成功，4条带偶数卷
                                    源端：仅4条带（奇数+偶数）卷
                                        跨集群热迁移
                                            smtx os 低版本升级到 630 集群 ：存量：4条带（奇数+偶数）卷 - 跨集群热迁移 到 smtx os 630及以上 - 迁移成功，保持 4条带（奇数+偶数）卷
                                            smtx os 低版本升级到 630 集群 ：存量：4条带（奇数+偶数）卷 - 跨集群热迁移 到 （smtx elf 630及以上 + 任意存储）- 迁移成功，保持 4条带（奇数+偶数）卷
                                        跨集群分段/冷迁移
                                            smtx os 低版本升级到 630 集群 ：存量 4条带（奇数+偶数）卷 - 跨集群分段迁移 到 smtx os 630及以上 - 迁移成功，4条带（奇数+偶数）卷
                                            smtx os 低版本升级到 630 集群 ：存量 4条带（奇数+偶数）卷 - 跨集群冷迁移 到 smtx os 630及以上 - 迁移成功，4条带（奇数+偶数）卷
                                            smtx os 低版本升级到 630 集群：存量4条带（奇数+偶数）卷 - 跨集群分段迁移 到 smtx os 630 以下 - 迁移成功，4条带（奇数+偶数）卷
                                            smtx os 低版本升级到 630 集群：存量4条带（奇数+偶数）卷 - 跨集群冷迁移 到 smtx os 630以下 - 迁移成功，4条带（奇数+偶数）卷
                                    源端：4条带（奇数+偶数）卷 + 8 条带偶数卷
                                        跨集群热迁移
                                            smtx os 低版本升级到 630 集群 ：含 存量4条带（奇数+偶数）卷 + 新增8条带偶数卷  - 跨集群热迁移 到 smtx os 630及以上 - 迁移成功，都使用4 条带卷容量不变：4条带（奇数+偶数）卷+新卷4条带偶数卷）
                                            smtx os 低版本升级到 630 集群 ：含 存量4条带（奇数+偶数）卷 + 新增8条带偶数卷  - 跨集群热迁移 到 （smtx elf 630及以上 + zbs）- 迁移成功，都使用4 条带卷容量不变：4条带（奇数+偶数）卷+新卷4条带偶数卷）
                                        跨集群分段/冷迁移
                                            smtx os 低版本升级到 630 集群 ：含存量4条带（奇数+偶数）卷 + 新增8条带偶数卷  - 跨集群分段迁移 到 smtx os 630及以上 - 迁移成功,存量卷偶数 4条带，新建卷偶数 8条带
                                            smtx os 低版本升级到 630 集群 ：存量4条带（奇数+偶数）卷 + 新增8条带偶数卷  - 跨集群冷迁移 到 smtx os 630及以上 - 迁移成功,存量卷偶数 4条带，新建卷偶数 8条带
                                            smtx os 低版本升级到 630 集群 ：存量4条带（奇数+偶数）卷 + 新增8条带偶数卷 - 跨集群分段迁移 到 smtx os 630以下 - 迁移成功，所有卷使用4 条带
                                            smtx os 低版本升级到 630 集群 ：存量4条带（奇数+偶数）卷 + 新增8条带偶数卷 - 跨集群冷迁移 到 smtx os 630以下 - 迁移成功，所有卷使用4 条带
                                存算分离迁移
                                    【smtx elf1 630级以上 + 任意存储】（不区分条带）迁移计算和存储到 【smtx os 630以下版本】 - 禁止迁移
                                    【smtx elf1 630级以上 + 任意存储】（不区分条带）迁移计算和存储到 【smtx elf2 630及以下版本 + 任意存储】 - 禁止迁移
                                    【smtx elf1 630级以上 + 任意存储】（不区分条带）仅迁移计算到 【smtx elf2 620以下 + 任意存储】 -  禁止迁移
                                    源端：仅8 条带偶数卷
                                        迁移计算 + 存储
                                            【smtx elf1 630级以上 + 任意存储】迁移计算和存储到 【smtx os 630及以上版本】 - 变更存储策略 - 迁移成功 ，8条带偶数卷
                                            【smtx elf1 630级以上 + 任意存储】迁移计算和存储到 【smtx elf2 630及以上版本 + 任意存储】 - 变更存储策略 - 迁移成功 ，8 条带偶数卷
                                        仅迁移计算
                                            【smtx elf1 630级以上 + 任意存储】仅迁移计算到 【smtx elf2 630及以上版本 + 任意存储】 -  迁移成功 ，都使用8条带卷偶数卷
                                        仅迁移存储
                                            【smtx elf1 630级以上 + zbs 570】仅迁移存储到 【smtx elf1 630及以上版本 + os620 】 - 变更存储策略 - 迁移成功 ，都使用8 条带偶数卷
                                    源端：仅4条带（奇数 + 偶数）卷
                                        迁移计算 + 存储
                                            【smtx elf1 630级以上 + 任意存储】迁移计算和存储到 【smtx os 630及以上版本】 - 变更存储策略 - 迁移成功 ，4条带（奇数+偶数）卷
                                            【smtx elf1 630级以上 + 任意存储】迁移计算和存储到 【smtx elf2 630及以上版本 + 任意存储】 - 变更存储策略 - 迁移成功 ，4条带（奇数+偶数）卷
                                        仅迁移计算
                                            【smtx elf1 630级以上 + 任意存储】仅迁移计算到 【smtx elf2 630及以上版本 + 任意存储】 -  迁移成功 ，4条带（奇数+偶数）卷
                                        仅迁移存储
                                            【smtx elf1 630级以上 + zbs 570】仅迁移存储资源到 【smtx elf1 630及以上版本 + os620 】 - 变更存储策略 - 迁移成功 ，4条带（奇数+偶数）卷
                                    源端：4条带（奇数+偶数）卷 + 8 条带偶数卷
                                        迁移计算 +存储
                                            【smtx elf1 630级以上 + 任意存储】迁移计算和存储到 【smtx os 630及以上版本】 - 变更存储策略 - 迁移成功，都使用4 条带卷容量不变：4条带（奇数+偶数）卷+新卷4条带偶数卷）
                                            【smtx elf1 630级以上 + 任意存储】迁移计算和存储到 【smtx elf2 630 及以上版本 + 任意存储】 - 变更存储策略 - 迁移成功 ，都使用4 条带卷容量不变：4条带（奇数+偶数）卷+新卷4条带偶数卷）】
                                        仅迁移计算
                                            【smtx elf1 630级以上 + 任意存储】仅迁移计算到 【smtx elf2 630及以上版本 + 任意存储】 -  迁移成功 ，条带容量不变 4条带（奇数+偶数）卷 + 8 条带偶数卷
                                        仅迁移存储
                                            【smtx elf1 630级以上 + zbs 570】仅迁移存储到 【smtx elf1 630及以上版本 + os620 】 - 变更存储策略 - 迁移成功 ，条带卷容量不变：4条带（奇数+偶数）卷 + 8 条带偶数卷
                            低版本迁移（仅4条带卷 vm）
                                os 跨集群迁移
                                    跨集群热迁移
                                        smtx os 630 以下集群 - 热迁移到 os 630 级以上集群 - 卷容量奇数，4条带
                                        smtx os 630 以下集群 - 热迁移到 【elf 630 及以上 + 任意存储】集群 - 卷容量奇数，4条带
                                        smtx os 630 以下集群 - 热迁移到 【elf 630 以下 + 任意存储】集群 - 卷容量奇数，4条带
                                    跨集群分段/冷迁移
                                        smtx os 630 以下集群 - 分段迁移到 os 630 级以上集群 - 卷容量奇数，4条带
                                        smtx os 630 以下集群 - 冷迁移到 os 630 级以上集群 - 卷容量奇数，4条带
                                存算分离迁移
                                    迁移计算和存储
                                        【smtx elf1 630以下 + 任意存储】迁移计算和存储到 【smtx os 630及以上版本】 - 变更存储策略 - 迁移成功 ，卷容量奇数4条带
                                        【smtx elf1 630以下 + 任意存储】迁移计算和存储到 【smtx elf 630及以上 + 任意存储】 - 变更存储策略 - 迁移成功 ，卷容量奇数4条带
                                        smtx elf 630 以下集群 - 热迁移到 【elf 630 以下 + 任意存储】集群 - 卷容量奇数，4条带
                                    仅迁移计算
                                        【smtx elf1 630以下 + 任意存储】仅迁移计算到 【smtx elf 630及以上版本】 - 迁移成功 ，卷容量奇数4条带
                                        smtx os 630 以下集群 - 热迁移到 【elf 630 以下 + 任意存储】集群 - 卷容量奇数，4条带
                                    仅迁移存储
                                        【smtx elf1 630以下 + 任意存储zbs 564】仅迁移存储到 【smtx elf1 630以下 + os630】 - 迁移成功 ，卷容量奇数4条带
                    内容库模版
                        os620 奇数卷- 分发到os630--删除620 模版-- 创建vm容量仍保持奇数
                        模版- 分发
                            编辑模版所属集群分发
                                仅4条带（奇数+偶数）卷模版
                                    os 上 奇数卷4条带 模版 - 分发到 os 630 以下 - 奇数卷 4 条带
                                    os上 奇数卷4条带 模版 - 分发到 os 630及以上 - 奇数卷 4 条带
                                    os上 奇数卷4条带 模版 - 分发到 zbs - 奇数卷 4 条带
                                    zbs 集群 奇数卷4条带 模版 - 分发到 os 630 以下 - 奇数卷 4 条带
                                    zbs 奇数卷4条带 模版 - 分发到 os 630及以上 - 奇数卷 4 条带
                                    zbs 奇数卷4条带 模版 - 分发到其他 zbs - 奇数卷 4 条带
                                仅8条带（仅偶数卷）模版
                                    os 630 及以上：偶数卷8条带 模版 - 分发到 os 630 以下 - 偶数卷 4 条带
                                    os 630 及以上：偶数卷8条带 模版 - 分发到 os 630 及以上 - 偶数卷 8 条带
                                    os 630 及以上：偶数卷8条带 模版 - 分发到 zbs 以下 - 偶数卷 8 条带
                                    zbs 集群 偶数卷8条带 模版 - 分发到 os 630 以下 - 偶数卷 4 条带
                                    zbs 偶数卷8条带 模版 - 分发到 os 630及以上 - 偶数卷 8 条带
                                    zbs 偶数卷8条带 模版 - 分发到其他 zbs - 偶数卷 8 条带
                                4条带（奇数+偶数）卷 + 8 条带偶数卷模版
                                    os 630 及以上：4条带（奇数+偶数）卷 + 8 条带偶数卷模版 - 分发到 os 630 以下 - 4条带（奇数+偶数）卷 + 4条带偶数卷模版
                                    os 630 及以上：4条带（奇数+偶数）卷 + 8 条带偶数卷模版 -  分发到 os 630 及以上 - 4条带（奇数+偶数）卷 + 8 条带偶数卷模版
                                    os 630 及以上：4条带（奇数+偶数）卷 + 8 条带偶数卷模版 -  分发到 zbs 集群 - 4条带（奇数+偶数）卷 + 8 条带偶数卷模版
                                    zbs 集群：4条带（奇数+偶数）卷 + 8 条带偶数卷模版 - 分发到 os 630 以下 - 4条带（奇数+偶数）卷 + 4条带偶数卷模版
                                    zbs 集群：4条带（奇数+偶数）卷 + 8 条带偶数卷模版 -  分发到 os 630 及以上 - 4条带（奇数+偶数）卷 + 8 条带偶数卷模版
                                    zbs 集群：4条带（奇数+偶数）卷 + 8 条带偶数卷模版 -  分发到 zbs 集群 - 4条带（奇数+偶数）卷 + 8 条带偶数卷模版
                            集群 - 模版创建vm - 分发
                                os630及以上 集群模版创建 vm - 选择含4条带奇数卷模版 - 创建vm 成功，分发后模版4条带奇数卷，创建的 vm 卷 4条带奇数卷
                                （elf 630及以上 + 任意存储）集群模版创建 vm - 选择含4条带奇数卷模版 - 创建vm 成功，分发后模版4条带奇数卷，创建的 vm 卷 4条带奇数卷
                                os630及以下 集群模版创建 vm - 选择含8条带模版 - 创建vm 成功，分发后模版4条带卷，创建的 vm 卷 4条带卷
                                （elf630及以下 + 存储 os630及以上/zbs）集群模版创建 vm - 选择含8条带模版 - 创建vm 成功，分发后模 zbs 上保持8条带卷，创建的 vm 卷 8条带卷 （存储集群是 os630 以下 时保持 4 条带）
                        smtx os 集群使用
                            vm 克隆为模版
                                os 630 及以上集群
                                    os630 及以上（8条带偶数卷） vm - 克隆为模版 - 8条带偶数卷
                                    os630 及以上（4条带奇数卷+偶数卷） vm - 克隆为模版 - 容量条带不变：4条带（奇数+偶数）卷
                                    os630 及以上 【存量4条带（奇数+偶数）卷 + 新增 8条带偶数卷】 vm - 克隆为模版 - 容量条带不变：【存量4条带（奇数+偶数）卷 + 新增8 条带偶数卷】
                                os 630 以下 集群
                                    os630 以下（4条带奇数卷+偶数卷） vm - 克隆为模版 - 奇数卷、偶数卷都是 4 条带
                            vm 转化为模版
                                os 630 及以上集群
                                    os630 及以上（8条带偶数卷） vm - 转化为模版 - 8条带偶数卷
                                    os630 及以上（4条带奇数卷+偶数卷） vm - 转化为模版 - 容量条带不变：4条带（奇数+偶数）卷
                                    os630 及以上【存量4条带（奇数+偶数）卷 + 新增 8条带偶数卷】vm - 转化为模版 - 容量条带不变：【存量4条带（奇数+偶数）卷 + 新增 8条带偶数卷】
                                os 630 以下集群
                                    os630 以下（4条带奇数卷+偶数卷） vm - 转化为模版 - 奇数卷、偶数卷都是 4 条带
                            模版克隆为虚拟机
                                os 集群
                                    os 630 及以上模版
                                        仅 8 条带 偶数卷模版
                                            克隆为 os 630 及以上 vm - 偶数卷 8 条带
                                            克隆为 os 630 以下（含分发） vm - 偶数卷 4 条带
                                        4条带（奇数+偶数卷）模版
                                            克隆为 os 630 及以上 vm，并新增卷 - 已有卷：（奇数+偶数）卷 4 条带，新增卷：偶数 8 条带
                                            克隆为 os 630 以下（含分发） vm - （奇数+偶数）卷 4 条带
                                        4条带（奇数+偶数）卷 + 8 条带偶数卷模版
                                            克隆为 os 630 及以上 vm - 4条带（奇数+偶数）+8条带偶数卷
                                            克隆为 os 630 以下 vm（含分发） - 4条带（奇数+偶数）卷 + 4 条带偶数卷模版
                                    os 630 以下 - 4条带（奇数+偶数）卷模版
                                        克隆为 os 630 以下 vm - （奇数+偶数）卷 4 条带
                                        克隆为 os 630 以上 vm（含分发） - （奇数+偶数）卷 4 条带
                            模版转化为虚拟机
                                os 630 及以上模版
                                    仅含8条带 偶数卷模版
                                        转化为 os 630 及以上 vm - 偶数卷 8 条带
                                    4条带（奇数+偶数卷）模版
                                        转换到 os630  集群 -  4条带（奇数+偶数）卷
                                    4条带（奇数+偶数卷） + 8条带偶数卷 - 模版
                                        转换到 os630  集群 - 条带容量不变：4条带（奇数+偶数）卷 + 8 条带偶数卷
                                os 630 以下 - 4条带（奇数+偶数）卷模版
                                    转化为 os 630 以下 vm - （奇数+偶数）卷 4 条带
                        存算分离集群使用
                            vm 克隆为模版
                                elf630 及以上
                                    8 条带偶数卷模版  vm
                                        【elf630 及以上 + os 630以下】（8条带偶数卷） vm  - 克隆为模版 - 降级为 4条带偶数卷
                                        【elf630 及以上 + os 630及以上】（8条带偶数卷） vm  - 克隆为模版 - 8 条带偶数卷
                                        【elf630 及以上 + 任意zbs：zbs564 】（8 条带偶数卷） vm  - 克隆为模版 - 8 条带偶数卷
                                        【elf630 及以上 + 任意zbs：zbs570】（8 条带偶数卷） vm  - 克隆为模版 - 8 条带偶数卷
                                    4条带（奇数+偶数）卷  vm
                                        【elf630 及以上 + os 630以下】（4条带奇数卷+偶数卷） vm  - 克隆为模版 - 奇数卷、偶数卷都是 4 条带
                                        【elf630 及以上 + os 630及以上】（4条带奇数卷+偶数卷） vm  - 克隆为模版 - 容量条带不变：4条带（奇数+偶数）卷
                                        【elf630 及以上 + 任意zbs：zbs564 】（4条带奇数卷+偶数卷） vm  - 克隆为模版 - 容量条带不变：4条带（奇数+偶数）卷
                                        【elf630 及以上 + 任意zbs：zbs570】（4条带：奇数卷+偶数卷） vm  - 克隆为模版 - 容量条带不变：4条带（奇数+偶数）卷
                                    4条带（奇数+偶数）卷 + 8 条带偶数卷 vm
                                        【elf630 及以上 + os 630以下】4条带（奇数+偶数）卷 + 8 条带偶数卷 vm  - 克隆为模版 - 4条带（奇数+偶数）卷 + 4条带偶数卷
                                        【elf630 及以上 + os 630及以上】 4条带（奇数+偶数）卷 + 8条带偶数卷 vm  - 克隆为模版 -  容量条带不变：4条带（奇数+偶数）卷 + 8条带偶数卷
                                        【elf630 及以上 + 任意zbs：zbs564 】 4条带（奇数+偶数）卷 + 8条带偶数卷 vm  - 克隆为模版 - 容量条带不变： 4条带（奇数+偶数）卷 + 8条带偶数卷
                                        【elf630 及以上 + 任意zbs：zbs570】 4条带（奇数+偶数）卷 + 8条带偶数卷 vm  - 克隆为模版 - 容量条带不变： 4条带（奇数+偶数）卷 + 8条带偶数卷
                                elf630 及以下
                                    【elf630 以下 + os 630以下】（4条带奇数卷+偶数卷） vm  - 克隆为模版 - 奇数卷、偶数卷都是 4 条带
                                    【elf630 以下 + os 630及以上】（4条带奇数卷+偶数卷） vm  - 克隆为模版 - 条带容量不变：4条带奇数卷+偶数卷
                                    【elf630 以下 + 任意zbs：zbs564 】（4条带奇数卷+偶数卷） vm  - 克隆为模版 - 条带容量不变：4条带奇数卷+偶数卷
                                    【elf630 以下 + 任意zbs：zbs570】（4条带奇数卷+偶数卷） vm  - 克隆为模版 - 条带容量不变：4条带奇数卷+偶数卷
                            vm 转化为模版
                                elf 630 及以上
                                    8 条带偶数卷模版  vm
                                        【os630 及以上 + os 630以下】（8条带偶数卷） vm  - 转化为模版 - 降级为 4条带偶数卷
                                        【os630 及以上 + os 630及以上】（8条带偶数卷） vm  - 转化为模版 - 8 条带偶数卷
                                        【os630 及以上 + 任意zbs：zbs564 】（8 条带偶数卷） vm  - 转化为模版 - 8 条带偶数卷
                                        【os630 及以上 + 任意zbs：zbs570】（8 条带偶数卷） vm  - 转化为模版 - 8 条带偶数卷
                                    4条带（奇数+偶数）卷 vm
                                        【os630 及以上 + os 630以下】4条带（奇数+偶数）卷 vm  - 转化为模版 - 奇数卷、偶数卷都是 4 条带
                                        【os630 及以上 + os 630及以上】4条带（奇数+偶数）卷 vm  - 转化为模版 - 容量条带不变：4条带（奇数+偶数）卷
                                        【os630 及以上 + 任意zbs：zbs564 】4条带（奇数+偶数）卷 vm  - 转化为模版 - 容量条带不变：4条带（奇数+偶数）卷
                                        【os630 及以上 + 任意zbs：zbs570】4条带（奇数+偶数）卷 vm  - 转化为模版 - 容量条带不变：4条带（奇数+偶数）卷
                                    4条带（奇数+偶数）卷 + 8 条带偶数卷 vm
                                        【os630 及以上 + os 630以下】4条带（奇数+偶数）卷 + 8 条带偶数卷 vm  - 转化为模版 - 4条带（奇数+偶数）卷 + 4 条带偶数卷 vm
                                        【os630 及以上 + os 630及以上】4条带（奇数+偶数）卷 + 8 条带偶数卷 vm   - 转化为模版 - 容量条带不变： 4条带（奇数+偶数）卷 + 8条带偶数卷
                                        【os630 及以上 + 任意zbs：zbs564 】4条带（奇数+偶数）卷 + 8 条带偶数卷 vm - 转化为模版 - 容量条带不变： 4条带（奇数+偶数）卷 + 8条带偶数卷
                                        【os630 及以上 + 任意zbs：zbs570】4条带（奇数+偶数）卷 + 8 条带偶数卷 vm - 转化为模版 - 容量条带不变： 4条带（奇数+偶数）卷 + 8条带偶数卷
                                elf 630 及以下
                                    【os630 以下 + os 630以下】（4条带奇数卷+偶数卷） vm  - 转化为模版 - 4条带奇数卷+偶数卷
                                    【os630 以下 + os 630及以上】（4条带奇数卷+偶数卷） vm  - 转化为模版 - 4条带奇数卷+偶数卷
                                    【os630 以下 + 任意zbs：zbs564 】（4条带奇数卷+偶数卷） vm  - 转化为模版 - 4条带奇数卷+偶数卷
                                    【os630 以下 + 任意zbs：zbs570】（4条带奇数卷+偶数卷） vm  - 转化为模版 - 4条带奇数卷+偶数卷
                            模版克隆为虚拟机
                                os 模版
                                    630 及以上模版
                                        8 条带 偶数卷模版
                                            克隆为 elf 630 及以上 + os 630 及以上 vm，新增卷 - 都是偶数卷 8 条带
                                            克隆为 elf 630 以下 + os 630以上的 vm，新增卷 - 已有卷偶数卷 8 条带，新增卷奇数4条带【特例】
                                        4条带（奇数+偶数卷）模版
                                            克隆为 elf 630 及以上 + os 630及以上 的 vm，并新增卷 - 已有卷 4条带（奇数+偶数卷）模版，新增卷 偶数 8 条带
                                            克隆为 elf 630 以下 + os 630及以上 的 vm，并新增卷 - 已有卷 4条带（奇数+偶数卷）模版，新增卷 偶数 4 条带
                                        4条带（奇数+偶数）卷 + 8 条带偶数卷模版
                                            克隆为 elf 630 及以上 + os 630及以上 的 vm ，并新增卷 - 已有卷：4条带（奇数+偶数）卷 + 8 条带偶数卷模版 ，新增卷偶数8条带
                                            克隆为 elf 630 以下 + os 630及以上 的 vm ，并新增卷 - 已有卷：4条带（奇数+偶数）卷 + 8 条带偶数卷模版 ，新增卷奇数4条带【特例】
                                    630 及以下 4条带 奇数+偶数卷模版
                                        克隆为 elf 630 以上 + os 630 以下 vm，并新增卷 - 已有卷：4条带（奇数+偶数）卷 ，新增卷偶数 8 条带
                                        克隆为 elf 630 以下 + os 630 以下 vm，并新增卷 - 已有卷：4条带（奇数+偶数）卷 ，新增卷奇数 4 条带
                                zbs 模版
                                    zbs 8 条带 偶数卷模版
                                        克隆为 elf 630 及以上 + zbs 的 vm，并新增卷 - 都是偶数卷 8 条带
                                        克隆为 elf 630 以下 +  zbs 的 vm，并新增卷奇数 - 已有卷偶数卷 8 条带，新增卷奇数 4 条带【特例】
                                    zbs 4 条带（奇数+偶数）卷模板
                                        克隆为 elf 630 及以上 + zbs 的 vm，并新增卷 - 已有卷： 4 条带（奇数+偶数），新增卷：偶数8条带
                                        克隆为 elf 630 以下 + zbs 的 vm，并新增卷奇数 - 已有卷： 4 条带（奇数+偶数）卷，新增卷奇数4条带
                                    zbs:4条带（奇数+偶数）卷 + 8 条带偶数卷模版
                                        克隆为 elf 630 及以上 + zbs 的 vm，并新增卷 - 已有卷：4条带（奇数+偶数）卷 + 8 条带偶数，新增卷：偶数8条带
                                        克隆为 elf 630 以下 + zbs 的 vm，并新增卷奇数 - 已有卷：4条带（奇数+偶数）卷 + 8 条带偶数，新增卷奇数4条带
                            模版转化为虚拟机
                                os 模版
                                    630 及以上 模版
                                        8 条带 偶数卷模版
                                            转化为 elf 630 及以上 + os 630 以上 vm - 偶数卷 8 条带
                                            转化为 elf 630 以下 + os 630以上的 vm - 偶数卷 8 条带 ！！！
                                        4条带（奇数+偶数卷）模版
                                            转换到 elf630 及以上 + os630及以上的 vm -   4 条带(奇数卷+ 偶数卷）
                                            转换到 elf630 以下 + os630及以上的 vm -  4 条带(奇数卷+ 偶数卷）
                                        4条带（奇数+偶数）卷 + 8 条带偶数卷模版
                                            转换到 elf630 及以上 + os630及以上的 vm -  4条带（奇数+偶数）卷 + 8 条带偶数卷
                                            转换到 elf630 以下+ os630及以上的 vm -  4条带（奇数+偶数）卷 + 8 条带偶数卷！！！
                                    os630 以下 4 条带奇数卷模板
                                        转化为 elf 630 以下 + os 630 以下 vm - 奇数卷 4 条带
                                        转化为 elf 630 以上 + os 630 以下 vm - 奇数卷 4 条带
                                zbs 模版
                                    zbs 8 条带 偶数卷模版
                                        转化为 elf 630 以上 + zbs 的 vm - 偶数卷 8 条带
                                        转化为 elf 630 以下 +  zbs 的 vm - 偶数卷 8 条带！！！
                                    zbs 4 条带 奇数卷模板
                                        转化为 elf 630 以上 + zbs 的 vm - 奇数卷 4 条带
                                        转化为 elf 630 以下 + zbs 的 vm - 奇数卷 4 条带
                                    zbs:4条带（奇数+偶数）卷 + 8 条带偶数卷
                                        转化为 elf 630 以上 + zbs 的 vm - 4条带（奇数+偶数）卷 + 8 条带偶数卷
                                        转化为 elf 630 以下 +  zbs 的 vm - 4条带（奇数+偶数）卷 + 8 条带偶数卷！！！
                2025-10-31 版本内容库+迁移用例，废弃
                    模版
                        vm 克隆为模版
                            smtx os
                                630 以下集群 os 存量vm(含奇数卷) - 快速拷贝 克隆 为 os 630 及以上 模版成功 - 模版卷容量（奇数）、条带不变 ---- 是否还检查模版快速拷贝到 smtx os630/zbs 580 以下集群的回归？？
                                630 以下 os 集群 存量vm(含奇数卷) - 升级后快速拷贝 克隆 为 os 630及以上 模版成功 - 模版卷容量（奇数）、条带不变
                                os 630 vm - 快速拷贝 克隆 为os 630（8条带）模版成功 - 模版卷容量偶数、条带8
                                os 630 vm - 快速拷贝 克隆 为 zbs（8条带）模版成功 - 模版卷容量偶数、条带8
                                os 630 vm - 快速拷贝 克隆 为低版本（630 以下os 集群）模版 - 禁止选择低版本 os 集群，提示原因：不支持条带数为 8 的虚拟卷（若一个集群符合多种禁用原因，按照以上编号顺序展示）
                            smtx elf +zbs
                                smtx elf 620 +zbs 570 存量vm(含奇数卷) - 快速拷贝 克隆 为 zbs580 及以上 模版成功 - 模版卷容量（奇数）、条带不变 ---- 是否还检查模版快速拷贝到 smtx os630/zbs 580 以下集群的回归？？
                                smtx elf 620 +zbs 570 存量vm(含奇数卷) - smtx elf 升级630 后快速拷贝 克隆 为 zbs 580 及以上 模版成功 - 模版卷容量（奇数）、条带不变
                            os 和 elf+zbs 交互
                                630 以下 os 集群 存量vm(含奇数卷) - 升级后快速拷贝 克隆 为 os 630及以上 模版成功 - 模版卷容量（奇数）、条带不变
                                630 以下 os 集群存量vm(含奇数卷) - 升级后快速拷贝 克隆 为 zbs 及以上 模版成功 - 模版卷容量（奇数）、条带不变
                                os 630 vm - 快速拷贝 克隆 为 zbs 模版 - 创建成功 - 模版容量偶数、8条带
                                os 630 vm - 快速拷贝 克隆 为 zbs 模版 - 创建成功 - 模版容量偶数、8条带
                                smtx elf 620 +zbs 570 存量vm(含奇数卷) - smtx elf 升级630 后快速拷贝 克隆 为模版 - 禁止克隆为 os 630 以下的模版
                        模版 分发
                            模版转化为 vm
                                630 os 存量卷+含8 条带卷的虚拟机模版 - 转化到 smtx os 630 以上集群，转化成功，存量卷容量条带不变，630 卷容量不变、8条带
                                630os 存量卷+含8 条带卷的虚拟机模版 - 转化到 smtx elf 630 以上集群，转化成功，存量卷容量条带不变，630 卷容量不变、8条带
                                630 os 存量卷+含8 条带卷的虚拟机模版 - 转化到 smtx os 630 以下集群，禁止转化
                                630 os 存量卷+含8 条带卷的虚拟机模版 - 转化到 smtx elf 630 以下集群，禁止转化
                                zbs 存量卷+含8 条带卷的虚拟机模版 - 转化到 smtx os 630 以上集群，转化成功，存量卷容量条带不变，630 卷容量不变、8条带
                                zbs 存量卷+含8 条带卷的虚拟机模版 - 转化到 smtx elf 630 以上集群，转化成功，存量卷容量条带不变，630 卷容量不变、8条带
                                zbs 存量卷+含8 条带卷的虚拟机模版 - 转化到 smtx os 630 以下集群，禁止转化
                                zbs 存量卷+含8 条带卷的虚拟机模版 - 转化到 smtx elf 630 以下集群，禁止转化
                            编辑模版所属集群
                                smtx os 630 上：存量卷+含8 条带卷的虚拟机模版 - 分发到 os 630 级以上集群，分发成功，存量卷容量条带不变，630 卷容量不变、8条带
                                smtx os 630 上：含8 条带的虚拟机模版 - 分发到 os 630 级以下集群，禁止分发成功
                                smtx os 630 上：存量卷+含8 条带卷的虚拟机模版 - 分发到 zbs 集群，分发成功，存量卷容量条带不变，630 卷容量不变、8条带
                                smtx zbs上：存量卷+含8 条带卷的虚拟机模版 - 分发到 zbs 集群，分发成功，存量卷容量条带不变，630 卷容量不变、8条带
                                smtx zbs 上：存量卷+含8 条带卷的虚拟机模版 - 分发到 smtx os 630 级以上 集群，分发成功，存量卷容量条带不变，630 卷容量不变、8条带
                                smtx zbs 上：存量卷+含8 条带卷的虚拟机模版 - 分发到 630 以下集群，禁止分发
                            模克隆创建 vm
                                630 以下集群 存量模版 - 从模版（包含奇数卷）创建vm - 原虚拟卷容量不变，不自动调整为偶数，条带数不变
                                630 以下集群 存量模版 - 新增卷容量奇数自动调整为偶数，创建成功，检查创建卷条带数为8
                                630 以下集群 存量模版 - 从模版创建虚拟机 - 挂载630 新建卷（偶数）、存量卷 - 创建vm 成功，630 卷 容量偶数、8条带，存量卷条带数不变
                                os 630 模版 - 已有卷是偶数8条带、新增卷容量为奇数自动调整为偶数、挂载：630 新建卷（偶数）+ 存量卷 - 创建vm 成功，630 卷容量偶数、 8条带，存量卷容量、条带数不变
                                630 os 存量卷+含8 条带卷的虚拟机模版 - smtx os 630 以上集群，克隆创建vm成功，存量卷容量条带不变，630 卷容量不变、8条带
                                630os 存量卷+含8 条带卷的虚拟机模版 - smtx elf 630 以上集群，克隆创建vm成功，存量卷容量条带不变，630 卷容量不变、8条带
                                630 os 存量卷+含8 条带卷的虚拟机模版 - 克隆创建vm到 smtx os 630 以下集群，禁止创建
                                630 os 存量卷+含8 条带卷的虚拟机模版 - 克隆创建vm到 smtx elf 630 以下集群，禁止创建
                                zbs 存量卷+含8 条带卷的虚拟机模版 - smtx os 630 以上集群，克隆创建vm成功，存量卷容量条带不变，630 卷容量不变、8条带
                                zbs 存量卷+含8 条带卷的虚拟机模版 - smtx elf 630 以上集群，克隆创建vm成功，存量卷容量条带不变，630 卷容量不变、8条带
                                zbs 存量卷+含8 条带卷的虚拟机模版 - 克隆创建vm到 smtx os 630 以下集群，禁止创建
                                zbs 存量卷+含8 条带卷的虚拟机模版 - 克隆创建vm到 smtx elf 630 以下集群，禁止创建
                        vm 转化为模版
                            smtx os
                                630 以下 os 集群 存量vm(含奇数卷) - 快速拷贝 转化 为 os 630 及以上 集群模版成功 - 模版卷容量（奇数）、条带不变
                                630 以下 os 集群 存量vm(含奇数卷) - 升级后快速拷贝 转化 为 os630 及以上 集群模版成功 - 模版卷容量（奇数）、条带不变
                                os 630 vm - 快速拷贝 转化 为os 630（8条带）模版成功 - 模版卷容量偶数、条带8
                                630 vm - 快速拷贝 转化 为低版本（630 以下os 集群）模版 - 禁止选择低版本 os 集群，提示原因：不支持条带数为 8 的虚拟卷（若一个集群符合多种禁用原因，按照以上编号顺序展示）
                            smtx os  和 elf+zbs 交互
                                os-->zbs
                                    630 以下 os 集群 存量vm(含奇数卷) - 升级后快速拷贝 转化 为 zbs 580 及以上  集群模版成功 - 模版卷容量（奇数）、条带不变
                                    os 630 vm - 快速拷贝 转化 为 zbs580及以上 模版 - 创建成功 - 模版容量偶数、8条带
                                    os 630 vm - 快速拷贝 转化 为 zbs 580 以下 模版 - 禁止创建
                    迁移
                        集群内迁移
                            SMTX OS 存量虚拟机（含奇数卷）- 集群内热迁移 - 卷容量、条带数不变
                            SMTX OS 虚拟机（含奇数卷） - 集群内冷迁移 - 卷容量、条带数不变
                            SMTX OS 630 新建虚拟机 - 集群内热迁移 - 卷容量偶数、条带数8
                            SMTX OS 630 新建虚拟机 - 集群内冷迁移 - 卷容量偶数、条带数8
                            smtx elf 630  存量虚拟机（含奇数卷）-  集群内热迁移 - 卷容量、条带数不变
                            smtx elf 630  存量虚拟机（含奇数卷）-  集群内冷迁移 - 卷容量、条带数不变
                            smtx elf 630  新建虚拟机 -  集群内热迁移 - 卷容量偶数、条带数8
                            smtx elf 630  新卷虚拟机（含奇数卷）-  集群内冷迁移 - 卷容量偶数、条带数8
                        跨集群迁移
                            smtx os 迁移
                                smtx os 低版本升级到 630 集群 ：仅含存量卷（4条带）- 跨集群热迁移 到 smtx os 630以下 - 不支持迁移到低版本，禁止迁移
                                smtx os 低版本升级到 630 集群 ：仅含存量卷（4条带） - 跨集群热迁移 到 （smtx elf 630以下 + zbs）-  - 不支持迁移到低版本，禁止迁移
                                smtx os 低版本升级到 630 集群 ：含存量卷（4条带）+新增8条带卷 - 跨集群热迁移 到 smtx os 630及以上 - 迁移成功,存量卷容量、条带不变，新建卷容量不变、条带8
                                smtx os 低版本升级到 630 集群 ：含存量卷（4条带）+新增8条带卷 - 跨集群热迁移 到 （smtx elf 630及以上 + zbs）- 迁移成功,存量卷容量、条带不变，新建卷容量不变、条带8
                                smtx os 低版本升级到 630 集群 ：含存量卷（4条带）+新增8条带卷 - 跨集群热迁移 到 smtx os 630以下 - 禁止迁移
                                smtx os 低版本升级到 630 集群 ：含存量卷（4条带）+新增8条带卷 - 跨集群热迁移 到 （smtx elf 630以下 + zbs）- 禁止迁移
                                smtx os 低版本升级到 630 集群 ：含存量卷（4条带）+新增8条带卷 - 跨集群分段迁移 到 smtx os 630以下 - 迁移成功使用目标集群的存储策略
                                smtx os 低版本升级到 630 集群 ：含存量卷（4条带）+新增8条带卷 - 跨集群冷迁移 到 smtx os 630以下 - 迁移成功使用目标集群的存储策略
                            smtx elf 迁移
                                仅迁移计算
                                    含 8条带的虚拟机 smxt elf1+zbs1 - 仅迁移计算到 630及以上 smtx elf2+zbs1 - 迁移成功，新建卷容量不变、条带8
                                    含 8条带的虚拟机 smxt elf1+zbs1 - 仅迁移计算到 630以下 smtx elf2+zbs1 - 禁止迁移
                                仅迁移存储
                                    含 8 条带的虚拟机，仅迁移存储： smtxelf1+zbs1 到 smtxelf1+zbs2 -  迁移成功,存量卷容量 条带求不变,新建卷偶数，条带8
                                    含 8 条带的虚拟机，仅迁移存储： smtxelf1+zbs1 到 smtxelf1+os-  迁移成功,存量卷容量 条带求不变,新建卷偶数，条带8
                                    含 8 条带的虚拟机，仅迁移存储： smtxelf1+os 到 smtxelf1+zbs2 -  迁移成功,存量卷容量 条带求不变,新建卷偶数，条带8
                                迁移计算 +存储
                                    smtx elf 含存量+8条带虚拟卷 - 迁移计算+存储 630及以上 smtxelf1+zbs1 到 630及以上smtxelf2+zbs2  - 迁移成功,存量卷容量 条带求不变,新建卷偶数，条带8
                                    smtx elf 含存量+8条带虚拟卷 - 迁移计算+存储 630及以上 smtxelf1+zbs1 到 630及以上smtxelf2+os  - 迁移成功,存量卷容量 条带求不变,新建卷偶数，条带8
                                    smtx elf 含存量+8条带虚拟卷 - 迁移计算+存储 630及以上 smtxelf1+zbs1 到 630及以上smtxos - 迁移成功,存量卷容量 条带求不变,新建卷偶数，条带8
                                    smtx elf 含存量+8条带虚拟卷 - 迁移计算+存储 630及以上 smtxos 到 630及以上smtxelf2+zbs2  - 迁移成功,存量卷容量 条带求不变,新建卷偶数，条带8
                                    smtx elf 含存量+8条带虚拟卷 - 迁移计算+存储 630及以上 smtxelf1+zbs1 到 630及以下smtxelf2+zbs2 - 禁止迁移
                                    smtx elf 含存量+8条带虚拟卷 - 迁移计算+存储 630及以上 smtxelf1+zbs1 到 630及以下smtxelf2+os - 禁止迁移
                                    smtx elf 含存量+8条带虚拟卷 - 迁移计算+存储 630及以上 smtxelf1+zbs1 到 630及以下smtxos- 禁止迁移
                                    smtx elf 含存量+8条带虚拟卷 - 迁移计算+存储 630及以上 smtxos 到 630及以下smtxelf+zbs - 禁止迁移
            ELF-7857 修改 SMTX OS 下 ELF 服务的选主方式
                新部署集群
                    默认使用 v2 Leader 方案
                升级场景（ 620 升级到 630 ）
                    升级过程中
                        升级过程中， 查询选主方案从 v1 切换为 v2【校验实际不好把握，升级后确认切换到 v2 也可以】
                    升级后检查
                        查询选主方案为 v2 Leader
                        ha leader 主机的  ha 服务最晚启动
                        检查升级期间没有 ha 发生
                Leader 方案切换
                    630 集群关闭 v2 Leader 方案，回退到 v1 Leader
                    630 集群在 v1 Leader 的环境下，打开 v2 Leader
                故障测试
                    关联服务主节点，关联服务故障
                        elf-vm-scheduler 主节点服务 stop， 检查服务主节点正确切换
                        elf-vm-monitor 主节点服务 stop， 检查服务主节点正确切换
                        elf-exporter 主节点服务 stop， 检查服务主节点正确切换
                        elf-fs 主节点服务 stop， 检查服务主节点正确切换
                    zk 主节点， zk 服务故障
                        zk leader stop zk 服务，检查 elf-fs ， elf-vm-scheduler， elf-vm-monitor， elf-exporter  的 leader 都没有发生切换
                    zk leader 主机故障， 检查关联功能
                        zk leader 主机故障 -  存储网络故障
                            HA（不同 HA 类型分别检查）
                                故障场景：主机异常， 触发 HA 故障重建
                                故障场景：虚拟机状态异常， 触发 HA 本地重建
                                故障场景：虚拟机网络故障， 触发 HA 故障重建
                                故障场景：虚拟机网络故障， 触发热迁移虚拟机
                                故障场景：虚拟机操作系统故障， 触发虚拟机重启
                            集群内热迁移
                                源端主机 zk leader 故障（ifdown port-storage），故障主机的虚拟机发起集群内热迁移， 迁移失败
                                目标主机 zk leader 故障（ifdown port-storage），故障主机的虚拟机发起集群内热迁移， 迁移失败
                            跨集群热迁移
                                源集群源主机 zk leader 故障（ifdown port-storage），触发跨集群热迁移,  迁移失败
                                目标集群目标主机 zk leader 故障（ifdown port-storage），触发跨集群热迁移， 任务失败
                            ELF 监控
                                zk leader 故障（ifdown port-storage），非故障主机的检查数据是否可以正常采集和展示以及数据没有断开
                            ELF 报警
                                zk leader 故障（ifdown port-storage），报警不应该被误触发
                            OVF 导入导出
                                zk leader 故障（ifdown port-storage），OVF 导入导出任务成功
                        zk leader 主机故障 -  关机
                            HA（不同 HA 类型分别检查）
                                故障场景：主机异常， 触发 HA 故障重建
                                故障场景：虚拟机状态异常， 触发 HA 本地重建
                                故障场景：虚拟机网络故障， 触发 HA 故障重建
                                故障场景：虚拟机网络故障， 触发热迁移虚拟机
                                故障场景：虚拟机操作系统故障， 触发虚拟机重启
                            集群内热迁移
                                源端主机 zk leader 故障（zk stop），故障主机的虚拟机发起集群内热迁移
                                目标主机 zk leader 故障（zk stop），故障主机的虚拟机发起集群内热迁移
                            跨集群热迁移
                                源集群源主机 zk leader 故障（zk stop），触发跨集群热迁移
                                目标集群目标主机 zk leader 故障（zk stop），触发跨集群热迁移
                            ELF 监控
                                zk leader 故障（zk stop），检查数据是否可以正常采集和展示以及数据没有断开
                            ELF 报警
                                zk leader 故障（zk stop），报警不应该被误触发
                            OVF 导入导出
                                zk leader 故障（zk stop），OVF 导入导出任务成功
            630-常住缓存允许使用精简制备
                UI
                    各入口常驻缓存 tooltip 内文案更新 - 只显示 【启用常驻缓存后，%卷类型%的数据将保留在缓存层，从而获得更稳定的高性能。 】删除【设置为常驻缓存的%卷类型%必须使用厚置备的存储策略。】
                    smtx os 及以上集群 - 创建虚拟卷 - 开启常驻缓存  - 保持默认精简制备，无【“启用常驻缓存时展示的”Tip】
                    smtx os 630 及以上 各方式创建/编辑vm 操作虚拟卷 - 开启常住缓存- 卷保持默认精简制备，无【“启用常驻缓存时展示的”Tip】
                    smtx elf630 级以上+ os630/zbs570 -  各方式创建/编辑vm 操作虚拟卷 - 开启常住缓存- 卷保持默认精简制备，无【“启用常驻缓存时展示的”Tip】
                    smxelf630 + os630/zbs570 以下存储，检查创建 vm 、卷开启常驻缓存时，常驻缓存的topltip说明、必须使用厚制备的tip，都应使用630 以下旧版本提示
                    检查启用常驻缓存时 - 允许编辑制备方式，精简制备、厚制备可自动选择
                    源数据的存储策略（开启常驻缓存厚制备） - 克隆卷保持与源一致（开启常驻缓存厚制备），可手动调整制备方式、是否开启常驻缓存
                    编辑 vm 虚拟机卷 - 已开启常驻缓存的卷 - 关闭常驻缓存时触发提示：【关闭常驻缓存后可能导致存储空间回收操作失败，可通过重启虚拟机恢复。】 - 进 os/elf 630 级以上版本支持，低版本无该提示
                vm 操作
                    不同集群类型 - 创建 vm
                        smtx os 630 创建空白虚拟机 创建 vm 含 副本卷+ ec 卷 开启常驻缓存 精简制备、开启常驻缓存 厚制备 4种卷 - 创建成功，卷属性检查正确
                        smtx elf 630 + zbs 570及以上 - 新建 vm 卷开启常驻缓存，使用精简制备 - 创建 vm 成功，卷属性检查正确
                        smtx elf 630 + os 630级以上 - 新建 vm 卷开启常驻缓存，使用精简制备 - 创建 vm 成功，卷属性检查正确
                        smtx elf 630 + os 630以下 - 新建 vm 卷开启常驻缓存，不能使用精简制备，只能使用厚制备  - 创建 vm 成功，卷属性检查正确
                        smtx elf 630 + zbs 570以下 - 新建 vm 卷开启常驻缓存，不能使用精简制备，只能使用厚制备  - 创建 vm 成功，卷属性检查正确
                    克隆
                        克隆创建 vm (含开启 2副本 pin 厚制备 vol01 + ec 未开启 pin 精简制备卷vol02) - 已有卷 vol01: 3副本 开启 调整 pin 精简制备模式 + vol02 ec 开启 pin 精简直播 + 新建 副本卷开启 pin 2副本精简制备 - 完全拷贝克隆创建成功
                        批量克隆创建 vm (含开启 2副本 pin 厚制备 vol01 + ec 未开启常 pin 简制备卷vol02) - 已有卷 vol01: 3副本 开启 调整 pin 厚制备模式 + vol02 ec 开启 pin 精简直播 + 新建 副本卷开启 pin 2副本精简制备 - 快速拷贝克隆创建成功
                        创建虚拟机时挂在已有卷（开启 pin 厚制备+开启 pin 精简备） - 挂载成功，vm 正常使用
                    快照
                        快照(含开启 pin 2副本厚制备 vol01+ 未开启pin EC 精简制备vol02) - 快照重建vm - 已有卷：vol01 调整 3副本 关闭pin 厚制备 + vol02 开启pin 精简制备 + 新建卷开启 pin 2副本精简制备 - 创建成功
                        vm 未常驻缓存精简制备创建快照_01 - 编辑卷开启常驻缓存厚制备 快照_02  - vm 回滚到 快照 01 成功：卷开启常驻缓存（常驻缓存开启后不能回滚），厚制备（开启后不能回滚）
                编辑 vm
                    新增卷
                        添加 开启常驻缓存的 精简制备卷 、开启常驻缓存的 厚制备 副本卷、ec卷 - 添加新建卷成功
                    已有卷
                        编辑 开机vm - 已有卷（EC卷+副本卷）开启pin ：默认使用精简制备，新增卷开启 pin 使用精简制备 - 编辑成功
                        编辑 关机vm - 已有卷（EC卷+副本卷）开启pin ：默认使用精简制备，新增卷开启 pin 使用精简制备 - 编辑成功
                        编辑 开机 vm 已开启常驻缓存厚制备的 EC卷+副本卷 - 关闭常驻缓存 - 变为普通卷厚制备
                        编辑 开机 vm 已开启常驻缓存精简制备的 EC卷+副本卷 - 关闭常驻缓存 - 变为普通卷精简制备
                        编辑已开启常驻缓存2副本精简制备的卷 - 调整为3副本厚制备 - 副本提升变更成功
                        编辑已开启常驻缓存3副本精简制备的卷 - 调整为3副本厚制备 - 副本降级变更成功
                        编辑 开机vm（含 开启pin ：默认使用精简制备）EC卷+副本卷 - 扩容- 编辑成功
                        编辑 开机vm（含 开启pin ：默认使用精简制备）EC卷+副本卷  - 开启数据加密 - 编辑成功
                        编辑 关机vm（含 开启pin ：默认使用精简制备）EC卷+副本卷  - 修改总线类型- 编辑成功
                    挂载卷
                        仅包含存量 开常驻缓存+厚制备的卷 - 挂载 EC/副本 开常驻缓存+精简制备的共享/非共享卷，使用不同总线 - 挂载成功
                    其他信息
                        虚拟机已开启常驻缓存，精简制备  - 编辑虚拟机名称、网卡等信息，不影响常驻缓存模式
                        vm1、vm2 挂载开启常驻缓存 精简制备共享卷01 - 编辑 vm1 共享卷01 为厚制备 ,vm2 上共享卷01 也为厚制备
                        vm1、vm2 挂载开启常驻缓存 精简制备共享卷01 - 编辑 vm2 共享卷01为关闭常驻缓存 ,vm1 上共享卷01 也关闭常驻缓存
                虚拟机模版（2025-11-10 版本）废弃
                    内容库模版创建 vm
                        os630/zbs570 及以上版本
                            编辑模版所属集群
                                os 630 及以上模版
                                    编辑分发到 os630 及以上 - 检查 os630及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    编辑分发到 zbs570 及以上 - 检查 os630及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    编辑分发到 os630 以下 - 检查 os630及以上版本 模版卷:vol_01、vol_02 都开启常驻缓存厚制备
                                    编辑分发到 zbs570 以下 - 检查 os630及以上版本 模版卷:vol_01、vol_02 都开启常驻缓存厚制备
                                zbs 570 及以上模版
                                    编辑分发到 os630 及以上 - 检查 os630及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    编辑分发到 zbs570 及以上 - 检查 os630及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    编辑分发到 os630 以下 - 检查 os630及以上版本 模版卷:vol_01、vol_02 都开启常驻缓存厚制备
                                    编辑分发到 zbs570 以下 - 检查 os630及以上版本 模版卷:vol_01、vol_02 都开启常驻缓存厚制备
                            模版创建 vm
                                os 630 及以上模版
                                    os630 使用该模版创建vm - vm01 默认开启常驻缓存精简制备：切换为厚制备，vm02 默认选择常驻缓存厚制备：切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                                    elf 630+zbs570 及以上版本 -  使用该模版创建vm - vm01 默认开启常驻缓存精简制备：切换为厚制备，vm02 默认选择常驻缓存厚制备：切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                                    elf 630+os630 及以上版本 -  使用该模版创建vm - vm01 默认开启常驻缓存精简制备：切换为厚制备，vm02 默认选择常驻缓存厚制备：切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                                    elf 630+zbs570 以下版本 -  使用该模版创建vm - vm01 、vm02 均使用常驻缓存厚制备：不可切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                                    elf 630+ os630 以下版本 -  使用该模版创建vm - vm01 、vm02 均使用常驻缓存厚制备：不可切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                                    os 630以下版本 -  使用该模版创建vm - vm01 、vm02 均使用常驻缓存厚制备：不可切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                                    elf 630以下版本 + 任意存储集群 -  使用该模版创建vm - vm01 、vm02 均使用常驻缓存厚制备：不可切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                                zbs 570 及以上模版
                                    os630 使用该模版创建vm - vm01 默认开启常驻缓存精简制备：切换为厚制备，vm02 默认选择常驻缓存厚制备：切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                                    elf 630+zbs570 及以上版本 -  使用该模版创建vm - vm01 默认开启常驻缓存精简制备：切换为厚制备，vm02 默认选择常驻缓存厚制备：切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                                    elf 630+os630 及以上版本 -  使用该模版创建vm - vm01 默认开启常驻缓存精简制备：切换为厚制备，vm02 默认选择常驻缓存厚制备：切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                                    elf 630+zbs570 以下版本 -  使用该模版创建vm - vm01 、vm02 均使用常驻缓存厚制备：不可切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                                    elf 630+ os630 以下版本 -  使用该模版创建vm - vm01 、vm02 均使用常驻缓存厚制备：不可切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                                    os 630以下版本 -  使用该模版创建vm - vm01 、vm02 均使用常驻缓存厚制备：不可切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                                    elf 630以下版本 + 任意存储集群 -  使用该模版创建vm - vm01 、vm02 均使用常驻缓存厚制备：不可切换为精简制备 - 创建 vm 成功 vol_01、vol_02  卷属性正确
                            模版转换为 vm
                                os 630 及以上模版
                                    转换为 os630 的 vm - 转换成功，vol_01 开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630+ zbs570 及以上版本 的 vm - 转换成功，vol_01 开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630+ os630 及以上版本 的 vm - 转换成功，vol_01 开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630+ zbs570 以下版本 的 vm - 转换成功，vol_01 、ol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630+ os630 以下版本 的 vm - 转换成功，vol_01 、ol_02 开启常驻缓存2副本厚制备卷
                                    转换为 os630 以下版本 的 vm - 转换成功，vol_01 、ol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630 以下版本 + 任意存储  的 vm - 转换成功，vol_01 、ol_02 开启常驻缓存2副本厚制备卷
                                zbs570 及以上模版
                                    转换为 os630 的 vm - 转换成功，vol_01 开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630+ zbs570 及以上版本 的 vm - 转换成功，vol_01 开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630+ os630 及以上版本 的 vm - 转换成功，vol_01 开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630+ zbs570 以下版本 的 vm - 转换成功，vol_01 、ol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630+ os630 以下版本 的 vm - 转换成功，vol_01 、ol_02 开启常驻缓存2副本厚制备卷
                                    转换为 os630 以下版本 的 vm - 转换成功，vol_01 、ol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630 以下版本 + 任意存储  的 vm - 转换成功，vol_01 、ol_02 开启常驻缓存2副本厚制备卷
                            vm 克隆为模版
                                630os、630elf+zbs570/os630 及以上版本 vm
                                    os630 vm - 克隆为 os630 及以上版本 模版 - 检查 os 630 及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    os630 vm - 克隆为 zbs570 及以上版本 模版 - 检查 zbs570 及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    os630 vm - 克隆为 os630 以下版本 模版 - 检查 os630以下版本 模版卷:vol_01、vol_02 开启常驻缓存厚制备
                                    os630 vm - 克隆为 zbs570 以下版本 模版 - 检查 zbs570 以下版本 模版卷:vol_01、vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 及以上版本 vm - 克隆为 os630 及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 及以上版本 vm - 克隆为 zbs570 及以上版本 模版 - 检查 zbs570 及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 及以上版本 vm - 克隆为 os630 以下版本 模版 - 检查 os630以下版本 模版卷:vol_01、vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 及以上版本 vm - 克隆为 zbs570 以下版本 模版 - 检查 zbs570 以下版本 模版卷:vol_01、vol_02 开启常驻缓存厚制备
                                    elf630 + os630 及以上版本 vm - 克隆为 os630 及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    elf630 + os630 及以上版本 vm - 克隆为 zbs570 及以上版本 模版 - 检查 zbs570 及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    elf630 + os630 及以上版本 vm - 克隆为 os630 以下版本 模版 - 检查 os630以下版本 模版卷:vol_01、vol_02 开启常驻缓存厚制备
                                    elf630 + os630 及以上版本 vm - 克隆为 zbs570 以下版本 模版 - 检查 zbs570 以下版本 模版卷:vol_01、vol_02 开启常驻缓存厚制备
                                630elf+zbs570/os630 以下版本 vm
                                    elf630 + zbs570 以下版本 vm - 克隆为 os630 及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 以下版本 vm - 克隆为 zbs570 及以上版本 模版 - 检查 zbs570 及以上版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 以下版本 vm - 克隆为 os630 以下版本 模版 - 检查 os630 以下版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 以下版本 vm - 克隆为 zbs570 以下版本 模版 - 检查 zbs570 以下版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + os630 以下版本 vm - 克隆为 os630 及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + os630 以下版本 vm - 克隆为 zbs570 及以上版本 模版 - 检查 zbs570 及以上版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + os630 以下版本 vm - 克隆为 os630 以下版本 模版 - 检查 os630 以下版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + os630 以下版本 vm - 克隆为 zbs570 以下版本 模版 - 检查 zbs570 以下版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                            vm 转化为模版
                                630os、630elf+zbs570/os630 及以上版本 vm
                                    os630 vm - 转化为 os630 及以上版本 模版 - 检查 os 630 及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    os630 vm - 转化为 zbs570 及以上版本 模版 - 检查 zbs570 及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    os630 vm - 转化为 os630 以下版本 模版 - 检查 os630以下版本 模版卷:vol_01、vol_02 开启常驻缓存厚制备
                                    os630 vm - 转化为 zbs570 及以上版本 模版 - 检查 zbs570 以下版本 模版卷:vol_01、vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 及以上版本 vm - 转化为 os630 及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 及以上版本 vm - 转化为 zbs570 及以上版本 模版 - 检查 zbs570 及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 及以上版本 vm - 转化为 os630 以下版本 模版 - 检查 os630及以上版本 模版卷:vol_01、vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 及以上版本 vm - 转化为 zbs570 及以上版本 模版 - 检查 zbs570 及以上版本 模版卷:vol_01、vol_02 开启常驻缓存厚制备
                                    elf630 + os630 及以上版本 vm - 转化为 os630 及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    elf630 + os630 及以上版本 vm - 转化为 zbs570 及以上版本 模版 - 检查 zbs570 及以上版本 模版卷:vol_01 开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    elf630 + os630 及以上版本 vm - 转化为 os630 以下版本 模版 - 检查 os630及以上版本 模版卷:vol_01、vol_02 开启常驻缓存厚制备
                                    elf630 + os630 及以上版本 vm - 转化为 zbs570 及以上版本 模版 - 检查 zbs570 及以上版本 模版卷:vol_01、vol_02 开启常驻缓存厚制备
                                630elf+zbs570/os630 以下版本 vm
                                    elf630 + zbs570 以下版本 vm - 转化为 os630 及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 以下版本 vm - 转化为 zbs570 及以上版本 模版 - 检查 zbs570 及以上版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 以下版本 vm - 转化为 os630 以下版本 模版 - 检查 os630 以下版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + zbs570 以下版本 vm - 转化为 zbs570 以下版本 模版 - 检查 zbs570 以下版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + os630 以下版本 vm - 转化为 os630 及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + os630 以下版本 vm - 转化为 zbs570 及以上版本 模版 - 检查 zbs570 及以上版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + os630 以下版本 vm - 转化为 os630 以下版本 模版 - 检查 os630 以下版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                                    elf630 + os630 以下版本 vm - 转化为 zbs570 以下版本 模版 - 检查 zbs570 以下版本 模版卷:vol_01未开启常驻缓存精简制备、vol_02 开启常驻缓存厚制备
                        存量630/zbs570 及以下版本
                            编辑模版所属集群
                                630 以下模版
                                    编辑分发到 os 630 及以上 - 检查 os630及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    编辑分发到 zbs570 及以上版本- 检查 zbs570 及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                zbs 570 以下模版
                                    编辑分发到 os 630 及以上 - 检查 os630及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                    编辑分发到 zbs570 及以上版本- 检查 zbs570及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                            模版创建vm
                                630 以下模版
                                    os630 使用该模版创建vm - 可编辑 vm01 开启常驻缓存精简制备，vm02 默认选择常驻缓存厚制备：切换为精剪制备 - 创建 vm 成功 v0s_01、vol_02 常驻缓存精简制备
                                    elf630 + os630 使用该模版创建vm - 可编辑 vm01 开启常驻缓存精简制备，vm02 默认选择常驻缓存厚制备：切换为精剪制备 - 创建 vm 成功 v0s_01、vol_02 常驻缓存精简制备
                                    elf630 + zbs570 使用该模版创建vm - 可编辑 vm01 开启常驻缓存精简制备，vm02 默认选择常驻缓存厚制备：切换为精剪制备 - 创建 vm 成功 v0s_01、vol_02 常驻缓存精简制备
                                    elf630 + os630 以下 - 使用该模版创建vm - 可编辑 vm01 开启常驻缓存厚制备，vm02 默认选择常驻缓存厚制备：不切换为精剪制备 - 创建 vm 成功 vol_01、vol_02 常驻缓存厚制备
                                    elf630 + zbs570 以下 - 使用该模版创建vm - 可编辑 vm01 开启常驻缓存厚制备，vm02 默认选择常驻缓存厚制备：不切换为精剪制备 - 创建 vm 成功 vol_01、vol_02 常驻缓存厚制备
                                zbs570 以下模版
                                    os630 使用该模版创建vm - 可编辑 vm01 开启常驻缓存精简制备，vm02 默认选择常驻缓存厚制备：切换为精剪制备 - 创建 vm 成功 v0s_01、vol_02 常驻缓存精简制备
                                    elf630 + os630 使用该模版创建vm - 可编辑 vm01 开启常驻缓存精简制备，vm02 默认选择常驻缓存厚制备：切换为精剪制备 - 创建 vm 成功 v0s_01、vol_02 常驻缓存精简制备
                                    elf630 + zbs570 使用该模版创建vm - 可编辑 vm01 开启常驻缓存精简制备，vm02 默认选择常驻缓存厚制备：切换为精剪制备 - 创建 vm 成功 v0s_01、vol_02 常驻缓存精简制备
                                    elf630 + os630 以下 - 使用该模版创建vm - 可编辑 vm01 开启常驻缓存厚制备，vm02 默认选择常驻缓存厚制备：不切换为精剪制备 - 创建 vm 成功 vol_01、vol_02 常驻缓存厚制备
                                    elf630 + zbs570 以下 - 使用该模版创建vm - 可编辑 vm01 开启常驻缓存厚制备，vm02 默认选择常驻缓存厚制备：不切换为精剪制备 - 创建 vm 成功 vol_01、vol_02 常驻缓存厚制备
                            模版转换为 vm
                                os 620 以下模版
                                    转换为 os630 的 vm - 转换成功，vol_01 未开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630 + zbs570 及以上版本 的 vm - 转换成功，vol_01 未开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630 + os630 及以上版本 的 vm - 转换成功，vol_01 未开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630 + zbs570 以下版本 的 vm - 转换成功，vol_01 未开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630 + os630 以下版本 的 vm - 转换成功，vol_01 未开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                zbs570 以下模版
                                    转换为 os630 的 vm - 转换成功，vol_01 未开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630 + zbs570 及以上版本 的 vm - 转换成功，vol_01 未开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630 + os630 及以上版本 的 vm - 转换成功，vol_01 未开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630 + zbs570 以下版本 的 vm - 转换成功，vol_01 未开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                                    转换为 elf630 + os630 以下版本 的 vm - 转换成功，vol_01 未开启常驻2副本缓存精简制备卷 + vol_02 开启常驻缓存2副本厚制备卷
                            存量vm- 克隆为模版
                                os 620 vm - 克隆为 os 630及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                os 620 vm - 克隆为  zbs570 级以上 模版 - 检查 zbs570及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                elf 620 + zbs存储 vm - 克隆为 os 630及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                elf 620 + zbs存储 vm - 克隆为  zbs570 级以上 模版 - 检查 zbs570及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                elf 620 + os存储 vm - 克隆为 os 630及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                elf 620 + os存储 vm - 克隆为  zbs570 级以上 模版 - 检查 zbs570及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                            存量vm- 转换为模版
                                os 620 vm - 转换为 os 630及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                os 620 vm - 转换为  zbs570 级以上 模版 - 检查 zbs570及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                elf 620 + zbs存储 vm - 转换为 os 630及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                elf 620 + zbs存储 vm - 转换为  zbs570 级以上 模版 - 检查 zbs570及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                elf 620 + os存储 vm - 转换为 os 630及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                                elf 620 + os存储 vm - 转换为  zbs570 级以上 模版 - 检查 zbs570及以上版本 模版卷:vol_01 未开启常驻缓存精简制备，vol_02 开启常驻缓存厚制备
                03-新方案内容库 Tower-20718
                    vm 克隆为模版
                        os 630 含常驻缓存（副本精简制备+ec厚制备）的常驻缓存vm - 克隆为本集群模版 - ELF api保留常驻缓存属性(tower UI VM不使用)，制备不变
                        os 620 含常驻缓存（副本厚制备+ec厚制备）的常驻缓存vm - 克隆为本集群模版 - ELF api保留常驻缓存属性(tower UI VM不使用)，制备不变
                        elf630 + os630 及以上版本 vm - 克隆为 os630 及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01 不包含常驻缓存精简制备，vol_02 不包含常驻缓存厚制备
                        elf630 + os630以下版本 vm - 克隆为 os630 以下版本 模版 - 检查 os630 以下版本 模版卷:vol_01 不包含常驻缓存精简制备，vol_02 不包含常驻缓存厚制备
                        elf 630 +zbs 570 含常驻缓存（副本精简制备+ec厚制备）卷 vm - 克隆为本集群ZBS570模版 - 不保留常驻缓存属性，制备不变
                        elf 630 +zbs 564 含常驻缓存（副本厚制备+ec厚制备）卷 vm - 克隆为 模版 - zbs570 不保留常驻缓存属性，制备不变
                        特例：elf630 + os630 及以上版本 vm - 克隆为 os630 及以上 全闪集群(分发) - 版本 模版 - 检查 os630及以上版本 模版卷:vol_01 不包含常驻缓存精简制备，vol_02 不包含常驻缓存厚制备
                        特例：elf630 + os630 及以上版本 vm - 克隆为 os630 及以上 关闭常驻缓存集群（分发） - 版本 模版 - 检查 os630及以上版本 模版卷:vol_01 不包含常驻缓存精简制备，vol_02 不包含常驻缓存厚制备
                    vm 转化为模版
                        os 630 含常驻缓存（副本精简制备+ec厚制备）的常驻缓存vm - 转化为 模版 - 不保留常驻缓存属性，制备不变
                        os 620 含常驻缓存（副本厚制备+ec厚制备）的常驻缓存vm - 转化为 模版 - 不保留常驻缓存属性，制备不变
                        elf630 + os630 及以上版本 vm - 转化为 os630 及以上版本 模版 - 检查 os630及以上版本 模版卷:vol_01 关闭常驻缓存精简制备，vol_02 关闭常驻缓存厚制备
                        elf630 + os630 以下版本 vm - 转化为 os630 以下版本 模版 - 检查 os630 以下版本 模版卷:vol_01 关闭常驻缓存精简制备、vol_02 关闭常驻缓存厚制备
                        elf 630 +zbs 570 含常驻缓存（副本精简制备+ec厚制备）卷 vm - 转化为 模版 - zbs570 不保留常驻缓存属性，制备不变
                        elf 630 +zbs 564 含常驻缓存（副本厚制备+ec厚制备）卷 vm - 转化为 模版 - zbs570 不保留常驻缓存属性，制备不变
                        特例：elf630 + os630 及以上版本 vm - 转化为 os630 及以上 全闪集群 - 版本 模版 - 检查 os630及以上版本 模版卷:vol_01 不包含常驻缓存精简制备，vol_02 不包含常驻缓存厚制备
                        特例：elf630 + os630 及以上版本 vm - 转化为 os630 及以上 关闭常驻缓存集群 - 版本 模版 - 检查 os630及以上版本 模版卷:vol_01 不包含常驻缓存精简制备，vol_02 不包含常驻缓存厚制备
                    模版创建 vm
                        tower 480 新模版
                            os 集群模版
                                os 630 模版创建vm - 卷vol_01 精简制备 + 卷 vol_02 厚制备 - 快速克隆创建vm
                                os 630 模版创建vm - 卷vol_01 精简制备 + 卷 vol_02 厚制备 都开启常驻缓存 - 快速克隆创建vm
                                os 630 模版创建vm - 卷vol_01 切换为开启常驻缓存厚制备 + 卷 vol_02 切换为开启常驻缓存精简制备 - 完全克隆创建vm
                                elf 630 + os630 模版创建 vm - 卷开启常驻缓存 - 快速克隆创建 vm 成功
                                elf 630 + os620 模版创建 vm - 卷开启常驻缓存(仅支持后制备) - 快速克隆创建 vm 成功
                                elf 620 + os630 模版创建 vm - 卷开启常驻缓存（仅支持厚制备） - 完全克隆创建 vm 成功
                                elf 620 + os620 模版创建 vm - 卷开启常驻缓存（仅支持厚制备） - 完全克隆创建 vm 成功
                                elf 630 + 其他os630 (含分发) - 模版创建 vm - 卷开启常驻缓存 - 快速克隆创建 vm 成功
                                elf 630 + 其他zbs570 (含分发) - 模版创建 vm - 卷开启常驻缓存 - 快速克隆创建 vm 成功
                            zbs  集群模版
                                elf 630 + zbs570 模版创建 vm - 卷开启常驻缓存 - 快速克隆创建 vm 成功
                                elf 630 + zbs570 模版创建vm - 卷vol_01 切换为开启常驻缓存厚制备 + 卷 vol_02 切换为开启常驻缓存精简制备 - 完全克隆创建vm
                                elf 630 + zbs564 模版创建 vm - 卷开启常驻缓存(仅支持后制备) - 快速克隆创建 vm 成功
                                elf 620 + zbs570 模版创建 vm - 卷开启常驻缓存（仅支持厚制备） - 完全克隆创建 vm 成功
                                elf 620 + zbs564 模版创建 vm - 卷开启常驻缓存（仅支持厚制备） - 完全克隆创建 vm 成功
                                elf 630 + 其他os630 (含分发) - 模版创建 vm - 卷开启常驻缓存 - 快速克隆创建 vm 成功
                                elf 630 + 其他zbs570 (含分发) - 模版创建 vm - 卷开启常驻缓存 - 快速克隆创建 vm 成功
                        存量数据检查
                            存量620开启常驻缓存模版 - os620 创建vm - 常驻缓存保持关闭厚制备 - 操作开启开启常驻缓存（仅支持厚制备）创建 vm 成功
                            存量620开启常驻缓存模版 - os630（含分发）创建vm - 常驻缓存保持关闭厚制备 - 操作开启常驻缓存精简制备 - 完全克隆创建 vm 成功
                            存量620开启常驻缓存模版 - os630+os620 创建vm - 常驻缓存保持关闭厚制备 - 操作开启常驻缓存（仅支持厚制备）创建 vm 成功
                    模版转换 vm
                        tower 480 新模版
                            os 模版
                                os 630 模版(os630 elf api 存储常驻缓存) - 转换为 os 630 vm：开启常驻缓存，卷vol_01 副本 精简制备 + 卷 vol_02 ec 厚制备
                                os 630 模版(os630 elf api 存储常驻缓存) - 转换为 elf 630+os630 vm：开启常驻缓存，卷vol_01 副本 精简制备 + 卷 vol_02 ec 厚制备
                                os 630 模版(os630 elf api 存储常驻缓存) - 转换为 elf 620+os630 vm：开启常驻缓存，卷vol_01 副本 精简制备 + 卷 vol_02 ec 厚制备
                                os 630 模版(os630 api 未存储常驻缓存) - 转换为 elf 630+os630 vm：关闭常驻缓存，卷vol_01 副本 精简制备 + 卷 vol_02 ec 厚制备
                                os620 模版(os620 api 未存储常驻缓存) - 转化为 elf630+os 620 vm - 关闭常驻缓存，卷vol_01 副本 精简制备 + 卷 vol_02 ec 厚制备
                                os 630 模版(os630 api 未存储常驻缓存) - 转换为 elf 620+os630 vm：关闭常驻缓存，卷vol_01 副本 精简制备 + 卷 vol_02 ec 厚制备
                            zbs 模版
                                zbs570 模版 - 转换为 elf 630+zbs570 vm：关闭常驻缓存，卷vol_01 副本 精简制备 + 卷 vol_02 ec 厚制备
                                zbs564 模版 - 转换为 elf 630+zbs564 vm：关闭常驻缓存，卷vol_01 副本 精简制备 + 卷 vol_02 ec 厚制备
                                zbs570 模版 - 转换为 elf 620+zbs570 vm：关闭常驻缓存，卷vol_01 副本 精简制备 + 卷 vol_02 ec 厚制备
                        存量数据检查
                            os 存量模版
                                存量620开启常驻缓存模版 - 转化为 os620 vm - 常驻缓存开启厚制备
                                存量620开启常驻缓存模版 - 转化为 elf630+os620 vm - 常驻缓存保持开启厚制备
                                存量620开启常驻缓存模版 - 转化为 elf620+os620 vm - 常驻缓存保持开启厚制备
                            zbs570 模版--tower470 升级 tower480 使用
                                检查 升级 480后，模版元数据 contentLibraryVmTemplate.vm_disks 不记录常驻缓存属性 - iscsiLunSnapshots 卷 iscsi lun 常驻缓存 "prioritized": false
                                分发到其他 os/zbs 集群，分发的目标 os/zbs  模版元数据和 iscsi lun  常驻缓存属性关闭
                                elf630 + zbs 模版克隆创建 vm  - 卷常驻缓存属性默认关闭，开启常驻缓存精简制备+厚制备 - 快速克隆创建vm
                                elf630 + zbs 模版克隆创建 vm  - 卷常驻缓存属性默认关闭，开启常驻缓存厚制备 - 快速克隆创建vm
                                模版转化为 elf630+zbs570 - vm 关闭常驻缓存
                                模版转化为 elf620+zbs570 -  vm 关闭常驻缓存
                    模版编辑所属集群
                        tower 480模版
                            os 630 (elf api 常驻缓存开启)模版 - 分发到 os 630 级以上集群 - 常驻缓存关闭
                            os 630 (elf api 常驻缓存开启)模版 - 分发到 os 630 级以下集群 - 留常驻缓存关闭
                            os 630 (elf api 常驻缓存开启)模版 - 分发到 任意zbs 集群 - 常驻缓存关闭
                            os 630 (elf api 常驻缓存关闭)模版 - 分发到任意集群 - 常驻缓存关闭
                            zbs570 模版 - 分发到任意集群 - 常驻缓存关闭
                        存量数据
                            存量已开启常驻缓存的630 以下 os 模版 - 分发到 os630 以下 集群 - 常驻缓存关闭
                            存量已开启常驻缓存的630 以下 os 模版 - 分发到 os630 及以上 集群 - 常驻缓存关闭
                            存量已开启常驻缓存的630 以下 os 模版 - 分发到 任意 zbs 集群 - 常驻缓存关闭
                迁移
                    集群内迁移
                        smtx os/elf 集群内迁移不迁移存储资源，不单独检查
                    跨集群迁移
                        同版本/高版本到低版本迁移
                            目标端未开启/不支持常驻缓存
                                smtx os 630迁移到 smtx os 630级以上（未开起常驻缓存） - 提示迁移将关闭常驻缓存，选择2副本精简制备 - 迁移成功 ，2个卷都是精简制备关闭常驻缓存(zbs chunk 多实例集群)
                                smtx os 630迁移到 【smtx elf630级以上+zbs570 及以上（未开起常驻缓存）】 - 提示迁移将关闭常驻缓存，选择2副本精简制备 - 迁移成功 ，2个卷都是精简制备关闭常驻缓存
                                smtx os 630迁移到 【smtx elf630级以上+zbs570 以下（未开起常驻缓存）】 - 提示迁移将关闭常驻缓存，选择2副本精简制备 - 迁移成功 ，2个卷都是精简制备关闭常驻缓存
                            目标端开启常驻缓存
                                os 跨集群迁移
                                    跨集群热迁移
                                        smtx os 630 热迁移到 smtx os 630及以上版本 - 选择2副本精简制备 - 迁移成功 2个卷都是 开启常驻缓存2副本精简制备
                                        smtx os 630 热迁移到 【smtx elf 630级以上 + zbs570 及以上】  - 选择2副本精简制备 - 迁移成功 2个卷都是 开启常驻缓存2副本精简制备
                                        smtx os 630 热迁移到 【smtx elf 630级以上 + zbs570 以下开启常驻缓存】  - 选择2副本精简制备 - 迁移成功 vol_01、vol_02 开启常驻缓存 2副本厚制备
                                        smtx os 630 热迁移到 【smtx elf 630级以上 + os630 及以上】  - 选择2副本精简制备 - 迁移成功 2个卷都是 开启常驻缓存2副本精简制备
                                        smtx os 630 热迁移到 【smtx elf 630级以上 + os630 以下开启常驻缓存】  - 选择2副本精简制备 - 迁移成功 vol_01、vol_02 开启常驻缓存 2副本厚制备
                                        smtx os 630 热迁移到 smtx os 630 以下版本 - 不支持迁移到低版本 os 集群
                                        smtx os 630 热迁移到 【smtx elf 630 以下 + zbs/os 开启常驻缓存】  - 不支持迁移到低版本 elf 集群
                                    跨集群分段/冷迁移
                                        smtx os 630 分段迁移（源端保留vm）到 smtx os 630及以上版本 - 选择2副本精简制备 - 迁移成功 2个卷都是 开启常驻缓存2副本精简制备
                                        smtx os 630 冷迁移（源端保留vm）到 smtx os 630及以上版本 - 选择2副本精简制备 - 迁移成功 2个卷都是 开启常驻缓存2副本精简制备
                                        smtx os 630 分段迁移（源端不保留vm）到 smtx os 630以下版本 - 选择2副本精简制备 - 迁移成功 2个卷都是 开启常驻缓存2副本厚制备
                                        smtx os 630 冷迁移（源端不保留vm）到 smtx os 630 以下版本 - 选择2副本精简制备 - 迁移成功 2个卷都是 开启常驻缓存2副本厚制备
                                存算分离迁移
                                    迁移计算和存储
                                        【smtx elf 630级以上 + zbs570 及以上】迁移计算和存储到 smtx os 630及以上版本   - 选择2副本精简制备 - 迁移成功 2个卷都是 开启常驻缓存2副本精简制备
                                        【smtx elf1 630级以上 + zbs1 570 及以上】迁移计算和存储到 【smtx elf2 630级以上 + zbs2  570 及以上】  - 选择2副本精简制备 - 迁移成功 2个卷都是 开启常驻缓存2副本精简制备
                                        【smtx elf1 630级以上 + zbs1 570 及以上】迁移计算和存储到 【smtx elf2 630级以上 + zbs2  570 以下】  - 选择2副本精简制备 - 迁移成功 ，vol_01 开启常驻缓存2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                                        【smtx elf1 630级以上 + zbs570 及以上】迁移计算和存储到 【smtx elf2 630级以上 + os630 及以上】  - 选择2副本精简制备 - 迁移成功 2个卷都是 开启常驻缓存2副本精简制备
                                        【smtx elf1 630级以上 + zbs1 570 及以上】迁移计算和存储到 【smtx elf2 630级以上 + os630 以下】  - 选择2副本精简制备 - 迁移成功 ，vol_01 开启常驻缓存2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                                        【smtx elf 630级以上 + zbs570 及以上】迁移计算和存储到 smtx os 630以下 - 禁止迁移到 低版本
                                        【smtx elf1 630级以上 + zbs1 570 及以上】迁移计算和存储到 【smtx elf2 630以下 + 存储elf/os 】  - 禁止迁移到低版本
                                        【smtx elf 630级以上 + os630 及以上】迁移计算和存储到 smtx os 630及以上版本   - 选择2副本精简制备 - 迁移成功 2个卷都是 开启常驻缓存2副本精简制备
                                        【smtx elf1 630级以上 + os630 及以上】迁移计算和存储到 【smtx elf2 630级以上 + zbs2  570 及以上】  - 选择2副本精简制备 - 迁移成功 2个卷都是 开启常驻缓存2副本精简制备
                                        【smtx elf1 630级以上 + os630 及以上】迁移计算和存储到 【smtx elf2 630级以上 + zbs2  570 以下】  - 选择2副本精简制备 - 迁移成功 ，vol_01 开启常驻缓存2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                                        【smtx elf1 630级以上 + os630 及以上】迁移计算和存储到 【smtx elf2 630级以上 + os630 及以上】  - 选择2副本精简制备 - 迁移成功 2个卷都是 开启常驻缓存2副本精简制备
                                        【smtx elf1 630级以上 + os630 及以上】迁移计算和存储到 【smtx elf2 630级以上 + os630 以下】  - 选择2副本精简制备 - 迁移成功 ，vol_01 开启常驻缓存2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                                        【smtx elf 630级以上 + os630 及以上】迁移计算和存储到 smtx os 630以下 - 禁止迁移到 低版本
                                        【smtx elf1 630级以上 + os630 及以上】迁移计算和存储到 【smtx elf2 630以下 + 存储elf/os 】  - 禁止迁移到低版本
                                    仅迁移计算
                                        【smtx elf1 630级以上 + zbs1 570 及以上】仅迁移计算到 【smtx elf2 630 及以上 + zbs1 570 及以上】 - 选择2副本精简制备 - 迁移成功 ，保持 vol_01 开启常驻缓存2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                                        【smtx elf1 630级以上 + os630 及以上】仅迁移存储到 【smtx elf2 630 及以上 + os630 及以上】 - 选择2副本精简制备 - 迁移成功 ，保持 vol_01 开启常驻缓存2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                                        【smtx elf1 630级以上 + zbs1 564 及以上】仅迁移计算到 【smtx elf2 630 及以上 + zbs1 564 及以上】 - 选择2副本精简制备 - 迁移成功 ，保持 vol_01 2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                                        【smtx elf1 630级以上 + os620 及以上】仅迁移存储到 【smtx elf2 630 及以上 + os620 及以上】 - 迁移成功 ，保持 vol_01 2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                                        【smtx elf1 630级以上 + 存储zbs570/os630以下 】仅迁移计算到 【smtx elf2 630以下 + 存储elf/zbs 】 - 禁止迁移到低版本 smtx elf
                                    仅迁移存储
                                        【smtx elf1 630级以上 + zbs1 570 及以上】仅迁移存储到 【smtx elf1 630 及以上 + zbs2 570 及以上】 - 选择2副本精简制备 - 迁移成功 ，vol_01 、vol_02 开启常驻缓存2副本精简制备
                                        【smtx elf1 630级以上 + zbs1 570 及以上】仅迁移存储到 【smtx elf1 630及以上+ zbs2 570 以下】 - 选择2副本精简制备 - 迁移成功 ， vol_01、vol_02 开启常驻缓存 2副本厚制备
                                        【smtx elf1 630级以上 + zbs1 570 及以上】仅迁移存储到 【smtx elf1 630 及以上 + os630 及以上】 - 选择2副本精简制备 - 迁移成功 ，vol_01 、vol_02 开启常驻缓存2副本精简制备
                                        【smtx elf1 630级以上 + zbs1 570 及以上】仅迁移存储到 【smtx elf1 630及以上+ os630 以下】 - 选择2副本精简制备 - 迁移成功 ， vol_01、vol_02 开启常驻缓存 2副本厚制备
                                        【smtx elf1 630级以上 + os630 及以上】仅迁移存储到 【smtx elf1 630 及以上 + os630 及以上】 - 选择2副本精简制备 - 迁移成功 ，vol_01 、vol_02 开启常驻缓存2副本精简制备
                                        【smtx elf1 630级以上 + os630 及以上】仅迁移存储到 【smtx elf1 630及以上+ os630 以下】 - 选择2副本精简制备 - 迁移成功 ， vol_01、vol_02 开启常驻缓存 2副本厚制备
                                        【smtx elf1 630级以上 + os630 及以上】仅迁移存储到 【smtx elf1 630 及以上 + zbs2 570 及以上】 - 选择2副本精简制备 - 迁移成功 ，vol_01 、vol_02 开启常驻缓存2副本精简制备
                                        【smtx elf1 630级以上 + os630 及以上】仅迁移存储到 【smtx elf1 630及以上+ zbs2 570 以下】 - 选择2副本精简制备 - 迁移成功 ， vol_01、vol_02 开启常驻缓存 2副本厚制备
                        低版本迁移到高版本
                            os 跨集群迁移
                                跨集群热迁移
                                    smtx os 620 热迁移到 smtx os 630及以上版本 - 选择2副本精简制备 - 迁移成功，2个卷都是2副本精简制备，且vol_02开启常驻缓存
                                    smtx os 620 热迁移到 【smtx elf 630级以上 + zbs570 及以上】  - 选择2副本精简制备 - 迁移成功，2个卷都是2副本精简制备，且vol_02开启常驻缓存
                                    smtx os 620 热迁移到 【smtx elf 630级以上 + zbs570 以下开启常驻缓存】  - 选择2副本精简制备 - 迁移成功 vol_01 精简制备、vol_02 开启常驻缓存 2副本厚制备
                                    smtx os 620 热迁移到 【smtx elf 630级以上 + os630 及以上】  - 选择2副本精简制备 - 迁移成功，2个卷都是2副本精简制备，且vol_02开启常驻缓存
                                    smtx os 620 热迁移到 【smtx elf 630级以上 + os630 以下开启常驻缓存】  - 选择2副本精简制备 - 迁移成功 vol_01 精简制备、vol_02 开启常驻缓存 2副本厚制备
                                分段/冷迁移
                                    smtx os 620 分段迁移（源端保留vm）到 smtx os 630及以上版本 - 选择2副本精简制备 - 迁移成功 2个卷都是 2副本精简制备，且vol_02 开启常驻缓存
                                    smtx os 620 冷迁移（源端不保留vm）到 smtx os 630及以上版本 - 选择2副本精简制备 - 迁移成功 2个卷都是 2副本精简制备，且vol_02 开启常驻缓存
                            存算分离迁移
                                迁移计算和存储
                                    【smtx elf 620 + 存储 os/zbs】迁移计算和存储到 smtx os 630及以上版本   - 选择2副本精简制备 - 迁移成功 2个卷都是 2副本精简制备，且 vol_02开启常驻缓存
                                    【smtx elf 620 + 存储 os/zbs】迁移计算和存储到 【smtx elf2 630级以上 + zbs2  570 及以上】  - 选择2副本精简制备 - 迁移成功 2个卷都是 2副本精简制备，且 vol_02开启常驻缓存
                                    【smtx elf 620 + 存储/os/zbs】迁移计算和存储到 【smtx elf2 630级以上 + zbs2  570 以下】   - 选择2副本精简制备 - 迁移成功 ，vol_01 2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                                    【smtx elf 620 + 存储 os/zbs】迁移计算和存储到 【smtx elf2 630级以上 + os630 及以上】  - 选择2副本精简制备 - 迁移成功 2个卷都是 2副本精简制备，且 vol_02开启常驻缓存
                                    【smtx elf 620 + 存储/os/zbs】迁移计算和存储到 【smtx elf2 630级以上 + os630 以下】   - 选择2副本精简制备 - 迁移成功 ，vol_01 2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                                仅迁移存储
                                    smtx elf630 以下集群+ 存储，不支持创建常驻缓存精简制备卷，不检查仅迁移存储场景
                                仅迁移计算
                                    【smtx elf1 620 + zbs1 570 及以上】仅迁移计算到 【smtx elf2 630 及以上 + zbs1 570 及以上】- 迁移成功 ， vol_01 2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                                    【smtx elf1 620 + zbs1 570 以下】仅迁移计算到 【smtx elf2 630 及以上 + zbs1 570 以下】- 迁移成功 ， vol_01 2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                                    【smtx elf1 620 + os630及以上】仅迁移计算到 【smtx elf2 630 及以上 + os630 及以上版本】- 迁移成功 ， vol_01 2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                                    【smtx elf1 620 + os630以下】仅迁移计算到 【smtx elf2 630 及以上 + os630 以下】- 迁移成功 ， vol_01 2副本精简制备 + vol_02 开启常驻缓存 2副本厚制备
                虚拟卷
                    克隆存量开启常驻缓存的厚制备 副本卷 - 克隆成功，仍开启常驻缓存，使用厚制备
                    克隆存量开启常驻缓存的厚制备 ec卷 - 克隆成功，仍开启常驻缓存，使用厚制备
                    创建开启常驻缓存的精简制备副本共享卷 - 创建成功
                    创建开启常驻缓存的精简制备EC非共享卷 - 创建成功
                    克隆新建开启常驻缓存的精简制备 副本共享卷 - 克隆成功，开启常驻缓存，使用精简制备
                    克隆新建开启常驻缓存的精简制备 ec 共享卷 - 克隆成功，开启常驻缓存，使用精简制备
                    克隆新建开启常驻缓存的精简制备 ec 共享卷 - 克隆成功，开启常驻缓存，使用精简制备
                    克隆新建开启常驻缓存的精简制备 ec 共享卷 - 克隆成功，开启常驻缓存，使用精简制备
                场景测试
                    升级场景
                        克隆 存量 vm 操作
                            源：含开启常驻缓存厚制备卷 - 630 克隆创建 vm - 卷开启常驻缓存，保持厚制备  - 切换为精简制备，完全拷贝创建 vm 成功
                            源：含开启常驻缓存厚制备卷 - smtx elf630  +zbs 570 克隆创建 vm - 卷开启常驻缓存，保持厚制备  - 切换为精简制备，创建 vm 成功
                            源：含开启常驻缓存厚制备卷 - smtx elf630  +os 630 及以上版本 克隆创建 vm - 卷开启常驻缓存，保持厚制备  - 切换为精简制备，创建 vm 成功
                            源：含开启常驻缓存厚制备卷 - smtx elf630  +zbs570 以下版本 克隆创建 vm - 卷开启常驻缓存，保持厚制备  - 不能切换为精简制备，创建 vm 成功
                            源：含开启常驻缓存厚制备卷 - smtx elf630  +os 630 以下版本 克隆创建 vm - 卷开启常驻缓存，保持厚制备  - 不能切换为精简制备，创建 vm 成功
                        快照重建 vm
                            源：含开启常驻缓存厚制备卷 - 630 快照重建 vm - 卷开启常驻缓存，保持厚制备  - 切换为精简制备，创建 vm 成功
                            源：含开启常驻缓存厚制备卷 - smtx elf630  +zbs 570 快照重建 vm - 卷开启常驻缓存，保持厚制备  - 切换为精简制备，创建 vm 成功
                            源：含开启常驻缓存厚制备卷 - smtx elf630  +os 630 及以上版本 快照重建 vm - 卷开启常驻缓存，保持厚制备  - 切换为精简制备，创建 vm 成功
                            源：含开启常驻缓存厚制备卷 - smtx elf630  +zbs570 以下版本快照重 vm - 卷开启常驻缓存，保持厚制备  - 不能切换为精简制备，创建 vm 成功
                            源：含开启常驻缓存厚制备卷 - smtx elf630  +os 630 以下版本快照重建 vm - 卷开启常驻缓存，保持厚制备  - 不能切换为精简制备，创建 vm 成功
                    数据存储位置检查
                        vm 新建开启常驻缓存精简制备卷40G - 检查 集群常驻缓存减少 40G，集群存储空间不变，fio 写数据后，数据存储在 perf 层，不会下沉到 cap 层
                        vm 新建开启常驻缓存厚制备卷40G - 检查 集群常驻缓存减少 40G，存储空间减少 40G，fio 写数据后，数据存储在 perf 层
                        vm 已有 40G 精简制备卷，已 fio 20G 数据在 cap 层的 - 开启常驻缓存 - 已有数据提升至 perf 层，cap 层释放空间空间（占用 0G），检查集群存储空间增大回收 20G，常驻缓存层减小20G
                        vm 已有已 fio 数据在 cap 层的精简制备卷 - 开启常驻缓存，已有数据提升至常驻缓存层后 - fio 新数据 - 检查新数据在 perf 层不会发生下沉，不占用 cap 层空间（保持0G占用）
                        vm 已有 40G 厚制备卷，已 fio 20G 数据在 cap 层的 - 开启常驻缓存 - 已有数据提升至 perf 层，cap 层数据回收但不释放空间，检查集群存储空间不变保持 40G，常驻缓存层减小20G
                        vm 已有已 fio 数据在 cap 层的厚制备 40G卷 - 开启常驻缓存，已有数据提升至常驻缓存层后 - fio 新数据 - 检查新数据在 perf 层不会发生下沉，cap 层占用保持40G
                        vm 已开启 常驻缓存的厚制备40G卷 - 关闭常住缓存：已有数据发生下沉，下沉到 cap 层 - 释放常驻缓存空间 40G，存储空间保持占用厚制备40G - 集群释放40G 常驻缓存空间，存储空间不变
                        vm 已开启 常驻缓存的精简制备40G卷 - 关闭常住缓存：已有数据发生下沉，下沉到 cap 层 - 释放常驻缓存空间40G，存储空间下沉数据40G  - 集群释放40G 常驻缓存空间，新增下沉数据占用存储空间
                        存储空间不足 常驻缓存预留空间不足时 - 启用常驻缓存成功
                    ZBS-18769 的相关修复，检查 vm unmap
                        已开启常驻缓存精简制备的开机 windows vm - fio 写数据，关闭常驻缓存 进行 unmap 失败，vm 重启后操作 unmap 回收成功
                        已开启常驻缓存厚制备的开机 linux vm - fio 写数据，关闭常驻缓存 进行 unmap 失败，vm 重启后操作 unmap 回收成功
                系统配置检查
                    集群无ec厚制备8条带存储策略 - 630 创建虚拟 ec 卷 开启常驻缓存 使用精简制备 - 创建 卷成功 使用ec精简制备存储策略，tower/elf 都会检查添加 ec 厚制备存储策略
                    630 vm 卷开启常驻缓存精简制备时 如果没有对应的存储策略，会触发自动创建
                    删除目标端2副本精简存储策略 - 跨集群热迁移开启常驻缓存2副本精简制备vm. - 迁移成功，目标端新建该存储策略
            ELF-8072 热迁移默认启用 CPU Throttle 99% 持续指定时间后自动 abort
                新集群默认值检查
                    elf-tool  migration_caps  list
                升级集群默认值检查
                    elf-tool  migration_caps  list
                命令行设置
                    elf-tool  migration_caps enable_migration_with_tls
                    elf-tool  migration_caps disable_migration_with_tls
                    elf-tool  migration_caps enable_ac_cpu_throttle_timeout
                    elf-tool migration_caps disable_ac_cpu_throttle_timeout
                    elf-tool migration_caps   enable_ic_cpu_throttle_timeout
                    elf-tool migration_caps disable_ic_cpu_throttle_timeout
                    elf-tool migration_caps update_cpu_throttle_timeout_duration
                数据库
                    数据库记录默认配置 in_cluster true , across_cluster true
                迁移
                    集群内迁移，生效【throttle 优化】策略 - 迁移任务自动取消
                    跨集群热迁移，生效【throttle 优化】策略 - 迁移任务自动取消
            ELF-7977 虚拟机网卡粒度配置网卡队列数
                创建空白虚拟机
                    在「网络设备」配置步骤中，为每个虚拟网卡增加该编辑项
                    创建虚拟机，新网卡【网卡队列数】支持范围检查， 1-16
                编辑虚拟机网卡
                    开机虚拟机，已有网卡不支持编辑【网卡队列数】
                    开机虚拟机，新增  vlan  virtio 网卡支持设置【网卡队列数】
                    开机虚拟机，新增  VPC  virtio 网卡支持设置【网卡队列数】
                    开机虚拟机，新增  DPDK  virtio 网卡支持设置【网卡队列数】【630 不支持测试】
                    开机虚拟机，新增非 virtio 网卡不支持设置【网卡队列数】，如：e1000、直通网卡（PCI、SR-IOV）
                    关机虚拟机，编辑已有网卡【网卡队列数】， 新增 新增 virtio 网卡 支持设置【网卡队列数】
                    编辑网卡【网卡队列数】支持范围检查， 1-16
                特例虚拟机
                    SVM 虚拟机， 部署和编辑页面涉及，保持和普通虚拟机一样展示网卡队列数
                    其他系统服务虚拟机，不允许编辑网卡，每个网卡的网卡队列展示【自动配置】
                虚拟机详情
                    网卡位置展示【网卡队列数】， 自动配置 或者 1-16 的值
                虚拟机克隆为虚拟机
                    存量多网卡不同队列数配置的虚拟机，克隆虚拟机时，网卡队列数和源虚拟机配置一致
                虚拟机模版
                    虚拟机克隆为模版，弹窗提醒： 不包含网卡队列数配置
                    虚拟机转化为模版，弹窗提醒： 不包含网卡队列数配置
                    从模版创建虚拟机时，网卡队列数默认都是【自动配置】
                    从模版转化为虚拟机，新虚拟机网卡列数都是【自动配置】
                虚拟机快照
                    展示
                        列表不展示网卡队列数
                        源虚拟机存在情况下， 快照详情包含【网卡队列数】展示，和源虚拟机一致
                        源虚拟机被删除情况下， 快照详情包含【网卡队列数】展示，和源虚拟机一致
                    回滚
                        快照网卡队列不同， 虚拟机修改所有网卡的队列配置，快照回滚后虚拟机的【网卡队列数】和快照保持一致
                    重建
                        快照网卡队列不同，快照重建时网卡队列数默认保持和快照一致， 默认配置重建成功
                        快照网卡队列不同，快照重建时网卡队列数默认保持和快照一致， 修改所有网卡队列数重建成功
                虚拟机迁移
                    集群内迁移
                        集群内冷迁移， 检查网卡队列数保持不变
                        集群内热迁移， 检查网卡队列数保持不变
                    跨集群热迁移
                        跨集群热迁移
                            【源集群】和【目标集】都支持，迁移后保留配置
                                SMTXOS 630 跨集群热迁移到 SMTXOS 630
                                SMTXOS 630 跨集群热迁移到 SMTXELF 630
                                SMTXELF 630 跨集群热迁移到 SMTXOS 630
                                SMTXELF 630 跨集群热迁移到 SMTXELF 630
                                SMTX OS（ELF）5.1.5 for 宁德  跨集群热迁移到  SMTXOS 630
                                【SMTX OS（ELF）5.1.5 for 宁德】  跨集群热迁移到  【SMTX OS（ELF）5.1.5 for 宁德】
                            【源集群】不支持，【目标集】支持，迁移后网卡队列数是默认值【自动配置】
                                SMTX OS 515  跨集群热迁移到 SMTX OS 630
                                SMTX OS 620  跨集群热迁移到 SMTX OS 630
                                SMTX OS 515 跨集群热迁移到 【SMTX OS（ELF）5.1.5 for 宁德】
                            【源集群】支持，【目标集】不支持
                                【SMTX OS（ELF）5.1.5 for 宁德】 跨集群热迁移到 SMTXOS 620【单个迁移】，检查文案
                                【SMTX OS（ELF）5.1.5 for 宁德】 跨集群热迁移到 SMTXOS 620【批量迁移】，检查文案
                                迁移后目标虚拟机
                                    不做冷重启时，队列数与在源集群配置的一致。
                                    冷重启（强制重启 或者 关机再开机）后，队列数会变更为默认值【自动配置】
                        跨集群分段， 冷迁移
                            单个虚拟机， 跨集群冷迁移， 检查弹窗提示
                            单个虚拟机， 跨集群分段迁移， 检查弹窗提示
                            多个虚拟机批量跨集群冷迁移， 检查弹窗提示
                            多个虚拟机批量跨集群分段迁移， 检查弹窗提示
                虚拟机 OVF 导入导出
                    导入虚拟机界面不设置网卡多队列， 该属性使用默认值，如【自动配置】
                    导出 OVF 文件中不包含网卡队列数配置
                集群兼容性检查
                    GET /api/v2/elf/cluster_capabilities 包含 vNicExpectedQueues
                虚拟机回收站
                    虚拟机移入回收站再恢复， 网卡队列数不变
                Tower 事件
                    创建空白虚拟机
                    从快照重建 - 特例，只有重建描述，不包含虚拟机详细配置
                    从模版创建虚拟机
                    克隆虚拟机
                    编辑虚拟机事件
                Tower 权限
                    包含「编辑虚拟机」权限时，可编辑
                    不包含「编辑虚拟机」权限时，不可编辑
                集群升级
                    存量虚拟机的网卡队列数默认为【自动配置】( vm.data.nics[].expected_queues  = 0 )
                Tower 中英文界面检查
                    中文界面主要测试，英文界面回归检查一部分
            【补充测试】硬件设备直通 & 主机维护模式
                USB 直通
                    挂载 USB 的虚拟机所在主机进入维护模式，提示需要关闭该虚拟机
                USB over Network
                    挂载 USB 的虚拟机所在主机进入维护模式（正常迁移虚拟机）再退出维护模式（成功回迁虚拟机）
                SR-IOV 网卡
                    添加 SR-IOV 网卡的虚拟机所在主机进入维护模式，提示需要关闭该虚拟机
                PCI 网卡
                    添加  PCI 网卡的虚拟机所在主机进入维护模式（，提示需要关闭该虚拟机
                加密卡
                    挂载 加密卡 的虚拟机所在主机进入维护模式，提示需要关闭该虚拟机
                GPU
                    挂载 GPU 的虚拟机所在主机进入维护模式，提示需要关闭该虚拟机
                vGPU
                    挂载 vGPU 的虚拟机所在主机进入维护模式，提示需要关闭该虚拟机
                海光 HCT
                    添加 CCP 加密控制器的虚拟机所在主机进入维护模式，提示需要关闭该虚拟机
            【补充测试】硬件设备直通 & 虚拟机强制关机
                USB over Network
                    挂载 USB 的虚拟机强制关机，检查虚拟机所属主机状态正常
                SR-IOV 网卡
                    添加 SR-IOV 网卡的虚拟机强制关机，检查虚拟机所属主机状态正常
                PCI 网卡
                    添加  PCI 网卡的虚拟机强制关机，检查虚拟机所属主机状态正常
                加密卡
                    挂载 加密卡 的虚拟机强制关机，检查虚拟机所属主机状态正常
                GPU
                    挂载 GPU 的虚拟机强制关机，检查虚拟机所属主机状态正常
                vGPU
                    挂载 vGPU 的虚拟机强制关机，检查虚拟机所属主机状态正常
                海光 HCT
                    添加 CCP 加密控制器的虚拟机强制关机，检查虚拟机所属主机状态正常
            【项目任务 - 运维管理】支持修改时区（仅命令行） - 关联 ELF 测试
                修改时区
                    虚拟机不开启【恢复时同步主机时区】，主机修改时区，检查虚拟机时间不随主机时区发生变化， 虚拟机时间从暂停当时的时间开始继续运行
                    虚拟机开启【恢复时同步主机时区】，主机修改时区，虚拟机恢复后，检查虚拟机时间和主机时间一致（预期参考 utc 做同步）， 虚拟机时区不变
            【补充测试】OS 630 增加【GPU  L20 + 开放驱动 】
                SMTXOS-630-x86-hygon3-oe 【kernel 5.10】
                    L20 GPU 直通
                    L20 vGPU 直通
                SMTXOS-630-x86-hygon3-tl3 【kernel 5.4】
                    L20 GPU 直通
                    L20 vGPU 直通
            【补充测试】OS630 - TL3 SRIOV 功能验证
                hygon tl3
                    网卡列表 - 网卡用途修改为 SR-IOV , 并切分 vf 成功
                    2 个虚拟机关联 SR-IOV  网卡， 配置 ip 后可以 ping 到对方， 可以 ssh 到对方
                    网卡列表 - 网卡用途修改为 PCI 直通
                    虚拟机添加 PCI 网卡， 虚拟机内部配置 ip 后，可 ping 到网络内的其他机器
                arm tl3
                    网卡列表 - 网卡用途修改为 SR-IOV , 并切分 vf 成功
                    2 个虚拟机关联 SR-IOV  网卡， 配置 ip 后可以 ping 到对方， 可以 ssh 到对方
                    网卡列表 - 网卡用途修改为 PCI 直通
                    虚拟机添加 PCI 网卡， 虚拟机内部配置 ip 后，可 ping 到网络内的其他机器
            ELF-7593 支持内置 KMS 和国密算法
                Tower 关联集群
                    SMTX OS
                        关联 SMTXOS 不开启加密的集群，关联集群页面不展示加密
                        关联 SMTXOS-620 已开启加密的集群，关联集群页面展示加密配置，默认不加密， 可设置开启加密算法支持  AES-256
                        关联 SMTXOS-630 已开启加密的集群（KMS 不支持 SM4），关联集群页面展示加密配置，默认不加密， 开启时可设置加密算法  AES-256
                        关联 SMTXOS-630 已开启加密的集群（支持 SM4），关联集群页面展示加密配置，默认不加密， 开启时可设置加密算法  AES-256、SM4
                        Tower 480 关联 OS-620，关联后可成功开启加密
                        Tower 480 关联  OS-630，关联后可成功开启加密
                        tower 不存在当前集群关联的 KMS - 关联后 OS 630 集群不展示关联 KMS
                        关联已启用外置 KMS + AES-256 加密的集群， 关联后 OS-630 会展示算法 AES-256， 关联 KMS 服务展示空
                        关联已启用外置 KMS + AES-256 加密的集群， 关联后 OS-620 会展示算法 AES-256， 关联 KMS 服务展示空
                        关联已启用外置 KMS + SM4 加密的集群， 关联后 OS-630 会展示算法 SM4， 关联 KMS 服务展示空
                    SMTX ELF
                        ELF 和 存储集群不是都支持加密， 此时关联 SMTX ELF 集群不展示加密配置
                        关联存储集群只支持 AES-256，关联集群页面展示加密配置，默认不加密， 开启时可设置加密算法  AES-256
                        SMTX ELF 未关联存储集群， 关联集群页面不展示加密
                        SMTX ELF 关联多个存储集群， 关联集群页面不展示加密
                        Tower 480 关联 ELF-630 + ZBS-570，关联后可成功开启加密
                    ACOS
                        AOC 4.8.0 关联 ACOS 6.3.0，关联后可成功开启加密
                        关联已启用外置 KMS + SM4 加密的集群， 关联后 ACOS-630 会展示算法 AES-256， 和关联 KMS 服务
                集群加密设置
                    启用加密
                        不支持加密的集群（ OS-611 /  ZBS-561 ），集群 - 设置 - 导航项不展示加密
                        不支持内置 KMS（OS-620 / ZBS-562 ~ 564 / ACOS-620）， 默认不开启加密
                        不支持内置 KMS（OS-620 / ZBS-562 ~ 564 / ACOS-620）， 开启加密选择【外置可用密钥管理服务】 算法只能选择 AES-256， 同步检查 Tower 事件
                        不支持内置 KMS（OS-620 / ZBS-562 ~ 564 / ACOS-620）， 关闭加密，再开启加密
                        不支持内置 KMS（OS-620 / ZBS-562 ~ 564 / ACOS-620）， 所有 KMS 异常， 禁止开启加密
                        支持内置 KMS （ OS-630 / ZBS-570 / ACOS-630 ）， 默认不开启加密
                        支持内置 KMS （ OS-630 / ZBS-570 / ACOS-630 ）， 开启加密选择【外置可用密钥管理服务】， 同步检查 Tower 事件
                        支持内置 KMS （ OS-630 / ZBS-570 / ACOS-630 ）， 开启加密选择【内置密钥管理服务】， 同步检查 Tower 事件
                        支持内置 KMS （ OS-630 / ZBS-570 / ACOS-630 ）， 没有加密资源时， 切换加密服务,  设置成功， 同步检查 Tower 事件
                        支持内置 KMS （ OS-630 / ZBS-570 / ACOS-630 ）， 关闭加密，再开启加密
                        支持内置 KMS （ OS-630 / ZBS-570 / ACOS-630 ）， 所有 KMS 异常， 禁止开启加密
                    关闭加密
                        仅虚拟机包含加密卷，静态数据加密无法关闭
                        仅虚拟卷包含加密卷，静态数据加密无法关闭
                        仅模版包含加密卷（ OS 集群 加密虚拟机转化为模版），静态数据加密无法关闭
                        仅快照包含加密卷（ OS 集群 加密虚拟机创建快照，但源虚拟机被删除），静态数据加密无法关闭
                        虚拟机、虚拟卷、模版、快照 都不包含加密卷， 仅 zbs 存在加密资源，静态数据加密无法关闭
                        集群没有加密数据，静态数据加密关闭成功 - Tower 事件记录加密状态变更
                    KMS
                        编辑 KMS
                            内置 KMS 修改为外置 KMS， Tower 事件增加密钥管理服务变更值
                            外置 KMS 修改为内置 KMS， Tower 事件增加密钥管理服务变更值
                        内置 KMS （ OS-630 / ZBS-580 / ACOS-630 ）
                            内置 KMS 展示连接状态
                            重新加密 （在还有加密资源的情况下操作）
                            备份密钥，和上一个版本一致，不展示 KMS 类型和服务名称
                            下载密钥
                            导入密钥
                        外置 KMS
                            外置 KMS， 展示连接状态
                            重新加密（在还有加密资源的情况下操作）
                            备份密钥，和上一个版本一致，不展示 KMS 类型和服务名称
                            下载密钥
                            导入密钥
                集群默认存储策略
                    集群未开启加密
                        集群未开启加密，存储策略不展示数据加密设置
                    开启加密
                        ELF 关联存储的默认存储策略位置展示静态数据加密（已选择算法字符）， 也可以修改加密配置
                        开启静态数据加密，不选择加密算法，点保存，提示： 请选择加密算法
                        加密算法仅支持 AES-256 的集群， 加密算法设置为 AES-256 （选项只有 AES-256 ）
                        加密算法支持 AES-256、SM4  的集群，设置 AES-256， 设置后检查创建虚拟机/虚拟卷的加密选项
                        加密算法支持 AES-256、SM4  的集群，设置 SM4， 设置后检查创建虚拟机/虚拟卷的加密选项
                        集群已包含加密资源，不允许关闭静态数据加密开关和加密算法,  默认存储策略可随时编辑加密
                        集群没有加密资源时，关闭加密，再开启加密
                        所选 KMS 异常时， 未开启加密的集群，静态数据加密开关可用 KMS 服务禁止选择（只允许选择可用的服务）
                        所选 KMS 异常时， 已开启加密的集群，静态数据加密开关和加密算法选项全部禁用
                        集群配置内置 KSM， 默认存储策略设置开启加密 + AES-256 算法， 设置成功并检查事件
                        集群配置内置 KSM， 默认存储策略设置开启加密 + SM4 算法， 设置成功并检查事件
                        集群配置外置 KSM， 默认存储策略设置开启加密 + AES-256 算法， 设置成功并检查事件
                        集群配置外置 KSM， 默认存储策略设置开启加密 + SM4 算法， 设置成功并检查事件
                        集群配置外置 KSM,  外置 KSM 不支持 SM4 时， 默认存储策略设置开启加密, 算法选项不展示 SM4
                        OS-630、ZBS-580 集群默认存储策略可设置 不加密、AES-256、SM4
                        ELF-630 + OS-630 + ZBS-580， 存储集群默认存储策略可设置 不加密、AES-256 、SM4
                        ELF-620 + OS-630 + ZBS-580， 存储集群默认存储策略可设置 不加密、AES-256
                        ELF-630 + OS-620 + ZBS-570， 存储集群 OS-620、ZBS-570 集群默认存储策略可设置 不加密、AES-256
                        ELF-610 + OS-630 或者 ZBS-580， 存储集群默认存储策略不展示加密设置项
                        ACOS0630, 默认存储策略可设置 不加密、AES-256  ( KMS 支持 SM4 时算法设置项也不展示 SM4 )
                    关闭加密
                        集群不包含加密卷，集群存储策略关闭加密成功
                虚拟机
                    创建空白虚拟机
                        集群未开启加密， 创建虚拟机时磁盘存储策略位置不展示静态数据加密设置项
                        集群默认存储策略未启用加密,  创建空白虚拟机时磁盘默认展示不开启加密， 多磁盘设置不同加密配置创建虚拟机成功
                        集群默认存储策略 AES-256,  创建空白虚拟机时磁盘默认展示开启加密 + AES-256， 多磁盘设置不同加密配置创建虚拟机成功
                        集群默认存储策略 SM4,  创建空白虚拟机时磁盘默认展示开启加密 + SM4， 多磁盘设置不同加密配置创建虚拟机成功
                        创建虚拟机事件，增加加密配置
                    虚拟机编辑磁盘
                        编辑磁盘，已有磁盘不允许修改加密属性
                        编辑磁盘，新建卷默认加密属性和集群默认存储策略一致（ 不加密/AES-256/SM4 ）
                        编辑磁盘，新建卷可配置加密属性（添加多个磁盘覆盖不同加密配置）
                        编辑磁盘，挂载已有卷（ 不加密/AES-256/SM4 ）不允许修改加密配置，编辑成功，虚拟机开机正常
                        编辑虚拟机磁盘事件，增加加密配置
                    从虚拟机克隆虚拟机
                        克隆弹窗，已有磁盘默认和源卷加密配置一致，快速克隆成功，虚拟机开机正常
                        克隆弹窗，已有磁盘修改加密配置，完全克隆成功（不允许快速克隆），虚拟机开机正常
                        克隆弹窗，新建卷默认加密属性和集群默认存储策略一致（ 不加密/AES-256/SM4 ），克隆成功，虚拟机开机正常
                        克隆弹窗，新建卷可配置加密属性（添加多个磁盘覆盖不同加密配置），克隆成功，虚拟机开机正常
                        克隆弹窗，挂载已有卷（ 不加密/AES-256/SM4 ）不允许修改加密配置，克隆成功，虚拟机开机正常
                        克隆虚拟机磁盘事件，增加加密配置
                虚拟机快照
                    创建快照
                        虚拟机包含不同加密配置的虚拟卷（不加密、AES-256、SM4）， 创建普通快照成功
                        虚拟机包含不同加密配置的虚拟卷（不加密、AES-256、SM4）， 创建一致性普通快照成功
                    快照重建虚拟机
                        重建弹窗，已有磁盘默认和源卷加密配置一致，保持默认值，快速克隆成功，虚拟机开机正常
                        重建弹窗，已有磁盘修改加密配置，完全克隆成功（不允许快速克隆），虚拟机开机正常
                        重建弹窗，新建卷默认加密属性和集群默认存储策略一致（ 不加密/AES-256/SM4 ），克隆成功，虚拟机开机正常
                        重建弹窗，新建卷可配置加密属性（添加多个磁盘覆盖不同加密配置），克隆成功，虚拟机开机正常
                        重建弹窗，挂载已有卷（ 不加密/AES-256/SM4 ）不允许修改加密配置，克隆成功，虚拟机开机正常
                    快照回滚
                        虚拟机包含不同加密配置的虚拟卷（不加密、AES-256、SM4）创建快照，虚拟机不修改加密属性，回滚后加密属性不变
                        虚拟机包含不同加密配置的虚拟卷（不加密、AES-256、SM4）创建快照，虚拟机不允许修改加密属性2 ( 已有卷不支持修改 )，回滚后加密属性和虚拟机一致（属性1）
                    快照计划
                        创建快照组，快照组生成的快照中虚拟卷的加密状态与原虚拟卷一致
                        从快照组回滚虚拟机，虚拟卷的的加密状态与原虚拟卷一致
                        从快照组克隆虚拟机，虚拟卷加密设置默认与原虚拟卷一致
                    备份计划
                        虚拟机包含不同加密配置的虚拟卷（不加密、AES-256、SM4），可正常备份
                    复制计划
                        虚拟机包含不同加密配置的虚拟卷（不加密、AES-256、SM4），可正常复制
                虚拟机迁移
                    SMTXOS  集群内迁移
                        集群内冷热迁移，加密配置不变
                    SMTXOS  - OS 跨集群迁移 - 热、分段、冷 迁移
                        目标集群不支持加密
                            迁移弹窗不展示加密配置， 热迁移， 迁移目标虚拟机不加密
                            迁移弹窗不展示加密配置， 分段迁移， 迁移目标虚拟机不加密
                            迁移弹窗不展示加密配置， 冷迁移， 迁移目标虚拟机不加密
                        目标集群支持加密但关闭加密
                            迁移弹窗不展示加密配置， 热迁移， 迁移目标虚拟机不加密
                            迁移弹窗不展示加密配置， 分段迁移， 迁移目标虚拟机不加密
                            迁移弹窗不展示加密配置， 冷迁移， 迁移目标虚拟机不加密
                        源集群不支持加密，目标集群支持加密
                            源集群不支持加密（OS-610 迁移到 OS-620/OS-630 加密集群），  迁移弹窗会展示加密配置 - 热迁移
                            源集群不支持加密（OS-610 迁移到 OS-620/OS-630 加密集群），  迁移弹窗会展示加密配置 - 分段迁移
                            源集群不支持加密（OS-610 迁移到 OS-620/OS-630 加密集群），  迁移弹窗会展示加密配置 - 冷迁移
                        源集群支持加密（只支持 AES-256），目标集群支持加密
                            迁移弹窗默认展示目标集群存储策略配置（ 不加密、AES-256 ）
                            迁移弹窗设置不加密， 热迁移， 迁移目标虚拟机不加密
                            迁移弹窗设置不加密， 分段迁移， 迁移目标虚拟机不加密
                            迁移弹窗设置不加密， 冷迁移， 迁移目标虚拟机不加密
                            迁移弹窗设置加密算法 AES-256 ， 热迁移， 迁移目标虚拟机加密算法 AES-256
                            迁移弹窗设置加密算法 AES-256 ， 分段迁移， 迁移目标虚拟机加密算法 AES-256
                            迁移弹窗设置加密算法 AES-256 ， 冷迁移， 迁移目标虚拟机加密算法 AES-256
                        源集群支持加密（支持 AES-256、SM4 ），目标集群支持加密
                            迁移弹窗默认展示目标集群存储策略配置（ 不加密、AES-256、SM4 ）
                            目标集群不支持 SM4 算法， 迁移弹窗默认加密算法不展示 SM4， （ tower oapi  和 elf api 返回 zbs 给的错误 ）
                            迁移弹窗设置不加密， 热迁移， 迁移目标虚拟机不加密
                            迁移弹窗设置不加密， 分段迁移， 迁移目标虚拟机不加密
                            迁移弹窗设置不加密， 冷迁移， 迁移目标虚拟机不加密
                            迁移弹窗设置加密算法 AES-256 ， 热迁移,   迁移目标虚拟机加密算法 AES-256
                            迁移弹窗设置加密算法 AES-256 ， 分段迁移,   迁移目标虚拟机加密算法 AES-256
                            迁移弹窗设置加密算法 AES-256 ， 冷迁移,   迁移目标虚拟机加密算法 AES-256
                            迁移弹窗设置加密算法 SM4 ， （630 - 630 ）热迁移， 迁移目标虚拟机加密算法 SM4
                            迁移弹窗设置加密算法 SM4 ， （620 - 630 ）热迁移有文案提示， 分段和冷迁移没有文案
                            迁移弹窗设置加密算法 SM4 ， 分段迁移， 迁移目标虚拟机加密算法 SM4
                            迁移弹窗设置加密算法 SM4 ， 冷迁移， 迁移目标虚拟机加密算法 SM4
                    SMTXELF - 仅迁移计算 - 集群内热迁移
                        源虚拟机开启加密， 冷热迁移成功
                        源虚拟机不开启加密， 冷热迁移成功
                    SMTXELF - 仅迁移计算 - 跨集群热迁移
                        源虚拟机开启加密， 热迁移成功
                        源虚拟机不开启加密， 热迁移成功
                    SMTXELF - 仅迁移存储 - 热迁移
                        目标存储集群不支持加密
                            迁移弹窗不展示加密配置， 迁移目标虚拟机不加密
                        目标存储集群支持加密但关闭加密
                            迁移弹窗不展示加密配置， 迁移目标虚拟机不加密
                        源集群不支持加密， 目标存储集群开启加密
                            迁移弹窗会展示加密配置，但是不允许设置， 有提示
                        源集群开启加密， 目标存储集群开启加密 - 620 迁移到 620
                            迁移弹窗展示加密配置（目标集群默认存储策略）， 迁移目标虚拟机按迁移弹窗设置生效
                            设置不加密，迁移成功
                            设置 AES-256 ，迁移成功
                        源集群开启加密， 目标存储集群开启加密 - 620 迁移到 630
                            迁移弹窗展示加密配置（目标集群默认存储策略）， 迁移目标虚拟机按迁移弹窗设置生效
                            设置不加密，迁移成功
                            设置 AES-256 ，迁移成功
                            无法选择 SM4
                        源集群开启加密， 目标存储集群开启加密 - 630 迁移到 630
                            迁移弹窗展示加密配置（目标集群默认存储策略， 不加密、AES-256、SM4 ）， 迁移目标虚拟机按迁移弹窗设置生效
                            设置不加密，迁移成功
                            设置 AES-256 ，迁移成功
                            设置 SM4 ，迁移成功
                            目标存储集群不支持 SM4 算法， 迁移弹窗默认加密算法不展示 SM4  ( tower oapi 和 elf api 返回 zbs 给的错误 )
                    SMTXELF - 迁移计算加存储 - 热迁移
                        目标存储集群不支持加密
                            迁移弹窗不展示加密配置， 迁移目标虚拟机不加密
                        目标存储集群支持加密但关闭加密
                            迁移弹窗不展示加密配置， 迁移目标虚拟机不加密
                        源存储集群不支持加密， 目标存储集群支持加密
                            迁移弹窗展示加密配置但是禁用， 迁移目标虚拟机不加密
                        源存储集群支持加密， 目标存储集群支持加密 - 620 迁移到 620
                            迁移弹窗展示加密配置（目标集群默认存储策略）， 迁移目标虚拟机按迁移弹窗设置生效
                            迁移设置不加密
                            迁移设置 AES-256
                        源存储集群支持加密， 目标存储集群支持加密 - 620 迁移到 630
                            迁移弹窗展示加密配置（目标集群默认存储策略）， 迁移目标虚拟机按迁移弹窗设置生效
                            迁移设置不加密
                            迁移设置 AES-256
                            不支持选择 SM4,   迁移方式在选择热迁移的时候有文案提示
                        源存储集群支持加密， 目标存储集群支持加密 - 630 迁移到 630
                            迁移弹窗展示加密配置（目标集群默认存储策略）， 迁移目标虚拟机按迁移弹窗设置生效
                            迁移设置不加密
                            迁移设置 AES-256
                            迁移设置 SM4
                            目标存储集群不支持 SM4 算法， 迁移弹窗默认加密算法不展示 SM4 （ tower oapi 和 elf api 返回 zbs 给的错误）
                    OS 和 ELF 相互迁移 - 热迁移
                        OS 迁移到 ELF
                            OS-630 热迁移到 ELF-630 + ZBS-570+ /  ELF-630 + OS-630， 迁移设置不加密, 迁移成功
                            OS-630 热迁移到 ELF-630 + ZBS-570+ /  ELF-630 + OS-630， 迁移设置 AES-256, 迁移成功
                            OS-630 热迁移到 ELF-630 + ZBS-580 /  ELF-630 + OS-630， 迁移设置 SM4（目标端 KMS 支持 SM4）,  迁移成功
                            OS-630 热迁移到 ELF-630 + ZBS-580 /  ELF-630 + OS-630（ 目标端 KMS 不支持 SM4）， 迁移页面无法选择 SM4
                            OS-630 热迁移到 ELF-630 + OS620， 设置不加密， 迁移成功
                            OS-630 热迁移到 ELF-630 + OS620， 设置 AES-256， 迁移成功
                            OS-630 热迁移到 ELF-630 + OS620， 迁移弹窗不展示 SM4
                            OS-630 热迁移到 ELF-630 + ZBS-564， 迁移弹窗不展示加密算法， 迁移目标虚拟机不加密
                            OS-620 热迁移到 ELF-630 + ZBS-570+ / ELF-630 + OS-620,   迁移设置不加密 , 迁移成功
                            OS-620 热迁移到 ELF-630 + ZBS-570+ / ELF-630 + OS-620,   迁移设置 AES-256, 迁移成功
                            OS-620 热迁移到 ELF-630 + OS-630， 设置不加密, 迁移成功
                            OS-620 热迁移到 ELF-630 + OS-630， 设置 AES-256, 迁移成功
                            OS-620 热迁移到 ELF-630 + OS-630，无法 设置 SM4
                            OS-610 热迁移到 ELF-630 + ZBS-570 / ELF-630 + OS-630， 迁移弹窗会展示加密属性但禁用且有提示， 迁移目标虚拟机不加密
                        ELF 迁移到 OS
                            ELF-630 + ZBS-570+ 热迁移到 OS-630， 设置不加密， 迁移成功
                            ELF-630 + ZBS-570+ 热迁移到 OS-630， 设置 AES-256， 迁移成功
                            ELF-630 + ZBS-580、OS-630 热迁移到 OS-630， 设置 SM4（ 目标端 KMS 支持 SM4 ）， 迁移成功
                            ELF-630 + ZBS-570、OS-620 热迁移到 OS-630， 设置 SM4（ 目标端 KMS 支持 SM4 ）， 迁移成功
                            ELF-630 + ZBS-580、OS-630 热迁移到 OS-630， 无法设置 SM4（  目标端 KMS 不支持 SM4 ）
                            ELF-620 + ZBS-570 热迁移到 OS-630， 设置不加密， 迁移成功
                            ELF-620 + ZBS-570 热迁移到 OS-630， 设置 AES-256， 迁移成功
                            ELF-620 + ZBS-570 热迁移到 OS-630，不支持 设置 SM4
                            ELF-610 + ZBS-570 热迁移到 OS-630， 迁移弹窗会展示加密属性但禁用且有提示， 迁移目标虚拟机不加密
                虚拟卷
                    创建（非共享）虚拟卷
                        默认和集群默认存储策略一致， 设置不加密，创建成功
                        设置 AES-256 加密，创建成功
                        设置 SM4 加密，创建成功
                    创建共享虚拟卷
                        默认和集群默认存储策略一致， 设置不加密，创建成功
                        设置 AES-256 加密，创建成功
                        设置 SM4 加密，创建成功
                    克隆虚拟卷
                        不展示加密属性，克隆后和源卷加密属性一致
                内容库模版
                    模版分发
                        OS-620 集群1 的 AES-256 加密虚拟机
                            克隆为模版， 转化为 OS-620 集群1 （支持 AES-256）的虚拟机，检查新虚拟机磁盘保持加密，和源虚拟机一致
                            克隆为模版， 分发到其他 OS-620 集群2（支持 AES-256）， 再转化为虚拟机，检查新虚拟机磁盘不加密
                            转化为模版， 分发到其他 OS-620 集群2（支持 AES-256）， 再转化为虚拟机，检查新虚拟机磁盘不加密
                            克隆为模版，分发到其他 OS-630 集群3（支持所有算法），再转化为虚拟机，检查新虚拟机磁盘不加密
                            克隆为模版，分发到其他 ZBS-570 集群4（仅支持AES-256），再转化为（ELF-任意版本 + ZBS-570 集群的）虚拟机，检查新虚拟机磁盘不加密
                        OS-630 集群1 的 AES-256/SM4 加密虚拟机
                            AES-256
                                克隆为模版， 转化为 OS-630 集群1 （支持所有算法）的虚拟机，检查新虚拟机磁盘保持加密，和源虚拟机一致
                                克隆为模版， 分发到其他 OS-630 集群2（支持所有算法）， 再转化为虚拟机，检查新虚拟机磁盘不加密
                                转化为模版， 分发到其他 OS-630 集群2（支持所有算法）， 再转化为虚拟机，检查新虚拟机磁盘不加密
                                克隆为模版，分发到其他 OS-620 集群3（仅支持 AES-256），再转化为虚拟机，检查新虚拟机磁盘不加密
                                克隆为模版，分发到其他 ZBS-570 集群4（仅支持AES-256），再转化为（ELF-任意版本 + ZBS-570 集群的）虚拟机，检查新虚拟机磁盘不加密
                            SM4
                                克隆为模版， 转化为 OS-630 集群1 （支持所有算法）的虚拟机，检查新虚拟机磁盘保持加密，和源虚拟机一致
                                克隆为模版， 分发到其他 OS-630 集群2（支持所有算法）， 再转化为虚拟机，检查新虚拟机磁盘不加密
                                转化为模版， 分发到其他 OS-630 集群2（支持所有算法）， 再转化为虚拟机，检查新虚拟机磁盘不加密
                                克隆为模版，分发到其他 OS-620 集群3（仅支持 AES-256），再转化为虚拟机，检查新虚拟机磁盘不加密
                                克隆为模版，分发到其他 ZBS-570 集群4（仅支持AES-256），再转化为（ELF-任意版本 + ZBS-570 集群的）虚拟机，检查新虚拟机磁盘不加密
                        ELF 630 + ZBS-580/OS-630 集群1 的 AES-256/SM4 加密虚拟机
                            AES-256
                                克隆为模版， 转化为 ELF 630 集群1 （支持所有算法）的虚拟机，检查新虚拟机磁盘不加密
                                克隆为模版，分发到其他 ZBS-570 集群2（仅支持AES-256），再转化为（ELF-任意版本 + ZBS-570 集群的）虚拟机，检查新虚拟机磁盘不加密
                                转化为模版，分发到其他 ZBS-570 集群2（仅支持AES-256），再转化为（ELF-任意版本 + ZBS-570 集群的）虚拟机，检查新虚拟机磁盘不加密
                                克隆为模版，分发到其他 OS-630 集群3（支持所有算法），再转化为虚拟机，检查新虚拟机磁盘不加密
                                克隆为模版，分发到其他 OS-620 集群4（仅支持 AES-256），再转化为虚拟机，检查新虚拟机磁盘不加密
                            SM4
                                克隆为模版， 转化为 ELF 630 集群1 （支持所有算法）的虚拟机，检查新虚拟机磁盘不加密
                                克隆为模版，分发到其他 ZBS-570 集群2（仅支持AES-256），再转化为（ELF-任意版本 + ZBS-570 集群的）虚拟机，检查新虚拟机磁盘不加密
                                转化为模版，分发到其他 ZBS-570 集群2（仅支持AES-256），再转化为（ELF-任意版本 + ZBS-570 集群的）虚拟机，检查新虚拟机磁盘不加密
                                克隆为模版，分发到其他 OS-630 集群3（支持所有算法），再转化为虚拟机，检查新虚拟机磁盘不加密
                                克隆为模版，分发到其他 OS-620 集群4（仅支持 AES-256），再转化为虚拟机，检查新虚拟机磁盘不加密
                    模版创建虚拟机
                        OS-620 （仅支持 AES-256）模版 - 不分发创建虚拟机
                            未加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 集群默认存储策略未启用加密
                            未加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 集群默认存储策略已启用加密 AES-256
                            AES-256 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 集群默认存储策略未启用加密
                            AES-256 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 集群默认存储策略已启用加密 AES-256
                            虚拟机（磁盘含 不加密、AES-256 ）转化为模版， 模版转化为虚拟机，磁盘含 不加密、AES-256
                        OS-630 （支持 AES-256 + SM4）模版 - 不分发创建虚拟机
                            未加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略未启用加密
                            未加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略已启用加密 AES-256
                            未加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略已启用加密 SM4
                            AES-256 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略未启用加密
                            AES-256 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略已启用加密 AES-256
                            AES-256 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略已启用加密 SM4
                            SM4 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机 ，默认存储策略未启用加密
                            SM4 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机 ，默认存储策略已启用加密 AES-256
                            SM4 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机 ，默认存储策略已启用加密 SM4
                            虚拟机（磁盘含 不加密、AES-256、SM4 ）转化为模版， 模版转化为虚拟机，磁盘含 不加密、AES-256、SM4
                        ELF + 存储集群（存储集群不支持加密）的模版 - 不分发创建虚拟机（模版不保留加密配置）
                            未加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略未启用加密
                        ELF + 存储集群（仅支持 AES-256）的模版 - 不分发创建虚拟机（模版不保留加密配置）
                            未加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略未启用加密
                            未加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略已启用加密 AES-256
                            AES-256 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略未启用加密
                            AES-256 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略已启用加密 AES-256
                            虚拟机（磁盘含 不加密、AES-256）转化为模版， 模版转化为虚拟机
                        ELF + 存储集群（支持 AES-256 + SM4）的模版 - 不分发创建虚拟机（模版不保留加密配置）
                            未加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略未启用加密
                            未加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略已启用加密 AES-256
                            未加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略已启用加密 SM4
                            AES-256 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略未启用加密
                            AES-256 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略已启用加密 AES-256
                            AES-256 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机， 默认存储策略已启用加密 SM4
                            SM4 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机 ，默认存储策略未启用加密
                            SM4 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机 ，默认存储策略已启用加密 AES-256
                            SM4 加密虚拟机克隆为模版， 模版创建（克隆）虚拟机 ，默认存储策略已启用加密 SM4
                            虚拟机（磁盘含 不加密、AES-256、SM4 ）转化为模版， 模版转化为虚拟机
                        OS 集群加密模版，转到为虚拟机
                            os-620 ( AES-256) 加密虚拟机克隆为模版，elf-620 +  os-620 ( AES-256 ) 模版转化为虚拟机,  目标虚拟机保持加密算法
                            elf620+ os630(AES+SM4)，转化为虚拟机
                            elf-630 + os-620 ( AES-256 ) 模版，转化为虚拟机， 目标虚拟机保持加密算法
                            elf-630 + os-630 ( AES-256 + SM4 )，转化为虚拟机， 目标虚拟机保持加密算法
                    模版创建 + 分发场景
                        OS 集群加密模版（加密虚拟机克隆为当前集群模版）， 创建虚拟机选择其他集群， 磁盘启用加密， 最后的克隆选项应该是完全克隆
                    存量模版数据检查
                        zbs570 模版--tower470 升级 tower480 使用
                            检查 升级 480后，模版元数据 contentLibraryVmTemplate.vm_disks 不记录常驻缓存属性 - contentLibraryVmTemplate.zbs_storage_info 加密属性为 null, iscsiLunSnapshots 卷 iscsi lun 开启加密
                            分发到其他 os/zbs 集群，分发的目标 os/zbs  模版元数据和 iscsi lun  加密关闭
                            elf630 + zbs 模版克隆创建 vm  - zbs 集群默认存储策略加密配置关闭 - vm加密属性与一致所有卷加密关闭 - 完全拷贝（模版开启加密的卷完全克隆）
                            elf620 +zbs 模版克隆创建 vm  - zbs 集群默认存储策略加密配置开启 - vm加密属性与一致所有卷加密开启 - 完全拷贝（模版未开启加密的卷完全克隆）
                            模版转化为 elf630+zbs570 - vm 开启加密 AES
                            模版转化为 elf620+zbs570 - vm 开启加密 AES
                OVF
                    虚拟机
                        630 包含 AES-256/SM4 加密属性的虚拟机 OVF 导出成功， OVF 文件不记录加密属性
                        630 包含 AES-256/SM4 加密属性的虚拟机 OVF 导出再导入 不支持加密的集群（如 610）
                        630 包含 AES-256/SM4 加密属性的虚拟机 OVF 导出再导入  VMware
                        630 包含 AES-256/SM4 加密属性的虚拟机 OVF 导出再导入  相同集群,  导入弹窗磁盘默认加密配置和集群默认存储策略一致
                        630 包含 AES-256/SM4 加密属性的虚拟机 OVF 导出再导入  相同集群,  修改磁盘加密属性（不加密/AES-256/SM4），导入成功
                        630 包含 AES-256/SM4 加密属性的虚拟机 OVF 导出再导入 ， 导入时新创建虚拟卷不加密/AES-256/SM4），导入成功
                        630 包含 AES-256/SM4 加密属性的虚拟机 OVF 导出再导入 ， 导入时挂载已有卷（不加密/AES-256/SM4）不允许修改加密配置， 导入成功
                    虚拟卷
                        630 包含 AES-256/SM4 加密属性的虚拟卷， 对应磁盘导出 qcow、raw、vmdk， 导出成功
                        630 包含 AES-256/SM4 加密属性的虚拟卷， 再导入不支持加密的集群（如 610），导入成功
                        630 包含 AES-256/SM4 加密属性的虚拟卷， 再导入相同集群时， 导入窗口磁盘加密属性和集群默认存储策略配置一致（不加密/AES-256/SM4）
                        630 包含 AES-256/SM4 加密属性的虚拟卷，导入时按默认配置，导入成功，虚拟机挂载磁盘开机正常
                        630 包含 AES-256/SM4 加密属性的虚拟卷，导入时修改加密配置（和默认值不同），导入成功，虚拟机挂载磁盘开机正常
                    虚拟机模版
                        630 包含 AES-256/SM4 加密属性的虚拟机 OVF 导出成功， OVF 文件不记录加密属性
                        630 包含 AES-256/SM4 加密属性的虚拟机， OVF 导出再导入模版时， 导入弹窗保留加密配置项， 默认展示集群默认存储策略的值
                集群运维
                    主机关机再开机
                        已开启加密已开启  HA 的虚拟机， HA 重建成功，虚拟机开机系统正常
                        已开启加密已未开启  HA 的虚拟机， 被主机关机一起关机了虚拟机（不会留下日志和事件）， 重新开机主机开机虚拟机后系统正常
                    主机重启
                        已开启加密已开启  HA 的虚拟机， HA 重建或状态恢复，虚拟机开机系统正常
                        已开启加密已未开启  HA 的虚拟机， 被 HA self fence 暂停或关机， 重新开机后系统正常
                    集群升级
                        不支持加密的集群，升级到支持加密的集群
                            升级前
                                准备存量虚拟机， 包含 3+ 磁盘，方便升级后设置不同加密算法
                                准备存量快照
                                准备存量模版
                            升级后检查
                                集群开启加密，设置默认加密算法 AES-256/SM4
                                存量虚拟机， 克隆虚拟机，开启加密,  配置 AES-256/SM4
                                存量虚拟机， 编辑添加新磁盘，配置 AES-256/SM4
                                存量虚拟机， 创建快照， 从快照重建虚拟机，开启加密,  配置 AES-256/SM4
                                存量虚拟机， 转化为模板，从模板创建开启加密虚拟机,  配置 AES-256/SM4
                                存量虚拟机，克隆为模板，从模板创建开启加密虚拟机,  配置 AES-256/SM4
                                存量虚拟机快照检查， 回滚虚拟机
                                存量虚拟机快照检查， 从快照创建虚拟机，开启加密,  配置 AES-256/SM4
                                存量虚拟机快照检查， 快照原虚拟机开启加密后，用存量快照回滚， 回滚后虚拟机保持不加密（和存量快照的加密配置一致
                                存量虚拟机模板检查，从模板创建开启加密虚拟机,  配置 AES-256/SM4
                                存量虚拟机模板检查，模板转化为虚拟机
                        支持加密的集群升级，升级过程中
                            升级前
                                准备存量已配置加密虚拟机、虚拟卷、模版、快照
                            升级后检查
                                集群加密算法展示 AES-256 算法
                                存量虚拟机检查， 克隆虚拟机，开启加密,  配置 AES-256
                                存量虚拟机检查， 编辑虚拟机，新增磁盘配置 AES-256
                                存量虚拟机检查， 创建快照， 从快照重建虚拟机，开启加密,  配置 AES-256
                                存量虚拟机检查， 转化为模板，从模板创建开启加密虚拟机,  配置 AES-256
                                存量虚拟机检查， 克隆为模板，从模板创建开启加密虚拟机,  配置 AES-256
                                存量虚拟机快照检查,  回滚虚拟机
                                存量虚拟机快照检查,  从快照创建虚拟机，开启加密,  配置 AES-256
                                存量虚拟机快照检查,   快照原虚拟机开启加密后，用存量快照回滚， 回滚后虚拟机保持加密（和存量快照的加密配置一致， 已有卷不允许修改加密配置）
                                存量虚拟机模板检查,  从模板创建开启加密虚拟机,  配置 AES-256
                                存量虚拟机模板检查,   模板转化为虚拟机
                    角色转换
                        zbs-meta 转给 storage， 检查加密虚拟机内部 io 正常
                        storage 转为 zbs-meta， 再设置为 leader， 检查加密虚拟机内部 io 正常
                    主机维护模式
                        包含加密虚拟机的主机进入退出维护模式正常， 检查加密虚拟机内部 io 正常
                故障场景
                    国密 SM4 KVM 故障
                        KMS 异常后（连接异常/证书异常）
                            创建加密虚拟机/虚拟卷，Tower 禁止创建
                            克隆加密虚拟机，禁止开启加密，克隆失败
                            虚拟机创建快照/一致性快照，创建失败
                            从加密模板创建虚拟机，禁止开启加密，克隆任务失败
                            从加密快照回滚虚拟机/重建虚拟机，回滚成功，重建禁止开启加密，重建任务卡住，KMS 恢复后任务成功
                            跨集群热/冷/分段迁移加密虚拟机，迁移失败
                            导入虚拟机，禁止开启加密
                            导出加密虚拟机，导出失败
                            虚拟机开机，开机成功，无法进入系统
                            虚拟机重启，重启成功， 无法进入系统
                            加密虚拟机关机，关机成功
                            加密虚拟机强制关机，关机成功
                            虚拟机 Guest OS 内读写文件，虚拟机 IO 异常
                            开启 HA 的虚拟机，触发 HA，HA 成功
                            未开启 HA 的虚拟机，系统 Hang，恢复 KMS 后，系统进入readonly 状态， 关机再开机后系统可正常使用
                        虚拟机操作过程中 KMS 异常
                            创建加密虚拟机/虚拟卷，创建失败
                            克隆加密虚拟机，克隆失败
                            虚拟机创建快照/一致性快照，创建失败
                            从加密模板创建虚拟机，创建失败
                            从加密快照回滚虚拟机/重建虚拟机，操作失败
                            导入虚拟机，开启加密，导入失败
                            导出加密虚拟机，导出失败
                            虚拟机开机，开机失败
                            虚拟机重启，重启失败
                            加密虚拟机关机，关机失败
                            加密虚拟机强制关机，关机成功
                            虚拟机 Guest OS 内读写文件，虚拟机 IO 异常
                            开启 HA 的虚拟机，触发 HA，HA 重试多次后失败
                            未开启 HA 的虚拟机，系统 Hang，导入密钥恢复时，短暂 hang 或 长时间 hang 的虚拟机行为，系统进入readonly 状态
                            跨集群热迁移加密虚拟机，源集群故障，迁移失败
                            跨集群热迁移加密虚拟机，目标集群故障，迁移失败
                            跨集群冷迁移加密虚拟机，源集群故障，迁移失败
                            跨集群冷迁移加密虚拟机，目标集群故障，迁移失败
                            跨集群分段迁移加密虚拟机，原始数据传输阶段，迁移失败
                            跨集群分段迁移加密虚拟机，增量数据传输阶段，迁移失败，清理目标集群数据
                    内置 KMS 故障
                        KMS 异常后（连接异常/证书异常）
                            创建加密虚拟机/虚拟卷，Tower 创建任务失败， EKMSConnectFailed
                            克隆加密虚拟机，克隆失败， 提示：连接密钥管理服务失败
                            虚拟机创建快照/一致性快照，创建失败， 任务提示： 连接密钥管理服务失败
                            从加密模板创建虚拟机（磁盘保持加密），创建任务失败（连接密钥管理服务失败）
                            从加密快照回滚虚拟机/重建虚拟机，回滚成功，重建禁止开启加密，重建任务卡住，KMS 恢复后任务成功
                            跨集群热/冷/分段迁移加密虚拟机，迁移失败
                            导入虚拟机失败，提示不支持加密
                            导出加密虚拟机，导出失败
                            虚拟机开机，开机失败
                            虚拟机重启，重启成功
                            加密虚拟机关机，关机成功
                            加密虚拟机强制关机，关机成功
                            虚拟机 Guest OS 内读写文件，虚拟机 IO 异常
                            开启 HA 的虚拟机，触发 HA 重建成功
                            未开启 HA 的虚拟机，系统 Hang，导入密钥恢复时，短暂 hang 或 长时间 hang 的虚拟机行为，系统进入readonly 状态
                        虚拟机操作过程中 KMS 异常
                            创建加密虚拟机/虚拟卷，创建失败
                            克隆加密虚拟机，克隆失败
                            虚拟机创建快照/一致性快照，创建失败
                            从加密模板创建虚拟机，创建失败
                            从加密快照回滚虚拟机/重建虚拟机，操作失败
                            导入虚拟机，开启加密，导入失败
                            导出加密虚拟机，导出失败
                            虚拟机开机，开机失败
                            虚拟机重启，重启失败
                            加密虚拟机关机，关机失败
                            加密虚拟机强制关机，关机成功
                            虚拟机 Guest OS 内读写文件，虚拟机 IO 异常
                            开启 HA 的虚拟机，触发 HA，HA 重试多次后失败
                            未开启 HA 的虚拟机，系统 Hang，导入密钥恢复时，短暂 hang 或 长时间 hang 的虚拟机行为，系统进入readonly 状态
                            跨集群热迁移加密虚拟机，源集群故障，迁移失败
                            跨集群热迁移加密虚拟机，目标集群故障，迁移失败
                            跨集群冷迁移加密虚拟机，源集群故障，迁移失败
                            跨集群冷迁移加密虚拟机，目标集群故障，迁移失败
                            跨集群分段迁移加密虚拟机，原始数据传输阶段，迁移失败
                            跨集群分段迁移加密虚拟机，增量数据传输阶段，迁移失败，清理目标集群数据
                    内置 KMS 服务主机切换
                        检查加密虚拟机内部 io 正常
                        zbs-meta leader 切换 和虚拟机开启关闭加密并行，预期虚拟机编辑任务可以成功（至少不会因为加密失败）
                加密加速
                    集群 - 设置 - 加密
                        展示加密加速开关
                        未开启加密加速的集群，密钥管理服务不允许选择只支持 SM4 的 KMS
                        开启加密加速的集群，密钥管理服务可以选择只支持 SM4 的 KMS
                    集群 - 设置 - 默认存储策略
                        集群加密加速未开启， 关联仅支持 SM4 的 KMS或者内置 KMS， 此时默认存储策略设置算法选项不允许设置 SM4
                        集群加密加速开启， 关联仅支持 SM4 的 KMS或者内置 KMS， 此时默认存储策略设置算法选项可以设置 SM4
                    跨集群迁移
                        OS-620+  -->  OS-630
                            目标集群未开启加密加速， 迁移弹窗的加密算法展示 SM4 但是不支持选择，有提示
                            目标集群开启加密加速， 迁移弹窗的加密算法展示 SM4 且可以选择，没有提示，检查迁移成功
                        OS-620+  -->  ELF-630 + OS-630
                            目标集群未开启加密加速， 迁移弹窗的加密算法展示 SM4 但是不支持选择，有提示
                            目标集群开启加密加速， 迁移弹窗的加密算法展示 SM4 且可以选择，没有提示，检查迁移成功
            ELF-7840 支持集群预留和虚拟机开启 iothread
                集群设置
                    查看集群设置 elf-tool elf_cluster get_iothread_pcpu
                    set_iothread_pcpu
                        集群没有独占虚拟机
                            配置 iothread count = 0（ 取消  iothread 预留），执行成功，  且可重复执行
                            配置 iothread count 小于主机可用 pcpu 数量 ，执行成功
                            配置 iothread count 大于主机可用 pcpu 数量 ，执行失败，CLUSTER_IOTHREAD_CAPABILITY_RESERVED_PCPU_FAILED
                            配置增加  iothread count， 小于主机可用 pcpu 数量时 ，执行成功
                            配置 iothread count 前后检查 vms_summary， vms_summary.available_exclusive_cpu 的差值为  iothread count
                            虚拟机已启用 iothread， 集群关闭 iothread  失败 CLUSTER_IOTHREAD_CAPABILITY_DECREASING_RESERVATION_PRECHECK_FAILED
                        集群有独占虚拟机
                            未配置 iothread pcpu， 开启 iothread 失败， 约束仅集群没有独占虚拟机时，才允许动态配置 io_thread 预留；
                            已配置 iothread pcpu 增加 count 设置失败，CLUSTER_IOTHREAD_CAPABILITY_EXCLUSIVE_CHECK_FAILED
                            已配置 iothread pcpu 减少 count 设置成功
                    set_iothread_pcpu_on_host
                        elf-tool elf_cluster set_iothread_pcpu_on_host <host_uuid> <pcpu_list> # 配置指定节点, pcpu 绑定关系
                        集群没有独占虚拟机
                            已知 count =0， 配置 1节点 iothread 预留（ pcpu 范围 = 2 ）， 设置失败 CLUSTER_IOTHREAD_CAPABILITY_MISMATCH_LENGTH
                            已知 count =2， 配置 1节点 iothread 预留（ pcpu 范围 = 2 ）， 设置成功
                            已知 count =2， 配置 2节点 iothread 预留（  pcpu 范围 = 4 ），  设置失败 CLUSTER_IOTHREAD_CAPABILITY_MISMATCH_LENGTH
                            已知 count =2， 配置 1节点 iothread 预留（ pcpu 范围 = 1 ）， 设置失败 CLUSTER_IOTHREAD_CAPABILITY_MISMATCH_LENGTH
                        集群有独占虚拟机
                            set_iothread_pcpu_on_host 设置独占虚拟机 pcpu 位置，设置失败
                            set_iothread_pcpu_on_host 设置空闲 pcpu 位置（非独占虚拟机），设置失败
                虚拟机设置 io_thread
                    集群未启用 iothread 预留， 关机虚拟机启用 iothread 能力失败 ELF_CLUSTER_IOTHREAD_DISABLED
                    集群已启用 iothread 预留， 开机虚拟机启用 iothread 能力失败 PRECHECK_VMS_STATE_UNMATCH
                    集群已启用 iothread 预留， 关机虚拟机启用 iothread 能力成功
                    虚拟机查看 io_thread elf-tool elf_vm show_iothread
                    未启用 iothread 的虚拟机，关闭 iothread （ elf-tool elf_vm disable_iothread ）成功
                    已启用 iothread 的虚拟机，关闭 iothread （ elf-tool elf_vm disable_iothread ）成功
                虚拟机 iothread 配置效果检查
                    检查 domian xml
                    所属主机检查虚拟机 qemu 进程检查
                io_thread 和磁盘绑定关系
                    集群 iothread.count 大于等于虚拟机 virtio 磁盘数量，虚拟机开机成功
                    集群 iothread.count 小于虚拟机 virtio 磁盘数量,  虚拟机开机成功
                    已启用 io_thread 且开机的虚拟机 - 删除同一个 iothread 分组（iothread1）的磁盘，删除成功
                    已启用 io_thread 且开机的虚拟机 - 删除不同 iothread 分组的磁盘，删除成功
                    已启用 io_thread 且开机的虚拟机，其中一个 iothread （ iothread1  ）没有磁盘的情况下，热添加磁盘成功
                io_thread 虚拟机迁移
                    SMTXOS 集群内迁移
                        已启用 io_thread 且开机的虚拟机， 集群内热迁移成功
                        已启用 io_thread 且关机的虚拟机， 集群内冷迁移成功， 目标主机上开机成功
                    SMTXELF 仅迁移计算
                        已启用 io_thread 且开机的虚拟机， 集群内热迁移成功
                        已启用 io_thread 且关机的虚拟机， 集群内冷迁移成功， 目标主机上开机成功
                    SMTXELF 仅迁移存储
                        已启用 io_thread 且开机的虚拟机， 集群内热迁移成功
                    OS-630 - OS-630
                        【源集群启用 iothread 2 个， 目标集群关闭 iothread】 虚拟机热迁移成功
                        【源集群启用 iothread 2 个， 目标集群启用 iothread 2 个】，虚拟机热迁移成功
                        【源集群启用 iothread 2 个， 目标集群启用 iothread 1 个】， 虚拟机热迁移成功
                        【源集群启用 iothread 2 个， 目标集群启用 iothread 3 个】，虚拟机热迁移成功
                        开启 iothread 虚拟机， 跨集群分段迁移后，目标虚拟机关闭 iothread
                        开启 iothread 虚拟机， 跨集群冷迁移后，目标虚拟机关闭 iothread
                    OS-630 - ELF - 630
                        【源集群启用 iothread 2 个， 目标集群关闭 iothread】 虚拟机热迁移成功
                        【源集群启用 iothread 2 个， 目标集群启用 iothread 2 个】，虚拟机热迁移成功
                        【源集群启用 iothread 2 个， 目标集群启用 iothread 1 个】， 虚拟机热迁移成功
                        【源集群启用 iothread 2 个， 目标集群启用 iothread 3 个】，虚拟机热迁移成功
                    ELF-630 - OS-630
                        【源集群启用 iothread 2 个， 目标集群关闭 iothread】 虚拟机热迁移成功
                        【源集群启用 iothread 2 个， 目标集群启用 iothread 2 个】，虚拟机热迁移成功
                        【源集群启用 iothread 2 个， 目标集群启用 iothread 1 个】， 虚拟机热迁移成功
                        【源集群启用 iothread 2 个， 目标集群启用 iothread 3 个】，虚拟机热迁移成功
                    ELF1-630 + ZBS1-570   - ELF2-630 + ZBS1-570 , 仅迁移计算
                        【源集群启用 iothread 2 个， 目标集群启用 iothread 2 个】，虚拟机热迁移成功
                    ELF1-630 + ZBS1-570   - ELF2-630 + ZBS2-570 , 迁移计算加存储
                        【源集群启用 iothread 2 个， 目标集群启用 iothread 2 个】，虚拟机热迁移成功
                io_thread 虚拟机开机
                    当前主机开机，检查开机后虚拟机系统正常
                    开机到指定主机， 检查开机后虚拟机系统正常
                虚拟机模版
                    关闭 iothread 的虚拟机克隆为模版， 模版不包含 iothread， 模版再创建虚拟机，新虚拟机 iothread 为关闭状态
                    开启 iothread 的虚拟机克隆为模版， 模版不包含 iothread， 模版再创建虚拟机，新虚拟机 iothread 为关闭状态
                    开启 iothread 的虚拟机转化为模版,  模版不包含 iothread， 模版再转化虚拟机， 新虚拟机 iothread 为关闭状态
                    关闭 iothread 的虚拟机克隆为模版， 模版不包含 iothread， 模版分发创建到其他集群，新虚拟机 iothread 为关闭状态
                虚拟机快照
                    创建普通快照， 快照不包含 iothread 配置
                    创建一致性快照， 快照不包含 iothread 配置
                    关闭 iothread 的虚拟机创建快照，快照重建虚拟机， 新虚拟机 iothread 为关闭状态
                    开启 iothread 的虚拟机创建快照，快照重建虚拟机， 新虚拟机 iothread 为关闭状态
                    开启 iothread 的虚拟机创建快照，源虚拟机修改 iothread 配置， 快照回滚， 源虚拟机 iothread 配置不变
                    不开启 iothread 的虚拟机创建快照，源虚拟机开启 iothread 配置， 快照回滚， 源虚拟机 iothread 配置不变
                ELF API
                    当前集群 io_thread
                        GET /api/v2/elf/cluster_iothread_capabilities
                    编辑集群 io_thread
                        集群有 cpu 独占虚拟机，编辑失败
                        关闭预留 {"reserved_count": 0}
                        编辑每个主机预留 pcpu 编辑成功， {"reserved_count": 2, "host": {"host_uuid1": [4,5], "host_uuid2": [6,7], "host_uuid3": [8,9]}}
                        增加 pcpu 数量，编辑成功
                        减少 pcpu 数量，编辑成功
                        不改变 pcpu 的数量，修改 pcpu 位置，编辑成功
                        优先挑选距离 zbs 服务更近的 pcpu，可以跨越 numa，若数量不够，job 失败
                        若节点开启了超线程，则挑选 pcpu 时，必须是非 sibling 关系。若数量不够，job 失败
                    vms_summary 对 pcpu 计算调整
                        GET /api/v2/compute/vms_summary 检查 available_exclusive_cpu 已经去掉 iothread_reserved_count 了
                    虚拟机 update_iothread
                        io_thread cluster_capabilities 的 reserved_count 非 0 时设置成功
                        io_thread cluster_capabilities 的 reserved_count 为 0 时设置失败
                ELF 命令行
                    elf-tool elf_cluster get_iothread_pcpu # 查看集群所有节点预留情况
                    elf-tool elf_cluster set_iothread_pcpu --count 2 # 配置每个节点预留 iothread pcpu 数量，count 可选参数，默认值为 2
                    elf-tool elf_cluster set_iothread_pcpu_on_host <host_uuid> <pcpu_list> # 配置指定节点, pcpu 绑定关系
                    vhost 集群执行 	elf-tool elf_cluster set_iothread_pcpu --count 2  返回  ELF_CLUSTER_BOOST_ENABLED
                定时任务
                    kvm_vm_guarantee_cpu_exclusive
                集群兼容性
                    需求兼容性
                        数据库， cluster_capabilities 增加 iothread_pcpu_reservation
                        api 检查 cluster_capabilities 返回数据增加 iothread_pcpu_reservation
                    集群类型兼容性
                        SMTXOS （ ELF ）boost （ 多 chunk 实例只能部署 boost 模式 ）集群设置  iothread 失败
                        SMTXOS （ ELF ）非 boost 集群设置  iothread 成功， 虚拟机设置  iothread 成功
                        SMTXELF 集群设置  iothread 成功， 虚拟机设置  iothread 成功
                        ACOS ( AVE )  集群设置  iothread 成功， 虚拟机设置  iothread 成功
                集群运维
                    新部署集群
                        630B89+ 新部署非 boost ，检查  cluster_capabilities 的 iothread_pcpu_reservation 已完成初始化（ 默认不开启 iothread ）
                        630B89+ 新部署 boost ，检查  cluster_capabilities 的 iothread_pcpu_reservation 已完成初始化（ 默认不开启 iothread ）
                    集群升级
                        630B 版本升级
                            630 的 B89 之前的版本升级到 B89+
                        低版本升级到 630
                            升级前数据准备
                                准备开机且 cpu 独占的虚拟机
                            升级后检查
                                cluster_capabilities 的 iothread_pcpu_reservation 已完成初始化， 初始 reserved_count = 0， host_allocations = {}
                                存量虚拟机包含开启独占的虚拟机， 集群启用 iothread 失败
                                存量虚拟机都没有开启独占（编辑取消独占）， 集群启用 iothread 成功
                                存量虚拟机启用 iothread
                    vhost 开关
                        非 boost 集群转化为 boost 集群
                        非 boost 集群转化为 boost 集群
                            转化前数据
                                集群启用 iothread
                                虚拟机启用 iothread
                                记录 vms_summary api 返回可独占的数量
                            转化后测试
                                集群为 iothread 预留的 pcpu 应该释放
                                cluster_capabilities 的 iothread_pcpu_reservation 数据保持不变。只是预留失效了。可以观察之前 vms_summary api 返回可独占的数量
                                存量开机开启 iothread 的虚拟机，iothread 相关配置应该失效
                                存量开机开启 iothread 的虚拟机，转化前已关机，转化后开机成功
                                存量关机开启 iothread 的虚拟机，开机成功
                                存量关机虚拟机，开启 iothread 失败 ELF_CLUSTER_BOOST_ENABLED
                                存量关机虚拟机，关闭 iothread 成功
                        boost 集群转化为非 boost 集群
                            转化前数据
                                准备开机关机虚拟机
                                cluster_capabilities 的 iothread_pcpu_reservation 数据是关闭的
                            转化后测试
                                cluster_capabilities 的 iothread_pcpu_reservation 数据保持不变， 保持关闭
                                集群开启 iothread 成功， 预留 pcpu 配置正确
                                存量关机虚拟机启用 iothread 成功
                        非 boost 集群，转化为 boost 集群，再转为非 boost
                            初始非 boost 集群检查
                                集群启用 iothread
                                开机虚拟机启用 iothread
                                记录 vms_summary api 返回可独占的数量
                            第一次转为 boost 集群
                                虚拟机开机配置独占，尝试让独占使用的 pcpu 是集群转化前 iothread 指定的 pcpu
                            第二次转为非 boost 集群
                                cluster_capabilities 的 iothread_pcpu_reservation 数据保持不变且生效。可以观察之前 vms_summary api 返回可独占的数量
                                第一次转化后的 cpu 独占虚拟机开机后独占生效，预期 pcpu  位置和【 iothread 指定的 cpu 】不一致
                    主机维护模式
                        集群开启 iothread， 虚拟机开启 iothread 后， 主机进入退出维护模式
            ELF-7956 支持 CDROM ISO 访问随机从一组 initiators 中选择 initiator
                smtxos630 - intel
                    上传和删除 iso
                        上传 iso 到某个集群，成功,allowed_initiator 值为 */*
                        上传 iso 到多个集群，成功
                        删除 iso， 成功
                        vmtools iso 上传，成功
                    iso 分发
                        内容库里的iso 已被虚拟机挂载，分发到同版本的其他集群后挂载给虚拟机，成功
                        内容库里的iso 已被虚拟机挂载，分发到低版本的其他集群后挂载给虚拟机，成功
                    虚拟机模版
                        虚拟机挂载iso后转化为模版，模版转化为虚拟机，开机后挂载 iso，成功，iso能正常使用
                        虚拟机挂载iso后克隆为模版，模版创建虚拟机，开机后挂载 iso，成功，iso能正常使用
                    挂载 iso
                        虚拟机有2个cdrom，给其中某个cdrom 挂载 iso，成功
                        虚拟机有4 个cdrom均挂载 iso，成功
                        虚拟机的 cdrom 挂载着 iso且开机状态，切换挂载不同的 iso
                        挂载了 iso 的虚拟机克隆多个虚拟机，开机访问 iso，成功
                        虚拟机关机状态挂载 iso，，成功；开机后虚拟机能正常使用iso
                        虚拟机开机状态挂载 iso，成功，虚拟机能正常使用 iso
                        移除 iso 后再挂载 iso，成功
                        挂载 vmtools 映像，成功
                        批量升级vmtools，成功
                        虚拟机有 4个cdrom，给空的cdrom挂载 iso，切换挂载不同的iso，移除 iso；另一个cdrom不挂载
                        虚拟机挂载 iso 后打快照，移除iso，关机-回滚快照，开机，成功，iso 能正常使用,iqn name 可能会变化
                        挂载iso后重启虚拟机，iso能正常使用
                        挂载 iso后禁用，修改为其他iso，再启用，虚拟机内iso正常使用
                        挂载 iso后热添加磁盘 virtio+ scsi，成功
                        挂载 iso 同时热添加磁盘 virtio+ scsi，成功
                        挂载 iso同时热删除磁盘 virtio+ scsi，成功
                        切换 iso、移除iso，同时热删除磁盘 virtio+ scsi，成功
                        给windows 虚拟机挂载 iso，成功
                    移除 iso
                        移除虚拟机的某个 iso，成功
                        移除虚拟机的多个 iso，成功
                        关机，删除虚拟机cdrom及挂载iso
                    虚拟机迁移
                        挂载了iso的虚拟机集群内迁移，成功
                        挂载了iso的虚拟机跨集群热迁移，成功
                        挂载了iso的虚拟机跨集群分段迁移，成功
                        挂载了iso的虚拟机跨集群冷迁移，成功
                    存量数据，集群升级场景
                        从smtxos 5.1.x 升到 smtxos 6.3.0，给存量虚拟机的 cdrom 挂载新iso，切换 iso，移除 iso
                        从smtxos 6.2.0 升到 smtxos 6.3.0，给存量虚拟机的 cdrom 挂载新iso，热添加磁盘，切换 iso热删除磁盘，移除 iso
                        虚拟机开机，原来挂载的 iso 都会自动配置 initiator
                smtxelf630 - oe
                    虚拟机关机状态挂载 iso，，成功；开机后虚拟机能正常使用iso
                    虚拟机开机状态挂载 iso，成功，虚拟机能正常使用 iso
                    移除 iso 后再挂载 iso，成功
                    虚拟机有 4个cdrom，给空的cdrom挂载 iso，切换挂载不同的iso，移除 iso；另一个cdrom不挂载
                smtxos630 - arm
                    虚拟机关机状态挂载 iso，，成功；开机后虚拟机能正常使用iso
                    虚拟机开机状态挂载 iso，成功，虚拟机能正常使用 iso
                    移除 iso 后再挂载 iso，成功
                    虚拟机有 4个cdrom，给空的cdrom挂载 iso，切换挂载不同的iso，移除 iso；另一个cdrom不挂载
            TOWER-20994 在界面提示用户：关闭防病毒后，将自动删除隔离区文件
                单个虚拟机启用防病毒弹窗，给出提示
                批量虚拟机启用防病毒弹窗，给出提示
                单个虚拟机关闭防病毒弹窗，给出提示
                批量虚拟机关闭防病毒弹窗，给出提示
                已开启防病毒的虚拟机，克隆虚拟机弹窗，给出提示
            ELF-7934 支持将指定的虚拟卷回滚到 zbs volume snapshot
                回滚当前卷的快照
                回滚其他卷的快照， 即指定 zbs_snapshot_uuid
            ELF-8180 调整 ELF 相关服务日志滚动策略
                elf 相关服务
                    有调整 usbredir-manager
                        case p1 日志正常记录
                        case p2 构造当前输出文件大小超过阈值
                        case p3 强制归档日志文件
                        case p3 归档日志命名检查
                        case p2 日志归档文件删除后日志记录正常
                    有调整 vnc-proxy
                        case p1 日志正常记录
                        case p2 构造当前输出文件大小超过阈值
                        case p3 强制归档日志文件
                        case p3 归档日志命名检查
                        case p2 日志归档文件删除后日志记录正常
                    有调整 elf-fs
                        case p1 日志正常记录
                        case p2 构造当前输出文件大小超过阈值
                        case p3 强制归档日志文件
                        case p3 归档日志命名检查
                        case p2 日志归档文件删除后日志记录正常
                    有调整 vm-security-controller
                        case p1 日志正常记录
                        case p2 日志文件删除后日志记录正常
                        case p2 构造当前输出文件大小超过阈值
                        case p3 强制归档日志文件
                        case p3 归档日志命名检查
                        case p2 日志归档文件删除后日志记录正常
                    不用调整也满足 elf-vm-scheduler、elf-dhcp、elf-vm-watchdog、elf-exporter、elf-rest-server、vmtools-agent、virtlogd，抽查elf-rest-server
                        case p1 日志正常记录
                        case p2 构造当前输出文件大小超过阈值
                        case p3 强制归档日志文件
                        case p3 归档日志命名检查
                        case p2 日志归档文件删除后日志记录正常
                    有调整 elf-vm-monitor
                        case p1 日志正常记录
                        case p2 构造当前输出文件大小超过阈值
                        case p3 强制归档日志文件
                        case p3 归档日志命名检查
                        case p2 日志归档文件删除后日志记录正常
                    部分调整，依赖 TUNA 日志滚动前置检查 libvirtd
                        case p1 日志正常记录
                        case p2 构造当前输出文件大小超过阈值
                        case p3 强制归档日志文件
                        case p3 归档日志命名检查
                        case p2 日志归档文件删除后日志记录正常
                    其它检查
                        case p2 日志配置文件
                        case p2 测试形态
                        case p2 日志过期清理机制
                        case p3 根分区可用空间小于1G
                        case p3 升级场景
    SMTXELF
        SMTXELF 6.2.0 + Tower 4.6.0
            SMTX ELF 620 支持关联 SMTX OS 集群【Tower 4.6.0】
                虚拟机资源管理
                    克隆虚拟机
                        克隆创建虚拟机 - 挂载 ISO - 创建成功，ISO 挂载正常
                OVF 导入导出
                    取消导出虚拟机、虚拟卷
                    取消导入虚拟机、虚拟卷
                内容库
                    虚拟机模板
                        SMTX OS 集群创建的虚拟机模板，分发到其他被 SMTX ELF 关联的 SMTX OS/ZBS 集群，取消分发，取消成功
                        分发不同 CPU 架构虚拟机模板到被 SMTX ELF 关联的不同 CPU 架构 SMTX OS 集群（已知问题TOWER-17902）
                    ISO
                        基于 NFS 文件的 ISO（SMTX OS < 6.2.0）
                            SMTX ELF 关联 SMTX OS 存储集群前上传到 SMTX OS 集群的 ISO
                                SMTX OS 集群的 ISO，分发到其他被 SMTX ELF 关联的 SMTX OS/ZBS 集群，取消分发，取消成功
                        基于 iSCSI Lun 的 ISO（SMTX OS >= 6.2.0）
                            SMTX ELF 关联 SMTX OS 存储集群前上传到 SMTX OS 集群的 ISO
                                SMTX OS 集群的 ISO，分发到其他被 SMTX ELF 关联的 SMTX OS/ZBS 集群，取消分发，取消成功
        专项测试 - 故障场景
            SMTXZBS 故障
                主机故障
                    ZBS 集群 meta leader 主机关机， 检查 SMTXELF 虚拟机保持稳定运行， 没有 io 中断
                    ZBS 集接入 vip leader 主机关机， 检查 SMTXELF 虚拟机保持稳定运行， 没有 io 中断
                    ZBS 集群 meta leader 且接入  vip leader 主机关机， 检查 SMTXELF 虚拟机保持稳定运行， 没有 io 中断
        6.3.0
            【回归测试】SMTXELF 迁移网络回归
                迁移网络
                    SMTXELF 配置迁移网络
                集群内热迁移（仅迁移计算）
                    配置迁移网络的情况下， 集群内迁移优先走迁移网络迁移数据
                    不配置迁移网络的情况下， 集群内迁移走存储接入网络迁移数据
                仅迁移存储
                    配置迁移网络的情况下， 仅迁移存储检查实际使用的网路是存储接入网络
                跨集群仅迁移计算
                    配置迁移网络的情况下， 集群内迁移优先走迁移网络迁移数据
                    不配置迁移网络的情况下， 集群内迁移走存储网络迁移数据
                跨集群迁移计算加存储
                    配置迁移网络的情况下， 集群内迁移优先走迁移网络迁移数据
                    不配置迁移网络的情况下， 集群内迁移走存储网络迁移数据
    SMTX ZBS
        SMTXELF 关联 ZBS
            关联集群
                SMTX ELF 关联 SMTX ZBS 集群
            虚拟机
                创建虚拟机选择存储集群为当前 SMTXZBS
                虚拟机克隆时不允许更换存储集群，克隆弹窗展示存储集群名称
                虚拟机仅迁移存储，迁移到其他存储，在迁移到当前存储，迁移成功
                虚拟机所属存储为当前 SMTXZBS 集群， OVF 导出成功，导入时选择当前 ZBS 集群，导入成功
                虚拟机 HA 成功
            内容库
                模版
                    虚拟机所属存储为当前 SMTXZBS 集群， 克隆为模版，克隆弹窗默认存储集群为当前 ZBS 集群
                    虚拟机所属存储为当前 SMTXZBS 集群， 转化为模版，转化弹窗默认存储集群为当前 ZBS 集群
                    内容库模版创建（克隆）虚拟机，新虚拟机存储集群选择当前 ZBS 集群，创建成功
                    内容库模版转化为虚拟机，转化弹窗存储集群选择当前 ZBS 集群，转化成功
                    内容库模版初始不包含当前 ZBS 集群，编辑所属集群添加当前 ZBS 集群
                    内容库模版初始包含当前 ZBS 集群，编辑所属集群添加其他 ZBS 集群，然后删除当前 ZBS 集群， 2 次编辑都成功
                    内容库模版 OVF 导出成功
                    内容库模版 OVF 导入，选择当前 ZBS 集群，导入成功
                ISO
                    ISO 本地文件上传到 ZBS 集群
                    ISO URL 上传到 ZBS 集群
                    其他集群 ISO 编辑所属集群 - 增加当前 ZBS 集群
                    当前 ZBS 集群 ISO 编辑所属集群 - 增加其他集群， 删除当前 ZBS 集群，2 次编辑成功
            快照
                普通快照
                    虚拟机关联存储集群，创建普通快照成功，快照重建和回滚正常
                一致性快照
                    虚拟机关联存储集群，创建一致性快照成功，快照重建和回滚正常
                快照计划
                    虚拟机关联存储集群，创建快照计划成功，快照计划执行成功
            升级场景
                ZBS 集群升级期间，虚拟机 io 预期不发生中断
    Tower
        ELF Tower UI 集成测试
            不同配置的虚拟机
                VMTools ISO 挂载方式
                    Disk-CDROM 载入 VMTools ISO
                    USB 载入 VMTools ISO
        Tower 内容库
            Tower 内容库 - 虚拟机模板
                模板应用
                    特殊场景记录
                        case 1119434 关联-- fisheye 挂载的vmtools  cd-rom 虚拟机 - 克隆转化为模版后 - tower 内容库 分发到其他集群成功
        Tower 发布前 ELF 回归测试
            内容库
                ISO
                    并发 - 编辑 ISO 所属集群分发、模版创建vm -分发有进度时 -  取消编辑 ISO 所属集群 - 所有任务取消分发成功【tower 460】
                模板
                    并发 - 编辑 ISO 所属集群分发、模版创建vm -分发有进度时 -  取消编辑 ISO 所属集群 - 所有任务取消分发成功【tower460】
                    smtx os1 的UEFI 虚拟机 - 克隆创建模版并分发到os2、zbs1  - 检查模版有nvram 文件 - 后续 os_01、os_02、elf+os_01、elf+zbs_01 模版创建 vm 有 nvram 能正常进入操作系统
                    smtx elf+zbs 的UEFI 虚拟机 - 转化创建模版并分发到os1、os2  - 检查模版有nvram 文件 - 后续 os_01、os_02、elf+os_01、elf+zbs_01 模版创建 vm 有 nvram 能正常进入操作系统
            虚拟机
                迁移
                    （610 及以上集群 elf）跨集群 - smtx elf 与os 迁移存储+存储：smtx elf1.os1  to smtx os - 迁移成功【460开始支持elf+os】
                快照
                    快照管理页面 - 修改快找名称、描述 成功，删除快找成功
                虚拟机组
                    tower 视图选项从 主机视图 ---> 切换为虚拟机组试图 - 切换成功
                    操作虚拟机组：创建、编辑、移动层级 - 操作成功
            虚拟卷
                操作克隆创建开启加密、ec 策略、常驻缓存的虚拟卷 - 创建成功
            集群存储策略
                tower 关联 os 集群 - 设置存储策略：开启加密的 ec 厚制备 - 关联集群成功，默认存储策略设置成功，事件记录正确
                tower smtx elf关联  集群 - 设置存储策略：开启加密的 3副本 精简制 备 zbs 集群 - 关联存储成功，默认存储策略设置成功，事件记录正确
            回收站
                回收站设置集群回收天数成功 - 删除 vm 后 vm 不再集群虚拟机列表展示，查看回收站 vm 剩余天数正确，回收站删除 vm 成功
                集群未开启回收站 - 永久删除虚拟机，删除成功，不进回收站
                开启虚拟卷回收站 - os 集群删除虚拟卷，删除成功，不进回收站
        4.6.0
            跨集群热迁移限速【tower460】-2025-03-31 取消
                UI 检查
                    跨集群热迁移：先后选热迁移启用带宽限制 - 变更为分段迁移，会清空"启用带宽限制"的勾选
                    跨集群热迁移：分段迁移选项下，如果直接点击「启用带宽限制」将自动切换至「热迁移选项」
                功能测试
                    虚拟机不同配置覆盖
                        含单块有数据虚拟机卷的虚拟机 - 热迁移限速正确
                        含多块有数据虚拟机卷的虚拟机 - 热迁移限速正确
                        配置 cpu qos、ec 卷、副本卷、常驻缓存卷、加密卷、vpc、pci、sr-iov 网卡的虚拟机 - 热迁移限速正确
                        windows bios  虚拟机限速正常
                        windows UEFI  虚拟机限速正常
                        linux bios  虚拟机限速正常
                        linux uefi  虚拟机限速正常
                迁移有效性检查
                    在迁移期间虚拟机内部跑磁盘 IO：fio，预期整个周期 io 正常
                    在迁移期间虚拟机网络正常：iperf3 ，网络可以持续检测
                    进行迁移一致性进行检查：使用 palantir 校验数据一致性 - 主机默认开启
                    tower server 触发限速为0（UI不可触发） - 检查迁移限速：预期实际迁移为不限速，事件记录为不限速
            异步长任务虚拟机、卷、模板导出 & 模板、ISO 分支 - 持手动取消
                回归测试
                    ovf 导入
                        导入虚拟机 时 - 取消导入成功
                        导入虚拟机模板 时 - 取消导入成功
                        导入虚拟卷 时 - 取消导入成功
                    跨集群热迁移
                        跨集群热迁移虚拟机 - 取消迁移成功
                ovf 资源导出
                    导出虚拟机含mac 地址 - 取消导出 - 取消成功
                    导出虚拟机不含mac 地址 - 取消导出 - 取消成功
                    导出普通虚拟机模板 - 取消导出 - 取消成功
                    导出cloud-init 虚拟机模板 - 取消导出 - 取消成功
                    导出虚拟卷 VMDK 模式 - 取消导出 - 取消成功
                    导出虚拟卷 QCOW2 模式 - 取消导出 - 取消成功
                    导出虚拟卷 RAW 模式 - 取消导出 - 取消成功
                    取消导出的模板，重新导出后，重新导入能正常使用
                    取消导出的虚拟机，重新导出后，重新导入能正常使用
                    取消导出的虚拟卷，重新导出后，重新导入能正常使用
                    取消ovf 导入导出任务的elf 残留数据 - 检查有每10min的定时任务清理
                内容库资源分发取消
                    ISO
                        各方式创建 vm 挂载 iso
                            创建空白
                                smtx os 创建虚拟机 - 挂载分发其他 smtx os 的 iso  - 取消成功
                                smtx os 创建虚拟机 - 挂载分发其他 smtx elf + zbs 的 iso  - 取消成功
                                smtx elf +zbs 创建虚拟机 - 挂载分发其他 smtx os 的 iso  - 取消成功
                                smtx elf + zbs 创建虚拟机 - 挂载分发其他 smtx elf + zbs 的 iso  - 取消成功
                            克隆创建
                                smtx os 克隆含 iso 的vm - 更换挂载分发其他 smtx os 的 iso 创建虚拟机 - 取消成功
                                smtx os 克隆不含 iso 的vm创建虚拟机 - 挂载分发其他 smtx elf + zbs 的 iso 创建虚拟机  - 取消成功
                                smtx elf +zbs  克隆含 iso 的vm - 更换挂载分发其他 smtx os 的 iso 创建虚拟机 - 取消成功
                                smtx elf +zbs 克隆不含 iso 的vm创建虚拟机 - 挂载分发其他 smtx elf + zbs 的 iso 创建虚拟机  - 取消成功
                            快照重建
                                smtx os 快照重建新增 cd-rom  重建vm - 挂载分发其他 smtx os 的 iso 创建虚拟机  - 取消成功smtx os
                                smtx os 快照重建新增 cd-rom 创建虚拟机 - 挂载分发其他 smtx elf + zbs 的 iso 创建虚拟机   - 取消成功
                                smtx elf +zbs 快照重建新增 cd-rom创建vm - 挂载分发其他 smtx os 的 iso 创建虚拟机  - 取消成功
                                smtx elf +zbs 快照重建新增 cd-rom 创建虚拟机 - 挂载分发其他 smtx elf + zbs 的 iso 创建虚拟机 - 取消成功
                            模板分发
                                路径2：内容库模板创建vm
                                    smtx os 虚拟机模板挂载 1个 iso - 创建虚拟机到 smtx os 集群 - 在分发 iso 阶段取消 - 取消成功
                                    smtx os 虚拟机模板挂载4个 iso - 创建虚拟机到 smtx  elf + os 集群 - 在分发 3个 iso 成功后 - 取消成功成功 - 已分发的模板、iso 可正常使用
                                    smtx zbs 虚拟机模板挂载4个 iso - 创建虚拟机到 smtx  elf + zbs 集群 - 在分发 3个 iso 成功后 - 取消成功成功 - 已分发的模板、iso 可正常使用
                                路径1：内容库单独分发 iso
                                    smtx os 集群内容库 ISO  - 编辑所属集群：分发到其他集群 smtxos\smtx zbs - 取消分发成功
                                    smtx zbs 集群内容库 ISO  - 编辑所属集群：分发到其他集群 smtxos\smtx zbs - 取消分发成功
                                    smtx os 取消分发的 iso - 正常分发，能正常识别使用
                                    smtx zbs 取消分发的 iso - 正常分发，能正常识别使用
                            ovf 导入虚拟机挂载iso
                                ovf 导入虚拟机  - 挂载多个从其他集群分发的 iso - 分发 1个成功后，取消分发 - 取消成功，已分发 iso 可正常使用
                                ovf 导入虚拟机  - 挂载多个从其他集群分发的 iso - 分发第一个 iso 取消分发 - 取消成功
                        编辑vm
                            开机vm - smtx os 编辑未挂载iso 的 cd - rom - 挂载分发其他 smtx os 的 iso  - 取消成功
                            开机vm - smtx os  编辑挂载iso 的 cd - rom - 更换 iso 挂载分发其他 smtx elf + zbs 的 iso  - 取消成功
                            关机vm - smtx elf +zbs 编辑未挂载iso 的 cd - rom - 挂载分发其他 smtx os 的 iso  - 取消成功
                            关机vm - smtx elf + zbs 编辑挂载iso 的 cd - rom - 更换 iso 挂载分发其他 smtx elf + zbs 的 iso  - 取消成功
                    虚拟机模板
                        路径2：集群使用内容库模板创建vm
                            smtx os 虚拟机模板 - 创建虚拟机到 smtx os 集群 -  在分发模板阶段取消 - 取消成功
                            smtx elf + zbs 虚拟机模板 - 创建虚拟机到 smtx elf + os 集群 -在分发模板阶段取消 - 取消成功
                            smtx elf + zbs 的虚拟机模板 - 创建虚拟机到 smtx elf + zbs  集群 - 在分发模板阶段取消 - 取消成功
                        路径3：虚拟机克隆为模板分发多个集群
                            smtx os 虚拟机 - 克隆创建虚拟机模板到 多个集群 smtx os + smtx zbs  - 在分发模板阶段取消 - 取消成功:本集群模板创建成功，其他集群模板分发中断
                            smtx zbs 虚拟机 - 克隆创建虚拟机模板到 多个集群 smtx os + smtx zbs  - 在分发模板阶段（1个其他集群B分发成功）后取消 - 取消成功:本集群A、其他集群B模板创建成功，剩余集群模板分发中断
                        路径4：虚拟机转化为模板分发多个集群
                            smtx os 虚拟机 - 转化为虚拟机模板到 多个集群 smtx os + smtx zbs  - 在分发模板阶段（1个其他集群B分发成功）后取消 - 取消成功:本集群A、其他集群B模板创建成功，剩余集群模板分发中断
                            smtx zbs 虚拟机 - 转化为虚拟机模板到 多个集群 smtx os + smtx zbs  - 在分发模板阶段取消 - 取消成功:本集群模板创建成功，其他集群模板分发中断
                        路径1：内容库单独分发 模板
                            smtx os 集群内容库 cloud-init 模板  - 编辑所属集群：分发到其他集群 smtxos\smtx zbs - 分发模板时，取消分发成功：所有集群都没分发到模板
                            smtx zbs 集群内容库模板  - 编辑所属集群：分发到其他集群 smtxos\smtx zbs - 分发1个集群成功后 - 取消分发成功：已分发集群可正常使用
                            smtx os 取消分发的 模板 - 正常分发，能正常识别使用
                            smtx zbs 取消分发的 模板 - 正常分发，能正常识别使用
                    取消分发后数据清理检查
                        取消iso 分发后  - 检查无残留：iso 所属集群不包含取消分发的目标集群
                        取消 模板 分发后  - 检查无残留：iso 所属集群不包含取消分发的目标集群
                不同进度取消任务
                    ovf 导出虚拟机 - 迁移任务进行中，取消迁移任务 - 取消成功
                    进行不同导出进度取消迁移的虚拟机 - 重新导出后导入集群，能正常识别使用 - 残留数据定时任务清理
                    ovf 导出虚拟卷 - 迁移任务进行中，取消迁移任务 - 取消成功
                    进行不同导出进度取消迁移的虚拟卷 - 重新导出后导入集群，能正常识别使用 - 残留数据定时任务清理
                    ovf 导出虚拟机模板 - 迁移迁移任务进行中，取消迁移任务 - 取消成功
                    进行不同导出进度取消迁移的虚拟机模板 - 重新导出后导入集群，能正常识别使用 - 残留数据定时任务清理
                    检查从模板创建 vm 分发模板阶段：正在初始化 - 分发中 - 即将完成分发
                    检查编辑模板所属集群 - 分发模板阶段：正在初始化 - 分发中 - 即将完成分发
                    内容库 模板 分发 - 正在初始化阶段 - 无取消任务入口
                    内容库 模板 分发 - 分发中 - 有取消任务入口，可正常取消
                    内容库 模板 分发 - 即将完成 - 无取消任务入口
                    内容库 - 分发模板初始化 ~ 分发中边界，取消任务 - 取消成功
                    内容库 - 分发模板  50% 左右取消任务 - 取消成功
                    内容库 - 分发模板 100% ~ 分发完成边界，取消任务 - 取消成功
                    内容库 - 进行不同分发进度取消迁移的虚拟机模板 - 重新分发后，能正常识别使用 -检查无残留数据
                    检查创建虚拟机挂载 iso 分发阶段：正在初始化 - 分发中 - 即将完成分发
                    检查编辑 iso所属集群分发阶段：正在初始化 - 分发中 - 即将完成分发
                    内容库 iso 分发 - 正在初始化阶段 - 无取消任务入口
                    内容库 iso 分发 - 分发中 - 有取消任务入口，可正常取消
                    内容库 iso 分发 - 即将完成 - 无取消任务入口
                    内容库 - 分发 iso 初始化 ~ 分发中边界，取消任务 - 取消成功
                    内容库 - 分发 iso  50% 左右取消任务 - 取消成功
                    内容库 - 分发 iso 100% ~ 分发完成边界，取消任务 - 取消成功
                    内容库 - 进行不同分发进度取消迁移的iso  - 重新分发后，能正常识别使用 -检查无残留数据
                    编辑iso 所属集群- 分发的 iso 到不同集群 - 出现不同原因（api 超时）分发失败及手动触发的失败 - 分发详情能正确展示
                多任务操作
                    取消资源分发时的提示检查
                        检查 - 中文 - 提示语符合预期
                        检查 - 英文 - 提示语符合预期
                        模板
                            场景一：含编辑模板所属集群的并发任务
                                取消 - 编辑模板所属集群 任务，预期提示：集群os_01 、集群os_02、smtxelf+zbs、smtx_os_01模板批量的 10个vm 取消
                                取消 - 模板批量创建10个vm 到集群os_02，预期提示：集群 os_02：编辑模板所属集群会被取消；集群 os_01：os_01、elf+os_01 创建vm、编辑模板所属集群会被取消；smtx+zbs 模板批量的 10个vm 会被取消；集群 os_03：编辑模板所属集群分发会被取消
                                取消 - 模板批量创建10个vm 到集群os_01，预期提示：集群 os_01：smtelf+os_01 批量创建vm（os_01批量创建的当前这个1个任务会取消，但不在提示语提示）会被取消、编辑模板所属集群会被取消；集群 os_02：os_02 创建vm、编辑模板所属集群会被取消；smtx+zbs 模板批量的 10个vm 会被取消；集群 os_03：编辑模板所属集群分发会被取消
                                取消 - 模板批量创建10个vm 到集群 smtx elf+os_01，预期提示：集群 os_01：os_01批量创建、smtelf+os_01 批量创建9个vm 会被取消、编辑模板所属集群会被取消；集群 os_02：os_02 创建vm、编辑模板所属集群会被取消；smtx+zbs 模板批量的 10个vm 会被取消；集群 os_03：编辑模板所属集群分发会被取消
                                取消 - 模板批量创建10个vm 到集群smxtefl+zbs，预期提示：集群 os_01：os_01批量创建、smtelf+os_01 批量创建10个vm 会被取消、编辑模板所属集群会被取消；集群 os_02：os_02 创建vm、编辑模板所属集群会被取消；集群 os_03：编辑模板所属集群分发会被取消
                                先进行 创建vm 分发模板操作，后进行编辑模板所属集群操作 - 检查 创建、编辑模板所属集群取消时，都是取消所有使用该资源的任务
                                先进行编辑模板所属集群操作，后进行 创建vm 分发模板操作 - 检查 创建、编辑模板所属集群是取消时，都是取消所有使用该资源的任务
                                编辑模板所属集群分发到 集群os_01、os_02、os_03、smtxelf+zbs、smtx_os_01，同时集群os_01、os_02、os_04、smelf+os_05、smtxelf+zbs、smtx_os_01 从该模板创建虚拟机 - 取消 os_04、smtxelf+os_05 模版创建任务 - 不影响其他任务执行
                            场景二：不含编辑模板所属集群的并发任务
                                取消 - 模板批量创建10个vm 到集群os_02，预期 （ os_02 批量创建的当前这1个任务会取消，但不再提示语提示），集群 os_01、smtxelf+os_01、smtx+zbs 模板批量的 10个vm 成功
                                取消 - 模板批量创建10个vm 到集群os_01，预期提示：集群smtelf+os_01 模板创建vm 会被取消（ os_01 批量创建的当前这1个任务会取消，但不再提示语提示），集群 os_02、smtx+zbs 模板批量的 10个vm 成功
                                取消 - 模板批量创建10个vm 到集群smxtefl+os_01，预期提示：集群 os_01、smtxelf+os_01 模板批量的 10个vm 会被取消，集群 os_02、smtx elf+zbs 模板批量的 10个vm 成功
                                取消 - 模板批量创建10个vm 到集群smxtefl+zbs，预期提示：集群 smtxelf+zbs 会被取消，集群 os_01、os_02、smtx elfos_01 模板批量的 10个vm 成功
                        ISO
                            场景一：含编辑 ISO 所属集群的并发任务
                                挂载单个 iso
                                    先进行 创建vm 分发模板操作，后进行编辑模板所属集群操作 - 检查 创建、编辑模板所属集群取消时，都是取消所有使用该资源的任务
                                    先进行编辑模板所属集群操作，后进行 创建vm 分发模板操作 - 检查 创建、编辑模板所属集群是取消时，都是取消所有使用该资源的任务
                                    取消 - 编辑 ISO 所属集群分发任务，预期提示：集群os_01、os_02、smtxelf+zbs、smtxelf+os_01 模板批量的 10个vm 、克隆批量的 10个vm 、快照重建vm、ovf 导入vm、编辑 vm 任务取消
                                    取消 - 集群 smtos_02 从该模板创建10 vm  挂载分发 iso，预期提示：集群 smtxos_02 的 ISO 分发克隆批量的 10个vm 、快照重建vm、ovf 导入vm、编辑 vm 任务都被取消，集群os_01、smtxelf+os_01、smtxelf+zbs 创建挂载任务取消，集群os_03分发取消
                                    取消 - 集群os_01 从该模板创建10 vm  挂载分发 iso，预期提示：集群 os_01、smtxelf+os_01的 ISO 分发克隆批量的 10个vm 、快照重建vm、ovf 导入vm、编辑 vm 任务都被取消，集群os_02、smtx elf+zbs分发、创建挂载任务取消，集群os_03分发取消
                                    取消 - 集群os_01 克隆批量创建10 vm 挂载分发 iso ，预期提示：集群os_01、smtxelf+os_01 的 ISO 分发、模板批量的 10个vm 、快照重建vm、ovf 导入vm、编辑 vm 任务都被取消，集群os_02、smtxelf+zbs 分发、创建挂载任务取消，集群os_03分发取消
                                    取消 - 集群os_01 快照重建vm挂载分发 iso ，预期提示：集群os_01、smtxelf+os_01的 ISO 分发、模板批量的 10个vm 、克隆批量创建10个 vm、ovf 导入vm、编辑 vm 任务都被取消，集群os_02、smtxelf+zbs 分发、创建挂载任务取消，集群os_03分发取消
                                    取消 - 集群 os_01 ovf 导入vm 挂载分发 iso ，预期提示：集群 os_01、smtxelf+os_01的 ISO 分发、模板批量的 10个vm 、克隆批量创建10个 vm、快照重建 vm、编辑vm 任务都被取消，集群os_02、smtxelf+zbs分发、创建挂载任务取消，集群os_03分发取消
                                    取消 - 集群os_01 编辑 vm  挂载分发 iso ，预期提示：集群 os_01、smtxelf+os_01 的 ISO 分发、模板批量的 10个vm 、克隆批量创建10个 vm、快照重建 vm、ovf 导入 vm 任务都被取消，集群os_02、smtxelf+zbs 分发、创建挂载任务取消，集群os_03分发取消
                                    取消 - 集群 smtxelf+os_01 从该模板创建10 vm  挂载分发 iso，预期提示：集群 os_01、smtxelf+os_01的 ISO 分发克隆批量的 10个vm 、快照重建vm、ovf 导入vm、编辑 vm 任务都被取消，集群os_02、smtx elf+zbs分发、创建挂载任务取消，集群os_03分发取消
                                    取消 - 集群 smtxelf+zbs 克隆批量创建10 vm 挂载分发 iso ，预期提示：集群 smtxelf+zbs 的 ISO 分发、模板批量的 10个vm 、快照重建vm、ovf 导入vm、编辑 vm 任务都被取消，集群os_01、smtxelf+os_01、os_02 分发、创建挂载任务取消，集群os_03分发取消
                                挂在多个 iso
                                    编辑iso_01~04 所属集群到os_01、os_02、0s_03、zbs ，os_01、os_02、smtxelf+os_01、smtxelf+zbs虚拟机创建时挂载不同 iso（但包含iso_02）- 取消 iso_02 分发 - os_01、os_02、smtxelf+os_01、smtxelf+zbs 的虚拟机创建任务取消，所有的创建vm动作失败， iso2 分发取消，其他iso 编辑所属集群正常成功
                                    编辑iso_01~04 所属集群到os_01、os_02、0s_03、zbs ，os_01、smtxelf+os_01、smtxelf+zbs虚拟机创建时挂载不同 iso（但不包含iso_02）- 取消 iso_02 分发 - os_01、smtxelf+os_01、smtxelf+zbs 的虚拟机创建任务取消，所有 iso 分发正常成功，所有的创建vm正常成功
                            场景二：不含编辑 ISO 所属集群的并发任务
                                挂载单个 iso
                                    取消 - 集群 smtos_02 从该模板创建10 vm  挂载分发 iso，预期提示：集群 smtxos_02 的 克隆批量的 10个vm 、快照重建vm、ovf 导入vm、编辑 vm 任务都被取消，集群os_01、smtxelf+os_01、smtxelf+zbs 创建挂载任务正常成功，集群os_03分发正常成功
                                    取消 - 集群 smtxelf+os_01 从该模板创建10 vm  挂载分发 iso，预期提示：集群 os_01、smtxelf+os_01的 克隆批量的 10个vm 、快照重建vm、ovf 导入vm、编辑 vm 任务都被取消，集群os_02、smtx elf+zbs分发、创建挂载任务正常成功，集群os_03分发正常成功
                                    取消 - 集群smtx elf+os_01 克隆批量创建10 vm 挂载分发 iso ，预期提示：集群os_01、smtxelf+os_01 的 模板批量的 10个vm 、快照重建vm、ovf 导入vm、编辑 vm 任务都被取消，集群os_02、smtxelf+zbs 分发、创建挂载任务正常成功，集群os_03分发正常成功
                                    取消 - 集群smtx elf+os_01 快照重建vm挂载分发 iso ，预期提示：集群os_01、smtxelf+os_01的 模板批量的 10个vm 、克隆批量创建10个 vm、ovf 导入vm、编辑 vm 任务都被取消，集群os_02、smtxelf+zbs 分发、创建挂载任务正常成功，集群os_03分发正常成功
                                    取消 - 集群 smtxelf+os_01 ovf 导入vm 挂载分发 iso ，预期提示：集群 os_01、smtxelf+os_01的模板批量的 10个vm 、克隆批量创建10个 vm、快照重建 vm、编辑vm 任务都被取消，集群os_02、smtxelf+zbs分发、创建挂载任务正常成功，集群os_03分发正常成功
                                    取消 - 集群 smtxelf+os_01 编辑 vm  挂载分发 iso ，预期提示：集群 os_01、smtxelf+os_01 的 模板批量的 10个vm 、克隆批量创建10个 vm、快照重建 vm、ovf 导入 vm 任务都被取消，集群os_02、smtxelf+zbs 分发、创建挂载任务取消，集群os_03分发取消
                                    取消 - 集群 smtxos_01 编辑 vm  挂载分发 iso，预期提示：集群 os_01、smtxelf+os_01的 ISO 分发模板创建、克隆批量的 10个vm 、快照重建vm、ovf 导入vm、都被取消，集群os_02、smtx elf+zbs分发、创建挂载任务正常成功，集群os_03分发正常成功
                                    取消 - 集群 smtxelf+zbs 模板批量创建10 vm 挂载分发 iso ，预期提示：集群 smtxelf+zbs 的 克隆批量的 10个vm 、快照重建vm、ovf 导入vm、编辑 vm 任务都被取消，集群os_01、smtxelf+os_01、os_02 分发、创建挂载任务正常成功，集群os_03分发正常成功
                                挂在多个 iso
                                    虚拟机创建时os_01、os_02挂载 iso_01\02\05\06、smtxelf+os_01、smtxelf+zbs挂载挂载 iso_03\04\05\06 - 取消 os_01 创建 - 所有集群的创建vm动作终止创建失败
                                    虚拟机创建时os_01、os_02挂载 iso_01\02、smtxelf+os_01、smtxelf+zbs挂载挂载 iso_03\04 - 取消 os_01 创建 - os_01\os_02集群的创建vm动作终止创建失败，smtxelf+os_01、smtxelf+zbs 创建vm 成功
                                    虚拟机创建时os_01、smtxelf+os_01挂载 iso_01\02，os_02、smtxelf+zbs挂载挂载 iso_03\04 - 取消 smtxelf+os_01 创建 - os_01、smtxelf+os_01 集群的创建vm动作终止创建失败，os_02、smtxelf+zbs 创建vm 成功
                                    虚拟机创建时os_01、smtxelf+os_01挂载 iso_01\02，os_02、smtxelf+zbs挂载挂载 iso_03\04 - 取消 smtxelf+zbs 创建 - os_02、smtxelf+zbs 集群的创建vm动作终止创建失败，os_01、smtxelf+os_01 创建vm 成功
                    多任务操作
                        取消单个异步任务 - 取消成功
                        短时间操作取消多个(5个及以上)异步任务- 取消成功
                        克隆源 vm  - 创建虚拟机分发4个iso - 分发3个 iso 后，取消任务 成功，已分发的3个iso正常使用
                        克隆源 vm 挂载iso  - 批量10个创建虚拟机更新分发4个iso - 分发3个 iso 后，取消任务成功，已分发的3个iso正常使用
                        克隆源 vm 未挂载 - 批量10个创建虚拟机分发1个iso - 取消其中一个任务 - 同时取消批量创建所有任务
                        克隆源 vm 挂载 - 批量10个创建虚拟机更新分发1个iso - 取消其中一个任务 - 同时取消批量创建所有任务
                        克隆源 vm 未挂载 - 批量10个创建虚拟机分发4个iso - 分发3个 iso 后，取消其中一个任务 - 同时取消批量创建所有任务，已分发的3个iso正常使用
                        克隆源 vm 挂载 iso - 批量10个创建虚拟机更新分发4个iso - 分发3个 iso 后，取消其中一个任务 - 同时取消批量创建所有任务，已分发的3个iso正常使用
                        分发模板，批量10个创建虚拟机分发1个iso - 分发模板阶段，取消 - 会同时取消批量创建所有vm（任务记录单个，事件记录多个）
                        分发模板，批量10个创建虚拟机分发4个iso - 在分发模板阶段，取消其中一个任务 - 同时取消批量创建所有vm（任务记录单个，事件记录多个）
                        分发模板，批量10个创建虚拟机分发1个iso - 分发iso 时，取消 - 同时取消批量创建所有vm（任务记录单个，事件记录多个），已分发的模板能正常使用
                        分发模板，批量10个创建虚拟机分发4个iso - 分发3个 iso 后，取消 - 同时取消批量创建所有vm（任务记录单个，事件记录多个），已分发的模板和3个iso正常使用
                        编辑虚关机拟机挂载4个 iso  - 分发3个iso 后 - 取消分发任务成功 - 虚拟机是未挂载 ，已分发的3个 iso 可在集群使用
                        编辑虚关机拟机更新挂载4个 iso  - 分发3个iso 后 - 取消分发任务成功 - 虚拟机是原始iso  ，已分发的3个 iso 可在集群使用
                        编辑虚开机机拟机挂载4个 iso  - 分发3个iso 后 - 取消分发任务成功 - 虚拟机是未挂载 ，已分发的3个 iso 可在集群使用
                        编辑虚开机拟机更新挂载4个 iso  - 分发3个iso 后 - 取消分发任务成功 - 虚拟机是挂载 原iso，已分发的3个 iso 可在集群使用
                故障测试
                    重复取消分发iso - Tower 触发重复取消报错提示
                    重复取消分发模板 - Tower 触发重复取消报错提示
                    ovf 导出失败 - Tower 报错提示正常
            tower460 调整集群默认存储策略为 3 副本
                tower 460 关联集群
                    smtx os 集群
                        关联 大于3节点 smtx os 620 集群 - 检查默认存储策略使用 3副本精简置备
                        关联 3节点 smtx os 515 集群 - 检查默认存储策略使用 3副本精简置备
                        关联 2节点 smtx os 集群 - 检查默认存储策略使用 3副本精简置备
                        关联 1节点 smtx os 集群 - 检查默认存储策略使用 3副本精简置备
                        编辑修改默认存储策略 - 可修改成功，创建虚拟机、虚拟卷使用修改后的默认存储策略
                        新关联集群 - 创建虚拟机 - 检查虚拟卷使用：3副本精简置备存储策略，新增卷使用集群默认 3副本存储策略
                        新关联集群 - 创建虚拟卷 - 检查虚拟卷使用：3副本精简置备存储策略
                        新关联集群 - 分发 2副本模板创建虚拟机 - 检查虚拟卷使用：2副本精简置备存储策略，新增卷使用集群默认 3副本存储策略
                        新关联集群3节点集群 - 分发 ec模板创建虚拟机 - 检查虚拟卷使用：降级为集群默认3副本精简置备存储策略，新增卷使用集群默认 3副本存储策略
                        克隆创建虚拟机 - 已有卷存储策略与源vm一致，新增卷使用默认 3副本存储策略
                        快照重建虚拟机 - 已有卷存储策略与源快照一致，新增卷使用默认 3副本存储策略
                        ovf 导入虚拟机模板 - 已有卷使用默认集群存储策略：3副本精简置备（只能新增cd-rom，不能新增卷）
                        ovf 导入虚拟机 - 已有卷存储策略、新增卷使用默认集群存储策略：3副本精简置备
                        ovf 导入虚拟卷 - 卷存储策略使用集群默认存储策略
                        编辑开机虚拟机 - 新增卷使用集群默认 3副本存储策略
                        编辑关机虚拟机 - 新增卷使用集群默认 3副本存储策略
                    smtx elf + elf/os 集群
                        smtx elf620 新关联 3节点 zbs570 集群 - 检查默认存储策略使用 3副本精简置备
                        smtx elf620 新关联 3节点 os620 集群 - 检查默认存储策略使用 3副本精简置备
                        编辑修改存储 os 默认存储策略 - 可修改成功，创建虚拟机、虚拟卷使用修改后的默认存储策略
                        编辑开机虚拟机 - 新增卷使用集群默认 3副本存储策略
                        编辑关机虚拟机 - 新增卷使用集群默认 3副本存储策略
                        新关联 zbs 集群 - 创建虚拟机 - 检查虚拟卷使用：3副本精简置备存储策略
                        新关联 os 集群 - 创建虚拟卷 - 检查虚拟卷使用：3副本精简置备存储策略
                        新关联 os集群 - 分发 2副本模板创建虚拟机 - 检查虚拟卷使用：2副本精简置备存储策略，新增卷使用集群默认 3副本存储策略
                        新关联集群3节点 zbs 集群 - 分发 ec模板创建虚拟机 - 检查虚拟卷使用：降级为集群默认3副本精简置备存储策略，新增卷使用集群默认 3副本存储策略
                        克隆创建虚拟机 - 已有卷存储策略与源vm一致，新增卷使用默认 3副本存储策略
                        快照重建虚拟机 - 已有卷存储策略与源快照一致，新增卷使用默认 3副本存储策略
                        tower 460 上 smtx zbs ovf 导入虚拟机模板 -（只能新增cd-rom，不能新增卷）
                        ovf 导入虚拟机 - 已有卷存储策略、新增卷使用默认集群存储策略：3副本精简置备
                        ovf 导入虚拟卷 - 卷存储策略使用集群默认存储策略：3副本精简
                tower 430 之前版本
                    tower 421:cluster settings 为空的集群 - tower 升级 460
                        smtx os 集群
                            smtx os 600 3节点集群 - Tower 升级 460 后，检查默认存储策略使用 3副本精简置备（UI 存储策略为 3副本精简，graphql 保持 setting null，保存后 setting 才会有值）
                            smtx os 513 3节点集群 - Tower 升级 460 后，检查默认存储策略使用 3副本精简置备（UI 存储策略为 3副本精简，graphql 保持 setting null，保存后 setting 才会有值）
                            Tower 升级 460 后，编辑修改集群默认存储策略 - 可修改成功，创建虚拟机、虚拟卷使用修改后的默认存储策略
                            smxt os集群， Tower 升级 460 后 - 创建虚拟机 - 检查虚拟卷使用：3副本精简置备存储策略
                            smxt os集群， Tower 升级 460 后 - 创建虚拟卷 - 检查虚拟卷使用：3副本精简置备存储策略
                            smxt os集群， Tower 升级 460 后 - 分发 2副本模板创建虚拟机 - 检查虚拟卷使用：2副本精简置备存储策略，新增卷使用集群默认 3副本存储策略
                            smxt os集群， Tower 升级 460 后 - 分发 ec模板创建虚拟机 - 检查虚拟卷使用：降级为集群默认3副本精简置备存储策略，新增卷使用集群默认 3副本存储策略
                            编辑开机虚拟机 - 新增卷使用集群默认 3副本存储策略
                            编辑关机虚拟机 - 新增卷使用集群默认 3副本存储策略
                            克隆创建虚拟机 - 已有卷存储策略与源vm一致，新增卷使用默认 3副本存储策略
                            快照重建虚拟机 - 已有卷存储策略与源快照一致，新增卷使用默认 3副本存储策略
                            ovf 导入虚拟机模板 - 已有卷使用默认集群存储策略：3副本精简置备（只能新增cd-rom，不能新增卷）
                            ovf 导入虚拟机 - 已有卷存储策略、新增卷使用默认集群存储策略：3副本精简置备
                            ovf 导入虚拟卷 - 卷存储策略与集群默认存储策略一致 3副本精简
                        smtx elf + zbs 集群
                            smtx elf600 关联 3节点 zbs560 集群 - Tower 升级 460 后，检查默认存储策略使用 3副本精简置备
                            Tower 升级 460 后，编辑修改zbs 默认存储策略 - 可修改成功，创建虚拟机、虚拟卷使用修改后的默认存储策略
                            smxt elf + zbs 集群， Tower 升级 460 后 - 创建虚拟机 - 检查虚拟卷使用：3副本精简置备存储策略
                            smxt elf + zbs 集群， Tower 升级 460 后 - 创建虚拟卷 - 检查虚拟卷使用：3副本精简置备存储策略
                            smxt elf + zbs 集群， Tower 升级 460 后 - 分发 2副本模板创建虚拟机 - 检查虚拟卷使用：2副本精简置备存储策略，新增卷使用集群默认 3副本存储策略
                            smxt elf + zbs 集群， Tower 升级 460 后 - 分发 ec模板创建虚拟机 - 检查虚拟卷使用：降级为集群默认3副本精简置备存储策略，新增卷使用集群默认 3副本存储策略
                            编辑开机虚拟机 - 新增卷使用集群默认 3副本存储策略
                            编辑关机虚拟机 - 新增卷使用集群默认 3副本存储策略
                            克隆创建虚拟机 - 已有卷存储策略与源vm一致，新增卷使用默认 3副本存储策略
                            快照重建虚拟机 - 已有卷存储策略与源快照一致，新增卷使用默认 3副本存储策略
                            ovf 导入虚拟机模板 - 已有卷存储策略使用默认集群存储策略：3副本精简置备（只能新增cd-rom，不能新增卷）
                            ovf 导入虚拟机 - 已有卷存储策略、新增卷使用默认集群存储策略：3副本精简置备
                            ovf 导入虚拟卷 - 卷存储策略与集群默认存储策略一致 3副本精简
                    tower 430:cluster settings 不为空的集群 - tower 升级 460
                        smtx os 集群
                            smtx os 610 已设置默认存储策略集群 - Tower 升级 460 后，检查默认存储策略保持：升级前的存储策略（如升级前设置默认2副本，升级后 默认2副本）
                            smtx os 513 已设置默认存储策略集群 - Tower 升级 460 后，检查默认存储策略保持：升级前的存储策略（如升级前设置默认2副本，升级后 默认2副本）
                            Tower 升级 460 后，编辑修改集群默认存储策略 - 可修改成功，创建虚拟机、虚拟卷使用修改后的默认存储策略
                            smtx os 已设置默认存储策略集群 ， Tower 升级 460 后 - 创建虚拟机 - 检查虚拟卷使用：升级前配置的存储策略
                            smtx os已设置默认存储策略集群， Tower 升级 460 后 - 创建虚拟卷 - 检查虚拟卷使用：升级前配置的存储策略
                            smtx os已设置默认存储策略集群， Tower 升级 460 后 - 分发 3副本模板创建虚拟机 - 检查虚拟卷使用：模板的存储策略，新增卷使用集群默认存储策略（与升级前一致）
                            smtx os已设置默认存储策略3副本集群， Tower 升级 460 后 - 分发 ec模板创建虚拟机 - 检查虚拟卷使用：降级为集群默认存储策略，新增卷使用集群默认存储策略（与升级前一致）
                            编辑开机虚拟机 - 新增卷使用集群默认存储策略（与升级前一致）
                            编辑关机虚拟机 - 新增卷使用集群默认存储策略（与升级前一致）
                            克隆创建虚拟机 - 已有卷存储策略与源vm一致，新增卷使用集群默认存储策略（与升级前一致）
                            快照重建虚拟机 - 已有卷存储策略与源快照一致，新增卷使用集群默认存储策略（与升级前一致）
                            ovf 导入虚拟机模板 - 已有卷使用集群默认存储策略（与升级前一致）（只能新增cd-rom，不能新增卷）
                            ovf 导入虚拟机 - 已有卷、新增卷使用集群默认存储策略（与升级前一致）
                            ovf 导入虚拟卷 - 卷存储策略与集群默认存储策略一致
                            升级前使用 ec 策略 2+2 的集群 -  升级460后，剩余4个节点运行，集群存储策略降级为3副本，剩余3个节点，降级为 2副本
                            升级前使用 ec 策略 2+1 的集群 -  升级460后，剩余3个节点，降级为 2副本
                        smtx elf + zbs 集群
                            smtx elf610+zbs560 已设置默认存储策略集群 - Tower 升级 460 后，检查默认存储策略保持：升级前的存储策略（如升级前设置默认2副本，升级后 默认2副本）
                            Tower 升级 460 后，编辑修改集群默认存储策略 - 可修改成功，创建虚拟机、虚拟卷使用修改后的默认存储策略
                            smtx elf+zbs 已设置默认存储策略集群 ， Tower 升级 460 后 - 创建虚拟机 - 检查虚拟卷使用：升级前配置的存储策略
                            smtx elf+zbs 已设置默认存储策略集群， Tower 升级 460 后 - 创建虚拟卷 - 检查虚拟卷使用：升级前配置的存储策略
                            smtx elf+zbs 已设置默认存储策略集群， Tower 升级 460 后 - 分发 3副本模板创建虚拟机 - 检查虚拟卷使用：模板的存储策略，新增卷使用集群默认存储策略（与升级前一致）
                            smtx elf+zbs 已设置默认存储策略3副本集群， Tower 升级 460 后 - 分发 ec模板创建虚拟机 - 检查虚拟卷使用：降级为集群默认存储策略，新增卷使用集群默认存储策略（与升级前一致）
                            编辑开机虚拟机 - 新增卷使用集群默认存储策略（与升级前一致）
                            编辑关机虚拟机 - 新增卷使用集群默认存储策略（与升级前一致）
                            克隆创建虚拟机 - 已有卷存储策略与源vm一致，新增卷使用集群默认存储策略（与升级前一致）
                            快照重建虚拟机 - 已有卷存储策略与源快照一致，新增卷使用集群默认存储策略（与升级前一致）
                            tower 460 上 smtx zbs ovf 导入虚拟机模板 -（只能新增cd-rom，不能新增卷）
                            ovf 导入虚拟机 - 已有卷、新增卷使用集群默认存储策略（与升级前一致）
                            ovf 导入虚拟卷 - 卷存储策略与集群默认存储策略一致
                graphql 存储策略配置检查
                    tower 430之前 没有保存过默认存储策略配置的集群，升级430 - graphql： cluster settings 默认存储测策略 null
                    tower 430 新关联/保存过默认存储策略配置的集群 - graphql: cluster settings 有指定的存储策略
                    tower 460 配置默认3副本生效的集群(新关联/未保存过存储策略)：graphql: cluster settings 指定为 3副本精简存储策略
                    cluster settings 存储策略是指：smtx os 集群  graphql 中 clusterForStoragePolicy.cluster.settings.default_storage_policy
                    cluster settings 存储策略是指：smtx elf +zbs/os 集群  graphql 中 clusterDataForStorageClusterSettings.cluster.storage_clusters_config.[zbs_index].default_storage_policy
                场景测试
                    smtx os 跨集群热迁移时，存储策略 - 预期为目标端配置的默认存储策略
                    smtx elf 集群仅迁移存储 - 目标端为 os 集群时，存储策略是smtxelf 上关联时配置的存储策略
                    smtx elf 集群仅迁移存储 - 目标端为 zbs 集群时，存储策略是smtxelf 上关联配置的存储策略
                    smtx elf 集群迁移 计算和存储  - 目标端为 smtx os 集群，存储策略预期使用目标端集群配置的默认存储策略
                    smtx elf 集群迁移 计算和存储  - 目标端为 smtx elf + zbs 集群，存储策略预期使用 目标端 smtx elf 为 zbs 配置的存储策略
                    smtx elf 集群迁移 计算和存储 - 目标端为 smtx elf + os 集群，存储策略预期使用 目标端 smtx elf 为os 配置的存储策略
                    配置ec 存储策略后切换为副本策略 - 预期副本策略默认配置：为3副本精简
            TOWER-14242 批量创建[高级模式]适配，虚拟卷名称使用虚拟机名称做前缀
                虚拟机创建
                    高级命名模式与虚拟卷名称交互检查
                        模板创建vm
                            创建 3 个虚拟机 修改高级命名- 挂载共享卷、cd-rom，对共享卷、cd-rom 命名无影响
                            创建 3 个虚拟机 不修改高级命名- 检查已有3个虚拟卷、新增3个卷的名称是：对应虚拟机名称 + 虚拟卷序号
                            创建 10 个虚拟机修改高级模式命名 - 检查已有3个虚拟卷、新增3个卷的名称是：对应修改后虚拟机名称 + 虚拟卷序号
                            创建 10 个虚拟机修改高级模式命名 - 检查已有3个虚拟卷、新增3个卷的名称是：- 自定义格式虚拟卷名称 - 创建出的虚拟机，自定义卷名称不变，其他卷所使用虚拟机名称做前缀
                            创建 10 个虚拟机修改高级模式命名 - 检查已有3个虚拟卷、新增3个卷的名称是：- 修改卷名称保持格式【vm{{i}}-1】- 创建出的虚拟机，所有卷仍所使用虚拟机名称做前缀
                            创建 10 个虚拟机修改高级模式命名 - 检查已有3个虚拟卷、新增3个卷的名称是：- 修改卷名称保持格式【 vm{{i}}-1-copy）】 - 创建出的虚拟机，所有卷仍所使用虚拟机名称做前缀
                            创建 10 个虚拟机修改高级模式命名 - 检查已有3个虚拟卷、新增3个卷：通过 copy 生成新卷 - copy 卷、其他卷，命名正确
                            创建 10 个虚拟机修改高级模式命名 - 检查已有3个虚拟卷、新增3个卷：通过 copy 生成新卷， copy后新卷再次 copy 后 - 检查：多次 copy 卷、其他卷，命名正确
                            创建 10 个虚拟机修改高级模式命名 - 已有卷、新增卷根据本次修改命名 - 返回修改起始名vm_name（修改命名公式）重新到虚拟卷页面：已有卷名称不变(若含公式则不计算)，后续所有虚拟机的新增卷、多次copy已有卷、多次 copy 新增卷都根据新虚拟机名称命名
                            创建 10 个虚拟机修改高级模式命名 - 已有卷、新增卷根据本次修改命名 - 返回修改某几个vm_name 重新到虚拟卷页面：已有卷名称不变，后续新增卷、多次copy已有卷、多次 copy 新增卷，这几个vm根据新虚拟机名称命名,其他虚拟卷按原始命名
                            创建 10 个虚拟机 修改高级命名后 - x86 的最大 64 个虚拟卷，都根据规则命名
                            创建 10 个虚拟机 修改高级命名后 - arm 的 1 nic + 10 virtio 虚拟卷，都根据规则命名
                            创建 10 个虚拟机 修改高级命名后 - arm 的 1 nic +32 scsi 虚拟卷，都根据规则命名
                        克隆创建vm
                            创建 3 个虚拟机 修改高级命名- 挂载共享卷、cd-rom，对共享卷、cd-rom 命名无影响
                            创建 3 个虚拟机 不修改高级命名- 检查已有3个虚拟卷、新增3个卷的名称是：对应虚拟机名称 + 虚拟卷序号
                            创建 10 个虚拟机修改高级模式命名 - 检查已有3个虚拟卷、新增3个卷的名称是：对应修改后虚拟机名称 + 虚拟卷序号
                            创建 10 个虚拟机修改高级模式命名 - 检查已有3个虚拟卷、新增3个卷的名称是：- 自定义格式虚拟卷名称 - 创建出的虚拟机，自定义卷名称不变，其他卷所使用虚拟机名称做前缀
                            创建 10 个虚拟机修改高级模式命名 - 检查已有3个虚拟卷、新增3个卷的名称是：- 修改卷名称保持格式【vm{{i}}-1】 - 创建出的虚拟机，所有卷仍所使用虚拟机名称做前缀
                            创建 10 个虚拟机修改高级模式命名 - 检查已有3个虚拟卷、新增3个卷的名称是：- 修改卷名称保持格式【 vm{{i}}-1-copy）】 - 创建出的虚拟机，所有卷仍所使用虚拟机名称做前缀
                            创建 10 个虚拟机修改高级模式命名 - 检查已有3个虚拟卷、新增3个卷：通过 copy 生成新卷 - copy 卷、其他卷，命名正确
                            创建 10 个虚拟机修改高级模式命名 - 检查已有3个虚拟卷、新增3个卷：通过 copy 生成新卷， copy后新卷再次 copy 后 - 检查：多次 copy 卷、其他卷，命名正确
                            创建 10 个虚拟机修改高级模式命名 - 已有卷、新增卷根据本次修改命名 - 返回修改起始名vm_name（修改命名公式）重新到虚拟卷页面：已有卷名称不变(若含公式则不计算)，后续所有虚拟机的新增卷、多次copy已有卷、多次 copy 新增卷都根据新虚拟机名称命名
                            创建 10 个虚拟机修改高级模式命名 - 已有卷、新增卷根据本次修改命名 - 返回修改某几个vm_name 重新到虚拟卷页面：已有卷名称不变，后续新增卷、多次copy已有卷、多次 copy 新增卷，这几个vm根据新虚拟机名称命名,其他虚拟卷按原始命名
                            创建 10 个虚拟机 修改高级命名后 - x86 的最大 64 个虚拟卷，都根据规则命名
                            创建 10 个虚拟机 修改高级命名后 - arm 的 1 nic + 10 virtio 虚拟卷，都根据规则命名
                            创建 10 个虚拟机 修改高级命名后 - arm 的 1 nic +32 scsi + 5virtio 虚拟卷，都根据规则命名
                            创建 3 个虚拟机 修改高级命名- 挂载共享卷、cd-rom，对共享卷、cd-rom 命名无影响
                        高级模式公式检查
                            批量创建时 - 检查侧边栏虚拟机名称正常展示公式
                            批量创建虚拟机时 - 高级模式 - 包含命名表达式的字符：{}-+i，不影响虚拟卷命名
                            批量创建时，修改高级模式命名：自定义某几个虚拟机名称前缀 - 检查已有3个虚拟卷、新增3个卷的名称是：对应虚拟机修改后虚拟机名称 + 虚拟卷序号
                            批量创建时，修改高级模式命名：自定义某几个虚拟机名称后缀 - 检查已有3个虚拟卷、新增3个卷的名称是：对应虚拟机修改后虚拟机名称 + 虚拟卷序号
                            批量创建时，修改高级模式命名：自定义某几个虚拟机名称修改中间名 - 检查已有3个虚拟卷、新增3个卷的名称是：对应虚拟机修改后虚拟机名称 + 虚拟卷序号
                            批量创建时，修改高级模式命名：自定义某几个虚拟机完全重命名 - 检查已有3个虚拟卷、新增3个卷的名称是：对应虚拟机修改后虚拟机名称 + 虚拟卷序号
            TOWER-16658 内容库-UEFI 模板创建分发保留 NVRAM 数据
                UEFI 虚拟机模板分发
                    UEFI 模版创建虚拟机到其他集群【创建任务包含分发】
                        SMTXOS1 UEFI 模版创建虚拟机到 SMTXOS2 集群， 目标虚拟机开机成功
                        SMTXOS1 UEFI 模版创建虚拟机到 SMTX ELF1 + SMTXZBS1 集群， 目标虚拟机开机成功
                        SMTXOS1 UEFI 模版创建虚拟机到 SMTX ELF1 + SMTXOS1 集群， 目标虚拟机开机成功
                        SMTXOS1 UEFI 模版创建虚拟机到 SMTX ELF1 + SMTXOS2 集群， 目标虚拟机开机成功
                        SMTX ELF1 + SMTXZBS1 的 UEFI 模版创建虚拟机到 SMTXOS2 集群， 目标虚拟机开机成功
                        SMTX ELF1 + SMTXZBS1 的 UEFI 模版创建虚拟机到 SMTX ELF1 + SMTXZBS2 集群， 目标虚拟机开机成功
                        SMTX ELF1 + SMTXZBS1 的 UEFI 模版创建虚拟机到 SMTX ELF1 + SMTXOS2 集群， 目标虚拟机开机成功
                        SMTX ELF1 + SMTXOS1 的 UEFI 模版创建虚拟机到 SMTXOS1 集群， 目标虚拟机开机成功
                        SMTX ELF1 + SMTXOS1 的 UEFI 模版创建虚拟机到 SMTXOS2 集群， 目标虚拟机开机成功
                        SMTX ELF1 + SMTXOS1 的 UEFI 模版创建虚拟机到 SMTX ELF1 + SMTXZBS2 集群， 目标虚拟机开机成功
                        SMTX ELF1 + SMTXOS1 的 UEFI 模版创建虚拟机到 SMTX ELF1 + SMTXOS2 集群， 目标虚拟机开机成功
                    UEFI 模版转化为虚拟机到其他集群
                        SMTXOS1 UEFI 模版转化为虚拟机， 目标虚拟机开机成功
                        SMTX ELF1 + SMTXOS1 的 UEFI 模版转化为虚拟机， 目标虚拟机开机成功
                    SMTXOS 集群模版
                        SMTXOS 虚拟机克隆的模版分发到 SMTXOS 集群， 目标模版有 nvram 数据，目标模版创建的虚拟机也有 nvram 数据
                        SMTXOS 虚拟机克隆的模版分发到 SMTXZBS 集群， 目标模版有 nvram 数据，目标模版创建的虚拟机也有 nvram 数据
                    SMTXZBS 作为存储集群的模版
                        SMTXELF + SMTXZBS 虚拟机克隆的模版分发到 SMTXOS 集群， 目标模版有 nvram 数据
                        SMTXELF + SMTXZBS1 虚拟机克隆的模版分发到 SMTXZBS2 集群， 目标模版有 nvram 数据
                    SMTXOS 作为存储集群的模版
                        SMTXELF + SMTXOS1 虚拟机克隆的模版分发到 SMTXOS2 集群， 目标模版有 nvram 数据
                        SMTXELF + SMTXOS1 虚拟机克隆的模版分发到 SMTXZBS2 集群， 目标模版有 nvram 数据
                回归测试
                    BIOS 模板创建 vm
                        SMTXOS1 创建 BIOS 模板 分发到 SMTXOS2 集群，目标模版克隆创建虚拟机，目标虚拟机开机正常
                        SMTX ELF1 + SMTXOS1 的 BISO 模版克隆为虚拟机到 SMTX ELF1 + SMTXZBS2 集群， 目标虚拟机开机成功
                集群兼容性
                    不兼容的集群， ～ 4.0.10 /  5.0.0 ～ 5.0.2
                        从【不支持集群】的 UEFI 模版分发到其他【支持的集群】，不保留 nvram 数据
                        从【支持的集群】的模版分发到 【不支持的集群】 的 UEFI 模版，不保留 nvram 数据
                    支持的集群， 4.0.11 ～ 4.0.14 / 5.0.3 ～ /5.1.0 ～ /  6.0.0 ～
                        从【支持集群】的 UEFI 模版分发到其他【支持的集群】，保留 nvram 数据
                模版数据来源兼容性
                    非 Tower 方式【fisheye】创建的 UEFI 模版，Tower 不保留 nvram 数据
                    Tower 4.6.0 之前已有的历史 UEFI 模版，不保留 nvram 数据
                UEFI 虚拟机创建内容库模版
                    SMTXOS 集群
                        创建模版
                            SMTXOS 的 UEFI 虚拟机，克隆为内容库模版，模版有 nvram 数据
                            SMTXOS 的 UEFI 虚拟机，转化为内容库模版，模版有 nvram 数据
                        创建模版后再操作
                            模版克隆为虚拟机，目标虚拟机有 nvram 数据
                            模版转化为虚拟机，目标虚拟机有 nvram 数据
                    SMTXELF
                        创建模版
                            SMTXELF 的 UEFI 虚拟机，克隆为内容库模版（所属存储为 SMTX ZBS 集群），模版有 nvram 数据
                            SMTXELF 的 UEFI 虚拟机，克隆为内容库模版（所属存储为 SMTX OS 集群），模版有 nvram 数据
                            SMTXELF 的 UEFI 虚拟机，转化为内容库模版（所属存储为 SMTX ZBS 集群），模版有 nvram 数据
                            SMTXELF 的 UEFI 虚拟机，转化为内容库模版（所属存储为 SMTX OS 集群），模版有 nvram 数据
                        创建模版后再操作
                            SMTXZBS 集群模版克隆为 SMTXELF + SMTXZBS 集群虚拟机（没有分发），目标虚拟机有 nvram 数据
                            SMTXZBS 集群模版转化为 SMTXELF + SMTXZBS 集群虚拟机（没有分发），目标虚拟机有 nvram 数据【备注：转化是不允许修改所属集群】
                            SMTXOS 集群模版克隆为 SMTXELF + SMTXOS 集群虚拟机（没有分发），目标虚拟机有 nvram 数据
                OVF 导入 UEFI 虚拟机模版
                    OVF 导入 UEFI 虚拟机模版， 模版不包含 nvram
                Tower admin API
                    新增 dump-content-library-vm-template-nvram-data 查询模版的 nvram
            TOWER-15920 虚拟机模板创建虚拟机实际使用内容库模板逻辑创建虚拟机
                smtx os 内容库 UEFI 模板分发到 新集群成功 - 模板在目标集群创建虚拟机成功，且能正常识别操作系统
                smtx os 内容库 BIOS模板分发到 新集群成功 - 模板在目标集群创建虚拟机成功，且能正常识别操作系统
        4.6.1
            Tower 禁止 KB-5828 受影响版本集群执行跨集群热迁移
                x86
                    4.0.x
                        4.0.x 不支持跨集群热迁移， UI 提示文案【迁移选项页面提示】
                    5.0.x
                        5.0.0 ~ 5.0.5
                            5.0.0 ~ 5.0.5 集群，不支持跨集群热迁移， UI 提示文案
                        5.0.6
                            未应用 Hotfix Patch 的集群
                                5.0.x：5.0.6 未应用 Hotfix Patch 的集群， 不支持跨集群热迁移， UI 提示文案
                                5.0.x：5.0.6 P1 未应用 Hotfix Patch 的集群， 不支持跨集群热迁移， UI 提示文案
                                5.0.x：5.0.6 P2 未应用 Hotfix Patch 的集群， 不支持跨集群热迁移， UI 提示文案
                            已应用 Hotfix Patch 的集群
                                5.0.x：5.0.6 已应用 Hotfix Patch 的集群， 支持做跨集群热迁移
                                5.0.x：5.0.6 P1 已应用 Hotfix Patch 的集群， 支持做跨集群热迁移
                                5.0.x：5.0.6 P2 已应用 Hotfix Patch 的集群， 支持做跨集群热迁移
                        5.0.7
                            5.0.x：5.0.7 集群，不支持跨集群热迁移， UI 提示文案
                            5.0.x：5.0.7 solution 集群，不支持跨集群热迁移， UI 提示文案
                            5.0.x：5.0.7-P1 集群，支持跨集群热迁移
                    5.1.x
                        > 5.1.3
                            5.1.4 支持跨集群热迁移
                            5.1.5 支持跨集群热迁移
                        5.1.0
                            5.1.0 集群，不支持跨集群热迁移， UI 提示文案
                        5.1.1
                            5.1.1 集群，不支持跨集群热迁移， UI 提示文案
                            5.1.1-P1 集群，不支持跨集群热迁移， UI 提示文案
                        5.1.2
                            5.1.2 集群，不支持跨集群热迁移， UI 提示文案
                            5.1.2 solution 集群，不支持跨集群热迁移， UI 提示文案
                            5.1.2-P1 集群， 支持跨集群热迁移
                        5.1.3
                            5.1.3 集群，不支持跨集群热迁移， UI 提示文案
                            5.1.3 solution 集群，不支持跨集群热迁移， UI 提示文案
                            5.1.3-P1 集群，支持跨集群热迁移
                arm
                    5.1.2
                        5.1.2 集群，不支持跨集群热迁移， UI 提示文案
                    5.1.3
                        5.1.3 集群，不支持跨集群热迁移， UI 提示文案
                        5.1.3-P1 集群， 支持跨集群热迁移
                    > 5.1.3
                        5.1.5 集群， 支持跨集群热迁移
            CPU 独占入口 TOWER-18519
                3.x / 4.0.x 集群， 不支持 CPU 独占
                5.0.x: 5.0.0 ~ 5.0.4 集群， 不支持 CPU 独占
                5.0.x:  >= 5.0.5， 支持 CPU 独占
                5.1.x ， 支持 CPU 独占
            OAPI 虚拟机电源操作添加限制
                运行中状态
                    触发开机，预期失败
                    触发关机，关机成功
                    触发强制关机，关机成功
                    触发重启， 重启成功
                    触发强制重启， 重启成功
                    触发恢复，预期失败
                    触发暂停，暂停成功
                关机状态
                    触发开机，开机成功
                    触发关机，预期失败
                    触发强制关机，预期失败
                    触发重启， 预期失败
                    触发强制重启， 预期失败
                    触发暂停，预期失败
                    触发恢复，预期失败
                暂停状态
                    触发开机，预期失败
                    触发关机，预期失败
                    触发强制关机， 关机成功
                    触发重启， 预期失败
                    触发强制重启， 预期失败
                    触发暂停， 预期失败
                    触发恢复， 恢复成功
            Tower 支持 VMTOOLS 执行脚本
                异常场景
                    集群未开启支持 VMTools 执行命令行功能
                    虚拟机 SVT 不可用
                    虚拟机不是开机状态
                    虚拟机不存在
                oapi
                    集群开启功能
                        触发 http://172.20.152.140/v2/api/execute-command-in-vm 可以正常对虚拟机执行命令行
                    集群关闭功能
                        触发 api 后返回功能不支持 SVT_CLUSTER_CAPABILITY_DISABLED
                sdk
                    ApiClient 可以正常触发 execute_command_in_vm【公网版本不包含这个功能】
                graphql
                    mutation {   executeCommandInVm 可以触发对虚拟机执行命令行
                Tower 事件审计
                    执行成功的记录， 记录中包含脚本原始字符
                    执行失败， 记录执行返回的原始信息
                升级组合测试
                    【tower 4.6.0+ patch、OS514P1 + patch、VMTools 3.2.2 + patch】 升级到【4.6.1 + OS 5.1.5 + VMTools 4.0.0】
                    【平安科技当前版本】 升级到 【tower 4.6.0+ patch、OS514P1 + patch、VMTools 3.2.2 + patch】
                API 文档
                    预期 api 文档中不包含  【vmtools 执行命令行】支持范围的 api 描述【oapi 正常展示， sdk 不展示】
            TOWER-18662 arm模版 cd-rom 使用检查（461&442）
                模版使用
                    含 cd-rom(usb) 、不含 scsi 卷 的 515 模版 - 514集群创建 vm 并添加 scsi 卷成功 - 检查 集群内部模版、新虚拟机 cd-rom 是 scsi 总线
                    含 cd-rom（usb） 、不含 scsi 卷 的 610及以上 模版 - 600集群创建 vm 并添加 scsi 卷成功 - 检查 集群内部模版、新虚拟机 cd-rom 是 scsi 总线
                    含 cd-rom(usb) 、不含 scsi 卷 的 610及以上 模版 - 514 集群创建 vm 删除cd-rom，并添加新 cd-rom、 scsi 卷成功 - 检查 集群内部模版、新虚拟机 cd-rom 是 scsi 总线
                    含 cd-rom（usb） 、不含 scsi 卷 的 515 模版 - 600 集群创建 vm 删除cd-rom，并添加新 cd-rom、 scsi 卷成功 - 检查 集群内部模版、新虚拟机 cd-rom 是 scsi 总线
                    含 cd-rom(scsi) 、不含 scsi 卷 的 515 以下 模版 - 515集群创建 vm 并添加 scsi 卷成功 - 检查 集群内部模版、新虚拟机 cd-rom 是 usb 总线
                    含 cd-rom（scsi） 、不含 scsi 卷 的 600 模版 - 610及以上 集群创建 vm 并添加 scsi 卷成功 - 检查 集群内部模版、新虚拟机 cd-rom 是 usb 总线
                    含 cd-rom(scsi) 、不含 scsi 卷 的 600 模版 - 515 集群创建 vm 删除cd-rom，并添加新 cd-rom、 scsi 卷成功 - 检查 集群内部模版、新虚拟机 cd-rom 是 usb 总线
                    含 cd-rom（scsi） 、不含 scsi 卷 的 515以下 模版 - 610及以上 集群创建 vm 删除cd-rom，并添加新 cd-rom、 scsi 卷成功 - 检查 集群内部模版、新虚拟机 cd-rom 是 usb 总线
                    含 cd-rom(usb 从os 分发) 、不含 scsi 卷的 arm 架构 zbs 模版 - 在 smtx elf + zbs  - 创建 vm 并添加 scsi 卷成功 - 检查虚拟机 cd-rom 是 scsi 总线 （ELF-5784 保持arm cd-rom 是 scsi ）
                    含 cd-rom(scsi) 、不含 scsi 卷的 arm 架构 zbs 模版 - 在 smtx elf+ zbs  - 创建 vm 并添加 scsi 卷成功 - 检查虚拟机 cd-rom 是 scsi 总线 （ELF-5784 保持arm cd-rom 是 scsi）
                    含 cd-rom(usb) 、含virtio+scsi 卷 的 515 模版 - 514集群创建 vm 并添加 scsi 卷成功 - 检查 集群内部模版、新虚拟机 cd-rom 是 scsi 总线
                    含 cd-rom(scsi) 、含virtio+scsi 卷 的 600 模版 - 620集群创建 vm 并添加 scsi 卷成功 - 检查 集群内部模版、新虚拟机 cd-rom 是 usb 总线
                    无 cd-rom 模版 - 创建vm 添加 virtio+scsi+cdrom- 515、610及以上vm cd-rom是 usb，515以下、600vm cd-rom是 scsi
                    x86 架构 - 检查 515 含cd-rom(ide)  模版 - 创建vm 到低版本 514、高版本620、zbs - 检查虚拟机 tower ui、 elf api 为 ide 总线
                虚拟机模版分发
                    含 cd-rom (usb)、不含 scsi 卷 的 515 模版 - 分发到 514 集群,集群集群内部模版 cd-rom 是 scsi 总线 ；分发到 610+  集群 - 检查 集群内部模版 cd-rom 是 usb 总线  - 内容库 UI 展示为 USB 总线
                    含 cd-rom (usb）、不含 scsi 卷 的 610+ 的模版 - 分发到 600 集群,集群集群内部模版 cd-rom 是 scsi 总线 ；分发到 515 集群 - 检查 集群内部模版 cd-rom 是 usb 总线 - 内容库 UI 展示为 USB 总线
                    含 cd-rom (usb）、不含 scsi 卷 的 515 的模版 - 分发到 514 集群后，删除 515  的集群 - 数据同步后检查 集群内部模版 cd-rom 是 scsi 总线 ，内容库 UI 展示为 USB 总线（已知问题 TOWER-18739）
                    含 cd-rom (usb）、不含 scsi 卷 的 610+ 的模版 - 分发到 600 集群后，删除 610+  的集群 - 数据同步后检查 集群内部模版 cd-rom 是 scsi 总线 ，内容库 UI 展示为 USB 总线（已知问题 TOWER-18739）
                    含 cd-rom (scsi)、不含 scsi 卷 的 515 以下模版 - 分发到 515、610+  集群 - 检查 集群内部模版 cd-rom 是 usb 总线 ，内容库 UI 展示为 scsi 总线
                    含 cd-rom (scsi)、不含 scsi 卷 的 600 模版 - 分发到 515、610+  集群 - 检查 集群内部模版 cd-rom 是 usb 总线 ，内容库 UI 展示为 scsi 总线
                    含 cd-rom (scsi）、不含 scsi 卷 的 515以下 的模版 - 分发到 515 集群后，删除 515以下  的集群 - 数据同步后检查 集群内部模版 cd-rom 是 usb 总线 ，内容库 UI 展示为 scsi 总线（已知问题 TOWER-18739）
                    含 cd-rom (scsi）、不含 scsi 卷 的 600 的模版 - 分发到 610+ 集群后，删除 600 的集群 - 数据同步后检查 集群内部模版 cd-rom 是 usb 总线 ，内容库 UI 展示为 scsi 总线（已知问题 TOWER-18739）
                    含 cd-rom (usb)、不含 scsi 卷 的 515/610+ 的 模版 - 分发到 zbs 集群，删除虚拟机515是 610 + 的集群 - 数据同步后检查 内容库 UI 展示为 USB 总线
                    含 cd-rom (scsi)、不含 scsi 卷 的 515以下、600 的 模版 - 分发到 zbs 集群，删除虚拟机 515 以下、 600 的集群 - 数据同步后检查内容库 UI 展示为 scsi 总线
                    含 cd-rom (usb）、不含 scsi 卷 的 515 的模版 - 分发到 514 集群后，删除 515 的集群 - 取消514 集群与tower关联后重新关联集群 - cd-rom 总线为 scsi
                    含 cd-rom (scsi）、不含 scsi 卷 的 600 的模版 - 分发到 610及以上 集群后，删除 600 的集群 - 取消 610及以上 集群与tower关联后重新关联集群 - cd-rom 总线为 usb
                    x86 架构 - 检查 515 含cd-rom(ide)  模版 - 分发到低版本 514、高版本620、zbs - 检查虚拟机模版  tower ui、 elf api 为 ide 总线
        4.7.0
            回收站
                回收站 UI 菜单
                    回收站虚拟机菜单展示检查
                        虚拟机下面没有资源
                        虚拟机下面有多个虚拟机，包含分页
                    一键清空
                        回收站一键清空
                            清空一个虚拟机
                            清空多个虚拟机
                            清空所有类似资源
                            没有资源时，一键清空不可用
                        虚拟机页面一键清空
                            清空一个虚拟机
                            清空多个虚拟机
                            没有资源时，一键清空不可用
                    关联不同集群检查
                        未关联集群不展示回收站菜单
                        Tower 4.7.0 仅关联 SMTXZBS（>=5.7.0） 集群， 展示 回收站 菜单 （Tower 461 同场景不展示）
                回收站规则
                    默认规则
                        tower 4.6.1
                            Tower 4.6.1 - 默认启用，保留 30 天，无特例规则
                            默认清理时间为 Tower 每天 23:59【检查系统事件中 回收站虚拟机永久删除 的触发时间】
                        tower 4.7.0
                            Tower 4.7.0 - 默认启用，保留 30 天，无特例规则
                            默认清理时间为 Tower 每 30 分钟执行一次， ZBS 集群每 1 分钟执行一次。
                    关联集群
                        SMTX OS 集群【已关闭 ZBS 回收站】
                            Tower 级别规则为【开启回收站】，Tower 关联 SMTXOS 集群后，SMTX OS 回收站为开启
                            Tower 级别规则为【关闭回收站】，Tower 关联 SMTXOS 集群后，SMTX OS 回收站为关闭
                        SMTX OS(>=6.3.0) 集群【已启用 ZBS 回收站】
                            Tower 级别规则为【开启回收站】，Tower 关联 SMTXOS 集群后，SMTX OS 回收站为开启
                            Tower 级别规则为【关闭回收站】，Tower 关联 SMTXOS 集群后，Tower 级别保持关闭，给集群增加一条特例规则配置开启回收站
                            关联到 Tower 后展示已经进入回收站的资源（虚拟化资源对应 lun ）
                        关联 SMTX ELF 集群
                            回收站状态跟随 Tower 级别默认规则
                    新部署集群
                        新部署 SMTX OS （ >=6.3.0）集群的 ZBS 回收规则为关闭
                        新部署 SMTX OS （< 6.3.0 ）集群的 ZBS 回收规则为关闭
                        SMTX ELF 没有集群回收站状态
                    集群升级
                        SMTX OS 集群升级到 6.3.0+
                            Tower 级别规则为【开启回收站】，SMTX OS 回收站为开启
                            Tower 级别规则为【关闭回收站】，SMTX OS 回收站为关闭
                            升级前集群没有特例规则
                                Tower 默认为关闭，Tower 和集群保持一致的配置，无特殊处理。
                                Tower 默认为开启，Tower 设置集群开启 zbs 回收站， 设置特例规则？
                            升级前集群有特例规则
                                特例规则为开启， 同步设置集群开启回收站 ？？？
                                特例规则为关闭，保持关闭状态。
                                特例规则为开启，保持开启状态，且 tower 发起一次设置 zbs 回收站为开启。
                        SMTX ELF 集群升级到 6.3.0+
                            Tower 回收站中集群的配置规则不变
                    修改规则
                        Tower 修改默认规则
                            集群没有特例规则
                                Tower 级别默认规则修改为开启，设置成功，SMTX OS / SMTX ELF 集群同步设置开启成功，SMTX OS 集群 ZBS 回收站同步开启
                                Tower 级别默认规则修改为关闭，设置成功，SMTX OS / SMTX ELF 集群同步设置关闭成功，SMTX OS 集群 ZBS 回收站同步关闭
                            集群有特例规则
                                Tower 级别默认规则修改为开启，设置成功， SMTX OS / SMTX ELF 保持按特例规则生效
                                Tower 级别默认规则修改为关闭，设置成功， SMTX OS / SMTX ELF 保持按特例规则生效
                        Tower 修改特例规则
                            Tower 设置开启回收站，集群特例规则设置关闭回收站，集群实际按关闭回收站生效
                            Tower 设置关闭回收站，集群特例规则设置开机回收站，集群实际按开启回收站生效
                        ZBS 命令行修改集群回收站设置
                            Tower 和 SMTX OS 集群配置一致（无特例规则）
                                都是开启回收站， ZBS 命令行设置关闭回收站， Tower 同步数据后为集群增加一条特例规则（配置关闭回收站）
                                都是关闭回收站， ZBS 命令行设置开启回收站，  Tower 同步数据后为集群增加一条特例规则（配置开启回收站）
                            Tower 和 SMTX OS 集群配置不同
                                Tower 配置开启，SMTX OS 配置关闭，ZBS 命令行设置开启， Tower 在 1 小时后同步到集群开启回收站，自动修改集群特例规则为开启回收站
                                Tower 配置关闭，SMTX OS 配置开启，ZBS 命令行设置关闭， Tower 在 1 小时后同步到集群关闭回收站，自动修改集群特例规则为关闭回收站
                        集群关闭回收站
                            已经在回收站的资源立即删除
                    修改回收时间
                        Tower 已存在回收站虚拟机 N 天过期， 修改回收站规则为 N-1 天过期， UI 提示部分虚拟机在修改规则后 30 分钟内自动永久删除。
                        集群 已存在回收站虚拟机 N 天过期， 修改回收站规则为 N-1 天过期， UI 提示部分虚拟机在修改规则后 30 分钟内自动永久删除。
                    故障场景
                        Tower 编辑集群回收站规则，集群回收站规则修改失败情况，预期 Tower 任务也失败
                回收站恢复资源（虚拟机恢复）
                    原虚拟机已启用常驻缓存， 恢复弹窗提示：恢复至原所属主机，默认不启用常驻缓存
                    集群内存在原虚拟机同名虚拟机，恢复虚拟机时提示存在重名需要重命名，重命名后恢复成功
                    恢复多个虚拟机，其中一部分原虚拟机已开启常驻缓存，批量恢复弹窗提示：恢复至原所属主机，默认不启用常驻缓存
                    恢复多个虚拟机，其中存在重名的虚拟机，需要分别设置新名称
                关闭回收站
                    回收站已有资源立即删除，有提示
                Tower 运维
                    已有回收站的默认规则和特例规则保持不变（仅对升级前 UI 创建的特例规则做保留）
                任务
                    创建特例规则， 任务描述： 更新 xxxx 集群回收站设置
                    编辑特例规则， 任务描述： 更新 xxxx 集群回收站设置
                    删除特例规则， 任务描述： 更新 xxxx 集群回收站设置
                事件
                    创建特例规则, 事件类型：编辑回收站特例规则， 详情描述具体规则
                    编辑特例规则, 事件类型：编辑回收站特例规则， 详情描述具体变更
                    删除特例规则, 事件类型：编辑回收站特例规则， 详情描述具体变更
                SMTXOS （ELF）集群（>=630）
                    SMTXOS（>= 6.3.0） 已配置开启 ZBS 回收站
                        tower 全局开启回收站，关联集群， 关联后集群回收站配置为开启回收站（无特例规则）
                        tower 全局关闭回收站，关联集群， 关联后集群回收站配置为开启回收站（有特例规则）
                        Tower 回收站删除虚拟机时，在 elf 的资源立即删除，在 zbs 的关联资源立即删除
                        Tower 立即删除非虚拟机资源（ISO、模版、快照、卷），在 elf 的资源立即删除，在 zbs 的关联资源立即删除。
                    SMTXOS 已配置关闭 ZBS 回收站
                        tower 全局开启回收站，关联集群， 关联后集群回收站配置为关闭回收站（有特例规则）
                        tower 全局关闭回收站，关联集群， 关联后集群回收站配置为关闭回收站（无特例规则）
                        Tower 删除所有虚拟化资源（虚拟机、ISO、模版、快照、卷），在 elf 的资源立即删除，在 zbs 的关联资源立即删除。
                    支持命令行设置 ZBS 回收站是否启用的状态
                        Tower 上已开启集群回收站
                            命令行设置关闭 ZBS 回收站， Tower 需要定期同步并更新 Tower 展示为集群已关闭回收站
                            此时的数据同步时间差导致会出现 Tower 上开启回收站但是 ZBS 关闭回收站的情况，需要兼容处理
                            Tower 同步集群是否开启回收站的时间间隔为1 小时
                        Tower 上已关闭集群回收站
                            命令行设置开启 ZBS 回收站， Tower 需要定期同步并更新 Tower 展示为集群已开启回收站
                            此时的数据同步时间差导致会出现 Tower 上关闭回收站但是 ZBS 开启回收站的情况，需要兼容处理。
                        集群升级
                            不支持 ZBS 回收站的集群升级到支持 ZBS 回收站的（620 升级到 630）， 按 tower 已有对这个集群的回收站策略（默认或者特例）设置给集群。
                    Tower 回收站设置
                        Tower 全局设置开启回收站， SMTXOS 集群同步设置为开启（集群的 ZBS 回收站一起设置开启）
                        Tower 特例规则设置集群开启回收站， SMTXOS 集群的 ZBS 回收站一起设置开启
                        Tower 设置集群关闭回收站， SMTXOS 集群的 ZBS 回收站一起设置关闭
                SMTXELF 集群
                    SMTX ELF 【开启回收站】
                        存储集群 开启 ZBS 回收站
                            已适配 SMTX ELF（ >=630 ）
                                Tower 删除所有虚拟化资源，在 elf 的资源立即删除，在 zbs 的关联资源立即删除
                            未适配 SMTX ELF（ < 630 ）
                                Tower 删除虚拟机，在 elf 的资源立即删除，在 zbs 的关联资源进入 zbs 回收站。
                                Tower 非虚拟机资源（ISO、模版、快照、卷），在 elf 的资源立即删除，在 zbs 的关联资源进入 zbs 回收站。
                        存储集群 关闭 ZBS 回收站
                            Tower 删除（回收站删除或者立即删除）所有虚拟化资源（虚拟机、ISO、模版、快照、卷），在 elf 的资源立即删除，在 zbs 的关联资源立即删除。
                    SMTX ELF 【关闭回收站】
                        存储集群 开启 ZBS 回收站
                            已适配 SMTX ELF（ >=630 ）
                                Tower 立即删除虚拟机，在 elf 的资源立即删除，在 zbs 的关联资源进入 zbs 回收站
                                Tower 删除非虚拟机资源（ISO、模版、快照、卷），在 elf 的资源立即删除，在 zbs 的关联资源立即删除。
                            未适配 SMTX ELF（ < 630 ）
                                删除虚拟机，在 elf 的资源立即删除，在 zbs 的关联资源进入 zbs 回收站。
                                删除非虚拟机资源（ISO、模版、快照、卷），在 elf 的资源立即删除，在 zbs 的关联资源进入 zbs 回收站。
                        存储集群 关闭 ZBS 回收站
                            Tower 立即删除所有虚拟化资源（虚拟机、ISO、模版、快照、卷），在 elf 的资源立即删除，在 zbs 的关联资源立即删除。
            TOWER-18265 tower UI 支持克隆虚拟卷
                UI-验收测试
                    操作入口：集群 - 虚拟卷  - 虚拟卷详情：克隆
                    克隆卷页面检查 - 源虚拟卷名称、虚拟卷类型、存储策略：不可修改，与源虚拟卷保持一致
                    克隆卷页面检查 - 虚拟卷名称：默认为「{{源虚拟卷名称}}-clone」，可修改
                    克隆卷页面检查 - 描述： 默认为「克隆自{{源虚拟卷名称}}」，可修改
                    克隆卷页面检查 - 虚拟卷名称校验：校验规则：长度 255 个字符，字符「不支持分号（;）、反斜杠（\）和双引号（"）。其他均支持
                    克隆卷页面检查 - 描述 校验规则：UI 无限制，后端限制字符长度 255，不校验非法字符集
                    克隆卷页面检查 - 虚拟卷名称：名称重复校验 --待确认
                    英文页面检查 - 克隆卷 - 页面正常
                    克隆的虚拟卷 - 页面可操作项：克隆、导出、删除
                    克隆的虚拟卷 - 卷详情展示：卷基础信息、卷存储策略信息展示正确，可跳转项：数据中心、集群、挂载的vm（未挂载不展示） ，跳转正确
                    克隆虚拟卷 - 监控分析 - 数据监控正确
                    克隆虚拟卷 - 标签 - 添加/删除标签成功
                    批量编辑标签：克隆虚拟卷、创建的卷 - 批量添加/删除标签成功
                    导出 csv 文件含：克隆虚拟卷、创建的卷 - 导出成功，下载的数据正确
                    从虚拟卷克隆来的卷 - 再次发起克隆 - 克隆成功，使用默认名称和描述，其他配置与源虚拟卷一致 - 挂载到vm 可正常 fio 使用
                    ACOS tower 470  - 有虚拟卷克隆的入口，克隆卷正常
                克隆卷使用
                    克隆
                        版本检查
                            smtx os 3.x (3.5.17)集群操作 - 普通虚拟卷2副本精简制备，克隆 - 克隆成功使用默认名称和描述，其他配置与源虚拟卷一致 - 挂载到vm 可正常 fio 使用
                            smtx os 4.x (4.0.14)集群操作 - 共享虚拟卷普通虚拟卷3副本厚制备，克隆 - 克隆成功使用默认名称和描述，其他配置与源虚拟卷一致 - 挂载到vm 可正常 fio 使用
                            smtx os 5.x (5.1.5)集群操作 - 普通虚拟卷2副本厚制备，克隆 - 克隆成功使用默认名称和描述，其他配置与源虚拟卷一致 - 挂载到vm 可正常 fio 使用
                            smtx os 6.x (6.2.0)集群操作 - 共享虚拟卷 EC 策略，克隆 - 克隆成功使用默认名称和描述，其他配置与源虚拟卷一致 - 挂载到vm 可正常 fio 使用
                            smtx elf 6.x +zbs  (elf 620+zbs 562)集群操作 - 普通虚拟卷 副本策略，克隆 - 克隆成功使用默认名称和描述，其他配置与源虚拟卷一致 - 挂载到vm 可正常 fio 使用
                            smtx elf 6.x +os  (elf 620+os620)集群操作 - 共享虚拟卷 EC 策略，克隆 - 克隆成功使用默认名称和描述，其他配置与源虚拟卷一致 - 挂载到vm 可正常 fio 使用
                        高级属性检查
                            支持 EC 策略的集群，EC卷 - 克隆 - 克隆成功，存储策略 EC 卷，使用默认名称和描述，其他配置与源虚拟卷一致，事件记录正确
                            支持常驻缓存的集群，开启常驻缓存的卷 - 克隆 - 克隆成功，常驻缓存开启，使用默认名称和描述，其他配置与源虚拟卷一致，事件记录正确
                            支持常驻缓存的集群，关闭常驻缓存的卷 - 克隆 - 克隆成功，常驻缓存关闭，使用默认名称和描述，其他配置与源虚拟卷一致，事件记录正确
                            支持数据加密的集群，开启加密的卷 - 克隆 - 克隆成功，数据加密关闭，使用默认名称和描述，其他配置与源虚拟卷一致，事件记录正确
                            支持数据加密的集群，关闭加密的卷 - 克隆 - 克隆成功，数据加密关闭，使用默认名称和描述，其他配置与源虚拟卷一致，事件记录正确
                            smtx os 620 :EC 策略、开启常驻缓存、开启数据加密的卷 - 克隆 - 克隆成功：常驻缓存、数据加密开启，使用默认名称和描述，其他配置与源虚拟卷一致，事件记录正确
                            smtx elf620 + zbs :EC 策略、开启常驻缓存、开启数据加密的卷 - 克隆 - 克隆成功：常驻缓存、数据加密开启，使用默认名称和描述，其他配置与源虚拟卷一致，事件记录正确
                            smtx elf620 + os620 :EC 策略、开启常驻缓存、开启数据加密的卷 - 克隆 - 克隆成功：常驻缓存、数据加密开启，使用默认名称和描述，其他配置与源虚拟卷一致，事件记录正确
                        事件
                            虚拟卷克隆  - 事件记录正确，记录卷信息与源卷数据一致
                    ovf 导出/导入
                        克隆卷详情 - 导出 VMDK 格式卷，导出虚拟卷成功
                        克隆卷详情 - 导出 RAW 格式卷，导出虚拟卷成功
                        克隆卷详情 - 导出 QCOW2 格式卷，导出虚拟卷成功
                        批量操作导出：克隆卷、新建卷 - VMDK 格式，导出虚拟卷成功
                        批量操作导出：克隆卷、新建卷 - RAW 格式，导出虚拟卷成功
                        批量操作导出：克隆卷、新建卷 - QCOW2 格式，导出虚拟卷成功
                        克隆的 VMDK 卷批量导出后 - 重新导入集群 ，能挂载到虚拟机进行 fio
                        克隆的 RAW 卷导出后 - 重新导入集群 ，能挂载到虚拟机进行 fio
                        克隆的 QCOW 卷导出后 - 重新导入集群 ，能挂载到虚拟机进行 fio
                        类型为共享卷的克隆卷 - 卷详情无导出入口，不支持 ovf 导出
                        类型为共享卷的克隆卷、创建卷 - 批量导出，校验不支持导出
                    删除
                        单个删除 - 克隆的虚拟卷 - 删除成功
                        批量删除 - 克隆的虚拟卷 - 删除成功
                        批量删除 - 直接创建的原虚拟卷和克隆创建的虚拟卷 - 删除成功
                    虚拟机使用克隆卷
                        普通克隆卷（副本策略、开启常驻缓存、加密）- 挂在到关机虚拟机，编辑总线 - 挂载成功，vm 可正常使用
                        共享克隆卷（副本策略、开启常驻缓存、加密） -  挂在到开机虚拟机，编辑总线 - 挂载成功，vm 可正常使用
                        编辑虚拟机 - 编辑克隆普通卷（副本策略、开启常驻缓存、加密） -  编辑副本策略、关闭常驻缓存、容量 - 编辑生效
                        编辑虚拟机 - 编辑克隆共享卷（EC 策略、关闭常驻缓存、加密） -  编辑开启常驻缓存、容量 - 编辑生效
            TOWER-16914 虚拟机组多级嵌套
                虚拟机组弹窗
                    面包屑
                        面包屑：展示已选择的虚拟机组路
                        第五层级虚拟机组 - 路径展示正确：集群/L1/L2/L3/L4/L5
                        第一层级虚拟机组 - 路径展示正确：集群/L1
                        未创建虚拟机组 - 路径展示正确：集群
                    弹窗大小
                        弹窗宽度固定为 720px，高度取决于 viewport 高度，为 Viewport 高度 -  80px*2
                        弹窗的最小高度为 460px，最大高度为 1200px
                    搜索框支持模糊匹配
                        检查搜索框展示：未操作默认展示、鼠标悬浮展示灰框，选中展示蓝色并有光标闪动
                        模糊匹配时，不对列表进行过滤（始终展示所有项）；
                        模糊匹配时，自动展开匹配项的所有父级项；
                        模糊匹配时，若某项的子级项均未匹配关键字，则收起该项；
                        模糊匹配时，加粗并标蓝搜索关键字。
                    虚拟机组选择列表
                        Tree Item 样式说明
                            检查第一层级虚拟机组 - 无没有缩进
                            检查子层级虚拟机组 - 每个子组与上一个组缩进 24px（设计稿22px 无影响忽略）
                            检查拖动表示标识展示：鼠标悬浮/选中虚拟机组时，展示 Icon suffix (optional) 图标
                            检查折叠功能 - 折叠图标：在有子组时才展示，没有子组不展示 - 折叠/展开功能正确
                            检查虚拟机组图标展示：展示图标和虚拟机组名称
                        Tree Item 交互说明
                            点击 Branch node 整体（含子组的虚拟机组名称）时，意味着选中该层级且展开所有子级 - UI 该层级被选中为蓝色，并展示该层级下子项----没展开 记录 ticket
                            点击 Caret（折叠图标）具备局部行为，单点击 Caret 仅展开所有子级，不选中当前项 - UI 该层级不会被选中，并展示该层级下子项
                    新建虚拟机组
                        固定展示在虚拟机组弹窗的最下方，上方tree列表在上虞空间内滚动
                        在当前选中项中创建子虚拟机组 - 未输入文字前，禁用创建 button
                        输入文字后，创建 button 解除禁用 - 点击后触发创建
                        点击创建 button 后，输入框禁用，当前项的 triangle （虚拟机组）和创建 button 展示 loading 状态
                        发起虚拟机组创建时 - 虚拟机组 tree 不会被折叠
                        创建成功，虚拟机组 tree 保持展开，按照名称顺序展示虚拟机组，并默认选中新创建的组
                        创建失败，在输入框下方展示 error info
                        在同一层级创建同名虚拟机组 - 不能创建，报错：当前层级内已存在同名虚拟机组。
                        检查虚拟机组 - 字符长度：1-255，超过长度报错：虚拟机组名称支持的字符长度范围为 1-255。
                        检查虚拟机组，非法字符集：不允许输入特定字符：（%, &, *, $, #, @, !, \, /, :, *, ?, ", <, >, |, ;, '） - 输入有校验提示 ：不支持如下特殊字符：%, &, *, $, #, @, !, \, /, :, *, ?, ", <, >, |, ;, '
                        若未选中任何项，则意为在当前集群创建虚拟机组
                        选中虚拟机组，则意为在当前虚拟机组创建子虚拟机组
                        若选中虚拟机组为 L5 层，则禁用输入框并展示禁用文案
                        集群没有虚拟机组 - 虚拟机组弹窗展示：无虚拟机组
                    虚拟机组拖动
                        交互说明
                            交互说明：虚拟机组未选中时default--> 选中变为 active-->拖拽时额外展示一个 drag 状态的选项漂浮上方--->移到目标位置松开变为 default
                            Tree Item 说明 - 需在 spacer 右侧，Caret 左侧展示 draggable icon（default 状态下隐藏）；增加 drag 状态
                            Drag indicator - 的展示位置将预示移动位置检查：移动位置为当前项的平级
                            Drag indicator - 的展示位置将预示移动位置检查：移动位置为当前项的子级
                            Drag indicator - 的展示位置将预示移动位置检查：移动位置为当前项的父级
                            当拖拽项与当前项水平位置差距在 -32px 至 +32px 以内时 - 移动位置为当前项的平级：目前不支持自定义排序，平级移动无效 只能看到 移动线 drag
                            当拖拽项与当前项水平位置差距在 大于 +32px 以内时 - 移动位置为当前项的子级：L2 向右移动为L3 变为之前的子级组
                            当拖拽项与当前项水平位置差距小于 -32px 时， 且当前项下方没有平级项 - 移动位置为当前项的父级且没有展开子级项时 - 移动位置为当前项的父级:L3 向左水平移动为 L2 层级
                            移动时支持目标组停留2s自动展开子级：移动其他组到当前项未展开子级项时，移动项鼠标在此组状态停留超过 2s，则自动展开子级项
                            当前项A展开子级项情况下，无论水平位置如何，都仅能将拖拽项A01移动至当前项A组内的A02/3的子级，不可移动至平级或父级
                            当拖拽项与当前项下一项的垂直位置重合时，在当前项的下方展示 drag indication，直至拖拽项与当前项重合
                            名称顺序-按照ACSII 排序与左侧边栏一致
                        场景测试
                            降低层级：将3级虚拟机组（不含子组），移动为其他2级组的子组
                            降低层级：将3级虚拟机组（含子组L4/5），移动为其他3机组的子组 - 层级超过5级禁止移动
                            提成层级：将3级虚拟机组（含子组L4/5），移动为2级组 - 该组及其子组移动成功
                            平级移动：将3级虚拟机组（含子组L4/5），移动为其他2级组的子组 - 该组及其子组移动成功
                            跨L1级组移动：平级移动：将3级虚拟机组（含子组L4/5），移动为其他1机组下2级组的子组 - 该组及其子组移动成功
                            同一层级虚拟机组不支持自定义排序，预期名称按 ACSII 排序
                            检查虚拟机组变更层级后 - 左侧边栏虚拟机数量统计正确
                            虚拟机组层级移动后 - 左侧菜单栏虚拟机计数统计存在延迟 - 产品研发确认延迟符合预期
                            将虚拟机组移动到同名虚拟机组相同层级 - 校验同一层级不能重复
                            在不同层级下创建/移动同名虚拟机机组 - 可正常使用同名虚拟机组
                虚拟机
                    创建虚拟机
                        各方式创建 vm 入口 - 增加选择所属虚拟机组入口 - 增加「（选填）」后缀；弹窗具备拖拽、创建功能（若用户无虚拟机组编辑权限，则隐藏这两个功能）
                        创建vm. - 选择所属虚拟机组（右侧规格配置栏展示所属组） - 新建虚拟机组 - 创建vm 成功，虚拟机所属组展示正确
                        模版创建vm. - 选择所属虚拟机组（右侧规格配置栏展示所属组） - 使用已有虚拟机组 - 创建vm 成功，虚拟机所属组展示正确
                        克隆创建vm - 选择所属虚拟机组（右侧规格配置栏展示所属组） - 新建虚拟机组 - 创建vm 成功，虚拟机所属组展示正确
                        快照重建vm. - 选择所属虚拟机组（右侧规格配置栏展示所属组） - 使用已有虚拟机组 - 创建vm 成功，虚拟机所属组展示正确
                        ovf 导入创建vm. - 选择所属虚拟机组（右侧规格配置栏展示所属组） - 使用已有虚拟机组 - 创建vm 成功，虚拟机所属组展示正确
                        创建vm 过程中 虚拟机组使用 - 选择集群前，禁用虚拟机组按钮
                        创建vm 过程中 虚拟机组使用 - 选择集群后，解除禁用虚拟机组按钮
                        创建vm 过程中 虚拟机组使用 - 虚拟机组弹窗符合预期与其他入口一致
                        使用时的虚拟组时路经检查 -  固定最多展示三个虚拟机组名称，若层级多于三级，则前面的组固定省略并展示为 .../，hover 展示完整名称；若虚拟机组名称仍旧过长，则在后打点截断
                        使用时的虚拟组时路经检查 - 名称过长存在省略时，需展示完整名称 tooltip
                        使用时的虚拟组时路经检查 - 再次打开「选择虚拟机组」弹窗 并已选中当前选中组（需展开选中组的父级项）
                        主机视图 - 虚拟机详情 - 「所属组」字段展示完整路径；跳转行为和原行为保持一致：点击后跳转至对应虚拟机组的虚拟机列表页 - 左侧导航栏为当前集群
                        虚拟机组视图 - 虚拟机详情 - 「所属组」字段展示完整路径；跳转行为和原行为保持一致：点击后跳转至对应虚拟机组的虚拟机列表页 - 左侧导航栏所属虚拟机组
                    迁移
                        集群内
                            smtx os/elf 集群内迁移 - 虚拟机组不改变
                        跨集群
                            smtx elf 集群仅迁移存储 ：smtx elf +zbs 迁移到 smtx elf + os  - 虚拟机组不改变
                            smtx elf 集群仅迁移存储 ：smtx elf +zbs1 迁移到 smtx elf + zbs2  - 虚拟机组不改变
                            smtx elf 集群仅迁移计算 ：smtx elf1+zbs 迁移到 smtx elf2 + zbs  - 迁移后目标端不分组
                            smtx os 跨集群热迁移 到 os - 迁移后目标端不分组
                            smtx os 跨集群热迁移 到 smtx elf+os/zbs - 迁移后目标端不分组
                            smtx elf+ os/zbs  跨集群热迁移 到 smtx os - 迁移后目标端不分组
                            smtx os 跨集群分段迁移 到 os - 迁移后目标端不分组
                            smtx os 跨集群冷迁移 到 os - 迁移后目标端不分组
                    虚拟机列表 - 所属组
                        组织架构级别 - 虚拟机列表 - 列选项：所属组 - 展示虚拟机组的完整路径，未分组展示为「-」- csv 导出文件符合预期
                        数据中心级别 - 虚拟机列表 - 列选项：所属组 - 展示虚拟机组的完整路径，未分组展示为「-」- csv 导出文件符合预期
                        可用域级别 - 没有虚拟机列表
                        集群级别 - 虚拟机列表 - 列选项：所属组 - 展示虚拟机组的完整路径，未分组展示为「-」- csv 导出文件符合预期
                        主机级别 - 虚拟机列表 - 列选项：所属组 - 展示虚拟机组的完整路径，未分组展示为「-」- csv 导出文件符合预期
                报警规则
                    470 预期预期只实现 虚拟机组 path 展示别的没有修改 - 增加虚拟机组的完整路径展示，最多展示两行 路径超过长度则打点截断，hover 展示完整路
                事件记录
                    创建虚拟机 - 事件记录为：创建虚拟机 {{虚拟机名称}}，描述如下：
虚拟机组：{{组完整目录}}
                    创建虚拟机组 - 事件记录为：创建虚拟机组{{组完整目录}}
                    编辑虚拟机组名称 - 事件记录为：创建虚拟机组{{组完整目录}}
                    编辑虚拟机组层级结构 - 事件记录为：移动虚拟机组 {{组完整目录}} 至 {{组完整目录}}。
                    删除虚拟机组 -事件记录为：删除虚拟机组{{组完整目录}}
                    报警信息事件中展示虚拟机组
                    虚拟机加入虚拟机组 - 事件记录为：将虚拟机{{虚拟机组}}加入虚拟机组{{组完整目录}}。
                    虚拟机移出虚拟机组 - 事件记录为：将虚拟机{{虚拟机名}}从虚拟机组{{组完整目录}}移出。
                    变更虚拟机所属组 - 事件记录为：将虚拟机 {{虚拟机名}} 从虚拟机组 {{组完整目录}} 移动到组 {{组完整目录}}。
                报表管理 - 资产列表
                    在「虚拟机」报表中可查看虚拟机所属组 - 多级嵌套，展示格式为「父虚拟机组/子虚拟机组..」展示完成目录
                角色权限
                    [基础设施 - 虚拟机] 权限 角色 - smtx os 分配 - 虚拟机组管理权限 - 可操作虚拟机 移至组内
                    [基础设施 - 虚拟机] 权限 角色 - smtx elf 分配 - 虚拟机组管理权限 - 可操作虚拟机 从组中移除
                    [基础设施 - 虚拟机] 权限 角色 - 不可操作虚拟机组 - 创建/编辑/删除权限
                    「运维管理和设置-集群级别-虚拟机组」权限角色 - 分配 - 虚拟机组权限 - 可操作创建虚拟机组
                    「运维管理和设置-集群级别-虚拟机组」权限角色 - 分配 - 虚拟机组权限 - 可操作编辑虚拟机组名称
                    「运维管理和设置-集群级别-虚拟机组」权限角色 - 分配 - 虚拟机组权限 - 可操作编辑虚拟机组层级结构
                    「运维管理和设置-集群级别-虚拟机组」权限角色 - 分配 - 虚拟机组权限 - 可操作删除虚拟机组
                    「运维管理和设置-集群级别-虚拟机组」权限角色 - 不可操作虚拟机所属组权限
                    拥有 [基础设施 - 虚拟机]  + 「运维管理和设置-集群级别-虚拟机组」权限角色  - 可编辑虚拟机所属组、可创建/编辑/删除 虚拟机组
                故障场景
                    smtx os 集群失联时 -  graphql 操作创建/删除/移动虚拟机组、编辑虚拟机所属组 - 创建成功
                    smtx elf 集群失联时 -  graphql 操作创建/删除/移动虚拟机组、编辑虚拟机所属组 - 创建成功
                    smtx elf +zbs/os，存储集群失联时 - UI 操作编辑虚拟机所属组 - 创建组/移动至其他组/移出组成功
                    smtx os 集群 license 过期时 - UI 可操作 - 操作创建/删除/移动虚拟机组、编辑虚拟机所属组 - 创建成功
                    smtx elf 集群 license 过期时 -UI 可操作 - 操作创建/删除/移动虚拟机组、编辑虚拟机所属组 - 创建成功
                    smtx elf +zbs/os，存储集群 license 过期时 -UI 可操作 - 操作编辑虚拟机所属组 - 创建成功
                    smtx elf + zbs 集群，zbs 集群未关联到 tower - 操作编辑虚拟机所属组 - 创建成功
                470 不支持 skip
                    虚拟机多选---skip 470 不支持
                        交互说明
                            与 AntD Tree 应用场景不同的是，checked 仅代表选中当前项（为了用户使用方便，提供选中父级-自动选中所有子孙项的交互，但是保留仅选中父级项的能力）；-- 什么能力移动？
                            此处计数展示的非子级项个数，而是虚拟机组内虚拟机的个数（不包括子虚拟机组内的虚拟机）；
                            在末尾展示当前集群中的「未分组虚拟机」？？？？
                            多选时支持拖动吗？
                        场景测试：
                            选择包含子组的虚拟机组时 - 勾选父项会自动展开所有子孙项，并 勾选 所有子孙项
                            选择包含子组的虚拟机组时 - 取消勾选会父项组，会取消勾选 所有子孙项
                            勾选第5层子项 - 会联动该子项勾选L1/2/3/4父项？？- 但不会勾选各层级父项中的其他子项
                            勾选第5层子项 - 会联动该子项勾选L1/2/3/4父项 - 取消勾选第 5层子项，不会取消各上层父项的勾选？？
                            检查组内虚拟机计数 - 只有在多选场景下展示计数：展示组内虚拟机数量（不含子组）--多选未支持不检查 skip
                            检查：多选按钮 - 选中虚拟机组后才展示多选按钮，选中时选展示为✅--skip
                    报警规则--skip 470 不支持
                        自定义报警规则 - 报警对象 - 虚拟机组 - 选单个虚拟机组
                        自定义报警规则 - 报警对象 - 虚拟机组 - 选多个虚拟机组
                        自定义报警规则 - 报警对象 - 虚拟机组 - 选未分组虚拟机组
                        自定义报警规则页面检查 - 检查报警规则详情 - 展示虚拟机组的完整路径，省略及打点规则同上，hover 展示完整名称 tooltip
                        自定义报警规则列表 - 配置下发失败的提示 - 展示虚拟机组的完整路径
                        报警规则筛选页面，报警对象可按虚拟机组筛选
                版本覆盖
                    tower 低版本升级至 470 后 - 集群  - 有470 版本完整虚拟机组功能 - 集群增加虚拟机组入口、可看到升级前已有的虚拟机组
                    检查smtx os 3.x、4.x、5.x、6.x + tower 470  新增支持虚拟机组功能正常
                    检查AOC os + ACOS  tower 470  新增支持虚拟机组功能
                    中文界面功能检查符合预期
                    英文界面功能检查符合预期
                资源导航器与列表
                    页面导航栏
                        创建
                            各层级创建虚拟机组
                                入口规则
                                    入口：虚拟机组视图 - 集群层级 - 虚拟机组 - 虚拟机列表页面 - 新建资源，展示第三项是：创建虚拟机组 项
                                    入口：虚拟机组视图 - 集群层级 - 虚拟机组 - 子虚拟机组
-  新建资源，展示第一项是：创建虚拟机组 项
                                    入口：集群层级 - 虚拟机组是「未分组」时，隐藏：创建虚拟机组 项
                                    入口：集群层级 - 虚拟机组页面，虚拟机组是「L5 层级虚拟机组」时，隐藏：创建虚拟机组 项
                                校验
                                    创建多级虚拟机组 - 检查子组上限为 4层，含父组共 5 层
                                    检查第一层级虚拟机组，字符长度：1-255
                                    检查子组虚拟机组，字符长度：1-255
                                    检查第一层级虚拟机组，非法字符集：不允许输入特定字符：（%, &, *, $, #, @, !, \, /, :, *, ?, ", <, >, |, ;, '） - 输入有校验提示无法保存
                                    检查子组虚拟机组，非法字符集：不允许输入特定字符：（%, &, *, $, #, @, !, \, /, :, *, ?, ", <, >, |, ;, '） - 输入有校验提示无法保存
                                    检查第一层级虚拟机组，不能创建相同名称的第一层级组- 创建同名时，有校验提示无法保存
                                    检查子组虚拟机组，不能在同一层级创建相同名称的子组- 创建同名时，有校验提示无法保存
                                    检查虚拟机组，不在同一层级创建相同名称的组- 创建成功，如1、2、3、4、5 层级全部同名成功--可以吗，需要校验吗
                                    检查创建符合长度、字符集的虚拟机组；父、子组成功
                        编辑
                            入口 - 集群 - 虚拟机组 - 各层级虚拟机组列表 - 指定虚拟机组 - 【…】中编辑名称 - 遵循名称长度、字符集、同名校验
                            入口 - 集群 - 更层级虚拟机组 - 右上角编辑：编辑名称、编辑层级结构
                            无权限时，隐藏整个「编辑」入口；
                            虚拟机组为「未分组」时，隐藏整个「编辑」入口
                            虚拟机组 - 右上角编辑名称 - 遵循名称长度、字符集、同名校验
                            编辑层级结构 - 即使用拖动功能编辑层级结构（拖动相关用例中检查）
                        删除虚拟机组
                            无虚拟机组编辑权限时，隐藏 more button；
                            入口 - 集群 - 虚拟机组 - 各层级虚拟机组列表 - 指定虚拟机组 - 【…】中删除虚拟机组
                            入口 - 集群 - 更层级虚拟机组 - 右上角编辑【…】中删除虚拟机组
                            当前组中均无虚拟机 - 删除成功 - 提示 删除虚拟机组 %group-name% 成功，页面跳转到 当前集群的虚拟机组列表页面
                            当前组有及其子孙虚拟机组中均无虚拟机 - 提示 删除虚拟机组 %group-name% 以及子虚拟机组成功，页面跳转到 当前集群的虚拟机组列表页
                            当前组及其子孙虚拟机组中存在虚拟机，展示回绝弹窗 - 显示虚拟机及虚拟机组关系对照：展示虚拟机组的路径（从删除组开始）；虚拟机组中的虚拟机，超过 2 个时，展示 .......
                            并发删除虚拟机组与虚拟机组内创建vm 并发 - 触发兜底校验：删除虚拟机组失败 - 虚拟机组或其子组内存在虚拟机。--graphql 触发
                        路径展示
                            面包屑展示当前虚拟机组的完整路径
                            虚拟机组名称过长时，路径展示正确，完整展示（沿用之前设计设计稿已修改）
                    资源导航
                        左侧边栏 - 虚拟机组视图
                            固定首层层级缩进 - 16px
                            每个层级递进缩进 20px
                            折叠状态 - 点击则展开/收起子组，hover 与点击特效与集群层保持一致；若无子组则不展示此部分。
                            虚拟机组名称 - 名称过长时打点截断 - 当前导航栏最小宽度为 200px（已有定义），文字过长时沿用当前的打点截断定义
                            Extra Indent 缩进 - 虚拟机组下层 - 若无子组，则需展示额外缩进 20px。
                            虚拟机数量 计数缩进 - 计数缩进
                            计数展示：当前组及所有子组下的虚拟机总数 - 如：L1 层级展示的vm 总数=L1下虚拟机数 + 各子组虚拟机数量
                            集群层级 - 会展示未分组虚拟机 - 虚拟机组层级不涉及未分组状态
                            检查 5层虚拟机群组 - 左侧边栏展示正确
                            检查 - 有子虚拟机组，无计数 - UI 展示
                            检查 - 有子虚拟机组，有计数
                            检查 - 无子虚拟机组，无计数 - UI 展示
                            检查 - 无子虚拟机组，有计数 - UI 展示
                            回归测试：检查主机视图个层级 - 缩进正常
                            L1 层级展示的vm 总数=L1下虚拟机数 + 各子组虚拟机数量
                    虚拟机组 - 虚拟机列表
                        展示子虚拟机组中所有虚拟机
                            虚拟机组视图 - 左侧边栏：切换到集群虚拟机组（非 L5） - 展示虚拟机和子虚拟机组 标签页
                            虚拟机组视图 - 左侧边栏：切换到集群虚拟机组（L5） - 只展示虚拟机标签页
                            虚拟机组视图 - 左侧边栏：切换到集群虚拟机组 - 虚拟机列表 - 新增项：是否展示子虚拟机组中虚拟机，默认不勾选
                            虚拟机组视图 - 左侧边栏：切换到集群虚拟机组 - 虚拟机列表 - 勾选展示子虚拟机组中虚拟机 - 勾选后展示当前虚拟机组中的所有虚拟机（包括所有子虚拟机组中的虚拟机)
                            虚拟机组视图 - 左侧边栏：切换到集群虚拟机组 - 虚拟机列表 - 未勾选展示子虚拟机组中虚拟机 - 勾选后展示当前虚拟机组中的所有虚拟机（不包括所有子虚拟机组中的虚拟机）
                            虚拟机组视图 - 左侧边栏：切换到集群未分组 - 虚拟机列表 - 不展示子虚拟机组 项
                        虚拟机组层级的虚拟机列表「所属组」
                            虚拟机组层级的虚拟机列表增加「所属组」字段，其他层级的「所属组」字段需修改展示方式
                            固定最多展示两个虚拟机组名称，若层级多于两级，则前面的组固定省略并展示为 .../，hover 展示完整名称；若虚拟机组名称仍旧过长，则在后打点截断
                            若没有所属组，则展示为「-」
                            虚拟机所属组 ：字符较长含省略或打点截断 - 鼠标悬浮展示完整路径，点击后跳转至对应虚拟机组的虚拟机列表页面后可跳转
                        移至组与移出组
                            虚拟机组 - 视图检查
                                虚拟机列表 - 未分组的单个虚拟机 - 【…】编辑虚拟机组 - 已有虚拟机组
                                虚拟机列表 - 未分组多个虚拟机 - 【…】编辑虚拟机组 - 新建虚拟机组
                                虚拟机列表 - 已分组的单个虚拟机 - 【…】编辑虚拟机组 - 自动选中虚拟机当前所在组，并展开当前组的所有父级项和一级子级项 - 触发更新单个vm 的任务
                                虚拟机列表 - 在同一个分组的多个虚拟机 - 【…】批量编辑虚拟机组 - 自动选中虚拟机当前所在组，并展开当前组的所有父级项和一级子级项 - 触发更新多个vm 的任务
                                虚拟机列表 - 在不同分组的多个虚拟机 - 【…】批量编辑虚拟机组 - 平铺展示当前集群下所有 L1 虚拟机组 - 触发更新多个vm 的任务
                                移动组时 - 拖拽当前分组变更位置 - 分组变更位置成功，虚拟机更新分组成功
                                移动组时 - 更新新创建分组 - 新增分组成功，虚拟机更新分组成功
                                虚拟机列表 - 【…】移出虚拟机组弹窗更新 - L1/2/3/4/5层级使用新 UI
                                单个虚拟机移出组 - 触发弹窗提示：提示中展示完整路径 - 移出组成功
                                批量vm 移出组 - 若所选虚拟机均属于同一组，则展示虚拟机当前所在组的路径 - 移出组成功
                                批量vm 移出组 - 若所选虚拟机均属于不同组，则不展示路径 - 移出组成功
                                若所选虚拟机：为分组 +已分组 - 批量vm 移出组项不展示
                            主机 - 视图检查
                                虚拟机列表 - 未分组的单个虚拟机 - 【…】编辑虚拟机组 - 已有虚拟机组
                                虚拟机列表 - 未分组多个虚拟机 - 【…】编辑虚拟机组 - 新建虚拟机组
                                虚拟机列表 - 已分组的单个虚拟机 - 【…】编辑虚拟机组 - 自动选中虚拟机当前所在组，并展开当前组的所有父级项和一级子级项 - 触发更新单个vm 的任务
                                虚拟机列表 - 在同一个分组的多个虚拟机 - 【…】批量编辑虚拟机组 - 自动选中虚拟机当前所在组，并展开当前组的所有父级项和一级子级项 - 触发更新多个vm 的任务
                                虚拟机列表 - 在不同分组的多个虚拟机 - 【…】批量编辑虚拟机组 - 平铺展示当前集群下所有 L1 虚拟机组 - 触发更新多个vm 的任务
                                移动组时 - 拖拽当前分组变更位置 - 分组变更位置成功，虚拟机更新分组成功
                                移动组时 - 更新新创建分组 - 新增分组成功，虚拟机更新分组成功
                                虚拟机列表 - 【…】移出虚拟机组弹窗更新 - 组织架构/数据中心/集群/主机层级使用新 UI
                                单个虚拟机移出组 - 触发弹窗提示：提示中展示完整路径 - 移出组成功
                                批量vm 移出组 - 若所选虚拟机均属于同一组，则展示虚拟机当前所在组的路径 - 移出组成功
                                批量vm 移出组 - 若所选虚拟机均属于不同组，则不展示路径 - 移出组成功
                                若所选虚拟机：为分组 +已分组 - 批量vm 移出组项不展示
                        导出 csv
                            虚拟机组视图 - 虚拟机组- 虚拟机列表 - 不勾选子虚拟机 - 下载 csv 文件，符合预期不包含子虚拟机组vm - 所属组：展示虚拟机组path
                            虚拟机组视图 - 虚拟机组- 虚拟机列表 - 勾选子虚拟机 - 下载 csv 文件，符合预期包含子虚拟机组vm - 所属组：展示虚拟机组path
                            虚拟机组视图 - 未分组虚拟机- 虚拟机列表  - 下载 csv 文件，符合预期包含未分组所有 vm  - 所属组 展示为 空
                    虚拟机组列表
                        虚拟机组视图
                            列表
                                集群 - 未分组 页面 - 不展示虚拟机组 tab ,只有 虚拟机列表 tab
                                集群 - L5层级虚拟机组 页面 - 不展示虚拟机组 tab ,只有 虚拟机列表 tab
                                集群 - 虚拟机组 - 默认不勾选：展示子虚拟机组中所有虚拟机组
                                集群 - 虚拟机组 - 若虚拟机组内没有子虚拟机组则不展示 - 勾选框：展示子虚拟机组中所有虚拟机组
                                集群 - 虚拟机组 - 勾选后平铺展示当前虚拟机组中的所有虚拟机组（包括所有子虚拟机组中的虚拟机组）
                                虚拟机组列表 - 名称 - 是 字符串类型、列选项默认展示、支持排序、筛选、默认宽度160px
                                虚拟机组列表 - 名称 - 支持交互：hover 变蓝，点击后跳转至对应虚拟机组的虚拟机列表页面
                                虚拟机组列表 - 组目录 - 是 字符串类型、列选项默认展示、支持排序、筛选、默认宽度240px，不支持交互
                                虚拟机组列表 - 虚拟机数量 - 是 数值类型、列选项默认展示、支持排序、筛选、默认宽度100px，不支持交互
                                虚拟机组列表 - 指定虚拟机组 - 「…」编辑虚拟机组名称 - 打开虚拟机组名称弹窗，虚拟机组名称遵循校验：同层级不能同名、支持1-255字符、符合字符集校验 - 重命名成功
                                虚拟机组列表  - 指定虚拟机组 - 「…」- 删除 - 打开「删除虚拟机组」弹窗
                                无虚拟机组编辑权限时 - 虚拟机组列表  - 指定虚拟机组 - 隐藏 more button 「…」
                                列选项可取消展示  - 取消展示：组目录、虚拟机数量成功
                            筛选
                                虚拟机组：名称、组目录、虚拟机数量 支持筛选
                                筛选不到符合要求的数据 - 页面展示：没有匹配到的对象，并展示清空按钮 - 点击清空筛选规则
                                筛选虚拟机组的名称：”包含“指定定字符 - 筛选数据正确成功
                                筛选虚拟机组的名称：“不包含” 指定字符 - 筛选数据正确成功
                                筛选虚拟机组的组目录：”包含“ 指定字符 - 筛选数据正确成功
                                筛选虚拟机组的组目录：”不包含“ 指定字符 - 筛选数据正确成功
                                筛选虚拟机数量： >= 指定数值的虚拟机组 -  筛选数据正确成功
                                筛选虚拟机数量： > 指定数值的虚拟机组 -  筛选数据正确成功
                                筛选虚拟机数量： = 指定数值的虚拟机组 -  筛选数据正确成功
                                筛选虚拟机数量： < 指定数值的虚拟机组 -  筛选数据正确成功
                                筛选虚拟机数量： < = 指定数值的虚拟机组 -  筛选数据正确成功
                                虚拟机组的名称、组目录组合筛选正确
                                虚拟机组的名称、虚拟机数量组合筛选正确
                                虚拟机组的组目录、虚拟机数量组合筛选正确
                                虚拟机组的名称、组目录、虚拟机数量组合筛选正确
                                不勾选 ：展示子虚拟机组中所有虚拟机组 - 筛选正确
                                勾选 ：展示子虚拟机组中所有虚拟机组 - 筛选正确
                                全部留空时筛选展示默认的所有数据
                            导出 csv
                                虚拟机组默认展示数据 - 导出 数据正确
                                勾选展示自虚拟机组中所有虚拟机组 - 导出数据正确
                                筛选数据后导出 - 导出数据正确与筛选一致
                                列选项可取消展示组目录、虚拟机数量 - 导出文件仍包含所有列选项：名称、组目录、虚拟机数量
                        主机视图 - 新增虚拟机组 tab
                            虚拟机组列表 - 默认展示：名称、组目录、虚拟机数量 - 不勾选展示子虚拟机组中所有虚拟机组，字段均支持排序、筛选
                            主机视图虚拟机组 - 集群层级虚拟机组 - 只有创建入口，没有编辑名称/层级机构入口
                            L1 层级虚拟机组 导出 csv 文件正确
                            L1 层级虚拟机组 数据是筛选符合预期
                            虚拟机组列表 - 勾选展示子虚拟机组中所有虚拟机组，虚拟组数据名称、组目录、虚拟机数量 正确，虚拟机组总数正确
                    主机视图 与 虚拟机组视图切换交互检查
                        主机视图 组织架构层级在虚拟机列表 tab 时 - 点击列选项/vm 详情：所属组后 - tab 展示虚拟机所属组的虚拟机列表 - 左侧边栏选中当前虚拟机所属集群
                        主机视图 数据中心层级在虚拟机列表 tab 时 - 点击列选项/vm 详情：所属组后 - tab 展示虚拟机所属组的虚拟机列表 - 左侧边栏选中当前虚拟机所属集群
                        主机视图 集群层级在虚拟机列表 tab 时 - 点击列选项/vm 详情：所属组后 - tab 展示虚拟机所属组的虚拟机列表 - 左侧边栏选中当前虚拟机所属集群
                        主机视图 主机层级在虚拟机列表 tab 时 - 点击列选项/vm 详情：所属组后 - tab 展示虚拟机所属组的虚拟机列表 - 左侧边栏选中当前虚拟机所属集群
                        主机视图 集群层级在虚拟机列表 tab 时 - 点击列选项/vm 详情：所属组后 - tab 展示虚拟机组虚拟机列表 - 主机视图 切换为 虚拟机组视图，预期：切换后左侧边栏选中当前虚拟机所属虚拟机组
                        主机视图 集群层级 L1 层级虚拟机组 tab 时，将主机视图 切换为 虚拟机组视图，预期：切换后左侧边栏选中当前集群
                        主机视图 集群层级在L2/3/4 子虚拟机组 tab 时，将主机视图 切换为 虚拟机组视图，预期：切换后左侧边栏选中当前虚拟机组
                        主机视图 集群层级在L1/2/3/4/5 子虚拟机组虚拟机列表 tab 时，将主机视图 切换为 虚拟机组视图，预期：切换后左侧边栏选中当前虚拟机所属虚拟机组
                        虚拟机组视图 集群层级 L1 层级虚拟机组 tab 时，将虚拟机组视图 切换为 主机视图，预期：切换后左侧边栏选中当前集群
                        虚拟机组视图 集群层级 L2/3/4 层级虚拟机组 tab 时，将虚拟机组视图 切换为 主机视图，预期：切换后左侧边栏选中当前集群
                        虚拟机组视图 集群层级在L1/2/3/4/5 子虚拟机组虚拟机列表 tab 时，将虚拟机组视图 切换为 主机视图，预期：切换后左侧边栏选中当前虚拟机所属集群
            TOWER-18370  创建常驻缓存卷与集群常驻缓存配置并发 - 校验优化
                新增 "ec":"UPriorVolumeExistedWhenDisablePriorInCluster" - “集群内存在启用常驻缓存的卷” - 场景：并发 集群关闭常驻缓存 与 创建常驻缓存卷任务 - 创建常驻缓存卷先结束时，编辑集群常驻缓存设置触发
                新增 "ec":"UInsufficientPrsWhenDecreasePlannedPrs"- “集群预留常驻缓存容量需大于常驻缓存已使用容量。” - 场景：并发 集群降低常驻缓存容量 与 创建常驻缓存卷 - 创建常驻缓存卷先结束时，编辑集群常驻缓存设置触发
                已有  "error_code":"ENoPrioSpace" -  “集群空闲预留缓存容量不足。” - 场景：并发 集群关闭常驻缓存 与 创建常驻缓存卷 - 集群关闭常驻缓存进行中，创建常驻缓存卷任务先结束时，创建常驻缓存卷触发
                已有 "ec":"PRECHECK_CLUSTER_RESIDENT_VOLUME_INACTIVE" - “集群未启用数据常驻缓存。” - 场景：并发 集群关闭常驻缓存 与 创建常驻缓存卷 - 集群关闭常驻缓存先结束时，创建常驻缓存卷触发
            tower 470 调整内容库模版 target 白名单
                TOWER-13326 内容库模版支持白名单控制访问权限
                    数据检查
                        前后端一致性检查
                            UI 展示 taget：IP 白名单 全部禁止 IQN 白名单自适应 自动保持为所包含 LUN 的 IQN 白名单的并集; --- 对应 zbs target 配置为 Whitelist ：“” 、IQN Whitelist  “ */*”、Adaptive IQN Whitelist：True
                            UI 展示 lun ：IQN 白名单 全部允许--- 对应 zbs target 配置为 Allowed Initiators：“ */* ”、Single Access ：“False”
                        内容库模版 target /lun 检查方式
                            获取内容库模版id - tower 内容库 - 查看模版详情 - 模版 url 结尾 uuid 是内容库模版 id
                            graphql 查询：使用模版 id 查询 contentLibraryVmTemplates - 获取zbs 模版的 zbs 存的zbs_storage_info.iscsi_lun_snapshot_uuid
                            graphql 查询：使用 iscsi_lun_snapshot_uuid 在 iscsiLunSnapshots 查询 - 获取 该 zbs 模版的 target name、lun_name
                            tower - zbs 集群 - target ：查询 zbs 模版对应的 target 白名单配置 - target IP 白名单 全部禁止 IQN 白名单自适应 自动保持为所包含 LUN 的 IQN 白名单的并集;
                            tower - zbs 集群 - target  - lun ：查询 zbs 模版对应的 lun 白名单配置 - lun IQN 白名单 全部允许
                            zbs 查询 target 白名单配置：zbs-iscsi  target show <target_name>
                            zbs 查询 lun 白名单配置：zbs-iscsi  lun show <target_name> <lun_id>  （lun_id 可以在 towerzbs 集群 lun 详情查看到 ）
                    模版创建
                        elf+zbs 570 新建vm - 克隆为模版 - 预期新建  taget：IP 白名单 全部禁止 IQN 白名单 自适应 自动保持为所包含 LUN 的 IQN 白名单的并集; lun：IQN 白名单 全部允许
                        elf+zbs 563 新建vm -克隆为模版 - 预期新建  taget：IP 白名单 全部禁止 IQN 白名单 自适应 自动保持为所包含 LUN 的 IQN 白名单的并集; lun：IQN 白名单 全部允许
                        elf+zbs 570 新建vm - 转化为为模版 - 预期新建  taget：IP 白名单 全部禁止 IQN 白名单 自适应 自动保持为所包含 LUN 的 IQN 白名单的并集; lun：IQN 白名单 全部允许
                        elf+zbs 563 新建vm - 转化为模版 - 预期新建  taget：IP 白名单 全部禁止 IQN 白名单 自适应 自动保持为所包含 LUN 的 IQN 白名单的并集; lun：IQN 白名单 全部允许
                        ovf 导入 虚拟机模版到 zbs 570 集群 - 预期新建 taget：IP 白名单 全部禁止 IQN 白名单 自适应 自动保持为所包含 LUN 的 IQN 白名单的并集; lun：IQN 白名单 全部允许
                        ovf 导入 虚拟机模版到 zbs 563 集群 - 预期新建 taget：IP 白名单 全部禁止 IQN 白名单 自适应 自动保持为所包含 LUN 的 IQN 白名单的并集; lun：IQN 白名单 全部允许
                        elf+os 新建vm - 克隆为模版 - 查询zbs后端，预期 taget：Whitelist <集群所有主机 hostname ip>，
IQN Whitelist默认 “*/*” ; lun：查询不到（该lun 是模版源虚拟机的lun,该源虚拟机是elf+os 创建模版的临时虚拟机已删除，所以查询不到lun ）-- 已有逻辑
                        elf+os 新建vm - 转化为模版 - 查询zbs后端，预期 taget：Whitelist <集群所有主机 hostname ip>，
IQN Whitelist默认 “*/*” ; lun：查询不到（该lun 是模版源虚拟机的lun,该源虚拟机是elf+os 创建模版的临时虚拟机已删除，所以查询不到lun ）-- 已有逻辑
                        os 集群创建的虚拟机模版 - 查询zbs后端，预期 taget：Whitelist <集群所有主机 hostname ip>， IQN Whitelist默认 “*/*” ; lun：Allowed Initiators :"*/*" ,Single Access :False(与源虚拟机iscsi path 一致，源虚拟机删除就查不到lun) -- 已有逻辑
                    模版使用
                        模版分发并创建
                            elf+zbs570 新建虚拟机模版 - 在 elf+zbs570 创建虚拟机成功，开机正常访问系统
                            elf+zbs 570 新建虚拟机模版 - 在 elf+zbs563 创建(含分发)vm成功，可开机正常访问系统，zbs 563 模版 target /lun白名单正确
                            elf+zbs 570 新建虚拟机模版 - 在 elf+os 创建(含分发)vm成功，可开机正常访问系统，os 模版 target /lun白名单正确 - 继续在 smtx os 集群创建 vm 可正常开机访问系统
                            elf+os 新建虚拟机模版 - 在 elf+zbs70 创建(含分发)vm成功，可开机正常访问系统，zbs 570 模版 target /lun白名单正确
                            tower470 前已存储在 elf+zbs 563 虚拟机模版 - 在 elf+zbs570 创建(含分发)vm成功，可开机正常访问系统，zbs 570 模版 target /lun白名单正确
                            tower470 前已存储在 elf+os 虚拟机模版 - 在 elf+zbs563 创建(含分发)vm成功，可开机正常访问系统，zbs 570 模版 target /lun白名单正确
                            elf+zbs 570 新建虚拟机模版 - 在 smtx os 创建(含分发) vm， 可正常开机访问系统 -  继续在 elf+smtx os 集群创建 vm 可正常开机访问系统
                        编辑模版所属集群
                            elf+zbs 570 新建虚拟机模版，分发到 zbs563 - 预期使用 zbs563 已新建的  taget：IP 白名单 全部禁止 IQN 白名单 自适应 自动保持为所包含 LUN 的 IQN 白名单的并集; lun：IQN 白名单 全部允许
                            elf+zbs 563 新建虚拟机模版，分发到zbs 570 - 预期 zbs570 已新建的 taget：IP 白名单 全部禁止 IQN 白名单 自适应 自动保持为所包含 LUN 的 IQN 白名单的并集; lun：IQN 白名单 全部允许
                            elf+zbs 563/570 新建虚拟机模版，分发到 os 成功 - os UI 不展示target/lun，查询zbs后端，预期 taget：Whitelist <集群所有存储节点>， IQN Whitelist默认 “*/*” ; lun：查询不到（该lun 是模版源虚拟机的lun,该源虚拟机是elf+os 创建模版的临时虚拟机已删除，所以查询不到lun ）
                            elf+os 新建虚拟机模版，分发到zbs 570/563 - 预期 使用已 新建的 taget：IP 白名单 全部禁止 IQN 白名单 自适应 自动保持为所包含 LUN 的 IQN 白名单的并集; lun：IQN 白名单 全部允许
                            tower470 前已存储在 os 和 zbs 563 虚拟机模版，分发到 zbs570/563 - 预期新建 taget：IP 白名单 全部禁止 IQN 白名单 自适应 自动保持为所包含 LUN 的 IQN 白名单的并集; lun：IQN 白名单 全部允许
                            tower470 前已存储在 elf+zbs 563 虚拟机模版，分发到 zbs570 - 预期 新建 taget：IP 白名单 全部禁止 IQN 白名单 自适应 自动保持为所包含 LUN 的 IQN 白名单的并集; lun：IQN 白名单 全部允许
                            tower470 前已存储在 elf+zbs 563 虚拟机模版，分发到 smtx os 成功 - os UI 不展示target/lun，查询zbs后端，预期 taget：Whitelist <集群所有存储节点>， IQN Whitelist默认 “*/*” ; lun：查询不到（原因同上 ） 	 ￼
                        模版转化为虚拟机
                            elf+zbs 563 新建虚拟机模版，分发到 zbs570、os - 转化（选保留其他集群上的模版）到 smtx os、elf +zbs570为虚拟机，开机正常访问系统
                            elf+zbs 570 新建虚拟机模版，分发到 zbs563、os - 转化（选保留其他集群上的模版）到 elf+os、elf+zbs563 为虚拟机，开机正常访问系统
                            elf+os 新建虚拟机模版，分发到zbs 570/563 -  转化（选保留其他集群上的模版）到 smtx os、elf+zbs563、elf +zbs570为虚拟机，开机正常访问系统
                            tower470 前已存储在 os 和 zbs 563 虚拟机模版，分发到 zbs570 -  转化（选保留其他集群上的模版）到 smtx os、elf+zbs563、elf +zbs570为虚拟机，开机正常访问系统
                            tower470 前已存储在 elf+zbs 563 虚拟机模版，分发到 zbs570  - 转化（选保留其他集群上的模版）到 smtx elf+zbs563、elf +zbs570为虚拟机，开机正常访问系统
                            tower470 前已存储在 elf+zbs 563 虚拟机模版，分发到 smtx os 成功 - 转化（选保留其他集群上的模版）到 elf+os、elf+zbs563、elf +zbs570为虚拟机，开机正常访问系统
                        删除虚拟机模版
                            删除 tower470+zbs570 新建的集群模版 - 会删除 target 下的lun ，不会删除 target - target 白名单在lun 删除前后保持一致
                            删除 tower 470:elf+os 新建的模版（只有 target 没有lun） - target 白名单不变
                    target 白名单限制有效性检查
                        内容库 zbs： IP 白名单为全部禁止的target  - api\rpc 操作不受限制：api 可在 target 先创建 lun
                        内容库 zbs： IP 白名单为全部禁止的target  - zbs client 不受限制：
                        内容库 zbs： IP 白名单为全部禁止的target - 禁止：iscsi 客户端访问 target
                内容库 ISO 白名单（470 未修改）
                    数据检查
                        内容库 ISO target/lun 检查
                            内容库 ISO - 所属集群，查看graphql: contentLibraryImageClusters - 获取ISO：所属os 集群的 elf_images.id、所属 zbs 集群的 iscsi_luns.id
                            graphql 查询 - os 集群使用 elf_image.id 查询 elfImages - 获取 ISO 存储在os 集群上的 iscsi.path(target/lun_id)、集群信息等
                            graphql 查询 - zbs 集群使用 iscsi_luns.id 查询 iscsiLuns - 获取 lun 对应的 target/lun 白名单、集群信息等
                        前后端一致性检查
                            zbs 内容库iso，UI 展示 taget：IP 白名单 全部允许 IQN 白名单自适应 全部允许; --- 对应 zbs target 配置为 Whitelist ：“*/*” 、IQN Whitelist  “ */*”、Adaptive IQN Whitelist：False
                            zbs 内容库iso，UI 展示 lun ：IQN 白名单 全部允许--- 对应 zbs target 配置为 Allowed Initiators：“ */* ”、Single Access ：“False”
                    470 回归 iso 使用
                        smtx os 620-hp3 集群新上传iso - 检查zbs :target 配置为 Whitelist：<集群所有主机 hostname ip>，IQN Whitelist：“*/*", Adaptive IQN Whitelist  False - 继续分发到zbs563、570 集群：taget、lun 白名单全部允许
                        zbs 570 新上传iso :taget、lun 白名单全部允许 - 继续分发到zbs563、os 集群：taget、lun 白名单全部允许
                        zbs 563 新上传iso :taget、lun 白名单全部允许 - 继续分发到zbs570、os 集群：taget、lun 白名单全部允许
                        tower 470 前 zbs 563 已有 ISO  - 继续分发到zbs570、os 集群：taget、lun 白名单全部允许
                        tower 470 前 os 已有 ISO  - 继续分发到zbs570、563 集群：taget、lun 白名单全部允许
                        elf +zbs 570集群创建vm 挂载iso（从563新上传iso 分发） - 虚拟机创建成功 iso 可正常识别，570zbs iso target/lun 白名单全部允许
                        elf +zbs 570集群创建vm 挂载iso（从os 之前已有 iso 分发） - 虚拟机创建成功 iso 可正常识别，570zbs iso target/lun 白名单全部允许
                    tower 480 - zbs集群修复调整：TOWER-20974 iso target 白名单过滤条件
                        1、tower 上没有带锁的本zbs集群的 target，上传iso
                            上传iso 及使用
                                tower 上没有带锁的本zbs集群的 target，上传iso 自动创建白名单全部允许的、2副本精简制备4条带 target - iso 对应的 lun：白名单全部允许 2副本精简制备 4条带
                                efl+zbs：挂载 iso 开机成功
                                efl+zbs：使用该iso 的 vm，跨集群迁移计算和存储成功，ISO被卸载不影响迁移
                            os 集群 iso 分发到 zbs
                                os 集群的iso 分发到【没有本tower + 集群 target 的zbs】 - 分发的 iso  自动创建白名单全部允许的、2副本精简制备4条带 target - iso 对应的 lun：白名单全部允许 2副本精简制备 4条带
                        2、zbs 只有白名单全部禁用的 target 的集群，集群上传 iso
                            上传iso 及使用
                                zbs 只有白名单全部禁用的 target 的集群，集群上传 iso 没找到  白名单符合要求的 target，触发自动创建 白名单全部允许的、2副本精简制备4条带 target - iso 对应的 lun：白名单全部允许 2副本精简制备 4条带
                                efl+zbs：挂载 iso 开机成功
                                efl+zbs：使用该iso 的 vm，跨集群迁移计算和存储成功，ISO被卸载不影响迁移
                            os 集群 iso 分发到 zbs
                                os 集群的iso 分发到【只有白名单全部禁用的 target 的 zbs 集群】 - 分发的 iso  自动创建白名单全部允许的、2副本精简制备4条带 target - iso 对应的 lun：白名单全部允许 2副本精简制备 4条带
                        3、集群有 target 白名单全部允许、全部禁用的 target 时，集群上传 iso
                            上传iso 及使用
                                集群有 target 白名单全部允许、全部禁用的 target 时，集群上传 iso  - 过滤使用zbs 集群，已有的 白名单为全允许的、2副本精简制备4条带 target - iso 对应的 lun：白名单全部允许 2副本精简制备 4条带
                                efl+zbs：挂载 iso 开机成功
                                efl+zbs：使用该iso 的 vm，跨集群迁移计算和存储成功，ISO被卸载不影响迁移
                            os 集群 iso 分发到 zbs
                                os 集群的iso 分发到【有 target 白名单全部允许、全部禁用的 target的 zbs 集群 】 - 分发的iso 使用zbs 集群：已有的 白名单为全允许的、2副本精简制备4条带 target - iso 对应的 lun：白名单全部允许 2副本精简制备 4条带
                    tower 480 - os集群iso 在存算分离修复调整：TOWER-21426 iso target 白名单
                        在已有错误 白名单的 os 集群上，os 集群 - 新上传 iso ,elf+os 集群使用该 ISO - 检查 内容库 ISO新建【target contentLibraryImages 的 元数据 iscsi_luns 是 白名单全部允许】
                        在已有正确、错误 【contentLibraryImages 的 元数据 iscsi_luns 】的集群上 - 新上传 iso ，elf+os 集群使用 iso - 检查新 iso 使用 正确的 白名单全部允许的 target
            oapi
                oapi 支持配置重建优先级 TOWER-18553
                    创建空白虚拟机
                        创建空白虚拟机配置 HA = true ,ha_priority=高， 创建成功，ha_priority 配置生效
                        创建空白虚拟机配置 HA = true ,ha_priority=中， 创建成功，ha_priority 配置生效
                        创建空白虚拟机配置 HA = true ,ha_priority=低， 创建成功，ha_priority 配置生效
                        创建空白虚拟机配置 HA = false , 配置 ha_priority， 虚拟机创建成功，实际  ha_priority 不生效
                        创建空白虚拟机配置 HA = false , 不配置 ha_priority， 虚拟机创建成功
                    编辑虚拟机
                        ha=false 的虚拟机，编辑为 ha 为 true, 不配置 ha_priority， 编辑成功，编辑后 ha_priority  未配置
                        ha=false 的虚拟机，编辑为 ha 为 true, 且配置 ha_priority， 编辑成功，编辑后 ha_priority  有配置
                        ha=true 且有配置 ha_priority 的虚拟机，编辑为 ha 为 false，编辑成功， 编辑后 HA 关闭
                        ha=true 且有配置 ha_priority 的虚拟机，编辑为 ha 为 true 且 ha_priority = 其他配置值 ，编辑成功， 编辑后  ha_priority 按更新值生效
                    从模版创建虚拟机
                        单任务接口
                            模版配置 ha_priority, 从模版创建虚拟机(单接口创建1个)配置新 ha_priority
                            模版配置 ha_priority, 从模版创建虚拟机(单接口创建2个)配置新 ha_priority
                            从模版创建虚拟机不配置 ha_priority, 单接口创建成功
                        批量任务接口
                            模版配置 ha_priority, 从模版创建虚拟机(批量接口创建1个)配置新 ha_priority
                            模版配置 ha_priority, 从模版创建虚拟机(批量接口创建2个)配置新 ha_priority
                            从模版创建虚拟机不配置 ha_priority, 批量接口创建成功
                    从快照重建虚拟机
                        从快照重建虚拟机不配置 ha_priority， 重建成功，新虚拟机的 ha_priority 和快照一致
                        从快照重建虚拟机配置 ha_priority ， 重建成功，新虚拟机的 ha_priority 按新配置生效
                    从虚拟机克隆虚拟机
                        从虚拟机克隆新虚拟机不配置 ha_priority， 克隆成功，新虚拟机的 ha_priority 和 源虚拟机一致
                        从虚拟机克隆新虚拟机配置新的 ha_priority， 克隆成功，新虚拟机的 ha_priority 生效新配置值
            TOWER-18792 - 低版本集群支持虚拟机「存储使用率」字段
                不展示存储使用率
                    虚拟机详情 - 不展示 存储使用率项
                    虚拟机使用者视图 - 不展示 存储使用率项
                    回收站虚拟机列表  - 不展示 存储使用率项
                    ER 隔离中的虚拟机列表  - 不展示 存储使用率项
                展示存储使用率
                    虚拟卷详情列表
                        虚拟卷详情 - 保持仍有 存储使用率项，不做调整
                        组织架构层级 - 虚拟卷列表- 保持仍有 存储使用率项，不做调整
                        数据中心层级 - 虚拟卷列表- 保持仍有 存储使用率项，不做调整
                        可用域层级 - 不展示虚拟卷入口
                        集群层级 - 虚拟卷列表- 保持仍有 存储使用率项，不做调整
                        主机层级 - 不展示虚拟卷入口
                        虚拟机组级别 - 不展示虚拟卷入口
                    虚拟机详情列表
                        610 以下集群：smtx os/smtx elf：包含 6.x（ 6.0.0）、5.x（515）、4.x(4.0.10)、3.x（3.5.17）
                        610 及以上集群：包含smtx os/smtx elf：610、620+
                        虚拟机列表导出时增加「存储使用率」列，对 6.1.0 及以上版本展示为「-」（报表导出没有按层级区分都展示该选项）
                        低于 610 集群 虚拟机列 增加 [存储使用率] 项 - 不是默认列 - 勾选该列选项可正确展示
                        低于 610 集群 虚拟机列 增加 [存储使用率] 项 - 支持排序
                        组织架构 - 虚拟机列表 - 不展示 存储使用率 列选项 - 报表导出都展示存储使用率列选项：610以下展示具体数据，610及以上展示为 [-]
                        数据中心层级 - 不展示 存储使用率 列选项 - 报表导出都展示存储使用率列选项：610以下展示具体数据，610及以上展示为 [-]
                        tower - 只有  610以下集群 - 组织架构、数据中心层级 - 虚拟机列表：不展示 存储使用率列选项
                        610 以上集群 - 可用域层级 - 预期虚拟机列表 - 不展示存储使用率项 - 报表导出都展示存储使用率列选项：610及以上展示为 [-]
                        610及以上集群 - 集群层级 - 虚拟机列表 - 没有存储使用率项 - 报表导出都展示存储使用率列选项：610及以上展示为 [-]
                        610及以上集群 - 主机层级 - 虚拟机列表 - 没有存储使用率项 - 报表导出都展示存储使用率列选项：610及以上展示为 [-]
                        610及以上集群 - 虚拟机组层级 - 虚拟机列表 - 没有存储使用率项 - 报表导出都展示存储使用率列选项：610及以上展示为 [-]
                        低于 610 集群 - 可用域层级 - 预期虚拟机列表 - 展示存储使用率项 - 列选项可排序，列表导出符合预期
                        低于 610 集群 - 集群层级 - 虚拟机列表 - 展示存储使用率项 - 列选项可排序，列表导出符合预期
                        低于 610 集群 - 主机层级 - 虚拟机列表 - 展示存储使用率项 - 列选项可排序，列表导出符合预期
                        低于 610 集群 - 虚拟机组层级 - 虚拟机列表 - 展示存储使用率项 - 列选项可排序，列表导出符合预期
            虚拟机 vnc 页面拆分成单独的页面
                tower 正常登录情况下查看 vnc
                    打开 vnc 性能检查（直连成功情况下展示性能比之前快， 直连失败情况下和之前一样）（都可以打开）
                已打开 vnc 的情况下，登出 tower
                    vnc 页面立即不可查看，提示 Unauthorized. Please login to continue.， 并提供登录跳转按钮
                    重新登录后， vnc 自动切换到正常查看页面（不需要刷新页面）
        4.7.1
            虚拟机使用者新增快照权限
                UI 文案检查
                    中文页面 - UI 展示和校验提示等 - 是正确中文文案，符合预期
                    英文页面 - UI 展示和校验提示等 - 是正确英文文案，符合预期
                角色管理
                    检查角色管理 - 虚拟机使用者权限- 新增权限：虚拟机快照管理
                    角色管理 - 虚拟机使用者权限：虚拟机快照管理 权限 - 新增！ 数据说明
                用户管理
                    检查新增用户 - 分发虚拟机使用者权限 - 有虚拟机快照的操作权限：概览新增快照管理 tab 页面、vm 详细有虚拟机快照 tab 页 - 操作权限正确
                    检查低版本tower 已分发虚拟机使用者权限用户 - tower 升级后 - 登陆已有用户：有虚拟机快照的操作权限- 操作权限正确
                概览 - 虚拟机快照管理 tab 页面
                    登陆虚拟机管理者用户 - 检查“我的虚拟机” 更新为 “虚拟机管理者用户名”
                    登陆虚拟机管理者用户 - 检查新增 tab：”虚拟机快照“列表页面
                    “虚拟机快照“列表页面 - 无导出快照列表入口
                    虚拟机快照列表 - 列选项数据检查
                        列选项包括：名称、描述、源虚拟机、独占容量、快照时间字段
                        ”名称“ - 是字符串类型、默认宽带 240px、不支持交互，支持排序、支持（按字符串类型）筛选 - 检查排序：升序降序正确
                        “描述” -  - 是字符串类型、默认宽带 180px、不支持交互，不支持排序、支持（按字符串类型）筛选
                        “源虚拟机” - 是 icon+字符串类型、默认宽带 200px、支持交互，支持排序、支持（按对象属组）筛选 - 不支持排序
                        源虚拟机 - 交互检查：悬浮鼠标 名称，hover 变蓝，点击可跳转至虚拟机列表页面，并打开详情面板
                        "独占容量" - “描述” -  - 是数值类型、默认宽带 120px、支持交互，支持排序、支持（按数值，单位：GiB）筛选 - 排序：升序降序正确
                        独占容量 - 表头具备 hover tooltip:所属集群为 SMTX OS（版本 5.1.0 及以上）或 SMTX ELF 时，展示为独占物理容量；所属集群为 SMTX OS（版本 5.1.0 以下）时，对数值增加 hover tooltip 展示为逻辑占用空间
                        独占容量  - 当当列表中快照所属虚拟机所属集群为 510 以下版本的 OS 集群时，对数值增加 hover tooltip
                        快照更多操作“…”检查 - 包含 查看详情、删除 两个选项
                        快照更多操作“…”- 点击“查看详情 ”：触发弹窗与 Tower 中虚拟机快照详情弹窗保持一致
                        快照更多操作“…” - 点击“删除”，触发与 Tower 当前删除虚拟机快照弹窗持一致
                        快照更多操作“…” - “删除 ”：属于快照计划的虚拟机快照隐藏「删除」入口，其他快照展示删除按钮
                    筛选数据检查
                        快速筛选
                            快速筛选（使用名称筛选） - 筛选数据符合预期
                        高级筛选
                            快照名称 - 包含指定字段 - 筛选正确
                            虚拟机快照页面 - 仅支持当前页面搜索，不支持全局搜索
                            源虚拟机筛选项 - 只展示虚拟机用户者有权限的虚拟机，不展示无权限虚拟机
                            独占物理容量 - 运算符 ”>=“ 的数据 - 针对 515 及以上集群的数据 - 筛选成功
                            独占物理容量 - 运算符 “<=”的数据 - 针对 515 以下（是逻辑容量）集群的数据 - 筛选成功
                            独占物理容量 - 运算符 “< ”的数据 - 包含 515级以上、515 以下集群数据 - 筛选成功，是按GiB 筛选
                            独占物理容量 - 运算符 “>”的数据 - 包含 515级以上、515 以下集群数据 - 筛选成功
                            独占物理容量 - 运算符 “= ”的数据 - 包含 515级以上、515 以下集群数据 - 筛选成功
                            快照时间 - 筛选指定时间区间的数据 - 包含 515级以上、515 以下集群数据 - 筛选成功
                            快照名称、源虚拟机、独占容量、快照时间 组合筛选数据 - 筛选成功
                虚拟机详情 - 快照
                    基本信息
                        入口：虚拟机详情 - 快照 tab 页 - 快照 tab页，默认有创建快照入口
                        515 级以上集群默认展示名称、描述、独占物理容量、快照时间、更多操组“…” 、设置里选项入口
                        515 以下集群默认展示名称、描述、逻辑占用空间、快照时间、更多操组“…” 、设置里选项入口
                        快照可按 快照时间排序，其他项不可排序
                        快照 tab - 列选项”设置“ 默认选中所有数据：名称、描述、独占物理容量、快照时间可调整顺序 - 调整顺数成功
                        快照tab - 快照：更多可操作项，包含 查看详情、回滚、删除
                    快照展示
                        展示运维管理员创建的快照
                        展示超级管理员创建的快照
                        展示其他虚拟机管理员创建的快照
                        快照列表 - 展示普通虚拟机快照
                        展示虚拟机已有的快照计划快照：定时任务快照、手动执行的快照
                        查看快照详情 - 展示虚拟机快照基本信息、网卡数量、磁盘数量
                        展示其他用户创建的一致性快照
                        展示复制计划、备份计划创建的快照
                        虚拟机进行跨集群热迁移（迁移后的虚拟机所属用户不清空） - 虚拟机使用者检查：虚拟机仍然展示，迁移残留的源虚拟机快照不展示
                        放入回收站的虚拟机 - 虚拟机使用者不展示虚拟机和快照
                        删除的虚拟机 - 虚拟机使用者不展示虚拟机和快照
                        从回收站恢复的虚拟机（含快照） - 放入回收站，会清空虚拟机所属用户，从回收站恢复后不恢复所属用户
                    创建快照
                        运行 vmtools 的虚拟机 - 创建时展示虚拟机一致性快照 入口
                        不运行 vmtools 的虚拟机 - 创建时不展示虚拟机一致性快照 入口
                        创建快照 - 与 Tower 创建虚拟机快照弹窗交互、校验保持一致；
                        已有管理员账户快照 - 使用虚拟机管理员创建快照 - 默认名称为：“vm-name -index” - index 排序正确
                        已有管理员账户、虚拟机管理员账户快照 - 使用当前虚拟机管理员创建快照 - 默认名称为：“vm-name -index” - index 排序正确
                        使用虚拟机管理员创建快照 - 自定义快照名称创建快照正确
                        自定义快照名称 - 单独空格（含 1 个和连续空格）：前端未限制，提交任务后报错
                        自定义快照名称 - 首空格 + 名称：前段未限制，可以成功提交，前端展示去掉空格；
                        自定义快照名称- 150 个字符、非法字符集合校验正确
                    快照回滚
                        制造场景触发：以下虚拟卷在创建快照后被删除，回滚将会重建并重新挂载。 - 校验提示正确，回滚成功
                        制造场景触发：”以下磁盘或 ISO 映像将会被重新挂载。“ - 校验提示正确回滚成功，回滚数据正确
                        制造场景触发：“快照中不包含以下磁盘或 ISO 映像，回滚将会被卸载。” - 校验提示正确回滚成功，回滚数据正确
                        制造场景触发：“以下虚拟卷在创建快照后被挂载至其他虚拟机，将无法被回滚。” - 校验提示正确回滚成功，回滚数据正确
                        制造场景触发：“以下 ISO 映像在创建快照后已经被删除，回滚后 CD-ROM 中将不包含原 ISO 映像。” - 校验提示正确回滚成功，回滚数据正确
                        开机虚拟机 - 快照回滚 - 无法回滚
                        关机虚拟机 - 可以触发快照回滚
                        普通虚拟机快照回滚成功 - 回滚数据正确
                        一致性虚拟机快照回滚成功 - 回滚数据正确
                        自动快照计划快照回滚成功 - 回滚数据正确
                        手动快照计划快照回滚成功 - 回滚数据正确
                    删除快照
                        删除该虚拟机管理者账户创建的虚拟机快照成功
                        删除其他虚拟机管理者账户 - 创建的虚拟机快照成功
                        删除运维管理员账户创建的普通虚拟机快照成功
                        删除快照计划的快照 - 无删除入口
                运维管理员检查
                    虚拟机详情-快照
                        虚拟机管理员创建的快照能快速同步到运维管理员快照列表
                        虚拟机管理员创建的快照 - 能在运维管理员看到用户事件记录：快照创建记录（含用户名称）
                        虚拟机管理员回滚快照 - 能在运维管理员看到用户事件记录：快照回滚记录（含用户名称）
                        虚拟机管理员删除的快照 - 能在运维管理员看到用户事件记录：快照删除记录（含用户名称）
                        虚拟机管理员账户创建的虚拟机快照 - 运维管理员能回滚 - 回滚数据正确
                    快照管理页面
                        快照管理页面：虚拟机管理员账户创建的虚拟机快照 - 运维管理员能重建 - 重建数据正确
                        快照管理页面：虚拟机管理员账户创建的虚拟机快照 - 运维管理员能删除 - 删除成功
                        快照管理页面：虚拟机管理员账户创建的虚拟机快照 - 运维管理员能编辑标签 - 编辑标签成功
                场景测试
                    数据同步检查
                        虚拟机使用者用户、虚拟机管理员间能快速同步到各账户下的快照数据 - 最长间隔 30s
                    并发检查
                        admin00 操作虚拟机进行开机或其他操作，user01\user02能同步到 vm 正在更新中是不可操作无法创建快照的状态
                        user01 操作虚拟机进行开机或其他操作，admin00\user02能同步到 vm 正在更新中是不可操作无法创建快照的状态
                        admin00 操作虚拟机进行开机，user01\user02 查看 vm 处于关机状态做回滚操作，但出现并发场景，此时是以任务触发为结果
                        admin00 、user01、user02 并发操作 vm 回滚到不同快照不会出现数据混乱 - 以最后一次回滚的结果为准
            支持虚拟机分配给多个虚拟机使用者
                UI 文案检查
                    中文页面 - UI 展示和校验提示等 - 是正确中文文案，符合预期
                    英文页面 - UI 展示和校验提示等 - 是正确英文文案，符合预期
                用户管理
                    检查分发虚拟机使用者权限给新增的多个用户 - 为多个虚拟机用户分发同一批 vm - 检查多个新增用户可操作同一批 vm
                    检查低版本tower 已分发虚拟机使用者权限用户 - tower 升级后 - 可与其他新增虚拟机使用者权限用户 - 操作同一批vm
                虚拟机分配用户
                    编辑虚拟机配置使用者
                        操作入口
                            入口：虚拟机详情 - 基本信息 - 编辑虚拟机所属用户（所属用户可以为空）
                            入口：虚拟机列表 - 更多操作“…”：编辑 - 编辑所属用户：可多选多个虚拟机使用者用户
                            入口：虚拟机列表 - 选择单个 vm ：编辑 - 编辑所属用户：可多选多个虚拟机使用者用户
                            入口：虚拟机列表 - 选择 多个vm ：编辑 - 编辑所属用户：可多选多个虚拟机使用者用户 - 批量操作成功
                        功能检查
                            编辑虚拟机所属用户时 - 筛选框，默认勾选 ：仅展示虚拟机使用者
                            编辑虚拟机所属用户时 - 取消勾选 ：仅展示虚拟机使用者，会展示所有超级管理员、运维管理员、虚拟机使用者用户
                            编辑虚拟机时，清空虚拟机所属用户 - 清空成功，可以为空
                            编辑虚拟机时，增加虚拟机所属用户 - 添加成功
                            批量选中不同所属用户的虚拟机 - 所属用户展示为空 - 添加新用户 - 虚拟机切换配置为新所属用户成功
                            批量选中完全相同用户的虚拟机 - 所属用户展示完全相同用户 - 删除相同用户，各虚拟机相同用户删除成功
                    虚拟机所属用户展示
                        虚拟机详情 - 基本信息 - 所属用户，可展示 v m 所属的多个虚拟机使用者账户、也展示运维管理员、超级管理员用户
                        虚拟机列表 - 列选项，可展示虚拟机所属用户字段
                        虚拟机所属用户 - 若仅包含一个用户，直接展示用户名称
                        虚拟机所属用户 - 超过一个用户，会展示所属用户数量 - 鼠标悬浮展示所有用户
                    创建 vm 编辑所属用户
                        创建空白 vm - 基本信息：编辑多个所属用户 - 创建v m 成功，检查分配所属用户正确
                        克隆批量创建 vm - 基本信息：编辑多个所属用户 - 创建多个vm 成功，检查分配所属用户正确
                        模版批量创建vm - 基本信息：编辑多个所属用户 - 创建 vm 成功，检查分配所属用户正确
                        快照重建 vm - 基本信息：编辑多个所属用户 - 创建 vm 成功，检查分配所属用户正确
                        ovf 导入vm时 - 基本信息：编辑多个所属用户 - 创建vm 成功，检查分配所属用户正确
                        创建虚拟机时默认选中当前用户
                高级筛选
                    当前页面筛选
                        虚拟机列表 - 筛选所属用户：单个虚拟机使用者用户 - 筛选成功，数据正确
                        虚拟机列表 - 筛选所属用户：多个虚拟机使用者用户 - 筛选成功，数据正确
                        虚拟机列表 - 筛选所属用户：虚拟机使用者用户、运维管理员、超级管理员  - 组合筛选成功，数据正确
                        虚拟机列表 - 筛选所属用户：虚拟机使用者用户 与其他筛选项  - 组合筛选成功，数据正确
                        筛选所属用户时 - 使用的是用户姓名，而不是用户名 - TOWER-20062（480 优化处理）
                    全局筛选
                        虚拟机 资源 - 筛选所属用户：单个虚拟机使用者用户 - 筛选成功，数据正确
                        虚拟机资源 - 筛选所属用户：多个虚拟机使用者用户 - 筛选成功，数据正确
                        虚拟机 资源 - 筛选所属用户：虚拟机使用者用户、运维管理员、超级管理员  - 组合筛选成功，数据正确
                        虚拟机 资源 - 筛选所属用户：虚拟机使用者用户 与其他筛选项  - 组合筛选成功，数据正确
                        虚拟机资源 - 筛选所属用户时 - 使用的是用户姓名，而不是用户名 - TOWER-20062（480 优化处理）
                事件记录
                    创建空白虚拟机 - 用户事件记录：虚拟机所属用户分配详情
                    克隆批量虚拟机 - 用户事件记录：虚拟机所属用户分配详情
                    模版批量虚拟机 - 用户事件记录：虚拟机所属用户分配详情
                    快照重建虚拟机 - 用户事件记录：虚拟机所属用户分配详情
                    ovf 导入虚拟机 - 用户事件记录：虚拟机所属用户分配详情
                    编辑虚拟机 - 用户事件记录：虚拟机所属用户分配详情
                导出报表
                    虚拟机列表 - 导出列表不包含虚拟机所属用户
                    导出报表 - 虚拟机资源 - 虚拟机列表 - 导出列表不包含虚拟机所属用户
        4.8.0
            资源优化
                自定义规则
                    tower 默认没有自定义规则
                    创建自定义规则 - 范围：所有符合条件的集群
                    创建自定义规则 - 范围：部分集群
            TOWER-20285 默认存储策略调整
                smtx os 集群
                    关联 smtx os 集群
                        关联时集群时，默认展示：展示副本策略，纠删码按集群展示、加密按集群展示
                        关联时（非双活、支持ec ）集群时，默认展示：为保证关键业务数据高可用，建议采用 3 副本或 EC K+2，可容忍任意两块物理盘或两个节点同时故障。
                        关联单节点集群 - 存储策略能选2/3副本能关联到 tower，但实际tower 不触发创建副本的4中存储策略，使用的是 elf 默认存储策略【无客户场景，UI不限制】
                        关联2节点集群 - 存储策略能选2/3副本能关联到 tower，但实际tower 不触发创建副本的4中存储策略，使用的是 elf 默认存储策略【无客户场景，，UI不限制】
                        关联 smtxos610 及以上版本 三节点集群 - 新增存储策略配置页面 - 默认为副本策略精简制备，副本数留空，ec 策略不可选 - 关联集群成功
                        关联 smtxos610 以下版本 三节点集群 - 新增存储策略配置页面 - 默认为副本策略精简制备，副本数留空，不展示 ec 策略 和 ec 提示语 - 关联集群成功
                        关联 smtxos610 及以上版本 三节点 部分层部署的集群（如全闪 128.81） - 新增存储策略配置页面 - 默认为副本策略精简制备，副本数留空，不展示 ec 策略 和 ec提示语 - 关联集群成功
                        关联已开启存储加密服务的 os 集群 - 展示 加密服务选项并且默认不开启 - 关联集群成功
                        关联已开启存储加密服务的 os 集群 - 展示 加密服务选项，操作开启 - 关联集群成功
                        关联双活集群时， - 默认 3副本精简制备，不可选2副本，不展示 ec 策略和ec 提示 - 关联成功
                        关联 非双活集群时 - 默认选中副本策略，并且不勾选 副本数 - 保存数据校验提示：请选择默认副本数
                        关联 610 及以上版本 4节点集群时，能选择 ec 策略 - 切换为 ec 策略时：默认为精简制备，配比默认[2+1] 不可更改 - 关联成功
                        关联 610 以上4节点集群时，默认为副本策略未选择副本数时，切换为 ec 策略 - 重新切换为 副本策略时仍保持未选中副本数
                        关联 610 及以上版本 大于4节点集群时，能选择 ec 策略 - 切换为 ec 策略时：默认为精简制备，配比默认[2+1]，可更改配比：已有配置 - 关联成功
                        关联 610 及以上版本 大于4节点集群时，能选择 ec 策略 - 切换为 ec 策略时：默认为精简制备，配比默认[2+1]，可更改配比：自定义配比 - 关联成功
                        关联 610 及以上版本 大于4节点集群时，能选择 ec 策略 - 切换为 ec 策略时：默认为精简制备，配比默认[2+1]，可更改配比：自定义配比 - 关联成功
                        若集群关联成功，默认存储策略配置失败，集群仍然会关联到 Tower，默认存储策略会设置为：3 副本、精简置备、不启用加密【研发1⃣️代码模拟构造，QA不单独检查】
                        若关联集群成功，但是配置默认存储策略失败，tower 任务展示如下：配置集群默认存储策略失败，请在集群“设置”选项卡的“存储策略”中调整集群默认存储策略。
                        SMTX OS（VMware）集群 - 关联到 tower 时，不应有关联存储配置页面
                        tower480 操作新关联 630 及以上集群，设置任意存储策略，都会触发tower 在后端自动创建 4 条带 和 8 条带存储策略共 8 种
                        操作关联 集群：配置ec 策略，实际后端不会触发tower 在后端自动创建 ec 策略，只有新建卷资源才会创建对应 ec 存策略
                    事件记录
                        tower 关联集群：检查使用 副本策略配置支持加密的集群 -事件记录：将集群 {{集群名}} 加入 {{CloudTower}}。 默认存储策略配置 {{成功/失败}}包含：冗余策略和制备方式、是否开启加密
                        tower 关联集群：检查使用 ec策略配置不支持加密的集群 -事件记录：将集群 {{集群名}} 加入 {{CloudTower}}。 默认存储策略配置 {{成功/失败}}包含：冗余策略和制备方式（无加密项）
                        AOC 关联 集群：检查使用 副本策略配置支持加密的集群 -事件记录：将集群 {{集群名}} 加入 {{AOC}}。 默认存储策略配置 {{成功/失败}}包含：冗余策略和制备方式、是否开启加密
                        AOC 关联 集群：检查使用 ec策略配置不支持加密的集群 -事件记录：将集群 {{集群名}} 加入 {{AOC}}。 默认存储策略配置 {{成功/失败}}包含：冗余策略和制备方式（无加密项）
                    配置存储策略
                        smtx os 双活集群修改存储策略 - 默认存储策略 3副本精简制备，可调整制备模式，不会展示新增的提示语
                        smtx os 非双活+支持 ec 的集群，修改存储策略 - 新增提示：为保证关键业务数据高可用，建议采用 3 副本或纠删码（K+2），可容忍任意两块物理盘或两个节点同时故障。
                        smtx os 双活/不支持 ec 的集群，修改存储策略 - 新增提示：为保证关键业务数据高可用，建议采用 3 副本，可容忍任意两块物理盘或两个节点同时故障。--不提示ec 策略
                smtx elf 集群
                    关联 smtx elf 集群
                        smtx elf 只有一个关联存储且已关联至 tower
                            smtx elf 关联集群时 - 新增：增加关联存储默认存储策略的区域
                            smtx elf 关联的 os/zbs 存储集群 - 展示 存储集群名称，名称过长时 打点省略
                            关联的存储集群为不同类型数据检查
                                关联时集群时，默认展示：展示副本策略，纠删码按集群展示、加密按集群展示
                                关联存储是 非双活集群时 - 默认选中副本策略，并且不勾选 副本数 - 保存数据校验提示：请选择默认副本数
                                关联时（非双活、支持ec ）集群时，默认展示：为保证关键业务数据高可用，建议采用 3 副本或 EC K+2，可容忍任意两块物理盘或两个节点同时故障。
                                关联存储是 单节点 os/zbs 集群 -  存储策略能选2/3副本能关联到 tower，但实际tower 不触发创建副本的4中存储策略，使用的是 elf 默认存储策略【无客户场景，，UI不限制】
                                关联存储是 2节点os/zbs 集群 -  存储策略能选2/3副本能关联到 tower，但实际tower 不触发创建副本的4中存储策略，使用的是 elf 默认存储策略【无客户场景，，UI不限制】
                                关联存储是 smtxos610/zbs560 及以上版本 三节点集群 - 新增存储策略配置页面 - 默认为副本策略精简制备，副本数留空，ec 策略不可选 - 关联集群成功，存储策略正确
                                关联存储是  smtxos610/zbs560 以下版本 三节点集群 - 新增存储策略配置页面 - 默认为副本策略精简制备，副本数留空，不展示 ec 策略 和 ec 提示语 - 关联集群成功
                                关联存储是  smtxos610 及以上版本 三节点 部分层部署的集群（如全闪 128.81） - 新增存储策略配置页面 - 默认为副本策略精简制备，副本数留空，不展示 ec 策略 和 ec提示语 - 关联集群成功
                                关联存储是 已开启存储加密服务的 os 副本策略集群 - 展示 加密服务选项并且默认不开启 - 关联集群成功
                                关联存储是 已开启存储加密服务的 os ec 策略集群 - 展示 加密服务选项，操作开启 - 关联集群成功
                                关联存储是 双活 os 集群时， - 默认 3副本精简制备，不可选2副本，不展示 ec 策略和ec 提示 - 关联成功
                                关联存储是 os610/zbs560 及以上版本 4节点集群时，能选择 ec 策略 - 切换为 ec 策略时：默认为精简制备，配比默认[2+1] 不可更改 - 关联成功
                                关联存储是 os610/zbs560 以上4节点集群时，默认为副本策略未选择副本数时，切换为 ec 策略 - 重新切换为 副本策略时仍保持未选中副本数
                                关联存储是 os610/zbs560 及以上版本 5节点集群时，能选择 ec 策略 - 切换为 ec 策略时：默认为精简制备，配比默认[2+1]， 可更改配比 - 关联成功
                                关联 存储是 610/560 及以上版本 大于4节点集群时，能选择 ec 策略 - 切换为 ec 策略时：默认为精简制备，配比默认[2+1]，可更改配比：自定义配比 - 关联成功
                                关联 存储是 610/560 及以上版本 大于4节点集群时，能选择 ec 策略 - 切换为 ec 策略时：默认为精简制备，配比默认[2+1]，可更改配比：自定义配比 - 关联成功
                                若集群关联成功，默认存储策略配置失败，集群仍然会关联到 Tower，关联存储os/zbs 的默认存储策略会设置为：3 副本、精简置备、不启用加密【研发1⃣️代码模拟构造，QA不单独检查】
                                若关联smtxelf 集群成功，但是 存储 os/zbs 配置默认存储策略失败，tower 任务展示如下：配置集群默认存储策略失败，请在集群“设置”选项卡的“存储策略”中调整集群默认存储策略。
                        smtx elf 只有一个关联存储且未关联至 tower
                            关联 smtx elf(含1个关联存储 os/zbs)，关联页面展示该存储（os/zbs）的接入点 ip
                            关联 smtx elf(含1个关联存储 os/zbs)，关联时 展示提示语：该存储使用3副本精简制备，UI 展示冗余策略 3副本精简制备，不是提示加密项
                            关联 smtx elf(含1个关联存储 os/zbs)，关联到 tower 即配置存储（os/zbs）都是用3副本精简制备 - 检查smtx elf 关联成功后 ，存储集群策略都是 3副本精简制备
                        smtx elf 关联多个存储
                            已关联多个关联存储 smtx elf，不需要考虑关联存储是否已关联到 tower，关联页面展示关联存储个数正确（包含存储 时 os/zbs）
                            已关联多个关联存储的smtx elf ，关联时 展示提示语：所有存储都是用3副本精简制备，UI 展示 冗余策略 3副本精简制备，不是提示加密项
                            已关联多个关联存储 smtx elf，关联到 tower 即配置所有 存储（os/zbs）都是用3副本精简制备 - 检查smtx elf 关联成功后 ，所有存储都是 3副本精简制备
                        smtx elf 没有关联存储
                            smtx elf 没有关联存储时 关联到 tower  - 展示所属数据中心选择，不展示存储策略配置页面
                    添加存储
                        添加存储时，用户名密码正确 - 进入 存储集群默认存储策略设置页面
                        已关联到tower 的存储集群 os/zbs
                            若关联存储添加成功，默认存储策略配置失败，关联存储会添加成功，关联存储的默认存储策略会设置为：3 副本、精简置备、不启用加密。【研发1⃣️代码模拟构造，QA不单独检查】
                            关联时集群时，默认展示：展示副本策略，纠删码按集群展示、加密按集群展示
                            关联存储是 非双活集群时 - 默认选中副本策略，并且不勾选 副本数 - 保存数据校验提示：请选择默认副本数
                            关联时（非双活、支持ec ）集群时，默认展示：为保证关键业务数据高可用，建议采用 3 副本或 EC K+2，可容忍任意两块物理盘或两个节点同时故障。
                            关联存储是  smtxos610 及以上版本 三节点 部分层部署的集群（如全闪 128.81） - 新增存储策略配置页面 - 默认为副本策略精简制备，副本数留空，不展示 ec 策略 和 ec提示语 - 关联集群成功
                            关联存储是 已开启存储加密服务的 os/zbs 集群 - 展示 加密服务选项，操作开启 - 关联集群成功
                            关联存储是 双活 os 集群时， - 默认 3副本精简制备，不可选2副本，不展示 ec 策略和ec 提示 - 关联成功
                            关联存储是 os610/zbs560 及以上版本 5节点集群时，能选择 ec 策略 - 切换为 ec 策略时：默认为精简制备，配比默认[2+1]， 可更改配比 - 关联成功
                            添加存储集群，进行存储策略配置事取消或关闭弹窗，不会发起任务该存储集群不会被添加，
                        未关联到 tower 的存储集群 os/zbs
                            关联时（非双活、支持ec ）集群时，默认展示：为保证关键业务数据高可用，建议采用 3 副本，可容忍任意两块物理盘或两个节点同时故障。
                            关联存储是  smtxos610 及以上版本 三节点 部分层部署的集群（如全闪 128.81） - 新增存储策略配置页面 - 默认为副本策略精简制备，副本数留空，不展示 ec 策略 和 ec提示语 - 关联集群成功
                            关联存储是 已开启存储加密服务的 os/zbs 集群 - 不展示加密服务选项 - 关联集群成功
                            关联存储是 双活 os 集群时， - 默认 3副本精简制备，不可选2副本，不展示 ec 策略和ec 提示 - 关联成功
                            关联存储是 os610/zbs560 及以上版本 4节点集群时，不能选择 ec集群（未纳管无法感知）- 是用副本策略关联存储成功
                    编辑关联存储的存储策略
                        编辑elf 关联存储策略。-提示语更新：该操作仅可在当前集群中不存在运行中的虚拟机时执行。请确保编辑后提供关联存储的集群没有变化。
                    事件记录
                        关联集群
                            tower 关联集群：检查使用 副本策略配置支持加密的集群 -事件记录：将集群 {{集群名}} 加入 {{CloudTower}}。 默认存储策略配置 {{成功/失败}}包含：冗余策略和制备方式、是否开启加密
                            tower 关联集群：检查使用 ec策略配置不支持加密的集群 -事件记录：将集群 {{集群名}} 加入 {{CloudTower}}。 默认存储策略配置 {{成功/失败}}包含：冗余策略和制备方式（无加密项）
                        配置关联存储
                            配置关联存储 os ec策略支持加密 {{关联存储的接入虚拟 IP}} 。 关联存储默认存储策略配置 {{成功/失败}}： 包含：冗余策略和制备方式、是否开启加密
                            配置关联存储 zbs副本 策略支持加密 {{关联存储的接入虚拟 IP}} 。 关联存储默认存储策略配置 {{成功/失败}}： 包含：冗余策略和制备方式（无加密）
            TOWER-20085 卷回收站 - 虚拟化适配
                SMTXOS 6.3.0, 默认开启 ZBS 回收站 - P1
                    ISO
                        Tower 删除 ISO，直接删除不进入 ZBS 回收站
                        ISO 上传失败（如 非 ISO 格式），检查上传 ISO 过程中的 lun 删除不会进入回收站
                        从已有 iso 的集群列表中移除一个集群，直接删除，不进回收站
                    虚拟机
                        Tower 删除虚拟机
                            Tower 直接删除虚拟机，删除成功
                            Tower 回收站删除虚拟机，删除成功
                            集群开启回收站，删除虚拟机，进回收站
                    删除虚拟机模版
                        Tower 删除内容库模版
                            Tower 删除内容库虚拟机模版，删除成功，不进回收站
                    删除虚拟卷
                        Tower 删除虚拟卷
                            Tower 删除虚拟卷，删除成功，不进回收站
                    跨集群迁移
                        跨集群冷迁移失败涉及卷的删除时不进回收站
                        跨集群分段迁移失败涉及卷的删除时不进回收站
                SMTXOS 6.3.0, 设置关闭 ZBS 回收站
                    ISO
                        删除 ISO 成功，不进回收站
                        从已有 iso 的集群列表中移除一个集群，不进回收站
                    删除虚拟机
                        Tower 删除虚拟机
                            Tower 永久删除虚拟机，删除成功，不进回收站
                            Tower 回收站删除虚拟机，删除成功
                            集群未开启回收站，删除虚拟机，不进回收站
                    删除虚拟机模版
                        Tower 删除内容库模版
                            Tower 删除内容库虚拟机模版，删除成功，不进回收站
                    删除虚拟卷
                        Tower 删除虚拟卷
                            Tower 删除虚拟卷，删除成功，不进回收站
                    跨集群迁移
                        跨集群冷迁移失败涉及卷的删除时不进回收站
                        跨集群分段迁移失败涉及卷的删除时不进回收站
                SMTXELF 6.2.0 + 支持 ZBS 回收站点的 ZBS 5.7.0 - P1
                    永久删除弹窗里的文案提示
                        从tower全局视图永久删除虚拟机、虚拟卷
                            删除一个虚拟机（smtxelf 6.2.0），弹窗提示进回收站
                            批量删除虚拟机（部分虚拟机是 620集群）
                            批量删除虚拟机（所有虚拟机是 620集群）
                            批量删除虚拟卷（部分虚拟机是 620集群）
                            批量删除虚拟卷（所有虚拟机是 620集群）
                            删除一个虚拟卷（smtxelf 6.2.0），弹窗提示进回收站
                        从回收站里永久删除虚拟机
                            删除一个虚拟机（smtxos 6.2.0），不提示轮进回收站
                        从回收站-集群特例规则编辑里永久删除虚拟机
                            删除一个虚拟机（smtxos 6.2.0），不提示轮进回收站
                    ISO
                        删除 ISO 成功，不进回收站
                        从已有 iso 的集群列表中移除一个集群，不进回收站
                    删除虚拟机
                        Tower 删除虚拟机
                            Tower 直接删除虚拟机，删除成功
                            Tower 回收站删除虚拟机，删除成功
                            SMTXELF 开启回收站，ZBS也开启回收站 ，删除虚拟机，虚拟机进回收站，从回收站永久删除虚拟机后，LUN 进回收站
                            SMTXELF 开启回收站，ZBS不开启回收站 ，删除虚拟机，虚拟机进回收站，从回收站永久删除虚拟机后，LUN 不进回收站
                            SMTXELF 未开启回收站 +  ZBS 开启回收站，永久删除虚拟机，虚拟机不进回收站，对应的 lun 进回收站
                            SMTX ELF & SMTX ZBS 集群均不开启回收站，删除虚拟机，VM 和对应的 LUN 均直接被删除，不进回收站
                    删除虚拟机模版
                        Tower 删除内容库模版
                            Tower 删除内容库虚拟机模版，删除成功，不进回收站
                    删除虚拟卷
                        Tower 删除虚拟卷
                            Tower 删除虚拟卷，删除成功
                            zbs集群开启回收站，删除虚拟卷，进回收站
                            zbs集群未开启回收站，删除虚拟卷，不进回收站
                    跨集群迁移
                        跨集群冷迁移失败涉及卷的删除时不进回收站
                        跨集群分段迁移失败涉及卷的删除时不进回收站
                    删除快照
                        zbs集群开启回收站
                            删除虚拟机普通快照，直接删除，不进回收站
                            删除虚拟机一致性快照，直接删除，不进回收站
                            删除虚拟卷快照，直接删除，不进回收站
                        zbs集群未开启回收站
                            删除虚拟机普通快照，直接删除，不进回收站
                            删除虚拟机一致性快照，直接删除，不进回收站
                            删除虚拟卷快照，直接删除，不进回收站
                SMTXELF 6.2.0 + 支持 ZBS 回收站点的 SMTXOS 6.3.0
                    永久删除弹窗里的文案提示
                        批量删除虚拟机（部分虚拟机是 620集群）
                        批量删除虚拟机（所有虚拟机是 620集群）
                        批量删除虚拟卷（部分虚拟机是 620集群）
                        批量删除虚拟卷（所有虚拟机是 620集群）
                        删除一个虚拟机（smtxos 6.2.0）
                        删除一个虚拟卷（smtxos 6.2.0）
                    ISO
                        删除 ISO 成功，不进回收站
                        从已有 iso 的集群列表中移除一个集群，不进回收站
                    删除虚拟机
                        Tower 删除虚拟机
                            Tower 直接删除虚拟机，删除成功
                            Tower 回收站删除虚拟机，删除成功
                            SMTXELF 开启回收站，ZBS也开启回收站 ，删除虚拟机，虚拟机进回收站，从回收站永久删除虚拟机后，LUN 进回收站
                            SMTXELF 开启回收站，ZBS不开启回收站 ，删除虚拟机，虚拟机进回收站，从回收站永久删除虚拟机后，LUN 不进回收站
                            SMTXELF 未开启回收站 +  ZBS 开启回收站，永久删除虚拟机，虚拟机不进回收站，对应的 lun 进回收站
                            SMTX ELF & SMTX ZBS 集群均不开启回收站，删除虚拟机，VM 和对应的 LUN 均直接被删除，不进回收站
                    删除虚拟机模版
                        Tower 删除内容库模版
                            Tower 删除内容库虚拟机模版，删除成功，不进回收站
                    删除虚拟卷
                        Tower 删除虚拟卷
                            Tower 删除虚拟卷，删除成功
                            zbs集群开启回收站，删除虚拟卷，进回收站
                            zbs集群未开启回收站，删除虚拟卷，不进回收站
                    跨集群迁移
                        跨集群冷迁移失败涉及卷的删除时不进回收站
                        跨集群分段迁移失败涉及卷的删除时不进回收站
                    删除快照
                        zbs集群开启回收站
                            删除虚拟机普通快照，直接删除，不进回收站
                            删除虚拟机一致性快照，直接删除，不进回收站
                            删除虚拟卷快照，直接删除，不进回收站
                        zbs集群未开启回收站
                            删除虚拟机普通快照，直接删除，不进回收站
                            删除虚拟机一致性快照，直接删除，不进回收站
                            删除虚拟卷快照，直接删除，不进回收站
                SMTXELF 6.3.0 + 支持 ZBS 回收站的 ZBS 5.7.0  - P1
                    ISO
                        Tower 删除 ISO，直接删除不进入 ZBS 回收站
                        ISO 上传失败（如 非 ISO 格式），检查上传 ISO 过程中的 lun 删除不会进入回收站
                        从已有 iso 的集群列表中移除一个集群
                    虚拟机
                        Tower 删除虚拟机
                            Tower 直接删除虚拟机，删除成功
                            Tower 回收站删除虚拟机，删除成功
                            SMTXELF 禁用回收站 +  ZBS 开启回收站，永久删除虚拟机，虚拟机不进回收站，对应的 lun 不进回收站
                            SMTXELF 开启回收站，ZBS也开启回收站 ，删除虚拟机，虚拟机进回收站，从回收站永久删除虚拟机后，LUN 不进回收站
                            SMTXELF 开启回收站，ZBS不开启回收站 ，删除虚拟机，虚拟机进回收站，从回收站永久删除虚拟机后，LUN 不进回收站
                            SMTX ELF & SMTX ZBS 集群均不开启回收站，删除虚拟机，VM 和对应的 LUN 均直接被删除，不进回收站
                    删除虚拟机模版
                        Tower 删除内容库模版
                            Tower 删除内容库虚拟机模版，删除成功
                    删除虚拟卷
                        Tower 删除虚拟卷
                            Tower 删除虚拟卷，删除成功
                            zbs开启回收站，删除虚拟卷，不进回收站
                            zbs未开启回收站，删除虚拟卷，不进回收站
                    跨集群迁移
                        跨集群热迁移计算资源失败，涉及卷的删除时不进回收站
                        跨集群热迁移计算和存储资源迁移失败，涉及卷的删除时不进回收站
                    删除快照
                        zbs集群开启回收站
                            删除虚拟机普通快照，直接删除，不进回收站
                            删除虚拟机一致性快照，直接删除，不进回收站
                            删除虚拟卷快照，直接删除，不进回收站
                        zbs集群未开启回收站
                            删除虚拟机普通快照，直接删除，不进回收站
                            删除虚拟机一致性快照，直接删除，不进回收站
                            删除虚拟卷快照，直接删除，不进回收站
                SMTXELF 6.3.0 + 支持 ZBS 回收站的 SMTXOS 6.3.0
                    ISO
                        删除 ISO 成功
                        从已有 iso 的集群列表中移除一个集群
                    删除虚拟机
                        Tower 删除虚拟机
                            Tower 直接删除虚拟机，删除成功
                            Tower 回收站删除虚拟机，删除成功
                            SMTXELF 禁用回收站 +  ZBS 开启回收站，永久删除虚拟机，虚拟机不进回收站，对应的 lun 不进回收站
                            SMTXELF 开启回收站，ZBS也开启回收站 ，删除虚拟机，虚拟机进回收站，从回收站永久删除虚拟机后，LUN 不进回收站
                            SMTXELF 开启回收站，ZBS不开启回收站 ，删除虚拟机，虚拟机进回收站，从回收站永久删除虚拟机后，LUN 不进回收站
                            SMTX ELF & SMTX ZBS 集群均不开启回收站，删除虚拟机，VM 和对应的 LUN 均直接被删除，不进回收站
                    删除虚拟机模版
                        Tower 删除内容库模版
                            Tower 删除内容库虚拟机模版，删除成功，不进回收站
                    删除虚拟卷
                        Tower 删除虚拟卷
                            Tower 删除虚拟卷，删除成功
                            zbs开启回收站，删除虚拟卷，不进回收站
                            zbs未开启回收站，删除虚拟卷，不进回收站
                    跨集群迁移
                        跨集群冷迁移失败涉及卷的删除时不进回收站
                        跨集群分段迁移失败涉及卷的删除时不进回收站
                    删除快照
                        zbs集群开启回收站
                            删除虚拟机普通快照，直接删除，不进回收站
                            删除虚拟机一致性快照，直接删除，不进回收站
                            删除虚拟卷快照，直接删除，不进回收站
                        zbs集群未开启回收站
                            删除虚拟机普通快照，直接删除，不进回收站
                            删除虚拟机一致性快照，直接删除，不进回收站
                            删除虚拟卷快照，直接删除，不进回收站
                SMTXELF 6.3.0 + 不支持 ZBS 回收站的 ZBS 5.6.4  - P1
                    ISO
                        删除 ISO 成功，不进回收站
                        从已有 iso 的集群列表中移除一个集群，不进回收站
                    删除虚拟机
                        Tower 删除虚拟机
                            Tower 直接删除虚拟机，删除成功
                            Tower 回收站删除虚拟机，删除成功
                            smtxelf 集群开启回收站，删除虚拟机，进回收站，从回收站永久删除虚拟机后，不进回收站
                            smtxelf 集群未开启回收站，删除虚拟机，不进回收站
                    删除虚拟机模版
                        Tower 删除内容库模版
                            Tower 删除内容库虚拟机模版，删除成功，不进回收站
                    删除虚拟卷
                        Tower 删除虚拟卷
                            Tower 删除虚拟卷，删除成功
                            smtxelf 集群开启回收站，删除虚拟机，不进回收站
                            smtxelf 集群未开启回收站，删除虚拟机，不进回收站
                    跨集群迁移
                        跨集群冷迁移失败涉及卷的删除时不进回收站
                        跨集群分段迁移失败涉及卷的删除时不进回收站
                    删除快照
                        zbs集群开启回收站
                            删除虚拟机普通快照，直接删除，不进回收站
                            删除虚拟机一致性快照，直接删除，不进回收站
                            删除虚拟卷快照，直接删除，不进回收站
                        zbs集群未开启回收站
                            删除虚拟机普通快照，直接删除，不进回收站
                            删除虚拟机一致性快照，直接删除，不进回收站
                            删除虚拟卷快照，直接删除，不进回收站
                SMTXELF 6.3.0 + 不支持 ZBS 回收站的 SMTXOS 6.2.0
                    ISO
                        删除 ISO 成功，不进回收站
                        从已有 iso 的集群列表中移除一个集群，不进回收站
                    删除虚拟机
                        Tower 删除虚拟机
                            Tower 直接删除虚拟机，删除成功
                            Tower 回收站删除虚拟机，删除成功
                            smtxelf 集群开启回收站，删除虚拟机，进回收站，从回收站永久删除虚拟机后，不进回收站
                            smtxelf 集群未开启回收站，删除虚拟机，不进回收站
                    删除虚拟机模版
                        Tower 删除内容库模版
                            Tower 删除内容库虚拟机模版，删除成功，不进回收站
                    删除虚拟卷
                        Tower 删除虚拟卷
                            Tower 删除虚拟卷，删除成功
                            smtxelf 集群开启回收站，删除虚拟机，不进回收站
                            smtxelf 集群未开启回收站，删除虚拟机，不进回收站
                    跨集群迁移
                        跨集群冷迁移失败涉及卷的删除时不进回收站
                        跨集群分段迁移失败涉及卷的删除时不进回收站
                    删除快照
                        zbs集群开启回收站
                            删除虚拟机普通快照，直接删除，不进回收站
                            删除虚拟机一致性快照，直接删除，不进回收站
                            删除虚拟卷快照，直接删除，不进回收站
                        zbs集群未开启回收站
                            删除虚拟机普通快照，直接删除，不进回收站
                            删除虚拟机一致性快照，直接删除，不进回收站
                            删除虚拟卷快照，直接删除，不进回收站
            TOWER-20360 虚拟机快照管理-删除
                快照跳转虚拟机
                删除系统虚拟机快照
                删除普通虚拟机快照
                删除副本虚拟机快照
            TOWER-19569	 Tower 跨集群冷/分段迁移创建 LUN 设置 IQN 白名单
                源端数据
                    非 vhost
                        os 630 非 vhost 上源端关机 vm  - virtio/scsi/ide 卷 白名单：Allowed Initiators   空;  Single Access     True;
                        os 630 非 vhost 上源端开机 vm  - virtio/scsi/ide 卷 白名单：Allowed Initiators  “iqn.2013-11.org.smartx:vm_uuid.host_uuid.0”; Single Access True;
                    vhost
                        os 630 vhost 上源端关机 vm  - virtio/scsi 卷白名单: Single access: True;不展示 VM UUID/MACHINE UUID；
ide卷白名单: Allowed Initiators 空;Single Access True;
                        os 630 vhost 上源端开机 vm  -  virtio/scsi 卷白名单: Single access: True;展示 VM UUID/MACHINE UUID；
ide卷白名单: Allowed Initiators “iqn.2013-11.org.smartx:vm_uuid.host_uuid.0”; Single Access True;
                目标端 620hp4 及以上版本
                    非 vhost
                        冷迁移
                            os 630 非 vhost vm 冷迁移到 os 630 非 vhost  - 迁移后检查目标端集群 vm  virtio/scsi/ide 卷 白名单：Allowed Initiators 空; Single Access True;
                            冷迁移后，vm 在 目标端 非vhsot 集群开机 - 检查  vm virtio/scsi/ide 卷：白名单：Allowed Initiators “iqn.2013-11.org.smartx:vm_uuid.host_uuid.0”; Single Access True;
                            os 630 非 vhost vm 冷迁移到 os 630 非 vhost  -  检查迁移过程中新建 autogen-by-cross-migration 相关 target/lun 迁移完成后已清理
                        分段迁移
                            os 630 非 vhost vm 分段迁移到 os 630 非 vhost  - 迁移后 检查目标端集群 开机 vm  virtio/scsi/ide 卷 白名单：Allowed Initiators “iqn.2013-11.org.smartx:vm_uuid.host_uuid.0”; Single Access True;
                            分段迁移后，vm 在 目标端 非vhsot 集群关机 - zbs-iscsi lun show <target. lun_id> 检查  vm virtio/scsi/ide 卷：白名单：Allowed Initiators “空”; Single Access True;
                            os 630 非 vhost vm 分段迁移到 os 630 非 vhost  -  检查迁移过程中新建 autogen-by-cross-migration 相关 target/lun 迁移完成后已清理
                    vhost
                        冷迁移
                            os 630 非 vhost vm 冷迁移到 os 630 vhost  - 迁移后 检查目标端集群 vm virtio/scsi 卷白名单: Single access: True;不展示 VM UUID/MACHINE UUID；
ide卷白名单: Allowed Initiators 空;Single Access True;
                            冷迁移后，vm 在 目标端 vhost 集群开机 - 检查virtio/scsi 卷白名单: Single access: True;展示 VM UUID/MACHINE UUID；
ide卷白名单: Allowed Initiators “iqn.2013-11.org.smartx:vm_uuid.host_uuid.0”; Single Access True;
                            os 630 非 vhost vm 冷迁移到 os 630 非 vhost  -  检查迁移过程中新建 autogen-by-cross-migration 相关 target/lun 迁移完成后已清理
                        分段迁移
                            os 630 非 vhost vm 分段迁移到 os 630 vhost  - 迁移后 检查目标端集群 开机 vm virtio/scsi 卷白名单: Single access: True;展示 VM UUID/MACHINE UUID；
ide卷白名单: Allowed Initiators “iqn.2013-11.org.smartx:vm_uuid.host_uuid.0”; Single Access True
                            分段迁移后，vm 在 目标端 vhost 集群关机 -  virtio/scsi 卷白名单: Single access: True;不展示 VM UUID/MACHINE UUID；
ide卷白名单: Allowed Initiators 空;Single Access True;
                            os 630 非 vhost vm 分段迁移到 os 630 vhost  -  检查迁移过程中新建 autogen-by-cross-migration 相关 target/lun 迁移完成后已清理
                目标端 620hp4 以下版本
                    vhost
                        冷迁移到 vhost
                            os 630 非 vhost vm 冷迁移到 os 515p2 vhost  - 迁移后 检查目标端集群 vm virtio/scsi 卷白名单: Single access: True;展示 VM UUID/MACHINE UUID 为 “*/*”；
ide卷白名单: Allowed Initiators “*/*”;Single Access True;
                            冷迁移后，vm 在 目标端 vhost 集群开机 - 检查virtio/scsi 卷白名单: Single access: True;展示 VM UUID/MACHINE UUID；
ide卷白名单: Allowed Initiators “iqn.2013-11.org.smartx:vm_uuid.host_uuid.0”; Single Access True;
                            os 630 非 vhost vm 冷迁移到 os 515p2 非 vhost  -  检查迁移过程中新建 autogen-by-cross-migration 相关 target/lun 迁移完成后已清理
                        分段迁移到 vhost
                            os 630 非 vhost vm 分段迁移到 os 515p2 非 vhost  - 迁移后 检查目标端集群 开机 vm  virtio/scsi 卷白名单: Single access: True;展示 VM UUID/MACHINE UUID；
ide卷白名单: Allowed Initiators “iqn.2013-11.org.smartx:vm_uuid.host_uuid.0”; Single Access True;
                            分段迁移后，vm 在 目标端 非vhsot 集群关机 - virtio/scsi 卷白名单: Single access: True;不展示 VM UUID/MACHINE UUID ；
ide卷白名单: Allowed Initiators “空”;Single Access True;
                            os 630 非 vhost vm 分段迁移到 os 515p2 非 vhost  - 检查迁移过程中新建 autogen-by-cross-migration 相关 target/lun 迁移完成后已清理
                    非vhost
                        冷迁移
                            os 630 非 vhost vm 冷迁移到 os 515p2 非vhost  - 迁移后 检查目标端集群 vm virtio/scsi/ide  卷白名单: Allowed Initiators “*/*”;Single Access False;
                            冷迁移后，vm 在 目标端 非vhost 集群开机 - 检查virtio/scsi/ide卷白名单: Allowed Initiators “iqn.2013-11.org.smartx:vm_uuid.host_uuid.0”; Single Access True;
                            os 630 非 vhost vm 冷迁移到 os 515p2 非 vhost  -  检查迁移过程中新建 autogen-by-cross-migration 相关 target/lun 迁移完成后已清理
                        分段迁移到
                            os 630 非 vhost vm 分段迁移到 os 515p2 非 vhost  - 迁移后 检查目标端集群 开机 vm  virtio/scsi/ide 卷 白名单：Allowed Initiators “iqn.2013-11.org.smartx:vm_uuid.host_uuid.0”; Single Access True;
                            分段迁移后，vm 在 目标端 非vhsot 集群关机 - zbs-iscsi lun show <target. lun_id> 检查  vm virtio/scsi/ide 卷：白名单：Allowed Initiators “空”; Single Access True;
                            os 630 非 vhost vm 分段迁移到 os 515p2 非 vhost  - 检查迁移过程中新建 autogen-by-cross-migration 相关 target/lun 迁移完成后已清理
分布式系统管理
    集群生命周期管理
        集群部署
            功能测试
                GUI功能
                    集群配置
                        部署选项页面 - 静态数据加密部分存在
                        部署选项页面 - 静态数据加密 - 下方描述：加密加速可为静态数据加密功能提供独占的 CPU 核心。如需支持 SM4 加密算法则必须启用加密加速。
                        部署选项页面 - 静态数据加密 - 选择 不启用加密加速
                        部署选项页面 - 静态数据加密 - 选择 启用加密加速
                        部署选项页面 - 静态数据加密 - 不做选择 - 直接进行下一步， 报错：请为静态数据加密选择是否启用加密加速。
                        acos - 部署选项页面 - 静态数据加密 - 下方描述：加密加速可为静态数据加密功能提供独占的 CPU 核心
                    检查配置
                        检查配置页面 - 基本信息 - 已启用加密加速 - 显示正确
                        检查配置页面 - 基本信息 - 不启用加密加速 - 显示正确
        集群升级
            CentOS 升级转换 openEuler
                覆盖平台/版本范围
                    x86-vmware
                        转换后 io reroute 功能正常
            630-升级
                升级
                    多实例
                        两个实例升级（同版本升级）
                            normal
                                环境检查
                                    【节点的资源应满足升级目标版本系统服务的需求】- 节点预留内存值
                                        有节点内存不满足预留内存的值 - 不通过
                                        所有节点满足预留内存值 - 通过
                                    【节点计算资源应满足容量规格的要求】- 节点 CPU、内存值
                                        有节点不满足所需 CPU 值 - 不通过
                                        有节点不满足所需内存值 - 不通过
                                        所有节点满足所需 CPU、内存值 - 通过
                                部署方式
                                    分层
                                        OS 安装在软 RAID 1
                                            混闪
                                            全闪
                                    不分层
                                        OS 安装在硬 RAID 1
                            large
                                环境检查
                                    【节点的资源应满足升级目标版本系统服务的需求】- 节点预留内存值
                                        有节点内存不满足预留内存的值 - 不通过
                                        所有节点满足预留内存值 - 通过
                                    【节点计算资源应满足容量规格的要求】- 节点 CPU、内存值
                                        有节点不满足所需 CPU 值 - 不通过
                                        有节点不满足所需内存值 - 不通过
                                        所有节点满足所需 CPU、内存值 - 通过
                                部署方式
                                    分层
                                        OS 安装在软 RAID 1  - 全闪
                                    不分层
                                        OS 安装在硬 RAID 1
                                        OS 安装在软 RAID 1
                                            混闪
                            平台
                                smtxos
                                    vhost + rdma
                                tos
                                    vhost
                            升级后
                                集群上虚拟机状态正常
                                升级前集群安装了全家桶，升级后全家桶服务运行正常
                                不会产生异常告警信息
                                升级后服务状态正常
                                使用巡检执行检查和升级前比较无新增异常
                                升级后配置符合预期
                                    预留内存值
                                    cpuset 符合预期
                                    cgroup 符合预期（具体值在 cgroup 中验证）
                                升级后的运维操作
                                    节点添加
                                    节点移除
                                    节点运维
                                        节点角色转换：storage -> master
                                        节点角色转换：master -> storage
                                        重启节点主机
                                        关机节点，然后再开机
                        四个实例升级（同版本升级）
                            环境检查
                                【节点的资源应满足升级目标版本系统服务的需求】- 节点预留内存值
                                    有节点内存不满足预留内存的值 - 不通过
                                    所有节点满足预留内存值 - 通过
                                【节点计算资源应满足容量规格的要求】- 节点 CPU、内存值
                                    有节点不满足所需 CPU 值 - 不通过
                                    有节点不满足所需内存值 - 不通过
                                    所有节点满足所需 CPU、内存值 - 通过
                            部署方式
                                分层
                                    OS 安装在软 RAID 1
                                        混闪
                                        全闪
                                不分层
                                    OS 安装在软 RAID 1
                                        混闪
                                        全闪
                            平台（和 2实例交叉来）
                                smtxos
                                    vhost + rdma
                                arcfra
                                    vhost
                            升级后
                                集群上虚拟机状态正常
                                升级前集群安装了全家桶，升级后全家桶服务运行正常
                                不会产生异常告警信息
                                升级后服务状态正常
                                使用巡检执行检查和升级前比较无新增异常
                                升级后配置符合预期
                                    预留内存值
                                    cpuset 符合预期
                                    cgroup 符合预期（具体值在 cgroup 中验证）
                                升级后的运维操作
                                    节点添加
                                    节点移除
                                    节点运维
                                        节点角色转换：storage -> master
                                        节点角色转换：master -> storage
                                        重启节点主机
                                        关机节点，然后再开机
                    ELF 相关功能点
                        亚信支持
                            升级前检查
                                低于 6.3.0 版本集群无 vm-security-controller 使用630 版本环境检查成功
                                6.3.0及以上版本 vm-security-controller 服务异常 - 环境检查通过
                                6.3.0及以上版本 vm-security-controller 服务正常 - 环境检查成功
                            升级后检查
                                所有节点有 rpm:  vm-security-controller-1.0.0-rc16.0.g4f3bab4.el7.x86_64
                                节点存在：/etc/elfvirt/vs.conf 配置文件
                                vm-security-controller 服务运行正常
                                重启 vm-security-controller 服务可以正常起来
                                vm-security-controller 服务异常，集群产生服务异常告警
                                cgroup: 在 /smtx.slice/smtx-elf.slice/
                                cpuset: 运行在 /zbs/app
                                vm-security-controller
                                    主节点有此服务
                                    存储主节点有此服务
                                    witness 节点不运行此服务
                            升级
                                深度防护开默认未开启 - 升级更高版本 - 升级成功
                                仅开启深度防护，未上传或创建虚拟机  - 升级更高版本 - 升级成功
                                深度防护开启后关闭 - 升级更高版本 - 升级成功
                                深度防护开启  - 配置 Everoute 网络安全导流功能 - 升级更高版本，升级成功
                                深度防护开启  - 导入虚拟机 - 升级更高版本，升级成功
                        ELF 服务支持通过 zk 自行选主
                            升级过程
                                升级中：elf-tool upgrade_cluster post_update_cluster 步骤执行 setup_cluster_capabilities 失败，升级失败，失败后支持重试
                                升级快结束：由于 ha 服务处于停止状态，一同进行拉起
                                回归 smtxelf 平台：保持通过 zbs-cluster show_election_servers 命令获取 ha_leader 的方式
                                回归 vmware 平台：ha 服务是先停的 meta leader 的服务，然后停其他非 meta leader 节点的服务
                                升级前
                                    低于 6.2.0 升级到 630： ha 服务是先停 meta leader 的服务，然后停其他非 meta leader 节点的服务
                                    6.3.0 关闭 v2 升级更高版本： ha 服务是先停 meta leader 的服务，然后停其他非 meta leader 节点的服务
                                    630 开启v2 升级更高版本：ha 服务是先停 elf-vm-monitor leader 的服务，然后停其他非 elf-vm-monitor leader 节点的服务
                            升级成功后
                                服务检查运行正常
                                    elf-vm-scheduler：仅在主节点
                                    elf-vm-monitor：在所有节点运行
                                    elf-exporter：在所有节点运行
                                    elf-fs：在所有节点运行
                                运维操作
                                    查询：elf-tool elf_cluster is_enabled_election_v2
                                    关闭：elf-tool elf_cluster disable_election_v2
                                    开启：elf-tool elf_cluster enable_election_v2
                                    查询节点服务角色：zbs-cluster show_election_servers
                                检查选主
                                    低版本升级到 630  - 确认集群使用 v2 选主机制
                                    已经是 v2 选主，关闭 v2 选主后升级集群，升级后为 v1 选主机制
                                    630 集群 v2 选主，升级到更高版本后还是 v2 选主机制
                            场景
                                smtxelf
                                tos arm
                                centos x86
                                hygon oe
                                vmware
                                    查询、开启、关闭等命令在 vmware 平台不支持
                                    elf 相关的服务在 vmware 平台不存在
                升级自动化验证
                    SMTX
                        SMTXOS
                            el7-x86_64-smtxos-elf
                                3xx (升级kernel)
                                    3.0.5;3.5.17;4.0.13;5.0.5;5.1.4P1;6.2.0P4;当前版本
                                    3.5.17;4.0.12;5.0.3;5.1.4;当前版本
                                    3.5.17;4.0.14;507P2;当前版本
                                4xx
                                    从 4.0.5 升级至当前版本
                                    从 4.0.6 升级至当前版本
                                    从 4.0.7 升级至当前版本
                                    从 4.0.8 升级至当前版本
                                    从 4.0.9 升级至当前版本
                                    从 4.0.10 升级至当前版本
                                    从 4.0.11 升级至当前版本
                                    从 4.0.12 升级至当前版本
                                    从 4.0.13 升级至当前版本
                                    从 4.0.14 升级至当前版本
                                    4.0.0;4.0.5;4.0.6;4.0.9;4.0.14;5.0.13;5.0.14;5.1.4P2;5.1.5P1;当前版本
                                    4.0.5;4.0.6;4.0.7;4.0.8;4.0.9;4.0.10;4.0.11;4.0.12;4.0.13;4.0.14;5.1.1;当前版本
                                5xx
                                    非vhost+ 非rdma
                                        从 5.0.0 升级至当前版本
                                        从 5.0.1 升级至当前版本
                                        从 5.0.2 升级至当前版本
                                        从 5.0.3 升级至当前版本
                                        从 5.0.4 升级至当前版本
                                        从 5.0.5 升级至当前版本
                                        从 5.0.6 升级至当前版本
                                        从 5.0.7 升级至当前版本
                                        从 5.1.0 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3 升级至当前版本
                                        从 5.1.4 升级至当前版本
                                        从 5.1.5 升级至当前版本
                                        从 6.0.0 升级至当前版本
                                        从 6.1.0 升级至当前版本
                                        从 6.1.1 升级至当前版本
                                        从 6.2.0 升级至当前版本
                                        从 5.0.7 P2 升级至当前版本
                                        从 5.1.5 P1 升级至当前版本
                                        从 6.1.1 P1 升级至当前版本
                                        从 6.2.0 P4 升级至当前版本
                                        5.0.0;5.0.3;5.0.5;5.0.7;5.1.5;当前版本
                                        5.0.0;5.0.2;5.0.4;5.0.7;当前版本
                                        5.0.1;5.0.3;5.0.5;5.1.4;当前版本
                                    vhost
                                        从 5.0.0 升级至当前版本
                                        从 5.0.1 升级至当前版本
                                        从 5.0.2 升级至当前版本
                                        从 5.0.3 升级至当前版本
                                        从 5.0.4 升级至当前版本
                                        从 5.0.5 升级至当前版本
                                        从 5.0.6 升级至当前版本
                                        从 5.0.7 升级至当前版本
                                        从 5.1.0 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3 升级至当前版本
                                        从 5.1.4 升级至当前版本
                                        从 5.1.5 升级至当前版本
                                        从 6.0.0 升级至当前版本
                                        从 6.1.0 升级至当前版本
                                        从 6.1.1 升级至当前版本
                                        从 6.2.0 升级至当前版本
                                        从 5.0.7 P1 升级至当前版本
                                        从 5.1.4 P2 升级至当前版本
                                        从 5.1.5 P1 升级至当前版本
                                        从 6.1.1 P1 升级至当前版本
                                        从 6.2.0 P4 升级至当前版本
                                        5.0.0;5.0.4;5.0.6;5.1.5;当前版本
                                        5.0.0;5.0.2;5.0.4;5.0.7;当前版本
                                        5.0.1;5.0.3;5.0.5;5.1.4;当前版本
                                    vhost+rdma（低于5.1.0可以不用跑）
                                        从 5.0.0 升级至当前版本
                                        从 5.0.1 升级至当前版本
                                        从 5.0.2 升级至当前版本
                                        从 5.0.3 升级至当前版本
                                        从 5.0.4 升级至当前版本
                                        从 5.0.5 升级至当前版本
                                        从 5.0.6 升级至当前版本
                                        从 5.0.7 升级至当前版本
                                        从 5.1.0 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3 升级至当前版本
                                        从 5.1.4 升级至当前版本
                                        从 5.1.5 升级至当前版本
                                        从 6.0.0 升级至当前版本
                                        从 6.1.1  升级至当前版本
                                        从 6.1.1 P1  升级至当前版本
                                        从 6.2.0 P4 升级至当前版本
                                        5.0.0;5.0.3;5.0.5;5.1.1;当前版本
                                双活
                                    40x
                                        从 4.0.10 升级至当前版本
                                        从 4.0.11 升级至当前版本
                                        从 4.0.12 升级至当前版本
                                        从 4.0.13 升级至当前版本
                                        从 4.0.14 升级至当前版本
                                        4.0.10;4.0.14;当前版本
                                    50x （可以少跑）
                                        从 5.0.0 升级至当前版本
                                        从 5.0.1 升级至当前版本
                                        从 5.0.2 升级至当前版本
                                        从 5.0.3 升级至当前版本
                                        从 5.0.4 升级至当前版本
                                        从 5.0.5 升级至当前版本
                                        从 5.0.6 升级至当前版本
                                        从 5.0.7 升级至当前版本
                                        从 5.1.0 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3 升级至当前版本
                                        从 5.1.4 升级至当前版本
                                        从 5.1.5 升级至当前版本
                                        从 6.0.0 升级至当前版本
                                        从 6.1.0 升级至当前版本
                                        从 6.1.1 升级至当前版本
                                        从 6.2.0 升级至当前版本
                                        从 5.0.7 P2 升级至当前版本
                                        从 6.1.1 P1 升级至当前版本
                                        从 5.1.4 P2 升级至当前版本
                                        从 5.1.5 P1 升级至当前版本
                                        从 6.2.0 P4 升级至当前版本
                                        5.0.1;5.0.4;5.1.5;当前版本
                                        4.0.11;5.0.3;5.1.5;当前版本
                            oe2003-x86_64-smtxos-elf
                                非vhost + 非rdma
                                    从 5.0.6 升级至当前版本
                                    从 5.0.7 升级至当前版本
                                    从 5.1.0 升级至当前版本
                                    从 5.1.1 升级至当前版本
                                    从 5.1.2 升级至当前版本
                                    从 5.1.3 升级至当前版本
                                    从 5.1.4 升级至当前版本
                                    从 5.1.5 升级至当前版本
                                    从 6.0.0 升级至当前版本
                                    从 6.1.0 升级至当前版本
                                    从 6.1.1 升级至当前版本
                                    从 6.2.0 升级至当前版本
                                    从 5.0.7 P1 升级至当前版本
                                    从 5.1.4 P2 升级至当前版本
                                    从 5.1.5 P1 升级至当前版本
                                    5.0.6;5.1.4 P2;6.2.0 P4;当前版本
                                vhost
                                    从 5.0.6 升级至当前版本
                                    从 5.0.7 升级至当前版本
                                    从 5.1.0 升级至当前版本
                                    从 5.1.1 升级至当前版本
                                    从 5.1.2 升级至当前版本
                                    从 5.1.3 升级至当前版本
                                    从 5.1.4 升级至当前版本
                                    从 5.1.5 升级至当前版本
                                    从 6.0.0 升级至当前版本
                                    从 6.1.0 升级至当前版本
                                    从 6.1.1 升级至当前版本
                                    从 6.2.0 升级至当前版本
                                    5.0.6;5.1.1;6.0.0;6.3.0
                                vhost+rdma（低于5.1.0 可以不用执行）
                                    从 5.0.6 升级至当前版本
                                    从 5.0.7 升级至当前版本
                                    从 5.1.0 升级至当前版本
                                    从 5.1.0 升级至当前版本
                                    从 5.1.1 升级至当前版本
                                    从 5.1.2 升级至当前版本
                                    从 5.1.3 升级至当前版本
                                    从 5.1.4 升级至当前版本
                                    从 5.1.5 P1 升级至当前版本
                                    从 6.0.0 升级至当前版本
                                    从 6.1.0 升级至当前版本
                                    从 6.1.1 P1升级至当前版本
                                    从 6.2.0 P4升级至当前版本
                                    5.0.6;5.1.1;6.1.1;当前版本
                            oe2003-arm-smtxos-elf
                                arm oe
                                    非vhost、rdma
                                        从 5.0.3 升级至当前版本
                                        从 5.0.4 升级至当前版本
                                        从 5.0.5 升级至当前版本
                                        从 5.0.6 升级至当前版本
                                        从 5.0.7 升级至当前版本
                                        从 5.1.0 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3 升级至当前版本
                                        从 5.1.4 升级至当前版本
                                        从 5.1.5 升级至当前版本
                                        从 6.0.0 升级至当前版本
                                        从 6.1.0 升级至当前版本
                                        从 6.1.1 升级至当前版本
                                        从 6.2.0 升级至当前版本
                                        从 5.0.7 P2 升级至当前版本
                                        从 5.1.5 P1 升级至当前版本
                                        从 6.1.1 P1 升级至当前版本
                                        从 6.2.0 P4 升级至当前版本
                                        5.0.3;5.0.5;5.1.1;6.1.1;当前版本
                                        5.0.4;5.1.1;6.0.0;6.2.0 P4;当前版本
                                    vhost
                                        从 5.0.5 升级至当前版本
                                        从 5.0.6 升级至当前版本
                                        从 5.0.7 升级至当前版本
                                        从 5.1.0 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3 升级至当前版本
                                        从 5.1.4 升级至当前版本
                                        从 5.1.5 升级至当前版本
                                        从 6.0.0 升级至当前版本
                                        从 6.1.0 升级至当前版本
                                        从 6.1.1 升级至当前版本
                                        从 6.2.0 升级至当前版本
                                        5.0.5;5.1.1;6.0.0;当前版本
                                        5.0.5;5.1.1;6.0.0;6.2.0 P4;当前版本
                                    vhost+rdma （挑一两个）
                                        从 5.0.5 升级至当前版本
                                        从 5.1.0 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3升级至当前版本
                                        从 5.1.4 升级至当前版本
                                        从 5.1.5 升级至当前版本
                                        从 6.0.0 升级至当前版本
                                        从 6.1.1 升级至当前版本
                                        从 6.2.0P4 升级至当前版本
                                        5.1.1;6.1.1;当前版本
                                centos-to-oe
                                    4.0.9->5.0.5(转oe)->5.1.3->升级至当前版本
                                    4.0.12->4.0.14->5.0.5(转oe)->6.1.1P1->升级至当前版本
                                    4.0.9->4.0.14->5.0.7(转oe)->5.0.7 P2;升级至当前版本
                            oe2003-hygon-smtxos-elf
                                hygon oe
                                    非 vhost+ 非 rdma
                                        从 5.0.3 升级至当前版本
                                        从 5.0.4 升级至当前版本
                                        从 5.0.5 升级至当前版本
                                        从 5.0.6 升级至当前版本
                                        从 5.0.7 升级至当前版本
                                        从 5.1.0 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3 升级至当前版本
                                        从 5.1.4 升级至当前版本
                                        从 5.1.5 升级至当前版本
                                        从 6.0.0 升级至当前版本
                                        从 6.1.0 升级至当前版本
                                        从 6.1.1 升级至当前版本
                                        从 6.2.0 升级至当前版本
                                        从 6.2.0 P4 升级至当前版本
                                        5.0.3;5.0.5;5.1.1;6.1.1;当前版本
                                        5.0.4;5.1.1;6.0.0;当前版本
                                    vhost
                                        从 5.0.3 升级至当前版本
                                        从 5.0.4 升级至当前版本
                                        从 5.0.5 升级至当前版本
                                        从 5.0.6 升级至当前版本
                                        从 5.0.7 升级至当前版本
                                        从 5.1.0 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3 升级至当前版本
                                        从 5.1.4升级至当前版本
                                        从 5.1.5 升级至当前版本
                                        从 6.0.0 升级至当前版本
                                        从 6.1.0 升级至当前版本
                                        从 6.1.1 升级至当前版本
                                        从 6.2.0 升级至当前版本
                                        5.0.3;5.0.5;5.1.1;6.2.0;当前版本
                                        5.0.3;5.1.0;6.0.0;当前版本
                                    vhost+rdma （挑一两个 rdma）
                                        从 5.0.3 升级至当前版本
                                        从 5.0.4 升级至当前版本
                                        从 5.0.5 升级至当前版本
                                        从 5.0.6 升级至当前版本
                                        从 5.0.7 升级至当前版本
                                        从 5.1.0 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3 升级至当前版本
                                        从 5.1.4 升级至当前版本
                                        从 5.1.5 升级至当前版本
                                        从 6.0.0 升级至当前版本
                                        从 61.1 升级至当前版本
                                        从 6.2.0 升级至当前版本
                                        5.1.4;6.2.0-P1;当前版本
                                        5.0.4;5.1.1;6.0.0;当前版本
                                    双活(不常跑)
                                        从 5.0.3 升级至当前版本
                                        从 5.0.4 升级至当前版本
                                        从 5.0.5 升级至当前版本
                                        从 5.0.6 升级至当前版本
                                        从 5.0.7 升级至当前版本
                                        从 5.1.0 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3 升级至当前版本
                                        从 5.1.4 升级至当前版本
                                        从 5.1.5 升级至当前版本
                                        从 6.0.0 升级至当前版本
                                        从 6.1.0 升级至当前版本
                                        从 6.1.1 升级至当前版本
                                        从 6.2.0 升级至当前版本
                                        5.0.3;5.0.6;5.1.4;6.2.0;当前版本
                                centos-to-oe
                                    4.0.8->4.0.14->5.0.5(转oe)->5.1.3->升级至当前版本
                                    4.0.13->5.0.7(转oe)->升级至当前版本
                            el7-x86_64-smtxos-vmware
                                非 rdma
                                    3xx (升级kernel)
                                        3.0.5;3.5.17;4.0.14;5.1.5;当前版本
                                        3.0.21;3.5.1;3.5.10;4.0.5;4.0.12;5.0.6;5.1.4P1;当前版本
                                        3.5.0;3.5.17;4.0.10;5.0.3;5.1.5;当前版本
                                        3.5.17;4.0.12;5.0.7P2;当前版本
                                        3.5.17;4.0.14;5.1.4P2;当前版本
                                    4xx
                                        从 4.0.5 升级至当前版本
                                        从 4.0.6 升级至当前版本
                                        从 4.0.7 升级至当前版本
                                        从 4.0.8 升级至当前版本
                                        从 4.0.9 升级至当前版本
                                        从 4.0.10 升级至当前版本
                                        从 4.0.11 升级至当前版本
                                        从 4.0.12 升级至当前版本
                                        从 4.0.13 升级至当前版本
                                        从 4.0.14 升级至当前版本
                                        4.0.0;4.0.2;4.0.4;4.0.6;4.0.8;4.0.10;4.0.12;4.0.14;当前版本
                                        4.0.1;4.0.5;4.0.9;4.0.11;4.0.13;5.0.6;5.1.4P1;当前版本
                                        4.0.5;4.0.6;4.0.7;4.0.8;4.0.9;4.0.10;4.0.11; 4.0.12;4.0.13;4.0.14;5.1.1;当前版本
                                    5xx
                                        从 5.0.0 升级至当前版本
                                        从 5.0.1 升级至当前版本
                                        从 5.0.2 升级至当前版本
                                        从 5.0.3 升级至当前版本
                                        从 5.0.4 升级至当前版本
                                        从 5.0.5 升级至当前版本
                                        从 5.0.6 升级至当前版本
                                        从 5.0.7 升级至当前版本
                                        从 5.1.0 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3 升级至当前版本
                                        从 5.1.4 升级至当前版本
                                        从 5.1.5  升级至当前版本
                                        从 6.0.0 升级至当前版本
                                        从 6.1.0 升级至当前版本
                                        从 6.1.1 升级至当前版本
                                        从 6.2.0 升级至当前版本
                                        5.0.0;5.0.2;5.0.4;5.1.4;当前版本
                                        5.0.1;5.0.3;5.0.5;5.1.1;当前版本
                                rdma
                                    5xx、6xx(是否挑两个路径就可以)
                                        从 5.0.0 升级至当前版本
                                        从 5.0.1 升级至当前版本
                                        从 5.0.2 升级至当前版本
                                        从 5.0.3 升级至当前版本
                                        从 5.0.4 升级至当前版本
                                        从 5.0.5 升级至当前版本
                                        从 5.0.6 升级至当前版本
                                        从 5.0.7 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3 升级至当前版本
                                        从 5.1.4 升级至当前版本
                                        从 5.1.5 升级至当前版本
                                        从 6.0.0 升级至当前版本
                                        从 6.1.1 升级至当前版本
                                        从 6.2.0 升级至当前版本
                                双活 (低优先级)
                                    40x
                                        从 4.0.10 升级至当前版本
                                        从 4.0.11 升级至当前版本
                                        从 4.0.12 升级至当前版本
                                        从 4.0.13 升级至当前版本
                                        从 4.0.14 升级至当前版本
                                        4.0.10;4.0.14;5.0.6;5.1.5;当前版本
                                    50x
                                        从 5.0.0 升级至当前版本
                                        从 5.0.1 升级至当前版本
                                        从 5.0.2 升级至当前版本
                                        从 5.0.3 升级至当前版本
                                        从 5.0.4 升级至当前版本
                                        从 5.0.5 升级至当前版本
                                        从 5.0.6 升级至当前版本
                                        从 5.0.7 升级至当前版本
                                        从 5.1.0 升级至当前版本
                                        从 5.1.1 升级至当前版本
                                        从 5.1.2 升级至当前版本
                                        从 5.1.3 升级至当前版本
                                        从 5.1.4 升级至当前版本
                                        从 5.1.5 升级至当前版本
                                        5.0.0;5.0.2;5.0.5;5.1.1;当前版本
                                        4.0.11;5.0.3;5.0.5;5.1.5;当前版本
                                    6.x.x
                                        从 6.0.0 升级至当前版本
                                        从 6.1.0 升级至当前版本
                                        从 6.1.1 升级至当前版本
                                        从 6.2.0 升级至当前版本
                                        4.0.11;5.0.3;5.0.5;6.2.0;当前版本
                            oe2003-x86_64-smtxos-vmware
                                非 rdma
                                    从 5.0.6 升级至当前版本
                                    从 5.0.7 升级至当前版本
                                    从 5.1.0 升级至当前版本
                                    从 5.1.1 升级至当前版本
                                    从 5.1.2 升级至当前版本
                                    从 5.1.3 升级至当前版本
                                    从 5.1.4 升级至当前版本
                                    从 5.1.5 升级至当前版本
                                    从 6.0.0 升级至当前版本
                                    从 6.1.0 升级至当前版本
                                    从 6.1.1 升级至当前版本
                                    从 6.2.0 升级至当前版本
                                    5.0.6;5.1.5;当前版本
                                    5.0.6;5.1.1;6.1.1;当前版本
                                rdma(是否挑一个路径就可以)
                                    从 5.0.6 升级至当前版本
                                    从 5.0.7 升级至当前版本
                                    从 5.1.0 升级至当前版本
                                    从 5.1.1 升级至当前版本
                                    从 5.1.2 升级至当前版本
                                    从 5.1.3 升级至当前版本
                                    从 5.1.4 升级至当前版本
                                    从 5.1.5 升级至当前版本
                                    从 6.1.0 升级至当前版本
                                    从 6.1.1 升级至当前版本
                                    从 6.2.0 升级至当前版本
                                    5.1.0;5.1.4;6.2.0;当前版本
                                    5.0.6;5.1.4P1;当前版本
                                双活
                                    从 5.0.6 升级至当前版本
                                    从 5.0.7 升级至当前版本
                                    从 5.1.0 升级至当前版本
                                    从 5.1.1 升级至当前版本
                                    从 5.1.2 升级至当前版本
                                    从 5.1.3 升级至当前版本
                                    从 5.1.4 升级至当前版本
                                    从 5.1.5 升级至当前版本
                                    从 6.0.0 升级至当前版本
                                    从 6.1.0 升级至当前版本
                                    从 6.1.1 升级至当前版本
                                    从 6.2.0 升级至当前版本
                                    5.0.6;5.1.0;6.0.0;当前版本
                                    5.0.7;5.1.4;当前版本
                        SMTXELF
                            x86 oe
                                6.0.0;当前版本 + kernel
                                6.1.0;当前版本 + kernel
                                6.1.1;当前版本 + kernel
                                6.2.0;当前版本 + kernel
                                6.2.0 P4;当前版本 + kernel
                                6.0.0;6.1.1;6.2.0;当前版本
                            arm
                                6.0.0;当前版本 + kernel
                                6.1.0;当前版本 + kernel
                                6.1.1;当前版本 + kernel
                                6.2.0;当前版本 + kernel
                                6.2.0 P4;当前版本 + kernel
                                6.1.0;6.2.0 P4;当前版本
                            tos
                                x86 oe
                                    同版本升级
                                arm
                                    同版本升级
                    TOS
                        hygon tos
                            非 vhost + 非 rdma
                                5.1.4 P1;当前版本
                                5.1.5P1;当前版本
                            vhost
                                5.1.4 P1;当前版本
                                5.1.5;当前版本
                            vhost +  rdma
                                5.1.5;当前版本
                            双活（优先级低）
                                5.1.4 P1;当前版本
                                5.1.5;当前版本
                        arm tos
                            非 vhost + 非 rdma
                                5.1.4 P1;当前版本
                                5.1.5;当前版本
                                5.1.5P1;当前版本
                            vhost
                                5.1.4 P1;当前版本
                                5.1.5;当前版本
                            vhost +  rdma
                                5.1.5 P1;当前版本
                    ACOS
                        smtxos
                            非 vhost + 非 rdma
                                6.1.1;当前版本
                                6.1.1 P1;当前版本
                                6.2.0;当前版本
                                6.2.0 P4;当前版本
                            vhost
                                6.1.1;当前版本
                                6.1.1 P1;当前版本
                                6.2.0;当前版本
                                6.2.0 P4;当前版本
                            双活（低优先级）
                                6.1.1;当前版本
                                6.2.0;当前版本
                                6.1.1 P1;当前版本
                                6.2.0 P4;当前版本
                        vmware
                            6.1.1;当前版本
                            6.1.1 P1;当前版本
                            6.2.0;当前版本
                            6.2.0 P4;当前版本
                场景测试
                    smtxos
                        低版本：5.1.5/620 P4 安装部署全家桶，升级到 630 后各个服务运行正常
                        大规格测试 - 16+ 或 24 节点集群升级测试
                        低版本 lsm 版本是 1.0.0 升级 到 2.3.0 版本
                        低版本集群扩容 /boot 分区后执行升级
                        6.2.0 P4 手动开启 vhost 功能执行升级 630
                        其他运维操作后升级，这个 allinone 会覆盖到，这里就不单独验证
                        rdma 开启后执行升级
                        rdma 关闭后执行升级
                        kvm
                            3.0.5;3.5.16(内核);4.0.13(内核);5.0.6;5.1.5;扩容系统分区;当前版本(生内核)
                        vmware
                            3.0.5;3.5.17;4.0.14(内核);5.0.5;5.1.4;6.2.0;当前版本
                    tos
                        hygon
                            408;5.0.5;转 oe;5.1.4;515; 515P1;转 tl3;当前版本
                        arm
                            409;5.0.3;5.0.7 转 oe;5.1.4;515 P1;转 tl3;当前版本
                    vGPU 测试
                        centos: 5.10.0-247.0.0.el7.v79.x86_64
                        oe: 5.10.0-247.0.0.oe1.v79
                        tos: 5.4.119-19.0009.54.tl3.v99
                    ovs 升级 ovs-coverage( 网络组已经覆盖，可以skip)
                        active-backup [ovs-bond]  配置集群升级到 630
                        active-backup [linux-bond] 升级到 630
                        balance-slb 配置集群升级到 630
                        balance-xor 配置集群升级到 630
                        升级自动化增加检查 ovs 版本： ovs-vsctl --version
        节点管理
            添加节点
                功能测试
                    添加后检查
                        开启 加密加速的集群 - 扩容成功，主机开启加密加速    -  /etc/zbs/crypto_boost_enabled
                        未开启 加密加速 的集群 - 扩容成功 - 主机未开启加密加速
                        部署成功后tower 上面简单检查  -     集群设置 - 加密    -      加密加速 - 已启用
                应用场景测试
                    同时扩容5+节点
            删除节点
                应用场景测试
                    3 节点集群3 master集群，移除1个健康的节点
                    3 节点集群3 master集群，移除1个无响应的节点
                    双活集群 - 移除节点
                    移除chunk 多实例主机
                    移除 全缓存盘主机
                    移除- 分层 全缓存盘 + 独立ssd 节点
                    移除- 分层 缓存盘 + 数据盘 + 独立ssd 节点
                    移除- 分层 全数据盘 节点
                    移除- 分层 全数据盘 + 独立ssd 节点
            角色转换
                应用场景测试
                    角色转换重入 - 转成master -在 primary 节点执行 mongo_member_add 时，停掉 A 的 mongod - 失败后重试成功（TUNA-7660）
                    双活集群，master to storage
                    双活集群， storage to master
                    角色转换 chunk 多实例主机
                    全缓存盘主机 - storage to master
                    全缓存盘主机 - master to storage
                    全缓存盘主机 + 独立ssd - storage to master
                    全缓存盘主机 + 独立ssd  - master to storage
                    分层 全数据盘 节点 - storage to master
                    分层 全数据盘 节点 -  master to storage
                    分层 全数据盘 + 系统盘独立ssd 节点 -  storage to master
                    分层 全数据盘 + 系统盘独立ssd 节点 - master to storage
            zbs 570 部署扩容强制修改密码
                tower：470
                    x86 tower
                    arm tower
                cluster
                    单活 smtxzbs 570+
                        x86-el7-570 新部署
                            留空使用默认密码：部署成功，root、smartx 账户均可以用默认密码（HC!r0cks + 小写的集群序列号前 8 位）访问
                            自定义密码：部署成功，root、smartx 账户均可以用自定义密码访问
                        arm-oe -570 新部署
                            留空使用默认密码：部署成功，root、smartx 账户均可以用默认密码（HC!r0cks + 小写的集群序列号前 8 位）访问
                            自定义密码：部署成功，root、smartx 账户均可以用自定义密码访问
                        x86-el7-570 新部署后扩容
                            自定义密码：扩容成功，root、smartx 账户均可以用自定义密码访问该扩容节点。其他节点仍用部署时设置的原密码
                            留空使用默认密码：部署成功，root、smartx 账户均可以用默认密码（HC!r0cks + 小写的集群序列号前 8 位）访问
                        arm-oe-562 升到 570，扩容
                            留空使用默认密码：扩容成功，root、smartx 账户均可以用默认密码访问该扩容节点。其他节点仍用 HC 密码访问
                            自定义密码：扩容成功，root、smartx 账户均可以用自定义密码访问该扩容节点。其他节点仍用 HC 密码访问
                    双活 SMTXZBS：570+
                        x86-oe 570 新部署
                            留空使用默认密码：部署成功，仲裁节点 & 其他节点的 root、smartx 账户均可以用默认密码访问。
                            自定义密码：部署成功，仲裁节点 & 其他节点的 root、smartx 账户均可以用自定义密码访问
                        x86-oe-570 新部署后扩容
                            留空使用默认密码：扩容成功，root、smartx 账户均可以用默认密码访问该扩容节点。其他节点仍用部署时设置的密码
                            自定义密码：扩容成功，root、smartx 账户均可以用自定义密码访问该扩容节点。其他节点仍用部署时设置的密码
                    单活转双活 SMTX ZBS：570
                        添加节点：3+1，其中1 的密码自定义
                            经确认，zbs 570 不支持单活转双活
                UI 检查
                    部署（单双活部署时的 UI 无差别哈？）
                        Field 默认为空，输入后密码显示为加密
                        点击小眼睛 icon，展示密码
                        格式：至少 8 位字符，必须包含数字、大小写英文字母和特殊字符。
                        两次密码是否一致：两次输入的密码不一致。
                        与默认密码是否一致：不可只使用默认前缀作为密码。
                    扩容
                        系统文案区分：SMTX OS、SMTX ELF、SMTX ZBS
                        Field 默认为空，输入后密码显示为加密
                        点击小眼睛 icon，展示密码
                        格式：至少 8 位字符，必须包含数字、大小写英文字母和特殊字符。
                        两次密码是否一致：两次输入的密码不一致。
                        与默认密码是否一致：不可只使用默认前缀作为密码。
                cluster 通用检查
                    集群节点密码不一致时，做一些运维操作
                        集群升级
                        主机进入维护模式
                        关闭主机
                        重启主机
                        更新集群许可
                        巡检工具执行巡检
                        巡检中心执行巡检
                        采集日志
                    新部署 zbs570 集群&设置密码后
                        检查 cloudtower installer 功能正常，可以做 tower ui 部署
                    扩容后的 zbs570 集群 & 设置密码后
                        检查 cluster installer 功能正常，可以做 tower ui 部署
                    日志
                        部署时的日志里不能展示明文密码
                        扩容时的日志里不能展示明文密码
                tower 通用检查
                    中英文
                        部署界面
                        扩容界面
                        单双活转换界面，同扩容
                    权限
                        有「基础设施-硬件-主机-主机管理」权限的用户，在做主机扩容时要有设置密码的权限
                    事件
                        没有影响，不暴露主机密码
            tower 4.6.0 角色转换和移除节点优化
                移除节点前迁移回收站虚拟机
                    回收站中虚拟机占用存储过多，不能迁移到其他节点 - 其他项不通过（集群中其他主机的空闲存储空间充足 ）
                    smtxos
                        待移除节点关机 & 待移除节点处于维护模式 & 回收站存在虚拟机处于该节点
                            节点移除成功，开启HA的虚拟机迁移到集群其他节点
                            节点移除成功，未开启HA的虚拟机迁移到集群其他节点
                        待移除节点关机 & 待移除节点  不 处于维护模式 & 回收站存在虚拟机处于该节点
                            节点移除成功，开启HA的虚拟机迁移到集群其他节点
                            节点移除成功，未开启HA的虚拟机迁移到集群其他节点
                        待移除节点  开机  & 待移除节点处于维护模式 & 回收站存在虚拟机处于该节点
                            节点移除成功，开启HA的虚拟机迁移到集群其他节点
                            节点移除成功，未开启HA的虚拟机迁移到集群其他节点
                    smtxelf(同 smtxos)
                        待移除节点关机 & 待移除节点处于维护模式 & 回收站存在虚拟机处于该节点
                            节点移除成功，开启HA的虚拟机迁移到集群其他节点
                            节点移除成功，未开启HA的虚拟机迁移到集群其他节点
                        待移除节点关机 & 待移除节点处于不维护模式 & 回收站存在虚拟机处于该节点
                            节点移除成功，开启HA的虚拟机迁移到集群其他节点
                            节点移除成功，未开启HA的虚拟机迁移到集群其他节点
                        待移除节点开机 & 待移除节点处于维护模式 & 回收站存在虚拟机处于该节点
                            节点移除成功，开启HA的虚拟机迁移到集群其他节点
                            节点移除成功，未开启HA的虚拟机迁移到集群其他节点
                角色转换增加 zk 及 mongo 服务状态检查
                    见第3 部分文案重构
                集群变更（角色转换、主机移除）前置检查文案重构
                    移除主机
                        acos elf 文案检查（20项）
                        acos vmware 文案检查（17 项）
                        smtxos elf 文案检查（20项）
                            检查项右侧数字统计检查项总数正确（20）
                            检查项
                                当前主机不是主节点
                                集群中主节点数量满足要求
                                集群中其他主机的 chunk 服务不处于 REMOVING 或 IDLE 状态
                                移除当前主机后，集群中可提供存储服务的主机数满足纠删码卷的要求
                                集群中没有正在添加的主机
                                集群中没有正在进入维护模式的主机
                                集群中没有处于维护模式的其他主机
                                集群中没有正在移除或移除失败的其他主机
                                集群中没有正在转换角色或转换失败的主机
                                集群中没有数据恢复
                                集群中没有 dead pextent
                                集群不处于升级中状态
                                仲裁节点处于健康状态
                                移除当前主机后，优先可用域中至少有 2 个健康的主机，次级可用域中至少有 1 个健康的主机
                                当前主机处于无响应状态或维护模式状态
                                    处于无响应状态  - 存在提示：当前主机处于无响应状态。（注意状态）
                                    不处于无响应状态 - 没有提示（通过状态）
                                当前主机上没有回收站之外的虚拟机
                                    smtxos - 去掉「（移除主机时将自动删除回收站中的虚拟机）」
                                    zbs - ZBS 集群文案改为「当前主机上没有系统服务虚拟机」
                                当前主机上没有被虚拟机挂载的 USB 设备
                                    检查通过
                                    检查不通过 - 展示被 VM 挂载的 USB 设备名
                                集群 ZooKeeper 及 MongoDB 服务正常运行
                                    展示具体主机
                                    只有zk异常
                                    只有monggo 异常
                                    仲裁节点的mongo异常
                                    zk 与mongo 均异常
                                        同一个节点 - zk 与 mongo均异常
                                        不同的节点，有的zk异常，有的mongo异常
                                集群中其他主机的空闲存储空间充足
                                    检测通过
                                    检查不通过 - 提示：预计额外需要 %200 GiB% 的存储空间。
                                集群中没有涉及当前主机的虚拟机放置组
                                    检查项通过
                                    检查项不通过 - 展示关联的 VM 放置组的名称
                            移除节点无响应 tip 提示
                                移除无响应 + 主节点数量通过
                                    其他项通过
                                        提示：我已知晓：当前主机处于无响应状态，在移除主机后，请勿开机（如需使用该主机，请先为其重装系统）
                                    其他项不通过
                                        不提示我已知晓
                                移除无响应 + 主节点数量为2
                                    提示：我已知晓：当前主机处于无响应状态，在移除主机后，请勿开机（如需使用该主机，请先为其重装系统）；集群中将仅存在 2 个健康的主节点，需尽快增加健康主节点的数量。
                        smtxos vmware 文案检查（17项）
                            tip 提示：不支持获取 VMware ESXi 平台的虚拟机，请确保当前主机上没有虚拟机。
                            检查项
                                当前 SCVM 处于无响应状态或维护模式状态
                                当前 SCVM 不是主节点
                                集群中主节点数量满足要求
                                集群 ZooKeeper 及 MongoDB 服务正常运行
                                集群中其他 SCVM 的 chunk 服务不处于 removing 或 idle 状态
                                移除当前 SCVM 后，集群中可提供存储服务的 SCVM 数满足纠删码卷的要求
                                集群中其他主机的空闲存储空间充足
                                集群中没有正在添加的主机
                                集群中没有正在进入维护模式的 SCVM
                                集群中没有处于维护模式的其他 SCVM
                                集群中没有正在移除或移除失败的其他 SCVM
                                集群中没有正在转换角色或转换失败的 SCVM
                                集群中没有数据恢复
                                集群中没有 dead pextent
                                集群不处于升级中状态
                                仲裁节点处于健康状态
                                移除当前 SCVM 后，优先可用域中至少有 2 个健康的 SCVM
                        smtxelf 文案检查（13 项）
                            当前主机处于无响应状态或维护模式状态
                            当前主机上没有回收站之外的虚拟机
                            当前主机上没有被虚拟机挂载的 USB 设备
                            当前主机不是主节点
                            集群中主节点数量满足要求
                            集群 ZooKeeper 及 MongoDB 服务正常运行
                            集群中没有涉及当前主机的虚拟机放置组
                            集群中没有正在添加的主机
                            集群中没有正在进入维护模式的主机
                            集群中没有处于维护模式的其他主机
                            集群中没有正在移除或移除失败的其他主机
                            集群中没有正在转换角色或转换失败的主机
                            集群不处于升级中状态
                    角色转换
                        acos elf 文案检查（10项）
                        acos vmware 文案检查（9 项）
                        smtxos elf 文案检查（10项）
                            检查项
                                当前主机转换角色后，集群中主节点数量满足要求
                                集群中没有数据恢复
                                集群中没有正在添加的主机
                                集群中没有正在进入维护模式的主机
                                集群中没有处于维护模式的其他主机
                                集群中没有正在移除或移除失败的主机
                                集群中没有正在转换角色或转换失败的其他主机
                                集群不处于升级中状态
                                仲裁节点处于健康状态
                                %主机状态等检查%
                                    存储\计算节点 转 主节点
                                        主机健康 + 不处于维护模式 - 满足状态，提示：当前主机处于健康状态，且不处于维护模式状态
                                        主机不健康 + 不处于维护模式 - 未满足状态，提示：当前主机处于健康状态，且不处于维护模式状态
                                        主机健康 + 处于维护模式 - 未满足状态，提示：当前主机处于健康状态，且不处于维护模式状态
                                        集群中其他主机处于健康状态 - 提示：集群中其他主机处于健康状态
                                        集群中存在主机不处于健康状态 - 提示：主机 %hostname-1%、 %hostname-2% 不处于健康状态。
                                    主节点 转 存储\计算节点
                                        集群中全部主机处于健康或无响应状态 - 提示：集群中全部主机处于健康或无响应状态
                                        集群中存在主机处于异常状态 - 提示：主机 %hostname-1%、 %hostname-2% 不处于健康或无响应状态。
                                集群 ZooKeeper 及 MongoDB 服务正常运行
                                    存储节点转 主节点
                                        zk 检查不通过
                                        mongo 检查不通过
                                        zk 与 mongo 检查均不通过
                                            同一个节点 zk与mongo检查不通过
                                            不同的节点，有的zk不通过，有的mongo不通过
                                    主节点转 存储节点
                                        zk 检查不通过
                                        mongo 检查不通过
                                        节点处于无响应状态
                                        节点处于健康状态
                                        zk 与 mongo 检查均不通过
                                            同一个节点 zk与mongo检查不通过
                                            不同的节点，有的zk不通过，有的mongo不通过
                        smtxos vmware 文案检查（9项）
                            %SCVM 状态等检查%
                            当前 SCVM 转换角色后，集群中主节点数量满足要求
                            集群 ZooKeeper 及 MongoDB 服务正常运行
                            集群中没有数据恢复
                            集群中没有正在添加的主机
                            集群中没有正在进入维护模式的 SCVM
                            集群中没有处于维护模式的其他 SCVM
                            集群中没有正在移除或移除失败的 SCVM
                            集群中没有正在转换角色或转换失败的其他 SCVM
                            集群不处于升级中状态
                        smtxelf 文案检查（9项）
                            当前主机转换角色后，集群中主节点数量满足要求
                            集群中没有正在添加的主机
                            集群中没有正在进入维护模式的主机
                            集群中没有处于维护模式的其他主机
                            集群中没有正在移除或移除失败的主机
                            集群中没有正在转换角色或转换失败的其他主机
                            集群不处于升级中状态
                            仲裁节点处于健康状态
                            %主机状态等检查%
                                存储\计算节点 转 主节点
                                    主机健康 + 不处于维护模式 - 满足状态，提示：当前主机处于健康状态，且不处于维护模式状态
                                    主机不健康 + 不处于维护模式 - 未满足状态，提示：当前主机处于健康状态，且不处于维护模式状态
                                    主机健康 + 处于维护模式 - 未满足状态，提示：当前主机处于健康状态，且不处于维护模式状态
                                    集群中其他主机处于健康状态 - 提示：集群中其他主机处于健康状态
                                    集群中存在主机不处于健康状态 - 提示：主机 %hostname-1%、 %hostname-2% 不处于健康状态。
                                主节点 转 存储\计算节点
                                    集群中全部主机处于健康或无响应状态 - 提示：集群中全部主机处于健康或无响应状态
                                    集群中存在主机处于异常状态 - 提示：主机 %hostname-1%、 %hostname-2% 不处于健康或无响应状态。
                            集群 ZooKeeper 及 MongoDB 服务正常运行
                                zk 检查不通过
                                mongo 检查不通过
                                zk 与 mongo 检查均不通过
                                    同一个节点 zk与mongo检查不通过
                                    不同的节点，有的zk不通过，有的mongo不通过
                集群变更（角色转换、主机移除）支持 zbs 5.7.0
                    关联 zbs 5.7.0 集群后 - tower上不能角色转、移除节点
                命令行移除主机前置检查：目标主机是否存在 vm 文案调整
                    tower ui 移除 SCVM 主机，执行成功
                    命令行移除scvm，移除成功，提示正确
                回归
                    acos 6.2.0
                    smtxos vmware 6.2.0
                    smtxelf 6.2.0
                    smtxos elf 6.2.0
                        arm
                        hygon
                        x86
                    应用场景
                        3节点smtx os集群 - 1 master 节点无响应
                            无响应master 角色转换 + 移除节点 - 提示正确
                        3节点smtxelf集群 - 1 master 节点无响应
                            无响应master 角色转换 + 移除节点 成功 - 提示正确
                        4节点集群 - 1 master 节点无响应
                            无响应主机 角色转换+移除节点 - 成功
                        5 节点 5 master 集群，2个master节点无响应
                            对无响应节点 角色转换+移除节点 - 成功
        6.1.0 安装部署升级
            discard
                安装：OS 盘且 /sys/block/{}/queue/discard_granularity 非 0 才执行 blkdiscard
                部署：OS 盘的非系统分区及数据盘都会执行
        TencentOS
            license 激活 -  离线激活方式
            安装/升级 os 后操作系统版本&配置检查
                服务检查
                    预留内存是否符合预期
            运维功能 &产品适配+Tower UI check
                升级中心
                    安装部署后版本显示 5.1.4 P1，服务组件信息显示正确，后端查看 hpctl 和 hotfix-package
                    升级后版本显示 5.1.4 P1，服务组件信息显示正确，后端查看 hpctl 和 hotfix-package
                    5.1.4 P1 tos 升级到 5.1.5 tos 成功
                    5.1.4 P1 tos 升级到 5.1.4 tos 成功
                    5.1.4 P1 tos vhost 升级到 5.1.5 tos 成功
                    5.1.5 arm 非 tos 的升级文件不能上传到 tos 集群
                    5.1.5 hygon 非 tos 的升级文件不能上传到 tos 集群
                    非 tos 5.1.4 补丁文件上传Tower，关联 tos 没有内置补丁包的集群不可见非 tos 5.1.4 补丁文件
                    升级中心服务 v1.1.1-rc.1 升级到 Tower4.5.0 上可以对 非 tos 集群上传升级文件并执行升级
                    非 tos 5.x.x 升级到 5.1.5 版本成功
                    tos tower 内置升级中心 v1.0.1-rc.3 的服务
            独立SSD 支持
                磁盘管理
                    标准容量规格
                        不分层部署
                            可以正常卸载数据盘
                            新挂载数据盘
                                可以正常挂载 > 30 GiB 的磁盘
                                不可挂载 ≤ 30 GiB 的磁盘
                            不可挂载含元数据分区的盘
                                tower 界面
                                fisheye 界面
                                命令行
                            同时存在独立部署和非独立部署的集群可以正常挂载含元数据分区的盘
                                系统分区
                                元数据分区
                                Journal 分区 10 GiB
                                未分区 10 GiB
                                剩下全部为数据分区
                        分层部署不共享磁盘
                            可以正常卸载缓存盘
                            可以正常挂载&卸载数据盘
                            新挂载缓存盘
                                可以正常挂载 > 20 GiB 的磁盘
                                不可挂载 ≤ 20 GiB 的磁盘
                            不可挂载含元数据分区的盘
                                tower 界面
                                fisheye 界面
                                命令行
                            同时存在独立部署和非独立部署的集群可以正常挂载含元数据分区的盘
                                系统分区
                                元数据分区
                                Journal 分区 10 GiB
                                未分区 10 GiB
                                剩下全部为缓存分区
                        tower 展示系统盘信息
                            原  nohalo （= not os in soft raid1）部署方式下的系统盘展示情况
                            组织/数据中心/集群层（主机 tab页）
                                新增一列「SMTX 系统盘」，位于 「状态后」后一位
                                排序
                                磁盘列表不展示独立部署的系统盘
                                    不分层
                                    分层不共享盘
                                    分层且共享盘
                            主机详情页
                                SMTX 系统盘 Widget
                                    名称
                                    状态
                                    成员盘
                                    详情跳转 btn
                                详情 Tab
                                    监控（提供「存储性能」相关指标，同普通物理盘」）
                                    标签
                                    详情
                                        虚拟盘盘符;状态;类型;总容量;型号;固件版本;所属数据中心;所属集群;所属主机;用途与分区（元数据分区、引导分区、EFI 系统分区、系统分区、未分区）
                                    成员物理盘
                                        M.2 SATA 型号
                                            编号;状态;剩余寿命;类型;型号;固件版本;序列号
                                            more btn
                                                闪灯
                                                停止闪灯
                                        M.2 NVMe Dell
                                            编号;状态;剩余寿命;类型;型号;固件版本;序列号
                                            more btn
                                                闪灯
                                                停止闪灯
                                        M.2 NVMe Lenovo
                                            编号;状态;剩余寿命;类型;型号;固件版本;序列号
                                            more btn
                                                闪灯
                                                停止闪灯
                                        Boardcom 型号
                                            编号;状态;剩余寿命;类型;型号;固件版本;序列号
                                            more btn
                                                闪灯
                                                停止闪灯
                    故障测试
                        独立部署节点
                            硬 RAID 下虚拟盘（VD）物理盘数量冗余度
                                中文
                                    报警文案：主机 { .labels.hostname } 硬件 RAID 下的虚拟盘 { .labels._vd_name } 冗余度不足。
                                    触发原因：硬件 RAID 下组成虚拟盘的物理盘数量少于二。
                                    影响：当前无影响。如果硬件 RAID 下虚拟盘中的最后一块物理盘损坏，可能导致服务器无法正常启动，或启动后系统运行异常。
                                    解决方法：按需增加物理盘数量，重新配置硬件 RAID下的虚拟盘，纠正错误状态。
                                    报警等级：注意
                                英文
                                    报警文案：The hardware RAID virtual disk on the host { .labels.hostname } has insufficient redundancy.
                                    触发原因：The number of physical disks constituting the hardware RAID virtual disk is less than two.
                                    影响：Currently no impact. However, if the last physical disk constituting the hardware RAID virtual disk is damaged, the server might not be able to boot properly; if the server can be booted, the system might encounter exceptions.
                                    解决方法：Increase the number of physical disks as needed, and reconfigure the hardware RAID virtual disk to correct its error state.
                                    报警等级：Notice
                                成员盘 Table
                                    成员物理盘少于两块（存在成员物理盘）触发告警
                                    暂不支持从当前硬件中获取成员物理盘信息 不触发告警
                                系统盘详情 Table
                                    状态变更为异常
                                    出现异常 Tip
                                主机详情页
                                    只展示一块成员盘时状态更改为异常
                                    没有识别到成员盘时状态为正常，且不展示成员盘信息
                                组织/数据中心/集群层
                                    概览页出现 异常 tip
                                    主机 Table 的 「SMTX 系统盘」 展示为异常
                            硬 RAID 下物理盘（PD）的 S.M.A.R.T. 自检
                                中文
                                    报警文案：主机 { .labels.hostname } 硬件 RAID 下的物理盘 { .labels._serial } S.M.A.R.T. 检测不通过。
                                    触发原因：硬件 RAID 下的物理盘 S.M.A.R.T. 检测异常。
                                    影响：硬件 RAID 下的物理盘故障风险显著提高。
                                    解决方法：联系售后技术支持，更换物理盘。
                                    报警等级：严重
                                英文
                                    报警文案：The physical disk { .labels._serial } in hardware RAID on the host { .labels.hostname } failed the S.M.A.R.T. test.
                                    触发原因：The physical disk in hardware RAID failed the S.M.A.R.T. test.
                                    影响：The physical disk has a significant risk of failure.
                                    解决方法：Contact technical support to replace the physical disk.
                                    报警等级：Critical
                                成员盘 Table
                                    状态变更为异常
                                    出现异常 Tip （ S.M.A.R.T. 不通过）
                                系统盘详情 Table
                                    状态变更为异常
                                    出现异常 Tip （存在 %N% 块 S.M.A.R.T. 不通过的成员物理盘）
                                主机详情页
                                    状态变更为异常
                                    对应成员盘的状态变更为 S.M.A.R.T. 不通过
                                组织/数据中心/集群层
                                    概览页出现 异常 tip
                                    主机 Table 的 「SMTX 系统盘」 展示为异常
                            硬 Raid 下物理盘（PD）的寿命不足报警
                                不影响到系统盘状态
                                不影响组织/数据中心/集群层的概览、主机 Table 界面
                                中文
                                    报警文案：主机 { .labels.hostname } 硬件 RAID 下的物理盘 { .labels._serial } 寿命不足 { .threshold}。
                                    触发原因：检测到硬件 RAID 下的物理盘预期寿命不足。
                                    影响：物理盘寿命到期后，故障风险和性能下降的概率将显著提高。
                                    解决方法：联系售后技术支持，更换物理盘。
                                    报警等级：注意（阈值默认 20%）
                                英文
                                    报警文案：The physical disk { .labels._serial } in hardware RAID on the host { .labels.hostname } has a remaining lifespan below { .threshold }.
                                    触发原因：The physical disk in hardware RAID has an insufficient lifespan.
                                    影响：After the physical disk reaches the end of its lifespan, its risk of failure and possibility of performance degradation will increase significantly.
                                    解决方法：Contact technical support to replace the physical disk.
                                    报警等级：Notice (default threshold 20%)
                                成员盘 Table
                                    状态不变
                                    剩余寿命正常更新
                                主机详情页
                                    状态不变
                                    对应成员盘的状态正常更新
                            硬 RAID 下的虚拟盘（VD）状态
                                中文
                                    报警文案：主机 { .labels.hostname } 硬件 RAID 下的虚拟盘 { .labels._vd_name } 状态异常：{ .labels.status }。
                                    触发原因：硬件 RAID 下的虚拟盘状态异常。
                                    影响：硬件 RAID 下的虚拟盘可能无法被系统正常使用。
                                    解决方法：重新配置硬件 RAID下的虚拟盘，纠正错误状态。
                                    报警等级：严重
                                英文
                                    报警文案：The hardware RAID virtual disk { .labels._vd_name } on the host { .labels.hostname } is abnormal.
                                    触发原因：The hardware RAID virtual disk is abnormal.
                                    影响：The hardware RAID virtual disk might not function properly.
                                    解决方法：Reconfigure the hardware RAID virtual disk to correct its error state.
                                    报警等级：Critical
                                系统盘详情 Table
                                    状态变更为异常
                                    出现异常 Tip （硬 RAID 下的虚拟盘状态异常）
                                主机详情页
                                    状态变更为异常
                                    不影响成员盘的信息
                                组织/数据中心/集群层
                                    概览页出现 异常 tip
                                    主机 Table 的 「SMTX 系统盘」 展示为异常
                        非独立部署节点
                            验证冗余度不足告警是否生效
                            验证 RAID 告警是否生效
                        拔盘测试
                            闪灯确认待更换盘的位置;若为 SATA/NVMe 且非 Boardcom 的服务器关机;拔盘;插盘;若服务器关机，则开机;手动恢复 RAID 组;检查 tower 界面信息
        515 write cache 检查
            文档检查
            回归测试（同 smtxos 5.1.4 tl3）
            部署
                可以获取到硬 raid1 所用的 Write Cache 策略
                    博通 控制器
                    Write Cache 为 Write Through
                        软raid 安装后部署  - 部署成功（没有相关提示）
                        系统盘独立ssd安装后部署  - 部署成功（没有相关提示）
                        系统盘独立ssd安装但是选择其他磁盘作为独立系统盘，博通控制器下面的磁盘用作其他用途 - 部署成功（有提示）
                    Write Cache 不为 Write Through
                        软raid安装后部署  - 部署成功（没有相关提示）
                        系统盘独立ssd安装但是选择其他磁盘作为独立系统盘，博通控制器下面的磁盘(vd)用作其他用途 - 部署成功（有提示）
                        系统盘独立ssd安装后部署  - 不允许部署（有相关提示）
                            主机置灰，不允许选择
                            提示：该主机的操作系统部署在独立物理盘上，但硬件 RAID 的 Write cache 没有设置为 Write through 策略，存在数据丢失隐患。
                无法获取到硬 raid1 所用的 Write Cache 策略
                    其他控制器
                        eg：Marvell NVMe M.2（Dell BOSS-N1）
                        软raid 安装后部署  - 部署成功（没有相关提示）
                        系统盘独立ssd安装后部署   - 部署成功（有相关提示）
                            点击“配置存储” - UI有弹窗
                            不勾选（默认）“我已确认：以下主机的硬件 RAID 的 Write cache 已设置为 Write through 策略” - 不可以进行下一步
                            勾选“我已确认：以下主机的硬件 RAID 的 Write cache 已设置为 Write through 策略” - 可以进行下一步
                            再次点击配置存储 - 进入配置存储页面
                            弹窗提示 - 选中的 3 台主机的操作系统部署在独立物理盘上：
                                主机数量&主机名称提示正确
                                部分主机软radi安装，部分主机硬raid 安装 - 主机数量&主机名称提示正确
                                部分主机可以感知到Write cache策略，部分主机感知不到write cache 策略 - 主机名&主机数量提示正确
            扩容
                可以获取到硬 raid1 所用的 Write Cache 策略
                    博通 控制器
                    Write Cache 为 Write Through
                        软raid 安装后扩容  - 扩容成功（没有相关提示）
                        系统盘独立ssd安装后扩容  - 扩容成功（没有相关提示）
                        系统盘独立ssd安装但是选择其他磁盘作为独立系统盘，博通控制器下面的磁盘(vd)用作其他用途 - 扩容成功（有相关提示）
                        集群的控制节点为独立ssd安装但不能感知write cache ， 添加节点为硬raid 并且可以感知到write cache - 扩容成功&没有提示
                    Write Cache 不为 Write Through
                        软raid安装后扩容  - 部署成功（没有相关提示）
                        独立系统盘后扩容  - 不允许部署（有相关提示）
                        系统盘独立ssd安装但是选择其他磁盘作为独立系统盘，博通控制器下面的磁盘(vd)用作其他用途  - 扩容成功（有相关提示）
                无法获取到硬 raid1 所用的 Write Cache 策略
                    其他控制器
                        软raid安装后扩容  - 扩容成功（没有相关提示）
                        系统盘独立ssd安装后扩容  - 扩容成功（有相关提示）
                            点击“下一步” - UI有弹窗
                            不勾选（默认）“我已确认：以下主机的硬件 RAID 的 Write cache 已设置为 Write through 策略” - 不可以进行下一步
                            勾选“我已确认：以下主机的硬件 RAID 的 Write cache 已设置为 Write through 策略” - 可以进行下一步
                            再次点击“下一步” - 进入配置存储页面
                            安装为硬raid 但是选择的磁盘不在博通控制器下面  - 部署成功（有相关提示）
                            弹窗提示 - 选中的 3 台主机的操作系统部署在独立物理盘上：
                                主机数量&主机名称提示正确
                                部分主机软radi安装，部分主机硬raid 安装 - 主机数量&主机名称提示正确
                                部分主机可以感知到Write cache策略，部分主机感知不到write cache 策略 - 主机名&主机数量提示正确
            报警
                可以获取到硬 raid1 所用的 Write Cache 策略
                    博通 控制器
                    控制器 Write Cache 为 Write Through
                        软raid安装后部署  - 没有报警
                        系统盘独立ssd安装后部署  - 没有报警
                        系统盘独立ssd安装但是选择其他磁盘作为系统盘，博通控制器下面的磁盘(vd)用作其他用途- 没有报警
                    控制器Write Cache 不为 Write Through
                        软raid安装后部署  - 没有报警
                        系统盘独立ssd安装但是选择其他磁盘作为系统盘，博通控制器下面 的磁盘(vd)用作其他用途 - 没有报警
                        安装为硬raid  - 有报警
                            主机 { .labels.hostname } 系统盘所在的硬件 RAID 下的虚拟盘 { .labels._vd_name } 的 Write Cache 策略非  Write Through，请尽快进行调整，以便正常完成后续操作。
                            触发原因：硬件 RAID 下的虚拟盘的 Write Cache 策略非预期的 Write Through 策略。
                            影响：使用了硬件 RAID 下的虚拟盘在遇上断电场景时可能会导致数据丢失。
                            解决方法：重新配置硬件 RAID 下的虚拟盘的 Write Cache 策略为 Write Through 策略。
                            报警等级：严重
                            The Write Cache policy of hardware RAID virtual disk { .labels._vd_name } on which the system disk of the host { .labels.hostname } resides is not Write Through, please reconfigure it soon.
                无法获取到硬 raid1 所用的 Write Cache 策略
                    其他控制器
                        软raid安装- 部署后没有报警
                        系统盘独立ssd安装 - 部署后没有报警
            独立系统盘
                smtx系统盘异常（回归）  - 提示包含4条情况
                smtx系统盘异常 - 硬件 RAID 的 Write cache 没有设置为 Write through 策略 - 提示包含4条情况
                smtx系统盘健康 - 可以正常显示
            升级
                smtxos 升级
                    x86\oe 低版本升级到smtxos 5.1.5
                        主机安装为软raid - 没有报警
                        不使用软raid安装（就版本的方式），write cache不是write through - 没有报警
                    tls 低版本升级到smtxos 5.1.5
                        主机安装为软raid - 没有报警
                        系统盘独立ssd安装，write cache不是write through - 有报警
                tower 升级
                    tower从低版本升级到 tower 4.4.2
                        x86\oe 版本
                            系统盘独立ssd安装，write cache不是write through - 有报警
                        tl3 版本
                            系统盘独立ssd安装，write cache不是write through - 有报警
                    tower从低版本升级到 tower 4.6.0
                        x86\oe 版本
                            系统盘独立ssd安装，write cache不是write through - 有报警
            tl3 与其他平台的tower，集群相互关联
                tower-441-tencent & smtxos-514-HP1-tencent需要绑定使用，不需要考虑交叉
                tower 442 tl3关联 smtxos 5.1.4 tl3 集群
                    系统盘独立ssd安装 - 可以正常扩容
                    5.1.4 节点使用软raid 安装 - 可以正常扩容
                tower 442 tl3关联 smtxos 5.1.5 tl3 集群
                    软raid 安装 可以正常扩容
                    系统盘独立ssd安装 - 可以正常扩容
                    可以正常显示独立系统盘
                tower 442 tl3关联 smtxos 5.1.4 oe 集群
                    5.1.4 节点不使用软raid 安装（旧版本的方式） - 不允许扩容
                    5.1.4 节点使用软raid 安装 - 可以正常扩容
                tower 442 tl3关联 smtxos 5.1.5 oe 集群
                    可以正常显示独立系统盘
                    软raid 安装 可以正常扩容
                    系统盘独立ssd安装 - 可以正常扩容
                tower 442 x86 关联 smtxos 514 oe 集群
                    5.1.4 节点不使用软raid 安装（旧版本的方式） - 可以正常扩容
                    5.1.4 节点使用软raid 安装 - 可以正常扩容
                tower 442 x86 关联 smtxos 515 oe 集群
                    可以正常显示独立系统盘
                    软raid 安装 可以正常扩容
                    系统盘独立ssd安装 - 可以正常扩容
                tower 442 x86 关联 smtxos 515 tl3 集群
                    可以正常显示独立系统盘
                    软raid 安装 可以正常扩容
                    系统盘独立ssd安装 - 可以正常扩容
                tower 442 x86 关联 smtxos 514 tl3 集群
                    不支持这种方式
            支持的版本
                smtxelf - 不支持
                smtxos
                    620 后续版本 - 不在此次测试范围
                    515 及 后续版本
                        tower 4.6.0
                        tower 4.4.2（主要测试）
                        vmware 平台  - 不支持
                        smtxos
                            x86
                            arm
                                tl3
                                oe
                            hygon
                                tl3
                                oe
                tower 4.6.0
                    acos（注意英文）
                    tower
                tower 4.4.2
                    oe
                    x86
                    tl3
                smtxzbs
                    570及后续版本 - 不在此次测试范围
        515 hp 腾讯os 转换
            平台架构
                arm
                    409 -> 5.0.5  -> 转 oe -> 514->根分区扩容 ->515P1 -> 转 tl3
                    4010 ->505 ->转oe -> 515->补丁到P1 ->转 tl3
                    4014 -> 507 ->转oe ->515P1 -> 转 tl3
                    506 oe -> 515p1 -> 升级kernel -> 转 tl3
                    507 oe - > 515 p1->转tl3 -> 630 -> 升级kernel
                    510 oe -> 515 -> 转 tl3
                    513 hp - >515hp -> 转 tl3 -> 原地补丁 515 hp1
                hygon
                    4.0.8 -> 5.0.5  -> 转 oe -> 513 ->515hp -> 转 tl3
                    4010 ->505 ->转oe -> 515hp1 ->转 tl3
                    4014 -> 507 ->转oe ->hp->515hp1 -> 转 tl3
                    505 oe -> 515hp1 -> 转 tl3
                    507 oe - > 515hp1 ->转tl3 -> 升级中心 630 -> 升级kernel
                    511 oe -> 515hp1 ->升级kernel-> 转 tl3
                    512 hp - >515hp1 -> 转 tl3 -> 原地补丁
            场景测试
                3节点集群
                5节点集群
                5节点以上集群
                双活集群
                hygon 安装部署UEFI 引导， 升级之后转换
                hygon 安装部署 BIOS 引导， 升级之后转换
                转换一个节点之后，检查虚拟机可以从oe->tl3
                转换部分节点之后，检查虚拟机可以从tl3-> oe
                物理环境大量数据规格下转换测试(较多虚拟机开机、虚拟卷，集群资源占用比较多)
                静态路由部署的双活集群
                部署&关联全家桶集群& enable feature
                    转tl3 成功
                    系统服务功能转换前后正常，不受影响
                    检查业务虚拟机的状态和功能正常
                集群特性
                    集群开启vhost 和rdma
                    网络融合
                    bonding 模式
                    DRS
                    节点开启iommu，转换之后检查iommu 状态
                    节点独立ssd 部署，转换之后检查状态
                运维场景组合
                    低版本升级一路升级上来，之后到515 扩容新节点，之后再转tl3
                    低版本升级一路升级上来，之后到515 操作角色转换、移除节点，之后再转tl3
                    集群低版本升级上来，转tl3 之后，操作角色转换、维护模式、添加主机、移除节点
            异常测试
                集群x86 oe 执行转换工具提示错误
                centos 执行提示错误
                已经是tl3 的执行工具
                集群版本不是515hp 而是515 ，执行转换工具，预期提示错误
                执行转换的时候集群有数据恢复
                转换过程中的主机异常
                    第一次重启之后，转换过程中，主机存储网络断开
                    第一次重启之前，主机断电重启
                    第一次重启之后，转换过程中断电
            转换测试
                进入维护模式
                正常下载转换工具&解压
                检查服务状态（已有的命令行，不做扩展测试，遇到什么测试什么）
                清理工具包
                退出维护模式
                下载错误的包（比方uefi下载了bios），会提示错误
                在非smartx 目录下面执行解压，会提示错误
                precheck
                    虚拟机关机检查
                        有开机虚拟机 -检查不通过
                        有暂停虚拟机-检查不通过？
                        未知状态虚拟机 - 维护模式会检查位置状态虚拟机，此条用例可以跳过
                        无开机虚拟机 -检查通过
                    存储网络 MAC 配置信息
                        存在
                        存储网络配置不存在
                        正确性不校验
                        接入网络-配置存在
                        接入网络-配置不存在
                        管理网络-配置不存在
                    检查当前安装的 Kernel 包数量
                        kernel 包超过1个
                        kernel 包1 个
                        kernel 是否和最新的rpm 匹配
                    检查根分区空间使用率
                        剩余空间不足10G
                        剩余空间超过10 G
                    是否存在 ISO 9660 设备挂载
                        存在
                        不存在
                    当前节点GRUB 配置
                        正确
                        不正确 -检查bios 和 uefi 对应的路径下没有配置文件
                            /boot/efi/EFI/$distro/grub.cfg
                            /boot/grub2/grub.cfg 或者 /etc/grub2-efi.cfg
                            /etc/default/grub
                    检查 efi 挂载点是否正常挂载
                        存在或者bios 引导
                        不存在
                执行转换
                    转换命令行参数提示检查
                    转换成功
                    转换时间看下
                    -- dryrun 检查
                    自动重启
                        重启成功
                        成功之后再物理主机开机检查下开机启动页面是否提示tl3
                        重启失败
                    转换失败
                        节点无法启动？
                        支持重试？ 手动重启尝试下
            转换后检查点
                可观测采集的指标正常（看下agent 是否正常运行）
                告警信息 - 集群无异常告警信息
                巡检中心
                系统检查
                    系统检查 - 使用uname -r查看节点kernel版本:
                    系统检查 - 查看节点操作系统是否为：XXX tl3 （cat  /etc/redhat-release）
                    系统检查 - 内核启动配置文件中为 tencent os（/boot/grub/grub.conf 或者 /boot/efi/EFI/$distro/grub.cfg或者cat /etc/default/grub ）
                    系统检查 - hostnamectl命令获取操作系统的详细信息
                    转tl3后，启动文件中/proc/cmdline kernel更新正确
                服务检查
                    服务检查 - 检查节点上的服务运行正常
                    服务检查 - 查看节点rpm包和515 tl3 版本(新安装部署)预期是一致的
                    全文件的比对
                转成功后，重启节点过程中，重启界面kernel和操作系统都为tl3
                    hygon
                    arm
                转 tl3 后是否还要验证一下 license 激活
                    kms
                    离线 ---不用测
                转换后功能回归
                    sre all in one
                    elf all in one
                    zbs all in one
                    network all in one
        6.3.0 多实例、跨网卡bonding 安装部署扩容
            RDMA 使用 ovs bonding，跨网卡bonding
                部署
                    RDMA + 同一网卡间 bond（cx4 / cx5 / cx6 任意选一即可）+ ovs ab，功能正常，流控正常。
                    RDMA + 跨网卡 bond（4 网口，cx4 / cx5）+ ovs balance-tcp，功能正常，流控正常，多路径正常。
                    开启 RDMA，部署时不支持 balance-slb bond
                    部署时存储网启用 RDMA，选择关联网口时，可以选择不同网卡的网口
                    部署时存储网启用 RDMA，关联网口选择多个后，展示网口绑定模式，默认选择 active-backup，仅支持选择 active-backup 和 balance-tcp
                    rdma + active-backup 模式 - 选择相同网卡的两个网口 -  部署成功，bonding为ovs bond
                    rdma + active-backup 模式   - 选择不同cx4 网卡的两个网口 - 部署成功，bonding为ovs bond
                    rdma + active-backup 模式 - 选择不同型号的网卡（cx4+cx5）的两个网口 - 部署成功，bonding为ovs bond
                    rdma + balance-slb - 不支持
                    rdma + balance-tcp 模式 - 选择相同网卡的两个网口 - 部署成功，bonding为ovs bond
                    rdma + balance-tcp 模式 - 选择不同cx4 网卡的两个网口 - 部署成功，bonding为ovs bond
                    rdma + balance-tcp 模式 - 选择不同型号的网卡（cx4+cx5）的两个网口 - 部署成功，bonding为ovs bond
                    active-backup 模式-  部署成功，bonding为ovs bond
                    balance-slb - 部署成功，bonding为ovs bond
                    balance-tcp 模式 - 部署成功，bonding为ovs bond
                    bonding 配置文件符合预期 - (/etc/zbs/chunk_storage_network_config)
                    vmware + rdma - 选择相同网卡的两个网口 -  部署成功，bonding为ovs bond
                    vmware + rdma  - 选择不同网卡的两个网口 -  部署成功，bonding为ovs bond
                    vmware + rdma - 选择不同型号的不同网卡的两个网口 - 部署成功，bonding为ovs bond
                    vmware - 选择相同网卡的两个网口 -  部署成功，bonding为ovs bond
                    vmware  - 选择不同网卡的两个网口 - 部署成功，bonding为ovs bond
                    vmware  - 选择不同型号的不同网卡的两个网口 - 部署成功，bonding为ovs bond
                交换机相关
                    开启 RDMA，部署时选择的网卡跨交换机（M-LAG 或堆叠），bond 可以选择（ovs-ab / ovs balance-tcp），balance-tcp 必须验证。部署正常，集群可正常工作。
                    开启 RDMA，部署时选择的网卡跨交换机（M-LAG 或堆叠），bond 可以选择（ovs-ab / ovs-balance-tcp），升级正常，集群可正常工作。
                添加主机
                    rdma + active-backup 模式 - 选择相同网卡的两个网口 -  添加成功，bonding为ovs bond
                    rdma + active-backup 模式   - 选择不同cx4 网卡的两个网口 - 添加成功，bonding为ovs bond
                    rdma + active-backup 模式 - 选择不同型号的网卡（cx4+cx5）的两个网口 - 添加成功，bonding为ovs bond
                    rdma + balance-slb - 不支持
                    rdma + balance-tcp 模式 - 选择相同网卡的两个网口 - 添加成功，bonding为ovs bond
                    rdma + balance-tcp 模式 - 选择不同cx4 网卡的两个网口 - 添加成功，bonding为ovs bond
                    rdma + balance-tcp 模式 - 选择不同型号的网卡（cx4+cx5）的两个网口 - 添加成功，bonding为ovs bond
                    集群存储网启用了 RDMA 且为 ovs bond 时，添加主机选择关联网口时，支持选择不同网卡上的网口
                    集群存储网启用了 RDMA 且为 linux bond 时，添加主机选择关联网口时，禁止选择不同网卡上的网口
            移除主机
                normal
                    分层
                        1实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                        2实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                    不分层
                        1实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
                        2实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
                large
                    分层
                        1实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                        2实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                        4实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                    不分层
                        1实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
                        2实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
                        4实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
            角色转换
                normal
                    分层
                        1实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                        2实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                    不分层
                        1实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
                        2实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
                large
                    分层
                        1实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                        2实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                        4实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                    不分层
                        1实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
                        2实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
                        4实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
            目标版本
                软件版本
                    SMTX OS 6.3.0
                    CloudTower 4.8
                CPU 架构
                    intel
                    hygon
                        oe
                        tl3
                    arm（鲲鹏）
                        oe
                        tl3
            产品架构
                多实例模式为节点属性，不会有集群级别的属性
                两个系统盘没强制要求在第一个磁盘池
                部署集群或者添加节点时可选择实例数量
                    可以逐个指定
                    支持的实例数量为 1，2，4 总计 3 种
                        节点为单实例等价于节点没有开启多实例
                        硬盘池少的节点会成为集群性能瓶颈。
                        文档中有提示
                不同硬盘池必须是相同的分层模式
                    不开启分层
                    开启分层
                        全闪分层
                        混闪分层
                限制
                    集群部署后不支持修改节点的硬盘池数量
                    单硬盘池数据分区容量上限 256TiB，缓存分区总容量上限 51TiB
                    ｜ 可以通过将节点删除，再加回来时设置多实例
                        升级集群默认每个节点一个硬盘池，对应一个 chunk 实例
                        ｜ 可以通过移除节点再添加回来的方式，为新添加的节点开启多 chunk 实例
                            规格不支持在线更改
                            ｜ 离线状态可以通过扩容系统分区的方式调整
                            ｜ 产品不支持
                        命令行没有限制 chunk 实例的操作
                            移除 chunk 实例
                                先 zbs-meta storage_pool remove_chunk，然后 zbs-meta chunk remove
                            添加 chunk 实例
                                zbs-meta chunk register
                    硬盘池数量上限为 255
                        硬盘池按照 ID 从小到大的顺序依次向 Meta 进行注册
                        qa 覆盖 12 * 4
                配置文件调整
                    在确定实例数后，需要在配置持久化在 /etc/sysconfig/zbs-chunkd 中（不注入代表实例为 1）
                    ｜ CHUNK_COUNT=N
            部署集群
                节点 CPU 和内存满足多硬盘池对计算资源的需求
                Normal
                    CPU
                        单 CPU 最小物理核心数 12，总逻辑核心数量(HT 之后) ≥ 48
                            总逻辑核心数 < 48 - 不满足条件
                            总逻辑核心数 = 48
                            总逻辑核心数 > 48
                            单 CPU 最小物理核心数 < 12
                            单 CPU 最小物理核心数 = 12
                            单 CPU 最小物理核心数 > 12
                        CPU 内每个 NUMA Node 包含的物理核心数 ≤ 6，推荐 ≥ 8
                            6
                                不支持开启多实例模式
                            8
                                支持开启多实例模式
                    内存 128 G
                        < 128G  - 不满足条件
                        ≥ 128G
                    部署场景
                        存储分层模式
                            OS 安装在独立的硬 RAID 1
                                混闪配置
                                    ｜ 一般两种，比如 NVMe SSD + HDD
                                        系统盘
                                            ｜ 2 块 SSD 和存储控制器构建硬 RAID 1
                                                预留空间
                                                系统分区
                                                    OS 185 G
                                                    ｜ LSM DB 120 G
                                                    ｜ ​Other 65 G
                                                元数据分区
                                                    Meta&ZK 100 G
                                                Journal 分区
                                                    10 G
                                        缓存盘
                                            缓存盘和数据盘独立部署
                                        NVMe SSD，SATA/SAS SSD
                                            缓存盘（默认）
                                            数据盘（可选）
                                        HDD
                                            数据盘（默认）
                                            缓存盘（可选）
                                        硬盘池最小盘数校验
                                            一块缓存盘
                                        实例推荐
                                            1 实例
                                                SSD  < 4 时
                                            2 实例
                                                SSD ≥  8
                                                SSD ≥  4
                                                    ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                多种类型 SSD
                                    ｜ 一般两种，比如 NVMe SSD + SATA SSD
                                        系统盘
                                            ｜ 2 块 SSD 和存储控制器构建硬 RAID 1
                                        缓存盘
                                            缓存盘和数据盘独立部署
                                        NVMe SSD
                                            缓存盘（默认）
                                            数据盘（可选）
                                        SATA/SAS SSD
                                            数据盘（默认）
                                            缓存盘（可选）
                                        硬盘池最小盘数校验
                                            一块缓存盘
                                        实例推荐 -  节点同时包含 NVMe SSD 和 SATA/SAS SSD，以 NVMe SSD 为准
                                            1 实例
                                                nvme SSD  < 4 时
                                                    NVME SSD  < 4，SATA/SAS SSD < 4
                                                    NVME SSD  < 4，SATA/SAS SSD > 4
                                            2 实例
                                                sata SSD ≥  8
                                                8
                                                    = nvme SSD ≥  4
                                                        ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                单一 SSD 包含不同的属性,允许用户修改物理盘用途（新增）
                                    考虑高 DWPD 和低 DWPD、QLC/TLC/PLC
                                        含元数据分区的缓存盘修改为含元数据分区的数据盘（默认按单一类型 SSD 方式部署）
                                            缓存和数据共享所有物理盘（1：9）
                                            系统盘
                                                含元数据分区的数据盘
                                            SSD
                                                数据盘
                                            硬盘池最小盘数校验
                                                1 块含元数据分区的数据盘或数据盘
                                        含元数据分区的数据盘修改为含元数据分区的缓存盘（按多种类型 SSD 方式部署）
                                            ｜ 分区方式：系统分区 + 元数据分区 + Journal 分区 10GiB + 缓存分区 + 未分区 10GiB。至少 2 块
                                                缓存盘和数据盘独立部署
                                                系统盘
                                                    含元数据分区的缓存盘（所有节点的系统盘用途需要保持一致）
                                                SSD
                                                    数据盘（默认）
                                                    缓存盘（可选）
                                                硬盘池最小盘数校验
                                                    1 块含元数据分区的缓存盘或缓存盘
                                        实例推荐
                                            1 实例
                                                SSD  < 4 时
                                            2 实例
                                                SSD ≥  8
                                                nvme SSD ≥  8
                                                SSD ≥  4
                                                    ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                            OS 安装在软 RAID 1
                                混闪配置
                                    ｜ 一般两种，比如 NVMe SSD + HDD
                                        启动盘
                                        含元数据分区的缓存盘
                                            ｜ 至少 2 块
                                                未分区 10 G
                                                缓存分区
                                                系统分区
                                                    1实例 - OS 185 G
                                                        ｜ LSM DB 120 G
                                                        ｜ ​Other 65 G
                                                    2实例 - OS 185 G
                                                        ｜ ​Other 65 G
                                                        ｜ LSM DB 120 G
                                                            每个实例 60 G
                                                元数据分区
                                                    Meta&ZK 100 G
                                                Journal 分区
                                                    10 G
                                        缓存盘
                                            缓存盘和数据盘独立部署
                                        NVMe SSD，SATA/SAS SSD
                                            缓存盘（默认）
                                            数据盘（可选）
                                        HDD
                                            数据盘（默认）
                                            缓存盘（可选）
                                        硬盘池最小盘数校验
                                            1 块含元数据分区的缓存盘或缓存盘
                                        实例推荐
                                            集群所有主机实例数不一致
                                            可由用户主动选择
                                            1 实例
                                                SSD  < 4 时
                                            2 实例
                                                SSD ≥  8
                                                nvme SSD ≥  8
                                                SSD ≥  4
                                                    ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                多种类型 SSD
                                    ｜ 一般两种，比如 NVME SSD + SATA SSD
                                        启动盘
                                        缓存盘和数据盘独立部署
                                        含元数据分区的缓存盘
                                            ｜ 至少 2 块
                                        NVMe SSD
                                            缓存盘（默认）
                                            数据盘（可选）
                                        SATA/SAS SSD
                                            数据盘（默认）
                                            缓存盘（可选）
                                        硬盘池最小盘数校验
                                            1 块含元数据分区的缓存盘或缓存盘
                                        实例推荐 -  节点同时包含 NVMe SSD 和 SATA/SAS SSD，以 NVMe SSD 为准
                                            1 实例
                                                nvme SSD  < 4 时
                                                    NVME SSD  < 4，SATA/SAS SSD < 4
                                                    NVME SSD  < 4，SATA/SAS SSD > 4
                                            2 实例
                                                sata SSD ≥  8
                                                nvme SSD ≥  8
                                                8
                                                    = nvme SSD ≥  4
                                                        ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                单一 SSD 包含不同的属性,允许用户修改物理盘用途（新增）
                                    ｜ 如高 DWPD 和低 DWPD、QLC/TLC/PLC
                                        含元数据分区的缓存盘修改为含元数据分区的数据盘（默认按单一类型 SSD 方式部署）
                                            缓存和数据共享所有物理盘（1：9）
                                            系统盘
                                                含元数据分区的数据盘
                                            SSD
                                                数据盘
                                            硬盘池最小盘数校验
                                                1 块含元数据分区的数据盘或数据盘
                                        含元数据分区的数据盘修改为含元数据分区的缓存盘（按多种类型 SSD 方式部署）
                                            ｜ 分区方式：系统分区 + 元数据分区 + Journal 分区 10GiB + 缓存分区 + 未分区 10GiB。至少 2 块
                                                缓存盘和数据盘独立部署
                                                系统盘
                                                    含元数据分区的缓存盘（所有节点的系统盘用途需要保持一致）
                                                SSD
                                                    数据盘（默认）
                                                    缓存盘（可选）
                                                硬盘池最小盘数校验
                                                    1 块含元数据分区的缓存盘或缓存盘
                                        实例推荐
                                            1 实例
                                                SSD  < 4 时
                                            2 实例
                                                SSD ≥  8
                                                nvme SSD ≥  8
                                                SSD ≥  4
                                                    ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                            说明
                                混闪配置或多种类型 SSD 全闪配置时，单节点限制
                                    数据盘的总容量不超过 128 TB
                                    缓存盘和系统盘总容量不超过 25 TB
                                    缓存盘、系统盘和数据盘总数量不超过 64
                                    缓存盘和系统盘的总容量与数据盘总容量之比应高于 10%
                                单一类型 SSD 全闪配置时，单节点限制
                                    数据盘和系统盘的总容量不超过 128 TB
                                    系统盘和数据盘总数量不超过 32
                        存储不分层模式
                            OS 安装在独立的硬 RAID 1
                                ｜ 启动盘和系统盘共用
                                    系统盘
                                        预留空间
                                        系统分区
                                            OS 185 G
                                            ｜ LSM DB 120 G
                                            ｜ ​Other 65 G
                                        元数据分区
                                            Meta&ZK 100 G
                                        Journal 分区
                                            10 G
                                    NVMe SSD，SATA/SAS SSD
                                        数据盘
                                    硬盘池最小盘数校验
                                        一块数据盘
                                    不支持开启多实例
                                        NVMe SSD ≥ 8  仍为单实例
                                    实例推荐
                                        1 实例
                                            SSD  < 4 时
                                        2 实例
                                            SSD ≥  8
                                            nvme SSD ≥  8
                                            SSD ≥  4
                                                ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                            OS 安装在软 RAID 1
                                启动盘
                                系统盘
                                    含元数据分区的数据盘
                                        ｜ 至少 2 块
                                            未分区 10 G
                                            缓存分区
                                            系统分区
                                                OS 185 G
                                                ｜ LSM DB 120 G
                                                ｜ ​Other 65 G
                                            元数据分区
                                                Meta&ZK 100 G
                                            Journal 分区
                                                10 G
                                NVMe SSD，SATA/SAS SSD
                                    数据盘
                                硬盘池最小盘数校验
                                    1 块含元数据分区的数据盘或数据盘
                                支持开启多实例
                                    1实例
                                    2实例
                                实例推荐
                                    1 实例
                                        SSD  < 4 时
                                    2 实例
                                        SSD ≥  8
                                        SSD ≥  4
                                            ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                            说明
                                数据盘和系统盘总容量不超过 128 TB
                                数据盘和系统盘总数量不可超过 32
                Large
                    Mem 256 GB
                    CPU
                        单 CPU 最小物理核心数 16 ，总逻辑核心 （HT 之后） >=64
                        CPU 内每个 NUMA Node 包含的物理核心数  >=8, 推荐 >=12
                        单 CPU 最小物理核心数 16 ，总逻辑核心 （HT 之后） =64
                        总逻辑核心 （HT 之后） < 64
                        单 CPU 最小物理核心数 15, 总逻辑核心 （HT 之后） >=64
                        单 CPU 最小物理核心数 >16, 总逻辑核心 （HT 之后） >=64
                        单 CPU 最小物理核心数 =16 , 总逻辑核心 （HT 之后） >=64
                    部署场景
                        存储分层模式
                            OS 安装在独立的硬 RAID 1
                                混闪配置
                                    ｜ 一般两种，比如 NVMe SSD 或 SATA/SAS SSD + HDD
                                        系统盘
                                            ｜ 2 块 960 GB 及以上的 SSD 和存储控制器构建硬 RAID 1
                                                journal 分区 10 G
                                                预留空间
                                                系统分区
                                                    ｜ 340 G
                                                        Other 100 G
                                                        LSM DB 240 G
                                                            1 个实例，每个实例 240 G
                                                            2 个实例，每个实例 120 G
                                                            4 个实例，，每个实例 60 G
                                                元数据分区
                                                    Meta&ZK 300 G
                                        缓存盘
                                            缓存盘和数据盘独立部署
                                        NVMe SSD，SATA/SAS SSD
                                            缓存盘（默认）
                                            数据盘（可选）
                                        HDD
                                            数据盘（默认）
                                            缓存盘（可选）
                                        硬盘池最小盘数校验
                                            一块缓存盘
                                        实例推荐
                                            4 实例 - 可以选择但不会推荐
                                            1 实例
                                                SSD  < 4 时
                                            2 实例
                                                NVMe SSD ≥  8
                                                SATA/SAS SSD ≥ 4
                                                SATA/SAS SSD ≥ 8
                                                nvme SSD ≥  8
                                                NVMe SSD ≥  4
                                                    ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                        磁盘推荐
                                            允许用户修改物理盘所属的硬盘池
                                            用途为“不挂载”的硬盘将不属于任何硬盘池
                                            独立部署的系统盘不属于任何硬盘池
                                            含元数据分区的盘必须属于一个硬盘池，即不允许选择不挂载
                                            若用户修改了硬盘池数量，需按照新的硬盘池数量重新调整硬盘所属的硬盘池
                                            缓存盘/数据盘数量均衡
                                                缓存盘/数据盘容量均衡
                                                    NVMe 盘放入相同 NUMA Node 的硬盘池
                                                        用途为“含元数据分区的盘”优先放置在第一个硬盘池内
                                                            ID 最小的硬盘池
                                                                ｜ NUMA 不一定有条件测到
                                                                    4 个 SSD + 9 个 HDD 的分层模式开启 2 实例，每个实例持有的 SSD 数量为 [2, 2] ，HDD 数量为 [5, 4]
                                            强制策略
                                                需满足硬盘池对最小盘数的要求
                                多种类型 SSD
                                    ｜ 一般两种，比如 NVMe SSD + SATA SSD
                                        系统盘
                                            ｜ 2 块 960 GB 及以上的 SSD 和存储控制器构建硬 RAID 1
                                        缓存盘
                                            缓存盘和数据盘独立部署
                                        NVMe SSD
                                            缓存盘（默认）
                                            数据盘（可选）
                                        SATA/SAS SSD
                                            数据盘（默认）
                                            缓存盘（可选）
                                        硬盘池最小盘数校验
                                            一块缓存盘
                                            一块数据盘
                                        实例推荐
                                            ｜ 节点同时包含 NVMe SSD 和 SATA/SAS SSD，以 NVMe SSD 为准
                                                4 实例 - 可以选择但不会推荐
                                                1 实例
                                                    NVME SSD  < 4 时
                                                        NVME SSD  < 4，SATA SSD < 4
                                                        NVME SSD  < 4，SATA SSD > 4
                                                2 实例
                                                    nvme SSD ≥  8
                                                    NVMe SSD ≥  4
                                                        ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                按单一 SSD
                                    实例推荐
                                        4 实例 - 可以选择但不会推荐
                                        1 实例
                                            SSD  < 4 时
                                        2 实例
                                            SSD ≥  8
                                            nvme SSD ≥  8
                                            SSD ≥  4
                                                ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                    含元数据分区的缓存盘修改为含元数据分区的数据盘（默认按单一类型 SSD 方式部署）
                                        缓存和数据共享所有物理盘（1：9）
                                        系统盘
                                            SMTX 系统盘
                                        SSD
                                            数据盘
                                        硬盘池最小盘数校验
                                            1 块含元数据分区的数据盘或数据盘
                                    含元数据分区的数据盘修改为含元数据分区的缓存盘（按多种类型 SSD 方式部署）
                                        ｜ 分区方式：系统分区 + 元数据分区 + Journal 分区 10GiB + 缓存分区 + 未分区 10GiB。至少 2 块
                                            缓存盘和数据盘独立
                                            系统盘
                                                SMTX 系统盘
                                            SSD
                                                数据盘（默认）
                                                缓存盘（可选）
                                            硬盘池最小盘数校验
                                                1 块含元数据分区的缓存盘或缓存盘
                            OS 安装在软 RAID 1
                                混闪配置
                                    启动盘
                                    系统盘
                                        含元数据分区的缓存盘
                                            ｜ 2 块 1.6 TB 的数据中心级 SSD
                                                系统分区
                                                journal 分区
                                                未分区 10 G
                                                缓存分区
                                                ｜ 340 G
                                                    Other 100 G
                                                    LSM DB 240 G
                                                        1 个实例，每个实例 240 G
                                                        2 个实例，每个实例 120 G
                                                        4实例
                                                元数据分区
                                                    Meta&ZK 300 G
                                    缓存盘
                                        每个实例最好两块缓存盘
                                        缓存盘和数据盘独立部署
                                    NVMe SSD，SATA/SAS SSD
                                        缓存盘（默认）
                                        数据盘（可选）
                                    HDD
                                        数据盘（默认）
                                        缓存盘（可选）
                                    硬盘池最小盘数校验
                                        1 块含元数据分区的缓存盘或缓存盘
                                    实例推荐
                                        4 实例 - 可以选择但不会推荐
                                        可由用户主动选择
                                        1 实例
                                            SSD  < 4 时
                                        2 实例
                                            4 ≤ NVMe SSD < 8
                                            4 ≤ SATA/SAS SSD < 8
                                            SATA/SAS SSD ≥ 8
                                            nvme SSD ≥  8
                                    磁盘推荐
                                        缓存盘/数据盘数量均衡
                                            缓存盘/数据盘容量均衡
                                                NVMe 盘放入相同 NUMA Node 的硬盘池
                                                    用途为“含元数据分区的盘”优先放置在第一个硬盘池内
                                                        ID 最小的硬盘池
                                                            4 个 SSD + 9 个 HDD 的分层模式开启 2 实例，每个实例持有的 SSD 数量为 [2, 2] ，HDD 数量为 [5, 4]
                                多种类型 SSD 全闪配置
                                    磁盘推荐
                                    系统盘
                                        含元数据分区的缓存盘
                                    缓存盘
                                        每个实例最好两块缓存盘
                                        缓存盘和数据盘独立部署
                                    NVMe SSD
                                        缓存盘（默认）
                                        数据盘（可选）
                                    SATA/SAS SSD
                                        数据盘（默认）
                                        缓存盘（可选）
                                    硬盘池最小盘数校验
                                        1 块含元数据分区的缓存盘或缓存盘
                                    实例推荐
                                        ｜ 节点同时包含 NVMe SSD 和 SATA/SAS SSD，以 NVMe SSD 为准
                                            4 实例 - 可以选择但不会推荐
                                            1 实例
                                                NVME SSD  < 4 时
                                                    NVME SSD  < 4，SATA/SAS SSD < 4
                                                    NVME SSD  < 4，SATA/SAS SSD > 4
                                            2 实例
                                                4 ≤ NVMe SSD < 8
                                                NVMe SSD ≥  8
                                单一 SSD(｜ 考虑高 DWPD 和低 DWPD、QLC/TLC/PLC)
                                    含元数据分区的缓存盘修改为含元数据分区的数据盘（默认按单一类型 SSD 方式部署）
                                        缓存和数据共享所有物理盘（1：9）
                                        系统盘
                                            含元数据分区的数据盘
                                        SSD
                                            数据盘
                                        硬盘池最小盘数校验
                                            1 块含元数据分区的数据盘或数据盘
                                    含元数据分区的数据盘修改为含元数据分区的缓存盘（按多种类型 SSD 方式部署）
                                        ｜ 分区方式：系统分区 + 元数据分区 + Journal 分区 10GiB + 缓存分区 + 未分区 10GiB。至少 2 块
                                            缓存盘和数据盘独立
                                            系统盘
                                                含元数据分区的缓存盘（所有节点的系统盘用途需要保持一致）
                                            SSD
                                                数据盘（默认）
                                                缓存盘（可选）
                                            硬盘池最小盘数校验
                                                1 块含元数据分区的缓存盘或缓存盘
                                    实例推荐
                                        4 实例 - 可以选择但不会推荐
                                        1 实例
                                            SSD  < 4 时
                                        2 实例
                                            SATA/SAS SSD ≥  4
                                            NVME SSD ≥  8
                            说明
                                闪配置或多种类型 SSD 全闪配置时，单节点限制
                                    数据盘的总容量不超过 256 TB
                                    缓存盘和系统盘总容量不超过 50 TB
                                    缓存盘、系统盘和数据盘总数量不超过 64
                                    缓存盘和系统盘的总容量与数据盘总容量之比应高于 10%
                                单一类型 SSD 全闪配置时，单节点限制
                                    数据盘和系统盘的总容量不超过 256 TB
                                    系统盘和数据盘总数量不超过 32
                        存储不分层模式
                            OS 安装在独立的硬 RAID 1
                                系统盘
                                NVMe SSD，SATA/SAS SSD
                                    数据盘
                                硬盘池最小盘数校验
                                    一块数据盘
                                实例推荐
                                    4 实例 - 可以选择但不会推荐
                                    1 实例
                                        SSD  < 4 时
                                    2 实例
                                        SATA/SAS SSD ≥  4
                                        NVME SSD ≥  8
                            OS 安装在软 RAID 1
                                启动盘
                                系统盘
                                    含元数据分区的数据盘
                                NVMe SSD，SATA/SAS SSD
                                    数据盘
                                硬盘池最小盘数校验
                                    1 块含元数据分区的数据盘或数据盘
                                实例推荐
                                    4 实例 - 可以选择但不会推荐
                                    1 实例
                                        SSD  < 4 时
                                    2 实例
                                        SATA/SAS SSD ≥  4
                                        NVME SSD ≥  8
                            说明
                                数据盘和系统盘总容量不超过 256 TB
                                数据盘和系统盘总数量不可超过 32
            添加主机
                Normal
                    CPU
                        单 CPU 最小物理核心数 12，总逻辑核心数量(HT 之后) ≥ 48
                            总逻辑核心数 < 48 - 不满足条件
                            总逻辑核心数 = 48
                            总逻辑核心数 > 48
                            单 CPU 最小物理核心数 < 12
                            单 CPU 最小物理核心数 = 12
                            单 CPU 最小物理核心数 > 12
                        CPU 内每个 NUMA Node 包含的物理核心数 ≤ 6，推荐 ≥ 8
                            6
                                不支持开启多实例模式
                            8
                                支持开启多实例模式
                    内存 128 G
                        < 256G  - 不满足条件
                        ≥ 256G
                    添加主机场景
                        存储分层模式
                            OS 安装在独立的硬 RAID 1
                                混闪配置
                                    ｜ 一般两种，比如 NVMe SSD + HDD
                                        系统盘
                                            ｜ 2 块 SSD 和存储控制器构建硬 RAID 1
                                                预留空间
                                                系统分区
                                                    OS 185 G
                                                    ｜ LSM DB 120 G
                                                    ｜ ​Other 65 G
                                                元数据分区
                                                    Meta&ZK 100 G
                                                Journal 分区
                                                    10 G
                                        缓存盘
                                            缓存盘和数据盘独立部署
                                        NVMe SSD，SATA/SAS SSD
                                            缓存盘（默认）
                                            数据盘（可选）
                                        HDD
                                            数据盘（默认）
                                            缓存盘（可选）
                                        硬盘池最小盘数校验
                                            一块缓存盘
                                        实例推荐
                                            集群所有主机实例数不一致
                                                1 实例
                                                    SSD  < 4 时
                                                2 实例
                                                    SSD ≥  8
                                                    SSD ≥  4
                                                        ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                            集群所有主机实例数一致
                                                1 实例
                                                    集群所有节点均为单实例 & 添加的主机ssd 磁盘数>4
                                                2 实例
                                                    集群所有节点均为2实例 & 4 <= 添加的主机ssd 磁盘数<=8
                                                    集群所有节点均为2实例 &  添加的主机ssd 磁盘数>=8
                                多种类型 SSD
                                    ｜ 一般两种，比如 NVMe SSD + SATA SSD
                                        系统盘
                                            ｜ 2 块 SSD 和存储控制器构建硬 RAID 1
                                        缓存盘
                                            缓存盘和数据盘独立部署
                                        NVMe SSD
                                            缓存盘（默认）
                                            数据盘（可选）
                                        SATA/SAS SSD
                                            数据盘（默认）
                                            缓存盘（可选）
                                        硬盘池最小盘数校验
                                            一块缓存盘
                                        实例推荐 -  节点同时包含 NVMe SSD 和 SATA/SAS SSD，以 NVMe SSD 为准
                                            集群所有主机实例数不一致
                                                1 实例
                                                    nvme SSD  < 4 时
                                                        NVME SSD  < 4，SATA/SAS SSD < 4
                                                        NVME SSD  < 4，SATA/SAS SSD > 4
                                                2 实例
                                                    sata SSD ≥  8
                                                    8
                                                        = nvme SSD ≥  4
                                                            ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                            集群所有主机实例数一致
                                                1 实例
                                                    集群所有节点均为单实例 & 添加的主机nvme  ssd 磁盘数>4
                                                2 实例
                                                    集群所有节点均为2实例 & 4 <= 添加的主机nvme  ssd 磁盘数<=8
                                                    集群所有节点均为2实例 &  添加的主机nvme ssd 磁盘数>=8
                                单一 SSD 包含不同的属性,允许用户修改物理盘用途（新增）
                                    考虑高 DWPD 和低 DWPD、QLC/TLC/PLC
                                        含元数据分区的缓存盘修改为含元数据分区的数据盘（默认按单一类型 SSD 方式部署）
                                            缓存和数据共享所有物理盘（1：9）
                                            系统盘
                                                SMTX 系统盘
                                            SSD
                                                数据盘
                                            硬盘池最小盘数校验
                                                1 块含元数据分区的数据盘或数据盘
                                        含元数据分区的数据盘修改为含元数据分区的缓存盘（按多种类型 SSD 方式部署）
                                            ｜ 分区方式：系统分区 + 元数据分区 + Journal 分区 10GiB + 缓存分区 + 未分区 10GiB。至少 2 块
                                                缓存盘和数据盘独立部署
                                                系统盘
                                                    SMTX 系统盘
                                                SSD
                                                    数据盘（默认）
                                                    缓存盘（可选）
                                                硬盘池最小盘数校验
                                                    1 块含元数据分区的缓存盘或缓存盘
                                        实例推荐
                                            集群所有主机实例数不一致
                                                1 实例
                                                    SSD  < 4 时
                                                2 实例
                                                    SSD ≥  8
                                                    nvme SSD ≥  8
                                                    SSD ≥  4
                                                        ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                            集群所有主机实例数一致
                                                1 实例
                                                    集群所有节点均为单实例 & 添加的主机ssd 磁盘数>4
                                                2 实例
                                                    集群所有节点均为2实例 & 4 <= 添加的主机ssd 磁盘数<=8
                                                    集群所有节点均为2实例 &  添加的主机ssd 磁盘数>=8
                            OS 安装在软 RAID 1
                                混闪配置
                                    ｜ 一般两种，比如 NVMe SSD + HDD
                                        启动盘
                                        含元数据分区的缓存盘
                                            ｜ 至少 2 块
                                                未分区 10 G
                                                缓存分区
                                                系统分区
                                                    1实例 - OS 185 G
                                                        ｜ LSM DB 120 G
                                                        ｜ ​Other 65 G
                                                    2实例 - OS 185 G
                                                        ｜ ​Other 65 G
                                                        ｜ LSM DB 120 G
                                                            每个实例 60 G
                                                元数据分区
                                                    Meta&ZK 100 G
                                                Journal 分区
                                                    10 G
                                        缓存盘
                                            缓存盘和数据盘独立部署
                                        NVMe SSD，SATA/SAS SSD
                                            缓存盘（默认）
                                            数据盘（可选）
                                        HDD
                                            数据盘（默认）
                                            缓存盘（可选）
                                        硬盘池最小盘数校验
                                            1 块含元数据分区的缓存盘或缓存盘
                                        实例推荐
                                            集群所有主机实例数不一致
                                                可由用户主动选择
                                                1 实例
                                                    SSD  < 4 时
                                                2 实例
                                                    SSD ≥  8
                                                    nvme SSD ≥  8
                                                    SSD ≥  4
                                                        ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                            集群所有主机实例数一致
                                                可由用户主动选择
                                                1 实例
                                                    集群所有节点均为单实例 & 添加的主机ssd 磁盘数>4
                                                2 实例
                                                    集群所有节点均为2实例 & 4 <= 添加的主机ssd 磁盘数<=8
                                                    集群所有节点均为2实例 &  添加的主机ssd 磁盘数>=8
                                多种类型 SSD
                                    ｜ 一般两种，比如 NVME SSD + SATA SSD
                                        启动盘
                                        缓存盘和数据盘独立部署
                                        含元数据分区的缓存盘
                                            ｜ 至少 2 块
                                        NVMe SSD
                                            缓存盘（默认）
                                            数据盘（可选）
                                        SATA/SAS SSD
                                            数据盘（默认）
                                            缓存盘（可选）
                                        硬盘池最小盘数校验
                                            1 块含元数据分区的缓存盘或缓存盘
                                        实例推荐 -  节点同时包含 NVMe SSD 和 SATA/SAS SSD，以 NVMe SSD 为准
                                            集群所有主机实例数不一致
                                                1 实例
                                                    nvme SSD  < 4 时
                                                        NVME SSD  < 4，SATA/SAS SSD < 4
                                                        NVME SSD  < 4，SATA/SAS SSD > 4
                                                2 实例
                                                    sata SSD ≥  8
                                                    nvme SSD ≥  8
                                                    8
                                                        = nvme SSD ≥  4
                                                            ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                            集群所有主机实例数一致
                                                1 实例
                                                    集群所有节点均为单实例 & 添加的主机nvme  ssd 磁盘数>4
                                                2 实例
                                                    集群所有节点均为2实例 & 4 <= 添加的主机nvme  ssd 磁盘数<=8
                                                    集群所有节点均为2实例 &  添加的主机nvme ssd 磁盘数>=8
                                单一 SSD 包含不同的属性,允许用户修改物理盘用途（新增）
                                    ｜ 如高 DWPD 和低 DWPD、QLC/TLC/PLC
                                        含元数据分区的缓存盘修改为含元数据分区的数据盘（默认按单一类型 SSD 方式部署）
                                            缓存和数据共享所有物理盘（1：9）
                                            系统盘
                                                含元数据分区的数据盘
                                            SSD
                                                数据盘
                                            硬盘池最小盘数校验
                                                1 块含元数据分区的数据盘或数据盘
                                        含元数据分区的数据盘修改为含元数据分区的缓存盘（按多种类型 SSD 方式部署）
                                            ｜ 分区方式：系统分区 + 元数据分区 + Journal 分区 10GiB + 缓存分区 + 未分区 10GiB。至少 2 块
                                                缓存盘和数据盘独立部署
                                                系统盘
                                                    含元数据分区的缓存盘（所有节点的系统盘用途需要保持一致）
                                                SSD
                                                    数据盘（默认）
                                                    缓存盘（可选）
                                                硬盘池最小盘数校验
                                                    1 块含元数据分区的缓存盘或缓存盘
                                        实例推荐
                                            集群所有主机实例数不一致
                                                1 实例
                                                    SSD  < 4 时
                                                2 实例
                                                    SSD ≥  8
                                                    nvme SSD ≥  8
                                                    SSD ≥  4
                                                        ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                            集群所有主机实例数一致
                                                1 实例
                                                    集群所有节点均为单实例 & 添加的主机ssd 磁盘数>4
                                                2 实例
                                                    集群所有节点均为2实例 & 4 <= 添加的主机ssd 磁盘数<=8
                                                    集群所有节点均为2实例 &  添加的主机ssd 磁盘数>=8
                            说明
                                混闪配置或多种类型 SSD 全闪配置时，单节点限制
                                    数据盘的总容量不超过 128 TB
                                    缓存盘和系统盘总容量不超过 25 TB
                                    缓存盘、系统盘和数据盘总数量不超过 64
                                    缓存盘和系统盘的总容量与数据盘总容量之比应高于 10%
                                单一类型 SSD 全闪配置时，单节点限制
                                    数据盘和系统盘的总容量不超过 128 TB
                                    系统盘和数据盘总数量不超过 32
                        存储不分层模式
                            OS 安装在独立的硬 RAID 1 - 启动盘和系统盘共用
                                系统盘
                                    预留空间
                                    系统分区
                                        OS 185 G
                                        ｜ LSM DB 120 G
                                        ｜ ​Other 65 G
                                    元数据分区
                                        Meta&ZK 100 G
                                    Journal 分区
                                        10 G
                                NVMe SSD，SATA/SAS SSD
                                    数据盘
                                硬盘池最小盘数校验
                                    一块数据盘
                                实例推荐
                                    集群所有主机实例数不一致
                                        1 实例
                                            SSD  < 4 时
                                        2 实例
                                            SSD ≥  8
                                            nvme SSD ≥  8
                                            SSD ≥  4
                                                ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                    集群所有主机实例数一致
                                        1 实例
                                            集群所有节点均为单实例 & 添加的主机ssd 磁盘数>4
                                        2 实例
                                            集群所有节点均为2实例 & 4 <= 添加的主机ssd 磁盘数<=8
                                            集群所有节点均为2实例 &  添加的主机ssd 磁盘数>=8
                            OS 安装在软 RAID 1
                                启动盘 - 不显示
                                系统盘
                                    含元数据分区的数据盘
                                        ｜ 至少 2 块
                                            未分区 10 G
                                            缓存分区
                                            系统分区
                                                OS 185 G
                                                ｜ LSM DB 120 G
                                                ｜ ​Other 65 G
                                            元数据分区
                                                Meta&ZK 100 G
                                            Journal 分区
                                                10 G
                                NVMe SSD，SATA/SAS SSD
                                    数据盘
                                硬盘池最小盘数校验
                                    1 块含元数据分区的数据盘或数据盘
                                实例推荐
                                    集群所有主机实例数不一致
                                        1 实例
                                            SSD  < 4 时
                                        2 实例
                                            SSD ≥  8
                                            SSD ≥  4
                                                ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                    集群所有主机实例数一致
                                        1 实例
                                            集群所有节点均为单实例 & 添加的主机ssd 磁盘数>4
                                        2 实例
                                            集群所有节点均为2实例 & 4 <= 添加的主机ssd 磁盘数<=8
                                            集群所有节点均为2实例 &  添加的主机ssd 磁盘数>=8
                            说明
                                数据盘和系统盘总容量不超过 128 TB
                                数据盘和系统盘总数量不可超过 32
                Large
                    CPU
                        单 CPU 最小物理核心数 16 ，总逻辑核心 （HT 之后） >=64
                        CPU 内每个 NUMA Node 包含的物理核心数  >=8, 推荐 >=12
                        CPU 内每个 NUMA Node 包含的物理核心数  = 6, 推荐 >=12   - 不允许开启多实例
                    添加主机场景
                        存储分层模式
                            OS 安装在独立的硬 RAID 1
                                混闪配置 - 一般两种，比如 NVMe SSD 或 SATA/SAS SSD + HDD
                                    系统盘
                                        ｜ 2 块 960 GB 及以上的 SSD 和存储控制器构建硬 RAID 1
                                            journal 分区 10 G
                                            预留空间
                                            系统分区-  340 G
                                                Other 100 G
                                                LSM DB 240 G
                                                    1 个实例，每个实例 240 G
                                                    2 个实例，每个实例 120 G
                                                    4 个实例，，每个实例 60 G
                                            元数据分区
                                                Meta&ZK 300 G
                                    缓存盘
                                        缓存盘和数据盘独立部署
                                    NVMe SSD，SATA/SAS SSD
                                        缓存盘（默认）
                                        数据盘（可选）
                                    HDD
                                        数据盘（默认）
                                        缓存盘（可选）
                                    硬盘池最小盘数校验
                                        一块缓存盘
                                    实例推荐
                                        集群所有主机实例数不一致
                                            4 实例 - 可以选择但不会推荐
                                            1 实例
                                                SSD  < 4 时
                                            2 实例
                                                SSD ≥  8
                                                nvme SSD ≥  8
                                                SSD ≥  4
                                                    ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                        集群所有主机实例数一致
                                            1 实例
                                                集群所有节点均为单实例 & 添加的主机ssd 磁盘数>4
                                            2 实例
                                                集群所有节点均为2实例 & 4 <= 添加的主机ssd 磁盘数<=8
                                                集群所有节点均为2实例 &  添加的主机ssd 磁盘数>=8
                                            4 实例
                                                集群所有节点均为4实例 & 添加的主机ssd 磁盘数>=8
                                    磁盘推荐
                                        允许用户修改物理盘所属的硬盘池
                                        用途为“不挂载”的硬盘将不属于任何硬盘池
                                        独立部署的系统盘不属于任何硬盘池
                                        含元数据分区的盘必须属于一个硬盘池，即不允许选择不挂载
                                        若用户修改了硬盘池数量，需按照新的硬盘池数量重新调整硬盘所属的硬盘池
                                        缓存盘/数据盘数量均衡
                                            缓存盘/数据盘容量均衡
                                                NVMe 盘放入相同 NUMA Node 的硬盘池
                                                    用途为“含元数据分区的盘”优先放置在第一个硬盘池内
                                                        ID 最小的硬盘池
                                                            ｜ NUMA 不一定有条件测到
                                                                4 个 SSD + 9 个 HDD 的分层模式开启 2 实例，每个实例持有的 SSD 数量为 [2, 2] ，HDD 数量为 [5, 4]
                                        强制策略
                                            需满足硬盘池对最小盘数的要求
                                多种类型 SSD -  一般两种，比如 NVMe SSD + SATA SSD
                                    系统盘
                                        ｜ 2 块 960 GB 及以上的 SSD 和存储控制器构建硬 RAID 1
                                    缓存盘
                                        缓存盘和数据盘独立部署
                                    NVMe SSD
                                        缓存盘（默认）
                                        数据盘（可选）
                                    SATA/SAS SSD
                                        数据盘（默认）
                                        缓存盘（可选）
                                    硬盘池最小盘数校验
                                        一块缓存盘
                                        一块数据盘
                                    实例推荐 -  节点同时包含 NVMe SSD 和 SATA/SAS SSD，以 NVMe SSD 为准
                                        集群所有主机实例数不一致
                                            4 实例 - 可以选择但不会推荐
                                            1 实例
                                                nvme SSD  < 4 时
                                            2 实例
                                                sata SSD ≥  8
                                                nvme SSD ≥  8
                                                8
                                                    = nvme SSD ≥  4
                                                        ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                        集群所有主机实例数一致
                                            1 实例
                                                集群所有节点均为单实例 & 添加的主机nvme  ssd 磁盘数>4
                                            2 实例
                                                集群所有节点均为2实例 & 4 <= 添加的主机nvme  ssd 磁盘数<=8
                                                集群所有节点均为2实例 &  添加的主机nvme ssd 磁盘数>=8
                                            4 实例
                                                集群所有节点均为4实例 & 添加的主机nvme ssd 磁盘数>=8
                                按单一 SSD
                                    实例推荐
                                        集群所有主机实例数不一致
                                            4 实例 - 可以选择但不会推荐
                                            1 实例
                                                SSD  < 4 时
                                            2 实例
                                                SSD ≥  8
                                                nvme SSD ≥  8
                                                SSD ≥  4
                                                    ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                        集群所有主机实例数一致
                                            1 实例
                                                集群所有节点均为单实例 & 添加的主机ssd 磁盘数>4
                                            2 实例
                                                集群所有节点均为2实例 & 4 <= 添加的主机ssd 磁盘数<=8
                                                集群所有节点均为2实例 &  添加的主机ssd 磁盘数>=8
                                            4 实例
                                                集群所有节点均为4实例 & 添加的主机ssd 磁盘数>=8
                                    含元数据分区的缓存盘修改为含元数据分区的数据盘（默认按单一类型 SSD 方式部署）
                                        缓存和数据共享所有物理盘（1：9）
                                        系统盘
                                            SMTX 系统盘
                                        SSD
                                            数据盘
                                        硬盘池最小盘数校验
                                            1 块含元数据分区的数据盘或数据盘
                                    含元数据分区的数据盘修改为含元数据分区的缓存盘（按多种类型 SSD 方式部署）
                                        ｜ 分区方式：系统分区 + 元数据分区 + Journal 分区 10GiB + 缓存分区 + 未分区 10GiB。至少 2 块
                                            缓存盘和数据盘独立
                                            系统盘
                                                SMTX 系统盘
                                            SSD
                                                数据盘（默认）
                                                缓存盘（可选）
                                            硬盘池最小盘数校验
                                                1 块含元数据分区的缓存盘或缓存盘
                            OS 安装在软 RAID 1
                                混闪配置
                                    启动盘 - 不显示
                                    磁盘推荐
                                    系统盘 - 含元数据分区的缓存盘 - 2 块 1.6 TB 的数据中心级 SSD
                                        journal 分区
                                        未分区 10 G
                                        缓存分区
                                        系统分区
                                            ｜ 340 G
                                                Other 100 G
                                                LSM DB 240 G
                                                    1 个实例，每个实例 240 G
                                                    2 个实例，每个实例 120 G
                                                    4 个实例，每个实例 60 G
                                        元数据分区
                                            Meta&ZK 300 G
                                    缓存盘
                                        每个实例最好两块缓存盘
                                        缓存盘和数据盘独立部署
                                    NVMe SSD，SATA/SAS SSD
                                        缓存盘（默认）
                                        数据盘（可选）
                                    HDD
                                        数据盘（默认）
                                        缓存盘（可选）
                                    硬盘池最小盘数校验
                                        1 块含元数据分区的缓存盘或缓存盘
                                    实例推荐
                                        集群所有主机实例数不一致
                                            4 实例 - 可以选择但不会推荐
                                            可由用户主动选择
                                            1 实例
                                                SSD  < 4 时
                                            2 实例
                                                SSD ≥  8
                                                nvme SSD ≥  8
                                                SSD ≥  4
                                                    ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                        集群所有主机实例数一致
                                            可由用户主动选择
                                            1 实例
                                                集群所有节点均为单实例 & 添加的主机ssd 磁盘数>4
                                            2 实例
                                                集群所有节点均为2实例 & 4 <= 添加的主机ssd 磁盘数<=8
                                                集群所有节点均为2实例 &  添加的主机ssd 磁盘数>=8
                                            4 实例
                                                集群所有节点均为4实例 & 添加的主机ssd 磁盘数>=8
                                多种类型 SSD 全闪配置
                                    系统盘
                                        含元数据分区的缓存盘
                                    缓存盘
                                        每个实例最好两块缓存盘
                                        缓存盘和数据盘独立部署
                                    NVMe SSD
                                        缓存盘（默认）
                                        数据盘（可选）
                                    SATA/SAS SSD
                                        数据盘（默认）
                                        缓存盘（可选）
                                    硬盘池最小盘数校验
                                        1 块含元数据分区的缓存盘或缓存盘
                                    实例推荐 -  节点同时包含 NVMe SSD 和 SATA/SAS SSD，以 NVMe SSD 为准
                                        集群所有主机实例数不一致
                                            4 实例 - 可以选择但不会推荐
                                            1 实例
                                                nvme SSD  < 4 时
                                                    NVME SSD  < 4，SATA/SAS SSD < 4
                                                    NVME SSD  < 4，SATA/SAS SSD > 4
                                            2 实例
                                                sata SSD ≥  8
                                                nvme SSD ≥  8
                                                8
                                                    = nvme SSD ≥  4
                                                        ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                        集群所有主机实例数一致
                                            1 实例
                                                集群所有节点均为单实例 & 添加的主机nvme  ssd 磁盘数>4
                                            2 实例
                                                集群所有节点均为2实例 & 4 <= 添加的主机nvme  ssd 磁盘数<=8
                                                集群所有节点均为2实例 &  添加的主机nvme ssd 磁盘数>=8
                                            4 实例
                                                集群所有节点均为4实例 & 添加的主机nvme ssd 磁盘数>=8
                                    磁盘推荐
                                        优先级
                                            数量均衡；
                                            容量均衡；
                                            NUMA 亲和；
                                            实例 ID
                                单一 SSD(｜ 考虑高 DWPD 和低 DWPD、QLC/TLC/PLC)
                                    含元数据分区的缓存盘修改为含元数据分区的数据盘（默认按单一类型 SSD 方式部署）
                                        缓存和数据共享所有物理盘（1：9）
                                        系统盘
                                            含元数据分区的数据盘
                                        SSD
                                            数据盘
                                        硬盘池最小盘数校验
                                            1 块含元数据分区的数据盘或数据盘
                                    含元数据分区的数据盘修改为含元数据分区的缓存盘（按多种类型 SSD 方式部署）
                                        ｜ 分区方式：系统分区 + 元数据分区 + Journal 分区 10GiB + 缓存分区 + 未分区 10GiB。至少 2 块
                                            缓存盘和数据盘独立
                                            系统盘
                                                含元数据分区的缓存盘（所有节点的系统盘用途需要保持一致）
                                            SSD
                                                数据盘（默认）
                                                缓存盘（可选）
                                            硬盘池最小盘数校验
                                                1 块含元数据分区的缓存盘或缓存盘
                                    实例推荐
                                        集群所有主机实例数不一致
                                            4 实例 - 可以选择但不会推荐
                                            1 实例
                                                SSD  < 4 时
                                            2 实例
                                                SSD ≥  8
                                                nvme SSD ≥  8
                                                SSD ≥  4
                                                    ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                        集群所有主机实例数一致
                                            1 实例
                                                集群所有节点均为单实例 & 添加的主机ssd 磁盘数>4
                                            2 实例
                                                集群所有节点均为2实例 & 4 <= 添加的主机ssd 磁盘数<=8
                                                集群所有节点均为2实例 &  添加的主机ssd 磁盘数>=8
                                            4 实例
                                                集群所有节点均为4实例 & 添加的主机ssd 磁盘数>=8
                            说明
                                闪配置或多种类型 SSD 全闪配置时，单节点限制
                                    数据盘的总容量不超过 256 TB
                                    缓存盘和系统盘总容量不超过 50 TB
                                    缓存盘、系统盘和数据盘总数量不超过 64
                                    缓存盘和系统盘的总容量与数据盘总容量之比应高于 10%
                                单一类型 SSD 全闪配置时，单节点限制
                                    数据盘和系统盘的总容量不超过 256 TB
                                    系统盘和数据盘总数量不超过 32
                        存储不分层模式
                            OS 安装在独立的硬 RAID 1
                                系统盘
                                NVMe SSD，SATA/SAS SSD
                                    数据盘
                                硬盘池最小盘数校验
                                    一块数据盘
                                实例推荐
                                    集群所有主机实例数不一致
                                        4 实例 - 可以选择但不会推荐
                                        1 实例
                                            SSD  < 4 时
                                        2 实例
                                            SSD ≥  8
                                            nvme SSD ≥  8
                                            SSD ≥  4
                                                ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                    集群所有主机实例数一致
                                        1 实例
                                            集群所有节点均为单实例 & 添加的主机ssd 磁盘数>4
                                        2 实例
                                            集群所有节点均为2实例 & 4 <= 添加的主机ssd 磁盘数<=8
                                            集群所有节点均为2实例 &  添加的主机ssd 磁盘数>=8
                                        4 实例
                                            集群所有节点均为4实例 & 添加的主机ssd 磁盘数>=8
                            OS 安装在软 RAID 1
                                启动盘
                                系统盘
                                    含元数据分区的数据盘
                                NVMe SSD，SATA/SAS SSD
                                    数据盘
                                硬盘池最小盘数校验
                                    1 块含元数据分区的数据盘或数据盘
                                实例推荐
                                    集群所有主机实例数不一致
                                        4 实例 - 可以选择但不会推荐
                                        1 实例
                                            SSD  < 4 时
                                        2 实例
                                            SSD ≥  8
                                            nvme SSD ≥  8
                                            SSD ≥  4
                                                ｜ 满足配置 2 硬盘池的前提条件，但不满足配置 4 硬盘池的要求
                                    集群所有主机实例数一致
                                        1 实例
                                            集群所有节点均为单实例 & 添加的主机ssd 磁盘数>4
                                        2 实例
                                            集群所有节点均为2实例 & 4 <= 添加的主机ssd 磁盘数<=8
                                            集群所有节点均为2实例 &  添加的主机ssd 磁盘数>=8
                                        4 实例
                                            集群所有节点均为4实例 & 添加的主机ssd 磁盘数>=8
                            说明
                                数据盘和系统盘总容量不超过 256 TB
                                数据盘和系统盘总数量不可超过 32
            RDMA 使用 ovs bonding，跨网卡bonding
                部署
                    RDMA + 同一网卡间 bond（cx4 / cx5 / cx6 任意选一即可）+ ovs ab，功能正常，流控正常
                    RDMA + 跨网卡 bond（4 网口，cx4 / cx5）+ ovs balance-tcp，功能正常
                    开启 RDMA，部署时不支持 balance-slb bond
                    部署时存储网启用 RDMA，选择关联网口时，可以选择不同网卡的网口
                    部署时存储网启用 RDMA，关联网口选择多个后，展示网口绑定模式，默认选择 active-backup，仅支持选择 active-backup 和 balance-tcp
                    rdma + active-backup 模式 - 选择相同网卡的两个网口 - 部署成功，bonding为ovs bond
                    rdma + active-backup 模式 - 选择不同cx4 网卡的两个网口 - 部署成功，bonding为ovs bond
                    rdma + active-backup 模式 - 选择不同型号的网卡（cx4+cx5）的两个网口 - 部署成功，bonding为ovs bond
                    rdma + balance-tcp 模式 - 选择相同网卡的两个网口 - 部署成功，bonding为ovs bond
                    rdma + balance-tcp 模式 - 选择不同cx4 网卡的两个网口 - 部署成功，bonding为ovs bond
                    rdma + balance-tcp 模式 - 选择不同型号的网卡（cx4+cx5）的两个网口 - 部署成功，bonding为ovs bond
                    active-backup 模式- 部署成功，bonding为ovs bond
                    balance-slb - 部署成功，bonding为ovs bond
                    balance-tcp 模式 - 部署成功，bonding为ovs bond
                    bonding 配置文件符合预期 - (/etc/zbs/chunk_storage_network_config)
                    vmware + rdma - 选择相同网卡的两个网口 - 部署成功，bonding为ovs bond
                    vmware + rdma - 选择不同网卡的两个网口 - 部署成功，bonding为ovs bond
                    vmware + rdma - 选择不同型号的不同网卡的两个网口 - 部署成功，bonding为ovs bond
                    vmware - 选择相同网卡的两个网口 - 部署成功，bonding为ovs bond
                    vmware - 选择不同网卡的两个网口 - 部署成功，bonding为ovs bond
                    vmware - 选择不同型号的不同网卡的两个网口 - 部署成功，bonding为ovs bond
                扩容
                    rdma + active-backup 模式 - 选择相同网卡的两个网口 - 添加成功，bonding为ovs bond
                    rdma + active-backup 模式 - 选择不同cx4 网卡的两个网口 - 添加成功，bonding为ovs bond
                    rdma + active-backup 模式 - 选择不同型号的网卡（cx4+cx5）的两个网口 - 添加成功，bonding为ovs bond
                    rdma + balance-tcp 模式 - 选择相同网卡的两个网口 - 添加成功，bonding为ovs bond
                    rdma + balance-tcp 模式 - 选择相同网卡的两个网口 - 添加成功，bonding为ovs bond
                    rdma + balance-tcp 模式 - 选择不同cx4 网卡的两个网口 - 添加成功，bonding为ovs bond
                    rdma + balance-tcp 模式 - 选择不同型号的网卡（cx4+cx5）的两个网口 - 添加成功，bonding为ovs bond
                    集群存储网启用了 RDMA 且为 ovs bond 时，添加主机选择关联网口时，支持选择不同网卡上的网口
                    集群存储网启用了 RDMA 且为 linux bond 时，添加主机选择关联网口时，禁止选择不同网卡上的网口
                    集群从低版本升级后为rdma + balance-slb（linux bond） - 扩容成功后保持linux bond
                        扩容成功
                        不允许跨网卡
                    集群从低版本升级后为rdma + active-backup （linux bond）- 扩容成功后保持linux bond
                        扩容成功
                        不允许跨网卡
            前端
                扫描集群
                    选中的 N 台主机的操作系统部署模式不同。建议同一集群内的主机使用相同的操作系统部署模式
                    ｜ 不会拦截部署
                    选择相同容量规格的主机
                    节点展示
                        展示容量规格
                            Normal
                            Large
                        展示系统盘
                            操作系统与缓存/数据共享物理盘
                            操作系统使用独立物理盘
                    ｜ 会拦截部署
                        容量规格必须相同
                            normal，larget
                配置存储
                    物理盘用途
                        删掉文案：所有主机的物理盘是同一类型SSD。分层模式下，副本卷将仅使用容量层,仅纠删码卷会使用缓存层。
                        新增文案：请根据主机的硬件配置，为每个主机配置物理盘池数量和每个池中的物理盘用途。为提升容错能力，建议每个池中至少包含2块SSD。每次修改物理盘池梳理后，需重新配置物理盘数量。
                            上述文案 [物理盘池数量]显示 tooltip
                            ｜ 物理盘池数量对主机配置的要求∶
                            ｜ 每个NUMA节点均含8个及以上的物理核心，才支持多个池。
                            ｜ 标准容量规格仅支持2个池;大容量规格最多支持4个池
                            ｜ CPU 和内存满足池对计算资源的要求。
                            ｜ ​物理盘数满足池对最小盘数的要求。
                            ｜
                    样式更新
                        主机间增加分割线
                    物理盘池
                        SMTX 系统盘，不属于任何池，固定展示在第一个池上方
                        池数
                            新增选择磁盘池数量入口
                            仅支持一个池时，不可选
                        按池分组
                            将盘分组展示在各池内：池标识展示格式为「池%chunk-id%」(「池」字固定展示)
                            如池内没有盘，则“池内”展示如图空状态 (submit后，header变红、报错)
                        不挂载
                            不挂载的盘(即“未加入池的盘”)单独成组，用途取值为空
                            如果没有“不挂载的盘”，则不展示该分组
                        新增按键
                            多个池时，提供“移动 btn”;只有1个池时，提供“移除btn”，不挂载区域，提供“加入池 btn”
                            hover btn 显示 tooltip;点击打开 menu，menu内选项（下图以4个池为例)
                                某个池的元数据盘，选项为其他池
                                某个池的非元数据盘，选项为其他池 + 不挂载
                                不挂载，选项为全部池
                                只有 1 个池，从池中移出（即不挂载）
                        用途更改
                            不可更改用途
                                系统盘独立部署的系统盘
                                不分层的数据盘
                            可更改用途
                                分层的缓存盘改为数据盘
                                缓存盘和含元数据分区的缓存盘
                        错误验证
                            物理盘池数量
                            仅【缓存盘和数据盘独立部署】每个池至少包含 1 个缓存盘
                            ｜ 错误文案：池内应至少包含一个缓存盘
                            ｜ 集群内池的总数量
                                错误文案：集群最多可配置 255 个物理盘
                            缓存盘和数据盘独立部署
                                每个池应至少包含一个数据盘（或含元数据分区的数据盘）
                                ｜ 错误文案：池内应至少包含一个数据盘
                            缓存盘和数据盘共享
                                每个池应至少包含一个数据盘（或含元数据分区的数据盘）
                                ｜ 错误文案：池内应至少包含一个数据盘
                    分层 + 单一类型 SSD
                        新增 tip: 所有主机的物理盘均为%NVMe 或 SATA/SAS% SSD，默认将所有盘的部分容量作为缓存使用。若主机上的盘具备不同属性，建议：每个物理盘池中包含不同属性的盘﹔使用高速盘作为缓存使用，低速盘作为数据盘使用。
                        系统盘用途
                            展示条件
                                字段展示条件∶分层＋所有主机的所有盘是单一类型SSD＋存在主机是“操作系统与缓存/数据共享物理盘”模式
                                    全部节点为“操作系统与缓存/数据共享物理盘"
                                    部分节点为 “操作系统与缓存/数据共享物理盘"
                                    全部节点为单一类型 SSD
                                    部分节点为 NVME + SATA SSD - 不展示
                            默认选择
                                默认选择「含元数据分区的数据盘」，其他盘必须为数据盘（包含缓存分区，1：9）
                                可选「含元数据分区的缓存盘」，其他盘可指定为缓存盘或数据盘（包含缓存分区，1：9）
                            tip 信息
                                适用于“操作系统与缓存/数据共享物理盘"模式的主机,各主机的系统盘用途需一致。
                        盘用途
                            “操作系统与缓存盘/数据盘共享部署”的主机
                                系统盘用途为「含元数据分区的数据盘」时，非系统盘固定为「数据盘」(不可编辑)
                                系统盘用途为「含元数据分区的缓存盘」时，非系统盘可选择「数据盘」或「缓存盘」、默认为「数据盘」
                            “操作系统独立部署”的主机
                                非系统盘可选择「数据盘」或「缓存盘」、默认为「数据盘」
                检查配置 -
                    物理盘
                        新增所属磁盘池
                        不挂载的盘，所属物理盘池为[不挂载]，用途为 [不挂载]
                        SMTX 系统盘，所属物理盘池取值为空，用途为 SMTX 系统盘
            应用场景
                全闪集群添加主机
                    全 ssd集群 添加主机全nvme
                    全nvme集群 添加主机全ssd
                    全ssd 缓存盘和数据盘独立部署 - 添加主机缓存盘和数据盘独立
                    全ssd 缓存盘和数据盘独立部署 - 添加主机 缓存和数据共享所有物理盘
                    全ssd  缓存和数据共享所有物理盘- 添加主机缓存盘和数据盘独立
                    全ssd  缓存和数据共享所有物理盘- 添加主机 缓存和数据共享所有物理盘
                    分层集群，添加节点全数据盘
                    分层集群 ， 添加节点全缓存盘
                全闪部署
                    全ssd节点与全nvme节点同时存在
                chunk多实例
                    同一个集群 - 不同节点不同实例数
                    smtxelf - 不支持
                    smtxos os vmware - 不支持
                    /etc/sysconfig/zbs-chunkd
                    规格
                        normal（48 cpu + 256 memory ）
                            最大实例数 2
                                1
                                2
                        large（64 cpu + 256 memory ）
                            最大实例数 4
                                1
                                2
                                4
                    推荐模式（根据ssd数量）
                        [1, 4) 时 1 实例；
                        [4, ∞) 时 2 实例
                    集群特性
                        双活 - 开启多实例
                            部署
                            扩容
                        支持 RDMA - 开启多实例
                            部署
                            扩容
                        开启vhost - 开启多实例
                            部署
                            扩容
                            集群中存在开启多实例的主机，不允许执行 zbs-cluster vhost disable
                        不开启vhost - 不支持使用多实例
                            部署
                            扩容
                        网络融合 - 开启多实例
                            部署
                            扩容
        6.2U1 SMTX 产品版本规范
            tower 472
                tower
                    ZBS 集群关联 ELF集群
                    tower 关联集群页面
                        SMTX ELF 6.2 U1
                        SMTX OS（ELF）双活 6.2 U1
                        vmware 单活 6.2 U1
                    集群列表
                        总的集群列表
                        数据中心层级的集群列表
                        「集群版本」字段
                            “6.2 U1” 显示正确
                            集群版本大小排序正确
                        筛选
                            筛选条件“集群版本包含 6.2 U1” 时可以正确筛选出对应版本的集群
                            筛选条件“集群版本不包含 6.2 U1” 时可以正确过滤对应版本的集群
                        导出
                            SMTX ELF 6.2 U1 版本号显示正确
                            SMTX OS（ELF） 6.2 U1 版本号显示正确
                    集群概览页
                        “集群”card 版本显示正确
                            SMTX ELF 6.2 U1
                            SMTX OS（ELF）单活 6.2 U1
                            SMTX OS（ELF）双活 6.2 U1
                            vmware 单活 6.2 U1
                    集群设置页
                        「块存储」模块
                            可以将 SMTXOS（ELF）集群的分布式块存储服务通过 iSCSI 协议提供给 SMTX ELF 6.2 U1 集群使用
                        许可
                            SMTX ELF 6.2 U1 更新许可成功
                            vmware 单活 6.2 U1 更新许可成功
                            商务系统对应更改
                    虚拟机
                        虚拟机转换为虚拟机模版
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        虚拟机克隆为虚拟机模板
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        创建空白虚拟机
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        导入虚拟机
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                    虚拟机模板
                        从模板创建虚拟机
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        计算集群上的虚拟机模板转换为虚拟机
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        导入虚拟机模板
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                    虚拟卷
                        创建虚拟卷
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        导入虚拟卷
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                    虚拟机迁移
                        跨集群迁移时，能成功过滤出 6.2U1 集群
                        版本号显示正确
                    报警
                        内置报警规则
                            编辑
                                报警对象可以成功过滤出 6.2 U1 集群
                        自定义报警规则
                            创建
                                集群粒度：可以成功过滤出 6.2 U1 集群，并创建成功
                                虚拟机组粒度：可以成功过滤出 6.2 U1 集群下的虚拟机组，并创建成功
                                虚拟机粒度：可以成功过滤出 6.2 U1 集群下的虚拟机，并创建成功
                            编辑
                                集群粒度：可以新增或减少 6.2U1 集群，并编辑成功
                                虚拟机组粒度：可以新增或减少 6.2U1 集群下的虚拟机组，并编辑成功
                                虚拟机粒度：可以新增或减少 6.2U1 集群下的虚拟机，并编辑成功
                        通知配置
                            邮件
                                集群内部
                                    可以为 6.2U1 集群创建新的邮件通知配置
                                    编辑已有的邮件通知配置，可以新增或减少 6.2U1 集群
                                可观测性
                                    可以为 6.2U1 集群创建新的邮件通知配置
                                    编辑已有的邮件通知配置，可以新增或减少 6.2U1 集群
                            SNMP trap
                                集群内部
                                    可以为 6.2U1 集群创建新的 SNMP trap
                                    编辑已有的 SNMP trap，可以新增或减少 6.2U1 集群
                                可观测性
                                    可以为 6.2U1 集群创建新的 SNMP trap
                                    编辑已有的 SNMP trap，可以新增或减少 6.2U1 集群
                            webhook
                                可以为 6.2U1 集群创建新的 webhook
                                编辑已有的 webhook，可以新增或减少 6.2U1 集群
                        通知策略
                            静默策略
                                可以为 6.2U1 集群创建新的静默策略
                                编辑已有的静默策略，可以新增或减少 6.2U1 集群
                            聚合策略
                                可以为 6.2U1 集群创建新的静默策略
                                编辑已有的静默策略，可以新增或减少 6.2U1 集群
                    快照计划
                        可以为 6.2U1 集群创建新的快照计划
                        已有的快照计划不允许编辑所属集群？
                    资源优化
                        预置规则
                            编辑已有规则的应用对象，正确显示 6.2U1 集群版本号，且可以新增或减少该版本的集群
                        自定义规则
                            创建新的自定义规则时应用对象列表，正确显示了 6.2U1 版本号，且可以为该集群创建规则
                            编辑已有规则的应用对象，正确显示 6.2U1 集群版本号，且可以新增或减少该版本的集群
                        动态资源调度-- 未启用集群列表
                            「集群版本」字段正确显示了 6.2U1
                    回收站
                        创建新的特例规则时应用对象列表，正确显示了 6.2U1 版本号，且可以为该集群创建特例规则
                        可以成功编辑 6.2U1 集群的特例规则
                    报表
                        报表模板-资产列表，生成的文件中，集群版本正确显示为 6.2U1
                        自动生成的报表-资产列表，生成的文件中，集群版本正确显示为 6.2U1
                    系统配置
                        syslog 服务器--用于日志传输
                            创建时应用对象列表，正确显示了 6.2U1 版本号，且可以为该集群配置 syslog 服务器
                            编辑已有配置时，正确显示了 6.2U1 版本号，可以新增或减少该版本的集群
                        SNMP 传输
                            创建时应用对象列表，正确显示了 6.2U1 版本号，且可以为该集群配置 SNMP 传输
                            编辑已有配置时，正确显示了 6.2U1 版本号，可以新增或减少该版本的集群
                        虚拟机工具
                            上传时目标集群，正确显示了 6.2U1 版本号，可以将虚拟机工具上传到 6.2U1 版本的集群上
                OS
                    新部署
                        新部署后集群版本号显示正确
                    升级
                        6.2.0 升级到 6.2 U1后，版本号显示正确
                    配置文件
                        tuna-release.yaml 文件中版本号显示正确
                    hotfix
                        构造一下 6.2U1 p1  看一下带 hotfix 的集群版本号在 tower 各处的显示
                        目前看就集群概览页、升级中心、巡检中心做了适配，其他大部分地方都不带 p1 ，所以目前 6.2 U1 p1 还是保持这种状态嘛-----huimin
                    filan build
                        没有 build 号时展示正确
                相关产品
                    网络流量可视化
                    内容库
                        编辑虚拟机模板所属集群
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        虚拟机模板批量分发
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        ISO 上传
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        编辑 ISO 映像所属集群
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        ISO 批量分发
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                    高级监控
                        新部署：6.2U1 vmware 集群可以成功部署高级监控
                        600 版本集群部署高级监控后，可以成功升级到 6.2U1
                        该页面中，集群列表的「集群版本」字段正确显示为 6.2U1
                        对应出 6.2U1 的高级监控版本嘛？-- 6.2.1
                    升级中心
                        随升级中心 1.2.2 进行测试
                    巡检中心
                        随巡检中心 1.2.2 进行测试
                    可观测
                        编辑 OBS 服务关联集群时，集群 list 中正确显示了 6.2U1 版本号
                        关联 tower 系统服务时，版本号显示为 4.8p1、4.7 p2
                    cluster installer
                        集群适配
                        tower 适配
                    ER
                        编辑系统服务关联集群
                        ER controller 扩容
                        ER 服务替换节点
                        部署 ER 服务（6.2 U1 符合目标集群版本要求时能成功过滤出来，且版本号显示正确）
                            选择 controller 所属集群
                            选择 LB 实例所属集群
                        相关功能的开启/关闭时的集群版本限制
                            vpc 关联集群
                            创建边缘网关
                            网络负责均衡器 创建 LB 实例
                            网络导流关联集群？不支持 6.2U1 版本集群？
                    备份复制
                        部署
                        关联
                        相关功能的开启/关闭时的集群版本限制
                    SFS
                        相关功能的开启/关闭时的集群版本限制
                        是否拿 tower 版本号：4.8 p1、4.7 p2
                        部署时
                            6.2 U1 符合目标集群版本要求时能成功过滤出来，且版本号显示正确
                        编辑系统服务关联集群时
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                            可以成功关联/取消关联
                    容器镜像仓库
                        部署
                            目标集群：SMTX OS（ELF）双活 6.2 U1，能成功过滤出该集群，且版本号显示正确
                            目标集群：SMTX OS（ELF）单活 6.2 U1，能成功过滤出该集群，且版本号显示正确
                    cloudtower 代理
                        部署时可以成功过滤出 6.2U1 版本集群
                    SKS
                        确认 sks 在 tower 480 里不适配 OS 集群版本改造
            tower 481
                tower
                    ZBS 集群关联 ELF集群
                    tower 关联集群页面
                        SMTX ELF 6.2 U1
                        SMTX OS（ELF）双活 6.2 U1
                        vmware 单活 6.2 U1
                    集群列表
                        总的集群列表
                        数据中心层级的集群列表
                        「集群版本」字段
                            “6.2 U1” 显示正确
                            集群版本大小排序正确
                        筛选
                            筛选条件“集群版本包含 6.2 U1” 时可以正确筛选出对应版本的集群
                            筛选条件“集群版本不包含 6.2 U1” 时可以正确过滤对应版本的集群
                        导出
                            SMTX ELF 6.2 U1 版本号显示正确
                            SMTX OS（ELF） 6.2 U1 版本号显示正确
                    集群概览页
                        “集群”card 版本显示正确
                            SMTX ELF 6.2 U1
                            SMTX OS（ELF）单活 6.2 U1
                            SMTX OS（ELF）双活 6.2 U1
                            vmware 单活 6.2 U1
                    集群设置页
                        「块存储」模块
                            可以将 SMTXOS（ELF）集群的分布式块存储服务通过 iSCSI 协议提供给 SMTX ELF 6.2 U1 集群使用
                        许可
                            SMTX ELF 6.2 U1 更新许可成功
                            vmware 单活 6.2 U1 更新许可成功
                            商务系统对应更改
                    虚拟机
                        虚拟机转换为虚拟机模版
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        虚拟机克隆为虚拟机模板
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        创建空白虚拟机
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        导入虚拟机
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                    虚拟机模板
                        从模板创建虚拟机
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        计算集群上的虚拟机模板转换为虚拟机
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        导入虚拟机模板
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                    虚拟卷
                        创建虚拟卷
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        导入虚拟卷
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                    虚拟机迁移
                        跨集群迁移时，能成功过滤出 6.2U1 集群
                        版本号显示正确
                    报警
                        内置报警规则
                            编辑
                                报警对象可以成功过滤出 6.2 U1 集群
                        自定义报警规则
                            创建
                                集群粒度：可以成功过滤出 6.2 U1 集群，并创建成功
                                虚拟机组粒度：可以成功过滤出 6.2 U1 集群下的虚拟机组，并创建成功
                                虚拟机粒度：可以成功过滤出 6.2 U1 集群下的虚拟机，并创建成功
                            编辑
                                集群粒度：可以新增或减少 6.2U1 集群，并编辑成功
                                虚拟机组粒度：可以新增或减少 6.2U1 集群下的虚拟机组，并编辑成功
                                虚拟机粒度：可以新增或减少 6.2U1 集群下的虚拟机，并编辑成功
                        通知配置
                            邮件
                                集群内部
                                    可以为 6.2U1 集群创建新的邮件通知配置
                                    编辑已有的邮件通知配置，可以新增或减少 6.2U1 集群
                                可观测性
                                    可以为 6.2U1 集群创建新的邮件通知配置
                                    编辑已有的邮件通知配置，可以新增或减少 6.2U1 集群
                                    为系统服务-tower 创建新的邮件通知配置，tower 版本号显示为 4.8 P1
                            SNMP trap
                                集群内部
                                    可以为 6.2U1 集群创建新的 SNMP trap
                                    编辑已有的 SNMP trap，可以新增或减少 6.2U1 集群
                                可观测性
                                    可以为 6.2U1 集群创建新的 SNMP trap
                                    编辑已有的 SNMP trap，可以新增或减少 6.2U1 集群
                                    为系统服务-tower 创建新的 SNMP trap，tower 版本号显示为 4.8 P1
                            webhook
                                可以为 6.2U1 集群创建新的 webhook
                                编辑已有的 webhook，可以新增或减少 6.2U1 集群
                                为系统服务-tower 创建新的 webhook，tower 版本号显示为 4.8 P1
                        通知策略
                            静默策略
                                可以为 6.2U1 集群创建新的静默策略
                                编辑已有的静默策略，可以新增或减少 6.2U1 集群
                                为系统服务-tower 创建新的 静默策略时，tower 版本号显示为 4.8 P1
                            聚合策略
                                可以为 6.2U1 集群创建新的静默策略
                                编辑已有的静默策略，可以新增或减少 6.2U1 集群
                                为系统服务-tower 创建新的 聚合策略时，不显示 tower 版本号
                    快照计划
                        可以为 6.2U1 集群创建新的快照计划
                        已有的快照计划不允许编辑所属集群
                    资源优化
                        预置规则
                            编辑已有规则的应用对象，正确显示 6.2U1 集群版本号，且可以新增或减少该版本的集群
                        自定义规则
                            创建新的自定义规则时应用对象列表，正确显示了 6.2U1 版本号，且可以为该集群创建规则
                            编辑已有规则的应用对象，正确显示 6.2U1 集群版本号，且可以新增或减少该版本的集群
                        动态资源调度-- 未启用集群列表
                            「集群版本」字段正确显示了 6.2U1
                    回收站
                        创建新的特例规则时应用对象列表，正确显示了 6.2U1 版本号，且可以为该集群创建特例规则
                        可以成功编辑 6.2U1 集群的特例规则
                    报表
                        报表模板-资产列表，生成的文件中，集群版本正确显示为 6.2U1
                        自动生成的报表-资产列表，生成的文件中，集群版本正确显示为 6.2U1
                    系统配置
                        syslog 服务器--用于日志传输
                            创建时应用对象列表，正确显示了 6.2U1 版本号，且可以为该集群配置 syslog 服务器
                            编辑已有配置时，正确显示了 6.2U1 版本号，可以新增或减少该版本的集群
                        SNMP 传输
                            创建时应用对象列表，正确显示了 6.2U1 版本号，且可以为该集群配置 SNMP 传输
                            编辑已有配置时，正确显示了 6.2U1 版本号，可以新增或减少该版本的集群
                        虚拟机工具
                            上传时目标集群，正确显示了 6.2U1 版本号，可以将虚拟机工具上传到 6.2U1 版本的集群上-- 不显示集群版本号
                OS
                    新部署
                        新部署后集群版本号显示正确
                    升级
                        6.2.0 升级到 6.2 U1后，版本号显示正确
                    配置文件
                        tuna-release.yaml 文件中版本号显示正确
                    hotfix
                        构造一下 6.2U1 p1  看一下带 hotfix 的集群版本号在 tower 各处的显示
                        目前看就集群概览页、升级中心、巡检中心做了适配，其他大部分地方都不带 p1 ，所以目前 6.2 U1 p1 还是保持这种状态嘛：可观测下个版本适配，其余产品确认不做适配
                    filan build
                        没有 build 号时展示正确
                相关产品
                    网络流量可视化
                    内容库
                        编辑虚拟机模板所属集群
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        虚拟机模板批量分发
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        ISO 上传
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        编辑 ISO 映像所属集群
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        ISO 批量分发
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                    高级监控
                        新部署：6.2U1 vmware 集群可以成功部署高级监控
                        600 版本集群部署高级监控后，可以成功升级到 6.2U1
                        该页面中，集群列表的「集群版本」字段正确显示为 6.2U1
                        6.2U1 版本集群兼容的高级监控版本显示为 6.2.1
                    升级中心
                        随升级中心 1.2.2 进行测试
                    巡检中心
                        随巡检中心 1.2.2 进行测试
                    可观测
                        编辑 OBS 服务关联集群时，集群 list 中正确显示了 6.2U1 版本号
                        关联 tower 系统服务时，版本号显示为 4.8p1、4.7 p2
                    cluster installer
                        集群适配
                        tower 适配
                    ER
                        编辑系统服务关联集群
                        ER controller 扩容
                        ER 服务替换节点
                        部署 ER 服务（6.2 U1 符合目标集群版本要求时能成功过滤出来，且版本号显示正确）
                            选择 controller 所属集群
                            选择 LB 实例所属集群
                        相关功能的开启/关闭时的集群版本限制
                            vpc 关联集群
                            创建边缘网关
                            网络负责均衡器 创建 LB 实例
                            网络导流关联集群？不支持 6.2U1 版本集群？
                    备份复制
                        部署
                        关联
                        相关功能的开启/关闭时的集群版本限制
                    SFS
                        相关功能的开启/关闭时的集群版本限制
                        是否拿 tower 版本号：4.8 p1、4.7 p2
                        部署时
                            6.2 U1 符合目标集群版本要求时能成功过滤出来，且版本号显示正确
                        编辑系统服务关联集群时
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                            可以成功关联/取消关联
                    容器镜像仓库
                        部署
                            目标集群：SMTX OS（ELF）双活 6.2 U1，能成功过滤出该集群，且版本号显示正确
                            目标集群：SMTX OS（ELF）单活 6.2 U1，能成功过滤出该集群，且版本号显示正确
                    cloudtower 代理
                        部署时可以成功过滤出 6.2U1 版本集群
                    SKS
                        确认 sks 在 tower 480 里不适配 OS 集群版本改造
            ARCFRA 481
                tower
                    ZBS 集群关联 ELF集群
                    tower 关联集群页面
                        SMTX ELF 6.2 U1
                        SMTX OS（ELF）单活 6.2 U1
                        vmware 单活 6.2 U1
                    集群列表
                        总的集群列表
                        数据中心层级的集群列表
                        「集群版本」字段
                            “6.2 U1” 显示正确
                            集群版本大小排序正确
                        筛选
                            筛选条件“集群版本包含 6.2 U1” 时可以正确筛选出对应版本的集群
                            筛选条件“集群版本不包含 6.2 U1” 时可以正确过滤对应版本的集群
                        导出
                            VMware 6.2 U1 版本号显示正确
                            SMTX OS（ELF） 6.2 U1 版本号显示正确
                    集群概览页
                        “集群”card 版本显示正确
                            SMTX ELF 6.2 U1
                            SMTX OS（ELF）单活 6.2 U1
                            SMTX OS（ELF）双活 6.2 U1
                            vmware 单活 6.2 U1
                    集群设置页
                        「块存储」模块
                            可以将 SMTXOS（ELF）集群的分布式块存储服务通过 iSCSI 协议提供给 SMTX ELF 6.2 U1 集群使用
                        许可
                            SMTX OS 6.2 U1 更新许可成功
                            vmware 单活 6.2 U1 更新许可成功
                            商务系统对应更改？
                    虚拟机
                        虚拟机转换为虚拟机模版
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        虚拟机克隆为虚拟机模板
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        创建空白虚拟机
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        导入虚拟机
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                    虚拟机模板
                        从模板创建虚拟机
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        计算集群上的虚拟机模板转换为虚拟机
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        导入虚拟机模板
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                    虚拟卷
                        创建虚拟卷
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        导入虚拟卷
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                    虚拟机迁移
                        跨集群迁移时，能成功过滤出 6.2U1 集群
                        版本号显示正确
                    报警
                        内置报警规则
                            编辑
                                报警对象可以成功过滤出 6.2 U1 集群
                        自定义报警规则
                            创建
                                集群粒度：可以成功过滤出 6.2 U1 集群，并创建成功
                                虚拟机组粒度：可以成功过滤出 6.2 U1 集群下的虚拟机组，并创建成功
                                虚拟机粒度：可以成功过滤出 6.2 U1 集群下的虚拟机，并创建成功
                            编辑
                                集群粒度：可以新增或减少 6.2U1 集群，并编辑成功
                                虚拟机组粒度：可以新增或减少 6.2U1 集群下的虚拟机组，并编辑成功
                                虚拟机粒度：可以新增或减少 6.2U1 集群下的虚拟机，并编辑成功
                        通知配置
                            邮件
                                集群内部
                                    可以为 6.2U1 集群创建新的邮件通知配置
                                    编辑已有的邮件通知配置，可以新增或减少 6.2U1 集群
                                可观测性
                                    可以为 6.2U1 集群创建新的邮件通知配置
                                    编辑已有的邮件通知配置，可以新增或减少 6.2U1 集群
                            SNMP trap
                                集群内部
                                    可以为 6.2U1 集群创建新的 SNMP trap
                                    编辑已有的 SNMP trap，可以新增或减少 6.2U1 集群
                                可观测性
                                    可以为 6.2U1 集群创建新的 SNMP trap
                                    编辑已有的 SNMP trap，可以新增或减少 6.2U1 集群
                            webhook
                                可以为 6.2U1 集群创建新的 webhook
                                编辑已有的 webhook，可以新增或减少 6.2U1 集群
                        通知策略
                            静默策略
                                可以为 6.2U1 集群创建新的静默策略
                                编辑已有的静默策略，可以新增或减少 6.2U1 集群
                            聚合策略
                                可以为 6.2U1 集群创建新的静默策略
                                编辑已有的静默策略，可以新增或减少 6.2U1 集群
                    快照计划
                        可以为 6.2U1 集群创建新的快照计划
                        已有的快照计划不允许编辑所属集群
                    资源优化
                        预置规则
                            编辑已有规则的应用对象，正确显示 6.2U1 集群版本号，且可以新增或减少该版本的集群
                        自定义规则
                            创建新的自定义规则时应用对象列表，正确显示了 6.2U1 版本号，且可以为该集群创建规则
                            编辑已有规则的应用对象，正确显示 6.2U1 集群版本号，且可以新增或减少该版本的集群
                        动态资源调度-- 未启用集群列表
                            「集群版本」字段正确显示了 6.2U1
                    回收站
                        创建新的特例规则时应用对象列表，正确显示了 6.2U1 版本号，且可以为该集群创建特例规则
                        可以成功编辑 6.2U1 集群的特例规则
                    报表
                        报表模板-资产列表，生成的文件中，集群版本正确显示为 6.2U1
                        自动生成的报表-资产列表，生成的文件中，集群版本正确显示为 6.2U1
                    系统配置
                        syslog 服务器--用于日志传输
                            创建时应用对象列表，正确显示了 6.2U1 版本号，且可以为该集群配置 syslog 服务器
                            编辑已有配置时，正确显示了 6.2U1 版本号，可以新增或减少该版本的集群
                        SNMP 传输
                            创建时应用对象列表，正确显示了 6.2U1 版本号，且可以为该集群配置 SNMP 传输
                            编辑已有配置时，正确显示了 6.2U1 版本号，可以新增或减少该版本的集群
                        虚拟机工具
                            上传时目标集群，正确显示了 6.2U1 版本号，可以将虚拟机工具上传到 6.2U1 版本的集群上
                OS
                    新部署
                        新部署后集群版本号显示正确
                    升级
                        6.2.0 升级到 6.2 U1后，版本号显示正确
                    配置文件
                        tuna-release.yaml 文件中版本号显示正确
                    hotfix
                        构造一下 6.2U1 p1  看一下带 hotfix 的集群版本号在 tower 各处的显示
                        目前看就集群概览页、升级中心、巡检中心做了适配，其他大部分地方都不带 p1 ，所以目前 6.2 U1 p1 还是保持这种状态嘛-----huimin
                    filan build
                        没有 build 号时展示正确
                相关产品
                    网络流量可视化
                    内容库
                        编辑虚拟机模板所属集群
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        虚拟机模板批量分发
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        ISO 上传
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        编辑 ISO 映像所属集群
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                        ISO 批量分发
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                    高级监控
                        新部署：6.2U1 vmware 集群可以成功部署高级监控
                        600 版本集群部署高级监控后，可以成功升级到 6.2U1
                        该页面中，集群列表的「集群版本」字段正确显示为 6.2U1
                        对应出 6.2U1 的高级监控版本嘛？-- 6.2.1
                    升级中心
                        随升级中心 1.2.2 进行测试
                    巡检中心
                        随巡检中心 1.2.2 进行测试
                    可观测
                        编辑 OBS 服务关联集群时，集群 list 中正确显示了 6.2U1 版本号
                        关联 tower 系统服务时，版本号显示为 4.8p1、4.7 p2
                    cluster installer
                        集群适配
                        tower 适配
                    ER
                        编辑系统服务关联集群
                        ER controller 扩容
                        ER 服务替换节点
                        部署 ER 服务（6.2 U1 符合目标集群版本要求时能成功过滤出来，且版本号显示正确）
                            选择 controller 所属集群
                            选择 LB 实例所属集群
                        相关功能的开启/关闭时的集群版本限制
                            vpc 关联集群
                            创建边缘网关
                            网络负责均衡器 创建 LB 实例
                            网络导流关联集群？不支持 6.2U1 版本集群？
                    备份复制
                        部署
                        关联
                        相关功能的开启/关闭时的集群版本限制
                    SFS
                        相关功能的开启/关闭时的集群版本限制
                        是否拿 tower 版本号：4.8 p1、4.7 p2
                        部署时
                            6.2 U1 符合目标集群版本要求时能成功过滤出来，且版本号显示正确
                        编辑系统服务关联集群时
                            能成功过滤出 6.2U1 集群
                            版本号显示正确
                            可以成功关联/取消关联
                    容器镜像仓库
                        部署
                            目标集群：SMTX OS（ELF）双活 6.2 U1，能成功过滤出该集群，且版本号显示正确
                            目标集群：SMTX OS（ELF）单活 6.2 U1，能成功过滤出该集群，且版本号显示正确
                    cloudtower 代理
                        部署时可以成功过滤出 6.2U1 版本集群
                    SKS
                        确认 sks 在 tower 480 里不适配 OS 集群版本改造
    集群硬件管理
        磁盘管理
            515 独立ssd 支持tower相关
                tower 4.6.0
                    原  nohalo （= not os in soft raid1）部署方式，升级到 515 的系统盘展示情况
                    5.1.4 el7 iso，非独立 raid 部署
                        组织层/数据中心层级，主机列表不存在 smtx 系统盘，物理盘表单能正常显示含元数据分区的盘、数据盘、缓存盘
                        能正常批量挂载&单一卸载数据盘
                    514 arm tl3 iso，独立 raid 部署
                        主机层级物理盘表单界面不显示含元数据分区的盘，能正常显示缓存盘、数据盘，主机概览界面能正常显示smtx 系统盘
                        能正常批量挂载&单一卸载缓存盘
                    514 hygon tl3 iso，非独立 raid 部署
                        能正常批量挂载&单一卸载含元数据分区的盘
                        集群层级，主机列表不显示 smtx 系统盘，物理盘列表能正常显示数据盘、缓存盘、含元数据分区的盘
                    5.1.5 独立 raid 部署
                        el7
                            能正常批量挂载&单一卸载数据盘
                            组织层级，主机表单界面正常显示 smtx 系统盘，物理盘表单正常显示缓存盘，数据盘，不显示含元数据分区的盘
                            无法挂载含元数据分区的盘
                        arm oe
                            能正常批量挂载&单一卸载缓存盘
                            数据中心层级，主机列表正常显示 smtx 系统盘
                        oe x86
                            能正常批量挂载&单一卸载存盘
                            集群层级，主机列表正常显示 smtx 系统盘
                        hygon tl3
                            能正常批量挂载&单一卸载缓存盘
                            主机层级，概览界面正常显示 smtx 系统盘，
                    5.1.5 非独立 raid 部署
                        el7
                            能正常批量挂载&单一卸载数据盘
                            主机物理盘表单正常显示含元数据分区的盘、缓存盘，数据盘，概览页面不显示 smtx 系统盘
                        arm tl3
                            能正常批量挂载&单一卸载含元数据分区的盘
                            集群层级主机列表不显示 smtx 系统盘
                        oe x86
                            能正常批量挂载&单一卸载缓存盘
                            数据中心层级主机列表不显示 smtx 系统盘
                        hygon oe
                            能正常批量挂载&单一卸载含元数据分区的数据盘
                            组织层级主机列表界面不显示 smtx 系统盘
                tower 4.4.2
                    5.1.4 el7 iso，非独立 raid 部署
                        tl3 tower
                            组织层/数据中心层级，主机列表不存在 smtx 系统盘，物理盘表单能正常显示含元数据分区的盘、数据盘、缓存盘
                            能正常批量挂载&单一卸载数据盘
                        oe tower
                            组织层/数据中心层级，主机列表不存在 smtx 系统盘，物理盘表单能正常显示含元数据分区的盘、数据盘、缓存盘
                            能正常批量挂载&单一卸载数据盘
                    514 arm tl3 iso，独立 raid 部署
                        tl3 tower
                            主机层级物理盘表单界面不显示含元数据分区的盘，能正常显示缓存盘、数据盘，主机概览界面能正常显示smtx 系统盘
                            能正常批量挂载&单一卸载缓存盘
                        el7 tower
                            主机层级物理盘表单界面不显示含元数据分区的盘，能正常显示缓存盘、数据盘，主机概览界面能正常显示smtx 系统盘
                            能正常批量挂载&单一卸载缓存盘
                    514 hygon tl3 iso，非独立 raid 部署，使用 oe tower
                        能正常批量挂载&单一卸载含元数据分区的盘
                        集群层级，主机列表不显示 smtx 系统盘，物理盘列表能正常显示数据盘、缓存盘、含元数据分区的盘
                    5.1.5 独立 raid 部署
                        独立 ssd 部署嵌套集群升级检查
                        el7，使用 oe tower
                            能正常批量挂载&单一卸载数据盘
                            组织层级，主机表单界面正常显示 smtx 系统盘，物理盘表单正常显示缓存盘，数据盘，不显示含元数据分区的盘
                            无法挂载含元数据分区的盘
                        arm oe，使用 tl3 tower
                            能正常批量挂载&单一卸载缓存盘
                            数据中心层级，主机列表正常显示 smtx 系统盘
                        oe x86，使用 el7 tower
                            能正常批量挂载&单一卸载存盘
                            集群层级，主机列表正常显示 smtx 系统盘
                        hygon tl3 ，使用 el7 tower
                            能正常批量挂载&单一卸载缓存盘
                            主机层级，概览界面正常显示 smtx 系统盘，
                    5.1.5 非独立 raid 部署
                        细分主题 5
                        el7 ，使用 el7 tower
                            能正常批量挂载&单一卸载数据盘
                            主机物理盘表单正常显示含元数据分区的盘、缓存盘，数据盘，概览页面不显示 smtx 系统盘
                        arm tl3，使用 tl3 tower
                            能正常批量挂载&单一卸载含元数据分区的盘
                            集群层级主机列表不显示 smtx 系统盘
                        oe x86，使用 oe tower
                            能正常批量挂载&单一卸载缓存盘
                            数据中心层级主机列表不显示 smtx 系统盘
                        hygon oe，使用 oe tower
                            能正常批量挂载&单一卸载含元数据分区的数据盘
                            组织层级主机列表界面不显示 smtx 系统盘
                    原  nohalo （= not os in soft raid1）部署方式，升级到 515 的系统盘展示情况
                        tl3 tower
                        oe tower
            515 磁盘亚健康调整
                zbs-node show_disk_status 字段变更
                    io error -> chunk io errors count
                    Checksum error ->  chunk checksum errors count
                    chunk io error detected  -> chunk io error count overflow
                    chunk checksum error detected -> chunk checksum error count overflow
                chunk io error detected
                    数据盘
                        chunk 返回的 num_io_errors 为 300 时，值为 false，无告警
                        chunk 返回的 num_io_errors 为 301 时，值为 true，有告警
                    含元数据分区的缓存盘
                        chunk 返回的 num_io_errors 为 301 时，值为 true，有告警
                chunk checksum error detected
                    数据盘
                        chunk 返回的 num_checksum_errors 为 100时，值为 false，无告警
                        chunk 返回的 num_checksum_errors 为 101时，值为 true，有告警
                    含元数据分区的数据盘
                        chunk 返回的 num_checksum_errors 为 101时，值为 true，有告警
                新增 reallocated Sector Count
                    检查 tower 亚健康告警信息(442、470)
                        旧 tower 关联新集群的告警，会出现告警，但磁盘详情页可能没告警信息？
                        新 tower 关联旧集群的告警，能正常告警
                        reallocated 告警的中英文文案
                    缓存盘
                        Reallocated Sector Count = 0，Current Pending Sector Count  = 399
                        Reallocated Sector Count = 0，Current Pending Sector Count  = 400
                        Reallocated Sector Count = 400，Current Pending Sector Count  = 0
                        Reallocated Sector Count = 1，Current Pending Sector Count  = 398
                        Reallocated Sector Count = 1，Current Pending Sector Count  = 399
                    数据盘
                        Reallocated Sector Count = 400，Current Pending Sector Count  = 0
                    含元数据分区的缓存盘
                        Reallocated Sector Count = 1，Current Pending Sector Count  = 398
                    含元数据分区的数据盘
                        Reallocated Sector Count = 1，Current Pending Sector Count  = 399
                磁盘的关联信息采集使用 zbs-node show_disk_status
                    --with_rawdata 参数，用于输出高延时告警前后原始数据
                    extra_info 新增信息
                        iops_threshold
                        sector_ps_threshold
                        bw_mib_ps
                        bw_mib_ps_threshold
                原有内容回归
                    chunk errflag detected ，chunk 标记磁盘有 error flag
                    chunk warnflag detected ，chunk 标记磁盘有 warn flag
                    iostat latency detected，tuna 探测到磁盘存在 io 延时
                    smart error detected，磁盘 smartctl 检查到错误
                    software raid faulty detected，raid 故障告警
                    offline due to io timeout，磁盘 io 超时被内核置为 offline
                    offline due to cmd abort，磁盘 cmd abort 被内核置为 offline
                    offline due to error queue，磁盘错误队列被内核置为 offline
            tower 480 支持磁盘日志导出
                smtxos
                    510 以下的低版本集群
                        不会自动安装 tuna-collector 服务
                        检查日志采集功能是否正常可用
                        界面不会在对应磁盘界面提供日志下载功能
                            磁盘详情页
                            磁盘 more btn
                    510 及以上，630 以下的低版本集群（ el7/oe x86）
                        tuna-collector 服务未就绪时，tower 界面显示采集工具未就绪，对话框中没有下载日志入口
                        安装 tuna-collector 服务
                            tuna-collector  服务状态是否正常
                            集群的日志采集功能是否正常可用
                            自动通过 lcm-manager 下发 tuna-collector rpm 并安装在集群所有节点中
                                部分节点安装成功，界面展示那展示 500 bad gateway
                                全部节点安装成功可以正常下载
                        对具体磁盘进行日志下载
                            5.1.0（elf）
                                默认选择 smartx 日志和 zbs-node 日志（磁盘列表中对应磁盘的 more btn 中触发下载）
                                    含元数据分区的缓存盘
                                        确认smartx 日志和 cmd 获取内容是否一致
                                        确认 zbs-node 日志和 cmd 获取内容是否一致
                            5.1.1（vmware）
                                默认选择 smartx 日志和 zbs-node 日志（磁盘列表中对应磁盘的 more btn 中触发下载）
                                    缓存盘
                                        确认smartx 日志和 cmd 获取内容是否一致
                                        确认 zbs-node 日志和 cmd 获取内容是否一致
                            5.1.2（elf）
                                默认选择 smartx 日志和 zbs-node 日志（磁盘列表中对应磁盘的 more btn 中触发下载）
                                    数据盘（不含 journal）
                                        确认smartx 日志和 cmd 获取内容是否一致
                                        确认 zbs-node 日志和 cmd 获取内容是否一致
                            5.1.3（vmware）
                                默认选择 smartx 日志和 zbs-node 日志（磁盘列表中对应磁盘的 more btn 中触发下载）
                                    未挂载的盘
                                        确认smartx 日志和 cmd 获取内容是否一致
                                        确认 zbs-node 日志和 cmd 获取内容是否一致
                            5.1.4（vmware）
                                选择所属主机的 message 日志（磁盘详情页触发下载）
                                    含元数据分区的缓存盘
                                        message 日志是否和主机中的一致
                            5.1.5（elf）
                                选择所属主机的 message 日志（磁盘详情页触发下载）
                                    缓存盘
                                        message 日志是否和主机中的一致
                            6.0.0（vmware）
                                选择所属主机的 message 日志（磁盘详情页触发下载）
                                    数据盘（不含 journal）
                                        message 日志是否和主机中的一致
                            6.1.0（elf）
                                选择所属主机的 message 日志（磁盘详情页触发下载）
                                    未挂载的盘
                                        message 日志是否和主机中的一致
                            6.1.1（elf）
                                默认选择 smartx 日志和 zbs-node 日志（磁盘列表中对应磁盘的 more btn 中触发下载）
                                    含元数据分区的数据盘（不含缓存分区）
                                        确认smartx 日志和 cmd 获取内容是否一致
                                        确认 zbs-node 日志和 cmd 获取内容是否一致
                            6.2.0（elf）
                                默认选择 smartx 日志和 zbs-node 日志（磁盘列表中对应磁盘的 more btn 中触发下载）
                                    数据盘（含 journal）
                                        确认smartx 日志和 cmd 获取内容是否一致
                                        确认 zbs-node 日志和 cmd 获取内容是否一致
                    6.3.0 版本（hygon tl3）
                        tuna-collector 服务自身
                            集群本身的 tuna-collector 版本大于/等于 tower 中携带的版本，是否不会降低版本，日志采集功能是否正常可用，是否能正常触发磁盘日志下载
                            集群本身的 tuna-collector 版本小于 tower 中携带的版本
                                对其升级前，界面展示未就绪
                                升级后，界面可以正常下载磁盘日志
                                集群的日志采集功能正常可用
                        对具体磁盘进行日志下载
                            默认选择 smartx 日志和 zbs-node 日志（磁盘列表中对应磁盘的 more btn 中触发下载）
                                挂载中的含元数据分区的缓存盘
                                    确认smartx 日志和 cmd 获取内容是否一致
                                    确认 zbs-node 日志和 cmd 获取内容是否一致
                            选择所属主机的 message 日志（磁盘详情页触发下载）
                                含元数据分区的数据盘（不含缓存分区）
                                    message 日志是否和主机中的一致
                                挂载中的数据盘
                                    message 日志是否和主机中的一致
                smtxzbs
                    550 以下的低版本集群
                        不会自动安装 tuna-collector 服务
                        界面不会在对应磁盘界面提供日志下载功能
                        检查日志采集功能是否正常可用
                    550 及以上的集群（arm oe）
                        tuna-collector 服务未就绪时，tower 界面显示采集工具未就绪，界面没有下载日志入口（磁盘列表的 more btn 和 磁盘详情页）
                        安装 tuna-collector 服务
                            自动通过 lcm-manager 下发 tuna-collector rpm 并安装在集群所有节点中
                            tuna-collector  服务状态是否正常
                            集群的日志采集功能是否正常可用
                        对具体磁盘进行日志下载
                            5.6.1
                                默认选择 smartx 日志和 zbs-node 日志（磁盘列表中对应磁盘的 more btn 中触发下载）
                                    含元数据分区的数据盘（含缓存分区，共享盘）
                                        确认smartx 日志和 cmd 获取内容是否一致
                                        确认 zbs-node 日志和 cmd 获取内容是否一致
                            5.6.0
                                默认选择 smartx 日志和 zbs-node 日志（磁盘列表中对应磁盘的 more btn 中触发下载）
                                    数据盘（缓存共享盘）
                                        确认smartx 日志和 cmd 获取内容是否一致
                                        确认 zbs-node 日志和 cmd 获取内容是否一致
                            5.5.0
                                默认选择 smartx 日志和 zbs-node 日志（磁盘列表中对应磁盘的 more btn 中触发下载）
                                    卸载中的盘
                                        确认smartx 日志和 cmd 获取内容是否一致
                                        确认 zbs-node 日志和 cmd 获取内容是否一致
                            5.6.2
                                选择所属主机的 message 日志（磁盘详情页触发下载）
                                    含元数据分区的数据盘（含缓存分区，共享盘）
                                        message 日志是否和主机中的一致
                            5.6.3
                                选择所属主机的 message 日志（磁盘详情页触发下载）
                                    数据盘（缓存共享盘）
                                        message 日志是否和主机中的一致
                            5.6.4
                                选择所属主机的 message 日志（磁盘详情页触发下载）
                                    卸载中的盘
                                        message 日志是否和主机中的一致
                            5.7.0
                                选择所属主机的 message 日志（磁盘详情页触发下载）
                                    含元数据分区的数据盘（不含缓存分区）
                                        message 日志是否和主机中的一致
                其他情况测试
                    ui 覆盖
                        默认选择  smartx 日志和 zbs-node 日志，且不可取消勾选
                        选择系统日志后可以取消勾选
                        磁盘日志下载对话框中/英文文案对比检查
                    下载文件大小& 内容
                        1 G
                        5 G
                        10 G
                        高延迟磁盘，zbs-node 日志需要有磁盘速率内容
                        raid 故障盘 + io error + error flag
                        check sum error + smart error
                    故障测试
                        注入故障后，host plug 无法安装/升级成功，检查第二次重试是否能正常完成安装/升级
                        注入故障后，下载日志失败，恢复后检查是否能正常下载
                        下载日志过程中重启对应节点 tuna-collector 服务
                        触发下载日志前重启节点的 tuna-collector 服务，检查界面文案
                        第一次安装 tuna-collector 时，因为其他 lcm 操作（角色转换/扩缩容等）导致冲突失败，集群需要正常可用，无异常出现，且下一个任务周期能正常安装完成
                        已经安装好 tuna-collector 后，即使存在非扩容的其他 lcm 操作，也可以下载磁盘日志
                        扩容完成后，需要等待新节点部署完成 tuna-collector 服务才可以正常下载
                        注入故障后，采集日志失败，恢复后能正常恢复采集，不受影响
                            缓存路径在 /tmp/disk-logs/任务 uuid
                            需要关注多次采集一个盘，缓存内容是否不会被应用（1 h 周期 ）
                    升级测试
                        tower 版本升级，lcm-manager 中携带的 tuna-collector 版本大于当前集群中已安装版，会触发更新 tuna-collector 服务，在更新完成前磁盘日志下载对话框提示采集工具未就绪
                            tower 升级正常
                            日志采集/磁盘日志下载正常
                        低版本集群升级（升级到非 630 版本）后，关注 tuna-collector 服务是否正常工作
                            集群升级正常
                            日志采集/磁盘日志下载正常
                        集群升级后的 tuna-collector 比 tower 的 tuna-collector 高，tuna-collector 跟随集群版本
                            集群升级正常
                            日志采集/磁盘日志下载正常
        PCI 设备管理
            网卡
                tower470 SR-IOV 展示变更
                    不支持
                        集群版本在 6.0 之上(包括 smtxos 和 smtxelf)，且网卡不支持
                            展示为不支持
                            more btn 编辑网口用途不展示 SR-IOV 信息
                        集群版本在 6.0 之下，为 el7 /oe x86 集群，且网卡不支持
                            展示为不支持
                            more btn 编辑网口用途不展示 SR-IOV 信息
                        集群版本在 6.0 之下，且为 arm 集群 / hygon 集群
                            展示为不支持
                            more btn 编辑网口用途不展示 SR-IOV 信息
                    驱动未安装
                        网卡支持，且升级到 6xx 版本，但内核未升级
                            展示为驱动未安装
                            hover 提示「请将集群 Kernel 升级至当前集群对应的版本，以使用 SR-IOV 直通功能。」
                            more btn 编辑网口用途展示 SR-IOV ，但选项 disable
                    驱动未就绪
                        网卡支持，且升级到 6xx 版本，并且内核也升级完成，但主机还未重启
                            展示为驱动未就绪
                            hover 提示「请重启主机，以使用 SR-IOV 直通功能。」
                            more btn 编辑网口用途展示 SR-IOV ，但选项 disable
                    未启用
                        网卡支持，且升级到 6xx 版本，并且内核也升级完成，主机已经重启，但未配置网口用途为 SRIOV
                            展示为未启用
                            more btn 编辑网口用途展示 SR-IOV ，且选项可选
                    待重启
                        网卡支持，且升级到 6xx 版本，并且内核也升级完成，主机已经重启，配置网口用途为 SRIOV，但还未完成重启
                            展示为待重启
                            hover 提示 「请重启主机， SR-IOV 才会生效。」
                            more btn 编辑网口用途展示 SR-IOV ，已选择
                    已启用
                        直接部署的高版本集群，若网卡支持应该为未启用
                        网卡支持，且升级到 6xx 版本，内核也升级完成，主机已经重启，配置网口用途为 SR-IOV，已完成重启
                            网口用途展示为 SR-IOV 直通
                            SR-IOV 正常展示数量
                            SR-IOV 已使用数量正常展示
                            more btn 出现重新切分 SR-IOV 直通网卡选项
                            编辑网口用途选项包括 SR-IOV 选项
                            重新切分 SR-IOV 数量后，通过 lspci 命令可以看见虚拟网口，ip a 也能看见新增的网口
                    高级筛选和排序
                        排序检查（除 「不支持」、「未启用」）
                        SR-IOV 状态
                            全部
                            驱动未安装
                            驱动未就绪
                            待重启
                            已启用
                        SR-IOV 直通网卡数量
                            ≥
                            >
                            ≤
                            <
                            =
                        SR-IOV 直通网卡已使用数量
                            ≥
                            >
                            ≤
                            <
                            =
                630启用 sriov 减少一次启动
                    smtxos
                        mellanox
                            sriov 状态为已启用/未启用/不支持/驱动未安装 时，没有重配按钮
                            节点没有开启 iommu，开启后网卡选择为 sriov 切分，默认切分数量和最大数量一致，sriov 状态为待重启
                            点击重配按钮后， tower 界面出现任务，任务同步下发到集群，执行完成后有审计事件
                            重配成功后，网卡状态为待重启，重配按钮消失
                            重启后 sriov 状态为未启用，可以正常启用并配置 sriov 切分
                            节点没有开启 iommu，开启后网卡选择为 sriov 切分，默认切分数量和最大数量不一致
                                版本为 630，网卡的 sriov 状态是驱动未就绪，出现重配按钮
                                版本小于 630，网卡的 sriov 状态是驱动未就绪，但不存在重配按钮
                        Solarflare
                            sriov 状态为已启用/未启用/不支持/驱动未安装 时，没有重配按钮
                            节点没有开启 iommu，开启后网卡选择为 sriov 切分，默认切分数量和最大数量一致，sriov 状态为待重启
                            点击重配按钮后， tower 界面出现任务，任务同步下发到集群，执行完成后有审计事件
                            重配成功后，网卡状态为待重启，重配按钮消失
                            重启后 sriov 状态为已=未启用，可以正常启用并配置 sriov 切分
                            节点没有开启 iommu，开启后网卡选择为 sriov 切分，默认切分数量和最大数量不一致
                                版本为 630，网卡的 sriov 状态是驱动未就绪，出现重配按钮
                                版本小于 630，网卡的 sriov 状态是驱动未就绪，但不存在重配按钮
                    smtxelf
                        mellanox
                            sriov 状态为已启用/未启用/不支持/驱动未安装 时，没有重配按钮
                            节点没有开启 iommu，开启后网卡选择为 sriov 切分，默认切分数量和最大数量一致，sriov 状态为待重启
                            点击重配按钮后， tower 界面出现任务，任务同步下发到集群，执行完成后有审计事件
                            重配成功后，网卡状态为待重启，重配按钮消失
                            重启后 sriov 状态为已启用，可以正常配置 sriov 切分
                            节点没有开启 iommu，开启后网卡选择为 sriov 切分，默认切分数量和最大数量不一致
                                版本为 630，网卡的 sriov 状态是驱动未就绪，出现重配按钮
                                版本小于 630，网卡的 sriov 状态是驱动未就绪，但不存在重配按钮
                        Solarflare
                            sriov 状态为已启用/未启用/不支持/驱动未安装 时，没有重配按钮
                            节点没有开启 iommu，开启后网卡选择为 sriov 切分，默认切分数量和最大数量一致，sriov 状态为未启用
                            点击重配按钮后， tower 界面出现任务，任务同步下发到集群，执行完成后有审计事件
                            重配成功后，网卡状态为待重启，重配按钮消失
                            重启后 sriov 状态为已启用，可以正常配置 sriov 切分
                            节点没有开启 iommu，开启后网卡选择为 sriov 切分，默认切分数量和最大数量不一致
                                版本为 630，网卡的 sriov 状态是驱动未就绪，出现重配按钮
                                版本小于 630，网卡的 sriov 状态是驱动未就绪，但不存在重配按钮
    集群软件管理
        系统服务管理
            620 podman 移除
                场景测试
                    升级
                        自动化覆盖升级路径/特性
                            SMTX ZBS
                                arm
                                    5.6.2 -> 5.7.0
                                    5.6.1 -> 5.7.0
                                    5.6.0 -> 5.7.0
                                    5.5.0 -> 5.7.0
                                    5.4.1 -> 5.7.0
                                    5.4.0 -> 5.7.0
                                    5.3.0 -> 5.7.0
                                    5.2.0 -> 5.7.0
                                hygon
                                    5.6.2 -> 5.7.0
                                    5.6.1 -> 5.7.0
                                    5.6.0 -> 5.7.0
                                    5.5.0 -> 5.7.0
                                    5.4.1 -> 5.7.0
                                    5.4.0 -> 5.7.0
                                    5.3.0 -> 5.7.0
                                    5.2.0 -> 5.7.0
                                    5.0.0 -> 5.4.1 -> 转 oe ->  5.7.0
                                centos x86
                                    5.6.2 -> 5.7.0
                                    5.6.1 -> 5.7.0
                                    5.6.0 -> 5.7.0
                                    5.5.0 -> 5.7.0
                                    5.4.1 -> 5.7.0
                                    5.4.0 -> 5.7.0
                                    5.3.0 -> 5.7.0
                                    5.2.0 -> 5.7.0
                                    5.1.0 -> 541 -> 560 -> 5.7.0
                                    5.0.0 -> 5.40 -> 5.5.0-> 5.7.0
                功能测试
                    mongodb
                        日志达到上限后会切文件
                    envoy
                        日志达到上限后会切文件
                    vipservice
                        日志达到上限后会切文件
                        确认获取的内存使用量正确
            hotpatch -  (514 hp & 515)
                功能验证
                    5.1.4-P1  手动清理 logrotate.tuna.d  后能正常安装 patch
                    6.2.0-P4 执行预检查&安装 patch 会在日志里面显示检查 smtx-release 后进入到下一个节点的检查，不会安装 patch，不应该清理 logrorate.tuna.d 路径
                    5.1.4 P1 双活集群安装 patch 时，仲裁节点不会跳过执行
                    5.1.4-P1 使用 oe arm 版本直接部署，tower 使用 460 版本，可观测使用 1.3.1 版本，关联可观测并配置好流量可视化，部分节点存在特别大日志文件（logrotate.tuna.d  中配置的服务日志，且接近写满系统分区）
                        预检查
                            存在大日志文件文件节点在 console 输出中的 Display oversized logs found 步骤存在 [KB0007335] Oversized log detected: /var/log/zbs/consul-server/consul-server.log (1.1GiB) 相关输出
                            不存在大日志文件节点在 console 输出中的 Display oversized logs found 步骤显示 [KB0007335] No oversized logs found.
                        安装中
                            观察安装过程中节点根分区所在硬盘的 %util 不会明显升高
                            安装日志没有异常输出
                        安装后
                            重新执行预检查，console 中所有节点显示均为 No oversized logs found.
                            观察第一次轮转日志时节点根分区所在硬盘的 %util 不会明显升高
                            检查升级完成后主机服务是否正常没有发生重启
                            检查安装完成后日志被清理，空间释放
                            不会出现 watch dog kill 服务（查看 messages 日志）
                            watchdog 日志不会出现新增写入耗时较长的日志（ curl 127.0.0.1:10300/api/v1/watchdog/log_warn）
                            检查安装后 logrotate.tuna.d 路径是否不存在
                            检查原 logrotate.tuna.d 中的配置是否在 logrotate.smartx.d 中存在
                            手动给指定日志增加文件大小，检查定时任务是否能正确轮转日志
                            取消关联 & 重新关联可观测，各节点上也不存在 logrotate.tuna.d 路径
                            执行巡检检查集群
                            检查原 logrotate.tuna.d 中配置的日志是否在正常记录
                                /var/log/ipmi-agent/
                                /var/log/ovm-agent/
                                /var/log/zbs/vipservice/
                    5.1.4-P1 升级到 515 使用 tl3 v2 arm 版本，使用独立 ssd 部署，tower 使用 450 版本，可观测使用 1.3.1 版本，关联可观测并配置好流量可视化，存在特别大日志文件（logrotate.tuna.d  中配置的服务日志，且接近写满系统分区）
                        预检查
                            存在大日志文件文件节点在 console 输出中的 Display oversized logs found 步骤存在 [KB0007335] Oversized log detected: /var/log/zbs/consul-server/consul-server.log (1.1GiB) 相关输出
                            不存在大日志文件节点在 console 输出中的 Display oversized logs found 步骤显示 [KB0007335] No oversized logs found.
                        安装中
                            观察安装过程中节点根分区所在硬盘的 %util 不会明显升高
                            安装日志没有异常输出
                        安装后
                            重新执行预检查，console 中所有节点显示均为 No oversized logs found.
                            观察第一次轮转日志时节点根分区所在硬盘的 %util 不会明显升高
                            检查升级完成后主机服务是否正常没有发生重启
                            检查安装完成后空间自动释放
                            不会出现 watch dog kill 服务（查看 messages 日志）
                            watchdog 日志不会出现新增写入耗时较长的日志（ curl 127.0.0.1:10300/api/v1/watchdog/log_warn）
                            检查安装后 logrotate.tuna.d 路径是否不存在
                            检查原 logrotate.tuna.d 中的配置是否在 logrotate.smartx.d 中存在
                            手动给指定日志增加文件大小，检查定时任务是否能正确轮转日志
                            升级可观测后检查各节点上也不存在 logrotate.tuna.d 路径
                            执行巡检检查集群
                            检查原 logrotate.tuna.d 中配置的日志是否在正常记录
                                /var/log/ovm-agent/
                                /var/log/zbs/vipservice/
                    5.1.4-P1 升级到 515 使用 hygon oe 版本直接部署，tower 使用 450 版本，可观测使用 1.3.1 版本，关联可观测并配置好流量可视化，不存在特别大的日志文件（logrotate.tuna.d  中配置的服务日志，但存在较多其他日志或日志压缩包
                        预检查
                            所有节点 console 输出中的 Display oversized logs found 步骤显示 [KB0007335] No oversized logs found.
                        安装中
                            观察安装过程中节点根分区所在硬盘的 %util 不会明显升高
                            安装日志没有异常输出
                        安装后
                            重新执行预检查，console 中所有节点显示均为 No oversized logs found.
                            观察第一次轮转日志时节点根分区所在硬盘的 %util 不会明显升高
                            不会出现 watch dog kill 服务（查看 messages 日志）
                            watchdog 日志不会出现新增写入耗时较长的日志（ curl 127.0.0.1:10300/api/v1/watchdog/log_warn）
                            检查安装后 logrotate.tuna.d 路径是否不存在
                            检查原 logrotate.tuna.d 中的配置是否在 logrotate.smartx.d 中存在
                            手动给指定日志增加文件大小，检查定时任务是否能正确轮转日志
                            其他日志不会被清理
                            取消关联 & 重新关联可观测，各节点上也不存在 logrotate.tuna.d 路径
                            执行巡检检查集群
                            检查原 logrotate.tuna.d 中配置的日志是否在正常记录
                                /var/log/ovm-agent/
                                /var/log/zbs/vipservice/
                    5.0.5 -
                        5.1.4-P1(oe x86,vmware 集群），tower 使用 4.6.0，无可观测，不存在特别大的日志文件
                            预检查
                                所有节点 console 输出中的 Display oversized logs found 步骤显示 [KB0007335] No oversized logs found.
                            安装中
                                观察安装过程中节点根分区所在硬盘的 %util 不会明显升高
                                安装日志没有异常输出
                            安装后
                                重新执行预检查，console 中所有节点显示均为 No oversized logs found.
                                观察第一次轮转日志时节点根分区所在硬盘的 %util 不会明显升高
                                不会出现 watch dog kill 服务（查看 messages 日志）
                                watchdog 日志不会出现新增写入耗时较长的日志（ curl 127.0.0.1:10300/api/v1/watchdog/log_warn）
                                检查安装后 logrotate.tuna.d 路径是否不存在
                                检查原 logrotate.tuna.d 中的配置是否在 logrotate.smartx.d 中存在
                                手动给指定日志增加文件大小，检查定时任务是否能正确轮转日志
                                执行巡检检查集群
                                检查原 logrotate.tuna.d 中配置的日志是否在正常记录
                                    /var/log/ipmi-agent/
                                    /var/log/ovm-agent/
                                    /var/log/zbs/vipservice/
                升级验证
                    5.1.4-P1 安装 hotfix patch 后升级到 5.1.5-P1，检查  logrotate.tuna.d 路径是否不存在
                    5.1.4-P1 安装 hotfix patch 后升级到 6.2.0-P4，升级完成后检查  logrotate.tuna.d 路径是否存在，再次安装 patch 时日志显示检查  smtx-release 后直接进入下一个节点的检查，不会继续安装 ，日志轮转正常
                    5.1.4-P1 升级到 5.1.5 后安装 hotfix package，安装后安装 515 P1  logrotate.tuna.d 路径是否不存在
                    5.1.4-P1 升级到 5.1.5 后安装 hotfix package，安装后升级 630，检查 logrotate.tuna.d 路径是否存在
            514 hp3 logrotate 机制
                使用 tower 4.6.2
                安装 iso（需要集群中存在虚拟机并且存在小 io）
                    使用 oe x86 iso，vhost + 独立 ssd 部署
                    检查 message 日志中不存在 watchdog kill 服务
                    检查 watchdog 日志不存在异常  curl 127.0.0.1:10300/api/v1/watchdog/log_warn
                    不存在 /etc/logrotate.tuna.d 配置路径
                    新版本巡检没有 logrotate 配置目录的告警
                    vipservice
                        制造 /var/log/zbs/vipservice/vipservice.log 超过 200M ，检查是否正常 logrotate，检查 logrotate 后日志是否能正常产生
                    ovm-agent
                        制造 /var/log/ovm-agent/collector.log 超过 500M，检查是否正常 truncate，检查 logrotate 后日志是否能正常产生
                        制造 /var/log/ovm-agent/configcenter-agent.log 超过 200M，检查是否正常 logrotate，检查 logrotate 后日志是否能正常产生
                        制造 /var/log/ovm-agent/vector-agent.log 超过 1G，检查是否正常 truncate，检查 logrotate 后日志是否能正常产生
                        制造 /var/log/ovm-agent/vmagent.log 复制后超过剩余根分区容量（超过 1G），检查是否正常 truncate，检查 logrotate 后日志是否能正常产生
                    ipmi-agent
                        制造 /var/log/ipmi-agent/alert-proxy.log 存在超过 500M 日志，检查是否正常 truncate，检查 logrotate 后日志是否能正常产生
                        制造 /var/log/ipmi-agent/ipmi-agent-clean.log 存在超过 200M 日志，检查是否正常 logrotate，检查 logrotate 后日志是否能正常产生
                        制造 /var/log/ipmi-agent/ipmi-agent-init.log 存在超过 1G 日志，检查是否正常 truncate，检查 logrotate 后日志是否能正常产生
                        制造 /var/log/ipmi-agent/ipmi-agent.log存在超过 200M 日志，检查是否正常 logrotate，检查 logrotate 后日志是否能正常产生
                    其他服务（挑选两个）
                        制造 /var/log/zbs/job-center-worker.celery.INFO 存在超过 1G 日志，检查是否正常 truncate，检查 logrotate 后日志是否能正常产生
                        制造 /var/log/zbs/cluster_upgrade.INO 存在超过 200M 日志，检查是否正常 logrotate，检查 logrotate 后日志是否能正常产生
                    检查各节点的 logrotate.sh 文件内容是否符合预期
                        /usr/share/smartx/script/logrotate.sh
                安装 hotfix package
                    使用 tl3 hygon iso，不分层部署
                    安装前准备（不同节点选择其中的一部分配置，不重复，且保持一个节点没有其中的异常）
                        制造 /var/log/ovm-agent/vector-agent.log  存在复制后超过剩余根分区容量（超过 1G）
                        制造 /var/log/ovm-agent/configcenter-agent.log 超过 200M
                        制造 /var/log/ipmi-agent/ipmi-agent-init.log 存在不超过 10 M 日志
                    安装后
                        会存在 /etc/logrotate.tuna.d 配置路径
                        新版本巡检中心不存在 logrotate 配置告警
                        安装日志检查
                            无异常日志产生
                        日志文件检查
                            /var/log/ovm-agent/vector-agent.log  被 truncate，无压缩包，且有新日志产生
                            /var/log/ovm-agent/configcenter-agent.log 存在压缩包，且有新日志产生
                            /var/log/ipmi-agent/ipmi-agent-init.log 没有压缩包，日志和原来一致没有被 truncate
                        配置文件检查
                            /usr/share/smartx/script/logrotate.sh
                        节点空间检查
                            系统分区占用空间出现明显释放
                        制造超大日志文件，执行 logrotate 动作系统资源检查
                            系统盘 %util 使用率不会明显提升到 80% 以上
                            cpu 使用率上限不会超过 50%（top 观察）
                升级 iso
                    使用 oe arm iso，分层部署
                    升级前准备不同节点选择其中的一部分配置，不重复，且保持一个节点没有其中的异常）
                        制造 /var/log/zbs/vipservice/vipservice.log 存在复制后超过剩余根分区容量（超过 1G）
                        制造 /var/log/ovm-agent/vector-agent.log 超过 5 G
                        制造 /var/log/ipmi-agent/alert-proxy.log 存在超过 10G
                    升级后检查
                        会存在 /etc/logrotate.tuna.d 配置路径
                        新版本巡检中心不存在 logrotate 配置告警
                        升级日志检查
                            无异常日志产生
                        日志文件检查
                            /var/log/zbs/vipservice/vipservice.log  不存在压缩包，有新日志产生
                            /var/log/ovm-agent/vector-agent.log 没有压缩包，正常产生新日志
                            /var/log/ipmi-agent/alert-proxy.log 正常产生新日志
                        配置文件检查
                            原有配置：/usr/share/smartx/script/logrotate.sh
                        节点空间检查
                            系统分区占用空间出现明显释放
                        制造超大日志文件，执行 logrotate 动作系统资源检查
                            系统盘 %util 使用率不会明显提升到 80% 以上
                            cpu 使用率上限不会超过 50%（top 观察）
                迭代路径
                    5.1.4 - 5.1.4-P1 直接安装/升级到 package 版本
                    5.1.4-P1 - one time patch 后直接安装/升级到 package 版本
                    5.1.3 - 5.1.4-P1 ，手动清理 logrotate.tuna.d 后直接安装/升级到 package 版本
                    完整按照 ticket 中执行的测试用例路径根据覆盖一次
        服务资源管理
            CPU
                cgroup
                    smtxos
                        功能测试
                            cgroup 配置
                                主机启动时 NVMe盘顺序变化，chunk绑定的 numa node 变更后 cgconfig 配置可能与当前 cgroup 冲突导致 cgconfig 启动失败
                                zbs cgroups NUMA node 选择
                                    arm 集群 - chunk cgroup 中 cpu 在 HBA 卡所在 numa node 上 (SMTXOS 5.1.2/6.0.0)
                                    开启超线程，zbs/others 组和zbs/chunk-main 组CPU都不会从同一个物理核心上分配（SMTXOS 5.1.4）
            620hp3 cgroup
                安装部署
                    平台和路径
                        不开启任何功能 - centos x86 - storage CPU: 8，master CPU: 9
                        开启 vhost - arm 飞腾 - storage CPU: 11，master CPU: 12
                        开启 vhost - hygon - storage CPU: 11，master CPU: 12
                        oe x86 - storage CPU: 8，master CPU: 9
                        vmware - centos x86（CPU：6）配置保持不变
                        SMTXELF - oe x86 - storage CPU: 4，master CPU: 5
                        zbs 平台不涉及变动，不用关注
                    安装部署/升级/补丁安装后检查点
                        升级后 ovs-vswitchd、ovsdb-server(不会重启)、svcresctld 重启成功且运行正确
                        在 master 、storage 节点运行 cpuset 脚本，确认 cpuset 所在 cgroup 符合预期 (witness  节点不需要检查)
                        升级前流量可视化打开 - 升级完成确认移动到 zbs/app
                        /etc/cgconfig.d/cpuset.conf 配置检查
                            SMTXOS kvm master节点 zbs/app CPU 个数为：4，zbs/network 已经删除
                            SMTXOS kvm  storage节点 zbs/app CPU 个数为：3，zbs/network 已经删除
                            SMTXELF master节点 zbs/app CPU 个数为：4，zbs/network 已经删除
                            SMTXELF storage节点 zbs/app CPU 个数为：3，zbs/network 已经删除
                        service
                            ovsdb-server.service 预期所在 cgroup: smtx.slice/smtx-network.slice/ovsdb-server.service -  - 检查配置文件：/etc/systemd/system/ovsdb-server.service.d/cgroup.conf
                            ovs-vswitchd.service 预期所在 cgroup: smtx.slice/smtx-network.slice/ovs-vswitchd.service - 检查配置文件：/etc/systemd/system/ovs-vswitchd.service.d/cgroup.conf
                            安装补丁后重启节点后进行检查
                            服务设置 CPU 额度为： 5%
                                vipservice (systemctl cat xxx | grep CPUQuota) 检查所属的(上层) slice
                                network-firewall
                                net-health-check
                        cpu cgroup
                            smtxos kvm
                                smtx.slice/smtx-network.slice cpu.cfs_quota_us 值：200000 （限制 2个 core）
                                master (zbs/app: 4，smtx.slice: 8)
                                    smtx.slice cpu.shares 值：8192
                                    user.slice + init.slice(可能不存在) + machine.slice + system.slice 的 cpu.shares = 4096（或3072）
                                    smtx.slice/smtx-network.slice cpu.shares 值：(动态计算) ～= 2389 （7168/3 ～= 2389.3）
                                storage (zbs/app: 3，smtx.slice: 8)
                                    smtx.slice cpu.shares 值：8192
                                    user.slice + init.slice(可能不存在) + machine.slice + system.slice 的 cpu.shares = 4096（或3072）
                                    smtx.slice/smtx-network.slice cpu.shares 值：(动态计算) - 3583（公式计算结果实际是 3584，但是开发计算 share 先取整了，有一点误差影响不大，保持现在的计算方式）
                                arm 飞腾 master (zbs/app: 5，smtx.slice: 8)
                                    smtx.slice cpu.shares 值：8192
                                    user.slice + init.slice + machine.slice + system.slice 的 cpu.shares = 4096
                                    smtx.slice/smtx-network.slice cpu.shares 值：(动态计算) - 1792
                                arm 飞腾 storage (zbs/app: 4，smtx.slice: 8)
                                    smtx.slice cpu.shares 值：8192
                                    user.slice + init.slice + machine.slice + system.slice 的 cpu.shares = 4096
                                    smtx.slice/smtx-network.slice cpu.shares 值：(动态计算) - 1792
                            SMTXELF
                                smtx.slice/smtx-network.slice cpu.cfs_quota_us 值：200000 （限制 2个 core）
                                master (zbs/app: 4，smtx.slice: 7)
                                    smtx.slice cpu.shares 值：8192
                                    smtx.slice/smtx-network.slice cpu.shares 值：(动态计算) - 2048
                                    user.slice + init.slice(有可能不存在) + machine.slice + system.slice 的 cpu.shares = 4096
                                storage (zbs/app: 3，smtx.slice: 7)
                                    smtx.slice cpu.shares 值：8192
                                    smtx.slice/smtx-network.slice cpu.shares 值：(动态计算) - 3072
                                    user.slice + init.slice + machine.slice + system.slice 的 cpu.shares = 4608
                    资源竞争（可以不验证，文飞会覆盖）
                        当 zbs/app  CPU 被打满时，smtx.slice 和 user.slice + init.slice + machine.slice + system.slice 的 CPU 使用比例：2:1
                        smtx-network.slice  被打满且 zbs/app 未被打满，查看最多使用 2 CPU 资源
                        zbs/app  CPU 未被打满，正常使用 smtx-network.slice ，network 使用 1 CPU
                    角色转换
                        master 转 storge
                        storage 转 master
                升级
                    升级路径
                        SMTXOS kvm centos x86 4.0.14 升级到 6.2.0 P3 （zbs/app: 2 -> 4）
                        SMTXOS kvm oe x86  5.1.4（开启流量可视化） 升级到 6.2.0 P3 （zbs/app: 2 -> 4）
                        SMTXOS kvm arm 6.1.0 升级到 6.2.0 P3 （zbs/app: 3 -> 4）
                        SMTXOS vmware ọe 6.1.1 升级到 6.2.0 P3（无变化）
                        SMTXELF oe x86 6.0.0 升级到 6.2.0 P3 （zbs/app: 2 -> 4）
                        SMTXELF arm 6.1.1 升级到 6.2.0 P3 （zbs/app: 3 -> 4）
                        开启 vhost：5.0.5 -> 620 P3
                        SMTXOS kvm centos x86 双活 4.0.14 升级到 6.2.0 P3
                        SMTXOS kvm oe x86 vhost + rdma  6.1.0 升级到 6.2.0 P3
                        3 节点嵌套 16 个CPU，独占5个 CPU，5.1.4 升级到 6.2.0 P3 可以成功 （zbs-dynamic/aurora-ha 升级过程短暂使用1个 CPU，最多可独占5个 CPU，否则不能开机）
                补丁安装
                    安装路径
                        SMTXOS kvm centos x86：6.2.0 P2 -> 620 P3
                        SMTXOS kvm oe x86：6.2.0 P1 -> 620 P3
                        SMTXOS kvm arm: 6.2.0 -> 6.2.0 P3
                        SMTXOS kvm hygon: 6.2.0 -> 6.2.0 P3
                        SMTXOS vmware oe x86：6.2.0 -> 620 P3 (配置保持不变)
                        SMTXELF oe x86：6.2.0 P1 -> 620 P3
                        SMTXELF arm: 6.2.0 -> 6.2.0 P3
                资源指标回归
                    资源指标回归
                        cpu_cpuset_state_percent （TUNA-2649）
                            zbs/network 查询不到数据
                            查询 全部 CPU 使用率
                            查询单个 CPU 使用率
                            查询 cpuset: zbs/app 组的cpu 使用率
                    扩展指标确认（后台命令行打开规则项）
                        6.1.1 版本 开启扩展服务和资源告警 - 升级集群到 6.2.0 P3 - 无异常告警信息产生
                        安装部署的集群，开启扩展服务和资源告警 - 无异常告警信息产生
                        物理集群 - 安装补丁后，开启扩展服务和资源告警 - 无异常告警信息产生
                        检查告警规则 - 手动触发告警规则
                            cpuset cgroup  /zbs/app 期望的 cpus 限制为，实际为
                            cpu cgroup 期望的 rt_runtime_us 为，实际为
                            cpu cgroup 期望的 rt_period_us 为，实际为
                            cpuset cgroup zbs/network 不存在 (不会产生此条告警，确认配置文件中 zbs/network 已经被删除)
                            服务 xx 期望的 CGroupPath
                                服务 ovs-vswitchd.service 期望的CGroupPath 为，实际为
                                服务 ovsdb-server.service 期望的CGroupPath 为，实际为
            630 cgroup 网络独占核心
                网络独立核心需求
                    性能 sdn 测试
                    功能&回归测试
                        独立核心
                            服务检查
                                切换到独立核心服务不会重启
                                运行在 zbs/network
                                    ovs-vswitch
                                    ovsdb-server
                                    network- firewall
                                    net-health-check
                                    traffice-mirror
                                    mcast-agent
                                    vipservice
                                    ovs-coverage
                                    netguard
                                    L2Ping
                                    lldpd
                                    netreactor
                                    everoute 和 流量可视化 相关进程
                                        everoute-agent
                                        everoute-collector
                                        everoute 相关的 agent
                                        healthproxy
                                        eradm
                            核心数检查
                                zbs/app  master 3核心，storage 2 核心
                                zbs/network 2 核心
                                飞腾 zbs/app 多一个核心
                            配置文件
                                /etc/zbs/network_cpu_mode 配置文件,并且文件内容符合预期
                                cat /etc/cgrules.conf 增加网络服务的配置，并且在network 分组下
                                独立网络核心，删掉配置文件，重启之后仍是独立核心，但是执行config 会变成share核心
                                独立网络核心，清空配置文件，重启之后仍是独立核心，但是执行config 会变成share核心
                            扩容节点
                                新节点预期和集群的配置保持一致---【根据控制节点的network_cpu_mode信息确定新节点的信息（/etc/zbs/network_cpu_mode 文件的生成）】
                                新节点的cpuset  配置符合预期
                                扩容的日志检查看下：exec: svcrescheck run
                            回归
                                指标告警回归
                                    指标检查 cpu_cpuset_state_percent - /zbs/network 组有采集
                                    告警：cpuset cgroup /zbs/network  期望的 cpus 限制为，实际为
                                    告警：服务 ovs-vswitchd.service 期望的CGroupPath 为，实际为
                                    回归指标：cpu_cpuset_state_percent - /zbs/app 组有采集
                                    回归告警：cpuset cgroup /zbs/app 期望的 cpus 限制为，实际为
                                服务设置 CPU 额度 和内存限制
                                    lldpd        5%        50MiB
                                    net-health-check        5%        100MiB
                                    network-firewall        5%        50 MiB
                                    vipservice        5%        100MiB
                                    mcast-agent        5%        100MiB
                                    ovs-coverage        5%        50MiB
                                    traffic-mirror        5%        100MiB
                                    l2ping        20%        100MiB
                                    netreactor        5%        50 MiB
                                    netguard        5%        50MiB
                                    ovs-vswitchd 无限制
                                    ovsdb-server 无限制
                                运维回归
                                    缩容
                                    内存预留不变
                                    重启主机之后配置不变
                                    同版本升级环境配置不变
                                    zbs-deploy-manage config_cgroup 执行之后cpuset 不变
                                    角色转换
                                        storage-> master
                                        master->storage
                        共享核心 - 预期保持620 hp4 一样的网络配置-回归为主
                            服务检查
                                切换回共享核心-服务没有重启
                                运行在 zbs/app -这里没有修改，选取几个服务确认
                                    ovs-vswitch
                                    ovsdb-server
                                    network- firewall
                                    net-health-check
                                    vipservice
                                    L2Ping
                                    everoute 相关进程：everoute-agent
                            核心数检查
                                zbs/app  master 4核心，storage 3 核心
                                network 分组不存在
                                飞腾情况下多1个核心
                            配置文件
                                /etc/zbs/network_cpu_mode 配置文件,并且文件内容符合预期
                                cat /etc/cgrules.conf 不包含网络服务的配置
                            回归
                                cat /sys/fs/cgroup/cpu/smtx.slice/smtx-network.slice cpu.cfs_quota_us 值：200000 （限制 2个 core）
                                /etc/systemd/system/smtx-network.slice.d/99-svcres.conf  里面的CPUQuota 是 200%
                                运维
                                    安装部署环境预期默认是share 核心
                                    主机重启后配置符合预期
                                    低版本升级上来-默认都是share 核心
                                        51X->630
                                        50X->630
                                        40X->630
                                        620 p4->630
                                    角色转换
                                        storage-> master ，符合master预期
                                        master->storage，符合storage 预期
                                    扩容节点
                                        如果集群是升级上来，预期新节点上面有配置；控制节点没有
                                        如果集群是从独立核心切换回来，或者新部署集群，预期新节点和已有节点上的配置文件一致 【根据控制节点的network_cpu_mode信息确定新节点的信息（/etc/zbs/network_cpu_mode 文件的生成）】
                                        新节点的cpu 配置符合预期
                                        扩容的日志检查看下：exec: svcrescheck run
                                share值
                                    os elf master
                                        master (zbs/app: 4，smtx.slice: 8 +1  meta-main 新增 1 核心)
                                        master：smtx.slice cpu.shares 值：8192
                                        master： smtx.slice/smtx-network.slice cpu.shares 值：(动态计算) ～= 2389 （7168/3 ～= 2389.3）
                                    os elf storage
                                        master (zbs/app: 3，smtx.slice: 8)
                                        master：smtx.slice cpu.shares 值：8192
                                        master： smtx.slice/smtx-network.slice cpu.shares 值：(动态计算) ～= 3583
                                服务设置 CPU 额度 和内存限制
                                    lldpd        5%        50MiB
                                    net-health-check        5%        100MiB
                                    network-firewall        5%        50 MiB
                                    vipservice        5%        100MiB
                                    mcast-agent        5%        100MiB
                                    ovs-coverage        5%        50MiB
                                    traffic-mirror        5%        100MiB
                                    l2ping        20%        100MiB
                                    netreactor        5%        50 MiB
                                    netguard        5%        50MiB
                                    ovs-vswitchd 无限制
                                    ovsdb-server 无限制
                                指标告警回归
                                    指标检查 cpu_cpuset_state_percent - /zbs/network 组没有数据; zbs/app 组有数据
                                    告警：cpuset cgroup /zbs/app  期望的 cpus 限制为，实际为
                                    告警：服务 ovs-vswitchd.service 期望的CGroupPath 为，实际为
                        命令行 zbs-cluster network_cpu_mode
                            help
                            打印符合预期
                            传递非预期的参数提示
                            独立核心：zbs-cluster network_cpu_mode set --mode isolate_normal
                                检查配置文件内容正确：/etc/zbs/network_cpu_mode
                                cpu 核心符合预期
                                开启独立核心的时候，如果cpu 核心不够，cgroup 配置时候失败，不会滚，检查重试成功& cgroup配置符合预期
                            共享核心：zbs-cluster network_cpu_mode set --mode share
                                检查配置文件内容正确：/etc/zbs/network_cpu_mode
                                cpu 核心符合预期
                        场景测试
                            51X->630  开启独立核心
                            50X->630 开启独立核心
                            40X->630 开启独立核心
                            620 hp2->630 开启独立核心
                            620 hp4 ->630 开启独立核心
                            开启独立核心之后再关闭
                            开启故障-试一下开启过程中，个别节点断连，之后修复故障再重试；预期是成功的
                    平台路径
                        vmware 环境
                            zbs/app: master 2 核心 ; storage 2 核心
                            vmware 执行命令行不生效，预期有提示
                            cpu 总体占用 +1：6 +1  核心（chunk 多实例meta-main +1）
                        hygon chunk 4个实例  环境
                            命令行
                            共享核心
                            开启独立核心
                        arm 2实例 鲲鹏
                            命令行
                            共享核心
                            开启独立核心
                        arm  飞腾
                            命令行
                            共享核心
                            开启独立核心
                        双活环境
                            仲裁节点不处理，命令行看下
                            在仲裁节点上执行，witness 节点预期不会做配置，其他节点可以配置成功
                            其他节点同上面检查点
                        smtxelf 环境
                            命令行
                            共享核心
                            开启独立核心
                        arcfra 环境
                            命令行
                            共享核心
                            开启独立核心
                        tencent os
                            命令行
                            共享核心
                            开启独立核心
            515 hp catl 网络独占核心
                后续升级路径测试是要加一个这个hp calt的 升级路径
                独立核心
                    zbs-deploy cgroup config 执行之后独立核心配置不变
                    服务检查
                        切换到独立核心服务没有重启
                        运行在 zbs/network
                            ovs-vswitch
                            ovsdb-server
                            vipservice
                            L2Ping
                            lldpd
                            netreactor
                            everoute 和 流量可视化 相关进程
                                everoute-agent
                                everoute-collector
                                everoute/.../agent
                                healthproxy
                                eradm
                    核心数检查
                        zbs/app  master 3核心，storage 2核心
                        zbs/network 2 核心
                    配置文件
                        /etc/zbs/network_cpu_mode 配置文件,并且文件内容符合预期
                        cat /etc/cgrules.conf 增加网络服务的配置，并且在network 分组下 --- 全量列表目前是；再讨论下
                        独立网络核心，删掉配置文件，重启之后变成共享核心，执行config 会把cgrules.conf 中 network 清理掉
                        独立网络核心，清空配置文件，重启之后变成共享核心，执行config 会把cgrules.conf 中 network 清理掉
                    扩容节点
                        新节点预期和集群的配置保持一致---【根据控制节点的network_cpu_mode信息确定新节点的信息（/etc/zbs/network_cpu_mode 文件的生成）】
                        新节点的cpu 配置符合预期
                        扩容的日志检查看下：exec: svcrescheck run
                    回归
                        内存预留不变
                        运维
                            缩容
                            向630升级- 符合630的独立核心配置情况
                            515 hp1 catl 原地补丁看一下- 符合独立核心配置
                            重启主机之后独立核心配置不变
                            角色转换
                                storage-> master
                                master->storage
                        指标告警回归
                            指标检查 cpu_cpuset_state_percent - /zbs/network 组有采集
                            告警：cpuset cgroup /zbs/network  期望的 cpus 限制为，实际为
                            告警：服务 l2ping@storage.service 期望的CGroupPath 为，实际为
                            回归指标：cpu_cpuset_state_percent - /zbs/app 组有采集
                            回归告警：cpuset cgroup /zbs/app 期望的 cpus 限制为，实际为
                        服务设置 CPU 额度 和内存限制
                            lldpd        5%        50MiB
                            vipservice        5%        100MiB
                            l2ping        20%        100MiB
                            netreactor        5%        50 MiB
                            ovs-vswitchd 无 无
                            ovsdb-server 无无
                共享核心回归
                    服务检查
                        切换回共享核心-网络相关服务无重启
                        运行在 zbs/app
                            ovs-vswitch
                            ovsdb-server
                            vipservice
                    核心数检查
                        zbs/app  master 3核心，storage 2 核心
                        network 分组不存在
                        回归
                            zbs/meta-main 1核心
                            zbs/chunk-main 1核心
                            zbs/chunk-io 1核心
                            zbs/others 1核心
                    配置文件
                        切换回share mode：/etc/zbs/network_cpu_mode 配置文件,并且文件内容符合预期
                        补丁升级上来/etc/zbs/network_cpu_mode 配置文件不存在
                        cat /etc/cgrules.conf 不包含网络服务的配置
                    扩容节点
                        集群原节点无配置 - 新节点预期有/etc/zbs/network_cpu_mode配置
                        新节点的cpu 配置符合预期
                        扩容的日志检查看下：exec: svcrescheck run
                    回归
                        运维
                            主机重启
                            缩容
                            515->515 hp catl 补丁都是默认 share核心
                            安装部署环境预期默认是share 核心
                            515 p1 catl ->630 上述配置符合预期
                            515 p1 catl-原地补丁环境上述配置符合预期
                            角色转换
                                storage-> master
                                master->storage
                            低版本升级上来 ，默认也是share 核心
                                512>513> 515 p1 catl
                                513 hp->515 p1 catl
                                515 > 515 p1 calt
                        服务设置 CPU 额度 和内存限制
                            lldpd        5%        50MiB
                            vipservice        5%        100MiB
                            l2ping        20%        100MiB
                            netreactor        5%        50 MiB
                            ovs-vswitchd 无 无
                            ovsdb-server？
                        指标告警回归
                            指标检查 cpu_cpuset_state_percent - /zbs/network 组没有数据; zbs/app 组有数据
                            告警：cpuset cgroup /zbs/app  期望的 cpus 限制为，实际为
                            告警：服务l2ping.service 期望的CGroupPath 为，实际为
                命令行 zbs-cluster network_cpu_mode
                    help
                    返回打印符合预期
                    非法参数提示
                    共享核心：zbs-cluster network_cpu_mode set --mode share
                        检查配置文件内容正确：/etc/zbs/network_cpu_mode
                        cpu 核心符合预期
                    独立核心：zbs-cluster network_cpu_mode set --mode isolate_normal
                        检查配置文件内容正确：/etc/zbs/network_cpu_mode
                        cpu 核心符合预期
                        开启独立核心的时候，如果cpu 核心不够？
                场景测试
                    512>513> 515 p1 catl oe x86 开启独立核心---物理环境测试
                    513 hp->515 p1 catl oe x86 开启独立核心
                    515 > 515 p1 calt oe x86 开启独立核心
                    故障测试 - 开启过程中节点失联
                    客户手动配置过，会被盖住，重新开启独占模式，预期配置符合预期
            630 cgroup chunk 多实例和内存告警
                cgroup
                    cpuset  （基于zbs 570 做过完整测试，这里只测试有差异的地方）
                        iscsi 增强模式不测试
                        nvmf 不会启用
                        numa 优选预期& group 放置和zbs 570一样，有物理环境简单看1-2组
                        meta main
                            normal 1实例 -2 核心
                            large 4 实例  - 2 核心
                            large 2 实例 - 2核心
                            small 1实例 - 1 核心
                        app
                            非飞腾开启独立核心时候master 变为3个核心，storage 为2
                            非飞腾未开启独立核心时候 master 4个核心，storage 为3
                            飞腾开启独立核心时候master 和 storage 都为4
                            飞腾未开启独立核心时候master  和storage 5
                        iscsi
                            未开启 iscisi 增强模式，不打开
                                1实例
                                多实例
                        aurora
                            1实例 2个核心
                            2实例 2个核心
                            4实例 4个核心
                            1 实例 不开启vhost 不开启
                        zbs-dynamic/aurora-ha
                            开启vhost 时候开启 1个核心
                        zbs/chunk-cprs
                            双活 1核心
                            非双活不开启
                        zbs/lsm-dbN
                            1实例  vhost 1 核心
                            2 实例 vhost  2 核心
                            4 实例 vhost 4 核心
                            非vhost，不开启
                        zbs/chunk-dcN -剪枝
                            未开启 RDMA & 单实例  不开启
                            开启RDMA 单实例 2核心
                            未开启RDMA&2实例  2核心
                            未开启RDMA&4实例 4核心
                            开启RDMA & 4实例  4 核心
                        zbs/chunk-insN -剪枝
                            单实例&未开启vhost
                                lsm-io 0
                                chunk -main  1
                                chunk-io 1
                            单实例开启vhost
                                lsm-io 2
                                chunk-main 1
                                chunk-io 1
                            4实例&开启vhost
                                lsm-io  8
                                chunk -main  4
                                chunk-io 4
                            2实例&开启vhost
                                lsm -io 4
                                chunk-main 2
                                chunk-io 2
                        单 NUMA 6 物理核心(ZBS 570 不支持)
                            app 2
                            chunk-ins1 2
                            others 1
                            meta-main 1
                        vmware 环境
                            zbs others 1
                            其他都不开启
                            master total 为10 或者 9或者8
                            meta-main
                                small 1核心
                                normal 2 核心
                            chunk-insN
                                lsm-io 0
                                chunk -main  1
                                chunk-io 1
                            zbs/app
                                master 2
                                storage 2
                            chunk-dc
                                RDMA  2
                                未开启 RDMA 0
                        smtxelf 环境
                            meta-main  1
                            zbs/app  master4  storage 3 (未开启独立核心)
                    memory
                        ARM 模式下，zbs.chunk 多占用 2 G 内存，zbs570 测试过
                        vmware 环境，qemu 0， 3个dmalloc
                        zbs.metamain  占用保持  6 G, zbs.others 占用保持 3 G
                        smtx elf zbs 没有占用内存，qemu 和 os elf 计算一样
                        zbs  分组占用
                            small 单实例
                            normal 单实例
                            large 2 实例
                            large 单实例
                            smtx-zbs-chunkd.slice
                                10/20/40 + C + 2 (ARM)
                                8 G  x 实例数 +  2 G  IO buffer * 实例数+ C:   （节点上挂载的所有 Partition 每 10 TiB 对应 * 1.5 G向上取整）；
                                之前测试过每种规格最大数据盘挂载，这里不单独测试 C的上限了，测试普通挂载计算公式是对的即可
                                双活 + 1
                        大页
                            单实例模式保持 3 G +  2G （vHost 开启）
                            多实例模式下为 8 G +  2G （vHost 开启）
                                2实例
                                4实例
                        OS 上挂载的 Cache 分区体积
                            Partition * 20% ，则按照每 8 TiB Cache 增加 2 G 的方式来增加内存占用  -  测试下
                                数据盘 10T
                                挂载cache 超过数据盘20% 以上8T
                    回归
                        升级集群检查QE 和 DF环境未打test 标签环境-随机检查一些
                        4实例开启 RDMA & vhost
                            大页：   8 dmalloc + 2 vhost
                            如果 OS 上挂载的 Cache 分区体积 > Partition * 20% ，则按照每 8 TiB Cache 增加 2 G
                            内存预留   =  63 + partition部分(上限39G) + cache超出部分 + qemu动态计算 +[1 双活]  +[1 vHost] +[2 ARM] + [大页内存]
                            smtx.slice - 分组名称后面要改下
                                分组变化
                                smtx-elf.slice        3
                                smtx-tuna.slice        4
                                smtx-network.slice        2
                                smtx-lcm.slice        5
                                smtx-infra.slice        3
                                    smtx-infra-mongod.slice - 新名字    smtx-mongod.slice    2 挪出infra 分组, 放到上级分组：smtx.slice
                                    smtx-infra-zk.slice    新名字   smtx-zk.slice     2 挪出竟然分组，放到上级分组：smtx.slice
                                    smtx-infra-jc.slice        1
                                    smtx-infra-common.slice        2
                                smtx-zbs.slice        49 + ?
                                    smtx-zbs-metamain.slice        6
                                    smtx-zbs-others.slice        3
                                    smtx-zbs-chunkd.slice
                                        40G + parition部分(上限-/-/39G)+cache超出部分        +[1 vhost] +[1 双活] + [2 ARM]
                                        8 G  x 实例数 +  2 G  IO buffer * 实例数+  C:  （节点上挂载的所有 Partition 每 10 TiB 对应 * 1.5 G向上取整） & Cache 分区体积 > Partition * 20% ，则按照每 8 TiB Cache 增加 2 G 的方式来增加内存占用
                                smtx-obs.slice        2
                                    smtx-obs-prometheus.slice       1
                            qemu
                                1. x86_64：5.5G + 节点物理内存总量G/128
                                2. aarch64: 17G + 节点物理内存总量G/256G * 100M
                                x86 非vhost 预留   800M
                                x86 vhost 不预留800M
                                非 vhost arm 环境不预留 800 M
                            cpu 总核心占用32 +
                                zbs/meta-main  2
                                zbs/others 1
                                zbs/app  非独立核心 master 4 ， storage 3
                                zbs/iscsi 1 不开启
                                zbs/lsm-db1-db4  4
                                zbs/chunk-dc1- dc4   4
                                zbs/aurora 4
                                zbs-dynamic/aurora-ha 1
                                nvmf 不开启
                                chunk-ins1& ins2&ins 3& ins4  16
                                    zbs/lsm-io 2*4
                                    zbs/chunk-main 1*4
                                    zbs/chunk-io 1*4
                            chunk 配置
                                ISCSI_USE_THREAD= false
                                DATA_CHANNEL_THREAD_COUNT= 1
                                LSM_IO_THREAD_NUM=2
                                ZBS_DMALLOC_USES_HUGEPAGE=true
                                ZBS_DMALLOC_MEMORY_SIZE=8589934592
                内存告警
                    扩展指标回归 - 默认开启哪些& 手动开启回归一下
                    全量物理环境搜下，如果有触发看下是否符合使用场景
                    内存压力事件告警 （irate(cgroup_memory_pressure_event_total[5m])
                        { .threshold } threshold: 0,  INFO ）
                            告警静默和告警聚合视情况回归
                            集群未关联可观测触发&解决
                            关联可观测触发&解决
                            集群部署高级监控~略
                            告警规则
                                Tower 上面新增告警规则
                                    新部署tower
                                    升级tower
                                    未关联新版本集群的tower 预期不展示
                                编辑告警规则-端到端检查触发
                                    修改阈值
                                    禁用、启用
                                    告警级别编辑
                                    设置特例规则
                            告警触发
                                增加某个组的压力判断触发时效和文案提示是否满足等
                                检查告警对象、触发时间、报警源、告警等级、报警规则、持续时间
                                告警文案中英文检查
                                    Message
                                        中： 检测到 { .labels.hostname } 上分组 { .labels._name } 出现内存压力事件。
                                        英： A memory pressure event occurred on the group { .labels._name } of the host { .labels.hostname }.
                                    Cause
                                        中：节点上的系统服务内存占用出现异常升高。
                                        英： The memory usage of system services on the node has increased abnormally.
                                    Impacts
                                        中：节点的稳定性受到影响。
                                        英：The node's stability is affected.
                                    Solutions
                                        中： 请联系售后进行处理。
                                        英:  Please contact technical support for assistance.
                                不同内存分组触发
                                    user.slice
                                    smtx-tuna.slice
                                    stress 进程指定到分组
                                    指标数值的验证验证，查看指标曲线走势图
                                    子组
                                        mongo
                                        zk
                            告警解决
                                自动解决
                                解决时间
                            告警接收至少检查一组
                                webhook
                    内存使用量频繁达到限制量告警 （min_over_time(irate(cgroup_memory_failcnt[5m])[5m:])
                        { .threshold } threads: 1000,  NOTICE ）
                            告警静默和告警聚合视情况回归
                            集群未关联可观测触发&解决
                            关联可观测触发&解决
                            集群部署高级监控~略
                            告警规则
                                如果有平台区分，比方vmware 或者smtxelf 不支持要看一下，适用集群里预期不包含在报警对象里
                                Tower 上面新增告警规则
                                    新部署tower
                                    升级tower
                                    未关联新版本集群的tower 预期不展示
                                编辑告警规则-端到端检查触发
                                    修改阈值
                                    禁用、启用
                                    告警级别编辑
                                    设置特例规则
                            告警触发
                                增加某个组的压力判断触发时效和文案提示是否满足等
                                检查告警对象、触发时间、报警源、告警等级、报警规则、持续时间
                                告警文案中英文检查
                                    Message
                                        中：检测到 { .labels.hostname } 上分组 { .labels._name } 内存使用量频繁达到上限。
                                        英：The memory usage on the group { .labels._name } of the host { .labels.hostname } frequently reaches its limit.
                                    Cause
                                        中：节点上的系统服务内存负载较高。
                                        英：The memory load of system services on the node is high.
                                    Impacts
                                        中：节点的稳定性受到影响。
                                        英：The node's stability is affected.
                                    Solutions
                                        中：请联系售后进行处理。
                                        英:  Please contact technical support for assistance.
                                不同内存分组触发
                                    user.slice
                                    smtx-network.slice
                                    子组
                                        jc
                                        zbs-chunk
                            告警解决
                                自动解决
                                解决时间
                            告警接收至少检查一组
                                webhook
                    默认开启的指标
                        /metrics/cgroups 接口，注册是的优先级为 VERY_HIGH。
                        cgroup_memory_pressure_event_total (新增指标，分组内存压力，忽略无数值的分组)
                        cgroup_memory_failcnt （分组内存频繁达到限制量，忽略无数值的分组）
                        cgroup_memory_usage_total （分组内存使用量，默认忽略200MB以下的分组，开启了扩展指标时全部采集）
                        cgroup_cpu_usage_total （分组 CPU 使用量，忽略无数值的分组）
                        cgroup_cpu_nr_throtteld （CPU 受限制的程度： nr_throtteld 变化量/nr_periods 变化量， 忽略无数值的分组）
                        cgroup_cpu_nr_periods（CPU 受限制的程度， 忽略无数值的分组）
                        新部署环境
                        升级环境
                    平台架构
                        vmware
                        双活仲裁 会有顶层层级告警
                        升级集群 hygon
                        新部署 arm tl3
                        smtxelf
                        arcfra - 关键字
                            arcfra 升级环境
                            arcfra 新部署环境
                            非arcfra 升级环境，涉及关键字去除，要检查下smtx.slice 分组以及下面的子组名称
                                4.X
                                50X
                                51X
                                6.X
            630 系统服务内存&cpu资源限制
                内存和cpu限制 -服务名称；cpu quota；内存限制；所在分组
                    网络 - 随独立核心验证完，不再测试 - 630 去掉了 network cpu quota 的限制
                    双活仲裁看一下
                    arcfra 不测试，tl3 要看下
                    SRE 和基础组件的压力测试-不容易构造随df 长稳运行测试
                    df 和qe 环境开启扩展指标观察下
                    TUNA-5108 调整重要任务的 oom score
                    新部署
                    SRE
                        tuna-rest-server        -        400MiB        smtx-tuna.slice
                        tuna-exporter        10%        200MiB        smtx-tuna.slice
                        disk-healthd        10%        200MiB        smtx-tuna.slice
                        sd-offline        10%        100MiB        smtx-tuna.slice
                        tuna-collector        30%        3GiB        smtx-tuna.slice    	 目前是在 /usr/lib/systemd/system/tuna-collector.service 里直接做的限制， 采集日志涉及到压缩，消耗 cpu 较高。
                        network-monitor        10%        200MiB        smtx-tuna.slice
                        master-monitor        10%        200MiB        -
                        consul-exporter        10%        100MiB        smtx-tuna.slice
                        octopus        10%        400MiB        smtx-obs.slice
                        oscar        10%        50MiB        smtx-obs.slice
                        siren        10%        200MiB        smtx-obs.slice
                        fluent-bit        20%        200MiB        smtx-obs.slice
                        prometheus        20%       内存在上层组限制  san:8GiB, else: 1GiB
                        vmagent        10%        300MiB        smtx-obs.slice
                        snmpd        10%        400MiB        smtx-obs.slice
                        dolphin        10%        -        smtx-obs.slice
                        node-exporter        10%        100MiB        smtx-obs.slice
                        aquarium        10%        100MiB        smtx-tuna.slice
                        crab        -       100MiB        smtx-tuna.slice
                        seal        10%        100MiB        smtx-tuna.slice
                        harbor        -       100MiB        smtx-tuna.slice
                        zbs-deploy-server        -        -        smtx-lcm.slice
                        cluster-upgrader        20% ?        -        smtx-lcm.slice  升级涉及到 iso 上传过程里，是否会有临时的内存需求
                        cloudtower-installer        10%        -        smtx-lcm.slice
                        smtx-lcm.slice:   -,  5GiB
                        smtx-obs.slice:   -,  2GiB
                        smtx-tuna.slice:  -, 4GiB
                    基础组件
                        mongod        -        -        -900        smtx-mongod.slice        smtx-mongod.slice: -, 3G (无变化)
                        zookeeper        -        -        -900        smtx-zk.slice        smtx-zk.slice: -, 2G (无变化)
                        job-center-scheduler        5%        200MiB                smtx-infra-jc.slice        smtx-infra-jc.slice: -, 1G
                        job-center-worker        -        -                smtx-infra-jc.slice
                        consul-server        10%        300MiB                smtx-infra-common.slice
                        consul        10%        200MiB                smtx-infra-common.slice
                        envoy        20%(设在父组)        -                smtx-infra-envoy.slice        smtx-infra-envoy.slice: -, 400M    需要加上 cpu quota
                        envoy-xds        10%        100MiB                smtx-infra-common.slice
                        nginx        -        -                smtx-infra-common.slice
                        svcresctld        10%        400MiB                smtx-infra-common.slice
                        ntpm        5%        100MiB                smtx-infra-common.slice
                        chronyd        5%        100MiB                smtx-infra-common.slice
                        zbs-watchdogd        5%        100MiB                smtx-infra-common.slice
                        containerd        -        -                smtx-tuna.slice
                        dnsmasq        5%        50MiB                system.slice        dnsmasq 是否也挪到smtx-tuna.slice 下去？
                        crond        -        -                system.slice
                        rsyslog        -        -                system.slice
                        user.slice  0.5c
                        system.slice:  -, 4G
                        smtx-infra-common.slice: -, 2G
                        smtx-infra.slice: -, 6G -> 3G
                    ZBS
                        zbs-rest-server        20%        400MiB        smtx-zbs-app.slice
                        timemachine        20%        300MiB        smtx-zbs-app.slice
                        zbs-inspectord        20%        150 MiB        smtx-zbs-app.slice
                        zbs-iscsi-redirectord        30%        300 MiB        smtx-zbs-app.slice
                        整组： -        800MiB        smtx-zbs-app.slice:
                        zbs-taskd 30% 300 MiB smtx-zbs-app.slice
                    ELF
                        elf-vm-scheduler	200	-	200 MiB	smtx-elf.slice
                        elf-dhcp	50	20%	200MiB	smtx-elf.slice
                        elf-vm-monitor	200	-	200 MiB	smtx-elf.slice
                        elf-vm-watchdog	200	-	100 MiB	smtx-elf.slice
                        vnc-proxy	100	10%	100 MiB	smtx-elf.slice
                        elf-exporter	50	30%	500 MiB	smtx-elf.slice
                        elf-rest-server	100	-	500 MiB	smtx-elf.slice
                        libvirtd	200	-	200 MiB	smtx-elf.slice
                        vmtools-agent	100	40%	200 MiB	smtx-elf.slice
                        usbredir-manager	100	10%	100 MiB	smtx-elf.slice
                        elf-fs	100	10%		smtx-elf.slice
                        vm-security-controller	100	15%	50 MiB	smtx-elf.slice
                        virtlogd	200	-	200 MiB	smtx-elf.slice
                        smtx-elf.slice:  -, 3GiB
                    smtxelf
                        基础组件 -同上
                        SRE -同上
                        elf -同上
                    vmware
                        基础组件 -同上
                        SRE -同上
                        ZBS -同上
                    升级环境
                        4.X
                        50X
                        51X
                        6.X
                        自动化脚本检查限制配置&生效
                    运维场景
                        升级到高版本（build），资源限制服务预期
                        节点重启之后，资源限制服务预期
            621 cgroup
                网络独立核心
                    性能 sdn 测试
                    功能&回归测试
                        独立核心
                            服务检查
                                切换到独立核心服务不会重启服务
                                运行在 zbs/network - 选取几个
                                    ovs-vswitch
                                    ovsdb-server
                                    everoute 和 流量可视化 相关进程
                                        everoute-agent
                            核心数检查
                                zbs/app  master 3核心，storage 2 核心
                                zbs/network 2 核心
                                飞腾 zbs/app 多2个核心
                            配置文件
                                /etc/zbs/network_cpu_mode 配置文件,并且文件内容符合预期
                                cat /etc/cgrules.conf 增加网络服务的配置，并且在network 分组下
                            扩容节点
                                新节点预期和集群的配置保持一致---【根据控制节点的network_cpu_mode信息确定新节点的信息（/etc/zbs/network_cpu_mode 文件的生成）】
                                新节点的cpuset  配置符合预期
                                扩容的日志检查看下：exec: svcrescheck run -e
                            回归
                                指标告警回归
                                    指标检查 cpu_cpuset_state_percent - /zbs/network 组有采集
                                    告警：cpuset cgroup /zbs/network  期望的 cpus 限制为，实际为
                                    告警：服务 ovs-vswitchd.service 期望的CGroupPath 为，实际为
                                    回归指标：cpu_cpuset_state_percent - /zbs/app 组有采集
                                    回归告警：cpuset cgroup /zbs/app 期望的 cpus 限制为，实际为
                                服务设置 CPU 额度 和内存限制  CPU Quota	Memory Quota
                                    lldpd        5%        50MiB
                                    net-health-check        5%        100MiB
                                    network-firewall        5%        50 MiB
                                    vipservice        5%        100MiB ，所在组一起看下
                                    mcast-agent        5%        100MiB
                                    ovs-coverage        5%        50MiB
                                    traffic-mirror        5%        100MiB
                                    l2ping        20%        100MiB
                                    netreactor        5%        50 MiB
                                    netguard        5%        50MiB
                                    ovs-vswitchd 无 无
                                    ovsdb-server
                                    smtx-network.slice  （200% 去掉了？， 2GiB）
                                运维回归
                                    缩容
                                    内存预留不变
                                    重启主机之后配置不变
                                    同版本升级环境配置不变
                                    zbs-deploy cgroup config 执行之后cpuset 不变
                                    角色转换
                                        storage-> master
                                        master->storage
                        共享核心 - 预期保持620 hp4 一样的网络配置-回归为主
                            服务检查
                                切换回共享核心-服务没有重启
                                运行在 zbs/app -这里没有修改，选取几个服务确认
                                    vipservice
                                    L2Ping
                            核心数检查
                                zbs/app  master 4核心，storage 3 核心
                                network 分组不存在
                            配置文件
                                /etc/zbs/network_cpu_mode 配置文件,并且文件内容符合预期
                                cat /etc/cgrules.conf 不包含网络服务的配置
                            回归
                                和app共用三个核心
                                    cat /sys/fs/cgroup/cpu/smtx.slice/smtx-network.slice cpu.cfs_quota_us 值：-1
                                    share值
                                        os elf master
                                            master (zbs/app: 3，smtx.slice: 8)
                                            master：smtx.slice cpu.shares 值：8192
                                            master： smtx.slice/smtx-network.slice cpu.shares 值：(动态计算) ～= 2389 （7168/3 ～= 2389.3）
                                        os elf storage
                                            master (zbs/app: 4，smtx.slice: 8)
                                            master：smtx.slice cpu.shares 值：8192
                                            master： smtx.slice/smtx-network.slice cpu.shares 值：(动态计算) ～= 3583
                                服务设置 CPU 额度为： 5%
                                    lldpd        5%        50MiB
                                    net-health-check        5%        100MiB
                                    network-firewall        5%        50 MiB
                                    vipservice        5%        100MiB
                                    mcast-agent        5%        100MiB
                                    ovs-coverage        5%        50MiB
                                    traffic-mirror        5%        100MiB
                                    l2ping        20%        100MiB
                                    netreactor        5%        50 MiB
                                    netguard        5%        50MiB
                                    ovs-vswitchd 无 无
                                    ovsdb-server 无 无
                                    smtx-network.slice  （200% 去掉了？， 2GiB）
                                运维
                                    安装部署环境预期默认是share 核心
                                    低版本升级上来-默认都是share 核心
                                        51X->621
                                    角色转换
                                        storage-> master ，符合master预期
                        命令行 zbs-cluster network_cpu_mode
                            help
                            打印符合预期
                            传递非预期的参数提示
                            独立核心：zbs-cluster network_cpu_mode set --mode isolate_normal
                                检查配置文件内容正确：/etc/zbs/network_cpu_mode
                                cpu 核心符合预期
                            共享核心：zbs-cluster network_cpu_mode set --mode share
                                检查配置文件内容正确：/etc/zbs/network_cpu_mode
                                cpu 核心符合预期
                        场景测试
                            514 P3 ->621  开启独立核心
                            620 hp2->621 开启独立核心
                            开启独立核心之后再关闭
                            6.2.1 升级到6.3.0 不支持不需要测试
                            5.1.5 P2 开启独立核心之后升级到6.2.1 符合独立核心配置
                    平台路径
                        vmware 环境
                            zbs/app: master 2 核心 ; storage 2 核心
                            vmware 执行命令行不生效，预期有提示
                            cpu 总体占用保持不变：6 核心（chunk 多实例再看下是否有变化）
                        arm  飞腾
                            命令行
                            共享核心
                            开启独立核心
                        双活环境
                            仲裁节点不处理，命令行看下
                            在仲裁节点上执行，预期不会做配置
                            其他节点同上面检查点
                        smtxelf 环境
                            命令行
                            共享核心
                            开启独立核心
                        arcfra 环境
                            命令行
                            共享核心
                            开启独立核心
                621 cgroup 常规回归
                    内存
                        内存预留检查
                            mini  - "普通内存：41 + 动态计算 +[1 双活]  +[1 vHost] +[2 ARM] + [大页内存] "
                            normal -"53 + 动态计算 +[1 双活]  +[1 vHost] +[2 ARM] + [大页内存] "
                            large -  "63 + 动态计算 +[1 双活]  +[1 vHost] +[2 ARM] + [大页内存]"
                            vmware normal  -  "50 + [1 双活]  +min_free + [3 大页内存]"
                            smtxelf    13+动态计算
                        内存cgroup 限制
                            smtx.slice        37G/49G/59G  +[1 vhost] +[1 双活] + [2 ARM]
                                smtx-elf.slice           3G
                                smtx-tuna.slice           4G
                                smtx-network.slice           2G
                                smtx-lcm.slice           5G
                                smtx-infra.slice           6G
                                    smtx-infra-mongod.slice              2G
                                    smtx-infra-zk.slice              1G
                                    smtx-infra-jc.slice              1G
                                    smtx-infra-common.slice              2G
                                smtx-zbs.slice           27G/39G/49G  +[1 vhost] +[1 双活] + [2 ARM]
                                    smtx-zbs-metamain.slice              6G
                                    smtx-zbs-chunkd.slice              18G/30G/40G  +[1 vhost] +[1 双活] + [2 ARM]
                                    smtx-zbs-others.slice              3G
                                smtx-obs.slice           2G
                                    smtx-obs-prometheus.slice              1G
                    cpuset 检查
                        zbs/chunk-main  1
                        zbs/chunk-io  1
                        zbs/others  1
                        zbs/lsm-db  1
                        zbs/meta-main*
                            普通容量规格：           zbs/meta-main 组 CPU 数量为 1
                            大容量规格 zbs/meta-main 组 CPU 数量为 2，SMTXOS 占用总计 +1； (SMTXOS 6.2.0)
                        zbs/app*
                            飞腾
                            非飞腾
                        zbs/lsm-io
                            开启vhost  2
                            未开启vhost  无
                        zbs/chunk-dcc (rdma)
                            开启RDMA  2 （独立线程改动）
                            vmware 环境 1
                            未开启RDMA 无
                        zbs/aurora (vhost)
                            开启vhost  1
                            未开启vhost  无
                        zbs/chunk-cprs (仅双活)
                            开启双活 1
                            未开启双活 无
                        zbs/network (仅SMTXOS.ELF, SMTXELF)
                            开启独立核心 2
                            未开启独立核心 无
                    资源指标回归
                        资源指标回归
                            cpu_cpuset_state_percent （TUNA-2649）
                        扩展指标确认（后台命令行打开规则项）
                            物理集群开启扩展服务和资源告警 - 无异常告警信息产生
                            检查告警规则 - 手动触发告警规则
                                cpuset cgroup  /zbs/app 期望的 cpus 限制为，实际为
                                服务 xx 期望的 CGroupPath
                                    服务 ovs-vswitchd.service 期望的CGroupPath 为，实际为
                                    服务 ovsdb-server.service 期望的CGroupPath 为，实际为
                    运维场景回归
                        开启vhost、关闭vhost
                        开启rdma、关闭rdma
                        角色转换
                            storage-> master
                            master->storage
                iSCSI独立线程
                    功能验证&回归
                        未开启独立线程-略，同上cgroup 常规回归内容
                        性能测试- ZBS & ELF测试
                        开启独立线程
                            enable-force-chunk-dc-thread
                                集群已经开启了RDMA，可以执行，不会调整cgroup、会增加配置文件
                                集群所有节点配置文件
                                    /etc/zbs/chunk_dc_threads_force_enable  为true
                                    /etc/zbs/chunk_dc_threads_force_enable 默认没有该文件
                                    /etc/sysconfig/zbs-chunkd 配置文件
                                        使用配置项 CHUNK_RUN_DCC_IN_NEW_THREAD 和 CHUNK_RUN_DCS_IN_NEW_THREAD
                                        vmware 环境 CHUNK_RUN_DCC_IN_NEW_THREAD
                                cgroup
                                    增加 os elf zbs/chunk-dcc 1 核心 &zbs/chunk-dc 是 1 核心  /vmware zbs/chunk-dcc 1 核心
                                    检查核心数不足的时候不能和其他核心polling 共用物理核心，开启会失败
                                    不能放在 cpu 0上
                                    检查对应的线程在 chunk-dcc 和chunk-dcs中，需要重启chunk ，需要记录文档
                            enable-force-chunk-iscsi-thread
                                vmware 环境开启不支持，不需要测试
                                配置文件
                                    /etc/zbs/chunk_iscsi_threads_force_enable 为true
                                    /etc/zbs/chunk_iscsi_threads_force_enable 默认没有该文件
                                    /etc/sysconfig/zbs-chunkd 中 ISCSI_USE_THREAD=true
                                cgroup
                                    zbs/iscsi 分组开启，占用1个核心
                                    检查对应的线程在 iscsi 中，需要重启chunk
                                    核心数不够的时候开启失败，不能放在cpu 0上，不能和其他共享物理核心
                            enable-force-chunk-lsmio-thread
                                开启vhost 环境，允许执行，关闭vhost 不会影响现成开启状态
                                vmware 环境开启- 不需要测试
                                配置文件
                                    /etc/zbs/enable_lsm_io_thread 为true
                                    /etc/zbs/enable_lsm_io_thread  默认就有
                                    /etc/sysconfig/zbs-chunkd 中 LSM_IO_THREAD_NUM=2
                                cgroup
                                    zbs/lsm-io 开启，分配两个核心
                                    CPU不够时可能会缩减为1或0
                                    可以放到cpu 0 上
                                    检查对应的线程在  zbs/lsm-io 中，需要重启chunk
                            iscsi_boost_enabled
                                配置文件
                                    不支持开启增强模式之后能单独关闭某个独立线程，这个开启之后上面几个配置文件不生效
                                    配置文件
                                        /etc/zbs/iscsi_boost_enabled 内容为true
                                        集群部署开启vhost 和rdma ，默认也没有该配置文件；开启之后增加配置文件，设置true
                                        enable 之后，其他三个配置文件不变，原来没有就没有，有的是什么value 就是什么
                                        检查 /etc/sysconfig/zbs-chunkd 中 ISCSI_USE_THREAD=true/fasle 选项，DATA_CHANNEL_THREAD_NUM 选项，LSM_IO_THREAD_NUM 选项
                                    cgroup
                                        配置同开启RDMA和vhost 新部署的环境
                                        需要重启chunk，对应线程才能运行在对应的组下面
                            扩容节点增强模式或者独立线程需要根据控制节点配置保持一致
                                enable-force-chunk-iscsi-thread
                                    false
                                    true
                                iscsi_boost_enabled
                                    false
                                    true
                            开启之后回归
                                运维回归 穿插在上面借个不同开启配置的集群里验证
                                    缩容
                                    开启之后，内存预留不变
                                    重启主机之后配置不变
                                    同版本升级配置不变
                                    不支持升级630
                                    zbs-deploy cgroup config 执行之后cpuset 不变
                                    vhost 开启、关闭，预期不影响几个独立线程的配置文件，cgroup 配置 按照配置项和 vhost两者
                                    RDMA开启、关闭， 预期不影响几个独立线程的配置文件，cgroup 配置 按照配置项和 vhost两者
                                    角色转换
                                        storage-> master
                                        master->storage
                                开启之后指标采集告警提示预期符合新的cgroup配置
                                    cpu_cpuset_state_percent （TUNA-2649）
                                    检查告警规则 - 手动触发告警规则
                                        cpuset cgroup  /zbs/chunk-dcc 期望的 cpus 限制为，实际为
                                        分组预期存在，实际不存在
                        关闭独立线程-优先级低选1-2个看下
                            手动逐个节点关闭，并重新执行zbs-deploy-mange config_cgroup
                            检查关闭之后的cpuset 符合预期
                            register service  & 重启svcresctl  服务
                        命令行验证
                            zbs-cluster chunk_cgroups --enable-iscsi-boost
                            zbs-cluster chunk_cgroups --enable-force-chunk-dc-thread
                            zbs-cluster chunk_cgroups --enable-force-chunk-iscsi-thread
                            zbs-cluster chunk_cgroups --enable-force-chunk-lsmio-thread
                            help
                            打印符合预期
                            传递非预期的参数提示
                        场景测试（穿插开启不同线程或者开启ISCSI 增强模式）
                            升级前注入某个配置 升级之后保留开启状态 https://docs.google.com/document/d/1P6oncQO88WiFZN01lC2i5JwkRmnwnrX_lBnpJGFL4fU/edit?tab=t.0
                            已经开启个别独立线程之后再开启增强模式，预期成功，配置文件增 iscsi boost，chunk 配置文件符合开启配置 &cgroup 配置符合开启预期
                            515 P2->621  开启独立线程
                            开启独立线程之后再关闭
                            开启独立线程之后再开启网络独立核心预期成功
                            6.4.0 单独测试，6.2.1 开启独立线程之后再升级到6.4.0 也是单独测试； 6.2.1 升级到6.3.0 不支持不需要测试
                        平台路径 - 穿插开启不同的线程或者增强模式
                            vmware 环境
                                zbs/app: master 3 核心 ; storage 2 核心
                                vmware 执行命令行生效，增加一个 zbs/chunk-dcN ， 不会增加 iscsi 和 lsm io？
                                vmware 支持开启的话，看下scvm 资源不够的情况
                                关闭独立线程
                            hygon  环境
                                命令行
                                开启独立线程
                                关闭独立线程
                            arm 2实例 鲲鹏
                                命令行
                                开启独立线程
                            arm  飞腾
                                命令行
                                开启独立线程
                                关闭独立线程
                            双活环境
                                仲裁节点不处理，命令行看下& 配置文件检查下
                                在仲裁节点上执行，预期不会做配置
                                其他节点同上面检查点
                                关闭独立线程
                            smtxelf 环境
                                smtxelf 执行命令行预期不生效，有提示？
                            arcfra 环境
                                命令行
                                开启独立线程
                                关闭独立线程
                            tencent os
                                命令行
                                开启独立线程
                                关闭独立线程
    集群设置管理
        630支持 sshd 端口修改
            版本平台
                tower
                    ui install arm 480
                    vm install x86-oe 480
                    443 升级到 480 后
                        做修改集群 ssh 服务端口号成功
                        主机 ssh 端口不一致告警
                            告警规则正确
                            告警触发成功
                            告警解决成功
                            告警接收成功
                cluster(和系统无关，不区分 tl3、elf、oe)
                    smtx os(elf) 630 单活
                    smtx os(elf) 630 双活
                    smtx os(vmware)630
                    smtx elf 630
                    smtx zbs 集群设置页面有「安全-服务端口」入口，但是 ssh 服务对应的 more btn 下只有“编辑 IP 白名单”按钮，没有“编辑端口号”按钮，以及低版本集群如 smtx os 620、smtx elf 620 也没有该按钮
                    集群升级
                        smtxos (elf)  515 单活修改过集群主机端口为非 22 端口-10023，集群升级到 630，升级失败,修改为 22 后重新触发升级成功，然后再修改回 10023，修改成功
                        smtxos (elf) 515 单活集群端口号均为22，升级到 630 后编辑主机端口号成功
                        smtxos (elf) 515 hp 双活集群端口号均为 22，升级到 630 后编辑主机端口号成功
                        smtxos (vmware) 507p2单活集群端口号均为 22，升级到 630 后编辑主机端口号成功
                        smtx elf 620 单活集群端口号均为 22，升级到 630 后编辑主机端口号成功
            UI
                集群设置页面新增「安全-服务端口」入口
                “访问控制”板块主文案为：“启用访问限制，可配置各节点的 snmp 和 ssh 服务的访问规则。”
                仅 VMware 集群常驻显示 tip 提示：“此处仅管理 SCVM 的服务端口。请确保 ESXi 主机的 ssh 服务正常使用 22 端口。”
                “服务端口”列表
                    「端口号」列：默认宽度改为 104px
                    删除「可配置」列
                    “ssh 服务” 对应字段校验
                        端口号：默认展示当前值
                        协议：TCP
                        描述：用于 SSH 远程登录集群主机或 SCVM。
                        IP 白名单：默认展示”全部允许“
                        more btn - 编辑端口号：点击，打开”编辑 ssh 服务的端口号“弹窗
                        more btn - 编辑 IP 白名单：点击，打开”编辑 ssh 服务的 IP 白名单“弹窗
                各主机的 ssh 端口号不一致
                    ssh 服务的”端口号“列展示红色 ”各节点不一致“ tag
                    “服务端口” section 上方展示红色 tip 提示“....”
                        x 个主机：10022；y 个主机：22；
                        点击「编辑 ssh 端口号」按钮，打开”编辑 ssh 服务的端口号“弹窗
                        smtx zbs 集群主机 ssh 端口不一致时没有该 tip 提示，也没有不一致的 tag
                禁用情况
                    未启用「访问控制」
                        禁用所有服务的「编辑 IP 白名单」btn
                        hover info icon 显示 tooltip 提示”集群未启用访问限制。“
                    集群存在正在执行中的”采集日志“任务
                        禁用 ssh 服务的「编辑端口号」btn
                        hover info icon 显示 tooltip 提示”集群正在采集日志......“
                    集群正在升级
                        tip 提示”正在升级集群……暂时无法编辑访问控制和服务。“
                        禁用所有服务的「编辑 IP 白名单」btn，不显示 info icon
                        禁用 ssh 服务的「编辑端口号」btn，不显示 info icon
                    集群存在执行中的”添加主机“任务
                        tip 提示”集群正在添加主机……暂时无法编辑访问控制和服务端口号。“
                        禁用「访问控制」section 的「编辑」btn
                        禁用 ssh 服务的「编辑端口号」btn，不显示 info icon
                    集群存在异常主机
                        关机中
                            tip 提示”集群中存在 N 个异常主机，无法编辑访问控制和服务端口号。“
                            hover 「N 个异常主机」tooltip 提示：主机&对应状态
                            主机名过长时，tooltip 中主机名称打点省略
                            禁用「访问控制」section 的「编辑」btn
                            禁用 ssh 服务的「编辑端口号」btn，不显示 info icon
                        重启中
                            tip 提示”集群中存在 N 个异常主机，无法编辑访问控制和服务端口号。“
                            hover 「N 个异常主机」tooltip 提示：主机&对应状态
                            禁用「访问控制」section 的「编辑」btn
                            禁用 ssh 服务的「编辑端口号」btn，不显示 info icon
                        异常状态
                            tip 提示”集群中存在 N 个异常主机，无法编辑访问控制和服务端口号。“
                            hover 「N 个异常主机」tooltip 提示：主机&对应状态
                            禁用「访问控制」section 的「编辑」btn
                            禁用 ssh 服务的「编辑端口号」btn，不显示 info icon
                        无响应状态
                            tip 提示”集群中存在 N 个异常主机，无法编辑访问控制和服务端口号。“
                            hover 「N 个异常主机」tooltip 提示：主机&对应状态
                            禁用「访问控制」section 的「编辑」btn
                            禁用 ssh 服务的「编辑端口号」btn，不显示 info icon
                    集群连接异常
                        该页面显示“集群连接异常的空白状态”
                「编辑端口号」弹窗
                    仅 VMware 集群增加 description ”该操作仅针对 SCVM，不会变更 ESXi 主机的 ssh 服务端口号。“
                    正确展示当前集群名称、当前端口号
                    端口号输入框下方提示”建议配置在 10022-10099 之间。“
                    未做端口号修改时「保存」按钮 disable
                    端口号输入框校验
                        输入框类型为 number input，仅允许输入阿拉伯数字
                        为空时，blur+onchange、submit，inline 提示”请输入端口号“
                        端口号范围，blur+onchange、submit，inline 提示”仅支持 0-65535 之间的整数。“
                    端口号 onchange 且不为空
                        提示”我已知晓..“内容，且默认不勾选。「检查」、「保存」按钮 disable
                        勾选”我已知晓...“后「检查」按钮 enable，「保存」按钮 disable
                    前置检查
                        检查中
                            禁用：端口号 field、我已知晓 checkbox
                            「保存」按钮 disable
                            点击「取消」或「X」按钮，返回服务端口列表，且端口号修改不会下发
                            提示“正在检查是否可变更为新端口号......”"预计共花费约 10秒。"
                            检查项-3项 均为 loading 状态
                                新端口号未被其他服务使用
                                ssh 服务的配置正确
                                各%主机/SCVM%的管理网络之间、存储网络之间可通过新端口号连通
                        检查不通过
                            检查项：第一个不通过，只有第 三个检查项会跳过；第二个检查项不会被第一个检查项干扰。集群节点并行做上述三项检查
                            增加提示：无法将 ssh 服务变更为新端口号。请解决问题后，再尝试变更。
                            增加「重新检查」按钮：点击重新进入检查中状态
                            「保存」按钮 disable
                            点击「取消」或「X」按钮，返回服务端口列表，且端口号不会改变
                            端口号 field、我已知晓 checkbox 变为可编辑状态
                            重新编辑端口号：页面回到上述“端口号 onchange 且不为空”状态
                            取消勾选“我已知晓 checkbox”，「重新检查」按钮 disable
                            检查项
                                仅1 失败：1「未满足」tag；2「已满足」；3「跳过」
                                不可能有 1、2、3都失败，因为 1失败了，3会被跳过
                                仅2失败
                                    1「满足」tag；2「未满足」tag；3「满足」
                                    展示配置有误的主机名：以下%主机/SCVM%的 ssh 服务配置有误：host1、host2。请检查服务配置，并重启服务后，再尝试编辑端口号。
                                仅3失败
                                    1、2「满足」tag；3「未满足」tag
                                    以下%主机/SCVM%的网络之间无法通过新端口号连通：hostname-1 与 hostname-2 的管理网络；hostname-2 与 hostname-3 的存储网络；hostname-1 与 hostname-3 的管理网络、存储网络
                                1、2 都失败
                                    检查一下提示
                                2、3 都失败
                                    1「满足」tag；2、3 提示检查
                        检查通过
                            三项均展示「已满足」tag
                            增加提示“ssh 服务可变更为新端口号。确认变更吗？”
                            再次修改端口号
                                页面回到上述“端口号 onchange 且不为空”状态
                            不再修改端口
                                取消勾选“我已知晓 checkbox”，「保存」按钮 disable
                                点击「保存」，各主机开始下发新端口号配置
                                点击「取消」或「X」，返回服务端口列表，且端口号修改不会下发
                task
                    编辑中
                        loading 按钮；xx 分钟前开始
                        “编辑集群 %cluster-name% 的 ssh 服务的端口号”
                    编辑成功
                        task 成功；耗时正确
                        “编辑集群 %cluster-name% 的 ssh 服务的端口号”
                    编辑失败
                        task 失败；耗时正确
                        “编辑集群 %cluster-name% 的 ssh 服务的端口号”
                        inline 错误提示“N 个节点编辑失败：hostname-1、hostname-2、hostname-3。Error Mes.”
                「编辑 ssh 服务的 IP 白名单」
                    文案更新为“编辑 %ssh% 服务的 IP 白名单 ”
                    文案更新为“编辑集群 #%cluster-name%# 的 %ssh% 服务的 IP 白名单。”
                「添加主机」弹窗
                    集群已有主机端口一致：10022；待添加节点端口为22，添加成功后，“执行部署” step 提示“集群内各主机的 ssh 服务端口号不一致。”
                    集群已有主机端口一致：10022；待添加节点端口为22，添加失败后，无 tip 提示
                    点击 tip 提示中的「编辑 ssh 端口号」btn，打开点击「编辑 ssh 端口号btn」，打开 [集群设置 > 服务端口] 页
                    在该页面将集群主机修改端口号一致后，重新打开添加主机详情弹窗，弹窗中不在展示该 tip 提示--实时查询
            功能测试
                修改端口号前置检查
                    成功
                        可以成功进入下一步任务提交操作
                    失败
                        修改为其他系统（多试几个）已占用端口，前置检查失败
                        /etc/ssh/sshd_config 文件不存在，SSH 服务的配置正确性检查（sshd -T）失败
                        /etc/ssh/sshd_config 有多余参数时，SSH 服务的配置正确性检查（sshd -T）失败（缺失已有参数时不影响
                        主机的管理网无法通过新端口号连通（nc -zv <peer_ip> 10023）
                        主机的存储网无法通过新端口号连通（nc -zv <peer_ip> 10023）
                        主机的管理网与存储网无法通过新端口号连通（nc -zv <peer_ip> 10023）
                        scvm 的管理网无法通过新端口号连通（nc -zv <peer_ip> 10023）
                        scvm 的存储网无法通过新端口号连通（nc -zv <peer_ip> 10023）
                        scvm 的管理网与存储网无法通过新端口号连通（nc -zv <peer_ip> 10023）
                        修改失败的检查点后，重新检查成功，可以成功进入下一步任务提交操作
                下发修改端口号配置
                    修改成功后
                        列表值显示对应更改
                        终端已有的主机 ssh 连接不会断开
                        在终端使用新的 ssh 端口号，可以成功访问主机
                        修改后 sshd -T 再次检查 SSH 服务的配置正确性
                        修改后进行集群漏扫
                        主机/scvm 的 管理网通过新端口号可以连通
                        主机/scvm 的 存储网通过新端口号可以连通
                        主机/scvm 的 管理网与存储网通过新端口号可以连通
                    修改失败
                        修改3台主机，其中2台下发失败，task 整体为失败，失败的两台主机仍为之前的端口号
                        下发失败后，各主机 ssh 服务端口号回滚为修改前的，且能用之前的端口号正常工作
                        下发失败原因
                            被修改端口号已被防火墙禁用（在前置检查中就可以监测出来？---在前置检查中失败
                            主机管理网不通，下发失败
                            主机存储网不通，下发失败
                            vip 所在节点 apiserver 停掉了，下发失败
                修改端口号后
                    smtx os(elf) 630 单活
                        修改全部主机端口号为 10022 后
                            集群部署失败：必须要求客户环境先临时开放 22 端口才能完成部署
                            磁盘故障日志采集
                            日志
                                采集
                                下载
                                解压查看
                            集群扩容
                                单节点：端口号为 22，扩容成功
                                单节点：端口号为 10023，扩容失败
                                多节点：端口号均为 22，扩容成功
                                多节点：端口号均为 22，扩容成功。根据引导进入集群设置页面，按要求编辑该集群的端口号一致，操作成功
                                多节点：端口号均为 10023，扩容失败
                                多节点：端口号部分 22、部分 10023，全部失败。将非 22 节点端口号修改为 22 后，重新添加，全部成功
                                单节点：端口号为 22，添加成功后，修改为 10023，然后移除该节点，重新添加失败，重新修改为 22 后，能再次添加成功
                                先添加一个节点，再添加一个节点
                            主机管理
                                主机重启
                                集群整体关机
                                进入维护模式
                                退出维护模式
                                移除主机
                                storage 转 master 成功
                                master 转 storage 成功
                                主机时间修改
                                修改节点管理 ip
                            升级中心
                                集群版本升级-hotfix packages（例如 630p1 .iso），成功
                                集群版本升级-普通 iso，成功
                                集群 kernel 升级成功
                                集群扩容根分区成功
                                集群安装补丁-hot patch，成功（630 临时构建 .run 文件
                                集群 vgpu 升级
                                121 支持非 22 端口集群的升级
                            双活转换
                                单活转双活成功，同步仲裁节点管理 IP 成功
                                仲裁节点重建
                            vhost
                                开启
                                关闭
                            RDMA
                                开启
                                关闭
                            集群上下线工具
                                上线
                                下线
                            巡检中心
                                集群巡检
                                报告导出
                                单集群报告检查
                                多集群报告检查
                                tower UI 巡检结果查看
                            cluster installer
                                部署该系统服务，成功
                                用该服务做集群部署操作，成功
                                用该服务做 集群扩容，成功
                            部署在该集群上的其他功能预期不受影响-(-低优先级
                                sks
                                ER
                                备份与容灾
                                SFS
                                V2V 迁移工具
                                cloudtower
                                    在该集群上部署 tower 系统 vm
                                    部署在该集群上的 tower 升级
                                    部署在该集群上的 tower HA 不受影响？走一下看看
                                    部署在该集群上的 tower 中的 alpha 插件 功能不受影响---和 xiaojun 确认一下是否用到了 ssh
                                        下述插件只覆盖：巡检工具，其余不覆盖
                                        导入 ER 安装包
                                        导入 ISO
                                        回收站后门
                                        快速反馈
                                        批量转换虚拟机为虚拟机模板
                                        嵌套集群
                                        升级中心
                                        通过标签批量分发模板到集群
                                        虚拟机详情增强
                                        巡检工具
                                        样式助手
                                        cloudtower application
                                        cloudtower metrics
                                        legacy fisheye
                        主机端口号不一致：部分 10022、部分 10023 后
                            日志
                                采集
                                下载
                                解压查看
                            升级中心
                                集群版本升级-hotfix packages，成功(630 暂无该 iso?
                                集群版本升级-普通 iso，成功
                                集群 kernel 升级成功
                                集群扩容根分区成功
                                集群安装补丁-hot patch，成功（630 暂无该 .run 文件
                                集群 vgpu 升级？
                            集群上下线工具
                                上线
                                下线
                            巡检中心
                                集群巡检
                                报告导出
                                单集群报告检查
                                多集群报告检查
                                tower UI 巡检结果查看
                            集群扩容
                                单节点：端口号为 22，扩容成功
                                多节点：端口号均为 22，扩容成功
                    smtx os(elf) 630 双活
                        修改全部主机端口号为 10022
                            日志
                                采集
                                下载
                                解压查看
                            升级中心
                                集群版本升级-hotfix packages（例如 630p1 .iso），成功
                                集群版本升级-普通 iso，成功
                                集群 kernel 升级成功
                                集群扩容根分区成功
                                集群安装补丁-hot patch，成功（630 临时构建 .run 文件
                                集群 vgpu 升级
                            主机管理
                                主机重启
                                集群整体关机
                                进入维护模式
                                退出维护模式
                                移除主机
                                storage 转 master 成功
                                master 转 storage 成功
                                主机时间修改
                                修改节点管理 ip
                            vhost
                                开启
                                关闭
                            可观测
                                已关联的集群，在主机修改端口号后，关联状态仍正常
                                OBS 关联该集群成功
                                对该集群进行本地数据迁移成功
                                OBS 告警接收成功
                                开启流量可视化成功
                                OBS 卸载成功
                            集群上下线工具
                                上线
                                下线
                            巡检中心
                                集群巡检
                                报告导出
                                单集群报告检查
                                多集群报告检查
                                tower UI 巡检结果查看
                            集群扩容
                                单节点：端口号为 22，扩容成功
                                多节点：端口号均为 22，扩容成功
                    smtx os(vmware)630
                        scvm 全部主机端口号改为 10022，esxi 仍为 22 后
                            部署 io reroute 成功
                            升级 io reroute 成功
                            scvm 和 esxi 的连接仍正常
                            日志
                                采集
                                下载
                                解压查看
                            cluster installer
                                部署 cluster installer 系统服务，成功
                                VMware 扩容
                            集群扩容
                                单节点：端口号为 22，扩容成功
                                多节点：端口号均为 22，扩容成功
                            升级中心
                                集群版本升级-hotfix packages，成功(630 暂无该 iso?
                                集群版本升级-普通 iso，成功
                                集群 kernel 升级成功
                                集群扩容根分区成功
                                集群安装补丁-hot patch，成功（630 暂无该 .run 文件
                                集群 vgpu 升级？
                            集群上下线工具
                                上线
                                下线
                            巡检中心
                                集群巡检
                                报告导出
                                单集群报告检查
                                多集群报告检查
                                tower UI 巡检结果查看
                            可观测
                                该集群与 OBS 服务的关联状态仍正常
                            高级监控
                                部署
                        scvm 全部主机端口号改为 10022，esxi 修改为非 22 后
                            部署 io reroute 成功
                            升级 io reroute 成功
                            scvm 和 esxi 的连接仍正常
                            日志采集、下载成功
                            集群扩容成功
                    smtx elf 630
                        修改全部主机端口号为 10022
                            集群扩容
                                单节点：端口号为 22，扩容成功
                                多节点：端口号均为 22，扩容成功
                            日志
                                采集
                                下载
                                解压查看
                            升级中心
                                集群版本升级-hotfix packages，成功(630 暂无该 iso?
                                集群版本升级-普通 iso，成功
                                集群 kernel 升级成功
                                集群扩容根分区成功
                                集群安装补丁-hot patch，成功（630 暂无该 .run 文件
                                集群 vgpu 升级？
                            集群上下线工具
                                上线
                                下线
                            巡检中心
                                集群巡检
                                报告导出
                                单集群报告检查
                                多集群报告检查
                                tower UI 巡检结果查看
                新增主机 ssh 端口不一致告警
                    告警规则
                        字段检查
                            启用状态：默认为启用
                            报警描述：检测到集群中存在 SSH 端口配置不一致的情况。
                            报警等级：默认为严重警告
                            报警对象：630+ smtx os(elf)、630+ smtx os(vmware)、630+ smtx elf（无 smtx zbs 集群）
                        编辑
                            编辑为禁用：满足该告警触发条件后，不会触发告警
                            重新编辑为启用：满足告警触发条件后，触发告警
                            编辑报警等级为“注意”，已触发告警自动解决，重新触发注意级别告警
                            编辑报警等级为“信息”，已触发告警自动解决，重新触发信息级别告警
                            创建特例规则：符合特例规则的报警对象在满足触发条件后，触发告警
                    告警
                        未关联 OBS 服务
                            告警触发：符合报警规则的对象触发报警
                            告警解决：不符合告警要求后，自动解决。解决时间显示正确
                            告警接收：邮件
                            告警字段检查
                                告警 title 正确：检测到集群中存在 SSH 端口配置不一致的情况。
                                触发原因：集群中共有 { .labels.total_hosts } 台主机，检测到 { .labels.unique_ports } 个不同的SSH端口配置。端口分布详情：{ .labels.port_mapping }。
                                影响：SSH 端口配置不一致将直接导致集群的日志收集、升级与巡检等运维操作失败，进而削弱集群管理的统一性与安全管控能力。
                                解决方法：检查各主机的 SSH 配置文件(/etc/ssh/sshd_config)，手动统一所有主机的 SSH 端口配置。配置文件更正之后，请在界面上重新编辑 SSH 端口并进行保存。
                                报警源：集群内部
                                报警等级：与报警规则一致
                                报警对象：集群名称
                                报警规则：显示正确 & 跳转正确
                                触发时间：与实际触发时间一致
                                持续时间：与实际持续时间一致
                        关联了 OBS 服务
                            告警触发：符合报警规则的对象触发报警
                            告警解决：不符合告警要求后，自动解决。解决时间显示正确
                            告警接收：webhook、邮件
                            字段检查
                                告警 title 正确：检测到集群中存在 SSH 端口配置不一致的情况。
                                触发原因：集群中共有 { .labels.total_hosts } 台主机，检测到 { .labels.unique_ports } 个不同的SSH端口配置。端口分布详情：{ .labels.port_mapping }。
                                影响：SSH 端口配置不一致将直接导致集群的日志收集、升级与巡检等运维操作失败，进而削弱集群管理的统一性与安全管控能力。
                                解决方法：检查各主机的 SSH 配置文件(/etc/ssh/sshd_config)，手动统一所有主机的 SSH 端口配置。配置文件更正之后，请在界面上重新编辑 SSH 端口并进行保存。
                                报警源：可观测性服务 xx
                                报警等级：与报警规则一致
                                报警对象：集群名称
                                报警规则：显示正确 & 跳转正确
                                触发时间：与实际触发时间一致
                                持续时间：与实际持续时间一致
            通用功能
                中英文
                事件审计
                    事件类型：编辑服务端口
                    描述：编辑集群 xxxx 的 ssh 服务的端口号，配置变化为：端口号：{{原配置}} --> {{新配置}}
                    触发时间
                    结束时间
                    状态
                        失败
                        成功
                权限
                    「运维管理和设置-单个集群内」增加“服务端口-编辑集群的 ssh 服务的端口号”
                    创建自定义角色分配该权限，可以成功做编辑集群 ssh 服务端口号操作
                    创建自定义角色不分配该权限，无编辑集群 ssh 服务端口号入口
                    运维管理员可以成功编辑
                    只读角色无该权限、无该操作入口
                    安全审计员无该权限、无该操作入口
                    用户管理员无该权限、无该操作入口
                    虚拟机使用者无该权限、无该操作入口
            场景测试
                smtx os(elf) 集群设置了虚拟机 ip，并以该 ip 与 tower 关联，编辑集群端口号操作成功
                smtx elf 集群设置了虚拟机 ip，并以该 ip 与 tower 关联，编辑集群端口号操作成功
                修改集群 ssh 服务端口号时，tower 发生 HA，修改成功
                node1、node2： 10022；node3： 10023，node4：22，编辑端口为 10023，node1、node2、node4 成功修改为 10023
                smtx elf 关联了 zbs 集群，当 elf 集群修改端口号后的一些运维操作
                    已有的关联存储仍正常关联
                    添加新的关联存储成功
                    编辑已有关联存储的存储策略成功
            ARCFRA
                版本平台
                    AOC：480
                    ACOS 630 单活
                    ACOS 630 双活
                    vmware 集群
                    没有 arcfra smtx elf
                UI
                    集群设置- 安全-端口访问控制列表
                    编辑 ssh 服务端口弹窗
                    tower task
                    tower 事件列表
                    tower 权限列表
                    tower 告警规则
                功能（低优先级
                    权限
                        创建该自定义权限的角色后，可以成功编辑 ssh 服务端口号
                    编辑 ssh 服务端口号
                        编辑
                        检查中
                        检查不通过
                        检查不通过后重新检查
                        检查通过
                        编辑成功
                    编辑 ssh 服务端口号后
                        添加主机
                        集群升级
                        集群日志采集
                        主机重启
                        角色转换
                        部署 OBS 服务成功
                        关联 OBS 服务后数据迁移成功
                    告警
                        告警触发
                        告警解决
                        告警接收
    系统运维管理
        日志采集
            5.1.5 日志采集增强
                node_info 分组下增加 disk_info
                node_info 分组下增加 sos report
                    smtx os 5.1.4- 版本集群不展示 UI 入口
                    单活 smtx os(elf) 515 x86-el7，开启 Boost 模式
                        集群层级采集
                        节点层级采集
                        下载
                        下载后内容检查
                    单活 smtx os(elf) 515 x86-oe，未开启 Boost 模式
                        集群层级采集
                        节点层级采集
                        下载
                        下载后内容检查：CPU、内存、hba 卡、网络
                    单活 smtx os(elf) 515 arm-oe
                        集群层级采集
                        节点层级采集
                        下载
                        下载后内容检查：CPU、内存、hba 卡、网络
                    单活 smtx os(elf) 515 hygon-oe
                        集群层级采集
                        节点层级采集
                        下载
                        下载后内容检查：CPU、内存、hba 卡、网络
                    双活  smtx os(elf) 515 x86-el7
                        集群层级采集
                        节点层级采集:仲裁、非仲裁节点均可采集到
                        下载
                        下载后内容检查：CPU、内存、hba 卡、网络
                    单活 smtx os(vmware) 515 x86-el7
                        集群层级采集
                        节点层级采集:仲裁、非仲裁节点均可采集到
                        下载
                        下载后内容检查：CPU、内存、hba 卡、网络
                    smtx zbs
                        不支持本次优化，UI 上不提供 node_info -> sos_report 入口
                    压力测试
                        制造2W + 日志文件，且采集日期选项包含在制造的日志文件中，查看是否采集成功且进度打印正常
                        集群 CPU 较高时，可以成功采集、下载日志，且日志内容成功采集了 sosreporter
                    命令行
                        采集集群日志
                        采集节点日志
                            按照发送的参数采集成功，且进度条正常
                                log-collector cluster collect
                增加 巡检 agent、巡检节点运行日志采集
                    巡检工具-turbot-server：记录当前节点调用巡检自身 api 的记录信息获取当前节点的数据
                    巡检中心-inspector-agent：巡检中心 server 找了一个节点去部署 inspector-agent 的日志，turbot-server：节点调用巡检自身 api 的记录信息获取当前节点的数据
                    tuna_logs 分组下增加 inspector 采集项
                        smtx os 5.1.5+ 版本集群有无使用巡检中心/巡检工具做过巡检，UI 上均有入口
                        5.1.5- 版本集群不展示 UI 入口
                        单活 smtx os(elf) 515 x86-oe
                            使用巡检工具对该集群进行巡检，采集日志，下载，查看日志内容
                            使用巡检中心对该集群进行巡检，采集日志，下载，查看日志内容
                            集群层级采集
                            节点层级采集
                        单活 smtx os(elf) 515 x86-el7
                            使用巡检中心对该集群进行巡检，采集日志，下载，查看日志内容
                            使用巡检工具对该集群进行巡检，采集日志，下载，查看日志内容
                            先试用巡检工具，后使用巡检中心对该集群进行巡检，采集日志，下载，查看日志内容
                            集群层级采集
                            节点层级采集
                        单活 smtx os(elf) 515 arm-el7
                            集群层级采集
                            节点层级采集
                            使用巡检中心对该集群进行巡检，采集日志，下载，查看日志内容
                            使用巡检工具对该集群进行巡检，采集日志，下载，查看日志内容
                        单活 smtx os(elf) 515 hygon-oe
                            集群层级采集
                            节点层级采集
                            使用巡检中心对该集群进行巡检，采集日志，下载，查看日志内容
                            使用巡检工具对该集群进行巡检，采集日志，下载，查看日志内容
                        双活  smtx os(elf) 515 x86-el7
                            集群层级采集
                            节点层级采集：仲裁节点可以采集，但是采集后不显示该文件夹（tuna_logs -- inspector）；非仲裁节点可以采集且文件内容正确
                            使用巡检中心对该集群进行巡检，采集日志，下载，查看日志内容
                            使用巡检工具对该集群进行巡检，采集日志，下载，查看日志内容
                        单活 smtx os(vmware) 515 x86-el7
                            集群层级采集
                            节点层级采集
                            使用巡检中心对该集群进行巡检，采集日志，下载，查看日志内容
                            使用巡检工具对该集群进行巡检，采集日志，下载，查看日志内容
                支持采集内存态数据和硬件固件版本（戴尔、联想一体机），网卡没有一体机的限制，只有存储控制器的需要一体机的限制
                    SMTX OS-515 VMware 集群
                        集群层级采集
                        节点层级采集
                        下载
                        下载后内容检查-网卡固件信息（查看文件路径： nodexx.tar.gz - node_info_xx - report_node_info_nodeip - 文档中搜索关键字 collect hardware info、VMware nic info）
                        下载后内容检查-存储控制器信息（查看文件路径： nodexx.tar.gz - node_info_xx - report_node_info_nodeip - 文档中搜索关键字 collect hardware info）
                    SMTX OS- 515 ELF 集群
                        集群层级采集
                        节点层级采集
                        下载
                        下载后内容检查-网卡固件信息（查看文件路径： nodexx.tar.gz - node_info_xx - sosreport-nodename-xx.tar.gz -整个 sosreport-xx 文件夹下的内容）
                        下载后内容检查-存储控制器信息（查看文件路径：nodexx.tar.gz - node_info_xx - 该目录下找到 report_node_info_节点管理 ip，搜索关键字” hardware info“）【一部分主机可以，要看是否兼容主机的存储控制器平台
                问题单回归
                    TUNA-6855
                    TUNA-6642
                    TUNA-6764
                    TUNA-6654
            zbs 570 日志采集增强
                node_info 分组下增加 sos report
                    zbs 562- 版本集群不支持本次优化，UI 上不提供 node_info -> sos_report 入口
                    单活  zbs570 x86-el7，开启 Boost 模式
                        集群层级采集
                        节点层级采集
                        下载
                        下载后内容检查
                    单活 zbs570 arm-oe，未开启 Boost 模式
                        集群层级采集
                        节点层级采集
                        下载
                        下载后内容检查：CPU、内存、hba 卡、网络
                    双活  zbs570 x86-el7
                        集群层级采集
                        节点层级采集:仲裁、非仲裁节点均可采集到
                        下载
                        下载后内容检查：CPU、内存、hba 卡、网络
                    压力测试
                        制造2W + 日志文件，且采集日期选项包含在制造的日志文件中，查看是否采集成功且进度打印正常
                        主机 CPU 较高时，可以成功采集、下载日志，且日志内容成功采集了 sosreporter
                    命令行
                        采集集群日志
                        采集节点日志
                            按照发送的参数采集成功，且进度条正常
                                log-collector cluster collect
                增加 巡检 agent、巡检节点运行日志采集
                    巡检工具-turbot-server：记录当前节点调用巡检自身 api 的记录信息获取当前节点的数据
                    巡检中心-inspector-agent：巡检中心 server 找了一个节点去部署 inspector-agent 的日志，turbot-server：节点调用巡检自身 api 的记录信息获取当前节点的数据
                    tuna_logs 分组下增加 inspector 采集项
                        zbs570+ 版本集群有无使用巡检中心/巡检工具做过巡检，UI 上均有入口
                        zbs562- 版本集群不展示 UI 入口
                        单活 zbs570 x86-el7
                            使用巡检中心对该集群进行巡检，采集日志，下载，查看日志内容
                            使用巡检工具对该集群进行巡检，采集日志，下载，查看日志内容
                            先试用巡检工具，后使用巡检中心对该集群进行巡检，采集日志，下载，查看日志内容
                            集群层级采集
                            节点层级采集
                        单活 zbs570 arm-oe
                            集群层级采集
                            节点层级采集
                            使用巡检中心对该集群进行巡检，采集日志，下载，查看日志内容
                            使用巡检工具对该集群进行巡检，采集日志，下载，查看日志内容
                        双活  zbs570 x86-el7
                            集群层级采集
                            节点层级采集：仲裁节点可以采集，但是采集后不显示该文件夹（tuna_logs -- inspector）；非仲裁节点可以采集且文件内容正确
                            使用巡检中心对该集群进行巡检，采集日志，下载，查看日志内容
                            使用巡检工具对该集群进行巡检，采集日志，下载，查看日志内容
        运维命令行
            630 时区修改
                smtxos/acos
                    正常执行 cmd
                        zbs-cluster get_available_timezones # 获取当前环境所支持的时区列表信息
                            主节点执行
                            存储节点执行
                        zbs-cluster get_available_timezones --zone_filter Asia # 支持查询区域中所支持的时区列表信息
                            主节点执行
                            存储节点执行
                        zbs-cluster get_available_timezones --zone_filter Shanghai  # 查询获取具体地点的时区是否支持
                            主节点执行
                            存储节点执行
                        zbs-cluster show_timezone   # 展示当前集群中所有节点设置的时区信息
                            主节点执行
                            存储节点执行
                        zbs-cluster set_timezone --timezone Asia/Shanghai # 设置集群所有节点的具体时区
                            执行一次后所有节点检查当前时区
                            需要从界面顺序重启所有节点才完成设置，在重启后再次在所有节点检查当前时区
                        设置完时区后需要检查服务状态和功能
                            ntp server
                                检查所有节点服务状态是否正常
                                更新 ntp 检查是否正常
                            mongo
                                检查所有节点服务状态是否正常
                                创建虚拟机
                            elf-exporter
                                检查所有节点服务状态是否正常
                                检查虚拟机监控信息
                            elf-rest-server
                                检查所有节点服务状态是否正常
                                创建虚拟机
                            elf-vm-watchdog
                                检查所有节点服务状态是否正常
                            net-health-check
                                检查所有节点服务状态是否正常
                                curl 127.0.0.1:12889/debug 有返回即可
                            ovs-coverage
                                检查所有节点服务状态是否正常
                            vm-security-controller
                                检查所有节点服务状态是否正常
                                    vsc-cli ping 测试
                            elf-vm-scheduler
                                检查 master 节点服务状态是否正常，storage 节点服务是否未启动
                                创建虚拟机使用自动调度
                            elf-dhcp
                                检查 master 节点服务状态是否正常，storage 节点服务是否未启动
                                创建有 os 的虚拟机，检查是否可以通过 dhcp 获取到 ip 地址
                            vmtools-agent
                                检查所有节点服务状态是否正常
                            tuna-rest-server
                                检查所有节点服务状态是否正常
                                创建虚拟机
                            crab
                                检查所有节点服务状态是否正常
                                创建虚拟机
                            tuna-exporter
                                检查所有节点服务状态是否正常
                                检查节点磁盘监控信息
                            svcresctld
                                检查所有节点服务状态是否正常
                            network-monitor
                                检查所有节点服务状态是否正常
                                检查节点网络监控信息
                            aquarium
                                检查所有节点服务状态是否正常
                            fluent-bit
                                检查所有节点服务状态是否正常
                                检查事件审计内容
                            job-center-worker
                                检查所有节点服务状态是否正常
                                创建虚拟机
                            zbs-rest-server
                                检查所有节点服务状态是否正常
                                创建虚拟机
                            siren
                                检查非仲裁节点服务状态是否正常，仲裁节点服务是否未启动
                                制造告警并解决
                            octopus
                                检查非仲裁节点服务状态是否正常，仲裁节点服务是否未启动
                                制造告警
                            disk-healthd
                                检查非仲裁节点服务状态是否正常，仲裁节点服务是否未启动
                                挂载磁盘
                            timemachine
                                检查非仲裁节点服务状态是否正常，仲裁节点服务是否未启动
                                配置虚拟机定时快照
                            dnsmasq
                                检查非仲裁节点服务状态是否正常，仲裁节点服务是否未启动
                            vipservice
                                检查非仲裁节点服务状态是否正常，仲裁节点服务是否未启动
                                vipservice-tool show
                            network-firewall
                                检查非仲裁节点服务状态是否正常，仲裁节点服务是否未启动
                                network-firewall cli 有返回
                            dolphin
                                检查非仲裁节点服务状态是否正常，仲裁节点服务是否未启动
                                部署高级监控
                            job-center-scheduler
                                检查 master 节点服务状态是否正常，storage 节点服务是否未启动
                                创建虚拟机
                            seal
                                检查 master 节点服务状态是否正常，storage 节点服务是否未启动
                            master-monitor
                                检查非仲裁节点服务状态是否未启动，仲裁节点服务是否正常
                            cluster-upgrader
                                检查所有节点服务状态是否正常
                                集群升级
                    场景组合
                        节点 a 设置时区后，不重启，节点 A 再次设置另一个时区
                        节点 a 设置时区后，不重启，节点 B 设置另一个时区
                        节点 a 设置时区后，重启，节点 a 设置另一个时区
                        集群设置好时区后，扩容集群，扩容完成后被扩容的节点时区预期和集群设置好的时区一致
                        集群设置好时区后，升级到更高的版本，时区不会回退
                        集群设置时区时异常情况导致不同节点间时区不一致，在异常节点恢复后重新设置时区，集群预期正常工作无新增告警
                        修改好时区后，关联可观测
                        修改好时区后，巡检中心巡检
                smtxelf
                    正常执行 cmd
                        zbs-cluster get_available_timezones # 获取当前环境所支持的时区列表信息
                            主节点执行
                            非主节点执行
                        zbs-cluster get_available_timezones --zone_filter Asia # 支持查询区域中所支持的时区列表信息
                            主节点执行
                            非主节点执行
                        zbs-cluster get_available_timezones --zone_filter Shanghai # 查询获取具体地点的时区是否支持
                            主节点执行
                            非主节点执行
                        zbs-cluster show_timezone   # 展示当前集群中所有节点设置的时区信息
                            主节点执行
                            非主节点执行
                        zbs-cluster set_timezone --timezone Asia/Shanghai # 设置集群所有节点的具体时区
                            执行一次后所有节点检查当前时区
                            需要从界面顺序重启所有节点才完成设置，在重启后再次在所有节点检查当前时区
                        设置完时区后需要检查服务状态和功能
                            ntp server
                                检查所有节点服务状态是否正常
                                更新 ntp 检查是否正常
                            mongo
                                检查所有节点服务状态是否正常
                                创建虚拟机
                            elf-exporter
                                检查所有节点服务状态是否正常
                                检查虚拟机监控信息
                            elf-rest-server
                                检查所有节点服务状态是否正常
                                创建虚拟机
                            elf-vm-watchdog
                                检查所有节点服务状态是否正常
                            net-health-check
                                检查所有节点服务状态是否正常
                                curl 127.0.0.1:12889/debug 有返回即可
                            ovs-coverage
                                检查所有节点服务状态是否正常
                            vm-security-controller
                                检查所有节点服务状态是否正常
                                    vsc-cli ping 测试
                            elf-vm-scheduler
                                检查 master 节点服务状态是否正常，storage 节点服务是否未启动
                                创建虚拟机使用自动调度
                            elf-dhcp
                                检查 master 节点服务状态是否正常，storage 节点服务是否未启动
                                创建有 os 的虚拟机，检查是否可以通过 dhcp 获取到 ip 地址
                            vmtools-agent
                                检查所有节点服务状态是否正常
                            tuna-rest-server
                                检查所有节点服务状态是否正常
                                创建虚拟机
                            crab
                                检查所有节点服务状态是否正常
                                创建虚拟机
                            tuna-exporter
                                检查所有节点服务状态是否正常
                                检查节点磁盘监控信息
                            svcresctld
                                检查所有节点服务状态是否正常
                            network-monitor
                                检查所有节点服务状态是否正常
                                检查节点网络监控信息
                            aquarium
                                检查所有节点服务状态是否正常
                            fluent-bit
                                检查所有节点服务状态是否正常
                                检查事件审计内容
                            job-center-worker
                                检查所有节点服务状态是否正常
                                创建虚拟机
                            zbs-rest-server
                                检查所有节点服务状态是否正常
                                创建虚拟机
                            siren
                                检查所有节点服务状态是否正常
                                制造告警并解决
                            octopus
                                检查所有节点服务状态是否正常
                                制造告警
                            disk-healthd
                                检查所有节点服务状态是否正常
                                挂载磁盘
                            timemachine
                                检查所有节点服务状态是否正常
                                配置虚拟机定时快照
                            dnsmasq
                                检查所有节点服务状态是否正常
                            vipservice
                                检查所有节点服务状态是否正常
                                vipservice-tool show
                            network-firewall
                                检查所有节点服务状态是否正常
                                network-firewall cli 有返回
                            dolphin
                                检查所有节点服务状态是否正常
                                部署高级监控
                            job-center-scheduler
                                检查 master 节点服务状态是否正常，storage 节点服务是否未启动
                                创建虚拟机
                            seal
                                检查 master 节点服务状态是否正常，storage 节点服务是否未启动
                            cluster-upgrader
                                检查所有节点服务状态是否正常
                                集群升级
                    场景组合
                        节点 a 设置时区后，不重启，节点 A 再次设置另一个时区
                        节点 a 设置时区后，不重启，节点 B 设置另一个时区
                        节点 a 设置时区后，不重启，节点 a 设置另一个时区
                        集群设置好时区后，扩容集群，扩容完成后被扩容的节点时区预期和集群设置好的时区一致
                        集群设置好时区后，升级到更高的版本，时区不会回退
                        集群设置时区时异常情况导致不同节点间时区不一致，在异常节点恢复后重新设置时区，集群预期正常工作无新增告警
                        修改好时区后，关联可观测
                        修改好时区后，巡检中心巡检
        630 RDMA开关
            流量控制 - zhaoguo测试
            bonding & 其他vhost 等特性组合 - zhaoguo测试
            虚拟机fio影响 - zhaoguo测试
            UI （中英文）
                英文
                入口
                    系统网络列表
                        630 os elf  存储网络未开启RDMA， ... （more）提供 【启用RDMA】btn
                        点击【启用RDMA】，打开启用确认弹窗
                        630 os elf  存储网络开启RDMA， ... （more）提供 【关闭RDMA】btn
                        点击【关闭RDMA】，关闭确认弹窗
                        630 os elf  管理&接入网络， ... （more）都不提供 【启用RDMA】btn
                        630 OS ELF 双活不提供btn
                        低版本双活都不提供btn
                        620 hp4 os elf 存储网络未开启RDMA ，... （more）不提供 【启用RDMA】btn
                        51X  os elf集群未开启RDMA ，... （more）不提供 【启用RDMA】btn
                        630 smtxelf 存储网络未开启RDMA， ... （more）不提供 【启用RDMA】btn
                        630 vmware 存储网络未开启RDMA， ... （more）不提供 【启用RDMA】btn
                        630 vmware 存储网络开启RDMA， ... （more）不提供 【关闭RDMA】btn
                        开启失败的话，这里仍显示【启用RDMA】 btn---这里重点看下关联节点开启成功，其他失败的场景
                        关闭失败的话，这里仍显示【关闭RDMA】 btn ---这里重点看下关联节点开启成功，其他失败的场景
                        启用过程中，btn 显示【启用 RDMA 中...】 并禁用
                        关闭过程中，btn 显示【关闭 RDMA 中...】 并禁用
                        启用和关闭的小图标是一样的
                    存储网络详情面板
                        630 os elf  存储网络未开启RDMA, 显示 【启用RDMA】btn
                        点击【启用RDMA】，打开启用确认弹窗
                        630 os elf  存储网络开启RDMA，显示 【关闭RDMA】btn
                        点击【关闭RDMA】，打开启用确认弹窗
                        630 os elf  管理&接入网络， 不提供 【启用RDMA】btn
                        630 以及低版本双活都不提供btn
                        620 hp4 os elf 存储网络未开启RDMA ，不提供 【启用RDMA】btn
                        51X  os elf集群未开启RDMA ，不提供 【启用RDMA】btn
                        630 smtxelf 存储网络未开启RDMA，不提供 【启用RDMA】btn
                        630 vmware 存储网络未开启RDMA，不提供 【启用RDMA】btn
                        630 vmware 存储网络开启RDMA，不提供 【关闭RDMA】btn
                        从上面系统网路列表中点击开启或者关闭，存储详情面板也展示对应的进度或者失败状态
                        关闭成功没有Tip 提示
                        开启失败
                            开启失败的话，这里仍显示【启用RDMA】 btn & 可点状态
                            按钮上面有红色Tip进度
                            右侧提供【查看结果】超链接，点开展示结果弹窗
                            点击「Remove btn」，移除 Tip，不再展示（再次启用/关闭失败时，才需要展示）
                        关闭失败
                            关闭失败的话，这里仍显示【关闭RDMA】 btn & 可点状态
                            按钮上面有红色Tip进度展示
                            右侧提供【查看结果】超链接 & 点击打开结果弹窗
                            点击「Remove btn」，移除 Tip，不再展示（再次启用/关闭失败时，才需要展示）
                        开启中
                            启用过程中，btn禁用
                            按钮上面有蓝色Tip进度展示：【正在启用RDMA......】
                            右侧提供【查看进度】超链接，点开展示进度弹窗
                        关闭中
                            关闭过程中，btn禁用
                            按钮上面有Tip进度展示：【正在关闭RDMA......】
                            右侧提供【查看进度】超链接&展示进度弹窗
                        启用成功
                            集群最新一条「启用 RDMA」任务是成功的，任务完成时，显示上图蓝色 Tip
                            Tip 文案：已启用 RDMA，请尽快在业务空闲期间为 RDMA 功能配置流量控制。否则，集群存在大的 I/O 带宽时，可能出现 RDMA 丢包断连而产生数据恢复。
                            集群任务被最新RDMA 刷新，这里Tip 还展示吗
                            点击「Remove btn」，移除 Tip，不再展示（再次启用成功时，才需要展示）
                启用RDMA弹窗
                    不可启用
                        Header：无法启用存储网络 RDMA
                        文案：无法启用集群 #%cluster-name%# 的存储网络 storage-network 的 RDMA。
                        具体原因检查点，随下面功能测试-skip
                        【关闭】按钮，弹窗关闭，回到入口页面
                        无法启用
                            有什么无法开启的原因提示什么，满足的条件不展示
                            集群正在升级……
                            所属虚拟分布式交换机关联了其他系统网络。
                            所属虚拟分布式交换机的网口绑定模式不是 OVS bonding 的 active-backup 或 balance-tcp 模式。
                            该网络已启用 QoS。
                            该网络的 VLAN ID 不是 0。
                            CPU 架构不满足
                                文案：集群中存在 N 个主机的 CPU 不是 Intel x86_64、AMD x86_64、Hygon x86_64 或鲲鹏 AArch64。
                                列出对应不满足的主机名称
                            主机不是健康状态
                                文案：集群中存在 N 个主机不是健康状态。
                                列出不满足的主机名称
                            所属虚拟机分布式交换机关联了Everoute 服务的一下功能
                                er service name： 分布式防火墙、网络安全导流
                                er service name：分布式防火墙
                                er service name：网络安全导流
                            存在网口不支持RDMA
                                文案：存在 N 个关联物理网口不支持 RDMA。
                                列出对应主机名称以及对应的不满足的网口
                                以上三项主机名称过长的时候，主机名称完整展示
                    预检查没问题显示可启用弹窗
                        Header：启用存储网络RDMA
                        文案：确认启用集群 #%cluster-name%# 的存储网络 storage-network 的 RDMA？
                        建议Tip：建议在业务空闲期间启用 RDMA。启用后，请尽快在业务空闲期间为 RDMA 功能配置流量控制；否则，集群存在大的 I/O 带宽时，可能出现 RDMA 丢包断连而产生数据恢复。
                关闭RDMA弹窗
                    可关闭
                        Header：关闭存储网络RDMA
                        文案：确认关闭集群 #%cluster-name%# 的存储网络 storage-network 的 RDMA？
                        描述（灰字）：关闭后，可按需删除 RDMA 功能的流量控制配置。保留配置不影响存储服务的正常运行。
                        关闭按钮展示【关闭RDMA】
                        点击提交 [关闭 RDMA 任务]， 不自动打开任务详情弹窗
                        取消，关闭弹窗，不进行关闭任务
                        点击「关闭RDMA」，弹窗消失
                    无法关闭
                        Header：无法关闭存储网络 RDMA
                        文案：无法关闭集群 #%cluster-name%# 的存储网络 storage-network 的 RDMA。
                        描述（灰字）：所属虚拟分布式交换机的网口绑定模式不是 OVS bonding。
                        【关机】按钮，弹窗关闭，回到入口页面
                        这里的关闭-只关闭窗口
                        其他原因不考虑
                启用任务进度
                    任务列表
                        文案：启用集群 %cluster-name% 存储网络的 RDMA
                        时间展示
                        启用失败，下面展示红色文案：启用 RDMA 失败。
                        启用成功，下面展示灰色提示：已成功启用 RDMA，请尽快在业务空闲期间为 RDMA 功能配置流量控制。否则，集群存在大的 I/O 带宽时，可能出现 RDMA 丢包断连而产生数据恢复。
                        右侧【...】可点击查看详情
                    任务执行中详情
                        Header：存储网络启用RDMA
                        文案 启用集群 #%cluster-name%# 存储网络 storage-network 的 RDMA。
                        文案这里集群名称过长看下
                        显示蓝色Tip条件：集群内正在进行数据恢复
                        以上两个主机名称过长打点展示并支持hover
                        点击关闭按钮，退出任务详情弹窗
                        配置主机
                            header: 1 配置主机
                            右侧显示未开始或者执行中
                            执行中的话时间显示：开始时间和耗时，耗时需要实时更新
                            详列：所有主机和管理ip，以及进度
                            详细步骤
                                编辑节点配置
                                检查存储网络关联网口的健康状态，并禁止网口隔离动作
                        重启存储服务
                            header: 2 重启存储服务
                            右侧显示未开始或者执行中
                            执行中的话时间显示：开始时间和耗时，耗时需要实时更新
                            详列：所有主机和管理ip，以及详细进度
                            可展开和折叠不同主机的详细进度
                            默认展开：执行中的步骤和失败的步骤
                            默认折叠：已完成的步骤和未开始的步骤
                            详细进度检查
                                进入存储维护模式
                                重启chunk 服务
                                退出存储维护模式
                                允许网口隔离动作
                    任务失败详情
                        配置主机上面红色Tip显示：启用 RDMA 失败。请联系售后解决问题后重试，重试将从失败处继续执行。
                        配置主机处错显示红X，并在下面展示失败原因 Error msg
                        多个原因，同时展示
                        重启服务储出错，在步骤处显示红X 并展示Error message
                        具体失败原因随功能测试覆盖
                        最近一次“启用 RDMA 任务”（且任务为失败）提供「重试 btn」，其他情况不提供
                        上一次'启用RDMA '失败的任务，重试按钮不可见
                        点击重试，打开【启用RDMA 任务弹窗】
                        右侧位置展示红叉【失败】or 个别绿对钩【成功】
                        其他UI 展示同上执行中
                    任务成功详情
                        配置主机上面蓝色Tip显示：已成功启用 RDMA，请尽快在业务空闲期间为 RDMA 功能配置流量控制。否则，集群存在大的 I/O 带宽时，可能出现 RDMA 丢包断连而产生数据恢复。
                        右侧位置展示对钩+【成功】
                        下面任务显示对钩
                        其他UI 展示同上执行中
                关闭任务进度
                    任务列表
                        文案：关闭集群 %cluster-name% 存储网络的 RDMA
                        时间展示
                        关闭失败，下面展示红色文案：关闭 RDMA 失败。
                        关闭成功，展示成功
                        右侧【...】可点击查看详情
                        任务前面 icon 进度展示正确
                    任务执行中详情
                        Header：存储网络关闭 RDMA
                        文案 关闭集群 #%cluster-name%# 存储网络 storage-network 的 RDMA。
                        文案这里集群名称过长看下
                        显示蓝色Tip条件：正在进行数据恢复……恢复完成后，将自动继续执行。
                        按主机分别展示
                        主机名称过长打点展示
                        主机名+管理ip+关闭状态
                        默认展开：执行中的步骤和失败的主机
                        可展开和折叠不同主机的详情
                        默认折叠：已完成的步骤和未开始的主机
                        点击关闭按钮，退出任务详情弹窗
                        主机XXX
                            编辑配置文件
                            进入存储维护模式
                            重启 chunk 服务
                            退出存储维护模式
                            调整 CPU 和内存资源分配
                    任务失败详情
                        配置主机上面红色Tip显示：关闭 RDMA 失败。请联系售后解决问题后重试，重试将从失败处继续执行。
                        对应主机处显示红X，并在下面失败步骤处展示失败原因 Error msg
                        多个原因，同时展示
                        具体失败原因随功能测试覆盖
                        最近一次“关闭 RDMA 任务”（且任务为失败）提供「重试 btn」，其他情况不提供
                        上一次失败的关闭任务，不可见重试btn
                        点击重试，页面展示正确
                        右侧位置展示红叉【失败】or 个别绿对钩【成功】
                        其他UI 展示同上执行中
                    任务成功详情
                        配置主机上面灰色Tip显示：关闭集群 #%cluster-name%# 存储网络 storage-network 的 RDMA。
                        每个主机右侧位置展示对钩+【成功】
                        下面任务显示对钩
                        其他UI 展示同上执行中
                        没有重试按钮
                其他功能禁用
                    集群升级、角色转换、移除节点、维护模式、电源管理等-待讨论
                    存储网络变更&选择VDS禁用
                        目标虚拟分布式交换机下拉列表增加禁用项
                        网络下面显示灰色
                            已关联的存储网络启用 RDMA 中...
                            已关联的存储网络关闭 RDMA 中...
                        创建系统网络：选择所属 VDS，其中存储VDS 应该禁用
                            SMTX OS（ELF）：接入网络、迁移网络、镜像出口网络
                            ZBS 不支持创建 管理、存储和接入网络
                        迁移系统网络：选择目标 VDS，存储VDS应该禁用
                            SMTX OS（ELF）：管理网络、接入网络、迁移网络、镜像出口网络
                            SMTX ZBS：管理网络、接入网络
                        编辑存储网络应该也禁用
                            编辑MTU -禁用
                            VLAN ID - 禁用
                            QoS - 禁用
                    编辑VDS禁用
                        VDS table
                            点击编辑弹出的选项框禁用，显示原因：关联网络启用 RDMA 中…
                            点击编辑弹出的选项框禁用，显示原因：关联网络关闭 RDMA 中...
                            禁用下面的几个编辑选项都禁用
                        VDS 详情面板
                            灰色tips：关联的存储网络正在%启用/关闭% RDMA……无法编辑虚拟分布式交换机。
                            Tip 右侧显示查看进度
                            点击查看详情，展示开启进度弹窗
                            点击查看详情，展示关闭进度弹窗
                            编辑菜单下的选项都禁用
                            详情下基本信息右侧编辑禁用
                            详情下基本信息 LGMP/MLD侦听编辑禁用
                            详情下基本信息 DPDK 编辑禁用
                            详情下关联主机 编辑禁用
                    添加主机
                        点击添加主机，弹窗显示原因：新增原因：「该集群的存储网络正在%启用/关闭% RDMA……」
                        有其他优先级高的，优先展示
                        一次性弹窗在480上面会修改，这里需要再测试一遍
            功能测试
                集群架构& 特性等组合
                    Intel x86_64 & large 2 实例
                    AMD x86_64
                    Hygon x86_64 & large 4 实例 & vhost
                    鲲鹏 AArch64 &normal 2 实例
                    tl3
                    arcfra
                    qe 集群开启或关闭，运行几天
                    飞腾不支持-预检查预期会提示
                    双活集群不支持（同上测试）
                    vhost 集群
                开启
                    开启预检查
                        集群正在升级，不可启用& 提示无法启用原因
                            集群正在升级-不通过
                            集群vgpu & kernel 升级中-不通过
                            文案展示
                            集群未处于升级中，检查通过
                            扩容根分区 - 预期不通过
                        双活检查，命令行看一下后端返回，前面UI没有入口
                            双活开启
                            双活未开启
                        节点健康情况
                            主机无响应
                            主机亚健康 - 预期不通过
                            chunk 状态
                                维护模式
                                idel
                                removing
                                in use
                                    健康-通过
                                    connect error
                                    expired
                        数据恢复检查
                            有数据恢复
                            无数据恢复
                        存储网络所属VDS
                            ovs bonding 模式为ab -通过
                            ovs bonding 为 balance tcp -通过
                            ovs bonding 为 balance-slb - 不通过
                            支持RDMA检查
                                个别节点上面的网口不支持RDMA-不通过
                                所有节点关联的网口都支持RDMA-预检查通过
                                展示主机以及对应不支持的网口
                                RDMA 运行在非RoCE 模式-不通过
                                白名单这里选qe环境有的测试，不全覆盖-通过
                                bonding 的网口不是同一张网卡，预期支持
                                没有bonding-预期通过
                                部署的时候两个网口一个支持一个不支持RDMA
                                同一张网卡，一个网口不支持RDMA
                                单网口 - 预期通过
                            是否包含其他系统网络
                                包含其他系统网络：迁移网络、接入网络、管理网络、镜像出口网络等-不通过
                                不包含其他系统网络-通过
                            ER关联检查
                                存储网所在的 VDS 没有关联到 ER 防火墙
                                存储网络所在VDS 没有关联到 ER 安全导流
                                存储网络有关联 ER防火墙-不通过
                                存储VDS有关联分布式防火墙-不通过
                            网口故障
                                bonding模式下，如ab模式单网口故障 - 预期不通过
                                单网口l2ping隔离掉 - 预期通过？-- to wenfei
                                接着上调用例，隔离恢复，端口还能加回去& 检查是否RDMA功能正常
                                存储网络故障，预检查会提示主机不健康等
                        存储网络条件
                            未配置Qos-通过
                            配置Qos-不通过
                            VLAN ID 为0-通过
                            VLAN ID 不为0-不通过
                        预检查后
                            存在基于 lcm-manager 的冲突任务，无法点击「启用 RDMA」
                                主机角色转换过程中
                                移除主机过程中
                                采集物理盘日志过程中
                                角色转换过程中
                    开启过程中
                        开启和关闭过程中虚拟机操作、运维等 - jinrui 帮忙cover
                        RDMA 状态展示，以及开关展示情况，预期
                    开启成功
                        预检查条件满足，预期可以开启成功
                        开启过程中有数据恢复，下个节点开始前要等待数据恢复完成
                        开启成功后概览页和网络刷新RDMA状态，展示RDMA 关闭btn
                    开启成功检查
                        /etc/zbs/rdma_enabled 为 true
                        cgroup 配置符合rdma 配置： zbs-deploy-manage show_cgroup
                        确定 cat /proc/meminfo  | grep HugePages 中大页的数量 HugePages_Total 是 2560（如果开启 vHost/NVMF 可能更多）-630 下看下最大规格情况的大页内存
                        RDMA 网卡的 PFC 流控 - zhaoguo帮忙验证
                        基于 Global Pause 流量控制配置- zhaoguo帮忙验证
                        chunk 服务重启成功
                        开启中和开启后集群虚拟机运行正常
                        开启中和成功后监控图显示正常& 无非预期的告警产生
                        /etc/sysconfig/zbs-chunkd
                            CHUNK_USE_RDMA=true
                            CHUNK_SERVER_DATA_IBDEV_NAME=rocexxxxx,rocexxxxx
                            ZBS_DMALLOC_USES_HUGEPAGE=true
                            ZBS_DMALLOC_MEMORY_SIZE=5368709120 （2实例和4实例也要看下）
                    开启失败
                        主机CPU 不满足，配置主机处提示：主机的 CPU 或内存不满足启用 RDMA 要求。
                        开启失败，UI 展示报错正确
                        其他原因，随故障测试
                        查看RDMA状态展示以及开关展示情况
                    开启重试
                        点击重试按钮，进入开启预检查流程（确认窗口）
                        重试，会重开一个开启一样的任务
                        重试成功，预期所有节点都开启RDMA，检查点同开启成功
                        成功的主机会检查&跳过，操作从失败的主机
                        从两个入口处预期也支持进入重试
                关闭
                    关闭预检查
                        存储网络所属 VDS 的 Bonding 方式需为 OVS Bonding - 通过
                        存储网络单网口 - 通过
                        集群中存在正在进入维护模式或处于（存储）维护模式的主机 - 不通过
                        预检查后
                            存在基于 lcm-manager 的冲突任务，无法点击「关闭 RDMA」
                                主机角色转换过程中
                                移除主机过程中
                                采集物理盘日志过程中
                                角色转换过程中
                    关闭成功
                        关闭过程中有数据恢复，下个节点开始前要等待数据恢复完成
                        关闭成功后概览页和网络刷新RDMA状态，展示RDMA 开启btn
                        上面开启成功的用例预期都能关闭成功，需要double check下
                    关闭成功检查
                        /etc/zbs/rdma_enabled 为 false
                        cgroup 配置符合rdma 配置： zbs-deploy-manage show_cgroup
                        chunk 服务重启成功
                        大页内存不用的预期被回收
                        在 /etc/sysconfig/zbs-chunkd，以下配置不存在
                            CHUNK_USE_RDMA=true
                            CHUNK_SERVER_DATA_IBDEV_NAME=rocexxxxx,rocexxxxx
                            ZBS_DMALLOC_USES_HUGEPAGE=true
                            ZBS_DMALLOC_MEMORY_SIZE=5368709120
                    关闭过程中
                        过程中虚拟机操作、运维等- jinrui帮忙cover
                        RDMA 状态展示，以及开关展示情况，预期
                    关闭失败
                        查看RDMA状态展示以及开关展示情况
                        其他运维禁用情况 - 再讨论
                        随故障测试
                    关闭重试
                        点击重试按钮，重新加载该页面
                        重试，重开一个关闭任务展示
                        重试成功检查点- 参看关闭成功检查
                        从两个入口处，预期也支持关闭重试
                事件审计
                    开启RDMA
                        文案：编辑存储网络{{存储网络名}}，配置变化为： RDMA：未启用 → 启用
                        回归时间、用户等
                        开启失败
                        重试也计入事件审计
                    关闭RDMA
                        编辑存储网络{{存储网络名}}，配置变化为： RDMA：启用 → 未启用
                        回归时间、用户等
                        关闭失败
                        重试也计入事件审计
                权限管理
                    有权限：系统网络 > 系统网络管理（需要同时勾选虚拟机分布式交换机的管理）
                    无权限
            场景组合测试
                开启之后，集群重启
                关闭之后，集群重启
                存储、接入网络融合情况下，不支持开启
                存储和管理网络融合情况下，不支持开启
                大规格集群 8-16节点+&enabe vhost - 开启RDMA之后再关闭（尽量找环境）
                开启之后巡检
                关闭之后巡检
                全家桶部署集群上开启和关闭，double check 下流量可视化否有波动 （tower 要部署在集群里面-关注下是否有延迟）
                升级
                    RDMA（500~504 OVS bonding） 初始版本部署一路升级上来，关闭RDMA，之后再升级
                    （505-620） RDMA（linux bonding 模式 ）升级上来，手动转成OVS bonding ， 关闭RDMA ，再开启
                    低版本 OVS bonding balance-slb 开启RDMA升级上来，关闭
                    低版本 OVS bonding balance-slb 升级上来，之后预检查会失败，手动转换之后再开启
                    未开启 RDMA低版本 OVS bonding  ab 升级上来，开启RDMA
                    未开启 RDMA低版本 OVS bonding  balance tcp 升级上来，开启RDMA
                    3.X 部署，一路升级上来，开启RDMA，之后再升级
                    4.X 部署一路升级上来，开启RDMA
                    507 转oe 升级上来，开启、关闭RDMA
                节点管理
                    开启RDMA之后添加节点
                    关闭RDMA之后添加节点
                    开启RDMA之后，角色转换，再移除节点
                    关闭RDMA之后，角色转换再移除节点
                    开启RDMA 之后再开启vhost
                回归测试
                    内存不足大页分配的情况，需要释放部分虚拟机，这里是cgroup已有的内容，简单回归下
                    开启、关闭过程中虚拟机的影响、以及开启之后虚拟机检查- jinrui 会帮忙确认
                    er&网络- wenfei帮忙确认
                    虚拟机的io zhaoguo 测试
                    其他系统服务预期不会被影响
                        可观测关联集群
                        可观测开启流量可视化
            故障测试（故障失败之后都要测试下回复故障&重试）
                部分节点开启成功后，集群的存储状态以及影响等--zhaoguo帮忙cover
                开启故障
                    网络故障
                        开启过程中个别节点存储网络不通
                        管理网络不通不影响开启或者关闭
                    磁盘故障
                        开启过程中主机的系统盘故障
                        开启过程中主机的缓存盘或者数据盘故障
                    节点异常
                        开启过程中，主机重启
                        开启过程中主机掉电
                    节点服务异常
                        开启过程中chunk服务异常
                        其他服务 - 不需要测试
                开启步骤故障
                    /etc/zbs/rdma_enabled 不存在
                    cgroup 配置过程中，有其他进程导致cgroup 变化（模拟下手动config_cgroup）
                    chunk 配置文件不存在或者被其他进程锁住
                    PFC 流控修改时候被其他进程干扰（手动配置下. /etc/sysconfig/zbs-chunkd; /usr/share/zbs/bin/zbs_config_rdma_qos.sh dscp $CHUNK_SERVER_ACCESS_QOS_MODE）
                    节点已经进入维护模式  - 需要wangna帮忙看下
                    数据恢复迟迟不结束，产生dead
                关闭故障
                    网络故障
                        关闭过程中个别节点存储网络不通
                        管理网络不通不影响开启或者关闭
                    磁盘故障
                        开启过程中主机的系统盘故障
                        关闭过程中主机的系统盘故障
                        开启过程中主机的缓存盘或者数据盘故障
                        关闭过程中主机的缓存盘或者数据盘故障
                    节点异常
                        关闭过程中主机重启
                        关闭过程中主机掉电
                    节点服务异常
                        关闭过程中chunk 服务异常
                        其他服务-不需要测试
                关闭步骤故障
                    /etc/zbs/rdma_enabled 不存在
                    cgroup 配置过程中，有其他进程导致cgroup 变化（模拟下手动config_cgroup）
                    chunk 配置文件不存在或者被其他进程锁住
                    PFC 流控修改时候被其他进程干扰（手动配置下. /etc/sysconfig/zbs-chunkd; /usr/share/zbs/bin/zbs_config_rdma_qos.sh dscp $CHUNK_SERVER_ACCESS_QOS_MODE）
                    节点已经进入维护模式
                    数据恢复迟迟不结束，产生dead
            命令行
                zbs-cluster rdma enable
                zbs-cluster rdma disable
                zbs-node set_rdma enable/disable precheck
                zbs-node set_rdma enable/disable change_config
                zbs-node set_rdma enable/disable restart
                network-tool 转换为 active-backup bond
                单个节点开启成功后其他节点失败，查看：zbs-chunk dc get_manager_info --type storage
            接口测试 - tower api 随ticket 验证- 这里略
                /api/v1/clusters/{cluster_uuid}/storage/set_rdma
            zbs 测试用例
                新部署集群
                    balance-slb / RDMA off / 跨物理网卡
                    active-backup / RDMA on / 不跨物理网卡
                低版本升级到 smtxos-630
                    smtxos 5.0.0 - 5.0.4
                        balance-slb / RDMA off / 跨物理网卡（配置继承）
                        balance-tcp → active-backup / RDMA on / 不跨物理网卡（升级后转换 bond）
                    smtxos 5.0.5 - 6.2.0
                        balance-slb / RDMA off / 不跨物理网卡（配置继承）
                        802.3ad → active-backup → balance-tcp / RDMA on / 不跨物理网卡（升级后转换 bond）
        630 ntp 强制同步
            集群
                UI 测试
                    英文文案
                    集群时间设置
                        1 当前集群的时区、时间及 NTP 服务器配置状态数据，均源自集群内时钟管理服务主节点。
                        1.1 hover 展示：“在时钟管理服务中，集群通过选主机制确定唯一的主节点。主节点作为集群的统一时间源，负责为所有节点提供时钟同步服务。”
                        非编辑状态表格内容-随功能测试
                        tower升级480 上来，旧版本集群仍展示旧的格式，并且数据正确
                        tower 升级480 上来& 集群升级到630 ，UI 展示同上述内容 1->5 &数据正确
                        新版本集群搭配旧版本tower 不考虑
                        2. 集群时间
                            集群时区展示 - “%区域/名称% （%UTC偏移量%）”
                            非 Asia/Shanghai（UTC+08:00）时区看一下
                            集群时间回归
                        3. 强制同步
                            文案& 按钮：强制同步至 NTP 服务器时间。
                            点击按钮 - 强制同步时间弹窗
                        4. NTP 服务器时间 + 时间展示
                            未配置： NTP 服务器时间     暂未配置外部 NTP 服务器
                            配置过NTP展示：
                                NTP 服务器时间   集群 ntpm leader 时间（leader 调整5分钟）
                                NTP 服务器时间     无法获取
                                    ntp 相关api 异常
                                    ntp 服务器异常
                                    集群异常
                                    集群失联
                                    刚关联集群
                        5. NTP 服务器
                            建议文案：建议配置 3 个及以上的外部服务器地址，并确保集群所有主机均可访问，以保证时间同步。
                            若不配置外部 NTP 服务器，则所有主机向时钟管理服务主节点保持同步。
                            Default 样式：未配置 NTP 服务器时，展示空白状态
                            编辑
                                空白页展示添加服务器按钮
                                「添加服务器」
                                    点击【添加服务器】新增一行 当没有 NTP 服务器时，不展示表头，仅展示按钮；
                                    当大于等于 1 行时，展示表头，每行展示服务器地址、状态 remove button，点击后则删除此行
                                    新增20行看一下展示
                                表格
                                    服务器地址
                                    状态，默认展示 -
                                    填入服务器地址校验
                                        填入有效地址时，解除「检查有效性」按钮禁用；
                                        填入时，禁用「保存」按钮
                                        字段校验
                                            请填写 NTP 服务器地址。
                                            请填写正确格式的 NTP 服务器地址。
                                            地址重复。
                                            域名地址重复。
                                            域名和ip 重复没有校验
                                    remove button
                                        hover 提示：移除
                                        点击后删除所在行
                                        删除掉所有行之后，最上面的表头隐藏掉
                                    检查有效性状态机
                                        当所有服务器地址输入框都填入有效字段，禁用->未检查（可点击）
                                        地址UI校验通过之后再点击添加ntp服务器，检查按钮切回不可点
                                        修改某个ip，检查按钮仍可点
                                        点击【检查有效性】->检查中
                                        检查中：按钮显示loading 状态，文案提示：正在检查有效性....
                                        检查不通过
                                            保存按钮不可点（回车也不可以）
                                            文案提示：有效性检查不通过，请尝试更换服务器地址。
                                            检查有效性按钮仍可以点击
                                            对应NTP 服务器地址下方提示error msg
                                        检查通过
                                            文案提示：有效性检查通过，请保存配置。
                                            检查有效性按钮仍可以点击
                                            保存按钮可点击（回车也可以）
                                    保存
                                        点击后发起「编辑集群设置」任务，保存当前的 NTP server 配置（若均为空则视为未配置 NTP server）；
                                        点击后退出编辑模式
                                        检查通过之后，保存按钮才可以点
                                        检查通过之后，修改某个ip 或者添加新的服务器，保存变为按钮不可点
                                        已有保存成功的记录，编辑删除一个，不经过检查保存按钮不可点
                            取消编辑
                                点击取消编辑，退出编辑模式
                    强制同步弹窗
                        Title :强制同步时间
                        文案：确认强制同步集群 xxx 的时间至 NTP 服务器时间吗？
                        x 关闭
                        取消
                        时间
                            配置了NTP服务
                                无法获取
                                若配置了NTP server，展示： 时间 + 时区（以 “%区域/名称% （%UTC偏移量%）） 显示正确
                                预期同时间设置页面UI展示一样
                            没有配置NTP
                                自定义时间 + 输入框 + 时区（以 “%区域/名称% （%UTC偏移量%））展示
                                自定义时间校验
                                    没有输入：请填写自定义时间。
                                    输入格式不对 ：仅支持 YYYY-MM-DD HH:mm:ss 格式的时间（如 2025-07-23 14:30:00）。
                                    格式正确-可以保存
                                    日期很超前
                                    很久以前日期
                                    格式不对-预期不能保存
                                        YYYY-MM-DD HH:mm
                                        YYYY MM DD HH:mm:ss
                                        YYYY/MM/DD HH:mm:ss
                                        MM-DD-YYYY HH:mm:ss
                                        dd-MMM-yyyy HH:mm:ss
                                        YYYY-MM-DD HH:mm:ss tt
                        我已知晓：强制同步期间会重启对应的集群服务，禁止在同步期间进行集群变更，集群业务不受影响。
                            勾选
                            不勾选
                        强制同步按钮
                            二次确认框勾选之后可以点击，但是时间格式校验不通过的话不能提交
                            取消勾选 按钮变回不能可点击
                            点击强制按钮，发起【强制同步】任务，窗口消失
                    无法强制同步
                        Title: 无法强制同步时间
                        文案：无法强制同步集群 #%cluster-name%# 的时间。
                        错误文案
                            用户不感知的任务： 「集群正在执行后台任务……请稍后重试。」 -630-磁盘日志采集部署agent阶段
                            用户感知的任务： 「集群中存在执行中的%操作类型%任务。」
                            感知任务的%操作类型%
                                「转换节点角色」
                                「移除主机」「移除 SCVM」（注意：「SCVM」文案前后均有空格）
                                「启用存储网络 RDMA」「关闭存储网络 RDMA」（注意：「RDMA」文案前后均有空格）
                                「强制同步时间」- 当前tower
                                集群正在编辑 ssh 服务端口号……
                        关闭
                            X 关闭窗口
                            关闭按钮
                    同步任务
                        文案：强制同步%同步对象%时间至%同步方式%。 （同步对象： 集群 %culster-name%； 同步方式：自动以时间或者NTP 服务器时间）
                        进行中
                            提供详情按钮
                            点击详情展开详情窗口
                        成功
                            成功之后详情按钮可点
                        失败
                            提示失败原因
                            提供详情按钮
                        详情窗口
                            Title：强制同步时间
                            文案：强制同步%同步对象%时间至%同步方式%。 （同步对象： 集群 %culster-name%； 同步方式：自动以时间或者NTP 服务器时间）
                            提示： 关闭弹窗后，任务将在后台继续进行，可在任务中心再次打开本弹窗。
                            当发起强制同步任务时，将会立即打开此弹窗，关闭此弹窗不影响任务继续进行；
                            可参考「移除主机」、「升级 CT」弹窗，交互保持一致，尺寸为非常规尺寸的全屏弹窗（Slack 讨论、组件定义）；日志需具备搜索能力（组件定义）---
                            展示「关闭」按钮，点击后不影响任务继续进行
                            重试同步」按钮，点击重试同步后再次发起同步任务
                            点击重试同步，日志和进度刷新从头开始计入
                            重试同步仅支持ntp服务器同步，自定义不支持
                            同步进度
                                不展示剩余时间
                                同步中
                                    显示进度百分比，进度条符合预期
                                    开始时间和用时正确
                                同步失败
                                    显示进度条，X 失败
                                    开始时间和用时正确
                                同步成功
                                    显示进度条到底，对钩+成功
                                    开始时间和用时正确
                            日志
                                预期和后端日志保持一致
                                ctl+f 可以搜索关键字
                                日志字体大小看一下
                    事件审计
                        NTP 服务器时间
                            文案：强制同步集群 {{集群名}}  的时间至 NTP 服务器时间
                            同步成功
                            同步失败
                        自定义时间
                            文案：强制同步集群  {{集群名}} 的时间至自定义时间
                            同步成功
                            同步失败
                    集群概览页面 -集群名称下方展示tip
                        集群未配置外部 NTP 服务器。
                            文案：集群未配置外部 NTP 服务器。 右侧展示【去配置】超链接和关闭按钮
                            首次关联集群或编辑集群设置后，若集群未配置有效的 NTP 服务器，且用户有集群设置权限时，则展示此条 tip；
                            点击「去配置」后跳转到「集群设置 - 集群时间」页面，点击 remove button 后，当前配置未变更前，该用户不再展示此 tip
                            用户没有权限，不展示这个tip
                        NTP 无法与当前集群同步时间
                            文案：外部 NTP 服务器与当前集群无法同步时间。右侧展示【强制同步】超链接和关闭按钮
                            触发「外部 NTP 服务器与集群无法同步时间」报警，且用户有强制同步时间权限时，展示此条 tip；报警被解决时，自动隐藏 tip；（tip 展示顺序暂未确定，请 cc @yuhe.han 讨论）
                            点击「强制同步」后直接打开「强制同步集群至 NTP 服务时间」弹窗，点击 remove button 后，新报警触发前，该用户不再展示此 tip
                            用户没有权限，不展示这个tip
                功能
                    有效性检查，chrony后端命令double 确认下
                        不通过
                            error 类型
                                非ntp 地址，error msg：NTP端无响应
                                2个ntp地址时间不同步:多个 NTP 服务器无法达成一致。
                                地址连不上提示：网络连通异常
                                不支持使用集群上的虚拟机 IP 地址作为外部 NTP 服务器。
                                获取 NTP 服务器状态失败。
                                地址解析失败。
                                Chrony 客户端检查未通过。
                                地址无效（兜底）-前端有校验，看下api返回
                            error 场景
                                ntp服务是非默认端口
                                ntp服务未运行-无响应
                                配置4个服务器：两两时间一致；
                        通过
                            配置一个服务器和集群时间不一致，预期通过
                            配置三个服务器：两个服务器时间一致，一个服务器时间不一致，预期通过
                            上述两个服务器时间一致，一个服务器时间不一致，检查通过之后，再删除一个不可保存，再次检查预期不通过
                            配置多个服务器 & 包含windows ntp 服务器
                            域名地址
                        故障
                            集群故障
                            ntpm leader 异常（选主异常的情况）
                            单节点故障没有影响
                            chronyd 故障
                            vip 节点的ntpm 异常
                    表格内服务器状态，chrony后端命令double 确认下
                        状态15s 同步一次
                        前面校验能同步时间的就返回通过，这里的状态是要case by case 显示
                        状态异常的时候检查tower 设置页面同步显示
                        不同ntp 多个显示异常
                        所有ntp 异常，集群会触发告警
                        3个ntp 剩余一个可用的话，再次校验，可能不通过，测试看下现象
                        状态检查
                            没有发现问题：  PASS
                            域名无法解析（NET_ADDRESS_RESOLVE），error：地址解析失败
                            IP网络无法联通 （NET_IP_CONNECTIVITY），error：网络连通异常
                            NTP 服务器端无响应  (NTP_RESPONSIVE)：服务端无响应
                            chrony 检查失败 （构造场景较为困难）：客户端检查未通过
                            多个NTP服务器无法达成一致（CHRONY_MAJORITY）：客户端检查未通过
                            系统时间与NTP服务器时间偏差太大（TP_DISTANCE）：存在时间偏差
                    同步
                        未配置ntp
                            同步不成功
                                部分节点失联
                                ntpm leader 选主异常
                                集群失联
                                服务重启不成功
                                vip 所在节点 ntpm 异常
                                看下不成功集群节点的现象
                            同步成功
                                检查服务重启成功，集群正常运行
                                所有节点时间同步成设置的时间
                        配置了ntp
                            同步不成功
                                当配置的ntp服务都不可用
                                3 ntp 服务器chrony 检查无法达成一致，预期不成功
                                部分节点失联
                                ntpm leader 选主异常
                                集群失联
                                服务重启不成功
                                vip 所在节点 ntpm 异常
                                看下不成功集群节点的现象
                            同步成功
                                正常的ntp服务器
                                正常的域名服务器
                                检查服务重启成功
                                所有节点时间同NTP server的时间
                                修改时区之后再同步
                                2：1 的配置，两个可用ntp都故障不可用，能够同步成功
                                部分ntp服务异常，先排除状态不正常的，剩余的状态正常的ntp 能达成一致就可以同步成功
                回归
                    集群时间展示正常
                    节点时间展示正常
                    chrony 版本正确
                    UI 设置
                        有权限
                        没权限
                    告警
                        关联可观测告警触发&解决
                        未关联可观测告警触发&解决
                        回归集群和tower 时钟不一致告警
                        告警项
                            {target}_can_connect_with_ntp_server
                                检查metrics 数据上报正常
                                外部ntp server，当节点（leader ）无法与ntp sever 通信，触发告警
                            {target}_can_sync_with_ntp_server
                                检查metrics 数据上报正常
                                外部的 ntp server，时差很大，也会触发告警
                                外部的 ntp server，当前节点为 ntpm Leader 节点，与设置的外部 NTP 源无法同步时，会触发告警
                                内部ntp server，当前节点为 ntpm Follower 节点，和内部的 NTP Leader 无法同步时，会触发告警
                                时间差超过600 s 不能同步时钟，一定有告警
                            {target}_time_offset_with_ntp_server_seconds
                                检查metrics 数据上报正常
                                时钟偏移量大于30s 触发告警
                            新增集群没有配置ntp 服务器告警
                                配置ntp 服务器
                                未配置ntp 服务器
                                集群未关联可观测触发&解决
                                关联可观测触发&解决
                                英文文案
                                告警规则
                                    vmware 或者smtxelf 都要看下
                                    Tower 上面新增告警规则
                                        新部署tower
                                        升级tower
                                        未关联新版本集群的tower 预期不展示
                                    编辑告警规则-端到端检查触发
                                        修改阈值
                                        禁用、启用
                                        告警级别编辑
                                        设置特例规则
                                告警触发
                                    依据业务判断触发时效和文案提示是否满足等
                                    tower 展示的告警对象、触发时间、报警源、告警等级、报警规则、持续时间
                                    告警文案中英文检查
                                告警解决
                                    手动解决
                                    自动解决
                                    解决时间
                                告警接收至少检查一组
                                    webhook
                            域名配置的时候，解析失败之后预期告警：
                                {target}_can_connect_with_ntp_server
                                {target}_can_sync_with_ntp_server
                    低版本ntp 服务时间设置
                        62X
                        51X
                api
                    GET /v1/server/show/cluster  每个节点信息中增加 time_zone 字段，格式为 "+08:00"
                    GET /v1/server/show/node  中增加 time_zone 字段, 格式为 "+08:00"
                    POST /v1/server/time
                    POST /v1/source/check
                命令行
                    ntpm
                        ntpm source set
                        ntpm source show     容器
                        ntpm server start
                        ntpm server sync
                        ntpm server health  容器
                        ntpm server show      （字段名称会有变化）
                        tower 新版本回归下告警-xinning
                    时钟同步命令
                        zbs-cluster sync_time
                        zbs-node sync_time
                        zbs-cluster sync_internal_leader_to_normal --time <time_string>
                        zbs-cluster sync_internal_leader_to_normal  --time "-60 second"
                场景组合
                    个别节点时间不能同步时间，预期可以强制同步解决，执行巡检
                    手动模拟节点主板时间不准，重启节点之后手动同步，之后巡检
                    集群同步到自定义时间（时间差不大），新增加节点之后，节点时间可以自动同步
                    强制同步之后，可观测metrices 和告警触发
                    df 和qe 全家桶集群点击强制同步，检查集群告警和服务运行情况，执行巡检
                    告警触发和tip 展示一致
                        未配置ntp
                        无法和ntp server 同步
                平台
                    vmware环境
                    smtxelf 环境
                    hygon + 腾讯os  升级环境
                    arm 升级环境
                    arcfra
                    双活集群，着重看下仲裁节点
        Tower 480 HA - 运维功能回归
            tower 升级场景
            ha 之后的passive tower 简单看下，再次ha回来
            故障模拟
                master tower 关机故障
                master tower 断开网络
                命令行触发一下
            + - 集群运维
                监控图表回归
                角色转换
                    低版本（pvc日志写满200M ）tower 升级到4.8.0
                    历史数据
                        角色转换成功
                        角色转换失败
                        主机失败的标记
                    ha 之后
                        成功和失败的记录
                        主机失败的标记
                        失败记录重试
                        日志
                        任务
                    进行中
                        master-》storage
                        storage->master
                        ha 之后支持重试
                移除节点
                    进行中
                    低版本（pvc日志写满200M ）tower 升级到4.8.0
                    历史数据
                        移除节点成功
                        移除节点失败1-重启服务前
                        移除节点失败2 -重启服务之后
                        失败的标记
                    ha 之后
                        重试失败的任务
                        日志
                        任务
                        失败的记录
                添加主机
                    进行中
                    历史数据
                        网络前失败
                        网络后失败
                        成功记录
                    ha 之后
                        失败清理重试
                        日志
                        任务
                rdma 开关
                    ha 之后检查
                        开启失败记录
                        关闭失败记录
                        重试开启
                        重试关闭
                        任务
                        事件
                    存在进行中的任务发生 ha
                        开启 rdma
                        关闭 rdma
                    功能回归
                        开启
                        关闭
                        失败重试
                    历史数据
                        开启
                        关闭
                        开启失败
                        关闭失败
                节点重启
                    历史数据
                        节点重启
                        重启失败
                    功能
                        节点关机
                ssh 端口修改
                    功能回归
                    历史数据
                        更新端口
                        改失败
                        端口不一致告警
                    ha 之后
                        解决告警
                磁盘挂载
                    批量挂载中
                    卸载中
                    历史数据
                        成功
                        失败
                集群日志采集
                    ha 之后历史数据能下载
                ntp 一键同步
                    历史数据
                        配置ntp服务器
                        ntp 配置失败
                    功能
                        配置ntp
                        校验检查
                维护模式
                    tower ha 几个虚拟机部署在老版本集群上面 回归
                    tower ha 三个虚拟机部署在一个集群上
                        预检查页面业务虚拟机不提示tower 虚拟机
                        系统服务虚拟机提示默认忽略放置组
                        迁出& 迁回
                        tower 虚拟机不能迁移回归
                    tower 单点部署回归
                        预检查
                        系统服务提示
                        迁出、迁回
            + - 集群上下线工具
                文档处理，回归下
            集群部署硬件监控组件
                ha 前构造历史数据
                    部署硬件监控组件成功
                    部署硬件监控组件失败
                    已触发 sel 报警
                发生 ha
                    正在部署硬件监控组件
                ha 后检查
                    ha 前进行中的部署任务（重试次数未耗尽） -   继续执行 - 执行成功
                    ha 前进行中的部署任务（重试次数耗尽） -   直接失败
                    检查 已触发 sel 告警存在，手动解决成功
                    触发新 sel 告警成功
        630  -  8 条带数回归 - 可观测 & 高级监控
            obs
                部署
                    新部署 630 单活 smtxos 集群
                        系统盘
                            检查 条带数是 4
                        数据盘
                            检查 条带数是 8
                    630 smtxos 以下
                        数据盘
                            检查 条带数是 4
                        系统盘
                            检查 条带数是 4
                    zbs 570
                        数据盘
                            检查 条带数是 4
                        系统盘
                            检查 条带数是 4
                    zbs 580（暂不支持）
                        数据盘
                            检查 条带数是 4
                        系统盘
                            检查 条带数是 8
                    涉及到 分发 scos 模版，简单看一下条带数
                        scos 模版只包含系统盘，分发保持4条带不变，以上操作在同一个 tower 创建obs 已包含分发系统盘检查
                扩容
                    数据盘是 4条带 扩容后保持 4 条带
                    数据盘是 8 条带 扩容后保持 8 条带
                    系统盘不影响 保持 4 条带
                    磁盘容量只能扩容为偶数 TOWER-20786
                        630 smtxos 集群
                            检查扩容 obs 磁盘界面，输入奇数自动变为偶数
                            检查部署 obs ui 界面，输入奇数自动变为偶数
                        630 smtxelf + zbs 570 集群
                            检查扩容 obs 磁盘界面，输入奇数自动变为偶数
                            检查部署 obs ui 界面，输入奇数自动变为偶数
                        570 zbs 集群
                            可使用 奇数容量扩容
                        低于 630 smtxos 集群
                            可使用 奇数容量扩容
                        低版本集群部署 obs  - 升级集群至 630
                            使用偶数容量扩容
                升级场景
                    低版本集群部署 obs  - 升级集群至 630
                        系统盘
                            检查 条带数是 4
                        数据盘
                            检查 条带数是 4
                    低版本集群部署 obs  - 升级集群至 630  - 升级 obs
                        系统盘
                            检查 条带数是 4
                        数据盘
                            检查 条带数是 4
                    630 新部署 obs - 升级 obs
                        系统盘
                            检查 条带数是 4
                        数据盘
                            检查 条带数是 8
            高级监控
                部署 630  vmware 集群
                    系统盘
                        检查条带数是 4
                    数据盘
                        检查条带数是 4/8
                    磁盘容量扩容为偶数
                        扩容成功
                        检查数据盘条带数与扩容前一致
                        检查系统盘条带数与扩容前一致
                    磁盘容量扩容为奇数
                        扩容失败，检查报错提示语
                        检查数据盘条带数与扩容前一致
                        检查系统盘条带数与扩容前一致
                部署到低版本 smtxos 集群 - 升级集群至 630
                    系统盘
                        检查条带数是 4
                    数据盘
                        检查条带数是 4
                    磁盘容量扩容为偶数
                        扩容成功
                        检查数据盘条带数与扩容前一致
                        检查系统盘条带数与扩容前一致
                    磁盘容量扩容为奇数
                        扩容成功
                        检查数据盘条带数与扩容前一致
                        检查系统盘条带数与扩容前一致
                    升级高级监控
                        系统盘
                            检查条带数是 4
                        数据盘
                            检查条带数是 4
                从 fisheye 部署在 630 smtxos 集群
                    系统盘
                        检查条带数是 4
                    数据盘
                        检查条带数是 4/8
                    磁盘容量扩容为偶数
                        扩容成功
                        检查数据盘条带数与扩容前一致
                        检查系统盘条带数与扩容前一致
                    磁盘容量扩容为奇数
                        扩容失败，检查报错提示语
                        检查数据盘条带数与扩容前一致
                        检查系统盘条带数与扩容前一致
    双活
        POC
            VM 创建，自动调度至合适的主机，预期在优先可用域
            VM 创建，指定优先可用域
            VM 创建，指定次级可用域
            单可用域故障
            全部可用域故障
            可用域之间网络故障，zk leader 在优先可用域
            可用域之间网络故障，zk leader 在次级可用域
            优先可用域节点扩容（配置静态路由）
            次级可用域节点扩容（配置静态路由）
            优先可用域节点缩容（配置静态路由）
            次级可用域节点缩容（配置静态路由）
            磁盘扩容
            磁盘缩容
            维护模式
            安装部署
                smtxos-5.1.3，6.1.0 开始支持 arm 平台
                smtxos-6.2.0 开始支持 vhost（命令行 enable/disable vhost）
                ELF 平台安装部署
                VMware 平台安装部署
                存储网 bond
                不支持 NVMF 和 RDMA
                smtxos-5.1.4 ,6.1.0 开始支持系统盘独占物理盘
                SMTX ELF 不支持双活部署
            非双活转双活&仲裁节点重建
                系统盘独占物理盘（实际硬 raid 本身是需要硬件层面有两个 ssd）
                系统盘和缓存盘共享
                配置静态路由，重建仲裁节点
                非双活转双活
            升级
                分层模式，6.0.0 之前版本升级到 6.0.0 之后版本
                不分层模式，6.0.0 之前版本升级到 6.0.0 之后版本
平台组件
    监控报警系统
        监控告警项
            630 root 账号失效告警（crond 失效问题）
                增加告警
                    告警规则
                        新增规则
                            主机 { .labels.hostname } 用户 { .labels._user } 的登录密码将在 { .value } 天后过期。
                                手动增加登录密码的有效期 - 告警自动解决
                                注意告警（默认值)
                                    user_password_days_until_expire 等于 10 天 - 【注意】级别的告警
                                    user_password_days_until_expire 大于 5 且小于 10天 - 【注意】级别的告警
                                    user_password_days_until_expire 由 3 天更新为 6 天，【严重】级别告警自动解决，新产生【注意】级别告警
                                严重告警（默认值）
                                    user_password_days_until_expire 等于 5 天 - 【严重警告】
                                    user_password_days_until_expire 小于 5 天 - 【严重警告】
                                    user_password_days_until_expire 由 6 天更新为 小于 5 天，【注意】级别告警会自动解决，新产生【严重】级别告警
                            主机 {{ $labels.hostname }} 用户 {{ $labels._user }} 的登录密码已过期。
                                密码已经过期，手动增加登录密码的有效期 - 告警自动解决
                                严重告警
                                    user_password_expired 为 true 已经过期 -  【严重警告】
                                    user_password_days_until_expire 由 5 天更新为：过期，密码将过期告警自动解决，新产生密码已过期告警
                        编辑告警规则 - 端到端检查触发
                            禁用告警规则
                            启用告警规则
                            重置为默认值
                            设置特例规则
                            报警级别编辑
                                启用 / 不启用 【信息】级别
                                启用 / 不启用 【注意】级别
                                启用 / 不启用 【严重警告】级别
                                3 个报警级别都同时启用
                                只启用一个报警级别
                            修改阈值
                                修改【信息】级别告警阈值
                                修改【注意】级别告警阈值
                                修改【严重警告】级别告警阈值
                        告警触发 & 解决
                            告警触发
                                账户密码快过期触发告警
                                账户密码密码已过期触发告警
                                账户密码未过期且过期时间大于告警范围 - 不会产生告警
                                告警文案中、英文检查
                                Tower 展示的触发告警内容正确：报警对象、触发时间、报警源、告警等级、报警规则、持续时间
                                触发告警时间：20 分钟
                            告警解决
                                触发告警 - 未解决问题 - 手动解决告警 - 会立即新产生新的一样的告警
                                触发告警 - 解决问题 - 手动解决告警
                                触发告警 - 解决问题 - 自动解决告警
                                告警已解决 - 展示的报警对象、触发时间、报警源、告警等级、报警规则、触发时间、解决时间正确
                                解决时间：10 分钟
                        Tower 新增告警
                            新部署 Tower 验证规则
                            低版本 升级上来的 Tower 验证规则
                            未关联新版本集群 Tower 不展示新增告警规则
                        其他
                            告警发送 - webhook
                            创建静默策略 - 静默时间内集群产生的告警不会通过 webhook、邮件等发送
                            集群关联可观测 - 触发告警 & 解决告警
                            集群未关联可观测 -  触发告警 & 解决告警
                            回归 - 选择几个其他告警规则，触发 & 解决功能正常
                    验证平台
                        vmware 集群
                        smtxos (centos) 平台 - 双活集群，witness 节点过期也需要有告警
                        smtxelf 平台
                        arcfra 平台
                        tos arm 平台
                    验证用户
                        smtxos 平台用户
                            root 用户
                            admin 用户
                            smartx 用户
                            手动新建的用户 - 无告警
                        arcfra 平台用户
                            root 用户
                            admin 用户
                            arcfra 用户
                            手动新建的用户 -  无告警
                    场景
                        3 节点集群，密码同时过期 - 每个节点都产生告警
                        4 节点集群，有 3 个节点已过期，有一个节点将要过期
                        vmware 低版本 root 密码快过期，升级后产生告警 - 解决root 密码快失效问题 - 告警自动解决
                        smtxos 低版本 root 密码已过期，升级后产生告警 - 解决 root 密码失效问题 - 告警自动解决
                        6.3.0 安装部署集群密码快过期/已过期 - 可以正常产生告警
                        6.3.0 版本集群 root 密码过期，产生告警 - 手动修改过期时间 - 告警自动解决 - 集群 logrotate 功能生效、crond  服务运行正常
                    metric 查看
                        host_user_password_until_expire_days
                        host_user_password_expired
                        host_user_password_never_expires
                        host_user_password_locked
            630/621 新增网口传输使用率、接收使用率告警
                告警规则
                    Tower 上面新增告警规则
                        新部署 tower
                        升级 tower
                        未关联新版本集群（630）的 tower - 不展示
                        aoc
                    编辑告警规则 - 端到端检查触发
                        修改默认阈值
                        禁用、启用
                        告警级别编辑
                        设置特例规则
                    告警支持的平台，检查适用集群包含在报警对象中
                        621 smtxos
                        621smtxelf
                        vmware、zbs  - 不支持
                告警触发
                    集群关联可观测
                        网口接收带宽使用率
                            检查触发实效和告警文案提示一致
                            检查 tower 展示的触发原因、影响、解决方法、报警源、报警等级、报警对象、报警规则、触发时间、持续时间、解决时间正确
                            告警文案中英文检查
                        网口发送带宽使用率
                            检查触发实效和告警文案提示一致
                            检查 tower 展示的触发原因、影响、解决方法、报警源、报警等级、报警对象、报警规则、触发时间、持续时间、解决时间正确
                            告警文案中英文检查
                        网口平均带宽使用率
                            检查触发实效和告警文案提示一致
                            检查 tower 展示的触发原因、影响、解决方法、报警源、报警等级、报警对象、报警规则、触发时间、持续时间、解决时间正确
                            告警文案中英文检查
                    集群未关联可观测
                        网口接收带宽使用率
                            检查触发实效和告警文案提示一致
                            检查 tower 展示的触发原因、影响、解决方法、报警源、报警等级、报警对象、报警规则、触发时间、持续时间、解决时间正确
                            告警文案中英文检查
                        网口发送带宽使用率
                            检查触发实效和告警文案提示一致
                            检查 tower 展示的触发原因、影响、解决方法、报警源、报警等级、报警对象、报警规则、触发时间、持续时间、解决时间正确
                            告警文案中英文检查
                        网口平均带宽使用率
                            检查触发实效和告警文案提示一致
                            检查 tower 展示的触发原因、影响、解决方法、报警源、报警等级、报警对象、报警规则、触发时间、持续时间、解决时间正确
                            告警文案中英文检查
                告警解决
                    自动解决
                    解决时间正确
                    集群未关联/关联可观测
                告警接收
                    webhook 通知
                监控视图
                    添加/删除/编辑 图表
                        网口带宽平均使用率
                        网口带宽传输使用率
                        网口带宽接收使用率
                        关联可观测情况下
                        未关联可观测情况下
                        切换 2h，24h，7d，30d 都可以正常展示
                        对网卡做压力测试，使用率不会超过 100%
                        图表导出 CSV 正确
                        图表复制到其他监控视图正确
        6.2.0 siren稳定性提升
            新增根分区只读类型的自监控告警
                版本平台
                    cluster
                        smtxzbs 双活 570
                        smtxzbs 562 升级到 570
                    升级场景
                        tower 442+obs 131 + zbs 562，升级到，tower 461+obs 140+zbs 570
        5.1.5 告警支持转发到可观测
            515 集群关联到可观测 -告警通知端到端检查
                可观测邮件通知配置
                可观测 snmp trap 通知配置
                可观测 web hook 通知配置
                回归下系统服务的告警可以发送
                只测试企业微信、其他的渠道不cover
                转发失败的情况下-可观测没发送成功，集群本地可以发送
                tower 版本检查
                    442 + 可观测 1.2.1 简单回归看下
                    460 + 可观测 1.2.1 简单回归看下
                    460 +1.3.1 简单回归看下
                    tower 440 -低版本集群升级到tower 442 + 515
                    集群关联到可观测，本地邮件通知&snp trap 配置自动生成可观测配置（1.2 之后就可以支持）
                    442 +可观测 1.3.1
                        515 可以支持配置、并且下发成功
                        515 以下版本不支持
                        回归600 以上版本集群可以配置、不受影响
                        通知编辑页面版本提示正确
                        邮件列表页面header 处版本提示正确
                        英文检查
                        集群内邮件配置：应急报警提示展示515 集群； 未配置邮件报警通知不展示515的集群
                    460  + 可观测1.4.0
                        515 可以支持配置、并且下放成功
                        515 以下版本不支持
                        回归600 以上版本集群可以配置、不受影响
                        页面版本提示正确
                        邮件列表页面header 处版本提示正确
                        静默和聚合要支持515吗？ - 不支持
                        英文检查
                        集群内邮件配置：应急报警提示展示515 集群； 未配置邮件报警通知不展示515的集群 - tower 460 去掉了
                本地报警通知回归
                    本地邮件配置
                    snmp trap 本地
                报警项回归 -可以转发到可观测并且发送通知-要看下告警文案内容格式等
                    集群metrics 告警
                    集群日志类告警
                    集群磁盘插拔类告警
                    集群自监控告警 - 不支持
                集群类型、架构等
                    515 vmware 集群不支持配置
                    tencent os 支持配置
                    arm 支持
                    hygon 支持
                    双活集群 支持
            回归
                515 只有本地监控
                    tower 上面不支持配置该集群的可观测配置
                    回归监控图表
                    回归告警 & 本地告警通知
                    snmp 传输
                    告警通知
                        snmp trap
                        邮件
                515 部署高级监控
                    tower 上面不支持配置该集群的可观测配置
                    回归监控图表
                    回归告警 & 本地告警通知
                    高级监控的部署、升级检查（顺道适配下最新版本高级监控）
                    回归下迁移数据到可观测
                    snmp 传输
                    告警通知
                        snmp trap
                        邮件
To Delete
    安装部署扩容
        目标版本
            smtxos-6.3.0 支持多实例部署
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
        部署集群
            fishey ui
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
            normal
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
                        1 实例
                            OS 安装在独立的硬 RAID1
                        2 实例
                            OS 安装在独立的硬 RAID1
                    OS 安装在软 RAID1
                        混闪配置
                        多种类型 SSD
                        单一 SSD，缓存盘和数据盘共享（默认）
                        单一 SSD，缓存盘和数据盘独占（可选）
                        1 实例
                            OS 安装在软 RAID 1
                        2 实例
                            OS 安装在软 RAID 1
                不分层
                    单节点数据空间容量最大 128TiB，缓存 26TiB
                    数据盘和系统盘总数量不可超过 32
                    OS 安装在独立的硬 RAID1
                        OS 安装在独立的硬 RAID 1
                    OS 安装在软 RAID1
                        OS 安装在软 RAID 1
            large
                规格
                    单 CPU 最小物理核心数 12 ，总逻辑核心 （HT 之后） >=48
                    CPU 内每个 NUMA Node 包含的物理核心数  >=8, 推荐 >=12
                    单实例，CPU 内每个 NUMA Node 包含的物理核心数  = 8，不开启 zbs/iscsi
                    单实例，CPU 内每个 NUMA Node 包含的物理核心数 =10，开启 zbs/iscsi
                    2个实例，开启 zbs/iscs，占用 23 核
                    最小内存 256G
                    查看 /etc/zbs/node_zbs_spec 为 Large
                分层
                    OS 安装在软 RAID1
                        混闪配置
                        多种类型 SSD
                        单一 SSD，缓存盘和数据盘共享（默认）
                        单一 SSD，缓存盘和数据盘独占（可选）
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
                    OS 安装在独立的硬 RAID1
                        混闪配置
                        多种类型 SSD
                        单一 SSD, 缓存盘和数据盘共享（默认）
                        单一 SSD, 缓存盘和数据盘独占（如果有一块缓存盘）
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
                        4 实例
                            混闪配置
                            多种类型 SSD 全闪配置
                            单一 SSD，缓存盘和数据盘共享（默认）
                            单一 SSD，缓存盘和数据盘独占
                OS 安装在独立的硬 RAID1
                    混闪配置
                    多种类型 SSD
                    单一 SSD, 缓存盘和数据盘共享（默认）
                    单一 SSD, 缓存盘和数据盘独占（如果有一块缓存盘）
                不分层
                    规格
                        缓存盘和数据盘共享
                        缓存盘和数据盘独占
                    1实例
                        OS 安装在独立的硬 RAID1
                        OS 安装在软 RAID 1
                    2实例
                        OS 安装在独立的硬 RAID1
                        OS 安装在软 RAID 1
        添加主机
            添加节点UI
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
            添加主机
                normal
                    分层
                        1实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                        2实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                    不分层
                        1实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
                        2实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
                large
                    分层
                        1实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                        2实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                        4实例
                            OS 安装在独立的硬 RAID1，混闪节点（分层）
                            OS 安装在独立的硬 RAID1，多种 SSD 节点（分层）
                            OS 安装在独立的硬 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，混闪节点（分层）
                            OS 安装在软 RAID1，多种 SSD 节点
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享磁盘）
                            OS 安装在软 RAID1，单一 SSD 节点（分层，缓存和数据共享独占磁盘）
                            OS 安装在独立的硬 RAID1，全缓存盘
                            OS 安装在软 RAID1，全缓存盘
                    不分层
                        1实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
                        2实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
                        4实例
                            OS 安装在独立的硬 RAID1
                            OS 安装在软 RAID1
KERNEL
    驱动适配验证
        el7 and oe - kernel - 5.10
            emulex - fc 卡 - CSFS 使用
            exanic - ExaNIC 网卡驱动
            fisec - 渔翁加密卡驱动
            hinic3 - 华为海思 SP680 系列网卡驱动
            intel-i40e-driver - x710 网卡驱动
            intel-ice-driver - Intel E810 网卡驱动
            kae - 华为鲲鹏上的一个类加密驱动 ， huangyong 在跟进
            netswift - 网讯 10G 网卡驱动
            nvidia-vgpu - vGPU 驱动 - 安装在集群主机上， 虚拟机里需要单独安装 nvidia 官网驱动
            ofed-5.8-5.1.1.2 - mellanox 网卡驱动
            qla - fc 卡 - CSFS 使用
            rnp - 中科沐创网卡驱动 - 已知 ziteng 在测试，驱动未就绪
            sfc - solarflare 网卡驱动
            sw - 三未信安加密卡驱动
            sxe - 海光四机型的网卡 LD 1160-2X 2-port 10G SFP+  的驱动
            yusur - 中科驭数的网卡驱动
            kernel-5.10.0-*， perf-5.10.0-*  - 集群 kernel 升级覆盖
        tl3 - kernel - 5.4
            emulex - fc 卡 - CSFS 使用
            fisec - 渔翁加密卡驱动
            hinic3 - 华为海思 SP680 系列网卡驱动
            intel-i40e-driver - x710 网卡驱动
            intel-ice-driver - Intel E810 网卡驱动
            netswift - 网讯 10G 网卡驱动
            nvidia-vgpu - vGPU 驱动 - 安装在集群主机上
            ofed-5.8-5.1.1.2 - mellanox 网卡驱动
            qla - fc 卡 - CSFS 使用
            rnp - 中科沐创网卡驱动 - 已知 ziteng 在测试，驱动未就绪
            sfc - solarflare 网卡驱动
            sw - 三未信安加密卡驱动
            sxe - 海光四机型的网卡 LD 1160-2X 2-port 10G SFP+  的驱动
            yusur - 中科驭数的网卡驱动
            kernel-5.4.119-*， perf-5.4.119-*， bpftool-5.4.119-* - 集群 kerenl 升级测试覆盖
    Kernel 版本升级
        SMTXOS
            Intel x86_64 架构
                el7
                    kernel-4.18.0-193.28.1.el7.smartx.18.x86_64 - 5.0.7，5.1.2
                    kernel-4.18.0-193.28.1.el7.smartx.25.x86_64 - 5.1.3
                    kernel-4.18.0-193.28.1.el7.smartx.34.x86_64 - 5.1.4
                    kernel-4.19.90-2307.3.0.el7.smartx.33.x86_64 - 6.0.0
                    kernel-4.19.90-2307.3.0.el7.smartx.60.x86_64 - 6.1.0
                    kernel-4.19.90-2307.3.0.el7.v97.x86_64 - 6.2.0
                    kernel-4.18.0-193.28.1.el7.smartx.54.x86_64 - 5.1.5
                    kernel-5.10.0-247.0.0.el7.v72.x86_64 - 6.3.0-B79
                oe
                    kernel-4.19.90-2112.8.0.0131.oe1.smartx.19.x86_64 - 5.0.7， 5.1.2
                    kernel-4.19.90-2112.8.0.0131.oe1.smartx.28.x86_64 - 5.1.3
                    kernel-4.19.90-2112.8.0.0131.oe1.smartx.68.x86_64 - 5.1.4
                    kernel-4.19.90-2307.3.0.oe1.smartx.33.x86_64 - 6.0.0
                    kernel-4.19.90-2307.3.0.oe1.smartx.60.x86_64 - 6.1.0
                    kernel-4.19.90-2307.3.0.oe1.v97.x86_64 - 6.2.0
                    kernel-4.19.90-2307.3.0.oe1.v115.x86_64 - 5.1.5
                    kernel-5.10.0-247.0.0.oe1.v72.x86_64 - 6.3.0-B79
            Hygon x86_64 架构
                oe
                    kernel-4.19.90-2112.8.0.0131.oe1.smartx.19.x86_64 - 5.0.7，5.1.2
                    kernel-4.19.90-2112.8.0.0131.oe1.smartx.28.x86_64 - 5.1.3
                    kernel-4.19.90-2112.8.0.0131.oe1.smartx.68.x86_64 - 5.1.4
                    kernel-4.19.90-2307.3.0.oe1.smartx.33.x86_64 - 6.0.0
                    kernel-4.19.90-2307.3.0.oe1.smartx.60.x86_64 - 6.1.0
                    kernel-4.19.90-2307.3.0.oe1.v97.x86_64 - 6.2.0
                    kernel-4.19.90-2307.3.0.oe1.v115.x86_64 - 5.1.5
                    kernel-5.10.0-247.0.0.oe1.v72.x86_64 - 6.3.0-B79
                tl3
                    kernel-5.4.119-19.0009.54.tl3.v89.x86_64 - 5.1.5
                    kernel-5.4.119-19.0009.54.tl3.v94.x86_64 - 6.3.0-B79
            鲲鹏 AArch64 架构
                oe
                    kernel-4.19.90-2112.8.0.0131.oe1.smartx.19.aarch64 - 5.0.7，5.1.2
                    kernel-4.19.90-2112.8.0.0131.oe1.smartx.28.aarch64 - 5.1.3
                    kernel-4.19.90-2112.8.0.0131.oe1.smartx.68.aarch64 - 5.1.4
                    kernel-4.19.90-2307.3.0.oe1.smartx.33.aarch64 - 6.0.0
                    kernel-4.19.90-2307.3.0.oe1.smartx.60.aarch64 - 6.1.0
                    kernel-4.19.90-2307.3.0.oe1.v97.aarch64 - 6.2.0
                    kernel-4.19.90-2307.3.0.oe1.v115.aarch64 - 5.1.5
                    kernel-5.10.0-247.0.0.oe1.v72.aarch64 - 6.3.0-B79
                tl3
                    kernel-5.4.119-19.0009.54.tl3.v89.aarch64 - 5.1.5
                    kernel-5.4.119-19.0009.54.tl3.v94.aarch64 - 6.3.0-B79
        SMTXELF
            x86-oe
                kernel-4.19.90-2307.3.0.oe1.smartx.33.aarch64 - 6.0.0
                kernel-4.19.90-2307.3.0.oe1.smartx.60.x86_64 - 6.1.1
                kernel-4.19.90-2307.3.0.oe1.v97.x86_64 - 6.2.0
                kernel-5.10.0-247.0.0.oe1.v72.x86_64 - 6.3.0-B58
            arrch64-oe
                kernel-4.19.90-2307.3.0.oe1.smartx.33.x86_64 - 6.0.0
                kernel-4.19.90-2307.3.0.oe1.smartx.60.aarch64 - 6.1.1
                kernel-4.19.90-2307.3.0.oe1.v97.aarch64 - 6.2.0
                kernel-5.10.0-247.0.0.oe1.v72.aarch64 - 6.3.0-B58
            x86-tl3
                kernel-5.4.119-19.0009.54.tl3.v94.x86_64 - 6.3.0-B58
            arrch64-tl3
                kernel-5.4.119-19.0009.54.tl3.v94.aarch64 - 6.3.0-B58
        ACOS
            el7
                kernel-4.19.90-2307.3.0.el7.smartx.60.x86_64 - 6.1.0
                kernel-4.19.90-2307.3.0.el7.v60.x86_64 - 6.1.1
                kernel-4.19.90-2307.3.0.el7.v97.x86_64 - 6.2.0
                kernel-5.10.0-247.0.0.el7.v72.x86_64 - 6.3.0-B79
        vGPU升级
            任务中心
                升级内核成功 - 「查看详情」
                升级内核中 - 「查看详情」
            上传 vGPU 驱动文件
                可选集群：存在 vGPU 用途的主机 + 集群未包含所选驱动文件 + CPU、操作系统 与驱动文件相同 + 集群当前内核版本小于 vGPU 驱动文件
                2	通过「本地上传」vGPU 驱动文件
                通过「URL 上传」vGPU 驱动文件
            集群详情
                Title：显示驱动文件名称
                下方显示：适配的内核版本；发布时间
            内核环境检查提交页面
                有 vGPU 主机未升级内核 + 上传内核对应驱动文件 - 无提示文案
                有 vGPU 主机未升级内核 + 无匹配的 vGPU 驱动文件 - 提示文案
            升级页面
                未上传内核对应驱动文件-选择全部主机
                    存在 vGPU 用途的主机 - 有错误提示文案。点击「升级」 Footer 报错：缺少 vGPU 驱动文件。
                    存在 vGPU 用途的主机，上传不匹配的 vGPU 驱动文件 - 有错误提示文案
                上传内核对应驱动文件（有vGPU 主机
                    1	上传内核版本的 vGPU 驱动文件 - 可以正常选择并升级内核
                升级部分主机的内核 - 选择主机
                    存在vGPU 用途的主机，取消“禁用” 选择限制 - 更新文案：存在 vGPU 用途的 GPU 设备
                    vGPU 用途的主机和关联 Tower 是一个主机 - 禁止选择当前主机 - 提示文案
                    未上传内核对应驱动文件
                        选择无 vGPU 主机 - 可以正常选择和升级内核
                        选择有 vGPU 主机 - 有错误文案
                    上传内核对应驱动文件
                        选择无 vGPU 设备主机 - 可以选择并升级内核
                        选择有 vGPU 设备主机 - 可以选择并升级内核
                    确认是否是 vGPU 主机
                        有 GPU 设备，未启用 - 识别为非 vGPU 主机
                        有 vGPU 驱动，安装驱动后启用 vGPU - vGPU 主机
                升级内核
                    选择无 vGPU 主机，升级内核步骤和之前保持一致，不会增加：「升级 vGPU 驱动」步骤
                    选择有 vGPU 主机，升级内核步骤增加：「升级 vGPU 驱动」步骤
                升级后检查
                    确认之前的 vGPU 驱动被删除
                    执行命令：rpm -qi Nvidia-vGPU 查看新驱动安装成功
                    执行命令：nvidia-smi 输出 GPU 信息
                    节点上存在挂载了 vGPU 设备的虚拟机，节点升级 vGPU 成功后，开启虚拟机能够正常运行
                升级路径
                    smtxos515 到 smtxos620u1 （tl3）vGPU
    功能测试
        ethtool 调整网卡参数的测试
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