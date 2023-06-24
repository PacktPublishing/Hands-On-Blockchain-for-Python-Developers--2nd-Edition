# @version ^0.3.0

my_grandma_wallet: address
author: String[100]
fib_list: int16[5]
fib_dynamic_array: DynArray[int128, 5]
struct Permission:
    write: bool
    execute: bool
my_permission: Permission
donaturs: HashMap[address, uint256]


@external
def __init__():
    self.my_grandma_wallet = 0xde93510CFa39Ab92BF927399F799DbE71997Ee0b
    self.author = "Arjuna Sky Kok"
    self.fib_list = [1, 1, 2, 3, 5]
    self.fib_dynamic_array.append(1)
    self.fib_dynamic_array.append(1)
    self.fib_dynamic_array.append(2)
    self.my_permission = Permission({write: True, execute: False})
    self.donaturs[self.my_grandma_wallet] = 4000000000000000000

    donation_target : int128 = 80000000000000000000
