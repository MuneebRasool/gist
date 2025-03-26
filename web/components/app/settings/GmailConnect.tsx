'use client';
import GmailIcon from '@/assets/GmailIcon';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { NylasAuthService } from '@/services/nylas/auth.service';
import { useNylasStatusStore } from '@/store';
import { Check, Loader2 } from 'lucide-react';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import { toast } from 'sonner';

const GmailConnect = () => {
	const { isConnected, isLoading, email } = useNylasStatusStore();
	const [loading, setLoading] = useState(false);
	const router = useRouter();
	const handleGmailConnect = async () => {
		if (isConnected || isLoading) return;
		try {
			setLoading(true);
			const res = await NylasAuthService.getAuthUrl();
			if (res.error) {
				toast.error(res.error.message);
			} else {
				router.push(res.data?.url ?? '');
			}
		} catch (error) {
			console.log(error);
		} finally {
			setLoading(false);
		}
	};
	return (
		<Card className='w-full border-none bg-transparent shadow-none'>
			<CardHeader className='px-2 py-4'>
				<CardTitle className='font-urbanist text-xl font-semibold'>Gmail Integration</CardTitle>
				<CardDescription>Connect Your Gmail</CardDescription>
			</CardHeader>
			<CardContent className='px-2'>
				<div className='flex flex-col gap-2'>
					<div>
						{isLoading ? (
							<Button className='flex items-center gap-3' variant='outline'>
								<Loader2 className='animate-spin' />
								Loading...
							</Button>
						) : isConnected ? (
							<div className='flex flex-col gap-2'>
								<Button variant='outline' className='flex w-fit items-center gap-3 font-medium'>
									<span className='flex items-center gap-3 text-green-500'>
										<div className='relative flex items-center'>
											<div className='h-2 w-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]' />
											<div className='absolute -left-0.5 -top-0.5 h-3 w-3 animate-ping rounded-full bg-green-500/40' />
											<div className='absolute h-2 w-2 animate-pulse rounded-full bg-green-500/60' />
										</div>
										{email}
									</span>
								</Button>
							</div>
						) : (
							<Button variant='outline' className='flex items-center gap-3' onClick={handleGmailConnect}>
								{loading ? <Loader2 className='animate-spin' /> : <GmailIcon />}
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
