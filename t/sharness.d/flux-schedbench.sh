#
# project-local sharness extras for flux-schedbench
#

# Add the source tree's Python bindings to PYTHONPATH so that
# flux.schedbench.* is importable without a prior `make install`.
PYTHONPATH="${SHARNESS_TEST_SRCDIR}/../src/bindings/python:${PYTHONPATH}"
export PYTHONPATH

FLUX_EXEC_PATH_PREPEND="${SHARNESS_TEST_SRCDIR}/../src/cmd"
export FLUX_EXEC_PATH_PREPEND
