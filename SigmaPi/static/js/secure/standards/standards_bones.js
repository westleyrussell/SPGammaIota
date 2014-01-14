var changes_open = false;
var expired_open = false;
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
	$('#probation_table').dataTable({
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
} );