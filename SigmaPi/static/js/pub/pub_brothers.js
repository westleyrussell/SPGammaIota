$(document).ready(function(){
	var exec_thresh = $('#exec_start').offset().top
	var sen_thresh = $('#senior_start').offset().top
	var jun_thresh = $('#junior_start').offset().top
	var soph_thresh = $('#sophomore_start').offset().top
	var fresh_thresh = $('#freshman_start').offset().top

	var thresh = 100; //$('#banner-top').outerHeight();
	$(window).scroll(function(e){
		if (window.scrollY > exec_thresh) {
			$('#brothers-nav .active').removeClass('active');
			$('#exec-nav').addClass('active');
		}

		if (window.scrollY > sen_thresh) {
			$('#brothers-nav .active').removeClass('active');
			$('#senior-nav').addClass('active');
		}

		if (window.scrollY > jun_thresh) {
			$('#brothers-nav .active').removeClass('active');
			$('#junior-nav').addClass('active');
		}

		if (window.scrollY > soph_thresh) {
			$('#brothers-nav .active').removeClass('active');
			$('#sophomore-nav').addClass('active');
		}
		if (window.scrollY > fresh_thresh) {
			$('#brothers-nav .active').removeClass('active');
			$('#freshman-nav').addClass('active');
		}
	});
});