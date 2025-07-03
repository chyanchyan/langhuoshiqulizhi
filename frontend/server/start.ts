import app from './app';
import config from './config';
import http from 'http';

const PORT = parseInt(config.server.port.toString(), 10);
const HOST = config.server.host;

// 使用http.createServer来避免类型问题
const server = http.createServer(app.callback());

server.listen(PORT, HOST, () => {
  console.log(`🚀 Koa服务器启动成功!`);
  console.log(`📍 地址: http://${HOST}:${PORT}`);
  console.log(`📊 健康检查: http://${HOST}:${PORT}/health`);
  console.log(`🔧 环境: ${process.env.NODE_ENV || 'development'}`);
  console.log(`⏰ 启动时间: ${new Date().toLocaleString('zh-CN')}`);
});

// 优雅关闭
process.on('SIGTERM', () => {
  console.log('收到SIGTERM信号，正在关闭服务器...');
  server.close(() => {
    console.log('服务器已关闭');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('收到SIGINT信号，正在关闭服务器...');
  server.close(() => {
    console.log('服务器已关闭');
    process.exit(0);
  });
}); 