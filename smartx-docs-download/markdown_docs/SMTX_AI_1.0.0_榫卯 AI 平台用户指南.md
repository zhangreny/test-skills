---
title: "SMTX_AI/1.0.0/榫卯 AI 平台用户指南"
source_url: "https://internal-docs.smartx.com/smtx-ai/1.0.0/user_guide/overview/preface-generic"
sections: 44
---

# SMTX_AI/1.0.0/榫卯 AI 平台用户指南
## 关于本文档

# 关于本文档

本文档介绍了榫卯 AI 平台（简称 AI 平台）的安装部署和配置使用的详细内容。

阅读本文档需了解 AI、Kubernetes 等相关概念，了解虚拟化、容器、模型、推理等相关技术，并具备数据中心操作的丰富经验。

---

## 文档更新信息

# 文档更新信息

- **2026-02-26：新增“升级静态节点集群版本”小节**
- **2026-02-09：新增“手动导入模型文件至模型仓库”小节**
- **2026-02-03：新增配置 OpenShift 兼容性小节**
- **2026-01-30：配合榫卯 AI 平台 1.0.0 正式发布**

---

## 文档概述

# 文档概述

为帮助您全面了解榫卯 AI 平台的核心概念、使用方法及最佳实践，请您参照如下章节指引阅读相关章节。

1. 如需快速体验平台功能，[功能体验](/smtx-ai/1.0.0/user_guide/getting-started/quick-start-overview)章节将指导您在单节点上以最快速度部署简化版 AI 平台，并创建第一个 AI 负载进行体验。
2. 如需了解完整部署细节，包括生产级别部署和更多部署选项，请参考[部署 AI 平台](/smtx-ai/1.0.0/user_guide/getting-started/deploy-overview)完成完整的 AI 平台部署。
3. 完成安装部署后，完成基础设施建设：

   1. [创建容器镜像仓库](/smtx-ai/1.0.0/user_guide/infrastructure/image-registry#%E5%88%9B%E5%BB%BA%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F%E4%BB%93%E5%BA%93)为集群部署提供所需的容器镜像。
   2. 集群节点无法访问 Docker Hub 或访问速度慢时，可以[手动导入镜像](/smtx-ai/1.0.0/user_guide/infrastructure/image-registry#%E6%89%8B%E5%8A%A8%E5%AF%BC%E5%85%A5%E9%95%9C%E5%83%8F)。
   3. [创建集群](/smtx-ai/1.0.0/user_guide/infrastructure/cluster-overview)。
4. 完成基础设施建设后，进行模型和推理相关资源的管理：

   1. [创建模型仓库](/smtx-ai/1.0.0/user_guide/model-service/model-registry#%E5%88%9B%E5%BB%BA%E6%A8%A1%E5%9E%8B%E4%BB%93%E5%BA%93)用于存放模型。
   2. 使用命令行工具[管理模型仓库中的模型](/smtx-ai/1.0.0/user_guide/model-service/model-management)。
   3. 平台提供[模型目录](/smtx-ai/1.0.0/user_guide/model-service/model-catalog)，可在创建推理实例时选择合适的模型目录简化配置过程。
   4. [创建推理实例](/smtx-ai/1.0.0/user_guide/model-service/endpoint#%E5%88%9B%E5%BB%BA%E6%8E%A8%E7%90%86%E5%AE%9E%E4%BE%8B)，平台将从所选择的模型仓库加载具体的模型供[推理引擎](/smtx-ai/1.0.0/user_guide/model-service/engine)使用。
5. 通过阅读[访问控制](/smtx-ai/1.0.0/user_guide/access-control/concepts)章节，了解如何实现用户管理、权限控制，如何通过工作空间策略实现多租户隔离，以及如何从外部通过 API 密钥集成 AI 平台。
6. 平台还提供了一系列的辅助工具和配置功能，如[自定义平台外观](/smtx-ai/1.0.0/user_guide/setting/oem-config)、[导入 YAML](/smtx-ai/1.0.0/user_guide/yaml/yaml-import)、[导出 YAML](/smtx-ai/1.0.0/user_guide/yaml/yaml-export) 等，帮助您简化管理和运维工作，实现个性化配置。
7. 针对 AI 平台使用中遇到的常见问题，请阅读[常见问题处理](/smtx-ai/1.0.0/user_guide/faq/hf-download-hangs)了解详细的解决方案。

---

## 产品介绍

# 产品介绍

榫卯 AI 平台（简称“AI 平台”）基于开源软件 Neutree 开发，是一款面向企业级用户的大模型基础设施管理平台，旨在帮助企业在本地环境中安全、高效地管理异构算力资源，快速部署和优化推理服务，加速生成式 AI 应用在各行业的落地与创新。

AI 平台采用灵活兼容的架构，支持多种运行环境与加速器类型，集成模型管理、算力调度、推理服务及权限治理等核心能力，有效提升 AI 基础设施的使用效率与稳定性，降低资源管理复杂度，强化数据与模型的可控性与安全性。

![功能架构图](https://cdn.smartx.com/internal-docs/assets/d96ef1b4/user_guide_product.png)

AI 平台为您提供如下特性：

- **统一、高效的算力资源池**

  - 支持多种算力运行环境，如虚拟机、服务器和 Kubernetes 集群。
  - 支持将来自不同厂商（如 NVIDIA、昇腾等）的加速器统一纳入 AI 平台管理，实现资源统一调度。多模型实例可共享同一个加速器，通过智能分片与隔离技术，有效避免算力浪费，提升总体吞吐。
- **便捷、全面的模型管理**

  - 支持 Text-generation、Text-embedding、Text-rerank 等主流模型类型，满足丰富的企业级应用场景。
  - 可从 Hugging Face 一键拉取开源模型，也支持上传自定义模型，便于企业使用自研或第三方模型。
  - 通过模型目录功能，预设推理引擎、资源规格与运行参数，实现模型部署标准化，降低运维成本。
- **灵活且高性能的推理服务**

  - 支持多副本部署与高可用保障：推理服务支持配置多个副本实例，实现负载均衡和故障自动切换，确保服务高可用性。当某个副本实例出现故障时，AI 平台会自动将流量转移到健康的副本，保证业务连续性。
  - AI 平台基于 KVCache 感知的多副本负载均衡机制，智能优化推理请求路由，有效提升 KVCache 命中率，从而显著提升大模型预填推理性能与响应效率，满足高并发业务场景需求。
- **完善的租户与权限管理**

  - 每个租户拥有独立的资源与模型空间，确保业务之间互不干扰，数据安全可控。
  - 支持按角色定义访问权限，覆盖模型管理、推理调用、资源调度等多个维度，便于统一治理。
  - 提供 Token 使用量统计，帮助 AI 平台实现访问限流、成本控制与可计费能力。

---

## 功能体验

# 功能体验

本章节提供单节点 Docker 部署方案，帮助您快速体验 AI 平台的核心功能，适用于概念验证和功能测试环境。

如您需要在生产环境部署或了解更多部署选项，请参考[部署 AI 平台](/smtx-ai/1.0.0/user_guide/getting-started/deploy-overview)章节。

---

## 功能体验 > 部署要求

# 部署要求

AI 平台可以在虚拟机或物理服务器环境中通过 Docker 快速部署。为了确保平台能够正常运行并获得良好的体验，请确保虚拟机或者服务器的 CPU 架构和操作系统版本满足《榫卯 AI 平台发布说明》中[版本兼容说明](/smtx-ai/1.0.0/release_notes/compatibility)中的要求，并确保资源与网络端口配置满足以下要求。

- **资源配置**

  - CPU: 8 核 vCPU
  - 内存: 16 GiB
  - 存储: 600 GiB
- **网络配置**

  服务器或虚拟机能够访问 Docker Hub 和 Hugging Face 等外部资源。
- **防火墙端口**

  - 确保用于部署控制平面的服务器或虚拟机的 3000 端口开放。
  - 确保用于部署监控组件的服务器或虚拟机的 3030 端口开放。

---

## 功能体验 > 快速部署

# 快速部署

## 配置操作系统

请参考本节内容，在待部署的虚拟机或物理服务器中完成系统配置，并安装 Docker 作为容器运行时。

### 系统配置

RHEL/Rocky Linux/openEulerUbuntu

1. 配置静态 IP 地址：

   ```
   sudo vi /etc/sysconfig/network-scripts/ifcfg-<interface>
   ```

   `<interface>` 需替换为网口名称，例如 `eth0`。
2. 配置 DNS 服务器：

   ```
   sudo vi /etc/resolv.conf
   ```
3. 关闭防火墙：

   ```
   sudo systemctl stop firewalld && sudo systemctl disable firewalld
   ```
4. 关闭 SELinux：

   ```
   echo -e "SELINUX=disabled\nSELINUXTYPE=targeted" | sudo tee /etc/selinux/config
   sudo setenforce 0
   ```
5. 安装依赖软件：

   ```
   sudo dnf install rsync pciutils -y
   ```

1. 配置静态 IP 地址和 DNS 服务器：

   ```
   sudo vi /etc/netplan/50-cloud-init.yaml
   ```
2. 应用上述网络配置：

   ```
   sudo netplan apply
   ```
3. 关闭防火墙：

   ```
   sudo ufw disable
   ```
4. 可选项，按需关闭 AppArmor：

   ```
   sudo systemctl disable apparmor && sudo systemctl stop apparmor
   ```
5. 安装依赖软件：

   ```
   sudo apt-get update && sudo apt-get install rsync pciutils -y
   ```
6. 重启操作系统使配置生效：

   ```
   sudo reboot
   ```

### 安装 Docker

RHEL/Rocky LinuxopenEulerUbuntu

1. 安装 Docker CE：

   ```
   sudo dnf -y install dnf-plugins-core
   sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
   sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
2. 启动 Docker 服务：

   ```
   sudo systemctl enable --now docker
   ```
3. 确认 Docker 已成功安装：

   ```
   docker --version
   ```
4. 重启操作系统使配置生效：

   ```
   sudo reboot
   ```

1. 配置基础环境与仓库：

   ```
   dnf -y install dnf-plugins-core
   dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
   ```
2. 指定系统版本号：

   ```
   sed -i 's/\$releasever/8/g' /etc/yum.repos.d/docker-ce.repo
   ```
3. 安装 Docker CE：

   ```
   dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
4. 启动 Docker 服务：

   ```
   systemctl enable --now docker
   ```

1. 更新软件包索引：

   ```
   sudo apt-get update
   sudo apt-get -y install ca-certificates curl
   ```
2. 添加 Docker GPG 密钥：

   ```
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc
   ```
3. 添加 Docker 软件源：

   ```
   echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```
4. 安装 Docker CE：

   ```
   sudo apt-get update
   sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
5. 启动 Docker 服务：

   ```
   sudo systemctl enable --now docker
   ```
6. 确认 Docker 已成功安装：

   ```
   docker --version
   ```

## 下载部署工具

请在待部署的虚拟机或物理服务器中安装榫卯 AI 平台命令行工具并为其分配可执行权限，该命令行工具用于部署 AI 平台的监控组件和控制平面。

1. 根据服务器的 CPU 架构下载对应的 AI 平台命令行工具安装文件。
2. 为命令行工具安装文件分配可执行权限。

   ```
   chmod +x neutree-cli-<arch>
   ```

   `<arch>` 需替换为服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。

## 部署监控组件

使用 AI 平台命令行工具部署监控组件 OBSStack 为平台提供系统监控和可观测性支持。

1. 启动监控组件服务：

   ```
   ./neutree-cli-<arch> launch obs-stack
   ```

   `<arch>` 需替换为服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。

   说明：

   此方式将自动从 DockerHub 拉取所需镜像，请确保服务器网络可访问 DockerHub。
2. 若监控组件服务启动失败，请通过以下命令查看监控组件服务日志以排查问题：

   ```
   docker compose -f ./neutree-deploy/obs-stack/docker-compose.yml logs
   ```

## 部署控制平面

使用 AI 平台命令行工具部署简化配置的控制平面，提供用户管理界面。

1. 在终端执行如下命令生成随机 JWT 密钥：

   ```
   openssl rand -base64 32 | tr '+/' '-_' | tr -d '='
   ```

   说明：

   AI 平台使用 JWT（JSON Web Token）进行身份验证和授权，JWT 密钥用于保障 JWT 的安全性。
2. 启动控制平面服务：

   ```
   ./neutree-cli-<arch> launch neutree-core \
     --version=v1.0.0-enterprise \
     --metrics-remote-write-url=http://<obstack_ip>:8480/insert/0/prometheus/ \
     --jwt-secret=<jwt_secret> \
     --grafana-url=http://<obstack_ip>:3030 \
     --admin-password=<admin_password>
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<arch>` | 服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<obstack_ip>` | 监控组件所在服务器的 IP 地址。 |
   | `<jwt_secret>` | 准备工作中生成的 JWT 密钥字符串。 |
   | `<admin_password>` | AI 平台管理员初始密码。可选项，建议配置自定义初始密码；留空则由系统自动生成，需在 AI 平台部署完成后通过 `docker logs -f migration` 获取。 |

   说明：

   此方式将自动从 DockerHub 拉取所需镜像，请确保服务器网络可访问 DockerHub。
3. 若控制平面服务启动失败，可通过以下命令查看控制平面服务日志以排查问题：

   ```
   docker compose -f ./neutree-deploy/neutree-core/docker-compose.yml logs
   ```

## 验证部署结果

等待所有服务启动完成后，验证部署结果。

1. 检查所有服务状态：

   ```
   docker ps
   ```
2. 使用管理员账号 `admin@neutree.local` 和初始密码访问 AI 平台管理界面 `http://<control_plane_ip>:3000`。

   若无法访问 AI 平台管理界面请确认 Docker 服务是否运行正常。

---

## 功能体验 > 快速创建推理实例

# 快速创建推理实例

您可以根据部署环境的网络情况，选择合适的 YAML 示例文件[导入](/smtx-ai/1.0.0/user_guide/yaml/yaml-import) AI 平台，快速创建一个推理实例。导入后您可以在 AI 平台该实例下的测试平台中进行[对话测试](/smtx-ai/1.0.0/user_guide/model-service/endpoint#%E5%BF%AB%E9%80%9F%E6%B5%8B%E8%AF%95)。

本节提供如下两个场景的 YAML 示例文件：

- 若您的环境可以访问 Docker Hub 或 Hugging Face 并且速度较快，建议参考示例一从 Docker Hub 拉取容器镜像和从 Hugging Face 下载模型。
- 若您的环境无法访问 Docker Hub、Hugging Face 或者速度较慢，请参考示例二使用国内加速镜像获取容器镜像和模型。

示例文件中配置了名为 `quick-start-inference` 的推理实例，该推理实例使用 `llama.cpp` 推理引擎运行小型模型 `Tinystories-gpt-0.1-3m-GGUF`。由于示例中使用的模型尺寸极小，生成的文本内容主要用于体验基本流程，不具备实际业务环境的应用价值。

使用时请将示例文件中的如下参数替换为实际值：

| 参数 | 描述 |
| --- | --- |
| `<control_plane_ip>` | 控制平面所在的服务器的 IP 地址。 |
| `<ssh_user>` | 控制平面所在的服务器的 SSH 用户名，需为 root 用户或具有 root 权限的其他用户。 |
| `<ssh_private_key>` | 控制平面所在的服务器的 SSH 私钥的 Base64 编码字符串。 使用前请确保该私钥对应的公钥已添加到服务器的信任列表中：  ``` mkdir -p ~/.ssh && cat <ssh_public_key_path> >> ~/.ssh/authorized_keys chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys ```  随后可通过以下命令获取私钥的 Base64 编码：  `cat <ssh_private_key_path> | base64 -w 0` |

示例一示例二

```
apiVersion: v1
kind: Cluster
metadata:
  name: quick-start-cluster
  workspace: default
spec:
  type: ssh
  config:
    ssh_config:
      provider:
        head_ip: <control_plane_ip>
      auth:
        ssh_user: <ssh_user>
        ssh_private_key: <ssh_private_key>
  image_registry: public-docker
  version: v1.0.0
---
apiVersion: v1
kind: Endpoint
metadata:
  name: quick-start-inference
  workspace: default
spec:
  cluster: quick-start-cluster
  model:
    registry: public-hugging-face
    name: afrideva/Tinystories-gpt-0.1-3m-GGUF
    file: "*8_0.gguf"
    version: main
    task: text-generation
  engine:
    engine: llama-cpp
    version: v0.3.7
  resources:
    cpu: '1'
    memory: '1'
  replicas:
    num: 1
  deployment_options:
    scheduler:
      type: consistent_hash
  variables:
    engine_args: {}
---
apiVersion: v1
kind: ImageRegistry
metadata:
  name: public-docker
  workspace: default
spec:
  url: https://docker.io
  repository:
  authconfig:
    username: ""
    password: ""
    auth: ""
---
apiVersion: v1
kind: ModelRegistry
metadata:
  name: public-hugging-face
  workspace: default
spec:
  type: hugging-face
  url: https://huggingface.co
  credentials: ""
```

```
apiVersion: v1
kind: Cluster
metadata:
  name: quick-start-cluster
  workspace: default
spec:
  type: ssh
  config:
    ssh_config:
      provider:
        head_ip: <control_plane_ip>
      auth:
        ssh_user: <ssh_user>
        ssh_private_key: <ssh_private_key>
  image_registry: public-1ms
  version: v1.0.0
---
apiVersion: v1
kind: Endpoint
metadata:
  name: quick-start-inference
  workspace: default
spec:
  cluster: quick-start-cluster
  model:
    registry: public-hf-mirror
    name: afrideva/Tinystories-gpt-0.1-3m-GGUF
    file: "*8_0.gguf"
    version: main
    task: text-generation
  engine:
    engine: llama-cpp
    version: v0.3.7
  resources:
    cpu: '1'
    memory: '1'
  replicas:
    num: 1
  deployment_options:
    scheduler:
      type: consistent_hash
  variables:
    engine_args: {}
---
apiVersion: v1
kind: ImageRegistry
metadata:
  name: public-1ms
  workspace: default
spec:
  url: https://docker.1ms.run
  repository:
  authconfig:
    username: ""
    password: ""
    auth: ""
---
apiVersion: v1
kind: ModelRegistry
metadata:
  name: public-hf-mirror
  workspace: default
spec:
  type: hugging-face
  url: https://hf-mirror.com
  credentials: ""
```

---

## 部署 AI 平台

# 部署 AI 平台

AI 平台包含监控组件和控制平面，监控组件为平台提供系统监控和可观测性支持，控制平面提供平台管理、用户界面、API 服务等核心功能。

如需快速体验平台功能，可参考[功能体验](/smtx-ai/1.0.0/user_guide/getting-started/quick-start-overview)。

---

## 部署 AI 平台 > 部署模式

# 部署模式

AI 平台支持以下两种部署方式，您可以根据实际需求选择适合的部署模式：

- [**Docker 部署**](/smtx-ai/1.0.0/user_guide/getting-started/deploy-docker)：适合中小规模部署和开发环境，使用 Docker Compose 部署。
- [**Kubernetes 部署**](/smtx-ai/1.0.0/user_guide/getting-started/deploy-kubernetes)：适合大规模生产环境，组件部署在 Kubernetes 服务的 Pod 上，与 SMTX Kubernetes 服务（以下简称 “SKS”）配合使用时将充分利用 SKS 的高可用和弹性扩展能力。

---

## 部署 AI 平台 > 部署要求

# 部署要求

部署 AI 平台前，请确保部署 AI 平台的服务器、虚拟机或 Pod 的 CPU 架构和操作系统版本满足《榫卯 AI 平台发布说明》中[版本兼容说明](/smtx-ai/1.0.0/release_notes/compatibility)中的要求，并阅读本节了解 AI 平台所需的资源要求以及各组件间的网络端口开放要求。

## 资源要求

AI 平台各组件占用的资源如下表所示，请确保您的服务器、虚拟机或 Pod 中资源满足要求：

| 组件 | CPU | 内存 | 存储 |
| --- | --- | --- | --- |
| 监控组件 | 4 核 vCPU | 8 GiB | 400 GiB |
| 控制平面 | 4 核 vCPU | 8 GiB | 200 GiB |

## 网络要求

为了确保 AI 平台正常进行，当源端访问目标端时，目标端需要开放相应的端口，请您根据端口说明开放目标端的相应端口。下列端口的传输端协议为 TCP。

| 源端 | 目标端 | 端口 | 用途 |
| --- | --- | --- | --- |
| 外部客户端 | 控制平面 | 3000 | 访问 AI 平台 Web 管理界面。 |
| 外部客户端 | 监控组件 | 3030 | 访问 Grafana 监控界面。 |
| 控制平面 | 监控组件 | 8480 | 写入监控指标。 |

---

## 部署 AI 平台 > 使用 Docker Compose 部署

# 使用 Docker Compose 部署

AI 平台支持通过 Docker 将监控组件和控制平面部署到服务器或虚拟机中。建议将监控组件和控制平面部署在不同的服务器或位于不同主机的虚拟机中，以提高平台的可用性和性能。

## 配置操作系统

请根据服务器或虚拟机的操作系统类型，参考以下章节进行系统配置并安装 Docker 作为容器运行时。

### 系统配置

RHEL/Rocky Linux/openEulerUbuntu

1. 配置静态 IP 地址：

   ```
   sudo vi /etc/sysconfig/network-scripts/ifcfg-<interface>
   ```

   `<interface>` 需替换为网口名称，例如 `eth0`。
2. 配置 DNS 服务器：

   ```
   sudo vi /etc/resolv.conf
   ```
3. 关闭防火墙：

   ```
   sudo systemctl stop firewalld && sudo systemctl disable firewalld
   ```
4. 关闭 SELinux：

   ```
   echo -e "SELINUX=disabled\nSELINUXTYPE=targeted" | sudo tee /etc/selinux/config
   sudo setenforce 0
   ```

1. 配置静态 IP 地址和 DNS 服务器：

   ```
   sudo vi /etc/netplan/50-cloud-init.yaml
   ```
2. 应用上述网络配置：

   ```
   sudo netplan apply
   ```
3. 关闭防火墙：

   ```
   sudo ufw disable
   ```
4. 可选项，按需关闭 AppArmor：

   ```
   sudo systemctl disable apparmor && sudo systemctl stop apparmor
   ```
5. 重启操作系统使配置生效：

   ```
   sudo reboot
   ```

### 安装 Docker

RHEL/Rocky LinuxopenEulerUbuntu

1. 安装 Docker CE：

   ```
   sudo dnf -y install dnf-plugins-core
   sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
   sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
2. 启动 Docker 服务：

   ```
   sudo systemctl enable --now docker
   ```
3. 确认 Docker 已成功安装：

   ```
   docker --version
   ```
4. 重启操作系统使配置生效：

   ```
   sudo reboot
   ```

1. 配置基础环境与仓库：

   ```
   dnf -y install dnf-plugins-core
   dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
   ```
2. 指定系统版本号：

   ```
   sed -i 's/\$releasever/8/g' /etc/yum.repos.d/docker-ce.repo
   ```
3. 安装 Docker CE：

   ```
   dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
4. 启动 Docker 服务：

   ```
   systemctl enable --now docker
   ```

1. 更新软件包索引：

   ```
   sudo apt-get update
   sudo apt-get -y install ca-certificates curl
   ```
2. 添加 Docker GPG 密钥：

   ```
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc
   ```
3. 添加 Docker 软件源：

   ```
   echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```
4. 安装 Docker CE：

   ```
   sudo apt-get update
   sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
5. 启动 Docker 服务：

   ```
   sudo systemctl enable --now docker
   ```
6. 确认 Docker 已成功安装：

   ```
   docker --version
   ```

## 部署监控组件

登录用于部署监控组件的服务器或虚拟机，部署监控组件为整个平台提供可观测性支持。

**准备工作**

1. 根据服务器的 CPU 架构下载指定版本的 AI 平台命令行工具安装文件和控制平面离线镜像文件。
2. 为命令行工具安装文件分配可执行权限：

   ```
   chmod +x neutree-cli-<arch>
   ```

   `<arch>` 需替换为服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。
3. 通过命令行工具加载控制平面离线镜像：

   镜像加载至本地镜像上传至远程镜像仓库

   ```
   ./neutree-cli-<arch> import controlplane \
     --package <controlplane_package> \
     --local
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<arch>` | 服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<controlplane_package>` | 控制平面离线镜像文件名称，格式为 `neutree-controlplane-v1.0.0-enterprise-<arch>.tar.gz`。 |

   ```
   ./neutree-cli-<arch> import controlplane \
     --package <controlplane_package> \
     --mirror-registry <mirror_registry> \
     --registry-username <registry_username> \
     --registry-password <registry_password>
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<arch>` | 服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<controlplane_package>` | 控制平面离线镜像文件名称，格式为 `neutree-controlplane-v1.0.0-enterprise-<arch>.tar.gz`。 |
   | `<mirror_registry>` | 镜像仓库地址。 |
   | `<registry_username>` | 镜像仓库用户的用户名，需为具备上传镜像权限的用户。 |
   | `<registry_password>` | 镜像仓库用户的登录密码或访问密钥（例如 token）。 |

**操作步骤**

1. 启动监控组件服务：

   从本地拉取镜像从远程镜像仓库拉取镜像

   ```
   ./neutree-cli-<arch> launch obs-stack
   ```

   `<arch>` 需替换为服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。

   ```
   ./neutree-cli-<arch> launch obs-stack \
     --mirror-registry <mirror_registry>
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<arch>` | 服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<mirror_registry>` | 镜像仓库地址。 |
2. 访问 `http://<obstack_ip>:3030/`，显示 Grafana 登录界面即表示监控组件部署成功。

   `<obstack_ip>` 需替换为监控组件所在服务器的 IP 地址。

## 部署控制平面

登录用于部署控制平面的服务器或虚拟机，部署控制平面提供平台管理、用户界面、API 服务等核心功能。

**准备工作**

1. 在终端执行如下命令生成随机 JWT 密钥：

   ```
   openssl rand -base64 32 | tr '+/' '-_' | tr -d '='
   ```

   说明：

   AI 平台使用 JWT（JSON Web Token）进行身份验证和授权，JWT 密钥用于保障 JWT 的安全性。
2. 根据服务器的 CPU 架构下载指定版本的 AI 平台命令行工具和控制平面离线镜像文件。
3. 为命令行工具安装文件分配可执行权限：

   ```
   chmod +x neutree-cli-<arch>
   ```

   `<arch>` 需替换为服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。
4. 通过命令行工具加载控制平面离线镜像：

   镜像加载至本地镜像上传至远程镜像仓库

   ```
   ./neutree-cli-<arch> import controlplane \
     --package <controlplane_package> \
     --local
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<arch>` | 服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<controlplane_package>` | 控制平面离线镜像文件名称，格式为 `neutree-controlplane-v1.0.0-enterprise-<arch>.tar.gz`。 |

   ```
   ./neutree-cli-<arch> import controlplane \
     --package <controlplane_package> \
     --mirror-registry <mirror_registry> \
     --registry-username <registry_username> \
     --registry-password <registry_password>
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<arch>` | 服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<controlplane_package>` | 控制平面离线镜像文件名称，格式为 `neutree-controlplane-v1.0.0-enterprise-<arch>.tar.gz`。 |
   | `<mirror_registry>` | 镜像仓库地址。 |
   | `<registry_username>` | 镜像仓库用户的用户名，需为具备上传镜像权限的用户。 |
   | `<registry_password>` | 镜像仓库用户的登录密码或访问密钥（例如 token）。 |

**操作步骤**

1. 启动控制平面服务：

   从本地拉取镜像从远程镜像仓库拉取镜像

   ```
   ./neutree-cli-<arch> launch neutree-core \
     --version=v1.0.0-enterprise \
     --metrics-remote-write-url=http://<obstack_ip>:8480/insert/0/prometheus/ \
     --jwt-secret=<jwt_secret> \
     --grafana-url=http://<obstack_ip>:3030 \
     --admin-password=<admin_password> \
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<arch>` | 服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<obstack_ip>` | 监控组件所在服务器的 IP 地址。 |
   | `<jwt_secret>` | 准备工作中生成的 JWT 密钥字符串。 |
   | `<admin_password>` | AI 平台管理员初始密码。可选项，建议配置自定义初始密码；留空则由系统自动生成，需在 AI 平台部署完成后通过 `docker logs -f migration` 获取。 |

   ```
   ./neutree-cli-<arch> launch neutree-core \
     --version=v1.0.0-enterprise \
     --metrics-remote-write-url=http://<obstack_ip>:8480/insert/0/prometheus/ \
     --jwt-secret=<jwt_secret> \
     --grafana-url=http://<obstack_ip>:3030 \
     --admin-password=<admin_password> \
     --mirror-registry=<mirror_registry>
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<arch>` | 服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<obstack_ip>` | 监控组件所在服务器的 IP 地址。 |
   | `<jwt_secret>` | 准备工作中生成的 JWT 密钥字符串。 |
   | `<admin_password>` | AI 平台管理员初始密码。可选项，建议配置自定义初始密码；留空则由系统自动生成，需在 AI 平台部署完成后通过 `docker logs -f migration` 获取。 |
   | `<mirror_registry>` | 镜像仓库地址。 |
2. 检查服务状态：

   ```
   docker ps
   ```
3. 使用管理员账号 `admin@neutree.local` 和初始密码访问 `http://<control_plane_ip>:3000`，成功访问 AI 平台管理界面表示部署成功。

   `<control_plane_ip>` 需替换为控制平面所在服务器的 IP 地址。

## 部署昇腾插件

使用昇腾 NPU 时，请参考本节内容在部署了控制平面的服务器或虚拟机中部署昇腾插件。否则请跳过本节内容。

1. 根据服务器的 CPU 架构和昇腾插件版本下载昇腾插件离线镜像文件。
2. 通过命令行工具加载昇腾插件离线镜像文件：

   镜像加载至本地镜像上传至远程镜像仓库

   ```
   ./neutree-cli-<arch> import controlplane \
     --package <ascend_npu_plugin_package> \
     --local
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<arch>` | 服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<ascend_npu_plugin_package>` | 昇腾插件离线镜像文件名称，格式为 `ascend-npu-accelerator-plugin-v1.0.0-<arch>.tar.gz`。 |

   ```
   ./neutree-cli-<arch> import controlplane \
     --package <ascend_npu_plugin_package> \
     --mirror-registry <mirror_registry> \
     --registry-username <registry_username> \
     --registry-password <registry_password>
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<arch>` | 服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<ascend_npu_plugin_package>` | 昇腾插件离线镜像文件名称，格式为 `ascend-npu-accelerator-plugin-v1.0.0-<arch>.tar.gz`。 |
   | `<mirror_registry>` | 镜像仓库地址。 |
   | `<registry_username>` | 镜像仓库用户的用户名，需为具备上传镜像权限的用户。 |
   | `<registry_password>` | 镜像仓库用户的登录密码或访问密钥（例如 token）。 |
3. 启动昇腾插件：

   从本地拉取镜像从远程镜像仓库拉取镜像

   ```
   docker run --name ascend-npu-accelerator-plugin -p 8090:8080 \
     --restart always -d neutree/ascend-npu-accelerator-plugin:v1.0.0 \
     --plugin-access-url=http://<control_plane_ip>:8090 \
     --plugin-server-url=http://<control_plane_ip>:3001
   ```

   `<control_plane_ip>` 需替换为控制平面所在服务器的 IP 地址。

   ```
   docker run --name ascend-npu-accelerator-plugin -p 8090:8080 \
     --restart always -d <mirror_registry>/neutree/ascend-npu-accelerator-plugin:v1.0.0 \
     --plugin-access-url=http://<control_plane_ip>:8090 \
     --plugin-server-url=http://<control_plane_ip>:3001
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<mirror_registry>` | 镜像仓库地址。 |
   | `<control_plane_ip>` | 控制平面所在服务器的 IP 地址。 |
4. 确认插件注册成功：

   ```
   docker logs -f neutree-core
   ```

   输出中包含 `Register accelerator plugin: npu` 则表明插件注册成功。

---

## 部署 AI 平台 > Kubernetes 部署

# Kubernetes 部署

Kubernetes 部署方式将通过 Helm Chart 一键部署包含控制平面和监控组件的 AI 平台。

## 前提条件

为确保 AI 平台部署成功，请确认您具备 Kubernetes 集群的镜像仓库访问权限，且您的 Kubernetes 集群满足以下要求：

- Kubernetes 集群支持持久化存储，已安装 CSI 插件并设置默认的、支持 ReadWriterOnce 的文件系统类型置备的存储类。

  配合 SKS 使用时，请在 CloudTower 中为 SKS 工作负载集群启用 CSI 插件。详情请参考《SMTX Kubernetes 服务管理指南》的**管理插件**、**管理存储类**章节。
- Kubernetes 集群支持 LoadBalancer 类型的服务，并且分配至少 3 个 LoadBalancer 服务地址。

  配合 SKS 使用时，请在 CloudTower 中为 SKS 工作负载集群启用 MetalLB 插件，并分配至少 3 个 LoadBalancer 服务地址。详情请参考《SMTX Kubernetes 服务管理指南》的**管理插件**章节。

## 准备工作

1. 配置 Kubeconfig，具体配置方法请参考[使用 kubeconfig 文件组织集群访问](https://kubernetes.io/zh-cn/docs/concepts/configuration/organize-cluster-access-kubeconfig/)。
2. 在终端执行如下命令生成随机 JWT 密钥：

   ```
   openssl rand -base64 32 | tr '+/' '-_' | tr -d '='
   ```

   说明：

   AI 平台使用 JWT（JSON Web Token）进行身份验证和授权，JWT 密钥用于保障 JWT 的安全性。
3. 上传 AI 平台控制平面离线镜像至 Kubernetes 集群的镜像仓库。

   1. 根据服务器的 CPU 架构下载指定版本的 AI 平台命令行工具安装文件和控制平面离线镜像文件。
   2. 为命令行工具安装文件分配可执行权限：

      ```
      chmod +x neutree-cli-<arch>
      ```

      `<arch>` 需替换为服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。
   3. 通过命令行工具将控制平面镜像上传至指定的镜像仓库：

      ```
      ./neutree-cli-<arch> import controlplane \
        --package <controlplane_package> \
        --mirror-registry <mirror_registry> \
        --registry-username <registry_username> \
        --registry-password <registry_password>
      ```

      | 参数 | 描述 |
      | --- | --- |
      | `<arch>` | 需替换为服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
      | `<controlplane_package>` | 控制平面离线镜像文件名称，格式为 `neutree-controlplane-v1.0.0-enterprise-<arch>.tar.gz`。 |
      | `<mirror_registry>` | 镜像仓库地址。 |
      | `<registry_username>` | 镜像仓库用户的用户名，需为具备上传镜像权限的用户。 |
      | `<registry_password>` | 镜像仓库用户的登录密码或访问密钥（例如 token）。 |

## 部署流程

1. 下载 Helm Chart 安装文件。
2. 创建并编辑配置文件：

   ```
   helm show values ./neutree-v1.0.0-enterprise.tgz > values.yaml
   ```

   参数描述如下：

   - **核心配置**

     | 参数 | 默认值 | 描述 |
     | --- | --- | --- |
     | `jwtSecret` | `"mDCvM4zSk0ghmpyKhgqWb0g4igcOP0Lp"` | JWT 密钥字符串。当前提供默认值，但生产环境建议修改为准备工作中生成的 JWT 密钥字符串。 |
     | `adminPassword` | 无 | 自定义 AI 平台管理员初始密码，可选项，建议配置。留空则由系统自动生成，需在 AI 平台部署完成后通过 `kubectl -n neutree logs -l app.kubernetes.io/component=neutree-post-migration-hook-job` 获取，仅在第一次部署时可以通过 Pod 日志查看。 |
     | `imagePullSecrets` | `[]` | 镜像拉取密钥列表，格式为 `[{name: "secret-name"}]`。 |
     | `system.grafana.url` | `""` | 外部 Grafana 访问 URL，留空使用内置 Grafana。 |
     | `metrics.remoteWriteUrl` | `""` | 远程 metrics 存储地址，留空使用内置 Victoria Metrics。 |
   - **镜像配置**

     | 参数 | 默认值 | 描述 |
     | --- | --- | --- |
     | `global.image.registry` | 无 | 全局远程镜像仓库地址，当前 Grafana 不会继承该配置，需要单独配置。 |
     | `global.imageRegistry` | 无 | Grafana 远程镜像仓库地址。 |
   - **服务配置**

     | 参数 | 默认值 | 描述 |
     | --- | --- | --- |
     | `api.service.type` | `ClusterIP` | API 服务类型，支持 `LoadBalancer`、`NodePort`、`ClusterIP`。 |
     | `api.service.nodePort` | `""` | NodePort 端口配置。 |
   - **存储**

     | 参数 | 默认值 | 描述 |
     | --- | --- | --- |
     | `db.persistence.enabled` | `true` | 是否启用数据库持久化存储。 |
     | `db.persistence.size` | `40Gi` | 数据库存储容量。 |
     | `vmstorage.persistentVolume.size` | `40Gi` | 监控数据存储容量。 |

     **配置示例**

     ```
     # 核心配置
     jwtSecret: "<jwt_secret>"
     imagePullSecrets: []
     adminPassword: "<admin_password>"

     # 系统配置
     system:
       grafana:
        url: ""

     metrics:
       remoteWriteUrl: ""

     # 服务配置
     api:
       service:
         type: LoadBalancer

     # 数据库配置
     db:
       persistence:
         enabled: true
         size: 40Gi

     # 监控配置
     victoria-metrics-cluster:
       vmstorage:
         persistentVolume:
           size: 40Gi

     grafana:
       adminUser: admin
       adminPassword: your-secure-password
     ```
3. 安装 AI 平台：

   ```
   helm install neutree neutree-v1.0.0-enterprise.tgz -f values.yaml \
     --namespace=neutree \
     --create-namespace
   ```
4. 检查 Pod 状态：

   ```
   kubectl get pods -n neutree
   ```
5. 使用管理员账号 `admin@neutree.local` 和初始密码访问 AI 平台管理界面。

   - `api.service.type` 为 `NodePort` 时，访问地址为 `http://<NODE_IP>:<nodePort>`。
   - `api.service.type` 为 `LoadBalancer` 时，访问地址为 `http://<LOADBALANCER_IP>:3000`。
   - `api.service.type` 为 `ClusterIP` 时，需额外执行 `kubectl -n neutree port-forward svc/neutree-api-service 3000:3000` 从本地的 3000 端口访问 `http://127.0.0.1:3000`。

## 修改监控组件配置

AI 平台部署后将默认启用监控组件 VictoriaMetrics 和 Grafana，您可以通过编辑 `values.yaml` 文件修改监控组件的配置，如禁用组件、设置存储容量以及修改密码。

```
victoria-metrics-cluster:
  enabled: true # 设置为 false 可禁用内置 VictoriaMetrics
  global:
    image:
      registry: "registry.example.com/neutree-ai"
  vmstorage:
    persistentVolume:
      size: 40Gi # 设置监控数据存储容量

grafana:
  enabled: true # 设置为 false 可禁用内置 Grafana
  image:
    registry: registry.example.com/neutree-ai
  adminUser: admin
  adminPassword: your-secure-password # 生产环境必须修改
```

## 部署昇腾插件

使用昇腾 NPU 时请在控制平面所在 Namespace 部署昇腾插件。否则请跳过本节内容。

1. 根据服务器的 CPU 架构和昇腾插件版本下载昇腾插件离线镜像文件。
2. 通过命令行工具将昇腾插件离线镜像文件上传至远程镜像仓库：

   ```
   ./neutree-cli-<arch> import controlplane \
     --package <ascend_npu_plugin_package> \
     --mirror-registry <mirror_registry> \
     --registry-username <registry_username> \
     --registry-password <registry_password>
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<arch>` | 服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<ascend_npu_plugin_package>` | 昇腾插件离线镜像文件名称，格式为 `ascend-npu-accelerator-plugin-v1.0.0-<arch>.tar.gz`。 |
   | `<mirror_registry>` | 镜像仓库地址。 |
   | `<registry_username>` | 镜像仓库用户的用户名，需为具备上传镜像权限的用户。 |
   | `<registry_password>` | 镜像仓库用户的登录密码或访问密钥（例如 token）。 |
3. 下载昇腾插件 Helm Chart 安装文件。
4. 安装昇腾插件：

   ```
   helm install ascend-npu-accelerator-plugin ascend-npu-accelerator-plugin-v1.0.0.tgz \
     --namespace=neutree \
     --create-namespace \
     --set image.registry=<mirror_registry>
   ```

   `<mirror_registry>` 需替换为镜像仓库地址。
5. 确认昇腾插件注册成功：

   ```
   kubectl -n neutree logs -l app.kubernetes.io/component=neutree-core
   ```

   输出中包含 `Register accelerator plugin: npu` 则表明插件注册成功。

---

## 查看平台概览

# 查看平台概览

使用过程中您可以在 AI 平台管理界面左侧导航栏中选择**概览**，查看 AI 平台的整体情况。

概览页面将展示如下信息：

- 集群数量
- 推理实例数量
- 监控信息

  | 指标 | 描述 |
  | --- | --- |
  | Cluster Utilization | 集群利用率。集群内所有物理资源（CPU、GPU、内存、磁盘等）的聚合利用率。忽略应用 (Application)变量。 |
  | QPS per application | 应用 QPS。每个所选应用的每秒查询数。 |
  | Error QPS per application per error code | 基于错误码的应用错误 QPS。每个所选应用按错误代码分类的每秒错误查询数。 |
  | P50 latency per application | 应用 P50 延迟。每个所选应用的 P50 延迟。 |
  | P90 latency per application | 应用 P90 延迟。每个所选应用的 P90 延迟。 |
  | P99 latency per application | 应用 P99 延迟。每个所选应用的 P99 延迟。 |
  | Replicas per deployment | 部署副本数。每个部署 (Deployment) 的副本数量。忽略应用变量。 |
  | QPS per deployment | 部署 QPS。每个部署的每秒查询数。 |
  | Error QPS per deployment | 部署错误 QPS。每个部署的每秒错误查询数。 |
  | P50 latency per deployment | P50 延迟。每个部署的 P50 延迟。 |
  | P90 latency per deployment | P90 延迟。每个部署的 P90 延迟。 |
  | P99 latency per deployment | P99 延迟。每个部署的 P99 延迟。 |
  | Queue size per deployment | 部署队列大小。每个部署中排队的请求数量。忽略应用变量。 |
  | Node count | 节点数量。此集群中的节点数量。忽略应用变量。 |
  | Node network | 节点网络速度。每个节点的网络速度。忽略应用变量。 |
  | Ongoing HTTP Requests | 进行中的 HTTP 请求。HTTP 代理中的正在进行的请求数。 |
  | Ongoing gRPC Requests | 进行中的 gRPC 请求。gRPC 代理中的正在进行的请求数。 |
  | Scheduling Tasks | 调度任务数。路由中的请求调度任务数。 |
  | Scheduling Tasks in Backoff | 退避中的调度任务数。路由中处于“退避（Backoff）”状态的请求调度任务数量。 |
  | Controller Control Loop Duration | 控制器控制循环耗时。最近一次控制器控制循环的持续时间。 |
  | Number of Control Loops | 控制循环次数。控制器执行的控制循环总数。在控制器的生命周期内单调递增。 |

---

## 管理基础设施 > 基本概念

# 基本概念

## 集群

集群用于运行 AI 负载，每一个集群对应一个 Ray 集群。每个集群由一个或多个节点组成，工作负载以容器的形式运行节点上。

## 模型缓存

模型缓存用于在集群范围内缓存来自模型仓库的模型文件，以减少对模型仓库的访问。当部署在同一个集群的多个推理服务实例使用相同模型时，模型缓存可以避免重复下载，提高资源利用效率。

## 容器镜像仓库

容器镜像仓库为集群部署提供所需的容器镜像。

---

## 管理基础设施 > 管理容器镜像仓库

# 管理容器镜像仓库

容器镜像仓库是 AI 平台基础设施层的重要组件，为集群部署提供所需的容器镜像。

若集群节点与 Docker 客户端兼容的容器镜像仓库（如 Docker Hub）连通，[创建容器镜像仓库](#%E5%88%9B%E5%BB%BA%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F%E4%BB%93%E5%BA%93)后集群将通过这些容器镜像仓库获取 AI 平台的容器镜像。

若集群节点无法连通上述容器镜像仓库或访问速度较慢，则可以[手动导入容器镜像](#%E6%89%8B%E5%8A%A8%E5%AF%BC%E5%85%A5%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F)。

## 创建容器镜像仓库

1. 登录 AI 平台管理界面，在左侧菜单栏中单击**容器镜像仓库**，在右侧页面单击**创建**。
2. 填写配置信息。

   - **基本信息**

     | 参数 | 描述 | 创建后是否允许编辑 |
     | --- | --- | --- |
     | 名称 | 容器镜像仓库的名称。 | 否 |
     | 工作空间 | 容器镜像仓库所属的工作空间。 | 否 |
   - **镜像仓库**

     | 参数 | 描述 | 创建后是否允许编辑 |
     | --- | --- | --- |
     | URL | 容器镜像仓库的 URL。使用 Docker Hub 时，URL 为 `https://docker.io`。 | 是 |
     | 仓库 | 容器镜像仓库中的**项目**或**仓库**。使用 Docker Hub 时，无需填写。 | 是 |
   - **身份验证**

     | 参数 | 描述 | 创建后是否允许编辑 |
     | --- | --- | --- |
     | 用户名 | 访问容器镜像仓库的用户名。 | 是 |
     | 密码 | 访问容器镜像仓库的用户密码。 | 是 |
3. 确认所有配置信息无误后，单击**保存**。

## 手动导入容器镜像

网络环境受限时，您可以将所需的容器镜像手动导入到 AI 平台的容器镜像仓库中。

**操作步骤**

1. 根据服务器的 CPU 架构下载指定版本的 AI 平台命令行工具安装文件和指定加速器类型的集群离线镜像文件。
2. 通过命令行工具上传集群离线镜像至指定的镜像仓库：

   ```
   ./neutree-cli-<arch> import cluster \
   --package <cluster_package> \
   --mirror-registry <mirror_registry> \
   --registry-username <registry_username> \
   --registry-password <registry_password>
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<arch>` | 服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<cluster_package>` | 集群离线镜像文件名称。 - 静态节点集群离线镜像文件格式为 `neutree-cluster-ssh-<accelerator_type>-v1.0.0-<arch>.tar.gz`。其中 `<accelerator_type>` 为加速器类型，取值为 `nvidia_gpu`、`amd_gpu` 或 `npu`。 - Kubernetes 集群离线镜像文件格式为 `neutree-cluster-k8s-v1.0.0-<arch>.tar.gz`。 |
   | `<mirror_registry>` | 镜像仓库地址。 |
   | `<registry_username>` | 镜像仓库用户的用户名，需为具备上传镜像权限的用户。 |
   | `<registry_password>` | 镜像仓库用户的登录密码或访问密钥（例如 token）。 |

## 查看容器镜像仓库

登录 AI 平台管理界面，在左侧菜单栏中单击**容器镜像仓库**，右侧容器镜像仓库列表将展示当前所有容器镜像仓库，单击容器镜像仓库名称即可查看详情。

## 编辑容器镜像仓库

容器镜像仓库创建后，您可以根据实际需求修改镜像仓库 URL、仓库信息以及身份验证配置。

1. 登录 AI 平台管理界面，在容器镜像仓库列表或详情页面单击菜单图标（**...**），选择**编辑**。
2. 在配置页面按需修改，具体参数说明请参考[创建容器镜像仓库](#%E5%88%9B%E5%BB%BA%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F%E4%BB%93%E5%BA%93)。
3. 确认配置信息无误后，单击**保存**完成编辑。

## 删除容器镜像仓库

1. 登录 AI 平台管理界面，在容器镜像仓库列表或详情页面单击菜单图标（**...**），选择**删除**。
2. 在弹出的对话框中，二次确认后单击**删除**，容器镜像仓库将被永久删除。

---

## 管理基础设施 > 管理集群

# 管理集群

集群负责 AI 模型推理、计算资源管理等功能，分为以下两种类型：

- [静态节点集群](/smtx-ai/1.0.0/user_guide/infrastructure/cluster-ssh)：适用于将服务器或虚拟机作为静态节点组成集群。控制平面通过 IP + SSH 信息访问静态节点。
- [Kubernetes 集群](/smtx-ai/1.0.0/user_guide/infrastructure/cluster-kubernetes)：适用于在已有 Kubernetes 集群上创建 AI 集群。AI 平台仅部署模型和推理所依赖的系统服务，计算资源由原生 Kubernetes 管理。控制平面通过 Kubeconfig 访问 Kubernetes 集群。

---

## 管理基础设施 > 管理集群 > 管理静态节点集群

# 管理静态节点集群

支持将服务器或虚拟机作为节点组成静态节点集群，分为**头节点**和**工作节点**两种节点类型：

- **头节点**：既是控制节点也是工作节点，负责运行管控服务的同时也可运行 AI 负载。
- **工作节点**：仅运行 AI 负载，不运行管控服务。

集群最小规模为单节点，即仅配置头节点，无需添加工作节点，此时头节点上同时运行管控服务和 AI 负载。

多节点集群中，推荐您使用不含加速器的节点作为头节点运行管控服务，将包含加速器的节点添加为工作节点专门用于 AI 负载。

请您根据业务需求，提前规划工作节点的数量。

## 节点要求

请确保节点的配置需满足如下要求：

- **资源配置**

  - 系统盘：200 GiB
  - CPU：至少 8 核 vCPU
  - 内存：至少 16 GiB
- **操作系统镜像**

  | 加速器类型 | 操作系统镜像 |
  | --- | --- |
  | **CPU** 或 **NVIDIA GPU** | Rocky-8.10-x86\_64-minimal.iso |
  | **华为昇腾 NPU** | OpenEuler-22.03-LTS-SP4-aarch64-dvd.iso |
  | **AMD GPU** | Ubuntu-22.04.5-live-server-amd64.iso |
- **端口要求**

  当源端访问目标端时，目标端需要开放相应的端口，请根据以下列表开放相应的端口。若无特殊说明，下面列举的端口均为 TCP 端口。

  | 源端 | 目标端 | 端口 | 用途 |
  | --- | --- | --- | --- |
  | 控制平面 | 所有节点 | 22 | 用于远程登录、静态节点初始化及维护。 |
  | 54311 | 抓取各节点的运行状态数据。 |
  | 44217 | 获取自动扩缩容相关的监控数据。 |
  | 44227 | 导出仪表盘的监控数据。 |
  | 所有节点 | 所有节点 | 10002-20000 | 节点间数据交换与分布式计算的核心通道。 |
  | 8077 | 用于节点管理。 |
  | 8076 | 用于共享内存对象访问和分发。 |
  | 56999 | 用于各节点执行环境（依赖包等）管理。 |
  | 头节点 | 所有节点 | 52365、8078 | 用于仪表盘相关命令下发的代理。 |
  | 控制平面 | 头节点 | 8265、8079 | 访问图形化管理界面。 |
  | 8000 | vLLM 模型推理服务的入口。 |
  | 工作节点 | 头节点 | 6379 | Ray 集群的元数据中心。 |
  | 开发者 | 头节点 | 10001 | 允许从远程脚本连接到集群运行作业。 |

## 配置操作系统

请根据节点的操作系统类型，参考以下章节进行系统配置并安装 Docker 作为容器运行时。

### 系统配置

RHEL/Rocky Linux/openEulerUbuntu

1. 配置静态 IP 地址：

   ```
   sudo vi /etc/sysconfig/network-scripts/ifcfg-<interface>
   ```

   `<interface>` 需替换为网口名称，例如 `eth0`。
2. 配置 DNS 服务器：

   ```
   sudo vi /etc/resolv.conf
   ```
3. 关闭防火墙：

   ```
   sudo systemctl stop firewalld && sudo systemctl disable firewalld
   ```
4. 关闭 SELinux：

   ```
   echo -e "SELINUX=disabled\nSELINUXTYPE=targeted" | sudo tee /etc/selinux/config
   sudo setenforce 0
   ```
5. 安装依赖软件：

   ```
   sudo dnf install rsync pciutils -y
   ```

1. 配置静态 IP 地址和 DNS 服务器：

   ```
   sudo vi /etc/netplan/50-cloud-init.yaml
   ```
2. 应用上述网络配置：

   ```
   sudo netplan apply
   ```
3. 关闭防火墙：

   ```
   sudo ufw disable
   ```
4. 可选项，按需关闭 AppArmor：

   ```
   sudo systemctl disable apparmor && sudo systemctl stop apparmor
   ```
5. 安装依赖软件：

   ```
   sudo apt-get update && sudo apt-get install rsync pciutils -y
   ```
6. 重启操作系统使配置生效：

   ```
   sudo reboot
   ```

### 安装 Docker

RHEL/Rocky LinuxopenEulerUbuntu

1. 安装 Docker CE：

   ```
   sudo dnf -y install dnf-plugins-core
   sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
   sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
2. 启动 Docker 服务：

   ```
   sudo systemctl enable --now docker
   ```
3. 确认 Docker 已成功安装：

   ```
   docker --version
   ```
4. 重启操作系统使配置生效：

   ```
   sudo reboot
   ```

1. 配置基础环境与仓库：

   ```
   dnf -y install dnf-plugins-core
   dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
   ```
2. 指定系统版本号：

   ```
   sed -i 's/\$releasever/8/g' /etc/yum.repos.d/docker-ce.repo
   ```
3. 安装 Docker CE：

   ```
   dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
4. 启动 Docker 服务：

   ```
   systemctl enable --now docker
   ```

1. 更新软件包索引：

   ```
   sudo apt-get update
   sudo apt-get -y install ca-certificates curl
   ```
2. 添加 Docker GPG 密钥：

   ```
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc
   ```
3. 添加 Docker 软件源：

   ```
   echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```
4. 安装 Docker CE：

   ```
   sudo apt-get update
   sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
5. 启动 Docker 服务：

   ```
   sudo systemctl enable --now docker
   ```
6. 确认 Docker 已成功安装：

   ```
   docker --version
   ```

## 配置加速器

若节点包含加速器，请根据加速器类型完成相应配置：

NVIDIA GPUAMD GPU昇腾 NPU

请参考 [NVIDIA 官方文档](https://docs.nvidia.com/)进行如下配置：

1. 关闭 NVIDIA GPU Nouveau driver。请参考 *Virtual GPU Software User Guide* 中 **Disabling the Nouveau Driver for NVIDIA Graphics Cards** 章节。
2. 安装不高于 590.x.x 且不低于 530.x.x 版本 NVIDIA Graphics driver。请参考 *Virtual GPU Software User Guide* 中 **Installing the NVIDIA vGPU Software Graphics Driver** 章节。
3. 安装 NVIDIA Container Toolkit。请参考 *NVIDIA Container Toolkit* 中 **Installing the NVIDIA Container Toolkit** 章节。

当前集群镜像支持的 ROCM 软件版本为 6.3.3，请安装对应版本的 AMDGPU driver 和 AMD Container Toolkit。请参考 [AMD 官⽅文档](https://instinct.docs.amd.com/latest/) 《AMD Container Toolkit Documentation》中 *Quick Start Guide* 章节。

请参考[昇腾官方文档](https://www.hiascend.com/document)进行如下配置：

1. 安装 CANN 版本为 8.1.RC1 的昇腾 310P3 NPU 驱动和固件包。请参考《CANN 软件安装指南》中**安装 NPU 驱动和固件**章节。
2. 安装 7.0.RC1 版本 Ascend Docker Runtime。请参考《CANN 软件安装指南》中**安装 Ascend Docker Runtime** 章节。

## 准备 SSH 私钥

在创建静态节点集群之前，您需要准备 SSH 私钥用于节点认证。控制平面将使用 SSH 私钥，通过 SSH 协议安全地连接并管理集群中的各个节点。

### 创建 SSH 密钥对

SSH 密钥对包含公钥和私钥，用于节点认证和安全通信。为提高安全性，不同的集群建议使用不同的 SSH 密钥对。

如果您还没有 SSH 密钥对，请通过以下步骤创建：

1. 在控制平面或本地机器上执行以下命令生成 SSH 密钥对：

   ```
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com" -f ~/.ssh/sunmao_cluster_key
   ```

   参数说明如下：

   | 参数 | 说明 |
   | --- | --- |
   | `-t rsa` | 指定密钥的加密算法类型为 RSA。 |
   | `-b 4096` | 指定密钥长度为 4096 位。 |
   | `-C "your_email@example.com"` | 为密钥添加注释，通常使用邮箱地址。 |
   | `-f ~/.ssh/sunmao_cluster_key` | 指定密钥文件的保存路径和名称。 |
2. 当提示 `Enter passphrase (empty for no passphrase)` 时，请直接按回车键留空即不设置密码。
3. 命令执行完成后，密钥对将在指定位置生成：

   - 私钥文件位于 `~/.ssh/sunmao_cluster_key`，私钥是敏感信息，请妥善保管，不要泄露给他人。
   - 公钥文件位于 `~/.ssh/sunmao_cluster_key.pub`，需配置到集群中所有节点中。

### 配置公钥到目标节点

节点中的 `~/.ssh/authorized_keys` 文件用于存储允许访问的公钥，参考本节内容将公钥配置到所有节点后，SSH 将自动采用密钥登录，不再提示输入密码。

1. 将公钥内容复制到目标节点的 `~/.ssh/authorized_keys` 文件中，按需选择如下任一方式：

   通过 ssh-copy-id 工具自动分发手动配置

   ```
   ssh-copy-id -i ~/.ssh/sunmao_cluster_key.pub <username>@<node_ip>
   ```

   ```
   cat ~/.ssh/sunmao_cluster_key.pub | ssh <username>@<node_ip> "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
   ```

   | 参数 | 说明 |
   | --- | --- |
   | `<username>` | SSH 用户名，需为 root 用户或具有 root 权限的其他用户。 |
   | `<node_ip>` | 集群节点的 IP 地址。 |
2. 设置目标节点上 `~/.ssh/authorized_keys` 文件及其所在目录的权限：

   ```
   ssh <username>@<node_ip> "chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"
   ```

### 检查 SSH 连接

在集群中所有节点执行以下命令测试 SSH 连接，确保每个节点都能正常连接。

1. 使用私钥测试 SSH 连接：

   ```
   ssh -i ~/.ssh/sunmao_cluster_key <username>@<node_ip>
   ```

   预期无需输入密码即可成功登录，表示 SSH 密钥配置正确。
2. 非 root 用户需测试 root 权限：

   ```
   ssh -i ~/.ssh/sunmao_cluster_key <username>@<node_ip> "sudo whoami"
   ```

   预期返回 `root`，表示该用户具有 sudo 权限。

### 获取私钥内容

创建集群前请通过以下命令获取私钥内容：

```
cat ~/.ssh/sunmao_cluster_key
```

私钥内容格式类似于：

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAACFwAAAAdzc2gtcn
...
-----END OPENSSH PRIVATE KEY-----
```

注意：

- 私钥是敏感信息，请妥善保管，不要泄露给他人。
- 确保私钥文件的权限为 600（`chmod 600 ~/.ssh/sunmao_cluster_key`），否则 SSH 服务器可能会拒绝使用该密钥。

## 创建集群

1. 登录 AI 平台管理界面，在左侧菜单栏中单击**集群**，在右侧页面单击**创建**。
2. 填写配置信息。

   - **基础信息**

     | 参数 | 描述 | 创建后是否允许编辑 |
     | --- | --- | --- |
     | 名称 | 集群的名称。 | 否 |
     | 工作空间 | 集群所属的工作空间。 | 否 |
   - **镜像仓库**

     为集群选择镜像仓库，用于存放集群相关的容器镜像。若没有可选的镜像仓库，请参考[创建容器镜像仓库](/smtx-ai/1.0.0/user_guide/infrastructure/image-registry#%E5%88%9B%E5%BB%BA%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F%E4%BB%93%E5%BA%93)小节创建。集群创建后不允许编辑。
   - **集群类型**

     集群的类型，选择**静态节点**。集群创建后不允许编辑。
   - **提供商**

     | 参数 | 描述 | 创建后是否允许编辑 |
     | --- | --- | --- |
     | 头节点 IP | 头节点的 IP 地址。 | 否 |
     | 工作节点 IP | 工作节点的 IP 地址。 - 单节点集群无需填写此项。 - 多节点集群输入一个 IP 后单击 **+ 添加**即可添加下一个 IP。 | 是 |
   - **节点认证**

     | 参数 | 描述 | 创建后是否允许编辑 |
     | --- | --- | --- |
     | SSH 用户 | SSH 用户名，需为 root 用户或具有 root 权限的其他用户。 | 否 |
     | SSH 私钥 | SSH 私钥字符串。可以参考[准备 SSH 私钥](#%E5%87%86%E5%A4%87-ssh-%E7%A7%81%E9%92%A5)小节获取。 | 否 |
   - **模型缓存**

     | 参数 | 描述 | 创建后是否允许编辑 |
     | --- | --- | --- |
     | 名称 | 模型缓存名称。 | 否 |
     | 缓存类型 | 静态节点集群仅支持 **Host Path**。 | 否 |
     | 缓存路径 | 模型缓存的主机路径。 | 是 |

     若创建时未配置模型缓存，集群创建后不允许添加模型缓存。
3. 确认配置信息无误后，单击**保存**完成创建。

## 查看集群

登录 AI 平台管理界面，在左侧菜单栏中单击**集群**，右侧集群列表将展示当前所有集群，单击集群名称即可查看详情。

在详情页面可以按需查看**基础信息**、**监控**和 **Ray 仪表盘**。

## 编辑集群

集群创建后，您可以根据实际需求修改集群工作节点的配置和模型缓存路径。

1. 登录 AI 平台管理界面，在集群列表或详情页面单击菜单图标（**...**），选择**编辑**。
2. 在配置页面按需修改，具体参数说明请参考[创建集群](#%E5%88%9B%E5%BB%BA%E9%9B%86%E7%BE%A4)。
3. 确认配置信息无误后，单击**保存**完成编辑。

## 删除集群

1. 登录 AI 平台管理界面，在集群列表或详情页面单击菜单图标（**...**），选择**删除**。
2. 在弹出的对话框中，二次确认后单击**删除**，集群将被永久删除。

---

## 管理基础设施 > 管理集群 > 管理 Kubernetes 集群

# 管理 Kubernetes 集群

## 配置加速器

若 Kubernetes 节点包含加速器，请根据加速器类型完成相应配置。

NVIDIA GPUAMD GPU昇腾 NPU

与 SKS 配合使用时，请在 CloudTower 中为 SKS 工作负载集群启用 NVIDIA GPU Operator 插件，详情请参考《SMTX Kubernetes 服务管理指南》的**配置集群插件**章节。

与其他标准 Kubernetes 集群配合使用时，请参考 [NVIDIA 官方文档](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html)《NVIDIA GPU Operator》中 *Installing the NVIDIA GPU Operator* 章节安装 NVIDIA GPU Operator。

请参考 [AMD 官⽅文档](https://rocm.docs.amd.com/en/latest/)进行如下配置：

1. 当前集群镜像支持的 ROCM 软件版本为 6.3.3，请安装对应版本的 AMDGPU driver。请参考 *AMD ROCm documentation* 中 **AMDGPU driver installation** 章节。
2. 当前集群镜像支持的 ROCM 软件版本为 6.3.3，请安装对应版本的 AMD GPU Device Plugin。请参考 *Device Plugin Documentation* 中 **AMD GPU Device Plugin for Kubernetes** 章节。

请参考[昇腾官方文档](https://www.hiascend.com/document)进行如下配置：

1. 安装 CANN 版本为 8.1.RC1 的昇腾 310P3 NPU 驱动和固件包。请参考《CANN 软件安装指南》中**安装 NPU 驱动和固件**章节。
2. 安装 7.0.RC1 版本 Ascend Docker Runtime。请参考《CANN 软件安装指南》中**安装 Ascend Docker Runtime** 章节。
3. 安装 7.0.RC1 版本 Ascend Device Plugin。请参考《组件安装》中手动安装 **Ascend Device Plugin** 章节。

## 创建集群

1. 登录 AI 平台管理界面，在左侧菜单栏中单击**集群**，在右侧页面单击**创建**。
2. 填写配置信息。

   - **基础信息**

     | 参数 | 描述 | 创建后是否允许编辑 |
     | --- | --- | --- |
     | 名称 | 集群的名称。 | 否 |
     | 工作空间 | 集群所属的工作空间。 | 否 |
   - **镜像仓库**

     为集群选择镜像仓库，用于存放集群相关的容器镜像。若没有可选的镜像仓库，请参考[创建容器镜像仓库](/smtx-ai/1.0.0/user_guide/infrastructure/image-registry#%E5%88%9B%E5%BB%BA%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F%E4%BB%93%E5%BA%93)小节创建。集群创建后不允许编辑。
   - **集群类型**

     集群的类型，选择 **Kubernetes**。集群创建后不允许编辑。
   - **提供商**

     填入集群的 Kubeconfig 字符串，用于访问 Kubernetes 集群。集群创建后不允许编辑。
   - **路由**

     | 参数 | 描述 | 创建后是否允许编辑 |
     | --- | --- | --- |
     | 访问模式 | 路由组件的访问模式：**LoadBalancer** 和 **NodePort**。 选择 **LoadBalancer** 时需要确保 Kubernetes 集群支持 LoadBalancer 服务。 | 是 |
     | 副本数 | 路由组件的副本数。推荐至少设置为 2，以支持高可用。 | 是 |
     | CPU | 路由组件 CPU 数量。 | 是 |
     | 内存 | 路由组件内存容量。 | 是 |
   - **模型缓存**

     | 参数 | 描述 | 创建后是否允许编辑 |
     | --- | --- | --- |
     | 名称 | 模型缓存名称。 | 否 |
     | 缓存类型 | 支持的缓存类型： - **Host Path**：本地缓存。 - **NFS**：NFS 缓存。 - **PVC**：持久化存储，仅支持 ReadWriteMany。 | 是 |
     | 缓存路径 | 模型缓存的路径。 - 缓存类型为 **Host Path** 时需指定主机路径。 - 缓存类型为 **NFS** 时需指定 NFS 服务器路径。 - 缓存类型为 **PVC** 时无需配置此项。 | 是 |
     | NFS 服务器地址 | NFS 服务器的 IP 地址或域名，仅缓存类型为 **NFS** 时需要配置。 | 是 |
     | 存储 | 指定用于模型缓存的存储容量，仅缓存类型为 **PVC** 时需要配置。 | 是 |
     | 存储类名称 | 指定用于模型缓存的存储类名称，仅缓存类型为 **PVC** 时需要配置。 | 否 |

     若创建时未配置模型缓存，集群创建后允许添加模型缓存。
3. 确认配置信息无误后，单击**保存**完成创建。

## 查看集群

登录 AI 平台管理界面，在左侧菜单栏中单击**集群**，右侧集群列表将展示当前所有集群，单击集群名称即可查看详情。

在详情页面可以按需查看**基础信息**和**监控**。

## 编辑集群

集群创建后，您可以根据实际需求修改集群的路由和模型缓存的部分配置。

1. 登录 AI 平台管理界面，在集群列表或详情页面单击菜单图标（**...**），选择**编辑**。
2. 在配置页面按需修改，具体参数说明请参考[创建集群](#%E5%88%9B%E5%BB%BA%E9%9B%86%E7%BE%A4)。
3. 确认配置信息无误后，单击**保存**完成编辑。

## 删除集群

1. 登录 AI 平台管理界面，在集群列表或详情页面单击菜单图标（**...**），选择**删除**。
2. 在弹出的对话框中，二次确认后单击**删除**，集群将被永久删除。

---

## 管理模型服务 > 基本概念

# 基本概念

模型是 AI 负载的核心资源，推理是 AI 平台核心的 AI 负载类型。

## 模型仓库

模型仓库用于存放模型，AI 平台支持 **Hugging Face** 类型的公有模型仓库和基于**文件系统**的私有模型仓库。

## 模型目录

模型目录集合了常用模型的最佳实践参数，预设了推理引擎、资源规格与运行参数，旨在实现模型部署标准化，降低运维成本。

## 推理引擎

推理引擎是 AI 平台内置的、用于运行模型的代码框架，包含多种可配置参数，提供模型加载、加速器适配、推理优化、OpenAI 兼容 API 等功能。

## 推理实例

推理实例是模型推理服务的具体部署实体，每个推理实例对应一个独立的推理服务，可对外提供 OpenAI 兼容的 API 接口。一个推理实例内包含模型选择、推理引擎配置以及推理参数设置等完整的推理服务运行环境。

---

## 管理模型服务 > 管理模型仓库

# 管理模型仓库

模型仓库用于存放模型，分为以下两种类型：

- **[Hugging Face](https://huggingface.co/) 模型仓库**是公有模型仓库，提供丰富的模型资源。

  部署推理实例时选择 Hugging Face 模型仓库，推理引擎将自动从 Hugging Face 拉取开源模型，缓存至本地后使用。
- **文件系统模型仓库**是私有模型仓库，适用于存放企业内部开发的专有模型或经过定制化的第三方模型。文件系统模型仓库提供更高的安全性和可控性。此版本的文件系统模型仓库基于 NFS 实现，后续版本将支持本地文件系统。

  部署推理实例时选择文件系统模型仓库，推理引擎将直接从文件系统中读取模型。

## 创建模型仓库

1. 登录 AI 平台管理界面，在左侧菜单栏中单击**模型仓库**，在右侧页面单击**创建**。
2. 填写配置信息。

   | 参数 | 描述 | 创建后是否允许编辑 |
   | --- | --- | --- |
   | 名称 | 模型仓库的名称。 | 否 |
   | 工作空间 | 模型仓库所属的工作空间。 | 否 |
   | 类型 | 模型仓库的类型：**Hugging Face** 和**文件系统**。 | 是 |
   | URL | 模型仓库的地址。 - 对于 **Hugging Face** 模型仓库，请填入 Hugging Face Hub 地址。可以使用标准的 Hugging Face URL `https://huggingface.co/` ，也可以使用 Hugging Face 兼容的镜像 URL，例如 `https://hf-mirror.com/`。 - 对于**文件系统**模型仓库，使用 NFS 作为模型仓库，格式为 `nfs://$NFS_IP:/$PATH_TO_DIR`。当前支持 NFSv3 和 NFSv4.x 协议。 | 是 |
   | 凭据 | Hugging Face 模型仓库需填入 HF token 即 Hugging Face 用户访问令牌，请参考 [Hugging Face 官方文档](https://huggingface.co/docs/hub/en/security-tokens#how-to-manage-user-access-tokens)获取。 | 是 |
3. 确认配置信息无误后，单击**保存**完成创建。

## 查看模型仓库

登录 AI 平台管理界面，在左侧菜单栏中单击**模型仓库**，右侧模型仓库列表将展示当前所有模型仓库，单击模型仓库名称即可查看详情。

## 编辑模型仓库

模型仓库创建后，您可以根据实际需求修改模型仓库的类型、URL 和凭据。

1. 登录 AI 平台管理界面，在模型仓库列表或详情页面单击菜单图标（**...**），选择**编辑**。
2. 在配置页面按需修改，具体参数说明请参考[创建模型仓库](#%E5%88%9B%E5%BB%BA%E6%A8%A1%E5%9E%8B%E4%BB%93%E5%BA%93)。
3. 确认配置信息无误后，单击**保存**完成编辑。

## 删除模型仓库

说明：

删除文件系统模型仓库时，不会删除对应目录下保存的模型。

**操作步骤**

1. 登录 AI 平台管理界面，在模型仓库列表或详情页面单击菜单图标（**...**），选择**删除**。
2. 在弹出的对话框中，二次确认后单击**删除**，模型仓库将被永久删除。

---

## 管理模型服务 > 管理模型

# 管理模型

创建模型仓库后，您可以根据模型仓库的类型选择不同的方式对模型仓库中的模型进行管理。

- **Hugging Face 模型仓库**：模型存储在 Hugging Face 平台上，请参考 [Hugging Face 官方文档](https://huggingface.co/docs/hub/models)管理模型。
- **文件系统模型仓库**：模型存储在本地中，请参考本章节使用榫卯 AI 平台命令行工具推送、查看或删除模型。您也可以[从 Hugging Face 下载模型](#%E4%BB%8E-hugging-face-%E4%B8%8B%E8%BD%BD%E6%A8%A1%E5%9E%8B)并将其推送至文件系统模型仓库中进行管理。

## 准备工作

在管理文件系统模型仓库中的模型前，需要完成以下准备工作：

1. 根据服务器的 CPU 架构下载对应的 AI 平台命令行工具安装文件。

   注意：

   榫卯 AI 平台命令行工具通过 HTTP API 与 AI 平台进行交互，请您确保命令行工具与 AI 平台间的网络连通。
2. 为命令行工具安装文件分配可执行权限。

   ```
   chmod +x neutree-cli-<arch>
   ```

   可以通过以下命令查看工具的使用帮助：

   ```
   neutree-cli-<arch> model -h
   ```
3. [创建 API 密钥](/smtx-ai/1.0.0/user_guide/access-control/api-key#%E5%88%9B%E5%BB%BA-api-%E5%AF%86%E9%92%A5)并妥善保存。

## 推送模型

使用 AI 平台命令行工具将本地模型推送至文件系统模型仓库：

```
neutree-cli-<arch> model push <local_model_dir> \
  -n <model_name> \
  -d [model_description] \
  -v [model_version] \
  -r <model_registry> \
  -w [workspace] \
  --api-key <api_key> \
  --server-url <server_url>
```

参数描述如下：

| 参数 | 描述 |
| --- | --- |
| `<local_model_dir>` | 本地模型所在的目录。 |
| `<model_name>` | 模型在模型仓库中存储的名称。文件系统模型仓库的模型名称暂不支持 `/`，请调整为其他字符，例如 `_`。若创建推理模型时使用模型目录，请确保此处设置的模型名称与模型目录中的模型名称一致。 |
| `[model_description]` | 模型的描述，选填。 |
| `[model_version]` | 模型的版本，选填，留空时系统将自动生成。在模型仓库中，同一名称的模型可以拥有多个版本。 |
| `<model_registry>` | 目标模型仓库的名称。 |
| `[workspace]` | 工作空间的名称，选填，留空时默认使用 `default` 工作空间。 |
| `<api_key>` | 准备工作中创建的 API 密钥。 |
| `<server_url>` | 控制平面的访问地址，例如 `http://localhost:3000`。 |

## 查看模型

使用以下命令查看文件系统模型仓库中的模型：

```
neutree-cli-<arch> model list -r <model_registry> \
  -w [workspace] \
  --api-key <api_key> \
  --server-url <server_url>
```

参数描述如下：

| 参数 | 描述 |
| --- | --- |
| `<model_registry>` | 目标模型仓库的名称。 |
| `[workspace]` | 工作空间的名称，选填，留空时默认使用 `default` 工作空间。 |
| `<api_key>` | 准备工作中创建的 API 密钥。 |
| `<server_url>` | 控制平面的访问地址，例如 `http://localhost:3000`。 |

## 删除模型

使用以下命令删除文件系统模型仓库中的模型：

```
neutree-cli-<arch> model delete <model_name>:<model_version> \
  -r <model_registry> \
  -w [workspace] \
  --api-key <api_key> \
  --server-url <server_url>
```

参数描述如下：

| 参数 | 描述 |
| --- | --- |
| `<model_name>` | 模型在模型仓库中存储的名称。 |
| `<model_version>` | 模型的版本，若推送模型时未制定版本号，请先[查看模型版本](#%E6%9F%A5%E7%9C%8B%E6%A8%A1%E5%9E%8B)。 |
| `<model_registry>` | 目标模型仓库的名称。 |
| `[workspace]` | 工作空间的名称，选填，留空时默认使用 `default` 工作空间。 |
| `<api_key>` | 准备工作中创建的 API 密钥。 |
| `<server_url>` | 控制平面的访问地址，例如 `http://localhost:3000`。 |

## 从 Hugging Face 下载模型

文件系统模型仓库请跳过本节。

1. 安装 Hugging Face 命令行工具，请参考 [Hugging Face 官方文档](https://huggingface.co/docs/huggingface_hub/main/en/guides/cli)。
2. 登录 Hugging Face：

   ```
   hf auth login
   ```
3. 使用 `hf download` 命令下载模型到本地目录。以下是几个常用场景的示例：

   - **下载完整模型**

     将 Hugging Face 上的完整模型下载到本地目录，例如将 `Qwen/Qwen3-0.6B` 模型完整下载到 `./test-model` 目录。

     ```
     hf download Qwen/Qwen3-0.6B --local-dir ./test-model
     ```
   - **选择性下载特定文件**

     对于大型模型仓库，可以通过 `--include` 和 `--exclude` 参数精确控制下载内容，提高效率：

     - 只下载特定精度的模型。例如只下载 Q8.0 精度的 GGUF 模型：

       ```
       hf download microsoft/Phi-3-mini-4k-instruct-gguf \
         --include "*q8_0.gguf" \
         --local-dir ./phi3-q8
       ```
     - 下载多种类型的关键文件。例如下载 Q8.0 精度的模型及配置文件：

       ```
       hf download microsoft/Phi-3-mini-4k-instruct-gguf \
         --include "*q8_0.gguf" \
         --include "*.json" \
         --include "*.txt" \
         --local-dir ./phi3-q8
       ```
     - 排除不需要的大文件。例如下载 `Qwen/Qwen3-0.6B` 模型但排除大型权重文件：

       ```
       hf download Qwen/Qwen3-0.6B \
         --exclude "*.safetensors" \
         --exclude "pytorch_model.bin" \
         --local-dir ./qwen3-lightweight
       ```

模型下载至本地目录并完成[准备工作](#%E5%87%86%E5%A4%87%E5%B7%A5%E4%BD%9C)后，即可按需[推送](#%E6%8E%A8%E9%80%81%E6%A8%A1%E5%9E%8B)、[查看](#%E6%9F%A5%E7%9C%8B%E6%A8%A1%E5%9E%8B)或[删除](#%E5%88%A0%E9%99%A4%E6%A8%A1%E5%9E%8B)模型。

---

## 管理模型服务 > 管理模型目录

# 管理模型目录

模型目录是一组模型、推理引擎和推理实例的相关配置参数的集合，您可以通过选择模型目录快速创建推理实例，实现推理实例的模版化分发。

## 获取模型目录

经过验证的模型目录将发布至在线模型商店，您可以从模型商店获取最新的模型目录的 YAML 文件。

1. 访问[模型商店](https://neutree-ai.github.io/model-catalog/)，查看所有可用的模型目录，可以通过任务类型筛选模型目录。
2. 勾选所需的模型目录，单击 **Generate YAML**。
3. 弹出的 **Generated YAML Configuration** 窗口中将展示所选模型目录对应的 YAML 配置文件，单击 **Copy** 复制完整的 YAML 内容。

   说明：

   如需调整模型目录中的配置，可以在导入 AI 平台前使用文本编辑器修改 YAML 文件。

## 匹配模型名称

使用模型目录时，请确保 AI 平台模型仓库中存在与模型目录中配置相同且名称一致的模型。

Hugging Face 模型仓库文件系统模型仓库

确认模型目录中配置的模型名称与 Hugging Face 模型仓库中的模型名称一致。

1. 查看 Hugging Face 模型仓库中模型的名称。

   以 `https://huggingface.co/` 为例，可以通过模型卡片查看模型名称，模型名称的格式为 `$ORG/$MODEL`。例如 `https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B` 的模型名称为 `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`。
2. 查看模型目录的模型名称。查看 YAML 文件中 `.spec.model.name` 字段或查看 AI 平台管理界面展示的模型名称。
3. 确认模型目录中的模型名称与 Hugging Face 模型仓库中的模型名称一致。

   若不一致，请更新模型目录的 YAML 文件中 `.spec.model.name` 字段。

确认模型目录中配置的模型名称与[推送模型](/smtx-ai/1.0.0/user_guide/model-service/model-management#%E6%8E%A8%E9%80%81%E6%A8%A1%E5%9E%8B)时设置的模型名称一致。

- 若已有模型目录，希望在模型仓库中推送对应模型，请在[推送模型](/smtx-ai/1.0.0/user_guide/model-service/model-management#%E6%8E%A8%E9%80%81%E6%A8%A1%E5%9E%8B)时将 `<model_name>` 字段设置为模型目录中的模型名称。
- 若模型仓库中已有与模型目录相对应的模型，但名称不匹配，请更新模型目录的 YAML 文件中 `.spec.model.name` 字段。

## 导入模型目录

登录 AI 平台管理界面，单击**导入 YAML**，选择合适的导入方式导入模型目录 YAML 文件。详细内容请参考[导入 YAML](/smtx-ai/1.0.0/user_guide/yaml/yaml-import) 小节。

## 查看模型目录

登录 AI 平台管理界面，在左侧菜单栏中单击**模型目录**，右侧模型目录列表将展示当前导入的所有模型目录，单击模型目录名称即可查看详情。

## 编辑模型目录

如需调整已导入的模型目录的内容，请您在本地使用文本编辑器修改该模型目录的 YAML 文件，然后将修改后的 YAML 文件重新[导入](/smtx-ai/1.0.0/user_guide/yaml/yaml-import) AI 平台。

## 删除模型目录

1. 登录 AI 平台管理界面，在模型目录列表或详情页面单击菜单图标（**...**），选择**删除**。
2. 在弹出的对话框中，二次确认后单击**删除**，模型目录将被永久删除。

---

## 管理模型服务 > 管理推理引擎

# 管理推理引擎

AI 平台提供内置的推理引擎，不支持创建全新的推理引擎以及删除推理引擎。Kubernetes 类型集群支持为内置的推理引擎添加新版本。

## 查看推理引擎

登录 AI 平台管理界面，在左侧菜单栏中单击**推理引擎**，右侧推理引擎列表将展示平台内置的所有推理引擎，单击推理引擎名称，进入详情可以查看推理引擎支持的任务类型与参数。

当前默认支持的推理引擎：

| 名称 | 版本 | 描述 |
| --- | --- | --- |
| vllm | [v0.8.5](https://hub.docker.com/layers/vllm/vllm-openai/v0.8.5/images/sha256-6cf9808ca8810fc6c3fd0451c2e7784fb224590d81f7db338e7eaf3c02a33d33) | vLLM 社区 v0.8.5 版本，静态节点集群将默认使用该版本。 |
| [v0.11.2](https://hub.docker.com/layers/vllm/vllm-openai/v0.11.2/images/sha256-47a9896f86818fea323b2d38082758c62d9a0155d6fe6c4dbd7d735c556f680a) | vLLM 社区 v0.11.2 版本，kubernetes 集群将默认使用该版本。 |
| llama-cpp | [v0.3.7](https://github.com/abetlen/llama-cpp-python/releases/tag/v0.3.7) | Llama-cpp python High-level 实现（Llama-cpp commit: 794fe23f29fb40104975c91fe19f23798f7c726e）。 |
| mindie | [v2.0.0.rc.1](https://www.hiascend.com/document/detail/zh/mindie/20RC1/releasenote/releasenote_0001.html) | MindIE 官方提供的 v2.0.0.rc.1 社区版本。 |

## 新增推理引擎版本

仅 `Kubernetes` 类型集群支持新增推理引擎版本。

**操作步骤**

1. [创建 API 密钥](/smtx-ai/1.0.0/user_guide/access-control/api-key#%E5%88%9B%E5%BB%BA-api-%E5%AF%86%E9%92%A5)并妥善保存。
2. 根据服务器的 CPU 架构下载指定版本的 AI 平台命令行工具安装文件和指定的推理引擎版本包。
3. 通过命令行工具导入引擎版本包：

   从 Docker Hub 拉取从远程镜像仓库拉取

   `imageRegistry` 配置为 Docker Hub 时，仅需导入引擎版本的元数据，无需导入镜像。执行如下命令将自动从 Docker Hub 拉取推理引擎镜像。

   ```
   ./neutree-cli-<arch> import engine --skip-image-push \
   --package <engine_version_package> \
   --api-key <api_key> \
   --server-url <server_url>
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `<arch>` | 需替换为服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<engine_version_package>` | 推理引擎版本包名称，例如 `vllm-v0.8.5.tar.gz`。 |
   | `<api_key>` | 步骤 1 中创建的 API 密钥。 |
   | `<server_url>` | 控制平面的访问地址，例如 `http://localhost:3000`。 |

   ```
   ./neutree-cli-<arch> import engine [--skip-image-push] \
   --package <engine_version_package> \
   --mirror-registry <mirror_registry> \
   --registry-username <registry_username> \
   --registry-password <registry_password> \
   --api-key <api_key> \
   --server-url <server_url>
   ```

   | 参数 | 描述 |
   | --- | --- |
   | `[--skip-image-push]` | 可选参数，若镜像已存在于目标仓库、且您仅需上传版本元数据到平台时，可以配置此参数。 |
   | `<arch>` | 需替换为服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
   | `<engine_version_package>` | 推理引擎版本包名称，例如 `vllm-v0.8.5.tar.gz`。 |
   | `<mirror_registry>` | 镜像仓库地址。填入兼容 OCI 的镜像仓库地址，无需携带 https:// 前缀。 例如：指定镜像仓库地址为 `registry.smtx.io/neutree-ai`，镜像将被上传到 `registry.smtx.io/neutree-ai/vllm/vllm-openai:v0.XX.XX`。 仓库中需预先创建好对应的项目。 |
   | `<registry_username>` | 镜像仓库用户的用户名，需为具备上传镜像权限的用户。 |
   | `<registry_password>` | 镜像仓库用户的登录密码或访问密钥（例如 token）。 |
   | `<api_key>` | 步骤 1 中创建的 API 密钥。 |
   | `<server_url>` | 控制平面的访问地址，例如 `http://localhost:3000`。 |
4. 导入完成后，登录 AI 平台管理界面，在左侧菜单栏中单击**推理引擎**，确认推理引擎列表中存在新增的引擎版本。

---

## 管理模型服务 > 管理推理实例

# 管理推理实例

建议您使用模型目录创建推理实例，AI 平台会自动填充模型目录中相关配置，按需修改后即可快速创建推理实例。AI 平台也支持不选择模型目录，手动填写推理实例配置参数。

## 创建推理实例

1. 登录 AI 平台管理界面，在左侧菜单栏中单击**推理实例**，在右侧页面单击**创建**。
2. 填写配置信息。

   | 参数 | 描述 | 创建后是否允许编辑 |
   | --- | --- | --- |
   | 名称 | 推理实例的名称。 | 否 |
   | 工作空间 | 推理实例所属的工作空间。 | 否 |
   | 集群 | 推理实例所属的集群。 | 是 |
   | 模型仓库 | 推理实例所属的模型仓库。 | 是 |
   | 模型目录（模板） | 可选项。 - 为推理实例选择模型目录后，该模型目录所内置的参数填充至自定义配置信息中，按需修改即可。 - 未选择模型目录时，需自行填写模型配置。 | 否 |
   | CPU | 分配给模型的 CPU 核心数。 | 是 |
   | 内存 | 分配给模型的内存容量。 | 是 |
   | 加速卡 | 分配给模型的加速卡类型及型号。 | 是 |
   | 加速器数量 | 分配给模型的加速卡数量配置。静态节点集群支持逻辑切分，可配置 <1 的数量。 | 是 |

   注意：

   使用模型目录时，请确保模型仓库中存在与模型目录配置相匹配的模型，否则可能导致实例创建失败。
3. 单击**自定义设置**，按需填写自定义配置信息。

   若已在基础配置中指定了模型目录，自定义配置信息中将自动填充该模型目录内置的参数，按需编辑即可，此处的修改不会对模型目录产生影响。若未指定模型目录，按需填写自定义配置即可。

   - **模型设置**

     | 参数 | 描述 | 创建后是否允许编辑 |
     | --- | --- | --- |
     | 模型名称 | 推理实例使用的模型的名称。 | 是 |
     | 模型版本 | 推理实例使用的模型的版本。  对于多版本模型，您可以按需自定义具体的版本。  此项留空时，AI 平台将自动使用最新的模型版本：Hugging Face 模型仓库为 main version，文件系统模型仓库为 latest version。 | 是 |
     | 模型文件 | 推理实例使用的模型文件，请填入模型文件夹中的入口文件。 - **safetensors** 类型的模型不需要填写此项。 - **GGUF** 类型的模型，需要选择所需的量化版本的 GGUF 文件作为入口文件，例如 8 bit 量化版本，则选择 `*8_0.gguf` 结尾的文件作为入口文件。 | 是 |
   - **引擎设置**

     | 参数 | 描述 | 创建后是否允许编辑 |
     | --- | --- | --- |
     | 引擎 | 推理实例的推理引擎。 - **vllm**：主流的开源推理引擎，具备高效的模型推理能力，适用于 NVIDIA GPU、AMD GPU 场景。 - **llama-cpp**：轻量级推理引擎，适用于纯 CPU 场景，需使用 `GGUF` 格式的模型。 - **mindie**：针对昇腾 NPU 优化的推理引擎，适用于昇腾 NPU 场景。 | 是 |
     | 引擎版本 | 推理实例的引擎版本。默认填充最新版本，可以按需选择具体的版本。  静态节点集群使用 vLLM 引擎时，仅支持选择 v0.8.5 版本。 | 是 |
     | 任务类型 | 推理实例的任务类型。一个推理实例可能支持多种任务类型，需根据所用模型选择与之匹配的任务类型。 - **文本生成**：即最常见的 LLM 推理场景。 - **文本嵌入**：生成文本的向量表示，常用作文本相似度计算。 - **文本重排序**：根据文本相似度对文本进行排序，常用作搜索结果重排序。 | 是 |
   - **副本设置**

     | 参数 | 描述 | 创建后是否允许编辑 |
     | --- | --- | --- |
     | 副本数 | 推理实例的副本策略。通过多副本实现推理实例的高可用，每个副本均占用一份资源设置。 | 是 |
     | 调度器类型 | 使用 vLLM 推理引擎时，推荐使用**一致性哈希**策略，调度器将感知引擎中的 KVCache 分布，智能优化推理请求路由，有效提升 KVCache 命中率。 其余场景推荐使用**轮询**策略，保持负载均匀。 | 是 |
   - **高级选项**

     - 引擎变量：可以选择引擎中定义的参数，也可以输入自定义的键、值。推理实例创建后允许编辑已有引擎变量，也可以添加新的键值对。
     - 环境变量：可以输入自定义的键、值。推理实例创建后允许编辑已有环境变量，也可以添加新的键值对。
4. 确认配置信息无误后，单击**保存**完成创建。

## 查看推理实例

登录 AI 平台管理界面，在左侧菜单栏中单击**推理实例**，右侧推理实例列表将展示当前所有推理实例，单击推理实例名称即可查看详情。在详情页面可以按需查看**基础信息**、**Ray 仪表盘**、**监控**、**日志**和**测试平台**。

### 获取 API URL

在详情页面的**基本信息**页签中，**服务地址**即外部服务调用此推理实例的 `API URL`，为任意兼容 OpenAI API 的客户端[创建 API 密钥](/smtx-ai/1.0.0/user_guide/access-control/api-key#%E5%88%9B%E5%BB%BA-api-%E5%AF%86%E9%92%A5)后客户端即可通过 API 密钥调用此 API URL 进行集成。

说明：

使用 API URL 时请务必在 URL 后添加 `/v1`。

例如通过 API 查看推理实例的模型：

```
curl  <API_URL>/v1/models \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer <api_key>'
```

### 查看监控与日志

AI 平台提供了 Ray 仪表盘、监控和日志帮助您掌握推理实例的运行状态和性能指标，从而及时发现和解决问题。

- **Ray 仪表盘**：仅静态节点集群中提供 Ray 仪表盘。在详情页面选择 **Ray 仪表盘**页签即可查看推理实例的 Ray 仪表盘的信息，通过 Ray 仪表盘可以跟踪应用程序的性能，用于监控和调试 Ray 应用程序。
- **监控**：在详情页面选择**监控**页签即可查看推理实例的实时的监控信息，可以筛选监控数据的时间范围，还可以设置自动刷新监控数据的频率。对于使用 vLLM 引擎的推理实例，还可以进一步查看 vLLM 引擎上报的监控数据。
- **日志**：在详情页面选择**日志**页签即可查看推理实例的应用日志、错误输出和标准输出，可以通过关键词和时间范围快速筛选日志，并支持日志下载。

### 快速测试

AI 平台提供了测试平台，您可以快速验证推理实例的功能是否正常，以及模型效果是否符合预期，从而及时调整推理实例的配置。

在详情页面选择**测试平台**页签，平台将根据推理实例的任务类型展示对应的测试界面。

- 对于**文本生成**任务，将展示对话窗口，用于测试推理 API 的基本功能。
- 对于**文本嵌入**任务，将展示一组可编辑的文本，单击**生成**后，将展示生成的文本向量之间的相似度关系。
- 对于**文本重排序**任务，将展示一个可编辑的提示词以及一组可编辑的相关文本，单击**生成**后，将展示文本与提示词之间的关联性重排结果。

## 编辑推理实例

推理实例创建后，您可以根据实际需求修改推理实例的资源、模型、引擎、副本以及高级选项配置。

1. 登录 AI 平台管理界面，在推理实例列表或详情页面单击菜单图标（**...**），选择**编辑**。
2. 在配置页面按需修改，具体参数说明请参考[创建推理实例](#%E5%88%9B%E5%BB%BA%E6%8E%A8%E7%90%86%E5%AE%9E%E4%BE%8B)。
3. 确认配置信息无误后，单击**保存**完成编辑。

## 暂停推理实例

当推理实例暂时不需要使用时，您可以通过暂停操作释放推理实例占用的资源。暂停推理实例后，其占用的加速器资源（如 GPU、NPU 等）、CPU 和内存资源将被释放，您可以将这些资源分配给其他推理实例或应用使用。暂停期间，推理实例的配置、模型文件和历史记录将被完整保留，您可以随时恢复推理实例以继续提供推理服务。

说明：

推理实例暂停后将无法对外提供推理服务，请确保在暂停前已通知相关用户或系统。

**操作步骤**

1. 登录 AI 平台管理界面，在推理实例列表或详情页面单击菜单图标（**...**），选择**暂停**。推理实例将进入暂停状态，资源将被释放。
2. 查看推理实例的状态已更新为`暂停中`。

**后续操作**

如需恢复推理实例，在推理实例列表或详情页面单击菜单图标（**...**），选择**恢复**，推理实例将被重新分配资源并恢复运行。

## 删除推理实例

1. 登录 AI 平台管理界面，在推理实例列表或详情页面单击菜单图标（**...**），选择**删除**。
2. 在弹出的对话框中，二次确认后单击**删除**，推理实例将被永久删除。

---

## 管理访问控制 > 基本概念

# 基本概念

AI 平台通过工作空间策略，将用户加入特定工作空间以限制用户的资源范围，为用户选择角色以限制用户对资源范围内资源的操作权限，提供安全、标准、功能完整的用户认证和权限管理能力。

外部程序可以通过集成 AI 平台，程序化的使用 AI 平台提供的能力。

## 用户

用户是 AI 平台中的基本身份实体，可以通过配置工作空间策略使同一个用户在不同的工作空间中拥有不同的角色。

## 角色

角色定义了一组操作权限的集合，用于控制用户可以执行的操作。

## 工作空间

工作空间是实现资源隔离的核心，用于控制不同用户对资源的可见性和访问权限。

## 工作空间策略

工作空间策略描述了用户、角色、工作空间三者之间的关联关系。

## API 密钥

API 密钥是外部程序访问 AI 平台的凭据，每个 API 密钥的权限与创建 API 密钥的用户的权限一致。

## AI 网关

AI 平台内置一个 AI 网关作为所有推理实例 API 的接入点。AI 网关提供基于 API 密钥的鉴权以及用量统计能力。

---

## 管理访问控制 > 应用场景

# 应用场景

本节介绍 AI 平台用户管理功能的典型应用场景，帮助您根据实际业务需求合理配置用户权限。

## 单一管理员

适用于小型团队、个人开发者，仅需要一名管理员负责所有操作的场景，此时使用 AI 平台初始管理员即可。

## 权限分离

适用于中大型团队，需要根据岗位职责分离不同权限，提高系统安全性和管理规范性的场景。您可以通过创建不同类型的角色，将平台管理、业务开发和审计监控等职责分离：

- **管理员**：全局管理员权限，负责平台的整体管理和维护。
- **开发者**：特定工作空间的推理实例操作权限，负责模型部署和推理服务管理。
- **审计员**：全局只读权限，负责监控和审计平台活动，不具备修改权限。

**示例**

1. 管理员在**用户**页面创建多个用户:
   - 用户 A
   - 用户 B
2. 管理员在**角色**页面创建自定义角色：
   - "开发者"角色，分配推理实例的创建、编辑、删除等权限。
   - "审计员"角色，仅分配各模块的查看权限。
3. 在**工作空间策略**页面为不同用户配置相应权限：
   - 为用户 A 配置全局策略和"开发者"角色。
   - 为用户 B 配置全局策略和"审计员"角色。

## 多租户隔离

适用于需要为不同团队、部门或外部客户提供独立 AI 服务，同时保证数据隔离和资源安全的场景。您可以通过工作空间实现多租户隔离，每个租户拥有独立的资源与模型空间，确保业务之间互不干扰，数据安全可控。

- **管理员**：拥有全局管理员权限，负责平台基础设施和多租户架构的搭建。
- **租户 A**：仅在工作空间 A 中拥有特定操作权限。
- **租户 B**：仅在工作空间 B 中拥有特定操作权限。

**示例**

1. 管理员在**工作空间**页面创建多个工作空间。

   - 工作空间 A
   - 工作空间 B
2. 管理员在**用户**页面创建多个用户。

   - 用户 1
   - 用户 2
   - ···
   - 用户 n
3. 管理员在**角色**页面创建"开发者"角色，分配推理实例的创建、编辑、删除等权限。
4. 在**工作空间策略**页面为不同用户配置相应权限：

   - 为部分用户配置工作空间 A 和"开发者"角色。
   - 为其他用户配置工作空间 B 和"开发者"角色。

---

## 管理访问控制 > 管理用户

# 管理用户

## 创建用户

管理员可以按照如下操作步骤创建用户：

1. 登录 AI 平台管理界面，在左侧菜单栏中单击**用户**，在右侧页面单击**创建**。
2. 填写配置信息。

   | 参数 | 描述 | 创建后是否允许编辑 |
   | --- | --- | --- |
   | 姓名 | 用户的名称。 | 否 |
   | 邮箱 | 用户的邮箱，用于登录 AI 平台。 | 是，仅管理员可编辑。 |
   | 密码 | 用户的密码，用于登录 AI 平台。 | 是，仅用户自己可编辑。 |
   | 确认密码 | 再次确认用户的密码。 | - |
3. 确认配置信息无误后，单击**保存**完成创建。

## 查看用户

登录 AI 平台管理界面，在左侧菜单栏中单击**用户**，右侧用户列表将展示当前所有用户，单击用户名称进入详情还可以查看当前用户的全局角色以及在特定工作空间中的角色。

## 编辑用户

用户创建后，管理员可以修改所有用户的邮箱，但密码只能由用户自己修改。

### 修改邮箱

1. 登录 AI 平台管理界面，管理员在用户列表或详情页面单击菜单图标（**...**），选择**编辑**。
2. 在配置页面修改用户的邮箱。
3. 确认配置信息无误后，单击**保存**完成编辑。

### 修改密码

1. 登录 AI 平台管理界面，单击界面右上角用户名称所在下拉菜单，然后单击**更新密码**。
2. 在**设置新密码**页面输入新密码并进行二次确认。
3. 单击**更新**完成编辑。

## 删除用户

1. 登录 AI 平台管理界面，在用户列表或详情页面单击菜单图标（**...**），选择**删除**。
2. 在弹出的对话框中，二次确认后单击**删除**，用户及其所有相关配置将被永久删除。

---

## 管理访问控制 > 管理角色

# 管理角色

角色定义了一组操作权限的集合，用于限制用户允许执行的操作。角色分为以下两种类型：

- **内置角色**：平台内置**管理员角色**，该角色拥有平台的所有操作权限，不允许编辑和删除。
- **自定义角色**：管理员根据业务需求创建的角色，可以灵活配置权限。

## 创建自定义角色

1. 登录 AI 平台管理界面，在左侧菜单栏中单击**角色**，在右侧页面单击**创建**。
2. 填写角色的**名称**。角色创建后不允许编辑。
3. 为该角色分配**权限**。权限按功能模块分组显示，单击允许该角色执行的权限即可完成选择。角色创建后允许编辑。
4. 确认配置信息无误后，单击**保存**完成创建。

## 查看角色

登录 AI 平台管理界面，在左侧菜单栏中单击**角色**，右侧角色列表将展示当前所有角色的信息，单击角色名称进入详情即可查看详细的权限配置。

## 编辑角色

角色创建后，您可以根据实际需求修改角色的权限。

1. 登录 AI 平台管理界面，在角色列表或详情页面单击菜单图标（**...**），选择**编辑**。
2. 在配置页面按需修改，具体参数说明请参考[创建自定义角色](#%E5%88%9B%E5%BB%BA%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%92%E8%89%B2)。
3. 确认配置信息无误后，单击**保存**完成编辑。

## 删除角色

1. 登录 AI 平台管理界面，在角色列表或详情页面单击菜单图标（**...**），选择**删除**。
2. 在弹出的对话框中，二次确认后单击**删除**，角色将被永久删除。

---

## 管理访问控制 > 管理工作空间

# 管理工作空间

工作空间是 AI 平台资源隔离和权限控制的核心概念。

- 集群、模型仓库、模型目录、容器镜像仓库、推理引擎、推理实例均只能归属于一个工作空间，从而实现了资源隔离。
- 将用户添加至特定工作空间，并分配角色。用户只能查看和操作已加入工作空间内的资源，实现不同用户或团队对资源的访问和操作权限。

AI 平台会自动创建名为 `default` 的默认工作空间。对于单一用户或小规模使用场景，使用默认工作空间即可满足需求。

## 创建工作空间

1. 登录 AI 平台管理界面，在左侧菜单栏中单击**工作空间**，在右侧页面单击**创建**。
2. 填写工作空间的**名称**。工作空间创建后不允许编辑。
3. 确认名称无误后，单击**保存**完成创建。

## 查看工作空间

登录 AI 平台管理界面，在左侧菜单栏中单击**工作空间**，右侧工作空间列表将展示当前所有工作空间，单击工作空间名称进入详情还可以查看加入该工作空间的用户及其角色。

## 删除工作空间

1. 登录 AI 平台管理界面，在工作空间列表或详情页面单击菜单图标（**...**），选择**删除**。
2. 在弹出的对话框中，二次确认后单击**删除**，工作空间将被永久删除。

---

## 管理访问控制 > 管理工作空间策略

# 管理工作空间策略

工作空间策略通过建立用户、角色和工作空间三者的关联关系，限制用户在特定工作空间内的操作权限，实现细粒度的权限控制。

## 创建工作空间策略

1. 登录 AI 平台管理界面，在左侧菜单栏中单击**工作空间策略**，在右侧页面单击**创建**。
2. 填写配置信息。

   | 参数 | 描述 | 创建后是否允许编辑 |
   | --- | --- | --- |
   | 名称 | 工作空间策略的的名称。 | 否 |
   | 用户 | 待分配权限的目标用户。 | 是 |
   | 角色 | 用户在工作空间中的角色。 | 是 |
   | 策略范围 | 工作空间策略的生效范围。 - **全局**表示对所有工作空间生效，通常用于管理员或需要跨工作空间操作权限的用户。 - **工作空间**表示仅在指定的工作空间内生效。 | 是 |
   | 工作空间 | 策略范围选择**工作空间**时需指定适用该策略的工作空间。 | 是 |

   说明：

   用户同时拥有全局权限和工作空间权限时，实际权限为全局权限和工作空间权限的**并集**。
3. 确认配置信息无误后，单击**保存**完成创建。

## 查看工作空间策略

登录 AI 平台管理界面，在左侧菜单栏中单击**工作空间策略**，右侧工作空间策略列表将展示当前所有工作空间策略的信息，单击工作空间策略名称即可查看详情。

## 编辑工作空间策略

工作空间策略创建后，您可以根据实际需求修改策略中配置的用户、角色、策略范围和工作空间。

1. 登录 AI 平台管理界面，在工作空间策略列表或详情页面单击菜单图标（**...**），选择**编辑**。
2. 在配置页面按需修改，具体参数说明请参考[创建工作空间策略#创建工作空间策略)。
3. 确认配置信息无误后，单击**保存**完成编辑。

## 删除工作空间策略

1. 登录 AI 平台管理界面，在工作空间策略列表或详情页面单击菜单图标（**...**），选择**删除**。
2. 在弹出的对话框中，二次确认后单击**删除**，工作空间策略将被永久删除。

---

## 管理访问控制 > 管理 API 密钥

# 管理 API 密钥

API 密钥是用户调用推理实例 API 和 AI 平台控制平面 API 时的凭据。

API 密钥将继承创建者在对应工作空间中的权限。用户调用控制平面 API 时，平台将根据 API 密钥的权限进行鉴权。用户调用推理实例 API 时，平台将根据 API 密钥进行用量统计。

## 创建 API 密钥

为确保您在权限管理和用量统计时实现更细粒度的控制能力，建议您为不同的 AI 应用创建不同的 API 密钥。

1. 登录 AI 平台管理界面，在左侧菜单栏中单击 **API 密钥**，在右侧页面单击**创建**。
2. 为 API 密钥选择**工作空间**并填写**名称**，API 密钥创建后不允许编辑。
3. 确认配置信息无误后，单击**保存**完成创建。

注意：

API 密钥内容创建后将无法再次查看，请及时复制并妥善保存。

## 查看 API 密钥

登录 AI 平台管理界面，在左侧菜单栏中单击 **API 密钥**，右侧 API 密钥列表将展示所有 API 密钥，单击 API 密钥名称进入详情，可以查看该 API 密钥的用量统计信息。

说明：

AI 平台每 5 分钟统计一次使用信息。用户调用 API 时，需完成一次聚合统计后，详情页内才会展示该用户的使用信息。

## 删除 API 密钥

1. 登录 AI 平台管理界面，在 API 密钥列表或详情页面单击菜单图标（**...**），选择**删除**。
2. 在弹出的对话框中，二次确认后单击**删除**，API 密钥将被永久删除。

---

## 管理 YAML 配置 > 导入 YAML

# 导入 YAML

您可以使用导入 YAML 功能快速创建资源。

1. 登录 AI 平台管理界面，在顶部单击**导入 YAML**。
2. 在弹出的**从 YAML 导入资源**对话框中，选择合适的导入方式导入 YAML 文件。

   - **上传 YAML 文件**：单击文件选择框，选择 `.yaml` 或 `.yml` 格式的文件。
   - **从 URL 导入**：在输入框中填入 YAML 文件的 URL，单击**获取**下载文件内容。
   - **粘贴 YAML 内容**：在文本框中直接输入或粘贴 YAML 内容。支持多文档 YAML 格式，请使用 `---` 分隔不同资源。
3. 单击**导入资源**后将显示导入进度，包括总资源数量和当前进度。
4. 导入完成后，将展示成功、跳过和错误的资源信息，每个资源的详细处理结果包含资源类型、名称和状态。

说明：

若已存在的同名资源会被自动**跳过**，不会覆盖。

---

## 管理 YAML 配置 > 导出 YAML

# 导出 YAML

您可以使用导出 YAML 功能批量迁移 AI 平台中的资源配置。

1. 登录 AI 平台管理界面，在顶部单击**导出 YAML**。
2. 选择需要导出的资源类型。

   - 单击资源类型名称右侧的展开按钮，可查看该类型下的具体资源实例并按需选择。
   - 单击资源类型名称左侧的复选框，可选择该类型下的所有资源实例。
   - 单击右上角的**全选**可快速选择所有类型的资源。
3. 设置导出选项。默认启用所有清理选项，表示仅生成可迁移的配置文件，您可以单击右上角的设置图标![设置图标](https://cdn.smartx.com/internal-docs/assets/d96ef1b4/yaml-export.png)按需禁用导出选项。
4. 单击**生成 YAML** 预览内容，确认无误后将其复制到剪贴板或下载为文件。

---

## 更新平台设置 > 自定义平台外观

# 自定义平台外观

管理员可以个性化定制 AI 平台的管理界面中展示的品牌名称和 Logo。

1. 登录 AI 平台管理界面，在左侧菜单栏中单击**自定义外观**。
2. 填写**品牌名称**。
3. 单击**上传 Logo** 选择品牌标识文件作为主要 Logo。当前支持 `PNG`、`JPG` 和 `SVG` 格式的图片文件。

   说明：

   为确保在各种显示场景下的最佳效果，图片尺寸推荐 64x64 px。
4. （可选）单击**上传折叠 Logo** 选择侧边栏折叠时显示的 Logo，通常为更简洁的、适合在有限的空间内显示的图标。若未上传折叠 Logo，AI 平台将自动使用主要 Logo 作为侧边栏折叠时的显示。
5. 确认无误后，单击**保存**完成创建。

---

## 更新平台设置 > 更新许可

# 更新许可

AI 平台提供试用、订阅和永久三种许可。

| 许可类型 | 说明 |
| --- | --- |
| 试用许可 | 首次安装后的许可类型。过期后仅允许导入许可以及删除 AI 平台中的资源。您可以按需更新为订阅许可或永久许可。 |
| 订阅许可 | 按需选择订阅时长，更为灵活。过期后仅允许导入许可以及删除 AI 平台中的资源。 |
| 永久许可 | 许可永久有效。 |

**操作步骤**

1. 登录 AI 平台管理界面，在左侧菜单栏中单击**许可**。
2. 在**更新许可**下的**许可代码**输入框中输入许可代码。
3. 单击输入框外部的空白区域，载入新许可信息。
4. 确认无误后，单击**更新许可**完成许可更新。

---

## 常见问题处理 > 下载 Hugging Face 模型时卡住

# 下载 Hugging Face 模型时卡住

## 问题描述

网络环境不稳定时，使用 `huggingface-cli` 或集成 `hf_hub` 库从 Hugging Face 下载模型时可能会卡住。

您可能观察到如下现象：

- 下载进度停止后不再恢复。
- 没有报错，但进程就此卡住。
- 网络延迟较高或丢包率较高的环境中，更容易发生这个问题。

## 问题原因

该问题为 hf\_xet 组件的已知问题。HuggingFace 使用 hf\_xet 组件提升模型的下载效率，但在网络连接不稳定的环境下，Xet 下载可能会无限期地卡住。

## 解决方案

下载模版时设置环境变量 `HF_HUB_DISABLE_XET=1` 以禁用 Xet 协议，回退至标准的 HTTP 协议。修改下载协议后虽然速度可能较慢，但在网络不稳定的情况下更可靠。

请根据您下载模型的方式选择合适的解决方案。

自动下载模型手动下载模型

推理实例配置 Hugging Face 模型仓库，自动从 Hugging Face 拉取开源模型时遇到此问题可以通过如下步骤解决：

1. 登录 AI 平台管理界面，在推理实例列表选择目标推理实例，或在目标推理实例的详情页面单击菜单图标（**...**），选择**编辑**。
2. 在配置信息页面单击**配置详情**，在环境变量中添加如下内容：

   - 键：HF\_HUB\_DISABLE\_XET
   - 值：1
3. 单击**保存**完成编辑。

使用 HuggingFace 命令行工具手动下载模型时遇到此问题，请设置环境变量 `HF_HUB_DISABLE_XET=1`。如下示例表示下载模型时配置环境变量以解决此问题。

```
export HF_HUB_DISABLE_XET=1
huggingface-cli download meta-llama/Llama-3.1-8B-Instruct --local-dir ./models/llama-3.1-8b
```

## 相关链接

- [xet-core#409](https://github.com/huggingface/xet-core/issues/409)
- [xet-core#483](https://github.com/huggingface/xet-core/issues/483)

---

## 常见问题处理 > 使用非标准 SSH 端口

# 使用非标准 SSH 端口

## 问题描述

AI 平台通过 SSH 协议连接节点从而管理静态节点集群。SSH 默认端口为 22，如您的节点当前使用其他端口，可能导致添加节点失败。

## 解决方案

AI 平台使用 Ray 作为底层集群管理工具，由于 Ray 不支持直接配置 SSH 端口，请使用 SSH 配置文件为每一个节点配置非标准 SSH 端口来解决此问题。

**操作步骤**

1. 创建 SSH 配置文件并添加节点配置。

   ```
   mkdir -p ./ssh-config
   cat > ./ssh-config/config << 'EOF'
   Host <host_alias>
       HostName <host_ip>
       Port <ssh_port>
       User <user>

   Host <host_alias>
       HostName <host_ip>
       Port <ssh_port>
       User <user>
   EOF
   chmod 600 ./ssh-config/config
   ```

   参数说明如下：

   | 参数 | 说明 |
   | --- | --- |
   | `<host_alias>` | 节点别名，用于在 SSH 配置中标识节点，以及配置完成后添加节点至集群时使用。 |
   | `<host_ip>` | 节点的 IP 地址。 |
   | `<ssh_port>` | 节点使用的 SSH 端口。 |
   | `<user>` | SSH 用户名，需为 root 用户或具有 root 权限的其他用户。 |

   **使用示例**

   ```
   mkdir -p ./ssh-config
   cat > ./ssh-config/config << 'EOF'
   Host gpu-node-1
       HostName 192.168.1.100
       Port 2222
       User root
   EOF
   chmod 600 ./ssh-config/config
   ```

   上述示例表示创建 `./ssh-config/config` 并在其中添加如下配置：节点别名为 `gpu-node-1`，IP 为 `192.168.1.100` 节点使用的端口为 `2222`，用户名 `root`。
2. 将 SSH 配置文件挂载至 AI 平台的 `neutree-core` 容器。

   请根据您的部署模式选择合适的方式挂载。

   使用 Docker ComposeKubernetes

   1. 更新 `docker-compose.yaml` 文件，将 SSH 配置文件挂载至 `neutree-core` 容器。

      ```
      services:
        neutree-core:
          # ... other configurations
          volumes:
            - ./ssh-config:/root/.ssh:ro
      ```
   2. 重启服务。

      ```
      docker-compose up -d
      ```

   注意

   后续使用 `docker-compose.yaml` 升级 AI 平台控制平面时，您的自定义卷挂载可能会被覆盖。升级后，请务必重新将 SSH 配置文件挂载至 `neutree-core` 容器。

   1. 创建一个包含 SSH 配置的 ConfigMap。

      ```
      kubectl create configmap ssh-config --from-file=config=./ssh-config -n neutree
      ```

      或通过 YAML 文件创建 ConfigMap：

      ```
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: ssh-config
        namespace: neutree
      data:
        config: |
          Host gpu-node-1
              HostName 192.168.1.100
              Port 2222
              User root
      ```
   2. 更新 `neutree-core` Deployment，以挂载 SSH 配置文件。

      ```
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: neutree-core
        namespace: neutree
      spec:
        template:
          spec:
            containers:
              - name: neutree-core
                # ... other configurations
                volumeMounts:
                  - name: ssh-config
                    mountPath: /root/.ssh
                    readOnly: true
            volumes:
              - name: ssh-config
                configMap:
                  name: ssh-config
                  defaultMode: 0600
      ```
   3. 使配置生效：

      ```
      kubectl apply -f neutree-core-deployment.yaml -n neutree
      ```
3. 测试节点 SSH 连接是否正常，以验证 SSH 配置文件和节点配置是否正确。
4. 在 AI 平台的集群中添加节点。请使用节点别名（如上示例的 `gpu-node-1`）而不是 IP 地址。

## 相关链接

Ray 相关限制请参考 [Ray Discuss: Specify SSH port to cluster YAMLs](https://discuss.ray.io/t/specify-ssh-port-to-cluster-yamls/502)。

---

## 常见问题处理 > Kubernetes 集群监控显示 No data

# Kubernetes 集群监控显示 No data

## 问题描述

AI 平台在 Kubernetes 集群上部署数据面集群时，依赖 Kubernetes 集群的 `node-exporter` 和 `dcgm-exporter` 组件收集并暴露节点和 GPU 的 Prometheus 格式的指标数据，而 AI 平台本身不包含这两个组件的部署，所以 AI 平台无法获取并展示节点和 GPU 的监控数据。

## 解决方案

AI 平台将自动采集所有节点的 9100 端口以收集 Kubernetes 集群的节点指标，自动采集带有 `app=nvidia-dcgm-exporter` 标签的 Pod 的 9400 端口以收集 Kubernetes 集群 GPU 指标。

- 若您已部署 `node-exporter` 和 `dcgm-exporter`，请确保您的组件满足[组件说明](#%E7%BB%84%E4%BB%B6%E8%AF%B4%E6%98%8E)中的指标端点和部署方式，满足要求即可在 AI 平台的集群详情监控页面正常看到节点和 GPU 的监控数据。
- 若您未部署 `node-exporter` 和 `dcgm-exporter`，请在 Kubernetes 集群中的每一个节点[手动安装 node-exporter](#%E5%AE%89%E8%A3%85-node-exporter)，在包含 GPU 的节点上[手动安装 dcgm-exporter](#%E5%AE%89%E8%A3%85-dcgm-exporter)，以采集节点和 GPU 的监控指标。组件部署完成后，即可在 AI 平台的集群详情监控页面正常看到节点和 GPU 的监控数据。

### 组件说明

| 组件 | 用途 | 指标类型 | 指标端点 | 部署方式 |
| --- | --- | --- | --- | --- |
| [node-exporter](https://github.com/prometheus/node_exporter) | 采集节点的硬件指标和操作系统指标。 | 收集 CPU、内存、磁盘、网络等系统级别的监控数据。 | 9100 | DaemonSet |
| [dcgm-exporter](https://github.com/NVIDIA/dcgm-exporter) | 采集 NVIDIA GPU 指标。 | 收集 GPU 利用率、显存、温度、功耗等 GPU 相关的监控数据。 | 9400 | DaemonSet |

说明：

- 上述组件通常占用资源较少，但在大规模集群中部署时请合理设置资源限制。
- 若 dcgm-exporter 的部署模式与本文档不同，请务必确认满足其他要求。
- OpenShift 环境安装需要先参考[配置 OpenShift 兼容性](/smtx-ai/1.0.0/user_guide/faq/openshift-compatibility)为对应命名空间创建 SCC 配置。

### 安装 node-exporter

`node-exporter` 用于暴露节点的系统指标，必须以 DaemonSet 方式部署到集群的每个节点上。

**前提条件**

请确保 AI 平台数据面集群能够访问 `node-exporter` 的 9100 端口。

**操作步骤**

1. 修改下述命令中 `<namespace>` 然后执行，以安装 `node-exporter`。

   ```
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

   helm install node-exporter prometheus-community/prometheus-node-exporter --namespace=<namespace>
   ```
2. 检查 node-exporter Pod 运行状态：

   ```
   kubectl get pods -n <namespace> -l app=node-exporter
   ```

   预期所有 Pod 状态为 `Running`，表示 `node-exporter` 已成功部署到所有节点。
3. 验证指标端点：

   ```
   kubectl port-forward -n <namespace> <node-exporter-pod-name> 9100:9100
   curl http://localhost:9100/metrics
   ```

   预期返回 Prometheus 格式的指标数据，表示 `node-exporter` 已就绪。

### 安装 dcgm-exporter

`dcgm-exporter` 用于暴露 NVIDIA GPU 的监控指标，需要部署在所有包含 GPU 的节点上，可以使用节点选择器或污点容忍来限制部署范围。

**前提条件**

- AI 平台数据面集群能够访问 `dcgm-exporter` 的指标端点（默认端口为 9400）。
- Kubernetes 集群已安装 NVIDIA GPU Operator 或已手动安装 NVIDIA Graphics driver 和 Container Toolkit。
- Kubernetes 集群 GPU 节点可被 Kubernetes 正确识别，可以通过 `kubectl describe node <node-name>` 查看 GPU 资源。

**操作步骤**

1. 修改下述命令中的 `<namespace>` 后执行，以安装 `dcgm-exporter`。

   ```
   kubectl apply -f - << EOF
   apiVersion: v1
   data:
     dcgm-metrics.csv: |
       # Format
       # If line starts with a '#' it is considered a comment
       # DCGM FIELD, Prometheus metric type, help message

       # Clocks
       DCGM_FI_DEV_SM_CLOCK,  gauge, SM clock frequency (in MHz).
       DCGM_FI_DEV_MEM_CLOCK, gauge, Memory clock frequency (in MHz).

       # Temperature
       DCGM_FI_DEV_MEMORY_TEMP, gauge, Memory temperature (in C).
       DCGM_FI_DEV_GPU_TEMP,    gauge, GPU temperature (in C).

       # Power
       DCGM_FI_DEV_POWER_USAGE,              gauge, Power draw (in W).
       DCGM_FI_DEV_TOTAL_ENERGY_CONSUMPTION, counter, Total energy consumption since boot (in mJ).

       # PCIE
       # DCGM_FI_DEV_PCIE_TX_THROUGHPUT,  counter, Total number of bytes transmitted through PCIe TX (in KB) via NVML.
       # DCGM_FI_DEV_PCIE_RX_THROUGHPUT,  counter, Total number of bytes received through PCIe RX (in KB) via NVML.
       DCGM_FI_DEV_PCIE_REPLAY_COUNTER, counter, Total number of PCIe retries.

       # Utilization (the sample period varies depending on the product)
       DCGM_FI_DEV_GPU_UTIL,      gauge, GPU utilization (in %).
       DCGM_FI_DEV_MEM_COPY_UTIL, gauge, Memory utilization (in %).
       DCGM_FI_DEV_ENC_UTIL,      gauge, Encoder utilization (in %).
       DCGM_FI_DEV_DEC_UTIL ,     gauge, Decoder utilization (in %).

       # Errors and violations
       DCGM_FI_DEV_XID_ERRORS,            gauge,   Value of the last XID error encountered.
       # DCGM_FI_DEV_POWER_VIOLATION,       counter, Throttling duration due to power constraints (in us).
       # DCGM_FI_DEV_THERMAL_VIOLATION,     counter, Throttling duration due to thermal constraints (in us).
       # DCGM_FI_DEV_SYNC_BOOST_VIOLATION,  counter, Throttling duration due to sync-boost constraints (in us).
       # DCGM_FI_DEV_BOARD_LIMIT_VIOLATION, counter, Throttling duration due to board limit constraints (in us).
       # DCGM_FI_DEV_LOW_UTIL_VIOLATION,    counter, Throttling duration due to low utilization (in us).
       # DCGM_FI_DEV_RELIABILITY_VIOLATION, counter, Throttling duration due to reliability constraints (in us).

       # Memory usage
       DCGM_FI_DEV_FB_FREE, gauge, Framebuffer memory free (in MiB).
       DCGM_FI_DEV_FB_USED, gauge, Framebuffer memory used (in MiB).
       DCGM_FI_DEV_FB_TOTAL, gauge, Framebuffer memory total (in MiB).
       DCGM_FI_DEV_FB_RESERVED, gauge, Framebuffer memory reserved (in MiB).

       # ECC
       # DCGM_FI_DEV_ECC_SBE_VOL_TOTAL, counter, Total number of single-bit volatile ECC errors.
       # DCGM_FI_DEV_ECC_DBE_VOL_TOTAL, counter, Total number of double-bit volatile ECC errors.
       # DCGM_FI_DEV_ECC_SBE_AGG_TOTAL, counter, Total number of single-bit persistent ECC errors.
       # DCGM_FI_DEV_ECC_DBE_AGG_TOTAL, counter, Total number of double-bit persistent ECC errors.

       # Retired pages
       # DCGM_FI_DEV_RETIRED_SBE,     counter, Total number of retired pages due to single-bit errors.
       # DCGM_FI_DEV_RETIRED_DBE,     counter, Total number of retired pages due to double-bit errors.
       # DCGM_FI_DEV_RETIRED_PENDING, counter, Total number of pages pending retirement.

       # NVLink
       # DCGM_FI_DEV_NVLINK_CRC_FLIT_ERROR_COUNT_TOTAL, counter, Total number of NVLink flow-control CRC errors.
       # DCGM_FI_DEV_NVLINK_CRC_DATA_ERROR_COUNT_TOTAL, counter, Total number of NVLink data CRC errors.
       # DCGM_FI_DEV_NVLINK_REPLAY_ERROR_COUNT_TOTAL,   counter, Total number of NVLink retries.
       # DCGM_FI_DEV_NVLINK_RECOVERY_ERROR_COUNT_TOTAL, counter, Total number of NVLink recovery errors.
       DCGM_FI_DEV_NVLINK_BANDWIDTH_TOTAL,            counter, Total number of NVLink bandwidth counters for all lanes.
       # DCGM_FI_DEV_NVLINK_BANDWIDTH_L0,               counter, The number of bytes of active NVLink rx or tx data including both header and payload.

       # VGPU License status
       DCGM_FI_DEV_VGPU_LICENSE_STATUS, gauge, vGPU License status

       # Remapped rows
       DCGM_FI_DEV_UNCORRECTABLE_REMAPPED_ROWS, counter, Number of remapped rows for uncorrectable errors
       DCGM_FI_DEV_CORRECTABLE_REMAPPED_ROWS,   counter, Number of remapped rows for correctable errors
       DCGM_FI_DEV_ROW_REMAP_FAILURE,           gauge,   Whether remapping of rows has failed

       # Static configuration information. These appear as labels on the other metrics
       DCGM_FI_DRIVER_VERSION,        label, Driver Version
       # DCGM_FI_NVML_VERSION,          label, NVML Version
       # DCGM_FI_DEV_BRAND,             label, Device Brand
       # DCGM_FI_DEV_SERIAL,            label, Device Serial Number
       # DCGM_FI_DEV_OEM_INFOROM_VER,   label, OEM inforom version
       # DCGM_FI_DEV_ECC_INFOROM_VER,   label, ECC inforom version
       # DCGM_FI_DEV_POWER_INFOROM_VER, label, Power management object inforom version
       # DCGM_FI_DEV_INFOROM_IMAGE_VER, label, Inforom image version
       # DCGM_FI_DEV_VBIOS_VERSION,     label, VBIOS version of the device

       # DCP metrics
       DCGM_FI_PROF_GR_ENGINE_ACTIVE,   gauge, Ratio of time the graphics engine is active (in %).
       # DCGM_FI_PROF_SM_ACTIVE,          gauge, The ratio of cycles an SM has at least 1 warp assigned (in %).
       # DCGM_FI_PROF_SM_OCCUPANCY,       gauge, The ratio of number of warps resident on an SM (in %).
       DCGM_FI_PROF_PIPE_TENSOR_ACTIVE, gauge, Ratio of cycles the tensor (HMMA) pipe is active (in %).
       DCGM_FI_PROF_DRAM_ACTIVE,        gauge, Ratio of cycles the device memory interface is active sending or receiving data (in %).
       # DCGM_FI_PROF_PIPE_FP64_ACTIVE,   gauge, Ratio of cycles the fp64 pipes are active (in %).
       # DCGM_FI_PROF_PIPE_FP32_ACTIVE,   gauge, Ratio of cycles the fp32 pipes are active (in %).
       # DCGM_FI_PROF_PIPE_FP16_ACTIVE,   gauge, Ratio of cycles the fp16 pipes are active (in %).
       DCGM_FI_PROF_PCIE_TX_BYTES,      gauge, The rate of data transmitted over the PCIe bus - including both protocol headers and data payloads - in bytes per second.
       DCGM_FI_PROF_PCIE_RX_BYTES,      gauge, The rate of data received over the PCIe bus - including both protocol headers and data payloads - in bytes per second.
   kind: ConfigMap
   metadata:
     name: metrics-config
     namespace: <namespace>
   ---
   apiVersion: apps/v1
   kind: DaemonSet
   metadata:
     labels:
       app.kubernetes.io/name: dcgm-exporter
       app.kubernetes.io/version: 4.7.1
     name: dcgm-exporter
     namespace: <namespace>
   spec:
     revisionHistoryLimit: 10
     selector:
       matchLabels:
         app.kubernetes.io/name: dcgm-exporter
         app.kubernetes.io/version: 4.7.1
     template:
       metadata:
         creationTimestamp: null
         labels:
           app: nvidia-dcgm-exporter
           app.kubernetes.io/name: dcgm-exporter
           app.kubernetes.io/version: 4.7.1
         name: dcgm-exporter
       spec:
         automountServiceAccountToken: false
         containers:
         - env:
           - name: DCGM_EXPORTER_LISTEN
             value: :9400
           - name: DCGM_EXPORTER_KUBERNETES
             value: "true"
           - name: DCGM_EXPORTER_COLLECTORS
             value: /etc/dcgm-exporter/dcgm-metrics.csv
           image: nvcr.io/nvidia/k8s/dcgm-exporter:4.4.2-4.7.1-ubuntu22.04
           imagePullPolicy: IfNotPresent
           name: dcgm-exporter
           ports:
          - containerPort: 9400
             name: metrics
             protocol: TCP
           resources:
             limits:
               cpu: 200m
               memory: 512Mi
             requests:
               cpu: 100m
               memory: 128Mi
           securityContext:
             allowPrivilegeEscalation: false
             capabilities:
               add:
               - SYS_ADMIN
               drop:
               - ALL
             runAsNonRoot: false
             runAsUser: 0
           terminationMessagePath: /dev/termination-log
           terminationMessagePolicy: File
           volumeMounts:
           - mountPath: /var/lib/kubelet/pod-resources
             name: pod-gpu-resources
             readOnly: true
           - mountPath: /etc/dcgm-exporter/dcgm-metrics.csv
             name: metrics-config
             readOnly: true
             subPath: dcgm-metrics.csv
         dnsPolicy: ClusterFirst
         restartPolicy: Always
         securityContext: {}
         terminationGracePeriodSeconds: 30
         volumes:
         - hostPath:
             path: /var/lib/kubelet/pod-resources
             type: ""
           name: pod-gpu-resources
         - configMap:
             defaultMode: 420
             items:
             - key: dcgm-metrics.csv
               path: dcgm-metrics.csv
             name: metrics-config
           name: metrics-config
     updateStrategy:
       rollingUpdate:
         maxSurge: 0
         maxUnavailable: 1
       type: RollingUpdate
   EOF
   ```
2. 检查 dcgm-exporter Pod 运行状态：

   ```
   kubectl get pods -n <namespace> -l app=dcgm-exporter
   ```

   预期所有 Pod 状态为 `Running`，表示 `dcgm-exporter` 已成功部署到所有包含 GPU 的节点。
3. 验证指标端点：

   ```
   kubectl port-forward -n <namespace> <dcgm-exporter-pod-name> 9400:9400
   curl http://localhost:9400/metrics
   ```

   预期返回包含 GPU 相关指标的数据（如 `DCGM_FI_DEV_GPU_UTIL` 等），表示 `dcgm-exporter` 已就绪。

## 相关链接

[NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/overview.html)

---

## 常见问题处理 > 配置 OpenShift 兼容性

# 配置 OpenShift 兼容性

## 问题描述

在 OpenShift 环境中使用 AI 平台时，由于 OpenShift 的安全上下文约束（Security Context Constraints, SCC）与标准 Kubernetes 集群有所不同，直接部署可能会导致控制面和数据面 Pod 无法正常启动或运行。

您可能观察到如下现象：

- 控制面 Helm 部署失败，Pod 无法启动。
- 数据面集群创建后，Pod 处于 CrashLoopBackOff 状态。

## 问题原因

OpenShift 使用 SCC 来控制 Pod 的安全权限，默认的 SCC 策略比标准 Kubernetes 更加严格。AI 平台的某些组件可能需要特定的权限，如特权模式、主机网络访问、特定的用户 ID 等，这些权限需要通过创建自定义 SCC 来授予。

## 解决方案

针对 OpenShift 环境，需要分别为[控制面](#%E4%B8%BA%E6%8E%A7%E5%88%B6%E9%9D%A2%E9%85%8D%E7%BD%AE-scc)和[数据面](#%E4%B8%BA%E6%95%B0%E6%8D%AE%E9%9D%A2%E9%9B%86%E7%BE%A4%E9%85%8D%E7%BD%AE-scc)配置相应的 SCC。

注意：

创建和管理 SCC 配置需要集群管理员权限。

### 为控制面配置 SCC

在 OpenShift 上部署 AI 平台控制面时，需要在执行 Helm 安装之前创建必要的 SCC。

**操作步骤**

1. 修改下述命令中 `<namespace>` 为 AI 平台控制面部署的命名空间，然后执行该命令以创建控制面所需的 SCC。

   ```
   kubectl apply -f - <<EOF
   kind: SecurityContextConstraints
   apiVersion: security.openshift.io/v1
   metadata:
     name: neutree-controlplane-scc
     annotations:
       kubernetes.io/description: "Custom SCC for Neutree AI ControlPlane to allow root and any UID/GID."
   priority: 10000
   allowHostDirVolumePlugin: true
   allowHostIPC: true
   allowHostNetwork: true
   allowHostPID: true
   allowHostPorts: true
   allowPrivilegeEscalation: true
   allowPrivilegedContainer: true
   allowedCapabilities:
   - '*'
   allowedUnsafeSysctls:
   - '*'
   readOnlyRootFilesystem: false
   runAsUser:
     type: RunAsAny
   seLinuxContext:
     type: RunAsAny
   fsGroup:
     type: RunAsAny
   supplementalGroups:
     type: RunAsAny
   seccompProfiles:
   - '*'
   volumes:
   - '*'
   groups:
   - system:serviceaccounts:<namespace>
   EOF
   ```
2. 验证 SCC 创建成功：

   ```
   oc get scc
   ```

   预期列表中将展示名称为 `neutree-controlplane-scc` 的 SCC。
3. 执行 Helm 安装部署控制面：

   ```
   helm install <release-name> <chart-name> -n <namespace>
   ```

   | 参数 | 说明 |
   | --- | --- |
   | `<release-name>` | Helm release 名称。 |
   | `<chart-name>` | AI 平台控制面 Helm chart 名称或路径。 |
   | `<namespace>` | AI 平台控制面部署的命名空间。 |
4. 验证控制面 Pod 运行状态：

   ```
   kubectl get pods -n <namespace>
   ```

   预期所有 Pod 状态为 `Running`。

### 为数据面集群配置 SCC

在 OpenShift 上创建数据面集群时，需要在集群创建完成后，为数据面创建 SCC，然后重建所有数据面 Pod。

**操作步骤**

1. 在 AI 平台管理界面[创建数据面集群](/smtx-ai/1.0.0/user_guide/infrastructure/cluster-kubernetes#%E5%88%9B%E5%BB%BA%E9%9B%86%E7%BE%A4)，集群创建完成后 Pod 可能因权限问题无法正常启动。
2. 获取数据面集群使用的命名空间：

   ```
   kubectl get ns -l neutree.ai/neutree-cluster=<cluster>,neutree.ai/neutree-workspace=<workspace>
   ```

   | 参数 | 说明 |
   | --- | --- |
   | `<cluster>` | 数据面集群名称。 |
   | `<workspace>` | 数据面集群所属的工作空间名称。 |
3. 将 `<namespace>` 替换为步骤 2 中获取的数据面集群命名空间，然后执行该命令以创建数据面所需的 SCC。

   ```
   kubectl apply -f - <<EOF
   kind: SecurityContextConstraints
   apiVersion: security.openshift.io/v1
   metadata:
     name: neutree-datacluster-scc
     annotations:
       kubernetes.io/description: "Custom SCC for Neutree AI Data Cluster to allow root and any UID/GID."
   priority: 10000
   allowHostDirVolumePlugin: true
   allowHostIPC: true
   allowHostNetwork: true
   allowHostPID: true
   allowHostPorts: true
   allowPrivilegeEscalation: true
   allowPrivilegedContainer: true
   allowedCapabilities:
   - '*'
   allowedUnsafeSysctls:
   - '*'
   readOnlyRootFilesystem: false
   runAsUser:
     type: RunAsAny
   seLinuxContext:
     type: RunAsAny
   fsGroup:
     type: RunAsAny
   supplementalGroups:
     type: RunAsAny
   seccompProfiles:
   - '*'
   volumes:
   - '*'
   groups:
   - system:serviceaccounts:<namespace>
   EOF
   ```
4. 验证 SCC 创建成功。

   ```
   oc get scc
   ```

   预期列表中将展示名称为 `neutree-datacluster-scc` 的 SCC。
5. 将 `<namespace>` 替换为步骤 2 中获取的数据面集群命名空间，然后执行该命令以重建数据面集群的所有 Pod。

   ```
   kubectl delete pods --all -n <namespace>
   ```

   Pod 删除后，Kubernetes 控制器将自动重建，新的 Pod 将使用已配置的 SCC。
6. 验证数据面 Pod 运行状态：

   ```
   kubectl get pods -n <namespace>
   ```

   预期所有 Pod 状态为 `Running`，无权限相关错误。
7. 登录 AI 平台管理界面，在左侧菜单栏中单击**集群**，在集群列表中确认数据面集群状态为**运行中**。

## 相关链接

[OpenShift 官方文档 - Managing Security Context Constraints](https://docs.openshift.com/container-platform/latest/authentication/managing-security-context-constraints.html)

---

## 常见问题处理 > 对接外部 Grafana

# 对接外部 Grafana

AI 平台内置了 Grafana 用于监控和可视化系统指标，但在某些情况下，您可能希望使用已有的外部 Grafana 实例来统一管理多个系统的监控数据。

## 步骤 1：配置外部 Grafana 支持匿名访问和 UI 嵌入

外部 Grafana 必须支持匿名访问和 UI 嵌入后，AI 平台才能将 Grafana 仪表板嵌入至管理界面。

1. 编辑 Grafana 配置文件（通常为 `grafana.ini` 或通过环境变量配置）。
2. 启用匿名访问：

   ```
   [auth.anonymous]
   enabled = true
   ```
3. 允许 UI 嵌入：

   ```
   [security]
   allow_embedding = true
   ```
4. 重启 Grafana 服务使配置生效。

## 步骤 2：在外部 Grafana 添加 AI 平台指标数据源

将外部 Grafana 数据源配置为 AI 平台配置的 Prometheus 指标端点。

1. 登录外部 Grafana 管理界面，导航至 **Configuration**（部分版本为 **Connections**） > **Data Sources**。
2. 单击 **Add data source**，选择 **Prometheus**。
3. 配置数据源参数：

   | 参数 | 说明 |
   | --- | --- |
   | Name | 数据源名称，必须为 `neutree-cluster`。 |
   | URL | AI 平台配置的 Prometheus 服务地址，例如：`http://<prometheus-host>:9090`。 |
4. 单击 **Save & Test** 验证连接。

## 步骤 3：导入 Neutree Dashboard

AI 平台提供了预配置的 Grafana 仪表板，用于展示系统关键指标。

1. 使用 AI 平台命令行工具获取 Dashboard 配置文件。

   执行以下命令导出 Dashboard 配置文件：

   ```
   neutree-cli-<arch> launch obs-stack --dry-run
   ```

   导出的 Dashboard 配置文件位于 `neutree-deploy/obs-stack/grafana/dashboards` 目录下：

   ```
   tree neutree-deploy/obs-stack/grafana/dashboards
   ```

   目录结构如下：

   ```
   neutree-deploy/obs-stack/grafana/dashboards
   ├── data_grafana_dashboard.json
   ├── dcgm_exporter_dashboard.json
   ├── default_grafana_dashboard.json
   ├── node_exporter_dashboard.json
   ├── overview_dashboard.json
   ├── router_dashboard.json
   ├── serve_deployment_grafana_dashboard.json
   ├── serve_grafana_dashboard.json
   └── vllm_grafana_dashboard.json
   ```
2. 在 Grafana 中导入 Dashboard。

   1. 登录外部 Grafana 管理界面，导航至 **Dashboards** > **Import** 。
   2. 单击 **Upload JSON file** 并选择下载的 Dashboard JSON 文件，或直接粘贴 JSON 内容。
   3. 在导入配置中完成如下配置：

      - **Name**：保持默认的仪表板名称。
      - **Folder**：选择或创建文件夹以组织仪表板（例如：`Default`）。
   4. 单击 **Import** 完成导入。
3. 重复上述步骤导入其他 Dashboard 文件。

## 步骤 4：在 AI 平台中配置外部 Grafana 地址

请根据 AI 平台的部署方式选择合适的方式配置外部 Grafana 地址，以便在 AI 平台管理界面中嵌入仪表板：

- 使用 Docker Compose 部署请通过 `aunch --grafana-url` 配置为外部 Grafana 地址。
- Kubernetes 部署请参考[修改监控组件配置](/smtx-ai/1.0.0/user_guide/getting-started/deploy-kubernetes#%E4%BF%AE%E6%94%B9%E7%9B%91%E6%8E%A7%E7%BB%84%E4%BB%B6%E9%85%8D%E7%BD%AE)章节更新 Grafana 相关配置项，禁用内置 Grafana 并配置 `system.grafana.url` 为外部 Grafana 地址。

## 步骤 5：验证配置成功

1. 访问外部 Grafana，确认 Neutree Dashboard 能够正常显示数据。
2. 登录 AI 平台管理界面，检查监控页面是否正确嵌入并显示外部 Grafana 仪表板。

## 相关链接

- [Grafana 匿名访问配置](https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/grafana/#anonymous-authentication)
- [Grafana 嵌入配置](https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/#allow-embedding)

---

## 常见问题处理 > 手动导入模型至模型仓库

# 手动导入模型至模型仓库

## 问题描述

AI 平台支持使用 `neutree-cli-<arch> model push` 命令将模型推送至模型仓库，详见[推送模型](/smtx-ai/1.0.0/user_guide/model-service/model-management#%E6%8E%A8%E9%80%81%E6%A8%A1%E5%9E%8B)，但该方式需要通过 API 上传模型文件，模型体积较大时耗时较长；并且您使用 AI 平台的过程中，可能存在以下场景需要将已下载的模型文件手动导入至 AI 平台的模型仓库：

- 模型文件已通过 U 盘、硬盘拷贝等离线方式传输到节点上，需要导入至 AI 平台使用。
- 从 Hugging Face 或其他来源手动下载了模型文件，希望将其注册到 AI 平台的模型仓库中。
- 网络环境受限，无法通过 AI 平台自动下载模型，需要通过其他环境下载然后导入至 AI 平台使用。

## 解决方案

如果模型文件已在 NFS 存储所在的节点上，本节提供 `import-model.sh` 脚本直接将模型文件导入至模型仓库。该脚本通过本地文件复制的方式完成导入，跳过了网络传输环节，速度更快，操作更简便。

### 前提条件

- 模型文件已下载到节点本地目录。
- 节点已挂载 NFS 存储。
- 节点已安装 Python 3。用于自动生成版本号，若手动指定版本号则可以忽略此项。

### 步骤 1：创建脚本

在模型文件所在节点上创建导入脚本 `import-model.sh`，内容如下：

```
#!/bin/bash
# import-model.sh
# 用法: ./import-model.sh <源目录> <模型名> [版本号] [NFS 路径]

set -e

SOURCE_DIR="$1"
MODEL_NAME="$2"
VERSION="$3"
NFS_PATH="${4:-/mnt/bentoml}"

if [ -z "$SOURCE_DIR" ] || [ -z "$MODEL_NAME" ]; then
    echo "用法: $0 <源目录> <模型名> [版本号] [NFS 路径]"
    echo "示例: $0 /tmp/qwen2-0.5b-instruct qwen2-0.5b-instruct"
    echo "示例: $0 /tmp/qwen2-0.5b-instruct qwen2-0.5b-instruct v1.0"
    echo "示例: $0 /tmp/qwen2-0.5b-instruct qwen2-0.5b-instruct v1.0 /mnt/bentoml"
    exit 1
fi

# 模型名称转小写
MODEL_NAME=$(echo "$MODEL_NAME" | tr '[:upper:]' '[:lower:]')

# 若未提供版本号，则自动生成
if [ -z "$VERSION" ]; then
    VERSION=$(python3 -c "import uuid, base64; u=uuid.uuid1(); print(base64.b32encode(u.bytes[:6]+u.bytes[8:12]).decode().lower().rstrip('='))")
fi
VERSION=$(echo "$VERSION" | tr '[:upper:]' '[:lower:]')

TARGET_DIR="${NFS_PATH}/models/${MODEL_NAME}/${VERSION}"

echo "导入模型: ${MODEL_NAME}"
echo "版本号: ${VERSION}"
echo "目标目录: ${TARGET_DIR}"

# 创建目录
mkdir -p "${TARGET_DIR}"

# 复制文件
echo "复制模型文件..."
cp -r "${SOURCE_DIR}"/* "${TARGET_DIR}/"

# 计算目录大小
SIZE=$(du -sh "${TARGET_DIR}" | cut -f1)

# 生成 model.yaml
cat > "${TARGET_DIR}/model.yaml" << EOF
name: ${MODEL_NAME}
version: ${VERSION}
size: ${SIZE}
module: ""
api_version: v1
signatures: {}
labels: {}
options: {}
metadata: {}
context:
    framework_name: transformers
    framework_versions: {}
    bentoml_version: 1.4.6
    python_version: "3.12"
creation_time: "$(date -u +"%Y-%m-%dT%H:%M:%S.000000+00:00")"
EOF

# 更新 latest
echo -n "${VERSION}" > "${NFS_PATH}/models/${MODEL_NAME}/latest"

# 设置权限
chmod -R 755 "${NFS_PATH}/models/${MODEL_NAME}"

echo "导入完成!"
echo "模型标签: ${MODEL_NAME}:${VERSION}"
```

为脚本分配可执行权限：

```
chmod +x import-model.sh
```

### 步骤 2：运行脚本导入模型

运行脚本将模型导入至模型仓库：

```
./import-model.sh <源目录> <模型名> [版本号] [NFS 路径]
```

参数说明如下：

| 参数 | 是否必填 | 说明 |
| --- | --- | --- |
| `<源目录>` | 是 | 模型文件所在的本地目录路径。 |
| `<模型名>` | 是 | 模型名称，脚本会自动将其转换为小写。 |
| `[版本号]` | 否 | 模型版本号。若不指定，脚本会自动生成一个唯一版本号。 |
| `[NFS 路径]` | 否 | NFS 存储的挂载路径，默认为 `/mnt/bentoml`。 |

**使用示例**

- 使用默认设置导入模型（自动生成版本号，使用默认 NFS 路径）：

  ```
  ./import-model.sh /tmp/qwen2-0.5b-instruct qwen2-0.5b-instruct
  ```
- 指定版本号导入模型：

  ```
  ./import-model.sh /tmp/qwen2-0.5b-instruct qwen2-0.5b-instruct v1.0
  ```
- 指定版本号和自定义 NFS 路径：

  ```
  ./import-model.sh /tmp/qwen2-0.5b-instruct qwen2-0.5b-instruct v1.0 /mnt/bentoml
  ```

### 步骤 3：验证导入结果

导入完成后，脚本会输出格式为`模型名:版本号`的模型标签。您可以使用 `neutree-cli-<arch> model list` 命令查看模型是否已被 AI 平台正常识别，详见[查看模型](/smtx-ai/1.0.0/user_guide/model-service/model-management#%E6%9F%A5%E7%9C%8B%E6%A8%A1%E5%9E%8B)。

---

## 常见问题处理 > 升级静态节点集群版本

# 升级静态节点集群版本

当 AI 平台发布静态节点集群的临时版本时，由于 AI 平台尚未支持静态节点集群的在线升级，需要手动升级。本节以 `v1.0.0-vllm0.11.2-ray2.53.0` 为例，介绍如何手动将静态节点集群升级至临时版本。

## 前提条件

- 已获取目标版本的静态节点集群离线镜像文件（`.tar.gz` 格式）及 AI 平台 CLI 工具。
- 已准备好可访问的镜像仓库，并拥有具备推送权限的账号。
- 已拥有登录控制面安装节点所在的机器的权限。

## 步骤 1：导入集群镜像至镜像仓库

在持有镜像包的机器上执行以下命令，将集群离线镜像导入至您的镜像仓库：

```
./neutree-cli-<arch> import cluster \
-p <cluster_package> \
--mirror-registry <mirror_registry> \
--registry-username <registry_username> \
--registry-password <registry_password>
```

参数说明如下：

| 参数 | 说明 |
| --- | --- |
| `<arch>` | 服务器的 CPU 架构，取值为 `amd64` 或 `aarch64`。 |
| `<cluster_package>` | 集群离线镜像文件名称。例如 `neutree-cluster-ssh-nvidia_gpu-v1.0.0-vllm0.11.2-ray2.53.0-amd64.tar.gz`。 |
| `<mirror_registry>` | 镜像仓库地址。 |
| `<registry_username>` | 镜像仓库用户的用户名，需为具备上传镜像权限的用户。 |
| `<registry_password>` | 镜像仓库用户的登录密码或访问密钥（例如 token）。 |

等待命令执行完成，确认镜像已成功推送至镜像仓库后，继续执行后续步骤。

## 步骤 2：导出当前集群 YAML

将当前静态节点配置集群[导出为 YAML 文件](/smtx-ai/1.0.0/user_guide/yaml/yaml-export)。

1. 登录 AI 平台管理界面，在顶部单击**导出 YAML**。
2. 选择**集群**资源类型，勾选目标静态节点集群。
3. 单击**生成 YAML** 预览内容，确认无误后下载为文件，留待后续步骤修改使用。

## 步骤 3：删除当前集群

注意：

删除集群需要先删除部署在该集群的推理实例，请确保当前集群上的推理实例配置已经通过 YAML 导出备份，以便于新版本集群创建后快速恢复。

1. 在集群列表中找到目标集群，单击菜单图标（**...**），选择**删除**。
2. 在弹出的确认对话框中确认删除操作，等待集群删除完成。

## 步骤 4：修改集群 YAML 并重新导入

1. 打开步骤 2 中导出的集群 YAML 文件，找到 `.spec.version` 字段，将其修改为目标版本号：

   ```
   spec:
     version: v1.0.0-vllm0.11.2-ray2.53.0
   ```
2. 保存修改后的 YAML 文件。
3. [导入修改后的 YAML 文件](/smtx-ai/1.0.0/user_guide/yaml/yaml-import)。

   1. 登录 AI 平台管理界面，在顶部单击**导入 YAML**。
   2. 在弹出的**从 YAML 导入资源**对话框中，单击文件选择框，上传修改后的 YAML 文件，然后单击**导入资源**。
4. 导入完成后，确认资源状态显示成功，等待集群恢复正常运行状态。

## 步骤 5：更新 vmagent 指标采集配置

新版本集群镜像调整了 vLLM 指标名称，需要手动更新控制面 vmagent 的指标采集配置。

控制面部署在服务器或虚拟机控制面部署在 Kubernetes

1. 登录控制面安装节点所在的机器。
2. 打开 vmagent 配置文件 `./neutree-deploy/neutree-core/vmagent/prometheus.yml`，将其内容替换为以下配置：

   ```
   global:
     scrape_interval: 30s # Set the scrape interval to every 30 seconds. Default is every 1 minute.

   scrape_configs:
   # Scrape from each Ray node as defined in the service_discovery.json provided by Ray.
   - job_name: 'neutree'
     file_sd_configs:
     - files:
       - '/etc/prometheus/scrape/*.json'

   # Ray use applicationName as application label value in metrics.
   # it cause the UI can not show the dashboard correctly.
   # So we use relabeling to change it to "endpointName".
     metric_relabel_configs:
       - source_labels: [application]
         target_label: application_original
         regex: '(.+)'
         replacement: '$1'
       - source_labels: [application]
         regex: '([^_]+)_(.+)'
         target_label: application
         replacement: '$2'
       # Convert ray_vllm: or ray_vllm_ prefix to vllm: prefix
       # ray_vllm:e2e_request_latency_seconds_bucket => vllm:e2e_request_latency_seconds_bucket (old clusters)
       # ray_vllm_e2e_request_latency_seconds_bucket => vllm:e2e_request_latency_seconds_bucket (Ray 2.53.0+)
       - source_labels: [__name__]
         regex: 'ray_vllm[:_](.+)'
         target_label: __name__
         replacement: 'vllm:$1'
   ```
3. 保存配置文件后，执行以下命令重启 vmagent 使配置生效：

   ```
   docker restart vmagent
   ```
4. 确认 vmagent 重启成功，检查其日志中无报错信息。

1. 执行如下命令，编辑 vmagent 配置文件。

   ```
   kubectl edit cm vmagent-config -n neutree
   ```
2. 在配置中找到 prometheus.yml 键，将其值更新为新的采集配置：

   ```
   global:
     scrape_interval: 30s # Set the scrape interval to every 30 seconds. Default is every 1 minute.

   scrape_configs:
   # Scrape from each Ray node as defined in the service_discovery.json provided by Ray.
   - job_name: 'neutree'
     file_sd_configs:
     - files:
       - '/etc/prometheus/scrape/*.json'

   # Ray use applicationName as application label value in metrics.
   # it cause the UI can not show the dashboard correctly.
   # So we use relabeling to change it to "endpointName".
     metric_relabel_configs:
       - source_labels: [application]
         target_label: application_original
         regex: '(.+)'
         replacement: '$1'
       - source_labels: [application]
         regex: '([^_]+)_(.+)'
         target_label: application
         replacement: '$2'
       # Convert ray_vllm: or ray_vllm_ prefix to vllm: prefix
       # ray_vllm:e2e_request_latency_seconds_bucket => vllm:e2e_request_latency_seconds_bucket (old clusters)
       # ray_vllm_e2e_request_latency_seconds_bucket => vllm:e2e_request_latency_seconds_bucket (Ray 2.53.0+)
       - source_labels: [__name__]
         regex: 'ray_vllm[:_](.+)'
         target_label: __name__
         replacement: 'vllm:$1'
   ```

## 步骤 6：验证升级成功

登录 AI 平台管理界面，通过如下步骤验证集群版本升级成功：

1. [查看集群列表或集群详情页面](/smtx-ai/1.0.0/user_guide/infrastructure/cluster-ssh#%E6%9F%A5%E7%9C%8B%E9%9B%86%E7%BE%A4)，确认集群状态恢复为**正常**。
2. [创建一个测试推理实例](/smtx-ai/1.0.0/user_guide/model-service/endpoint#%E5%88%9B%E5%BB%BA%E6%8E%A8%E7%90%86%E5%AE%9E%E4%BE%8B)，确认实例可以正常启动并提供服务。
3. [查看推理实例详情的监控页面](/smtx-ai/1.0.0/user_guide/model-service/endpoint#%E6%9F%A5%E7%9C%8B%E7%9B%91%E6%8E%A7%E4%B8%8E%E6%97%A5%E5%BF%97)，确认 vLLM 相关监控指标可以正常展示。

---

## 版权信息

# 版权信息

版权所有 © 2026 北京志凌海纳科技股份有限公司（SmartX）保留一切权利。

本文档和本文档包含的全部信息受中华人民共和国法律法规及国际公约对知识产权的管辖和保护。本文档和本文档包含的全部信息的版权由 SmartX 或其许可方所有。未经 SmartX 书面许可，不得以任何方式，包括但不限于电子、机械或光学的方式对本文档内容的部分或全部进行复制、修改、传播、经销、翻印、拆解、存储在检索系统中或其他任何形式的使用。本文档中出现的所有非 SmartX 的公司名称、产品名称和服务名称仅用于识别目的，可能是其各自所有者的注册商标、商标或服务标记，不应被视为未经其所有者书面许可而授予使用前述任何商标、标志的许可或权利，亦不代表该所有者对任何产品或服务信息的授权使用或背书。
