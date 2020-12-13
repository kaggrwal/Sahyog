
class AuthenticationErrors:

     UserAlreadyExistsError = {
         "message": "User with given username already exists",
         "status": 400
     }
     LoginFailureError = {
        "message": "Login Failure, Please check the login details and login again ",
        "status": 400
     }
     UserNotFoundError = {
         "message": "User not found with this username",
         "status": 400
     }
