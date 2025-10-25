#!/usr/bin/env python3
# Combine gamma_MI and gamma_spec to compute the Gewirtz Invariant:
#   F = gamma_MI / (2 * gamma_spec)
#
# Usage:
#   python fit_invariant_ratio.py --mi mi_fit.json --spec spec_fit.json --out invariant.json
import argparse, json, math, time

def main():
    ap = argparse.ArgumentParser(description='Compute the Gewirtz Invariant F = gamma_MI / (2*gamma_spec).')
    ap.add_argument('--mi', required=True, help='JSON produced by run_mi_ringdown.py')
    ap.add_argument('--spec', required=True, help='JSON produced by compute_spectral_decay.py')
    ap.add_argument('--out', default='invariant.json', help='output JSON')
    args = ap.parse_args()

    with open(args.mi, 'r', encoding='utf-8') as f:
        mi = json.load(f)
    with open(args.spec, 'r', encoding='utf-8') as f:
        sp = json.load(f)

    gamma_mi = float(mi['gamma_mi'])
    gamma_spec = float(sp['gamma_spec'])
    F = gamma_mi / (2.0 * gamma_spec)

    out = {
        'gamma_mi': gamma_mi,
        'gamma_spec': gamma_spec,
        'F': F,
        'definition': 'F = gamma_MI / (2 * gamma_spec)',
        'timestamp': int(time.time())
    }
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()
