"""Command-line interface for co2-synthesis."""
import argparse

from loguru import logger
from . import cfg
from . import generate_page_main
from .google_sheet import get_url_from_sheet_id_and_gid


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate static web page for ocean CO2 products synthesis"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="co2-synthesis 0.1.0"
    )

    parser.add_argument(
        "--google-sheet-url",
        type=str,
        help="Full URL of the Google Sheet to fetch data from",
        default=None
    )
    
    args = parser.parse_args()
    
    if args.google_sheet_url:
        google_sheet_url = args.google_sheet_url
    else:
        # Call the generate_page main function
        sheet_id = cfg.GOOGLE_SHEET_ID
        gid = cfg.GOOGLE_TAB_ID

        google_sheet_url = get_url_from_sheet_id_and_gid(sheet_id, gid)

    logger.info("Generating synthesis page...")
    generate_page_main(google_sheet_url)

    logger.info("Page generation complete!")


if __name__ == "__main__":
    main()
