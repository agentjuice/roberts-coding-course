/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['Bangers', 'cursive'],
        body: ['Nunito', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        neon: {
          cyan: '#00ffcc',
          pink: '#ff00ff',
          yellow: '#ffcc00',
          red: '#ff4444',
          green: '#39ff14',
        },
        dark: {
          900: '#0b0b13',
          800: '#111827',
          700: '#1a1a2e',
        }
      }
    },
  },
  plugins: [],
}
