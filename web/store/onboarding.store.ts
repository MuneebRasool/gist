import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { QuestionWithOptions } from '@/types/agent';
import { SimplifiedEmail } from '@/services/agent/onboarding.service';
import { EmailMessage } from '@/services/nylas/email.service';

interface OnboardingState {
	topEmails: EmailMessage[];
	// Email rating related state
	ratedEmails: SimplifiedEmail[];
	emailRatings: Record<string, number>;
	userEmail: string | null;
	domain: string | null;

	// Questions related state
	questions: QuestionWithOptions[];
	summary: string;
	answers: Record<string, string>;

	// UI state
	isLoading: boolean;
	isCompleted: boolean;
	currentStep: 'email-rating' | 'questions' | 'reviewPersonality' | 'task_generation' | 'completed';

	// Actions
	setRatedEmails: (emails: SimplifiedEmail[]) => void;
	setEmailRatings: (ratings: Record<string, number>) => void;
	setUserEmail: (email: string | null) => void;
	setDomain: (domain: string | null) => void;
	setQuestions: (questions: QuestionWithOptions[]) => void;
	setSummary: (summary: string) => void;
	setAnswer: (question: string, answer: string) => void;
	setIsLoading: (isLoading: boolean) => void;
	setIsCompleted: (isCompleted: boolean) => void;
	setTopEmails: (emails: EmailMessage[]) => void;
	setCurrentStep: (step: 'email-rating' | 'questions' | 'reviewPersonality' | 'task_generation' | 'completed') => void;
	resetState: () => void;
}

const initialState = {
	topEmails: [],
	ratedEmails: [],
	emailRatings: {},
	userEmail: null,
	domain: null,
	questions: [],
	summary: '',
	answers: {},
	isLoading: false,
	isCompleted: false,
	currentStep: 'email-rating' as const,
};

export const useOnboardingStore = create<OnboardingState>()(
	persist(
		(set) => ({
			...initialState,

			setRatedEmails: (emails) => set({ ratedEmails: emails }),
			setTopEmails: (emails) => set({ topEmails: emails }),
			setEmailRatings: (ratings) => set({ emailRatings: ratings }),
			setUserEmail: (email) => set({ userEmail: email }),
			setDomain: (domain) => set({ domain: domain }),
			setQuestions: (questions) => set({ questions }),
			setSummary: (summary) => set({ summary }),
			setAnswer: (question, answer) =>
				set((state) => ({
					answers: {
						...state.answers,
						[question]: answer,
					},
				})),
			setIsLoading: (isLoading) => set({ isLoading }),
			setIsCompleted: (isCompleted) => set({ isCompleted }),
			setCurrentStep: (step) => set({ currentStep: step }),
			resetState: () =>
				set({
					topEmails: [],
					ratedEmails: [],
					emailRatings: {},
					userEmail: null,
					domain: null,
					questions: [],
					summary: '',
					answers: {},
					isLoading: false,
					isCompleted: false,
					currentStep: 'email-rating',
				}),
		}),
		{
			name: 'onboarding-storage',
			partialize: (state) => ({
				ratedEmails: state.ratedEmails,
				topEmails: state.topEmails,
				emailRatings: state.emailRatings,
				userEmail: state.userEmail,
				domain: state.domain,
				questions: state.questions,
				answers: state.answers,
				summary: state.summary,
				currentStep: state.currentStep,
				isCompleted: state.isCompleted,
			}),
		}
	)
);
