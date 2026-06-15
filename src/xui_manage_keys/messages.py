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
)

import logging

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
    client: AsyncClient, target_user: str, text: str
) -> RoomSendResponse | None:
    room_id = await get_or_create_room(client, target_user)

    if room_id is None:
        return

    sync_response = await client.sync(timeout=1000)
    if isinstance(sync_response, SyncError):
        print(f"❌ Error - Sync failed: {sync_response.message}")
        return

    response = await client.room_send(
        room_id=room_id,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": text,
        },
        ignore_unverified_devices=True,
    )

    if isinstance(response, RoomSendError):
        print(f"❌ Error - Sending message")
        return

    print(f"✅ Message to user {target_user} was send succesfull")

    return response


async def sendKey(
    homeserver: str,
    bot_id: str,
    password: str,
    target_user: str,
    message: str,
    matrix_store: str,
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

    result = await send_message(client, target_user, message)

    if result is None:
        print("❌ Error - Message sending failed")
        await client.logout()
        await client.close()
        return

    await client.logout()
    await client.close()
    return True
