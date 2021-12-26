module.exports = {
  // syntax: 'postcss-scss',
  // parser: 'postcss-scss',
  plugins: [
    // require('postcss-simple-vars'),
    require('postcss-import'),
    require('postcss-nested-ancestors'),
    require('postcss-nested'),
    require('postcss-each'),
    require('postcss-for'),
    require('tailwindcss'),
    require('autoprefixer'),
  ]
}
