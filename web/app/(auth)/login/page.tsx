'use client';

import * as React from 'react';
import SignInForm from '@/components/auth/SignInForm';

export default function LoginPage() {
	return (
		<main className='flex h-screen flex-col items-center justify-center gap-5 p-3'>
			<h1 className='mb-9 text-center text-3xl font-semibold text-muted-foreground'>
				Delegate your workflow with Gist
			</h1>
			<SignInForm />
		</main>
	);
}
