import { TaskResponse } from '@/types/tasks';
import { Card, CardContent } from '@/components/ui/card';
import React, { useState } from 'react';
import {
	CalendarDays,
	Mail,
	Loader2,
	AlertCircle,
	Video,
	Phone,
	ShoppingBag,
	Bug,
	BarChart,
	GripVertical,
} from 'lucide-react';
import { Sheet, SheetContent, SheetHeader, SheetTitle } from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import EmailService from '@/services/nylas/email.service';
import { Email } from '@/types/nylasEmail';
import { format } from 'date-fns';
import { toast } from 'sonner';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';

const getTaskIcon = (task: string) => {
	const taskLower = task.toLowerCase();
	if (taskLower.includes('video') || taskLower.includes('zoom') || taskLower.includes('meet')) return Video;
	if (taskLower.includes('call') || taskLower.includes('phone')) return Phone;
	if (taskLower.includes('bug') || taskLower.includes('fix')) return Bug;
	if (taskLower.includes('pick up') || taskLower.includes('buy') || taskLower.includes('get')) return ShoppingBag;
	return Mail;
};

const TaskCard = ({ task }: { task: TaskResponse }) => {
	const [email, setEmail] = useState<Email | null>(null);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const [open, setOpen] = useState(false);
	const [isCompleted, setIsCompleted] = useState(false);

	const fetchEmail = async () => {
		if (!task.messageId) return;
		if (loading) return;
		setOpen(true);
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

	const getPriorityColorClasses = (priority: string | undefined) => {
		switch (priority?.toLowerCase()) {
			case 'high':
				return 'bg-red-500/10 text-red-600 hover:bg-red-500/20';
			case 'medium':
				return 'bg-amber-500/10 text-amber-600 hover:bg-amber-500/20';
			case 'low':
				return 'bg-green-500/10 text-green-600 hover:bg-green-500/20';
			default:
				return 'bg-gray-500/10 text-gray-600 hover:bg-gray-500/20';
		}
	};

	const getDeadlineColorClasses = (deadline: string | undefined) => {
		if (!deadline) return 'bg-gray-500/5 text-gray-700';

		const deadlineLower = deadline.toLowerCase();
		if (deadlineLower.includes('before noon') || deadlineLower.includes('urgent')) {
			return 'bg-red-500/5 text-red-700';
		}
		if (deadlineLower.includes('eod') || deadlineLower.includes('end of day')) {
			return 'bg-gray-500/5 text-gray-800';
		}
		return 'bg-blue-500/5 text-blue-700';
	};

	const TaskIcon = getTaskIcon(task.task);

	return (
		<>
			<Card
				className={`group relative overflow-hidden border-none bg-background/80 shadow-sm transition-all hover:bg-white/90 hover:shadow-md ${isCompleted ? 'opacity-50' : ''}`}
			>
				<CardContent className='flex items-start gap-4 p-4'>
					<Checkbox
						checked={isCompleted}
						onCheckedChange={(checked) => setIsCompleted(checked as boolean)}
						className='mt-1'
					/>

					<div className='flex-1 space-y-2'>
						<div className='flex items-start justify-between gap-2'>
							<div className='flex items-center gap-2'>
								<div className={`rounded-full p-1.5 ${getPriorityColorClasses(task.priority)}`}>
									<TaskIcon className='h-4 w-4' />
								</div>
								<h3 className={`text-lg font-semibold text-gray-800 ${isCompleted ? 'line-through' : ''}`}>
									{task.task}
								</h3>
							</div>
							<div className='flex items-center gap-2'>
								{task.priority && (
									<Badge variant='outline' className={`rounded-full ${getPriorityColorClasses(task.priority)}`}>
										{task.priority}
									</Badge>
								)}
								{task.deadline && (
									<Badge variant='outline' className={`rounded-full ${getDeadlineColorClasses(task.deadline)}`}>
										{task.deadline}
									</Badge>
								)}
								<div className='cursor-grab opacity-0 transition-opacity group-hover:opacity-70'>
									<GripVertical className='h-5 w-5 text-gray-400' />
								</div>
							</div>
						</div>

						{/* Display scores if available */}
						{(task.relevance_score !== undefined ||
							task.utility_score !== undefined ||
							task.cost_score !== undefined) && (
							<div className='flex flex-wrap gap-3 text-xs text-gray-600'>
								{task.relevance_score !== undefined && (
									<div className='flex items-center gap-1'>
										<BarChart className='h-3 w-3' />
										<span>Relevance: {task.relevance_score}</span>
									</div>
								)}
								{task.utility_score !== undefined && (
									<div className='flex items-center gap-1'>
										<BarChart className='h-3 w-3' />
										<span>Utility: {task.utility_score}</span>
									</div>
								)}
								{task.cost_score !== undefined && (
									<div className='flex items-center gap-1'>
										<BarChart className='h-3 w-3' />
										<span>Cost: {task.cost_score}</span>
									</div>
								)}
							</div>
						)}

						<div className='flex items-center justify-between'>
							<p className='text-sm text-gray-600'>Created {format(new Date(task.createdAt), 'MMM d, yyyy')}</p>
							{task.messageId && (
								<Button
									variant='ghost'
									size='sm'
									className='hover:bg-primary/10 hover:text-primary'
									onClick={fetchEmail}
								>
									{loading ? <Loader2 className='h-4 w-4 animate-spin' /> : <Mail className='h-4 w-4' />}
									<span className='ml-2'>View Email</span>
								</Button>
							)}
						</div>
					</div>
				</CardContent>
			</Card>

			<Sheet open={open} onOpenChange={setOpen}>
				<SheetContent className='min-w-full overflow-hidden sm:min-w-[600px]'>
					<SheetHeader>
						<SheetTitle className='text-2xl font-bold text-gray-900'>Email Details</SheetTitle>
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
										<h3 className='text-xl font-bold tracking-tight text-gray-900'>{email.subject}</h3>
										<p className='mt-2 text-sm text-gray-600'>{formatEmailDate(email.date)}</p>
									</div>

									<div className='space-y-3 rounded-lg bg-card p-4'>
										<div className='flex gap-3'>
											<span className='min-w-20 font-semibold text-gray-800'>From:</span>
											<span className='text-primary'>{email.from[0]?.name || email.from[0]?.email}</span>
										</div>
										<div className='flex gap-3'>
											<span className='min-w-20 font-semibold text-gray-800'>To:</span>
											<span className='text-gray-700'>{email.to.map((to) => to.name || to.email).join(', ')}</span>
										</div>
										{email.cc.length > 0 && (
											<div className='flex gap-3'>
												<span className='min-w-20 font-semibold text-gray-800'>CC:</span>
												<span className='text-gray-600'>{email.cc.map((cc) => cc.name || cc.email).join(', ')}</span>
											</div>
										)}
									</div>

									<Separator className='my-6' />

									<div className='prose prose-sm dark:prose-invert max-w-none text-gray-800'>
										<div dangerouslySetInnerHTML={{ __html: email.body }} />
									</div>
								</div>
							</ScrollArea>
						) : (
							<div className='flex h-full items-center justify-center'>
								<div className='text-center'>
									<Loader2 className='mx-auto h-8 w-8 animate-spin text-primary' />
									<p className='mt-2 text-sm text-gray-600'>Loading email...</p>
								</div>
							</div>
						)}
					</div>
				</SheetContent>
			</Sheet>
		</>
	);
};

export default TaskCard;
