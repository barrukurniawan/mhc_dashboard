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

class status_user_view:

	DB = database.get_db_conn(config.barru_DB_core)

	def __init__(self):
		pass
	#end deff

	def _status_process(self, params):
		response = {
			"message_action" : "GET_STATUS_SUCCESS",
			"message_desc"   : "",
			"message_data"   : {}
		}

		try:
			fk_user_id	= params["fk_user_id"]
			print fk_user_id

			get_id_user_auth = self.DB.db_user_auth.find_one({
				"fk_user_id"	: fk_user_id
			})
			print get_id_user_auth

			get_status_twitter = self.DB.db_status.find({
				"fk_user_id"	: fk_user_id
			})
			print get_status_twitter

			status_list = []
			for user_status in get_status_twitter:
				fk_user_id  = user_status["fk_user_id"]
				status      = user_status["status"]
				time_status = user_status["time_status"]

				detail_user_status = {
					"fk_user_id"  : fk_user_id,
					"status"	  : status,
					"time_status" : time_status
				}
				status_list.append(detail_user_status)
			#end for

			print status_list

			response["message_data"] = status_list

		except:
			print "ERROR"
			response["message_action"] = "GET_STATUS_SUCCESS"
			response["message_desc"]   = ""
		return response
		#end try
	#end def
#end class
