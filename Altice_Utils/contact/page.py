from .. import ui
from . import contact_form, ContactState, MessageModel, entries_table


def contact_entries_page():
    return ui.base_page(
        entries_table()
    )


def contact_page():
    return ui.base_page(
        contact_form(),
    )
