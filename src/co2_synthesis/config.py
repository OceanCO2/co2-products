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
    WEBSITE_IMAGE_MB: float = 0.3  # target max image size in MB
    WEBSITE_COLOR: str = "#0095ff"  # primary color for website
    WEBSITE_SUBTITLE: str = "A unified interface to access all ocean carbon products. For more information:"
    PUBLICATION_LINK: str = "https://essd.copernicus.org/articles/18/1405/2026/"
    PUBLICATION_CITATION: str = "Jiang et al. (2026)"

    # Filter settings
    DATA_FILTERS: tuple[str, ...] = (
        "Data Type",
        "Spatial domains",
        "Temporal resolution",
        "Spatial resolution",
    )

cfg = Config()   # type: ignore
