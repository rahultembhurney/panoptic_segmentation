import sys 

def error_message_detail(error, error_detail: sys):
    _, _, execution_info = error_detail.exc_info()

    filename = execution_info.tb_frame.f_code.co_filename
    line_no = execution_info.tb_lineno

    error_message = f"Error in script: {filename} \n line number: {line_no} \n message: {str(error)}."
    
    return error_message

class AppException(Exception):
    def __init__(self, error_message, error_details):
        '''
        Params:
            error_message: error message in string format.
        "'''
        super().__init__(error_message)

        self.error_message = error_message_detail(
            error=error_message,
            error_detail=error_details
        )

    def __str__(self):
        return self.error_message
