import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from '@/components/ui/sheet';
import EmailService from '@/services/nylas/email.service';
import { Email } from '@/types/nylasEmail';
import { Loader2 } from 'lucide-react';
import React, { useEffect, useState } from 'react';

interface EmailSheetProps {
	isOpen: boolean;
	setIsOpen: (isOpen: boolean) => void;
	messageId?: string;
}

const EmailSheet = ({ isOpen, setIsOpen, messageId }: EmailSheetProps) => {
	const [emailDetails, setEmailDetails] = useState<Email | null>(null);
	const [loading, setLoading] = useState(false);

	const getEmailDetails = async (messageId: string) => {
		try {
			setLoading(true);
			const res = await EmailService.getEmailById(messageId);
			if (res.data) {
				setEmailDetails(res.data);
			}
		} catch (error) {
			console.error(error);
		} finally {
			setLoading(false);
		}
	};

	useEffect(() => {
		if (messageId) {
			getEmailDetails(messageId);
		}
	}, [messageId]);

	if (!messageId) {
		return null;
	}

	return (
		<Sheet open={isOpen} onOpenChange={setIsOpen}>
			<SheetContent className='w-[90%] overflow-y-auto sm:min-w-[600px]'>
				<SheetHeader>
					<SheetTitle>{emailDetails?.subject || ''}</SheetTitle>
				</SheetHeader>
				<div className='space-y-4 py-4'>
					{loading ? (
						<div className='flex items-center justify-center py-8'>
							<Loader2 className='h-6 w-6 animate-spin' />
						</div>
					) : emailDetails ? (
						<>
							<div>
								<div className='font-semibold'>From:</div>
								{emailDetails.from?.map((participant, index) => (
									<div key={index}>
										{participant.name} ({participant.email})
									</div>
								))}
							</div>
							<div>
								<div className='font-semibold'>To:</div>
								{emailDetails.to?.map((participant, index) => (
									<div key={index}>
										{participant.name} ({participant.email})
									</div>
								))}
							</div>
							{emailDetails.cc?.length > 0 && (
								<div>
									<div className='font-semibold'>CC:</div>
									{emailDetails.cc?.map((participant, index) => (
										<div key={index}>
											{participant.name} ({participant.email})
										</div>
									))}
								</div>
							)}
							<div className='border-t pt-4'>
								<div className='prose max-w-none' dangerouslySetInnerHTML={{ __html: emailDetails.body }} />
							</div>
						</>
					) : (
						<div>Failed to load email details</div>
					)}
				</div>
			</SheetContent>
		</Sheet>
	);
};

export default EmailSheet;
