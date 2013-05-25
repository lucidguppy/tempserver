import cherrypy
import sqlite3
from datetime import datetime, timedelta
import time
from jinja2 import Environment, PackageLoader



class HelloWorld:
    def __init__(self):
        self.env = Environment(loader=PackageLoader('tempserver', 'templates'))

    def index(self):
        return "HELLO WORLD"
    index.exposed = True

    def samples(self):
        #open the dbo
        conn = sqlite3.connect('temperatures.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        c = conn.cursor()
        s = c.execute('''SELECT * FROM temperatures
                        WHERE ts > ?
                        ORDER BY ts ASC''', (datetime.now()-timedelta(hours=24),))
        samples = []
        ii = 0
        for row in s:
            samples.append((time.mktime(row[0].timetuple())*1000,row[-1]))
            ii +=1
        conn.commit()
        conn.close()
        #render the template
        template = self.env.get_template("data.html")
        return template.render(samples=samples)
    samples.exposed = True


if __name__ == "__main__":
    import os.path 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {'global':{'server.socket_host': '0.0.0.0',
            'server.socket_port': 80,},
            "/": {'tools.staticdir.root': current_dir},
	    "/static": {'tools.staticdir.on': True,
                        'tools.staticdir.dir':'static'} }
    cherrypy.quickstart(HelloWorld(),'/',config=conf)
