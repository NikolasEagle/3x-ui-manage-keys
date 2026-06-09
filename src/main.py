import argparse, asyncio
from pyxui_async import XUI
from pyxui_async.errors import BadLogin

import pprint


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--url", type=str, help="URL panel - http://<host>:<port>"
    )
    parser.add_argument("-U", "--username", type=str, help="Username")
    parser.add_argument("-p", "--password", type=str, help="Password")
    parser.add_argument("-i", "--id", type=int, help="Inbound ID")
    args = parser.parse_args()

    async def get_all_clients():

        PANEL_URL = args.url
        USERNAME = args.username
        PASSWORD = args.password
        INBOUND_ID = args.id

        xui = XUI(full_address=PANEL_URL, panel="", https=True, timeout=30)

        try:
            await xui.login(USERNAME, PASSWORD)
            print("✅ Authorization successful")

            inbound_response = await xui.get_inbound(inbound_id=INBOUND_ID)

            if inbound_response.success:
                inbound = inbound_response.obj
                clients = inbound.settings.clients

                if not clients:
                    print(f"❌ Error - Inbound {INBOUND_ID} nave no clients")
                    return

                print(f"📋 Count clients into inbound {INBOUND_ID}: {len(clients)})")

                for client in clients:
                    pprint.pprint(
                        {
                            "protocol": inbound.protocol,
                            "id": client.id,
                            "server": PANEL_URL.replace("https://", "").split("/")[0],
                            "port": inbound.port,
                            "transport": inbound.streamSettings.network,
                            "encryption": inbound.settings.encryption,
                            "path": inbound.streamSettings.xhttpSettings.path,
                            "host": inbound.streamSettings.xhttpSettings.host,
                            "mode": inbound.streamSettings.xhttpSettings.mode,
                            "security": inbound.streamSettings.security,
                            "pbk": inbound.streamSettings.realitySettings.settings[
                                "publicKey"
                            ],
                            "fp": inbound.streamSettings.realitySettings.settings[
                                "fingerprint"
                            ],
                            "sni": inbound.streamSettings.realitySettings.serverNames[
                                0
                            ],
                            "sid": inbound.streamSettings.realitySettings.shortIds[0],
                            "spx": inbound.streamSettings.realitySettings.settings[
                                "spiderX"
                            ],
                            "pqv": inbound.streamSettings.realitySettings.settings[
                                "mldsa65Verify"
                            ],
                            "remark": inbound.remark,
                            "email": client.email,
                        }
                    )
            else:
                print(f"❌ Error - Failed to get inbound: {inbound_response.msg}")
        except BadLogin:
            print("❌ Error - Authorization failed")
        except Exception as err:
            print(f"❌ Error - {err}")

    asyncio.run(get_all_clients())


if __name__ == "__main__":
    main()
