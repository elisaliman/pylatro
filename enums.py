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
