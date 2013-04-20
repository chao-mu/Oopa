"""
Detect common languages
"""

from collections import defaultdict
import re

import enchant

from analysis import Analysis, frequency_table

class LanguageAnalysis(Analysis):
    """
    Languages found in passwords
    """

    def __init__(self):
        self.language_count = {}
        self.dicts = {}
        for lang in enchant.list_languages():
            try:
                self.dicts[lang] = enchant.Dict(lang)
                self.language_count[lang] = 0
            except enchant.errors.DictNotFoundError:
                continue

        super(LanguageAnalysis, self).__init__()

    def analyze(self, word):
        """
        Increment language count
        """
            
        for lang, dic in self.dicts.iteritems():
            if dic.check(word):
                self.language_count[lang] += 1

    def report(self):
        return frequency_table("Language", self.language_count, self.word_count)
