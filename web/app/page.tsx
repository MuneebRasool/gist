'use client';
import { useSession } from 'next-auth/react';
import Loading from './loading';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function HomePage() {
	const { data: session, status } = useSession();
	const router = useRouter();

	useEffect(() => {
		if (status === 'loading') {
			return;
		}
		if (session?.user) {
			return router.push('/app');
		} else {
			return router.push('/login');
		}
	}, [router, session?.user, status]);

	return <Loading text='Preparing your experience...' />;
}
