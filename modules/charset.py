"""
Analyzes the character sets used in a wordlist.
"""

from collections import OrderedDict
import re

from oopa.analysis import Analysis
from oopa.table import FrequencyTable

class CharsetAnalysis(Analysis):

    def __init__(self):
        # We use an OrderedDict so that order is preserved in rows.
        self.charsets = OrderedDict([
            ["Lower Alpha", r'^[a-z]+$'],
            ["Upper Alpha", r'^[A-Z]+$'],
            ["Mixed Alpha", r'^(?=.*[a-z])(?=.*[A-Z])[a-zA-Z]+$'],
            ["Numeric", r'^\d+$'],
            ["Lower Alphanumeric", r'^(?=.*\d)(?=.*[a-z])[a-z0-9]+$'],
            ["Upper Alphanumeric", r'^(?=.*\d)(?=.*[A-Z])[A-Z0-9]+$'],
            ["Mixed Alphanumeric", r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])[a-zA-Z\d]+$'],
            ["Special", r'^[^a-zA-Z\d]+$'],
            ["Special, Numeric", r'^(?=.*\d)(?=.*[^a-zA-Z\d])[^a-zA-Z]+$'],
            ["Special, Lower Alpha", '^(?=.*[a-z])(?=.*[^a-zA-Z\d])[^\dA-Z]+$'],
            ["Special, Upper Alpha", '^(?=.*[A-Z])(?=.*[^a-zA-Z\d])[^\da-z]+$'],
            ["Special, Mixed Alpha", '^(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z\d])[^\d]+$'],
            ["Special, Lower Alphanumeric", r'^(?=.*\d)(?=.*[a-z])(?=.*[^a-zA-Z\d])[^A-Z]+$'],
            ["Special, Upper Alphanumeric", r'^(?=.*\d)(?=.*[A-Z])(?=.*[^a-zA-Z\d])[^a-z]+$'],
            ["Special, Mixed Alphanumeric", r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z\d])'],
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
        table = FrequencyTable("Charset", end=len(self.charset_counts))

        table.add_counts(self.word_count, self.charset_counts)

        return table
