from state_logic.carddata import CardDataBase
from typing import Callable
from state_logic.poker_hand_type import *
from enums import AbilityWhole, AbilType, AbilCategory


class JokerData(CardDataBase):
    name: str
    ability: Callable[..., int]
    hand_hand_condition: Callable[[list[CardData]], bool] | None
    ability_category: tuple[AbilCategory, ...]
    ability_type: tuple[AbilType, ...]
    value: int
    scored: bool

    def __init__(
        self,
        name: str,
        value: int,
        ability: Callable[..., int],
        ability_whole: AbilityWhole,
        hand_condition: Callable[..., bool] | None = None,
    ):
        super().__init__()
        self.name = name
        self.ability = ability
        self.ability_category = tuple(ability_whole.category)
        self.ability_type = tuple(ability_whole.type)
        self.hand_condition = hand_condition  # HAND MUST BE SORTED RANK-WISE IF PASSED
        self.value = value
        self.scored = False

    def __repr__(self):
        return f"JokerData: {self.name}"


def create_add_x(x: int) -> Callable[[int], int]:
    def add_x(num: int) -> int:
        return num + x

    return add_x


def create_test_hand(handtype: HandType) -> Callable[[list[CardData]], bool]:
    test_functions: dict[HandType, Callable[[list[CardData]], bool]] = {
        HandType.PAIR: lambda hand: bool(get_n_of_a_kind(hand, 2)),
        HandType.THREE: lambda hand: bool(get_n_of_a_kind(hand, 3)),
        HandType.TWOPAIR: lambda hand: bool(get_n_of_a_kind(hand, 2))
        and len(hand) == 4,
        HandType.STRAIGHT: lambda hand: bool(get_straight(hand)),
        HandType.FLUSH: lambda hand: bool(get_flush(hand)),
    }
    try:
        return test_functions[handtype]
    except KeyError:
        raise ValueError(f"Error: Passed bad hand type: {handtype}")


def generate_jokers() -> list[JokerData]:
    sly = JokerData(
        "Sly Joker",
        3,
        create_add_x(50),
        AbilityWhole(AbilType.ADD_CHIPS, AbilCategory.INDIE),
        create_test_hand(HandType.PAIR),
    )
    wily = JokerData(
        "Wily Joker",
        3,
        create_add_x(100),
        AbilityWhole(AbilType.ADD_CHIPS, AbilCategory.INDIE),
        create_test_hand(HandType.THREE),
    )
    clever = JokerData(
        "Clever Joker",
        4,
        create_add_x(80),
        AbilityWhole(AbilType.ADD_CHIPS, AbilCategory.INDIE),
        create_test_hand(HandType.TWOPAIR),
    )
    dev = JokerData(
        "Devious Joker",
        4,
        create_add_x(100),
        AbilityWhole(AbilType.ADD_CHIPS, AbilCategory.INDIE),
        create_test_hand(HandType.STRAIGHT),
    )
    crafty = JokerData(
        "Crafty Joker",
        4,
        create_add_x(80),
        AbilityWhole(AbilType.ADD_CHIPS, AbilCategory.INDIE),
        create_test_hand(HandType.FLUSH),
    )
    jolly = JokerData(
        "Jolly Joker",
        3,
        create_add_x(8),
        AbilityWhole(AbilType.ADD_MULT, AbilCategory.INDIE),
        create_test_hand(HandType.PAIR),
    )
    zany = JokerData(
        "Zany Joker",
        4,
        create_add_x(12),
        AbilityWhole(AbilType.ADD_MULT, AbilCategory.INDIE),
        create_test_hand(HandType.THREE),
    )
    mad = JokerData(
        "Mad Joker",
        4,
        create_add_x(10),
        AbilityWhole(AbilType.ADD_MULT, AbilCategory.INDIE),
        create_test_hand(HandType.TWOPAIR),
    )
    crazy = JokerData(
        "Crazy Joker",
        4,
        create_add_x(12),
        AbilityWhole(AbilType.ADD_MULT, AbilCategory.INDIE),
        create_test_hand(HandType.STRAIGHT),
    )
    droll = JokerData(
        "Droll Joker",
        4,
        create_add_x(10),
        AbilityWhole(AbilType.ADD_MULT, AbilCategory.INDIE),
        create_test_hand(HandType.FLUSH),
    )
    jokers = [sly, wily, clever, dev, crafty, jolly, zany, mad, crazy, droll]
    return jokers
