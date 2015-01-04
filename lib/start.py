import sqlite3

from lib import tmpls

class Start(object):
    def renderTemplate(self, node, header, navbar, data):
        node.header = header
        node.navbar = navbar
        node.item.repeat(self.renderItem, data)

    def renderItem(self, node, data):
        podId, podName, status, timestamp = data
        node.timestamp.text = timestamp
        node.pod.html = "<a href=\"/pods/" + str(podId) + "\">" + podName + "</a>"
        if status < 90:
            status = "<span class=\"glyphicon glyphicon-warning-sign\"></span> " + str(status)
        node.status.html = str(status) + "%"

    def index(self):
        t = tmpls.Tmpls()
        data = []
        with sqlite3.connect('federation.db') as con:
            for row in con.execute("SELECT ROWID, podName, timestamp FROM pod ORDER BY ROWID DESC"):
                allCnt = 0
                successCnt = 0
                for podRow in con.execute("SELECT success FROM federation WHERE podId LIKE " + str(row[0])):
                    allCnt += 1
                    if podRow[0]: successCnt += 1
                percent = (successCnt / allCnt) * 100
                data.append((row[0], row[1], percent, row[2]))

        return t.index().render(self.renderTemplate, t.header(), t.navbar(), data)

    index.exposed = True

