---
title: "SMTXZBS/5.7.0/SMTX ZBS 块存储配置指南"
source_url: "https://internal-docs.smartx.com/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_preface_generic"
sections: 30
---

# SMTXZBS/5.7.0/SMTX ZBS 块存储配置指南
## 关于本文档

# 关于本文档

本⽂档介绍了如何在 SMTX ZBS 块存储集群中创建块存储，以及如何配置外部客⼾端通过 iSCSI、NVMe over TCP 和 NVMe over RDMA 协议访问 SMTX ZBS 块存储。

阅读本文档需了解 SMTX ZBS 块存储软件、iSCSI 协议和 NVMe-oF 协议等相关技术背景知识，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 更新信息

**2025-12-01**：配合 SMTX ZBS 5.7.0 正式发布。

相较于 SMTX ZBS 5.6.4，本文档主要进行了如下更新：

- 更新了本文档的相关概念；
- 更新了流控相关配置；
- 新增开机自动挂载 iSCSI 文件系统操作；
- 新增 ESXi 主机通过双网口连接 SMTX ZBS 块存储的操作指导。

---

## 概述

# 概述

SMTX ZBS（读作 SmartX ZBS）是由北京志凌海纳科技股份有限公司（以下简称 “SmartX” ）研发的分布式存储软件，可以为客户端提供基于 iSCSI、 NVMe over RDMA 和 NVMe over TCP 协议访问的块存储服务。本文档介绍了如何在块存储集群和外部客户端进行配置，使得客户端能够使用 SMTX ZBS 提供的块存储服务。

---

## iSCSI 存储服务

# iSCSI 存储服务

块存储集群支持外部客户端通过 iSCSI 协议远程访问其块存储服务。

---

## iSCSI 存储服务 > 相关概念

# 相关概念

本节介绍了 iSCSI 相关概念，如您在配置过程中遇到不熟悉的概念，可在此快速查找对应的详细解释。

## iSCSI

iSCSI（Internet Small Computer System Interface）是在 SCSI 协议基础上发展的一种网络存储协议，它将 SCSI 协议封装在 IP 数据包中，并通过 IP 网络进行传输，从而使客户端在本地即可使用远程服务器上的存储设备，极大地扩展了存储设备的可访问性和灵活性。iSCSI 的优势在于能够利用现有的 IP 网络架构，降低存储网络的搭建和维护成本，同时提供与直接连接 SCSI 设备相似的性能，能够为客户端提供高效、稳健的存储访问服务。iSCSI 尤其适用于需要远程存储访问、灵活扩展存储容量和简化存储管理的环境。

## iSCSI Initiator

iSCSI Initiator 是安装在客户端主机的软件或硬件设备，负责发起与远程存储设备（即 iSCSI Target）的连接和数据传输。iSCSI Initiator 可以是一个安装在操作系统中的软件应用程序，也可以是集成在网络适配器中的专用硬件。iSCSI Initiator 通过 IP 网络向 iSCSI Target 发送请求，以实现数据的读取和写入，使得客户端能够像访问本地存储设备一样访问远程存储资源。

## iSCSI Target

iSCSI Target 是 iSCSI Initiator 访问的存储设备，用于响应 Initiator 的存储访问请求。iSCSI Target 将存储资源虚拟化为逻辑单元（LUNs）并提供给远程客户端使用。对于 Initiator 来说，iSCSI Target 提供的 LUN 类似于本地连接的存储设备。SMTX ZBS 块存储集群支持 Initiator 通过统一的接入虚拟 IP 访问 iSCSI Target，无需为每个 iSCSI Target 配置不同的 IP 地址。

## iSCSI LUN

iSCSI LUN（iSCSI Logical Unit Number）是在 iSCSI 存储服务中用于唯一标识存储设备上逻辑单元的编号。逻辑单元是一个逻辑概念，在 SMTX ZBS 块存储集群中可以对应于一个存储卷（Volume）。iSCSI Initiator 通过 iSCSI 协议与 iSCSI Target 进行通信，请求访问特定的 iSCSI LUN，iSCSI Target 接收到请求后，根据 LUN 的标识符将请求路由到相应的存储资源，然后将响应返回给 Initiator，使得 iSCSI Initiator 可以像使用本地存储一样使用 SMTX ZBS 块存储。

## 白名单

白名单是一种访问控制机制，用于指定允许访问 iSCSI Target 和 iSCSI LUN 的客户端。可通过业务主机和手动配置的方式来配置白名单。

- **使用业务主机配置白名单**

  您可以通过选择业务主机和业务主机组的方式（需提前[创建业务主机和业务主机组](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_183)），来指定可访问 iSCSI Target 和 iSCSI LUN 的客户端白名单。

  - **手动选择业务主机和业务主机组**

    手动勾选允许加入白名单的业务主机和业务主机组。若选择业务主机组时，若后续组内新增或删除业务主机时，会自动同步更新白名单。选择的业务主机（含主机组内的业务主机）必须均已配置 IQN 地址或均已配置 IP 地址。

    iSCSI LUN 的业务主机白名单默认与 iSCSI Target 相同，您也可以选择取消与所属 Target 保持一致，在所属 Target 白名单的范围内，进一步为 iSCSI LUN 选择可访问的业务主机。

    > **说明**：
    >
    > 使用业务主机指定白名单时，Initiator CHAP 的设置已包含在业务主机的设置中。
  - **自适应**

    开启自适应后，iSCSI Target 的 IQN 白名单会自动保持为所包含 LUN 的 IQN 白名单的并集，IP 白名单将为**全部允许**。

    在 iSCSI Target 启用自适应的情况下，iSCSI LUN 白名单配置方式默认使用业务主机，您可以自行添加允许访问该 LUN 的业务主机。也可选择手动配置白名单。
- **手动配置白名单**

  手动通过设置 IP 地址和 IQN 来标识可以访问 iSCSI Target 和 iSCSI LUN 的客户端。

  > **说明**：
  >
  > - 只有同时属于 IP 白名单和 IQN 白名单的客户端才可以访问 iSCSI Target。
  > - 若要访问 iSCSI LUN，客户端必须同时在该 LUN 的 IQN 白名单以及其所属 Target 的 IP 白名单和 IQN 白名单上。

  - **IP 白名单**

    通过 IP 地址标识的允许访问 iSCSI Target 的客户端。iSCSI Target 的 IP 白名单可设置为**全部禁止**、**允许指定 IP**、**全部允许**，默认为**全部允许**。
  - **IQN 白名单**

    通过 IQN 标识的允许访问 iSCSI Target 和 iSCSI LUN 的客户端。

    iSCSI Target 的 IQN 白名单可设置为**自适应**、**全部禁止**、**允许指定 IQN**、**全部允许**，默认为**自适应**。当选择**自适应**时，会自动保持为所包含 LUN 的 IQN 白名单的并集。

    iSCSI LUN 可以在 iSCSI Target IQN 白名单的范围内，进一步自定义可访问 LUN 的 IQN 白名单，可设置为**全部禁止**、**允许指定 IQN**、**全部允许**。当所属的 iSCSI Target 禁止全部客户端访问时，指定的 LUN 的 IQN 白名单将不会生效。

## 身份认证

由于 iSCSI 技术通过 IP 网络远程连接存储，确保网络连接的安全性至关重要。iSCSI 支持使用 CHAP (Challenge Handshake Authentication Protocol) 协议对 iSCSI Target 和 iSCSI Initiator 进行认证，以提高存储访问的安全性。

CHAP 协议通过挑战-握手的方式确保合法性验证的安全性。SMTX ZBS 块存储支持 Initiator CHAP 认证和 Target CHAP 认证，这两种认证方式结合在一起，既可防止未经授权的客户端访问存储资源，也可确保目标客户端只与授权的 Target 建立连接。这种双向认证机制可有效提升 iSCSI 存储连接整体的安全性。

### Initiator CHAP

Initiator CHAP 是单向 CHAP 认证，用于 Target 对 iSCSI Initiator 进行身份认证，但 Initiator 无需验证 Target。

### Target CHAP

开启 Target CHAP 后，iSCSI Initiator 将对 iSCSI Target 进行身份认证。开启 Target CHAP 认证时，需同时开启 Initiator 认证，实现 iSCSI Target 和 iSCSI Initiator 的双向认证。

## 存储策略

SMTX ZBS 块存储集群的存储策略包括冗余策略（多副本、纠删码）、置备方式、条带化、常驻缓存模式和数据加密。

### **冗余策略**

- **多副本**

  多副本技术是指在多个节点上存放相同数据的多个副本，以保障数据的高可用性。多副本为数据提供了冗余机制，即使某个节点发生故障，其他健康节点依然还有完整的副本，可保证数据正常的 I/O 读写。

  SMTX ZBS 块存储集群支持 2 副本和 3 副本。当集群可提供存储服务的节点数不低于 5 个时，默认为 3 副本，否则默认为 2 副本。对于双活集群，只支持 3 副本。
- **纠删码**

  纠删码（Erasure Coding，EC）是一种数据冗余机制。它通过特定的算法对 K 个原始数据块（Data Block）进行处理，生成 M 个校验块（Parity Block）。在损坏数据块的数量不超过 M 的情况下，可通过纠删码算法，利用 K 个可用的数据块和校验块即可重建出损坏的数据块，实现数据的恢复和容错能力。通过纠删码，即使部分数据丢失，仍然可以恢复完整的数据，能够有效地提高存储系统的可靠性和容量利用率。

  选择纠删码作为冗余策略时，集群中可提供存储服务（至少一个硬盘池存储服务健康且非移除中）的节点数至少 K+M+1。

  > **说明**：
  >
  > 块存储集群需满足如下条件才可使用纠删码：
  >
  > - 可提供存储服务的节点数不小于 4；
  > - 集群为分层存储模式；
  > - 集群未启用双活特性。

### **置备方式**

置备方式是一种存储空间分配策略。SMTX ZBS 块存储集群支持厚置备和精简置备两种置备方式。

- **厚置备**

  使用厚置备方式时，在创建 iSCSI LUN 时，ZBS 会立即为 LUN 分配所指定的所有空间，即使 LUN 实际上仅使用了部分容量，但整个指定空间都会始终被 LUN 占用，无法被其他资源所使用。

  由于在创建 iSCSI LUN 时就分配了整个指定的容量，厚置备的 iSCSI LUN 在进行写操作时不会受到动态空间分配的影响，因此可以在某种程度上提供更加稳定的性能，且因存储空间在一开始就已经全部分配，所以不需要频繁地进行动态调整。
- **精简置备**

  使用精简置备方式时，在创建 iSCSI LUN 时，ZBS 并不立即为 LUN 分配整个指定的空间，而是根据需要动态分配，只有在实际写入数据时才会分配实际的存储空间，未写入时不占用存储空间资源。

  由于精简置备的 iSCSI LUN 只在实际需要时才会被分配存储空间，避免了预先分配可能导致空间浪费，提升了空间的利用率，且可以灵活适应一些需求动态变化的业务场景。

### **条带化**

条带化（Striping）是指数据分割成大小相同的条带（Stripe），并尽可能将每条数据分别写入到不同硬盘上，以充分利用多个硬盘 I/O 能力的方法。

在 SMTX ZBS 块存储集群中，用户可以对 iSCSI LUN 灵活设置条带数（包括 1、2、4、8，默认为 8），条带化可以充分发挥多硬盘并行工作的优势，条带数越多，并行度越高，尤其在处理顺序 I/O 时性能表现更为出色。条带大小默认为 256 KiB，不可更改。

### **常驻缓存**

数据常驻缓存（Volume pining）是块存储集群在分层部署（包括混闪分层部署和全闪分层部署）模式下可使用的一种存储优化策略。

分层部署的块存储集群在默认情况下，LUN 中具有较高访问频率的数据将停留在速度更快的缓存层，访问频率较低的数据将下沉至速度相对较慢的数据层。对 LUN 启用常驻缓存模式后，LUN 的数据将始终保留在缓存层，从而获得更稳定的高性能。

> **说明**：
>
> 块存储集群仅在集群部署模式为分层部署时允许数据常驻缓存。

## 数据加密

启用数据加密可以对 iSCSI LUN 进行加密保护。在数据写入时，系统将对数据进行加密后存储至物理盘；在数据读取时，系统将先对加密数据进行解密，将解密后的明文数据返回客户端。

> **说明**：
>
> - 若要启用数据加密，请确认在集群设置中已启用了加密功能。具体操作请参考[管理加密功能](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_167)功能。
> - 在使用加密卷的过程中，请确保密钥管理服务器的许可在有效期内。

## I/O 突发

I/O 突发是指在指定的时间段内，系统的 I/O 操作可以短暂地超过预设的 IOPS 上限或带宽上限。这允许系统在应对临时的高负载或需要更快响应时间的情况时可以提供更高的性能，同时也可以通过设置突发上限和持续时间上限进行更精细化的管理。

下图示意了开启 IOPS 限制，并且允许 I/O 突发时可能出现的 IOPS 监控图形。

![](https://cdn.smartx.com/internal-docs/assets/06ea7d56/zbs_administration_guide_017.png)

在 t1 和 t2 时间段内，分别发生了 1 次 I/O 突发。

- t1 持续时长低于设定的持续时间上限：IOPS 可以高于 IOPS 上限，且低于 IOPS 突发上限。
- t2 持续时长高于设定的持续时间上限：当突发流量累计到一定程度时，IOPS 被限制到 IOPS 上限以下。

## LUN 快照

LUN 快照是指对 iSCSI LUN 在某个时间点的状态进行记录和保存的功能。快照捕捉了 LUN 在某一时刻的状态，使得用户可以在之后的时间点回溯到这个特定的数据状态，实现数据备份、恢复、测试以及其他用途。

---

## iSCSI 存储服务 > 配置概览

# 配置概览

iSCSI 存储服务的配置包括：

- 在块存储集群创建 iSCSI Target 和 iSCSI LUN。
- 配置通过 iSCSI 协议访问存储的客户端（Linux/Windows/VMware vSphere 集群）。

**前提条件**

- 客户端及版本需适配 SMTX ZBS 块存储。适配的客户端及版本请参考《SMTX ZBS 5.7.0 发布说明》的[客户端和存储协议配套说明](/smtxzbs/5.7.0/zbs_release_notes/zbs-release-notes-03#%E5%AE%A2%E6%88%B7%E7%AB%AF%E5%92%8C%E5%AD%98%E5%82%A8%E5%8D%8F%E8%AE%AE%E9%85%8D%E5%A5%97%E8%AF%B4%E6%98%8E)。
- 客户端与块存储集群的接入网络能够连通。

---

## iSCSI 存储服务 > 创建 iSCSI Target 和 iSCSI LUN

# 创建 iSCSI Target 和 iSCSI LUN

## 创建 iSCSI Target

1. 登录 CloudTower 控制台，进入块存储集群的管理界面，选择**设置**>**虚拟 IP**，输入 iSCSI 接入虚拟 IP。
2. 在块存储集群的管理界面，单击右上方的**创建**，选择**创建 iSCSI Target**。
3. 在弹出的创建页面上，设置 iSCSI Target 的名称、描述、白名单、登录认证信息、存储策略和默认 I/O 限制。具体参数说明请参考[相关概念](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_23)。

   > **说明**：
   >
   > - 在 iSCSI Target 设置的副本数、置备方式和是否启用常驻缓存、是否启用加密，仅作为该 iSCSI Target 内新建 LUN 的默认存储策略。您也可以在创建 LUN 或编辑 LUN 时设置单独的存储策略。
   > - 双活集群的冗余策略不支持纠删码配置，仅支持 3 副本配置。
   > - 若需启用常驻缓存模式，请确保已在集群的**设置** > **常驻缓存**界面启用了**允许数据常驻缓存**。
   > - iSCSI Target 设置的 I/O 限制仅作为该 iSCSI Target 内新建 LUN 的默认 I/O 限制选项，而非 iSCSI Target 整体的 I/O 限制。
4. 单击**创建**，完成 iSCSI Target 的创建。

## 创建 iSCSI LUN

1. 进入 iSCSI Target 管理界面，单击右上方的**创建**，选择**创建 LUN**。
2. 在弹出的创建页面上，设置 iSCSI LUN 的名称、容量、ID、存储策略、访问设置和 I/O 限制。具体参数说明请参考[相关概念](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_011)。

   > **说明**：
   >
   > - 新建的 LUN 默认使用所属 iSCSI Target 的存储策略和 I/O 限制，您也可以为 LUN 自定义副本数、常驻缓存模式、IQN 白名单和 I/O 限制、是否启用加密，但冗余策略类型和具体的纠删码参数必须与所属 iSCSI Target 保持相同，创建后不可更改。
   > - 双活集群的冗余策略不支持纠删码配置，仅支持 3 副本配置。
3. 单击**创建**，完成 iSCSI LUN 的创建。

---

## iSCSI 存储服务 > 配置客户端通过 iSCSI 协议访问存储

# 配置客户端通过 iSCSI 协议访问存储

SMTX ZBS 支持 Linux 客户端、Windows 客户端和 VMware vSphere 集群通过 iSCSI 协议访问块存储。

---

## iSCSI 存储服务 > 配置客户端通过 iSCSI 协议访问存储 > 配置 Linux 客户端

# 配置 Linux 客户端

Linux 主机可以通过 Open-iSCSI 连接存储。

**注意事项**

- 为确保 Linux 主机能够通过 iSCSI 协议连接存储，建议进行优化配置。以下两种配置可任选其一，但推荐配置允许 iscsid 访问 chunk 的 3261 端口。

  - 允许 iscsid 访问 chunk 的 3261 端口（推荐配置）

    `sudo yum install policycoreutils-python`

    `sudo semanage port -a -t iscsi_port_t -p tcp 3261`
  - 关闭 SELinux

    1. 确认 SElinux 当前状态。

       `getenforce`
    2. 关闭 SElinux。

       - 临时关闭

         `setenforce 0`
       - 永久关闭

         修改 `/etc/selinux/config` 配置文件，将 `SELINUX=enforcing` 修改 为 `SELINUX=disabled`。 重启系统后生效。
- 对于克隆生成的 Linux 系统，其 IQN 与源系统的 IQN 相同。为避免连接异常，请执行 `iscsi-iname` 命令生成新的 IQN，并编辑 `/etc/iscsi/initiatorname.iscsi` 文件，用新的 IQN 覆盖原来的 IQN。
- 为使 Open-iSCSI 具有更好的兼容性，建议编辑 `/etc/iscsi/iscsid.conf` 配置文件，对如下参数进行如下调整：

  - `node.session.queue_depth = 128`（默认值为 32）
  - `node.conn[0].timeo.login_timeout = 5`（默认值为 15）
  - `node.session.initial_login_retry_max = 24`（默认值为 8）
  - `node.session.cmds_max = 1024`（默认值为 128）
  - `node.session.iscsi.DefaultTime2Wait = 1`（新增参数）
  - `iface.delayed_ack = disable`

## 连接存储

1. 发现存储。其中 `Cluster iSCSI VIP` 为 iSCSI 接入虚拟 IP。

   `iscsiadm -m discovery -t st -p <Cluster iSCSI VIP>`
2. 连接存储。其中 `IQN-name` 为 Target 的 IQN 名称。

   `iscsiadm -m node -T <IQN-name> -p <Cluster iSCSI VIP> -l`
3. 查看连接状态确认已成功连接存储。

   `iscsiadm -m session -P 1`
4. 查看已挂载的存储。存储挂载后即可正常使用。

   `iscsiadm -m session -P 3`

用户也可选择配置客户端重启后是否自动挂载存储，配置方法如下：

1. 编辑 `/etc/iscsi/iscsid.conf` 配置文件，修改 `node.startup` 参数。

   - 重启后自动挂载存储

     `node.startup = automatic`
   - 重启后手动挂载存储

     `node.startup = manual`
2. 重新执行 `iscsiadm -m discovery -t st -p <Cluster iSCSI VIP>` 命令发现存储。
3. 执行以上操作后，客户端在重启后将根据配置文件自动或需手动挂载存储。

配置示例如下：

```
[root@scvm69 15:25:18 ~]$iscsiadm -m discovery -t st -p 10.0.10.73
10.0.10.73:3260,1 iqn.2016-02.com.smartx:system:test
[root@scvm69 15:25:30 ~]$iscsiadm -m node -T iqn.2016-02.com.smartx:system:test -p 10.0.10.73 -l
Logging in to [iface: default, target: iqn.2016-02.com.smartx:system:test, portal: 10.0.10.73,3260] (multiple)
Login to [iface: default, target: iqn.2016-02.com.smartx:system:test, portal: 10.0.10.73,3260] successful.
[root@scvm69 15:25:59 ~]$iscsiadm -m session -P 1
Target: iqn.2016-02.com.smartx:system:test (non-flash)
    Current Portal: 10.0.10.71:3261,1
    Persistent Portal: 10.0.10.73:3260,1
        **********
        Interface:
        **********
        Iface Name: default
        Iface Transport: tcp
        Iface Initiatorname: iqn.1994-05.com.redhat:a3644b1ed44
        Iface IPaddress: 10.0.10.69
        Iface HWaddress: <empty>
        Iface Netdev: <empty>
        SID: 1
        iSCSI Connection State: LOGGED IN
        iSCSI Session State: LOGGED_IN
        Internal iscsid Session State: NO CHANGE
```

## 配置 CHAP 认证

若 iSCSI Target 开启了 CHAP 认证，则 Linux 客户端需配置认证信息。

> **注意**：
>
> 开启 Target CHAP 进行双向认证时，需同时完成 Initiator CHAP 和 Target CHAP 认证配置。

- **Initiator CHAP**

  编辑 `/etc/iscsi/iscsid.conf` 配置文件，添加如下内容。其中 `username` 和 `password` 与 iSCSI Target 中 Initiator CHAP 设置的用户名、密码需保持相同。

  `node.session.auth.authmethod = CHAP`

  `node.session.auth.username = username`

  `node.session.auth.password = password`
- **Target CHAP**

  编辑 `/etc/iscsi/iscsid.conf` 配置文件，添加如下内容。其中 `username_in` 和 `password_in` 与 iSCSI Target 中 Target CHAP 设置的用户名、密码需保持相同。

  `node.session.auth.username_in = username_in`

  `node.session.auth.password_in = password_in`

完成 CHAP 认证配置后，请重启 iscsid 服务。

## 配置 DM-Multipath

**推荐配置**

- 如果计算节点通过 Multipath 连接 ZBS（常见于 H3C CAS、Huawei FusionCompute 和 OpenStack 环境），建议在 Multipath 配置文件中为 ZBS 指定专用规则。以 CentOS 为例，可在 `/etc/multipath.conf` 的 `devices` 字段中添加如下 ZBS device 配置：

  ```
  devices {
      device {
          vendor                  "ZBS"
          product                 "VOLUME"
          path_grouping_policy    "multibus"
          failback                "immediate"
          prio                    "const"
          path_selector           "service-time 0"
          path_checker            "tur"
          fast_io_fail_tmo        5
          dev_loss_tmo            125
          no_path_retry           60
          flush_on_last_del       yes
          deferred_remove         yes
      }
  }
  ```

  | 配置项 | 说明 |
  | --- | --- |
  | vendor | 指定该 device 配置要应用于的存储设备的供应商名称。 |
  | product | 指定该 device 配置要应用于的存储设备的产品名称。 |
  | path\_grouping\_policy | 指定多路径的路径分组策略。设置为 `multibus` 表示将所有可用路径放入同一个优先级组。 |
  | failback | 指定当主路径恢复可用时的回切策略。设置为 `immediate` 表示立即回切到主路径组。 |
  | prio | 指定路径优先级算法。设置为 `const` 表示所有路径具有相同固定优先级。 |
  | path\_selector | 指定在路径组内选择 I/O 路径的策略。设置为 `service-time 0` 表示根据路径的估测服务时间动态分配 I/O。 |
  | path\_checker | 指定路径可用性检测方式。设置为 `tur` 表示使用 `TEST UNIT READY` 指令检测路径是否正常。 |
  | fast\_io\_fail\_tmo | 该参数将全局配置所有 iSCSI 设备的 `recovery_tmo` 参数，即 iSCSI 设备连接的超时时间。 |
  | dev\_loss\_tmo | 指定设备丢失超时时间。 |
  | no\_path\_retry | 指定当设备所有路径都不可用时的 I/O 重试策略。设置为 `60` 表示最多重试 60 次。 |
  | flush\_on\_last\_del | 设置为 `yes` 时，当设备的最后一条路径被删除时，multipathd 守护进程将禁用队列重试。 |
  | deferred\_remove | 设置为 `yes` 时，当设备的最后一条路径被删除时，DM-Multipath 将执行延迟删除而非立即删除。 |

**使配置生效**

- 要使 `/etc/multipath.conf` 中的最新配置立即生效，请执行：

  `systemctl restart multipathd`
- 执行该命令不会影响正在进行的 I/O 操作。

## 配置开机自动挂载 iSCSI 磁盘文件系统

若需在客户端系统启动阶段自动挂载 iSCSI 磁盘文件系统，建议在客户端主机上完成如下配置：

**前提条件**
请确保已在 SMTX ZBS 集群中正确配置了目标主机与相关 iSCSI LUN 的访问权限。包括：

- 确保目标主机已包含在目标 iSCSI LUN 的访问白名单中；
- 与目标 iSCSI LUN 位于相同 Target 的其他 iSCSI LUN，已明确配置了拒绝该主机访问。

**操作步骤**

1. 编辑客户端主机的 `/etc/fstab` 配置文件，添加该文件系统的挂载条目：

   `<device> <mount point> <type> <options> <dump> <pass>`

   例如：

   ```
   /dev/iscsi_test_vg/iscsi_test_lv    /mnt/test   xfs     defaults,_netdev,nofail,x-systemd.requires=iscsi.service,x-systemd.after=network-online.target  0 0
   ```

   | 参数 | 说明 |
   | --- | --- |
   | `device` | 指定要自动挂载的设备（块设备或逻辑卷）。  可直接使用设备路径，例如：`/dev/iscsi_test_vg/iscsi_test_lv`；  也可使用设备 UUID，例如：`UUID=3ec46a85-ccec-4f48-bab6-c7b5b8a512ea`。  设备 UUID 可通过 `blkid <device>` 获取，例如：`blkid /dev/iscsi_test_vg/iscsi_test_lv`。 |
   | `mount point` | 文件系统的挂载点。 |
   | `type` | 文件系统类型。 |
   | `options` | 挂载选项，以英文逗号分隔多个参数。对于 iSCSI 磁盘文件系统，除 `defaults` 外，建议指定如下全部参数： - `_netdev`：表示该设备依赖网络，只有网络启动后才能挂载。 - `nofail`：表示挂载失败后，不阻塞系统启动。 - `x-systemd.requires=iscsi.service`：指示 systemd 在挂载前必须先启动 `iscsi.service`。 - `x-systemd.after=network-online.target`：指示挂载动作要在网络完全就绪后再执行。 |
   | `dump` | dump 备份标志，决定该文件系统是否需要备份。 - `0`：不需要备份 - `1`：需要备份 |
   | `pass` | fsck 检查顺序，决定系统启动时文件系统检查的顺序。 - `0`：文件系统不需要检查，fsck 会跳过该文件系统 - `1`：fsck 最先检查该文件系统，通常用于根文件系统 - `2`：其他需要检查的文件系统，按驱动器顺序检查 |
2. 为了在开机启动时能够通过 iSCSI 协议连接存储，建议进行优化配置。以下两种方法可任选其一，但推荐配置允许 iscsid 访问 chunk 的 3261 端口。

   - 允许 iscsid 访问 chunk 的 3261 端口（推荐配置）。

     `sudo yum install policycoreutils-python`

     `sudo semanage port -a -t iscsi_port_t -p tcp 3261`
   - 永久关闭 SELinux。

     修改 `/etc/selinux/config` 配置文件，将 `SELINUX=enforcing` 修改为 `SELINUX=disabled`。 重启系统后生效。
3. 系统中如果残留不存在的或无法访问的 iSCSI 节点，可能会在阻塞 open-iscsi 服务的启动，导致系统开机时无法自动登录其他正常节点。因此，建议及时清理无效节点。

   - 查看当前所有 iSCSI 节点：

     `iscsiadm -m node`
   - 删除已失效或不可达的节点（需指定对应的 IQN 和 portal IP）：

     `iscsiadm -m node -T <IQN> -p <IP>:<port> -o delete`
4. 设置系统启动时自动执行 iSCSI 登录操作。

   - CentOS / Fedora 系列：

     `systemctl enable iscsi`
   - Ubuntu 系列：

     `systemctl enable open-iscsi`
5. 设置文件系统所在 iSCSI Target 的登录策略，使其在系统启动时自动登录。

   `iscsiadm -m node -T <IQN-name> -p <Cluster iSCSI VIP> --op update -n node.startup -v automatic`

---

## iSCSI 存储服务 > 配置客户端通过 iSCSI 协议访问存储 > 配置 Windows 客户端

# 配置 Windows 客户端

Windows Server 可使用系统自带的 iSCSI 客户端连接 SMTX ZBS 块存储。

## 连接存储

1. 单击**控制面板**， 搜索“iscsi”。
2. 在查找结果中选择**设置 iSCSI 发起程序**。若出现询问是否启动该服务的对话框，请单击**是**。
3. 在弹出的对话框中，单击**发现**选项卡 ，单击**发现门户**按钮，弹出**发现目标门户**对话框。输入块存储集群的 iSCSI 接入虚拟 IP，单击**确定**，开始连接块存储集群。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image5.png)
4. 连接成功后，单击**目标门户**中的**刷新**按钮，即可在**目标**标签页中发现对应的存储。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image8.png)
5. 选中对应的数据存储，单击**连接**后，即可在计算机管理中的**磁盘管理**中发现对应磁盘。可以对该磁盘进行分区、格式化等操作。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image10.png)

## 配置 CHAP 认证

若 iSCSI Target 开启了 CHAP 认证，则客户端需配置认证信息。

> **注意**
>
> 开启 Target CHAP 进行双向认证时，需同时配置 Initiator CHAP 和 Target CHAP 认证。

- **Initiator CHAP**

  1. 在 iSCSI 发起程序中，在已发现的 Target 中选择目标 Target，单击**连接**按钮。

     ![](https://cdn.smartx.com/internal-docs/assets/c577f847/windows-initiator-chap-1.png)
  2. 在弹出的对话框中，选择**高级**，进入高级设置界面。

     ![](https://cdn.smartx.com/internal-docs/assets/c577f847/windows-initiator-chap-2.png)
  3. 勾选**启用 CHAP 登录**，输入用户名和密码信息。该用户名和密码和 iSCSI Target 中 Initiator CHAP 设置的用户名、密码需保持相同。  
     若需进行 Target CHAP 认证，则需勾选**执行相互身份验证**，并完成后续的 Target CHAP 认证。

     ![](https://cdn.smartx.com/internal-docs/assets/c577f847/windows-initiator-chap-3.png)
- **Target CHAP**

  1. 在 iSCSI 发起程序的**配置**选项卡，单击 **CHAP** 按钮。

     ![](https://cdn.smartx.com/internal-docs/assets/c577f847/windows-target-chap-1.png)
  2. 输入 Target CHAP 的密码。Windows 在进行 Target CHAP 认证时，自动使用 Target IQN 作为用户名，因此此处无需输入用户名。

     ![](https://cdn.smartx.com/internal-docs/assets/c577f847/windows-target-chap-2.png)

## 回收存储空间

当客户端的文件系统不再需要使用部分存储空间时（如删除文件），这部分空间会变成未使用空间。为避免这些未使用空间长期占用存储容量，可以通过 Windows 的**磁盘优化**功能释放存储空间，提高存储利用率。

> **说明**：
>
> 该操作仅适用于精简置备的 iSCSI LUN。

操作方法如下：

1. 选择**开始** -> **设置** -> **系统** -> **存储**，选择**优化驱动器和释放空间**，单击**优化驱动器**。
2. 在磁盘优化工具中选择希望优化的驱动器（即虚拟卷），单击**优化**，系统将开始执行磁盘优化操作。

磁盘优化完成后，可在任一节点执行 `zbs-iscsi lun list <target_name>` 命令，通过查看输出结果中的 `Unique Size` 的变化来确认存储空间是否已释放。

> **说明**：
>
> 存储空间的释放是一个渐进的过程，若释放的空间较大，可能需等待一段时间才能使空间完全释放，请您耐心等待。

---

## iSCSI 存储服务 > 配置客户端通过 iSCSI 协议访问存储 > 配置 VMware vSphere 集群

# 配置 VMware vSphere 集群

本节介绍如何配置远端 VMware vSphere 集群挂载 SMTX ZBS 块存储作为数据存储（Datastore）使用。

**注意事项**

为确保 ESXi 主机可正常通过 iSCSI 协议挂载 SMTX ZBS 块存储，需在 ESXi 主机上安装 SmartXISCSIFirewall VIB 插件。

SmartXISCSIFirewall VIB 插件和 ESXi 主机的版本适配关系如下：

- ESXi 6.5 及以上版本、ESXi 7.0 U2 及以上版本需安装 1.0.1 版本的 SmartXISCSIFirewall VIB 插件。
- ESXi 8.0 U1a 及以上版本需安装 2.0.1 版本的 SmartXISCSIFirewall VIB 插件。

**前提条件**

- 已根据 ESXi 版本提前获取对应版本的 SmartXISCSIFirewall VIB 插件安装包。
- VMware vSphere 集群中的 ESXi 主机的 IP 地址可以连通块存储集群的接入网络。

## 第 1 步：配置 VMware vSphere 集群支持 iSCSI

1. 在每台 ESXi 主机上更改 ESXi 安装软件权限，避免 SmartXISCSIFirewall VIB 插件安装过程中出现权限错误。

   `esxcli software acceptance set --level=CommunitySupported`
2. 在每台 ESXi 主机上安装 SmartXISCSIFirewall VIB 插件。复制插件安装包到 ESXi 主机后，运行以下命令安装插件：

   `esxcli software vib install -v path -f`

   其中 `path` 需要替换为真实环境中 SmartXISCSIFirewall VIB 插件完整的绝对路径，例如 `/tmp/SmartXISCSIFirewall_1.0.1.vib`。

   > **说明**：
   >
   > ESXi 主机安装 1.0.1 版本 SmartXISCSIFirewall VIB 插件后，若需升级至 ESXi 8.0 U1a 及以上版本，请先执行 `esxcli software vib update -v path --no-sig-check` 命令将 SmartXISCSIFirewall VIB 插件升级至 2.0.1 版本，然后再进行 ESXi 升级。
3. 使用 VMware vSphere Web Client 登录到 vCenter Server，浏览到 ESXi 主机界面。选中 ESXi 主机， 选择**配置**>**系统**>**防火墙**>**编辑**，确认 **SmartXISCSIFirewall** 已勾选：

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/smartx-iscsi-firewall.png)

## 第 2 步：为 ESXi 主机配置与块存储集群连通的接入网络

ESXi 主机既可以通过单一网口连接块存储集群，也可以采用多网口配置以增强可靠性和性能。使用多网口配置时，当某个网口发生故障时，仍可保证连接不中断，同时还可提供更高的带宽。对于多网口配置，本文将以双网口为例进行说明。

### ESXi 主机通过单网口连接块存储集群

1. 在 ESXi 主机界面，选择**配置**>**网络**>**虚拟交换机**>**添加网络**，在弹出的**添加网络**界面中，选择 **VMkernel 网络适配器**。单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/installationguide_032.png)
2. 进入**选择目标设备**。选择**新建标准交换机**。
3. 创建标准交换机。单击**添加**按钮，将合适的物理网络适配器分配给新创建的交换机。

   > **说明**：
   >
   > 由于接入网络要求必须是 10 Gb 及以上的以太网，因此可根据网络适配器**状态**一栏显示的适配器的速率信息，选择 10000 Mb 及以上的网络适配器。
4. 设置端口属性。在**端口属性**选项页面，使用默认的属性设置，单击 **NEXT**。
5. 设置 IPv4 参数。选择**使用静态 IPv4 设置**，在 **IPv4 地址**中输入 ESXi 主机的接入 IP 并设置子网掩码。

   若接入网络有明确的子网规划（例如接入网络自身存在网关），则按照接入网络的实际子网掩码配置。若接入网络未配置网关，确保配置的子网掩码可保证 ESXI 接入 IP 和 SMTX ZBS 块存储集群的接入 IP 处于同一子网即可。
6. 完成配置后，在 ESXi 上 Ping 块存储集群的接入虚拟 IP，确认网络可以正常连接。

### ESXi 主机通过双网口连接块存储集群

1. 在 ESXi 主机界面，选择**配置**>**网络**>**虚拟交换机**>**添加网络**，在弹出的**添加网络**界面中，选择 **VMkernel 网络适配器**。单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/installationguide_032.png)
2. 进入**选择目标设备**。选择**新建标准交换机**。
3. 创建标准交换机。单击**添加**按钮，将合适的 **2** 个物理网络适配器分配给新创建的交换机。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image11.png)

   > **说明**：
   >
   > 由于接入网络要求必须是 10 Gb 及以上的以太网，因此可根据网络适配器**状态**一栏显示的适配器的速率信息，选择 10000 Mb 及以上的网络适配器。
4. 设置端口属性。在**端口属性**选项页面，使用默认的属性设置，单击 **NEXT**。
5. 设置 IPv4 参数。选择**使用静态 IPv4 设置**，在 **IPv4 地址**中输入 ESXi 主机的**接入 IP 1**并设置子网掩码。

   若接入网络有明确的子网规划（例如接入网络自身存在网关），则按照接入网络的实际子网掩码配置。若接入网络未配置网关，确保配置的子网掩码可保证 ESXI 接入 IP 和 SMTX ZBS 块存储集群的接入 IP 处于同一子网即可。
6. 完成上述配置后，请重新进入 ESXi 主机界面，选择**配置**>**网络**>**虚拟交换机**>**添加网络**，在弹出的**添加网络**界面中，选择 **VMkernel 网络适配器**。单击 **NEXT**。
7. 进入**选择目标设备**。选择**现有标准交换机**，并选择步骤 **3** 中已创建的标准交换机。单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image12.png)
8. 设置端口属性。在**端口属性**选项页面，使用默认的属性设置，单击 **NEXT**。
9. 设置 IPv4 参数。选择**使用静态 IPv4 设置**，在 **IPv4 地址**中输入 ESXi 主机的**接入 IP 2**并设置子网掩码。请确保接入 IP 2 和接入 IP 1 在同一子网。
10. 设置 VMKernel 网络适配器的故障切换顺序。选择已创建的标准交换机，依次编辑其上的 VMKernel 网络适配器，在**绑定和故障切换** > **故障切换顺序**中，勾选**替代**，仅指定一个物理网络适配器作为活动适配器，并将另一个物理网络适配器移至未用的适配器列表。确保每个 VMkernel 适配器都绑定在不同的活动适配器上，以实现网络冗余与高可用性。

    ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image13.png)

    ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image14.png)
11. 完成配置后，在 ESXi 上 Ping 块存储集群的接入虚拟 IP，确认网络可以正常连接。

## 第 3 步：配置 iSCSI Target 作为数据存储（Datastore）使用

1. 为 ESXi 主机添加软件 iSCSI 适配器。在 ESXi 主机界面，依次选择**配置**>**存储适配器**>**添加软件适配器**，选择**添加软件 iSCSI 适配器**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/iscsi-software-adapter-2.png)
2. 在 ESXi 的存储适配器上添加 iSCSI Target。在 ESXi 主机界面依次单击**存储适配器** > **iSCSI Software Adapter**，然后选择 Target 的发现方式。

   - **动态发现**：此方式可自动连接指定 SMTX ZBS 集群中允许当前 ESXi 主机访问的所有 Target。若选择此方式，请单击**添加**，然后在**添加发送目标服务器**界面，输入接入虚拟 IP 和 3260 端口。

     ![](https://cdn.smartx.com/internal-docs/assets/c577f847/add-iscsi-software-adapter-2.png)
   - **静态发现**：此方式可自动连接指定 SMTX ZBS 集群中允许当前 ESXi 主机访问的指定 Target。若选择此方式，请单击**添加**，然后在**添加静态目标服务器**界面，输入接入虚拟 IP 、 3260 端口和 Target IQN。

     ![](https://cdn.smartx.com/internal-docs/assets/c577f847/add-iscsi-software-adapter-4.png)
   > **说明**：
   >
   > 对于任意一个 Target，只有属于该 Target 的 IP 白名单和 IQN 白名单的客户端才可以访问该 Target。
3. 若 iSCSI Target 开启了 CHAP 认证，则在添加发送目标服务器时，需同时配置认证信息。若未开启 CHAP 认证，可跳过此步骤。

   在**添加发送目标服务器**界面，取消勾选**从父项继承身份验证设置**，选择对应的 CHAP 认证方式，并输入用户名和密码信息。该用户名和密码须和 iSCSI Target 中设置的 CHAP 用户名、密码相同。注意，若开启了 Target CHAP 认证，需同时配置 Initiator CHAP 认证（出站 CHAP 凭据）和 Target CHAP 认证（入站 CHAP 凭据）。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/add-iscsi-software-adapter-3.png)
4. 配置网络绑定。单击**网络端口绑定**>**添加**，选择存储网络对应的物理网卡。

   **说明**：若选择双网口连接块存储，请同时勾选两个物理网卡，并在添加完毕后，确认两个端口的端口组策略状态为**合规**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image15.png)
5. 单击**重新扫描适配器**。扫描完成后可以在**设备**中发现块存储集群的 LUN。您可以根据 LUN UUID 确认对应的 LUN。

   > **说明**：
   >
   > ESXi 主机仅能扫描到允许其访问的 iSCSI LUN。对于任意一个 LUN，只有属于该 LUN 的 IQN 白名单的客户端才可以访问该 LUN。

   默认情况下，LUN 存储设备的多路径策略为固定，只会使用单个网口访问存储。如需同时使用两个网口，请在选中单个存储设备后，在**属性** > **多路径策略** > **操作** >**编辑多路径策略**，将路径选择策略设置为**循环**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image16.png)
6. 在每一台需要访问 LUN 的 ESXi 主机上重复 1 ~ 5 步。
7. 前往**数据存储**，新建基于该 LUN 的 VMware 数据存储。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/create-datastore-with-zbs-target-2.png)

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/create-datastore-with-zbs-target-3.png)

   选择较高版本的 VMFS。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/create-datastore-with-zbs-target-4.png)
8. 在每一台 ESXi 主机执行 `/sbin/auto-backup.sh` 或 `/sbin/backup.sh 0 /bootbank` 命令，保存配置。

## 第 4 步：在集群中其他节点挂载 VMware 数据存储

VMware 数据存储建立一次即可，集群中的其他节点挂载该数据存储后即可使用。

## 第 5 步：调整 ESXi 性能参数

1. 将最大 I/O 大小从默认的 128 K 调整到 512 K。

   登录每台 ESXi 主机，执行以下命令。

   `esxcli system settings advanced set -o /ISCSI/MaxIoSizeKB -i 512`
2. 进入 ESXi 主机界面，单击**配置**，选择**存储适配器**，单击**高级选项**>**编辑**，进入 iSCSI 控制器选项界面，对 iSCSI HBA 的配置进行如下配置，将读 I/O 最大 512 K（默认 128 K）。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/tune-zbs-iscsi-hba.png)

   保持 **DelayedACK** 的状态为 **false**，以关闭 iSCSI 控制器的延迟确认功能；

   为使 iSCSI 控制器在遇到网络异常等故障时能更快地进行重试，减少故障恢复时间，请将 **RecoveryTimeout** 参数值设置为 **1**，将 **NoopInterval** 参数值设置为 **1**，并保持 **NoopTimeout** 参数为默认值 **10**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/reduce-recovery-timeout.png)
3. 调整通过 iSCSI 控制器访问的每个 LUN 的队列深度。

   执行以下命令，调整 `HostQDepth` 值为 1024（默认值为 128）：

   `esxcli system module parameters set -m iscsi_vmk -p iscsivmk_HostQDepth=1024`

   执行以下命令确认设置是否成功：

   `esxcfg-module -g iscsi_vmk`
4. 重启 ESXi 主机。

## 第 6 步：回收存储空间

当 ESXi 主机删除或迁移了虚拟机，以及在虚拟机操作系统中删除了文件后，被删除虚拟机关联的磁盘或删除的文件原本占用的存储空间会变成未使用状态。但是，存储端无法主动感知到这些数据已被删除，而仍将为客户端分配这些存储空间。为避免这些未使用空间长期占用 SMTX ZBS 块存储容量，可以通过 UNMAP 命令通知 SMTX ZBS，允许其回收这些未使用空间。SMTX ZBS 收到 UNMAP 命令后，会释放命令指定的未使用 LBAs（逻辑块地址），释放的存储空间可以重新分配，提高存储利用率。

> **说明**：
>
> 该操作仅适用于精简置备的 iSCSI LUN。

请按照如下步骤释放存储空间。

1. 根据释放存储空间的不同场景，执行以下操作在客户端释放存储空间。

   - 在 ESXi 中删除虚拟机时，请选择“**所选虚拟机及其关联的磁盘**”；删除磁盘时，请勾选“**从数据存储删除文件**”。
   - 在虚拟机操作系统中释放存储空间有以下几种情况：

     - 保留虚拟卷但是释放虚拟卷上的所有数据。对于 Linux 虚拟机，执行 `blkdiscard <dev path>` 命令完成此操作，其中 `dev path` 为指定要释放的虚拟卷。
     - 仅释放虚拟卷上不需要的数据。

       对于 Linux 虚拟机，可执行 `fstrim <fs path>` 命令完成此操作，其中 `fs path` 为指定要释放的文件路径；

       对于 Windows 虚拟机，可使用**磁盘优化**功能完成此操作。
     > **说明**：
     >
     > 在开启了空间自动回收的 VMFS6 环境下，单次执行 blkdiscard 或 fstrim 命令仅能释放少量空间，且可能会返回“Input/output error”信息。在此情况下，可多次执行命令直至不再报错以完成空间释放。
2. 通知 SMTX ZBS 释放存储空间。根据 VMFS 数据存储的类型不同，可以使用不同的方法来配置数据存储和虚拟机的空间回收。

   - VMFS6 支持自动回收存储空间，VMFS6 在完成数据删除后会自动通知 SMTX ZBS 释放存储空间。您可以通过选中相应数据存储，在右键菜单中选择**编辑空间回收**来开启自动空间回收功能。
   - VMFS5 只支持手动回收存储空间。在 VMFS5 完成数据删除后，请在 ESXi 主机依次执行 UNMAP 命令 `esxcli storage vmfs extent list` 和 `esxcli storage vmfs unmap -u <vmfs uuid>` 以通知 SMTX ZBS 释放存储空间。
3. 完成空间释放操作后，可在任一节点执行 `zbs-iscsi lun list <target_name>` 命令，通过查看输出结果中的 `Unique Size` 的变化来确认存储空间是否已释放。

   > **说明**：
   >
   > 存储空间的释放是一个渐进的过程，若释放的空间较大，可能需等待一段时间才能使空间完全释放，请您耐心等待。

---

## iSCSI 存储服务 > 回收存储空间

# 回收存储空间

回收存储空间有以下 3 种方式，您可以根据实际需要进行选择。

- **保留 LUN 并释放其存储空间**：使用 UNMAP 命令在客户端释放某个 LUN 对应存储设备的存储空间，但仍保留 LUN。
- **卸载客户端的 LUN 并删除 LUN**：确认某个 LUN 已不再使用后，先从客户端卸载该 LUN 对应的存储设备，再在块存储集群中删除该 LUN。
- **移除客户端的 Target 连接并删除 Target**：确认某个 Target 已不再使用后，先从客户端移除该 Target 的连接，再在块存储集群中删除该 Target。

---

## iSCSI 存储服务 > 回收存储空间 > 保留 LUN 并释放其存储空间

# 保留 LUN 并释放其存储空间

当客户端的文件系统不再需要使用部分存储空间时（如删除文件），这部分空间会变成未使用空间。为避免这些未使用空间长期占用 SMTX ZBS 块存储容量，可以通过 UNMAP 命令通知 SMTX ZBS，允许其回收这些未使用空间。SMTX ZBS 收到 UNMAP 命令后，会释放命令指定的未使用 LBAs（逻辑块地址），释放的存储空间可以重新分配，提高存储利用率。

> **注意**：
>
> - 以下操作仅适用于精简置备的 iSCSI LUN。
> - 若在 LUN 上格式化文件系统时，选择允许文件系统自动进行空间回收（具体操作可参阅对应文件系统的使用指南），则文件系统会自动回收删除文件后释放的空间，您无需执行以下操作。
> - 以下操作将清理 LUN 上的部分或所有数据，LUN 上的数据一旦被清理将无法恢复。

## 在客户端释放存储空间

### Linux 客户端

1. 执行 `ls -l /dev/disk/by-path` 命令，在输出结果中根据要回收的 LUN 的信息查找并记录对应虚拟卷的设备符号。

   **输出示例**

   ```
   lrwxrwxrwx. 1 root root  9 Oct  1 13:00 ip-10.0.18.72:3260-iscsi-iqn.2016-02.com.smartx:system:smartx-test-lun-1 -> ../../sdb
   ```

   其中，`iscsi-iqn.2016-02.com.smartx:system:smartx-test` 表示 iSCSI Target 的 IQN，`lun-1` 表示对应 LUN ID，`sdb` 表示对应虚拟卷的设备符号。
2. 选择释放虚拟卷的部分或所有存储空间。

   - 释放部分存储空间：执行 `fstrim <fs path>` 命令，其中 `<fs path>` 为指定要释放的文件路径。
   - 释放所有存储空间。以下步骤皆以对 `/dev/sdb` 进行操作为例。

     1. 执行 `umount` 命令卸载虚拟卷的所有分区。例如 `sudo umount /dev/sdb1`。
     2. 执行 `blkdiscard <dev path>` 命令释放虚拟卷上的所有存储空间。例如：`blkdiscard /dev/sdb`。

### Windows 客户端

1. 在客户端中执行以下 PowerShell 命令，然后在输出结果中根据磁盘的 `serialnumber` 确认要回收的 LUN 对应的磁盘。客户端所挂载的 LUN 的 UUID 即对应磁盘的 `serialnumber`。

   ```
   get-physicaldisk | select friendlyname,serialnumber,Size
   ```
2. 选择释放磁盘的部分或所有存储空间。

   - 释放部分存储空间：

     1. 选择**开始** > **设置** > **系统** > **存储**，选择**优化驱动器和释放空间**，单击**优化驱动器**。
     2. 在磁盘优化工具中选择需要释放存储空间的磁盘，单击**优化**。系统将开始执行磁盘优化操作。
   - 释放所有存储空间：

     > **注意**：
     >
     > 该操作无法撤回。一旦执行，磁盘中包含的数据将无法找回，请谨慎操作。

     1. 打开**计算机管理**，选择**磁盘管理**。
     2. 将需要释放存储空间的磁盘进行格式化。

### VMware vSphere 集群

1. 登录 vSphere Client，在已挂载要回收的 LUN 的任一 ESXi 主机的管理界面上，单击**配置** > **存储适配器** > **iSCSI Software Adapter** > **设备**，根据需要回收的 LUN 的 UUID （在设备名称的末尾显示）查看对应的 VMFS 数据存储。
2. 在客户端释放存储空间。请根据释放存储空间的具体场景执行相应的操作。

   - 在 ESXi 中删除虚拟机时，请选择**所选虚拟机及其关联的磁盘**，删除磁盘时，请勾选**从数据存储删除文件**。
   - 在虚拟机操作系统中释放存储空间有以下几种情况：

     - 释放 Linux 操作系统的存储空间：请参考 [Linux 客户端操作指导](#linux-%E5%AE%A2%E6%88%B7%E7%AB%AF)。
     - 释放 Windows 操作系统的存储空间：请参考 [Windows 客户端操作指导](#windows-%E5%AE%A2%E6%88%B7%E7%AB%AF)。
     > **说明**：
     >
     > 在开启了空间自动回收的 VMFS6 环境下，单次执行 `blkdiscard` 或 `fstrim` 命令仅能释放少量空间，且可能会返回 “Input/output error” 信息。在此情况下，可多次执行命令直至不再报错以完成空间释放。
3. 通知 SMTX ZBS 回收存储空间。根据 VMFS 数据存储的类型不同，可以使用不同的方法来配置数据存储和虚拟机的空间回收。

   - VMFS6 支持自动回收存储空间，VMFS6 在完成数据删除后会自动通知 SMTX ZBS 回收存储空间。您可以通过选中相应数据存储，在右键菜单中选择**编辑空间回收**来开启自动空间回收功能。
   - VMFS5 只支持手动回收存储空间。在 VMFS5 完成数据删除后，请在 ESXi 主机依次执行 UNMAP 命令 `esxcli storage vmfs extent list` 和 `esxcli storage vmfs unmap -u <vmfs uuid>` 以通知 SMTX ZBS 回收存储空间。

## 在块存储集群确认存储空间是否已回收

在 SMTX ZBS 块存储集群的任一节点执行 `zbs-iscsi lun list <target_name>` 命令，通过查看输出结果中的 `Unique Size` 的变化来确认存储空间是否已回收。

> **说明**：
>
> 存储空间的回收是一个渐进的过程，若回收的空间较大，可能需等待一段时间（通常为若干分钟）才能使空间完全回收，请您耐心等待。

---

## iSCSI 存储服务 > 回收存储空间 > 卸载客户端的 LUN 并删除 LUN

# 卸载客户端的 LUN 并删除 LUN

## 在客户端卸载 LUN 对应的存储设备

您需要在每个已挂载目标 LUN 的客户端上执行卸载操作。

### Linux 客户端操作指导

**注意事项**

在 Linux 客户端上卸载 LUN 对应的虚拟卷并不会释放 LUN 的存储空间。

**操作步骤**

1. 执行 `ls -l /dev/disk/by-path` 命令，然后在如下输出结果中根据要回收的 LUN 的信息查找并记录对应虚拟卷的设备符号。

   **输出示例**

   ```
   lrwxrwxrwx. 1 root root  9 Oct  1 13:00 ip-10.0.18.72:3260-iscsi-iqn.2016-02.com.smartx:system:smartx-test-lun-1 -> ../../sdb
   ```

   其中，`ip-10.0.18.72:3260` 表示 iSCSI Target 的 IP 和端口号，`iscsi-iqn.2016-02.com.smartx:system:smartx-test` 表示 iSCSI Target 的 IQN，`lun-1` 表示对应 LUN 的 id，`sdb` 表示对应虚拟卷的设备符号。
2. 执行 `df -l` 命令，根据要卸载的虚拟卷设备符号查找并记录对应 LUN 的所有文件系统的挂载点。
3. 执行 `umount <mnt point>` 命令，将对应 LUN 的每个分区从客户端卸载，其中 `<mnt point>` 表示每个分区的文件系统的挂载点。
4. （可选）若客户端存在直接使用对应 LUN 的服务，例如 Oracle 的 ASM 服务，请停止该类服务的运行。
5. 检查 `/etc/fstab` 文件中是否已配置对应 LUN 的所有文件系统的自动挂载信息，若已配置，请删除相关配置信息。
6. 执行 `df -l` 命令检查虚拟卷是否已卸载成功。若在输出结果中查找不到对应 LUN 的所有文件系统的挂载点，则表明虚拟卷已卸载成功。
7. 执行 `echo 1 > /sys/block/<device_name>/device/delete` 命令，以通知内核停止使用该 LUN 设备并将其从系统中移除，其中 `<device_name>` 表示要卸载的虚拟卷的设备符号。

### Windows 客户端操作指导

**注意事项**

在 Windows 客户端上删除 LUN 对应的磁盘并不会释放 LUN 的存储空间。

**操作步骤**

1. 在客户端中执行以下 PowerShell 命令，然后在输出结果中根据磁盘的 `serialnumber` 确认要回收的 LUN 对应的磁盘。客户端所挂载的 LUN 的 UUID 即对应磁盘的 `serialnumber`。

   ```
   get-physicaldisk | select friendlyname,serialnumber,Size
   ```
2. 打开 Windows 系统的**计算管理**，选择**磁盘管理**，删除对应磁盘并将其置为离线状态。

### VMware vSphere 集群操作指导

1. 登录 vSphere Client，在已挂载要回收的 LUN 的任一 ESXi 主机的管理界面上，单击**配置** > **存储适配器** > **iSCSI Software Adapter** > **设备**，根据需要回收的 LUN 的 UUID （在设备名称的末尾显示）查看对应的 VMFS 数据存储。
2. 单击需要回收的 VMFS 数据存储，跳转至数据存储的管理界面后，单击**虚拟机**以查看当前数据存储所关联的虚拟机。
3. 删除当前数据存储与虚拟机关联的存储资源。您可以选择直接删除虚拟机或者仅删除虚拟机内使用该数据存储的数据盘。
   > **注意**：
   >
   > 存储资源删除后将无法恢复，请谨慎操作。若您选择保留虚拟机，并且虚拟机的系统盘使用了该数据存储，建议先备份虚拟机或将虚拟机的存储资源克隆至其他 VMFS 数据存储。
4. 确保当前数据存储与虚拟机关联的存储资源已删除后，返回该数据存储的管理界面，单击**操作** > **删除数据存储**。
5. 返回 iSCSI Software Adapter 的**设备**选项卡，对要回收的 LUN 执行**分离**操作。

## 在块存储集群删除 LUN

确认该 LUN 不再使用后，请登录 CloudTower，删除该 LUN。

> **注意**：
>
> 该操作无法撤回。LUN 一旦删除，其中包含的数据将无法找回，请谨慎操作。

---

## iSCSI 存储服务 > 回收存储空间 > 移除客户端的 Target 连接并删除 Target

# 移除客户端的 Target 连接并删除 Target

## 在客户端移除 Target 连接

您需要在每个已连接目标 Target 的客户端上移除 Target 连接。

### Linux 客户端操作指导

1. 在客户端执行 `iscsiadm -m session -P3` 命令以查看当前连接的 Target 的信息及其关联 LUN 的信息。
2. 确保要卸载的 Target 关联的 LUN 对应的虚拟卷均已不再使用并已卸载，可参考 [Linux 客户端操作指导](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_35#linux-%E5%AE%A2%E6%88%B7%E7%AB%AF%E6%93%8D%E4%BD%9C%E6%8C%87%E5%AF%BC)卸载这些虚拟卷。
3. 执行 `iscsiadm -m node -T <your target name> -u` 以从 Target 登出。
4. 执行 `iscsiadm -m node -T <your target name> -o delete` 命令以删除 Target 的记录。

### Windows 客户端操作指导

1. 确保该 Target 所关联的 LUN 对应的磁盘均已不再使用并已删除，可参考 [Windows 客户端操作指导](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_35#windows-%E5%AE%A2%E6%88%B7%E7%AB%AF%E6%93%8D%E4%BD%9C%E6%8C%87%E5%AF%BC)删除这些磁盘。
2. 打开 iSCSI 发起程序，在**目标**选项卡处选择要移除的 Target 并单击**断开连接**。
3. 单击**发现**选项卡并在 Target 门户处移除 Target 所在存储集群的 iSCSI 接入虚拟 IP，然后返回**目标**选项卡并单击**刷新**。

### VMware vSphere 集群操作指导

1. 登录 vSphere Client，在 ESXi 主机界面上，单击**配置** > **存储适配器** > **iSCSI Software Adapter** > **设备**，根据 Target 所关联的所有 LUN 的 UUID （在设备名称的末尾显示）查看对应的 VMFS 数据存储。
2. 确保所有要回收的 LUN 均已从 ESXi 主机上分离。对于不满足要求的 LUN，请参考 [VMware vSphere 集群操作指导](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_35#vmware-vsphere-%E9%9B%86%E7%BE%A4%E6%93%8D%E4%BD%9C%E6%8C%87%E5%AF%BC)执行操作。
3. 单击**静态发现**，然后移除不再使用的 iSCSI Target。

## 在块存储集群删除 Target

1. 确认该 Target 不再使用后，请在 CloudTower 上删除该 Target 关联的 LUN。
2. 删除该 Target。

---

## NVMe 存储服务

# NVMe 存储服务

SMTX ZBS 块存储集群支持客户端通过 NVMe over TCP 和 NVMe over RDMA 协议远程访问其块存储服务。用户可以根据客户端的网络硬件条件选择通过 NVMe over TCP 或者 NVMe over RDMA 协议使用 NVMe 存储服务。

---

## NVMe 存储服务 > 相关概念

# 相关概念

本节介绍了 NVMe-oF 相关概念，如您在配置过程中遇到不熟悉的概念，可在此快速查找对应的详细解释。

## NVMe

NVMe (Non-Volatile Memory Express) 是一种用于服务器访问内部或直连存储的协议，相比于传统的存储访问协议，NVMe 具有高带宽、低延时和低 CPU 使用率的特性，能够提供更快的访问速度，更大限度发挥 SMTX ZBS 块存储的优越性能。

## NVMe-oF

NVMe-oF（NVMe over Fabrics）是 NVMe 协议的扩展，用于支持服务器通过不同的网络传输架构远程访问目标存储。NVMe-oF 支持多种类型的网络传输协议，SMTX ZBS 支持外部客户端通过 NVMe over RDMA 协议和 NVMe over TCP 协议访问集群的块存储服务。

- **NVMe over RDMA**

  NVMe over RDMA 基于 RDMA 协议栈，可绕过操作系统内核，通过网卡直接访问内存数据，从而节省大量 CPU 资源，提高系统的吞吐量，并降低网络通信延时。
- **NVMe over TCP**

  NVMe over TCP 基于传统的 TCP/IP 协议栈，客户端可以通过以太网远程访问存储。NVMe over TCP 对网络硬件没有特殊要求，在标准以太网卡和以太网网络交换机上即可实现部署，无需大量的硬件投资，具有很好的普适性，同时能够提供良好的传输性能。

## NVMe Subsystem

NVMe Subsystem 是逻辑上的存储集合，通过 NVMe 限定名称 (NQN) 标识，一个 NVMe Subsystem 可以包含一个或多个 Namespace。

## NVMe Namespace

NVMe Namespace 类似于存储设备或 LUN，客户端在发现 Namespace 后，将在存储设备列表中显示该 Namespace 的存储设备。

## 接入点分配策略

接入点策略是指 NVMe Namespace 的接入点分配方式，包含继承策略和均衡策略两种。推荐使用继承策略，均衡策略一般用于多个 Namespace 构建 LVM。

- **继承策略**

  在继承策略下，Namespace 会继承客户端的接入点。同一客户端访问的所有 Namespace 使用相同的接入点，而不同客户端尽量使用各自的接入点。继承策略适用于大多数场景，特别是多个客户端访问共享卷的情况。

  该策略下支持两种 Namespace 类型：

  - **卷**：多个客户端通过相同的接入点连接存储。
  - **共享卷**：多个客户端尽量使用不同的接入点连接存储，适用于多个客户端同时访问同一存储资源的场景，如 VMware 主机以存储池方式访问共享卷，或多个 Oracle 主机构建 RAC。
- **均衡策略**

  选择该策略后将不能直接创建 Namespace，需要先创建 Namespace Group，然后在 Namespace Group 中创建 Namespace。Namespace 将会均衡地分布在所有接入点上，同时保证属于同一个 Group 的 Namespace 尽量使用不同的接入点。

  利用此策略，可以使用同一个 Group 中的 Namespace 构建 LVM，单个客户端充分利用多个接入点的处理能力，将 I/O 性能实现最大化。

## 白名单

白名单是一种客户端访问控制机制，用于明确指定被允许访问 NVMe Subsystem 和 NVMe Namespace 的客户端。可通过业务主机和手动配置的方式来配置白名单。

- **使用业务主机配置白名单**

  您可以通过选择业务主机和业务主机组的方式（需提前[创建业务主机和业务主机组](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_183)），来指定可访问 NVMe Subsystem 和 NVMe Namespace 的客户端白名单。

  - **手动选择业务主机和业务主机组**

    手动勾选允许加入白名单的业务主机和业务主机组。若选择业务主机组时，若后续组内新增或删除业务主机时，会自动同步更新白名单。选择的业务主机（含主机组内的业务主机）必须均已配置 NQN 地址。

    NVMe Namespace 的业务主机白名单默认与 NVMe Subsystem 相同，您也可以选择取消与所属 NVMe Subsystem 保持一致，在所属 NVMe Subsystem 白名单的范围内，进一步为 Namespace 选择可访问的业务主机。
  - **自适应**

    开启自适应后，NQN 白名单会自动保持为所包含 NVMe Namespace 的 NQN 白名单的并集，IP 白名单将为**全部允许**。

    在 NVMe Subsystem 启用自适应的情况下，NVMe Namespace 白名单配置方式默认使用业务主机，您可以自行添加允许访问该 Namespace 的业务主机。也可选择手动配置白名单。
- **手动配置白名单**

  手动通过设置 IP 地址和 NQN 来标识可以访问 NVMe Subsystem 和 NVMe Namespace 的客户端。

  > **说明**：
  >
  > - 只有同时属于 IP 白名单和 NQN 白名单的客户端才可以访问 NVMe Subsystem。
  > - 若要访问 NVMe Namespace，客户端必须同时在该 Namespace 的 IQN 白名单以及其所属的 NVMe Subsystem 的 IP 白名单和 NQN 白名单上。

  - **IP 白名单**

    通过 IP 地址标识的允许访问 NVMe Subsystem 的客户端。NVMe Subsystem 的 IP 白名单可设置为**全部禁止**、**允许指定 IP**、**全部允许**，默认为**全部允许**。
  - **NQN 白名单**

    通过 NQN 标识的允许访问 NVMe Namespace 的客户端。

    NVMe Subsystem 的 NQN 白名单可设置为**全部禁止**、**允许指定 NQN**、**全部允许**，**自适应**，默认为**自适应**。
    当选择自适应时，会自动保持为所包含 NVMe Namespace 的 NQN 白名单的并集。

    NVMe Namespace 的 NQN 白名单可设置为**全部禁止**或**允许指定 NQN**。当所属的 NVMe Subsystem 允许全部客户端访问时，Namespace 需要指定 NQN 白名单，仅允许特定的客户端访问或禁止全部客户端访问；当所属的 NVMe Subsystem 禁止全部客户端访问时，指定的 Namespace 的 NQN 白名单将不会生效。

    > **注意**：
    >
    > NQN 白名单一般只应包含一个客户端，若包含多个，可能存在多个客户端并发写导致数据损坏的风险。对于 VMware Datastore 和 Oracle RAC 使用场景，由于客户端保证了多写的数据安全，可以指定多个客户端。

## 存储策略

SMTX ZBS 块存储集群的存储策略包括冗余策略（多副本、纠删码）、置备方式、条带化、常驻缓存模式和数据加密。

### 冗余策略

- **多副本**

  多副本技术是指在多个节点上存放相同数据的多个副本，以保障数据的高可用性。多副本为数据提供了冗余机制，即使某个节点发生故障，其他健康节点依然还有完整的副本，可保证数据正常的 I/O 读写。

  SMTX ZBS 块存储集群支持 2 副本和 3 副本。当集群可提供存储服务的节点数不低于 5 个时，默认为 3 副本，否则默认为 2 副本。对于双活集群，只支持 3 副本。
- **纠删码**

  纠删码（Erasure Coding，EC）是一种数据冗余机制。它通过特定的算法对 K 个原始数据块（Data Block）进行处理，生成 M 个校验块（Parity Block）。在损坏数据块的数量不超过 M 的情况下，可通过纠删码算法，利用 K 个可用的数据块和校验块即可重建出损坏的数据块，实现数据的恢复和容错能力。通过纠删码，即使部分数据丢失，仍然可以恢复完整的数据，能够有效地提高存储系统的可靠性和容量利用率。

  选择纠删码作为冗余策略时，集群中可提供存储服务（至少一个硬盘池存储服务健康且非移除中）的节点数至少 K+M+1。

  > **说明**：
  >
  > 块存储集群需满足如下条件才可使用纠删码：
  >
  > - 可提供存储服务的节点数不小于 4；
  > - 集群为分层存储模式；
  > - 集群未启用双活特性。

### 置备方式

置备方式是一种存储空间分配策略。SMTX ZBS 块存储集群支持厚置备和精简置备两种置备方式。

- **厚置备**

  使用厚置备方式时，在创建 NVMe Namespace 时，ZBS 会立即为 NVMe Namespace 分配所指定的所有空间，即使 NVMe Namespace 实际上仅使用了部分容量，但整个指定空间都会始终被 NVMe Namespace 占用，无法被其他资源所使用。

  由于在创建 NVMe Namespace 时就分配了整个指定的容量，厚置备的 NVMe Namespace 在进行写操作时不会受到动态空间分配的影响，因此可以在某种程度上提供更加稳定的性能，且因存储空间在一开始就已经全部分配，所以不需要频繁地进行动态调整。

  > **说明**：
  >
  > 若 NVMe Subsystem 或 NVMe Namespace 启用了常驻缓存模式，则只支持厚置备方式。
- **精简置备**

  使用精简置备方式时，在创建 NVMe Namespace 时，ZBS 并不立即为 NVMe Namespace 分配整个指定的空间，而是根据需要动态分配，只有在实际写入数据时才会分配实际的存储空间，未写入时不占用存储空间资源。

  由于精简置备的 NVMe Namespace 只在实际需要时才会被分配存储空间，避免了预先分配可能导致空间浪费，提升了空间的利用率，且可以灵活适应一些需求动态变化的业务场景。

### 条带化

条带化（Striping）是指数据分割成大小相同的条带（Stripe），并尽可能将每条数据分别写入到不同硬盘上，以充分利用多个硬盘 I/O 能力的方法。

在 SMTX ZBS 块存储集群中，用户可以对 NVMe Namespace 灵活设置条带数（包括 1、2、4、8，默认为 8），条带化可以充分发挥多硬盘并行工作的优势，条带数越多，并行度越高，尤其在处理顺序 I/O 时性能表现更为出色。条带大小默认为 256 KiB，不可更改。

### 常驻缓存

数据常驻缓存（Volume pining）是块存储集群在分层部署（包括混闪分层部署和全闪分层部署）模式下可使用的一种存储优化策略。

分层部署的集群在默认情况下，NVMe Namespace 中具有较高访问频率的数据将停留在速度更快的缓存层，访问频率较低的数据将下沉至速度相对较慢的数据层。对 NVMe Namespace 启用常驻缓存模式后，Namespace 的数据将始终保留在缓存层，从而获得更稳定的高性能。

## 数据加密

启用数据加密可以对 NVMe Namspace 进行加密保护。在数据写入时，系统将对数据进行加密后存储至物理盘；在数据读取时，系统将先对加密数据进行解密，将解密后的明文数据返回客户端。

> **说明**：
>
> - 若要启用数据加密，请确认在集群设置中已启用了加密功能。具体操作请参考[管理加密功能](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_167)功能。
> - 在使用加密卷的过程中，请确保密钥管理服务器的许可在有效期内。

## I/O 突发

I/O 突发是指在指定的时间段内，系统的 I/O 操作可以短暂地超过预设的 IOPS 上限或带宽上限。这允许系统在应对临时的高负载或需要更快响应时间的情况时可以提供更高的性能，同时也可以通过设置突发上限和持续时间上限进行更精细化的管理。

下图示意了开启 IOPS 限制，并且允许 I/O 突发时可能出现的 IOPS 监控图形。

![](https://cdn.smartx.com/internal-docs/assets/06ea7d56/zbs_administration_guide_017.png)

在 t1 和 t2 时间段内，分别发生了 1 次 I/O 突发。

- t1 持续时长低于设定的持续时间上限：IOPS 可以高于 IOPS 上限，且低于 IOPS 突发上限。
- t2 持续时长高于设定的持续时间上限：当突发流量累计到一定程度时，IOPS 被限制到 IOPS 上限以下。

---

## NVMe 存储服务 > 配置概览

# 配置概览

NVMe 存储服务的配置内容包括：

- 在块存储集群创建 NVMe Subsystem 和 NVMe Namespace。
- 配置使用 NVMe over TCP 或 NVMe over RDMA 协议访问存储的客户端（Linux/VMware vSphere 集群）。

**前提条件**

- 客户端及版本需适配 SMTX ZBS 块存储。适配的客户端及版本请参考《SMTX ZBS 5.7.0 发布说明》的[计算端和存储协议配套说明](/smtxzbs/5.7.0/zbs_release_notes/zbs-release-notes-03#%E8%AE%A1%E7%AE%97%E7%AB%AF%E5%92%8C%E5%AD%98%E5%82%A8%E5%8D%8F%E8%AE%AE%E9%85%8D%E5%A5%97%E8%AF%B4%E6%98%8E)。
- NVMe over RDMA 对网络硬件环境有以下要求：

  - 块存储集群存储节点的接入网卡支持 RDMA 功能。
  - 客户端的接入网卡支持 RDMA 功能，且与存储节点的接⼊⽹络能够互通。
  - 块存储集群存储节点和客户端的接入网络交换机支持基于 L3 DSCP 的 PFC 流量控制或者 Global Pause 流量控制。

---

## NVMe 存储服务 > 创建 NVMe Subsystem 和 Namespace

# 创建 NVMe Subsystem 和 Namespace

## 创建 NVMe Subsystem

1. 在块存储集群的管理界面，单击右上方的**创建**，选择**创建 NVMe Subsystem**。
2. 在弹出的创建页面上，设置 NVMe Subsystem 的名称、描述、接入点分配策略、白名单、存储策略和默认 I/O 限制。具体参数说明请参考[相关概念](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_29)。

   > **说明**：
   >
   > - 在 NVMe Subsystem 设置的副本数、置备方式和是否启用常驻缓存，仅作为该 NVMe Subsystem 内新建 NVMe Namespace 的默认存储策略。您也可以在创建 NVMe Namespace 或编辑 NVMe Namespace 时设置单独的存储策略。
   > - 若需启用常驻缓存模式，请确保已在块存储集群的**设置** > **常驻缓存**界面启用了**允许数据常驻缓存**。
   > - 在 NVMe Subsystem 设置的 I/O 限制仅作为该 NVMe Subsystem 内新建 NVMe Namespace 的默认 I/O 限制选项，而非 NVMe Subsystem 整体的 I/O 限制。
3. 单击**创建**，完成 NVMe Subsystem 的创建。

## 创建 NVMe Namespace

1. 进入 NVMe Subsystem 管理界面，单击右上方的**创建**，选择**创建 Namespace**。
2. 在弹出的创建页面上，设置 Namespace 的名称、容量、ID、所属 Namespace Group,存储策略、访问设置和 I/O 限制。具体参数说明请参考[相关概念](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_29)。

   > **说明**：
   >
   > - 若 NVMe Subsystem 采用均衡策略进行接入点分配，其中的 LUN 需加入 Namespace Group。在创建 Namespace 时，您可以选择已有的 Namespace Group，或新建 Namespace Group 并将 Namespace 加入其中。
   > - 新建的 NVMe Namespace 默认使用所属 NVMe Subsystem 的存储策略和 I/O 限制，您也可以为 Namespace 自定义副本数、常驻缓存模式、NQN 白名单和 I/O 限制，但冗余策略类型和具体的纠删码参数必须与所属 NVMe Subsystem 保持相同，创建后不可更改。
3. 单击**创建**，完成 NVMe Namespace 的创建。

在块存储集群完成 NVMe Subsystem 和 Namespace 的创建后，请继续完成客户端的配置。

---

## NVMe 存储服务 > 配置客户端通过 NVMe over TCP 访问存储

# 配置客户端通过 NVMe over TCP 访问存储

块存储集群支持 Linux 客户端和 VMware vSphere 集群通过 NVMe over TCP 协议访问其块存储服务。

---

## NVMe 存储服务 > 配置客户端通过 NVMe over TCP 访问存储 > 配置 Linux 客户端

# 配置 Linux 客户端

1. 安装 nvme-cli 命令行工具。

   `yum install nvme-cli`
2. 加载 nvme\_tcp 驱动：

   ```
   [root@57-71 ~]# modprobe nvme_tcp
   [root@57-71 ~]# lsmod | grep nvme
   nvme_tcp               32768  0
   nvme_fabrics           24576  1 nvme_tcp
   nvme_core             110592  2 nvme_tcp,nvme_fabrics
   ```

   若希望客户端在启动时自动加载 nvme\_tcp 驱动，可执行如下命令：

   `echo nvme_tcp | sudo tee /etc/modules-load.d/nvme_tcp.conf`
3. 确认客户端操作系统的 NVMe 驱动支持 Multipath 功能，以便能够通过多路径访问来保证高可用。

   ```
   [root@57-71 ~]# cat /sys/module/nvme_core/parameters/multipath
   Y
   ```

   若 NVMe 驱动支持 Multipath 功能，但是默认值为 `N`，可进行以下配置，配置完成后重启系统，再次输入以上命令，确认输出为 `Y`。

   1. 创建 `/etc/modprobe.d/nvme_core.conf` 配置文件并配置 `options nvme_core multipath=Y`。

      ```
      $ cat /etc/modprobe.d/nvme_core.conf
      options nvme_core multipath=Y
      ```
   2. 重建 `initramfs` 文件系统。

      ```
      dracut --force --verbose
      ```
   > **说明**
   >
   > - Linux 的 NVMe 驱动从 4.15.18 版本开始支持 Multipath 功能。当前已验证支持的版本包括：CentOS 8.4、Ubuntu 20.04.2、openSUSE Leap 15.3。
4. 确认客户端的 NQN。

   ```
   [root@57-71 ~]# cat /etc/nvme/hostnqn
   nqn.2014-08.org.nvmexpress:uuid:82729b6b-4541-41a9-a75b-7bced1d407bd
   ```

   > **说明**
   >
   > - 客户端要发现和连接 Subsystem，需保证其 NQN 在 Susbystem 的 NQN 白名单内，且 IP 在 Subsystem 的 IP 白名单内。
   > - 客户端要发现和挂载 Namespace，除需满足上述连接 Susbystem 的条件，客户端 NQN 也需在 Namespace 的 NQN 白名单内。
   > - 对于克隆生成的 Linux 系统，其 NQN 与源系统的 NQN 相同。为避免连接异常，请执行 `nvme gen-hostnqn` 命令生成新的 NQN，并编辑 `/etc/nvme/hostnqn` 文件，用新的 NQN 覆盖原来的 NQN。
5. 发现存储。 `NVMF Access IP` 为各节点的接入 IP。可输入任一节点的 IP 地址，返回的发现结果相同。

   `nvme discover -t tcp -a <NVMF Access IP> -s 8009`
6. 连接存储。对于同一个 `NQN-name`，需要多次执行该命令，确保连接到每个节点，以便能够通过多路径访问存储。

   `nvme connect -t tcp -a <NVMF Access IP> -n <NQN-name> -l <Ctrl Loss Timeout> -s 8009`

   > **说明**
   >
   > `Ctrl Loss Timeout` 为客户端重连存储的超时时间。当客户端与存储之间的连接中断后，客户端会自动重新连接存储，若在超时时间内未能重连成功，则会停止自动重连，此时，需手动连接存储。默认的会话超时时间为 600（秒），推荐设置为 604800（秒）。
7. 确认 `discard_max_bytes` 值。若该值大于 16 MB（即 `16777216`），会触发 I/O 错误，建议将其值修改为 1 MB，即 `1048576`。

   **示例**：

   ```
   root@centos8:/root # cd /sys/block/nvme4n1/queue/
   root@centos8:/sys/block/nvme4n1/queue # grep . -r | grep discard
   grep: wbt_lat_usec: Invalid argument
   discard_zeroes_data:0
   discard_max_bytes:2199023255040
   discard_max_hw_bytes:2199023255040
   max_discard_segments:256
   discard_granularity:512
   root@centos8:/sys/block/nvme4n1/queue # echo 1048576 > discard_max_bytes
   root@centos8:/sys/block/nvme4n1/queue # grep . -r | grep discard
   grep: wbt_lat_usec: Invalid argument
   discard_zeroes_data:0
   discard_max_bytes:1048576
   discard_max_hw_bytes:2199023255040
   max_discard_segments:256
   discard_granularity:512
   ```
8. 查看连接状态。

   `nvme list-subsys`

配置示例如下：

```
[root@57-71 ~]# nvme discover -t tcp -a 10.0.58.75 -s 8009
Discovery Log Number of Records 34, Generation counter 138
=====Discovery Log Entry 0======
trtype:  tcp
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  0
trsvcid: 8009
subnqn:  nqn.2020-12.com.smartx:system:lp-sub1
traddr:  10.0.68.211
sectype: none

[root@57-71 ~]# nvme connect -t tcp -a 10.0.58.75 -s 8009 -n nqn.2020-12.com.smartx:system:sub1 -l 604800
[root@57-71 ~]# nvme connect -t tcp -a 10.0.58.76 -s 8009 -n nqn.2020-12.com.smartx:system:sub1 -l 604800
[root@57-71 ~]# nvme connect -t tcp -a 10.0.58.77 -s 8009 -n nqn.2020-12.com.smartx:system:sub1 -l 604800

[root@57-71 ~]# nvme list-subsys
nvme-subsys11 - NQN=nqn.2020-12.com.smartx:system:sub1
\
 +- nvme11 tcp traddr=10.0.58.75 trsvcid=8009 live
 +- nvme12 tcp traddr=10.0.58.76 trsvcid=8009 live
 +- nvme13 tcp traddr=10.0.58.77 trsvcid=8009 live

[root@57-71 ~]# lsblk | grep nvme
nvme11n1 259:115  0    10G  0 disk
nvme11n2 259:117  0    10G  0 disk

[root@57-71 ~]# nvme list-subsys /dev/nvme11n1
nvme-subsys11 - NQN=nqn.2020-12.com.smartx:system:sub1
\
 +- nvme11 tcp traddr=10.0.58.75 trsvcid=8009 live non-optimized
 +- nvme12 tcp traddr=10.0.58.76 trsvcid=8009 live non-optimized
 +- nvme13 tcp traddr=10.0.58.77 trsvcid=8009 live optimized
```

> **说明**：
>
> - 若客户端的 Linux 发行版的内核版本低于 5.16.16，在和节点失去连接后，可能出现 Linux NVMe 驱动重连无法成功的问题，需要重启计算节点并重连存储。
> - 所有版本的 Linux 客户端在重启后默认不会自动重连存储。若需重启后自动重连，请根据您的 Linux 客户端版本是否提供开机自动重连存储的服务执行操作。
>   - 若提供，请执行以下命令启用该服务。
>
>     ```
>     systemctl enable nvmf-autoconnect.service
>     systemctl start nvmf-autoconnect.service
>     ```
>   - 若未提供，请执行以下命令配置开机连接 NVMe 控制器。
>
>     ```
>     cd /etc/rc.d
>     cp rc.local rc.local.bak
>     cat <<EOF >> ./rc.local
>     # 将如下内容输入到 ./rc.local 文件中。
>     modprobe nvme_tcp
>     nvme connect -t tcp -a <Access IP> -n <NQN Name> -s 8009 # 对于同一个 NQN Name，需要多次输入该命令，确保连接到每个节点，以便能够通过多路径访问存储。
>     # EOF 表示输入结束
>     EOF
>
>     chmod ugo+x /etc/rc.d/rc.local
>     ```

---

## NVMe 存储服务 > 配置客户端通过 NVMe over TCP 访问存储 > 配置 VMware vSphere 集群

# 配置 VMware vSphere 集群

本节介绍如何配置远端 VMware vSphere 集群通过 NVMe over TCP 协议挂载 SMTX ZBS 块存储作为数据存储（Datastore）使用。

**前提条件**

VMware vSphere 集群中需要访问 SMTX ZBS 块存储的 ESXi 主机配置了可以连通集群接入网络的地址。

## 第 1 步：为 ESXi 主机配置与块存储集群连通的接入网络

ESXi 主机既可以通过单一网口连接块存储集群，也可以采用多网口配置以增强可靠性和性能。使用多网口配置时，当某个网口发生故障时，仍可保证连接不中断，同时还可提供更高的带宽。对于多网口配置，本文将以双网口为例进行说明。

### ESXi 主机通过单网口连接块存储集群

1. 使用 VMware vSphere Web Client 登录到 vCenter Server，浏览到 ESXi 主机。
2. 在 ESXi 主机界面，选择**配置**>**网络**>**虚拟交换机**>**添加网络**，在弹出的**添加网络**界面中，选择 **VMkernel 网络适配器**。单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/installationguide_032.png)
3. 进入**选择目标设备**。选择**新建标准交换机**。
4. 创建标准交换机。单击添加按钮，选择物理网络适配器分配给新创建的交换机。

   > **说明**：
   >
   > 由于接入网络要求必须是 10Gb 及以上的以太网，因此可根据网络适配器**状态**一栏显示的适配器的速率信息，选择 10000 Mb 及以上的网络适配器。
5. 设置端口属性。在**端口属性**选项页面，可用服务中勾选 **NVMe over TCP**，单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/add-nvmf-tcp-vmkernel.png)
6. 设置 IPv4 参数。选择**使用静态 IPv4 设置**，在**IPv4 地址**中输入 ESXi 主机的接入 IP 并设置子网掩码。

   若接入网络有明确的子网规划（例如接入网络自身存在网关），则按照接入网络的实际子网掩码配置。若接入网络未配置网关，确保配置的子网掩码可保证 ESXI 接入 IP 和 SMTX ZBS 块存储集群的接入 IP 处于同一子网即可。
7. 完成配置后，在 ESXi 上 Ping 块存储集群的接入地址，确认网络可以正常连接。

### ESXi 主机通过双网口连接块存储集群

1. 在 ESXi 主机界面，选择**配置**>**网络**>**虚拟交换机**>**添加网络**，在弹出的**添加网络**界面中，选择 **VMkernel 网络适配器**。单击 **NEXT**

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/installationguide_032.png)
2. 进入**选择目标设备**。选择**新建标准交换机**。
3. 创建标准交换机。单击**添加**按钮，选择物理网络适配器分配给新创建的交换机。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image11.png)

   > **说明**：
   >
   > 由于接入网络要求必须是 10Gb 及以上的以太网，因此可根据网络适配器**状态**一栏显示的适配器的速率信息，选择 10000 Mb 及以上的网络适配器。
4. 设置端口属性。在端口属性选项页面，可用服务中勾选 **NVMe over TCP**，单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/add-nvmf-tcp-vmkernel.png)
5. 设置 IPv4 参数。选择**使用静态 IPv4 设置**，在**IPv4 地址**中输入 ESXi 主机的接入 IP 1 并设置子网掩码。

   若接入网络有明确的子网规划（例如接入网络自身存在网关），则按照接入网络的实际子网掩码配置。若接入网络未配置网关，确保配置的子网掩码可保证 ESXI 接入 IP 和 SMTX ZBS 块存储集群的接入 IP 处于同一子网即可。
6. 完成上述配置后，请重新进入 ESXi 主机界面，选择**配置**>**网络**>**虚拟交换机**>**添加网络**，在弹出的**添加网络**界面中，选择 **VMkernel 网络适配器**。单击 **NEXT**。
7. 进入**选择目标设备**。选择**现有标准交换机**，并选择步骤 **3** 中已创建的标准交换机。单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image12.png)
8. 设置端口属性。在**端口属性**选项页面，可用服务中勾选 **NVMe over TCP**，单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/add-nvmf-tcp-vmkernel.png)
9. 设置 IPv4 参数。选择**使用静态 IPv4 设置**，在**IPv4 地址**中输入 ESXi 主机的接入 IP 2 并设置子网掩码。请确保接入 IP 2 和接入 IP 1 在同一子网。
10. 设置 VMKernel 网络适配器的故障切换顺序。选择已创建的标准交换机，依次编辑其上的 VMKernel 网络适配器，在**绑定和故障切换** > **故障切换顺序**中，勾选**替代**，仅指定一个物理网络适配器作为活动适配器，并将另一个物理网络适配器移至未用的适配器列表。确保每个 VMkernel 适配器都绑定在不同的活动适配器上，以实现网络冗余与高可用性。

    ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image13.png)

    ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image14.png)
11. 完成配置后，在 ESXi 主机上 Ping 块存储集群的接入地址，确认网络可以正常连接。

## 第 2 步：配置 VMware vSphere 集群支持 NVMe over TCP

1. 为每台 ESXi 主机安装 NVMe 软件适配器。依次单击**配置**>**存储适配器**>**添加软件适配器**，在添加界面选择**添加软件 NVMe over TCP 适配器**，并选择上一步骤中标准交换机使用的物理网络适配器。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/nvmf-tcp-software-adapter.png)

   > **说明**：
   >
   > 若使用双网口连接块存储集群，请为每一个 vmnic 均添加对应的软件 NVMe over TCP 适配器。
2. 设置 ESXi 主机的 hostnqn。将 vmknvme 驱动参数设置为 `vmknvme_hostnqn_format=0`，重启后将以 UUID 格式生成 hostnqn。

   ```
   $ esxcli system module parameters set -m vmknvme -p vmknvme_hostnqn_format=0
   $ reboot
   $ esxcli nvme info get
   Host NQN:
   nqn.2014-08.org.nvmexpress:uuid:61277a96-a5c8-054c-f93c-b8599f2e5e08
   ```

## 第 3 步：配置 NVMe Subsystem 作为数据存储（Datastore）使用

1. 在 ESXi 的存储适配器上添加 NVMe Subsystem。依次单击**存储适配器**> **VMware NVME over TCP 存储适配器**>**控制器**>**添加控制器**，选择**手动**方式，依次输入子系统 NQN、块存储集群任一节点的接入 IP 和 8009 端口，并设置**保持活动超时**为 5 秒。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/add-nvmf-tcp-software-adapter.png)

   > **说明**：
   >
   > **自动**方式默认**保持活动超时**的时长为 60 秒，在故障切换时会产生较长时间的 I/O 中断，因此不建议使用。
2. 重复步骤 1，为每个节点添加接入 IP 的控制器，以便使用 Multipath。
3. 单击**重新扫描适配器**。扫描完成后可以在**设备**中发现块存储集群的 Namespace。
4. 单击**重新扫描存储**，重新扫描主机上的所有存储适配器以发现新添加的存储设备和/或 VMFS 卷。
5. （可选）若采用双网口连接块存储，请对两个 NVMe over TCP 存储适配器均重复以上步骤。
6. 单击**存储设备**，根据 NVMe TCP Disk 的 EUI（根据 ZBS 的 Namespace UUID 生成，去掉了所有 `-` 连接符）找到对应的设备，单击**属性**>**多路径策略**>**操作**>**编辑多路径**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/edit-nvmf-tcp-multipath-policy-1.png)
7. 选择**路径选择策略**为**固定**，保存设置。该配置能保证 ESXi 主机每次只会通过单个路径访问 ZBS 存储。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/edit-nvmf-tcp-multipath-policy-2.png)
8. 在每一台需要访问 ZBS 的 ESXi 主机上重复上述步骤。
9. 前往**数据存储**，创建基于该 Namespace 的 VMware 数据存储。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/create-datastore-with-zbs-subsystem-1.png)

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/create-datastore-with-zbs-tcp-subsystem-2.png)

   选择较高版本的 VMFS。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/create-datastore-with-zbs-subsystem-3.png)

## 第 4 步：挂载 VMware 数据存储到块存储集群中的其他节点

VMware 数据存储（Datastore）建立一次即可，块存储集群中的其他节点挂载该数据存储后即可使用。

---

## NVMe 存储服务 > 配置客户端通过 NVMe over RDMA 访问存储

# 配置客户端通过 NVMe over RDMA 访问存储

SMTX ZBS 块存储集群支持 Linux 客户端和 VMware vSphere 集群通过 NVMe over RDMA 协议访问其块存储服务。

---

## NVMe 存储服务 > 配置客户端通过 NVMe over RDMA 访问存储 > 配置 Linux 客户端

# 配置 Linux 客户端

## 连接存储

1. 安装 nvme-cli 命令行工具。

   `yum install nvme-cli`
2. 加载 nvme\_rdma 驱动：

   ```
   [root@57-71 ~]# modprobe nvme_rdma
   [root@57-71 ~]# lsmod | grep nvme_rdma
   nvme_rdma              45056  0
   nvme_fabrics           24576  1 nvme_rdma
   nvme_core             114688  5 nvme_rdma,nvme_fabrics
   rdma_cm               110592  2 nvme_rdma,rdma_ucm
   ib_core               421888  9 rdma_cm,ib_ipoib,nvme_rdma,iw_cm,ib_umad,rdma_ucm,ib_uverbs,mlx5_ib,ib_cm
   mlx_compat             16384  15 rdma_cm,ib_ipoib,mlxdevm,nvme_rdma,iw_cm,nvme_core,auxiliary,nvme_fabrics,ib_umad,ib_core,  
   rdma_ucm,ib_uverbs,mlx5_ib,ib_cm,mlx5_core
   ```

   若希望客户端在启动时自动加载 nvme\_rdma 驱动，可执行如下命令：

   `echo nvme_rdma | sudo tee /etc/modules-load.d/nvme_rdma.conf`
3. 确认客户端操作系统的 NVMe 驱动支持 Multipath 功能，以便能够通过多路径访问来保证高可用。

   ```
   [root@57-71 ~]# cat /sys/module/nvme_core/parameters/multipath
   Y
   ```

   若 NVMe 驱动支持 Multipath 功能，但是默认值为 `N`，可进行以下配置，配置完成后重启系统，再次输入以上命令，确认输出为 `Y`。

   1. 创建 `/etc/modprobe.d/nvme_core.conf` 配置文件并配置 `options nvme_core multipath=Y`。

      ```
      $ cat /etc/modprobe.d/nvme_core.conf
      options nvme_core multipath=Y
      ```
   2. 重建 `initramfs` 文件系统。

      ```
      dracut --force --verbose
      ```
   > **说明**
   >
   > - Linux 的 NVMe 驱动从 4.15.18 版本开始支持 Multipath 功能。当前已验证支持的版本包括：CentOS 8.4、Ubuntu 20.04.2、openSUSE Leap 15.3。
4. 确认客户端的 NQN。

   ```
   [root@57-71 ~]# cat /etc/nvme/hostnqn
   nqn.2014-08.org.nvmexpress:uuid:82729b6b-4541-41a9-a75b-7bced1d407bd
   ```

   > **说明**
   >
   > - 客户端要发现和连接 Subsystem，需保证其 NQN 在 Susbystem 的 NQN 白名单内，且 IP 在 Subsystem 的 IP 白名单内。
   > - 客户端要发现和挂载 Namespace，除需满足上述连接 Susbystem 的条件，客户端 NQN 也需在 Namespace 的 NQN 白名单内。
   > - 对于克隆生成的 Linux 系统，其 NQN 与源系统的 NQN 相同。为避免连接异常，请执行 `nvme gen-hostnqn` 命令生成新的 NQN，并编辑 `/etc/nvme/hostnqn` 文件，用新的 NQN 覆盖原来的 NQN。
5. 发现存储。 `NVMF Access IP` 为各节点的接入 IP。可输入任一节点的 IP 地址，返回的发现结果相同。

   `nvme discover -t rdma -a <NVMF Access IP> -s 4420`
6. 连接存储。对于同一个 `NQN-name`，需要多次执行该命令，确保连接到每个节点，以便能够通过多路径访问存储。

   `nvme connect -t rdma -a <NVMF Access IP> -n <NQN-name> -l <Ctrl Loss Timeout>`

   > **说明**
   >
   > `Ctrl Loss Timeout` 为客户端重连存储的超时时间。当客户端与存储之间的连接中断后，客户端会自动重新连接存储，若在超时时间内未能重连成功，则会停止自动重连，此时，需手动连接存储。默认的会话超时时间为 600（秒），推荐设置为 604800（秒）。
7. 确认 `discard_max_bytes` 值。若该值大于 16 MB（即 `16777216`），会触发 I/O 错误，建议将其值修改为 1 MB，即 `1048576`。

   **示例**：

   ```
   root@centos8:/root # cd /sys/block/nvme4n1/queue/
   root@centos8:/sys/block/nvme4n1/queue # grep . -r | grep discard
   grep: wbt_lat_usec: Invalid argument
   discard_zeroes_data:0
   discard_max_bytes:2199023255040
   discard_max_hw_bytes:2199023255040
   max_discard_segments:256
   discard_granularity:512
   root@centos8:/sys/block/nvme4n1/queue # echo 1048576 > discard_max_bytes
   root@centos8:/sys/block/nvme4n1/queue # grep . -r | grep discard
   grep: wbt_lat_usec: Invalid argument
   discard_zeroes_data:0
   discard_max_bytes:1048576
   discard_max_hw_bytes:2199023255040
   max_discard_segments:256
   discard_granularity:512
   ```
8. 查看连接状态。

   `nvme list-subsys`

配置示例如下：

```
[root@57-71 ~]# nvme discover -t rdma -a 10.0.58.75 -s 4420
Discovery Log Number of Records 58, Generation counter 192
=====Discovery Log Entry 0======
trtype:  rdma
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  25
trsvcid: 4420
subnqn:  nqn.2020-12.com.smartx:system:sub1
traddr:  10.0.58.75
rdma_prtype: not specified
rdma_qptype: connected
rdma_cms:    rdma-cm
rdma_pkey: 0x0000

[root@57-71 ~]# nvme connect -t rdma -a 10.0.58.75 -s 4420 -n nqn.2020-12.com.smartx:system:sub1 -l 604800
[root@57-71 ~]# nvme connect -t rdma -a 10.0.58.76 -s 4420 -n nqn.2020-12.com.smartx:system:sub1 -l 604800
[root@57-71 ~]# nvme connect -t rdma -a 10.0.58.77 -s 4420 -n nqn.2020-12.com.smartx:system:sub1 -l 604800

[root@57-71 ~]# nvme list-subsys
nvme-subsys11 - NQN=nqn.2020-12.com.smartx:system:sub1
\
 +- nvme11 rdma traddr=10.0.58.75 trsvcid=4420 live
 +- nvme12 rdma traddr=10.0.58.76 trsvcid=4420 live
 +- nvme13 rdma traddr=10.0.58.77 trsvcid=4420 live

[root@57-71 ~]# lsblk | grep nvme
nvme11n1 259:115  0    10G  0 disk
nvme11n2 259:117  0    10G  0 disk

[root@57-71 ~]# nvme list-subsys /dev/nvme11n1
nvme-subsys11 - NQN=nqn.2020-12.com.smartx:system:sub1
\
 +- nvme11 rdma traddr=10.0.58.75 trsvcid=4420 live non-optimized
 +- nvme12 rdma traddr=10.0.58.76 trsvcid=4420 live non-optimized
 +- nvme13 rdma traddr=10.0.58.77 trsvcid=4420 live optimized
```

> **说明**：
>
> - 若客户端的 Linux 发行版的内核版本低于 5.16.16，在和节点失去连接后，可能出现 Linux NVMe 驱动重连无法成功的问题，需要重启计算节点并重连存储。
> - 所有版本的 Linux 客户端在重启后默认不会自动重连存储。若需重启后自动重连，请根据您的 Linux 客户端版本是否提供开机自动重连存储的服务执行操作。
>   - 若提供，请执行以下命令启用该服务。
>
>     ```
>     systemctl enable nvmf-autoconnect.service
>     systemctl start nvmf-autoconnect.service
>     ```
>   - 若未提供，请执行以下命令配置开机连接 NVMe 控制器。
>
>     ```
>     cd /etc/rc.d
>     cp rc.local rc.local.bak
>     cat <<EOF >> ./rc.local
>     # 将如下内容输入到 ./rc.local 文件中。
>     modprobe mlx5_core
>     modprobe nvme_rdma
>     nvme connect -t rdma -a <Access IP> -n <NQN Name> -s 4420
>     # EOF 表示输入结束
>     EOF
>
>     chmod ugo+x /etc/rc.d/rc.local
>     ```

## 配置流量控制

为了保证性能，客户端和存储端接入网络交换机需配置相同的流量控制方式。可配置基于 L3 DSCP 的 PFC 流量控制和基于 Global Pause 的流量控制，但推荐使用基于 L3 DSCP 的 PFC 流量控制。

### 在交换机配置（以 Mellanox Switch 为例）

- **基于 L3 DSCP 的 PFC 流量控制（推荐配置）**

  1. 将 RoCE 的流量类型设置为 3 并开启 ECN，以便启用 DCQCN。将 ECN 的最低和最高触发阈值都设置为 3000 KB。

     ```
     switch > enable
     switch # configure terminal
     switch (config) # interface ethernet 1/1-1/2 traffic-class 3 congestion-control ecn minimum-absolute 3000 maximum-absolute 3000
     ```
  2. 设置 QoS trust mode 为 L3（DSCP）。

     `switch (config) # interface ethernet 1/1-1/2 qos trust L3`
  3. 将交换机的 PFC 在 priority 3 上开启。

     ```
     switch (config) # dcb priority-flow-control enable force
     switch (config) # dcb priority-flow-control priority 3 enable
     switch (config) # interface ethernet 1/1-1/2 dcb priority-flow-control mode on force
     switch (config) # interface ethernet 1/1-1/2 pfc-wd
     ```
  4. 验证 PFC 是否已开启，确认后保存配置。

     ```
     switch (config) # show dcb priority-flow-control

     PFC: enabled
     Priority Enabled List: 3
     Priority Disabled List: 0 1 2 4 5 6 7

     -------------------------------------------------
     Interface        PFC admin        PFC oper
     -------------------------------------------------
     Eth1/1           Auto             Enabled
     Eth1/2           Auto             Enabled
     ......

     switch (config) # configuration write
     ```
- **基于 Global Pause 流量控制**

  设置 RDMA 网卡所连交换机端口的 `flowcontrol` 为 `on`，验证并保存配置。

  ```
  Mellanox Switch
  switch > enable
  switch # configure terminal
  switch (config) #
  switch (config) # interface ethernet 1/1-1/2 flowcontrol send on force
  switch (config) # interface ethernet 1/1-1/2 flowcontrol receive on force
  switch (config) # show interfaces ethernet 1/1 | include Flow-control
  Flow-control                     : receive on send on
  switch (config) # show interfaces ethernet 1/2 | include Flow-control
  Flow-control                     : receive on send on
  switch (config) # configuration write
  ```

### 在 Linux 客户端配置 (以 Mellanox RDMA 网卡为例)

1. 根据 Linux 的版本，建议在 Mellanox 官⽹[下载 OFED 驱动最新的 .tgz 安装包](https://www.mellanox.com/products/infiniband-drivers/linux/mlnx_ofed)。此处以 CentOS 8.4 为例：

![](https://cdn.smartx.com/internal-docs/assets/c577f847/download_ofed_driver.png)

2. 解压安装包后，执行以下命令安装驱动。安装完毕后请重启 Linux 客户端。

`./mlnxofedinstall --with-nvmf`

> **说明**：
>
> - 根据 Linux 版本的不同，在安装驱动过程可能会提示系统缺少一些必需的软件包，请根据界面指引安装这些软件包。具体的解决方法请参考 Mellanox 官⽹的 [Installation Related Issues](https://docs.mellanox.com/display/MLNXOFEDv543100/Installation+Related+Issues)。
> - MLNX\_OFED 驱动 5.5-1.0.3.2 版本会造成 NVMe over RDMA 连接发生异常，建议使用其他版本的驱动。

3. 确定客户端的接入网卡。执行 `ibdev2netdev` 命令查看网卡与 RDMA 设备的对应关系，示例输出如下：

   ```
   rocexb8cef603001313d4 port 1 ==> enp1s0f0 (Up)
   rocexb8cef603001313d5 port 1 ==> enp1s0f1 (Up)
   rocexb83fd2030091f37a port 1 ==> bond0 (Up)
   ```

   - 若接入网卡为 enp1s0f1，则后续流控配置命令中的 `$netdev` 和 `$ibdev_name` 参数分别为：

     - `$netdev` = `enp1s0f1`
     - `$ibdev_name` = `rocexb8cef603001313d5`
   - 若接入网卡使用 RDMA 多网口绑定（如 bond0），请继续执行命令 `cat /proc/net/bonding/bond0 | grep "Slave Interface"`确认子接口。示例输出如下：

     ```
     Slave Interface: enp152s0f0
     Slave Interface: enp152s0f1
     ```

     则后续流控配置命令中的 `$netdev` 和 `$ibdev_name` 参数分别为：

     - `$netdev` = `enp152s0f0`, `enp152s0f1`（每个子接口需分别配置）
     - `$ibdev_name` = `rocexb83fd2030091f37a`
4. 配置流量控制。

   - **基于 L3 DSCP 的 PFC 流量控制（推荐配置）**

     ```
     $ mlnx_qos -i $netdev --trust dscp
     $ mlnx_qos -i $netdev --pfc 0,0,0,1,0,0,0,0
     $ echo 106 > /sys/class/infiniband/$ibdev_name/tc/1/traffic_class
     ```
   - **基于 Global Pause 流量控制**

     ```
     ethtool -A $netdev tx on
     ethtool -A $netdev rx on
     ```
5. 配置持久化。为保证配置在系统重启后仍然生效，可按以下步骤操作：

   1. 新建脚本 `/usr/local/bin/set_qos_for_rdma.sh`，以 `#!/bin/bash` 作为脚本第一行，再加入前述的流控配置命令。
   2. 在 /etc/systemd/system/ 目录中新建文件 `set_qos_for_rdma.service`，内容如下：

      ```
      [Unit]
      Description=Set qos for rdma at startup
      After=network.target

      [Service]
      Type=oneshot
      ExecStart=/usr/local/bin/set_qos_for_rdma.sh

      [Install]
      WantedBy=multi-user.target
      ```
   3. 执行以下命令，在系统启动时运行 `set_qos_for_rdma` 服务。

      ```
      sudo systemctl daemon-reload
      sudo systemctl start set_qos_for_rdma.service
      sudo systemctl status set_qos_for_rdma.service
      sudo systemctl enable set_qos_for_rdma.service
      ```

---

## NVMe 存储服务 > 配置客户端通过 NVMe over RDMA 访问存储 > 配置 VMware vSphere 集群

# 配置 VMware vSphere 集群

本文以 VMware 7.0U3C 为例，介绍如何配置远端 VMware vSphere 集群挂载 SMTX ZBS 块存储作为数据存储（Datastore）使用。

**前提条件**

VMware vSphere 集群中需要访问 SMTX ZBS 块存储的 ESXi 主机配置了可以连通块存储集群接入网络的地址。

## 第 1 步：为 ESXi 主机配置与块存储集群连通的接入网络

ESXi 主机既可以通过单一网口连接块存储集群，也可以采用多网口配置以增强可靠性和性能。使用多网口配置时，当某个网口发生故障时，仍可保证连接不中断，同时还可提供更高的带宽。对于多网口配置，本文将以双网口为例进行说明。

### ESXi 主机通过单网口连接块存储集群

1. 使用 VMware vSphere Web Client 登录到 vCenter Server，浏览到 ESXi 主机。
2. 在 ESXi 主机界面，选择**配置**>**网络**>**虚拟交换机**>**添加网络**，在弹出的**添加网络**界面中，选择 **VMkernel 网络适配器**。单击 **NEXT**

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/installationguide_032.png)
3. 进入**选择目标设备**。选择**新建标准交换机**。
4. 创建标准交换机。单击**添加**按钮，选择支持 RDMA 的物理网络适配器分配给新创建的交换机。

   > **说明**：
   >
   > 由于接入网络要求必须是 10Gb 及以上的以太网，因此可根据网络适配器**状态**一栏显示的适配器的速率信息，选择 10000 Mb 及以上的网络适配器。
5. 设置端口属性。在**端口属性**选项页面，可用服务中勾选 **NVMe over RDMA**，单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/add-nvmf-rdma-vmkernel.png)

   > **说明**：
   >
   > 在 VMware 7.0U2 版本的可用服务中无 **NVMe over RDMA** 选项，无需进行此项设置。
6. 设置 IPv4 参数。选择**使用静态 IPv4 设置**，在**IPv4 地址**中输入 ESXi 主机的接入 IP 并设置子网掩码。

   若接入网络有明确的子网规划（例如接入网络自身存在网关），则按照接入网络的实际子网掩码配置。若接入网络未配置网关，确保配置的子网掩码可保证 ESXI 接入 IP 和 SMTX ZBS 块存储集群的接入 IP 处于同一子网即可。
7. 完成配置后，在 ESXi 上 Ping 块存储集群的接入地址，确认网络可以正常连接。

### ESXi 主机通过双网口连接块存储集群

1. 在 ESXi 主机界面，选择**配置**>**网络**>**虚拟交换机**>**添加网络**，在弹出的**添加网络**界面中，选择 **VMkernel 网络适配器**。单击 **NEXT**

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/installationguide_032.png)
2. 进入**选择目标设备**。选择**新建标准交换机**。
3. 创建标准交换机。单击**添加**按钮，选择支持 RDMA 的物理网络适配器分配给新创建的交换机。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image11.png)

   > **说明**：
   >
   > 由于接入网络要求必须是 10Gb 及以上的以太网，因此可根据网络适配器**状态**一栏显示的适配器的速率信息，选择 10000 Mb 及以上的网络适配器。
4. 设置端口属性。在端口属性选项页面，可用服务中勾选 **NVMe over RDMA**，单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/add-nvmf-rdma-vmkernel.png)

   > **说明**：
   >
   > 在 VMware 7.0U2 版本的可用服务中无 **NVMe over RDMA** 选项，无需进行此项设置。
5. 设置 IPv4 参数。选择**使用静态 IPv4 设置**，在**IPv4 地址**中输入 ESXi 主机的接入 IP 1 并设置子网掩码。

   若接入网络有明确的子网规划（例如接入网络自身存在网关），则按照接入网络的实际子网掩码配置。若接入网络未配置网关，确保配置的子网掩码可保证 ESXI 接入 IP 和 SMTX ZBS 块存储集群的接入 IP 处于同一子网即可。
6. 完成上述配置后，请重新进入 ESXi 主机界面，选择**配置**>**网络**>**虚拟交换机**>**添加网络**，在弹出的**添加网络**界面中，选择 **VMkernel 网络适配器**。单击 **NEXT**。
7. 进入**选择目标设备**。选择**现有标准交换机**，并选择步骤 **3** 中已创建的标准交换机。单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image12.png)
8. 设置端口属性。在**端口属性**选项页面，可用服务中勾选 **NVMe over RDMA**，单击 **NEXT**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/add-nvmf-rdma-vmkernel.png)

   > **说明**：
   >
   > 在 VMware 7.0U2 版本的可用服务中无 **NVMe over RDMA** 选项，无需进行此项设置。
9. 设置 IPv4 参数。选择**使用静态 IPv4 设置**，在**IPv4 地址**中输入 ESXi 主机的接入 IP 2 并设置子网掩码。请确保接入 IP 2 和接入 IP 1 在同一子网。
10. 设置 VMKernel 网络适配器的故障切换顺序。选择已创建的标准交换机，依次编辑其上的 VMKernel 网络适配器，在**绑定和故障切换** > **故障切换顺序**中，勾选**替代**，仅指定一个物理网络适配器作为活动适配器，并将另一个物理网络适配器移至未用的适配器列表。确保每个 VMkernel 适配器都绑定在不同的活动适配器上，以实现网络冗余与高可用性。

    ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image13.png)

    ![](https://cdn.smartx.com/internal-docs/assets/c577f847/image14.png)
11. 完成配置后，在 ESXi 主机上 Ping 块存储集群的接入地址，确认网络可以正常连接。

## 第 2 步：配置 VMware vSphere 集群支持 NVMe over RDMA

1. 为每台 ESXi 主机安装 NVMe 适配器。在 ESXi 主机界面，依次选择**配置**> **RDMA 适配器**，确认上一步加入标准交换机的 vmnic 对应的 RDMA 适配器名称。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/nvmf-software-adapter-3.png)
2. 依次单击**配置**>**存储适配器**>**添加软件适配器**，在添加界面选择**添加软件 NVMe over RDMA 适配器**，并选择适配器。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/nvmf-software-adapter-2.png)

   > **说明**：
   >
   > 若使用双网口连接块存储集群，请为每一个 vmnic 均添加对应的软件 NVMe over RDMA 适配器。
3. 设置 ESXi 主机的 hostnqn。将 vmknvme 驱动参数设置为 `vmknvme_hostnqn_format=0`，重启后将以 UUID 格式生成 hostnqn。

   ```
   $ esxcli system module parameters set -m vmknvme -p vmknvme_hostnqn_format=0
   $ reboot
   $ esxcli nvme info get
   Host NQN:
   nqn.2014-08.org.nvmexpress:uuid:5ffefdd7-0a51-3700-0b16-001e6792303a
   ```

## 第 3 步：配置 NVMe Subsystem 作为数据存储（Datastore）使用

1. 在 ESXi 的存储适配器上添加 NVMe Subsystem。依次单击**存储适配器**> **VMware NVME over RDMA 存储适配器**>**控制器**>**添加控制器**，选择**手动**方式，依次输入子系统 NQN、块存储集群任一节点的接入 IP 和 4420 端口，并设置**保持活动超时**为 5 秒。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/add-nvmf-software-adapter-2.png)

   > **注意**：
   >
   > **自动**方式默认**保持活动超时**的时长为 60 秒，在故障切换时会产生较长时间的 IO 中断，因此不建议使用。
2. 重复步骤 1，为每个节点添加接入 IP 的控制器，以便使用 Multipath。
3. 单击**重新扫描适配器**。扫描完成后可以在**设备**中发现块存储集群的 Namespace。
4. 单击**重新扫描存储**，重新扫描主机上的所有存储适配器以发现新添加的存储设备和/或 VMFS 卷。
5. （可选）若采用双网口连接块存储，请对两个 RDMA 存储适配器均重复以上步骤。
6. 单击**存储设备**，根据 NVMe RDMA Disk 的 EUI（根据 ZBS 的 Namespace UUID 生成，去掉了所有 `-` 连接符）找到对应的设备，单击**属性**>**多路径策略**>**操作**>**编辑多路径**。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/edit-nvmf-multipath-policy-1.png)
7. 选择**路径选择策略**为**固定**，保存设置。该配置能保证 ESXi 主机每次只会通过单个路径访问 ZBS 存储。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/edit-nvmf-multipath-policy-2.png)
8. 在每一台需要访问 ZBS 的 ESXi 主机上重复上述步骤。
9. 前往**数据存储**，创建基于该 Namespace 的 VMware 数据存储。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/create-datastore-with-zbs-subsystem-1.png)

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/create-datastore-with-zbs-subsystem-2.png)

   选择较高版本的 VMFS。

   ![](https://cdn.smartx.com/internal-docs/assets/c577f847/create-datastore-with-zbs-subsystem-3.png)

## 第 4 步：挂载 VMware 数据存储到块存储集群中的其他节点

VMware 数据存储（Datastore）建立一次即可，块存储集群中的其他节点挂载该数据存储后即可使用。

> **注意**：
>
> 若块存储集群从 5.0.0 升级到该版本且 ESXi 发生重启，需要重新挂载 Datastore，挂载时选择“保留现有的签名”，挂载方式请参考 [VMware 官方文档](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.storage.doc/GUID-EEFEB765-A41F-4B6D-917C-BB9ABB80FC80.html)。

## 配置流量控制

为了保证性能，客户端和存储端接入网络的交换机需配置相同的流量控制方式。可配置基于 L3 DSCP 的 PFC 流量控制和基于 Global Pause 的流量控制，但推荐使用基于 L3 DSCP 的 PFC 流量控制。

### 在交换机配置（以 Mellanox Switch 为例）

- **基于 L3 DSCP 的 PFC 流量控制配置（推荐配置）**

  1. 将 RoCE 的流量类型设置为 3 并开启 ECN，以便启用 DCQCN。将 ECN 的最低和最高触发阈值都设置为 3000 KB。

     ```
     switch > enable
     switch # configure terminal
     switch (config) # interface ethernet 1/1-1/2 traffic-class 3 congestion-control ecn minimum-absolute 3000 maximum-absolute 3000
     ```
  2. 设置 QoS trust mode 为 L3（DSCP）。

     `switch (config) # interface ethernet 1/1-1/2 qos trust L3`
  3. 将交换机的 PFC 在 priority 3 上开启。

     ```
     switch (config) # dcb priority-flow-control enable force
     switch (config) # dcb priority-flow-control priority 3 enable
     switch (config) # interface ethernet 1/1-1/2 dcb priority-flow-control mode on force
     switch (config) # interface ethernet 1/1-1/2 pfc-wd
     ```
  4. 验证 PFC 是否已开启，确认后保存配置。

     ```
     switch (config) # show dcb priority-flow-control

     PFC: enabled
     Priority Enabled List: 3
     Priority Disabled List: 0 1 2 4 5 6 7

     -------------------------------------------------
     Interface        PFC admin        PFC oper
     -------------------------------------------------
     Eth1/1           Auto             Enabled
     Eth1/2           Auto             Enabled
     ......

     switch (config) # configuration write
     ```
- **基于 Global Pause 流量控制配置**

  设置 RDMA 网卡所连交换机端口的 `flowcontrol` 为 `on`，验证并保存配置。

  ```
  Mellanox Switch
  switch > enable
  switch # configure terminal
  switch (config) #
  switch (config) # interface ethernet 1/1-1/2 flowcontrol send on force
  switch (config) # interface ethernet 1/1-1/2 flowcontrol receive on force
  switch (config) # show interfaces ethernet 1/1 | include Flow-control
  Flow-control                     : receive on send on
  switch (config) # show interfaces ethernet 1/2 | include Flow-control
  Flow-control                     : receive on send on
  switch (config) # configuration write
  ```

### 在 ESXi 主机配置 (以 Mellanox RDMA 网卡为例)

VMware vSphere 集群中所有节点均需配置相同的流量控制方式。

- **基于 L3 DSCP 的 PFC 流量控制配置（推荐配置）**

  ```
  esxcli system module parameters set -m nmlx5_core -p "trust_state=2"
  esxcli system module parameters set -m nmlx5_rdma -p "dscp_force=26"
  reboot
  esxcfg-module -g nmlx5_core
  esxcfg-module -g nmlx5_rdma
  ```
- **基于 Global Pause 流量控制配置**

  通过以下命令，查看对应 vmnic 的 Pause RX 和 Pause TX 列，若输出为 `TRUE`，则表明已开启了 Global Pause 流量控制。

  `esxcli network nic pauseParams list`

  如果以上输出为 `False`，则可通过以下命令配置 pause params 在 TX 和 RX 开启。该配置在重启后依旧生效。

  `esxcli network nic pauseParams set -t 1 -r 1 -n vmnicX`

---

## NVMe 存储服务 > 回收存储空间

# 回收存储空间

回收存储空间有以下 3 种方式，您可以根据实际需要进行选择。

- **保留 Namespace 并释放其存储空间**：使用 UNMAP 命令在客户端释放某个 Namespace 对应存储设备的存储空间，但仍保留 Namespace。
- **卸载客户端的 Namespace 并删除 Namespace**：确认某个 Namespace 已不再使用后，先从客户端卸载该 Namespace 对应的存储设备，再在块存储集群中删除该 Namespace。
- **移除客户端的 Subsystem 连接并删除 Subsystem**：确认某个 Subsystem 已不再使用后，先从客户端移除该 Subsystem 的连接，再在块存储集群中删除该 Subsystem。

---

## NVMe 存储服务 > 回收存储空间 > 保留 Namespace 并释放其存储空间

# 保留 Namespace 并释放其存储空间

## 在客户端释放存储空间

### Linux 客户端

1. 执行 `ls -l /dev/disk/by-id/ | grep nvme` 命令，查询客户端已挂载的 Namespcace 盘符。

   **示例**：

   ```
   root@centos8:/root # ls -l /dev/disk/by-id/ | grep nvme
   lrwxrwxrwx 1 root root 13 Jun 21 14:13 nvme-SMARTX_Controller_SMARTX0001 -> ../../nvme4n1
   lrwxrwxrwx 1 root root 13 Jun 21 12:11 nvme-uuid.57461498-13e2-42f1-b077-5f70efc8c4db -> ../../nvme0n2
   lrwxrwxrwx 1 root root 13 Jun 21 14:13 nvme-uuid.bd741324-fa5c-43f8-b595-edc2950501d1 -> ../../nvme4n1
   lrwxrwxrwx 1 root root 13 Jun 21 13:12 nvme-uuid.d638a76d-88b2-494e-a850-8eac62adaece -> ../../nvme0n1
   ```

   其中，`nvme-uuid.<UUID>` 为挂载的 Namespace UUID，`nvme4n1` 为对应的盘符。
2. 选择释放虚拟卷的部分或所有存储空间。

   - 释放部分空间：执行 `fstrim <path>` 命令，其中 `<path>` 为指定要释放的文件路径。
   - 释放所有空间。以下步骤皆以对 `/dev/nvme4n1` 操作为例。

     1. 执行 `umount` 命令卸载所有分区。例如 `sudo umount /dev/nvme4n1`。
     2. 执行 `uname -a` 命令查看内核版本。若内核版本高于 5.13，可跳过以下确认 `discard_max_bytes` 值的步骤。

        **示例**：

        ```
        root@centos8:/sys/block/nvme4n1/queue # uname -a
        Linux centos8 4.18.0-305.3.1.el8.x86_64 #1 SMP Tue Jun 1 16:14:33 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
        ```
     3. 确认 `discard_max_bytes` 值。若该值大于 16 MB（即 `16777216`），会触发 I/O 错误，建议将其值修改为 1 MB，即 `1048576`。

        **示例**：

        ```
        root@centos8:/root # cd /sys/block/nvme4n1/queue/
        root@centos8:/sys/block/nvme4n1/queue # grep . -r | grep discard
        grep: wbt_lat_usec: Invalid argument
        discard_zeroes_data:0
        discard_max_bytes:2199023255040
        discard_max_hw_bytes:2199023255040
        max_discard_segments:256
        discard_granularity:512
        root@centos8:/sys/block/nvme4n1/queue # echo 1048576 > discard_max_bytes
        root@centos8:/sys/block/nvme4n1/queue # grep . -r | grep discard
        grep: wbt_lat_usec: Invalid argument
        discard_zeroes_data:0
        discard_max_bytes:1048576
        discard_max_hw_bytes:2199023255040
        max_discard_segments:256
        discard_granularity:512
        ```
     4. 执行 `blkdiscard <dev path>` 命令释放空间。例如：`blkdiscard /dev/nvme4n1`。

### VMware vSphere 集群

1. 登录 vSphere Client，在 ESXi 主机界面，单击**配置** > **存储适配器** > **VMware NVMe over TCP/RDMA Storage Adapter** > **设备**，根据需要回收的 Namespace 的 UUID 查看对应的 VMFS 数据存储。
2. 在客户端释放存储空间。请根据释放存储空间的具体场景执行相应的操作。

   - 在 ESXi 中删除虚拟机时，请选择**所选虚拟机及其关联的磁盘**，删除磁盘时，请勾选**从数据存储删除文件**。
   - 在虚拟机操作系统中释放存储空间有以下几种情况：

     - 释放 Linux 操作系统的存储空间：请参考 [Linux 客户端操作指导](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_34#linux-%E5%AE%A2%E6%88%B7%E7%AB%AF)。
     - 释放 Windows 操作系统的存储空间：请参考 [Windows 客户端操作指导](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_34#windows-%E5%AE%A2%E6%88%B7%E7%AB%AF)。
     > **说明**：
     >
     > 在开启了空间自动回收的 VMFS6 环境下，单次执行 `blkdiscard` 或 `fstrim` 命令仅能释放少量空间，且可能会返回 “Input/output error” 信息。在此情况下，可多次执行命令直至不再报错以完成空间释放。
3. 通知 SMTX ZBS 回收存储空间。根据 VMFS 数据存储的类型不同，可以使用不同的方法来配置数据存储和虚拟机的空间回收。

   - VMFS6 支持自动回收存储空间，VMFS6 在完成数据删除后会自动通知 SMTX ZBS 回收存储空间。您可以通过选中相应数据存储，在右键菜单中选择**编辑空间回收**来开启自动空间回收功能。
   - VMFS5 只支持手动回收存储空间。在 VMFS5 完成数据删除后，请在 ESXi 主机依次执行 UNMAP 命令 `esxcli storage vmfs extent list` 和 `esxcli storage vmfs unmap -u <vmfs uuid>` 以通知 SMTX ZBS 回收存储空间。

## 在块存储集群确认存储空间是否已回收

在 SMTX ZBS 块存储集群任一节点执行 `zbs-nvmf ns list <subsystem>` 命令，通过查看 `Perf Unique Size` 和 `Cap Unique Size` 来确认存储空间是否已回收。

> **说明**：
>
> 存储空间的回收是一个渐进的过程，若回收的空间较大，可能需等待一段时间（通常为若干分钟）才能使空间完全回收，请您耐心等待。

---

## NVMe 存储服务 > 回收存储空间 > 卸载客户端的 Namespace 并删除 Namespace

# 卸载客户端的 Namespace 并删除 Namespace

## 在客户端卸载 Namespace 对应的存储设备

您需要在每个已挂载目标 Namespace 的客户端上执行卸载操作。

### Linux 客户端操作指导

**注意事项**

在 Linux 客户端上卸载 Namespace 对应的虚拟卷并不会释放 Namespace 的存储空间。

**操作步骤**

1. 执行 `ls -l /dev/disk/by-id` 命令，然后在如下输出结果中查找并记录要卸载的虚拟卷的设备符号。

   ```
   lrwxrwxrwx 1 root root 9 Sep 29 12:34 nvme-eui.1234567890abcdef1234567890abcdef -> ../../nvme0n1
   ```

   其中，`nvme-eui.1234567890abcdef1234567890abcdef` 表示 Namespace 的 uuid，`nvme0n1` 表示对应虚拟卷的设备符号。
2. 执行 `df -l` 命令，根据要卸载的虚拟卷设备符号查找并记录相应 Namespace 的所有文件系统的挂载点。
3. 执行 `umount <mnt point>` 命令，将相应 Namespace 的每个分区从客户端卸载，其中 `<mnt point>` 表示每个分区的文件系统的挂载点。
4. （可选）若客户端存在直接使用相应 Namespace 的服务，请停止该类服务的运行。
5. 检查 `/etc/fstab` 文件中是否已配置相应 Namespace 的所有文件系统的自动挂载信息，若已配置，请删除相关配置信息。
6. 执行 `df -l` 命令检查虚拟卷是否已卸载成功。若在输出结果中查找不到相应 Namespace 的所有文件系统的挂载点，则表明虚拟卷已卸载成功。

### VMware vSphere 集群操作指导

1. 登录 vSphere Client，在 ESXi 主机界面，单击**配置** > **存储适配器** > **VMware NVMe over TCP/RDMA Storage Adapter** > **设备**，根据需要回收的 Namespace 的 UUID （在设备名称的末尾显示）查看对应的 VMFS 数据存储。
2. 单击需要回收的 VMFS 数据存储，跳转至数据存储的管理界面后，单击**虚拟机**以查看当前数据存储所关联的虚拟机。
3. 删除当前数据存储与虚拟机关联的存储资源。您可以选择直接删除虚拟机或者仅删除虚拟机内使用该数据存储的数据盘。
   > **注意**：
   >
   > 存储资源删除后将无法恢复，请谨慎操作。若您选择保留虚拟机，并且虚拟机的系统盘使用了该数据存储，建议先备份虚拟机或将虚拟机的存储资源克隆至其他 VMFS 数据存储。
4. 确保当前数据存储与虚拟机关联的存储资源已删除后，返回该数据存储的管理界面，单击**操作** > **删除数据存储**。
5. 返回 VMware NVMe over TCP/RDMA Storage Adapter 的**设备**选项卡，对要回收的 Namespace 执行**分离**操作。

## 在块存储集群删除 Namespace

确认该 Namespace 不再使用后，请登录 CloudTower，删除该 Namespace。

> **注意**：
>
> 该操作无法撤回。一旦删除，Namespace 中包含的数据将无法找回，请谨慎操作。

---

## NVMe 存储服务 > 回收存储空间 > 移除客户端的 Subsystem 连接并删除 Subsystem

# 移除客户端的 Subsystem 连接并删除 Subsystem

## 在客户端移除 Subsystem 连接

您需要在每个已连接目标 Subsystem 的客户端上移除对应的 Subsystem 连接。

### Linux 客户端操作指导

1. 在客户端执行 `nvme list` 命令查看操作系统中所有可用的 NVMe 设备信息。其中 `Model` 为 `SMARTX Controller` 的 NVMe 设备即表示该设备为块存储集群的 Namespace 对应的虚拟卷，如 `/dev/nvme0n1` 和 `/dev/nvme0n2`，请记录下这些虚拟卷。

   ```
   [root@centos-1 network-scripts]# nvme list
   Node             SN                   Model                                    Namespace Usage                      Format           FW Rev
   ---------------- -------------------- ---------------------------------------- --------- -------------------------- ---------------- --------
   /dev/nvme0n1     SMARTX0001           SMARTX Controller                        1          42.95  GB /  42.95  GB    512   B +  0 B   23.01
   /dev/nvme0n2     SMARTX0001           SMARTX Controller                        2          42.95  GB /  42.95  GB    512   B +  0 B   23.01
   ```
2. 对上一步记录的每个虚拟卷执行 `nvme list-subsys <Node>` 命令，然后通过输出结果中的 NQN 筛选出属于要卸载的 Subsystem 所关联 Namespace 对应的虚拟卷。

   ```
   [root@centos-1 network-scripts]# nvme list-subsys /dev/nvme0n1
   nvme-subsys0 - NQN=nqn.2020-12.com.smartx:system:shunkai-test
   \
   +- nvme0 tcp traddr=10.0.18.74 trsvcid=8009 live non-optimized
   ```
3. 确认对应虚拟卷均已不再使用并已卸载，可参考 [Linux 客户端操作指导](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_39#linux-%E5%AE%A2%E6%88%B7%E7%AB%AF%E6%93%8D%E4%BD%9C%E6%8C%87%E5%AF%BC)卸载这些虚拟卷。
4. 执行 `df -h` 命令，确保在输出结果中未显示对应虚拟卷。
5. 执行 `nvme disconnect -n <your subsystem nqn>` 命令以断开与 Subsystem 的连接。
6. 清理 `/etc/nvme/discovery.conf` 和 `/etc/rc.d/rc.local` 中对相应 Subsystem 的连接配置和流量控制的持久化配置。

### VMware vSphere 集群操作指导

1. 登录 vSphere Client，在 ESXi 主机界面上，单击**配置** > **存储适配器** > **VMware NVMe over TCP** / **RDMA Storage Adapter** > **设备**，根据 Subsystem 所关联的所有 Namespace 的 UUID （在设备名称的末尾显示）查看对应的 VMFS 数据存储。
2. 确保所有要回收的 Namespace 均已从 ESXi 主机上分离。对于不满足要求的 Namespace，请参考 [VMware vSphere 集群操作指导](/smtxzbs/5.7.0/zbs_configuration/zbs_configuration_39#vmware-vsphere-%E9%9B%86%E7%BE%A4%E6%93%8D%E4%BD%9C%E6%8C%87%E5%AF%BC)执行操作。
3. 单击**控制器**，然后移除不再使用的 Subsystem 对应的控制器。

## 在块存储集群删除 Subsystem

1. 确认该 Subsystem 不再使用后，请在 CloudTower 上删除该 Subsystem 关联的 Namespace。
2. 删除该 Subsystem。

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
