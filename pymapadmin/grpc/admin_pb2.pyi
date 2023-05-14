"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _ResultCode:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _ResultCodeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ResultCode.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    SUCCESS: _ResultCode.ValueType  # 0
    FAILURE: _ResultCode.ValueType  # 1

class ResultCode(_ResultCode, metaclass=_ResultCodeEnumTypeWrapper): ...

SUCCESS: ResultCode.ValueType  # 0
FAILURE: ResultCode.ValueType  # 1
global___ResultCode = ResultCode

@typing_extensions.final
class Result(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CODE_FIELD_NUMBER: builtins.int
    RESPONSE_FIELD_NUMBER: builtins.int
    KEY_FIELD_NUMBER: builtins.int
    code: global___ResultCode.ValueType
    response: builtins.bytes
    key: builtins.str
    def __init__(
        self,
        *,
        code: global___ResultCode.ValueType = ...,
        response: builtins.bytes = ...,
        key: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["code", b"code", "key", b"key", "response", b"response"]) -> None: ...

global___Result = Result

@typing_extensions.final
class LoginRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTHCID_FIELD_NUMBER: builtins.int
    SECRET_FIELD_NUMBER: builtins.int
    AUTHZID_FIELD_NUMBER: builtins.int
    TOKEN_EXPIRATION_FIELD_NUMBER: builtins.int
    authcid: builtins.str
    secret: builtins.str
    authzid: builtins.str
    token_expiration: builtins.float
    def __init__(
        self,
        *,
        authcid: builtins.str = ...,
        secret: builtins.str | None = ...,
        authzid: builtins.str | None = ...,
        token_expiration: builtins.float | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_authzid", b"_authzid", "_secret", b"_secret", "_token_expiration", b"_token_expiration", "authzid", b"authzid", "secret", b"secret", "token_expiration", b"token_expiration"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_authzid", b"_authzid", "_secret", b"_secret", "_token_expiration", b"_token_expiration", "authcid", b"authcid", "authzid", b"authzid", "secret", b"secret", "token_expiration", b"token_expiration"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_authzid", b"_authzid"]) -> typing_extensions.Literal["authzid"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_secret", b"_secret"]) -> typing_extensions.Literal["secret"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_token_expiration", b"_token_expiration"]) -> typing_extensions.Literal["token_expiration"] | None: ...

global___LoginRequest = LoginRequest

@typing_extensions.final
class LoginResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESULT_FIELD_NUMBER: builtins.int
    BEARER_TOKEN_FIELD_NUMBER: builtins.int
    @property
    def result(self) -> global___Result: ...
    bearer_token: builtins.str
    def __init__(
        self,
        *,
        result: global___Result | None = ...,
        bearer_token: builtins.str | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_bearer_token", b"_bearer_token", "bearer_token", b"bearer_token", "result", b"result"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_bearer_token", b"_bearer_token", "bearer_token", b"bearer_token", "result", b"result"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_bearer_token", b"_bearer_token"]) -> typing_extensions.Literal["bearer_token"] | None: ...

global___LoginResponse = LoginResponse

@typing_extensions.final
class PingRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___PingRequest = PingRequest

@typing_extensions.final
class PingResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESULT_FIELD_NUMBER: builtins.int
    PYMAP_VERSION_FIELD_NUMBER: builtins.int
    PYMAP_ADMIN_VERSION_FIELD_NUMBER: builtins.int
    @property
    def result(self) -> global___Result: ...
    pymap_version: builtins.str
    pymap_admin_version: builtins.str
    def __init__(
        self,
        *,
        result: global___Result | None = ...,
        pymap_version: builtins.str = ...,
        pymap_admin_version: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["result", b"result"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["pymap_admin_version", b"pymap_admin_version", "pymap_version", b"pymap_version", "result", b"result"]) -> None: ...

global___PingResponse = PingResponse

@typing_extensions.final
class AppendRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    USER_FIELD_NUMBER: builtins.int
    SENDER_FIELD_NUMBER: builtins.int
    RECIPIENT_FIELD_NUMBER: builtins.int
    MAILBOX_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    FLAGS_FIELD_NUMBER: builtins.int
    WHEN_FIELD_NUMBER: builtins.int
    user: builtins.str
    sender: builtins.str
    recipient: builtins.str
    mailbox: builtins.str
    data: builtins.bytes
    @property
    def flags(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    when: builtins.int
    def __init__(
        self,
        *,
        user: builtins.str = ...,
        sender: builtins.str | None = ...,
        recipient: builtins.str | None = ...,
        mailbox: builtins.str | None = ...,
        data: builtins.bytes = ...,
        flags: collections.abc.Iterable[builtins.str] | None = ...,
        when: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_mailbox", b"_mailbox", "_recipient", b"_recipient", "_sender", b"_sender", "mailbox", b"mailbox", "recipient", b"recipient", "sender", b"sender"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_mailbox", b"_mailbox", "_recipient", b"_recipient", "_sender", b"_sender", "data", b"data", "flags", b"flags", "mailbox", b"mailbox", "recipient", b"recipient", "sender", b"sender", "user", b"user", "when", b"when"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_mailbox", b"_mailbox"]) -> typing_extensions.Literal["mailbox"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_recipient", b"_recipient"]) -> typing_extensions.Literal["recipient"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_sender", b"_sender"]) -> typing_extensions.Literal["sender"] | None: ...

global___AppendRequest = AppendRequest

@typing_extensions.final
class AppendResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESULT_FIELD_NUMBER: builtins.int
    MAILBOX_FIELD_NUMBER: builtins.int
    VALIDITY_FIELD_NUMBER: builtins.int
    UID_FIELD_NUMBER: builtins.int
    @property
    def result(self) -> global___Result: ...
    mailbox: builtins.str
    validity: builtins.int
    uid: builtins.int
    def __init__(
        self,
        *,
        result: global___Result | None = ...,
        mailbox: builtins.str = ...,
        validity: builtins.int | None = ...,
        uid: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_uid", b"_uid", "_validity", b"_validity", "result", b"result", "uid", b"uid", "validity", b"validity"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_uid", b"_uid", "_validity", b"_validity", "mailbox", b"mailbox", "result", b"result", "uid", b"uid", "validity", b"validity"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_uid", b"_uid"]) -> typing_extensions.Literal["uid"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_validity", b"_validity"]) -> typing_extensions.Literal["validity"] | None: ...

global___AppendResponse = AppendResponse

@typing_extensions.final
class UserData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ParamsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    PASSWORD_FIELD_NUMBER: builtins.int
    ROLES_FIELD_NUMBER: builtins.int
    PARAMS_FIELD_NUMBER: builtins.int
    password: builtins.str
    @property
    def roles(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def params(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        password: builtins.str | None = ...,
        roles: collections.abc.Iterable[builtins.str] | None = ...,
        params: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_password", b"_password", "password", b"password"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_password", b"_password", "params", b"params", "password", b"password", "roles", b"roles"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_password", b"_password"]) -> typing_extensions.Literal["password"] | None: ...

global___UserData = UserData

@typing_extensions.final
class GetUserRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    USER_FIELD_NUMBER: builtins.int
    ENTITY_TAG_FIELD_NUMBER: builtins.int
    user: builtins.str
    entity_tag: builtins.int
    def __init__(
        self,
        *,
        user: builtins.str = ...,
        entity_tag: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_entity_tag", b"_entity_tag", "entity_tag", b"entity_tag"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_entity_tag", b"_entity_tag", "entity_tag", b"entity_tag", "user", b"user"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_entity_tag", b"_entity_tag"]) -> typing_extensions.Literal["entity_tag"] | None: ...

global___GetUserRequest = GetUserRequest

@typing_extensions.final
class SetUserRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    USER_FIELD_NUMBER: builtins.int
    ENTITY_TAG_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    user: builtins.str
    entity_tag: builtins.int
    @property
    def data(self) -> global___UserData: ...
    def __init__(
        self,
        *,
        user: builtins.str = ...,
        entity_tag: builtins.int | None = ...,
        data: global___UserData | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_entity_tag", b"_entity_tag", "data", b"data", "entity_tag", b"entity_tag"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_entity_tag", b"_entity_tag", "data", b"data", "entity_tag", b"entity_tag", "user", b"user"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_entity_tag", b"_entity_tag"]) -> typing_extensions.Literal["entity_tag"] | None: ...

global___SetUserRequest = SetUserRequest

@typing_extensions.final
class DeleteUserRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    USER_FIELD_NUMBER: builtins.int
    ENTITY_TAG_FIELD_NUMBER: builtins.int
    user: builtins.str
    entity_tag: builtins.int
    def __init__(
        self,
        *,
        user: builtins.str = ...,
        entity_tag: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_entity_tag", b"_entity_tag", "entity_tag", b"entity_tag"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_entity_tag", b"_entity_tag", "entity_tag", b"entity_tag", "user", b"user"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_entity_tag", b"_entity_tag"]) -> typing_extensions.Literal["entity_tag"] | None: ...

global___DeleteUserRequest = DeleteUserRequest

@typing_extensions.final
class UserResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESULT_FIELD_NUMBER: builtins.int
    USER_FIELD_NUMBER: builtins.int
    ENTITY_TAG_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    @property
    def result(self) -> global___Result: ...
    user: builtins.str
    entity_tag: builtins.int
    @property
    def data(self) -> global___UserData: ...
    def __init__(
        self,
        *,
        result: global___Result | None = ...,
        user: builtins.str | None = ...,
        entity_tag: builtins.int | None = ...,
        data: global___UserData | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_entity_tag", b"_entity_tag", "_user", b"_user", "data", b"data", "entity_tag", b"entity_tag", "result", b"result", "user", b"user"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_entity_tag", b"_entity_tag", "_user", b"_user", "data", b"data", "entity_tag", b"entity_tag", "result", b"result", "user", b"user"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_entity_tag", b"_entity_tag"]) -> typing_extensions.Literal["entity_tag"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_user", b"_user"]) -> typing_extensions.Literal["user"] | None: ...

global___UserResponse = UserResponse
