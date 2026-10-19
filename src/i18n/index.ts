import { en } from './en';
import { hu } from './hu';

export type Locale = 'en' | 'hu';
export type Translation = typeof en;

export const translations: Record<Locale, Translation> = { en, hu };

export function getTranslation(lang: Locale): Translation {
  return translations[lang] ?? en;
}

export const locales: Locale[] = ['en', 'hu'];
export const defaultLocale: Locale = 'en';

/** Fills Android-style placeholders (%d, %s, %1$d …) copied from the app's strings. */
export function fmt(template: string, ...args: (string | number)[]): string {
  let next = 0;
  return template.replace(/%(?:(\d+)\$)?[ds]/g, (_, pos) => String(args[pos ? Number(pos) - 1 : next++]));
}

/** "Day 2" or "Days 2-3" for a phase spanning [startHour, endHour). */
export function dayLabel(t: Translation, startHour: number, endHour: number): string {
  const startDay = Math.floor(startHour / 24) + 1;
  const endDay = Math.floor((endHour - 1) / 24) + 1;
  return startDay === endDay ? fmt(t.phases.daySingle, startDay) : fmt(t.phases.dayRange, startDay, endDay);
}
