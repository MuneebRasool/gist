import React from 'react';
import { Button } from '@/components/ui/button';
import { Library, Inbox } from 'lucide-react';
import Link from 'next/link';

const FloatingButtons: React.FC = () => {
	return (
		<div className='flex w-full gap-4'>
			<Link href='/app/dashboard/library' className='flex-1'>
				<Button
					className='flex h-14 w-full items-center justify-center gap-2 rounded-2xl bg-background/40 text-lg font-medium backdrop-blur-md transition-all duration-200 hover:bg-background/50'
					variant='ghost'
				>
					<Library className='h-5 w-5' />
					Library
				</Button>
			</Link>
			<Link href='/app/dashboard/drawer' className='flex-1'>
				<Button
					className='flex h-14 w-full items-center justify-center gap-2 rounded-2xl bg-background/40 text-lg font-medium backdrop-blur-md transition-all duration-200 hover:bg-background/50'
					variant='ghost'
				>
					<Inbox className='h-5 w-5' />
					Drawer
				</Button>
			</Link>
		</div>
	);
};

export default FloatingButtons;
