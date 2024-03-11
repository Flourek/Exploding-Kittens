var item = document.getElementById("cards");

  window.addEventListener("wheel", function (e) {
    if (e.deltaY > 0) item.scrollLeft += 100;
    else item.scrollLeft -= 100;
  });


socket.on('back', function() {
    window.location.href = "/game";
});

socket.on('new_card', function(url) {
    // Redirect to the specified URL
    window.location.href = "/game?new_card=1";

});

socket.on('redirect', function(url) {
    // Redirect to the specified URL
    window.location.href = url;
});


socket.on('reload', function () {
    location.reload();
});