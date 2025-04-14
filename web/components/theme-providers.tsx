'use client';

import * as React from 'react';
import { ThemeProvider as NextThemesProvider } from 'next-themes';

export function ThemeProvider({ children, ...props }: React.ComponentProps<typeof NextThemesProvider>) {
	return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}




// user must not be able to visit /login if they are already logged in
//user must not be able to visit welcome page if onboarding is completed
// user must not be able to visit onboarding page if onboarding is completed