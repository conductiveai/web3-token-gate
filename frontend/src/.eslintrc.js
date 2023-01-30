// module.exports = {
//     rules: {
//       "no-console": "off",
//       "no-warning-comments": "off"
//     }
//   }
  

module.exports = {
  // plugins: ["vue"],
  // extends: [
  //   // add more generic rulesets here, such as:
  //   'eslint:recommended',
  //   'plugin:vue/vue3-recommended',
  // ],
  rules: {
    // override/add rules settings here, such as:
        "quotes": [ 1, "single", { "allowTemplateLiterals": true }],
        "no-undef": [ "warn" ],
        "semi": ["warn", "always"],
        "vue/script-indent": ["error", 2, { "baseIndent": 1 , "switchCase": 0, "ignores": [] }],
        "no-use-before-define":"warn",
        "vue/order-in-components": ["error", {"order": ["el","name","key","parent","functional",["delimiters", "comments"],["components", "directives", "filters"],"extends","mixins",["provide", "inject"],"ROUTER_GUARDS","layout","middleware","validate","scrollToTop","transition","loading","inheritAttrs","model",["props", "propsData"],"emits","setup","asyncData","data","fetch","head","computed","watch","watchQuery","LIFECYCLE_HOOKS","methods",["template", "render"],"renderError"]}],
        "no-console":"warn",
        "vue/match-component-file-name": ["error", {  "extensions": ["js"],  "shouldMatchCase": false}],
        "camelcase": [ "off" ],
        "no-confusing-arrow":"warn",
        "object-curly-spacing": [ "warn", "always" ],
        "brace-style":"warn",
        "eqeqeq":["warn","smart"]
  }
}