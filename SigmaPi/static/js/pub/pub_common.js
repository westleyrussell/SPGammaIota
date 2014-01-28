$(document).ready(function(){
	$('#pub-nav').waypoint(function(direction){
		console.log('waypoint');
		if (direction === 'up') {
			$('#pub-nav').removeClass('fixed');
			$('.top-header').removeClass('adjusted');
		} else {
			$('#pub-nav').addClass('fixed');
			$('.top-header').addClass('adjusted');
		}
	});
});