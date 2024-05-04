import asyncio
import aioipfs

async def cat_file():
    client = aioipfs.AsyncIPFS()

    hash = 'QmY7MiYeySnsed1Z3KxqDVYuM8pfiT5gGTqprNaNhUpZgR'
    result = await client.cat(hash)
    print(result)
    await client.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(cat_file())
