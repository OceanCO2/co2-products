# Creates web page for publication by Jiang et al. (2025)

Creates a static web page of information about different ocean CO2 products. 
The web page is populated from a Google Sheet document. 

On the website, all products are listed together (inspired by CMEMS). One can filter the product by different criteria, such as whether the product covers the open ocean or coastal ocean, the spatial and temporal resolution, etc. The google sheet contains the information about which column is filterable and which is not.

## Usage
To activate one of the filters by default, add the following to the URL: `?data-type=Surface data-derived`. In a full link, this would look like:
[/index.html?data-type=Surface%20data-derived](./output/index.html?data-type=Surface%20data-derived)



## Google Sheet structure

The table below shows information about the Google Sheet structure. The first row contains information about the filter type - if no type is given, then it is not filterable. The second row contains the column headers. The subsequent rows contain the actual data for each product. When fully populated, the table will contain > 80 products.


## HTML structure
The HTML structure is created using Jinja2 templates. The main template is `template.html`, which contains the overall structure of the web page. The *product* table is generated dynamically based on the data from the Google Sheet.
Each product is a \<div> element with class "product-card". These can be filtered using JavaScript based on the selected criteria. 


Styling of the web page is done using CSS, which is included in the `styles.css` file. The layout is responsive and adapts to different screen sizes.

The filters will be located in a sidebar on the left side of the page, while the product cards will be displayed in a grid layout on the right side. 

### Product card structure
This can be found in the `static/templates/data-card.html` file. This will be populated from the Google Sheet data (see table example above). 


### Details about filter types

- **Checkbox filter**: Shows a list of options that are checkboxes - users can select multiple options. Products that match any of the selected options will be displayed.
- **Number range filter**: Allows users to select a range of numbers. Products that fall within the selected range will be displayed.


## Repository structure

- `/src/`: contains the source code for generating the web page
  - `generate_page.py`: main script to generate the web page  
  - `google_sheet.py`: module to read data from the Google Sheet
  - `filters.py`: module to handle filter logic
- `/static/`: contains static files such as CSS and JavaScript
  - `/templates/`: contains the Jinja2 templates for the web page
  - `styles.css`: CSS file for styling the web page
  - `scripts.js`: JavaScript file for handling filter interactions
- `/output/`: contains the generated web page files
  - `index2.html`: the main HTML file for the web page