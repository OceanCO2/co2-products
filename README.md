# Creates web page for publication by Jiang et al. (2025)

Creates a static web page of information about different ocean CO2 products. 
The web page is populated from a Google Sheet document. 

On the website, all products are listed together (inspired by CMEMS). One can filter the product by different criteria, such as whether the product covers the open ocean or coastal ocean, the spatial and temporal resolution, etc. The google sheet contains the information about which column is filterable and which is not.


## Google Sheet structure

The table below shows information about the Google Sheet structure. The first row contains information about the filter type - if no type is given, then it is not filterable. The second row contains the column headers. The subsequent rows contain the actual data for each product. When fully populated, the table will contain > 80 products.

| data-category | card-title | card-subheading | card-image | card-attribute.icon | card-attribute.label | card-attribute.value | card-attribute.icon | card-attribute.label | card-attribute.value | card-attribute.icon | card-attribute.label | card-attribute.value | card-attribute.icon | card-attribute.label | card-attribute.value | card-summary | card-citation | card-citation-link | card-data-access | card-detail.title | card-detail.content | card-detail.title | card-detail.content |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Surface data-derived | OceanSODA-ETHZv1 | Gregor and Gruber (2020) | https://essd.copernicus.org/articles/13/777/2021/essd-13-777-2021-avatar-web.png | fa-solid fa-hourglass-start | Temporal resolution | monthly | fa-solid fa-ruler-horizontal | Spatial resolution | 1.0° | fa-solid fa-calendar-days | Period | 1982 - 2022 | fa-solid fa-globe | Spatial domains | Open Ocean, Surface | Full marine carbonate system | Gregor and Gruber (2020) | https://doi.org/10.5194/essd-13-777-2021 | https://doi.org/10.25921/m5wx-ja34 | Highlight |  | Method |  |
| Surface data-derived | OceanSODA-ETHZv2 | Gregor et al. (2024) | https://agupubs.onlinelibrary.wiley.com/cms/asset/7decc330-7468-429c-bae9-ac51b085be30/gbc21584-fig-0007-m.jpg | fa-solid fa-hourglass-start | Temporal resolution | 8-daily | fa-solid fa-ruler-horizontal | Spatial resolution | 0.25° | fa-solid fa-calendar-days | Period | 1982 - 2024 | fa-solid fa-globe | Spatial domains | Open Ocean, Surface | High resolution fluxes | Gregor et al. (2024) | https://doi.org/10.1029/2024GB008127 | https://zenodo.org/records/11206366 | Highlight |  | Method |  |
| Surface data-derived | ∆fCO2 and Flux Climatology | Fay et al. (2023) | https://essd.copernicus.org/articles/16/2123/2024/essd-16-2123-2024-avatar-web.png | fa-solid fa-hourglass-start | Temporal resolution | climatology, monthly | fa-solid fa-ruler-horizontal | Spatial resolution | 1.0° | fa-solid fa-calendar-days | Period |  | fa-solid fa-globe | Spatial domains | Open Ocean, Surface | Updated Takahashi climatology | Fay et al. (2023) | https://essd.copernicus.org/articles/16/2123/2024/ | https://doi.org/10.25921/295g-sn13 | Highlight | else | Method | something |
| Surface data-derived | VLIZ-SOMFFN | Landschützer et al. (2016) | https://agupubs.onlinelibrary.wiley.com/cms/asset/547d18a7-69b5-4e93-96b2-5e8371310b43/gbc20188-fig-0001-m.jpg | fa-solid fa-hourglass-start | Temporal resolution | monthly | fa-solid fa-ruler-horizontal | Spatial resolution | 1.0° | fa-solid fa-calendar-days | Period | 1982 - 2024 | fa-solid fa-globe | Spatial domains | Surface, Open Ocean | The OG | Landschützer et al. (2016) |  |  | Highlight |  | Method |  |
Here is the link to the Google Sheet:  
https://docs.google.com/spreadsheets/d/1rg9yf1IxSr6fI7UvbrbMqrywRgIPS240uaphIplUXBo/edit?usp=sharing


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