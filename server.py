import cherrypy
import sys
import os

from lib import start, pod

if __name__ == '__main__':
    if not os.path.isfile('federation.db'):
        print("Please run test.py-script first!")
        sys.exit(1)

    d = cherrypy.dispatch.RoutesDispatcher()
    d.connect('getPod-1', '/pods/:podId', controller=pod.Pod(), action='getPod')

    # global config
    cherrypy.config.update({
        'environment': 'production',
        'log.error_file': 'error.log'
    })

    conf = {
        '/pods' : {'request.dispatch' : d},
        '/fonts': {
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : os.getcwd() + '/static/fonts'
        }
    }
    cherrypy.tree.mount(start.Start(), config=conf)

    cherrypy.engine.start()
    cherrypy.engine.block()
