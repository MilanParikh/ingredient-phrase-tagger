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

                _coerce_values_to_numbers(row)

                try:
                    print translator.translate_row(row)
                # ToDo: deal with this
                except UnicodeDecodeError:
                    print ''

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


def _coerce_values_to_numbers(row):
    """Converts string values in a row to numbers where possible.

    Args:
        row: A row of labelled ingredient data. This is modified in place so
            that any of its values that contain a number (e.g. "6.4") are
            converted to floats and the 'index' value is converted to an int.
    """
    for key in row:
        if key == 'index':
            row[key] = int(row[key])
        else:
            try:
                row[key] = float(row[key])
            except ValueError:
                pass
