'use client';

import React from 'react';
import { motion } from 'framer-motion';

export default function OnboardingEmailRatingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gradient-to-r from-[#e6dcda] to-[#cfc6cb]">
      <main className="flex-1">
        <div className="flex min-h-screen flex-col">
          <motion.header 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="absolute left-8 top-8 z-10 flex items-center gap-3"
          >
            <div className="flex h-10 w-10 items-center justify-center overflow-hidden rounded-full bg-gray-300/50">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.5, type: "spring" }}
                className="text-lg font-medium text-gray-700"
              >
                G
              </motion.div>
            </div>
            <motion.p 
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.6 }}
              className="text-lg font-medium text-gray-700"
            >
              Hi, I&apos;m Gist!
            </motion.p>
          </motion.header>
          
          <div className="flex-1">
            {children}
          </div>
          
          <motion.footer
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="py-6"
          >
            <div className="container mx-auto">
              <div className="flex justify-center">
                <div className="flex items-center gap-3 rounded-full bg-white/80 px-4 py-2 text-xs font-medium text-gray-500 shadow-sm backdrop-blur-sm">
                  <span>© {new Date().getFullYear()} GIST</span>
                  <span className="h-1 w-1 rounded-full bg-gray-300"></span>
                  <span>All rights reserved</span>
                </div>
              </div>
            </div>
          </motion.footer>
        </div>
      </main>
    </div>
  );
} 