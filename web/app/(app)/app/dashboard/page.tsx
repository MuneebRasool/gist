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
	const { data: session } = useSession();

	const filteredTasks = useMemo(() => {
		return tasks.filter(task => task.classification === 'Main Focus-View');
	}, [tasks]);

	useEffect(() => {
		if (session?.user?.id) {
			fetchTasks(session.user.id);
		}
	}, [session?.user?.id, fetchTasks]);

	const handleTasksReordered = (reorderedTasks: TaskResponse[]) => {
		const taskIds = reorderedTasks.map(task => task.task_id);
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

	if (isLoading) {
		return <Loading text='Fetching your tasks...' />;
	}

	return (
		<div className='space-y-8 pt-10 relative h-full'>
			<div className='max-w-7xl mx-auto h-full'>
				<h1 className='text-4xl font-semibold text-gray-800'>Your Focus Today</h1>
				<div className="flex flex-col gap-56 mt-6 justify-between"> {/* Changed gap from 4 to 24 (100px) */}
					<SortableTaskList 
						tasks={filteredTasks} 
						emptyMessage={{
							title: "No Focus Tasks Found",
							description: "No main focus tasks found. Tasks classified as main focus will appear here."
						}}
						onTasksReordered={handleTasksReordered}
					/>

					<FloatingButtons
						onLibraryClick={handleLibraryClick}
						onDrawerClick={handleDrawerClick}
					/>
				</div>
			</div>
		</div>
	);
}