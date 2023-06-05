from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class BossResponse(_message.Message):
    __slots__ = ["rankings"]
    RANKINGS_FIELD_NUMBER: _ClassVar[int]
    rankings: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, rankings: _Optional[_Iterable[int]] = ...) -> None: ...

class DRRequest(_message.Message):
    __slots__ = ["dung", "rio_link"]
    DUNG_FIELD_NUMBER: _ClassVar[int]
    RIO_LINK_FIELD_NUMBER: _ClassVar[int]
    dung: str
    rio_link: str
    def __init__(
        self, dung: _Optional[str] = ..., rio_link: _Optional[str] = ...
    ) -> None: ...

class DRResponse(_message.Message):
    __slots__ = ["name", "rankings"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RANKINGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    rankings: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self, name: _Optional[str] = ..., rankings: _Optional[_Iterable[int]] = ...
    ) -> None: ...

class RRRequest(_message.Message):
    __slots__ = ["dfffc", "raid", "rio_link"]
    DFFFC_FIELD_NUMBER: _ClassVar[int]
    RAID_FIELD_NUMBER: _ClassVar[int]
    RIO_LINK_FIELD_NUMBER: _ClassVar[int]
    dfffc: str
    raid: str
    rio_link: str
    def __init__(
        self,
        raid: _Optional[str] = ...,
        dfffc: _Optional[str] = ...,
        rio_link: _Optional[str] = ...,
    ) -> None: ...

class RRResponse(_message.Message):
    __slots__ = ["name", "rankings"]

    class RankingsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: BossResponse
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[BossResponse, _Mapping]] = ...,
        ) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    RANKINGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    rankings: _containers.MessageMap[str, BossResponse]
    def __init__(
        self,
        name: _Optional[str] = ...,
        rankings: _Optional[_Mapping[str, BossResponse]] = ...,
    ) -> None: ...
