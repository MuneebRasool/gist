import Sidebar from '@/components/app/Sidebar';

export default function DashBoardLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<div className="min-h-screen bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-rose-100/80 via-white to-blue-100/80">
			<Sidebar />
			<main className="ml-16 min-h-screen p-8">
				<div className="mx-auto max-w-7xl">
					{children}
				</div>
			</main>
		</div>
	);
}
