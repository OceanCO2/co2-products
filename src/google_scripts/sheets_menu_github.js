function makeMenuItem() {
  SpreadsheetApp.getUi()
      .createMenu('GitHub tools') // Name of the main menu
      .addItem('Update Ocean CO2 products website', 'callGithubApi') // Button name and function name
      .addToUi();
}
