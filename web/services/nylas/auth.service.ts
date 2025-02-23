import { ApiClient } from '@/lib/api-client';
import { UserDto } from '@/types/auth';

/**
 * Service class for handling Nylas authentication operations
 */
export class NylasAuthService {
	/**
	 * Retrieves the Nylas authentication URL
	 * @returns The authentication URL for Nylas OAuth flow
	 */
	static async getAuthUrl() {
		return await ApiClient.get<{
			url: string;
		}>('/api/nylas/auth-url');
	}
	/**
	 * Exchanges the OAuth code for user credentials
	 * @param {string} code - The authorization code received from Nylas OAuth
	 * @returns User data after successful authentication
	 */
	static async storeGrantIdFromCode(code: string) {
		return await ApiClient.post<UserDto>('/api/nylas/exchange', { code });
	}

	/**
	 * Retrieves the connection status for Nylas
	 * @returns An object indicating the connection status
	 */
	static async getConnectionStatus() {
		return await ApiClient.get<{ connected: boolean; email: string }>('/api/nylas/connection-status');
	}
}
