/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/styles/**/*.css',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      transitionProperty: {
        'height': 'height',
        'spacing': 'margin, padding',
      },
    },
  },
  safelist: [
    // Layout classes
    {
      pattern: /^(h|w)-([0-9]+|full|screen|auto)/,
      variants: ['sm', 'md', 'lg'],
    },
    {
      pattern: /^(bg|text|border)-(.*)$/,
      variants: ['hover', 'dark', 'dark:hover'],
    },
    {
      pattern: /^(grid-cols|gap)-([0-9]+)/,
      variants: ['sm', 'md', 'lg'],
    },
    // Animation and transition classes
    'animate-pulse-slow',
    'transition-all',
    'transition-colors',
    'transition-opacity',
    'duration-200',
    'duration-300',
    // Specific component classes
    'sidebar-icon',
    'sidebar-tooltip',
  ],
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
