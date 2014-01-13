$(document).ready(function() {

	last_checked = new Date() / 1000;

	$('#request_points_button').click(function() {
		$('#request_points_form').slideToggle(450);
	});
	$('#request_points_cancel').click(function() {
		$('#request_points_form').slideToggle(450);
	});

	// Handler for pi point request
	$('#send_request_button').click(function() {
		var witness = $("#id_witness").val();
		var reason = $("#id_reason").val();
		var url = "points/request/";
		var csrftoken = $.cookie('csrftoken');
		$.ajax({
			type:"POST",
			beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
		            // Send the token to same-origin, relative URLs only.
		            // Send the token only if the method warrants CSRF protection
		            // Using the CSRFToken value acquired earlier
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }				
			},
			url: url,
			data: {
				reason: reason,
				witness: witness
			}
		}).done(function( data ) {
			$('#id_witness').val("");
			$('#id_reason').val("");
			$('#request_points_form').slideToggle(450);
			$('#request_points_button').text("Request Sent");
		});
	});
});


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}