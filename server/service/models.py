class WrapResponseDto:
    def __init__(self, message: str | None, result: dict[str, any] | None, error = None) -> None:
        self.message = message
        self.result = result
        self._error = error
        
    @classmethod
    def error(cls, error: str, message: str | None = "Something went wrong"):
        return cls(message, None, error)
    
    @classmethod
    def success(cls, result: dict[str, any] | None, message: str | None = "Success"):
        return cls(message, result)
    
    def to_json(self):
        return dict(
            message=self.message,
            result=self.result,
            error=self._error
        )
        
    @property
    def is_error(self):
        return self._error != None and self._error

class RegisterRequestDto:
    def __init__(self, email, phone_number, password) -> None:
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.username = "Nugget"
        
    def name(self, username: str):
        self.username = username
        return self

    @classmethod
    def from_json(cls, json: dict[str, any]):
        register_info = cls(json['email'], json['phone_number'], json['password'])
        if 'username' in json:
            register_info = register_info.name(json['username'])
        return register_info

class LoginRequestDto:
    def __init__(self, email, password, access_token) -> None:
        self.email = email
        self.password = password
        self.access_token = access_token
    
    @classmethod
    def from_access_token(cls, token: str):
        return cls(None, None, token)
    
    @classmethod
    def from_user_credentical(cls, email: str, password: str):
        return cls(email, password, None)
    
    @classmethod 
    def from_json(cls, json: dict[str, any]):
        return cls(json.get('email'), json.get('password'), json.get('access_token'))
    
    @property
    def type(self):
        """Return: 
        0 if login by email and password
        1 if login by access token
        -1 if error (missing email or password, missing all)
        """
        if self.email and self.password:
            return 0
        if self.access_token:
            return 1
        return -1
    
class LoginResponseDto:
    def __init__(self, access_token, refresh_token) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token
        
    def to_json(self):
        return dict(
            access_token=self.access_token,
            refresh_token=self.refresh_token
        )