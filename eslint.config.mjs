import { defineConfig, globalIgnores } from 'eslint/config';
import nextVitals from 'eslint-config-next/core-web-vitals';
import nextTypescript from 'eslint-config-next/typescript';

export default defineConfig([
  ...nextVitals,
  ...nextTypescript,
  {
    rules: {
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
      // RTL is mirrored with logical properties only (brief §3).
      'no-restricted-syntax': [
        'error',
        {
          selector: 'Literal[value=/(^|\s)-?(ml|mr|pl|pr|left|right|rounded-l|rounded-r|border-l|border-r|text-left|text-right)-/]',
          message: 'Use logical utilities (ms-/me-/ps-/pe-/start-/end-/text-start) so RTL mirrors.',
        },
      ],
    },
  },
  globalIgnores(['.next/**', 'out/**', 'next-env.d.ts', 'backend/**', 'playwright-report/**', 'test-results/**']),
]);
