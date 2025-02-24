import { TaskResponse } from '@/types/tasks';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import React, { useState } from 'react';
import { CalendarDays, Mail, Loader2, AlertCircle } from 'lucide-react';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import EmailService from '@/services/nylas/email.service';
import { Email } from '@/types/nylasEmail';
import { format } from 'date-fns';
import { toast } from 'sonner';

const TaskCard = ({ task }: { task: TaskResponse }) => {
	const [email, setEmail] = useState<Email | null>(null);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);

	const fetchEmail = async () => {
		if (!task.messageId) return;

		try {
			setLoading(true);
			setError(null);
			const response = await EmailService.getEmailById(task.messageId);
			if (response.error) {
				toast.error(response.error.message);
			}
			if (response.data) {
				setEmail(response.data ?? null);
			}
		} catch (err) {
			setError('Failed to fetch email details');
			console.error('Error fetching email:', err);
		} finally {
			setLoading(false);
		}
	};

	const formatEmailDate = (dateString: string) => {
		return format(new Date(dateString), 'PPP p');
	};

	return (
		<Card
			key={task.task_id}
			className='group relative transition-all duration-300 hover:shadow-lg dark:hover:shadow-primary/5'
		>
			<CardHeader className='flex flex-row items-start justify-between space-y-0 pb-4'>
				<div className='space-y-3'>
					<CardTitle className='text-xl font-bold tracking-tight'>{task.task}</CardTitle>
					{task.deadline && (
						<CardDescription className='flex items-center gap-2 text-sm font-medium text-muted-foreground'>
							<CalendarDays className='h-4 w-4 text-primary' />
							{task.deadline}
						</CardDescription>
					)}
				</div>
				{task.messageId && (
					<Sheet>
						<SheetTrigger asChild>
							<Button
								variant='ghost'
								size='icon'
								className='rounded-full transition-colors hover:bg-primary/10 hover:text-primary'
								onClick={fetchEmail}
							>
								{loading ? <Loader2 className='h-5 w-5 animate-spin' /> : <Mail className='h-5 w-5' />}
							</Button>
						</SheetTrigger>
						<SheetContent className='min-w-full overflow-hidden sm:min-w-[600px]'>
							<SheetHeader>
								<SheetTitle className='text-2xl font-bold'>Email Details</SheetTitle>
							</SheetHeader>
							<div className='mt-6 h-full'>
								{error ? (
									<div className='flex items-center gap-2 rounded-md bg-destructive/10 p-4 text-destructive'>
										<AlertCircle className='h-5 w-5' />
										{error}
									</div>
								) : email ? (
									<ScrollArea className='h-[calc(100vh-120px)] pr-4'>
										<div className='space-y-6'>
											<div className='rounded-lg bg-muted/30 p-4'>
												<h3 className='text-xl font-bold tracking-tight'>{email.subject}</h3>
												<p className='mt-2 text-sm text-muted-foreground'>{formatEmailDate(email.date)}</p>
											</div>

											<div className='space-y-3 rounded-lg bg-card p-4'>
												<div className='flex gap-3'>
													<span className='min-w-20 font-semibold'>From:</span>
													<span className='text-primary'>{email.from[0]?.name || email.from[0]?.email}</span>
												</div>
												<div className='flex gap-3'>
													<span className='min-w-20 font-semibold'>To:</span>
													<span>{email.to.map((to) => to.name || to.email).join(', ')}</span>
												</div>
												{email.cc.length > 0 && (
													<div className='flex gap-3'>
														<span className='min-w-20 font-semibold'>CC:</span>
														<span className='text-muted-foreground'>
															{email.cc.map((cc) => cc.name || cc.email).join(', ')}
														</span>
													</div>
												)}
											</div>

											<Separator className='my-6' />

											<div className='prose prose-sm dark:prose-invert max-w-none'>
												<div dangerouslySetInnerHTML={{ __html: email.body }} />
											</div>
										</div>
									</ScrollArea>
								) : (
									<div className='flex h-full items-center justify-center'>
										<div className='text-center'>
											<Loader2 className='mx-auto h-8 w-8 animate-spin text-primary' />
											<p className='mt-2 text-sm text-muted-foreground'>Loading email...</p>
										</div>
									</div>
								)}
							</div>
						</SheetContent>
					</Sheet>
				)}
			</CardHeader>
			<CardContent>
				<div className='flex items-center justify-between'>
					<p className='text-sm text-muted-foreground'>Created {format(new Date(task.createdAt), 'MMM d, yyyy')}</p>
				</div>
			</CardContent>
		</Card>
	);
};

export default TaskCard;
