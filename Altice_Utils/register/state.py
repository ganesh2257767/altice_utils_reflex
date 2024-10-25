import reflex as rx
import bcrypt
from . import UserModel
from sqlalchemy.exc import IntegrityError
from .. import navigation
import asyncio

class RegisterState(rx.State):
    form_data: dict
    email: str
    password: str
    confirm_password: str

    @rx.var
    def passwords_match(self):
        return self.password == self.confirm_password

    @rx.var
    def valid_email(self):
        return self.email.endswith("@alticeusa.com")


    async def handle_form_submit(self, form_data):
        self.form_data = form_data
        self.form_data.pop('confirm_password')
        print(self.form_data)
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(self.password.encode("utf-8"), salt)
        self.form_data['password'] = hashed_password
        with rx.session() as session:
            try:
                user = UserModel(**self.form_data)
                session.add(user)
                session.commit()
            except IntegrityError:
                yield rx.toast.error(
                    "User already exists",
                    position="bottom-center"
                )
            else:
                yield rx.toast.success(
                    "User registered successfully",
                    position="bottom-center"
                )
            finally:
                self.reset()
