import os.path, json
import asyncio
import aioipfs
import cv2
import os
from ape import accounts, Contract, project
from ape import networks
from ethpm_types import ContractType
from ape_ethereum.transactions import Receipt
from web3 import Web3, IPCProvider
from decentralized_videos.settings import STATICFILES_DIRS, STATIC_URL, BASE_DIR, MEDIA_ROOT

BLOCKCHAIN_NETWORK = "local"
BLOCKCHAIN_PROVIDER = "geth"

async def get(ipfs_path, download_path):
    client = aioipfs.AsyncIPFS()

    await client.get(ipfs_path, dstdir=download_path)
    await client.close()

async def add(file_path):
    client = aioipfs.AsyncIPFS()

    files = [file_path]
    hash = None
    async for added_file in client.add(files):
        hash = added_file['Hash']
    await client.close()
    return hash

class VideosSharing:

    def __init__(self):
        self.w3 = Web3(IPCProvider('/tmp/geth.ipc'))
        self.address = Web3.to_checksum_address(os.environ["VIDEO_SHARING_ADDRESS"])

        with open('../videos_sharing_smart_contract/.build/VideoSharing.json') as f:
            contract = json.load(f)
            self.abi = contract['abi']

    def recent_videos(self, amount=20):
        with networks.ethereum[BLOCKCHAIN_NETWORK].use_provider(BLOCKCHAIN_PROVIDER):
            ct = ContractType.parse_obj({"abi": self.abi})
            self.SmartContract = Contract(self.address, ct)
            events = self.SmartContract.UploadVideo.query("*", start_block=0)

        videos = []
        for event in events["event_arguments"]:
            video = {}
            video['user'] = event['_user']
            video['index'] = event['_index']
            video['path'] = self.get_video_path(video['user'], video['index'])
            video['title'] = self.get_video_title(video['user'], video['index'])
            video['thumbnail'] = self.get_video_thumbnail(video['path'])
            videos.append(video)
        videos.reverse()
        return videos[:amount]

    def get_video_path(self, user, index):
        with networks.ethereum[BLOCKCHAIN_NETWORK].use_provider(BLOCKCHAIN_PROVIDER):
            ct = ContractType.parse_obj({"abi": self.abi})
            self.SmartContract = Contract(self.address, ct)
            return self.SmartContract.videos_path(user, index)

    def get_video_title(self, user, index):
        with networks.ethereum[BLOCKCHAIN_NETWORK].use_provider(BLOCKCHAIN_PROVIDER):
            ct = ContractType.parse_obj({"abi": self.abi})
            self.SmartContract = Contract(self.address, ct)
            return self.SmartContract.videos_title(user, index)

    def get_video_thumbnail(self, ipfs_path):
        thumbnail_file = str(STATICFILES_DIRS[0]) + '/' + ipfs_path + '.png'
        url_file = STATIC_URL + '/' + ipfs_path + '.png'
        print(thumbnail_file)

        if os.path.isfile(thumbnail_file):
            return url_file
        else:
            return "https://bulma.io/images/placeholders/640x480.png"

    def get_video(self, user, index):
        video = {}
        ipfs_path = self.get_video_path(user, index)
        video_title = self.get_video_title(user, index)
        video_file = str(STATICFILES_DIRS[0]) + '/' + ipfs_path + '.mp4'
        thumbnail_file = str(STATICFILES_DIRS[0]) + '/' + ipfs_path + '.png'
        video['title'] = video_title
        video['user'] = user
        video['index'] = index
        with networks.ethereum[BLOCKCHAIN_NETWORK].use_provider(BLOCKCHAIN_PROVIDER):
            ct = ContractType.parse_obj({"abi": self.abi})
            self.SmartContract = Contract(self.address, ct)
            video['aggregate_likes'] = self.SmartContract.video_aggregate_likes(user, index)

        if os.path.isfile(video_file):
            video['url'] = STATIC_URL + '/' + ipfs_path + '.mp4'
        else:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(get(ipfs_path, get(str(BASE_DIR))))
            video['url'] = STATIC_URL + '/' + ipfs_path + '.mp4'

        if not os.path.isfile(thumbnail_file):
            self.process_thumbnail(ipfs_path)

        return video

    def upload_video(self, video_user, password, video_file, title):
        video_path = str(MEDIA_ROOT) + '/video.mp4'
        with open(video_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
        loop = asyncio.get_event_loop()
        ipfs_path = loop.run_until_complete(add(video_path))
        title = title[:19]
        with networks.ethereum[BLOCKCHAIN_NETWORK].use_provider(BLOCKCHAIN_PROVIDER):
            ct = ContractType.parse_obj({"abi": self.abi})
            self.SmartContract = Contract(self.address, ct)
            sender = accounts.load(video_user)
            sender.set_autosign(True, passphrase=password)
            self.SmartContract.upload_video(ipfs_path, title, sender=sender)

    def process_thumbnail(self, ipfs_path):
        thumbnail_file = str(STATICFILES_DIRS[0]) + '/' + ipfs_path + '.png'
        if not os.path.isfile(thumbnail_file):
            video_path = str(STATICFILES_DIRS[0]) + '/' + ipfs_path + '.mp4'
            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            _, frame = cap.read()
            cv2.imwrite(thumbnail_file, frame)

    def like_video(self, video_liker, password, video_user, index):
        with networks.ethereum[BLOCKCHAIN_NETWORK].use_provider(BLOCKCHAIN_PROVIDER):
            ct = ContractType.parse_obj({"abi": self.abi})
            self.SmartContract = Contract(self.address, ct)
            sender = accounts.load(video_liker)
            if self.SmartContract.video_has_been_liked(sender.address, video_user, index):
                return
            sender.set_autosign(True, passphrase=password)
            self.SmartContract.like_video(video_user, index, sender=sender)


videos_sharing = VideosSharing()
