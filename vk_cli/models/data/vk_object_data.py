import datetime
from dataclasses import dataclass

from dacite import Config


@dataclass
class VKObjectData:
    id: int | None  # идентификатор объекта
    source: dict

    class Meta:
        config = Config(
            type_hooks={
                datetime.datetime: datetime.datetime.fromtimestamp,
                bool: bool,
                int: int,
            }
        )


@dataclass
class VKOwnedObjectData(VKObjectData):
    owner_id: int  # идентификатор владельца объекта
