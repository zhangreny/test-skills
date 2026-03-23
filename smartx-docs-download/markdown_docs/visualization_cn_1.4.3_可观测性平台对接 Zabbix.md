---
title: "visualization_cn/1.4.3/可观测性平台对接 Zabbix"
source_url: "https://internal-docs.smartx.com/visualization_cn/1.4.3/visualization_zabbix/visualization_zabbix_preface"
sections: 20
---

# visualization_cn/1.4.3/可观测性平台对接 Zabbix
## 关于本文档

# 关于本文档

本文档介绍了如何在 Zabbix 端和 CloudTower 端进行配置，将可观测性平台纳管的所有 SmartX 集群和系统服务数据与 Zabbix 进行对接，从而实现通过 Zabbix 监控各集群或系统服务的健康状况。

---

## 文档更新信息

# 文档更新信息

**2026-02-06：配合可观测性平台 1.4.3 正式发布**

---

## 安装 Zabbix

# 安装 Zabbix

Zabbix 一般安装在集群外的虚拟机中，用以获取集群或系统服务的监控或报警信息。在实际环境中，若客户已安装了 Zabbix，可跳过此安装介绍。

Zabbix 支持在多个操作系统中安装，本文以 CentOS7-minimal 操作系统下安装 Zabbix 4.0 LTS 为例，介绍 Zabbix 的安装操作。更多操作系统下的安装可参考 [Zabbix 官方的安装指引](https://www.Zabbix.com/download)。

---

## 安装 Zabbix > 安装前准备

# 安装前准备

## 设置安装环境

在安装 Zabbix 前，请先安装 epel-release repo，以获取一些系统自带 repo 无法获取到的 rpm，并关闭 SELinux 服务和 firewalld 防火墙，避免后续无法访问 Zabbix Web 前端。

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

Zabbix Server 是 Zabbix 的核心组件，用于获取 SMTX OS 集群发出的报警信息。请按照如下操作安装 Zabbix Server，并设置 Zabbix 访问 MySQL 的用户名及密码。

1. 安装 Zabbix release repo。

   ```
   yum install -y https://repo.zabbix.com/zabbix/4.0/rhel/7/x86_64/zabbix-release-4.0-1.el7.noarch.rpm
   ```
2. 安装 Zabbix server。

   ```
   yum install -y zabbix-server-mysql
   ```
3. 设置 Zabbix 访问 MySQL 数据库的用户名。此处以用户名为 `Zabbix'@'localhost'` 举例。

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

1. 安装 Zabbix Web 前端。

   ```
   yum install -y zabbix-web-mysql
   ```
2. 设置 Zabbix Web 前端的时区。

   ```
   sed -i.bak 's/# php_value date.timezone .*$/php_value date.timezone Asia\/Hong_Kong/g' /etc/httpd/conf.d/zabbix.conf
   ```
3. 重启 httpd 服务。

   ```
   systemctl restart httpd
   ```

---

## 安装 Zabbix > 连通 MySQL 数据库

# 连通 MySQL 数据库

1. 在浏览器输入 `http://<ip>/zabbix`，打开 Zabbix Web 前端。其中 `ip` 为Zabbix 所在节点的 IP 地址。默认的登录用户名为 `Admin`，密码为 `zabbix`。
2. 在 **Welcome** 和 **Check of pre-requests** 步骤可直接单击 **Next step**，进入 **Configure DB connection** 配置，选择数据库类型为 MySQL，并输入已创建的 MySQL 数据库的用户名和密码。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_01.png)
3. 后续步骤中，可直接单击 **Next step**，完成所有配置。

---

## 监控对接

# 监控对接

可观测性平台内置有监控功能，并通过 CloudTower 提供了图形化界面对所有关联集群和系统服务进行监控管理。但在实际场景中，部分客户也会使用第三方工具对接可观测性平台进行监控，典型的第三方工具为 Zabbix。

本文介绍如何在 Zabbix 端和 CloudTower 端进行配置，将可观测性平台纳管的所有 SmartX 集群和系统服务数据与 Zabbix 进行对接，从而实现通过 Zabbix 监控各集群或系统服务的健康状况。

---

## 监控对接 > CloudTower 端配置

# CloudTower 端配置

1. 在 CloudTower **系统配置**主界面左侧的导航树选择 **SNMP 传输**，单击右上角**创建 SNMP 传输**，弹出**创建 SNMP 传输**对话框。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_02.png)
2. 设置如下参数。

   | 参数 | 说明 |
   | --- | --- |
   | 名称 | 输入用户名，建议保持和 Zabbix 中设置的 SNMP Host 名称相同。 |
   | 传输对象 | 所创建的 SNMP 传输的传输对象。支持选择已关联本版本可观测性服务的集群。 |
   | 协议 | UDP 协议。 |
   | 端口 | 161 端口。 |
   | 版本 | 选择 “v2c”。 |
   | 群组 | 输入群组名称，例如 “smartx”。请勿使用 “public” 作为群组名，否则有可能被漏扫软件扫描到高危漏洞。 |
3. 单击**创建**，完成 SNMP 传输配置。

---

## 监控对接 > Zabbix 端配置 > 从 CloudTower 拷贝 MiB 文件至 Zabbix

# 从 CloudTower 拷贝 MiB 文件至 Zabbix

MiB 文件定义了 SmartX 集群可被监控的信息。当 Zabbix 从可观测性平台接收到了监控数据后，将根据 MiB 将数据转换为可读格式。请在 CloudTower 的 **SNMP 传输**页面下载 MiB 文件，并将解压后的文件拷贝至 Zabbix。

1. 登录 CloudTower，在**系统配置**主界面左侧的导航树选择 **SNMP 传输**。进入 SNMP 传输页面，单击**下载 MiB**。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_03.png)

   > **说明**：
   >
   > 如果 SNMP 传输配置的传输对象关联了多个可观测性服务，下载的 MiB 文件为多个压缩包，命名格式为 `<可观测性服务虚拟机 IP>-MIB.zip`。在配置 Zabbix 模板时，需为每个压缩包中的模版进行配置。
2. 将 MiB 文件解压至本地，解压缩后包括 `zabbix_metric_template.xml` 和 `METRICS.mib` 文件。

---

## 监控对接 > Zabbix 端配置 > 配置 Zabbix 模板

# 配置 Zabbix 模板

从 CloudTower 下载的 MiB 文件中，包括了 Zabbix 模板文件 `zabbix_metric_template.xml`。该模板定义了当前可观测服务关联集群可获取监控数据的信息。

## 导入模板

1. 打开 Zabbix Web 前端，选择 **Configuration > Templates** 界面，单击 **Import**，进入导入模板界面。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_04.png)
2. 单击**选择文件**，在已解压至本地的 MiB 文件夹中，选择模板文件 `zabbix_metric_template.xml`，并勾选如下设置。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_05.png)
3. 单击 **Import** 导入模版。对于 6.0 LTS 和 6.4 版本的 Zabbix，在单击 **Import** 之后，将弹出模板导入预览，确认之后再次单击 **Import**，完成导入。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_06.png)

   完成导入后可在模板列表查看导入的模板。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_07.png)

## 配置模板的环境信息

1. 单击导入模板**<可观测性服务虚拟机 IP>-METRICS-MIB template** 进入模板配置界面，在 **Macros** 页签下，选择 **Template macros**，配置以下两项环境参数。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_08.png)

   | 参数 | 说明 |
   | --- | --- |
   | {$SNMP\_COMMUNITY} | 输入 Community 名称。此处需保持和 CloudTower 的 SNMP 传输配置中设置的群组名相同。请勿使用默认的 “public” 名称，否则有可能产生高危漏洞。 |
   | {$SNMP\_PORT} | 端口号设置为 “161”。 |
2. 环境参数配置完毕后，单击 **Update** 应用更新。

---

## 监控对接 > Zabbix 端配置 > 配置 SNMP Host

# 配置 SNMP Host

当 Zabbix 对接可观测性平台时，需创建 SNMP Host，一个 SNMP Host 对应一个可观测性服务。若要对接多个可观测性服务的监控数据，请创建多个 SNMP Host。

1. 在浏览器输入 `http://<ip>/zabbix`，打开 Zabbix 的 Web 前端，其中 `ip` 为 Zabbix 所在节点的 IP 地址。输入 Zabbix Web 前端的用户名和密码，默认的用户名和密码分别为 `Admin` 和 `zabbix`。
2. 进入 **Configuration > Hosts** 界面，单击 **Create host**，弹出配置页面，配置如下参数：

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_09.png)

   | 参数 | 说明 |
   | --- | --- |
   | Host name | 输入 SNMP Host 的名称，可任意填写。 |
   | Templates | 选择已导入的可观测性服务的模板。 例如需要对接 IP 地址为 192.168.20.236 的可观测性服务时，请选择对应的模版。 |
   | Groups | 选择 Host 所在的 Group，此处选择 “SMTX Observability”。 |
   | Interface | - 输入可观测性服务虚拟机的 IP 地址。若 Zabbix 与可观测性服务虚拟机跨网关，请同时添加网关 IP 地址。端口设置为 161。 - 选择 SNMP 类型。建议选择 SNMP version 为 SNMPv2，Zabbix 对于 v3 版本的传输支持能力不稳定。 |
3. （可选）如果客户直接使用 Zabbix Server 接收监控信息可跳过此步骤，当客户需要通过 Zabbix Proxy 接收监控信息时，可在 **Hosts** 配置页面的 **Monitored by proxy** 下拉框选择对应的 Zabbix Proxy 完成配置，如下图所示。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_10.png)
4. 单击 **Add**，完成创建。

---

## 监控对接 > 验证传输对接结果

# 验证传输对接结果

完成 Zabbix 端和 CloudTower 端的配置后，请参考以下方法验证 Zabbix 和可观测性平台的监控系统是否对接成功。

1. 登录 Zabbix Web 前端，在 **Configuration > Hosts** 界面，单击已创建的 SNMP Host，在 **Discovery rules** 界面选中所有 rules，单击 **Exexcute now**，手动触发规则执行和监控数据获取。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_11.png)
2. 打开 **Monitoring > Latest data**，选择监控的 Host，单击 **Apply**，查看是否有数据，若 **Last Value** 列有数据，则表示 Zabbix 已能够获取监控数据， Zabbix 已对接到了可观测性平台。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_12.png)

---

## 监控对接 > 常见问题

# 常见问题

当可观测性服务关联的集群发生更新时，Zabbix 端可能较长时间无法自动获取新关联集群的数据。此时可以在 **Configuration > Hosts** 界面，单击已创建的 SNMP Host，在 **Discovery rules** 界面手动触发更新。如果等待 5 分钟后仍没有获取到数据，可以尝试重新导入模板文件，并在配置 SNMP Host 时选择相应模板文件，然后手动触发执行规则。

---

## 报警对接 > Zabbix 端配置 > 配置 Zabbix Server

# 配置 Zabbix Server

## 启用 SNMP Trapper

1. 启用 Zabbix 端 SNMP Trapper 以接收 trap 信息，并设置接收 trap 信息的 SNMPTrapperFile 文件。

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

snmptrapd 用于 Zabbix 接收 trap 信息，请执行以下命令安装并启用 snmptrapd 服务。

1. 安装 snmptrapd 软件。

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

snmptt（SNMP Trap Translator ) 用于将接收的原始报警信息（trap 消息）进行格式化输出，使原始的报警内容更易于阅读。若客户的实际环境中未安装 snmptt，建议参考[格式化报警内容](/visualization_cn/1.4.3/visualization_zabbix/visualization_zabbix_16)，对报警信息进行正则化。

1. 安装 snmptt。

   ```
   yum install -y snmptt perl-Sys-Syslog
   ```
2. 设置 snmptt 的时间输出格式。

   ```
   sed -i.bak 's/#date_time_format =/date_time_format = %H:%M:%S %Y\/%m\/%d/g' /etc/snmp/snmptt.ini
   ```
3. 设置 snmptt 的 trap 消息过滤关键字和格式。

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

## 报警对接 > Zabbix 端配置 > 配置 SNMP Host 和 SNMP Item > 创建 SNMP Host

# 创建 SNMP Host

当 Zabbix 对接可观测性平台时，需创建 SNMP Host，一个 SNMP Host 对应一个可观测性服务。若要对接多个可观测性服务的报警数据，请创建多个 SNMP Host。

1. 在浏览器输入 `http://<ip>/zabbix`，打开 Zabbix 的 Web 前端，其中 `ip` 为 Zabbix 所在节点的 IP 地址。输入 Zabbix Web 前端的用户名和密码，默认的用户名和密码分别为 `Admin` 和 `zabbix`。
2. 进入 **Configuration > Hosts** 界面，单击 **Create host**，弹出配置页面，配置如下参数：

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_13.png)

   | 参数 | 说明 |
   | --- | --- |
   | Host name | 输入 SNMP Host 的名称，可任意填写。 |
   | Templates | - |
   | Groups | 选择 Host 所在的 Group，此处选择 “SMTX Observability”。 |
   | Interface | - 输入可观测性服务虚拟机的 IP 地址。若 Zabbix 与可观测性服务虚拟机跨网关，请同时添加网关 IP 地址。端口设置为 161。 - 选择 SNMP 类型。建议选择 SNMP version 为 SNMPv2，Zabbix 对于 v3 版本的传输支持能力不稳定。 |
3. （可选）如果客户直接使用 Zabbix Server 接收监控信息可跳过此步骤，当客户需要通过 Zabbix Proxy 接收监控信息时，可在 **Hosts** 配置页面的 **Monitored by proxy** 下拉框选择对应的 Zabbix Proxy 完成配置，如下图所示。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_14.png)
4. 单击 **Add**，完成创建。

---

## 报警对接 > Zabbix 端配置 > 配置 SNMP Host 和 SNMP Item > 创建 SNMP Item

# 创建 SNMP Item

1. 单击已创建的 SNMP Host，选择 Items 配置。单击 **Create item**，弹出 Item 配置界面。
2. 在 **Item** 配置界面，配置如下参数。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_15.png)

   | 参数 | 说明 |
   | --- | --- |
   | Name | 输入Item 的名称。 |
   | Type | 选择 Item 类型为 “SNMP trap”。 |
   | Host Interface | 选择 Item 类型后自动填充。 |
   | Type of information | 选择 “Log”。 |
   | Log time format | 输入 Log 的时间格式。例如：`hh:mm:ss yyyy/MM/dd`。 |
3. 单击 **Add**，完成 SNMP Item 创建。
4. （可选）解析中文报警文案。

   由于中文字符在 SNMP TRAP 消息中以 16 进制字符的形式传输，且 Zabbix 默认没有中文解析，因此若报警对接时语言选择中文，则在zabbix 页面将呈现16 进制字符的报警信息 ，不利于用户阅读。

   当客户环境已安装 snmptt 时，您可通过如下步骤增加中文字符处理。配置后，报警文案将自动被解析为中文字符进行展示。若未安装 snmptt，请参考[中文报警对接](/visualization_cn/1.4.3/visualization_zabbix/visualization_zabbix_16#%E4%B8%AD%E6%96%87%E6%8A%A5%E8%AD%A6%E5%AF%B9%E6%8E%A5)中的步骤进行操作以进行中文解析。

   > **注意**：
   >
   > 仅 4.2 及以上版本的 Zabbix 支持自定义 JavaScript 的 item preprocessing，在配置解析中文报警文案之前，请确认您安装的 Zabbix 的版本满足要求。

   1. 在 **Create item** 界面，单击 **PreProcessing**，进入配置界面。

      ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_16.png)
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

      | 参数 | 说明 |
      | --- | --- |
      | Value | 输入测试示例，可分别输入中文示例和英文示例以分别测试中英文解析是否有效。 - 中文示例：`15:55:11 2023/12/26 .1.3.6.1.4.1.42000.9999.28 "SMTXOS-Alert" UNKNOWN - ZBXTRAP 172.20.221.135 [TRIGGERED:CRITICAL] E4 B8 BB E6 9C BA 20 73 63 61 6C 65 2D 31 20 E7 9A 84 E6 9C 8D E5 8A A1 E8 BF 9B E7 A8 8B 20 65 6C 66 2D 64 68 63 70 20 E6 9C AA E8 BF 90 E8 A1 8C E3 80 82` - 英文示例：`03:37:31 2023/12/24 .1.3.6.1.4.1.42000.9999.34 "SMTXOS-Alert" UNKNOWN - ZBXTRAP 172.20.221.135 [RESOLVED:CRITICAL] The storage network 5-minute P90 ping response time is greater than 5ms between the two hosts: scale-1 and juan-li-smtxos-6-0-0-b121X20231214113913X1.` |
      | Time | - |
      | Previous value | - |
      | Previous time | - |
      | End of line sequence | 选择 **LF** |
      | Preprocessing steps | 在 Result 字段下输出解析结果 |
   4. 当中英文解析分别输出如下结果时，表明配置成功。

      中文解析结果：

      ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_17.png)

      英文解析结果：

      ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_18.png)

---

## 报警对接 > Zabbix 端配置 > 配置 SNMP Host 和 SNMP Item > 格式化报警内容（未安装 snmptt）

# 格式化报警内容（未安装 snmptt）

> **说明**：
>
> 若客户环境未安装 snmptt，或者使用了 Perl 将 Trap 消息写入 SNMPTrapperFile。为使接收的 Trap 消息更易于阅读，请参考本节内容对 Trap 信息进行格式化。若客户已安装 snmptt ，可跳过此步骤。

## 英文报警对接

当报警内容为英文时，请参考如下步骤进行格式化。

在 **Create item** 界面，单击 **PreProcessing**，然后添加正则表达式来提取报警内容。

![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_19.png)

添加的正则表达式与 snmptrapd 服务的日志输出格式有关，需要根据具体输出的日志调整匹配使用的正则表达式，以如下日志为例。

```
2023-12-01 16:39:05 <UNKNOWN> [UDP: [192.168.29.131]:60858->[192.168.27.106]:162]:
.1.3.6.1.2.1.1.3.0 = Timeticks: (1701419918) 196 days, 22:09:59.18        .1.3.6.1.6.3.1.1.4.1.0 = OID: .1.3.6.1.4.1.42000.9999.34        .1.3.6.1.4.1.42000.999 = OID: .1.3.6.1.4.1.42000.9999.34        .1.3.6.1.4.1.42000.999.1 = Timeticks: (1701419917) 196 days, 22:09:59.17        .1.3.6.1.4.1.42000.999.3 = INTEGER: 30        .1.3.6.1.4.1.42000.999.4 = STRING: "CRITICAL"        .1.3.6.1.4.1.42000.999.5 = IpAddress: 192.168.29.131        .1.3.6.1.4.1.42000.999.2 = STRING: "The storage network 5-minute P90 ping response time is greater than 5ms between the two hosts: yingjie-511X20230809114256X1 and yingjie-511X20230809114256X3."        .1.3.6.1.4.1.42000.999.6 = STRING: "TRIGGERED"
```

使用如下正则表达式从原始日志提取所需字段：

pattern： `\"(.*)\"([\s\S]*?)(\d+\.\d+\.\d+\.\d+)([\s\S]*?)\"(.*)\"`

此正则 pattern 共有五组通过括号内的正则表达式匹配的内容。其中：

- 第 1 组： `\"(.*)\"`用于匹配 `""`内表示报警级别的任意字符串，如 CRITICAL；
- 第 2 组： `([\s\S]*?)` 用于匹配包括换行在内的任意字符；
- 第 3 组： `(\d+\.\d+\.\d+\.\d+)` 用于匹配可观测服务虚拟机的 IP 地址；
- 第 4 组： `([\s\S]*?)` 同第 2 组，用于匹配包括换行在内的任意字符；
- 第 5 组： `\"(.*)\"` 用于匹配报警文案。

在实际情况中，不同客户希望呈现的报警内容格式可能不同，此处以正则表达式输出 `SMTX-Alert level(\1), ip(\3), message(\5) 为例`，展示如何通过正则表达式设置报警内容呈现格式。
其中：

- `SMTX-Alert level(\1)` 表示使用第 1 组正则表达式过滤出报警级别；
- `ip(\3)` 表示使用第 3 组正则表达式过滤出可观测服务虚拟机的 IP 地址；
- `message(\5)` 表示使用第 5 组正则表达式过滤出报警的内容。

在上述正则表达式下，过滤出以下格式的报警内容：SMTX-Alert level(CRITICAL), ip(192.168.x.x), message(The cluster is recovering data.)，即过滤出 IP 地址为 192.168.x.x 的集群内，报警级别为 CRITICAL ，报警内容为 “The cluster is recovering data.” 的报警信息。

## 中文报警对接

由于 snmptrapd 的日志内中文是 16 进制字符串，因此当报警信息中包括中文字符时，需要根据实际输出格式调整匹配使用的正则表达式，并增加脚本转义匹配到的报警相关字段。

1. 添加正则表达式

   以如下格式的 snmptrapd 日志输出为例：

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

   此时正则 `\"(.*)\"([\s\S]*?)(\d+\.\d+\.\d+\.\d+)([\s\S]*?)\"(.*)\"` 匹配到的五组内容分别为：

   - 第 1 组 `\"(.*)\"` 报警级别 CRITICAL；
   - 第 2 组 `([\s\S]*?)` 用于匹配包括换行在内的任意字符；
   - 第 3 组 `(\d+\.\d+\.\d+\.\d+)` 用于匹配可观测服务虚拟机的 IP 地址 10.111.130.81；
   - 第 4 组 `([\s\S]*?)` 同第 2 组，用于匹配包括换行在内的任意字符，此时匹配到的内容为从 ip地址下一行开始，”TRIGGERED” 之前的所有内容；
   - 第 5 组 `\"(.*)\"` 报警状态 TRIGGERED。
2. 配置中文转义

   当客户现场的 snmptrapd 实际输出格式与文档不同时可以组合使用各字段。获取各字段内容后需要通过脚本转义中文文案。

   在 **Create item** 界面，单击 **PreProcessing**，正则匹配之后添加 **JavaScript** 脚本，用于转义 16 进制报警文案，内容如下：

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_20.png)

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
   str = p + decodeURIComponent(escape(str)) + ")\n";
   return str
   }
   return hex2a(value);
   ```

---

## 报警对接 > CloudTower 端配置

# CloudTower 端配置

1. 登录 CloudTower，在**报警**主界面左侧的导航树选择**通知配置**，单击右上角 **+ 创建通知配置**，选择**创建 SNMP 陷阱配置**。
2. 在弹出的**创建 SNMP 陷阱配置**界面，设置如下参数。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_21.png)

   | 参数 | 说明 |
   | --- | --- |
   | 报警源 | 选择可观测性服务。 |
   | 名称 | 输入用户名，可任意填写。 |
   | 报警对象 | 勾选需要接收报警信息的报警对象。 |
   | 远端 IP | 输入 Zabbix Server 所在节点的 IP 地址。若用户配置了 Zabbix Proxy，则填写 Zabbix Proxy 所在节点的 IP 地址。 |
   | 端口 | 输入“162” 。 |
   | 团体名 | 指定用于访问远程 SNMP 管理器的团体名。 |
   | 报警等级 | 勾选需要接收的报警等级。 |
   | 启用配置 | 开启启用配置开关。 |
3. 单击**发送测试消息**按钮可向配置的远端 Zabbix 发送测试 Trap 消息。
4. 访问 Zabbix Web 前端，在 **Monitoring > Latest data** 页面，选择对应的 Host，点击 **History** 查看是否出现了测试消息，如果出现对应消息，说明配置成功。

   ![](https://cdn.smartx.com/internal-docs/assets/eb26b672/zabbix_22.png)
5. 单击**创建**，完成 SNMP 陷阱创建。

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
