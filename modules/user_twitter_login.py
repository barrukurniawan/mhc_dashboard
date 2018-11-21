import json
import urllib2
import urllib
import json
import traceback
import hashlib
import time
import random

from core          import database
from core          import config
from core          import sanitize
from modules       import signature
from modules       import security
from stdlib        import idgen
from stdlib        import utils
from bson.objectid import ObjectId

class user_twitter_login:

    DB = database.get_db_conn(config.barru_DB_core)

    def __init__(self):
        pass
    #end def

    def _process(self, params):
        response = {
            "message_action"   :  "USER_LOGIN_SUCCESS" ,
            "message_desc"     :  "USER_LOGIN_SUCCESS" ,
            "message_data"     :  {}
        }
        try:
            username      = params["username"]
            username      = sanitize.clean_html({"text" : username })
            password      = params["password"]
            password      = sanitize.clean_html({"text" : password })

            length_username = len(username)
            username_suffix = username[
                length_username - config.G_USERNAME_SUFFIX : length_username
            ]

            password_md5 = hashlib.md5()
            password_md5.update(password + username_suffix)
            password_hash = password_md5.hexdigest()

            account_rec = self.DB.db_user.find_one({
                "username" : username,
                "password" : password_hash
            })
            user_id  = account_rec["_id"]
            username = account_rec["username"]
            email    = account_rec["email"]
            
            account_auth = self.DB.db_user_auth.find_one({
                "email" : email
            })
            fk_user_id = account_auth["fk_user_id"]

            response = {
                "message_action" : "USER_LOGIN_SUCCESS" ,
                "message_desc"   : "USER_LOGIN_SUCCESS" ,
                "message_data"   : {
                    "fk_user_id" : fk_user_id,
                    "id"         : user_id,
                    "username"   : username,
                    "email"      : email,
                },
            }
        except Exception, e:
            print traceback.format_exc()
            response["message_action"] = "USER_LOGIN_FAILED"
            response["message_desc"  ] = "USER_LOGIN_FAILED" + " " + str(e)
        # end try
        return response
    # end def
#end class
