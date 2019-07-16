import asyncio
import uvloop

from chanel.app import create_app
from chanel.setting import SETTINGS
from chanel.vault import VaultClient

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    VaultClient.initialize()

    app = create_app()

    app.run(host=SETTINGS.RUN_HOST, port=SETTINGS.RUN_PORT, debug=SETTINGS.DEBUG)
