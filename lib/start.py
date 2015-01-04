import sqlite3

from lib import tmpls, config

c = config.Config().load()

class Start(object):
    def renderTemplate(self, node, header, navbar, data):
        node.header = header
        node.navbar = navbar
        node.item.repeat(self.renderItem, data)

    def renderItem(self, node, data):
        podId, podName, percent, timestamp = data
        node.timestamp.text = timestamp
        node.pod.html = "<a href=\"/pods/" + str(podId) + "\">" + podName + "</a>"
        status = "{0:.2f}%".format(percent)
        if percent < 90:
            status = "<span class=\"glyphicon glyphicon-warning-sign\"></span> " + status
        node.status.html = status

    def index(self):
        t = tmpls.Tmpls()
        data = []
        with sqlite3.connect(c['global']['database_path']) as con:
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

