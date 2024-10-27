import reflex as rx
from . import FQDNState
from ..login import LoginState


def fqdn_table():
    return rx.card(
        rx.vstack(
            rx.center(
                rx.heading(
                    "FQDN Result",
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
                        rx.table.column_header_cell("FQDN Name"),
                        rx.table.column_header_cell("MAC"),
                        rx.table.column_header_cell("DNs"),
                        rx.table.column_header_cell("Time"),
                    ),
                ),
                rx.table.body(
                    rx.table.row(
                        rx.table.row_header_cell(FQDNState.fqdn_name),
                        rx.table.cell(FQDNState.mac),
                        rx.table.cell(FQDNState.dns),
                        rx.table.cell(FQDNState.time),
                    )
                ),
                width="100%",
            ),
            spacing="6",
            width="100%",
        ),
        rx.center(
            rx.hstack(
                rx.button("Delete FQDN", color_scheme="red", size="3"),
                rx.button("Clear result table", color_scheme="blue", size="3", on_click=FQDNState.reset_results),

            ),
            padding="2em"
        ),
        max_width="90%",
        size="4",
        width="100%",
    )
