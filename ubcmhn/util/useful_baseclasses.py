import logging

# Class that can be inherited to provide a .l() logger method.
class LoggableBase(object):
    def l(self) -> logging.Logger:
        loggerobj = getattr(self, '__logger__', None)

        if not loggerobj:
            self.__logger__ = logging.getLogger(self.__class__.__name__)

        return self.__logger__