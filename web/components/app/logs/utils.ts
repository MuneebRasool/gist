import { TaskResponse } from '@/types/tasks';
import { format, isToday, isYesterday } from 'date-fns';

export interface GroupedTasks {
	[key: string]: TaskResponse[];
}

export const groupTasksByDate = (tasks: TaskResponse[]): GroupedTasks => {
	return tasks.reduce((acc: GroupedTasks, task) => {
		const date = new Date(task.createdAt);
		const dateKey = format(date, 'yyyy-MM-dd');

		const displayKey = isToday(date) ? 'Today' : isYesterday(date) ? 'Yesterday' : format(date, 'MMMM d, yyyy');

		if (!acc[displayKey]) {
			acc[displayKey] = [];
		}
		acc[displayKey].push(task);
		return acc;
	}, {});
};

export const getSortedDates = (groupedTasks: GroupedTasks): string[] => {
	const dates = Object.keys(groupedTasks);
	return ['Today', ...dates.filter((date) => date !== 'Today')];
};
