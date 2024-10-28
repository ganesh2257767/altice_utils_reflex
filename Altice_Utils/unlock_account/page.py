from .. import ui
from . import unlock_account_form


def unlock_account_page():
    return ui.base_page(
                unlock_account_form()
    )
