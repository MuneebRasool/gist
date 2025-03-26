import React, { useState } from 'react';
import { TaskResponse } from '@/types/tasks';
import { Mic } from 'lucide-react';
import {
	DndContext,
	closestCenter,
	KeyboardSensor,
	PointerSensor,
	useSensor,
	useSensors,
	DragEndEvent,
	DragStartEvent,
	DragOverlay,
} from '@dnd-kit/core';
import {
	arrayMove,
	SortableContext,
	sortableKeyboardCoordinates,
	verticalListSortingStrategy,
	useSortable,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { useTasksStore } from '@/store/tasks';
import { SortableTaskItem } from './SortableTaskItem';

interface SortableTaskListProps {
	tasks: TaskResponse[];
	emptyMessage: {
		title: string;
		description: string;
	};
	onTasksReordered?: (tasks: TaskResponse[]) => void;
}

const SortableTaskList = ({ tasks, emptyMessage, onTasksReordered }: SortableTaskListProps) => {
	const [sortedTasks, setSortedTasks] = useState<TaskResponse[]>(tasks);
	const [activeId, setActiveId] = useState<string | null>(null);
	const [completedTasks, setCompletedTasks] = useState<Set<string>>(new Set());
	const { reorderTask } = useTasksStore();

	React.useEffect(() => {
		const sortedByRelevance = [...tasks].sort((a, b) => {
			if (a.relevance_score !== undefined && b.relevance_score !== undefined) {
				return b.relevance_score - a.relevance_score;
			}
			if (a.relevance_score !== undefined) return -1;
			if (b.relevance_score !== undefined) return 1;
			return 0;
		});

		setSortedTasks(sortedByRelevance);
	}, [tasks]);

	const sensors = useSensors(
		useSensor(PointerSensor, {
			activationConstraint: {
				distance: 8,
			},
		}),
		useSensor(KeyboardSensor, {
			coordinateGetter: sortableKeyboardCoordinates,
		})
	);

	const handleDragStart = (event: DragStartEvent) => {
		setActiveId(event.active.id as string);
	};

	const handleDragEnd = async (event: DragEndEvent) => {
		const { active, over } = event;

		if (over && active.id !== over.id) {
			const oldIndex = sortedTasks.findIndex((item) => item.task_id === active.id);
			const newIndex = sortedTasks.findIndex((item) => item.task_id === over.id);

			const task = sortedTasks.find((task) => task.task_id === active.id);
			const classification = task?.classification || '';

			const reorderedTasks = arrayMove(sortedTasks, oldIndex, newIndex);
			setSortedTasks(reorderedTasks);

			if (onTasksReordered) {
				onTasksReordered(reorderedTasks);
			}

			if (task) {
				await reorderTask(task.task_id, oldIndex, newIndex, classification, reorderedTasks);
			}
		}

		setActiveId(null);
	};

	const activeTask = activeId ? sortedTasks.find((task) => task.task_id === activeId) : null;

	const handleToggleComplete = (taskId: string) => {
		setCompletedTasks((prev) => {
			const newSet = new Set(prev);
			if (newSet.has(taskId)) {
				newSet.delete(taskId);
			} else {
				newSet.add(taskId);
			}
			return newSet;
		});
	};

	if (sortedTasks.length === 0) {
		return (
			<div className='flex flex-1 flex-col items-center gap-6 overflow-y-auto rounded-3xl bg-background/70 py-12 backdrop-blur-md'>
				<div className='rounded-full bg-primary/20 p-3'>
					<Mic className='h-6 w-6 text-primary' />
				</div>
				<div className='text-center'>
					<h3 className='text-lg font-medium text-gray-800'>{emptyMessage.title}</h3>
					<p className='text-sm text-gray-600'>{emptyMessage.description}</p>
				</div>
			</div>
		);
	}

	return (
		<div className='flex-1 overflow-y-auto rounded-3xl bg-background/70 backdrop-blur-md'>
			<DndContext
				sensors={sensors}
				collisionDetection={closestCenter}
				onDragStart={handleDragStart}
				onDragEnd={handleDragEnd}
			>
				<SortableContext items={sortedTasks.map((task) => task.task_id)} strategy={verticalListSortingStrategy}>
					<div className='overflow-hidden'>
						{sortedTasks.map((task, index) => (
							<React.Fragment key={task.task_id}>
								<SortableTaskItem
									task={task}
									isDragging={activeId === task.task_id}
									isCompleted={completedTasks.has(task.task_id)}
									onToggleComplete={() => handleToggleComplete(task.task_id)}
								/>
								{index < sortedTasks.length - 1 && <div className='mx-6 h-px bg-border' />}
							</React.Fragment>
						))}
					</div>
				</SortableContext>

				<DragOverlay adjustScale={true}>
					{activeTask ? (
						<div className='w-full rounded-3xl bg-background/40 shadow-lg backdrop-blur-md'>
							<SortableTaskItem task={activeTask} />
						</div>
					) : null}
				</DragOverlay>
			</DndContext>
		</div>
	);
};

export default SortableTaskList;
