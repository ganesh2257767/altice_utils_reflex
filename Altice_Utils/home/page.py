import reflex as rx
from .. import ui
from ..login import LoginState
from .dashboard import home_dashboard

def home_page():
    return ui.base_page(
            home_dashboard()
    )
