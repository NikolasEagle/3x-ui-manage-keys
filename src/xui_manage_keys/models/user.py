from dataclasses import dataclass


@dataclass
class Key:
    protocol: str
    id: str
    server: str
    port: int
    transport: str
    encryption: str
    path: str
    host: str
    mode: str
    security: str
    pbk: str
    fp: str
    sni: str
    sid: str
    spx: str
    pqv: str
    remark: str
    email: str


@dataclass
class User:
    username: str
    prefix: str
    keys: list[Key]
