'use client';
import Loading from '@/app/loading';
import { useLibraryTasksStore } from '@/store/libraryTasks';
import TaskEmail from '@/components/app/tasks/TaskEmails/TaskEmail';
import { Mic } from 'lucide-react';

export default function LibraryPage() {
	const { tasks, isLoading } = useLibraryTasksStore();

	if (isLoading) {
		return <Loading text='Fetching your tasks...' />;
	}

	return (
		<div className='flex max-h-[calc(100dvh-68px)] flex-col space-y-4 overflow-hidden pb-3'>
			<h1 className='text-3xl font-semibold tracking-tight'>Task Library</h1>

			<div className='flex flex-1 flex-col gap-4 rounded-3xl bg-background/80 p-4 backdrop-blur-md'>
				{tasks.map((task) => (
					<TaskEmail key={task.messageId} email={task} />
				))}
				{tasks.length === 0 && (
					<div className='flex flex-1 flex-col items-center gap-6 overflow-y-auto rounded-3xl bg-background/30 py-12 backdrop-blur-md'>
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
