from datetime import datetime
from typing import TypeAlias

from pydantic import BaseModel, Field, validator

Date: TypeAlias = str


def check_date(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return value
    except ValueError:
        raise ValueError("date must be %Y-%m-%d %H:%M:%S format")


class BaseCollectionDataSchema(BaseModel):
    user_id: int = Field(...)
    first_name: str = Field(...)
    last_name: str | None = None
    user_name: str = Field(...)


class MongoCollectionDataSchema(BaseCollectionDataSchema):
    """
    Schema for data documents collection in Mongo Atlas DB.
    """

    start_command: list[Date] = Field(default_factory=list)
    help_command: list[Date] = Field(default_factory=list)
    donate_command: list[Date] = Field(default_factory=list)
    sent_greeting_message: list[Date] = Field(default_factory=list)
    radiation_monitoring: list[Date] = Field(default_factory=list)
    monitoring_points: list[Date] = Field(default_factory=list)
    sent_location: list[Date] = Field(default_factory=list)

    # validators
    _check_date = validator(
        "start_command",
        "help_command",
        "donate_command",
        "sent_greeting_message",
        "radiation_monitoring",
        "monitoring_points",
        "sent_location",
        each_item=True,
        allow_reuse=True,
    )(check_date)


class FileCollectionDataSchema(BaseCollectionDataSchema):
    """
    Schema for data documents collection in JSON file.
    """

    create_at: str = Field(...)

    # validators
    _check_date = validator("create_at", allow_reuse=True)(check_date)
