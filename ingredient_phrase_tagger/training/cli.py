import csv
import optparse

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

        with open(self.opts.data_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for index, row in enumerate(csv_reader):
                if index < start or index >= end:
                    continue

                parsed_row = _parse_row(row)

                print translator.translate_row(parsed_row).encode('utf-8')

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


def _parse_row(row):
    """Converts string values in a row to numbers where possible.

    Args:
        row: A row of labelled ingredient data. This is modified in place so
            that any of its values that contain a number (e.g. "6.4") are
            converted to floats and the 'index' value is converted to an int.
    """
    return {
        'input': row['input'].decode('utf-8'),
        'name': row['name'].decode('utf-8'),
        'qty': float(row['qty']),
        'range_end': float(row['range_end']),
        'unit': row['unit'].decode('utf-8'),
        'comment': row['comment'].decode('utf-8'),
    }
