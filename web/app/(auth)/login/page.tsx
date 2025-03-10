'use client';

import * as React from 'react';
import SignInForm from '@/components/auth/SignInForm';

export default function LoginPage() {
	return (
		<main className='flex min-h-screen items-center justify-center bg-gradient-to-br from-rose-50 to-slate-100 p-4'>
			<SignInForm />
		</main>
	);
}
