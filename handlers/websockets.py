import logging

from tornado.websocket import WebSocketHandler
from zmq.eventloop.zmqstream import ZMQStream

clients = []


class PanWebSocket(WebSocketHandler):

    def open(self, channel):
        """ Client opening connection to unit """

        if channel is None:
            channel = self.settings['name']

        logging.debug("Setting up subscriber for channel: {}".format(channel))

        try:
            self.stream = ZMQStream(self.settings['msg_subscriber'].subscriber)

            # Register the callback
            self.stream.on_recv(self.on_data)
            logging.debug("WS opened for channel {}".format(channel))

            # Add this client to our list
            clients.append(self)
        except Exception as e:
            logging.warning("Problem establishing websocket for {}: {}".format(self, e))

    def on_data(self, data):
        """ From the PANOPTES unit """
        msg = data[0].decode('UTF-8')
        logging.debug("WS Received: {}".format(msg))

        for client in clients:
            client.write_message(msg)

    def on_message(self, message):
        """ From the client """
        logging.debug("WS Sent: {}".format(message))
        # cmd_publisher = self.settings['cmd_publisher']
        # try:
        # cmd_publisher.send_message('PAWS', message)
        # except Exception as e:
        # print("Problem sending message from PAWS", e)

    def on_close(self):
        """ When client closes """
        clients.remove(self)
        logging.debug("WS Closed")
