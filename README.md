pymap-admin
===========

[![Build Status](https://travis-ci.org/icgood/pymap-admin.svg?branch=master)](https://travis-ci.org/icgood/pymap-admin)
[![Coverage Status](https://coveralls.io/repos/icgood/pymap-admin/badge.svg)](https://coveralls.io/r/icgood/pymap-admin)
[![PyPI](https://img.shields.io/pypi/v/pymap-admin.svg)](https://pypi.python.org/pypi/pymap-admin)
[![PyPI](https://img.shields.io/pypi/pyversions/pymap-admin.svg)](https://pypi.python.org/pypi/pymap-admin)
[![PyPI](https://img.shields.io/pypi/l/pymap-admin.svg)](https://pypi.python.org/pypi/pymap-admin)

The `pymap-admin` tool can be used to perform various admin functions against a
running pymap server. This is a separate [grpc][2] service using [grpclib][3]
listening on a port, typically 9090.

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

[1]: https://github.com/icgood/pymap
[2]: https://grpc.io/
[3]: https://github.com/vmagamedov/grpclib
