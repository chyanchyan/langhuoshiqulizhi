export const config = {
  // 服务器配置
  server: {
    port: process.env.PORT || 3001,
    host: process.env.HOST || 'localhost'
  },
  
  // 会话配置
  session: {
    key: 'SESSIONID',
    maxAge: 86400000, // 24小时
    autoCommit: true,
    overwrite: true,
    httpOnly: true,
    signed: true,
    rolling: false,
    renew: false,
    secure: process.env.NODE_ENV === 'production',
    sameSite: null
  },
  
  // CORS配置
  cors: {
    origin: ['http://localhost:3000', 'http://localhost:3001'],
    credentials: true
  },
  
  // 代理配置
  proxy: {
    timeout: 10000,
    maxFileSize: 200 * 1024 * 1024 // 200MB
  },
  
  // 数据库配置（如果需要）
  database: {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432'),
    username: process.env.DB_USERNAME || 'postgres',
    password: process.env.DB_PASSWORD || 'password',
    database: process.env.DB_NAME || 'myapp'
  }
};

export default config; 