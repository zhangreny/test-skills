---
title: "sks_cn/1.5.1/SMTX Kubernetes 服务微服务应用部署实践"
source_url: "https://internal-docs.smartx.com/sks_cn/1.5.1/sks_microservice/sks_microservice_preface"
sections: 11
---

# sks_cn/1.5.1/SMTX Kubernetes 服务微服务应用部署实践
## 关于本文档

# 关于本文档

本文档主要介绍了一个通过 SKS 部署微服务应用的例子。

---

## 文档更新信息

# 文档更新信息

**2025-12-12：配合 SMTX Kubernetes 服务 1.5.1 正式发布**

---

## 微服务应用说明

# 微服务应用说明

开发了一套微服务应用（图书查询管理）系统，可用于给客户进行应用的部署演示，典型的场景如下：

- 通用的应用部署演示，一套应用系统全部部署在 K8s 集群中。
- EIC 扁平网络，VM-Pod 互联互通，统一安全策略管理。将如下 rating 服务部署在虚拟机中，其他部署在容器中。具体可参考《用 Everoute 进行虚拟机-容器统一安全策略管理》培训 [PPT](https://docs.google.com/presentation/d/1nWSrRArNKJwFp6isX45pBNPoTXY7w4n4/edit?slide=id.p1#slide=id.p1) 和[录屏](https://meeting.tencent.com/login.html?redirect_link=https%3A%2F%2Fmeeting.tencent.com%2Fmeeting-record%2Fshares%3Fid%3De6b42dc9-22ad-441b-a8bd-c2d0b884376d%26hide_more_btn%3Dtrue%26from%3D3%26reload%3D1&id=e6b42dc9-22ad-441b-a8bd-c2d0b884376d&hide_more_btn=true&from=3)。

---

## 微服务应用说明 > 架构

# 架构

![](https://cdn.smartx.com/internal-docs/assets/4431a113/sks_microservice_01.png)

---

## 微服务应用说明 > 组件

# 组件

包含 6 个组件，其中 4 个组件包含业务逻辑。

## frontend

前端通过 Vue.js 开发，内置 nginx，将流量代理到 Spring Cloud GateWay 服务。

![](https://cdn.smartx.com/internal-docs/assets/4431a113/sks_microservice_02.png)

## Spring Cloud Gateway

基于 Java Spring Boot 开发，集成 Spring Cloud Gateway，为微服务提供网关。

![](https://cdn.smartx.com/internal-docs/assets/4431a113/sks_microservice_03.png)

## backend

使用 Golang 语言开发，提供图书的增删改查 RESTFul API 接口。

## rating

使用 Golang 语言开发，提供 /rating 接口实现图书的评分（通过调用 backend 服务）。

## nacos

注册中心，Spring Cloud Gateway、backend、rating 服务将调用地址注册到 nacos 中。

## mysql

nacos 使用的数据库。需要使用 ELF CSI。

---

## 部署微服务应用

# 部署微服务应用

以下服务均已经准备好了 K8s YAML 文件，可以通过 YAML 导入功能快速完成部署。

---

## 部署微服务应用 > MySQL

# MySQL

## 部署

[mysql.yaml](https://drive.google.com/open?id=1AnVFxFNSb1aOnaISW8T6Z3YEmWQDLeH1)

> **注意**：
>
> - MySQL 的参数、密码（P@s5w0rd）和 CSI Driver（默认使用 smtx-elf-csi-driver），可以根据实际情况调整。
> - 建议部署在 mysql 名字空间中。

## 初始化

通过 Pod 控制台可以快速进入到 MySQL 运行的容器，进行数据库和表的创建：

![](https://cdn.smartx.com/internal-docs/assets/4431a113/sks_microservice_04.png)

```
mysql -h 127.0.0.1 -u root -p
create database nacos;
use nacos;
```

把 [nacos-mysql.sql](https://drive.google.com/open?id=1yP_m3OUEBmfe76hjBUjgmMPr3uq3GnkK) sql 直接 copy 到终端中完成表的创建。

具体可参考[视频](https://mp.weixin.qq.com/s/n_aURtsWN6PW2N9yWgB7vQ)。

---

## 部署微服务应用 > Nacos

# Nacos

[nacos-nopodAntiAffinity.yaml](https://drive.google.com/open?id=1LjyjmpVxTpelwuoYcY0rkCrytHfnY87h)

> **注意**：
>
> - 建议部署在 nacos 名字空间下。
> - 可通过如下 ConfigMap 配置 nacos 与 mysql 的连接信息，如果 mysql 没有部署在 mysql 名字空间下，需要手动修改 mysql.host：
>
>   ![](https://cdn.smartx.com/internal-docs/assets/4431a113/sks_microservice_05.png)
> - 如果已经有了 nacos/或者 nacos 部署在其他名字空间可以直接修改应用配置，修改方式如下：
>
>   ![](https://cdn.smartx.com/internal-docs/assets/4431a113/sks_microservice_06.png)

通过 NodePort 地址打开 nacos UI：<http://172.21.222.29:31048/nacos/> （用户名/密码：nacos/nacos）

---

## 部署微服务应用 > 业务应用

# 业务应用

## 部署

可以一键完成 frontend、Spring Cloud Gateway、backend、和 rating 服务的快速导入部署。

- [bookstore-frontend.yaml](https://drive.google.com/open?id=1EtEMRem2nBmu9jufDqWxr0auvYrTb8ZJ)
- [bookstore-apigateway.yaml](https://drive.google.com/open?id=1zn2-sNwdHmMQbYWxm3FKYdia58kjpgbt)
- [bookstore-backend.yaml](https://drive.google.com/open?id=1uGCykqI-QcUGKY25ovSd_ZDf_gVk8zeE)
- [bookstore-rating.yaml](https://drive.google.com/open?id=1yUk-SCC_Y5hRzHFxbCp2oXaZ1eQVcE4c)

> **注意**：
>
> 注意 apigateway、backend以及 rating 服务的 nacos 注册地址，参考上个步骤。

## 验证

Nacos：检查服务是否注册成功。

![](https://cdn.smartx.com/internal-docs/assets/4431a113/sks_microservice_07.png)

frontend 默认使用 NodePort 进行暴露，打开前端页面进行操作。

![](https://cdn.smartx.com/internal-docs/assets/4431a113/sks_microservice_08.png)

---

## 其他 > 源代码

# 源代码

- <http://gitlab.smartx.com/dong.zhu/bookstore-apigateway>
- <http://gitlab.smartx.com/dong.zhu/bookstore-frontend>
- <http://gitlab.smartx.com/dong.zhu/bookstore-backend>
- <http://gitlab.smartx.com/dong.zhu/bookstore-rating>

---

## 版权信息

# 版权信息

版权所有 © 2025 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
