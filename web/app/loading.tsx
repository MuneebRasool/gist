'use client';

import React from 'react';

interface LoadingProps {
	text?: string;
}

const Loading = ({ text = 'Gist is working on building your view...' }: LoadingProps) => {
	return (
		<div className='fixed inset-0 z-50 flex items-center justify-center'>
			<div className='flex flex-col items-center justify-center space-y-8'>
				<div className='relative'>
					<div className='h-12 w-12 animate-spin rounded-full border-4 border-[#A5B7C8]/30 border-t-[#A5B7C8]' />
				</div>
				<p className='text-lg font-medium text-gray-600'>{text}</p>
			</div>
		</div>
	);
};

export default Loading;
