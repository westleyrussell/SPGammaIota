$(document).ready(function() {	
	$.fn.dataTableExt.oStdClasses["sFilter"] = "ui label black"
	$.fn.dataTableExt.oStdClasses["sLength"] = "ui label black"
	$.fn.dataTableExt.oStdClasses["sInfo"] = "ui message"
	$.fn.dataTableExt.oStdClasses["sPagePrevEnabled"] = "ui button active"
	$.fn.dataTableExt.oStdClasses["sPagePrevDisabled"] = "ui button disabled"
	$.fn.dataTableExt.oStdClasses["sPageNextEnabled"] = "ui button active"
	$.fn.dataTableExt.oStdClasses["sPageNextDisabled"] = "ui button disabled"
	$('#points_table').dataTable({
		"bSort": false,
	});
	$('#requests_table').dataTable({
		"bSort": false,
	});
	$('#changes_table').dataTable({
		"bSort": false,
	});
	$('#tabs').tabs();

	$( "#modify-points-form" ).dialog({
      autoOpen: false,
      height: 300,
      width: 350,
      modal: true,
      draggable:false,
      resizable:false,
      buttons: {
        "Modify Points": function() {
        },
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });

    $( "#grant-points-form" ).dialog({
      autoOpen: false,
      height: 300,
      width: 350,
      modal: true,
      draggable:false,
      resizable:false,
      buttons: {
        "Approve Request": function() {
        },
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });

    $(".modify-points-button").click(function(){

    	var id = $(this).attr("id");
    	var cur_points = $("#"+id+".points-points-field").first().text();
    	var user = $("#"+id+".points-name-field").first().text();

    	$("#modify-points-form-user").html(user);
    	$("#modify-points-form-points").val(cur_points);
    	$("#modify-points-form").dialog("open");
    });

    $(".approve-points-button").click(function() {
    	$('#grant-points-form').dialog('open');
    });

 
    $( "#create-user" )
      .button()
      .click(function() {
        $( "#dialog-form" ).dialog( "open" );
      });
 });