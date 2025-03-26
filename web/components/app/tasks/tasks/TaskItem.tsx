import { Button } from '@/components/ui/button';
import { TaskResponse } from '@/types/tasks';
import { Check, Mail, Menu } from 'lucide-react';
import React, { useState } from 'react';
import EmailSheet from '../EmailSheet';

interface TaskItemProps {
	task: TaskResponse;
	isCompleted?: boolean;
	onToggleComplete?: () => void;
	isDraggable?: boolean;
	hideCheckBox?: boolean;
}

const TaskItem = ({ task, isCompleted, onToggleComplete, hideCheckBox, isDraggable }: TaskItemProps) => {
	const [isOpen, setIsOpen] = useState(false);
	return (
		<>
			<div className='flex items-center gap-4'>
				{!hideCheckBox && (
					<button
						onClick={(e) => {
							e.stopPropagation();
							onToggleComplete?.();
						}}
						className='flex size-9 shrink-0 items-center justify-center rounded-md border'
					>
						{isCompleted && <Check className='size-6 text-muted-foreground' />}
					</button>
				)}
				<div className='min-w-0 flex-1'>
					<h3
						className={`text-xl font-medium text-foreground/80 ${isCompleted ? 'text-muted-foreground line-through' : ''}`}
					>
						{task.task}
					</h3>
					{task.task && (
						<p
							className={`mt-1 text-lg text-foreground/60 ${isCompleted ? 'text-muted-foreground/80 line-through' : ''}`}
						>
							{task.task}
						</p>
					)}
				</div>
				<div className='flex shrink-0 items-center gap-3'>
					{task.messageId && (
						<Button variant='ghost' size='icon' onClick={() => setIsOpen(true)}>
							<Mail className='h-4 w-4' />
						</Button>
					)}
					<span className='text-sm text-gray-500'>
						{new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
					</span>
					{isDraggable && <Menu size={20} className='font-light text-muted-foreground' />}
				</div>
			</div>
			<EmailSheet isOpen={isOpen} setIsOpen={setIsOpen} messageId={task.messageId} />
		</>
	);
};

export default TaskItem;
