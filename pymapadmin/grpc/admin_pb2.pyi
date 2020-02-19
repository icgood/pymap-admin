# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    List as typing___List,
    Optional as typing___Optional,
    Text as typing___Text,
    Tuple as typing___Tuple,
    Union as typing___Union,
    cast as typing___cast,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int
builtin___str = str
if sys.version_info < (3,):
    builtin___buffer = buffer
    builtin___unicode = unicode


class Result(builtin___int):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    @classmethod
    def Name(cls, number: builtin___int) -> builtin___str: ...
    @classmethod
    def Value(cls, name: builtin___str) -> 'Result': ...
    @classmethod
    def keys(cls) -> typing___List[builtin___str]: ...
    @classmethod
    def values(cls) -> typing___List['Result']: ...
    @classmethod
    def items(cls) -> typing___List[typing___Tuple[builtin___str, 'Result']]: ...
    SUCCESS = typing___cast('Result', 0)
    ERROR_RESPONSE = typing___cast('Result', 1)
SUCCESS = typing___cast('Result', 0)
ERROR_RESPONSE = typing___cast('Result', 1)

class PingRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    client_version = ... # type: typing___Text

    def __init__(self,
        *,
        client_version : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> PingRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> PingRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"client_version"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"client_version",b"client_version"]) -> None: ...

class PingResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    server_version = ... # type: typing___Text

    def __init__(self,
        *,
        server_version : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> PingResponse: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> PingResponse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"server_version"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"server_version",b"server_version"]) -> None: ...

class Login(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    user = ... # type: typing___Text

    def __init__(self,
        *,
        user : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Login: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Login: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"user"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"user",b"user"]) -> None: ...

class AppendRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    sender = ... # type: typing___Text
    recipient = ... # type: typing___Text
    mailbox = ... # type: typing___Text
    data = ... # type: builtin___bytes
    flags = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    when = ... # type: builtin___int

    @property
    def login(self) -> Login: ...

    def __init__(self,
        *,
        login : typing___Optional[Login] = None,
        sender : typing___Optional[typing___Text] = None,
        recipient : typing___Optional[typing___Text] = None,
        mailbox : typing___Optional[typing___Text] = None,
        data : typing___Optional[builtin___bytes] = None,
        flags : typing___Optional[typing___Iterable[typing___Text]] = None,
        when : typing___Optional[builtin___int] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> AppendRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> AppendRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"login"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"data",u"flags",u"login",u"mailbox",u"recipient",u"sender",u"when"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"login",b"login"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"data",b"data",u"flags",b"flags",u"login",b"login",u"mailbox",b"mailbox",u"recipient",b"recipient",u"sender",b"sender",u"when",b"when"]) -> None: ...

class AppendResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    result = ... # type: Result
    error_type = ... # type: typing___Text
    error_response = ... # type: builtin___bytes
    mailbox = ... # type: typing___Text
    validity = ... # type: builtin___int
    uid = ... # type: builtin___int

    def __init__(self,
        *,
        result : typing___Optional[Result] = None,
        error_type : typing___Optional[typing___Text] = None,
        error_response : typing___Optional[builtin___bytes] = None,
        mailbox : typing___Optional[typing___Text] = None,
        validity : typing___Optional[builtin___int] = None,
        uid : typing___Optional[builtin___int] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> AppendResponse: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> AppendResponse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"error_response",u"error_type",u"mailbox",u"result",u"uid",u"validity"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"error_response",b"error_response",u"error_type",b"error_type",u"mailbox",b"mailbox",u"result",b"result",u"uid",b"uid",u"validity",b"validity"]) -> None: ...
