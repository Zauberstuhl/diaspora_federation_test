from htmltemplate import Template

class Tmpls(object):
    def index(self): return Template(open("templates/index.html").read())
    def header(self): return Template(open("templates/header.html").read())
    def navbar(self): return Template(open("templates/navbar.html").read())
    def pod(self): return Template(open("templates/pod.html").read())

