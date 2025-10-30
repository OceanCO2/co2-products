import pathlib
import dotenv
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class Config(BaseSettings):
    GOOGLE_SHEET_ID: str
    GOOGLE_TAB_ID: str
    FONTAWESOME_KEY: str

    ROOT: pathlib.Path = pathlib.Path(dotenv.find_dotenv('.env')).parent.resolve()

cfg = Config()