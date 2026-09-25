<div align="center">

<h1><img src="assets/brand/liberomax_wordmark_white.svg?v=20260924" width="520" alt="LIBERO-MAX"></h1>

### Do Robot Policies Adapt When the World Changes?

[![Project](https://img.shields.io/badge/Project-website-a7444e?style=flat-square)](https://liberomax.github.io/)
[![Paper](https://img.shields.io/badge/Paper-coming%20soon-6b7280?style=flat-square)](#citation)
[![LIBERO-MAX](https://img.shields.io/badge/LIBERO--MAX-8%20events-a7444e?style=flat-square)](benchmark/max8000)
[![Pairs](https://img.shields.io/badge/Pairs-8%2C000-62676e?style=flat-square)](benchmark/max8000)
[![Evaluated](https://img.shields.io/badge/Evaluated-14%20policies-62676e?style=flat-square)](#results)

[Dataset](benchmark/max8000) · [LIBERO-MAX Lite](benchmark/lite) · [Benchmark specification](docs/BENCHMARK_SPEC.md) · [Evaluation guide](docs/RUNTIME_INTEGRATION.md)

</div>

![LIBERO-MAX benchmark overview](assets/figures/benchmark_overview.png?v=20260924)

LIBERO-MAX measures whether robot policies remain effective when the world changes **after execution has begun**. Each case pairs a **Base** rollout, which retains the source configuration, with a **Dynamic** rollout that replays the same executed prefix and then receives one controlled event. The task, initial state, instruction, and policy seed are shared. This matched comparison measures the effect of adding a change to an ongoing task.

## LIBERO-MAX and LIBERO-MAX Lite

Both tracks use the same paired protocol and eight event types.

| Benchmark | Pairs | Use |
|---|---:|---|
| **LIBERO-MAX** | 8,000 | Full evaluation |
| **LIBERO-MAX Lite** | 800 | Fast checks |

Lite is a fixed subset of Max, with 100 pairs per event. Use Lite to check an
adapter, then Max for final reporting.

The eight online changes cover four event families:

- **Geometry:** target relocation and receptacle relocation.
- **Observation:** camera shift and sensor-noise onset.
- **Appearance and clutter:** illumination switch, visual-theme switch, and distractor burst.
- **Path constraint:** obstacle insertion.

### Lineage and acknowledgements

![Construction of LIBERO-MAX from LIBERO, LIBERO-Plus, and LIBERO-PRO](assets/figures/benchmark_construction.png?v=20260924)

Built on [LIBERO](https://arxiv.org/abs/2306.03310), with 5,600 source cases from
[LIBERO-Plus](https://arxiv.org/abs/2510.13626) and 2,400 from
[LIBERO-PRO](https://arxiv.org/abs/2510.03827). Each source case becomes a matched
Base/Dynamic pair with one change during execution.

See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) for the complete attribution and license notes.

<p align="center">
  <img src="assets/media/target-relocation.gif" width="24%" alt="Target relocation">
  <img src="assets/media/camera-shift.gif" width="24%" alt="Camera shift">
  <img src="assets/media/illumination-switch.gif" width="24%" alt="Illumination switch">
  <img src="assets/media/obstacle-insertion.gif" width="24%" alt="Obstacle insertion">
</p>

## Results

### Every policy loses success after an online change

All fourteen policies are evaluated on the same **8,000 Base/Dynamic pairs**.
Success falls by **11.0–25.7 percentage points** after an event, with every
paired 95% bootstrap interval below zero.

![Base and Dynamic success for all fourteen policies on the full LIBERO-MAX benchmark](assets/figures/performance_gap.png?v=20260924)

Among tasks solved in Base, **20.8%–56.1% become failures** in Dynamic. Paired
outcomes distinguish these regressions from tasks that fail in both conditions
or become successful after the change.

![Paired task outcomes and conditional regression across fourteen policies](assets/figures/paired_outcomes.png?v=20260924)

### Geometry and observation changes reveal shared vulnerabilities

Target relocation causes the largest loss for eleven policies. Camera shifts
and sensor noise expose additional policy-specific weaknesses, while
illumination and visual-theme changes are generally milder.

![Dynamic success loss from Base by event type](assets/figures/change_type_breakdown.png?v=20260924)

### Camera controls separate viewpoint difficulty and execution history

We compare **Base, change at Reset, and change Mid-task** on all **1,000 camera
cases per policy** for X-VLA, π0.5, and HiMem-WAM, totaling 9,000 rollouts.
The changed view can already impair performance from the first input. Mid-task
success exceeds Reset for all three policies, showing that performance also
depends on the trajectory from which the changed view is encountered.
The cohort contains 700 Plus and 300 PRO cases; π0.5 uses H = 10 and Q = 5
here, compared with H = 50 in the primary benchmark.

![Paired camera-control contrasts across three policies on 1,000 cases each](assets/figures/camera_paired_contrasts.png?v=20260924)

### Changing query cadence alone leaves a substantial gap

On the same 800 matched pairs per policy, Dynamic success remains **11.1–23.0
points below Base** across all 18 tested settings. The best serving cadence
depends on the policy. For X-VLA and GR00T N1.7, the decoded action horizon
changes with the query interval.

![Base and Dynamic success across valid query cadences](assets/figures/action_cadence.png?v=20260924)

### A targeted response partially recovers the sensor-noise loss

On a separate fixed set of **300 sensor-noise cases**, image restoration
improves X-VLA without retraining. Quality gating uses the current images,
without an event flag or clean reference image.

| Processing | Base SR (%) | Dynamic SR (%) | Dynamic gain (pp), paired 95% CI |
|---|---:|---:|---:|
| Native | 66.7 | 40.7 | — |
| Always-on | 68.3 | 47.3 | +6.7 [2.3, 11.0] |
| Quality-gated | 67.0 | 47.7 | +7.0 [3.0, 11.3] |

<details>
<summary><strong>Additional analyses: Lite validation, camera strength, coverage, and source breakdowns</strong></summary>

#### Lite tracks the full benchmark

Lite estimates the reported success rates and gaps within 2.4 points of Max
and preserves 88 of 91 pairwise Dynamic orderings.

![LIBERO-MAX and LIBERO-MAX Lite validation](assets/figures/max_lite_validation.png?v=20260924)

#### Milder camera shifts

X-VLA retains a positive Mid-task versus Reset difference at quarter, half,
and full shift strength on the same 1,000 camera cases. Both changed-view
conditions remain below Base even at quarter strength.

![X-VLA success under quarter, half, and full camera-shift strength](assets/figures/camera_strength_success.png?v=20260924)

#### Event exposure and response coverage

Trigger and post-event query coverage distinguish reaching the event from
receiving feedback after it. All assigned cases remain in the success-rate
denominator.

![Event-trigger and post-event response diagnostics](assets/figures/mechanism_diagnostics.png?v=20260924)

#### Source-category breakdowns

The source analyses show how paired losses vary across the Plus and PRO
categories used to construct LIBERO-MAX.

![Summary of paired losses across source categories](assets/figures/source_category_summary.png?v=20260924)

![Paired success changes across LIBERO-Plus source categories](assets/figures/source_categories_plus.png?v=20260924)

![Paired success changes across LIBERO-PRO source categories](assets/figures/source_categories_pro.png?v=20260924)

</details>

## Quick start

```bash
git clone https://github.com/liberomax/LIBERO-MAX.git
cd LIBERO-MAX
python -m pip install -e .
make validate
```

For one example, use X-VLA on a single GPU. First prepare the model environment,
source checkouts, and split manifests using the [evaluation guide](docs/RUNTIME_INTEGRATION.md).
Then run the Plus group:

```bash
PYTHONPATH="$PWD/scripts/libero_source_overlay:$PWD/src${PYTHONPATH:+:$PYTHONPATH}" \
LIBERO_SOURCE_PACKAGE_ROOT="$PWD/.deps/LIBERO-plus/libero" \
LIBERO_CONFIG_PATH="$PWD/.deps/libero-plus-config" \
TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1 \
python scripts/run_xvla_persistent_benchmark.py artifacts/xvla-lite/plus.json \
  --output-root artifacts/xvla-lite/plus --gpus 0 --resume \
  --lerobot-root /path/to/lerobot --checkpoint /path/to/checkpoint \
  --query-interval 30
```

The guide includes the PRO run and aggregation for the complete 800-pair Lite
evaluation. To evaluate Max, use its 8,000-pair manifest with the same checkpoint
and inference settings.

## Repository structure

```text
LIBERO-MAX/
├── benchmark/
│   ├── max8000/              # Full 8,000-pair manifest and source revisions
│   └── lite/                 # Fixed 800-pair manifest and selection record
├── schemas/                 # Manifest, scenario, and result schemas
├── src/libero_max/           # Validation, pairing, events, and evaluation utilities
├── scripts/                  # Model adapters, aggregation, and figure generation
├── examples/                 # Small scenario and paired-result examples
├── tests/                    # Protocol, release, and launcher checks
├── docs/                     # Benchmark specification and evaluation guide
└── assets/figures/           # Figures rendered in this README
```

## Authors

Yunbei Zhang, Zijian Jin, Yuanzhe Liu, Janet Wang, Xilun Zhang, Yuyou Zhang,
Zhenyu Zhang, Daoan Zhang, Shuaicheng Niu, Gen Li, Jianfei Yang, Jihun Hamm,
Ismini Lourentzou, Weirui Ye, Bo Liu, Peter Stone, Marco Pavone.

## Citation

The paper PDF and BibTeX will be added after release. For now, please cite the repository URL:

```text
https://github.com/liberomax/LIBERO-MAX
```
