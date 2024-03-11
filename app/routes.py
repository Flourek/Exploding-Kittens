from flask import Blueprint, render_template, redirect, request, session, url_for

from .events import clients, io, create_room, get_game, room_exists

main = Blueprint("main", __name__)


@main.route('/')
def index():
    return render_template('land.html')


@main.route('/join')
def join():
    session.permanent = True
    username = request.args.get('username')
    room = request.args.get('room')
    session["username"] = username
    session["room"] = room

    if username and room:
        return redirect("lobby")

    return render_template('join.html')


@main.route('/error/')
def error(error="Cos poszlo nie tak"):
    return render_template('error.html', error=error)

# "Stwórz nową grę"
@main.route('/create')
def create():
    session.permanent = True

    username = request.args.get('username')
    if username:
        print(username)
        session["username"] = username

        code = create_room(username)
        session["room"] = code

        return redirect("lobby")

    return render_template('create.html')


# Poczekalnia, tylko host możę rozpocząć gre
@main.route('/lobby')
def lobby():
    if not session.get("username"):
        return error("Zły użytkownik")

    if not room_exists(session["room"]):
        return error("Gra nie istnieje")

    game = get_game(session["room"])
    clients = game.clients
    host: bool = game.host == session["username"]

    return render_template('lobby.html', clients=clients, host=host)


# Głowny widok na rozrywke
@main.route('/game')
def game():
    if not room_exists(session["room"]):
        return error("Gra nie istnieje")

    game = get_game(session["room"])

    if game.winner:
        return win()

    cards = game.get_player(session["username"]).cards
    played = game.played[-3:]
    turn = game.player()
    your_turn = turn.name == session["username"]
    players = game.turn.players

    return render_template('game.html', cards=cards, turn=turn, your_turn=your_turn, players=players, played=played)


# Wybieranie który gracz ma zrobić przysługę, a potem wybieranie którą karte oddać
@main.route('/game/favor/')
@main.route('/game/favor/<target>')
def favor(target=None):
    game = get_game(session["room"])
    alive_players = game.turn.players.copy()
    alive_players.remove(game.player())

    if target is None:
        return render_template('choose.html', players=alive_players, event="favor_choose_player")
    else:
        cards = game.get_player(session["username"]).cards
        return render_template('favor.html', cards=cards, target=target)


@main.route('/game/cat')
@main.route('/game/cat/<target>')
def cat(target=None):
    game = get_game(session["room"])
    alive_players = game.turn.players.copy()
    alive_players.remove(game.player())

    if target is None:
        return render_template('choose.html', players=alive_players, event="cat_choose_player")
    else:
        target_cards = game.get_player(target).cards
        cards_count = len(target_cards)
        return render_template('cat.html', cards_count=cards_count, target=target)


# Co kryje przyszłość
@main.route('/game/future')
def future():
    game = get_game(session["room"])
    cards = game.deck.cards[-3:]

    return render_template('future.html', cards=cards[::-1])


# Przerwanie akcji czyli powrót na strone główną
@main.route('/game/nono')
def nono():
    io.emit('back')
    return redirect(url_for('main.game'))

#
@main.route('/game/win')
def win():
    game = get_game(session["room"])

    winner = game.winner

    if not winner:
        return error("Gra się jeszcze nie skończyła")

    losers = [x.name for x in game.turn.players]
    losers.remove(winner.name)

    return render_template('win.html', winner=winner, losers=losers)

# Kiedy gracz wyciągnie bombę, jeśli rozbroi to może dać karte z powrotem do talii
@main.route('/game/explode/<int:defused>')
def explode(defused=False):
    game = get_game(session["room"])

    if defused:
        defuseCard = game.played[-1][0] if defused else None
        cards_count = len(game.deck.cards)
        return render_template('defuse.html', defuseCard=defuseCard, cards_count=cards_count)
    else:
        return render_template('explode.html')
