import cherrypy
import pymongo
import json
import urllib2
import urllib
import json
import traceback
import hashlib
import time
import random
import datetime

from core          import database
from core          import config
from core          import sanitize
from modules       import signature
from bson.objectid import ObjectId

class status_user_proc:

	DB = database.get_db_conn(config.barru_DB_core)

	def __init__(self):
		pass
	#end deff

	def _status_process(self, params):
		response = {
			"message_action" : "INPUT_STATUS_SUCCESS",
			"message_desc"   : "An error has occured",
			"message_data"   : {}
		}

		try:
			fk_user_id	= cherrypy.session.get("fk_user_id")
			status      = params["status"]
			time_status	= params["time_status"]
			print fk_user_id
			print status
			print time_status

			add_status_twitter = self.DB.db_status.insert({
				"status"			: status,
				"time_status"		: time_status,
				"fk_user_id"		: fk_user_id
			})

			pkey_user_status = self.DB.db_status.find_one({
				"status" : status
			})

			id_user_status = str(pkey_user_status["_id"])

			response["message_data"] = {
				"id_user_status"	: id_user_status,
				"fk_user_id"		: fk_user_id,
				"status"			: status,
				"time_status"		: time_status
			}

			response["message_action"] = "INPUT_STATUS_SUCCESS"

		except Exception, e:
			print traceback.format_exc()
			response["message_action"] = "INPUT_STATUS_FAILED"
			response["message_desc"]   = "An error has occured"
		#end try
		return response
	#end def
#end class
