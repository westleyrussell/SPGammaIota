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

$(document).ready(function() {
	$('#add_link_button').click(function() {
		$('#add_link_form').slideToggle(450);
	});
	$('#add_link_cancel').click(function() {
		$('#add_link_form').slideToggle(450);
	});

	$('.view_comments').click(function() {
		var element = this;
		var link_id = $(element).attr('id');
		var comments = "#"+link_id + ".comments";
		$(comments).first().slideToggle(450);
		if($(element).first().text() == "View Comments")
		{
			$(element).first().text("Hide Comments");
		}
		else
		{
			$(element).first().text("View Comments");
		}
	});

	$('.comment-button').click(function() {
		var id = $(this).attr('id');
		var text = $('#'+id+'.comment-text').val();
		
		var url = id + "/comment/";

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
				comment: text
			}
		}).done(function(msg) {
			console.log("Success!");
		});
	});

	$('.like_button').click(function() {
		var element = this;
		var link_id = $(this).attr('id');

		var url = link_id + "/like/";
		var like_count_ele = "#"+link_id +".like-counts";

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
		}).done(function( data ) {
			if($(element).text() == "Dislike")
			{
				$(element).text("Like");
				$(like_count_ele).first().text(data.likes);
			}
			else
			{
				$(element).text("Dislike");
				$(like_count_ele).first().text(data.likes);
			}
		});
	});
});