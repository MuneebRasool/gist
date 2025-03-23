'use client';

import { useTasksStore } from '@/store/tasks';
import { useEffect, useMemo } from 'react';
import { useSession } from 'next-auth/react';
import Loading from '@/app/loading';
import SortableTaskList from '@/components/app/tasks/SortableTaskList';
import FloatingButtons from '@/components/app/FloatingButtons';
import { TaskResponse } from '@/types/tasks';

export default function DashboardPage() {
	const { tasks, fetchTasks, isLoading, updateTaskOrder } = useTasksStore();
	const { data: session, status } = useSession();

	useEffect(() => {
		if (session?.user?.id) {
			fetchTasks(session.user.id);
		}
	}, [session?.user?.id, fetchTasks]);

	const handleTasksReordered = (reorderedTasks: TaskResponse[]) => {
		const taskIds = reorderedTasks.map((task) => task.task_id);
		updateTaskOrder(taskIds);
	};

	const handleLibraryClick = () => {
		// TODO: Implement library functionality
		console.log('Library clicked');
	};

	const handleDrawerClick = () => {
		// TODO: Implement drawer functionality
		console.log('Drawer clicked');
	};

	if (status === 'loading') {
		return <Loading text='Loading...' />;
	}

	if (isLoading) {
		return <Loading text='Fetching your tasks...' />;
	}

	return (
		<div className='mx-auto flex h-[calc(100dvh-68px)] w-full flex-col space-y-3 overflow-hidden p-3'>
			<h1 className='text-3xl font-semibold'>Your Focus Today</h1>
			<div className='flex flex-1 flex-col justify-between gap-4 overflow-hidden'>
				<SortableTaskList
					tasks={tasks}
					emptyMessage={{
						title: 'No Focus Tasks Found',
						description: 'No main focus tasks found. Tasks classified as main focus will appear here.',
					}}
					onTasksReordered={handleTasksReordered}
				/>
				<FloatingButtons />
			</div>
		</div>
	);
}
