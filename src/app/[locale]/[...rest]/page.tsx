import { notFound } from 'next/navigation';

/** Unmatched paths under a locale get the localised 404 inside the site chrome. */
export default function CatchAll() {
  notFound();
}
