import reflex as rx
from .. import ui
from ..login import LoginState

def home_page():
    return ui.base_page(
            rx.heading(f"Welcome {LoginState.current_user.first_name}", size='4')
    )
