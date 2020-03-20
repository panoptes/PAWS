# Generic stuff
import logging
import os
import os.path

# Web stuff stuff
import tornado
import tornado.options
from bokeh.server.server import Server

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
#tornado.options.define("debug", default=True, help="debug mode")
#TODO TN THIS DOES NOT WORK: Traceback (most recent call last):
#tornado.options.Error: Option 'log-file-prefix' already defined in /[...]/lib/python3.6/site-packages/tornado/log.py
#tornado.options.define('log_file_prefix', default='/var/RemoteObservatory/logs/paws.log')

class WebAdmin(tornado.web.Application):

    """ The main Application entry for our PANOPTES admin interface """

    def __init__(self, config={}):

        db = database.FileDB()
        #db = database.FileDB(db_name='/var/RemoteObservatory/DB')
        msg_subscriber = PanMessaging.create_subscriber(6511)
        # TODO: Fix the 'messaging' host below so not hard-coded
        #msg_subscriber = PanMessaging.create_subscriber(6511, host='messaging')
        cmd_publisher = PanMessaging.create_publisher(6500)

        self._base_dir = '{}'.format(os.getenv('PAWS',
            default='/home/gnthibault/projects/PAWS'))
#            default='/var/RemoteObservatory/PAWS'))

        name = config.setdefault('name', 'PAWS')
        server = config.setdefault('server_url', '0.0.0.0')

        server_url = '{}:{}'.format(server, tornado.options.options.port)

        app_handlers = [
            (r"/", base.MainHandler),
            (r"/login", base.LoginHandler),
            (r"/observations/(.*)", base.ObservationsHistoryHandler),
            (r"/ws/(.*)", websockets.PanWebSocket),
        ]
        settings = dict(
            template_path=os.path.join(self._base_dir, "templates"),
            static_path=os.path.join(self._base_dir, "static"),
            xsrf_cookies=True,
            cookie_secret="PANOPTES_SUPER_DOOPER_SECRET",
            login_url="/login", # redirect() will go there
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
            debug=True,
            #debug=tornado.options.options.debug,
            #log_to_stderr=True,
            #log_file_prefix='/var/RemoteObservatory/logs/paws.log'
        )

        super().__init__(app_handlers, **settings)


if __name__ == '__main__':
    # First instantiate main tornado infrastructure
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(WebAdmin(load_config()))
    http_server.listen(tornado.options.options.port)
    io_loop = tornado.ioloop.IOLoop.current()
    
    
    # Now instantiate bokeh app
    tornado_port = tornado.options.options.port
    bokeh_server = Server({'/bokeh_weather': base.bokeh_weather_app},
                          io_loop=io_loop,
                          allow_websocket_origin=[f"localhost:{tornado_port}"])
    # Launch the whole thing
    print(f"Starting PAWS on port {tornado_port}")
    io_loop.start()    
