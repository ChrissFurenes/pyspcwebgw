import asyncio
import aiohttp

from aiohttp import DigestAuthMiddleware
from pyspcwebgw import SpcWebGateway

API_URL = "http://192.168.1.10:8088"
WS_URL = "http://192.168.1.10:8088"

GET_USER = "get_user"
GET_PASS = "get_pwd"

async def callback(entity):
    print("SPC update:", entity)

async def main():
    digest_auth = DigestAuthMiddleware(
        login=GET_USER,
        password=GET_PASS,
    )

    async with aiohttp.ClientSession(
        middlewares=(digest_auth,)
    ) as websession:
        spc = SpcWebGateway(
            asyncio.get_running_loop(),
            websession,
            api_url=API_URL,
            ws_url=WS_URL,
            async_callback=callback,
        )

        result = await spc.async_load_parameters()

        if result is False:
            print("Failed to connect to SPC Web Gateway")
            return

        print("Connected")
        print(spc.info)
        print(spc.areas)

asyncio.run(main())