$(document).ready(function() {

    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('update_text', function(data) {
	$('#message-area').text(data.text);
    });

    socket.on('new_thumbnail', function(data) {
	$('#photos').prepend(data.new_thumbnail_html);
	$('.photo-container').fadeIn();
    });

    socket.on('failed', function(data) {
	$('.action-button').removeClass('disabled');
	$('#message-area').text(data.error);
    });

    socket.on('re-enable', function() {
	$('.action-button').removeClass('disabled');
    });

    $('.action-button').click(function(event) {
	$('.action-button').addClass('disabled');
	var num_pics = $(this).attr('value');

	socket.emit('take_pics', {num_pics: num_pics});
    });

});
