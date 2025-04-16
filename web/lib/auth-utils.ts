import { signOut } from 'next-auth/react';

/**
 * Handles complete logout by signing out of next-auth and clearing localStorage
 */
export const handleLogout = async () => {
	// Clear all items from localStorage
	localStorage.clear();

	// Sign out from next-auth
	await signOut();
};
