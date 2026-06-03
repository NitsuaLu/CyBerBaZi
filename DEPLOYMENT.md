# 八字排盘 — 部署指南

## 前置条件

你需要准备：

- **一台云服务器**（阿里云 ECS / 腾讯云 CVM），1核1G 最低配即可
- **一个域名**（在阿里云/腾讯云购买）
- 服务器安装 Docker 和 Docker Compose

## 第一步：购买域名和服务器

1. 去 [阿里云](https://www.aliyun.com) 或 [腾讯云](https://cloud.tencent.com) 注册账号
2. 购买一个域名，比如 `bazi.example.com`（约 30-60 元/年）
3. 购买一台云服务器，最低配置即可（新用户约 50-100 元/年）
   - 操作系统选 **Ubuntu 22.04** 或 **CentOS 8**
   - 记住服务器公网 IP

## 第二步：域名解析

在域名管理后台添加一条 DNS 记录：

| 类型 | 主机记录 | 记录值 |
|------|----------|--------|
| A    | @        | 你的服务器公网IP |

## 第三步：服务器安装 Docker

SSH 登录服务器后执行：

```bash
# 安装 Docker
curl -fsSL https://get.docker.com | bash

# 启动 Docker
systemctl start docker
systemctl enable docker

# 安装 Docker Compose
apt update && apt install docker-compose -y
```

## 第四步：上传代码

在本地电脑上：

```bash
# 1. 先构建前端
cd D:/CyBerBaZi/apps/web
npm install && npm run build

# 2. 上传到服务器（替换为你服务器的IP和用户名）
cd D:/CyBerBaZi
scp -r . root@你的服务器IP:/opt/bazi

# 如果 scp 不可用，可以用 git clone 或 FTP 上传
```

## 第五步：配置并启动

在服务器上：

```bash
cd /opt/bazi

# 1. 修改域名
sed -i 's/your-domain.com/你的真实域名/g' nginx.conf

# 2. 启动服务
chmod +x deploy.sh
bash deploy.sh
```

## 第六步：配置 SSL（HTTPS）

```bash
# 安装 Certbot
apt install certbot python3-certbot-nginx -y

# 自动获取并配置 SSL 证书
certbot --nginx -d 你的域名

# 证书到期会自动续期
```

## 访问

打开浏览器访问 `https://你的域名` 即可。

## 日常维护

```bash
# 查看日志
docker compose logs -f

# 重启服务
docker compose restart

# 更新代码后重新部署
cd /opt/bazi
bash deploy.sh
```
