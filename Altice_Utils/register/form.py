import reflex as rx

from . import RegisterState
from .. import navigation

def register_form() -> rx.Component:
    return rx.card(
        rx.form(
            rx.vstack(
                rx.center(
                    rx.heading(
                        "Create an account",
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
                            name="first_name",
                            required=True,
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
                            name="last_name",
                            required=True,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "Email address",
                            size="3",
                            weight="medium",
                            text_align="left",
                            width="100%",
                        ),
                        rx.cond(
                            RegisterState.valid_email,
                            rx.text(""),
                            rx.text(
                                "Must be @alticeusa.com",
                                size="3",
                                weight="medium",
                                text_align="right",
                                width="100%",
                                color="red"
                            ),
                        ),
                        width="100%",
                    ),

                    rx.input(
                        rx.input.slot(rx.icon("at-sign")),
                        placeholder="user@alticeusa.com",
                        type="email",
                        size="3",
                        width="100%",
                        name="email",
                        required=True,
                        on_change=RegisterState.set_email
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "Password",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("lock")),
                        placeholder="Enter your password",
                        type="password",
                        size="3",
                        width="100%",
                        name="password",
                        required=True,
                        on_change=RegisterState.set_password
                    ),
                    justify="start",
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "Confirm Password",
                            size="3",
                            weight="medium",
                            text_align="left",
                            width="100%",
                        ),
                        rx.cond(
                            RegisterState.passwords_match,
                            rx.text(""),
                            rx.text(
                                "Passwords do not match",
                                size="3",
                                weight="medium",
                                text_align="right",
                                width="100%",
                                color="red"
                            ),
                        ),
                        width="100%",
                    ),

                    rx.input(
                        rx.input.slot(rx.icon("lock")),
                        placeholder="Enter your password again",
                        type="password",
                        size="3",
                        width="100%",
                        name="confirm_password",
                        required=True,

                        on_change=RegisterState.set_confirm_password
                    ),
                    justify="start",
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "Role",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.select(
                        ["ADMIN", "USER"],
                        name="role",
                        width="50%",
                        size="3",
                        required=True
                    ),
                    justify="start",
                    spacing="2",
                    width="100%",
                ),
                rx.button(
                    "Register",
                    size="3",
                    width="100%",
                    type="submit",
                    disabled=~RegisterState.passwords_match | ~RegisterState.valid_email,
                    loading=RegisterState.loading
                ),
                rx.center(
                    rx.text("Already registered?", size="3"),
                    rx.link("Sign in", href=navigation.LOGIN_ROUTE, size="3"),
                    opacity="0.8",
                    spacing="2",
                    direction="row",
                    width="100%",
                ),
                spacing="6",
                width="100%",
            ),
            reset_on_submit=True,
            on_submit=RegisterState.handle_form_submit
        ),
        max_width="30em",
        size="4",
        width="100%",
    )
