/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        zinc: {
          800: '#27272a',
          900: '#18181b',
        }
      }
    },
  },
  plugins: [],
}
