'use client';

import { useTasksStore } from '@/store/tasks';
import { useEffect } from 'react';
import { useSession } from 'next-auth/react';
import Loading from '@/app/loading';
import TaskCard from '@/components/app/tasks/TaskCard';
import { Mic } from 'lucide-react';

export default function DashboardPage() {
	const { tasks, fetchTasks, isLoading } = useTasksStore();
	const { data: session } = useSession();

	console.log(tasks);

	useEffect(() => {
		if (session?.user?.id) {
			fetchTasks(session.user.id);
			console.log('Tasks fetched:', tasks);
		}
	}, [session?.user?.id, fetchTasks]);

	if (isLoading) {
		return <Loading text="Fetching your tasks..." />;
	}

	return (
		<div className="space-y-8">
			<h1 className="text-4xl font-bold tracking-tight text-gray-900">Your Focus Today</h1>

			{/* <div className="rounded-xl bg-white/20 p-6 shadow-lg backdrop-blur-sm"> */}
				<div className="space-y-4">
					{tasks.map((task) => (
						<TaskCard key={task.task_id} task={task} />
					))}
					{tasks.length === 0 && (
						<div className="flex flex-col items-center gap-6 rounded-2xl bg-white/40 py-12 backdrop-blur-sm">
							<div className="rounded-full bg-primary/20 p-3">
								<Mic className="h-6 w-6 text-primary" />
							</div>
							<div className="text-center">
								<h3 className="text-lg font-semibold text-gray-800">No Tasks Found</h3>
								<p className="text-sm text-gray-600">
									No tasks found. New tasks will appear here once they are extracted from your emails.
								</p>
							</div>
						</div>
					)}
				</div>
			</div>
		// </div>
	);
}
