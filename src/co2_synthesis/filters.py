from collections import defaultdict
import numpy as np


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

    dates = []
    for key in filter:
        # first remove duplicates and empty strings
        filter[key]['options'] = [k for k in set(filter[key]['options']) if k]

        # then determine type of the filter
        vals = filter[key]['options']
        if all([is_date_range(v) for v in vals]):
            filter[key]['type'] = 'date-range'
            ranges = np.array([get_date_ranges(v) for v in vals])
            # determines the overall min and max range
            range_min = int(ranges[:,0].min())
            range_max = int(ranges[:,1].max())
            # defaults are the ranges that cover most products
            default_min = int(ranges[:,0].max())
            default_max = int(ranges[:,1].min())
            if default_min > default_max:
                default_min = default_min - 1
            filter[key]['min_max'] = [range_min, range_max]
            filter[key]['default'] = [default_min, default_max]
            filter[key].pop('options', None)
            dates += key,
        else:
            filter[key]['type'] = 'multi-select'
    for key in dates:
        filter.pop(key, None)
        
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