'use client';
import {
	Home,
	ListTodo,
	Bell,
	User,
	Mic,
	ChevronLeft,
	ChevronRight,
	Menu,
	Settings,
	LogOut,
	Rows2,
	Book,
} from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { useState, useEffect } from 'react';
import { signOut } from 'next-auth/react';

const navItems = [
	{ icon: Home, label: 'Home', href: '/app/dashboard' },
	{ icon: Rows2, label: 'Drawer', href: '/app/dashboard/drawer' },
	{ icon: Book, label: 'Library', href: '/app/dashboard/library' },
	{ icon: Bell, label: 'Notifications', href: '/app/dashboard/notifications' },
	{ icon: Settings, label: 'Settings', href: '/app/dashboard/settings' },
];

interface SidebarProps {
	topOffset?: number;
}

// Create a custom event for sidebar collapse state
const SIDEBAR_COLLAPSE_EVENT = 'sidebar-collapse-change';

export default function Sidebar({ topOffset = 0 }: SidebarProps) {
	const pathname = usePathname();
	const [isCollapsed, setIsCollapsed] = useState(false);

	// Emit custom event when collapsed state changes
	useEffect(() => {
		const event = new CustomEvent(SIDEBAR_COLLAPSE_EVENT, {
			detail: { isCollapsed },
		});
		window.dispatchEvent(event);
	}, [isCollapsed]);

	return (
		<aside
			className={cn(
				'fixed left-0 ml-4 flex h-[calc(100vh-120px)] flex-col pb-5 backdrop-blur-sm transition-all duration-300',
				isCollapsed ? 'w-16' : 'w-56'
			)}
			style={{ top: `calc(${topOffset}px + 120px)` }}
		>
			<div className='flex flex-col items-center gap-6'>
				<div className={`flex ${isCollapsed ? 'justify-center' : 'w-full justify-start px-4'}`}>
					<button
						onClick={() => setIsCollapsed(!isCollapsed)}
						className={cn(
							'flex h-12 w-12 items-center justify-center gap-3 rounded-xl text-muted-foreground hover:bg-white/30'
						)}
					>
						{isCollapsed ? <ChevronRight size={24} /> : <ChevronLeft size={24} />}
					</button>
				</div>
				{navItems.map((item) => (
					<Link
						key={item.href}
						href={item.href}
						className={cn(
							'group relative flex h-12 items-center gap-3 rounded-xl px-3 transition-all duration-200 hover:bg-white/30',
							pathname === item.href ? 'bg-white/30' : 'text-muted-foreground',
							isCollapsed ? 'w-12 justify-center' : 'w-48 justify-start'
						)}
					>
						<item.icon className='h-6 w-6 transition-transform duration-200 group-hover:scale-110' />
						{!isCollapsed && <span className='font-medium'>{item.label}</span>}
					</Link>
				))}
			</div>

			<div className='mt-auto flex justify-center'>
				<button
					onClick={() => {
						signOut();
					}}
					className={cn(
						'flex h-12 items-center gap-3 rounded-xl text-gray-600 transition-all duration-200 hover:bg-white/30',
						isCollapsed ? 'w-12 justify-center' : 'w-48 justify-start px-3'
					)}
				>
					<LogOut className='h-6 w-6' />
					{!isCollapsed && <span className='font-medium'>Logout</span>}
				</button>
			</div>
		</aside>
	);
}
