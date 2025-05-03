import itertools
import math
import random
import time
from collections import Counter
from typing import List


class Deck:
    def __init__(self) -> None:
        self.cards = list(range(52))
        random.shuffle(self.cards)

    def draw(self, n: int = 1) -> List[int]:
        drawn, self.cards = self.cards[:n], self.cards[n:]
        return drawn


def card_to_rank(card):
    # 0 -> 2 and 12 -> Ace
    return card % 13


def card_to_suit(card):
    # 0 -> ♣, 1 -> ♦, 2 -> ♥, 3 -> ♠
    return card // 13


# assigns value to the ranking of a hand
# 0 is high card and 8 is royal flush
def rank_hand(cards):
    ranks = [c % 13 for c in cards]
    suits = [c // 13 for c in cards]

    rank_counts = Counter(ranks)
    counts = sorted(rank_counts.values(), reverse=True)


    count_and_rank = sorted(rank_counts.items(),
                              key=lambda kv: (kv[1], kv[0]),
                              reverse=True)
    sorted_ranks = [r for r, _ in count_and_rank]

    is_flush = len(set(suits)) == 1
    unique   = sorted(set(ranks))
    is_wheel = unique == [0, 1, 2, 3, 12]
    is_straight = len(unique) == 5 and (
        unique[-1] - unique[0] == 4 or is_wheel
    )
    top_of_straight = 3 if is_wheel else unique[-1]

    if is_straight and is_flush:
        return 8, top_of_straight

    if counts[0] == 4:
        quad, kicker = sorted_ranks[0], sorted_ranks[1]
        return 7, quad, kicker

    if counts == [3, 2]:
        triple, pair = sorted_ranks[0], sorted_ranks[1]
        return 6, triple, pair

    if is_flush:
        return 5, *sorted(ranks, reverse=True)

    if is_straight:
        return 4, top_of_straight

    if counts[0] == 3:
        triple = sorted_ranks[0]
        kickers = sorted(sorted_ranks[1:], reverse=True)
        return 3, triple, *kickers

    if counts[0] == 2 and counts[1] == 2:
        high_pair, low_pair, kicker = sorted_ranks[0], sorted_ranks[1], sorted_ranks[2]
        return 2, high_pair, low_pair, kicker

    if counts[0] == 2:
        pair = sorted_ranks[0]
        kickers = sorted(sorted_ranks[1:], reverse=True)
        return 1, pair, *kickers

    return 0, *sorted(ranks, reverse=True)


# gets the best combination of 5 out of the 7 total cards
def best_of_seven(seven_cards):
    best = None
    for five in itertools.combinations(seven_cards, 5):
        r = rank_hand(five)
        if best is None or r > best:
            best = r
    return best


def rollout_once(my_hole, community):
    deck = Deck()

    for c in my_hole + community:
        deck.cards.remove(c)

    opp_hole = deck.draw(2)
    remaining_board = deck.draw(5 - len(community))
    board_full = community + remaining_board

    my_rank = best_of_seven(my_hole + board_full)
    opp_rank = best_of_seven(opp_hole + board_full)

    if my_rank > opp_rank:
        return 1.0
    if my_rank < opp_rank:
        return 0.0
    return 0.5


class Node:
    __slots__ = ("move", "w", "n")
    def __init__(self, move):
        self.move = move
        self.w = 0.0
        self.n = 0


def ucb(nd, tot, c=1.41421356237):
    if nd.n == 0: return float("inf")
    return nd.w / nd.n + c * math.sqrt(math.log(tot) / nd.n)


# decision maker
def decide(hole, board, limit=10.0, thresh=.5):
    fold = Node("fold")
    stay = Node("stay")
    kids = (stay, fold)

    fold.n, fold.w = 1, 0.0
    stay.n, stay.w = 1, rollout_once(hole, board)
    tot = 2
    end = time.perf_counter() + limit

    while time.perf_counter() < end:
        nd = max(kids, key=lambda k: ucb(k, tot))
        reward = 0.0 if nd.move == "fold" else rollout_once(hole, board)
        nd.n += 1
        nd.w += reward
        tot += 1

    p = stay.w / stay.n
    return "stay" if p >= thresh else "fold"


class PokerBot:
    def __init__(self, limit=10.0, thresh=.5):
        self.limit = limit
        self.thresh = thresh

    def action(self, hole, board):
        return decide(hole, board, self.limit, self.thresh)


if __name__ == "__main__":
    d = Deck()
    h = d.draw(2)
    b = d.draw(3)
    print("hole:", h, "board:", b, "->", PokerBot().action(h, b))