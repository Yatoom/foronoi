class Tell:
    @staticmethod
    def print(verbose, *text, sep=' ', end='\n', file=None):
        if not verbose:
            return
        print(*text, sep=sep, end=end, file=file)
