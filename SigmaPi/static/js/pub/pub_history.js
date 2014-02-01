$(document).ready(function(){

	$('#founding').waypoint(function(direction) {
		if(direction === 'up')
		{
			$('#history-nav .active').removeClass('active');
			$('#founding-nav').addClass('active');
		}
	}, { offset: '25%' });

	$('#rebuilding').waypoint(function(direction) {
		if(direction === 'down')
		{
			$('#history-nav .active').removeClass('active');
			$('#rebuilding-nav').addClass('active');
		}

		if(direction == 'up')
		{
			$('#history-nav .active').removeClass('active');
			$('#founding-nav').addClass('active');	
		}
	}, { offset: '25%' });

	$('#present').waypoint(function(direction) {
		if(direction === 'down')
		{
			$('#history-nav .active').removeClass('active');
			$('#present-nav').addClass('active');
		}

		if(direction == 'up')
		{
			$('#history-nav .active').removeClass('active');
			$('#rebuilding-nav').addClass('active');	
		}
	}, { offset: '25%' });

	$("#present-nav").click(function() {

		$('html, body').stop(true, true);

    	$('html, body').animate({
        	scrollTop: $('#present').offset().top
    	}, 800);
	});

	$("#founding-nav").click(function() {

		$('html, body').stop(true, true);

    	$('html, body').animate({
        	scrollTop: $('#founding').offset().top
    	}, 800);
	});

	$("#rebuilding-nav").click(function() {

		$('html, body').stop(true, true);

    	$('html, body').animate({
        	scrollTop: $('#rebuilding').offset().top
    	}, 800);
	});
});