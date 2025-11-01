/**
 * @OnlyCurrentDoc
 * This script triggers a GitHub Action.
 */

// --- 1. CONFIGURATION ---
// SET THESE VALUES
var GITHUB_OWNER = 'OceanCO2'; // Your GitHub username or organization
var GITHUB_REPO = 'co2-products'; // Your GitHub repository name
var GITHUB_EVENT_TYPE = 'google_sheet_updated'; // Must match your workflow 'types'
var SPREADSHEET_TAB_ID = 0; // Copied from the URL of the spreadsheet

// --- 5. API LOGIC ---

/**
 * Performs the actual API call to GitHub.
 * This is separated for clarity and modularity.
 */
function callGithubApi() {
  // Retrieve the GitHub Token from Script Properties for security.
  var GITHUB_TOKEN = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');

  if (!GITHUB_TOKEN) {
    Logger.log('ERROR: GITHUB_TOKEN script property is not set.');
    return; // Stop execution
  }

  // Set up the GitHub API endpoint
  var url = 'https://api.github.com/repos/' + GITHUB_OWNER + '/' + GITHUB_REPO + '/dispatches';

  // Create the payload to send to GitHub.
  var payload = {
    event_type: GITHUB_EVENT_TYPE,
    client_payload: {
      message: 'Triggered by Google Sheet edit',
      spreadsheet_id: SpreadsheetApp.getActiveSpreadsheet().getId(),
      spreadsheet_tab_id: SPREADSHEET_TAB_ID,
    }
  };

  // Set up the HTTP request options
  var options = {
    'method': 'post',
    'contentType': 'application/json',
    'headers': {
      'Authorization': 'token ' + GITHUB_TOKEN,
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'Google-Apps-Script' // GitHub API recommends setting a User-Agent
    },
    'payload': JSON.stringify(payload),
    'muteHttpExceptions': true // Prevents script from stopping on a bad request
  };

  // Make the external request
  var response = UrlFetchApp.fetch(url, options);
  var responseCode = response.getResponseCode();
  var responseBody = response.getContentText();

  if (responseCode === 204) {
    Logger.log('Success! GitHub repository_dispatch event triggered.');
  } else {
    Logger.log('Error triggering GitHub dispatch: ' + responseCode);
    Logger.log('Response: ' + responseBody);
  }
}
