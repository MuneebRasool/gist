'use client';
import React from 'react';
import Link from 'next/link';
import { Frown, Home, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const NotFoundPage = () => {
	return (
		<div className='flex min-h-screen items-center justify-center bg-background p-4'>
			<Card className='w-full max-w-md text-center'>
				<CardHeader>
					<CardTitle className='flex items-center justify-center text-3xl'>
						<Frown className='mr-3 h-12 w-12 text-primary' />
						404 - Page Not Found
					</CardTitle>
					<CardDescription className='text-base'>
						Oops! The page you&apos;re looking for doesn&apos;t exist.
					</CardDescription>
				</CardHeader>
				<CardContent className='space-y-6'>
					<div className='rounded-lg border border-dashed border-primary/20 bg-muted/10 p-6'>
						<p className='text-muted-foreground'>
							The requested URL might have been removed, renamed, or temporarily unavailable.
						</p>
					</div>
					<div className='flex flex-col space-y-4'>
						<Button asChild className='w-full'>
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
				</CardContent>
			</Card>
		</div>
	);
};

export default NotFoundPage;
