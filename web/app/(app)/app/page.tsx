'use client';

import { useNylasStatusStore } from '@/store';
import { useTasksStore } from '@/store/tasks';
import { CalendarDays } from 'lucide-react';
import { useEffect } from 'react';
import { useSession } from 'next-auth/react';
import Loading from '@/app/loading';
import TaskCard from '@/components/app/tasks/TaskCard';
import WelcomeMessage from '@/components/app/onboarding/WelcomeMessage';

export default function HomePage() {
	const { isConnected, isLoading: emailStatusLoading } = useNylasStatusStore();
	const { tasks, fetchTasks, isLoading } = useTasksStore();
	const { data: session } = useSession();

	useEffect(() => {
		if (session?.user?.id) {
			fetchTasks(session.user.id);
		}
	}, [session?.user?.id, fetchTasks]);

	if (isLoading || emailStatusLoading) {
		return <Loading />;
	}

	if (!isConnected) {
		return (
			<div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-rose-50 to-slate-100">
				<WelcomeMessage />
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
			{tasks.length === 0 && (
				<div className='flex flex-col items-center gap-6 py-8'>
					<CalendarDays className='h-16 w-16 text-primary' />
					<div className='text-center'>
						<h3 className='text-lg font-semibold'>No Tasks Found</h3>
						<p className='text-sm text-muted-foreground'>
							No tasks found. New tasks will appear here once they are extracted from your emails.
						</p>
					</div>
				</div>
			)}
		</div>
	);
}
