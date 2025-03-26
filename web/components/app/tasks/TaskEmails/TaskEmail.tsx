import { Button } from '@/components/ui/button';
import { TaskEmailResponse } from '@/types/tasks';
import { Mail, Trash2 } from 'lucide-react';
import React, { useState } from 'react';
import EmailSheet from '../EmailSheet';

interface TaskEmailProps {
	email: TaskEmailResponse;
}

const TaskEmail = ({ email }: TaskEmailProps) => {
	const [isOpen, setIsOpen] = useState(false);

	return (
		<>
			<div className='flex items-center justify-between gap-4 p-4'>
				<div>
					<h3 className='line-clamp-2 text-lg font-medium'>Email {email.subject}</h3>
					<div className='line-clamp-2 text-muted-foreground'>{email.snippet}</div>
				</div>
				<div className='flex'>
					<Button variant='ghost' size='icon' onClick={() => setIsOpen(true)}>
						<Mail className='h-4 w-4' />
					</Button>
					<Button variant='ghost' size='icon'>
						<Trash2 className='h-4 w-4' />
					</Button>
				</div>
			</div>

			<EmailSheet isOpen={isOpen} setIsOpen={setIsOpen} messageId={email.messageId} />
		</>
	);
};

export default TaskEmail;
