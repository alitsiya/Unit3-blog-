import os
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Content(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

        
class MainPage(Handler):
    def render_front(self, title="", content="", error=""):
        self.render("front.html", title=title, content=content, error = error)
    def get(self):
        self.render_front()
    def post(self):
        title = self.request.get("subject")
        content = self.request.get("content")
        if title and content:
        	a = Content(title=title, content = content)
        	a.put()
        	self.redirect("/newpost")
        else:
            error = "we need both a title and some content!" 
            self.render_front(title, content, error)

class ViewPost(Handler):
    def render_front(self):
        contents = db.GqlQuery("SELECT * FROM Content ORDER BY created DESC")
        self.render("main.html", contents = contents)
    def get(self):
        self.render_front()

app = webapp2.WSGIApplication([
    ('/newpost', MainPage), 
    ('/', ViewPost)
], debug=True)
