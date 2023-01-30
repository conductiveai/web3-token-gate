
//add fallback resolve.fallback: { "stream": false }

module.exports = {
  "presets": [
    ["@vue/app", {
    "polyfills": [
      "es.promise",
      "es.symbol"
    ]
  }]
  ]
}

