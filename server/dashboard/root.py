from twisted.web import resource, static
from dashboard.pages import *


class DashboardRoot(resource.Resource):
    def __init__(self):
        super().__init__()
        self.putChild(b"", HomePage())
        
        self.putChild(b"static", static.File("server/dashboard/static"))
