import type { Metadata } from 'next';
import './globals.css';
import Loading from './loading';
import { Suspense } from 'react';
import Providers from './providers';

export const metadata: Metadata = {
	title: 'Gist',
	description: 'Gist a task management app',
	appleWebApp: {
		title: 'Gist',
	},
};

export default async function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang='en' suppressHydrationWarning>
			<body className={`antialiased`}>
				<Suspense fallback={<Loading />}>
					<Providers>{children}</Providers>
				</Suspense>
			</body>
		</html>
	);
}
