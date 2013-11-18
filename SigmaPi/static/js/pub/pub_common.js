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

	var thresh = 100; //$('#banner-top').outerHeight();
	$(window).scroll(function(e){
		if (window.scrollY > thresh) {
			$('#pub-nav').addClass('fixed');
		} else {
			$('#pub-nav').removeClass('fixed');
		}
	});
});