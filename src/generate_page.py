import os
import shutil
import re
import html
from jinja2 import Environment, FileSystemLoader
from google_sheet import get_sheet_data
from filters import generate_filters, split_multi_values

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

if __name__ == '__main__':
    main()
