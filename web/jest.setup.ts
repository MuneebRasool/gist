import '@testing-library/jest-dom';

jest.mock('next-auth/react', () => ({
	useSession: jest.fn(),
}));
