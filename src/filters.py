import re


def split_multi_values(value):
    """Split comma-separated cell values, trimming brackets and quotes."""
    if not value:
        return []
    cleaned = value.strip()
    if cleaned.startswith('[') and cleaned.endswith(']'):
        cleaned = cleaned[1:-1]
    parts = []
    for part in cleaned.split(','):
        token = part.strip().strip('"').strip("'")
        if token:
            parts.append(token)
    return parts or [cleaned]


def generate_filters(filter_types, headers, data):
    """
    Generate filter options based on the data.

    Args:
        filter_types (list): List of filter types.
        headers (list): List of headers.
        data (list): List of data rows.

    Returns:
        dict: Dictionary of filters, keyed by header, with type and options.
    """
    filters = {}
    for i, ftype in enumerate(filter_types):
        if ftype:
            header = headers[i]
            values = [row[i] for row in data if row[i]]
            if ftype.lower() == 'checkbox':
                options = set()
                for v in values:
                    for token in split_multi_values(v):
                        options.add(token)
                filters[header] = {'type': 'checkbox', 'options': sorted(options)}
            elif ftype.lower() == 'radio':
                options = set()
                for v in values:
                    for token in split_multi_values(v):
                        options.add(token)
                filters[header] = {'type': 'radio', 'options': sorted(options)}
            elif 'slider' in ftype.lower():
                range_min = None
                range_max = None
                max_start = None
                min_end = None
                period_options = set()
                has_period_range = False
                numeric_values = []

                for raw_value in values:
                    value = raw_value.strip()
                    if not value or value.lower() == 'na':
                        continue

                    range_match = re.match(r'^(\d{3,4})\s*-\s*(\d{3,4})$', value)
                    if range_match:
                        has_period_range = True
                        start = int(range_match.group(1))
                        end = int(range_match.group(2))
                        if range_min is None or start < range_min:
                            range_min = start
                        if range_max is None or end > range_max:
                            range_max = end
                        if max_start is None or start > max_start:
                            max_start = start
                        if min_end is None or end < min_end:
                            min_end = end
                        continue

                    try:
                        numeric_values.append(float(value))
                    except ValueError:
                        for token in split_multi_values(value):
                            period_options.add(token)

                if has_period_range or period_options:
                    filter_data = {'type': 'period'}
                    if range_min is not None and range_max is not None:
                        filter_data['range_min'] = range_min
                        filter_data['range_max'] = range_max
                        filter_data['default_min'] = max_start
                        filter_data['default_max'] = min_end
                    if period_options:
                        filter_data['options'] = sorted(period_options)
                    if filter_data.get('range_min') is not None or filter_data.get('options'):
                        filters[header] = filter_data
                elif numeric_values:
                    min_val = min(numeric_values)
                    max_val = max(numeric_values)
                    filters[header] = {'type': 'slider', 'min': min_val, 'max': max_val}
    return filters


__all__ = ['generate_filters', 'split_multi_values']
