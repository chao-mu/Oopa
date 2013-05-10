#!/usr/bib/env python

"""
A tool to analyze wordlists
"""

import argparse
import codecs
import importlib
import inspect
import pkgutil

from oopa.analysis import Analysis
import oopa.modules

def main():
    analysis_classes = find_analysis_classes()

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
        default=10,
    )
    parser.add_argument(
        "--sort",
        help="The column to sort on",
        default=None,
    )
    parser.add_argument(
        "--pot",
        action="store_true",
        help="Use with john.pot and hashcat's --output-file",
    )
    args = parser.parse_args()

    analysis = analysis_classes[args.analysis]()

    words = read_wordlist(args.wordlist, args.encoding)

    if args.pot:
        words = ["".join(word.split(":", 1)[1:]) for word in words]

    for word in words:
        analysis.process(word)

    table = analysis.report() 
    if args.sort is not None:
        table.reversesort = True
        table.sortby = args.sort

    if args.top != "all" and table.end is None:
        table.end = int(args.top)

    if args.greppable:
        print table.greppable()
    else:
        print table

def read_wordlist(path, encoding="raw"):
    if encoding == "raw":
        wordlist = open(path, "r")
    else:
        wordlist = codecs.open(path, "r", encoding) 

    return wordlist.read().splitlines()

def find_analysis_classes():
    analyses = {}

    package_itr = pkgutil.walk_packages(
        path=oopa.modules.__path__,
        prefix=oopa.modules.__name__ + "."
    );

    for importer, mod_name, is_package in package_itr:
        if is_package:
            continue

        mod = importlib.import_module(mod_name)

        analysis = None
        for name, member in inspect.getmembers(mod, inspect.isclass):
            if Analysis.__name__ in [c.__name__ for c in member.__bases__]:
                analysis = member
        
        if analysis is None:
            print "Error: Analysis subclass not found in %s" % (mod.__path__)

        analyses[mod_name.split(".")[-1]] = analysis

    return analyses

if __name__ == "__main__":
    main()
