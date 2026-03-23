5.1.5
    回归测试
        network-tool
            网口连通性检测
                未设置bond时，执行检测命令
                ovs-ab
                    执行network-tool check-ovs-bond-nics --bond_mode “active-backup”检测OVS-AB模式下主备端口连通性----返回联通正常
                    执行network-tool check-ovs-bond-nics --bond_mode “active-backup”检测OVS-AB模式下主备端口连通性----返回联通存在故障
                    网卡状态为Down时，执行network-tool check-ovs-bond-nics --bond_mode “active-backup”
                balanc-slb
                    执行network-tool check-ovs-bond-nics --bond_mode “balance-sl”检测OVS-AB模式下主备端口连通性----返回联通正常
                    执行network-tool check-ovs-bond-nics --bond_mode “balance-slb”检测OVS-AB模式下主备端口连通性----返回联通存在故障
                    网卡状态为Down时，执行network-tool check-ovs-bond-nics --bond_mode “balance-slb"
            网口切换
                不开启RDMA
                    ovs-active-backup模式先增加后减少网口
                    ovs-balance-ab转单网口模式
                    单网口转多网口并选择ovs-active-backup模式
                    ovs-active-backup转ovs-balance-tcp模式
                    ovs-active-backup转ovs-balance-slb模式
                    ovs-balance-slb模式先增加后减少网口
                    ovs-balance-slb转单网口模式
                    单网口转多网口并选择ovs-balance-slb模式
                    ovs-balance-slb转ovs-active-backup模式
                    ovs-balance-slb转ovs-balance-tcp模式
                    ovs-balance-tcp转单网口模式
                    单网口转多网口并选择ovs-balance-tcp模式
                    ovs-balance-tcp转ovs-active-backup模式
                    ovs-balance-tcp转ovs-balance-slb模式
                开启RDMA
                    ovs-bond+rdma
                        504及以前集群升级，ovs-ab转Linux-ab
                        ovs-balance-tcp转Linux-802.3ad
                        ovs-balance-slb转Linux-ab
                    Linux-bond+rdma
                        Linux-ab转Linux-xor
                        Linux-ab转Linux-802.3ad
                        Linux-ab转单网口
                        Linux-xor转Linux-ab
                        Linux-xor转Linux-802.3ad
                        Linux-xor转单网口
                        Linux-802.3ad转Linux-ab
                        Linux-802.3ad转Linux-xor
                        Linux-802.3ad转单网口
                        单网口转换为Linux-ab
                        单网口转换为Linux-xor
                        单网口转换为Linux-802.3ad
        network-preconfig（待定，等待tui）
            network-preconfig 创建Linux 802.3ad bond端口组
            network-preconfig 创建vlan子接口绑定到Linux 802.3ad bond端口组并配置IP地址
            network-preconfig 清理 802.3ad 配置
            使用子接口的IP地址进行安装部署流程可成功部署集群
            集群部署完成后network-preconfig产生的接口及配置文件预期可以被自动清除
    加固测试
        mtu
            网口
                1500 -> 9000，检查配置
                9000 -> 1500，检查配置
            管理网络
                1500-> 9000，同时提升网口mtu，检查网口配置，8000包可发送
                9000 -> 1500，检查网口配置，8000包不可发送
                1500-> 9000，无需同时提升网口mtu，检查网口配置，8000包可发送
            存储网络
                1500-> 9000，同时提升网口mtu，检查网口配置，8000包可发送
                9000 -> 1500，检查网口配置，8000包不可发送
                1500-> 9000，无需同时提升网口mtu，检查网口配置，8000包可发送
        vip
            vip-mgt
                vip 所在节点
                    ifdown，ifup 存储网，vip转移到其他节点，所有节点与vip通信正常
                    ifdown 存储网，vip转移到其他节点，其他节点与vip通信正常 ，半小时后，ifup，所有节点与vip通信正常
                    systemctl restart zookeeper，vip不转移，所有节点与vip通信正常
                    stop zookeeper，vip不转移，所有节点与vip通信正常，半小时后start，vip不转移，所有节点与vip通信正常
                    restart vip-service，vip转移到其他节点，所有节点与vip通信正常
                    vip-service运行半小时后，stop，vip转移到其他节点，其他节点与vip通信正常 ，半小时后，start，所有节点与vip通信正常
                非 vip 所在节点
                    ifdown，ifup 存储网，vip不转移，所有节点与vip通信正常
                    ifdown 存储网，vip不转移，其他节点与vip通信正常 ，半小时后，ifup存储网络，所有节点与vip通信正常
                    systemctl restart zookeeper，vip不转移，所有节点与vip通信正常
                    stop zookeeper，vip不转移，所有节点与vip通信正常，半小时后start，vip不转移，所有节点与vip通信正常
                    restart vip-service，vip 不转移，所有节点与vip通信正常
                    vip-service运行半小时后，stop，vip 不转移，其他节点与vip通信正常 ，半小时后，start，所有节点与vip通信正常
                集群
                    ifdown，ifup 存储网，所有节点与vip通信正常
                    ifdown 存储网，ifup，所有节点与vip通信正常
                    systemctl restart zookeeper，所有节点与vip通信正常
                    stop zookeeper，半小时后start，所有节点与vip通信正常
                    restart vip-service，所有节点与vip通信正常
                    vip-service运行半小时后 stop，半小时后，start，所有节点与vip通信正常
            vip-access
                vip 所在节点
                    ifdown，ifup 存储网，vip转移到其他节点，所有节点与vip通信正常
                    ifdown 存储网，vip转移到其他节点，其他节点与vip通信正常 ，半小时后，ifup，所有节点与vip通信正常
                    systemctl restart zookeeper，vip不转移，所有节点与vip通信正常
                    stop zookeeper，vip不转移，所有节点与vip通信正常，半小时后start，vip不转移，所有节点与vip通信正常
                    restart vip-service，vip转移到其他节点，所有节点与vip通信正常
                    vip-service运行半小时后，stop，vip转移到其他节点，其他节点与vip通信正常 ，半小时后，start，所有节点与vip通信正常
                非 vip 所在节点
                    ifdown，ifup 存储网，vip不转移，所有节点与vip通信正常
                    ifdown 存储网，vip不转移，其他节点与vip通信正常 ，半小时后，ifup存储网络，所有节点与vip通信正常
                    systemctl restart zookeeper，vip不转移，所有节点与vip通信正常
                    stop zookeeper，vip不转移，所有节点与vip通信正常，半小时后start，vip不转移，所有节点与vip通信正常
                    restart vip-service，vip 不转移，所有节点与vip通信正常
                    vip-service运行半小时后，stop，vip 不转移，其他节点与vip通信正常 ，半小时后，start，所有节点与vip通信正常
                集群
                    ifdown，ifup 存储网，所有节点与vip通信正常
                    ifdown 存储网，半小时后，ifup，所有节点与vip通信正常
                    systemctl restart zookeeper，所有节点与vip通信正常
                    stop zookeeper，半小时后start，所有节点与vip通信正常
                    restart vip-service，所有节点与vip通信正常
                    vip-service运行半小时后，stop ，半小时后，start，所有节点与vip通信正常
    网络中断时间测试
        vds
            增删网口
                ovs-bond
                    active-backup
                        1->2
                        2->3
                        3->2
                        2->1
                    balance-slb
                        1->2
                        2->3
                        3->2
                        2->1
                    balance-tcp
                        1->2
                        2->1
                linux-bond
                    active-backup
                        1->2
                        2->1
                    balance-xor
                        1->2
                        2->1
                    802.3ad
                        1->2
                        2->1