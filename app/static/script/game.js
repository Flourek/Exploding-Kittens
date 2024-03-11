const socket = io();


$(function () {
    console.log(socket.sid)
    socket.emit("user_join");


    socket.on('favor_give_card', function (url) {
        window.location.href = url;
    });


})

$("#stackButton").click(function() {
        socket.emit("take_card");
});

function play_card(index){
    socket.emit("play_card", index);
}


socket.on('card_played', function () {
    location.href = "?animate=1";
    // $(".played3").addClass("animateCard");
});

