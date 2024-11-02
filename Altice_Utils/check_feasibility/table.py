import reflex as rx

from . import CheckFeasibilityState


def populate_result_table(cell_data: str):
    return rx.cond(
        cell_data.contains("AVAILABLE") | cell_data.contains("NOT_AVAILABLE"),
        rx.cond(
            cell_data.contains("NOT"),
        rx.table.cell(rx.badge(cell_data, color_scheme="crimson", size="3"), justify="center"),
        rx.table.cell(rx.badge(cell_data, color_scheme="cyan", size="3"), justify="center"),
        ),
        rx.table.cell(cell_data, justify="center")
    )


def check_feasibility_table():
    return rx.card(
        rx.vstack(
            rx.center(
                rx.heading(
                    "Check Feasibility Result",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",

                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Address", justify="center"),
                            rx.table.column_header_cell("PDO ID", justify="center"),
                            rx.table.column_header_cell("Status", justify="center"),
                        ),
                    ),
                    rx.table.body(
                        rx.table.row(
                            rx.foreach(CheckFeasibilityState.result, populate_result_table),
                        )
                    ),
                    width="100%",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),

            spacing="6",
            width="100%",
        ),
        max_width="50%",
        size="4",
        width="100%",
    )
