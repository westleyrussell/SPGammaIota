$(document).ready(function(){

	$('#overview').waypoint(function(direction) {
		if(direction === 'up')
		{
			$('#service-nav .active').removeClass('active');
			$('#overview-nav').addClass('active');
		}
	}, { offset: '25%' });

	$('#guitar').waypoint(function(direction) {
		if(direction === 'down')
		{
			$('#service-nav .active').removeClass('active');
			$('#guitar-nav').addClass('active');
		}

		if(direction == 'up')
		{
			$('#service-nav .active').removeClass('active');
			$('#overview-nav').addClass('active');	
		}
	}, { offset: '25%' });

	$('#ace').waypoint(function(direction) {
		if(direction === 'down')
		{
			$('#service-nav .active').removeClass('active');
			$('#ace-nav').addClass('active');
		}

		if(direction == 'up')
		{
			$('#service-nav .active').removeClass('active');
			$('#guitar-nav').addClass('active');	
		}
	}, { offset: '25%' });

	$('#upcoming').waypoint(function(direction) {
		if(direction === 'down')
		{
			$('#service-nav .active').removeClass('active');
			$('#upcoming-nav').addClass('active');
		}

		if(direction == 'up')
		{
			$('#service-nav .active').removeClass('active');
			$('#ace-nav').addClass('active');	
		}
	}, { offset: '25%' });

	$("#overview-nav").click(function() {

		$('html, body').stop(true, true);

    	$('html, body').animate({
        	scrollTop: $('#overview').offset().top
    	}, 800);
	});

	$("#guitar-nav").click(function() {

		$('html, body').stop(true, true);

    	$('html, body').animate({
        	scrollTop: $('#guitar').offset().top
    	}, 800);
	});

	$("#ace-nav").click(function() {

		$('html, body').stop(true, true);

    	$('html, body').animate({
        	scrollTop: $('#ace').offset().top
    	}, 800);
	});
	$("#upcoming-nav").click(function() {

		$('html, body').stop(true, true);

    	$('html, body').animate({
        	scrollTop: $('#upcoming').offset().top
    	}, 800);
	});
});