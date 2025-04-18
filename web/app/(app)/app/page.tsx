import WelcomeMessage from '@/components/app/onboarding/WelcomeMessage';
import { NylasAuthService } from '@/services/nylas/auth.service';
import { redirect } from 'next/navigation';

export default async function HomePage() {
	const response = await NylasAuthService.getConnectionStatus();
	if (response.data?.connected) {
		return redirect('/app/dashboard');
	}
	return (
		<div className='flex min-h-screen items-center justify-center'>
			<WelcomeMessage />
		</div>
	);
}
