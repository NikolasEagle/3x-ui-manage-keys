import asyncio, sys

from .flags import extract_info_from_flags
from .xui_client import get_clients_keys
from .keys import generate_keys
from .files import save_file_keys
from .config import read_config


async def async_main():
    auth_info = extract_info_from_flags()
    config = read_config(auth_info=auth_info)
    if not config:
        return
    clients_keys = await get_clients_keys(auth_info=auth_info)
    if not clients_keys:
        return
    keys = generate_keys(clients_keys)
    success = await save_file_keys(auth_info=auth_info, keys=keys)
    if not success:
        return

def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("❌ Error - Interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"❌ Error - {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
