# flux-schedbench

Scheduler benchmarks for the [Flux](https://flux-framework.org) resource
manager. Measures submit throughput, allocation rates, and placement quality
against fake or real resources, and saves results for later comparison.

## Requirements

- [flux-core](https://github.com/flux-framework/flux-core) ≥ 0.85.0 (with
  `pkgutil` namespace-package support in `flux/__init__.py`)
- Python ≥ 3.6

## Build and install

```sh
./autogen.sh
/path/to/flux ./configure
make install
```

`./configure` detects the prefix automatically when `flux` is in `PATH`.
Pass an explicit prefix with `--prefix=/path/to/flux` if needed.

## Subcommands

### `flux schedbench run TEST [OPTIONS]`

Run a named benchmark. By default a fresh Flux subinstance is launched with
fake resources; pass `--exec` to benchmark the current enclosing instance
instead.

Key options:

| Flag | Default | Description |
|------|---------|-------------|
| `-N, --nodes` | 4 | Fake-resource node count |
| `-c, --cores-per-node` | 64 | Cores per node |
| `-g, --gpus-per-node` | 8 | GPUs per node |
| `--njobs` | 1000 | Jobs to submit |
| `--scheduler` | `sched-simple` | Scheduler module to load |
| `--scheduler-options` | — | Module options string (shlex-parsed) |
| `--hwloc-xml-path` | — | Per-node hwloc XML for topology-aware runs |
| `--amend-r` | — | Python callable to mutate R before KVS write |
| `--tag` | — | Free-form label stored in the result |
| `--results-file` | `./schedbench-results.json` | Output file |
| `-x, --exec` | — | Run against the current enclosing instance |

### `flux schedbench sweep [TEST] [OPTIONS]`

Run a cross-product parameter study as parallel Flux jobs. Comma lists and
[RFC 45](https://flux-framework.readthedocs.io/projects/flux-rfc/en/latest/spec_45.html)
ranges (e.g. `16-1024:2`) become sweep axes; scalars stay fixed. A live
dashboard tracks progress across the matrix.

Pass `--from FILE.toml` for structured sweep definitions including
multi-module scheduler recipes.

### `flux schedbench report TEST [OPTIONS]`

Pretty-print results for a benchmark from the results file.

## Benchmarks

**`throughput`** — Submit *N* jobs as fast as possible. Headline metric:
throughput (jobs/sec, broker-side from submit to clean). Also records
submit, alloc, ingest, and script-wall rates.

**`fill-machine`** — Submit jobs sized to saturate the resource set, then
cancel. Measures how fast the scheduler fills the machine and cancels work
en masse.

**`locality`** — Score how well the scheduler packs each slot's cores and
GPUs into a single NUMA/socket domain. Requires `--hwloc-xml-path`.
Headline metric: mean locality fraction (0–1).

## Examples

Basic throughput run against 4-node fake cluster:

```sh
flux schedbench run throughput --njobs=500
```

Larger cluster with a non-default scheduler:

```sh
flux schedbench run throughput -N 100 --cores-per-node=32 \
    --scheduler=sched-fluxion-qmanager \
    --scheduler-options="queue-depth=64"
```

Locality benchmark on a synthetic NUMA topology:

```sh
lstopo -i "package:2 numa:4 core:8 pu:1" --of xml > syn.xml
flux schedbench run locality -N 16 --hwloc-xml-path=./syn.xml \
    --nslots=2 --slot-cores=4 --njobs=200
```

Parameter sweep over node counts and job counts:

```sh
flux schedbench sweep throughput \
    --nodes=16,32,64,128 --njobs=4096,8192
```

Or from a TOML sweep file:

```sh
flux schedbench sweep --from sweep.toml
```

Print results:

```sh
flux schedbench report throughput
```

## Development

Run the test suite:

```sh
make check
```

Tests require a working `flux` in `PATH` (or `FLUX` set in the
environment). The Python unit tests (`t/python/`) run without a broker;
the sharness tests (`t/*.t`) launch their own Flux subinstances.

Code style is enforced by [pre-commit](https://pre-commit.com):

```sh
pip install pre-commit
pre-commit install
```
