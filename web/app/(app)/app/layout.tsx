import FloatingFooter from '@/components/app/FloatingNavbar';

export default function DashBoardLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<div className="min-h-screen bg-gradient-to-r from-[#e6dcda] via-[#cfc6cb] to-[#ced4d8]">
			{children}
			<FloatingFooter />
		</div>
	);
}