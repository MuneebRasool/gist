'use client';
import React, { useState } from 'react';
import { Button } from '../ui/button';
import GoogleIcon from '@/assets/GoogleIcon';
import { signIn } from 'next-auth/react';
import { Loader2 } from 'lucide-react';

const GoogleSignin = () => {
	const [isLoading, setIsLoading] = useState(false);
	return (
		<Button
			variant='outline'
			className='h-14 w-full items-center rounded-lg border-gray-200 bg-background text-lg font-medium hover:bg-gray-50'
			onClick={async () => {
				setIsLoading(true);
				await signIn('google', {
					callbackUrl: '/app',
				});
				setIsLoading(false);
			}}
			disabled={isLoading}
		>
			{isLoading ? <Loader2 className='mr-2 h-6 w-6 animate-spin' /> : <GoogleIcon className='mr-2 h-8 w-8' />}
			Sign up with Google
		</Button>
	);
};

export default GoogleSignin;
