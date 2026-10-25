import logging
from os import getenv
from dotenv import load_dotenv


logging.basicConfig(
    format="[%(asctime)s]: [%(name)s)]: [%(levelname)s]: %(message)s",
)

logger = logging.getLogger(__name__)


load_dotenv()


class StandartLoader:
    
    @property
    def get_token_bot(self) -> str:
        token = getenv("TOKEN_BOT")

        if not token:
            logger.error(
                "get_token_bot: telegram token is not defined"
            )
            raise FileNotFoundError
        
        return token

    @property
    def get_db_config(self) -> str:
        
        DB_NAME = getenv("DB_NAME")
        DB_PASS = getenv("DB_PASS")
        DB_PORT = getenv("DB_PORT")
        DB_USER = getenv("DB_USER")
        DB_HOST = getenv("DB_HOST")
        
        if not all(
            [
                
                isinstance(DB_NAME, str),
                isinstance(DB_PASS, str),   
                isinstance(DB_PORT, str),   
                isinstance(DB_USER, str),
                isinstance(DB_HOST, str),
            ]
        ):
            logger.error(
                "get_db_config: the program did not identify the data for connecting to the database"
            )
            raise FileNotFoundError
        
        
        return (
            f"postgresql+asyncpg://{DB_USER}:{DB_PASS}"
            f"@{DB_HOST}:{DB_PORT}"
            f"/{DB_NAME}"
        )
        
    @property
    def get_output(self) -> str:
        chat = getenv("OUTPUT_CHAT")
        
        if not chat:
            logger.warning(
                "get_output: telegram chat for withdrawals is not specified"
            )
            raise FileNotFoundError
        
        return chat