import json
from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        """Converts a string to a dict.

        Body()を使うと文字列になるので、dictに変換する。
        """
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
