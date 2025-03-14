from state_logic.carddata import CardData
from enums import Suit, Rank, HandType
from operator import attrgetter
from collections import Counter


def get_hand_type(cards: list[CardData]) -> tuple[list[CardData], HandType]:
    """
    Takes a played hand and returns played cards and hand type

    Args:
        cards (list[CardData]): list of cards played

    Returns (tuple[list[CardData], str]): Tuple containing a list of cards
        played in the determined poker hand, and the poker hand name
    """
    ###TODO: Add a ctx parameter so i can check straights and flushes
    # and other rules based on the jokers or conditions of the current
    # game

    # Sorts cards by descending rank to make checks easier
    key_attr = attrgetter("get_rank.value")
    cards = sorted(cards, key=key_attr, reverse=True)
    card_len = len(cards)
    flush = get_flush(cards)

    # Checks are ordered in order of highest to lowest priority hand type
    if card_len == 5: #WILL HAVE TO UPDATE THESE CHECKS
        # Flush Five
        if (five_of_a_kind := get_n_of_a_kind(cards, 5)) and five_of_a_kind == flush:
            return five_of_a_kind, HandType.FIVE_F

        # Flush House
        if (full_house := get_full_house(cards)) and full_house == flush:
            return full_house, HandType.HOUSE_F

        if five_of_a_kind:
            return five_of_a_kind, HandType.FIVE

        if (flush := get_flush(cards)) and (straight := get_straight(cards)):
            if is_royal_flush(straight):
                return flush, HandType.ROYAL_F
            return flush, HandType.STRAIGHT_F

    if card_len >= 4:
        if four_of_a_kind := get_n_of_a_kind(cards, 4):
            return four_of_a_kind, HandType.FOUR

    if card_len == 5:
        if full_house: # Assigned when checking flush house
            return full_house, HandType.FULL

        if flush: # Assigned at start of checks
            return flush, HandType.FLUSH

        if straight: # Assigned when checking straight flush
            return straight, HandType.STRAIGHT

    if card_len >= 3:
        if three_of_a_kind := get_n_of_a_kind(cards, 3):
            return three_of_a_kind, HandType.THREE

    if card_len >= 4:
        pass #If two pair

    if card_len >= 2:
        if pair := get_n_of_a_kind(cards, 2):
            return pair, HandType.PAIR

    return [cards[0]], HandType.HIGH

def get_flush(cards: list[CardData]) -> list[CardData]:
    """
    Checks for a flush in cards
    Raises ValueError if cards length is too small to form a flush
    """
    ###TODO: Add a flush_size param or something similar
    FLUSH_REQ = 5
    if len(cards) < FLUSH_REQ:
        raise ValueError(f"Hand size must be at least {FLUSH_REQ} to form a flush. Current hand size: {len(cards)}")
    suit_counter = Counter(card.get_suit for card in cards)
    flush_suit, count = suit_counter.most_common(1)[0]
    if count >= FLUSH_REQ:
        return [card for card in cards if card.get_suit == flush_suit]
    return []

def get_full_house(cards: list[CardData]) -> list[CardData]:
    """
    Checks for a full house in cards
    Raises ValueError if cards length is too small to form a full house
    """
    if len(cards) < 5:
        raise ValueError(f"Hand size must be at least 5 to form a full house. Current hand size: {len(cards)}")
    rank_counter = Counter(card.get_rank for card in cards)
    triple_rank = None
    pair_rank = None
    for rank, count in rank_counter.most_common():
        if count >= 3:
            triple_rank = rank
            break
    if triple_rank is None:
        return []
    for rank, count in rank_counter.most_common():
        if rank != triple_rank and count >= 2:
            pair_rank = rank
            break
    if pair_rank is None:
        return []
    triple_cards = [card for card in cards if card.get_rank == triple_rank][:3]
    pair_cards = [card for card in cards if card.get_rank == pair_rank][:2]
    return triple_cards + pair_cards

def get_straight(cards: list[CardData]) -> list[CardData]:
    """
    Checks for a straight in cards.
    Raises ValueError if cards length is too small to form a straight
    """
    ###TODO: Add a straight_size param or something similar
    STRAIGHT_REQ = 5
    if len(cards) < STRAIGHT_REQ:
        raise ValueError(f"Hand size must be at least {STRAIGHT_REQ} to form a straight. Current hand size: {len(cards)}")
    played = []
    for idx, card in enumerate(cards[1:STRAIGHT_REQ]): #WILL ONLY CHECK FIRST 4 CARDS IF SET TO 4, WILL NEED TO LET IT ALSO CHECK THE LAST 4 CARDS EVENTUALLY
        if card.get_rank.value - cards[idx - 1].get_rank.value != 1:
            return []
        played.append(card)
    return played

def is_royal_flush(straight_flush: list[CardData]) -> bool:
    """
    Determines if a straight flush is also a royal flush
    Must pass through a straight flush
    """
    return straight_flush[-1].get_rank.value >= Rank.TEN.value


def get_n_of_a_kind(cards: list[CardData], n: int) -> list[CardData]:
    """
    Checks if cards contains n of a kind

    Args:
        n: number of a kind
        cards (list[CardData]): cards to check

    Return (list[CardData]): List of cards that are n of a kind
    """
    counter = Counter(cards)
    kinds = {card for card, count in counter.items() if count == n}
    return [card for card in cards if card in kinds]
