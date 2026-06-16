from dataclasses import dataclass


@dataclass
class MatrixUser:
    name: str
    prefix: str


@dataclass
class Remark:
    users: list[MatrixUser]


@dataclass
class MatrixConfig:
    homeserver: str
    identity_server: str
    bot_id: str
    bot_password: str
    matrix_store: str
    remarks: dict[str, Remark]
