from prometheus_client.core import (
    InfoMetricFamily, GaugeMetricFamily, REGISTRY
)
from datetime import datetime
import requests

from prometheus_client import make_wsgi_app
from wsgiref.simple_server import make_server


class NetioCollector:
    def __init__(self):
        self.data = {}
        self.url = 'http://192.168.0.242/netio.json'


    def scrape(self):
        r = requests.get(self.url, auth=('netio', 'netio'))
        r.raise_for_status()
        print(r.json())
        self.data = r.json()

    def collect(self):
        self.scrape()
        i = InfoMetricFamily('netio_info', 'popisek')
        i.add_sample('agent', {k: str(v) for k, v in self.data['Agent'].items()}, 1)
        # i.info(self.data['Agent'])
        yield i



if __name__ == '__main__':
    REGISTRY.register(NetioCollector())
    app = make_wsgi_app()
    httpd = make_server('', 9595, app)
    httpd.serve_forever()
