---
title: "cluster-onoff/1.0.4/集群上下线工具用户指南"
source_url: "https://internal-docs.smartx.com/cluster-onoff/1.0.4/cluster_onoff_user_guide/cluster_onoff_user_guide_preface"
sections: 17
---

# cluster-onoff/1.0.4/集群上下线工具用户指南
## 关于本文档

# 关于本文档

本文档介绍了如何使用集群上下线工具对 SMTX OS 集群、SMTX ELF 集群和 SMTX ZBS 集群执行上线和下线操作。

阅读本文档需要了解 SMTX OS 超融合软件、SMTX ELF 虚拟化软件、SMTX ZBS 软件、CloudTower 管理平台，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

**2026-02-04：文档随集群上下线工具 1.0.4 正式发布**

首次发布集群上下线工具 1.0.4 用户指南。

---

## 概述

# 概述

在集群上下线的过程中，通常需要执行复杂的操作，如批量关闭虚拟机、关闭系统服务、检查集群状态等。手动执行这些操作不仅耗时，而且容易出错。为了简化这些操作并提升运维效率，北京志凌海纳科技股份有限公司（以下简称“SmartX”）推出了集群上下线工具。该工具通过命令行实现集群上下线自动化，减少了人工操作的复杂性与风险。

集群上下线工具支持批量开关虚拟机、统一开关系统服务，并能够自动检查集群状态，确保集群在上下线过程中的安全性和稳定性。通过简化操作和降低配置复杂度，该工具能够有效减少人力投入，降低操作风险，适用于机房搬迁、旧集群下线、机房网络改造、预期内机房断电等多种场景。

---

## 准备集群上下线工具

# 准备集群上下线工具

进行集群上、下线操作前，请先查阅本版本《集群上下线工具发布说明》中的[版本配套说明](/cluster-onoff/1.0.4/cluster_onoff_release_notes/cluster_onoff_release_notes_04)，确认产品版本与集群上下线工具兼容，然后参考以下步骤准备集群上下线工具。

**操作步骤**

1. 在 CloudTower 的**集群**主界面中找到需维护的集群，然后在该集群的管理界面中单击**设置** > **集群连接信息**，获取集群 IP 地址。
2. 根据 CPU 架构和操作系统下载集群上下线工具，并赋予可执行权限。

   - （推荐使用）若在集群中的任一节点或 SCVM 中执行集群上下线操作，请下载 Linux 系统的文件，并将其拷贝到集群的任一节点或 SCVM 中，如拷贝到 `/home/smartx/` 目录下，然后在该目录下执行 `chmod +x ctcli` 命令赋予可执行权限。
   - 若在 macOS 系统的本地主机中执行集群上下线操作，请下载 macOS 系统的文件，然后使用终端工具打开该文件，执行 `chmod +x ctcli` 命令赋予可执行权限。
   - 若在 Windows 系统的本地主机中执行集群上下线操作，请下载 Windows 系统的文件。
3. 在该工具所在目录下创建 `config.yaml` 文件并根据如下示例进行配置。

   ```
   # CloudTower IP 地址
   operation-center-host: 192.168.28.80
   # CloudTower 登录用户
   operation-center-username: root
   # CloudTower 登录密码
   operation-center-password: 'xxxxxx'
   # CloudTower 登录方式，当前支持 LOCAL/LDAP
   user-source: LOCAL/LDAP
   # 是否忽略 TLS 校验
   skip-tls-verify: true
   # SMTX 集群 IP 地址（步骤 1 中获取的集群 IP 地址）
   cluster-connect-ip: 192.168.67.xx
   # SMTX 集群超级管理员登录用户名
   cluster-username: root
   # SMTX 集群超级管理员登录密码
   cluster-password: '111111'
   # SMTX 集群中任一节点的 SSH 登录用户名（集群中所有节点的 SSH 登录用户名需一致）
   cluster-ssh-username: ssh_user
   # SMTX 集群中节点的 SSH 登录密码（集群中所有节点的 SSH 登录密码需一致）
   cluster-ssh-password: 'yyyyyy'
   ```
4. 检查当前目录下是否存在 `ctcli` 文件和 `config.yaml` 文件。若存在，则集群上下线工具及其配置文件已准备完成。您可参考[集群上下线工具命令参数说明](/cluster-onoff/1.0.4/cluster_onoff_user_guide/cluster_onoff_user_guide_09)提前了解该工具的命令参数说明。

---

## 集群下线 > SMTX OS（ELF）集群和 SMTX ELF 集群下线

# SMTX OS（ELF）集群和 SMTX ELF 集群下线

集群下线分为 4 个阶段：关闭业务虚拟机、关闭系统服务虚拟机、关闭 CloudTower 虚拟机及代理虚拟机、检查并关闭集群所有节点。
集群上下线工具将自动判断集群中的虚拟机类型并执行关闭操作，无需手动区分。

1. 获取需维护集群的序列号。您可以在 CloudTower 的**集群**主界面中找到需维护的集群，然后在该集群的管理界面中单击**设置** > **软件许可**，在**许可信息**中即可获取集群的序列号。
2. 进入集群上下线工具所在目录。

   - 若集群上下线工具在集群的任一节点中，请登录该节点，然后进入工具所在的目录。
   - 若集群上下线工具在本地主机中，请使用终端工具打开集群上下线工具。
3. 关闭集群中的业务虚拟机。

   1. 执行如下命令，导出包含集群中所有业务虚拟机信息的 `vms.csv` 文件，其中 `$CLUSTER_UUID` 表示在步骤 1 中获取的集群序列号。

      ```
      ./ctcli script vm export --cluster-uuid $CLUSTER_UUID > vms.csv
      ```

      对于安装了 SMTX 虚拟机工具的虚拟机，支持在集群上线后检测虚拟机操作系统的启动状态。在导出过程中，集群上下线工具将探测虚拟机的 OpenSSH 端口（22）是否可连通。如果端口可连通，则在导出信息的 `SSHConnected` 列标记 `true`，并在集群上线后对这些虚拟机操作系统的启动状态进行检测。

      导出后，您可根据实际业务类型调整 `vms.csv` 文件中的虚拟机顺序，后续业务虚拟机的关闭顺序将以此文件中的顺序为准。
   2. 执行如下命令，关闭集群中的业务虚拟机。关闭过程中，您可在 CloudTower 的任务中心查看虚拟机关闭任务，确认关闭状态。

      ```
      ./ctcli script vm stop --cluster-uuid $CLUSTER_UUID --vms-file ./vms.csv
      ```

      如果虚拟机关机失败，可能是虚拟机未安装操作系统、操作系统不支持 ACPI 等原因导致的。此时可添加 `--force=true` 参数，强制关闭虚拟机。

      ```
      ./ctcli script vm stop --cluster-uuid $CLUSTER_UUID --vms-file ./vms.csv --force=true
      ```
4. 关闭集群中的系统服务虚拟机。

   1. 执行如下命令，从 `vms.csv` 文件中导出所有系统服务虚拟机信息至 `system-services.yaml` 文件中。

      ```
      ./ctcli script system-service export --cluster-uuid $CLUSTER_UUID --vms-file ./vms.csv 2>/dev/null > system-services.yaml
      ```

      如果工具执行环境为 Windows 系统，需将 `2>/dev/null` 替换为 `2>NUL`。
   2. 执行如下命令，关闭集群中的系统服务虚拟机。关闭过程中，您可在 CloudTower 的任务中心查看虚拟机关闭任务，确认关闭状态。

      ```
      ./ctcli script system-service stop --cluster-uuid $CLUSTER_UUID --services-file ./system-services.yaml
      ```
5. 执行如下命令，关闭集群中的 CloudTower 虚拟机和 CloudTower 代理虚拟机。

   ```
   ./ctcli script tower stop --cluster-uuid $CLUSTER_UUID --services-file ./system-services.yaml
   ```
6. 执行如下命令，检查集群所有节点是否可以正常关闭。如果节点无法关闭，请根据对应的提示信息，解决问题后重新执行。

   ```
   ./ctcli script cluster stop-hosts --cluster-uuid $CLUSTER_UUID --check-only
   ```
7. 执行如下命令，检查并关闭集群所有节点。如果集群中的节点均可正常关机，检查通过后，会提示您再次输入集群序列号以确认关闭节点。

   ```
   ./ctcli script cluster stop-hosts --cluster-uuid $CLUSTER_UUID
   ```

   您也可以根据需求通过在命令中添加如下参数调整操作：

   `--comfirm-alert=true`：当检查发现集群存在硬件告警时，如果确认集群的硬件告警符合预期，可添加此参数忽略告警。

   `--disable-services=true`：若希望在集群重新上线后，不自动启动节点内的服务，可添加此参数禁止服务自启动。
8. 启动集群停机维护的相关工作。

---

## 集群下线 > SMTX OS（VMware ESXi）集群下线

# SMTX OS（VMware ESXi）集群下线

1. 获取需维护集群的序列号。您可以在 CloudTower 的**集群**主界面中找到需维护的集群，然后在该集群的管理界面中单击**设置** > **软件许可**，在**许可信息**中即可获取集群的序列号。
2. 通过 VMware vSphere Web Client 登录到 vCenter Server，并定位到某个 SCVM 所在 ESXi 主机的其他虚拟机（非 SCVM 虚拟机），右键单击该虚拟机并选择**启动** > **关闭客户机操作系统**，关闭虚拟机的操作系统。
3. 参考上一步，将集群中所有 SCVM 所在 ESXi 主机的其他虚拟机（除了 vCLS 虚拟机）全部关机。对于 vCLS 虚拟机，如果它使用的是在 SMTX OS 集群中创建的 NFS Export 对应的数据存储，请将该虚拟机迁移到别的数据存储上。
4. 在 vCenter Server 中选中集群，然后在右侧界面单击**配置 > 服务 > vSphere 可用性**，在 vSphere 可用性设置界面右侧单击**编辑**，然后在弹出的**编辑集群设置**对话框中关闭 **vSphere HA** 选项。单击**确定**，关闭集群的 HA 功能。
5. 进入集群上下线工具所在的目录。

   - 若集群上下线工具在 SCVM 中，请使用 SSH 方式登录该 SCVM，然后进入工具所在的目录。
   - 若集群上下线工具在本地主机中，请使用终端工具打开集群上下线工具。
6. 执行以下命令检查集群所有 SCVM 是否可以正常关闭。其中，`$CLUSTER_UUID` 表示在步骤 1 中获取的集群序列号。

   ```
   ./ctcli script cluster stop-hosts --cluster-uuid $CLUSTER_UUID --check-only
   ```

   如果 SCVM 无法关闭，请根据日志中的提示信息，解决问题后重新执行。
7. 执行以下命令检查并关闭集群所有 SCVM。若集群中的 SCVM 均可以正常关闭，将提示您再次输入集群的序列号以确认关闭，确认成功后开始关闭集群 SCVM。

   ```
   ./ctcli script cluster stop-hosts --cluster-uuid $CLUSTER_UUID
   ```

   您也可以根据需求通过在命令中添加如下参数调整操作：

   - `--confirm-alert=true`：当检查发现集群存在硬件告警时，如果确认集群的硬件告警符合预期，可添加此参数忽略告警。
   - `--disable-services=true`：若希望在集群重新上线后，不自动启动 SCVM 内的服务，可添加此参数禁止服务自启动。
   > **说明：**
   >
   > 如果使用 SSH 方式登录失败，可以执行以下步骤依次关闭 SCVM。
   >
   > 1. 通过 vCenter Server 连接并依次登录集群的 SCVM，并在所有 SCVM 中执行下述命令停止相关服务。
   >
   >    ```
   >    /usr/share/tuna/script/control_all_services.sh --action=stop --group=all
   >    ```
   > 2. 在 vCenter Server 中浏览到 SCVM，右键选择**启动** > **关闭客户机操作系统**，关闭 SCVM 虚拟机的操作系统。
   >
   >    若 vCenter Server 使用了 SMTX OS 提供的存储，则在执行完前面的步骤后，vCenter Server 将无法正常使用，此时可以登录到 SCVM 所在的 ESXi 主机，手动执行 SCVM 虚拟机关机操作。
8. 参考下述步骤，在 vCenter Server 中依次关闭集群中所有的 ESXi 主机。

   1. 浏览到某个 SCVM 所在的 ESXi 主机，右键单击 ESXi 主机并选择**维护模式** > **进入维护模式**，ESXi 主机进入维护模式。
   2. 右键单击 ESXi 主机并选择**电源** > **关机**，关闭 ESXi 主机的电源。
   > **注意：**
   >
   > 若 vCenter Server 所在的 ESXi 主机也在集群中，建议通过 IPMI 管理台对 ESXi 主机执行关机。
9. 启动集群停机维护的相关工作。

---

## 集群下线 > SMTX ZBS 集群下线

# SMTX ZBS 集群下线

集群下线分为 3 个阶段：关闭系统服务虚拟机、关闭 CloudTower 虚拟机、检查并关闭集群所有节点。
集群上下线工具将自动判断集群中的虚拟机类型并执行关闭操作，无需手动区分。

1. 获取需维护集群的序列号。您可以在 CloudTower 的**集群**主界面中找到需维护的集群，然后在该集群的管理界面中单击**设置** > **软件许可**，在**许可信息**中即可获取集群的序列号。
2. 进入集群上下线工具所在目录。

   - 若集群上下线工具在集群的任一节点中，请登录该节点，然后进入工具所在的目录。
   - 若集群上下线工具在本地主机中，请使用终端工具打开集群上下线工具。
3. 关闭集群中的系统服务虚拟机。

   1. 执行如下命令，导出包含集群所有系统服务虚拟机信息的 `vms.csv` 文件，其中 `$CLUSTER_UUID` 表示在步骤 1 中获取的集群序列号。

      ```
      ./ctcli script vm export --cluster-uuid $CLUSTER_UUID > vms.cs
      ```
   2. 执行如下命令，从 `vms.csv` 文件中导出所有系统服务虚拟机信息至 `system-services.yaml` 文件中。

      ```
      ./ctcli script system-service export --cluster-uuid $CLUSTER_UUID --vms-file ./vms.csv 2>/dev/null > system-services.yaml
      ```

      如果工具执行环境为 Windows 系统，需将 `2>/dev/null` 替换为 `2>NUL`。
   3. 执行如下命令，关闭集群中的系统服务虚拟机。关闭过程中，您可在 CloudTower 的任务中心查看虚拟机关闭任务，确认关闭状态。

      ```
      ./ctcli script system-service stop --cluster-uuid $CLUSTER_UUID --services-file ./system-services.yaml
      ```
4. 执行如下命令，关闭集群中的 CloudTower 虚拟机。

   ```
   ./ctcli script tower stop --cluster-uuid $CLUSTER_UUID --services-file ./system-services.yaml
   ```
5. 执行如下命令，检查集群所有节点是否可以正常关闭。如果节点无法关闭，请根据对应的提示信息，解决问题后重新执行。

   ```
   ./ctcli script cluster stop-hosts --cluster-uuid $CLUSTER_UUID --check-only
   ```
6. 执行如下命令，检查并关闭集群所有节点。如果集群中的节点均可正常关机，检查通过后，会提示您再次输入集群序列号以确认关闭节点。

   ```
   ./ctcli script cluster stop-hosts --cluster-uuid $CLUSTER_UUID
   ```

   您也可以根据需求通过在命令中添加如下参数调整操作：

   `--comfirm-alert=true`：当检查发现集群存在硬件告警时，如果确认集群的硬件告警符合预期，可添加此参数忽略告警。

   `--disable-services=true`：若希望在集群重新上线后，不自动启动节点内的服务，可添加此参数禁止服务自启动。
7. 启动集群停机维护的相关工作。

---

## 集群上线 > SMTX OS（ELF）集群和 SMTX ELF 集群上线

# SMTX OS（ELF）集群和 SMTX ELF 集群上线

1. 将集群所有节点开机，并进入集群上下线工具所在目录。

   - 若集群上下线工具在集群的任一节点中，请登录该节点，然后进入工具所在的目录。
   - 若集群上下线工具在本地主机中，请使用终端工具打开集群上下线工具。
2. 根据在 [SMTX OS（ELF）集群和 SMTX ELF 集群下线](/cluster-onoff/1.0.4/cluster_onoff_user_guide/cluster_onoff_user_guide_04)的步骤 7 中，是否使用 `--disable-services=true` 参数禁止在集群重新上线后自动启动节点内的服务，选择对应步骤。

   - **未禁止服务自启动**：执行如下命令，确认集群网络连通性、时钟同步状态和内部服务状态正常。

     ```
     ./ctcli script cluster check-hosts
     ```

     若状态正常，将提示 `Check cluster success`。
   - **已禁止服务自启动**

     1. 执行如下命令，确认集群网络连通性和时钟同步状态正常，其中 `$mgt_ip` 表示集群内任一节点的管理 IP。

        ```
        ./ctcli script cluster check-hosts --cluster-connect-ip $mgt_ip --check-item network
        ./ctcli script cluster check-hosts --cluster-connect-ip $mgt_ip --check-item time
        ```

        > **注意**：
        >
        > 当在集群上下线工具的 `config.yaml` 文件中填写的集群 IP 地址不是管理虚拟 IP 时，无需添加 `--cluster-connect-ip $mgt_ip` 参数。

        若状态正常，将提示 `Check cluster success`。
     2. 执行如下命令，手动启动集群内的所有服务。

        ```
        ./ctcli script cluster start-hosts-services
        ```
     3. 执行如下命令，再次确认集群网络连通性、时钟同步状态和内部服务状态正常。

        ```
        ./ctcli script cluster check-hosts
        ```

        若状态正常，将提示 `Check cluster success`。
3. 执行如下命令，启动 CloudTower 虚拟机。启动后，您可通过浏览器访问 CloudTower 界面，确认 CloudTower 服务正常。

   ```
   ./ctcli script tower start --cluster-uuid $CLUSTER_UUID --services-file ./system-services.yaml
   ```
4. 确认 CloudTower 服务正常后执行如下命令，启动 CloudTower 代理虚拟机。

   ```
   ./ctcli script tower start-agent-mesh --cluster-uuid $CLUSTER_UUID --services-file ./system-services.yaml
   ```
5. 执行如下命令，启动系统服务虚拟机。启动过程中，您可在 CloudTower 的任务中心查看虚拟机启动任务，确认启动状态。

   ```
   ./ctcli script system-service start --cluster-uuid $CLUSTER_UUID --services-file ./system-services.yaml
   ```
6. 执行如下命令，启动业务虚拟机，虚拟机启动顺序与关闭顺序相反。启动过程中，您可在 CloudTower 任务中心查看虚拟机启动任务，确认启动状态。您也可以在输出结果中进行确认，如果 `ActionResult` 列显示为 `true`，表示虚拟机启动成功；如果显示为 `false`，则表示虚拟机启动失败。

   ```
   ./ctcli script vm start --cluster-uuid $CLUSTER_UUID --vms-file ./vms.csv
   ```

   在虚拟机启动过程中，集群上下线工具还会对 [SMTX OS（ELF）集群和 SMTX ELF 集群下线](/cluster-onoff/1.0.4/cluster_onoff_user_guide/cluster_onoff_user_guide_04)步骤 2 中标记为 `true` 的虚拟机进行检测。如果输出结果中 `CheckResult` 列显示为 `true`，表示虚拟机操作系统启动成功；如果显示为 `false`，则表示虚拟机操作系统启动失败或虚拟机内部存在问题。

---

## 集群上线 > SMTX OS（VMware ESXi）集群上线

# SMTX OS（VMware ESXi）集群上线

1. 在 vCenter Server 中依次对集群中所有的 ESXi 主机开机。

   > **注意：**
   >
   > 若 vCenter Server 所在的 ESXi 主机也在集群中，建议通过 IPMI 管理台对 ESXi 主机执行开机。
2. 开启 ESXi 主机后，在 vCenter Server 中右键单击 ESXi 主机并选择**维护模式** > **退出维护模式**，然后开启 ESXi 主机中的 SCVM 虚拟机。
3. 参考上一步开启集群中所有 ESXi 主机中的 SCVM 虚拟机。
4. 进入集群上下线工具所在的目录。

   - 若集群上下线工具在 SCVM 中，请使用 SSH 方式登录该 SCVM，然后进入工具所在的目录。
   - 若集群上下线工具在本地主机中，请使用终端工具打开集群上下线工具。
5. 参考以下步骤检查集群状态。

   请根据在 [SMTX OS（VMware ESXi）集群下线](/cluster-onoff/1.0.4/cluster_onoff_user_guide/cluster_onoff_user_guide_05)期间执行关闭 SCVM 命令时，是否使用 `--disable-services=true` 参数禁止在集群重新上线后自动启动 SCVM 内的服务，选择对应步骤。

   - **未禁止服务自启动**：执行以下命令，确认集群网络连通性、时钟同步状态和内部服务状态正常。

     ```
     ./ctcli script cluster check-hosts
     ```

     若状态正常，将提示 `Check cluster success`。
   - **已禁止服务自启动**

     1. 执行以下命令，确认集群网络连通性和时钟同步状态正常，其中 `$mgt_ip` 表示集群内任意一个 SCVM 管理 IP。

        ```
        ./ctcli script cluster check-hosts --cluster-connect-ip $mgt_ip --check-item network
        ./ctcli script cluster check-hosts --cluster-connect-ip $mgt_ip --check-item time
        ```

        > **注意**：
        >
        > 当在集群上下线工具的 `config.yaml` 文件中填写的集群 IP 地址不是管理虚拟 IP 时，无需添加 `--cluster-connect-ip $mgt_ip` 参数。

        若状态正常，将提示 `Check cluster success`。
     2. 执行以下命令启动 SCVM 内的服务。

        ```
        ./ctcli script cluster start-hosts-services
        ```
     3. 执行以下命令，再次确认集群网络连通性、时钟同步状态和内部服务状态正常。

        ```
        ./ctcli script cluster check-hosts
        ```

        若状态正常，将提示 `Check cluster success`。
6. 在 vCenter Server 中选中集群，然后在右侧界面单击**配置 > 服务 > vSphere 可用性**，在 vSphere 可用性设置界面右侧单击**编辑**，然后在弹出的**编辑集群设置**对话框中开启 **vSphere HA** 选项。单击**确定**，开启集群的 HA 功能。
7. 在 vCenter Server 中右键单击某个业务虚拟机，然后选择**启动** > **打开电源**。
8. 参考上一步，按需开启集群中的其他业务虚拟机。

---

## 集群上线 > SMTX ZBS 集群上线

# SMTX ZBS 集群上线

1. 将集群所有节点开机，并进入集群上下线工具所在目录。

   - 若集群上下线工具在集群的任一节点中，请登录该节点，然后进入工具所在的目录。
   - 若集群上下线工具在本地主机中，请使用终端工具打开集群上下线工具。
2. 根据在 [SMTX ZBS 集群下线](/cluster-onoff/1.0.4/cluster_onoff_user_guide/cluster_onoff_user_guide_15)的步骤 6 中，是否使用 `--disable-services=true` 参数禁止在集群重新上线后自动启动节点内的服务，选择对应步骤。

   - **未禁止服务自启动**：执行如下命令，确认集群网络连通性、时钟同步状态和内部服务状态正常。

     ```
     ./ctcli script cluster check-hosts
     ```

     若状态正常，将提示 `Check cluster success`。
   - **已禁止服务自启动**

     1. 执行如下命令，确认集群网络连通性和时钟同步状态正常，其中 `$mgt_ip` 表示集群内任一节点的管理 IP。

        ```
        ./ctcli script cluster check-hosts --cluster-connect-ip $mgt_ip --check-item network
        ./ctcli script cluster check-hosts --cluster-connect-ip $mgt_ip --check-item time
        ```

        > **注意**：
        >
        > 当在集群上下线工具的 `config.yaml` 文件中填写的集群 IP 地址不是管理虚拟 IP 时，无需添加 `--cluster-connect-ip $mgt_ip` 参数。

        若状态正常，将提示 `Check cluster success`。
     2. 执行如下命令，手动启动集群内的所有服务。

        ```
        ./ctcli script cluster start-hosts-services
        ```
     3. 执行如下命令，再次确认集群网络连通性、时钟同步状态和内部服务状态正常。

        ```
        ./ctcli script cluster check-hosts
        ```

        若状态正常，将提示 `Check cluster success`。
3. 执行如下命令，启动 CloudTower 虚拟机。启动后，您可通过浏览器访问 CloudTower 界面，确认 CloudTower 服务正常。

   ```
   ./ctcli script tower start --cluster-uuid $CLUSTER_UUID --services-file ./system-services.yaml
   ```
4. 执行如下命令，启动系统服务虚拟机。启动过程中，您可在 CloudTower 的任务中心查看虚拟机启动任务，确认启动状态。

   ```
   ./ctcli script system-service start --cluster-uuid $CLUSTER_UUID --services-file ./system-services.yaml
   ```

---

## 集群上下线工具命令参数说明

# 集群上下线工具命令参数说明

本章中提到的命令行格式说明如下表所示。您在任何命令后都可以输入 `-h` 或者 `--help` 获得此命令的帮助提示。

| **格式** | **描述** |
| --- | --- |
| `./ctcli script cluster start-hosts-services` | 不带参数的命令，按原样输入。 |
| `<check-item>` | 尖括号表示必选参数，需用参数值代替。  语法：`--check-item <check-item>`  输入：`--check-item network` |
| `|` | 竖线用于分隔多个互斥的可选参数。 |
| `{}` | 大括号表示有多个参数，但必选一个。 |
| `[]` | 方括号表示可选参数，可为空。 |

---

## 集群上下线工具命令参数说明 > 控制集群

# 控制集群

## 检查集群状态

`./ctcli script cluster check-hosts [--check-item <check-item>] [--cluster-uuid <string>]`

| **参数** | **说明** |
| --- | --- |
| `--check-item <check-item>` | 集群状态的检查项，`<check-item>` 可以替换为以下参数：  - all：默认值，所有检查项 - network：网络连通情况 - time：时钟同步情况 - service：节点服务状态 |
| `--cluster-uuid <string>` | 集群的序列号。 |

## 启动并检查集群所有主机服务

`./ctcli script cluster start-hosts-services`

## 检查并关闭集群所有节点

`./ctcli script cluster stop-hosts --cluster-uuid <string> [--check-only] [--confirm-alert={true|false}] [--disable-services={true|false}`  
`] [--force={true|false}]`

| **参数** | **说明** |
| --- | --- |
| `--cluster-uuid <string>` | 集群的序列号。 |
| `--check-only` | 仅检查集群节点是否可以正常关闭。 |
| `--confirm-alert={true|false}` | 确认集群告警，即使集群存在硬件告警也会忽略，默认为 `false`。 |
| `--disable-services={true|false}` | 禁止在集群重新上线后自动启动节点内的服务，默认为 `false`。 |
| `--force={true|false}` | 强制关闭集群节点，跳过预检查，默认为 `false`。 |

---

## 集群上下线工具命令参数说明 > 导出集群中所有虚拟机信息

# 导出集群中所有虚拟机信息

`./ctcli script vm export --cluster-uuid <string>`

| **参数** | **说明** |
| --- | --- |
| `--cluster-uuid <string>` | 集群的序列号。 |

---

## 集群上下线工具命令参数说明 > 操作所有系统服务虚拟机

# 操作所有系统服务虚拟机

## 导出所有系统服务虚拟机信息

`./ctcli script system-service export --cluster-uuid <string> --vms-file <vms_file_name>`

| **参数** | **说明** |
| --- | --- |
| `--cluster-uuid <string>` | 集群的序列号。 |
| `--vms-file <vms_file_name>` | 包含所有虚拟机信息的文件名。 |

## 启动所有系统服务虚拟机

`./ctcli script system-service start --cluster-uuid <string> --service-file <service_file_name>`

| **参数** | **说明** |
| --- | --- |
| `--cluster-uuid <string>` | 集群的序列号。 |
| `--service-file <service_file_name>` | 包含系统服务虚拟机信息的文件名。 |

## 关闭所有系统服务虚拟机

`./ctcli script system-service stop --cluster-uuid <string> --service-file <service_file_name>`

| **参数** | **说明** |
| --- | --- |
| `--cluster-uuid <string>` | 集群的序列号。 |
| `--service-file <service_file_name>` | 包含系统服务虚拟机信息的文件名。 |

---

## 集群上下线工具命令参数说明 > 操作 CloudTower 虚拟机和代理虚拟机

# 操作 CloudTower 虚拟机和代理虚拟机

## 启动 CloudTower 虚拟机

`./ctcli script tower start --cluster-uuid <string> --service-file <service_file_name>`

| **参数** | **说明** |
| --- | --- |
| `--cluster-uuid <string>` | 集群的序列号。 |
| `--service-file <service_file_name>` | 包含系统服务虚拟机信息的文件名。 |

## 关闭 CloudTower 虚拟机

`./ctcli script tower stop --cluster-uuid <string> --service-file <service_file_name>`

| **参数** | **说明** |
| --- | --- |
| `--cluster-uuid <string>` | 集群的序列号。 |
| `--service-file <service_file_name>` | 包含系统服务虚拟机信息的文件名。 |

## 启动 CloudTower 代理虚拟机

`./ctcli script tower start-agent-mesh --cluster-uuid <string> --service-file <service_file_name>`

| **参数** | **说明** |
| --- | --- |
| `--cluster-uuid <string>` | 集群的序列号。 |
| `--service-file <service_file_name>` | 包含系统服务虚拟机信息的文件名。 |

## 关闭 CloudTower 代理虚拟机

`./ctcli script tower stop-agent-mesh --cluster-uuid <string> --service-file <service_file_name>`

| **参数** | **说明** |
| --- | --- |
| `--cluster-uuid <string>` | 集群的序列号。 |
| `--service-file <service_file_name>` | 包含系统服务虚拟机信息的文件名。 |

---

## 集群上下线工具命令参数说明 > 操作集群中所有业务虚拟机

# 操作集群中所有业务虚拟机

## 启动集群中所有业务虚拟机

`./ctcli script vm start --cluster-uuid <string> --vms-file <vms_file_name> [--parallel={true|false}]`

| **参数** | **说明** |
| --- | --- |
| `--cluster-uuid <string>` | 集群的序列号。 |
| `--vms-file <vms_file_name>` | 包含所有虚拟机信息的文件名。 |
| `--parallel={true|false}` | 是否并行启动虚拟机，默认为 `true`。 |

## 关闭集群中所有业务虚拟机

`./ctcli script vm stop --cluster-uuid <string> --vms-file <vms_file_name> [--force={true|false}] [--parallel={true|false}]`

| **参数** | **说明** |
| --- | --- |
| `--cluster-uuid <string>` | 集群的序列号。 |
| `--vms-file <vms_file_name>` | 包含所有虚拟机信息的文件名。 |
| `--force={true|false}` | 表示是否强制关闭（断电）所有虚拟机，默认为 `false`。 |
| `--parallel={true|false}` | 表示是否并行启动虚拟机，默认为 `true`。 |

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
