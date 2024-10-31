import reflex as rx

from . import ContactState, UserMessage


def render_function(user_message: UserMessage):
    return rx.table.row(
        rx.table.cell(user_message.name),
        rx.table.cell(user_message.email),
        rx.table.cell(user_message.message),
        rx.table.cell(user_message.created_at),
        rx.table.cell(
            rx.cond(
                user_message.completed,
                "Yes",
                "No"
            ),
        ),
        rx.table.cell(
            rx.hstack(
                rx.cond(
                    user_message.completed,
                    rx.tooltip(
                        rx.button(rx.icon("check", size=20), size="1", disabled=True),
                        content="Action item already completed"
                    ),
                    rx.tooltip(
                        rx.button(rx.icon("check", size=20), size="1", color_scheme="green",
                                  on_click=lambda: ContactState.complete_entry(user_message.id), loading=ContactState.loading_complete),
                        content="Mark this action item as complete"
                    )
                ),
                rx.cond(
                    user_message.completed,
                    rx.tooltip(
                        rx.button(rx.icon("x", size=20), size="1", color_scheme="orange",
                                  on_click=lambda: ContactState.undo_complete_entry(user_message.id), loading=ContactState.loading_incomplete),
                        content="Undo this action item and mark as incomplete"
                    ),
                    rx.tooltip(
                        rx.button(rx.icon("x", size=20), size="1", disabled=True),
                        content="Action item not yet completed"
                    )
                ),
                rx.dialog.root(
                    rx.dialog.trigger(
                        rx.button(rx.icon("trash-2", size=20), size="1", color_scheme="red", loading=ContactState.loading_delete),
                    ),
                    rx.dialog.content(
                        rx.dialog.title("Are you sure?"),
                        rx.dialog.description(
                            f"This action will permanently delete this message from {user_message.email} with id: {user_message.id}",
                        ),
                        rx.hstack(
                            rx.dialog.close(
                                rx.button("Yes", size="3", color_scheme="red",
                                          on_click=lambda: ContactState.delete_entry(user_message.id)),
                            ),
                            rx.dialog.close(
                                rx.button("No", size="3"),
                            ),
                            padding_top="1em",
                        )
                    ),
                )
            )

        )
    )


def entries_table():
    return rx.card(
        rx.cond(
            ContactState.loading_messages,
            rx.vstack(
                rx.center(
                    rx.heading(
                        "Loading messages",
                        size="6",
                        as_="h2",
                        text_align="center",
                        width="100%",
                    ),
                    direction="column",
                    spacing="5",
                    width="100%",
                ),
                rx.center(
                    rx.spinner(
                        size="3",
                        loading=ContactState.loading_messages
                    ),
                    direction="column",
                    spacing="5",
                    width="100%",
                )
            ),
            rx.cond(
                ContactState.all_messages,
                rx.vstack(
                    rx.center(
                        rx.heading(
                            "Action Items",
                            size="6",
                            as_="h2",
                            text_align="center",
                            width="100%",
                        ),
                        direction="column",
                        spacing="5",
                        width="100%",
                    ),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Name"),
                                rx.table.column_header_cell("Email"),
                                rx.table.column_header_cell("Message"),
                                rx.table.column_header_cell("Created At"),
                                rx.table.column_header_cell("Completed?"),
                                rx.table.column_header_cell("Actions"),
                            ),
                        ),
                        rx.table.body(
                            rx.foreach(ContactState.all_messages, render_function)
                        ),
                        width="100%",
                    ),
                    spacing="6",
                    width="100%",
                ),
                rx.center(
                    rx.center(
                        rx.heading(
                            "No action items to display",
                            size="6",
                            as_="h2",
                            text_align="center",
                            width="100%",
                        ),
                        direction="column",
                        spacing="5",
                        width="100%",
                    )
                ),
            )
        ),
        max_width="90%",
        size="4",
        width="100%",
        on_mount=ContactState.get_entries
    )
