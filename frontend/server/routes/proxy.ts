import Router from 'koa-router';
import { Context } from 'koa';
import axios, { AxiosError } from 'axios';

const router = new Router();

// 代理中间件
const proxyMiddleware = async (ctx: Context, next: () => Promise<any>) => {
  const targetUrl = ctx.request.header['x-target-url'] as string;
  
  if (!targetUrl) {
    ctx.status = 400;
    ctx.body = {
      success: false,
      message: '缺少目标URL'
    };
    return;
  }

  try {
    const method = ctx.method.toLowerCase();
    const headers = { ...ctx.request.header };
    delete headers['x-target-url']; // 删除自定义头部
    
    const config = {
      method,
      url: targetUrl,
      headers,
      data: method !== 'get' ? ctx.request.body : undefined,
      params: method === 'get' ? ctx.query : undefined,
      timeout: 10000
    };

    const response = await axios(config);
    
    ctx.status = response.status;
    ctx.body = response.data;
    
    // 复制响应头
    Object.keys(response.headers).forEach(key => {
      ctx.set(key, response.headers[key]);
    });
    
  } catch (error) {
    console.error('代理请求失败:', error);
    ctx.status = 500;
    ctx.body = {
      success: false,
      message: '代理请求失败',
      error: error instanceof AxiosError ? error.message : '未知错误'
    };
  }
};

// 通用代理路由
router.all('*', proxyMiddleware);

// 特定API代理示例
router.get('/external-api', async (ctx: Context) => {
  try {
    const response = await axios.get('https://jsonplaceholder.typicode.com/posts/1');
    ctx.body = {
      success: true,
      data: response.data,
      message: '代理外部API成功'
    };
  } catch (error) {
    ctx.status = 500;
    ctx.body = {
      success: false,
      message: '代理外部API失败',
      error: error instanceof AxiosError ? error.message : '未知错误'
    };
  }
});

export default router; 