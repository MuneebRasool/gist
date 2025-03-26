'use client';
import React from 'react';
import Link from 'next/link';
import { Frown, Home, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';

const NotFoundPage = () => {
	return (
		<div className='flex min-h-screen items-center justify-center p-4'>
			<div className='w-full max-w-md space-y-8 rounded-xl bg-background/70 p-8 shadow-lg backdrop-blur-sm'>
				<div className='text-center'>
					<div className='mb-6 flex justify-center'>
						<Frown className='h-16 w-16 text-muted-foreground' />
					</div>
					<h1 className='mb-2 text-3xl font-bold text-foreground'>404 - Page Not Found</h1>
					<p className='text-muted-foreground'>Oops! The page you&apos;re looking for doesn&apos;t exist.</p>
				</div>

				<div className='rounded-lg border border-border/20 bg-background/30 p-6'>
					<p className='text-muted-foreground'>
						The requested URL might have been removed, renamed, or temporarily unavailable.
					</p>
				</div>

				<div className='flex flex-col space-y-4'>
					<Button asChild variant='default' className='w-full'>
						<Link href='/'>
							<Home className='mr-2 h-4 w-4' />
							Return to Home
						</Link>
					</Button>
					<Button variant='outline' className='w-full' onClick={() => window.history.back()}>
						<ArrowLeft className='mr-2 h-4 w-4' />
						Go Back
					</Button>
				</div>
			</div>
		</div>
	);
};

export default NotFoundPage;
