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
