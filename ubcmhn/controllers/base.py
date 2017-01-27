## Base Controller to be used in the app's controllers
## Automatically instantiates a Db connection, using config's params.

from ubcmhn.config.configloader import CfgClass
from ubcmhn.model import DbEngine
from ubcmhn.util.useful_baseclasses import LoggableBase

# All controllers inherit from this one.
class BaseController(LoggableBase):
    def __init__(self, config : CfgClass):

        # save CONFIG
        self.config = config

        # get Database Object, and clear the session object.
        self.db = self.__getdatabase()

        # Run custom init.
        self.init()

    def init(self):
        """Override this to do additional initialization"""
        pass

    def __getdatabase(self) -> DbEngine:
        return DbEngine(self.config)