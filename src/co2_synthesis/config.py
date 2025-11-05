import pathlib
import dotenv
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class Config(BaseSettings):
    LOGGER_LEVEL: str = 'DEBUG'
    LOCAL_BUILD: bool = False
    ROOT: pathlib.Path = pathlib.Path(dotenv.find_dotenv('.env')).parent.resolve()
    
    GOOGLE_SHEET_ID: str
    GOOGLE_TAB_ID: str

    GITHUB_REPO: str = 'https://github.com/OceanCO2/co2-products'
    SUBMISSION_FORM: str = "https://docs.google.com/forms/d/e/1FAIpQLSdguEed1sRdgHjhP_KsgHeh_G7gHjz8qGmuTu9C7K_fK7hyUQ/viewform"
    CONTACT_EMAIL: str = "noaa.ocads@noaa.gov"

    # website settings
    WEBSITE_TITLE: str = "Ocean CO2 Products"
    WEBSITE_DESCRIPTION: str = "Ocean carbon products from Jiang et al. (2025)"
    WEBSITE_COPY: str = "&copy; Website by <a href='https://github.com/lukegre/' target='_blank'>Luke Gregor</a> (2025)"

    # Filter settings
    DATA_FILTERS: tuple[str, ...] = (
        "Data Type",
        "Spatial domains",
        "Temporal resolution",
        "Spatial resolution",
    )

cfg = Config()   # type: ignore
