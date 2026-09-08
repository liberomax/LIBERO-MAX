# LIBERO-MAX Benchmark Specification

Status: current released benchmark, version 3.0.0. This specification describes
LIBERO-MAX (Max) and LIBERO-MAX Lite (Lite), as used in the fourteen-policy
paper evaluation.

## Evaluation tracks

| Track | Matched pairs per policy | Scored rollouts per policy | Source composition | Use |
| --- | ---: | ---: | --- | --- |
| Max | 8,000 | 16,000 | 5,600 Plus-derived + 2,400 PRO-derived | Primary benchmark reporting |
| Lite | 800 | 1,600 | 560 Plus-derived + 240 PRO-derived | Integration, ablation, early comparison |

The [Max manifest](../benchmark/max8000/libero_max_8000.json) fixes all case
IDs and event parameters. [Lite](../benchmark/lite/README.md) is a deterministic
subset of Max, selected from manifest metadata with seed `20260830` without
inspecting policy outcomes. Each event contributes 100 Lite pairs: 70
Plus-derived and 30 PRO-derived. Case membership is shared across checkpoints
and query cadences. Use the same checkpoint and released native serving
configuration when comparing a policy on Max and Lite.

The source tasks cover LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-10.
A case ID identifies a task instance and a frozen event configuration; 8,000
pairs do not mean 8,000 unique tasks.

## Matched Base and Dynamic episodes

Each case has two arms, called `control` and `intervention` in the manifest:

- **Base:** execute the task without an exogenous event.
- **Dynamic:** share the task, instruction, initial simulator state, policy
  seed, and executed pre-event action prefix, then apply exactly one frozen
  event during execution.

Both arms use the original LIBERO goal-completion predicate. The comparison
measures the outcome effect of adding one online event after the shared
prefix. It does not compare the same perturbation at reset and during execution,
or establish internal detection and replanning.

The paired protocol requires exact pre-event replay, not merely matching reset
seeds. Adapters must record and verify the initial-state and action-prefix
agreement before their results are aggregated.

## Eight events and four reporting families

Each Max event contains 1,000 pairs; each Lite event contains 100 pairs.

| Reporting family | Event | Manifest `change_type` |
| --- | --- | --- |
| Observation | Camera shift | `camera_shift` |
| Observation | Sensor-noise onset | `sensor_noise_onset` |
| Geometry | Target relocation | `target_relocation` |
| Geometry | Receptacle relocation | `receptacle_relocation` |
| Appearance and clutter | Illumination switch | `illumination_switch` |
| Appearance and clutter | Visual-theme switch | `visual_theme_switch` |
| Appearance and clutter | Distractor burst | `distractor_burst` |
| Path constraint | Obstacle insertion | `obstacle_insertion` |

These are the paper's reporting families. Legacy `change_family` codes in the
versioned manifests are retained for compatibility; use the explicit event
mapping above when reproducing the four-family tables.

## Frozen cases and event timing

Every case records its suite, task index, initial-state index, policy seed,
scenario ID, trigger, and resolved change payload. Intervention randomness is
resolved when the manifest is built. Evaluation must apply those stored values
without resampling event directions, object identities, or poses.

Use the trigger in each released case. Record the event step, the next
post-event observation/query, and the actions executed between them. The
policy's native observation cadence and action commitment are part of its
reported inference configuration. Trigger coverage and post-event response-query
coverage are separate diagnostics.

A policy that terminates before the trigger has a valid `trigger_unreached`
outcome; it is not an infrastructure error or a reason to remove the case.
Likewise, an event with no subsequent policy query remains in the end-to-end
score and is identified separately in response-conditioned diagnostics.

## Reporting and coverage

For each policy and track, report:

1. The planned denominator and completed, missing, invalid, and duplicate case
   counts, with outcomes for both arms.
2. Base success rate, Dynamic success rate, and the paired difference
   `Dynamic SR - Base SR`, in percentage points.
3. The four paired outcomes: preserved success `(1,1)`, change-associated success
   `(0,1)`, event-associated regression `(1,0)`, and persistent failure `(0,0)`.
4. Conditional regression: the share of Base successes that fail in Dynamic,
   `count(1,0) / [count(1,1) + count(1,0)]`.
5. Confidence intervals and paired tests, plus event, task-suite, source, and
   source-category breakdowns.
6. Checkpoint identity, native inference settings, trigger coverage, and
   post-event response-query coverage.

All headline rates use the full frozen denominator. Missing records must never
be dropped to inflate success. Infrastructure and trace-integrity errors must
be repaired and rerun before an evaluation is declared complete. They are
reported separately from valid task failures and unreached triggers.

The current comparison contains fourteen complete Max evaluations. Model-family
labels describe the evaluated policies; heterogeneous training and serving
protocols prevent interpreting family differences as a controlled architecture
comparison. See the [README results](../README.md#results).

## Release validation and integration

From the repository root:

```bash
make validate
```

The [Lite release guide](../benchmark/lite/README.md) provides the deterministic
selection record and a runnable evaluation example. The [README quick
start](../README.md#quick-start) provides installation and one model example.
The [runtime integration guide](RUNTIME_INTEGRATION.md) provides environment setup,
source-specific evaluation commands, aggregation, and the common adapter
interface.
