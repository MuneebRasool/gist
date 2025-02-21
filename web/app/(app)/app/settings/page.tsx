'use client';
import GmailConnect from '@/components/app/settings/GmailConnect';
import { Separator } from '@/components/ui/separator';
import { Settings2 } from 'lucide-react';
import React from 'react';

const Settings = () => {
	return (
		<div className='mx-auto flex h-full max-w-4xl flex-col gap-3 px-2 py-10 sm:px-5'>
			<div className='flex items-center justify-between gap-4'>
				<div className='space-y-2'>
					<div className='flex items-center space-x-2'>
						<Settings2 className='h-6 w-6 text-primary' />
						<h1 className='text-xl font-semibold'>Settings</h1>
					</div>
					<p className='text-muted-foreground'>Manage all your Settings</p>
				</div>
			</div>
			<Separator />
			<GmailConnect />
			<Separator />
		</div>
	);
};

export default Settings;
