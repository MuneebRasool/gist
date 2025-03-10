'use client';

import Sidebar from '@/components/app/Sidebar';
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
		<div className='flex h-dvh bg-gradient-to-r from-[#e6dcda] via-[#cfc6cb] to-[#ced4d8]'>
			<Sidebar />
			<main
				className={`h-dvh flex-1 overflow-y-auto p-8 pt-24 transition-all duration-300 ${sidebarCollapsed ? 'pl-20' : 'pl-60'}`}
			>
				<div className='mx-auto max-w-7xl'>{children}</div>
				{/* <ScrollBar orientation='vertical' /> */}
			</main>
		</div>
	);
}
