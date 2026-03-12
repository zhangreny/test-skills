---
title: "SMTXOS/6.3.0/VAAl-NAS 插件安装与升级指南"
source_url: "https://internal-docs.smartx.com/smtxos/6.3.0/vaainas/vaai_nas_installtion_upgrade/vaai_nas_installtion_upgrade_01"
sections: 12
---

# SMTXOS/6.3.0/VAAl-NAS 插件安装与升级指南
## 关于本文档

# 关于本文档

本文档介绍了当 SMTX OS 结合 VMware ESXi 平台以超融合的形态进行部署时，在 ESXi 主机上安装和升级 VAAI-NAS 插件的操作方法。

---

## 更新信息

# 更新信息

- **2026-02-04：更新 VAAI-NAS 插件可兼容的 SMTX OS 版本说明**
- **2025-01-22：删除与 ESXi 6.x 配套的 VAAI-NAS 插件版本的安装、升级步骤，并更新VAAI-NAS 插件可兼容的 SMTX OS 版本**
- **2024-09-20：更新 VAAI-NAS 插件可兼容的 SMTX OS 版本说明**
- **2024-06-13：增加 ESXi 8.0 U1a 后续版本的适配信息**
- **2023-08-01：增加 ESXi 8.0 U1a 版本的适配信息**
- **2022-10-13：配合 1.3-3 和 2.1-4 版本软件正式发布**

  软件新发布 **1.3-3** 和 **2.1-4** 版本，其中 **1.3-3** 版本支持 ESXi 6.5 P06 及后续版本和 ESXi 6.7 P03 及后续版本；**2.1-4** 版本支持 ESXi 7.0 U2 及后续版本，并获得 VMware 官方认证。
- **2022-07-12：配合 1.3-2 版本软件正式发布**

  软件新发布 **1.3-2** 版本，该版本支持 ESXi 6.5 P06 及后续版本和 ESXi 6.7 P03 及后续版本，并且已获得 VMware 的官方认证。
- **2022-06-01：配合 2.1-3 版本软件正式发布**

  软件新发布 **2.1-3** 版本，该版本已获得 VMware 的官方认证。
- **2021-11-08：配合 2.1-2 版本软件正式发布**

  软件新发布 **2.1-2** 版本，该版本支持 ESXi 7.0 U2 及后续版本，并且已获得 VMware 的官方认证。
- **2020-12-11：更新软件升级逻辑和下载路径**

  由于 1.3-1 版本的 VAAI-NAS 插件获得 VMware 的官方认证，且支持 SMTX OS 3.0.X、3.5.X 及 4.0.X 所有版本，但 VMware 官方只支持 ESXi 6.5 和 6.7 版本，基于此手册更新了软件升级逻辑和下载路径。
- **2020-11-12：配合 1.3-1 版本软件第一次发布**

---

## 安装或升级 VAAI-NAS 插件的原则

# 安装或升级 VAAI-NAS 插件的原则

SMTX OS（读作 SmartX OS）结合 VMware ESXi 平台以超融合的形态进行部署时，通过 NFS 为 VMware 虚拟机提供存储服务。为支持 NFS 文件的厚置备模式和快速克隆文件等功能，SmartX 同时提供了 SMTX VAAI-NAS 插件（简称 “VAAI-NAS 插件”），并已获得 [VMware 官方认证](https://compatibilityguide.broadcom.com/detail?program=san&productId=39807&persona=live)。

SmartX 最新发布的 2.1-4 版本的 VAAI-NAS 插件可以兼容 SMTX OS 5.x.x、6.0.x、6.1.x、6.2.x 和 6.3.x 的所有版本，并且可以适配 ESXi 7.0 U2 及后续版本，ESXi 8.0 U1a 及后续版本。

为避免升级或安装 VAAI-NAS 插件失败，请先根据当前的 VMware ESXi 虚拟化平台版本，参考以下原则，评估是否需要安装或升级 SMTX VAAI-NAS 插件。

| **ESXi 版本** | **安装或升级建议** |
| --- | --- |
| VMware ESXi 7.0 U2 及后续版本 | 直接安装或升级至 **2.1-4** 版本。 |
| VMware ESXi 8.0 U1a 及后续版本 |
| VMware ESXi 7.0 GA | 请勿直接安装或者升级 VAAI-NAS 插件，可以参考以下两种方案：  - 先升级 ESXi 至上述适配版本，然后再安装或升级至 2.1-4 版本的 VAAI-NAS 插件。 - 不安装或升级 VAAI-NAS 插件，保持现状。 |
| VMware ESXi 7.0b |
| VMware ESXi 7.0 U1 |

---

## 判断 ESXi 主机是否需要安装或升级 VAAI-NAS 插件

# 判断 ESXi 主机是否需要安装或升级 VAAI-NAS 插件

1. 打开 ESXi 主机 SSH 服务，通过 SSH Client 连接到 ESXi。
2. 执行如下命令，检查当前 ESXi 主机是否已安装 VAAI-NAS 插件。若已安装，请继续确定插件版本。

   `esxcli software vib list | grep -i zbs`

   - 系统无输出，表明当前系统未安装 VAAI-NAS 插件，请参考[安装或升级 VAAI-NAS 插件的原则](vaai_nas_installtion_upgrade_05)和[安装 VAAI-NAS 插件](vaai_nas_installtion_upgrade_09)，完成 VAAI-NAS 插件的安装。
   - 系统输出的版本低于配套 ESXi 主机的 VAAI-NAS 插件版本，请参考[安装或升级 VAAI-NAS 插件的原则](vaai_nas_installtion_upgrade_05)和[升级 VAAI-NAS 插件](vaai_nas_installtion_upgrade_10)，完成 VAAI-NAS 插件的升级。
   - 系统输出的版本与配套 ESXi 主机的 VAAI-NAS 插件版本相同，则无需安装或者升级 VAAI-NAS 插件。

---

## 安装 VAAI-NAS 插件

# 安装 VAAI-NAS 插件

本章将介绍如何安装 2.1-4 版本的 VAAI-NAS 插件。

**前提条件**

- VMware ESXi 主机版本为 ESXi 7.0 U2 及后续版本，或 ESXi 8.0 U1a 及后续版本。
- 已下载适配 ESXi 主机版本的 SMTX VAAI-NAS 插件安装文件。

**操作步骤**

1. 打开 ESXi 主机 SSH 服务，通过 SSH Client 连接到 ESXi。
2. 将 VAAI-NAS 插件的安装文件拷贝至 ESXi 主机的根目录中。
3. 依次执行如下命令：

   - `/etc/init.d/vaai-nasd stop`
   - `esxcli software component apply -d /SMX-ZBSNasPlugin_2.1-4.zip`

     执行完后，系统将输出以下信息：

     ```
     Installation Result
         Components Installed: SMX-ZBSNasPlugin_1.0-0.0.0008
         Components Removed:
         Components Skipped:
         Message: Operation finished successfully.
         Reboot Required: false
     ```
   - `/etc/init.d/vaai-nasd start`
4. 输入以下命令检查安装是否成功。请注意核对显示的版本号与安装的版本号是否一致。

   `esxcli software vib list | grep -i zbs`
5. 输入以下命令检查 VAAI-NAS 插件是否正常工作。

   `esxcli storage nfs list`

   - 若系统执行命令后无任何信息输出，表明系统未挂载 NFS 存储，请在挂载 NFS 存储后重新执行上述检查命令。
   - 若系统输出 `Hardware Acceleration Supported` 信息，如下述举例中所示，表明 VAAI-NAS 插件安装成功且运行正常。

     ```
     # esxcli storage nfs list
     Volume Name Host Share Accessible Mounted Read-Only isPE Hardware Acceleration
     ---------------------- ------------ -------------- ---------- ------- --------- -----
     nfsexport 192.168.33.2 /nfs/nfsexport true true false false Supported
     ```
   - 若系统输出 `Hardware Acceleration Not Supported` 信息，表明 VAAI-NAS 插件运行不正常，请联系 SmartX 售后工程师进行处理。

---

## 升级 VAAI-NAS 插件

# 升级 VAAI-NAS 插件

本文章将介绍如何升级 VAAI-NAS 插件，您可根据 VMware ESXi 版本以及已安装的 VAAI-NAS 插件版本选择从 2.1-x 版本升级至 2.1-4 版本、或者从 1.3-x 版本升级至 2.1-4 版本。

---

## 升级 VAAI-NAS 插件 > 从 2.1-x 版本升级至 2.1-4 版本

# 从 2.1-x 版本升级至 2.1-4 版本

**前提条件**

VMware ESXi 主机版本为 ESXi 7.0 U2 及后续版本或者 ESXi 8.0 U1a 及后续版本，并且 VMware ESXi 主机安装了 2.1-1 ~ 2.1-3 版本的 VAAI-NAS 插件。

**注意事项**

VAAI-NAS 插件从 2.1-1 ~ 2.1-3 版本升级到 2.1-4 版本，不需要重启 ESXi。

**操作步骤**

1. 打开 ESXi 主机 SSH 服务，通过 SSH Client 连接到 ESXi。
2. 将 VAAI-NAS 插件安装文件拷贝至 ESXi 主机的根目录中。
3. 依次执行如下命令：

   - `/etc/init.d/vaai-nasd stop`
   - `esxcli software component apply -d /SMX-ZBSNasPlugin_2.1-4.zip`

     执行完命令后，系统将输出以下信息：

     ```
     Installation Result
        Components Installed: SMX-ZBSNasPlugin_1.0-0.0.0008
        Components Removed: SMX-ZBSNasPlugin_1.0-0.0.0007
        Components Skipped:
        Message: Operation finished successfully.
        Reboot Required: false
     ```
   - `/etc/init.d/vaai-nasd start`
4. 执行以下命令检查升级是否成功。请注意核对显示的版本号与升级的目标版本号是否一致。

   `esxcli software vib list | grep -i zbs`
5. 执行以下命令检查 VAAI-NAS 插件是否正常工作。

   `esxcli storage nfs list`

   - 若系统执行命令后无任何信息输出，表明系统未挂载 NFS 存储，请在挂载 NFS 存储后重新执行上述检查命令。
   - 若系统输出 `Hardware Acceleration Supported` 信息，如下述举例中所示，表明 VAAI-NAS 插件安装成功且运行正常。

     ```
     # esxcli storage nfs list
     Volume Name Host Share Accessible Mounted Read-Only isPE Hardware Acceleration
     ---------------------- ------------ -------------- ---------- ------- --------- -----
     nfsexport 192.168.33.2 /nfs/nfsexport true true false false Supported
     ```
   - 若系统输出 `Hardware Acceleration Not Supported` 信息，表明 VAAI-NAS 插件运行不正常，请联系 SmartX 售后工程师进行处理。

---

## 升级 VAAI-NAS 插件 > 从 1.3-x 版本升级至 2.1-4 版本

# 从 1.3-x 版本升级至 2.1-4 版本

**前提条件**

VMware ESXi 主机版本为 ESXi 7.0 U2 及后续版本或者 ESXi 8.0 U1a 及后续版本，但安装了 1.3-x 版本（适用于 ESXi 6.x 版本）的 VAAI-NAS 插件，例如 1.3-1 版本。

**注意事项**

- 从 VAAI-NAS 1.3-x 版本升级到 2.1-4 版本，需要重启 ESXi 才能使之生效。
- 如果当前的 ESXi 版本需要从 ESXi 6.x 版本升级至 ESXi 7.0 U2 及后续版本或者 ESXi 8.0 U1a 及后续版本，并且当前 ESXi 主机已安装 VAAI-NAS 插件，建议参考[从 ESXi 6.x 升级至 7.0 U2 及后续版本或 8.0 U1a 及后续版本并升级 VAAI-NAS 插件](vaai_nas_installtion_upgrade_17.md#%E4%BB%8E-esxi-6x-%E5%8D%87%E7%BA%A7%E8%87%B3-70-u2-%E5%8F%8A%E5%90%8E%E7%BB%AD%E7%89%88%E6%9C%AC%E6%88%96-80-u1a-%E7%89%88%E6%9C%AC%E5%B9%B6%E5%8D%87%E7%BA%A7-vaai-nas-%E6%8F%92%E4%BB%B6)进行操作，可以减少一次服务器的重启。
- 如果 ESXi 版本从 6.x 已升级至 7.0 U2 及后续版本或者 ESXi 8.0 U1a 及后续版本，但是未移除 1.3-x 版本的 VAAI-NAS 插件，请参考以下操作步骤，将插件升级至 2.1-4 版本；如果 ESXi 在版本升级时已经移除 1.3-x 版本的 VAAI-NAS 插件，可参考[安装 VAAI-NAS 插件](vaai_nas_installtion_upgrade_09)直接安装最新版本的 VAAI-NAS 插件即可。

**操作步骤**

1. 打开 ESXi 主机 SSH 服务，通过 SSH Client 连接到 ESXi。
2. 将 VAAI-NAS 插件安装文件拷贝至 ESXi 主机的根目录中。
3. 依次执行如下命令：

   `/etc/init.d/vaai-nasd stop`

   `esxcli software component apply -d /SMX-ZBSNasPlugin_2.1-4.zip`

   执行完后，系统将输出以下信息：

   ```
   Installation Result
      Components Installed: SMX-ZBSNasPlugin_1.0-0.0.0008
      Components Removed:
      Components Skipped:
      Message: The update completed successfully, but the system needs to be reboote   for the changes to be effective.
      Reboot Required: true
   ```
4. 重启 ESXi 主机。
5. 执行以下命令检查升级是否成功。请注意核对显示的版本号与升级的目标版本号是否一致。

   `esxcli software vib list | grep -i zbs`
6. 执行以下命令检查 vaai-nasd 服务的状态是否正常。

   `/etc/init.d/vaai-nasd status`

   若系统输出 `vaai-nasd is running` 信息，表明状态正常。
7. 执行以下命令检查 VAAI-NAS 插件是否正常工作。

   `esxcli storage nfs list`

   - 若系统执行命令后无任何信息输出，表明系统未挂载 NFS 存储，请在挂载 NFS 存储后重新执行上述检查命令。
   - 若系统输出 `Hardware Acceleration Supported` 信息，如下述举例中所示，表明 VAAI-NAS 插件安装成功且运行正常。

     ```
     # esxcli storage nfs list
     Volume Name Host Share Accessible Mounted Read-Only isPE Hardware Acceleration
     ---------------------- ------------ -------------- ---------- ------- --------- -----
     nfsexport 192.168.33.2 /nfs/nfsexport true true false false Supported
     ```
   - 若系统输出 `Hardware Acceleration Not Supported` 信息，表明 VAAI-NAS 插件运行不正常，请联系 SmartX 售后工程师进行处理。

---

## 卸载 VAAI-NAS 插件

# 卸载 VAAI-NAS 插件

VAAI-NAS 插件在安装完后，一般不需要卸载，但在某些特殊场景下可能需要先卸载 VAAI-NAS 插件。例如，当 VMware ESXi 主机需要升级时，建议在升级前先卸载 VAAI-NAS 插件，待 VMware ESXi 主机版本完成升级后，再重新安装适配的 VAAI-NAS 插件版本。

本章将介绍如何卸载 2.1-4 版本的 VAAI-NAS 插件。

**操作步骤**

1. 打开 ESXi 主机 SSH 服务，通过 SSH Client 连接到 ESXi。
2. 执行以下命令，确认 VAAI-NAS 插件为 **2.1-4** 版本。

   `esxcli software vib list | grep -i zbs`
3. 执行以下命令，关闭 vaai-nasd 服务。

   `/etc/init.d/vaai-nasd stop`
4. 执行以下命令，卸载 VAAI-NAS 插件。

   `esxcli software vib remove -n SMX-ESX-ZBSNasPlugin`

   执行完命令后，如下述举例所示，系统将提示卸载成功，以及所卸载的软件信息。

   ```
   # esxcli software vib remove -n SMX-ESX-ZBSNasPlugin
   Removal Result
     Message: Operation finished successfully.
     Reboot Required: false
     VIBs Installed:
     VIBs Removed: SMX_bootbank_SMX-ESX-ZBSNasPlugin_2.1-4
     VIBs Skipped:
   ```

---

## 最佳实践

# 最佳实践

## 从 ESXi 6.x 升级至 7.0 U2 及后续版本或 8.0 U1a 及后续版本并升级 VAAI-NAS 插件

如果用户需要将 ESXi 从 6.x 升级到 7.0 U2 及后续版本或 8.0 U1a 及后续版本，并且当前的 ESXi 6.x 中已安装 VAAI-NAS 插件，可参考以下步骤进行操作，减少 1 次服务器的重启。

1. 在升级 ESXi 之前，执行命令 `esxcli software vib list | grep -i zbs`，在系统输出中获取 **plugin\_name**。
2. 执行下列命令移除旧版插件：

   `esxcli software vib remove -n <plugin_name>`
3. 执行 ESXi 主机的升级操作，将主机版本升级至 7.0 U2 及后续版本或 8.0 U1a 及后续版本。
4. 参考[安装 VAAI-NAS 插件](vaai_nas_installtion_upgrade_09)的步骤安装 VAAI-NAS 插件，安装完成后无需重启 ESXi 主机。

---

## FAQ

# FAQ

## 2.1-4 版本

1. Q：搭配 VMware ESXi 7.0 U2 版本的虚拟化平台进行部署的 SMTX OS 集群，在 vCenter Server 上为虚拟机添加磁盘时，若界面上 `Location` 参数显示为 **Store with the virtual machine**，`Disk Provisioning` 参数只能选择 **Thin Provision**，无法为虚拟机创建厚置备磁盘，如下图所示。此时该如何设置才能支持为虚拟机添加厚置备磁盘？

   ![](https://cdn.smartx.com/internal-docs/assets/02e4bc2f/vaai_nas_installtion_upgrade_01.png)

   A：首先须先安装完 2.1-4 版本的 SMTX VAAI-NAS 插件，或者将 VAAI-NAS 插件升级至 2.1-4 版本，并且确认 VAAI-NAS 插件正常工作。然后在 vCenter Server 中参考如下步骤进行设置。

   1. 使用 VMware vSphere Web Client 登录到 vCenter Server，右键选中虚拟机，单击 **Edit Settings**，弹出 **Edit Settings**界面。
   2. 在 **Edit Settings** 界面中选择 **Virtual Hardware** > **New Hard disk**， 单击 `Location` 选项，手动选择目的 NFS Datastore。
   3. 查看 `Disk Provisioning` 参数的选项中是否包含 **Thick Provision Lazy Zeroed** 和 **Thick Provision Eager Zeroed**。

      - 若包含上述两个选项，请将该选项设置为 **Thick Provision Eager Zeroed**，如下图所示。单击 **OK** 保存设置，重新为虚拟机添加厚置备磁盘。

        ![](https://cdn.smartx.com/internal-docs/assets/02e4bc2f/vaai_nas_installtion_upgrade_02.png)
      - 若不包含上述两个选项，则不支持为虚拟机创建厚置备磁盘，请直接联系 SmartX 售后工程师。
2. Q：搭配 VMware ESXi 7.0 U2 及后续版本或者 ESXi 8.0 U1a 及后续版本的虚拟化平台进行部署的 SMTX OS 集群，如何在虚拟机上启用 NAS 本机快照？

   A：在安装完或升级至 2.1-4 版本的 SMTX VAAI-NAS 插件后，可通过在虚拟机中设置并启用 NAS 本机快照，从而实现在 SMTX OS 集群中快速创建虚拟机快照。详细的设置步骤可参考 VMware 官方文档[在虚拟机上启用 NAS 本机快照](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/vsphere/vsphere/8-0/vsphere-storage-8-0/storage-hardware-acceleration-in-vsphere/vsphere-hardware-acceleration-on-nas-devices.html#GUID-4F43BDCD-3748-4BE5-B57E-663211249EE3-en)。

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
