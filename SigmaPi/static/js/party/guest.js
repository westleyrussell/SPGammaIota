function pollServer(lastCheck){

	$.getJSON(document.ROOT_URL + '/poll',{
			last: lastCheck
		},
		function(data) {

		}
	);
}

/*
	Submit the guest data in the supplied 
	form field
*/
function submitGuest(field) {

	var gender = field.data('gender');
	var name = field.val();

	$.post(document.ROOT_URL + '/guests/create',{
			name: name,
			gender: gender
		},
		function(response) {
			response = $.parseJSON(response);
		}
	);
}


$(document).ready(function(){

	//URL of the party page, this will be different for each party,
	//but only needs to be calculated once
	

	$('.guest-submit .name').keyup(function(e){
		//listen for the enter keypress, this is when a guest is submitted
		if (e.keyCode == 13) {
			submitGuest($(this));
		}
	});

	d = new Date();
	last = d.getTime();

	setInterval(3000,function(){
		console.log('polling');
		if (pollServer(last)) {
			//new guests added, update timestamp
			d = new Date();
			last = d.getTime();
		}
	});
});