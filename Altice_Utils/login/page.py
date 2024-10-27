from .. import ui
from . import login_form


def login_page():
    return ui.base_page(
                login_form()
    )
