from .card import *


class Player:

    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.alive = True
        self.cards = self.game.deck.deal()

    def __eq__(self, other):
        return self.name == other.name

    def take_card(self):
        card = self.game.deck.pop()
        redirect = card.on_draw()

        if isinstance(card, Explode):
            return redirect

        self.cards.insert(0, card)
        print(Card.pprint(self.cards))

    def take_card_from(self, player, card_index):
        card = player.get_card_by_index(card_index)

        self.cards.insert(0, card)
        player.cards.remove(card)

    # move to deck

    def explode(self):

        self.alive = False

        if self.game.player() == self:
            self.game.turn.end()

    def play_card(self, card, **args):
        if not self.alive:
            print("player is dead")
            return -1

        # if isinstance(card, Nono):
        if not card.check():
            return -1

        if card not in self.cards:
            print("error! the player does not have this card")
            return -1

        self.cards.remove(card)
        return card.action(**args)

    def get_card_by_index(self, index):
        if index < 0 or 0 >= len(self.cards):
            print("wrong index!")
            return

        return self.cards[index]

    def play_card_by_index(self, index, **args):
        card = self.get_card_by_index(index)
        self.play_card(card, **args)


if __name__ == "__main__":
    g = Player("MEKS", "e")
    g.cards = [Card.Explode(), Card.Defuse()]
    g.play_card(g.cards[0])
    print(g.cards)
