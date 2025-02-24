import { create } from 'zustand';
import { AuthService } from '@/services/auth.service';
import { UserDto } from '@/types/auth';

interface UserState {
	user: UserDto | null;
	isLoading: boolean;
	error: string | null;
	fetchUserInfo: () => Promise<void>;
	setUser: (user: UserDto | null) => void;
	updateUser: (data: Partial<UserDto>) => Promise<void>;
	clearUser: () => void;
}

export const useUserStore = create<UserState>((set) => ({
	user: null,
	isLoading: false,
	error: null,

	fetchUserInfo: async () => {
		try {
			set({ isLoading: true, error: null });
			const user = await AuthService.getCurrentUserInfo();
			if (user.error) {
				throw new Error(user.error.message);
			}
			set({ user: user.data, isLoading: false });
		} catch (error) {
			set({ error: (error as Error).message, isLoading: false });
		}
	},

	setUser: (user) => {
		set({ user });
	},

	updateUser: async (data) => {
		try {
			set({ isLoading: true, error: null });
			const updatedUser = await AuthService.updateCurrentUser(data);
			if (updatedUser.error) {
				throw new Error(updatedUser.error.message);
			}
			set({ user: updatedUser.data, isLoading: false });
		} catch (error) {
			set({ error: (error as Error).message, isLoading: false });
		}
	},

	clearUser: () => {
		set({ user: null, error: null });
	},
}));
