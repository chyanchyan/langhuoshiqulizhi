import { Context, Next } from 'koa';

// 错误处理中间件
export const errorHandler = async (ctx: Context, next: Next) => {
  try {
    await next();
  } catch (err) {
    console.error('服务器错误:', err);
    
    // 类型守卫
    const isError = (error: unknown): error is Error & { status?: number } => {
      return error instanceof Error;
    };
    
    const error = isError(err) ? err : new Error('未知错误');
    
    ctx.status = (error as any).status || 500;
    ctx.body = {
      success: false,
      message: error.message || '服务器内部错误',
      timestamp: new Date().toISOString()
    };
    
    // 触发错误事件
    ctx.app.emit('error', error, ctx);
  }
};

// 404处理中间件
export const notFoundHandler = async (ctx: Context) => {
  ctx.status = 404;
  ctx.body = {
    success: false,
    message: '请求的资源不存在',
    path: ctx.path,
    timestamp: new Date().toISOString()
  };
}; 