# Creates web page for publication by Jiang et al. (2025)

Creates a static web page of information about different ocean CO2 products. 
The web page is populated from a Google Sheet document. 

On the website, all products are listed together (inspired by CMEMS). One can filter the product by different criteria, such as whether the product covers the open ocean or coastal ocean, the spatial and temporal resolution, etc. The google sheet contains the information about which column is filterable and which is not.


## Google Sheet structure

The table below shows information about the Google Sheet structure. The first row contains information about the filter type - if no type is given, then it is not filterable. The second row contains the column headers. The subsequent rows contain the actual data for each product. When fully populated, the table will contain > 80 products.

| Filter type | checkbox | radio | checkbox | checkbox | slider |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Shown on card | subheader | back | front | front | back | header | back | back | back | back | no |
|  | Product type | Area | Spatial resolution | Temporal resolution | Years | Product name | Methodology | Highlights | Reference | Data access | Image |
|  | Data synthesis products | Both | 0.25 | monthly | climatology | MPI-ULB-SOM-FFN | ... | ... | Landschützer et al. (2020) | Link to data | https://www.ncei.noaa.gov/access/ocean-carbon-acidification-data-system/oceans/Figure1_MPI-ULB-SOM_FFN.jpg |
|  | Data synthesis products | Both | 0.25 | monthly | 1982 - 2024 | OceanSODA-ETHZv2 | A neural network approach | ... | Gregor et al. (2024) | https://zenodo.org/records/11206366 | https://data.up.ethz.ch/shared/ESA-OHOA/OceanSODA_ETHZ_HR-v2023.prerelease-flux/_img/gantt_chart.png |

Here is the link to the Google Sheet:  
https://docs.google.com/spreadsheets/d/1rg9yf1IxSr6fI7UvbrbMqrywRgIPS240uaphIplUXBo/edit?usp=sharing


## HTML structure
The HTML structure is created using Jinja2 templates. The main template is `template.html`, which contains the overall structure of the web page. The *product* table is generated dynamically based on the data from the Google Sheet.
Each product is a \<div> element with class "product-card". These can be filtered using JavaScript based on the selected criteria. 


Styling of the web page is done using CSS, which is included in the `styles.css` file. The layout is responsive and adapts to different screen sizes.

The filters will be located in a sidebar on the left side of the page, while the product cards will be displayed in a grid layout on the right side. 

### Details about "product-card"
Each product card contains the following elements:
- Product name: displayed as a heading
- Image: a thumbnail image representing the product - if no image is provided, show the back of the card instead
- Methodology: a brief description of the methodology used for the product
- Clicking the product card will display more detailed information about the product - the card will turn over to show the back side with more details such as highlights, reference, and data access link. The header will still be the same when turned over. Users can click again to turn the card back to the front side. Links here will take the user to the data source. 

### Details about filter types

- **Checkbox filter**: Shows a list of options that are checkboxes - users can select multiple options. Products that match any of the selected options will be displayed.
- **Radio filter**: Shows a list of options that are radio buttons - users can select only one option. Products that match the selected option will be displayed.
- **Slider filter**: Column may contain A - B, where A is valid min, and B is valid max for that product . Alternatively, the product may have a string in the slider column - if this is the case, then add a radio box selector to that column category. If a product's range overlaps with the selected range, it will be displayed.
- **No filter**: Columns without a filter type are displayed as-is in the product cards and are not filterable.


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
  - `index.html`: the main HTML file for the web page