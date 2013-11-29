$(document).ready(function(){
	
	$('#secure_nav').sidebar({
		duration: 150,
	});
	
	$('#nav_toggle').click(function(){
			$('#secure_nav').sidebar('toggle');
	});

});