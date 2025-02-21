import React from 'react';
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useTheme } from 'next-themes';
import { Moon } from 'lucide-react';
import { Sun } from 'lucide-react';
import { LayoutDashboard, LogOut, Settings } from 'lucide-react';

const ProfileDropdown = ({ setOpen }: { setOpen: (open: boolean) => void }) => {
	const { data: session } = useSession();
	const router = useRouter();
	const { resolvedTheme, setTheme } = useTheme();

	return (
		<DropdownMenu>
			<DropdownMenuTrigger asChild>
				<Button variant='ghost' size='icon' className='rounded-full'>
					<Avatar className='h-8 w-8'>
						<AvatarImage src={session?.user?.image || ''} />
						<AvatarFallback>
							{session?.user?.name
								? session?.user?.name
										.split(' ')
										.map((word) => word[0])
										.join('')
										.slice(0, 2)
										.toUpperCase()
								: 'OG'}
						</AvatarFallback>
					</Avatar>
				</Button>
			</DropdownMenuTrigger>
			<DropdownMenuContent className='w-56'>
				<DropdownMenuItem
					className='cursor-pointer'
					onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
				>
					<Sun className='mr-2 size-4 rotate-0 scale-100 transition-transform dark:-rotate-90 dark:scale-0' />
					<Moon className='absolute mr-2 size-4 rotate-90 scale-0 transition-transform dark:rotate-0 dark:scale-100' />
					Switch Theme
				</DropdownMenuItem>
				<DropdownMenuItem className='cursor-pointer' onClick={() => router.push('/app/settings')}>
					<Settings className='mr-2 h-4 w-4' />
					Settings
				</DropdownMenuItem>
				<DropdownMenuItem
					onClick={() => {
						setOpen(true);
					}}
					className='cursor-pointer text-red-600 hover:!text-red-600'
				>
					<LogOut className='mr-2 h-4 w-4' />
					Sign out
				</DropdownMenuItem>
			</DropdownMenuContent>
		</DropdownMenu>
	);
};

export default ProfileDropdown;
