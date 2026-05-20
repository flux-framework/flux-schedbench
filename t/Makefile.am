TEST_EXTENSIONS = .t .py

T_LOG_DRIVER = env AM_TAP_AWK='$(AWK)' $(SHELL) \
	$(top_srcdir)/config/tap-driver.sh
PY_LOG_DRIVER = $(FLUX) python $(top_srcdir)/config/tap-driver.py

AM_TESTS_ENVIRONMENT = \
	export PYTHONPATH="$(abs_top_srcdir)/src/bindings/python:$(PYTHON_SITE_PACKAGES):$$PYTHONPATH"; \
	export PYTHON="${PYTHON}"; \
	export FLUX="${FLUX}";

clean-local:
	rm -fr trash-directory.* test-results .prove *.broker.log python/__pycache__



# TESTSCRIPTS lists both sharness (.t) and Python (.py) tests.
# Python tests run standalone via tap-driver.py; they call
# subflux.rerun_under_flux() to re-exec themselves inside a Flux instance.
TESTSCRIPTS = \
	python/t6000-schedbench-bulkrun.py \
	python/t6030-schedbench-benchmarks.py \
	python/t6031-schedbench-locality.py \
	python/t6040-schedbench-ui.py \
	t6020-schedbench.t

TESTS = $(TESTSCRIPTS)
dist_check_SCRIPTS = $(TESTSCRIPTS)

EXTRA_DIST = \
    sharness.sh \
    sharness.d \
    scripts
