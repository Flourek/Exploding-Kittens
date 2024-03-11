from .card import *
import random


class Deck:
    def __init__(self, game):
        self.game = game
        self.cards = []
        self.before_mix = []

        self.create_new_deck()

    def create_new_deck(self):

        self.cards =            []

        self.cards.extend( [Nono(self.game)   for _ in range(5)] )
        self.cards.extend( [Attack(self.game) for _ in range(4)])
        self.cards.extend( [Skip(self.game)   for _ in range(4)] )
        self.cards.extend( [Favor(self.game)  for _ in range(4)] )
        self.cards.extend( [Mix(self.game)    for _ in range(4)] )
        self.cards.extend( [Future(self.game) for _ in range(4)])

        self.cards.extend( [Cat(self.game, variation=1)  for _ in range(4)])
        self.cards.extend( [Cat(self.game, variation=2)  for _ in range(4)])
        self.cards.extend( [Cat(self.game, variation=3)  for _ in range(4)])
        self.cards.extend( [Cat(self.game, variation=4)  for _ in range(4)])
        self.cards.extend( [Cat(self.game, variation=5)  for _ in range(4)])

        self.shuffle()

    def add_bombs(self):
        defuses = 6 - len(self.game.clients)

        self.cards.extend(      [Defuse(self.game) for _ in range(defuses)] )
        self.cards.extend(      [Explode(self.game) for _ in range(4)] )
        self.shuffle()


    def reset(self):
        self.cards = [card for card, player in self.game.played]
        self.game.played = []
        self.shuffle()

    def deal(self):

        cards = [Defuse(self.game)]

        for _ in range(7):
            cards.append(self.pop())

        return cards

    def pop(self):
        if not self.cards:
            self.reset()

        return self.cards.pop()

    def insert_bomb(self, index):
        bomb = Explode(self.game)
        length = len(self.cards)
        self.cards.insert(length - index, bomb)

    def shuffle(self):
        self.before_mix = self.cards.copy()
        random.shuffle(self.cards)

    def revert_shuffle(self):
        self.game.deck.cards = self.game.deck.before_mix.copy()


if __name__ == "__main__":

    e = Deck()
    # print(e.cards)

    for x in e.cards:
        print(x.type)
