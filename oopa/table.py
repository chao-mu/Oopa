from prettytable import PrettyTable

class AnalysisTable(PrettyTable):

    def _get_rows(self, options):
        """
        Taken and modified from prettytable.py until the following is resolved:
        https://code.google.com/p/prettytable/issues/detail?id=29
        """
        rows = copy.deepcopy(self._rows)

        # Sort if necessary
        if options["sortby"]:
            sortindex = self._field_names.index(options["sortby"])
            # Decorate
            rows = [[row[sortindex]]+row for row in rows]
            # Sort
            rows.sort(reverse=options["reversesort"], key=options["sort_key"])
            # Undecorate
            rows = [row[1:] for row in rows]

        return rows[options["start"]:options["end"]]

    def greppable(self, sep=':'):
        """
        The table as a string that's grep friendly.
        Field names prefixed by #
        """
        options = self._get_options({})

        output = "#" + sep.join(self._field_names)
        for row in self._get_rows(options):
            output += "\n" + sep.join(map(unicode, row))

        return output

class FrequencyTable(AnalysisTable):

    def __init__(self, primary_field, **kwargs):
        """
        Adds Percentage and Count columns. The are calculated
        when add_counts is called. Same arguments as AnalysisTable.
        """
        field_names = [primary_field, "Percentage", "Count"]

        if "sortby" not in kwargs:
            kwargs["reversesort"] =True
            kwargs["sortby"] = "Count" 

        super(FrequencyTable, self).__init__(field_names, **kwargs)

    def add_counts(self, total, counts):
        for key, count in counts.iteritems():
            percent = round(count / float(total) * 100, 2)
            self.add_row([key, percent, count])
