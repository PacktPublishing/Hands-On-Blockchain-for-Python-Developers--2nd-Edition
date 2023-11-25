# @version ^0.3.0

struct Video:
    path: String[50]
    title: String[20]

event Transfer:
    _from: indexed(address)
    _to: indexed(address)
    _value: uint256

event Approval:
    _owner: indexed(address)
    _spender: indexed(address)
    _value: uint256

event UploadVideo:
    _user: indexed(address)
    _index: uint256

event LikeVideo:
    _video_liker: indexed(address)
    _video_uploader: indexed(address)
    _index: uint256

user_videos_index: HashMap[address, uint256]

name: public(String[20])
symbol: public(String[3])
totalSupply: public(uint256)
decimals: public(uint256)
balances: HashMap[address, uint256]
allowed: HashMap[address, HashMap[address, uint256]]

all_videos: HashMap[address, HashMap[uint256, Video]]
likes_videos: HashMap[Bytes[100], bool]
aggregate_likes: HashMap[Bytes[100], uint256]


@external
def __init__():
    _initialSupply: uint256 = 500
    _decimals: uint256 = 3
    self.totalSupply = _initialSupply * 10 ** _decimals
    self.balances[msg.sender] = self.totalSupply
    self.name = 'Video Sharing Coin'
    self.symbol = 'VID'
    self.decimals = _decimals
    log Transfer(ZERO_ADDRESS, msg.sender, self.totalSupply)

@external
@view
def balanceOf(_owner: address) -> uint256:
    return self.balances[_owner]

@internal
def _transfer(_source: address, _to: address, _amount: uint256) -> bool:
    assert self.balances[_source] >= _amount
    self.balances[_source] -= _amount
    self.balances[_to] += _amount
    log Transfer(_source, _to, _amount)
    return True

@external
def transfer(_to: address, _amount: uint256) -> bool:
    return self._transfer(msg.sender, _to, _amount)

@external
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    assert _value <= self.allowed[_from][msg.sender]
    assert _value <= self.balances[_from]
    self.balances[_from] -= _value
    self.allowed[_from][msg.sender] -= _value
    self.balances[_to] += _value
    log Transfer(_from, _to, _value)
    return True

@external
def approve(_spender: address, _amount: uint256) -> bool:
    self.allowed[msg.sender][_spender] = _amount
    log Approval(msg.sender, _spender, _amount)
    return True

@external
@view
def allowance(_owner: address, _spender: address) -> uint256:
    return self.allowed[_owner][_spender]

@external
def upload_video(_video_path: String[50], _video_title: String[20]) -> bool:
    _index: uint256 = self.user_videos_index[msg.sender]
    self.all_videos[msg.sender][_index] = Video({ path: _video_path, title: _video_title })
    self.user_videos_index[msg.sender] += 1
    log UploadVideo(msg.sender, _index)
    return True

@external
@view
def latest_videos_index(_user: address) -> uint256:
    return self.user_videos_index[_user]

@external
@view
def videos_path(_user: address, _index: uint256) -> String[50]:
    return self.all_videos[_user][_index].path

@external
@view
def videos_title(_user: address, _index: uint256) -> String[20]:
    return self.all_videos[_user][_index].title

@external
def like_video(_user: address, _index: uint256) -> bool:
    _msg_sender_str: bytes32 = convert(msg.sender, bytes32)
    _user_str: bytes32 = convert(_user, bytes32)
    _index_str: bytes32 = convert(_index, bytes32)
    _key: Bytes[100] = concat(_msg_sender_str, _user_str, _index_str)
    _likes_key: Bytes[100] = concat(_user_str, _index_str)
    assert _index < self.user_videos_index[_user]
    assert self.likes_videos[_key] == False
    self.likes_videos[_key] = True
    self.aggregate_likes[_likes_key] += 1
    self._transfer(msg.sender, _user, 1)
    log LikeVideo(msg.sender, _user, _index)
    return True

@external
@view
def video_has_been_liked(_user_like: address, _user_video: address, _index: uint256) -> bool:
    _user_like_str: bytes32 = convert(_user_like, bytes32)
    _user_video_str: bytes32 = convert(_user_video, bytes32)
    _index_str: bytes32 = convert(_index, bytes32)
    _key: Bytes[100] = concat(_user_like_str, _user_video_str, _index_str)
    return self.likes_videos[_key]

@external
@view
def video_aggregate_likes(_user_video: address, _index: uint256) -> uint256:
    _user_video_str: bytes32 = convert(_user_video, bytes32)
    _index_str: bytes32 = convert(_index, bytes32)
    _key: Bytes[100] = concat(_user_video_str, _index_str)
    return self.aggregate_likes[_key]
