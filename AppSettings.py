import os
from AppLogger import AppLogger

class AppSettings():
    name = ""
    value = ""

    @staticmethod
    def get(name):
        returnVal = AppSettings()
        returnVal.name = name
        returnVal.value = os.environ.get(name)
        if not returnVal.value:
            raise Exception(("Setting %s not found") % (returnVal.name))
        else:
            AppLogger.log("Setting {} = {}".format(returnVal.name, returnVal.value))
            return returnVal.value
