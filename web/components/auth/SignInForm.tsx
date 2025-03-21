'use client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useState } from 'react';
import GoogleSignin from './GoogleSignin';

export default function SignInForm() {
	const [email, setEmail] = useState('');

	const handleEmailSignIn = (e: React.FormEvent) => {
		e.preventDefault();
		// Handle email sign in logic here
	};

	return (
		<div className='w-full max-w-[600px] space-y-6 rounded-3xl bg-white/70 px-14 py-10 backdrop-blur-sm'>
			<form onSubmit={handleEmailSignIn} className='space-y-4'>
				<Input
					type='email'
					placeholder='name@yourdomain.com'
					value={email}
					onChange={(e) => setEmail(e.target.value)}
					className='h-14 rounded-lg px-4 text-lg placeholder:text-center placeholder:text-lg placeholder:text-muted-foreground'
				/>

				<Button
					type='submit'
					className='h-14 w-full rounded-lg bg-foreground text-lg font-medium text-background hover:bg-foreground/90'
				>
					Continue with email
				</Button>
			</form>

			<div className='flex justify-center px-4 text-sm'>or</div>

			<GoogleSignin />

			<p className='mt-4 text-center text-xs text-gray-500'>
				By continuing, you agree to Gist&apos;s{' '}
				<a href='#' className='underline'>
					Consumer Terms
				</a>{' '}
				and{' '}
				<a href='#' className='underline'>
					Usage Policy
				</a>
				, and acknowledge their{' '}
				<a href='#' className='underline'>
					Privacy Policy
				</a>
				.
			</p>
		</div>
	);
}
