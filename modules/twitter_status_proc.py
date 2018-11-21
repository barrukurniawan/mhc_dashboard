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

class twitter_status_proc:

    barruDB = database.get_db_conn( config.barru_DB_twitter )

    def __init__(self):
        pass
    #end def

    def _process(self, params):
        response = {
            "message_action"   :  "STATUS_INSERT_SUCCESS" ,
            "message_desc"     :  "STATUS_INSERT_SUCCESS" ,
            "message_data"     :  {}
        }
        try:
            fk_user_id  = params["fk_user_id"   ]
            time        = params["time"         ]
            date        = params["date"         ]
            subject     = params["subject"      ]
            location    = params["location"     ]

            rooms_rec = database.get_record("db_twitter_status")
            rooms_rec["fk_user_id"  ] = fk_user_id
            rooms_rec["subject"     ] = subject
            rooms_rec["location"    ] = location
            rooms_rec["date"        ] = date
            rooms_rec["time"        ] = time
            self.barruDB.db_twitter_status.insert( rooms_rec )
        except Exception, e:
            print traceback.format_exc()
            response["message_action"] = "STATUS_INSERT_FAILED"
            response["message_desc"  ] = "STATUS_INSERT_FAILED" + " " + str(e)
        # end try
        return response
    #end def

#end class
