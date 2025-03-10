'use client';
import { Home, ListTodo, Bell, User, Mic, ChevronLeft, ChevronRight, Menu } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';

const navItems = [
  { icon: Home, label: 'Home', href: '/app/dashboard' },
  { icon: ListTodo, label: 'Tasks', href: '/app/tasks' },
  { icon: Bell, label: 'Notifications', href: '/app/notifications' },
  { icon: User, label: 'Profile', href: '/app/profile' },
];

interface SidebarProps {
  topOffset?: number;
}

// Create a custom event for sidebar collapse state
const SIDEBAR_COLLAPSE_EVENT = 'sidebar-collapse-change';

export default function Sidebar({ topOffset = 0 }: SidebarProps) {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  // Emit custom event when collapsed state changes
  useEffect(() => {
    const event = new CustomEvent(SIDEBAR_COLLAPSE_EVENT, { 
      detail: { isCollapsed } 
    });
    window.dispatchEvent(event);
  }, [isCollapsed]);

  return (
    <aside 
      className={cn(
        "fixed left-0 flex h-screen flex-col bg-[#e6dcda] py-10 backdrop-blur-sm transition-all duration-300",
        isCollapsed ? "w-16" : "w-56"
      )}
      style={{ top: topOffset }}
    >
      <Button 
        variant="ghost" 
        size="icon" 
        className="absolute -right-3 top-12 z-10 h-6 w-6 rounded-full bg-white shadow-md"
        onClick={() => setIsCollapsed(!isCollapsed)}
      >
        {isCollapsed ? <ChevronRight className="h-3 w-3" /> : <ChevronLeft className="h-3 w-3" />}
      </Button>

      <div className="flex flex-col items-center gap-6">
        {navItems.map((item) => (
          <Tooltip key={item.href} delayDuration={0}>
            <TooltipTrigger asChild>
              <Link
                href={item.href}
                className={cn(
                  "group relative flex h-12 items-center gap-3 rounded-xl px-3 transition-all duration-200 hover:bg-white hover:shadow-md",
                  pathname === item.href 
                    ? "bg-white text-primary shadow-md" 
                    : "text-gray-600",
                  isCollapsed ? "justify-center w-12" : "w-48 justify-start"
                )}
              >
                <item.icon className="h-6 w-6 transition-transform duration-200 group-hover:scale-110" />
                {!isCollapsed && <span className="font-medium">{item.label}</span>}
              </Link>
            </TooltipTrigger>
            {isCollapsed && (
              <TooltipContent side="right" className="border-none bg-primary/90 text-white">
                {item.label}
              </TooltipContent>
            )}
          </Tooltip>
        ))}
      </div>
      
      <div className="mt-auto mb-6 flex justify-center">
        <Tooltip delayDuration={0}>
          <TooltipTrigger asChild>
            <button 
              className={cn(
                "flex h-12 items-center gap-3 rounded-xl text-gray-600 transition-all duration-200 hover:bg-white hover:shadow-md",
                isCollapsed ? "justify-center w-12" : "w-48 justify-start px-3"
              )}
            >
              <Mic className="h-6 w-6" />
              {!isCollapsed && <span className="font-medium">Voice Commands</span>}
            </button>
          </TooltipTrigger>
          {isCollapsed && (
            <TooltipContent side="right" className="border-none bg-primary/90 text-white">
              Voice Commands
            </TooltipContent>
          )}
        </Tooltip>
      </div>
    </aside>
  );
}
