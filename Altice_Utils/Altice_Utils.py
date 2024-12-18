"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from . import navigation
from .check_feasibility import check_feasibility_page
from .contact import contact_page, contact_entries_page
from .fqdn import fqdn_page
from .home import home_page
from .login import login_page, LoginState
from .password_reset import password_reset_page
from .register import register_page
from .unlock_account import unlock_account_page

app = rx.App()
app.add_page(home_page, route=navigation.HOME_ROUTE, on_load=LoginState.check_login)
app.add_page(login_page, route=navigation.LOGIN_ROUTE)
app.add_page(register_page, route=navigation.REGISTER_ROUTE)
app.add_page(contact_page, route=navigation.CONTACT_ROUTE, on_load=LoginState.check_login)
app.add_page(contact_entries_page, route=navigation.CONTACT_ENTRIES_ROUTE, on_load=LoginState.check_login)
app.add_page(fqdn_page, route=navigation.FQDN_ROUTE, on_load=LoginState.check_login)
app.add_page(password_reset_page, route=navigation.PASSWORD_RESET_ROUTE, on_load=LoginState.check_login)
app.add_page(unlock_account_page, route=navigation.UNLOCK_ACCOUNT_ROUTE, on_load=LoginState.check_login)
app.add_page(check_feasibility_page, route=navigation.CHECK_FEASIBILITY_ROUTE, on_load=LoginState.check_login)
