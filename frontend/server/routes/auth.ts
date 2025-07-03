import Router from 'koa-router';
import { Context } from 'koa';

const router = new Router();

// 登录
router.post('/login', async (ctx: Context) => {
  const { username, password } = ctx.request.body;

  if (!username || !password) {
    ctx.status = 400;
    ctx.body = {
      success: false,
      message: '用户名和密码不能为空'
    };
    return;
  }

  // 模拟用户验证
  if (username === 'admin' && password === '123456') {
    // 设置会话
    ctx.session.user = {
      id: 1,
      username: 'admin',
      role: 'admin',
      loginTime: new Date().toISOString()
    };

    ctx.body = {
      success: true,
      data: {
        user: ctx.session.user,
        token: 'mock-jwt-token-' + Date.now()
      },
      message: '登录成功'
    };
  } else {
    ctx.status = 401;
    ctx.body = {
      success: false,
      message: '用户名或密码错误'
    };
  }
});

// 登出
router.post('/logout', async (ctx: Context) => {
  ctx.session = null;
  ctx.body = {
    success: true,
    message: '登出成功'
  };
});

// 获取当前用户信息
router.get('/profile', async (ctx: Context) => {
  if (!ctx.session.user) {
    ctx.status = 401;
    ctx.body = {
      success: false,
      message: '未登录'
    };
    return;
  }

  ctx.body = {
    success: true,
    data: ctx.session.user,
    message: '获取用户信息成功'
  };
});

// 检查登录状态
router.get('/check', async (ctx: Context) => {
  ctx.body = {
    success: true,
    data: {
      isLoggedIn: !!ctx.session.user,
      user: ctx.session.user || null
    },
    message: '检查登录状态成功'
  };
});

export default router; 