"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config

from . import navigation
from .home import home_page
from .contact import contact_page, contact_entries_page, ContactState
from .login import login_page, LoginState
from .register import register_page
from .fqdn import fqdn_page



app = rx.App()
app.add_page(home_page, route=navigation.HOME_ROUTE, on_load=LoginState.check_login)
app.add_page(contact_page, route=navigation.CONTACT_ROUTE, on_load=LoginState.check_login)
app.add_page(login_page, route=navigation.LOGIN_ROUTE)
app.add_page(register_page, route=navigation.REGISTER_ROUTE)
app.add_page(contact_entries_page, route=navigation.CONTACT_ENTRIES_ROUTE, on_load=LoginState.check_login)
app.add_page(fqdn_page, route=navigation.FQDN_ROUTE, on_load=LoginState.check_login)