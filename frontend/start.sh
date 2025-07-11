#!/bin/bash

# 构建前端应用
echo "构建前端应用..."
npm run build

# 启动Koa服务器
echo "🚀 启动Koa服务器..."
npm run server 