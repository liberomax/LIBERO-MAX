<div align="center">

<h1><img src="assets/brand/liberomax_wordmark_white.svg?v=20260911" width="520" alt="LIBERO-MAX"></h1>

### Do robot policies adapt when the world changes during execution?

[![Paper](https://img.shields.io/badge/Paper-coming%20soon-6b7280?style=flat-square)](#citation)
[![LIBERO-MAX](https://img.shields.io/badge/LIBERO--MAX-8%2C000%20pairs-a7444e?style=flat-square)](benchmark/max8000)
[![Evaluated](https://img.shields.io/badge/Evaluated-14%20policies-62676e?style=flat-square)](#results)
[![Website](https://img.shields.io/badge/Project-website-111827?style=flat-square)](https://liberomax.github.io/)

[Dataset](benchmark/max8000) · [LIBERO-MAX Lite](benchmark/lite) · [Benchmark specification](docs/BENCHMARK_SPEC.md) · [Evaluation guide](docs/RUNTIME_INTEGRATION.md)

</div>

![LIBERO-MAX benchmark overview](assets/figures/benchmark_overview.png?v=20260911)

LIBERO-MAX measures whether a robot policy preserves task success after an **exogenous change introduced during execution**. Every Dynamic rollout is paired with a no-event Base control that shares the task, reset state, instruction, policy seed, and executed action prefix. The pair differs only when one frozen event is applied to Dynamic, isolating the outcome effect of adding that online change. The benchmark does not infer whether a policy internally detected the event or deliberately replanned.

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

![Construction of LIBERO-MAX from LIBERO, LIBERO-Plus, and LIBERO-PRO](assets/figures/benchmark_construction.png?v=20260911)

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

### Full benchmark results

Across fourteen policies, one online event reduces success by 11.0–25.7 points;
20.8%–56.1% of Base successes become Dynamic failures. Lite estimates the
reported rates and gaps within 2.4 points of Max and preserves 88 of 91 Dynamic
rank orderings.

![LIBERO-MAX and LIBERO-MAX Lite validation](assets/figures/max_lite_validation.png?v=20260911)

### Where policies lose success

The event-level view reports Dynamic success loss from the matched Base control. Geometry and observation changes produce the largest median losses, with substantial checkpoint-specific variation.

![Dynamic success loss from Base by event type](assets/figures/change_type_breakdown.png?v=20260911)

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

## Citation

The paper PDF and BibTeX will be added after release. For now, please cite the repository URL:

```text
https://github.com/liberomax/LIBERO-MAX
```
