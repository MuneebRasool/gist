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
import { LogOut, Settings } from 'lucide-react';

const ProfileDropdown = ({ setOpen }: { setOpen: (open: boolean) => void }) => {
	const { data: session } = useSession();
	const router = useRouter();

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
				<DropdownMenuItem className='cursor-pointer' onClick={() => router.push('/app/dashboard/settings')}>
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
