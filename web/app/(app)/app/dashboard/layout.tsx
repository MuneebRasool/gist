'use client';

import Sidebar from '@/components/app/Sidebar';
import { useState, useEffect } from 'react';
import { Mic } from 'lucide-react';

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

		window.addEventListener(SIDEBAR_COLLAPSE_EVENT, handleSidebarChange as EventListener);
		return () => {
			window.removeEventListener(SIDEBAR_COLLAPSE_EVENT, handleSidebarChange as EventListener);
		};
	}, []);

	return (
		<div className='min-h-dvh bg-gradient-to-r from-[#e6dcda] via-[#cfc6cb] to-[#ced4d8]'>
			<div className="w-full px-8 pt-6">
				<div className="flex items-center gap-2 mb-4">
					<div className="h-8 w-8 rounded-full bg-gray-400/20"></div>
					<div className="text-lg text-gray-600">
						Press <kbd className="rounded bg-gray-200/20 px-1.5 py-0.5 text-sm">⌘</kbd> + <kbd className="rounded bg-gray-200/20 px-1.5 py-0.5 text-sm">K</kbd> to chat with Gist or add the <kbd className="rounded bg-gray-200/20 px-1.5 py-0.5 text-sm">Space Bar</kbd> to talk
					</div>
					<div className="ml-auto">
						<button className="rounded-full bg-gray-400/20 p-2 hover:bg-gray-400/30">
							<Mic className="h-5 w-5 text-gray-600" />
						</button>
					</div>
				</div>
			</div>
			<div className='flex'>
				<Sidebar topOffset={0} />
				<div className={`flex-1 transition-all duration-300 ${sidebarCollapsed ? 'pl-20' : 'pl-60'}`}>
					<div className='h-[calc(100vh-120px)] overflow-y-auto'>
						<div className='mx-auto max-w-7xl px-8 h-full'>
							{children}
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}