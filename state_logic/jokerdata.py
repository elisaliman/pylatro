from state_logic.carddata import CardDataBase
from typing import Callable
from state_logic.poker_hand_type import *


class JokerData(CardDataBase):
    name: str
    ability: Callable[...,int]
    hand_hand_condition: Callable[[list[CardData]], bool] | None
    ability_type: str
    value: int


    def __init__(self, name: str, value: int, ability: Callable[..., int], ability_type: str="", hand_condition: Callable[...,bool] | None=None):
        super().__init__()
        self.name = name
        self.ability = ability
        self.ability_type = ability_type
        self.hand_condition = hand_condition # HAND MUST BE SORTED RANK-WISE IF PASSED
        self.value = value

    def __repr__(self):
        return f"JokerData: {self.name}"

def generate_jokers() -> list[JokerData]:
    sly = JokerData("Sly Joker", 3, lambda c: c + 50, "chip", hand_condition=lambda hand: bool(get_n_of_a_kind(hand, 2)))
    wily = JokerData("Wily Joker", 3, lambda c: c + 100, "chip", hand_condition=lambda hand: bool(get_n_of_a_kind(hand, 3)))
    clever = JokerData("Clever Joker", 4, lambda c: c + 80, "chip", hand_condition=lambda hand: bool(get_n_of_a_kind(hand, 2) and len(hand)==4))
    dev = JokerData("Devious Joker", 4, lambda c: c + 100, "chip", hand_condition=lambda hand: bool(get_straight(hand)))
    crafty = JokerData("Crafty Joker", 4, lambda c: c + 80, "chip", hand_condition=lambda hand: bool(get_flush(hand)))
    jolly = JokerData("Jolly Joker", 3, lambda m: m + 8, "mult", hand_condition=lambda hand: bool(get_n_of_a_kind(hand, 2)))
    zany = JokerData("Zany Joker", 4, lambda m: m + 12, "mult",hand_condition=lambda hand: bool(get_n_of_a_kind(hand, 3)))
    mad = JokerData("Mad Joker", 4, lambda m: m + 10, "mult",hand_condition=lambda hand: bool(get_n_of_a_kind(hand, 2) and len(hand)==4))
    crazy = JokerData("Crazy Joker", 4, lambda m: m + 12, "mult", hand_condition=lambda hand:bool(get_straight(hand)))
    droll = JokerData("Droll Joker", 4, lambda m: m + 10, "mult", hand_condition=lambda hand: bool(get_flush(hand)))
    jokers = [sly, wily, clever, dev, crafty, jolly, zany, mad, crazy, droll]
    return jokers