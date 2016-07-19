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


class MountInfo(tornado.web.UIModule):

    """ Displays information about the mount """

    def render(self):
        return self.render_string("mount_info.html")


class SystemInfo(tornado.web.UIModule):

    """ Displays information about the mount """

    def render(self):
        return self.render_string("system_info.html")


class WeatherInfo(tornado.web.UIModule):

    """ Displays information about the mount """

    def render(self):
        return self.render_string("weather_info.html")


class CameraInfo(tornado.web.UIModule):

    """ Displays information about the mount """

    def render(self):
        return self.render_string("camera_info.html")


class StateInfo(tornado.web.UIModule):

    """ Displays information about the mount """

    def render(self):
        return self.render_string("state_info.html")


class TargetInfo(tornado.web.UIModule):

    """ Displays information about the target """

    def render(self):
        return self.render_string("target_info.html")


class SensorStatus(tornado.web.UIModule):

    """ UI modules for the environmental sensors """

    def render(self):

        return self.render_string("sensor_status.html")


class BotChat(tornado.web.UIModule):

    """ UI modules for chatting with the bot """

    def render(self):

        return self.render_string("bot_chat.html")


class Webcam(tornado.web.UIModule):

    """ A module for showing the webcam """

    def render(self, webcam):
        return self.render_string("webcams.html", webcam=webcam)


class CurrentImage(tornado.web.UIModule):

    """ UI modules for listing the current images """

    def render(self, img_fn, id, title='', size=2):

        imgs = listify(img_fn)

        return self.render_string("display_image.html", img_list=imgs, title=title, id=id)


class ImageList(tornado.web.UIModule):

    """ UI modules for listing the current images """

    def render(self, targets=[], visits=[], images=[]):

        return self.render_string("image_list.html", target_list=targets, visit_list=visits, img_list=images)
