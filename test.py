import asyncio

from mpets import MpetsApi

async def main():
    mpets = MpetsApi()
    r = await mpets.start(password="asd", type="1")
    print(r)
    g = await mpets.test_s()
    print(g)


asyncio.run(main())