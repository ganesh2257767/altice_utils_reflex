import asyncio
import threading
import time
import random
import reflex as rx
from ..home import UsageModel
from ..login import LoginState


class FQDNState(rx.State):
    mac: str
    fqdn_name: str
    dns: list[str]
    result_ready: bool = False
    start: bool = False
    status: str
    time: int = 0
    time_str: str

    def long_function(self, mac):
        time.sleep(random.randint(5, 15))
        self.status = "Done!"
        self.mac = mac
        self.fqdn_name = "some_fqdn_name"
        self.dns = ["9595959750", "95959599754"]
        self.result_ready = True
        self.start = False

    async def handle_form_submit(self, form_data):
        print(form_data)
        self.reset_results()
        self.start = True
        self.time_str = "00:00"
        yield
        t = threading.Thread(target=self.long_function, args=(form_data['mac'],))
        t.start()
        while self.start:
            await asyncio.sleep(1)
            self.time += 1
            m, s = divmod(self.time, 60)
            self.time_str = f"{m:0>2}:{s:0>2}"
            yield
        await self.add_usage_entry()
        self.status = "Done"
        t.join()
        yield

    async def add_usage_entry(self):
        login_state = await self.get_state(LoginState)
        with rx.session() as session:
            used_by = login_state.current_user.email
            usage = UsageModel(
                used_by=used_by,
                service_used="FQDN"
            )
            session.add(usage)
            session.commit()


    def reset_results(self):
        self.reset()
