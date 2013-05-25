import cherrypy
import sqlite3
from datetime import datetime, timedelta
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
                        ORDER BY ts DESC''', (datetime.now()-timedelta(seconds=5),)).fetchall()
        conn.commit()
        conn.close()
        #render the template
        template = self.env.get_template("data.html")
        return template.render(samples=s)
    samples.exposed = True


if __name__ == "__main__":
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 80,
                           })
    cherrypy.quickstart(HelloWorld(), "/")
