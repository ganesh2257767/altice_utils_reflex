import json
import os

import reflex as rx
import requests
import xmltodict
from requests.auth import HTTPBasicAuth

from ..home import UsageModel
from ..login import LoginState


class UnlockAccountState(rx.State):
    url: str
    corp: str
    house: str
    unlock_pid: str
    unlock_opr: str
    loading: bool = False
    error_code: str
    status: str
    cdx_username: str = os.getenv("CDX_USERNAME")
    cdx_password: str = os.getenv("CDX_PASSWORD")

    urls: dict = {"QA INT": "http://cdapix-int.lab.cscqa.com:80/cdxservices/ws",
                  "QA 2": "http://cdapix-q2.lab.cscqa.com:80/cdxservices/ws",
                  "QA 3": "http://cdapix-q3.lab.cscqa.com:80/cdxservices/ws"}

    HEADERS: dict = {"Content-Type": "text/xml"}

    # After account is locked in IDA
    # 1: Query lock to get Operator and lock PID
    # 2: Once Operator and Lock PID is retreived, unlock the account using these details
    # 3: Now lock with the provisioning party (ESC/DHG or ODO)
    # 4: Complete IDA submission and check message

    body_query_lock: str = """<?xml version="1.0"?>
        <soapenv:Envelope xmlns:cab="http://www.cablevision.com/"
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <soapenv:Header/>
            <soapenv:Body>
                <cab:sendxml soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                    <application xsi:type="xsd:string">CLAWS</application>
                    <xmlReq xsi:type="xsd:string">
                        <![CDATA[<?xml version="1.0"?> <transaction>
                            <apiname>QueryLock</apiname>
                            <comcorp>{}</comcorp>
                            <house>{}</house>
                            <opr>SM2</opr>
                            </transaction>]]>
                    </xmlReq>
                </cab:sendxml>
            </soapenv:Body>
        </soapenv:Envelope>
    """

    body_unlock: str = """<?xml version="1.0"?>
        <soapenv:Envelope xmlns:cab="http://www.cablevision.com/"
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <soapenv:Header/>
            <soapenv:Body>
                <cab:sendxml soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                    <application xsi:type="xsd:string">CLAWS</application>
                    <xmlReq xsi:type="xsd:string">
                        <![CDATA[<?xml version="1.0"?> <transaction>
                            <apiname>UnLockAcct</apiname>
                            <comcorp>{}</comcorp>
                            <house>{}</house>
                            <opr>{}</opr>
                            <lockacct_pid>{}</lockacct_pid>
                            </transaction>]]>
                    </xmlReq>
                </cab:sendxml>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    body_lock: str = """<?xml version="1.0"?>
        <soapenv:Envelope xmlns:cab="http://www.cablevision.com/"
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <soapenv:Header/>
            <soapenv:Body>
                <cab:sendxml soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                    <application xsi:type="xsd:string">CLAWS</application>
                    <xmlReq xsi:type="xsd:string">
                        <![CDATA[<?xml version="1.0"?> <transaction>
                        <apiname size="40">LockAcct</apiname>
                        <comcorp size="5">{}</comcorp>
                        <house size="6">{}</house>
                        <opr size="3">{}</opr>
                        </transaction>]]>
                    </xmlReq>
                </cab:sendxml>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    async def handle_form_submit(self, form_data):
        self.loading = True
        self.status = "Querying the lock status..."
        await self.add_usage_entry()
        yield
        try:
            query_lock_response = self.query_lock(self.url, self.corp, self.house)
        except Exception as e:
            self.loading = False
            self.status = f"{type(e)}: {str(e)}"
            return
        else:
            print(query_lock_response)
            self.error_code = query_lock_response.get("errorcode")

        if self.error_code == "0":
            self.unlock_pid = query_lock_response.get("lockacct_pid")
            self.unlock_opr = query_lock_response.get("opr")
            self.status = f"Unlocking the account (Found locked by OPR: {self.unlock_opr} with PID: {self.unlock_pid}..."
            try:
                unlock_account_response = self.unlock_account()
            except Exception as e:
                self.status = f"{type(e)}: {str(e)}"
                return
            else:
                # if errorcode is 0, display message unlocked successfully
                # else print the error message
                pass
            finally:
                self.loading = False
        else:
            return

    async def add_usage_entry(self):
        login_state = await self.get_state(LoginState)
        with rx.session() as session:
            used_by = login_state.current_user.email
            usage = UsageModel(
                used_by=used_by,
                service_used="Unlock Account"
            )
            session.add(usage)
            session.commit()


    def set_env_url(self, env):
        self.url = self.urls.get(env)

    def query_lock(self, url, corp, house):
        res = requests.post(url, self.body_query_lock.format(corp, house), headers=self.HEADERS,
        auth=HTTPBasicAuth(self.cdx_username, self.cdx_password))
        final_dict = self.process_response(res)
        return final_dict


    def unlock_account(self):
        res = requests.post(self.url, self.body_unlock.format(self.corp, self.house, self.unlock_opr, self.unlock_pid),
                            headers=self.HEADERS, auth=HTTPBasicAuth(self.cdx_username, self.cdx_password))
        final_dict = self.process_response(res)
        print(final_dict)
        return final_dict

    def lock_account(self, url, corp, house, operator):
        res = requests.post(url, self.body_lock.format(corp, house, operator), headers=self.HEADERS,
                            auth=HTTPBasicAuth(self.cdx_username, self.cdx_password))
        print(res.status_code)
        return res


    @staticmethod
    def process_response(response):
        # Converting the full XML response to Dictionary
        full_response_dict = xmltodict.parse(response.content)

        # Getting the inner XML from the Dictionary
        inner_xml = full_response_dict["env:Envelope"]["env:Body"]["m:sendxmlResponse"]["result"]["#text"]

        # Converting that inner XML to dict
        inner_dict = xmltodict.parse(inner_xml)

        # Getting the required sub dict from the inner dict
        final_dict = inner_dict['transaction']
        return final_dict
