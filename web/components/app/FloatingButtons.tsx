import React from 'react';
import { Button } from '@/components/ui/button';
import { Inbox, Library } from 'lucide-react';
import { useDrawerTasksStore } from '@/store/drawerTasks';
import { useLibraryTasksStore } from '@/store/libraryTasks';
import TaskEmail from './tasks/TaskEmails/TaskEmail';
import Link from 'next/link';

const FloatingButtons: React.FC = () => {
	const { tasks } = useDrawerTasksStore();
	const { tasks: libraryTasks } = useLibraryTasksStore();
	return (
		<div className='flex w-full gap-4 px-2'>
			<div className='flex-1'>
				<div className='group relative'>
					<div className='absolute bottom-full h-0 w-full overflow-hidden border-gray-400/60 transition-all duration-300 group-hover:h-[450px] group-hover:border-b'>
						<div className='h-[450px] w-full rounded-t-2xl bg-background/40 backdrop-blur-md'>
							<div className='flex items-center justify-end pt-1'>
								<Link href='/app/dashboard/library'>
									<Button variant='link' size='sm'>
										View all
									</Button>
								</Link>
							</div>
							<div className='flex flex-col overflow-y-auto'>
								{libraryTasks.slice(0, 3).map((task) => (
									<TaskEmail key={task.messageId} email={task} />
								))}
							</div>
						</div>
					</div>
					<Button
						className='relative flex h-14 w-full items-center justify-center gap-2 rounded-2xl bg-background/40 text-lg font-medium backdrop-blur-md transition-colors duration-200 hover:bg-background/50 group-hover:rounded-t-none'
						variant='ghost'
					>
						<Library className='h-5 w-5' />
						Library
					</Button>
				</div>
			</div>
			<div className='flex-1'>
				<div className='group relative'>
					<div className='absolute bottom-full h-0 w-full overflow-hidden border-gray-400/60 transition-all duration-300 group-hover:h-[450px] group-hover:border-b'>
						<div className='h-[450px] w-full rounded-t-2xl bg-background/40 backdrop-blur-md'>
							<div className='flex items-center justify-end pt-1'>
								<Link href='/app/dashboard/drawer'>
									<Button variant='link' size='sm'>
										View all
									</Button>
								</Link>
							</div>
							<div className='flex flex-col overflow-y-auto'>
								{tasks.slice(0, 3).map((task) => (
									<TaskEmail key={task.messageId} email={task} />
								))}
							</div>
						</div>
					</div>
					<Button
						className='relative flex h-14 w-full items-center justify-center gap-2 rounded-2xl bg-background/40 text-lg font-medium backdrop-blur-md transition-colors duration-200 hover:bg-background/50 group-hover:rounded-t-none'
						variant='ghost'
					>
						<Inbox className='h-5 w-5' />
						Drawer
					</Button>
				</div>
			</div>
		</div>
	);
};

export default FloatingButtons;
