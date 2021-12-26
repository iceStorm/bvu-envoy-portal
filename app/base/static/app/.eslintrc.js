module.exports = {
  env: {
    browser: true,
    commonjs: true,
    es2021: true,
  },
  extends: [
    'airbnb-base',
  ],
  parserOptions: {
    ecmaVersion: 13,
  },
  rules: {
  },
  ignorePatterns: [
    './dist/**/*.js',
    './assets/**/*.js',
  ], // <<< ignore all files in test folder
};
