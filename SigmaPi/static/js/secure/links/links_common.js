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

	$('.like_button').click(function() {
		var element = this;
		var link_id = $(this).attr('id');

		var url = link_id + "/like/";
		var like_count_ele = "#"+link_id +".like-counts";
		$.post( url, function( data ) {
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