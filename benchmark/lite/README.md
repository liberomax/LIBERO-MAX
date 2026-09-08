# LIBERO-MAX Lite

LIBERO-MAX Lite is the fixed 800-pair evaluation track for rapid policy
integration, ablation, and early comparison. It is a strict subset of the
released LIBERO-MAX benchmark and uses the same paired protocol and event
taxonomy.

The split contains 100 cases from each of the eight online event types. Every
event contains 70 LIBERO-Plus cases and 30 LIBERO-PRO cases, preserving the
70:30 source composition of LIBERO-MAX. A persistent pseudorandom generator with seed
`20260830` selects the outcome-blind subset before any policy result is
inspected. These are also the fixed case IDs used by the cadence analysis. The
same case IDs apply to every checkpoint and every query cadence.

| Benchmark | Matched pairs | Scored rollouts per checkpoint | Intended use |
| --- | ---: | ---: | --- |
| LIBERO-MAX | 8,000 | 16,000 | Primary benchmark reporting |
| LIBERO-MAX Lite | 800 | 1,600 | Integration, debugging, ablation, early comparison |

The manifest records the benchmark default query interval for schema
compatibility. Model evaluations should apply the same released native query
cadence in LIBERO-MAX Lite and LIBERO-MAX. Case membership is independent of
query cadence.

Validate the release:

```bash
make validate-lite
```

Rebuild it deterministically from LIBERO-MAX:

```bash
python scripts/build_lite_split.py
```

## Evaluate a checkpoint

Follow the [evaluation guide](../../docs/RUNTIME_INTEGRATION.md) using
`benchmark/lite/libero_max_lite.json`. It runs the 560 Plus-derived and 240
PRO-derived cases in their matching environments and aggregates all 800 pairs.
Use the same checkpoint and native inference settings for both source groups
and for the subsequent Max evaluation.

`case_index.csv` lists the released cases. `selection_summary.json` records the
selection seed, quotas, and source manifest.
