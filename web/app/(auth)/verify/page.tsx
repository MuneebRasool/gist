'use client';

import * as React from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { InputOTP, InputOTPGroup, InputOTPSlot } from '@/components/ui/input-otp';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Loader2 } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { AuthService } from '@/services/auth.service';
import { Label } from '@/components/ui/label';

export default function VerifyPage() {
	const [isLoading, setIsLoading] = React.useState(false);
	const [otp, setOtp] = React.useState('');
	const [email, setEmail] = React.useState('');
	const router = useRouter();

	React.useEffect(() => {
		const storedEmail = localStorage.getItem('verificationEmail');
		if (!storedEmail) {
			router.push('/register');
			return;
		}
		setEmail(storedEmail);
	}, [router]);

	const handleVerify = async () => {
		if (otp.length !== 6) {
			toast.error('Please enter a valid OTP');
			return;
		}

		setIsLoading(true);
		try {
			const res = await AuthService.verifyEmail(email, otp);
			if (res.data) {
				toast.success('Email verified successfully');
				localStorage.removeItem('verificationEmail');
				router.push('/login');
			} else {
				toast.error('Invalid OTP');
			}
		} catch (error) {
			toast.error('Verification failed');
		} finally {
			setIsLoading(false);
		}
	};

	const handleResend = () => {
		toast.success('New OTP sent to your email');
	};

	return (
		<div className='flex min-h-screen items-center justify-center p-2 sm:p-4'>
			<Card className='w-full max-w-lg rounded-lg'>
				<CardHeader className='space-y-3 pb-4'>
					<CardTitle className='bg-gradient-to-r from-primary to-primary/80 bg-clip-text text-center text-3xl font-bold text-transparent'>
						Verify Your Email
					</CardTitle>
					<CardDescription className='text-center text-base'>Enter the 6-digit code sent to your email</CardDescription>
				</CardHeader>
				<CardContent className='space-y-6 p-6'>
					<div className='flex flex-col gap-2'>
						<Label htmlFor='email'>Email</Label>
						<Input value={email} disabled className='text-center' />
					</div>
					<div className='flex flex-col items-center gap-2'>
						<Label htmlFor='otp' className='w-full'>
							OTP
						</Label>
						<InputOTP maxLength={6} value={otp} onChange={(value) => setOtp(value)}>
							<InputOTPGroup>
								<InputOTPSlot index={0} />
								<InputOTPSlot index={1} />
								<InputOTPSlot index={2} />
								<InputOTPSlot index={3} />
								<InputOTPSlot index={4} />
								<InputOTPSlot index={5} />
							</InputOTPGroup>
						</InputOTP>
					</div>
					<Button onClick={handleVerify} className='w-full text-base font-medium' disabled={isLoading}>
						{isLoading && <Loader2 className='mr-2 h-5 w-5 animate-spin' />}
						Verify Email
					</Button>
				</CardContent>
				<CardFooter className='flex justify-center'>
					<Button variant='ghost' onClick={handleResend} className='text-sm text-muted-foreground'>
						Didn&apos;t receive code? Resend
					</Button>
				</CardFooter>
			</Card>
		</div>
	);
}
