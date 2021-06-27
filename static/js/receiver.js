$(document).ready(function(){
  let namespace = "/test";
  photo = document.getElementById('photo');

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

  socket.on('connect', function() {
    console.log('Connected!');
  });

  socket.on('out-image-event',function(data){
    var img = new Image();

    img.src = dataURL//data.image_data
    photo.setAttribute('src', data.image_data);

    });


});
