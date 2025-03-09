'use client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useState } from 'react';
import GoogleSignin from './GoogleSignin';

export default function SignInForm() {
  const [email, setEmail] = useState('');

  const handleEmailSignIn = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle email sign in logic here
  };

  return (
    <div className="w-full max-w-md space-y-8 rounded-3xl bg-white/90 p-8 backdrop-blur-sm">
      <div className="text-center">
        <h1 className="text-3xl font-semibold text-gray-700">Delegate your workflow with Gist</h1>
      </div>
      
      <form onSubmit={handleEmailSignIn} className="mt-8 space-y-4">
        <Input
          type="email"
          placeholder="name@yourdomain.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="h-12 rounded-lg border-gray-200 bg-white px-4 text-base"
        />
        
        <Button 
          type="submit" 
          className="h-12 w-full rounded-lg bg-black text-base font-medium text-white hover:bg-black/90"
        >
          Continue with email
        </Button>
      </form>

      <div className="relative my-6">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-gray-200"></div>
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="bg-white px-4 text-gray-500">or</span>
        </div>
      </div>

      <GoogleSignin />

      <p className="mt-4 text-center text-xs text-gray-500">
        By continuing, you agree to Gist's{' '}
        <a href="#" className="underline">Consumer Terms</a> and{' '}
        <a href="#" className="underline">Usage Policy</a>, and acknowledge their{' '}
        <a href="#" className="underline">Privacy Policy</a>.
      </p>
    </div>
  );
} 