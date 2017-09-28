$(document).ready(function() {


    $('.action-button').click(function(event) {
	$('.action-button').addClass('disabled');
	var num_pics = $(this).attr('value');
	var ws = new WebSocket("ws://" + document.location.host + "/take_pics");

	ws.onopen = function() {
	    ws.send(JSON.stringify({num_pics: num_pics}));
	};

	ws.onmessage = function(msgevent) {
	    var payload = $.parseJSON(msgevent.data);
	    if ('text' in payload) {
		$('#message-area').text(payload.text);
	    } else if ('error' in payload) {
		$('#message-area').text(payload.text);
	    } else if ('new_thumbnail_html' in payload) {
		$('#photos').prepend(payload.new_thumbnail_html);
		$('.photo-container').fadeIn();
	    }
	}

	ws.onclose = function() {
	    $('.action-button').removeClass('disabled');
	}
    });



});
