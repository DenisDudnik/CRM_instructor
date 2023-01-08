import datetime
import uuid
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, validator


class MessageTypes(str, Enum):
    notify = 'notify'
    message = 'message'
    init = 'init'


class UserItem(BaseModel):
    id: uuid.UUID
    name: str


class WebsocketData(BaseModel):
    kind: MessageTypes
    from_user: Union[UserItem, str]
    to_user: Optional[Union[UserItem, str]]
    text: Optional[str]
    timestamp: str = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')

    @validator('timestamp', pre=True)
    def format_date(cls, value: datetime.datetime) -> str:
        if isinstance(value, datetime.datetime):
            value = value.strftime('%d-%m-%Y %H:%M')
        return value


class UsersList(BaseModel):
    result: List[UserItem]
