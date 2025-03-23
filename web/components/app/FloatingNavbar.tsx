'use client';
import React, { useEffect, useRef, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Home, Plus } from 'lucide-react';
import Link from 'next/link';
import { signOut, useSession } from 'next-auth/react';
import {
	AlertDialog,
	AlertDialogAction,
	AlertDialogCancel,
	AlertDialogContent,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogTitle,
} from '../ui/alert-dialog';
import ProfileDropdown from './ProfileDropdown';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '../ui/tooltip';

const FloatingFooter = () => {
	const [open, setOpen] = useState(false);
	return (
		<TooltipProvider>
			<div
				className={`fixed bottom-3 left-1/2 -translate-x-1/2 transform rounded-full border bg-card/95 p-2 opacity-100 shadow-lg backdrop-blur transition-all duration-300 ease-in-out hover:shadow-xl supports-[backdrop-filter]:bg-card/60`}
			>
				<nav className='relative flex items-center gap-8 px-4'>
					<Link href='/app'>
						<Button
							variant='ghost'
							size='icon'
							className='h-9 w-9 transition-all duration-300 hover:scale-110 hover:bg-muted/80'
						>
							<Home className='h-5 w-5' />
							<span className='sr-only'>Home</span>
						</Button>
					</Link>

					<Tooltip delayDuration={0}>
						<TooltipTrigger asChild>
							<Button
								variant='ghost'
								size='icon'
								className='group relative scale-110 transform rounded-full bg-primary text-primary-foreground shadow-lg transition-all duration-300 hover:scale-125 hover:bg-primary hover:text-primary-foreground hover:shadow-xl'
							>
								<Plus className='h-6 w-6 transition-transform duration-300 group-hover:rotate-90' />
								<span className='sr-only'>New Project</span>
							</Button>
						</TooltipTrigger>
						<TooltipContent side='top' align='center'>
							Create Task
						</TooltipContent>
					</Tooltip>

					<ProfileDropdown setOpen={setOpen} />
				</nav>
			</div>
			<AlertDialog open={open} onOpenChange={setOpen}>
				<AlertDialogContent>
					<AlertDialogHeader>
						<AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
						<AlertDialogDescription>This action will log you out of your account.</AlertDialogDescription>
					</AlertDialogHeader>
					<AlertDialogFooter>
						<AlertDialogCancel>Cancel</AlertDialogCancel>
						<AlertDialogAction
							onClick={async () => {
								await signOut({ callbackUrl: '/login' });
							}}
						>
							Logout
						</AlertDialogAction>
					</AlertDialogFooter>
				</AlertDialogContent>
			</AlertDialog>
		</TooltipProvider>
	);
};

export default FloatingFooter;
