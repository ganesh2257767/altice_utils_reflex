import reflex as rx

from . import UsageState
from ..login import LoginState


def pie_chart() -> rx.Component:
    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=UsageState.usages,
            data_key="count",
            name_key="service",
            cx="50%",
            cy="50%",
            padding_angle=1,
            inner_radius="70",
            outer_radius="100",
            label=True,
        ),
        rx.recharts.legend(),
        height=300,
    )


def home_dashboard():
    return rx.card(
        rx.center(
            rx.vstack(
                rx.heading(f"Welcome, {LoginState.current_user.first_name}", size="5"),
                rx.hstack(
                    rx.text("Usage Analytics", size="4", weight="medium"),
                    align="center",
                    spacing="2",
                ),
                align="center",
                width="100%",
                justify="center",
            ),
            pie_chart()
        ),
        max_width="80%",
        size="4",
        width="100%",
        on_mount=UsageState.get_usage_data()
    )
