from .player import Player


class Turn:

    def __init__(self, game, clients):
        self.game = game
        self.players = [Player(client, self.game) for client in clients]
        self.current = self.players[0]

        self.i = 0
        self.attacked = None
        self._end_without_taking = False
        self._end = False

    # account for unalive
    def increment(self):
        self.i += 1
        self.i %= len(self.players)
        self.current = self.players[self.i]

        if not self.current.alive:
            self.increment()

    def decrement(self):
        self.i -= 1
        self.i %= len(self.players)
        self.current = self.players[self.i]

        if not self.current.alive:
            self.decrement()

    def remove_players(self, player):
        self.players.remove(player)
        self.decrement()

        if len(self.players) == 1:
            print(f"{self.players[0].name} won! yippe")
            exit()

    def end(self):

        if self._end:
            self._end = False
            return True
        else:
            self._end = True
            return False

    def end_without_taking(self):
        self._end_without_taking = True
        self.end()

    def attack(self):
        next = (self.i + 1) % len(self.players)
        self.attacked = self.players[next]

    def advance(self):

        if isinstance(self.attacked, Player):
            if self.attacked == self.current:
                print(f"{self.current.name} must play twice")
                self.attacked = None
                return

        self.increment()

        if not self.current.alive:
            self.advance()
