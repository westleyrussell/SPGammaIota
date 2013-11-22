$(document).ready(function(){

	$('#senior').waypoint(function(direction) {
		if(direction === 'up')
		{
			$('#brothers-nav .active').removeClass('active');
			$('#exec-nav').addClass('active');
		}
	}, { offset: '25%' });

	$('#senior').waypoint(function(direction) {
		if(direction === 'down')
		{
			$('#brothers-nav .active').removeClass('active');
			$('#senior-nav').addClass('active');
		}
	}, { offset: '25%' });

	$('#junior').waypoint(function(direction) {
		if(direction === 'up')
		{
			$('#brothers-nav .active').removeClass('active');
			$('#senior-nav').addClass('active');
		}
	}, { offset: '25%' });

	$('#junior').waypoint(function(direction) {
		if(direction === 'down')
		{
			$('#brothers-nav .active').removeClass('active');
			$('#junior-nav').addClass('active');
		}
	}, { offset: '25%' });

	$('#sophomore').waypoint(function(direction) {
		if(direction === 'up')
		{
			$('#brothers-nav .active').removeClass('active');
			$('#junior-nav').addClass('active');
		}
	}, { offset: '25%' });

	$('#sophomore').waypoint(function(direction) {
		if(direction === 'down')
		{
			$('#brothers-nav .active').removeClass('active');
			$('#sophomore-nav').addClass('active');
		}
	}, { offset: '25%' });

	$('#freshman').waypoint(function(direction) {
		if(direction === 'up')
		{
			$('#brothers-nav .active').removeClass('active');
			$('#sophomore-nav').addClass('active');
		}
	}, { offset: '25%' });

	$('#freshman').waypoint(function(direction) {
		if(direction === 'down')
		{
			$('#brothers-nav .active').removeClass('active');
			$('#freshman-nav').addClass('active');
		}
	}, { offset: '25%' });



	$("#exec-nav").click(function() {

		$('html, body').stop(true, true);

    	$('html, body').animate({
        	scrollTop: $('#exec').offset().top
    	}, 1000);
	});

	$("#senior-nav").click(function() {

		$('html, body').stop(true, true);

    	$('html, body').animate({
        	scrollTop: $('#senior').offset().top
    	}, 1000);
	});

	$("#junior-nav").click(function() {

		$('html, body').stop(true, true);

    	$('html, body').animate({
        	scrollTop: $('#junior').offset().top
    	}, 1000);
	});

	$("#sophomore-nav").click(function() {

		$('html, body').stop(true, true);

    	$('html, body').animate({
        	scrollTop: $('#sophomore').offset().top 
    	}, 1000);
	});

	$("#freshman-nav").click(function() {

		$('html, body').stop(true, true);

    	$('html, body').animate({
        	scrollTop: $('#freshman').offset().top
    	}, 1000);
	});
});