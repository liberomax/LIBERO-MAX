# LIBERO-MAX paper experiment matrix

Status: current fourteen-policy evaluation on Max and the fixed Lite subset.
The [benchmark specification](BENCHMARK_SPEC.md) defines the released protocol;
the [README results](../README.md#results) and [project
website](https://yunbeizhang.github.io/LIBERO-MAX/) show the corresponding figures.

## Complete primary comparison

Every policy below has 8,000 matched Base/Dynamic pairs on Max and is audited on
the same fixed 800-pair Lite subset. There are eight VLA policies, one VLA+WAM
policy, and five WAM policies. Each checkpoint uses its released native inference
configuration; the table is a comparison of policies under those protocols.

Rates are percentages; the gap is Dynamic minus Base in percentage points.
Values are rounded independently from the full-precision results.

| Family | Policy | Max Base SR | Max Dynamic SR | Max gap |
| --- | --- | ---: | ---: | ---: |
| VLA | π0.5 | 79.7 | 65.7 | -13.9 |
| VLA | OpenVLA-OFT | 64.3 | 43.2 | -21.1 |
| VLA | X-VLA | 62.6 | 37.7 | -24.9 |
| VLA | Xiaomi-Robotics-0 | 70.3 | 52.0 | -18.3 |
| VLA | MolmoAct2 | 80.3 | 66.9 | -13.4 |
| VLA | SmolVLA | 26.1 | 15.0 | -11.0 |
| VLA | GR00T N1.7 | 69.3 | 50.0 | -19.3 |
| VLA | DM0.5 | 79.8 | 62.1 | -17.7 |
| VLA+WAM | VLA-JEPA | 73.5 | 54.3 | -19.2 |
| WAM | Cosmos-Policy | 77.4 | 59.3 | -18.2 |
| WAM | Fast-WAM | 42.0 | 24.0 | -18.0 |
| WAM | HiMem-WAM | 73.0 | 57.7 | -15.3 |
| WAM | Light-WAM | 54.8 | 37.3 | -17.5 |
| WAM | DiT4DiT | 65.1 | 39.4 | -25.7 |

Every policy loses 11.0 to 25.7 success-rate points. Among Base successes,
20.8% to 56.1% become failures after the online event. These are completed
results; no additional policy run is required to fill the primary table.

## Max and Lite coverage

Max combines 5,600 Plus-derived and 2,400 PRO-derived pairs. Lite is the fixed
800-pair subset containing 100 pairs per event, with 70 Plus-derived and 30
PRO-derived cases in each event. The Lite selection seed is `20260830`.

Across all fourteen policies, Lite differs from Max by at most 2.4 points over
Base rates, Dynamic rates, and paired gaps. It preserves 88 of 91 pairwise
Dynamic orderings. The three local differences involve X-VLA versus DiT4DiT,
Xiaomi-Robotics-0 versus VLA-JEPA, and Light-WAM versus DiT4DiT; the last pair
ties on Lite. Max remains the primary reporting track.

The earlier 800-case PRO-only comparison pool is not LIBERO-MAX Lite. Use
[`benchmark/lite`](../benchmark/lite/README.md) for the released Lite manifest
and membership, and [`benchmark/max8000`](../benchmark/max8000) for Max.

## Completed cadence analysis

The current paper reports the completed action-cadence sweep for X-VLA, π0.5,
GR00T N1.7, and Fast-WAM on the same fixed 800-pair pool. It contains 18 valid
policy/cadence settings, or 14,400 matched pairs. These ablations are reported
separately from each policy's native-protocol primary result.

## Partial diagnostic and adapter availability

Mimic-Video is an appendix-only diagnostic with 5,972 supported Max pairs across
LIBERO-Spatial, LIBERO-Object, and LIBERO-Goal. The public release has no
LIBERO-10 checkpoint, leaving 2,028 unsupported pairs. Its supported-scope Base
and Dynamic success rates are 56.7% and 31.9%, a 24.8-point decrease. It is
excluded from the fourteen-policy main table, headline ranges, rankings, and
cross-policy statistics.

The public repository includes integrations for π0.5, OpenVLA-OFT, X-VLA,
VLA-JEPA, Cosmos-Policy, Fast-WAM, and LingBot-VA. LingBot-VA is a reference
integration and is not a primary paper row. Model-side adapters for the other
evaluated policies are not redistributed here. See the [supported adapter
list](../README.md#supported-model-adapters) for the public entry points.

## Historical and future work

The earlier [paper plan](PAPER_PLAN.md) describes the v1 physical/intent tracks,
notification ablations, and development milestones. Those records are separate
from the current Max/Lite evaluation. The [human feasibility review
procedure](HUMAN_FEASIBILITY_REVIEW.md) describes secondary review; a queued
case is not a completed human demonstration.

Direct adaptation diagnostics, latent-residual interruption, and multiple-event
extensions are future research directions. They are not included among the
completed results above.
