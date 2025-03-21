'use client';

import Sidebar from '@/components/app/Sidebar';
import { useState, useEffect } from 'react';
import { Mic } from 'lucide-react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useOnboardingStore } from '@/store/onboarding.store';
import { GistContext } from '@/components/app/GistContext';

export default function DashBoardLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	const router = useRouter();
	const { data: session } = useSession();
	const { setUserEmail } = useOnboardingStore();

	// Check onboarding status from session and redirect if needed
	useEffect(() => {
		if (session?.user && session.user.onboarding === false) {
			// Set email in store for onboarding
			setUserEmail(session.user.email);
			// Redirect to onboarding with email
			const encodedEmail = encodeURIComponent(session.user.email);
			router.push(`/app/onboarding?email=${encodedEmail}`);
		}
	}, [session, router, setUserEmail]);

	return (
		<>
			<GistContext />
			<Sidebar>{children}</Sidebar>
		</>
	);
}
