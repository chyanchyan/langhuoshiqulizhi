import { Context } from 'koa';

// 扩展Context类型
export interface AppContext extends Context {
  session: {
    user?: User;
  };
  state: {
    user?: User;
  };
}

// 用户类型
export interface User {
  id: number;
  username: string;
  role: string;
  loginTime: string;
}

// API响应类型
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message: string;
  timestamp?: string;
}

// 分页类型
export interface Pagination {
  page: number;
  limit: number;
  total: number;
}

// 分页响应类型
export interface PaginatedResponse<T> extends ApiResponse<{
  list: T[];
  pagination: Pagination;
}> {} 