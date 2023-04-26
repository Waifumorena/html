// Conectarse al servidor utilizando WebSocket
var socket = new WebSocket('ws://149.56.67.133:5000/');

// Manejar la recepción de mensajes del servidor
socket.onmessage = function(event) {
  var mensaje = event.data;
  $('#mensajes').append('<div>' + mensaje + '</div>');
}

// Manejar el envío de mensajes desde el formulario de entrada
$('#formulario').submit(function(event) {
  event.preventDefault();
  var mensaje = $('#mensaje').val();
  socket.send(mensaje);
  $('#mensaje').val('');
});
