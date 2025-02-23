export type LoginResponse = {
	access_token: string;
	user: UserDto;
	token_type: string;
};

export type UserDto = {
	id: string;
	name: string;
	email: string;
	avatar?: string;
	nylas_email?: string;
};

export type UserUpdateRequest = {
	name?: string;
	email?: string;
	avatar?: string;
};

export type RegisterRequest = {
	name: string;
	email: string;
	avatar?: string;
	password: string;
};

export type GoogleAuthRequest = {
	id_token: string;
	user_data: {
		email: string;
		name: string;
		picture?: string;
	};
};
