import {
	addDays,
	differenceInDays,
	format,
	formatDistanceToNow,
	isAfter,
	isToday,
	isTomorrow,
	isValid,
	isYesterday,
	parseISO,
	subDays,
} from 'date-fns';

export const getRelativeTime = (date: string | Date) => {
	return formatDistanceToNow(new Date(date), { addSuffix: true });
};

export function isValidDate(date: any) {
	return isValid(date);
}

export const formatDate = (dateString: string | Date) => {
	const date = new Date(dateString);
	return format(date, 'dd MMM yyyy');
};

export const getTimeFromDate = (date: Date | string) => {
	return format(new Date(date), 'hh:mm a');
};

export const checkIfDateIsInFuture = (date: Date | string) => {
	return isAfter(new Date(date), new Date());
};

export const sanitizeTimeStampToDate = (timestamp: string) => {
	const date = new Date(timestamp);
	if (isValidDate(date)) {
		return date;
	}
	return null;
};

export const getCurrentTimestamp = () => {
	return Date.now();
};

export function parseDate(isoString: string) {
	return parseISO(isoString);
}

export function checkIsToday(date: Date | string) {
	return isToday(date);
}

export function checkIsTomorrow(date: Date | string) {
	return isTomorrow(date);
}

export function checkIsYesterday(date: Date | string) {
	return isYesterday(date);
}

export function addDaysToDate(date: Date | string, days: number) {
	return addDays(date, days);
}

export function subtractDaysFromDate(date: Date | string, days: number) {
	return subDays(date, days);
}

export function getDifferenceInDays(date1: Date | string, date2: Date | string) {
	return differenceInDays(date1, date2);
}
