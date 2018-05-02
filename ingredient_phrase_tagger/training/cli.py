import optparse

import labelled_data
import translator


class Cli(object):

    def __init__(self, argv):
        self.opts = self._parse_args(argv)
        self._upstream_cursor = None

    def run(self):
        self.generate_data(self.opts.count, self.opts.offset)

    def generate_data(self, count, offset):
        """
        Generates training data in the CRF++ format for the ingredient
        tagging task
        """

        start = int(offset)
        end = int(offset) + int(count)

        with open(self.opts.data_path) as data_file:
            data_reader = labelled_data.Reader(data_file)
            for index, row in enumerate(data_reader):
                if index < start or index >= end:
                    continue

                print translator.translate_row(row).encode('utf-8')

    def _parse_args(self, argv):
        """
        Parse the command-line arguments into a dict.
        """

        opts = optparse.OptionParser()

        opts.add_option("--count", default="100", help="(%default)")
        opts.add_option("--offset", default="0", help="(%default)")
        opts.add_option(
            "--data-path",
            default="nyt-ingredients-snapshot-2015.csv",
            help="(%default)")

        (options, args) = opts.parse_args(argv)
        return options
