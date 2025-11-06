function makeMenuItem() {
  SpreadsheetApp.getUi()
      .createMenu('GitHub tools') // Name of the main menu
      .addItem('Build website', 'callGithubApi') // Button name and function name
      .addToUi();
}
