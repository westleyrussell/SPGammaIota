var requests_table;
var changes_table;
var hours_table;

function initialize() {
  $.fn.dataTableExt.oStdClasses["sFilter"] = "ui label black"
  $.fn.dataTableExt.oStdClasses["sLength"] = "ui label black"
  $.fn.dataTableExt.oStdClasses["sInfo"] = "ui message"
  $.fn.dataTableExt.oStdClasses["sPagePrevEnabled"] = "ui button active"
  $.fn.dataTableExt.oStdClasses["sPagePrevDisabled"] = "ui button disabled"
  $.fn.dataTableExt.oStdClasses["sPageNextEnabled"] = "ui button active"
  $.fn.dataTableExt.oStdClasses["sPageNextDisabled"] = "ui button disabled"
  hours_table = $('#hours_table').dataTable({
    "bSort": false,
  });
  requests_table = $('#requests_table').dataTable({
    "bSort": false,
  });
  changes_table = $('#changes_table').dataTable({
    "bSort": false,
  });
  $('#tabs').tabs();

  $('#reset-hours-button').click(function() {
    $('#reset-hours-form').dialog( 'open' );
  });

  $( "#modify-hours-form" ).dialog({
      autoOpen: false,
      height: 375,
      width: 350,
      modal: true,
      draggable:false,
      resizable:false,
      buttons: {
        "Modify Hours": function() {
          var userid = $(".modify-hours-form-userid").attr("id");
          var hours = $("#modify-hours-form-hours").val();
          modifyHours(userid, hours);

          $("#modify-hours-form-hours").val("");
          $(this).dialog("close");
        },
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });

    $( "#add-brother-form" ).dialog({
      autoOpen: false,
      height: 375,
      width: 350,
      modal: true,
      draggable:false,
      resizable:false,
      buttons: {
        "Add Brother": function() {
          var userid = $("#id_brother").val();
          var hours = $("#id_hours").val();
          modifyHours(userid, hours);

          $("#id_brother").val("");
          $("#id_hours").val("");
          $(this).dialog("close");
        },
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });

    $( "#reset-hours-form" ).dialog({
      autoOpen: false,
      height: 220,
      width: 350,
      modal: true,
      draggable:false,
      resizable:false,
      buttons: {
        "Reset": function() {
          resetHours();
          $(this).dialog("close");
        },
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });
}

function setupClickListeners()
{
    $(".modify-hours-button").click(showModifyHoursForm);

    $(".approve-hours-button").click(approveRequest);
 
    $( "#add-brother" ).click(function() {
        $( "#add-brother-form" ).dialog( "open" );
      });

    $(".deny-request-button").click(denyHoursRequest);
}

function showModifyHoursForm()
{
  var id = $(this).attr("id");
  var cur_hours = $("#"+id+".hours-hours-field").first().text();
  var user = $("#"+id+".hours-name-field").first().text();

  $("#modify-hours-form-user").html(user);
  $(".modify-hours-form-userid").attr("id", id);
  $("#modify-hours-form-hours").val(cur_hours);
  $("#modify-hours-form").dialog("open");
}

function denyHoursRequest()
{
  var id = $(this).attr("id");
  deleteRequest(id);
}

function modifyHours(userid, newhours)
{
  var url = userid+"/";
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
      "hours":newhours,
    },
  }).done(function( data ) {
    var id = data['id'];
    var name = data['name'];
    var oldHours = data['old_hours'];
    var hours = data['hours'];
    var date = data['date'];
    var modifier = data['modifier'];

    //Update the standings if it exists.
    //Check if exists
    if($("#"+id+".hours-row").length > 0)
    {
      $("#"+id+".hours-hours-field").first().html(hours);
    }
    else
    {
      //Otherwise create it.
      var standings_data = [name, hours, '<a id='+id+' class="ui tiny red button deny-request-button">Deny</a>'];
      hours_table.fnAddData(standings_data);
    }

    //Update the change log
    var change_data = [date, modifier, name, oldHours, hours];
    changes_table.fnAddData(change_data);

  });
}

function resetHours()
{
  var url = "reset/";
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
    location.reload();
  });;
}

function approveRequest()
{
  var request_id = $(this).attr("id");
  var url = "request/"+request_id+"/accept/";
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
    var pos = requests_table.fnGetPosition($("#"+request_id+".requests_row").get(0));
    requests_table.fnDeleteRow(pos);
    var id = data['id'];
    var name = data['name'];
    var oldHours = data['old_hours'];
    var hours = data['hours'];
    var date = data['date'];
    var modifier = data['modifier'];

    //Update the standings if it exists.
    //Check if exists
    if($("#"+id+".hours-row").length > 0)
    {
      $("#"+id+".hours-hours-field").first().html(hours);
    }
    else
    {
      //Otherwise create it.
      var standings_data = [name, hours, '<a id='+id+' class="ui tiny red button deny-request-button">Deny</a>'];
      hours_table.fnAddData(standings_data);
    }

    //Update the change log
    var change_data = [date, modifier, name, oldHours, hours];
    changes_table.fnAddData(change_data);
  });
}

function deleteRequest(requestid)
{
  var url = "request/"+requestid+"/delete/";
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
    var pos = requests_table.fnGetPosition($("#"+requestid+".requests_row").get(0));
    requests_table.fnDeleteRow(pos);
  });
}

//Util functions for csrf

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

$(document).ready(function() {	
  initialize();
  setupClickListeners();
 });



