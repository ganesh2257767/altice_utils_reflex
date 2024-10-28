import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DB_URL')
config = rx.Config(
    app_name="Altice_Utils",
    db_url=db_url
)