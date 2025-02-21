import { FolderKanban } from 'lucide-react';
import React from 'react';

const Page = () => {
	return (
		<div className='mx-auto flex h-full max-w-6xl flex-col gap-5 py-10 sm:px-5'>
			<div className='mb-8 flex items-center justify-between gap-4'>
				<div className='space-y-2'>
					<div className='flex items-center space-x-2'>
						<FolderKanban className='h-6 w-6 text-primary' />
						<h1 className='text-xl font-semibold'>Tasks</h1>
					</div>
					<p className='text-muted-foreground'>Manage all your Tasks</p>
				</div>
			</div>
			{/* Content */}
		</div>
	);
};

export default Page;
