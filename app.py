import os
import os.path
import sys

import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options

from zmq.eventloop import ioloop

from handlers import base, websockets
from ui import modules

ioloop.install()

sys.path.append(os.getenv('POCS', os.path.join(os.path.dirname(__file__), "..")))

from panoptes.utils import database
from panoptes.utils.messaging import PanMessaging

tornado.options.define("port", default=8888, help="port", type=int)
tornado.options.define("debug", default=False, help="debug mode")


class WebAdmin(tornado.web.Application):

    """ The main Application entry for our PANOPTES admin interface """

    def __init__(self, config={}):

        db = database.PanMongo()
        messaging = PanMessaging()

        self._base_dir = '{}'.format(os.getenv('PAWS', default='/var/panoptes/PAWS'))
        name = config.setdefault('name', 'PAWS')
        server = config.setdefault('server_url', '127.0.0.1')

        server_url = '{}:{}'.format(server, tornado.options.options.port)

        app_handlers = [
            (r"/", base.MainHandler),
            (r"/ws/(.*)", websockets.PanWebSocket),
        ]
        settings = dict(
            cookie_secret="PANOPTES_SUPER_DOOPER_SECRET",
            template_path=os.path.join(self._base_dir, "templates"),
            static_path=os.path.join(self._base_dir, "static"),
            xsrf_cookies=True,
            db=db,
            messaging=messaging,
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
    http_server = tornado.httpserver.HTTPServer(WebAdmin({'name': 'PAN001'}))
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()
