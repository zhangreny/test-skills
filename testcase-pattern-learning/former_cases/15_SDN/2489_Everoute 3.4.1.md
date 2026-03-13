ER-1495 安全策略测试
    [放行-标签] A(any) B(any) - Delete A
    [放行-标签] A(any) B(0.0.0.0/0) - Delete B
    [放行-标签] A(0.0.0.0/0) B(any) - Delete B
    [放行-标签] A(0.0.0.0/0) B(0.0.0.0/0) - Delete A
    [放行-标签] A(any->specific) B(any) - Modify A
    [放行-标签] A(0.0.0.0/0->specific) B(0.0.0.0/0) - Modify A
    [放行-安全组] A(any) B(any) - Delete A
    [放行-安全组] A(any) B(0.0.0.0/0) - Delete B
    [放行-安全组] A(0.0.0.0/0) B(any) - Delete B
    [放行-安全组] A(0.0.0.0/0) B(0.0.0.0/0) - Delete A
    [放行-安全组] A(any->specific) B(any) - Modify A
    [放行-安全组] A(0.0.0.0/0->specific) B(0.0.0.0/0) - Modify A
    [放行-IP组] A(any) B(any) - Delete A
    [放行-IP组] A(any) B(0.0.0.0/0) - Delete B
    [放行-IP组] A(0.0.0.0/0) B(any) - Delete B
    [放行-IP组] A(0.0.0.0/0) B(0.0.0.0/0) - Delete A
    [放行-IP组] A(any->specific) B(any) - Modify A
    [放行-IP组] A(0.0.0.0/0->specific) B(0.0.0.0/0) - Modify A
    [拒绝-标签] A(0.0.0.0/0) B(0.0.0.0/0) - Delete A
    [拒绝-标签] A(0.0.0.0/0->specific) B(0.0.0.0/0) - Modify A
    [拒绝-IP组] A(0.0.0.0/0) B(0.0.0.0/0) - Delete A
    [拒绝-IP组] A(0.0.0.0/0->specific) B(0.0.0.0/0) - Modify A
    [拒绝-安全组] A(0.0.0.0/0) B(0.0.0.0/0) - Delete A
    [拒绝-安全组] A(0.0.0.0/0->specific) B(0.0.0.0/0) - Modify A
    [放行-IP组] 重启OVS - A(0/0) B(0/0)
    [放行-标签组] 重启OVS - A(any) B(any)
    [放行-安全组] 重启OVS - A(any) B(specific)
    [拒绝-安全组] 重启OVS - A(0/0) B(0/0)
    [拒绝-IP组] 重启OVS - A(0.0.0.0/0) B(specific)
ER-1499 流量可视化测试
    源端发起-新建连接 (ARP Stale/转发表老化/开启可视化)
    源端发起-新建连接 (ARP Stale/转发表老化/关闭可视化)
    源端发起-新建连接 (ARP Stale/转发表正常/开启可视化)
    源端发起-新建连接 (ARP Stale/转发表正常/关闭可视化)
    源端发起-新建连接 (ARP可达/转发表老化/开启可视化)
    源端发起-新建连接 (ARP可达/转发表老化/关闭可视化)
    源端发起-新建连接 (ARP可达/转发表正常/开启可视化)
    源端发起-新建连接 (ARP可达/转发表正常/关闭可视化)
    源端发起-已建立连接 (ARP Stale/转发表老化/开启可视化)
    源端发起-已建立连接 (ARP Stale/转发表老化/关闭可视化)
    源端发起-已建立连接 (ARP Stale/转发表正常/开启可视化)
    源端发起-已建立连接 (ARP Stale/转发表正常/关闭可视化)
    源端发起-已建立连接 (ARP可达/转发表老化/开启可视化)
    源端发起-已建立连接 (ARP可达/转发表老化/关闭可视化)
    源端发起-已建立连接 (ARP可达/转发表正常/开启可视化)
    源端发起-已建立连接 (ARP可达/转发表正常/关闭可视化)
    目标端发起-已建立连接 (ARP Stale/转发表老化/开启可视化)
    目标端发起-已建立连接 (ARP Stale/转发表老化/关闭可视化)
    目标端发起-已建立连接 (ARP Stale/转发表正常/开启可视化)
    目标端发起-已建立连接 (ARP Stale/转发表正常/关闭可视化)
    目标端发起-已建立连接 (ARP可达/转发表老化/开启可视化)
    目标端发起-已建立连接 (ARP可达/转发表老化/关闭可视化)
    目标端发起-已建立连接 (ARP可达/转发表正常/开启可视化)
    目标端发起-已建立连接 (ARP可达/转发表正常/关闭可视化)
发版升级路径测试
    3.4.1
        SmartX Everoute 2.0.4 -> 3.4.1 升级
        SmartX Everoute 3.0.0 -> 3.4.1 升级
        SmartX Everoute 3.1.0 -> 3.4.1 升级
        SmartX Everoute 3.1.1 -> 3.4.1 升级
        SmartX Everoute 3.2.0 -> 3.4.1 升级
        SmartX Everoute 3.3.1 -> 3.4.1 升级
        SmartX Everoute 3.4.0 -> 3.4.1 升级
        Arcfra ANS 3.1.0 -> 3.4.1 升级
        Arcfra ANS 3.1.1 -> 3.4.1 升级
        Arcfra ANS 3.2.0 -> 3.4.1 升级
        Arcfra ANS 3.3.1 -> 3.4.1 升级
        Arcfra ANS 3.4.0 -> 3.4.1 升级