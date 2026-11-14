Prime-counting entry using an odd-only sieve of Eratosthenes.

Run command: `sh run.sh` (reads N from stdin, prints pi(N) to stdout).

Language: C (gcc/cc, no dependencies).

| N | pi(N) |
|---:|---:|
| 10 | 4 |
| 100 | 25 |
| 1000 | 168 |
| 100000 | 9592 |
| 1000000 | 78498 |

`primes.b64` is a prebuilt x86-64 Linux binary of primes.c (base64), so the run command skips compilation when present; the C source is authoritative and builds with `gcc -O3 -o primes primes.c`.
