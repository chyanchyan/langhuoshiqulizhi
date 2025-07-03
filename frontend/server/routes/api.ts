import Router from 'koa-router';
import { Context } from 'koa';

const router = new Router();

// 用户相关API
router.get('/users', async (ctx: Context) => {
  ctx.body = {
    success: true,
    data: [
      { id: 1, name: '张三', email: 'zhangsan@example.com' },
      { id: 2, name: '李四', email: 'lisi@example.com' }
    ],
    message: '获取用户列表成功'
  };
});

router.get('/users/:id', async (ctx: Context) => {
  const { id } = ctx.params;
  ctx.body = {
    success: true,
    data: {
      id: parseInt(id),
      name: '张三',
      email: 'zhangsan@example.com',
      createdAt: new Date().toISOString()
    },
    message: '获取用户信息成功'
  };
});

router.post('/users', async (ctx: Context) => {
  const { name, email } = ctx.request.body;
  
  if (!name || !email) {
    ctx.status = 400;
    ctx.body = {
      success: false,
      message: '姓名和邮箱不能为空'
    };
    return;
  }

  ctx.body = {
    success: true,
    data: {
      id: Math.floor(Math.random() * 1000),
      name,
      email,
      createdAt: new Date().toISOString()
    },
    message: '创建用户成功'
  };
});

// 数据相关API
router.get('/data', async (ctx: Context) => {
  const { page = 1, limit = 10 } = ctx.query;
  
  ctx.body = {
    success: true,
    data: {
      list: Array.from({ length: parseInt(limit as string) }, (_, i) => ({
        id: i + 1,
        title: `数据项 ${i + 1}`,
        content: `这是第 ${i + 1} 个数据项的内容`,
        createdAt: new Date().toISOString()
      })),
      pagination: {
        page: parseInt(page as string),
        limit: parseInt(limit as string),
        total: 100
      }
    },
    message: '获取数据列表成功'
  };
});

export default router; 