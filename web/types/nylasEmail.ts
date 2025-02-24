export type GetEmailOptions = {
	limit?: number;
	offset?: string;
	unread?: boolean;
	starred?: boolean;
	in_folder?: string;
	/**
	 * received_after is a Unix timestamp in seconds.
	 */
	received_after?: number;
	/**
	 * received_before is a Unix timestamp in seconds.
	 */
	received_before?: number;
	subject?: string;
};

export type EmailParticipant = {
	name: string;
	email: string;
};

export type Email = {
	id: string;
	subject: string;
	from: EmailParticipant[];
	to: EmailParticipant[];
	cc: EmailParticipant[];
	bcc: EmailParticipant[];
	reply_to: EmailParticipant[];
	date: string;
	snippet: string;
	body: string;
	unread: boolean;
	starred: boolean;
};

export type EmailResponse = {
	data: Email[];
	next_cursor: string;
};
