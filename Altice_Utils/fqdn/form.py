import reflex as rx
from . import FQDNState

def fqdn_form() -> rx.Component:
    return rx.card(
        rx.form(
            rx.vstack(
                rx.center(
                    rx.heading(
                        "FQDN",
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
                        "MAC",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",

                    ),
                    rx.input(
                        rx.input.slot(rx.icon("router")),
                        placeholder="ABC123XYZ456",
                        size="3",
                        width="100%",
                        name="mac",
                        required=True,
                        max_length=12,
                        min_length=12
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.button("Submit", size="3", width="100%", loading=FQDNState.start),
                spacing="6",
                width="100%",
            ),
            on_submit=FQDNState.handle_form_submit
        ),
        max_width="28em",
        size="4",
        width="100%",
    )