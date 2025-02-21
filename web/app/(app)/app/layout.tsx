import FloatingFooter from '@/components/app/FloatingNavbar';

export default function DashBoardLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<div className='h-dvh overflow-y-auto'>
			{children}
			<FloatingFooter />
		</div>
	);
}
