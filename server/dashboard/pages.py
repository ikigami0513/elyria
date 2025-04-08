from twisted.web import resource
from dashboard import env


class HomePage(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        template = env.get_template("index.html")
        html = template.render()
        return html.encode()
    