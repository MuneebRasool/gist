import { create } from 'zustand';
import { QuestionWithOptions } from '@/types/agent';

interface OnboardingState {
	questions: QuestionWithOptions[];
	summary: string;
	answers: Record<string, string>;
	isLoading: boolean;
	isCompleted: boolean;
	setQuestions: (questions: QuestionWithOptions[]) => void;
	setSummary: (summary: string) => void;
	setAnswer: (question: string, answer: string) => void;
	setIsLoading: (isLoading: boolean) => void;
	setIsCompleted: (isCompleted: boolean) => void;
	resetState: () => void;
}

export const useOnboardingStore = create<OnboardingState>((set) => ({
	questions: [],
	summary: '',
	answers: {},
	isLoading: false,
	isCompleted: false,
	setQuestions: (questions) => set({ questions }),
	setSummary: (summary) => set({ summary }),
	setAnswer: (question, answer) => 
		set((state) => ({ 
			answers: { 
				...state.answers, 
				[question]: answer 
			} 
		})),
	setIsLoading: (isLoading) => set({ isLoading }),
	setIsCompleted: (isCompleted) => set({ isCompleted }),
	resetState: () => set({ 
		questions: [], 
		summary: '', 
		answers: {}, 
		isLoading: false, 
		isCompleted: false 
	}),
})); 