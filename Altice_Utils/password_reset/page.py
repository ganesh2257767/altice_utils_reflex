from .. import ui
from . import password_reset_form


def password_reset_page():
    return ui.base_page(
                password_reset_form()
    )
