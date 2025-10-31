import pathlib
import re
import requests
import csv
import pandas as pd
from io import StringIO
from typing import Literal


readers = {
    'pandas': pd.read_csv,
    'csv': csv.reader,
}


def get_sheet_data(full_url: str, reader='pandas', **kwargs):
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

    url = get_download_url_from_sheet_url(full_url, format='csv')
    buffer = get_sheet_as_buffer(url)

    data = readers[reader](buffer, **kwargs)
    
    return data 


def download_sheet_as_excel(full_url: str, output_path: str | pathlib.Path):
    """
    Download the Google Sheet as an Excel file.

    Args:
        full_url (str): The full URL of the Google Sheet.
        output_path (str): The path to save the Excel file.
    """

    sheet_id, gid = get_id_and_gid_from_url(full_url)  # validate URL
    download_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"

    response = requests.get(download_url)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        f.write(response.content)


def get_sheet_as_buffer(full_url: str, format:Literal['csv', 'excel']='csv') -> StringIO:
    """
    Retrieve the Google Sheet data as a StringIO object.

    Args:
        full_url (str): The full URL of the Google Sheet.

    Returns:
        StringIO: A StringIO object containing the CSV data.
    """
    download_url = get_download_url_from_sheet_url(full_url, format=format)
    response = requests.get(download_url)
    response.raise_for_status()
    return StringIO(response.content.decode('utf-8-sig'))


def get_download_url_from_sheet_url(sheet_url:str, format:Literal['csv', 'excel']='csv') -> str:
    """
    Convert a full Google Sheet URL to a direct CSV export URL, including tab ID if present.

    Args:
        sheet_url (str): The full URL of the Google Sheet.

    Returns:
        str: The direct CSV export URL.
    """
    match = re.match(r'https://docs.google.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/.*gid=(\d+))?', sheet_url)
    if not match:
        raise ValueError("Invalid Google Sheet URL")
    
    sheet_id = match.group(1)
    gid = match.group(3) if match.group(3) else '0'

    download_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:{format}&gid={gid}'

    return download_url


def get_url_from_sheet_id_and_gid(sheet_id: str, gid: str) -> str:
    """
    Construct the full Google Sheet URL from sheet ID and gid.

    Args:
        sheet_id (str): The Google Sheet ID.
        gid (str): The tab ID (gid).

    Returns:
        str: The full Google Sheet URL.
    """
    return f'https://docs.google.com/spreadsheets/d/{sheet_id}/edit?gid={gid}'


def get_id_and_gid_from_url(sheet_url: str) -> tuple[str, str]:
    """
    Extract the sheet ID and gid from a full Google Sheet URL.

    Args:
        sheet_url (str): The full URL of the Google Sheet.

    Returns:
        tuple[str, str]: A tuple containing the sheet ID and gid.
    """
    match = re.match(r'https://docs.google.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/.*gid=(\d+))?', sheet_url)
    if not match:
        raise ValueError("Invalid Google Sheet URL")

    sheet_id = match.group(1)
    gid = match.group(3) if match.group(3) else '0'

    return sheet_id, gid
