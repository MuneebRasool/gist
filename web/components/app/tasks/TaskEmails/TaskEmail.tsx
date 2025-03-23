import { Button } from '@/components/ui/button';
import { TaskEmailResponse } from '@/types/tasks';
import { Mail, Trash2 } from 'lucide-react';
import React, { useState } from 'react';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from '@/components/ui/sheet';
import EmailService, { EmailMessage } from '@/services/nylas/email.service';
import { Loader2 } from 'lucide-react';
import { Email } from '@/types/nylasEmail';

interface TaskEmailProps {
	email: TaskEmailResponse;
}

const TaskEmail = ({ email }: TaskEmailProps) => {
	const [isOpen, setIsOpen] = useState(false);
	const [emailDetails, setEmailDetails] = useState<Email | null>(null);
	const [loading, setLoading] = useState(false);

	const handleOpenSheet = async () => {
		setIsOpen(true);
		setLoading(true);
		try {
			const response = await EmailService.getEmailById(email.messageId);
			console.log(response, email.messageId);
			if (response.data) {
				setEmailDetails(response.data);
			}
		} catch (error) {
			console.error('Failed to fetch email details:', error);
		} finally {
			setLoading(false);
		}
	};

	return (
		<>
			<div className='flex items-center justify-between gap-4 p-4'>
				<div>
					<h3 className='line-clamp-2 text-lg font-medium'>Email {email.subject}</h3>
					<div className='line-clamp-2 text-muted-foreground'>{email.snippet}</div>
				</div>
				<div className='flex'>
					<Button variant='ghost' size='icon' onClick={handleOpenSheet}>
						<Mail className='h-4 w-4' />
					</Button>
					<Button variant='ghost' size='icon'>
						<Trash2 className='h-4 w-4' />
					</Button>
				</div>
			</div>

			<Sheet open={isOpen} onOpenChange={setIsOpen}>
				<SheetContent className='w-[90%] overflow-y-auto sm:min-w-[540px]'>
					<SheetHeader>
						<SheetTitle>{emailDetails?.subject || email.subject}</SheetTitle>
					</SheetHeader>
					<div className='space-y-4 py-4'>
						{loading ? (
							<div className='flex items-center justify-center py-8'>
								<Loader2 className='h-6 w-6 animate-spin' />
							</div>
						) : emailDetails ? (
							<>
								<div>
									<div className='font-semibold'>From:</div>
									{emailDetails.from?.map((participant, index) => (
										<div key={index}>
											{participant.name} ({participant.email})
										</div>
									))}
								</div>
								<div>
									<div className='font-semibold'>To:</div>
									{emailDetails.to?.map((participant, index) => (
										<div key={index}>
											{participant.name} ({participant.email})
										</div>
									))}
								</div>
								{emailDetails.cc?.length > 0 && (
									<div>
										<div className='font-semibold'>CC:</div>
										{emailDetails.cc?.map((participant, index) => (
											<div key={index}>
												{participant.name} ({participant.email})
											</div>
										))}
									</div>
								)}
								<div className='border-t pt-4'>
									<div className='prose max-w-none' dangerouslySetInnerHTML={{ __html: emailDetails.body }} />
								</div>
							</>
						) : (
							<div>Failed to load email details</div>
						)}
					</div>
				</SheetContent>
			</Sheet>
		</>
	);
};

export default TaskEmail;
