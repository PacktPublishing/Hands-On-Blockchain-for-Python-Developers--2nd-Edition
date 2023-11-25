import pytest
from ape.exceptions import ContractLogicError

def upload_video(contract, account, video_path, video_title):
    contract.upload_video(video_path, video_title, sender=account)

def transfer_coins(contract, source, destination, amount):
    contract.transfer(destination, amount, sender=source)

def like_video(contract, video_liker, video_uploader, index):
    contract.like_video(video_uploader, index, sender=video_liker)

def test_upload_video(contract, deployer):
    video_sharing = contract

    video_uploader = deployer

    index = video_sharing.latest_videos_index(video_uploader)
    assert index == 0

    upload_video(video_sharing, video_uploader, 'video-ipfs-path', "video title")

    index = video_sharing.latest_videos_index(video_uploader)
    path = video_sharing.videos_path(video_uploader, 0)
    title = video_sharing.videos_title(video_uploader, 0)
    assert index == 1
    assert path == 'video-ipfs-path'
    assert title == "video title"

    upload_video(video_sharing, video_uploader, 'video-ipfs-path2', "video title2")

    index = video_sharing.latest_videos_index(video_uploader)
    path = video_sharing.videos_path(video_uploader, 1)
    title = video_sharing.videos_title(video_uploader, 1)
    assert index == 2
    assert path == 'video-ipfs-path2'
    assert title == "video title2"

    events = video_sharing.UploadVideo.query("*", start_block=-1)

    assert events["event_arguments"][0]["_user"] == video_uploader
    assert events["event_arguments"][0]["_index"] == 0

    assert events["event_arguments"][1]["_user"] == video_uploader
    assert events["event_arguments"][1]["_index"] == 1

def test_like_video(contract, accounts):
    video_sharing = contract

    manager = accounts[0]
    video_uploader = accounts[1]
    video_liker = accounts[2]
    video_liker2 = accounts[3]

    transfer_coins(video_sharing, manager, video_liker, 100)
    transfer_coins(video_sharing, manager, video_liker2, 100)
    transfer_coins(video_sharing, manager, video_uploader, 50)
    upload_video(video_sharing, video_uploader, 'video-ipfs-path', "video title")

    liked = video_sharing.video_has_been_liked(video_liker, video_uploader, 0)
    assert liked == False
    liked2 = video_sharing.video_has_been_liked(video_liker2, video_uploader, 0)
    assert liked2 == False
    video_uploader_balance = video_sharing.balanceOf(video_uploader)
    assert video_uploader_balance == 50
    video_liker_balance = video_sharing.balanceOf(video_liker)
    assert video_liker_balance == 100
    video_liker2_balance = video_sharing.balanceOf(video_liker2)
    assert video_liker2_balance == 100
    aggregate_likes = video_sharing.video_aggregate_likes(video_uploader, 0)
    assert aggregate_likes == 0

    like_video(video_sharing, video_liker, video_uploader, 0)

    liked = video_sharing.video_has_been_liked(video_liker, video_uploader, 0)
    assert liked == True
    liked2 = video_sharing.video_has_been_liked(video_liker2, video_uploader, 0)
    assert liked2 == False
    video_uploader_balance = video_sharing.balanceOf(video_uploader)
    assert video_uploader_balance == 51
    video_liker_balance = video_sharing.balanceOf(video_liker)
    assert video_liker_balance == 99
    video_liker2_balance = video_sharing.balanceOf(video_liker2)
    assert video_liker2_balance == 100
    aggregate_likes = video_sharing.video_aggregate_likes(video_uploader, 0)
    assert aggregate_likes == 1

    like_video(video_sharing, video_liker2, video_uploader, 0)

    liked = video_sharing.video_has_been_liked(video_liker2, video_uploader, 0)
    assert liked == True
    liked2 = video_sharing.video_has_been_liked(video_liker2, video_uploader, 0)
    assert liked2 == True
    video_uploader_balance = video_sharing.balanceOf(video_uploader)
    assert video_uploader_balance == 52
    video_liker_balance = video_sharing.balanceOf(video_liker)
    assert video_liker_balance == 99
    video_liker2_balance = video_sharing.balanceOf(video_liker2)
    assert video_liker2_balance == 99
    aggregate_likes = video_sharing.video_aggregate_likes(video_uploader, 0)
    assert aggregate_likes == 2

    events = video_sharing.LikeVideo.query("*", start_block=-1)

    assert events["event_arguments"][0]["_video_liker"] == video_liker
    assert events["event_arguments"][0]["_video_uploader"] == video_uploader
    assert events["event_arguments"][0]["_index"] == 0

    assert events["event_arguments"][1]["_video_liker"] == video_liker2
    assert events["event_arguments"][1]["_video_uploader"] == video_uploader
    assert events["event_arguments"][1]["_index"] == 0

    with pytest.raises(ContractLogicError):
        like_video(video_sharing, video_liker, video_uploader, 0)
