from dataclasses import dataclass


@dataclass
class AuthInfo:
    PANEL_URL: str
    USERNAME: str
    PASSWORD: str
    ID: int
    OUTPUT: str
    CONFIG: str
