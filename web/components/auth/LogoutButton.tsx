'use client';

import { Button } from '@/components/ui/button';
import { LogOut } from 'lucide-react';
import { handleLogout } from '@/lib/auth-utils';

export function LogoutButton() {
	return (
		<Button variant='ghost' size='sm' className='text-muted-foreground hover:text-foreground' onClick={handleLogout}>
			<LogOut className='mr-2 h-4 w-4' />
			Logout
		</Button>
	);
}
