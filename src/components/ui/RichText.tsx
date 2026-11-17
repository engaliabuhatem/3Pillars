import { cn } from '@/lib/utils';

/**
 * HTML from the CMS editor. It is sanitised on save by the backend
 * (apps/core/fields.py, an allow-list of tags with no attributes besides
 * links), which is what makes rendering it here safe.
 */
export function RichText({ html, className }: { html: string; className?: string }) {
  if (!html) return null;
  return (
    <div
      className={cn(
        'max-w-prose text-body',
        '[&_p]:mb-5 [&_p:last-child]:mb-0 [&_h2]:mt-10 [&_h2]:mb-4 [&_h2]:text-h3 [&_h2]:font-semibold',
        '[&_h3]:mt-8 [&_h3]:mb-3 [&_h3]:text-xl [&_h3]:font-semibold',
        '[&_ul]:mb-5 [&_ul]:list-disc [&_ul]:ps-6 [&_ol]:mb-5 [&_ol]:list-decimal [&_ol]:ps-6 [&_li]:mb-2',
        '[&_a]:text-blue [&_a]:underline [&_a]:underline-offset-4 hover:[&_a]:no-underline',
        'on-navy:[&_a]:text-blue-200',
        '[&_blockquote]:my-8 [&_blockquote]:border-s-2 [&_blockquote]:border-blue [&_blockquote]:ps-6 [&_blockquote]:text-lead',
        className,
      )}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
