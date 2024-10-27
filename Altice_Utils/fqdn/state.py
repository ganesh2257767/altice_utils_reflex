import asyncio

import reflex as rx

class FQDNState(rx.State):
    mac: str
    fqdn_name: str
    dns: list[str]
    time: str
    result_ready: bool = False
    start: bool = False

    async def handle_form_submit(self, form_data):
        print(form_data)
        self.reset_results()
        self.start = True
        yield
        # Start performing checks
        # Perform FQDN checks here (Long function)
        await asyncio.sleep(5)
        self.mac = form_data['mac']
        self.fqdn_name = "some_fqdn_name"
        self.dns = ["9595959750", "95959599754"]
        self.time = "00:30"
        self.result_ready = True
        self.start = False

    def reset_results(self):
        self.reset()

