import tornado.escape
import tornado.web

import glob


class BaseHandler(tornado.web.RequestHandler):

    """
    BaseHandler is inherited by all Handlers and is responsible for any
    global operations. Provides the `db` property and the `get_current_user`
    """

    def initialize(self):
        self.config = self.settings['config']
        self.db = self.settings['db']

    def get_current_user(self):
        """
        Looks for a cookie that shows we have been logged in. If cookie
        is found, attempt to look up user info in the database
        """
        # Get email from cookie
        email = tornado.escape.to_unicode(self.get_secure_cookie("email"))
        if not email:
            return None

        # Look up user data
        user_data = self.db.admin.find_one({'username': email})
        if user_data is None:
            return None

        return user_data


class MainHandler(BaseHandler):

    def get(self):
        user_data = self.get_current_user()

        self.render("main.hbs", user_data=user_data, db=self.db)


class ImagesHandler(BaseHandler):

    def get(self, sequence=None):

        if sequence > '':

            img_dir = '/var/panoptes/images/fields'

            # target_list = glob.glob("{}/*".format(img_dir))
            # visit_list = glob.glob("{}/**/*".format(img_dir))
            img_list = glob.glob("{}/{}/*.jpg".format(img_dir, sequence))

            images = [img.replace('/var/panoptes/images/fields/', '') for img in img_list]

            images.sort()
            images.reverse()

            self.render("images.hbs", images=images)
        else:
            self.render("no_images.hbs")
