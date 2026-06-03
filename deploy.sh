#!/bin/bash
# ==================================
# 八字排盘部署脚本
# 使用方法: bash deploy.sh
# ==================================
set -e

echo "=== 1. 构建前端 ==="
cd apps/web
npm install
npm run build
cd ../..

echo "=== 2. 构建并启动 Docker 服务 ==="
docker compose up -d --build

echo "=== 3. 完成！==="
echo "访问 http://你的服务器IP 查看应用"
echo "访问 http://你的服务器IP/api/v1/health 测试API"
