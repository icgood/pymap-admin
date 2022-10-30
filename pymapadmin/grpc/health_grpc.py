# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: pymapadmin/grpc/health.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

import pymapadmin.grpc.health_pb2


class HealthBase(abc.ABC):

    @abc.abstractmethod
    async def Check(self, stream: 'grpclib.server.Stream[pymapadmin.grpc.health_pb2.HealthCheckRequest, pymapadmin.grpc.health_pb2.HealthCheckResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Watch(self, stream: 'grpclib.server.Stream[pymapadmin.grpc.health_pb2.HealthCheckRequest, pymapadmin.grpc.health_pb2.HealthCheckResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/grpc.health.v1.Health/Check': grpclib.const.Handler(
                self.Check,
                grpclib.const.Cardinality.UNARY_UNARY,
                pymapadmin.grpc.health_pb2.HealthCheckRequest,
                pymapadmin.grpc.health_pb2.HealthCheckResponse,
            ),
            '/grpc.health.v1.Health/Watch': grpclib.const.Handler(
                self.Watch,
                grpclib.const.Cardinality.UNARY_STREAM,
                pymapadmin.grpc.health_pb2.HealthCheckRequest,
                pymapadmin.grpc.health_pb2.HealthCheckResponse,
            ),
        }


class HealthStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Check = grpclib.client.UnaryUnaryMethod(
            channel,
            '/grpc.health.v1.Health/Check',
            pymapadmin.grpc.health_pb2.HealthCheckRequest,
            pymapadmin.grpc.health_pb2.HealthCheckResponse,
        )
        self.Watch = grpclib.client.UnaryStreamMethod(
            channel,
            '/grpc.health.v1.Health/Watch',
            pymapadmin.grpc.health_pb2.HealthCheckRequest,
            pymapadmin.grpc.health_pb2.HealthCheckResponse,
        )
