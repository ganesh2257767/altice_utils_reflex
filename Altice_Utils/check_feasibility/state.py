import asyncio
import json
import os
import reflex as rx
from . import all_addresses
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class AddressException(Exception):
    """Raised when the address is invalid (Decided when split)."""
    pass


class CheckFeasibilityState(rx.State):
    addresses: dict = all_addresses
    env: str
    side: str
    technology: str
    address: str
    side_dropdown: list[str]
    technology_dropdown: list[str]
    addresses_dropdown: list[str]
    current_address_dict: dict
    loading: bool = False
    result: list[str]
    result_ready: bool = False


    def set_environment(self, value, set_what):
        match set_what:
            case "env":
                self.env = value
            case "side":
                self.side = value
            case "technology":
                self.technology = value

        self.current_address_dict = self.addresses[self.env]["addresses"]
        self.side_dropdown = list(self.current_address_dict.keys())
        if self.side:
            self.current_address_dict = self.current_address_dict.get(self.side)
            self.technology_dropdown = list(self.current_address_dict.keys())
        if self.technology and self.technology in self.technology_dropdown:
            self.current_address_dict = self.current_address_dict.get(self.technology)
            self.addresses_dropdown = list(self.current_address_dict)


    async def handle_form_submit_specific_address(self, form_data):
        self.result.clear()
        self.result_ready = False
        self.loading = True
        yield
        check_feasibility_response = await self.check_feasibility()
        print("Check feasibility response: ", check_feasibility_response)
        if check_feasibility_response['success']:
            self.result.extend([self.address, check_feasibility_response.get("ftthPdo", ""), check_feasibility_response.get("availability")])
            self.result_ready = True
        else:
            yield rx.toast.error(check_feasibility_response.get("errorMessage"), position="bottom-center")

        self.loading = False


    async def handle_form_submit_next_address(self, form_data):
        self.result.clear()
        self.result_ready = False
        self.loading = True
        yield

        next_available_response = await self.next_available()
        print("Next available response: ", next_available_response)
        if next_available_response['success']:
            self.result.extend([self.address, next_available_response.get("ftthPdo", ""),
                                next_available_response.get("availability")])
            self.result_ready = True
        else:
            yield rx.toast.error(next_available_response.get("errorMessage"), position="bottom-center")

        self.result_ready = True
        self.loading = False


    def format_address(self) -> tuple[str, str, str, str, str] | None:
        try:
            address: list = self.address.split()
        except AttributeError:
            raise AddressException

        if len(address) == 6:
            street_num, street_name, city, state, zipc = address[0], " ".join(
                address[1:3]), address[3], address[4], address[5]
            return street_num, street_name, city, state, zipc
        else:
            raise AddressException

    def get_token(self, get_token_url: str) -> str | dict:
        user = os.getenv("CHECK_FEASIBILITY_USER")
        password = os.getenv("CHECK_FEASIBILITY_PASSWORD")
        now = datetime.now().strftime('%a %b %d %H:%M:%S %Y')
        get_token: str = f"""{{
                            "apiName": "checkFTTHFeasibility",
                            "apiVersion": "V2",
                            "userName": "{user}",
                            "password": "{password}",
                            "sessionId": "{now}",
                            "sourceApp": "IDA"
                        }}"""
        get_token_json = json.loads(get_token)

        try:
            token_response = requests.post(
                get_token_url, json=get_token_json).json()
        except requests.exceptions.ConnectionError:
            return {"success": False, "errorMessage": "Make sure VPN is connected, or check network connection."}
        except json.decoder.JSONDecodeError:
            return {"success": False, "errorMessage": "Token generation failed!"}
        else:
            return token_response

    async def check_feasibility(self) -> dict | str:
        get_token_url = self.addresses[self.env]['get_token']
        check_feasibility_url = self.addresses[self.env]['check_feasibility']

        try:
            street_num, street_name, city, state, zipc = self.format_address()
        except AddressException:
            return {"success": False, "errorMessage": "Invalid Address."}

        token_response = self.get_token(get_token_url)
        print(token_response)

        if token_response['success']:
            check_feasibility_request = f"""{{
                                                "sessionId" : "{token_response['sessionId']}",
                                                "sourceApp" : "IDA",
                                                "token" : "{token_response['token']}",
                                                "address" : {{
                                                    "streetNumber" : "{street_num}",
                                                    "streetName" : "{street_name}",
                                                    "city" : "{city}",
                                                    "state" : "{state}",
                                                    "zipCode" : "{zipc}"
                                                }}
                                            }}"""
            check_feasibility_request_json = json.loads(check_feasibility_request)

            try:
                feasibility_response = requests.post(
                    check_feasibility_url, json=check_feasibility_request_json).json()
            except requests.exceptions.ConnectionError:
                return {"success": False, "errorMessage": "VPN or Connection Error."}

            with open('temp.json', 'w') as f:
                json.dump(feasibility_response, f, indent=4)
            return feasibility_response
        return token_response

    async def next_available(self):
        print("In next available address function")
        print(self.current_address_dict)
        addresses = [x for x in self.current_address_dict if '=' not in x]

        for address in addresses:
            self.address = address
            print(self.address)
            feasibility = await self.check_feasibility()
            print(feasibility)
            if feasibility['success']:
                av = feasibility.get("availability", 'None')
                if av == "AVAILABLE":
                    return feasibility
            else:
                return feasibility
        return {"success": False, "errorMessage": "No Ports available."}

    def reset_page(self):
        self.reset()
