const socket = io();


$('a').click( function () {
    username = $(this).html().trim()
    socket.emit(event, username);      // cat_choose_player favor_choose_player
});

