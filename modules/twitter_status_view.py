import json
import pymongo
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

class twitter_status_view:

    barruDB = database.get_db_conn( config.barru_DB_twitter )

    def __init__(self):
        pass
    #end def

    def _process(self, params):
        response = {
            "message_action"   :  "STATUS_DISPLAY_SUCCESS" ,
            "message_desc"     :  "STATUS_DISPLAY_SUCCESS" ,
            "message_data"     :  {}
        }
        try:
            page_size     = 5
            search_key    = params["keyword"]
            fk_user_id    = params["fk_user_id"]
            page          = params["page"]
            sort_page     = params["sort"]
            filter_search = params["filter_search"]
            sort_page = int(sort_page)
            skips         = page_size * (int(page) - 1)
            print page

            userView      = self.barruDB.db_user_status.find_one({"pkey":fk_user_id})
            
            if sort_page == 1:
                statusView    = self.barruDB.db_twitter_status.find({"fk_user_id":fk_user_id, filter_search :{"$regex":search_key}}).sort(filter_search,1).skip(skips).limit(page_size)
            else :
                statusView    = self.barruDB.db_twitter_status.find({"fk_user_id":fk_user_id, filter_search :{"$regex":search_key}}).sort(filter_search,-1).skip(skips).limit(page_size)

            total_status  = self.barruDB.db_twitter_status.find({"fk_user_id":fk_user_id}).count()

            print total_status
            statusList    = []
            for statusUser in statusView:
				room = {
					"fk_user_id"   : statusUser["fk_user_id"] ,
                    "first"        : userView["first"]        ,
                    "last"         : userView["last"]         ,
					"time"         : statusUser["time"]       ,
					"date"         : statusUser["date"]       ,
					"subject"      : statusUser["subject"]    ,
					"location"     : statusUser["location"]
				}
				statusList.append(room)
			#End for
            response["message_data"] = statusList

        except Exception, e:
            print traceback.format_exc()
            response["message_action"] = "STATUS_DISPLAY_FAILED"
            response["message_desc"  ] = "STATUS_DISPLAY_FAILED" + " " + str(e)
        # end try
        return response
    #end def

#end class
