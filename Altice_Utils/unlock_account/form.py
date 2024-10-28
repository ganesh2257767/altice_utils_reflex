import reflex as rx
from . import UnlockAccountState


def unlock_account_form() -> rx.Component:
    return rx.card(
        rx.form(
            rx.vstack(
                rx.center(
                    rx.heading(
                        "Unlock Account",
                        size="6",
                        as_="h2",
                        text_align="center",
                        width="100%",
                    ),
                    direction="column",
                    spacing="5",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "Environment",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",

                    ),
                    rx.select(
                        items=["QA INT", "QA 2"],
                        size="3",
                        width="100%",
                        name="env",
                        required=True
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                        rx.text(
                            "Corp",
                            size="3",
                            weight="medium",
                        ),
                    rx.input(
                        rx.input.slot(rx.icon("compass")),
                        placeholder="Enter corp",
                        type="text",
                        size="3",
                        width="100%",
                        name="corp",
                        min_length=4,
                        max_length=5,
                        required=True
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "House",
                        size="3",
                        weight="medium",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("warehouse")),
                        placeholder="Enter house",
                        type="text",
                        size="3",
                        width="100%",
                        name="house",
                        max_length=6,
                        required=True
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.button("Unlock", size="3", width="100%"),
                spacing="6",
                width="100%",
            ),
            reset_on_submit=True,
            on_submit=UnlockAccountState.handle_form_submit
        ),
        max_width="28em",
        size="4",
        width="100%",
    )
