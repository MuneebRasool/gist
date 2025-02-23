import { NylasAuthService } from '@/services/nylas/auth.service';
import { NextRequest, NextResponse } from 'next/server';

export const GET = async (req: NextRequest) => {
	try {
		const code = req.nextUrl.searchParams.get('code');
		if (!code) {
			return NextResponse.json({ status: 'error', errorMessage: 'No authorization code found' });
		}
		const res = await NylasAuthService.storeGrantIdFromCode(code);
		if (res.error) {
			return NextResponse.json({ status: 'error', errorMessage: res.error.message });
		}
		return NextResponse.redirect(`${req.nextUrl.origin}/app/settings`);
	} catch (error) {
		return NextResponse.json({
			status: 'error',
			errorMessage: 'Failed to verify authorization code. Please try again.',
		});
	}
};
