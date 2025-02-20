import { render, screen } from '@testing-library/react';
import HomePage from '@/app/page';
import { useSession } from 'next-auth/react';

describe('Page', () => {
	it('renders unauthenticated state with main CTA', () => {
		(useSession as jest.Mock).mockReturnValue({
			data: null,
			status: 'unauthenticated',
		});

		render(<HomePage />);
	});

	it('renders authenticated state with user info', () => {
		(useSession as jest.Mock).mockReturnValue({
			data: {
				user: {
					name: 'Test User',
					email: 'test@example.com',
				},
			},
			status: 'authenticated',
		});

		render(<HomePage />);
	});
});
