import reflex as rx
from ..register import UserModel
import bcrypt
from sqlalchemy import select
from .. import navigation
from sqlalchemy.exc import NoResultFound

class LoginState(rx.State):
    current_user: UserModel | None  = None
    loading: bool = False

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
        self.loading = True
        yield
        with rx.session() as session:
            statement = select(UserModel).where(UserModel.email == form_data['email'])
            try:
                user = session.exec(statement).one()[0]
                print("Login user: ", user)
            except NoResultFound as e:
                yield rx.toast.error("Invalid credentials.", position="bottom-center")
                self.loading = False
                yield
                return
            else:
                if not bcrypt.checkpw(form_data['password'].encode("utf-8"), user.password.encode("utf-8")):
                    self.loading = False
                    yield rx.toast.error("Invalid credentials.", position="bottom-center")
                    return

            self.current_user = user
            self.loading = False
            yield rx.redirect(navigation.HOME_ROUTE)
