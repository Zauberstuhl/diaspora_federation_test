import cherrypy
import sqlite3
import sys
import os.path

from htmltemplate import Template

DB_STRING = "federation.db"

class Start(object):
    def renderTemplate(self, node, title, data):
        node.pagetitle.text = title
        node.item.repeat(self.renderItem, data)

    def renderItem(self, node, data):
        pod1, pod2, success = data
        node.pod1.text = pod1
        node.pod2.text = pod2
        node.result.html = self.result(success)

    def renderResult(self, node, success):
        if not success:
            node.info.atts['class'] = "glyphicons glyphicon-remove"

    def result(self, success):
        template = Template(open("templates/result.html").read())
        return template.render(self.renderResult, success)

    def index(self):
        data = []
        with sqlite3.connect(DB_STRING) as con:
            for row in con.execute("SELECT * FROM federation ORDER BY ROWID DESC"):
                data.append((row[0], row[1], row[2]))

        template = Template(open("templates/index.html").read())
        return template.render(self.renderTemplate, 'Index', data)

    index.exposed = True

class Register(object):
    def render(self, node, title):
        node.pagetitle.content = title

    def index(self):
        html = open("templates/register.html").read()
        template = Template(html)
        return template.render(self.render, 'Register')

    index.exposed = True


if __name__ == '__main__':
    if not os.path.isfile(DB_STRING):
        print("Please run test.py-script first!")
        sys.exit(1)

    cherrypy.tree.mount(Register(), '/register')
    cherrypy.tree.mount(Start())

    cherrypy.engine.start()
    cherrypy.engine.block()
