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
