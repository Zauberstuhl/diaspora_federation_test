import sqlite3

from htmltemplate import Template

class Start(object):
    def renderTemplate(self, node, data):
        node.item.repeat(self.renderItem, data)

    def renderItem(self, node, data):
        podId, podName, status = data
        node.pod.html = "<a href=\"/pods/" + str(podId) + "\">" + podName + "</a>"
        if status < 90:
            status = "<span class=\"glyphicon glyphicon-warning-sign\"></span> " + str(status)
        node.status.html = str(status) + "%"

    def index(self):
        data = []
        with sqlite3.connect('federation.db') as con:
            for row in con.execute("SELECT ROWID, podName FROM pod ORDER BY ROWID DESC"):
                allCnt = 0
                successCnt = 0
                for podRow in con.execute("SELECT success FROM federation WHERE podId LIKE " + str(row[0])):
                    allCnt += 1
                    if row[0]: successCnt += 1
                percent = (successCnt / allCnt) * 100
                data.append((row[0], row[1], percent))

        template = Template(open("templates/index.html").read())
        return template.render(self.renderTemplate, data)

    index.exposed = True

