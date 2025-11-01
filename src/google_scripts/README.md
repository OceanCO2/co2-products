# ⚙️ Setup and Configuration

Automatic Menu Initialization (Google Apps Script Trigger)This project uses a Google Apps Script trigger named google_sheet_trigger to ensure that custom functionalities are available immediately upon opening the spreadsheet.

| Setting | Value | Description |
|---|---|---|
| Function to run | makeMenuItem | The Apps Script function responsible for creating the custom menu items (e.g., "Run Report", "Update Data") in the spreadsheet toolbar. |
| Event Source | From spreadsheet | The trigger is tied directly to the associated Google Sheet. |
| Event Type | On open | This trigger fires automatically every time a user opens the spreadsheet, guaranteeing the custom menu is always loaded. |
| Deployment | Head | Refers to the current, latest version of the Apps Script code. |

## Why is this necessary?
The makeMenuItem function must run before a user attempts to use any custom tool. By setting the trigger to On open, we ensure the custom menu items are visible and functional in the sheet's toolbar immediately, providing a seamless user experience.