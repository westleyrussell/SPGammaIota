$(document).ready(function(){

	$('#feed').carouFredSel({
		circular: true,
		infinite: true,
		responsive: true,
		direction: 'left',
		align: 'center',
		width: '100%',
		scroll : {
			items: 1,
			easing: "linear",
			duration: 800,
			fx: "directscroll",
			pauseOnHover: true
		}
	});
});