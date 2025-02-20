'use client';

import * as React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Loader2 } from 'lucide-react';
import { signIn } from 'next-auth/react';
import { Button } from '@/components/ui/button';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { toast } from 'sonner';
import { PasswordInput } from '@/components/ui/password-input';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { loginSchema } from '@/validations';
import GoogleIcon from '@/assets/GoogleIcon';
import GoogleSignin from '@/components/auth/GoogleSignin';

export default function LoginPage() {
	const [isLoading, setIsLoading] = React.useState(false);
	const router = useRouter();

	const form = useForm<z.infer<typeof loginSchema>>({
		resolver: zodResolver(loginSchema),
		defaultValues: {
			email: '',
			password: '',
		},
	});

	async function onSubmit(values: z.infer<typeof loginSchema>) {
		setIsLoading(true);
		const res = await signIn('credentials', {
			email: values.email,
			password: values.password,
			redirect: false,
		});
		if (res?.error) {
			toast.error('Invalid email or password');
		} else {
			router.push('/');
			toast.success('Logged in successfully');
		}
		setIsLoading(false);
	}

	return (
		<div className='flex min-h-screen items-center justify-center p-2 sm:p-4'>
			<Card className='w-full max-w-lg rounded-lg'>
				<CardHeader className='space-y-3 pb-8'>
					<CardTitle className='bg-gradient-to-r from-primary to-primary/80 bg-clip-text text-center text-3xl font-bold text-transparent'>
						Welcome back
					</CardTitle>
					<CardDescription className='text-center text-base'>
						Enter your credentials to access your account
					</CardDescription>
				</CardHeader>
				<CardContent className='space-y-6 p-6'>
					<Form {...form}>
						<form onSubmit={form.handleSubmit(onSubmit)} className='space-y-5'>
							<FormField
								control={form.control}
								name='email'
								render={({ field }) => (
									<FormItem>
										<FormLabel className='text-base'>Email</FormLabel>
										<FormControl>
											<Input placeholder='example@email.com' {...field} />
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
											<PasswordInput placeholder='Enter your password' {...field} />
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>
							<Button type='submit' className='w-full text-base font-medium' disabled={isLoading}>
								{isLoading && <Loader2 className='mr-2 h-5 w-5 animate-spin' />}
								Sign In
							</Button>
						</form>
					</Form>
				</CardContent>
				<CardFooter className='flex flex-col space-y-6 pt-3'>
					{/* <div className='relative w-full'>
						<div className='absolute inset-0 flex items-center'>
							<div className='w-full border-t border-muted' />
						</div>
						<div className='relative flex justify-center text-sm'>
							<span className='bg-background px-3 text-muted-foreground'>Or continue with</span>
						</div>
					</div>
					<GoogleSignin /> */}
					<p className='text-center text-sm text-muted-foreground'>
						Don&apos;t have an account?{' '}
						<Link
							href='/register'
							className='font-medium text-primary underline underline-offset-4 hover:text-primary/90'
						>
							Create an account
						</Link>
					</p>
				</CardFooter>
			</Card>
		</div>
	);
}
