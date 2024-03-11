const socket = io();

function give_card(index, username){
    socket.emit("favor_give_card", username, index);
}

