import os

class AppSettings():
    name = ""
    value = ""

    @staticmethod
    def get(name):
        returnVal = AppSettings()
        returnVal.name = name
        returnVal.value = os.environ.get(name)
        if not returnVal.value:
            raise Exception("Setting not found")
        else:
            return returnVal
