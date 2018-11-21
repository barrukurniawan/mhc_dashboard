/*
 * Written by Blipcom PTY LTD
 *
 * 	Authors: Sidnei Budiman
 *
 * */

SG_shuffle_keypad = function() 
{
	var array = [0,1,2,3,4,5,6,7,8,9];
	var currentIndex = array.length, temporaryValue, randomIndex;
  	while (0 !== currentIndex) 
	{
    		randomIndex    	    = Math.floor(Math.random() * currentIndex);
    		currentIndex  	   -= 1;
    		temporaryValue 	    = array[currentIndex];
    		array[currentIndex] = array[randomIndex];
    		array[randomIndex]  = temporaryValue;
  	}

	console.log( array )

	$("#pin_top_left"     ).val(array[0]);
	$("#pin_top_middle"   ).val(array[1]);
	$("#pin_top_right"    ).val(array[2]);

	$("#pin_middle_left"  ).val(array[3]);
	$("#pin_middle_middle").val(array[4]);
	$("#pin_middle_right" ).val(array[5]);

	$("#pin_bottom_left"  ).val(array[6]);
	$("#pin_bottom_middle").val(array[7]);
	$("#pin_bottom_right" ).val(array[8]);

	$("#pin_bottom_bottom_middle").val(array[9]);
}

SG_action_sell = function()
{

	SG_shuffle_keypad();

        var date_now  = new Date();
        var curr_time = date_now.getTime();
        var wallet_id = $("#account_details_id").val();

        AJAX_SERVER_call(
                SG_action_sell_CALLBACK,
                "GET",
                "/api_user_check_balance",
                {curr_time :  curr_time, from_wallet_id : wallet_id },
                true
        );
};

SG_action_sell_CALLBACK = function(msg_data)
{
        var message_action = msg_data.message_action;
        if ( message_action == "USER_CHECK_BALANCE_SUCCESS" )
        {
                var balance = msg_data.message_data.balance;
                var amount  = $("#berat_emas").val();
                if (parseFloat(balance) >= parseFloat(amount))
                {
                        $('#demo-modal-3').modal('toggle');
                }
                else
                {
                        alert("saldo not enough");
                }
        }
};

AJAX_SERVER_call = function(callback_func, method, wservice, uri, bool)
{
        _g_jqxhr = $.ajax(
        {
                url      : wservice ,
                method   : method   ,
                data     : uri      ,
                dataType : "json"
        }).done(
                function(msg_json)
                {
                        callback_func(msg_json);
                }
        ).fail(
                function(msg_json)
                {
                        callback_func(msg_json);
                }
        ).always(
                function()
                {
                }
        );
}

Number.prototype.toFixedDown = function(digits) {
	var re = new RegExp("(\\d+\\.\\d{" + digits + "})(\\d)"),                          m = this.toString().match(re);
       	return m ? parseFloat(m[1]) : this.valueOf();
};

                 $(function() {
                                $('.form_berat_emas').on('input', function() {
                                        this.value = this.value
                                        .replace(/[^\d.]|(\.[\d]{4}).|(\..*)\./g, '$1');
                                });
                        });

$(document).ready(function(){
	$('#berat_emas').keyup(function(){
        $("#sell-gold_rupiah").text(parseFloat($('#berat_emas').val() * buy_price).toFixedDown(4));
        $("#dup_sell-gold_rupiah").text(parseFloat($('#berat_emas').val() * buy_price).toFixedDown(4));
	});
});

$(document).ready(function (){
	$('select').wrap('<div class="select_wrapper"></div>')
        $('select').parent().prepend('<span>'+ $(this).find(':selected').text() +'</span>');
        $('select').parent().children('span').width($('select').width());
        $('select').css('display', 'none');
        $('select').parent().append('<ul class="select_inner"></ul>');
       	$('select').children().each(function(){
        var opttext = $(this).text();
        var optval = $(this).val();
        $('select').parent().children('.select_inner').append('<li id="' + optval + '">' + opttext + '</li>');
 });
 	$('select').parent().find('li').on('click', function (){
        var cur = $(this).attr('id');
       	$('select').parent().children('span').text($(this).text());
        $('select').children().removeAttr('selected');
        $('select').children('[value="'+cur+'"]').attr('selected','selected');
        console.log($('select').children('[value="'+cur+'"]').text());
        });
        $('select').parent().on('click', function (){
        $(this).find('ul').slideToggle('fast');
        });
});
