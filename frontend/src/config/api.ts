// API配置
const API_CONFIG = {
  // 使用相对路径，通过Koa代理转发
  BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || '',

  // API端点
  ENDPOINTS: {
    AUTH: '/api/enterAuth',
    HEALTH: '/api/health',
    PLAYER_RECORD: '/api/getPlayerRecord',
    UPLOAD_PIC: '/api/uploadRecordPic'
  }
};

// 获取完整的API URL
export const getApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};

// 导出配置
export default API_CONFIG; 