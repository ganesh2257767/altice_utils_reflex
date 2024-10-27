from .. import ui
from . import register_form


def register_page():
    return ui.base_page(
                register_form()
    )
