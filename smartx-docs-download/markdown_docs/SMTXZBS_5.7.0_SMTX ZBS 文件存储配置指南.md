---
title: "SMTXZBS/5.7.0/SMTX ZBS 文件存储配置指南"
source_url: "https://internal-docs.smartx.com/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_preface"
sections: 41
---

# SMTXZBS/5.7.0/SMTX ZBS 文件存储配置指南
## 关于本文档

# 关于本文档

本文档介绍了如何配置 Linux 客户端通过 NFS 协议访问文件存储。

阅读本文档需了解文件存储、NFS 协议等相关技术背景知识，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

- **2026-02-06：文档随 SMTX 文件存储 1.3.0 正式发布**

  - **NFS**：增加了导出路径中包含特殊字符时挂载文件系统的处理方式。
  - **HDFS**：增加了对 HDFS 协议的支持。
- **2025-11-24**：**文档随 SMTX ZBS 5.7.0 正式发布**。

  相较于 5.6.4，本版本主要更新如下：

  - 增加卸载文件系统小节；
  - 增加 UNC 访问文件系统相关内容。

---

## 概述

# 概述

SMTX ZBS 是由北京志凌海纳科技股份有限公司（以下简称 “SmartX”）自主研发的分布式存储产品，可以为用户提供基于 NFS 协议和 HDFS 协议访问的文件存储服务 SFS。

---

## NFS

# NFS

NFS（Network File System，网络文件系统）是一种用于文件共享的网络协议，允许网络中的计算机之间共享资源。

SFS 当前支持为 Linux 和 Windows 客户端提供基于 NFS 协议访问的文件存储服务。

---

## NFS > 准备工作

# 准备工作

## 创建文件系统

客户端使用文件存储前，请您确认文件存储集群中已经存在状态为`已上线`的文件系统。否则，请参考《SMTX ZBS 管理指南》[创建](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_142)一个新的文件系统或将已有的文件系统[上线](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_146)。

## 获取挂载路径

文件系统上线后，SFS 将为其提供多个挂载路径，挂载路径的格式为 `文件接入 IP 地址/导出路径`。使用其中一个挂载路径挂载文件系统则表示客户端通过该挂载路径名称中的文件接入 IP 挂载和访问文件系统。

**挂载建议**

挂载文件系统前，请您阅读如下建议，为文件系统选择合适的挂载路径。

- 为了充分发挥就地访问和缓存的性能优势，提高访问性能：

  - 相同场景的文件数据使用同一个子目录，通过同一个挂载路径挂载；
  - 不同场景的文件数据使用不同的子目录，通过不同的挂载路径挂载，并尽量均匀地使用挂载路径访问文件系统。
- 多个客户端需要挂载同一个文件系统时：

  - 如不同客户端访问同一文件时存在读写或写写冲突，请确保这些客户端通过同一个挂载路径挂载该文件系统，否则文件的访问性能会急剧下降。
  - 如不同客户端仅读取同一文件，那么这些客户端可以通过同一个挂载路径也可以通过不同的挂载路径挂载该文件系统。
- 客户端与文件控制器位于同一主机时，建议您通过该文件控制器的文件接入 IP 为客户端挂载文件系统，以保证文件接入网卡对应的物理网口故障时客户端访问文件系统不受影响。

**操作步骤**

1. 登录 CloudTower 进入**文件存储**页面，在左侧导航栏中单击**文件存储集群**。
2. 在文件存储集群列表中单击文件系统所属的文件存储集群，进入概览页面单击**文件系统状态**卡片，或选择**文件系统**页签。
3. 在文件系统列表中单击需要挂载的文件系统，在弹出的详情面板中查看该文件系统的所有挂载路径。
4. 单击目标挂载路径本身或路径右侧的按钮复制路径。

---

## NFS > Linux 客户端 > 配置 Linux 客户端

# 配置 Linux 客户端

支持配置 Linux 客户端通过 NFSv3 和 NFSv4.1 访问 SFS 的文件系统。

配置前请确保客户端的网络与文件存储集群的文件接入网络连通。

## 安装 NFS 客户端

请您根据客户端的操作系统，通过如下命令安装 NFS 客户端。

- **Debian/Ubuntu**

  ```
  apt-get update && apt-get install nfs-common
  ```
- **CentOS/Redhat**

  ```
  yum install nfs-utils
  ```

## 配置防火墙

如果 NFS 客户端运行在防火墙环境下，请参考《SMTX ZBS 防火墙端口说明》文件存储集群端口说明的[外部防火墙端口开放规则](/smtxzbs/5.7.0/zbs_firewall_guide/zbs_firewall_guide_05#nfs)配置 NFS 客户端的防火墙规则以允许对应端口流量出入。

## 配置唯一标识（仅 NFSv4.1）

NFSv4.1 协议中，NFS 服务端根据 NFS 客户端发送的唯一标识 `co_ownerid` 来维护 NFS 客户端的状态，更多资料参考 [NFSv4 client identifier](https://docs.kernel.org/filesystems/nfs/client-identifier.html)。

默认情况下，`co_ownerid` 以 “Linux NFS” 开头，后跟客户端的主机名。如果多个 NFS 客户端主机名重复，那么 NFS 客户端的唯一标识 `co_ownerid` 也会重复，这些客户端访问文件系统时会互相干扰，导致文件系统操作失败、卡住等，影响文件系统的可用性。因此，使用 NFSv4.1 挂载文件系统时，请避免不同 NFS 客户端的主机名重复。

如果无法避免客户端主机名重复，您可以通过如下操作自定义 nfs module 参数 `nfs.nfs4_unique_id` 从而设置 `co_ownerid` 的唯一性：

1. 查看 NFS 客户端的 nfs4\_unique\_id：

   ```
   sudo systool -v -m nfs | grep -i nfs4_unique
   ```

   **输出示例**

   ```
   nfs4_unique_id = ""
   ```
2. 自定义 nfs4\_unique\_id：

   ```
   sudo 
   echo options nfs nfs4_unique_id="your_id" > /etc/modprobe.d/nfsclient.conf
   ```

   **输入示例**

   自定义 nfs4\_unique\_id 为 vm\_for\_play：

   ```
   sudo 
   echo options nfs nfs4_unique_id="vm_for_play" > /etc/modprobe.d/nfsclient.conf
   ```
3. 重启 NFS 客户端机器。

   ```
   sudo reboot
   ```
4. 再次查看当前 NFS 客户端的 nfs4\_unique\_id，确认自定义值生效：

   ```
   systool -v -m nfs | grep -i nfs4_unique
   ```

   **输出示例**

   ```
   nfs4_unique_id = "vm_for_play"
   ```

---

## NFS > Linux 客户端 > LDAP 身份映射

# LDAP 身份映射

文件系统的身份验证方式为 `UNIX` 时，SFS 将根据 NFS 客户端的 UID 和 GID 为不同用户提供不同访问权限。

如果同一个用户在不同客户端中的 UID 和 GID 不同，该用户通过不同客户端对同一个文件系统的访问权限不同，可能出现您通过客户端 A 创建的文件，在客户端 B 上无法修改的问题。

此时您可以通过 LDAP 配置域用户的 UID 和 GID，使同一个用户在不同客户端通过域账户访问同一个文件系统时具备一致的访问权限。

---

## NFS > Linux 客户端 > 挂载文件系统

# 挂载文件系统

Linux 客户端挂载文件系统后才能访问文件存储服务。

## 挂载选项

本节仅列举几项推荐配置的挂载选项，详细的挂载选项说明请参考 Linux 官方文档 [man fstab](https://man7.org/linux/man-pages/man5/fstab.5.html) 和 [man nfs](https://linux.die.net/man/5/nfs)。

| 挂载选项 | 描述 | 建议值 |
| --- | --- | --- |
| vers | NFS 协议的版本号，SFS 支持 v3 和 v4.1。 | vers=3 或 vers=4.1 |
| lock/nolock | 仅 vers=3 时生效，是否使用文件锁功能。  - lock：使用文件锁功能。 - nolock：不使用文件锁功能。 | nolock |
| proto | NFS 客户端向文件系统传输请求的传输层协议。 | proto=tcp |
| sec | NFS 客户端访问文件系统的身份验证方式。  - sec=sys，默认值，对应 UNIX 身份验证方式。 - sec=none，对应 `None` 身份验证方式。 | 文件系统配置为 `None` 身份验证方式时，必须显式配置 sec=none。 **注意**：如果在 CloudTower 修改了文件系统的身份验证方式，需要设置新的 sec 值并重新挂载。 |
| rsize | NFS 客户端从文件系统单次读取的数据块大小。 | rsize=1048576 |
| wsize | NFS 客户端向文件系统单次写入的数据块大小。 | wsize=1048576 |
| hard/soft | NFS 请求超时后 NFS 客户端的恢复行为。  - hard：当文件系统暂时不可用时，NFS 客户端会继续发送 NFS 请求，直至文件系统恢复。 - soft：当文件系统暂时不可用时，NFS 客户端在完成所设置的重试请求次数（retrans）之后 NFS 请求仍失败的话，就会向应用程序返回错误。可能会有数据污染风险。 | hard |
| timeo | NFS 客户端请求的超时时间，单位为 0.1 秒。超时发生后，NFS 客户端会根据 **hard/soft**、**retrans** 等参数决定是否重试。 | timeo=600（代表超时时间为 60 秒） |
| retrans | NFS 客户端重试请求的次数，超过此次数之后 NFS 客户端将根据 **hard/soft** 尝试进一步的恢复行为。 | retrans=2 |
| resvport/noresvport | NFS 客户端与文件系统通信时是否使用特权源端口。   - resvport： NFS 客户端与文件系统通信时使用特权源端口。 - noresvport：NFS 客户端与文件系统通信时使用新的非特权源端口。 | noresvport  **说明**：v5.4 及更低版本的 Linux 内核在网络连接断开后，NFS 客户端会尝试在同一非特权传输控制协议（TCP）源端口上重新连接，可能会持续失败，此时 NFS 客户端使用新的 TCP 源端口可以快速重新连接到文件系统，保障故障恢复后的文件系统可用性。 |
| acl/noacl | 仅 vers=3 时生效，是否使用 ACL 功能。 | noacl  **说明**：SFS 不支持 ACL 功能。 |

## 挂载方式

文件系统支持通过手动挂载和自动挂载两种方式进行挂载。

### 手动挂载

您可以通过如下 Linux 命令行手动将文件系统挂载到本地目录：

```
sudo mount -t nfs -o <mount_options> <mount_path> <mount_point>
```

- `<mount_options>` 替换为[挂载选项](#%E6%8C%82%E8%BD%BD%E9%80%89%E9%A1%B9)，可以按需配置多项，各项之间使用 `,` 连接。不同的 NFS 协议版本推荐配置的挂载选项如下：

  - **NFSv3**

    `vers=3,nolock,proto=tcp,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport,noacl`
  - **NFSv4.1**

    `vers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport`
- `<mount_path>` 替换为[挂载路径](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_04#%E8%8E%B7%E5%8F%96%E6%8C%82%E8%BD%BD%E8%B7%AF%E5%BE%84)。若挂载路径中包含 `` ` `` ，`~` ，`!` ，`@` ，`#` ，`$` ，`%` ，`^` ，`&` ，`(` ，`)` ，`-` ，`=` ，`+` ，`_` ，`,` ，`.` ，`;` ，`[` ，`]` ，`{` ，`}` ，挂载时必须在挂载路径前后增加单引号 `'` 。若挂载路径中包含 `'` ，挂载时必须在挂载路径前后增加单引号 `'` ，并且在原本挂载命令的单引号后增加 `\''` 。
- `<mount_point>` 替换为文件系统挂载的位置，也就是 NFS 客户端本地目录地址。

**挂载示例**

1. 通过如下命令，使用 NFSv4.1 协议将文件系统`fs-pkg-repo1` 通过挂载路径 `192.168.20.84:/fs-pkg-repo1` 挂载到本地目录 `/mnt/test` 中，为其配置的挂载选项为 `rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport`。

   ```
   sudo mount -t nfs -o vers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport 192.168.20.84:/fs-pkg-repo1 /mnt/test
   ```
2. 挂载后可通过如下命令查看 NFS 挂载信息：

   ```
   mount | grep nfs
   ```

   输出如下参数表示挂载成功：

   ```
   192.168.20.84:/fs-pkg-repo1 on /mnt/test type nfs4 (rw,relatime,vers=4.1,rsize=1048576,wsize=1048576,namlen=255,hard,noresvport,​proto=tcp,​timeo=600,retrans=2,sec=sys,clientaddr=192.168.23.18,local_lock=none,addr=192.168.20.84)
   ```

### 自动挂载

参考[挂载选项](#%E6%8C%82%E8%BD%BD%E9%80%89%E9%A1%B9)，将挂载选项配置到 `/etc/fstab` 文件。

---

## NFS > Linux 客户端 > 卸载文件系统

# 卸载文件系统

Linux 客户端无需访问文件系统或需要重新挂载文件系统时，请参考本节内容将文件系统从客户端中卸载。

1. 执行如下 Linux 命令卸载文件系统：

   ```
   sudo umount <mount_point>
   ```

   `<mount_point>` 需替换为文件系统挂载的位置，也就是 NFS 客户端本地目录地址。
2. 执行如下命令查看 NFS 挂载信息，以确认文件系统已卸载。

   ```
   mount | grep nfs
   ```

---

## NFS > Linux 客户端 > 访问文件系统

# 访问文件系统

将文件系统挂载到 Linux 客户端的本地目录后，您可以像访问本地文件系统一样访问 SFS 的文件系统。部分版本的 Linux 限制了文件系统根目录下的部分文件操作，详情请参考 [Linux 官方文档](https://man7.org/linux/man-pages/man5/proc.5.html) 中 **protected\_regular** 、**protected\_hardlinks** 等描述。为了避免文件操作失败，请参考如下示例在**子目录**中操作文件访问文件存储服务。

```
> mkdir /mnt/test/d1
> echo hello > /mnt/test/d1/f1
> cat /mnt/test/d1/f1
hello
```

---

## NFS > Windows 客户端

# Windows 客户端

[配置 Windows 客户端](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_08)后，您可以通过[挂载文件系统](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_09)到本地盘以访问 SFS，也可以[配置 UNC](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_16) 后通过 UNC 路径访问。

---

## NFS > Windows 客户端 > 配置 Windows 客户端

# 配置 Windows 客户端

支持配置 Windows 客户端通过 NFSv3 访问身份验证方式为 `UNIX 系统验证`的文件系统，不支持文件锁功能。

## 前提条件

- 请确保客户端的网络与文件存储集群的文件接入网络连通。
- 请确保文件存储集群已启用 Windows NFS 访问，如未启用请参考[编辑文件存储集群配置](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_149)。

> **注意**:
>
> 为避免 Windows NFS 客户端和 SFS 后端大小写参数不一致导致访问异常，[安装 Windows NFS 客户端](#%E5%AE%89%E8%A3%85-nfs-%E5%AE%A2%E6%88%B7%E7%AB%AF)后，请务必[配置 Windows NFS 客户端区分大小写](#%E9%85%8D%E7%BD%AE%E5%8C%BA%E5%88%86%E5%A4%A7%E5%B0%8F%E5%86%99%E5%8F%82%E6%95%B0)。

## 安装 NFS 客户端

请根据 Windows 版本选择安装 NFS 客户端的方式：

- **Windows Server**（推荐使用）

  - 以管理员权限使用 PowerShell 安装

    ```
    Install-WindowsFeature NFS-Client
    ```
  - 使用 GUI 界面安装

    1. 打开服务器管理器，选择**添加角色和功能**；
    2. 在**服务器角色**选项卡中选择**文件和存储服务**，在**文件和 iSCSI 服务**下选择**文件服务器和 NFS 服务器**，然后选择**下一步**；
    3. 在功能页选择 **NFS 客户端**，然后单击**安装**。
- **Windows PC**

  - 以管理员权限使用 PowerShell 安装

    ```
    Enable-WindowsOptionalFeature -FeatureName ServicesForNFS-ClientOnly, ClientForNFS-Infrastructure -Online -NoRestart
    ```
  - 使用 GUI 界面安装

    1. 打开控制面板，选择**程序** ；
    2. 程序和功能中选择**启用或者关闭 Windows 功能** ；
    3. 选择 **NFS 服务-NFS 客户端**，单击**确定**。

打开命令提示符，输入 `mount`，返回如下信息，表示安装成功。

```
C:\Users\Administrator>mount

本地    远程                                 属性
-------------------------------------------------------------------------------

C:\Users\Administrator>
```

## 配置 NFS 客户端参数

请**务必**为 NFS 客户端配置**区分大小写**参数，**推荐**配置 **hard** 挂载类型参数。

### 配置区分大小写参数

Windows NFS 客户端默认不区分目录项名称的大小写，而 SFS 后端仅支持区分大小写，为避免二者配置不一致带来的访问异常，请以管理员权限通过命令提示符执行下述命令配置 Windows 客户端区分大小写：

```
nfsadmin client config casesensitive=yes
```

### 配置 hard 挂载类型

Windows NFS 客户端默认使用 `soft` 挂载类型，推荐使用 `hard` 挂载类型以保障 I/O 持续可用。请以管理员权限通过命令提示符执行下述命令配置挂载类型为 `hard`。

```
nfsadmin client config mtype=hard
```

## 配置防火墙

如果 NFS 客户端运行在防火墙环境下，请参考《SMTX ZBS 防火墙端口说明》文件存储集群端口说明的[外部防火墙端口开放规则](/smtxzbs/5.7.0/zbs_firewall_guide/zbs_firewall_guide_05#nfs)配置 NFS 客户端的防火墙规则以允许对应端口流量出入。

---

## NFS > Windows 客户端 > UNIX 身份映射

# UNIX 身份映射

Windows 用户使用 NFS 客户端访问 SFS 时，Windows 用户需要映射到 UNIX 环境的 UID 和 GID。

您可以通过 Windows 提供的如下三种方式，自定义映射到 UNIX 环境的 UID 和 GID，以管理不同用户对文件的权限。

完成下述任一方式的配置后，您需重新挂载文件系统，通过命令提示符的 `mount` 命令查看输出的 `UID` 和 `GID` 为目标值来确认修改生效。

## 匿名映射

默认情况下，Windows 上所有用户被映射为匿名 UID（AnonymousUid）和 GID（AnonymousGid），此映射方式下，Windows 上所有用户具备相同的文件访问权限。

匿名 UID 和 GID 均默认为 `-2`，您可以自定义这两个值。

**操作步骤**

1. 下述 PowerShell 命令（填写参数 `<unix_uid>` 和 `<unix_gid>`）会创建注册表项 `AnonymousUID` 和 `AnonymousGID` 并设置值：

   ```
   New-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\ClientForNFS\CurrentVersion\Default" -Name AnonymousUID -Value <unix_uid> -PropertyType "DWord"
   New-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\ClientForNFS\CurrentVersion\Default" -Name AnonymousGID -Value <unix_gid> -PropertyType "DWord"
   ```

   如果上述命令报错：`New-ItemProperty : The property already exists.` 说明注册表项已存在，您可通过下述命令设置：

   ```
   Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\ClientForNFS\CurrentVersion\Default" -Name AnonymousUID -Value <unix_uid>
   Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\ClientForNFS\CurrentVersion\Default" -Name AnonymousGID -Value <unix_gid>
   ```
2. 使用 PowerShell 命令查看注册表项 `AnonymousUID` 和 `AnonymousGID` 的当前值：

   ```
   Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\ClientForNFS\CurrentVersion\Default" -Name AnonymousUID
   Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\ClientForNFS\CurrentVersion\Default" -Name AnonymousGID
   ```
3. 重启 Windows NFS 客户端。命令提示符执行下述命令：

   ```
   nfsadmin client stop
   nfsadmin client start
   ```
4. 重新挂载，并通过命令提示符的 `mount` 命令查看 `UID` 和 `GID` 以确认生效。

## 通过 Windows 本地配置文件进行身份映射

Windows 支持通过本地配置文件 `%SYSTEMROOT%\system32\drivers\etc\passwd` 自定义本地用户映射的 UID 和 GID。

**操作步骤**

1. 以管理员身份使用记事本编辑 `C:\Windows\System32\drivers\etc\passwd` 文件。如不存在该文件，请先创建，管理员权限执行 PowerShell：

   ```
   New-Item -Path "C:\Windows\System32\drivers\etc\passwd" -ItemType File
   ```
2. 在文件中增加用户配置并保存。

   以自定义本地用户 `local_user1` 的 `UID` 和 `GID` 为 1003 为例：

   ```
   local_user1:x:1003:1003:comment:C:\Users\local_user1
   ```
3. 重启 Windows NFS 客户端。命令提示符执行下述命令：

   ```
   nfsadmin client stop
   nfsadmin client start
   ```
4. 使用上述用户 `local_user1` 重新挂载，并通过命令提示符的 `mount` 命令查看 `UID` 和 `GID` 以确认生效。

## 通过 Active Directory 服务进行身份映射（仅支持 Windows Server）

如果您的 Windows Server 已加入到 Active Directory（简称 AD）的域中，可以通过 AD 管理域用户的 UNIX 身份映射，使域用户通过不同 Windows 系统访问 SFS 时具有相同的访问权限。

**操作步骤**

1. 自定义 AD 映射的 UID 和 GID。

   1. 选择 Active Directory 管理中心的对应用户，右键选择**属性**；
   2. 单击**扩展**，然后单击**属性编辑器**；
   3. 设置 `uidNumber` 以及 `gidNumber` 取值，单击**确定**。
2. 配置 Windows NFS 客户端使用 AD 映射的 UID 和 GID。

   1. 管理员身份执行如下 PowerShell 命令，启用 ADLookup：

      ```
      PS C:\Users\Administrator> Set-NfsMappingStore -EnableADLookup $true
      ```
   2. 切换到域账户，此处为 `aduser1`，执行如下 PowerShell 命令，确认输出的 `ADLookupEnabled` 为 **True**：

      ```
      PS C:\Users\aduser1> Get-NfsMappingStore
      UNMServer               :
      UNMLookupEnabled        : False
      ADDomain                :
      ADLookupEnabled         : True
      LdapServer              :
      LdapNamingContext       :
      LdapLookupEnabled       : False
      PasswdFileLookupEnabled : False
      ```
   3. 执行如下 PowerShell 命令，确认输出的 `UserIdentifier` 和 `GroupIdentifier` 为上一步骤中自定义的值：

      ```
      PS C:\Users\aduser1> Get-NfsMappedIdentity -AccountType user -AccountName aduser1
      UserIdentifier      : 1002
      GroupIdentifier     : 1002
      UserName            : aduser1
      PrimaryGroup        :
      SupplementaryGroups :
      ```
   4. 使用域账户 `aduser1` 重新挂载，并通过命令提示符的 `mount` 命令查看 `UID` 和 `GID` 以确认生效。

---

## NFS > Windows 客户端 > 挂载文件系统

# 挂载文件系统

Windows 客户端挂载文件系统后才能访问文件存储服务。

## 挂载选项

本节仅列举几项推荐配置的挂载选项，详细的挂载选项说明请参考 [Windows 官方文档](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mount)。

| 挂载选项 | 描述 | 建议值 |
| --- | --- | --- |
| mtype | NFS 共享的挂载类型。默认为 soft。  - hard：当存在连接问题时，会一直重试直到恢复。 - soft：当存在连接问题时，soft 更快返回失败。 | mtype=hard  **说明**：建议使用 hard 挂载以保障 I/O 持续可用。 |
| nolock | 禁用文件锁功能。 | nolock  **注意**：SFS 当前不支持通过 NFSv3 使用文件锁，但 Windows NFS 客户端默认打开文件锁，因此**必须**显式配置禁用文件锁功能。 |
| sec | NFS 客户端访问文件系统的身份验证方式。默认为 sec=sys，对应 `UNIX 系统验证`方式。 | sec=sys 或不配置该项  **注意**：SFS 当前仅支持 Windows 上默认的 sys 认证方式，**请勿**显式配置其他身份验证方式。 |

## 挂载方式

文件系统支持通过手动挂载和自动挂载两种方式进行挂载。

### 手动挂载

通过命令提示符执行如下命令将文件系统挂载到本地：

```
mount <mount_options> <mount_path> <devicename>
```

- `<mount_options>` 替换为[挂载选项](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_09#%E6%8C%82%E8%BD%BD%E9%80%89%E9%A1%B9)，可以按需配置多项，多项间使用空格分割，且请务必配置 `nolock`。
- `<<mount_path>` 替换为[挂载路径](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_04#%E8%8E%B7%E5%8F%96%E6%8C%82%E8%BD%BD%E8%B7%AF%E5%BE%84)。若挂载路径中包含 `'` ，`` ` `` ，`~` ，`!` ，`@` ，`#` ，`$` ，`%` ，`^` ，`&` ，`(` ，`)` ，`-` ，`=` ，`+` ，`_` ，`,` ，`.` ，`;` ，`[` ，`]` ，`{` ，`}`字符时，挂载时必须在挂载路径前后增加双引号 `"` 。
- `<devicename>` 替换为文件系统挂载的本地盘位置。

**挂载示例**

1. 打开命令提示符，执行如下命令，将文件系统 `fs-pkg-repo1` 通过挂载路径 `192.168.20.84:/fs-pkg-repo1` 挂载到本地 `Z` 盘中，为其配置的挂载选项为 `-o nolock mtype=hard`。

   ```
   mount -o nolock mtype=hard 192.168.20.84:/fs-pkg-repo1 Z:
   ```
2. 执行 `mount` 命令，输出如下信息表示挂载成功。确认 `casesensitive=yes` 以及给定参数符合预期。

   ```
   C:\Users\Administrator>mount

   本地    远程                                 属性
   -------------------------------------------------------------------------------
   Z:       \\192.168.20.84\fs-pkg-repo1           UID=-2, GID=-2
                                                   rsize=1048576, wsize=1048576
                                                   mount=hard, timeout=0.8
                                                   retry=1, locking=no
                                                   fileaccess=755, lang=GB2312-80
                                                   casesensitive=yes
                                                   sec=sys

   C:\Users\Administrator>
   ```

### 自动挂载

1. 单击**此电脑**，选择**计算机**，选择**映射网络驱动器**。
2. 驱动器选择本地盘符，例如 **Z:**。
3. 文件夹填充挂载路径，例如**192.168.20.84:/fs-pkg-repo1**。
4. 勾选**登录时重新连接**，然后单击**完成**。
5. 执行 `mount` 命令，输出如下信息表示挂载成功。预期 Windows 系统重启后挂载仍有效，无需再次挂载。

   ```
   C:\Users\Administrator>mount

   本地    远程                                 属性
   -------------------------------------------------------------------------------
   Z:       \\192.168.20.84\fs-pkg-repo1           UID=-2, GID=-2
                                                   rsize=1048576, wsize=1048576
                                                   mount=hard, timeout=0.8
                                                   retry=1, locking=no
                                                   fileaccess=755, lang=GB2312-80
                                                   casesensitive=yes
                                                   sec=sys

   C:\Users\Administrator>
   ```

---

## NFS > Windows 客户端 > 卸载文件系统

# 卸载文件系统

Windows 客户端无需访问文件系统或需要重新挂载文件系统时，请参考本节内容将文件系统从客户端中卸载。

1. 通过命令提示符执行如下命令卸载文件系统：

   ```
   umount <devicename>
   ```

   `<devicename>` 需替换为文件系统挂载的本地盘位置。
2. 执行 `mount` 命令查看 NFS 挂载信息，以确认文件系统已卸载。

---

## NFS > Windows 客户端 > 配置 UNC

# 配置 UNC

Universal Naming Convention (UNC) 是 Windows 系统中用于访问网络共享资源的命名约定。根据本节内容修改 Windows 客户端的 UNC 相关配置，即可通过 UNC 路径访问文件存储。

**前提条件**

**确保**[已配置区分大小写参数](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_08#%E9%85%8D%E7%BD%AE%E5%8C%BA%E5%88%86%E5%A4%A7%E5%B0%8F%E5%86%99%E5%8F%82%E6%95%B0)，**建议**将[挂载类型设置为 hard](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_08#%E9%85%8D%E7%BD%AE-hard-%E6%8C%82%E8%BD%BD%E7%B1%BB%E5%9E%8B)。

**操作步骤**

以下操作步骤以 Windows Server 2022 为例进行说明，其他 Windows 版本操作步骤类似。

1. 修改 Windows 客户端解析 UNC 路径的顺序，使其优先通过 NFS 网络共享解析：

   1. 打开**任务栏**，在搜索框中搜索 `ncpa.cpl` 并打开控制面板项以进入网络连接；或依次选择**控制面板** > **网络和 Internet** > **网络和共享中心** > **更改适配器设置**。
   2. 按 Alt 键调出菜单栏，选择**高级** > **高级设置**。
   3. 在弹出的**高级设置** > **提供程序顺序**窗口中，选中 `NFS Network` 并将其移至列表首位。
   4. 单击**确定**以保存配置。
2. 配置 Windows 客户端解析 UNC 路径时禁用 DFS 客户端：

   1. 以管理员权限运行 PowerShell，执行以下命令：

      ```
      PS C:\Users\Administrator> Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Services\Mup" -Name "DisableDfs" -Value 1 -Type DWORD -Force
      ```
   2. 执行以下命令验证设置已成功：

      ```
      PS C:\Users\Administrator> (Get-ItemProperty -Path "HKLM:\System\CurrentControlSet\Services\Mup").DisableDfs
      1
      ```
3. 重启 Windows 系统，使配置生效。

**后续操作**

完成配置后即可通过格式为 `\\<access_ip>\<export_path>\[subdirectory]\[file]` 的 UNC 路径访问文件系统。

- `<access_ip>` 替换为文件存储集群的文件接入 IP。
- `<export_path>` 替换为导出路径，默认为文件系统名称，可通过 CloudTower 文件系统详情页查看，如 `ns1`。
- `[subdirectory]` 可选参数，替换为子目录名称，如 `d1`。
- `[file]` 可选参数，替换为文件名，如 `hello.txt`。

---

## NFS > Windows 客户端 > 访问文件系统

# 访问文件系统

您可以通过文件资源浏览器、Windows 命令提示符和 Windows PowerShell 终端等访问 SFS 文件系统。

以 Windows 命令提示符为例，创建目录 `testdir`，并在其下创建文件 `testfile.txt`：

```
C:\Users\Administrator>Z:

Z:\>mkdir testdir

Z:\>cd testdir

Z:\testdir>echo hello > testfile.txt

Z:\testdir>type testfile.txt
hello
```

---

## HDFS

# HDFS

HDFS（Hadoop Distributed File System）是 Apache Hadoop 生态系统的一部分，是一个分布式文件系统，旨在处理大规模数据集的存储和处理。

SFS 当前支持基于 Apache Hadoop 的开源发行版如 CDH（Cloudera Distribution of Hadoop）、HDP（Hortonworks Data Platform）以及其他 Hadoop 应用如 Hive、HBase、StarRocks 和 Doris。

---

## HDFS > 准备工作

# 准备工作

## 确认网络连通

Hadoop 集群中的计算节点通过文件存储集群的文件存储网络访问 SFS 的 API server、data server 和 meta server，请确保文件存储集群的文件存储网络与 Hadoop 集群网络相互连通，以保证元数据查询和数据读写的正常进行。

## 创建文件系统

确认文件存储集群中已经存在状态为`已上线`且协议为 `HDFS` 的文件系统。否则，请参考《SMTX ZBS 管理指南》[创建](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_142)一个新的文件系统或将已有的文件系统[上线](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_146)。

## 下载 SFS Hadoop Java SDK 安装包

根据所对接的 Hadoop 环境，下载对应的 SFS Hadoop Java SDK 安装包：

- CDH 环境请下载 SFS-PARCEL 和 SFS-CSD 安装文件。
- HDP 环境请下载 SFS-HDP 安装文件。
- 其他特定应用如 HDFS、Hive、HBase、Tez、StarRocks 和 Doris，请下载 SFS-hadoop 安装文件。

## 下载 Kubeconfig 文件

SFS Hadoop 客户端通过 Kubeconfig 文件访问文件存储集群的 API server、获取元数据服务位置、数据节点拓扑，请参考《SMTX ZBS 管理指南》在 CloudTower 中[下载文件存储集群 Kubeconfig 文件](../zbs_administration_guide/zbs_administration_guide_200)。

---

## HDFS > 配置 CDH > 安装 SFS Hadoop 客户端

# 安装 SFS Hadoop 客户端

CDH 环境下，SFS Hadoop 客户端的部署遵循 Cloudera Manager 的扩展规范，通过 CSD（Custom Service Descriptor）实现统一服务管理，并利用 Parcel 机制进行客户端文件的自动化分发和版本控制。

**操作步骤**

1. 将 SFS-CSD 安装文件放置到 Cloudera Manager 节点的 `/opt/cloudera/csd` 目录中，将 SFS-PARCEL 安装文件解压后放置到 `/opt/cloudera/parcel-repo` 目录中。
2. 重启 Cloudera Manager 服务：

   ```
   service cloudera-scm-server restart
   ```
3. 激活 Parcel。

   1. 登录 Cloudera Manager Web UI 界面，在导航栏中选择**主机（Hosts）** > **Parcel**。
   2. 在 Parcel 列表中选择名称为 **SFS** 的 Parcel，单击**分配（Distribute）**。
   3. Parcel 分配完成后，单击**激活（Activate）**。
4. 添加 SFS 服务。

   1. 登录 Cloudera Manager Web UI 界面，单击 Hadoop 集群名称。
   2. 单击**添加服务（Add Service）**，在列表中选择 **SFS**。
   3. 在**自定义角色分配（Assign Roles）** 页面为 SFS 服务分配主机。

      ![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_01.png)
   4. 在**审核更改（Review Changes）** 页面配置 `install_dirs`。
   5. 按照界面指引完成剩余页面配置。若无报错，则表示安装成功。

---

## HDFS > 配置 CDH > 安装 Kubeconfig

# 安装 Kubeconfig

在 Hadoop 节点中安装 Kubeconfig 后，SFS Hadoop 客户端会根据 `core-site.xml` 中 `sfs.kubeconfig.path` 的取值访问 Kubeconfig 文件，使 Hadoop 组件可以访问并使用 SFS 作为其存储。

**操作步骤**

1. 在所有需要安装 SFS Hadoop 客户端的节点中创建 `/opt/sfs/.kube` 路径。
2. 将文件存储集群的 Kubeconfig 文件上传到所有节点的 `/opt/sfs/.kube` 路径下。

---

## HDFS > 配置 CDH > 通过 Cloudera Manager 修改服务配置

# 通过 Cloudera Manager 修改服务配置

请参考本节内容修改 CDH 集群中已有的服务的配置。

若您需要在 CDH 集群中添加新服务，请参考[修改新增服务配置](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_37)完成操作。

## HDFS

- CDH 5.x

  通过 HDFS 服务界面修改 `core-site.xml`。

  ![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_02.png)

  若您确认所有服务配置的路径均需指向 SFS，将 `fs.defaultFS` 设置为 SFS 地址，使用时即可省去 `sfs://${file_system_name}` 协议前缀。

  ```
  <property>
      <name>fs.defaultFS</name>
      <value>sfs://${file_system_name}</value>
  </property>
  ```

  示例配置如下，详细配置参数及说明请参考 [SFS 参数总览](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_27)。

  ```
  <property>
    <name>fs.sfs.impl</name>
    <value>io.fs.SfsFileSystem</value>
  </property>

  <property>
    <name>fs.AbstractFileSystem.sfs.impl</name>
    <value>io.fs.SfsAbstractFileSystem</value>
  </property>

  <property>
      <name>fs.defaultFS</name>
      <value>sfs://ns1</value>
  </property>

  <property>
    <name>sfs.kubeconfig.path</name>
    <value>/opt/sfs/.kube/config</value>
  </property>

  <property>
    <name>sfs.apiservers</name>
    <value>10.200.134.251,10.200.134.252,10.200.134.253</value>
  </property>
  ```
- CDH 6.x

  1. 通过 HDFS 服务界面修改 `core-site.xml`。示例配置如 CDH 5.x，详细配置参数及说明请参考 [SFS 参数总览](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_27)。
  2. 通过 YARN 服务界面修改 `mapreduce.application.classpath`，添加 `$HADOOP_COMMON_HOME/lib/sfs-hadoop.jar`。

     ![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_03.png)
  3. 通过 DistCp 将 Yarn 的相关数据迁移到 SFS。

     ```
     hadoop distcp -p  hdfs://cdh-longterm-01:8020/user/yarn  sfs://ns1/user/yarn
     ```
  4. 通过 Yarn 服务界面修改 `mapred-site.xml`：

     ![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_15.png)

     示例配置：

     ```
     <property>
       <name>mapreduce.application.framework.path</name>
       <value>sfs://${file_system_name}/user/yarn/mapreduce/mr-framework/${your_cdh_version}-mr-framework.tar.gz#mr-framework</value>
     </property>
     ```

服务配置修改后，请参考[测试验证](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_22#hadoop)章节内容确认 SFS 可用。

## HBase

1. 通过 HBase 服务界面修改 `hbase-site.xml`：

   ![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_09.png)

   示例配置：

   ```
   <property>
     <name>hbase.rootdir</name>
     <value>sfs://${file_system_name}/hbase</value>
   </property>

   <property>
     <name>hbase.wal.dir</name>
     <value>sfs://${file_system_name}/hbase-wal</value>
   </property>
   ```

   > **说明**：
   >
   > 若原始 `hbase-site.xml` 中未配置 `hbase.wal.dir`，则无需设置该项。
2. 若 HBase 集群存在旧数据，为避免冲突，您可以选择删除或迁移旧数据：

   - 删除原有 HBase 集群里的所有数据。通过 ZooKeeper 客户端删除 `zookeeper.znode.parent` 配置的 znode（默认 /hbase）。
   - 将原有 HBase 集群数据迁移到新的 SFS HBase 集群中。详细迁移步骤请参考[迁移数据](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_31#hbase)章节。
3. 重启 HBase 集群，使配置生效。

## Hive（可选）

如需将数据库的默认创建位置设置在 SFS 上，请通过 Hive 服务界面修改 `hive-site.xml`，将 `hive.metastore.warehouse.dir` 设置为 SFS 上的路径。修改后，Hive 数据库和表均默认创建在 SFS 上。

![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_05.png)

## Spark

1. 通过 Spark 服务界面修改 `spark-defaults.conf`，添加配置项 `spark.hadoop.fs.AbstractFileSystem.sfs.impl=io.fs.SfsAbstractFileSystem`。

   ![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_14.png)
2. 在每个 CDH 节点上运行以下命令，为 Spark 添加 SFS Hadoop 客户端依赖：

   ```
   ln -sf \
       /opt/cloudera/parcels/CDH/lib/hadoop/lib/sfs-hadoop.jar \
       /opt/cloudera/parcels/CDH/lib/spark/jars/sfs-hadoop.jar
   ```

## 重启集群并验证

通过 Cloudera Manager 修改上述服务配置后需重启 Hadoop 集群，使配置修改生效。待集群重启成功后，请参考[测试验证](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_22#hbase)章节内容确认 SFS 可用。

---

## HDFS > 配置 CDH > 修改新增服务配置

# 修改新增服务配置

若您在 CDH 集群中添加新的 HDFS、Yarn、HBase、Hive 和 Spark 服务，由于 CDH 集群在添加新服务时不支持将第三方存储（如 SFS）直接设置为默认文件系统，因此需要通过以下步骤来完成新服务的添加和数据迁移：

1. 通过 HDFS 服务界面修改 `core-site.xml`，临时将 `fs.defaultFS` 恢复为默认的 HDFS 路径，通常为 `hdfs://<nameservice>`。
2. 在 Cloudera Manager 中创建并添加新服务，并完成服务的初始化操作。
3. 使用 DistCp 工具将新服务在 HDFS 中生成的初始化数据迁移至 SFS 文件系统。

   ```
   hadoop distcp -p  hdfs://${namenode_ip:port}/user/${new_service}  sfs://${file_system_name}/user/${new_service}
   ```

   Spark 示例如下：

   ```
   hadoop distcp -p  hdfs://cdh-longterm-01:8020/user/spark  sfs://ns1/user/spark
   ```
4. 通过 HDFS 服务界面修改 `core-site.xml`，将 `fs.defaultFS` 重新设置为 SFS 路径 `sfs://${file_system_name}`，保存配置后重启受影响的相关服务，使新配置生效。

---

## HDFS > 配置 CDH > 升级 SFS Hadoop 客户端

# 升级 SFS Hadoop 客户端

1. 将最新版本的 SFS-PARCEL 安装文件解压后放置到 `/opt/cloudera/parcel-repo` 目录中。
2. 重启 Cloudera Manager 服务：

   ```
   service cloudera-scm-server restart
   ```
3. 激活 Parcel。

   1. 登录 Cloudera Manager Web UI 界面，在导航栏中选择**主机（Hosts）** > **Parcel**。
   2. 单击**检查新 Parcel（Check for New Parcels）**。
   3. 在 Parcel 列表中选择新的 **SFS**，单击**分配（Distribute）**。
   4. Parcel 分配完成后，单击**激活（Activate）**。
4. 删除 Yarn 中的 usercache，使 Yarn 应用最新的安装文件：

   ```
   sudo rm -rf ​/yarn/nm/usercache
   ```
5. 重启 Hadoop 集群，使配置修改生效。
6. 参考[测试验证](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_22#hbase)章节内容确认 SFS 可用。

---

## HDFS > 配置 CDH > 卸载 SFS Hadoop 客户端

# 卸载 SFS Hadoop 客户端

1. 删除 SFS 服务。

   1. 登录 Cloudera Manager Web UI 界面，单击 Hadoop 集群名称。
   2. 在集群界面中找到 **SFS** 服务的 **Actions** 菜单，选择 **Delete**。
2. 删除 SFS-Parcel。

   1. 在 Cloudera Manager Web UI 导航栏中选择**主机（Hosts）** > **Parcel**。
   2. 在 Parcel 列表中选择名称为 **SFS** 的 Parcel，单击**停用（Deactivate）**。
   3. 选择**从主机移除（Remove from host）** > **删除（Delete）**。
3. 手动删除 SFS-CSD 安装文件。删除 Cloudera Manager 节点的 `/opt/cloudera/csd` 目录中的 SFS-CSD 文件。
4. 恢复服务配置。

   1. 在 Cloudera Manager Web UI 中，将 CDH 中的所有[新增或修改的服务配置](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_21)恢复原状。
   2. 重启 Hadoop 服务，使配置修改生效。
5. 重启 Cloudera Manager 服务：

   ```
   service cloudera-scm-server restart
   ```

---

## HDFS > 配置 HDP > 安装 SFS Hadoop 客户端

# 安装 SFS Hadoop 客户端

HDP 环境中，SFS 客户端通过 Ambari 管理平台进行统一配置和管理生命周期，并利用客户端自动分发功能实现配置文件的集中化部署。

**操作步骤**

1. 将 SFS-HDP 安装文件解压后放置到 Ambari Server 节点的 `/var/lib/ambari-server/resources/stacks/HDP/${your_hdp_version}/services` 目录中。
2. 重启 Ambari Server：

   ```
   systemctl restart ambari-server
   ```

   或

   ```
   ambari-server restart
   ```
3. 添加 SFS 服务：

   1. 打开 Ambari Web UI，进入 **Services** 页面，单击 **Add Service**。
   2. 在 **Choose services** 页面选择 **SFS**。
   3. 完成 **Assign masters**、 **Assign slaves and clients** 配置。
   4. 在 **Customize services** 页面配置 `install_dirs`。

      ![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_06.png)
   5. 按照界面指引完成剩余页面配置。若无报错，则表示安装成功。

---

## HDFS > 配置 HDP > 安装 Kubeconfig

# 安装 Kubeconfig

在 Hadoop 节点中安装 Kubeconfig 后，SFS Hadoop 客户端会根据 `core-site.xml` 中 `sfs.kubeconfig.path` 的取值访问 Kubeconfig 文件，使 Hadoop 组件可以访问并使用 SFS 作为其存储。

**操作步骤**

1. 在所有需要安装 SFS Hadoop 客户端的节点中创建 `/opt/sfs/.kube` 路径。
2. 将文件存储集群的 Kubeconfig 文件上传到所有节点的 `/opt/sfs/.kube` 路径下。

---

## HDFS > 配置 HDP > 通过 Ambari Web UI 修改服务配置

# 通过 Ambari Web UI 修改服务配置

## HDFS

通过 HDFS 服务界面修改 `core-site.xml`，非默认的字段请在 Custom core-site 自行添加。

若您确认所有服务配置的路径均需指向 SFS，将 `fs.defaultFS` 设置为 SFS 地址，使用时即可省去 `sfs://${file_system_name}` 协议前缀。

```
<property>
  <name>fs.defaultFS</name>
  <value>sfs://${file_system_name}</value>
</property>
```

示例配置如下，详细配置参数及说明请参考 [SFS 参数总览](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_27)。

```
<property>
  <name>fs.sfs.impl</name>
  <value>io.fs.SfsFileSystem</value>
</property>

<property>
  <name>fs.AbstractFileSystem.sfs.impl</name>
  <value>io.fs.SfsAbstractFileSystem</value>
</property>

<property>
  <name>fs.defaultFS</name>
  <value>sfs://ns1</value>
</property>
   
<property>
  <name>sfs.kubeconfig.path</name>
  <value>/opt/sfs/.kube/config</value>
</property>

<property>
  <name>sfs.apiservers</name>
  <value>10.200.134.251,10.200.134.252,10.200.134.253</value>
</property>

<property>
  <name>sfs.node_name.node1</name>
  <value>sfs-0</value>
</property>

<property>
  <name>sfs.node_name.node2</name>
  <value>sfs-1</value>
</property>

<property>
  <name>sfs.node_name.node3</name>
  <value>sfs-2</value>
</property>

<property>
  <name>sfs.supergroup</name>
  <value>hadoop</value>
</property>

<property>
  <name>sfs.superuser</name>
  <value>hdfs</value>
</property>
```

## MapReduce2

1. 将 MapReduce 相关目录从 HDFS 迁移到 SFS 中：

   ```
   hadoop fs -get hdfs://{your-hdfs-uri}/hdp/apps/{hdp.version}/tez/tez.tar.gz
   mkdir ./tmp
   tar -xzf ./tez.tar.gz -C ./tmp
   cp sfs-hadoop-{sfs.version}.jar ./tmp
   tar -czf ./tez.tar.gz -C ./tmp .
   ```
2. 通过 MapReduce2 服务界面修改 `mapreduce.application.classpath`，在末尾使用 `:` 隔开现有内容，然后增加 `/usr/hdp/${hdp.version}/hadoop/lib/sfs-hadoop.jar`，无需替换变量。

   ![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_07.png)

## HBase

1. 通过 HBase 服务界面修改 `hbase-site.xml`：

   ![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_09.png)

   示例配置：

   ```
   <property>
     <name>hbase.rootdir</name>
     <value>sfs://${file_system_name}/hbase</value>
   </property>

   <property>
     <name>hbase.wal.dir</name>
     <value>sfs://${file_system_name}/hbase-wal</value>
   </property>
   ```
2. 若 HBase 集群存在旧数据，为避免冲突，您可以选择删除或迁移旧数据：

   - 删除原有 HBase 集群里的所有数据。通过 ZooKeeper 客户端删除 `zookeeper.znode.parent` 配置的 znode（默认 /hbase）。
   - 将原有 HBase 集群数据迁移到新的 SFS HBase 集群。详细迁移步骤请参考[迁移数据](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_31#hbase)章节。

## Tez

1. 获取最新版本 SFS-hadoop 安装文件。
2. 通过 Tez 服务界面获取 `tez.lib.uris` 路径，默认为 `/hdp/apps/${your_hdp_version}/tez/tez.tar.gz`。
3. 将 SFS-hadoop 安装文件下载到 `tez.tar.gz` 压缩包中，禁止改变压缩包内部结构。

   操作示例：

   ```
   hadoop fs -get hdfs://${your-hdfs-uri}/hdp/apps/${your_hdp_version}/tez/tez.tar.gz
   mkdir ./tmp
   tar -xzf ./tez.tar.gz -C ./tmp
   cp sfs-hadoop-1.3.0.jar ./tmp
   tar -czf ./tez.tar.gz -C ./tmp .
   ```
4. 将更新后的 `tez.tar.gz` 压缩包上传到 `sfs://${file_system_name}/hdp/apps/${your_hdp_version}/tez/tez.tar.gz`。
5. 通过 Tez 服务界面修改 `tez-site.xml` 中 `tez.lib.uris` 为步骤 4 的上传路径。

   ![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_10.png)

## Hive（可选）

如需将数据库的默认创建位置设置在 SFS 上，请通过 Hive 服务界面修改 `hive.metastore.warehouse.dir` 为 SFS 上的路径。修改后，Hive 数据库和表均默认创建在 SFS 上。

![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_08.png)

## 重启服务并验证

1. 重启服务，使配置修改生效。若服务已启用 HA，滚动重启即可。
2. 参考[测试验证](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_22#hbase)章节内容确认 SFS 可用。

---

## HDFS > 配置 HDP > 升级 SFS Hadoop 客户端

# 升级 SFS Hadoop 客户端

1. 将最新版本的 SFS-HDP 安装文件解压后放置到 Ambari Server 节点的 `/var/lib/ambari-server/resources/stacks/HDP/${your_hdp_version}/services` 目录中。
2. 重启 Ambari Server：

   ```
   systemctl restart ambari-server
   ```

   或

   ```
   ambari-server restart
   ```
3. 卸载现有 SFS 服务。

   1. 打开 Ambari Web UI，进入 **Services** 页面，选择现有的 **SFS**。
   2. 在 **Configs** 页面，单击 **ACTIONS**，选择 **Delete Service**。

   ![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_11.png)
4. 添加新 SFS 服务。

   1. 打开 Ambari Web UI，进入 **Services** 页面，单击 **Add Service**。
   2. 在 **Choose services** 页面选择新的 **SFS**。
   3. 完成 **Assign masters**、 **Assign slaves and clients** 配置。
   4. 在 **Customize services** 页面配置 `install_dirs`。

      ![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_06.png)
   5. 按照界面指引完成剩余页面配置。
5. 删除 Yarn 中的 usercache，使 Yarn 应用最新的安装文件：

   ```
   sudo rm -rf ​/yarn/nm/usercache
   ```
6. 重启服务，使配置修改生效。若服务已启用 HA，滚动重启即可。
7. 参考[测试验证](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_22#hbase)章节内容确认 SFS 可用。

---

## HDFS > 配置 HDP > 卸载 SFS Hadoop 客户端

# 卸载 SFS Hadoop 客户端

1. 删除 SFS 服务。

   1. 打开 Ambari Web UI，进入 **Services** 页面，选择 **SFS**。
   2. 在 **Configs** 页面，单击 **ACTIONS**，选择 **Delete Service**。
2. 手动删除 SFS-HDP 安装文件。删除 Ambari Server 节点的 `/var/lib/ambari-server/resources/stacks/HDP/${your_hdp_version}/services` 目录中的 SFS-HDP 文件。
3. 恢复服务配置。

   1. 在 Ambari Web UI 中，将 HDP 中的所有[新增或修改的服务配置](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_25)恢复原状。
   2. 重启 Hadoop 服务，使配置修改生效。
4. 重启 Ambari Server：

   ```
   systemctl restart ambari-server
   ```

   或

   ```
   ambari-server restart
   ```

---

## HDFS > 配置特定 Hadoop 应用 > HDFS

# HDFS

## 安装 SFS Hadoop 客户端

将 SFS-hadoop 安装文件和 `$JAVA\_HOME/lib/tools.jar` 下载至 `${HADOOP_HOME}/share/hadoop/common/lib/` 目录中。

## 安装 Kubeconfig

1. 在所有需要安装 SFS Hadoop 客户端的节点中创建 `/opt/sfs/.kube` 路径。
2. 将文件存储集群的 Kubeconfig 文件上传到所有节点的 `/opt/sfs/.kube` 路径下。

## 修改服务配置

1. 修改 `core-site.xml` 添加 SFS 参数，详细配置参数及说明请参考 [SFS 参数总览](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_27)。

   若您确认所有服务配置的路径均需指向 SFS，将 `fs.defaultFS` 设置为 SFS 地址，使用时即可省去 `sfs://${file_system_name}` 协议前缀。

   ```
   <property>
       <name>fs.defaultFS</name>
       <value>sfs://${file_system_name}</value>
   </property>
   ```
2. 参考[测试验证](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_22#hadoop)章节内容确认 SFS 可用。
3. 若运行 Yarn 相关操作报错 “Class io.fs.SfsFileSystem not found”，请执行如下操作：

   1. 执行 `stop-yarn.sh` 命令，并确保 ResourceManager、NodeManager 已暂停。
   2. 执行 `start-yarn.sh` 命令，重新启动 Yarn。

## 升级 SFS Hadoop 客户端

1. 将最新的 SFS-hadoop 安装文件更新至 `${HADOOP_HOME}/share/hadoop/common/lib/` 目录中。
2. 删除 Yarn 中的 usercache，使 Yarn 应用最新的安装文件：

   ```
   sudo rm -rf ​/yarn/nm/usercache
   ```
3. 参考[测试验证](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_22#hadoop)章节内容确认 SFS 可用。

---

## HDFS > 配置特定 Hadoop 应用 > HBase

# HBase

## 安装 SFS Hadoop 客户端

参考 [HDFS](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_28) 章节为 HDFS 安装 SFS Hadoop 客户端和 Kubeconfig 并修改服务配置。

## 修改服务配置

1. 通过 HBase 服务界面修改 `hbase-site.xml`：

   示例配置：

   ```
   <property>
     <name>hbase.rootdir</name>
     <value>sfs://${file_system_name}/hbase</value>
   </property>

   <property>
     <name>hbase.wal.dir</name>
     <value>sfs://${file_system_name}/hbase-wal</value>
   </property>
   ```
2. 重启 Hbase 服务使配置生效，若启用 HA，滚动重启即可。
3. 若 HBase 集群存在旧数据，为避免冲突，您可以选择删除或迁移旧数据：

   - 删除原有 HBase 集群里的所有数据。通过 ZooKeeper 客户端删除 `zookeeper.znode.parent` 配置的 znode（默认 /hbase）。
   - 将原有 HBase 集群数据迁移到新的 SFS HBase 集群。详细迁移步骤请参考[迁移数据](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_31#hbase)章节。
4. 参考[测试验证](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_22#hbase)章节内容确认 SFS 可用。

## 升级 SFS Hadoop 客户端

1. 将最新的 SFS-hadoop 安装文件更新至 `${HADOOP_HOME}/share/hadoop/common/lib/` 目录中。
2. 重启 Hbase 服务使配置生效，若启用 HA，滚动重启即可。
3. 参考[测试验证](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_22#hbase)章节内容确认 SFS 可用。

---

## HDFS > 配置特定 Hadoop 应用 > Hive

# Hive

## 安装 SFS Hadoop 客户端

1. 参考 [HDFS](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_28) 章节为 HDFS 安装 SFS Hadoop 客户端和 Kubeconfig 并修改服务配置。
2. 将 SFS-hadoop 安装文件和 `$JAVA\_HOME/lib/tools.jar` 下载至 `${HIVE_HOME}/auxlib` 目录中。

## 修改服务配置

1. 如需将数据库的默认创建位置设置在 SFS 上，请修改 `hive.metastore.warehouse.dir` 为 SFS 上的路径。修改后，Hive 数据库和表均默认创建在 SFS 上。

   ```
   <property>
   <name>hive.metastore.warehouse.dir</name>
   <value>sfs://${file_system_name}/user/hive/warehouse</value>
   </property>
   ```
2. 重启 Hive 服务使配置生效，若启用 HA，滚动重启即可。
3. 参考[测试验证](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_22#hive)章节内容确认 SFS 可用。

## 升级 SFS Hadoop 客户端

1. 将最新的 SFS-hadoop 安装文件更新至 `${HADOOP_HOME}/share/hadoop/common/lib/` 目录中。
2. 将最新的 SFS-hadoop 安装文件更新至 `${HIVE_HOME}/auxlib` 目录中。
3. 重启 Hive 服务使配置生效，若启用 HA，滚动重启即可。
4. 参考[测试验证](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_22#hive)章节内容确认 SFS 可用。

---

## HDFS > 配置特定 Hadoop 应用 > Tez

# Tez

## 安装 SFS Hadoop 客户端

1. 参考 [HDFS](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_28) 章节为 HDFS 安装 SFS Hadoop 客户端和 Kubeconfig 并修改服务配置。
2. 将 `$JAVA\_HOME/lib/tools.jar` 下载至 `${HADOOP_HOME}/share/hadoop/common/lib/` 目录中。
3. 通过 `tez-site.xml` 获取 `tez.lib.uris` 路径，默认为 `/hdp/apps/${your_hdp.version}/tez/tez.tar.gz`。
4. 将 SFS-hadoop 安装文件放入 `tez.tar.gz` 中，禁止改变压缩包内部结构。
5. 将更新后的 `tez.tar.gz` 上传到 SFS 文件系统中。例如：`sfs://${file_system_name}/apps/tez.tar.gz`。
6. 修改 `tez-site.xml` 中 `tez.lib.uris` 为步骤 5 的上传路径。

## 修改服务配置

修改 `tez-site.xml` 中的 `tez.lib.uris` 为[安装 SFS Hadoop 客户端](#%E5%AE%89%E8%A3%85-sfs-hadoop-%E5%AE%A2%E6%88%B7%E7%AB%AF)中步骤 5 的上传路径。

## 升级 SFS Hadoop 客户端

1. 将最新的 SFS-hadoop 安装文件更新至 `${HADOOP_HOME}/share/hadoop/common/lib/` 目录中。
2. 将 `$JAVA\_HOME/lib/tools.jar` 下载至 `${HADOOP_HOME}/share/hadoop/common/lib/` 目录中。
3. 通过 `tez-site.xml` 获取 `tez.lib.uris` 路径，默认为 `/hdp/apps/${your_hdp.version}/tez/tez.tar.gz`。
4. 将最新的 SFS-hadoop 安装文件放入 `tez.tar.gz` 压缩包中，禁止改变压缩包内部结构。
5. 将更新后的 `tez.tar.gz` 压缩包上传到 SFS 文件系统中。例如：`sfs://${file_system_name}/apps/tez.tar.gz`。
6. 修改 `tez-site.xml` 中 `tez.lib.uris` 为步骤 5 的上传路径。

---

## HDFS > 配置特定 Hadoop 应用 > StarRocks

# StarRocks

## 安装 SFS Hadoop 客户端

将 SFS-hadoop 安装文件和 `$JAVA\_HOME/lib/tools.jar` 下载至 `${STARROCKS_HOME}/be/lib/hadoop/common` 和 `${STARROCKS_HOME}/fe/lib` 目录中。

## 安装 Kubeconfig

1. 在所有需要安装 SFS Hadoop 客户端的节点中创建 `/opt/sfs/.kube` 路径。
2. 将文件存储集群的 Kubeconfig 文件上传到所有节点的 `/opt/sfs/.kube` 路径下。

## 修改服务配置

1. 修改 BE 节点 `${STARROCKS_HOME}/be/conf/core-site.xml` 配置：

   示例配置如下，详细配置参数及说明请参考 [SFS 参数总览](/smtxzbs/5.7.0/sfs_configuration/sfs_configuration_27)。

   ```
   <property> 
     <name>fs.defaultFS</name>  
     <value>sfs://ns1/</value> 
   </property>  
   <property> 
     <name>fs.sfs.impl</name>  
     <value>io.fs.SfsFileSystem</value> 
   </property>  
   <property>
     <name>fs.AbstractFileSystem.sfs.impl</name>  
     <value>io.fs.SfsAbstractFileSystem</value> 
   </property>  
   <property> 
     <name>sfs.kubeconfig.path</name>  
     <value>/opt/sfs/.kube/config</value> 
   </property>
   ```
2. 修改 FE 节点配置。

   1. 修改 `${STARROCKS_HOME}/fe/conf/fe.conf` 配置：

      ```
      <property> 
        <name>cloud_native_hdfs_url</name>  
        <value>sfs://${file_system_name}/user/starrocks/</value> 
      </property>  
      <property> 
        <name>cloud_native_storage_type</name>  
        <value>HDFS</value> 
      </property>
      ```
   2. 修改 `${STARROCKS_HOME}/fe/conf/core-site.xml` 配置与 BE 节点保持一致。
3. 如需配置数据库默认创建在 SFS 上，可设置默认存储卷：

   1. 创建存储卷：

      ```
      CREATE STORAGE VOLUME sfs_volume TYPE = HDFS LOCATIONS = ("sfs://${file_system_name}/path-to-starrocks/");
      ```
   2. 设置默认存储卷：

      ```
      SET sfs_volume AS DEFAULT STORAGE VOLUME;
      ```
4. 重启 StarRocks 服务使配置生效，若启用 HA，滚动重启即可。

## 升级 SFS Hadoop 客户端

1. 将最新的 SFS-hadoop 安装文件更新至 `${STARROCKS_HOME}/be/lib/hadoop/common` 和 `${STARROCKS_HOME}/fe/lib` 目录中。
2. 重启 StarRocks 服务使配置生效，若启用 HA，滚动重启即可。

---

## HDFS > 配置特定 Hadoop 应用 > Doris

# Doris

## 安装 SFS Hadoop 客户端

将 SFS-hadoop 安装文件和 `$JAVA\_HOME/lib/tools.jar` 下载至 `${DORIS_HOME}/be/lib/hadoop_hdfs/common` 和 `${DORIS_HOME}/fe/lib` 目录中。

## 安装 Kubeconfig

1. 在所有需要安装 SFS Hadoop 客户端的节点中创建 `/opt/sfs/.kube` 路径。
2. 将文件存储集群的 Kubeconfig 文件上传到所有节点的 `/opt/sfs/.kube` 路径下。

## 修改服务配置

1. 创建 SFS 存储库 `sfs_vault_demo`，其中 `hadoop.username` 需填写访问 SFS 使用的用户名。

   **示例配置**

   ```
   mysql -h ${FE_IP} -P9030 -uroot
   // 创建 SFS 存储库
   CREATE STORAGE VAULT IF NOT EXISTS sfs_vault_demo PROPERTIES (     
     "type" = "hdfs",
     "fs.defaultFS" = "sfs://ns1",                 
     "path_prefix" = "big/data",                               
     "hadoop.username" = "hadoop", 
     "fs.AbstractFileSystem.sfs.impl" = "io.fs.SfsAbstractFileSystem", 
     "fs.sfs.impl" = "io.fs.SfsFileSystem", 
     "sfs.kubeconfig.path" = "/opt/sfs/.kube/config"
   );
   ```
2. 重启 Doris 服务使配置生效，若启用 HA，滚动重启即可。
3. 重启完成后即可将 `sfs_vault_demo` 作为数据源。

## 升级 SFS Hadoop 客户端

1. 将最新的 SFS-hadoop 安装文件更新至 `${DORIS_HOME}/be/lib/hadoop_hdfs/common` 和 `${DORIS_HOME}/fe/lib` 目录中。
2. 重启 Doris 服务使配置生效，若启用 HA，滚动重启即可。

---

## HDFS > 测试验证

# 测试验证

Hadoop 应用启用 SFS Hadoop JAVA SDK 后即可使用 SFS，本节提供各类应用的基本操作以验证能否正常使用 SFS。

## HDFS

Hadoop 生态组件一般通过 `org.apache.hadoop.fs.FileSystem` 类与 HDFS 对接，SFS 继承 `org.apache.hadoop.fs.FileSystem` 类来支持 Hadoop 生态的各个组件，您可以通过 hadoop fs 命令操作 SFS 的文件系统。

```
hadoop fs -ls sfs://${file_system_name}/
hadoop fs -mkdir sfs://${file_system_name}/sfs-test
hadoop fs -rm -r sfs://${file_system_name}/sfs-test
```

## Yarn/MapReduce2

```
hadoop jar /path/to/hadoop-mapreduce-client-jobclient-*-tests.jar TestDFSIO -write -nrFiles 1 -Size 1MB -resFile /tmp/write.log
```

## HBase

```
create 'test', 'cf'
list 'test'
put 'test', 'row1', 'cf:a', 'value1'
scan 'test'
get 'test', 'row1'
disable 'test'
drop 'test'
```

## Hive

```
create table if not exists person(
    name string,
    age int
)

location 'sfs://${file_system_name}/tmp/person';
insert into table person values('tom',25);
insert overwrite table person select name, age from person;
select name, age from person;
drop table person;
```

## Spark

```
spark-submit \
    --class org.apache.spark.examples.SparkPi \
    --master yarn --deploy-mode \
    client /opt/cloudera/parcels/CDH/lib/spark/examples/jars/spark-examples_*.jar 1000
```

---

## HDFS > SFS 参数总览

# SFS 参数总览

Hadoop 的 `core-site.xml` 文件用于配置 SFS 参数。

## 核心配置（必填）

对接 Hadoop 和 SFS 文件系统的关键配置，包括声明 Hadoop 使用的文件系统类型和接口定义，以及文件存储集群的访问路径和 IP 信息。若变更文件系统配置，需重启服务以更新配置。

| 配置项 | 默认值 | 描述 |
| --- | --- | --- |
| fs.AbstractFileSystem.sfs.impl | io.fs.SfsAbstractFileSystem | 指定要使用的存储实现，默认使用 `sfs://` 作为 scheme。 |
| fs.sfs.impl | io.fs.SfsFileSystem | 指定要使用的存储实现，默认使用 `sfs://` 作为 scheme。 |
| sfs.apiservers | null | 指定可访问的 SFS API server 服务的 IP 地址，即文件存储集群的文件控制器中主节点的文件存储 IP，例如：`10.20.156.1,10.20.156.2,10.20.156.2`。 您可以通过 CloudTower 文件存储集群的**设置** > **文件控制器**页面查看，其中序号 0～2 的文件控制器是主节点。 |
| sfs.kubeconfig.path | null | 指定用于访问文件存储集群的 Kubeconfig 文件路径，保证配置后 SFS Hadoop 客户端可访问到该路径，例如：`/opt/sfs/.kube/config`。 |

## 权限配置（可选）

未配置如下权限参数时，Hadoop 服务通过客户端访问 SFS 时将使用默认配置。

| 配置项 | 默认值 | 描述 |
| --- | --- | --- |
| sfs.superuser | hdfs | 超级用户。 |
| sfs.supergroup | supergroup | 超级用户组。 |
| sfs.users | null | 配置用户名和 UID 的列表文件的地址，例如 `sfs://name/etc/users`。 列表中的文件格式为 `<username>:<UID>`，一行一个用户，每个用户的 UID 必须唯一。 |
| sfs.groups | null | 配置用户组、GID 和组成员的列表文件的地址，例如 `sfs://${file_system_name}/etc/groups`。 列表中的文件格式为 `<group-name>:<GID>:<username1>,<username2>`，一行一个用户组。 |

**配置示例**

```
// sfs://ns1/etc/users 文件内容
alice:1
bob:2
tom:3
// sfs://ns1/etc/groups 文件内容
groupa:1:alice
groupb:2:bob,tom
// 在 Custom core-site 添加对应 HDFS 配置
<property>
    <name>sfs.superuser</name>
    <value>hdfs</value>
</property>
<property>
    <name>sfs.supergroup</name>
    <value>supergroup</value>
</property>
<property>
    <name>sfs.users</name>
    <value>sfs://ns1/etc/users</value>
</property>
<property>
    <name>sfs.groups</name>
    <value>sfs://ns1/etc/groups</value>
</property>
```

## 数据亲和性配置（可选）

Hadoop 计算节点的 I/O 请求默认将随机下发至文件控制器中的存储节点。

为避免超融合模式下跨主机通信或存算分离模式下跨域跨机架通信，减少网络性能损耗，建议您配置数据亲和性，即配置文件控制器和 Hadoop 计算节点的拓扑关系，将 Hadoop 计算节点的 I/O 优先下发至指定的文件控制器。

| 配置项 | 默认值 | 描述 |
| --- | --- | --- |
| sfs.node\_name.${host\_name} | null | 用于节点亲和性配置，配置计算节点 `${host_name}` 的数据优先下发至目标 SFS 文件控制器 `${file_controller_name}`（通过 CloudTower 文件存储集群的**设置** > **文件控制器**页面即可查看文件控制器的名称）。 |

**示例场景及配置**

![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_12.png)

图示为超融合模式下文件控制器与 Hadoop 计算节点位于同一主机，为避免跨主机通信带来的性能损耗，将 Hadoop 计算节点的 I/O 优先下发至位于同一主机的文件控制器：

- Hadoop-1 的 I/O 优先下发至 SFS-1；
- Hadoop-2 的 I/O 优先下发至 SFS-2；
- Hadoop-3 和 Hadoop-4 的 I/O 优先下发至 SFS-3。

配置如下：

```
<property>
    <name>sfs.node_name.Hadoop-1</name>
    <value>SFS-1</value>
</property>

<property>
    <name>sfs.node_name.Hadoop-2</name>
    <value>SFS-2</value>
</property>

<property>
    <name>sfs.node_name.Hadoop-3</name>
    <value>SFS-3</value>
</property>

<property>
    <name>sfs.node_name.Hadoop-4</name>
    <value>SFS-3</value>
</property>
```

---

## HDFS > 迁移数据

# 迁移数据

Hadoop 应用已有数据时，为保证切换至 SFS 时业务正常运行，请参考本节内容迁移数据。

## HBase

### 在线迁移

将源 HBase 集群的历史数据以快照形式导入目标 SFS HBase 集群，并通过 [HBase Replication](https://hbase.apache.org/book.html?utm_source=chatgpt.com#_cluster_replication) 将源集群的数据同步备份至目标集群，待数据备份成功后，即可将业务切换到目标集群。

1. 在源集群上配置备份关系：

   ```
   add_peer '${replication_name}', CLUSTER_KEY => "${zookeeper_path}:2181:/hbase",TABLE_CFS => { "${table_name}" => []}
   enable_table_replication '${table_name}'
   ```

   | 参数 | 说明 |
   | --- | --- |
   | `${replication_name}` | 备份关系的名称，用于唯一标识备份关系，例如 `1`。 |
   | `${zookeeper_path}` | 目标集群 ZooKeeper 的地址，可以通过访问 `http://${hbase_master_ip}:16010` Hbase UI 获取，例如 `sfs-hadoop1`。 |
   | `${table_name}` | 待迁移的表的名称，例如 `test_table`。 |

   输入示例：

   ```
   add_peer '1', CLUSTER_KEY => "sfs-hadoop1:2181:/hbase",TABLE_CFS => { "test_table" => []}
   enable_table_replication 'test_table'
   ```
2. 在源集群上暂停备份：

   ```
   disable_peer("${replication_name}")
   ```

   输入示例：

   ```
   disable_peer("1")
   ```
3. 在源集群上为待迁移的表创建快照：

   ```
   snapshot '${table_name}','${snapshot_name}'
   ```

   | 参数 | 说明 |
   | --- | --- |
   | `${table_name}` | 待迁移的表的名称。 |
   | `${snapshot_name}` | 自定义表快照的名称。 |
4. 在目标集群上导入快照：

   ```
   hbase org.apache.hadoop.hbase.snapshot.ExportSnapshot \
   -snapshot ${snapshot_name} \
   -copy-from hdfs://${your-hdfs-uri}/hbase \
   -copy-to sfs://${file_system_name}/hbase/ \
   -mappers 1 \
   -bandwidth 20
   ```

   | 参数 | 说明 |
   | --- | --- |
   | `${your-hdfs-uri}` | 源集群 HDFS 的 URI。 |
5. 在目标集群上恢复快照：

   ```
   disable '${table_name}'
   restore_snapshot '${snapshot_name}'
   enable '${table_name}'
   ```
6. 在源集群上开启备份。

   ```
   enable_peer("${replication_name}")
   ```
7. 等待备份完成。

### 离线迁移

CDH 6.3.2 版本请参考 [CDH 6.3.2 迁移方案](#cdh-632-%E8%BF%81%E7%A7%BB%E6%96%B9%E6%A1%88)，其他版本请参考 [默认迁移方案](#%E9%BB%98%E8%AE%A4%E8%BF%81%E7%A7%BB%E6%96%B9%E6%A1%88)。

#### 默认迁移方案

1. 在源集群中关闭所有表：

   ```
   disable_all '.*'
   ```
2. 在目标集群中通过 DistCp 工具导入数据：

   ```
   sudo -u hbase hadoop distcp -Dmapreduce.map.memory.mb=1500 -p ${your_filesystem}/${hbase.rootdir}/data sfs://${file_system_name}/${hbase.rootdir}/data
   ```
3. 在目标集群中删除 HBase 元数据：

   ```
   sudo -u hbase hadoop fs -rm -r sfs://${file_system_name}/${hbase.rootdir}/data/hbase
   ```
4. 在目标集群中修复元数据：

   ```
   sudo -u hbase hbase hbck -fixMeta -fixAssignments
   ```

#### CDH 6.3.2 迁移方案

1. 在源集群中关闭所有表：

   ```
   disable_all '.*'
   ```
2. 在源集群中停止 Hbase 服务。
3. 在目标集群中停止 Hbase 服务。
4. 在目标集群中通过 DistCp 工具导入数据：

   1. 导入 hbase.rootdir 下的数据：

      ```
      sudo -u hbase hadoop distcp -Dmapreduce.map.memory.mb=1500 -p ${your_filesystem}/${hbase.rootdir} sfs://${file_system_name}/${hbase.rootdir}
      ```
   2. 若设置了 hbase.wal.dir，则还需要导入其中的数据：

      ```
      sudo -u hbase hadoop distcp -Dmapreduce.map.memory.mb=1500 -p hdfs://${your_filesystem}/${hbase.wal.dir} sfs://${file_system_name}/${hbase.wal.dir}
      ```
5. 在目标集群中删除 ZooKeeper 客户端上 HBase 的元数据节点路径：

   ```
   delete /hbase/meta-region-server
   ```
6. 在目标集群中启动 Hbase 服务，并启用表。

## Hive

Hive 支持使用多种文件系统存储数据。

对于未分区表，整张表的数据必须在同一个文件系统上。迁移数据时可以使用 [DistCp 工具](https://hadoop.apache.org/docs/stable/hadoop-distcp/DistCp.html) 将 HDFS 中的数据迁移至 SFS，然后修改元数据更新表的数据位置即可。

对于分区表，表里每个分区的数据可以位于不同的文件系统。可以在插入新的分区数据时，将新分区的数据位置设置在 SFS 文件系统上，再逐步将已有分区的数据使用 [DistCp 工具](https://hadoop.apache.org/docs/stable/hadoop-distcp/DistCp.html)迁移至 SFS 后更新分区数据的数据位置。

**前提条件**

Hive 已停写。

**迁移示例**

此处以迁移数据库为例，介绍迁移流程。

1. 获取数据库当前数据位置：

   ```
   DESCRIBE DATABASE ${database_name};
   ```

   输出示例：

   ![](https://cdn.smartx.com/internal-docs/assets/ccb60c6c/sfs_configuration_13.png)
2. 迁移数据库：

   ```
   hadoop distcp -update -delete -prbugpct -strategy dynamic ${database_src_location} ${database_dst_location}
   ```

   | 参数 | 说明 |
   | --- | --- |
   | `${database_src_location}` | 数据库的源数据位置，例如 `hdfs://hdp-longterm-01:8020/warehouse/tablespace/managed/hive/mydb.db`。 |
   | `${database_dst_location}` | 数据库的目标数据位置，例如 `/warehouse/tablespace/managed/hive/mydb.db`。 |
3. 迁移任务完成后，修改元数据中数据库和表的数据位置：

   ```
   ALTER DATABASE ${database_name} SET LOCATION ${database_dst_location};
   ALTER TABLE ${table_name} SET LOCATION ${table_dst_location};
   ```
4. 通过 Hive SQL 验证数据完整性：

   ```
   select count(*) from ${database_name}.${table_name};
   ```

---

## 附录 > 配置文件存储集群

# 配置文件存储集群

CloudTower 版本低于 4.7.0 时，请在文件存储集群部署成功后，参考本节内容命令行按需配置 Windows NFS 访问。

CloudTower 版本为 4.7.0 及以上时，使用命令行修改配置不生效，请参考《SMTX ZBS 管理指南》中[编辑文件存储集群的配置](/smtxzbs/5.7.0/zbs_administration_guide/zbs_administration_guide_149)章节，在 CloudTower 界面配置 Windows NFS 访问。

## 前提条件

您需要选择一个文件控制器，设置工具 `kubectl`:

```
alias kubectl="docker run --rm --net host -v /opt/iomesh/sfs/config/certs/admin.conf:/tmp/admin.conf -e KUBECONFIG=/tmp/admin.conf bitnami/kubectl:1.27.7"
```

## 启用 Windows 客户端访问

1. 在上述文件控制器上，执行下述命令以启用 Windows 客户端访问：

   ```
   kubectl patch sfscl default --type='merge' -p '{"spec":{"enable_nfs_from_windows":true}}'
   ```
2. 执行下述命令确认启用是否生效：

   ```
   kubectl get sfscl default -oyaml | grep enable_nfs_from_windows
   ```

   输出如下结果则表示 Windows 客户端访问已启用。

   ```
   enable_nfs_from_windows: true
   ```

## 停用 Windows 客户端访问

1. 在上述文件控制器上，执行下述命令以停用 Windows 客户端访问：

   ```
   kubectl patch sfscl default --type='merge' -p '{"spec":{"enable_nfs_from_windows":false}}'
   ```
2. 执行下述命令确认停用是否生效：

   ```
   kubectl get sfscl default -oyaml | grep enable_nfs_from_windows
   ```

   输出如下结果则表示 Windows 客户端访问已停用。

   ```
   enable_nfs_from_windows: false
   ```

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
