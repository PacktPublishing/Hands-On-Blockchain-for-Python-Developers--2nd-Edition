import asyncio
import aioipfs

async def get():
    client = aioipfs.AsyncIPFS()

    cute_cat_picture = 'QmW2WQi7j6c7UgJTarActp7tDNikE4B2qXtFCfLPdsgaTQ/cat.jpg'
    await client.get(cute_cat_picture, dstdir='.')
    await client.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(get())
