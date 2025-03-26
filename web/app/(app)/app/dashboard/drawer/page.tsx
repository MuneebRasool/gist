'use client';
import { useEffect } from 'react';
import { useSession } from 'next-auth/react';
import Loading from '@/app/loading';
import SortableTaskList from '@/components/app/tasks/SortableTaskList';
import { useDrawerTasksStore } from '@/store/drawerTasks';
import TaskEmail from '@/components/app/tasks/TaskEmails/TaskEmail';
import { Mic } from 'lucide-react';

export default function DrawerPage() {
	const { tasks, isLoading } = useDrawerTasksStore();

	if (isLoading) {
		return <Loading text='Fetching your tasks...' />;
	}

	return (
		<div className='flex max-h-[calc(100dvh-68px)] flex-col space-y-4 overflow-hidden pb-3'>
			<h1 className='text-3xl font-semibold tracking-tight'>Task Drawer</h1>

			<div className='flex flex-1 flex-col gap-4 rounded-3xl bg-background/80 p-4 backdrop-blur-md'>
				{tasks.map((task) => (
					<TaskEmail key={task.messageId} email={task} />
				))}
				{tasks.length === 0 && (
					<div className='flex flex-1 flex-col items-center gap-6 rounded-3xl py-12'>
						<div className='rounded-full bg-primary/20 p-3'>
							<Mic className='h-6 w-6 text-primary' />
						</div>
						<div className='text-center'>
							<h3 className='text-lg font-medium text-gray-800'>No tasks found</h3>
							<p className='text-sm text-gray-600'>Add a task to your library to get started</p>
						</div>
					</div>
				)}
			</div>
		</div>
	);
}
