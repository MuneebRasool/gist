export const envConfig = {
	GOOGLE_CLIENT_ID: process.env.GOOGLE_CLIENT_ID || 'my-google-client-id',
	GOOGLE_CLIENT_SECRET: process.env.GOOGLE_CLIENT_SECRET || 'my-google-client-secret',
	NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET || 'my-secret',
	NEXTAUTH_URL: process.env.NEXTAUTH_URL || 'http://localhost:3000',
	APP_URL: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',
	API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
	NODE_ENV: process.env.NODE_ENV || 'development',
};
