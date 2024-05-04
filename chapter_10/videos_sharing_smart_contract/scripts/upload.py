from ape import accounts, project
import aioipfs
import asyncio
import os

async def add(file_path):
    client = aioipfs.AsyncIPFS()

    files = [file_path]
    hash = None
    async for added_file in client.add(files):
        hash = added_file['Hash']
    await client.close()
    return hash

def main():

    address = os.environ["VIDEO_SHARING_ADDRESS"]
    password = os.environ["VIDEO_ACCOUNT_PASSWORD"]
    account = os.environ["VIDEO_ACCOUNT"]
    deployer = accounts.load(account)
    deployer.set_autosign(True, passphrase=password)
    contract = project.VideoSharing.at(address)

    directory = '../stock_videos'
    movies = os.listdir(directory)
    for index, movie in enumerate(movies):
        movie_path = directory + '/' + movie
        loop = asyncio.get_event_loop()
        ipfs_path = loop.run_until_complete(add(movie_path))
        title = movie.rstrip('.mp4')[:19]
        contract.upload_video(ipfs_path, title, sender=deployer)
