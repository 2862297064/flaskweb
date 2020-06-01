
// For authoring Nightwatch tests, see
// http://nightwatchjs.org/guide#usage

module.exports = {
  'default e2e tests': function (browser) {
    const devServer = browser.globals.devServerURL
    browser
      .url('http://localhost:8080')
      .waitForElementVisible('#app', 5000)
      .end()
  }
}
