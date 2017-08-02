import logging

class Loggable(object):
    """Mixin class to add logging."""
    
    def __init__(self, 
                 log_file_name = 'log.txt',
                 log_level = logging.INFO, 
                 log_name = 'MyApp'):
        self.log_file_name = log_file_name
        self.log_level = log_level
        self.log_name = log_name
        self.logger = self._get_logger()

    def _get_logger(self):
        # create our logger
        logger = logging.getLogger(self.log_name)
        logger.setLevel(self.log_level)
        
        # set a handler
        handler = logging.FileHandler(
                      self.log_file_name)
        logger.addHandler(handler)
        
        # format log entries
        formatter = logging.Formatter(
            "%(asctime)s: %(name)s - "
            "%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        
        return logger
        
    def log(self, log_line, severity=None):
        self.logger.log(severity or self.log_level,
                        log_line)

    def warn(self, log_line):
        self.logger.warn(log_line)


class MyClass(Loggable):
    """A class that you write."""
    
    def __init__(self):
        Loggable.__init__(self, 
                          log_file_name = 'log2.txt')
        #super(MyClass, self).__init__(
        #                  log_file_name = 'log2.txt')
        
    def do_something(self):
        print("Doing something!")
        self.log("I did something!")
        self.log("Some debugging info", logging.DEBUG)
        self.warn("Something bad happened!")

test = MyClass()
test.do_something()
