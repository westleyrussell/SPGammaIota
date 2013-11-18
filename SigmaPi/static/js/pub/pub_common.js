$(document).ready(function(){

	parts = document.URL.split('/');
	page = parts[parts.length-1];

	$('#pub-nav .active').removeClass('active');
	switch(page){

		case 'history':
			$('#nav-history').addClass('active');
			break;
		case 'service':
			$('#nav-service').addClass('active');
			break;
		default:
			$('#nav-home').addClass('active');
			break;
	}

	var thresh = 100; //The height of the top banner
	$(window).scroll(function(e){
		if (window.scrollY > thresh) {
			$('#pub-nav').addClass('fixed');
		} else {
			$('#pub-nav').removeClass('fixed');
		}
	});
});