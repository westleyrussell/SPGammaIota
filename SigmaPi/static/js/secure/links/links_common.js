$(document).ready(function() {
	$('#add_link_button').click(function() {
		$('#add_link_form').slideToggle(450);
	});
	$('#add_link_cancel').click(function() {
		$('#add_link_form').slideToggle(450);
	});

	$('.view_comments').click(function() {
		console.log(this);
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