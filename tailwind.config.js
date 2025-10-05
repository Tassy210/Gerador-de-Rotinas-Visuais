/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './rotinas/templates/**/*.{html,js}', // Caminho corrigido
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}