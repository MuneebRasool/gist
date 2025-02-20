import { z } from 'zod';

export const safeParse = <T>(parse: (_: any) => T, input: any): T => {
	try {
		const output = parse(input);
		return output;
	} catch {
		// return null;
		throw new Error(`Invalid input: ${input}`);
	}
};

export const getString = (input: any): string => {
	return z.string().parse(input);
};

export const getNonEmptyString = (input: any): string => {
	return z.string().min(1).parse(input);
};

export const getNumber = (input: any): number => {
	return z.number().or(z.string().regex(/^\d+$/).transform(Number)).parse(input);
};

export const getNonNegativeNumber = (input: any): number => {
	return z.number().min(0).or(z.string().regex(/^\d+$/).transform(Number)).parse(input);
};

export const getBoolean = (input: any): boolean => {
	return z
		.boolean()
		.or(z.enum(['true', 'false']).transform((val) => val === 'true'))
		.or(
			z
				.number()
				.min(0)
				.max(1)
				.transform((val) => Boolean(val))
		)
		.parse(input);
};

export const getArray = <T>(input: any): T[] => {
	return z.array(z.any()).parse(input);
};

export const getSingletonValue = <T>(input: T[]): T => {
	if (input.length !== 1) {
		throw new Error(`${input} is not a singleton array!`);
	}

	return input[0];
};

export const getNonNullValue = <T>(input: T | null): T => {
	if (input === null || input === undefined) {
		throw new Error(`${input} is null!`);
	}

	return input;
};
