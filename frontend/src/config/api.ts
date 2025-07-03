// API配置
const API_CONFIG = {
  // 从环境变量获取API基础URL，如果没有则使用默认值
  BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://172.30.23.175:5000',
  
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