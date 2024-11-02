import reflex as rx

from .. import navigation
from ..login import LoginState


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.link(
                        rx.heading(
                            "Altice Utils", size="7", weight="bold",
                        ),
                        href=navigation.HOME_ROUTE
                    ),
                    justify="center",
                    align_items="center",
                ),
                rx.cond(
                    LoginState.is_authenticated,
                    rx.hstack(
                        navbar_link("FQDN", navigation.FQDN_ROUTE),
                        navbar_link("Check Feasibility", navigation.CHECK_FEASIBILITY_ROUTE),
                        navbar_link("Netwin Helper", "/#"),
                        navbar_link("Unlock Account", navigation.UNLOCK_ACCOUNT_ROUTE),
                        navbar_link("Contact", navigation.CONTACT_ROUTE),
                        spacing="5",
                        justify="start",
                    ),
                    rx.hstack()
                ),
                rx.cond(
                    LoginState.is_authenticated,
                    rx.hstack(
                        rx.avatar(
                            fallback=f"{LoginState.current_user.first_name[0]}{LoginState.current_user.last_name[0]}",
                            radius="full",
                            size="4"
                        ),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.icon("chevron-down", size=30)
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    "Reset Password",
                                    on_click=rx.redirect(navigation.PASSWORD_RESET_ROUTE),
                                ),
                                rx.cond(
                                    LoginState.current_user.role == "ADMIN",
                                    rx.menu.item(
                                        "Check Messages",
                                        on_click=rx.redirect(navigation.CONTACT_ENTRIES_ROUTE),
                                    ),
                                ),
                                rx.menu.separator(),
                                rx.menu.item(
                                    "Logout",
                                    color="red",
                                    on_click=LoginState.logout
                                ),
                            ),
                        ),
                        justify="end",
                        align_items="center",
                    ),
                    rx.hstack(
                        rx.link(
                            rx.button(
                                "Register",
                                size="3",
                                variant="outline",
                            ),
                            href=navigation.REGISTER_ROUTE,
                        ),
                        rx.link(
                            rx.button(
                                "Log In",
                                size="3",
                                variant="outline",
                            ),
                            href=navigation.LOGIN_ROUTE,
                            spacing="4",
                            justify="end",
                        )
                    ),
                ),

                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.link(
                        rx.heading(
                            "Altice Utils", size="6", weight="bold",
                        ),
                        href=navigation.HOME_ROUTE
                    ),

                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon("menu", size=30)
                    ),
                    rx.menu.content(
                        rx.menu.item("FQDN"),
                        rx.menu.item("Check Feasibility"),
                        rx.menu.item("Netwin Helper"),
                        rx.menu.item("Contact", on_click=rx.redirect(navigation.CONTACT_ROUTE)),
                        rx.menu.separator(),
                        rx.menu.item("Log in", on_click=rx.redirect(navigation.LOGIN_ROUTE)),
                        rx.menu.item("Register", on_click=rx.redirect(navigation.REGISTER_ROUTE)),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        width="100%",
    )
