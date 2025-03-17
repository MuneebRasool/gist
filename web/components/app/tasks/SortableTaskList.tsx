import React, { useState } from 'react';
import { TaskResponse } from '@/types/tasks';
import TaskCard from './TaskCard';
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

interface SortableTaskItemProps {
  task: TaskResponse;
  isDragging?: boolean;
}

// Wrapper component for making TaskCard sortable
const SortableTaskItem = ({ task, isDragging }: SortableTaskItemProps) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({ id: task.task_id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
    cursor: 'grab',
    position: 'relative' as const,
    zIndex: isDragging ? 1 : 'auto',
  };

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      <TaskCard task={task} />
    </div>
  );
};

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
  const { reorderTask } = useTasksStore();

  // Update sorted tasks when the input tasks change
  React.useEffect(() => {
    // Sort tasks by relevance_score (highest first) if available
    const sortedByRelevance = [...tasks].sort((a, b) => {
      // If both have relevance scores, sort by them (highest first)
      if (a.relevance_score !== undefined && b.relevance_score !== undefined) {
        return b.relevance_score - a.relevance_score;
      }
      // If only one has a relevance score, prioritize the one with a score
      if (a.relevance_score !== undefined) return -1;
      if (b.relevance_score !== undefined) return 1;
      // If neither has a relevance score, maintain original order
      return 0;
    });
    
    setSortedTasks(sortedByRelevance);
  }, [tasks]);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8, // 8px of movement required before activating
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
      // Find the original indices
      const oldIndex = sortedTasks.findIndex((item) => item.task_id === active.id);
      const newIndex = sortedTasks.findIndex((item) => item.task_id === over.id);
      
      // Get the task and its classification
      const task = sortedTasks.find(task => task.task_id === active.id);
      const classification = task?.classification || '';
      
      // Update the local state with the new order
      const reorderedTasks = arrayMove(sortedTasks, oldIndex, newIndex);
      setSortedTasks(reorderedTasks);
      
      // Call the callback with the new order if provided
      if (onTasksReordered) {
        onTasksReordered(reorderedTasks);
      }
      
      // Send feedback to the backend about the reordering
      if (task) {
        // Pass the reordered tasks to find tasks above and below
        await reorderTask(task.task_id, oldIndex, newIndex, classification, reorderedTasks);
      }
    }
    
    setActiveId(null);
  };

  // Find the active task
  const activeTask = activeId ? sortedTasks.find(task => task.task_id === activeId) : null;

  if (sortedTasks.length === 0) {
    return (
      <div className='flex flex-col items-center gap-6 rounded-2xl bg-white/40 py-12 backdrop-blur-sm'>
        <div className='rounded-full bg-primary/20 p-3'>
          <Mic className='h-6 w-6 text-primary' />
        </div>
        <div className='text-center'>
          <h3 className='text-lg font-semibold text-gray-800'>{emptyMessage.title}</h3>
          <p className='text-sm text-gray-600'>{emptyMessage.description}</p>
        </div>
      </div>
    );
  }

  return (
    <DndContext 
      sensors={sensors} 
      collisionDetection={closestCenter} 
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
      <SortableContext items={sortedTasks.map(task => task.task_id)} strategy={verticalListSortingStrategy}>
        <div className='space-y-4'>
          {sortedTasks.map((task) => (
            <SortableTaskItem 
              key={task.task_id} 
              task={task} 
              isDragging={activeId === task.task_id}
            />
          ))}
        </div>
      </SortableContext>
      
      {/* Drag overlay to show what's being dragged */}
      <DragOverlay adjustScale={true}>
        {activeTask ? (
          <div className="opacity-90 transform scale-105 shadow-lg">
            <TaskCard task={activeTask} />
          </div>
        ) : null}
      </DragOverlay>
    </DndContext>
  );
};

export default SortableTaskList; 