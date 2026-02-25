# Web page for Ocean CO2 Products

*from publication by [Jiang et al. (2026)](https://doi.org/10.5194/essd-18-1405-2026)*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18384592.svg)](https://doi.org/10.5281/zenodo.18384592)

This repository creates a static web page of different data products with a filter functionality. 
It is designed to be as low-maintenance as possible, and thus, the data lives in a Google Sheet document.
The Google Sheet is populated by a Google Form. 
Cards have a front and back side with an image, summary, and attributes on the front, and details, citation, and data access on the back. 

## Update the web page

Go to the [Actions Page](https://github.com/OceanCO2/co2-products/actions/workflows/manual-build.yaml) and click "Run Workflow" (only visible to repo members). 

## Configuration
### 1. Set up the repository
1. Fork this repository to your own GitHub account.
2. Clone the forked repository to your local machine.
3. Install `uv` on your machine (https://docs.astral.sh/uv/getting-started/installation/)
4. Install a virtual environment with `uv sync`

### 1. Create a Google Sheet
The Google Sheet must have some columns that match with the structure of the HTML template and Python code that generates the web page. The names must match exactly (case sensitive). There are some special cases (attributes, details) where columns can be repeated, to allow for multiple attributes or detail sections.  
**card-attributes** are used for filtering product cards. These three columns (icon, label, value) can be repeated as an block with different values to indicate different attributes. It is critical that you keep the three columns that belong together, adjacent to each other.  
**card-details** are similar to attributes, but are only shown on the back of the card and contain more text. You can repeat the two columns (title, content) as a block to add multiple detail sections. The back of the card scrolls if there is too much content to fit.
| **Card Face**     |     | **Field**                 | **Description**                                                         |
|-------------------|-----|:--------------------------|-------------------------------------------------------------------------|
| front + back      |     | `card-title`              | Title of the card. Truncated on front, but shown in full on the back.   |
| front + back      |     | `card-subheading`         | Subheading of the card                                                  |
| front             |     | `card-image`              | URL of the card image (downloaded, and resized if too large)            |
| front             |     | `card-summary`            | Message below the image on the front of the card                        |
| front             |   * | `card-attribute.icon`     | Font Awesome icon (e.g., `fa-solid fa-database`)                        |
| front             |   * | `card-attribute.label`    | Category label for the attribute                                        |
| front             |   * | `card-attribute.value`    | Value for the attribute. Comma separate multiple attributes for one label |
| back              |     | `card-citation`           | Citation shown on the back of the card (e.g., Author et al. (2025))     |
| back              |     | `card-citation-link`      | DOI or link to the paper                                                |
| back              |     | `card-data-access`        | URL to the landing page for data download                               |
| back              |   * | `card-detail.title`       | Title of the detail section                                             |
| back              |   * | `card-detail.content`     | Content of the detail section (up to 300 words)                         |

*Note on images:* Images are downloaded by the Python script and resized if they exceed the maximum size defined in the configuration file (default is 0.3 MB). If the website blocks an image from being loaded, the original image URL will be used instead, but this may slow down the page load time. Recommended image aspect ratio is roughly w3 x h2.

### 2. Populate the Google Sheet with Forms
I recommend that you create a Google Form that feeds into the Google Sheet. You can use data validation in the Form to restrict inputs to certain values (e.g., for card-attribute labels). This will ensure consistency across entries. You can then reference values from the Form Sheet tab to the web-formatted Sheet tab.
To preserve the order of the entries in the Google Form sheet, I use an index column in the web-formatted Sheet. Further, the first row of the web-formatted sheet contains the name of the column from the Google Form sheet, which minimizes the risk of getting columns mixed up. I use the following formula to pull data from the Form sheet into the web-formatted Sheet (example with cell `B3`): 
```excel
=HLOOKUP(B$1,google_form!$1:$159,$A3,FALSE)  
```
Where `B$1` is the name of the column in the Form sheet, `google_form!$1:$159` is the range of the Form sheet (adjust as needed), `$A3` is the index value for the current row, and `FALSE` indicates an exact match. When using this approach, make sure to set the `GOOGLE_SHEET_SKIPROWS` and `GOOGLE_SHEET_INDEXCOL` options in `config.py` accordingly (see step 4). Additionally, the index column must start in row 1 of the web-formatted sheet.

### 3. Set up Google Sheet Scripts
Create a Google Apps Script in the Google Sheet to add a custom menu item that triggers the GitHub API call to rebuild the website. You can use the provided `sheets_menu_github.js` script as a starting point. This script adds a menu item called "GitHub tools" with a button "Build website" that calls the `callGithubApi` function when clicked. This triggers the GitHub Actions workflow (`./.github/workflows/process-sheet-update.yaml`). You will need to have a GitHub Personal Access Token (PAT) with appropriate permissions (read/write content) to trigger the workflow. The token is entered in the Google Apps Script project properties as `GITHUB_TOKEN`. 

### 4. Update configuration in `config.py`
Create a `.env` file that contains the google sheet ID and tab ID. Any values in `config` can be entered in the `.env` file which will override the default values in the `config.py` file. Here's a description of the main configuration options:

- `GOOGLE_SHEET_ID`: The ID of the Google Sheet containing the data products. Only used for local builds.
- `GOOGLE_TAB_ID`: The ID of the specific tab in the Google Sheet to read. Only used for local builds.
- `GOOGLE_SHEET_SKIPROWS`: Number of rows to skip in the web-formatted Google Sheet. The column headers must be in the first row after the skipped rows.
- `GOOGLE_SHEET_INDEXCOL`: The index column number (0-based) in the web-formatted Google Sheet that contains the index values for each row.
- `SUBMISSION_FORM`: URL to the Google Form for data submission - will be linked on the web page.
- `GITHUB_REPO`: The GitHub repository URL where the website is hosted - will be linked on the web page.
- `WEBSITE_TITLE`: Title of the web page.
- `WEBSITE_DESCRIPTION`: Subtitle or description of the web page.
- `WEBSITE_IMAGE_MB`: Maximum size of images to be saved locally for the web page (in MB).
- `WEBSITE_COLOR`: Color theme for the website (hex code) - used in Header, footer, and links. 
- `DATA_FILTERS`: Tuple of card-attribute labels to be used as filters on the web page, in the order they should appear.

### 5. Run the script to generate the web page locally
To develop locally, you need to first set up the `.env` file with the Google Sheet ID and Tab ID (assuming comment access with link). The you can run `uv run co2-synthesis`. 

### 6. Build using GitHub Actions
Once you have set up the Google Sheet scripts and GitHub Actions workflows, you can trigger a rebuild of the web page directly from the Google Sheet using the custom menu item. Alternatively, you can trigger the workflow manually from the GitHub Actions tab in your repository.


## Repository structure

- `/src/`: contains the source code for generating the web page
  - `/src/co2_synthesis/`: main package
    - `generate_page.py`: main script to generate the web page  
    - `google_sheet.py`: module to read data from the Google Sheet
    - `filters.py`: module to handle filter logic
    - `config.py`: configuration file for the web page
    - `images.py`: module to handle image downloading and resizing
    - `cli.py`: command-line interface for running the script
  - `google_scripts/`:
    - `README.md`: instructions for setting up the Google Sheets script
    - `sheets_functions.js`: additional Google Sheets functions (check image size, validate URL, etc.)
    - `github_trigger.js`: Google Apps Script to trigger GitHub Actions workflow
    - `sheets_menu_github.js`: Google Apps Script to add custom menu in Google Sheets with GitHub build trigger
- `/static/`: contains static files such as CSS and JavaScript
  - `/templates/`: contains the Jinja2 templates for the web page
    - `template.html`: main HTML template for the web page
    - `data-card.html`: HTML template for individual product cards
    - `sidebar.html`: HTML template for the filter sidebar
  - `styles.css`: CSS file for styling the web page (also run through Jinja2 for config variables)
  - `scripts.js`: JavaScript file for handling filter interactions
- `.github/workflows/`: contains GitHub Actions workflows
  - `process-sheet-update.yaml`: Triggered by Google Sheets script to rebuild the web page
  - `manual-build.yaml`: Manual trigger to rebuild the web page (need to provide sheet ID and tab ID)
  - `google-sheet-build.yaml`: triggered by menu button in Google Sheets to rebuild the web page
- `/output/`: contains the generated web page files
  - `index.html`: the main HTML file for the web page
  - `styles.css`: the CSS file for the web page
  - `scripts.js`: the JavaScript file for the web page

