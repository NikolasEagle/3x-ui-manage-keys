from .models import User


def convert_slash(string: str) -> str:
    slash = "/"
    if slash in string:
        return string.replace(slash, "%2F")
    return string


def generate_keys(users: list[User]) -> list[str]:
    keys = []
    for user in users:
        key = (
            f"{user.protocol}://"
            f"{user.id}@{user.server}:{user.port}"
            f"?type={user.transport}"
            f"&encryption={user.encryption}"
            f"&path={convert_slash(user.path)}"
            f"&host={convert_slash(user.host)}"
            f"&mode={user.mode}"
            f"&security={user.security}"
            f"&pbk={user.pbk}"
            f"&fp={user.fp}"
            f"&sni={user.sni}"
            f"&sid={user.sid}"
            f"&spx={convert_slash(user.spx)}"
            f"&pqv={user.pqv}"
            f"#{user.remark}-{user.email}"
        )
        keys.append(key)
    return keys
