import type { Metadata } from 'next';
import './globals.css';
import Loading from './loading';
import { Suspense } from 'react';
import Providers from './providers';
import FloatingFooter from '@/components/app/FloatingNavbar';
import { Background } from '@/components/app/Background';

export const metadata: Metadata = {
	title: 'Gist',
	description: 'Gist a task management app',
	appleWebApp: {
		title: 'Gist',
	},
};

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang='en' suppressHydrationWarning>
			<body className={`antialiased`}>
				<Providers>
					<Background />
					<Suspense fallback={<Loading />}>{children}</Suspense>
				</Providers>
			</body>
		</html>
	);
}
