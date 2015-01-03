from htmltemplate import Template

class Register(object):
    def render(self, node, title):
        node.pagetitle.content = title

    def index(self):
        html = open("templates/register.html").read()
        template = Template(html)
        return template.render(self.render, 'Register')

    index.exposed = True

