import pprint

import aiofiles, aiofiles.os
from .models import AuthInfo, User, Key, MatrixConfig


async def check_file(filepath: str, filename: str) -> str | None:
    try:
        full_path = f"{filepath}/{filename}"
        exists = await aiofiles.os.path.isfile(full_path)
        if not exists:
            print(f"❌ Error - File not found")
            return
        return full_path
    except PermissionError:
        print(f"❌ Error - No permissions for reading {filepath}")
    except OSError as err:
        print(f"❌ Error - OS error: {err}")
    except Exception as err:
        print(f"❌ Error - {err}")
    return


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


async def distribute_keys(
    auth_info: AuthInfo, config: MatrixConfig, keys: list[Key]
) -> list[User] | None:
    filepath = auth_info.OUTPUT
    remark = keys[0].remark
    matrix_users = config.remarks[remark].users
    users = []
    for key in keys:
        for matrix_user in matrix_users:
            if matrix_user.prefix == f"{key.email.split("_")[0]}_":
                if (
                    not User(
                        username=matrix_user.name, prefix=matrix_user.prefix, keys=[]
                    )
                    in users
                ):
                    users.append(
                        User(
                            username=matrix_user.name,
                            prefix=matrix_user.prefix,
                            keys=[],
                        )
                    )
    for key in keys:
        for user in users:
            if user.prefix == f"{key.email.split("_")[0]}_":
                filename = f"{key.remark}-{key.email}.txt"
                fullpath = await check_file(filepath=filepath, filename=filename)
                if fullpath is None:
                    return
                user.keys.append(fullpath)

    return users
