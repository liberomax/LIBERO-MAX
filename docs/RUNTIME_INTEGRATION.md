# Run an evaluation

Start with Lite (800 pairs), then use the same checkpoint and inference settings
on Max (8,000 pairs). The commands below use X-VLA on one GPU. Other public
adapters are listed in the [README](../README.md#supported-model-adapters).

## 1. Prepare the model and simulation environments

Use the model's upstream CUDA environment and a local LIBERO checkpoint. For
X-VLA, `--lerobot-root` must contain the LeRobot X-VLA implementation used by
the checkpoint, including its LIBERO observation processors. Model weights and
model dependencies are installed separately from this benchmark package.

From the LIBERO-MAX repository root, install the benchmark in that environment:

```bash
python -m pip install -e .
```

Plus and PRO use different task registries and data roots. Run them in separate
processes so each case uses its original source environment. Prepare the pinned
source checkouts:

```bash
mkdir -p .deps
git clone https://github.com/sylvestf/LIBERO-plus.git .deps/LIBERO-plus
git -C .deps/LIBERO-plus checkout 4976dc30028e805ff8094b55501d532c48fec182

git clone https://github.com/Zxy-MLlab/LIBERO-PRO.git .deps/LIBERO-PRO
git -C .deps/LIBERO-PRO checkout 2b910b5b5f53016bef9907632f6f840f1ce2229c

python scripts/setup_libero_pro_substrate.py \
  --libero-pro-root .deps/LIBERO-PRO \
  --dataset-root .deps/libero-pro-data \
  --config-dir .deps/libero-pro-config
```

The setup command uses the Hugging Face `hf` CLI to download the pinned PRO
BDDL and initial-state files. Install the simulator dependencies required by
the source repositories in the model environment; the reference runtime uses
MuJoCo 3.2.6 and robosuite 1.4.0. Ensure that the Plus checkout contains its
`libero/libero/bddl_files`, `init_files`, and `assets` directories.

Create an isolated Plus configuration:

```bash
python - <<'PY'
import json
from pathlib import Path
source = Path('.deps/LIBERO-plus/libero/libero').resolve()
config = Path('.deps/libero-plus-config')
config.mkdir(parents=True, exist_ok=True)
paths = {
    'benchmark_root': source,
    'bddl_files': source / 'bddl_files',
    'init_states': source / 'init_files',
    'assets': source / 'assets',
    'datasets': Path('.deps/libero-plus-data').resolve(),
}
(config / 'config.yaml').write_text(json.dumps({k: str(v) for k, v in paths.items()}))
PY
```

## 2. Run the two source groups

Split the frozen manifest by source. This preserves every case ID and event
parameter. Set `MANIFEST=benchmark/max8000/libero_max_8000.json` and a new
`RUN` directory to run Max instead.

```bash
MANIFEST=benchmark/lite/libero_max_lite.json
RUN=artifacts/xvla-lite

python - "$MANIFEST" "$RUN" <<'PY'
import json
import sys
from pathlib import Path
manifest = json.loads(Path(sys.argv[1]).read_text())
output = Path(sys.argv[2])
output.mkdir(parents=True, exist_ok=True)
for source in ('plus', 'pro'):
    cases = [case for case in manifest['cases']
             if (case.get('substrate_variant', {}).get('benchmark') == 'LIBERO-PRO')
             == (source == 'pro')]
    (output / f'{source}.json').write_text(json.dumps({**manifest, 'cases': cases}))
PY

export PYTHONPATH="$PWD/scripts/libero_source_overlay:$PWD/src${PYTHONPATH:+:$PYTHONPATH}"

TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1 \
LIBERO_SOURCE_PACKAGE_ROOT="$PWD/.deps/LIBERO-plus/libero" \
LIBERO_CONFIG_PATH="$PWD/.deps/libero-plus-config" \
python scripts/run_xvla_persistent_benchmark.py "$RUN/plus.json" \
  --output-root "$RUN/plus" --gpus 0 --resume \
  --lerobot-root /path/to/lerobot --checkpoint /path/to/checkpoint \
  --query-interval 30

LIBERO_SOURCE_PACKAGE_ROOT="$PWD/.deps/LIBERO-PRO/libero" \
LIBERO_CONFIG_PATH="$PWD/.deps/libero-pro-config" \
python scripts/run_xvla_persistent_benchmark.py "$RUN/pro.json" \
  --output-root "$RUN/pro" --gpus 0 --resume \
  --lerobot-root /path/to/lerobot --checkpoint /path/to/checkpoint \
  --query-interval 30
```

The Plus command enables loading the pinned source’s NumPy initial-state
files with recent PyTorch versions. Replace the two model paths with the same
checkout and checkpoint in both commands. `--gpus 0,1` enables two GPUs; `--resume` skips completed cases.
For another model, use its adapter and native query interval in both runs.

## 3. Aggregate against the complete manifest

```bash
python scripts/aggregate_cosmos_benchmark.py "$RUN/plus" \
  --case-root "$RUN/pro" --manifest "$MANIFEST" \
  --output-dir "$RUN/summary" --query-interval 30 --require-render-qa
```

Despite its historical filename, this aggregator is shared by the public
adapters. It writes `benchmark_summary.json` and `end_to_end_results.jsonl`.
Use the end-to-end Base and Dynamic success rates and their paired difference.
A complete result accounts for all 800 Lite or 8,000 Max pairs. Check
`coverage.execution_complete`; repair missing or invalid runs before reporting.
Valid task failures and unreached triggers remain in the denominator.

## Add a model adapter

The common shard interface is:

```text
runner.py MANIFEST --output-root ROOT --shard-index I --num-shards N --resume [model arguments]
```

Load `cases[I::N]`, keep one policy instance resident, and write each case below
`ROOT/cases/CASE_ID`. Use the [X-VLA shard](../scripts/run_xvla_persistent_shard.py)
as the complete example. It restores the same initial state and policy seed,
replays Base actions exactly until the event, applies the stored intervention,
and records both terminal outcomes. Keep the initial-state and action-prefix
checks: they establish that a Base/Dynamic pair is valid.

`scripts/run_dynamic_benchmark.py` provides optional dynamic GPU scheduling
for this interface. Give it one source group at a time with the matching
source environment. Resource scheduling does not change event timing or
model inference settings.
