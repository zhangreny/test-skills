---
name: gog-linux-installer
description: |
  在 CentOS/RHEL 8 Linux 服务器上安装 Homebrew 和 gog (Google Workspace CLI) 的完整步骤。
  适用于无 UI 的 Linux 服务器环境。
  当用户需要在 Linux 服务器上安装 gog 工具时触发。
---

# gog Linux Installer

在 CentOS/RHEL 8 上安装 Homebrew 和 gog 的完整指南。

## 概述

本 Skill 包含在 Linux 服务器（特别是 CentOS/RHEL 8）上安装 gog 的完整步骤，包括：
- 创建非 root 用户
- 安装 Homebrew (Linuxbrew)
- 安装 gog
- 配置 Google OAuth 认证

## 安装步骤

### 1. 创建非 root 用户

```bash
sudo adduser smartx
```

### 2. 授予 sudo 权限

```bash
sudo usermod -aG wheel smartx
```

### 3. 设置用户密码

```bash
echo "HC!r0cks" | sudo passwd --stdin smartx
```

### 4. 切换到 smartx 用户并安装 Homebrew

```bash
su - smartx
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 5. 设置 brew 环境变量

```bash
echo >> /home/smartx/.bashrc
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv bash)"' >> /home/smartx/.bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv bash)"
```

### 6. 安装 gog

```bash
brew install steipete/tap/gogcli
```

### 7. 创建 root 软链接（可选）

使 root 用户也能使用 gog：先切回 root，再创建软链接。

```bash
exit   # 从 smartx 会话切回 root
ln -s /home/linuxbrew/.linuxbrew/bin/gog /usr/local/bin/gog
```

### 8. 配置 Google OAuth 凭证

1. 访问 https://console.cloud.google.com/apis/credentials 创建 OAuth 凭证
2. 下载客户端 Secret JSON 文件
3. 执行授权：

```bash
gog auth credentials /path/client_secret_xxx.json
```

### 9. 添加账户和服务

```bash
gog auth add yourname@smartx.com --services drive
```

#### 无 UI 服务器 OAuth 认证

如果是在无 UI 的 Linux 服务器上，需要通过本地浏览器完成 OAuth 认证：

##### 步骤

1. **复制认证 URL 在本机上处理**

   运行 `gog auth add` 命令后会返回一个 OAuth 授权 URL，复制到你的本机（Mac/Linux）访问和授权 Google
   会跳转到到 http://127.0.0.1:<PORT>/oauth2/callback?state=... 这种 url，请记录这个 Port

2. **本地根据端口号执行 SSH 隧道**

   在你的本机（Mac/Linux）上执行：

   ```bash
   ssh -L <PORT>:127.0.0.1:<PORT> root@linux服务器IP
   ```

3. **本机浏览器刷新认证后页面**

   在本机浏览器刷新一下 http://127.0.0.1:<PORT>/oauth2/callback?state=... 的页面（SSH 隧道会将请求转发到服务器）

4. **完成认证**

   在浏览器中完成 Google 账号授权后，服务器端会自动接收验证结果

### 10. 验证安装

```bash
gog drive search "周报" --max 10
```

## 常见问题

### Homebrew 安装失败

- 确保系统已安装依赖：`sudo yum install curl git`
- 可能需要先安装 Developer Tools

### OAuth 认证失败

- 确认 OAuth 凭证的 redirect URI 配置正确
- 检查 SSH 隧道是否正常建立
- 确认端口号一致

### 权限问题

- 确保 smartx 用户对 ~/.gog 目录有写权限

---

*参考来源：gog 官方文档 + CentOS 8 实测*
