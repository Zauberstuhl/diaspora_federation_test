import sqlite3

from htmltemplate import Template

class Pod(object):
    def renderTemplate(self, node, data):
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

    def getPod(self, podId=None):
        data = []
        with sqlite3.connect('federation.db') as con:
            for row in con.execute("SELECT pod1, pod2, success " +
                    "FROM federation WHERE podId LIKE " +
                    podId + " ORDER BY ROWID DESC"):
                data.append((row[0], row[1], row[2]))

        template = Template(open("templates/pod.html").read())
        return template.render(self.renderTemplate, data)

