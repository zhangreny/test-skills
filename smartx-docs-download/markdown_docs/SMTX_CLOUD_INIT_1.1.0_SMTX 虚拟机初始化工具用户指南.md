---
title: "SMTX_CLOUD_INIT/1.1.0/SMTX 虚拟机初始化工具用户指南"
source_url: "https://internal-docs.smartx.com/smtx-cloud-init/1.1.0/cloud-init-guide/cloud-init-guide-preface-generic"
sections: 28
---

# SMTX_CLOUD_INIT/1.1.0/SMTX 虚拟机初始化工具用户指南
## 关于本文档

# 关于本文档

本文档介绍了如何使用 SMTX 虚拟机初始化工具分别为 Linux 虚拟机和 Windows 虚拟机进行初始化配置。

---

## 更新信息

# 更新信息

**2025-07-31：配合 SMTX 虚拟机初始化工具 1.1.0 正式发布**

相较于上一版本，本版本此次更新内容如下：

- **使用虚拟机初始化工具初始化 Windows 虚拟机**：
  - **安装虚拟机初始化工具**：将 cloudbase-init 安装包由 1.1.1 更新为 1.1.4。
  - **修改配置文件**：增加拷贝 cloudbase-init-unattend.conf 配置文件的内容。
- **使用虚拟机初始化工具初始化 Linux 虚拟机 > 将虚拟机转化为虚拟机模板**：增加重置虚拟机 Machine ID 的步骤。
- **附录 > Q&A**：补充在使用虚拟机初始化工具初始化 Linux 虚拟机和 Windows 虚拟机时可能遇到的问题及解决方法。
- 对文档结构进行了优化，将《cloud-init 用户指南》和《cloudbase-init 用户指南》合并为一本文档。

---

## 概述

# 概述

在创建新虚拟机时，经常需要对虚拟机进行初始化设置，如设置主机名、IP 地址、SSH 密钥等。当批量创建虚拟机时，如对每个虚拟机手动进行初始化设置，则操作较为麻烦。在此场景下，您可为虚拟机安装 SMTX 虚拟机初始化工具，使虚拟机在首次开机时自动完成初始化设置，提高配置效率。

SMTX 虚拟机初始化工具（以下简称“虚拟机初始化工具”），以简化兼容关系、降低配置复杂度、以及避免初始化完成后的冗余为目的，在第三方工具的基础上进行了功能优化。该工具基于 cloud-init 和 cloudbase-init 而构建，旨在为 Linux 虚拟机和 Windows 虚拟机提供初始化配置支持。

- **Linux 虚拟机**

  通过 cloud-init 和 elf-python3 为虚拟机提供初始化配置支持。

  - cloud-init：支持多种 Linux 操作系统，负责执行虚拟机的初始化配置流程。
  - elf-python3：为 cloud-init 提供运行环境，确保其在隔离的 Python 环境中执行，并且能够避免与操作系统本身的 Python 环境冲突。
- **Windows 虚拟机**

  通过 cloudbase-init 和相关脚本为虚拟机提供初始化支持，支持多个版本的 Windows 操作系统。

虚拟机初始化工具可以为虚拟机自动完成一系列系统初始化配置，仅在虚拟机开机启动时执行，执行完成后立即退出，不会监听任何端口。此外，对于 Linux 虚拟机来说，虚拟机初始化工具在完成虚拟机初始化配置之后，将自动完成功能禁用，以避免影响虚拟机后续的正常使用。

ELF 平台通过使用配置了虚拟机初始化工具的虚拟机模板创建虚拟机的方式，实现对虚拟机初始化功能的支持。使用该虚拟机模板创建的新虚拟机会自动包含用户提供的初始化数据。这些数据作为数据源（被称为 config drive ISO），以 USB 磁盘形式自动挂载到虚拟机上，虚拟机内部会显示为 `QEMU HARDDISK USB Device`。在虚拟机首次启动时，它将自动读取并应用该数据源中的内容，从而达到用户预期的初始化效果。

> **注意**：
>
> 初始化过程完成后，数据源仍会保留在虚拟机中挂载，且不会对操作系统造成任何影响。

您可以使用虚拟机初始化工具完成如下初始化配置。

- 主机名
- 默认用户的密码

  - Linux 虚拟机的默认用户为 `root`
  - Windows 虚拟机的默认用户为 `Admin`。
- SSH 公钥，用于 SSH 远程登录主机
- DNS
- IP 地址，支持 DHCP 和静态 IP 配置
- 自定义用户数据，可通过设置脚本实现更多自动化配置
- 重置 Linux 虚拟机的 Machine ID

如需了解更多信息，请参考 [cloud-init 官方文档](https://cloudinit.readthedocs.io/en/latest/)和 [cloudbase-init 官方文档](https://cloudbase-init.readthedocs.io/en/latest/index.html)。

---

## 虚拟机初始化工具与虚拟机操作系统的版本配套说明

# 虚拟机初始化工具与虚拟机操作系统的版本配套说明

本版本的 SMTX 虚拟机初始化工具支持操作系统版本和固件类型在《SMTX 虚拟机初始化工具兼容性列表》上的虚拟机。您可单击[下载《SMTX 虚拟机初始化工具 1.1.0 兼容性列表》](https://cdn.smartx.com/internal-docs/assets/1e801dcd/SMTX 虚拟机初始化工具 1.1.0 兼容性列表.xlsx)，将文档下载至本地查看。

对于操作系统版本和固件类型不在上述兼容性列表，但在 SMTX 虚拟机服务兼容性列表的虚拟机，请根据 SMTX OS 集群或 SMTX ELF 集群版本参考对应的《cloud-init 虚拟机初始化配置指南》和《cloudbase-init 虚拟机初始化配置指南》进行配置。

---

## 使用虚拟机初始化工具初始化 Linux 虚拟机

# 使用虚拟机初始化工具初始化 Linux 虚拟机

请根据如下步骤使用虚拟机初始化工具初始化 Linux 虚拟机。

---

## 使用虚拟机初始化工具初始化 Linux 虚拟机 > 安装虚拟机初始化工具 > 上传并挂载虚拟机初始化工具 ISO 映像

# 上传并挂载虚拟机初始化工具 ISO 映像

请按照如下步骤上传并挂载 ISO 映像。

**前提条件**

- 请提前获取虚拟机初始化工具安装文件。
- 待挂载虚拟机初始化工具 ISO 映像的虚拟机已安装操作系统，且操作系统版本与虚拟机初始化工具兼容。

**操作步骤**

1. 请参考《CloudTower 使用指南》的“管理内容库 > 管理 ISO 映像”小节，将虚拟机初始化工具 ISO 映像上传至内容库，并分发至待挂载虚拟机所属集群。
2. 在虚拟机详情面板单击**磁盘**字段右侧的**编辑**，弹出**编辑磁盘**对话框。
3. 单击**挂载 CD-ROM** > **载入 ISO 映像**，选择虚拟机初始化工具 ISO 映像。
4. 单击**保存**。

---

## 使用虚拟机初始化工具初始化 Linux 虚拟机 > 安装虚拟机初始化工具 > 在操作系统中安装虚拟机初始化工具

# 在操作系统中安装虚拟机初始化工具

**前提条件**

请提前获取虚拟机操作系统 `root` 账户的使用权限。

**操作步骤**

下面以在操作系统 CentOS Linux 7.5 上安装为例，介绍安装虚拟机初始化工具的详细步骤。

1. 使用 root 账号通过 SSH 连接到虚拟机。

   `ssh root@<VM's IP address>`

   您也可以使用普通用户账号通过 SSH 连接到虚拟机后，使用 sudo 工具执行后续的安装命令。
2. 在客户机操作系统内挂载 ISO 映像。

   `mkdir /mnt/<dir_to_mount_iso>`

   `mount -o loop /dev/<cloudinit_iso_cdrom> /mnt/<dir_to_mount_iso>`

   - `<dir_to_mount_iso>`：用来挂载 ISO 映像的目录。
   - `<cloudinit_iso_cdrom>`：在挂载虚拟机初始化工具时，挂载 ISO 映像的 CD-ROM 的设备名称。如无法确定设备名称，可通过 lsblk 命令进行查看。例如

     - `mkdir /mnt/cdrom`
     - `mount -o loop /dev/sr0 /mnt/cdrom`
3. 执行安装脚本。

   `bash /mnt/<dir_to_mount_iso>/cloud-init/tools/install_cloud_init.sh`

   - 若当前客户机操作系统内已经安装了虚拟机初始化工具或第三方 cloud-init 程序，请根据界面提示卸载已经安装的虚拟机初始化工具，然后继续完成安装。
   - 若当前客户机操作系统内没有安装虚拟机初始化工具或第三方 cloud-init 程序，请根据界面提示完成安装。

   安装成功后您将看到 `Installation successful` 的提示。

   您也可以直接输入以下命令，默认卸载已安装的虚拟机初始化工具或第三方 cloud-init 程序并完成安装新的虚拟机初始化工具。

   `bash /mnt/<dir_to_mount_iso>/cloud-init/tools/install_cloud_init.sh --auto-yes`

---

## 使用虚拟机初始化工具初始化 Linux 虚拟机 > 将虚拟机转化为虚拟机模板

# 将虚拟机转化为虚拟机模板

**前提条件**

在将虚拟机转化为虚拟机模板之前，请确保 `/etc/cloud/` 目录下不包含名为 `cloud-init.disabled` 的禁用文件。否则使用虚拟机模板创建新的虚拟机后，虚拟机初始化程序不会启动。

**注意事项**

Linux 虚拟机在初始化时会随机生成一个 Machine ID，用于唯一标识虚拟机。当使用虚拟机模板创建新的虚拟机时，虚拟机会继承和原虚拟机相同的 Machine ID。建议在将虚拟机转化为模板前，手动重置虚拟机的 Machine ID。这个过程将会删除现有的机器标识符，并在下次启动时生成新的 machine ID，从而确保虚拟机的唯一性。

**操作步骤**

1. （可选）在已安装虚拟机初始化工具的虚拟机上执行 `cloud-init clean --machine-id` 重置命令，以将 `/etc/machine-id` 文件重置为 `uninitialized` 状态（即未初始化状态）。
2. 关闭虚拟机，并卸载已挂载虚拟机初始化工具 ISO 的 CD-ROM。若虚拟机已有网卡静态 IP 配置，则建议您手动删除配置。
3. 参考《CloudTower 使用指南》的“将虚拟机克隆或转化为虚拟机模板”小节，将虚拟机转化成虚拟机模板。

> **说明**：
>
> - 对于使用 `systemd` 服务的操作系统，若执行重置命令后，虚拟机有过开关机行为，则在最后一次关机之前需重新手动执行重置命令。
> - 对于不使用 `systemd` 服务的操作系统，执行重置命令后，`/etc/machine-id` 文件会被删除。此时，需要在通过虚拟机模板创建的新虚拟机上手动执行 `systemd-machine-id-setup` 命令，或使用 user-data 脚本让虚拟机自动执行 `systemd-machine-id-setup` 命令以生成新的 machine ID。
> - 将已安装虚拟机初始化工具的虚拟机转化成模板时，务必将`已安装虚拟机初始化工具`选项标记为**是**，否则后续通过模板创建虚拟机时无法配置初始化数据。
> - 若虚拟机在完成虚拟机初始化工具的安装配置后、转化为模板前执行过重启或关机操作，则需在最后一次关机前执行[清理虚拟机初始化实例](/smtx-cloud-init/1.1.0/cloud-init-guide/cloud-init-guide-14)的操作。

---

## 使用虚拟机初始化工具初始化 Linux 虚拟机 > 使用虚拟机模板创建虚拟机

# 使用虚拟机模板创建虚拟机

创建虚拟机模板后，可使用此模板创建虚拟机。使用模板创建虚拟机时，除了可配置一般的虚拟机参数以外，还可配置虚拟机初始化数据。初始化完成之后将自动禁用虚拟机初始化工具，以避免虚拟机重启后再次出现初始化行为。

您可以通过 Web 控制台或 CloudTower 创建虚拟机，也可以通过 RESTful API 和 CloudTower SDK 进行创建。本节仅描述使用模板创建虚拟机时的初始化配置。使用虚拟机模板创建虚拟机的详细步骤以及选项描述，请参考《SMTX OS 管理指南》的“从模板创建虚拟机”章节。

> **说明**：
>
> 克隆安装有虚拟机初始化工具的虚拟机时，为了避免影响克隆后的虚拟机启动时自动执行不必要的初始化流程，建议参考 [Linux 虚拟机卸载方式](/smtx-cloud-init/1.1.0/cloud-init-guide/cloud-init-guide-15)的步骤，在克隆的虚拟机上卸载虚拟机初始化工具。

## 通过 Web 控制台/CloudTower 创建虚拟机

通过 Web 控制台和 CloudTower 创建虚拟机的方法基本相同，此处以 CloudTower 为例。

**操作步骤**

1. 登录 CloudTower，在界面右上角单击**创建**，选择**从模板创建虚拟机**。
2. 进入创建界面，选择预先制作的虚拟机模板，参考《SMTX OS 管理指南》，配置虚拟机的基本信息名称、计算资源、存储资源等。
3. 配置**网络设备**时，在**虚拟机初始化网络配置**部分，选择虚拟机的 IP 配置方式。

   - **配置静态 IP 地址**：为虚拟机配置静态 IP 和静态路由。
   - **启用网卡 DHCP**：为虚拟机启用 DHCP 以获取动态 IP。
   - **不作配置**：不配置 IP 地址。
   > **说明**：
   >
   > - 当虚拟机的网络类型为 `VPC 网络`时，如 IP 地址留空则不允许选择`配置静态 IP 地址`方式；如已填写 IP 地址并选择`配置静态 IP 地址`方式，系统将自动配置虚拟机静态 IP 为已填写的 IP 地址。
   > - 若选择**配置静态 IP 地址**，单击**下一步**之后，系统将进行 IP 地址冲突检测。若检测到冲突，您可根据需要修改 IP 地址或禁用虚拟网卡，如继续使用当前 IP 地址，可能由于 IP 地址冲突影响集群中的其他业务。
   > - 若选择**不作配置**，虚拟机初始化工具不会在系统中生成网卡配置文件，网卡最终会由虚拟机操作系统决定被分配 DHCP 地址或不分配 IP 地址。
4. 在**初始化配置**部分，配置虚拟机初始化数据。

   1. 填写客户机操作系统的主机名、默认账户的密码、SSH 公钥和 DNS 等。
   2. 配置用户数据。您可以配置不超过 32 KB 的用户数据，配置示例请参考 [Linux 虚拟机用户数据示例](/smtx-cloud-init/1.1.0/cloud-init-guide/cloud-init-guide-04)。
5. 单击**创建**，完成虚拟机创建。

## 通过 CloudTower RESTful API/ SDK 创建虚拟机

您可以通过 CloudTower 提供的 RESTful API 和 SDK 使用模板创建虚拟机，并配置初始化数据。详情请参考 [RESTful API 描述文档](https://code.smartx.com/api)的“从内容库模版创建虚拟机”章节和 [SDK 描述文档](https://code-site.smartx.com/user-cases/content-library/#%25E9%2580%259A%25E8%25BF%2587%25E5%2586%2585%25E5%25AE%25B9%25E5%25BA%2593%25E%5B%25E2%2580%25A6%5D%25E5%25BB%25BA%25E5%25B9%25B6%25E7%25BC%2596%25E8%25BE%2591-cloud-init)。

---

## 使用虚拟机初始化工具初始化 Windows 虚拟机

# 使用虚拟机初始化工具初始化 Windows 虚拟机

请按照下述步骤使用虚拟机初始化工具初始化 Windows 虚拟机。

---

## 使用虚拟机初始化工具初始化 Windows 虚拟机 > 安装虚拟机初始化工具 > 上传并挂载虚拟机初始化工具 ISO 映像

# 上传并挂载虚拟机初始化工具 ISO 映像

请按照如下步骤上传并挂载 ISO 映像。

**前提条件**

- 请提前获取虚拟机初始化工具安装文件。
- 待挂载虚拟机初始化工具 ISO 映像的虚拟机已安装操作系统，且操作系统版本与虚拟机初始化工具兼容。

**操作步骤**

1. 请参考《CloudTower 使用指南》的“管理内容库 > 管理 ISO 映像”小节，将虚拟机初始化工具 ISO 映像上传至内容库，并分发至待挂载虚拟机所属集群。
2. 在虚拟机详情面板单击**磁盘**字段右侧的**编辑**，弹出**编辑磁盘**对话框。
3. 单击**挂载 CD-ROM** > **载入 ISO 映像**，选择虚拟机初始化工具 ISO 映像。
4. 单击**保存**。

---

## 使用虚拟机初始化工具初始化 Windows 虚拟机 > 安装虚拟机初始化工具 > 在操作系统安装虚拟机初始化工具

# 在操作系统安装虚拟机初始化工具

下面以在操作系统 Windows Server 2008 R2 上安装为例，介绍安装虚拟机初始化工具的详细步骤。

**操作步骤**

1. 挂载 SMTX 虚拟机初始化工具 ISO 之后，打开虚拟机控制台，以管理员身份登录 Windows 操作系统。
2. 双击**我的电脑**，在**文件管理器**中双击加载 SMTX 虚拟机初始化工具 ISO 映像的 CD-ROM，并进入 ISO 映像所在目录下的 cloudbase-init 目录。
3. 以管理员身份运行 `CloudbaseInitSetup_1_1_4_x64.msi` 安装包。
4. 进入 cloudbase-init 安装界面，勾选 **I accept the terms in the License Agreement**，单击 **Next**。
5. 使用默认安装路径，单击 **Next**。
6. 在 **Configuration options** 窗口中，设置用户名为 **Admin**，日志输出串口选择 **COM1**，且不勾选 **Run Cloudbase-Init service as LocalSystem**。单击 **Next** 继续。

   > **说明**：
   >
   > 您也可以自定义用户名。若选择自定义用户名，则在[拷贝配置文件](/smtx-cloud-init/1.1.0/cloud-init-guide/cloud-init-guide-19)时，需要将 `Admin` 替换为自定义用户名。
7. 单击 **Install**，在 **Completed the Cloudbase-Init Setup Wizard** 窗口，请参考如下提示进行设置：

   - 若希望通过模板创建的虚拟机生成新的 SID，请选择 **Run Sysprep to create a generalized image. This is necessary if you plan to duplicate this instance, for example by creating a Glance image** 选项，否则请取消选中此选项；
   - 取消勾选 **Shutdown when Sysprep terminates** 选项，否则 sysprep 执行完后会立即重启虚拟机。

     > **注意**：
     >
     > 若通过 cloudbase-init 执行 sysprep，请确保**剩余 Windows 重置计数**大于等于 1，否则无法执行 sysprep 封装。可通过执行 `slmgr.vbs /dlv` 命令查看**剩余 Windows 重置计数**。
8. 若在步骤 7 中勾选了 **Run Sysprep to create a generalized image. This is necessary if you plan to duplicate this instance, for example by creating a Glance image** 选项，请在保持安装对话框打开的情况下，执行[拷贝配置文件](/smtx-cloud-init/1.1.0/cloud-init-guide/cloud-init-guide-19)的操作。
9. 在对话框中单击 **Finish**，完成安装。

安装后，可在控制面板中单击**管理工具** > **服务**，若存在 cloudbase-init 服务，则表明安装成功。

---

## 使用虚拟机初始化工具初始化 Windows 虚拟机 > 拷贝配置文件

# 拷贝配置文件

请在安装 ISO 映像所在的目录下的 `cloudbase-init` 目录中，找到 `cloudbase-init.conf` 配置文件和 `cloudbase-init-unattend.conf` 配置文件，并将配置文件拷贝到 `C:\Program Files\Cloudbase Solutions\Cloudbase-Init\conf\` 目录下（如果该目录已存在配置文件则需要先删除相应文件再进行拷贝）。

> **说明**：
>
> - 若您在[在操作系统安装虚拟机初始化工具](/smtx-cloud-init/1.1.0/cloud-init-guide/cloud-init-guide-18)的步骤 8 中已执行拷贝配置文件操作，则无需重复执行。
> - 若您在[在操作系统安装虚拟机初始化工具](/smtx-cloud-init/1.1.0/cloud-init-guide/cloud-init-guide-18)的步骤 6 中修改了默认用户名，则在安装完成后，需要修改拷贝后的 `cloudbase-init.conf` 和 `cloudbase-init-unattend.conf` 配置文件，将 `username` 字段中的 `Admin` 替换为安装时指定的用户名。

---

## 使用虚拟机初始化工具初始化 Windows 虚拟机 > 将虚拟机转化为虚拟机模板

# 将虚拟机转化为虚拟机模板

**完成虚拟机初始化工具的安装配置后，请关闭虚拟机，并卸载已挂载 SMTX 虚拟机初始化工具 ISO 的 CD-ROM**。若虚拟机已有网卡静态 IP 配置文件，则建议您手动删除该文件。然后再参考《CloudTower 使用指南》的“将虚拟机克隆或转化为虚拟机模板”章节，将虚拟机转化成虚拟机模板。

> **注意**：
>
> 将已安装虚拟机初始化工具的虚拟机转化成模板时，务必将`已安装虚拟机初始化工具` 选项标记为**是**，否则后续通过模板创建虚拟机时无法配置初始化数据。

---

## 使用虚拟机初始化工具初始化 Windows 虚拟机 > 使用虚拟机模板模板创建虚拟机

# 使用虚拟机模板创建虚拟机

将已安装虚拟机初始化工具的虚拟机转化为虚拟机模板后，可使用此模板创建虚拟机。使用模板创建虚拟机时，除可配置一般的虚拟机参数，还可配置虚拟机初始化数据。

您可以通过 Web 控制台或 CloudTower 创建虚拟机，也可以通过 RESTful API 和 CloudTower SDK 进行创建。本节仅描述使用虚拟机模板创建虚拟机过程中的初始化配置。使用虚拟机模板创建虚拟机的详细步骤以及选项描述，请参考《SMTX OS 管理指南》的“从模板创建虚拟机”章节。

> **说明**：
>
> 克隆安装有虚拟机初始化工具的虚拟机时，为了避免影响克隆后的虚拟机启动时自动执行不必要的初始化流程，建议参考 [Windows 虚拟机卸载方式](/smtx-cloud-init/1.1.0/cloud-init-guide/cloud-init-guide-25)的步骤，在克隆的虚拟机上卸载虚拟机初始化工具。

## 通过 Web 控制台/CloudTower 创建虚拟机

通过 Web 控制台和 CloudTower 创建虚拟机的方法基本相同，此处以 CloudTower 为例。

**操作步骤**

1. 登录 CloudTower，在界面右上角单击**创建**，选择**从模板创建虚拟机**。
2. 进入创建界面，选择预先制作的 cloudbase-init 虚拟机模板，参考《SMTX OS 管理指南》，配置虚拟机的基本信息名称、计算资源、存储资源等。
3. 配置**网络设备**时，在**虚拟机初始化网络配置**部分，选择虚拟机的 IP 配置方式。

   - **配置静态 IP 地址**：为虚拟机配置静态 IP 和静态路由。
   - **启用网卡 DHCP**：为虚拟机启用 DHCP 以获取动态 IP。
   - **不作配置**：不配置 IP 地址。
   > **说明**：
   >
   > - 当虚拟机的网络类型为 `VPC 网络`时，如 IP 地址留空则不允许选择`配置静态 IP 地址`方式；如已填写 IP 地址并选择`配置静态 IP 地址`方式，系统将自动配置虚拟机静态 IP 为已填写的 IP 地址。
   > - 若选择**配置静态 IP 地址**，单击**下一步**之后，系统将进行 IP 地址冲突检测。若检测到冲突，您可根据需要修改 IP 地址或禁用虚拟网卡，如继续使用当前 IP 地址，可能由于 IP 地址冲突影响集群中的其他业务。
   > - 若选择**不作配置**，虚拟机初始化工具不会在系统中生成网卡配置文件，网卡最终会由虚拟机操作系统决定被分配 DHCP 地址或不分配 IP 地址。
4. 在**初始化配置**部分，配置虚拟机初始化数据。

   1. 填写客户机操作系统的主机名、默认账户的密码、SSH 公钥和 DNS 等。
   2. 配置用户数据。您可以配置不超过 32 KB 的用户数据，配置示例请参考 [Windows 虚拟机用户数据示例](/smtx-cloud-init/1.1.0/cloud-init-guide/cloud-init-guide-26)。
5. 单击**创建**，完成虚拟机创建。

## 通过 CloudTower RESTful API/ SDK 创建虚拟机

您可以通过 CloudTower 提供的 RESTful API 和 SDK 使用模板创建虚拟机，并配置初始化数据。详情请参考 [RESTful API 描述文档](https://code.smartx.com/api)的“从内容库模版创建虚拟机”章节和 [SDK 描述文档](https://code-site.smartx.com/user-cases/content-library/#%25E9%2580%259A%25E8%25BF%2587%25E5%2586%2585%25E5%25AE%25B9%25E5%25BA%2593%25E%5B%25E2%2580%25A6%5D%25E5%25BB%25BA%25E5%25B9%25B6%25E7%25BC%2596%25E8%25BE%2591-cloud-init)。

---

## 运维管理 > 禁用虚拟机初始化工具（仅针对 Windows 虚拟机）

# 禁用虚拟机初始化工具（仅针对 Windows 虚拟机）

使用虚拟机初始化工具为 Linux 虚拟机完成初始化配置之后，虚拟机初始化工具将自动被禁用，因此您无需手动执行禁用操作。

使用虚拟机初始化工具为 Windows 虚拟机完成初始化配置后初始化之后，为了避免虚拟机重启之后出现再次初始化的行为，您可通过以下两种方式禁用虚拟机初始化工具。

**方式一**：在 cloudbase-init > tools 目录中以管理员身份执行 `disable_cloudbase_init.bat` 脚本禁用 cloudbase-init。

**方式二**：依次单击**控制面板** > **管理工具** > **服务**，右键单击 cloudbase-init 服务，选择**属性**，将服务的启动类型修改为**禁用**，并单击**保存**。

---

## 运维管理 > 清理虚拟机初始化实例

# 清理虚拟机初始化实例

在以下场景中需要清理虚拟机初始化实例：

- 当通过虚拟机模板创建的虚拟机因依赖服务异常而未按预期运行时，可通过执行如下操作进行修复：

  1. 将该模板重新转换为虚拟机，并修改相关配置。
  2. 清理虚拟机初始化实例，恢复虚拟机到初始状态。
  3. 关机后，将虚拟机重新转换为模板。
- 如果需要将已通过虚拟机初始化工具进行初始化的虚拟机重新转化为模板，需执行以下操作：

  1. 清理虚拟机初始化实例，恢复虚拟机到初始状态。
  2. 关机后，将虚拟机重新转化为模板。

---

## 运维管理 > 清理虚拟机初始化实例 > 清理 Linux 虚拟机初始化实例方式

# 清理 Linux 虚拟机初始化实例方式

支持使用以下两种方式进行清理：

- 使用 `cloud-init clean --logs --seed --disabled` 命令可直接清理。
- 参考[在操作系统中安装虚拟机初始化工具](/smtx-cloud-init/1.1.0/cloud-init-guide/cloud-init-guide-06)部分，执行 `bash /mnt/<dir_to_mount_iso>/cloud-init/tools/clean_cloud_init.sh` 清理虚拟机初始化实例。若提示 `cloud-init configuration cleanup completed` 则表明清理成功。

> **说明**：
>
> 如果虚拟机中存在因初始化行为而产生的网卡静态 IP 配置文件，则需要您手动删除。

---

## 运维管理 > 清理虚拟机初始化实例 > 清理 Windows 虚拟机初始化实例方式

# 清理 Windows 虚拟机初始化实例方式

支持通过以下两种方式进行清理：

- 删除虚拟机初始化工具的相关注册表项即可完成清理。其中，注册表项位于 `HKEY_LOCAL_MACHINE\SOFTWARE\Cloudbase Solutions`。
- 参考[在操作系统中安装虚拟机初始化工具](/smtx-cloud-init/1.1.0/cloud-init-guide/cloud-init-guide-18)小节，以管理员身份执行 `clean_cloudbase_init.bat` 脚本清理虚拟机初始化实例。

---

## 运维管理 > 卸载虚拟机初始化工具 > Linux 虚拟机卸载方式

# Linux 虚拟机卸载方式

在使用虚拟机初始化工具对 Linux 虚拟机完成初始化配置之后，虚拟机初始化工具将自动被禁用，因此后续使用虚拟机时不必将其卸载。

您也可以执行如下命令，默认卸载已安装的虚拟机初始化工具。

`bash /mnt/<dir_to_mount_iso>/cloud-init/tools/uninstall_cloud_init.sh --auto-yes`

---

## 运维管理 > 卸载虚拟机初始化工具 > Windows 虚拟机卸载方式

# Windows 虚拟机卸载方式

若完成初始化配置后手动禁用了虚拟机初始化工具，则无需卸载。否则，则可通过单击**控制面板** > **程序（卸载程序）** 进行卸载。卸载完成后，你可根据需要删除 `C:\Program Files\Cloudbase Solutions` 安装目录。

---

## 附录 > 用户数据示例 > Linux 虚拟机用户数据示例

# Linux 虚拟机用户数据示例

虚拟机初始化工具支持的 Linux 虚拟机用户数据可参考以下官方文档。

- [User-Data Formats](https://cloudinit.readthedocs.io/en/latest/topics/format.html)
- [Cloud Config Examples](https://cloudinit.readthedocs.io/en/latest/topics/examples.html)
- [Modules](https://cloudinit.readthedocs.io/en/latest/topics/modules.html)

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

## 附录 > 用户数据示例 > Windows 虚拟机用户数据示例

# Windows 虚拟机用户数据示例

虚拟机初始化工具支持的 Windows 虚拟机用户数据，可参考官方文档 [Userdata](https://cloudbase-init.readthedocs.io/en/latest/userdata.html)。

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

- 对于使用虚拟机模板创建的 Windows 7 和 Windows server 2016 虚拟机，开机输入密码后会系统进行三次重启，重启结束后可正常使用。
- 通过模板创建虚拟机时不支持配置静态路由和 DHCP，需在创建后为虚拟机手动配置。
- 在未选择通过虚拟机初始化工具配置网络或配置 DHCP 网络的情况下，ConfigDrive 提供的数据不满足虚拟机初始化工具对于网络配置的数据格式要求，因此 DNS Server 配置不生效。

---

## 附录 > Q&A

# Q&A

以下列举了在使用虚拟机初始化工具初始化 Linux 虚拟机和 Windows 虚拟机时，可能出现的一些问题及相应的解决方法。当您在使用虚拟机初始化工具的过程中遇到问题时，可查阅本章节进行问题定位，并根据提供的解决方法解决问题。

---

## 附录 > Q&A > 使用虚拟机初始化工具初始化 Linux 虚拟机

# 使用虚拟机初始化工具初始化 Linux 虚拟机

## Q：通过 cloud-init 配置 DNS 时，cloud-init 正常执行，为什么 DNS 没有生效

A: 该问题可能是由于虚拟机模版 `/etc/resolv.conf` 文件已存在 3 个 DNS 配置导致，使用 `/etc/resolv.conf` 配置 DNS 的 Linux 发行版都会有此限制。cloud-init 基于 resolv.conf 实现 DNS 配置，且配置方式为增加 DNS，不会取代原有的 DNS。根据 [resolv.conf(5)](https://man7.org/linux/man-pages/man5/resolv.conf.5.html)的限制，resolv.conf 中最多只能配置 3 个 DNS。

因此，若虚拟机模版 `/etc/resolv.conf` 文件已配置了 3 个 DNS，通过 cloud-init 配置 DNS 将会失败，在 `/var/log/cloud-init.log` 中也会输出 `ignoring nameserver {dns_server}: adding would exceed the maximum of '3' name servers (see resolv.conf(5))` 日志。

## Q：使用 eni 网络配置工具的操作系统（如果 Debian 操作系统）通过 cloud-init 配置 DNS 时，cloud-init 正常执行，为什么 DNS 没有生效

A: 该问题可能是由于虚拟机在使用 eni 网络配置工具来配置网络时，一般搭配 `resolvconf.service` 服务来配置 DNS。某些操作系统可能未安装该服务，导致 DNS 配置失败，需要在制作虚拟机模版时安装 `resolvconf.service` 服务并确保该服务开机自动启动。

## Q: 使用 Netplan 网络配置工具的操作系统（如 Kylin Desktop v10 操作系统）通过 cloud-init 配置静态 IP 网络时，cloud-init 正常执行，为什么静态 IP 配置、路由、DNS 均未生效？

A: 该问题可能是由于虚拟机的 Netplan 网络配置工具使用 `systemd-networkd` 服务来管理网络。但是 `systemd-networkd` 服务并未设置开机自启动，虽然 cloud-init 服务已经将预期的网络配置写入 Netplan 的配置目录下，但由于 `systemd-networkd` 服务处于未启动状态，所以会导致配置网络失败。

此时使用 `netplan apply` 命令可以启动 `systemd-networkd` 服务并应用相关配置，观察到网络配置恢复后，可确认符合该问题的描述。解决方式是在制作 cloud-init 虚拟机模版时使用 `systemctl enable systemd-networkd` 命令将该服务设置开机自动启动。

## Q：使用 Netplan 网络配置工具的操作系统（如 Ubuntu 18.04 系统）通过 cloud-init 配置静态 IP 网络时，cloud-init 正常执行，为什么静态 IP 配置没有生效？

A：该问题可能是由于在在 `/etc/netplan` 目录中存在多个配置文件，例如 `01-network-manager-all.yaml` 和 `50-cloud-init.yaml`，系统将按照顺序依次处理配置文件。因此，如果存在多个配置文件，可能会导致配置冲突，从而影响网络设置的效果。

例如，假设 `01-network-manager-all.yaml` 文件对虚拟网卡 ens4 设置了 DHCP 配置，那么这个设置可能会覆盖或干扰 `50-cloud-init.yaml` 文件中对 ens4 的配置。另外，假设 `01-network-manager-all.yaml` 文件中包含了不存在的网卡配置，也可能会导致网络配置失败，进而导致`50-cloud-init.yaml` 文件的配置无法生效。

建议将 `01-network-manager-all.yaml` 文件备份并从 `/etc/netpalan` 目录中移除后，重新制作 cloud-init 模板并创建 cloud-init 虚拟机。

## Q：使用 eni 网络配置工具的操作系统（如 Debian 或 Ubuntu 16.04 系统）通过 cloud-init 配置静态 IP 网络时，cloud-init 正常执行，为什么静态 IP 配置没有生效？

A：这个问题可能是由于没有正确配置 `/etc/network/interfaces` 文件，而导致

由于 cloud-init 会将网络配置信息写入 `/etc/network/interfaces.d/50-cloud-init.cfg` 文件
，若没有正确配置 `/etc/network/interfaces` 文件，将导致 `50-cloud-init.cfg` 配置失效，从而导致静态 IP 配置没有生效。

请根据以下要求配置`/etc/network/interfaces` 文件。

1. 包含 source 语句

   `/etc/network/interfaces` 文件必须包含以下行，以确保能够加载 `/etc/network/interfaces.d/*` 目录中的配置文件：

   `source /etc/network/interfaces.d/*`
2. 避免冲突

   `/etc/network/interfaces` 文件中不应包含与 `/etc/network/interfaces.d/50-cloud-init.cfg` 文件中指定的网卡相同的配置，以防止配置冲突。

以下是符合要求的 `/etc/network/interfaces` 文件示例，其中只配置了回环接口 lo：

```
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback
```

建议修改为上述配置，以确保 `50-cloud-init.cfg` 文件中的网络设置能够正确加载并生效。

## Q: 使用 eni 网络配置工具的操作系统（如 Ubuntu Server 18.04 操作系统）通过虚拟机初始化工具配置静态 IP 网络时，为什么静态 IP 配置、路由、DNS 均未生效？

A: 该问题可能是由于虚拟机中同时存在 eni 网络配置工具和 Netplan 网络配置工具，且 Netplan 配置工具优先级更高。因此虚拟机初始化工具在执行初始化流程时，会自动选择 Netplan 配置工具。但由于 Netplan 配置工具的后端服务 systemd-networkd 服务未被启用，最终导致网络配置失败。

在这种情况下，您需要在将虚拟机转化为虚拟机模板前，编辑 `/etc/cloud/cloud.cfg` 文件，将 `network.renderers` 配置项中的 `eni` 字段调整为列表中的第一个元素。

## Q: 使用 NetworkManager 网络配置工具的操作系统（如 Debian、OPENSUSE、Fedora、UOS 操作系统的某些版本）通过虚拟机初始化工具配置 DNS 时，为什么 DNS 的配置信息有时在 `/etc/resolv.conf` 文件中显示而有时不会显示？

A：当使用 NetworkManager 配置 DNS 时，DNS 配置会存储在 NetworkManager 的网卡配置中，而在不同的操作系统中， `/etc/resolv.conf` 文件的内容可能由不同的系统服务管理，因此可能会出现以下几种情况：

- **DNS 由 resolvconf 服务管理**（例如 Debian 11 操作系统）

  此时，`/etc/resolv.conf` 是一个符号链接，指向 `/run/resolvconf/resolv.conf`。NetworkManager 不会直接将 DNS 写入 `/etc/resolv.conf`，而是将其写入 `/run/resolvconf/resolv.conf`。由于 `/etc/resolv.conf` 指向 `/run/resolvconf/resolv.conf`，因此 DNS 配置可以直接在 `/etc/resolv.conf` 文件中显示。
- **DNS 由 systemd-resolved 服务管理**（例如 Fedora 36 操作系统）

  此时，`/etc/resolv.conf` 是一个符号链接，指向 `/run/systemd/resolve/stub-resolv.conf` 或 `/run/systemd/resolve/resolv.conf`。

  - 当指向 `/run/systemd/resolve/stub-resolv.conf` 时（存根模式）：

    由于 `/etc/resolv.conf` 文件仅包含一个本地 DNS 地址（127.0.0.53），所有 DNS 请求会通过 systemd-resolved 服务处理。因此只有 systemd-resolved 服务才记录了配置 DNS 服务器的服务，而 `/etc/resolv.conf` 文件中不会显示真实的 DNS 服务器 IP。

    在这种情况下，您可使用命令 `resolvectl status` 查看当前生效的 DNS 配置。或者手动将存根模式切换为非存根模式。
  - 当指向 `/run/systemd/resolve/resolv.conf` 时（非存根模式）：

    此时 `/etc/resolv.conf` 文件中会显示真实的 DNS 服务器 IP（由 systemd-resolved 服务生成）。
- **DNS 由 NetworkManager 直接管理**（例如 UOS 20 操作系统）

  此时，`/etc/resolv.conf` 文件不是一个符号链接。在这种情况下，NetworkManager 会直接将 DNS 配置写入 `/etc/resolv.conf` 文件。因此，可以在 `/etc/resolv.conf` 文件中直接显示。

需要注意的是，如果 `/etc/resolv.conf` 文件不是一个符号链接，并且在将虚拟机转化为虚拟机模板之前，虚拟机已经配置了 DNS（`/etc/resolv.conf` 文件中包含 "Generated by VMTools" 注释）。那么在通过虚拟机模板创建虚拟机时使用虚拟机初始化工具配置 DNS 时，NetworkManager 将无法将 DNS 配置写入该文件。为了让 DNS 配置生效，需要修改 `/etc/NetworkManager/NetworkManager.conf` 配置文件，在 dns=none 这一行开头加上 `#` ，并重启 NetworkManager 服务。

## Q: 为什么在某些操作系统（如 CentOS 7.0）通过虚拟机初始化工具配置主机名时，主机名未生效？

A: 在 CentOS 7.0 操作系统中，通过虚拟机初始化工具配置主机名时，可能会出现主机名未生效的情况（但这不会影响初始化流程的正常进行）。这是因为 CentOS 7.0 版本在配置主机名时需要关闭 SELinux 才能生效。若 SELinux 启用，主机名配置命令行可能会被阻止，从而导致配置失败。

上述情况可能是因为系统中启用了 SELinux。SELinux 启用后，主机配置命令可能会被阻止，从而导致配置失败。请在将虚拟机转化为虚拟机模板之前，关闭 SELinux。

## Q: 为什么在使用 NetworkManager 网络配置工具的操作系统（如 Debian、openSUSE、Fedora、UOS 等某些版本）通过虚拟机初始化工具配置静态 IP 时，静态 IP 配置没有生效？

A: 在使用 NetworkManager 网络配置工具的操作系统中（如 Debian、openSUSE、Fedora、UOS 等），默认情况下，NetworkManager 会管理所有的网络接口，这可能导致与传统的 eni 或其他网络配置工具产生冲突。如果 `/etc/network/interfaces.d/` 或 `/etc/netplan/` 目录下存在与 NetworkManager 配置文件（例如 /etc/NetworkManager/system-connections/cloud-init-ens4.nmconnection）冲突的网卡配置，静态 IP 配置可能无法生效。

您可以通过如下步骤解决该问题：

1. 检查并删除任何与 NetworkManager 配置冲突的网卡配置文件。
2. 重启 NetworkManager 服务，使其管理的网卡配置生效。

## Q：当在部分操作系统（如银河麒麟桌面版 V10 SP1）中通过 cloud-init 配置包含 `!` 的 root 密码时，cloud-init 执行成功，但实际密码为什么未生效？

A：因为在 Bash 中，`!` 是一个特殊字符，用于历史命令扩展。当密码中包含 `!` 时，Bash 会将其误认为是历史命令的引用，从而导致密码不生效。

您可按照如下步骤在虚拟机模板 Guest OS 中永久关闭 histexpand，以消除 `!` 的解析冲突。

1. 执行如下命令打开 /etc/bash.bashrc 文件。

   `vim /etc/bash.bashrc`
2. 在文件末尾添加 `set +H`。
3. 保存并退出编辑器。
4. 执行以下命令使配置立即生效。

   `source /etc/bash.bashrc`

> **说明**：
>
> 如果后期仍需使用此功能，可在创建虚拟机后自行开启。

---

## 附录 > Q&A > 使用虚拟机初始化工具初始化 Windows 虚拟机

# 使用虚拟机初始化工具初始化 Windows 虚拟机

## Q：Windows 操作系统使用 cloudbase-init 配置虚拟机，虚拟机初次开机后，为什么相关配置没有生效？

A：该问题通常是由于虚拟机初始化工具在使用本地数据源进行初始化时，未等待磁盘挂载成功就开始运行的情况。在某些情况下（例如集群开启了 boost 模式）虚拟机的服务启动速度较快，虚拟机初始化工具没有在操作系统挂载完所有硬盘后就进行了初始化，从而导致无法获取到本地数据源，最终导致配置失效。

为解决此问题，可以通过替换部分源代码文件来实现延迟等待数据源加载。具体步骤如下：

1. 在安装 ISO 映像所在目录的 `cloudbase-init` 目录中，找到 `baseconfigdrive.py` 配置文件。
2. 将该配置文件复制到 `C:\Program Files\Cloudbase Solutions\Cloudbase-Init\Python\Lib\site-packages\cloudbaseinit\metadata\services` 目录，并替换原有文件。
3. 修改 `C:\Program Files\Cloudbase Solutions\Cloudbase-Init\conf\` 目录下的 `cloudbase-init.conf` 配置文件，新增如下配置：

   ```
   retry_count=4
   retry_count_interval=5
   ```
4. 重新启动虚拟机操作系统。

## Q：在 Windows 10 操作系统安装虚拟机初始化工具时，勾选了“Run Sysprep to create a generalized image”，为什么提示“Sysprep 无法验证你的 Windows 安装”？

A：出现此问题通常是由于某些已安装的 Windows 应用程序包与 Sysprep 工具发生冲突。根据 `%WINDIR%\System32\Sysprep\Panther\setupact.log` 错误日志中的信息，错误源自执行 `Sysprep_Clean_Validate_Opk` 时出现问题，错误代码为 `0x139f`。

**解决方法**：

1. 使用 管理员权限 打开 PowerShell。
2. 运行以下命令，查找并移除以下冲突的应用程序包：
   `Get-AppxPackage -AllUsers | Where-Object { $_.PackageFullName -like "Microsoft.VCLibs.110.00*" }`
3. 根据上一步的输出，移除输出中的所有包，例如：

   在 PowerShell 中依次执行以下命令：

   ```
   Remove-AppxPackage -Package "Microsoft.VCLibs.110.00_11.0.51106.1_x86__8wekyb3d8bbwe"
   Remove-AppxPackage -Package "Microsoft.WinJS.2.0_1.0.9600.17018_neutral__8wekyb3d8bbwe"
   Remove-AppxPackage -Package "Microsoft.Media.PlayReadyClient.2_2.11.2154.0_x86__8wekyb3d8bbwe"
   ```

这些步骤会移除导致冲突的应用程序包，此时卸载虚拟机初始化工具，重启虚拟机后重新安装虚拟机初始化工具即可。

## Q：在 Windows 11 操作系统安装虚拟机初始化工具时，勾选了“Run Sysprep to create a generalized image”，为什么提示“Sysprep 无法验证你的 Windows 安装”？

A：该问题需要根据 %WINDIR%\System32\Sysprep\Panther\setupact.log 错误日志中的信息具体分析。

- 如果错误信息为：`Audit mode cannot be turned on if reserved storage is in use. An update or servicing operation may be using reserved storage`

  出现此问题通常是因为启用了保留存储（Reserved Storage），并且可能有更新或服务操作正在使用保留存储。在执行 Sysprep\_Clean\_Validate\_Opk 时，错误代码 0x975 表示无法启用审计模式，因为保留存储正在使用。

  **解决方法**：

  1. 禁用 Windows 更新并等待至少 1 周，以确保没有更新或服务操作占用保留存储。
  2. 在此期间，可以参考官方文档 Sysprep Error - Clean Validate OPK 进行更进一步的排查。

  禁用 Windows 更新并等待一段时间后，卸载虚拟机初始化工具，重启虚拟机后重新安装虚拟机初始化工具即可。
- 如果错误信息为：`Error SYSPRP Failed to remove apps for the current user: 0x80073cf2`

  这个问题通常是由于 Windows 11 中某些预装应用程序阻止 Sysprep 的执行。

  **解决方法**：

  1. 使用 PowerShell 移除日志中阻止 Sysprep 运行的安装包后再次尝试，例如如下安装包会阻止 Sysprep 运行，需要在管理员模式下打开 PowerShell，执行以下命令：

  ```
  Get-AppxPackage Microsoft.OneDriveSync | Remove-AppxPackage
  Get-AppxPackage MicrosoftWindows.Client.WebExperience | Remove-AppxPackage
  Get-AppxPackage Microsoft.LanguageExperiencePacken-GB | Remove-AppxPackage
  Get-AppxPackage Microsoft.LanguageExperiencePackzh-CN | Remove-AppxPackage 
  Get-AppxPackage Microsoft.WidgetsPlatformRuntime | Remove-AppxPackage
  ```

  2. 执行完成后，卸载虚拟机初始化工具，重启虚拟机后重新安装虚拟机初始化工具即可。

## Q：在 Windows 操作系统安装虚拟机初始化工具时，出现提示“api-ms-win-crt-runtime-l1-1-0.dll is missing from your computer”，该如何解决？

A：这个错误通常是因为缺少 `Microsoft Visual C++ Redistributable` 中的运行时库。为了解决此问题，可以通过以下步骤修复：

1. 下载并安装 Microsoft Visual C++ Redistributable（vc\_redist.exe）。
2. 安装完成后，重新启动虚拟机。

安装完成后，系统应能正确识别所需的 DLL 文件，解决缺少文件的问题。详情请参考文档：[API-MS-WIN-CRT-RUNTIME-L1-1-0.DLL 错误解决方法](https://learn.microsoft.com/zh-tw/answers/questions/3277665/api-ms-win-crt-runtime-l1-1-0-dll)。

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
