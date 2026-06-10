import asyncio

from flags import extract_info_from_flags
from xui_client import get_clients
from keys import generate_keys
from files import save_file_keys


async def main():
    auth_info = extract_info_from_flags()
    clients = await get_clients(auth_info)
    if not clients:
        return
    keys = generate_keys(clients)
    success = await save_file_keys(auth_info=auth_info, keys=keys)
    if not success:
        return


if __name__ == "__main__":
    asyncio.run(main())
