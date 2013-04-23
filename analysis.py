#!/usr/bib/env python

"""
A tool to analyze wordlists
"""

import argparse
import codecs
from collections import OrderedDict
import glob
import importlib
import inspect
import os
import re

from prettytable import PrettyTable

def main():
    analysis_classes = find_analysis_classes("modules")

    parser = argparse.ArgumentParser(
        description="Analyzes wordlists and prints pretty descriptions.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "wordlist",
        help="Wordlist to analyze",
    )
    parser.add_argument(
        "--analysis",
        help="Which analysis to run",
        required=True,
        choices=analysis_classes.keys()
    )
    parser.add_argument(
        "--encoding",
        help="Expected file encoding",
        default="raw",
    )
    parser.add_argument(
        "--greppable",
        help="An output able to easily be processed",
        action='store_true',
    )
    parser.add_argument(
        "--top",
        help="The number of rows to cap at in long reports",
        default=20,
    )
    args = parser.parse_args()

    analysis = analysis_classes[args.analysis]()

    if args.encoding == "raw":
        wordlist = open(args.wordlist, 'r')
    else:
        wordlist = codecs.open(args.wordlist, 'r', args.encoding) 

    words = wordlist.read().splitlines()
    for word in words:
        analysis.process(word)
    
    table = analysis.report()
    if args.top != "all":
        table.trim(int(args.top))

    if args.greppable:
        print table.greppable()
    else:
        print table

def find_analysis_classes(module_dir):
    analyses = {}
    for path in glob.glob(os.path.join(module_dir, "*.py")):
        directory, filename = os.path.split(path)

        if re.match("^__", filename):
            continue

        analysis_name = re.sub("\.py$", "", filename)
        mod_name = "%s.%s" % (module_dir, analysis_name)
        mod = importlib.import_module(mod_name)

        analysis = None
        for name, member in inspect.getmembers(mod, inspect.isclass):
            if Analysis.__name__ in [c.__name__ for c in member.__bases__]:
                analysis = member
        
        if analysis is None:
            raise Exception("Analysis subclass not found in %s" % (path))        

        analyses[analysis_name] = analysis

    return analyses

class Analysis(object):

    def __init__(self):
        self.word_count = 0

    def process(self, word):
        self.word_count += 1
        self.analyze(word)

    def analyze(self, word):
        """
        Analyze a single value and update instance variables.
        """
        raise NotImplementedError

    def report(self):
        """
        Report on analysis
        """
        raise NotImplementedError

    def __str__(self):
        return str(self.report())

class AnalysisTable(PrettyTable):

    def greppable(self, sep=':'):
        options = self._get_options({})

        output = "#" + sep.join(self._field_names)
        for row in self._get_rows(options):
            output += "\n" + sep.join(map(unicode, row))

        return output

    def trim(self, n):
        """
        Reduce to n rows.
        """
        options = self._get_options({})
        self._rows = self._get_rows(options)[:n]

class FrequencyTable(AnalysisTable):

    def __init__(self, primary_field, **kwargs):
        """
        Adds Percentage and Count columns. The are calculated
        when add_counts is called. Same arguments as AnalysisTable.
        """
        field_names = [primary_field, "Percentage", "Count"]
        
        super(FrequencyTable, self).__init__(field_names, **kwargs)

    def add_counts(self, total, counts):
        for key, count in counts.iteritems():
            percent = round(count / float(total) * 100, 2)
            self.add_row([key, percent, count])

if __name__ == "__main__":
    main()
