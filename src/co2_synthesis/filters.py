from collections import defaultdict
import numpy as np
from . import cfg


def create_filters(products:list[dict]) -> dict:
    filter = defaultdict(lambda: defaultdict(list))

    for p in products:
        filter['Data Type']['options'].append(p['data-category'])
        attrs = p['card-attribute']
        for attr in attrs:
            key = attr['label']
            value = split_strip(attr['value'])
            filter[key]['options'].extend(value)

    filter = defeaultdict_to_dict(filter)
    filter = {k: v for k, v in filter.items() if k in cfg.DATA_FILTERS}

    for key in filter:
        # first remove duplicates and empty strings
        filter[key]['options'] = sorted([k for k in set(filter[key]['options']) if k])
        filter[key]['type'] = 'multi-select'
        
    return defeaultdict_to_dict(filter)


def split_strip(val):
    val = str(val)
    vals = val.split(',')
    return [v.strip() for v in vals]


def is_date_range(val):
    return get_date_ranges(val) is not None

    
def get_date_ranges(val):
    import re
    pattern = r'^\s*(\d{4})\s*[-:]\s*(\d{4})\s*$'
    match = re.match(pattern, val)
    if match:
        start, end = [int(f) for f in match.groups()]
        return (start, end)
    return None


def defeaultdict_to_dict(d):
    if isinstance(d, defaultdict):
        d = {k: defeaultdict_to_dict(v) for k, v in d.items()}
    return d