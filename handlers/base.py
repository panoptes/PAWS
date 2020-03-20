# Web stuff
import tornado

# Astro stuff
from astropy import units as u

# POCS stuff
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

class LoginHandler(BaseHandler):
    def get(self):
        self.render(
                'login_template.html',
        )

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

class MainHandler(BaseHandler):

    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        user_data = self.current_user
        self.render("main.hbs", user_data=user_data, db=self.db)

def bokeh_weather_app(doc):
    # Setup source for data
    source = ColumnDataSource(dict(x=[], y=[]))
    columns = [
        TableColumn(field="x", title="X"),
        TableColumn(field="y", title="Y"),
    ]
    data_table = DataTable(source=source, columns=columns)
    user_str = doc.session_context.id
    doc_by_user_str[user_str] = doc
    source_by_user_str[user_str] = source
    
    # Now setup nice plot
    #Graph configuration
    p = figure(title="Title", title_location='above',
               sizing_mode="scale_width", plot_width=800, plot_height=500)
    #Add Y Grid line - Set color to none
    p.ygrid.grid_line_color = None
    #Add X axis label
    p.xaxis.axis_label = "Date"
    #https://docs.bokeh.org/en/latest/docs/reference/models/formatters.html#bokeh.models.formatters.DatetimeTickFormatter
    p.xaxis.formatter=DatetimeTickFormatter()
    #Add Y axis Label
    p.yaxis.axis_label = "Value"
    #Set Title configuration
    p.title.text_color = "black"
    p.title.text_font = "times"
    p.title.text_font_style = "italic"
    #Set background configuration
    p.background_fill_color = "white"
    p.background_fill_alpha = 0.5
    #Change X axis orientation label
    #p.xaxis.major_label_orientation = 1.2
    #------------Hover configuration -----------------#
    #https://docs.bokeh.org/en/latest/docs/user_guide/tools.html?highlight=hover#basic-tooltips
    # Add the HoverTool to the figure for showing spectrum values
    p.add_tools(HoverTool(tooltips=[
                                    ("Date", "@x{%H:%M}"),
                                    ("Value", "@y{0.00}")],
                          formatters={'@x': 'datetime'},
                          mode='vline'))
    # Plot actual data
    p.line('x', 'y',  source=source, legend_label='My variable of interest')
    #Set legen configuration (position and show/hide)
    p.legend.location = "top_left"
    p.legend.click_policy="hide"

    # Add to the doc
    doc.add_root(p)

class ObservationsHistoryHandler(BaseHandler):

    @tornado.gen.coroutine
    @tornado.web.authenticated
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
