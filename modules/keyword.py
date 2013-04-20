"""
Attempts to find common "keywords" in a password list
"""

from collections import defaultdict
import re

from prettytable import PrettyTable

from analysis import Analysis, frequency_table

CHAR_MIN = 3

class KeywordAnalysis(Analysis):

    def __init__(self):
        self.keywords = defaultdict(lambda: 0)

        regex = [
            r'^[^a-z]*([a-z]+)[^a-z]*$',
        ]
        self.keyword_regex = [re.compile(r) for r in regex]

        super(KeywordAnalysis, self).__init__()

    def analyze(self, word):
        """
        Stores keyword counts in in self.keywords
        """
        for keyword in self.extract_keywords(word):
            self.keywords[keyword] += 1

    def extract_keywords(self, source):
        keywords = set()
        source = source.lower()
        
        for word in source.split():
            if self.is_keyword(word):
                keywords.add(word)

            for prog in self.keyword_regex:
                result = prog.match(word)
                if result is None:
                    continue
                words = [g for g in result.groups() if self.is_keyword(g)]
                keywords.update(words)

        return keywords

    def is_keyword(self, word):
        return len(word) >= CHAR_MIN

    def report(self):
        """
        Reports top possible keywords 
        """
        inverted = defaultdict(lambda: [])
        for keyword, count in self.keywords.iteritems():
            inverted[count].append(keyword) 

        if not inverted:
            return "No keywords of length >= %s found" % (CHAR_MIN)

        if max(inverted.keys()) == 1:
            return "No keywords found more than once"

        table = PrettyTable(["Keyword", "Count"])
        while table.rowcount < 10 and inverted:
            current_max = max(inverted.keys())

            if current_max <= 1:
                break

            for keyword in inverted[current_max]:
                table.add_row([keyword, current_max])

            del inverted[current_max]

        return table
