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
			setUserEmail(session.user.email);
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
