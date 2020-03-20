""" Collection of UI modules for the admin web interface

"""
import tornado


def listify(obj):
    """ Given an object, return a list

    Always returns a list. If obj is None, returns empty list,
    if obj is list, just returns obj, otherwise returns list with
    obj as single member.

    Returns:
        list:   You guessed it.
    """
    if obj is None:
        return []
    else:
        return obj if isinstance(obj, (list, type(None))) else [obj]

class BokehPlot(tornado.web.UIModule):

    """ Displays information about the mount """

    def render(self, template_path):
        return self.render_string(template_path)

class MountInfo(tornado.web.UIModule):

    """ Displays information about the mount """

    def render(self):
        return self.render_string("mount_info.hbs")


class SystemInfo(tornado.web.UIModule):

    """ Displays information about the mount """

    def render(self):
        return self.render_string("system_info.hbs")


class WeatherInfo(tornado.web.UIModule):

    """ Displays information about the mount """

    def render(self):
        return self.render_string("weather_info.hbs")


class CameraInfo(tornado.web.UIModule):

    """ Displays information about the mount """

    def render(self):
        return self.render_string("camera_info.hbs")


class StateInfo(tornado.web.UIModule):

    """ Displays information about the mount """

    def render(self):
        return self.render_string("state_info.hbs")


class ObservationInfo(tornado.web.UIModule):

    """ Displays information about the target """

    def render(self):
        return self.render_string("observation_info.hbs")


class SensorStatus(tornado.web.UIModule):

    """ UI modules for the environmental sensors """

    def render(self):
        return self.render_string("sensor_status.hbs")


class BotChat(tornado.web.UIModule):

    """ UI modules for chatting with the bot """

    def render(self):
        return self.render_string("bot_chat.hbs")


class PolarAlign(tornado.web.UIModule):

    """ UI modules for chatting with the bot """

    def render(self):

        return self.render_string("polar_align.hbs")


class Webcam(tornado.web.UIModule):

    """ A module for showing the webcam """

    def render(self, webcam):
        return self.render_string("webcams.hbs", webcam=webcam)


class Image(tornado.web.UIModule):

    """ UI modules for listing the current images """

    def render(self, img_fn, id, title='', size=2):

        imgs = listify(img_fn)

        return self.render_string("display_image.hbs", img_list=imgs, title=title, id=id)


class ImageList(tornado.web.UIModule):

    """ UI modules for listing the current images """

    def render(self, images=[]):

        return self.render_string("image_list.hbs", images=images)
