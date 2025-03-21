import { envConfig } from '@/config';
import { NylasAuthService } from '@/services/nylas/auth.service';
import { NextRequest, NextResponse } from 'next/server';

export const GET = async (req: NextRequest) => {
	try {
		const code = req.nextUrl.searchParams.get('code');
		if (!code) {
			return NextResponse.json({ status: 'error', errorMessage: 'No authorization code found' });
		}

		// Exchange code for user credentials
		const res = await NylasAuthService.storeGrantIdFromCode(code);
		if (res.error) {
			return NextResponse.json({ status: 'error', errorMessage: res.error.message });
		}

		// Get connection status to retrieve email
		const connectionStatus = await NylasAuthService.getConnectionStatus();
		if (connectionStatus.error) {
			return NextResponse.redirect(`${envConfig.APP_URL}/app`);
		}

		// Store email in query params for the onboarding page
		const email = connectionStatus.data?.email;

		// Redirect to onboarding page with email parameter
		if (email) {
			const encodedEmail = encodeURIComponent(email);
			// Redirect to onboarding page directly, the page will handle showing email rating step first
			return NextResponse.redirect(`${envConfig.APP_URL}/app/onboarding?email=${encodedEmail}`);
		}

		// Fallback if email is not available
		return NextResponse.redirect(`${envConfig.APP_URL}/app`);
	} catch (error) {
		console.error('OAuth exchange error:', error);
		return NextResponse.json({
			status: 'error',
			errorMessage: 'Failed to verify authorization code. Please try again.',
		});
	}
};
