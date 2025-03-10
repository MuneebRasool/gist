// import Sidebar from '@/components/app/Sidebar';
// import { Mic } from 'lucide-react';

// export default function DashBoardLayout({
// 	children,
// }: Readonly<{
// 	children: React.ReactNode;
// }>) {
// 	return (
// 		<div className="min-h-screen bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-rose-100/80 via-white to-blue-100/80">
// 			<div className="pt-24 relative">
// 				<div className="absolute left-8 top-8 z-10 flex items-center gap-2 text-gray-600">
// 					<div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-200/50">
// 						<Mic className="h-5 w-5" />
// 					</div>
// 					<span className="text-sm">Press ⌘ + A to chat with Gist or hold the Space Bar to talk</span>
// 				</div>
// 				<Sidebar />
// 				<main className="ml-16 min-h-screen p-8">
// 					<div className="mx-auto max-w-7xl">
// 						{children}
// 					</div>
// 				</main>
// 			</div>
// 		</div>
// 	);
// }
'use client';

import Sidebar from '@/components/app/Sidebar';
import FloatingFooter from '@/components/app/FloatingNavbar';
import { Mic } from 'lucide-react';
import { useState, useEffect } from 'react';

// Match the event name with the one in Sidebar.tsx
const SIDEBAR_COLLAPSE_EVENT = 'sidebar-collapse-change';

export default function DashBoardLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

	// Listen for sidebar collapse events
	useEffect(() => {
		const handleSidebarChange = (event: CustomEvent) => {
			setSidebarCollapsed(event.detail.isCollapsed);
		};

		// Add event listener
		window.addEventListener(SIDEBAR_COLLAPSE_EVENT, handleSidebarChange as EventListener);

		// Clean up
		return () => {
			window.removeEventListener(SIDEBAR_COLLAPSE_EVENT, handleSidebarChange as EventListener);
		};
	}, []);

	return (
		<div className="min-h-screen bg-gradient-to-r from-[#e6dcda] to-[#cfc6cb]">
			{/* Top chat line */}
			<div className="fixed left-8 top-8 z-20 flex items-center gap-3 text-gray-600">
				<div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-200/50">
					<div className="h-9 w-9 rounded-full bg-[#A5B7C8]" />
				</div>
				<span className="pl-1 text-sm">Press ⌘ + A to chat with Gist or hold the Space Bar to talk</span>
			</div>
			
			{/* Content area with sidebar and main content */}
			<div className="flex h-screen">
				<Sidebar topOffset={50} />
				<main 
					className={`flex-1 p-8 pt-24 transition-all duration-300 ${
						sidebarCollapsed ? 'pl-20' : 'pl-60'
					}`}
				>
					<div className="mx-auto max-w-7xl">
						{children}
					</div>
				</main>
			</div>
			
			<FloatingFooter />
		</div>
	);
}