import reflex as rx
from . import ContactModel
from typing import List
from sqlmodel import select

class ContactState(rx.State):
    form_data: dict
    entries: List['ContactModel'] = []
    async def handle_form_submit(self, form_data):
        self.form_data = form_data
        print(form_data)
        with rx.session() as session:

            entry = ContactModel(
                **form_data
            )
            session.add(entry)
            session.commit()
            yield rx.toast.success("Contact request successful.", position="bottom-center")

    def populate_contact_entries(self):
        with rx.session() as session:
            statement = select(ContactModel)
            entries = session.exec(statement).all()
            self.entries = entries
            print(self.entries)

