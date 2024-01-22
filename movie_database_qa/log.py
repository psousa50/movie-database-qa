class Log:
    def __init__(self, options={}):
        self.options = options

    def log(self, *args):
        print(*args)

    def log_if(self, type, *args):
        if type in self.options.get("types", []):
            print(*args)

    def verbose(self, *args):
        if self.options.get("verbose", False):
            print(*args)


_log = Log()


def verbose(*args):
    _log.verbose(*args)


def log(*args):
    _log.log(*args)


def log_if(type, *args):
    _log.log_if(type, *args)


def setup_log(options):
    _log.options = options
