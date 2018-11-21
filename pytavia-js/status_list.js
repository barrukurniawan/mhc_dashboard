// $(document).ready(function () {
//   	$('#get-data').click(function () {
//   		get_status_user();

//   });
// });
var list;
get_status_user = function(api){
get_status_list = $.getJSON(api, function(data,status) {
		list ="";

		$.each(data.message_data, function (i){

			list += '<div>' + '<h3> my status :' + data.message_data[i].status + '</h3>' + 
					'<h4>' + data.message_data[i].time_status +  '</h4>' + '</div>';
		});
		$("#result_status").html(list);
		console.log(list);
	});
};

get_status_user('/api_status_user_view');
document.getElementById("hasil").append(list);