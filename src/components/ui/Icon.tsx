import {
  Activity,
  Award,
  Briefcase,
  Building,
  Calculator,
  ChartGantt,
  CircleCheck,
  ClipboardCheck,
  Factory,
  Flag,
  FlagTriangleRight,
  Hammer,
  HardHat,
  Landmark,
  Layers,
  Map,
  Network,
  PencilRuler,
  Route,
  Scale,
  ShieldCheck,
  Signature,
  Target,
  TrendingUp,
  Users,
  Zap,
  type LucideIcon,
} from 'lucide-react';

/**
 * Icons editors can name in the admin ("Icon name from lucide.dev"). A fixed
 * map keeps the bundle to the icons actually offered; an unknown name renders
 * the neutral fallback instead of breaking the page.
 */
const ICONS: Record<string, LucideIcon> = {
  Activity,
  Award,
  Briefcase,
  Building,
  Calculator,
  ChartGantt,
  CircleCheck,
  ClipboardCheck,
  Factory,
  Flag,
  FlagTriangleRight,
  Hammer,
  HardHat,
  Landmark,
  Layers,
  Map,
  Network,
  PencilRuler,
  Route,
  Scale,
  ShieldCheck,
  Signature,
  Target,
  TrendingUp,
  Users,
  Zap,
};

export const ICON_NAMES = Object.keys(ICONS);

export function Icon({ name, className }: { name: string; className?: string }) {
  const Component = ICONS[name] ?? CircleCheck;
  return <Component aria-hidden className={className} strokeWidth={1.5} />;
}
