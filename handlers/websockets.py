from tornado.websocket import WebSocketHandler

from zmq.eventloop.zmqstream import ZMQStream
import logging

clients = []


class PanWebSocket(WebSocketHandler):
    logger = logging.getLogger('PAWS')

    def open(self, channel):
        """ Client opening connection to unit """
        if channel is None:
            channel = self.settings['name']

        self.logger.info("Setting up listener for channel: {}".format(channel))

        try:
            messaging = self.settings['messaging']

            self.socket = messaging.register_listener(channel=channel)
            self.stream = ZMQStream(self.socket)

            # Register the callback
            self.stream.on_recv(self.on_data)
            self.logger.info("WS opened for channel {}".format(channel))

            # Add this client to our list
            clients.append(self)
        except Exception as e:
            self.logger.warning("Problem establishing websocket for {}: {}".format(self, e))

    def on_data(self, data):
        """ From the PANOPTES unit """
        msg = data[0].decode('UTF-8')
        self.logger.debug("WS Received: {}".format(msg))
        self.write_message(msg)

    def on_message(self, message):
        """ From the client """
        self.logger.info("WS Sent: {}".format(message))

    def on_close(self):
        """ When client closes """
        clients.remove(self)
        self.logger.info("WS Closed")
