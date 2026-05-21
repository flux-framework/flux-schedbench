flux-schedbench version 0.1.0 - 2026-05-21
------------------------------------------

Initial release of flux-schedbench, a scheduler benchmarking tool for
the [Flux](https://flux-framework.org) resource manager.

## Subcommands

 * `flux schedbench run TEST` runs a named benchmark against a
   fresh fake-resources subinstance (default) or the current enclosing
   instance (`--exec`).  Results are appended to a JSON results file
   for later comparison.
 * `flux schedbench report TEST` pretty-prints results from the results
   file as a table.  Supports named formats, user-defined formats via
   `~/.config/flux/`, `--filter`, and `--sort`.
 * `flux schedbench sweep` runs a full parameter-matrix sweep.  Each
   axis-capable flag (`--nodes`, `--njobs`, `--scheduler`, etc.) accepts
   a scalar, comma list, or RFC 45 range to define sweep axes; the
   cross-product drives parallel Flux jobs.  Sweeps can also be defined
   in TOML files via `--from`.

## Benchmarks

 * `throughput` — submits N jobs and measures submit, allocation, start,
   and completion rates.
 * `fill-machine` — saturates the scheduler by submitting enough jobs to
   fill every slot, then measures time-to-fill and allocation rate.
 * `locality` — measures placement quality under topology-aware
   scheduling; supports `--duration=fill` and `--duration=count` modes.

## Features

 * Fake-resources mode launches a single-broker `flux start` subinstance
   configured with synthetic R (via `flux-config-fake-resources(5)`),
   isolating benchmarks from real cluster state.
 * `--scheduler` selects the scheduler module loaded in the subinstance
   (default: `sched-simple`); `--scheduler-options` passes module args.
 * `--hwloc-xml-path` and `--amend-r` support topology-aware benchmarks
   (e.g. Fluxion with NUMA topology injected into R).
 * Two event-watcher implementations: `journal` (single KVS-watch
   subscription) and `per-job` (one subscription per job) selectable
   via `--watcher`.
 * Interactive terminal UI with live progress bars and a metrics summary;
   falls back to a JSON event stream when stdout is not a TTY.
 * `pip install flux-schedbench` installs the tool into PATH for use
   with any flux-core installation.
