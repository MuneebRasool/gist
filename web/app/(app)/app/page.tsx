'use client';

import { redirect } from 'next/navigation';
import { useNylasStatusStore } from '@/store';
import { useEffect } from 'react';
import { useSession } from 'next-auth/react';
import Loading from '@/app/loading';
import WelcomeMessage from '@/components/app/onboarding/WelcomeMessage';

export default function HomePage() {
  const { isConnected, isLoading: emailStatusLoading, checkConnection } = useNylasStatusStore();
  const { data: session } = useSession();

  useEffect(() => {
    if (session?.user?.id) {
      checkConnection();
    }
  }, [session?.user?.id, checkConnection]);

  if (emailStatusLoading) {
    return <Loading text="Checking your email connection..." />;
  }

  if (isConnected) {
    redirect('/app/dashboard');
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-rose-100/80 via-white to-blue-100/80">
      <WelcomeMessage />
    </div>
  );
}
