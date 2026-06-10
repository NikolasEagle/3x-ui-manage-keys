import aiofiles
from .models import AuthInfo


async def save_file(filepath: str, filename: str, content: str) -> bool:
    try:
        async with aiofiles.open(f"{filepath}/{filename}", "w", encoding="utf-8") as f:
            await f.write(content)
        return True
    except PermissionError:
        print(f"❌ Error - No permissions for writing")
    except OSError as err:
        print(f"❌ Error - OS error: {err}")
    except Exception as err:
        print(f"❌ Error - {err}")
    return False


async def save_file_keys(auth_info: AuthInfo, keys: list[str]) -> bool | None:
    filepath = auth_info.OUTPUT
    for key in keys:
        filename = f'{key.split("#")[-1].replace("\n", "")}.txt'
        success = await save_file(filepath, filename, key)
        if not success:
            return
    print(
        f"✅ Success! - {len(keys)} keys were saved successful into directory {filepath}"
    )
    return True
