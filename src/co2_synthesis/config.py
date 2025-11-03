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
    WEBSITE_DESCRIPTION: str = "Ocean carbon products from Jiang et al. (2025)"
    WEBSITE_COPY: str = "&copy; Website by Luke Gregor (2025)"
    WEBSITE_INFOS_HTML: str = """
        <a href="https://docs.google.com/forms/d/e/1FAIpQLSdguEed1sRdgHjhP_KsgHeh_G7gHjz8qGmuTu9C7K_fK7hyUQ/viewform" target="_blank">Submit a new dataset</a>
        <br>

    """

    DATA_FILTERS: tuple[str, ...] = (
        "Data Type",
        "Spatial domains",
        "Temporal resolution",
        "Spatial resolution",
    )

cfg = Config()   # type: ignore
