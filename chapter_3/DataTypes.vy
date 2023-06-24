# @version ^0.3.0

life_is_beautiful: bool
var_int1: int8
var_int2: int64
var_int3: int128
var_int4: int256
var_uint1: uint8
var_uint2: uint64
var_uint3: uint128
var_uint4: uint256
pi: decimal
my_grandma_wallet: address
var_byte1: bytes32
var_byte2: bytes18
var_bytes: Bytes[56]
author: String[100]
enum Direction:
    NORTH
    SOUTH
    WEST
    EAST
direction: Direction
my_list: int16[5]
my_dynamic_array: DynArray[int128, 5]
struct Permission:
    write: bool
    execute: bool
my_permission: Permission
donaturs: HashMap[address, uint256]
