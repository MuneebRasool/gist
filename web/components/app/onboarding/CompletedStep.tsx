import React from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';

const CompletedStep = () => {
	const router = useRouter();

	const handleDashboardNavigation = () => {
		router.push('/app/dashboard');
	};

	return (
		<div className='flex h-full flex-col items-center justify-center'>
			<h1 className='mb-4 text-3xl font-semibold text-green-500'>Onboarding Completed!</h1>
			<p className='mb-8 text-gray-600'>You&apos;re all set. Get ready to explore your dashboard.</p>
			<Button variant='default' size='lg' onClick={handleDashboardNavigation}>
				Go to Dashboard
			</Button>
		</div>
	);
};

export default CompletedStep;
