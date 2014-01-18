var changes_open = false;
var expired_open = false;
var probation_table;
$(document).ready(function() {	
	$.fn.dataTableExt.oStdClasses["sFilter"] = "ui label black"
	$.fn.dataTableExt.oStdClasses["sLength"] = "ui label black"
	$.fn.dataTableExt.oStdClasses["sInfo"] = "ui message"
	$.fn.dataTableExt.oStdClasses["sPagePrevEnabled"] = "ui button active"
	$.fn.dataTableExt.oStdClasses["sPagePrevDisabled"] = "ui button disabled"
	$.fn.dataTableExt.oStdClasses["sPageNextEnabled"] = "ui button active"
	$.fn.dataTableExt.oStdClasses["sPageNextDisabled"] = "ui button disabled"
	$('#bones_table').dataTable({
		"bSort": false,
	});
	$('#bone_history_table').dataTable({
		"bSort": false,
	});
	probation_table = $('#probation_table').dataTable({
		"bSort": false,
	});
	$('#expired_bones_table').dataTable({
		"bSort": false,
	});
	$('#bone_datepicker').datepicker();
	$('#probation_datepicker').datepicker();
	$('#tabs').tabs();
	$('#levy_bone_button').click(function() {
		$('#levy_probation_form').slideUp(450);
		$('#levy_bone_form').slideToggle(450);
	});

	$('#levy_bone_cancel').click(function() {
		$('#levy_bone_form').slideToggle(450);
	});

	$('#levy_probation_button').click(function() {
		$('#levy_bone_form').slideUp(450);
		$('#levy_probation_form').slideToggle(450);
	});

	$('#levy_probation_cancel').click(function() {
		$('#levy_probation_form').slideToggle(450);
	});

		// Handler for probation termination
	$('.end-probation').click(function() {
		var id = $(this).attr("id");

		var url = "probation/"+id+"/delete/";
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
			var pos = probation_table.fnGetPosition($("#"+id+".probation-row").get(0));
			probation_table.fnDeleteRow(pos);
		});
	});
} );


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