import io
import unittest

from ingredient_phrase_tagger.training import labelled_data


class ReaderTest(unittest.TestCase):

    def test_reads_valid_label_file(self):
        mock_file = io.BytesIO("""
index,input,name,qty,range_end,unit,comment
63,4 to 6 large cloves garlic,garlic,4.0,6.0,clove,
77,3 bananas,bananas,3.0,0.0,,
106,"2 1/2 pounds bell peppers (about 6 peppers in assorted colors), cut into 2-inch chunks",bell peppers,2.5,0.0,pound,"(about 6 peppers in assorted colors), cut into 2-inch chunks"
""".strip())
        reader = labelled_data.Reader(mock_file)
        self.assertEqual([{
            'input': u'4 to 6 large cloves garlic',
            'qty': 4.0,
            'unit': u'clove',
            'name': u'garlic',
            'range_end': 6.0,
            'comment': u'',
        }, {
            'input': u'3 bananas',
            'qty': 3.0,
            'unit': u'',
            'name': u'bananas',
            'comment': u'',
            'range_end': 0.0,
        }, {
            'input': (u'2 1/2 pounds bell peppers (about 6 peppers in '
                      u'assorted colors), cut into 2-inch chunks'),
            'qty':
            2.5,
            'unit':
            u'pound',
            'name':
            u'bell peppers',
            'range_end':
            0.0,
            'comment': (u'(about 6 peppers in assorted colors), cut into '
                        u'2-inch chunks'),
        }], [r for r in reader])

    def test_reads_file_with_utf8_encoding(self):
        mock_file = io.BytesIO(
            (u'index,input,name,qty,range_end,unit,comment\n'
             u'1,2 jalape\xc3\xb1os,jalape\xc3\xb1os,2.0,0.0,,,\n'
            ).encode('utf-8'))
        reader = labelled_data.Reader(mock_file)
        self.assertEqual([{
            'input': u'2 jalape\xc3\xb1os',
            'name': u'jalape\xc3\xb1os',
            'qty': 2.0,
            'unit': u'',
            'range_end': 0.0,
            'comment': u'',
        }], [r for r in reader])

    def test_interprets_empty_range_end_as_zero(self):
        mock_file = io.BytesIO("""
index,input,name,qty,range_end,unit,comment
77,3 bananas,bananas,3.0,,,
""".strip())
        reader = labelled_data.Reader(mock_file)
        self.assertEqual({
            'input': u'3 bananas',
            'qty': 3.0,
            'unit': u'',
            'name': u'bananas',
            'comment': u'',
            'range_end': 0.0,
        }, reader.next())

    def test_raises_error_when_csv_does_not_have_required_columns(self):
        with self.assertRaises(labelled_data.InvalidHeaderError):
            mock_file = io.BytesIO("""
index,input,UNEXPECTED_COLUMN,qty,range_end,unit,comment
77,3 bananas,bananas,3.0,0.0,,
""".strip())
            labelled_data.Reader(mock_file).next()


class WriterTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_writes_valid_rows(self):
        mock_file = io.BytesIO()
        writer = labelled_data.Writer(mock_file)
        writer.writerows([{
            'input': u'4 to 6 large cloves garlic',
            'qty': 4.0,
            'unit': u'clove',
            'name': u'garlic',
            'range_end': 6.0,
            'comment': u'',
        }, {
            'input': u'3 bananas',
            'qty': 3.0,
            'unit': u'',
            'name': u'bananas',
            'comment': u'',
            'range_end': 0.0,
        }, {
            'input': (u'2 1/2 pounds bell peppers (about 6 peppers in '
                      u'assorted colors), cut into 2-inch chunks'),
            'qty':
            2.5,
            'unit':
            u'pound',
            'name':
            u'bell peppers',
            'range_end':
            0.0,
            'comment': (u'(about 6 peppers in assorted colors), cut into '
                        u'2-inch chunks'),
        }])
        self.assertMultiLineEqual("""
input,name,qty,range_end,unit,comment
4 to 6 large cloves garlic,garlic,4.0,6.0,clove,
3 bananas,bananas,3.0,0.0,,
"2 1/2 pounds bell peppers (about 6 peppers in assorted colors), cut into 2-inch chunks",bell peppers,2.5,0.0,pound,"(about 6 peppers in assorted colors), cut into 2-inch chunks"
""".strip(),
                                  mock_file.getvalue().strip())

    def test_writes_valid_rows_one_by_one(self):
        mock_file = io.BytesIO()
        writer = labelled_data.Writer(mock_file)
        writer.writerow({
            'input': u'4 to 6 large cloves garlic',
            'qty': 4.0,
            'unit': u'clove',
            'name': u'garlic',
            'range_end': 6.0,
            'comment': u'',
        })
        writer.writerow({
            'input': u'3 bananas',
            'qty': 3.0,
            'unit': u'',
            'name': u'bananas',
            'comment': u'',
            'range_end': 0.0,
        })
        writer.writerow({
            'input': (u'2 1/2 pounds bell peppers (about 6 peppers in '
                      u'assorted colors), cut into 2-inch chunks'),
            'qty':
            2.5,
            'unit':
            u'pound',
            'name':
            u'bell peppers',
            'range_end':
            0.0,
            'comment': (u'(about 6 peppers in assorted colors), cut into '
                        u'2-inch chunks'),
        })
        self.assertMultiLineEqual("""
input,name,qty,range_end,unit,comment
4 to 6 large cloves garlic,garlic,4.0,6.0,clove,
3 bananas,bananas,3.0,0.0,,
"2 1/2 pounds bell peppers (about 6 peppers in assorted colors), cut into 2-inch chunks",bell peppers,2.5,0.0,pound,"(about 6 peppers in assorted colors), cut into 2-inch chunks"
""".strip(),
                                  mock_file.getvalue().strip())

    def test_writes_with_utf8_encoding(self):
        mock_file = io.BytesIO()
        writer = labelled_data.Writer(mock_file)
        writer.writerow({
            'input': u'2 jalape\xc3\xb1os',
            'name': u'jalape\xc3\xb1os',
            'qty': 2.0,
            'unit': u'',
            'range_end': 0.0,
            'comment': u'',
        })
        self.assertMultiLineEqual(
            (u'input,name,qty,range_end,unit,comment\n'
             u'2 jalape\xc3\xb1os,jalape\xc3\xb1os,2.0,0.0,,\n'),
            mock_file.getvalue().decode('utf-8'))
