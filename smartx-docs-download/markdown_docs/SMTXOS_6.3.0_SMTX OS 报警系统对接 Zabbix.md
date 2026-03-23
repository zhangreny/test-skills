---
title: "SMTXOS/6.3.0/SMTX OS 报警系统对接 Zabbix"
source_url: "https://internal-docs.smartx.com/smtxos/6.3.0/zabbix_alert/zabbix_alert_preface"
sections: 19
---

# SMTXOS/6.3.0/SMTX OS 报警系统对接 Zabbix
## 关于本文档

# 关于本文档

SMTX OS 内置有报警功能，并提供了图形化界面对集群报警进行管理。但在实际场景中，部分客户也会使用第三方工具管理集群的报警信息，典型的第三方工具为 Zabbix。

本文档介绍了如何在 Zabbix 端和 SMTX OS 端进行配置，将 SMTX OS 的报警系统与 Zabbix 进行对接，从而实现通过 Zabbix 监控集群的报警信息。

阅读本文档需了解 SMTX OS 超融合软件，了解虚拟化、软件定义存储、分布式存储等相关技术背景知识，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

**2026-02-04：配合 SMTX OS 6.3.0 正式发布**

---

## 安装 Zabbix

# 安装 Zabbix

Zabbix 一般安装在集群外的虚拟机中，用以监控集群的健康状况。在实际环境中，若客户已安装了 Zabbix，可跳过此安装介绍。

Zabbix 支持在多个操作系统中安装，本文以 CentOS7-minimal 操作系统下安装 Zabbix 4.0 LTS 为例，介绍 Zabbix 的安装操作。更多操作系统下的安装可参考 Zabbix 官方的[安装指引](https://www.Zabbix.com/download)。

---

## 安装 Zabbix > 安装前准备

# 安装前准备

## 设置安装环境

在安装 Zabbix 前，请先安装 epel-release repo，以获取一些系统自带 repo 无法获取的 rpm。并关闭 SELinux 服务和 firewalld 防火墙，避免后续无法访问 Zabbix Web 前端。

**操作步骤**

1. 安装 epel-release repo。

   ```
   yum install -y epel-release
   yum update -y
   ```
2. 关闭 SELinux 服务。

   ```
   sed -i.bak 's/^SELINUX=.*$/SELINUX=disabled/g' /etc/selinux/config
   setenforce 0
   ```
3. 关闭 firewalld 防火墙。

   ```
   systemctl disable firewalld
   systemctl stop firewalld
   ```

## 安装 MySQL 数据库

Zabbix 从 SMTX OS 集群获取的监控数据需要存储到数据库中。Zabbix 官方支持的数据库有 MySQL 和 PostgreSQL，本文以 MySQL 5.7 版本为例, 介绍数据库的安装方法。

**操作步骤**

1. 安装 MySQL 5.7 community release repo。

   ```
   yum install -y https://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/mysql57-community-release-el7-10.noarch.rpm
   ```
2. 安装 MySQL Server。

   ```
   rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022
   yum install -y mysql-community-server
   ```
3. 启用 mysqld 服务。

   ```
   systemctl enable mysqld
   systemctl start mysqld
   ```
4. 更新 MySQL root 密码。

   ```
   grep 'temporary password' /var/log/mysqld.log
   mysql_secure_installation
   ```

---

## 安装 Zabbix > 安装 Zabbix Server

# 安装 Zabbix Server

Zabbix Server 是 Zabbix 的核心组件，用于获取 SMTX OS 集群发出的监控信息。请按照如下操作安装 Zabbix Server，并设置 Zabbix 访问 MySQL 的用户名及密码。

**操作步骤**

1. 安装 Zabbix release repo。

   ```
   yum install -y https://repo.zabbix.com/zabbix/4.0/rhel/7/x86_64/zabbix-release-4.0-1.el7.noarch.rpm
   ```
2. 安装 Zabbix server。

   ```
   yum install -y zabbix-server-mysql
   ```
3. 设置 Zabbix 访问 MySQL 数据库的用户名。此处以用户名为 `zabbix` 举例。

   ```
   mysql -u root -p <<EOF
   CREATE DATABASE zabbix CHARACTER SET utf8 COLLATE utf8_bin;
   CREATE USER 'zabbix'@'localhost' IDENTIFIED BY '!QAZ2wsx';
   GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'localhost';
   EOF
   ```
4. 初始化 Zabbix 的 MySQL 数据库。

   ```
   zcat /usr/share/doc/zabbix-server-mysql-*/create.sql.gz | mysql -u zabbix -p zabbix
   ```
5. 设置 Zabbix 访问 MySQL 数据库的密码。此处以设置密码为 `!QAZ2wsx` 为例。

   ```
   cat <<'EOF' >> /etc/zabbix/zabbix_server.conf
   DBPassword=!QAZ2wsx
   EOF
   ```
6. 启用 Zabbix Server 服务。

   ```
   systemctl enable zabbix-server
   systemctl start zabbix-server
   ```

---

## 安装 Zabbix > 安装 Zabbix Web 前端

# 安装 Zabbix Web 前端

Zabbix Web 是 Zabbix 配套的前端工具，用于管理监控数据源、绘制监控数据、呈现报警的组件。用户可以通过 Web 前端，设置监控的数据类型，并查看监控数据。

**操作步骤**

1. 安装 Zabbix Web 前端。

   ```
   yum install -y zabbix-web-mysql
   ```
2. 设置 Zabbix Web 前端的时区。

   ```
   sed -i.bak 's/# php_value date.timezone .*$/php_value date.timezone Asia\/Hong_Kong/g' /etc/httpd
   /conf.d/zabbix.conf
   ```
3. 重启 httpd 服务。

   ```
   systemctl restart httpd
   ```

---

## 安装 Zabbix > 连通 MySQL 数据库

# 连通 MySQL 数据库

1. 在浏览器输入 `http://<ip>/zabbix`，打开 Zabbix Web 前端。其中 `ip` 为Zabbix 所在节点的 IP 地址。默认的登录用户名为 Admin，密码为 zabbix。
2. 在 **Welcome** 和 **Check of pre-requests** 步骤直接单击 **Next step**，进入 **Configure DB connection** 配置，选择数据库类型为 MySQL，并输入已创建的 MySQL 数据库的用户名和密码。

   ![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_01.png)
3. 后续步骤中，可直接单击 **Next step**，完成所有配置。

---

## 配置 Zabbix

# 配置 Zabbix

请参考如下步骤配置 Zabbix。

---

## 配置 Zabbix > 配置 Zabbix Server

# 配置 Zabbix Server

Zabbix Server 端配置 SNMP Trap 接收时，可采用以下两种方式完成 trap 的格式化解析。请根据相应步骤，完成 Zabbix Server 的配置。

- 基于 bash trap 接收脚本方式
- 基于 snmptt 方式

> **说明**：
>
> 新版本操作系统上（比如 centos8 ）已经无法安装 snmptt，推荐使用基于 bash trap 接收脚本方式配置 Zabbix Server。

---

## 配置 Zabbix > 配置 Zabbix Server > 配置 Zabbix Server（基于 bash trap 接收脚本方式）

# 配置 Zabbix Server（基于 bash trap 接收脚本方式）

## 启用 SNMP Trapper

1. 启用 SNMP Trapper 以接收 trap 信息，并设置接收 trap 信息的 SNMPTrapperFile 文件。

   ```
   cat <<'EOF' >> /etc/zabbix/zabbix_server.conf
   StartSNMPTrapper=1
   SNMPTrapperFile=/var/lib/zabbix/snmptraps/snmptraps.log
   EOF
   ```

   > **参数说明**：
   >
   > - `StartSNMPTrapper=1`：将此参数设置为 1，以启动 SNMP Trapper 进程。
   > - `SNMPTrapperFile=/var/lib/zabbix/snmptraps/snmptraps.log`：指定一个用于存储 Trap 的文件。请确保文件所在的目录已存在，并且 Zabbix 用户（通常为 `zabbix`）有读写权限 。建议使用示例中的路径。
2. 重启 Zabbix Server 以使配置生效。

   ```
   systemctl restart zabbix-server
   ```

## 配置 snmptrapd 和 Bash 接收器脚本

这一步的目的是让系统自带的 snmptrapd 服务在收到 Trap 后，将数据转发给一个脚本，由这个脚本负责格式化和写入 Zabbix 的 Trap 文件。

1. 下载官方的 Bash 接收器脚本：

   官方在 GitHub 上提供了可直接使用的脚本。将其下载到系统的可执行路径下（如 `/usr/sbin/`）。 以下示例是以 zabbix 7.0 版本里为例，请根据实际版本做修改。

   ```
   curl -o /usr/sbin/zabbix_trap_handler.sh https://raw.githubusercontent.com/zabbix/zabbix-docker/7.0/Dockerfiles/snmptraps/alpine/conf/usr/sbin/zabbix_trap_handler.sh
   ```
2. 为脚本添加可执行权限。

   ```
   chmod +x /usr/sbin/zabbix_trap_handler.sh
   ```
3. 修改 `/usr/sbin/zabbix_trap_handler.sh` 中 `ZABBIX_TRAPS_FILE` 一行的配置和[启用 SNMP Trapper](#%E5%90%AF%E7%94%A8-snmp-trapper)步骤 1 中的 `zabbix SNMPTrappFile` 为同一文件。

   ```
   ZABBIX_TRAPS_FILE="/var/lib/zabbix/snmptraps/snmptraps.log"
   ```
4. 在 `/etc/snmp/snmptrapd.conf` 添加如下配置，然后重启 snmptrapd 服务即可。

   ```
   traphandle default /bin/bash /usr/sbin/zabbix_trap_handler.sh
   disableAuthorization yes
   ```

---

## 配置 Zabbix > 配置 Zabbix Server > 配置 Zabbix Server（基于 snmptt 方式）

# 配置 Zabbix Server（基于 snmptt 方式）

## 启用 SNMP Trapper

1. 启用 SNMP Trapper 以接收 trap 信息，并设置接收 trap 信息的 SNMPTrapperFile 文件。

   ```
   cat <<'EOF' >> /etc/zabbix/zabbix_server.conf
   StartSNMPTrapper=1
   SNMPTrapperFile=/var/log/snmptt/snmptt.log
   EOF
   ```
2. 重启 Zabbix Server 以使配置生效。

   ```
   systemctl restart zabbix-server
   ```

## 安装 snmptrapd 服务

snmptrapd 用于 Zabbix 接收 SMTX OS 集群发出的 SNMP Trap 信息。请执行以下命令安装并启用 snmptrapd 服务。

1. 安装 snmptrapd 服务。

   ```
   yum install -y net-snmp
   ```
2. 设置 snmptrapd 使用 snmptt 处理 trap 信息。

   ```
   cat <<'EOF' >> /etc/snmp/snmptrapd.conf
   disableAuthorization yes
   traphandle default snmptt
   EOF
   ```
3. 设置 snmptrapd 的命令行选项。

   ```
   cat <<'EOF' >> /etc/sysconfig/snmptrapd
   OPTIONS="-On -Lsd"
   EOF
   ```
4. 启用 snmptrapd 服务。

   ```
   systemctl start snmptrapd
   ```

## 安装 snmptt

snmptt（SNMP Trap Translator） 用于将接收的原始报警信息（trap 消息）进行格式化输出，使原始的报警内容更易于阅读。若客户的实际环境中未安装 snmptt，则建议参考格式化报警内容，对报警信息进行正则化。

1. 安装 snmptt。

   ```
   yum install -y snmptt perl-Sys-Syslog
   ```
2. 设置 snmptt 的时间输出格式。

   ```
   sed -i.bak 's/#date_time_format =/date_time_format = %H:%M:%S %Y\/%m\/%d/g' /etc/snmp/snmptt.ini
   ```
3. 设置 snmptt 的 trap 消息过滤格式。

   ```
   cat <<'EOF' >> /etc/snmp/snmptt.conf
   #
   #
   #
   EVENT general .* SMTXOS-Alert
   FORMAT ZBXTRAP $aA [$7:$4] $6
   EOF
   ```

---

## 配置 Zabbix > 配置 SNMP Host 和 SNMP Item

# 配置 SNMP Host 和 SNMP Item

当 Zabbix 对接 SMTX OS 报警系统时，需创建 SNMP Host，并为 Host 创建一个 SNMP Item，用以监控集群的报警信息。其中，SNMP Host 定义了 Zabbix 监控的 SMTX OS 集群，SNMP Item 为监控的数据类型。

---

## 配置 Zabbix > 配置 SNMP Host 和 SNMP Item > 创建 SNMP Host

# 创建 SNMP Host

一个 SMTX OS 集群可以创建多个 SNMP Host，若需监控多个集群，请为每个集群和每个可观测性服务分别创建 SNMP Host。

**操作步骤**

1. 在浏览器输入 `http://<ip>/Zabbix`，打开 Zabbix Web 前端，其中 `ip` 为 Zabbix 所在节点的 IP 地址。输入 Zabbix 前端的用户名和密码，默认的用户名和密码分别为 Admin 和 zabbix。
2. 进入 **Configuration** > **Hosts** 界面 ，单击 **Create host**，弹出如下配置界面，并配置相关参数。

   ![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_14.png)

   | 参数 | 描述 |
   | --- | --- |
   | Host name | 输入 SNMP Host 的名称。 |
   | Groups | 选择 Host 所在的 Group。 |
   | SNMP interfaces | 根据以下规则输入 IP 地址，并将端口设置为 `161`： - 若集群已关联可观测性服务，则输入可观测性服务的 IP 地址。 - 若集群未关联可观测性服务，则：   - 若集群已配置 VIP，则输入集群的 VIP 地址。   - 若集群未配置 VIP，则输入 SMTX OS 集群中 zbs-taskd leader 节点的管理 IP 地址。若 Zabbix 与 SMTX OS 节点跨网关，请同时添加网关 IP 地址。 |
3. 单击 **Add**，完成 SNMP Host 的创建。
4. 若该集群未配置 VIP，则重复步骤 2-3，为集群内的每个 master 节点创建 SNMP Host。在配置 SNMP interfaces 参数时，输入当前节点的管理 IP 地址，若 Zabbix 与 SMTX OS 节点跨网关，请同时添加网关 IP 地址。
5. （可选）若客户直接使用 Zabbix Server 接受报警信息则可跳过此步骤。当客户需要通过 Zabbix Proxy 接收集群发送的报警信息时，则可在 **Host** 页面的 **Monitored by proxy** 下拉框选择对应的 Zabbix Proxy 完成配置，如下图所示。

   ![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_15.png)

---

## 配置 Zabbix > 配置 SNMP Host 和 SNMP Item > 创建 SNMP Item

# 创建 SNMP Item

**操作步骤**

1. 单击已创建的 SNMP Host，选择 Items 配置。单击 **Create item**，弹出 Item 配置界面。
2. 在 **Item** 配置界面，配置如下参数。

   ![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_16.png)

   | 参数 | 描述 |
   | --- | --- |
   | Name | 输入Item 的名称。 |
   | Type | 选择 Item 类型为 “SNMP trap”。 |
   | Host Interface | 选择 Item 类型后自动填充。 |
   | Type of information | 选择 “Log”。 |
   | Log time format | 输入 Log 的时间格式。例如：`hh:mm:ss yyyy/MM/dd`。 |
3. 单击 **Add**，完成 **SNMP Item** 的创建。
4. （可选）解析中文报警文案。

   由于中文字符在 SNMP TRAP 消息中以 16 进制字符的形式传输，且 zabbix 默认没有中文解析，因此若报警对接时语言选择中文，则在zabbix 页面将呈现 16 进制字符的报警信息，不利于用户阅读。

   当客户环境已安装 snmptt 时，您可通过如下步骤增加中文字符处理。配置后，报警文案将自动被解析为中文字符进行展示。若未安装 snmptt，请参考[中文报警对接](/smtxos/6.3.0/zabbix_alert/zabbix_alert_12#%E4%B8%AD%E6%96%87%E6%8A%A5%E8%AD%A6%E5%AF%B9%E6%8E%A5)中的步骤进行操作以进行中文解析。

   > **注意**：
   >
   > 仅 4.2 及以上版本的 Zabbix 支持自定义 JavaScript 的 item preprocessing，在配置解析中文报警文案之前，请确认您安装的 Zabbix 的版本满足要求。

   1. 在 **Create item** 界面，单击 **PreProcessing**，进入配置界面。

      ![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_17.png)
   2. 配置 JavaScript 脚本，内容如下：

      ```
      function hex2a(input){
      const markers = ["INFO]", "NOTICE]", "CRITICAL]"];
      var leftPart = "";
      var rightPart = "";
      for (var i = 0; i < markers.length; i++) {
          const marker = markers[i];
          const index = value.indexOf(marker);

          if (index !== -1) {
          leftPart = value.substring(0, index).trim();
          leftPart = leftPart + marker;
          rightPart = value.substring(index + marker.length).trim().replace(/\s*/g,"").toString();
          break;
          }
      }

      var str = '';
      try{
          for (var i = 0; i < rightPart.length && rightPart.substr(i,2)!== '00'; i += 2)
          str += String.fromCharCode(parseInt(rightPart.substr(i, 2), 16));
          str = leftPart + " " + decodeURIComponent(escape(str)) + "\n";
      }
      catch(err) {
          str = input
      }

      return str
      }
      return hex2a(value);
      ```
   3. 单击界面右侧的 **Test** 按钮，并在弹出的对话框中输入如下信息，以测试配置是否生效。

      | 参数 | 描述 |
      | --- | --- |
      | Value | 输入测试示例，可分别输入中文示例和英文示例以分别测试中英文解析是否有效。 - **中文示例**：  15:55:11 2023/12/26 .1.3.6.1.4.1.42000.9999.28 "SMTXOS-Alert" UNKNOWN - ZBXTRAP 172.20.221.135 [TRIGGERED:CRITICAL] E4 B8 BB E6 9C BA 20 73 63 61 6C 65 2D 31 20 E7 9A 84 E6 9C 8D E5 8A A1 E8 BF 9B E7 A8 8B 20 65 6C 66 2D 64 68 63 70 20 E6 9C AA E8 BF 90 E8 A1 8C E3 80 82 - **英文示例**：  03:37:31 2023/12/24 .1.3.6.1.4.1.42000.9999.34 "SMTXOS-Alert" UNKNOWN - ZBXTRAP 172.20.221.135 [RESOLVED:CRITICAL] The storage network 5-minute P90 ping response time is greater than 5ms between the two hosts: scale-1 and juan-li-smtxos-6-0-0-b121X20231214113913X1. |
      | Time | - |
      | Previous value | - |
      | Previous time | - |
      | End of line sequence | 选择 **LF** |

      当中英文解析分别输出如下结果时，表明配置成功。

      - **中文解析结果**：

        ![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_18.png)
      - **英文解析结果**：

        ![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_19.png)

---

## 配置 Zabbix > 配置 SNMP Host 和 SNMP Item > 格式化报警内容（未安装 snmptt）

# 格式化报警内容（未安装 snmptt）

> **说明**：
>
> - 若客户环境未安装 snmptt，或者使用了 Bash 或 Perl 将 Trap 消息写入 SNMPTrapperFile。为使接收的 Trap 消息更易于阅读，请参考本节内容对 Trap 信息进行格式化。若客户已安装 snmptt ，可跳过此步骤。
> - 若用户环境安装的是 Zabbix 7.x，请参考 [FAQ](/smtxos/6.3.0/zabbix_alert/zabbix_alert_15#q%E8%8B%A5%E7%94%A8%E6%88%B7%E4%BD%BF%E7%94%A8%E7%9A%84%E6%98%AF-zabbix-7x%E5%A6%82%E4%BD%95%E6%8F%90%E5%8F%96-zabbix-trap-%E6%8A%A5%E8%AD%A6%E6%96%87%E6%A1%88) 中的步骤进行处理。

## 英文报警对接

当报警内容为英文时，请参考如下步骤进行格式化。

**操作步骤**

1. 在 **Create item** 界面，单击 **PreProcessing**，进入格式化界面。

   ![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_20.png)
2. 添加正则表达式提取报警内容。

   添加的正则表达式与 snmptrapd 服务的日志输出格式有关，需要根据具体输出的日志调整匹配使用的正则表达式，下面以如下日志为例添加正则表达式提取所需字段。

   **日志示例**：

   ```
   2023-12-01 16:39:05 <UNKNOWN> [UDP: [192.168.29.131]:60858->[192.168.27.106]:162]:
   .1.3.6.1.2.1.1.3.0 = Timeticks: (1701419918) 196 days, 22:09:59.18        .1.3.6.1.6.3.1.1.4.1.0 = OID: .1.3.6.1.4.1.42000.9999.34        .1.3.6.1.4.1.42000.999 = OID: .1.3.6.1.4.1.42000.9999.34        .1.3.6.1.4.1.42000.999.1 = Timeticks: (1701419917) 196 days, 22:09:59.17        .1.3.6.1.4.1.42000.999.3 = INTEGER: 30        .1.3.6.1.4.1.42000.999.4 = STRING: "CRITICAL"        .1.3.6.1.4.1.42000.999.5 = IpAddress: 192.168.29.131        .1.3.6.1.4.1.42000.999.2 = STRING: "The storage network 5-minute P90 ping response time is greater than 5ms between the two hosts: yingjie-511X20230809114256X1 and yingjie-511X20230809114256X3."        .1.3.6.1.4.1.42000.999.6 = STRING: "TRIGGERED"
   ```

   **正则表达式**：

   `pattern： \"(.*)\"([\s\S]*?)(\d+\.\d+\.\d+\.\d+)([\s\S]*?)\"(.*)\"`

   - 第 1 组：`\”(.*)\”` 用于匹配“”内表示报警级别的任意字符串，如 CRITICAL；
   - 第 2 组：`([\s\S]*?)` 用于匹配包括换行在内的任意字符；
   - 第 3 组：`(\d+\.\d+\.\d+\.\d+)` 用于匹配 SMTX OS 集群的 IP 地址；
   - 第 4 组：`([\s\S]*?)` 同第 2 组，用于匹配包括换行在内的任意字符；
   - 第 5 组：`\”(.*)\”` 用于匹配报警文案。

   **匹配结果**：

   在实际情况中，不同客户希望呈现的报警内容格式可能不同，此处以正则表达式输出 `SMTX-Alert level(\1), ip(\3), message(\5)` 为例，展示如何通过正则表达式设置报警内容呈现格式。

   其中：

   - `SMTX-Alert level(\1)` 表示使用第 1 组正则表达式过滤出报警级别；
   - `ip(\3)` 表示使用第 3 组正则表达式过滤出 SMTX OS 集群的 IP 地址；
   - `message(\5)` 表示使用第 5 组正则表达式过滤出报警的内容。

   在上述正则表达式下，过滤出以下格式的报警内容：`SMTX-Alert level(CRITICAL), ip(192.168.x.x), message(The cluster is recovering data.)`，即过滤出 IP 地址为 `192.168.x.x` 的集群内，报警级别为 `CRITICAL` ，报警内容为 `The cluster is recovering data.` 的报警信息。

## 中文报警对接

由于 snmptrapd 的日志内中文是 16 进制字符串，因此当报警信息中包括中文字符时，需要根据实际输出格式调整匹配使用的正则表达式，并增加脚本转义匹配到的报警相关字段。

**操作步骤**

1. 添加正则表达式。

   **日志示例**：

   ```
   15:24:32 2023/11/09 ZBXTRAP 10.111.130.216
   PDU INFO:
   notificationtype            TRAP
   transactionid               5603
   community                   public
   errorstatus                 0
   version                     1
   requestid                   37
   receivedfrom                UDP: [10.111.130.216]:55152->[10.110.224.15]:162
   errorindex                  0
   messageid                   0
   VARBINDS:
   DISMAN-EVENT-MIB::sysUpTimeInstance type=67 value=Timeticks: (1699514672) 196 days, 16:52:26.72
   SNMPv2-MIB::snmpTrapOID.0      type=6  value=OID: SNMPv2-SMI::enterprises.42000.9999.37
   SNMPv2-SMI::enterprises.42000.999 type=6  value=OID: SNMPv2-SMI::enterprises.42000.9999.37
   SNMPv2-SMI::enterprises.42000.999.1 type=67 value=Timeticks: (1699514671) 196 days, 16:52:26.71
   SMMPv2-SMI::enterprises.42000.999.3 type=2  value=INTEGER: 20
   SNMPV2-SMI::enterprises.42000.999.4 type=4  value=STRING: "NOTICE"
   SNMPv2-SMI::enterprises.42000.999.5 type=64 value=IpAddress: 10.111.130.81
   SNMPv2-SMI::enterprises.42000.999.2 type=4  value=Hex-STRING: E4 B8 8B E5 88 97 20 31 20 E8 8A 82 E7 82 B9 E7
   9A 84 20 49 50 4D 49 20 E4 BF A1 E6 81 AF E6 9C
   AA E8 AE BE E7 BD AE E6 88 96 E8 AE BE E7 BD AE
   E4 B8 8D E6 AD A3 E7 A1 AE EF BC 9A 7A 6A 73 6D
   78 64 65 76 2D 63 36 2D 6E 66 35 32 38 30 6D 36
   2D 66 30 35 E3 80 82
   SNMPv2-SMI::enterprises.42000.999.6 type=4  value=STRING: "TRIGGERED"
   ```

   **正则表达式**：

   `pattern： \"(.*)\"([\s\S]*?)(\d+\.\d+\.\d+\.\d+)([\s\S]*?)\"(.*)\"`

   **匹配结果**：

   - 第 1 组 `\”(.*)\”` 报警级别 CRITICAL；
   - 第 2 组 `([\s\S]*?)` 用于匹配包括换行在内的任意字符；
   - 第 3 组 `(\d+\.\d+\.\d+\.\d+)` 用于匹配 SMTX OS 集群的 IP 地址 10.111.130.81；
   - 第 4 组 `([\s\S]*?)` 同第 2 组，用于匹配包括换行在内的任意字符，此时匹配到的内容为从 ip 地址下一行开始，”TRIGGERED” 之前的所有内容；
   - 第 5 组 `\”(.*)\”` 报警状态 TRIGGERED。
2. 配置中文转义。

   当客户现场的 snmptrapd 实际输出格式与文档不同时可以组合使用各字段。获取各字段内容后需要通过脚本转义中文文案。

   在 **Create item** 界面，单击 **PreProcessing**，正则匹配之后添加 JavaScript 脚本，用于转义 16 进制报警文案，内容如下：

   ![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_21.png)

   JavaScript 脚本内容如下：

   ```
   function hex2a(hexx){
   var parts = hexx.split('Hex-STRING: ');
   var pre = parts[0].split("SNMPv2-SMI")
   var p = pre[0]
   var partion = parts[1].split('SNMPv2-SMI');
   var hex = partion[0].replace(/\s*/g,"").toString();
   var str = '';
   for (var i = 0; i < hex.length && hex.substr(i,2)!== '00'; i += 2)
       str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
   str = p + decodeURIComponent(escape(str)) + "）\n";
   return str
   }
   return hex2a(value);
   ```

---

## SMTX OS 集群端配置

# SMTX OS 集群端配置

1. 登录 CloudTower，在**报警**主界面左侧的导航树选择**通知配置**，单击右上角 **+ 创建通知配置**，选择**创建 SNMP 陷阱配置**。
2. 在弹出的**创建 SNMP 陷阱配置**界面，设置如下参数。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | 输入用户名，可任意填写。 |
   | 版本 | 选择 SNMP 陷阱的协议版本，选择 v2c 。 |
   | 应用对象 | 选择 SNMP 陷阱配置的应用对象。 |
   | 远端 IP | 输入 Zabbix Server 所在节点的 IP 地址。若用户配置了 Zabbix Proxy，则填写 Zabbix Proxy 所在节点的 IP 地址。 |
   | 端口 | 输入“162” 。 |
   | 团体名 | 指定用于访问远程 SNMP 管理器的团体名。 |
   | 启用配置 | 开启启用配置开关 |
3. 单击**创建**，完成 SNMP 陷阱的创建。

---

## 验证对接是否成功

# 验证对接是否成功

完成 Zabbix 端和 SMTX OS 端的配置后，请参考以下方法验证 Zabbix 和 SMTX OS 的报警系统是否对接成功。

**操作步骤**

1. 进入 CloudTower 或者 SMTX OS 的 Web 控制台，手动解决一个报警。

   > **说明**：
   >
   > 目前 CloudTower 仅支持手动解决优先类型的报警， 若没有可以手动解决的报警，可通过修改告警规则来临时触发告警。
2. 进入 Zabbix Web 前端，在 **Monitoring** > **Latest data** 页面，选择对应的 Host，点击 **History** 查看是否出现了对应的报警条目。若出现相应的报警条目，则说明配置成功。

   ![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_22.png)

   ![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_23.png)

---

## 附录 > FAQ

# FAQ

## Q：若 Zabbix 端无法查看 SMTX OS 端的报警信息，应该怎么办？

A：请参考如下思路进行问题定位：

1. 请参考以上配置介绍，确认 SMTX OS 端和 Zabbix Server 端已配置正确。
2. 在 SMTX OS 节点抓包，查看报警信息的发送是否正常。

   在 SMTX OS 节点，执行 `tcpdump -i port -mgt host ip -w 100.cap` 命令，抓取节点向 Zabbix Server 发送的报文，其中 `ip` 为 Zabbix Server 端的 IP 地址。查看 SMTX OS 节点是否向 Zabbix Server 发送了 Trap 信息。如果发送了信息，输出内容应如下图所示，若未抓取到 Trap 信息，请联系研发处理。

   ![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_24.png)
3. 若 SMTX OS 节点能够正常发送 Trap 信息，请在 Zabbix 端进行抓包，并过滤出节点发出的报文。若 Zabbix 端未抓取到 SMTX OS 集群发出的报文，请检查 Zabbix 和集群之间的网络连接是否正常。
4. 若 Zabbix 可以抓取 SMTX OS 节点发出的 Trap 信息，请查看报文的 community 字段的值和 SNMP Host 配置的 community 值是否相同，若不相同，请重新设置 SNMP Host 的 community 参数，确保和 SMTX OS 中设置的 community 值相同。
5. 若 Zabbix 端能够正常收取 SMTX OS 节点发出的 Trap 报文，请执行如下操作。

   1.查看 Zabbix Server 端的 /etc/zabbix/zabbix\_server.conf 或者 /etc/zabbix/zabbix\_trap\_receiver.pl 配置文件，获取 SNMPTrapperFile 文件的路径。

   2. 执行 `tail -f /tmp/zabbix_traps.tmp` 命令，查看 SNMPTrapperFile 文件信息。其中 `/tmp/zabbix_traps.tmp` 为 SNMPTrapperFile 文件的路径，请以客户环境实际的路径代替。

      ![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_25.png)
   3. 若在 Zabbix\_traps.tmp 可以查看到 trap 信息，说明 SMTX OS 集群已经将 trap 信息发送到了 Zabbix Server。此时可以确定 Zabbix Server 的 snmptrapper 未从 SNMPTrapperFile 获取数据。请执行命令 `systemctl restart snmptrapd` 和 `systemctl restart snmptt` 命令重启 snmptrapd 和 snmptt 进程，然后重新检查 Zabbix Web 前端是否可以正常查看报警信息。
   4. 若前端仍无法查看告警信息，请检查是否由于 SMTX OS 节点和 Zabbix 跨网络，导致 SNMPTrapperFile 文件中告警信息的 IP 地址与 SNMP Host 中设置的节点 IP 地址不同。如果两个 IP 地址不同，请手动修改将 Host 中 SNMP interfaces IP 地址修改为SNMPTrapperFile 中的 IP 地址，然后再次检查是否可以查看告警信息。
6. 若以上操作仍不能解决问题，请联系研发处理。

## Q：若用户使用的是 Zabbix 7.x，如何提取 zabbix trap 报警文案？

A：请根据报警文案的语言选择对应处理方式。

> **说明**：
>
> 以下方法中提供的 javascript 脚本都是通过 [AI 平台](https://chat.deepseek.com/share/vq85sshnvr0ul8mgg8)生成的，已经尽可能的适配可能出现的 trap 消息格式。如果在实际环境中进行配置时，遇到了一些无法适配的消息格式，可以在 AI 平台中提供 trap 消息正文和原始脚本，以对脚本进行更新。获取更新后的脚本后，可以通过 zabbix 的 Test 按钮进行验证。

### snmptrapd 接收的报警为英文

报警文案示例：

```
2025-07-25T06:13:25-0400 ZBXTRAP 192.168.20.242
UDP: [192.168.20.242]:56309->[192.168.23.250]:162
DISMAN-EVENT-MIB::sysUpTimeInstance = 202:22:39:44.05
SNMPv2-MIB::snmpTrapOID.0 = SNMPv2-SMI::enterprises.42000.9999.1
SNMPv2-SMI::enterprises.42000.999 = SNMPv2-SMI::enterprises.42000.9999.1
SNMPv2-SMI::enterprises.42000.999.1 = 202:22:39:43.91
SNMPv2-SMI::enterprises.42000.999.3 = 30
SNMPv2-SMI::enterprises.42000.999.4 = "CRITICAL"
SNMPv2-SMI::enterprises.42000.999.5 = "ELF-SRE-Dev-Env-600-17.11-test"
SNMPv2-SMI::enterprises.42000.999.2 = "{854476d9-6267-45fc-927b-d46090489c3e:ELF-SRE-Dev-Env-600-17.11-test} Host node-17-11: The service process disk-healthd is not running."
SNMPv2-SMI::enterprises.42000.999.6 = "TRIGGERED"
```

#### 方法一

使用如下正则表达式从原始日志提取所需字段：

```
pattern：(?s)UDP:\s*\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\].*?\.\d+\.\d+\.4\s*=\s*"(INFO|NOTICE|WARNING|CRITICAL|ERROR)".*?\.\d+\.\d+\.2\s*=\s*"(.*?)"
```

此正则 pattern 共有 3 组通过括号内的正则表达式匹配的内容。其中：

- 动态提取 IP：从 UDP: [192.168.20.242] 中捕获 IP
- 精准匹配 OID 结构：
  - `\.\d+\.\d+\.4`：匹配告警级别字段（如 42000.999.4）
  - `\.\d+\.\d+\.2`：匹配告警消息字段（如 42000.999.2）
- 完整消息提取：`(.*?)` 确保引号内的全部内容被捕获，避免截断

在实际情况中，不同客户希望呈现的报警内容格式可能不同，此处以正则表达式输出 `SMTX-Alert level(\2), ip(\1), message(\3)` 为例，展示如何通过正则表达式设置报警内容呈现格式。 其中：

- `SMTX-Alert level(\1)`：表示使用第 2 组正则表达式过滤出报警级别；
- `ip(\3)`：表示使用第 1 组正则表达式过滤出可观测服务虚拟机的 IP 地址；
- `message(\5)`：表示使用第 3 组正则表达式过滤出报警的内容。

在上述正则表达式下，过滤出以下格式的报警内容：

`SMTX-Alert level(CRITICAL), ip(192.168.20.242), message({854476d9-6267-45fc-927b-d46090489c3e:ELF-SRE-Dev-Env-600-17.11-test} Host node-17-11: The service process disk-healthd is not running.)`

#### 方法二（推荐）

在 Preprocessing 里增加一个 javascript 脚本，内容如下：

```
/**
 * Extract and process SNMP Trap alert data
 * @param {string} trapMsg - Raw SNMP Trap message
 * @returns {object} Object containing parsed results
 */
function extractAlertData(trapMsg) {
    // Main processing logic
    try {
        // 1. Extract IP address (supports both ZBXTRAP and UDP formats)
        var ipMatch = trapMsg.match(/(?:ZBXTRAP|UDP:\s*\[)(\d+\.\d+\.\d+\.\d+)/);
        // If standard format not matched, try to find any IP in the message
        var ip = ipMatch ? ipMatch[1] : (trapMsg.match(/\d+\.\d+\.\d+\.\d+/) || ["Unknown IP"])[0];
        
        // 2. Extract alert level (match fixed OID pattern 42000.999.4)
        var levelMatch = trapMsg.match(/42000\.999\.4\s*=\s*"([^"]+)"/);
        var level = levelMatch ? levelMatch[1] : "UNKNOWN";
        
        // 3. Extract status (TRIGGERED/RESOLVED) - match fixed OID pattern 42000.999.6
        var statusMatch = trapMsg.match(/42000\.999\.6\s*=\s*"([^"]+)"/);
        var status = statusMatch ? statusMatch[1] : "UNKNOWN";
        
        // 4. Extract message content - match fixed OID pattern 42000.999.2
        var messageMatch = trapMsg.match(/42000\.999\.2\s*=\s*"([^"]+)"/);
        if (!messageMatch) throw "No valid message found";
        
        var message = messageMatch[1];
        
        // 5. Format output
        return {
            status: status,
            level: level,
            ip: ip,
            message: message,
            raw: trapMsg // Optional: keep original data
        };
        
    } catch (err) {
        return {
            error: "Processing failed: " + err,
            raw: trapMsg.length > 200 ? trapMsg.substr(0, 200) + "..." : trapMsg
        };
    }
}

// Usage example
var result = extractAlertData(value);

if (result.error) {
    return result.error;
} else {
    return 'Status[' + result.status + '], Level[' + result.level + '], IP:' + result.ip + ', Message:' + result.message;
}
```

整体 preprocessing 的配置效果截图如下：

![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_26.png)

测试结果如下：

![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_27.png)

### snmptrapd 接收的报警文案为中文

文案示例如下：

```
UDP: [192.168.20.242]:38161->[192.168.23.250]:162
DISMAN-EVENT-MIB::sysUpTimeInstance = 202:22:39:49.71
SNMPv2-MIB::snmpTrapOID.0 = SNMPv2-SMI::enterprises.42000.9999.1
SNMPv2-SMI::enterprises.42000.999 = SNMPv2-SMI::enterprises.42000.9999.1
SNMPv2-SMI::enterprises.42000.999.1 = 202:22:39:49.71
SNMPv2-SMI::enterprises.42000.999.3 = 10
SNMPv2-SMI::enterprises.42000.999.4 = "INFO"
SNMPv2-SMI::enterprises.42000.999.5 = ""
SNMPv2-SMI::enterprises.42000.999.2 = "E8 BF 99 E6 98 AF E4 B8 80 E6 9D A1 E6 B5 8B E8
AF = 95 E6 B6 88 E6 81 AF E3 80 82 E6 82 A8 E4 B8
BA = E5 8F AF E8 A7 82 E6 B5 8B E6 80 A7 E6 9C 8D
E5 = 8A A1 E8 99 9A E6 8B 9F E6 9C BA 20 28 31 39
32 = 2E 31 36 38 2E 32 30 2E 32 34 32 29 20 E9 85
8D = E7 BD AE E7 9A 84 E6 8A A5 E8 AD A6 E9 80 9A
E7 = 9F A5 20 71 69 75 70 69 6E 67 2D 74 72 61 70
2D = 66 6F 72 2D 6F 62 73 20 E5 8F AF E4 BB A5 E6
AD = A3 E7 A1 AE E5 B7 A5 E4 BD 9C E3 80 82 "
SNMPv2-SMI::enterprises.42000.999.6 = "TRIGGERED"
```

#### 方法一

使用如下正则表达式从原始日志提取所需字段：

`pattern：(?s)UDP:\s*\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\].*?\.\d+\.\d+\.4\s*=\s*"(INFO|NOTICE|WARNING|CRITICAL|ERROR)".*?\.\d+\.\d+\.2\s*=\s*"(.*?)"`

此正则 pattern 共有3组通过括号内的正则表达式匹配的内容。其中：

- 动态提取 IP：从 UDP: [192.168.20.242] 中捕获 IP
- 精准匹配 OID 结构：
  - `\.\d+\.\d+\.4`：匹配告警级别字段（如 42000.999.4）
  - `\.\d+\.\d+\.2`：匹配告警消息字段（如 42000.999.2）
- 完整消息提取：`(.*?)` 确保引号内的全部内容被捕获，避免截断。

定义输出为：`\1|\2|\3`

在 Preprocessing 里增加 javascript 脚本，内容如下：

```
function hexToChinese(hexStr) {
    // 清理 Hex 字符串（移除空格、换行、=号和引号）
    var cleanedHex = hexStr.replace(/[\s="]+/g, '');
    
    // Hex 转 UTF-8 中文字符
    var result = '';
    for (var i = 0; i < cleanedHex.length; i += 2) {
        var hexByte = cleanedHex.substr(i, 2);
        var charCode = parseInt(hexByte, 16);
        if (!isNaN(charCode)) {
            result += String.fromCharCode(charCode);
        }
    }
    
    // 处理 UTF-8 编码
    try {
        return decodeURIComponent(escape(result));
    } catch (e) {
        return result; // 解码失败时返回原始 Hex 内容
    }
}

// 主处理逻辑
try {
    // 解析输入（格式：IP|告警级别|Hex消息）
    var parts = value.split('|');
    if (parts.length < 3) {
        throw "输入格式错误，需要 IP|LEVEL|HEX_MSG 格式";
    }
    
    var ip = parts[0];
    var level = parts[1];
    var message = hexToChinese(parts[2]);
    
    // 返回格式化结果
    return 'Level[' + level + '], IP:' + ip + ', Message:' + message;
    
} catch (err) {
    return 'Error: ' + err;
}
```

整体 preprocessing 的配置效果截图如下：

![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_28.png)

测试结果如下：

![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_29.png)

#### 方法二（推荐）

在 Preprocessing 里增加一个 javascript 脚本，内容如下：

```
function hexToChinese(hexStr) {
    // 清理 Hex 字符串（移除空格、换行、=号和引号）
    var cleanedHex = hexStr.replace(/[\s="]+/g, '');
    
    // Hex 转 UTF-8 中文字符
    var result = '';
    for (var i = 0; i < cleanedHex.length; i += 2) {
        var hexByte = cleanedHex.substr(i, 2);
        var charCode = parseInt(hexByte, 16);
        if (!isNaN(charCode)) {
            result += String.fromCharCode(charCode);
        }
    }
    
    // 处理 UTF-8 编码
    try {
        return decodeURIComponent(escape(result));
    } catch (e) {
        return "[解码失败] " + result;
    }
}

// 主处理逻辑
try {
    // 原始 Trap 消息
    var trapMsg = value;
    
    // 1. 提取 IP 地址
    var ipMatch = trapMsg.match(/(?:ZBXTRAP|UDP:\s*\[)(\d+\.\d+\.\d+\.\d+)/);
    var ip = ipMatch ? ipMatch[1] : (trapMsg.match(/\d+\.\d+\.\d+\.\d+/) || ["未知IP"])[0];
    
    // 2. 提取告警级别（匹配固定 OID 模式 42000.999.4）
    var levelMatch = trapMsg.match(/42000\.999\.4\s*=\s*"([^"]+)"/);
    var level = levelMatch ? levelMatch[1] : "未知级别";
    
    // 3. 提取状态（TRIGGERED/RESOLVED）- 匹配固定 OID 模式 42000.999.6
    var statusMatch = trapMsg.match(/42000\.999\.6\s*=\s*"([^"]+)"/);
    var status = statusMatch ? statusMatch[1] : "未知状态";
    
    // 4. 提取 Hex 消息（匹配固定 OID 模式 42000.999.2）
    var hexMatch = trapMsg.match(/42000\.999\.2\s*=\s*"((?:[0-9A-F]{2}[\s=]*)+)"/i);
    if (!hexMatch || !hexMatch[1]) throw "未找到有效的 Hex 编码消息";
    
    // 5. Hex 转中文
    var message = hexToChinese(hexMatch[1]);
    
    return '状态[' + status + '], 级别[' + level + '], 来源IP:' + ip + ', 内容:' + message;
    
} catch (err) {
    return '处理失败: ' + err + '\n原始数据片段:\n' + value.substr(0, 200) + (value.length > 200 ? "..." : "");
}
```

整体 preprocessing 的配置效果截图如下：

![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_30.png)

测试结果如下：

![](https://cdn.smartx.com/internal-docs/assets/5336cc75/zabbix_31.png)

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
