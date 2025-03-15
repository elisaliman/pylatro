import random

import state_logic.poker_hand_type as pk
from enums import HandType, Rank, Suit
from state_logic.carddata import CardData


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


class GameplayLogic:
    deck: list[CardData]
    hand: list[CardData]
    played: list[CardData]
    jokers: list[CardData]
    hand_size: int
    _num_hands: int
    _num_discards: int
    score: int
    done: bool

    def __init__(self):
        self.deck = generate_deck(True)
        self.deck_total = len(self.deck)
        self.hand = []
        self.played = []
        self.jokers = []
        self.hand_size = 8
        self._num_hands = 4
        self._num_discards = 30
        self.score = 0
        self.done = False

    @property
    def is_deck_empty(self) -> bool:
        """
        Checks if deck is empty

        Returns (bool): True if deck is empty, false otherwise
        """
        return len(self.deck) == 0

    @property
    def num_hands(self) -> int:
        return self._num_hands

    @property
    def num_discards(self) -> int:
        return self._num_discards

    @property
    def deck_remaining(self) -> int:
        return len(self.deck)

    def sort_cards(self, by_rank: bool) -> None:
        if by_rank:
            self.hand = sorted(
                self.hand, key=lambda card: (-card.get_rank.value, card.get_suit.value)
            )
        else:
            self.hand = sorted(
                self.hand, key=lambda card: (card.get_suit.value, -card.get_rank.value)
            )

    def num_selected(self) -> int:
        """
        Returns number of selected cards
        """
        count = 0
        for cards in self.hand:
            if cards.selected:
                count += 1
        return count

    def deal_to_hand(self) -> None:
        """
        Deals cards from deck into hand
        Raises ValueError if tries to deal to a full hand
        """
        hand_num_empty = self.hand_size - len(self.hand)
        if hand_num_empty == 0:
            raise ValueError("Cannot deal to a full hand!")
        for _ in range(hand_num_empty):
            if not self.is_deck_empty:
                dealt = self.deck.pop()
                self.hand.append(dealt)

    def select_card(self, card: CardData) -> None:
        """
        Selects card to be played

        Args:
            card (Card): Card to select
        """
        if card.selected:
            card.selected = False
        elif self.num_selected() < 5:
            card.selected = True

    def play_hand(self) -> list[CardData]:
        """
        Plays selected cards for points.
        Raises ValueError if less than one card is selected
        Raises ValueError if not enough hands left to use

        Retuns (list[CardData]): list of CardData in order for GUI to know which
            cards were actually counted for points
        """
        if self.num_selected() == 0:
            raise ValueError(f"Must have at least one card selected!")
        if self._num_hands <= 0:
            raise ValueError(f"Cannot play! No hands left! {self._num_hands=}")
        self.played = [card for card in self.hand if card.selected]
        valid_cards, hand_type = pk.get_hand_type(self.played)
        print(hand_type)
        # base_chips, base_mult = get_level(hand_type) # need to add base chips and base mult getter from hand type, probably new file with new class stored in game.py?
        base_chips, base_mult = (0, 1)
        chips = base_chips
        for card in valid_cards:
            chips += min(card.get_rank.value + 2, 10)
            if card.get_rank == Rank.ACE:
                chips += 1
        ###
        # Stand in for mult system. Will need to implement hand levels system
        # with unique base mults and chips. Will also have to implement joker
        # system here i think.
        ###
        self._num_hands -= 1
        if self._num_hands == 0:
            self.done = True
        self.score += chips * base_mult
        self.played.clear()
        return valid_cards

    def discard(self, just_played: bool = False) -> None:
        """
        Discards selected cards
        Raises ValueError if called with no selected cards or if no discards
        left

        Args:
            just_played (bool, optional): if true, wont deduct a discard as
                it means the fucntion was called to rid the played cards, not
                cards from hand
        """
        if self.num_selected() <= 0:
            raise ValueError(f"Must have at least one card selected!")
        if self._num_discards <= 0:
            raise ValueError(f"Cannot discard! No Discards left! {self._num_discards=}")
        list = []
        for card in self.hand:
            if not card.selected:
                list.append(card)
        self.hand = list
        if not just_played:
            self._num_discards -= 1
        # self.hand = [card for card in self.hand if not card.selected]
        # Should almost always call self.deal_to_hand() afterwards


# if __name__ == "__main__":
# logic = GameplayLogic() # comments are for unshuffled deck
# logic.deal_to_hand()
# print(f"{logic.hand=}")
# logic.select_card(logic.hand[0])
# logic.select_card(logic.hand[1])
# logic.select_card(logic.hand[2])
# logic.select_card(logic.hand[3])
# logic.select_card(logic.hand[4])
# logic.select_card(logic.hand[5])
# logic.select_card(logic.hand[6])
# logic.select_card(logic.hand[4])
# for card in logic.hand:
#     print(f"{card.selected=}")
# print("score before: ", logic.score)
# logic.play_hand()
# print(f"{logic.played=}")
# print("score after: ", logic.score) # should be 44
# print(f"before: {logic.hand=}") # should have 5 cards
# logic.deal_to_hand()
# print(f"after: {logic.hand=}") # should have 8 cards
