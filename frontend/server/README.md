# Koa服务器

这是一个基于Koa的后端服务器，提供前后端转发、路由管理、请求体解析和会话管理功能。

## 功能特性

- ✅ **路由管理**: 使用koa-router进行路由管理
- ✅ **请求体解析**: 使用koa-body解析JSON、表单数据等
- ✅ **会话管理**: 使用koa-session2管理用户会话
- ✅ **前后端转发**: 支持代理外部API请求
- ✅ **CORS支持**: 跨域请求支持
- ✅ **静态文件服务**: 提供静态文件访问
- ✅ **错误处理**: 统一的错误处理机制
- ✅ **认证中间件**: 用户认证和权限控制
- ✅ **日志记录**: 请求日志记录

## 安装依赖

```bash
npm install
```

## 启动服务器

### 开发模式
```bash
npm run server:dev
```

### 生产模式
```bash
npm run server
```

## API接口

### 认证相关
- `POST /auth/login` - 用户登录
- `POST /auth/logout` - 用户登出
- `GET /auth/profile` - 获取用户信息
- `GET /auth/check` - 检查登录状态

### 用户管理
- `GET /api/users` - 获取用户列表
- `GET /api/users/:id` - 获取指定用户
- `POST /api/users` - 创建新用户

### 数据管理
- `GET /api/data` - 获取数据列表（支持分页）

### 代理功能
- `ALL /proxy/*` - 通用代理路由
- `GET /proxy/external-api` - 外部API代理示例

### 系统接口
- `GET /` - 服务器状态
- `GET /health` - 健康检查

## 使用示例

### 前端调用示例

```javascript
// 登录
const loginResponse = await fetch('/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'admin',
    password: '123456'
  }),
  credentials: 'include'
});

// 获取用户列表
const usersResponse = await fetch('/api/users', {
  credentials: 'include'
});

// 代理请求
const proxyResponse = await fetch('/proxy/external-api', {
  credentials: 'include'
});
```

## 配置说明

配置文件位于 `config/index.ts`，包含：

- 服务器配置（端口、主机）
- 会话配置（过期时间、安全设置）
- CORS配置（允许的域名）
- 代理配置（超时时间、文件大小限制）

## 中间件说明

- `authMiddleware`: 用户认证中间件
- `roleMiddleware`: 角色权限中间件
- `loggerMiddleware`: 日志记录中间件
- `errorHandler`: 错误处理中间件

## 注意事项

1. 开发环境下CORS和会话安全设置较为宽松
2. 生产环境请修改相关安全配置
3. 代理功能需要谨慎使用，避免安全风险
4. 建议在生产环境中使用HTTPS 