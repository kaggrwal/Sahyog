
class ValidationFailException(Exception):

    def __init__(self,errors, msg):
       self.errors = errors

class UserServiceException(Exception):

    def __init__(self,errors, msg):
       self.errors = errors
