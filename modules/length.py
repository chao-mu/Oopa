"""
Analyzes the length of words in a wordlist.
"""

from collections import defaultdict

from analysis import Analysis, AnalysisTable, FrequencyTable

class LengthAnalysis(Analysis):

    def __init__(self):
        self.length_counts = defaultdict(lambda: 0)

        super(LengthAnalysis, self).__init__()

    def analyze(self, word):
        """
        Records the length of each string
        """
        length = len(word)
        self.length_counts[length] += 1

    def report(self):
        """
        Reports occurences of length
        """
        table = FrequencyTable("Length", sortby="Length")

        table.add_counts(self.word_count, self.length_counts)

        return table
