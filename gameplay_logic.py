from enums import Suit, Rank
import random
from card import Card

def generate_deck(shuffle: bool=False) -> list['CardData']:
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

class CardData():
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

    def __repr__(self):
        return f"CD: {self._rank.name.capitalize()} of {self._suit.name.capitalize()}s"

class GameplayLogic():
    deck: list[CardData]
    hand: list[CardData] # will need to add sorting, so u can sort by suit or rank
    played: list[CardData]
    jokers: list[CardData]
    hand_size: int
    num_hands: int
    num_discards: int
    score: int
    done: bool

    def __init__(self):
        self.deck = generate_deck(True)
        self.hand = []
        self.played = []
        self.jokers = []
        self.hand_size = 8
        self.num_hands = 4
        self.num_discards = 3
        self.score = 0
        self.done = False

    @property
    def is_deck_empty(self) -> bool:
        """
        Checks if deck is empty

        Returns (bool): True if deck is empty, false otherwise
        """
        return len(self.deck) == 0

    def num_selected(self) -> int:
        """
        Returns number of selected cards
        """
        count = 0
        for cards in self.hand:
            if cards.selected:
                count += 1
        return count

    def convert_to_card_data(self, gui_card: Card) -> CardData:
        """
        Gets CardData in hand that matches the GUI Card
        """
        suit, rank = gui_card.suit, gui_card.rank
        for card_data in self.hand:
            if card_data.get_suit == suit and card_data.get_rank == rank:
                return card_data
        raise ValueError("Matching card not found in hand")

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
                delt = self.deck.pop()
                self.hand.append(delt)

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

    def play_hand(self) -> None:
        """
        Plays selected cards for points.
        Raises ValueError if less than one card is selected
        """
        if self.num_selected() == 0:
            raise ValueError(f"Must have at least one card selected!")
        for card in self.hand:
            if card.selected:
                self.played.append(card)
        self.hand = [card for card in self.hand if not card.selected]
        # Currenlty plays all cards. Will need to implement poker hands to
        # play highest ranked hand of cards
        chips = 0
        for card in self.played:
            chips += min(card.get_rank.value + 2, 11)
        ###
        # Stand in for mult system. Will need to implement hand levels system
        # with unique base mults and chips. Will also have to implement joker
        # system here i think.
        ###
        mult = 1
        self.num_hands -= 1
        if self.num_hands == 0:
            self.done = True
        self.score += chips * mult
        self.played = []

    def discard(self) -> None:
        """
        Discards selected cards
        Raises ValueError if called with no selected cards or if no discards
        left
        """
        if self.num_selected() == 0:
            raise ValueError(f"Must have at least one card selected!")
        if self.num_discards == 0:
            raise ValueError(f"Cannot discard! No Discards left!")
        list = []
        for card in self.hand:
            if not card.selected:
                list.append(card)
        self.hand = list
        self.num_discards -= 1
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



