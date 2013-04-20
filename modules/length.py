"""
Analyzes the length of words in a wordlist.
"""

from collections import defaultdict

from prettytable import PrettyTable

from analysis import Analysis, frequency_table

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
        Reports occurences of length and summary
        """
        total = sum([c for c in self.length_counts.values()]) 
        lengths = self.length_counts.keys()

        table = PrettyTable(["Total Words", "Min", "Max"])
        table.add_row([total, min(lengths), max(lengths)])
        report = str(table)
 
        report += "\n\n"
        report += str(frequency_table("Length", self.length_counts, self.word_count))

        return report
