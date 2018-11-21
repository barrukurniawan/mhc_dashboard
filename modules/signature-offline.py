import pymongo
import json
import base64
import M2Crypto
import datetime
import pyDes
import random
import time
import hashlib
import binascii
import traceback
import sys

sys.path.append("../core")
sys.path.append("../stdlib")
sys.path.append("../modules")
sys.path.append("../")


from core          import config
from core          import database
from Crypto.Cipher import AES

class signature:

    dbPayment = database.get_db_conn(config.wmsDB_core)

    def _create_onway_hash(self, params):
        response_json = {
            "message_status" : "SUCCESS",
            "message_action" : "HASH_CREATE_SUCCESS",
            "message_desc"   : "",
            "message_data"   : {},
        }
        token = "00000"
        try:
            merchant_label  = params["merchant_label"]
            dlk_code        = params["dlk_code"      ]
            sequance        = params["sequance"      ]
            api_key_rec     = self.dbPayment.db_merchant_api_key.find_one({
                "merchant_label" : merchant_label
            })
            if api_key_rec != None:
                merchant_label = api_key_rec["merchant_label"]
                merchant_id    = api_key_rec["merchant_id"   ]
                merchant_key   = api_key_rec["merchant_key"  ]
                mercToken      = merchant_label +"%|%"+ merchant_id +"%|%"+\
                    dlk_code +"%|%"+ merchant_key + "%|%" + str(sequance)
                token          = hashlib.sha256(mercToken.encode('ascii')).hexdigest()
            #end if
        except Exception, e:
            response_json["message_action"] = "HASH_CREATE_FAILED"
            response_json["message_desc"  ] = str(e)
            response_json["message_data"  ] = { "message_except" : str(e) }
            print traceback.format_exc()
        #end try
        return token
    #end def

    """
        This will create the signature for the 
            dompetku connection code
    """
    def _create_signature(self, params):
        userid = config.G_DMPTKU_USERID
        key    = config.G_DMPTKU_KEY
        pin    = config.G_DMPTKU_PIN
        init   = config.G_DMPTKU_PKCS5_INIT
        if params.has_key("init"):
            init = params["init"]
        #end if
        if params.has_key("pin"):
            pin  = params["pin"]
        #end if

        current_date = datetime.datetime.now()
        hour_tm      = current_date.hour
        minute_tm    = current_date.minute
        second_tm    = current_date.second
        SIGNA        = str(hour_tm) + str(minute_tm) + str(second_tm) + pin
        SIGNB        = pin[::-1] + "|" + init
        SIGNC        = SIGNA + "|" + SIGNB 
        desHandle    = pyDes.triple_des(
                key, 
                pyDes.ECB,
                padmode=pyDes.PAD_PKCS5
        )
        cypherText = base64.b64encode(desHandle.encrypt(SIGNC.encode()))
        return cypherText 
    #end def

    """
        This will create the narindo signature for when
            we send the data to narindo
    """
    def _create_narindo_signature(self, MSISDN, PRODUCT):
        RANDOM_SEED  = random.randint(1,1000000)
        REQID        = "DLKA_" + str(int(time.time())) + "_" + str(RANDOM_SEED) 
        USERID       = config.G_NARINDO_USERNAME
        PASSWORD     = config.G_NARINDO_PASSWORD
        ENCRYPT      = REQID + MSISDN + PRODUCT + USERID + PASSWORD
        SIGN         = hashlib.sha1(ENCRYPT).hexdigest()
        send_data    = {
            "sign"     : SIGN.upper() ,
            "reqid"    : REQID        ,
            "userid"   : USERID       ,
            "password" : PASSWORD
        }
        return send_data
    # end def

    """
        This will create the signature for doku
    """
    def _simpel_padding (self, string, pad_pattern):
        if pad_pattern == None:
            pad_pattern = ' '
        # end if
        remain = len( string ) % 16
        if remain == 0:
            return string
        # end if
        padding_add = 16 - remain
        for idx in range(0 , padding_add):
            string = string + pad_pattern
        # end for
        return string
    # end def

    def _simpel_encrypt (self, string):
        secret     = self._simpel_padding( config.G_SIMPEL_SHAREDKEY , '0' ) 
        string     = self._simpel_padding( string , None ) 
        iv         = 'fedcba9876543210'
        cipher     = AES.new(secret, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(string)
        hextext    = binascii.hexlify(ciphertext)
        return hextext
    # end def

    def _create_simpel_signature(self, REQUESTDATETIME, SESSIONID):
        CHANNELCODE = config.G_SIMPEL_CHANNEL
        SHAREDKEY   = config.G_SIMPEL_SHAREDKEY
        LOGINID     = config.G_SIMPEL_USERNAME
        ENCRYPT     = None
        if SESSIONID == None:
            ENCRYPT = CHANNELCODE + REQUESTDATETIME + SHAREDKEY + LOGINID
        else:
            ENCRYPT = CHANNELCODE + SESSIONID + REQUESTDATETIME + SHAREDKEY + LOGINID
        # end if
        """
            This is where we have to create the signature to send 
        """
        doku_sign = hashlib.sha1(ENCRYPT).hexdigest()
        return doku_sign
    # end def


    def _decrypt_qrcode(self, params):
        cypherText   = params["cypherText"]
        desHandle    = pyDes.triple_des(
                "5879fa21b1d7a82ba8fdb88b" ,
                pyDes.ECB,
                padmode=pyDes.PAD_PKCS5
        )
        actual_text  = desHandle.decrypt( base64.b64decode(cypherText) )
        print actual_text
        return actual_text
    #end def

#end class

sequence = sys.argv[1]
s = signature()._create_onway_hash({
    "merchant_label" : "DEALOKA",
    "dlk_code"       : "DLK_123456_ID",
    "sequance"       : sequence
})
print s
