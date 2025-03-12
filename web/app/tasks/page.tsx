'use client';
import React, { useState, useCallback, useEffect } from 'react';
import { TasksService } from '@/services/tasks.service';
import { TaskResponse } from '@/types/tasks';
import { toast } from 'sonner';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { ChevronUp, ChevronDown } from 'lucide-react';
import { useSession } from 'next-auth/react';

export default function TaskListPage() {
  const { data: session } = useSession();
  const [tasks, setTasks] = useState<TaskResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        if (session?.user?.id) {
          const response = await TasksService.getUserTasks(session.user.id);
          if (response.data) {
            setTasks(response.data);
          }
        }
      } catch (error) {
        toast.error('Failed to fetch tasks');
        console.error('Error fetching tasks:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [session?.user?.id]);

  const moveTask = useCallback(async (index: number, direction: 'up' | 'down') => {
    const task = tasks[index];
    try {
      // Call the reorder API
      await TasksService.reorderTask(task.task_id, direction);

      // Update the local state
      const newTasks = [...tasks];
      if (direction === 'up' && index > 0) {
        [newTasks[index], newTasks[index - 1]] = [newTasks[index - 1], newTasks[index]];
      } else if (direction === 'down' && index < tasks.length - 1) {
        [newTasks[index], newTasks[index + 1]] = [newTasks[index + 1], newTasks[index]];
      }

      setTasks(newTasks);
      toast.success('Task reordered successfully');

      // Refresh tasks to get updated scores
      if (session?.user?.id) {
        const response = await TasksService.getUserTasks(session.user.id);
        if (response.data) {
          setTasks(response.data);
        }
      }
    } catch (error) {
      toast.error('Failed to reorder task');
      console.error('Error reordering task:', error);
    }
  }, [tasks, session?.user?.id]);

  const toggleTask = async (taskId: string) => {
    try {
      // In a real implementation, you would update the task completion status on the server
      toast.success('Task status updated');
    } catch (error) {
      toast.error('Failed to update task status');
      console.error('Error updating task:', error);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto py-8">
        <Card>
          <CardContent className="p-8">
            <div className="text-center">Loading tasks...</div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8">
      <Card>
        <CardHeader>
          <CardTitle>Task List</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {tasks.map((task, index) => (
              <div 
                key={task.task_id}
                className="flex items-center justify-between p-4 bg-card rounded-lg border"
              >
                <div className="flex items-center space-x-4">
                  <Checkbox
                    onCheckedChange={() => toggleTask(task.task_id)}
                  />
                  <span>
                    {task.task}
                  </span>
                  <div className="ml-4 text-sm text-muted-foreground">
                    {task.relevance_score !== undefined && (
                      <span className="mr-4">Relevance: {task.relevance_score.toFixed(1)}</span>
                    )}
                    {task.utility_score !== undefined && (
                      <span className="mr-4">Utility: {task.utility_score.toFixed(1)}</span>
                    )}
                    {task.cost_score !== undefined && (
                      <span>Cost: {task.cost_score.toFixed(1)}</span>
                    )}
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={() => moveTask(index, 'up')}
                    disabled={index === 0}
                  >
                    <ChevronUp className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={() => moveTask(index, 'down')}
                    disabled={index === tasks.length - 1}
                  >
                    <ChevronDown className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
