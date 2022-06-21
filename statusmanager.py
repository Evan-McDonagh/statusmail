from config import config
from custom_status_check import custom_status_check
import requests
from datetime import datetime
from dataclasses import dataclass
from requests import Response

# KNOWN STATE

# For managing known state of target domain prior to making any requests

class UpState:
    UP = "UP"
    DOWN = "DOWN"

def get_up_state() -> str:
    try:
        with open("./.upstate","r") as f:
            result = f.readlines()[0]
    except FileNotFoundError:
        with open("./.upstate","w") as f:
            result = UpState.UP
            f.write(result)
    return result

def set_up_state(state: str):
    with open("./.upstate", "w") as f:
        f.write(state)
    return

def should_email(up_state: str, ok: bool):
    return up_state == UpState.UP and not ok

def update_up_state(initial_state: str, ok: bool):
    if ok:
        if initial_state == UpState.DOWN:
            set_up_state(UpState.UP)
        return

    if initial_state == UpState.DOWN:
        return
    
    set_up_state(UpState.DOWN)
    return

# STATUS CHECKING 

@dataclass
class OutageReport:
    domain: str
    response: Response
    time: datetime

def default_status_check():
    url = f"https://{config.domain}"
    return requests.get(url)

def check_status(custom: bool):
    if not custom:
        return default_status_check()
    return custom_status_check()

def check_status_and_generate_outage_report(custom: bool):
    res = check_status(custom)
    return OutageReport(config.domain,res,datetime.now())