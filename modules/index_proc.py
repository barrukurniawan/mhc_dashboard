#####################################################
#                                                   #
# Add all of your custom classes here .. this is    #
# just a sample display of your custom class        #
#                                                   #
#####################################################

import urllib2
import urllib
import json
import traceback
import time

from Cheetah.Template import Template

from core import config
from core import database

from stdlib  import sanitize

from modules       import signature
from bson.objectid import ObjectId

# upload file
import os
import os.path
from cherrypy.lib import static
from PIL import Image

class index_proc:

	DB = database.get_db_conn(config.barru_DB_core)

	def __init__(self):
 		pass
	#end def

	def _process(self, params):

		html_page = params['html']
		fk_user_id = params['fk_user_id']
		username = params['username']

		user_account_auth = self.DB.db_user_auth.find_one({
			"fk_user_id" : fk_user_id
		})

		html_template = Template(
			html_page,
			searchList=[{
				"config":configMap,
				"noteList":noteList,
				"username":username,
				"level":level
			}]
		)

		return str(html_template)
	# end def

#end class
