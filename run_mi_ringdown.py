#!/usr/bin/env python3
# Compute mutual information (MI) vs lag from a 1D time series and fit an exponential:
#     I(tau) = A * exp(-gamma_MI * tau) + C
#
# Usage:
#     python run_mi_ringdown.py --input data/strain.csv --dt 1.0e-4 --max_lag 4000 --out mi_fit.json [--bins 64]
#
# Input:
#     CSV with a single column named 'h' containing uniformly sampled values.
#     --dt is the sampling interval in seconds.
#
# Output:
#     JSON file with estimated gamma_MI and basic diagnostics.

import argparse
import json
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

def mi_hist(x, y, bins=64):
    """Simple histogram-based mutual information estimate."""
    c_xy, _, _ = np.histogram2d(x, y, bins=bins)
    p_xy = c_xy / np.sum(c_xy)
    p_x = np.sum(p_xy, axis=1, keepdims=True)
    p_y = np.sum(p_xy, axis=0, keepdims=True)

    eps = 1e-12
    with np.errstate(divide='ignore', invalid='ignore'):
        term = p_xy * (np.log(p_xy + eps) - np.log(p_x + eps) - np.log(p_y + eps))
    term[np.isnan(term)] = 0.0
    return float(np.sum(term))

def exp_model(tau, A, gamma, C):
    return A * np.exp(-gamma * tau) + C

def main():
    ap = argparse.ArgumentParser(description="Compute MI(τ) and fit γ_MI from a 1D time series.")
    ap.add_argument("--input", required=True, help="CSV with column 'h' (strain / signal)")
    ap.add_argument("--dt", type=float, required=True, help="Sampling interval in seconds")
    ap.add_argument("--max_lag", type=int, default=4000, help="Maximum lag in samples")
    ap.add_argument("--bins", type=int, default=64, help="Histogram bins for MI estimate")
    ap.add_argument("--out", required=True, help="Output JSON path for fit results")
    args = ap.parse_args()

    # Load data
    df = pd.read_csv(args.input)
    if 'h' not in df.columns:
        raise ValueError("Input CSV must contain a single column named 'h'.")
    h = df['h'].to_numpy().astype(float)

    # Compute MI vs lag
    lags = np.arange(1, args.max_lag + 1, dtype=int)
    mi_vals = np.empty_like(lags, dtype=float)
    for i, L in enumerate(lags):
        mi_vals[i] = mi_hist(h[:-L], h[L:], bins=args.bins)
    tau = lags * args.dt  # seconds

    # Initial parameter guesses for exponential fit
    tail_n = max(10, len(mi_vals) // 10)
    C0 = float(np.mean(mi_vals[-tail_n:]))
    A0 = float(max(mi_vals[0] - C0, 1e-6))
    g0 = 1.0 / max(1e-6, 0.1 * tau.max())  # weakly informative
    p0 = [A0, g0, C0]

    popt, pcov = curve_fit(exp_model, tau, mi_vals, p0=p0, maxfev=20000)
    A, gamma_mi, C = map(float, popt)

    out = {
        "gamma_mi": gamma_mi,
        "A": A,
        "C": C,
        "dt": float(args.dt),
        "max_lag": int(args.max_lag),
        "bins": int(args.bins),
        "n_samples": int(h.size),
        "notes": "Histogram MI estimate with exponential fit: I(tau)=A*exp(-gamma_MI*tau)+C"
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
