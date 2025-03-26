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
	FolderOpen,
} from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { useState, useEffect } from 'react';

const navItems = [
	{ icon: Home, label: 'Home', href: '/app/dashboard' },
	{ icon: FolderOpen, label: 'Logs', href: '/app/dashboard/logs' },
];

interface SidebarProps {
	children?: React.ReactNode;
}

// Create a custom event for sidebar collapse state
const SIDEBAR_COLLAPSE_EVENT = 'sidebar-collapse-change';

export default function Sidebar({ children }: SidebarProps) {
	const pathname = usePathname();
	const [isCollapsed, setIsCollapsed] = useState(true);

	// Emit custom event when collapsed state changes
	useEffect(() => {
		const event = new CustomEvent(SIDEBAR_COLLAPSE_EVENT, {
			detail: { isCollapsed },
		});
		window.dispatchEvent(event);
	}, [isCollapsed]);

	return (
		<div className='flex h-dvh flex-col gap-4 pt-4'>
			<div className='flex items-center justify-between gap-2 px-8'>
				<div className='flex items-center gap-2'>
					<div className='h-8 w-8 rounded-full bg-gray-400/20'></div>
					<div className='text-lg text-gray-600'>
						Press <kbd className='rounded bg-gray-200/20 px-1.5 py-0.5 text-sm'>⌘</kbd> +{' '}
						<kbd className='rounded bg-gray-200/20 px-1.5 py-0.5 text-sm'>K</kbd> to chat with Gist or add the{' '}
						<kbd className='rounded bg-gray-200/20 px-1.5 py-0.5 text-sm'>Space Bar</kbd> to talk
					</div>
				</div>
				<div>
					<button className='rounded-full bg-gray-400/20 p-2 hover:bg-gray-400/30'>
						<Mic className='h-5 w-5 text-gray-600' />
					</button>
				</div>
			</div>
			<div className='flex flex-1'>
				<aside
					className={cn(
						'ml-4 flex h-full flex-col pb-5 backdrop-blur-sm transition-all duration-300',
						isCollapsed ? 'w-16' : 'w-56'
					)}
				>
					<div className='flex flex-col items-center gap-6'>
						<div className={`flex ${isCollapsed ? 'justify-center' : 'w-full justify-start px-4'}`}>
							<button
								onClick={() => setIsCollapsed(!isCollapsed)}
								className={cn(
									'flex h-12 w-12 items-center justify-center gap-3 rounded-xl text-muted-foreground hover:bg-background/30'
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
									'group relative flex h-12 items-center gap-3 rounded-xl px-3 transition-all duration-200 hover:bg-background/30',
									pathname === item.href ? 'bg-background/30' : 'text-muted-foreground',
									isCollapsed ? 'w-12 justify-center' : 'w-48 justify-start'
								)}
							>
								<item.icon className='h-6 w-6 transition-transform duration-200 group-hover:scale-110' />
								{!isCollapsed && <span className='font-medium'>{item.label}</span>}
							</Link>
						))}
					</div>

					<div className='mt-auto flex justify-center'>
						<Link href='/app/dashboard/settings'>
							<button
								className={cn(
									'flex h-12 items-center gap-3 rounded-xl text-gray-600 transition-all duration-200 hover:bg-background/30',
									isCollapsed ? 'w-12 justify-center' : 'w-48 justify-start px-3'
								)}
							>
								<Settings className='h-6 w-6' />
								{!isCollapsed && <span className='font-medium'>Settings</span>}
							</button>
						</Link>
					</div>
				</aside>
				<div className={`max-h-[calc(100dvh-68px)] flex-1 px-2 transition-all duration-300`}>{children}</div>
			</div>
		</div>
	);
}
