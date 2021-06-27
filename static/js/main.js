//sends
$(document).ready(function(){
  if (window.location.protocol == "https:") {
    var ws_scheme = "wss://";
  } else {
     var ws_scheme = "ws://"
  };

    var outbox = new ReconnectingWebSocket(ws_scheme + location.host + "/submit");

  let namespace = "/test";
  let video = document.querySelector("#videoElement");
  let canvas = document.querySelector("#canvasElement");
  let ctx = canvas.getContext('2d');
  photo = document.getElementById('photo');
  var localMediaStream = null;

outbox.onclose = function(){
    console.log('outbox closed');
    this.outbox = new WebSocket(outbox.url);
};
  //var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

  function sendSnapshot() {
    if (!localMediaStream) {
      return;
    }

    ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);

    let dataURL = canvas.toDataURL('image/jpeg');
    //socket.emit('input image', dataURL);

    outbox.send(JSON.stringify({ messagetype: 'input image', data: dataURL }));

    //socket.emit('output image')

    outbox.send(JSON.stringify({ messagetype: 'output image'}));

//    var img = new Image();
//    socket.on('out-image-event',function(data){
//
//
//    img.src = dataURL//data.image_data
//    photo.setAttribute('src', data.image_data);
//
//    });


  }

//  socket.on('connect', function() {
//    console.log('Connected!');
//  });

  var constraints = {
    video: {
      width: { min: 640 },
      height: { min: 480 }
    }
  };

  navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
    video.srcObject = stream;
    localMediaStream = stream;

    setInterval(function () {
      sendSnapshot();
    }, 50);
  }).catch(function(error) {
    console.log(error);
  });


});
