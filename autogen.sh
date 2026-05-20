#!/bin/sh
#
# flux-schedbench is a Python-only project — no libtool needed.
# Just run autoreconf to generate the configure script.
#
echo "Running autoreconf --force --verbose --install"
autoreconf --force --verbose --install || exit
echo "Now run ./configure."
