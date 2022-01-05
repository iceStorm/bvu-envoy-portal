// const _ = require('lodash');
const tailpress = require('@jeffreyvr/tailwindcss-tailpress');
const colors = require('tailwindcss/colors');
const theme = require('./theme.json');

const themeColors = tailpress.colorMapper(tailpress.theme('settings.color.palette', theme));

module.exports = {
  // mode: 'jit',
  content: [
    '../../../*/*.html',
    '../../../**/*.html',
    './src/css/**/*.css',
    './src/js/**/*.js',
  ],
  safelist: [
    'bg-primary-dark',
  ],
  theme: {
    container: {
      padding: {
        DEFAULT: '1rem',
        sm: '2rem',
        lg: '0rem',
      },
    },
    extend: {
      colors: {
        ...themeColors,
        green: colors.emerald,
        yellow: colors.amber,
        purple: colors.violet,
        gray: colors.neutral,
        footer: '#313131',
      },
      borderWidth: {
        1.5: '1.5px',
      },
      height: {
        'fit-content': 'fit-content',
      },
      maxWidth: {
        '1/4': '25%',
        '1/2': '50%',
        '3/4': '75%',
        'mobile-search-box': '235px',
      },
      gridTemplateColumns: {
        'mega-menu': 'repeat(auto-fill, minmax(250px, 1fr))',
        footer: 'repeat(auto-fit, minmax(200px, 1fr))',
        'single-post-lg': '1.618fr 1fr',
        'single-post-sm': '1fr',
      },
    },
    screens: {
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: tailpress.theme('settings.layout.wideSize', theme),
    },
  },
  plugins: [
    tailpress.tailwind,
  ],
};
