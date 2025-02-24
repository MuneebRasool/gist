import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import EmailService from '@/services/nylas/email.service';
import { AgentService } from '@/services/agent.service';
import { useTasksStore } from '@/store/tasks';
import { useState } from 'react';
import { toast } from 'sonner';
import { Loader2, Mail, Shield, ListTodo } from 'lucide-react';
import { Email } from '@/types/nylasEmail';
import { ExtractedEmailData } from '@/types/agent';

type Step = 'fetch' | 'classify' | 'extract' | 'complete';

export const TaskExtractorOnboarding = ({ userId }: { userId: string }) => {
	const [step, setStep] = useState<Step>('fetch');
	const [emails, setEmails] = useState<Email[]>([]);
	const [nonSpamEmails, setNonSpamEmails] = useState<ExtractedEmailData[]>([]);
	const [loading, setLoading] = useState(false);
	const { fetchTasks } = useTasksStore();

	const fetchEmails = async () => {
		try {
			setLoading(true);
			const response = await EmailService.getEmails({ limit: 30 });
			if (response.error) {
				toast.error(response.error.message);
			} else if (!response.data) {
				toast.error('Failed to fetch emails');
			} else {
				setEmails(response.data?.data);
				setStep('classify');
			}
		} catch (error) {
			toast.error('Failed to fetch emails');
		} finally {
			setLoading(false);
		}
	};

	const classifyEmails = async () => {
		try {
			setLoading(true);
			const response = await AgentService.classifySpams({
				emails: emails.map((email) => ({
					id: email.id,
					subject: email.subject,
					body: email.body,
					from_: email.from,
				})),
			});
			const nonSpam = response.data?.non_spam;
			setNonSpamEmails(nonSpam ?? []);
			setStep('extract');
		} catch (error) {
			toast.error('Failed to classify emails');
		} finally {
			setLoading(false);
		}
	};

	const extractTasks = async () => {
		try {
			setLoading(true);
			const response = await AgentService.extractTaskBatch({
				emails: nonSpamEmails.map((email) => ({
					id: email.id,
					body: email.body,
					subject: email.subject,
					from_: email.from_,
				})),
			});

			// Fetch updated tasks
			await fetchTasks(userId);
			setStep('complete');
		} catch (error) {
			toast.error('Failed to extract tasks');
		} finally {
			setLoading(false);
		}
	};

	const renderStep = () => {
		switch (step) {
			case 'fetch':
				return (
					<div className='flex flex-col items-center gap-6 py-8'>
						<Mail className='h-16 w-16 text-primary' />
						<div className='text-center'>
							<h3 className='text-lg font-semibold'>Fetch Recent Emails</h3>
							<p className='text-sm text-muted-foreground'>Let&apos;s start by fetching your recent emails</p>
						</div>
						<Button onClick={fetchEmails} disabled={loading} className='w-full max-w-xs'>
							{loading ? <Loader2 className='mr-2 h-4 w-4 animate-spin' /> : 'Fetch Emails'}
						</Button>
					</div>
				);

			case 'classify':
				return (
					<div className='flex flex-col items-center gap-6 py-8'>
						<Shield className='h-16 w-16 text-primary' />
						<div className='text-center'>
							<h3 className='text-lg font-semibold'>Filter Spam Emails</h3>
							<p className='text-sm text-muted-foreground'>
								We&apos;ll filter out spam emails to focus on important tasks
							</p>
						</div>
						<div className='w-full max-w-md space-y-4'>
							<div className='space-y-2'>
								{emails.map((email) => (
									<div key={email.id} className='rounded-lg border p-3 text-sm'>
										<p className='font-medium'>{email.subject}</p>
										<p className='text-muted-foreground'>
											From: {email.from[0]?.name || email.from[0]?.email || 'Unknown'}
										</p>
									</div>
								))}
							</div>
							<Button onClick={classifyEmails} disabled={loading} className='w-full'>
								{loading ? <Loader2 className='mr-2 h-4 w-4 animate-spin' /> : 'Filter Emails'}
							</Button>
						</div>
					</div>
				);

			case 'extract':
				return (
					<div className='flex flex-col items-center gap-6 py-8'>
						<ListTodo className='h-16 w-16 text-primary' />
						<div className='text-center'>
							<h3 className='text-lg font-semibold'>Extract Tasks</h3>
							<p className='text-sm text-muted-foreground'>Now we&apos;ll extract tasks from your non-spam emails</p>
						</div>
						<div className='w-full max-w-md space-y-4'>
							<div className='space-y-2'>
								{nonSpamEmails.map((email) => (
									<div key={email.id} className='rounded-lg border p-3 text-sm'>
										<p className='font-medium'>{email.subject}</p>
										<p className='text-muted-foreground'>
											From: {email.from_[0]?.name || email.from_[0]?.email || 'Unknown'}
										</p>
									</div>
								))}
							</div>
							<Button onClick={extractTasks} disabled={loading} className='w-full'>
								{loading ? <Loader2 className='mr-2 h-4 w-4 animate-spin' /> : 'Extract Tasks'}
							</Button>
						</div>
					</div>
				);

			case 'complete':
				return (
					<div className='flex flex-col items-center gap-6 py-8'>
						<div className='rounded-full bg-primary/10 p-3'>
							<ListTodo className='h-12 w-12 text-primary' />
						</div>
						<div className='text-center'>
							<h3 className='text-lg font-semibold'>Tasks Extracted!</h3>
							<p className='text-sm text-muted-foreground'>
								Your tasks have been successfully extracted. You can now view them below.
							</p>
						</div>
					</div>
				);
		}
	};

	return (
		<Card className='mx-auto w-full max-w-2xl'>
			<CardHeader>
				<CardTitle>Extract Tasks from Emails</CardTitle>
				<CardDescription>Let&apos;s help you extract tasks from your recent emails</CardDescription>
			</CardHeader>
			<CardContent>{renderStep()}</CardContent>
		</Card>
	);
};
