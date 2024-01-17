import reflex as rx
from os import getenv

config = rx.Config(
    app_name="meeting_notes",
    api_url=getenv("ROOT_PATH", "http://localhost:3000/"),
)
