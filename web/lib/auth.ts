import { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import GoogleProvider from 'next-auth/providers/google';
import { envConfig } from '@/config';
import { AuthService } from '@/services/auth.service';

declare module 'next-auth' {
	interface User {
		id: string;
		email: string;
		name: string;
		avatar: string;
		token: string;
		onboarding?: boolean;
		nylas_email?: string;
	}
	interface Session {
		user: User;
	}
}

declare module 'next-auth/jwt' {
	interface JWT {
		id: string;
		token: string;
		email: string;
		name: string;
		avatar: string;
		onboarding?: boolean;
		nylas_email?: string;
	}
}

export const authOptions: NextAuthOptions = {
	secret: envConfig.NEXTAUTH_SECRET,
	session: {
		strategy: 'jwt',
	},
	pages: {
		signIn: '/login',
	},
	providers: [
		GoogleProvider({
			clientId: envConfig.GOOGLE_CLIENT_ID!,
			clientSecret: envConfig.GOOGLE_CLIENT_SECRET!,
		}),
		CredentialsProvider({
			name: 'Credentials',
			credentials: {
				email: { label: 'Email', type: 'email' },
				password: { label: 'Password', type: 'password' },
			},
			async authorize(credentials) {
				if (!credentials?.email || !credentials?.password) {
					return null;
				}

				const res = await AuthService.login(credentials.email, credentials.password);

				if (res.error) {
					throw new Error(res.error.message);
				}

				return {
					id: res.data?.user.id ?? '',
					email: res.data?.user.email ?? '',
					name: res.data?.user.name ?? '',
					avatar: res.data?.user.avatar ?? '',
					token: res.data?.access_token ?? '',
					onboarding: res.data?.user.onboarding,
					nylas_email: res.data?.user.nylas_email,
				};
			},
		}),
	],
	callbacks: {
		async signIn({ user, account }) {
			if (account?.provider === 'google') {
				try {
					const response = await AuthService.googleAuth({
						id_token: account.id_token!,
						user_data: {
							email: user.email,
							name: user.name,
							picture: user.image || undefined,
						},
					});
					if (response.data) {
						user.id = response.data.user.id;
						user.token = response.data.access_token;
						user.avatar = response.data.user.avatar ?? '';
						user.email = response.data.user.email;
						user.name = response.data.user.name;
						user.onboarding = response.data.user.onboarding;
						user.nylas_email = response.data.user.nylas_email;
						return true;
					}
				} catch (error) {
					console.error('Google auth error:', error);
					return false;
				}
			}
			return true;
		},
		session: ({ session, token }) => {
			return {
				...session,
				user: {
					...session.user,
					id: token.id,
					token: token.token,
					avatar: token.avatar,
					onboarding: token.onboarding,
					nylas_email: token.nylas_email,
				},
			};
		},
		jwt: ({ token, user, trigger, session }) => {
			if (trigger === 'update') {
				return { ...token, onboarding: session?.onboarding };
			}
			if (user) {
				return {
					...token,
					id: user.id,
					name: user.name,
					email: user.email,
					avatar: user.avatar,
					token: user.token,
					onboarding: user.onboarding,
					nylas_email: user.nylas_email,
				};
			}
			return token;
		},
	},
};
