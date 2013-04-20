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
        description="Analyzes wordlists and prints pretty descriptions."
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
#    parser.add_argument(
#        "--limit",
#        help="The number of results to cap at in long reports",
#        type=int,
#        default=10,
#    )
    args = parser.parse_args()

    analysis = analysis_classes[args.analysis]()

    if args.encoding == "raw":
        wordlist = open(args.wordlist, 'r')
    else:
        wordlist = codecs.open(args.wordlist, 'r', args.encoding) 

    words = wordlist.read().splitlines()
    for word in words:
        analysis.process(word)
    
    print analysis

def find_analysis_classes(module_dir):
    analyses = {}
    for path in glob.glob(os.path.join(module_dir, "*.py")):
        directory, filename = os.path.split(path)

        if re.match("^__", filename):
            continue

        analysis_name = re.sub("\.py$", "", filename)
        mod = importlib.import_module("%s.%s" % (module_dir, analysis_name))

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

def frequency_table(key_header, counts, total):
    rows = []
    for key, count in counts.iteritems():
        percent = round(count / float(total) * 100, 2)
        rows.append([key, percent, count])

    table = PrettyTable([key_header, "Percentage", "Count"])
    for row in rows:
        table.add_row(row)

    return table

if __name__ == "__main__":
    main()
