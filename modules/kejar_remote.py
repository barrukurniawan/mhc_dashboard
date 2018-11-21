import json
import time
import random

from core    import config
from core    import database
from stdlib  import remote
from modules import signature

def call(params):
    route_call   = params["route_call"  ]
    sequance     = params["sequance"    ]
    send_params  = params["params"      ]
    remote_host  = config.G_KEJAR_HOST + ":" + config.G_KEJAR_PORT

    rand_dlk     = random.randint(
        config.G_DLK_RANGE_START,
        config.G_DLK_RANGE_END
    )
    dlk_middle   = int(time.time())
    dlk_code     = "DLK_" + str(dlk_middle) + "_" + str(rand_dlk) + "_ID"
    access_token = signature.signature()._create_onway_hash({
        "merchant_label" : config.G_H2H_LABEL,
        "dlk_code"       : dlk_code,
        "sequance"       : sequance
    })
    send_params["dlk_code" ] = dlk_code
    send_params["h2h_label"] = config.G_H2H_LABEL
    send_params["token"    ] = access_token
    response    = remote.call({
        "scheme" : "http"      ,
        "host"   : remote_host ,
        "route"  : route_call  ,
        "param"  : send_params
    })
    return response
# end def
