import reflex as rx
from . import CheckFeasibilityState

def check_feasibility_form() -> rx.Component:
    return rx.card(
        rx.center(
            rx.heading(
                "Check Feasibility",
                size="6",
                as_="h2",
                text_align="center",
                width="100%",
            ),
            direction="column",
            spacing="5",
            width="100%",
        ),
        rx.tabs.root(
            rx.center(
                rx.tabs.list(
                    rx.tabs.trigger("On A Specific Address", value="tab1"),
                    rx.tabs.trigger("Next Available Address", value="tab2"),
                    size="2",
                    loop=True
                ),
            ),
            rx.tabs.content(
                rx.form(
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.text(
                                    "Environment",
                                    size="3",
                                    weight="medium",
                                    text_align="left",
                                    width="100%",
                                ),
                                rx.select(
                                    value=CheckFeasibilityState.env,
                                    items=CheckFeasibilityState.addresses.keys(),
                                    width="100%",
                                    on_change=lambda x: CheckFeasibilityState.set_environment(x, 'env'),
                                    required=True
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Side",
                                    size="3",
                                    weight="medium",
                                    text_align="left",
                                    width="100%",
                                ),
                                rx.select(
                                    value=CheckFeasibilityState.side,
                                    items=CheckFeasibilityState.side_dropdown,
                                    width="100%",
                                    on_change=lambda x: CheckFeasibilityState.set_environment(x, 'side'),
                                    required=True
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Technology",
                                    size="3",
                                    weight="medium",
                                    text_align="left",
                                    width="100%",
                                ),
                                rx.select(
                                    value=CheckFeasibilityState.technology,
                                    items=CheckFeasibilityState.technology_dropdown,
                                    width="100%",
                                    on_change=lambda x: CheckFeasibilityState.set_environment(x, 'technology'),
                                    required=True
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text(
                                "Address",
                                size="3",
                                weight="medium",
                                text_align="left",
                                width="100%",
                            ),
                            rx.select(
                                value=CheckFeasibilityState.address,
                                items=CheckFeasibilityState.addresses_dropdown,
                                width="100%",
                                required=True,
                                on_change=CheckFeasibilityState.set_address,
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        rx.button("Check", size="3", width="100%", loading=CheckFeasibilityState.loading),
                        spacing="6",
                        width="100%",
                    ),
                    reset_on_submit=True,
                    padding="1.25rem",
                    on_submit=CheckFeasibilityState.handle_form_submit_specific_address,
                    id="form1"
                ),
                value="tab1"
            ),
            rx.tabs.content(
                rx.form(
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.text(
                                    "Environment",
                                    size="3",
                                    weight="medium",
                                    text_align="left",
                                    width="100%",
                                ),
                                rx.select(
                                    value=CheckFeasibilityState.env,
                                    items=CheckFeasibilityState.addresses.keys(),
                                    width="100%",
                                    on_change=lambda x: CheckFeasibilityState.set_environment(x, 'env'),
                                    required=True
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Side",
                                    size="3",
                                    weight="medium",
                                    text_align="left",
                                    width="100%",
                                ),
                                rx.select(
                                    value=CheckFeasibilityState.side,
                                    items=CheckFeasibilityState.side_dropdown,
                                    width="100%",
                                    on_change=lambda x: CheckFeasibilityState.set_environment(x, 'side'),
                                    required=True
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Technology",
                                    size="3",
                                    weight="medium",
                                    text_align="left",
                                    width="100%",
                                ),
                                rx.select(
                                    value=CheckFeasibilityState.technology,
                                    items=CheckFeasibilityState.technology_dropdown,
                                    width="100%",
                                    on_change=lambda x: CheckFeasibilityState.set_environment(x, 'technology'),
                                    required=True
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            width="100%"
                        ),
                        # rx.vstack(
                        #     rx.text(
                        #         "Address",
                        #         size="3",
                        #         weight="medium",
                        #         text_align="left",
                        #         width="100%",
                        #     ),
                        #     rx.select(
                        #         value=CheckFeasibilityState.address,
                        #         items=CheckFeasibilityState.addresses_dropdown,
                        #         width="100%",
                        #         on_change=CheckFeasibilityState.set_address
                        #     ),
                        #     spacing="2",
                        #     width="100%",
                        # ),
                        rx.button("Check", size="3", width="100%", loading=CheckFeasibilityState.loading),
                        spacing="6",
                        width="100%",
                    ),
                    reset_on_submit=True,
                    padding="1.25rem",
                    on_submit=CheckFeasibilityState.handle_form_submit_next_address,
                    id="form2"
                ),
                value="tab2"
            ),
            default_value="tab1",
            padding="1rem"
        ),
        max_width="28em",
        size="4",
        width="100%",
        on_mount=CheckFeasibilityState.reset_page
    )
