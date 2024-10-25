import reflex as rx
from . import ContactState

def contact_form() -> rx.Component:
    return rx.card(
        rx.form(
            rx.vstack(
                rx.center(
                    rx.heading(
                        "Send me a message",
                        size="6",
                        as_="h2",
                        text_align="center",
                        width="100%",
                    ),
                    direction="column",
                    spacing="5",
                    width="100%",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            "First Name",
                            size="3",
                            weight="medium",
                            text_align="left",
                            width="100%",
                        ),
                        rx.input(
                            rx.input.slot(rx.icon("user")),
                            placeholder="First Name",
                            type="text",
                            size="3",
                            width="100%",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text(
                            "Last Name",
                            size="3",
                            weight="medium",
                            text_align="left",
                            width="100%",
                        ),
                        rx.input(
                            rx.input.slot(rx.icon("user")),
                            placeholder="Last Name",
                            type="text",
                            size="3",
                            width="100%",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                ),
                rx.vstack(
                    rx.text(
                        "Email address",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("at-sign")),
                        placeholder="user@alticeusa.com",
                        type="email",
                        size="3",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "Message",
                            size="3",
                            weight="medium",
                        ),
                        justify="between",
                        width="100%",
                    ),
                    rx.text_area(
                        placeholder="Your message/concern here",
                        type="password",
                        size="3",
                        width="100%",
                        height="100%",
                        resize="vertical"
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.button("Submit", size="3", width="100%"),
                spacing="6",
                width="100%",
            ),
            reset_on_submit=True,
        ),
        max_width="28em",
        size="4",
        width="100%",
    )