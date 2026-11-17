import Image from 'next/image';
import type { Client } from '@/lib/cms/types';

/**
 * Approved client and partner logos as a slow marquee. The list is rendered
 * twice for a seamless loop; the copy is hidden from assistive tech. It pauses
 * on hover and focus, and stands still under reduced motion.
 */
export function TrustStrip({ clients, label }: { clients: Client[]; label: string }) {
  const logos = clients.flatMap((c) => (c.logo ? [{ ...c, logo: c.logo }] : []));
  if (logos.length === 0) return null;

  const row = (hidden: boolean) => (
    <ul aria-hidden={hidden || undefined} className="flex shrink-0 items-center gap-16 pe-16">
      {logos.map((client) => (
        <li key={client.id} className="relative h-10 w-36 shrink-0 opacity-70 grayscale transition duration-base hover:opacity-100 hover:grayscale-0">
          <Image src={client.logo.src} alt={hidden ? '' : client.name} fill sizes="144px" className="object-contain" />
        </li>
      ))}
    </ul>
  );

  return (
    <div
      aria-label={label}
      role="region"
      className="group flex overflow-hidden [mask-image:linear-gradient(to_right,transparent,black_10%,black_90%,transparent)]"
    >
      <div className="flex animate-marquee group-focus-within:[animation-play-state:paused] group-hover:[animation-play-state:paused] motion-reduce:animate-none rtl:[animation-direction:reverse]">
        {row(false)}
        {row(true)}
      </div>
    </div>
  );
}
