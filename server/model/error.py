import json


class ErrorResponse:
    def __init__(self, message="Unknown error has occurenced") -> None:
        self.message = message

    def to_json(self, to_string: bool) -> dict[str, any] | str:
        json_obj = dict(message=self.message)
        if to_string:
            return json.dumps(json_obj)
        return json_obj
