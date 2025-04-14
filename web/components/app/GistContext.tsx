'use client';

import { useEffect, useState, useCallback } from 'react';
import { X, Mic, StopCircle } from 'lucide-react';

// Define types for the Web Speech API
interface SpeechRecognitionEvent extends Event {
	results: SpeechRecognitionResultList;
}

interface SpeechRecognitionResultList {
	[index: number]: SpeechRecognitionResult;
	length: number;
}

interface SpeechRecognitionResult {
	[index: number]: SpeechRecognitionAlternative;
	length: number;
	isFinal: boolean;
}

interface SpeechRecognitionAlternative {
	transcript: string;
	confidence: number;
}

interface SpeechRecognition {
	continuous: boolean;
	interimResults: boolean;
	start: () => void;
	stop: () => void;
	onresult: (event: SpeechRecognitionEvent) => void;
	onend: () => void;
}

declare global {
	interface Window {
		webkitSpeechRecognition: new () => SpeechRecognition;
		SpeechRecognition: new () => SpeechRecognition;
	}
}

export const GistContext = () => {
	const [isOpen, setIsOpen] = useState(false);
	const [isListening, setIsListening] = useState(false);
	const [transcript, setTranscript] = useState('');
	const [recognition, setRecognition] = useState<SpeechRecognition | null>(null);

	const startListening = useCallback(() => {
		setIsListening(true);

		// Check if browser supports speech recognition
		if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
			const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
			const recognitionInstance = new SpeechRecognition();

			recognitionInstance.continuous = true;
			recognitionInstance.interimResults = true;

			recognitionInstance.onresult = (event: SpeechRecognitionEvent) => {
				const transcript = Array.from(event.results)
					.map((result) => result[0])
					.map((result) => result.transcript)
					.join('');

				setTranscript(transcript);
			};

			recognitionInstance.onend = () => {
				if (isListening) {
					handleQuery(transcript);
					setIsListening(false);
					setIsOpen(false);
					setTranscript('');
				}
			};

			recognitionInstance.start();
			setRecognition(recognitionInstance);
		} else {
			console.error('Speech recognition not supported');
		}
	}, [isListening, transcript]);

	useEffect(() => {
		const handleKeyDown = (e: KeyboardEvent) => {
			// Check for Cmd + K (Mac) or Ctrl + K (Windows)
			if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
				e.preventDefault();
				setIsOpen(true);
				startListening();
			}
		};

		window.addEventListener('keydown', handleKeyDown);
		return () => window.removeEventListener('keydown', handleKeyDown);
	}, [startListening]);

	const handleQuery = (query: string) => {
		console.log('Query handled:', query);
	};

	const handleClose = () => {
		if (recognition) {
			recognition.stop();
		}
		setIsListening(false);
		setIsOpen(false);
		setTranscript('');
	};

	const handleStop = () => {
		if (recognition) {
			recognition.stop();
			console.log('Transcript:', transcript);
		}
		setIsListening(false);
		setIsOpen(false);
		setTranscript('');
	};

	if (!isOpen) return null;

	return (
		<>
			{/* Backdrop */}
			<div className='fixed inset-0 z-50 bg-foreground/30 backdrop-blur-sm' onClick={handleClose} />

			{/* Modal */}
			<div className='fixed left-1/2 top-1/2 z-50 w-full max-w-lg -translate-x-1/2 -translate-y-1/2 rounded-xl'>
				<div className='flex flex-col items-center gap-4'>
					<div className='flex h-32 w-full items-center justify-center'>
						<div
							className={`rounded-full p-4 ${
								isListening ? 'bg-red-100 dark:bg-red-900/30' : 'bg-gray-100 dark:bg-gray-700'
							}`}
						>
							{isListening ? (
								<StopCircle className='h-8 w-8 cursor-pointer text-red-500' onClick={handleStop} />
							) : (
								<Mic className='h-8 w-8 text-gray-500' />
							)}
						</div>
					</div>

					{transcript && (
						<div className='w-full rounded-lg bg-gray-50 p-4 dark:bg-gray-900'>
							<p className='text-gray-600 dark:text-gray-300'>{transcript}</p>
						</div>
					)}

					{isListening && (
						<button onClick={handleStop} className='mt-2 rounded-lg bg-red-500 px-4 py-2 text-white hover:bg-red-600'>
							Stop Listening
						</button>
					)}
				</div>
			</div>
		</>
	);
};
