from .. import ui
from . import check_feasibility_form, CheckFeasibilityState, check_feasibility_table
import reflex as rx

def check_feasibility_page():
    return ui.base_page(
        check_feasibility_form(),
        rx.cond(
            CheckFeasibilityState.result_ready,
            check_feasibility_table(),
        )
    )
