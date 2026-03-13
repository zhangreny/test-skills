vendor 添加字段 - Observability
    无 vendor 许可
        obs121 未开启流量可视化，升级后导入新的含vendor的1.4流量可视化许可，成功
        obs121 已开启流量可视化，升级后导入新的含vendor的1.4流量可视化许可，成功
        obs131 已开启流量可视化，升级后导入新的含vendor的1.4流量可视化许可，成功
        obs131 无集群开启开启流量可视化，升级后导入新的含vendor的1.4流量可视化许可，成功
        arcfra obs 140许可无法导入
    前后均为vendor许可的更新
        导入新的含vendor的1.4流量可视化许可，成功
        arcfra obs 无法导入
er340 + tower470 LB 支持物理 CPU 许可
    Tower 场景及功能
        LB 许可卡片显示
            试用许可 - 插槽 [LB - 试用 - 15days - socket - 12]
                已经过期，VPC未过期，会提前VPC许可
                即将过期
                额度未完全使用，显示已有和可用
                额度完全使用
                hover 已用，检查 tooltip 描述和数值
            订阅许可 - 插槽 [LB - 订阅 - 15days - socket - 12]
                已经过期，VPC未过期，会提前VPC许可
                即将过期
                额度未完全使用，显示已有和可用
                额度完全使用
                hover 已用，检查 tooltip 描述和数值
            永久许可 - 插槽 [LB - 永久 - socket - 12]
                额度未完全使用，显示已有和可用
                额度完全使用
                hover 已用，检查 tooltip 描述和数值
        集群扩容场景 [集群节点和额外节点注意打快照]
            DFW vm 许可，LB 插槽许可 [DFW - 订阅 - 30days - vm - 2]
                LBI 集群被 DFW 关联，LB 许可数量正好可以满足扩容，不报错 [LB - 订阅 - 30days - socket - 8]
                LB 许可满足一个主机的扩容但不满足两个主机的扩容，两个报错，一个不报错 [LB - 订阅 - 30days - socket - 8]
                LB 许可使用未满，但是数量不足以满足扩容，报错 [LB - 试用 - 30days - socket - 7]
                LB 许可使用已满，但扩容主机上没有LBI，不报错 [最后测试，LB - 订阅 - 30days - socket - 8]
                DFW vm 许可已满，扩容被 DFW 关联的集群不报错 [DFW - 订阅 - 30days - vm - 2]
                报错信息只包含 LB
            DFW CPU 许可，LB vCPU 许可 [LB - 订阅 - 30days - vCPU - 4]
                扩容LBI所在集群，DFW CPU 许可数量正好可以满足扩容，不报错 [DFW - 订阅 - 30days - socket - 8]
                DFW 许可满足一个主机的扩容但不满足两个主机的扩容，两个报错，一个不报错 [DFW - 订阅 - 30days - socket - 8]
                DFW 许可使用未满，但是数量不足以满足扩容，报错 [DFW - 订阅 - 30days - socket - 7]
                DFW 许可使用已满，但扩容集群未被DFW关联，不报错 [最后测试，DFW - 订阅 - 30days - socket - 8]
                LB vcpu 许可已满，扩容被 DFW 关联的 LBI 集群不报错
                报错信息只包含 DFW
            DFW CPU 许可，LB 插槽许可
                DFW CPU 刚好满足，LB CPU 刚好满足，不报错 [DFW - 订阅 - 30days - socket - 8][LB - 订阅 - 30days - socket - 8]
                DFW CPU 刚好满足，LB CPU 不足，报错只包含 LB [DFW - 订阅 - 30days - socket - 8][LB - 试用 - 30days - socket - 7]
                DFW CPU 不足，LB CPU 刚好满足，报错只包含 DFW [DFW - 订阅 - 30days - socket - 7][LB - 订阅 - 30days - socket - 8]
                DFW CPU 不足，LB CPU 不足，不报错 [DFW - 订阅 - 30days - socket - 7][LB - 试用 - 30days - socket - 7]
                DFW CPU 不足，LB 满足，但扩容的 LBI 集群未被 DFW 关联，不报错 [DFW - 订阅 - 30days - socket - 7][LB - 订阅 - 30days - socket - 8]
                DFW CPU 充足，LB 不足，但扩容的集群被 DFW 关联耽误 LBI，不报错 [DFW - 订阅 - 30days - socket - 8][LB - 试用 - 30days - socket - 7]
        部署和启用 LB 的许可弹窗
            部署 ER
                vCPU [LB - 订阅 - 30days - vCPU - 4]
                    LB vCPU 不满足创建四个 lbvm，报错。创建两个，提交成功。
                    LB vCPU 不足时 部署开启 lb 的 er340，报错。[已使用 4/4]
                    LB vCPU 充足时 部署开启 lb 的 er340，不报错，部署成功，检查许可使用。
                    LB vcpu 不足时 部署开启 lb 的 er204，报错。[已使用 4/4]
                    LB vCPU 充足时 部署开启 lb 的 er204，不报错，部署成功，检查许可使用。
                插槽 [LB - 试用 - 30days - socket - 7][LB - 订阅 - 15days - socket - 12]
                    LB 插槽 不满足在新的四节点集群上部署，报错。三节点不报错，提交成功。
                    LB 插槽 不足时 在新集群上 部署开启 lb 的 er340，报错 [已使用 6/7]
                    LB 插槽 不足时 在旧集群上 部署开启 lb 的 er340，成功，检查许可使用。[已使用 6/7]
                    LB 插槽 不足时 在新集群上 部署开启 lb 的 er204，报错。[已使用 6/7]
                    LB 插槽 不足时 在旧集群上 部署开启 lb 的 er204，成功，检查许可使用。[已使用 6/7]
                    LB 插槽 充足时 在新集群上 部署开启 lb 的 er340，成功，检查许可使用。[已使用 0/12]
                    LB 插槽 充足时 在旧集群上 部署开启 lb 的 er340，成功，检查许可使用。[已使用 6/12]
                    LB 插槽 充足时 在新集群上 部署开启 lb 的 er204，成功，检查许可使用。[已使用 0/12]
                    LB 插槽 充足时 在旧集群上 部署开启 lb 的 er340，成功，检查许可使用。[已使用 6/12]
            启用 ER
                vCPU [LB - 订阅 - 30days - vCPU - 4]
                    LB vCPU 不满足创建四个 lbvm，报错。创建两个，提交成功。
                    LB vCPU 不足时 er340 启用 LB，报错。 [已使用 4/4]
                    LB vCPU 充足时 er340 启用 LB，不报错，部署成功，检查许可使用。
                    LB vcpu 不足时 er204 启用 LB，报错。 [已使用 4/4]
                    LB vCPU 充足时 er204 启用 LB，不报错，部署成功，检查许可使用。
                插槽 [LB - 试用 - 30days - socket - 7][LB - 订阅 - 15days - socket - 12]
                    LB 插槽 不满足在新的四节点集群上部署，报错。三节点不报错，提交成功。
                    LB 插槽 不足时 在新集群上 er340 启用 LB，报错。[已使用 6/7]
                    LB 插槽 不足时 在旧集群上 er340 启用 LB，成功，检查许可使用。[已使用 6/7]
                    LB 插槽 不足时 在新集群上 er204 启用 LB，报错。[已使用 6/7]
                    LB 插槽 不足时 在旧集群上 er204 启用 LB，成功，检查许可使用。[已使用 6/7]
                    LB 插槽 充足时 在新集群上 er340 启用 LB，成功，检查许可使用。[已使用 0/12]
                    LB 插槽 充足时 在旧集群上 er340 启用 LB，成功，检查许可使用。[已使用 6/12]
                    LB 插槽 充足时 在新集群上 er204 启用 LB，成功，检查许可使用。[已使用 0/12]
                    LB 插槽 充足时 在旧集群上 er340 启用 LB，成功，检查许可使用。[已使用 6/12]
            创建 LBI（只有 er340 支持）
                vCPU
                    LB vCPU 不满足创建四个 lbvm，报错。但满足创建两个 lbvm，提交成功。[LB - 永久 - vCPU - 8][已使用 4/8]
                    LB vCPU 不足时 er340 创建 LBI，报错。[LB - 订阅 - 30days - vCPU - 4][已使用 4/4]
                    LB vCPU 充足时 er340 创建 LBI，不报错，创建成功，检查许可使用。[LB - 永久 - vCPU - 8][已使用 4/8]
                插槽 [LB - 试用 - 30days - socket - 7][LB - 订阅 - 15days - socket - 12]
                    LB 插槽 不满足在新的四节点集群上部署，报错。三节点不报错，提交成功，检查许可使用。[已使用 6/12]
                    LB 插槽 不足时 在新集群上 er340 创建 LBI，报错。[已使用 6/7]
                    LB 插槽 不足时 在旧集群上 er340 创建 LBI，成功，检查许可使用。[已使用 6/7]
                    LB 插槽 充足时 在新集群上 er340 创建 LBI，成功，检查许可使用。[已使用 6/12]
                    LB 插槽 充足时 在旧集群上 er340 创建 LBI，成功，检查许可使用。[已使用 6/12]
        DFW 和 VPC 许可不足文案调整
            DFW CPU 插槽 关联集群时 文案调整 [分布式防火墙的可用额度为] [DFW - 订阅 - 30days - socket - 7]
            VPC 为扩容后集群编辑 tepip 时许可不足文案调整 [虚拟专有云网络的可用额度为] [VPC - 订阅 - 30days - socket - 7]
            VPC 新关联集群时许可不足文案调整 [虚拟专有云网络的可用额度为] [VPC - 订阅 - 30days - socket - 7]
    其他功能验证
        许可归还
            集群缩容
                插槽
                    tower 缩容，比如 os620，许可归还
                    命令行缩容，归还许可
                vCPU
                    tower 缩容，比如 os620，不许可归还
                    命令行缩容，不归还许可
            删除 LBI（er340 支持）
                插槽
                    本 ER340 无其他 LBI，其余 ER 在该集群上也无 LBI，许可归还
                    本 ER340 有其他 LBI，其余 ER 在该集群上无 LBI，不归还许可
                    本 ER340 无其他 LBI，其余 ER340 在该集群上有 LBI，不归还许可
                    本 ER340 无其他 LBI，其余 ER204 在该集群上有开启 LB 的 Everoute，不归还许可
                vCPU
                    删除后检查许可使用，直接归还对应数量vCPU
            Everoute 关闭 LB（er340 卸载负载均衡功能前提：没有任何 LBI 或 LBG）
                插槽 - er310
                    其余 ER 在该集群上也无 LBI，许可归还
                    其余 ER340 在该集群上有 LBI，不归还许可
                    其余 ER204 在该集群上有开启 LB 的 Everoute，不归还许可
                vCPU - er310
                    关闭后立刻归还对应数量vCPU
            卸载开启 LB 的 Everoute（er340 卸载 er 前提：没有任何 LBI 或 LBG）
                插槽 - er310
                    其余 ER 在该集群上也无 LBI，许可归还
                    其余 ER340 在该集群上有 LBI，不归还许可
                    其余 ER204 在该集群上有开启 LB 的 Everoute，不归还许可
                vCPU - er310
                    关闭后立刻归还对应数量vCPU
        许可更新
            tower 470 首次部署 LB 为 vCPU 许可，试用 90 天
            支持 CPU 插槽的 LB 许可无法导入 <= 470 的 Tower，检查错误信息
            支持 CPU 插槽的 LB 许可额度不满足当前 LBI 所在所有集群的额度，无法导入，检查错误信息 [LB - 试用 - 30days - socket - 7][已使用 12/7]
            支持 CPU 插槽的 LB 许可额度刚刚好满足当前 LBI 所在所有集群的额度，导入成功，再创建无关集群的 lBI 报错 [LB - 订阅 - 15days - socket - 12][已使用 12/12]
            支持 vCPU 的 LB 许可刚刚好满足额度，导入成功，创建任何 LBI 报错 [LB - 永久 - vCPU - 8][已使用 8/8]
            许可过期时间早于当前时间，则不允许更新，检查错误信息 [LB - 订阅 - 1days - socket - 12]
            vcpu 更新
                vCPU 试用 -> CPU 插槽 试用，检查使用情况
                vCPU 试用 -> CPU 插槽 订阅，检查使用情况
                vCPU 试用 -> CPU 插槽 永久，检查使用情况
                vCPU 订阅 -> CPU 插槽 试用，检查使用情况
                vCPU 订阅 -> CPU 插槽 订阅，检查使用情况
                vCPU 订阅 -> CPU 插槽 永久，检查使用情况
                vCPU 永久 -> CPU 插槽 试用，检查使用情况
                vCPU 永久 -> CPU 插槽 订阅，检查使用情况
                vCPU 永久 -> CPU 插槽 永久，检查使用情况
            cpu 插槽更新
                CPU 插槽 试用 -> vCPU 试用，检查使用情况
                CPU 插槽 试用 -> vCPU 订阅，检查使用情况
                CPU 插槽 试用 -> vCPU 永久，检查使用情况
                CPU 插槽 订阅 -> vCPU 试用，检查使用情况
                CPU 插槽 订阅 -> vCPU 订阅，检查使用情况
                CPU 插槽 订阅 -> vCPU 永久，检查使用情况
                CPU 插槽 永久 -> vCPU 试用，检查使用情况
                CPU 插槽 永久 -> vCPU 订阅，检查使用情况
                CPU 插槽 永久 -> vCPU 永久，检查使用情况
            cpu 插槽更新
                CPU 插槽 试用 -> CPU 插槽 试用，检查使用情况
                CPU 插槽 试用 -> CPU 插槽 订阅，检查使用情况
                CPU 插槽 试用 -> CPU 插槽 永久，检查使用情况
                CPU 插槽 订阅 -> CPU 插槽 试用，检查使用情况
                CPU 插槽 订阅 -> CPU 插槽 订阅，检查使用情况
                CPU 插槽 订阅 -> CPU 插槽 永久，检查使用情况
                CPU 插槽 永久 -> CPU 插槽 试用，检查使用情况
                CPU 插槽 永久 -> CPU 插槽 订阅，检查使用情况
                CPU 插槽 永久 -> CPU 插槽 永久，检查使用情况
        LBG 相关场景回归
            同集群两 LBI 创建 LBG，许可不变
            跨集群两 LBI 创建 LBG，许可不变
            删除同集群 LBG，LBI 不删除，许可不变
            删除跨集群 LBG，LBI 不删除，许可不变
        多 Controller 场景回归
            多 ER controller 场景下，部署时将 LBI 部署于新集群，检查许可增加
            多 ER controller 场景下，新建 LBI 于新集群，检查许可增加
            多 ER controller 场景下，新建 LBI 于旧集群，检查许可不变
            多 ER controller 场景下，删除 LBI 于有其他 LBI 集群，检查许可不变
            多 ER controller 场景下，删除 LBI 于无其他 LBI 集群，检查许可减少
            无任何 LBI，卸载 ER，许可不变
    升级场景（尽量去贴用户使用，tower 需要对应额外申请许可）
        tower345 + er204 订阅许可，升级至 tower470 + er340 成功后预期只保留 DFW 许可，LB 为试用许可
            er340 继续创建 LBI 成功，查看试用许可使用
            创建新 ER 开启 LB 成功，查看试用许可使用
            更新 LB 订阅许可为 CPU插槽，er340 同集群继续创建 LBI 成功，订阅许可不涨
            更新 LB 订阅许可为 CPU插槽，er340 不同集群创建 LBI 成功，订阅许可涨
            更新 LB 订阅许可为 CPU插槽，er340 删除集群上非唯一 LBI 成功，订阅许可不退还
            更新 LB 订阅许可为 CPU插槽，er340 删除集群上唯一 LBI 成功，订阅许可退还
            许可数量允许下扩容 LBI 所在集群，订阅许可涨
            缩容 LBI 所在集群，许可退还
            更新 LB 永久许可为 CPU插槽，er340 同集群继续创建 LBI 成功，订阅许可不涨
            更新 LB 永久许可为 CPU插槽，er340 不同集群创建 LBI 成功，订阅许可涨
            更新 LB 永久许可为 CPU插槽，er340 删除集群上非唯一 LBI 成功，订阅许可不退还
            更新 LB 永久许可为 CPU插槽，er340 删除集群上唯一 LBI 成功，订阅许可退还
            许可数量允许下扩容 LBI 所在集群，永久许可涨
            缩容 LBI 所在集群，许可退还
        tower345 + er204 试用许可 （只覆盖基础功能）
            更新 LB 订阅许可为 CPU插槽，er340 同集群继续创建 LBI 成功，订阅许可不涨
            更新 LB 订阅许可为 CPU插槽，er340 不同集群创建 LBI 成功，订阅许可涨
            更新 LB 订阅许可为 CPU插槽，er340 删除集群上非唯一 LBI 成功，订阅许可不退还
            更新 LB 订阅许可为 CPU插槽，er340 删除集群上唯一 LBI 成功，订阅许可退还
        tower345 + er204 永久许可 （只覆盖基础功能）
            更新 LB 永久许可为 CPU插槽，er340 同集群继续创建 LBI 成功，订阅许可不涨
            更新 LB 永久许可为 CPU插槽，er340 不同集群创建 LBI 成功，订阅许可涨
            更新 LB 永久许可为 CPU插槽，er340 删除集群上非唯一 LBI 成功，订阅许可不退还
            更新 LB 永久许可为 CPU插槽，er340 删除集群上唯一 LBI 成功，订阅许可退还
        tower 460 + er331 订阅许可，升级至 tower470 + er340 成功后
            er340 继续创建 LBI 成功，查看 vCPU 使用
            创建新 ER 开启 LB 成功，查看 vCPU 使用
            更新 LB 订阅许可为 CPU插槽，er340 同集群继续创建 LBI 成功，订阅许可不涨
            更新 LB 订阅许可为 CPU插槽，er340 不同集群创建 LBI 成功，订阅许可涨
            更新 LB 订阅许可为 CPU插槽，er340 删除集群上非唯一 LBI 成功，订阅许可不退还
            更新 LB 订阅许可为 CPU插槽，er340 删除集群上唯一 LBI 成功，订阅许可退还
            许可数量允许下扩容 LBI 所在集群，订阅许可涨
            缩容 LBI 所在集群，订阅许可退还
            更新 LB 永久许可为 CPU插槽，er340 同集群继续创建 LBI 成功，订阅许可不涨
            更新 LB 永久许可为 CPU插槽，er340 不同集群创建 LBI 成功，订阅许可涨
            更新 LB 永久许可为 CPU插槽，er340 删除集群上非唯一 LBI 成功，订阅许可不退还
            更新 LB 永久许可为 CPU插槽，er340 删除集群上唯一 LBI 成功，订阅许可退还
            许可数量允许下扩容 LBI 所在集群，永久许可涨
            缩容 LBI 所在集群，许可退还
    异常场景
        Tower 470 上关联了集群 A 上有 LBI，在其他 tower 内把 LBIvm 迁移到了不被 Tower 470 关联的集群 B，检查是否能绕过许可的点数使用。
    许可过期
        只支持删除 vs，无法创建和编辑
        只支持删除 lbi lbg，无法创建和编辑
        只支持卸载 lb 功能，无法开启 lb 功能
        不支持任何操作 hc
        不支持任何操作 rs
        不支持编辑任何网络关联