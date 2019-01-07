import os
import os.path

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from zmq.eventloop import ioloop

from handlers import base
from handlers import websockets
from ui import modules

#from pocs.utils import database
from utils import database 
#from pocs.utils.config import load_config
from utils.config import load_config
#from pocs.utils.messaging import PanMessaging
from utils.messaging import PanMessaging

ioloop.install()

tornado.options.define("port", default=8888, help="port", type=int)
tornado.options.define("debug", default=False, help="debug mode")
# tornado.options.define('log_file_prefix', default='/var/panoptes/logs/paws.log')


class WebAdmin(tornado.web.Application):

    """ The main Application entry for our PANOPTES admin interface """

    def __init__(self, config={}):

        db = database.FileDB()
        msg_subscriber = PanMessaging.create_subscriber(6511)
        cmd_publisher = PanMessaging.create_publisher(6500)

        self._base_dir = '{}'.format(os.getenv('PAWS',
                                               default='/home/gnthibault/projects/PAWS'))
#                                               default='/var/RemoteObservatory/PAWS'))
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
    http_server = tornado.httpserver.HTTPServer(WebAdmin(load_config()))
    http_server.listen(tornado.options.options.port)
    print("Starting PAWS on port {}".format(tornado.options.options.port))
    tornado.ioloop.IOLoop.instance().start()
