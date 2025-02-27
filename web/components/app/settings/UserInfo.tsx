import React, { useEffect } from 'react';
import { useUserStore } from '@/store';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { Skeleton } from '@/components/ui/skeleton';
import { Separator } from '@/components/ui/separator';

const UserInfo = () => {
	const { user, isLoading, error, fetchUserInfo } = useUserStore();

	useEffect(() => {
		fetchUserInfo();
	}, [fetchUserInfo]);

	if (error) {
		return (
			<Card className='border-destructive'>
				<CardContent className='pt-6'>
					<p className='text-destructive'>{error}</p>
				</CardContent>
			</Card>
		);
	}

	if (isLoading) {
		return (
			<Card>
				<CardContent className='space-y-4 pt-6'>
					<div className='flex items-center space-x-4'>
						<Skeleton className='h-12 w-12 rounded-full' />
						<div className='space-y-2'>
							<Skeleton className='h-4 w-[200px]' />
							<Skeleton className='h-4 w-[150px]' />
						</div>
					</div>
				</CardContent>
			</Card>
		);
	}

	if (!user) {
		return null;
	}

	return (
		<>
			<Card className='w-full border-none bg-transparent shadow-none'>
				<CardHeader className='px-2 pb-4'>
					<div className='flex items-center justify-between'>
						<CardTitle className='text-xl font-semibold'>
							<h3>Profile Information</h3>
						</CardTitle>
					</div>
					<CardDescription>Manage your profile and view personality insights</CardDescription>
				</CardHeader>
				<CardContent className='px-2'>
					<div className='flex items-start space-x-6'>
						<Avatar className='h-20 w-20'>
							<AvatarImage src={user.avatar} alt={user.name} />
							<AvatarFallback className='text-lg'>
								{user.name
									.split(' ')
									.map((n) => n[0])
									.join('')
									.toUpperCase()}
							</AvatarFallback>
						</Avatar>
						<div className='space-y-4'>
							<div>
								<h3 className='text-lg font-medium'>{user.name}</h3>
								<p className='text-muted-foreground'>{user.email}</p>
							</div>
							{user.nylas_email && (
								<div>
									<p className='text-sm font-medium'>Connected Email</p>
									<p className='text-sm text-muted-foreground'>{user.nylas_email}</p>
								</div>
							)}
							<Sheet>
								<SheetTrigger asChild>
									<Button variant='outline'>View Personality Insights</Button>
								</SheetTrigger>
								<SheetContent className='min-w-full overflow-hidden sm:min-w-[600px]'>
									<SheetHeader>
										<SheetTitle>Your Personality Insights</SheetTitle>
										<SheetDescription>Based on your communication patterns and interactions</SheetDescription>
									</SheetHeader>
									<div className='mt-6 h-[calc(100vh-130px)] space-y-4 overflow-y-auto'>
										{user.personality && user.personality.length > 0 ? (
											user.personality.map((trait, index) => <div key={index}>{trait}</div>)
										) : (
											<p className='text-sm text-muted-foreground'>
												No personality insights available yet. Continue using the platform to generate insights.
											</p>
										)}
									</div>
								</SheetContent>
							</Sheet>
						</div>
					</div>
				</CardContent>
			</Card>
			<Separator />
		</>
	);
};

export default UserInfo;
