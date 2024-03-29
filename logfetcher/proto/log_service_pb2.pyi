from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BossResponse(_message.Message):
    __slots__ = ["rankings"]
    RANKINGS_FIELD_NUMBER: _ClassVar[int]
    rankings: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, rankings: _Optional[_Iterable[int]] = ...) -> None: ...

class CharacterAddRequest(_message.Message):
    __slots__ = ["channel_id", "rio_character_link"]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    RIO_CHARACTER_LINK_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    rio_character_link: str
    def __init__(self, rio_character_link: _Optional[str] = ..., channel_id: _Optional[str] = ...) -> None: ...

class CharacterAddResponse(_message.Message):
    __slots__ = ["rd_char_id"]
    RD_CHAR_ID_FIELD_NUMBER: _ClassVar[int]
    rd_char_id: int
    def __init__(self, rd_char_id: _Optional[int] = ...) -> None: ...

class DRRequest(_message.Message):
    __slots__ = ["dung", "rio_link"]
    DUNG_FIELD_NUMBER: _ClassVar[int]
    RIO_LINK_FIELD_NUMBER: _ClassVar[int]
    dung: str
    rio_link: str
    def __init__(self, dung: _Optional[str] = ..., rio_link: _Optional[str] = ...) -> None: ...

class DRResponse(_message.Message):
    __slots__ = ["name", "rankings"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RANKINGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    rankings: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, name: _Optional[str] = ..., rankings: _Optional[_Iterable[int]] = ...) -> None: ...

class GuildAddRequest(_message.Message):
    __slots__ = ["channel_id", "rio_guild_link"]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    RIO_GUILD_LINK_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    rio_guild_link: str
    def __init__(self, rio_guild_link: _Optional[str] = ..., channel_id: _Optional[str] = ...) -> None: ...

class GuildAddResponse(_message.Message):
    __slots__ = ["rd_guild_id"]
    RD_GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    rd_guild_id: int
    def __init__(self, rd_guild_id: _Optional[int] = ...) -> None: ...

class RRRequest(_message.Message):
    __slots__ = ["dfffc", "raid", "rio_link"]
    DFFFC_FIELD_NUMBER: _ClassVar[int]
    RAID_FIELD_NUMBER: _ClassVar[int]
    RIO_LINK_FIELD_NUMBER: _ClassVar[int]
    dfffc: int
    raid: str
    rio_link: str
    def __init__(self, raid: _Optional[str] = ..., dfffc: _Optional[int] = ..., rio_link: _Optional[str] = ...) -> None: ...

class RRResponse(_message.Message):
    __slots__ = ["name", "rankings"]
    class RankingsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: BossResponse
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[BossResponse, _Mapping]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    RANKINGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    rankings: _containers.MessageMap[str, BossResponse]
    def __init__(self, name: _Optional[str] = ..., rankings: _Optional[_Mapping[str, BossResponse]] = ...) -> None: ...
