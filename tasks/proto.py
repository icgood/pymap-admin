# type: ignore

from invoke import task, Collection

from .check import check_import


@task
def fetch_health_proto(ctx):
    """Download the latest canonical health.proto file."""
    ctx.run("""curl -o {}/grpc/health.proto \
            https://raw.githubusercontent.com/grpc/grpc-proto/master/grpc/health/v1/health.proto
            """.format(ctx.package))


@task(check_import)
def compile(ctx):
    """Run the protoc compiler."""
    ctx.run('python -m grpc_tools.protoc '
            '@{}/grpc/grpc_tools.protoc-args'.format(ctx.package))


@task(fetch_health_proto, compile)
def all(ctx):
    """Run all proto utilities."""
    pass


ns = Collection(fetch_health_proto, compile)
ns.add_task(all, default=True)
