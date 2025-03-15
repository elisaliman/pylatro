from enums import Suit, Rank


class CardData:
    suit: Suit
    rank: Rank
    selected: bool

    def __init__(self, suit: Suit, rank: Rank):
        self._suit = suit
        self._rank = rank
        self.selected = False

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
