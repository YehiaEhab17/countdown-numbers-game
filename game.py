from enum import Enum
from random import randint, shuffle

LARGE_DECK = [25, 50, 75, 100]
SMALL_DECK = [i for i in range(1, 11)] * 2
VALID_OPERATIONS = ["+", "-", "*", "/"]


class Status(Enum):
    INVALID_NUM = "not a valid number"
    INVALID_OP = "not a valid operator"
    NOT_IN_POOL = "these numbers are not in the playable pool"
    NEG = "operation would result in a negative number"
    FRAC = "operation would result in a fractional number"
    INVALID = "invalid operation"
    OK = "valid operation"


def draw_cards(large_choice: int) -> list[int]:
    """large choice must be 0..4"""
    if large_choice < 0 or large_choice > 4:
        raise ValueError("Must be 0..4")

    playable_deck: list[int] = []
    large_deck = LARGE_DECK.copy()
    small_deck = SMALL_DECK.copy()
    shuffle(large_deck)
    shuffle(small_deck)

    playable_deck.extend(large_deck[:large_choice])
    playable_deck.extend(small_deck[: 6 - large_choice])

    return sorted(playable_deck)


def get_target():
    return randint(100, 999)


def is_valid_step(
    n1: int, n2: int, op: str, playable_deck: list[int]
) -> tuple[Status, int | None]:
    """expects only ints"""
    if not validate_number(n1) or not validate_number(n2):
        return (Status.INVALID_NUM, None)

    if not validate_operation(op):
        return (Status.INVALID_OP, None)

    if n1 == n2 and playable_deck.count(n1) < 2:
        return (Status.NOT_IN_POOL, None)
    if not is_in_pool(n1, playable_deck) or not is_in_pool(n2, playable_deck):
        return (Status.NOT_IN_POOL, None)

    try:
        if op == "+":
            return (Status.OK, n1 + n2)
        if op == "-":
            return (Status.OK, n1 - n2) if n1 > n2 else (Status.NEG, None)
        if op == "*":
            return (Status.OK, n1 * n2)
        if op == "/":
            return (Status.OK, n1 // n2) if n1 % n2 == 0 else (Status.FRAC, None)

    except ArithmeticError:
        pass

    return (Status.INVALID, None)


def validate_number(n: int):
    return n > 0


def validate_operation(op: str):
    return op in VALID_OPERATIONS


def is_in_pool(n: int, playable_deck: list[int]):
    return validate_number(n) and n in playable_deck


def update_pool(n1: int, n2: int, result: int, playable_deck: list[int]):
    """expects only ints"""
    playable_deck.remove(n1)
    playable_deck.remove(n2)
    playable_deck.append(result)
