import { z } from 'zod';

export const PostSchema = z.object({
	id: z.string().uuid(),
	title: z.string().min(5, 'Title must be at least 5 characters long'),
	content: z.string().min(20, 'Content must be at least 20 characters long'),
	authorId: z.string().uuid(),
});

export const CreatePostSchema = z.object({
	title: z.string().min(5, 'Title must be at least 5 characters long'),
	content: z.string().min(20, 'Content must be at least 20 characters long'),
});

export type Post = z.infer<typeof PostSchema>;
