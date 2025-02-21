import type { Metadata } from 'next';
import './globals.css';
import { Nunito } from 'next/font/google';
import Loading from './loading';
import { Suspense } from 'react';
import Providers from './providers';

const nunito = Nunito({
	subsets: ['latin'],
});

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
			<body className={`${nunito.className} antialiased`}>
				<Suspense fallback={<Loading />}>
					<Providers>{children}</Providers>
				</Suspense>
			</body>
		</html>
	);
}
