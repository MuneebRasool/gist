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
import GoogleSignin from '@/components/auth/GoogleSignin';
import SignInForm from '@/components/auth/SignInForm';

export default function LoginPage() {
	return (
		<main className="flex min-h-screen items-center justify-center bg-gradient-to-br from-rose-50 to-slate-100 p-4">
			<SignInForm />
		</main>
	);
}
