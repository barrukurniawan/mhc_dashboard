import json
import urllib2
import urllib
import json
import traceback
import hashlib
import time
import random

from core             import database
from core             import config
from core             import sanitize
from stdlib           import idgen
from stdlib           import remote
from bson.objectid    import ObjectId
from Cheetah.Template import Template

class user_dashboard_view:

    barruDB = database.get_db_conn( config.barru_DB_twitter )

    def __init__(self):
        pass
    #end def

    def _html(self, params):
        response = {
            "message_action"   :  "USER_DISPLAY_SUCCESS" ,
            "message_desc"     :  "USER_DISPLAY_SUCCESS" ,
            "message_data"     :  {}
        }
        try:
            html_page = params["html"]
            # resp_display_data = self._get_display_data( params )
            # html_obj  = Template(
            #     html_page,
            #     searchList = [ resp_display_data ]
            # )
            html_obj  = Template(
                html_page
            )
            response["message_data"  ] = { "html" : str( html_obj ) }
        except Exception, e:
            print traceback.format_exc()
            response["message_action"] = "USER_DISPLAY_FAILED"
            response["message_desc"  ] = "USER_DISPLAY_FAILED" + " " + str(e)
        # end try
        return response
    # end def
#end class
