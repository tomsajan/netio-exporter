from prometheus_client.core import (
    InfoMetricFamily, GaugeMetricFamily, REGISTRY, CounterMetricFamily
)
from datetime import datetime
from collections import namedtuple
import requests

from prometheus_client import make_wsgi_app
from wsgiref.simple_server import make_server

Metric = namedtuple('Metric', ('metric_family', 'name', 'doc', 'unit'))

# Unit usage: https://prometheus.io/docs/practices/naming/#base-units
METRIC_DB = {
    'Voltage': Metric(GaugeMetricFamily, 'voltage', 'input voltage (V)', 'volts'),
    'Frequency': Metric(GaugeMetricFamily, 'frequency', 'frequency (Hz)', 'hertz'),
    'TotalCurrent': Metric(GaugeMetricFamily, 'current', 'total current (A)', 'amperes'),
    'OverallPowerFactor': Metric(GaugeMetricFamily, 'power_factor', 'overall power factor (ratio)',
                                 'ratio'),
    'TotalLoad': Metric(GaugeMetricFamily, 'load', 'total load (W)', 'watts'),
    'TotalEnergy': Metric(CounterMetricFamily, 'energy', 'total energy used (Wh)', 'watthours'),
    'State': Metric(GaugeMetricFamily, 'state', 'state of the outlet, 1 on, 0 off', ''),
    'Current': Metric(GaugeMetricFamily, 'current', 'current (A)', 'amperes'),
    'PowerFactor': Metric(GaugeMetricFamily, 'power_factor', 'power factor (ratio)', 'ratio'),
    'Load': Metric(GaugeMetricFamily, 'load', 'load (W)', 'watts'),
    'Energy': Metric(CounterMetricFamily, 'energy', 'energy used (Wh)', 'watthours'),
    # name
}


class NetioCollector:
    def __init__(self):
        self.data = {}
        self.url = 'http://192.168.0.242/netio.json'
        self.metrics = []

    def scrape(self):
        r = requests.get(self.url, auth=('netio', 'netio'))
        r.raise_for_status()
        print(r.json())
        self.data = r.json()

    def scrape_mock(self):
        from mock import MOCK_4C, MOCK_COBRA
        self.data = MOCK_COBRA

    def process_data(self):
        # clean data from previous run
        self.metrics = []

        # process global section
        for key, value in self.data.get('GlobalMeasure', {}).items():
            metric_metadata = METRIC_DB.get(key)
            if not metric_metadata:
                continue
            self.metrics.append(
                # EXAMPLE:
                # GaugeMetricFamily('netio_global_power', 'global power measured',
                #                   unit='watthours', value=33)
                metric_metadata.metric_family(
                    f'netio_global_{metric_metadata.name}',
                    metric_metadata.doc,
                    unit=metric_metadata.unit,
                    value=value
                )
            )

        # process individual outputs

        outputs = self.data.get('Outputs')
        if not outputs:
            return

        # assuming there is at least one output
        # and that all outputs have the same format

        # iterate over metrics
        for metric_name in outputs[0].keys():
            metric_metadata = METRIC_DB.get(metric_name)
            if not metric_metadata:
                continue
            metric = metric_metadata.metric_family(
                f'netio_port_{metric_metadata.name}',
                metric_metadata.doc,
                unit=metric_metadata.unit,
                labels=['id']
            )

            # iterate over outputs
            # group the metric values from outputs
            for output in outputs:
                metric.add_metric(
                    labels=[str(output['ID'])],
                    value=output[metric_name]
                )
            self.metrics.append(metric)



    def collect(self):
        # self.scrape()
        self.scrape_mock()

        # i = InfoMetricFamily('netio_info', 'popisek')
        # i.add_sample('agent', {k: str(v) for k, v in self.data['Agent'].items()}, 1)
        # i.info(self.data['Agent'])

        # yield i
        self.process_data()

        for metric in self.metrics:
            yield metric




if __name__ == '__main__':
    REGISTRY.register(NetioCollector())
    app = make_wsgi_app()
    httpd = make_server('', 9595, app)
    httpd.serve_forever()
