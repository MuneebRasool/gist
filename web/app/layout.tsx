import type { Metadata } from 'next';
import './globals.css';
import Loading from './loading';
import { Suspense } from 'react';
import Providers from './providers';
import FloatingFooter from '@/components/app/FloatingNavbar';

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
					<Suspense fallback={<Loading />}>
						{children}
					</Suspense>
					<FloatingFooter />
				</Providers>
			</body>
		</html>
	);
}
