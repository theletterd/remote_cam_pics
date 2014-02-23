$(document).ready(function() {

/*    $('.action-button').click(function(event) {
	var num_frames = $(this).attr('value');

	$.ajax({
	    type: 'POST',
	    url: '/take_pics',
	    data: {framenum: num_frames},
	    success: location.reload(),
	    async: false
	});
    });
*/
    $('.action-button').click(function(event) {
	// maybe it makes sense to disable all the buttons here.
	$('.action-button').addClass('disabled');

	var num_pics = $(this).attr('value');

	var ws = new WebSocket("ws://" + document.location.host + "/ws_take_pics");

	ws.onopen = function() {
	    ws.send(JSON.stringify({num_pics: num_pics}));
	};

	ws.onmessage = function(msgevent) {
	    var message = $.parseJSON(msgevent.data);
	    if ('text' in message) {
		$('#message-area').text(message.text);
	    }
	    if ('new_thumbnail_html' in message) {
		$('#photos').prepend(message.new_thumbnail_html);
	    }
	};

	ws.onclose = function(msgevent) {
	    $('.action-button').removeClass('disabled');
	};

	// an then re-enable here, or on on-close.
    });
});