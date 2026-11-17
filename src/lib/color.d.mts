export function hexToRgb(hex: string): [number, number, number];
export function rgbToHex(rgb: number[]): string;
export function hexToOklch(hex: string): { l: number; c: number; h: number };
export function oklchToHex(color: { l: number; c: number; h: number }): string;
export function luminance(hex: string): number;
export function contrast(a: string, b: string): number;
