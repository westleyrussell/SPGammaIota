var doers_table;
var givers_table;

$(document).ready(function() {
	setupRequestPointsForm();

	setupRequestCoverForm();
	setupOfferCoverForm();

	setupDataTables();
	$('#tabs').tabs();

	$('.delete-giver-job').click(function() {
		var id = $(this).attr("id");
		deleteCoverRequest(id, false)
	});

	$('.delete-taker-job').click(function() {
		var id = $(this).attr("id");
		deleteCoverRequest(id, true)
	});

	$('.take-job').click(function() {
		var id = $(this).attr("id");
		acceptCoverRequest(id, false)
	});
	
	$('.give-job').click(function() {
		var id = $(this).attr("id");
		acceptCoverRequest(id, true)
	});
});

function setupRequestPointsForm()
{
	$( "#request_points_form" ).dialog({
      autoOpen: false,
      height: 375,
      width: 350,
      modal: true,
      draggable:false,
      resizable:false,
      buttons: {
        "Send Request": function() {
			var witness = $("#id_witness").val();
			var reason = $("#id_reason").val();
			var url = "points/request/";
			var csrftoken = $.cookie('csrftoken');
			$.ajax({
				type:"POST",
				beforeSend: function(xhr, settings) {
			        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
			            // Send the token to same-origin, relative URLs only.
			            // Send the token only if the method warrants CSRF protection
			            // Using the CSRFToken value acquired earlier
			            xhr.setRequestHeader("X-CSRFToken", csrftoken);
			        }				
				},
				url: url,
				data: {
					reason: reason,
					witness: witness
				}
			}).done(function( data ) {
				$('#id_witness').val("");
				$('#id_reason').val("");
				$('#request_points_form').dialog('close');
				$('#request_points_button').text("Request Sent");
			});
		},
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });

	$('#request_points_button').click(function() {
		$('#request_points_form').dialog( 'open' );
	});
}

function setupRequestCoverForm()
{
	$( "#request_cover_form" ).dialog({
	autoOpen: false,
	height: 600,
	width: 400,
	modal: true,
	draggable:false,
	resizable:false,
	buttons: {
	"Send Request": function() {
		var job = $(".request #id_job").first().val();
		var details = $(".request #id_details").first().val();
		sendCoverRequest(job, details, 1);
		
		$(".request #id_job").val("");
		$(".request #id_details").val("");
		$(this).dialog("close");
	},
	Cancel: function() {
	  $( this ).dialog( "close" );
	}
	}
	});

	$('#request_job_take_button').click(function() {
		$('#request_cover_form').dialog( 'open' );
	});
}

function setupOfferCoverForm()
{
	$( "#offer_cover_form" ).dialog({
	autoOpen: false,
	height: 525,
	width: 400,
	modal: true,
	draggable:false,
	resizable:false,
	buttons: {
	"Send Request": function() {
		var job = $(".offer #id_job").first().val();
		var details = $(".offer #id_details").first().val();
		sendCoverRequest(job, details, 2);
		
		$(".offer #id_job").val("");
		$(".offer #id_details").val("");
		$(this).dialog("close");
	},
	Cancel: function() {
	  $( this ).dialog( "close" );
	}
	}
	});

	$('#request_job_button').click(function() {
		$('#offer_cover_form').dialog( 'open' );
	});
}

function setupDataTables()
{
	$.fn.dataTableExt.oStdClasses["sLength"] = "ui label black"
	$.fn.dataTableExt.oStdClasses["sInfo"] = "ui message"
	$.fn.dataTableExt.oStdClasses["sPagePrevEnabled"] = "ui button active"
	$.fn.dataTableExt.oStdClasses["sPagePrevDisabled"] = "ui button disabled"
	$.fn.dataTableExt.oStdClasses["sPageNextEnabled"] = "ui button active"
	$.fn.dataTableExt.oStdClasses["sPageNextDisabled"] = "ui button disabled"
	doers_table = $('#doers_table').dataTable({
		"bFilter":false,
		"bSort": false,
	});
	$('#points_table').dataTable({
							"bFilter":false,
							"bSort": false,
						});
	$('#bones_table').dataTable({
							"bFilter":false,
							"bSort": false,
						});
	givers_table = $('#givers_table').dataTable({
							"bFilter":false,
							"bSort": false,
						});
}

function deleteCoverRequest(requestid, taker)
{
  var url = "jobs/request/delete/"+requestid+"/";
  var csrftoken = $.cookie('csrftoken');
  $.ajax({
    type:"POST",
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }       
     },
    url: url,
  }).done(function( data ) {
  	if(taker)
  	{
		var pos = doers_table.fnGetPosition($("#"+requestid+".jobs-row").get(0));
		doers_table.fnDeleteRow(pos);
  	}
  	else
  	{
		var pos = givers_table.fnGetPosition($("#"+requestid+".jobs-row").get(0));
		givers_table.fnDeleteRow(pos);
  	}

  	updatePoints(data.points);
  	updateRequestCount(data.requestCount);

  	if(data.error)
  	{
  		reportError(data.error);
  	}
  });
}

function acceptCoverRequest(requestid, taker)
{	  
  var url = "jobs/request/take/"+requestid+"/";
  var csrftoken = $.cookie('csrftoken');
  $.ajax({
    type:"POST",
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }       
     },
    url: url,
  }).done(function( data ) {
  	if(data.error)
  	{

  		if(data.delete)
  		{
  			if(taker)
	  		{
				var pos = doers_table.fnGetPosition($("#"+requestid+".jobs-row").get(0));
				doers_table.fnDeleteRow(pos);
	  		}
	  		else
	  		{
				var pos = givers_table.fnGetPosition($("#"+requestid+".jobs-row").get(0));
				givers_table.fnDeleteRow(pos);
	  		}

	  		updateRequestCount(data.requestCount)
  		}
  		reportError(data.error);
  	}
  	else
  	{
	  	if(taker)
	  	{
			var pos = doers_table.fnGetPosition($("#"+requestid+".jobs-row").get(0));
			doers_table.fnDeleteRow(pos);
	  	}
	  	else
	  	{
			var pos = givers_table.fnGetPosition($("#"+requestid+".jobs-row").get(0));
			givers_table.fnDeleteRow(pos);
	  	}
	  	updatePoints(data.points);
	  	updateRequestCount(data.requestCount);
  	}
	
  });	
}

function sendCoverRequest(job, details, type)
{
	var takingJob = type == 2;
	var url = "jobs/request/add/"+type+"/";
	var csrftoken = $.cookie('csrftoken');
	$.ajax({
		type:"POST",
		beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
	            // Send the token to same-origin, relative URLs only.
	            // Send the token only if the method warrants CSRF protection
	            // Using the CSRFToken value acquired earlier
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }				
		},
		url: url,
		data: {
			job: job,
			details: details
		}
	}).done(function( data ) {
		if(data.error)
		{
			reportError(data.error);
		}
		else
		{
			var requester = data.requester;
			var job = data.job;
			var details = data.details;
			var requestCount = data.requestCount;
			var id = data.id;

			if(takingJob)
			{
				var table_data = [requester, job, details, '<button id='+id+' class="ui red tiny button delete-taker-job">Delete</button>']
				doers_table.fnAddData(table_data);
			}
			else
			{
				var table_data = [requester, job, details, '<button id='+id+' class="ui red tiny button delete-giver-job">Delete</button>']
				givers_table.fnAddData(table_data);
			}
      		updateRequestCount(requestCount);
		}
	});
}

function updatePoints(points)
{
	$("#pi-points-ticker").first().text(points + " Pi Points");
}

function updateRequestCount(requestCount)
{
	$("#request-count").first().text(requestCount);
}

function reportError(error)
{
	alert(error);
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}