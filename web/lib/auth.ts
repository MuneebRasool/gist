import { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import { compare } from 'bcrypt';
import { NEXTAUTH_SECRET } from '@/config';
import { AuthService } from '@/services/auth.service';

declare module 'next-auth' {
	interface User {
		id: string;
		email: string;
		name: string;
		avatar: string;
		token: string;
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
	}
}

export const authOptions: NextAuthOptions = {
	secret: NEXTAUTH_SECRET,
	session: {
		strategy: 'jwt',
	},
	pages: {
		signIn: '/login',
	},
	providers: [
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
					return null;
				}

				return {
					id: res.data?.user.id ?? '',
					email: res.data?.user.email ?? '',
					name: res.data?.user.name ?? '',
					avatar: res.data?.user.avatar ?? '',
					token: res.data?.access_token ?? '',
				};
			},
		}),
	],
	callbacks: {
		session: ({ session, token }) => {
			return {
				...session,
				user: {
					...session.user,
					id: token.id,
					token: token.token,
					avatar: token.avatar,
				},
			};
		},
		jwt: ({ token, user }) => {
			if (user) {
				return {
					...token,
					id: user.id,
					name: user.name,
					email: user.email,
					avatar: user.avatar,
					token: user.token,
				};
			}
			return token;
		},
	},
};
