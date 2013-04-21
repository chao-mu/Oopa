from collections import defaultdict
import operator
import re

from analysis import AnalysisTable, Analysis, FrequencyTable

CHAR_MIN = 3

class KeywordAnalysis(Analysis):
    """
    Attempts to find common "keywords" in a password list by
    removing leading and trailing non-alphabetic characters,
    unifying case, and then reporting results.
    """

    def __init__(self):
        self.keywords = defaultdict(lambda: 0)

        super(KeywordAnalysis, self).__init__()

    def analyze(self, word):
        """
        Stores keyword counts in in self.keywords
        """
        keyword = word.lower()
        keyword = re.sub(r'[^a-z]+$', '', keyword)
        keyword = re.sub(r'^[^a-z]+', '', keyword)

        if len(keyword) >= CHAR_MIN:
            self.keywords[keyword] += 1

    def report(self):
        """
        Reports top possible keywords 
        """
        table = AnalysisTable(
            ["Keyword", "Count"],
            sortby="Count",
            reversesort=True
        )
        for keyword, count in self.keywords.iteritems():
            table.add_row([keyword, count])

        return table
