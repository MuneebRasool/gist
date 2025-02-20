'use client';
import { Button } from '@/components/ui/button';
import { signOut, useSession } from 'next-auth/react';
import Link from 'next/link';

export default function HomePage() {
	const { data: session } = useSession();

	if (session?.user) {
		return (
			<div className='flex h-screen flex-col items-center justify-center gap-4'>
				<div className='flex flex-col items-center gap-2'>
					<div>{session?.user?.id}</div>
					<div>{session?.user?.name}</div>
					<div>{session?.user?.email}</div>
				</div>
				<Button onClick={() => signOut()}>Logout</Button>
			</div>
		);
	}
	return (
		<div className='flex h-screen items-center justify-center gap-4'>
			<Link href='/login'>
				<Button>Login</Button>
			</Link>
			<Link href='/register'>
				<Button>Register</Button>
			</Link>
		</div>
	);
}
