import { format } from 'date-fns';

export function prettyDate(date) {
  if (!date) {
    return null;
  }

  return format(date, 'MMMM d, yyyy');
}