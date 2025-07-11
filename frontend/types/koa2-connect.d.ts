declare module 'koa2-connect' {
  import { Context, Next } from 'koa';
  
  export function koaConnect(middleware: any): (ctx: Context, next: Next) => Promise<void>;
} 