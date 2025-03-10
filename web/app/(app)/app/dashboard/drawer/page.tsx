'use client';

import { useTasksStore } from '@/store/tasks';
import { useEffect, useMemo } from 'react';
import { useSession } from 'next-auth/react';
import Loading from '@/app/loading';
import TaskCard from '@/components/app/tasks/TaskCard';
import { Mic } from 'lucide-react';

export default function DashboardPage() {
	const { tasks, fetchTasks, isLoading } = useTasksStore();
	const { data: session } = useSession();

	// Filter tasks with classification = "drawer"
	const filteredTasks = useMemo(() => {
		return tasks.filter(task => task.classification === 'Drawer');
	}, [tasks]);

	useEffect(() => {
		if (session?.user?.id) {
			fetchTasks(session.user.id);
		}
	}, [session?.user.id, fetchTasks]);

	if (isLoading) {
		return <Loading text='Fetching your tasks...' />;
	}

	return (
		<div className='space-y-8'>
			<h1 className='text-4xl font-bold tracking-tight text-gray-900'>Task Drawer</h1>

			{/* <div className="rounded-xl bg-white/20 p-6 shadow-lg backdrop-blur-sm"> */}
			<div className='space-y-4'>
				{filteredTasks.map((task) => (
					<TaskCard key={task.task_id} task={task} />
				))}
				{filteredTasks.length === 0 && (
					<div className='flex flex-col items-center gap-6 rounded-2xl bg-white/40 py-12 backdrop-blur-sm'>
						<div className='rounded-full bg-primary/20 p-3'>
							<Mic className='h-6 w-6 text-primary' />
						</div>
						<div className='text-center'>
							<h3 className='text-lg font-semibold text-gray-800'>Drawer Empty</h3>
							<p className='text-sm text-gray-600'>
								No drawer tasks found. Tasks classified as drawer will appear here.
							</p>
						</div>
					</div>
				)}
			</div>
		</div>
		// </div>
	);
}