/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/styles/**/*.css',
  ],
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
      height: {
        '12': '3rem',
      },
      width: {
        '12': '3rem',
      },
    },
  },
  safelist: [
    'h-12',
    'w-12',
  ],
  plugins: [
    // @ts-ignore
    require('@tailwindcss/forms'),
    // @ts-ignore
    require('@tailwindcss/typography'),
  ],
}