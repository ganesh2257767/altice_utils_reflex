import reflex as rx
from . import ContactModel
from sqlmodel import select

class ContactState(rx.State):
    form_data: dict
    entries: list[ContactModel] | None = None


    def get_entries(self):
        with rx.session() as session:
            self.entries = session.exec(select(ContactModel)).all()

    async def handle_form_submit(self, form_data):
        self.form_data = form_data
        with rx.session() as session:

            entry = ContactModel(
                **self.form_data
            )
            session.add(entry)
            session.commit()
        yield rx.toast.success("Message recorded successfully.", position="bottom-center")
        self.reset()
