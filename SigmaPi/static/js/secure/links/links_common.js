var last_checked = 0;
var POLL_WAIT = 10000; //5 seconds

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

function checkForNewCommentsOrLikes()
{
	$.ajax({
		url:"updates/",
		data: { 'last': last_checked },
		type: 'GET',
		dataType: 'json',
		success: function( data ) {
			var links = data.links;
			var comments = data.comments;

			// Handle counts first
			for(var i = 0; i < links.length; i++)
			{
				var link = links[i];
				var id = link.pk;
				var commentCount = link.commentCount;
				var likeCount = link.likeCount;

				// Like counts
				var like_count_ele = "#"+id+".like-counts";
				var like_word_ele = "#"+id+".like-word";
				$(like_count_ele).first().text(likeCount);

				// Properly pluralize the like label.
				if(likeCount == 1)
				{
					$(like_word_ele).first().text("Like");
				}
				else
				{
					$(like_word_ele).first().text("Likes");	
				}

				//	Comment counts
				var comment_count_ele = "#"+id+".comment-counts";
				var comment_word_ele = "#"+id+".comment-word";

				$(comment_count_ele).first().text(commentCount);
				if(commentCount == 1)
				{
					$(comment_word_ele).first().text("Comment");
				}
				else
				{
					$(comment_word_ele).first().text("Comments");
				}
			}

			// Add in the new comments.
			for(var i = 0; i < comments.length; i++)
			{
				var comment = comments[i];
				var text = comment.content;
				var date = comment.date;
				var id = comment.pk;
				var commentor = comment.poster;
				var element_ider = "#"+id+".comments-list";


				template = $($("#comments-template").clone());
				template.removeClass("hidden");
				template.find('.author').html(commentor);
				template.find('.date').html(date);
				template.find('.comment_text').html(text);
				template.appendTo($(element_ider).first());
				template.show();
			}

			last_checked = new Date() / 1000;
			setTimeout(checkForNewCommentsOrLikes, POLL_WAIT);
		}
	})
}

$(document).ready(function() {

	last_checked = new Date() / 1000;

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
		var text_ider = '#'+id+'.comment-text';
		var text = $(text_ider).val();
		
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
		}).done(function( data ) {

			$(text_ider).val("");
			var element_ider = "#" + id + ".comments-list";
			var author = data.author;
			var date = data.date;
			var comment = data.comment;
			var count = data.commentCount;

			template = $($("#comments-template").clone());
			template.removeClass("hidden");
			template.find('.author').html(author);
			template.find('.date').html(date);
			template.find('.comment_text').html(comment);
			template.appendTo($(element_ider).first());
			template.show();

			var comment_count_ele = "#"+id+".comment-counts";
			var comment_word_ele = "#"+id+".comment-word";

			$(comment_count_ele).first().text(count);
			if(count == 1)
			{
				$(comment_word_ele).first().text("Comment");
			}
			else
			{
				$(comment_word_ele).first().text("Comments");
			}
		});
	});

	// Handler of like button being clicked.
	$('.like_button').click(function() {
		var link_id = $(this).attr('id');
		var like_count_ele = "#"+link_id +".like-counts";
		var link_word_ele = "#"+link_id + ".like-word";
		var csrftoken = $.cookie('csrftoken');
		var url = link_id + "/like/";
		var element = this;
		var was_liked = $(element).attr('name') == "y";

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
			// Update the text of the button and the like count.
			if(was_liked)
			{
				$(element).text("Like");
				$(element).attr('name', "n");
				$(like_count_ele).first().text(data.likes);
			}
			else
			{
				$(element).text("Unlike");
				$(element).attr('name', "y");
				$(like_count_ele).first().text(data.likes);
			}

			// Properly pluralize the like label.
			if(data.likes == "1")
			{
				$(link_word_ele).first().text("Like");
			}
			else
			{
				$(link_word_ele).first().text("Likes");	
			}
		});
	});

	$('.ui.checkbox')
  		.checkbox();
  		
	checkForNewCommentsOrLikes();
});