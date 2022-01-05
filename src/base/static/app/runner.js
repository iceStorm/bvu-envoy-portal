const cssModulesPlugin = require('esbuild-css-modules-plugin');

require('esbuild')
  .build({
    logLevel: 'info',
    entryPoints: [
      'src/js/base.js',
    ],
    bundle: true,
    outfile: 'dist/js/base.js',
    // minify: true,
    format: 'esm',
    plugins: [
      cssModulesPlugin(),
    ],
    watch: true,
  })
  .catch(() => process.exit(1));
