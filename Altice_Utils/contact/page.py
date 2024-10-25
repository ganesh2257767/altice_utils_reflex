from .. import ui
from . import contact_form, ContactState, ContactModel
import reflex as rx

def update_entries_table(contact: ContactModel):
    return rx.table.row(
        rx.table.row_header_cell(contact.user_id + ' ' + contact.last_name),
        rx.table.cell(contact.email),
        rx.table.cell(contact.message)
    )


def entries_table():
    return (
        rx.vstack(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Name"),
                        rx.table.column_header_cell("Email"),
                        rx.table.column_header_cell("Message"),
                    ),
                ),
                rx.table.body(
                    # rx.foreach(
                    #     ContactState.entries, update_entries_table
                    # )
                    ),
                width="100%",
            ))
    )

def contact_entries_page():
    return ui.base_page(
        "Contact Entries",
        entries_table()
    )


def contact_page():
    return ui.base_page(
        "",
        contact_form(),
    )
