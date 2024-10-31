import reflex as rx
import bcrypt
from ..register import UserModel

class PasswordResetState(rx.State):
    old_password: str
    new_password: str
    confirm_new_password: str
    loading: bool = False

    @rx.var
    def passwords_match(self):
        return self.new_password == self.confirm_new_password

    @rx.var
    def same_as_old_password(self):
        if self.new_password:
            return self.new_password == self.old_password
        return False


    async def handle_form_submit(self, form_data):
        self.loading = True
        yield
        with rx.session() as session:
            try:
                statement = UserModel.select().where(UserModel.email==form_data["email"])
                user = session.exec(statement).one()

                print("User:", user)

                if not bcrypt.checkpw(self.old_password.encode("utf-8"), user.password.encode("utf-8")):
                    yield rx.toast.error("Current password is incorrect.", position="bottom-center")
                    return
                form_data.pop('confirm_new_password')
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(self.new_password.encode("utf-8"), salt)

                user.password = hashed_password.decode("utf-8")
                session.add(user)
                session.commit()

                yield rx.toast.success(
                    "Password changed successfully",
                    position="bottom-center"
                )
            finally:
                self.loading = False
                self.reset()
