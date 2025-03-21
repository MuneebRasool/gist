import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import React from 'react';
import { redirect } from 'next/navigation';

export default async function OnboardingLayout({ children }: { children: React.ReactNode }) {
	const session = await getServerSession(authOptions);
	if (session?.user.onboarding) {
		redirect('/app/dashboard');
	}
	if (!session) {
		redirect('/login');
	}
	return <main className='flex h-screen flex-col'>{children}</main>;
}
