'use client';
import { useSession } from 'next-auth/react';
import Loading from './loading';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function HomePage() {
	const { data: session } = useSession();
	const router = useRouter();

	useEffect(() => {
		if (session?.user) {
			return router.push('/app');
		}
	}, [router, session?.user]);

	return <Loading />;
}
