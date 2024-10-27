import reflex as rx
from . import fqdn_form, fqdn_table, FQDNState
from .. import ui


def fqdn_page():
    return ui.base_page(
        fqdn_form(),
        rx.cond(
            FQDNState.result_ready,
            fqdn_table(),
        )
    )
