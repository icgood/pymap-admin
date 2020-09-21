pymap-admin
===========

[![Build Status](https://travis-ci.com/icgood/pymap-admin.svg?branch=master)](https://travis-ci.com/icgood/pymap-admin)
[![Coverage Status](https://coveralls.io/repos/icgood/pymap-admin/badge.svg)](https://coveralls.io/r/icgood/pymap-admin)
[![PyPI](https://img.shields.io/pypi/v/pymap-admin.svg)](https://pypi.python.org/pypi/pymap-admin)
[![PyPI](https://img.shields.io/pypi/pyversions/pymap-admin.svg)](https://pypi.python.org/pypi/pymap-admin)
[![PyPI](https://img.shields.io/pypi/l/pymap-admin.svg)](https://pypi.python.org/pypi/pymap-admin)

The `pymap-admin` tool can be used to perform various admin functions against a
running pymap server. This is a separate [grpc][2] service using [grpclib][3]
listening on a socket.

#### [API Documentation](https://icgood.github.io/pymap-admin/)

### Connections

By default, the `pymap-admin` command will attempt to interact with a pymap
admin server over a UNIX socket, typically in `/tmp/pymap/pymap-adin.sock`.
With the `--host` or `$PYMAP_ADMIN_HOST` options, you can use a TCP connection
(the default grpc port is 50051). However, the pymap admin service must also be
configured to listen on a port, using either of these options:

```
pymap ... --admin-private 127.0.0.1:50051 ...
pymap ... --admin-public 0.0.0.0:9090 ...
```

The `--admin-private` option will function exactly like the UNIX socket: all
operations will succeed unencrypted and without authentication. As such, a
"private" admin service port should be properly firewalled.

The `--admin-public` option is safe to expose publicly. It is SSL/TLS encrypted
using the same certificate as your IMAP sockets, and commands are authenticated
on a per-user basis. For example, to append a message to a user's INBOX, that
user must authenticate:

```
pymap-admin --password=... append user@example.com
# or $PYMAP_ADMIN_PASSWORD
# or --ask-password
```

## Commands

#### [API Documentation](http://icgood.github.io/pymap-admin/)

### `ping` Command

Pings the running server and reports its version string.

```
$ pymap-admin ping
server_version: "0.14.1"
```

### `append` Command

To append a message directly to a mailbox, without using IMAP, use the
`append` admin command. First, check out the help:

```
$ pymap-admin append --help
```

As a basic example, you can append a message to a like this:

```
$ cat <<EOF | pymap-admin append demouser
> From: user@example.com
>
> test message!
> EOF
mailbox: "INBOX"
validity: 1784302999
uid: 101

2.0.0 Message delivered
```

### User Commands

These commands access and manipulate the users on the system:

```
$ pymap-admin list-users --help
$ pymap-admin set-user --help
$ pymap-admin get-user --help
$ pymap-admin delete-user --help
```

The `list-users` command lists all usernames on the system, one per line.
Passing a username to `get-user` will display that user's metadata, including
the (securely hashed) password string. A username can be deleted with
`delete-user`. The `set-user` command will create and update a username and its
password.

If using pymap as part of the [slimta-docker][4] configuration, see its
[Address Management][5] documentation for additional options.

[1]: https://github.com/icgood/pymap
[2]: https://grpc.io/
[3]: https://github.com/vmagamedov/grpclib
[4]: https://github.com/slimta/slimta-docker
[5]: https://github.com/slimta/slimta-docker#address-management
