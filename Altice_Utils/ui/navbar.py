import reflex as rx

from ..login import LoginState
from .. import navigation


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
                        navbar_link("Check Feasibility", "/#"),
                        navbar_link("Netwin Helper", "/#"),
                        navbar_link("Contact", navigation.CONTACT_ROUTE),
                        spacing="5",
                        justify="start",
                    ),
                    rx.hstack()
                ),
                rx.cond(
                    LoginState.is_authenticated,
                    rx.hstack(
                        rx.link(
                            rx.button(
                                "Log Out",
                                size="3",
                                variant="outline",
                                color="red",
                                on_click=LoginState.logout
                            ),
                            href=navigation.LOGIN_ROUTE,
                            spacing="4",
                            justify="end",
                        )
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
