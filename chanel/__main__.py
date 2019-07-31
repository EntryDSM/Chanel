import asyncio

from sys import argv

import uvloop

from chanel.app import create_app

if __name__ == "__main__" and len(argv) == 4:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    app = create_app()
    app.run(host=argv[1], port=argv[2], debug=argv[3])
