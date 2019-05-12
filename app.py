import logging
import os
import os.path

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handlers import base
from handlers import websockets
from ui import modules

#from pocs.utils import database
from utils import database 
#from pocs.utils.config import load_config
from utils.config import load_config
#from pocs.utils.messaging import PanMessaging
from utils.messaging import PanMessaging

tornado.options.define("port", default=8888, help="port", type=int)
tornado.options.define("debug", default=True, help="debug mode")
#TODO TN THIS DOES NOT WORK: Traceback (most recent call last):
#tornado.options.Error: Option 'log-file-prefix' already defined in /[...]/lib/python3.6/site-packages/tornado/log.py
#tornado.options.define('log_file_prefix', default='/var/RemoteObservatory/logs/paws.log')

class WebAdmin(tornado.web.Application):

    """ The main Application entry for our PANOPTES admin interface """

    def __init__(self, config={}):

        db = database.FileDB(db_name='/var/RemoteObservatory/DB')
        msg_subscriber = PanMessaging.create_subscriber(6511)
        # TODO: Fix the 'messaging' host below so not hard-coded
        #msg_subscriber = PanMessaging.create_subscriber(6511, host='messaging')
        cmd_publisher = PanMessaging.create_publisher(6500)

        self._base_dir = '{}'.format(os.getenv('PAWS',
            default='/home/gnthibault/projects/PAWS'))
#            default='/var/RemoteObservatory/PAWS'))
        name = config.setdefault('name', 'PAWS')
        server = config.setdefault('server_url', '127.0.0.1')

        server_url = '{}:{}'.format(server, tornado.options.options.port)

        app_handlers = [
            (r"/", base.MainHandler),
            (r"/observations/(.*)", base.ObservationsHistoryHandler),
            (r"/ws/(.*)", websockets.PanWebSocket),
        ]
        settings = dict(
            cookie_secret="PANOPTES_SUPER_DOOPER_SECRET",
            template_path=os.path.join(self._base_dir, "templates"),
            static_path=os.path.join(self._base_dir, "static"),
            xsrf_cookies=True,
            db=db,
            msg_subscriber=msg_subscriber,
            cmd_publisher=cmd_publisher,
            config=config,
            name=name,
            server_url=server_url,
            site_title=name,
            ui_modules=modules,
            port=tornado.options.options.port,
            compress_response=True,
            debug=tornado.options.options.debug,
        )

        super().__init__(app_handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(WebAdmin(get_config(host='0.0.0.0')))
    http_server.listen(tornado.options.options.port)
    print("Starting PAWS on port {}".format(tornado.options.options.port))
    tornado.ioloop.IOLoop.current().start()
