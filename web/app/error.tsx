'use client';
import React from 'react';
import { AlertTriangle, Home, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

interface ErrorProps {
	error: Error & { digest?: string };
	reset: () => void;
}

const ErrorPage: React.FC<ErrorProps> = ({ error, reset }) => {
	return (
		<div className='flex min-h-screen items-center justify-center bg-background p-4'>
			<Card className='w-full max-w-md'>
				<CardHeader className='text-center'>
					<CardTitle className='mb-4 flex items-center justify-center'>
						<AlertTriangle className='mr-2 h-12 w-12 text-destructive' />
						Error Occurred
					</CardTitle>
					<CardDescription>Something unexpected happened</CardDescription>
				</CardHeader>
				<CardContent className='space-y-6'>
					<div className='rounded-lg bg-muted/50 p-4'>
						<p className='break-words text-sm text-muted-foreground'>{error.message || 'An unknown error occurred'}</p>
						{error.digest && <p className='mt-2 text-xs text-muted-foreground'>Error ID: {error.digest}</p>}
					</div>

					<div className='flex justify-center space-x-4'>
						<Button variant='outline' className='w-full' onClick={() => reset()}>
							<RefreshCw className='mr-2 h-4 w-4' />
							Try Again
						</Button>
						<Button variant='secondary' className='w-full' asChild>
							<a href='/'>
								<Home className='mr-2 h-4 w-4' />
								Home
							</a>
						</Button>
					</div>
				</CardContent>
			</Card>
		</div>
	);
};

export default ErrorPage;
