'use client';

import React from 'react';
import { Loader2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

const Loading = () => {
	return (
		<div className='fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm'>
			<Card className='w-full max-w-sm'>
				<CardContent className='flex flex-col items-center justify-center space-y-4 p-6'>
					<Loader2 className='h-12 w-12 animate-spin text-primary' strokeWidth={1.5} />
					<div className='space-y-2 text-center'>
						<h2 className='text-xl font-semibold text-foreground'>Loading</h2>
						<p className='text-sm text-muted-foreground'>Preparing your content</p>
					</div>
					<div className='h-1 w-full overflow-hidden bg-primary/10'>
						<div className='animate-progress-bar h-full bg-primary'></div>
					</div>
				</CardContent>
			</Card>
		</div>
	);
};

export default Loading;
