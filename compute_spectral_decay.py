#!/usr/bin/env python3
# Estimate spectral/energy decay constant gamma_spec from a 1D time series.
# Method: amplitude envelope via Hilbert transform, fit E(t) = A * exp(-gamma_spec * t) + C
#
# Usage:
#   python compute_spectral_decay.py --input data/strain.csv --dt 1.0e-4 --out spec_fit.json [--start 0.0] [--end -1]
#
# Inputs:
#   --input : CSV with a single column named 'h'
#   --dt    : sampling interval in seconds
#   --start : optional start time (sec) for fitting window (default 0.0)
#   --end   : optional end time (sec) for fitting window (default -1 = until end)
#
# Output:
#   JSON with gamma_spec and fit diagnostics.
import argparse, json
import numpy as np
import pandas as pd
from scipy.signal import hilbert
from scipy.optimize import curve_fit

def exp_model(t, A, gamma, C):
    return A * np.exp(-gamma * t) + C

def main():
    ap = argparse.ArgumentParser(description='Estimate gamma_spec via Hilbert envelope exponential fit.')
    ap.add_argument('--input', required=True, help='CSV with column h')
    ap.add_argument('--dt', type=float, required=True, help='sampling interval in seconds')
    ap.add_argument('--out', required=True, help='output JSON path')
    ap.add_argument('--start', type=float, default=0.0, help='fit window start time (sec)')
    ap.add_argument('--end', type=float, default=-1.0, help='fit window end time (sec), -1 for end')
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    if 'h' not in df.columns:
        raise ValueError("Input CSV must contain a single column named 'h'.")
    h = df['h'].to_numpy().astype(float)

    # Envelope
    env = np.abs(hilbert(h))
    n = env.size
    t = np.arange(n) * args.dt

    # Fit window
    t0 = max(0.0, args.start)
    t1 = t[-1] if args.end < 0 else min(args.end, t[-1])
    mask = (t >= t0) & (t <= t1)
    t_fit = t[mask]
    e_fit = env[mask]

    # Initial guesses
    # Offset ~ median of last 10% of window
    tail_n = max(10, int(0.1 * e_fit.size))
    C0 = float(np.median(e_fit[-tail_n:]))
    A0 = float(max(e_fit.max() - C0, 1e-8))
    g0 = 1.0 / max(1e-6, 0.1 * (t_fit[-1] - t_fit[0] if t_fit.size > 1 else args.dt))
    p0 = [A0, g0, C0]

    bounds = ([0.0, 0.0, 0.0], [np.inf, np.inf, np.inf])
    popt, pcov = curve_fit(exp_model, t_fit, e_fit, p0=p0, bounds=bounds, maxfev=200000)
    A, gamma_spec, C = map(float, popt)

    out = {
        "gamma_spec": gamma_spec,
        "A": A,
        "C": C,
        "dt": float(args.dt),
        "start": float(t0),
        "end": float(t1),
        "n_samples": int(n),
        "notes": "Hilbert envelope exponential fit E(t)=A*exp(-gamma_spec*t)+C"
    }
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()
