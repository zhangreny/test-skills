Tower SRE
    Tower 安装部署
        fisheye rpm
            5.1.5
                UI installer 新增前置鉴权
                    访问 https://SMTX_ManageIP_Address/operation-center-installer - IP 无效，页面无法加载
                    访问 https://SMTX_ManageIP_Address/operation-center-installer - IP 对应的集群版本不满足要求，页面提示缺少参数
                    访问 https://SMTX_ManageIP_Address/operation-center-installer - IP 非集群 IP，页面无法加载
                    访问 https://SMTX_ManageIP_Address/operation-center-installer - IP 对应的集群版本为 5.1.5 及以上，展示鉴权页面
                    鉴权页面 - 提示语、输入字段 与 UI 设计稿一致
                    鉴权页面 - 集群超级管理员用户名为空，点击下一步，输入框标红下方报错 ”请填写超级管理员用户名。“
                    鉴权页面 - 集群超级管理员密码为空，点击下一步，输入框标红下方报错 ”请填写超级管理员密码。“
                    鉴权页面 - 用户名或密码填写错误，点击下一步，页面报错 “用户名或密码错误。”
                    鉴权页面 - 密码填写后，打点加密展示
                    鉴权页面 - 用户名和密码均填写正确，点击下一步，集群启用 Boost，跳转至关联 CloudTower 页面
                    鉴权页面 - 用户名和密码均填写正确，点击下一步，集群未启用 Boost，跳转至关联 CloudTower 页面
                    鉴权页面 - 用户名和密码均填写正确，点击下一步，API 中的密码加密展示
                    关联 CloudTower 页面 - 部署全新的 CloudTower 并将集群关联成功
                    关联 CloudTower 页面 - 将集群关联至已有的 CloudTower 成功
                    切换语言 - 鉴权页面的提示语、字段、报错提示，正常翻译为英文
                    安装进度页面 - 安装报错，点击返回配置步骤页面，正常返回关联 CloudTower 页面
                    集群部署完成，跳转至关联 CloudTower 页面 - 集群 fisheye rpm 符合预期，展示鉴权页面
                    集群部署完成，跳转至关联 CloudTower 页面 - 集群 fisheye rpm 不符合预期，展示关联 CloudTower 页面
                    浏览器兼容 - Safari、Google、Firefox 均可通过正确的 URL 访问鉴权页面
                    集群版本测试 - SMTX OS 5.1.5 及以上、fisheye rpm 版本不符合预期的集群
                    集群 CPU 架构测试 - Intel x86_64、oe x86_64、Arrch64
                    集群是否启用 Boost 测试 - 已启用、未启用
                    集群计算平台 - ELF、VMware ESXi
    Tower 应用 CAPP & SCOS
        460 调整默认副本数为 3，精简置备
            低版本部署的 agent mesh 服务，CAPP 升级后，检查 instance 中的 storageReplicas 设置为 2
            低版本部署 agent mesh 服务，CAPP 升级后，能升级 agent mesh 成功，副本数为 2
            低版本部署的可观测服务，CAPP 升级后，检查 instance 中的 storageReplicas 设置为 2
            低版本部署可观测服务，CAPP 升级后，能升级可观测成功，副本数为 2
            低版本部署的备份服务，CAPP 升级后，检查 instance 中的 storageReplicas 设置为 2
            低版本部署备份服务，CAPP 升级后，能升级备份服务成功，副本数为 2
            低版本部署的 SKS 服务，CAPP 升级后，检查 registry instance 中的 storageReplicas 设置为 2
            低版本部署 SKS 服务，CAPP 升级后，能升级 SKS 成功，副本数为 2
            低版本部署 SKS 服务，CAPP 升级后，能提升 SKS 成功，新提升的节点副本数为 2
            低版本部署的 SFS 服务，CAPP 升级后，检查不改写 SFS controller instance 中 storageReplicas:2
            低版本部署 SFS 服务，CAPP 升级后，能升级 SFS 成功
            CAPP 1.6.1，新部署 agent mesh，检查副本数为 3
            新部署的 3 副本 agent mesh 升级成功
            CAPP 1.6.1，新部署 备份服务，检查副本数为 3
            新部署的3副本备份服务升级成功
            CAPP 1.6.1，新部署可观测，检查副本数为 3
            新部署的3副本可观测服务升级成功
            CAPP 1.6.1，新部署 SKS，检查 registry 副本数为 3
            新部署的3副本 SKS 升级成功
            CAPP 1.6.1，新部署 SFS，检查 SFS controller instance 副本数为 2
            新部署的 SFS 服务升级成功，副本数不变
            新部署的系统服务，在集群一键提升副本处，都无需再提升
            低版本部署的 agent mesh 服务，通过集群一键提升副本到 3，然后 CAPP 升级到 1.6.1，检查不会设置  instance 中的 storageReplicas 为 2
            低版本部署的 agent mesh 服务，通过集群一键提升副本到 3，然后 CAPP 升级到 1.6.1，对 agent mesh 升级成功
            低版本部署的可观测服务，通过集群一键提升副本到 3，然后 CAPP 升级到 1.6.1，检查不会设置  instance 中的 storageReplicas 为 2
            低版本部署的可观测服务，通过集群一键提升副本到 3，然后 CAPP 升级到 1.6.1，升级可观测能成功
            低版本部署的 SKS 服务，通过集群一键提升副本到 3，然后 CAPP 升级到 1.6.1，检查不会设置  instance 中的 storageReplicas 为 2
            低版本部署的 SKS 服务，通过集群一键提升副本到 3，然后 CAPP 升级到 1.6.1，升级 SKS 能成功
            低版本部署的复制服务，通过集群一键提升副本到 3，然后 CAPP 升级到 1.6.1，检查不会设置  instance 中的 storageReplicas 为 2
            低版本部署的复制服务，通过集群一键提升副本到 3，然后 CAPP 升级到 1.6.1，升级 SKS 能成功
        CAPP 支持自定义 SSH 端口
            不传入任何层级的端口设置，默认创建 22 为 ssh 端口的系统服务
            检查默认 22 端口的系统服务监控状态正常
            检查默认 22 端口的系统服务升级成功
            在 template 层级设置自定义端口，创建系统服务成功
            自定义 template 层级端口的系统服务监控状态正常
            自定义端口的系统服务升级成功，升级后检查配置正确
            在 instance 层级设置自定义端口，创建系统服务成功
            自定义 instance 层级端口的系统服务监控状态正常
            自定义端口的系统服务升级成功，升级后检查 instance 配置正确
            instance 的配置能覆盖 template 层级的配置
            在 template 层级指定 ssh 端口，部署系统服务，然后修改 ssh 端口配置
            在 instance 层级指定 ssh 端口，部署的系统服务，然后修改 ssh 端口配置
            自定义端口系统服务，检查 ssh 服务正常
            多实例的，template 指定自定义 ssh 端口，创建系统服务
            多实例的，template 指定自定义 ssh 端口，创建系统服务，然后修改 template 端口配置
            多实例的，template 指定自定义 ssh 端口，创建系统服务，然后修改每个实例为不同的端口配置
            多实例的，template 层级指定自定义 ssh 端口，系统服务升级
            多实例的，instance 层级指定自定义 ssh 端口，创建系统服务
            多实例的，instance 层级指定自定义 ssh 端口，修改 instance 的配置
            多实例的，instance 层级指定自定义 ssh 端口，系统服务升级
            多实例，instance 层级的 ssh 端口配置能覆盖 template 的配置，创建系统服务
            多实例，instance 层级的 ssh 端口配置能覆盖 template 的配置，修改 instance 层级的端口配置
    Tower - 4.6.0 调整
        TOWER-16748 tower 备份及重建
            4.6.0 installer 实现备份和重建
                在原 tower 部署除「可观测性平台」以外的其他系统服务，执行备份时预期失败，指定 --force 可以进行强制备份
                备份前，tower 部署有 SKS 服务，sks 容器镜像仓库为自签名证书。在备份 tower 执行重建，预期 SKS 相关 pod 无法恢复，因为备份 tower 虚拟机系统内没有安装 sks 容器镜像仓库的 CA 证书，containerd 没有此证书设置
                重建后的 tower，页面上操作 cloudtower 升级，能够顺利完成
                重建后的 tower，/var/lib/smartx 目录下的 ssh 密钥和容器镜像不会丢失
                重建 tower 需要和原 tower ip 地址完全相同，重建 tower 虚拟机开机后，需要将原 tower 关机
                原 tower k8s 上安装 cloudtower-alpha，metrics-server 或其他三方应用，不会备份这些应用的镜像
                原 tower 虚拟机上安装其他三方软件，自定义 systemd unit 配置，不会备份上述内容
                原 tower 上人为更新过 scos ova，会备份最新的 ova 并顺利重建
                原 tower 上发生过升级中心自升级，随后备份，执行重建后，是以 ISO  中的配置启动升级中心
                执行备份指令时，ctrl+c 强制退出，可以重新执行备份命令且顺利完成
                执行恢复命令时，ctrl+c  强制退出，可以重新执行恢复命令且顺利完成
                禁止使用 tmpfs 目录存储备份文件
                在原 tower 备份时，如果指定目录所在的文件系统使用量超过 50%，不允许备份
                在新 tower 恢复时，如果根目录文件系统使用量超过 50%，不允许恢复
                在原 tower 备份时，如果根目录所在文件系统使用量超过 50%，但是 --dir 指定的目录所在文件系统内剩余空间充足，允许备份
                备份时指定备份文件名称中有特殊字符，使用该文件重建时，能够顺利完成
                重建时能够顺利到正确的 postgresql 转储的 sql
                原虚拟机部署有 cloudtower-alpha 及第三方应用，执行备份后在新虚拟机重建，流程可以顺利完成
                重建之后，重启一次 tower 机器，重启后各 pod 正常恢复，troubleshooter 诊断无失败项
        TOWER-16841 Tower 支持 UI 升级
            事件审计
                分别从本地和 url 上传文件，「上传 CloudTower 升级文件」描述信息中，会区分上传方式
                点击「检查环境」按钮，产生「升级前预检查」用户审计事件，即使有检查不通过项，事件审计状态为成功
            tower 任务
                发起升级后，产生 Tower 任务「将 CloudTower 从版本 xxx 升级至 xxx」，任务卡片展示当前所处阶段，有访问独立升级页的超链接
            命令行升级
                小于 4.6.0 的低版本升级到 tower 4.6.0，需要通过命令行升级
                小于 4.6.0 的低版本直接升级 tower 4.6.0 以上版本，需要通过命令行升级
                当前 tower 是 4.6.0，使用 4.6.0 升级文件进行命令行升级可以完成，再进行界面升级可以完成。即支持同版本升级
                当前 tower 是 4.6.0，可以使用 4.6.0及 以上版本的升级文件进行命令行升级
            界面操作
                上传升级文件
                    URL 上传，点击上传按钮后，如果文件扩展名不是 .tar.gz，footer 显示文件扩展名提示。--不再适用，前端输入框需要 .tar.gz 和 .json 结尾
                    上传完升级文件后，「本地上传」和「URL 上传」将不再展示
                    多个浏览器标签页访问 tower，选择好文件后，同时点击「上传」按钮，只会产生一个上传任务，其他的直接报错
                    url 上传，launcherd 下载文件过程中中断，任务失败，产生失败的事件审计
                删除升级文件
                    上传完升级文件后，无法再上传升级文件，从页面删除升级文件后，页面上显示上传文件组件
                独立预检查
                    独立预检查失败时，「升级」无法点击，只有当最近一次独立预检查所有检查项均通过时，「升级」按钮可点击
                    多个浏览器标签页同时点击「检查环境」按钮，独立返回结果不会冲突
                    CloudTower Pods 未处于运行中状态，展示未满足
                    目标版本低于当前版本，展示未满足
                    IO 检查不通过，展示未满足
                    CloudTower 虚拟机的容量规格不符合要求，展示未满足
                    空间不足，独立预检查失败，展示错误提示
                    目标 CPU 架构、操作系统与当前 CloudTower 不一致，展示未满足
                    k9s 进程检查冲突，展示错误提示
                升级
                    当升级文件文件上传完毕后，出现「升级」按钮，此时可以点击「升级」触发升级
                    如果进行过「独立预检查」，需要最近一次「独立预检查」所有检查项均通过，「升级」按钮才可点击
                    多个浏览器标签页同时点击「升级」按钮并在二次确认，只有一个能够发起
                    发起升级操作之后，不再展示在此之前的预检查结果
                升级记录
                    「系统配置 > CloudTower 升级」存在「升级记录」TAB 页
                独立升级页
                    「升级中」进度页，存在「打开 cloudtower」按钮，点击后在新标签页访问 tower overview 页面
            API 操作
                上传升级文件
                    升级文件 MD5 校验失败，上传失败
                其他
                    发起多个升级任务，重复的任务会失败
            场景
                先在界面上发起 cloudtower 升级，已经通过预检查进行到正式升级步骤，此时发起命令行升级
                先在 tower 虚拟机系统内发起命令行升级，此时在界面上发起 cloudtower 升级
                当前是 4.6.0，使用 4.7.0 的全量升级包进行升级，携带的内核 rpm 版本变化
                先在 tower 虚拟机系统内执行 instaler update，随后在界面上发起 cloudtower 升级
                先在界面上发起 cloudtower 升级，随后在 tower 虚拟机系统内执行 installer update
                在界面上发起 cloudtower 升级后，操作 tower 虚拟机重启，等待 tower server 恢复后，确认 tower 任务、事件审计、升级记录、独立升级页的显示
                在界面上发起 cloudtower 升级后，操作 tower 虚拟机强制关机，开机后等待 tower server 恢复后，确认 tower 任务、事件审计、升级记录、独立升级页的显示
                在界面上发起 cloudtower 升级后，操作 tower 虚拟机发生 HA，开机后等待 tower server 恢复后，确认 tower 任务、事件审计、升级记录、独立升级页的显示
                cloudtower 升级流程有内核升级步骤，自动重启，在 launcherd 和 tower server 都无法提供服务时，刷新独立升级页
                cloudtower 升级流程中有内核升级步骤，自动重启，在 launcherd 能提供服务但 tower server 未就绪时，分别访问 tower 和独立升级页
                系统预检查失败，升级任务失败，检查升级结果和升级页面
                解压升级文件失败，升级任务失败，检查升级结果和升级页面
                升级 launcherd 失败，升级任务失败，检查升级结果和升级页面
                升级内核失败，升级任务失败，检查升级结果和升级页面
                等待环境就绪失败，升级任务失败，检查升级结果和升级页面
                服务部署失败，升级任务失败，检查升级结果和升级页面
                应用部署失败，升级任务失败，检查升级结果和升级页面
                清理临时文件失败，升级任务失败，检查升级结果和升级页面
                触发升级后，launcherd 有重启，检查任务能正常结束
                升级完成后，清理升级文件失败，不影响升级成功的结果
        集群一键提升副本数兼容系统服务 -- abandon
            不同环境覆盖
                Tower 覆盖
                AOC 覆盖
            SMTX OS 一键提升集群副本
                一键提升入口页面
                    集群中存在 1 副本业务虚拟机卷，页面提示：该集群内存在 1 副本的虚拟卷，数据丢失风险较高，请尽快提升其副本数。
                    集群中存在 1 副本和 2 副本业务虚拟机卷，页面提示：该集群内存在 1 副本的虚拟卷，数据丢失风险较高，请尽快提升其副本数。
                    集群有 NFS 虚拟卷 1/2副本，触发展示灰色提示信息：部分虚拟卷不支持提升副本数，一键提升时将会被跳过。鼠标 hover 详情里显示「NFS虚拟卷」。
                    集群有可观测虚拟机 2副本，触发展示灰色提示信息：部分虚拟卷不支持提升副本数，一键提升时将会被跳过。鼠标 hover 详情里显示「可观测性虚拟机的虚拟机卷」。
                    集群有 SFS 虚拟机 2副本，触发展示灰色提示信息：部分虚拟卷不支持提升副本数，一键提升时将会被跳过。鼠标 hover 详情里显示「文件控制器系统盘，文件系统对应虚拟卷」。
                    集群有 1.4 以下的 SKS 虚拟机 2副本，触发展示灰色提示信息：部分虚拟卷不支持提升副本数，一键提升时将会被跳过。鼠标 hover 详情里显示「通过 CSI 创建的虚拟卷」。
                    集群里有上面的多个系统服务虚拟机 2 副本，鼠标 hover 时的列表详情正确。
                    集群有 1.4 的 SKS 虚拟机 2副本，不触发展示灰色提示信息：部分虚拟卷不支持提升副本数，一键提升时将会被跳过。
                    有 agent-mesh 虚拟机 2副本，不触发展示灰色提示信息：部分虚拟卷不支持提升副本数，一键提升时将会被跳过。
                    集群有 备份虚拟机 2副本，不触发展示灰色提示信息：部分虚拟卷不支持提升副本数，一键提升时将会被跳过。
                    集群有 ER 虚拟机 2副本，不触发展示灰色提示信息：部分虚拟卷不支持提升副本数，一键提升时将会被跳过。
                    除开可观测和 SFS，所有的业务虚拟机，agent-mesh，备份，SKS 允许提升的卷都已经为 3副本，展示无虚拟卷的副本数可提升
                    所有的业务虚拟机 3 副本，但存在 2 副本的 agent mesh，不展示无虚拟卷的副本数可提升
                    所有的业务虚拟机 3 副本，但存在 2 副本的 备份服务虚拟卷，不展示无虚拟卷的副本数可提升
                    所有的业务虚拟机 3 副本，但存在 2 副本的 SKS 管控面虚拟卷，不展示无虚拟卷的副本数可提升
                    系统服务都不可提升了，但是存在业务虚拟机可提升，不展示无虚拟卷的副本数可提升
                一键提升操作弹框
                    2 副本可观测系统服务虚拟卷，触发提示：不包含如下虚拟卷: 可观测性虚拟机的虚拟卷
                    2 副本 SFS 虚拟卷，触发提示：不包含如下虚拟卷: 文件控制器系统盘，文件系统对应的虚拟卷
                    2副本 1.4 以下 SKS，触发提示：不包含如下虚拟卷: 通过 CSI 创建的 PV 卷
                    NFS 虚拟卷触发提示：不包含如下虚拟卷：NFS 虚拟卷
                    如果需要提升的副本会造成常驻缓存预留容量不足，提交时展示错误文案： 集群常驻缓存预留容量不足。预计额外需要 XX.XX GiB 的预留缓存容量。
                集群直接提升副本数
                    一键提升时，1/2 副本的业务虚拟卷直接提升
                    一键提升时， ER 的虚拟卷直接提升，我会联系 wenfei 帮忙确认提升的正确性，提升后服务的可用性
                    更多业务虚拟卷提升场景，jinrui 姐他们做基础回归
                    tower 虚拟机跟随集群提升副本数，检查提升后运维操作正常
                    tower 虚拟机跟随集群提升副本数，检查提升后使用正常
                    回收站中的业务虚拟卷会直接提升
                    正在提升的虚拟卷 entityAsyncStatus 会被标记为 UPDATING，提升完后恢复正常
                系统服务相关虚拟卷的特殊处理
                    一键提升时，跳过 SFS 文件控制器系统盘，不做提升
                    一键提升时，跳过  SFS 存储集群中的虚拟卷，不做提升
                    一键提升时，跳过可观测虚拟机卷，不做提升
                    SKS 测试参考 http://testrail.smartx.com/index.php?/suites/view/442&group_by=cases:section_id&group_order=asc&display_deleted_cases=0&group_id=321063
                    备份测试参考 http://testrail.smartx.com/index.php?/suites/view/271&group_by=cases:section_id&group_order=asc&display_deleted_cases=0&group_id=321625
                    已经卸载的系统服务，虚拟卷进入回收站，会当做普通卷直接提升
                    agent mesh 通过集群一键提升副本数
                        x86 部署，一键提升副本数成功
                        x86 部署，提升副本数之后升级检查
                        ARM 部署，一键提升副本数成功
                        ARM 部署，一键提升副本数后升级检查
                        提升副本数成功后，再次一键提升集群副本，会跳过此 agent mesh 虚拟卷
                        集群存储空间不够，触发一键提升集群副本，agent mesh 副本提升，虚拟机处于数据恢复中
                        agent mesh 提升副本之后，回归基本功能
                        460 版本以前，集群做过一键提升副本数，升级到 460 后会视为 3 副本，不能再得到提升
                        卸载提升过副本的 agent mesh 成功
                        在一键提升副本的集群上，新部署 agent mesh，检查功能正常
            ELF+ZBS 提升副本数
                ELF 集群内没有系统服务，有可提升副本数的虚拟卷，「提升副本数」按钮可用
                ELF 集群内有未提升的 ER 服务，没有可提升副本数的虚拟卷，「提升副本数」按钮可用，提升 ER 的副本数能成功
                ELF 集群内 ER 和业务虚拟机卷均不可再提升，禁用「提升副本数」按钮，mouser hover 展示提示信息：无虚拟卷的副本数可提升
                ELF 集群内 ER 和业务虚拟机卷均不可再提升，部署可观测服务，检查禁用「提升副本数」按钮，mouser hover 展示提示信息：无虚拟卷的副本数可提升(不支持提升可观测性副本数)
                ELF 集群内 ER 和业务虚拟机卷均不可再提升，部署可观测服务和 agent-mesh，「提升副本数」按钮可用，触发 agent-mesh 提升副本成功
                ELF 集群内 ER、agent-mesh 和业务虚拟机卷均不可再提升，部署可观测服务，检查禁用「提升副本数」按钮，mouser hover 展示提示信息：无虚拟卷的副本数可提升(不支持提升可观测性副本数)
                ELF 集群内 ER 和业务虚拟机卷均不可再提升，部署可观测服务，创建 NFS 卷，检查禁用「提升副本数」按钮，mouser hover 展示提示信息：无虚拟卷的副本数可提升(不支持提升可观测性、NFS 卷副本数)
                一键提升操作弹框
                    2 副本可观测系统服务虚拟卷，触发提示：不包含如下虚拟卷: 可观测性虚拟机的虚拟卷
                    NFS 虚拟卷触发提示：不包含如下虚拟卷：NFS 虚拟卷
                    如果需要提升的副本会造成常驻缓存预留容量不足，提交时展示错误文案： 集群常驻缓存预留容量不足。预计额外需要 XX.XX GiB 的预留缓存容量。
            OAPI 检查
                通过 OAPI 传入可观测性服务虚拟卷 id，预期报错，不能提升
                通过 OAPI 传入 sfs 服务虚拟卷 id，预期报错，不能提升
                通过 OAPI 传入 SKS 1.4 以下 CSI 创建的虚拟卷 id，预期报错，不能提升
                通过 OAPI 传入 agent-mesh，SKS registry，SKS 1.4 以上 CSI创建的虚拟卷，备份服务，ER，2副本业务虚拟卷 id，预期正确提升
        TOWER-17464 备份、恢复 etcd 脚本
            centos7.x86_64 ISO 部署 tower，执行 etcd 备份及恢复顺利完成
            oe2003.x86_64 ISO 部署 tower，执行 etcd 备份及恢复顺利完成
            oe2003.aarch64 ISO 部署 tower，执行 etcd 备份及恢复顺利完成
            centos7.x86_64 cloudtower-installer 部署 tower，执行 etcd 备份及恢复顺利完成
            oe2003.x86_64 cloudtower-installer 部署 tower，执行 etcd 备份及恢复顺利完成
            oe2003.aarch64 cloudtower-installer 部署 tower，执行 etcd 备份及恢复顺利完成
            任意历史版本升级到当前支持备份恢复脚本的版本，执行 etcd 备份及恢复顺利完成
            部署完毕后，/usr/local/bin 目录下存在 backup-etcd.sh 和 restore-etcd.sh，内容符合预期，权限为 755
            部署完毕后，/etc/cron.d 目录下存在 backup-etcd 文件，内容是 0 2 * * * root /usr/local/bin/backup-etcd.sh
            每天凌晨两点，执行  etcd 备份，在 /usr/share/{vendor}/backup/etcd 目录下产生 snapshot_$TIMESTAMP.db
            备份 etcd 的日志记录在 /var/log/backup-etcd.log
            每天凌晨2点完成 etcd 备份后，删除旧文件，保留最新的7份 snapshot 文件
            无法直接执行 ctr 命令，备份脚本记录错误后结束
            没有 /etc/kubernetes/pki/etcd/ca.crt 文件时，备份脚本记录错误后结束
            没有 etcd 容器镜像时，备份脚本记录错误后结束
            containerd 未运行，备份脚本执行预期会失败
            手动执行备份脚本时，不是以 root 账户执行脚本，预期会失败
            etcd 当前已经故障，如 wal crc mismatch，定时备份失败，不会产生新的 snapshot 文件，也不会执行旧文件清理逻辑
            给 tower 虚拟机盘注入 io 延迟，执行备份脚本，预期会失败
            备份过程中 tower 虚拟机关机，可能产生不可用的 snapshot，文件扩展名为 .part，无法用于恢复。开机后 ，再次备份能顺利完成
            自动备份开始后，又手动执行 backup-etcd.sh，两个备份过程独立，均能顺利完成
            恰好在 tower 虚拟机系统启动过程中，定时执行触发，可能无法顺利备份（containerd 未就绪）
            手动执行backup-etcd脚本，执行过程中 ctr+c 中断，可能产生扩展名为 .part 的文件。再次执行备份，能够顺利完成
            不完整备份产生的 .part 文件不会被自动清理
            在两个终端先后手动执行 backup-etcd 脚本，预期都能顺利完成
            执行备份脚本时，tower 虚拟机恰好发生集群内热迁移，备份可以顺利完成，迁移可以顺利完成
            执行备份脚本时，tower 虚拟机恰好发生跨集群热迁移，备份可以顺利完成，迁移可以顺利完成
            执行备份脚本时，tower 虚拟机恰好被暂停，预期会失败
            当前 etcd 是正常运行状态，执行恢复脚本，可以顺利完成
            当前 etcd 无法正常工作，例如没有 etcd 容器，或 wal crc mismatch，或 can't get reachable pages，使用 snapshot 恢复，可以顺利完成，etcd 能够恢复
            执行恢复脚本，无日志文件记录
            执行恢复脚本时，未指定参数会提示用法
            执行恢复脚本时，指定的 snapshot 文件实际不存在，输出错误后结束
            执行恢复脚本时，不是以 root 账户执行，输出错误后结束
            执行恢复脚本前，构造无运行中状态或退出状态的 etcd 容器，可以顺利完成恢复
            无法直接执行 ctr 命令，执行恢复脚本，输出错误后结束
            无法直接执行 crictl 命令，执行恢复脚本，输出错误后结束
            /etc/kubernetes/pki/etcd/ca.crt 不存在，执行恢复脚本，输出错误后结束
            没有 etcd 镜像，执行恢复脚本，输出错误后结束
            执行恢复脚本，还未运行到 etcdctl snapshot restore 时，ctr+z 终止，再次执行，可以顺利完成
            执行恢复脚本，执行 etcdctl snapshot restore 过程中，ctrl +z 终止，再次执行，可以顺利完成
            执行恢复脚本，指定的文件路径不是 .db 后缀的 etcd snapshot 文件，在 etcdctl snapshot restore 阶段失败
            执行恢复脚本，指定的文件是 .db 后缀的 etcd snapshot 文件但实际不完整，在 etcdctl snapshot restore 阶段失败
            在两个终端同时执行恢复脚本，预期会失败
            在两个终端同时执行备份脚本和恢复脚本，各自独立完成
            给 tower 虚拟机盘注入 io 延迟，随后执行恢复脚本，有可能失败
            执行恢复脚本，执行到 etcdctl snapshot restore 时强制关机虚拟机，开机后，再次执行恢复脚本能够顺利完成
            执行恢复脚本过程中，tower 虚拟机发生集群内热迁移，可以顺利完成
            执行恢复脚本过程中，tower 虚拟机发生跨集群热迁移，恢复可以顺利完成，迁移可以顺利完成
            执行恢复脚本过程中，tower 虚拟机被暂停，预期恢复失败
            使用一个无效的 snapshot 恢复，恢复失败。再使用一个有效的 snapshot 恢复，可以顺利完成
        TOWER-17254 集群一键提升副本数兼容系统服务
            SMTX OS 集群
                在副本数提升的页面增加提示信息 "提升范围：用户创建的虚拟卷以及 CloudTower 虚拟机的虚拟卷"
                一键提升弹框增加提示信息 "提升范围：用户创建的虚拟卷以及 CloudTower 虚拟机的虚拟卷"
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，排除 可观测服务虚拟卷
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，排除 agent mesh 虚拟卷
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，排除 备份复制服务 虚拟卷
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，排除 ER 虚拟卷
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，排除 SFS 虚拟卷
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，排除 SKS 服务管控面虚拟卷
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，排除 SKS 工作负载集群虚拟卷
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，排除 SKS CSI 创建的虚拟卷
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，排除高级监控的虚拟卷
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，包含  Tower 虚拟机的虚拟卷
                触发集群一键提升副本数，2 副本的可观测性服务虚拟卷不会被提升
                集群一键提升副本数之后，再对可观测服务做运维升级能成功
                触发集群一键提升副本数，2 副本的 agent mesh 虚拟卷不会被提升
                集群一键提升副本数之后，再对 agent mesh 做运维升级能成功
                触发集群一键提升副本数，2 副本的 ER 虚拟卷不会被提升
                集群一键提升副本数之后，再对 ER 做运维升级能成功
                触发集群一键提升副本数，2 副本的 备份复制服务 虚拟卷不会被提升
                集群一键提升副本数之后，再对 备份复制服务 做运维升级能成功
                触发集群一键提升副本数，2 副本的 SFS 服务管控面虚拟卷不会被提升
                集群一键提升副本数之后，再对 SFS 做运维升级能成功
                触发集群一键提升副本数，2 副本的 SKS 服务管控面虚拟卷不会被提升
                触发集群一键提升副本数，2 副本的 SKS 工作负载集群虚拟卷不会被提升
                触发集群一键提升副本数，2 副本的 SKS CSI 虚拟卷不会被提升
                集群一键提升副本数之后，再对 SKS 做运维升级能成功
                触发集群一键提升副本数，2 副本的 高级监控虚拟卷不会被提升
                集群一键提升副本数之后，再对 高级监控 做运维升级能成功
                触发集群一键提升副本数，2 副本的 Tower 虚拟卷会被提升
                集群一键提升副本数之后，再对 Tower 做运维升级，磁盘扩容能成功
                触发集群一键提升副本数，2 副本的用户业务虚拟卷会被提升
                触发集群一键提升副本数，没有挂载给虚拟机的 2 副本虚拟卷会被提升
                提交一键提升副本数，如果集群有开启常驻缓存，并且当前需要提升的 Tower 虚拟卷和用户业务虚拟卷超过常驻缓存预留容量，就报错提示 “集群常驻缓存预留容量不足。预计额外需要 XX.XX GB 的预留缓存容量。”
                检查英文版页面提示信息，触发提升时的常驻缓存提示信息
                通过 API 直接提升 2 副本的可观测性服务虚拟卷，API 返回错误信息，不会做提升
                通过 API 直接提升 2 副本的 ER 服务虚拟卷，API 返回错误信息，不会做提升
                通过 API 直接提升 2 副本的复制备份服务虚拟卷，API 返回错误信息，不会做提升
                通过 API 直接提升 2 副本的 agent mesh 虚拟卷，API 返回错误信息，不会做提升
                通过 API 直接提升 2 副本的 SKS 管控面虚拟卷，API 返回错误信息，不会做提升
                通过 API 直接提升 2 副本的 SKS 工作负载虚拟卷，API 返回错误信息，不会做提升
                通过 API 直接提升 2 副本的 SKS CSI 虚拟卷，API 返回错误信息，不会做提升
                通过 API 直接提升 2 副本的 SFS 虚拟卷，API 返回错误信息，不会做提升
                通过 API 直接提升 2 副本的高级监控 虚拟卷，API 返回错误信息，不会做提升
                系统服务卸载后放入回收站，相关虚拟卷在集群一键提升时会被提升
                虚拟卷从系统服务上卸载后，如果相应的标识被去掉了，则能被一键提升
                虚拟卷从系统服务上卸载后，如果相应的标识仍然保持了，不能被一键提升，比如：SFS shard/ SKS  pvc
            SMTX ELF 集群关联存储
                一键提升弹框，增加提示信息 "提升范围：用户创建的虚拟卷以及 CloudTower 虚拟机的虚拟卷"
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，排除 可观测服务虚拟卷
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，排除 agent mesh 虚拟卷
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，排除 ER 虚拟卷
                一键提升弹框，待提升的 2 副本虚拟卷副本数统计，包含  Tower 虚拟机的虚拟卷
                触发关联存储一键提升副本数，2 副本的可观测性服务虚拟卷不会被提升
                一键提升副本数之后，再对可观测服务做运维升级能成功
                触发关联存储一键提升副本数，2 副本的 agent mesh 虚拟卷不会被提升
                一键提升副本数之后，再对 agent mesh 做运维升级能成功
                触发关联存储一键提升副本数，2 副本的 Tower 虚拟卷会被提升
                一键提升副本数之后，再对 Tower 做运维升级能成功
                触发关联存储一键提升副本数，2 副本的 ER 虚拟卷不会被提升
                一键提升副本数之后，再对 ER 做运维升级能成功
                触发关联存储一键提升副本数，2 副本的用户业务虚拟卷会被提升
                触发关联存储一键提升副本数，没有挂载给虚拟机的 2 副本虚拟卷会被提升
                检查英文版页面提示信息
                通过 API 直接提升 2 副本的可观测性服务虚拟卷，API 返回错误信息，不会做提升
                通过 API 直接提升 2 副本的 ER 服务虚拟卷，API 返回错误信息，不会做提升
                通过 API 直接提升 2 副本的 agent mesh 虚拟卷，API 返回错误信息，不会做提升
    tencentos 发行版
        4.4.1
            创建新虚拟机，挂载 ISO 部署，部署顺利完成
            使用 cloudtower-installer 部署顺利完成
            在 tencentos SMTX OS 集群中部署顺利完成
            在 非 tencentos SMTX OS 集群中部署顺利完成
            在 SMTXOS 、SMTX ELF、SMTX ZBS、VMware 各类集群中部署顺利完成
            机器重启后，tower k8s 环境正常恢复，pod 均就绪
            执行 installer update 顺利完成
            修改 tower 虚拟机 ip 后，执行 installer update-ip 顺利完成
            部署后使用当前版本的升级文件升级，顺利完成
            部署后使用当前版本的其他系统发行版、其他架构的升级文件升级，预期会失败
            执行 installer renew-certs 可以顺利完成
    tower 虚拟机配置多网卡
        ISO 部署，在创建虚拟机时设置两张同虚拟机网络的网卡。安装系统后为第二张网卡配置 ip 和路由，确保两个 ip 均能访问。部署顺利完成，可以使用两个 IP  访问 tower
        ISO 部署，在创建虚拟机时设置两张不同虚拟机网络的网卡。安装系统后为第二张网卡配置 ip 和路由，确保两个 ip 均能访问。部署顺利完成，可以使用两个 IP 访问 tower
        已经部署好的 tower，新增一张网卡，配置 ip，调整必要内核参数，确保两个 ip 均能访问 tower，关闭或删除原网卡，可以用新网卡 ip 访问 tower
    TOWER - 4.4.3,4.6.2 调整
        TOWER-19294, TOWER-19318 检查
            检查  temporal helm charts，TEMPORAL_ADDRESS 环境变量有 passthrough:/// 前缀
            检查 temporal-admintools  pod 中容器环境变量，TEMPORAL_ADDRESS 的值有 passthrough:/// 前缀
            检查 temporal-schema pod 中容器环境变量，TEMPORAL_ADDRESS 的值有 passthrough:/// 前缀
            /etc/resolv.conf 设置 nameserver 为单个内网 dns 服务器，coredns 开启转发插件，制造 dns 服务器无法响应，重启一次 coredns 和 node-local-dns，重装 temporal helm release，预期可以顺利完成
            /etc/resolv.conf 设置 nameserver 为单个内网 dns 服务器，coredns 开启转发，制造 dns 服务器无法响应，重装 01 开始的所有应用，预期均能顺利完成
            /etc/resolv.conf 设置 nameserver 为单个内网 dns 服务器，coredns 开启转发，制造 dns 服务器无法响应。在页面升级中心操作一次集群升级，可以顺利完成，在 /debug/teporal/namespaces/upgrade-center 查看 workflows，都应正常完成
            /etc/resolv.conf 设置 nameserver 为单个内网 dns 服务器，coredns 开启转发，制造 dns 服务器无法响应。在页面集群节点列表操作一次节点角色转换，可以顺利完成，在 /debug/teporal/namespaces/lcm-manager 查看 workflows，都应正常完成
            /etc/resolv.conf 设置 nameserver 为单个内网 dns 服务器，coredns 开启转发，制造 dns 服务器无法响应。在页面操作虚拟机跨集群迁移，可以顺利完成，在 /debug/teporal/namespaces/default 查看 workflows，都应正常完成
            部署 tower 前，设置 resolv.conf 文件中 nameserver 为多个有效公网 dns，部署顺利完成
            部署 tower 前，设置 resolv.conf 文件中 nameserver 为 ipv6 地址，预期安装应用 00 阶段，coredns 不会开启转发插件
            部署 tower 前，设置 resolv.conf 文件中 nameserver 为非 ipv4 格式地址，预期安装应用 00 阶段，coredns 不会开启转发插件
            部署 tower 前，设置 resolv.conf 文件中同时包含有效的 nameserver 和格式错误的 nameserver，预期安装应用 00 阶段，coredns 不会开启转发插件
            部署 tower 前，设置 resolv.conf 文件中 nameserver 为 127.0.0.1，nslookup 不存在域名预期响应 connection refused 字样，coredns 不会开启转发插件
            cloudtower-installer 部署 tower，为 tower 设置不受限的 ip 地址，部署顺利完成
            cloudtower-installer 部署 tower，为 tower 设置受 ACL 规则限制的 ip 地址，无法访问公网，无法访问内网 dns server，部署顺利完成
            installer nameserver set --values 变更 reslov.conf 的 nameserver 时，会校验数量不超过3个，格式为 ipv4
            installer deploy/rebuild/update/update-ip 等命令均根据 /etc/resolv.conf 的实际 nameserver 确定 coredns 是否开启转发插件，并将有效的 nameserver 配置写入 /root/.config/tower.yaml
    tower - 4.7.0 调整
        TOWER-18407 UI 升级优化
            升级到 4.7.0 后，选择4.6.0版本升级文件和元数据文件，元数据检查不通过
            执行 installer update-ip，会重启 launcherd，访问「CloudTower 升级」页面，deploy API 正常响应
            独立升级页登录 API，payload 中密码为密文
            页面上统一术语，使用「升级文件」
            windows/linux/mac 三种操作系统，chrome/firefox/safari 等浏览器，访问独立升级页查看日志查看器 xterm ，支持 ctrl + a 全选，ctrl + c 复制，按行/按页滚动页面
            本地上传升级文件时，launcherd 重启，已上传分块会在 24 小时后被清理
            url 上传升级文件时，断开 launcherd 和远端的连接，临时下载文件会在 24 小时（最差情况为48小时）后被清理
            SQLite 迁移到 PostgreSQL
                全新部署 tower 4.7.0，launcherd 启动时，在 postgresql 创建迁移记录表和bundle等表，设置迁移状态为完成
                4.6.1 未进行过页面升级，sqlite 各表没有记录。使用命令行升级到 4.7.0，升级过程中，在 launcherd 重新启动时迁移到 postgresql，升级顺利完成
                4.6.1进行过页面升级，sqlite 除bundle外的表均存在记录。使用命令行升级到 4.7.0，升级过程中，在 launcherd 重新启动时迁移到 postgresql，升级顺利完成，访问页面可查看所有升级记录
                4.6.0 页面上传 4.7.0 的升级文件，并进行独立预检查。bundle/precheck/task等表存在记录。tower 系统内下载解压 4.7.0 升级文件使用命令行升级，升级顺利完成，在 launcherd 启动时迁移数据到 postgresql
                4.6.0 未进行过页面升级，使用页面升级到 4.7.0，升级顺利完成
                4.6.0 进行过页面升级，使用页面升级到 4.7.0，升级顺利完成，访问页面可以查看到所有升级记录
                已经部署或升级到 4.7.0，反复重启 launcherd，不会发生迁移
                低于 4.6.0 版本，通过命令行升级到 4.7.0，升级顺利完成，实际没有迁移行为，迁移记录表的状态为完成
                4.6.0  sqlite 中各表存在数据，升级 4.7.0 时，启动 luancherd 时中断。再次启动 launcherd 顺利完成
            统一命令行和界面升级
                命令行升级统一使用 sh upgrade-cloudtower.sh 触发，当前版本大于等于 4.6.0 时，核心步骤为 installer upgrade
                installer upgrade 命令会升级新的 launcherd rpm，再调用launcherd /upgrade/minimal API 进行升级
                触发命令行升级后，「CloudTower 升级」页面仍能够选择文件执行上传
                已经有 bundle 记录，进行命令行升级可以顺利完成，升级完成后，bundle 记录仍存在，cloudtower-uploads 目录下的升级文件仍存在
                4.6.0及以下版本，执行 installer upgrade 命令会提示不被允许
                4.7.0 及以上版本，执行 installer upgrade_legacy 命令会提示不被允许
                4.7.0 及以上版本，执行 installer upgrade 命令正常完成
                页面上已经触发升级，再进行命令行升级，提示升级进行中，直接中止
                低于 tower 4.6.0 版本，执行命令行升级 4.7.0 版本，升级顺利完成，升级过程中页面没有 banner 等提示，没有任务，没有升级记录，没有独立升级页
                tower 4.6.0/4.7.0 版本，执行命令行升级 4.7.0 版本，产生 tower 任务，发起用户为 system-service
                tower 4.6.0/4.7.0，执行命令行升级 4.7.0，页面有 banner 等提示，产生升级记录，链接跳转独立升级页，实时展示升级进度和日志
                tower 4.6.0/4.7.0，执行命令行升级 4.7.0，升级完毕不会产生用户事件审计
        4.7.0 tower 支持 tencentos
            ISO 部署
                使用 tl3 x86_64/aarch64 版本 ISO，可以部署在 SMTXOS 集群
                使用 tl3 x86_64/aarch64 版本 ISO，可以部署在 SMTXELF 集群
                使用 tl3 x86_64/aarch64 版本 ISO，可以部署在 SMTXZBS 集群
                使用 tl3 x86_64/aarch64 版本 ISO，可以部署在 VMware 集群
                使用 tl3 x86_64/aarch64 版本 ISO，可以部署在使用 tencentos 发行版的集群
                使用 tl3 x86_64/aarch64 版本 ISO，可以部署在不使用 tencentos 发行版的集群
            cloudtower-installer 部署
                部署使用的 cloud-image 为 tencentos 发行版
                使用 tl3 x86_64/aarch64 cloudtower-installer 安装文件，可以部署在 SMTXOS 集群
                使用 tl3 x86_64/aarch64 cloudtower-installer 安装文件，可以部署在 SMTXELF 集群
                使用 tl3 x86_64/aarch64 cloudtower-installer 安装文件，可以部署在 SMTXZBS 集群
                使用 tl3 x86_64/aarch64 cloudtower-installer 安装文件，可以部署在使用 tencentos 发行版的集群
                使用 tl3 x86_64/aarch64 cloudtower-installer 安装文件，可以部署在不使用 tencentos 发行版的集群
            历史版本升级
                4.4.1-p1 两种架构的 tl3 tower，可以顺利升级到 4.7.0 版本
                4.4.1-p2 两种架构的 tl3 tower，可以顺利升级到 4.7.0 版本
                4.4.2 两种架构的 tl3 tower，可以顺利升级到 4.7.0 版本
                历史版本发行版不是 tl3，使用 tl3 的升级文件升级，执行升级脚本时会检查并拦截
            系统服务部署、垂直扩容、升级等
                tl3 tower 部署系统服务，产生的虚拟机使用 tencentos 系统，tower 页面上显示 tencentos 图标
                tl3 tower 部署 everoute 服务，垂直扩容 everoute 服务虚拟机
                tl3 tower 部署备份服务，垂直扩容服务虚拟机
                tl3 tower 部署复制服务，垂直扩容服务虚拟机
                tl3 tower 部署 cloudtower 代理，垂直扩容服务虚拟机
                tl3 tower 部署可观测性服务，垂直扩容服务虚拟机
                tl3 tower 部署 SKS 服务，垂直扩容 SKS 容器镜像仓库所在虚拟机
                tl3 tower 部署普通容器镜像仓库，垂直扩容服务虚拟机
                tl3 tower 部署文件存储服务，垂直扩容服务虚拟机
                tower 4.4.2 版本部署 1.3.2 版本 cloudtower 代理，升级 tower 后，再升级 cloudtower 代理为 1.3.3 版本
            tower 备份重建
                tower 4.7.0 openeuler 版本，能够顺利迁移发行版到 tencentos
                tower 4.7.0 tencentos 版本，能够顺利迁移发行版到 openeuler
                tower 4.7.0 centos 版本，能够顺利迁移发行版到 tencentos
                tower 4.7.0 tencentos 版本，能够顺利迁移发行版到 centos
                tower 4.7.0 tencentos x86_64 版本，能够顺利迁移到 tencentos aarch64
                tower 4.7.0 tencentos aarch64 版本，能够顺利迁移到 tencentos x86_64
            通用检查
                troubleshooter 诊断均通过，不检查 bridge 和 br_netfilters 内核模块
                txos.service 未启用
                nf_tables 模块不会被禁用
                绿盟 RSAS 扫描漏洞，不会存在 CVE-2024-1086（nf_tables 相关）漏洞
                绿盟 RSAS 扫描漏洞，不会存在中高危漏洞（误报除外）
                携带两种架构的 tencentos base 的 scos ova
                能够顺利变更网卡 ip 地址，并使用 installer update-ip 更新环境
                kernel 为 kernel-5.4.119-19.0009.54.tl3.v60.x86_64.rpm 或 kernel-5.4.119-19.0009.54.tl3.v60.aarch64.rpm
                可以顺利通过 kms 在线激活 tencentos
                subscription rpm 的版本为 subscription-1.0.6-11
                可以从备份的 etcd 快照恢复 etcd
        TOWER-18979 tower pod 资源限制
            embed-monitor命名空间下的kube-state-metrics pod 中容器的  requests  为0，由于pod template 中 resources requests 和 limits 都已定义，因此不会被 resources-webhook patch
            embed-monitor命名空间下的node-exporter pod 中容器的 requests 为0，由于pod template 中 resources requests 和 limits 都已定义，因此不会被 resources-webhook patch
            embed-monitor命名空间下的postgres-exporter pod 中的容器 requests 为0，由于pod template 中 resources requests 和 limits 都已定义，因此不会被 resources-webhook patch
            embed-monitor命名空间下的prometheus-blackbox-exporter pod 中的容器 requests 为0，由于pod template 中 resources requests 和 limits 都已定义，因此不会被 resources-webhook patch
            cloudtower-system命名空间下的observability-agent pod 中的容器 requests 为0，由于pod template 中 resources requests 和 limits 都已定义，因此不会被 resources-webhook patch
            cloudtower-system命名空间下的ntpm pod 中的容器 requests 为0，由于pod template 中 resources requests 和 limits 都已定义，因此不会被 resources-webhook patch
            cloudtower-system命名空间下的time-exporter pod 中的容器 requests 为0，由于pod template 中 resources requests 和 limits 都已定义，因此不会被 resources-webhook patch
            高配 tower，openresty 容器 requests，cpu 100m，mem 128Mi
            高配 tower，server 容器 requests，cpu 1，mem 2048Mi
            高配 tower，prisma 容器 requests，cpu 1，mem 1536Mi
            高配 tower，prisma-worker 容器 requests，cpu 500m，mem 768Mi
            高配 tower，worker 容器 requests，cpu 500m，mem 1024Mi
            低配 tower，openresty 容器 requests，cpu 50m，mem 64Mi
            低配 tower，server 容器 requests，cpu 500m，mem 1024Mi
            低配 tower，prisma 容器 requests，cpu 500，mem 768Mi
            低配 tower，prisma-worker 容器 requests，cpu 250m，mem 768Mi
            低配 tower，worker 容器 requests，cpu 250m，mem 512Mi
            存在 apps 06-RESOURCES-WEBHOOK，存在 resource-webhook deployment 和 mutatingwebhookconfigurations
            webhook 用于在 pod 创建时为容器配置 resources requests 和 limits，豁免 kube-system/ingress-nginx/cert-manger/kube-public/local-path-storage 等命名空间
            pod 存在 webhook.resources/ignore: "true" 标签，webhook 不生效
            pod 存在 app.kubernetes.io/name: "tower-authn" 标签，webhook 不生效
            pod 存在 app.kubernetes.io/name: resources-webhook 标签，webhook 不生效
            pod 存在 app: cloudtower-cloudtower 标签，webhook 不生效
            pod 存在 app: cloudtower-worker 标签，webhook 不生效
            pod 存在 app: cloudtower-prisma 标签，webhook 不生效
            pod 存在 app: cloudtower-prisma-worker 标签，webhook 不生效
            pod metadata 存在webhook.resources/ignore: "true" annotation 的，webhook 不生效
            创建负载，pod template 中同时设置 annotation webhook.resources/ignore: "true" 和 label app:cloudtower-prisma-worker，webhook 不生效，原生的 mutationwebhookconfiguration 先生效，因此 resources-webhook 不会有相关日志
            resource-webhook 控制器不工作时，删除不受 webhook 影响创建流程的 pod，能够顺利重建
            installer deploy/update/upgrade_legacy/upgrade 以及页面升级过程中，会设置 resource-webhook 默认limit为系统内计算资源的 0.25
            创建 pod 时为容器定义完整 requests/limits，webhook 不调整 resources-quota
            创建 pod 时容器定义了requests 但未定义 limits ，resources-webhook 将为容器设置 limits，并添加 annotation
            创建 pod 时容器定义了 requests，limits 只定义了 cpu，未定义 memory，resources-webhook 将为容器设置 limits.memory，并添加 annotation
            创建 pod 时容器定义了 requests，limits 只定义了 memory，未定义 cpu，resources-webhook 将为容器设置 limits.cpu，并添加 annotation
            创建 pod 时容器定义了 limits，未定义 requests，k8s 会将 requests 设置成和 limits 一样
            创建 pod 时没有为容器定义 requests 和 limits，resources-webhook 将为容器设置 limits，requests 的 cpu 和 memory 都为0，且添加 annotation
            创建 pod 时，pod 中存在 init container 以及多个 container，只有要一个容器缺少 limits 定义，就会被 resources-webhook 设置默认 limits 并添加 annotation
            被 resources-webhook 设置了容器 limits 的 pod，再编辑 pod 对应的 deploy/sts/daemonset 修改limit，重建的 pod 仍然受 resources-webhook 规则影响
            通过 installer update 调整 resource-wehook 的 ratio 阈值从 0.25 到 0.5,原先被 resource-webhook 设置了 limit 的 pod 会删除重建
            resources-webhook 部署后，旧的未设置 resources 的容器，会被 installer delete
            创建新虚拟机挂载 ISO 部署高配 tower，部署顺利完成，所有 pod 中容器 resources quota 符合预期
            创建新虚拟机挂载 ISO 部署低配 tower，部署顺利完成，所有 pod 中容器 resources quota 符合预期
            cloudtower-installer 部署高配 tower，部署顺利完成，所有 pod 中容器 resources quoata 符合预期
            cloudtower-installer 部署低配 tower，部署顺利完成，所有 pod 中容器 resources quoata 符合预期
            高配 tower 部署所有系统服务，均能部署成功
            tower k8s 中 default 和 kube-node-lease 命名空间默认没有标签，在这两个命名空间下创建负载会被 resources-webhook 忽略
        TOWER-18980 升级后不覆盖 ingress-nginx ssl 证书
            4.7.0 tower 为 ingress-nginx 配置 tls 证书，使用升级脚本升级 tower，升级完成后 nginx 仍使用该 tls 证书
            4.7.0 tower 为 ingress-nginx 配置 tls 证书，通过页面操作升级 tower，升级完成后 nginx 仍使用该 tls 证书
            4.7.0 tower 为 ingress-nginx 配置 tls 证书，变更 tower 网卡ip，执行 installer update-ip，完成后 nginx 仍使用该 tls 证书
            4.7.0 tower 为 ingress-nginx 配置 tls 证书，执行 installer update，完成后 nginx 仍使用该 tls 证书
            4.7.0 tower 为 ingress-nginx 配置 tls 证书，执行 installer renew-cert --force，完成后 nginx 仍使用该 tls 证书
            4.6.1/4.6.0 tower 为 ingress-nginx 配置 tls 证书，通过页面操作升级到 4.7.0，升级完成后 nginx 仍使用该 tls 证书
            4.6.1/4.6.0 tower 为 ingress-nginx 配置 tls 证书，通过升级脚本升级到 4.7.0，升级完成后 nginx 仍使用该 tls 证书
            低于 4.6.0 的 tower 为 ingress-nginx 配置 tls 证书，通过升级脚本升级到 4.7.0，升级完成后 nginx 仍使用该 tls 证书
            4.7.0 tower 执行 installer backup，再进行重建流程，重建完成后 nginx 仍使用该 tls 证书
            低于 4.6.0 的 tower 没有为 ingres-nginx 配置 tls 证书，通过升级脚本升级到 4.7.0，升级完成后 nginx  不会指定 tls 证书
            4.6.1/4.6.0 tower 没有为 ingress-nginx 配置 tls 证书，通过升级脚本/界面升级到 4.7.0，升级完成后 nginx 不会指定 tls 证书
        capp 修复不一致的副本数
            脚本处理「一键提升集群副本数」造成系统服务的VM 副本数跟 CAPP 不一致
                参数检查
                    tower 无法访问，返回报错信息，登录失败
                    使用本地用户登录，用户名密码正确，登录成功
                    使用本地用户登录，用户名密码错误，登录失败，返回错误信息
                    使用 LDAP 用户登录，用户名密码正确，登录成功
                    使用 LDAP 用户登录，用户名密码错误，登录失败，返回错误信息
                    使用 root 及 运维管理员权限，可以成功处理 capp 副本
                    使用只读权限用户，操作修复配置会失败
                    交互式命令，不确认修复操作，超时退出
                    交互式命令，确认修复操作，输入n， 退出不做修复
                    交互式命令，确认修复操作，输入y， 修复 capp 配置
                    预设环境变量，执行命令可以成功
                    CLOUDTOWER_ENDPOINT 如果不设置，默认使用 127.0.0.1
                    交互式输入环境信息，执行命令可以成功
                    参数检查：-y,-h,- -dry-run
                测试场景
                    没有任何需要修复的系统服务，执行脚本提示不需要修复，不做配置更改
                    如果有些系统服务的 vm instance 已经找不到了，应该跳过，继续修复剩余的 instance
                    重复执行脚本，已经修复过的 CAPP 配置不会再发生改变
                    x86 环境脚本运行
                    arm 环境脚本运行
                    arm 架构的 tower 修复
                    x86 架构的 tower 修复
                    AOC 验证脚本修复
                    各种系统服务场景一：3.4.5 升级 4.4.0，再升级 4.6.1，包含多个副本数一致以及不一致的系统服务，详见用例步骤
                    各种系统服务场景二：4.2.0 升级 4.6.1，包含多个副本数一致以及不一致的系统服务，详见用例步骤
            tower 升级自动处理
                检查修复阶段在所有组件升级完之后进行
                检查系统服务如果 capp 配置是 2，但实际副本数为 3，升级成功后，capp 配置会修复为 instances："storageReplicas": 3
                检查系统服务如果 capp 配置是 2，实际副本数为 2，升级成功后，capp 配置不改变
                检查修复配置为 3 后，系统服务能升级成功
    Tower - 4.7.1 调整
        TOWER-20147
            UI installer
                centos7.x86_64
                    部署 Tower 成功
                oe2003.x86_64
                    部署 Tower 成功
                oe2003.aarch64
                    部署 Tower 成功
            VM install
                centos7.x86_64
                    resolv.conf 文件不存在 - 部署 Tower 成功
                    resolv.conf 中的 nameserver 不存在 - 部署 Tower  成功
                    resolv.conf 中的 nameserver 不可达 - 部署 Tower 成功
                    resolv.conf 文件存在，其中的 nameserver 正常 - 部署 Tower 成功
                oe2003.x86_64
                    resolv.conf 文件不存在 - 部署 Tower 成功
                    resolv.conf 中的 nameserver 不存在 - 部署 Tower  成功
                    resolv.conf 中的 nameserver 不可达 - 部署 Tower 成功
                    resolv.conf 文件存在，其中的 nameserver 正常 - 部署 Tower 成功
                oe2003.aarch64
                    resolv.conf 文件不存在 - 部署 Tower 成功
                    resolv.conf 中的 nameserver 不存在 - 部署 Tower  成功
                    resolv.conf 中的 nameserver 不可达 - 部署 Tower 成功
                    resolv.conf 文件存在，其中的 nameserver 正常 - 部署 Tower 成功
            升级
                centos7.x86_64
                    resolv.conf 文件不存在 - 升级 Tower 成功
                    resolv.conf 中的 nameserver 不存在 - 升级 Tower  成功
                    resolv.conf 中的 nameserver 不可达 - 升级 Tower 成功
                    resolv.conf 文件存在，其中的 nameserver 正常 - 升级 Tower 成功
                oe2003.x86_64
                    resolv.conf 文件不存在 - 升级 Tower 成功
                    resolv.conf 中的 nameserver 不存在 - 升级 Tower  成功
                    resolv.conf 中的 nameserver 不可达 - 升级 Tower 成功
                    resolv.conf 文件存在，其中的 nameserver 正常 - 升级 Tower 成功
                oe2003.aarch64
                    resolv.conf 文件不存在 - 升级 Tower 成功
                    resolv.conf 中的 nameserver 不存在 - 升级 Tower  成功
                    resolv.conf 中的 nameserver 不可达 - 升级 Tower 成功
                    resolv.conf 文件存在，其中的 nameserver 正常 - 升级 Tower 成功
            运维操作
                Tower VM HA 之后 - Tower 恢复后，访问正常，pods 均为 running
                Tower VM 强制重启之后 - Tower 恢复后，访问正常，pods 均为 running
                Tower VM 强制关机后再开机 - Tower 恢复后，访问正常，pods 均为 running
    tower - 4.8.0 调整
        cloudtower HA
            HA 部署
                UI 方式
                    部署入口
                        系统配置，CloudTower 升级上方，新增 「CloudTower 高可用」菜单
                        当前 Tower 版本 4.8.0 及以上，tower 所在集群为 SMTX ELF，集群未被该 tower 纳管，「CloudTower 高可用」菜单不可见
                        当前 Tower 版本 4.8.0 及以上，tower 所在集群为 SMTX OS（ELF），集群未被该 tower 纳管，「CloudTower 高可用」菜单不可见
                        当前 Tower 版本 4.8.0 及以上，tower 所在集群为 ZBS，集群未被该 tower 纳管，「CloudTower 高可用」菜单不可见
                        当前 Tower 版本 4.8.0 及以上，tower 所在集群为 SMTX OS（VMware），集群未被该 tower 纳管，「CloudTower 高可用」菜单不可见
                        当前 Tower 版本 4.8.0 及以上，tower 所在集群为 SMTX ELF，集群被该 tower 纳管，「CloudTower 高可用」菜单可见
                        当前 Tower 版本 4.8.0 及以上，tower 所在集群为 SMTX OS（ELF），集群被该 tower 纳管，「CloudTower 高可用」菜单可见
                        当前 Tower 版本 4.8.0 及以上，tower 所在集群为 ZBS，集群被该 tower 纳管，「CloudTower 高可用」菜单不可见
                        当前 Tower 版本 4.8.0 及以上，tower 所在集群为 SMTX OS（VMware），集群被该 tower 纳管，「CloudTower 高可用」菜单不可见
                        只读及以上权限的角色可以看到 「CloudTower 高可用」菜单
                        部署了 sks 的 Tower，「CloudTower 高可用」菜单不可见
                        tl3-x86 环境 Tower，「CloudTower 高可用」菜单不可见
                        tl3-arm 环境 Tower，「CloudTower 高可用」菜单不可见
                        低版本 UI installer 部署的 oe-x86 ，升级到 4.8.0，无法部署 HA，隐藏入口
                        低版本 UI installer 部署的 centos-x86，升级到 4.8.0，无法部署 HA，隐藏入口
                    未启用 HA
                        无权限用户的展示
                            菜单入口展示的时候，无论是否关联 tower 集群、企业许可、许可有效期、tower 未升级，始终展示无权限的提示
                            菜单入口隐藏的时候，无权限的用户也看不到菜单
                        有权限用户，根据启用条件展示不同内容
                            Tower 许可基础版，许可过期，tower 所在集群未被纳管，则顶部展示过期 banner，HA页面展示许可不满足+集群未纳管的提示
                            Tower 许可基础版，许可过期，tower 所在集群被纳管，则顶部展示过期 banner，HA页面展示许可不满足的提示
                            Tower 许可基础版，许可过期，tower 所在集群未被纳管，tower 升级中，则顶部展示过期 banner + 升级 banner， HA 页面展示许可不满足+集群未纳管的提示
                            Tower 许可基础版，许可过期，tower 所在集群被纳管，tower 升级中，则顶部展示过期 banner + 升级 banner， HA 页面展示许可不满足提示
                            Tower 许可基础版，许可未过期，tower 所在集群未被纳管，则 HA 页面展示许可不满足+集群未纳管的提示
                            Tower 许可基础版，许可未过期，tower 所在集群被纳管，则 HA 页面展示许可不满足的提示
                            Tower 许可基础版，许可未过期，tower 所在集群未被纳管，tower 升级中，则顶部展示升级 banner， HA 页面展示许可不满足+集群未纳管的提示
                            Tower 许可基础版，许可未过期，tower 所在集群被纳管，tower 升级中，则顶部展示升级 banner， HA 页面展示许可不满足的提示
                            Tower 许可企业版或企业增强版，许可过期，tower 升级中，tower 所在集群未被纳管，则顶部展示过期 banner + 升级 banner，HA页面展示集群未被纳管提示
                            Tower 许可企业版或企业增强版，许可过期，tower 升级中，tower 所在集群被纳管，则顶部展示过期 banner + 升级 banner，HA页面展示部署说明，启用中按钮禁用
                            Tower 许可企业版或企业增强版，许可未过期，tower 升级中，tower 所在集群被纳管，则顶部展示升级 banner，HA页面展示部署说明，启用中按钮禁用
                            Tower 许可企业版或企业增强版，许可未过期，tower 升级中，tower 所在集群未被纳管，则顶部展示升级 banner，HA页面展示集群未被纳管的提示
                            Tower 许可企业版或企业增强版，许可过期，tower 所在集群未被纳管，则顶部展示过期 banner，HA页面展示许集群未纳管的提示
                            Tower 许可企业版或企业增强版，许可过期，tower 所在集群被纳管，则顶部展示过期 banner，HA页面展示部署说明，启用中按钮禁用
                            Tower 许可企业版或企业增强版，许可未过期，tower 所在集群未被纳管，则HA页面展示许集群未纳管的提示
                            Tower 许可企业版或企业增强版，许可未过期，tower 所在集群被纳管，则HA页面展示部署说明，启用中按钮可用
                            顶部的过期 banner，更新许可检查
                            顶部的升级 banner，查看进度检查
                            许可不是企业版的时候，有更新许可的入口，点击更新许可跳转到 [系统配置 > 软件许可] 页面
                            条件均满足，展示启用说明的时候，点击「上传」跳转到 [内容库 > ISO 映像] 页面，并打开 [上传 ISO 映像] 弹窗
                            条件均满足，展示启用说明的时候，点击打开 [创建空白虚拟机] 弹窗
                            条件均满足，展示启用说明的时候，点击「启用」button 打开 [启用 CloudTower 高可用] 弹窗
                            页面基本样式和内容对照 UI spec 检查
                            Tower 低配的规格，UI 上禁用「启用高可用」button，并且主动节点下方红字提示：仅高配的 CloudTower 支持启用高可用。
                            Tower 低配的规格，与许可过期/升级中/许可类型不允许，同时发生，检查 UI 展示正确
                    HA启用配置
                        CloudTower 管理 IP：展示当前 tower 的管理 IP
                        主动节点 HA 网络：需过滤 VLAN 类型为 access 的虚拟网络
                        主动节点 HA 网络：默认选中「使用主动节点的管理网络」，并展示当前管理网的虚拟机网络名称，子网掩码和网关。用户需要填写「IP 地址」
                        主动节点 HA 网络：使用主动节点的管理网络，IP 地址为必填，留空有校验提示
                        主动节点 HA 网络：使用主动节点的管理网络，IP 地址格式校验及提示
                        主动节点 HA 网络：使用主动节点的管理网络，IP 地址与表单里其他 IP 地址重复，有校验和提示
                        主动节点 HA 网络：选择「使用其他虚拟机网络」后，用户需要手动设置「虚拟机网络」「IP 地址」「子网掩码」「默认网关」字段
                        主动节点 HA 网络：使用其他虚拟机网络，虚拟机网络必选，留空有校验提示
                        主动节点 HA 网络：使用其他虚拟机网络，虚拟机网络选择，展示 tower 所在集群的 vlan access 类型的虚拟网络列表，过长有滚动条
                        主动节点 HA 网络：使用其他虚拟机网络，虚拟机网络选择，按照名称排序展示，过滤掉主动节点管理网络
                        主动节点 HA 网络：使用其他虚拟机网络，虚拟机网络选择，注意名称太长时的展示
                        主动节点 HA 网络：使用其他虚拟机网络，IP 地址为必填，留空有校验提示
                        主动节点 HA 网络：使用其他虚拟机网络，IP 地址格式校验及提示
                        主动节点 HA 网络：使用其他虚拟机网络，IP 地址与表单里其他 IP 地址重复，有校验和提示
                        主动节点 HA 网络：使用其他虚拟机网络，子网掩码，必填，留空有校验提示
                        主动节点 HA 网络：使用其他虚拟机网络，子网掩码格式校验及提示
                        主动节点 HA 网络：使用其他虚拟机网络，网关，必填
                        主动节点 HA 网络：使用其他虚拟机网络，网关有格式校验及提示
                        主动节点 HA 网络：使用其他虚拟机网络，会过滤掉主动节点的管理网络
                        主动节点 HA 网络：未填写 IP 和子网掩码，点击转换为 CIDR 块，出现空值 CIDR 块供用户填写，内置 inlinehelp 展示格式
                        主动节点 HA 网络：用户填写了 IP ，子网掩码为空，点击转换为 CIDR 块，报错不切换
                        主动节点 HA 网络：用户填写了子网掩码，IP 地址为空，点击转换为 CIDR 块，报错不切换
                        主动节点 HA 网络：用户填写了正确格式的 IP 和子网掩码，点击转换为 CIDR 块，CIDR 块自动根据已填写的 IP 地址和子网掩码填充正确的值
                        主动节点 HA 网络：用户填写了格式错误的 IP 和子网掩码，点击转换为 CIDR 块，将无法转换。错误的格式界面上有错误提示
                        主动节点 HA 网络：点击转换为 CIDR 块之后，隐藏 IP 和子网掩码两个配置
                        主动节点 HA 网络：点击转换为 IP 地址和子网掩码之后，隐藏 CIDR 块配置
                        主动节点HA 网络：从 CIDR 转换为 IP 和子网掩码，如果已经填写了格式正确的 CIDR 块，会自动填充 IP 地址和子网掩码
                        主动节点HA 网络：从 CIDR 转换为 IP 和子网掩码，如果未填写了格式正确的 CIDR 块， 报错不切换
                        主动节点 HA 网络：使用 CIDR 块，IP 地址与表单里其他 IP 地址重复，有校验和提示
                        被动节点，虚拟机选择：下拉列表展示，每条数据展示虚拟机名称及集群名称
                        被动节点，虚拟机选择：下拉列表检查虚拟机名称过长的展示
                        被动节点，虚拟机选择：下拉列表检查集群名称过长的展示
                        被动节点，虚拟机选择：下拉列表按照虚拟机名称排序
                        被动节点，虚拟机选择：下拉列表支持搜索
                        被动节点，虚拟机选择：下拉列表滚动条
                        被动节点，虚拟机选择：需要过滤掉 zbs 集群
                        被动节点，虚拟机选择：选择了虚拟机之后，虚拟机下方展示所属数据中心，集群，主机的列表
                        被动节点，虚拟机选择：选择了虚拟机之后，触发校验，如果虚拟机与当前 tower 处于同一主机，红色错误提示同一主机
                        被动节点，虚拟机选择：选择了虚拟机之后，触发校验，如果虚拟机有一个或多个网络设备，红色错误提示网络设备
                        被动节点，虚拟机选择：选择了虚拟机之后，触发校验，如果虚拟机有一个或多个网络设备+与当前 tower 处于同一主机，红色错误提示两个信息
                        被动节点，管理网络：虚拟机网络默认不选中任何网络
                        被动节点，管理网络：虚拟机网络必选，留空有校验提示
                        被动节点，管理网络：虚拟机网络选择，展示被动节点所在集群的 vlan access 类型的虚拟网络列表，过长有滚动条
                        被动节点，管理网络：虚拟机网络选择，按照名称排序展示
                        被动节点，管理网络：虚拟机网络选择，注意名称太长时的展示
                        被动节点，HA 网络：默认不选中任何网络
                        被动节点，HA 网络：虚拟机网络必选，留空有校验提示
                        被动节点，HA 网络：虚拟机网络选择，展示被动节点所在集群的 vlan access 类型的虚拟网络列表，过长有滚动条
                        被动节点，HA 网络：虚拟机网络选择，按照名称排序展示
                        被动节点，HA 网络：虚拟机网络选择，注意名称太长时的展示
                        被动节点，HA 网络：IP 地址为必填，留空有校验提示
                        被动节点，HA 网络：IP 地址格式校验及提示
                        被动节点，HA 网络：IP 地址与表单里其他 IP 地址重复，有校验和提示
                        被动节点，HA 网络：子网掩码格式校验及提示
                        被动节点，HA 网络：子网掩码，必填，留空有校验提示
                        被动节点，HA 网络：网关，必填
                        被动节点，HA 网络：网关有格式校验及提示
                        被动节点 HA 网络：未填写 IP 和子网掩码，点击转换为 CIDR 块，出现空值 CIDR 块供用户填写，内置 inlinehelp 展示格式
                        被动节点 HA 网络：用户填写了 IP ，子网掩码为空，点击转换为 CIDR 块，报错不切换
                        被动节点 HA 网络：用户填写了子网掩码，IP 地址为空，点击转换为 CIDR 块，报错不切换
                        被动节点 HA 网络：用户填写了正确格式的 IP 和子网掩码，点击转换为 CIDR 块，CIDR 块自动根据已填写的 IP 地址和子网掩码填充正确的值
                        被动节点 HA 网络：用户填写了格式错误的 IP 和子网掩码，点击转换为 CIDR 块，CIDR 块留空
                        被动节点 HA 网络：点击转换为 CIDR 块之后，隐藏 IP 和子网掩码两个配置
                        被动节点 HA 网络：点击转换为 IP 地址和子网掩码之后，隐藏 CIDR 块配置
                        被动节点HA 网络：从 CIDR 转换为 IP 和子网掩码，如果已经填写了格式正确的 CIDR 块，会自动填充 IP 地址和子网掩码
                        被动节点HA 网络：从 CIDR 转换为 IP 和子网掩码，如果未填写了格式正确的 CIDR 块， 报错不切换
                        被动节点 HA 网络：使用 CIDR 块，IP 地址与表单里其他 IP 地址重复，有校验和提示
                        仲裁节点：IP 地址必填，留空有校验提示
                        仲裁节点：IP 地址格式校验及提示
                        仲裁节点：IP 地址与表单里其他 IP 地址重复，有校验和提示
                        仲裁节点：如果与其他节点位于同一主机，触发错误提示：各 HA 节点必须放置在不同主机上，但当前的仲裁节点和%主动节点/被动节点%位于同一主机。
                        管理网络和HA 网络同一个网络，但是网关、子网掩码配置不对，会在提交时报错
                        以 CIDR 块配置提交部署 HA
                        以 IP 地址形式配置提交部署 HA
                        手动填写的配置不满足条件出现错误提示，修正后错误提示消失
                        选择项不满足条件出现错误提示，重新选择满足条件后，错误提示消失
                        被动节点，如果管理网络和HA 网络使用同一个 vlan，那么子网掩码必须一样，否则报错
                        被动节点，如果管理网络和HA 网络使用同一个 vlan，那么网关必须一样，否则报错
                        主动节点，如果管理网络和HA 网络使用不通网络，那么必须是不同的网段，否则报错
                        主动节点，如果管理网络和HA 网络使用不通网络，那么网关必须不一样，否则报错
                    HA 部署进度
                        进入部署中，前端不能再提交部署请求，新的部署请求失败报错
                        部署中，通过 API 再次提交部署请求应该报错
                        部署中，顶部会展示 HA 部署提示的 banner
                        点击顶部部署 HA banner 的「查看进度」，跳转展示部署中页面
                        部署中的页面会展示：当前步骤名，进度条，时间等信息，对照设计文档检查
                        部署过程中刷新页面，或者新开页面，都能看到当前的部署进度展示
                        部署中，检查部署过程的信息展示和同步
                        等到部署成功，页面会展示成功的状态，顶部的 banner 消失。下一次接口请求到数据后，会自动化刷新成 HA 的拓扑图展示。
                        等到部署失败，会展示失败的步骤及名称，失败的状态，顶部的 banner 消失
                        部署失败，如果失败的步骤可以重试，页面会展示重试按钮，点击重试按钮，打开启用 HA 配置弹窗，并填充上一次的配置信息
                    三节点 HA 部署
                        物理环境
                            Active(SMTX OS ELF) + Passive(SMTX OS ELF) + Witness(SMTX OS ELF)
                            Active(SMTX OS ELF) + Passive(SMTX OS ELF) + Witness(SMTX ELF)
                            Active(SMTX ELF) + Passive(SMTX ELF) + Witness(SMTX ELF)
                            Active(SMTX OS ELF) + Passive(SMTX ELF) + Witness(其他地方)
                            Active(SMTX OS ELF) + Passive(SMTX OS ELF) + Witness(其他地方)
                            Active(SMTX OS 双活) + Passive(SMTX OS) + Witness(其他地方)
                            Active(ACOS) + Passive(ACOS) + Witness(其他地方)
                            同一 SMTX OS ELF 集群：Active + Passive
                            同一 SMTX ELF 集群：Active + Passive
                            同一数据中心，不同集群：Active ，Passive
                            跨数据中心：Active ，Passive
                            zbs 集群不支持
                            ARM 环境
                            el7-x86 环境
                            oe-x86 环境
                            5.x 版本集群
                            6.x 版本集群
                            UI installer 部署,el7-x86 tower 部署 HA 成功
                            UI installer 部署,oe-x86 tower 部署 HA 成功
                            UI installer 部署,oe-arm tower 部署 HA 成功
                            VM install 部署,el7-x86 tower 部署 HA 成功
                            VM install 部署,oe-x86 tower 部署 HA 成功
                            VM install 部署,oe-arm tower 部署 HA 成功
                            UI installer 部署 x86 tl3 tower，不支持部署 HA
                            UI installer 部署 arm tl3 tower，不支持部署 HA
                            VM install 部署 x86 tl3 tower，不支持部署 HA
                            VM install 部署 arm tl3 tower，不支持部署 HA
                            升级上来的 UI installer 部署的 el7-x86 tower，不支持部署 HA
                            升级上来的 UI installer 部署的 oe-x86 tower，不支持部署 HA
                            低版本 UI installer 部署的 arm，升级到 4.8.0，不支持部署 HA
                            Active(SMTX OS 双活) + Passive(SMTX OS 双活) + Witness(SMTX OS 双活)
                        网络环境
                            HA 网络与管理网络处于同一网段，管理网络和 HA 网络复用
                            HA 网络和管理网络处于不同网段，单管理网络，单 HA 网络
                            HA 网络和管理网络处于不同网段，HA 节点也处于不同网段，L3 跨三个集群
                            active/passive 和 witness 同子网，active / passive 不同子网，vip 独立
                            active/passive/vip 同子网，witness 不同子网
                            交换机带了 tag vlan，去部署 HA。具体的网络情况 wenfei 交流一下
                            使用静态 IP 部署的 active，去组建 HA
                            使用静态 IP 部署的 witness，去组建 HA
                            使用动态 IP 部署的 active，去组建 HA
                            使用动态 IP 部署的 witness，去组建 HA
                        节点规格
                            active & passive：高配，且配置相同，witness：4C 8G 200G
                            低配 的 Tower 接口发起部署，应该报错
                            低配的 Tower UI 上提示 “仅高配的 CloudTower 支持启用高可用。”，不支持启用 HA
                        HA 启用步骤
                            预检查
                                active，passive，witness 三节点中任意节点 的 hostname 相同，不影响部署
                                active、passive、witness 节点的 vm name 相同，不影响部署
                                passive HA IP 被占用，不能部署，返回对应错误信息 - 这个目前做不到
                                tower 处于升级状态，不能部署，启用高可用的按钮置灰
                                passive 节点配置了网卡，不能部署，返回错误
                                节点不挂载当前 tower 版本对应的 iso，不影响部署，但前提是挂载过并安装过 OS
                                passive 节点和当前 tower 处于同一主机，不能部署，返回错误
                                witness 节点和当前 tower 处于同一主机，不能部署，返回错误
                                witness 节点和 passive 处于同一主机，不能部署，返回错误
                                三个节点均处于同一主机，不能部署，返回错误
                                所有检查通过，进入下一阶段
                                检查不通过，部署终止，HA 部署状态为失败，可以重试
                                部署前检查项：checkNetworkConnectivity: 检查网络连通性
                                部署前检查项：checkNetworkLatency: 检查网络延迟
                                部署前检查项： checkCPUArchitecture: 检查 CPU 架构一致性
                                部署前检查项：checkPackage: 检查安装包文件完整性
                                部署前检查项：checkOSDistribution: 检查操作系统发行版一致性
                                部署前检查项：checkDiskSpace: 检查磁盘空间
                                部署前检查项：checkVMSpec: 检查虚拟机规格一致性
                            网络配置
                                主动节点 HA 网络：vlanId 不存在，部署失败，返回错误
                                主动节点 HA 网络：IP 地址冲突，部署失败，返回错误 - 这个目前做不到
                                主动节点 HA 网络：配置错误的网关，部署失败，返回错误
                                主动节点 HA 网络：子网掩码与网关不匹配，部署失败，返回错误
                                被动节点 HA 网络：vlanId 不存在，部署失败，返回错误
                                被动节点 HA 网络：IP 地址冲突，部署失败，返回错误 - 这个目前做不到
                                被动节点 HA 网络：配置错误的网关，部署失败，返回错误
                                被动节点 HA 网络：子网掩码与网关不匹配，部署失败，返回错误
                                网络参数设置都正确，HA 网络配置成功
                                active 如果管理网络和 HA 网络不同子网，添加 HA 网卡，网卡状态 enable
                                passive 如果管理网络和 HA 网络不同子网，添加两张网卡，管理网卡和 HA 网卡都是 enable
                                passive 管理网络和 HA 网络同一子网，添加一张网卡，网卡 enable
                                网络配置失败，部署终止，HA 部署状态失败
                                网络配置失败，自动清理已经配置的网卡，清理成功可以重试，不成功不能重试
                            部署前检查
                                active 和 witness HA 网络不联通，不能部署，返回对应错误信息
                                passive 节点 HA 网络延迟探测5 次，取平均值，10ms 以内通过。超过 10ms，不能部署。
                                witness 节点 HA 网络延迟探测5 次，取平均值，10ms 以内通过。超过 10ms，不能部署。
                                active 节点不满足 spec 要求，不能部署，返回对应错误信息
                                passive 节点不满足 spec 要求，不能部署，返回对应错误信息
                                witness 节点不满足 spec 要求，不能部署，返回对应错误信息
                                active、passive、witness 任一架构不同，不能部署
                                磁盘空间要求，暂时没有做
                                passive 节点剩余磁盘空间不足 30G
                                active 节点剩余磁盘空间不足 30G
                                witness 节点剩余磁盘空间不足 30G
                                检查失败，HA 部署失败，尝试清理网卡，清理成功可以重试，清理失败不能重试
                                active 节点 5432/9090 端口连通性检查，未正常开放，不能部署，返回对应报错信息
                                passive 节点 5432/9090 端口连通性检查，未正常开放，不能部署，返回对应报错信息
                                witness 节点 5432/9090 端口连通性检查，未正常开放，不能部署，返回对应报错信息
                                passive 节点的 /var/lib/postgresql 目录下不为空，不能部署，返回对应报错信息
                                witness 节点的 /var/lib/postgresql-monitor 目录下不为空，不能部署，返回对应报错信息
                                active、passive、witness 的安装包版本不一致，不能部署
                            集群配置
                                三个节点在同一集群 - 创建放置组规则
                                标记各节点为系统服务虚拟机（witness 有可能不在 tower 上）
                                部署失败，不清理放置组规则，这次交付不允许重试。会尝试清理网卡。
                                三个节点分别在不同集群 - 不会创建放置组规则
                                三个节点在两个集群 - 为在同集群的两个节点，创建放置组规则
                            部署 witness 节点
                                sh ./preinstall.sh，物料检查，物料缺失，部署失败 - 在部署前检查节点进行
                                执行 deploy witness 失败（./binary/installer ha deploy witness --deploy-mode threeNode --cluster-config /etc/cloudtower/cluster.yaml）
                                witeness 节点如果部署失败，HA 也会失败
                            部署 active 节点
                                配置管理网卡、HA 网卡 - 在网络配置阶段进行
                                tower 单转主，拉起跟 HA 相关的服务时出错，部署任务失败
                            加入 passive 节点
                                配置管理网卡、HA 网卡 - 在网络配置阶段进行
                                物料缺失，部署失败 - 在部署前检查阶段进行
                                被动节点加入 HA 网络失败，部署失败
                            Tower 组件转成 HA
                                这个阶段异常，Tower 大概率不可用
                            状态检查
                                集群状态检查
                                节点状态检查
                                文件同步状态检查
                                检查 cloudtower 三个节点的组件是否 ready
                                注意检查日志里面是否有异常
                        部署过程故障
                            部署过程中，模拟 active -> witness 不可访问
                            部署过程中，模拟 active -> passive 不可访问
                            部署过程中，模拟 passive -> witness 不可访问
                            部署过程中，模拟 passive -> active 不可访问
                            部署过程中，模拟  witness-> passive 不可访问
                            部署过程中，模拟  witness-> active 不可访问
                            部署时 witness 节点重启
                            部署时 passive 节点重启
                            部署时主动节点 launcherd 异常重启
                            部署过程中的不同阶段，witeness 和 passive 节点随机重启
                        部署检查
                            部署过程
                                部署过程中，集群不会出现中间状态，比如单 tower 转 active 时，不会出现 demote 状态，也不会出现 failover。部署结束后，根据部署结果展示集群状态
                                部署过程中不触发非预期的告警信息
                            部署成功
                                HA 页面展示
                                    HA 页面展示基本 HA 信息，各个节点的状态、网络、节点信息等
                                    如果没有关联可观测，需要展示将 CloudTower 关联到可观测的提示信息
                                    如果没有关联可观测，用户有可观测的管理权限，需要展示「关联可观测服务」，点击打开系统配置的可观测页面
                                    如果没有关联可观测，用户没有可观测的管理权限，不展示「关联可观测服务」，只展示关联可观测的提示信息
                                    部署前已经关联了可观测，部署成功后保持关联状态
                                    关联了可观测的时候，如果出现了 failover，需要确认可观测的关联状态是否会有异常  --挪到系统服务适配
                                主节点检查
                                    HA controller 运行
                                    k8s control plane pod 运行
                                    launcherd 运行检查
                                    postgres 运行检查：使用连接 postgres 的方式检查
                                    pgaf 运行检查
                                    containerd  运行检查
                                    file server 运行检查
                                    tower server 运行
                                    业务 pod 全部运行
                                    embed-monitor 组件 grafana-server 默认不启用
                                    embed-monitor 组件 vm-single 运行
                                    embed-monitor 组件 vm-agent 运行
                                    embed-monitor 组件 vector 运行
                                    ntpm 运行
                                    node-exporter 运行
                                    ingress-nginx-controller 运行
                                    everoute-agent 运行
                                    kube-proxy 运行
                                    node-local-dns 运行
                                    vip 网卡运行正常，检查 network manager 的配置
                                    HA 网卡运行正常，检查network manager 的配置
                                    k8s 证书检查
                                    host agent 的运行检查
                                    支持的 UI 界面操作 - 可以编辑虚拟机组，移至组、从组内移出
                                    支持的 UI 界面操作 - 可以编辑虚拟机放置组，移至组、从组内移出
                                    支持的 UI 界面操作 - 创建快照、查看详情、编辑快照基本信息、编辑标签、删除快照
                                    支持的 UI 界面操作 - 加入快照计划，并生成快照组
                                    支持的 UI 界面操作 - 集群内热迁移
                                    支持的 UI 界面操作 - 关联标签、移除标签
                                    支持的 UI 界面操作 - 打开终端并可正常输入命令
                                    支持的 UI 界面操作 - 查看网络链路，跳转到集群的网络拓扑页面
                                从节点检查
                                    HA controller 运行
                                    k8s control plane pod 运行
                                    launcherd 被 disable
                                    postgres 运行检查
                                    pgaf 运行检查
                                    containerd  运行检查
                                    file server 被 disable
                                    tower server 运行
                                    业务 pod 都不运行
                                    embed-monitor 组件 grafana-server 默认不启用
                                    embed-monitor 组件 vm-single 运行
                                    embed-monitor 组件 vm-agent 运行
                                    embed-monitor 组件 vector 运行
                                    ntpm 运行
                                    node-exporter 运行
                                    ingress-nginx-controller 运行
                                    everoute-agent 运行
                                    kube-proxy 运行
                                    node-local-dns 运行
                                    vip 网卡运行正常，检查网卡设置 ONBOOT 为 no
                                    HA 网卡运行正常，检查网卡设置 ONBOOT 为 yes
                                    k8s 证书检查
                                    支持的 UI 界面操作 - 可以编辑虚拟机组，移至组、从组内移出
                                    支持的 UI 界面操作 - 可以编辑虚拟机放置组，移至组、从组内移出
                                    支持的 UI 界面操作 - 创建快照、查看详情、编辑快照基本信息、编辑标签、删除快照
                                    支持的 UI 界面操作 - 加入快照计划，并生成快照组
                                    支持的 UI 界面操作 - 集群内冷迁移、集群内热迁移
                                    支持的 UI 界面操作 - 关联标签、移除标签
                                    支持的 UI 界面操作 - 打开终端并可正常输入命令
                                    支持的 UI 界面操作 - 查看网络链路，跳转到集群的网络拓扑页面
                                仲裁节点检查
                                    postgres 运行检查
                                    pgaf 运行检查
                                    embed-monitor 组件 vm-agent 运行
                                    embed-monitor 组件 vector 运行
                                    HA 网卡运行和配置检查
                                    支持的 UI 界面操作 - 可以编辑虚拟机组，移至组、从组内移出
                                    支持的 UI 界面操作 - 可以编辑虚拟机放置组，移至组、从组内移出
                                    支持的 UI 界面操作 - 创建快照、查看详情、编辑快照基本信息、编辑标签、删除快照
                                    支持的 UI 界面操作 - 加入快照计划，并生成快照组
                                    支持的 UI 界面操作 - 集群内冷迁移、集群内热迁移
                                    支持的 UI 界面操作 - 关联标签、移除标签
                                    支持的 UI 界面操作 - 打开终端并可正常输入命令
                                    支持的 UI 界面操作 - 查看网络链路，跳转到集群的网络拓扑页面
                                其他
                                    如果 active 和 passive 在同一集群上，自动启用「必须放置在不同主机」的放置组策略
                                    如果 active 和 passive 和 witness 在同一集群上，自动启用「必须放置在不同主机」的放置组策略
                                    如果 active 和 witness 在同一集群上，自动启用「必须放置在不同主机」的放置组策略
                                    如果 passive 和 witness 在同一集群上，自动启用「必须放置在不同主机」的放置组策略
                                    active 虚拟机被标识为系统服务，不能手动对 vm 做一些运维操作，所在集群不能移除
                                    passive 虚拟机被标识为系统服务，不能手动对 vm 做一些运维操作，不能移除所在集群
                                    witness 节点如果在 Tower 上纳管，虚拟机也被标识为系统服务，不能手动对 vm 做一些运维操作，不能移除所在集群
                                    文件复制方式为异步
                                    etcd 数据会迁移至 kine，检查组件状态正常
                                    已有的系统服务的安装包会迁移到 fileserver
                                    查看 postgreSQL 中创建的资源的键值对存在，例如 namespace
                                    使用 kubectl get pods -A 可以正常查询出 pods 的信息
                                    使用 kubectl get nods 可以正常查询出集群节点的状态
                                任务和事件
                                    检查成功任务：配置 CloudTower 高可用。
                                    产生成功的用户事件：配置 CloudTower 高可用。
                                集群主机操作
                                    active/passive/witness 节点在同一集群，一键提升虚拟卷副本数，三个节点的副本数均提升
                                    active/passive/witness 节点在不同集群，某个集群上的节点副本数被提升时，允许节点间副本数不同
                                    active 和 passive 节点副本数不同，不影响 failover 后 passive 提升为主节点
                                    active/passive/witness 节点在 SMTX OS 515 集群上，所在主机进入维护模式，会忽略放置组规则允许迁出
                                    active/passive/witness 节点在 SMTX ELF 630 集群上，所在主机进入维护模式，会忽略放置组规则允许迁出
                                    active 节点在 SMTX OS 507 集群上，所在主机进入维护模式，无法迁出，检查报错信息中包含 active VM 名称
                                    passive 节点在 SMTX OS 507 集群上，所在主机进入维护模式，无法迁出，检查报错信息中包含 passive VM 名称
                                    witness 节点在 SMTX OS 507 集群上，所在主机进入维护模式，无法迁出，检查报错信息中包含 witness VM 名称
                                    主机未进入维护模式，关闭 active 节点所在主机 - 弹窗上存在 HA 相关的提示，检查不通过报错，无法关闭主机
                                    主机未进入维护模式，关闭 witness 节点所在主机 - 弹窗上存在 HA 相关的提示，检查不通过报错，无法关闭主机
                                    主机未进入维护模式，关闭 passive 节点所在主机 - 弹窗上存在 HA 相关的提示，检查不通过报错，无法关闭主机
                                    主机进入维护模式中，关闭 active 节点所在主机 - 弹窗上存在 HA 相关的提示，检查不通过报错，无法关闭主机
                                    主机进入维护模式中，关闭 witness 节点所在主机 - 弹窗上存在 HA 相关的提示，检查不通过报错，无法关闭主机
                                    主机进入维护模式中，关闭 passive 节点所在主机 - 弹窗上存在 HA 相关的提示，检查不通过报错，无法关闭主机
                                    主机未进入维护模式，重启 active 节点所在主机 - 弹窗上存在 HA 相关的提示，检查不通过报错，无法重启主机
                                    主机未进入维护模式，重启 witness 节点所在主机 - 弹窗上存在 HA 相关的提示，检查不通过报错，无法重启主机
                                    主机未进入维护模式，重启 passive 节点所在主机 - 弹窗上存在 HA 相关的提示，检查不通过报错，无法重启主机
                                    主机进入维护模式中，重启 active 节点所在主机 - 弹窗上存在 HA 相关的提示，检查不通过报错，无法重启主机
                                    主机进入维护模式中，重启 witness 节点所在主机 - 弹窗上存在 HA 相关的提示，检查不通过报错，无法重启主机
                                    主机进入维护模式中，重启 passive 节点所在主机 - 弹窗上存在 HA 相关的提示，检查不通过报错，无法重启主机
                                    active/passive/witness 节点在 SMTX OS 630 集群上，所在主机进入维护模式，会忽略放置组规则允许迁出
                            部署失败
                                HA 页面展示
                                    HA 界面会展示失败步骤及原因
                                    HA 界面只保留最近一次的失败部署记录
                                    如果失败后，不能保持单点状态，检查下是否还会展示上面的单点提示。- 设计/前端上目前的处理都是启用失败，都是报仍为单点 tower 这样的报错信息
                                重试部署
                                    在预检查阶段失败，界面提供重试按钮，再重新发起部署，自动填充上次的配置
                                    主动节点 HA 网络配置失败，界面提供重试按钮，再重新发起部署，自动填充上次的配置
                                    被动节点 HA 网络配置失败，界面提供重试按钮，再重新发起部署，自动填充上次的配置
                                    部署前检查阶段失败，界面提供重试按钮，再重新发起部署，自动填充上次的配置
                                    集群部署阶段失败，界面上不提供重试按钮，需要人工介入处理才能重新部署
                                    部署仲裁节点失败，界面上不提供重试按钮，需要人工介入处理才能重新部署
                                    转主动节点失败，概率环境会异常，需要人工介入处理才能重新部署
                                    被动节点加入 HA 失败，界面上不提供重试按钮，需要人工介入处理才能重新部署
                                    应用适配高可用失败，界面上不提供重试按钮，需要人工介入处理才能重新部署
                                    HA 部署状态检查失败，界面上不提供重试按钮，需要人工介入处理
                                    HA 部署最后的清理失败，界面上不提供重试按钮，需要人工介入处理
                                    重试自动填充配置后，检查配置的编辑和再次提交
                                    重试的 HA 部署，如果没有人为故障，能够部署成功
                                    需要人工介入处理的，在运维文档里体现操作细节
                                    重试的时候自动填充配置，如果 vlan 已被删除，自动留空
                                    重试的时候自动填充配置，如果 passive 虚拟机已被删除，自动留空
                                任务和事件
                                    产生失败的任务：配置 CloudTower 高可用，检查任务信息。
                                    产生失败的事件：配置 CloudTower 高可用，检查事件信息。
                                Tower 状态
                                    在预检查阶段失败，CloudTower 仍保持单点状态正常工作
                                    在 HA 网络配置阶段失败，CloudTower 仍保持单点状态正常工作
                                    在 HA 部署前预检查阶段失败，CloudTower 仍保持单点状态正常工作
                                    在部署 witeness 阶段失败，CloudTower 仍保持单点状态正常工作
                                    在部署 active 节点阶段失败，CloudTower 不能保持单点状态正常工作
                                    在加入 passive 节点阶段失败，CloudTower 仍保持单点状态正常工作，但是不建议客户使用
                                    HA 部署完状态检查阶段失败，不能保证 HA 正常工作
                        场景测试
                            部署失败，然后重试部署，仍然部署失败
                            部署失败，排查失败的原因，并修复后重试部署，部署成功
                            部署失败，然后重试部署，出现新的问题，仍然部署失败
                            部署失败，再使用别的配置进行部署，部署成功
                            部署失败，再使用别的配置进行部署，部署过程出现问题，部署失败
                            三个节点的时区不一致，能部署成功，各个节点使用内部的 ntp server 同步成一致  --这个阶段不一定做
                            Tower 有配置 ntp server，部署 HA 集群
                            Tower 未配置 ntp server，部署 HA 集群
                            tower 部署好所有的系统服务，然后把 tower 转成 HA，HA 部署成功后，检查所有的系统服务工作正常，再对所有的系统服务做升级运维能成功
                            tower 转HA，再新部署系统服务服务，检查系统服务的工作正常
                            Tower 未配置 nameserver，部署 HA
                            Tower 配置错误的 nameserver，部署 HA
                            Tower 配置 ipv6 地址的 nameserver，部署 HA，启用成功后，三个节点的 /etc/resolv.conf 配置对齐，与 active 对齐
                            Tower 配置有效的 nameserver，部署 HA
                            升级至 4.8.0 - 部署 CloudTower HA 节点，配置 HA
                            部署时，触发 active 节点集群内热迁移，预期不影响 HA 部署
                            部署时，触发 active 节点跨集群分段迁移，预期不影响 HA 部署
                            部署时，触发 passive 节点集群内热迁移，预期不影响 HA 部署
                            部署时，触发 passive 节点跨集群热迁移，预期不影响 HA 部署
                            部署时，触发 Tower 升级操作，预期不会升级，返回错误信息
                            原单节点为 centos7.x86_64 Tower - 升级后启用 HA 配置成功
                            原单节点为 oe2003.x86_64 Tower - 升级后启用 HA 配置成功
                            原单节点为 aarch64 Tower - 升级后启用 HA 配置成功
                            原单节点为低配，提升为高配 - 升级后启用 HA 配置成功
                            原单节点为 UI installer 部署的 Tower - 升级后不支持部署 HA
                            原单节点为 VM install 部署的 Tower - 升级后启用 HA 配置成功
                            转 HA 后，使用之前的安装包全新部署系统服务
                            转 HA 之后检查所有系统服务的 license 信息
                            三个节点的时间不一致，能部署成功，各个节点使用内部的 ntp server 同步成一致
                            HA 部署好之后，给 tower 配置一个时间差异很大的 ntp server，检查不会出现时间跳变
                            部署 HA，同步升级物理集群，HA 部署成功
                            原节点为低配，提升为高配后 - 可启用 HA 并成功
                            启用 HA 之前，将三个节点的 /etc/resolv.conf 文件删除 - 启用 HA 会失败
                            active 没有 /etc/resolv.conf、passive 未配置 nameserver、witness 配置错误的 nameserver - 启用 HA 会失败
                            active 存在有效的 nameserver、passive 没有 /etc/resolv.conf、witness 未配置 nameserver - 启用 HA 成功
                            active 未配置 nameserver、passive 配置错误的 nameserver、witness 没有 /etc/resolv.conf - 启用 HA 成功
                            active 配置 ipv6 的 nameserver、passive 和 witness 存在有效的 nameserver - 启用 HA 成功
                            新部署的 AOC，启用 HA 之后，部署所有系统服务成功，手动和自动 failover 成功，系统服务和 AOC 正常
                            低版本已部署所有系统服务的 AOC，升级之后，启用 HA 成功，手动和自动 failover 成功，系统服务和 AOC 正常
                        文件系统
                            active xfs 文件系统 + passive xfs 文件系统 + witness xfs 文件系统 - 不支持启用 HA
                            active ext4 文件系统 + passive ext4 文件系统 + witness ext4 文件系统 - HA 集群运行正常
                            active ext4 文件系统 + passive ext4 文件系统 + witness ext4 文件系统 - HA 集群异常后，无法通过备份重建恢复，不支持 HA 模式的备份
                    权限控制
                        新增「CloudTower高可用」权限，检查权限页面
                        内置角色：超级管理员具有该权限，可以进行 Tower HA 的配置
                        内置角色：运维管理员具有该权限，可以进行 Tower HA 的配置
                        内置角色：非超级管理员和运维管理员的其他角色，不具有 CloudTower 高可用权限。不能进行 Tower HA 的配置操作，页面展示无权限的提示。
                        自定义角色：配置该权限的角色，如果 Tower 未配置HA，可以进行 Tower HA 的配置操作。
                        自定义角色：未配置该权限的角色，不具有 CloudTower 高可用权限。不能进行 Tower HA 的配置操作，页面展示无权限的提示。
                        新增角色和编辑角色，检查事件中该权限的描述
                    API 测试
                        成功启用三节点（active + passive + witness）高可用模式。
                        尝试在已启用 HA 的环境中再次启用，直接返回错误信息。
                        请求中缺少必填字段，如 deployMode ，返回错误信息。
                        节点角色填写错误，如 active->master，返回错误信息。
                        witness 节点填写不需要的字段，如 vmId 这些。
                        active/passive 节点缺少管理网络配置。
                        active/passive 节点缺少 HA 网络配置。
                        IP 地址格式错误。
                        active，passive，witness 三节点中任意 ha ip 相同，不能部署，返回对应错误信息
                        低配的 Tower 提交部署 HA，API 返回错误提示：仅高配的 CloudTower 支持启用高可用。
                        升级中的 Tower 启用 HA，返回错误信息
                        passive 节点存在网卡，启用 HA 返回错误信息
            HA 升级
                UI 升级
                    三节点 HA 升级
                        升级页面检查
                            「当前版本」信息
                                「系统配置- CloudTower 升级」展示当前版本信息：CloudTower 版本、内核版本、CPU架构、操作系统
                            HA 未就绪提示
                                HA 部署失败状态，升级页面展示「CloudTower 高可用（HA）状态未就绪」提示信息。
                                HA 部署中，升级页面展示「CloudTower 高可用（HA）状态未就绪」提示信息。
                                等到 HA 部署完成，「CloudTower 高可用（HA）状态未就绪」提示信息隐藏。
                                仲裁节点 down，集群 unhealthy 状态，升级页面展示「CloudTower 高可用（HA）状态未就绪」提示信息。
                                仲裁节点恢复正常，HA 状态 ready 后，「CloudTower 高可用（HA）状态未就绪」提示信息隐藏。
                                主节点 down，集群 recovering 状态，UI 不可访问
                                备节点 down，仲裁正常，主节点 Wait_Active-》集群 demoted 状态，升级页面展示「CloudTower 高可用（HA）状态未就绪」提示信息。
                                备节点 catching-up，仲裁正常，主节点 Wait_Active-》集群 demoted 状态，升级页面展示「CloudTower 高可用（HA）状态未就绪」提示信息。
                                主备恢复正常，HA 状态从 demoted 变成  ready 后，「CloudTower 高可用（HA）状态未就绪」提示信息隐藏。
                                备节点从主节点同步数据-》集群 Catching Up 状态，升级页面展示「CloudTower 高可用（HA）状态未就绪」提示信息。
                                数据同步完，HA 状态从 Catching Up 变成 ready 后，「CloudTower 高可用（HA）状态未就绪」提示信息会消失。
                                仲裁节点和备节点 down，升级页面展示「CloudTower 高可用（HA）状态未就绪」提示信息。
                                仲裁节点和备节点恢复，HA 状态变成 ready 后，「CloudTower 高可用（HA）状态未就绪」提示信息会消失。
                                提示 HA 状态未就绪时，点击「查看 HA 集群」跳转到 「CloudTower 高可用」页面
                                未上传升级文件，HA 状态未就绪的提示，在上面文件区域的上方
                                已上传升级文件，HA 状态未就绪的提示，在升级文件区域的下方
                                升级失败和HA 状态未就绪的两个错误提示同时出现
                            操作按钮禁用
                                HA 状态 down，这时 UI 应该不可用，无法上传升级文件
                                HA 状态 Recovering，这时 UI 应该不可用，无法上传升级文件
                                HA demoted 状态，不能上传升级文件，禁用本地上传，url 上传操作
                                HA unhealthy 状态，不能上传升级文件，禁用本地上传，url 上传操作
                                HA catching up 状态，不能上传升级文件，禁用本地上传，url 上传操作
                                HA ready 状态，可以上传升级文件
                                HA 状态 down，这时 UI 应该不可用，无法做升级操作
                                HA 状态 Recovering，这时 UI 应该不可用，无法做升级操作
                                HA demoted 状态，不能发起升级操作，禁用检查环境和升级按钮
                                HA unhealthy 状态，不能发起升级操作，禁用检查环境和升级按钮
                                HA catching up 状态，不能发起升级操作，禁用检查环境和升级按钮
                                HA ready 状态，可以发起升级操作，检查环境和升级按钮可用
                                Tower 订阅许可过期，允许从「系统配置 > CloudTower」操作上传文件、删除文件、独立预检查、启动升级
                                Tower 试用许可过期，上传文件、删除文件、独立预检查、启动升级 这些操作会报错许可已过期
                        上传升级文件
                            校验文件，清单文件中升级文件版本低于 tower 当前实际版本时，展示错误提示
                            校验文件，清单文件中，升级文件 cpu 架构信息和当前 tower 虚拟机实际架构不同时，展示错误提示
                            校验文件，清单文件中，升级文件操作系统发行版信息和当前 tower 不同时，展示错误提示
                            上传完成后出现「检查环境」、「升级」按钮
                            上传完升级文件后，「本地上传」和「URL 上传」将不再展示
                            上传过升级文件程中，中止上传，分块上传立刻中止，tower 虚拟机内已经上传的分块会被清理
                            「上传 CloudTower 升级文件」任务因手动终止失败，展示指定的错误信息
                            url 上传，launcherd 下载文件过程中中断，任务失败，产生失败的事件审计
                            本地上传升级文件成功
                            url 上传升级文件成功
                            升级文件上传，升级文件存放在主节点，不做其他节点的同步
                            上传升级文件之后，发生 failover，新的主节点没有对应的升级文件，需要重新上传
                            上传升级文件的过程中，触发 failover，上传升级文件失败
                            上传升级文件的过程中，随机断开节点之间的网络，未触发 failover，不影响升级文件上传成功
                            上传升级文件的过程中，挂掉备节点，集群进入 demoted 状态，不影响升级文件上传成功
                            上传升级文件的过程中，挂掉仲裁节点，集群进入 unhealthy 状态，不影响升级文件上传成功
                            上传升级文件的过程中，触发 catching up，不影响升级文件上传成功
                            上传升级文件的过程中，挂掉主节点，上传任务失败
                        删除升级文件
                            上传完毕后，页面可操作删除升级文件，弹出二次确认 modal，在 tower 虚拟机文件系统删除升级文件
                            上传完升级文件后，无法再上传升级文件，从页面删除升级文件后，上传文件可用
                            主动删除升级文件产生 tower 任务
                            上传完升级文件之后，如果发生了 failover，UI 上继续展示升级文件预览，进入页面时会展示错误信息，并且禁用升级和检查环境的 button。
                            上传完升级文件之后，如果发生了 failover，不能提交升级任务，升级按钮 disable
                            使用升级文件完成 tower 升级后，升级文件自动被清理，检查三个节点都不会有残留
                        独立环境检查
                            新增检查项：「CloudTower 高可用（HA）状态」检查项
                            仲裁节点 down，集群 unhealthy 状态，「CloudTower 高可用（HA）状态」检查项不通过，环境检查失败，检查错误信息正确
                            备节点 down，集群 demoted 状态，「CloudTower 高可用（HA）状态」检查项不通过，环境检查失败，检查错误信息正确
                            备节点从主节点同步数据，集群 Catching Up 状态，「CloudTower 高可用（HA）状态」检查项不通过，环境检查失败，检查错误信息正确
                            仲裁节点和备节点 down，「CloudTower 高可用（HA）状态」检查项不通过，环境检查失败，检查错误信息正确
                            检查项回归： tower pods crash
                            检查项回归： 版本判断、cpu 架构、操作系统
                            检查项回归： 规格检查，这里应该判断主、备、仲裁三节点（witness 还没加）
                            检查项回归：占用磁盘空间，这里应该判断主、备、仲裁三节点
                            检查项回归：IO await，判断主、备、仲裁三节点
                            检查项回归：k9s 进程，判断主、备节点
                            最近一次「独立预检查」失败，升级按钮 disable
                            最近一次「独立预检查」所有检查项均通过，「升级」按钮 enable
                        HA 升级
                            触发升级操作
                                点击「升级」按钮后，出现二次确认弹窗，确认后 tower 页面展示顶部 banner 提示正在进行升级，存在「查看进度」按钮，点击后在新标签页打开独立升级页
                                「系统配置 - CloudTower 升级」页中「升级」Tab 页出现正在升级提示，存在「查看进度」按钮，在新标签页访问独立升级页 url
                                确认升级后，「系统配置 - CloudTower 升级」页中的「删除文件」、「检查环境」、「升级」按钮无法点击
                                确认升级后，产生「将 CloudTower 从版本 xxx 升级至 xxx」任务，任务卡片提供「详情」按钮，点击在新窗口打开「独立升级页」
                                「将 CloudTower 从版本 xxx 升级至 xxx」任务进行中时，任务卡片能展示当前阶段「正在检查环境」或「正在升级」
                                「将 CloudTower 从版本 xxx 升级至 xxx」任务失败时，任务卡片中展示失败信息，以及跳转链接
                                多个浏览器标签页同时点击「升级」按钮并在二次确认，只有一个能够发起
                                发起升级操作之后，不再展示在此之前的预检查结果
                            HA 升级场景
                                先在界面上发起 cloudtower 升级，已经通过预检查进行到正式升级步骤，此时发起命令行升级，预期操作失败
                                先在 tower 虚拟机系统内发起命令行升级，此时在界面上发起 cloudtower 升级，预期请求失败
                                先在 tower 虚拟机系统内执行 instaler update，随后在界面上发起 cloudtower 升级，预期请求失败
                                先在界面上发起 cloudtower 升级，随后在 tower 虚拟机系统内执行 installer update，预期操作失败
                                在界面上发起 cloudtower 升级后，操作 active 虚拟机重启，预期会触发 failover，升级任务会失败，确认 tower 任务、事件审计、升级记录、独立升级页的显示
                                在界面上发起 cloudtower 升级后，操作 active 虚拟机强制关机，预期会触发 failover，升级任务会失败，确认 tower 任务、事件审计、升级记录、独立升级页的显示
                                在界面上发起 cloudtower 升级后，操作 active/passive 虚拟机热迁移，预期不影响升级任务
                                系统预检查失败，升级任务失败，检查升级结果和升级页面
                                解压升级文件失败，升级任务失败，检查升级结果和升级页面
                                升级 launcherd 失败，升级任务失败，检查升级结果和升级页面
                                同步升级文件到仲裁节点失败，升级任务失败，检查升级结果和升级页面
                                升级仲裁节点失败，升级任务失败，检查升级结果和升级页面
                                同步升级文件到被动节点失败，升级任务失败，检查升级结果和升级页面
                                升级被动节点失败，升级任务失败，检查升级结果和升级页面
                                升级主动节点失败，升级任务失败，检查升级结果和升级页面
                                检查 HA 集群状态失败，升级任务失败，检查升级结果和升级页面
                                触发升级后，launcherd 有重启，检查任务能正常结束
                                升级完成后，清理升级文件失败，不影响升级成功的结果
                                低版本升级到 Tower 480 后，转 HA 集群，再做 HA 升级，检查升级能成功，历史的升级任务不会丢失
                                升级前部署好系统服务，升级完成检查系统服务的状态正常
                                升级前部署好系统服务，HA 升级完成，对系统服务做运维能成功
                                HA 升级成功后，预期各节点的角色不会发生改变
                                升级成功后，检查各节点上组件运行情况
                                HA 升级，预期不触发节点和集群状态相关告警
                                需要覆盖所有不同 tower 安装包的升级
                                升级过程中，passive 或者 witness 异常，升级任务失败
                            升级失败 banner
                                触发升级，在检查环境阶段失败，顶部展示警告 banner「CloudTower 升级的环境检查不通过。请解决问题后，重新尝试升级。详情」点击详情在新标签页打开「独立升级页」
                                触发升级，在升级阶段失败，顶部展示警告 banner「CloudTower 升级失败，请勿进行业务变更。请联系售后。 详情」点击详情在新标签页打开「独立升级页」
                                没有升级权限的用户，可以看见检查环境失败的顶部 banner，但不显示「详情」按钮
                                没有升级权限的用户，可以看见升级失败的顶部 banner，但不显示「详情」按钮
                                多个 banner 的上下顺序：许可过期> 升级失败> 用户密码过期
                                如果检查环境失败，重新触发单独检查环境，检查环境失败提示的 banner 不消失，重新触发升级后消失。
                                如果检查环境失败，重新触发检查环境仍然失败，会再次展示检查环境失败提示的 banner
                                如果升级失败，用户无法在 UI 再次操作升级，升级失败的 banner 一直保持
                                如果升级失败，后台处理升级成功后，升级失败的 banner 消失
                        独立升级页
                            独立升级页，密码输入框为空时，「查看进度」按钮无法点击，密码输入框有内容时，「查看进度」按钮变为可点击
                            访问独立升级页显示「CloudTower 升级」，输入 cloudtower 账户密码完成认证后，打开页面会显示最近一次的升级任务进度
                            如果没有升级记录，独立升级页展示无升级记录的提示，并可点击提示信息里的「CloudTower 升级页面」打开升级页面。
                            独立升级页 token 有效期 24 小时
                            独立升级页可切换中英文，aoc 只能使用英文
                            进度页展示升级的目标版本以及当前进度，仅展示一个进度条，进度条展示整个升级行为的开始时间，已用时间，以及当前步骤
                            升级步骤检查：解压安装包，升级 launcherd，先做预检查，同步升级文件到备和仲裁节点，“备-仲裁-主”依次升级，最后检查 HA 集群状态。
                            检查升级环境的检查项有「HA 状态」、「目标版本高于当前版本」、「CloudTower 高可用（HA）状态」、「cpu 架构、操作系统与当前 tower 匹配」、「虚拟机的 I/O 等待不超过 30 ms」、「文件系统可用空间充足」、「不存在k9s进程」、「cloudtower pods 均处于运行中状态」、「CloudTower 未安装临时补丁」
                            「检查升级环境」存在未通过项时，「只看未满足」toggle默认开启，展示未通过项
                            「检查升级环境」存在多条未通过项，一一展示错误信息
                            「检查升级环境」失败时，在「tower > 系统配置 > CloudTower 升级> 升级记录」页产生一条失败的记录
                            升级过程中、升级失败、升级成功，可查看升级日志，默认展开可折叠，展开后显示日志查看器，自动定位到最新日志，宽度高度固定，自动换行。支持搜索，搜索命中高亮，搜索框支持粘贴，支持复制文本
                            升级日志，查看器检索默认为正则搜索、且大小写不敏感，高亮命中内容
                            升级日志，查看器固定高度，内部有滚动滑块
                            升级失败，展示失败步骤，展示错误信息，日志查看器默认定位到本次升级日志的结尾
                            升级失败，出现「打开 CloudTower 」按钮，点击后在新的标签页访问 tower overview 页面
                            升级失败，在「tower > 系统配置 > CloudTower 升级 > 升级记录」页产生一条失败的记录
                            升级成功，在「tower > 系统配置 > CloudTower 升级 > 升级记录」页产生一条成功的记录
                            升级页面始终展示「打开 CloudTower 」按钮，点击后在新的标签页访问 tower overview 页面
                        任务和事件
                            升级成功的任务和事件信息检查
                            升级失败的任务和事件信息检查
                    权限控制
                        没有 「Cloud Tower HA」的管理权限，但是有 「CloudTower 升级」权限，可以进行上传升级文件和升级 Tower 的操作
                        有 「Cloud Tower HA」的管理权限，没有 「CloudTower 升级」权限，在「系统配置」导航栏无法看到「CloudTower 升级」项
                        有「CloudTower 升级」权限，可以进行上传升级文件和升级 Tower 的操作
                        无「CloudTower 升级」权限的用户，在「系统配置」导航栏无法看到「CloudTower 升级」项
                        无「CloudTower 升级」权限的用户，当前 Tower 出现升级提示的顶部 banner 时，不显示「查看进度」按钮
                        无「CloudTower 升级」权限的用户，当前 Tower 出现升级失败提示的顶部 banner 时，不显示「详情」按钮
                        无「CloudTower 升级」权限的用户，当前 Tower 出现升级环境检查失败提示的顶部 banner 时，不显示「详情」按钮
                        无「CloudTower 升级」权限的用户，无法查看 Tower 任务卡片的详情：“上传升级文件”、“删除升级文件”、“将 CloudTower 从 xxx 升级到 xxx”
                        无「CloudTower 升级」权限的用户，无法在“上传升级文件”任务卡片操作中止
                        有「CloudTower 升级」权限的用户，当前 Tower 出现升级提示的顶部 banner 时，显示「查看进度」按钮
                        有「CloudTower 升级」权限的用户，当前 Tower 出现升级失败提示的顶部 banner 时，显示「详情」按钮
                        有「CloudTower 升级」权限的用户，当前 Tower 出现升级环境检查失败提示的顶部 banner 时，显示「详情」按钮
                        有「CloudTower 升级」权限的用户，可以查看 Tower 任务卡片的详情：“上传升级文件”、“删除升级文件”、“将 CloudTower 从 xxx 升级到 xxx”
                        有「CloudTower 升级」权限的用户，可以在“上传升级文件”任务卡片操作中止
                        内置角色 - 运维管理员有「CloudTower 升级」管理权限
                        内置角色 - 超级管理员有「CloudTower 升级」管理权限
                        其他内置角色没有「CloudTower 升级」的管理权限
                cli 升级
                    命令行升级，界面上有升级相关 banner 提示
                    命令行升级时，UI 上无法再发起升级请求
                    UI 上正在升级中，触发命令行升级会提示升级中，不能再次升级
                    命令行升级时，可以在 UI 访问独立升级页面查看升级进度
                    命令行升级成功，UI 上能看到任务记录，不产生事件
                    命令行升级失败，UI 上能看到任务记录，不产生事件
                    命令行升级成功，UI 上能看到升级记录，升级详情和日志
                    命令行升级失败，UI 上能看到升级记录，升级详情和日志
                    命令行升级失败，UI 上有告警
                    命令行升级失败，可以处理失败原因后，在 UI 上再次发起升级
            HA 运行
                HA - 正常状态
                    HA 页面展示
                        HA 部署好之后，HA 页面展示 HA 拓扑图，及各节点的信息
                        主节点始终在左，被动节点始终在右，仲裁节点显示在下方
                        不同分辨率下，页面的整体展示 ok
                        active、passive 节点卡片正确展示 IP、子网、网关的信息
                        witness 节点卡片只展示 ip
                        如果 tower 未关联 obs，页面顶部显示未关联可观测 1.2.0 的 Tip
                        关联可观测 1.2.0 以上版本后，顶部提示 tip 消失
                        用户有可观测性服务管理权限 - 顶部提示关联可观测的 tip 展示 “关联可观测性服务” 按钮
                        点击 “关联可观测性服务” 的按钮 - 跳转至可观测性页面
                        用户没有可观测性服务管理权限 - 顶部提示关联可观测的 tip 不展示 “关联可观测性服务” 按钮
                        英文界面下 - 正常翻译为英文
                    监控告警
                        监控组件
                            主、备节点上通过 systemd 部署 postgres-exporter
                            主、备节点上的 ha-controller 采集 ping/pgaf/lsyncd 指标，witness 节点上的 ha -controller  采集 pgaf/ping 指标
                            ha-controlle 的 metrics API 获取自身指标，metrics/ha API 获取 pgaf/ping/lsyncd/postgres-exporter 相关指标
                            主备节点的 vmagent 会配置主备节点的 vmsingle 地址实现多写
                            主备节点的 vector 会配置主备节点的 vlsingle 地址实现多写
                            三节点部署时，每个节点都将部署日志和指标采集和存储组件
                        日志存储和查询
                            在 tower 主、备节点上启动 grafana，均可以查询到 tower 主/备/witness 采集的指标信息
                            tower 上部署可观测性服务，并关联 tower 自身，可以在可观测性平台的 grafana 面板查询到 tower 主/备/witness 采集的日志
                        指标存储和查询
                            ha 相关监控指标来源于 postgres-exporter/ping/lsyncd/pgaf
                            指标中的 static_configs 设置 relabel_configs，标识指标的来源节点 HA 网卡 ip。查询指标时可依据来源 ip 查询
                            在 tower 主、备节点上启动 grafana，均可以查询到 tower 主/备/witness 采集的指标信息
                            tower 上部署可观测性服务，并关联 tower 自身，可以在可观测性平台的 grafana 面板查询到 tower 主/备/witness 采集的指标信息
                            指标中会区分指标来源的角色，标识主、备
                        内置告警
                            资源使用率告警
                                增加 HA 节点 cpu 占用过高的告警规则：运行 CloudTower 高可用节点的虚拟机{.vm_IP} 的 CPU 占用过高。默认阈值为 90%，注意
                                主动节点 cpu 占用超过 90%，产生告警，检查告警文案信息正确
                                主动节点产生 cpu 占用高的告警之后，降低 cpu 占用，告警能及时清除
                                被动节点 cpu 占用超过 90%，产生告警，检查告警文案信息正确
                                被动节点产生 cpu 占用高的告警之后，降低 cpu 占用，告警能及时清除
                                仲裁节点 cpu 占用超过 90%，产生告警，检查告警文案信息正确
                                仲裁节点产生 cpu 占用高的告警之后，降低 cpu 占用，告警能及时清除
                                修改 cpu 过高的告警阈值，修改后能生效，主动被动仲裁节点都按照新的阈值告警
                                增加 HA 节点内存使用率过高的告警：运行 CloudTower 高可用节点的虚拟机{.vm_IP} 的存储空间不足。默认阈值为 80%，注意
                                主动内存使用率超过 80%，产生告警，检查告警文案信息正确
                                主动节点产生内存使用率过高的告警之后，降低内存占用，告警能及时清除
                                被动节点内存使用率超过 80%，产生告警，检查告警文案信息正确
                                被动节点产生内存使用率过高的告警之后，降低内存占用，告警能及时清除
                                仲裁节点内存使用率超过 80%，产生告警，检查告警文案信息正确
                                仲裁节点产生内存使用率过高的告警之后，降低内存占用，告警能及时清除
                                修改内存使用率过高的告警阈值，修改后能生效，主动被动仲裁节点都按照新的阈值告警
                                增加 HA 节点磁盘空间不足的告警：运行 CloudTower 高可用节点的虚拟机{.vm_IP} 的内存使用率过高。默认阈值为 90%，注意
                                主动磁盘使用率超过 90%，产生告警，检查告警文案信息正确
                                主动节点产生磁盘不足的告警之后，降低磁盘占用，告警能及时清除
                                被动节点磁盘使用率超过 90%，产生告警，检查告警文案信息正确
                                被动节点产生磁盘不足的告警之后，降低磁盘占用，告警能及时清除
                                仲裁节点磁盘使用率超过 90%，产生告警，检查告警文案信息正确
                                仲裁节点产生磁盘不足的告警之后，降低磁盘占用，告警能及时清除
                                修改磁盘不足的告警阈值，修改后能生效，主动被动仲裁节点都按照新的阈值告警
                                单 Tower 的告警规则不生效：运行 { .service_type } { .service_name } 的虚拟机 { .vm_name } 的 CPU 占用过高。
                                单 Tower 的告警规则不生效：运行 { .service_type } { .service_name } 的虚拟机 { .vm_name } 的存储空间不足。
                                单 Tower 的告警规则不生效：运行 { .service_type } { .service_name } 的虚拟机 { .vm_name } 的内存使用率过高。
                                报警通知选一个通路回归一下
                            NTP 告警
                                单 Tower 已有的告警规则生效：{ .service_type } { .service_name } 未配置 NTP 服务器。
                                如果 CloudTower 未配置外部 NTP 服务器，产生告警。
                                CloudTower 配置好外部 NTP 服务器，告警清除。
                                修改未配置 NTP 服务器的告警规则，能生效。
                                单 Tower 的已有告警规则生效：{ .service_type } { .service_name } 无法与 NTP 服务器 { .ntp_server } 建立连接。
                                CloudTower 无法与外部 NTP 连接时，产生告警，检查文案信息正确。
                                CloudTower 与外部 NTP 连接恢复后，告警清除。
                                单 Tower 的已有告警规则对 HA 生效：CloudTower 与 NTP 服务器时间偏移量过大。
                                CloudTower 与 NTP 服务器时间偏移量大产生告警，检查文案信息正确。
                                CloudTower 与 NTP 服务器时间恢复一致，告警清除。
                                报警通知选一个通路回归一下
                        告警规则的注册
                            单  Tower 关联可观测，然后部署 HA，部署成功后，HA 相关告警规则自动注册
                            HA Tower 新关联可观测，HA 相关告警规则自动注册
                            HA Tower 移除关联可观测，HA 相关告警规则取消
                            HA Tower 没有关联可观测，Tower 上不展示 HA 相关告警
                    数据同步
                        上传的文件 - 存放至 fileserver 中，并通过 pgaf 同步至 passive 节点
                        触发的日志 - 存放至 fileserver 中，并通过 pgaf 同步至 passive 节点
                        保留的自动生成的报表 - 存放至 fileserver 中，并通过 pgaf 同步至 passive 节点
                        创建虚拟机，创建数据中心，造成 db 数据变化，然后切换主备，检查数据正确
                        上传系统服务安装包，并创建系统服务，然后切换主备，检查数据正确
                    手动 failover
                        无同步文件，手动 failover，预期主从切换成功，检查节点主从切换后的节点角色正确，集群状态正确
                        无同步文件，手动 failover成功后，检查主备节点上组件正确运行
                        无同步文件，手动 failover 成功后，检查切换记录，会记录一条手动主被切换的记录，信息正确
                        同步文件过程中，手动 failover，预期主从切换成功，检查节点主从切换后的节点角色正确，集群状态正确
                        同步文件过程中，手动 failover成功后，检查主备节点上组件正确运行
                        同步文件过程中，手动 failover 成功后，检查切换记录，会记录一条手动主被切换的记录，信息正确
                        同步文件过程中，手动 failover 成功后，同步中的那部分文件可能丢失
                HA - 状态转换
                    主动节点异常
                        节点故障
                            chaos-active-1：（1）集群 ready，模拟 Active 节点掉电 / VM 强制关机，witness 探测 active 超时，集群变为 recovering 状态，触发 failover，故障转移期间服务不可用。
                            chaos-active-1：（2）集群 recovering 状态， failover 完成后，passive 节点提升为 wait_active 状态，集群状态为 demoted，服务恢复可用。
                            chaos-active-1：（3）开机旧主节点，该节点先分配 catchingUp 角色从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                            chaos-active-2：（1）集群 ready，Active 节点磁盘损坏（PG 所在分区写满/损坏），预期进行 failover，故障转移期间服务不可用.
                            chaos-active-2：（2）集群 recovering 状态， failover 完成后，passive 节点提升为 wait_active 状态，集群状态为 demoted，服务恢复可用。
                            chaos-active-2：（3）恢复旧主节点磁盘空间，该节点先分配 catchingUp 角色从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                            chaos-active-3：（1）集群 ready，Active 节点内核 hang 死，预期触发 failover，集群变为 recovering 状态，故障转移期间服务不可用
                            chaos-active-3：（2）集群 recovering 状态， failover 完成后，passive 节点提升为 wait_active 状态，集群状态为 demoted，服务恢复可用。
                            chaos-active-3：（3）恢复旧主节点，该节点先分配 catchingUp 角色从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                            chaos-active-4：（1）集群 ready，active 虚拟机文件系统冻结，健康探测失败，active 转为 Down，集群变为 recovering 状态，触发 failover，故障转移期间服务不可用。
                            chaos-active-4：（2）集群 recovering 状态， failover 完成后，passive 节点提升为 wait_active 状态，集群状态为 demoted，服务恢复可用。
                            chaos-active-4：（3）恢复旧主节点，该节点先分配 catchingUp 角色从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                            chaos-active-5：（1）集群 ready，Active 节点 PG 挂掉，触发 failover，集群变为 recovering 状态，故障转移期间服务不可用。
                            chaos-active-5：（2）集群 recovering 状态， failover 完成后，passive 节点提升为 wait_active 状态，集群状态为 demoted，服务恢复可用。
                            chaos-active-5：（3）恢复旧主节点 PG，该节点先分配 catchingUp 角色从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                            chaos-active-6：集群 ready，Active 节点 CPU steal > 70% 导致 tower server 不可用， 不触发 failover
                            chaos-active-7：集群 recovering 状态，故障转移过程中 witness 节点异常，故障转移失败，集群目标状态为 down，手动恢复 witness 后可继续故障转移
                            chaos-active-8：集群 recovering 状态，故障转移过程中 passive 节点异常，故障转移失败，集群目标状态为 down，需要人工介入
                            chaos-active-9：集群 recovering 状态，故障转移过程中，旧 active 节点快速恢复，passive 继续提升为 active，就主节点作为新的 passive 加入。
                            chaos-active-10：故障转移完成，集群 demoted 状态，新 wait_active 节点异常，服务不可用，需要人工介入
                            chaos-active-11：故障转移完成，集群 demoted 状态，witness 节点异常，服务不可用，需要人工介入
                            chaos-active-12：集群 demoted 状态，旧主节点恢复，集群变为 catching up 状态，数据同步过程中，active 节点异常，集群 down，服务不可用（将无法自动故障转移，需要 active 恢复）
                            chaos-active-13：集群 demoted 状态，旧主节点恢复，集群变为 catching up 状态，数据同步过程中，witness 节点异常，数据继续同步，服务可用，集群变成 demoted 状态
                            chaos-active-14：集群 demoted 状态，旧主节点恢复，集群变为 catching up 状态，数据同步过程中 witness 节点异常，集群变成 demoted 状态。passive 节点再异常，集群 down，服务不可用。
                            chaos-active-15：集群 down，恢复 witness 节点，集群变为 demoted 状态，恢复 passive，分配 catching up 角色，开始数据同步，数据同步完成后，catching_up 变为 passive，集群 ready
                            chaos-active-16：短时间内多次 Active 节点挂起，不会触发频繁切换/脑裂
                            chaos-active-17：多次触发当前集群的 主节点故障，使主从连续多次切换
                            chaos-active-18：active 节点的 kubelet/containerd/cni/coredns 等故障，不会触发 pgaf 故障转移
                            chaos-active-19：active 重启，触发 failover，检查 HA 正常，active 起来后作为 passive 加入 HA，HA 集群最终 ready
                            chaos-active-20：active 在 fisheye 上关机，触发 failover，检查 HA 正常，active 起来后作为 passive 加入 HA，HA 集群最终 ready
                            chaos-active-21：active vm 里执行关机，触发 failover，检查 HA 正常，active 起来后作为 passive 加入 HA，HA 集群最终 ready
                        数据同步
                            主节点在上传安装包时异常 - 安装包上传失败
                            主节点在上传安装包时异常 - 自动 failover 并成功，记录一条主被切换的记录，信息记录正确
                            主节点在上传安装包时异常 - fileserver 服务在新 active 拉起，db 中无数据损坏
                            同步文件时，主异常 - 自动 failover 并成功，记录一条主被切换的记录，信息记录正确
                            同步文件时，主异常 - fileserver 服务在新 active 拉起，同步中的那部分文件可能丢失（可能会导致相关功能不可用）
                            failover 完成 - 原 passive 节点升级为 active 节点，worker queue 中开始存放文件
                            failover 完成，原 active 节点恢复后 - 降级为 passive 节点，开始从主节点同步文件
                        手动 failover
                            HA 集群自动 failover 过程中，通过 cli 手动 failover - 报错
                    被动节点异常
                        HA 页面展示
                            页面顶部会展示红色警示信息："被动节点异常，无法切换主被节点。当主动节点异常时，将无法进行故障转移"。
                            被动节点上的卡片展示「异常」状态，被动节点卡片变红色外框。
                        节点故障
                            chaos-passive-1：（1）passive 节点关机，active 节点状态变为 wait active，集群状态为 demoted，服务保持可用
                            chaos-passive-1：（2）passive 节点恢复，分配 catching up 角色，从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                            chaos-passive-2：（1）集群 ready，passive 节点磁盘损坏（PG 所在分区写满/损坏），active 节点状态变为 wait active，集群状态为 demoted，服务保持可用
                            chaos-passive-2：（2）passive 节点恢复，分配 catching up 角色，从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                            chaos-passive-3：（1）集群 ready，passive 节点内核 hang 死，active 节点状态变为 wait active，集群状态为 demoted，服务保持可用
                            chaos-passive-3：（2）passive 节点恢复，分配 catching up 角色，从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                            chaos-passive-4：（1）集群 ready，passive 节点 CPU steal > 90% ，passive 节点依然能正确响应 HA 探测
                            chaos-passive-5：（1）集群 ready，passive 节点 PG 挂掉，active 节点状态变为 wait active，集群状态为 demoted，服务保持可用
                            chaos-passive-5：（2）passive 节点恢复，分配 catching up 角色，从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                            chaos-passive-6：（1）passive 虚拟机文件系统冻结，健康监测失败，active 节点状态变为 wait active，passive 变为 down，集群状态为 demoted，服务保持可用
                            chaos-passive-6：（2）passive 节点恢复，分配 catching up 角色，从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                            chaos-passive-7：（1）passive 异常，pgaf 切换到异步复制，集群变为 demoted 状态，witness 节点再异常，集群状态 down，无法提供服务
                            chaos-passive-7：（2）down 状态时，恢复 witness 节点，集集群状态保持 down，无法提供服务
                            chaos-passive-8：（1）passive 异常，pgaf 未切换到异步复制，witness 节点再异常，集群状态 down，无法提供服务
                            chaos-passive-8：（2）down 状态时，恢复 witness 节点，集群转为 demoted 状态，可以提供服务
                            chaos-passive-9：（1）passive 节点异常，pgaf 未切换到异步复制，再让 active 异常，集群变成 down，无法提供服务
                            chaos-passive-9：（2） down 状态时，恢复 active 节点，集群状态保持 down，无法提供服务
                            chaos-passive-10：（1）passive 节点异常，pgaf 切换到异步复制，集群变成 demoted。再让 active 异常，集群状态 down，无法提供服务
                            chaos-passive-10：（2） down 状态时，恢复 active 节点，active 节点变成 wait_active，集群状态为 demoted，可以提供服务
                            chaos-passive-11：短时间内多次 passive 节点异常再恢复
                            chaos-passive-12：passive 重启，active 变成 wait_active，集群降级，passive ready 后，集群恢复健康，各节点角色正确
                            chaos-passive-13：passive 操作强制关机，active 变成 wait_active，集群降级，passive ready 后，集群恢复健康，各节点角色正确
                            chaos-passive-14：passive vm 里操作关机，active 变成 wait_active，集群降级，passive ready 后，集群恢复健康，各节点角色正确
                        数据同步
                            从节点异常 - active 节点正常将文件存在 worker queue 中，不再进行同步
                            从节点恢复后 - 开始从 active 节点同步文件
                            passive 异常，降级状态下，创建虚拟机，创建数据中心，造成 db 数据变化，然后恢复 passive，检查数据同步正确（同步完后，挂掉 active，做一次 failover 来确认）
                            passive 异常，降级状态下，上传系统服务安装包，并创建系统服务，然后恢复 passive，检查数据同步正确。（同步完后，挂掉 active，做一次 failover 来确认）
                        手动 failover
                            通过 cli 手动 failover - 报错
                    仲裁节点异常
                        HA 页面展示
                            页面顶部会展示红色警示信息："仲裁节点异常。当主动节点异常时，将无法进行故障转移"。
                            仲裁节点上的卡片展示「异常」状态，被动节点卡片变红色外框。
                        节点故障
                            chaos-witness-1：（1）witness 节点关机，active 和 passive 节点状态不变，集群变成 unhealthy，服务保持可用，不具备 HA 的能力。
                            chaos-witness-1：（2）witness 节点恢复，集群恢复 ready，提供 HA 的能力。这个过程中不会触发 failover。
                            chaos-witness-2：（1）witness 网络断开，跟 active 和 passive 均不连通，active 和 passive 节点状态不变，集群变成 unhealthy，服务保持可用，不具备 HA 的能力。
                            chaos-witness-2：（2）witness 节点恢复，集群恢复 ready，提供 HA 的能力。
                            chaos-witness-3：（1）witness 节点网络异常，集群 unhealthy，active 节点再网络异常，集群状态 down，服务不可用
                            chaos-witness-3：（2） 恢复 witness 节点，触发 failover，passive 被提升 wait_active，集群恢复服务
                            chaos-witness-3：（3） 恢复旧 active 节点，作为 passive 加入集群，集群状态恢复 ready
                            chaos-witness-4：（1）witness 节点异常，集群 unhealthy，active 节点网络异常，集群状态 down，服务不可用
                            chaos-witness-4：（2） 恢复 active 节点，服务不可用，节点取法就绪
                            chaos-witness-4：（3） 恢复 witness 节点，服务恢复可用，集群状态恢复 ready。会发生一次 failover。
                            chaos-witness-5：（1）witness 节点异常，集群 unhealthy，active 节点再关机，集群状态 down，服务不可用
                            chaos-witness-5：（2） 恢复 active 节点，服务不可用，active 和 passive 节点也无法 ready
                            chaos-witness-5：（3） 恢复 witness 节点，服务恢复可用，集群状态恢复 ready，会发生一次 failover。
                            chaos-witness-6：（1）witness 节点异常，集群 unhealthy，active 节点操作暂停，集群状态 down，服务不可用
                            chaos-witness-6：（2） 恢复 active 节点，服务恢复可用，不会做 failover 切换
                            chaos-witness-6：（3） 恢复 witness 节点，集群状态恢复 ready
                            chaos-witness-7：（1）witness 节点异常，集群 unhealthy，passive 节点网络异常，集群状态 down，服务不可用
                            chaos-witness-7：（2） 恢复 passive 节点，passive 不能就绪，服务无法恢复
                            chaos-witness-7：（3） 恢复witness 节点，集群状态恢复 ready。不会发生 failover
                            chaos-witness-8：（1）witness 节点异常，集群 unhealthy，passive 节点关机，集群状态 down，服务不可用
                            chaos-witness-8：（2） 恢复 passive 节点，passive 无法就绪，集群不可用
                            chaos-witness-8：（3） 恢复witness 节点，集群状态恢复 ready
                            chaos-witness-9：（1）witness 节点异常，集群 unhealthy，passive 节点再异常，集群状态 down，服务不可用
                            chaos-witness-9：（2） 恢复 witness 节点，服务恢复可用，集群降级状态
                            chaos-witness-9：（3） 恢复 passive 节点，服务恢复可用，集群状态恢复 ready
                            chaos-witness-10：witness 强制关机，集群 unhealthy，witness ready 后，集群恢复健康，各节点角色正确
                            chaos-witness-11：witness vm 里关机，集群 unhealthy，witness ready 后，集群恢复健康，各节点角色正确
                            chaos-witness-12：witness 重启，集群 unhealthy，witness ready 后，集群恢复健康，各节点角色正确
                        数据同步
                            witness 异常时，上传的文件存放至 fileserver 中，并通能同步至 passive 节点
                            witness 异常时，触发的日志存放至 fileserver 中，并能同步至 passive 节点
                            witness异常时，自动生成的报表，存放至 fileserver 中，并能 同步至 passive 节点
                        手动 failover
                            通过 cli 手动 failover - 报错
                    被动和仲裁同时异常
                        HA 页面展示
                            页面顶部会展示第一条红色警示信息："被动节点异常，取法切换主被节点。当主动节点异常时，将无法进行故障转移"。
                            页面顶部会展示第二条红色警示信息："仲裁节点异常。当主动节点异常时，将无法进行故障转移"。
                            被动节点上的卡片展示「异常」状态，被动节点卡片变红色外框。
                            仲裁节点上的卡片展示「异常」状态，被动节点卡片变红色外框。
                        节点故障
                            同时 down 掉 passive 和 witness，集群变为 down，服务不可用
                            用户可使用运维命令将存活的 active 节点强制转换为单节点，再重新组建 CloudTower HA 集群，有数据丢失的风险，需要提示用户能保证恢复到到具体时间点的数据。（480 不支持 HA 节点转换单节点）
                            单独恢复 passive 节点，服务无法恢复
                            单恢复 witness 节点，集群 demoted 状态，服务恢复可用
                            恢复 passive 和 witness 节点，数据同步，完成后集群 ready 状态
                        数据同步
                            passive 和 witness 异常，服务不可用，不再文件同步
                            passivie 和 witness 都恢复后，服务恢复正常，同步文件正常
                        手动 failover
                            通过 cli 手动 failover - 报错
                    主动和被动均异常
                        主动和被动同时异常，服务不可用
                        节点恢复
                            单恢复主节点，服务可用，不具备 HA 能力，可以进行基本的业务操作，上传文件能成功。
                            主节点恢复一段时间后，再恢复从节点，从节点会自动从主去同步文件。数据同步好之后，可以恢复 HA 的能力。
                            单恢复从节点，节点变为 wait_active 状态，记录一条主被切换的记录，信息记录正确
                            failover 完成，再恢复原来 active 节点恢复后 - 降级为 passive 节点，恢复 HA 能力，开始从新主节点同步文件。
                        手动 failover
                            通过 cli 手动 failover - 报错
                    主动和仲裁均异常
                        集群 down，不能提供服务
                        节点恢复
                            单恢复主节点，服务不能恢复
                            恢复主节点之后，再恢复 witness 节点，集群 HA 能力恢复
                            单恢复 witness 节点，会触发 failover，原来的 passive 节点变为 wait_active，服务可用
                            恢复 witness 节点之后，再恢复 原来的 active 节点，会作为 passive 节点加入 HA，并从当前 active 节点同步数据。集群最终恢复 ready，恢复 HA 能力
                            用户可使用运维命令将存活的 passive 节点强制转换为单节点，再重新组建 CloudTower HA 集群，有数据丢失的风险，需要提示用户能保证恢复到到具体时间点的数据。（480 不支持 HA 节点转换单节点）
                        手动 failover
                            通过 cli 手动 failover - 报错
                    主、被、仲裁全部异常
                        三节点当前均为关机状态，按 witness > active > passive 顺序依次开机虚拟机，能够恢复主备形态，正常向 passive 同步
                        三节点当前均为关机状态，按 active > witness > passive 顺序依次开机虚拟机，能够恢复主备形态，正常向 passive 同步
                        三节点当前均为关机状态，按 active > passive > witness 顺序依次开机虚拟机，能够恢复主备形态，正常向 passive 同步
                        节点恢复
                            如果三个节点均异常，针对节点的恢复顺序，目前没有建议，需要看客户的现场，具体分析
                    网络故障
                        chaos-nt-1：（1）模拟 active 隔离，active 转为 Down，关闭 VIP 防止多主冲突，集群变为 recovering 状态，触发 failover，故障转移期间服务不可用。
                        chaos-nt-1：（2）集群 recovering 状态， failover 完成后，passive 节点提升为 wait_active 状态，集群状态为 demoted，服务恢复可用。
                        chaos-nt-1：（3）恢复旧的主动节点的网络，该节点先分配 catchingUp 角色从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                        chaos-nt-2：（1）模拟 passive 隔离，active 变成 wait_active，集群变为 demoted，服务可用
                        chaos-nt-2：（2）恢复 passive 网络，该节点先分配 catchingUp 角色从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                        chaos-nt-3：（1）模拟 witeness 隔离，active 和 passive 状态不变，集群变为 demoted，服务可用
                        chaos-nt-3：（2）恢复 witness 网络，集群恢复成 ready
                        chaos-nt-4：（1）模拟 active <-> witness 网络故障，active 转为 Down，关闭 VIP 防止多主冲突，集群变为 recovering 状态，触发 failover，故障转移期间服务不可用。
                        chaos-nt-4：（2）集群 recovering 状态， failover 完成后，passive 节点提升为 wait_active 状态，集群状态为 demoted，服务恢复可用。
                        chaos-nt-4：（3）恢复网络，旧主节点先分配 catchingUp 角色从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                        chaos-nt-5：（1）模拟 active <-> passive 网络故障，集群进入降级状态，active 节点状态变为 wait active，数据无法同步，passive 变为 catching up
                        chaos-nt-5：（2）恢复网络， passive 追赶数据，数据一致后，集群恢复 ready，wait_active 恢复 为 active，passive 恢复 passive
                        chaos-nt-6：（1）模拟 witness <-> passive 网络故障，集群进入降级状态，active 节点状态变为 wait active，passive 变为 catching up
                        chaos-nt-6：（2）恢复网络，集群恢复 ready，wait_active 恢复 为 active，passive 恢复 passive
                        chaos-nt-7：（1）模拟 active -> witness 故障，集群变为 recovering 状态，触发 failover，故障转移期间服务不可用。
                        chaos-nt-7：（2）集群 recovering 状态， failover 完成后，passive 节点提升为 wait_active 状态，集群状态为 demoted，服务恢复可用。
                        chaos-nt-7：（3）恢复网络，旧主节点先分配 catchingUp 角色从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                        chaos-nt-8：（1）模拟 active -> passive 网络故障，集群进入降级状态，active 节点状态变为 wait active，数据无法同步，passive 变为 catching up
                        chaos-nt-8：（2）恢复网络， passive 追赶数据，数据一致后，集群恢复 ready，wait_active 恢复 为 active，passive 恢复 passive
                        chaos-nt-9：（1）模拟 passive -> witness 网络故障，集群进入降级状态，active 节点状态变为 wait active
                        chaos-nt-9：（2）恢复网络， 集群恢复 ready，wait_active 恢复 为 active，passive 恢复 passive
                        chaos-nt-10：（1）模拟 passive -> active 网络故障，集群进入降级状态，active 节点状态变为 wait active
                        chaos-nt-10：（2）恢复网络， 集群恢复 ready，wait_active 恢复 为 active，passive 恢复 passive
                        chaos-nt-11：（1）模拟 witness -> passive 网络故障，集群进入降级状态，active 节点状态变为 wait active，passive 的状态会被设置为 catchingUp，无法再提供 failover 能力
                        chaos-nt-11：（2）恢复网络， 集群恢复 ready，wait_active 恢复 为 active，passive 恢复 passive
                        chaos-nt-12：（1）模拟 witness -> active 故障，witness 将 active 转为 down，触发 failover，晋升 passive，集群变为 recovering，故障转移期间服务不可用。
                        chaos-nt-12：（2）集群 recovering 状态， failover 完成后，passive 节点提升为 wait_active 状态，集群状态为 demoted，服务恢复可用。
                        chaos-nt-12：（3）恢复网络，旧主节点先分配 catchingUp 角色从当前 wait_active 节点同步数据，集群变为 Catching Up。数据同步完成后，集群变成 ready，wait_active 节点变成 active，Catching Up 节点变为 passive。
                        chaos-net-13：网络震荡，增加 active、passive、witness 之间的网络延迟，观察 HA 等相关服务状态及使用情况
                        chaos-net-14：active 网络丢包严重，会触发 failover
                        chaos-net-15：passive 网络丢包严重，passive 会 down，HA 降级。恢复丢包后，HA 恢复 ready。
                        chaos-net-16：witness 网络丢包严重，witness 可能会 down，还会触发 failover，如果一直维持丢包，有可能触发多次 failover。丢包恢复后，HA 恢复正常。
                    切换记录
                        无切换记录 - 页面为空白状态，展示 “无记录”
                        触发切换的时间 - xxxx-xx-xx xx:xx 触发，时间正确
                        触发切换的类型 - 手动/自动，类型记录正确
                        触发切换的节点记录 - 尝试将主动节点从 xxxx 切换为 xxxx，节点名称正确
                        自动切换展示切换原因，手动的不展示。原因只能展示粗略展示 xxx 节点异常。
                        切换记录条数 - 每页最多展示 20 条
                        切换记录条数 - 翻页查看切换记录，数据正确展示无重复
                        切换记录条数 - 页码显示与数据条数对应
                        切换记录排序 - 按照触发时间倒序排序
                        无高可用权限的用户 - 可以正常查看切换记录列表
                        有高可用权限的用户 - 可以正常查看切换记录列表
                        英文翻译 - 无切换记录，页面信息正确翻译为英文
                        英文翻译 - 有切换记录无翻页，页面信息正确翻译为英文
                        英文翻译 - 有切换记录且翻页，页面信息正确翻译为英文
                    监控告警
                        节点状态告警
                            新增告警规则：CloudTower 高可用被动节点异常。默认级别：严重告警
                            被动节点异常 5min，触发告警，检查告警信息。
                            被动节点恢复正常后，告警清除。
                            修改被动节点异常的告警规则配置后，能及时生效。
                            新增告警规则：CloudTower 高可用仲裁节点异常。默认级别：严重告警
                            仲裁节点异常 5min，触发告警，检查告警信息。
                            仲裁节点恢复正常后，告警清除。
                            修改仲裁节点异常的告警规则配置后，能及时生效。
                            新增告警规则：CloudTower 高可用{{节点类型}}节点与{{节点类型}}节点时间偏移量过大。默认阈值：60s 严重, 30s 注意，10s 信息。持续三分钟产生告警
                            主动节点和被动节点的时间偏移量过大，持续三分钟触发告警，检查告警信息。
                            主动节点和被动节点的时间偏移恢复后，告警清除。
                            主动节点和仲裁节点的时间偏移量过大，持续三分钟触发告警，检查告警信息。
                            主动节点和仲裁节点的时间偏移恢复后，告警清除。
                            被动节点和仲裁节点的时间偏移量过大，不产生告警，开发确认过
                            报警通路选一种回归一下
                            时间偏移量过大，通过运维手册恢复，保障 HA 集群正常运行
                        故障转移告警
                            新增告警规则：CloudTower 高可用故障转移完成。默认等级：信息
                            故障转移完成后，产生高可用故障转移完成的告警，检查告警信息。
                            故障转移失败，人工处理完成恢复后，是否产生该条告警？
                            修改故障转移完成的告警配置，能生效。
                            报警通路选一种回归一下
                        网络连接告警
                            新增告警规则：CloudTower 高可用{{vm_ip}}节点到{{vm_ip}}节点的平均往返延迟异常。默认等级和阈值：待定。
                            触发  active -> passive 间延迟高，超过 1min 产生对应告警，检查告警信息。
                            取消  active -> passive 网络延迟，告警清除。
                            触发 active->witness 间延迟高，超过 1min 产生对应告警，检查告警信息。
                            取消 active->witness 网络延迟，告警清除。
                            触发 passive->witness 间延迟高，超过 1min 产生对应告警，检查告警信息。
                            取消 passive->witness 网络延迟，告警清除。
                            修改节点往返延迟告警规则的阈值和等级配置，能生效。
                            新增告警规则：CloudTower 高可用{{vm_ip}}节点到{{vm_ip}}节点的网络连接异常。。默认等级和阈值：待定。
                            触发 active -> passive 网络不联通，超过 1min 产生对应告警，检查告警信息。
                            恢复 active -> passive 网络联通，告警清除。
                            触发  active -> witness 网络不联通，超过 1min 产生对应告警，检查告警信息。
                            恢复 active -> witness网络联通，告警清除。
                            触发 passive->witness 网络不联通，超过 1min 产生对应告警，检查告警信息。
                            恢复 passive->witness 网络联通，告警清除。
                            修改节点网络连接异常告警规则的阈值和等级配置，能生效。
                            报警通路选一种回归一下
                        文件丢失告警
                            新增告警规则：存在 %丢失文件数量% 个文件丢失。默认等级：注意
                            模拟文件丢失，触发告警
                            补偿文件，告警清除
                            检查告警文案内容。
                            选一个通路回归一下告警通知。
                HA - 数据同步
                    HA 页面展示
                        页面顶部会展示提示信息："被动节点正在同步主动节点的数据……请等待同步完成。同步期间，无法切换主被节点"。
                        主被节点之间的连线显示同步中的样式，icon 有转动效果。
                        被动节点展示「同步中」状态。
                    数据同步告警
                        新增规则：CloudTower 高可用主动节点与被动节点数据同步差异过大。默认阈值：差异 >5 s 为注意，>30 s 为严重警告
                        英文界面下 - 报警规则正常翻译为了英文
                        触发数据同步差异大的报警，检查报警信息
                        数据同步一致，告警信息清除
                        禁用 主被数据同步差异过大 的报警规则 - 达到触发条件，不再触发报警
                        修改 主被数据同步差异过大 的报警规则等级 - 达到触发条件，触发新等级报警
                        新增CloudTower 高可用数据同步中断的告警规则，默认为严重告警
                        中断数据同步 1min 产生告警，检查文案信息正确
                        恢复数据同步后，告警清除
                        修改数据同步的告警配置能生效
                        禁用数据同步告警后，触发数据同步中断不再产生告警
                        报警通路选一种回归一下
                    手动 failover
                        通过 cli 手动 failover - 报错
                组件故障
                    stop active 节点 HA controller，systemctl 会自动拉起，这期间不触发 failover
                    stop active 节点 pgautofailover，systemctl 会自动拉起，会触发 failover
                    删除 active 节点 kine pod，预期不触发 failover
                    fileserver 异常的时候，不触发 failover，但是服务会变得不可用。fileserver 恢复后，服务恢复可用。
                    主库 hang 住，触发 failover
                    复制延迟，不触发 failover
                    pgaf keeper 进程异常，触发 failover
                    pgaf monitor 进程异常，会被主进程拉起，不会触发 failover
                系统集成
                    HA 集群上，做关联产品回归。
                    物理集群
                        ifdown eth0 断掉虚拟机的管理网络，Tower HA 网络也是用的管理网，Tower 异常，ifup eth0 恢复网络后，Tower 可以恢复正常
                        集群存储网络异常，vm 无法正常工作，也影响 tower HA
                        HA 节点在同一个物理集群，物理集群 license 过期，IO 会受影响，不能保证 HA 集群正常工作
                        HA 节点不在同一个物理集群，其中一个物理集群 license 过期，IO 会受影响，受IO 影响的 HA 节点可能异常
                        HA 三个节点都可以被一键提升副本数
                        HA 节点都在同一集群内，一键提升副本数后，HA 集群正常工作
                        HA 节点在不同集群，单个节点被一键提升副本数，不影响 HA 集群工作
                        HA 节点在不同集群，单个节点被一键提升副本数，HA 切换不会有问题
                        HA 节点在不同集群，单个节点被一键提升副本数，HA 升级不会有问题
                        HA 节点部署在双活集群上，active 所在节点重启，触发 failover，节点恢复后，tower vm 恢复，HA 恢复 ready
                        HA 节点部署在双活集群上，passive 所在节点重启，集群 demoted，节点恢复后，tower vm 恢复，HA 恢复 ready
                        HA 节点部署在双活集群上，witness 所在节点重启，集群 unhealthy，节点恢复后，tower vm 恢复，HA 恢复 ready
                        HA 节点部署在双活集群上，active 所在节点故障，触发虚拟机重建，HA 触发 failover，tower vm 恢复，HA 恢复 ready
                        HA 节点部署在双活集群上，passive 所在节点故障，触发虚拟机重建，集群 demoted，tower vm 恢复，HA 恢复 ready
                        HA 节点部署在双活集群上，witness 所在节点故障，触发虚拟机重建，集群 unhealthy，tower vm 恢复，HA 恢复 ready
                        SRE 相关的运维操作，主机，集群升级，维护模式，jingyue 他们有测试
                        active 所在物理集群的 meta leader 节点重启，预期不触发 Tower HA failover
                    虚拟机相关
                        虚拟机热迁移过程中，模拟故障，触发 HA 切换，预期迁移任务失败
                        虚拟机冷迁移过程中，模拟故障，触发 HA 切换，预期迁移任务失败
                        ISO 分发过程中，模拟故障，触发 HA 切换，预期任务失败
                        模板分发过程中，模拟故障，触发 HA 切换，预期任务失败
                        创建虚拟机，模拟故障，触发 HA 切换，预期任务失败
                        导入虚拟机时，模拟故障，触发 HA 切换，预期任务失败
                        导出虚拟机时，模拟故障，触发 HA 切换，预期任务失败
                        active 节点虚拟机 HA 重建，会触发 failover，虚拟机重建好了之后，HA 恢复 ready
                        passive 节点虚拟机 HA 重建，会触发降级，虚拟机重建好了之后，HA 恢复 ready
                        witness 节点虚拟机 HA 重建，会触发 unhealthy，虚拟机重建好了之后，HA 恢复 ready
                    系统服务
                        部署 SFS 的过程中，模拟故障，触发 HA 切换 - 部署任务失败，已部署的 SFS 能卸载掉
                        卸载 SKS 的 tower，部署成 HA，模拟故障，触发 HA 切换，HA 集群正常
                        部署 ER 的过程中，模拟故障，触发 HA 切换 - 部署任务失败
                        部署 备份/复制 的过程中，模拟故障，触发 HA 切换 - 部署任务失败
                        部署 Agent Mesh 的过程中，模拟故障，触发 HA 切换，部署任务失败，capp 自己有重试，系统服务实际可以部署出来。
                        部署 可观测 的过程中，模拟故障，触发 HA 切换 - 部署任务失败。已部署的服务可以卸载掉。
                        HA 切换完成 - 检查已部署的系统服务，服务状态为正常
                    commander
                        使用 VIP 关联可以成功，数据能查询到
                        关联中，如果被关联的 CloudTower 正在进行故障切换，预期关联失败。
                        commander 先关联单节点 tower，然后 tower 启用了 HA，启用成功后，commander  关联状态不受影响。
                        HA 集群发生 failover 时，commander 上显示 CloudTower 服务异常；HA 切换结束后，commander 上恢复正常。
                    通用业务
                        手动检查一些基本业务，比如报表下载
                        cloudtower 许可过期，HA 能正常使用
                性能指标
                    关注三节点的 cpu、mem、磁盘 IO 数据指标
                    切换时，观察 failover 耗时
                    HA 环境关联 xxx 多个集群，包括 xxxx 个虚拟机，进行各种常规故障 failover，检查 HA 服务、功能及是否影响业务
                事件和任务
                    每一次自动触发故障转移，会产生系统事件：“触发 CloudTower 高可用故障切换，尝试将 CloudTower 主节点从 {{原主节点 HA 网络 IP}} 切换至 {{新主节点 HA 网络 IP}}。”
                    每一次手动触发故障转移，会产生系统事件：“触发 CloudTower 高可用故障切换，尝试将 CloudTower 主节点从 {{原主节点 HA 网络 IP}} 切换至 {{新主节点 HA 网络 IP}}。”
                    「状态 - 成功/失败」代表 failover 是否被成功触发；不代表 failover 是否完成。
                    事件仅记录触发时间，不记录完成时间和完成状态。
                节点时间不一致
                    active 和 passive 节点时间不一致 - failover 完成，上传文件可能会出现时间错乱
                    active 和 passive 节点时间不一致 - failover 完成，触发的事件可能会出现时间错乱
                    active 和 passive 节点时间不一致 - failover 完成，触发的任务可能会出现时间错乱
                    active 和 passive 节点时间不一致 - failover 完成，系统服务触发的报警，可能不受影响
                    active 和 passive 节点时间不一致 - 不会出现 pg 数据丢失的情况
                    active 和 passive 节点时间不一致 - 文件同步正常
                    节点之间的时间误差小于 10min，ntp 能自动同步时间
                    节点之间的时间误差大于 10min，ntp 不能自动同步时间
                其他场景
                    部署前修改 tower vm 的hostname，然后再部署 HA，部署成功后做 failover 切换，功能正常
                    部署前修改 passive vm 的hostname，然后再部署 HA，部署成功后做 failover 切换，功能正常
                    部署前修改 witness vm 的hostname，然后再部署 HA，部署成功后做 failover 切换，功能正常
                    active 使用静态 IP 部署 tower，再部署 HA，部署成功后做 failover 切换，功能正常
                    witness 使用静态 IP 部署 tower，再部署 HA，部署成功后做 failover 切换，功能正常
                    active 和 witness 使用静态 IP 部署 tower，再部署 HA，部署成功后做 failover 切换，功能正常
                    active 和 witness 使用动态 IP 部署 tower，再部署 HA，部署成功后做 failover 切换，功能正常
            文件同步
                capp
                    /v2/api/upload-cloudtower-application-package - 将安装包上传至 CloudTower
                    capp package manager - 解压上传的安装包并将 容器镜像包、运行时文件 存储到本地
                    capp package manager - 读取 package.yaml 在 CloudTowerApplicationPackage 表中创建记录
                    /files api - 将本地 容器镜像包、运行时文件 上传至 fileserver 指定 path
                    capp package manager - 将 fileserver 中的 path 回填至 CloudTowerApplicationPackage 表
                    安装包上传完成 - 使用该安装包可以正常部署系统服务
                    /v2/api/delete-cloudtower-application-package - 将安装包从 CloudTower 删除
                    /files/{fileId} api - 通过 path 删除 fileserver 中的文件
                    capp package manager - 删除 CloudTowerApplicationPackage 表的记录
                    安装包删除完成 - 部署系统服务时没有该安装包的选项
                    capp manager - 初次启动时生成的 ssh key 存在新增的 CloudTowerApplicationGlobalConfig 表中
                    capp package 解压出的 images.tar 和 assets 文件 - 生成 sha256 与 fileserver 数据库中记录的 sha256 进行对比预期一致
                    OBS
                        上传安装包 - 上传成功，CloudTowerApplicationPackage 表中有记录，fileserver 中有文件
                        Tower HA 模式 - active 和 passive 节点均正常，active 上传安装包完成，并同步至 passive，可启用 failover
                        Tower HA 模式 - passive 节点在上传安装包时异常，上传成功，但无法同步至 passive，恢复后继续同步
                        Tower HA 模式 - active 节点在同步安装包时异常，同步失败，可启用 failover，但可能导致安装包丢失
                        部署服务 - 使用 active 节点上的安装包进行部署，可部署成功
                        部署服务 - failover 后，使用新 active 节点上的安装包进行部署，可部署成功
                    Agent Mesh
                        上传安装包 - 上传成功，CloudTowerApplicationPackage 表中有记录，fileserver 中有文件
                        上传安装包 - 上传失败，CloudTowerApplicationPackage 表中无记录，fileserver 中无文件
                        Tower HA 模式 - active 和 passive 节点均正常，active 上传安装包完成，并同步至 passive，可启用 failover
                        Tower HA 模式 - active 节点在上传安装包时异常，上传失败，没有可同步文件至 passive，可启用 failover
                        Tower HA 模式 - active 节点在同步安装包时异常，同步失败，可启用 failover，但可能导致安装包丢失
                        Tower HA 模式 - passive 节点在上传安装包时异常，上传成功，但无法同步至 passive，恢复后继续同步
                        Tower HA 模式 - passive 节点在同步安装包时异常，同步失败，恢复后继续同步
                        部署服务 - 使用 active 节点上的安装包进行部署，可部署成功
                        部署服务 - failover 后，使用新 active 节点上的安装包进行部署，可部署成功
                    SFS
                        上传安装包 - 上传成功，CloudTowerApplicationPackage 表中有记录，fileserver 中有文件
                        Tower HA 模式 - active 和 passive 节点均正常，active 上传安装包完成，并同步至 passive，可启用 failover
                        Tower HA 模式 - passive 节点在上传安装包时异常，上传成功，但无法同步至 passive，恢复后继续同步
                        Tower HA 模式 - active 节点在同步安装包时异常，同步失败，可启用 failover，但可能导致安装包丢失
                        部署服务 - 使用 active 节点上的安装包进行部署，可部署成功
                        部署服务 - failover 后，使用新 active 节点上的安装包进行部署，可部署成功
                    Backup
                        上传安装包 - 上传成功，CloudTowerApplicationPackage 表中有记录，fileserver 中有文件
                        Tower HA 模式 - active 和 passive 节点均正常，active 上传安装包完成，并同步至 passive，可启用 failover
                        Tower HA 模式 - passive 节点在上传安装包时异常，上传成功，但无法同步至 passive，恢复后继续同步
                        Tower HA 模式 - active 节点在同步安装包时异常，同步失败，可启用 failover，但可能导致安装包丢失
                        部署服务 - 使用 active 节点上的安装包进行部署，可部署成功
                        部署服务 - failover 后，使用新 active 节点上的安装包进行部署，可部署成功
                    Replication
                        上传安装包 - 上传成功，CloudTowerApplicationPackage 表中有记录，fileserver 中有文件
                        Tower HA 模式 - active 和 passive 节点均正常，active 上传安装包完成，并同步至 passive，可启用 failover
                        Tower HA 模式 - passive 节点在上传安装包时异常，上传成功，但无法同步至 passive，恢复后继续同步
                        Tower HA 模式 - active 节点在同步安装包时异常，同步失败，可启用 failover，但可能导致安装包丢失
                        部署服务 - 使用 active 节点上的安装包进行部署，可部署成功
                        部署服务 - failover 后，使用新 active 节点上的安装包进行部署，可部署成功
                    容器镜像仓库
                        上传 user-registry 安装包 - 上传成功，CloudTowerApplicationPackage 表中有记录，fileserver 中有文件
                        Tower HA 模式 - active 和 passive 节点均正常，active 上传安装包完成，并同步至 passive，可启用 failover
                        Tower HA 模式 - passive 节点在上传安装包时异常，上传成功，但无法同步至 passive，恢复后继续同步
                        Tower HA 模式 - active 节点在同步安装包时异常，同步失败，可启用 failover，但可能导致安装包丢失
                        部署服务 - 使用 active 节点上的安装包进行部署，可部署成功
                        部署服务 - failover 后，使用新 active 节点上的安装包进行部署，可部署成功
                日志
                    集群角色转换触发的日志 - 需要上传至 fileserver 并同步至 passive 节点
                    集群添加主机触发的日志 - 不需要测试，走的 tuna api，非 fileserver
                    集群移除主机触发的日志 - 需要上传至 fileserver 并同步至 passive 节点
                报表
                    保留的自动生成的资产列表报表 - 需要上传至 fileserver 并同步至 passive 节点。切换主从后，下载报表能成功。
                    保留的自动生成的资源优化报表 - 需要上传至 fileserver 并同步至 passive 节点。切换主从后，下载报表能成功
                    Tower HA 模式 - active 节点在同步报表时异常，同步失败，可启用 failover，但可能导致报表丢失
                    报表下载 - failover 后，在新 active 节点上下载报表成功
                    同步失败的报表 - 在 UI 上仍然展示，但是不能下载
                其他
                    部署或升级后的 ER island UI 代码文件 - 需要上传至 fileserver 并同步至 passive 节点
                    部署时的 容器服务 island UI 代码文件 - 需要上传至 fileserver 并同步至 passive 节点
                    部署或升级后的 SFS island UI 代码文件 - 需要上传至 fileserver 并同步至 passive 节点
                    部署或升级后的 巡检中心 island UI 代码文件 - 需要上传至 fileserver 并同步至 passive 节点
                    上传的 ER 安装包，解压后的临时安装文件 - 无需迁移，不需要检查
                    上传的 ER 升级包，解压后的临时安装文件 - 无需迁移，不需要检查
                    上传的容器镜像仓库安装包，解压后的临时安装文件 - 需要上传至 fileserver 并同步至 passive 节点
                    上传的 ER 安装包 - 需要上传至 fileserver 并同步至 passive 节点
                    上传的 Host Plugin Package 镜像包 - 需要上传至 fileserver 并同步至 passive 节点
                    可观测关联集群时生成的配置文件 - 存在 pg 中并通过 pgaf 同步复制到 passive pg，检查下 failover 后在新 active 节点上，集群仍正常关联
                    上传至升级中心的集群升级文件 - 需要上传至 fileserver 并同步至 passive 节点
                    vgpu 文件 - 需要上传至 fileserver 并同步至 passive 节点
                    上传至升级中心的集群补丁文件 - 需要上传至 fileserver 并同步至 passive 节点
                HA 启用前存量文件
                    capp
                        启用 HA 之前已上传的 SFS 安装包 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        启用 HA 之前已上传的容器镜像仓库安装包 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        启用 HA 之前已上传的 备份/复制 安装包 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        启用 HA 之前已上传的 Agent Mesh 安装包 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        启用 HA 之前已上传的 可观测 安装包 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        文件同步过程中 active 节点异常，触发 failover - 可能会导致安装包同步失败
                        安装包同步失败，提供文件补偿方式 - 在新 active 节点重新上传相同安装包，保证系统服务可用
                    日志
                        启用 HA 之前集群角色转换触发的日志 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        启用 HA 之前集群添加主机触发的日志 - 不需要测试，走的 tuna api，非 fileserver
                        启用 HA 之前集群移除主机触发的日志 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                    报表
                        启用 HA 之前保留的自动生成的资产列表报表 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        启用 HA 之前保留的自动生成的资源优化报表 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        Tower HA 模式 - active 节点在同步报表时异常，同步失败，可启用 failover，但可能导致报表丢失
                        报表下载 - failover 后，在新 active 节点上下载报表成功
                        同步失败的报表 - 在 UI 上仍然展示，但是不能下载
                    其他
                        部署或升级后的 ER island UI 代码文件 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        部署时的 容器服务 island UI 代码文件 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        部署或升级后的 SFS island UI 代码文件 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        部署或升级后的 巡检中心 island UI 代码文件 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        上传的 ER 安装包，解压后的临时安装文件 - 无需迁移，不需要检查
                        上传的 ER 升级包，解压后的临时安装文件 - 无需迁移，不需要检查
                        上传的容器镜像仓库安装包，解压后的临时安装文件 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        上传的 ER 安装包 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        上传的 Host Plugin Package 镜像包 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        可观测关联集群时生成的配置文件 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        上传至升级中心的集群升级文件 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                        vgpu 文件 - 需要上传至 fileserver 并同步至 passive 节点
                        上传至升级中心的集群补丁文件 - 迁移至 fileserver 并在 HA 集群 ready 后自动同步至 passive 节点
                文件丢失告警
                    新增报警 “存在 %丢失文件数量% 个文件丢失。” - 默认等级为注意
                    Tower 已上传的文件安装包，启用 HA 后发生 failover - 文件丢失，触发报警
                    Tower 已上传的容器镜像仓库安装包，启用 HA 后发生 failover - 文件丢失，触发报警
                    Tower 已上传的 ER 安装包，启用 HA 后发生 failover - 文件丢失，触发报警
                    Tower 已上传的 备份/复制 安装包，启用 HA 后发生 failover - 文件丢失，触发报警
                    Tower 已上传的 代理 安装包，启用 HA 后发生 failover - 文件丢失，触发报警
                    Tower 已上传的可观测安装包，Tower 升级后并发生 failover - 文件丢失，触发报警
                    报警触发信息检查 - 触发原因/影响/解决方法、报警源/等级/对象/规则/触发时间
                    删除并上传对应版本的安装包 - 报警解决
                    报警解决信息检查 - 触发原因/影响/解决方法、报警源/等级/对象/规则/触发时间/解决时间
                    禁用 文件丢失 的报警规则 - 达到触发条件，不再触发报警
                    修改 文件丢失 的报警规则等级 - 达到触发条件，触发新等级报警
                    报警通知配置 - 选一条告警通路，检查一下通知信息
            HA 运维操作
                节点扩容
                    active 扩容 cpu\mem
                    active 扩容磁盘
                    passive 扩容 cpu\mem
                    passive 扩容磁盘
                    witness 扩容 cpu\mem
                    witness 扩容磁盘
                更新 Tower 许可
                    Tower license 过期 - HA 集群正常工作，可以触发 failover
                    企业版试用许可过期 - 更新至企业版订阅许可成功，HA 集群正常工作。更新许可后，触发一次 failover，检查功能正常。
                    企业版试用许可过期 - 更新至企业版永久许可成功，HA 集群正常工作。更新许可后，触发一次 failover，检查功能正常。
                    企业版订阅许可过期 - 更新至企业版永久许可成功，HA 集群正常工作。更新许可后，触发一次 failover，检查功能正常。
                备份和重建（跨架构&发行版迁移）
                    HA 形态下，暂不支持 HA 的备份和重建迁移
                    HA 形态下，passive 异常，通过重建恢复 passive 节点，HA 集群恢复正常，可正常 failover，重建后的 passive 提升为主节点
                    HA 形态下，witness 异常，通过重建恢复 witness 节点，HA 集群恢复正常，可正常 failover，passive 提升为主节点
                跨集群迁移
                    active 节点
                        active 迁移过程中，active 可达，HA 不受影响，tower 正常可用
                        active 分段迁移，active 关机重建时，会触发 failover
                        active 迁移完成, HA 可用，tower 可用
                        active 虚拟机热迁移，不影响 tower，不触发 HA
                    passive 节点
                        passive 节点迁移过程中，passive 可达，系统正常可用
                        passive 节点迁移过程中，passive 可达，正常同步文件停止
                        passive 节点迁移过程中 ，passive 可达， active 异常，自动 failover
                        passive 节点分段迁移，源虚拟机关机操作之后，在目标集群重建时，passive 不可用，这时候会影响 HA 相关功能
                        passive 迁移完成后，HA 集群恢复正常，数据同步和 failover 相关功能正常
                    witness 节点
                        witness 节点迁移过程中，witness 可达，系统正常可用
                        witness 节点迁移过程中，witness 可达，active 异常，可以自动 failover
                        witness 节点分段迁移，源虚拟机关机，在目标集群重建时，witeness 会异常，这时 HA 相关功能不可用
                        witness 节点迁移完成，active 异常，可自动 failover
                NTP 测试
                    外部 NTP server 的配置和修改，配置好 NTP server 之后，tower 跟随 NTP server 时间
                    配置外部 NTP 服务器后，做 failover，NTP 服务器配置有效，时间同步正确
                    HA 运行过程中，各个节点之间时间差异小于 10 min，能自动同步时间
                    HA 运行过程中，各个节点之间时间差异大于 10 min，手动同步时间
                    NTP server 与 cloudtower 时间小于 10min，自动同步
                    NTP server 与 cloudtower 时间大于 10min，手动同步
                    ntpm server - help
                    ntpm server - sync
                    ntpm server - show
                    ntpm server - health
                    ntpm source - help
                    ntpm source - show
                集成场景
                    上传系统服务安装包，触发 failover 让上传任务失败；failover 完成后再出发 cloudTower 升级
                    上传系统服务安装包，触发 failover 让上传任务失败；failover 完成后，再重新上传同一个安装包，然后部署系统服务
                    挂掉 passive 节点，上传系统服务安装包，然后再恢复 passive 节点，数据同步完后，再升级 Tower
                    挂掉 passive 节点，上传系统服务安装包，然后再恢复 passive 节点，数据同步完后，再 failover，再部署该系统服务
            480 不支持
                两节点部署
                    物理环境
                        Active(SMTX OS ELF) + Passive(SMTX OS ELF)
                        Active(SMTX ELF) + Passive(SMTX ELF)
                        Active(SMTX OS ELF) + Passive(SMTX ELF)
                        Active(SMTX OS 双活) + Passive(SMTX OS)
                        Active(SMTX OS ELF) + Passive(SMTX ZBS)
                        Active(SMTX ZBS) + Passive(SMTX ELF)
                        Active(ACOS ELF) + Passive(ACOS ELF)
                        同一 SMTX OS ELF 集群：Active + Passive
                        同一 SMTX ELF 集群：Active + Passive
                        同一数据中心，不同集群：Active ，Passive
                        跨数据中心：Active ，Passive
                    网络环境
                        HA 网络与管理网络处于同一网段，单管理网络，单 HA 网络
                        HA 网络和管理网络处于不同网段，单管理网络，单 HA 网络
                        HA 网络和管理网络处于不同网段，HA 节点也处于不同网段，单管理网络，多 HA 网络
                    节点规格
                        active & passive：8C 19G 400G
                    HA 启用
                        预检查
                            active，passive，witness 三节点中任意节点 的 hostname 相同，不能部署，返回对应错误信息
                            tower 处于升级状态，不能部署，返回错误
                            passive 节点配置了网卡，不能部署，返回错误
                            passive 节点和当前 tower 处于同一主机，不能部署，返回错误哦
                        网络配置
                            主动节点 HA 网络：vlanId 不存在，部署失败，返回错误
                            主动节点 HA 网络：IP 地址冲突，部署失败，返回错误
                            主动节点 HA 网络：配置错误的网关，部署失败，返回错误
                            主动节点 HA 网络：子网掩码与网关不匹配，部署失败，返回错误
                            被动节点 HA 网络：vlanId 不存在，部署失败，返回错误
                            被动节点 HA 网络：IP 地址冲突，部署失败，返回错误
                            被动节点 HA 网络：配置错误的网关，部署失败，返回错误
                            被动节点 HA 网络：子网掩码与网关不匹配，部署失败，返回错误
                        部署前检查
                            active 和 witness HA 网络不联通，不能部署，返回对应错误信息
                            passive 节点 HA 网络延迟超过 10ms，不能部署
                            witness 节点 HA 网络延迟超过 10ms，不能部署
                            active 节点不满足 spec 要求，不能部署，返回对应错误信息
                            passive 节点不满足 spec 要求，不能部署，返回对应错误信息
                            witness 节点不满足 spec 要求，不能部署，返回对应错误信息
                            active、passive、witness 任一架构不同，不能部署
                            这个版本暂时不检查磁盘空间，UI 部署时，界面上有文字提示期望的 vm spec
                        部署 witness 节点
                            sh ./preinstall.sh，物料检查，物料缺失，部署失败
                            执行 deploy monitor 失败（./binary/installer ha deploy-monitor --ha-iface eth0）
                        CloudTower 单转主
                            管理网络，网卡配置
                            拉起跟 HA 相关的服务时出错,部署任务失败
                        加入 passive 节点
                            配置管理网卡
                            物料缺失，部署失败
                            被动节点加入 HA 网络失败，部署失败
                        状态检查
                            集群状态检查
                            节点状态检查
                        部署完清理
                            主动节点临时文件清理
                            被动节点临时文件清理
                            仲裁节点临时文件清理
                        部署过程故障
                            部署时 witness 网络不可访问
                            部署时 witness 节点掉电
                            部署时 passive 节点掉电
                            部署时 passive 节点网络不可访问
                            部署时，触发 active 节点集群内热迁移
                            部署时，触发 active 节点跨集群热迁移
                            部署时，触发 passive 节点集群内热迁移
                            部署时，触发 passive 节点跨集群热迁移
                            部署时，触发 Tower 升级操作
                            部署时主动节点 launcherd 异常重启
                        部署完检查
                            部署成功
                                HA 页面展示
                                    HA 页面展示基本 HA 信息，各个节点的状态、网络、节点信息等
                                    如果没有关联可观测，需要展示将 CloudTower 关联到可观测的提示信息
                                    如果没有关联可观测，用户有可观测的管理权限，需要展示「关联可观测服务」，点击打开系统配置的可观测页面
                                    如果没有关联可观测，用户没有可观测的管理权限，不展示「关联可观测服务」，只展示关联可观测的提示信息
                                主节点检查
                                    HA controller 运行
                                    k8s control plane pod 运行
                                    launcherd 运行检查
                                    postgres 运行检查
                                    pgaf 运行检查
                                    containerd  运行检查
                                    file server 运行检查
                                    tower server 运行
                                    业务 pod 全部运行
                                    embed-monitor 组件 grafana 运行
                                    embed-monitor 组件 vm-single 运行
                                    embed-monitor 组件 vm-agent 运行
                                    embed-monitor 组件 vector 运行
                                    ntpm 运行
                                    node-exporter 运行
                                    ingress-nginx-controller 运行
                                    everoute-agent 运行
                                    kube-proxy 运行
                                    node-local-dns 运行
                                    vip 网卡运行正常，检查网卡设置 ONBOOT 为 no
                                    HA 网卡运行正常，检查网卡设置 ONBOOT 为 yes
                                    k8s 证书检查
                                从节点检查
                                    HA controller 运行
                                    k8s control plane pod 运行
                                    launcherd 被 disable
                                    postgres 运行检查
                                    pgaf 运行检查
                                    containerd  运行检查
                                    file server 被 disable
                                    tower server 运行
                                    业务 pod 都不运行
                                    embed-monitor 组件 grafana 运行
                                    embed-monitor 组件 vm-single 运行
                                    embed-monitor 组件 vm-agent 运行
                                    embed-monitor 组件 vector 运行
                                    ntpm 运行
                                    node-exporter 运行
                                    ingress-nginx-controller 运行
                                    everoute-agent 运行
                                    kube-proxy 运行
                                    node-local-dns 运行
                                    vip 网卡运行正常，检查网卡设置 ONBOOT 为 no
                                    HA 网卡运行正常，检查网卡设置 ONBOOT 为 yes
                                    k8s 证书检查
                                仲裁节点检查
                                    postgres 运行检查
                                    pgaf 运行检查
                                    embed-monitor 组件 vm-agent 运行
                                    embed-monitor 组件 vector 运行
                                    HA 网卡运行和配置检查
                                其他
                                    如果 active 和 passive 在同一集群上，自动启用「必须放置在不同主机」的放置组策略
                                    active 虚拟机被标识为系统服务，不能手动对 vm 做一些运维操作
                                    passive 虚拟机被标识为系统服务，不能手动对 vm 做一些运维操作
                                    witness 节点如果在 Tower 上纳管，虚拟机也被标识为系统服务，不能手动对 vm 做一些运维操作
                                    文件复制方式为异步
                                任务和事件
                                    检查成功任务描述
                                    检查成功事件描述
                            部署失败
                                HA 页面展示
                                    配置界面展示失败步骤及原因
                                    HA 界面只保留最近一次的失败部署记录
                                Tower 状态
                                    在预检查阶段失败，CloudTower 仍保持单点状态正常工作
                                    在 HA 网络配置阶段失败，CloudTower 仍保持单点状态正常工作
                                    在 HA 部署前预检查阶段失败，CloudTower 仍保持单点状态正常工作
                                    在部署 witeness 阶段失败，CloudTower 仍保持单点状态正常工作
                                    在部署 active 节点阶段失败，CloudTower 不能保持单点状态正常工作
                                    在加入 passive 节点阶段失败，CloudTower 不能保持单点状态正常工作
                                    HA 部署完状态检查阶段失败，不能保证 HA 正常工作
                                    HA 部署后清理阶段失败，HA 正常工作，部署任务失败
                                重试部署
                                    在预检查阶段失败，界面提供重试按钮，再重新发起部署，自动填充上次的配置
                                    主动节点 HA 网络配置失败，界面提供重试按钮，再重新发起部署，自动填充上次的配置
                                    被动节点 HA 网络配置失败，界面提供重试按钮，再重新发起部署，自动填充上次的配置
                                    部署前检查阶段失败，界面提供重试按钮，再重新发起部署，自动填充上次的配置
                                    部署仲裁节点失败，界面上不提供重试按钮，需要人工介入处理才能重新部署
                                    部署主动节点，界面上不提供重试按钮，需要人工介入处理才能重新部署
                                    被动节点加入 HA 失败，界面上不提供重试按钮，需要人工介入处理才能重新部署
                                    重试自动填充配置后，检查配置的编辑和再次提交
                                    重试的 HA 部署，如果没有人为故障，能够部署成功
                                任务和事件
                                    部署失败的任务详情检查
                                    部署失败的事件检查
                        场景测试
                            部署失败，然后重试部署，仍然部署失败
                            部署失败，排查失败的原因，并修复后重试部署，部署成功
                            部署失败，然后重试部署，出现新的问题，仍然部署失败
                            部署失败，再使用别的配置进行部署，部署成功
                            部署失败，再使用别的配置进行部署，部署过程出现问题，部署失败
                            三个节点的时区不一致，能部署成功，各个节点使用内部的 ntp server 同步成一致
                            Tower 有配置 ntp server，部署 HA 集群
                            Tower 未配置 ntp server，部署 HA 集群
                            tower 部署好所有的系统服务，然后把 tower 转成 HA，HA 部署成功后，检查所有的系统服务工作正常，再对所有的系统服务做升级运维能成功
                Tower - cli 部署 HA
                    三节点部署
                        物理环境
                            Active(SMTX OS ELF) + Passive(SMTX OS ELF) + Witness(SMTX OS ELF)
                            Active(SMTX ELF) + Passive(SMTX OS VMWare) + Witness(SMTX OS VMWare)
                            Active(SMTX OS VMWare) + Passive(SMTX OS ELF) + Witness(SMTX OS ELF)
                            不同数据中心：Active(SMTX OS VMWare) + Passive(SMTX OS VMWare) + Witness(其他地方)
                            同一 SMTX VMWare 集群：Active + Passive，witness （其他地方）
                            Active(SMTX OS ELF) + Passive(SMTX ELF) + Witness(其他地方)
                            Active(ACOS ELF) + Passive(ACOS VMWare) + Witness(其他地方)
                        网络环境
                            HA 网络与管理网络处于同一网段，单管理网络，单 HA 网络
                            HA 网络和管理网络处于不同网段，单管理网络，单 HA 网络
                            HA 网络和管理网络处于不同网段，HA 节点也处于不同网段，单管理网络，多 HA 网络
                        节点规格
                            active & passive：8C 19G 400G，witness：4C 8G 200G
                        HA 启用  -- 等具体的 cli 命令确定了再补充
                            预检查
                                active，passive，witness 三节点中任意节点 的 hostname 相同，不能部署，返回对应错误信息
                                active 和 witness HA 网络不联通，不能部署，返回对应错误信息
                                passive 节点 HA 网络延迟超过 10ms，不能部署
                                witness 节点 HA 网络延迟超过 10ms，不能部署
                                active 节点不满足 spec 要求，不能部署，返回对应错误信息
                                passive 节点不满足 spec 要求，不能部署，返回对应错误信息
                                witness 节点不满足 spec 要求，不能部署，返回对应错误信息
                                active、passive、witness 任一架构不同，不能部署
                                witness 不是健康状态 ？
                                passive 不是开机状态 ？
                                三个节点的时间是否需要一致？
                                active 处于升级状态 ？是否需要处理这种状态，有可能升级和 HA 同时提交？
                                active 节点剩余磁盘空间检查？
                                passive 节点剩余磁盘空间检查？
                            部署过程故障
                                部署时 witness 不可访问
                                部署时 witness 服务 down 掉
                                部署时 witness 节点掉电
                                部署 passive 节点失败
                                部署时，触发 Tower 升级操作
                                launcherd 异常重启
                            部署检查
                                部署成功检查
                                    HA 页面展示
                                        HA 页面展示基本 HA 信息，各个节点的状态、网络、节点信息等
                                    主节点检查
                                        HA controller 运行及配置检查
                                        k8s control plane pod 运行检查
                                        k8s api server 运行检查
                                        postgres 运行检查
                                        pgaf 运行检查
                                        prisma & prisma worker 运行检查
                                        local-path-provisioner 运行检查
                                        coredns 运行检查
                                        containerd  运行检查
                                        kine 运行检查
                                        file server 运行检查
                                        业务 pod：temporal 运行检查
                                        业务 pod：drs-operator 运行检查
                                        vip 网卡运行正常，检查网卡设置 ONBOOT 为 no
                                        HA 网卡运行正常，检查网卡设置 ONBOOT 为 yes
                                        embed-monitor 组件 grafana 运行
                                        embed-monitor 组件 vm-single 运行
                                        embed-monitor 组件 vm-agent 运行
                                    从节点检查
                                        HA controller 运行及配置检查
                                        k8s control plane pod 运行检查
                                        k8s api server 运行检查
                                        postgres 运行检查
                                        业务 pod 不运行？
                                        pgaf 不运行
                                        kine 不运行
                                        file server 不运行
                                        vip 网卡 down 掉，检查网卡设置 ONBOOT 为 no
                                        HA 网卡运行正常，检查网卡设置 ONBOOT 为 yes
                                        embed-monitor 组件 grafana 运行
                                        embed-monitor 组件 vm-single 运行
                                        embed-monitor 组件 vm-agent 运行
                                    仲裁节点检查
                                        monitor 运行检查
                                        HA 网卡运行和配置检查
                                    其他
                                        如果 active 和 passive 在同一集群上，自动启用「必须放置在不同主机」的放置组策略
                                        active 虚拟机被标识为系统服务，不能手动对 vm 做一些运维操作
                                        passive 虚拟机被标识为系统服务，不能手动对 vm 做一些运维操作
                                        witness 节点如果在 Tower 上纳管，虚拟机也被标识为系统服务，不能手动对 vm 做一些运维操作
                                        文件复制方式为异步
                                        主节点所在集群可能未被 tower 纳管
                                    任务和事件
                                        检查任务描述
                                        检查事件描述
                                部署失败检查
                                    配置界面展示失败步骤及原因
                                    CloudTower 仍保持单点状态
                                HA 部署
                                    部署中，前端不能再提交部署请求
                                    部署中，通过 API 再次提交部署请求应该报错
                                    部署中，顶部会展示 HA 部署提示的 banner
                                    点击顶部部署 HA banner 的「查看进度」，跳转展示部署中页面
                                    部署中的页面会展示：当前步骤名，进度条，时间等信息，对照设计文档检查
                                    部署中，检查任务的信息展示
                                    等到部署成功，页面会展示成功的状态，顶部的 banner 消失
                                    等到部署失败，会展示失败的步骤及名称，失败的状态，顶部的 banner 消失
                                    部署失败，页面会展示重试按钮，点击重试按钮，打开启用 HA 配置弹窗，并填充上一次的配置信息
                            场景测试
                                部署失败，然后重试部署，仍然部署失败
                                部署失败，排查失败的原因，并修复后重试部署，部署成功
                                部署失败，然后重试部署，出现新的问题，仍然部署失败
                                部署失败，再使用别的配置进行部署，部署成功
                                部署失败，再使用别的配置进行部署，部署过程出现问题，部署失败
                                节点所在集群未被 tower 纳管
                                节点所在集群被 tower 纳管
                手动切换主备
                    手动切换操作入口 - 系统配置的 CloudTower 高可用页面，右上角 “切换主被节点” 按钮
                    点击 “切换主被节点” 按钮 - 弹出 切换主被节点 弹窗
                    弹窗 - 标题和提示语正确
                    弹窗 - 不填写切换原因，点击 切换 按钮，弹窗关闭，触发 failover
                    弹窗 - 填写切换原因，点击 切换 按钮，弹窗关闭，触发 failover
                    弹窗 - 点击 取消 或者 X 号，弹窗关闭
                    记录入口 - 系统配置的 CloudTower 高可用页面，主被切换记录 tab 页
                    主被切换记录 tab 页 - 未操作过主被切换展示 无记录
                    主被切换记录 tab 页 - 记录主被切换的 切换方式/触发时间/耗时/发起用户/失败原因/切换原因
                    主被切换记录 tab 页 - 切换记录按照触发时间倒序排序
                    主被切换记录 tab 页 - 每页最多展示 20 项
                    主被切换记录 tab 页 - 切换原因，触发切换时没有填写则不展示
                    主被切换记录 tab 页 - 切换原因，填写了 255 个字，查看长文案展示
                    英文翻译 - 弹窗、主被切换记录 Tab 页 正常翻译
                    无仲裁节点
                        failover 成功后，原 active 节点会被隔离，需要手动加入 HA 集群并重置隔离状态
                        主被均正常
                            主向从未同步文件 - failover 成功，记录一条主被切换的记录，信息记录正确
                            主向从未同步文件 - 原 passive 节点上线为 active 节点
                            主向从未同步文件 - 原 active 节点被隔离，防止脑裂风险
                            主向从未同步文件 - fileserver 服务在新 active 拉起，db 中无数据损坏
                            主向从未同步文件 - 集群状态经历 unhealthy -> demoted
                            主向从正同步文件 - failover 成功，记录一条主被切换的记录，信息记录正确
                            主向从正同步文件 - 原 passive 节点上线为 active 节点
                            主向从正同步文件 - 原 active 节点被隔离，防止脑裂风险
                            主向从正同步文件 - fileserver 服务在新 active 拉起，同步中的那部分文件可能丢失
                            主向从正同步文件 - 集群状态经历 unhealthy -> demoted
                        主节点异常
                            主节点在上传安装包时异常 - failover 成功，记录一条主被切换的记录，信息记录正确
                            主节点在上传安装包时异常 - 原 passive 节点上线为 active 节点
                            主节点在上传安装包时异常 - 原 active 节点被隔离，防止脑裂风险
                            主节点在上传安装包时异常 - fileserver 服务在新 active 拉起，db 中无数据损坏
                            主节点在上传安装包时异常 - 节点恢复时机，集群状态，详见步骤
                            主向从正同步文件时异常 - failover 成功，记录一条主被切换的记录，信息记录正确
                            主向从正同步文件时异常 - 原 passive 节点上线为 active 节点
                            主向从正同步文件时异常 - 原 active 节点被隔离，防止脑裂风险
                            主向从正同步文件时异常 - fileserver 服务在新 active 拉起，同步中的那部分文件可能丢失
                            主向从正同步文件时异常 - 节点恢复时机，集群状态，同「主节点上传安装包时异常」
                            主节点在 failover 过程中异常 - failover 成功，记录一条主被切换记录，信息记录正确
                            主节点在 failover 过程中异常 - 原 passive 节点保持原级不变
                            主节点在 failover 过程中异常 - 原 active 节点被隔离，防止脑裂风险
                            主节点在 failover 过程中异常 - fileserver 服务在新 active 拉起，同步中的那部分文件可能丢失
                            主节点在 failover 过程中异常 - 节点恢复时机，集群状态，详见步骤
                        被节点异常
                            被节点在 failover 前异常 - 不支持 failover，当前集群状态为 demoted
                            被节点在 failover 过程中异常 - failover 失败，记录一条主被切换记录，信息记录正确
                            被节点在 failover 过程中异常 - 原 passive 节点恢复后，保持原级不变
                            被节点在 failover 过程中异常 - 原 active 节点保持原级不变
                            被节点在 failover 过程中异常 - 节点恢复时机，集群状态，详见步骤
                        主被均异常
                            主被节点在 failover 前均异常 - 不支持 failover
                            主被节点在 failover 过程中均异常 - failover 失败，记录一条主被切换记录，信息记录正确
                            主被节点在 failover 过程中均异常 - 原 passive 节点恢复后，保持原级不变
                            主被节点在 failover 过程中均异常 - 原 active 节点恢复后，保持原级不变
                            主被节点在 failover 过程中均异常 - 节点恢复时机，集群状态，详见步骤
                    有仲裁节点
                        主被仲裁均正常
                            主向从未同步文件 - failover 成功，记录一条主被切换的记录，信息记录正确
                            主向从未同步文件 - 原 passive 节点上线为 active 节点
                            主向从未同步文件 - 原 active 节点降级为 passive 节点
                            主向从未同步文件 - fileserver 服务在新 active 拉起，db 中无数据损坏
                            主向从未同步文件 - 集群状态经历 ready -> demoted -> ready
                            主向从正同步文件 - failover 成功，记录一条主被切换的记录，信息记录正确
                            主向从正同步文件 - 原 passive 节点上线为 active 节点
                            主向从正同步文件 - 原 active 节点降级为 passive 节点
                            主向从正同步文件 - fileserver 服务在新 active 拉起，同步中的那部分文件可能丢失
                            主向从正同步文件 - 集群状态经历 ready -> demoted -> ready
                        仲裁节点异常
                            仲裁节点在 failover 前异常 - failover 成功，记录一条主被切换的记录，信息记录正确
                            仲裁节点在 failover 前异常 - 原 passive 节点上线为 active 节点
                            仲裁节点在 failover 前异常 - 原 active 节点降级为 passive 节点
                            仲裁节点在 failover 前异常 - fileserver 服务在新 active 拉起，db 中无数据损坏
                            仲裁节点在 failover 前异常 - 节点恢复时机，集群状态，详见步骤
                            仲裁节点在 failover 过程中异常 - failover 成功，记录一条主被切换的记录，信息记录正确
                            仲裁节点在 failover 过程中异常 - 原 passive 节点上线为 active 节点
                            仲裁节点在 failover 过程中异常 - 原 active 节点降级为 passive 节点
                            仲裁节点在 failover 过程中异常 - fileserver 服务在新 active 拉起，db 中无数据损坏
                            仲裁节点在 failover 过程中异常 - 节点恢复时机，集群状态，详见步骤
                        主被仲裁均异常
                            主被仲裁在 failover 前均异常 - 不支持 failover，当前集群状态为 down
                            主被仲裁在 failover 过程中均异常 - failover 失败，记录一条主被切换记录，信息记录正确
                            主被仲裁在 failover 过程中均异常 - 原 passive 节点恢复后，保持原级不变
                            主被仲裁在 failover 过程中均异常 - 原 active 节点恢复后，保持原级不变
                            主被仲裁在 failover 过程中均异常 - 节点恢复时机，集群状态，详见步骤
                        被节点异常
                            被节点在 failover 前异常 - 不支持 failover，当前集群状态为 demoted
                            被节点在 failover 过程中异常 - failover 失败，记录一条主被切换记录，信息记录正确
                            被节点在 failover 过程中异常 - 原 passive 节点恢复后，保持原级不变
                            被节点在 failover 过程中异常 - 原 active 节点保持原级不变
                            被节点在 failover 过程中异常 - 节点恢复时机，集群状态，详见步骤
                        主仲裁均异常
                            主仲裁在 failover 前均异常 - failover 成功，记录一条主被切换的记录，信息记录正确
                            主仲裁在 failover 前均异常 - 原 passive 节点上线为 active 节点
                            主仲裁在 failover 前均异常 - 原 active 节点恢复后，降级为 passive 节点
                            主仲裁在 failover 前均异常 - fileserver 服务在新 active 拉起，db 中无数据损坏
                            主仲裁在 failover 前均异常 - 节点恢复时机，集群状态，详见步骤
                            主仲裁在 failover 过程中均异常 - failover 成功，记录一条主被切换的记录，信息记录正确
                            主仲裁在 failover 过程中均异常 - 原 passive 节点上线为 active 节点
                            主仲裁在 failover 过程中均异常 - 原 active 节点恢复后，降级为 passive 节点
                            主仲裁在 failover 过程中均异常 - fileserver 服务在新 active 拉起，db 中无数据损坏
                            主仲裁在 failover 过程中均异常 - 节点恢复时机，集群状态，详见步骤
                        主被均异常
                            主被在 failover 前均异常 - 不支持 failover，当前集群状态为 down
                            主被在 failover 过程中均异常 - failover 失败，记录一条主被切换记录，信息记录正确
                            主被在 failover 过程中均异常 - 原 passive 节点保持原级不变
                            主被在 failover 过程中均异常 - 原 active 节点恢复后，保持原级不变
                            主被在 failover 过程中均异常 - 节点恢复时机，集群状态，详见步骤
                        被仲裁均异常
                            被仲裁在 failover 前均异常 - 不支持 failover，当前集群状态为 demoted
                            被仲裁在 failover 过程中均异常 - failover 失败，记录一条主被切换记录，信息记录正确
                            被仲裁在 failover 过程中均异常 - 原 passive 节点恢复后，保持原级不变
                            被仲裁在 failover 过程中均异常 - 原 active 节点保持原级不变
                            被仲裁在 failover 过程中均异常 - 节点恢复时机，集群状态，详见步骤
                HA 运维
                    修改 HA 网络设置
                    修改 HA 节点 hostname
                    修改 VIP
                        KB 支持变更 CloudTower IP，变更后 HA 能正常运行
                        修改 vip，然后挂掉 witness 节点，触发集群不健康，再恢复 witness，HA 能恢复正常
                        修改 vip，然后挂掉 passive 节点，触发集群降级，再恢复 passive，HA 能恢复正常
                        修改 vip，然后挂掉 active 节点，触发集群 failover，再恢复 active，观察 HA 能恢复正常
                        修改 vip，然后做一些业务操作，部署系统服务，创建虚拟机。然后触发 failover，保证数据能正确同步
            单节点 Tower 回归
                单节点升级
                    cli 升级
                        4.6.0 UI 升级到 4.8.0，然后再通过命令行升级
                        4.6.1 命令行升级到 4.8.0，然后再通过命令行升级
                        4.7.0 命令行升级到 4.8.0，然后再通过命令行升级
                        4.7.0 UI 升级到 4.8.0，然后再通过命令行升级
                        命令行升级，界面上有升级相关 banner 提示
                        命令行升级时，UI 上无法再发起升级请求
                        UI 上正在升级中，触发命令行升级会提示升级中，不能再次升级
                        命令行升级时，可以在 UI 访问独立升级页面查看升级进度
                        命令行升级成功，UI 上能看到任务记录，不产生事件
                        命令行升级失败，UI 上能看到任务记录，不产生事件
                        命令行升级成功，UI 上能看到升级记录，升级详情和日志
                        命令行升级失败，UI 上能看到升级记录，升级详情和日志
                        命令行升级成功，UI 上有告警
                        命令行升级失败，可以处理失败原因后，在 UI 上再次发起升级
                    UI 升级
                        删除升级文件
                            上传完毕后，页面可操作删除升级文件，弹出二次确认 modal，在 tower 虚拟机文件系统删除升级文件
                            使用升级文件完成 tower 升级后，升级文件自动被清理
                            主动删除升级文件产生 tower 任务
                            上传完升级文件后，无法再上传升级文件，从页面删除升级文件后，页面上显示上传文件组件
                        独立预检查
                            支持「独立预检查」，仅进行预检查，实际不进行升级，「CloudTower 升级」页面展示目标版本的最近一次独立预检查结果
                            独立预检查过程中，页面禁用「删除文件」、「检查环境」、「升级」按钮，检查结束时，按钮激活
                            独立预不展示检查过程中，检查结果同步返回一次展示所有结果。（最新设计稿）
                            独立检查不产生 task
                            独立检查事件完成后，记录事件，事件里显示检查结果是成功还是失败
                            「检查 CloudTower 升级至 xxx 版本的升级环境」检查失败时，显示返回的错误文案，无「详情」跳转链接
                            独立预检查各检查项均通过时，展示重新检查建议
                            独立预检查存在检查项不通过时，「只看未满足」toggle 默认开启，仅显示检查不通过项
                            独立预检查将检查「目标版本高于当前版本」、「升级包架构和操作系统发行版与本 tower 匹配」、「tower 虚拟机系统内存储空间充足」、「系统内没有没有冲突的进程」、「各 pod（除开 job）均处于运行中状态」
                            独立预检查结束后，删除升级文件，显示上传组件，文件预览消失，预检查结果消失
                            独立预检查失败时，「升级」无法点击，只有当最近一次独立预检查所有检查项均通过时，「升级」按钮可点击
                            多个浏览器标签页同时点击「检查环境」按钮，独立返回结果不会冲突
                            CloudTower Pods 未处于运行中状态，展示未满足
                            目标版本低于当前版本，展示未满足
                            IO 检查不通过，展示未满足
                            CloudTower 虚拟机的容量规格不符合要求，展示未满足
                            空间不足，独立预检查失败，展示错误提示
                            目标 CPU 架构、操作系统与当前 CloudTower 不一致，展示未满足
                            k9s 进程检查冲突，展示错误提示
                        升级
                            当升级文件文件上传完毕后，出现「升级」按钮，此时可以点击「升级」触发升级
                            如果进行过「独立预检查」，需要最近一次「独立预检查」所有检查项均通过，「升级」按钮才可点击
                            点击「升级」按钮后，出现二次确认弹窗，确认后 tower 页面展示顶部 banner 提示正在进行升级，存在「查看进度」按钮，点击后在新标签页打开独立升级页
                            「系统配置 - CloudTower 升级」页中「升级」Tab 页出现正在升级提示，存在「查看进度」按钮，在新标签页访问独立升级页 url
                            确认升级后，「系统配置 - CloudTower 升级」页中的「删除文件」、「检查环境」、「升级」按钮无法点击
                            确认升级后，产生「将 CloudTower 从版本 xxx 升级至 xxx」任务，任务卡片提供「详情」按钮，点击在新窗口打开「独立升级页」
                            「将 CloudTower 从版本 xxx 升级至 xxx」任务进行中时，任务卡片能展示当前阶段「正在检查环境」或「正在升级」
                            「将 CloudTower 从版本 xxx 升级至 xxx」任务失败时，任务卡片中展示失败信息，以及跳转链接
                            多个浏览器标签页同时点击「升级」按钮并在二次确认，只有一个能够发起
                            发起升级操作之后，不再展示在此之前的预检查结果
                        升级记录
                            「系统配置 > CloudTower 升级」存在「升级记录」TAB 页
                            展示所有通过「系统配置 - CloudTower 升级」操作的升级记录，单个记录包含开始时间、耗时、升级成功或失败
                            仅最近一次升级记录提供「详情」按钮，跳转独立升级页
                            预检查失败的升级记录，展示「环境检查不通过」
                            在升级阶段失败的升级记录，显示%具体的升级步骤名%出错
                        独立升级页
                            触发 tower 升级后，访问独立升级页显示「CloudTower 升级」，需要输入 cloudtower 账户密码完成认证后查看进度
                            当前 tower 不在升级状态，访问独立升级页，需要输入 cloudtower 账户密码认证
                            当前 tower 从未进行使用过「CloudTower 升级」，访问独立升级页，需要输入 cloudtower 账户密码认证，显示「无 CloudTower 升级记录」
                            独立升级页显示「无 CloudTower 升级记录」时，存在跳转链接，点击后在新标签页访问「系统配置 > CloudTower  升级」页面 url，浏览器 local storage 无 token 时重定向到 tower 登录页
                            独立升级页，密码输入框为空时，「查看进度」按钮无法点击，密码输入框有内容时，「查看进度」按钮变为可点击
                            独立升级页，点击「查看进度」按钮，实际是使用 tower 虚拟机系统内的 cloudtower 账户密码进行 ssh 登录校验，验证通过返回给客户端一个 24 小时的 jwt 放置在 localstorage
                            独立升级页可切换中英文，aoc 只能使用英文
                            进度页展示升级的目标版本以及当前进度，仅展示一个进度条，前者通过后展示后者，共有8个步骤
                            进度条展示整个升级行为的开始时间，已用时间
                            检查升级环境的检查项有「目标版本高于当前版本」、「cpu 架构、操作系统与当前 tower 匹配」、「文件系统可用空间充足」、「不存在k9s进程」、「cloudtower pods 均处于运行中状态」
                            「检查升级环境」存在未通过项时，「只看未满足」toggle默认开启，展示未通过项
                            「检查升级环境」有其他原因导致失败时，展示错误信息
                            「检查升级环境」进度页，存在「打开 cloudtower」按钮，点击后在新的标签页访问 tower overview 页面
                            「检查升级环境」失败时，在「tower > 系统配置 > CloudTower 升级> 升级记录」页产生一条失败的记录
                            「升级中」进度页，存在「打开 cloudtower」按钮，点击后在新标签页访问 tower overview 页面
                            进度条显示当前步骤名，升级整体开始时刻，已用时
                            「升级中」进度条，当需要更新内核，但是此步骤超时，出现提示语
                            升级过程中、升级失败、升级成功，可查看升级日志，默认折叠，展开后显示日志查看器，自动定位到最新日志，宽度高度固定，自动换行。支持搜索，搜索命中高亮，搜索框支持粘贴，支持复制文本
                            日志查看器检索默认为正则搜索、且大小写不敏感，高亮命中内容
                            日志查看器固定高度，内部有滚动滑块
                            「升级中」失败，展示失败步骤，展示错误信息，日志查看器默认定位到本次升级日志的结尾
                            「升级中」失败，在「tower > 系统配置 > CloudTower 升级 > 升级记录」页产生一条失败的记录
                            「升级中」失败，出现「打开 CloudTower 」按钮，点击后在新的标签页访问 tower overview 页面
                            升级成功后，在「tower > 系统配置 > CloudTower 升级 > 升级记录」页产生一条成功的记录
                            升级成功，出现「打开 CloudTower 」按钮，点击后在新的标签页访问 tower overview 页面
                        上传升级文件
                            校验文件，清单文件中升级文件版本低于 tower 当前实际版本时，展示错误提示
                            校验文件，清单文件中，升级文件 cpu 架构信息和当前 tower 虚拟机实际架构不同时，展示错误提示
                            校验文件，清单文件中，升级文件操作系统发行版信息和当前 tower 不同时，展示错误提示
                            上传完成后出现「检查环境」、「升级」按钮
                            上传完升级文件后，「本地上传」和「URL 上传」将不再展示
                            「上传 CloudTower 升级文件」任务因手动终止失败，展示指定的错误信息
                            url 上传，launcherd 下载文件过程中中断，任务失败，产生失败的事件审计
                            本地上传升级文件成功
                            url 上传升级文件成功
                            升级文件上传，升级文件存放在主节点，不做其他节点的同步
                            上传升级文件之后，发生 failover，新的主节点没有对应的升级文件，需要重新上传
                            上传过程中，支持中止上传，分块上传立刻中止，tower 虚拟机内已经上传的分块会被清理
                        权限控制
                            没有 「Cloud Tower HA」的管理权限，但是有 「CloudTower 升级」权限，可以进行上传升级文件和升级 Tower 的操作
                            有 「Cloud Tower HA」的管理权限，没有 「CloudTower 升级」权限，在「系统配置」导航栏无法看到「CloudTower 升级」项
                            有「CloudTower 升级」权限，可以进行上传升级文件和升级 Tower 的操作
                            无「CloudTower 升级」权限的用户，在「系统配置」导航栏无法看到「CloudTower 升级」项
                            无「CloudTower 升级」权限的用户，当前 Tower 出现升级提示的顶部 banner 时，不显示「查看进度」按钮
                            无「CloudTower 升级」权限的用户，无法查看 Tower 任务卡片的详情：“上传升级文件”、“删除升级文件”、“将 CloudTower 从 xxx 升级到 xxx”
                            无「CloudTower 升级」权限的用户，无法在“上传升级文件”任务卡片操作中止
                            无「CloudTower 升级」权限的用户，当前 Tower 出现升级提示的顶部 banner 时，不显示「查看进度」按钮
                            内置角色 - 运维管理员有「CloudTower 升级」管理权限
                            内置角色 - 超级管理员有「CloudTower 升级」管理权限
                            其他内置角色没有「CloudTower 升级」的管理权限
                    场景
                        先在界面上发起 cloudtower 升级，已经通过预检查进行到正式升级步骤，此时发起命令行升级
                        先在 tower 虚拟机系统内发起命令行升级，此时在界面上发起 cloudtower 升级
                        当前是 4.6.0，使用 4.7.0 的全量升级包进行升级，携带的内核 rpm 版本变化
                        先在 tower 虚拟机系统内执行 instaler update，随后在界面上发起 cloudtower 升级
                        先在界面上发起 cloudtower 升级，随后在 tower 虚拟机系统内执行 installer update
                        在界面上发起 cloudtower 升级后，操作 tower 虚拟机重启，等待 tower server 恢复后，确认 tower 任务、事件审计、升级记录、独立升级页的显示
                        在界面上发起 cloudtower 升级后，操作 tower 虚拟机强制关机，开机后等待 tower server 恢复后，确认 tower 任务、事件审计、升级记录、独立升级页的显示
                        在界面上发起 cloudtower 升级后，操作 tower 虚拟机发生 HA，开机后等待 tower server 恢复后，确认 tower 任务、事件审计、升级记录、独立升级页的显示
                        cloudtower 升级流程有内核升级步骤，自动重启，在 launcherd 和 tower server 都无法提供服务时，刷新独立升级页
                        cloudtower 升级流程中有内核升级步骤，自动重启，在 launcherd 能提供服务但 tower server 未就绪时，分别访问 tower 和独立升级页
                        系统预检查失败，升级任务失败，检查升级结果和升级页面
                        解压升级文件失败，升级任务失败，检查升级结果和升级页面
                        升级 launcherd 失败，升级任务失败，检查升级结果和升级页面
                        升级内核失败，升级任务失败，检查升级结果和升级页面
                        等待环境就绪失败，升级任务失败，检查升级结果和升级页面
                        服务部署失败，升级任务失败，检查升级结果和升级页面
                        应用部署失败，升级任务失败，检查升级结果和升级页面
                        清理临时文件失败，升级任务失败，检查升级结果和升级页面
                        触发升级后，launcherd 有重启，检查任务能正常结束
                        升级完成后，清理升级文件失败，不影响升级成功的结果
                    任务
                        删除升级文件时，产生 Tower 任务「删除 CloudTower 升级文件 xxx」
                        上传升级文件时，产生 Tower 任务「上传 CloudTower 升级文件」
                        发起升级后，产生 Tower 任务「将 CloudTower 从版本 xxx 升级至 xxx」，任务卡片展示当前所处阶段，有访问独立升级页的超链接
                    事件审计
                        存在「上传 CloudTower 升级文件」用户审计事件类型，包含「状态」、「触发时间」、「结束时间」、「用户」、「登录 IP」、「描述」，「描述」中有升级文件名称
                        上传 CloudTower 升级文件过程中人为中止，产生「状态为失败」的事件审计
                        本地上传 CloudTower 升级文件过程中制造客户端网络中断，15分钟后，自动失败，产生「状态为失败」的事件审计
                        上传 CloudTower 升级文件过程中制造异常（停止 server 容器、上传过程中使文件系统剩余容量耗尽），恢复后，事件审计及任务正常
                        上传 CloudTower 升级文件过程中，停止 launcherd 服务，产生「状态为失败」的事件审计
                        上传 CloudTower 升级文件顺利完成，产生「状态为成功」的事件审计
                        分别从本地和 url 上传文件，「上传 CloudTower 升级文件」描述信息中，会区分上传方式
                        存在「删除 CloudTower 升级文件」用户审计事件类型，不包含「所属集群」信息，「描述」中有升级文件名称
                        构造「删除 CloudTower 升级文件」失败的情况，产生「状态为失败」的事件审计
                        当「删除 CloudTower 升级文件」顺利完成，产生「状态为成功」的事件审计
                        存在「升级前预检查」用户审计事件类型，不包含「所属集群」信息
                        构造「升级前预检查」任务本身执行失败的情况（未触发预检查或预检查异常中止），产生「状态为失败」的事件审计
                        点击「检查环境」按钮，产生「升级前预检查」用户审计事件，即使有检查不通过项，事件审计状态为成功
                        存在「启动 CloudTower 升级」用户审计事件类型，描述信息中包含当前版本和目标版本信息
                        启动升级后，在预检查阶段出现检查项不通过，产生「状态为失败」的事件审计
                        启动升级后，构造预检查未启动或预检查异常中止的情况，产生「状态为失败」的事件审计
                        启动升级后，预检查通过，在升级流程的任意步骤失败，产生「状态为失败」的事件审计
                        启动升级后，仅当升级顺利完成，才产生「状态为成功」的事件审计
                单节点部署
                    VM 的部署，日常的 smoke，以及自动化回归会覆盖
                    Installer 部署，自动化回归会覆盖
                单节点运维
                    修改  IP
                    cpu、内存扩容
                    磁盘扩容
                    AOC 备份重建
                    480 不走 etcd 了，之前的 etcd 备份重建不需要了
                    centos7.x86_64 备份重建
                    oe2003.x86_64 备份重建
                    oe2003.aarch64 备份重建
                    tl3.aarch64 备份重建
                    tl3.x86_64 备份重建
                告警规则生效检查
                    运行 { .service_type } { .service_name } 的虚拟机 { .vm_name } 的 CPU 占用过高。
                    运行 { .service_type } { .service_name } 的虚拟机 { .vm_name } 的存储空间不足。
                    运行 { .service_type } { .service_name } 的虚拟机 { .vm_name } 的内存使用率过高。
                    { .service_type } { .service_name } 未配置 NTP 服务器。
                    { .service_type } { .service_name } 无法与 NTP 服务器 { .ntp_server } 建立连接。
                    CloudTower 与 NTP 服务器时间偏移量过大。
                Tower 界面操作
                    tower 打上系统服务的标识
                    tower 可以被集群一键提升副本数
                    生命周期：移出组/移至组
                    编辑：编辑虚拟机放置组
                    快照操作：创建快照、编辑快照基本信息、删除快照
                    快照计划：加入快照计划
                    迁移操作：集群内冷/热迁移
                    标签操作：分配/移除标签
                    其他：打开终端
                    移除集群：支持移除集群
                    单节点 Tower 在主机进入维护模式时，自动热迁移到其他主机
                    单节点 Tower 在主机退出维护模式时，自动迁回到原主机
                fileserver 相关改动影响
                    定时报表的生成
                    系统服务安装包上传
                    其他业务组的，由对应 QE 回归，收集回归结果
        首次登录支持修改密码
            UI 测试
                策略启用 入口 - 系统配置 - 安全 - 密码安全，新增 首次登录修改初始密码 选项
                选项位置 - 在 密码复杂度 选项下面，密码重复限制 选项上面
                选项默认值 - 默认不开启
                选项下方提示语 - 启用后，用户首次登录时，会被要求强制修改密码。
                修改密码 入口 - 登录 - 修改密码
                页面提示语 - 首次登录需要修改密码。
                输入框 - 新密码、确认新密码，输入框内展示 inner text
                按钮 - 保存密码并登录
                英文界面下 - 页面正常翻译为英文
            启用后功能测试
                新创建的用户，未修改过密码 - 启用策略后，首次登录 CloudTower 时需要修改密码
                新创建的用户，被其他用户修改过密码 - 启用策略后，首次登录 CloudTower 时无需再修改密码
                新创建的用户，密码过期修改过密码 - 启用策略后，首次登录 CloudTower 时无需再修改密码
                升级前已创建的用户 - 启用策略后，首次登录 CloudTower 时无需再修改密码
                升级前已创建的用户，升级前修改过密码 - 启用策略后，首次登录 CloudTower 时无需再修改密码
                升级前已创建的用户，升级后修改过密码 - 启用策略后，首次登录 CloudTower 时无需再修改密码
                事件
                    启用 首次登录修改初始密码 - 触发一条 “编辑 CloudTower 访问配置” 的用户事件，详见步骤
                    关闭 首次登录修改初始密码 - 触发一条 “编辑 CloudTower 访问配置” 的用户事件，详见步骤
                    用户登录需要修改初始密码，用户名不存在导致鉴权失败 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录需要修改初始密码，初始密码有误导致鉴权失败 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录需要修改初始密码，初始密码错误次数未超过登录失败次数限制 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录需要修改初始密码，初始密码错误次数超过登录失败次数限制 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录需要修改初始密码，初始密码过期导致登录失败 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录需要修改初始密码，新密码与初始密码相同，修改失败 - 触发一条失败的 “初始化密码并登录” 的用户事件，详见步骤
                    用户登录需要修改初始密码，当前密码复杂度规则不符合实际规则，修改失败 - 触发一条失败的 “初始化密码并登录” 的用户事件，详见步骤
                    用户登录需要修改初始密码，邮件双因子验证失败 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录需要修改初始密码，邮件验证码错误 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录需要修改初始密码，邮件验证码过期 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录需要修改初始密码，短信双因子验证失败 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录需要修改初始密码，短信验证码错误 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录需要修改初始密码，短信验证码过期 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录需要修改初始密码，邮件和短信双因子验证失败 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录需要修改初始密码，修改成功（已通过邮件双因子） - 触发一条成功的 “初始化密码并登录” 的用户事件，详见步骤
                    用户登录需要修改初始密码，修改成功（已通过短信双因子） - 触发一条成功的 “初始化密码并登录” 的用户事件，详见步骤
                    用户登录需要修改初始密码，修改成功（未启用双因子） - 触发一条成功的 “初始化密码并登录” 的用户事件，详见步骤
                    英文界面下 - 用户事件正常翻译为英文
                用户登录
                    新创建用户使用初始密码登录 - 自动跳转至 修改密码 页面
                    不填写 新密码 和 确认新密码 - 保存密码失败，新密码 输入框上方报错 “请提供新密码。”
                    新密码不符合密码复杂度规则 - 保存密码失败，新密码 输入框下方不符合规则项标红
                    不填写 确认新密码 - 保存密码失败，确认新密码 输入框下方报错 “请再次确认新密码。”
                    新密码与初始密码相同 - 保存密码失败，新密码 输入框下方报错 “新密码不可与初始密码相同。”
                    确认新密码 与 新密码 不一致 - 保存密码失败，确认新密码 输入框下方报错 “再次输入的密码与新密码不一致。”
                    关闭 修改密码 页面，访问 https://ip/#/overview - 仍跳转至登录页面
                    在 修改密码 页面刷新 - 重新回到登录页面
                    在 修改密码 页面，修改成功前，该用户密码被管理员修改 - 保存密码失败，报错 “密码已被修改，请刷新页面并重新登录”
                    在 修改密码 页面，修改成功前，该用户密码被管理员修改 - 刷新页面，使用管理员修改的密码，登录成功
                    登出后使用旧的初始密码登录 - 登录失败
                    登出后使用修改后的新密码登录 - 登录成功
                    英文界面下 - 报错信息正常翻译为英文
                    Tower license 过期，用户登录时需要修改初始密码 - 可修改密码成功并登录至 CloudTower
                    在修改密码页面，修改成功前，启用了双因子 - 修改密码成功并登录至 CloudTower，无需再做双因子验证
                    未修改过密码的新创建用户，在启用策略前已登录 - 启用策略后，强制登出，需要重新登录并修改初始密码
                    在 修改密码 页面，修改成功前，策略被关闭 - 保存密码成功，并登录至 CloudTower，触发一条 “初始化密码并登录” 的用户事件
                    root 超级管理员，启用策略前登录 - 启用后，不会强制登出，重新登录也不需要修改密码
                    密码复杂度
                        密码复杂度为 低复杂度 - 用户登录时修改初始密码，新密码需要符合密码低复杂度规则
                        密码复杂度为 中复杂度 - 用户登录时修改初始密码，新密码需要符合密码中复杂度规则
                        密码复杂度为 高复杂度 - 用户登录时修改初始密码，新密码需要符合密码高复杂度规则
                        用户初始密码复杂度为低，登录时要求密码复杂度为中 - 使用初始密码可以登录并自动跳转至修改密码页面
                        修改密码成功，通过新密码登录 CloudTower - 可以登录成功
                        用户在修改密码过程中，密码复杂度规则更新 - 修改密码时 api 报错，限制使用旧密码复杂度规则
                    密码重复限制
                        新创建的用户，通过编辑用户修改初始密码，新密码与初始密码相同 - 修改失败，报错 “新密码不可与初始密码相同。”
                        新创建的用户，通过编辑用户修改初始密码，新密码与初始密码不同 - 修改成功
                        新创建的用户，通过密码过期修改初始密码，新密码与初始密码相同 - 修改失败，报错 “新密码与当前密码相同。”
                        新创建的用户，通过密码过期修改初始密码，新密码与初始密码不同 - 修改成功
                        新创建的用户，用户登录时修改初始密码，新密码与初始密码相同 - 修改失败，报错 “新密码不可与初始密码相同。”
                        新创建的用户，用户登录时修改初始密码，新密码与初始密码不同 - 修改成功
                        升级前已创建的用户，未修改过密码，通过编辑用户修改当前密码，新密码与当前密码相同 - 修改失败，报错密码重复
                        升级前已创建的用户，未修改过密码，通过编辑用户修改当前密码，新密码与当前密码不同 - 修改成功
                        升级前已创建的用户，未修改过密码，通过个人设置修改当前密码，新密码与当前密码相同 - 修改失败，报错密码重复
                        升级前已创建的用户，未修改过密码，通过个人设置修改当前密码，新密码与当前密码不同 - 修改成功
                        升级前已创建的用户，未修改过密码，通过密码过期修改当前密码，新密码与当前密码相同 - 修改失败，报错 "新密码与当前密码相同。"
                        升级前已创建的用户，未修改过密码，通过密码过期修改当前密码，新密码与当前密码不同 - 修改成功
                        新创建的用户，修改过密码，通过编辑用户修改当前密码，新密码与当前密码相同 - 修改失败，报错密码重复
                        新创建的用户，修改过密码，通过编辑用户修改当前密码，新密码与过去最新使用过的 5 个密码不同 - 修改成功
                        新创建的用户，修改过密码，通过密码过期修改当前密码，新密码与当前密码相同 - 修改失败，报错 "新密码与当前密码相同。"
                        新创建的用户，修改过密码，通过密码过期修改当前密码，新密码与过去最新使用过的 5 个密码不同 - 修改成功
                        新创建的用户，修改过密码，通过个人设置修改当前密码，新密码与当前密码相同 - 修改失败，报错密码重复
                        新创建的用户，修改过密码，通过个人设置修改当前密码，新密码与过去最新使用过的 5 个密码不同 - 修改成功
                    登录失败次数限制
                        用户使用初始密码登录失败次数，未超过登录失败次数限制 - 密码仍错误，无法进入到修改密码页面
                        用户使用初始密码登录失败次数，超过登录失败次数限制 - 密码正确，无法进入到修改密码页面
                        账号超过锁定时间后，使用正确的初始密码登录 - 跳转至修改密码页面，密码修改成功，登录至 CloudTower
                    启用双因子
                        启用邮件认证，用户没有邮箱，用户名和密码鉴权成功 - 报错，无法跳转到身份验证页面
                        启用邮件认证，用户已填写邮箱，用户名和密码鉴权成功 - 跳转到身份验证页面，自动发送验证码
                        启用短信认证，用户没有手机号码，用户名和密码鉴权成功 - 报错，无法跳转到身份验证页面
                        启用短信认证，用户已填写手机号码，用户名和密码鉴权成功 - 跳转到身份验证页面，自动发送验证码
                        启用邮件和短信认证，用户未填写邮箱，用户名和密码鉴权成功 - 跳转到身份验证页面，自动发送验证码
                        启用邮箱和短信认证，用户未填写手机号码，用户名和密码鉴权成功 - 跳转到身份验证页面，自动发送验证码
                        启用邮箱和短信认证，用户未填写邮箱和手机号码，用户名和密码鉴权成功 - 报错，无法跳转到身份验证页面
                        启用邮箱和短信认证，用户已填写邮箱和手机号码，用户名和密码鉴权成功 - 跳转到身份验证页面，自动发送验证码
                        输入错误的验证码 - 无法进入到修改密码页面
                        输入正确的验证码 - 进入到修改密码页面，密码修改成功，登录至 CloudTower
                    会话超时
                        用户登录时修改初始密码后，登录成功，超时自动登出后 - 使用初始密码登录失败
                        用户登录时修改初始密码后，登录成功，超时自动登出后 - 使用新密码登录成功，无需再修改密码
                    用户角色
                        新创建的 运维管理员，未修改过密码 - 启用策略后，首次登录 CloudTower 时需要修改密码
                        新创建的 运维管理员，修改过密码 - 启用策略后，首次登录 CloudTower 时无需再修改密码
                        新创建的 只读用户，未修改过密码 - 启用策略后，首次登录 CloudTower 时需要修改密码
                        新创建的 只读用户，修改过密码 - 启用策略后，首次登录 CloudTower 时无需再修改密码
                        新创建的 安全审计员，未修改过密码 - 启用策略后，首次登录 CloudTower 时需要修改密码
                        新创建的 安全审计员，修改过密码 - 启用策略后，首次登录 CloudTower 时无需再修改密码
                        新创建的 用户管理员，未修改过密码 - 启用策略后，首次登录 CloudTower 时需要修改密码
                        新创建的 用户管理员，修改过密码 - 启用策略后，首次登录 CloudTower 时无需再修改密码
                        新创建的 虚拟机使用者，未修改过密码 - 启用策略后，首次登录 CloudTower 时需要修改密码
                        新创建的 虚拟机使用者，修改过密码 - 启用策略后，首次登录 CloudTower 时无需再修改密码
                        新创建的 工作负载集群使用者，未修改过密码 - 启用策略后，首次登录 CloudTower 时需要修改密码
                        新创建的 工作负载集群使用者，修改过密码 - 启用策略后，首次登录 CloudTower 时无需再修改密码
                        新创建的 自定义权限用户，未修改过密码 - 启用策略后，首次登录 CloudTower 时需要修改密码
                        新创建的 自定义权限用户，修改过密码 - 启用策略后，首次登录 CloudTower 时无需再修改密码
                    用户创建来源
                        本地用户 - 支持修改密码，存在 首次登录修改初始密码 限制
                        LDAP/AD 用户 - 不支持修改密码，不存在 首次登录修改初始密码 限制
                        SSO 用户 - 不支持修改密码，不存在 首次登录修改初始密码 限制
            未启用功能回归
                事件
                    用户登录不需要修改初始密码，用户名不存在导致鉴权失败 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录不需要修改初始密码，密码有误导致鉴权失败 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录不需要修改初始密码，密码错误次数未超过登录失败次数限制 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录不需要修改初始密码，密码错误次数超过登录失败次数限制 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录不需要修改初始密码，密码过期导致登录失败 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录不需要修改初始密码，邮件双因子验证失败 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录不需要修改初始密码，邮件验证码错误 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录不需要修改初始密码，邮件验证码过期 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录不需要修改初始密码，短信双因子验证失败 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录不需要修改初始密码，短信验证码错误 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录不需要修改初始密码，短信验证码过期 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                    用户登录不需要修改初始密码，邮件和短信双因子验证失败 - 触发一条失败的 "用户登录" 的用户事件，详见步骤
                用户登录
                    新创建和升级前已创建的用户，没修改过密码 - 首次登录 CloudTower 时，不需要修改密码
                    新创建和升级前已创建的用户，修改过密码 - 首次登录 CloudTower 时，不需要修改密码
                    Tower license 过期，用户登录时无需修改初始密码 - 登录至 CloudTower 成功
                    新创建的用户，没修改过密码 - 启用策略后，再次登录 CloudTower 时，需要修改密码
                    新创建的用户，修改过密码 - 启用策略后，再次登录 CloudTower 时，不需要修改密码
                    启用双因子
                        启用邮件认证，用户已填写邮箱，用户名和密码鉴权成功 - 跳转到身份验证页面，自动发送验证码
                        启用短信认证，用户已填写手机号码，用户名和密码鉴权成功 - 跳转到身份验证页面，自动发送验证码
                        启用邮箱和短信认证，用户已填写邮箱和手机号码，用户名和密码鉴权成功 - 跳转到身份验证页面，自动发送验证码
                        输入正确的验证码 - 登录至 CloudTower 成功
                    用户角色
                        新创建的 运维管理员，未修改过密码 - 未启用策略，首次登录 CloudTower 时，不需要修改密码
                        新创建的 只读用户，未修改过密码 - 未启用策略，首次登录 CloudTower 时，不需要修改密码
                        新创建的 安全审计员，未修改过密码 - 未启用策略，首次登录 CloudTower 时，不需要修改密码
                        新创建的 用户管理员，未修改过密码 - 未启用策略，首次登录 CloudTower 时，不需要修改密码
                        新创建的 虚拟机使用者，未修改过密码 - 未启用策略，首次登录 CloudTower 时，不需要修改密码
                        新创建的 工作负载集群使用者，未修改过密码 - 未启用策略，首次登录 CloudTower 时，不需要修改密码
                        新创建的 自定义权限用户，未修改过密码 - 未启用策略，首次登录 CloudTower 时，不需要修改密码
            权限测试
                已分配「运维管理和设置- CloudTower 级别 - 密码安全」权限的用户 - 可操作启用和关闭
                未分配「运维管理和设置- CloudTower 级别 - 密码安全」权限的用户 - 选项置灰
            升级测试
                低版本升级至当前版本 - 新增 首次登录修改初始密码 功能
            API 测试
                新创建的用户，通过 api 修改密码，启用策略后 - 用户登录时不需要再修改密码，触发 “修改密码” 和 “用户登录” 事件
                新创建的用户，未修改过密码，启用策略后，通过 api 访问虚拟机列表 - 报错，无法访问
                新创建的用户，未修改过密码，关闭策略，通过 api 访问虚拟机列表 - 返回正常
                在 修改密码 页面，修改成功前，该用户密码被管理员修改，浏览器 fetch 发送登录请求 - 登录成功
        Agent-mesh 回归
            x-86 Tower
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，agent-mesh 正常
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，对 agent-mesh 做升级操作能成功
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，卸载 agent-mesh 正常
                4.6.2 上传安装包，然后升级到 4.8.0，使用 4.6.2 上传的安装包部署 agent-mesh 成功
                4.6.2 上传安装包，然后升级到 4.8.0，删除安装包正常
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，回归 ISO 分发
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，回归 虚拟机模板 分发
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，回归冷迁移
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，再部署 HA，再对 agent-mesh 做升级能成功
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，再部署 HA，再使用 462 上传的安装包做部署能成功
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，再部署 HA，做 HA failover，再使用 462 上传的安装包做部署能成功
                4.6.2 上传安装包，然后升级到 4.8.0，再部署 HA，删除安装包正常
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，再部署 HA，回归 ISO 分发
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，再部署 HA，回归 虚拟机模板 分发
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，再部署 HA，回归 分段 迁移
                新部署 4.8.0，agent-mesh 上传安装包，部署、升级、卸载 agent-mesh
                新部署 4.8.0，新部署 agent-mesh, 回归 ISO 分发
                新部署 4.8.0，新部署 agent-mesh, 回归 虚拟机模板 分发
                新部署 4.8.0，新部署 agent-mesh, 回归冷迁移
                HA，agent-mesh 上传安装包，部署、升级、卸载 agent-mesh
                HA，新部署 agent-mesh, 回归 ISO 分发
                HA，新部署 agent-mesh, 回归 虚拟机模板 分发
                HA，新部署 agent-mesh, 回归冷迁移
                HA，部署 agent-mesh，部署过程中 failover，当前部署任务失败，等 failover 完成后，CAPP 重试，部署能成功。
                HA，升级 agent-mesh，升级过程中 failover，当前任务失败，等 failover 完成后，重新发起升级，升级能成功。
                HA，卸载 agent-mesh，卸载过程中 failover，当前任务失败，等 failover 完成后，CAPP 重试，卸载能成功，或者用户手动重试，卸载能成功。
                4.8.0 单 Tower 模拟查询数据库出错，已有的 agent-mesh 安装包不会被立即删除
                4.8.0 HA Tower 模拟查询数据库出错，已有的 agent-mesh 安装包不会被立即删除
                4.8.0 单 Tower 测速检查
                4.8.0 HA Tower 测速检查
            arm Tower
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，agent-mesh 正常
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，对 agent-mesh 做升级操作能成功
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，卸载 agent-mesh 正常
                4.6.2 上传安装包，然后升级到 4.8.0，使用 4.6.2 上传的安装包部署 agent-mesh 成功
                4.6.2 上传安装包，然后升级到 4.8.0，删除安装包正常
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，回归 ISO 分发
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，回归 虚拟机模板 分发
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，回归 冷迁移
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，再部署 HA，再对 agent-mesh 做升级能成功
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，再部署 HA，再使用 462 上传的安装包做部署能成功
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，再部署 HA，卸载 agent 正常
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，再部署 HA，做 HA failover，再使用 462 上传的安装包做部署能成功
                4.6.2 上传安装包，然后升级到 4.8.0，再部署 HA，删除安装包正常
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，再部署 HA，回归 ISO 分发
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，再部署 HA，回归 虚拟机模板 分发
                4.6.2 上传安装包，部署 agent-mesh，然后升级到 4.8.0，再部署 HA，回归 分段 迁移
                新部署 4.8.0，agent-mesh 上传安装包，部署、升级、卸载 agent-mesh
                新部署 4.8.0，新部署 agent-mesh, 回归 ISO 分发
                新部署 4.8.0，新部署 agent-mesh, 回归 虚拟机模板 分发
                新部署 4.8.0，新部署 agent-mesh, 回归冷迁移
                HA，agent-mesh 上传安装包，部署、升级、卸载 agent-mesh
                HA，新部署 agent-mesh, 回归 ISO 分发
                HA，新部署 agent-mesh, 回归 虚拟机模板 分发
                HA，新部署 agent-mesh, 回归 分段迁移
                HA，部署 agent-mesh，部署过程中 failover，当前部署任务失败，等 failover 完成后，CAPP 重试，部署能成功。
                HA，升级 agent-mesh，升级过程中 failover，当前任务失败，等 failover 完成后，重新发起升级，升级能成功。
                HA，卸载 agent-mesh，卸载过程中 failover，当前任务失败，等 failover 完成后，CAPP 重试，卸载能成功。
                4.8.0 单 Tower 模拟查询数据库出错，已有的 agent-mesh 安装包不会被立即删除
                4.8.0 HA Tower 模拟查询数据库出错，已有的 agent-mesh 安装包不会被立即删除
                4.8.0 单 Tower 测速检查
                4.8.0 HA Tower 测速检查
        NTP 优化 - CT 时间
            UI 测试
                配置入口 - 系统配置 - CloudTower 时间
                用户存在 ”运维管理和设置-CloudTower 级别-NTP 服务器“ 权限 - 可以编辑
                用户不存在 ”运维管理和设置-CloudTower 级别-NTP 服务器“ 权限 - 入口正常展示，不可编辑
                关联可观测提示
                    提示语 - ”请将 CloudTower 关联至 1.2.0 及以上版本的可观测性服务，以获取相关报警。“
                    按钮 - ”关联可观测性服务“
                    用户存在 监控运维-可观测性服务 的权限，Tower 未关联 1.2.0 及以上版本 obs - 展示提示语，包括按钮
                    用户存在 监控运维-可观测性服务 的权限，Tower 已关联 1.2.0 及以上版本 obs - 不展示提示语和按钮
                    用户不存在 监控运维-可观测性服务 的权限，Tower 未关联 1.2.0 及以上版本 obs - 展示提示语，不展示按钮
                    用户不存在 监控运维-可观测性服务 的权限，Tower 已关联 1.2.0 及以上版本 obs - 不展示提示语和按钮
                    点击 ”关联可观测服务“ 按钮 - 跳转至 可观测性 页面
                    英文界面下 - 提示语和按钮翻译为英文
                当前时间
                    CloudTower 时区 - 展示格式为 “%区域/名称% （%UTC偏移量%）”
                    CloudTower 时区 - 查看非  Asia/Shanghai (UTC+08:00)  时区的展示（Tower 和 NTP 时间仍跟随浏览器时区展示）
                    CloudTower 时间 - 展示格式为 ”YYYY-MM-DD HH:mm:ss“
                    CloudTower 时间 - ntp 相关 api 异常，展示 ”-“
                    NTP 服务器时间 - 未配置 NTP server 则展示 ”暂未配置外部 NTP 服务器“
                    NTP 服务器时间 - 已配置且可正常获取时间，则展示格式为 ”YYYY-MM-DD HH:mm:ss“
                    NTP 服务器时间 - 已配置但是 NTP server 异常则展示 ”无法获取“
                    NTP 服务器时间 - ntp 相关 api 异常，已配置 NTP server，展示 ”无法获取“
                    英文界面下 - 字段和文案展示为英文
                NTP 服务器
                    配置建议提示 - ”建议配置 3 个及以上的外部服务器地址，并确保 CloudTower 可访问，以保证时间同步。“
                    未配置 NTP server - 展示空白状态，存在提示 ”暂未配置 NTP 服务器“
                    英文界面下 - 字段、文案和报错信息展示为英文
                    编辑
                        点击 ”编辑“ - 按钮文案变为 ”取消编辑“，点击后退出编辑模式
                        点击 ”编辑“ - 展示 ”添加服务器“、”检查有效性“、”保存“ 按钮
                        点击 ”编辑“ - 当没有 NTP 服务器时，不会展示 服务器地址列表 表头
                        点击 ”编辑“ - 存在 NTP 服务器时，展示列表，”服务器地址” 回显可编辑，状态“ 字段固定展示为 ”-“
                        添加服务器
                            点击 ”添加服务器“，新增 1 行，”服务器地址” 字段可编辑，”状态“ 字段固定展示为 ”-“，不可编辑
                            NTP 服务器只有 1 行时，不展示 remove button
                            NTP 服务器有 2 行及以上时，每一行都展示 remove button，删除至只有 1 行时，不再支持删除
                            新增至 20 行查看展示无异常
                        服务器表格
                            表格字段 - ”服务器地址“、”状态“
                            填写有效的服务器地址 - 解除 ”检查有效性“ 按钮的禁用
                            填入服务器地址的过程中 - ”保存“ 按钮一直禁用
                            服务器地址为空 - 输入框标红，下方报错 ”请填写 NTP 服务器地址。“
                            服务器地址格式非 ipv4 或 FQDN - 输入框标红，下方报错 ”请填写正确格式的 NTP 服务器地址。“
                            填写了重复的 ipv4 服务器地址 - 输入框标红，下方报错 ”地址重复“
                            填写了重复的 FQDN 服务器地址 - 输入框标红，下方报错 ”地址重复“
                            域名和 ip 重复 - 目前没有校验
                            remove button - hover 提示 ”移除“，点击后删除所在行
                        检查有效性
                            当所有服务器地址，输入框都填入有效字段 - ”检查有效性“ 按钮从禁用变成可点击的状态
                            现有服务器地址，有效性检查通过后，再添加服务器 - ”检查有效性“ 按钮切回禁用状态
                            修改某个服务器地址，地址有效 - ”检查有效性“ 按钮仍然可点
                            点击 ”检查有效性“ - 按钮显示 loading 状态，不可点击，表格下方展示文案 ”正在检查有效性...“
                            检查不通过 - 展示文案 ”有效性检查不通过，请尝试更换服务器地址。“
                            检查不通过 - ”检查有效性“ 按钮仍可以点击，”保存“ 按钮不可点（回车也不可以）
                            检查不通过 - 对应的 NTP 服务器地址下方提示 error message
                            检查通过 - 展示文案 ”有效性检查通过，请保存配置。“
                            检查通过 - ”检查有效性“ 按钮可以点击，”保存“ 按钮可以点击（回车也可以）
                        保存
                            点击 ”保存“ 按钮，发起任务，保存当前配置的 NTP 服务器配置
                            退出编辑模式
                            检查通过之后，保存按钮才可以点
                            检查通过之后，修改某个ip 或者添加新的服务器，保存变为按钮不可点
                            已有保存成功的记录，编辑删除一个，不经过检查保存按钮不可点
                    取消编辑
                        点击取消编辑，退出编辑模式
                        不会保存刚才填写的 NTP 服务器地址
                        编辑前已有 NTP 服务器，取消编辑后，仍正常展示
            功能测试
                NTP 服务器
                    检查有效性
                        不通过
                            无法 ping 通的一个地址 - 有效性检查不通过，error message 为 ”网络连通异常。“
                            可 ping 通的非 ntp 地址 - 有效性检查不通过，error message 为 ”NTP 服务端无响应。“
                            ntp 服务器异常 - 有效性检查不通过，error message 为 ”NTP 服务端无响应。“
                            2 个 ntp 的时间不一致 - 有效性检查不通过，error message 为 ”多个 NTP 服务器无法达成一致。“
                            使用 Tower 上的集群管理 ip（关联至 Tower 所用的 ip）作为 ntp 地址 - 有效性检查不通过，error message
                            使用 Tower 上的主机管理 ip 作为 ntp 地址 - 有效性检查不通过，error message
                            使用 Tower 上的集群 vip 作为 ntp 地址 - 有效性检查不通过，error message
                            使用 Tower 上的虚拟机 ip 作为 ntp 地址 - 有效性检查不通过，error message
                            Tower 上资源 ip 的校验，需要是精准匹配，不能是模糊匹配
                            获取 NTP 服务器状态失败。(FAIL_EXCEPTION 代表检查过程中出现未知错误，不好模拟)
                            Chrony 客户端检查未通过。
                            地址解析失败。
                            地址无效。-  兜底错误码（jingyue 在集群侧已测试）
                            配置 4 个 NTP 服务器，两两时间一致 -  有效性检查不通过，error message
                            英文界面下 - error message 翻译为英文
                        通过
                            配置一个服务器和 Tower 时间不一致 - 有效性检查通过
                            配置三个服务器，两个服务器时间一致，一个服务器时间不一致 - 有效性检查通过
                            两个服务器时间一致，一个服务器时间不一致，检查通过之后，删除相同的一个，不可保存，再次检查不通过
                            配置多个服务器 & 包含windows ntp 服务器
                            域名地址
                    服务器状态
                        状态 15s 同步一次
                        不同 ntp 多个显示异常
                        所有 ntp 异常，Tower 会触发告警
                        3 个 ntp 剩余一个可用的话，再次校验，可能不通过
                        NTP 服务器状态正常
                        域名无法解析（NET_ADDRESS_RESOLVE）
                        IP网络无法联通 （NET_IP_CONNECTIVITY）
                        NTP请求无响应 (NTP_RESPONSIVE)
                        chrony 检查失败
                        多个NTP服务器无法达成一致（CHRONY_MAJORITY）
                        系统时间与NTP服务器时间偏差太大（TP_DISTANCE）
                    时间同步
                        当配置的 ntp 服务都不可用 - 无法同步时间
                        NTP 服务器状态正常 - 可正常同步时间
                        域名 NTP 服务器状态正常 - 可正常同步时间
                        修改时区之后再同步 - 可正常同步时间（Tower 部署后不支持修改时区，部署前修改了时区）
                        NTP 服务器之间的时间偏差大 - 无法自动 sync
                        Tower 与 NTP 服务器之间的时间偏差大 - 无法自动 sync
                        2:1（2 个时间一致，1 个不一致）的配置，两个可用 ntp 都故障不可用，使用另一个能够同步成功
                        部分ntp服务异常，先排除状态不正常的，剩余的状态正常的ntp 能达成一致就可以同步成功
                        命令行手动为 Tower 同步时钟 - 可以同步成功
                用户事件
                    编辑 CloudTower 的 NTP 服务器，触发事件
                任务
                    编辑 CloudTower 的 NTP 服务器，触发任务
            关联回归
                报警
                    Tower 已关联 1.2.0 及以上版本的 obs - 正常展示下面四条报警规则
                    Tower 未关联 1.2.0 及以上版本的 obs - 不展示下面四条报警规则
                    域名配置的时候，解析失败之后预期触发 无法连接 NTP 的报警
                    未配置 NTP
                        报警规则
                            {系统服务类型} {系统服务名称}未配置 NTP 服务器
                        报警触发
                            Tower 未配置 NTP 服务器，持续 1min 及以上 - 触发 信息 等级的报警
                            报警信息检查 - 触发原因/影响/解决方法、报警源/等级/对象/规则/触发时间
                            英文界面下 - 报警信息正常翻译为了英文
                        报警解决
                            为 Tower 配置 NTP 服务器，持续 1min 及以上 - 未配置 NTP 服务器 的报警自动解决
                            报警信息检查 - 触发原因/影响/解决方法、报警源/等级/对象/规则/触发时间/解决时间
                        修改报警规则
                            修改报警规则的阈值和等级 - 达到新的报警规则的触发条件，触发报警
                            新增特例规则 - 达到特例规则的触发条件，触发报警
                        禁用报警规则
                            达到报警的触发条件 - 不触发报警
                        报警通知
                            已配置 邮件报警通知 - 报警可正常发送
                    无法连接 NTP
                        报警规则
                            {系统服务类型}{系统服务名称}无法与 NTP 服务器{{外部服务器地址}}建立连接
                        报警触发
                            NTP 服务未恢复，持续 1min 及以上 - 触发 注意 等级的报警
                            报警信息检查 - 触发原因/影响/解决方法、报警源/等级/对象/规则/触发时间
                            英文界面下 - 报警信息正常翻译为了英文
                        报警解决
                            设置一个有效的 NTP 服务器，持续 1min 及以上 - 报警自动解决
                            报警信息检查 - 触发原因/影响/解决方法、报警源/等级/对象/规则/触发时间/解决时间
                        修改报警规则
                            修改报警规则的阈值和等级 - 达到新的报警规则的触发条件，触发报警
                            新增特例规则 - 达到特例规则的触发条件，触发报警
                        禁用报警规则
                            达到报警的触发条件 - 不触发报警
                        报警通知
                            已配置 snmptrap 报警通知 - 报警可正常发送
                    时间偏移量大
                        报警规则
                            {系统服务类型}{系统服务名称}与 NTP 服务器时间偏移量过大
                        报警触发
                            Tower 与 NTP 时间偏移量 10-30s 内，持续 1min 及以上-触发信息等级的报警
                            Tower 与 NTP 时间偏移量 30-60s 内，持续 1min 及以上-触发注意等级的报警
                            Tower 与 NTP 时间偏移量 60s 及以上，持续 1min 及以上-触发严重等级的报警
                            报警信息检查 - 触发原因/影响/解决方法、报警源/等级/对象/规则/触发时间
                            英文界面下 - 报警信息正常翻译为了英文
                        报警解决
                            Tower 与 NTP 服务器的时间偏移量小于阈值，持续 1min 及以上 - 报警自动解决
                            报警信息检查 - 触发原因/影响/解决方法、报警源/等级/对象/规则/触发时间/解决时间
                        修改报警规则
                            修改报警规则的阈值和等级 - 达到新的报警规则的触发条件，触发报警
                            新增特例规则 - 达到特例规则的触发条件，触发报警
                        禁用报警规则
                            达到报警的触发条件 - 不触发报警
                        报警通知
                            已配置 webhook 报警通知 - 报警可正常发送
                    与可观测时间不同步
                        报警规则
                            CloudTower 与系统服务虚拟机 {.vm_name} 的时间偏移量过大
                        报警触发
                            可观测 与 Tower 时间偏移量 30-60s ，持续 1min 及以上 - 触发注意等级的报警
                            可观测与 Tower 时间偏移量 60s 及以上，持续 1min 及以上 - 触发严重等级的报警
                        报警解决
                            可观测与 Tower 时间偏差量小于阈值 ，持续 1min 及以上 - 报警自动解决
                            报警信息检查 - 触发原因/影响/解决方法、报警源/等级/对象/规则/触发时间/解决时间
                        修改报警规则
                            修改报警规则的阈值和等级 - 达到新的报警规则的触发条件，触发报警
                            新增特例规则 - 达到特例规则的触发条件，触发报警
                        禁用报警规则
                            达到报警的触发条件 - 不触发报警
                        报警通知
                            已配置 webhook 报警通知 - 报警可正常发送
            CLI 测试
                ntpm
                    help
                ntpm server
                    help
                    sync（强制同步 NTP 与 Tower 的时间）
                    show（字段名称会有变化）
                    health
                ntpm source
                    help
                    set
                    show
            升级测试
                低版本未配置 NTP 服务器，升级至当前版本 - UI 更新，无 NTP 服务器，可编辑
                低版本已配置 NTP 服务器，升级至当前版本 - UI 更新，NTP 服务器正常展示，可编辑
            故障测试
                NTP Server 失联 - Tower 时钟无法正常 sync
                Tower 与 NTP Server 之间网络异常 - Tower 时钟无法正常 sync
                Tower Server pod 重启，重启成功 - Tower 时钟可以正常 sync
                Tower NTPM pod 重启，重启成功 - Tower 时钟可以正常 sync
                Tower VM 重启，重启成功 - Tower 时钟可以正常 sync
                Tower VM 关机一段时间再开机 - Tower 时钟可以正常 sync
                手动修改浏览器时间 - Tower UI 上时间的展示会更新
                手动修改 Tower VM 时间 - Tower 时钟可以正常 sync
        630 8 条带数回归（tower 和 capp 这次都不适配 8 条带）
            agent-mesh + scos 模板分发
                tower480 及以上 + smtx elf 630，tower 首次部署系统服务， agent-mesh 部署成功，系统盘为 4 条带
                tower480 及以上 + smtx elf 630，升级 agent-mesh 成功，保持 4 条带
                tower480 及以上 + smtx elf 630，扩容 agent-mesh 成功，为 4 条带
                tower480 及以上 + smtx elf 630，卸载 agent-mesh
                tower480 及以上 + smtx os(elf) 630，tower 首次部署系统服务， agent-mesh 部署成功 4 条带
                tower480 及以上 + smtx  os(elf) 630，升级 agent-mesh 成功，为 4 条带
                tower480 及以上 + smtx  os(elf) 630，扩容 agent-mesh 成功，为 4 条带
                tower480 及以上 + smtx  os(elf) 630，卸载 agent-mesh
                630 集群的 4 条带 scos 模板分发到低版本集群，部署 agent-mesh 成功，为 4 条带
                低版本集群的 4 条带 scos 模板分发到 630 集群，部署 agent-mesh 成功，为 4 条带
            tower
                630 集群 UI installer 部署 Tower，centos7.x86_64,4 条带
                630 集群 UI installer 部署 Tower，oe2003.x86_64，4 条带
                630 集群 UI installer 部署 Tower，oe2003.aarch64，4 条带
                630 集群 UI installer 部署 Tower，tl3.x86_64，4 条带
                630 集群 UI installer 部署 Tower，tl3.aarch63，4 条带
                630 集群部署 tower  4条带，扩容成功
                zbs580 集群 UI installer 部署 Tower，centos7.x86_64
                zbs580 集群 UI installer 部署 Tower，oe2003.x86_64
                zbs580 集群 UI installer 部署 Tower，oe2003.aarch64
                zbs580 集群 UI installer 部署 Tower，tl3.x86_64
                zbs580 集群 UI installer 部署 Tower，tl3.aarch63
        630 部署 Tower 优化
            UI installer 新增前置鉴权
                访问 https://SMTX_ManageIP_Address/operation-center-installer - IP 无效，页面无法加载
                访问 https://SMTX_ManageIP_Address/operation-center-installer - IP 对应的集群版本不满足要求，页面提示缺少参数
                访问 https://SMTX_ManageIP_Address/operation-center-installer - IP 非集群 IP，页面无法加载
                访问 https://SMTX_ManageIP_Address/operation-center-installer - IP 对应的集群版本为 6.3.0 及以上，展示鉴权页面
                鉴权页面 - 提示语、输入字段 与 UI 设计稿一致
                鉴权页面 - 集群超级管理员用户名为空，点击下一步，输入框标红下方报错 ”请填写超级管理员用户名。“
                鉴权页面 - 集群超级管理员密码为空，点击下一步，输入框标红下方报错 ”请填写超级管理员密码。“
                鉴权页面 - 用户名或密码填写错误，点击下一步，页面报错 “用户名或密码错误。”
                鉴权页面 - 密码填写后，打点加密展示
                鉴权页面 - 用户名和密码均填写正确，点击下一步，集群启用 Boost，跳转至关联 CloudTower 页面
                鉴权页面 - 用户名和密码均填写正确，点击下一步，集群未启用 Boost，跳转至关联 CloudTower 页面
                鉴权页面 - 用户名和密码均填写正确，点击下一步，API 中的密码加密展示
                关联 CloudTower 页面 - 部署全新的 CloudTower 并将集群关联成功
                关联 CloudTower 页面 - 将集群关联至已有 CloudTower 成功
                切换语言 - 鉴权页面的提示语、字段、报错提示，正常翻译为英文
                安装进度页面 - 安装报错，点击返回配置步骤页面，正常返回配置 CloudTower 环境页面
                集群部署完成，跳转至关联 CloudTower 页面 - 集群 fisheye rpm 符合预期，展示鉴权页面
                集群部署完成，跳转至关联 CloudTower 页面 - 集群 fisheye rpm 不符合预期，展示关联 CloudTower 页面
                浏览器兼容 - Safari、Google、Firefox 均可通过正确的 URL 访问鉴权页面
                集群版本测试 - SMTX OS 6.3.0 及以上、fisheye rpm 版本不符合预期的集群
                集群类型测试 - SMTX OS、SMTX ELF
                集群 CPU 架构测试 - Intel x86_64、oe x86_64、Arrch64
                集群是否启用 Boost 测试 - 已启用、未启用
                集群计算平台 - ELF、VMware ESXi
                OEM 类型 - Arcfra
    Tower - 4.7.2 & 4.8.1  调整
        通过 443 端口访问集群
            Web 功能性测试
                升级的 Tower
                    集群放开的 80 端口
                        禁用集群的 80 和 443 端口，集群会失联，新版本 agent mesh 无法测速
                        禁用集群的 80 端口，然后放开集群的 443 端口，集群连接状态正常，新版本 agent mesh 可正常测速
                        集群
                            已关联的 SMTX OS（ELF）集群 - 连接状态正常
                            已关联的 SMTX ZBS 集群 - 连接状态正常
                            已关联的 SMTX ELF 集群 - 连接状态正常
                            已关联的 SMTX OS（VMware）集群 - 连接状态正常
                            新关联 SMTX OS（ELF）集群 - 关联成功
                            新关联 SMTX ZBS 集群 - 关联成功
                            新关联 SMTX ELF 集群 - 关联成功
                            新关联 SMTX OS（VMware）集群 - 关联成功
                            采集集群日志 - 采集成功
                            下载采集的集群日志 - 下载成功
                            删除采集的集群日志 - 删除成功
                        主机
                            编辑主机名 - 成功
                            主机进入维护模式 - 成功
                            集群主机硬件运行状况 - 传感器/系统事件日志 列表正常展示
                        虚拟机
                            创建/编辑/删除 虚拟机 - 成功
                            虚拟机集群内冷迁移 - 成功
                            虚拟机集群内热迁移 - 成功
                            虚拟机跨集群冷迁移 - 成功
                            虚拟机跨集群热迁移 - 成功
                            虚拟机跨集群分段迁移 - 成功
                            从回收站删除虚拟机 - 成功
                            打开虚拟机终端 - 正常打开，可以登录并输入命令
                        数据同步
                            主机节点 - 正常同步至 Tower 并正常展示
                            虚拟机数据 - 正常同步至 Tower 并正常展示
                            内容库虚拟机模版数据 - 正常同步至 Tower 并正常展示
                            内容库 ISO 映像数据 - 正常同步至 Tower 并正常展示
                        Agent Mesh
                            低版本
                                agent mesh v1.3.5 在 Tower 升级前已部署，Tower 升级后，agent mesh 可以对集群正常测速（x86）
                                agent mesh v1.3.5 在 Tower 升级后部署，可以部署成功，也可以对集群正常测速（x86）
                                升级
                                    低版本 agent mesh 升级至新版本成功（x86 版本）
                                    可以对集群正常测速
                                    内容库/虚拟机创建 通过代理 分发 ISO 成功
                                    内容库 通过代理 分发 虚拟机模版 成功
                                    通过代理跨集群分段迁移虚拟机成功
                                    检查分发后的 ISO 和分发前的 MD5 值相同
                            新版本
                                部署新版本的 agent mesh 成功（x86 版本）
                                可以对集群正常测速
                                内容库/虚拟机创建 通过代理 分发 ISO 成功
                                内容库 通过代理 分发 虚拟机模版 成功
                                通过代理跨集群分段迁移虚拟机成功
                                存在通过代理分发失败的情况，卸载代理，可以成功
                        系统服务部署
                            部署 备份/复制 成功
                            部署 代理 成功
                            部署 可观测 成功
                            部署 ER 成功
                            部署 SKS 成功
                        内容库
                            通过 Tower 内置的 data-channel URL 上传 ISO 成功
                            通过 Tower 内置的 data-channel 分发 ISO 成功
                            通过 Tower 内置的 data-channel 下载 ISO 成功
                            上传和下载后的 ISO，MD5 值相同
                            通过 Tower 内置的 data-channel 跨集群冷迁移虚拟机成功
                    集群放开的 443 端口
                        集群
                            SMTX OS（ELF）集群在 Tower 升级前关联 - 无法关联成功
                            SMTX OS（ELF）集群在 Tower 升级后关联 - 可以关联成功
                        Agent Mesh
                            低版本
                                agent mesh v1.3.4 在 Tower 升级前无法部署，因为集群异常（x86 版本）
                                agent mesh v1.3.4 在 Tower 升级后部署，可以部署成功，但是无法对集群测速（x86 版本）
                            新版本
                                部署新版本的 agent mesh 成功（x86 版本）
                                可以对集群正常测速
                                内容库/虚拟机创建 通过代理 分发 ISO 成功
                                内容库 通过代理 分发 虚拟机模版 成功
                                通过代理跨集群分段迁移虚拟机成功
                                存在通过代理分发失败的情况，卸载代理，可以成功
                        内容库
                            通过 Tower 内置的 data-channel URL 上传 ISO 成功
                            通过 Tower 内置的 data-channel 分发 ISO 成功
                            通过 Tower 内置的 data-channel 下载 ISO 成功
                            上传和下载后的 ISO，MD5 值相同
                    集群放开的 80 + 443 端口
                        集群
                            已关联的 SMTX OS（ELF）集群 - 连接状态正常
                            已关联的 SMTX ZBS 集群 - 连接状态正常
                            已关联的 SMTX ELF 集群 - 连接状态正常
                            已关联的 SMTX OS（VMware）集群 - 连接状态正常
                            新关联 SMTX OS（ELF）集群 - 关联成功
                            新关联 SMTX ZBS 集群 - 关联成功
                            新关联 SMTX ELF 集群 - 关联成功
                            新关联 SMTX OS（VMware）集群 - 关联成功
                            采集集群日志 - 采集成功
                            下载采集的集群日志 - 下载成功
                            删除采集的集群日志 - 删除成功
                        主机
                            编辑主机名 - 成功
                            主机进入维护模式 - 成功
                            集群主机硬件运行状况 - 传感器/系统事件日志 列表正常展示
                        虚拟机
                            创建/编辑/删除 虚拟机 - 成功
                            虚拟机集群内冷迁移 - 成功
                            虚拟机集群内热迁移 - 成功
                            虚拟机跨集群冷迁移 - 成功
                            虚拟机跨集群热迁移 - 成功
                            虚拟机跨集群分段迁移 - 成功
                            从回收站删除虚拟机 - 成功
                            打开虚拟机终端 - 正常打开，可以登录并输入命令
                        数据同步
                            主机节点 - 正常同步至 Tower 并正常展示
                            虚拟机数据 - 正常同步至 Tower 并正常展示
                            内容库虚拟机模版数据 - 正常同步至 Tower 并正常展示
                            内容库 ISO 映像数据 - 正常同步至 Tower 并正常展示
                        Agent Mesh
                            低版本
                                agent mesh v1.3.3 在 Tower 升级前已部署，Tower 升级后，agent mesh 可以对集群正常测速（arm 版本）
                                agent mesh v1.3.3 在 Tower 升级后部署，可以部署成功，也可以对集群正常测速（arm 版本）
                                升级
                                    低版本 agent mesh 升级至新版本成功（arm 版本）
                                    可以对集群正常测速
                                    内容库/虚拟机创建 通过代理 分发 ISO 成功
                                    内容库 通过代理 分发 虚拟机模版 成功
                                    通过代理跨集群分段迁移虚拟机成功
                                    检查分发后的 ISO 可以正常使用
                            新版本
                                部署新版本的 agent mesh 成功（arm 版本）
                                可以对集群正常测速
                                内容库/虚拟机创建 通过代理 分发 ISO 成功
                                内容库 通过代理 分发 虚拟机模版 成功
                                通过代理跨集群分段迁移虚拟机成功
                                检查分发后的 ISO 可以正常使用
                        系统服务部署
                            部署 备份/复制 成功
                            部署 代理 成功
                            部署 可观测 成功
                            部署 ER 成功
                            部署 SKS 成功
                        内容库
                            通过 Tower 内置的 data-channel URL 上传 ISO 成功
                            通过 Tower 内置的 data-channel 分发 ISO 成功
                            通过 Tower 内置的 data-channel 下载 ISO 成功
                            上传和下载后的 ISO，MD5 值相同
                            通过 Tower 内置的 data-channel 跨集群冷迁移虚拟机成功
                新部署 Tower
                    集群放开的 80 端口
                        集群
                            关联 SMTX OS（ELF）集群 - 关联成功
                            关联 SMTX ZBS 集群 - 关联成功
                            关联 SMTX ELF 集群 - 关联成功
                            关联 SMTX OS（VMware）集群 - 关联成功
                            采集集群日志 - 采集成功
                            下载采集的集群日志 - 下载成功
                            删除采集的集群日志 - 删除成功
                        主机
                            编辑主机名 - 成功
                            主机进入维护模式 - 成功
                            集群主机硬件运行状况 - 传感器/系统事件日志 列表正常展示
                        虚拟机
                            创建/编辑/删除 虚拟机 - 成功
                            虚拟机集群内冷迁移 - 成功
                            虚拟机集群内热迁移 - 成功
                            虚拟机跨集群冷迁移 - 成功
                            虚拟机跨集群热迁移 - 成功
                            虚拟机跨集群分段迁移 - 成功
                            从回收站删除虚拟机 - 成功
                            打开虚拟机终端 - 正常打开，可以登录并输入命令
                        数据同步
                            主机节点 - 正常同步至 Tower 并正常展示
                            虚拟机数据 - 正常同步至 Tower 并正常展示
                            内容库虚拟机模版数据 - 正常同步至 Tower 并正常展示
                            内容库 ISO 映像数据 - 正常同步至 Tower 并正常展示
                        Agent Mesh
                            低版本
                                部署 v1.3.5 的低版本 agent mesh，可以部署成功，也可以对集群正常测速（arm 版本）
                                将 v1.3.5 版本的 agent mesh 升级至新版本，升级成功，可以对集群正常测速（arm 版本）
                            新版本
                                部署新版本的 agent mesh 成功（arm 版本）
                                可以对集群正常测速
                                内容库/虚拟机创建 通过代理 分发 ISO 成功
                                内容库 通过代理 分发 虚拟机模版 成功
                                通过代理跨集群分段迁移虚拟机成功
                                存在通过代理分发失败的情况，卸载代理，可以成功
                        系统服务部署
                            部署 备份/复制 成功
                            部署 代理 成功
                            部署 可观测 成功
                            部署 ER 成功
                            部署 SKS 成功
                        内容库
                            通过 Tower 内置的 data-channel URL 上传 ISO 成功
                            通过 Tower 内置的 data-channel 分发 ISO 成功
                            通过 Tower 内置的 data-channel 下载 ISO 成功
                            上传和下载后的 ISO，MD5 值相同
                            通过 Tower 内置的 data-channel 跨集群冷迁移虚拟机成功
                    集群放开的 443 端口
                        禁用集群的 443 和 80 端口，集群会失联，新版本 agent mesh 无法测速
                        禁用集群的 443 端口，然后放开集群的 80 端口，集群连接状态正常，新版本 agent mesh 可正常测速
                        集群
                            关联 SMTX OS（ELF）集群 - 关联成功
                            关联 SMTX ZBS 集群 - 关联成功
                            关联 SMTX ELF 集群 - 关联成功
                            关联 SMTX OS（VMware）集群 - 关联成功
                            采集集群日志 - 采集成功
                            下载采集的集群日志 - 下载成功
                            删除采集的集群日志 - 删除成功
                        主机
                            编辑主机名 - 成功
                            主机进入维护模式 - 成功
                            集群主机硬件运行状况 - 传感器/系统事件日志 列表正常展示
                        虚拟机
                            创建/编辑/删除 虚拟机 - 成功
                            虚拟机集群内冷迁移 - 成功
                            虚拟机集群内热迁移 - 成功
                            虚拟机跨集群冷迁移 - 成功
                            虚拟机跨集群热迁移 - 成功
                            虚拟机跨集群分段迁移 - 成功
                            从回收站删除虚拟机 - 成功
                            打开虚拟机终端 - 正常打开，可以登录并输入命令
                        数据同步
                            主机节点 - 正常同步至 Tower 并正常展示
                            虚拟机数据 - 正常同步至 Tower 并正常展示
                            内容库虚拟机模版数据 - 正常同步至 Tower 并正常展示
                            内容库 ISO 映像数据 - 正常同步至 Tower 并正常展示
                        Agent Mesh
                            低版本
                                部署 v1.3.5 的低版本 agent mesh，可以部署成功，但是无法对集群测速（x86 版本）
                                部署 v1.3.4 的低版本 agent mesh，可以部署成功，但是无法对集群测速（x86 版本）
                                低版本 agent mesh 升级至新版本后，可以对集群测速（x86）
                            新版本
                                部署新版本的 agent mesh 成功（x86 版本）
                                可以对集群正常测速
                                内容库/虚拟机创建 通过代理 分发 ISO 成功
                                内容库 通过代理 分发 虚拟机模版 成功
                                通过代理跨集群分段迁移虚拟机成功
                                存在通过代理分发失败的情况，卸载代理，可以成功
                        系统服务部署
                            部署 备份/复制 成功
                            部署 代理 成功
                            部署 可观测 成功
                            部署 ER 成功
                            部署 SKS 成功
                        内容库
                            通过 Tower 内置的 data-channel URL 上传 ISO 成功
                            通过 Tower 内置的 data-channel 分发 ISO 成功
                            通过 Tower 内置的 data-channel 下载 ISO 成功
                            上传和下载后的 ISO，MD5 值相同
                            通过 Tower 内置的 data-channel 跨集群冷迁移虚拟机成功
                    集群放开的 80 + 443 端口
                        禁用集群的 443 和 80 端口，集群会失联，新版本 agent mesh 无法测速
                        禁用集群的 443 端口，然后放开集群的 80 端口，集群连接状态正常，新版本 agent mesh 可正常测速
                        禁用集群的 80 端口，然后放开集群的 443 端口，集群连接状态正常，新版本 agent mesh 可正常测速
            端口连通性测试
                新部署 Tower
                    通过 netcat 检查集群与 Tower 之间的端口连通性，端口可达
                    通过 netstat 检查 Tower 的 Nginx 进程，绑定了 443 和 80 端口
                升级的 Tower
                    通过 netcat 检查集群与 Tower 之间的端口连通性，端口可达
                    通过 netstat 检查 Tower 的 Nginx 进程，绑定了 443 和 80 端口
                新部署的 agent mesh
                    检查集群与 agent mesh 之间的端口连通性，端口可达
                升级的 agent mesh
                    检查集群与 agent mesh 之间的端口连通性，端口可达
            安全性测试
                新部署 Tower
                    通过绿盟进行漏扫 - 无端口相关漏洞
                升级的 Tower
                    通过绿盟进行漏扫 - 无端口相关漏洞
                新部署的 agent mesh
                    通过绿盟进行漏扫 - 无端口相关漏洞
                升级的 agent mesh
                    通过绿盟进行漏扫 - 无端口相关漏洞
            兼容性测试
                新部署 Tower
                    Linux + Chrome - 测试 Web 功能正常
                    当 80 和 443 端口均禁掉 - 集群失联，新版本 agent mesh 无法测速
                    当 80 和 443 端口均放开时 - 优先使用 443 端口，集群连接正常，新版本 agent mesh 可正常测速
                    先放开 80 端口，再放开 443 端口 - 切换至使用 443 端口（agent-mesh-manager、tower api）
                    当 80 端口禁掉 - 使用 443 端口，可以正常关联集群，新版本 agent mesh 可正常测速
                    先放开 443 端口，再放开 80 端口 - 仍使用 443 端口（agent-mesh-manager、tower api）
                    当 443 端口禁掉 - 使用 80 端口，集群连接正常，新版本 agent mesh 可正常测速
                    https 连接 60s 超时之后，会尝试 http 连接，可连接成功，15min 后，再尝试 https 连接
                    客户端/服务器错误，不会触发 fallback 策略
                升级的 Tower
                    Windows + Microsoft Edge - 测试 Web 功能正常
                    当 80 和 443 端口均禁掉 - 集群失联，新版本 agent mesh 无法测速
                    当 80 和 443 端口均放开时 - 优先使用 443 端口，集群连接正常，新版本 agent mesh 可正常测速
                    先放开 80 端口，再放开 443 端口 - 切换至使用 443 端口（agent-mesh-manager、tower api）
                    当 80 端口禁掉 - 使用 443 端口，可以正常关联集群，新版本 agent mesh 可正常测速
                    先放开 443 端口，再放开 80 端口 - 仍使用 443 端口（agent-mesh-manager、tower api）
                    当 443 端口禁掉 - 可自动切换至 80 端口，集群连接正常，新版本 agent mesh 可正常测速
                    https 连接 60s 超时之后，会尝试 http 连接，可连接成功，15min 后，再尝试 https 连接
                    客户端/服务器错误，不会触发 fallback 策略
        CloudTower/AOC 版本号规范适配
            CloudTower 升级
                升级页面
                    升级到新版本后，小版本，升级页面的当前 CloudTower 版本展示为 x.x Px  格式
                    升级到新版本后，非小版本，升级页面的当前 CloudTower 版本展示为 x.x
                    升级到新版本后，小版本，升级文件预览的版本展示为 x.x Px  格式
                    升级到新版本后，非小版本，升级文件预览的版本展示为 x.x
                    升级到新版本后，小版本，升级弹窗的版本展示为 x.x Px  格式
                    升级到新版本后，非小版本，升级弹窗的版本展示为 x.x
                    升级中的提示，小版本，显示 x.x Px 格式
                    升级中的提示，非小版本，显示 x.x 格式
                    升级到新版本后，小版本，升级记录里的版本展示为 x.x Px  格式
                    升级到新版本后，非小版本，升级记录里的版本展示为 x.x
                    历史的升级记录里的版本号不变，保持之前的三位展示 x.x.x
                上传安装包
                    上传升级文件，任务和信息保持升级文件的名称
                    删除升级文件，任务和信息保持升级文件的名称
                独立升级页面
                    升级到新版本后，如果是小版本，独立升级页面的版本展示为 x.x Px  格式
                    升级到新版本后，非小版本，独立升级页面的版本展示为 x.x
                事件和任务
                    升级到新版本后，如果是小版本，事件里的版本展示为 x.x Px  格式
                    升级到新版本后，非小版本，事件里的版本展示为 x.x
                    升级到新版本后，如果是小版本，任务里的版本展示为 x.x Px  格式
                    升级到新版本后，非小版本，任务里的版本展示为 x.x
                    历史的升级事件和任务描述里，保持三位版本号 x.x.x
                    低版本升级到新版本-小版本，升级完成后，事件里的记录目标版本为 x.x Px 格式
                    低版本升级到新版本-非小版本，升级完成后，事件里的记录目标版本为 x.x 格式
                    低版本升级到新版本-小版本，升级完成后，任务里的记录目标版本为 x.x Px 格式
                    低版本升级到新版本-非小版本，升级完成后，任务里的记录目标版本为 x.x  格式
                升级方式
                    UI 升级检查相关页面的展示正确
                    cli 升级后，检查升级页面的展示
                    cli 升级，检查升级记录，因为不能更改安装包里的信息，因此会展示安装包里的版本
                    cli 升级，检查独立升级页面，因为不能更改安装包里的信息，因此会展示安装包里的版本
                    cli 升级，任务信息因为不能更改安装包里的信息，因此会展示安装包里的版本
            关于页面
                小版本，检查关于页面，tower 的版本展示为 x.x Px
                非小版本，检查关于页面，tower 的版本展示为 x.x
        CloudTower 安装支持指定 iowait 阈值
            单 Tower
                VM install 部署前设置 LAUNCHERD_PRECHECK_IOWAIT_THRESHOLD 变量，然后部署 tower，检查部署时该变量生效，部署成功后，变量持久化到 /etc/sysconfig/launcherd 文件
                VM install 部署前设置 LAUNCHERD_PRECHECK_IOWAIT_THRESHOLD 变量，然后部署 tower，再通过 UI install 的方式升级 tower，变量有效
                VM install 部署前设置 LAUNCHERD_PRECHECK_IOWAIT_THRESHOLD 变量，然后部署 tower，再通过 cli 的方式升级 tower，变量有效
                部署时未设置，升级前设置 LAUNCHERD_PRECHECK_IOWAIT_THRESHOLD，cli 升级 tower，变量有效
                单机不支持 ui installer
            HA
                代码未合入 481
    AOC 471 & 480 patch
        AOC 默认时区调整
            在 ACOS-6.2.0-P4-solution-v1 集群上，VM install 部署 AOC 成功，timedatectl 检查，默认时区为 Asia/Singapore
            在 ACOS-6.2.0-P4-solution-v1 集群上，UI installer 部署 AOC 成功，UI 和 timedatectl 分别检查，默认时区为 Asia/Singapore
            在 ACOS-6.3.0-solution-v1 集群上，VM install 部署 AOC 成功，UI 和 timedatectl 分别检查，默认时区为 Asia/Singapore
            在 ACOS-6.3.0-solution-v1 集群上，UI installer 部署 AOC 成功，UI 和 timedatectl 分别检查，默认时区为 Asia/Singapore
            低版本升级至当前版本，时区仍展示原时区，例如 Asia/Shanghai
            VM install 部署 AOC 前，调整时区为 Asia/Seoul，部署成功后，时区仍为 Asia/Seoul
            UI installer 部署 AOC 前，调整时区为 Asia/Oral，部署成功后，时区仍为 Asia/Oral
            AOC 配置 NTP server 成功，可以正常从 NTP server 同步时间
            AOC 关联集群成功，触发的任务时间正常
            AOC 设置一个定时生成资产列表的任务，可以正常生成报表
            ACOS 集群的虚拟机增加，AOC 可以正常的同步虚拟机数据
    Tower - 4.9.0 调整
        CloudTower/AOC 支持中文设置角色名称
            新部署的 Tower/AOC
                界面语言设置中文
                    角色管理页面
                        验证包含中文字符角色列表排序操作
                        创建自定义角色
                            创建自定义角色 - 纯中文名称，合法混合字符名称  - 可以创建成功
                            创建自定义角色 - 包含非法混合字符名称  - 显示正确提示，创建失败
                            创建自定义角色 - 含中文字符名称 - 长度限制测试 - 若有长度限制，应正常提示；若无，应能正常存储并在 UI 截断显示
                        编辑自定义角色
                            编辑自定义角色 - 纯中文名称，合法混合字符名称 - 可以编辑成功
                            编辑自定义角色 - 包含非法混合字符名称 - 显示正确提示，编辑失败
                            编辑自定义角色 - 含中文字符名称 - 长度限制测试 - 若有长度限制，应正常提示；若无，应能正常存储并在 UI 截断显示
                    用户管理页面
                        用户管理页面 - 创建用户 - 可以选择新创建的含中文字符的角色
                        用户管理页面 - 新创建用户可以正确显示含中文字符的角色
                        用户管理页面 - 编辑用户 - 编辑过的角色在可选择列表里正确显示
                    用户事件页面
                        对创建、删除、编辑角色操作检查统计事件，角色名可正确显示
                        对编辑用户角色操作检查统计事件，角色名可正确显示
                界面语言设置英文
                    角色管理页面
                        验证包含中文字符角色列表排序操作
                        创建自定义角色
                            创建自定义角色 - 纯中文名称，合法混合字符名称  - 可以创建成功
                            创建自定义角色 - 包含非法混合字符名称  - 显示正确提示，创建失败
                            创建自定义角色 - 含中文字符名称 - 长度限制测试 - 若有长度限制，应正常提示；若无，应能正常存储并在 UI 截断显示
                        编辑自定义角色
                            编辑自定义角色 - 纯中文名称，合法混合字符名称 - 可以编辑成功
                            编辑自定义角色 - 包含非法混合字符名称 - 显示正确提示，编辑失败
                            编辑自定义角色 - 含中文字符名称 - 长度限制测试 - 若有长度限制，应正常提示；若无，应能正常存储并在 UI 截断显示
                    用户管理页面
                        用户管理页面 - 创建用户 - 可以选择新创建的含中文字符的角色
                        用户管理页面 - 新创建用户可以正确显示含中文字符的角色
                        用户管理页面 - 编辑用户 - 编辑过的角色在可选择列表里正确显示
                    用户事件页面
                        对创建、删除、编辑角色操作检查统计事件，角色名可正确显示
                        对编辑用户角色操作检查统计事件，角色名可正确显示
            升级的 Tower/AOC
                界面语言设置中文
                    角色管理页面
                        验证包含中文字符角色列表排序操作
                        创建自定义角色
                            创建自定义角色 - 纯中文名称，合法混合字符名称  - 可以创建成功
                            创建自定义角色 - 包含非法混合字符名称  - 显示正确提示，创建失败
                            创建自定义角色 - 含中文字符名称 - 长度限制测试 - 若有长度限制，应正常提示；若无，应能正常存储并在 UI 截断显示
                        编辑自定义角色
                            编辑自定义角色 - 纯中文名称，合法混合字符名称 - 可以编辑成功
                            编辑自定义角色 - 包含非法混合字符名称 - 显示正确提示，编辑失败
                            编辑自定义角色 - 含中文字符名称 - 长度限制测试 - 若有长度限制，应正常提示；若无，应能正常存储并在 UI 截断显示
                    用户管理页面
                        用户管理页面 - 创建用户 - 可以选择新创建的含中文字符的角色
                        用户管理页面 - 新创建用户可以正确显示含中文字符的角色
                        用户管理页面 - 编辑用户 - 编辑过的角色在可选择列表里正确显示
                    用户事件页面
                        对创建、删除、编辑角色操作检查统计事件，角色名可正确显示
                        对编辑用户角色操作检查统计事件，角色名可正确显示
                界面语言设置英文
                    角色管理页面
                        验证包含中文字符角色列表排序操作
                        创建自定义角色
                            创建自定义角色 - 纯中文名称，合法混合字符名称  - 可以创建成功
                            创建自定义角色 - 包含非法混合字符名称  - 显示正确提示，创建失败
                            创建自定义角色 - 含中文字符名称 - 长度限制测试 - 若有长度限制，应正常提示；若无，应能正常存储并在 UI 截断显示
                        编辑自定义角色
                            编辑自定义角色 - 纯中文名称，合法混合字符名称 - 可以编辑成功
                            编辑自定义角色 - 包含非法混合字符名称 - 显示正确提示，编辑失败
                            编辑自定义角色 - 含中文字符名称 - 长度限制测试 - 若有长度限制，应正常提示；若无，应能正常存储并在 UI 截断显示
                    用户管理页面
                        用户管理页面 - 创建用户 - 可以选择新创建的含中文字符的角色
                        用户管理页面 - 新创建用户可以正确显示含中文字符的角色
                        用户管理页面 - 编辑用户 - 编辑过的角色在可选择列表里正确显示
                    用户事件页面
                        对创建、删除、编辑角色操作检查统计事件，角色名可正确显示
                        对编辑用户角色操作检查统计事件，角色名可正确显示
        支持 TOTP 动态验证码双因子认证
            部署的 Tower/AOC
                时间偏移测试：修改 CloudTower 系统时间，验证码校验失败。
                配置认证
                    默认算法 HMAC-SHA-1 可成功绑定，正确显示“已启用”和算法
                    扩展算法 HMAC-SHA-256 或 HMAC-SHA-512 可成功绑定，正确显示“已启用”和算法
                    首次启用时展示并支持复制恢复码，点击 ”关闭“ 后页面不再展示该信息
                    个人设置 - 动态验证码页面 - 启用 - 选择默认算法 - Microsoft authenticator 扫描二维码 - 输入正确验证码 - 登陆成功
                    配置入口
                        新增动态验证码页面正确显示 - 状态：未启用 - 启用项可正常启用
                        个人设置 - 账号安全分组 - 动态验证码
                    开启认证
                        点击启用 - 动态验证码页面 - 状态已启用 - 算法正常显示
                        启用弹窗
                            启用动态码二次验证 - 算法 - 下拉选项框 - 默认 HMAC-SHA-1
                            启用动态码二次验证  - 扫描二维码 - 二维码正常显示，可扫描
                            启用动态码二次验证 - 校验验证码 - 验证码 可正常输入6位验证码 - 点击启用
                            点击启用 - 保存一次性恢复码弹窗
                                保存一次性恢复码 - 提示恢复码仅展示一次 - 可复制到剪切板 - 关闭按键可关闭弹窗
                *禁用流程
                    禁用后，下一次登录时无需进行动态验证码双因子认证
                    可通过动态验证码页面 “禁用” 入口，确认页面成功禁用
                开启后相关功能影响
                    用户管理
                        具有用户管理权限的用户能够看到 用户列表 TOTP 动态验证码启用与否状态
                        具有用户管理权限的用户能够在编辑用户页面看到动态验证码双因子认证状态
                        编辑动态认证码双因子认证后，事件页面显示相应的用户事件
                        用户使用恢复码登录成功后，事件页面显示相应的用户事件
                        用户使用错误恢复码登录失败后，事件页面显示相应的用户事件
                        动态验证码登录因缺少双因子认证所需字段信息登录失败后，事件页面显示相应的用户事件
                        动态验证码登录因验证码错误登录失败后，事件页面显示相应的用户事件
                        动态验证码登录因验证码过期登录失败后，事件页面显示相应的用户事件
                        登录时启用了双因子认证，而在登录过程中关闭了双因子 导致登陆失败后，事件页面显示相应的用户事件
                    用户登陆
                        标准双因子登录, 用户名+密码通过后，输入 TOTP 码可成功登陆
                        用户名+密码通过后，输入错误的 6 位验证码，提示验证码错误，停留在双因子认证页面
                        使用已经登录过一次且未过期的验证码再次登录，验证码应失效（One-time），无法再次登录
                        多因子切换。同时开启邮件 and / or 短信和 TOTP，在登录页允许切换认证方式，且无需重新输入第一因子（密码）
                    恢复与兜底流程
                        从登陆的二次认证页面  “无法获取动态验证码” 进入恢复入口，使用恢复码登陆成功
                        恢复码登陆成功自动进入「动态验证码」设置页面，显示 “未启用” 状态。验证动态验证码状态回到配置前
                        通过 tacli 工具用恢复码自助移除用户的动态验证码配置，且恢复码使用成功一次后失效
                        验证通过 tacli 工具移除 TOTP 配置需要的用户权限，无权限用户调用 tacli 移除操作失败且有正确报错
            升级的 Tower/AOC
                启用流程
                    扩展算法 HMAC-SHA-256 或 HMAC-SHA-512 可成功绑定，正确显示“已启用”和算法
                    首次启用时展示并支持复制恢复码，点击 ”关闭“ 后页面不再展示该信息
                登陆认证流程
                    标准双因子登录, 用户名+密码通过后，输入 TOTP 码可成功登陆
                    用户名+密码通过后，输入错误的 6 位验证码，提示验证码错误，停留在双因子认证页面
                    使用已经登录过一次且未过期的验证码再次登录，验证码应失效（One-time），无法再次登录
                    多因子切换。升级前开启邮件和短信，升级后开启TOTP，在登录页允许切换认证方式，且无需重新输入第一因子（密码）
                恢复与兜底流程
                    从登陆的二次认证页面  “无法获取动态验证码” 进入恢复入口，使用恢复码登陆成功
                    恢复码登陆成功自动进入「动态验证码」设置页面，显示 “未启用” 状态。验证动态验证码状态回到配置前
                    通过 tacli 工具用恢复码自助移除用户的动态验证码配置，且恢复码使用成功一次后失效
                    验证通过 tacli 工具移除 TOTP 配置需要的用户权限，无权限用户调用 tacli 移除操作失败且有正确报错
                禁用流程
                    禁用后，下一次登录时无需进行动态验证码双因子认证
                    可通过动态验证码页面 “禁用” 入口，确认页面成功禁用
                用户管理与事件审计
                    具有用户管理权限的用户能够看到 用户列表 TOTP 动态验证码启用与否状态
                    具有用户管理权限的用户能够在编辑用户页面看到动态验证码双因子认证状态
                    编辑动态认证码双因子认证后，事件页面显示相应的用户事件
                    用户使用恢复码登录成功后，事件页面显示相应的用户事件
                    用户使用错误恢复码登录失败后，事件页面显示相应的用户事件
                    动态验证码登录因缺少双因子认证所需字段信息登录失败后，事件页面显示相应的用户事件
                    动态验证码登录因验证码错误登录失败后，事件页面显示相应的用户事件
                    动态验证码登录因验证码过期登录失败后，事件页面显示相应的用户事件
                    登录时启用了双因子认证，而在登录过程中关闭了双因子 导致登陆失败后，事件页面显示相应的用户事件
        Tower HA 调整
            放开对 SKS 的限制
                没有 SKS Registry：不隐藏 HA 入口
                SKS Registry v1.4.1 及以下：隐藏 HA 入口
                SKS Registry v1.6.0 及以上：没有 SKS，展示入口
                SKS Registry v1.6.0 及以上：SKS >= 1.6.0，展示入口
                SKS Registry v1.6.0 及以上：SKS < 1.6.0：隐藏 HA 入口
                Tower HA SKS 主菜单可见
            HA 支持多 VIP
                主节点异常的告警
                HA 部署
                    新增配置项检查
                        必填项校验
                        多个管理 IP 配置为相同，页面提示错误信息
                        管理 IP 配置格式错误，页面提示错误信息
                        配置网关与I管理 P不在同一网段，页面提示错误信息
                        新增的管理 IP 配置项与页面其他 IP 配置重复，页面提示错误信息
                        配置 UI 校验：待补充
                        配置 API 校验：待补充
                    网络模式
                        管理网和 HA 网络不复用，管理网在两个网段，两个 VIP，HA 网在三个网段
                        管理网和 HA 网络不复用，管理网在两个网段，两个 VIP，HA 网两个网段 (active 和 witness 同网段，passive 不同)
                        管理网和 HA 网络不复用，管理网在两个网段，两个 VIP，HA 网两个网段 (active 和 passive 同网段，witness 不同)
                        管理网和 HA 网络不复用，管理网在两个网段，两个 VIP，HA 网两个网段 (witness 和 passive 同网段，active 不同)
                        管理网和 HA 网络不复用，管理网在两个网段，两个 VIP，HA 同网段
                        管理网和 HA 网复用，active、passive、witness 都在不同网段，两个 VIP
                        管理网和 HA 网复用，active、witness 一个网段、passive 在不同网段，两个 VIP
                        管理网和 HA 网复用，passive、witness 一个网段、active 在不同网段，两个 VIP
                        管理网和 HA 网络不复用，管理网同网段，但配置两个 VIP，HA 网在三个网段
                        管理网和 HA 网络不复用，管理网同网段，但配置两个 VIP，HA 网两个网段 (active 和 witness 同网段，passive 不同)
                        管理网和 HA 网络不复用，管理网同网段，但配置两个 VIP，HA 网两个网段 (active 和 passive 同网段，witness 不同)
                        管理网和 HA 网络不复用，管理网同网段，但配置两个 VIP，HA 网两个网段 (witness 和 passive 同网段，active 不同)
                        管理网和 HA 网络不复用，管理网同网段，但配置两个 VIP，HA 同网段
                        管理网和 HA 网复用，管理网同网段，但配置两个 VIP，witness 在不同网段
                        管理网和 HA 网复用，管理网同网段，但配置两个 VIP，witness 也在同一网段
                    部署成功后检查
                        HA 配置多管理IP，HA 启用成功
                        部署成功后，检查 active 和 passive 的网络配置，vip 网卡均正确设置并启用
                        部署成功后，使用 ative 的 VIP 进行访问，页面功能正常
                        部署成功后，使用 passive 的 VIP 进行访问，页面提示"当前非主节点"，并提供链接引导至主节点，跳转至主节点后，正常加载 UI
                        部署成功后，使用 passive 的 VIP 进行 API 访问，返回错误码(如403/301)，明确非主节点状态
                        部署成功后，检查高可用页面，HA 相关节点的信息展示展示正确
                    事件和任务
                        检查部署操作的事件和任务信息
                    系统服务版本兼容性检查
                        Tower + 1.3.7 以下的 agent-mesh，不允许部署 HA
                        Tower + 1.6.0 以下的 sks，不允许部署 HA
                        Tower + 1.3.1 以下的 sfs，不允许部署 HA
                        Tower + x.x.x 以下的 obs，不允许部署 HA
                        Tower + x.x.x 以下的 er，不允许部署 HA
                        Tower + x.x.x 以下的备份服务，不允许部署 HA
                    架构和部署方式
                        vm install ，centos x86, Tower 启用 HA
                        vm install ，oe2003 x86, Tower 启用 HA
                        vm install ，oe2003 aarch64, Tower 启用 HA
                        UI install ，centos x86, Tower 启用 HA
                        UI install ，oe2003 x86, Tower 启用 HA
                        UI install ，oe2003 aarch64, Tower 启用 HA
                        vm install ，centos x86, AOC 启用 HA
                        UI install ，centos x86, AOC 启用 HA
                    物理环境
                        不同的物理集群，以及双活是否需要覆盖？
                    系统服务
                        agent-mesh
                            部署低版本 agent-mesh，不允许 Tower 转多管理 IP HA
                            部署低版本 agent-mesh，允许 Tower 转单管理 IP HA
                            部署新版本 agent-mesh，允许 Tower 转多管理 IP HA
                            部署新版本 agent-mesh，允许 Tower 转单管理 IP HA
                    失败及重试
                        预检查阶段失败，修复不通过的项，重试部署能成功
                        网络配置阶段失败，能自动回滚网络设置
                        网络配置阶段失败，修正网络配置后，重试部署能成功
                        重试部署时，UI 上自动填充上一次配置的字段
                        重试部署时，如果被动节点已经不存在了，则情况相关配置，包括此次新增的管理网络的设置
                        是否有新增的预检查项，需要检查失败和错误信息
                        passive 管理网卡设置失败
                        是否检查 443 端口的开放？
                HA failover
                    基本功能
                        active 故障，触发 failover，原 passive 升为 active，新的 VIP 启用
                        failover 成功后，使用新 VIP 访问，功能正常
                        failover 成功后，旧 active 节点未恢复，使用旧 VIP 访问不可达
                        failover 成功后，旧 active 节点恢复，使用旧 VIP 访问不可达，页面有引导提示跳转至当前主节点
                        failover 成功后，检查高可用页面的 CloudTower 管理 IP 显示正确
                        failover 成功后，检查业务基本功能：上传系统服务安装包
                        failover 成功后，检查业务基本功能：创建虚拟机
                        failover 成功后，检查业务基本功能：巡检中心触发巡检任务
                        failover 成功后，检查业务基本功能：升级中心触发升级任务
                        failover 成功后，检查业务基本功能：生成报表
                    故障场景
                        active 关机，触发 failover 成功
                        active 重启，触发 failover 成功
                        active 磁盘写满，触发 failover 成功
                        active HA 网络隔离，触发 failover 成功
                        active 管理网络分区，不触发 failover
                        passive HA 网络隔离，passive 异常
                        passive 管理网络隔离，HA 网络正常，passive 不会异常，是否需要增加告警？
                        passive 管理网络隔离，HA 网络正常，触发 failover，能否成功？
                HA 升级
                    部署成功后，未进行 failover，UI 升级 Tower 成功
                    部署成功后，未进行 failover，cli 升级 Tower 成功
                    部署成功后，触发 failover 成功，UI 升级 Tower 能成功
                    部署成功后，触发 failover 成功，cli 升级 Tower 能成功
                HA 监控告警
                    passive 节点异常，检查告警触发
                    witness 节点异常，检查告警触发
                    passive 和 active 的时间偏移量太大，检查告警触发
                    witness 和 active 的时间偏移量太大，检查告警触发
                    触发 failover，检查 CloudTower 高可用故障转移完成  告警触发
                    触发 active -> passive 间延迟高，超过 1min 产生对应告警
                    触发 active->witness 间延迟高，超过 1min 产生对应告警
                    触发 passive->witness 间延迟高，超过 1min 产生对应告警
                    触发 active -> passive 网络不联通，超过 1min 产生对应告警
                    触发 active -> witness 网络不联通，超过 1min 产生对应告警
                    触发 passive->witness 网络不联通，超过 1min 产生对应告警
                    文件丢失，触发告警
                    数据同步中断，触发告警
                    failover 之后，检查各项告警能正常触发
                proxy service
                    agent-mesh
                        多管理 IP HA，部署低版本的 agent-mesh 应该报错
                        多管理 IP HA，部署支持多管理 IP 的新版本 agent-mesh 成功
                        多管理 IP 的 HA 上，部署新版本的 agent-mesh
                        多管理 IP 的 HA 上，升级低版本 agent-mesh 到最新版本
                影响模块
                    登录验证
                        VIP 在原 tower，本地登录
                        VIP 在原 tower，LDAP 登录
                        VIP 在原 tower，saml 登录
                        failover 后，VIP 发生切换，本地登录
                        failover 后，VIP 发生切换，LDAP 登录
                        failover 后，VIP 发生切换，saml 登录
                    系统服务
                        系统服务部署在 vpc 里，怎么接受 tower vip 的变更？
                API/SDK/Terraform
                    active 彻底挂掉，切换后访问
                    触发 failover，切换后访问
            单 VIP HA
                HA 部署
                    新部署 tower
                HA 升级
                    低版本 Tower 升级到 490
                HA 运维操作
                    运维操作：更新 IP
                    带系统服务，更新  IP 后各种系统服务工作正常
                    运维操作：设置 nameserver
                系统服务
                    490+低版本系统服务
                    481 +新版本系统服务
                    低版本 tower 带系统服务升级到 490
                    481 HA 部署全家桶(除SKS)，升级到 490，检查系统服务工作正常
                    481 HA  升级到 490，部署 SKS 1.6.0，检查系统服务工作正常
                API/SDK/Terraform
                    active 彻底挂掉，切换后访问
                    触发 failover，切换后访问
            单 Tower 回归
                安装部署升级
                所有系统服务正常
                新部署新版本 agent-mesh，基本功能检查
                新部署旧版本 agent-mesh，基本功能检查
                新部署旧版本 agent-mesh，升级 agent-mesh，基本功能检查
                已部署的低版本 agent-mesh，tower 升级后基本功能检查
                已部署的低版本 agent-mesh，tower 升级后，升级 agent-mesh，基本功能检查
OEM
    Logo 和文案定制
        CLI
            配置更新
                命令行
                    交互式
                        执行 ./update-oem-config.py - 回车成功进入交互式命令行
                        --api-url - 不填写 URL，直接回车，报错
                        --config-file - 存在提示语，提示输入 json 配置文件路径
                        --config-file - 不填写文件路径，直接回车，报错
                        --config-file - 填写的文件路径不存在，回车报错提示文件不存在，重新输入
                        --config-file - 填写的 json 文件路径正确，格式正确，回车，提示配置成功
                    参数式
                        通过 token 鉴权进行 OEM 配置，详见步骤
                        通过 username 和 password 鉴权进行 OEM 配置，详见步骤
                Json 文件
                    图片参数
                        logo.FAVICON - 网站图片路径，不填写字段或参数路径，配置成功，则仍展示原已有配置
                        图片路径 - 输入的路径不存在，执行命令行报错，仍展示原已有配置
                        图片路径 - 输入存在的 .png 格式的图片路径，配置成功，展示当前配置
                        图片路径 - 输入存在的 .jpg 格式的图片路径，配置成功，展示当前配置
        UI 展示
            文案检查
                中英文界面下 - 文案正确展示相应配置
                系统配置
                    产品升级
                        标题中的产品名 - 文案正确
                        当前版本中的产品名 - 文案正确
                        解析升级包，文件预览中的产品名 - 文案正确
                        环境检查，预检查项 “目标 CPU 架构、主机操作系统与当前 CloudTower 一致” - 文案正确
                        环境检查，预检查项 “CloudTower 虚拟机的空闲存储空间充足” 中的产品名 - 文案正确
                        环境检查，预检查项 “CloudTower 虚拟机的容量规格符合要求” 中的产品名 - 文案正确
                        环境检查，预检查项 “CloudTower 虚拟机的 I/O 等待不超过 30 ms” 中的产品名 - 文案正确
                        环境检查，预检查项 “CloudTower 虚拟机内没有冲突的进程” 中的产品名 - 文案正确
                        环境检查，预检查项 “CloudTower Pods 均处于运行中状态” 中的产品名 - 文案正确
                        环境检查，预检查项 “CloudTower 未安装临时补丁” 中的产品名 - 文案正确
                        升级弹窗中的产品名 - 文案正确
                        删除升级文件弹窗中的产品名 - 文案正确
                        升级中，顶部提示语中的产品名 - 文案正确
                系统服务
                    Kubernetes 服务 - 未部署的提示语正确
                    文件存储 - 未部署的提示语正确
                    巡检中心 - 巡检记录的环境检查（VMware 集群）
                独立升级页
                    登录页面，标题中的产品名 - 文案正确
                    登录页面，底部版权信息 - 文案正确
                    查看进度页面，无升级记录，标题和提示语中的产品名 - 文案正确
                    查看进度页面，存在升级记录，标题中的产品名 - 文案正确
                    查看进度页面，预检查项 “目标 CPU 架构、主机操作系统与当前 CloudTower 一致” 中的产品名 - 文案正确
                    查看进度页面，预检查项 “CloudTower 虚拟机的空闲存储空间充足” 中的产品名 - 文案正确
                    查看进度页面，预检查项 “CloudTower 虚拟机的容量规格符合要求” 中的产品名 - 文案正确
                    查看进度页面，预检查项 “CloudTower 虚拟机的 I/O 等待不超过 30 ms” 中的产品名 - 文案正确
                    查看进度页面，预检查项 “CloudTower 虚拟机内没有冲突的进程” 中的产品名 - 文案正确
                    查看进度页面，预检查项 “CloudTower pods 均处于运行中状态” 中的产品名 - 文案正确
                    查看进度页面，预检查项 “CloudTower 未安装临时补丁” 中的产品名 - 文案正确
                    查看进度页面，“打开 CloudTower” 按钮中的产品名 - 文案正确
                    查看进度页面，重启超时提示语 “CloudTower 虚拟机重启超时。请联系售后。” 中的产品名 - 文案正确
            图片检查
                登录页
                    自定义 logo 宽度 > 180px，高度 > 60px - logo 等比例缩放至 宽度 <= 180px 且 高度 <= 60px
                    自定义 logo 宽度 > 180px，高度 <= 60px - logo 等比例缩放至 宽度 = 180px
                    自定义 logo 宽度 <= 180px，高度 > 60px - logo 等比例缩放至 高度 = 60px
                    自定义 logo 宽度 <= 180px，高度 <= 60px - logo 展示原尺寸，无需缩放
                    自定义虚化背景宽度 > 622px，高度 > 622px - logo 等比例缩放至 宽度 <= 622px 且 高度 <= 622px
                    自定义虚化背景宽度 > 622px，高度 <= 622px - logo 等比例缩放至 宽度 = 622px
                    自定义虚化背景宽度 <= 622px，高度 > 622px - logo 等比例缩放至 高度 = 622px
                    自定义虚化背景宽度 <= 622px，高度 <= 622px - logo 等比例缩放至 宽度 = 622px 或 高度 = 622px
                    边界情况测试 - 使用尺寸较小的图片，例如 10*10px，查看图片展示正常
                    边界情况测试 - 使用尺寸较大的图片，例如 6000*8000px，查看图片展示正常
                    图片类型测试 - png、gif、jpeg/jpg、ico
                关于页
                    自定义 logo 宽度 > 240px，高度 > 240px - logo 等比例缩放至 宽度 <= 240px 且 高度 <= 240px
                    自定义 logo 宽度 > 240px，高度 <= 240px - logo 等比例缩放至 宽度 = 240px
                    自定义 logo 宽度 <= 240px，高度 > 240px - logo 等比例缩放至 高度 = 240px
                    自定义 logo 宽度 <= 240px，高度 <= 240px - logo 展示原尺寸，无需缩放
                    边界情况测试 - 使用尺寸较小的图片，例如 10*10px，查看图片展示正常
                    边界情况测试 - 使用尺寸较大的图片，例如 6000*8000px，查看图片展示正常
                    图片类型测试 - png、gif、jpeg/jpg、ico
                概览页
                    自定义 logo 宽度 > 120px，高度 > 36px - logo 等比例缩放至 宽度 <= 120px 且 高度 <= 36px
                    自定义 logo 宽度 > 120px，高度 <= 36px - logo 等比例缩放至 宽度 = 120px
                    自定义 logo 宽度 <= 120px，高度 > 36px - logo 等比例缩放至 高度 = 36px
                    自定义 logo 宽度 <= 120px，高度 <= 36px - logo 展示原尺寸，无需缩放
                    边界情况测试 - 使用尺寸较小的图片，例如 10*10px，查看图片展示正常
                    边界情况测试 - 使用尺寸较大的图片，例如 6000*8000px，查看图片展示正常
                    图片类型测试 - png、gif、jpeg/jpg、ico
                Loading
                    自定义 loading 宽度 > 250px，高度 > 250px - logo 等比例缩放至 宽度 <= 250px 且 高度 <= 250px
                    自定义 loading 宽度 > 250px，高度 <= 250px - logo 等比例缩放至 宽度 = 250px
                    自定义 loading 宽度 <= 250px，高度 > 250px - logo 等比例缩放至 高度 = 250px
                    自定义 loading 宽度 <= 250px，高度 <= 250px - logo 等比例缩放至 宽度 = 250px 或 高度 = 250px
                    边界情况测试 - 使用尺寸较小的图片，例如 10*10px，查看图片展示正常
                    边界情况测试 - 使用尺寸较大的图片，例如 6000*8000px，查看图片展示正常
                    图片类型测试 - png、gif、jpeg/jpg、ico
                浏览器标签
                    边界情况测试 - 使用尺寸较小的图片，例如 10*10px，查看图片展示正常
                    边界情况测试 - 使用尺寸较大的图片，例如 6000*8000px，查看图片展示正常
                    图片类型测试 - png、jpeg/jpg、svg
                独立升级页
                    登录页面，上方 logo - 图片展示正确
                    查看进度页面，上方 logo - 图片展示正确
                    自定义 logo 宽度 > 180px，高度 > 60px - logo 等比例缩放至 宽度 <= 180px 且 高度 <= 60px
                    自定义 logo 宽度 > 180px，高度 <= 60px - logo 等比例缩放至 宽度 = 180px
                    自定义 logo 宽度 <= 180px，高度 > 60px - logo 等比例缩放至 高度 = 60px
                    自定义 logo 宽度 <= 180px，高度 <= 60px - logo 展示原尺寸，无需缩放
                    页面 loading - 图片展示正确
                    自定义 loading 宽度 > 250px，高度 > 250px - logo 等比例缩放至 宽度 <= 250px 且 高度 <= 250px
                    自定义 loading 宽度 > 250px，高度 <= 250px - logo 等比例缩放至 宽度 = 250px
                    自定义 loading 宽度 <= 250px，高度 > 250px - logo 等比例缩放至 高度 = 250px
                    自定义 loading 宽度 <= 250px，高度 <= 250px - logo 等比例缩放至 宽度 = 250px 或 高度 = 250px
                    浏览器标签页的 icon - 图片展示正确
            浏览器兼容
                Microsoft Edge
                    查看配置正常展示
        升级
            已配置不符合尺寸图片的低版本 Tower - 升级后正常缩放展示
            已配置缩放后符合尺寸图片的低版本 Tower - 升级后正常展示
    榫卯改造-Tower4.7.0
        默认 footer 展示
            Tower
                未关联集群时，概览页底部 footer 展示 "榫卯企业云平台"
                关联集群时，概览页底部 footer 展示 "榫卯企业云平台"
                页面加载中时，概览页底部 footer 展示 "榫卯企业云平台"
                页面报错时，概览页底部 footer 展示 "榫卯企业云平台"
                不同浏览器看一下展示效果
                检查其他页面不展示 footer，页面展示也不受此次变更影响
                检查不同角色用户看到的展示
                英文版检查
            AOC
                AOC 保持之前的展示，概览页底部不出现 footer
        OEM 配置文件自定义 footer
            Tower
                未关联集群时，概览页底部 footer 展示自定义的 footer 文案
                关联集群时，概览页底部 footer 展示自定义的 footer 文案
                页面加载中时，概览页底部 footer 展示自定义的 footer 文案
                页面报错时，概览页底部 footer 展示自定义的 footer 文案
                同时自定义 logo 和文案、footer，检查展示均正确
                检查其他页面不展示 footer，页面展示也不受此次变更影响
                不同浏览器检查展示效果
                不同 viewport（浏览器窗口）高度下， footer 的位置是否符合预期
                检查不同角色用户看到的展示
                英文版检查
            AOC
                AOC 不受影响，不展示 footer
Tower 通用功能
    事件审计
        虚拟机操作
            开机虚拟机 - 事件标题、描述、中英文、高级搜索中的事件类型
            关机虚拟机 - 事件标题、描述、中英文、高级搜索中的事件类型
            强制关机虚拟机 - 事件标题、描述、中英文、高级搜索中的事件类型
            重启虚拟机 - 事件标题、描述、中英文、高级搜索中的事件类型
            强制重启虚拟机 - 事件标题、描述、中英文、高级搜索中的事件类型
            暂停虚拟机 - 事件标题、描述、中英文、高级搜索中的事件类型
            恢复虚拟机 - 事件标题、描述、中英文、高级搜索中的事件类型
            克隆虚拟机 - 事件标题、描述、中英文、高级搜索中的事件类型
            将虚拟机移入回收站 - 事件标题、描述、中英文、高级搜索中的事件类型
            从回收站恢复虚拟机 - 事件标题、描述、中英文、高级搜索中的事件类型
            从虚拟机移除 USB 设备 - 高级搜索中的事件类型
            导出中文用户事件 - 上述事件的事件标题和描述正确
            导出英文用户事件 - 上述事件的事件标题和描述正确
        集群操作
            关联集群 - 事件标题、描述、中英文
            移除集群 - 事件标题、描述、中英文
            导出中文用户事件 - 上述事件的事件标题和描述正确
            导出英文用户事件 - 上述事件的事件标题和描述正确
    标签
        资源页面 - 编辑标签
            编辑标签 - GPU 设备
        资源页面 - 批量编辑标签
            批量编辑标签 - GPU 设备
        特殊场景测试
            编辑标签 - 关联资源的标签名对应更新
        标签字符限制
            创建标签
                key
                    不填写 - 无法创建标签，报错
                    填写空格 - 无法创建标签，报错
                    填写中文字符 - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写英文字母 - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写数字 - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写点 “.” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写下划线 “_” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写连字符 “-” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写中文逗号 “，” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写英文逗号 “,” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写中文括号 “（）” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写英文括号 “()” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    中间存在空格 - 创建标签成功，正确展示
                    前面存在空格 - 无法创建标签，报错
                    后面存在空格 - 无法创建标签，报错
                    前后均存在空格 - 无法创建标签，报错
                    包含 中英文 数字 点 下划线 连字符 中英文逗号括号 - 创建标签成功，正确展示
                    填写加号 “+” - 无法创建标签，报错
                    报错信息 - 英文检查
                value
                    不填写 - 创建标签成功，正确展示
                    填写空格 - 无法创建标签，报错
                    填写中文字符 - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写英文字母 - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写数字 - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写点 “.” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写下划线 “_” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写连字符 “-” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写中文逗号 “，” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写英文逗号 “,” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写中文括号 “（）” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    填写英文括号 “()” - 创建标签成功，正确展示，可在标签管理页被筛选出来
                    中间存在空格 - 创建标签成功，正确展示
                    前面存在空格 - 无法创建标签，报错
                    后面存在空格 - 无法创建标签，报错
                    前后存在空格 - 无法创建标签，报错
                    包含 中英文 数字 点 下划线 连字符 中英文逗号括号 - 创建标签成功，正确展示
                    填写加号 “+” - 无法创建标签，报错
                    报错信息 - 英文检查
            编辑标签
                key
                    不填写 - 编辑标签失败，报错
                    填写空格 - 编辑标签失败，报错
                    中间存在空格 - 编辑标签成功，正确展示
                    前后存在空格 - 编辑标签失败，报错
                    包含 中英文 数字 点 下划线 连字符 中英文逗号括号 - 编辑标签成功，正确展示
                    包含加号 “+” - 编辑标签失败，报错
                    报错信息 - 英文检查
                value
                    不填写 - 编辑标签成功，正确展示
                    填写空格 - 编辑标签失败，报错
                    中间存在空格 - 编辑标签成功，正确展示
                    前后存在空格 - 编辑标签失败，报错
                    包含 中英文 数字 点 下划线 连字符 中英文逗号括号 - 编辑标签成功，正确展示
                    包含加号 “+” - 编辑标签失败，报错
                    报错信息 - 英文检查
            兼容性
                Chrome
                    标签和值 包含 中英文 数字 点 下划线 连字符 中英文逗号括号 - 创建标签成功，正确展示
                    标签名或值 前后均存在空格 - 无法创建标签，报错
                Safari
                    标签和值 包含 中英文 数字 点 下划线 连字符 中英文逗号括号 - 创建标签成功，正确展示
                    标签名或值 前后均存在空格 - 无法创建标签，报错
                FireFox
                    标签和值 包含 中英文 数字 点 下划线 连字符 中英文逗号括号 - 创建标签成功，正确展示
                    标签名或值 前后均存在空格 - 无法创建标签，报错
                Microsoft Edge
                    标签和值 包含 中英文 数字 点 下划线 连字符 中英文逗号括号 - 创建标签成功，正确展示
                    标签名或值 前后均存在空格 - 无法创建标签，报错
        关联标签
            编辑
                数据中心 - 编辑标签、标签正常展示；创建标签成功
                集群 - 编辑标签、标签正常展示；创建标签成功
                主机 - 编辑标签、标签正常展示；创建标签成功
                物理盘 - 编辑标签、标签正常展示；创建标签成功
                网口 - 编辑标签、标签正常展示；创建标签成功
                虚拟分布式交换机 - 编辑标签、标签正常展示；创建标签成功
                虚拟机网络 - 编辑标签、标签正常展示；创建标签成功
                系统网络 - 编辑标签、标签正常展示；创建标签成功
                虚拟机 - 编辑标签、标签正常展示；创建标签成功
                虚拟机快照 - 编辑标签、标签正常展示；创建标签成功
                ISO 映像 - 编辑标签、标签正常展示；创建标签成功
                虚拟机模版 - 编辑标签、标签正常展示；创建标签成功
                虚拟卷 - 编辑标签、标签正常展示；创建标签成功
                iSCSI Target - 编辑标签、标签正常展示；创建标签成功
                LUN - 编辑标签、标签正常展示；创建标签成功
                NFS Export - 编辑标签、标签正常展示；创建标签成功
                NFS 文件 - 编辑标签、标签正常展示；创建标签成功
                NVMe Subsystem - 编辑标签、标签正常展示；创建标签成功
                NVMe Namespace - 编辑标签、标签正常展示；创建标签成功
                Namespace Group - 编辑标签、标签正常展示；创建标签成功
                一致性组 - 编辑标签、标签正常展示；创建标签成功
                GPU 设备 - 编辑标签、标签正常展示；创建标签成功
            批量编辑
                数据中心 - 批量编辑标签，标签正常展示；创建标签成功
                集群 - 批量编辑标签，标签正常展示；创建标签成功
                主机 - 批量编辑标签，标签正常展示；创建标签成功
                物理盘 - 批量编辑标签，标签正常展示；创建标签成功
                网口 - 批量编辑标签，标签正常展示；创建标签成功
                虚拟分布式交换机 - 批量编辑标签，标签正常展示；创建标签成功
                虚拟机网络 - 批量编辑标签，标签正常展示；创建标签成功
                系统网络 - 批量编辑标签，标签正常展示；创建标签成功
                虚拟机 - 批量编辑标签，标签正常展示；创建标签成功
                虚拟机快照 - 批量编辑标签，标签正常展示；创建标签成功
                ISO 映像 - 批量编辑标签，标签正常展示；创建标签成功
                虚拟机模版 - 批量编辑标签，标签正常展示；创建标签成功
                虚拟卷 - 批量编辑标签，标签正常展示；创建标签成功
                iSCSI Target - 批量编辑标签，标签正常展示；创建标签成功
                LUN - 批量编辑标签，标签正常展示；创建标签成功
                NFS Export - 批量编辑标签，标签正常展示；创建标签成功
                NFS 文件 - 批量编辑标签，标签正常展示；创建标签成功
                NVMe Subsystem - 批量编辑标签，标签正常展示；创建标签成功
                NVMe Namespace - 批量编辑标签，标签正常展示；创建标签成功
                Namespace Group - 批量编辑标签，标签正常展示；创建标签成功
                一致性组 - 批量编辑标签，标签正常展示；创建标签成功
                GPU 设备 - 批量编辑标签，标签正常展示；创建标签成功
    报表
        新增/修改字段
            报表导出方式 - 立即生成、自动生成
            报表格式 - Excel、CSV
            虚拟机报表
                标签 - 为空、1 个或 2 个及以上，名称较长，包含特殊字符；与虚拟机的 标签 信息一致
                CPU 兼容性 - 与虚拟机的 CPU 兼容性 信息一致
                存储使用量 - 0、大于 0 的值；与虚拟机的 存储使用量 信息一致
                客户机操作系统 UUID - 与虚拟机的 api 中 bios_uuid 信息一致
                主机管理 IP 地址 - 与虚拟机所属主机的 管理 IP 一致
            主机报表
                IPMI IP - 不存在、存在；与主机的 IPMI IP 信息一致
            报警规则报表
                阈值 - 不存在、0、大于 0 的值；与报警规则的 阈值 信息一致
    虚拟机管理
        虚拟机列表
            Organization Scope 下测试
            Datacenter Scope 下测试
            Cluster Scope 下测试
            Host Scope 下测试
            集群类型测试 - SMTX OS、SMTX ZBS、SMTX ELF、VMware ESXi
            新增字段
                CPU 兼容性 - 在列表正常展示，字段值与虚拟机详情一致；文案较长时缩略展示
                VLAN 虚拟网卡 - 在列表正常展示，字段值与虚拟机详情一致，详见步骤
                勾选/取消勾选 列字段 - 正常展示/不展示 在列表中
                自定义列字段的位置 - 在列表中的位置正确展示
                英文界面 - 新增字段正常翻译为英文
            高级筛选
                CPU 兼容性 - 暂不支持高级筛选
                VLAN 虚拟网卡 - 暂不支持高级筛选
            列表排序
                CPU 兼容性 - 暂不支持排序
                VLAN 虚拟网卡 - 暂不支持排序
            导出列表
                导出中文列表 - 新增字段和字段值正确展示
                导出英文列表 - 新增字段和字段值正确展示
报警信息
    集群连接异常
        报警规则
            新增报警规则 - {operation center name} 与 {集群类型} 集群 {集群名}连接异常。
            新增报警规则 - 集群无法连接，因｛集群类型｝集群｛集群名｝鉴权失败。
            新增的两条报警规则的默认等级 - 信息
            英文界面下 - 报警规则正常翻译为了英文
        报警触发
            Tower 访问集群 /v2/cluster/software api 无返回 - 触发 Tower 与集群连接异常的报警
            Tower 访问集群 /v2/cluster/software api 返回 404 - 触发 Tower 与集群连接异常的报警
            Tower 访问集群 /v2/cluster/software api 返回 api 异常 - 触发 Tower 与集群连接异常的报警
            Tower 访问集群 /v2/cluster/software api 返回其他错误 - 触发 Tower 与集群连接异常的报警
            集群重装导致 UUID 变更 - 触发 Tower 与集群连接异常的报警
            Tower 访问集群 /v2/cluster/software api 返回鉴权错误 - 触发集群鉴权失败的报警
            报警信息检查 - 触发原因/影响/解决方法、报警源/等级/对象/规则/触发时间
            英文界面下 - 报警信息正常翻译为了英文
        报警解决
            Tower 访问 /v2/cluster/software api 返回正常 - Tower 与集群连接异常的报警被解决
            修正集群的用户名和密码 - 集群鉴权失败的报警被解决
            移除连接异常的集群 - Tower 与集群连接异常的报警/集群鉴权失败的报警被解决
            报警信息检查 - 触发原因/影响/解决方法、报警源/等级/对象/规则/触发时间/解决时间
        禁用报警规则
            Tower 访问集群 /v2/cluster/software api 无返回 - 不再触发 Tower 与集群连接异常的报警
            Tower 访问集群 /v2/cluster/software api 返回鉴权错误 - 不再触发集群鉴权失败的报警
        修改报警规则
            修改 Tower 与集群连接异常的报警规则等级 - 达到触发条件，触发新等级的报警
            Tower 与集群连接异常的报警新增特例规则 - 达到特例规则的触发条件，触发报警
            修改集群鉴权失败的报警规则等级 - 达到触发条件，触发新等级的报警
            集群鉴权失败的报警新增特例规则 - 达到特例规则的触发条件，触发报警
        不同集群测试
            集群类型测试 - SMTX ELF、SMTX ZBS、SMTX OS（ELF、VMware ESXi）
            集群版本测试 - 6.2.x、5.6.x、5.1.x、6.3.x
        报警通知
            邮件/snmptrap/webhook - Tower 与集群连接异常的报警，可正常发送
            邮件/snmptrap/webhook - 集群鉴权失败的报警，可正常发送
        升级测试
            升级 Tower 至 470 及以上，升级 OBS 至 1.2.0 及以上 - 将 Tower 关联至 OBS，失联集群可触发报警
Tower UI 样式
    Tower 优化表格列展示和 toast 提示
        Toast 展示优化
            仅展示当前用户触发
                当前登录用户，触发任务 - Toast 正常展示
                非当前登录用户，触发任务 - 不展示 Toast 但任务列表正常记录任务状态
                system-service 触发的系统任务 - 不展示 Toast 但任务列表正常记录任务状态
                Toast 展示时长 - 3s 后自动消失
                虚拟机使用者 - 回归 Toast 仅展示当前用户触发
                用户管理员 - 回归 Toast 仅展示当前用户触发
                安全审计员 - 回归 Toast 仅展示当前用户触发
                只读用户 - 回归 Toast 仅展示当前用户触发
                工作负载集群使用者 - 回归 Toast 仅展示当前用户触发
                自定义角色的用户 - 回归 Toast 仅展示当前用户触发
                超级管理员/运维管理员 - 回归 Toast 仅展示当前用户触发
Tower 权限控制
    越权修复
        虚拟机使用者
            OAPI 回归
                OAPI 不支持查询 用户/系统事件
                OAPI 不支持查询 用户/角色管理列表
                OAPI 不支持查询 数据中心/集群/主机列表
                OAPI 不支持查询 内容库虚拟机模版/ ISO 映像列表
                OAPI 不支持查询 快照计划列表
                OAPI 不支持查询 任务列表
                OAPI 不支持查询 报警信息列表
        安全审计员
            OAPI 回归
                OAPI 支持查询 用户/系统事件
                OAPI 不支持查询 用户/角色管理列表
                OAPI 不支持查询 数据中心/集群/主机列表
                OAPI 不支持查询 内容库虚拟机模版/ ISO 映像列表
                OAPI 不支持查询 快照计划列表
                OAPI 不支持查询 任务列表
                OAPI 不支持查询 报警信息列表
        用户管理员
            集群
                Organization
                    query datacenters 获取数据中心信息
                    query clusters 获取集群信息
                    query hosts 获取主机信息
                    query vms 获取虚拟机信息
                    query iscsiTargets 获取 iscsiTarget 信息
                    query nvmfSubsystems 获取 nvmfSubsystem 信息
                    query disks 获取物理盘信息
                    query vmVolumes 获取虚拟卷信息
                    组织概览页正常展示
                    UI & OAPI 上均不支持 创建数据中心、关联集群
                Datacenter
                    数据中心概览页正常展示
                    UI & OAPI 上均不支持 修改数据中心、删除数据中心
                Cluster
                    query nics 获取网口信息
                    query usbDevices 获取 USB 设备信息
                    query gpuDevices 获取 GPU 设备信息
                    query pciDevices 获取 PCI 设备信息
                    query vmSnapshots 获取虚拟机快照信息
                    query vmPlacementGroups 获取虚拟机放置组信息
                    query getClusterTopologyInfo 获取集群网络拓扑信息
                    query vdses 获取虚拟分布式交换机信息
                    query vlans 获取虚拟机网络/系统网络信息
                    query graphs 获取集群监控分析信息
                    query logCollections 获取集群日志信息
                    query getClusterTopo 获取机架配置信息
                    集群概览页正常展示
                    集群设置可正常查看
                    UI & OAPI 上均不支持 创建空白虚拟机、创建虚拟卷
                    UI & OAPI 上均不支持 修改集群基本信息、移除集群
                Host
                    query hardwareHealthCheck 获取硬件运行状况
                    UI & OAPI 上均不支持 编辑主机名
            内容库
                虚拟机模版
                    query contentLibraryVmTemplates 获取虚拟机模版信息
                    虚拟机模版详情页正常展示
                    UI & OAPI 上均不支持 编辑基本信息、删除虚拟机模版
                ISO 映像
                    query contentLibraryImages 获取 ISO 信息
                    ISO 映像详情页正常展示
                    UI & OAPI 上均不支持 编辑 ISO 映像信息、删除 ISO
            报警
                报警信息
                    query alerts 获取 未解决/已解决 报警信息
                    query totalAlertCount 获取未解决报警数量
                报警规则
                    query globalAlertRules 获取内置报警规则信息
                    query customAlertRules 获取自定义报警规则信息
                    UI & OAPI 均不支持 更新内置报警规则
                通知配置
                    query alertNotifiers 获取邮件通知配置信息
                    query cloudTowerSnmpTrapReceivers 获取 SNMP 通知配置信息
                    query cloudTowerWebhookNotifiers 获取 webhook 通知配置信息
                    UI & OAPI 均不支持 编辑邮件通知配置
                通知策略
                    query alertSilencePolicies 获取静默通知策略信息
                    query alertGroupPolicies 获取聚合通知策略信息
            事件
                UI & OAPI 均不支持 查询用户事件
                UI & OAPI 均不支持 查询系统事件
            任务
                query taskTable 获取任务列表信息
            快照计划
                query snapshotPlans 获取快照计划信息
                UI & OAPI 均不支持 删除快照计划
            资源优化
                query entityFilters 获取预置规则/自定义规则信息
                query getManyDrsGroupsWithProposalInfo 获取已启用 DRS 集群信息
                UI & OAPI 均不支持 编辑自定义规则
            回收站
                query recycleVm 获取回收站虚拟机信息
                query getAllRecycleBinSettings 获取回收站规则信息
                UI & OAPI 均不支持 永久删除虚拟机
            报表
                query reportTemplates 获取报表模版信息
                query reportTasks 获取自动生成的报表信息
                UI & OAPI 均不支持 生成报表
            标签管理
                query labels 获取标签信息
                UI & OAPI 均不支持 创建标签
            系统配置
                软件许可
                    query deployedLicense 获取软件许可信息
                CloudTower 时间
                    query getCloudTowerTime 获取系统当前时间信息
                高级监控
                    query getClustersForDeploy 获取高级监控的集群信息
                SMTP 服务器
                    query smtpServers 获取 SMTP 服务器信息
                Syslog 服务器
                    query syslogs 获取 syslog 服务器信息
                SNMP 传输
                    query getCloudTowerSnmpTransportsInfo 获取 SNMP 传输信息
                用户管理
                    query users 获取用户列表信息
                    UI & OAPI 均支持 创建用户
                角色管理
                    query userRoleNexts 获取角色列表信息
                    UI & OAPI 均支持 创建角色
                LDAP/AD
                    query authnStrategies 获取 LDAP/AD 信息
                    UI & API 均不支持 测试 LDAP/AD 服务器连通性
                    query userRoleNexts 正常获取角色信息
                双因子认证
                    query mailMfaStrategies 获取邮件认证信息
                    query smsMfaStrategies 获取短信认证信息
                    query users 正常获取用户信息
                密钥管理服务
                    query allKmsClusters 获取 kms 集群信息
                虚拟机工具
                    query getSvtImages 获取虚拟机工具信息
            系统服务
                文件存储
                    query getCloudTowerApplicationPackagesList 获取 SFS 安装包信息
                    SFS 概览页正常展示
                Kubernetes 服务
                    query registryServices 获取 SKS 镜像仓库信息
                    SKS 概览页正常展示
                    设置弹窗正常展示
                网络与安全
                    query getEverouteInitialData 获取 ER 页面侧边栏 section 展示
                    query getV2EverouteLicenses 获取 ER 许可信息
                    query getEverouteClusters 获取 ER 服务信息
                    query getEveroutePackages 获取 ER 安装包信息
                    ER 概览页正常展示
                    VPC 概览页正常展示
                    设置弹窗正常展示
                网络流量可视化
                    query getTrafficVisualizationLicense 获取流量可视化许可信息
                备份与容灾
                    query getBackupLicense 获取备份与容灾许可信息
                    query getBackupServices 获取备份服务信息
                    query getReplicationServices 获取复制服务信息
                    Backup 概览页正常展示
                    设置弹窗正常展示
                巡检中心
                    query osAndZbsCluster 获取集群信息
                升级中心
                    query cloudTowerK8sApp 获取 k8s app 信息
                    升级中心概览页正常展示
                    设置弹窗正常展示
                CloudTower 代理
                    query clusterAndAgentMesh 获取代理信息
                    query getAgentMeshCloudTowerApplicationPackages 获取代理安装包信息
                可观测性
                    query bundleApplicationPackages 获取可观测安装包信息
                    设置弹窗正常展示
            个人设置
                mutation updateUser 修改姓名/电子邮箱/手机号码 成功
                mutation updateUser 修改用户密码成功，并通过新密码登录 Tower 成功
                mutation updateUser 启用安全密保问题成功，通过密码问题重置密码成功，使用新密码登录成功
                mutation updateUser 关闭安全密保问题成功，无法通过密码问题重置密码
                切换界面语言
        只读用户
            集群
                Organization
                    query datacenters 获取数据中心信息
                    query clusters 获取集群信息
                    query hosts 获取主机信息
                    query vms 获取虚拟机信息
                    query iscsiTargets 获取 iscsiTarget 信息
                    query nvmfSubsystems 获取 nvmfSubsystem 信息
                    query disks 获取物理盘信息
                    query vmVolumes 获取虚拟卷信息
                    组织概览页正常展示
                    UI & OAPI 上均不支持 创建数据中心、关联集群
                Datacenter
                    数据中心概览页正常展示
                    UI & OAPI 上均不支持 修改数据中心、删除数据中心
                Cluster
                    query nics 获取网口信息
                    query usbDevices 获取 USB 设备信息
                    query gpuDevices 获取 GPU 设备信息
                    query pciDevices 获取 PCI 设备信息
                    query vmSnapshots 获取虚拟机快照信息
                    query vmPlacementGroups 获取虚拟机放置组信息
                    query getClusterTopologyInfo 获取集群网络拓扑信息
                    query vdses 获取虚拟分布式交换机信息
                    query vlans 获取虚拟机网络/系统网络信息
                    query graphs 获取集群监控分析信息
                    query logCollections 获取集群日志信息
                    query getClusterTopo 获取机架配置信息
                    集群概览页正常展示
                    集群设置可正常查看
                    UI & OAPI 上均不支持 创建空白虚拟机、创建虚拟卷
                    UI & OAPI 上均不支持 修改集群基本信息、移除集群
                Host
                    query hardwareHealthCheck 获取硬件运行状况
                    UI & OAPI 上均不支持 编辑主机名
            内容库
                虚拟机模版
                    query contentLibraryVmTemplates 获取虚拟机模版信息
                    虚拟机模版详情页正常展示
                    UI & OAPI 上均不支持 编辑所属集群、删除虚拟机模版
                ISO 映像
                    query contentLibraryImages 获取 ISO 信息
                    ISO 映像详情页正常展示
                    UI & OAPI 上均不支持 编辑 ISO 映像信息、删除 ISO
            报警
                报警信息
                    query alerts 获取 未解决/已解决 报警信息
                    query totalAlertCount 获取未解决报警数量
                报警规则
                    query globalAlertRules 获取内置报警规则信息
                    query customAlertRules 获取自定义报警规则信息
                    UI & OAPI 均不支持 更新内置报警规则
                通知配置
                    query alertNotifiers 获取邮件通知配置信息
                    query cloudTowerSnmpTrapReceivers 获取 SNMP 通知配置信息
                    query cloudTowerWebhookNotifiers 获取 webhook 通知配置信息
                    UI & OAPI 均不支持 编辑邮件通知配置
                通知策略
                    query alertSilencePolicies 获取静默通知策略信息
                    query alertGroupPolicies 获取聚合通知策略信息
            事件
                UI & OAPI 均不支持 查询用户事件
                UI & OAPI 均不支持 查询系统事件
            任务
                query taskTable 获取任务列表信息
            快照计划
                query snapshotPlans 获取快照计划信息
                UI & OAPI 均不支持 删除快照计划
            资源优化
                query entityFilters 获取预置规则/自定义规则信息
                query getManyDrsGroupsWithProposalInfo 获取已启用 DRS 集群信息
                UI & OAPI 均不支持 编辑自定义规则
            回收站
                query recycleVm 获取回收站虚拟机信息
                query getAllRecycleBinSettings 获取回收站规则信息
                UI & OAPI 均不支持 永久删除虚拟机
            报表
                query reportTemplates 获取报表模版信息
                query reportTasks 获取自动生成的报表信息
                UI & OAPI 均不支持 生成报表
            标签管理
                query labels 获取标签信息
                UI & OAPI 均不支持 创建标签
            系统配置
                软件许可
                    query deployedLicense 获取软件许可信息
                CloudTower 时间
                    query getCloudTowerTime 获取系统当前时间信息
                高级监控
                    query getClustersForDeploy 获取高级监控的集群信息
                SMTP 服务器
                    query smtpServers 获取 SMTP 服务器信息
                Syslog 服务器
                    query syslogs 获取 syslog 服务器信息
                SNMP 传输
                    query getCloudTowerSnmpTransportsInfo 获取 SNMP 传输信息
                用户管理
                    UI & OAPI 均不支持 查询用户列表
                角色管理
                    UI & OAPI 均不支持 查询角色列表
                LDAP/AD
                    query authnStrategies 获取 LDAP/AD 信息
                    UI & API 均不支持 测试 LDAP/AD 服务器连通性
                    query userRoleNexts 报错无权限
                双因子认证
                    query mailMfaStrategies 获取邮件认证信息
                    query smsMfaStrategies 获取短信认证信息
                    query users 报错无权限
                密钥管理服务
                    query allKmsClusters 获取 kms 集群信息
                虚拟机工具
                    query getSvtImages 获取虚拟机工具信息
            系统服务
                文件存储
                    query getCloudTowerApplicationPackagesList 获取 SFS 安装包信息
                    SFS 概览页正常展示
                Kubernetes 服务
                    query registryServices 获取 SKS 镜像仓库信息
                    SKS 概览页正常展示
                    设置弹窗正常展示
                网络与安全
                    query getEverouteInitialData 获取 ER 页面侧边栏 section 展示
                    query getV2EverouteLicenses 获取 ER 许可信息
                    query getEverouteClusters 获取 ER 服务信息
                    query getEveroutePackages 获取 ER 安装包信息
                    ER 概览页正常展示
                    VPC 概览页正常展示
                    设置弹窗正常展示
                网络流量可视化
                    query getTrafficVisualizationLicense 获取流量可视化许可信息
                备份与容灾
                    query getBackupLicense 获取备份与容灾许可信息
                    query getBackupServices 获取备份服务信息
                    query getReplicationServices 获取复制服务信息
                    Backup 概览页正常展示
                    设置弹窗正常展示
                巡检中心
                    query osAndZbsCluster 获取集群信息
                升级中心
                    query cloudTowerK8sApp 获取 k8s app 信息
                    升级中心概览页正常展示
                    设置弹窗正常展示
                CloudTower 代理
                    query clusterAndAgentMesh 获取代理信息
                    query getAgentMeshCloudTowerApplicationPackages 获取代理安装包信息
                可观测性
                    query bundleApplicationPackages 获取可观测安装包信息
                    设置弹窗正常展示
            个人设置
                mutation updateUser 修改姓名/电子邮箱/手机号码 成功
                mutation updateUser 修改用户密码成功，并通过新密码登录 Tower 成功
                mutation updateUser 启用安全密保问题成功，通过密码问题重置密码成功，使用新密码登录成功
                mutation updateUser 关闭安全密保问题成功，无法通过密码问题重置密码
                切换界面语言
Tower 登录认证
    LDAP/AD/USP 集成
        LDAP/AD
            故障场景
                LDAP/AD 服务器失联 - 已登录的 LDAP 用户仍保持登录状态，但是登出后无法再次登录
            服务器数据兼容
                英文翻译 - 映射至 Tower 的用户存在重复的报错提示语
                basedn 内用户名重复
                    basedn 内，符合同步条件的数据，存在重复用户名 - 配置 LDAP 报错
                    basedn 内，符合同步条件的数据，存在重复用户名 - 编辑 LDAP 基本信息报错
                    basedn 内，修改符合同步条件的数据，使得用户名唯一 - 配置 LDAP 成功
                    basedn 内，符合同步条件的数据，存在重复用户名 - 编辑 LDAP 配置信息报错
                    basedn 内，符合同步条件的数据，存在重复用户名 - 编辑 LDAP 映射规则报错
                    basedn 内，符合同步条件的数据，存在重复用户名 - 符合同步条件的数据同步失败
                    basedn 内，不符合同步条件的数据，存在重复用户名 - 配置 LDAP 报错
                    basedn 内，修改不符合同步条件的数据，使得用户名唯一 - 配置 LDAP 成功
                    basedn 内，不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 基本信息报错
                    basedn 内，不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 配置信息报错
                    basedn 内，不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 映射规则报错
                    basedn 内，不符合同步条件的数据，存在重复用户名 - 符合同步条件的数据同步失败
                    basedn 内，符合同步条件与不符合同步条件的数据，存在重复用户名 - 配置 LDAP 报错
                    basedn 内，修改符合同步条件与不符合同步条件的数据，使得用户名唯一 - 配置 LDAP 成功
                    basedn 内，符合同步条件与不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 基本信息报错
                    basedn 内，符合同步条件与不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 配置信息报错
                    basedn 内，符合同步条件与不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 映射规则报错
                    basedn 内，符合同步条件与不符合同步条件的数据，存在重复用户名 - 符合同步条件的数据同步失败
                    basedn 内，符合同步条件的数据与已同步至 Tower 的用户，存在重复用户名 - 编辑 LDAP 基本信息报错
                    basedn 内，符合同步条件的数据与已同步至 Tower 的用户，存在重复用户名 - 编辑 LDAP 配置信息报错
                    basedn 内，符合同步条件的数据与已同步至 Tower 的用户，存在重复用户名 - 编辑 LDAP 映射规则报错
                    basedn 内，符合同步条件的数据与已同步至 Tower 的用户，存在重复用户名 - 符合同步条件的数据同步失败
                    已同步成功的重复用户名用户 - 登录 Tower 失败
                    已同步成功的用户，用户名唯一后 - 登录 Tower 成功
                    basedn 内，不符合同步条件的数据与已同步至 Tower 的用户，存在重复用户名 - 编辑 LDAP 基本信息报错
                    basedn 内，不符合同步条件的数据与已同步至 Tower 的用户，存在重复用户名 - 编辑 LDAP 配置信息报错
                    basedn 内，不符合同步条件的数据与已同步至 Tower 的用户，存在重复用户名 - 编辑 LDAP 映射规则报错
                    basedn 内，不符合同步条件的数据与已同步至 Tower 的用户，存在重复用户名 - 符合同步条件的数据同步失败
                    已同步成功的重复用户名用户 - 登录 Tower 失败
                    已同步成功的用户，用户名唯一后 - 登录 Tower 成功
                    编辑 LDAP 过滤条件，使得符合同步条件的数据，用户名唯一 - 编辑成功，用户同步成功
                    编辑 LDAP 用户名映射规则，使得符合同步条件的数据，用户名唯一 - 编辑成功，用户同步成功
                    编辑 LDAP 服务器数据属性，使得符合同步条件的数据，用户名唯一 - 编辑成功，用户同步成功
                basedn 内用户名唯一
                    basedn 内/外、符合/不符合同步条件的数据，用户名唯一 - 配置 LDAP 成功
                    basedn 内，符合/不符合同步条件的数据，已同步至 Tower 的用户，用户名唯一 - 编辑 LDAP 基本信息成功
                    basedn 内，符合/不符合同步条件的数据，已同步至 Tower 的用户，用户名唯一 - 编辑 LDAP 配置信息成功
                    basedn 内，符合/不符合同步条件的数据，已同步至 Tower 的用户，用户名唯一 - 编辑 LDAP 映射规则成功
                    basedn 内，符合/不符合同步条件的数据，已同步至 Tower 的用户，用户名唯一 - 符合同步条件的数据同步成功
                    同步成功的用户 - 可以成功登录 Tower
                basedn 外用户名重复
                    basedn 外，数据中存在重复用户名 - 配置 LDAP 成功
                    basedn 外，数据中存在重复用户名 - 编辑 LDAP 基本信息成功
                    basedn 外，数据中存在重复用户名 - 编辑 LDAP 配置信息成功
                    basedn 外，数据中存在重复用户名 - 编辑 LDAP 映射规则成功
                    basedn 外，数据中存在重复用户名 - 符合同步条件的数据同步成功
                    basedn 外，符合同步条件与不符合同步条件的数据，存在重复用户名 - 配置 LDAP 成功
                    basedn 外，符合同步条件与不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 基本信息成功
                    basedn 外，符合同步条件与不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 配置信息成功
                    basedn 外，符合同步条件与不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 映射规则成功
                    basedn 外，符合同步条件与不符合同步条件的数据，存在重复用户名 - 符合同步条件的数据同步成功
                    basedn 外，符合同步条件的数据与已同步至 Tower 的用户，存在重复用户名 - 配置 LDAP 成功
                    basedn 外，符合同步条件的数据与已同步至 Tower 的用户，存在重复用户名 - 编辑 LDAP 基本信息成功
                    basedn 外，符合同步条件的数据与已同步至 Tower 的用户，存在重复用户名 - 编辑 LDAP 配置信息成功
                    basedn 外，符合同步条件的数据与已同步至 Tower 的用户，存在重复用户名 - 编辑 LDAP 映射规则成功
                    basedn 外，符合同步条件的数据与已同步至 Tower 的用户，存在重复用户名 - 符合同步条件的数据同步成功
                    basedn 外，数据与已同步至 Tower 的用户，存在重复用户名 - 编辑 LDAP 基本信息成功
                    basedn 外，数据与已同步至 Tower 的用户，存在重复用户名 - 编辑 LDAP 配置信息成功
                    basedn 外，数据与已同步至 Tower 的用户，存在重复用户名 - 编辑 LDAP 映射规则成功
                    basedn 外，数据与已同步至 Tower 的用户，存在重复用户名 - 符合同步条件的数据同步成功
                    同步成功的用户 - 可以成功登录 Tower
                    basedn 外，不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 映射规则成功
                    basedn 外，不符合同步条件的数据，存在重复用户名 - 符合同步条件的数据同步成功
                basedn 内外用户名重复
                    basedn 外符合同步条件的数据与 basedn 内符合同步条件的数据，存在重复用户名 - 配置 LDAP 成功
                    basedn 外符合同步条件的数据与 basedn 内符合同步条件的数据，存在重复用户名 - 编辑 LDAP 基本信息成功
                    basedn 外符合同步条件的数据与 basedn 内符合同步条件的数据，存在重复用户名 - 编辑 LDAP 配置信息成功
                    basedn 外符合同步条件的数据与 basedn 内符合同步条件的数据，存在重复用户名 - 编辑 LDAP 映射规则成功
                    basedn 外符合同步条件的数据与 basedn 内符合同步条件的数据，存在重复用户名 - 符合同步条件的数据同步成功
                    basedn 外符合同步条件的数据与 basedn 内不符合同步条件的数据，存在重复用户名 - 配置 LDAP 成功
                    basedn 外符合同步条件的数据与 basedn 内不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 基本信息成功
                    basedn 外符合同步条件的数据与 basedn 内不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 配置信息成功
                    basedn 外符合同步条件的数据与 basedn 内不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 映射规则成功
                    basedn 外符合同步条件的数据与 basedn 内不符合同步条件的数据，存在重复用户名 - 符合同步条件的数据同步成功
                    basedn 外不符合同步条件的数据与 basedn 内符合同步条件的数据，存在重复用户名 - 配置 LDAP 成功
                    basedn 外不符合同步条件的数据与 basedn 内符合同步条件的数据，存在重复用户名 - 编辑 LDAP 基本信息成功
                    basedn 外不符合同步条件的数据与 basedn 内符合同步条件的数据，存在重复用户名 - 编辑 LDAP 配置信息成功
                    basedn 外不符合同步条件的数据与 basedn 内符合同步条件的数据，存在重复用户名 - 编辑 LDAP 映射规则成功
                    basedn 外不符合同步条件的数据与 basedn 内符合同步条件的数据，存在重复用户名 - 符合同步条件的数据同步成功
                    basedn 外不符合同步条件的数据与 basedn 内不符合同步条件的数据，存在重复用户名 - 配置 LDAP 成功
                    basedn 外不符合同步条件的数据与 basedn 内不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 基本信息成功
                    basedn 外不符合同步条件的数据与 basedn 内不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 配置信息成功
                    basedn 外不符合同步条件的数据与 basedn 内不符合同步条件的数据，存在重复用户名 - 编辑 LDAP 映射规则成功
                    basedn 外不符合同步条件的数据与 basedn 内不符合同步条件的数据，存在重复用户名 - 符合同步条件的数据同步成功
                    同步成功的用户 - 可以成功登录 Tower
                basedn 内外用户名唯一
                    basedn 内/外、符合/不符合同步条件的数据，用户名唯一 - 配置 LDAP 成功
                    basedn 内/外、符合/不符合同步条件的数据，已同步 Tower 的用户，用户名唯一 - 编辑 LDAP 基本信息成功
                    basedn 内/外、符合/不符合同步条件的数据，已同步 Tower 的用户，用户名唯一 - 编辑 LDAP 配置信息成功
                    basedn 内/外、符合/不符合同步条件的数据，已同步 Tower 的用户，用户名唯一 - 编辑 LDAP 映射规则成功
                    basedn 内/外、符合/不符合同步条件的数据，已同步 Tower 的用户，用户名唯一 - 符合同步条件的数据同步成功
                    同步成功的用户 - 可以成功登录 Tower
                姓名映射
                    数据的姓名映射字段不存在 - 配置/编辑 LDAP 仍然可以成功
                    数据的姓名映射字段不存在 - 数据可同步至 Tower，姓名复用用户名
                用户名映射
                    数据的姓名映射字段不存在 - 配置/编辑 LDAP 仍然可以成功
                    数据的姓名映射字段不存在 - 同步可以成功，但是无数据同步至 Tower
                手机号码映射
                    数据的手机号码映射字段不存在 - 配置/编辑 LDAP 仍然可以成功
                    数据的手机号码映射字段不存在 - 数据可同步至 Tower，手机号码展示空
                电子邮箱映射
                    数据的电子邮箱映射字段不存在 - 配置/编辑 LDAP 仍然可以成功
                    数据的电子邮箱映射字段不存在 - 数据可同步至 Tower，电子邮箱展示空
                update ldap attribute
                    修改用户名映射字段的值 - 已登录的 LDAP 用户仍保持登录状态，但是登出后需使用新用户名登录
                    修改用户名映射字段的值 - 同步服务器数据，已登录的 LDAP 用户强制登出
                    修改密码 - 已登录的 LDAP 用户仍保持登录状态，但是登出后需使用新密码登录
                    删除用户 - 已登录的 LDAP 用户仍保持登录状态，但是登出后无法再次登录
                    删除用户 - 同步服务器数据，已登录的 LDAP 用户强制登出
    密码安全
        密码重复限制
            UI 测试
                功能入口 - 系统配置 - 安全 - 密码安全，新增 密码重复限制 选项
                选项位置 - 在 密码复杂度 选项下面，密码有效时间 选项上面
                选项默认值 - 默认不开启
                选项下方提示语 - 启用后，用户更换密码时，新密码不可与最新 5 次密码更新的密码重复。
                英文界面下 - 正常翻译为英文
            密码重复策略
                用户修改的新密码，会与 最近使用过的 5 个密码进行校验，不允许重复
                低版本升级至当前版本 - 开始记录 最近使用过的 密码，最多 5 个
                当前版本更新 - 已记录的用户 最近使用过的 密码，不清空
                启用 密码重复限制 后关闭 - 已记录的用户 最近使用过的 密码，不清空
                启用 密码重复限制 后关闭 - 仍正常记录用户 最近使用过的 密码
            启用后关联功能测试
                用户修改密码 - 密码与过去规定个数内的密码，存在相同，修改失败
                用户修改密码 - 密码与过去规定个数内的密码，均不同，修改成功
                事件 - 用户事件
                    启用密码重复限制 - 触发一条 “编辑 CloudTower 访问限制” 的用户事件，详见步骤
                    关闭密码重复限制 - 触发一条 “编辑 CloudTower 访问限制” 的用户事件，详见步骤
                    英文界面下 - 用户事件正常翻译为英文
                个人设置 - 账号安全
                    用户修改个人密码 - 新密码与当前密码相同，点击 “保存” 时报错，修改失败
                    用户修改个人密码 - 新密码与最近第 2 个使用过的密码相同，点击 “保存” 时报错，修改失败
                    用户修改个人密码 - 新密码与最近第 5 个使用过的密码相同，点击 “保存” 时报错，修改失败
                    用户修改个人密码 - 新密码与最近第 6 个使用过的密码相同，保存并修改成功
                    修改密码成功 - 更新已记录的用户最近使用过的 5 个密码，当前密码为最新的 1 个
                    英文界面下 - 报错信息正常翻译为英文
                用户管理 - 编辑用户
                    修改其他用户密码 - 新密码与当前密码相同，点击 “保存” 时报错，修改失败
                    修改其他用户密码 - 新密码与最近第 3 个使用过的密码相同，点击 “保存” 时报错，修改失败
                    修改其他用户密码 - 新密码未使用过，保存并修改成功
                    用户修改个人密码 - 新密码与最近第 5 个使用过的密码相同，点击 “保存” 时报错，修改失败
                    用户修改个人密码 - 新密码未使用过，保存并修改成功
                    修改密码成功 - 更新已记录的用户最近使用过的 5 个密码，当前密码为最新的 1 个
                    英文界面下 - 报错信息正常翻译为英文
                登录页 - 忘记密码
                    用户修改个人密码 - 新密码与当前密码相同，点击 “保存” 时报错，修改失败
                    用户修改个人密码 - 新密码与最近第 4 个使用过的密码相同，点击 “保存” 时报错，修改失败
                    用户修改个人密码 - 新密码与最近第 5 个使用过的密码仅存在大小写差异，保存并修改成功
                    用户修改个人密码 - 新密码与最近第 6 个使用过的密码相同，点击 “保存” 成功，修改成功
                    修改密码成功 - 更新已记录的用户最近使用过的 5 个密码，当前密码为最新的 1 个
                    英文界面下 - 报错信息正常翻译为英文
                密码安全 - 密码过期
                    用户修改个人密码 - 新密码与当前密码相同，点击 “保存” 时报错，修改失败
                    用户修改个人密码 - 新密码与最近第 5 个使用过的密码相同，点击 “保存” 时报错，修改失败
                    用户修改个人密码 - 新密码与最近第 6 个使用过的密码相同，保存并修改成功
                    修改密码成功 - 更新已记录的用户最近使用过的 5 个密码，当前密码为最新的 1 个
                    英文界面下 - 报错信息正常翻译为英文
                API & OAPI 测试
                    通过 api 为用户修改密码 - 新密码与当前密码相同，报错，修改失败
                    通过 api 为用户修改密码 - 新密码与最近第 5 个使用过的密码相同，报错，修改失败
                    通过 api 为用户修改密码 - 新密码未使用过，修改成功
                    通过 oapi 为用户修改密码 - 新密码与最近第 3 个使用过的密码相同，报错，修改失败
                    通过 oapi 为用户修改密码 - 新密码与最近第 5 个使用过的密码仅存在大小写差异，修改成功
                    修改密码成功 - 更新已记录的用户最近使用过的 5 个密码，当前密码为最新的 1 个
                用户登录
                    修改密码失败 - 使用新密码登录失败，使用旧密码登录成功
                    修改密码成功 - 使用旧密码登录失败，使用新密码登录成功
            未启用关联功能回归
                用户修改密码 - 密码与过去规定个数内的密码，存在相同，修改成功
                用户修改密码 - 密码与过去规定个数内的密码，均不同，修改成功
                个人设置 - 账号安全
                    用户修改个人密码 - 新密码与当前密码相同，保存并修改成功
                    用户修改个人密码 - 新密码与最近第 5 个使用过的密码相同，保存并修改成功
                    修改密码成功 - 更新已记录的用户最近使用过的 5 个密码，当前密码为最新的 1 个
                用户管理 - 编辑用户
                    修改其他用户密码 - 新密码与当前密码相同，保存并修改成功
                    用户修改个人密码 - 新密码与最近第 4 个使用过的密码相同，保存并修改成功
                    修改密码成功 - 更新已记录的用户最近使用过的 5 个密码，当前密码为最新的 1 个
                登录页 - 忘记密码
                    用户修改个人密码 - 新密码与当前密码相同，保存并修改成功
                    用户修改个人密码 - 新密码未使用过，保存并修改成功
                    修改密码成功 - 更新已记录的用户最近使用过的 5 个密码，当前密码为最新的 1 个
                密码安全 - 密码过期
                    用户修改个人密码 - 新密码与当前密码相同，点击 “保存” 时报错，修改失败
                    用户修改个人密码 - 新密码与最近第 3 个使用过的密码相同，保存并修改成功
                    修改密码成功 - 更新已记录的用户最近使用过的 5 个密码，当前密码为最新的 1 个
                API & OAPI 测试
                    通过 api 为用户修改密码 - 新密码与当前密码相同，修改成功
                    通过 api 为用户修改密码 - 新密码与最近第 5 个使用过的密码相同，修改成功
                    通过 api 为用户修改密码 - 密码未使用过，修改成功
                    通过 oapi 为用户修改密码 - 新密码与当前密码相同，修改成功
                    修改密码成功 - 更新已记录的用户最近使用过的 5 个密码，当前密码为最新的 1 个
                用户登录
                    修改密码成功 - 使用新密码登录成功，使用旧密码登录失败
            权限测试
                已分配「运维管理和设置- CloudTower 级别-密码安全」权限的用户 - 可操作密码重复限制
                未分配「运维管理和设置- CloudTower 级别-密码安全」权限的用户 - 密码重复限制选项置灰
            升级测试
                低版本升级至当前版本 - 新增 密码重复限制 功能
            用户类型测试
                本地用户 - 支持修改密码，存在密码重复限制
                LDAP/AD 用户 - 不支持修改密码，不存在密码重复限制
                SSO 用户 - 不支持修改密码，不存在密码重复限制
            特殊场景测试
                用户 A 和 B 分别修改用户 C 的密码 - 两个密码均会被记录
                用户 A、B、C 同时修改用户 C 的密码为 “xxxx” - 其中一个用户修改成功，两个修改失败
                用户 A 分别用 Safari/Chrome/Firefox/Microsoft Edge 修改用户 C 的密码 - 四个密码均会被记录
                用户超时自动登出 - 重新登录，密码不会被记录
                CloudTower 过期后 - 用户修改密码成功，密码被记录，用户可通过新密码登录成功
                CloudTower 过期后 - 已启用密码重复限制，该限制仍正常生效