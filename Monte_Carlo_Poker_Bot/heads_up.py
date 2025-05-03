import random
from itertools import combinations
from card_info import card_to_str
from PokerBot import PokerBot, rank_hand


def show(cs):
    return " ".join(card_to_str(c) for c in cs)


def best5(cs):
    top = None
    for five in combinations(cs, 5):
        sc = rank_hand(five)
        if top is None or sc > top:
            top = sc
    return top


def opp_stays():
    return random.random() < .9


def run():
    stages = ["Pre-Flop", "Pre-Turn", "Pre-River"]
    deck = list(range(52))
    random.shuffle(deck)

    bot_hole = [deck.pop(), deck.pop()]
    opp_hole = [deck.pop(), deck.pop()]
    board = []
    bot = PokerBot()

    bot_fold = opp_fold = False

    for st in stages:
        if st == "Pre-Turn":
            board.extend([deck.pop() for _ in range(3)])
        elif st == "Pre-River":
            board.append(deck.pop())

        print(f"\n=== {st} ===")
        print("Board:", show(board))
        print("Bot  :", show(bot_hole))

        bot_act = bot.action(bot_hole, board)
        opp_act = "stay" if opp_stays() else "fold"
        print("Bot action:", bot_act)
        print("Opp action:", opp_act)

        if bot_act == "fold": bot_fold = True
        if opp_act == "fold": opp_fold = True
        if bot_fold or opp_fold: break

    if not (bot_fold or opp_fold):
        board.append(deck.pop())
        print("\n=== RIVER ===")
        print("Board:", show(board))

        bot_rank = best5(bot_hole + board)
        opp_rank = best5(opp_hole + board)

        print("\nShowdown:")
        print(f"Bot  {show(bot_hole)} -> {bot_rank}")
        print(f"Opp  {show(opp_hole)} -> {opp_rank}")

        if bot_rank > opp_rank:
            print("Hooray! The bot wins!")
        elif bot_rank < opp_rank:
            print("Aw man, the opponent wins.")
        else:
            print("Split pot.")
    else:
        if bot_fold and opp_fold:
            print("Both folded")
        elif bot_fold:
            print("Bot folded — Aw man, the opponent wins.")
        else:
            print("Opponent folded — Hooray! The bot wins.")


if __name__ == "__main__":
    run()
