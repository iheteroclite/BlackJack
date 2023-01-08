__version__ = 0.40
__author__ = 'iheteroclite'

import unittest
import pycodestyle


class TestCodeFormat(unittest.TestCase):

    def test_conformance(self):
        r"""Test conformity to PEP-8.

        'W503' (line break before binary operator) ignored as recent (2022)
        PEG-8 style guide prescribes avoidance of backslash \ for line
        continuation, and now allows/suggests mathematical long addition format
        """
        style = pycodestyle.StyleGuide(quiet=False, ignore=['W503'])
        result = style.check_files(['src/hand.py',
                                   # 'library/statistics.py',
                                    'library/io.py',
                                    'test/test_deck.py',
                                    'library/cheat.py',
                                    'src/sleeve.py',
                                    'test/test_probabilities.py',
                                    'test/test_style.py'])
        self.assertEqual(result.total_errors, 0,
                         'Found code style errors (and warnings).')

    def test_conformance_ignore_E722(self):
        r"""Test conformity to PEP-8.

        'E722' (bare except) ignored as this use case is in python3 docs"
        This means that try: except: is used without the ExceptionError
        can be used in this usecase as it features in python3 docs
        """
        style = pycodestyle.StyleGuide(quiet=False, ignore=['E722',
                                                            'W503'])
        result = style.check_files(['src/deck.py'])
        self.assertEqual(result.total_errors, 0,
                         'Found code style errors (and warnings).')

    def test_conformance_ignore_E226(self):
        r"""Test conformity to PEP-8.
        ignoring E226 as I think missing whitespace around a string
        operation is clearer:
        ' '*5 is clearer than ' ' * 5
        This is personal preference but I don't like to follow the
        style guide to the detriment of reader clarity.
        """
        style = pycodestyle.StyleGuide(quiet=False, ignore=['E226',
                                                            'W503'])
        result = style.check_files(['src/people.py'])
        self.assertEqual(result.total_errors, 0,
                         'Found code style errors (and warnings).')

    def test_conformance_change_line_length(self):
        r"""Test conformity to PEP-8.
        Ignoring line length in statistics, and one line reaches 83 chars,
        but is much clearer on a single line.
        in blackjack a line reaches 80 chars
        This is personal preference but I don't like to follow the
        style guide to the detriment of reader clarity.
        """

        style = pycodestyle.StyleGuide(quiet=False, ignore=['W503',
                                                            'E501'])
        result = style.check_files(['library/statistics.py',
                                    'blackjack.py'])
        self.assertEqual(result.total_errors, 0,
                         'Found code style errors (and warnings).')
