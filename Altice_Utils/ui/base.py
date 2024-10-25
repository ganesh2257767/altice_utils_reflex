import reflex as rx
from .navbar import navbar


def base_page(heading, *children) -> rx.Component:
    return rx.fragment(
    navbar(),
        rx.center(
            rx.heading(heading, size="9"),
            padding="20px"
        ),
        rx.vstack(
            *children,
            align="center",
            justify="between",
            spacing="4",
            min_height="50vh"
        ),
        rx.color_mode.button(position="bottom-right"),
    )
