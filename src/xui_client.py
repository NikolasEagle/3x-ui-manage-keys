from pyxui_async import (
    XUI,
    InboundResponse,
    Inbound,
    InboundSettings,
    StreamSettings,
    XhttpSettings,
)
from pyxui_async.errors import BadLogin

from models import AuthInfo, User


async def check_auth(xui: XUI, username: str, password: str) -> bool:
    try:
        await xui.login(username, password)
        print("✅ Authorization successful")
        return True
    except BadLogin:
        print("❌ Error - Authorization failed")
        return False
    except Exception as err:
        print(f"❌ Error - {err}")
        return False


async def get_clients(auth_info: AuthInfo) -> list[User] | None:
    PANEL_URL = auth_info.PANEL_URL
    USERNAME = auth_info.USERNAME
    PASSWORD = auth_info.PASSWORD
    INBOUND_ID = auth_info.ID

    xui = XUI(full_address=PANEL_URL, panel="", https=True, timeout=30)

    if await check_auth(xui=xui, username=USERNAME, password=PASSWORD):
        inbound_response = await xui.get_inbound(inbound_id=auth_info.ID)

        if not isinstance(inbound_response, InboundResponse):
            print(f"❌ Error - Bad request to get inbound {INBOUND_ID}")
            return

        if not inbound_response.success:
            print(f"❌ Error - Bad request to get inbound {INBOUND_ID}")
            return

        inbound = inbound_response.obj

        if not isinstance(inbound, Inbound):
            print(f"❌ Error - Inbound {INBOUND_ID} have no any data")
            return

        settings = inbound.settings

        if not isinstance(settings, InboundSettings):
            print(f"❌ Error - Inbound {INBOUND_ID} have no settings")
            return

        streamSettings = inbound.streamSettings

        if not isinstance(streamSettings, StreamSettings):
            print(f"❌ Error - Inbound {INBOUND_ID} have no xhttpSettings")
            return

        xhttpSettings = streamSettings.xhttpSettings

        if not isinstance(xhttpSettings, XhttpSettings):
            print(f"❌ Error - Inbound {INBOUND_ID} have no xhttpSettings")
            return

        realitySettings = streamSettings.realitySettings

        if not isinstance(realitySettings, XhttpSettings):
            print(f"❌ Error - Inbound {INBOUND_ID} have no realitySettings")
            return

        clients = settings.clients

        if not clients:
            print(f"❌ Error - Inbound {INBOUND_ID} have no clients")
            return

        print(f"📋 Count clients into inbound {INBOUND_ID}: {len(clients)})")

        users = []

        for client in clients:
            if (
                client.id is None
                or settings.encryption is None
                or xhttpSettings.path is None
                or xhttpSettings.host is None
                or xhttpSettings.mode is None
            ):
                print(f"❌ Error - Client have no data for generating key")
                return
            users.append(
                User(
                    protocol=inbound.protocol,
                    id=client.id,
                    server=PANEL_URL.replace("https://", "").split("/")[0],
                    port=inbound.port,
                    transport=streamSettings.network,
                    encryption=settings.encryption,
                    path=xhttpSettings.path,
                    host=xhttpSettings.host,
                    mode=xhttpSettings.mode,
                    security=streamSettings.security,
                    pbk=realitySettings.settings["publicKey"],
                    fp=realitySettings.settings["fingerprint"],
                    sni=realitySettings.serverNames[0],
                    sid=realitySettings.shortIds[0],
                    spx=realitySettings.settings["spiderX"],
                    pqv=realitySettings.settings["mldsa65Verify"],
                    remark=inbound.remark,
                    email=client.email,
                )
            )

        return users
    else:
        return
