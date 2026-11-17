'use client';

import { createContext, useContext, type ReactNode } from 'react';
import type { Locale } from './config';
import { getDictionary } from './dictionaries';

const LocaleContext = createContext<Locale>('en');

export function LocaleProvider({ locale, children }: { locale: Locale; children: ReactNode }) {
  return <LocaleContext.Provider value={locale}>{children}</LocaleContext.Provider>;
}

export const useLocale = () => useContext(LocaleContext);

/** Dictionaries hold formatter functions, which cannot cross the server/client boundary as props. */
export const useDictionary = () => getDictionary(useLocale());
