import pathlib
import dotenv
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class Config(BaseSettings):
    LOGGER_LEVEL: str = 'DEBUG'
    GOOGLE_SHEET_ID: str
    GOOGLE_TAB_ID: str

    ROOT: pathlib.Path = pathlib.Path(dotenv.find_dotenv('.env')).parent.resolve()

cfg = Config()   # type: ignore
