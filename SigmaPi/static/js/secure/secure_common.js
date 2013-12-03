$(document).ready(function(){
	
	$('#secure_nav').sidebar({
		duration: 150,
	});

	$('.ui.dropdown')
  		.dropdown({
  			on: 'hover'
  		})
	;
	
	$('#nav_toggle').click(function(){
			$('#secure_nav').sidebar('toggle');
	});

});