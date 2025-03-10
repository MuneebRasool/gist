'use client';

import React from 'react';
import { motion } from 'framer-motion';

export default function OnboardingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gradient-to-r from-[#e6dcda] via-[#cfc6cb] to-[#ced4d8]">
      <main className="flex-1">
        <div className="flex min-h-screen flex-col">
          <header className="absolute left-8 top-8 flex items-center gap-3">
            <div className="h-10 w-10 rounded-full bg-gray-300/50"></div>
            <motion.p
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, ease: "easeOut" }}
              className="text-lg font-medium text-gray-700"
            >
              Hi, I&apos;m Gist!
            </motion.p>
          </header>
          
          <div className="flex-1">
            {children}
          </div>
          
          <footer className="py-6">
            <div className="container mx-auto">
              <div className="flex justify-center">
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.8, duration: 0.5 }}
                  className="flex items-center gap-3 rounded-full bg-white/80 px-4 py-2 text-xs font-medium text-gray-500 shadow-sm backdrop-blur-sm"
                >
                  <span>© {new Date().getFullYear()} GIST</span>
                  <span className="h-1 w-1 rounded-full bg-gray-300"></span>
                  <span>All rights reserved</span>
                </motion.div>
              </div>
            </div>
          </footer>
        </div>
      </main>
    </div>
  );
} 