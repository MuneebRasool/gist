import React from 'react';

export default function OnboardingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-background">
      <main className="flex-1">
        <div className="flex flex-col min-h-screen">
          <header className="border-b py-4">
            <div className="container flex justify-center">
              <h1 className="text-2xl font-bold">GIST</h1>
            </div>
          </header>
          <div className="flex-1 py-8">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
} 