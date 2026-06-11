from nio import AsyncClient, RoomPreset, SyncError, RoomCreateError, RoomSendError, RoomSendResponse

async def find_room(client: AsyncClient, target_user: str) -> str | bool | None:
    response = await client.sync(timeout=3000)

    if isinstance(response, SyncError):
        print(f"❌ Error - Sync: {response.message}")
        return

    for room_id, room in client.rooms.items():
        try:
            users = set(room.users.keys())
            if users == {client.user_id, target_user}:
                return room_id

        except Exception as err:
            print(f"❌ Error - Room processing: {err}")
            return
    
    return False

async def get_or_create_room(client: AsyncClient, target_user: str) -> str | None:
    room_id = await find_room(
        client,
        target_user
    )

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
    )

    if isinstance(response, RoomCreateError):
        print(f"❌ Error - Room creating")
        return
    
    print(f"✅ Room {response.room_id} with user {target_user} was created succesfull")

    return response.room_id

async def send_message(client: AsyncClient, target_user: str, text: str) -> RoomSendResponse | None:
    room_id = await get_or_create_room(
        client,
        target_user,
    )

    if room_id is None:
        return

    response = await client.room_send(
        room_id=room_id,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": text,
        },
    )

    if isinstance(response, RoomSendError):
        print(f"❌ Error - Sending message")
        return
    
    print(f"✅ Message to user {target_user} was send succesfull")

    return response