from datetime import datetime

import reflex as rx
from sqlmodel import select

from . import ContactModel
from ..login import LoginState
from ..register import UserModel


class UserMessage(rx.Base):
    id: int
    name: str
    email: str
    message: str
    created_at: datetime
    completed: bool


class ContactState(rx.State):
    form_data: dict
    all_messages: list[UserMessage] = []

    def get_entries(self):
        self.all_messages.clear()
        with rx.session() as session:
            statement = select(UserModel, ContactModel).where(UserModel.email == ContactModel.created_by)
            list_user_messages = session.exec(statement).all()

        for user, message in list_user_messages:
            self.all_messages.append(
                UserMessage(
                    id=message.id,
                    name=f"{user.first_name} {user.last_name}",
                    email=user.email,
                    message=message.message,
                    created_at=message.created_at,
                    completed=message.completed)
            )

    def complete_entry(self, id_: int):
        with rx.session() as session:
            statement = select(ContactModel).where(ContactModel.id == id_)
            message: ContactModel = session.exec(statement).one()
            message.completed = True
            session.commit()
        yield rx.toast.info("Message marked as complete", position="bottom-center")
        self.get_entries()

    def undo_complete_entry(self, id_: int):
        with rx.session() as session:
            statement = select(ContactModel).where(ContactModel.id == id_)
            message: ContactModel = session.exec(statement).one()
            message.completed = False
            session.commit()
        yield rx.toast.info("Message marked as not complete", position="bottom-center")
        self.get_entries()

    def delete_entry(self, id_: int):
        with rx.session() as session:
            statement = select(ContactModel).where(ContactModel.id == id_)
            message: ContactModel = session.exec(statement).one()
            session.delete(message)
            session.commit()
        yield rx.toast.info("Message deleted successfully", position="bottom-center")
        self.get_entries()

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
