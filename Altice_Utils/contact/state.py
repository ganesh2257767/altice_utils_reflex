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
    loading_submit: bool = False
    loading_messages: bool = False
    loading_complete: bool = False
    loading_incomplete: bool = False
    loading_delete: bool = False

    def get_entries(self):
        self.loading_messages = True
        yield

        if not self.all_messages:
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
        self.loading_messages = False


    def complete_entry(self, id_: int):
        self.loading_complete = True
        yield
        with rx.session() as session:
            statement = select(ContactModel).where(ContactModel.id == id_)
            message: ContactModel = session.exec(statement).one()
            for message_instance in self.all_messages:
                if message_instance.id == id_:
                    message_instance.completed = True
            message.completed = True
            session.add(message)
            session.commit()
        yield rx.toast.info("Message marked as complete", position="bottom-center")
        self.loading_complete = False

    def undo_complete_entry(self, id_: int):
        self.loading_incomplete = True
        yield
        with rx.session() as session:
            statement = select(ContactModel).where(ContactModel.id == id_)
            message: ContactModel = session.exec(statement).one()
            for message_instance in self.all_messages:
                if message_instance.id == id_:
                    message_instance.completed = False
            message.completed = False
            session.add(message)
            session.commit()
        self.loading_incomplete = False
        yield rx.toast.info("Message marked as not complete", position="bottom-center")

    def delete_entry(self, id_: int):
        self.loading_delete = True
        yield
        with rx.session() as session:
            statement = select(ContactModel).where(ContactModel.id == id_)
            message: ContactModel = session.exec(statement).one()
            for message_instance in self.all_messages:
                if message_instance.id == id_:
                    self.all_messages.remove(message_instance)
            session.delete(message)
            session.commit()
        self.loading_delete = False
        yield rx.toast.info("Message deleted successfully", position="bottom-center")

    async def handle_form_submit(self, form_data):
        self.loading_submit = True
        yield
        self.form_data = form_data
        with rx.session() as session:
            entry = ContactModel(
                **self.form_data
            )
            session.add(entry)
            session.commit()
        self.reset()
        self.all_messages.clear()
        self.loading_submit = False
        yield rx.toast.success("Message recorded successfully.", position="bottom-center")
