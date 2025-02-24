'use client';

import { useNylasStatusStore } from '@/store';
import GmailConnect from '@/components/app/settings/GmailConnect';
import { TaskExtractorOnboarding } from '@/components/app/tasks/TaskExtractorOnboarding';
import { useTasksStore } from '@/store/tasks';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { CalendarDays } from 'lucide-react';
import { useEffect } from 'react';
import { useSession } from 'next-auth/react';
import Loading from '@/app/loading';
import TaskCard from '@/components/app/tasks/TaskCard';

export default function HomePage() {
	const { isConnected, isLoading } = useNylasStatusStore();
	const { tasks, fetchTasks } = useTasksStore();
	const { data: session } = useSession();

	useEffect(() => {
		if (session?.user?.id) {
			fetchTasks(session.user.id);
		}
	}, [session?.user?.id, fetchTasks]);

	if (isLoading) {
		return <Loading />;
	}

	if (!isConnected) {
		return (
			<div className='container mx-auto py-8'>
				<div className='mx-auto max-w-2xl'>
					<GmailConnect />
				</div>
			</div>
		);
	}

	if (tasks.length === 0) {
		return (
			<div className='container mx-auto py-8'>
				<TaskExtractorOnboarding userId={session?.user?.id ?? ''} />
			</div>
		);
	}

	return (
		<div className='container mx-auto py-8'>
			<h1 className='mb-6 text-2xl font-bold'>Your Tasks</h1>
			<div className='grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3'>
				{tasks.map((task) => (
					<TaskCard key={task.task_id} task={task} />
				))}
			</div>
		</div>
	);
}
