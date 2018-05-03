import io
import unittest

from ingredient_phrase_tagger.training import labelled_data
from ingredient_phrase_tagger.training import partitioner


class PartitionerTest(unittest.TestCase):

    def setUp(self):
        self.mock_training_file = io.BytesIO()
        self.mock_training_writer = labelled_data.Writer(
            self.mock_training_file)
        self.mock_testing_file = io.BytesIO()
        self.mock_testing_writer = labelled_data.Writer(self.mock_testing_file)

    def test_partition_80_percent_training(self):
        mock_label_reader = labelled_data.Reader(
            io.BytesIO("""
input,name,qty,range_end,unit,comment
1 cup foo,foo,1.0,0.0,cup,
2 drops foz,foz,2.0,0.0,drop,
3 ml faa,faa,3.0,0.0,ml,
4 cloves bar,bar,4.0,0.0,cloves,
5 oz baz,baz,5.0,0.0,oz,
""".strip()))
        partitioner.split_labels(
            mock_label_reader,
            self.mock_training_writer,
            self.mock_testing_writer,
            training_fraction=0.8)
        self.assertMultiLineEqual("""
input,name,qty,range_end,unit,comment
1 cup foo,foo,1.0,0.0,cup,
2 drops foz,foz,2.0,0.0,drop,
3 ml faa,faa,3.0,0.0,ml,
4 cloves bar,bar,4.0,0.0,cloves,
""".strip(),
                                  self.mock_training_file.getvalue().strip())
        self.assertMultiLineEqual("""
input,name,qty,range_end,unit,comment
5 oz baz,baz,5.0,0.0,oz,
""".strip(),
                                  self.mock_testing_file.getvalue().strip())

    def test_partition_20_percent_training(self):
        mock_label_reader = labelled_data.Reader(
            io.BytesIO("""
input,name,qty,range_end,unit,comment
1 cup foo,foo,1.0,0.0,cup,
2 drops foz,foz,2.0,0.0,drop,
3 ml faa,faa,3.0,0.0,ml,
4 cloves bar,bar,4.0,0.0,cloves,
5 oz baz,baz,5.0,0.0,oz,
""".strip()))
        partitioner.split_labels(
            mock_label_reader,
            self.mock_training_writer,
            self.mock_testing_writer,
            training_fraction=0.2)
        self.assertMultiLineEqual("""
input,name,qty,range_end,unit,comment
1 cup foo,foo,1.0,0.0,cup,
""".strip(),
                                  self.mock_training_file.getvalue().strip())
        self.assertMultiLineEqual("""
input,name,qty,range_end,unit,comment
2 drops foz,foz,2.0,0.0,drop,
3 ml faa,faa,3.0,0.0,ml,
4 cloves bar,bar,4.0,0.0,cloves,
5 oz baz,baz,5.0,0.0,oz,
""".strip(),
                                  self.mock_testing_file.getvalue().strip())

    def test_partition_with_max_labels_discards_labels(self):
        mock_label_reader = labelled_data.Reader(
            io.BytesIO("""
input,name,qty,range_end,unit,comment
1 cup foo,foo,1.0,0.0,cup,
2 drops foz,foz,2.0,0.0,drop,
3 ml faa,faa,3.0,0.0,ml,
4 cloves bar,bar,4.0,0.0,cloves,
5 oz baz,baz,5.0,0.0,oz,
""".strip()))
        partitioner.split_labels(
            mock_label_reader,
            self.mock_training_writer,
            self.mock_testing_writer,
            training_fraction=0.67,
            max_labels=3)
        self.assertMultiLineEqual("""
input,name,qty,range_end,unit,comment
1 cup foo,foo,1.0,0.0,cup,
2 drops foz,foz,2.0,0.0,drop,
""".strip(),
                                  self.mock_training_file.getvalue().strip())
        self.assertMultiLineEqual("""
input,name,qty,range_end,unit,comment
3 ml faa,faa,3.0,0.0,ml,
""".strip(),
                                  self.mock_testing_file.getvalue().strip())
