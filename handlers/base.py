import tornado.escape
import tornado.web

from astropy import units as u

#from pocs.utils import current_time
from Service.NTPTimeService import NTPTimeService

class BaseHandler(tornado.web.RequestHandler):

    """
    BaseHandler is inherited by all Handlers and is responsible for any
    global operations. Provides the `db` property and the `get_current_user`
    """

    def initialize(self):
        self.config = self.settings['config']
        self.db = self.settings['db']
        self.serv_time = NTPTimeService()

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

class ObservationsHistoryHandler(BaseHandler):

    def get(self, days=None):

        if days is None:
            days = 1

        current_time = self.serv_time.getUTCFromNTP()
        date = (current_time - days * u.day).datetime

        # TODO TN FileDB is for dummies
        #observations = self.db.observations.aggregate([
        observations = self.db.get_current('observations').aggregate([
            {"$match": {"date": {"$gte": date}}},
            {'$group':
                {
                    "_id": "$data.field_name",
                    "count": {"$sum": "$data.number_exposure"},
                    "exp_time": {"$sum": "$data.time_per_exposure"},
                    "date": {"$max": "$date"}
                }
             },
            {'$sort': {'date': 1}}
        ])
        print('observations is {}'.format(observations))

        self.render('observation_list.hbs', observation_list=observations)
