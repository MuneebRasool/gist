import { TaskResponse } from '@/types/tasks';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import EmailSheet from './EmailSheet';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Mail } from 'lucide-react';
import TaskItem from './tasks/TaskItem';

interface SortableTaskItemProps {
	task: TaskResponse;
	isDragging?: boolean;
	isCompleted?: boolean;
	onToggleComplete?: () => void;
}

export const SortableTaskItem = ({ task, isDragging, isCompleted, onToggleComplete }: SortableTaskItemProps) => {
	const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id: task.task_id });

	const style = {
		transform: CSS.Transform.toString(transform),
		transition,
		opacity: isDragging ? 0.5 : 1,
		cursor: 'grab',
		position: 'relative' as const,
		zIndex: isDragging ? 1 : 'auto',
	};

	return (
		<div ref={setNodeRef} style={style} {...attributes} {...listeners} className='px-9 py-6'>
			<TaskItem task={task} isCompleted={isCompleted} onToggleComplete={onToggleComplete} isDraggable />
		</div>
	);
};
