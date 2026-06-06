/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cream: '#F5F0E8',
        wine: '#4A2C39',
        malva: '#C4A4A4',
        rose: '#D4A5A5',
      }
    }
  },
  plugins: [],
}