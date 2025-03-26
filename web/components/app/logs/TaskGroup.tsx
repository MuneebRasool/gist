import { TaskResponse } from '@/types/tasks';
import React from 'react';
import TaskItem from '../tasks/tasks/TaskItem';

interface TaskGroupProps {
	title: string;
	tasks: TaskResponse[];
}

const TaskGroup = ({ title, tasks }: TaskGroupProps) => {
	if (tasks.length === 0) {
		return (
			<div className='flex flex-col gap-5 overflow-y-auto rounded-3xl bg-background/70 p-8 backdrop-blur-md'>
				<h2 className='pb-4 text-4xl font-light text-muted-foreground'>{title}</h2>
				<h3 className='text-center text-2xl font-light text-muted-foreground'>Nothing new yet!</h3>
			</div>
		);
	}
	return (
		<div className='flex flex-col gap-5 overflow-y-auto rounded-3xl bg-background/70 p-8 backdrop-blur-md'>
			<h2 className='border-b pb-4 text-4xl font-light text-muted-foreground'>{title}</h2>
			<div className='space-y-4'>
				{tasks.map((task, index) => (
					<React.Fragment key={task.task_id}>
						<TaskItem hideCheckBox task={task} />
						{index < tasks.length - 1 && <div className='h-px bg-border' />}
					</React.Fragment>
				))}
			</div>
		</div>
	);
};

export default TaskGroup;
