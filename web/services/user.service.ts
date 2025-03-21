import { ApiClient } from '@/lib/api-client';
import { PersonalityResponse } from '@/types/user';

export class UserService {
	static async updateUserPersonality(personality_data: string[]) {
		return ApiClient.put<PersonalityResponse>(`/api/users/personality`, {
			personality: personality_data,
		});
	}
	static async getUserPersonality() {
		return ApiClient.get<PersonalityResponse>(`/api/users/personality`);
	}
}
