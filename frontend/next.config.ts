import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: true,
  
  // 开发环境配置
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:5000/api/:path*', // 开发时直接代理到后端
      },
    ];
  },
  
  // 输出配置
  output: 'export', // 静态导出，配合Koa服务器使用
  
  // 禁用图片优化（因为使用静态导出）
  images: {
    unoptimized: true,
  },
  
  // 环境变量
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:3000',
  },
};

export default nextConfig;
