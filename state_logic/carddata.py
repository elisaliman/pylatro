from enums import Rank, Suit
from typing import Callable


class CardDataBase:
    edition: str | None # To be replaced by enums probably

    def __init__(self):
        self.edition = None

class CardData(CardDataBase):
    suit: Suit
    rank: Rank
    chips: int
    mult: int
    selected: bool
    seal: str | None # To be replaced by enums probably
    enhances: str | None # To be replaced by enums probably

    def __init__(self, suit: Suit, rank: Rank):
        super().__init__()
        self._suit = suit
        self._rank = rank
        self.chips = min(self._rank.value + 2, 10) if self._rank != Rank.ACE else 11
        self.selected = False
        self.enhances = None
        self.seal = None

    @property
    def get_suit(self) -> Suit:
        """Suit getter property"""
        return self._suit

    @property
    def get_rank(self) -> Rank:
        """Rank getter property"""
        return self._rank

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CardData):
            return False
        return self._suit == other.get_suit and self._rank == other._rank

    def __hash__(self):
        return hash((self._suit, self._rank))

    def __repr__(self):
        return f"CD: {self._rank.name.capitalize()} of {self._suit.name.capitalize()}s"
