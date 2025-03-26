import { Button } from '@/components/ui/button';
import { Mail, Calendar } from 'lucide-react';
import { motion } from 'framer-motion';
import { useState } from 'react';
import { useSession } from 'next-auth/react';
import { NylasAuthService } from '@/services/nylas/auth.service';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';

export default function AcknowledgeForm() {
	const [isLoading, setIsLoading] = useState(false);
	const { data: session } = useSession();
	const router = useRouter();
	const userName = session?.user?.name?.split(' ')[0] || 'there';

	const handleAcknowledge = async () => {
		try {
			setIsLoading(true);
			const res = await NylasAuthService.getAuthUrl();
			if (res.error) {
				toast.error(res.error.message);
			} else {
				router.push(res.data?.url ?? '');
			}
		} catch (error) {
			console.error('Failed to get auth URL:', error);
			toast.error('Failed to connect email. Please try again.');
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className='w-full max-w-xl px-4'>
			<div className='rounded-3xl bg-background/70 p-8 shadow-lg backdrop-blur-sm'>
				<div className='mb-6 flex items-center gap-3'>
					<h2 className='text-xl font-semibold text-gray-700'>Hi {userName},</h2>
				</div>

				<p className='mb-4 text-gray-600'>It&apos;s so nice to meet you.</p>
				<p className='mb-6 text-gray-600'>
					I&apos;d love for me to get to know you a little bit so I can better assist you. To help me with that, here
					are some access I need.
				</p>

				<div className='space-y-4'>
					<div className='rounded-xl border bg-background p-4'>
						<div className='flex items-center gap-3'>
							<Mail className='h-6 w-6 text-muted-foreground' />
							<p className='text-sm text-muted-foreground'>Grant Gist access to your email.</p>
						</div>
					</div>

					<div className='rounded-xl border bg-background p-4'>
						<div className='flex items-center gap-3'>
							<Calendar className='h-6 w-6 text-muted-foreground' />
							<p className='text-sm text-muted-foreground'>Allow Gist to access your calendar.</p>
						</div>
					</div>

					<Button
						onClick={handleAcknowledge}
						disabled={isLoading}
						className='mt-4 h-12 w-full bg-foreground text-base font-medium text-background hover:bg-foreground/90'
					>
						{isLoading ? (
							<div className='flex items-center gap-2'>
								<div className='h-4 w-4 animate-spin rounded-full border-2 border-border border-t-transparent' />
								Connecting...
							</div>
						) : (
							'Add Account'
						)}
					</Button>
				</div>
			</div>
		</motion.div>
	);
}
