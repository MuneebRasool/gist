export default function DashBoardLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return <div className='min-h-dvh bg-gradient-to-r from-[#e6dcda] via-[#cfc6cb] to-[#ced4d8]'>{children}</div>;
}
