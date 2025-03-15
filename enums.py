from enum import Enum
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
    HIGH = 0
    PAIR = 1
    TWOPAIR = 2
    THREE = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL = 6
    FOUR = 7
    STRAIGHT_F = 8
    ROYAL_F = 9
    FIVE = 10
    HOUSE_F = 11
    FIVE_F = 12