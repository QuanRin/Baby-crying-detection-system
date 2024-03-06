class RegisterInfo:
    def __init__(self, username,
                 age, phone_number, email, password
                 ) -> None:
        self.username = username
        self.age = age
        self.phone_number = phone_number
        self.email = email
        self.password = password

    @classmethod
    def from_json(cls, json: dict[str, any]):
        return cls(json['username'], json['age'], json['phone_number'], json['email'], json['password'])


class LoginInfo:

    @classmethod
    def from_credenticals(cls, email: str, password: str):
        return cls(0, email, password, None)

    @classmethod
    def from_access_token(cls, access_token: str):
        return cls(1, None, None, access_token)

    def __init__(self, type, email, password, access_token) -> None:
        self.type = type
        self.email = email
        self.password = password
        self.access_token = access_token

    @classmethod
    def from_json(cls, json: dict[str, any]):
        return cls(json['type'], json['email'], json['password'], json['access_token'])
