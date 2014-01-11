$(document).ready(function(){
	$('.sub-header').css('margin-top','0px'); //can't do this in the css for some reason.

	var thresh = 100; //The height of the top banner
	var subHeight = 63; //height of the top banner
	$(window).scroll(function(e){
		console.log(subHeight,window.scrollY);
		if (window.scrollY > thresh) {
			$('#pub-nav').addClass('fixed');
			$('.sub-header').css('margin-top',subHeight + 'px');
		} else {
			$('#pub-nav').removeClass('fixed');
			$('.sub-header').css('margin-top',0);
		}
	});
});