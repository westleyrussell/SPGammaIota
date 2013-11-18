$(document).ready(function(){
	var exec_thresh = $('#exec_start').offset().top
	var sen_thresh = $('#senior_start').offset().top
	var jun_thresh = $('#junior_start').offset().top
	var soph_thresh = $('#sophomore_start').offset().top
	var fresh_thresh = $('#freshman_start').offset().top

	$(window).scroll(function(e){
		$('#brothers-nav .active').removeClass('active');

		if (window.scrollY < sen_thresh) {
			$('#exec-nav').addClass('active');
		} else if (window.scrollY > sen_thresh && window.scrollY < jun_thresh) {
			$('#senior-nav').addClass('active');
		} else if (window.scrollY > jun_thresh && window.scrollY < soph_thresh) {
			$('#junior-nav').addClass('active');
		} else if (window.scrollY > soph_thresh && window.scrollY < fresh_thresh) {
			$('#sophomore-nav').addClass('active');
		} else if (window.scrollY > fresh_thresh) {
			$('#freshman-nav').addClass('active');
		}
	});
});