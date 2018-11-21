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

class twitter_auth_register:

    barruDB = database.get_db_conn( config.barru_DB_twitter )

    def __init__(self):
        pass
    #end def

    def _process(self, params):
        response = {
            "message_action"   :  "REGISTER_USER_SUCCESS",
            "message_desc"     :  "",
            "message_data"     :  {}
        }
        try:
            first               = params["first"            ]
            last                = params["last"             ]
            phone               = params["phone"            ]
            email               = params["email"            ]
            username            = params["username"         ]
            password            = params["password"         ]
            confirm_password    = params["confirm_password" ]
            user_type_status    = params["user_type_status" ]

            user_auth_rec = self.barruDB.db_user_auth_status.find_one({
                "email" : email
            })
            if user_auth_rec != None:
                response["message_action"   ] = "REGISTER_USER_FAILED"
                response["message_desc"     ] = "REGISTER_ACCOUNT_FAILED"
                return response
            # end if

            m_action = response["message_action"]
            if m_action == "REGISTER_USER_SUCCESS":
                user_rec = database.get_record("db_user_status")
                user_rec["first"            ] = first
                user_rec["last"             ] = last
                user_rec["phone"            ] = phone
                user_rec["user_type_status" ] = user_type_status
                fk_user_id = self.barruDB.db_user_status.insert(user_rec)
                fk_user_id = str( fk_user_id )

                password_hash = utils._get_passwd_hash({
                    "email"     : email,
                    "password"  : password
                })
                user_auth_rec = database.get_record("db_user_auth_status")
                user_auth_rec["fk_user_id"  ] = fk_user_id
                user_auth_rec["email"       ] = email
                user_auth_rec["username"    ] = username
                user_auth_rec["password"    ] = password_hash
                self.barruDB.db_user_auth_status.insert(user_auth_rec)

            else:
                response["message_action"] = "REGISTER_USER_FAILED"
                response["message_desc"  ] = "REGISTER_ACCOUNT_FAILED"
            # end if

        except Exception, e:
            print traceback.format_exc()
            response["message_action"] = "REGISTER_USER_FAILED"
            response["message_desc"  ] = str(e)
        # end try
        return response
    # end def
#end class
