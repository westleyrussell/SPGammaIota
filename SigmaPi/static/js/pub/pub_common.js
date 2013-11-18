$(document).ready(function(){
	parts = document.URL.split('/');

	first_url = parts[3];
	second_url = parts[4];
	zero_url = parts[2];

	$('#pub-nav .active').removeClass('active');

	if(first_url)
	{
		switch(first_url){
			case 'users':
				$('#nav-brothers').addClass('active');
				break;
			case 'history':
				$('#nav-history').addClass('active');
				break;
			case 'service':
				$('#nav-service').addClass('active');
				break;
			}
	}
	else
	{
		$('#nav-home').addClass('active');
	}
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