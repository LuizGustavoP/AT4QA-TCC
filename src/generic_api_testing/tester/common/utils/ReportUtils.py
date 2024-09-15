from common.config.config import GeneralSettings

class ReportUtils():

    def print_debug(str: str):
        
        if GeneralSettings.debug:
            print(str)