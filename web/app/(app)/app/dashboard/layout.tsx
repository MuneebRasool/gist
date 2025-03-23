'use client';

import Sidebar from '@/components/app/Sidebar';
import { useEffect } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useOnboardingStore } from '@/store/onboarding.store';
import { GistContext } from '@/components/app/GistContext';
import { useNylasStatusStore } from '@/store';
import { useDrawerTasksStore } from '@/store/drawerTasks';
import { useLibraryTasksStore } from '@/store/libraryTasks';

export default function DashBoardLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	const router = useRouter();
	const { data: session } = useSession();
	const { setUserEmail } = useOnboardingStore();
	const { checkConnection } = useNylasStatusStore();
	const { fetchTasks } = useDrawerTasksStore();
	const { fetchTasks: fetchLibraryTasks } = useLibraryTasksStore();

	// Check onboarding status from session and redirect if needed
	useEffect(() => {
		checkConnection();
	}, [checkConnection, session?.user.id]);

	useEffect(() => {
		if (session?.user?.id) {
			fetchTasks(session.user.id);
			fetchLibraryTasks(session.user.id);
		}
	}, [session?.user?.id, fetchTasks, fetchLibraryTasks]);
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
