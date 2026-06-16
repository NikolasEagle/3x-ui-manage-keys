from dataclasses import dataclass


@dataclass
class MatrixUser:
    username: str
    prefix: str


@dataclass
class Remark:
    users: list[MatrixUser]


@dataclass
class MatrixConfig:
    HOMESERVER: str
    IDENTITY_SERVER: str
    BOT_ID: str
    BOT_PASSWORD: str
    MATRIX_STORE: str
    REMARKS: list[Remark]
