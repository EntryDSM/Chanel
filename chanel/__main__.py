import asyncio

import uvloop

from chanel.app import create_app
from chanel.common.client.vault import VaultClient, settings

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    VaultClient.initialize()

    app = create_app()
    app.run(host=settings.RUN_HOST, port=settings.RUN_PORT, debug=settings.DEBUG)
