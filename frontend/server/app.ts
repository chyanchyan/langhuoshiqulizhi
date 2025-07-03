import Koa from 'koa';
import Router from 'koa-router';
import bodyParser from 'koa-body';
import session from 'koa-session2';
import cors from 'koa-cors';
import serve from 'koa-static';
import path from 'path';

// 导入路由
import apiRoutes from './routes/api';
import authRoutes from './routes/auth';
import proxyRoutes from './routes/proxy';

const app = new Koa();
const PORT = process.env.PORT || 3001;

// 中间件配置
app.use(cors({
  origin: (ctx) => {
    const allowedOrigins = ['http://localhost:3000', 'http://localhost:3001'];
    const origin = ctx.request.header.origin;
    if (origin && allowedOrigins.includes(origin)) {
      return origin;
    }
    return false;
  },
  credentials: true
}));

// 会话配置
app.use(session({
  key: 'SESSIONID',
  maxAge: 86400000, // 24小时
  autoCommit: true,
  overwrite: true,
  httpOnly: true,
  signed: true,
  rolling: false,
  renew: false,
  secure: false, // 开发环境设为false
  sameSite: null
}));

// 请求体解析
app.use(bodyParser({
  multipart: true,
  formidable: {
    maxFileSize: 200 * 1024 * 1024 // 200MB
  }
}));

// 静态文件服务
app.use(serve(path.join(__dirname, '../public')));

// 路由
const router = new Router();

// API路由
router.use('/api', apiRoutes.routes(), apiRoutes.allowedMethods());

// 认证路由
router.use('/auth', authRoutes.routes(), authRoutes.allowedMethods());

// 代理路由
router.use('/proxy', proxyRoutes.routes(), proxyRoutes.allowedMethods());

// 根路由
router.get('/', async (ctx) => {
  ctx.body = {
    message: 'Koa服务器运行正常',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  };
});

// 健康检查
router.get('/health', async (ctx) => {
  ctx.body = {
    status: 'ok',
    timestamp: new Date().toISOString()
  };
});

app.use(router.routes());
app.use(router.allowedMethods());

// 错误处理中间件
app.use(async (ctx, next) => {
  try {
    await next();
  } catch (err) {
    ctx.status = err.status || 500;
    ctx.body = {
      error: err.message || '服务器内部错误',
      timestamp: new Date().toISOString()
    };
    ctx.app.emit('error', err, ctx);
  }
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`🚀 Koa服务器运行在 http://localhost:${PORT}`);
  console.log(`📊 健康检查: http://localhost:${PORT}/health`);
});

export default app; 