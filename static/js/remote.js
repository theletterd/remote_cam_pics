$(document).ready(function() {

    $('.action-button').click(function(event) {
	var num_frames = $(this).attr('value');

	$.ajax({
	    type: 'POST',
	    url: '/take_pics',
	    data: {framenum: num_frames},
	    success: location.reload(),
	    async: false
	});
    });
});