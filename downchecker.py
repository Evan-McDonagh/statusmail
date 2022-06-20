from datetime import datetime
import os
from config import config
from sys import argv
from custom_status_check import custom_status_check
import requests

from emails import OutageReport, outage_email

has_custom_status_check = "-c" in argv or "--custom" in argv

# Managing known state of target site

class UpState:
    UP = "UP"
    DOWN = "DOWN"

def get_up_state() -> str:
    with open("./.upstate","r") as f:
        result = f.readlines()[0]
    return result

def set_up_state(state: str):
    with open("./.upstate", "w") as f:
        f.write(state)
    return

# Status checks

def default_status_check():
    url = f"https://{config.domain}"
    return requests.get(url)

def check_status():
    if not has_custom_status_check:
        return default_status_check()
    return custom_status_check()

def check_status_and_generate_email_message():
    res = check_status()

    up_state = get_up_state()

    if res.ok:
        if up_state == UpState.DOWN:
            set_up_state(UpState.UP)
        return

    if up_state == UpState.DOWN:
        return

    set_up_state(UpState.DOWN)

    email = outage_email(
        sender=config.sender,
        recipients=config.recipients,
        outage_report=OutageReport(config.domain,res,datetime.now())
    )
    return email

def main():
    email = check_status_and_generate_email_message()
    if not email:
        return
    print(email.as_string())

if __name__ == "__main__":
    main()
