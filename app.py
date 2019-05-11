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

from panoptes_utils import database
from panoptes_utils.config.client import get_config
from panoptes_utils.messaging import PanMessaging

tornado.options.define("port", default=8888, help="port", type=int)
tornado.options.define("port", default=8888, help="port", type=int)
tornado.options.define("debug", default=False, help="debug mode")
# tornado.options.define('log_file_prefix', default='/var/panoptes/logs/paws.log')


class WebAdmin(tornado.web.Application):

    """ The main Application entry for our PANOPTES admin interface """

    def __init__(self, config={}):

        db = database.PanDB()
        # TODO: Fix the 'messaging' host below so not hard-coded
        msg_subscriber = PanMessaging.create_subscriber(6511, host='messaging-hub')
        cmd_publisher = PanMessaging.create_publisher(6500)

        self._base_dir = '{}'.format(os.getenv('PAWS', default='/var/panoptes/PAWS'))
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
