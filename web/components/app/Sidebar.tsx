'use client';
import { Home, ListTodo, Bell, User, Mic } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';

const navItems = [
  { icon: Home, label: 'Home', href: '/app/dashboard' },
  { icon: ListTodo, label: 'Tasks', href: '/app/tasks' },
  { icon: Bell, label: 'Notifications', href: '/app/notifications' },
  { icon: User, label: 'Profile', href: '/app/profile' },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 flex h-screen w-20 flex-col items-center border-r border-border/30 bg-gradient-to-b from-rose-50/90 to-white/90 py-10 backdrop-blur-sm supports-[backdrop-filter]:bg-white/60">
      <div className="flex flex-col items-center gap-6">
        {navItems.map((item) => (
          <Tooltip key={item.href} delayDuration={0}>
            <TooltipTrigger asChild>
              <Link
                href={item.href}
                className={cn(
                  'group relative flex h-12 w-12 items-center justify-center rounded-xl transition-all duration-200 hover:bg-white hover:shadow-md',
                  pathname === item.href 
                    ? 'bg-white text-primary shadow-md' 
                    : 'text-gray-600'
                )}
              >
                <item.icon className="h-6 w-6 transition-transform duration-200 group-hover:scale-110" />
              </Link>
            </TooltipTrigger>
            <TooltipContent side="right" className="border-none bg-primary/90 text-white">
              {item.label}
            </TooltipContent>
          </Tooltip>
        ))}
      </div>
      
      <div className="mt-auto mb-6">
        <Tooltip delayDuration={0}>
          <TooltipTrigger asChild>
            <button className="flex h-12 w-12 items-center justify-center rounded-xl text-gray-600 transition-all duration-200 hover:bg-white hover:shadow-md">
              <Mic className="h-6 w-6" />
            </button>
          </TooltipTrigger>
          <TooltipContent side="right" className="border-none bg-primary/90 text-white">
            Voice Commands
          </TooltipContent>
        </Tooltip>
      </div>
    </aside>
  );
}
