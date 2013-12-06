/*
	Check with the server to see if any guests have been added since the last time we updated our page.
*/
function pollServer(){

	$.getJSON('guests/poll',{ last: LAST})
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
	console.log(data)
	$.post('guests/create', data)
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
	console.log('updating...');
	data = form.serialize();
	console.log(data);
	$.post('guests/update/' + form.data('id'),data)
		.success(function(response){
			console.log('success updating!');
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
	$.post('guests/destroy/' + form.data('id'))
		.success(function(){
			form.closest('.guest').slideUp();
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

	$('.guest').each(function(){

		var form = $(this).find('.entry');
		form.keyup(function(){
			var editTimeout = 0;
			//wait a a few seconds, then send an update request
			clearTimeout(editTimeout);
			editTimeout = setTimeout(function(){updateGuest(form);},800);
		});

		$(this).find('.delete').click(function(){
			deleteGuest(form);
		});
	});

	LAST = now();
	setInterval(pollServer, POLL_WAIT);
});