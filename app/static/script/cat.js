const socket = io();

function chooseCard(username, index) {
    socket.emit("cat_take_card", username, index);
}

