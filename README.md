# Creates web page for publication by Jiang et al. (2025)

Creates a static web page of information about different ocean CO2 products. 
The web page is populated from a Google Sheet document. 
Email Luke Gregor ([luke.gregor@sdsc.ethz.ch](mailto:luke.gregor@sdsc.ethz.ch)), or Liqing Jiang ([lqjiang@umd.edu](mailto:lqjiang@umd.edu)) for the Google Sheets link.


## Usage
Navigate to https://oceanco2.github.io/co2-products/ to access the website. 

To land on a page with some filters already applied, you can use the following approach: https://oceanco2.github.io/co2-products/?filter-name=filter%20value.  
Here, filter-name is `Data Type` for example (no spaces and not case sensitive), and filter value would be `Surface data-derived` (case sensitive).  
Applying the approach above, the link would be https://oceanco2.github.io/co2-products/?data-type=Surface%20data-derived. 


## Google Sheet structure

The Google Sheet has one sheet designed for data providers to fill out. Here, we've made things as easy as possible by providing categories, and checks on the htmls. You are also required to provide and image. This should be an html link to an image that is roughly w250 x h170 pixels. Using larger images will slow loading down once everyone has added their images, so use a thumbnail sized image. 

## HTML structure
The HTML structure is created using Jinja2 templates. The main template is `template.html`, which contains the overall structure of the web page. The *product* table is generated dynamically based on the data from the Google Sheet.
Each product is a \<div> element with class "product-card". These can be filtered using JavaScript based on the selected criteria. 

Styling of the web page is done using CSS, which is included in the `styles.css` file. The layout is responsive and adapts to different screen sizes.

The filters will be located in a sidebar on the left side of the page, while the product cards will be displayed in a grid layout on the right side. 

### Product card structure
This can be found in the `static/templates/data-card.html` file. This will be populated from the Google Sheet data (see table example above). 


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
