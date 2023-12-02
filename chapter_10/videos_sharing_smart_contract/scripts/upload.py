from ape import accounts, project
import ipfshttpclient
import os


def main():
    c = ipfshttpclient.connect()

    address = os.environ["VIDEO_SHARING_ADDRESS"]
    password = os.environ["VIDEO_ACCOUNT_PASSWORD"]
    deployer = accounts.load("video")
    deployer.set_autosign(True, passphrase=password)
    contract = project.VideoSharing.at(address)

    directory = '../stock_videos'
    movies = os.listdir(directory)
    for index, movie in enumerate(movies):
        ipfs_add = c.add(directory + '/' + movie)
        ipfs_path = ipfs_add['Hash']
        title = movie.rstrip('.mp4')[:19]
        contract.upload_video(ipfs_path, title, sender=deployer)
