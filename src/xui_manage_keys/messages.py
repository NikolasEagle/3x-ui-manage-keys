from nio import (
    AsyncClient,
    AsyncClientConfig,
    EnableEncryptionBuilder,
    LoginError,
    RoomPreset,
    SyncError,
    RoomCreateError,
    RoomSendError,
    RoomSendResponse,
    UploadError,
)

import logging, aiofiles, os, magic, io

logging.getLogger("nio.crypto").setLevel(logging.CRITICAL)


async def find_room(client: AsyncClient, target_user: str) -> str | bool | None:
    sync_response = await client.sync(timeout=3000)

    if isinstance(sync_response, SyncError):
        print(f"❌ Error - Sync failed: {sync_response.message}")
        return

    for room_id, room in client.rooms.items():
        try:
            users = set(room.users.keys())
            if users == {client.user, target_user}:
                return room_id

        except Exception as err:
            print(f"❌ Error - Room processing: {err}")
            return

    return False


async def get_or_create_room(client: AsyncClient, target_user: str) -> str | None:
    room_id = await find_room(client, target_user)

    if room_id is None:
        return

    if type(room_id) == str:
        print(f"✅ Room {room_id} with user {target_user} is found")
        return room_id

    print(f"⚠️ Room with user {target_user} is not found, create new a room")

    response = await client.room_create(
        invite=[target_user],
        is_direct=True,
        preset=RoomPreset.trusted_private_chat,
        initial_state=[EnableEncryptionBuilder().as_dict()],
    )

    if isinstance(response, RoomCreateError):
        print(f"❌ Error - Room creating")
        return

    print(f"✅ Room {response.room_id} with user {target_user} was created succesfull")

    return response.room_id


async def send_message(
    client: AsyncClient, room_id: str, target_user: str, message: str
) -> RoomSendResponse | None:

    response = await client.room_send(
        room_id=room_id,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": message,
        },
        ignore_unverified_devices=True,
    )

    if isinstance(response, RoomSendError):
        print(f"❌ Error - Sending message")
        return

    print(f"✅ Message to user {target_user} was send succesfull")

    return response


async def send_file(
    client: AsyncClient,
    room_id: str,
    target_user: str,
    file_path: str,
) -> RoomSendResponse | None:

    try:
        mime_type = magic.from_file(file_path, mime=True)
        filename = os.path.basename(file_path)
        filesize = os.path.getsize(file_path)

        async with aiofiles.open(file_path, "rb") as f:
            file_data = await f.read()

        file_obj = io.BytesIO(file_data)

        upload_response, _ = await client.upload(
            data_provider=file_obj,
            content_type=mime_type,
            filename=filename,
            filesize=filesize,
        )

        if isinstance(upload_response, UploadError):
            print("❌ Error - File upload failed")
            return

        content = {
            "body": filename,
            "msgtype": "m.file",
            "filename": filename,
            "url": upload_response.content_uri,
        }

        response = await client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content=content,
            ignore_unverified_devices=True,
        )

        if isinstance(response, RoomSendError):
            print(f"❌ Error - Sending file")
            return

        print(f"✅ File to user {target_user} was send succesfull")

        return response

    except PermissionError:
        print(f"❌ Error - No permissions for writing")
    except OSError as err:
        print(f"❌ Error - OS error: {err}")
    except Exception as err:
        print(f"❌ Error - {err}")
    return


async def send_key(
    homeserver: str,
    bot_id: str,
    password: str,
    target_user: str,
    message: str,
    matrix_store: str,
    file_path: str,
) -> bool | None:
    сonfig = AsyncClientConfig(
        max_limit_exceeded=0,
        max_timeouts=0,
        store_sync_tokens=True,
        encryption_enabled=True,
    )
    client = AsyncClient(
        homeserver=homeserver,
        user=bot_id,
        store_path=matrix_store,
        config=сonfig,
    )

    response = await client.login(password)

    if isinstance(response, LoginError):
        print(f"❌ Error - Login failed: {response.message}")
        await client.close()
        return

    print("✅ Login successful")

    room_id = await get_or_create_room(client, target_user)

    if room_id is None:
        return

    sync_response = await client.sync(timeout=1000)
    if isinstance(sync_response, SyncError):
        print(f"❌ Error - Sync failed: {sync_response.message}")
        return

    result_message = await send_message(
        client=client, room_id=room_id, target_user=target_user, message=message
    )

    if result_message is None:
        await client.logout()
        await client.close()
        return

    result_file = await send_file(
        client=client, room_id=room_id, target_user=target_user, file_path=file_path
    )

    if result_file is None:
        await client.logout()
        await client.close()
        return

    await client.logout()
    await client.close()
    return True
