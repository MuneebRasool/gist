'use client';

import { useTasksStore } from '@/store/tasks';
import { useEffect, useState } from 'react';
import { useSession } from 'next-auth/react';
import Loading from '@/app/loading';
import TaskCard from '@/components/app/tasks/TaskCard';
import { Mic } from 'lucide-react';
import { TaskResponse } from '@/types/tasks';

// Sample tasks for demonstration
const sampleTasks: TaskResponse[] = [
	{
		task_id: '1',
		task: 'Investigate the billing bug and apply a fix',
		deadline: 'Before noon',
		priority: 'high',
		userId: 'demo-user',
		createdAt: new Date().toISOString(),
		updatedAt: new Date().toISOString(),
	},
	{
		task_id: '2',
		task: 'Video Call with Ana',
		deadline: '2 PM',
		priority: 'medium',
		userId: 'demo-user',
		createdAt: new Date().toISOString(),
		updatedAt: new Date().toISOString(),
	},
	{
		task_id: '3',
		task: 'Pick up dry cleaning',
		deadline: '3 PM',
		priority: 'low',
		userId: 'demo-user',
		createdAt: new Date().toISOString(),
		updatedAt: new Date().toISOString(),
	},
	{
		task_id: '4',
		task: 'Phone Call with Eli',
		deadline: '3 PM',
		priority: 'medium',
		userId: 'demo-user',
		createdAt: new Date().toISOString(),
		updatedAt: new Date().toISOString(),
	},
	{
		task_id: '5',
		task: 'Ensure the billing fix is ready before the system update',
		deadline: 'EOD',
		priority: 'high',
		userId: 'demo-user',
		createdAt: new Date().toISOString(),
		updatedAt: new Date().toISOString(),
	},
];

export default function DashboardPage() {
	const { tasks: storeTasks, fetchTasks, isLoading, setTasks } = useTasksStore();
	const { data: session } = useSession();
	const [useDemoData, setUseDemoData] = useState(false);

	useEffect(() => {
		if (session?.user?.id) {
			fetchTasks(session.user.id);
		}
	}, [session?.user?.id, fetchTasks]);

	// Use demo data if no tasks are found after loading
	useEffect(() => {
		if (!isLoading && storeTasks.length === 0) {
			setUseDemoData(true);
		}
	}, [isLoading, storeTasks.length]);

	if (isLoading) {
		return <Loading />;
	}

	const displayTasks = useDemoData ? sampleTasks : storeTasks;

	return (
		<div className="space-y-8">
			<div className="flex items-center justify-between">
				<h1 className="text-4xl font-bold tracking-tight text-gray-900">Your Focus Today</h1>
				<div className="flex items-center gap-2 rounded-full bg-white/50 px-4 py-2 text-sm text-gray-600 backdrop-blur-sm">
					<Mic className="h-4 w-4" />
					<span>Press ⌘ + A to chat with Gist</span>
				</div>
			</div>

			<div className="space-y-4">
				{displayTasks.map((task) => (
					<TaskCard key={task.task_id} task={task} />
				))}
				{displayTasks.length === 0 && (
					<div className="flex flex-col items-center gap-6 rounded-2xl bg-white/50 py-12 backdrop-blur-sm">
						<div className="rounded-full bg-primary/10 p-3">
							<Mic className="h-6 w-6 text-primary" />
						</div>
						<div className="text-center">
							<h3 className="text-lg font-semibold">No Tasks Found</h3>
							<p className="text-sm text-muted-foreground">
								No tasks found. New tasks will appear here once they are extracted from your emails.
							</p>
						</div>
					</div>
				)}
			</div>
		</div>
	);
}
