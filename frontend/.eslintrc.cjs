module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
  },
  parser: 'vue-eslint-parser',
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false,
    ecmaVersion: 12,
    sourceType: 'module',
  },
  extends: [
    'plugin:vue/vue3-recommended',
    'eslint:recommended',
    'plugin:prettier/recommended'
  ],
  rules: {
    'vue/multi-word-component-names': 'off',
    // add your other custom rules here if needed
  },
};
