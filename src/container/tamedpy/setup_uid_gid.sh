#!/usr/bin/bash

# Quit on error.
set -e
# Treat undefined variables as errors.
set -u

function main {
  local sb_uid="${1:-}"
  local sb_gid="${2:-}"

  # Change the uid
    if [[ -n "${sb_uid:-}" ]]; then
        usermod -u "${sb_uid}" sandboxuser
    fi
    # Change the gid
    if [[ -n "${sb_gid:-}" ]]; then
        groupmod -g "${sb_gid}" sandboxuser
    fi

    # Setup permissions on the run directory where the sockets will be
    # created, so we are sure the app will have the rights to create them.

    # Make sure the folder exists.
    mkdir /tmp/py
    # Set owner.
    chown sandboxuser /tmp/py
    # Set permissions.
    chmod u=rwX,g=rwX,o=--- /tmp/py
}

main "$@"
