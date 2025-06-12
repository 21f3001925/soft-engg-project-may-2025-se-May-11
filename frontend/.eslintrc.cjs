module.exports = {
  env: {
    browser: true,
    es2022: true,
    node: true
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
    'plugin:vuejs-accessibility/recommended',
    'plugin:prettier/recommended'
  ],
  plugins: ['vue', 'vuejs-accessibility'],
  rules: {
    // accessibility rules
    'vuejs-accessibility/label-has-for': 'warn',
    'vuejs-accessibility/click-events-have-key-events': 'warn'
  }
};
  