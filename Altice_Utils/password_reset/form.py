import reflex as rx

from . import PasswordResetState
from ..login import LoginState


def password_reset_form() -> rx.Component:
    return rx.card(
        rx.form(
            rx.vstack(
                rx.center(
                    rx.heading(
                        "Reset Password",
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
                            name="email",
                            required=True,
                            read_only=True,
                            value=LoginState.current_user.email
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.text(
                        "Old Password",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("lock-open")),
                        placeholder="Current Password",
                        type="password",
                        size="3",
                        width="100%",
                        name="old_password",
                        required=True,
                        on_change=PasswordResetState.set_old_password
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text(
                        "New Password",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                        rx.cond(
                            PasswordResetState.same_as_old_password,
                            rx.text(
                                "New password cannot be same as old password",
                                size="3",
                                weight="medium",
                                text_align="right",
                                width="100%",
                                color="red"
                            ),
                            rx.text(""),
                        ),
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("lock-keyhole")),
                        placeholder="New Password",
                        type="password",
                        size="3",
                        width="100%",
                        name="new_password",
                        required=True,
                        on_change=PasswordResetState.set_new_password
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "Confirm New Password",
                            size="3",
                            weight="medium",
                            text_align="left",
                            width="100%",
                        ),
                        rx.cond(
                            PasswordResetState.passwords_match,
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
                        rx.input.slot(rx.icon("lock-keyhole")),
                        placeholder="Confirm New Password",
                        type="password",
                        size="3",
                        width="100%",
                        name="confirm_new_password",
                        required=True,
                        on_change=PasswordResetState.set_confirm_new_password
                    ),

                    justify="start",
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.button(
                        "Change Password",
                        size="3",
                        width="100%",
                        type="submit",
                        disabled=~PasswordResetState.passwords_match | PasswordResetState.same_as_old_password.bool()
                    ),

                    spacing="6",
                    width="100%",
                ),
                spacing="6",
                width="100%",

            ),
            reset_on_submit=True,
            on_submit=PasswordResetState.handle_form_submit
        ),
        max_width="30em",
        size="4",
        width="100%",
    )
