'use client';

import { useTasksStore } from '@/store/tasks';
import { useEffect, useMemo } from 'react';
import { useSession } from 'next-auth/react';
import Loading from '@/app/loading';
import SortableTaskList from '@/components/app/tasks/SortableTaskList';
import { TaskResponse } from '@/types/tasks';

export default function DashboardPage() {
	const { tasks, fetchTasks, isLoading, updateTaskOrder } = useTasksStore();
	const { data: session } = useSession();

	// Filter tasks with classification = "main focus view"
	const filteredTasks = useMemo(() => {
		return tasks.filter(task => task.classification === 'Main Focus-View');
	}, [tasks]);

	useEffect(() => {
		if (session?.user?.id) {
			fetchTasks(session.user.id);
		}
	}, [session?.user?.id, fetchTasks]);

	// Handle task reordering
	const handleTasksReordered = (reorderedTasks: TaskResponse[]) => {
		// Extract the task IDs in the new order
		const taskIds = reorderedTasks.map(task => task.task_id);
		
		// Update the task order in the store
		updateTaskOrder(taskIds);
		
		// The API call for feedback is now handled in the SortableTaskList component
	};

	if (isLoading) {
		return <Loading text='Fetching your tasks...' />;
	}

	return (
		<div className='space-y-8'>
			<h1 className='text-4xl font-bold tracking-tight text-gray-900'>Your Focus Today</h1>

			<SortableTaskList 
				tasks={filteredTasks} 
				emptyMessage={{
					title: "No Focus Tasks Found",
					description: "No main focus tasks found. Tasks classified as main focus will appear here."
				}}
				onTasksReordered={handleTasksReordered}
			/>
		</div>
	);
}