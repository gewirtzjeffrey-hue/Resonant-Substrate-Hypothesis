# RSH v11.2 — Reproducibility Package

This `/code` folder contains minimal scripts to reproduce the key quantities in the manuscript.

## Scripts

- `run_mi_ringdown.py` — compute MI(τ) and fit **gamma_MI** from a single-column CSV `h`.
- `compute_spectral_decay.py` — compute **gamma_spec** from the amplitude envelope (Hilbert) and fit an exponential.
- `fit_invariant_ratio.py` — combine the outputs and compute **F = gamma_MI / (2 * gamma_spec)**.

## Quickstart

```bash
# Create a virtual environment (optional)
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r code/requirements.txt

# Assume you have data/strain.csv with one column named 'h' and sampling interval dt=1.0e-4 s
python code/run_mi_ringdown.py --input data/strain.csv --dt 1.0e-4 --max_lag 4000 --out mi_fit.json
python code/compute_spectral_decay.py --input data/strain.csv --dt 1.0e-4 --out spec_fit.json
python code/fit_invariant_ratio.py --mi mi_fit.json --spec spec_fit.json --out invariant.json
```

### Input format
- `data/strain.csv` → one column named `h` (uniformly sampled).  
- `--dt` → sampling interval in seconds.

### Outputs
- `mi_fit.json` → estimated gamma_MI and fit diagnostics.  
- `spec_fit.json` → estimated gamma_spec and fit diagnostics.  
- `invariant.json` → F ratio and the two gammas.

### Citation
If you use these scripts, please cite the Zenodo DOIs:
- v10.1 (Empirical Validation Edition): 10.5281/zenodo.17422850
- v11.2 (Manuscript Edition): 10.5281/zenodo.17443377
