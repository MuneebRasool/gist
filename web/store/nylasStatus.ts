import { create } from 'zustand';
import { NylasAuthService } from '@/services/nylas/auth.service';

interface GmailStore {
	isConnected: boolean;
	isLoading: boolean;
	email: string | null;
	checkConnection: () => Promise<void>;
}

export const useNylasStatusStore = create<GmailStore>((set) => ({
	isConnected: false,
	isLoading: true,
	email: null,
	checkConnection: async () => {
		try {
			set({ isLoading: true });
			const response = await NylasAuthService.getConnectionStatus();
			if (response.error) {
				console.error('Failed to check Gmail connection:', response.error.message);
				set({ isConnected: false, email: null });
				return;
			}
			set({ isConnected: response.data?.connected, email: response.data?.email });
		} catch (error) {
			console.error('Failed to check Gmail connection:', error);
			set({ isConnected: false, email: null });
		} finally {
			set({ isLoading: false });
		}
	},
}));
