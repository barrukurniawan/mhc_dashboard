import urllib2
import urllib
import json
import traceback
import random

from core import config
from core import database

from modules        import signature
from stdlib         import idgen
from bson.objectid  import ObjectId

class security:

    wmsDB = database.get_db_conn( config.wms_userDB_core )

    def __init__(self):
        pass

    def wms_register_id(self, params):
        response = {
            "message_code"   : config.SUCCESS_REGISTER_WMS_ACCOUNT_CODE,
            "message_action" : config.SUCCESS_REGISTER_WMS_ACCOUNT_ACN ,
            "message_desc"   : "",
            "message_data"   : {}
        }
        try:
            merchant_api_key_rec = database.get_record("db_merchant_api_key")
            merchant_api_key_rec["merchant_label"] = params["merchant_label"]
            merchant_api_key_rec["merchant_id"   ] = params["merchant_id"   ]
            merchant_api_key_rec["merchant_key"  ] = params["merchant_key"  ]
            merchant_api_key_rec["pic_name"      ] = params["pic_name"      ]
            merchant_api_key_rec["pic_phone"     ] = params["pic_phone"     ]
            merchant_api_key_rec["company"       ] = params["company"       ]
            self.wmsDB.db_merchant_api_key.insert( merchant_api_key_rec )
        except Exception, e:
            response["message_code"  ] = config.FAILED_REGISTER_WMS_ACCOUNT_CODE
            response["message_action"] = config.FAILED_REGISTER_WMS_ACCOUNT_ACN
        # end try
        return response
    # end def

    def wms_locked(self, params):
        pass
    # end def

    def wms_void_trans(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label" ]
        dlk_code       = params["dlk_code"  ]
        token          = params["token"     ]
        partner_trx_id = params["partner_trx_id"]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(partner_trx_id)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def


    def wms_check_balance(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label" ]
        dlk_code       = params["dlk_code"  ]
        token          = params["token"     ]
        wallet_id      = params["wallet_id" ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(wallet_id)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_auth_login(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label" ]
        dlk_code       = params["dlk_code"  ]
        token          = params["token"     ]
        wallet_id      = params["wallet_id" ]
        password       = params["password"  ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(wallet_id) + str(password)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_merchant_buy(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"]
        dlk_code       = params["dlk_code" ]
        token          = params["token"    ]
        merch_wms_id   = params["to"       ]
        user_wms_id    = params["from"     ]
        amount         = params["amount"   ]
        pin            = params["pin"      ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(merch_wms_id) + str(user_wms_id) + str(amount) + str(pin)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_register_user(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"]
        dlk_code       = params["dlk_code" ]
        token          = params["token"    ]
        name           = params["name"     ]
        phone          = params["phone"    ]
        dob            = params["dob"      ]
        pin            = params["pin"      ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(name) + str(phone) + str(dob)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_register_merchant(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"]
        dlk_code       = params["dlk_code" ]
        token          = params["token"    ]
        wallet_id      = params["wallet_id"]
        password       = params["password" ]
        pin            = params["pin"      ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(wallet_id) + str(password) + str(pin)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_show_trans(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"]
        dlk_code       = params["dlk_code" ]
        token          = params["token"    ]
        target_id      = params["target_id"]
        start_dt       = params["start_dt" ]
        end_dt         = params["end_dt"   ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(target_id) + str(start_dt) + str(end_dt)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_transfer(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"]
        dlk_code       = params["dlk_code" ]
        token          = params["token"    ]
        user_from      = params["from"     ]
        user_to        = params["to"       ]
        amount         = params["amount"   ]
        pin            = params["pin"      ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(user_from) + str(user_to) + str(amount) + str(pin)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_token_gen(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"]
        dlk_code       = params["dlk_code" ]
        token          = params["token"    ]
        wallet_id      = params["wallet_id"]
        pin            = params["pin"      ]
        valid_tm       = params["valid_tm" ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(wallet_id) + str(pin) + str(valid_tm)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_token_redeem(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"  ]
        dlk_code       = params["dlk_code"   ]
        token          = params["token"      ]
        wallet_id      = params["wallet_id"  ]
        trans_token    = params["trans_token"]
        amount         = params["amount"     ]
        to             = params["to"         ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(wallet_id) + str(trans_token) + str(amount) + str(to)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_token_status(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"  ]
        dlk_code       = params["dlk_code"   ]
        token          = params["token"      ]
        wallet_id      = params["wallet_id"  ]
        trans_token    = params["trans_token"]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(wallet_id) + str(trans_token)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_cashin(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"]
        dlk_code       = params["dlk_code" ]
        token          = params["token"    ]
        user_to        = params["to"       ]
        amount         = params["amount"   ]
        pin            = params["pin"      ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(user_to) + str(amount) + str(pin)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_merchant_cashin(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"]
        dlk_code       = params["dlk_code" ]
        token          = params["token"    ]
        user_from      = params["from"     ]
        user_to        = params["to"       ]
        amount         = params["amount"   ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(user_from) + str(user_to) + str(amount)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_process_update_pin(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"]
        dlk_code       = params["dlk_code" ]
        token          = params["token"    ]
        wallet_id      = params["wallet_id"]
        new_pin        = params["new_pin"  ]
        old_pin        = params["old_pin"  ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       :  str(wallet_id) + str(new_pin) + str(old_pin)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_process_reset_pin(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"]
        dlk_code       = params["dlk_code" ]
        token          = params["token"    ]
        wallet_id      = params["wallet_id"]
        new_pin        = params["new_pin"  ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       :  str(wallet_id) + str(new_pin) 
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_process_update_password(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"]
        dlk_code       = params["dlk_code" ]
        token          = params["token"    ]
        wallet_id      = params["wallet_id"]
        new_password   = params["new_password"]
        old_password   = params["old_password"]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(wallet_id) + str(new_password) + str(old_password)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_process_reset_password(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"   ]
        dlk_code       = params["dlk_code"    ]
        token          = params["token"       ]
        wallet_id      = params["wallet_id"   ]
        new_password   = params["new_password"]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(wallet_id) + str(new_password)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_edit_user(self, params):
        verify_status  = "VERIFY_SUCCESS"
        h2h_label      = params["h2h_label"]
        dlk_code       = params["dlk_code" ]
        token          = params["token"    ]
        wallet_id      = params["wallet_id"]
        name           = params["name"     ]
        email          = params["email"    ]
        address        = params["address"  ]
        phone          = params["phone"    ]
        ktp            = params["ktp"      ]
        mother         = params["mother"   ]
        has_key_value  = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(wallet_id) + str(name) + str(email) + str(address) +\
                str(phone) + str(ktp) + str(mother)
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def

    def wms_edit_merchant(self, params):
        verify_status   = "VERIFY_SUCCESS"
        h2h_label       = params["h2h_label"      ]
        dlk_code        = params["dlk_code"       ]
        token           = params["token"          ]
        wallet_id       = params["wallet_id"      ]
        ktp             = params["ktp"            ]
        otp_phone       = params["otp_phone"      ]
        contact         = params["contact"        ]
        email           = params["email"          ]
        siup            = params["siup"           ]
        npwp            = params["npwp"           ]
        owner           = params["owner"          ]
        bank_name       = params["bank_name"      ]
        bank_accn_num   = params["bank_accn_num"  ]
        bank_accn_owner = params["bank_accn_owner"]
        has_key_value   = signature.signature()._create_onway_hash({
            "merchant_label" : h2h_label,
            "dlk_code"       : dlk_code,
            "sequance"       : str(wallet_id) + str(ktp) + str(otp_phone) + str(contact) +\
                str(email) + str(siup) + str(npwp) + str( bank_name ) +\
                str( bank_accn_num )
        })
        if token != has_key_value:
            verify_status = "VERIFY_FAILED"
        # end if
        return verify_status
    # end def
# end class
