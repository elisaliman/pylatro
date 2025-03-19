import random
from state_logic.carddata import CardData
from enums import Rank, Suit, HandType


def generate_deck(shuffle: bool = False) -> list["CardData"]:
    """
    Creates a standard deck of cards. Should be treated as a stack

    Args:
        shuffle (bool, optional): True to shuffle deck. Defaults to False
    """

    deck = []
    for suit in Suit:
        for rank in Rank:
            card = CardData(suit, rank)
            deck.append(card)
    if shuffle:
        random.shuffle(deck)
    return deck


def create_levels() -> dict[HandType, dict[str, int]]:
    """Creates hand levels with base chips and mult"""
    ###TODO: Might need to add a num played count at some point?
    levels: dict[HandType, dict[str, int]] = {
        HandType.FIVE_F: {"chips": 160, "mult": 16, "lvl": 1},  # "Flush Five"
        HandType.HOUSE_F: {"chips": 140, "mult": 14, "lvl": 1},  # "Flush House"
        HandType.FIVE: {"chips": 120, "mult": 12, "lvl": 1},  # "Five of a Kind"
        HandType.ROYAL_F: {"chips": 100, "mult": 8, "lvl": 1},  # "Royal Flush"
        HandType.STRAIGHT_F: {"chips": 100, "mult": 8, "lvl": 1},  # "Straight Flush"
        HandType.FOUR: {"chips": 60, "mult": 7, "lvl": 1},  # "Four of a Kind"
        HandType.FULL: {"chips": 40, "mult": 4, "lvl": 1},  # "Full House"
        HandType.FLUSH: {"chips": 35, "mult": 4, "lvl": 1},  # "Flush"
        HandType.STRAIGHT: {"chips": 30, "mult": 4, "lvl": 1},  # "Straight"
        HandType.THREE: {"chips": 30, "mult": 3, "lvl": 1},  # "Three of a Kind"
        HandType.TWOPAIR: {"chips": 20, "mult": 2, "lvl": 1},  # "Two Pair"
        HandType.PAIR: {"chips": 10, "mult": 2, "lvl": 1},  # "Pair"
        HandType.HIGH: {"chips": 5, "mult": 1, "lvl": 1},  # "High Card"
        HandType.EMPTY: {"chips": 0, "mult": 0, "lvl": 0},  # "Empty Hand"
    }
    return levels


# def create_blinds() -> list[tuple[int, str]]:
#     pass


class GameManagerLogic:
    """
    A class to manage a profile's overall progression and stats.
    Should be used to pass information down to gameplay_logic and
    other such places
    """

    deck: list["CardData"]  # Stores sorted game deck. (To be shuffled on gameplay)
    levels: dict[HandType, dict[str, int]]  # Hand levels and score
    blinds: list[int]
    round: int
    ante: int
    money: int

    def __init__(self):
        self.deck = generate_deck()
        self.levels = create_levels()
        self.blinds = [600, 450, 300]
        self.round = 0
        self.ante = 0
        self.money = 0

    def next_round(self):
        """To be called when a blind is selected"""
        self.round += 1
        if self.round % 3 == 1:
            self.ante += 1

    def skip_round(self):
        """
        To be called when a blind is skipped
        Raises a value error if attempted to skip a boss blind
        """
        if self.round % 3 == 0:
            raise ValueError("Cannot skip Boss Blind!!!")
        self.round += 1
