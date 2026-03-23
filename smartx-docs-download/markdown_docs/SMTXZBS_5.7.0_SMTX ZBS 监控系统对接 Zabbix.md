---
title: "SMTXZBS/5.7.0/SMTX ZBS 监控系统对接 Zabbix"
source_url: "https://internal-docs.smartx.com/smtxzbs/5.7.0/zabbix_monitoring/zabbix_monitoring_preface"
sections: 14
---

# SMTXZBS/5.7.0/SMTX ZBS 监控系统对接 Zabbix
## 关于本文档

# 关于本文档

SMTX ZBS 内置有监控功能，并提供了图形化界面对集群进行监控管理。但在实际场景中，部分客户也会使用第三方工具对集群进行监控，典型的第三方工具为 Zabbix。

本文档介绍了如何在 Zabbix 端和 SMTX ZBS 端进行配置，将 SMTX ZBS 的监控系统与 Zabbix 进行对接，从而实现通过 Zabbix 监控 SMTX ZBS 集群的健康状况。

阅读本文档需了解 SMTX ZBS 分布式存储软件，了解软件定义存储、分布式存储等相关技术背景知识，并具备丰富的数据中心操作经验。

---

## 文档更新信息

# 文档更新信息

**2025-12-01：配合 SMTX ZBS 5.7.0 正式发布**

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

Zabbix 从 SMTX ZBS 集群获取的监控数据需要存储到数据库中。Zabbix 官方支持的数据库有 MySQL 和 PostgreSQL，本文以 MySQL 5.7 版本为例, 介绍数据库的安装方法。

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

Zabbix Server 是 Zabbix 的核心组件，用于获取 SMTX ZBS 集群发出的监控信息。请按照如下操作安装 Zabbix Server，并设置 Zabbix 访问 MySQL 的用户名及密码。

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

**操作步骤**

1. 在浏览器输入 `http://<ip>/zabbix`，打开 Zabbix Web 前端。其中 `ip` 为Zabbix 所在节点的 IP 地址。默认的登录用户名为 Admin，密码为 zabbix。
2. 在 **Welcome** 和 **Check of pre-requests** 步骤直接单击 **Next step**，进入 **Configure DB connection** 配置，选择数据库类型为 MySQL，并输入已创建的 MySQL 数据库的用户名和密码。

   ![](https://cdn.smartx.com/internal-docs/assets/3f778d33/zabbix_01.png)
3. 后续步骤中，可直接单击 **Next step**，完成所有配置。

---

## 配置 Zabbix

# 配置 Zabbix

请参考如下步骤配置 Zabbix。

---

## 配置 Zabbix > 从 SMTX ZBS 下载 MiB 文件并拷贝至 Zabbix

# 从 SMTX ZBS 下载 MiB 文件并拷贝至 Zabbix

MiB 文件定义了 SMTX ZBS 集群可被监控的信息。当 Zabbix 从 SMTX ZBS 集群接收到了监控数据后，将使用 MiB 将数据转换为可读格式。请从 SMTX ZBS 下载 MiB 文件，并将解压后的文件拷贝至 Zabbix。

**操作步骤**

1. 登录 CloudTower，进入 SMTX ZBS 集群的**设置** > **SNMP 传输**界面，单击**下载 MiB**。

   ![](https://cdn.smartx.com/internal-docs/assets/3f778d33/zabbix_02.png)
2. 将 MiB 文件解压至本地。解压后文件包括：**METRICS-MIB.mib**、**SNMP-TRAP.mib** 和 **zabbix\_metric\_template.xml**。
3. 将解压出来的 **METRICS-MIB.mib** 文件拷贝至 Zabbix Server 后台的 `/usr/share/snmp/mibs/` 目录下。

   ```
   # ls -al /usr/share/snmp/mibs/METRICS-MIB.mib
   -rwxr--r--. 1 root root 370712 Mar 23 00:11 /usr/share/snmp/mibs/METRICS-MIB.mib
   ```
4. 重启 Zabbix-server 以读取 MiB 文件。

   ```
   # systemctl restart zabbix-server
   ```

---

## 配置 Zabbix > 配置 Zabbix 模板

# 配置 Zabbix 模板

从 SMTX ZBS 中下载的 MiB 文件中，包含了 Zabbix 模板文件 **zabbix\_smtx\_template.xml** 或者 **zabbix\_metric\_template.xml**。该模板定义了所有 Zabbix 可监控的 SMTX ZBS 集群的信息。

## 导入模板

**操作步骤**

1. 打开 Zabbix Web 前端，选择 **Configuration** > **Templates** 界面，单击 **Import** ，进入导入模板界面。

   ![](https://cdn.smartx.com/internal-docs/assets/3f778d33/zabbix_03.png)
2. 单击 **Select**，在已解压至本地的 MiB 文件夹中，选择模板文件 **zabbix\_smtx\_template.xml** 或者 **zabbix\_metric\_template.xml**，并勾选如下设置。

   ![](https://cdn.smartx.com/internal-docs/assets/3f778d33/zabbix_04.png)
3. 单击 **Import**，完成导入后可在模板列表查看到导入的模板。

## 配置模板的环境信息

**操作步骤**

1. 单击导入的模板 **SMTX OS Monitoring Template V1.1** 进入模板配置界面， 在 **Macros** 页签下，选择 **Template macros**，配置以下两项环境参数。

   ![](https://cdn.smartx.com/internal-docs/assets/3f778d33/zabbix_06.png)

   | 参数 | 描述 |
   | --- | --- |
   | {$SNMP\_V2\_COMMUNITY} | 输入 Community 名称。此处需保持和 SMTX ZBS 中设置的群组名相同。请勿使用默认的 “public” 名称，否则有可能产生高危漏洞。 |
   | {$SNMP\_V2\_PORT} | 端口号设置为 “161”。 |
2. 环境参数配置完毕后，单击 **Update**。

---

## 配置 Zabbix > 配置 SNMP Host

# 配置 SNMP Host

请参考如下步骤配置 SNMP Host。

## 创建 SNMP Host

当 Zabbix 对接 SMTX ZBS 监控系统时，需创建 SNMP Host。一个 SNMP Host 对应一个被 Zabbix 监控的 SMTX ZBS 集群。若需要监控多个集群，请创建多个 SNMP Host。

**操作步骤**

1. 在浏览器输入 `http://<ip>/zabbix`，打开 Zabbix 的 Web 前端，其中 `ip` 为 Zabbix 所在节点的 IP 地址。输入 Zabbix Web 前端的用户名和密码，默认的用户名和密码分别为 Admin 和 zabbix。
2. 进入 **Configuration** > **Hosts** > **Hosts** 界面 ，单击 **Create host**，弹出配置界面，并配置如下参数：

   ![](https://cdn.smartx.com/internal-docs/assets/3f778d33/zabbix_07.png)

   | 参数 | 描述 |
   | --- | --- |
   | Host name | 输入 SNMP Host 的名称，可任意填写。 |
   | Groups | 选择 Host 所在的 Group，此处选择 “SMTX OS”。 |
   | SNMP Interface | 根据以下规则输入 IP 地址，并将端口设置为 `161`： - 若集群已关联可观测性服务，则输入可观测性服务的 IP 地址。 - 若集群未关联可观测性服务，则：   - 若集群已配置 VIP，则输入集群的 VIP 地址。   - 若集群未配置 VIP，则输入主节点的管理 IP。若 Zabbix 与 SMTX ZBS 节点跨网关，请同时添加网关 IP 地址。 |
3. （可选）若客户直接使用 Zabbix Server 接受监控信息则可跳过此步骤。当客户需要通过 Zabbix Proxy 接收集群发送的监控信息时，则可在 **Host** 页面的 **Monitored by proxy** 下拉框选择对应的 Zabbix Proxy 完成配置，如下图所示。

   ![](https://cdn.smartx.com/internal-docs/assets/3f778d33/zabbix_08.png)

## 将 SNMP Host 和模板关联

1. 在 **Configuration** > **Hosts** 界面，单击需要对接的 Host，进入 **Templates** 界面，单击 **Select**，选择上一步已导入的模板，单击 **Add**，并单击 **Update**，完成模板的关联。

   ![](https://cdn.smartx.com/internal-docs/assets/3f778d33/zabbix_09.png)
2. 完成模板关联后，返回 **Configuration** > **Hosts** 界面。若 Templates 列可显示已导入的模板 **SMTX OS Monitoring Template V1.1**，则表示关联已成功。

   ![](https://cdn.smartx.com/internal-docs/assets/3f778d33/zabbix_10.png)

---

## 在 SMTX ZBS 集群配置 SNMP 传输

# 在 SMTX ZBS 集群配置 SNMP 传输

请参考如下步骤配置 SNMP 传输。

**操作步骤**

1. 登录 CloudTower，在集群的管理界面，选择**设置** > **SNMP 配置**，在 **SNMP 传输**页签下，单击**创建传输**。
2. 在弹出的**创建 SNMP 传输**界面，设置如下参数。

   | 参数 | 描述 |
   | --- | --- |
   | 名称 | 输入用户名，需保持和 Zabbix 中设置的 SNMP Host 名称相同。 |
   | 协议 | UDP 协议。 |
   | 端口 | 161 端口。 |
   | 版本 | 选择 “v2c”。 |
   | 群组 | 输入群组名称，例如 “smartx”。请勿使用 “public” 作为群组名，否则有可能产生高危漏洞。 |
3. 单击**创建**，完成 SNMP 传输设置。

---

## 验证对接是否成功

# 验证对接是否成功

完成 Zabbix 端和 SMTX ZBS 端的配置后，请参考以下方法验证 Zabbix 和 SMTX ZBS 的监控系统是否对接成功。

**操作步骤**

1. 登录 Zabbix Web 前端，在 **Configuration** > **Hosts** 界面， 单击已添加的 SNMP Host，在 **Discovery rules** 界面选中所有 rules，单击 **Check now**，手动获取监控数据。

   ![](https://cdn.smartx.com/internal-docs/assets/3f778d33/zabbix_11.png)
2. 打开 **Monitoring** > **Latest data**，选择监控的 **Host**，单击 **Apply**，查看是否有数据。

   ![](https://cdn.smartx.com/internal-docs/assets/3f778d33/zabbix_12.png)
3. 若主机监控项的 **Last Value** 有数值，即表示 Zabbix 已能够获取监控数据，成功对接到了 SMTX ZBS 监控系统。

   ![](https://cdn.smartx.com/internal-docs/assets/3f778d33/zabbix_13.png)

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
