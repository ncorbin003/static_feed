//gets video

$(document).ready(function(){
if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};

var inbox = new ReconnectingWebSocket(ws_scheme + location.host + "/receive");

  let namespace = "/test";
  photo = document.getElementById('photo');

//  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
//
//  socket.on('connect', function() {
//    console.log('Connected!');
//  });
//
//  socket.on('out-image-event',function(data){
//    var img = new Image();
//
//    img.src = dataURL//data.image_data
//    photo.setAttribute('src', data.image_data);
//
//    });

    inbox.onmessage = function(message) {
        console.log(message);
        var data = JSON.parse(message.data);
        var img = new Image();

        img.src = data//data.image_data
        photo.setAttribute('src', data);
    };

    inbox.onclose = function(){
    console.log('inbox closed');
    this.inbox = new WebSocket(inbox.url);

};

});
