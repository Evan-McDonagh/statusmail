from dataclasses import dataclass
from datetime import datetime
from email.message import EmailMessage
import json
from requests import Response
from typing import List
from tagstripper import strip_tags

@dataclass
class OutageReport:
    domain: str
    response: Response
    time: datetime

class Email:
    def __init__(self,sender: str, recipients: List[str], subject: str, html="", text="") -> None:
        self.sender = sender
        self.recipients = recipients
        self.subject = subject
        self.html = html
        if html and not text:
            self.text = strip_tags(html)

    def dumps(self):
        return json.dumps({
            "sender": self.sender,
            "recipients": self.recipients,
            "subject": self.subject,
            "html": self.html,
            "text": self.text, 
        })


def outage_email(sender: str,recipients: str,outage_report: OutageReport):
    html = f"""<body>
  <p>This is an automated email informing you of a failed test request to {outage_report.domain}.</p>
  <ul>
    <li>Status code: {outage_report.response.status_code}</li>
    <li>Time: {outage_report.time.isoformat()}</li>
  </ul>
</body>"""
    msg = EmailMessage()
    msg.set_content(strip_tags(html))
    msg.add_alternative(html)
    msg["Subject"] = f"Error {outage_report.response.status_code} Querying ${outage_report.domain}"
    msg["From"] = sender
    msg["To"] = ', '.join(recipients)
    return msg