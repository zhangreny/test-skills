---
title: "SMTXELF/6.3.0/SMTX cloudbase-init 虚拟机初始化配置指南"
source_url: "https://internal-docs.smartx.com/smtxelf/6.3.0/cloudbase-init-guide/cloudbase-init-guide-preface-generic"
sections: 14
---

# SMTXELF/6.3.0/SMTX cloudbase-init 虚拟机初始化配置指南
## 关于本文档

# 关于本文档

本文档介绍了如何使用 cloudbase-init 为 Windows 虚拟机进行初始化配置。

使用之前，请先查阅《SMTX 虚拟机初始化工具兼容性列表》，若虚拟机操作系统在列表中，建议您使用 SMTX 虚拟机初始化工具进行初始化配置，详情请参考《SMTX 虚拟机初始化工具 - cloudbase-init 用户指南》。

---

## 更新信息

# 更新信息

- **2025-02-14：更新内容如下：**

  - 在**第 5 步：使用 cloudbase-init 模板创建虚拟机**小节增加当选择配置静态 IP 地址时，系统将进行 IP 地址冲突检测的说明。
  - 在**第 4 步：将 cloudbase-init 虚拟机转化为虚拟机模板**小节，增加手动删除已有网卡静态 IP 配置文件的建议。
- **2024-04-30：更新使用 cloudbase-init 模板创建虚拟机的步骤中关于网络配置的部分。**
- **2022-08-31：第一版正式发布。**

---

## 概述

# 概述

在创建新虚拟机时，经常需对虚拟机进行初始化设置，如设置主机名、IP 地址、SSH 秘钥等。当批量创建虚拟机时，如对每个虚拟机手动进行初始化设置，则操作较为繁琐。在此场景下，您可以配置 cloudbase-init，使 Windows 虚拟机在首次开机时自动完成初始化配置，提高配置效率。

## cloudbase-init 简介

cloudbase-init 是一个第三方工具，可以为 Windows 虚拟机自动完成一系列系统初始化配置。cloudbase-init 作为一个非常驻服务，仅在虚拟机开机启动时执行，执行完成后立即退出，不会监听任何端口。

ELF 通过使用配置了 cloudbase-init 的虚拟机模板创建虚拟机的方式，实现对 cloudbase-init 的支持。使用 cloudbase-init 模板创建的新虚拟机包含了初始化数据，新虚拟机在第一次启动时将自动完成初始化配置。

您可以使用 cloudbase-init 完成如下初始化配置。

- 主机名
- 默认用户的密码

  默认用户为 `Admin`。
- SSH 公钥，用于 SSH 远程登录主机
- DNS
- IP 地址，支持 DHCP 和静态 IP 配置
- 自定义用户数据，可通过设置脚本实现更多自动化配置

如需了解 cloudbase-init 更多信息，请参考 [cloudbase-init 官方文档](https://cloudbase-init.readthedocs.io/en/latest/index.html)。

## cloudbase-init 与客户机操作系统的兼容性

cloudbase-init 与虚拟机操作系统的兼容性情况，请参考随产品版本发布的《SMTX 虚拟机服务兼容性指南》。

---

## 使用 cloudbase-init

# 使用 cloudbase-init

使用 cloudbase-init 请参照以下步骤进行操作。

---

## 使用 cloudbase-init > 第 1 步：创建空白虚拟机并安装操作系统

# 第 1 步：创建空白虚拟机并安装操作系统

创建一个空白虚拟机，并安装所需的客户机操作系统。具体操作方法，请参考《管理指南》的“创建虚拟机”和“为虚拟机安装操作系统”章节。

---

## 使用 cloudbase-init > 第 2 步：在操作系统安装 cloudbase-init

# 第 2 步：在操作系统安装 cloudbase-init

请根据 Windows 的系统类型，参考如下链接下载对应的 cloudbase-init 安装包。推荐安装 `cloudbase-init` 的 `dev` 版本。

- 32 位 Windows 系统：<https://www.cloudbase.it/downloads/CloudbaseInitSetup_x86.msi>
- 64 位 Windows 系统：<https://www.cloudbase.it/downloads/CloudbaseInitSetup_x64.msi>

**操作步骤**

1. 打开 cloudbase-init 安装包，勾选 **I accept the terms in the License Agreement**，单击 **Next**。
2. 使用默认安装路径，单击 **Next**。
3. 在 **Configuration options** 窗口中，设置用户名为 **Admin**，日志输出串口选择 **COM1**，且不勾选 **Run Cloudbase-Init service as LocalSystem**。单击 **Next** 继续。
4. 单击 **Install**，在 **Completed the Cloudbase-Init Setup Wizard** 窗口，请参考如下提示进行设置：

   - 若希望通过模板创建的虚拟机生成新的 SID，请选择 **Run Sysprep to create a generalized image. This is necessary if you plan to duplicate this instance, for example by creating a Glance image** 选项，否则请取消选中此选项；
   - 取消勾选 **Shutdown when Sysprep terminates** 选项，否则 sysprep 执行完后会立即重启虚拟机。

     > **注意**：
     >
     > 若通过 cloudbase-init 执行 sysprep， 请确保**剩余 Windows 重置计数**大于等于 1，否则无法执行 sysprep 封装。可通过执行 `slmgr.vbs /dlv` 命令查看**剩余 Windows 重置计数**。
5. 单击 **Finish**，完成安装。

---

## 使用 cloudbase-init > 第 3 步：修改 cloudbase-init 配置文件

# 第 3 步：修改 cloudbase-init 配置文件

安装完 cloudbase-init 后，请修改配置文件 `C:\Program Files\Cloudbase Solutions\Cloudbase-Init\conf\cloudbase-init.conf`，参考下表增加配置项。

| **配置项** | **描述** | **配置说明** |
| --- | --- | --- |
| metadata\_services=​cloudbaseinit.metadata​.services.configdrive​.ConfigDriveService | 配置 cloudbase-init 的 data source 为 Config Drive。 | 必须配置 |
| netbios\_host\_name​\_compatibility=false | 默认情况下，受 Windows 系统限制 hostname 长度不能超过 15 个字符，增加该配置项可使 Windows 系统支持最多 63 个字符。 | 推荐配置 |
| first\_logon\_behaviour=no | 默认情况下，Windows 系统强制用户（Admin）首次登录时修改密码，增加该配置项可取消此限制。 | 可选配置 |

`cloudbase-init.conf` 配置示例如下：

```
[DEFAULT]
username=Admin
groups=Administrators
inject_user_password=true
config_drive_raw_hhd=true
config_drive_cdrom=true
config_drive_vfat=true
bsdtar_path=C:\Program Files\Cloudbase Solutions\Cloudbase-Init\bin\bsdtar.exe
mtools_path=C:\Program Files\Cloudbase Solutions\Cloudbase-Init\bin\
verbose=true
debug=true
logdir=C:\Program Files\Cloudbase Solutions\Cloudbase-Init\log\
logfile=cloudbase-init.log
default_log_levels=comtypes=INFO,suds=INFO,iso8601=WARN,requests=WARN
logging_serial_port_settings=COM1,115200,N,8
mtu_use_dhcp_config=true
ntp_use_dhcp_config=true
local_scripts_path=C:\Program Files\Cloudbase Solutions\Cloudbase-Init\LocalScripts\
metadata_services=cloudbaseinit.metadata.services.configdrive.ConfigDriveService
netbios_host_name_compatibility=false
first_logon_behaviour=no
```

---

## 使用 cloudbase-init > 第 4 步：将 cloudbase-init 虚拟机转化为虚拟机模板

# 第 4 步：将 cloudbase-init 虚拟机转化为虚拟机模板

完成 cloudbase-init 安装配置后，请关闭虚拟机。若虚拟机已有网卡静态 IP 配置文件，则建议您手动删除该文件。然后请参考《CloudTower 使用指南》的“将虚拟机克隆或转化为虚拟机模板”章节将虚拟机转化为虚拟机模板。

> **注意**：
>
> 将已安装 cloudbase-init 的虚拟机转化成模板时，务必将`已安装 cloud-init` 选项标记为**是**，否则后续通过模板创建虚拟机时无法配置初始化数据。

---

## 使用 cloudbase-init > 第 5 步：使用 cloudbase-init 模板创建虚拟机

# 第 5 步：使用 cloudbase-init 模板创建虚拟机

创建 cloudbase-init 虚拟机模板后，可使用此模板创建虚拟机。使用 cloudbase-init 模板创建虚拟机时，除可配置一般的虚拟机参数，还可配置虚拟机初始化数据。

您可以通过 Web 控制台或 CloudTower 创建 cloudbase-init 虚拟机，也可以通过 RESTful API 和 CloudTower SDK 进行创建。本节仅描述使用 cloudbase-init 模板创建虚拟机过程中的初始化配置。使用虚拟机模板创建虚拟机的详细步骤以及选项描述，请参考《管理指南》的“从模板创建虚拟机”章节。

## 通过 Web 控制台/CloudTower 创建虚拟机

通过 Web 控制台和 CloudTower 创建虚拟机的方法基本相同，此处以 CloudTower 为例。

**操作步骤**

1. 登录 CloudTower，在界面右上角单击**创建**，选择**从模板创建虚拟机**。
2. 进入创建界面，选择预先制作的 cloudbase-init 虚拟机模板，参考《管理指南》，配置虚拟机的基本信息名称、计算资源、存储资源等。
3. 配置**网络设备**时，在 **Cloud-init 配置** 部分，选择虚拟机的 IP 配置方式。

   - **配置静态 IP 地址**：为虚拟机配置静态 IP 和静态路由。
   - **启用网卡 DHCP**：为虚拟机启用 DHCP 以获取动态 IP。
   - **不作配置**：不配置 IP 地址。
   > 说明：
   >
   > - 当虚拟机的网络类型为 `VPC 网络`时，如 IP 地址留空则不允许选择`配置静态 IP 地址`方式；如已填写 IP 地址并选择`配置静态 IP 地址`方式，系统将自动配置虚拟机静态 IP 为已填写的 IP 地址。
   > - 若选择**配置静态 IP 地址**，单击**下一步**之后，系统将进行 IP 地址冲突检测。若检测到冲突，您可根据需要修改 IP 地址或禁用虚拟网卡，如继续使用当前 IP 地址，可能由于 IP 地址冲突影响集群中的其他业务。
4. 在**初始化配置**部分，配置虚拟机初始化数据。

   1. 填写客户机操作系统的主机名、默认账户的密码、SSH 公钥和 DNS 等。
   2. 配置用户数据。您可以配置不超过 32 KB 的用户数据，配置示例请参考[用户数据示例](../cloudbase-init-guide/cloudbase-init-guide-04)。
5. 单击**创建**，完成虚拟机创建。

## 通过 CloudTower RESTful API/ SDK 创建虚拟机

您可以通过 CloudTower 提供的 RESTful API 和 SDK 使用模板创建虚拟机，并配置初始化数据。详情请参考 [RESTful API 描述文档](https://code.smartx.com/api)的“从内容库模版创建虚拟机”章节和 [SDK 描述文档](https://code-site.smartx.com/user-cases/content-library/#%25E9%2580%259A%25E8%25BF%2587%25E5%2586%2585%25E5%25AE%25B9%25E5%25BA%2593%25E%5B%25E2%2580%25A6%5D%25E5%25BB%25BA%25E5%25B9%25B6%25E7%25BC%2596%25E8%25BE%2591-cloud-init)。

---

## 使用 cloudbase-init > 第 6 步：确认 cloudbase-init 配置是否生效

# 第 6 步：确认 cloudbase-init 配置是否生效

使用模板创建虚拟机后，请将虚拟机开机，检查虚拟机的主机名、SSH 公钥、DNS 等初始化配置是否生效。若初始化配置未生效，需参考如下步骤，检查并修改模板的 cloudbase-init 配置文件。

**操作步骤**

更新 cloudbase-init 配置文件需将模板重新转化成虚拟机后再进行操作。您可以通过 Web 控制台和 CloudTower 将模板转化成虚拟机。下述操作以 Web 控制台为例。

1. 登录 Web 控制台，将虚拟机模板转化成虚拟机并开机。
2. 参考[第 3 步：修改 cloudbase-init 配置文件](cloudbase-init-guide-07)，更正 cloudbase-init 配置。
3. 重新初始化 cloudbase-init 的运行环境。

   删除注册表 `HKEY_LOCAL_MACHINE/SOFTWARE/Cloudbase Solutions/Cloudbase-Init/` 下相关配置。

   对于使用 `sysprep` 封装的 Windows 系统，还需参考如下命令手动执行 `sysprep`，执行完后虚拟机将自动关机。

   ```
   cd C:\Program Files\Cloudbase Solutions\Cloudbase-Init\conf
   C:\Windows\System32\Sysprep\sysprep.exe /generalize /oobe /shutdown /unattend:Unattend.xml
   ```
4. 重新将 cloudbase-init 虚拟机转化为模板，并使用模板再次创建虚拟机，检查虚拟机初始化配置是否生效。
5. 若仍存在问题，请重复以上步骤，直至 cloudbase-init 已正确配置。

---

## 后续操作注意事项

# 后续操作注意事项

**克隆 cloudbase-init 虚拟机**

cloudbase-init 数据是虚拟机的私有数据，不会随虚拟机克隆而传播。因此，克隆安装有 cloudbase-init 的虚拟机时，克隆的虚拟机无法获得相同的初始化配置，建议在克隆前先从 Guest OS 中卸载 cloudbase-init。

**卸载 cloudbase-init**

可通过单击**控制面板** > **程序（卸载程序）** 卸载 cloudbase-init。

---

## 附录 > 用户数据示例

# 用户数据示例

cloudbase-init 支持的用户数据，可参考官方文档 [Userdata](https://cloudbase-init.readthedocs.io/en/latest/userdata.html)。

本文以使用 User Data Script 和 Cloud-Config Runcmd 为例，介绍如何配置用户数据。其他复杂的应用请参考官方文档进行配置。

**User Data Script**

配置如下所示的 Shell Script，使虚拟机在第一次启动时执行命令 `echo "Hello World. The time is now $(date -R)!" >> /root/smartx.txt`。

```
#!/bin/sh
echo "Hello World.  The time is now $(date -R)!" >> /root/smartx.txt
```

**Cloud-Config Runcmd**

配置如下所示的 Cloud-Config Runcmd，使虚拟机在第一次启动时执行命令 `curl https://www.smartx.com/ -o /root/smartx.html`。

```
#cloud-config
runcmd:
 - [ curl, "https://www.smartx.com/", -o, /root/smartx.html ]
```

---

## 附录 > 已知问题

# 已知问题

- 对于使用 cloudbase-init 虚拟机模板创建的 Windows 7 和 Windows server 2016 虚拟机，开机输入密码后会系统进行三次重启，重启结束后可正常使用。
- 通过 cloudbase-init 模板创建虚拟机时不支持配置静态路由和 DHCP，需在创建后为虚拟机手动配置。
- cloudbase-init 0.9.11 稳定版在任何版本的 Windows 上都无法配置网络，请安装最新的 `Dev` 版本。

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
