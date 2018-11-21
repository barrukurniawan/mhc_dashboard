//global variables
var current_page;
var sort_page;
var filter_search;

// date now status post
var today = new Date();
var dd = today.getDate();
var mm = today.getMonth()+1; //January is 0!
var yyyy = today.getFullYear();

if(dd<10) {
    dd = '0'+dd
} 

if(mm<10) {
    mm = '0'+mm
} 
today = mm + '/' + dd + '/' + yyyy;

search_status = function(){
  var current_page = $('#current_page').val();
  var keyword_search = $('#keyword_search').val();
  var sort_page = $('#sort_page').val();
  var filter_search = $('#filter_search').val();
  console.log(sort_page + ' ini adalah sort');
  console.log(current_page + ' ini halaman yang ke load');
  get_status('/api_twitter_status_view', 'subject', keyword_search, current_page, filter_search, sort_page);
}


get_status = function(api, filter, keyword, current_page, filter_search, sort_page){

  GET_status = $.getJSON(api,'keyword=' + keyword + '&filter_search=' + filter_search + '&page=' + current_page + '&sort=' + sort_page, function(data,status) {

    list = "";

    $.each (data.message_data, function (i) {

        list +=  '<div class="cell-8">'+
              '<div class="card bg-blue fg-white">'+
              '<div class="card-content p-2">'+
              '<div class="row">'+
              '<div class="cell-8">'+
              '<h5>' + data.message_data[i].first + ' ' + data.message_data[i].last + ' says :</h5>'+
              '<center>' + '<h3>' + data.message_data[i].subject + '</h3>'+ '</center>' +
              '<p>' + data.message_data[i].date + ' - ' + data.message_data[i].time + '</p>'+
              '</div>'+
              '</div>'+
              '<!-- End row -->'+
              '</div>'+
              '</div>'+
              '<!-- End Card -->'+
              '</div>'+
              '<!-- cell-4 -->';
    });
    $("#tampil").html(list);
  });
};

get_status('/api_twitter_status_view', 'subject', '');

action_add_rooms = function(){

  var fk_user_id     = $("#input_fk_user_id").val();
  var time           = new Date().toLocaleTimeString();
  var date           = today;
  var subject        = $("#input_subject").val();
  var location       = "jakarta";

  AJAX_SERVER_call(
    action_add_room_CALLBACK      ,
    "GET"                         ,
    "/api_twitter_status_proc" ,
    {
      fk_user_id  : fk_user_id     ,
      time        : time           ,
      date        : date           ,
      subject     : subject        ,
      location    : location
    }
  );

};

action_add_room_CALLBACK = function(msg_data){
  var message_action = msg_data.message_action;

  if(message_action == "STATUS_INSERT_SUCCESS"){
    get_status('/api_twitter_status_view', 'subject', '');
    $('#input_subject').val("");
  }
  else{
    alert("failed input data to database");
  }
};

AJAX_SERVER_call = function(callback_func, method, api, parameter){

  _g_jqxhr = $.ajax({
    url      : api        ,
    method   : method     ,
    data     : parameter  ,
    dataType : "json"
  })
  .done(
    function(msg_json){
      callback_func(msg_json);
    }
  )
  .fail(
    function(msg_json){
      callback_func(msg_json);
    }
  )
  .always(
    function(){}
  );
};
