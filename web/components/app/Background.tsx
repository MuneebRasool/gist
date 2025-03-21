import React from 'react';

export const Background = () => {
	return (
		<div
			className='pointer-events-none fixed inset-0 -z-10 bg-cover bg-center bg-no-repeat'
			style={{
				backgroundImage: 'url(/background.svg)',
				opacity: 0.8, // Adjust opacity as needed
			}}
			aria-hidden='true'
		/>
	);
};
