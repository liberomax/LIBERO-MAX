# Tests

The CPU test suite checks the manifests, event runtime, paired scoring, and
model-adapter interfaces. It does not download model checkpoints or run GPU
evaluations.

```bash
python -m pip install -e . numpy pytest
make test
```

To validate the two released manifests only, run `make validate`.
