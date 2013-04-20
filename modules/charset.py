"""
Analyzes the character sets used in a wordlist.
"""

from collections import OrderedDict
import re

from prettytable import PrettyTable

from analysis import Analysis, frequency_table

class CharsetAnalysis(Analysis):

    def __init__(self):
        # We use an OrderedDict so reporting is consistent.
        self.charsets = OrderedDict([
            ["Lower Alpha", r'^[a-z]+$'],
            ["Upper Alpha", r'^[A-Z]+$'],
            ["Mixed Alpha", r'^(?=.*[a-z])(?=.*[A-Z])[a-zA-Z]+$'],
            ["Numeric", r'^\d+$'],
            ["Lower Alphanumeric", r'^(?=.*\d)(?=.*[a-z])[a-z0-9]+$'],
            ["Upper Alphanumeric", r'^(?=.*\d)(?=.*[A-Z])[A-Z0-9]+$'],
            ["Mixed Alphanumeric", r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])[a-zA-Z\d]+$'],
        ])
        self.charset_counts = OrderedDict([])
        for key, regex in self.charsets.iteritems():
            self.charsets[key] = re.compile(regex)
            self.charset_counts[key] = 0

        super(CharsetAnalysis, self).__init__()

    def analyze(self, word):
        for key, prog in self.charsets.iteritems():
            if prog.match(word):
                self.charset_counts[key] += 1

    def report(self):
        total = self.word_count
        table = frequency_table("Charset", self.charset_counts, total);

        return table
