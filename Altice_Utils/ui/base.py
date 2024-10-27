import reflex as rx
from .navbar import navbar


def base_page(*children) -> rx.Component:
    return rx.fragment(
    navbar(),
        rx.box(
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
