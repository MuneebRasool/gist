export function toCamelCase(string: string) {
	return string.replace(/([-_][a-z])/g, (group) => group.toUpperCase().replace('-', '').replace('_', ''));
}

export function toKebabCase(string: string) {
	return string
		.replace(/([a-z])([A-Z])/g, '$1-$2')
		.replace(/[\s_]+/g, '-')
		.toLowerCase();
}

export function toSnakeCase(string: string) {
	return string
		.replace(/([a-z])([A-Z])/g, '$1_$2')
		.replace(/[\s-]+/g, '_')
		.toLowerCase();
}

export function removeSpecialChars(string: string) {
	return string.replace(/[^a-zA-Z0-9 ]/g, '');
}

export function isEmpty(string: string) {
	return !string || string.trim().length === 0;
}

export function truncate(string: string, length: number, suffix = '...') {
	if (!string || string.length <= length) return string;
	return string.slice(0, length).trim() + suffix;
}

export function countOccurrences(string: string, searchString: string) {
	return string.split(searchString).length - 1;
}

export const slugify = (text: string) =>
	text
		.toString()
		.toLowerCase()
		.replace(/\s+/g, '-') // Replace spaces with -
		.replace(/[^\w-]+/g, '') // Remove all non-word chars
		.replace(/--+/g, '-') // Replace multiple - with single -
		.replace(/^-+/, '') // Trim - from start of text
		.replace(/-+$/, ''); // Trim - from end of text

export function extractNumbers(string: string) {
	return string.replace(/[^0-9]/g, '');
}

export function isAlphabetic(string: string) {
	return /^[A-Za-z]+$/.test(string);
}

export function isNumeric(string: string) {
	return /^[0-9]+$/.test(string);
}

export const enumToText = (text: string) => {
	return text
		.split('_')
		.map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
		.join(' ');
};

export const capitalizeFirstLetter = (text: string) => {
	return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
};

export const capitalizeEachWord = (text: string) => {
	return text.split(' ').map(capitalizeFirstLetter).join(' ');
};
