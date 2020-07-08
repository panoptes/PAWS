""" Collection of UI modules for the admin web interface

"""

# Web stuff
import bokeh
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

class BaseUIModule(tornado.web.UIModule):

    """
    BaseUIModule is inherited by all Handlers and is responsible for any
    global operations. Provides the `db` property and the `get_current_user`
    """

    def get_current_user(self):
        """
        Looks for a cookie that shows we have been logged in. If cookie
        is found, attempt to look up user info in the database
        """
        user_data = None
        try:
            user_data = tornado.escape.xhtml_escape(
                self.get_secure_cookie("user"))
        except TypeError as e:
            pass

        # Get email from cookie
        #email = tornado.escape.to_unicode(self.get_secure_cookie("email"))
        #if not email:
        #    return None

        # Look up user data
        #user_data = self.db.admin.find_one({'username': email})
        #if user_data is None:
        #    return None

        return user_data

class GuideInfo(BaseUIModule):

    """ Displays information about the mount """

    def render(self, template_path):
        user_str = tornado.escape.xhtml_escape(self.current_user)
        script = bokeh.embed.server_session(session_id=user_str,
            url='http://localhost:5006/bokeh_guiding')
        return self.render_string("guiding_info.hbs", script=script)

class FocusInfo(tornado.web.UIModule):

    """ Displays information about the last focus """

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


class WeatherInfo(BaseUIModule):

    """ Displays information about the mount """

    def render(self, template_path):
        user_str = tornado.escape.xhtml_escape(self.current_user)
        script = bokeh.embed.server_session(session_id=user_str,
            url='http://localhost:5006/bokeh_weather')
        return self.render_string(template_path, script=script)


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
