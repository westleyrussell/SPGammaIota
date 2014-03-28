$(document).ready(function(){

	$("#feed").carouFredSel({
		circular: true,
		infinite: true,
		direction: 'left',
		align: 'center',
		width: 1200,
		items : {
			height: 300
		},
		scroll: {
			items: 1,
			easing: "linear",
			duration: 800,
			fx: "crossfade",
		}
	});
});