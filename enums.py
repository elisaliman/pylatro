from enum import Enum, auto

class Suit(Enum):
    # Ordered in order they appear in sprite sheet
    HEART = 0
    CLUB = 1
    DIAMOND = 2
    SPADE = 3


class Rank(Enum):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12

class HandType(Enum):
    HIGH = (0, "High Card")
    PAIR = (1, "Pair")
    TWOPAIR = (2, "Two Pair")
    THREE = (3, "Three of a Kind")
    STRAIGHT = (4, "Straight")
    FLUSH = (5, "Flush")
    FULL = (6, "Full House")
    FOUR = (7, "Four of a Kind")
    STRAIGHT_F = (8, "Straight Flush")
    ROYAL_F = (9, "Royal Flush")
    FIVE = (10, "Five of a Kind")
    HOUSE_F = (11, "Flush House")
    FIVE_F = (12, "Flush Five")
    EMPTY = (13, "")

    @property
    def rank(self):
        return self.value[0]

    @property
    def name(self):
        return self.value[1]


class AbilCategory(Enum):
    INDIE = 0  # Abilities that trigger after all cards are scored.
    ON_PLAYED = 1 # triggers when a card is played, before it's scored.
    ON_SCORED = 2 # triggers when a card is scored.
    ON_HELD = 3 # triggers when a card is held in hand.
    ON_DISCARD = 4 # triggers on a discard.
    PASSIVE = 5 #  dont trigger, but have a passive effect...

class AbilType(Enum):
    # Joker ability types
    ADD_CHIPS = auto()
    ADD_MULT = auto()

class AbilityWhole():
    type: list[AbilType]
    category: list[AbilCategory]
    def __init__(self, type: AbilType | list[AbilType], category: AbilCategory | list[AbilCategory]):
        self.type = []
        if isinstance(type, list):
            self.type.extend(type)
        else:
            self.type.append(type)
        self.category = []
        if isinstance(category, list):
            self.category.extend(category)
        else:
            self.category.append(category)
