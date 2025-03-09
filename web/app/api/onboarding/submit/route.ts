import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';

export async function POST(req: NextRequest) {
  try {
    // Get user session
    const session = await getServerSession();
    if (!session) {
      return NextResponse.json({ error: { message: 'Unauthorized' } }, { status: 401 });
    }

    // Get answers from request body
    const body = await req.json();
    const { answers } = body;

    if (!answers || Object.keys(answers).length === 0) {
      return NextResponse.json(
        { error: { message: 'No answers provided' } },
        { status: 400 }
      );
    }

    // TODO: Send answers to the backend service once the endpoint is decided
    // For now, we'll just return a success response

    return NextResponse.json(
      { success: true, message: 'Onboarding answers submitted successfully' },
      { status: 200 }
    );
  } catch (error) {
    console.error('Error submitting onboarding answers:', error);
    return NextResponse.json(
      { error: { message: 'Failed to submit onboarding answers' } },
      { status: 500 }
    );
  }
} 