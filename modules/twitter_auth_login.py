import json
import urllib2
import urllib
import json
import traceback
import hashlib
import time
import random
import pystmark

from core             import database
from core             import config
from core             import sanitize
from stdlib           import idgen
from stdlib           import remote
from stdlib           import utils
from bson.objectid    import ObjectId
from Cheetah.Template import Template

class twitter_auth_login:

    barruDB = database.get_db_conn( config.barru_DB_twitter )

    def __init__(self):
        pass
    #end def

    def _process(self, params):
        response = {
            "message_action"   :  "LOGIN_USER_SUCCESS",
            "message_desc"     :  "",
            "message_data"     :  {}
        }
        try:
            email       = params["email"    ]
            password    = params["password" ]

            password_hash = utils._get_passwd_hash({
                "email"     : email,
                "password"  : password
            })

            user_auth_rec = self.barruDB.db_user_auth_status.find_one({
                "email" : email,
                "password"  : password_hash
            })

            if user_auth_rec == None:
                response["message_action"] = "USER_LOGIN_FAILED"
                response["message_desc"  ] = "USER_LOGIN_FAILED"
                return response
            # end if

            fk_user_id  = user_auth_rec["fk_user_id"]

            user_rec = self.barruDB.db_user_status.find_one({
                "pkey" : fk_user_id
            })
            user_rec["_id"] = str( user_rec["_id"] )

            response["message_data"  ] = {
                "user_auth_rec"  : user_auth_rec    ,
                "user_rec"       : user_rec
            }

        except Exception, e:
            print traceback.format_exc()
            response["message_action"] = "USER_LOGIN_FAILED"
            response["message_desc"  ] = "USER_LOGIN_FAILED" + " " + str(e)
        # end try
        return response
    # end def
#end class
