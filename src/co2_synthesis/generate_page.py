import os
import shutil
import re
import html
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from . google_sheet import get_sheet_data


def main():
    sheet_id = '1rg9yf1IxSr6fI7UvbrbMqrywRgIPS240uaphIplUXBo'
    filter_types, shown_on_card, headers, data = get_sheet_data(sheet_id)
    
    filters = generate_filters(filter_types, headers, data)
    
    # Prepare products
    products = []
    for row in data:
        product = dict(zip(headers, row))
        if product.get('Image'):
            match = re.search(r'href="([^"]*)"', product['Image'])
            if match:
                product['Image'] = match.group(1)
        data_attrs = {}
        for h in headers:
            if h in filters:
                attr_name = 'data-' + h.lower().replace(' ', '-')
                filter_config = filters[h]
                raw_value = product.get(h, '')
                attr_value = raw_value.strip()
                if filter_config['type'] in ('checkbox', 'radio'):
                    tokens = split_multi_values(raw_value)
                    attr_value = '||'.join(tokens)
                elif filter_config['type'] == 'period':
                    attr_value = raw_value.strip()
                attr_value = html.escape(attr_value, quote=True)
                data_attrs[attr_name] = attr_value
        product['data_attrs'] = ' '.join(f'{key}="{value}"' for key, value in data_attrs.items())
        products.append(product)
    
    # Setup Jinja2
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('template.html')
    
    # Render
    output = template.render(products=products, filters=filters, shown_on_card=shown_on_card, headers=headers)
    
    # Write to output
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write(output)
    
    # Copy static files
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
    for file in ['styles.css', 'scripts.js']:
        shutil.copy(os.path.join(static_dir, file), output_dir)


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

    return data


if __name__ == '__main__':
    main()
