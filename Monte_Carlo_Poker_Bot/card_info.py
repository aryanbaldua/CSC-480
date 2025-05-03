# maps so it is more efficient to search up with dictionary
SUITS = {0: "♣", 1: "♦", 2: "♥", 3: "♠"}
RANKS = {
     0: "2",  1: "3",  2: "4",  3: "5",
     4: "6",  5: "7",  6: "8",  7: "9",
     8: "10", 9: "J", 10: "Q", 11: "K", 12: "A",
}


def card_to_str(card: int) -> str:
    rank = card % 13
    suit = card // 13
    return f"{RANKS[rank]}{SUITS[suit]}"
