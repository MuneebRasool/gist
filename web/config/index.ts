export const appUrl = process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000';
export const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
export const node_env: 'development' | 'production' | 'test' = process.env.NODE_ENV || 'development';

export const NEXTAUTH_SECRET = process.env.NEXTAUTH_SECRET || 'my-secret';
export const NEXTAUTH_URL = process.env.NEXTAUTH_URL || 'http://localhost:3000';
