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
admin server over a UNIX socket, typically in `/tmp/pymap/pymap-admin.sock`.
See the `pymap-admin --help` commands for other connection options.

## Commands

### `save-args` Command

When administering remote pymap servers, it can be cumbersome to always supply
connection arguments every time, such as `--host`. This command saves the
arguments it is given to a config file.

```console
$ pymap-admin --host imap.example.com --port 50051 save-args
Config file written: /home/user/.config/pymap/pymap-admin.conf
```

### `login` Command

Sends login credentials and gets a bearer token. See
[Authentication](#authentication) for more information.

```console
$ pymap-admin login -is user@example.com
user@example.com Password:
result {
  response: ". OK Login completed."
}
bearer_token: "MDAwZWxvY2F0aW9uIAowMDMwaWRlbnRpZmllciA0ZmM4MD..."
```

### `ping` Command

Pings the running server and reports its version string.

```console
$ pymap-admin ping
pymap_version: "0.21.1"
pymap_admin_version: "0.5.2"
```

### `append` Command

To append a message directly to a mailbox, without using IMAP, use the
`append` admin command. First, check out the help:

```console
$ pymap-admin append --help
```

As a basic example, you can append a message to a like this:

```console
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

```console
$ pymap-admin set-user --help
$ pymap-admin get-user --help
$ pymap-admin delete-user --help
```

Passing a username to `get-user` will display that user's metadata, including
the (securely hashed) password string. A username can be deleted with
`delete-user`. The `set-user` command will create and update a username and its
password.

If using pymap as part of the [slimta-docker][4] configuration, see its
[Address Management][5] documentation for additional options.

## Authentication

Every command except [`ping`](#ping-command) requires authentication to
perform. Most commands will send a [macaroon][6] token to authenticate, except
for [`login`](#login-command) which uses the credentials provided.

When running `pymap-admin` and `pymap` on the same machine, a temporary file
containing an admin token is used by default, allowing unrestricted access to
all operations. This token is verified in-memory and is only valid for the
*current* `pymap` process.

To use this admin token on another machine, copy the `PYMAP_ADMIN_TOKEN=...`
line printed out on `pymap` startup and prefix it to `pymap-admin` calls, e.g.:

```console
$ PYMAP_ADMIN_TOKEN=... pymap-admin get-user user@example.com
```

### Permanent Tokens

For a token that is not tied to the current `pymap` process, use the
[`login`](#login-command) with the credentials of a user in the system. The
resulting token can be used to authenticate as that user in the future.

```console
$ pymap-admin login -is user@example.com
```

The `-s` flag will cause the token to be saved and used on future `pymap-admin`
commands. Use `--token-file` or `$PYMAP_ADMIN_TOKEN_FILE` to specify a
location, otherwise it is saved to `~/.pymap-admin.token`.

If `-s` is not given, the `bearer_token` value from the output can provided to
future `pymap-admin` commands with `$PYMAP_ADMON_TOKEN`.

### Admin Role

The builtin pymap backends use a special key "role" to assign admin privileges
to existing users, authorizing them to run `pymap-admin` commands on other
users.

```console
$ pymap-admin set-user --param role=admin user@example.com
```

This role may only be assigned by users that already have it, or by
authenticating using the admin token.

[1]: https://github.com/icgood/pymap
[2]: https://grpc.io/
[3]: https://github.com/vmagamedov/grpclib
[4]: https://github.com/slimta/slimta-docker
[5]: https://github.com/slimta/slimta-docker#address-management
[6]: https://github.com/ecordell/pymacaroons
