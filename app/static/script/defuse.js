const socket = io();

function choose_index(index){
    index = parseInt(index)
    socket.emit("defuse", index);
}

