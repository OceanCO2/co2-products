import pathlib
import dotenv
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class Config(BaseSettings):
    LOGGER_LEVEL: str = 'DEBUG'
    GOOGLE_SHEET_ID: str
    GOOGLE_TAB_ID: str

    GITHUB_REPO: str = 'https://github.com/OceanCO2/co2-products'

    ROOT: pathlib.Path = pathlib.Path(dotenv.find_dotenv('.env')).parent.resolve()

    # website settings
    WEBSITE_TITLE: str = "Ocean CO2 Products"
    WEBSITE_DESCRIPTION: str = "Synthesis of ocean carbon dioxide data products from publication by Jiang et al. (2025)"

    DATA_FILTERS: tuple[str, ...] = (
        "Data Type",
        "Spatial domains",
        "Temporal resolution",
        "Spatial resolution",
    )

cfg = Config()   # type: ignore
