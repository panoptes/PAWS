#Generic stuff
from datetime import datetime
import json

#Web stuff
import asyncio
import tornado
from tornado.log import app_log as app_log
from tornado.websocket import WebSocketHandler

#Numerical stuff
import numpy as np

# Local stuff
from handlers import users_info as users_info

clients = []

class PanWebSocket(WebSocketHandler):

    # This does not make sense
    # def get_current_user(self):
    #     """
    #     Looks for a cookie that shows we have been logged in. If cookie
    #     is found, attempt to look up user info in the database
    #     """
    #     user_data = None
    #     try:
    #         user_data = tornado.escape.xhtml_escape(
    #             self.get_secure_cookie("user"))
    #     except TypeError as e:
    #         pass
    #
    #     # Get email from cookie
    #     #email = tornado.escape.to_unicode(self.get_secure_cookie("email"))
    #     #if not email:
    #     #    return None
    #
    #     # Look up user data
    #     #user_data = self.db.admin.find_one({'username': email})
    #     #if user_data is None:
    #     #    return None
    #
    #     return user_data

    def open(self, channel):
        """ Client opening connection to unit """

        if channel is None:
            channel = self.settings['name']
        app_log.debug(f"Setting up subscriber for channel: {channel}")
        try:
            # Register the callback
            self.ioloop = asyncio.get_event_loop()
            self.settings['msg_subscriber'].register_callback(callback=self.on_data)
            app_log.debug(f"WS opened for channel {channel}")

            # Add this client to our list
            clients.append(self)
        except Exception as e:
            app_log.error(f"Problem establishing websocket for {self}: {e}")

    def on_data(self, data):
        """ Info message received from the obs controller, to be sent to the client web browser """
        app_log.debug(f"WS Received: {data}")
        msg = data[0].decode('UTF-8')

        async def write_message():
            client.write_message(msg)

        for client in clients:
            asyncio.run_coroutine_threadsafe(write_message(), self.ioloop)
        # Bokeh part
        self.update_bokeh(msg)

    def update_bokeh(self, msg):
        #user does not makes sense in websocket
        #user_key = tornado.escape.xhtml_escape(self.current_user)
        channel = msg.split(' ',1)[0]
        user_key = users_info.default_user
        if channel == "WEATHER":
            msg = json.loads(msg.split(' ', 1)[1])['data']
            self.update_weather_bokeh(user_key, msg)
        if channel == "GUIDING":
            msg = json.loads(msg.split(' ', 1)[1])['data']
            self.update_guiding_bokeh(user_key, msg)

    def update_weather_bokeh(self, user_key, data):
        update = {}
        update['date'] = [datetime.now()]
        update['safe'] = [data['safe']]
        update['WEATHER_RAIN_HOUR'] = [data['WEATHER_RAIN_HOUR']]
        update['WEATHER_TEMPERATURE'] = [data['WEATHER_TEMPERATURE']]
        update['WEATHER_WIND_GUST'] = [data['WEATHER_WIND_GUST']]
        update['WEATHER_WIND_SPEED'] = [data['WEATHER_WIND_SPEED']]

        source = users_info.weather_source_by_user_str[user_key]
        @tornado.gen.coroutine
        def update_callback():
            source.stream(update, rollover=7200)
        doc = users_info.weather_doc_by_user_str[user_key]  # type: Document
        doc.add_next_tick_callback(update_callback)  
        
    def update_guiding_bokeh(self, user_key, data):
        update = {}
        update['date'] = [datetime.now()]
        update['dx'] = [data['dx']]
        update['dy'] = [data['dy']]

        source = users_info.guiding_source_by_user_str[user_key]
        @tornado.gen.coroutine
        def update_callback():
            source.stream(update, rollover=7200)
        doc = users_info.guiding_doc_by_user_str[user_key]  # type: Document
        doc.add_next_tick_callback(update_callback)  

    def on_message(self, message):
        """ Command received from the client, to be sent to the obs controller """
        app_log.debug(f"WS Sent: {message}")
        cmd_publisher = self.settings['cmd_publisher']
        try:
            cmd_publisher.send_message('PAWS-CMD', message)
        except Exception as e:
            app_log.error(f"Problem sending message from PAWS {e}")

    def on_close(self):
        """ When client closes """
        try:
            clients.remove(self)
        except:
            pass
        app_log.debug("WS Closed")
