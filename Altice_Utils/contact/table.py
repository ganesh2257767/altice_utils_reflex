import reflex as rx
from sqlmodel import select

from . import ContactModel, ContactState
from ..register import UserModel


def update_entries_table():
    with rx.session() as session:
        statement = select(ContactModel)
        messages = session.exec(statement).all()

    for message in messages:
        with rx.session() as session:
            statement = select(UserModel).where(UserModel.email == message.created_by)
            user: UserModel = session.exec(statement).one()
            yield rx.table.row(
                rx.table.row_header_cell(user.first_name + " " + user.last_name),
                rx.table.cell(message.created_by),
                rx.table.cell(message.message),
                rx.table.cell(message.created_at.strftime("%Y-%m-%d %H:%M:%s")),
            )


def entries_table():
    return rx.card(
        rx.vstack(
            rx.center(
                rx.heading(
                    "Messages",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Name"),
                        rx.table.column_header_cell("Email"),
                        rx.table.column_header_cell("Message"),
                        rx.table.column_header_cell("Created At"),
                    ),
                ),
                rx.table.body(
                    *update_entries_table()

                ),
                width="100%",
            ),
            spacing="6",
            width="100%",
        ),
        max_width="90%",
        size="4",
        width="100%",
    )
