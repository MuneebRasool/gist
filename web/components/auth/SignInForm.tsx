'use client';
import { useState } from 'react';
import GoogleSignin from './GoogleSignin';

export default function SignInForm() {
	const [email, setEmail] = useState('');

	return (
		<div className='w-full max-w-[600px] space-y-6 rounded-3xl bg-background/70 px-14 py-10 backdrop-blur-sm'>
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
