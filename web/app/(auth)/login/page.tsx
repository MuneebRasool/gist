'use client';

import * as React from 'react';
import SignInForm from '@/components/auth/SignInForm';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function LoginPage() {
	const { data: session, status } = useSession();
	const router = useRouter();

	useEffect(() => {
		if (status === 'loading') {
			return;
		}
		if (session?.user) {
			return router.push('/app');
		}
	}, [router, session?.user, status]);

	return (
		<main className='flex h-screen flex-col items-center justify-center gap-5 p-3'>
			<h1 className='mb-9 text-center text-3xl font-semibold text-muted-foreground'>
				Delegate your workflow with Gist
			</h1>
			<SignInForm />
		</main>
	);
}
