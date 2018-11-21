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
from modules          import signature
from modules          import security
from stdlib           import utils
from bson.objectid    import ObjectId
from Cheetah.Template import Template

class user_twitter_register:

    DB = database.get_db_conn(config.barru_DB_core)

    def __init__(self):
        pass
    #end def

    def _process(self, params):
        email     = params["email"]
        email     = sanitize.clean_html({"text" : email })
        password  = params["password"]
        password  = sanitize.clean_html({"text" : password })
        username  = params["username"]
        username  = sanitize.clean_html({"text" : username })
        copass    = params["copass"]
        copass    = sanitize.clean_html({"text" : copass})
        user_auth = database.get_record("db_user_auth") 
        response = {
            "message_action" : "USER_REGISTER_SUCCESS",
            "message_desc"   : "USER_REGISTER_SUCCESS"
        }

        length_username = len(username)
        username_suffix = username[length_username - config.G_USERNAME_SUFFIX : length_username]
        password_md5 = hashlib.md5()
        password_md5.update(password + username_suffix)
        password_hash = password_md5.hexdigest()
        if password == copass :
            add_new_user = self.DB.db_user.insert({
                "username"  :username,
                "password"  :password_hash,
                "email"     :email
            })
            fk_user_id = str(add_new_user)
        #end if
        user_auth["email"]      = email
        user_auth["fk_user_id"] = fk_user_id
        user_auth["username"]   = username
        self.DB.db_user_auth.insert( user_auth )

        if add_new_user == None:
            response["message_action"] = "USER_REGISTER_FAILED"
            response["message_desc"  ] = "USER_REGISTER_FAILED"
        # end if
        return response 
    # end def
#end class