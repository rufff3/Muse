#!/bin/sh

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
cd "$SCRIPT_DIR" || exit 1

if [ -f primes.b64 ]; then
    base64 -d primes.b64 > primes || exit $?
    chmod +x primes || exit $?
else
    if ! cc -O3 -o primes primes.c; then
        gcc -O3 -o primes primes.c || exit $?
    fi
fi

exec ./primes
