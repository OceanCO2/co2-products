import requests
import csv
from io import StringIO

def get_sheet_data(sheet_id):
    """
    Retrieve data from the public Google Sheet.

    Args:
        sheet_id (str): The ID of the Google Sheet.

    Returns:
        tuple: (filter_types, shown_on_card, headers, data)
            - filter_types: List of filter types for each column.
            - shown_on_card: List indicating whether the column is shown on the card.
            - headers: List of column headers.
            - data: List of lists, each inner list is a row of data.
    """
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    response = requests.get(url)
    response.raise_for_status()
    csv_content = response.content.decode('utf-8-sig')
    reader = csv.reader(StringIO(csv_content))
    all_data = list(reader)
    # Strip whitespace from all cells
    all_data = [[cell.strip() for cell in row] for row in all_data]
    
    if len(all_data) < 3:
        raise ValueError("Sheet must have at least three rows: filter types, shown on card, headers.")
    
    filter_types = all_data[0]
    shown_on_card = all_data[1]
    headers = all_data[2]
    data = all_data[3:]
    
    return filter_types, shown_on_card, headers, data
