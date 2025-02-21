'use client';
import GmailIcon from '@/assets/GmailIcon';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import React, { useState } from 'react';

const GmailConnect = () => {
	const [gmailConnected, setGmailConnected] = useState(false);
	const handleGmailConnect = () => {
		setGmailConnected(!gmailConnected);
	};
	return (
		<Card className='w-full border-none bg-background shadow-none'>
			<CardHeader className='px-0 py-4'>
				<CardTitle>Gmail Integration</CardTitle>
				<CardDescription>Connect Your Gmail</CardDescription>
			</CardHeader>
			<CardContent className='px-0'>
				<div className='flex flex-col gap-2'>
					<div>
						{gmailConnected ? (
							<div className='flex items-center gap-2'>
								<Button variant='outline' className='flex items-center gap-3 font-medium'>
									<GmailIcon />
									<span className='flex items-center gap-2 text-green-500'>
										<span className='h-2 w-2 animate-pulse rounded-full bg-green-500'></span>
										Connected
									</span>
								</Button>
							</div>
						) : (
							<Button variant='outline' className='flex items-center gap-3' onClick={handleGmailConnect}>
								<GmailIcon />

								<p className='text-lg font-medium'>Connect your Email</p>
							</Button>
						)}
					</div>
					<p className='text-sm text-muted-foreground'>
						Connecting your email allows you to automate your outreach by sending emails directly from mail-merge.
					</p>
				</div>
			</CardContent>
		</Card>
	);
};

export default GmailConnect;
