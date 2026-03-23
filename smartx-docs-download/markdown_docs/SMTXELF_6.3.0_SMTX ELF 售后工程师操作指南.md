---
title: "SMTXELF/6.3.0/SMTX ELF 售后工程师操作指南"
source_url: "https://internal-docs.smartx.com/smtxelf/6.3.0/aftersales_guide/aftersales_guide_preface_generic"
sections: 21
---

# SMTXELF/6.3.0/SMTX ELF 售后工程师操作指南
## 关于本文档

# 关于本文档

本文档介绍了 SMTX ELF 上线后，售后工程师协助用户维护集群时可能执行的操作流程。

---

## 文档更新信息

# 文档更新信息

**2026-02-04：配合 SMTX ELF 6.3.0 正式发布**

相较于 SMTX ELF 6.2.0，本版本主要更新如下：

- 更新了**更换网卡**章节。
- 新增**关闭和恢复系统服务**、**集群停机维护**和**激活 TencentOS** 章节。

---

## 更换网卡

# 更换网卡

本节描述的操作步骤适用于在 SMTX ELF 集群的主机上更换网卡的场景。

**准备工作**

在关机更换网卡前，请按照如下要求检查即将安装的网卡和集群状态，并做好准备。

- 确认即将安装的网卡与服务器机型兼容，可通过[硬件兼容性查询工具](https://www.smartx.com/smtxos-compatibility/)进行查询。
- 若当前主机上存在无法迁出的其他虚拟机，该虚拟机处于运行中状态并且挂载了 PCI 直通网卡或 SR-IOV 直通网卡，则先将虚拟机关机，再打开**编辑虚拟机的网络设备**手动卸载该虚拟机上挂载的 PCI 直通网卡和 SR-IOV 直通网卡。
- 若当前主机上存在处于**关机**状态且挂载了 PCI 直通网卡或 SR-IOV 直通网卡的虚拟机，则需要打开**编辑虚拟机的网络设备**手动卸载该虚拟机上挂载的 PCI 直通网卡和 SR-IOV 直通网卡。

**操作步骤**

1. 登录 CloudTower，参考《SMTX ELF 运维指南》将待更换网卡的节点[置为主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_43)。
2. 参考《SMTX ELF 运维指南》在 CloudTower 中[关闭](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_45)该节点。
3. 更换网卡，更换结束后启动服务器。
4. 登录节点的 IPMI 管理台，确认 IPMI 管理台已识别新增加的网卡。
5. 请通过 SSH 登录节点，确认系统识别的新增网卡的名称是否与更换前网卡名称一致。

   - 若更换前后网卡型号不一致，且网卡名称不一致，请直接参考步骤 6 开始退出维护模式。
   - 若更换前后网卡型号一致，但网卡名称不一致。请执行如下操作：

     1. 将登录节点的角色切换为 root 用户。
     2. 执行如下命令查看新网卡当前的 MAC 地址：

        `ifconfig <new_nic_name>`

        其中 `<new_nic_name>` 为新网卡的当前名称。
     3. 修改原网卡配置文件内容：

        在 `vim /etc/sysconfig/network-scripts/ifcfg-<old_nic_name>` 配置文件中，将 **HWADDR** 修改为上一步骤中获取的 MAC 地址。

        其中 `<old_nic_name>` 为原网卡的名称，您可以登录 CloudTower，在集群的虚拟分布式交换机列表中选中管理网络、虚拟机网络或存储接入网络所在的虚拟分布式交换机查看。
     4. 执行 `reboot` 重启节点。
     5. 节点重启完成后，检查新网卡名称是否与原网卡名称一致。若一致，则直接参考步骤 6 开始退出维护模式，并跳过步骤 8 编辑虚拟交换机动作。
   - 若更换前后网卡名称一致，请参考步骤 6 开始退出维护模式，并跳过步骤 8 编辑虚拟交换机动作。
6. 参考《SMTX ELF 运维指南》在 CloudTower 中将该节点[退出主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_44)。
7. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`
8. 将管理网络、虚拟机网络或存储接入网络所在的虚拟交换机与新添加的网口完成关联。

   登录 CloudTower，在集群的虚拟分布式交换机列表中选中管理网络、虚拟机网络或存储接入网络所在的虚拟分布式交换机，单击右侧的 **...** 后选择**编辑**，在弹出的**编辑虚拟分布式交换机**对话框里勾选新增的网口前的复选框，并保存设置。
9. 确认集群的网络可正常访问。

   将集群中其他节点上的一台虚拟机手动迁移至已增加网卡的节点上，并登录该虚拟机的操作系统，若能 ping 通其他虚拟机，表明网络正常。

---

## 更换存储控制器

# 更换存储控制器

当用于构建系统盘的硬件 RAID 1 的存储控制器（如 RAID 卡或 Dell BOSS 卡）发生故障，系统盘也将故障且不可修复，需要先将故障存储控制器和系统盘所在的主机从集群中移除，完成存储控制器和系统盘更换后再将主机重新添加回原集群。

**准备工作**

- 确认即将安装的存储控制器与原来的存储控制器的型号完全相同。
- 记录存储控制器槽位。

**操作步骤**

1. 移除故障控制器所在的主机，请参考《SMTX ELF 运维指南》[移除节点](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_31)章节的内容进行操作。
2. 更换存储控制器后，开启服务器，将 2 块系统盘组建成硬件 RAID 1。
3. 将主机重新添加至原集群，请参考《SMTX ELF 运维指南》[添加节点](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_08)章节的内容进行操作。

---

## 更换 GPU

# 更换 GPU

本节描述的操作步骤仅适用于在SMTX ELF 集群的主机上更换 GPU 的场景。

**准备工作**

将主机上所有挂载了该 GPU 设备的虚拟机关机，并在**编辑虚拟机**页面卸载该 GPU 设备。

**操作步骤**

1. 登录 CloudTower，参考《SMTX ELF 运维指南》将待更换 GPU 的节点[置为主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_43)。
2. 参考《SMTX ELF 运维指南》在 CloudTower 中[关闭](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_45)该节点。
3. 更换 GPU，更换结束后启动服务器。

   > **说明：**
   >
   > 若主机上存在多个同名的 GPU 设备，可通过 GPU 设备信息中 **ID** 描述的 PCI 地址确定待移除的 GPU 的位置。
4. 登录 CloudTower，参考《SMTX ELF 运维指南》将该节点[退出主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_44)。
5. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`
6. 登录 CloudTower，进入该主机的概览界面，查看**GPU 设备**列表，确认新的 GPU 设备安装成功。

**注意事项**

若移除主机 GPU 前未卸载虚拟机的 GPU 设备，移除 GPU 后虚拟机将无法开机，并且提示“GPU 设备不存在”。此时虚拟机详情页中会标记已被移除的 GPU 设备，在**编辑虚拟机**中将其卸载后，重新开机即可。

---

## 更换加密控制器

# 更换加密控制器

本节描述的操作步骤仅适用于在SMTX ELF 集群的主机上更换加密控制器的场景。

**准备工作**

将主机上所有挂载了该加密控制器的虚拟机关机，并在**编辑虚拟机**页面卸载该加密控制器。

**操作步骤**

1. 登录 CloudTower，参考《SMTX ELF 运维指南》将待更换加密控制器的节点[置为主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_43)。
2. 参考《SMTX ELF 运维指南》在 CloudTower 中[关闭](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_45)该节点。
3. 更换加密控制器，更换结束后启动服务器。
4. 配置加密控制器 SR-IOV 直通。

   具体请参考《SMTX ELF 特性说明》的[使用加密控制器 SR-IOV 直通](/smtxelf/6.3.0/elf_property_notes/elf_property_notes_37)的步骤 3～5。
5. 登录 CloudTower，参考《SMTX ELF 运维指南》将该节点[退出主机维护模式](/smtxelf/6.3.0/elf_operation_maintenance/elf_operation_maintenance_44)。
6. 使用 SSH 方式登录此节点并执行如下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

---

## 关闭和恢复系统服务

# 关闭和恢复系统服务

集群停机维护时需要您参考本章节内容按顺序关闭 SMTX ELF 集群上的所有系统服务，运维结束后，还需参考本章节内容按顺序开启这些系统服务。

---

## 关闭和恢复系统服务 > 识别系统服务虚拟机

# 识别系统服务虚拟机

您可以在 Fisheye 的**所有虚拟机**视图中，根据下表搜索关键字，识别对应的所有系统服务虚拟机，然后执行相应操作。

| 系统服务 | 服务虚拟机 | 关键字 |
| --- | --- | --- |
| 可观测性平台 | 可观测性服务虚拟机 | `observability-` |
| Everoute | Everoute controller、负载均衡虚拟机 | `everoute-cluster-` |
| 边缘网关虚拟机 | `vpc-gateway-` |
| 深度安全防护 | 安全防护虚拟机 | `SVM-` |
| CloudTower | CloudTower 代理虚拟机 | `agent-mesh-node-` |
| CloudTower 虚拟机 | - CloudTower 未启用 HA：   - 通过 CloudTower Installer 安装部署时CloudTower 虚拟机名称为 `CloudTower`   - 在集群中手动创建虚拟机后再进行部署时，CloudTower 虚拟机名称为 您为其设置的`虚拟机名称` - CloudTower 启用 HA 后：   - 主动节点的名称为启用 HA 前的CloudTower 虚拟机名称，请根据安装部署方式确认。   - 仲裁节点和被动节点的名称为部署 CloudTower 高可用集群时您为其设置的`虚拟机名称`。 |

---

## 关闭和恢复系统服务 > 关闭系统服务

# 关闭系统服务

当 SMTX ELF 集群中部署了系统服务，维护前请参考本小节和[识别系统服务虚拟机](/smtxelf/6.3.0/aftersales_guide/aftersales_guide_06)小节的内容，识别并按顺序关闭这些系统服务。

## 准备工作

在关闭系统服务前，请您登录 CloudTower，进入**集群**的**虚拟机**列表，确认该集群中不存在除系统服务虚拟机外的虚拟机，或除系统服务虚拟机外的虚拟机均关机。

## 关闭系统服务顺序

![](https://cdn.smartx.com/internal-docs/assets/7b0c1b08/aftersales_guide_01.png)

上图展示了 SMTX ELF 集群中部署了所有系统服务时的关闭顺序，实际运维过程中请直接跳过未部署的系统服务。

**第一步**：关闭可观测性平台。

**第二步**：关闭 Everoute 和深度安全防护，这两个服务的关闭没有先后顺序。

**第三步**：关闭 CloudTower。

## 关闭系统服务虚拟机操作

一个系统服务中可能包含多个系统服务虚拟机，请参考本小节内容按顺序关闭系统服务中的所有系统服务虚拟机。

### 可观测性平台

登录 Fisheye，关闭可观测性服务虚拟机，**禁止选择**强制关机。

### Everoute

登录 Fisheye，批量关闭 Everoute controller、负载均衡虚拟机和边缘网关虚拟机。

### 深度安全防护

登录 CloudTower 关闭安全防护虚拟机。

### CloudTower

1. 登录 Fisheye，关闭 CloudTower 代理虚拟机，**禁止选择**强制关机。
2. 关闭 CloudTower 虚拟机：
   - 若 CloudTower 未启用 HA：登录 Fisheye，关闭 CloudTower 虚拟机，**禁止选择**强制关机。
   - 若 CloudTower 已启用 HA（所有关机操作均**禁止选择**强制关机）：
     - 集群上仅有其中一个高可用节点：
       1. 参考《CloudTower 使用指南》中**管理 CloudTower 高可用** > **查看基本信息**章节，确认该高可用节点状态正常。
       2. 关闭该高可用节点：
          - 主动节点虚拟机或被动节点虚拟机：登录 Fisheye，关闭虚拟机。
          - 仲裁节点虚拟机：
            - 部署在 VMware ESXi 平台时，直接关闭仲裁节点虚拟机。
            - 部署在 SMTX OS（ELF）平台时，登录 Fisheye，关闭仲裁节点虚拟机。
     - 集群上包含两个及以上高可用节点：登录 Fisheye，依次关闭被动节点虚拟机、仲裁节点虚拟机、主动节点虚拟机。

---

## 关闭和恢复系统服务 > 恢复系统服务

# 恢复系统服务

当 SMTX ELF 集群运维前关闭了系统服务，运维结束后，请参考本小节和[识别系统服务虚拟机](/smtxelf/6.3.0/aftersales_guide/aftersales_guide_06)小节的内容，识别并按顺序开启这些系统服务。

## 恢复系统服务顺序

SMTX ELF 集群恢复后，请按下图中的顺序确认系统服务虚拟机是否随主机自动开机成功，未开机的系统服务虚拟机请按照指引启动对应的系统服务。

> **说明**：
>
> - 目前支持随主机自动开机的系统服务虚拟机有**CloudTower 代理虚拟机**、**可观测性服务虚拟机**。
> - 下图展示了 SMTX ELF 集群中部署了所有系统服务时的恢复顺序，实际运维过程中请直接跳过未部署的系统服务。

![](https://cdn.smartx.com/internal-docs/assets/7b0c1b08/aftersales_guide_02.png)

**第一步**：恢复 CloudTower。

**第二步**：恢复 Everoute 和深度安全防护，这两个服务的恢复没有先后顺序。

**第三步**：恢复可观测性平台。

## 恢复系统服务虚拟机操作

### CloudTower

1. CloudTower 所在的主机开机。
2. 登录 Fisheye：

   - 若 CloudTower 未启用 HA： 开启 CloudTower 虚拟机。
   - 若 CloudTower 已启用 HA： 依次开启主动节点、仲裁节点、被动节点。
3. 确认运维前关闭的 CloudTower 代理虚拟机是否随主机开机。如未开机请登录 Fisheye 开机。

### 深度安全防护

1. 安全防护虚拟机所在主机开机。
2. 登录 CloudTower 确认运维前关闭的安全防护虚拟机是否随主机开机。如未开机请在 CloudTower 上将其开机。
3. 确认安全防护虚拟机开机后，将开启防病毒或深度包检测的虚拟机开机。

### Everoute

主机开机后，确认运维前关闭的 Everoute controller、负载均衡虚拟机和边缘网关虚拟机是否随主机开机。如未开机请登录 Fisheye 批量开机。

### 可观测性平台

主机开机后，确认运维前关闭的可观测性服务虚拟机是否随主机开机。如未开机请登录 Fisheye 开机。

---

## 集群停机维护

# 集群停机维护

当机房面临如下场景时，需要手动将 SMTX ELF 集群的主机关机，维护期结束后，还需要重新启动服务器，恢复集群的运行。

- 机房搬迁
- 旧集群下线
- 机房进行网络改造
- 在预期内机房断电

**操作步骤**

1. 登录 CloudTower，进入集群的虚拟机列表，确认该集群中不存在虚拟机，或者虚拟机处于**关机**状态。

   > **说明：**
   >
   > - 若虚拟机列表中存在部分未关机的虚拟机，并且虚拟机未安装操作系统，或者虚拟机的操作系统不支持 ACPI，此时可选中虚拟机，在弹出的虚拟机详情面板中单击**关机**，然后选择**强制关闭虚拟机**。
   > - 若虚拟机列表中存在未关机的系统服务虚拟机，请参考[关闭系统服务虚拟机](/smtxelf/6.3.0/aftersales_guide/aftersales_guide_07)处理。
2. 使用 SSH 方式登录集群中的一个节点，执行以下命令，关闭集群所有节点。

   ```
   zbs-cluster shutdown_hosts --hosts=all --action=poweroff --network=storage
   ```

   > **说明：**
   >
   > - 如果存储接入网络无法连通，可以将 `storage` 替换为 `mgt` ，使用管理网络来连接目标主机。
   > - 如果使用 SSH 方式登录失败，可以执行以下步骤依次关闭节点。
   >
   >   1. 通过 IPMI 管理控制台依次登录集群的每个节点，执行以下命令，停止集群上每个节点的相关服务。
   >
   >      ```
   >      /usr/share/tuna/script/control_all_services.sh --action=stop --group=all
   >      ```
   >   2. 在每个节点中执行以下命令，关闭节点。
   >
   >      `shutdown -h now`
   >
   >      如果执行上述命令关闭节点失败，可以通过在 IPMI 管理控制台关闭主机电源的方式来关闭节点。
3. 启动集群停机维护的相关工作，待工作结束后，重新将节点服务器开机。
4. 在节点上执行以下命令，确认所有服务运行正常。

   `sudo /usr/share/tuna/script/control_all_services.sh --action=status --group=role`

---

## 激活 TencentOS

# 激活 TencentOS

在基于 TencentOS 操作系统的 SMTX ELF 集群部署完成后，需要激活主机的操作系统，以获得腾讯官方的技术支持、安全更新等。您可参考本章节通过在线激活（KMS 激活）或离线激活的方式进行激活。

---

## 激活 TencentOS > 在线激活（KMS 激活）

# 在线激活（KMS 激活）

KMS（Key Management Service）激活是一种在线批量激活许可的方式，您可以参考本章节创建 KMS 服务器，并使用 KMS 激活 TencentOS Server 操作系统。当需要激活操作系统的主机数量较多时，建议使用此方式进行激活。

**前提条件**

- 已通过 SmartX 获取的 TencentOS Server 的许可（`tar.gz` 文件）。
- 已根据待激活主机的 CPU 架构获取 KMS 服务器的 OVF 文件（包含 `.ovf` 文件和 `.vmdk` 文件）。

---

## 激活 TencentOS > 在线激活（KMS 激活） > 准备工作 > 创建 KMS 服务器

# 创建 KMS 服务器

使用已获取的 OVF 文件，参考《SMTX ELF 管理指南》的[导入虚拟机](/smtxelf/6.3.0/elf_administration_guide/elf_administration_guide_020)小节，在待激活的 SMTX ELF 集群中创建一台虚拟机作为 KMS 服务器。在为虚拟机配置网络设备时，请选择一个可以与系统服务虚拟机连通的虚拟机网络。

---

## 激活 TencentOS > 在线激活（KMS 激活） > 准备工作 > 配置 KMS 服务器

# 配置 KMS 服务器

创建 KMS 服务器后，请使用 root 账户登录 KMS 服务器，然后按照如下步骤进行配置。

1. 根据集群当前网络环境为 KMS 服务器配置 IP。配置完成后，可执行 `ip ad` 命令查看当前 KMS 服务器的 IP 地址。
2. 在本地打开终端命令行工具，使用 scp 命令将许可文件上传到 KMS 服务器上，然后执行如下命令导入许可文件，其中 `license.tar.gz` 为许可文件的文件名。

   ```
   tar zxvf license.tar.gz -C /var/lib/txos
   ```
3. 执行如下命令启动 KMS 服务。

   ```
   systemctl enable txos-kms --now
   ```

   启动 KMS 服务后，可分别执行如下命令查看 KMS 服务状态和 KMS 服务器许可状态。

   - 查看 KMS 服务状态

     ```
     systemctl status txos-kms
     ```

     输出示例如下，如果 `Active` 一行显示为 `active (running)`，说明 KMS 服务已正常启动。

     ```
     systemctl status txos-kms
     txos-kms.service - TencentOS KMS Service
     Loaded: loaded (/etc/systemd/system/txos-kms.service; disabled; vendor preset: disabled)
     Active: active (running) since Tue 2025-04-08 10:44:57 CST; 14min ago
     Process: 1724 ExecStartPre=/usr/bin/txos-admin init-db (code=exited, status=0/SUCCESS)
     Process: 1721 ExecStartPre=/usr/bin/mkdir -p /var/lib/txos (code=exited, status=0/SUCCESS)
     Main PID: 1731 (txos-service)
     Tasks: 7 (limit: 2899)
     Memory: 31.2M
     CGroup: /system.slice/txos-kms.service
             └─1731 /usr/bin/txos-service -w /var/lib/txos -t 5
     ```
   - 查看 KMS 服务器许可状态

     ```
     txos-admin show
     ```

     如果输出如下信息，说明 KMS 服务器许可状态正常。

     ```
     # txos-admin show
     +----------------------------------+------+--------+-------+------+------+---------------------+
     |               kms                | type | period | count | used | free |         time        |
     +----------------------------------+------+--------+-------+------+------+---------------------+
     | 1497994293ae4887a61f5fcd8a05a0ca | TEST |   3    |   2   |  0   |  2   | 2025-04-08 10:44:57 |
     +----------------------------------+------+--------+-------+------+------+---------------------+
     ```

---

## 激活 TencentOS > 在线激活（KMS 激活） > 激活 SMTX ELF 主机操作系统

# 激活 SMTX ELF 主机操作系统

1. 通过 IPMI 管理台或 SSH 登录待激活操作系统的主机。
2. 使用 `sudo` 命令切换到 root 账户，执行如下命令激活操作系统，其中 `KMS_IP` 为已创建 KMS 服务器的 IP 地址。

   ```
   txos-tool set url=$KMS_IP
   txos-tool activate kms
   ```
3. 执行如下命令查看操作系统激活状态，若输出结果中 `status` 字段显示为 `Activated` ，说明操作系统激活成功。

   ```
   txos-tool show
   ```

   输出示例如下：

   ```
   txos-tool show
   url     :       $KMS_IP
   port    :       38400
   kms     :       true
   type    :       COMMERCIAL
   sn      :       AAAAAAAA-BBBBBBBB-CCCCCCCC
   hwid    :       AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB
   reg     :       CCCCCCCC-XXXXXXXX-YYYYYYYY-DDDDDDDD
   time    :       2025-03-12 ~ 2025-06-12
   status  :       Activated
   ```

---

## 激活 TencentOS > 离线激活

# 离线激活

若待激活的主机数量较少且无需搭建 KMS 服务器，您可以参考本章节，通过离线激活的方式激活 TencentOS Server 操作系统。

---

## 激活 TencentOS > 离线激活 > 准备工作 > 获取主机硬件 ID

# 获取主机硬件 ID

## 通过命令行获取

1. 通过 IPMI 管理台或 SSH 登录待激活操作系统的主机。
2. 使用 `sudo` 命令切换到 root 账户，执行如下命令，输出结果中的 `HW ID` 为该主机的硬件 ID，请记录此 ID。

   ```
   txos-tool pull hwid
   ```

   输出示例如下：

   ```
   txos-tool pull hwid
   ######################################################
   ##              ##  ##      ######  ##              ##
   ##  ##########  ####    ######  ##  ##  ##########  ##
   ##  ##      ##  ######          ######  ##      ##  ##
   ##  ##      ##  ##########          ##  ##      ##  ##
   ##  ##      ##  ####  ####    ##    ##  ##      ##  ##
   ##  ##########  ######          ######  ##########  ##
   ##              ##  ##  ##  ##  ##  ##              ##
   ##################  ##      ##    ####################
   ##    ##    ##  ####      ####  ##  ##  ##########  ##
   ##    ##      ######  ########  ##  ####      ####  ##
   ##  ####  ##      ####    ########  ##  ####  ########
   ####        ####              ##    ##    ######    ##
   ##  ####    ##        ##  ######  ####      ##  ######
   ##  ##  ##  ####  ##  ######  ########              ##
   ##    ####      ####    ####    ##    ####  ##    ####
   ##  ##  ##  ######  ##  ##      ####  ##            ##
   ##  ########    ##  ##  ######              ##      ##
   ##################  ####        ##  ######  ##  ######
   ##              ######        ####  ##  ##    ##    ##
   ##  ##########  ####  ####  ####    ######  ##      ##
   ##  ##      ##  ##    ##  ##  ####          ####    ##
   ##  ##      ##  ##        ##      ######    ##      ##
   ##  ##      ##  ####    ##  ####  ##  ####    ##    ##
   ##  ##########  ##  ####  ##    ####    ##  ####  ####
   ##              ##  ##    ##  ##      ##    ##      ##
   ######################################################
   HW ID: AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB
   ```
3. 参考步骤 1～2，获取其他待激活主机的硬件 ID。

## 通过脚本批量获取

**前提条件**

已获取 TencentOS License 激活脚本并上传至待激活集群中的任一主机。

**操作步骤**

1. 通过 IPMI 管理台或 SSH 登录已上传脚本的主机。
2. 使用 `sudo` 命令切换到 root 账户，执行如下命令获取主机硬件 ID。其中 `hosts_file` 为包含待收集硬件 ID 主机 IP 列表的文件（可自定义文件名，例如 `hosts.txt`）；若不提供此参数，脚本将自动从 Ansible inventory 中收集所有主机的硬件 ID。

   ```
   ./tl3.sh [hosts_file]
   ```

   如需指定待收集硬件 ID 的主机，可在当前主机中创建主机 IP 列表文件，并按照以下格式逐行填写待激活主机的存储 IP。

   ```
   10.0.xx.xx
   10.0.xx.xx
   10.0.xx.xx
   ```
3. 查看输出结果。脚本将按以下格式输出主机存储 IP 及其硬件 ID，并将结果保存至 `/tmp/hw_ids.txt` 文件。

   ```
   10.0.xx.xx, AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB
   10.0.xx.xx, AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB
   10.0.xx.xx, AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB
   ```

   可通过执行如下命令查看收集到的硬件 ID 信息。

   ```
   cat /tmp/activation_results.txt
   ```

---

## 激活 TencentOS > 离线激活 > 准备工作 > 获取许可码

# 获取许可码

联系 SmartX 售后工程师，提交所有待激活主机的硬件 ID，获取激活所需的许可码。

---

## 激活 TencentOS > 离线激活 > 激活 SMTX ELF 主机操作系统

# 激活 SMTX ELF 主机操作系统

## 通过命令行激活

1. 通过 IPMI 管理台或 SSH 登录待激活操作系统的主机。
2. 使用 `sudo` 命令切换到 root 账户，执行如下命令激活操作系统，其中 `$LICENSE_CODE` 为已获取的许可码。

   ```
   txos-tool set reg $LICENSE_CODE
   txos-tool activate offline
   ```

   输出示例如下：

   ```
   txos-tool set reg  CCCCCCCC-XXXXXXXX-YYYYYYYY-DDDDDDDD
   txos-tool activate offline
   Activate Success!
   ```
3. 执行如下命令查看操作系统激活状态，若输出结果中 `status` 字段显示为 `Activated`，说明操作系统激活成功。

   ```
   txos-tool show
   ```

   输出示例如下：

   ```
   txos-tool show
   url     :       $KMS_IP
   port    :       38400
   kms     :       false
   type    :       COMMERCIAL
   sn      :       AAAAAAAA-BBBBBBBB-CCCCCCCC
   hwid    :       AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB
   reg     :       CCCCCCCC-XXXXXXXX-YYYYYYYY-DDDDDDDD
   time    :       2025-03-12 ~ 2025-06-12
   status  :       Activated
   ```
4. 参考步骤 1～3 激活其他待激活主机的操作系统。

## 通过脚本批量激活

**前提条件**

已获取 TencentOS License 激活脚本并上传至待激活集群的中任一主机。

**操作步骤**

1. 通过 IPMI 管理台或 SSH 登录已上传脚本的主机。
2. 使用 `sudo` 命令切换到 root 账户，创建 `host_license.txt` 文件，并按以下格式逐行输入待激活主机的存储 IP、硬件 ID 和许可码。

   ```
   10.0.xx.xx, AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB, CCCCCCCC-XXXXXXXX-YYYYYYYY-DDDDDDDD
   10.0.xx.xx, AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB, CCCCCCCC-XXXXXXXX-YYYYYYYY-DDDDDDDD
   10.0.xx.xx, AAAAAAAA-XXXXXXXX-YYYYYYYY-BBBBBBBB, CCCCCCCC-XXXXXXXX-YYYYYYYY-DDDDDDDD
   ```
3. 执行如下命令激活操作系统。

   ```
   ./tl3.sh --activate host_license.txt
   ```

   执行过程中，脚本将依次激活 `host_license.txt` 文件中列出的主机，并在终端显示每台主机的激活状态，详细的执行日志将输出至 `/tmp/activation_results.txt` 文件。
4. 激活完成后，可通过执行如下命令查看主机激活状态。其中 `hosts_file` 为包含待查询主机 IP 列表的文件（可自定义文件名，例如 `hosts.txt`）；若不提供此参数，脚本将自动从 Ansible inventory 中收集所有主机的硬件 ID。

   ```
   ./tl3.sh -c|--check [hosts_file]
   ```

   如需自定义查看主机列表，可在当前主机创建主机 IP 列表文件，并按照以下格式逐行填写待确认激活状态主机的存储 IP：

   ```
   10.0.xx.xx
   10.0.xx.xx
   10.0.xx.xx
   ```

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
