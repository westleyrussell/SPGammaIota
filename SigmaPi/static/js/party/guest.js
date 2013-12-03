/*
	Check with the server to see if any guests have been added since the last time we updated our page.
*/
function pollServer(){

	$.getJSON(document.ROOT_URL + '/guests/poll',{ last: LAST})
		.success(function(response) {
			if (response.gcount > 0){
				LAST = now();
				console.log(LAST);
				response.guests.forEach(function(guest){

				});
			}
		})
		.fail(function(response){
			console.log(response);
		});
}

/*
	Submit the guest data in the supplied 
	form field
*/
function submitGuest(form) {

	data = form.serialize();
	$.post('/create', data)
		.success(function(response) {
			data = $.parseJSON(response);
			form.find('.name').val('');
		})
		.fail(function(response){
			console.log('failed to add guest');
		});
}

/*
	Send a guest name update to the server, keyed with the guests id
*/
function updateGuest(form) {
	data = form.serialize();
	$.post('/update/:' + form.data('id'),data)
		.success(function(response){

		})
		.fail(function(response){
			//alert the user that they cannot update this guest
			console.log(response);
		});
}

/*
	Delete a guest with a given id
*/
function deleteGuest(form) {
	$.post('/delete/:' + form.data('id'))
		.success(function(){
			//remove the guest
		})
		.fail(function(respone){
			//alert the user that they cannot delete this guest
			console.log(response);
		});
}


//Return current unix time
function now() {
	var d = new Date();
	return d.getTime();
}

$(document).ready(function(){

	//URL of the party page, this will be different for each party,
	//but only needs to be calculated once
	
	POLL_WAIT = 10000; //10 seconds

	$('.guestAdd-form').submit(function(e){
		submitGuest($(this));
		return false;
	});

	$('.entry').each(function(){
		var editTimeout = 0;
		var form = $(this)
		form.keyup(function(){
			//wait a a few seconds, then send an update request
			clearTimeout(editTimeout);
			editTimeout = setInterval(function(){updateGuest(form);},2000);
		});
	});

	LAST = now();

	setInterval(pollServer, POLL_WAIT);
});