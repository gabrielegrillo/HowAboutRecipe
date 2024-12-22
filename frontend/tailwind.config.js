/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        'personal-palette-light-orange': '#FFDAB9',
        'personal-palette-apricot': '#FBC4AB',
        'personal-palette-melon': '#F8AD9D',
        'personal-palette-coral-pink': '#F4978E',
        'personal-palette-light-coral': '#F08080',
        'personal-palette-blush': '#C86680',
        'personal-palette-magenta-haze': '#A04B7F',
        'personal-palette-english-violet': '#48304D',
      }
    },
  },
  plugins: [],
}
