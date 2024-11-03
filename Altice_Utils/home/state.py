import reflex as rx
from sqlmodel import select
from . import UsageModel


class UsageState(rx.State):
    usages: list[dict]

    async def get_usage_data(self):
        from ..login import LoginState
        login_state = await self.get_state(LoginState)
        self.reset()

        with rx.session() as session:
            statement = select(UsageModel).where(UsageModel.used_by == login_state.current_user.email).where(UsageModel.service_used == "FQDN")
            fqdn_count = session.exec(statement).all()

            statement2 = select(UsageModel).where(UsageModel.used_by == login_state.current_user.email).where(UsageModel.service_used == "Unlock Account")
            unlock_count = session.exec(statement2).all()

            statement3 = select(UsageModel).where(UsageModel.used_by == login_state.current_user.email).where(UsageModel.service_used.contains("Next"))
            next_count = session.exec(statement3).all()

            statement3 = select(UsageModel).where(UsageModel.used_by == login_state.current_user.email).where(UsageModel.service_used.contains("Specific"))
            specific_count = session.exec(statement3).all()

            statement4 = select(UsageModel).where(UsageModel.used_by == login_state.current_user.email).where(
                UsageModel.service_used.contains("Netwin"))
            netwin_count = session.exec(statement4).all()

            self.usages.extend([
                {"service": "FQDN", "count": len(fqdn_count), "fill": "var(--crimson-9)"},
                {"service": "Unlock Account", "count": len(unlock_count), "fill": "var(--sky-11)"},
                {"service": "Next Available", "count": len(next_count), "fill": "var(--purple-11)"},
                {"service": "Specific Address", "count": len(specific_count), "fill": "var(--teal-11)"},
                {"service": "Netwin Helper", "count": len(netwin_count), "fill": "var(--orange-11)"},
            ])
            print(self.usages)
            print()