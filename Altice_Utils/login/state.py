import reflex as rx
from ..register import UserModel
import bcrypt
from sqlalchemy import select
from .. import navigation
from sqlalchemy.exc import NoResultFound

class LoginState(rx.State):
    form_data: dict = {}
    current_user: UserModel | None  = None

    def logout(self):
        self.reset()
        return rx.redirect(navigation.LOGIN_ROUTE)

    @rx.var
    def is_authenticated(self):
        return self.current_user is not None

    def check_login(self):
        if not self.is_authenticated:
            return rx.redirect(navigation.LOGIN_ROUTE)

    async def handle_form_submit(self, form_data):
        self.form_data = form_data
        print(form_data)
        with rx.session() as session:
            statement = select(UserModel).where(UserModel.email == self.form_data['email'])
            try:
                user = session.exec(statement).one()[0]
            except NoResultFound as e:
                yield rx.toast.error("Invalid credentials.", position="bottom-center")
                return
            else:
                if not bcrypt.checkpw(self.form_data['password'].encode("utf-8"), user.password.encode("utf-8")):
                    yield rx.toast.error("Invalid credentials.", position="bottom-center")
                    return

            self.current_user = user
            yield rx.redirect(navigation.HOME_ROUTE)
