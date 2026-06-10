import asyncio

from flags import extract_info_from_flags
from xui_client import get_clients
from keys import generate_keys


def main():
    auth_info = extract_info_from_flags()
    clients = asyncio.run(get_clients(auth_info))
    if not clients:
        return
    keys = generate_keys(clients)


if __name__ == "__main__":
    main()
