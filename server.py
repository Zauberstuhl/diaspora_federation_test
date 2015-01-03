import cherrypy
import sys
import os.path

from lib import start, pod, register

if __name__ == '__main__':
    if not os.path.isfile('federation.db'):
        print("Please run test.py-script first!")
        sys.exit(1)

    d = cherrypy.dispatch.RoutesDispatcher()
    d.connect('getPod-1', '/pods/:podId', controller=pod.Pod(), action='getPod')

    # global config
    #cherrypy.config.update({'environment': 'production'})

    conf = {'/pods' : {'request.dispatch' : d}}
    cherrypy.tree.mount(register.Register(), '/register')
    cherrypy.tree.mount(start.Start(), config=conf)

    cherrypy.engine.start()
    cherrypy.engine.block()
