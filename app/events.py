from flask import request, session, url_for
from flask_socketio import emit, join_room
from .game import Game
from .game.card import *

from .extensions import io

clients = {}
rooms: dict[str: Game] = {}


@io.on("connect")
def handle_connect():
    if session['username']:
        clients[session['username']] = request.sid

    print(f"Client connected!")


@io.on('disconnect')
def test_disconnect():
    print('Client disconnected')


# Przy naciśnięciu "Stwórz nową grę"
@io.on("room_create")
def create_room(host, code=None, *players):
    if not code:
        code = Game.generate_code()

    if code in rooms:
        print("There already is a room like that ")
    else:
        print(f"Room {code} created!")
        rooms[code] = Game(code, host, players)

    return code


# Przy wejściu na strony /game i /game/*
@io.on("user_join")
def handle_user_join():
    room = session['room']
    username = session['username']

    if room not in rooms:
        print(f"{room} no such room exists!")
        return

    join_room(room)
    game = get_game(room)

    if username not in game.clients:
        clients[username] = request.sid

        print(f"User {username} {request.sid} joined room {room}!")

        game.add_client(username)
        emit('reload', to=room)


# Przy naciśnięciu "Rozpocznij" w lobby
@io.on("host_begin_game")
def host_begin_game():
    game = get_game(session["room"])

    game.begin()

    url = url_for('main.game')
    emit("redirect", url, to=session['room'])


# Zabranie karty z talii, co kończy turę. W przypadku bomby koniec tury odłożony na potem
@io.on("take_card")
def handle_take_card():
    game, player = reference(session)

    if (not permission(session)): return

    redirect = game.player().take_card()

    if redirect is not None:
        emit('redirect', redirect)
        if redirect == url_for('main.explode', defused=True): return

    game.finish_round()

    if game.check_win():
        url = url_for('main.win')
        emit("redirect", url, to=session['room'])
        return

    emit('back', to=session['room'], include_self=False)
    emit('new_card')


# Zagranie karty i powiązanej z nią czynności, która może zwrócić redirect na strone proszocą o dodatkowe inputy
@io.on("play_card")
def handle_play_card(index):
    game, player = reference(session)

    card = player.get_card_by_index(index)

    # każdy może rzucić nie nie w każdym momencie
    if not permission(session) and not isinstance(card, Nono): return

    redirect = player.play_card(card)

    if redirect == -1:
        return

    if redirect is not None:
        emit('redirect', redirect)

    emit('reload', to=session["room"])


# Odłożenie bomby do talii
@io.on("defuse")
def handle_defuse(index):
    game, player = reference(session)
    game.deck.insert_bomb(index)
    game.finish_round()

    emit('back', to=session["room"])
    emit("back")


# Przekazanie nowych danych wejściowych do Favor.action()
@io.on("play_favor")
def handle_play_favor(card_index, target, idx1, idx2):
    game, player = reference(session)
    player.play_card_by_index(card_index, target=target, idx1=idx1, idx2=idx2)
    emit('back')


# Wybranie gracza na którym ma działać karta Favor (przysługa)
@io.on("favor_choose_player")
def favor_choose_player(username):
    game, player = reference(session)

    sid = clients[username]
    username = game.player().name
    url = url_for('main.favor', target=username)
    emit('redirect', url, to=sid)
    emit('back')


# Oddanie karty innemu graczowi w ramach zagranej karty Favor (przysługa)
@io.on("favor_give_card")
def favor_give_card(target_username, card_index):
    game, giver = reference(session)

    gifted = game.get_player(target_username)
    gifted.take_card_from(giver, card_index)

    emit('new_card', to=clients[gifted.name])
    emit('back')


# Wybranie gracza na którym mają działać karty Cat
@io.on("cat_choose_player")
def cat_choose_player(username):
    url = url_for('main.cat', target=username)
    emit('redirect', url)


# Zabranie wybranej karty w ramach karty Cat
@io.on("cat_take_card")
def cat_take_card(username, card_index):
    game, gifted = reference(session)

    giver = game.get_player(username)
    gifted.take_card_from(giver, card_index)

    emit('reload', to=clients[giver.name])
    emit('new_card')


# Funkcja pomocnicza
def reference(session):
    game = get_game(session["room"])
    room = session["room"]
    player = game.get_player(session['username'])
    return game, player


def permission(session):
    game, player = reference(session)

    if game.turn.current != player:
        return False

    return True


def room_exists(room):
    if room in rooms:
        return rooms.get(room)
    else:
        return False


def get_game(room) -> Game:
    return rooms[room]


create_room("test", "test", "test1", "test2")
get_game("test").begin()
