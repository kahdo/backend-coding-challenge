import json
import os
from configparser import ConfigParser

from ubcmhn.util.useful_baseclasses import LoggableBase


class ConfigLoaderBase(dict, LoggableBase):
    def __init__(self, configname, rootpath="", configpath="configs", cfgfilename="config.ini",
                 datapath = 'data'):
        l = self.l()

        self.configname = configname

        # Generate Root Path
        self.rootpath = rootpath
        if not self.rootpath:
            self.rootpath = os.getcwd()
        l.debug("Root path = {0}".format(self.rootpath))

        # Generate Data Path
        wanteddatapath = os.path.join(self.rootpath, datapath)
        if os.path.isdir(wanteddatapath):
            self.datapath = wanteddatapath
            l.debug("Data path = {0}".format(self.datapath))
        else:
            l.debug("Missing Data Path.")

        # Generate Config Path
        self.configpath = os.path.join(self.rootpath, configpath)
        l.debug("Config path = {0}".format(self.configpath))

        self.wantedconfigfile = os.path.join(self.configpath, cfgfilename)
        l.debug("Wanted Config = {0}".format(self.wantedconfigfile))

        # Open config file.
        self.config = ConfigParser()
        self.config.read(self.wantedconfigfile)

        self.configsection = self.config[self.configname]
        l.debug("Opened Config \"{0}\"".format(self.configsection))

        # Iterate and set each attribute directly on the instance.
        # Populate __keys[].
        for _k in self.configsection:
            upkey = str(_k).upper()
            self[upkey] = self.configsection[upkey]

        ## Update or postprocess variables
        self.initproperties()

    def initproperties(self):
        """
        Override this to be able to postprocess configvars and generally modify the configloader
        I like to directly convert and assign variables to instance attributes, enabling autocomplete
        functionality in PyCharm, making everything a breeze inside the IDE.
        """
        pass

    def dumpvalues(self):
        l = self.l()
        l.debug("Attribute Dump:")
        for key in self.keys():
            l.debug("{0} = \"{1}\"".format(key, self[key]))

    def __repr__(self):
        return "<ConfigLoader: config[{0}] has {1} keys>".format(self.configname, len(self.keys()))


class UbcmhnConfigLoader(ConfigLoaderBase):
    def initproperties(self):

        # Autocomplete goodness.
        self.LOGLEVEL = -1
        self.LOGSTDOUT = -1
        self.URLPREFIX = ""
        self.DBCONNECTSTR = ""
        self.DBNAME = ""
        self.CELERYAPPNAME = ""
        self.CELERYBROKER = ""
        self.CELERYBACKEND = ""

        # Quickie: Make everything that looks like an int be and int :-)
        for _k in self:
            try:
                self[_k] = int(self[_k])
            except ValueError:
                continue
            finally:
                setattr(self, _k, self[_k])

# Use this class as the system's config class.
CfgClass = UbcmhnConfigLoader