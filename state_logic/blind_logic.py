import random
import copy

import state_logic.poker_hand_type as pk
from enums import HandType, Rank, Suit
from state_logic.carddata import CardData
from state_logic.game_manager import GameManagerLogic


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


class BlindLogic:
    blind: int
    manager: GameManagerLogic
    done: bool
    deck: list[CardData]
    hand: list[CardData]
    played: list[CardData]
    jokers: list[CardData]
    hand_size: int
    _num_hands: int
    _num_discards: int
    score: int

    def __init__(self, manager: GameManagerLogic):
        self.done = False
        self.manager = manager
        self.deck = copy.deepcopy(manager.deck)
        random.shuffle(self.deck)
        self.blind = self.manager.blinds.pop()
        self.deck_total = len(self.deck)
        self.hand = []
        self.played = []
        self.jokers = []
        self.hand_size = 8
        self._num_hands = 4
        self._num_discards = 30
        self.score = 0

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

    def get_hand_type(self) -> HandType:
        """
        Gets the hand type of the current selcted cards. Strictly used to give
        this information to the GUI
        """
        if self.num_selected() == 0:
            return HandType.EMPTY
        selected = [card for card in self.hand if card.selected]
        _, hand = pk.get_hand_type(selected)
        return hand

    def play_hand(self) -> tuple[list[CardData], HandType, tuple[int, int, int]]:
        """
        Plays selected cards for points.
        Raises ValueError if less than one card is selected
        Raises ValueError if not enough hands left to use

        Retuns (list[CardData]): list of CardData in order, handtype, and a
            a tuple containing (score, base chips, base mult)
        """
        if self.num_selected() == 0:
            raise ValueError(f"Must have at least one card selected!")
        if self._num_hands <= 0:
            raise ValueError(f"Cannot play! No hands left! {self._num_hands=}")
        self.played = [card for card in self.hand if card.selected]
        valid_cards, hand_type = pk.get_hand_type(self.played)
        # Sorts valid cards back into the order they were played
        valid_cards = [card for card in self.played if card in valid_cards]
        base_chips = self.manager.levels[hand_type]["chips"]
        base_mult = self.manager.levels[hand_type]["mult"]
        chips = base_chips
        for card in valid_cards:
            chips += card.chips
        ###
        # Stand in for mult system. Will need to implement hand levels system
        # with unique base mults and chips. Will also have to implement joker
        # system here i think.
        ###
        self.score += chips * base_mult
        self._num_hands -= 1
        self.played.clear()
        if self.score >= self.blind:
            self.end_game(won=True)
        if self._num_hands == 0:
            self.end_game(won=False)
        return (valid_cards, hand_type, (self.score, base_chips, base_mult))

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
        self.hand = [card for card in self.hand if not card.selected]
        if not just_played:
            self._num_discards -= 1
        # Should almost always call self.deal_to_hand() afterwards

    def end_game(self, won: bool=False) -> None:
        """
        Ends blind

        Args:
            won (bool, optional): By default False, but True if game was won
        """
        if self.done:
            raise ValueError("Game is already over!")
        self.done = True
        if won:
            print(f"You won! Entering shop...")
        else:
            print("Game Over! :(")
        # self.manager.deck = something? need someway to hand back modified deck if deck gets modified during game