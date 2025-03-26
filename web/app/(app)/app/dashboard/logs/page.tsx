'use client';
import { useTasksStore } from '@/store/tasks';
import React from 'react';
import TaskGroup from '@/components/app/logs/TaskGroup';
import { groupTasksByDate, getSortedDates } from '@/components/app/logs/utils';
import { useSession } from 'next-auth/react';

const Page = () => {
	const { tasks, fetchTasks, isLoading } = useTasksStore();
	const { data: session } = useSession();

	React.useEffect(() => {
		if (session?.user?.id) {
			fetchTasks(session.user.id, true);
		}
	}, [fetchTasks, session?.user?.id]);

	const groupedTasks = React.useMemo(() => {
		return groupTasksByDate(tasks);
	}, [tasks]);

	const sortedDates = React.useMemo(() => {
		return getSortedDates(groupedTasks);
	}, [groupedTasks]);

	if (isLoading) {
		return <div className='py-8 text-center'>Loading...</div>;
	}

	return (
		<div className='mx-auto flex h-[calc(100dvh-68px)] w-full flex-col space-y-6 overflow-hidden p-3 sm:p-5'>
			<h1 className='mb-4 text-5xl font-light text-muted-foreground'>Updates</h1>
			{sortedDates.map((date) => (
				<TaskGroup key={date} title={date} tasks={groupedTasks[date] || []} />
			))}
			{sortedDates.length === 0 && (
				<div className='flex flex-col items-center gap-5 overflow-y-auto rounded-3xl bg-background/70 p-8 backdrop-blur-md'>
					<h2 className='text-3xl font-light text-muted-foreground'>No updates found</h2>
				</div>
			)}
		</div>
	);
};

export default Page;
