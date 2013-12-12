(function($){
	/*
	Check with the server to see if any guests have been added since the last time we updated our page.
	*/
	function pollServer(){

		$.getJSON('guests/poll',{ last: LAST})
			.success(function(response) {
				if (response.gcount > 0){
					LAST = now();
					response.guests.forEach(function(guest){

					});
				}
			})
			.fail(function(response){
				console.log(response);
			});
	}


	function error(message) {
		/*
		t = $('#error-template');
		$(t).find('.header').text(message);
		$(t).find('.close').click(function(){
			$(t).hide();
		});
		$(t).show();
		*/

		alert(message);
	}
	function addGuest(guest) {

		template = $($('#guest-template').clone());
		form = template.find('form');

		form.find('.name').val(guest.name);
		form.find('.gender').val(guest.gender);
		form.data('id',guest.id);

		list = guest.gender == 'M' ? $('.list.guys') : $('.list.girls');
		template.appendTo(list);
		template.show();
		bindGuestHandlers.call(template);
	}


	function filterGuests(stub) {
		stub = stub.toLowerCase();
		if (stub == '') {
			$('.guest').removeClass('filter');
			return;
		}
		$('.guest').each(function(){
			text = $(this).find('.name').val().toLowerCase();
			console.log(text.substring(0,stub.length),stub);
			if(text.substring(0,stub.length) == stub) {
				$(this).removeClass('filter');
				return true;
			} else {
				$(this).addClass('filter');
			}
		});
	}
	/*
		Submit the guest data in the supplied 
		form field
	*/
	function submitGuest(form) {

		var fdata = form.serialize();
		$.post('guests/create', fdata)
			.success(function(response) {
				addGuest({name: form[0].name.value, gender: form[0].gender.value, id: response});
				form.find('.name').val('');
				var gender = form[0].gender.value == 'M' ? 'guys' : 'girls';
				updateCount(gender,1);
			})
			.fail(function(response){
				error('failed to add guest:' + response.responseText);
			});
	}

	/*
		Send a guest name update to the server, keyed with the guests id
	*/
	function updateGuest(form) {
		data = form.serialize();
		$.post('guests/update/' + form.data('id'),data)
			.success(function(response){
			})	
			.fail(function(response){
				//alert the user that they cannot update this guest
				error(response.responseText);
			});
	}

	/*
		Delete a guest with a given id
	*/
	function deleteGuest(form) {
		$.post('guests/destroy/' + form.data('id'))
			.success(function(){
				form.closest('.guest').slideUp();
				var gender = form[0].gender.value == 'M' ? 'guys' : 'girls';
				console.log('success');
				updateCount(gender,-1);

			})
			.fail(function(respone){
				//alert the user that they cannot delete this guest
				error(response.responseText);
			});
	}


	//Return current unix time
	function now() {
		var d = new Date();
		return d.getTime();
	}

	function bindGuestHandlers (){
		var form = $(this).find('.entry');

		if($(this).hasClass('mine')) {
			/*
			form.keyup(function(){
				var editTimeout = 0;
				//wait a a few seconds, then send an update request
				clearTimeout(editTimeout);
				editTimeout = setTimeout(function(){updateGuest(form);},800);
			});
			*/
			$(this).find('div.delete').click(function(){
				deleteGuest(form);
			});
		}else{
			$(this).find('input.name').prop('disabled',true);
		}
	}

	function updateCount(gender,delta) {
		document.COUNTER[gender] = document.COUNTER[gender] + delta;
		$('#'+gender+'-count').text(document.COUNTER[gender]);

		if (PARTYMODE) {
			$.post('count',{'gender': gender, 'delta': delta})
				.error(function(response){
					error(response.responseText);
				});
		}
	}

	function signin(id) {
		$.post('guests/signIn/' + id)
			.error(function(response){
				alert(response.responseText);
			});
	}

	function signout(id) {
		$.post('guests/signOut/' + id)
			.error(function(response){
				alert(response.responseText);
			});			
	}


	function bindPartyHandlers() {

		$('#partymode-nav .menu').each(function(){
			var gender = $(this).data('gender');
			$(this).find('.button').click(function(){
				if ($(this).hasClass('incr')) {
					updateCount(gender,1);
				} else {
					updateCount(gender,-1);
				}
			});
		});

		var timer;
		$('#filter').keyup(function(){
			var stub = $(this).find('input[name="filter"]').val();
			clearTimeout(timer);
			console.log(stub)
			timer = setTimeout(function(){
				filterGuests(stub);
			},200);
		});

		$('.guest').each(function(){

			var gender = $(this).data('gender');
			var gid = $(this).data('id');
			var cbox = $(this).find('.signin');
			if($(this).hasClass('signedIn'))
				cbox.prop('checked',true);

			console.log(gender,gid,cbox);
			$(this).click(function(){

				if($(this).hasClass('signedIn')) {
					updateCount(gender,-1);
					signout(gid);
					$(this).removeClass('signedIn');
					cbox.prop('checked',false);
				} else {
					updateCount(gender,1);
					signin(gid);
					$(this).addClass('signedIn');
					cbox.prop('checked',true);
				}
			});
		});
	}

	$(document).ready(function(){

		//URL of the party page, this will be different for each party,
		//but only needs to be calculated once
		
		POLL_WAIT = 10000; //10 seconds

		if ($('#filter').length > 0) {
			//we are in partymode
			PARTYMODE = true;
			bindPartyHandlers();
			console.log('binding party mode');

		} else {

			console.log('noparty');
			$('.guestAdd-form').submit(function(e){
				submitGuest($(this));
				return false;
			});

			$('.guest:visible').each(bindGuestHandlers);


			var hidden = null
			$('.my_list').click(function(){
				if ($(this).hasClass('active')) {
					return;
				}

				$(this).addClass('active');
				$('.full_list').removeClass('active');

				hidden = $('.guest:not(.mine)');
				hidden.hide();
			});

			$('.full_list').click(function(){
				if ($(this).hasClass('active')) {
					return;
				}
				$(this).addClass('active');
				$('.my_list').removeClass('active');

				if (hidden) {
					hidden.show();
				}
			})
		}


		LAST = now();
		//setInterval(pollServer, POLL_WAIT);
	});

})(jQuery);