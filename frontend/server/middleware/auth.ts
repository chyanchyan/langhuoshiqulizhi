import { Context, Next } from 'koa';

// 认证中间件
export const authMiddleware = async (ctx: Context, next: Next) => {
  // 检查会话中的用户信息
  if (!ctx.session.user) {
    ctx.status = 401;
    ctx.body = {
      success: false,
      message: '请先登录'
    };
    return;
  }

  // 将用户信息添加到ctx.state中，供后续中间件使用
  ctx.state.user = ctx.session.user;
  
  await next();
};

// 角色验证中间件
export const roleMiddleware = (requiredRole: string) => {
  return async (ctx: Context, next: Next) => {
    if (!ctx.state.user) {
      ctx.status = 401;
      ctx.body = {
        success: false,
        message: '请先登录'
      };
      return;
    }

    if (ctx.state.user.role !== requiredRole) {
      ctx.status = 403;
      ctx.body = {
        success: false,
        message: '权限不足'
      };
      return;
    }

    await next();
  };
};

// 日志中间件
export const loggerMiddleware = async (ctx: Context, next: Next) => {
  const start = Date.now();
  
  await next();
  
  const ms = Date.now() - start;
  const log = `${ctx.method} ${ctx.url} - ${ctx.status} - ${ms}ms`;
  
  console.log(log);
}; 