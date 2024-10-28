import reflex as rx


class UnlockAccountState(rx.State):

    def handle_form_submit(self, form_data):
        print(form_data)
