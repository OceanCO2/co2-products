import re
import requests
import csv
import pandas as pd
from io import StringIO


readers = {
    'pandas': pd.read_csv,
    'csv': csv.reader,
}


def get_sheet_data(full_url: str, reader='pandas'):
    """
    Retrieve data from the public Google Sheet.

    Args:
        full_url (str): The full URL of the Google Sheet.

    Returns:
        tuple: (filter_types, shown_on_card, headers, data)
            - filter_types: List of filter types for each column.
            - shown_on_card: List indicating whether the column is shown on the card.
            - headers: List of column headers.
            - data: List of lists, each inner list is a row of data.
    """
    
    url = google_sheet_url_to_csv_url(full_url)
    buffer = get_sheet_as_buffer(url)

    data = readers[reader](buffer)
    
    return data 



def get_sheet_as_buffer(full_url: str) -> StringIO:
    """
    Retrieve the Google Sheet data as a StringIO object.

    Args:
        full_url (str): The full URL of the Google Sheet.

    Returns:
        StringIO: A StringIO object containing the CSV data.
    """
    csv_url = google_sheet_url_to_csv_url(full_url)
    response = requests.get(csv_url)
    response.raise_for_status()
    return StringIO(response.content.decode('utf-8-sig'))


def google_sheet_url_to_csv_url(full_url:str) -> str:
    """
    Convert a full Google Sheet URL to a direct CSV export URL, including tab ID if present.

    Args:
        full_url (str): The full URL of the Google Sheet.

    Returns:
        str: The direct CSV export URL.
    """
    match = re.match(r'https://docs.google.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/.*gid=(\d+))?', full_url)
    if not match:
        raise ValueError("Invalid Google Sheet URL")
    
    sheet_id = match.group(1)
    gid = match.group(3) if match.group(3) else '0'
    
    csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&gid={gid}'
    return csv_url