'use client';

import * as React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Loader2 } from 'lucide-react';
import Link from 'next/link';

import { Button } from '@/components/ui/button';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage, FormDescription } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { PasswordInput } from '@/components/ui/password-input';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';
import { registerSchema } from '@/validations';
import { AuthService } from '@/services/auth.service';
import GoogleSignin from '@/components/auth/GoogleSignin';

export default function RegisterPage() {
	const [isLoading, setIsLoading] = React.useState(false);
	const router = useRouter();

	const form = useForm<z.infer<typeof registerSchema>>({
		resolver: zodResolver(registerSchema),
		defaultValues: {
			name: '',
			email: '',
			password: '',
			confirmPassword: '',
		},
	});

	async function onSubmit(values: z.infer<typeof registerSchema>) {
		setIsLoading(true);
		try {
			const res = await AuthService.register(values);
			if (res.data) {
				localStorage.setItem('verificationEmail', values.email);
				toast.success('Account created successfully. Please verify your email');
				router.push('/verify');
			} else {
				toast.error(res.error?.message);
			}
		} catch (error) {
			toast.error('An error occurred');
		} finally {
			setIsLoading(false);
		}
	}

	return (
		<div className='flex min-h-screen items-center justify-center p-2 sm:p-4'>
			<Card className='w-full max-w-lg rounded-lg'>
				<CardHeader className='space-y-3 pb-4'>
					<CardTitle className='text-center text-3xl font-bold'>Create an account</CardTitle>
					<CardDescription className='text-center text-base'>
						Enter your information to create your account
					</CardDescription>
				</CardHeader>
				<CardContent className='space-y-6 p-6'>
					<Form {...form}>
						<form onSubmit={form.handleSubmit(onSubmit)} className='space-y-5'>
							<FormField
								control={form.control}
								name='name'
								render={({ field }) => (
									<FormItem>
										<FormLabel className='text-base'>Full Name</FormLabel>
										<FormControl>
											<Input placeholder='John Doe' {...field} />
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>
							<FormField
								control={form.control}
								name='email'
								render={({ field }) => (
									<FormItem>
										<FormLabel className='text-base'>Email</FormLabel>
										<FormControl>
											<Input placeholder='example@email.com' type='email' {...field} />
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>
							<FormField
								control={form.control}
								name='password'
								render={({ field }) => (
									<FormItem>
										<FormLabel className='text-base'>Password</FormLabel>
										<FormControl>
											<PasswordInput placeholder='Create a password' {...field} />
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>
							<FormField
								control={form.control}
								name='confirmPassword'
								render={({ field }) => (
									<FormItem>
										<FormLabel className='text-base'>Confirm Password</FormLabel>
										<FormControl>
											<PasswordInput placeholder='Confirm your password' {...field} />
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>
							<Button type='submit' className='w-full text-base font-medium' disabled={isLoading}>
								{isLoading && <Loader2 className='mr-2 h-5 w-5 animate-spin' />}
								Create Account
							</Button>
						</form>
					</Form>
				</CardContent>
				<CardFooter className='flex flex-col space-y-3 pt-3'>
					<div className='relative w-full'>
						<div className='absolute inset-0 flex items-center'>
							<div className='w-full border-t border-muted' />
						</div>
						<div className='relative flex justify-center text-sm'>
							<span className='bg-background px-3 text-muted-foreground'>Or continue with</span>
						</div>
					</div>
					<GoogleSignin />
					<p className='text-center text-sm text-muted-foreground'>
						Already have an account?{' '}
						<Link href='/login' className='font-medium text-primary underline underline-offset-4 hover:text-primary/90'>
							Login here
						</Link>
					</p>
				</CardFooter>
			</Card>
		</div>
	);
}
