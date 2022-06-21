from email.message import EmailMessage
from email.headerregistry import Address
import smtplib
import re
from typing import Tuple
from config import SMTPConfig
from statusmanager import OutageReport
from html.parser import HTMLParser
from io import StringIO

class TagStripper(HTMLParser):
    '''Strips HTML tags from string'''
    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, data: str) -> None:
        self.text.write(data)

    def get_data(self):
        return self.text.getvalue()

def strip_tags(html: str):
    s = TagStripper()
    s.feed(html)
    return s.get_data()

def outage_email(sender: str,recipients: Tuple[str],outage_report: OutageReport):
    html = f"""\
<html>
    <head></head>
    <body>
      <p>This is an automated email informing you of a failed test request to {outage_report.domain}.</p>
      <ul>
        <li>Status code: {outage_report.response.status_code}</li>
        <li>Time: {outage_report.time.isoformat()}</li>
      </ul>
    </body>
</html>    
"""
    msg = EmailMessage()
    msg.set_content(strip_tags(html))
    msg.add_alternative(html,subtype="html")
    msg["Subject"] = f"Error {outage_report.response.status_code} Querying {outage_report.domain}"
    msg["From"] = parse_address(sender)
    msg["To"] = tuple(map(parse_address,recipients))
    return msg

def parse_address(address_string: str):
    display_name_match = re.match("<(.*?)>",address_string)
    email_address_match = re.search(">(.*)",address_string)

    if not display_name_match and not email_address_match:
        username, domain = address_string.split("@")
        return Address(username=username, domain=domain)
    
    display_name = display_name_match.groups()[0]
    email_address = email_address_match.group().strip()
    username, domain = email_address.split("@")
    return Address(display_name=display_name,username=username,domain=domain)


def send_message(smtp_config: SMTPConfig,message: EmailMessage):
    sender_address = message["From"]
    receiver_address = message["To"]
    
    session = smtplib.SMTP(smtp_config.server, 587)
    session.starttls()
    session.login(smtp_config.login,smtp_config.password)

    session.sendmail(sender_address,receiver_address,message.as_string())

    session.quit()