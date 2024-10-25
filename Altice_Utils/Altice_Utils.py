"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config

from . import ui
from . import navigation
from .contact import contact_page, contact_entries_page, ContactState
from .login import login_page, LoginState
from .register import register_page

def index():
    return ui.base_page(
            "Home Page",
            rx.heading("Welcome to the home page", size='4')
    )

app = rx.App()
app.add_page(index, route=navigation.HOME_ROUTE, on_load=LoginState.check_login)
app.add_page(contact_page, route=navigation.CONTACT_ROUTE)
app.add_page(login_page, route=navigation.LOGIN_ROUTE)
app.add_page(register_page, route=navigation.REGISTER_ROUTE)
app.add_page(contact_entries_page(), route=navigation.CONTACT_ENTRIES_ROUTE, on_load=ContactState.populate_contact_entries)