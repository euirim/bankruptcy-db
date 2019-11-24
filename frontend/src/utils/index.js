import { format } from 'date-fns';

export function prettyDate(date) {
  if (!date) {
    return null;
  }

  return format(new Date(date), 'MMMM d, yyyy');
}