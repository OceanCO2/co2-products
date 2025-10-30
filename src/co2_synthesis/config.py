import dotenv
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class Config(BaseSettings):
    GOOGLE_SHEET_ID: str
    GOOGLE_TAB_ID: str
    FONTAWESOME_KEY: str

cfg = Config()