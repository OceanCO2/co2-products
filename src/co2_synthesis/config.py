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
    GOOGLE_SHEET_SKIPROWS: int = 1
    GOOGLE_SHEET_INDEXCOL: int = 0

    GITHUB_REPO: str = 'https://github.com/OceanCO2/co2-products'
    SUBMISSION_FORM: str = "https://docs.google.com/forms/d/e/1FAIpQLSeNP4JO0QeNak7F5cYL_r7yKzxQCRsZi7bkP7kYD4G_chdBBg/viewform"
    CONTACT_EMAIL: str = "noaa.ocads@noaa.gov"

    # website settings
    WEBSITE_TITLE: str = "Ocean CO2 Products"
    WEBSITE_DESCRIPTION: str = "Ocean carbon products from Jiang et al. (2025)"
    WEBSITE_IMAGE_MB: float = 0.3  # target max image size in MB
    WEBSITE_COLOR: str = "#0095ff"  # primary color for website

    # Filter settings
    DATA_FILTERS: tuple[str, ...] = (
        "Data Type",
        "Spatial domains",
        "Temporal resolution",
        "Spatial resolution",
    )

cfg = Config()   # type: ignore
