from dataclasses import dataclass
import json
from typing import List

@dataclass
class SMTPConfig:
    server: str
    login: str 
    password: str

@dataclass
class __Config:
    domain: str
    sender: str
    recipients: List[str]
    smtp: SMTPConfig

    @classmethod
    def from_json(cls,json: dict):
        return cls(
            domain=json["domain"],
            sender=json["sender"],
            recipients=json["recipients"],
            smtp=SMTPConfig(
                server=json["smtp"]["server"],
                login=json["smtp"]["login"],
                password=json["smtp"]["password"]
            )
        )

    @classmethod
    def from_file(cls,rel_path: str):
        with open(rel_path,"r") as f:
            data = json.load(f)
        return cls.from_json(data)

config = __Config.from_file("./config.json")