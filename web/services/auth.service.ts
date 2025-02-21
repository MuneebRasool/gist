import { ApiClient } from '@/lib/api-client';
import { LoginResponse, RegisterRequest, UserDto, UserUpdateRequest, GoogleAuthRequest } from '@/types/auth';

/**
 * Auth service
 */
export class AuthService {
	/**
	 * Login user and return JWT token
	 * @param email
	 * @param password
	 */
	static async login(email: string, password: string) {
		return await ApiClient.post<LoginResponse>('/api/auth/login', { email, password });
	}

	/**
	 * Register a new user and send verification email
	 * @param data
	 */
	static async register(data: RegisterRequest) {
		return await ApiClient.post<UserDto>('/api/auth/register', data);
	}

	/**
	 * Verify user's email address
	 * @param email
	 * @param code
	 */
	static async verifyEmail(email: string, code: string) {
		return await ApiClient.post<boolean>('/api/auth/verify-email', { email, code });
	}

	/**
	 * Get current user information
	 */
	static async getCurrentUserInfo() {
		return await ApiClient.get<UserDto>('/api/auth/users/me');
	}

	/**
	 * Update current user
	 * @param data
	 */
	static async updateCurrentUser(data: UserUpdateRequest) {
		return await ApiClient.patch<UserDto>('/api/auth/users/me', data);
	}

	/**
	 * Delete current user
	 */
	static async deleteCurrentUser() {
		return await ApiClient.delete<boolean>('/api/auth/users/me');
	}

	/**
	 * Authenticate with Google
	 * @param data Google auth data
	 */
	static async googleAuth(data: GoogleAuthRequest) {
		return await ApiClient.post<LoginResponse>('/api/auth/google', data);
	}
}
