import asyncio
import aioipfs

async def add_file():
    client = aioipfs.AsyncIPFS()

    files = ['hello.txt']
    async for added_file in client.add(files):
        print('Imported file {0}, CID: {1}'.format(
            added_file['Name'], added_file['Hash']))
    await client.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(add_file())
