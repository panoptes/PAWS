# Generic stuff
import logging
import os
import os.path

# Web stuff
import tornado
import tornado.options
from bokeh.server.server import Server

# Local video webstream related
from WebcamStreamer import WebcamStreamer

# Local web stuff
from handlers import base
from handlers import websockets
from ui import modules

# Main POCS code
from utils import database, load_module
from utils.config import load_config

tornado.options.define("port", default=8000, help="port", type=int)
#tornado.options.define("debug", default=True, help="debug mode")
#TODO TN THIS DOES NOT WORK: Traceback (most recent call last):
#tornado.options.Error: Option 'log-file-prefix' already defined in /[...]/lib/python3.6/site-packages/tornado/log.py
#tornado.options.define('log_file_prefix', default='/var/RemoteObservatory/logs/paws.log')


class WebAdmin(tornado.web.Application):

    """ The main Application entry for our PANOPTES admin interface """

    def __init__(self, config={}):
        db = database.FileDB()
        #db = database.FileDB(db_name='/var/RemoteObservatory/DB')
        subscriber_name = config["paws_subscriber"]['module']
        subscriber_module = load_module('Service.' + subscriber_name)
        msg_subscriber = getattr(subscriber_module, subscriber_name)(
            config=config["paws_subscriber"])

        publisher_name = config["paws_publisher"]['module']
        publisher_module = load_module('Service.' + publisher_name)
        cmd_publisher = getattr(publisher_module, publisher_name)(
            config=config["paws_publisher"])

        if "webcam" in config["observatory"]:
            wc = WebcamStreamer(config["observatory"]["webcam"])
            wc.launch_webcam_stream_converter()

        self._base_dir = f"{os.getenv('PAWS', default='/home/gnthibault/projects/PAWS')}"

        name = config.setdefault('name', 'PAWS')
        server = config.setdefault('server_url', '0.0.0.0')

        server_url = f"{server}:{tornado.options.options.port}"

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
    bokeh_server = Server({'/bokeh_weather': base.bokeh_weather_app,
                           '/bokeh_guiding': base.bokeh_guiding_app},
                          io_loop=io_loop,
                          allow_websocket_origin=[f"localhost:{tornado_port}",
                                                  f"localhost:5006"])
    # Launch the whole thing
    print(f"Starting PAWS on port {tornado_port}")
    io_loop.start()    
