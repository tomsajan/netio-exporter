#!/usr/bin/env python

import argparse
import logging
import requests
import os

from collections import namedtuple
from wsgiref.simple_server import make_server
from prometheus_client import make_wsgi_app

from prometheus_client.core import (
    InfoMetricFamily, GaugeMetricFamily, REGISTRY, CounterMetricFamily
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('netio-exporter')

VERSION = '0.0.1'

# A named tuple that binds various aspects of each metric netio provides
Metric = namedtuple('Metric', ('metric_family', 'name', 'doc', 'unit', 'scale'))

# Unit usage: https://prometheus.io/docs/practices/naming/#base-units
# Basic units shall be used in prometheus, thus the scaling
# Netio presents some units in `mili` scale
METRIC_MAP = {
    'Voltage': Metric(GaugeMetricFamily, 'voltage', 'input voltage (V)', 'volts', 1),
    'Frequency': Metric(GaugeMetricFamily, 'frequency', 'frequency (Hz)', 'hertz', 1),
    'TotalCurrent': Metric(GaugeMetricFamily, 'current', 'total current (A)', 'amperes', 0.001),
    'OverallPowerFactor': Metric(GaugeMetricFamily, 'power_factor', 'overall power factor (ratio)',
                                 'ratio', 1),
    'TotalLoad': Metric(GaugeMetricFamily, 'load', 'total load (W)', 'watts', 1),
    'TotalEnergy': Metric(CounterMetricFamily, 'energy', 'total energy used (Wh)', 'watthours', 1),
    'State': Metric(GaugeMetricFamily, 'state', 'state of the outlet, 1 on, 0 off', '', 1),
    'Current': Metric(GaugeMetricFamily, 'current', 'current (A)', 'amperes', 0.001),
    'PowerFactor': Metric(GaugeMetricFamily, 'power_factor', 'power factor (ratio)', 'ratio', 1),
    'Load': Metric(GaugeMetricFamily, 'load', 'load (W)', 'watts', 1),
    'Energy': Metric(CounterMetricFamily, 'energy', 'energy used (Wh)', 'watthours', 1),
}


class NetioExporter:

    def __init__(self):
        self.args = self.parse_cmd_args()
        if self.args.debug:
            logger.setLevel(logging.DEBUG)

    @staticmethod
    def parse_cmd_args() -> argparse.Namespace:
        """
        Parse cmdline arguments. If argument not used, use NETIO_* env value,
        or fallback to default
        """
        logger.debug('Parsing arguments')
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--port',
                            dest='port',
                            type=int,
                            default=os.environ.get('NETIO_PORT', 9595),
                            help='Port to listen at')
        parser.add_argument('-u', '--netio-url',
                            dest='url',
                            default=os.environ.get('NETIO_URL', None),
                            # if non-empty ENV var is used,
                            # then the cmdline alternative is not required
                            required=not os.environ.get('NETIO_URL'),
                            help='Netio JSON API url')
        parser.add_argument('--username',
                            dest='username',
                            default=os.environ.get('NETIO_USERNAME', 'netio '),
                            help='Netio JSON API username')
        parser.add_argument('--password',
                            dest='password',
                            default=os.environ.get('NETIO_PASSWORD', 'netio'),
                            help='Netio JSON API password')
        parser.add_argument('-d', '--debug',
                            dest='debug',
                            action='store_true',
                            default=os.environ.get('NETIO_DEBUG', 'false').lower() == 'true',
                            help='Enable debug output')
        parser.add_argument('-t', '--timeout',
                            default=5,
                            type=int,
                            dest=os.environ.get('NETIO_TIMEOUT', 'timeout'),
                            help='Requests timeout')
        parser.add_argument('-v', '--version',
                            dest='version',
                            help='Print exporter version and exit',
                            action='version',
                            version=f'%(prog)s {VERSION}'
                            )

        return parser.parse_args()

    def __call__(self) -> None:
        logger.info('Starting Netio Prometheus Exporter')
        REGISTRY.register(NetioCollector(self.args))
        app = make_wsgi_app()
        httpd = make_server('', self.args.port, app)
        httpd.serve_forever()


class NetioCollector:
    def __init__(self, args):
        self.args = args
        self.data = {}
        self.metrics = []

    def scrape(self):
        """
        Obtain data from Netio
        """
        logger.debug(f'Scraping netio at {self.args.url}')
        r = requests.get(self.args.url,
                         auth=(self.args.username, self.args.password),
                         timeout=self.args.timeout)
        r.raise_for_status()
        self.data = r.json()

    def process_info(self):
        """
        Process Agent section of the json output
        """
        # netio info
        info = InfoMetricFamily('netio_agent', 'Global info about Netio agent')
        logger.debug('Processing netio agent info')
        info.add_metric([], {
            'model': self.data.get('Agent', {}).get('Model'),
            'version': self.data.get('Agent', {}).get('Version'),
            'json_version': self.data.get('Agent', {}).get('JSONVer'),
            'name': self.data.get('Agent', {}).get('DeviceName'),
            'outputs': str(self.data.get('Agent', {}).get('NumOutputs')),
            # in cobra, there is a `mac` field instead of the `SerialNumber` field. There are also some 4Cs, that have `SerialNumber` empty.
            'sn': (self.data.get('Agent', {}).get('SerialNumber') or
                   self.data.get('Agent', {}).get('MAC')) or
                  'Unknown',
            'target': self.args.url
        })
        logger.debug(f'Agent info metric: {info}')
        self.metrics.append(info)

    def process_global(self):
        """
        Process global section of the json output
        """
        # process global section
        logger.debug('Processing global stats')
        for key, value in self.data.get('GlobalMeasure', {}).items():
            metric_metadata = METRIC_MAP.get(key)
            if not metric_metadata:
                logger.debug(f'Global metric "{key}" not processed. '
                             f'Either not known or not wanted')
                continue
            logger.debug(f'Processing global metric "{key}"')
            self.metrics.append(
                # EXAMPLE:
                # GaugeMetricFamily('netio_global_power', 'global power measured',
                #                   unit='watthours', value=33)
                metric_metadata.metric_family(
                    f'netio_global_{metric_metadata.name}',
                    metric_metadata.doc,
                    unit=metric_metadata.unit,
                    # extract value and scale it to base SI units
                    value=value * metric_metadata.scale
                )
            )

    def process_outputs(self):
        """
        Process individual outputs of netio
        """
        # process individual outputs
        logger.debug('Processing individual Netio outputs.')
        outputs = self.data.get('Outputs')
        if not outputs:
            logger.debug('No output section found')
            return

        # assuming there is at least one output
        # and that all outputs have the same format

        # iterate over metrics
        for metric_name in outputs[0].keys():
            metric_metadata = METRIC_MAP.get(metric_name)
            if not metric_metadata:
                logger.debug(f'Output metric "{metric_name}" not processed. '
                             f'Either not known or not wanted')
                continue
            logger.debug(f'Processing "{metric_name}" output metric.')
            metric = metric_metadata.metric_family(
                f'netio_port_{metric_metadata.name}',
                metric_metadata.doc,
                unit=metric_metadata.unit,
                labels=['id','name']
            )

            # iterate over outputs
            # group the metric values from outputs
            for output in outputs:
                metric.add_metric(
                    labels=[str(output['ID']),str(output['Name'])],
                    # extract value and scale it to base SI units
                    value=output[metric_name] * metric_metadata.scale
                )
            self.metrics.append(metric)

    def process(self):
        # clean data from previous run
        self.metrics = []

        # process data
        self.process_info()
        self.process_global()
        self.process_outputs()

    def collect(self):
        """
        Called by Prometheus library on each prometheus request
        """
        self.scrape()
        self.process()

        for metric in self.metrics:
            yield metric


if __name__ == '__main__':
    ne = NetioExporter()
    ne()
