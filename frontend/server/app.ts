import Koa from 'koa';
import Router from 'koa-router';
import cors from 'koa-cors';
import bodyParser from 'koa-body';
import serve from 'koa-static';
import path from 'path';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { koaConnect } from 'koa2-connect';

const app = new Koa();
const router = new Router();

// 中间件配置
app.use(cors({
  origin: '*',
  credentials: true
}));

app.use(bodyParser({
  multipart: true,
  formidable: {
    maxFileSize: 200 * 1024 * 1024 // 200MB
  }
}));

// 静态文件服务
app.use(serve(path.join(__dirname, '../public')));
app.use(serve(path.join(__dirname, '../.next/static')));

// API代理配置
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:5000';

// 创建代理中间件
const proxyMiddleware = createProxyMiddleware({
  target: API_BASE_URL,
  changeOrigin: true,
  pathRewrite: {
    '^/api': '/api' // 保持API路径不变
  },
  onProxyReq: (proxyReq, req, res) => {
    console.log(`代理请求: ${req.method} ${req.url} -> ${API_BASE_URL}${req.url}`);
  },
  onProxyRes: (proxyRes, req, res) => {
    console.log(`代理响应: ${proxyRes.statusCode} ${req.url}`);
  },
  onError: (err, req, res) => {
    console.error('代理错误:', err);
  }
});

// 将代理中间件转换为Koa中间件
const koaProxy = koaConnect(proxyMiddleware);

// API路由 - 转发到后端
router.all('/api/*', async (ctx, next) => {
  await koaProxy(ctx, next);
});

// 健康检查端点
router.get('/health', async (ctx) => {
  ctx.body = { status: 'ok', message: 'Koa服务器运行正常' };
});

// 前端路由处理 - 返回index.html
router.get('*', async (ctx, next) => {
  if (ctx.path.startsWith('/_next') || ctx.path.startsWith('/api')) {
    return await next();
  }
  
  // 对于其他路由，返回前端应用
  ctx.type = 'text/html';
  ctx.body = `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>失去理智</title>
      </head>
      <body>
        <div id="__next"></div>
        <script src="/_next/static/chunks/main.js"></script>
      </body>
    </html>
  `;
});

app.use(router.routes());
app.use(router.allowedMethods());

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`🚀 Koa服务器运行在 http://localhost:${PORT}`);
  console.log(`📡 API代理目标: ${API_BASE_URL}`);
  console.log(`🌐 前端应用: http://localhost:${PORT}`);
});

export default app; 