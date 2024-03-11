import random
from flask import url_for


class Card:

    def __init__(self, type, game, variation=None):
        self.type = type
        self.game = game

        if variation is None:
            self.variation = random.randint(1,
                                            3) if type != "explode" else 1  # jest tylko jeden obrazek eksplodującego kotka
        else:
            self.variation = variation
        self.path = self.get_image_path()

    @staticmethod
    def pprint(cards):
        return [x.type for x in cards]

    def get_image_path(self):
        return f"{self.type}{self.variation}.png"

    def check(self):
        return True

    def action(self):
        self.game.played.append((self, self.game.player()))
        print(f"Card {self.type} played. Link: {self.path}")

    def on_draw(self):
        print(f"You got: {self.type}")


class Explode(Card):

    def __init__(self, game):
        super().__init__("explode", game)

    def action(self):
        super().action()

    def on_draw(self):
        super().on_draw()

        player = self.game.player()

        defused = False

        for card in player.cards:

            if isinstance(card, Defuse):
                player.play_card(card)
                defused = True
                break

        if not defused:
            player.explode()
            print("BUM")
            return url_for('main.explode', defused=False)
        else:
            return url_for('main.explode', defused=True)


class Defuse(Card):

    def __init__(self, game):
        super().__init__("defuse", game)

    def action(self):
        super().action()
        print("bomb has been defused")


class Future(Card):

    def __init__(self, game):
        super().__init__("future", game)

    def action(self):
        super().action()

        return url_for('main.future')


class Attack(Card):

    def __init__(self, game):
        super().__init__("attack", game)

    def action(self):
        super().action()
        self.game.turn.end_without_taking()
        self.game.turn.attack()
        self.game.finish_round()


class Skip(Card):

    def __init__(self, game):
        super().__init__("skip", game)

    def action(self):
        super().action()
        self.game.turn.end_without_taking()
        self.game.finish_round()


class Favor(Card):

    def __init__(self, game):
        super().__init__("favor", game)

    def action(self, target=None, index=None):
        super().action()

        if target is None:
            return url_for('main.favor')


class Mix(Card):

    def __init__(self, game):
        super().__init__("mix", game)

    def action(self):
        super().action()
        self.game.deck.shuffle()


class Cat(Card):

    def __init__(self, game, variation=None):
        super().__init__("cat", game, variation)

    def check(self):
        if not self.find_second():
            print("second cat card not found")
            return False
        else:
            return True

    def action(self, target=None, idx1=None, ):
        super().action()

        card = self.find_second()
        if card:
            self.game.player().cards.remove(card)  # kliknięty Cat sam sie usuwa tak jak inne karty
            self.game.played.append((card, self.game.player()))
        else:
            return

        if target is None:
            return url_for('main.cat')

    def find_second(self):

        cards = self.game.player().cards

        for card in cards:
            if isinstance(card, Cat) and card.variation == self.variation and card != self:
                return card

        return None


class Nono(Card):

    def __init__(self, game):
        super().__init__("nono", game)

    def check(self):

        if self.game.played:
            previous_card = self.game.played[-1][0]

            match previous_card:
                case Nono():
                    return False
                case Defuse():
                    return False

            return True

    def action(self):
        super().action()

        previous_card = self.game.played[-2][0]
        print(previous_card)

        match previous_card:
            case Skip():
                self.game.turn.decrement()

            case Attack():
                self.game.turn.decrement()
                self.game.turn.take_two = False

            case Future():
                return url_for('main.nono')

            case Favor():
                return url_for('main.nono')

            case Cat():
                return url_for('main.nono')

            case Nono():
                pass

            case Mix():
                self.game.deck.revert_shuffle()

            case Explode():
                pass
