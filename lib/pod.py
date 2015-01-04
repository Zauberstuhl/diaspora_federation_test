import sqlite3

from lib import tmpls, config

c = config.Config().load()

class Pod(object):
    def renderTemplate(self, node, header, navbar, data):
        node.header = header
        node.navbar = navbar
        node.item.repeat(self.renderItem, data)

    def renderItem(self, node, data):
        pod1, pod2, success = data
        node.pod1.text = pod1
        node.pod2.text = pod2
        node.result.html = self.result(success)

    def result(self, success):
        attr = "remove"
        if success: attr = "ok"
        return "<p class=\"glyphicon glyphicon-" + attr + "\"></p>"

    def getPod(self, podId=None):
        t = tmpls.Tmpls()
        data = []
        with sqlite3.connect(c['global']['database_path']) as con:
            for row in con.execute("SELECT pod1, pod2, success " +
                    "FROM federation WHERE podId LIKE " +
                    podId + " ORDER BY ROWID DESC"):
                data.append((row[0], row[1], row[2]))

        return t.pod().render(self.renderTemplate, t.header(), t.navbar(), data)

