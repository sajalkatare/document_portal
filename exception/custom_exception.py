import sys
import traceback
from logger.custom_logger import CustomLogger

logger = CustomLogger().get_logger(__file__)

class DocumentPortalException(Exception):
    """Custom exception for Document Portal errors."""
    def __init__(self, error_message:str, error_details:sys):
        _,_,exe_tb = error_details.exc_info()
        self.file_name = exe_tb.tb_frame.f_code.co_filename
        self.lineno = exe_tb.tb_lineno
        self.error_message = str(error_message)
        self.traceback_str = ''.join(traceback.format_exception(*error_details.exc_info()))
    
        

    def __str__(self):
        return f"""
        Error In : {self.file_name}
        At Line Number: {self.lineno}
        Error Message: {self.error_message}
        Traceback: {self.traceback_str}
        """

if __name__ == "__main__":
    try:
        a = 1 / 0  # This will raise a ZeroDivisionError
        print(a)
    except Exception as e:
        app_exception = DocumentPortalException(e,sys)
        logger.error(app_exception)
        raise app_exception