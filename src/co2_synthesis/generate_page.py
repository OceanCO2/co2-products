import pathlib
import shutil
import numpy as np
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from .google_sheet import get_sheet_data, download_sheet_as_excel
from .config import cfg
from .filters import create_filters
from loguru import logger


def generate_page_main(google_sheet_url: str):
    static_dir = cfg.ROOT / 'static'
    template_dir = static_dir / 'templates'

    output_dir = cfg.ROOT / 'docs'  # GitHub Pages serves from /docs
    output_dir.mkdir(exist_ok=True)  # create if doesn't exist

    logger.debug(f"Fetching data from Google Sheet: {google_sheet_url}")
    df = get_sheet_data(google_sheet_url, reader='pandas')
    logger.debug(f"Retrieved {len(df)} rows from Google Sheet.\n{df.T}")

    df = get_valid_products_only(df)
    products = list(df.apply(process_product_row, axis=1))
    filters = create_filters(products)
    
    jinja2_env = Environment(loader=FileSystemLoader(template_dir))
    template = jinja2_env.get_template('template.html')

    html = template.render(products=products, filters=filters, cfg=cfg)

    with open(output_dir / 'index.html', 'w') as f:
        f.write(html)

    download_sheet_as_excel(google_sheet_url, output_dir / 'data.xlsx')
    logger.info("Downloaded Google Sheet as Excel file for backup.")

    # Copy static files
    for file in ['styles.css', 'scripts.js']:
        shutil.copy(static_dir / file, output_dir / file)


def get_valid_products_only(products: pd.DataFrame) -> pd.DataFrame:
    """
    Check for incomplete product entries missing required fields.
    Logs a warning for any incomplete products found.
    Returns a DataFrame with only complete products.
    """
    df_no_incomplete_products = products.dropna(subset='card-title').replace({np.nan: ""})
    # show difference between incomplete and complete cards
    idx_incomplete = products.index.difference(df_no_incomplete_products.index)
    if len(idx_incomplete) > 0:
        logger.warning(
            f"Dropping {len(idx_incomplete)} incomplete products (missing card-title):\n"
            f"{products.loc[idx_incomplete].T}")
        
    return df_no_incomplete_products
    

def process_product_row(product_row: pd.Series) -> dict:
    """
    Process a product row from the DataFrame into a nested dictionary.
    that matches the structure required in the data-card.html template.
    """
    
    ser:pd.Series = product_row

    data = {}
    for key in ser.index:
        if '.' not in key:  # Simple key-value pair
            data[key] = ser[key]
        else:  # Nested structure (only 1 level deep)
            splits = key.split('.')
            if len(splits) == 2:  # the first nested key-value item
                (main_key, sub_key), index = splits, 0
            elif len(splits) == 3:  # subsequent nested key-value items have .num suffix
                main_key, sub_key, index = splits
                index = int(index)
            # create a dataframe that can insert at the correct index
            if main_key not in data:
                data[main_key] = pd.DataFrame()
            # now, we can insert the value at the correct index
            data[main_key].loc[index, sub_key] = ser[key]
    # Convert any DataFrames to list of dicts
    for key in data:
        if isinstance(data[key], pd.DataFrame):
            data[key] = data[key].to_dict(orient='records')

    # Create data attributes for filtering
    data_attrs = {}
    data_attrs[f"data-data-type"] = data.get('data-category', '')
    for attr in data.get('card-attribute', []):
        if attr.get('value'):
            attr_name = f"data-{attr['label'].lower().replace(' ', '-')}"
            # handle multiple values for multi-select filters
            values = [v.strip() for v in str(attr['value']).split(',')]
            data_attrs[attr_name] = '||'.join(values)
    
    data['data-attrs'] = ' '.join([f'{k}="{v}"' for k, v in data_attrs.items()])

    return data

