var g_uniq_code        = 0;
var g_total_rupiah     = 0;
var g_final_cash_amt   = 0;
var g_deposit_amt      = 0;
var g_max_rupiah       = 100000000;

//
// Currently selected bank details once clicked
//
var g_bank_name        = 0;
var g_bank_image       = 0;
var g_bank_instruction = 0;
var g_bank_acc_num     = 0;
var g_bank_acc_name    = 0;

BG_action_deposit = function()
{
	//
	// Set time for every request
	//
        var date_now     = new Date();
        var curr_time    = date_now.getTime();

	//
	// Screen elements set
	//
	var wallet_id    = $("#account_details_id").val();

	//
	// Global variables set
	//
	var amount       = g_deposit_amt   ;
	var fk_cust_id   = g_customer_id   ;
	var cash_amt     = g_final_cash_amt;
	var ori_cash_amt = g_total_rupiah  ;
	var unique_num   = g_uniq_code	   ;
	
	var http_params  = {
		from_wallet_id 	: wallet_id	  ,
		fk_customer_id 	: fk_cust_id	  ,
		amount         	: amount	  ,
		cash_amt	: cash_amt	  ,
		ori_cash_amt	: ori_cash_amt	  ,
		unique_num	: unique_num	  ,
		bank_accn_no	: g_bank_acc_num  ,
		bank_accn_nm	: g_bank_acc_name ,
		bank_name	: g_bank_name
	};	
	console.log( http_params );
	//
	// Send to the server
	//
	
		
	$("#nomor_rekening_id"   ).html( g_bank_acc_num );
	$("#bank_display_logo_id").attr( "src" , g_bank_image );
        AJAX_SERVER_call(
                BG_action_deposit_CALLBACK,
                "GET",
                "/api_user_deposit_preapproval_proc",
		http_params,
                true
        );
};

BG_action_deposit_CALLBACK = function(msg_data)
{
        var message_action = msg_data.message_action;
        if ( message_action == "USER_DEPOSIT_PREAPPROVAL_SUCCESS" )
        {
				
        }
};

BG_finalise_total_amount = function()
{
	var date_now  = new Date();
	var curr_time = date_now.getTime();
        AJAX_SERVER_call(
                BG_finalise_total_amount_CALLBACK,
                "GET"              ,
                "/api_user_deposit_uniq_num_gen",
                { 
			time 	 : curr_time,
			cash_amt : g_total_rupiah
		},
                true
        );		
};

BG_finalise_total_amount_CALLBACK = function(msg_data)
{
        var message_action  = msg_data.message_action;
        if ( message_action == "GEN_UNIQ_NUM_SUCCESS" )
        {
		var message_data = msg_data.message_data    ;
		var uniq_num     = message_data.uniq_id     ;
		var new_cash_amt = message_data.new_cash_amt;
		//
		// set the global here for the posting
		//
		g_final_cash_amt = new_cash_amt;

		$("#uniq_code_display" ).text("-" + uniq_num);
		$("#dup_total_rupiah_2").text("Rp." + thousand_format(new_cash_amt));
		g_uniq_code = parseInt(uniq_num);
        }
};

BG_get_paymethod_details = function(action_id)
{
	var date_now  = new Date();
	var curr_time = date_now.getTime();
        AJAX_SERVER_call(
                BG_get_paymethod_details_CALLBACK,
                "GET"              ,
                "/api_get_payment_detail",
                { time : curr_time, action_id : action_id },
                true
        );
};

BG_get_paymethod_details_CALLBACK = function(msg_data)
{
        var message_action  = msg_data.message_action;
        if ( message_action == "GET_PAYMENT_METHOD_DATA_SUCCESS" )
        {
		var pkey     	   = msg_data.message_data.config_rec.pkey;
		var message_data   = msg_data.message_data.config_rec.misc;

		g_bank_name        = message_data.bank_name;
		g_bank_image       = message_data.bank_image;
		g_bank_instruction = message_data.bank_instruction;
		g_bank_acc_num     = message_data.bank_acc_num;
		g_bank_acc_name    = message_data.bank_acc_name;
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


////////////////// ALL FUNCTIONS BELOW HERE ARE TO DISPLAY THE PRICE ON THE DIALOGS /////////////////////

sendEvent = function(sel, step, payment_id) 
{
	BG_get_paymethod_details( payment_id );
	BG_finalise_total_amount();
	$(sel).trigger('next.m.' + step);
}

Number.prototype.toFixedDown = function(digits) 
{
	var re = new RegExp("(\\d+\\.\\d{" + digits + "})(\\d)"),
	m      = this.toString().match(re);
	return m ? parseFloat(m[1]) : this.valueOf();
};

thousand_format = function(num)
{
        var n = num.toString(), p = n.indexOf('.');
        return n.replace(/\d(?=(?:\d{3})+(?:\.|$))/g, function($0, i){
                return p<0 || i<p ? ($0+',') : $0;
        });
}

$(document).ready(
	function()
	{
		//
		// Don't allow any other data to go into the 
		// 	field if its not a number
		//
		document.getElementById("berat_emas").addEventListener(
			"keypress", 
			function (evt) 
			{
				if (
					 (evt.which < 46 || evt.which > 57) && 
					!(evt.which == 8 || evt.which == 0 || evt.which == 46)
				)
				{
					evt.preventDefault();
			    	}
			}
		);
		document.getElementById("jumlah_dana").addEventListener(
			"keypress", 
			function (evt) 
			{
				if (
					 (evt.which < 46 || evt.which > 57 ) && 
					!(evt.which == 0 || evt.which == 8 || evt.which == 46 )
				)
				{
					evt.preventDefault();
			    	}
			}
		);
		$('#berat_emas').keyup(
			function()
			{
				var berat_emas   = null;
				var fee_total    = null;
				var fee_pajak    = null;

				var berat_emas   = ( $('#berat_emas').val());
				var c_berat_emas = berat_emas.replace(/\s/g, "");
				if (berat_emas.length != 0) 
				{
					var fee_total    = ( $('#berat_emas').val() * buy_price);	
					var fee_pajak    = (($('#berat_emas').val() * buy_price) * (npwp/100));
					
					var total_rupiah = parseFloat((fee_total) + (fee_pajak)).toFixedDown(4);

					g_total_rupiah   = Math.round( total_rupiah );
					g_deposit_amt    = berat_emas;

					if ( g_total_rupiah > g_max_rupiah )
					{
						var max_grams          = (g_max_rupiah / buy_price)
						var berat_emas         = max_grams
						var fix_fee_total      = parseFloat(max_grams)  * buy_price
						var fix_fee_pajak      = fix_fee_total * (npwp/100)
						var fix_total_rupiah   = parseFloat((fix_fee_total) + (fix_fee_pajak)).toFixedDown(4);
						var final_rupiah_value = "Rp." + thousand_format(Math.round( fix_fee_total ));

						g_total_rupiah = Math.round ( fix_total_rupiah );
						g_deposit_amt  = berat_emas;

						$('#berat_emas').val(max_grams.toFixedDown(4));
						$("#rp").text( g_max_rupiah );					


						$("#rp"                 ).text( final_rupiah_value );
						$('#gram'               ).text(berat_emas.toFixedDown(4));
						$('#dup_gram'           ).text(berat_emas.toFixedDown(4));
						$('#dup_gram_2'         ).text(berat_emas.toFixedDown(4));
						$('#rupiah'             ).text(berat_emas.toFixedDown(4));
						$('#dup_rupiah'         ).text(berat_emas.toFixedDown(4));
						$('#dup_rupiah_2'       ).text(berat_emas.toFixedDown(4));
						$("#total_cashout"      ).text(final_rupiah_value);
						$("#dup_total_cashout"  ).text(final_rupiah_value);
						$("#dup_total_cashout_2").text(final_rupiah_value);
						$("#fee_pajak"          ).text(final_rupiah_value);
						$("#dup_fee_pajak"      ).text(final_rupiah_value);
						$("#total_rupiah"       ).text("Rp." + thousand_format(g_total_rupiah));
						$("#dup_total_rupiah"   ).text("Rp." + thousand_format(g_total_rupiah));
						$("#dup_total_rupiah_2" ).text("Rp." + thousand_format(g_total_rupiah));
						return
					}
					var final_rupiah_value = Math.round(parseFloat(fee_total).toFixedDown(4));
					var final_rupiah_value = "Rp." + thousand_format( final_rupiah_value );
					$("#rp"			).text( final_rupiah_value );
					$('#gram'		).text(berat_emas);
					$('#dup_gram'		).text(berat_emas);
					$('#dup_gram_2'		).text(berat_emas);
					$('#rupiah'		).text(berat_emas);
					$('#dup_rupiah'		).text(berat_emas);
					$('#dup_rupiah_2'	).text(berat_emas);
					$("#total_cashout"	).text(final_rupiah_value);
					$("#dup_total_cashout"	).text(final_rupiah_value);
					$("#dup_total_cashout_2").text(final_rupiah_value);
					$("#fee_pajak"		).text(final_rupiah_value);
					$("#dup_fee_pajak"	).text(final_rupiah_value);
					$("#total_rupiah"	).text("Rp." + thousand_format(g_total_rupiah));
					$("#dup_total_rupiah"	).text("Rp." + thousand_format(g_total_rupiah));
					$("#dup_total_rupiah_2"	).text("Rp." + thousand_format(g_total_rupiah));
				}
				else
				{
					$("#rp"   ).text("");
					$('#gramz').text("");
				}
			}
		);
  		$('#jumlah_dana').keyup(
			function()
			{
				var calc_gram  = parseFloat($('#jumlah_dana').val() / buy_price).toFixedDown(4);
   				$('#gramz').text(calc_gram);

                                var berat_emas  = null;
                                var fee_total   = null;
                                var fee_pajak   = null;

                                var berat_emas  = calc_gram;
                                var fee_total   = Math.round(calc_gram * buy_price);
                                var fee_pajak   = Math.round(calc_gram * buy_price * (npwp/100));
                                var c_calc_gram = $('#jumlah_dana').val().replace(/\s/g, "");

                                g_total_rupiah  = parseFloat((fee_total) + (fee_pajak)).toFixedDown(4);
				g_deposit_amt   = berat_emas;

				var buy_cash_amount = parseFloat($('#jumlah_dana').val());
                                if (  buy_cash_amount > g_max_rupiah )
                                {
                                        var max_grams = (g_max_rupiah / buy_price)
                                        $('#gramz').text(max_grams.toFixedDown(4));
					$('#jumlah_dana').val(g_max_rupiah);

					var calc_gram  = parseFloat(g_max_rupiah / buy_price);
					var berat_emas = calc_gram.toFixedDown(4);
					var fee_total  = Math.round(calc_gram * buy_price);
					var fee_pajak  = Math.round(calc_gram * buy_price * (npwp/100));

					g_total_rupiah = parseFloat((fee_total) + (fee_pajak)).toFixedDown(4);
					g_deposit_amt  = max_grams;
					g_total_rupiah = Math.round( g_total_rupiah );
			
					fee_total = "Rp." + thousand_format( fee_total );
					fee_pajak = "Pp." + thousand_format( fee_pajak );

                                        $('#gram'               ).text(berat_emas);
                                        $('#dup_gram'           ).text(berat_emas);
                                        $('#dup_gram_2'         ).text(berat_emas);
                                        $('#rupiah'             ).text(berat_emas);
                                        $('#dup_rupiah'         ).text(berat_emas);
                                        $('#dup_rupiah_2'       ).text(berat_emas);
                                        $("#total_cashout"      ).text(fee_total);
                                        $("#dup_total_cashout"  ).text(fee_total);
                                        $("#dup_total_cashout_2").text(fee_total);
                                        $("#fee_pajak"          ).text(fee_pajak);
                                        $("#dup_fee_pajak"      ).text(fee_pajak);
                                        $("#total_rupiah"       ).text("Rp." + thousand_format(g_total_rupiah));
                                        $("#dup_total_rupiah"   ).text("Rp." + thousand_format(g_total_rupiah));
                                        return
                                }

                                if (c_calc_gram.length != 0)
                                {
					fee_total = "Rp." + thousand_format(  fee_total );
					fee_pajak = "Rp." + thousand_format(  fee_pajak );

					$('#gram'               ).text(berat_emas);
					$('#dup_gram'           ).text(berat_emas);
					$('#dup_gram_2'         ).text(berat_emas);
					$('#rupiah'             ).text(berat_emas);
					$('#dup_rupiah'         ).text(berat_emas);
					$('#dup_rupiah_2'       ).text(berat_emas);
					$("#total_cashout"      ).text(fee_total);
					$("#dup_total_cashout"  ).text(fee_total);
					$("#dup_total_cashout_2").text(fee_total);
					$("#fee_pajak"          ).text(fee_pajak);
					$("#dup_fee_pajak"      ).text(fee_pajak);
					$("#total_rupiah"       ).text("Rp." + thousand_format(g_total_rupiah));
					$("#dup_total_rupiah"   ).text("Rp." + thousand_format(g_total_rupiah));
				}
				else
				{
					$('#gramz').text("");
					$("#rp"   ).text("");
				}
  			}
		);
		$("#manual_transfer_pay_id").click(
			function(e)
			{
				BG_action_deposit();
			}
		);
	}
);

$("#jumlah_dana").prop("disabled", true)
$("#gramz"	).prop("disabled", true)
$("#c"		).click(
	function()
	{

		var deposit_option = $("#c").is(":checked")
		if ( deposit_option )
		{
			$("#berat_emas"	).prop("disabled",true )
			$("#rp"		).prop("disabled",true )
			$("#jumlah_dana").prop("disabled",false)
			$("#gramz"	).prop("disabled",false)
		}
		else
		{
			$("#berat_emas"	).prop("disabled",false)
			$("#rp"		).prop("disabled",false)
			$("#jumlah_dana").prop("disabled",true )
			$("#gramz"	).prop("disabled",true )
	  	}
		$("#gramz"      ).html("")
		$("#rp"         ).html("")
		$("#jumlah_dana").val ("")
		$("#berat_emas" ).val ("")
	}
);