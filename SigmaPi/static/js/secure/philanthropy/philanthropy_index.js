$(document).ready(function() {
  $( "#request_hours_form" ).dialog({
      autoOpen: false,
      height: 375,
      width: 350,
      modal: true,
      draggable:false,
      resizable:false,
      buttons: {
        "Send Request": function() {
			var hours = $("#id_hours").val();
			var activity = $("#id_activity").val();
			var description = $("#id_description").val();
			var url = "hours/request/";
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
					hours: hours,
					activity: activity,
					description: description
				}
			}).done(function( data ) {
				$('#id_hours').val("");
				$('#id_activity').val("");
				$('#id_description').val("");
				$('#request_hours_form').dialog('close');
				$('#request_hours_button').text("Request Sent");
			});
		},
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });

	$('#request_hours_button').click(function() {
		$('#request_hours_form').dialog( 'open' );
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