var requests_table;
var changes_table;
var points_table;

function initialize() {
  $.fn.dataTableExt.oStdClasses["sFilter"] = "ui label black"
  $.fn.dataTableExt.oStdClasses["sLength"] = "ui label black"
  $.fn.dataTableExt.oStdClasses["sInfo"] = "ui message"
  $.fn.dataTableExt.oStdClasses["sPagePrevEnabled"] = "ui button active"
  $.fn.dataTableExt.oStdClasses["sPagePrevDisabled"] = "ui button disabled"
  $.fn.dataTableExt.oStdClasses["sPageNextEnabled"] = "ui button active"
  $.fn.dataTableExt.oStdClasses["sPageNextDisabled"] = "ui button disabled"
  points_table = $('#points_table').dataTable({
    "bSort": false,
  });
  requests_table = $('#requests_table').dataTable({
    "bSort": false,
  });
  changes_table = $('#changes_table').dataTable({
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
          var userid = $(".modify-points-form-userid").attr("id");
          var points = $("#modify-points-form-points").val();
          modifyPiPoints(userid, points);

          $("#modify-points-form-points").val("");
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
          var points = $("#id_piPoints").val();
          modifyPiPoints(userid, points);

          $("#id_brother").val("");
          $("#id_piPoints").val("");
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
    $(".modify-points-button").click(showModifyPointsForm);

    $(".approve-points-button").click(approveRequest);
 
    $( "#add-brother" ).click(function() {
        $( "#add-brother-form" ).dialog( "open" );
      });

    $(".deny-request-button").click(denyPointsRequest);
}

function showModifyPointsForm()
{
  var id = $(this).attr("id");
  var cur_points = $("#"+id+".points-points-field").first().text();
  var user = $("#"+id+".points-name-field").first().text();

  $("#modify-points-form-user").html(user);
  $(".modify-points-form-userid").attr("id", id);
  $("#modify-points-form-points").val(cur_points);
  $("#modify-points-form").dialog("open");
}

function denyPointsRequest()
{
  var id = $(this).attr("id");
  deleteRequest(id);
}

function modifyPiPoints(userid, newpoints)
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
      "piPoints":newpoints,
    },
  }).done(function( data ) {
    var id = data['id'];
    var name = data['name'];
    var oldPoints = data['old_points'];
    var points = data['points'];
    var date = data['date'];
    var modifier = data['modifier'];

    //Update the standings if it exists.
    //Check if exists
    if($("#"+id+".points-row").length > 0)
    {
      $("#"+id+".points-points-field").first().html(points);
    }
    else
    {
      //Otherwise create it.
      var standings_data = [name, points, '<a id='+id+' class="ui tiny red button modify-points-button">Modify Points</a>'];
      points_table.fnAddData(standings_data);
    }

    //Update the change log
    var change_data = [date, modifier, name, oldPoints, points];
    changes_table.fnAddData(change_data);

  });
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
    var oldPoints = data['old_points'];
    var points = data['points'];
    var date = data['date'];
    var modifier = data['modifier'];

    //Update the standings if it exists.
    //Check if exists
    if($("#"+id+".points-row").length > 0)
    {
      $("#"+id+".points-points-field").first().html(points);
    }
    else
    {
      //Otherwise create it.
      var standings_data = [name, points, '<a id='+id+' class="ui tiny red button modify-points-button">Modify Points</a>'];
      points_table.fnAddData(standings_data);
    }

    //Update the change log
    var change_data = [date, modifier, name, oldPoints, points];
    changes_table.fnAddData(change_data);

    //Update the count
    $("#pprCount").first().html(data.pprCount);
    $("#pprCount2").first().html(data.pprCount);
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
    $("#pprCount").first().html(data.pprCount);
    $("#pprCount2").first().html(data.pprCount);
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



