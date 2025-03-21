import { Button } from '@/components/ui/button';
import { TaskEmailResponse } from '@/types/tasks';
import { Mail, Trash2 } from 'lucide-react';
import React from 'react';

interface TaskEmailProps {
	email: TaskEmailResponse;
}

const TaskEmail = ({ email }: TaskEmailProps) => {
	return (
		<div className='flex items-center justify-between gap-4 p-4'>
			<div>
				<h3 className='text-lg font-medium'>Email {email.messageId}</h3>
				<div className='line-clamp-2 text-muted-foreground'>{email.snippet}</div>
			</div>
			<div className='flex'>
				<Button variant='ghost' size='icon'>
					<Mail className='h-4 w-4' />
				</Button>
				<Button variant='ghost' size='icon'>
					<Trash2 className='h-4 w-4' />
				</Button>
			</div>
		</div>
	);
};

export default TaskEmail;
