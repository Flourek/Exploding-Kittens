from .deck import Deck
from .player import Player
from .card import Card
from .turn import Turn

import string
import random


class Game:

    def __init__(self, code, host, clients=None):
        self.code = code
        self.host = host
        self.clients = []

        if clients:
            self.clients.extend(clients)

        self.deck = None
        self.turn = None
        self.played = []  # list of touple (Card, Player)

        self.in_progress = False
        self.skip = False
        self.take_two = False
        self.winner: Player = None

        print(f"Created new game with code {self.code}")

    def begin(self):
        self.in_progress = True
        self.deck = Deck(self)
        self.turn = Turn(self, self.clients)
        self.deck.add_bombs()

    def finish_round(self):

        if self.turn._end_without_taking:
            self.turn._end_without_taking = False
        else:
            pass
            # self.player().take_card()

        self.turn.advance()

        print()
        print(f"Deck: {Card.pprint(self.deck.cards)}")
        print(f"It's now {self.player().name}'s turn.")

    def player(self) -> Player:
        return self.turn.current

    def get_player(self, username: str) -> Player:
        for player in self.turn.players:
            if player.name == username:
                return player

    def add_client(self, username: str):
        self.clients.append(username)

    def get_client(self, username: str):
        return self.clients[self.clients.index(username)]

    def check_win(self):
        if len(self.alive_players()) <= 1:
            self.winner = self.player()
            return True

    def alive_players(self):
        return [player for player in self.turn.players if player.alive]

    def set_turn(self, player_name):
        # Check if the player exists in the game
        if player_name not in [player.name for player in self.players]:
            print(f"Player '{player_name}' not found in the game.")
            return

        # Set the turn to the specified player
        self.turn = player_name
        print(f"It's now {player_name}'s turn.")

    @staticmethod
    def generate_code():

        characters = string.ascii_uppercase
        code = ''.join(random.choice(characters) for _ in range(6))

        return code


if __name__ == "__main__":
    g = Game("MEKS", "bope", "skooke")
    g.loop()
